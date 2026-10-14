arXiv:2007.02261v5 [cs.LO] 14 Jul 2024




                                            A Framework for Modelling, Verification and
                                         Transformation of Concurrent Imperative Programs




                                                          Maksym Bortin
dedicated to the people of Ukraine
                                  Abstract

This report gives a detailed presentation of a framework, embedded into the
simply typed higher-order logic and aimed to support sound and structured
reasoning upon various properties of models of imperative programs with in-
terleaved computations. As a case study, a model of the Peterson’s mutual
exclusion algorithm will be scrutinised in the course of the report illustrating
applicability of the framework.
                             Acknowledgements

A perception that some research in this direction could be useful emerged when
the author was part of the Trustworthy System group in Sydney, where a soft-
ware system component utilising multiple cores had to be formally modelled and
the intended behaviour verified. In short, an exceptional opportunity to apply
theoretical results fostering computer aided verification of practically relevant
software.
    The bulk of this work (especially concerning liveness reasoning) was sub-
sequently done at the Tallinn University of Technology with support by the
Estonian IT Academy under grant 2014-2020.4.05.19-0001.
Contents

1 Outlining Some Basic Design Decisions                                         5

2 A Generic Concurrent Imperative Language                                      9
  2.1 The syntax . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    9
  2.2 The underlying computational model . . . . . . . . . . . . . . . .       10
  2.3 Programs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   14
  2.4 Potential computations of a program . . . . . . . . . . . . . . . .      15

3 Stepwise Correspondences between Programs                                     17
  3.1 Definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
      3.1.1 Highlighting the fixed point structure . . . . . . . . . . . 19
  3.2 Properties of correspondences . . . . . . . . . . . . . . . . . . . . 20
      3.2.1 Closure properties . . . . . . . . . . . . . . . . . . . . . . 22
  3.3 Sequential normalisation . . . . . . . . . . . . . . . . . . . . . . . 26
  3.4 Replacing conditional and while-statements by jumps . . . . . . . 27

4 Potential Computations and Program Correspondences                      29
  4.1 Conditions on potential computations . . . . . . . . . . . . . . . 29
  4.2 Replaying finite potential computations . . . . . . . . . . . . . . 30
  4.3 A characterisation of the program equivalence . . . . . . . . . . . 32

5 A Hoare-style Rely/Guarantee Program Logic                               35
  5.1 The extended Hoare triples . . . . . . . . . . . . . . . . . . . . . 35
  5.2 The program correspondence rule . . . . . . . . . . . . . . . . . . 36
  5.3 Rules for skip and basic . . . . . . . . . . . . . . . . . . . . . . 38
  5.4 A rule for the parallel composition operator . . . . . . . . . . . . 39
  5.5 A rule for the sequential composition operator . . . . . . . . . . . 43

                                        9
CONTENTS


   5.6   A rule for while-statements . . . . . . . . . . . . . . . . . . . . .    44
   5.7   A rule for await-statements . . . . . . . . . . . . . . . . . . . . .    46
   5.8   A rule for conditional statements . . . . . . . . . . . . . . . . . .    47
   5.9   A brief summary . . . . . . . . . . . . . . . . . . . . . . . . . . .    47

6 Case Study: Peterson’s Mutual Exclusion Algorithm                           49
  6.1 Processing thread aux
                        0   . . . . . . . . . . . . . . . . . . . . . . . . . 54
  6.2 The intermediate result . . . . . . . . . . . . . . . . . . . . . . . 55
  6.3 A rule for mutex . . . . . . . . . . . . . . . . . . . . . . . . . . . 56
  6.4 An application of the mutex rule . . . . . . . . . . . . . . . . . . 57

7 State Relations as Pre- and Postconditions                               61
  7.1 Generalising the extended Hoare triples . . . . . . . . . . . . . . 62
  7.2 Abstracting code fragments . . . . . . . . . . . . . . . . . . . . . 64

8 Case Study: Strengthening the Specification                                67
  8.1 Lifting the mutex rule . . . . . . . . . . . . . . . . . . . . . . . . 67
  8.2 An application of the lifted mutex rule . . . . . . . . . . . . . . . 69

9 Verifying Liveness Properties of Programs                                 71
  9.1 Program positions . . . . . . . . . . . . . . . . . . . . . . . . . . 72
  9.2 Fair computations . . . . . . . . . . . . . . . . . . . . . . . . . . 75
  9.3 A refutational approach to proving liveness properties . . . . . . 77
  9.4 Program correspondences and fair computations . . . . . . . . . 85
  9.5 A brief summary . . . . . . . . . . . . . . . . . . . . . . . . . . . 89

10 Case Study: Proving Termination                                              91
   10.1 Preparations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92
   10.2 The actual refutation . . . . . . . . . . . . . . . . . . . . . . . . . 94
   10.3 Termination of mutex . . . . . . . . . . . . . . . . . . . . . . . . 96

11 Conclusion                                                                  99
   11.1 Fair computations and await-statements . . . . . . . . . . . . . . 100
   11.2 Enhancing the refutational approach . . . . . . . . . . . . . . . . 101
   11.3 Abstraction and granularity . . . . . . . . . . . . . . . . . . . . . 103

Bibliography                                                                     107

Index                                                                            111



                                        10
Introduction

The behaviours of programs running in parallel can become entangled to such an
extent that crucial interferences may easily escape all of thorough code reviews
and tests, leaving although rather rare yet potentially weighty faults undetected.
In situations when for example safe functioning of some nearly invaluable au-
tonomous devices is at stake, providing dependable assurances about the ab-
sence of faults in actions and interactions of the controlling processes can thus
hardly be regarded as dispensable. Such assurances however demand rigorous
verification of the deployed program code which basically cannot pass by formal
modelling with subsequent derivation of the required properties.
    From the specific perspective of safety- and mission-critical software, more
recent standards encourage application of formal modelling and reasoning for
certification of systems with high safety integrity levels. On the other hand,
they also demand to explicitly outline the limits of the chosen method regard-
ing compliance with the actual requirements specification, as the formal meth-
ods supplement [1] to the DO-178C standard [2] particularly stresses. Indeed,
like with outcomes of any other measure, applicability of formally derived con-
clusions to requirements on eventual implementations is bound to a series of
assumptions.
    In comparison to the sequential case, development of concurrent software has
significantly more sources for that. Considering for example some conveniently
structured code such as
       ...
       b = f(a);
       ...
the input/output properties of the invoked function f generally depend on the
properties of concurrently running processes: in the sequential case one can
simply assert that no other process can interfere when f(a) is evaluated drawing
thus further conclusions involving the value of b, but if the assertion is not met

                                        1
CONTENTS


then the variable b may assume quite different values. Besides that, it is a
common practice to rely on a compiler that translates the above fragment to an
assembly level code which shall behave accordingly. By doing so one actually
makes an implicit assumption that pushing a return address as well as the
argument on a stack in preparation to the function call also proceeds without
any interference. In presence of interleaving it is however per se not evident
why another process could not push some different values on the same stack
in between and hence rather hazy to what extent the conclusions concerning
behaviour of the structured code shall be applicable to the outcome of such
compilation.
    To approach these kinds of problems in a cohesive manner, the presented
framework encompasses state abstractions as well as high- and low-level lan-
guage features facilitating structured verification of input/output, invariant and
liveness properties of interleaved computations at various levels of abstraction.
Moreover, as a conservative extension to the simply typed higher-order logic
extended with Hindley-Milner polymorphism, the framework places great em-
phasis on the soundness of the deduced verification methods.
    A sound framework is surely a must as a theoretical foundation but from the
practical point of view, rigorous reasoning with larger models typically requires
an impressive amount of successive applications of various logical rules which
need to be instantiated at each particular step. And this is the point where proof
assistants ultimately become relevant, being capable to accomplish such com-
plex, yet largely mechanisable tasks in a highly reliable and efficient way. Based
on Robin Milner’s [3, 4] influential work, there are tools such as Isabelle 1 [5],
HOL-Light [6] and HOL [7] that provide the assistance, which is particularly
valuable concerning compliance with the mentioned software standards [8].
    Regarding related work, the development essentially leans on the work by
Stirling [9]: starting with the concept of potential computations controlled by
the environment, program, input and output conditions, it systematically ex-
tends the Owicki and Gries method [10] to a Hoare-style rely/guarantee pro-
gram logic for a concurrent while-language. With a few adaptations the notions
from [9] become ubiquitous in what follows. Moreover, the technique combining
deep and shallow embedding with abstraction over the type of program states,
which has been notably applied by Nieto [11] and Schirmer [12], is also at the
core of the presented encoding of the framework’s language in the higher-order
logic, whereas the elegant approach to a light-weight extension of the Hoare-
   1 A version of the presented framework for the Isabelle/HOL prover is available at

https://github.com/maksym-bortin/a framework


                                         2
CONTENTS


style program logic enabling state relations as postconditions has been adopted
from the presentation by van Staden [13] and slightly tuned. More of the related
work will be discussed at the beginning of Chapter 3 and in Chapter 9.
    This report is organised as follows. Next chapter gives brief explanations
for some basic decisions behind the framework’s design. Chapter 2 describes
the framework’s language and the underlying computational model featuring
interleaving and jumps. Chapter 3 is devoted to the notion of program cor-
respondence and its properties. Chapter 4 introduces the relevant conditions
on potential computations, places correspondences in this context and pays
moreover due attention to the special case of program equivalence. Chapter 5
presents a Hoare-style logic and Chapter 6 applies it to derive a rule for estab-
lishing input/output properties of a generic model of Peterson’s mutual exclu-
sion algorithm. Chapter 7 shows how the program logic from Chapter 5 can
be lifted to enable reasoning with state relations as postconditions, whereas
Chapter 8 utilises this extension to strengthen the results of Chapter 6. Based
on a concise notion of fair computations that is elaborated first, Chapter 9 de-
scribes an approach to verification of liveness properties. Essentially all of the
developed techniques will subsequently be applied in Chapter 10 which con-
cludes the case study by proving termination of the mutual exclusion model.
Finally, Chapter 11 concludes the entire presentation outlining most important
enhancements.




                                        3
Chapter 1

Outlining Some Basic
Design Decisions

This small chapter offers a superficial introduction to the framework’s ‘low-level
instructions’ and program transformations involving these. Although reaching
an assembly level representation of a concurrent program does not need to be an
objective of each development process, enabling this option shapes the frame-
work’s design as outlined below. This will be accomplished without delving
into much detail, appealing rather to the intuition that each program can be
transformed to another program that provably does exactly the same but uses
only jumps instead of conditional and while-statements to this end. Based on
this, the claim in what follows will be that any appropriately shaped program
can be brought into a form which is evaluated by the computational model (cf.
Section 2.2) without resorting to instructions unknown to an ordinary assembly
interpreter.
    One of the most striking differences between a structured and an assembly-
level language is that in the former case we can conveniently follow the syntax
tree in order to evaluate a program. For instance, the sequential composition
of some p and q (as usually denoted by p; q) is evaluated by descending to the
subtree p, processing this to some p1 and ‘pasting’ p1 back which ultimately
results in p1 ; q or just q whenever p1 “ skip i.e. the left branch has been com-
pletely evaluated. Placing jumps in this context, the effect of the command
cjump C to i otherwise p end shall be the following: if C holds in the current
state then we proceed to the code ρ i associated to the label i by means of a

                                        5
Outlining Some Basic Design Decisions


‘retrieving’ function ρ and continue with p otherwise. Although this in principle
mimics processing of conditional jumps by assembly interpreters, evaluations
of the sequential composition cjump C to i otherwise p end; q do not: they
would simply advance to the same q once ρ i or p is done with its computations.
Depending on where the code block ρ i is actually placed in the program text,
such behaviour can generally be achieved at the assembly level only when either
p or ρ i concludes with an explicit jump to the entry label of q. These consid-
erations underline that deploying jumps in tree-structured programs demands
certain preparations to make sense from the assembly-level perspective and the
transformations, sketched below, take care of that.

(1a) expressing conditional statements by jumps
A statement if C then p1 else p2 fi can equivalently be evaluated by evaluat-
ing cjump C to i otherwise p1 end instead if we additionally ensure ρ i “ p2
with a fresh label i ( C will denote the complement of the condition C). Ap-
plying this rule straight to a program such as if C then p1 else p2 fi; q yields
cjump C to i otherwise p1 end; q with ρ i “ p2 and hence the issues pointed
out above which are however addressed by the next rule.

(1b) sequential normalisation of conditional statements
Any sequential composition if C then p1 else p2 fi; q can be transformed to
the equivalent if C then p1 ; q else p2 ; q fi distributing essentially all of the
subsequent code to both branches. Applying (1a) to the latter, we consequently
obtain cjump C to i otherwise p1 ; q end with ρ i “ p2 ; q, whose evaluations
do not resort to implicit jumps.

(2a) expressing while-statements by jumps
Attempting to represent the usual syntactic construction while C do p od using
jumps, we simply would not know where to jump when C does not hold: we
need access to the entire syntax tree, e.g. while C do p od; q, to acquire this
information. In response to that the syntax of while-statements gets extended
to while C do p1 subsequently p2 od which by contrast can equivalently be
represented by cjump C to j otherwise p1 ; jump i end with two fresh different
labels i and j, defining additionally a retrieving function
          def
     ρ i “ cjump C to j otherwise p1 ; jump i end

                                        6
         def
and ρ j “ p2 to resolve these.
   It is moreover worth noting that the extra unconditional jump instruction
jump i following p1 opens possibilities for interleaving which are not present
with while C do p1 subsequently p2 od and the according evaluation rule in
Section 2.2 will take accounts of that by means of an exclusively for this purpose
used skip.

(2b) sequential normalisation of extended while-statements
Provided by the extended syntax of while-statements we proceed as in (1b): any
(sub)program of the form while C do p1 subsequently p2 od; q gets replaced
by the equivalent while C do p1 subsequently p2 ; q od.

(3) halting labels for sequential components
Let p1 , . . . , pn be sequential programs that shall run in parallel which is denoted
by kp1 , . . . , pn . Without any significant change to the overall behaviour we
can extend each component pi by the final jump to a fresh ‘halting’ label hi ,
                                            def
i.e. pi ; jump hi defining moreover ρphi q “ skip.
     By successive application of the rules (1b) and (2b) and then (1a) and (2a)
to each pi ; jump hi we eventually obtain kp11 , . . . , p1n together with a retrieving
function ρ that resolves all labels. This outcome can directly be interpreted as n
‘flat’ lists of labelled instructions with essentially the same computational effect
as kp1 , . . . , pn .

Summary
To sum up, this section outlined questions that arise when viewing evaluation of
structured programs with conditional and while-statements replaced by jumps
from the perspective of an assembly interpreter and how these questions are
addressed by the framework. All that will reappear in the following chapters
which by contrast are kept formal.




                                          7
Chapter 2

A Generic Concurrent
Imperative Language

The notions of shallow and deep embeddings arise quite naturally when a lan-
guage needs to be modelled in a formal system such as a proof assistant (cf. [6]).
The technique, notably applied by Nieto [11] and Schirmer [12] aiming to com-
bine the merits of both, will be used in this setting. More precisely, the syntax of
the framework’s language is basically deeply embedded by means of a free con-
struction. However, all indivisible state transformations as well as control flow
conditions (such as the variable C in the conditional and while-statements that
appeared in the preceding chapter) are embedded shallowly or, in other words,
the language is generated over all appropriately typed logical terms so that nei-
ther one-step state updates nor decisions whether e.g. a conditional statement
if C then p else q fi branches to p or to q require any additional evaluations
of language terms.


2.1      The syntax
This is modelled by means of the parameterised type Lα , where α is a type
parameter representing underlying states and L – a type constructor sending
any actual type τ supplied for α to the new type Lτ . For example, Lintˆint
would be an instance with the states carrying two integer variables. Note that
such instantiations will be relevant for specific modellings only, i.e. states remain
abstract at the level of uniform program logical reasoning.

                                         9
A Generic Concurrent Imperative Language


   The terms of type Lα are constructed by the following grammar:

        Lα   ::=   skip
               |   basic f
               |   cjump C to i otherwise Lα end
               |   Lα ; Lα
               |   kL˚α
               |   while C do Lα subsequently Lα od
               |   if C then Lα else Lα fi
               |   await C do Lα od

where

    - i is called a label ranging over the natural numbers (i.e. is of type nat, but
      any infinitely countable set of identifiers, such as strings, may in principle
      be employed here as well)

    - f is called a state transformer ranging over the values of type α ñ α

    - C is called a state predicate ranging accordingly over the values of type
      α ñ bool.

Furthermore, L˚α as usually stands for a finite sequence of elements of type
Lα . So kp1 , p2 , p3 constructs a new value of type Lα out of the three values
of this type. In general, the term kp1 , . . . , pm is called the parallel composition
of pi for 1 ď i ď m. A more convenient and common notation p1 k p2 is used
in place of kp1 , p2 . The reason for having kp1 , . . . , pn as a primitive, instead
of using the binary operator with nesting, will be given later in Section 4.2.
Regarding sequential composition, p1 ; p2 ; p3 will be used as a shorthand for
p1 ; pp2 ; p3 q. Moreover, while C do p subsequently skip od will be abbreviated
by while C do p od whereas await C do skip od – by wait C.
     A term of type Lα is called jump-free if it does not make use of cjump, and
it is called locally sequential if it does not make use of the parallel operator.


2.2      The underlying computational model
Program steps are constructed following the principles of ‘Structural Opera-
tional Semantics’ by Plotkin [14]. Carrying on the state abstraction built into
the language, let α be a fixed arbitrary type throughout this section.

                                         10
2.2. THE UNDERLYING COMPUTATIONAL MODEL


Program steps
In the context of a (code) retrieving function ρ of type nat ñ Lα , the effects
of one program step performed by a term p of type Lα in a state σ of type α
are captured by means of the relation ÑP of type Lα ˆ α ñ Lα ˆ α ñ bool,
connecting thus two configurations: a configuration ζ “ pp, σq comprises

   – the program part p denoted by Ppζq,

   – the state part σ denoted by Spζq.

A skip-configuration has thus the form pskip, σq where σ is some state.
    The notation ρ $ pp, σq ÑP pq, σ 1 q is used from now on to indicate that the
configuration pp, σq can be transformed via ÑP to pq, σ 1 q in the context of ρ.
    The set of possible transformation steps is defined inductively by the rules
listed in Figure 2.1, explained in more detail below.

The rule ‘Basic’ declares how an atomic, i.e. indivisible, computation step can
be performed by a state transformer f . For example, a configuration of the
form pbasicpg ˝ hq, σq can thus atomically be transformed to pskip, gph σqq.
As opposed to that, pbasic h; basic g, σq is at a finer level of granularity since
there is no indivisible step to the same skip-configuration, now reachable by
three program steps.

The rules ‘CJump-True’ and ‘CJump-False’ declare how a conditional jump
is handled in dependence on C. There and throughout this work, σ P C shall
abbreviate C σ “ True (σ R C accordingly). Furthermore, from now on let Jτ
denote the universal predicate on the type τ , i.e. the one which evaluates to True
for any element of type τ , e.g. Jnat is then the set N. For the sake of brevity we
will just write J whenever τ is clear from the context. The unconditional jump
instruction can thus be defined by
             def
      jump i “ cjump J to i otherwise skip end

such that ρ $ pjump i, σq ÑP pρ i, σq follows for any i and σ. Moreover, pρ i, σq
is the only successor of pjump i, σq, i.e. no branching as one would expect.
    It is worth to be once more highlighted that the framework does not impose
any constraints on the branching condition C except its type α ñ bool, whereas
according to the rules its evaluation takes only one step whatsoever, i.e. proceeds
atomically. Although such liberty can be handy in abstract modelling, C shall be

                                        11
A Generic Concurrent Imperative Language




     Basic
                           ρ $ pbasic f, σq ÑP pskip, f σq

                                                σPC
     CJump-True
                           ρ $ pcjump C to i otherwise p end, σq ÑP pρ i, σq

                                               σRC
     CJump-False
                           ρ $ pcjump C to i otherwise p end, σq ÑP pp, σq

                              ρ $ pp1 , σq ÑP pp11 , σ 1 q
     Sequential
                           ρ $ pp1 ; p2 , σq ÑP pp11 ; p2 , σ 1 q

     Sequential-skip
                           ρ $ pskip; p, σq ÑP pp, σq

                             ρ $ ppi , σq ÑP pp1i , σ 1 q       1ďiďm                   mą0
     Parallel
                           ρ $ pkp1 , . . . pi . . . , pm , σq ÑP pkp1 , . . . p1i . . . , pm , σ 1 q

     Parallel-skip
                           ρ $ pkskip, . . . , skip, σq ÑP pskip, σq
                                                             ˚
                             σPC      ρ $ pp, σq ÑP pskip, σ 1 q
     Await
                           ρ $ pawait C do p od, σq ÑP pskip, σ 1 q

                           σPC           x “ while C do p1 subsequently p2 od
     While-True
                                         ρ $ px, σq ÑP pp1 ; skip; x, σq

                           σRC           x “ while C do p1 subsequently p2 od
     While-False
                                            ρ $ px, σq ÑP pp2 , σq

                                             σPC
     Conditional-True
                           ρ $ pif C then p1 else p2 fi, σq ÑP pp1 , σq

                                             σRC
     Conditional-False
                           ρ $ pif C then p1 else p2 fi, σq ÑP pp2 , σq


                  Figure 2.1: Inductive rules for program steps.



                                            12
2.2. THE UNDERLYING COMPUTATIONAL MODEL


instantiated by conditions that can be handled by a single assembly instruction,
e.g. ‘does certain register contain 0?’, when a low-level representation needs to
be eventually reached.

The rule ‘Parallel’ essentially states that a configuration px, σ 1 q is a successor
of pkp1 , . . . pi . . . , pm , σq iff there is some p1i such that pp1i , σ 1 q is a successor
configuration of ppi , σq and x “ kp1 , . . . p1i . . . , pm where 1 ď i ď m. For example
pbasic f1 k basic f2 , σq has thus exactly two successors pskip k basic f2 , f1 σq
and pbasic f1 k skip, f2 σq whereas each of these has in turn only one successor:
pskip k skip, f2 pf1 σqq and pskip k skip, f1 pf2 σqq, respectively.

The rule ‘Parallel-skip’ complements the preceding rule: in cases when all of
the parallel components have terminated, kskip, . . . , skip may terminate in one
step as well. Thus, pbasic f1 k basic f2 , σq reaches either pskip, f2 pf1 σqq or
pskip, f1 pf2 σqq in altogether three program steps.

The rule ‘Await’ states that if σ P C holds and we have an evaluation of p
that starts with σ and terminates by means of n P N consecutive program steps
in some state then await C do p od also terminates in the same state, but by
means of a single indivisible step. Since ÑP is the smallest relation closed under
the rules in Figure 2.1, a configuration pawait C do p od, σq has no successors
when σ R C, i.e. the evaluation is then blocked. Consequently, await J do p od
cannot block an evaluation but creates an atomic section, abbreviated by xpy in
the sequel, which allows us to model behaviours where one parallel component
may force all others to instantly halt their computations until an atomic section
terminates. Taking up the example for the rule ‘Basic’, an atomic section such
as xbasic h; basic gy is computationally in principle the same as basicpg ˝ hq
since for any state σ the configuration pskip, gph σqq is the unique successor for
both, pxbasic h; basic gy, σq and pbasicpg ˝ hq, σq.

The rule ‘While-True’ largely has the standard form, except that it additionally
takes into account the transformation of while-statements to representation us-
ing jumps, sketched in Chapter 1, by means of the extra skip in pp1 ; skip; x, σq
that shall act as a sort of placeholder for a jump in the proof of Proposition 3.4.2.
    This deviation from the usual evaluation approaches is justified as follows.
Three layers can be identified in the framework’s language:
 (a) skip, basic, cjump and the sequential composition form the ‘inner’ layer:
     the computational core,

                                             13
A Generic Concurrent Imperative Language


 (b) the parallel composition and await additionally allow for modelling of
     software systems with controlled interleaving and wait-synchronisation,
     forming the ‘middle’ layer,

 (c) conditional and while-statements form the ‘outer’ layer and additionally
     enable structured programs serving thereby primarily modelling and ver-
     ification purposes.

Hence, in order to validate the computational model one has in principle to
scrutinise the rules in the layers (a) and (b). The presence of while-statements in
the language is on the other hand quintessential for usable program logics only:
for computation they shall be translated to the layer (a), the translation being
a subject to validation too. From this perspective, the behaviour of a while-
statement, determined by the rules ‘While-True’ and ‘While-False’, has in first
place to be provably equivalent to the behaviour of its layer (a) representation.
This, in turn, would not be the case without the extra skip in presence of
interleaving.


Environment steps
Apart from the program steps, the second integral component of the compu-
tational model is the environment which can also perform indivisible steps via
the ÑE relation following the only one rule that pp, σq ÑE pp1 , σ 1 q implies p “ p1
for any p, p1 , σ and σ 1 . That is, an environment step can randomly modify the
state of a configuration leaving its program part unchanged.


2.3      Programs
In line with the computational model, a program is constituted by a pair pρ, pq
where ρ is a code retrieving function and p is a term of type Lα . It should be
clear that with p being jump-free, a program does not actually need a retrieving
function to perform any of its computation steps or, more precisely, performs
the same steps independently of how ρ has been defined. Therefore, retrieving
functions will for the sake of brevity be mostly omitted in these cases such that
a jump-free term of type Lα may particularly be called a (jump-free) program
as well. By contrast, if e.g. jump i occurs in p then there can be two program
steps ρ $ pp, σq ÑP pp1 , σq and ρ1 $ pp, σq ÑP pp2 , σq with different p1 and p2 if
ρ i ‰ ρ1 i holds.

                                         14
2.4. POTENTIAL COMPUTATIONS OF A PROGRAM


    Note that with certain pairs pρ, pq one could achieve something similar to
programs having infinite source code: if p “ jump 0 and ρ i “ jumppi ` 1q holds
for all i P N then pρ, pq in principle corresponds to the ‘program’, written below
as a flat, yet infinite list of labelled instructions
           jump 0
       0 : jump 1
       1 : jump 2
       ...
(that is, each line i : jumppi ` 1q forms a separate block labelled by i) doing
nothing except perpetual jumping forward through the code. Such creations
can be regarded as a byproduct, and in the sequel we will only focus on pairs
pρ, pq that are well-formed. Intuitively, pρ, pq shall be considered well-formed
if all labels that are involved in the process of its evaluation can be statically
computed. Formally, for any p one can first define the finite set Jumps local p
of labels that occur in p. Further, for any set of labels L one can define the set
of its successor labels Nρ pLq by ti P Jumps local pρ jq | j P Lu and consider the
                        def Ť
closure Jumpspρ, pq “ nPN Nρn pJumps local pq. A program pρ, pq is then called
well-formed if the set Jumpspρ, pq is finite.
    Now, if there is some ρ1 that coincides with ρ on the set Jumpspρ, pq then
ρ $ pp, σq ÑP pp1 , σ 1 q entails ρ1 $ pp, σq ÑP pp1 , σ 1 q for any σ, σ 1 and p1 . That
is, ρ can be arbitrarily re-defined on any label i R Jumpspρ, pq without affecting
the evaluation. In particular, if p is jump-free then we have Jumpspρ, pq “ K
for any ρ by the above definition, which once more highlights that p is thus a
well-formed program and the choice of a retrieving function does not matter for
its evaluation.
    Lastly, taking up the question of sequentiality, a program pρ, pq is called
sequential if p is locally sequential and ρ i is moreover locally sequential for any
label i P Jumpspρ, pq. From the above considerations immediately follows that
a jump-free p is sequential iff it is locally sequential, regardless which ρ we take.
Note that program steps retain sequentiality, i.e. ρ $ pp, σq ÑP pp1 , σ 1 q entails
that pρ, p1 q is sequential if pρ, pq is.


2.4      Potential computations of a program
Having defined all possible one-step transformations on configurations, an infi-
nite potential computation sq of a program pρ, pq is a sequence of configurations
sq “ pp0 , σ0 q, pp1 , σ1 q, . . . where p0 “ p and either

                                           15
A Generic Concurrent Imperative Language


  (i) ρ $ ppi , σi q ÑP ppi`1 , σi`1 q or
 (ii) ppi , σi q ÑE ppi`1 , σi`1 q
holds for all i P N. Note that an infinite sequence of configurations is actually
a function of type nat ñ Lα ˆ α and any program has at least one such com-
putation since each type has at least one inhabitant so that some environment
step can always be performed.
     Furthermore, let n |sq and n |sq respectively denote the sequences obtained
