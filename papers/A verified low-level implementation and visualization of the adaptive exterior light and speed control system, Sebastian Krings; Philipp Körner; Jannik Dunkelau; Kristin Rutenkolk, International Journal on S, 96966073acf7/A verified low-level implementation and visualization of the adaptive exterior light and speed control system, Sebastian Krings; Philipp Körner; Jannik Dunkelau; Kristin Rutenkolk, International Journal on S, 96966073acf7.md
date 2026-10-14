International Journal on Software Tools for Technology Transfer (2024) 26:403–419
https://doi.org/10.1007/s10009-024-00750-5

    GENERAL
    Special Section: ABZ 2020/2021


A veriﬁed low-level implementation and visualization of
the adaptive exterior light and speed control system
Sebastian Krings1 · Philipp Körner2 · Jannik Dunkelau2 · Kristin Rutenkolk2


Accepted: 29 April 2024 / Published online: 27 May 2024
© The Author(s) 2024


Abstract
In this article, we present an approach to the ABZ 2020 case study that diﬀers from those usually presented at ABZ:
Rather than using a (correct-by-construction) approach following a formal method, we use C for a low-level implementation
instead. We strictly adhere to test-driven development for validation, and only afterwards apply model checking using CBMC
for veriﬁcation. While the approach has several beneﬁts compared to the more rigorous approaches, it also provides less
mathematical clarity and overall less thorough veriﬁcation. In consequence, our realization of the ABZ case study serves
as a baseline reference for comparison, allowing to assess the beneﬁt provided by the various formal modeling languages,
methods and tools.

Keywords Model checking · Formal methods · Veriﬁcation · Case study · Test-driven development · MISRA C

1 Introduction                                                        not common, yet. To do so, we implemented both the ELS
                                                                      and the SCS directly in (MISRA) C, following a test-driven
The ABZ 2020 Case Study [28] describes two assistants com-            development workﬂow. Only afterwards, we attempted for-
monly found in modern cars. The overall system consists of            mal veriﬁcation directly on the C code, using the CBMC
two loosely coupled components, the adaptive exterior light           model checker [18]. Both MISRA C and CBMC will be in-
system (ELS) and the speed control system (SCS). The ELS              troduced more thoroughly in Sects. 2.1 and 6.2, respectively.
controls head- and taillights, while the SCS controls the vehi-       Test-driven development and mocking of test objects will be
cle’s speed. Both have to take into account the environment           presented in Sect. 2.2.
and parameters deﬁned by the driver. Obviously, both are
safety critical components, rendering safety and security a           Rationale Sometimes formal methods’ practitioners claim
development priority.                                                 to hold a high ground over “traditional” software devel-
   In this article, we present our implementation of ELS              opment or at least claim that there rarely are disadvan-
and SCS. Our approach diﬀers from the other case study                tages [11, 24]. The argument seems convincing; yet, only
implementations in that we do not employ a fully formal de-           a few case studies have compared two teams working on the
velopment method. Instead, we attempted an approach closer            same project, one employing a formal approach and the other
to what might happen in industry, where formal methods are            working “traditionally”.
                                                                          One such study has been performed by Fitzgerald et
 P. Körner                                                           al. [12, 22] in cooperation with British Aerospace Systems
      p.koerner@hhu.de                                                and Equipment Ltd. The authors show that the teams behave
      S. Krings                                                       and develop diﬀerently, i.e., they focus on diﬀerent areas
      sebastian.krings@hhu.de                                         of the system in development. While the formal approach
      J. Dunkelau                                                     used in the study shows its merits, the authors also identify
      jannik.dunkelau@hhu.de                                          drawbacks due to the so far unknown methodology and a
      K. Rutenkolk                                                    requirement for training.
      kristin.rutenkolk@hhu.de                                            Furthermore, Larsen et al. [35] have discussed how to in-
                                                                      tegrate formal methods in a step-wise fashion. Comparable to
1     Independent researcher, Düsseldorf, Germany                     our approach, the authors incrementally add formal aspects
2     Institut für Informatik, Heinrich-Heine-Universität,            to an already existing development process. Their incremen-
      Universitätsstr. 1, D-40225 Düsseldorf, Germany                 tal approach is also veriﬁed by comparing two groups of


                                                                                                                           Springer
404                                                                                                                   S. Krings et al.


developers, one working with traditional tools for require-
ment analysis and one working with the workﬂow supported
by formal speciﬁcation. Again, formal methods proof to be
beneﬁcial if integrated into an existing workﬂow both delib-
erately and thoroughly.
   For this case study, we aim at providing a baseline for com-
parison with fully formal approaches or other approaches
combining formal and informal veriﬁcation, e.g., as sug-
gested for spacecrafts [43].
   We opted to postpone veriﬁcation as much as possible, to
allow a fair evaluation of (dis-)advantages of the individual
approaches. Our aim is to examine whether a rigorous ap-
proach is beneﬁcial in the context of the case study. If so,
we hope to add to the body of evidence that formal methods         Fig. 1 Meeting in a Virtual Seminar Room. The added avatars and
                                                                   higher immersion are supposed to increase collaboration during the
actually are beneﬁcial compared to “traditional” software
                                                                   COVID-19 pandemic
development.

Distinctive features Several features render our approach
                                                                   done by SK and PK. Both the ad-hoc and 3D visualization
unique: Firstly, as the implementation is written in C, it could
be directly deployed to an embedded system. Models written         was provided by KR due to her individual knowledge in this
in formal speciﬁcation languages would have to be reﬁned           area.
to an implementation level before code can be generated.
Furthermore, code generators usually are not proven and            Collaboration       We believe the ways and techniques for
might introduce new errors. In cases where code generation         collaboration can inﬂuence the overall quality of the results
is not easily applicable, side-by-side development of code is      produced by a team of developers, especially when it comes
suggested. However, this approach is error-prone as well.          to safety critical software. As we were working from diﬀerent
    Secondly, the implementation is close to actual hardware.      locations, we used asynchronous messaging via Mattermost1
Code that interacts with sensors or user input is separated,       for coordination and progress reports. The code was version-
i.e., it could immediately be linked to real sensors. Addi-        controlled using Git and GitHub. Finally, during the COVID-
tionally, our implementation makes use of threads, just as         19 pandemic, we additionally employed the software Gather2
the subcomponents of the system would run in parallel. We          for synchronous meetings discussing progress and next steps.
expect that most speciﬁcations using formal methods simply         In Gather, one controls an avatar through a virtual world,
allow some nondeterminism concerning the ordering of state
                                                                   and video conferences are started automatically based on
transitions.
                                                                   predeﬁned rooms or proximity. A screenshot of the authors
    In consequence, our implementation allows real-time sim-
                                                                   meeting in Gather is shown in Fig. 1.
ulation of the system, whereas state transitions in formal
methods usually happen instantly and do not amount for any
time elapsed. This also allows usage of our implementation         Additional contributions     This article is based on our
for hardware-in-the-loop tests, which are common for auto-         case study submission [34] and extends it by
motive software [21, 41].
                                                                   • a discussion on how the given requirements are represented
    Thirdly, C together with the MISRA rules restricting its
                                                                     and how far we can trace the impact of requirements on
usage stems from the automotive industry and is widely used
in practice. Thus, our implementation closely mimics real-           the implementation,
world development conditions.                                      • a thorough presentation of our approach to development,
                                                                   • improved visualization,
Team overview       Our team comes from a formal methods           • additional information on the development team, as well
background: While all members are very familiar with the             as the tools and techniques used,
B method [1, 2], we did not have particular expertise with         • an evaluation of readability and comprehensibility of our
C development or veriﬁcation tooling for C. The basic code           implementation, and
structure and the ﬁxture for the test scenarios were developed     • a comparison to the other case studies.
by SK and PK in a synchronous meeting. Afterwards, SK
implemented the ELS, JD was responsible for the SCS, and            1 https://mattermost.com/.
tests were provided by PK and KR. Formal veriﬁcation was            2 https://www.gather.town/.


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                             405


2 Background on used methodology and                                           Afterwards, the code is extended and improved to make
  tools                                                                     the test pass. As a result, a high test coverage and result-
                                                                            ing conﬁdence is achieved. Furthermore, the test suite helps
Our implementation complies with MISRA C and was de-                        during later refactorings.
veloped in a test-driven manner. Afterwards, CBMC was                          To simplify formulating tests and to allow testing program
employed for formal veriﬁcation. Below, we brieﬂy intro-                    parts in isolation, mocks can be used. A mock is an object
duce these methods and tools.                                               or library that simulates the input and output behavior of
   Since the actual code was C, we were also able to make                   program parts [7]. However, rather than implementing the
full use of common development tools and for example indi-                  full functionality, mocks are usually much simpler than the
vidually choose a preferred IDE or Editor, such as Qt Creator               code they replace. For instance, mocks often behave deter-
and Visual Studio Code.                                                     ministically or even to provide constant outputs. For testing
                                                                            purposes, mocks can record their inputs and provide them to
2.1 MISRA C                                                                 assertions.

