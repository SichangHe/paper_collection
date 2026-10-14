                                             Guiding LLM Temporal Logic Generation with
                                                Explicit Separation of Data and Control

                                              William Murphy, Nikolaus Holzer1 , Nathan Koenig1 , Leyi Cui2 , Raven
                                                       Rothkopf2 , Feitong Qiao1 , and Mark Santolucito2
                                                               1
                                                                 Columbia University, New York NY, USA
                                                     2
                                                         Barnard College, Columbia University, New York NY, USA
arXiv:2406.07400v1 [cs.LG] 11 Jun 2024




                                                Abstract. Temporal logics are powerful tools that are widely used for
                                                the synthesis and verification of reactive systems. The recent progress on
                                                Large Language Models (LLMs) has the potential to make the process of
                                                writing such specifications more accessible. However, writing specifica-
                                                tions in temporal logics remains challenging for all but the most expert
                                                users. A key question in using LLMs for temporal logic specification en-
                                                gineering is to understand what kind of guidance is most helpful to the
                                                LLM and the users to easily produce specifications. Looking specifically
                                                at the problem of reactive program synthesis, we explore the impact of
                                                providing an LLM with guidance on the separation of control and data–
                                                making explicit for the LLM what functionality is relevant for the spec-
                                                ification, and treating the remaining functionality as an implementation
                                                detail for a series of pre-defined functions and predicates. We present a
                                                benchmark set and find that this separation of concerns improves speci-
                                                fication generation. Our benchmark provides a test set against which to
                                                verify future work in LLM generation of temporal logic specifications.

                                                Keywords: Reactive Program Synthesis · Large Language Models ·
                                                Temporal Stream Logic · Code generation


                                         1    Introduction

                                         Linear temporal logic has proven useful in improving the safety and scalabil-
                                         ity of a variety of systems. It allows an author to specify formal, mathematical
                                         constraints on the behavior of a system, and programs to be generated or ver-
                                         ified against it. This has allowed programs to be generated that would be too
                                         complex for maintainers directly to understand, and has allowed systems to pro-
                                         vide mathematical guarantees in high-stakes environments. Adoption of linear
                                         temporal logic has been limited by the difficulty of composing specifications. In
                                         many cases, the specification is much easier to write than the generated program;
                                         however, we believe the specification can be made even easier. Large Language
                                         Models (LLMs) have revolutionized both code generation and natural language
                                         understanding (NLU). We propose a strategy to leverage these two strengths
                                         of LLMs in order to allow users to specify systems in natural language rather
                                         than the symbolic language of linear temporal logic. The natural language is
then translated into an LTL specification, which the user can inspect or apply
to further steps in a verification or synthesis pipeline.
   The field of linear temporal logic (LTL), the formal specification of the be-
havior of programs, has seen tremendous progress in recent years. LTL aims
to place logical, mathematically rigorous guarantees on the behavior of a sys-
tem, for the purpose of verifying an existing system or generating a new one.
A primary example of the successful use of LTL is the AMBA bus protocol [1].
Since then, the field has seen significant milestones in education [8], FPGA game
development [5], music [2], and interactive animations [11].
    An important extension of LTL is Temporal Stream Logic (TSL) [4], which
adds to LTL data of arbitrary type (rather than just Boolean) and the notions of
updates, predicates, and functions. TSL can be used to synthesize programs that
satisfy the TSL specification for all possible implementations of the function and
predicate terms. TSL is flexible and powerful, and its precision can be valuable
to high-stakes environments like medicine, energy, transportation, and defense.
However, its rigorous treatment of problems can be abstract to users. TSL’s
notational logic is challenging for less experienced users, and even experienced
users need to devote significant time and careful attention to each application.
The logical specification is also decoupled from the reasoning required for im-
plementing the function and predicate terms. This separation puts the burden
on the user to determine what details about a system are needed to verify its
behavior; by contrast, when a user discusses an example with a colleague, the
problem is usually stated in an informal, natural language way that includes
logical constraints mixed with illustrative details and facts about the implemen-
tation. When it comes to write the TSL spec, the user needs to separate out
these constraints and the TSL spec more closely resembles a mathematical pa-
per, stripped of all commentary and with only the equations. A further avenue
for improvement in TSL is the ease of editing existing specifications. For most
real applications, modifications need to be made after a first version, and pro-
cesses that aids editing for a user, who may not even be the original author, will
greatly increase the value of TSL. Moreover, many TSL specifications take place
in the same domain, using the same hardware, function implementations, and
conceptual constructs. These domain-specific TSLs would benefit from reusable
frameworks that capture the semantics of the target domain.
    In 2023, LLMs were used by 92% of U.S.-based developers in writing code.