by taking the first n P N configurations from sq (a prefix of sq) and by dropping
the first n configurations from sq (a suffix of sq). If sq is an infinite com-
putation and n ą 0 then the prefix n |sq forms a finite potential computation
sq 1 “ pp0 , σ0 q, . . . , ppn´1 , σn´1 q being a list of length n, denoted by |sq 1 |. For
a finite sq the side condition i ă |sq| must be provided when accessing its i-th
configuration, for convenience denoted by sq i . Moreover, the prefix n |sq is also
a finite potential computation whenever 0 ă n ď |sq| holds.
     Similarly, the suffix m |sq of a finite potential computation sq is also a finite
potential computation if m ă |sq| is provided for otherwise m |sq is an empty
list. In case sq is an infinite sequence, m |sq is by contrast one of its infinite
suffixes. The equality m |sq i “ sq i`m , i.e. the i-th configuration of the suffix is
the pi ` mq-th configuration of the original sequence, holds for any sq, m and i
with the side condition i ` m ă |sq| for finite sq.
     When the last configuration of a finite computation sq coincides with the first
configuration of sq 1 then we can compose the computation sq ’ sq 1 as follows.
We take the suffix 1 |sq 1 and attach it to sq using the first transition of sq 1 .
Thus, for any i we have psq ’ sq 1 qi “ sq i if i ă |sq| and psq ’ sq 1 qi “ sq 1i´|sq|`1
otherwise. Note that i ă |sq| ` |sq 1 | ´ 1 (i.e. i ă |sq ’ sq 1 |) must additionally
be provided in the latter case if sq 1 is finite.
     From now on, vpwω        ρ and vpwρ will respectively denote the sets of all infinite
and finite potential computations of pρ, pq. Since computation steps of a jump-
free p do not depend on the choice of ρ, we will just write vpwω and vpw in such
cases.
     Next chapter is devoted to program correspondences: a structured generic
approach to semantic relations between programs.




                                            16
Chapter 3

Stepwise Correspondences
between Programs

Potential computations of a program can be viewed as a transition graph having
configurations as vertices and atomic actions as edges with two different labels:
one for the program steps and one for the environment steps. Correspondences
will allow us to systematically compare the transition graphs generated by pro-
grams, i.e. their behaviour. This in particular covers the question whether two
programs behave in essentially the same way so that they also exhibit the same
relevant properties and can thus be regarded as equivalent. For example the
transformations replacing while-statements by jumps are supposed to result in
an equivalent program.
    In presence of interleaved actions even seemingly plain modifications to a
model may produce significant behaviour deviations so that reasoning demands
very fine-grained equivalences. In the context of concurrency theory, the most
commonly used equivalence relation on various sorts of labelled transition sys-
tems is therefore bisimulation due to Park [15] which is for instance also central
to the CCS process algebra by Milner [16]. Configurations of a pushdown au-
tomaton can also be viewed as processes generating (usually infinite) transition
graphs, and Stirling [17] showed that bisimulation equivalence is decidable for
a special class of pushdown automata. Generally, however, establishing bisimi-
larity (this is remarkably the same as finding a winning strategy in certain two-
player games, cf. Burkart et al. [18]) on infinite structures requires co-inductive
reasoning tailored to the particular instance.

                                        17
Stepwise Correspondences between Programs


    Deviating slightly from the bisimulation approach, programs in this frame-
work will be regarded as equivalent when they are mutually corresponding (the
exact definitions are given in Section 3.1 below) which is basically down to mu-
tual (i.e. bi-directional) similarity on the transition graphs. This equivalence
relation is weaker than bisimulation but turns out to be sufficient for all pur-
poses relevant in what follows. To outline the difference very abstractly, the
vertices s1 and t1 in the transition graphs
                          b ✲
                   s2         s4                               t3
                    ✻                                           ✻
                  a                                              b
                                                        a ✲
                   s1                           t1          t2
                  a                                             c
                    ❄     c ✲                                   ❄
                   s3         s5                               t4
are not mutually similar since neither s2 nor s3 can simulate the behaviours of
t2 so that s1 and t1 cannot be bisimilar either. With the following modification
                          b ✲
                   s2         s4                               t3
                    ✻          ✻                                ✻
                  a             b                                b
                          a ✲                           a ✲
                   s1         s6                t1          t2
                  a            c                                c
                    ❄     c ✲ ❄                                 ❄
                   s3        s5                                t4
they become mutually similar yet not bisimilar: s2 and s3 still cannot simulate
the behaviours of t2 .


3.1     Definitions
We first define when a set of pairs of L-terms forms a simulation and based on
that – when two programs are called corresponding.
Definition 3.1.1. Let X be a relation of type Lα ˆ Lβ ñ bool, where α and
β are state type abstractions. Further, let r be of type α ˆ β ñ bool, i.e. a
relation on the underlying states, and let ρ, ρ1 be two code retrieving functions of

                                        18
3.1. DEFINITIONS


type nat ñ Lα and nat ñ Lβ , respectively. Then X will be called a simulation
w.r.t. ρ, ρ1 and r if the following conditions hold:
 (1) if pp, qq P X and pσ1 , σ2 q P r then for any ρ1 $ pq, σ2 q ÑP pq 1 , σ21 q there is
     a program step ρ $ pp, σ1 q ÑP pp1 , σ11 q with pp1 , q 1 q P X and pσ11 , σ21 q P r,
 (2) if pskip, qq P X then q “ skip,
 (3) if pp, skipq P X then p “ skip.
Definition 3.1.2. Two programs pρ, pq and pρ1 , qq correspond w.r.t. r if there
exists some X that contains the pair pp, qq and is a simulation w.r.t. ρ, ρ1 , r.
This will be denoted by ρ, ρ1 |ù p Ěr q. Furthermore, pρ, pq and pρ1 , qq are called
mutually corresponding w.r.t. r if ρ1 , ρ |ù q Ěr˝ p additionally holds, where r˝
is the converse of r. This in turn will be denoted by ρ, ρ1 |ù p «r q.
    The notations ρ |ù p Ěr q and ρ |ù p «r q will be used whenever ρ and ρ1
are the same. With jump-free p and q we just write |ù p Ěr q and |ù p «r q.
Moreover, the index r will be omitted when r is the identity on the underlying
states such that if p and q are jump-free then we may simply write |ù p Ě q and
|ù p « q.

3.1.1     Highlighting the fixed point structure
The definitions are presented above in a form often favourable for reasoning
upon correspondences between programs. On the other hand, this form might
have slightly concealed the structure elaborated below focusing on jump-free
programs so that retrieving functions can be omitted for the sake of clarity.
    Let from now on r ˛ s denote the composition of relations r and s defined in
the standard way by tpa, bq | Dc. pa, cq P r ^ pc, bq P su. Thus, given a relation r
of type α ˆ β ñ bool, the transformer Tr sends each X of type Lα ˆ Lβ ñ bool
to the relation of the same type defined by
      ď
         tX 1 | pX 1 b rq ˛ ÑP Ď ÑP ˛ pX b rq ^ C X 1 u

where
   – s b r denotes a relational product containing ppp, σq, pq, σ 1 qq iff pp, qq P s
     and pσ, σ 1 q P r,
   – C X 1 stands for the condition: for all pp, qq P X 1 we have that p and q are
     jump-free and also p “ skip iff q “ skip.

                                           19
Stepwise Correspondences between Programs


By this it should be clear that a relation X is a simulation w.r.t. r by Defini-
tion 3.1.1 (restricted to jump-free terms) if and only if X is a postfixed point
of Tr i.e. X ĎŤTr X. Hence, as the union of the respective simulations, Ěr is
the same as tX | X Ď Tr Xu which is by definition the greatest fixed point
of Tr i.e. formally Ěr “ νTr . Furthermore, by the monotonicity of the rela-
tional composition and b-operator we have Tr pνTr q “ νTr and can particularly
conclude that Ěr is itself a postfixed point of Tr and hence a simulation by
Definition 3.1.1.
    It is worth to be noted that by assuming « Ď Tid p«q, i.e. that the mutual
correspondence with r “ id is likewise a postfixed point of Tid , we could infer
that the respective transition graphs of any jump-free p and q with |ù p « q are
bisimilar which, as pointed out before, is not true in this generality. A particular
consequence is that « is not a simulation in the sense of Definition 3.1.1 although
it clearly satisfies the conditions (2) and (3).
    Lifting lastly the restriction to jump-free terms, the relation transformer
additionally gets two retrieving functions as parameters and the above argu-
mentation accordingly yields that ρ, ρ1 |ù p Ěr q holds iff pp, qq P νTρ,ρ1 ,r does.


3.2      Properties of correspondences
From the above considerations follows that the relation tpp, qq | ρ, ρ1 |ù p Ěr qu is
the largest simulation w.r.t. ρ, ρ1 , r and the conditions (1)–(3) of Definition 3.1.1
consequently hold with tpp, qq | ρ, ρ1 |ù p Ěr qu in place of X (note once more
that one cannot proceed likewise with the mutual correspondence for any r).
   First, the condition (1) of Definition 3.1.1 with tpp, qq | ρ, ρ1 |ù p Ěr qu in
place of X can by induction be generalised to any number of steps:
                                                                    n
Proposition 3.2.1. Assume ρ, ρ1 |ù p Ěr q and ρ1 $ pq, σ2 q ÑP pq 1 , σ21 q where
n P N. Furthermore, suppose pσ1 , σ2 q P r. Then there exist p1 and σ11 such that
             n
ρ $ pp, σ1 q ÑP pp1 , σ11 q holds with ρ, ρ1 |ù p1 Ěr q 1 and pσ11 , σ21 q P r.

   The general transitivity rule for program correspondences has the following
form:

Proposition 3.2.2. If ρ1 , ρ2 |ù p1 Ěr p2 and ρ2 , ρ3 |ù p2 Ěs p3 then we also
have ρ1 , ρ3 |ù p1 Ěr ˛ s p3 .

Proof. The assumptions give us two simulations: X1 w.r.t. ρ1 , ρ2 , r containing
pp1 , p2 q, and X2 w.r.t. ρ2 , ρ3 , s containing pp2 , p3 q. The relational composition

                                          20
3.2. PROPERTIES OF CORRESPONDENCES


X1 ˛ X2 contains the pair pp1 , p3 q and is a simulation w.r.t. ρ1 , ρ3 , r ˛ s which
follows straight from the properties of X1 and X2 .

   With identities in place of r and s, the preceding statement simplifies to

Corollary 3.2.3. If ρ1 , ρ2 |ù p1 Ě p2 and ρ2 , ρ3 |ù p2 Ě p3 then we also have
ρ1 , ρ3 |ù p1 Ě p3 . Furthermore, for jump-free p1 , p2 , p3 we accordingly just have
that |ù p1 Ě p2 and |ù p2 Ě p3 imply |ù p1 Ě p3 .

   That Ě is moreover reflexive and hence a preorder is shown next. Note that
Ěr does not have to be a preorder for any r though.

Proposition 3.2.4. ρ |ù p Ě p.

Proof. The identity on Lα gives us a simulation w.r.t. the identity on α.

    The central consequence of Corollary 3.2.3 and Proposition 3.2.4 is that for
any jump-free p the set tpρ, xq | ρ |ù p « xu forms its equivalence class whose
elements indeed have a lot in common: one of the results in Section 5.2 is that
programs pρ, pq and pρ, qq exhibit the same rely/guarantee properties whenever
ρ |ù p « q holds. Moreover, under the same assumption using Proposition 3.2.2
one can show that for any x and r we have ρ |ù p Ěr x iff ρ |ù q Ěr x, i.e. pρ, pq
and pρ, qq correspond to exactly the same programs.
    These considerations essentially justify the choice of « as the program equiv-
alence for this framework and so we can step up to investigating on associativity
and commutativity properties.
    The sequential composition operator will be shown to be associative by
Proposition 3.2.5. Regarding associativity of the parallel composition, consider
                  def                                  def
the programs p “ pbasic f k skipq k skip and q “ basic f k pskip k skipq
with any f such that there exists a state σ ‰ f σ. If we assume |ù p Ě q then
by Proposition 3.2.1 to the step pq, σq ÑP pbasic f k skip, σq there must be
a corresponding step pp, σq ÑP px, σq with some x. This is however impossi-
ble since pp, σq ÑP ppskip k skipq k skip, f σq is the only one program step
from pp, σq, meaning that |ù p ﬀ q holds. Although the counterexample might
be perceived as technical, it nonetheless leads to the conclusion that the bi-
nary parallel operator is not associative at the level of small-step evaluation. In
other words, we take the edge off by allowing ‘flat’ lists of parallel components
(e.g. kbasic f, skip, skip) whose reordering shall not give rise to semantic dif-
ferences though and Corollary 3.2.7 makes that point explicit.

Proposition 3.2.5. ρ |ù p1 ; p2 ; p3 « pp1 ; p2 q; p3 .

                                           21
Stepwise Correspondences between Programs


Proof. We show ρ |ù p1 ; p2 ; p3 Ě pp1 ; p2 q; p3 whereas ρ |ù pp1 ; p2 q; p3 Ě p1 ; p2 ; p3
                                      def
follows similarly. The set X “ tpu; p2 ; p3 , pu; p2 q; p3 q | u P Ju Y id contains the
pair p1 ; p2 ; p3 and pp1 ; p2 q; p3 . Further, suppose ρ $ ppu; p2 q; p3 , σq ÑP px, σ 1 q
for some u. If u “ skip then x “ p2 ; p3 and σ 1 “ σ which can be matched by the
step ρ $ pskip; p2 ; p3 , σq ÑP pp2 ; p3 , σq. If u ‰ skip then we have a program
step ρ $ pu, σq ÑP pu1 , σ 1 q with some u1 such that x “ pu1 ; p2 q; p3 . Thus, we
further have ρ $ pu; p2 ; p3 , σq ÑP pu1 ; p2 ; p3 , σ 1 q which is a matching step since
pu1 ; p2 ; p3 , pu1 ; p2 q; p3 q P X.

Proposition 3.2.6. Let I “ t1, . . . , mu with m ą 0 and assume qi “ pπpiq for
all i P I where π is a permutation on I. Then ρ |ù kp1 , . . . , pm Ě kq1 , . . . , qm .

Proof. The following set contains the pair pkp1 , . . . , pm , kq1 , . . . , qm q:
           def
       X “ tpku1 , . . . , um , kv1 , . . . , vm q | @i P I. vi “ uπpiq u Y tpskip, skipqu

and is a simulation. To establish that, suppose ρ $ pkv1 , . . . , vm , σq ÑP px, σ 1 q
and pku1 , . . . , um , kv1 , . . . , vm q P X with some x, σ, σ 1 , u1 , . . . , um and v1 , . . . , vm .
If x is skip so are ui , vi for all i P I, i.e. we are done. Otherwise there is a step
ρ $ pvi , σq ÑP pvi1 , σ 1 q with some i P I such that x “ kv1 , . . . vi1 . . . , vm holds. We
then also have ρ $ pku1 , . . . uπpiq . . . , um , σq ÑP pku1 , . . . u1πpiq . . . , um , σ 1 q where
u1πpiq is set to vi1 . The program step is sound because uπpiq “ vi is assumed.

Corollary 3.2.7. Let I “ t1, . . . , mu with m ą 0 and assume qi “ pπpiq for all
i P I where π is a permutation on I. Then ρ |ù kp1 , . . . , pm « kq1 , . . . , qm .

Proof. The direction ρ |ù kp1 , . . . , pm Ě kq1 , . . . , qm is just Proposition 3.2.6. To
show ρ |ù kq1 , . . . , qm Ě kp1 , . . . , pm we once more apply Proposition 3.2.6, but
now with π ´1 for π. This is sound since π ´1 is also a permutation on I and we
have pi “ pπpπ´1 piqq “ qπ´1 piq for all i P I.

3.2.1       Closure properties
The rules presented in this section particularly enable syntax-driven derivations
of program correspondences, i.e. derivations following syntactic patterns.

Proposition 3.2.8. Let I “ t1, . . . , mu with m ą 0 and assume

  (1) ρ, ρ1 |ù pi Ěr qi for all i P I.

Then ρ, ρ1 |ù kp1 , . . . , pm Ěr kq1 , . . . , qm .

                                                   22
3.2. PROPERTIES OF CORRESPONDENCES


Proof. The assumption (1) provides simulations X1 , . . . , Xm w.r.t. ρ, ρ1 , r such
that ppi , qi q P Xi holds for all i P I. Then let
         def
     X “ tpku1 , . . . , um , kv1 , . . . , vm q | @i P I. pui , vi q P Xi u Y tpskip, skipqu

containing the pair pkp1 , . . . , pm , kq1 , . . . , qm q. To show that X is a simulation
w.r.t. ρ, ρ1 , r suppose we have a program step ρ1 $ pkv1 , . . . , vm , σ2 q ÑP px, σ21 q
with pσ1 , σ2 q P r and pku1 , . . . , um , kv1 , . . . , vm q P X.
     If x is skip then we have vi “ skip for all i P I and hence also ui “ skip
for all i P I due to pui , vi q P Xi . If x ‰ skip then there is a program step
ρ1 $ pvi , σ2 q ÑP pvi1 , σ21 q with some vi1 and i P I such that x “ kv1 , . . . vi1 . . . , vm .
Since we have pui , vi q P Xi and pσ1 , σ2 q P r, there is a matching program step
ρ $ pui , σ1 q ÑP pu1i , σ11 q with some u1i and σ11 such that pu1i , vi1 q P Xi and also
pσ11 , σ21 q P r hold. This in turn enables the transition

        ρ $ pku1 , . . . ui . . . , um , σ1 q ÑP pku1 , . . . u1i . . . , um , σ11 q

with pku1 , . . . u1i . . . , um , kv1 , . . . vi1 . . . , vm q P X.
Proposition 3.2.9. Assume
  (1) ρ, ρ1 |ù p1 Ěr q1 ,
  (2) ρ, ρ1 |ù p2 Ěr q2 .
Then ρ, ρ1 |ù p1 ; p2 Ěr q1 ; q2 .
Proof. From (1) and (2) we respectively obtain two simulations X1 , X2 w.r.t.
ρ, ρ1 , r with pp1 , q1 q P X1 and pp2 , q2 q P X2 . Further, let
         def
     X “ tpu; p2 , v; q2 q | pu, vq P X1 u Y X2

such that pp1 ; p2 , q1 ; q2 q P X holds in first place. It remains thus to show that
X is a simulation w.r.t. ρ, ρ1 , r. To this end let ρ1 $ pv; q2 , σ2 q ÑP px, σ21 q with
pσ1 , σ2 q P r and pu, vq P X1 . If v “ skip then u “ skip, x “ q2 and σ21 “ σ2
follow so that we are done since pp2 , q2 q P X2 and X2 Ď X.
     If v ‰ skip then x “ v 1 ; q2 which is due to a step ρ1 $ pv, σ2 q ÑP pv 1 , σ21 q with
some v 1 . By pu, vq P X1 we then have ρ $ pu, σ1 q ÑP pu1 , σ11 q with pσ11 , σ21 q P r
and pu1 , v 1 q P X1 . Thus, we derive the step ρ $ pu; p2 , σ1 q ÑP pu1 ; p2 , σ11 q with
pu1 ; p2 , xq P X.
    Next three propositions handle conditional, while- and await-statements tak-
ing additionally branching and blocking conditions into account.

                                                        23
Stepwise Correspondences between Programs


Proposition 3.2.10. Assume
 (1) ρ, ρ1 |ù p1 Ěr p2 ,
 (2) ρ, ρ1 |ù q1 Ěr q2 ,
 (3) for any pσ1 , σ2 q P r we have σ1 P C1 iff σ2 P C2 .
Then ρ, ρ1 |ù if C1 then p1 else q1 fi Ěr if C2 then p2 else q2 fi.
Proof. From (1) and (2) we respectively get simulations Xp , Xq w.r.t. ρ, ρ1 , r
with pp1 , p2 q P Xp and pq1 , q2 q P Xq . We define
       def
   X “ Xp Y Xq Y tpif C1 then p1 else q1 fi, if C2 then p2 else q2 fiqu

and show that X is a simulation w.r.t. ρ, ρ1 , r. First, note that as the union
of simulations, Xp Y Xq is a simulation as well. Then for the remaining case,
suppose we have a step ρ1 $ pif C2 then p2 else q2 fi, σ2 q ÑP px, σ2 q with
pσ1 , σ2 q P r. If σ2 P C2 then x “ p2 and hence there is the matching transition
ρ $ pif C1 then p1 else q1 fi, σ1 q ÑP pp1 , σ1 q since σ1 P C1 by (3). The case
with σ2 R C2 is symmetric.
Proposition 3.2.11. Let pwhile “ while C1 do p1 subsequently q1 od and
qwhile “ while C2 do p2 subsequently q2 od, and assume
 (1) ρ, ρ1 |ù p1 Ěr p2 ,
 (2) ρ, ρ1 |ù q1 Ěr q2 ,
 (3) for any pσ1 , σ2 q P r we have σ1 P C1 iff σ2 P C2 .
Then ρ, ρ1 |ù pwhile Ěr qwhile .
Proof. From (1) and (2) we respectively get simulations Xp , Xq w.r.t. ρ, ρ1 , r
with pp1 , p2 q P Xp and pq1 , q2 q P Xq . The relevant set of pairs X is defined by
         def
     X “ tppwhile , qwhile q, pskip; pwhile , skip; qwhile qu Y
         tpu; skip; pwhile , v; skip; qwhile q | pu, vq P Xp u Y Xq

To establish X as a simulation, suppose pσ1 , σ2 q P r and consider the following
cases.
    Regarding the first pair ppwhile , qwhile q, suppose ρ1 $ pqwhile , σ2 q ÑP px, σ2 q.
If σ2 P C2 then x “ p2 ; skip; qwhile and, moreover, σ1 P C1 by (3). Hence there
is the matching step ρ $ ppwhile , σ1 q ÑP pp1 ; skip; pwhile , σ1 q.

                                           24
3.2. PROPERTIES OF CORRESPONDENCES


   The next case with pskip; pwhile , skip; qwhile , q is clear because there is only
one possible step ρ1 $ pskip; qwhile , σ2 q ÑP pqwhile , σ2 q which is matched by the
only possible ρ $ pskip; pwhile , σ1 q ÑP ppwhile , σ1 q.
   Lastly, suppose ρ1 $ pv; skip; qwhile , σ2 q ÑP px, σ21 q with pu, vq P Xp . If we
have v “ skip then u “ skip follows leading to the same situation as in the
preceding case. Otherwise, with v ‰ skip we have x “ v 1 ; skip; qwhile due to
a program step ρ1 $ pv, σ2 q ÑP pv 1 , σ21 q. Since Xp is a simulation, we obtain a
transition ρ $ pu, σ1 q ÑP pu1 , σ11 q with pu1 , v 1 q P Xp and pσ11 , σ21 q P r. The latter
transition moreover entails ρ $ pu; skip; pwhile , σ1 q ÑP pu1 ; skip; pwhile , σ11 q.

Proposition 3.2.12. Assume

 (1) ρ, ρ1 |ù p1 Ěr p2 ,

 (2) σ2 P C2 implies σ1 P C1 for any pσ1 , σ2 q P r.

Then ρ, ρ1 |ù await C1 do p1 od Ěr await C2 do p2 od.
                      def
Proof. The set X “ tpawait C1 do p1 od, await C2 do p2 odq, pskip, skipqu
forms a simulation: ρ1 $ pawait C2 do p2 od, σ2 q ÑP px, σ21 q and pσ1 , σ2 q P r
                                         ˚
firstly entail σ2 P C2 , ρ1 $ pp2 , σ2 q ÑP pskip, σ21 q and x “ skip. By Proposi-
tion 3.2.1 and (1) we can further obtain a state σ11 such that pσ11 , σ21 q P r and
               ˚
ρ $ pp1 , σ1 q ÑP pskip, σ11 q hold. From this we can in turn derive the matching
step ρ $ pawait C1 do p1 od, σ1 q ÑP pskip, σ11 q as σ1 P C1 follows by (2).

   The remaining two propositions handle correspondences between the com-
binations of indivisible steps that will be relevant later on.

Proposition 3.2.13. If pf σ1 , g σ2 q P r holds for any pair pσ1 , σ2 q P r then we
have |ù basic f Ěr basic g.

Proof. The assumption provides that tpbasic f, basic gq, pskip, skipqu is a
simulation w.r.t. r.

Proposition 3.2.14. If for any pair pσ1 , σ2 q P r there exists some σ11 such that
             ˚
ρ $ pp, σ1 q ÑP pskip, σ11 q and pσ11 , f σ2 q P r hold then ρ |ù xpy Ěr basic f .
                def
Proof. Let X “ tpxpy, basic f q, pskip, skipqu. In order to show that X is a
simulation w.r.t. ρ and r, suppose pσ1 , σ2 q P r. Thus, by the assumption there
                                                               ˚
must be some state σ11 with pσ11 , f σ2 q P r and ρ $ pp, σ1 q ÑP pskip, σ11 q, such
that ρ $ pxpy, σ1 q ÑP pskip, σ11 q follows.

                                             25
Stepwise Correspondences between Programs


3.3      Sequential normalisation
As pointed out in Chapter 1, certain code restructurings are needed prior to
a rational replacement of conditional and while-statements by their represen-
tations using jumps. Next two propositions show that no semantic differences
arise by these restructurings whereas Section 3.4 proceeds to the actual jump-
transformations.
Proposition 3.3.1. Let
 (1) L “ if C then p1 else p2 fi; q,
 (2) R “ if C then p1 ; q else p2 ; q fi.
Then ρ |ù L « R.
Proof. We establish the correspondence ρ |ù L Ě R by showing that the set of
pairs tpL, Rqu Y id is a simulation w.r.t. ρ. Suppose ρ $ pR, σq ÑP px, σq with
some x and σ. If σ P C then x “ p1 ; q and hence we have the matching step
ρ $ pL, σq ÑP pp1 ; q, σq. The case with σ R C is symmetric and the opposite
direction ρ |ù R Ě L can be concluded likewise.
Proposition 3.3.2. Let
 (1) L “ while C do p1 subsequently p2 od; q,
 (2) R “ while C do p1 subsequently p2 ; q od.
Then ρ |ù L « R.
Proof. We will establish the correspondence ρ |ù L Ě R by showing that the set
    def
X “ tpskip; L, skip; Rq, pL, Rqqu Y tpv; skip; L, v; skip; Rqq | v P Ju Y id is
a simulation w.r.t. ρ whereas the opposite direction, i.e. ρ |ù R Ě L, follows in
a symmetric way.
    The case pskip; L, skip; Rq is clear. Next, assume ρ $ pR, σq ÑP px, σq with
some x and σ. If σ P C then x “ p1 ; skip; R and hence there is the matching
step ρ $ pL, σq ÑP pp1 ; skip; L, σq since pp1 ; skip; L, xq P X. If σ R C then we
have x “ p2 ; q and hence we can take the step from pL, σq to the same px, σq.
    Lastly, suppose ρ $ pv; skip; R, σq ÑP px, σ 1 q with some x, σ, σ 1 . If v “ skip
then x “ skip; R and σ 1 “ σ. Hence ρ $ pskip; skip; L, σq ÑP pskip; L, σq is
the matching step. If v ‰ skip then there is a step ρ $ pv, σq ÑP pv 1 , σ 1 q such
that x “ v 1 ; skip; R holds. Thus, ρ $ pv; skip; L, σq ÑP pv 1 ; skip; L, σ 1 q is the
matching transition in that case.

                                          26
3.4. REPLACING CONDITIONAL AND WHILE-STATEMENTS BY JUMPS


3.4         Replacing conditional and while-statements
            by jumps
Proposition 3.4.1. The program equivalence

      ρ |ù if C then p else ρ j fi « cjump C to j otherwise p end

holds for all ρ, C, p and j.
Proof. By taking the simulation w.r.t. ρ

      tpif C then p else ρ j fi, cjump C to j otherwise p endqu Y id

for the Ě-direction and

      tpcjump C to j otherwise p end, if C then p else ρ j fiqu Y id

for the opposite.
    The following proof utilises the extra skip built into the rule ‘While-True’
(cf. Figure 2.1).
Proposition 3.4.2. Assume
 (1) ρ i “ cjump C to j otherwise p; jump i end,
 (2) ρ j “ q.
Then ρ |ù while C do p subsequently q od « ρ i.
Proof. To establish the Ě-direction we define
      def
  X “ tpL, ρ iq, pskip; L, jump iqu Y tpu; skip; L, u; jump i | u P Ju Y id

where L stands for while C do p subsequently q od, and proceed by showing
that X is a simulation w.r.t. ρ.
   Regarding the pair pL, ρ iq, suppose there is a step ρ $ pρ i, σq ÑP px, σq
with some x and σ. If σ P C then x “ p; jump i which can be matched by the
program step ρ $ pL, σq ÑP pp; skip; L, σq since pp; skip; L, p; jump iq P X. If
σ R C then x “ ρ j “ q follows and we can simply take the step from pL, σq to
the same configuration pq, σq since id Ď X.
   Next, with pskip; L, jump iq any transition ρ $ pjump i, σq ÑP pρ i, σq can
be matched straight by ρ $ pskip; L, σq ÑP pL, σq since pL, ρ iq P X.

                                      27
Stepwise Correspondences between Programs


    Lastly, suppose we have ρ $ pu; jump i, σq ÑP px, σ 1 q with some x, σ, σ 1 and
u. If u “ skip then x “ jump i and σ 1 “ σ follow which is straight matched by
the step ρ $ pskip; skip; L, σq ÑP pskip; L, σq. If u ‰ skip then x “ u1 ; jump i
due to a step ρ $ pu, σq ÑP pu1 , σ 1 q with some u1 . This transition further entails
ρ $ pu; skip; L, σq ÑP pu1 ; skip; L, σ 1 q such that pu1 ; skip; L, u1 ; jump iq P X.
    The correspondence ρ |ù ρ i Ě L follows symmetrically.
   Note that for the sake of simplicity the above proposition captured only the
basic principle behind the transformation: it does not account for the circum-
stance that the construction p; jump i usually creates an additional subject to
the sequential normalisation described in Section 3.3. For instance, if p is a
conditional statement then jump i needs to be ‘pushed’ into both branches. To
address that, (1) may be generalised to ρ i “ cjump C to j otherwise p1 end
with some p1 satisfying ρ |ù p1 « p; jump i.




                                         28
Chapter 4

Potential Computations and
Program Correspondences

This chapter takes up the topic of potential computations and elaborates on
the question how potential computations of two corresponding programs are
related. In line with this, it will also pay due attention to a characterisation of
the program equivalence in terms of computations.


4.1      Conditions on potential computations
We start by defining the conditions that allow us to systematically access subsets
of potential computations of a program.

Definition 4.1.1. Let G be of type α ˆ α ñ bool, i.e. a state relation. Then
the program condition Prog G comprises all infinite potential computations sq
where pSpsq i q, Spsq i`1 qq P G holds for each program step sq i ÑP sq i`1 , as well
as all finite non-empty prefixes of such sq.

    Program conditions can thus be used to encircle computations where the
pre- and the poststate of each program step are related by some given G and,
as one might expect, environment steps will be handled accordingly next.

Definition 4.1.2. Let R be a state relation. Then the environment condition
Env ω R comprises all infinite potential computations sq where the condition
pSpsq i q, Spsq i`1 qq P R holds for each environment step sq i ÑE sq i`1 .

                                         29
Potential Computations and Program Correspondences


    This definition addresses only infinite computations for the following reason.
As defined by Stirling [9], the set of actual computations of a program is the
set of its potential computations without any environment steps. Thus, Env ω K
contains all infinite actual computations (here and in what follows, K denotes
the empty relation: the complement of the already introduced J). Prefixing
Env ω K does not give us the entire set of finite actual computations however:
actual computations of programs terminating on all inputs when run in isolation
would for instance be omitted. Therefore we explicitly recast Definition 4.1.2
as follows:
Definition 4.1.3. Let R be a state relation. Then the environment condi-
tion Env R comprises all finite potential computations sq where the condition
pSpsq i q, Spsq i`1 qq P R holds for any i ă |sq| ´ 1 with sq i ÑE sq i`1 .
    The set of (finite or infinite) actual computations is then consequently the
union of Env ω K and Env K. However, only the notation Env R will be used in
the sequel as it will be clear from the context which variant of the environment
condition is meant.
    The remaining two conditions apply to both, finite and infinite computations,
in particular allowing us to address input/output properties of programs.
Definition 4.1.4. Let C be of type α ñ bool, i.e. a state predicate. A poten-
tial computation sq satisfies the input condition In C if Spsq 0 q P C. Further-
more, if there is an index i with Ppsq i q “ skip and Spsq µ q P C holds for the
first such index µ then sq satisfies the output condition Out C.
    Despite a different formulation, the definition of Out C essentially coincides
with its counterpart given by Stirling [9]: one can show that sq P Out C holds
iff Ppsq i q “ skip implies that there exists some j ď i such that Ppsq j q “ skip
and Spsq j q P C hold for any i ă |sq| in case sq is finite or just for any i P N
otherwise.


4.2     Replaying finite potential computations
The following proposition resorts to environment conditions for showing how
finite potential computations can be replayed along program correspondences.
Proposition 4.2.1. Assume that ρ, ρ1 |ù p Ěr q, sq q P vqwρ1 , sq q P Env R1 and
r ˛ R1 Ď R ˛ r hold. Further, let σ be a state with pσ, Spsq q0 qq P r. Then there
exists a computation sq p P vpwρ with the same length as sq q satisfying moreover
the following conditions:

                                       30
4.2. REPLAYING FINITE POTENTIAL COMPUTATIONS


  (1) Spsq p0 q “ σ,
  (2) sq p P Env R,
  (3) pSpsq pi q, Spsq qi qq P r for any i ă |sq q |,
  (4) ρ, ρ1 |ù Ppsq pi q Ěr Ppsq qi q for any i ă |sq q |,
  (5) sq pi ÑE sq pi`1 iff sq qi ÑE sq qi`1 for any i ă |sq q | ´ 1.
Proof. We proceed by induction on the length of sq q . The case |sq q | “ 0 is
trivial since sq q P vqwρ1 implies that sq q is not empty. Next, if |sq q | “ 1 then
the singleton sequence pp, σq P vpwρ clearly meets the conditions (1)–(5).
     Further, suppose |sq| “ n ` 1 with n ě 1 and consider n |sq q , i.e. the prefix
