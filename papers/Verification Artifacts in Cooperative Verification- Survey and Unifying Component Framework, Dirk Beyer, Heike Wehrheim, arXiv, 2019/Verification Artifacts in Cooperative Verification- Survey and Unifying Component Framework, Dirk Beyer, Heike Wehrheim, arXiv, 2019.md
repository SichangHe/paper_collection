                                         Verification Artifacts in Cooperative Verification:
                                                  Survey and Unifying Component Framework

                                                                 Dirk Beyer1 and Heike Wehrheim2

                                                    1                             2
                                                        LMU Munich, Germany           Paderborn University, Germany


                                               Abstract. The goal of cooperative verification is to combine verification
                                               approaches in such a way that they work together to verify a system model.
                                               In particular, cooperative verifiers provide exchangeable information
arXiv:1905.08505v1 [cs.SE] 21 May 2019




                                               (verification artifacts) to other verifiers or consume such information from
                                               other verifiers with the goal of increasing the overall effectiveness and
                                               efficiency of the verification process.
                                               This paper first gives an overview over approaches for leveraging strengths
                                               of different techniques, algorithms, and tools in order to increase the
                                               power and abilities of the state of the art in software verification.
                                               Second, we specifically outline cooperative verification approaches and
                                               discuss their employed verification artifacts. We formalize all artifacts in
                                               a uniform way, thereby fixing their semantics and providing verifiers with
                                               a precise meaning of the exchanged information.


                                         Keywords: Cooperative Verification, Software Verification, Conditional Model
                                         Checking, Verification Witness, Exchange Format, Partial Verification, Reducer,
                                         Execution Report, Tool Combination


                                         1   Introduction
                                         The area of software verification studies methods and constructs tools for au-
                                         tomatically proving program properties. The recent past has seen an enormous
                                         improvement in this area, in particular with respect to scalability, precision,
                                         and the handling of different programming-language features. Today’s software-
                                         verification tools employ a variety of different techniques, ranging from data-flow
                                         analysis [57] over symbolic execution [58] to SAT-based approaches [14, 29]. As
                                         all these techniques have their particular strengths and weaknesses, a number of
                                         tools tightly integrate different —usually two— approaches into one tool (see [15]
                                         for an overview). For instance, the integration of techniques that under- and
                                         over-approximate the state space of the program is a frequent combination. Such
                                         combinations typically improve over pure approaches. However, such combina-
                                         tions also require new tool implementations for every additional integration of
                                         techniques. Portfolio combinations loosely integrate different tools: There is no
                                         communication between the approaches and the resulting combination can be
                                         composed from off-the-shelf components. Algorithm selection combines different
                                         approaches into one by first analyzing the input problem and then choosing the
                                         approach that will most likely (according to some heuristics) succeed.
    In contrast to these extremely tight or extremely loose combinations, coop-
erative verification is a combination of approaches that cooperate, that is, work
together to achieve the verification goal, but leave the existing tools (mostly)
untouched. Cooperative verifiers communicate with each other in order to max-
imize the common strength, in particular, by exchanging information about
intermediate results. In a framework for cooperative verification, the integration
of a new technique requires some implementation to make it understand the
communication, viz. be able to use intermediate results, but it can avoid a new
re-implementation of the combination — from the conceptual as well as from the
practical viewpoint. If the intermediate results come in a format already accepted
by the tool (e.g. as a program), the tool can even be employed as is.
    In this paper, we provide a classification of verification approaches according
to the interface and type of combination employed; we briefly survey combination
approaches, for portfolio, selection, cooperative, and conceptual combination
of verification approaches. We then discuss a number of aspects relevant to
cooperative verification, in particular its objectives and prerequisites.


2     Classification of Verification Approaches
In the following, we provide a classification of verifica-     p                 r
tion approaches according to their way of interfacing
                                                                      Analyze
and combining verification components. By the term
“verification approach” we understand an automatic            ϕb                 ω
or automatable formal method for solving verification
                                                           Fig. 1: Formal verification
tasks, i.e., for evaluating the proposition “Program p
satisfies behavioral specification ϕb ” and returning a result r, which can be
true (p |= ϕb ), false (p 6|= ϕb ), or unknown, and an (optional) witness ω,
which contains proof hints, as depicted in Fig. 1.

2.1    Overview over Interfaces
Output. The goal of a verification tool is to                          Consumption
                                                                        by humans
solve a verification task and to deliver the
                                                Verifier
computed results to either a verification en-                          Consumption
gineer for manual inspection or to a machine                           by machines

for further automated processing (Fig. 2). De-
pending on how the results are consumed (by         Fig. 2: Output Interfaces
human or by machine), the tool needs to use different formats.
    While researchers mainly concentrated on improving the (internal) verification
algorithms during the past two decades, it is understood since recently that it
is (at least) equally important to provide not only true/false answers, but
more details about the reasoning and the process of the verification.
Human. Almost all verification tools provide some kind of statistics to the
user, for example, about the number of iterations, of number of proof facts, or
consumed resources. Execution reports [30] present an underapproximation of
the successfully verified state space to the user. There are also approaches to
support interactive inspection of verification results, e.g., by visualization of
error paths [65] and verification-aided debugging [9].
Machine. In order to make it possible to validate verification results in an au-
tomated way, verification witnesses were introduced [6, 27], a machine-readable
exchange format (XML based). Verification witnesses make it possible to inde-
pendently re-verify the program based on knowledge that another verifier has
produced. This can increase trust in the results, can spread the risk of verification
errors, and can help making internal knowledge from the verification engine
accessible for the user (error paths, program invariants). Violation witnesses [12]
enhance the answer false by a description of the state space that contains an
error path (a program path that violates the specification), while correctness
witnesses [11] enhance the answer true by a description of program invariants
that are helpful to prove that the program satisfies the specification. It is known
since 15 years that test cases can be derived from error paths [7, 75], but this
approach was rarely used in practice and only since recently it is possible to
output and exchange this kind of information via a standard format.
    While the previous approaches, as the name indicates, witness the verification
result, it is also important to make intermediate results and partial results
accessible to further processing. Conditional model checking [17] reads as input
and writes as output a description of the already verified state space. That is, a
conditional verifier outputs a condition that describes the work already done, i.e,
the parts of the state space that are already verified. Another kind of intermediate
output for machines to later reuse it is the abstraction precision [21, 26]. In
CEGAR-based approaches [33] an abstract model is automatically constructed by
finding abstraction facts in refinement steps which are added to the precision of
the analysis (the more abstraction facts are added to the precision, the finer the
abstract model). Full abstract models can be used as certificate of correctness [54]
or in order to speed up later verification runs for different versions of the same
program during regression verification [48].

Input. Similar to the output, there are dif-
ferent interfaces for the kind of input that           Information
                                                      from humans
is given to the verification tools, some from                                  Verifier
users, some from machines, see Fig. 3.                 Information
                                                     from machines
Human. From the very beginning of program-
                                                         Fig. 3: Input Interfaces
ming, assertions were added to programs [73]
in order to make it easier to prove correctness. Nowadays, assertions, invariants,
pre- and post-conditions, are annotated in programs in a way that machines (inter-
active verifiers) can read. There are several languages and tools that support this,
and a nice overview over such tools and their application opportunities are given
in the annual competition on interactive software verification VerifyThis [41].
    There were also attempts to support the splitting of specifications and pro-