Previous work has attempted to leverage LLMs for the generation of tempo-
ral logic specifications [3, 7]; however, we propose to extend this work in two
directions. First, we generate a set of benchmarks using examples of signifi-
cant size and complexity that would be interesting to the community, both as
(1) validation for the practicality of generating real-world specifications, and
as (2) illustrative examples and inspiration for further work. Second, we ap-
ply LLM specification generation to temporal stream logic. We believe that TSL
can enhance generated specifications by providing powerful abstractions to serve
complex domains.


                                        2
    We believe that our pipeline provides a natural and helpful structure to the
TSL specification process. As it stands, TSL specifications, isolated from any
context, are challenging to parse for anyone but the original author. The cur-
rent solution has been to include a variety of unstructured commentary about
the specification, before, after, or interspersed in comments. Our pipeline gives
structure to this context, providing information in a predictable, natural lan-
guage format that is easy for humans to read, and contains enough detail to
define a rigorous specification.
    The core contributions of this paper can be summarized as follows:

1. We improve the usability of TSL specifications by proposing a pipeline that
   leverages LLMs for code generation.
2. We propose a set of benchmarks to test the practicality of this pipeline.
3. We observe LLMs are often able to generate correct specifications, and that
   making explicit the separation of data and control helps to increase the
   accuracy of LLM specification generation.

    In particular, our pipeline makes use of three components, each of which
the user must specify: (1) a short, high-level natural language summary of the
problem (2) a series of constraints on the system, stated in plain English, and
(3) the names and signatures of the function and predicates terms to be used in
the specification. We structured this approach around what we imagined to be
the most natural and human-friendly way to describe a specification, as a paper
or colleague might describe a system before writing a formal specification.


2   Motivating Example

To demonstrate the utility of our method, we will first provide an overview of
the current development process for reactive systems synthesized from Temporal
Stream Logic (TSL) specifications. We then describe how LLMs can be used to
expedite this process by generating implementations for a TSL specification’s
signals, predicates, function terms, and context-specific setup.
    For the sake of this motivating example, imagine we are trying to build a
reactive system that controls ball bouncing from left to right. We can specify the
behavior of this system using TSL, demonstrated in Fig 1. While understanding
the exact semantics of this specification is not necessary for this example, the
high-level functionality is that the ball should bounce back and forth between the
left and right boundaries of the screen. The ball signal captures the position
of the ball at each time step. When the ball reaches the leftmost boundary,
it should moveRight, and when it reaches the rightmost boundary, it should
moveLeft.
    After formalizing the temporal behavior of the reactive system, we can then
synthesize the controller code using our TSL synthesis tool. A synthesized JavaScript
code snippet representing the first state for the ball bouncing system is shown
in Fig 2. The code is a straightforward sequence of if statements with a global


                                        3
     always assume {
         [ ball <- moveLeft ball ] -> X (! rightmost ball ) ;
         [ ball <- moveRight ball ] -> X (! leftmost ball ) ;
         ! ( leftmost ball && rightmost ball ) ;
     }
     always guarantee {
         rightmost ball -> F [ ball <- moveLeft ball ];
         leftmost ball -> F [ ball <- moveRight ball ];
         (! leftmost ball && ! rightmost ball ) ->
              F ([ ball <- moveLeft ball ] || [ ball <- moveRight ball ]) ;
         ( leftmost ball && X (! leftmost ball ) ) -> ((! [ ball <- moveLeft ball ]) W
               rightmost ball ) ;
         ( rightmost ball && X (! rightmost ball ) ) -> ((! [ ball <- moveRight ball ])
               W leftmost ball ) ;
     }



                         Fig. 1: ball.tsl example TSL specification.




1    if (currentState === 0) {
2        if (!leftmost(ball) && rightmost(ball)) {
3            ball = moveLeft(ball)
4            currentState = 1
5        }
6        else if (!leftmost(ball) && !rightmost(ball)) {
7            ball = moveLeft(ball)
8            currentState = 1
9        }
10       else if (leftmost(ball) && !rightmost(ball)) {
11           ball = moveRight(ball)
12           currentState = 2
13       }
14   }




                  Fig. 2: ball.js synthesized code snippet from ball.tsl.




                                                   4
currentState variable, as well as any cell values that are instantiated as global
variables.
    After synthesizing the controller code, we must implement predicates like