sq 0 , . . . , sq qn´1 with the length n, for which we have n |sq q P vqwρ1 X Env R1 and
   q

pσ, Spn |sq q0 qq P r. Hence, by the induction hypothesis there is a computation
sq p P vpwρ with |sq p | “ n satisfying moreover the conditions (1)–(5) w.r.t. n |sq q .
This particularly means:
  (a) pSpsq pn´1 q, Spsq qn´1 qq P r and
 (b) ρ, ρ1 |ù Ppsq pn´1 q Ěr Ppsq qn´1 q.
      If we have an environment step sq qn´1 ÑE sq qn then pSpsq qn´1 q, Spsq qn qq P R1
holds since sq q P Env R1 is assumed. Hence, pSpsq pn´1 q, Spsq qn qq P r ˛ R1 can be
further inferred using (a). Then the assumption r ˛ R1 Ď R ˛ r provides some
σ 1 such that pSpsq pn´1 q, σ 1 q P R and pσ 1 , Spsq qn qq P r hold. We can thus extend
sq p by an environment step to sq p0 , . . . , sq pn´1 ÑE pPpsq pn´1 q, σ 1 q which yields a
computation in vpwρ of length n ` 1 satisfying the conditions (1)–(5) w.r.t. sq q .
      If we have a program step ρ1 $ sq qn´1 ÑP sq qn then with (a) and (b) we can
further obtain a step ρ $ sq pn´1 ÑP pp1 , σ 1 q such that ρ, ρ1 |ù p1 Ěr Ppsq qn q and
pσ 1 , Spsq qn qq P r hold. Extending thus sq p to sq p0 , . . . , sq pn´1 ÑP pp1 , σ 1 q we once
more get a computation in vpwρ of length n ` 1 satisfying (1)–(5) w.r.t. sq q .
    In particular, with r instantiated by id whereas R and R1 – by J, the above
statement simplifies to:
Corollary 4.2.2. If ρ, ρ1 |ù p Ě q and sq q P vqwρ1 then there is a computation
sq p P vpwρ with |sq p | “ |sq q | satisfying moreover
  (1) Spsq pi q “ Spsq qi q for any i ă |sq q |,
  (2) ρ, ρ1 |ù Ppsq pi q Ě Ppsq qi q for any i ă |sq q |,
  (3) sq pi ÑE sq pi`1 iff sq qi ÑE sq qi`1 for any i ă |sq q | ´ 1.

                                               31
Potential Computations and Program Correspondences


4.3      A characterisation of the program equiva-
         lence
Apart from its primary application later in Section 5.2, Proposition 4.2.1 is also
a step towards an interpretation of what a program equivalence ρ, ρ1 |ù p « q
actually means in terms of the potential computations of pρ, pq and pρ1 , qq: this
is expressed by the following proposition with a proof utilising Corollary 4.2.2.
Proposition 4.3.1. ρ, ρ1 |ù p Ě q holds iff there exists a function Φ sending
each sq q P vqwρ1 to a non-empty set of computations Φpsq q q such that
 (1) sq P vpwρ and |sq| “ |sq q | for all sq P Φpsq q q,
 (2) Spsq i q “ Spsq qi q for any i ă |sq q | and sq P Φpsq q q,
 (3) sq i “ skip iff sq qi “ skip for any i ă |sq q | and sq P Φpsq q q,
 (4) sq i ÑE sq i`1 iff sq qi ÑE sq qi`1 for any i ă |sq q | ´ 1 and sq P Φpsq q q,
 (5) Φpi`1|sq q q Ď i`1|Φpsq q q for any i ă |sq q |
where i`1 |Φpsq q q denotes the set of prefixes of length i ` 1 taken from each
computation in Φpsq q q.
Proof. To show that the condition ρ, ρ1 |ù p Ě q is necessary, suppose there is
such Φ and let

      X “ tpPpsq |sq q |´1 q, Ppsq q|sq q |´1 qq | sq q P vqwρ1 ^ sq P Φpsq q qu.
          def




Due to (1) and (2) we have Φpq, σq “ tpp, σqu for any state σ (where pq, σq and
pp, σq shall be understood as computations of length 1), hence pp, qq P X holds.
Next, we show that X is a simulation w.r.t. ρ, ρ1 and id (cf. Definition 3.1.1).
To this end we may assume sq q P vqwρ1 , sq P Φpsq q q, |sq q | “ n ` 1 with n P N
and, moreover, a program step ρ1 $ pPpsq qn q, σq ÑP pv, σ 1 q for which we have
to provide a matching step from the configuration pPpsq n q, σq. Let sq q1 extend
sq q by two configurations as follows: sq q ÑE pPpsq qn q, σq ÑP pv, σ 1 q. Thus, we
have sq q1 P vqwρ1 and n`1 |sq q1 “ sq q so that by (5) there exists a computation
sq 1 P Φpsq q1 q with n`1 |sq 1 “ sq. Since sq 1 also meets the conditions (1)–(4), it
must be of the form sq ÑE pPpsq n q, σq ÑP pu, σ 1 q giving us the matching step
ρ $ pPpsq n q, σq ÑP pu, σ 1 q because pu, vq “ pPpsq 1n`2 q, Ppsq qn`2
                                                                     1
                                                                        qq i.e. pu, vq P X.
              q                                q
For any sq P vqwρ and any sq P Φpsq q we can lastly conclude using (3) that
                      1

Ppsq |sq q |´1 q “ skip holds iff Ppsq q|sq q |´1 q “ skip does.

                                            32
4.3. A CHARACTERISATION OF THE PROGRAM EQUIVALENCE


    In order to show that ρ, ρ1 |ù p Ě q is sufficient, let Φ send each sq q P vqwρ1
to the non-empty set

      tsq P vpwρ | sq satisfies the conditions of Corollary 4.2.2 w.r.t. sq q u

such that (1)–(4) clearly hold. Regarding (5), let i ă |sq q | and sq p1 P Φpi`1 |sq q q.
Since Corollary 4.2.2 provides stepwise correspondence of sq p1 and i`1 |sq q , we
can particularly infer ρ, ρ1 |ù Ppsq pi 1 q Ě Ppsq qi q. Further, the suffix i |sq q starts
with sq qi and is not empty so that i |sq q P vPpsq qi qwρ1 holds. Resorting to Corol-
lary 4.2.2 once more, we can replay this suffix by some sq p2 P vPpsq pi 1 qwρ with
|sq p2 | “ |sq q | ´ i. Note that this construction ensures sq pi 1 “ sq p02 , i.e. the last
configuration of sq p1 is the first of sq p2 . Thus, sq p1 ’ sq p2 P vpwρ is well-defined
and we have i`1 |psq p1 ’ sq p2 q “ sq p1 and, moreover, sq p1 ’ sq p2 P Φpsq q q since
|sq p1 ’ sq p2 | “ |sq p1 | ` |sq p2 | ´ 1 “ pi ` 1q ` p|sq q | ´ iq ´ 1 “ |sq q |.
    Reflecting on this result, ρ, ρ1 |ù p « q can be expressed by a second-order
formula which relates computations of p and q without self-references in contrast
to the characterisation from Section 3.1.1 as an intersection of two greatest
fixed points. On the other hand, here we have the quite intricate condition (5)
capturing that for any sq q P vqwρ1 we can find some sq p P vpwρ which not only
corresponds to sq q by means of (1)–(4) but is also extendable in response to any
possible extension of sq q . Moreover, note that it is in principle possible to have
some sq P Φpsq 1 ’ sq 2 q with n |sq R Φpsq 1 q where n “ |sq 1 | and |sq 2 | ą 1 since
the condition (5) is not an equality.
    It is finally worth noting that projecting a computation sq 0 , . . . , sq n to the
sequence of states Spsq 0 q, . . . , Spsq n q can be viewed as constructing a trace of
the computation. Thus, by Proposition 4.3.1 from the assumption ρ, ρ1 |ù p « q
follows that the sets of such traces of pρ, pq and pρ1 , qq are equal, as one shall
expect from equivalent programs. Although such traces may be practical for
various purposes, they omit important pieces of structural data, particularly
used to define the notion of fair computations in Section 9.2.




                                            33
Chapter 5

A Hoare-style
Rely/Guarantee Program
Logic

The following chapter applies most of the concepts presented so far and is de-
voted to a Hoare-style program logic [19] for structured reasoning upon proper-
ties of programs with interleaved computations.


5.1     The extended Hoare triples
Within the logic, program properties are expressed by means of the extended
Hoare triples, denoted by ρ |ù tR, P u p tQ, Gu where the component R is called
the rely, P – the precondition, Q – the postcondition, and G – the guarantee.
Following Stirling [9], the word extended emphasises that such triples arise by a
generalisation of the Hoare triples used in the method by Owicki and Gries [10]
where non-interference conditions are derived from annotated assertions. With
the extended triples, such assertions are instead neatly captured by the compo-
nents that constitute the extension: the rely and the guarantee namely.
Definition 5.1.1. Let pρ, pq be a program, R and G – state relations, whereas
P and Q – state predicates. Then the condition ρ |ù tR, P u p tQ, Gu holds iff
Env R X In P X vpwρ Ď Out Q X Prog G does.
   Next definition explicitly addresses properties of infinite computations too:

                                       35
A Hoare-style Rely/Guarantee Program Logic


Definition 5.1.2. The condition ρ |ùω tR, P u p tQ, Gu holds iff

  (1) Env R X In P X vpwω
                        ρ Ď Out Q X Prog G and

  (2) ρ |ù tR, P u p tQ, Gu.

    As shown next, these two definitions turn out to be logically equivalent so all
rules in this chapter can refer to Definition 5.1.1 without any loss of generality.

Proposition 5.1.1. ρ |ù tR, P u p tQ, Gu iff ρ |ùω tR, P u p tQ, Gu.

Proof. That the condition ρ |ù tR, P u p tQ, Gu is necessary follows immediately
from Definition 5.1.2 whereas the opposite direction amounts to showing that
Env R X In P X vpwω  ρ Ď Out Q X Prog G is implied by ρ |ù tR, P u p tQ, Gu. To
this end let sq be an infinite computation in vpwω  ρ with sq P Env R X In P .
     To show sq P Out Q we can assume Ppsq i q “ skip with some i P N. Then
also the prefix i`1 |sq P vpwρ satisfies Env R and In P such that i`1 |sq P Out Q
follows from ρ |ù tR, P u p tQ, Gu. Since the last element of i`1 |sq is the skip-
configuration sq i we get some j ď i with Ppsq j q “ skip and Spsq j q P Q.
     Next, to show sq P Prog G we proceed very similarly. Assuming a program
step ρ $ sq i ÑP sq i`1 for some i P N, we now consider the prefix i`2 |sq P vpwρ
which satisfies Env R and In P . Using ρ |ù tR, P u p tQ, Gu we can first infer
i`2 |sq P Prog G to ultimately conclude pSpsq i q, Spsq i`1 qq P G.




5.2       The program correspondence rule
In essence, this rule gives sufficient conditions for turning program correspon-
dences into implications on program logical properties. From now on, let R ¨ X
denote tb | Da P X. pa, bq P Ru, i.e. the image of a set X under a relation R.

Proposition 5.2.1. Assume ρ, ρ1 |ù p Ěr q, ρ |ù tR, P u p tQ, Gu and

  (1) P 1 Ď r ¨ P ,

  (2) r ˛ R1 Ď R ˛ r,

  (3) r ¨ Q Ď Q1 ,

  (4) r˝ ˛ G ˛ r Ď G1 .

Then ρ1 |ù tR1 , P 1 u q tQ1 , G1 u.

                                        36
5.2. THE PROGRAM CORRESPONDENCE RULE


Proof. Let sq q P vqwρ1 X Env R1 X In P 1 . Then by (1) there is a state σ P P such
that pσ, Spsq q0 qq P r. With (2), Proposition 4.2.1 further provides the existence
of a potential computation sq p P vpwρ with |sq p | “ |sq q | satisfying moreover
 (a) sq p P Env R X In P ,
 (b) pSpsq pi q, Spsq qi qq P r for any i ă |sq q |,
  (c) ρ, ρ1 |ù Ppsq pi q Ěr Ppsq qi q for any i ă |sq q |,
 (d) sq pi ÑE sq pi`1 iff sq qi ÑE sq qi`1 for any i ă |sq q | ´ 1.
With (a) the assumed triple ρ |ù tR, P u p tQ, Gu gets applicable to sq p yielding
sq p P Out Q X Prog G which is in turn used to establish sq q P Out Q1 X Prog G1 .
    First, suppose Ppsq qi q “ skip with some i ă |sq q |. Then Ppsq pi q “ skip
follows by (c). Hence, sq p P Out Q entails some j ď i such that sq pj is a skip-
configuration and Spsq pj q P Q. From (b) and (c) we further infer that sq qj must
be also a skip-configuration and pSpsq pj q, Spsq qj qq P r holds. That is, Spsq qj q is
in the image of Q under r and hence Spsq qj q P Q1 follows by (3).
    Second, in order to show sq q P Prog G1 suppose there is some i ă |sq q | ´ 1
with a program step ρ1 $ sq qi ÑP sq qi`1 . Hence from (d) follows that there must
be also a program step at the same position on sq p , i.e. ρ $ sq pi ÑP sq pi`1 , so
that sq p P Prog G entails pSpsq pi q, Spsq pi`1 qq P G. Then pSpsq qi q, Spsq qi`1 qq P G1
follows by (4) since both, pSpsq pi q, Spsq qi qq P r and pSpsq pi`1 q, Spsq qi`1 qq P r, are
provided by (b).
    This proposition can also be viewed as a generalisation of the principle, usu-
ally called ‘the rule of consequence’: from a valid triple ρ |ù tR, P u p tQ, Gu one
obtains valid triples replacing R or P by a stronger relation/condition whereas
G or Q – by a weaker. Another key result of Proposition 5.2.1 is:
Corollary 5.2.2. If ρ |ù p « q then ρ |ù tR, P u p tQ, Gu iff ρ |ù tR, P u q tQ, Gu.
Proof. With id in place of r, the conditions (1)–(4) of Proposition 5.2.1 hold by
the reflexivity of Ď. We apply this instance to ρ |ù p Ě q and to ρ |ù q Ě p.
    In other words, equivalent programs exhibit the same rely/guarantee prop-
erties. Taking for example the jump-transformation

      ρ |ù if C then p else ρ j fi « cjump C to j otherwise p end

established by Proposition 3.4.1, any property derived within the program logic
for if C then p else ρ j fi applies to the counterpart on the rhs as well.

                                              37
A Hoare-style Rely/Guarantee Program Logic


5.3     Rules for skip and basic
This section commences the syntax-driven part of the rely/guarantee program
logic which comprises the rules whose successive application allows us to turn
triples into verification conditions using backwards reasoning guided by the pro-
gram syntax. Note however that the syntax-driven approach is hardly applica-
ble to programs carrying only little syntactic structure: programs that deploy
while-statements are decisively more amenable to generation of verification con-
ditions than those which use only jumps. This framework is therefore basically
not aimed at verifying properties of any possible program but only of those that
are provably equivalent to some jump-free program for which the verification
conditions are actually generated. A particular consequence of this indirection
is that a rule for cjump as well as code retrieving functions are omitted in the
syntax-driven part.
Proposition 5.3.1. |ù tR, P u skip tP, Gu.
Proof. A computation sq P vskipw has no program steps and hence satisfies any
program condition, whereas sq P Out P holds because sq P In P is assumed.
Proposition 5.3.2. Assume
 (1) R ¨ P Ď P ,
 (2) P Ď tσ | f σ P Q ^ pσ, f σq P Gu.
Then |ù tR, P u basic f tQ, Gu.
Proof. Let sq P Env R X In P X vbasic f w. If sq does not perform any program
steps then sq P Out Q X Prog G holds trivially. Otherwise let sq n ÑP sq n`1 be
the first program step, i.e. sq n “ pbasic f, σn q and sq n`1 “ pskip, f σn q must
hold with some σn and, moreover, for any m ă n we have only environment
steps sq m ÑE sq m`1 . Thus, by (1) and Spsq 0 q P P we can further induce σn P P
so that f σn P Q and pσn , f σn q P G follow by (2). Using this, sq P Prog G can
be inferred because sq does not have any other program steps from n ` 1 on,
i.e. n`1 |sq P vskipw, whereas sq P Out Q follows since sq n`1 is the first skip-
configuration on sq.
    The assumption (1) in Proposition 5.3.2 is usually called a stability assump-
tion: any environment step retains the precondition P , which is a general ap-
proach to reasoning about interference freedom. It is also worth noting that
skip is the only language constructor that can get away without a stability
assumption as Proposition 5.3.1 has shown.

                                       38
5.4. A RULE FOR THE PARALLEL COMPOSITION OPERATOR


5.4      A rule for the parallel composition operator
The following rule and the proof are, in essence, extensions of the rule and the
proof given by Stirling [9] for the binary operator p k q.

Proposition 5.4.1. Let I “ t1, . . . , mu with m ą 0. Furthermore, let G be a
reflexive state relation and assume
            Ş
  (1) P Ď kPI Pi ,
            Ş
  (2) R Ď kPI Ri ,
                            Ş
  (3) |ù tRk , Pk u pk tQk , lPI ztkuRl X Gu for any k P I,

 (4) Rk ¨ Qk Ď Qk for any k P I,
     Ş
 (5) kPI Qk Ď Q.

Then |ù tR, P ukp1 , . . . , pm tQ, Gu.

Proof. Let sq P Env R X In P X v kp1 , . . . , pm w and let sq 1 be the longest prefix
of sq that does not contain a skip-configuration. First, note that if sq does not
contain such a configuration at all then sq 1 “ sq holds. Second, as sq 1 is not
empty we have sq 1 P Env R X In P X v kp1 , . . . , pm w. Third, the program part of
each configuration on sq 1 has the form ku1 , . . . , um , e.g. Ppsq 10 q “ kp1, . . . , pm .
    For each k P I we can thus derive a computation sq k P vpk w from sq 1 such
that |sq k | “ |sq 1 | for all k P I and moreover the following conditions are met:

 (a) Ppsq 1i q “ kPpsq 1i q, . . . , Ppsq m
                                          i q for any i ă |sq |,
                                                             1



 (b) Spsq 1i q “ Spsq ki q for any i ă |sq 1 | and k P I,

  (c) if i ă |sq 1 | ´ 1 then sq 1i ÑE sq 1i`1 iff sq ki ÑE sq ki`1 holds for all k P I.

Note that sq k P In Pk follows for any k P I by (1) and (b).
                                             k
   Next, we show by contradiction that sq  Ť P Env Rk also holds for any k P I.
Assuming the opposite, the set of indices kPI Mk where
           def
      Mk “ ti | i ă |sq 1 | ´ 1 ^ sq ki ÑE sq ki`1 ^ pSpsqi q, Spsqi`1 qq R Rk u
                                                         Ť
is not empty. Then let µ be the least element of kPI Mk and let kµ P I be
chosen such that µ P Mkµ . Further, there must be some n P I with a program
step sq nµ ÑP sq nµ`1 : would sq nµ ÑE sq nµ`1 hold for all n P I then we could first

                                              39
A Hoare-style Rely/Guarantee Program Logic


infer sq 1µ ÑE sq 1µ`1 by (c), then pSpsqµ q, Spsqµ`1 qq P R since sq P Env R, and
hence pSpsqµ q, Spsqµ`1 qq P Rkµ by (2) in contradiction to µ P Mkµ . Combined
with the minimality ofŞµ this means µ`2 |sq n P Env Rn . With µ`2 |sq n P In Pn we
obtain µ`2 |sq n P Progp lPI ztnuRl X Gq by (3) and since kµ P I ztnu holds due to
µ R Mn , for the program step sq nµ ÑP sq nµ`1 we infer pSpsqµ q, Spsqµ`1 qq P Rkµ
which once more contradicts µ P Mkµ .
     The intermediate result is that sq k P vpk w X In Pk X Env Rk holds for each
k P I. Hence sq k P Out Qk X Prog G can be inferred for all k P I using (3) with
subsequent weakening of the program condition. This conclusion will be utilised
below to establish sq P Out Q X Prog G.
     First, to show sq P Out Q let n “ |sq 1 | and suppose there is some j ă |sq|
