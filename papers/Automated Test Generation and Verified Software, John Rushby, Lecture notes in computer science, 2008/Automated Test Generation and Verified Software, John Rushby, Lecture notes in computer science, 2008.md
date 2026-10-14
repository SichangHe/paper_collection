                   Automated Test Generation
                     and Veriﬁed Software

                                      John Rushby

                              Computer Science Laboratory
                                   SRI International
                                333 Ravenswood Avenue
                               Menlo Park, CA 94025 USA



        Abstract. Testing remains the principal means of veriﬁcation in com-
        mercial practice and in many certiﬁcation regimes. Formal methods of
        veriﬁcation will coexist with testing and should be developed in ways
        that improve, supplement, and exploit the value of testing. I describe
        automated test generation, which uses technology from formal methods
        to mechanize the construction of test cases, and discuss some of the re-
        search challenges in this area.


1     Introduction

By testing I mean observation of a program in execution under controlled condi-
tions. Observations are compared against an explicit or informal oracle to detect
bugs or conﬁrm correctness. Much of the testing process (i.e., the execution
and monitoring of tests) is automated in modern development environments,
but construction of test cases (i.e., the speciﬁc experiments to be performed)
remains a largely manual process.
   Testing is the method by which most software is veriﬁed today. This is true
for safety critical software as well as the commodity variety: the highest level of
ﬂight critical software (DO-178B Level A) is required to be tested to a structural
code coverage criterion known as MC/DC (Modiﬁed Condition/Decision Cover-
age) [1]. And although formal methods of analysis and veriﬁcation are becoming
sanctioned, even desired, by some certiﬁcation regimes, testing continues to be
required also—because it can expose diﬀerent kinds of problems (e.g., compiler
bugs), can examine the program in its system context, and increases the diversity
of evidence available.
   The weakness of testing is well-known to the formal methods and veriﬁcation
communities—it can only show the presence of bugs—but those communities are
now beginning to recognize its strength: it can show the presence of bugs—often,
very eﬀectively. It is a great advantage in veriﬁcation if the software to be veriﬁed
is actually correct, so inexpensive methods for revealing incorrectness early in

    This work was partially supported by NASA Langley Research Center through con-
    tract NAS1-00079, and by NSF grant CNS-0644783.

B. Meyer and J. Woodcock (Eds.): Veriﬁed Software, LNCS 4171, pp. 161–172, 2008.

c IFIP International Federation for Information Processing 2008
162     J. Rushby

the development and veriﬁcation process are necessary for veriﬁed software to
be economically viable.
   Thus, testing is not a rival to formal methods of veriﬁcation but a valuable
and complementary adjunct. It is worthwhile to study how each can support the
other, both in the technology that they employ, and in their contribution to the
overall goal of cost-eﬀective veriﬁcation.
   In this regard, the most signiﬁcant recent development in testing has been the
application of technologies from veriﬁcation (notably, model-checking, SAT and
SMT solving, and constraint satisfaction) to automate the generation of test
cases. Automated test generation poses urgent challenges and opportunities:
there are many technical challenges in achieving eﬀective automation, there is
a wealth of opportunity in the diﬀerent ways that automated testing can be
used, and there are serious implications for traditional certiﬁcation regimes—
and opportunities for innovative ones; there are also opportunities for theoretical
research in the relationship between testing and veriﬁcation, and for empirical
inquiry into their pragmatic combination.
   In this paper, I brieﬂy survey the topics mentioned above, and suggest re-
search directions for the development and use of automated test generation in
veriﬁcation.

2     Technology for Automated Test Generation
Much of the process of test execution and monitoring is automated in modern
software development practice. But the generation of test cases has remained
a labor-intensive manual task. Methods are now becoming available that can
automate this process.
   A simple test-generation goal is to ﬁnd an input that will drive execution of
a (deterministic, loop-free) program along a particular path in its control ﬂow
graph. By performing symbolic execution along the desired path and conjoining
the predicates that guard its branch points, we can calculate the condition that
the desired test input must satisfy. Then, by constraint satisfaction, we can ﬁnd a
speciﬁc input that provides the desired test case. This method generalizes to ﬁnd
tests for structural coverage criteria such as statement or branch coverage, and
for programs with loops and those that are reactive systems (i.e., that take an
input at each step). A major impetus for practical application of this approach
was the realization that (for ﬁnite state systems) it can be performed by an oﬀ-
the-shelf model checker: we simply check the property “always not P ,” where P is
a formula that speciﬁes the desired structural criterion, and the counterexample
produced by the model checker is then the test case desired [2]. Diﬀerent kinds of
structural or speciﬁcation-based tests can be generated by choosing suitable P .
   Using a model checker to generate tests in this way can be very straightfor-
