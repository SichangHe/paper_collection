                                               A case study in formal verification of a Java program

                                                                  Dmitry Brizhinev                                           Rajeev Goré
                                                      Research School of Computer Science                       Research School of Computer Science
                                                          Australian National University                            Australian National University
                                                               Canberra, Australia                                       Canberra, Australia
                                                              dmitry.brizhinev@anu.edu.au                                 rajeev.gore@anu.edu.au
arXiv:1809.03162v1 [cs.LO] 10 Sep 2018




                                         ABSTRACT                                                           1.1 JML
                                         We describe a successful attempt to formally verify a simple       JML (Java Modelling Language) [27] is a language for anno-
                                         genetic algorithm written in Java. To this end, we compare         tating Java programs with specifications. It supports func-
                                         several formal verification tools designed for Java, and se-       tion pre- and post-conditions, loop invariants, class invari-
                                         lect Krakatoa as the most appropriate for the task. Based          ants, and assertions at arbitrary positions in the code. JML
                                         on our experience, we present several suggestions for mak-         annotations are specially-formatted comments. Its syntax is
                                         ing the tools more user friendly, which we hope will lead to       very similar to Java code, making it very easy for a Java pro-
                                         wider adoption of formal methods. In particular, we dis-           grammer to learn and apply, and it supports some advanced
                                         cuss at length how useful it would be for provers to perform       operations such as \forall and \sum.
                                         some form of abduction, that is, for them to guess which
                                         extra assumptions they need to prove a statement. It is our        Java verification tools universally assume specifications writ-
                                         opinion that progress in this area would produce the largest       ten in JML, although they vary in their level of support for
                                         improvement in the usability of formal verification tools.         particular JML constructs.

                                         1.   INTRODUCTION                                                  1.2 Models
                                         Formal verification is a family of techniques for construct-       Reasoning about the behaviour of a program requires encod-
                                         ing proofs of the correctness of software. A program with          ing the semantics of the programming language into logic
                                         a formal proof of correctness is much less likely to contain       formulae [13]. This encoding is called a model. If the model
                                         bugs than one that has merely been tested. Unfortunately,          and the properties of the program we wish to prove are ex-
                                         the process is still prohibitively difficult with current tools,   pressed as an SMT problem, we can send them to an off-
                                         and formal verification is thus confined to systems with a         the-shelf solver that will attempt to prove the assertion or
                                         very high cost of failure, such as CPU design [23] and air-        find a counterexample.
                                         craft control systems [30]. However, we hope that better
                                         tools could add formal verification to the average program-        1.3 SMT
                                         mer’s code-checking toolkit, alongside testing and code re-        Traditional SAT solvers reason about formulas expressed in
                                         view, thus improving code quality across the board.                pure propositional logic. However, statements we wish to
                                                                                                            prove about programs often involve additional constructs
                                         Additionally, formal methods are easier to apply and have          with associated theories, such as the theory of integers, or
                                         been better developed for functional programming languages         the theory of lists. We can thus consider formal verifica-
                                         such as Haskell than for the more commonly used impera-            tion as an SMT (satisfiability modulo theories) problem [5].
                                         tive languages such as C and Java. As an example, the              While it may be possible to express a theory as a set of
                                         seL4 project to verify an operating system kernel [26] used        propositional axioms over the objects of interest, it turns
                                         Haskell as an intermediate representation in their proof pro-      out to be more efficient to extend SAT solvers with special-
                                         cess, rather than verifying properties of the C program di-        purpose routines for reasoning about these theories. Many
                                         rectly. As we are interested in encouraging wider adoption of      such SMT solvers are available, including CVC4 [4], Simplify
                                         formal methods, we investigated the current state of the art       [18], Yices [19], and Z3 [16].
                                         for verification of Java programs, a language currently seen
                                         as first or second by popularity [11, 3, 2]. To this end, we
                                         compared several verification tools for Java, and then ver-        1.4 Types of tool
                                         ified a simple program using the tool we thought the most          Given a Java program annotated with JML, there are several
                                         appropriate, Krakatoa [21].                                        possible approaches for checking its correctness.

                                         In this paper, we provide a comparison of the tools we inves-      1.4.1 Runtime assertion checking
                                         tigated, an overview of our experience with Krakatoa, and          JML pre-conditions, post-conditions, class invariants and as-
                                         several suggestions for making formal tools more accessible.       sertions can be checked at runtime. This is not really formal
                                                                                                            verification and will not be further considered here.
1.4.2 Bounded model checking
Bounded model checking verifies the correctness of the pro-      Table 1: Overview of Java verification tools surveyed
                                                                  Tool           Available Maintained Type          Ref