with Ppsq j q “ skip. Then j ě n must hold because sq 1 does not contain any
skip-configurations. Moreover, the step of sq at the position n ´ 1 must be a
program step to the first skip-configuration. That is, we have sq n´1 ÑP sq n
with sq n´1 “ pkskip, . . . , skip, σq and sq n “ pskip, σq and some state σ for
which σ P Q has to be established. Let k P I be fixed to this end. Using (a)
we can infer sq kn´1 “ pskip, σq such that from sq k P Out Qk the existence of an
index ik ď n ´ 1 with sq kik “ pskip, σik q and σik P Qk follows. Furthermore, this
property can be extended to Spsq kl q P Qk for all l ě ik using (4) since there   Ş are
only environment steps from ik on. Altogether, we can conclude σ P kPI Qk
and hence σ P Q is a consequence of (5).
     Second, to show sq P Prog G let n “ |sq 1 | and suppose sq i ÑP sq i`1 with
i ă |sq| ´ 1. Note that i ă n holds: i ě n implies Ppsq n q “ skip and hence
there would be only environment steps from n on. Further, if i “ n ´ 1 then
sq i “ pkskip, . . . , skip, σq and sq i`1 “ pskip, σq must hold with some state σ
and hence pσ, σq P G follows by the reflexivity assumption. Finally, if i ă n ´ 1
then (c) provides the existence of a program step sq ki ÑP sq ki`1 with k P I so
that pSpsq i q, Spsq i`1 qq “ pSpsq ki q, Spsq ki`1 qq P G follows from sq k P Prog G.

   With m “ 2, Proposition 5.4.1 can be simplified to a more convenient form:

Corollary 5.4.2. If G is a reflexive state relation and

 (1) P Ď P1 X P2 ,

 (2) R Ď R1 X R2 ,

 (3) |ù tR1 , P1 u p1 tQ1 , R2 X Gu,

 (4) |ù tR2 , P2 u p2 tQ2 , R1 X Gu,

                                          40
5.4. A RULE FOR THE PARALLEL COMPOSITION OPERATOR


 (5) R1 ¨ Q1 Ď Q1 ,
 (6) R2 ¨ Q2 Ď Q2 ,
 (7) Q1 X Q2 Ď Q
then |ù tR, P u p1 k p2 tQ, Gu.

An example
The rules in this section enable structured reasoning upon properties of pro-
grams with interleaved computations, but are far from being complete and the
renown ‘parallel increment’ example
                   def
      parallel-inc “ x :“ x ` 1 k x :“ x ` 1

will be used below to substantiate the claim. As a preparation to that, we first
describe how actual programs working on actual states can be represented.
    In what follows, any state σ on which a program operates comprises a map-
ping that sends each state variable occurring in the program (such as x in
parallel-inc above) to a value of a fixed type assigned to the variable, e.g. σx is
an integer in parallel-inc. Then an assignment of a value, denoted by an appro-
priately typed logical term t, to a state variable a amounts to the indivisible
step basicpλσ. σra :“ ts q with the updated state σra:“ts that sends a to the value
of t and any b ‰ a to σb. Note that if a state variable appears in t then
it actually stands for its image under σ. Thus, the assignment x :“ x ` 1 is
essentially a shorthand for basicpλσ. σrx :“ σx`1s q. Similar conventions apply
to state predicates: for instance a “ 0 stands for tσ | σa “ 0u. Furthermore,
primed variables will be used to capture state relations: e.g. a “ a1 ^ b “ a1 is
the same as tpσ, σ 1 q | σa “ σ 1 a ^ σb “ σ 1 au.
    Continuing with the ‘parallel increment’ example, let σ be a state assigning
some integer value to the only state variable x and consider the triple:

      |ù tK, x “ 0u parallel-inc tx “ 2, Ju                                       (5.1)

Since the rely condition K confines the scope of reasoning to the actual computa-
tions of parallel-inc, it is yet attainable to verify that (5.1) is indeed a property of
parallel-inc by plain unfolding Definition 5.1.1: this requires checking Outpx “ 2q
only for seven computations that start with the state σrx:“0s and perform up to
three program steps: Figure 5.1 depicts the relevant transition subgraph where
all environment steps are particularly omitted.

                                          41
A Hoare-style Rely/Guarantee Program Logic



                                pparallel-inc, σrx:“0s q



                          ✛                                        ✲
pskip k x :“ x ` 1, σrx:“1s q                              px :“ x ` 1 k skip, σrx:“1s q


                                      ✲
                                            ✛
                              pskip k skip, σrx:“2s q


                                          ❄
                                   pskip, σrx:“2s q


                Figure 5.1: A transition subgraph of parallel-inc.


   On the other hand, it is impossible to derive the same property immediately
by the rule in Corollary 5.4.2: assuming the opposite means that we have found
some Ri , Pi , Qi with i P t1, 2u such that
 (a) px “ 0q Ď P1 X P2 ,

 (b) |ù tR1 , P1 u x :“ x ` 1 tQ1 , R2 u,
 (c) |ù tR2 , P2 u x :“ x ` 1 tQ2 , R1 u,
 (d) Q1 X Q2 Ď px “ 2q.
        def
Let sq “ px :“ x ` 1, σrx:“0s q ÑP pskip, σrx:“1s q be a one-step computation
for which we have sq P Env K X vx :“ x ` 1w by construction. Furthermore,
sq P In P1 X In P2 can be inferred from (a) allowing us to apply (b) and (c) to
sq in order to obtain σrx:“1s P Q1 and σrx:“1s P Q2 such that σrx:“1s P px “ 2q
follows using (d), which is evidently a contradiction.
    This outcome shall however not lead to the hasty conclusion that (5.1) would
not be derivable by the rules at all, for it is: we can deploy two auxiliary variables
(each local to one of the parallel components) keeping their sum equal to x. This
allows us to establish a generalised property by an application of the parallel
rule. Then deriving the triple (5.1) in principle amounts to ‘discarding’ the

                                            42
5.5. A RULE FOR THE SEQUENTIAL COMPOSITION OPERATOR


auxiliaries by means of the program correspondence rule in the same way as it
will be accomplished in the case study Chapter 6, where auxiliary variables are
deployed for the same purpose: an application of the rule in Corollary 5.4.2.


5.5      A rule for the sequential composition oper-
         ator
The extra assumption (3) in the following statement will be justified below.
Proposition 5.5.1. Assume G is a reflexive state relation and
 (1) |ù tR, P u p tS, Gu,
 (2) |ù tR, Su q tQ, Gu,
 (3) q “ skip implies R ¨ Q Ď Q.
Then |ù tR, P u p; q tQ, Gu.
Proof. Suppose sq P Env R X In P X vp; qw. Further, let sq 1 be its longest prefix
that does not reach a configuration of the form pskip; q, σq and let n “ |sq 1 |.
Then for any i ă n there is some ui such that Ppsq i q “ ui ; q holds.
     If sq does not reach a configuration of the form pskip; q, σq then we have
sq 1 “ sq and Ppsq i q “ ui ; q for all i ă |sq|. This particularly means that there
are no skip-configurations on sq, i.e. sq P Out Q holds trivially. We can further
define sq pi “ pui , Spsq i qq for all i ă |sq| inheriting the respective transitions of
             def


sq. This construction provides sq p P Env R X In P X vpw such that we can infer
sq p P Out S X Prog G using (1). Then sq P Prog G follows from sq p P Prog G.
     Otherwise we have n ă |sq| and sq n “ pskip; q, σn q. In that case we define
   p def
sq i “ pui , Spsq i qq for all i ď n. In particular, |sq p | “ n ` 1 and sq pn is the first
skip-configuration on sq p . Since sq p P Env R X In P X vpw holds once more by
construction, we also infer sq p P Out S X Prog G using (1). Note however that
in contrast to the preceding case, σn P S now follows from sq p P Out S.
     Further, if sq has only environment steps from n on then sq P Out Q once
more holds trivially, whereas sq P Prog G is a consequence of sq p P Prog G.
     Otherwise, suppose sq makes a program step at m with n ď m ă |sq| ´ 1
and let m0 be the least such index, i.e. sq n ÑE . . . ÑE sq m0 ÑP sq m0 `1 with
sq m0 “ pskip; q, σm0 q and sq m0 `1 “ pq, σm0 q. For each configuration sq k with
n ď k ď m0 we thus have Ppsq k q “ skip; q and can derive the computation
sq q0 “ pq, σn q ÑE . . . ÑE pq, σm0 q which is composable with the suffix m0 `1 |sq.

                                            43
A Hoare-style Rely/Guarantee Program Logic

              def
Then let sq q “ sq q0 ’ m0 `1 |sq such that sq q P Out Q X Prog G follows from (2)
since sq q P Env R X In S X vqw is provided by this construction.
     Next we will show the output condition sq P Out Q. To this end let j ă |sq|
be an index with Ppsq j q “ skip. Then j ą m0 must hold, whereas j “ m0 ` 1
would entail q “ skip. In case q “ skip we have sq q P vskipw. In combination
with sq q P Out Q this yields σn P Q. Furthermore, using (3) we can thus induce
that Spsq qi q P Q holds for any i ă |sq q | and for Spsq qm0 ´n q in particular. Since
Spsq qm0 ´n q “ σm0 “ Spsq m0 `1 q we can conclude this case. With q ‰ skip as an
additional assumption, j ą m0 ` 1 follows by the above remarks. Thus, we have
Ppsq qj´n´1 q “ Ppsq j q “ skip such that sq q P Out Q entails some i ď j ´ n ´ 1
with Ppsq qi q “ skip and Spsq qi q P Q. If i ď m0 ´ n then we get a contradiction
in form of q “ skip. With i ą m0 ´ n we can first infer j ě i ` n ` 1 ą m0 ` 1,
and then Ppsq i`n`1 q “ Ppsq qi q “ skip and Spsq i`n`1 q “ Spsq qi q P Q.
     Finally, the program condition sq P Prog G follows from sq p P Prog G and
   q
sq P Prog G if we additionally take into account that the step sq m0 ÑP sq m0 `1 ,
omitted by the composition sq q0 ’ m0 `1 |sq , is covered by G as well since G is
assumed to be reflexive.
    That the assumptions (1) and (2) alone are not generally sufficient to remain
sound in presence of the purely auxiliary yet indispensable skip-operator can
be substantiated as follows. Suppose Proposition 5.5.1 would be valid without
              def
(3) and let p “ b :“ a ` 1; skip. Hence, |ù ta “ a1 , a “ 0u p tb “ 1, Ju would
be a consequence of
 |ù ta “ a1 , a “ 0u b :“ a ` 1 tb “ 1, Ju and
 |ù ta “ a1 , b “ 1u skip tb “ 1, Ju
where the former follows by Proposition 5.3.2 and the latter is just an instance
of Proposition 5.3.1. On the other hand, starting with some state σ P pa “ 0q
the three-step computation
 pp, σq ÑP pskip; skip, σrb:“1s q ÑE pskip; skip, σrb:“0s q ÑP pskip, σrb:“0s q
clearly satisfies Env pa “ a1 q X In pa “ 0q X vpw but not Out pb “ 1q.
    The statement of Proposition 5.5.1 is consequently not applicable to this
example: the respective instance of assumption (3) cannot be satisfied since the
postcondition b “ 1 is not stable under the rely a “ a1 .


5.6      A rule for while-statements
Proposition 5.6.1. Assume G is a reflexive state relation and

                                          44
5.6. A RULE FOR WHILE-STATEMENTS


 (1) R ¨ P Ď P ,

 (2) |ù tR, P X Cu p tP, Gu,

 (3) |ù tR, P X Cu q tQ, Gu.

Then |ù tR, P u while C do p subsequently q od tQ, Gu.

Proof. Let pwhile stand for while C do p subsequently q od. We have to show
sq P Out Q X Prog G for any sq P vpwhile w X Env R X In P and proceed to this
end by induction on the length of sq, which yields the induction hypothesis:

(H) sq 1 P Out Q X Prog G holds for any sq 1 P vpwhile w X Env R X In P with the
    length less than the length of sq, i.e. |sq 1 | ă |sq|.

However, only the following consequence of (H) will be employed below:

 (4) if sq 1 is a proper non-empty suffix of sq such that sq 10 “ ppwhile , σq holds
     with some σ P P then sq 1 P Out Q X Prog G.

If sq has no program steps then we are done. Otherwise we may assume that the
first transition of sq is a program step, because would we have sq 0 ÑE sq 1 then
1
  |sq would be a proper non-empty suffix of sq such that 1 |sq 0 “ sq 1 “ ppwhile , σq
with some σ P P due to (1) and hence 1 |sq P Out Q X Prog G follows from (4).
     That is, for the remainder of the proof we can assume sq 0 ÑP sq 1 such that
sq 0 “ ppwhile , σ0 q and sq 1 “ px, σ0 q hold with some x and σ0 P P .
     If σ0 R C then we have x “ q and 1 |sq P vqw X Env R X InpP X Cq. Hence
(3) entails 1 |sq P Out Q X Prog G and we can conclude sq P Out Q X Prog G by
the reflexivity of G.
     If σ0 P C then 1 |sq P vp; skip; pwhile w X Env R X In pP X Cq. Further, let sq 1
be the longest prefix of the suffix 1 |sq which does not reach a configuration of
the form pskip; skip; pwhile , σq with some state σ, and let n1 “ |sq 1 |. Then for
any i ă n1 we have some ui ‰ skip with Ppsq i`1 q “ ui ; skip; pwhile .
     If sq 1 “ 1 |sq then sq has no skip-configurations at all and hence sq P Out Q
holds trivially. We can further define the computation sq pi “ pui , Spsq i`1 qq for
                                                                 def


all i ă n1 inheriting the respective transitions of sq. Then sq P Prog G follows
from the reflexivity of G and sq p P Prog G which in turn follows from (2) since
we have sq p P vpw X Env R X In pP X Cq by construction.
     Otherwise we can assume n1 ă |sq| ´ 1 and define sq pi “ pui , Spsq i`1 qq now
                                                               def


for all i ď n1 . Then sq p P Out P X Prog G follows once more from (2) because
sq p P vpw X Env R X In pP X Cq still holds by construction. Furthermore, note

                                         45
A Hoare-style Rely/Guarantee Program Logic


that sq pn1 is the first skip-configuration on sq p . Translating these results to
sq we obtain sq n1 `1 “ pskip; skip; pwhile , σn1 `1 q with σn1 `1 P P and conclude
n1 `1
      |sq P vskip; skip; pwhile w X Env R X In P .
     In case there are not at least two program steps: from skip; skip; pwhile to
skip; pwhile and then from skip; pwhile to pwhile , the output condition sq P Out Q
once more holds trivially, whereas sq P Prog G follows from sq p P Prog G and the
reflexivity of G.
     Otherwise there must be some index n2 such that n1 ` 2 ă n2 ă |sq| and
sq n2 “ ppwhile , σn2 q hold. Using σn1 `1 P P and the stability assumption (1) we
can further induce σn2 P P , such that the hypothesis (4) is applicable to n2 |sq
yielding n2 |sq P Out Q X Prog G.
     To establish the output condition sq P Out Q in this last branch, let j ă |sq|
be an index with Ppsq j q “ skip. By the above follows that n2 ă j must hold,
i.e. Ppn2 |sq j´n2 q “ skip. Then n2 |sq P Out Q entails some i ď j ´ n2 such that
n2
   |sq i “ sq i`n2 “ pskip, σi`n2 q with some σi`n2 P Q.
     Lastly, sq P Prog G is a consequence of sq p P Prog G, n2 |sq P Prog G and the
reflexivity of G.


5.7     A rule for await-statements
The main difficulty with triples of the form |ù tR, P u await C do p od tQ, Gu is
to capture that any state σ before entering p is related by G to any state where
p might terminate when run in isolation starting with σ. As opposed to the
one-step state transformers (cf. Proposition 5.3.2), such runs of p can comprise
series of program steps and it would be rather very limiting to require from each
of them to comply with a transitive G. Therefore in the assumption (2) below,
σ represents a state before entering p and is also invoked in the postcondition to
link it to terminal states of p by means of the guarantee G. The same technique
can be encountered by Nieto [11, 20]. It is also worth noting that deploying the
assumption pP X Cq ˆ Q Ď G instead is in principle possible but would result
in a considerably weaker rule since pP X Cq ˆ Q generally gives only a rough
over-approximation of the actual input/output behaviour of p restricted to the
domain P X C.

Proposition 5.7.1. Assume

 (1) R ¨ P Ď P ,

 (2) |ù tK, P X C X tσuu p ttσ 1 | σ 1 P Q ^ pσ, σ 1 q P Gu, Ju for any state σ.

                                        46
5.8. A RULE FOR CONDITIONAL STATEMENTS


Then |ù tR, P u await C do p od tQ, Gu.
Proof. Let sq P Env R X In P X vawait C do p odw. If sq does not perform any
program steps then we are done. Next, suppose sq i ÑP sq i`1 with i ă |sq|´1 is
the first such step. Then sq i “ pawait C do p od, σi q and sq i`1 “ pskip, σi`1 q
                                 n
such that σi P C and pp, σi q ÑP pskip, σi`1 q with some n P N hold. Further,
noting that σi P P is induced by Spsq 0 q P P and the stability assumption (1),
we can derive sq p P Env K X In pP X Cq X vpw with |sq p | “ n ` 1, Spsq p0 q “ σi as
the initial and Spsq pn q “ σi`1 as the final state.
    Thus, we infer sq p P Outptσ 1 | σ 1 P Q ^ pσi , σ 1 q P Guq instantiating σ by σi in
(2), which yields σi`1 P Q and pσi , σi`1 q P G. Then sq P Out Q follows as sq i`1
is the first skip-configuration on sq, and sq P Prog G – since i`1 |sq P vskipw.


5.8      A rule for conditional statements
Proposition 5.8.1. Assume G is a reflexive state relation and
 (1) R ¨ P Ď P ,
 (2) |ù tR, P X Cu p tQ, Gu,
 (3) |ù tR, P X Cu q tQ, Gu.
Then |ù tR, P u if C then p else q fi tQ, Gu.
Proof. Let sq P Env R X In P X vif C then p else q fiw. If sq has no program
steps then we are done. Otherwise let sq i ÑP sq i`1 with i ă |sq| ´ 1 be the first
such step. Hence we have sq i “ pif C then p else q fi, σq and sq i`1 “ px, σq
with some x and σ. Further, note that the stability (1) and sq P In P induce
σ P P . If σ P C then x “ p and i`1 |sq P Env R X In pP X Cq X vpw follow. Thus,
with (2) we can first infer i`1 |sq P Out Q X Prog G and then sq P Out Q X Prog G.
The case σ R C is entirely symmetric.


5.9      A brief summary
Starting with the definition of the extended Hoare triples, this section was ded-
icated to the rely/guarantee program logic presenting the program correspon-
dence rule as well as a rule for each of the language constructors except cjump.
Although a rule for processing conditional jumps could simply be derived via
the program equivalence in Proposition 3.4.1 combined with Proposition 5.8.1,

                                           47
A Hoare-style Rely/Guarantee Program Logic


the actual purpose of the program logic is to enable syntax-driven generation
of verification conditions to extended Hoare triples with structured (i.e. jump-
free) programs only, as pointed out at the beginning of Section 5.3. Indirect
reasoning upon rely/guarantee properties of the corresponding programs using
jumps is complementary backed by Proposition 3.4.1 and Proposition 3.4.2.




                                      48
Chapter 6

Case Study: Peterson’s
Mutual Exclusion
Algorithm

This chapter embarks on the first part of the case study consisting of three
parts concerned with structured derivations of the relevant properties of thread 0
and thread 1 that are shown in Figure 6.1 and shall model the threads in the
algorithm by Peterson [21]. The definitions are respectively parameterised by
the logical variables cs 0 and cs 1 being thus the placeholders for whatever needs
to be accomplished within the critical sections since they can be instantiated by
any term of type Lτ for any particular type of states τ . The parallel composition
of the threads
                      def
      mutex cs 0 cs 1 “ thread 0 cs 0 k thread 1 cs 1

consequently models the actual protocol parameterised by the contents of the
critical sections. Note that this modelling is not tailored to transformations
to some low-level representations in particular due to the compound conditions
flag1 ^ turn and flag0 ^ turn as none of them could normally be evaluated by
means of one indivisible step, i.e. without interleaving. Nonetheless, this form
fits better to the the main goal of the case study: to illustrate the applicability
of the proposed methods without delving into lots of technical, yet eventually
important details deferred to Section 11.3.

                                           49
Case Study: Peterson’s Mutual Exclusion Algorithm



                    def
       thread 0 cs 0 “    flag0 :“ True;
                          turn :“ True;
                          while flag1 ^ turn do skip od;
                          cs 0 ;
                          flag0 :“ False

                    def
       thread 1 cs 1 “    flag1 :“ True;
                          turn :“ False;
                          while flag0 ^ turn do skip od;
                          cs 1 ;
                          flag1 :“ False


          Figure 6.1: Two threads in the mutual exclusion algorithm.


    It should be intuitively clear that the behaviours of mutex cs 0 cs 1 and the
plain uncontrolled composition cs 0 k cs 1 may substantially differ whenever cs 0
and cs 1 access some shared resource for reading and writing. More specifically,
many input/output properties that can be derived for mutex cs 0 cs 1 from prop-
erties of cs 0 and cs 1 just basically do not hold for cs 0 k cs 1 precisely because
mutex cs 0 cs 1 enables certain privileged conditions to cs 0 and cs 1 regarding in-
terleaving. The central goal of this section is to encapsulate by means of a single
generic rule the program logical steps transforming properties of cs 0 and cs 1 to
properties of mutex cs 0 cs 1 .
    First of all, in order to pin down the mentioned privileged conditions, let
shared be a state variable representing the resource to which both threads may
request access for reading and writing. Further, let P0 , Q0 and P1 , Q1 be some
given predicates on the values of shared so that e.g. by P0 shared (as explained
in Section 5.4 this is actually a shorthand for the set of states tσ | P0 σsharedu)
we can address the precondition of the critical section cs 0 and by Q0 shared
– its postcondition. Thus, the properties that the critical sections shall exhibit
in presence of interleaving can initially be sketched by means of the following
extended Hoare triples:

 |ù tshared “ shared1 ^ . . . , P0 sharedu cs 0 tQ0 shared, . . .u
 |ù tshared “ shared1 ^ . . . , P1 sharedu cs 1 tQ1 shared, . . .u

Among the relies, the equation shared “ shared1 in principle makes out the

                                        50
half of the privileged conditions: each critical section can locally assume that
the opposite thread does not modify shared, addressing thus the core effect
of mutual exclusion. Another half of the privileged conditions will accordingly
amount to the absence of the same equation among the yet entirely open guar-
antees: its presence there would simply preclude any modifications of shared
within cs 0 and cs 1 , confining the scope of reasoning to instances of cs 0 and cs 1
for which cs 0 k cs 1 would actually be a more efficient alternative to mutex cs 0 cs 1 .
    Examining mutex in more detail reveals that the condition flag1 ÝÑ turn
(i.e. flag1 _ turn) is sufficient for thread 0 to enter its critical section. How-
ever, the condition is not stable: suppose an evaluation of mutex is in a state σ
with σflag1 ^ σturn because thread 1 did not set flag1 yet such that by doing
so the evaluation runs into a state σ 1 with σ 1 flag1 ^ σ 1 turn. Without being
relevant for the behaviour of mutex, this instability poses a considerable prob-
lem from the verification perspective since practically each of the rely/guarantee
program logic rules asserts stability in some form. Deploying auxiliary variables
often leads to a solution in such situations. In this case, a weaker condition
      ‘thread 1 did not modify turn yet’ _ flag1 _ turn                            (6.1)
shall be captured by means of auxiliaries. Firstly, (6.1) is stable: if thread 1
sets flag1 then this happens entirely before it modifies turn due to the relative
order of these two assignments. Secondly, (6.1) is sufficient as well: thread 0 may
safely enter its critical section in particular when thread 1 did not modify turn
yet, no matter what the values of flag1 and turn are.
    Reifying this plan, the programs thread aux0   and thread aux
                                                              1   in Figure 6.2 re-
spectively deploy the variables turn aux0 and turn aux1 within the two extra
created atomic sections ensuring that e.g. turn aux1 is set by thread 1 without
any interruptions following the modification of turn. The essential effect is that
we get σturn aux1 ^ σturn where σ denotes any state that thread aux     1   reaches
by processing its atomic section. The auxiliary model of the mutual exclusion
algorithm is then accordingly defined by
      mutex aux cs 0 cs 1 “ thread aux             aux
                          def
                                   0 cs 0 k thread 1 cs 1

It is quite justified to conjecture what will be elaborated later on, namely that
the auxiliaries do not affect the behaviour of the actual mutex model whatso-
ever. Therefore without imposing any constraints on mutex itself we can also
presume that turn aux1 and turn aux2 initially hold so that (6.1) becomes
  turn aux1 _ flag1 _ turn.
    Summing up, the states on which mutex and mutex aux operate are shaped as
follows. First, the variables flag0 , flag1 and turn carry the Boolean values used

                                           51
Case Study: Peterson’s Mutual Exclusion Algorithm



           thread aux
                        def
                  0 cs 0 “     flag0 :“ True;
                              xturn :“ True;
                               turn aux0 :“ Truey;
                               while flag1 ^ turn do skip od;
                               cs 0 ;
                               flag0 :“ False

           thread aux
                        def
                  1 cs 1 “     flag1 :“ True;
                              xturn :“ False;
                               turn aux1 :“ Truey;
                               while flag0 ^ turn do skip od;
                               cs 1 ;
                               flag1 :“ False


            Figure 6.2: The threads augmented by the auxiliary variables.

for communication between threads. Second, the Boolean values of turn aux0
and turn aux1 will serve the verification purposes only, as explained above.
Third, there are shared, local0 , local1 whose exact type can remain open yet.
The variables local0 and local1 are respectively laid out for cs 0 and cs 1 to
make a local ‘snapshot’ of shared before submitting a modified value back to
shared.
    To render the subsequent argumentation in a more structured way, let
              def
    cond0 “ turn aux1 ^ flag1 ÝÑ turn
          def
    cond1 “ turn aux0 ^ flag0 ÝÑ turn
and consider the extended Hoare triple
|ù tR0 ,     turn aux0 ^ P0 sharedu thread aux
                                           0 cs 0 tQ0 shared, R1 u          (6.2)
where R0 denotes the rely condition
 flag0 “ flag10 ^ turn aux0 “ turn aux10 ^ local0 “ local10 ^               paq
 pturn aux0 ^ flag0 ^ cond0 ÝÑ shared “ shared1 q ^                         pbq
 pcond0 ÝÑ cond10 q ^                                                       pcq
 pP0 shared ÝÑ P0 shared1 q ^ pQ0 shared ÝÑ Q0 shared1 q                    pdq
whose interpretation is given line-by-line below:

                                           52
 (a) no step of thread aux
                       1   ever modifies flag0 , turn aux0 and local0 ;

 (b) the value of shared is retained by any program step of thread aux     1   from
     any state σ where thread aux
                                0   is requesting   the exclusive access to  shared
     (i.e. the condition σturn aux0 ^ σflag0 holds) and the request may be
     regarded as granted (i.e. σcond0 holds as well); note that this in particular
     applies when thread aux
                          0   is inside its critical section;

 (c) cond0 is stable;

 (d) each step of thread aux
                         1   retains the pre- and the postcondition of cs 0 ; the
     extent, to which actions of cs 1 on the shared resource must be constrained
     in order to protect what cs 0 achieves, varies for each particular instance
     of P0 and Q0 : the threads have to cooperate in this sense to eventually
     reach the intersection of Q0 shared and Q1 shared together.

As one might expect, the guarantee R1 in (6.2) is entirely symmetric to R0 :

flag1 “ flag11 ^ turn aux1 “ turn aux11 ^ local1 “ local11 ^
pturn aux1 ^ flag1 ^ cond1 ÝÑ shared “ shared1 q ^
pcond1 ÝÑ cond11 q ^
pP1 shared ÝÑ P1 shared1 q ^ pQ1 shared ÝÑ Q1 shared1 q

so that R0 and R1 just get swapped in the triple for thread aux
                                                            1 :

|ù tR1 , turn aux1 ^ P1 sharedu thread aux
                                       1 cs 1 tQ1 shared, R0 u

Regarding the critical sections, the extended Hoare triple

|ù tshared “ shared1 ^ local0 “ local10 , P0 sharedu cs 0 tQ0 shared, G0 u (6.3)

where G0 denotes the guarantee

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local1 “ local11 ^          (a)
 turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^                            (b)
 pP1 shared ÝÑ P1 shared1 q ^ pQ1 shared ÝÑ Q1 shared1 q                      (c)

captures the properties, parameterised by P0 , Q0 , P1 and Q1 , that cs 0 shall
exhibit. It will thus be assumed when deriving p6.2q in the next section. Note
once more the presence of shared “ shared1 among the rely conditions and its
absence in G0 which nonetheless requires from the program steps of cs 0

                                       53
Case Study: Peterson’s Mutual Exclusion Algorithm


 (a) not to modify flag0 , flag1 , turn as these are reserved for communication
     between the two threads as well as the variable local1 which is ‘owned’
     by thread aux
               1 ;

 (b) not to modify the auxiliary variables;

 (c) to retain the conditions P1 shared and Q1 shared in line with R1 .

Regarding cs 1 we accordingly assume

|ù tshared “ shared1 ^ local1 “ local11 , P1 sharedu cs 1 tQ1 shared, G1 u

where G1 denotes

flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local0 “ local10 ^
turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
pP0 shared ÝÑ P0 shared1 q ^ pQ0 shared ÝÑ Q0 shared1 q


6.1     Processing thread aux
                          0
The next goal is to establish (6.2) applying the rules of the rely/guarantee
program logic. For the first part of thread aux
                                            0   up to the critical section, i.e.

  thread pre
             def
         0   “      flag0 :“True;
                   xturn :“True;
                    turn aux0 :“Truey;
                    while flag1 ^ turn do skip od

we can derive the property

|ù tR0 , turn aux0 ^P0 sharedu
      thread pre
             0
   t flag0 ^ turn aux0 ^P0 shared ^ pflag1 ÝÑ       turnq, R1 u

using flag0 ^ turn aux0 ^ P0 shared and flag0 ^ turn aux0 ^ P0 shared as
the intermediate conditions which are both stable under R0 . Thus, it suffices
to derive the triple

|ù tR0 , flag0 ^ turn aux0 ^ P0 shared ^ pflag1 ÝÑ     turnqu
     cs 0                                                                    (6.4)
   t Q0 shared, R1 u

                                       54
6.2. THE INTERMEDIATE RESULT


to conclude (6.2). To this end we will appeal to the assumption (6.3) de-
spite the seeming discord: (6.3) intentionally relied on the privileged condi-
tion shared “ shared1 whereas R0 provides the same condition only under
the premise turn aux0 ^ flag0 ^ cond0 . In other words, the rely in the as-
sumed triple (6.3) is stronger than the rely in the anticipated conclusion (6.4).
This however makes merely the plain weakening, i.e. the program correspon-
dence rule (Proposition 5.2.1) with id in place of r, impossible but we apply the
rule instantiating r by a state relation that answers to the mentioned premise,
namely
       def
    r0 “ tpσ, σ 1 q | σ “ σ 1 ^ σturn aux0 ^ σflag0 ^ σcond0 u.