grams into modular parts, in order to make the verification task for the model
checkers easier, such as in the Blast query language [8, 68]. Last not least, and
this is one of the most difficult parts, each verifier expects a set of parameters
that the user has to set, in order to choose how the verifier should solve its
task. However, finding the right parameters is a challenging task, which could
use tool support itself (such as SMAC [52] or Tuner [71]).
Machine. A classic approach to make additional information available to a tool
is by transforming the original input, e.g., by simplification or enhancement. The
advantage is that there is no additional input (no extra parser, no need to imple-
ment additional features). For example, the first software model checkers did not
have a specification language, but the specification was weaved into the program
in a preprocessing step (as was done for the Slam [2] specification language Slic [1]
and the Blast [16] query language [8]). Even programs were made simpler [63].
    Verification witnesses and conditions were discussed already above as example
implementations for output interfaces. Verification witnesses can be taken as input
by validation tools that re-establish the verification result using independent tech-
nology. Also, the error path described by the violation witness can be replayed and
a test case can be derived from the path constraints along the found error path [13].
    Conditional model checking is not widespread yet because it was considered
difficult to extend a verifier such that it understands conditions as input and
reduces the state space accordingly before running the verification engine. This
problem was solved by the reducer-based construction of conditional verifiers:
Reducers [23, 37] can be used to construct (without implementation effort) condi-
tional model checkers from off-the-shelf verifiers that do not understand conditions
themselves, by reducing the original input program to a residual program that
contains all the behavior that is not yet covered by the condition and removes
as much as possible from the already-verified state space.


2.2   Overview over Combinations

In the early days of automatic program verification, tools implemented a single
technique for verification (e.g., explicit enumeration of state space or data-
flow analysis using a fixed abstract domain). In our classification (see Fig. 4)
these are represented as Basic. Later, the tools implementing these techniques
were considerably generalized, for instance by allowing abstract domains to
be flexibly set via tool parameters. Still, during one verification run a sin-
gle basic technique was employed.
    It soon turned out that a single verification technique may work well for
some verification tasks, but fail for others. This immediately triggered the ap-
plication of Combination techniques, in order to benefit from the different
strengths. Combinations can come in two sorts: A combination either treats
techniques or tools as Black Box objects and runs them (mainly) as they are
without implementation-specific integrations for which it matters what’s inside
the box, or a combination views a component as White Box, conceptually
integrating two or more techniques within a new tool. We distinguish three
forms of black-box combinations, without and with communication, and classify
all white-box approaches into one category.
                             Verification Approach



                          Basic              Combination



                            Black Box                           White Box



              Portfolio      Selection    Cooperative      Conceptual Integration



       Fig. 4: Hierarchy of verification approaches (using UML notation)



    Portfolio combinations are motivated by
the portfolio idea from economics [51], which           Verifier 1        ... Verifier n
is a means of distribution of risk: if one in-
vestment (here: of computational resources
in a certain technique) fails, there are other                     Verifier 1
investments (techniques) that will be success-
ful. A portfolio combination has a number                            ...
of approaches available, and on a given ver-
                                                                   Verifier n
ification task executes the approaches in a
fixed order sequentially (Fig. 5, top), or runs
all approaches in parallel (Fig. 5, bottom). Fig. 5: Portfolio approaches
The overall approach terminates if one com- (top: sequential, bottom: parallel)
ponent analysis was successful in obtaining
the result. The big advantage of this approach
is that it requires no knowledge about the components and there is almost
no effort for implementing the combination. Therefore, we placed this most
loosely coupled approach on the very left in the bottom row of our Fig. 4.
The big disadvantage of portfolio approaches is that the resources invested on
unsuccessful tools or approaches are lost.
   Algorithm Selection [67] is a solution to the problem of wasted resources of
portfolio approaches: Algorithm-selection approaches have a number of approaches
available, and on a given verification task choose one and execute it (Fig. 6).
That is, before starting an approach, a selection model is extracted from the
input, based on which a selector function predicts which approach would be best,
and only the potentially best approach is selected and executed. This requires
some knowledge about the (black box) characterization of the components, but
does not require any change of the implementation of the components.
   Portfolio and selection approaches run the component tools independently
from each other, without any form of information exchange between the ap-
proaches. The goal of combining strengths of different approaches and at the
                                         Verifier 1      ...         Verifier n


                          Selection-
                                          Selection
                            Model                             Selector
                                           Model
                          Extraction




                                                      Verifier selected



                            Fig. 6: Algorithm selection


same time avoiding to waste resources inspired the development of cooperative
combinations of verification approaches.
    Cooperation approaches enable the possibility of solving the problem to-
gether. Typically, tools exchange intermediate results (e.g., the state space which
has already been searched) in order to achieve a division of labor. Such co-
operative combinations range from two or more basic techniques running in
parallel and combining the information obtained for certain program locations
(e.g., combining partial verification results to proof witnesses [55]) to approaches
executing different tools in turns with each specializing to specific tasks (e.g., a
testing tool trying to achieve coverage together with a model checker constructing
counter examples to non-reachability [38]).
    Conceptual Integration is most intensively coupled approach and therefore
put on the very right end of the bottom row in our Fig. 4. The components are not
communicating via clear interfaces, but are tightly integrated and exchange data
structures via procedure calls and not via interfaces that could be externalized [15].
    In the following subsections, we describe some forms of non-cooperative
verification approaches in more detail. In the next section we explain some
examples for cooperative verification approaches.


2.3   Examples for Portfolio Combinations

While it seems obvious that combinations of verification techniques have a large
potential, for software verification the topic is not yet systematically investigated,
while it is used in other areas since many years [51].
Sequential Combinations. Examples of sequential combinations are SDV and
CPAchecker. The static driver verification (SDV) [3] tool chain at Microsoft
used a sequential combination (described in [72]) which first runs Corral [59]
for up to 1 400 s and then Yogi [64]. CPAchecker [24] won the competition
on software verification 2013 (SV-COMP’13, [5]) using a sequential combina-
tion [76] that started with explicit-state model checking for up to 100 s and
then switched to a predicate analysis [25].
Parallel Combinations. Examples of parallel combinations are the verifiers Ufo [47]
and PredatorHP [62], which start several different strategies simultaneously and
take the result from the approach that terminates first.


2.4   Examples for Algorithm Selection

Algorithm selection [67] first extracts a selection model from the input. In the
case of software verification, the input is the verification task (program and
its specification). The selection model describes some characteristics of the
verification task, for example, feature vectors (measurement values for certain
measures that map verification tasks to values). Based on the selection model, the
strategy selector chooses one strategy from a set of given verification strategies.
Approaches without Machine Learning. Strategy selection can be very simple and
yet effective. For example, a recent work has shown that it is possible with a few
boolean features to effectively improve the overall verification progress [10]. The
disadvantage is that the strategy selector needs to be explicitly defined by the
developer or user. This leads to approaches that use machine learning, in order
to automatically learn the strategy selector from training instances.
Machine-Learning-Based Approaches. The technique MUX [72] can be used to
synthesize a strategy selector for a set of features of the input program and a given
number of strategies. The strategies are verification tools in this case, and the
feature values are statically extracted from the source code of the input program.
Later, a technique that uses more sophisticated features was proposed [39, 40].
While the above techniques use explicit features (defined by measures on the
source code), a more recently developed technique [36] leaves it up to the machine
learning to obtain insights from the input program. The advantage is that there
is no need to define the features: the learner is given the control-flow graph,
the data-dependency graph, and the abstract syntax tree, and automatically
derives internally the characteristics that it needs. Also, the technique predicts
a ranking, that is, the strategy selector is not a function that maps verification
tasks to a strategy, but to a sequence of strategies.