gram assuming some fixed bound on the number of times a
loop body can be executed and a bound on the size of any ar-
rays. Under these assumptions, either a proof of correctness      LOOP             ✗           ✗              ?             [31]
or a counterexample can usually be generated automatically,       JACK             ✗           ✗              ?             [8]
even for complicated specifications. The result is equivalent     TACO             ✓           ?              BMC           [24]
to testing all possible inputs up to some size limit. It is       Sireum/Kiasan    ✓           ?              BMC           [17]
hoped that most bugs in the program will manifest them-           ESC/Java2        ✓           ✗              A-SMT         [15]
selves on small examples. This is the easiest way to verify       OpenJML          ✓           ✓              A-SMT         [14]
a program, but cannot guarantee correctness for inputs (or        KeY              ✓           ✓              A/I-SMT       [6]
execution paths) that exceed the bounds.                          Krakatoa         ✓           ✗              A/I-SMT       [21]


1.4.3 Automated SMT solving                                                       Table 2: Capabilities
Some tools encode the program and the JML assertions as           Tool             Java version FP \forall           \sum
an SMT problem and send it to an off-the-shelf SMT solver.
For this kind of proof to succeed, loops need to be annotated     LOOP             ?                ?   ?            ?
with appropriate invariants. Even then, between proof and         JACK             ?                ?   ?            ?
counterexample lies a large space of inputs on which the          TACO             =6               ✗   ✓            ✓
SMT solvers will time out or report failure. A verification       Sireum/Kiasan    =6               ✗   ✗            ✗
tool based on automated SMT solving (only) will then also         ESC/Java2        =4               ?   ?            ?
report failure. The only way to respond is to change the an-      OpenJML          =7               ✗   ✓            ✗
notations to something that might be easier to prove, or to       KeY              ≥6               ✗   ✓            ✓
abandon the proof attempt. In our experience, it is usually       Krakatoa         Any              ✓   ✓            ✗
possible (but difficult) to find annotations that lead to suc-
cess. The automated SMT solving approach is sometimes
referred to as ESC (Extended Static Checking).                                    Table 3: Ease of use
                                                                  Tool             Setup        Use
1.4.4 Interactive SMT solving
Some tools can also encode the SMT problem in a format            LOOP             ?                ?
suitable for sending to an interactive proof assistant such as    JACK             ?                ?
Isabelle/HOL [29] or Coq [1]. KeY[6] comes with its own in-       TACO             Difficult        Very Easy
teractive proof environment. These tools can still send proof     Sireum/Kiasan    Difficult        Easy
obligations to an automated solver, but when the attempt          ESC/Java2        Very Difficult   ?
fails they allow the user to try completing the proof inter-      OpenJML          Difficult        Average
actively. We thus refer to them as Automated/Interactive          KeY              Average          Very Difficult
SMT tools.                                                        Krakatoa         Very Difficult   Easy

1.4.5 Embedding in a theorem prover
It is also possible to port the entire program to the na-        Available Was the tool available for download?
tive language of Isabelle/HOL or Coq, and prove statements       Maintained Are the tool’s developers still involved, or has
about this version. Several Java programs have been verified         it been abandoned?
in this way [28, 12]. This gives maximum proving power, but
potentially sacrifices the ease of the automated tools. There    Type The type of tool: BMC (Bounded Model Checker),
is also no guarantee that the Isabelle/HOL version of the            A-SMT (Automated SMT solver), A/I-SMT (Interac-
program accurately captures all the semantics of the source          tive SMT solver).
language (e.g. integer overflows). The approach of seL4
[26] is similar to this – a separate proof of the behaviour of   Java version An indication of the Java versions supported
a Haskell program, and of the correctness of a C program              by the tool.
with respect to this Haskell specification.                      FP Can the tool reason about floating-point variables?

2.   COMPARISON                                                  \forall Does the tool understand the JML \forall anno-
We first present a side-by-side comparison of several tools,          tation? It is useful for reasoning about arrays.
and then more detailed comments on our experience with
                                                                 \sum Does the tool understand the JML \sum annotation?
each tool. In some cases, we use simple subjective judge-
                                                                     It is useful for proving termination of complex loops.
ments rather than something precise like “man-hours” be-
cause different users are likely to work at different rates.     Setup Subjective judgement of how difficult we found it to
                                                                     install the tool and get it to work.
2.1 Brief comparison
Tables 1, 2 and 3 give an overview of the tools we compared.     Use Subjective judgement of how difficult we found it to
The columns are described below, with “?” meaning that we            use the tool on several toy programs.
could not download the tool or we could not get it to run.
2.2 Detailed observations                                         2.2.7 Krakatoa
2.2.1 LOOP and JACK                                               Krakatoa is the most promising tool of the ones we have
LOOP and JACK seem to have been popular and very promis-          tried. It is built on Why3 [22], a programming language
ing in the early 2000s [7], but LOOP no longer has a website      and toolchain designed for verification. Krakatoa leverages
and JACK’s download links no longer work:                         the existing toolchain to convert Java programs and JML
http://www-sop.inria.fr/everest/soft/Jack/jack.html               annotations into SMT problems, or Coq or Isabelle proof
                                                                  goals. Krakatoa is the only tool we found that can reason
                                                                  correctly about floating point variables. It can treat them as