The proof obligations arising by an application of this instance of the program
correspondence rule to (6.3) and (6.4) are:

   - |ù cs 0 Ěr0 cs 0 which gets passed on to the mutex rule in form of an assump-
     tion, noting that it does not additionally constrain the set of admissible
     cs 0 instances as it merely requires from each step of cs 0 to retain the con-
     dition turn aux0 ^ flag0 ^ cond0 and this was anyway already captured
     by the guarantee G0 ;

   - r0 ˛ R0 Ď pshared “ shared1 ^ local0 “ local10 q ˛ r0 which holds since
     with r0 on the lhs we can derive shared “ shared1 from R0 and, moreover,
     cond0 ÝÑ cond10 is provided by R0 in order to establish r0 on the rhs;

   - flag0 ^ turn aux0 ^ P0 shared ^ pflag1 ÝÑ turnq Ď r0 ¨ pP0 sharedq
     which holds since flag1 ÝÑ turn entails cond0 ;

   - r0 ¨ pQ0 sharedq Ď Q0 shared which follows straight from r0 Ă id;

   - r0 ˛ G0 ˛ r0 Ď R1 which holds by the decisive property that the conditions
     turn aux0 ^ flag0 ^ cond0 and turn aux1 ^ flag1 ^ cond1 are mutually
     exclusive and hence in particular entail shared “ shared1 .


6.2     The intermediate result
What we achieved so far is to derive the extended Hoare triple

|ù tR0 , turn aux0 ^ P0 sharedu thread aux
                                       0 cs 0 tQ0 shared, R1 u


                                       55
Case Study: Peterson’s Mutual Exclusion Algorithm


by successive application of the program logical rules from Section 5 assuming

 |ù tshared “ shared1 ^ local0 “ local10 , P0 sharedu cs 0 tQ0 shared, G0 u

and |ù cs 0 Ěr0 cs 0 . In an entirely symmetric way we further derive

 |ù tR1 , turn aux1 ^P1 sharedu thread aux
                                       1   cs 1 tQ1 shared, R0 u

from the assumptions

 |ù tshared “ shared1 ^ local1 “ local11 , P1 shareducs 1 tQ1 shared, G1 u
                            def
and |ù cs 1 Ěr1 cs 1 with r1 “ tpσ, σ 1 q | σ “ σ 1 ^ σturn aux1 ^ σflag1 ^ σcond1 u.
   Regarding the auxiliary model mutex aux , i.e. thread aux                   aux
                                                               0 cs 0 k thread 1 cs 1 ,
we can thus conclude using the parallel composition rule (Corollary 5.4.2):

Proposition 6.2.1 (The auxiliary mutex rule). Assume
(1) |ù tshared “ shared1 ^ local0 “ local10 , P0 sharedu cs 0 tQ0 shared, G0 u
(2) |ù tshared “ shared1 ^ local1 “ local11 , P1 sharedu cs 1 tQ1 shared, G1 u
(3) |ù cs 0 Ěr0 cs 0
(4) |ù cs 1 Ěr1 cs 1 .
Then |ù tid, P0 shared ^ P1 shared ^ turn aux0 ^                 turn aux1 u
           thread aux             aux
                  0 cs 0 k thread 1 cs 1
        tQ0 shared ^ Q1 shared, Ju


6.3      A rule for mutex
Utilising this result, we once more resort to the program correspondence rule,
now instantiating r by the state relation
          def
     reqv “ tpσ, σ 1 q | σturn “ σ 1 turn ^ σshared “ σ 1 shared ^
                         p@i P t0, 1u. σflagi “ σ 1 flagi ^ σlocali “ σ 1 locali qu

i.e. the equivalence on states up to the values of the auxiliary variables. Thus, a
correspondence |ù p Ěreqv q allows us to transfer from p to q those state properties
that do not depend on the auxiliaries. For instance, Q shared is clearly such a
property for any Q. Hence, Qpσsharedq naturally entails Qpσ 1 sharedq provided
pσ, σ 1 q P reqv .

                                           56
6.4. AN APPLICATION OF THE mutex RULE


Proposition 6.3.1 (The mutex rule). Assume
(1) |ù tshared “ shared1 ^ local0 “ local10 , P0 sharedu cs 0 tQ0 shared, G0 u
(2) |ù tshared “ shared1 ^ local1 “ local11 , P1 sharedu cs 1 tQ1 shared, G1 u
(3) |ù cs 0 Ěr0 cs 0
(4) |ù cs 1 Ěr1 cs 1
(5) |ù cs 0 Ěreqv cs 0
(6) |ù cs 1 Ěreqv cs 1 .

Then |ù tid, P0 shared ^P1 sharedumutex cs 0 cs 1 tQ0 shared ^ Q1 shared, Ju.
Proof. Firstly, the triple
  |ù tid, P0 shared ^P1 shared ^ turn aux0 ^ turn aux1 u
        thread aux             aux
               0 cs 0 k thread 1 cs 1
     tQ0 shared ^ Q1 shared, Ju
follows by Proposition 6.2.1 using (1) – (4). Then we can apply Proposition 5.2.1
based on the correspondence
 |ù thread aux             aux
           0 cs 0 k thread 1 cs 1 Ěreqv thread 0 cs 0 k thread 1 cs 1

which follows by (5) and (6) since
 |ù xturn :“True; turn aux0 :“Truey Ěreqv turn :“True
and
 |ù xturn :“False; turn aux1 :“Truey Ěreqv turn :“False
can be derived using Proposition 3.2.14.
    To sum up, the assumptions (1) and (2) in the above rule are essential,
addressing in particular the input/output properties of the critical sections. As
opposed to that, (3)–(6) get routinely discarded when the rule is applied to
instances of cs 0 and cs 1 that sensibly avoid any form of access to the protocol
and the auxiliary variables.


6.4      An application of the mutex rule
As motivated at the beginning of the case study, by Proposition 6.3.1 we can
draw sound conclusions regarding the behaviour of the entire protocol for each

                                          57
Case Study: Peterson’s Mutual Exclusion Algorithm


appropriate instance of the critical sections as well as of the pre- and postcon-
ditions. In order to illustrate that, the critical sections will be instantiated by
programs, each adding an element to a shared set.
    Recall that the type of shared, local0 and local1 was left open as it is
basically immaterial to the functioning of the mutual exclusion protocol. Let
this type be int ñ bool, i.e. set of integers, in this example and the respective
tasks of the critical setions – to insert 0 and 1 to shared using local0 and
local1 . Thus, we instantiate cs 0 ÞÑ update 0 and cs 1 ÞÑ update 1 where
                def
       update 0 “ local0 :“ shared;
                  local0 :“ t0u Y local0 ;
                  shared :“ local0

                def
       update 1 “ local1 :“ shared;
                  local1 :“ t1u Y local1 ;
                  shared :“ local1

and show that upon termination of the mutex protocol, shared always contains
both, 0 and 1, i.e.

|ù tid, Ju mutex update 0 update 1 t0 P shared ^ 1 P shared, Ju.

The goal matches the conclusion of Proposition 6.3.1 if we set P0 and P1 to J,
Q0 to 0 P shared and Q1 to 1 P shared. Hence, to match its premises we first
need to establish

|ù tshared “ shared1 ^ local0 “ local10 , Ju update 0 t0 P shared, G01 u

where G01 is consequently the following instance of G0 :

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^
 local1 “ local11 ^ turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
 p1 P shared ÝÑ 1 P shared1 q.

The most intricate part constitutes the condition 1 P shared ÝÑ 1 P shared1
which update 0 can surely guarantee. As mentioned earlier, its purpose is to
ensure that update 0 does not compromise what update 1 is trying to accomplish,
i.e. does not remove 1 from shared in this instance.
    Similar observations can be made regarding the triple for update 1 :

|ù tshared “ shared1 ^ local1 “ local11 , Ju update 1 t1 P shared, G11 u

                                        58
6.4. AN APPLICATION OF THE mutex RULE


where G11 is the respective instance of G1 . The remaining proof obligations

|ù update 0 Ěr0 update 0
|ù update 1 Ěr1 update 1
|ù update 0 Ěreqv update 0
|ù update 1 Ěreqv update 1

can routinely be discarded by applying the syntax-driven correspondence rules
in Section 3.2.1 since both, update 0 and update 1 , avoid any form of access to
the state variables flag0 , flag1 , turn, turn aux0 and turn aux1 .




                                      59
Chapter 7

State Relations as Pre- and
Postconditions

A closer look at Definition 5.1.1 and the conclusion of the example application
of the mutex rule in the preceding chapter, i.e.
  |ù tid, Ju mutex update 0 update 1 t0 P shared ^ 1 P shared, Ju
reveals that the postcondition encircles the admissible values of shared in all
states where mutex update 0 update 1 might terminate without any accounts to its
initial values. So, for instance, shared could initially carry the set t2u, but t0, 1u
and t0, 1, 3u and the like would perfectly satisfy the postcondition although each
of the critical sections merely adds its entry to the shared resource. To come
up to that we however would need state relations rather than state predicates:
   shared Ď shared1 ^ 0 P shared1 ^ 1 P shared1
gives a more accurate postcondition which would allow us to conclude that
neither t0, 1u nor t0, 1, 3u can be an output with the input t2u.
    The insight is basically not new, and the problem is usually circumvented
by fixing initial values of relevant state variables by means of logical ‘link’ vari-
ables in preconditions in order to refer to these in postconditions. That is, in the
above example one could fix the initial value of shared by adding x “ shared
to the preconditions and refer to x in the postconditions by adding x Ď shared.
However, van Staden [13] in particular addresses this point by means of an ele-
gant approach leading to a systematic integration of the link variables technique
with the program logic.

                                         61
State Relations as Pre- and Postconditions


7.1      Generalising the extended Hoare triples
Firstly, taking a single state σ1 as a precondition allows us to use a state relation
Q as a postcondition that depends on the input: ρ |ù tR, tσ1 uu p tQ ¨ tσ1 u, Gu.
Note that resorting to a singleton set is decisive to this end because the plain
approach ρ |ù tR, P u p tQ ¨ P, Gu does not achieve the same effect with any P
for if σ 1 is in the image of P under Q, i.e. σ 1 P Q ¨ P , then there exists some
σ P P such that pσ, σ 1 q P Q which per se does not rule out pσ1 , σ 1 q R Q where
σ1 P P is the actual input state.
    Developing that further, ρ |ù tR, tσ1 uu p tQ ¨ tσ1 u, Gu in conjunction with
ρ |ù tR, tσ2 uu p tQ ¨ tσ2 u, Gu express that any sq P vpwρ X Env R X In ptσ1 , σ2 uq
satisfies the output condition OutpQ ¨ tSpsq 0 quq. Expressing the same using the
universal quantifier leads to @σ P tσ1 , σ2 u. ρ |ù tR, tσuu p tQ ¨ tσu, Gu. So with
a general parameter P in place of tσ1 , σ2 u the latter formula captures exactly
that if p terminates in a state σ 1 for an input state σ P P then pσ, σ 1 q P Q.
    The only deficiency in specifying the behaviour of a program pρ, pq by a set
of triples ρ |ù tR, tσuu p tQ ¨ tσu, Gu generated by σ P P is the blend of a state
relation Q as a postcondition with a state predicate P as a precondition, which
creates certain disbalance that poses particular challenges for reasoning about
sequential compositions and motivates the following definition.
Definition 7.1.1. Let pρ, pq be a program and R, P, Q, G – state relations. Then
ρ |ù2 tR, P u p tQ, Gu iff ρ |ù tR, tσuu p tQ ¨ tσ0 u, Gu holds for all pσ0 , σq P P .
    Next proposition essentially provides an alternative and slightly more suc-
cinct definition:
Proposition 7.1.1. ρ |ù2 tR, P u p tQ, Gu iff ρ |ù tR, P ¨ tσ0 uu p tQ ¨ tσ0 u, Gu
holds for all states σ0 .
Proof. A straight consequence of Definition 7.1.1 and Definition 5.1.1.
    A particular result is that any triple ρ |ù tR, P u p tQ, Gu is equivalent to
                                  def
ρ |ù2 tR, P u p tQ, Gu where A “ tpσ, σ 1 q | σ 1 P Au is a mapping that embeds
each state predicate A into state relations. On the other hand, by far not each
triple ρ |ù2 tR, P u p tQ, Gu has an equivalent counterpart with state predicates
as pre- and postconditions: consider for instance
      ρ |ù2 tid, idu p tshared Ď shared1 , Ju
which encompasses those programs pρ, pq that do ultimately retain all elements
in the set assigned to shared in the given input state if this leads to termination.

                                         62
7.1. GENERALISING THE EXTENDED HOARE TRIPLES


    A notable feature of such generalised triples is that each of the program
logic rules from Section 5 can seamlessly be lifted by a systematic replacement
of relational images with relational compositions. This will be illustrated below
by means of the program correspondence rule and the rule for basic.
Proposition 7.1.2. Assume ρ, ρ1 |ù p Ěr q, ρ |ù2 tR, P u p tQ, Gu and
  (1) r ˛ R1 Ď R ˛ r,
  (2) P 1 Ď P ˛ r,
  (3) Q ˛ r Ď Q1 ,
  (4) r˝ ˛ G ˛ r Ď G1 .
Then ρ1 |ù2 tR1 , P 1 u q tQ1 , G1 u.
Proof. By Proposition 7.1.1 we show ρ1 |ù tR1 , P 1 ¨ tσ0 uu q tQ1 ¨ tσ0 u, G1 u with
a fixed σ0 . Instantiating Proposition 5.2.1 by P 1 ¨ tσ0 u for P 1 and Q1 ¨ tσ0 u for
Q1 as well as P ¨ tσ0 u for P and Q ¨ tσ0 u for Q, it remains thus to establish the
following three proof obligations:
  (i) ρ |ù tR, P ¨ tσ0 uu p tQ ¨ tσ0 u, Gu is a plain consequence of the assumption
      ρ |ù2 tR, P u p tQ, Gu by Proposition 7.1.1;
 (ii) P 1 ¨ tσ0 u Ď r ¨ pP ¨ tσ0 uq which is equivalent to P 1 ¨ tσ0 u Ď pP ˛ rq ¨ tσ0 u
      and hence follows from (2);
 (iii) r ¨ pQ ¨ tσ0 uq Ď Q1 ¨ tσ0 u which is equivalent to pQ ˛ rq ¨ tσ0 u Ď Q1 ¨ tσ0 u
       and hence follows from (3).


Proposition 7.1.3. Assume
  (1) P ˛ R Ď P ,
  (2) P Ď tpσ, σ 1 q | pσ, f σ 1 q P Q ^ pσ 1 , f σ 1 q P Gu.
Then |ù2 tR, P u basic f tQ, Gu.
Proof. We have to show |ù tR, P ¨ tσ0 uu basic f tQ ¨ tσ0 u, Gu for any σ0 and
apply the instance of Proposition 5.3.2 with P ¨ tσ0 u for P and Q ¨ tσ0 u for Q.
This is sound because R ¨ pP ¨ tσ0 uq Ď P ¨ tσ0 u is a consequence of (1) whereas
P ¨ tσ0 u Ď tσ | f σ P Q ¨ tσ0 u ^ pσ, f σq P Gu – of (2).

   Next section proceeds to the onward topic concerning more structured rea-
soning upon rely/guarantee properties by means of abstraction and reuse.

                                              63
State Relations as Pre- and Postconditions


7.2     Abstracting code fragments
The key advantage of the generalised program logic presented in the preceding
section is that for the variety of environments specified by a rely R, the in-
put/output behaviour of a code fragment p can often be so accurately captured
by means of the pre- and postcondition in a triple |ù2 tR, P u p tQ, Gu that it is
worth to be proved once and then reused when showing rely/guarantee proper-
ties of programs where p occurs as a subroutine interleaved with an environment
in the specified variety.
    The principle is illustrated by a small example addressing most of the es-
sential points that arise with abstraction of code fragments in the context of
interleaving. The triple
|ù2 tx “ x1 , x “ x1 u inc tx1 “ x ` 1, x ď x1 u                              (7.1)
                                                                   def
displays a relation between the inputs and the outputs of inc “ x :“ x ` 1 if
the environment condition x “ x1 is met, i.e. the variable x can be viewed as
local to inc when it gets deployed by a thread. With any environment that does
not satisfy x “ x1 , the pre- and postcondition have to be adjusted accordingly.
For example, by weakening the rely to x ď x1 , the precondition would need to
be altered to x ď x1 to remain stable so that the most accurate postcondition
regarding x would consequently be x ă x1 . Further, the guarantee in (7.1) could
also be amplified to x ` 1 “ x1 , which would be the strongest possible only if
the underlying states have no other variables than x. That is, if there is another
variable, say v, then v “ v1 shall be guaranteed by inc as well. To some extent
this applies to the postcondition too: in the purely sequential setting one would
without much ado augment the pre- and postcondition in (7.1) by v “ v1 , but
in presence of interleaving this would in turn require the additional rely v “ v1
to ensure stability of thus updated precondition.
    Staying within the variety specified by the rely x “ x1 , the triple (7.1) can
for example be reused twice to show
|ù2 tx “ x1 , x “ x1 u inc; inc tx1 “ x ` 2, x ď x1 u
making the reasoning more structured and efficient compared to the plain pro-
cessing of x :“ x ` 1; x :“ x ` 1, i.e. with the definition of inc unfolded. For the
second invocation of inc one is however prompted to show
|ù2 tx “ x1 , x1 “ x ` 1u inc tx1 “ x ` 2, x ď x1 u                           (7.2)
which is not an immediate instance of (7.1) and demands the following general
consideration:

                                         64
7.2. ABSTRACTING CODE FRAGMENTS


Proposition 7.2.1. Assume P 1 is reflexive, R Ď R1 , G1 Ď G and
 (1) |ù2 tR1 , P 1 u p tQ1 , G1 u,
 (2) P ˛ Q1 Ď Q.
Then |ù2 tR, P u p tQ, Gu.
Proof. By Definition 7.1.1 we have to show |ù tR, tσuu p tQ ¨ tσ0 u, Gu for some
states σ0 , σ with pσ0 , σq P P . First note that |ù tR1 , tσuu p tQ1 ¨ tσu, G1 u follows
from (1) by Definition 7.1.1 since pσ, σq P P 1 . Thus, only Q1 ¨ tσu Ď Q ¨ tσ0 u
remains to be established. Assuming pσ, σ 1 q P Q1 with some σ 1 to this end we
can first infer pσ0 , σ 1 q P P ˛ Q1 and then pσ0 , σ 1 q P Q using (2).
   Since x “ x1 is reflexive and px1 “ x ` 1q ˛ px1 “ x ` 1q Ď x1 “ x ` 2 holds,
the triple (7.2) is derivable by the above proposition and (7.1).




                                           65
Chapter 8

Case Study: Strengthening
the Specification

The mutex rule in Proposition 6.3.1 can directly be lifted to the generalised pro-
gram logic with state relations as pre- and postconditions proceeding similarly
to Propositions 7.1.2 and 7.1.3.



8.1     Lifting the mutex rule
The key difference to Chapter 6 is that the parameters P0 , Q0 , P1 , Q1 can now
depend on two values of shared so that e.g. Q0 can capture a relation between
initial values of shared and its values when cs 0 terminates. Our goal is thus
the generalised conclusion of Proposition 6.3.1:

  |ù2 tid, P0 shared shared1 ^ P1 shared shared1 u
       thread 0 cs 0 k thread 1 cs 1                                         (8.1)
      tQ0 shared shared1 ^ Q1 shared shared1 , Ju

Note once more that with e.g. Q0 shared shared1 in the above postcondition
we respectively relate the value of shared in an initial state σ0 and its value
in a state where mutex may terminate starting from σ0 . This is in contrast to
relies and guarantees where shared and shared1 always refer to the respective
values in any two consecutive states on a computation.

                                       67
Case Study: Strengthening the Specification


   Hence (8.1) follows by Proposition 7.1.1 if we show

 |ù tid, pP0 σsharedq shared ^ pP1 σsharedq sharedu
      thread 0 cs 0 k thread 1 cs 1                                         (8.2)
    tpQ0 σsharedq shared ^ pQ1 σsharedq shared, Ju

for any state σ. In this context, Pi σshared and Qi σshared become fixed state
predicates for i P t0, 1u pointing to how Proposition 6.3.1 shall be instantiated
in order to match (8.2): P0 by P0 σshared, Q0 by Q0 σshared and so on. To
match the instantiated first premise of Proposition 6.3.1, namely

 |ù tshared “ shared1 ^ local0 “ local10 , pP0 σsharedq sharedu
      cs 0
    tpQ0 σsharedq shared, G01 u

with G01 denoting the respective instance of G0

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local1 “ local11 ^
 turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
 ppP1 σsharedq shared ÝÑ pP1 σsharedq shared1 q ^
 ppQ1 σsharedq shared ÝÑ pQ1 σsharedq shared1 q,

we consequently make the following assumption

 |ù2 tshared “ shared1 ^ local0 “ local10 , P0 shared shared1 u
       cs 0                                                                 (8.3)
     tQ0 shared shared1 , G011 u

where G011 shall denote

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local1 “ local11 ^
 turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
 p@v. pP1 vq shared ÝÑ pP1 vq shared1 q ^
 p@v. pQ1 vq shared ÝÑ pQ1 vq shared1 q.

In response to the instantiated second premise of Proposition 6.3.1 we moreover
make the symmetric assumption

 |ù2 tshared “ shared1 ^ local1 “ local11 , P1 shared shared1 u
       cs 1                                                                 (8.4)
     tQ1 shared shared1 , G111 u

                                        68
8.2. AN APPLICATION OF THE LIFTED mutex RULE


where G111 accordingly denotes

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local0 “ local10 ^
 turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
 p@v. pP0 vq shared ÝÑ pP0 vq shared1 q ^
 p@v. pQ0 vq shared ÝÑ pQ0 vq shared1 q.

The overall result is thus the following lifted rule for mutex:
Proposition 8.1.1. Assume (8.3) and (8.4) and
 |ù cs 0 Ěr0 cs 0 ,
 |ù cs 1 Ěr1 cs 1 ,
 |ù cs 0 Ěreqv cs 0 ,
 |ù cs 1 Ěreqv cs 1 .
Then we have (8.1).


8.2       An application of the lifted mutex rule
By contrast to Section 6.4, the rule in Proposition 8.1.1 allows us to derive a
significantly finer input/output property of mutex update 0 update 1 . To this end
we instantiate the parameters P0 , P1 , Q0 , Q1 so as to make the triples (8.3) and
(8.4) specify the behaviour of update 0 and update 1 taking into account also the
input value shared in presence of interleaving.
    More precisely, due to the inherent uncertainty whether the access to shared
will be granted to update 0 or to update 1 in first place, the pre- and postcondition
of the below triple account for both cases:

|ù2 tshared “ shared1 ^ local0 “ local10 ,
     shared “ shared1 _ shared Y t1u “ shared1 u
                                                                               (8.5)
      update 0
    tshared Y t0u “ shared1 _ shared Y t0, 1u “ shared1 , G01 u

where G01 becomes now accordingly

 flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 ^ local1 “ local11 ^
 turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
 pshared “ shared1 _ shared Y t0u “ shared1 q.

                                         69
Case Study: Strengthening the Specification


Note that G01 could have been used in this form in Section 6.4 as well, but the
weaker guarantee 1 P shared ÝÑ 1 P shared1 was more adequate there than
shared “ shared1 _ shared Y t0u “ shared1 .
    Since the assumption (8.4) is similarly addressed by means of the respective
triple for update 1 , using Proposition 8.1.1 we can conclude

|ù2 tid, pshared “ shared1 _ shared Y t1u “ shared1 q ^
         pshared “ shared1 _ shared Y t0u “ shared1 qu
       thread 0 update 0 k thread 1 update 1
    tpshared Y t0u “ shared1 _ shared Y t0, 1u “ shared1 q ^
     pshared Y t1u “ shared1 _ shared Y t0, 1u “ shared1 q, Ju

which can further be simplified to

|ù2 tid, idu mutex update 0 update 1 tshared Y t0, 1u “ shared1 , Ju          (8.6)

because from shared Y t0u “ shared1 ^ shared Y t1u “ shared1 we can infer
t0, 1u Ď shared and hence also shared Y t0, 1u “ shared1 .
    Unfolding the definitions, the triple (8.6) yields the following statement:
σshared Y t0, 1u “ σ 1 shared holds for all sq P vmutex update 0 update 1w X Env id
where σ “ Spsq 0 q and σ 1 is the state of the first skip-configuration on sq, if
such exists. That the existence is provided even though not for any but for
any fair computation sq P vmutex update 0 update 1 wω X Env id will ultimately be
shown in the last part of the case study in Chapter 10. The techniques applied
in Chapter 10 are derived from the general approach elaborated next.




                                        70
Chapter 9

Verifying Liveness
Properties of Programs

Liveness covers a variety of questions that is sometimes rather casually sum-
marised by ‘will something good eventually happen?’, answering which may
demand very involved reasoning in many instances. In the current context we
will confine ‘something good’ to certain computations of a program starting in
a state satisfying an input condition reach a state satisfying some output condi-
tion. Making this point clear, let p1 be the program

     while a ą 0 do skip subsequently b :“ True od

whereas p2 shall comprise the assignment a :“ 0 only (note that Park [15] uses
a similar introductory example for a similar purpose but in a different context).
Whether certain (which per se does not rule out all ) computations of p1 k p2
that start with a state satisfying a “ 1 ^ b eventually reach a state satisfying
b is an eligible question regarding liveness of p1 k p2 . One such computation
evidently exists: p2 assigns 0 to a, then p1 exits the while a ą 0 do . . . cycle
and can assign True to b. On the other hand, a computation where we have
only environment steps which do not modify b cannot reach a state satisfying b
whatsoever. Hence, certain computations can be consistent but surely cannot
mean any potential computation, be it finite or infinite. Intuitively, certain
shall therefore encircle the largest possible subset of potential computations of
p1 k p2 for which the answer to the question is a provable ‘yes’. More precisely,
we may consider the following candidates:

                                       71
Verifying Liveness Properties of Programs


 (1) vp1 k p2 w – i.e. all finite potential computations of p1 k p2 ,

 (2) vp1 k p2 wω X Env K – i.e. all infinite actual computations of p1 k p2 ,

 (3) vp1 k p2 wω X Env id – i.e. all infinite potential computations of p1 k p2 in
     presence of a ‘stuttering’ environment.

With (1) the answer is ‘no’: apart from many computations that just do not
reach a state satisfying b, vp1 k p2 w also contains all prefixes of computations
that do reach b once. Most of these prefixes, however, do not need to reach
b themselves: the singleton computation pp1 k p2 , σ0 q is the simplest example.
With (2) the answer is also ‘no’: by considering all infinite computations with-
out any environment steps we actually exclude the most relevant ones that reach
a state satisfying b and terminate. By contrast, the option (3) not only covers
all relevant computations of p1 k p2 that reach b and terminate yielding subse-
quently to the ‘stuttering’ environment, but also those with infinite runs of the
environment perpetually holding back all possible program steps, as well as of
the while a ą 0 do . . . cycles arbitrarily interleaved with the environment, all
having b as an invariant. Casting such runs out would result in an adequately
large subset of computations of p1 k p2 which nonetheless enables argumentation
that the answer to the above question is ‘yes’.
    These considerations ineluctably lead to the conclusion that some form of
fairness ought to be generally asserted on computations in vpwω      ρ in order to
achieve rational reasoning upon liveness properties of p, which is by no means a
new insight and various forms have been studied in the contexts of process alge-
bras and temporal logics (cf. [22, 23, 24] to name only a few). Taking advantage
of the syntactic structure built into the program part of each configuration, next
section develops a concise notion of fair potential computations.


9.1     Program positions
The starting point is a view of the inductive rules for program steps in Figure 2.1
from the rewriting system perspective. For example the rule

      ρ $ pbasic f, σq ÑP pskip, f σq

can in principle be regarded as the identity used to reduce px :“ 1 k x :“ 2, σq
either to pskip k x :“ 2, σrx:“1s q or to px :“ 1 k skip, σrx:“2s q by means of the
rule ‘Parallel’. Attaching two different positions to the subterms x :“ 1 and

                                         72
9.1. PROGRAM POSITIONS


x :“ 2 in order to indicate where a reduction can take place would make the
rule ‘Parallel’ essentially superfluous and resemble rewriting of terms in general
as described e.g. by Baader and Nipkow [25]. Furthermore, the configuration
px :“ 1; x :“ 2, σq can similarly be reduced to pskip; x :“ 2, σrx:“1s q by the rule
‘Sequential’, but by contrast not to px :“ 1; skip, σrx:“2s q as there is no rule
to this end. This deviation from general term rewriting, where each subterm
gets identified with a position, suggests the following insight: despite the same
tree structure, the terms x :“ 1 k x :“ 2 and x :“ 1; x :“ 2 exhibit different
sets of positions entitled for a substitution according to the inductive rules in
Figure 2.1.
    In line with the representation of term positions by words over the natural
numbers deployed in [25], the function Pos in this setting maps each term of
type Lα to a set of words over nat, referred to as program positions and defined
by the following recursive equations using pattern matching:
       Pos skip                       “      K
       Pospskip; qq                   “      t0u
       Pospp; qq                      “      t0w | w P Pos pu
       Pospkskip, . . . , skipq       “      t0u
                                             Ťm
       Pospkp1 , . . . , pm q         “        i“1 tiw | w P Pos pi u
       Pos p                          “      t0u
so that e.g. Pospx :“ 1 k x :“ 2q “ t10, 20u whereas Pospx :“ 1; x :“ 2q “ t00u.
    Immediate consequences of the definition are:
    - Pos p is empty iff p “ skip,
    - ǫ R Pos p,
    - if x P Pos p then x “ x1 0 (where x1 could also be the empty word ǫ),
    - Pos p contains more than one word only if the parallel operator, applied to
      at least two arguments different from skip, occurs in p. This particularly
      means that Pos p contains exactly one word for any locally sequential
      p ‰ skip.
   Further, the function satisfying the following recursive equations using pat-
tern matching
       p|0                      “   inr p
       pp ; qq|0x               “   p|x
       pkp1 , . . . , pm q|ix   “   pi |x
       p|x                      “   inl ()

                                                 73
Verifying Liveness Properties of Programs


returns a value of the co-product type 1 ` Lα where () denotes the value of the
unit type 1. Note that there is some t of type Lα such that p|x “ inr t holds
whenever x P Pos p. Hence by p|x we will for the sake of brevity refer to the
t and say that p|x retrieves the subterm determined by the program position
x P Pos p.
    Although p|x “ inr t is satisfiable also with x R Pos p (consider e.g. skip|0 ),