ward in model-based development, where we have an executable speciﬁcation
for the program that is in, or is easily translated to, the language of a model
checker: the tests are generated from the executable speciﬁcation, which then
provides the oracle when these are applied to the generated program. There are
many pragmatic issues in the selection of explicit-state, symbolic, or bounded
                          Automated Test Generation and Veriﬁed Software         163

model checkers for this task [3] and it is, of course, possible to construct special-
ized test generators that use the technology of model checking but customize it
appropriately for this application.
   The test generation task becomes more challenging when tests are to be gen-
erated directly from a low-level program description, such as C code, when the
path required is very long (e.g., when it is necessary to exhaust a loop counter),
when the program is not ﬁnite state, and when nondeterminism is present.
   When a higher-level speciﬁcation is unavailable and tests must be generated
directly from C code or similar low-level description, it is natural to adopt
techniques from software model checking. These seldom translate the program
directly into the language of a model checker but usually ﬁrst abstract it in
some way. Predicate abstraction [4] is the most common approach, and discov-
ery of suitable predicates is automated very eﬀectively in the lazy-abstraction
approach [5]. Abstractions for test generation are not necessarily the same as
those used for veriﬁcation. For the latter, the abstraction needs to be conserva-
tive (i.e., it should have more behaviors than the concrete program), whereas in
the former case we generally desire that any test generated from the abstrac-
tion should be feasible in the concrete program (i.e., the abstraction may have
fewer behaviors than the concrete program) [6]. This impacts the method for
constructing the abstraction, and the choice of theorem proving or constraint
satisfaction methods employed [7].
   When very long test sequences are needed to reach a desired test target, it is
sometimes possible to generate them using specialized model checking methods
(e.g., those based on an ATPG engine [8]), or by generating the test incremen-
tally, so that each subproblem is within reach of the model checker [3]. Some
of the most eﬀective current approaches for generating long test sequences use
combinations of methods. For example, random test generation rapidly produces
many long paths through the program; to reach an uncovered test target, we ﬁnd
a location “nearby” (e.g., measured by Hamming distance on the state variables)
that has been reached by random testing and then use model checking or con-
straint satisfaction to extend the path from that nearby location to the one
desired [9]. DART [10] uses a diﬀerent approach to explore all feasible execution
paths: the program under test is ﬁrst executed on some random input and mon-
itored to gather constraints on inputs at conditional branches during that run;
then a constraint solver is used to generate variants on the inputs to steer the
next execution of the program towards diﬀerent execution paths.
   Traditional model checking technology must be extended or adapted when
the program is not ﬁnite state. In some cases, an inﬁnite state bounded model
checker can be used (i.e., a bounded model checker that uses a decision procedure
for satisﬁability modulo theories (SMT) [11] rather than a Boolean SAT solver)
[12]. An SMT solver can, for example, generate real-valued inputs that can be
interpreted as delays to be used in testing a real-time program.
   In cases where inputs to the program are not simple numerical quantities
but data types such as trees or lists, a plausible approach is to ﬁx the base
type (e.g., elements of the tree are chosen from an alphabet of size 2), bound
164     J. Rushby

the size of the data type (e.g., trees with no more than 5 nodes), and then
generate all or many instances of the data type within those constraints. This is
easily automated when an axiomatic speciﬁcation for the data type is available
(e.g., rewrite rules specifying a tree), but straightforward approaches produce
highly redundant tests (i.e., they generate many inputs that are structurally
“isomorphic” to each other). Gaudel and her colleagues have developed methods
for generating tests in this way while reducing redundancy using “regularity”
and “uniformity” hypotheses [13, 14].
   A variant is where we lack a generator for the data type but have a recognizer
for it: for example, we may have a predicate that recognizes red-black trees
represented as linked lists. Here, we could randomly or exhaustively generate all
inputs up to some speciﬁed size and test them against the recognizing predicate,
but this is very ineﬃcient (e.g., very few randomly generated list structures
represent a valid red-black tree) and also generates many “isomorphs.” Hence,
it is best to view the search as a constraint satisfaction problem and to use
technology from that domain [15].
   The test generation problem changes signiﬁcantly when the program under