2.5   Examples for Conceptual Integrations

Conceptual integrations tightly combine two or more approaches into a new
tool, typically re-implementing the basic techniques. A frequent combination
of this type is integrating an overapproximating (static) may-analysis with an
underapproximating (dynamic) must-analysis. The tool SMASH [44] at the same
time maintains an over and an under approximation of the state space of programs.
Building on the same idea, Beckman et al. [4] (tool Yogi, first proposal of the
algorithm under name Synergy in [45]) in addition specifically employs testing to
derive alias information which is costly to precisely compute by a static analysis.
    A second form of conceptual integration is offered by tools running different
analysis in parallel in a form of “product” construction. A prototypical example is
the tool CPAchecker [24] with the possibility of specifying and running composite
                         p                r                  r’

                               Analyze          Analyze

                        ϕb     Verifier   ω      Validator   ω’


                     Fig. 7: Witness-based results validation
analyses. A composite analysis could for instance combine two sorts of data-flow
analyses (e.g., an interval analysis and an available-expression analysis). The
analyses are then jointly run and jointly derive analysis information for program
locations. The same idea was classically hard-coded as reduced product [35]
and further improved [20, 34, 42, 46, 60].
   All those combinations have in common that they exchange information, but
they are more intertwinned, hardcoded combinations, rather than interface-based
combinations. More approaches are described in the Handbook on Model Check-
ing, in the chapters on combining model checking with data-flow analysis [15],
with deductive verification [69], and with testing [43].


3     Cooperative Verification Approaches
In the following, we discuss approaches for cooperative verification, structured
according to the kind of information objects which are exchanged, and then
explain a few applications and their effects.

3.1   Exchangeable Objects for Communication and
      Information Transfer
We now classify the approaches for cooperative verification according to the
kinds of communication interfaces that they use. While our text always refers
to software verification for concrete examples, cooperative verification is in
no way limited to software.
Conditions and Residual Programs. Conditional model checking (CMC) [17]
means to produce a condition as output that describes the state-space that
was successfully verified. The (temporal) condition can be represented as an
automaton. This information can be passed on to another verifier as input,
instructing this verifier to not verify again those parts of the state space that are
covered by the condition. Using a reducer [23], a program can be reduced to those
parts of its state space that still has to be verified; the result is called residual
program. Symbiotic [31] can be seen as reducer-based cooperation (slicer + Klee).
Witnesses. Exchangeable witnesses serve as envelopes for error paths and in-
variants in a way that makes it possible to exchange the information between
different tools. A violation witness [6, 12, 27] explains the specification violation,
by describing a path through the program that violates the specification. A cor-
rectness witness [11] explains why the program satisfied the specification, by
describing invariants that are useful to have in a correctness proof. Figure 7
illustrates the process: The first analyzer verifies the program p according to
specification ϕb , and produces a result r and a witness ω. The second ana-
lyzer (re-)verifies the same program and specification using information from the
witness. If the result r matches the result r’, then the result is confirmed.
Precisions. Verification approaches that are based on counterexample-guided
abstraction refinement (CEGAR) [33] iteratively construct an abstract model
of the system. The “abstraction facts” that define the level of abstraction are
often formalized and expressed as precision [21, 26, 27]. The precision can be
exported as output, such that later verification runs can start from such a
given definition of the abstraction level.
Abstract States / Certificates. Extreme model checking [48] dumps the ab-
stract reachability graph (ARG) to a file when the verification process terminates.
Configurable certificates [54] are sets of abstract states that cover all reachable
states of the system. ARGs and configurable certificates can be used by a different
verifier to check its validity (completeness and soundness).
Path Programs and Path Invariants. Path programs [19] are programs (for
example, written in the same programming language as the input program) that
were invented to incorporate external invariant generators into CEGAR-based
approaches and are produced after a verifier has found an infeasible error path
(often called infeasible counterexample). The path program contains that path in
question, but usually also longer paths that use the same program operations,
that is, unrollings of a certain loop. The path program can now be given to a
tool for invariant synthesis (e.g., [18]) in order to obtain path invariants [19],
which are invariants for the whole path program, but in particular also for the
original path. The path invariants can then be fed back into the CEGAR-based
approach that was encountering the original path.


3.2   Objectives and Applications

Having exchangeable objects about (partial) verification results [28] available
is important to overcome a variety of practical problems. In the following, we
highlight a few of the objectives and applications that we can aim for.
Improvement of Effectiveness and Efficiency. Storing intermediate results
can be used to improve the effectiveness and efficiency of the verification process.
Stateful Verification and Reuse. Storing (exchangeable) objects that contain
information about intermediate verification results can be considered as a state
of the verification process, i.e., making the verification process stateful.
    Precisions that are stored and in later verification runs read and reused can
significantly improve the performance of regression verification [26]. The setup of
this strategy is the following: the first version of a module is verified and at the
end, the precision is written to a file. When the i-th version is verified, then the
verifier reads the precision that the verification run for version i−1 has written, in
order to save time discovering the right abstraction level for the abstract model.
    Configurable certificates [54] can reduce the validation time, because the
verifier that performs the validation of the certificate does “only” need to check
for the set of abstract states that all initial states are contained and that the
set is closed under successor transitions.
    Also caching-based approaches to improve the efficiency can be seen as a
stateful way of performing computation. For example, Green [74] makes symbolic
execution more efficient by caching previous intermediate results.
Stateless Verification and Parallelization. The previous argument was based on
having a state that contains the intermediate results. It is also possible to speed up
verification processes in a stateless way. The technique of conditional model check-
ing is used to split programs into parts that can be independently verified [70].
Improvement of Precision and Confidence. Witness-based results valida-
tion [11, 12] can be used to increase the confidence in the results of verification
tools, because it is possible to take a witness-based results validator to “replay” the
verification. That is, for a violation witness, the validator tries to find and confirm
the error path that the witness describes, and for a correctness witness, the valida-
tor tries to use the invariants in the witness to re-establish the proof of correctness.
    Execution-based results validation [13] extracts a test case from a violation
witness and executes it, in order to confirm that the specification violation is
observable in the executed program as well.
Explainability. The existence and availability of exchangeable objects with
information about the verification process makes it possible to develop approaches
for explaining what the verification process did and why the user should be more
confident about the verification result. There are preliminary results on explaining
and visualizing counterexamples, e.g., for SPIN models [61] and for C programs [9],
but due to the exchangeable witness format, many more approaches are possible.


4     Verification Artifacts
This section outlines a construction framework for cooperation. We study verifi-
cation artifacts, classify several verification tools as verification actors according
to their usage of artifacts, and define the semantics of some important artifacts.

4.1    Artifacts of Verification Tools
Verification artifacts are central to cooperation as they provide the means of
information exchange. A number of artifacts exist already, most notably of course
the programs themselves. We identified the following artifacts:
Program p. Defines the implemented behavior of the system. Syntax: C pro-
   gramming language (for example). We represent programs as control-flow
   automata in Sect. 4.3.
Behavior Specification ϕb . Defines requirements that all executions of a given
   program have to satisfy, often as conjunction of several properties. Syntax:
   The competition SV-COMP established a minimal set of properties that
   participants of the competition have to support 1 , which is based on LTL [66],
   but some tools also support monitor automata as specification. We represent
   properties by property automata in Sect. 4.3.