this modelling enables the following, in this context particularly useful property.
Proposition 9.1.1. If x P Pos p and p|x “ q|x then x P Pos q.
Proof. By induction on the length of x. Let x P Pos p and suppose p|x “ q|x . If
x has the length 0 then we are done since ǫ R Pos p. If x has the length 1 then
x “ 0 and hence p|0 “ q|0 entails p “ q.
    Next, suppose x has the form ix1 with x1 ‰ ǫ. In case i “ 0 we infer that there
are some p1 , p2 and q1 , q2 such that p “ p1 ; p2 and q “ q1 ; q2 . Thus, x P Pos p
entails x1 P Pos p1 whereas p|x “ q|x entails p1 |x1 “ q1 |x1 . From this x P Pos q
follows since x1 P Pos q1 is provided by the induction hypothesis.
    Lastly, in case i ą 0 we infer that there are some p1 , . . . , pm and q1 , . . . , qm1
where i ď m and i ď m1 such that p “ kp1 , . . . , pm and q “ kq1 , . . . , qm1 . Thus,
x P Pos p entails x1 P Pos pi whereas p|x “ q|x entails pi |x1 “ qi |x1 . From this
x P Pos q follows since x1 P Pos qi is provided by the induction hypothesis.
   Replacing p|x by p1 at the position x P Pos p is (once more in line with [25])
denoted by prp1 sx and defined by the equations
       prp1 s0                      “   p1
       pp ; qqrp1 s0x               “   pprp1 sx q; q
       pkp1 , . . . , pm qrp1 six   “   kp1 , . . . pi rp1 sx . . . , pm
   Regarding the three syntactic operations together, we have the property
                   "
                     q    if x “ x1
     pprqsx q|x1 “                                                      (9.1)
                     p|x1 otherwise
for any p, q and x, x1 P Pos p.
    A valuable consequence of Proposition 9.1.1 and (9.1) is:
Corollary 9.1.2. If there are two different positions x P Pos p and y P Pos p
then y P Pospprqsx q.
   The main objective behind these operations is to describe computation steps
by means of substitutions at program positions as the following proposition
shows.

                                                  74
9.2. FAIR COMPUTATIONS


Proposition 9.1.3. ρ $ pp, σq ÑP pq, σ 1 q iff there exist some x P Pos p and p1
such that ρ $ pp|x , σq ÑP pp1 , σ 1 q and q “ prp1 sx .

Proof. By structural induction on p for the if-direction, and on the relation ÑP
for the opposite.

    The above statement however does not provide the position x P Pos p that
has been reduced (or ‘fired’) by ρ $ pp, σq ÑP pq, σ 1 q so that q “ prp1 sx . On the
other hand, the existence of different x, x1 P Pos p with ρ $ pp|x , σq ÑP pu, σ 1 q,
ρ $ pp|x1 , σq ÑP pv, σ 1 q and prusx “ prvsx1 entails p|x “ u and p|x1 “ v, i.e. the
existence of program steps which behave like environment steps by retaining the
program part of a configuration.
    From ρ $ pp, σq ÑP pp, σ 1 q one can basically infer that p is not jump-free and
there is a label i with ρ i having the form cjump C to i otherwise w end. The
following example illustrates that retrieving functions with such a property can
be used to produce very peculiar effects: let ρ be a retrieving function satisfying
ρ 1 “ jump 1 and ρ 2 “ jump 2, and consider the program pρ, jump 1 k jump 2q.
Then any sq P vjump 1 k jump 2wω    ρ X Env K, i.e. any infinite actual computation
of pρ, jump 1 k jump 2), has the form

      pjump 1 k jump 2, Spsq 0 qq ÑP pjump 1 k jump 2, Spsq 0 qq ÑP . . .

in particular concealing which of the two jumps has been deployed by sq at all.
    Ruling such singularities generally out, only such retrieving functions ρ where
we have ρ i ‰ cjump C to i otherwise w end for all i, C, w will be considered
from now on. Then to each transition ρ $ pp, σq ÑP pq, σ 1 q there is the unique
fired position x P Pos p with a step ρ $ pp|x , σq ÑP pp1 , σ 1 q such that q “ prp1 sx .


9.2      Fair computations
It is essential to underline that in presence of await-statements, Pos p may also
contain program positions that are not always available for a substitution: if
x P Pos p with p|x “ await C do q od then

    - x is never available when C “ K,

    - availability of x depends only on termination of q when C “ J,

    - availability of x additionally depends on the evaluation of C otherwise.

                                           75
Verifying Liveness Properties of Programs


In order to keep the notion of fairness for the beginning as concise as possible,
we will focus on such program positions whose availability is state independent:
Definition 9.2.1. Let p be a term of type Lα . A position x P Pos p is called
always available if p|x “ await C do q od implies
 (a) C “ J and
                                                                          ˚
 (b) for any ρ and a state σ there exists σ 1 such that ρ $ pq, σq ÑP pskip, σ 1 q.
    Consequently, if x P Pos p is always available then for any σ there exist some
p1 and σ 1 such that ρ $ pp|x , σq ÑP pp1 , σ 1 q and ρ $ pp, σq ÑP pprp1 sx , σ 1 q hold.
    A fair computation in principle does not keep an always available position
from making its move once:
Definition 9.2.2. An infinite potential computation sq P vpwω ρ is called fair if
for any i P N and any always available x P PospPpsqi qq there exists j ě i with
a program step ρ $ sq j ÑP sq j`1 having x as the fired position and satisfying
Ppsq j q|x “ Ppsqi q|x . This will be denoted by sq P vpwfair
                                                         ρ .

    Thus, the definition leaves for instance open whether a program step will
ever be performed by some sq P vawait C do skip odwfair with C Ă J because
the only position 0 is not always available. Indeed, a plain generalisation of Def-
inition 9.2.2 from always available to any position would make it inadequately
restrictive as we would be able to infer that any sq P vawait C do skip odwfair
reaches a state satisfying C at least once. A way to generalise Definition 9.2.2
to additionally enable reasoning upon liveness properties of programs deploying
await-statements beyond atomic sections will be discussed in Section 11.1.
    For a program pρ, pq that is sequential, the property sq P vpwfairρ simplifies
to: sq P vpwωρ and for any i P N and any always available x P PospPpsqi qq there
exists j ě i with a program step ρ $ sq j ÑP sq j`1 . In other words, fairness for
sequential programs means that there are no infinite runs of environment steps
as long as an always available position is present.
    It shall lastly be outlined how this notion of fair computations allows us
to substantiate the answer ‘yes’ in the introductory example where we have
Pospp1 k p2 q “ t10, 20u and both positions are moreover always available. Hence,
any computation sq P vp1 k p2 wfair X Env id eventually reduces p2 to skip at the
position 20 assigning thereby 0 to a. Note that the first parallel component
must still be in the while a ą 0 do . . . cycle as a had constantly the value 1
prior to that. Now however only one available position remains and the states of
all subsequent configurations will moreover satisfy a “ 0. The first component

                                           76
9.3. A REFUTATIONAL APPROACH TO PROVING LIVENESS PROPERTIES


will therefore eventually exit the while a ą 0 do . . . cycle making in turn the
subterm b :“ True available at the position 10. Finally, the environment, prior
to keep on ‘stuttering’ ad infinitum, will first let sq reduce this position to skip
assigning thereby True to b, and then reduce skip k skip to skip.


9.3     A refutational approach to proving liveness
        properties
The above paragraph can at best be considered as a sketch of a sketch of an
argumentation that sq P vp1 k p2 wfair X In pa “ 1 ^ bq X Env id reaches a state
satisfying b. Nonetheless it pointed to how one can follow the program structure
in order to draw relevant conclusions, i.e. the very basic approach is to some
extent not unlike the syntax-driven rely/guarantee reasoning.
    Generally, to show that any fair computation of a program p that starts in
a state satisfying some given condition P and has only ‘stuttering’ environment
steps eventually reaches a state satisfying some given Q, one can attempt to
refute the opposite, i.e. that there exists sq P vpwfair X In P X Env id having Q
as an invariant. This motivates the following three definitions.
Definition 9.3.1. Let sq be an infinite sequence of configurations, p – a jump-
free program and P, Q – state predicates. Then the condition sq , P Ż p Ż Q
holds iff sq P vpwfair X In P and Spsq i q R Q holds for all i P N.
Definition 9.3.2. The condition sq ,N P Ż p Ż Q holds iff sq , P Ż p Ż Q and
Ppsq i q ‰ skip holds for all i P N.
Definition 9.3.3. Let additionally n P N. Then sq ,T P Ż p Ż Q Ż n holds iff
sq P vpwω X In P and Spsq i q R Q holds for all i P N, and moreover n is the least
number such that Ppsq n q “ skip.
     Thus, sq , P Ż p Ż Q entails sq ,N P Ż p Ż Q _ pDn. sq ,T P Ż p Ż Q Ż nq and
the disjunction is moreover exclusive: the condition sq ,N P Ż p Ż Q covers the
cases with a non-terminating sq and sq ,T P Ż p Ż Q Ż n – the cases with sq
reaching the first skip-configuration by n steps. In particular this means that
it is sound to refute the two cases in order to conclude that there exists some i
with Spsq i q P Q if sq P vpwfair X In P .
     Conversely, sq , P Ż p Ż Q follows straight from sq ,N P Ż p Ż Q, but the
same conclusion is not immediate with sq ,T P Ż p Ż Q Ż n as Definition 9.3.3
does not explicitly require from sq to be fair. This point is however settled by
the following general property.

                                        77
Verifying Liveness Properties of Programs


Proposition 9.3.1. If sq P vpwω
                              ρ and Ppsq n q “ skip then sq P vpwρ .
                                                                 fair



Proof. Unfolding Definition 9.2.2, let i P N and x P PospPpsqi qq be an always
available position. Firstly, note that i ă n must hold since otherwise we would
have x P Pos skip which is impossible. Next, we proceed by showing that the
additional assumption
 (a) each program step ρ $ sq j ÑP sq j`1 with j ě i and Ppsqj q|x “ Ppsqi q|x
     has the fired position x1 ‰ x
leads to a contradiction. Indeed, with (a) it is possible to derive
 (b) j ě i implies Ppsqj q|x “ Ppsqi q|x
for any j, so that taking n for j in (b) we get skip|x “ Ppsqi q|x which once
more yields x P Pos skip by Proposition 9.1.1, meaning that the negation of
(a) must be valid, i.e. sq P vpwfair
                                 ρ . Hence, it remains to show (b) which will be
accomplished by induction on j.
    The base case is clear since j “ 0 implies i “ 0. As the induction step we have
to show Ppsqj`1 q|x “ Ppsqi q|x additionally assuming (b) and j ` 1 ě i. Since
with j ` 1 “ i the goal follows straight, with j ě i we infer Ppsqj q|x “ Ppsqi q|x
from (b). Then only Ppsqj`1 q|x “ Ppsqj q|x remains to be established, noting
that x P PospPpsqj qq moreover holds by Proposition 9.1.1.
    Firstly, if we have a program step ρ $ sq j ÑP sq j`1 then (a) entails x1 ‰ x
where x1 is its fired position. Thus, Ppsqj`1 q|x “ pPpsqj qrp1 sx1 q|x “ Ppsqj q|x
follows using (9.1). Secondly, with sq j ÑE sq j`1 we have Ppsq j`1 q “ Ppsq j q.
   To sum up the result:
Corollary 9.3.2. sq , P Ż p Ż Q iff sq ,N P Ż p Ż Q _ pDn. sq ,T P Ż p Ż Q Ż nq
    Note that the two disjuncts are also useful on their own: one can for instance
attempt to refute statements of the form Dsq P Env id. sq ,N P Ż p Ż K which is
the same as to establish that any sq P vpwfair X Env id X In P reaches a skip-
configuration once, i.e. p terminates on any input in P .
    From the definitions follows that different conclusions can in general be
drawn depending on whether we have sq ,N P Ż p Ż Q or sq ,T P Ż p Ż Q Ż n.
The syntax-driven rules presented in the remainder of this section handle there-
fore the two cases for each language constructor (with particular restrictions on
await-statements for the non-terminating case) in place of p.
    Starting with the simplest, an assumption sq ,N P Ż skip Ż Q immediately
leads to a contradiction, whereas sq ,T P Ż skip Ż Q Ż n entails n “ 0.

                                        78
9.3. A REFUTATIONAL APPROACH TO PROVING LIVENESS PROPERTIES


    Similarly to skip, sq ,N P Ż basic f Ż Q leads to a contradiction too but,
in contrast to skip, fairness of sq is decisive for this conclusion as it rules out
infinite runs of environment steps. Further, with sq ,T P Ż basic f Ż Q Ż n in
addition to Spsq 0 q P P we can infer

 (a) n ą 0,

 (b) sq n´1 “ pbasic f, σq and sq n “ pskip, f σq,

 (c) f σ R Q

for some state σ, acquiring thus the information that the atomic action associ-
ated to f has been triggered at the point n ´ 1 on sq. As will become evident
later on, several such points can moreover indicate a relative order of events:
as opposed to the parallel composition basic f k basic g where we can merely
acquire that f and g have been triggered at some respective points n and m on
sq, with the sequential basic f ; basic g we would additionally have n ă m.
    Next two propositions handle the conditional and the await-statements.

Proposition 9.3.3. The following implications hold:

 (1) if sq ,N P Ż xpy Ż Q then there exists a state σ such that for all σ 1 the
     configuration pskip, σ 1 q is not reachable from pp, σq by any sequence of
                                  ˚
     program steps, i.e. pp, σq Ñ­ P pskip, σ 1 q;

 (2) if sq ,T P Ż await C do p od Ż Q Ż n then n ą 0, Spsq n´1 q P C and
                            ˚
            pp, Spsq n´1 qq ÑP pskip, Spsq n qq.

Proof. To show (1) we appeal to fairness as follows. Suppose for all states σ
                                       ˚
there exists some σ 1 such that pp, σq ÑP pskip, σ 1 q. Then the position 0 (i.e. xpy)
in Ppsq 0 q is always available, and since sq is fair there must be a program step
sq j ÑP sq j`1 with Ppsq j q “ xpy and Ppsq j`1 q “ skip which is a contradiction
to sq ,N P Ż xpy Ż Q.
     To show (2), suppose sq ,T P Ż await C do p od Ż Q Ż n and note that by
contrast to (1) not only atomic sections but all await-statements are thereby
covered. Since sq n is the first skip-configuration on sq we can infer n ą 0 and
pawait C do p od, Spsq n´1 qq ÑP pskip, Spsq n qq from which Spsq n´1 q P C and
                 ˚
pp, Spsq n´1 qq ÑP pskip, Spsq n qq follow.

Proposition 9.3.4. The following implications hold:

                                         79
Verifying Liveness Properties of Programs


 (1) if sq ,N P Ż if C then p else q fi Ż Q then there exists n ą 0 such that
     either n |sq ,N C Ż p Ż Q or n |sq ,N C Ż q Ż Q;

 (2) if sq ,T P Ż if C then p else q fi Ż Q Ż n then there exists some m P N
     with 0 ă m and m ď n such that either m |sq ,T C Ż p Ż Q Ż n ´ m or
     m
       |sq ,T C Ż q Ż Q Ż n ´ m .

Proof. In (1) we particularly have sq P vif C then p else q fiwfair which entails
that a program step reducing the available position 0 in Ppsq 0 q will eventually
be performed. That is, there must be some n ą 0 with sq n´1 ÑP sq n such that
Ppsq n´1 q “ if C then p else q fi and Spsq n q “ Spsqn´1 q. If Spsqn´1 q P C
then n |sq P vpwω starts in a state satisfying C. Furthermore, as a suffix of sq,
the computation n |sq P vpwω neither reaches a skip-configuration nor a state
satisfying Q and is moreover fair. Altogether n |sq ,N C Ż p Ż Q follows. With
Spsqn´1 q R C we similarly conclude n |sq ,N C Ż q Ż Q.
     In (2), sq ,T P Ż if C then p else q fi Ż Q Ż n entails some i ă n with
sq i ÑP sq i`1 and Ppsq i q “ if C then p else q fi because otherwise we would
have Ppsq n q ‰ skip. Hence, the suffix i`1 |sq starts either with pp, Spsq i`1 qq
where Spsq i`1 q P C or with pq, Spsq i`1 qq where Spsq i`1 q R C, and in both cases
reaches the first skip-configuration in n ´ i ´ 1 steps.

    Let sq „ sq 1 from now on denote that these infinite sequences of configu-
rations run through the same states, i.e. Spsq i q “ Spsq 1i q for all i P N. This
equivalence allows us to relate computations by their state traces and is of im-
portance to all of the remaining rules starting with the sequential composition.

Proposition 9.3.5. The following implications hold:

 (1) if sq ,N P Ż p;q Ż Q then there exists a computation sq 1 „ sq and either
     sq 1 ,N P Ż p Ż Q or there exist m, n P N with m ă n such that we have
     sq 1 ,T P Ż p Ż Q Ż m and n |sq ,N J Ż q Ż Q;

 (2) if sq ,T P Ż p;q Ż Q Ż n then there exist sq 1 „ sq and some m, l P N with
     m ă l ď n such that sq 1 ,T P Ż p Ż Q Ż m and l |sq ,T J Ż q Ż Q Ż n ´ l.

Proof. In (1) we assume sq P vp;qwfair that does not reach a skip-configuration.
First, suppose Ppsq i q ‰ skip; q holds for all i P N. In this case we can infer that
                                                                      def
for any i P N there is some ui with Ppsq i q “ ui ; q. Then let sq 1i “ pui , Spsq i qq.
Since sq 1 P vpwω and sq 1 „ sq are provided by this construction, it only remains
to be shown that sq 1 is fair. Let i P N and let x P Pos ui be an always available
position to this end. Then 0x is an always available position of ui ; q and hence

                                          80
9.3. A REFUTATIONAL APPROACH TO PROVING LIVENESS PROPERTIES


there is some j ě i with puj ; q, σq ÑP puj`1 ; q, σ 1 q, σ “ Spsq j q, σ 1 “ Spsq j`1 q,
the fired position 0x and, moreover, puj ; qq|0x “ pui ; qq|0x i.e. also uj |x “ ui |x .
That 0x is fired yields a program step ppuj ; qq|0x , σq ÑP pp1 , σ 1 q with some p1
such that uj`1 ; q “ puj ; qqrp1 s0x “ puj rp1 sx q; q holds. Thus, uj`1 “ uj rp1 sx and
puj |x , σq ÑP pp1 , σ 1 q, i.e. x is the fired position of puj , σq ÑP puj`1 , σ 1 q.
     Second, suppose µ is the smallest index with Ppsq µ q “ skip; q. We define
   1 def                                         def
sq i “ pui , Spsq i qq for all i ď µ and sq 1i “ pskip, Spsq i qq with sq 1i´1 ÑE sq 1i for
all i ą µ. Thus, sq 1 „ sq and sq 1 ,T P Ż p Ż Q Ż µ hold by construction. Since
the position 0 of Ppsq µ q is always available and sq is fair, we further have some
n ą µ with the program step sq n´1 ÑP sq n such that Ppsq n´1 q “ skip; q and,
consequently, Ppsq n q “ q. As nothing else than Spsq n q R Q may in general be
asserted regarding the state Spsq n q, we conclude n |sq ,N J Ż q Ż Q.
     In (2) we have sq P vp; qwω and Ppsq n q “ skip. Hence, there must be the
least index µ ă n with Ppsq µ q “ skip; q. Then for any i ď µ there is some ui
                                                                      def
such that Ppsq i q “ ui ; q holds and we once more define sq 1i “ pui , Spsq i qq for all
                 def
i ď µ and sq 1i “ pskip, Spsq i qq with sq 1i´1 ÑE sq 1i for all i ą µ. Thus, sq 1 „ sq
and sq 1 ,T P Ż p Ż Q Ż µ hold by construction. Further, there is some l with
µ ă l ď n such that Ppsq l q “ q for otherwise we would have Ppsq n q “ skip; q.
We therefore conclude l |sq ,T J Ż q Ż Q Ż n ´ l.
    Next proposition handles the cases with the parallel composition but, for
the sake of simplicity, of two components only. A very similar argumentation
however leads to a proof of the general rule: if sq ,N P Ż kp1 , . . . , pm Ż Q then
there is a function sending each k P t1, . . . , mu to a computation sq pk such that
  (i) sq pk „ sq for all k P t1, . . . , mu,
 (ii) sq pk , P Ż pk Ż Q for all k P t1, . . . , mu and
 (iii) there exists some k P t1, . . . , mu with sq pk ,N P Ż pk Ż Q.
For m “ 2, (ii) is the same as sq p1 , P Ż p1 Ż Q ^ sq p2 , P Ż p2 Ż Q which by
Corollary 9.3.2 is in turn equivalent to the formula

       psq p1 ,N P Ż p1 Ż Q _ pDn. sq p1 ,T P Ż p1 Ż Q Ż nqq ^
       psq p2 ,N P Ż p2 Ż Q _ pDn. sq p2 ,T P Ż p2 Ż Q Ż nqq.

Transforming it using the distributive law results in the three disjuncts encoun-
tered as (a),(b) and (c) in the part (1) of Proposition 9.3.6 whereas the fourth

      pDn. sq p1 ,T P Ż p1 Ż Q Ż nq ^ pDn. sq p2 ,T P Ż p2 Ż Q Ż nq

                                               81
Verifying Liveness Properties of Programs


contradicts (iii) and gets therefore discarded. The condition (iii) can thus dis-
appear as well because it is implied by each of the disjuncts (a), (b) and (c).
    Generally, if sq P v kp1 , . . . , pm wfair does not reach skip then there must be
non-terminating components pi1 , . . . , pik with 1 ď i1 ă . . . ă ik ď m and 0 ă k,
such that all pj withř j R`ti   1          ik u can accordingly be assumed as terminating.
                                 ˘, . . . ,m
This amounts to m        k“1 k
                               m
                                   “     2   ´ 1 branches (i.e. disjuncts) to be refuted in
order to refute sq ,N P Ż kp1 , . . . , pm Ż Q explaining also the three disjuncts for
m “ 2. As will become apparent in Chapter 10, with mutex we indeed will have
to follow all of the three branches. There is however a notable class of programs
with ‘independent’ parallel components whose non-termination can be refuted
independently of other components Žm            behaviour. More precisely, in such cases it
becomes possible to refute i“1 sq pi „ sq ^ sq pi ,N P Ż pi Ż Q, i.e. m branches.
    The part (2) of Proposition 9.3.6 is extended to m ą 2 components as follows:
if sq ,T P Ż kp1 , . . . , pm Ż Q Ż n then for all i P t1, . . . , mu there exist sq pi „ sq
and ni ă n such that sq pi ,T P Ż pi Ż Q Ż ni .
Proposition 9.3.6. The following implications hold:
 (1) if sq ,N P Ż p k q Ż Q then there exist sq p „ sq and sq q „ sq such that either
       (a) sq p ,N P Ż p Ż Q and sq q ,N P Ż q Ż Q, or
       (b) sq p ,N P Ż p Ż Q and there is some n with sq q ,T P Ż q Ż Q Ż n, or
       (c) sq q ,N P Ż q Ż Q and there is some n with sq p ,T P Ż p Ż Q Ż n;
 (2) if sq ,T P Ż p k q Ż Q Ż n then there exist sq p „ sq, sq q „ sq, n1 ă n and
      n2 ă n such that sq p ,T P Ż p Ż Q Ż n1 and sq q ,T P Ż q Ż Q Ż n2 .
Proof. In (1) we have a computation sq P vp k qwfair that does not reach a skip-
configuration. Now, if there would be some u, v, n1 , n2 with Ppsq n1 q “ skip k v
and Ppsq n2 q “ u k skip then we could infer Ppsq m q “ skip k skip where m is
the maximum of n1 and n2 , and hence by fairness of sq we could further obtain
some n ą m with Ppsq n q “ skip in contradiction to the assumption on sq. As
a result, for all i P N we have some ui and vi such that Ppsq i q “ ui k vi holds,
and define sq pi “ pui , Spsq i qq with sq pi ÑP sq pi`1 if there is sq i ÑP sq i`1 having
                 def


the fired position of the form 1x where x P Pos ui , and sq pi ÑE sq pi`1 otherwise.
Thus, sq p P vpwω and sq p „ sq are provided by this construction. To establish
that sq p is fair, let i P N and x P Pos ui be an always available position. Then
1x is an always available position of ui k vi , and since sq is fair there is some
j ě i with puj k vj , σq ÑP puj`1 k vj`1 , σ 1 q, σ “ Spsq j q, σ 1 “ Spsq j`1 q such that
    - uj |x “ puj k vj q|1x “ pui k vi q|1x “ ui |x

                                            82
9.3. A REFUTATIONAL APPROACH TO PROVING LIVENESS PROPERTIES


    - ppuj k vj q|1x , σq ÑP pp1 , σ 1 q

    - uj`1 k vj`1 “ puj k vj qrp1 s1x “ uj rp1 sx k vj

hold with some p1 . Then uj`1 “ uj rp1 sx and puj |x , σq ÑP pp1 , σ 1 q, i.e. x is the
fired position of puj , σq ÑP puj`1 , σ 1 q. A computation sq q „ sq with sq q P vqwfair
is constructed likewise – the fired position is here of the form 2x where x P Pos vj .
     Thus, if ui ‰ skip and vi ‰ skip hold for all i then sq p ,N P Ż p Ż Q and
   q
sq ,N P Ż q Ż Q follow by the above constructions. If we have ui ‰ skip for all
i but there is some j such that vj “ skip, we conclude sq p ,N P Ż p Ż Q and
sq q ,T P Ż q Ż Q Ż n where n is the first index with vn “ skip. The last case
with vi ‰ skip for all i and some j with uj “ skip is handled accordingly.
     In (2) we assume sq P vp k qwω and Ppsq n q “ skip where n is the least such
index. Then for all i ă n we have Ppsq i q “ ui k vi with some ui , vi . Furthermore,
Ppsq n´1 q “ skip k skip and sq n´1 ÑP sq n must hold as well. Consequently,
there exist the least index n1 ă n with un1 “ skip and the least index n2 ă n
with vn2 “ skip. We can thus define the computation sq p by sq pi “ pui , Spsq i qq
                                                                        def


for all i ď n1 and sq pi “ pskip, Spsq i qq with sq pi´1 ÑE sq pi for all i ą n1 , such
                          def

         p              p
that sq „ sq and sq ,T P Ż p Ż Q Ż n1 follow by this construction. Finally, a
computation sq q „ sq with sq q ,T P Ż q Ż Q Ż n2 is defined likewise.

    Shifting lastly the attention to while-statements, from an assumption of the
form sq ,T P Ż while C do p subsequently q od Ż Q Ż n we infer that there is
some i ď n with i |sq ,T C Ż q Ż Q Ż n ´ i. That is, sq proceeds to q in i ď n
steps reaching thereby a state in C from which it reaches a skip-configuration
in n ´ i steps. Note that such sq in general does not have to visit a state in C.
    With sq ,N P Ż while C do p subsequently q od Ż Q we can by contrast
infer that sq passes through the set of states satisfying C infinitely many times
whenever all fair computations of p and q, starting respectively from C and C,
reach a skip-configuration. This is captured by the following statement where
strictly ascending infinite sequence of naturals in this setting means a function
φ that maps each i of type nat to a value of the same type, for convenience
denoted by φi instead of φ i, such that φn ă φm holds for all n, m with n ă m.

Proposition 9.3.7. If sq ,N P Ż while C do p subsequently q od Ż Q then
either

 (1) there exists a strictly ascending infinite sequence of natural numbers φ
     such that for any n P N there exist some sq 1 „ φn |sq and m ă φn`1 ´ φn
     with sq 1 ,T C Ż p Ż Q Ż m, or

                                           83