2.2.2 TACO                                                        mathematical real numbers, or use a third-party Coq library
This tool takes a little effort to set up, but it illustrates     that describes the precise behaviour of IEEE floating point.
the benefits of bounded model checking. It easily proves
(bounded versions of) statements that the more powerful           Within the tool, the user can split proofs into separate obli-
tools struggle with. It does not support floating point arith-    gations. The tool can display which code block each obliga-
metic and knows it, producing an error message:                   tion refers to, and can send them to SMT solvers separately.
http://www.dc.uba.ar/inv/grupos/rfm_folder/TACO                   This produces several benefits. Firstly, if one proof attempt
                                                                  fails and another succeeds, the user knows which aspect of
2.2.3 Sireum/Kiasan                                               the code to focus on. Secondly, users might decide that they
Sireum/Kiasan is another bounded model checker that we            are satisfied with leaving some aspect unproven. The tool
felt was inferior to TACO. It claims to support floating point,   also provides separate goals for e.g. invariant preservation
but in fact does not (it proves the statement 0.0 == 1.0).        and termination, and separate goals for null pointer checks,
It also does not support the \forall annotation, which is         array bounds checks, and integer overflows. Thus, a user can
vital for reasoning about arrays:                                 choose to ignore these error conditions if they wish. Many of
https://code.google.com/archive/p/sireum/                         the other tools allow us to turn off integer overflow checking
                                                                  (for simplicity), but only before beginning the proof.
2.2.4 ESC/Java2
This tool seems to have been popular in its time, but has         Unfortunately, Krakatoa does not support the JML \sum
been superseded by OpenJML. It was difficult to install and       and \max statements. These are very helpful for proving
we were unable to get it to run. Supposedly it can send proof     termination of a loop (as part of the variant that decreases
obligations to Coq, which might elevate it to A/I-SMT sta-        with each loop iteration). However, Krakatoa does techni-
tus (OpenJML cannot do this at the present time):                 cally allow the inductive definition of complex logical func-
http://kindsoftware.com/products/opensource/ESCJava2/             tions (which are converted directly into Coq functions), so
                                                                  the sum could be defined in this way.
2.2.5 OpenJML                                                     Finally, we found it extraordinarily difficult to actually in-
The state of the art automated SMT tool. We found it              stall Krakatoa. Although the tool is currently ”frozen” while
difficult to get working, but eventually succeeded. Unfor-        the team works on Why3, it gives the appearance of being
tunately, it was not very useful. When attempting a proof,        well maintained. However, the install scripts seem to be
OpenJML sends an SMT problem to a solver. If the solver           broken, and the tool failed to automatically install its de-
fails, it gives up. The only action available afterwards is to    pendencies and Coq libraries. It took much effort to run the
edit loop invariants, in the hope that something will make        tool, but the result was pleasing. We thus decided to use
the prover succeed. For proving simple properties, however,       Krakatoa for our verification task:
OpenJML is quite easy to use. It does not support floating        http://krakatoa.lri.fr/
point and produces an error message:
http://www.openjml.org/
                                                                  3. VERIFICATION
                                                                  The Java program we verified is available at:
2.2.6 KeY                                                         https://github.com/dmitry-brizhinev/formal-verification.
KeY is the most prominent interactive tool for Java verifica-     It is a simple genetic algorithm that investigates different
tion. It has its own interactive proof environment, and sup-      deterrence strategies in international conflict. This compu-
ports sending proof obligations to SMT solvers. However,          tational model may be the subject of a future paper.
we found it extremely difficult to accomplish anything in
the tool. The documentation was several years (and several        3.1 Computational modelling
major versions) out of date. We were not able to actually
                                                                  Computational modelling in the sciences involves running a
launch an SMT solver from within KeY. We also could not
                                                                  simulation of some kind of system and observing the results.
introduce a lemma in the interactive environment. KeY had
                                                                  If the assumptions that went into the system hold in the real
patchy support for some JML features – in particular, we
                                                                  world, it is hoped that any insights gained from observing
did not know how to specify that some element of an array
                                                                  it will carry over to an understanding of the real-world phe-
is not modified in a loop body. Finally, KeY has a floating
                                                                  nomena of interest.
point option of questionable utility, unable as it is to prove
that 0.0 == 0.0:
                                                                  The functional correctness of such models is an issue not
http://www.key-project.org/
                                                                  often addressed. If a model with assumptions X produces
                                                                  output Y, we want to be confident that it is the dynam-
                                                                  ics of the model that led to Y, not a bug. However, since
                                                                  the desired output of the model is unknown, such bugs are