test is nondeterministic, or when part of the testing environment is not under
the control of the tester (e.g., testing an embedded system in its operational
environment). In these cases, we cannot generate test sequences independently
of their actual execution: it is necessary to observe the behavior of the system
in response to the test generated so far and to generate the next input in a way
that advances the purpose of the test (and to recognize when this cannot be
achieved and the current test should be abandoned). This kind of testing can
be seen as a game between the tester and the system under test: rather than
passive test cases (i.e., data) we need an active tester (i.e., a program), and test
generation becomes a problem of controller synthesis. Methods for solving this
problem can use technology similar to model checking but can seldom use an
oﬀ-the-shelf model checker [16]; SpecExplorer is a tool of this kind [17].
   The problem becomes yet more diﬃcult when the test environment includes
mechanical or biological systems: for example, testing the shift controller of an
automatic gearbox in its full system context with a (real or simulated) gearbox
attached, or testing a pacemaker against a simulated heart. Here, the test gen-
eration problem is escalated to one of controller synthesis in a hybrid system
(i.e., one whose description includes diﬀerential equations). This is a challenging
problem, but a plausible approach is to replace the hybrid elements of the mod-
eled environment by conservative discrete approximations, and then use methods
for test generation in nondeterministic systems [18]. As in the case of predicate
abstraction, the notion of “conservative” that is suitable for test generation may
diﬀer from that used in veriﬁcation.


3     Selection of Test Targets
The previous section has sketched how test cases can be generated automati-
cally; the next problem is to determine how to make good use of this capability.
                            Automated Test Generation and Veriﬁed Software         165

One approach uses test generation to help developers explore their emerging de-
signs [19]: a designer might say “show me a run that puts control at this point
with x ≤ 0.” This approach is very well-suited to model-based design environ-
ments (i.e., those where the design is executable), but is less so for traditional
programming. An approach that has proven useful in traditional programming
is random test generation at the unit level. In some programming environments,
each unit is automatically subjected to random testing against desired proper-
ties if these have been speciﬁed, or generic ones (e.g., no exceptions) as it is
checked in (Haskell QuickCheck [20] is the progenitor of this approach). A simi-
lar approach can be used in theorem proving environments: before attempting to
prove a putative theorem, ﬁrst try to refute it by random test generation [21] (in
PVS, this can also be tried during an interactive proof if the current proof goal
looks intractable [22]). These simple approaches are highly eﬀective in practice.
More challenging tests can be achieved by exhaustive generation of inputs up
to some bounded size [23]. In Extreme Programming, tests take on much of the
rôle played by speciﬁcations in more traditional development methods [24], and
automated, incremental test generation can support this approach [25].
    More traditional uses of testing are for systematic debugging, and for valida-
tion and veriﬁcation. In tests developed by humans, the ﬁrst of these is generally
driven by some explicit or implicit hypotheses about likely kinds of bugs, while
the others are driven by systematic “coverage” of requirements and code.
    One simple fault hypothesis is that errors are often made at the boundaries of
conditions (e.g., the substitution of < for ≤) and some automated test generators
target these cases [26]. Another hypothesis is that compound decisions (e.g.,
A∧B ∨C) may be constructed incorrectly so tests should target the “meaningful
impact” [27] of each condition within the decision (i.e., each must be shown able
to independently aﬀect the outcome).1 It turns out that these ideas are related:
boundary testing for x ≤ y is equivalent to rewriting the decision as x < y∨x = y
and then testing for meaningful impact of the two conditions. The classes of faults
detected by popular test criteria for compound decisions have been analyzed by
Kuhn [28] and extended by others [29, 30].
    Requirements- or speciﬁcation-based testing is most easily automated when
the requirements or speciﬁcation are provided in executable form—as is com-
monly done in model based development, thereby giving rise to model-based
testing [31]. Here, we can use the methods sketched in Section 2 to generate
tests that systematically explore the speciﬁed behavior. The usual idea is that a
good set of tests should thoroughly explore the control structure of the speciﬁca-
tion; typical criteria for such structural coverage are to reach every control state,
to take every transition between control states, and more elaborate variants that
explore the conditions within the decisions that control selection of transitions
(as in the meaningful impact criteria mentioned earlier). Structural coverage cri-
teria can be augmented by “test purposes” [32] that describe the kind of tests
we want to generate (e.g., those in which the gear input to a gearbox shift se-

1
    This use of decision and condition is the one employed in MC/DC, which is a testing
    criterion of this kind.
166     J. Rushby

lector changes at each step, but only to an adjacent value), by predicates that
describe relationships that should be explored (e.g., a queue is empty, full, or in
between) [33], or by speciﬁcations that describe the external environment [34].
Test purposes and predicates are related to predicate abstraction and can be
used to reduce the statespace of the model, and thereby ease the model checking
task underlying the test generation. Generating a separate test for each cover-
age target produces ineﬃcient test sets that contain many short tests and much
redundancy, so recent methods attempt to construct more eﬃcient “tours” that
visit many targets in each test [35, 3, 33].
   Requirements-based testing is more diﬃcult when requirements are speciﬁed