Verifying Liveness Properties of Programs


 (2) there exist some n ą 0 and sq 1 „ n |sq such that sq 1 ,N C Ż p Ż Q, or
 (3) there exists some n ą 0 such that n |sq ,N C Ż q Ż Q.
Proof. Let pwhile abbreviate while C do p subsequently q od and assume we
have sq P vpwhile wfair which starts with a state in P , has Q as a state invariant
and does not reach a skip-configuration. Moreover, we will assume the respec-
tive negations of (2) and (3) (note that the invariant Q is omitted because it
is inherited from sq in both cases anyway):
 (a) for any sq 1 P vpwfair X In C and n ą 0 such that sq 1 „ n |sq holds there exists
     j P N with Ppsq 1j q “ skip,
 (b) for any n ą 0 such that n |sq P vqwfair X In p Cq holds there exists m P N
     with Ppsq n`m q “ skip
in order to derive (1) constructively. To this end we first show that for any i P N
with a step sq i ÑP sq i`1 where Ppsq i q “ pwhile and Spsq i q P C there exists some
j ą i with a step sq j ÑP sq j`1 where Ppsq j q “ pwhile and Spsq j q P C. Notice
that sq i`1 “ pp; skip; pwhile , Spsq i qq in particular follows for such i.
      Further, suppose there is no k ą i with Ppsq k q “ skip; skip; pwhile . Then
for all k ą i we have some uk ‰ skip with Ppsq k q “ uk ; skip; pwhile , and define
      def
sq 1l “ pui`l`1 , Spsq i`l`1 qq for all l inheriting the respective transitions from sq.
Thus, sq 1 P vpwfair X In C and sq 1 „ i`1 |sq hold by construction. Resorting to (a)
we obtain some j with Ppsq 1j q “ ui`j`1 “ skip , i.e. a contradiction.
      Then let k ą i be an index with Ppsq k q “ skip; skip; pwhile . Since sq is a
fair computation, we get some l1 ą k with Ppsq l1 q “ skip; pwhile and further
some l2 ą l1 with Ppsq l2 q “ pwhile . Once more, since the position 0 of Ppsq l2 q
is always available and sq is fair, there is also some j ě l2 with sq j ÑP sq j`1
and Ppsq j q “ pwhile . In case Spsq j q R C we would have j`1 |sq P vqwfair X Inp Cq
and using (b) obtain some m with Ppsq j`m`1 q “ skip in contradiction to the
assumption that sq does not reach a skip-configuration.
      As the intermediate result we obtain a function ψ on the natural numbers
such that ψ n ą n, sq ψ n ÑP sq ψ n ` 1 , Ppsq ψ n q “ pwhile and Spsq ψ n q P C hold
for any n with sq n ÑP sq n`1 , Ppsq n q “ pwhile and Spsq n q P C. Moreover, note
that an initial index n0 with sq n0 ÑP sq n0 `1 and Ppsq n0 q “ pwhile exists since sq
is fair, whereas Spsq n0 q P C must additionally hold for otherwise we would have
n0 `1
       |sq P vqwfair X In p Cq and hence a contradiction using (b) as in the above
                                                                          def
paragraph. A strictly ascending sequence φ is thus defined by φi “ 1 ` ψ i n0 .
      Let n be an arbitrary natural number for the remainder of the proof. By
the definition of φ we have Ppsq φn q “ p; skip; pwhile , Ppsq φn`1 ´1 q “ pwhile and

                                          84
9.4. PROGRAM CORRESPONDENCES AND FAIR COMPUTATIONS


Spsq φn q P C. This in particular means that there must be the least index µ
such that φn ď µ ă φn`1 and Ppsq µ q “ skip; skip; pwhile hold. Then for any i
with φn ď i ď µ there is some ui with Ppsq i q “ ui ; skip; pwhile . Thus, we can
             def                                                    def
define sq 1i “ puφn `i , Spsq φn `i qq for all i ď µ ´ φn and sq 1i “ pskip, Spsq φn `i qq
for all i ą µ ´ φn . The computation sq meets the conditions sq 1 „ φn|sq and
                                                 1


sq 1 ,T C Ż p Ż Q Ż µ ´ φn by construction.

    Summing up, an assumption of the form sq , P Ż p Ż Q, where p does not
contain any await-statements beyond atomic sections, is first replaced by the
two disjuncts in Corollary 9.3.2 which in turn get processed by successive ap-
plication of the presented syntax-driven rules down to a series of branches to
be closed, i.e. refuted. In each of these we will have access to some additional
piece of event/control flow information, which comprises a collection of specific
to the particular branch state properties exhibited by hypothetical computa-
tions running through the same states as certain suffixes of the initially fixed
computation sq. This essentially allows us to project all this information back
onto sq evincing thereby the relative order of events whenever it is present. For
example, if a program starts with the assignment a :“True followed by the con-
ditional if b “ 1 then q else r fi then one part of the branches will exhibit
the properties σa and σ 1 b “ 1 with σ “ Spsq 1 q, σ 1 “ Spsq n q and 1 ă n, whereas
the other part – the properties σa and σ 1 b ‰ 1 with σ “ Spsq 1 q, σ 1 “ Spsq n q
and 1 ă n. Note that 1 ă n reflects that True is assigned to a first. Chapter 10
describes an application of this technique in detail.


9.4      Program correspondences and fair compu-
         tations
The systematic replaying of computations along program correspondences, as
implemented by the proof of Proposition 4.2.1 handling finite cases, similarly
applies to infinite computations yet without retaining fairness in general. Con-
sider for instance the correspondence |ù pbasic f k qq Ě q with a jump-free q.
Any sq q P vqwfair is thus replayed by the corresponding sq P vbasic f k qwω that
keeps the always available position 10 from making its move once, i.e. basic f
becomes so to say a ‘spare’ component in this process.
    This example underlines that retaining fairness demands additional restric-
tions on program correspondences. We will focus on a componentwise restriction
particularly prohibiting such ‘spare’ components. To sketch the principle sup-
pose |ù p1 Ě q1 and |ù p2 Ě q2 . Then we may require that any step from q1 k q2

                                           85
Verifying Liveness Properties of Programs


having the fired position ix where x P Pos qi and i P t1, 2u is matched by a step
from p1 k p2 with the fired position iy where y P Pos pi . An exact definition of
componentwise correspondence will be elaborated below.
Definition 9.4.1. A term p of type Lα will be called locally non-blocking if for
any p-subterm of the form await C do p1 od we have C “ J and, moreover, for
                                                     ˚
any σ there exists some σ 1 such that ρ $ pp1 , σq ÑP pskip, σ 1 q. Furthermore, a
program pρ, pq is called non-blocking if p is locally non-blocking and ρ i is locally
non-blocking for any label i P Jumpspρ, pq.
    Note that the above definition addresses all subterms of p and not only those
which are determined by the positions of p. Consider for instance a jump-free
p “ basic f ; await K do skip od. Although the position 00 of p, i.e. basic f , is
always available, the program is not non-blocking due to the ‘blocking’ subterm
await K do skip od: any sq P vpwfair has a suffix n |sq P vawait K do skip odwfair
without an available position. By contrast, any Ppsq i q is either skip or has an
always available position when sq P vpwfair
                                       ρ and pρ, pq is non-blocking. This follows
from the property that, as with the sequentiality, the non-blocking condition is
retained by the evaluation: for any step ρ $ pp, σq ÑP pp1 , σ 1 q the program pρ, p1 q
is non-blocking if pρ, pq is.
Definition 9.4.2. Let m ě 1 and r be of type α ˆ β ñ bool. Then two terms,
p of type Lα and q of type Lβ , will be called corresponding componentwise
w.r.t. m, r, ρ, ρ1 if p has the form kp1 , . . . , pm , q has the form kq1 , . . . , qm and,
moreover, the conditions
  (1) ρ, ρ1 |ù pi Ěr qi
  (2) pρ, pi q is sequential
  (3) pρ1 , qi q is non-blocking
hold for all i P t1, . . . , mu.
   Next proposition is essentially an extension of Proposition 4.2.1 to infinite
potential computation in presence of the ‘stuttering’ environment. It more-
over presumes componentwise corresponding programs in order to replay fair
computations as sketched above.
Proposition 9.4.1. Suppose p and q correspond componentwise w.r.t. m, r, ρ, ρ1
                                                                              q
and let sq q P vqwω
                  ρ1 X Env id. Furthermore, let σ0 be a state with pσ0 , Spsq 0 qq P r.
                                      p                                  p
Then there exists a computation sq P vpwω   ρ X Env id such that Spsq 0 q “ σ0 and
the following conditions hold for all n P N:

                                            86
9.4. PROGRAM CORRESPONDENCES AND FAIR COMPUTATIONS


  (1) either Ppsq pn q and Ppsq qn q correspond componentwise w.r.t. m, r, ρ, ρ1 or
      both are skip,
  (2) pSpsq pn q, Spsq qn qq P r,
  (3) if n ą 0 and ρ1 $ sq qn´1 ÑP sq qn has the fired position kx where 1 ď k ď m
      then there exists some x1 such that ρ $ sq pn´1 ÑP sq pn holds with the fired
      position kx1 .
Proof. We will show that to any finite computation sq P vpwρ X Env id satisfying
the conditions (1)–(3) for all n ă |sq| there exists a configuration extending sq to
sq 1 P vpwρ X Env id that in turn satisfies (1)–(3) for all n ď |sq| “ |sq 1 | ´ 1. Using
this argument we can construct an admissible sq p P vpwω          ρ X Env id recursively as
follows. Initially, pp, σ0 q is assigned to sq p0 . Next, let n P N and assume that the
prefix sq p0 , . . . , sq pn being a computation in vpwρ X Env id of length n ` 1 meets
the conditions (1)–(3) for all i ď n. Then any configuration extending the prefix
in the above sense can be assigned to sq pn`1 .
     Now, let sq P vpwρ X Env id, n “ |sq| and suppose that (1)–(3) hold for all
i ă n. Firstly, if there is an environment step sq qn´1 ÑE sq qn then sq qn “ sq qn´1
holds because sq q P Env id. By setting sq n “ sq n´1 we extend sq accordingly to
                                                   def


the computation sq 0 , . . . , sq n´1 ÑE sq n satisfying (1)–(3) for all i ď n.
     Secondly, with a program step ρ1 $ sq qn´1 ÑP sq qn we particularly have that
Ppsq n´1 q and Ppsq qn´1 q correspond componentwise w.r.t. m, r, ρ, ρ1 by the con-
dition (1) since Ppsq qn´1 q ‰ skip. This in turn means Ppsq n´1 q “ ku1 , . . . , um
and Ppsq qn´1 q “ kv1 , . . . , vm hold with some u1 , . . . , um and v1 , . . . , vm satisfying
ρ, ρ1 |ù uk Ěr vk for all 1 ď k ď m.
     Further, if Ppsq qn q ‰ skip then the fired position of ρ1 $ sq qn´1 ÑP sq qn is of
the form kx where 1 ď k ď m and x P Pos vk such that
    – ρ1 $ pvk |x , Spsq qn´1 qq ÑP pw, Spsq qn qq and
    – Ppsq qn q “ kv1 , . . . vk rwsx . . . , vm
hold with some w, i.e. we have ρ1 $ pvk , Spsq qn´1 qq ÑP pvk rwsx , Spsq qn qq. Using
ρ, ρ1 |ù uk Ěr vk we derive thus a matching step ρ $ puk , Spsq n´1 qq ÑP pu1k , σ 1 q
with some u1k and σ 1 satisfying ρ, ρ1 |ù u1k Ěr vk rwsx and pσ 1 , Spsq qn qq P r. Let x1
denote the fired position of ρ $ puk , Spsq n´1 qq ÑP pu1k , σ 1 q, i.e. x1 P Pos uk and
there is some w1 such that ρ $ puk |x1 , Spsq pn´1 qq ÑP pw1 , σ 1 q and u1k “ uk rw1 sx1
hold. Consequently, the program step

       ρ $ pku1 , . . . uk . . . , um , Spsq n´1 qq ÑP pku1 , . . . uk rw1 sx1 . . . , um , σ 1 q

                                                   87
Verifying Liveness Properties of Programs

                                                          def
has the fired position kx1 . Thus, by setting sq n “ pku1 , . . . uk rw1 sx1 . . . , um , σ 1 q
we extend sq to sq 0 , . . . , sq n´1 ÑP sq n satisfying (1)–(3) for all i ď n.
   Finally, in case Ppsq qn q “ skip we can infer vk “ skip and uk “ skip for all
k P t1, . . . , mu and extend sq to sq 0 , . . . , sq n´1 ÑP pskip, Spsq n´1 qq.

    Next proposition complements this result showing that the conditions (1)–
(3) are sufficient to draw conclusions about fairness of replayed computations.

Proposition 9.4.2. Let sq p P vpwω         q     ω
                                  ρ and sq P vqwρ1 be two computations satisfy-
ing the conditions (1)–(3) of the preceding proposition for all n P N. Then sq p
is fair whenever sq q is.

Proof. Let y be an always available position of Ppsq pi q with some i P N. By (1),
Ppsq pi q corresponds to Ppsq qi q componentwise w.r.t. m, r, ρ, ρ1 . This means that
Ppsq pi q “ ku1 , . . . , um and Ppsq qi q “ kv1 , . . . , vm hold with some u1 , . . . , um and
v1 , . . . , vm satisfying ρ, ρ1 |ù uk Ěr vk for all 1 ď k ď m because Ppsq pi q ‰ skip.
     If y “ 0 then we consequently have uk “ vk “ skip for all k P t1, . . . , mu.
Since sq q is assumed to be fair, there must further be some j ě i such that
Ppsq qj q “ kskip, . . . , skip and Ppsq qj`1 q “ skip. By the condition (1) we can
thus once more infer Ppsq pj q “ kskip, . . . , skip and Ppsq pj`1 q “ skip, i.e. we
have the program step ρ $ sq pj ÑP sq pj`1 with the fired position 0.
     Next, suppose y “ kx with k P t1, . . . , mu and x P Pos uk . Hence vk ‰ skip
due to ρ, ρ1 |ù uk Ěr vk and since pρ1 , vk q is assumed to be non-blocking, there
must be an always available x1 P Pos vk . Furthermore, kx1 is an always available
position of Ppsq qi q and since sq q is fair we get some j ě i such that the conditions

    – Ppsqjq q “ kv11 , . . . , vm
                                 1



    – x1 P Pos vk1

    – ρ1 $ sq qj ÑP sq qj`1 has the fired position kx1

hold with some v11 , . . . , vm
                              1
                                . This allows us to draw the following conclusions
regarding sq . Firstly, by the condition (1) we have Ppsq pj q “ ku11 , . . . , u1m with
               p

some locally sequential u11 , . . . , u1m . Secondly, the condition (3) yields a position
x11 P Pos u1k that has been fired by ρ $ sq pj ÑP sq pj`1 .
     It remains to show that the relevant position kx in Ppsq pi q must have been
fired by a step ρ $ sq pl ÑP sq pl`1 with i ď l ď j. Assuming the opposite we can
induce uk |x “ u1k |x and therefore x P Pos u1k holds by Proposition 9.1.1. On the
other hand, from the componentwise correspondence follows that u1k is locally
sequential and has thus at most one program position, i.e. x “ x11 .

                                              88
9.5. A BRIEF SUMMARY


   Combining the results of this section, the proof of the following corollary
consequently resorts first to Proposition 9.4.1 and then to Proposition 9.4.2
showing how termination properties can be carried along componentwise cor-
respondences. The statement’s applicability will be substantiated in the next
chapter establishing termination of fair computations of mutex indirectly via
the auxiliary model mutex aux .
Corollary 9.4.3. Let p and q correspond componentwise w.r.t. m, r, ρ, ρ1 and
assume
 (1) P 1 Ď r ¨ P ,
 (2) for any sq p P vpwfair
                       ρ X In P X Env id there exists some i with Ppsq i q “ skip.

Then for any computation sq q P vqwfair
                                   ρ1 X In P X Env id there also exists some i
                                            1


with Ppsq i q “ skip.
Proof. Let sq q P vqwfair
                      ρ1 X In P X Env id. Then from (1) we get a preimage σ P P
                                 1


of Spsq 0 q under r, i.e. pσ, Spsq q0 qq P r. As a result, Proposition 9.4.1 provides a
        q

corresponding computation sq p P vpwω       ρ X In P X Env id which must be moreover
fair by Proposition 9.4.2. Thus, from (2) we obtain some i with Ppsq pi q “ skip
and can conclude Ppsq qi q “ skip since ρ, ρ1 |ù Ppsq pi q Ěr Ppsq qi q.


9.5      A brief summary
Starting with the question which computations of a particular program reach a
state satisfying a predicate that one normally expects them to reach, this chap-
ter first focused on developing a concise notion of fair computations without
full support for await-statements however (the topic addressed in Section 11.1).
Based on this, a refutational approach to proving liveness properties has led to
a collection of syntax-driven rules for processing programs which are jump-free
and also do not make use of the await-statements beyond atomic sections. Sim-
ilarly to the program logic in Chapter 5 with the input/output and invariant
properties, processing statements by these rules can not only supply arguments
why a program exhibits some liveness property, but also hint to the reasons
why it does not. Lastly, correspondence conditions, stronger than in Proposi-
tion 4.2.1, ensuring that any fair computation of a program can be replayed
by a fair computation of a corresponding program have been elaborated. Next
chapter applies all of the techniques to establish termination of mutex.


                                          89
Chapter 10

Case Study: Proving
Termination

Recall the model mutex of the Peterson’s mutual exclusion algorithm shown
in Figure 6.1. The proofs in Chapter 6 implicitly utilised the property that
the threads cannot be simultaneously within their critical sections in order to
derive that a certain condition holds upon termination of mutex, i.e. for all
computations of mutex that reach a skip-configuration. In this sense it would
have taken significantly less efforts to achieve exactly the same result with a
slightly modified model simply making thread 0 (or thread 1 , or both) spin in
perpetual waiting to enter cs 0 (or cs 1 ), i.e. with while True do skip od in place
of while flag1 ^ turn do skip od. All fairness considerations become basically
irrelevant for (non-)termination of such a contrived model: no computation
will evidently reach a skip-configuration anyway. This is in contrast to the
following, more subtle modification attempting to ‘optimise’ the protocol by
ignoring turn, i.e.

       flag0 :“ True;
       while flag1 do skip od;
       cs 0 ;
       flag0 :“ False

being the modified thread 0 whereas thread 1 is modified accordingly. Although
intuitively clear, it is not straight forward anymore (one can make turn an aux-
iliary variable proceeding similarly to Chapter 6) to show that the threads still

                                        91
Case Study: Proving Termination


would not interfere on a shared resource. But the actual point is that a consid-
erable part of the fair computations would indeed reach a skip-configuration:
one thread can pass to its critical section without any interruption by the other
which can then freely move to its ‘busy waiting’ phase. As opposed to that,
not only a part but all fair computations of mutex eventually reach a skip-
configuration.
     To sum up, the ultimate goal of this part of the case study is a proof that any
computation in vmutex cs 0 cs 1 wfair X Env id reaches a skip-configuration provided
cs 0 and cs 1 unconditionally terminate. Also for this task we will resort to certain
properties of the auxiliary model mutex aux , shown in Figure 6.2, which are not
directly accessible by mutex, i.e. mutex aux is once more scrutinised first.


10.1       Preparations
Following the approach described in Section 9.3, we seek to refute the statement

 Dsq P Env id. sq ,N   turn aux0 ^ turn aux1 Ż mutex aux cs 0 cs 1 Ż K        (10.1)

assuming that any claim of non-termination of cs 0 or cs 1 can be refuted, i.e.

      @sq P. sq .N P Ż cs 0 Ż K
                                                                              (10.2)
      @sq P. sq .N P Ż cs 1 Ż K

                                                        p P Env id having
Now, from the assumption (10.1) we derive a computation sq
moreover the property

    p ,N
    sq       turn aux0 ^ turn aux1 Ż mutex aux cs 0 cs 1 Ż K                  (10.3)

It is essential to note that sqp will refer to this computation in the course of
the entire refutation process, i.e. up to Proposition 10.2.1. Furthermore, the
shorthand σ pi will be used for the state Spsq
                                             p i q of the i-th configuration on sq.
                                                                                p
    Sketching a general refutation plan, an application of the rule for the parallel
composition in Proposition 9.3.6 to (10.3) would produce the three branches:

 (a) thread aux
            0   and thread aux
                           1   do not terminate, or

 (b) thread aux
            0   terminates but thread aux
                                      1   does not, or

 (c) thread aux
            1   terminates but thread aux
                                      0   does not.

                                         92
10.1. PREPARATIONS


     In the branch (a) we could further infer that both threads got stuck in their
‘busy waiting’ phases, i.e. the conditions flag1 ^ turn and flag0 ^ turn must
recur infinitely often on sq,
                           p in particular meaning that the value of turn flips
infinitely many times. On the other hand, we could also derive that starting
from a certain point, the condition turn aux0 ^ turn aux1 holds perpetually
on sqp and hence from this very point the value of turn must remain constant
in contradiction to the previous conclusion.
     In the branch (b) only thread aux
                                    1    gets stuck in its ‘busy waiting’ phase,
i.e. only the condition flag0 ^ turn must recur infinitely often on sq. p On the
other hand, regarding thread aux0  we could now   derive that it eventually assigns
False to flag0 at some point on sq,
                                  p and hence flag0 holds perpetually starting
from this point. Altogether we would get a state on sq  p where both, flag0 and
flag0 , hold.
     The branch (c) is clearly symmetric to (b): replacing turn by turn as well
as swapping 0 and 1 in the preceding paragraph yields the sought contradiction.
We therefore will not treat this branch explicitly in what follows.
     Although rather superficial, these considerations nonetheless reveal that in
order to close a branch we appeal to certain invariants (e.g. flag0 keeps its
value once False assigned) which hold on any sq P vmutex aux wω X Env id. These
invariants are accurately captured by the guarantees of the following extended
Hoare triple

 |ùω tid,   turn aux0 ^ turn aux1 u mutex aux cs 0 cs 1 tJ, Gglobal u         (10.4)

where Gglobal accordingly stands for

 pturn aux0 ÝÑ turn aux10 q ^ pturn aux1 ÝÑ turn aux11 q ^
 pturn aux0 ^ flag10 ÝÑ flag0 q ^ pturn aux1 ^ flag11 ÝÑ flag1 q ^
 pturn aux0 ^ turn aux1 ÝÑ turn “ turn1 q.

The triple (10.4) is derivable using the program logic rules from Chapter 5 under
the assumptions |ù tJ, Ju cs 0 tJ, Gcs u and |ù tJ, Ju cs 1 tJ, Gcs u with Gcs merely
requiring from each program step of cs0 and cs1 to leave the auxiliary and the
protocol variables unmodified:
  turn aux0 “ turn aux10 ^ turn aux1 “ turn aux11 ^
  flag0 “ flag10 ^ flag1 “ flag11 ^ turn “ turn1 .
It is worth noting that the guarantees in Gglobal , immaterial from the perspec-
tive of potential interferences between the two threads (cf. Proposition 6.2.1),
become decisive arguments in the liveness context.

                                         93
Case Study: Proving Termination


                                                                 p P Prog Gglobal
    Now, the primary purpose of the triple (10.4) is to conclude sq
            p P vmutex aux cs 0 cs 1 wω X In p turn aux0 ^ turn aux1 q X Env id
using that sq
is a straight consequence of (10.3). This notably means that
      pi turn aux0 ÝÑ σ
  (i) σ               pi`1 turn aux0
      pi turn aux1 ÝÑ σ
 (ii) σ               pi`1 turn aux1
      pi turn aux0 ^ σ
(iii) σ              pi`1 flag0 ÝÑ σ
                                   pi flag0
      pi turn aux1 ^ σ
 (iv) σ              pi`1 flag1 ÝÑ σ
                                   pi flag1
     pi turn aux0 ^ σ
 (v) σ              pi turn aux1 ÝÑ σ
                                    pi turn “ σ
                                              pi`1 turn
hold globally on sq,
                  p i.e. for all i regardless of the kind of the transition from sqpi
to sq
   p i`1 : the program steps are covered by the above conclusion sq   p P Prog Gglobal
whereas the environment – by the property sq   p P Env id since (i)–(v) are especially
valid when σ pi “ σ
                  pi`1 .
    Next two propositions utilise (i)–(v) in order to derive relevant properties
for certain suffixes of sq.
                         p
Proposition 10.1.1. Let n, m P N with σ  pn turn aux0 and σ pm turn aux1 . Then
there exists d P N such that σ
                             pi turn “ σ
                                       pj turn holds for all i ě d and j ě d.