MISRA C is a set of development and style guidelines for C,                 2.3 CBMC
introduced by MISRA, the Motor Industry Software Relia-
bility Association. The standard [40] deﬁnes a subset of C                  CBMC [18] is a model checker for programs written in C. It
meant to be used for safety critical systems, in particular in              uses bounded model checking [8] to verify a default set of
the automotive sector. In fact, both ISO 26262 [29] and the                 properties, mostly related to common programming errors,
software speciﬁcation by AUTOSAR [23] suggest the usage                     such as:
of MISRA C for automotive applications.                                     • memory safety, including bounds checks and pointer
   The overall goal of MISRA C is to increase both safety and                 safety,
security by avoiding common pitfalls. Thus, the rules pro-                  • occurrence and treatment of exceptions, and
hibit or discourage the use of unsafe constructs, try to avoid              • absence of undeﬁned behavior due to C quirks.
ambiguities, and so on. The MISRA C standard distinguishes
                                                                            While those are worthwhile to ﬁnd and correct, they only
between three kinds of rules: those that are mandatory, those
                                                                            ensure general correctness but not adherence to the require-
that are required but could be ignored if a rationale is given,
                                                                            ments.
and rules that are advisory only. For instance, there is a re-
                                                                               To check individual properties, CBMC can be used to
quired rule stating that any switch statement should have
                                                                            verify user-given assertions stated as C-style assertions using
a default label and a mandatory rule stating that any path
                                                                            the macros in assert.h.
through a nonvoid function should end in a return statement.
   While most rules could be checked by hand, we used cp-
pcheck3 to verify compliance of our implementation. Given                   3 Case study overview
that some rules are undecidable, the result is only an indica-
tion and manual review is required as well.                                 The proposed case study for the ABZ 2020 [28] concerns
   Despite its prevalence, MISRA C has been criticized re-                  itself with two software-realized assistant systems from the
garding both eﬃciency and ease of use. In particular, the                   automotive domain, namely an adaptive exterior light system
possibilities of false positives [27] and of introducing new                (ELS) and a speed control system (SCS). The two software
errors by (thoughtlessly) changing code to adhere to the                    systems are parameterized with conﬁguration options that
rules [9] should be carefully considered. Despite the criti-                account for diﬀerent vehicle speciﬁcations either based on
cism, MISRA C remains the de facto standard in the auto-                    country-speciﬁc regulations or individual orders. These pa-
motive industry and is used throughout all production code                  rameters are:
in this case study.
                                                                            • an indicator on which side the driver seat is placed to
2.2 Test-driven development and mocking                                       distinguish between left- or right-hand traﬃc,
                                                                            • a market code specifying whether the car was build for the
Test-driven Development is an approach to software develop-                   USA, Canada, or the EU, and
ment that follows a certain development cycle: before imple-                • the information whether the vehicle is armored,
menting a new feature or ﬁxing an issue, an appropriate test                and are referenced throughout the listed requirements. While
case is formulated and executed [7]. Without code change,                   these parameters are shared by both subsystems, the case
the test is expected to fail.                                               study speciﬁcation deﬁnes further sensors, actuators, user
                                                                            interface, and functional requirements for the ELS and the
 3 http://cppcheck.sourceforge.net.                                         SCS individually.


                                                                                                                                   Springer
406                                                                                                                  S. Krings et al.


3.1 Adaptive exterior light system                                increases desired speed by 10 km/h) which might be time-
                                                                  sensitive (SCS-8: holding lever above 7◦ point for 2 seconds
The ELS speciﬁcation concerns itself with the exterior light-     increases speed every 2 seconds to next ten’s place), reactions
ing of the vehicle. This includes low and high beam head-         of the SCS to braking (SCS-16: turn cruise control oﬀ when
lights, a cornering light when turning left or right, the turn    brake is pushed), or reaction to predicted collisions (SCS-28:
signal, and the emergency brake light. The driver controls        if time to impact is less than time for standstill, activate brake
it via a rotary switch, a control lever (referred to as pitman    at 100%).
arm), a hazard warning light switch, and a darkness switch
(which only exists in armored vehicles).
    The ELS has 49 functional requirements speciﬁed (ELS-1        4 Requirements and modeling strategy
to ELS-49) which are grouped into 8 categories:
                                                                  In this section, we give an overview on how we transformed
• Direction blinking (ELS-1 to ELS-7),                            the requirements into code and test, our validation strategy
• Hazard warning light (ELS-8 to ELS-13),                         and the limitations of our implementation.
• Low beam headlights and cornering light (ELS-14 to ELS-
  29),                                                            4.1 Process from requirements to code and
• Manual high beam headlights (ELS-30 to ELS-31),                     assertions
• Adaptive high beam headlights (ELS-32 to ELS-38),
• Emergency brake light (ELS-39 to ELS-30),                       We used the requirements given in the case study descrip-
• Reverse light (ELS-41), and                                     tion without further modiﬁcation or transformation. For each
• Fault handling (ELS-42 to ELS-49).                              requirement we covered, we generated:
   Exemplary speciﬁcations include duration of ﬂashing            • Unit tests, which are used for test-driven development. See
light cycles (ELS-10: ﬂashing cycle duration is 1 second), sit-     Sect. 6.1 for details.
uational light activations (ELS-27: in reverse gear, both cor-    • Assertions to be checked via CBMC as presented in Sect. 6.
nering lights are active), default brightness factors (ELS-29:      These assertions are meant to verify that properties hold
100% for all lights), or behavior based on time-sensitive user      in general rather than just in the test scenarios.
input (ELS-2 vs. ELS-4: diﬀerent ﬂashing behavior when
                                                                     The validation sequences were taken from an Excel ﬁle
holding the pitman arm for less than 0.5 seconds or longer).
                                                                  and encoded in integration tests, using the same techniques
                                                                  as the unit tests.
3.2 Speed control system                                             Using CBMC to verify assertions can, of course, result
                                                                  in counterexamples. Those are given as traces, which can
The speciﬁcation for the SCS outlines behavior and func-          be used to create additional validation sequences by replac-
tionality for a cruise control and an adaptive cruise control,    ing erroneous steps by desired ones. Again, these tests can
a distance warning, emergency brake assist, a speed limit,        then be used to improve the implementation and ensure the
traﬃc sign recognition, and traﬃc jam following. The driver       absence of the counterexample.
interacts with the SCS by means of a cruise control lever,           The combined approach using both testing for validation
the brake pedal, the gas pedal, and the instrument cluster.       and model checking for veriﬁcation has its merits and pro-
Meanwhile the vehicle can give feedback and notiﬁcations          vides a high degree of certainty. However, it also has its
by means of a visual and an acoustic signal.                      drawbacks. In particular, the double meaning of assertions
   The SCS comprises 43 requirements (SCS-1 to SCS-41)            can lead to confusion: C-style asserts are used both to encode
grouped into 8 categories:                                        properties for CBMC and to fail tests. Yet, there is no com-
• Setting and modifying desired speed (SCS-1 to SCS-12),          bined methodology to react on failing assertions and errors
• Cruise control (SCS-13 to SCS-17),                              uncovered by model checking have to be handled diﬀerently
• Adaptive cruise control (SCS-18 to SCS-24),                     from failing tests.
• Distance warning (SCS-15 and SCS-26),
                                                                  4.2 Code structure
• Emergency brake assistant (SCS-27 and SCS-28),
• Speed limit (SCS-29 to SCS-35),
                                                                  The overall architecture of our implementation is depicted in
• Traﬃc Sign Detection (SCS-36 to SCS-39), and
                                                                  Fig. 2. We follow a structure that is fairly similar to that the
• Fault handling and general properties (SCS-40 to SCS-43).
                                                                  speciﬁcation provides. Since two subsystems are speciﬁed,
  Exemplary speciﬁcations include behavior changes of the         the code is separated into two folders, one for the cruise