by properties rather than models. One approach is to translate the properties
into automata (i.e., synchronous observers), then target structural coverage in
the automata. Alternatively, a direct approach is described in [36].

4     Testing for Veriﬁcation
Certiﬁcation regimes for which testing is an important component generally
require evidence that the testing has been thorough. DO-178B Level A (which
applies to the highest level of ﬂight-critical software in civil aircraft) is typical:
it requires MC/DC code coverage. The expectation is that tests are generated
by consideration of requirements and their execution is monitored to measure
coverage of the code. As the industry moves toward model-based development,
it can be argued that the requirements are represented by the models, and hence
that automated test generation from the model is a form of requirements-based
testing. One way to do this is by targeting MC/DC coverage in the model.
Heimdahl, George, and Weber did this for a model of a ﬂight guidance system
developed by Rockwell, and then executed the tests on implementations that had
been seeded with errors [37]. They found that the autogenerated tests detected
relatively few bugs, and generally performed worse than random testing. Part
of the explanation for this distressing observation is that the model checking
technology underpinning the test generation is “too clever”: it generally ﬁnds
the shortest test to discharge any given goal, and these short tests often exploit
some special case and never reach the interesting parts of the state space. There
is hope that methods that generate tours through many test goals will do better
than those that target the goals individually, or that suitable test purposes may
guide the test generator into more productive areas of the state space, but these
ideas need to be validated in practice.
   Another way in which testing has been employed for veriﬁcation is in “confor-
mance testing,” which is generally applied to distributed systems and protocols
(where the tester must be an active program). Given a formal speciﬁcation and
an implementation that purports to satisfy it, conformance testing generates
a series of tests such that any departure from the speciﬁcation will eventually
be revealed (subject to various technical caveats) [38]. Only a relatively small
number of tests can be performed in practice, so the eventuality guarantee is of
mainly theoretical interest, and the more pragmatic concern is to try and arrange
things so that tests generated early in the series are eﬀective at ﬁnding bugs.
                             Automated Test Generation and Veriﬁed Software            167

   Until recently, there has been relatively little work that uses automated testing
and static analysis or formal veriﬁcation in combination. One idea is to reduce
“false alarms” in static analysis by emitting only those errors for which a test
case to manifest it can be constructed. Dually, some static analysis methods
(such as slicing) can be used to ease the test generation task [39]. Rusu uses test
generation to decompose the classical formal veriﬁcation problem into smaller
components [40], while the Synergy method [41] alternates DART-like testing
and formal veriﬁcation to achieve highly automated property checking.


5     Research Challenges
Testing is the dominant means of veriﬁcation used today. Any research agenda
in software veriﬁcation must include testing as a topic, and its roadmap must
suggest how the proposed research will improve testing, and how it can use it,
as well as how it may replace it in selected areas.
   Automated test generation is an attractive topic in this area: it can reduce
the cost of testing and may improve its quality. And it is an “invisible” appli-
cation of formal methods and thus provides a good opportunity to introduce
this technology to new communities. Among the most eager adopters of this
capability are those in regulated industries where onerous testing requirements
constitute a signiﬁcant part of overall development costs.2 As mentioned above,
there is some evidence that simply using the test coverage requirements as a
target for automated test generation may be a ﬂawed strategy: coverage metrics
are intended to measure the thoroughness of human-generated tests, and do not
necessarily lead to good test sets when used in an inverted role as a speciﬁcation
for the tests required.
   Thus, an urgent research topic is development of techniques for specifying