often not obvious, and it is not necessarily possible to con-    3.4 Result
struct test cases. Indeed, the model may produce output          The correctness and safety of the model was mostly proven.
that the experimenter expects, and thus incorrectly confirm      We did not find any errors. There are three gaps (unfulfilled
their preconceptions, due to a bug. Formal methods are a         obligations) in the proof.
natural solution to this problem.
                                                                 Firstly, although Krakatoa correctly adds the values of static
3.2 Specification                                                final int constants as assumptions, it ignores the values of
The first step in formally verifying a piece of software is to   static final double ones. Thus, the value of one constant
specify its behaviour in an appropriate form. The verifica-      had to be added as a precondition to the main method for
tion process then provides a proof that the program’s real       the proof to succeed.
behaviour adheres to the specification.
                                                                 Secondly, Krakatoa provides very little to work with upon
Unfortunately, the program in question relies heavily on ran-    entering an object constructor. It is impossible to prove that
dom numbers. Thus, an ideal specification would need to          the new object being constructed is not equal to any other
express statements such as this function correctly calculates    object already in existence. This thus remains an unproven
the expected value of this random variable. As it stands, the    assertion in the program. It is not true in general (if the ob-
Java Modelling Language provides no means to reason about        ject has a superclass, the superclass constructor may have
random numbers, so the best specification of the function’s      already assigned the object to something else in the environ-
behaviour is the code itself. When no separate specifica-        ment), Krakatoa simply does not provide any assumptions
tion is possible, formal verification adds no value. Instead,    that would allow one to prove the statement even in specific
the verification effort focused on proving that no exceptions    cases where it is true. Notably, the software includes a few
could be raised during execution, and on a few basic asser-      test cases for situations akin to this, but the test cases are
tions (such as: that the expected value of an event with two     very weak – Krakatoa would fail to prove almost anything
possible outcomes is somewhere between the outcomes).            more complicated than those specific cases.

Each function was annotated with pre- and post-conditions        Finally, Krakatoa is unable to prove that System.out !=
that ensured all objects and arrays used by the code were        null, which makes it impossible to verify the safety of a
valid at all times. There were also a few assertions ensuring    print statement.
that the output values of functions were reasonable.
                                                                 All other proof obligations generated by Krakatoa have been
Full verification of this kind requires the use of appropriate   proven. 506 out of 512 were completed automatically, us-
loop invariants. These were added as they became necessary       ing CVC4 and Z3. Interestingly, the tools complemented
during the course of the proof.                                  each other. Some goals that Z3 could not prove were easily
                                                                 discharged by CVC4, and vice-versa. Only six goals were
                                                                 completed manually in Coq.
3.3 Workflow
The Krakatoa tool takes a Java source file annotated with        There are three instances of a loop invariant with an exis-
JML assertions and produces a list of Why3 obligations. The      tential quantifier. The automated provers were unable to
Why3 tool then provides an interface for proving these obli-     prove that the invariant holds initially. The proof is triv-
gations. It can perform some basic manipulations (such as        ially completed with two lines in Coq - first, specifying an
splitting an obligation into parts), send obligations to auto-   appropriate value, and then using the auto tactic.
mated provers (such as the SMT solvers CVC4, Z3, Simplify,
and Yices), or create proof scripts for interactive provers      There is one complex inequality – the property of the ex-
(such as Coq or Isabelle). Why3 also makes an effort to dis-     pected value calculation mentioned earlier. This requires a
play which line of Java code each obligation refers to, which    quite involved Coq proof of about 120 lines.
assertion (or safety property) it is checking, and which as-
sertions it includes as assumptions.                             Finally, there was a function with a fairly complex loop
                                                                 invariant that the automated provers could not quite ver-
Verifying code using Krakatoa is a trial-and-error process.      ify. There are two goals, for the two possible outcomes of a
The initial JML annotations are unlikely to be sufficient.       branch within the loop. Each goal requires a fairly simple
Having observed the proof goals generated by the tool, and       Coq proof, of about 15 lines. We present one of these proofs
which of them the automated provers cannot solve, one re-        as an example in Appendix C.
turns to the code and adds annotations as necessary. There
is a lot of boilerplate in the final product. For example,       The result is some confidence that the code is free from bugs.
many functions come with post-conditions guaranteeing that       Unfortunately, this guarantee rests on the assumption that
the function does not deallocate the objects it works with.      Krakatoa has no soundness errors. As discussed below, this
Sometimes a proof goal is out of reach of the automated          assumption is not as safe as one would like.
provers but can be discharged interactively in Coq. Most of
the time, however, an attempt at a proof in Coq simply il-       Additionally, Krakatoa models floating-point variables as
lustrates which assumptions are missing. Once the relevant       mathematical real numbers, so there are no guarantees about
assertions are added, the automated prover succeeds.             floating-point overflow or rounding. This model is still su-
                                                                 perior to anything provided by other Java tools.