SCS given user input (SCS-4: pushing lever above 7◦ point         control and the other for the light system. This is to help


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                              407


Fig. 2 System Architecture and
Internal Communication. ELS
and SCS are strictly decoupled;
clock, sensors, and driver input
are external to the controlling
system itself




                                                                            Table 1 Development Time
ensure that the systems are independent of each other. Shared
type deﬁnitions, e.g., the pedal deﬂection, the sensor state                Task                                                   Time (h)
enumeration, and shared sensors, are stored separately. An
artiﬁcial time sensor was introduced for testing, but can easily            basic implementation and code structure                2
be replaced by an actual clock.                                             ELS implementation, tests and scenarios                30
   Each of the subsystems is split into three header ﬁles and               SCS implementation, tests and scenarios                22
implementations. The ﬁrst header ﬁle declares the accessible                model checking                                         3
and shared sensors for the subsystem, and contains relevant                 refactoring and code cleanup                           2
type deﬁnitions. Another header ﬁle deﬁnes the user inter-                  state visualization                                    6
face, e.g., how the pitman arm may be moved or what input
                                                                            domain-speciﬁc visualization                           25
the pedals for gas and brakes may yield. The last header ﬁle
contains deﬁnitions for the actuators, i.e., what the system is
allowed to do. Only the latter two header ﬁles are actually                 4.3 Traceability of requirements
implemented, eventually resulting in three C ﬁles:
• A state struct that contains all the data relevant to the                 As the other case studies, we do not employ a fully for-
  subsystem.                                                                mal approach to traceability. The only form of traceabil-
• The user interface to simulate inputs. This changes some                  ity we provide is by using naming patterns. Our unit tests
  internal variables that keeps track of the state of the UI;               in general contain the requirement they are concerned
  in a deployed system, this can be replaced by additional                  with in the name of the test routine. Larger integration
  sensors. The attributes correspond to the signals that the                tests also reference the validation sequence they represent,
  subsystem has to communicate.                                             which in turn contains the requirements justifying individual
• The realization of the state machine with several guarded                 steps.
  state transitions. This is the actual implementation of the                  As a consequence, we can only trace which test cases are
  speciﬁed safety properties.                                               validating certain requirements and to what extent require-
   For the test cases, sensors are mocked. In order to get                  ments are covered. An example is given in listing 5, in which
an actual executable, real sensors have to be linked during                 we called the test els3_a_left. This indicates it is a test for
compilation. The time spend for development, validation and                 ﬁrst part (a) of the requirements ELS-3, which focuses on the
veriﬁcation is given in Table 1.                                            left-hand side direction blinking. Comments aside, we have
   For the sake of brevity, we will only show small code                    no link between a requirement and the individual part of the
snippets in this paper. The full implementation is available at             code realizing it. One could argue that there is a such a link
https://github.com/wysiib/abz2020-case-study-in-c-public.                   due to the nature of test-driven development and the use of


                                                                                                                                   Springer
408                                                                                                               S. Krings et al.


a version control system (VCS): the VCS would allow us to          the state machine within a reasonable time frame. Thus, any
spot the code written immediately after the test case, i.e., the   real system realized following our approach should be able to
code that made the test case pass for the ﬁrst time. Ideally,      guarantee execution within the smallest time resolution that
the code would be in the same commit as the test case or in        is relevant to the subsystems and their respective require-
the one immediately after.                                         ments.
   However, this link is weak, as both test cases and code            Yet, it is hard to give any real-time guarantees. The only
might be changed later on in subsequent commits. Further-          evidence that can be given is to run the system often enough
more, a subsequent code change might be related to one             and measure whether execution is kept in the speciﬁed tol-
or more already existing code changes. Refactorings add an         erances. However, this is still better than what we expect of
additional layer of complexity that the simple immediate           more formal approaches, which usually do not account for
test-to-source link could not follow.                              wall time at all.

4.4 Variability of requirements
                                                                   5 Model details
The speciﬁcation document gives requirements for cars with
diﬀerent features. Examples include the driver position,           In the following, we will detail implementation idioms we
which can be on the left- or right-hand side of the car; a         employed to simplify handling and veriﬁcation of the in-
market code (USA, Canada, or EU), which inﬂuences how              volved state machine, and explore some snippets of our code
direction blinking works (European cars have a dedicated           to showing these idioms in practice.
tail-lamp which American cars do not); and armored vehi-
cles, which have an additional darkness switch in order to         5.1 Formalization approach
suppress certain light features.
   In our current implementation, we handled the require-          As stated, we postponed veriﬁcation as much as possible.
ments’ variability by introducing artiﬁcial sensors. These         Instead, as our ﬁrst step, we set up the validation sequences
sensors produce a constant value for each of the above fea-        as test cases. Then, following test-driven development, we
ture and are assigned to local variables during the system’s       added to the implementation code by only considering the
initialization. While this approach was easy to implement on       ﬁrst failing assertion in a scenario. Once the test passed,
top of our initial system, it also pollutes both the code and      we moved on to the next. In a second step, we added test
program state to some extent.                                      cases that are directly related to one or sometimes several
   In the automotive industry, a commonly used approach            requirements.
for handling variability is software product line develop-            Finally, we set up CBMC and tried to verify the properties
ment [19, 32]. If the variability had been larger, we could        described by the requirements. As stated, we use the same
have split ELS and ECS into a common base product used             code for testing and formal veriﬁcation, avoiding any trans-
for all market segments and used a software product line ap-       lation between veriﬁcation and testing environments as done
proach to develop individual manifestations, e.g., for Canada      for instance by Chen et al. [16] and others. However, both
vs. USA.                                                           approaches remain distinct rather than being combined into
   Given that the variability in the requirements was not that     a single veriﬁcation procedure [44].
large, we opted for the simpler implementation in order to
concentrate on validation and veriﬁcation.                         5.2 Modeling idioms

4.5 Properties addressed & limitations                             Besides sticking to the MISRA C guidelines and test-driven
                                                                   development we also adopted two further idioms during
Due to time constraints, we opted not to implement every sin-      modeling: only use enumeration types, and do not expose
gle requirement but tried to cover as much as possible. Aside      mutability. We will motivate and elaborate on these in the
from the emergency brake light, all requirements have been         following subsections.
taken into account for the ELS. For the SCS, we implemented
about two-thirds of the requirements, up to (including) SCS-       5.2.1 Use enumeration types
28. While it would be nice to have a more complete imple-
mentation, we do not think that it would impact our gathered       We opted to deﬁne all types as enumeration types. This is
conclusions.                                                       to be expected for some data types, which are true enumera-
   A feature of the requirements that is not addressed satis-      tions, such as:
fyingly are timers. We are convinced that any modern CPU           typedef enum {Ready, Dirty, NotReady}
to be used in cars is fast enough to execute an iteration of                  sensorState;


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                                409


   Yet, we also deﬁned integer types as enumerations:
typedef enum {                                                              Listing 1 Sensor Reads and CBMC Assumptions
      percentage_low = 0,                                                   keyState ks = get_key_status();
      percentage_high = 100                                                 __CPROVER_assume(ks == NoKeyInserted || ks ==
} percentage;                                                                    KeyInserted || ks ==
   The reasons for this are twofold: ﬁrst, we can easily iden-                  KeyInIgnitionOnPosition);
tify thresholds and the value range for each type. While                    bool engine_on = get_engine_status();
percentages are straightforward, other values such as the                   __CPROVER_assume(engine_on == true ||
steering wheel angle are not easily represented in a human-                     engine_on == false);
understandable format. An excerpt of the corresponding type                 voltage voltage_battery = get_voltage_battery
deﬁnition is as follows (analogously for turning the steering                   ();
wheel to the right):                                                        __CPROVER_assume(voltage_battery >=
typedef enum {                                                                  voltage_min && voltage_battery <=
      st_calibrating = 0,                                                       voltage_max);
      st_hard_left_max = 1,           /* 1.0 deg */                         ...
      st_hard_left_min = 410,                                               __CPROVER_assume(implies(ks ==
      st_soft_left_max = 411, /* 0.1 deg */                                     KeyInIgnitionOnPosition, engine_on ==
                                                                                true));
      st_soft_left_min = 510,
                                                                            __CPROVER_assume(implies(engine_on == true,
      st_neutral_maxl = 511, st_neutral = 512,
                                                                                ks == KeyInIgnitionOnPosition));
      ... /* analogous for the right side */
} steeringAngle;
   Such a type deﬁnition renders it easier to identify, e.g., in
what direction the steering wheel is turned and how far. For                5.3 Coding examples
instance,
                                                                            Below, we present some key snippets of our implementation.
st_hard_left_max <= angle &&
                                                                            We focus on the concept of the ELS systems, as the SCS is
angle <= st_hard_left_min
                                                                            structured the same way.
can be used to check if the wheel has been turned far to the
                                                                               The core of our ELS is the light_do_step function,
left.                                                                       spanning over almost 300 lines of C code, that is called in a
   C behavior is undeﬁned if a value that is out of range of                loop. Some auxiliary functions exist to properly set the high
the corresponding enumeration is passed. Thus, our second                   beam light, blinkers, etc., where it was appropriate to heed
intention was that model checking tools could easily deduce                 the DRY principle. The light_do_step function can be
the actual value range rather than having to consider integers              divided in three major parts, described below.
exhaustively. This will be discussed further in Sect. 6.2.
                                                                            Sensor reads and type information for CBMC              First, all
                                                                            relevant sensors are read and stored locally. For veriﬁcation
5.2.2 Do not expose mutability
                                                                            with CMBC (as discussed in Sect. 6.2), it is necessary to
                                                                            provide type information for integer ranges and enums. List-
It is easy to write broken code when using mutable structs,                 ing 1 shows this for three examples: ﬁrst, all possible states
especially if they are used in order to communicate between                 of the key are enumerated. Second, as C represents booleans
threads. Instead, we pass values to and from interface func-                as integers, boolean values must be speciﬁed to be exactly
tions. This means, that values are copies of the data which                 true or false. Third, integer ranges such as the possible val-
are not referenced from anywhere else in the program and the                ues for the battery voltage have to be provided as an axiom.
receiver may do however they please with it. An example is                  Additionally, we add assumptions based on the speciﬁcation,
that the state from the light subsystem can be queried (for test            e.g., that the engine state is linked to the key position.
cases). The returned value will never change unless the test                   As noted, we implemented time as a sensor as well. List-
                                                                            ing 2 shows that we also had to add assumptions that the
case chooses to do so; no action in the ELS inﬂuences it. This
                                                                            timestamp only increases.
also allows reading multiple output variables consistently.
    On the other hand, frequently changing internal variables,              Implementation of requirements          Requirements are en-
are declared as local (using the static keyword). They are                  coded by a collection of if-statements. Interestingly, no else-
always stored in the same “place” and may not be exposed;                   branch exists in the function — most likely because the spec-
in particular, there are no getter functions for these variables.           iﬁcation does not contain the words “else” or “otherwise”.


                                                                                                                                     Springer
410                                                                                                               S. Krings et al.


                                                                5.4 Modeling of time constraints
Listing 2 Time as a Sensor
size_t tt = get_time();                                         When writing code that takes time into account, one is easily
__CPROVER_assume(tt >= when_light_on);                          tempted to access the current time provided by the operating
__CPROVER_assume(tt >= blink_timer);                            system. This is a bad when time-based properties are to
__CPROVER_assume(tt >= ambi_light_timer);                       be tested, as tests would have to be enriched with sleep
__CPROVER_assume(tt >= pitman_arm_move_time);                   statements to achieve proper timing for the situation under
                                                                test.
                                                                   Instead, we introduced an artiﬁcial sensor reporting the
                                                                current time in milliseconds, comparable to a unix times-
                                                                tamp. For testing, this sensor is mocked, and some artiﬁcial
Listing 3 Implementation of two Requirements                    time is provided. The code does not know anything about
// ELS-16 (has priority over ELS-17)                            time, it just reads a sensor returning an integer value.
if(!engine_on && (last_lrs != lrs_auto)                            The only assumption made is that one cannot go back in
    && (get_light_rotary_switch() == lrs_auto                   time. In consequence, the step functions can be called in a
    )) {                                                        continuous loop, independent of the computing speed and
    set_all_lights(0);                                          time needed for a single iteration. On fast hardware, there
}                                                               might even be several executions within the same times-
...                                                             tamp (e.g., if the resolution is milliseconds) or timestamps
// ELS-41: reverse gear                                         might pass without an execution following (e.g., when using
if(reverse_gear) {                                              nanoseconds). Mocking the sensor also has the advantage
    set_reverse_light(100);                                     that test scenarios, which would take several minutes of wall
}                                                               time, can be executed in milliseconds instead.
if(!reverse_gear) {                                                If the entire piece of software was to be shipped, it would
    set_reverse_light(0);                                       be trivial to swap out the sensor: One only has to link an
}                                                               implementation that provides the real time, which may be
                                                                provided by the operating system.

                                                                5.5 Readability and comprehensibility

