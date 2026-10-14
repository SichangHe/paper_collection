Software and Systems Modeling (2023) 22:1737–1749
https://doi.org/10.1007/s10270-023-01124-2

    EXPERT VOICE



A manifesto for applicable formal methods
Mario Gleirscher1,2         · Jaco van de Pol3,4          · Jim Woodcock3,5

Received: 9 June 2023 / Revised: 19 July 2023 / Accepted: 28 July 2023 / Published online: 18 August 2023
© The Author(s) 2023


Abstract
Recently, formal methods have been used in large industrial organisations (including AWS, Facebook/Meta, and Microsoft)
and have proved to be an effective part of a software engineering process finding important bugs. Perhaps because of that,
practitioners are interested in using them more often. Nevertheless, formal methods are far less applied than expected,
particularly for safety-critical systems where they are strongly recommended and have the most significant potential. We
hypothesise that formal methods still seem not applicable enough or ready for their intended use in such areas. In critical
software engineering, what do we mean when we speak of a formal method? And what does it mean for such a method to be
applicable both from a scientific and practical viewpoint? Based on what the literature tells about the first question, with this
manifesto, we identify key challenges and lay out a set of guiding principles that, when followed by a formal method, give
rise to its mature applicability in a given scope. Rather than exercising criticism of past developments, this manifesto strives
to foster increased use of formal methods in any appropriate context to the maximum benefit.

Keywords Formal methods · Formal verification · Software engineering · Tools · Research evaluation · Research transfer


1 Introduction                                                                recent course materials,1 tutorial papers (e.g. [10]), tool
                                                                              manuals (e.g. [11]) text books (e.g. [12, 13]), and a commu-
Formal methods have been an active research area for                          nity wiki.2 Evidence on successful formal method teaching,
decades. Theoretical foundations [1], method applications [2–                 training, and teaching-based transfer is steadily collected.
4], as well as effective ways to transfer [5, 6] them to                      However, the extent of these measures does not yet warrant
the practising engineer, have been thoroughly discussed                       a stable knowledge and skill base among graduated software
and empirically evidenced [7, 8]. The resources to learn                      engineering researchers and practitioners [14, 15].
about these methods range from early syllabuses [9] to                            Driven by the inspiration and critique of expert voices
                                                                              from academia [16–21] and industry [22, 23], formal meth-
                                                                              ods are considered to be one of the most promising tools to
Communicated by Bernhard Rumpe.                                               develop highly dependable software for applications with
B Mario Gleirscher                                                            critical requirements [14]. Developers of formal methods
     gleirscher@uni-bremen.de                                                 have always aimed at applicability in practical contexts,
     Jaco van de Pol                                                          notably with different degrees of success. Indeed, many prac-
     jaco@cs.au.dk                                                            titioners believe in the high potential of such methods and
     Jim Woodcock                                                             would use them to their maximum benefit, whether directly or
     jim.woodcock@york.ac.uk                                                  through powerful software tools [15]. Although there is broad
                                                                              interest in applying these methods in the engineering practice
1    University of Bremen, Bibliothekstrasse 5, 28359 Bremen,                 of dependable systems and software, this domain has not yet
     Germany
                                                                              successfully adopted formal methods. It is observed (e.g. [14,
2    Assuring Autonomy International Programme (AAIP),                        15]) that their use is still significantly weaker than expected,
     University of York, Deramore Lane, York YO10 5GH, UK
3    Aarhus University, Åbogade 34, 8200 Aarhus, Denmark                      1 Available from the Formal Methods Europe association: https://fme-
4    University of Twente, PO box 217, 7500 AE Enschede, The                  teaching.github.io/courses.
     Netherlands                                                              2 The Formal Methods Body of Knowledge (FMBoK): https://
5    University of York, Deramore Lane, York YO10 5GH, UK                     formalmethods.wikia.org.


                                                                                                                                      123
1738                                                                                                                      M. Gleirscher et al.


most alarmingly, even in safety-critical domains [24] where               2 Background
their application is, in parts and through a range of stan-
dards, explicitly recommended (e.g. IEC 61508 and 62443,                  2.1 What is a “formal method”?
DO-178). A progressive exception to this observation is the
railway domain [25] where formal methods are strongly rec-                There are many useful characterisations available from the
ommended (see EN 50128 and 50129) and frequently applied                  literature. For example, the IEEE Software Engineering Body
for highest-integrity level software.                                     of Knowledge says: “formal methods are software engineer-
    Thus, it is reasonable to assume that formal methods,                 ing methods used to specify, develop, and verify the software