Finally, through a special annotation, we instructed Kraka-      when we cannot complete a proof. However, we would not
toa to ignore integer overflow. This made the proving pro-       notice if one of Krakatoa’s premises was unsound – a proof
cess much simpler, but is another source of potential un-        of something we believe to be true would simply succeed
soundness. In particular, the model would overflow if it is      where it should not. Thus, a formal verification tool with
allowed to run for enough cycles, but it generally does not      completeness errors gives far less confidence than it should
run that long.                                                   in the soundness of the proof it produces.

4.   POTENTIAL FOR IMPROVEMENT                                   4.3 Floating point support
We believe that wider adoption of formal methods is de-          IEEE floating point arithmetic is complicated, and it is un-
sirable, because it would improve the quality of software.       surprising that most of the tools do not support it. How-
For this to happen, the tools need to become easier to use;      ever, most scientific computing uses floating point arith-
both so that existing users could apply formal methods more      metic. Hence, in the context of verifying a computational
widely, and to make them accessible to a greater population.     model, floating point support is essential. Modelling float-
Based on our experience with Krakatoa, we have identified        ing point variables as real numbers is not ideal, but is better
several areas in which we think more work would be particu-      than nothing. We see this shortcut as being akin to ignoring
larly fruitful. We note that our list does not include improv-   integer overflow – it may be an acceptable approximation,
ing the power of automated SMT solvers, which would ini-         as long as we are aware of its limitations.
tially seem the most obvious approach to making machine-
assisted proof work easier.                                      Much worse than a lack of floating point support is fake
                                                                 support. While TACO produced error messages informing
                                                                 us that it did not support floating point, Sireum/Kiasan and
4.1 Maintenance                                                  KeY claimed that they did. However, Sireum/Kiasan proved
Many of these tools surveyed appear to be academic projects      the false statement that 0.0 == 1.0, and KeY was unable
that were created and then abandoned. Some, like LOOP            to prove that 0.0 == 0.0. While x = x is not a theorem for
and JACK, are no longer accessible. Others do not sup-           IEEE floating points (NaN 6= NaN), a special case like that
port recent versions of Java. Installing old versions of Java    should be provable if their behaviour is adequately modelled.
is not only an extra burden during setup, it is also a secu-     A tool that cannot prove such a triviality is no better than
rity risk. Most tools were unexpectedly difficult to set up.     one that does not support floating point arithmetic at all.
Many of them had undocumented dependencies or broken
install packages. They often produced unhelpful error mes-       4.4 Error messages
sages when their dependencies were not satisfied. Finally,       Even before reaching the proving stage, many of the tools
documentation was either lacking, incomplete, or severely        surveyed failed to parse Java source or *.class files with
outdated. We could not complete our proof in Krakatoa un-        unhelpful error messages. Syntax error on line X is bad
til we looked at the developers’ test cases, which showcased     (especially when the correct syntax is undocumented), but
several undocumented annotations.                                assertion failure in parser is even worse. Widely used com-
                                                                 pilers have become adept at explaining their reasons for fail-
If a hypothetical researcher wishes to create a tool that peo-   ure, and formal verification tools should also aim to do so.
ple will actually use, we recommend that they plan ahead
to make sure they can document its features, and provide
some rudimentary maintenance in the future. This does not
                                                                 4.5 Comprehensible proof goals
                                                                 By the end of the process, we discovered that automated
mean supporting every new Java construct as it appears,
                                                                 SMT solvers could prove almost all of the statements of in-
but it would be an enormous improvement if the tools could
                                                                 terest about our program. However, this was only after a
at least parse more recent Java *.class files and provide
                                                                 long time spent adjusting the JML annotations. At the be-
precise error messages about unsupported features of Java.
                                                                 ginning of the process, it seemed that automated tools were
                                                                 hopelessly inadequate, and that better solvers or interactive
4.2 Bugs                                                         provers were necessary. This can create the illusion that
Krakatoa was the only tool we used for long enough to no-        more progress in automated proving is needed to make for-
tice actual bugs in the program. Besides a slew of Java          mal methods more accessible. But it is our opinion that two
features that the tool did not support and which elicited ob-    completely different factors are crucial. The first is reason-
scure error messages, there were several of what we would        ing about missing assumptions, which we discuss in the next
call completeness errors, where Krakatoa did not provide         section. The other is comprehensible proof goals.
enough assumptions to prove true statements. An exam-
ple is Krakatoa’s treatment of class invariants. For each        By comprehensible goals we mean that formal verification
class invariant, Krakatoa generates pre- and post-conditions     tools today do little to help the user understand the details
for each of the class’s functions. It also generates appro-      of the formal logical statement they are trying to prove. This
priate pre-conditions as assumptions to functions that take      statement is the result of a complex transformation process
elements of the class as parameters. However, Krakatoa does      peculiar to each tool, and may be very different from what
not assume that elements of an array satisfy the invariant.      the user expects based on the source code they are working
Thus, we had to manually add and prove the assertion that        with. Often, understanding the proof goal is enough to see
all elements of an array were valid at all times.                which annotations need to be changed.