Listing 4 Veriﬁcation of two Requirements                       MISRA C is already designed to improve readability [5], and
// ELS-22: low beam => tail lights                              given that C is a widely used language we assume our im-
assert(implies(blinking_direction != hazard,                    plementation to still be accessible for nonexpert developers
    implies(get_light_state().lowBeamLeft >                     unfamiliar with formal methods. Of course, the usual coding
    0, get_light_state().tailLampLeft > 0 ||                    guidelines for increasing readability apply to this case study
    get_light_state().tailLampRight > 0)));                     as well, e.g., naming conventions, limits on line length or
...                                                             nesting depths, consistent indentation, and the like.
// ELS-41: reverse gear turns on reverse                           In the following, we will revisit our implementation and
    lights                                                      discuss the readability of the code and hold it against this
assert(implies(reverse_gear, get_light_state                    assumption.
    ().reverseLight > 0));
assert(implies(!reverse_gear, get_light_state                   5.5.1 Readability metrics over ELS and SCS
    ().reverseLight == 0));
                                                                An intuitive metric for readability seems to be the number
                                                                of lines of code (LOC). ELS and SCS include 605 and 642
                                                                LOC, respectively, not counting 328 blank and 200 comment
In the snippet in listing 3, we show how two smaller require-   lines. However, more precise metrics for readability have
ments are realized.                                             been suggested.
                                                                   Buse and Weimer [13] show that the average number of
Assertions     The last part of the light_do_step function      identiﬁers per line, the average line length, or average nesting
contains code for invariant veriﬁcation. Listing 4 contains     depth are negatively correlated with readability. Simultane-
assertions that can be checked using CBMC to verify two         ously, the average number of comment lines, and the average
requirements.                                                   number of semantically breaking blank lines are positively


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                              411


correlated with readability. The negative impact of nesting                 property retains a given value along the way. While incred-
on readability is further pointed out by Johnson et al. [31].               ibly valuable for writing the tests, we acknowledge that the
Taking this into account, our code still seems to be read-                  macro’s name is not descriptive enough as it does not convey
able. We observe a minimum amount of nesting, with only                     its role as an assert statement. Hence, the readability of the
if-constructs introducing mostly only one extra level of in-                test itself decreases.
dentation, nesting for at most two levels. The average line
lengths for the ELS and SCS are 34.37 and 36.27 characters,                 5.5.4 Code pollution due to CMBC annotations
respectively, with maxima of 170 and 125 characters. These
numbers suggest that the majority of lines is short and com-                As C is not designed for formal veriﬁcation, we found that
prehensible, with some outliers rendering individual parts of               some annotations for CMBC started to pollute the code.
the code less readable.                                                     While adding asserts into the code to introduce invariants is
                                                                            straightforward and immerses into the C code quite well, we
5.5.2 Subjective readability of ELS and SCS                                 needed to add further axioms to the code so CMBC was able
                                                                            to properly work with our enum types. This resulted in clut-
Besides readability metrics, a more subjective way of esti-                 tering of the sensor reads as can be seen in listing 1. Here, we
mating the code readability is to simply try reading it again.              ended up with one big block of sensor read and value axiom
The main interest hereby lies within our step functions, which              pairs which impacts readability. However, in most formal
are continuously looped over. For the ELS and SCS modules,                  languages, this would be a nonissue as they were designed
these functions consist of 276 and 127 LOC, respectively.                   with invariants and axioms in mind and include them as ﬁrst
Both start by accessing all the sensors, partly without pro-                class citizens appropriately. Furthermore, we added these
cessing their return values. The rest of the implementation                 axioms at the very end of the development process whereas
follows a clear pattern: if-statements checking for a con-                  they are much more involved in early development stages in
dition to act upon. While the code lacks some comments                      fully formal methods.
which explain why certain things are done, the references
to the respective requirement from the case study accom-
pany the code fragments as annotations. Overall, as the code                6 Validation & veriﬁcation
is not written in a high-level speciﬁcation language which
more closely captures natural language, the overall readabil-               We tried to validate our implementation throughout the
ity seems to be limited by the general readability of (MISRA)               whole development process by using test-driven develop-
C code. While this can be seen as a drawback, one could also                ment, as we will discuss in Sect. 6.1. In addition, we used
argue that no further understanding of higher mathematics or                the CBMC model checker to fully verify diﬀerent proper-
set theory is required as, for instance, in certain formal lan-             ties of our implementation directly on the C code as we will
guages. Thus, we believe the code remains equally readable                  describe in Sect. 6.2.
to experts and nonexperts alike.
                                                                            6.1 Test-driven development using cmockery
5.5.3 Readability of the unit tests
                                                                            We used test-driven development based on the provided sce-
                                                                            narios. For this, we rely on Google’s cmockery library,4
Following, we want to take a closer look at our tests’ read-
                                                                            which provides a unit testing framework and allows mocking
ability. Each unit tests follows a pattern of arrange, act, assert,
                                                                            functions. Since we did not want to execute all tests in real-
as shown in listing 5. As this is a well-known technique, we
                                                                            time, we mocked functions that extract sensor data and the
assume the tests are comprehensible by nonexperts.
                                                                            current time in our test cases. We used two diﬀerent kinds of
   However, we can observe two points negatively impacting
                                                                            test cases for a ﬁrst quick validation:
readability. Firstly, some tests involve multiple assertions.
Especially in terms of time-sensitive behaviors, we observe                 • The provided scenarios were automatized and used as in-
patterns where the test advances the timer, asserts a speciﬁc                 tegration tests.
property (e.g., light on or oﬀ) then repeats the process to                 • In addition, we implemented unit tests for all requirements
assert the property change after a certain time.                              given in the speciﬁcation document. Of course, each unit
   Secondly, as this was such a common pattern speciﬁcally                    test only covers a minimal scenario that shows how the
in the ELS, we introduced macros which reduced boiler-                        requirement is supposed to be understood and automatizes
plate code, but might have reduced readability. The macro                     the veriﬁcation of that single scenario.
progress_time_partial in listing 5, line 31, for instance,
advances time for a given time frame and asserts that a                       4 https://github.com/google/cmockery.


                                                                                                                                    Springer
     412                                                                                                                             S. Krings et al.


                                                                                        As can be seen, we have implemented diﬀerent C macros
     Listing 5 Test of Requirement ELS-3                                             to simplify test case development:
1    void els3_a_left(void **state) {
2      init_system(leftHand, false, EU, false, false);                               • assert(_partial)_state which checks if the internal
3      sensors_and_time sensor_states = {0};
4                                                                                      states of ELS and SCS correspond to given assertions. The
5        assert_light_state(((light_state) {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0}));
                                                                                       assertions can specify the state both partially, as done in
 6
 7       // ignition: key inserted + ignition on
                                                                                       the listing, and fully.
 8       sensor = update_sensors(sensor, sensorTime, 1000);                          • progress_time(_partial) combines assertions on the
 9       sensor = update_sensors(sensor, sensorBrightnessSensor, 500);
10       sensor = update_sensors(sensor, sensorKeyState, KeyInIgnitionOnPosition);     state with a progression of time as reported by the time
11       sensor = update_sensors(sensor, sensorEngineOn, 1);
12                                                                                     sensor.
13       mock_and_execute(sensor_states);
14
15       sensor = update_sensors(sensor, sensorTime, 2000);                          Validation results   As expected, using test-driven devel-
16       pitman_vertical(pa_Downward5);
17       mock_and_execute(sensor_states);                                            opment provided the usual beneﬁts:
18
19
20
         assert_partial_state(blinkLeft, 100, blinkRight, 0);
         pitman_vertical(pa_ud_Neutral);
                                                                                     • having to formulate test cases helped us gain an under-
21       sensor = update_sensors(sensor, sensorTime, 2000);                            standing of the requirements and how they are supposed
22       mock_and_execute(sensor);
23                                                                                     to work,
24       pitman_vertical(pa_Upward7);
25                                                                                   • refactoring was made easier and more secure, and
26       progress_time_partial(2000, 2499, blinkLeft, 100, blinkRight, 0);
27       progress_time_partial(2500, 2999, blinkLeft, 0, blinkRight, 0);
                                                                                     • the implementation was closer to the actual speciﬁcation
28                                                                                     from the start.
29       int i;
30       for (i = 3; i < 6; i++) {
31          progress_time_partial(i*1000,       i*1000 + 499,                           The fact that we are working with an actual implementa-
32                                blinkLeft, 0, blinkRight, 100);
33          progress_time_partial(i*1000 + 500, i*1000 + 999,
                                                                                     tion made test-driven development come naturally. However,
34
35       }
                                  blinkLeft, 0, blinkRight, 0);                      diﬀerent ways of combining formal methods with test-driven
36   }                                                                               development have been discussed [6] as well. In addition,
                                                                                     developing speciﬁcations using continuous testing has been
                                                                                     suggested for former ABZ case studies in the context of the
                                                                                     B method [25, 26].
        A snippet taken from the test case of the requirement ELS-
     3 is shown in listing 5. The system is initialized to belong                    Inﬂuences on code        Using the macros above, our initial
     to an EU-based car with left-hand drive and without any                         design of splitting sensors, user input, and actuators did not
     extras such as ambient light, followed by the initialization                    have to be adapted further to be testable. Yet, it created a
     and assertions regarding the correctness of the initial state.                  vast amount of code entirely dedicated to testing. Of 5223
     Afterwards, in lines 8 to 15, we update the sensors to the                      source code lines (including a Makeﬁle and code used for
     values they should hold at the start of the test scenario and the               visualization but not counting comments and blank lines),
     code setting up the mocked functions is called. In particular,                  3786 lines are test code. In general, we needed quite a lot
     we set the time sensor used to simulate the actual clock as                     of code for the tests as we had to create the appropriate
     described in Sect. 5.4. Overall, the test setup phase ensures                   infrastructure to be able to handle the progression of time in
     that our artiﬁcial sensors report the required values.                          the test cases. Thus, future additional test will probably not
        Line 16 shows the diﬀerence between sensors and driver                       increase the number of lines of code needed for testing as
     interaction: While sensors have to be mocked in order to                        much.
     simulate an actual system, user input is given directly. This
     corresponds to what will happen in an actual car: the system                    6.2 Model checking using CBMC
     has to react to user input immediately, while it can read sensor
     data arbitrarily.                                                               As stated above, we used CBMC to verify properties of
        Line 19 asserts that the left blinker is on 100% and                         our implementation directly on the C code. Depending on
     the right one is on 0% once the step function was exe-                          where we place C-style assertions, they correspond to diﬀer-
     cuted after the user input was given. We use the function                       ent kinds of properties commonly used in state-based formal
     assert_partial_state, since we only make an assertion                           methods:
     regarding the two variables blinkLeft and blinkRight,                           • If placed at the end of the loop implemented by the ELS
     rather than making an assertion over all state variables.                         and the SCS state machines depicted in Fig. 2, assertions
        Finally, Lines 26–27, as well as 31–34, assert that for each                   correspond to safety invariants that have to hold in every
     millisecond in the time interval, the provided values remain                      state reachable by one of the subsystems.
     the same, i.e., that the step function does not change output                   • If placed anywhere inside the loop, assertions can be used
     values during that time frame.                                                    as invariants on intermediate states.


     Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                                413


• If placed outside the loop, we can check if properties hold
  after a certain number of iterations (controlled by CBMC’s                Listing 6 Partial CBMC Output
  unrolling preferences).                                                   State 59 file light/light-impl.c line 242
• By using additional variables for unrolling state traces,                     function light_do_step thread 0
  we can implement a lightweight veriﬁcation of temporal                    ---------------------------------------------
  properties. Of course, this is not as powerful as LTL or                   ks=/*enum*/NoKeyInserted
  CTL.                                                                          (00000000000000000000000000000000)

Examplary veriﬁcation of ELS-22           Requirement ELS-22                State 63 file light/light-impl.c line 242
is a great example for an invariant. It states “Whenever the                    function light_do_step thread 0
low or high beam headlights are activated, the tail lights are              ---------------------------------------------
activated, too”. For this, we can add an assertion such as:                  ks=/*enum*/KeyInIgnitionOnPosition
implies(get_light_state().lowBeamLeft > 0,                                      (00000000000000000000000000000010)
             get_light_state().tailLampLeft > 0 ||
             get_light_state().tailLampRight > 0)                           State 65 file light/light-impl.c line 244
    The disjunction in the second part of the implication is                    function light_do_step thread 0
important for American cars: as tail lamps are used for indi-               ---------------------------------------------
cators, it is accepted behavior if one tail lamp is temporarily              engine_on=FALSE (00000000)
deactivated during a ﬂashing cycle. When running CBMC,
it immediately came up with a counterexample. A part of the                 State 69 file light/light-impl.c line 244
output trace can be found in listing 6.                                         function light_do_step thread 0
    The counterexample shows how the two system variables                   ---------------------------------------------
ks, i.e., the key state, and engine_on, i.e., the engine’s                   engine_on=TRUE (00000001)
ignition state, change while light_do_step is executed.
    The main issue with such a counterexample is that each
variable assignment, function call, and return from a function              Table 2 Example Trace Violating ELS-22
introduces a new state. While this representation mimics the
                                                                            State Variable                   Iteration 1          Iteration 2
internal workings of the C code, it does not correspond to the
mental model: comparable to common state-based formal                       key_state                        NoKey                KeyIn
methods, we regarded a state change to include multiple
                                                                            engine_on                        FALSE                TRUE
variables at once.
                                                                            all_doors_closed                 FALSE                TRUE
    Hence, as we were only interested in comparing state
                                                                            brightness                       0                    37539
variables per full iteration of light_do_step, the output
                                                                            speed                            0                    936
was barely readable to us (the counterexample consists of
more than 200 lines and 50 low-level states).                               daytime_light_was_on             FALSE                TRUE
    CBMC can optionally reduce the output by removing as-                   low_beam_left                    0                    100
signments unrelated to the property. This did not work well                 low_beam_right                   0                    100
for us, as the assignment of signals for the low beam head-                 last_engine                      FALSE                TRUE
lights was removed as well. We ended up manually writing                    last_key_state                   NoKey                KeyIn
state variables in a spreadsheet to comprehend the scenario                 last_all_door_closed             FALSE                TRUE
and ultimately created our own visualization which we will                  tail_lamp_left                   0                    0
present in Sect. 7.2. A (condensed) version of the trace be                 tail_lamp_right                  0                    0
found in Table 2 (using “NoKey” for “NoKeyInserted” and
“KeyIn” for “KeyInIgnitionOnPosition”). Here, the (high-
level) state changes between two full iterations of our step                since daytime light was only tested by night, where, coinci-
function are shown, rather than changes of individual vari-                 dentally, other triggers activated the tail lamps. As this trace
ables during the execution. This representation aligned better              did not contain assignments of the tail lamp variables, we
to our mental model of the implementation and was thus more                 had to look up their initial (unchanged) values and add them
helpful for debugging.                                                      to the table manually.
    The error in our code was that, based on ELS-17, only the
low beam headlights were activated due to activated daytime                 Veriﬁcation results    However, the assertion still failed to
running light. This was not uncovered by the test scenarios,                verify. Upon further analysis of the property, we discovered


                                                                                                                                      Springer
414                                                                                                                 S. Krings et al.