still or again, seem not applicable enough or ready for their             by applying a rigorous mathematically based notation and
intended purpose. An alternative explanation would be that                language” [28, p. 9-7, Sec. 4.2]. A more recent definition [29]
modern programming languages and environments (e.g. C++                   covers the relevant aspects quite well, stating that “formal
2017, C#, Go, Java/Scala, Python 3, Rust) implicitly sup-                 methods are a set of techniques based on logic, mathe-
port a good part (e.g. run-time type checkers, static analysis            matics, and theoretical computer science that is used for
in IDEs, memory models in compilers, structured primitive                 specifying, developing, and verifying software and hardware
types such as lists) of what would have been called formal                systems.” We slightly refine this notion, saying that, by a for-
development in the period from the 1970s to the 1990s and                 mal method, we refer to an explicit mathematical model and
avoid many of the hard sought-after errors formal methods                 sound logical reasoning about critical properties [30]—such
were originally supposed to unveil [26]. This explanation is,             as reliability, safety, security, dependability, performance,
however, only reasonable if we ignore the massive increase                uncertainty, or cost—of a class of electrical, electronic, and
in software and hardware complexity since then and the                    programmable electronic or software systems. Model check-
increase in the use of software in areas with critical require-           ing (cf. [31, 32]), interactive theorem proving (e.g. [33–35]),
ments. Consequently, new kinds of problems and errors have                abstract interpretation and static analysis [36–38], program
emerged, and the original justification for using formal meth-            verification (e.g. [39–41]) and formal contracts [42] are clas-
ods remains valid, albeit at different levels of abstraction.             sical examples of versatile formal methods.
    In that light, the beneficial use of formal methods is hin-               Formal methods range from lightweight to heavy-weight
dered, for example, by poor scalability, missing, inadequate,             formalisms. The former usually focuses on full automation
or unqualified [27] tools, formal methods teaching and train-             at scale (e.g. model checking and abstract interpretation)
ing not reaching enough students and practitioners, and thus              or on providing formal techniques to programmers (e.g.
a shortcoming of trained personnel [15]. Of course, the natu-             through type systems, assertion languages, and IDE inte-
ral resistance against adopting new technologies or methods               gration). In contrast, the latter focuses more on guiding
exacerbates that situation. The lack of current knowledge                 software and systems engineers in their manual work steps
about these obstacles and the effectiveness and productiv-                (e.g. refinement-based methods such as B [23], VDM, or
ity of formal methods [24] raises a high demand for formal                Z [43]). Further approaches combine several (formal) tech-
methods research and goal-directed collaborations between                 niques under a correctness-by-construction philosophy (e.g.
academia, regulators, and industry. To help research and                  [44]). Finally, it is essential to note that there is a natural
transfer efforts gain momentum and foster success, we3 sug-               overlap between the formal foundations of computer science
gest some guiding principles of applicable formal methods                 and what is typically understood as a formal method in the
in forming a manifesto.                                                   more specific field of software engineering.

1.1 Outline                                                               2.2 What makes formal methods so special?

Sections 2 and 3 provide the background and motivation of                 Generally, a method can be considered a step-wise recipe
this manifesto and highlight related work. Section 4 repre-               guiding its user regarding the next steps in certain situations.
sents the manifesto, highlighting its ten principles in detail.           In analogy to other engineering disciplines, a formal method
Table 1 summarises the manifesto in a self-contained way.                 pushes the role of mathematics and logic in software engi-
Section 5 highlights some formal methods success stories.                 neering
Section 6 summarises aims, suggests actions to implement
the manifesto, and outlines the expected impact of these                   • to make objects explicit (e.g. natural processes, informa-
actions. Section 7 warns about the potential consequences                    tion, peoples’ thoughts) through notation with a precise
of inaction by the community, and Sect. 8 concludes.                         meaning agreed within a domain,
                                                                           • to reduce ambiguity about or subjective interpretation of
3 With “we/our”, we mean all the supporters or signatories of this man-      these objects (e.g. a system or its functioning) and foster
ifesto, including the initiators.                                            a precise understanding of that domain, and


123
A manifesto for applicable formal methods                                                                                             1739


 • to support mechanisation of critical or tedious tasks (e.g.              For example, a proof assistant with a sound core would
   analysis, verification).                                              be logically and algorithmically mature. Still, it might not
                                                                         be applicable enough if its user interface (e.g. the proof lan-
These features distinguish formal from informal (or “non-                guage and editor) or the theorem development facilities (e.g.
formal”) methods.4 A formal method is more than a (mod-                  assistance with invariant and proof search) are less advanced.
elling) notation or a development or analysis method and
differs from a programming language or a software engi-
neering tool.                                                            2.4 When do we expect a formal method to be
    Although there is no clear boundary between formal and                   applicable?
informal methods (formality may occur in degrees), one can
think that a software engineering method is “informal” if the            We expect applicability whenever we suggest a formal
use of mathematics and logic is neither essential nor required           method as a critical (quality assurance) instrument to be used
to achieve some useful results, and it is “formal” if mathemat-          at the core of a critical engineering task. That task will pri-
ics or logic are employed for achieving sound results reliably.          marily be a practical software engineering task, but it can
In model-based development and model-driven engineer-                    also be an engineering task in computer science research and
ing [45], a more nuanced distinction frequently made is the              teaching. While this expectation might sound obvious, it is
one between informal, semi-formal (providing a formalised                less so in the context of formal methods research, often not
syntax), and formal (associating formal semantics with this              getting the funding and opportunities to mature beyond sim-
syntax) techniques.                                                      ple applications and towards industrial scenarios.
                                                                            A formal method can be said to be directly applicable if the
2.3 What do we mean by “applicability”?                                  expected benefit from using the method in a task (e.g. early
                                                                         error reduction, design improvement, didactic gain, scientific
Generally, “applicable” means capable of being applied,                  insight) justifies the expected cost of applying it (e.g. formal-
within some defined and practically relevant scope. More                 isation effort, time, and resources). Conversely, it can be said
specifically, applying a formal method involves its use in the           that such a method is indirectly applicable if the expected
design, development, and analysis of a critical system and its           cost of not applying it (e.g. late failure handling costs, failure
substantial integration with the used                                    consequences) for that task would not be justified or accept-
                                                                         able.
 • development methodologies (e.g. structured develop-
   ment, model-based or model-driven engineering, assertion-
   based programming, test-driven development),                          2.5 What makes formal method applicability so
 • specification and modelling notations (e.g. UML, SysML),                  special?
   domain-specific languages, or programming languages,
   and                                                                   What makes it different from the applicability of other mod-
 • tools (e.g. compilers, checkers, integrated development               elling or programming methods, techniques, or languages?
   environments).                                                        A formal method requires one to use (through tools and with
                                                                         guidance) mathematical structures to represent and make
When we use the terms “applicable” or “applicability”, we                concise the meaning of objects (e.g. software or system
refer to a desirable degree or level of maturity5 of a formal            behaviour, data sets) to be reasoned upon. Proper under-
method. Consequently, this notion suggests some quanti-                  standing and efficient use of such structures need specific
tative (e.g. performance or economic) assessment to make                 abstraction capabilities, mathematical skills to be taught,
objective statements about the level of maturity and, thus,              and continuous application-oriented training. An applicable
the applicability of a formal method.                                    formal method is a method that addresses these particular
                                                                         requirements in this specific context.
4 For example, UML is a standardised notation and carries, through its

many historically inspired concepts, flavours of methods. However, to
obtain a corresponding formal method, UML’s concepts must be under-
pinned with precise semantics and a method to construct and reason       2.6 What is a manifesto, and why do we need one?
about UML models. Similarly, Java has a reasonably well-specified
grammar and platform. However, to obtain a formal method for Java,
executions of a Java program need to be given precise semantics and a
                                                                         A manifesto can be understood as “a series of technical or
method to reason about it logically and conceptually.                    expert views on a particular engineering task” [46], “a set
5 In analogy to NASA’s Technology Readiness Levels (NASA) and the        of commitments” of a community [47], or “a focal point of
CMMI framework from CMU.                                                 reference” catalysing communities [48]. Inspired by similar


                                                                                                                               123
1740                                                                                                                         M. Gleirscher et al.


successful efforts in other domains [48, 49],6 we summarise:            4.1 Motivation and provisional diagnosis
A manifesto expresses some consensual agreement among
stakeholders (e.g. experts, thought leaders, and users) in a            Formal methods aim at applicability and have been shown
domain, it is based on corresponding definitions, it concisely          to be effective. There is a perceived demand for them, since
conveys guidance in principles, discloses aims and commit-              practitioners are interested in using formal methods more
ments in the form of an appeal, suggests actions and can join           frequently. However, formal methods are less applied than
forces and, thus, initiate change.                                      expected, particularly in application domains with critical
                                                                        requirements.
                                                                           A provisional diagnosis is that formal methods still seem
3 Related work                                                          not applicable enough or ready for their intended use. Hence,
                                                                        we hypothesise that increasing their applicability will lead to
Our manifesto can be seen as a specific supplement of the               a broader adoption of formal methods both in research and
Verified Software Initiative [50], which has the long-term              practice.
aim to perform wide-ranging verification experiments and
case studies, improve the tool landscape, and foster the trans-
fer of formal methods research to industry. It also addresses           4.2 The ten principles of applicable formal methods
two principles of the wider digital humanities manifesto:7
software researchers and practitioners are responsible for              The manifesto recommends several principles that, when
the impact of their technologies and must reflect upon their            followed, can evidence various degrees of applicability of
approaches.                                                             a formal method both in research and practical software
   Kapor’s manifesto [51] proposed software design as a pro-            engineering. Consequently, an applicable formal method is
fession distinct from software engineering and driven by user           supposed to implement a coherent selection of these princi-
orientation. Our manifesto relates to Kapor’s ideas in that it          ples, albeit without the expectation that it will be possible or
builds on the observation that formal methods can be benefi-            optimal to implement all of them simultaneously. The prin-
cial for conceptual or design prototyping, formal methodists            ciples are detailed below.
are often in a neglected role, perhaps similar to software
designers in the 1980s and 1990s, and it delivers an argu-
ment of why and how formal methodists could soon act as                 4.2.1 Scope
successful specialist software designers.
   Ladkin’s manifesto [46, Ch. 10] includes principles and              A formal method should clearly define its scope of applica-
steps for using formal methods in practical and standard-               bility8 , its domain specificity, and come with understandable
compliant software assurance. At the same time, his mani-               guidance on how it is to be applied within that given scope.
festo covers many areas of software assurance; the section              The restriction to a limited scope may reduce some acciden-
on formal methods guidance concentrates on using formal                 tal complexity of the formal model and, thus, increase Ease
methods in assurance. Our manifesto complements Ladkin’s                of Use and support other principles.9
work with guidance on preparing formal methods applicable
in assurance and beyond.
   Rae et al.’s manifesto [47] aims to improve the use of               4.2.2 Methodology
research methods in safety science, however, not touching
on formal methods’ applicability in software safety.                    A formal method should provide a step-wise recipe and pro-
                                                                        cedural guidance for method users regarding possible next
                                                                        steps in corresponding situations. For example, it could sup-
4 The manifesto and its ten principles                                  port composition, modularity (e.g. using formal reasoning
                                                                        [52] about contracts [42]), and refinement, and come with
This section represents the manifesto with its goals, princi-           various sound abstraction or simplification techniques or at
ples, and aims. Each principle is explained and commented               least a range of effective modelling and specification guide-
on in more detail. Table 1 contains a concise version of the            lines.
manifesto to be communicated and referred to.

6 See also the GNU Manifesto (1985, https://www.gnu.org/gnu/            8 For example, embedded software engineering research or safety-

manifesto.html) and the Agile Manifesto (2001, http://agilemanifesto.   critical software practice in the automotive control domain.
org).                                                                   9 Generic methods will have a wider scope and some problems (e.g.
7 https://caiml.dbai.tuwien.ac.at/dighum/dighum-manifesto.              undecidability) are insurmountable.


123
A manifesto for applicable formal methods                                                                                                     1741


Table 1 The manifesto and its ten principles at a glance

Motivating observations
Success stories         Formal methods aim at applicability and were shown to be effective
Perceived demand        Practitioners are interested in using formal methods more frequently
But: Scarce use         Formal methods are less applied than expected, particularly in application domains with critical requirements
Provisional diagnosis
Formal methods still seem not applicable enough or ready for their intended use
Ten principles / precepts / commitments
Scope                   Clearly define the scope of applicability
Methodology             Provide concepts, tools, and procedural guidance (for scalability)
Integration             Integrate with methods, modelling techniques, and programming languages
Explainability          Allow established claims to be communicated precisely and clearly
Automation              Provide automated abstractions (for scalability)
Scalability             Apply to the size/complexity of systems operated in practice
Transfer                Provide teaching and training strategies
Usefulness              Provide evidence on effectiveness (for a good cost/benefit ratio)
Ease of Use             Provide evidence on efficiency (for a good cost/benefit ratio)
Evaluation              Demonstrate applicability in a credible way
Aims, actions, and expected impacts
Provide guidance for performing, writing, and reviewing formal methods research
Drive the selection of relevant unsolved (benchmark or fundamental) challenges and stimulate research proposals
Foster interactions between academia and industry
Establish connections between formal method developers and users (through explainability) and customers (through economic arguments)



4.2.3 Integration                                                            ment would be that a certificate can be generated, which
                                                                             enables checking the claim independently. Last but not least,
A formal method should create benefits through integration                   it requires that the claim (including the underlying modelling
with other methods. For example, it could be integrated10                    assumptions) can be communicated to human domain experts
with                                                                         and maybe even to end users. Explainability in this way is
                                                                             supposed to increase Usefulness.
  (i) a familiar design or engineering technique (e.g. contract-
      based design),                                                         4.2.5 Automation
 (ii) a widely used modelling technique (e.g. State Charts
      used in UML/SysML),                                                    A formal method should come with tool support that pre-
(iii) a programming language (e.g. JavaScript, C/C++,                        vents users from tedious work steps and helps them focus
      Java), or                                                              on essential and creative steps. In particular, it should pro-
(iv) a process model (e.g. Scrum).                                           vide automation support for any obvious or useful abstraction
                                                                             required to apply the method to the maximum benefit.
Integration in this way is supposed to increase Usefulness                   Automation usually pertains to difficult or tedious tasks and
and Ease of Use.                                                             can, thus, increase Scalability towards industrial-sized sys-
                                                                             tems.
4.2.4 Explainability
                                                                             4.2.6 Scalability
After successfully applying a formal method, what has been
demonstrated should be clear [27]. A minimal requirement                     A formal method should be applicable at a practically rele-
is that it can precisely state which claim has been established              vant scale,11 manageable with reasonable effort as a function
(as in a mathematical theorem). An even stricter require-
                                                                             11 Where scale may be quantified as, for example, lines of code, the
10 Conceptually aligned, representing a semantic layer for other meth-       number of fulfilled requirements or discharged theorems, the size of a
ods, presented through a common tool layer.                                  state space, or by a measure of complexity.


                                                                                                                                        123
1742                                                                                                                       M. Gleirscher et al.


of that scale. This principle is likely to be fostered by a clear         engineering problems and systems in its specified scope.
Methodology (e.g. superior algorithms, abstraction, modular               When proposed or presented, a formal method should be
approaches) and strong Automation.                                        accompanied by information about its benefits and foreseen
                                                                          challenges, limitations, or barriers. This principle integrates
4.2.7 Transfer                                                            the scientific method into the argumentation of formal meth-
                                                                          ods’ applicability.
A formal method should be accompanied by a teaching and
training strategy and corresponding materials. 12 This strat-             4.3 Aims, actions, and expected impact
egy and the materials may differ from one formal method to
another. However, average graduate students and experienced               The manifesto aims to provide guidance for performing, writ-
engineers should also be able to learn and apply a method                 ing, and reviewing formal methods research. It could drive
with reasonable effort. Notably, the mere availability of good            the selection of unsolved (benchmark or fundamental) chal-
teaching materials is not enough to reach a sufficiently large            lenges and stimulate research proposals and projects. More-
fraction of the student and practitioner cohorts.                         over, it could foster further interactions between academia
                                                                          and industry and establish connections between formal
4.2.8 Usefulness                                                          method developers and users (through explainability) and
                                                                          customers (through economic arguments).
The application of a formal method should be effective. For
example, it could be demonstrated (e.g. using case studies or
controlled experiments) what would have been different if a               5 Success stories of formal methods
conventional or non-formal alternative had been used instead                integration and transfer
(e.g., comparing relative fault-avoidance or fault-detection
effectiveness and the economic impacts of these metrics).                 There is plenty of anecdotal and stronger evidence on apply-
Usefulness as the governing factor for applicability will result          ing formal methods, not least in the form of success stories
from other principles, such as Explainability.                            of research integration, application, and transfer. Here, we
                                                                          mention some illustrative examples, without any ambition to
4.2.9 Ease of use                                                         be complete.

A formal method should be efficiently13 applicable. For                   5.1 Research integration
example, it could provide concepts, abstractions, or mod-
elling and reasoning primitives that help users with appropri-            Unifying Theories of Programming (UTP) is Hoare & He’s
ate skills (cf. Training) to apply it with reasonable effort (e.g.        long-term research agenda [54]. They intend to explore
low abstraction effort, low proof complexity, high productiv-             a common basis for understanding the semantics of the
ity) within the specified scope. Ease of Use can be addressed             modelling notations and programming languages used in
by other principles, such as Scalability and Automation, but              describing the behaviour of computer-based systems. Their
can also be approached in isolation. Usefulness and Ease                  technique is to describe diverse modelling and program-
of Use refer to the two main constructs of the Technology                 ming paradigms in a common semantic setting. They isolate
Acceptance Model [53], a widely used class of models for                  the individual features of these paradigms to emphasise
the assessment of end-user information technology.                        commonalities and differences. They devise formal, often
                                                                          approximate, links between theories to translate predicates
                                                                          from one theory into another. The links also translate specifi-
4.2.10 Evaluation
                                                                          cations into designs and programs as a development method.
                                                                          Understanding the links between formal methods is essen-
The principles above should be properly evidenced. Appli-
                                                                          tial, especially for building toolchains for heterogeneous
cability could be demonstrated compellingly (e.g. with rep-
                                                                          approaches.
resentative examples, with tools usable by other researchers
or practitioners, perhaps even with qualified tools [27]) by
showing that a formal method applies well to the range of                 5.2 Method and tool integration

12 Educational prerequisites, theoretical background material, exam-
                                                                          The Ptolemy project14 is a long-term effort to provide
ples, case studies, user guides, and tool manuals.
                                                                          an environment for specification, modelling, and simula-
13 Note that the term “efficiency” here refers to the gain/effort ratio   tion of concurrent systems based on a semantic framework
on the user’s side. Efficiency in terms of short tool run-time or low
algorithmic complexity is subsumed under Automation, Scalability.         14 https://ptolemy.berkeley.edu/ptolemyII/summary.htm.




123
A manifesto for applicable formal methods                                                                                   1743


for integrating components with heterogeneous models of            sectors where (automated) theorem provers and model check-
computation [55]. The AutoFocus project15 [45, 56, 57] is          ers have been routinely applied to scrutinise their ever more
another example of such a long-term effort, focusing on for-       complex circuits, for instance, at INTEL [67, 68], IBM [69]
mal methodological support from requirements capture and           and Oracle [70]. Perhaps this is because chips are mass-
visual specification down to code generation, testing, and         produced. Hence the costs of errors are high, and thus the
artefact evolution. Several large case studies in model-based      effort of applying formal methods paid off early.
development of embedded software were conducted over the               Another traditional sector for applying formal methods
years using different AutoFocus generations. Projects such         is the railway signalling domain, which their safety-critical
as Ptolemy and AutoFocus can be considered rigorous                nature can easily explain. Very early applications of for-
top-down approaches to constructing seamless toolchains for        mal methods to railways have been reported [25]. Many
engineering embedded software.                                     European projects (e.g. FMERail, INESS) and indeed whole
   Another point of view is taken by the jETI platform [58],       conferences (e.g. RSSRail16 ) studied the application of
integrating tools through web interfaces and enabling users        such methods to the railway domain. Although this could
to specify and realise new interactions between different for-     still be an academic exercise, increasingly, the agenda of
mal analysis tools. There is also integration between various      formal methods in railways is set by engineering compa-
paradigms, for instance, approaches combining model check-         nies (SHIFT2RAIL17 ) and infrastructure managers (EUL-
ing and theorem proving, as realised in PVS [59] and TLA+          YNX18 ). Indeed, the latter is quickly building expertise
[60].                                                              centres in model-based software engineering and formal ver-
   Yet another success story is the use of program verifi-         ification.
cation tools, that make formal methods directly applicable             In the past, a successful route to the broader deployment
to programs in widely used programming languages. Based            of formal methods in practice has been the standardisation of
on Hoare logic and separation logic, these tools leverage          their notations, for example, through ISO. Notable standard-
the recent progress in the efficiency of symbolic execution        isation efforts in this regard are, for instance, LOTOS [71],
and SMT solvers. Note that these tools require programmers         SDL [72], and the Z notation [43], and more recently PSL
to make extensive annotations in the source code. Notable          [73].
examples are Frama-C [61] (for C), KeY [40] (for Java),
SPARK [62] (for ADA), Vercors [41] (for concurrent Java            5.5 Non-embedded systems applications
and C with OpenMP or OpenCL), VeriFast (for concurrent
C and Java) and VIPER [63] (with front-ends for Go, Java,          Finally, formal methods are now also applied routinely in
Python and Rust).                                                  purely software-based platforms. An important initial exam-
                                                                   ple was the SLAM project at Microsoft [74], aimed at
5.3 Transfer through automation and unified visual                 Windows device driver compliance. Moreover, Facebook [6,
    environments                                                   75] and Amazon Web Services [76, 77] have reported on the
                                                                   application of formal methods for their infrastructure at a
Fully automated techniques, such as symbolic model check-          massive scale. Perhaps, this happened because formal meth-
ing [64, 65], assertion checking, and abstract interpretation      ods have matured. Another possible explanation is that the
[36] were demonstrated to be lightweight and scalable and,         availability and security requirements of contemporary soft-
thus, turned out to be an effective vehicle for the adoption       ware platforms are incredibly high. These platforms have
of formal methods in security- and safety-critical applica-        taken up the role of critical infrastructure. Other highlights
tions (e.g. chip production, operating system kernels, railway     in verified software are the formally verified optimising com-
systems). Additionally, unified and domain-specific visual         piler CompCert [78] and the formally verified Operating
modelling languages [66] (leading to e.g. UML and SysML),          System Microkernel seL4 [79].
combined with integrated model-driven development envi-
ronments, have played an important role in that adoption           5.6 Activities towards wider adoption
process.
                                                                   It could be argued that an even wider adoption can only be
5.4 Transfer via standards                                         realised by making formal methods applicable by average
                                                                   software engineers who have received an MSc degree in com-
The profit from formal methods is supposed to be maximal           puting or engineering. Apart from professional, easy-to-use
when thoroughly integrated into a company’s design and ver-
                                                                   16 https://rssrail2022.univ-gustave-eiffel.fr.
ification processes [24]. The chip industry was one of the first
                                                                   17 https://shift2rail.org.

15 https://www.fortiss.org/ergebnisse/software/autofocus-3.        18 https://www.eulynx.eu.




                                                                                                                      123
1744                                                                                                                      M. Gleirscher et al.


tool support, this requires insight into the trade-off between        (e.g. increase trust through Explainability, see Table 1),
investments in and benefits from formal methods applica-              to investigate the economic benefits through formal meth-
tion, as advocated in [80]. It also requires integrating formal       ods (e.g. economical value, metrics), or to develop new
methods tools with other artefacts in the usual design pro-           business models integrating such methods.
cesses, for instance, in agile development [81]. The benefits      4. Initiate a community of researchers that (i) performs eval-
of formal methods for making the process of code reviews              uations of existing formal approaches and new variants in
more efficient have been studied in [82].                             practical contexts, (ii) develops new formal approaches
   The evidence available from these success stories ranges           with an interest in achieving applicability early, and (iii)
from single to aggregated opinions of experts as well as              supports the transfer of these methods into dependable
anecdotal to very systematic case studies and thorough yet            systems practice.
sporadic tool evaluations. However, data from across a rep-
resentative range of samples have never been rigorously            We detail some of these impact categories below.
measured (e.g. using controlled method experiments [7, 8]).
Hence, albeit impressive, this evidence cannot underpin a          6.2 Impact on the conduct, writing, and review of
strong argument for a wider deployment of formal meth-                 formal methods research
ods in the industry. And without such a deployment, further
formal methods research risks becoming inapplicable. The           Showing the novelty of research on applying formal methods
underlying hypothesis that applicability is a core driver of       concerning state of the art is more complicated than show-
wider deployment is adopted from the theory of the Technol-        ing the novelty of a particular formal technique. Examples
ogy Acceptance Model [53].                                         and the superiority of an algorithm or tool can explain a for-
                                                                   malism, and its expressive power can be demonstrated by
                                                                   experiments, for instance, comparing a range of settings.
6 An impact-oriented plan for actions                              However, the evaluation of the applicability of a formal
                                                                   method as a whole is more intricate. So, what is the rec-
A manifesto should follow a specific aim, suggest possible         ommended way for research on applying formal methods?
actions, disclose the potential impacts hoped for, and discuss     How can one demonstrate its novelty concerning the state of
relevant implications.                                             the art?
                                                                      A few (old) answers [83] within software engineering
6.1 Overview of the expected impact of the                         research are: case studies [84], action research [85, Sec. 5.5]
    manifesto                                                      and controlled method experiments [86] [85, Ch. 8]. Fol-
                                                                   lowing these methods would greatly benefit the formal
We hope that the manifesto for applicable formal methods           methods community; Yin’s20 and Wohlin et al.’s proce-
will:                                                              dures provide welcome guidance. Specific guidelines will
                                                                   effectively aid researchers in conducting evaluation research,
1. Foster the collection and curation of real (small, medium,      writing results, and performing peer reviews in a repeatable,
   large) open19 problems (inspired by the success stories in      standardised, and fair manner. The manifesto’s principles
   Section 5) to be tackled by formal methods. At the lowest       (Section 4.2) may serve as an initial template for such guide-
   level, these can be benchmarks defined by practitioners,        lines. Explicitly addressing the Evaluation principle of this
   formal method users, or regulators (e.g., a “formal meth-       manifesto, ter Beek and Ferrari [87] propose detailed guide-
   ods with industry week” with short-term interactions to         lines for empirical studies on formal methods and tools.
   identify problems at a national or international level and
   follow-up commitments).                                         6.3 Implications of the manifesto on future formal
2. Provide guidance on how to perform formal method case               methods teaching
   studies and write case study papers and how to review
   them. We define a case study as an intensive examination        It is essential to have good case studies that are relevant to
   of a single example to generalise across a more extensive       students. They must be able to recognise the problem being
   set of examples. This generalisation makes case studies         solved. They should have realistic case studies for every vital
   helpful in teaching and industrial practice.                    concept taught in a formal methods course. This is particu-
3. Stimulate new research proposals and interdisciplinary          larly important for industrial courses, where it helps if the
   research collaboration, for example, to improve the inter-      presenter has good industrial experience using the formal
   face between different formal methods and their users           method. Robust tools are essential. There must be parsers

19 Challenging problems not yet solved in a satisfactory manner.   20 I.e. plan, design, prepare, collect, analyse, and share.




123
A manifesto for applicable formal methods                                                                                              1745


and type checkers. Model checkers are attractive but can           projects or the pure response to scientific questions. Only
disappoint if newcomers have difficulty scaling their use.         appropriately funded research projects will create convincing
Theorem provers have a higher entry barrier, but their suc-        evidence. Without such funding, however, an implementation
cess can be inspiring. A successful course teaches not just        of the manifesto will unlikely be successful.
one formal method but families of formal methods: students
like to see the connections between different formal methods.
Industrial courses should show how formal methods fit into
software management processes and popular methodologies.           6.5 Impact on the further development of the
This includes combining formal methods with testing strate-            formal methods community
gies and their role in formal domain engineering as part of
requirements engineering.                                          The manifesto could reduce the current fragmentation of
    In the context of the many (old) discussions about teaching    the formal methods community by subsequently integrat-
programming at grammar and secondary schools, a nearby             ing selective sub-communities, for example, communities
idea would also be to extend or even replace specific lessons      working on common semantic frameworks (e.g. the UTP
in traditional (e.g. procedural) programming paradigms with        community24 ) or formal method integration (e.g. the sub-
carefully thought-through studies in conceptualising pro-          communities around the “Formal Methods in Industrial Crit-
grams (e.g. by using simple automata) and using school             ical Systems (FMICS)", “Integrated Formal Methods (iFM)”,
mathematics to specify data and behaviour. Such preparation        “NASA Formal Methods (NFM)”, “Software Engineer-
in schools could foster formal methods of understanding and        ing and Formal Methods (SEFM)”, and “Forum Méthodes
use in later stages of education and training at university and,   Formelles” conference series25 ). Research artefact evalua-
finally, in industrial practice.                                   tion, often performed at these venues, effectively implements
                                                                   critical parts of the manifesto. Moreover, the manifesto could
6.4 Impact on the evaluation of future formal                      inspire new actions of researchers to work towards a collec-
    method research                                                tion of formal methods that follow the proposed principles.
                                                                      To make ongoing successes (Sect. 5) more sustainable, a
We expect the manifesto to motivate researchers to carry out       bilateral knowledge transfer should be ensured. The ability of
comparative method and tool evaluations (e.g. [88]), realistic     companies to adopt effective formal methods or even get their
case studies and goal-directed action research, and controlled     integration publicly funded should create incentives and per-
method experiments improving over previous lessons learnt          haps obligations for these enterprises to share their findings
[7, 8].                                                            from such efforts with the community. Indeed, the FM Europe
   For example, in the ABZ community, there are ongoing            Industry Committee26 runs a communication platform (e.g.
activities to create a case study library.21 Another example is    with seminars) to give formal method users from industry an
the VerifyThis collaborative long-term verification challenge      opportunity to share their insights and receive feedback from
bringing together formal methods researchers to show “that         formal method experts.
deductive program verification can produce relevant results           Closing this transfer feedback loop can integrate parts of
for real systems with acceptable effort”.22 Furthermore, the       the formal methods community. A further de-fragmentation
“Formal Methods for Autonomous Systems (FMAS)” work-               of the community could be fostered by a collective formal
shop series23 has adopted some principles of this manifesto        methods event, akin to CPS Week, ETAPS, or the Embed-
as a recommendation for authors when doing their research          ded Systems Week, with a critical mass of audiences from
evaluation.                                                        all corners of the community and from industry to create a
   Our field still suffers from a lack of sustainable funding      win-win situation and a fruitful competition for the tradition-
for software as a research infrastructure [89]. After being        ally smaller events. Results of orchestrated cross-community
recognised by the community, the funding agencies, and their       research evaluations (such as the VerifyThis challenge) using
committees, the manifesto has the potential to create new          practical benchmarks might as well be presented regularly at
lines and formats of research funding shaped explicitly to         such an event.
the needs of formal method evaluation and tool development,
such as funding for experiments and entrepreneurship fund-
ing for spin-offs. Comparative method experiments (e.g. [7,
8]) and usable tool interfaces require resources beyond PhD        24 https://www.cs.york.ac.uk/circus/utp2019.

                                                                   25 http://fmics.inria.fr,      http://www.ifmconference.org,     https://
21 https://abz2021.uni-ulm.de/case-study.
                                                                   shemesh.larc.nasa.gov/nfm2021,           https://sefm-conference.github.
22 https://verifythis.github.io.                                   io, https://projects.laas.fr/IFSE/FMF/.
23 https://fmasworkshop.github.io/FMAS2023.                        26 https://fmeurope.org/industry/.




                                                                                                                               123
1746                                                                                                                             M. Gleirscher et al.


6.6 Impact on software engineering as a legally                              lack of researcher engagement and, thus, research funding
    recognised profession                                                    [24, pp. 117:23,29].
                                                                                Secondly, formal methods might be wiped out by oppor-
In his Turing Award acceptance speech about 40 years ago,                    tunistic trends or powerful convenience technologies (e.g. rely-
Tony Hoare reviewed type safety precautions in program-                      ing too much on search- or AI-based software engineering)
ming languages and concluded: “In any respectable branch                     that can worsen the highlighted problems. It can be observed
of engineering, failure to observe such elementary precau-                   that software solutions constructed through automatic search
tions would have long been against the law” [26]. In this                    may require significant further investments into the reverse
regard, for example, U.S. law still does not recognise com-                  engineering of these solutions to verify them. This may hap-
puting (including software engineering) as a profession [90],                pen frequently in cases where not all critical properties to be
opposing ACM’s self-perception [91]. This is mainly because                  verified can be encoded into the search criteria.
software practitioners’ work is not subject to malpractice                      Thirdly, AI-based program synthesis techniques are about
claims based on a legal concept known as customary care.                     to replace parts of traditional programming with specifica-
Customary care defines (i.e. standardises) best practice more                tion tasks [94]. Without applicable formal methods and a
stringently27 than the notion of reasonable care applied to                  corresponding education, future software developers could
any occupation or business [90].                                             lack the specification skills needed to be literate in this new
    From a computing standpoint, ongoing legal debates about                 programming paradigm and to generate adequate software.
which other occupations28 should be treated as professions                   Appreciating Welsh’s reasonable forecast, we might still
could be advanced by this manifesto, corroborate codes such                  need to know how to specify, for example, efficient sort-
as ACM’s Code of Ethics and Professional Conduct [92]29 or                   ing and searching over human-usable input/output types to
the Ethical Guidelines of the German Informatics Society,30                  get something as beautiful and concise as quicksort or binary
and help to standardise results from the formal methods com-                 search correctly from an AI-based code generator [95].
munity as reasonable best practices underpinning such codes.                    Ultimately, decreasing global coordination among for-
    In Denmark, 51% of the developers hired by IT compa-                     mal methods researchers can lead to an extinction of the
nies developing software do not have a BSc/MSc degree in                     formal methods community, which is currently somewhat
computing.31 This situation is expected to be generalised to                 fragmented. It is difficult for the community to maintain
other European countries and, to a minor degree, to critical                 too many notations and too many tools and still make fast
application domains. To counter this development, Lichten-                   progress. This situation seems unique among related or other
berger [93], for example, suggests (again) treating software                 scientific disciplines (i.e. STEM33 ). Also, there is a prolifera-
engineering as a classical engineering discipline and striving               tion of formal method conferences and workshops competing
for accreditation. Along these lines, this manifesto could aid               for the same resources (i.e. papers, reviewers, etc.). Ide-
in the expansion of existing software engineering profession-                ally, a representative, coordinated approach could lead to an
alism32 within such domains.                                                 authoritative voice towards the scientific, governmental, and
                                                                             industrial communities and, perhaps, inspire new schemes
                                                                             for research funding.
7 A life without the manifesto

Above, we summarised the actions and expected outcomes                       8 Conclusions and outlook
of successfully implementing the manifesto. However, some
negative long-term consequences of not following an agenda                   The manifesto for applicable formal methods expresses aims
implied by the manifesto are to be foreseen.                                 and intentions. We hope it will give crucial impulses to for-
   Firstly, the progress of formal method research might be                  mal methods researchers to implement a modern research
further threatened by missing scalability, vacuous proofs,                   agenda for developing formal methods that can arguably be
lack of user education and training, poor tool integration,                  used for critical software engineering research. Even more
                                                                             importantly, these methods should be usable in the practi-
27 Taking state of the art including recent scientific results as a refer-
                                                                             cal engineering of systems and software whose functioning
ence.
28 “[E]very court to consider this question has refused to recognise
                                                                             is vital and whose failure would have unacceptable conse-
software developers as professionals” [90, p. 23].                           quences. Rather than exercising criticism of past develop-
29 Version 2018: https://www.acm.org/code-of-ethics.                         ments, the manifesto strives to foster progress in a currently
30 https://gi.de/ethicalguidelines.                                          dissatisfying situation found in the science of formal meth-
31 https://www.prosa.dk/artikel/nu-er-der-over-100000-it-                    ods.
professionelle.
32 https://en.wikipedia.org/wiki/Software_engineering_professionalism.       33 Science, Technology, Engineering, Mathematics.




123
A manifesto for applicable formal methods                                                                                                     1747


Acknowledgements We are grateful to Maurice ter Beek, Angelo                11. Parker, D., Norman, G., Kwiatkowska, M.: PRISM Model Checker
Gargantini, Frederik Krogsdal Jacobsen, Peter Gorm Larsen, Yan-                 (2022). http://www.prismmodelchecker.org/manual/
nick Moy, Jan Peleska, Elvinia Riccobene, and Bernhard Steffen for          12. Jones, C.B.: Software Development: A Rigorous Approach. Pren-
encouraging comments and valuable suggestions, also during the dis-             tice/Hall, Englewood Cliffs (1980)
cussion of this manifesto at our “Applicable Formal Methods (AppFM)”        13. Nipkow, T., Klein, G.: Concrete Semantics. Springer, Cham (2014)
workshop [96] (https://sites.google.com/view/appfm21/manifesto) co-         14. Garavel, H., ter Beek, M.H., van de Pol, J.: The 2020 expert survey
located at FM 2021. Further, thanks go to Marie Farrell and Matt                on formal methods. In: ter Beek, M.H., Ničković, D. (eds.) For-
Luckuck for including the manifesto as a recommendation in the FMAS             mal Methods for Industrial Critical Systems (FMICS), pp. 3–69.
workshop series submission guidelines. Finally, we thank three anony-           Springer (2020)
mous reviewers for providing us with many helpful comments.                 15. Gleirscher, M., Marmsoler, D.: Formal methods in dependable sys-
                                                                                tems engineering: a survey of professionals from Europe and North
Author contributions MG contributed the idea for the manifesto. All             America. Empir. Softw. Eng. 25, 4473–4546 (2020)
authors performed the literature research, wrote and discussed the draft,   16. Hall, A.: Seven myths of formal methods. IEEE Softw. 7, 11–19
and critically revised the work.                                                (1990)
                                                                            17. Bowen, J.P., Hinchey, M.G.: Seven more myths of formal methods.
Funding Open Access funding enabled and organized by Projekt                    IEEE Softw. 12, 34–41 (1995)
DEAL.                                                                       18. Knight, J.C., DeJong, C.L., Gibble, M.S., Nakano, L.G. Holloway,
                                                                                C.M., Hayhurst, K.J. (eds.): Why are formal methods not used
Declarations                                                                    more widely? In: Holloway, C.M. Hayhurst, K.J. (eds). 4th NASA
                                                                                Formal Methods Workshop, pp. 1–12 (1997)
                                                                            19. Barroca, L.M., McDermid, J.A.: Formal methods: use and rele-
Conflict of interest The authors declare that they have no conflict of          vance for the development of safety-critical systems. Comp. J. 35,
interest.                                                                       579–99 (1992)
                                                                            20. McDermid, J. et al.: Staples, J., Hinchey, M.G., Liu, S. (eds.)
Open Access This article is licensed under a Creative Commons                   In: Staples, J., Hinchey, M.G., Liu, S. (eds.) Towards Industrially
Attribution 4.0 International License, which permits use, sharing, adap-        Applicable Formal Methods: Three Small Steps, and One Giant
tation, distribution and reproduction in any medium or format, as               Leap. Formal Engineering Methods (ICFEM), 2nd International
long as you give appropriate credit to the original author(s) and the           Conference. IEEE (1998)
source, provide a link to the Creative Commons licence, and indi-           21. Parnas, D.L.: Really rethinking ‘formal methods’. Computer 43,
cate if changes were made. The images or other third party material             28–34 (2010)
in this article are included in the article’s Creative Commons licence,     22. Smith, B.C.: The limits of correctness. ACM SIGCAS Computers
unless indicated otherwise in a credit line to the material. If material        and Society 14(15), 18–26 (1985)
is not included in the article’s Creative Commons licence and your          23. Abrial, J.-R. Osterweil, L.J., Rombach, D., Soff, M.L. (eds.):
intended use is not permitted by statutory regulation or exceeds the            Formal methods in industry: achievements, problems, future.
permitted use, you will need to obtain permission directly from the copy-       Osterweil, L.J., Rombach, D., Soff, M.L. (eds.) Software Engi-
right holder. To view a copy of this licence, visit http://creativecomm         neering (ICSE), 28th International Conference. ACM (2006)
ons.org/licenses/by/4.0/.                                                   24. Gleirscher, M., Foster, S., Woodcock, J.: New opportunities for
                                                                                integrated formal methods. ACM Comput. Surv. 52, 117:1-117:36
References                                                                      (2019)
                                                                            25. Ferrari, A., ter Beek, M.H.: Formal methods in railways: a system-
 1. Huth, M., Ryan, M.: Logic in Computer Science: Modelling and                atic mapping study. ACM Comput. Surv. 55, 1–37 (2022)
    Reasoning about Systems. Cambridge University Press (2004)              26. Hoare, C.: The emperor’s old clothes. The 1980 ACM turing award
 2. Aichernig, B.K., Maibaum, T. (eds.). Formal Methods at the Cross-           lecture. Commun. ACM. 24, 75–83 (1981)
    roads. From Panacea to Foundational Support, LNCS, vol. 2757.           27. Gleirscher, M., Sachtleben, R., Peleska, J.: Qualification of proof
    Springer (2003)                                                             assistants, checkers, and generators: where are we and what next?
 3. Gnesi, S., Margaria, T.: Formal Methods for Industrial Critical Sys-        Sci. Comput. Program. 226, 102930 (2023)
    tems: A Survey of Applications. Wiley-IEEE Press (2013)                 28. Bourque, P., Fairley, R.E.: Guide to the Software Engineering Body
 4. Boulanger, J.-L.: Industrial Use of Formal Methods: Formal Veri-            of Knowledge (SWEBOK Guide). IEEE Computer Society (2014).
    fication. Wiley-ISTE (2012)                                                 http://www.swebok.org
 5. Miller, S.P., Whalen, M.W., Cofer, D.D.: Software model checking        29. Baudin, P., et al.: The dogged pursuit of bug-free C programs.
    takes off. Commun. ACM 53, 58–64 (2010)                                     Commun. ACM 64, 56–68 (2021)
 6. O’Hearn, P. W.: Continuous reasoning. In: Staton, S. (ed.) Logic        30. Rushby, J.: Critical system properties: survey and taxonomy.
    in Computer Science (LICS), Proceedings of the 33rd Annual                  Reliab. Eng. Syst. Safe. 43, 189–219 (1994)
    ACM/IEEE Symposium, pp. 13–25. ACM Press (2018)                         31. Baier, C., Katoen, J.: Principles of Model Checking. MIT Press
 7. Sobel, A., Clarkson, M.: Formal methods application: an empirical           (2008)
    tale of software development. IEEE Trans. Softw. Eng. 28, 308–320       32. Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R. (eds.): Hand-
    (2002)                                                                      book of Model Checking. Springer (2018)
 8. Pfleeger, S.L., Hatton, L.: Investigating the influence of formal       33. Bertot, Y., Castéran, P.: Texts in theoretical computer science.
    methods. Computer 30, 33–43 (1997)                                          In: Interactive Theorem Proving and Program Development—
 9. Garlan, D.: Formal methods for software engineers: tradeoffs in             Coq’Art: The Calculus of Inductive Constructions. An EATCS
    curriculum design. In: Sledge, C. (ed.) Software Engineering Edu-           Series. Springer (2004)
    cation, pp. 131–142. Springer, Berlin Heidelberg (1992)                 34. Paulson, L.C., Nipkow, T., Wenzel, M.: From LCF to Isabelle/HOL.
10. Behrmann, G., David, A., Larsen, K.G., Bernardo, M., Corradini,             Form. Asp. Comput. 31, 675–698 (2019)
    F.: A tutorial on UPPAAL. In: Bernardo, M., Corradini, F. (eds.)        35. Owre, S., Rushby, J.M., Shankar, N. Kapur, D.: (ed.) PVS: a proto-
    SFM. LNCS, vol. 3185, pp. 200–236. Springer, Berlin, Heidelberg             type verification system. In: Kapur, D. (ed.) Automated Deduction
    (2004)


                                                                                                                                       123
1748                                                                                                                                  M. Gleirscher et al.


    (CADE), LNCS, 11th International Conference, vol. 607, pp. 748–            56. Huber, F., Schätz, B., Schmidt, A., Spies, K.: AutoFOCUS—a
    752. Springer (1992)                                                           tool for distributed systems specification. In: Jonsson, B., Parrow,
36. Cousot, P., Cousot, R. Graham, R.M., Harrison, M.A. (eds.):                    J. (eds.) Formal Techniques in Real-Time and Fault-Tolerant Sys-
    Abstract interpretation: a unified lattice model for static analysis of        tems (FTRTFT), LNCS, vol. 1135, pp. 467–470. Springer, Berlin,
    programs by construction or approximation of fixpoints. In: Gra-               Heidelberg (1996)
    ham, R.M., Harrison, M.A. (eds.) POPL, pp. 238–52. ACM, Los                57. Broy, M.: A logical basis for component-oriented software and
    Angeles, California (1977)                                                     systems engineering. Comput. J. 53, 1758–82 (2010)
37. Andersen, L.O.: Program analysis and specialization for the C              58. Margaria, T., Nagel, R., Steffen, B. Rozenblit, J., O’Neill, T., Peng,
    programming language. Ph.D. thesis, University of Copenhagen                   J. (eds.): Remote integration and coordination of verification tools
    (1994)                                                                         in JETI. In: Rozenblit, J., O’Neill, T., Peng, J. (eds.) Engineer-
38. Andreasen, E.S., Møller, A., Nielsen, B.B. Ali, K., Cifuentes, C.              ing of Computer-Based Systems (ECBS), 12th IEEE International
    (eds.): Systematic approaches for increasing soundness and preci-              Conference, pp. 431–436. IEEE, Greenbelt, MD, USA (2005)
    sion of static analyzers. Ali, K., Cifuentes, C. (eds.) State of the Art   59. Owre, S., Rajan, S., Rushby, J.M., Shankar, N., Srivas, M.K. Alur,
    in Program Analysis (SOAP), 6th ACM SIGPLAN International                      R., Henzinger, T.A. (eds.): PVS: combining specification, proof
    Workshop, pp. 31–36. ACM, Barcelona, Spain (2017)                              checking, and model checking. In: Alur R, Henzinger, T.A. (eds).
39. Leino, K.R.M. Notkin, D., Cheng, B.H.C., Pohl, K. (eds.): Devel-               Computer Aided Verification (CAV), 8th International Conference,
    oping verified programs with Dafny. Notkin, D., Cheng, B.H.C.,                 LNCS, vol. 1102, pp. 411–414. Springer, New Brunswick, NJ, USA
    Pohl, K. (eds.) Software Engineering (ICSE), 35th International                (1996)
    Conference, pp. 1488–1490. IEEE (2013)                                     60. Lamport, L.: Specifying Systems, The TLA+ Language and Tools
40. Ahrendt, W. et al. (ed.): Deductive Software Verification—The                  for Hardware and Software Engineers. Addison-Wesley (2002)
    KeY Book—From Theory to Practice, vol. 10001, Lecture Notes                61. Baudin, P., et al.: The dogged pursuit of bug-free C programs:
    in Computer Science. Springer (2016)                                           the frama-c software analysis platform. Commun. ACM 64, 56–68
41. Blom, S., Darabi, S., Huisman, M.: Oortwijn, W. Polikarpova, N.,               (2021)
    Schneider, S.A. (eds.): The VerCors tool set: verification of parallel     62. McCormick, J.W., Chapin, P.C.: Building High Integrity Applica-
    and concurrent software. Polikarpova, N., Schneider, S.A. (eds.)               tions with SPARK. Cambridge University Press (2015)
    Integrated Formal Methods (iFM), 13th International Conference,            63. Müller, P., Schwerhoff, M., Summers, A.J., Jobstmann, B., Leino,
    LNCS, vol. 10510, pp. 102–110. Springer, Turin, Italy (2017)                   K.R.M. (eds.): Viper: a verification infrastructure for permission-
42. Meyer, B.: Applying ‘design by contract’. Computer 25, 40–51                   based reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Verifi-
    (1992)                                                                         cation, Model Checking, and Abstract Interpretation (VMCAI),
43. ISO/IEC 13568. Information technology—Z formal specification                   LNCS, vol. 9583, pp. 41–62. Springer (2016)
    notation—syntax, type system and semantics. Technical Report, Z            64. Burch, J.R., Clarke, E.M., McMillan, K.L., Dill, D.L., Hwang, L.J.:
    Standards Panel and ISO/IEC JTC 1/SC 22 (2002). https://www.                   Symbolic model checking: 1020 states and beyond. Inform. Com-
    iso.org/standard/21573.html                                                    put. 98, 142–170 (1992)
44. Hall, A., Chapman, R.: Correctness by construction. IEEE Softw.            65. Henzinger, T.A., Nicollin, X., Sifakis, J., Yovine, S.: Symbolic
    19, 18–25 (2002)                                                               model checking for real-time systems. Inform. Comput. 111, 193–
45. Broy, M., Rumpe, B.: Development use cases for semantics-driven                244 (1994)
    modeling languages. Commun. ACM 66, 62–71 (2023)                           66. Harel, D.: Statecharts: a visual formalism for complex systems.
46. Ladkin, P.B.: A critical-system assurance manifesto: issues arising            Sci. Comput. Program. 8, 231–74 (1987)
    from IEC 61508. Technical Report, Faculty of Technology, Biele-            67. Harrison, J., Kolaitis, P.G. (ed.). Formal verification at Intel. In:
    feld University (2018). https://rvs-bi.de/publications/RVS-Bk-17-              Kolaitis, P.G. (ed.) Logic in Computer Science (LICS), 18th IEEE
    01.html                                                                        Symposium, 45. IEEE (2003)
47. Rae, A., Provan, D., Aboelssaad, H., Alexander, R.: A manifesto            68. Fix, L. Grumberg, O., Veith, H.: (eds) Fifteen years of formal prop-
    for reality-based safety science. Saf. Sci. 126, 104654 (2020)                 erty verification in Intel. (eds Grumberg, O. & Veith, H.) 25 Years
48. Becker, C. et al.: In: Daoudagh, S., Lonetti, F. (eds.) Sustainability         of Model Checking, Vol. 5000 of LNCS, 139–144 (Springer, 2008)
    Design and Software: The Karlskrona Manifesto. Software Engi-              69. Ben-David, S., Eisner, C., Geist, D., Wolfsthal, Y.: Model checking
    neering (ICSE), 37th IEEE International Conference. IEEE/ACM                   at IBM. Form. Methods Syst. Des. 22, 101–108 (2003)
    (2015)                                                                     70. Rager, D.L. et al.: Piskac, R., Talupur, M.: Formal verification of
49. van der Aalst, W. et al.: Process mining manifesto. In: Daniel,                division and square root implementations, an Oracle report. In:
    F., Barkaoui, K., Dustdar, S. (eds.) Business Process Management               Piskac, R., Talupur, M. (eds.) Formal Methods in Computer-Aided
    Workshops, pp. 169–194. Springer, Berlin Heidelberg (2012)                     Design (FMCAD), pp. 149–152 (2016)
50. Hoare, T., Misra, J., Leavens, G.T., Shankar, N.: The verified soft-       71. ISO 8807. Information processing systems - open systems
    ware initiative: a manifesto. ACM Comput. Surv. 41, 1–8 (2009)                 interconnection—LOTOS—a formal description technique based
51. Kapor, M.: A software design manifesto. Dr. Dobb’s J. 16, 62–67                on the temporal ordering of observational behaviour. Standard,
    (1991)                                                                         ISO/IEC JTC 1/SC 7 (1989). https://www.iso.org/standard/16258.
52. Collette, P., Jones, C.B.: Enhancing the tractability of                       html
    rely/guarantee specifications in the development of interfer-              72. ITU SDL Z.100. Specification and description language (SDL).
    ing operations. In: Plotkin, G., Stirling, C.P., Tofte, M., Milner,            Standard, ITU (2010). http://www.sdl-forum.org/
    R. (eds.) Proof, Language, and Interaction: Essays in Honour of            73. IEEE. IEEE standard for property specification language (PSL).
    Robin Milner, pp. 277–308. MIT Press (2000)                                    IEEE Std 1850-2010 (Revision of IEEE Std 1850-2005), pp. 1–
53. Davis, F.D.: Perceived usefulness, perceived ease of use, and user             182 (2010)
    acceptance of information technology. MIS Q. 13, 319–40 (1989)             74. Ball, T., Levin, V., Rajamani, S.K.: A decade of software model
54. Hoare, T., He, J.: Unifying Theories of Programming. Prentice Hall             checking with SLAM. Commun. ACM 54, 68–76 (2011)
    (1998)                                                                     75. Distefano, D., Fähndrich, M., Logozzo, F., O’Hearn, P.W.: Scaling
55. Eker, J., et al.: Taming heterogeneity: the Ptolemy approach. Proc.            static analyses at Facebook. Commun. ACM 62, 62–70 (2019)
    IEEE 91, 127–144 (2003)                                                    76. Newcombe, C., et al.: How Amazon web services uses formal meth-
                                                                                   ods. Commun. ACM 58, 66–73 (2015)


123
A manifesto for applicable formal methods                                                                                                       1749


77. Chong, N., et al.: Code-level model checking in the software devel-                                        Mario Gleirscher is a postdoc
    opment workflow at amazon web services. Softw. Pract. Exp. 51,                                             in Computer Science at the Uni-
    772–797 (2021)                                                                                             versity of Bremen, Germany. He
78. Leroy, X.: Formal verification of a realistic compiler. Commun.                                            received the PhD and MSc degrees
    ACM 52, 107–115 (2009)                                                                                     in Computer Science, with a minor
79. Heiser, G., Klein, G., Andronick, J.: seL4 in Australia: from                                              in Mathematics, from the Tech-
    research to real-world trustworthy systems. Commun. ACM 63,                                                nical University of Munich, Ger-
    72–75 (2020)                                                                                               many. He has a Foundation Degree
80. Fitzgerald, J., Larsen, P.G., Jones, C.B., Liu, Z., Woodcock, J.:                                          in production engineering and sev-
    Balancing insight and effort: the industrial uptake of formal meth-                                        eral years of practical experience
    ods. In: Jones, C.B., Liu, Z., Woodcock, J. (eds.) Formal Methods                                          as a consultant, method engineer,
    and Hybrid Real-Time Systems: Essays in Honor of Dines Bjørner                                             and software developer. His inter-
    and Chaochen Zhou on the Occasion of Their 70th Birthdays, pp.                                             ests are in process calculi, stochas-
    237–254. Springer, Berlin, Heidelberg (2007)                                                               tic reasoning, and controller syn-
81. Gorm Larsen, P., Fitzgerald, J., Wolff, S. Gruner, S., Rumpe, B.: Are                                      thesis. He was awarded a Fellow-
    formal methods ready for agility? A reality check. In: Gruner, S.,      ship at the University of York, UK, funded by the German Research
    Rumpe, B. (eds.) Formal Methods and Agile Methods (FM+AM),              Foundation (DFG) for his research.
    2nd International Workshop, pp. 13–25, Gesellschaft für Infor-
    matik e.V., Bonn (2010)
82. Hentschel, M., Hähnle, R., Bubel, R., Ábrahám, E., Huisman, M.:                                              Jaco van de Pol is a full
    Can formal methods improve the efficiency of code reviews?. In:                                              professor in Computer Science at
    Ábrahám, E. & Huisman, M. (eds.) Integrated Formal Methods—                                                  Aarhus University since 2018. He
    12th International Conference, IFM 2016, Reykjavik, Iceland, June                                            received his PhD from Utrecht
    1–5, 2016, Proceedings, Lecture Notes in Computer Science, vol.                                              University (1996) on termination
    9681, pp. 3–19. Springer (2016)                                                                              of higher-order rewriting. He held
83. Basili, V.R., Selby, R.W., Hutchens, D.H.: Experimentation in soft-                                          positions at CWI Amsterdam
    ware engineering. IEEE Trans. Softw. Eng. SE–12, 733–743 (1986)                                              (1999) and TU Eindhoven (2004)
84. Yin, R.K.: Case Study Research: Design and Methods, 5th edn.                                                 and became a full professor at
    Sage, Los Angeles (2013)                                                                                     the University of Twente (2007).
85. Shull, F., Singer, J., Sjøberg, D.I.K. (eds.): Guide to Advanced                                             His research interests are auto-
    Empirical Software Engineering. Springer (2008)                                                              mated       verification    (high-
86. Wohlin, C., et al.: Experimentation in Software Engineering.                                                 performance model checking algo-
    Springer, Berlin (2012)                                                                                      rithms) and automated synthesis
87. ter Beek, M.H., Ferrari, A.: Empirical formal methods: guidelines                                            (planning, winning strategies,
    for performing empirical studies on formal methods. Software 1,         parameter synthesis). He investigated applications of formal tech-
    381–416 (2022)                                                          niques in railway safety, security, distributed and embedded systems,
88. Ferrari, A., Mazzanti, F., Basile, D., ter Beek, M.H.: System-          biological networks, and quantum circuits.
    atic evaluation and usability analysis of formal methods tools for
    railway signaling system design. IEEE Trans. Softw. Eng. 48,                                                Jim Woodcock is a Professor of
    4675–4691 (2022)                                                                                            Software Engineering at the Uni-
89. Hähnle, R.: Software as research infrastructure. In: ETAPS Blog                                             versity of York, a Fellow of the
    (2023). https://etaps.org/blog/007-reiner-haehnle/                                                          Royal Academy of Engineering,
90. Choi, B.H.: Software professionals, malpractice law, and codes of                                           a consulting Chartered Engineer,
    ethics. Commun. ACM 64, 22–24 (2021)                                                                        and an award-winning researcher
91. Chien, A.A.: Computing is a profession. Commun. ACM 60, 5–5                                                 and teacher. He is the Director of
    (2017)                                                                                                      the York Centre for Autonomous
92. Gotterbarn, D., Miller, K., Rogerson, S.: Software engineering code                                         Robotics for Laboratory Exper-
    of ethics. Commun. ACM 40, 110–118 (1997)                                                                   iments and a member of the
93. Lichtenberger, F. Bollin, A., Margaria, T., Perseil, I. (eds.): Mak-                                        RoboStar research group. He is
    ing formal methods popular: The crux is math education!. In:                                                a Professor of Digital Twins at
    Bollin, A., Margaria, T., Perseil, I. (eds.) FMSEE&T, CEUR Work-                                            Aarhus University, a Professor of
    shop Proceedings, vol. 1385 (2015). http://ceur-ws.org/Vol-1385/                                            Cyber-Physical Systems, and a
    paper5.pdf                                                                                                  Distinguished Researcher at
94. Welsh, M.: The end of programming. Commun. ACM 66, 34–35                Southwest University, Chongqing. He has dedicated his career to
    (2022)                                                                  searching for the mathematical principles that are essential to the prac-
95. Meyer, B.: AI does not help programmers. BLOG@CACM                      tice of software engineering. For the last decade, he has researched
    (2023). https://cacm.acm.org/blogs/blog-cacm/273577-ai-does-            the theory and practice of cyber-physical systems, robotics, and, most
    not-help-programmers                                                    recently, their probabilistic semantics. He is Editor-in-Chief of the
96. Gleirscher, M., van de Pol, J., Woodcock, J. (eds.): Applicable For-    ACM journal Formal Aspects of Computing and of the CUP journal
    mal Methods (AppFM), 1st FM Workshop, EPTCS, vol. 349. Open             Research Directions: Cyber-Physical Systems.
    Publishing Association (2021). http://eptcs.web.cse.unsw.edu.au/
    content.cgi?AppFM2021. 2111.07538



Publisher’s Note Springer Nature remains neutral with regard to juris-
dictional claims in published maps and institutional affiliations.


                                                                                                                                        123