leftmost(), rightmost() and function terms like moveLeft(), moveRight(),
as well as the ball signal and the wrapper code for the animation to fully con-
struct the reactive system. The current standard practice is to manually imple-
ment the reactive system as one would normally–as a web-app, for example–and
then refactor the code into pure functions and predicates that support the syn-
thesized controller code. This process is laborious and error-prone, as it requires
developers to understand the synthesized code and the TSL specification to
ensure that the system behaves as expected. Moreover, this process must be re-
peated for every new feature or modification to the TSL specification, making
it difficult to scale the development of reactive systems synthesized from TSL
specifications.

3     Background
What follows is a description of Temporal Stream Logic (TSL) and the TSL syn-
thesis pipeline. We give only basic overview of TSL as it relates to the synthesis
pipeline discussed in Sec. 4 of the paper. For a full exposition of TSL’s formal
background, we refer the reader to prior work [4].

3.1   Reactive synthesis and Temporal Stream Logic (TSL)
The goal of our system is to generate Temporal Stream Logic specifications based
on natural language. These specifications describe systems that are reactive in
the sense that they run in infinite loops, consuming input from the environment
and producing output. In the classical synthesis setting, using specification lan-
guages such as Linear Temporal Logic [10], time is discrete and inputs and out-
puts are given as vectors of Boolean signals. Temporal Stream Logic (TSL) [4] is
a specification language that provides an extra layer of abstraction that can be
applied to input and output values of arbitrary type (as opposed to only Boolean
as in LTL). Specifically, TSL introduces predicate terms, τP ∈ TP , which are used
to make observations on the environment, and function terms, τF ∈ TF , which
are used to construct output values. These predicate terms allow users to sepa-
rate the data and control of a system, encapsulating functionality in functions
and predicates that is irrelevant to the specification, so the specification need
only deal with the parts of the system that need to be understood in order to
provide the desired guarantees. Additionally, TSL introduces the notion of cell
values - values which are outputted by the system and piped back as input in
the following timestep. The grammar of a TSL formula, φ, is an extension to
the grammar of LTL:
             τP   := p τF0 τF1 . . . τFn−1
             τF := si | f τF0 τF1 · · · τFn−1
              φ := τP | [so ↢ τF ] | ¬φ | φ ∧ φ |          φ | φU φ

                                        5
where si ∈ I ∪ C is an input stream or cell value, and so ∈ O ∪ C is an output
stream or cell value. Together, all the available predicate names p and all the
available function names f form the set of function symbols F. A TSL formula
describes a system that consumes input I = I∪C and produces output O = O∪C.


3.2   TSL Synthesis and Universal Quantification

The realizability problem of TSL is stated as: given a TSL formula φ, is there
a strategy σ ∈ I + → O mapping a finite input stream (since the beginning of
time) to an output (at each particular timestep), such that for any infinite input
stream ι ∈ I ω , and every possible interpretation of the function symbols (some
concrete implementation) ⟨·⟩ : F → F, the execution of that strategy over the
input σ≀ ι satisfies φ, i.e.,

              ∃σ ∈ I + → O. ∀ι ∈ I ω . ∀⟨·⟩ : F → F. σ≀ ι, ι ⊨⟨·⟩ φ

If such a strategy σ exists, we say that σ realizes φ. The key insight here is
that in TSL we specify a temporal relation of predicate evaluations to function
applications–abstracting away from what these predicates and functions actually
do to any underlying data. In TSL synthesis, this model σ can be turned into a
block of program code that describes a Mealy machine [9], where the transitions
represent function and predicate terms.
    Critically, TSL separates control from data, meaning that the synthesized
controller code that realizes some TSL specification must be valid for any im-
plementation ⟨·⟩ of the function and predicate terms; data manipulations are
universally quantifiable. The universal quantification of TSL’s function and pred-
icate is particularly well-suited for the context of LLM specification generation.
This separation enables developers to first focus on when their system should
execute certain behaviors, and leave the question of how those behaviors should
be implemented for a later step in the development process. Traditionally, the
control is synthesized from TSL and the data is implemented manually by the
end-user, but we propose to automate both processes using LLMs.


4     System Overview

Our system is a prompt generation pipeline shown in Fig. 3 with an ablation
step to test removing several inputs. The core of the specification generation is
to feed a specification (4.1.4) into a large language model (4.1.5), which then
produces a TSL specification (4.1.6).
    The purpose of our system is to test the impact of including different pieces
of information in the specification generation prompt and observing a change
in the output specification. In particular, we include three important pieces of
information:

1. A high-level, natural language summary of the problem ("NL summary")

                                        6
2. A more detailed, natural language description of the most important as-
   sumptions and guarantees needed in the spec ("NL description")