a conﬂict between ELS-22 and hazard blinking in Canadian           during analysis of the requirements and during implement-
and US cars. In those cases, hazard blinking deactivates both      ing test cases. As we only performed validation steps after
tails lights for the dark cycle, thus violating the property. We   implementation, the validation steps just uncovered short-
extended our assertion by checking our variable for blinking       comings of our own implementation and noncompliances
direction beforehand:                                              with respect to the speciﬁcation. Due to page limitations, we
assert(implies(blinking_direction != hazard,                       will only present some of them:
                       /* old assertion */));                          ELS-37 is somewhat broken or at least highlights an in-
Afterwards, we were able to successfully verify the property       completeness in the speciﬁcation. For now, there is no way
using CBMC.                                                        to discern whether an adaptive cruise control is part of the
                                                                   vehicle; from the speciﬁcation, we had to assume that it is
Inﬂuences on code         At ﬁrst glance, using CBMC only re-      installed in every system. Then, according to SCS-1, there
quired to add assertions to the code. As assertions are often      does not even have to be a desired speed at all times: right
introduced as part of understanding certain scenarios, this        after engine startup no previous desired speed is available.
does not change the modeling strategy itself. Some addi-           We think that, in order to make sense at all, it rather should
tional assertions were required to let CBMC detect integer         be “is active” than “is part of the vehicle”. Also, this is the
ranges that are deﬁned by an enum (as otherwise, counterex-        only part of the speciﬁcation that refers to an advanced cruise
amples would ﬁnd, e.g., percentage values larger than 100,         control.
cf. Sect. 5.2), and that consecutive timestamps cannot get             ELS-42 to ELS-46 only partially specify what should
smaller.                                                           happen in case of subvoltage. Instead, information should
    A huge issue we encountered very late is that, by default,     be given for all light components how the software should
the tool only is able to work with internal state changes, i.e.,   react or whether they remain unaﬀected. Only the require-
state that the implementation adds. External state changes,        ment ELS-43 mentions a single unaﬀected component. In
i.e., state that is modiﬁed by user interaction or the environ-    particular, turn signals, the regular low beam headlights and
ment, were not part of our ﬁrst veriﬁcation attempts. This         the emergency break light remain unspeciﬁed. Additionally,
can be imagined as veriﬁcation of a car whose engine cannot        ELS-43 references ELS-31 for a situation where the light ro-
be started.                                                        tary switch is in position Auto and the pitman arm is pushed;
    CBMC can incorporate such external state changes if the        ELS-31, however, describes behavior if that switch is in the
corresponding function has nondet_ as a preﬁx of its name          On position and the pitman arm is pulled.
(which, naturally, collided with our naming conventions).              ELS-19 contains a contradiction: ﬁrst, it states that am-
Two modeling issues come with that: ﬁrst, constant values          bient lighting prolongs already active low beam headlights.
(such as the market code or installed features) might change       Later, it says that the headlamps “remain active or are acti-
on every call now. Thus, we had to refactor so that the values     vated”. We think that some actions are reasonable to activate
are retrieved once and the getter functions were replaced by       the headlight even if it was not on before (e.g., opening the
using these local variables. Second, we now cannot express         doors). Others deﬁnitely should not activate the headlight
certain orderings of external states: an example is the light      (e.g., if the brightness falls below the speciﬁed threshold, as
rotary switch that has to move from the oﬀ position via the        passing cars and the setting sun might trigger the brightness
auto position before it can be set to on. We found no way to       sensor). Also, it does not have any constraints regarding the
encode this behavior.                                              light rotary switch: if the switch is in the “oﬀ” position, we
                                                                   think the ambient light should not activate at all.
                                                                       While currentSpeed is speciﬁed as a sensor in the ELS,
7 Other observations                                               it is not clear how the SCS accesses this value. No sensor is
                                                                   provided according to the speciﬁcation, and only the brake
Our implementation work allowed us to identify several ﬂaws        pressure is mentioned as actuator but not the gas pedal. Thus,
in the speciﬁcation, as well as shortcomings of our imple-         the SCS as speciﬁed appears to only be responsible for de-
mentation strategy. In the following, we document such is-         termining the desired speed but not for actually deploying
sues and give suggestions and solutions.                           it to the current speed? To our understanding, the measured
                                                                   current speed should be a sensor to the SCS to allow it to
7.1 Speciﬁcation ambiguities, ﬂaws, and                            work properly.
    suggested improvements                                             SCS-23 speciﬁes a safety distance for the adaptive cruise
                                                                   control of 2.5 s · currentSpeed when the current speed is
During development, we identiﬁed several shortcomings or           below 20 km/h, and a safety distance of 2 m if both vehicles
ambiguities within the speciﬁcation. These issues were found       are standing. Assuming currentSpeed < 2.88, however, the


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                               415


safety distance according to SCS-23 is below 2 m and eﬀec-
tively approaches 0 the closer the vehicle gets to a standstill,
e.g., 2.5 s · 2.8 km/h = 2.5 s · 0.77 m/s = 1.925 m < 2 m . But
once a standstill is reached, the safety distance is reset to 2 m
and thus violated instantly. It remains unclear whether this
2 m distance is meant as minimum or intended to delay the
reaction to eventual acceleration of the vehicle in front.
    SCS-28 speciﬁes an acoustic signal which is to be played
if the time to reach a standstill with maximum deceleration
is greater than the time until impact. SCS-21, however, al-
ready speciﬁed another acoustic signal to be played when
maximum deceleration of 3 m/s2 is insuﬃcient to prevent
impact. As it is not speciﬁed what SCS-28 considers as max-
imum deceleration value these signals might overlap if 3 m/s2
can be assumed again. While the speciﬁcation does state the
maximum brake-implied deceleration to be 6 m/s2 , it is un-
clear whether this is the deceleration to be considered for
SCS-28.
                                                                            Fig. 3 OpenGL based domain-speciﬁc visualization, showing the car
7.2 Improvements to our employed                                            and its current speed
    methodology
                                                                            a mere demonstration tool, its value for development was
We are surprised how easy it was to implement the case                      diminished.
study in C, given that none of the authors is a professional                   To improve, we decided to further separate implementa-
C developer. While we were unsure during implementation,                    tion and visualization. Our goal was to keep interacting with
given our test harness and the results of CBMC, we now                      the implementation simple, but also allow replacing it with
have more conﬁdence in the correctness of our implementa-                   a new version straightforwardly.
tion. However, CBMC’s output was hard to interpret as we                       To achieve this, we added a small sensor implementation,
discussed above. Performance not being a primary concern,                   to be controlled from the outside and linked as a shared
our result turned out simple enough to not warrant further                  library. On top, we used F# to develop a visualization using
optimization.                                                               the RayLib library. This approach worked well, reducing
    To improve, we created diﬀerent visualizations. One such                the communication of the two components to a simple and
visualization is a state visualization based on PlantUML5                   somewhat stable C interface.
(cf. Fig. 5). A second visualization was a domain-speciﬁc vi-                  While the older OpenGL-based Visualization looked
sualization in C++ with OpenGL, using the existing sources                  pleasing, it almost completely omitted numerical feedback.
directly as part of the compilation.                                        This decision struck us as too extreme in retrospect, so we
    However, development was incomplete and thus omitted                    opted for a more minimal look, but including both a domain-
for the initial article. Revisiting the visualizations for this             speciﬁc visualization and values of state variables. For exam-
extended article, we found that both are not fully satisfactory:            ple, the steering angle directly corresponds to the displayed
The PlantUML-based visualization is very technical, directly                image of a steering wheel, as well as to the traced out path the
referring to implementation details. While it is still beneﬁcial            vehicle is currently headed (cf. Fig. 4). We found the visuals
for understanding test failures, it relies on knowledge about               very helpful in gaining a quick understanding of the imple-
the internal workings of the implementation and is thus not                 mentation’s behavior. The geometric intuition provided by
presentable to external stakeholders.                                       the 3D view was a welcome addition.
    In contrast, the C++ visualization is domain-speciﬁc, i.e.,                In contrast to the old visualization, we included an in-
it shows a car and its actuators, and is thus understandable                teractive component, enabling the user to experiment and
without knowing implementation details (cf. Fig. 3). How-                   explore the behavior. By default, an automatically animated
ever, as the visualization was directly linked to the C sources,            car will perform a lemniscate around an attractor point. This
it proved rather inﬂexible and prone to breakage when im-                   was surprisingly eﬀective in ﬁnding behavior that does not
plementation details changed. While it was still useful as                  conform with expectations: For instance, when using the
                                                                            pedals some reaction is to be expected. Yet, even though the
 5 https://plantuml.com/.                                                   pedal position indeed changed as seen in the visualization,


                                                                                                                                     Springer
416                                                                                                            S. Krings et al.


Fig. 4 Newly Developed
RayLib Visualization, showing
the car and visually representing
the status of its actuators




nothing happened with respect to the car’s movement. In con-
sequence, we noticed that neither does the gas pedal cause
acceleration, nor does the brake pedal decelerate the vehi-
cle. As far as the SCS is concerned, the brake pedal merely
disables cruise control as mandated by SCS-16.
   Using C for implementation proved very ﬂexible, as there
exists a plethora of ways to interact with other languages.
Thus, it would have been easy to use other ways of animation.
For instance, we were able to execute our implementation
in a browser by compiling it to wasm via the Emscripten
Compiler Frontend (emcc) and then interact with it using
JavaScript.