good test sets. There are two subtopics here: the role of the human tester will
change from construction of tests to speciﬁcation of tests (the tests will be gen-
erated automatically from the speciﬁcation), so we need ideas and techniques
for specifying tests (e.g., an extended notion of test purpose); second, we need
empirical data on what kinds of test speciﬁcation produce good tests (i.e., those
that are eﬀective in revealing errors). It is natural to assume that speciﬁcations
for tests should directly correspond to a method for generating the tests, but
modern automated test generation operates by constraint satisfaction (either ex-
plicitly, or implicitly via model checking) and this opens up the possibility that
tests can be speciﬁed indirectly in terms of recognizers. Concretely, we can spec-
ify tests indirectly by means of synchronous observers that “recognize a good
test when they see one” and raise a ﬂag to indicate it. Then we use a model
checker to ﬁnd circumstances that raise the ﬂag. This use of recognizers creates
many attractive possibilities for test speciﬁcation [43].
   Most current methods and tools for automated test generation are limited
to unit tests. A second general research area is development of methods and
2
    Alternatively, there has been some industrial use of formal veriﬁcation as a lower-cost
    replacement for MC/DC testing [42].
168     J. Rushby

technology for other (arguably more important) testing tasks, such as integra-
tion and system tests. At these levels, tests become interactive programs, and
the formal context becomes that of controller synthesis for nondeterministic,
timed, and hybrid systems. Abstraction is likely to be necessary, both for the
system under test and for its environment, and there are interesting questions
regarding the appropriate kinds of abstractions to use, and the theorem prov-
ing and model checking methods that are most suitable for constructing and
using them. Integration testing need not be restricted to the later stages of de-
velopment: much of requirements engineering is concerned with anticipation of
interactions among components, and the earlier and more completely these can
be understood the better. Model checking and automated integration testing
during development of (model-based) requirements could reduce the well-known
“explosion” of problems that traditionally arise at system integration time.
   A third suggested general research area is the integration of testing with for-
mal methods of analysis and veriﬁcation. Again, there are two subtopics: one is
technical integration—for example, how can testing help in formal speciﬁcation
and proof (cf. QuickCheck-like methods for rapid refutation)—while the other
focuses on how the overall veriﬁcation process can be decomposed into elements
that are eﬀectively tackled by diﬀerent means. For example, formal veriﬁcation
not only provides guarantees, it exposes assumptions—and these assumptions
can be useful targets for testing. Penetration testing for security at the highest
“evaluation assurance levels” uses exactly this approach. Here, the relationship
between formal veriﬁcation and testing is clear, but in other contexts it can
be less so. There are proposals, for example, to replace some unit test require-
ments in avionics by static analysis; yet testing can address some issues (such
as compiler bugs, which are a genuine problem) that static analysis does not
(unless applied to machine code), so the overall web of argument in support of
veriﬁcation may become interestingly complex.
   A companion paper in these proceedings outlines some of the issues in techni-
cal integration of veriﬁcation components [44], while the larger issues of “multi-
legged assurance,” in which the assurance case for a system is composed from
diﬀerent kinds of evidence, is only just beginning to receive attention [45, 46, 47]
and is a worthy topic for future study.

References
 1. Hayhurst, K.J., Veerhusen, D.S., Chilenski, J.J., Rierson, L.K.: A practical
    tutorial on modiﬁed condition/decision coverage. NASA Technical Memorandum
    TM-2001-210876, NASA Langley Research Center, Hampton, VA (2001),
    http://www.faa.gov/certification/aircraft/av-info/software/Research/
    MCDC%20Tutorial.pdf
 2. Gargantini, A., Heitmeyer, C.: Using model checking to generate tests from re-
    quirements speciﬁcations. In: Nierstrasz, O., Lemoine, M. (eds.) ESEC 1999 and
    ESEC-FSE 1999. LNCS, vol. 1687, pp. 146–162. Springer, Heidelberg (1999)
 3. Hamon, G., de Moura, L., Rushby, J.: Generating eﬃcient test sets with a model
    checker. In: 2nd International Conference on Software Engineering and Formal
    Methods (SEFM), pp. 261–270. IEEE Computer Society, Beijing (2004)
                            Automated Test Generation and Veriﬁed Software           169

 4. Saı̈di, H., Graf, S.: Construction of abstract state graphs with PVS. In: Grumberg,
    O. (ed.) CAV 1997. LNCS, vol. 1254, pp. 72–83. Springer, Heidelberg (1997)
 5. Henzinger, T.A., Jhala, R., Majumdar, R., Sutre, G.: Software veriﬁcation with
    BLAST. In: Ball, T., Rajamani, S.K. (eds.) SPIN 2003. LNCS, vol. 2648, pp. 235–
    239. Springer, Heidelberg (2003)
 6. Ball, T., Kupferman, O., Yorsh, G.: Abstraction for falsiﬁcation. In: [48], pp. 67–81
 7. Xia, S., Di Vito, B., Muñoz, C.: Predicate abstraction of programs with non-linear
    computation. In: Graf, S., Zhang, W. (eds.) ATVA 2006. LNCS, vol. 4218, pp.
    352–368. Springer, Heidelberg (2006)
 8. Boppana, V., Rajan, S.P., Takayama, K., Fujita, M.: Model checking based on
    sequential ATPG. In: [49], pp. 418–430
 9. Ho, P.H., Shiple, T., Harer, K., Kukula, J., Damiano, R., Bertacco, V., Taylor,
    J., Long, J.: Smart simulation using collaborative formal simulation engines. In:
    International Conference on Computer Aided Design (ICCAD), Jan Jose, CA,
    Association for Computing Machinery, pp. 120–126 (2000)