3. A separation of data and control in the form of function and predicate terms.
   The specification should use these to encapsulate logic not relevant to the
   assumptions and guarantees. ("Functions and predicates")



  NL summary (4.1.1)       NL description (4.1.2)       Funcs and predicates (4.1.3)



                       Spec generation prompt (4.1.4)



                                LLM (4.1.5)



                             TSL Spec (4.1.6)

                  Fig. 3: The specification generation pipeline


    As an example, consider the “bouncing ball” motivating benchmark. Below
are the three inputs included in the prompt. The natural language summary is
quite short, but paints a clear picture for the LLM of the abstractions involved.
It is important to establish a clear metaphor in this “high level summary”, be-
cause the LLM needs to be able to tie keywords together in subsequent natural
language. For example, when we use words like “wall”, “bounce”, “leftmost”, and
“move away”, the LLM will need to translate these natural language descriptions
into a geometric understanding of the situation.


    A ball is bouncing between two walls. The position of the ball can
    be represented as a number between 0 and 10, where 0 represents
    that the ball is against the leftmost wall and 10 represents
    that it is against the rightmost wall.

                        Fig. 4: Natural language summary


   The natural language description is the full description of the problem, after
the summary. Below is an excerpt of the first few lines of a natural language
description for the ball scenario. Here specific assumptions and guarantees are
spelled out, but in plain English using the scenario described in the summary.
When vocabulary is introduced in the summary (e.g. "Ball"), the LLM is capable


                                         7