7.3 Note about deriving a software
    implementation

As we have started from a low-level implementation in C,
the software implementation was always readily available.
Hence, in our case, the “model” can be directly compiled
and executed. However, testing the executable would still be
interesting if we look beyond our simple tests, i.e., with an
actual implementation at hand, hardware-in-the-loop tests
would be desirable.


8 Comparison
                                                                Fig. 5 Visualization using PlantUML
In the 2020 ABZ Proceedings, ﬁve other contributions were
published, all of them providing veriﬁed formal models
rather than implementations:
• Arcaini et al. [4], who utilized abstract state machines      • Leuschel et al. [36], who developed their solution in clas-
  (ASMs) [10] and the ASMETA framework [3],                       sical B [1] and later translated to Event-B for proof [2],
• Cunha et al. [20], who modeled their solution in Elec-        • Mammar et al. [38, 39], used Event-B for two distinct
  trum [37], an extension to Alloy [30],                          models of the ELS [39] and the SCS [38].


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                             417


    The main diﬀerence between our approach and the other                   allows modifying SVG graphics based on state variables.
case studies is that we tried to verify an existing low-level               While this approach is comparable to our visualization, no
implementation after it has been developed. In comparison,                  custom implementation aside from some glue code connect-
the formal approaches undertaken by the other case studies                  ing the image to the state values was needed.
tend towards following a correct-by-construction approach.                     Visualization and timers aside, the B and Event-B models
That is, they later derive an implementation from the formal                are much more formal than our implementation and rely
model by code generation, e.g., as possible for B [42].                     heavily on proof (by Rodin) and model checking (by ProB)
    The case study implemented using ASMs by Arcaini et                     rather than testing.
al. [4] uses a formalism of a much higher abstraction level                    The two articles by Mamar et al. concentrate on the
than our concrete implementation. However, code generation                  ELS [39] and the SCS [38] individually. A particular focus
is available for ASMs as outlined by the authors. As a result,              is on the model’s diﬀerentiation between the two systems
a C++ (rather than plain C) implementation could be derived                 and the environment. The model for the environment closely
from the formal models and might look somewhat like our                     resembles the sensors and inputs modules shown in Fig. 2.
direct implementation.                                                         Again, the case study uses ProB for model checking.
    Furthermore, ASMETA allows doing conformance test-                      Given that the authors intentionally tried to avoid rather
ing, i.e., deriving unit tests from the formal model rather than            costly LTL model checking and proof, their properties re-
writing them by hand as we did.                                             semble what we check using CBMC. In particular, simple
    The actual implementation aside, Arcaini et al. designed                properties on states sequences are rendered model checkable
their models in roughly the same fashion as we designed                     by storing the prestate in individual variables available for
our implementation. ELS and SCS are coupled very loosely                    comparison with the current state.
and developed as independently as possible. At the same
time, they share some signals, comparable to the actuators                  Further related work       An alternative to both our imme-
we deﬁned above. During development, features were added                    diate low-level implementation and to the code generation
gradually while keeping a (proven) reﬁnement chain intact.                  approaches that would usually follow with the other case
While we added features in roughly the same fashion and                     studies is to embed the formal models in runtime code di-
order, we had no access to a formal proof of reﬁnement.
                                                                            rectly, i.e., without compiling them to some other language.
Thus, we had to rely on our test cases entirely.
                                                                               For B, this has been outlined in a demonstration of the
    The approach followed by Arcaini et al. does not verify
                                                                            ETCS hybrid level 3, where a classical B model is able to
timing issues, as there is no continuous time in ASM. This is
                                                                            control real trains [26]. The approach uses the ProB Java
a weakness when compared to our low-level implementation
                                                                            API [33] to connect the formal model to the outside world
which could be executed in realtime.
                                                                            and allows interacting with it.
    The case study performed by Cunha et al. [20] follows
an approach to veriﬁcation and validation that is similar to
ours. Initially, the authors use test case given as animation
scenarios (i.e., small test cases) and reference scenarios (i.e.,           9 Conclusions
the execution sequences given in the speciﬁcation). This is
comparable to the test-driven development we employed as                    To summarize, we have implemented a low-level version of
discussed in Sect. 6.1.                                                     the ABZ 2020 case study in MISRA C, a language commonly
    Formal veriﬁcation of the requirements is performed after               used in the automotive industry. We relied on test-driven
(some of) the development steps. This is again is compara-                  development for validation as well as on formal veriﬁcation
ble to our approach of using CBMC on an already existing                    using model checking.
implementation (cf. Sect. 6.2).                                                Compared to case studies using more rigorous ap-
    The case study by Leuschel et al. [36] models time in the               proaches, our approach shows both advantages and disad-
same way we did. There is a dedicated model implementing                    vantages. In particular, our implementation stays close to the
timers based on elapsed milliseconds. In contrast to our sim-               actual system, can easily be deployed to an actual car, and
ple clock module shown in Fig. 2, Leuschel et al. use a more                could be used for simulation and hardware-in-the-loop tests.
involved timer, supporting deadlines and even triggers.                     Furthermore, due to the popularity of C in the automotive
    The case study also uses a domain speciﬁc visualiza-                    industry, it is more approachable by developer untrained in
tion tailored speciﬁcally for the case study. Here, using a                 formal methods. However, while CBMC is an excellent tool,
well-established formal method shows its merits. For B and                  we seemed to have hit every pitfall and in many instances
Event-B, a multitude of animation frameworks and tools is                   actually did not verify anything. Overall, for an untrained de-
available and can be used without much overhead. In the                     veloper, it is very easy to show “the wrong thing” and obtain
case study, a visualization tool called “VisB” is used, which               a “proven correct” signal while the code may still be faulty.


                                                                                                                                   Springer
418                                                                                                                                    S. Krings et al.


   In our attempts to address the (eventually) uncovered is-                  2. Abrial, J.R.: Modeling in Event-B: System and Software Engineer-
sues, we certainly missed the expressiveness and mathemat-                       ing. Cambridge University Press, New York (2010)
                                                                              3. Arcaini, P., Gargantini, A., Riccobene, E., Scandurra, P.: A model-
ical clarity of more rigorous approaches. In particular, the                     driven process for engineering a toolset for a formal method. Softw.
semantics of a guard substitutions would have been very                          Pract. Exp. 41(2), 155–166 (2011)
useful, as diﬀerent actions (e.g., controlling the low beam                   4. Arcaini, P., Bonfanti, S., Gargantini, A., Riccobene, E., Scandurra,
headlights and the cornering light) can be regarded in isola-                    P.: Modelling an automotive software-intensive system with adap-
                                                                                 tive features using ASMETA. In: Raschke, A., Méry, D., Houdek,
tion instead of considering 300 lines of a single step function.                 F. (eds.) Proceedings ABZ, pp. 302–317. Springer, Cham (2020)
Further, having invariants and other properties as ﬁrst class                 5. Bagnara, R., Bagnara, A., Hill, P.M.: The MISRA C coding stan-
citizens rather than inserting them artiﬁcially via macros and                   dard and its role in the development and analysis of safety- and
                                                                                 security-critical embedded software. In: Podelski, A. (ed.) Pro-
external functions is clearer and more convenient. Compared
                                                                                 ceedings Static Analysis, pp. 5–23. Springer, Cham (2018)
to a formal method, we were only able to do very lightweight                  6. Baumeister, H.: Combining Formal Speciﬁcations with Test Driven
veriﬁcation of temporal properties and would certainly have                      Development. Proceedings XP/Agile Universe, LNCS, vol. 3134.
favored to be able to model check LTL or CTL properties.                         Springer, Berlin (2004)
                                                                              7. Beck, K.: Test-Driven Development: By Example. Kent Beck Sig-
Thus, while we were able to verify our implementation to                         nature Book, Addison-Wesley (2003)
a certain degree, we suspect that a more thorough approach                    8. Biere, A., Cimatti, A., Clarke, E., Zhu, Y.: Symbolic model check-
would be able to provide stronger guarantees.                                    ing without BDDs. In: Proceedings TACAS, LNCS, vol. 1579,
   Furthermore, we currently do not validate any properties                      pp. 193–207. Springer, Berlin (1999)
                                                                              9. Boogerd, C., Moonen, L.: Assessing the value of coding standards:
on time constraints aside from simulating an external clock                      an empirical study. In: Proceedings ICSM, pp. 277–286. IEEE,
in the test cases. As part of possible future work, we intend                    New York (2008)
to use CBMC to try to provide real-time guarantees and to                    10. Börger, E., Gargantini, A., et al.: Proceedings ASM, vol. 2589.
                                                                                 Springer, Berlin (2003)
verify the correct behavior in presence of scheduling and                    11. Bowen, J.P., Hinchey, M.G.: Seven more myths of formal methods.
limited by the actual speciﬁcations of an embedded device.                       IEEE Softw. 12(4), 34–41 (1995)
   Both could be veriﬁed by providing a Verilog model                        12. Brookes, T.M., Fitzgerald, J.S., Larsen, P.G.: Formal and infor-