Proof. Let d be the maximum of n and m. With (i) and (ii) we can induce
pi turn aux0 ^ σ
σ                pi turn aux1 for all i ě d. Then σ
                                                  pi turn “ σ pi`1 turn follows for
all i ě d by (v). Thus, σpi turn “ σ
                                   pj turn holds for all i ě d and j ě d.
Proposition 10.1.2. Assume σ   pm turn aux0 and         pn flag0 with m ď n. Then
                                                        σ
 pi flag0 holds for all i ě n.
 σ
Proof. With (i) we first induce σpi turn aux0 for all i ě m. Then with       pn flag0
                                                                             σ
and (iii) we conclude σ pi flag0 for all i ě n.


10.2       The actual refutation
Following the general plan we start with processing (10.3) by successive ap-
plication of the syntax-driven rules from Section 9.3. Resolving the parallel
composition operator in the first place, an application of Proposition 9.3.6 to
(10.3) yields two computations sq 0 and sq 1 with sq 0 „ sq
                                                         p and sq 1 „ sq
                                                                      p such that
either
       sq 0 ,N turn aux0 ^ turn aux1 Ż thread aux   0   cs 0 Ż K
          1                                         aux                    (10.5)
       sq ,N turn aux0 ^ turn aux1 Ż thread 1 cs 1 Ż K

                                         94
10.2. THE ACTUAL REFUTATION


or
        sq 0 ,T   turn aux0 ^ turn aux1 Ż thread aux
                                                 0   cs 0 Ż K Ż n
                                                                            (10.6)
        sq 1 ,N   turn aux0 ^ turn aux1 Ż thread aux
                                                 1   cs 1 Ż K
hold with some n P N. Note once more that the third disjunct is omitted in this
presentation because it is the same as (10.6) with the indices 0 and 1 swapped.
    Further processing (10.5) using the rules from Section 9.3 leads to several
trivially refutable branches such as
        sq 1 ,N   turn aux0 ^ turn aux1 Ż flag0 :“ True Ż K , or
        sq ,N J Ż xturn :“ True; turn aux0 :“ Truey Ż K
          11



for some sq 1 and sq 11 . Moreover, note that all branches claiming termination
of the ‘busy waiting’ phase of thread aux
                                       0   or thread aux
                                                     1   are simply refutable as
well because all other parts of the program are unconditionally terminating due
to (10.2) which is a contradiction to (10.5). As a result, it remains only one
non-trivial branch exhibiting the following properties:
 (a) there are some m0 , m1 P N with σ
                                     pm0 turn aux0 and σ
                                                       pm1 turn aux1
 (b) there are two strictly ascending sequences of natural numbers φ, ψ and
     also some d0 ą m0 and d1 ą m1 such that both
              pφi `d0 flag1 ^ σ
        (b0 ) σ               pφi `d0 turn
              pψi `d1 flag0 ^ σ
        (b1 ) σ               pψi `d1 turn
        hold for all i P N.
Then by Proposition 10.1.1 and (a) we obtain some d such that the equality
pi turn “ σ
σ                                                       pφd `d0 turn “ σ
           pj turn holds for all i, j ě d, i.e. we have σ              pψd `d1 turn
in particular due to φd ě d and ψd ě d. In contradiction to that, σ    pφd `d0 turn
and σ pψd `d1 turn follow respectively from (b0 ) and (b1 ).
    Next we backtrack to the pending branch (10.6) that still needs to be pro-
cessed. Note that successive application of the rules from Section 9.3 to

     sq 0 ,T   turn aux0 ^ turn aux1 Ż thread aux
                                              0 cs 0 Ż K Ż n

goes ahead without any further branching, thereby producing a series of con-
clusions about the shape of sq 0 and hence also of sq.p In particular, we ob-
tain σ pn flag0 , i.e. flag0 holds on the n-th state of sq
                                                        p since the assignment
flag0 :“ False is carried out by the last program step on sq 0 . Moreover, we get

                                             95
Case Study: Proving Termination


some m ă n with σm turn aux0 , and hence Proposition 10.1.2 provides a more
advanced conclusion that σi flag0 holds for all i ě n. Regarding the opposite
thread, further processing of the assumption
  sq 1 ,N   turn aux0 ^ turn aux1 Ż thread aux
                                           1 cs 1 Ż K

as with (10.5) results in only one non-trivially refutable branch where we have
a strictly ascending sequence φ and some d such that σφi `d flag0 ^ σφi `d turn
holds for all i P N and hence for n in particular, i.e. σφn `d flag0 . On the other
hand we also have σφn `d flag0 since φn ě n.
    This concludes the refutation process of (10.1) so that the following propo-
sition can summarise the result:
Proposition 10.2.1. Assume
 (1) |ù tJ, Ju cs 0 tJ, Gcs u,
 (2) |ù tJ, Ju cs 1 tJ, Gcs u,
 (3) sq ,N P Ż cs 0 Ż K yields a contradiction for all sq and P ,
 (4) sq ,N P Ż cs 1 Ż K yields a contradiction for all sq and P .
Then any sq P vmutex aux cs 0 cs 1 wfair X Inp turn aux0 ^ turn aux1 q X Env id
has some n P N such that Ppsq n q “ skip.


10.3        Termination of mutex
To derive the corresponding result for mutex we proceed similarly to Section 6
using Corollary 9.4.3 instead of Proposition 4.2.1. The program correspondence,
   |ù mutex aux cs 0 cs 1 Ěreqv mutex cs 0 cs 1
established in Section 6, is however per se not sufficient because Corollary 9.4.3
presumes |ù thread aux                                          aux
                    0 cs 0 Ěreqv thread 0 cs 0 and |ù thread 1 cs 1 Ěreqv thread 1 cs 1
On the other hand, these correspondences have been implicitly derived from the
assumptions |ù cs 0 Ěreqv cs 0 and |ù cs 1 Ěreqv cs 1 in the proof of Proposition 6.3.1
since it used the syntax-driven rules from Section 3.2.1 only. Furthermore, note
that thread aux        aux
            0 , thread 1 , thread 0 and thread 1 are by definition sequential and
non-blocking, provided cs 0 and cs 1 are sequential and non-blocking.
    This essentially means that mutex aux cs 0 cs 1 and mutex cs 0 cs 1 correspond
componentwise w.r.t. reqv by Definition 9.4.2 whenever cs 0 and cs 1 are sequen-
tial and non-blocking as well as |ù cs 0 Ěreqv cs 0 and |ù cs 1 Ěreqv cs 1 hold.

                                            96
10.3. TERMINATION OF mutex


Proposition 10.3.1. Assume
 (1) |ù tJ, Ju cs 0 tJ, Gcs u,
 (2) |ù tJ, Ju cs 1 tJ, Gcs u,
 (3) sq ,N P Ż cs 0 Ż K yields a contradiction for any sq and P ,
 (4) sq ,N P Ż cs 1 Ż K yields a contradiction for any sq and P ,

 (5) |ù cs 0 Ěreqv cs 0 ,
 (6) |ù cs 1 Ěreqv cs 1 ,
 (7) cs 0 and cs 1 are sequential and non-blocking.
Then any sq P vthread 0 cs 0 k thread 1 cs 1 wfair X Env id eventually reaches a skip-
configuration.
Proof. Using Proposition 10.2.1 and the assumptions (1)–(4) we infer that any
sq P vmutex aux cs 0 cs 1 wfair X In p turn aux0 ^ turn aux1 q X Env id reaches a
skip-configuration. Moreover, mutex aux cs 0 cs 1 and mutex cs 0 cs 1 correspond
componentwise w.r.t. reqv due to the assumptions (5)–(7). Hence, in order to
apply Corollary 9.4.3 only J Ď reqv ¨ p turn aux0 ^ turn aux1 q remains to
be shown, i.e. for any σ there is some σ 1 with σ 1 turn aux0 , σ 1 turn aux1
                               def
and pσ 1 , σq P reqv . Set σ 1 “ σrturn aux0 :“ False, turn aux1 :“ Falses to this end.
    Regarding lastly the instantiation of cs 0 and cs 1 by update 0 and update 1 ,
defined in Section 6.4, any sq P vmutex update 0 update 1 wfair X Env id reaches a
skip-configuration by Proposition 10.3.1.
    The side condition ‘if such exists’ in the final result of Section 8.2 is now
discarded as follows: σshared Y t0, 1u “ σ 1 shared holds for any computation
sq P vmutex update 0 update 1 wfair X Env id where σ “ Spsq 0 q and σ 1 is the state of
the first skip-configuration on sq.




                                          97
Chapter 11

Conclusion

This report gave a detailed presentation of a framework, built as a conservative
extension to the simply typed higher-order logic and geared towards modelling,
verification and transformation of concurrent imperative programs. The essen-
tial points were:

   - a concise computational model encompassing fine-grained interleaving,
     state abstraction and jump instructions;

   - stepwise program correspondence relations allowing us in particular to
     reason upon properties of programs that use jumps in place of conditional
     and while-statements via a semantic equivalence to their structured coun-
     terparts;

   - a Hoare-style rely/guarantee program logic seamlessly tied in with the
     state abstraction and featuring the program correspondence rule as a gen-
     eralised rule of consequence;

   - a light-weight extension of the logic enabling state relations in place of
     pre/postconditions;

   - a refutational approach to proving liveness properties driven by a concise
     notion of fair computations.

The remainder of the chapter discusses further enhancements to the framework.

                                      99
Conclusion


11.1         Fair computations and await-statements
As pointed out in Section 9.2, a plain generalisation of Definition 9.2.2 from
always available to any program position would essentially require from in this
sense fair computations of await C do p od to visit a state satisfying C at least
once, confining thus the scope of liveness reasoning to rather a handpicked (and
sometimes even empty) subset of the potential computations of programs that
make use of await-statements beyond atomic sections. Whereas the concept of
an always available position can conveniently be detached from any notion of
computation, availability of a position referring to some wait C cannot: de-
pending on the computational context such program positions may be regarded
either as available or not. More precisely, such a position is certainly unavailable
on a computation that does not visit a state in C at all but it might become
available on a computation which does, leading to the question: how often shall
a computation pass through a state in C so that one can sensibly require from
it to reduce the subterm wait C to skip once? A finite number might be ap-
propriate to tackle some very specific models, but the general answer shall be:
infinitely often. Always available positions fit in this scheme as a corner case:
any infinite computation visits a state satisfying J infinitely often.
    As a result of these considerations, part (1) of Proposition 9.3.3 could be
generalised as follows:

   – if sq ,N P Ż await C do p od Ż Q then either
       (a) there exists a state σ such that for all σ 1 the configuration pskip, σ 1 q
           is not reachable from pp, σq by any sequence of program steps, i.e.
                   ˚
           pp, σq ­ÑP pskip, σ 1 q, or
      (b) the condition C recurs only finitely many times on sq.

Once more, Proposition 9.3.3 would be an instance of the above rule because J
does trivially recur infinitely often on any infinite computation. Processing thus
programs that resort to await-statements for synchronisation purposes we would
have to close the additional branch (b). The according variation of mutex aux

  flag0 :“ True;                flag1 :“ True;
 xturn :“ True;                xturn :“ False;
  turn aux0 :“ Truey;           turn aux1 :“ Truey;
  wait flag1 _ turn;            wait flag0 _ turn;
  cs 0 ;                        cs 1 ;
  flag0 :“ False                flag1 :“ False

                                        100
11.2. ENHANCING THE REFUTATIONAL APPROACH


can be used to illustrate this. As with mutex aux in Chapter 10 we process this
model by successive application of the syntax-driven rules from Section 9.3. In
contrast to Chapter 10, with this variation we clearly do not need to apply the
rule for while-statements, but encounter instead a branch carrying the assump-
tion of the form sq ,N P Ż wait flag1 _ turn Ż Q where sq „ sq.   p
    Appealing to the above presented, generalised version of Proposition 9.3.3
we could infer that flag1 _ turn recurs only finitely many times on sq and
hence also on sqp due to sq „ sq.
                               p Furthermore, non-termination assumption for
the second thread would let us symmetrically derive that flag0 _ turn recurs
only finitely many times on sq.
                              p We could thus reason that there must be
   – a suffix d0 |sq
                  p on which flag1 ^ turn holds globally, and
   – a suffix d1 |sq
                  p on which flag0 ^ turn holds globally.
Since ‘globally’ in particular means here ad infinitum, quite similarly to Chap-
ter 10 we would get a contradiction in form of a state σ on sq
                                                             p such that σturn
and σturn hold regardless whether we have d0 ď d1 or d0 ě d1 .


11.2      Enhancing the refutational approach
Each rule in Section 9.3 essentially just carried around the parameter Q, set to
capture an invariant condition on sq when drawing conclusions from assump-
tions of the form sq ,N P Ż p Ż Q or sq ,T P Ż p Ż Q Ż n. The sole motivation
behind that was to achieve a better perception of the underlying approach.
This parameter can actually be taken out and the invariant asserted only once
for the initial computation: the refutational approach using the syntax-driven
rules in Section 9.3 works the same regardless if we start with the assumption
Dsq P Env id. sq ,N P Ż p Ż Q or Dsq P Env id. sq ,N P Ż p Ż K ^ @i. Spsq i q R Q.
In the latter case we however avoid propagation of the invariant @i. Spsq 1i q R Q
explicitly down to each computation sq 1 that arises by successive application of
the rules.
    It is beneficial to keep track of environment conditions instead. To this end,
Definition 9.3.2 and Definition 9.3.3 shall respectively be updated to:
Definition 11.2.1. sq ,N R Ż P Ż p holds iff sq P vpwfair X Env R X In P X Out K
(note that sq P Out K is by Definition 4.1.4 equivalent to Ppsq i q ‰ skip for all
i P N).
Definition 11.2.2. Let additionally n P N. Then sq ,T R Ż P Ż p Ż n holds iff
sq P vpwω X Env R X In P and n is the least number such that Ppsq n q “ skip.

                                       101
Conclusion


     Adjusting the syntax-driven rules in Section 9.3 to this setting, only the
rule for the parallel composition cannot simply pass the environment condi-
tion parameter to the emerging computations. More precisely, the proof of
Proposition 9.3.6 derives from sq P vp k qwfair two computations sq p P vpwfair and
sq q P vqwfair such that program steps of sq p become supplementary environment
steps on sq q and vice versa. For that reason we cannot draw any particular con-
clusions regarding environment conditions on sq p and sq q from the assumption
sq P Env R alone, but assuming additionally the extended Hoare triples
     |ù tJ, Ju p tJ, Gp u   with some Gp Ě R
                                                                             (11.1)
     |ù tJ, Ju q tJ, Gq u   with some Gq Ě R
would consequently provide sq p P Env Gq and sq q P Env Gp . That is, an adjusted
rule for the parallel composition operator shall derive from the assumptions
sq ,N R Ż P Ż p k q and (11.1) that there exist sq p „ sq and sq q „ sq such that
either
 (a) sq p ,N Gq Ż P Ż p and sq q ,N Gp Ż P Ż q, or
 (b) sq p ,N Gq Ż P Ż p and there is some n with sq q ,T Gp Ż P Ż q Ż n, or
 (c) sq q ,N Gp Ż P Ż q and there is some n with sq p ,T Gq Ż P Ż p Ż n.
Note that with Gp “ Gq “ J the assumptions (11.1) become valid for all p and
q so that we in principle get back the part (1) of Proposition 9.3.6.
     Considering mutex aux once more but under a shifted angle, we may thus
refute the assumption sq p ,N id Ż turn aux0 ^ turn aux1 Ż mutex aux cs 0 cs 1
for a fixed initial computation sq.
                                  p To apply the above parallel composition rule
it is feasible to instantiate Gp by G0 and Gq by G1 where
        def
    G0 “ turn aux1 “ turn aux11 ^ flag1 “ flag11
        def
    G1 “ turn aux0 “ turn aux10 ^ flag0 “ flag10
noting that both, G0 and G1 , are reflexive state relations. As the result, we in
particular would have to close the branch with two computations sq 0 „ sq  p and
sq 1 „ sq
       p such that
    sq 0 ,N G1 Ż turn aux0 ^ turn aux1 Ż thread aux
                                                0   cs 0
    sq 1 ,N G0 Ż turn aux0 ^ turn aux1 Ż thread aux
                                                1 cs 1

hold and the set of hypothetical solutions to sq 0 and sq 1 gets strictly reduced in
comparison to Section 10.2 due to the properties sq 0 P Env G1 and sq 1 P Env G0 .
The merits of the refined technique will be highlighted in the next section.

                                        102
11.3. ABSTRACTION AND GRANULARITY



                         flag0 :“ True;
                        xturn :“ True;
                         turn aux0 :“ Truey;
                         checkout 0 ;
                         while mxcond0 do checkout 0 od;
                         cs 0 ;
                         flag0 :“ False


                       Figure 11.1: thread aux
                                           0   ‘unfolded’ .


11.3      Abstraction and granularity
As pointed out at the beginning of the case study in Chapter 6, the conditions
flag1 ^ turn and flag0 ^ turn, deployed by mutex to keep one of the threads
spinning, are actually examples of modelling that on the one hand makes the
essentials significantly clearer, but on the other – abstracts over interleaving to
which an eventual implementation may be subjected because from the low-level
code perspective an evaluation of e.g. flag1 ^ turn requires a series of atomic
actions: reading the respective Boolean values out of the memory, computing
their conjunction and storing the result so that a conditional jump can correctly
be performed. By then we in particular could not say whether the shared
memory locations still contain the values that have been read out at the start
of such a ‘checkout’ phase.
    Expressing that in terms of L, we ‘unfold’ thread aux
                                                       0   to the model shown in
Figure 11.1 where the additional parameter checkout 0 shall be instantiated by

      checkout 0 ÞÑ local flag0 :“ flag1 ;
                    local turn0 :“ turn;                                     (11.2)
                    mxcond0 :“ local flag0 ^ local turn0

with thread aux
             1  modified accordingly using checkout 1 .
    Thus, the model resides at a finer level of granularity than mutex aux in Fig-
ure 6.2, and the conclusion that it retains the properties, presented in Proposi-
tion 6.2.1 and Proposition 10.2.1, is not at all immediate: a state satisfying both,
flag1 and turn, is not explicitly required anymore to keep thread aux  0    spinning
in the ‘busy waiting’ phase so that especially the liveness reasoning in Chap-
ter 10 demands a revision. The crucial point to this end is that based on the

                                        103
Conclusion


enhancements to the refutational approach outlined in the preceding section, it
is strikingly more expedient to leave checkout 0 as another parameter alongside
cs 0 specifying a variety of its admissible instances as follows.
    Let R0 from now on denote the condition that the state variables local flag0 ,
local turn0 and mxcond0 remain unmodified, whereas G0 – that all other
variables remain unmodified. Symmetrically we have R1 and G1 for the state
variables local flag1 , local turn1 , mxcond1 and their complement. Then the
assumptions

(1)    |ù tJ, Ju checkout 0 tJ, G0 u
(2)    |ù tR0 , mxcond0 u checkout 0 tJ, mxcond10 ÝÑ mxcond0 u
(3)    |ù tpturn “ turn1 q ^ R0 , Ju checkout 0 tmxcond0 ÝÑ turn, Ju
(4)    |ù tpflag11 ÝÑ flag1 q ^ R0 , flag1 u checkout 0 t mxcond0 , Ju
(5)    @sq P R. sq .N R Ż P Ż checkout 0 .

(and accordingly for checkout 1 ) are sufficient to prove termination of the model
parameterised by checkout 0 and checkout 1 , being in particular resolvable by the
instantiation (11.2). What is more, this abstraction makes the verification pro-
cess significantly more structured and concise as will be sketched below keeping
to a refutation plan that in many aspects leans on the plan used in Chapter 10.
    Utilising the enhancement to the refutational approach drafted in the pre-
ceding section, we thus seek to refute the assumption

      p ,N id Ż P Ż mutex aux checkout 0 cs 0 checkout 1 cs 1
      sq                                                                   (11.3)

with a fixed initial computation sq
                                 p and P denoting the state predicate

       turn aux0 ^ turn aux1 ^ mxcond0 ^ mxcond1 .

Provided by the assumptions (1) and |ù tJ, Ju checkout 1 tJ, G1 u, the global
guarantees Gglobal (cf. (10.4) in Chapter 10)

|ùω tid, Pu mutex aux checkout 0 cs 0 checkout 1 cs 1 tJ, Gglobal u

remain derivable and apply thus to sq.
                                   p Recall that Gglobal in particular contains
turn aux0 ^ turn aux1 ÝÑ turn “ turn1 and turn aux0 ÝÑ turn aux10 and
turn aux1 ÝÑ turn aux11 . In the current setting we can moreover derive
|ùω tJ, Ju thread aux
                  0   checkout 0 cs 0 tJ, R1 u
                                                                           (11.4)
|ùω tJ, Ju thread aux
                  1   checkout 0 cs 1 tJ, R0 u

                                          104
11.3. ABSTRACTION AND GRANULARITY


and
|ùω tR0 , mxcond0 u thread aux                         1
                           0 checkout 0 cs 0 tJ, mxcond0 ÝÑ mxcond0 u
                                                                     (11.5)
|ùω tR1 , mxcond1 u thread aux                         1
                           1 checkout 0 cs 1 tJ, mxcond1 ÝÑ mxcond1 u

Using (11.4), an application of the parallel composition rule, sketched in the
preceding section, to (11.3) accordingly yields two computations sq 0 and sq 1
with sq 0 „ sq
            p and sq 1 „ sq
                         p such that either
 (a) sq 0 ,N R0 Ż P Ż thread aux
                             0   checkout 0 cs 0 and
        1                    aux
     sq ,N R1 Ż P Ż thread 1 checkout 1 cs 1 , or
 (b) sq 0 ,N R0 Ż P Ż thread aux
                             0   checkout 0 cs 0 and there is some n with
      sq 1 ,T R1 Ż P Ż thread aux
                              1   checkout 1 cs 1 Ż n, or
 (c) sq 1 ,N R1 Ż P Ż thread aux
                             1   checkout 1 cs 1 and there is some n with
        0                   aux
     sq ,T R0 Ż P Ż thread 0 checkout 0 cs 0 Ż n.
     An argumentation closing the branch (a) can be briefly outlined as fol-
lows. Processing both statements in (a) up to checkout 0 and checkout 1 us-
ing the syntax-driven rules yields a state on sq 0 where turn aux0 holds and
a state on sq 1 where turn aux1 holds. Projected back onto sq,     p we once more
(cf. Chapter 10) get some d such that turn aux0 ^ turn aux1 and hence also
turn “ turn1 hold globally on the suffix d |sq.p
     Propagating this result the other way round along the state equivalence
sq 0 „ sq
       p , for any two states σ, σ 1 on the suffix d |sq 0 we have σturn “ σ 1 turn.
We clearly get the same result for the suffix d |sq 1 due to sq 1 „ sq.p Next two
paragraphs focus on drawing further conclusions for thread aux  0   checkout 0 cs 0 .
     Unconditional termination for all instances of cs 0 has been assumed in Chap-
ter 10 whereas the assumption (5) additionally asserts the same for all instances
of checkout 0 . Thus sq 0 ,N R0 Ż P Ż thread aux
                                             0 checkout 0 cs 0 can hold only due to
non-termination of the ‘busy waiting’ phase while mxcond0 do checkout 0 od.
More precisely, processing sq 0 ,N R0 Ż P Ż thread aux
                                                     0 checkout 0 cs 0 using syntax-
driven rules yields a strictly ascending infinite sequence φ such that for all i P N
we have a computation i sq „ φi |sq 0 with i sq ,T R0 Ż mxcond0 Ż checkout 0 Ż i n
for some i n ă φi`1 ´ φi (the notations i sq and i n shall just emphasise that the
values are actually parameterised by i). From this we can further infer
  (i) d sq ,T pturn “ turn1 q^R0 Ż mxcond0 Ż checkout 0 Ż d n with d sq „ φd |sq 0
 (ii) for all states σ on sq 0 we have σmxcond0 “True.

                                         105
Conclusion


To (i) note that σturn “ σ 1 turn holds for any σ, σ 1 on d |sq 0 and for environment
steps on d sq in particular, since d ď φd . Regarding (ii), if there would be a state
σh0 “ Spsq 0h q with σh0 mxcond0 then using (11.5) we can derive σj0 mxcond0
for all j ě h and hence for φh ě h in particular, which is a contradiction since
the state Spsq 0φh q satisfies mxcond0 .
    Now with (i) we can take the decisive advantage of the checkout 0 abstraction:
the triple (3) ensures that for all sq P vcheckout 0 w X Env ppturn “ turn1 q ^R0 q
we have sq P Out pmxcond0 ÝÑ turnq whereas d sq not only meets the relevant
conditions but also reaches a skip-configuration in d n steps by (i). Hence we
have a state σ on φd |sq 0 such that σturn “True holds due to (ii). Then a
projection back onto sq  p yields that turn must hold globally on d |sq p because the
value of turn is constant on d |sq.p
    Recasting the argumentation in the last two paragraphs to thread aux   1   accord-
ingly yields that turn also holds globally on d |sq.p Altogether we particularly
get Spsqp d q P K and hence the branch (a) is closed.
    As in Chapter 6 and Chapter 10 we can establish a program correspondence
between the model in Figure 11.1 and

                         flag0 :“ True;
                         turn :“ True;
                         checkout 0 ;
                         while mxcond0 do checkout 0 od;
                         cs 0 ;
                         flag0 :“ False

translating the relevant protocol properties along the correspondence. Applying
subsequently the transformations from Section 3.3 and Section 3.4 in order to
replace the while-statements by jumps in both threads, we in principle arrive at
the componentwise equivalent representation

    flag0 :“ True;                              flag1 :“ True;
    turn :“ True;                               turn :“ False;
    checkout 0 ;                                checkout 1 ;
1 : cjump mxcond0 to 2                      3 : cjump mxcond1 to 4
     otherwise checkout 0 ; jump 1 end;          otherwise checkout 1 ; jump 3 end;
2 : cs 0 ;                                  4 : cs 1 ;
    flag0 :“ False                              flag1 :“ False

which is notably closer to a template for provably correct assembly level imple-
mentations derived from the Peterson’s mutual exclusion algorithm.

                                          106
Bibliography

[1] Radio Technical Commission for Aeronautics (RTCA). DO-333: Formal
    methods supplement to DO-178C and DO-278A, 2011.

[2] Radio Technical Commission for Aeronautics (RTCA). DO-178C: Software
    Considerations in Airborne Systems and Equipment Certification, 2011.

[3] Robin Milner. Implementation and applications of Scott’s logic for com-
    putable functions. SIGPLAN Notices, 7(1):1–6, January 1972.

[4] Robin Milner. The use of machines to assist in rigorous proof. Philosophical
    Transactions of the Royal Society of London A: Mathematical, Physical and
    Engineering Sciences, 312(1522):411–422, 1984.

[5] Tobias Nipkow, Lawrence Paulson, and Markus Wenzel. Isabelle/HOL —
    A Proof Assistant for Higher-Order Logic, volume 2283 of Lecture Notes in
    Computer Science. Springer, 2002.

[6] John Harrison. HOL light: An overview. In Stefan Berghofer, Tobias Nip-
    kow, Christian Urban, and Makarius Wenzel, editors, Theorem Proving in
    Higher Order Logics, 22nd International Conference, TPHOLs 2009, Mu-
    nich, Germany, August 17-20, 2009. Proceedings, volume 5674 of Lecture
    Notes in Computer Science, pages 60–66. Springer, 2009.

[7] Michael J. C. Gordon. Introduction to the HOL system. In Myla Archer,
    Jeffrey J. Joyce, Karl N. Levitt, and Phillip J. Windley, editors, Proceed-
    ings of the 1991 International Workshop on the HOL Theorem Proving
    System and its Applications, August 1991, Davis, California, USA, pages
    2–3. IEEE Computer Society, 1991.

                                     107
BIBLIOGRAPHY


 [8] Darren Cofer and Steven Miller. DO-333 certification case studies. In Ju-
     lia M. Badger and Kristin Yvonne Rozier, editors, NASA Formal Methods,
     pages 1–15. Springer, 2014.
 [9] Colin Stirling. A generalization of Owicki-Gries’s Hoare logic for a concur-
     rent while language. Theoretical Computer Science, 58(1):347–359, 1988.
[10] Susan Owicki and David Gries. An axiomatic proof technique for parallel
     programs. Acta Informatica, 6:319–340, 1976.
[11] Leonor P. Nieto. Verification of parallel programs with the Owicki-Gries and
     Rely-Guarantee methods in Isabelle/HOL. PhD thesis, Technical University
     Munich, Germany, 2002.
[12] Norbert Schirmer. Verification of Sequential Imperative Programs in Is-
     abelle/HOL. PhD thesis, Technical University Munich, Germany, 2006.
[13] Stephan van Staden. On rely-guarantee reasoning. In Ralf Hinze and
     Janis Voigtländer, editors, Mathematics of Program Construction - 12th
     International Conference, MPC 2015, Königswinter, Germany, June 29
     - July 1, 2015. Proceedings, volume 9129 of Lecture Notes in Computer
     Science, pages 30–49. Springer, 2015.
[14] Gordon D. Plotkin. The origins of structural operational semantics. The
     Journal of Logic and Algebraic Programming, 60-61:3–15, 2004.
[15] David Park. Concurrency and automata on infinite sequences. In Peter
     Deussen, editor, Theoretical Computer Science, pages 167–183. Springer,
     1981.
[16] Robin Milner. A Calculus of Communicating Systems, volume 92 of Lecture
     Notes in Computer Science. Springer, 1980.
[17] Colin Stirling. Decidability of bisimulation equivalence for normed push-
     down processes. Theoretical Computer Science, 195(2):113–131, 1998.
[18] Olaf Burkart, Didier Caucal, Faron Moller, and Bernhard Steffen. Ver-
     ification on infinite structures. In Jan A. Bergstra, Alban Ponse, and
     Scott A. Smolka, editors, Handbook of Process Algebra, pages 545–623.
     North-Holland / Elsevier, 2001.
[19] C. A. R. Hoare. An axiomatic basis for computer programming. Commu-
     nications of the ACM, 12(10):576–580, October 1969.

                                      108
BIBLIOGRAPHY


[20] Leonor P. Nieto. The rely-guarantee method in Isabelle/HOL. In Pier-
     paolo Degano, editor, Programming Languages and Systems, pages 348–
     362. Springer, 2003.
[21] Gary L. Peterson. Myths about the mutual exclusion problem. Information
     Processing Letters, 12(3):115–116, 1981.
[22] Rob van Glabbeek. Ensuring liveness properties of distributed systems:
     Open problems. Journal of Logical and Algebraic Methods in Programming,
     109:100480, 2019.
[23] Orna Kupferman and Moshe Y. Vardi. Verification of fair transition sys-
     tems. In Rajeev Alur and Thomas A. Henzinger, editors, Computer Aided
     Verification, pages 372–382. Springer, 1996.
[24] Yonit Kesten, Amir Pnueli, Li-on Raviv, and Elad Shahar. Model checking
     with strong fairness. Formal Methods in System Design, 28(1):57–84, 2006.

[25] Franz Baader and Tobias Nipkow. Term Rewriting and All That. Cam-
     bridge University Press, 1998.




                                     109
Index

atomic                           state part, 11
    section, 13
    step, 11                 extended Hoare triple, 35

bisimulation, 17             framework language
                                 await-statement, 10
computation                        wait , 10
     actual, 30                  conditional jump, 10
     composition, 16             conditional statement, 10
     fair, 76                    grammar, 10
                                 label, 10
     potential
                                 parallel composition, 10
        finite, 16
                                 sequential composition, 10
        infinite, 15
                                 state predicate, 10
     prefix, 16
                                 state transformer, 10
     step
                                 while-statement, 10
        environment, 14
        program, 11          jump
     suffix, 16                  conditional, 10
condition                        unconditional, 11
     environment, 29, 30     jump-free
     guarantee, 35               program, 14
     input, 30                   term, 10
     output, 30
     program, 29             locally non-blocking term, 86
     rely, 35                locally sequential term, 10
configuration, 11
     program part, 11        program, 14
     skip, 11                    equivalence, 21

                           111
INDEX


    jump-free, 14
    non-blocking, 86
    sequential, 15
    well-formed, 15
program correspondence, 19
    componentwise, 86
    mutual, 19
program position, 73
    always available, 76
    fired, 75

relational
     composition, 19
     image, 36
retrieving function, 11

simulation, 19
stability, 38
state variable, 41
     assignment, 41




                             112