Completeness errors are not as bad as soundness errors, but      The most incomprehensible goals come from the fully au-
their presence is a bad sign. Completeness errors stand out      tomated tools like OpenJML. These tools opaquely convert
annotations into proof goals, send them to SMT solvers, and         5. CONCLUSION
fail. Because the user cannot see the unprovable goal, they         Tools for formal verification of Java programs are in gener-
do not know why the proof failed. Appendix A gives an               ally poor shape, and do not support recent versions of Java.
example of a mistake that may trip up novices, and which            Nonetheless, they do exist, and are usable enough to verify
tools should be able to prevent.                                    a program. SMT solvers are powerful enough to prove most
                                                                    true statements of interest; the most difficult aspect of veri-
Some tools do display their proof goals. The interactive            fication was, in our experience, finding the right annotations
tools, KeY and Krakatoa, provide a full proof script that           to use to ensure the provers had enough assumptions to work
the user can examine. This is an improvement, as it often           with. We believe wider adoption of formal methods would
becomes clearer why a proof is failing once one has inves-          be beneficial, and making the tools more user-friendly will
tigated the obligation closely, and perhaps even attempted          bring about this goal. Existing tools could use better doc-
an interactive proof. However, it is not ideal, because the         umentation, error messages, and fewer bugs. We also think
language in which the proof goal is expressed is very far           a large usability gain is waiting to be realised by tools that
removed from the Java code it is based on, and important            can clearly relate the proof goals they generate to the source
details are often obscured by copious boilerplate.                  code the user is working with, and that can suggest missing
                                                                    assumptions to the user that would make a proof succeed.
We feel that making an effort to explain proof goals to
the user in terms of the code they are working with would
make the tools enormously more accessible. This means ex-           6. REFERENCES
pressing the statements being proved not in terms of com-            [1] The Coq Proof Assistant. https://coq.inria.fr/.
plex mangled names for constructs from the tool’s memory             [2] The RedMonk Programming Language Rankings:
model, but in terms of Java objects, and lines of Java code.             January 2016.
In Appendix B we include an example of what this would                   http://redmonk.com/sogrady/2016/02/19/language-rankings-1-1
look like in our ideal world.                                            Accessed: 2016-08-02.
                                                                     [3] TIOBE Index for July 2016.
4.6 Inferring missing assumptions                                        http://www.tiobe.com/tiobe-index/. Accessed:
As mentioned earlier, most of our program was successfully               2016-08-02.
verified with automated tools, but only after a long pro-            [4] C. Barrett, C. L. Conway, M. Deters, L. Hadarean,
cess of editing the annotations. Most of these edits involved            D. Jovanović, T. King, A. Reynolds, and C. Tinelli.
adding assumptions that were missing from the proof goal,                CVC4. In International Conference on Computer
such as function pre-conditions and loop invariants. We                  Aided Verification. Springer, 2011.
added them after looking closely at the generated proof goal,        [5] C. W. Barrett, R. Sebastiani, S. A. Seshia, and
or attempting an interactive proof and discovering the miss-             C. Tinelli. Satisfiability modulo theories. Handbook of
ing hypothesis. This bears repeating: the vast majority of               satisfiability, 185, 2009.
the statements that the SMT solvers could not prove were in          [6] B. Beckert, R. Hähnle, and P. H. Schmitt. Verification
fact false. More precisely, they were true when expressed as             of object-oriented software: The KeY approach.
JML assertions, but the proof obligations generated by the               Springer-Verlag, 2007.
tool were false, as they lacked information not captured by          [7] L. Burdy, Y. Cheon, D. R. Cok, M. D. Ernst, J. R.
the annotations. The main barrier to completing the proof                Kiniry, G. T. Leavens, K. R. M. Leino, and E. Poll.
automatically was not the power of the provers, but inade-               An overview of JML tools and applications.
quate annotations. We present an example in appendix B.                  International journal on software tools for technology
                                                                         transfer, 7(3), 2005.
With SMT solvers doing the proving, most of our effort was           [8] L. Burdy and A. Requet. JACK: Java applet
spent on inferring which assumptions were missing from our               correctness kit. In Proceedings, 4th Gemplus Developer
JML annotations. Thus, we believe the greatest potential                 Conference, Singapore, 2002.
for making formal verification more user friendly is in find-        [9] T. Bylander, D. Allemang, M. C. Tanner, and J. R.
ing ways to automatically answer the question which extra                Josephson. The computational complexity of
assumptions would make this goal true? This is the prob-                 abduction. Artificial intelligence, 49(1), 1991.
lem referred to as abduction [9], and we suffer no illusions
                                                                    [10] C. Calcagno, D. Distefano, J. Dubreil, D. Gabi,