10. Godefroid, P., Klarlund, N., Sen, K.: DART: Directed automated random test-
    ing. In: Conference on Programming Language Design and Implementation: PLDI,
    Chicago, IL. Association for Computing Machinery, pp. 213–223 (2005)
11. Barrett, C., de Moura, L., Stump, A.: SMT-COMP: Satisﬁability modulo theories
    competition. In: [48], pp. 20–23.
12. de Moura, L., Rueß, H., Sorea, M.: Lazy theorem proving for bounded model
    checking over inﬁnite domains. In: Voronkov, A. (ed.) CADE 2002. LNCS (LNAI),
    vol. 2392, pp. 438–455. Springer, Heidelberg (2002)
13. Bernot, G., Gaudel, M.C., Marre, B.: Software testing based on formal speciﬁca-
    tions: A theory and a tool. IEE/BCS Software Engineering Journal 6, 387–405
    (1991)
14. Gaudel, M.C.: Testing from formal speciﬁcations, a generic approach. In:
    Strohmeier, A., Craeynest, D. (eds.) Ada-Europe 2001. LNCS, vol. 2043, pp. 35–48.
    Springer, Heidelberg (2001)
15. Boyapati, C., Khurshid, S., Marinov, D.: Korat: Automated testing based on Java
    predicates. In: International Symposium on Software Testing and Analysis (IS-
    STA), Rome, Italy. Association for Computing Machinery, pp. 123–122 (2002)
16. Jéron, T., Morel, P.: Test generation derived from model-checking. In: [49], pp.
    108–121
17. Veanes, M., Campbell, C., Schulte, W., Tillmann, N.: Online testing with model
    programs. In: Proceedings of the 13th Annual Symposium on Foundations of Soft-
    ware Engineering (FSE), Lisbon, Portugal. Association for Computing Machinery,
    pp. 273–282 (2005)
18. Tiwari, A.: Abstractions for hybrid systems. In: Formal Methods in Systems Design
    (to appear, 2007), http://www.csl.sri.com/∼ tiwari/new.pdf
19. Ben-David, S., Gringauze, A., Sterin, B., Wolfsthal, Y.: PathFinder: A tool for de-
    sign exploration. In: Brinksma, E., Larsen, K.G. (eds.) CAV 2002. LNCS, vol. 2404,
    pp. 510–514. Springer, Heidelberg (2002)
20. Claessen, K., Hughes, J.: QuickCheck: a lightweight tool for random testing of
    Haskell programs. In: International Conference on Functional Programming, Mon-
    treal, Canada. Association for Computing Machinery, pp. 268–279 (2000)
21. Berghofer, S., Nipkow, T.: Random testing in Isabelle/HOL. In: 2nd International
    Conference on Software Engineering and Formal Methods, Beijing, China, pp. 230–
    239. IEEE Computer Society, Los Alamitos (2004)
22. Owre, S.: Random testing in PVS. In: Workshop on Automated Formal Methods
    (AFM), Seattle, WA (2006), http://fm.csl.sri.com/AFM06/papers/5-Owre.pdf
170     J. Rushby

23. Sullivan, K., Yang, J., Coppit, D., Khurshid, S., Jackson, D.: Software assurance
    by bounded exhaustive testing. In: International Symposium on Software Testing
    and Analysis (ISSTA), Boston, MA. Association for Computing Machinery, pp.
    133–142 (2004)