of connecting vocabulary in the natural language description (e.g. "move away
from") in a consistent abstraction of the scenario. It is not necessary to spell out
what English terms mean, as long as the English terms all describe a consistent
problem that a human reader would find plausible.


    Assumptions:

    1. If the ball is moved to the left, then in the next moment, it is
    guaranteed that the ball is not at the rightmost wall.

    ...


                 Fig. 5: Natural language description (excerpt)


    The third part of the specification is a core contribution of our work. We
separate the data and control of the problem by specifying an abstraction that
the specification will use to encapsulate logic not relevant to the guarantees and
assumptions. Here, we define functions “moveLeft/moveRight” and predicates
“leftmost/rightmost” that move or determine the position of the ball. By defining
these function interfaces, we cause the LLM to treat their logic as an irrelevant
implementation detail, and to focus on the logic necessary for the guarantees.


    Cells:
      "ball" is a cell that represents the state of the signal that
      determines how the ball should move
    Functions:
      moveLeft(ball) => returns a signal to move the ball to the left
      moveRight(ball) => returns a signal to move the ball to the right
    Predicates:
      leftmost(ball) => is the ball against the leftmost wall?
      rightmost(ball) => is the ball against the rightmost wall?

                   Fig. 6: Functions and predicates description




5   Evaluation

In this section, we present an evaluation on the efficacy of separating data and
control for generating TSL specifications with LLMs. We expand upon our mo-
tivating example in Sec 2 by evaluating our approach on a series of benchmarks
we devised for this purpose. This shows when the separation of data and control
improves the specification generation process.


                                         8
5.1    Benchmarks

We evaluated the pipeline on a series of benchmarks designed to test a number
of situations in which data was separated from control. In particular, we ran four
classes of benchmarks, and made three variations on one of the classes (Cube) in
order to test changes to the behavior of the generated program based on different
assumptions and guarantees in the same environment3 . These benchmarks aim
to capture a range of simple reactive systems that describe visual systems.
    We examined the quality of the generated specifications in three ways:

1. How often did the LLM produce a valid specification?
2. How often did the specification accurately model the problem?
3. Given that the specification was correct, how often did it accurately model
   the problem?

    We considered (3) important because it is possible to generate several speci-
fications and automatically detect and exclude malformed specifications. Below
is a table of the results for each of the benchmarks, evaluated according to each
of the three measures of quality.




    Fig. 7: Pipeline accuracy, measured by (1) incidence of valid specification



3
    Our full set of benchmarks is publicly available at https://github.com/
    Barnard-PL-Labs/TSL_LLM_Benchmark


                                        9
  Fig. 8: Pipeline accuracy, measured by (2) incidence of correct specification




Fig. 9: Pipeline accuracy, measured by (3) incidence of correctness given valid
specification


   Our results that the versions of the pipeline that separates data and control
through function terms tended to outperform ones without functions and pred-


                                       10
icates, but not always. The benefit of this separation tended to disappear when
the LLM seemed not to understand the definition of the function and predicate
terms. In particular, the LLM would sometimes treat the function and predicate
terms as though they had a different definition from what we intended, and this
caused problems. For example, in the benchmark "Vending", the LLM misinter-
preted the definition of "isLessThanPoint75", causing it to incorrectly subtract
off negative numbers.
    While further investigation is necessary, these results give initial evidence
that using LLM for temporal specification generation is


6   Related Work
LLM Enabled Code Generation Large Language Models (LLMs) have quickly
moved code generation to tackle problems that were previously far out of scope
for traditional program synthesis techniques [6]. However there is still a need
for software generation that has can provide formal guarantees of correctness.
A key aspect of such guarantees is having formal language descriptions (i.e.
specifications) of software.
    In pursuit of LLM assisted specifciation generation, recent works, such as
NL2spec [3] and Lang2LTL [7], have explored the transformation of natural lan-
guage descriptions into LTL specifications. These approaches aim to bridge the
gap between informal user requirements and formal temporal logic specifications,
enabling a more accessible and intuitive method for defining system behaviors
and properties.
    Further down the pipeline, we might imagine our LLM generated specifica-
tions being used for the automatic generation of systems. Prior work has explored
using reactive synthsis (and TSL specifications specifically) as a method for LLM
content generation [12]. Specifically, Rothkopf et al. explore how reactive syn-
thesis can be leveraged to enforce temporal constraints on content generated by
LLMs.


7   Conclusion
In conclusion, our goal was to test the value of separating control logic and data
for improving LLM generation of temporal logic specifications. We used Tempo-
ral Stream Logic to separate control and data via function and predicate terms,
and we devised a pipeline that incorporated a predefined set of abstractions be-
fore generating the specification. We created a set of benchmarks and performed
an ablation study, removing functions and predicates as well as all natural lan-
guage description except for a high-level summary. Our results indicate that a
clear abstraction improves specification generation, especially when the abstrac-
tion is chosen in such a way that it is easy for the LLM to understand. This
benchmark set provides a useful framework for future work, including problems
hard enough to be useful even after significant improvement in LLM capabili-
ties.

                                       11
References
 1. Bloem, R., Jacobs, S., Khalimov, A.: Parameterized synthesis case study: Amba
    ahb (extended version). arXiv preprint arXiv:1406.7608 (2014)
 2. Choi, W., Vazirani, M., Santolucito, M.: Program synthesis for musicians: A us-
    ability testbed for temporal logic specifications. In: Programming Languages and
    Systems: 19th Asian Symposium, APLAS 2021, Chicago, IL, USA, October 17–18,
    2021, Proceedings 19. pp. 47–61. Springer (2021)
 3. Cosler, M., Hahn, C., Mendoza, D., Schmitt, F., Trippel, C.: nl2spec: Interactively
    translating unstructured natural language to temporal logics with large language
    models. In: International Conference on Computer Aided Verification. pp. 383–396.
    Springer (2023)
 4. Finkbeiner, B., Klein, F., Piskac, R., Santolucito, M.: Temporal stream logic: Syn-
    thesis beyond the bools. In: International Conference on Computer Aided Verifi-
    cation. Springer (2019)
 5. Geier, G., Heim, P., Klein, F., Finkbeiner, B.: Syntroids: Synthesizing a game for
    fpgas using temporal logic specifications. In: 2019 Formal Methods in Computer
    Aided Design (FMCAD). pp. 138–146. IEEE (2019)
 6. Jimenez, C.E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K.:
    Swe-bench: Can language models resolve real-world github issues? arXiv preprint
    arXiv:2310.06770 (2023)
 7. Liu, J.X., Yang, Z., Schornstein, B., Liang, S., Idrees, I., Tellex, S., Shah, A.:
    Lang2ltl: translating natural language commands to temporal specification with
    large language models. In: Workshop on Language and Robotics at CoRL 2022
    (2022)
 8. Ma’ayan, D., Maoz, S.: Using reactive synthesis: An end-to-end exploratory case
    study. In: 2023 IEEE/ACM 45th International Conference on Software Engineering
    (ICSE). pp. 742–754. IEEE (2023)
 9. Mealy, G.H.: A method for synthesizing sequential circuits. The Bell System Tech-
    nical Journal 34(5), 1045–1079 (1955)
10. Pnueli, A.: The temporal logic of programs. In: 18th Annual Symposium on Foun-
    dations of Computer Science (sfcs 1977). pp. 46–57. ieee (1977)
11. Rothkopf, R., Cui, A.L., Zeng, H.T., Sinha, A., Santolucito, M.: Towards the us-
    ability of reactive synthesis: Building blocks of temporal logic. Plateau Workshop
    (2023)
12. Rothkopf, R., Zeng, H.T., Santolucito, M.: Enforcing temporal constraints on gen-
    erative agent behavior with reactive synthesis. arXiv preprint arXiv:2402.16905
    (2024)




                                          12