Test Specification ϕt . Defines requirements that a given test suite has to
   satisfy. Syntax: The competition Test-Comp established a minimal set of
   coverage criteria that participants of the competition have to support 2 , which
   is based on FQL [49, 50], but some tools also offer parameters for hard-coded
   coverage criteria. We represent coverage criteria via test-goal automata in
   Sect. 4.3.
Verification Result r. Verification tools return an evaluation of the state-
   ment “Program p satisfies specification ϕb .” as answer, which is from the
   set {true, false, unknown}.
Witness ω. Verification witnesses are used to witness an outcome of a veri-
   fication run, and thus can come in the form of violation and correctness
   witnesses. Syntax: XML-based witness format 3 that is supported by all
   available validators of verification results.
Test case t. Defines a sequence of values for all calls of external functions,
   i.e., inputs for the program. Syntax: XML-based test-case format 4 that is
   supported by all test-case generators that participate in Test-Comp.
Condition ψ. Defines the part of the program behavior that does not need to
   be further explored. For verification, ψ describes the already verified parts.
   For testing, ψ describes the parts of the program that are already covered by
   an existing test suite. Syntax: Condition automata using a notation similar
   to the Blast query language [8].

We use the corresponding capital letters to denote the types (i.e., sets of artifacts
of a kind), for example, the type P is the set of all C programs. Many tools
generate different forms of verification artifacts, but currently only very few
understand more than the artifact “program” as input.


4.2   Classification of Verification Tools as Actors

Based on the identified artifacts, we classify existing tools according to their
usage of artifacts into three sorts of verification actors:

Analyzers. Produce new knowledge about programs, for example verification
   results or test suites.
Transformers. Translate one artifact into another, in order to implement a
   certain feature or support cooperation.
Presenters. Prepare information from artifacts such that it can be presented
   in a human-readable form.
1
  https://sv-comp.sosy-lab.org/2019/rules.php
2
  https://test-comp.sosy-lab.org/2019/rules.php
3
  https://github.com/sosy-lab/sv-witnesses
4
  https://gitlab.com/sosy-lab/software/test-format
             p                           r        p                          r       p                       r

             ϕb        Analyze           ω                Analyze                   ϕb       Analyze

             ψ                           ψ        ϕb                         ω      ω                       ω
                  Conditional Verifier                 Verifier                           Validator

             p                                    p                                 p

                      Transform          p’       ϕb     Transform           t               Present

             ψ                                    ω                                  t
                     Reducer                           Test Extractor                    Test Executor



                                                           p             r
         p                     p’             r
                                                               Analyze           Transform       t       Present
              Transform             Analyze
                                                          ϕb             ω
        ψ                    ϕb               ω
         Conditional Verifier constructed from                    Execution-Based Validation constructed from
         Reducer and Verifier                                     Verifier, Test Extractor, and Test Executor

                 Fig. 8: Graphical visualization of the component framework


     To convey a better understanding of these concepts, consider the following
examples: A verifier is an analyzer of type P × Φb → R × Ω, which takes as input
a program p and a behavior specification ϕb , and produces as output a result r
and a witness ω 5 . A conditional verifier is of type P × Φb × Ψ → R × Ω × Ψ ,
i.e., a verifier that supports also input and output conditions. A validator is
of type P × Φb × Ω → R × Ω, i.e., a verifier that takes as input in addition a
witness. A test-case generator is also an analyzer, but of type P × Φt → 2T ,
which takes as input a program p and a test specification ϕt , and produces
as output a set ts ∈ 2T of test cases.
     Transformers are largely lacking today, only a few exist already [13, 23].
Transformers are, however, key to cooperation: only if a transformer can bring
the artifact into a form understandable by the next tool without implementing an
extension of this tool, cooperation can be put into practice. A test-case extractor
is a transformer of type P ×Φb ×Ω → T , which translates a program, specification,
and violation witness to a test case. The identity function is also a transformer
(for any given type). A reducer is a transformer of type P × Ψ → P , which takes
a program and a condition as input, and transforms it to a residual program.
     Presenters form the interface to the user. A test-case executor is a presenter
of type P × T → {}, which takes a program p and a test case T as input, and
shows a particular program execution to the software engineer.
     Now we can construct, for example, a conditional verifier from a reducer red
and an off-the-shelf verifier ver by composition. For inputs p and ϕb , the expression
ver(red(p, ϕb ), ϕb ) runs the construction. For a verification with an execution-
5
    All verifiers that participate in the competition SV-COMP are analyzers of this form.
                                                 (0,int x = input(), 1)
  0:   int x = input();                      0                            1
  1:   int a = 0;                                                             (1,int a=0, 2)
  2:   int b = 0;
                                                                          2
  3:   while (a < x) {
  4:        a++;                                                              (2, int b=0, 3)
  5:        b++;   // later elided                                        3
                                                       (3, a<x, 4)                 (3, !(a<x), 6)
        }
  6:                                                           4                     6
                                                 (4, a++, 5)       (5, b++, 3)
                                                               5

 (a) Example program p                           (b) Control-flow automaton Ap

            Fig. 9: Example program and its control-flow automaton


based result validation based on a given verifier ver, test extractor wit2test,
and test executor exec, we can write exec(p, wit2test(p, ϕb , ver(p, ϕb ).ω)). Fig-
ure 8 shows a graphical visualization of the individual components and the
two mentioned constructions.
   With our construction framework, it is possible to identify the gaps of
meaningful transformers, and propose solutions to close these gaps, as far
as needed for cooperation.

4.3    Semantics
We now develop the theoretical foundations of artifacts and actors. Artifacts
describe some information about a program (or a program itself), and for sound
cooperation we need to define the semantics of artifacts. For instance, a viola-
tion witness of a program describes a path of the program on which a specific
specification is violated, a condition describes a set of paths of a program which
have (or have not been) inspected by an analyzer. When employing cooperation
as a means for sharing the work load of validation, the cooperating tools need to
agree on the meaning of the exchanged artifacts. Without this, cooperation might
easily get unsound, e.g., returning a result true for a program and specification
although the combined usage of tools has failed to inspect the whole state space
of the program. By defining the semantics of artifacts, we also implicitly define
the desired semantics of the various actors operating on artifacts.
    We start the formalization of artifacts with the definition of programs, our