as to its difficulty. Abductive reasoning has been studied in
logic [25], philosophy [20] and artificial intelligence [32] as a        P. Hooimeijer, M. Luca, P. OâĂŹHearn,
means of inferring the cause of an event. Some such capa-                I. Papakonstantinou, J. Purbrick, and D. Rodriguez.
bility added to formal verification tools might allow them to            Moving fast with software verification. In NASA
make suggestions for extra annotations. Appendix B con-                  Formal Methods Symposium. Springer, 2015.
tains a concrete example.                                           [11] S. Cass. The 2015 top ten programming languages.
                                                                         IEEE Spectrum, July, 20, 2015.
We are aware of one static analysis tool, Facebook’s INFER          [12] P. Chalin, P. R. James, and G. Karabotsos. Using
[10], that uses a form of abduction. The INFER tool checks               isabelle/hol for static program verification in jml4.
several common error conditions such as null pointer deref-              Proceedings of TPHOLs: Emerging Trends, 2008.
erences, and does not require any annotations, because it           [13] E. M. Clarke, O. Grumberg, and D. Peled. Model
infers pre- and post-conditions automatically. We have not               checking. MIT press, 1999.
investigated INFER in this paper because it does not verify         [14] D. R. Cok. Openjml: JML for Java 7 by extending
user-specified post-conditions or assertions.                            OpenJDK. In NASA Formal Methods Symposium.
     Springer, 2011.                                            [31] J. Van Den Berg and B. Jacobs. The LOOP compiler
[15] D. R. Cok and J. R. Kiniry. ESC/Java2: Uniting                  for Java and JML. In International Conference on
     ESC/Java and JML. In International Workshop on                  Tools and Algorithms for the Construction and
     Construction and Analysis of Safe, Secure, and                  Analysis of Systems. Springer, 2001.
     Interoperable Smart Devices. Springer, 2004.               [32] B. Van Nuffelen. A-system: Problem solving through
[16] L. De Moura and N. Bjørner. Z3: An efficient SMT                abduction. In BNAIC, volume 1. Citeseer, 2001.
     solver. In International conference on Tools and
     Algorithms for the Construction and Analysis of
     Systems. Springer, 2008.
[17] X. Deng, J. Hatcliff, et al. Kiasan: a verification and
     test-case generation framework for Java based on
     symbolic execution. In Second International
     Symposium on Leveraging Applications of Formal
     Methods, Verification and Validation. IEEE, 2006.
[18] D. Detlefs, G. Nelson, and J. B. Saxe. Simplify: a
     theorem prover for program checking. Journal of the
     ACM (JACM), 52(3), 2005.
[19] B. Dutertre and L. De Moura. The Yices SMT solver.
     Tool paper at http://yices. csl. sri. com/tool-paper.
     pdf, 2(2), 2006.
[20] K. T. Fann. PeirceâĂŹs theory of abduction. Springer
     Science & Business Media, 2012.
[21] J.-C. Filliâtre and C. Marché. The
     Why/Krakatoa/Caduceus platform for deductive
     program verification. In International Conference on
     Computer Aided Verification. Springer, 2007.
[22] J.-C. Filliâtre and A. Paskevich. Why3 – where
     programs meet provers. In European Symposium on
     Programming. Springer, 2013.
[23] L. Fix. Fifteen years of formal property verification in
     intel. In 25 Years of Model Checking: History,
     Achievements, Perspectives. Springer, 2008.
[24] J. P. Galeotti, N. Rosner, C. G. López Pombo, and
     M. F. Frias. Analysis of invariants for efficient
     bounded verification. In Proceedings of the 19th
     international symposium on Software testing and
     analysis. ACM, 2010.
[25] A. C. Kakas, R. A. Kowalski, and F. Toni. The role of
     abduction in logic programming. Handbook of logic in
     artificial intelligence and logic programming, 5, 1998.
[26] G. Klein, K. Elphinstone, G. Heiser, J. Andronick,
     D. Cock, P. Derrin, D. Elkaduwe, K. Engelhardt,
     R. Kolanski, M. Norrish, et al. seL4: Formal
     verification of an OS kernel. In Proceedings of the
     ACM SIGOPS 22nd symposium on Operating systems
     principles. ACM, 2009.
[27] G. T. Leavens, A. L. Baker, and C. Ruby. JML: A
     notation for detailed design. In Behavioral
     specifications of Businesses and Systems. Springer,
     1999.
[28] H. Liu and J. S. Moore. Java program verification via
     a JVM deep embedding in ACL2. In International
     Conference on Theorem Proving in Higher Order
     Logics. Springer, 2004.
[29] T. Nipkow, L. C. Paulson, and M. Wenzel.
     Isabelle/HOL: a proof assistant for higher-order logic,
     volume 2283. Springer Science & Business Media,
     2002.
[30] J. M. Rushby and F. von Henke. Formal verification of
     algorithms for critical systems. IEEE Transactions on
     Software Engineering, 19(1), 1993.