of the hardware, sensors and connections. Afterwards, co-                        mal speciﬁcations of a secure system component: ﬁnal results in a
                                                                                 comparative study. In: Gaudel, M., Woodcock, J. (eds.) FME ’96:
veriﬁcation of the implementation with the Verilog circuit                       Industrial Beneﬁt and Advances in Formal Methods, Third Inter-
model can be performed by CBMC [17]. Additionally, we                            national Symposium of Formal Methods Europe, Co-Sponsored
would like to consider other tools that work directly on the                     by IFIP WG 14.3, Oxford, UK, March 18–22, 1996, Proceedings,
C code, e.g., Symbiotic [15] or Klee [14].                                       vol. 1051, pp. 214–227. Springer, Berlin (1996)
                                                                             13. Buse, R.P., Weimer, W.R.: Learning a metric for code readability.
   Further future research could be done in the combination                      IEEE Trans. Softw. Eng. 36(4), 546–558 (2010)
of formal and informal approaches, e.g., when thinking about                 14. Cadar, C., Dunbar, D., Engler, D.R., et al.: KLEE: unassisted and
code generators: proven invariants on a high-level model                         automatic generation of high-coverage tests for complex systems
                                                                                 programs. In: Proceedings OSDI, vol. 8, pp. 209–224. USENIX
could be compiled to C assertions. Then, they could be veri-
                                                                                 Association (2008)
ﬁed on the low-level code as well, eﬀectively demonstrating                  15. Chalupa, M., Vitovská, M., Strejček, J.: Symbiotic 5: boosted
the correctness of the code generators.                                          instrumentation. In: Proceedings TACAS, LNCS, vol. 10806,
                                                                                 pp. 442–446. Springer, Berlin (2018)
Funding Open Access funding enabled and organized by Projekt                 16. Chen, M., Ravn, A.P., Wang, S., Yang, M., Zhan, N.: A two-way
DEAL.                                                                            path between formal and informal design of embedded systems. In:
                                                                                 Proceedings UTP, LNCS, vol. 10134, pp. 65–92. Springer, Berlin
                                                                                 (2017)
Open Access This article is licensed under a Creative Commons At-            17. Clarke, E., Kroening, D., Yorav, K.: Behavioral consistency of C
tribution 4.0 International License, which permits use, sharing, adap-           and verilog programs using bounded model checking. In: Proceed-
tation, distribution and reproduction in any medium or format, as long           ings DAC, pp. 368–371. IEEE, New York (2003)
as you give appropriate credit to the original author(s) and the source,     18. Clarke, E., Kroening, D., Lerda, F.: A tool for checking ANSI-C
provide a link to the Creative Commons licence, and indicate if changes          programs. In: Proceedings TACAS, LNCS, vol. 2988, pp. 168–176.
were made. The images or other third party material in this article are          Springer, Berlin (2004)
included in the article’s Creative Commons licence, unless indicated         19. Clements, P., Northrop, L.: Software Product Lines. Addison-
otherwise in a credit line to the material. If material is not included in       Wesley, Boston (2002)
the article’s Creative Commons licence and your intended use is not          20. Cunha, A., Macedo, N., Liu, C.: Validating multiple variants of an
permitted by statutory regulation or exceeds the permitted use, you will         automotive light system with electrum. In: Raschke, A., Méry, D.,
need to obtain permission directly from the copyright holder. To view a          Houdek, F. (eds.) Proceedings ABZ, pp. 318–334. Springer, Cham
copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.         (2020)
                                                                             21. Fathy, H.K., Filipi, Z.S., Hagena, J., Stein, J.L.: Review of
                                                                                 hardware-in-the-loop simulation and its prospects in the automo-
                                                                                 tive area. In: Modeling and Simulation for Military Applications,
References                                                                       vol. 6228. SPIE, Bellingham (2006)
                                                                             22. Fitzgerald, J.S., Brookes, T.M., Green, M.A., Larsen, P.G.: Formal
 1. Abrial, J.R.: The B-Book: Assigning Programs to Meanings. Cam-               and informal speciﬁcations of a secure system component: ﬁrst re-
    bridge University Press, New York (1996)                                     sults in a comparative study. In: Naftalin, M., Denvir, B.T., Bertran,


Springer
A veriﬁed low-level implementation and visualization of the adaptive exterior light and speed control. . .                                        419


    M. (eds.) FME ’94: Industrial Beneﬁt of Formal Methods, Second          35. Larsen, P.G., Fitzgerald, J.S., Brookes, T.M.: Applying formal
    International Symposium of Formal Methods Europe, Barcelona,                speciﬁcation in industry. IEEE Softw. 13(3), 48–56 (1996)
    Spain, October 24–18, 1994. Proceedings, Lecture Notes in Com-          36. Leuschel, M., Mutz, M., Werth, M.: Modelling and validating
    puter Science, vol. 873, pp. 35–44. Springer, Berlin (1994)                 an automotive system in classical B and event-B. In: Raschke,
23. General Speciﬁcation of Basic Software Modules. AUTOSAR,                    A., Méry, D., Houdek, F. (eds.) Proceedings ABZ, pp. 335–350.
    Munich (2019)                                                               Springer, Cham (2020)
24. Hall, A.: Seven myths of formal methods. IEEE Softw. 7(5), 11–19        37. Macedo, N., Brunel, J., Chemouil, D., Cunha, A., Kuperberg, D.:
    (1990)                                                                      Lightweight speciﬁcation and analysis of dynamic systems with
25. Hansen, D., Ladenberger, L., Wiegard, H., Bendisposto, J.,                  rich conﬁgurations. In: Proceedings ACM SIGSOFT, FSE 2016,
    Leuschel, M.: Validation of the ABZ landing gear system us-                 pp. 373–383. Association for Computing Machinery, New York
    ing ProB. In: ABZ 2014: The Landing Gear Case Study, CCIS,                  (2016)
    vol. 433, pp. 1–17. Springer, Berlin (2015)                             38. Mammar, A., Frappier, M.: Modeling of a speed control system
26. Hansen, D., Leuschel, M., Schneider, D., Krings, S., Körner, P.,            using event-B. In: Raschke, A., Méry, D., Houdek, F. (eds.) Pro-
    Naulin, T., Nayeri, N., Skowron, F.: Using a formal B model at              ceedings ABZ, pp. 367–381. Springer, Cham (2020)
    runtime in a demonstration of the ETCS hybrid level 3 concept with      39. Mammar, A., Frappier, M., Laleau, R.: An event-B model of an
    real trains. In: Proceedings ABZ, LNCS, vol. 10817, pp. 292–306.            automotive adaptive exterior light system. In: Raschke, A., Méry,
    Springer, Berlin (2018)                                                     D., Houdek, F. (eds.) Proceedings ABZ, pp. 351–366. Springer,
27. Hatton, L.: Language subsetting in an industrial context: a compar-         Cham (2020)
    ison of MISRA C 1998 and MISRA C 2004. Inf. Softw. Technol.             40. MISRA C:2012 – Guidelines for the use of the C language in
    49(5), 475–482 (1998)                                                       critical systems. MISRA (2013)
28. Houdek, F., Raschke, A.: Adaptive Exterior Light and Speed Con-         41. Short, M., Pont, M.J.: Assessment of high-integrity embedded
    trol System                                                                 automotive control systems using hardware in the loop simulation.
29. ISO: Road Vehicles – Functional Safety (2011)                               J. Syst. Softw. 81(7), 1163–1183 (2008)
30. Jackson, D.: Software Abstractions: Logic, Language, and Analy-         42. Vu, F., Hansen, D., Körner, P., Leuschel, M.: A multi-target code
    sis. MIT Press, Cambridge (2012)                                            generator for high-level B. In: Proceedings IFM, pp. 456–473.
31. Johnson, J., Lubo, S., Yedla, N., Aponte, J., Sharif, B.: An empir-         Springer, Berlin (2019)
    ical study assessing source code readability in comprehension. In:      43. Yang, M., Zhan, N.: Combining Formal and Informal Methods
    Proceedings IEEE ICSME, pp. 513–523 (2019)                                  in the Design of Spacecrafts. LNCS, vol. 9506, pp. 290–323.
32. Käköla, T., Duenas, J.C.: Software Product Lines. Springer, Berlin          Springer, Berlin (2016)
    (2006)                                                                  44. Yuan, J., Shen, J., Abraham, J., Aziz, A.: On combining formal
33. Körner, P., Bendisposto, J., Dunkelau, J., Krings, S., Leuschel, M.:        and informal veriﬁcation. In: Proceedings CAV, LNCS, vol. 1254,
    Integrating formal speciﬁcations into applications: the ProB Java           pp. 376–387. Springer, Berlin (1997)
    API. Form. Methods Syst. Des., 1–28 (2020)
34. Krings, S., Körner, P., Dunkelau, J., Rutenkolk, C.: A veriﬁed          Publisher’s Note Springer Nature remains neutral with regard to ju-
    low-level implementation of the adaptive exterior light and speed       risdictional claims in published maps and institutional aﬃliations.
    control system. In: Raschke, A., Méry, D., Houdek, F. (eds.) Pro-
    ceedings ABZ, pp. 382–397. Springer, Cham (2020)




                                                                                                                                          Springer