24. Beck, K.: Test Driven Development: By Example. Addison-Wesley, Reading (2002)
25. Henzinger, T.A., Jhala, R., Majumdar, R., Sanvido, M.A.: Extreme model check-
    ing. In: Dershowitz, N. (ed.) Veriﬁcation: Theory and Practice. LNCS, vol. 2772,
    pp. 332–358. Springer, Heidelberg (2004)
26. Kosmatov, N., Legeard, B., Peureux, F., Utting, M.: Boundary coverage criteria
    for test generation from formal models. In: 15th International Symposium on Soft-
    ware Reliability Engineering (ISSRE 2004), Saint-Malo, France, pp. 139–150. IEEE
    Computer Society, Los Alamitos (2004)
27. Weyuker, E., Goradia, T., Singh, A.: Automatically generating test data from a
    Boolean speciﬁcation. IEEE Transactions on Software Engineering 20, 353–363
    (1994)
28. Kuhn, D.R.: Fault classes and error detection capability of speciﬁcation-based
    testing. ACM Transactions on Software Engineering and Methodology 8, 411–424
    (1999)
29. Tsuchiya, T., Kikuno, T.: On fault classes and error detection capability of
    speciﬁcation-based testing. ACM Transactions on Software Engineering and
    Methodology 11, 58–62 (2002)
30. Okun, V., Black, P.E., Yesha, Y.: Comparison of fault classes in speciﬁcation-based
    testing. Information and Software Technology 46, 525–533 (2004)
31. Utting, M., Legeard, B.: Practical Model-Based Testing. Morgan Kaufmann, San
    Francisco (2006)
32. Clarke, D., Jéron, T., Rusu, V., Zinovieva, E.: STG: a symbolic test generation
    tool. In: Katoen, J.-P., Stevens, P. (eds.) ETAPS 2002 and TACAS 2002. LNCS,
    vol. 2280, pp. 470–475. Springer, Heidelberg (2002)
33. Grieskamp, W., Gurevich, Y., Schulte, W., Veanes, M.: Generating ﬁnite state
    machines from abstract state machines. In: International Symposium on Software
    Testing and Analysis (ISSTA), Rome, Italy. Association for Computing Machinery,
    pp. 112–122 (2002)
34. du Bosquet, L., Ouabdesselam, F., Richier, J.L., Zuanon, N.: Lutess: A
    speciﬁcation-driven testing environment for synchronous software. In: 21st Interna-
    tional Conference on Software Engineering, pp. 267–276. IEEE Computer Society,
    Los Alamitos (1999)
35. Lee, D., Yannakakis, M.: Principles and methods of testing ﬁnite state machines.
    Proceedings of the IEEE 84, 1090–1123 (1996)
36. Whalen, M.W., Rajan, A., Heimdahl, M.P.E., Miller, S.P.: Coverage metrics for
    requirements-based testing. In: International Symposium on Software Testing and
    Analysis (ISSTA), Portland, ME. Association for Computing Machinery, pp. 25–36
    (2006)
37. Heimdahl, M.P., George, D., Weber, R.: Speciﬁcation test coverage adequacy crite-
    ria = speciﬁcation test generation Inadequacy criteria? In: High-Assurance Systems
    Engineering Symposium, Tampa, FL, pp. 178–186. IEEE Computer Society, Los
    Alamitos (2004)
38. Tretmans, J., Belinfante, A.: Automatic testing with formal methods. In: Eu-
    roSTAR 1999: 7th European Int. Conference on Software Testing, Analysis & Re-
    view. EuroStar Conferences, Barcelona, Spain, Galway, Ireland (1999)
                            Automated Test Generation and Veriﬁed Software           171

39. Bozga, M., Fernandez, J.C., Ghirvu, L.: Using static analysis to improve automatic
    test generatin. In: Schwartzbach, M.I., Graf, S. (eds.) ETAPS 2000 and TACAS
    2000. LNCS, vol. 1785, pp. 235–250. Springer, Heidelberg (2000)
40. Rusu, V.: Veriﬁcation using test generation techniques. In: Eriksson, L.-H., Lindsay,
    P.A. (eds.) FME 2002. LNCS, vol. 2391, pp. 252–271. Springer, Heidelberg (2002)
41. Gulavani, B.S., Henzinger, T.A., Kannan, Y., Nori, A.V., Rajamani, S.K.: Synergy:
    A new algorithm for property checking. In: Proceedings of the 14th Annual Sym-
    posium on Foundations of Software Engineering (FSE), Portland, OR. Association
    for Computing Machinery, pp. 117–127 (2006)