prime artifact. We denote the set of all program locations by Loc. Formally, a
program p is described by a control-flow automaton (CFA) Ap = (L, `0 , G) that
consists of a set of locations L ⊆ Loc, an initial location `0 ∈ L, and a set of
control-flow edges G ⊆ L×Ops×L, where Ops is the set of operations. Operations
can be (a) assignments, (b) assume statements (arising out of branches), and
(c) calls to functions retrieving inputs. Here, we assume to have a single such
function, called input. We let G = L × Ops × L be the set of all control-flow edges.
     We let X be the set of variables occurring in the operations Ops. For simplicity,
we restrict the type of variables to integers. A concrete data state c : X −→             ◦ Z
is thus a partial mapping from X to Z. In the left of Fig. 9 we see our running
example of the simple program p and its control-flow automaton on the right.
The program starts by retrieving an input for variable x, sets variables a and b
to 0, and then increments both while the value of a is less than that of x.
     A concrete program path of a program Ap = (L, `0 , G) is a sequence
            g1       gn
(c0 , `0 ) −−
            → . . . −−→ (cn , `n ), where the initial concrete data state c0 = ∅ as-
signs no value, gi = (`i−1 , opi , `i ) ∈ G, and ci−1 −op
                                                       −→ i
                                                            ci , i.e., (a) in case of assume
operations, ci−1 |= opi (opi is a boolean condition) and ci−1 = ci , (b) in case of
assignments, ci = SPopi (ci−1 ), where SP is the strongest-post operator of the op-
erational semantics, and (c) in case of inputs of the form x = input(), ci (x) ∈ Z
(nondeterministic choice of input) and ci (y) = ci−1 (y) for all y =      6 x. An edge g is
                                                            g1         gn
contained in a concrete program path π = (c0 , `0 ) −−      → . . . −−  → (cn , `n ) if g = gi
for some i, 1 ≤ i ≤ n. We let paths(Ap ) be the set of all concrete program paths.
     We allow artifacts to state assumptions on program variables. These are given
as state conditions (from a set Γ of predicates over a certain theory). We write
c |= γ to say that a concrete state c satisfies a state condition γ ∈ Γ . Artifacts
on a program p are represented by artifact automata:

Definition 1. An artifact automaton A = (Q, Σ, δ, q0 , Inv, F ) for a program
CFA Ap = (L, `0 , G) consists of

 – a finite set Q of states and an initial state q0 ∈ Q,
 – an alphabet Σ ⊆ 2G × Γ ,
 – a transition relation δ ⊆ Q × Σ × Q,
 – an invariant mapping Inv : Q → Γ , and
 – a set F ⊆ Q of final states.

    We write q −(D,γ)
                 −−−→ q 0 for (q, (D, γ), q 0 ) ∈ δ. In figures, we often elide invariants
as well as the assumptions on edges when they are true. We furthermore elide
the set notation when the element of 2G is a singleton.
    Artifact automata describe paths of a program. Depending on the sort of
artifact automaton, these could for instance be paths allowed or disallowed by a
specification, or paths already checked by a verifier. A path of the program can
be accepted (if the automaton reaches a final state) or covered by the automaton.

Definition 2. An artifact automaton A = (Q, Σ, δ, q0 , Inv, F ) matches a path
                g1            g2       gn                                      (G ,γ1 )
π = (c0 , `0 ) −−
                → (c1 , `1 ) −−
                              → . . . −−→ (cn , `n ) if there is a run ρ = q0 −−−1−−→
    (G2 ,γ2 )      (Gk ,γk )
q1 −−−−−→ . . . −−−−−→ qk , 0 ≤ k ≤ n, in A, s.t.

 1. ∀i, 1 ≤ i ≤ k : gi ∈ Gi ,
 2. ∀i, 0 ≤ i ≤ k : ci |= Inv(qi ) and
 3. ∀i, 1 ≤ i ≤ k : ci |= γi .

The artifact automaton A accepts the path π if A matches π and qk ∈ F , and
A covers π if A matches π and k = n.
           q0    o/w                                           q0        o/w

            (3, !(a<x), 6), a!=b                                    (3, (a<x), 4), true

           qe                                                  qf

  (a) Property automaton A¬ϕb                          (b) Test-goal automaton Aϕt

          Fig. 10: Automata for a property and a test-goal specification


    We let L(A) be the set of paths accepted by the automaton A (its language)
and paths(A) be the set of paths covered by A. As we will see below, some
artifact automata might have an empty set of final states and just describe
a set of paths that they cover.

Artifact Automata as Representation of Artifacts. We consider different
specializations of artifact automata and use the notation As to denote the
automaton that represents the syntactical object s.
(1) A property automaton (or, observer automaton) A¬ϕb                                =
(Q, Σ, δ, q0 , Inv, F ) is an artifact automaton that satisfies the following conditions:

 1. ∀q ∈ Q : Inv(q) = true ,
                         Wn                                    o
 2. ∀q ∈ Q \ F, ∀g ∈ G :     γ | ∃q 0 , ∃D, g ∈ D : q −(D,γ)
                                                       −−−→ q 0 = true
              W
   (assuming ∅ = false).

Condition 2 ensures that property automata only observe the state of the program
(when running in parallel with the program). They do not block, except for the
case when the final state is reached where blocking is allowed. Final states denote
the reaching of property violations (or, targets).
(2) A test-goal automaton Aϕt = (Q, Σ, δ, q0 , Inv, F ) is an artifact automaton
that has only trivial state invariants, i.e., ∀q ∈ Q : Inv(q) = true. If a final
state is reached, the test goal is fulfilled.
    Figure 10 shows two specification automata: In Fig. 10a we see a property
automaton specifying that variables a and b have to be equal when the loop
terminates, i.e., the error state is reached if there is a transition from location
3 to 6 at which a 6= b. The label o/w (otherwise) denotes all transitions other
than the ones explicitly depicted. Figure 10b depicts a test-goal automaton
for the branch condition entering the loop.
(3) A violation-witness automaton Aω = (Q, Σ, δ, q0 , Inv, F ) is again an ar-
tifact automaton with trivial state invariants only, i.e., ∀q ∈ Q : Inv(q) = true.
    Violation witnesses are used to describe the part of a program’s state space
which contains the error. The final state is reached if an error is detected. Counter
examples are a specific form of violation witnesses which describe a single path.
(4) A correctness-witness automaton Aω = (Q, Σ, δ, q0 , Inv, F ) is
an artifact automaton that has only trivial transition assumptions, i.e.,
  ∀(q, (D, γ), q 0 ) ∈ δ : γ = true , and there are no final states ( F = ∅ ). A cor-
rectness witness typically gives information about the state space of the program
(like a loop invariant) in order to facilitate its verification.
    In Fig. 11 we see both a correctness and a violation witness. The correctness
witness belongs to program p and, e.g., certifies that at location 3 variables a and
b are equal (via the invariant for q3 ). The violation witness on the right belongs
to program p with line 5 removed, i.e., a program which does not satisfy the
property stated in Fig. 10a. The violation witness states that an input value of x
being greater or equal to 1 is needed for directing the verifier towards the error.
(5) A condition automaton Aψ = (Q, Σ, δ, q0 , Inv, F ) is an artifact automa-
ton that satisfies

 1. ∀q ∈ Q : Inv(q) = true (no invariants on states) and
 2. ¬∃(qf , ∗, q) ∈ δ with qf ∈ F (no transitions leaving final states).

A condition is typically used to describe parts of the state space of a program,
e.g., the part already explored during verification. Final states are thus used
to fix which paths have already been explored.
    A test case is a sequence of input values consecutively supplied to the calls of
function input. Such a test case is encoded as artifact automaton using a special
template variable χ that can be instantiated with every program variable.
(6) A test-case automaton At = (Q, Σ, δ, q0 , Inv, F ) for a test case
hz1 , . . . , zn i is an artifact automaton with the following components:
 Q = {q0 , . . . , qn }, qi −((∗,χ=input(),∗),χ=z
                             −−−−−−−−−−−−−−i+1    −−
                                                    )
                                                   → qi+1 , qi −o/w
                                                                −→ qi (0 ≤ i < n)
and F = ∅ . For matching these special transitions (Gi , γi ) = ((∗, χ =
input(), ∗), χ = z) with program paths, the program transitions gi have to
be of the form (`, x = input(), `0 ) and the next state needs to satisfy ci (x) = z,
ci (y) = ci−1 (y) for y 6= x.
     Figure 12a gives a condition stating the exploration of the state space for
inputs less or equal to 0. This could for instance be the output of a verifier
having checked that the property holds for inputs x ≤ 0. Figure 12b is the
test-case automaton for the test case h4i.

Semantics of Artifact Automata. The above definitions fix the syntacti-
cal structure of artifact automata. In addition, we need to state their seman-
tics, i.e., the meaning of particular artifacts for a given program. In the fol-
lowing, we let Ap = (L, `0 , G) be the CFA for a program p and A¬ϕb , Aω ,
and Aϕt be artifact automata.
(i) The program p fulfills a property specification ϕb if paths(Ap ) ∩ L(A¬ϕb ) = ∅ .
Our running example p fulfills the property of Fig. 10a.
(ii) A correctness witness ω is valid for a program p and property specification ϕb
if paths(Ap ) ⊆ paths(Aω ) ∧ paths(Ap ) ∩ L(A¬ϕb ) = ∅ . We see here that a cor-
rectness witnesses can thus be used to facilitate verification: when we run program,
property, and correctness witness in parallel in order to check the emptiness of
                                                        q0

                                                          (0,int x=input(), 1), x ≥ 1

                      q0   true                         q0

                        (0,int x=input(), 1)              (1,int a=0, 2)
                                                        q1
                      q1   true
                                                          (2, int b=0, 3)
                        (1,int a=0, 2)
                                                        q2
                      q2   a=0
                                                             (3, a<x, 4)
                        (2, int b=0, 3)
                                                        q3
                      q3   a=b
       (3, a<x, 4)          (3, !(a<x), 6)                   (4, a++, 3)

      a = b q4                    q6   a=b              q4

  (4, a++, 5)     (5, b++, 3)                             (3, !(a<x), 6)

   a − 1 = b q5                                         qe

(a) Correctness witness automaton Aω           (b) Violation witness automaton Aω

Fig. 11: Automata for a correctness witness for program p and a violation witness
for p without line 5, both wrt. behavior specification ϕb of Fig. 10a

paths(Ap )∩L(A¬ϕb ), the correctness witness helps in proving the program correct.
The correctness witness in Fig. 11a is valid for p and the property in Fig. 10a.
(iii) A violation witness ω is valid for a program p and a property specification ϕb
if paths(Ap ) ∩ L(Aω ) ∩ L(A¬ϕb ) 6= ∅ . During verification, violation witnesses
can thus steer state-space exploration towards the property violation. Looking
again at the running example: If we elide the statement in location 5 of our
program, the automaton in Fig. 11b is a valid violation witness. It restricts the
state-space exploration to inputs for variable x which are greater or equal to 1.
(iv) A condition ψ is correct for a program p and property ϕb if
 paths(Ap ) ∩ L(Aψ ) ∩ L(A¬ϕb ) = ∅ . All program paths accepted by the con-
dition fulfill the specification given by the property automaton. The condition
in Fig. 12a describes all paths of the program p which initially started with
input x less or equal to 0. This condition is correct for p and the property
automaton in Fig. 10a.
    Finally, for testing we are interested in test inputs covering certain test goals.
(v) A test-case t for a program p covers the goals of a test-goal specification ϕt
if paths(Ap ) ∩ paths(At ) ∩ L(Aϕt ) 6= ∅ . Basically, we require that the inputs
provided by the test case guarantee program execution to reach (at least one)
test goal. If there are more than one final state in the test-goal automaton
(or the final state can be reached via different paths), the test-goal automa-
ton specifies several test goals. In this case, the test case covers only some
of these goals. The test-case automaton in Fig. 12b for p covers the (single)
goal of the test-goal automaton in Fig. 10b.
         q0                                                q0    o/w

          (0,int x=input(),1), x ≤ 0                        (*, χ = input(), *), χ = 4
         q1                                                q1    o/w

    (a) Condition automaton Aψ                        (b) Test-case automaton At

                  Fig. 12: Automata for a condition and a test case


5     Conclusion

Different verification approaches have different strengths, and the only way
to benefit from a variety of approaches is to combine them. The two classic
approaches of combining approaches either in white-box manner via a tight
conceptual integration or in black-bock manner via loosely coupled combinations,
such as portfolio or selection, are both insufficient.
    We propose that the right direction to go is the way of cooperation: a loosely-
coupled combination of tools that interact via clear interfaces and exchange
formats, in order to achieve the verification goal together. To this end, we provide
a classification and an overview of existing techniques, which we briefly describe,
while giving most importance to cooperative approaches.


References

 1. Ball, T., Rajamani, S.K.: SLIC: A specification language for interface checking (of
    C). Tech. Rep. MSR-TR-2001-21, Microsoft Research (2002)
 2. Ball, T., Rajamani, S.K.: The Slam project: Debugging system software via
    static analysis. In: Proc. POPL. pp. 1–3. ACM (2002). https://doi.org/10.1145/
    503272.503274
 3. Ball, T., Bounimova, E., Kumar, R., Levin, V.: SLAM2: Static driver verification
    with under 4 % false alarms. In: Proc. FMCAD. pp. 35–42. IEEE (2010)
 4. Beckman, N.E., Nori, A.V., Rajamani, S.K., Simmons, R.J., Tetali, S., Thakur,
    A.V.: Proofs from tests. IEEE Trans. Software Eng. 36(4), 495–508 (2010). https:
    //doi.org/10.1109/TSE.2010.49
 5. Beyer, D.: Second competition on software verification (Summary of SV-COMP
    2013). In: Proc. TACAS. pp. 594–609. LNCS 7795, Springer (2013). https://doi.
    org/10.1007/978-3-642-36742-7_43
 6. Beyer, D.: Software verification and verifiable witnesses (Report on SV-COMP
    2015). In: Proc. TACAS. pp. 401–416. LNCS 9035, Springer (2015). https://doi.
    org/10.1007/978-3-662-46681-0_31
 7. Beyer, D., Chlipala, A.J., Henzinger, T.A., Jhala, R., Majumdar, R.: Generating
    tests from counterexamples. In: Proc. ICSE. pp. 326–335. IEEE (2004). https:
    //doi.org/10.1109/ICSE.2004.1317455
 8. Beyer, D., Chlipala, A.J., Henzinger, T.A., Jhala, R., Majumdar, R.: The Blast
    query language for software verification. In: Proc. SAS. pp. 2–18. LNCS 3148,
    Springer (2004)
 9. Beyer, D., Dangl, M.: Verification-aided debugging: An interactive web-service for
    exploring error witnesses. In: Proc. CAV (2). pp. 502–509. LNCS 9780, Springer
    (2016). https://doi.org/10.1007/978-3-319-41540-6_28
10. Beyer, D., Dangl, M.: Strategy selection for software verification based on boolean
    features: A simple but effective approach. In: Proc. ISoLA. pp. 144–159. LNCS 11245,
    Springer (2018). https://doi.org/10.1007/978-3-030-03421-4_11
11. Beyer, D., Dangl, M., Dietsch, D., Heizmann, M.: Correctness witnesses: Exchanging
    verification results between verifiers. In: Proc. FSE. pp. 326–337. ACM (2016).
    https://doi.org/10.1145/2950290.2950351
12. Beyer, D., Dangl, M., Dietsch, D., Heizmann, M., Stahlbauer, A.: Witness validation
    and stepwise testification across software verifiers. In: Proc. FSE. pp. 721–733. ACM
    (2015). https://doi.org/10.1145/2786805.2786867
13. Beyer, D., Dangl, M., Lemberger, T., Tautschnig, M.: Tests from witnesses:
    Execution-based validation of verification results. In: Proc. TAP. pp. 3–23.
    LNCS 10889, Springer (2018). https://doi.org/10.1007/978-3-319-92994-1_1
14. Beyer, D., Dangl, M., Wendler, P.: A unifying view on SMT-based software verifi-
    cation. J. Autom. Reasoning 60(3), 299–335 (2018). https://doi.org/10.1007/
    s10817-017-9432-6
15. Beyer, D., Gulwani, S., Schmidt, D.: Combining model checking and data-flow analy-
    sis. In: Clarke, E.M., Henzinger, T.A., Veith, H. (eds.) Handbook on Model Checking,
    pp. 493–540. Springer (2018). https://doi.org/10.1007/978-3-319-10575-8_16
16. Beyer, D., Henzinger, T.A., Jhala, R., Majumdar, R.: The software model checker
    Blast. Int. J. Softw. Tools Technol. Transfer 9(5-6), 505–525 (2007). https:
    //doi.org/10.1007/s10009-007-0044-z
17. Beyer, D., Henzinger, T.A., Keremoglu, M.E., Wendler, P.: Conditional model
    checking: A technique to pass information between verifiers. In: Proc. FSE. ACM
    (2012). https://doi.org/10.1145/2393596.2393664
18. Beyer, D., Henzinger, T.A., Majumdar, R., Rybalchenko, A.: Invariant synthesis
    for combined theories. In: Proc. VMCAI. pp. 378–394. LNCS 4349, Springer (2007).
    https://doi.org/10.1007/978-3-540-69738-1_27
19. Beyer, D., Henzinger, T.A., Majumdar, R., Rybalchenko, A.: Path invariants. In:
    Proc. PLDI. pp. 300–309. ACM (2007)
20. Beyer, D., Henzinger, T.A., Théoduloz, G.: Lazy shape analysis. In: Proc. CAV.
    pp. 532–546. LNCS 4144, Springer (2006)
21. Beyer, D., Henzinger, T.A., Théoduloz, G.: Program analysis with dynamic precision
    adjustment. In: Proc. ASE. pp. 29–38. IEEE (2008). https://doi.org/10.1109/
    ASE.2008.13
22. Beyer, D., Jakobs, M.C.: CoVeriTest: Cooperative verifier-based testing. In: Proc.
    FASE. pp. 389–408. LNCS 11424, Springer (2019). https://doi.org/10.1007/
    978-3-030-16722-6_23
23. Beyer, D., Jakobs, M.C., Lemberger, T., Wehrheim, H.: Reducer-based construction
    of conditional verifiers. In: Proc. ICSE. pp. 1182–1193. ACM (2018). https://doi.
    org/10.1145/3180155.3180259
24. Beyer, D., Keremoglu, M.E.: CPAchecker: A tool for configurable software
    verification. In: Proc. CAV. pp. 184–190. LNCS 6806, Springer (2011). https:
    //doi.org/10.1007/978-3-642-22110-1_16
25. Beyer, D., Keremoglu, M.E., Wendler, P.: Predicate abstraction with adjustable-
    block encoding. In: Proc. FMCAD. pp. 189–197. FMCAD (2010)
26. Beyer, D., Löwe, S., Novikov, E., Stahlbauer, A., Wendler, P.: Precision reuse for
    efficient regression verification. In: Proc. FSE. pp. 389–399. ACM (2013). https:
    //doi.org/10.1145/2491411.2491429
27. Beyer, D., Wendler, P.: Reuse of verification results: Conditional model checking,
    precision reuse, and verification witnesses. In: Proc. SPIN. pp. 1–17. LNCS 7976,
    Springer (2013). https://doi.org/10.1007/978-3-642-39176-7_1
28. Beyer, D.: Partial verification and intermediate results as a solution to combine
    automatic and interactive verification techniques. In: Proc. ISoLA. pp. 874–880.
    LNCS 9952, Springer (2016). https://doi.org/10.1007/978-3-319-47166-2
29. Biere, A., Cimatti, A., Clarke, E.M., Zhu, Y.: Symbolic model checking without
    BDDs. In: Proc. TACAS. pp. 193–207. LNCS 1579, Springer (1999). https://doi.
    org/10.1007/3-540-49059-0_14
30. Castaño, R., Braberman, V.A., Garbervetsky, D., Uchitel, S.: Model checker ex-
    ecution reports. In: Proc. ASE. pp. 200–205. IEEE (2017). https://doi.org/10.
    1109/ASE.2017.8115633
31. Chalupa, M., Vitovská, M., Strejcek, J.: Symbiotic 5: Boosted instrumentation
    (competition contribution). In: Proc. TACAS. pp. 442–446. LNCS 10806, Springer
    (2018). https://doi.org/10.1007/978-3-319-89963-3_29
32. Christakis, M., Müller, P., Wüstholz, V.: Guiding dynamic symbolic execution
    toward unverified program executions. In: Proc. ICSE. pp. 144–155. ACM (2016).
    https://doi.org/10.1145/2884781.2884843
33. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided
    abstraction refinement for symbolic model checking. J. ACM 50(5), 752–794 (2003).
    https://doi.org/10.1145/876638.876643
34. Codish, M., Mulkers, A., Bruynooghe, M., de la Banda, M.G., Hermenegildo, M.:
    Improving abstract interpretations by combining domains. In: Proc. PEPM. pp.
    194–205. ACM (1993). https://doi.org/http://doi.acm.org/10.1145/154630.
    154650
35. Cousot, P., Cousot, R.: Systematic design of program-analysis frameworks. In: Proc.
    POPL. pp. 269–282. ACM (1979). https://doi.org/10.1145/567752.567778
36. Czech, M., Hüllermeier, E., Jakobs, M., Wehrheim, H.: Predicting rankings of
    software verification tools. In: Proc. SWAN. pp. 23–26. ACM (2017). https://doi.
    org/10.1145/3121257.3121262
37. Czech, M., Jakobs, M., Wehrheim, H.: Just test what you cannot verify! In: Proc.
    FASE. pp. 100–114. LNCS 9033, Springer (2015). https://doi.org/10.1007/
    978-3-662-46675-9_7
38. Daca, P., Gupta, A., Henzinger, T.A.: Abstraction-driven concolic testing. In: Proc.
    VMCAI. pp. 328–347. LNCS 9583, Springer (2016). https://doi.org/10.1007/
    978-3-662-49122-5_16
39. Demyanova, Y., Pani, T., Veith, H., Zuleger, F.: Empirical software metrics for
    benchmarking of verification tools. In: Proc. CAV. pp. 561–579. LNCS 9206, Springer
    (2015). https://doi.org/10.1007/978-3-319-21690-4_39
40. Demyanova, Y., Pani, T., Veith, H., Zuleger, F.: Empirical software metrics for
    benchmarking of verification tools. Formal Methods in System Design 50(2-3),
    289–316 (2017). https://doi.org/10.1007/s10703-016-0264-5
41. Ernst, G., Huisman, M., Mostowski, W., Ulbrich, M.: Verifythis - verification
    competition with a human factor. In: Proc. TACAS. pp. 176–195. LNCS 11429,
    Springer (2019). https://doi.org/10.1007/978-3-030-17502-3_12
42. Fischer, J., Jhala, R., Majumdar, R.: Joining data flow with predicates. In: Proc.
    FSE. pp. 227–236. ACM (2005). https://doi.org/10.1145/1081706.1081742
43. Godefroid, P., Sen, K.: Combining model checking and testing. In: Handbook
    of Model Checking, pp. 613–649. Springer (2018). https://doi.org/10.1007/
    978-3-319-10575-8_19
44. Godefroid, P., Nori, A.V., Rajamani, S.K., Tetali, S.: Compositional may-must
    program analysis: unleashing the power of alternation. In: Proc. POPL. pp. 43–56.
    ACM (2010). https://doi.org/10.1145/1706299.1706307
45. Gulavani, B.S., Henzinger, T.A., Kannan, Y., Nori, A.V., Rajamani, S.K.: Synergy:
    A new algorithm for property checking. In: Proc. FSE. pp. 117–127. ACM (2006).
    https://doi.org/10.1145/1181775.1181790
46. Gulwani, S., Tiwari, A.: Combining abstract interpreters. In: Proc. PLDI. pp.
    376–386. ACM (2006). https://doi.org/http://doi.acm.org/10.1145/1133981.
    1134026
47. Gurfinkel, A., Albarghouthi, A., Chaki, S., Li, Y., Chechik, M.: Ufo: Verification
    with interpolants and abstract interpretation (competition contribution). In: Proc.
    TACAS. pp. 637–640. LNCS 7795, Springer (2013). https://doi.org/10.1007/
    978-3-642-36742-7_52
48. Henzinger, T.A., Jhala, R., Majumdar, R., Sanvido, M.A.A.: Extreme model
    checking. In: Verification: Theory and Practice. pp. 332–358 (2003)
49. Holzer, A., Schallhart, C., Tautschnig, M., Veith, H.: Query-driven program testing.
    In: Proc. VMCAI. pp. 151–166. LNCS 5403, Springer (2009). https://doi.org/
    10.1007/978-3-540-93900-9_15
50. Holzer, A., Schallhart, C., Tautschnig, M., Veith, H.: How did you specify your
    test suite. In: Proc. ASE. pp. 407–416. ACM (2010). https://doi.org/10.1145/
    1858996.1859084
51. Huberman, B.A., Lukose, R.M., Hogg, T.: An economics approach to hard compu-
    tational problems. Science 275(7), 51–54 (1997)
52. Hutter, F., Hoos, H.H., Leyton-Brown, K.: Sequential model-based optimization for
    general algorithm configuration. In: Proc. LION. pp. 507–523. LNCS 6683, Springer
    (2011). https://doi.org/10.1007/978-3-642-25566-3_40
53. Jakobs, M.C.: Speed up configurable certificate validation by certificate reduction
    and partitioning. In: Proc. SEFM. pp. 159–174. LNCS 9276, Springer (2015).
    https://doi.org/10.1007/978-3-319-22969-0_12
54. Jakobs, M.C., Wehrheim, H.: Certification for configurable program analysis. In:
    Proc. SPIN. pp. 30–39. ACM (2014). https://doi.org/10.1145/2632362.2632372
55. Jakobs, M.: PARTP W : From partial analysis results to a proof witness. In: Proc.
    SEFM. pp. 120–135. LNCS 10469, Springer (2017). https://doi.org/10.1007/
    978-3-319-66197-1_8
56. Jakobs, M., Wehrheim, H.: Compact proof witnesses. In: Proc. NFM. pp. 389–403.
    LNCS 10227, Springer (2017). https://doi.org/10.1007/978-3-319-57288-8_28
57. Kildall, G.A.: A unified approach to global program optimization. In: Proc. POPL.
    pp. 194–206. ACM (1973). https://doi.org/10.1145/512927.512945
58. King, J.C.: Symbolic execution and program testing. Commun. ACM 19(7), 385–394
    (1976). https://doi.org/10.1145/360248.360252
59. Lal, A., Qadeer, S., Lahiri, S.K.: A solver for reachability modulo theories. In:
    Proc. CAV. pp. 427–443. LNCS 7358, Springer (2012). https://doi.org/10.1007/
    978-3-642-31424-7_32
60. Lerner, S., Grove, D., Chambers, C.: Composing data-flow analyses and trans-
    formations. In: Proc. POPL. pp. 270–282. ACM (2002). https://doi.org/http:
    //doi.acm.org/10.1145/503272.503298
61. Leue, S., Befrouei, M.T.: Counterexample explanation by anomaly detection. In:
    Proc. SPIN. pp. 24–42. LNCS 7385, Springer (2012). https://doi.org/10.1007/
    978-3-642-31759-0_5
62. Müller, P., Peringer, P., Vojnar, T.: Predator hunting party (competition con-
    tribution). In: Proc. TACAS. pp. 443–446. LNCS 9035, Springer (2015). https:
    //doi.org/10.1007/978-3-662-46681-0_40
63. Necula, G.C., McPeak, S., Rahul, S.P., Weimer, W.: Cil: Intermediate language
    and tools for analysis and transformation of C programs. In: Proc. CC. pp. 213–228.
    LNCS 2304, Springer (2002)
64. Nori, A.V., Rajamani, S.K., Tetali, S., Thakur, A.V.: The yogiproject: Software
    property checking via static analysis and testing. In: Proc. TACAS. pp. 178–181.
    LNCS 5505, Springer (2009). https://doi.org/10.1007/978-3-642-00768-2_17
65. Novikov, E., Zakharov, I.S.: Towards automated static verification of GNU C
    programs. In: Proc. PSI. pp. 402–416. LNCS 10742, Springer (2017). https://doi.
    org/10.1007/978-3-319-74313-4_30
66. Piterman, N., Pnueli, A.: Temporal logic and fair discrete systems. In: Hand-
    book of Model Checking, pp. 27–73. Springer (2018). https://doi.org/10.1007/
    978-3-319-10575-8_2
67. Rice, J.R.: The algorithm selection problem. Advances in Computers 15, 65–118
    (1976). https://doi.org/10.1016/S0065-2458(08)60520-3
68. O. Ŝerý: Enhanced property specification and verification in Blast. In: Proc. FASE.
    pp. 456–469. LNCS 5503, Springer (2009)
69. Shankar, N.: Combining model checking and deduction. In: Handbook of
    Model Checking., pp. 651–684. Springer (2018). https://doi.org/10.1007/
    978-3-319-10575-8_20
70. Sherman, E., Dwyer, M.B.: Structurally defined conditional data-flow static analysis.
    In: Proc. TACAS (2). pp. 249–265. LNCS 10806, Springer (2018). https://doi.
    org/10.1007/978-3-319-89963-3_15
71. Torsney-Weir, T., Saad, A., Möller, T., Hege, H., Weber, B., Verbavatz, J.: Tuner:
    Principled parameter finding for image segmentation algorithms using visual re-
    sponse surface exploration. IEEE Trans. Vis. Comput. Graph. 17(12), 1892–1901
    (2011). https://doi.org/10.1109/TVCG.2011.248
72. Tulsian, V., Kanade, A., Kumar, R., Lal, A., Nori, A.V.: MUX: Algorithm selection
    for software model checkers. In: Proc. MSR. ACM (2014)
73. Turing, A.: Checking a large routine. In: Report on a Conference on High Speed
    Automatic Calculating Machines. pp. 67–69. Cambridge Univ. Math. Lab. (1949)
74. Visser, W., Geldenhuys, J., Dwyer, M.B.: Green: Reducing, reusing, and recycling
    constraints in program analysis. In: Proc. FSE. pp. 58:1–58:11. ACM (2012).
    https://doi.org/10.1145/2393596.2393665
75. Visser, W., Păsăreanu, C.S., Khurshid, S.: Test input generation with Java
    PathFinder. In: Proc. ISSTA. pp. 97–107. ACM (2004). https://doi.org/10.
    1145/1007512.1007526
76. Wendler, P.: CPAchecker with sequential combination of explicit-state analysis
    and predicate analysis (competition contribution). In: Proc. TACAS. pp. 613–615.
    LNCS 7795, Springer (2013). https://doi.org/10.1007/978-3-642-36742-7_45