APPENDIX
A. PROOF GOAL EXAMPLE                                           (Jessie_memory_model.offset_max
When proof goals are opaque, there is no way to know if           usObject_alloc_table1
an SMT solver’s failure was because the statement is false,         (Jessie_memory_model.select
because the statement is very very difficult, or because the          usField object)) + 1 = 10
assumptions need a trivial strengthening. For example, the
SMT tools could not automatically prove that the code be-
low would not cause an ArrayIndexOutOfBoundsException:          It takes experience with Krakatoa to understand this. The
                                                                small change in usObject_alloc_table is the culprit. The
                                                                statement expresses the proposition
//@ invariant (\forall int j;
                0 <= j < i ==> array[j] == 0);
for(int i = 0; i < array.length; i++)                           object.field.length == 10
    array[i] = 0;
                                                                More specifically, the goal is to prove that the array still has
                                                                the same length as it did earlier. Because the doNothing()
The solution is to add 0 <= i <= array.length to the in-        function is not annotated, Krakatoa will not make any as-
variant. Those experienced in formal methods will see this      sumptions about the value of fields after it is called. Thus,
immediately, but novices may be baffled by the tools’ inabil-   it is impossible to prove anything about their value. To fix
ity to prove simple statements.                                 this, we should annotate doNothing() with details about
                                                                which fields it changes, and which fields remain the same.
If the tool showed the user the proof goal, along with its
assumptions, they should be able to spot the error quickly.     Ideally, when this proof fails, the prover should report that
                                                                it needs the extra assumption
B.    MISSING ASSUMPTION EXAMPLE
A prover that could report I could complete this proof, if      (Jessie_memory_model.offset_max
only I knew that P holds, would represent an enormous us-         usObject_alloc_table
ability improvement. We present here a simple example of            (Jessie_memory_model.select
the obscurity of the proof goals generated by Krakatoa, and           usField object))
of the kind of suggestion we would like to see from an ideal    = (Jessie_memory_model.offset_max
prover with abductive reasoning capability.                         usObject_alloc_table1
                                                                      (Jessie_memory_model.select
The following code:                                                     usField object)).


class Example {                                                 Even better, the tool should be able to relate this to ac-
  int[] field;                                                  tual Java code, and report something like I cannot prove
                                                                that object.field.length at line 9 of the file is equal to
    void doNothing() {                                          object.field.length at line 11.
      return;
    }
                                                                C.    COQ PROOF EXAMPLE
    static void func(Example object) {                          This is an example of the short Coq proof for one of the loop
      object.field = new int[10];                               invariants. This is the loop in question, edited for clarity:
      object.doNothing();
      //@ assert object.field.length == 10;
                                                                int best = 0;
    }
                                                                /*@
}
                                                                loop_invariant
                                                                (\forall int j; 0 <= j < h ==>
Would produce a long and complicated proof goal filled with       expectedValue(j) <= expectedValue(best))
boilerplate, which no SMT solver will prove. But somewhere      @*/
in there would be something like this:                          for (int h = 1; h < ATTACK_TYPES; h++) {
                                                                  if (expectedValue(h) > expectedValue(best))
                                                                    best = h;
Axiom:                                                          }

(Jessie_memory_model.offset_max
  usObject_alloc_table                                          The invariant produces three obligations. One to prove that
    (Jessie_memory_model.select                                 it holds initially, and one to prove that it holds after exe-
      usField object)) + 1 = 10                                 cuting the body where the if block is not entered, and one
                                                                where the block is entered. We present the third of these,
Proof Goal:                                                     where the block is entered.
The proof script itself is the file ending in
...highestExpectedValue_ensures_default_5.v
in the git repository https://github.com/dmitry-brizhinev/formal-verification.
It contains copious amounts of boilerplate. We present here
a version heavily edited for conciseness and clarity:


Variable j:Z, h’:Z, h:Z, best_old:Z, best_new:Z

Premise p1: forall (j’:Z), (0 <= j’ < h’)
     expectedValue j’ <= expectedValue best_old
Premise p2: expectedValue best_old < expectedValue h’
Premise p3: best_new = h’
Premise p4: h = h’ + 1
Premise p5: 0 <= j < h

Goal: expectedValue j <= expectedValue best_new

Proof:
rewrite p3.
cut (0 <= j < h’ \/ j = h’).
intro.
destruct H.
cut (expectedValue j <= expectedValue best_old).
intro.
apply Rle_trans with (r2 := expectedValue best_old).
trivial.
auto with *.
auto.
rewrite H.
auto with *.
omega.
Qed.


The key elements of the proof are:

  1. The first cut, splitting the proof into the cases j < h’
     and j = h’.
  2. Destruct, which considers the two cases separately.
  3. The second cut, which instantiates premise p1 with j’
     = j.
  4. The use of the transitivity of less-than, which connects
     premises p1 and p2
  5. Omega, which automatically solves some inequalities.