42. Duprat, S., Souyris, J., Favre-Felix, D.: Formal veriﬁcation workbench for Airbus
    avionics software. In: ERTS 2006: Embedded Real Time Software, Societe des
    Ingenieurs de l’Automobile (2006)
43. Hamon, G., de Moura, L., Rushby, J.: Automated test generation with SAL. Techni-
    cal note, Computer Science Laboratory, SRI International, Menlo Park, CA (2005),
    http://www.csl.sri.com/users/rushby/abstracts/sal-atg
44. de Moura, L., Owre, S., Rueß, H., Rushby, J., Shankar, N.: Integrating veriﬁcation
    components. In: These proceedings (2007)
45. Bloomﬁeld, R., Littlewood, B.: Multi-legged arguments: The impact of diversity
    upon conﬁdence in dependability arguments. In: The International Conference on
    Dependable Systems and Networks, pp. 25–34. IEEE Computer Society, San Fran-
    cisco (2003)
46. Littlewood, B., Wright, D.: The use of multi-legged arguments to increase conﬁ-
    dence in safety claims for software-based systems: a study based on a BBN analysis
    of an idealised example. IEEE Transactions on Software Engineering 33, 347–365
    (2007)
47. Rushby, J.: What use is veriﬁed software? In: 12th IEEE International Conference
    on the Engineering of Complex Computer Systems (ICECCS), Auckland, New
    Zealand, IEEE Computer Society, Los Alamitos (2007),
    http://www.csl.sri.com/∼ rushby/abstracts/iceccs07-vsi
48. Etessami, K., Rajamani, S.K. (eds.): CAV 2005. LNCS, vol. 3576. Springer, Hei-
    delberg (2005)
49. Halbwachs, N., Peled, D.A. (eds.): CAV 1999. LNCS, vol. 1633. Springer, Heidel-
    berg (1999)


A Discussion on John Rushby’s Presentation
Greg Nelson
John, I enjoyed your talk, especially the proposal part of it, and I have two
amendments to suggest to your proposal. First of all, you said that you did
not see any reason not to have the top-level logic to be quite comprehensive, a
superset of all the logics used by the tools, and you then rapidly read a paragraph
of features including, I remember, dependent typing but I heard many others.
And that caused alarm bells to go oﬀ in my mind, because I found that it is easier
to integrate a large number of features into a logic than into a programming
language, and it is not trivial. You can’t always get all the features that you
want to be added. For example, it is very diﬃcult to combine tools that assume
a typed logic with an untyped logic. And if you throw in dependent subtyping,
because you know that it is useful some time, you are actually excluding many
tools from the tool bus.
172     J. Rushby

John Rushby
Yes, that is true. So, for example, SAL has predicate subtypes like PVS, which
does not have full dependent subtyping. [Missing sentence]. So I think there is
some discussion possible here, mainly among those who can go into the highly
technical details. I’d observe, some of what is going on on the bus is typing
judgements. You know whether a thing is a ﬁnite state machine and that itself
is a predicate subtype, whether it is dependent or not is up to the discussion.

Greg Nelson
I just was conveying my concern for what it is worth to you that I would try
to make that top thing as simple as possible rather than as comprehensive as
possible.

John Rushby
Okay, we got 15 years of competition to ﬁgure this out.

Greg Nelson
My second proposal is that the query language by which the front-end or top
looks for tools on the tool bus to answer queries, I think, will become quite
more complicated than what you are describing. Let me give you an example to
explain that issue that, I think, is probably most important: Your example was:
I want to know if this is a well-typed term and one of the tools that can test well-
typedness comes back and returns the answer. It may very well be that no single
tool can do that, but that one tool can put that query into a certain normal form
and another query can ﬁnd the well-typedness of that normal from, so that you
really need to ﬁnd sequential compositions or functional compositions of tools.

John Rushby
That is exactly right. I glossed over [some aspects]. But I did have a slide that
talked about how you could discover that you could verify an inﬁnite state system
by making it ﬁnite state. The same chaining on queries could perhaps build those
sequential compositions for tasks like type checking. So I think, your question
shows that there are a lot of opportunities for spending money in this direction,
and I look forward to those of us trying it.

Tony Hoare
I hope, you will accept payment in kind.

John Rushby
Contributions? Certainly. Of tools and code, yes.
