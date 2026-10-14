                                        Incremental units-of-measure verification
                                        MATTHEW DANISH, University of Cambridge, United Kingdom
                                        DOMINIC ORCHARD, University of Kent, United Kingdom
arXiv:2406.02174v1 [cs.PL] 4 Jun 2024




                                        ANDREW RICE, University of Cambridge, United Kingdom
                                        Despite an abundance of proposed systems, the veriﬁcation of units-of-measure within programs remains
                                        rare in scientiﬁc computing. We attempt to address this issue by providing a lightweight static veriﬁcation
                                        system for units-of-measure in Fortran programs which supports incremental annotation of large projects.
                                        We take the opposite approach to the most mainstream existing deployment of units-of-measure typing (in
                                        F#) and generate a global, rather than local, constraints system for a program. We show that such a system can
                                        infer (and check) polymorphic units speciﬁcations for under-determined parts of the program. Not only does
                                        this ability allow checking of partially annotated programs but it also allows the global constraint problem
                                        to be partitioned. This partitioning means we can scale to large programs by solving constraints for each
                                        program module independently and storing inferred units at module boundaries (separate veriﬁcation). We
                                        provide an implementation of our approach as an extension to an open-source Fortran analysis tool.
                                        Additional Key Words and Phrases: units-of-measure, lightweight veriﬁcation

                                        1   INTRODUCTION
                                        Scientiﬁc computing and computational models are playing an increasingly important role in re-
                                        search, industry, and policy. However, such programs are just as prone to error as other kinds of
                                        software and their reliance on complex numerical routines makes testing diﬃcult. Very simple
                                        errors, such as a ﬂipped minus sign, have had signiﬁcant impact, for example, leading to retrac-
                                        tions from premier journals (Merali 2010). Lightweight veriﬁcation techniques have the potential
                                        to help in this situation (Orchard and Rice 2014) by providing scientists with tools that have a low
                                        speciﬁcation burden and integrate with existing practices. One example of this is dimension typing
                                        in which the consistency of dimensionality or units-of-measure in equations is statically veriﬁed.
                                        Units-of-measure mistakes have led to high-stakes disasters, such as the $327 million Mars Climate
                                        Orbiter (NASA 1998) disappearing during orbital insertion. An investigation later pinned the blame
                                        on a mix-up of units-of-measure, with ground-based software sending numbers in Imperial units
                                        instead of metric units, dropping the probe into the atmosphere of Mars (Stephenson et al. 1999).
                                        This is not the only time NASA projects have struggled to convert from Imperial to metric units.
                                        Such errors are implicated in at least one other crash (Marks 2009).
                                           Checking the consistency of units-of-measure in equations, or at least the physical dimensions
                                        of calculations, is a method long employed by scientists working with pen and paper (Macagno
                                        1971). Informal discussion with scientists and examination of scientiﬁc program code has shown
                                        that units-of-measure reasoning in code does take place but usually only by hand (Orchard et al.
                                        2015). Formal units checking has not been adopted in scientiﬁc programming despite the familiar-
                                        ity of the technique and a multitude of proposed systems for automated veriﬁcation (Jiang and Su
                                        2006; Kennedy 2009; Ore et al. 2017; Snyder 2013). One potential explanation for this is the burden
                                        Authors’ addresses: Matthew Danish, Department of Computer Science and Technology, University of Cambridge, 15 JJ
                                        Thomson Ave, Cambridge, Cambridgeshire, CB3 0FD, United Kingdom, mrd45@cam.ac.uk; Dominic Orchard, School of
                                        Computing, University of Kent, Canterbury, Kent, CT2 7NF, United Kingdom, D.A.Orchard@kent.ac.uk; Andrew Rice, De-
                                        partment of Computer Science and Technology, University of Cambridge, 15 JJ Thomson Ave, Cambridge, Cambridgeshire,
                                        CB3 0FD, United Kingdom, acr31@cam.ac.uk.

                                        © 2018 Copyright held by the owner/author(s).
                                        This is the author’s version of the work. It is posted here for your personal use. Not for redistribution.
:2                                            Matthew Danish, Dominic Orchard, and Andrew Rice

of applying units annotations to existing codebases, which may be a large burden if many annota-
tions are needed (some approaches even require that every variable declaration is annotated).
   In this paper, we describe a fresh approach to statically analysing and verifying units-of-measure
which eases this burden by supporting incremental annotation, rather than requiring a whole
program change. Units annotations (speciﬁcations) are orthogonal to the type system and placed
in comments. Thus, we integrate smoothly with existing tools and compilers, without modifying
the language or relying on the existing type system. We support any system of units that the user
would like to use, not only absolute units. We also allow user-deﬁned convenient aliases for units.
   The most mainstream units-of-measure checking system is part of the programming language
F# using an extension to its type system (Kennedy 2009) that uses local reasoning based on
Kennedy’s extension to ML (Kennedy 1996) to support uniﬁcation over the equational theory of
Abelian groups. Our principal contribution is an algorithm that takes a diﬀerent approach to the
same problem, by generating and solving global constraints. We describe the core algorithm and
its implications in Section 3. We show how our global constraint system can infer polymorphic
units for underdetermined systems (Section 3.4) and that this supports both genuine polymorphic
functions (Section 3.2) and also partial annotation of programs (Section 3.6). We also show that
dividing a large program into modules and recording inferred polymorphic units at the bound-
aries partitions the global constraint problem and allows our approach to scale to large programs
(Section 3.5). We give a quantitative analysis of this scaling in Section 4.
   Our approach is based on a novel modiﬁcation of standard techniques for reducing a matrix of
constraints to Hermite Normal Form. The modiﬁed algorithm allows us to choose a single solution
for a set of polymorphic unit constraints that would otherwise form an underconstrained system
if simply viewed as a set of linear equations. We formalise our algorithm, prove termination and
prove that it produces integer solutions (Section 3.3).
   We implemented our approach as an extension of CamFort, an open-source Fortran analysis
and veriﬁcation tool (Orchard et al. 2017). However, our work is applicable beyond Fortran. We
highlight in Section 3 any Fortran-speciﬁc parts and how our approach can be more generally
applied. Section 5 details practical experiences applying our tool to real-world scientiﬁc comput-
ing models; we discuss several examples of bugs and undocumented unit conversions found by
our tool. Section 6 compares our approach against the literature, including the work of Kennedy
(1994, 2009, 1996), Jiang and Su (2006), Chen et al. (2003); Hills et al. (2008); Roşu and Chen (2003),
Contrastin et al. (2016); Orchard et al. (2015), Ore et al. (2017), Keorkunian et al. (2017) and others.


2 OVERVIEW
2.1 Annotating and Checking Units-of-Measure
A physical dimension is a measured quantity such as length, mass, time or electric charge that can
be sensibly compared among its own kind. Other dimensions are derived, such as velocity mea-
sured as a length over time. Dimensional analysis is a standard technique for checking calculations
and understanding physical equations: by tracing the steps of computation with labelled dimen-
sions one can check if the resulting dimension is as intended. Units-of-measure are the conventional
names adopted for speciﬁc amounts of each dimension. For example, the length dimension can be
expressed in terms of metres, inches, feet, Smoots (Durant 2008), among many others.
   As a simple example, consider the elementary equation of ballistics: 𝑥 (𝑡) = 12 𝑎𝑡 2 + 𝑣 0𝑡 + 𝑥 0
transcribed into Fortran in Listing 1 (left). We could annotate every variable using our comment-
based syntax, but to save work we ﬁrst ask our system to suggest a small set of variables that is
suﬃcient to determine the others, by the command camfort units-suggest (Listing 1, right).
Incremental units-of-measure verification                                                                      :3

   In this case, our tool suggests annotating a, v0 and x. We annotate those variables as shown
in Listing 2 (left) using our comment-based unit syntax (deﬁne in Figure 1). We can then invoke
the inference engine as shown in Listing 2 (right). The result is that every variable has been suc-
cessfully assigned a consistent units-of-measure. We can import these inferred units back into the
program text using a related command, units-synth, which rewrites the original source code to
a speciﬁed ﬁle but with the inferred annotations automatically inserted as comments, as a time-
saving measure. Those annotations will then serve as static speciﬁcations that can be checked any
time in the future, for reassurance, and to aid code maintenance and documentation.

2.2 Polymorphic Units Annotation
Many functions (and subroutines) can correctly operate in a generic way on any units they are
given. Listing 3 gives two simple examples of units-polymorphic functions. Function d(n) simply
doubles the value of its parameter and function square(n) squares the value of its parameter. All
of the units are annotated in this example. Variables x and t are given concrete units metre and sec.
But in the function d, the parameter n is annotated with units named ’a. This is a polymorphic units
variable that can be substituted with any concrete units as needed. We follow the ML tradition,
where polymorphic names start with a single-quote and their names are pronounced by their Greek
alphabet equivalent, e.g. 𝛼 for ’a. The same variable is used to annotate d (its result) indicating
that for every call to d the units of the function’s result are the units of any argument substituted
for n. This can be seen in the program where both x = d(x) and t = d(t) are valid lines: one
instantiating d for units metre and the other for sec. Note that this implies that the literal 2 is
inferred to be unitless (a scaling factor).
   A similar scheme of polymorphic unit annotations appears in square (Listing 3, right). For the
nested function sqr, the parameter n is unit polymorphic ’a and thus the unit of the result is ’a
squared. Variables x, y, t and s have concrete units which are coherent with instantiations of sqr.
   The importance of polymorphism as an eﬀort-saving mechanism cannot be underestimated:
without polymorphism the programmer would be forced to write redundant copies of the function

  1     program ballistics                                $ camfort units-suggest ballistics.f90
  2       implicit none
  3       real, parameter :: x0 = 0                       ballistics.f90: 3 variable declarations
  4       real, parameter :: v0 = 20                         suggested to be given a specification:
  5       real, parameter :: a = -9.8                         (5:22)    a
  6       real :: x, t                                        (4:22)    v0
  7       x = 0.5 * a * t * t + v0 * t + x0                   (6:11)    x
  8     end program ballistics
 Listing 1. Transcription of ballistics equation: un-annotated (left) with suggestion from our tool (right).


        annotation ::= speciﬁcation | alias                    polyname ::= ’name
       speciﬁcation ::= commentchar = unit u :: vars                name ::= [a-zA-Z][a-zA-Z0-9_-]*
              alias ::= commentchar = unit :: name = u               vars ::= vars, var | var
      commentchar ::= ! (𝐹𝑜𝑟𝑡𝑟𝑎𝑛90) | c (𝐹𝑜𝑟𝑡𝑟𝑎𝑛77)                   var ::= [a-zA-Z][a-zA-Z0-9_-]*
                                                   𝑧
                 u ::= 𝑈 name | 1 | 𝑢𝑢 | 𝑢/𝑢 | 𝑢                        z∈Z
             𝑈 name ::= polyname | name

                         Fig. 1. Annotation syntax: units specification and aliases
:4                                               Matthew Danish, Dominic Orchard, and Andrew Rice

     1   program ballistics
     2     implicit none                                    $ camfort units-infer ballistics.f90
     3     real, parameter :: x0 = 0                        ballistics.f90:
     4     != unit metre / sec :: v0                          3:22 unit metre :: x0
     5     real, parameter :: v0 = 20                         5:22 unit metre / sec :: v0
     6     != unit metre / sec**2 :: a                        7:22 unit metre / (sec**2) :: a
     7     real, parameter :: a = -9.8                        9:11 unit metre :: x
     8     != unit metre :: x                                 9:14 unit sec :: t
     9     real :: x, t
 10        x = 0.5 * a * t * t + v0 * t + x0
 11      end program ballistics
Listing 2. Left: transcription of the ballistics equation with suggested variables a, v0 and x annotated with
units. Right: output of units-infer mode at command-line applied to the partially annotated program, show-
ing line number and column of inferred variables, e.g., at line 3 column 22, x0 is inferred to have unit metre.

              1    program double                            1    program square
              2      != unit metre :: x                      2      != unit metre     :: x
              3      != unit sec   :: t                      3      != unit metre**2 :: y
              4      real :: x = 10, t = 15                  4      real :: x = 10, y
              5      x = d(x)                                5      != unit sec       :: t
              6      t = d(t)                                6      != unit sec**2    :: s
              7                                              7      real :: t = 5, s
              8    contains                                  8      y = sqr(x)
              9                                              9      s = sqr(t)
              10     != unit 'a :: d                         10   contains
              11     real function d(n)                      11     != unit 'a**2 :: sqr
              12       != unit 'a :: n                       12     real function sqr(n)
              13       real :: n                             13       != unit 'a :: n
              14       d = 2 * n                             14       real :: n
              15     end function d                          15       sqr = n * n
              16   end program double                        16     end function sqr
                                                             17   end program square

                              Listing 3. Annotated examples of polymorphism.


d and sqr in these examples. More fundamentally, polymorphism describes essential structure and
properties of programs. For example, Kennedy (1996) proves that functions without side-eﬀects,
such as d, that accept and return the same units can be fully described in their behaviour by a
single constant multiplier. In other words, for every single-parameter function d that accepts and
returns the same units ’a, there must exist a number 𝑘 such that the function 𝜆𝑛.𝑘·𝑛 is extensionally
equivalent to d. Similarly, for each function like square that returns ’a**2, there exists some 𝑘 such
that the function is extensionally equivalent to 𝜆𝑛.𝑘 · 𝑛 2 . This property is known as dimensional
invariance or invariance under scaling (Atkey et al. 2015).

2.3      Modular Fortran
Real programs are usually much larger than these toy examples and contain many modules. The
Fortran 90 module system provides separation of name-spaces, and allows a module to import
names from another module, possibly after renaming. Large Fortran programs are compiled as
separate units and then linked together to form executables. Many diﬀerent third-party libraries
Incremental units-of-measure verification                                                               :5

    1   module helper                             1     ! Ballistics program unit
    2     implicit none                           2
    3     != unit :: speed = metre / sec          3     program ballistics
    4     != unit metre :: x0                     4       use helper
    5     real, parameter :: x0 = 0               5       implicit none
    6                                             6       real :: t1 = 2.0, t2 = 10.0
    7     != unit speed :: v0                     7       real :: xsum = x(t1) + x(t2)
    8     real, parameter :: v0 = 20              8
    9     real, parameter :: a = -9.8             9     contains
   10   contains                                 10
   11     real function square(n)                11       real function x(t)
   12       real :: n                            12         real :: t
   13       square = n * n                       13         x = 0.5 * a * square(t) + v0 * t + x0
   14     end function square                    14       end function x
   15   end module helper                        15     end program ballistics

                     Listing 4. Helper module (left) and ballistics program (right).

   $ camfort units-infer helper.f90                   $ camfort units-compile helper.f90
   helper.f90:                                        Compiling units for 'helper.f90'
     5:22 unit metre :: x0
     5:30 unit metre / sec :: v0                      $ camfort units-infer ballistics.f90
     7:3 unit ('a)**2 :: square                       helper.fsmod: parsed precompiled file.
     8:13 unit 'a :: n                                ballistics.f90:
                                                        5:11 unit sec :: t1
                                                        5:21 unit sec :: t2
                                                        6:11 unit metre :: xsum
                                                        8:3 unit metre :: x
                                                        9:13 unit sec :: t

  Listing 5. Output showing inferred polymorphism (left) and compilation of included modules (right).


might be referenced by a given program, but the source code for those libraries may not be avail-
able.
   We extended the program analysis engine in CamFort to support multiple modules and sepa-
rate analysis of units. This mechanism may also be used to provide annotations for closed-source
libraries. An illustrative example of inference across modules is given by a modularised version of
the ballistics example in Listing 4, comprising a helper module (left) imported by the use keyword
in the ballistics program (right), bringing its variables and functions into the current scope. The
main calculation is now performed by the function x(t) which uses the polymorphic square .
   The annotations for variables x0 and v0 are given in the helper module. We also show the units
alias feature by giving the name speed to metre / sec, which acts as a simple substitution. The
function square has been introduced with no unit annotations.
Listing 5 (left) shows the output of units inference on the helper module. The user-supplied an-
notations (for x0 and v0) are output along with two newly inferred annotations for square and its
parameter n. Since square does not specialise on any particular units, a freshly-generated polymor-
phic units variable is inferred for its parameter n, which is squared in its return unit.
   Listing 5 (right) shows the output of two commands. First, we run a new mode of opera-
tion named units-compile on the helper module to produce a special precompiled ﬁle named
helper.fsmod , which contains the information necessary to import units information into other
modules. These precompiled ﬁles are detailed in Section 3.5. Then we run units-infer on the
:6                                            Matthew Danish, Dominic Orchard, and Andrew Rice

ballistics module, which automatically detects and loads the precompiled ﬁle for helper. Al-
though the ballistics module does not contain any annotations the inference is successful and
the output identiﬁes ﬁve variables that can be assigned units: t1, t2, xsum, x and t. This result brings
together several aspects of our work: separately-compiled module information (Section 3.5), in-
terprocedural knowledge (Section 3.2), intrinsic functions (Section 3.7), and polymorphic units
(Section 3.4). The solution to the units constraints is then computed by a modiﬁed Hermite Normal
Form procedure (Section 3.3).

3    INFERENCE ALGORITHM
Our core algorithm provides both inference of units in a program and checking for those vari-
ables which have been given a units speciﬁcation. The algorithm proceeds by a syntax-directed
generation of constraints (Section 3.1), an intermediate stage of polymorphic specialisation (Sec-
tion 3.2) followed by a solving procedure (Section 3.3). We explain here also further details related
to polymorphic inference (Section 3.4) and separate veriﬁcation (Section 3.5). The constraints are
attached to the abstract syntax tree and can be traced back later for error-reporting purposes.
   Our implementation applies our algorithm to Fortran code across versions 66, 77, 90, and 95.
However, since the syntax of Fortran is extensive (International Organization for Standardization
2010), we explain the algorithm on a subset — a core imperative language. Figure 2 outlines the
syntax which comprises expressions, contained in statements, contained within blocks, contained
within program units (e.g., functions, modules). We use the following syntactic conventions:
  • Variables are denoted by 𝑥; array subscripting by 𝑥 (· · ·)
  • Functions are denoted by 𝑓 (including built-in functions) and subroutines by 𝑠;
  • Module and program names are denoted by 𝑚;
  • Literals are denoted by 𝑛 or 0 to which unique identiﬁers are associated ranged over by 𝑙;
  • Unique ‘call identiﬁers’ for function and subroutine calls are denoted by 𝑖;
  • The return and parameter variables to functions and subroutines are numbered 0, 1, . . . , 𝑘;
  • Explicitly annotated parametric polymorphic units variables are denoted by 𝛼.
Additional notation is explained on-demand. All names (variables, function names) are assumed
unique following the scoping rules of the underlying language.
   In Figure 2, the ﬁrst rule in the non-terminal node 𝐵 spec captures our key notion of units annota-
tion via comments. These annotations are intended to be placed directly before the declarations of
the variables they reference. Similarly, we support annotation of function return units by placing
an annotation just before a function deﬁnition, as captured by non-terminal 𝑝𝑢𝑖 . Our system also
supports aliasing of complex monomorphic units 𝑢 to a name, implemented by simple substitution.

3.1 Units Constraints
  Deﬁnition 3.1 (Units syntax and representation). The internal representation of units types (i.e.,
not the surface syntax of Figure 1) is ranged over by 𝑢:
                                  𝑢 ::= 𝑈 | 1 | 𝑢 1 𝑢 2 | 𝑢 𝑧 | uvar
where 𝑧 ∈ Z and 𝑈 is any concrete unit, e.g., metre, sec and 1 is the ‘unitless’ type. In our imple-
mentation, the concrete syntax of units variables uvar is in the ML style of type variables: e.g., ’a.
Internally, uvar splits into a more ﬁne-grained deﬁnition:
                 uvar ::= 𝑈 [lx] | 𝑈 [fs, klx, ∗] | 𝑈 [fs, klx, 𝑖] | 𝑈 [𝛼, ∗] | 𝑈 [𝛼, 𝑖]
where lx ranges over unique identiﬁers for literals 𝑙 or variables 𝑥; fs ranges over function
and subroutine names; klx ranges over lx or function parameters 𝑘; and 𝛼 ranges over ex-
plicit polymorphic-units variables. Therefore, 𝑈 [lx] is a units variable for literals or variables.
Incremental units-of-measure verification                                                                                                                   :7


        𝑒 ::= −𝑒 | 𝑒 ⊕ 𝑒 | 𝑒 ⊘ 𝑒 | 𝑒 *𝑒 | 𝑒 /𝑒 | 𝑒 **𝑛 | 𝑛 | 𝑥 | 𝑓 (𝑒) | 𝑥 (𝑒)
             where ⊕ ∈ { +, -} , ⊘ ∈ {==, /=, <, <=, >, >= } , and 𝑛 ranges over numeric literals
      𝑠𝑡 ::= 𝑥 = 𝑒 | 𝑥 (𝑒) = 𝑒 | call 𝑠 (𝑒)
            where 𝑠 includes built-in subroutines that omit the keyword call
    𝐵 act ::= 𝑠𝑡 | if 𝑒 then 𝐵 act else 𝐵 act end if | do while (𝑒) 𝐵 act end do
   𝐵 spec ::= != unit 𝑢 :: 𝑥 | real :: 𝑥 | integer :: 𝑥 | dimension :: 𝑥 (𝑛) | external :: 𝑥
       𝐵 ::= 𝐵 spec | 𝐵 act
      𝑐𝑠 ::= contains 𝑝𝑢𝑖
    𝑝𝑢𝑖 ::= != unit 𝑢 :: 𝑓
           | != unit :: 𝑛𝑎𝑚𝑒 = 𝑢
           | function 𝑓 (𝑥) [result (𝑥)] 𝐵 spec , 𝐵 act [𝑐𝑠] | subroutine 𝑠 (𝑥) 𝐵 spec , 𝐵 act [𝑐𝑠]
     𝑝𝑢 ::= 𝑝𝑢𝑖 | module 𝑚 𝐵 spec [𝑐𝑠] | program 𝑚 𝐵 spec , 𝐵 act [𝑐𝑠]

                                                      Fig. 2. Simplified Fortran syntax

𝑈 [fs, klx, ∗] is an abstract (universally quantiﬁed) units variable for klx inside function/subroutine
fs, 𝑈 [𝛼, ∗] is an abstract units variable for polymorphic units-variable 𝛼 coming from an explicit
signature, 𝑈 [fs, klx, 𝑖] is a units variable for klx in function or subroutine fs instantiated at unique
call site 𝑖, and 𝑈 [𝛼, 𝑖] is a units variable for 𝛼 instantiated at unique call site 𝑖.

   3.1.1 Expressions. Our inference algorithm assigns units to expressions in a compositional
manner, generating a set of units equality constraints. Figure 3 gives the rules for expressions
deﬁned by judgments of the form Γ ⊢ 𝑒 : 𝑢; Δ meaning 𝑒 has units 𝑢 in context Γ and generates
a set of units equality constraints Δ, whose elements are written 𝑢 1 ∼ 𝑢 2 . Variable environments
Γ are ordered sequences mapping variables to type information (real, integer, array), their unit,
and an optional attribute external to denote any externally deﬁned (thus abstract) functions and
variables.
   The units of variables and literals depend on whether they are at the top-level or inside a function
or subroutine, where they may be polymorphic. Such contexts are classiﬁed by a predicate:

 polycontext( 𝑓 , Γ)      𝑥 ∈Γ                          ¬polycontext( 𝑓 , Γ)         𝑥 ∈Γ                   Γ ⊢ 𝑒 1 : 𝑢 1 ; Δ1 Γ ⊢ 𝑒 2 : 𝑢 2 ; Δ2
                                     polyvar ex                                               var ex                                                  ⊕ex
     Γ ⊢ 𝑥 : 𝑈 [ 𝑓 , 𝑥, ∗]; ·                                    Γ ⊢ 𝑥 : 𝑈 [𝑥 ]; ·                          Γ ⊢ 𝑒 1 ⊕ 𝑒 2 : 𝑢 1 ; Δ1 , Δ2 , 𝑢 1 ∼ 𝑢 2

Γ ⊢ 𝑒 1 : 𝑢 1 ; Δ1 Γ ⊢ 𝑒 2 : 𝑢 2 ; Δ2               Γ ⊢ 𝑒 1 : 𝑢 1 ; Δ1 Γ ⊢ 𝑒 2 : 𝑢 2 ; Δ2                   Γ ⊢ 𝑒 1 : 𝑢 1 ; Δ1     Γ ⊢ 𝑒 2 : 𝑢 2 ; Δ2
                                      ⊘ex                                                 mul ex                                                        div ex
Γ ⊢ 𝑒1 ⊘ 𝑒2 : 1; Δ1, Δ2, 𝑢 1 ∼ 𝑢 2                      Γ ⊢ 𝑒1 *𝑒2 : 𝑢 1𝑢 2 ; Δ1, Δ2                              Γ ⊢ 𝑒1 /𝑒2 : 𝑢 1𝑢 2−1 ; Δ1 , Δ2

     Γ ⊢ 𝑒 : 𝑢; Δ                       Γ ⊢ 𝑒 : 𝑢; Δ 𝑛 ∈ Z                           Γ ⊢ 𝑥 : 𝑢; ·    isarray(𝑥, Γ) Γ ⊢ 𝑒 : 1; Δ
                  unary ex                                  power ex                                                            subscript ex
    Γ ⊢ −𝑒 : 𝑢; Δ                        Γ ⊢ 𝑒**𝑛 : 𝑢 𝑛 ; Δ                                         Γ ⊢ 𝑥 (𝑒 ) : 𝑢; Δ
                 𝑓 : external ∉ Γ freshid(𝑖 ) isfunction( 𝑓 , Γ) Γ ⊢ 𝑒 : 𝑢; Δ where 𝑢 = 𝑢 1 , . . . , 𝑢𝑘
                                                                                                                 fcall ex
                              Γ ⊢ 𝑓 (𝑒 ) : 𝑈 [ 𝑓 , 0, 𝑖 ]; Δ, 𝑢 1 ∼ 𝑈 [ 𝑓 , 1, 𝑖 ] , . . . , 𝑢𝑘 ∼ 𝑈 [ 𝑓 , 𝑘, 𝑖 ]
                       𝑓 : external ∈ Γ         isfunction( 𝑓 , Γ)       Γ ⊢ 𝑒 : 𝑢; Δ     where 𝑢 = 𝑢 1 , . . . , 𝑢𝑘
                                                                                                                         fcallextex
                                Γ ⊢ 𝑓 (𝑒 ) : 𝑈 [ 𝑓 , 0, 0]; Δ, 𝑢 1 ∼ 𝑈 [ 𝑓 , 1, 0] , . . . , 𝑢𝑘 ∼ 𝑈 [ 𝑓 , 𝑘, 0]
                       Γ ⊢ 𝑒1 : 𝑢 1 ; Δ1 Γ ⊢ 𝑒2 : 𝑢 2 ; Δ2 · · · Γ ⊢ 𝑒𝑘 : 𝑢𝑘 ; Δ𝑘 Δ = Δ1, Δ2, . . . , Δ𝑘
                                                                                                             list ex
                              Γ ⊢ 𝑒 : 𝑢; Δ     where 𝑒 = 𝑒1 , 𝑒2 , . . . , 𝑒𝑘 and 𝑢 = 𝑢 1 , 𝑢 2 , . . . , 𝑢𝑘

                                 Fig. 3. Rules for expressions (apart from literals, see Figure 4)
:8                                                    Matthew Danish, Dominic Orchard, and Andrew Rice

polycontext( 𝑓 , Γ) freshid(𝑙 )            polycontext( 𝑓 , Γ) 𝑛 ≠ 0            ¬polycontext( 𝑓 , Γ) freshid(𝑙 )
                                polyzeroex                           polylit ex                                  literal ex
      Γ ⊢ 0 : 𝑈 [ 𝑓 , 𝑙, ∗]; ·                    Γ ⊢ 𝑛 : 1; ·                          Γ ⊢ 𝑛 : 𝑈 [𝑙 ]; ·


                                         Fig. 4. Rules for literal expressions


     Deﬁnition 3.2. Given a function or subroutine name fs, then Γ is a polymorphic context for fs if:
                polycontext(fs, Γ) :=         ∃Γ1, Γ2, 𝑥 . Γ ≡ (Γ1, 𝑥 : 𝑈 [fs, 𝑥, ∗] , Γ2 ) ∧
                                                    ∀𝑥 ′, fs′ . 𝑥 ′ : 𝑈 [fs′ , 𝑥 ′ , ∗] ∈ Γ2 =⇒ fs = fs ′
That is, fs is the most recently enclosing function or subroutine in the context if there is a parameter
𝑥 in the environment associated with fs, and there is no other function or subroutine fs′ ahead of
it.
For example, polycontext is used in polyvar ex (Figure 3) to generate units for a variable 𝑥 in a func-
tion 𝑓 as the abstract units variable 𝑈 [𝑓 , 𝑥, ∗]. By contrast, variables in a monomorphic setting are
assigned 𝑈 [𝑥], which cannot later be instantiated. The rest of the expression rules generate vari-
ous constraints: compound units for multiplication and division (mul ex , div ex ), equality constraints
for addition (⊕ ex ) and boolean comparators (⊘ex ), preservation of units for negation (unary ex ), and
exponentiation of units by integer constants (power ex ). Function calls are by fcall ex and fcallext ex .
   Figure 3 uses some further helper predicates on environments and for fresh identiﬁer generation:
• freshid(𝑖) asserts that 𝑖 is a fresh identiﬁer in this derivation (any another instance of freshid( 𝑗 )
   is guaranteed to satisfy 𝑖 ≠ 𝑗 );
• isfunction(𝑓 , Γ) and isarray(𝑥, Γ) classify 𝑓 and 𝑥 based on their (normal) types in Γ.
   3.1.2 Literals. The rules for literals bear some explanation and are in the separate Figure 4.
There are three relevant rules that encode the handling of literal values recommended by Kennedy
(1996). polyzeroex provides a ‘polymorphic zero’ when used in a context where polymorphism is
allowed. polylit ex requires all other literal values found in a polymorphic context to be unitless.
Outside of a polymorphic context, literal ex generates a fresh units variable to be solved; this diﬀers
to Kennedy’s approach which we explain in more detail in Section 6.
   Since zero is the additive identity, and addition requires that all terms have the same units,
the only literal value that can act polymorphically is zero. If any other literal value could have
polymorphic units then a simple scalar multiplication would unify with any units, rendering the
checking procedure useless. For example, if nonzero polymorphic literals were allowed and we
modiﬁed the code in Listing 1 to be 0.5 * a * t + v0 * t, then it would pass the checker because
it would assume that the literal value 0.5 could be given units sec.
   Still, we need a way for literals to be given units within functions and subroutines. In the F#
units-of-measure extension you must annotate literals directly, for example:
     let w = 2.0<kg> + 3.5<kg>
However we avoid direct annotation because it violates our incremental principle of harmlessness:
to maintain usability of existing compilers and tools. We could instead create inline comment-
based annotations specifying the units, but this is cumbersome, not supported by all Fortran
compilers and potentially confusing. We found that the most practical way of assigning units to
nonzero literals is to carve out an exception for the case of assigning a literal value to a monomor-
phically annotated variable. In that case, no constraint is generated. This condition is expressed by
the rule assignliteral st in Figure 5 where isMonomorphic(𝑢) is true iﬀ 𝑢 does not have any paramet-
ric polymorphic units variables within it. When x is a Fortran variable annotated by monomorphic
units, simple assignment statements such as x = 2.0 are allowed, but any compound expression
Incremental units-of-measure verification                                                                 :9

involving nonzero literals falls back on polylit ex . This particular design choice has the virtue of
catching the common case of declaring constants (e.g. real :: x = 2.0) as well as discouraging the
poor practice (Martin 2009) of scattering ‘magic numbers’ throughout code (e.g. x = y - 9.381).
   3.1.3 Casting. The literal exception allows us to create ‘casting’ values that help convert be-
tween concrete units. For example, you can declare != unit cm/in :: inchesToCm followed by
real :: inchesToCm = 2.54. Abuse of casting can allow you to sidestep the units system but it
is a practical feature that cannot be avoided in real work, and this way the conversion factors are
named and documented rather than being scattered around the code. We would argue that better
practice would be to isolate all of the necessary conversion factors in a common module shared by
the entire program (or better yet, a library we may distribute along with our work). Conversion
factor literals can only be given monomorphic units. Section 3.7 discusses explicit, direct unit casts.
   3.1.4 Monomorphism restriction for nonzero literals. The restriction of the literal exception to
monomorphic units is important for soundness. Otherwise it would be possible to write programs
that circumvent the relationships expressed through polymorphism. For example,
                                                                           Í         a function with
units-polymorphic variable x could simply run a loop that computes 𝑥 2 = 𝑥1 𝑥 (see Listing 8). The
units inference process would simply interpret that as a series of additions that return the exact
same units as provided, rather than the square of those units. More generally, allowing the user to
annotate nonzero literals with polymorphic units would break the theorem of dimensional invari-
ance (Atkey et al. 2015; Kennedy 1996), which states that the behaviour of dimensionally-correct
equations is independent of the speciﬁc units-of-measure used. For a counterexample, suppose that
we were actually allowed to write a units-polymorphic function with a polymorphic literal, like
𝑓 (𝑥) = 𝑥 + 2. Then it would not satisfy its dimensional invariance theorem that 𝑓 (𝑘 · 𝑥) = 𝑘 · 𝑓 (𝑥)
for any 𝑘. To put some numbers on it, if we take 𝑥 = 1 inch then we ﬁnd that 𝑓 (𝑥) = 3 inches. How-
ever with 𝑘 = 2.54 cm/inch then 𝑓 (2.54 · 𝑥) = 4.54 cm, which is not equal to 2.54 · 𝑓 (𝑥) = 7.62 cm.
   3.1.5 Function calls. There are two rules for function calls, fcall ex and fcallext ex . The reason
is because Fortran supports passing functions as parameters, but does not have the concept
of ‘function types’ to properly describe their behaviour. Instead, such function parameters are
simply declared external . We support polymorphic functions but not arbitrary rank polymor-
phism (Jones et al. 2007). That would allow a function parameter to be instantiated with diﬀerent
units at each call-site, but would easily generate inconsistencies under the rules of our system.
To avoid this problem we collapse all external function parameter calls to call id 0 (chosen arbi-
trarily). That permits only a single polymorphic instance to be created, which is shared by calls
to that function parameter within the enclosing function body. Future work is to allow explicit
annotations on Fortran interface blocks to allow arbitrary rank polymorphism.
  3.1.6 Statements and Blocks. Statements (in the usual imperative sense) are typed by judgments
that have an incoming context Γ, set of constraints Δ and an outgoing constraint set Δ′ :
                                             Γ; Δ ⊢ 𝑠𝑡 { Δ′
The rules are given in Figure 5.
  Blocks include syntax such as conditionals or loops, which have a similar form to statements
and are typed by judgments of the form:
                                            Γ; Δ ⊢ 𝐵 { Γ ′ ; Δ′
is a relation between (Γ, Δ, 𝐵) and the subsequently produced context and constraint set (Γ ′, Δ′ )
(Figure 6). Blocks can include variable-type declarations (dimdecl bl , extdecl bl , typedecl bl ), and thus
they generate a new typing context Γ ′ .
:10                                                  Matthew Danish, Dominic Orchard, and Andrew Rice

   The rules for annotpoly bl and annotmono bl in Figure 6 are key to connecting the generated
units constraints with annotations of concrete units. The annotmono bl rule introduces concrete
units U for variable 𝑥 and thus generates a constraint 𝑈 [𝑥] ∼ U; annotpoly bl is similar but in a
polymorphic context hence 𝑥 may be units-polymorphic and so the generated constraint applies
the units variable representation 𝑈 [𝑓 , 𝑥, ∗] ∼ U.
   Rules for conditionals (if bl ) and loops (whilebl ) recursively apply expression typing and block-
typing rules, composing generated constraint and context sets sequentially. Thus, we perform a
‘may analysis’: we take the conjunction of constraints from all control-ﬂow paths, similar to a
standard type inference.

   3.1.7 Program Units. We introduce the notion of a template 𝑇 which maps function and sub-
routine names to their associated constraints, in order to support polymorphism (Section 3.2) and
to be used in precompiled (preveriﬁed) ﬁles (Section 3.5). Program units are typed in Figure 7 by
judgments of the following form:
                                                  Γ;𝑇 ⊢ 𝑝𝑢 { 𝑇 ′

is a relation between (Γ,𝑇 , 𝑝𝑢) and the subsequently produced template 𝑇 ′ .
   Program units are grouped into ﬁles which can be modules or top-level programs. Module-
maps 𝑀 map module names to tuples (Δ,𝑇 ) where Δ contains constraints associated with module
variables and 𝑇 are templates. A ﬁnal judgment form coalesces information from multiple modules:

                                                  𝑀 ⊢ 𝑝𝑢 { 𝑀 ′

is a relation between (𝑀, 𝑝𝑢) and the subsequently produced module-map 𝑀 ′ .

3.2 Interprocedural Polymorphic Instantiation
Once the constraints within all program units have been gathered and stored in a template ta-
ble we begin the process of instantiating polymorphic function or subroutine templates as con-
crete constraints. We identify all of the uses of a polymorphic function or subroutine fs by ﬁnding
pairs (fs, 𝑖) where 𝑖 represents the call-ids associated with function or subroutine calls contained
within the constraints. We call these pairs ‘instances’ and for each instance we invoke a recursive
function substInstance to look up the associated function or subroutine template and invoke
instantiate(𝑢, 𝑖) (Deﬁnition 3.3) on all of the abstract units 𝑢 within it.




                         freshid(𝑖) Γ ⊢ 𝑒 : 𝑢; Δ′ where 𝑢 = 𝑢 1, 𝑢 2, . . . , 𝑢𝑘
                                                                                             call st
                     Γ; Δ ⊢ call 𝑠 (𝑒) { Δ, Δ′, 𝑢 1 ∼ 𝑈 [𝑠, 1, 𝑖] , . . . , 𝑢𝑘 ∼ 𝑈 [𝑠, 𝑘, 𝑖]
           𝑛≠0     Γ ⊢ 𝑥 : 𝑈 [𝑥]; · ∀𝑢. (𝑈 [𝑥] ∼ 𝑢 ∈ Δ =⇒ isMonomorphic(𝑢))
                                                                            assignliteral st
                                     Γ; Δ ⊢ 𝑥 = 𝑛 { Δ
                                                          Γ ⊢ 𝑥 : 𝑢 1 ; · Γ ⊢ 𝑒 : 𝑢 2 ; Δ2 𝑒 ≠ 𝑛
                                   assignzerost                                                  assignst
           Γ; Δ ⊢ 𝑥 = 0 { Δ                                 Γ; Δ ⊢ 𝑥 = 𝑒 { Δ, Δ2, 𝑢 1 ∼ 𝑢 2

                 Γ ⊢ 𝑥 : 𝑢1; ·      Γ ⊢ 𝑒 : 𝑢 2 ; Δ2 (𝑒 ≠ 𝑛 ∨ 𝑒 = 0) Γ ⊢ 𝑒 : 1; Δ3
                                                                                   arrayassignst
                                 Γ; Δ ⊢ 𝑥 (𝑒) = 𝑒 { Δ, Δ2, Δ3, 𝑢 1 ∼ 𝑢 2

                                            Fig. 5. Rules for statements
Incremental units-of-measure verification                                                                                                    :11

                   Γ0 ; Δ0 ⊢ 𝐵 1 { Γ1 ; Δ1     Γ1 ; Δ1 ⊢ 𝐵 2 { Γ2 ; Δ2         ···   Γ𝑘 −1 ; Δ𝑘 −1 ⊢ 𝐵𝑘 { Γ𝑘 ; Δ𝑘
                                                                                                                    list bl
                                   Γ0 ; Δ0 ⊢ 𝐵 { Γ𝑘 ; Δ𝑘         where 𝐵 = 𝐵 1 , 𝐵 2 , . . . , 𝐵𝑘
               polycontext( 𝑓 , Γ)                                       ¬polycontext(𝑓 , Γ)
                                                 annotpoly bl                                          annotmono bl
 Γ; Δ ⊢ != unit U :: x { Γ; Δ, 𝑈 [ 𝑓 , 𝑥, ∗] ∼ U              Γ; Δ ⊢ != unit U :: x { Γ; Δ, 𝑈 [𝑥 ] ∼ U
  Γ; Δ ⊢ 𝑠𝑡 { Δ′
                   statement bl                                                                                                  typedecl bl
 Γ; Δ ⊢ 𝑠𝑡 { Γ; Δ′                         Γ; Δ ⊢ 𝑡 𝑦𝑝𝑒 :: 𝑥 { Γ, 𝑥 : 𝑡 𝑦𝑝𝑒; Δ             where 𝑡 𝑦𝑝𝑒 ∈ {real, integer}
                                                          dimdecl bl                                                            extdecl bl
    Γ; Δ ⊢ dimension :: 𝑥 (𝑛) { Γ, 𝑥 : array; Δ                                Γ; Δ ⊢ external :: 𝑥 { Γ, 𝑥 : external; Δ
Γ0 ⊢ 𝑒 : 1; Δ𝑒   Γ0 ; Δ0 ⊢ 𝐵 1 { Γ1 ; Δ1     Γ0 ; Δ1 ⊢ 𝐵 2 { Γ2 ; Δ2                  Γ0 ⊢ 𝑒 : 𝑢; Δ1   Γ0 ; Δ0 ⊢ 𝐵 { Γ1 ; Δ2
                                                                       if bl                                                          while bl
    Γ0 ; Δ0 ⊢ if 𝑒 then 𝐵 1 else 𝐵 2 end if { Γ0 ; Δ2 , Δ𝑒                      Γ0 ; Δ0 ⊢ do while (𝑒) 𝐵 end do { Γ0 ; Δ1, Δ2

                                                      Fig. 6. Rules for blocks


         ·; · ⊢ 𝐵 spec { Γ0 ; Δ let Γ1 = Γ0 , 𝑥 0 : 𝑈 [𝑓 , 𝑥 0 , ∗] , . . . , 𝑥𝑘 : 𝑈 [𝑓 , 𝑥𝑘 , ∗] Γ1 ;𝑇 ⊢ 𝑝𝑢 { 𝑇 ′
               Γ1 ; Δ ⊢ 𝐵 act { Γ ′ ; Δ′  let Δ′′ = Γ ′ (𝑥 0 ) ∼ 𝑈 [𝑓 , 0, ∗] , . . . , Γ ′ (𝑥𝑘 ) ∼ 𝑈 [𝑓 , 𝑘, ∗]
                                                                                                                               funres pu
           Γ;𝑇 ⊢ function 𝑓 (𝑥 1 , . . . , 𝑥𝑘 ) result (𝑥 0 ) 𝐵 spec , 𝐵 act contains 𝑝𝑢 { 𝑇 ′ , (𝑓 ↦→ Δ′, Δ′′ )

                     Γ;𝑇 ⊢ function 𝑓 (𝑥 1 , . . . , 𝑥𝑘 ) result (𝑓 ) 𝐵 spec , 𝐵 act contains 𝑝𝑢 { 𝑇 ′
                                                                                                                     funpu
                            Γ;𝑇 ⊢ function 𝑓 (𝑥 1 , . . . , 𝑥𝑘 ) 𝐵 spec , 𝐵 act contains 𝑝𝑢 { 𝑇 ′

          ·; · ⊢ 𝐵 spec { Γ0 ; Δ let Γ1 = Γ0 , 𝑥 1 : 𝑈 [𝑠, 𝑥 1 , ∗] , . . . , 𝑥𝑘 : 𝑈 [𝑠, 𝑥𝑘 , ∗] Γ1 ;𝑇 ⊢ 𝑝𝑢 { 𝑇 ′
                Γ1 ; Δ ⊢ 𝐵 act { Γ ′ ; Δ′  let Δ′′ = Γ ′ (𝑥 1 ) ∼ 𝑈 [𝑠, 1, ∗] , . . . , Γ ′ (𝑥𝑘 ) ∼ 𝑈 [𝑠, 𝑘, ∗]
                                                                                                                               subr pu
                  Γ;𝑇 ⊢ subroutine 𝑠 (𝑥 1 , . . . , 𝑥𝑘 ) 𝐵 spec , 𝐵 act contains 𝑝𝑢 { 𝑇 ′ , (𝑠 ↦→ Δ′, Δ′′ )

Γ;𝑇0 ⊢ 𝑝𝑢 1 { 𝑇1 · · · Γ;𝑇𝑘 −1 ⊢ 𝑝𝑢𝑘 { 𝑇𝑘                ·; · ⊢ 𝐵 spec { Γ; Δ Γ; · ⊢ 𝑝𝑢 { 𝑇
                                          list pu                                                  modulepu
         Γ;𝑇0 ⊢ 𝑝𝑢 1, . . . , 𝑝𝑢𝑘 { 𝑇𝑘            𝑀 ⊢ module 𝑚 𝐵 spec contains 𝑝𝑢 { 𝑀, 𝑚 ↦→ (Δ,𝑇 )

                          ·; · ⊢ 𝐵 spec { Γ; Δ        Γ; · ⊢ 𝑝𝑢 { 𝑇            Γ; Δ ⊢ 𝐵 act { Γ ′ ; Δ′
                                                                                                          programpu
                         𝑀 ⊢ program 𝑚 𝐵 spec , 𝐵 act contains 𝑝𝑢 { 𝑀, 𝑚 ↦→ (Δ′,𝑇 ′ )

                                                 Fig. 7. Rules for program units


  Deﬁnition 3.3 (Instantiation). For units 𝑢 and a call-site identiﬁer 𝑖 then instantiate(𝑢, 𝑖) is de-
ﬁned:
                                          
                                          𝑈 [fs, kxl, 𝑖] if 𝑢 = 𝑈 [fs, kxl, ∗]
                                          
                                          
                                          
                       instantiate(𝑢, 𝑖) = 𝑈 [𝛼, 𝑖]       if 𝑢 = 𝑈 [𝛼, ∗]
                                          
                                          
                                          𝑢              otherwise
                                          
   We distinguish ourselves from Osprey (Jiang and Su 2006) by supporting units-polymorphic
functions at all levels of the call-graph, not only the leaves. This is accomplished with a call-
id remap function that works on the given template prior to instantiation and rewrites all uses
of polymorphism within the template to have a fresh call-id speciﬁc to this particular call. The
substInstance function recurses down the call-graph performing both call-id remap and instan-
tiation of abstract units. We have chosen to stop the recursion when a cycle in the call-graph is
detected. This means we support recursive units-polymorphic functions in Fortran programs but
more complicated ‘units-polymorphic recursion’ (Mycroft 1984) is not supported: with recursive
calls, polymorphic units are instantiated at the ﬁrst level and must remain the same throughout
:12                                                             Matthew Danish, Dominic Orchard, and Andrew Rice


                                                   È𝑢 1 ∼ 𝑢 2 É ↦→ È𝑢 1 É = È𝑢 2 É
        È𝑢 1𝑢 2 É ↦→ È𝑢 1 É + È𝑢 2 É                     È𝑢 𝑧1 É ↦→ 𝑧 È𝑢 1 É                             È1É ↦→ 0
           È𝑈 É ↦→ B[𝑈 ]                           È𝑈 [𝛼, ∗]É ↦→ B[𝛼]                         È𝑈 [𝑓 𝑠, · · ·]É ↦→ C[𝑓 𝑠, · · ·]

  Fig. 8. Conversion of constraints to linear equations, where È−É is overloaded on constraints and units


                            given constraints of the form: 𝑐 1 C1 + · · · + 𝑐𝑚 C𝑚 = 𝑏 1 B1 + · · · + 𝑏𝑛 B𝑛
           where each unknown units variable C[· · ·] has been assigned a column 𝐶 𝑗 for 0 < 𝑗 ≤ 𝑚
                       and each base unit B[· · ·] has been assigned a column 𝐵 𝑗 for 0 < 𝑗 ≤ 𝑛
                                   C1   ···   C𝑚   B1   ···    B𝑛                               C1      ···   C𝑚   B1   ···   B𝑛
                               "                                    #          constraint1    𝑐′ = 1 · · · 𝑐′ 𝑏′ · · · 𝑏′ 
               constraint1         𝑐 1 · · · 𝑐𝑚 𝑏 1 · · · 𝑏𝑛                                  1             𝑚   1       𝑛 
                                                                                              0                           
      𝐴aug =           ..           .. . .    .  .. . .    .            𝐻=                    .                           
                        .            .     . ..   .     . ..                           ..     .       ..    .
                                                                                                             .  .
                                                                                                                .  ..    .
                                                                                                                         . 
                                                                                        .     .          . .   .     . . 
                                                                                                                          
                                                              Fig. 9. Matrices


the recursion, trading a small amount of expressiveness for better tractability. This is a common
choice with type systems and Kennedy (1996) also made the same decision in his work.

3.3     Reduction to Linear Diophantine Equations
We adopt and customise the method discussed by Wand and O’Keefe (1991) and further by
Jiang and Su (2006). First we extract constraints by analysing the structure of program code,
as described by Section 3.1, and then we convert the constraints to a set of linear Diophantine
equations relating units variables that can be solved simultaneously. Figure 8 shows the rules that
translate constraints and units into linear equations with terms corresponding to both unknown
units variables C[· · ·] and known base units B[· · ·]. This conversion to linear equation, and the
subsequent solving procedure, deals with the equational theory of units-of-measure (which form
an Abelian group).
   Once all constraints have been translated into linear equations, they are set up into the stan-
dard 𝐴𝑋 = 𝐵 matrix equation form. For the purposes of Gaussian elimination-style solvers this
is represented as an augmented matrix 𝐴aug = [𝐶𝐵] as shown in Figure 9. Each of the unknown
terms C[· · ·] corresponds to a column in the matrix 𝐶 on the left-hand side of 𝐴aug . Each of the
known base units B[· · ·] corresponds to a column in the matrix 𝐵 on the right-hand side of 𝐴aug .
The linear equations are transcribed into rows of 𝐴aug by taking the co-eﬃcients of each term and
placing them into the appropriate matrix under the corresponding column for that term.
   The Rouché–Capelli theorem (Shafarevich and Remizov 2012) states that if the rank of the co-
eﬃcient matrix 𝐴 is not equal to the rank of the augmented matrix 𝐴aug then the system of linear
equations is inconsistent, meaning a units error is detected and reported to the user. Otherwise,
the standard approach for solving the equations encoded in 𝐴aug obtains the unique Hermite Nor-
mal Form (HNF) 𝐻 , an upper-triangular matrix from which the answers can be easily extracted by
back-substitution (Cohen 2013).
  Deﬁnition 3.4 (Hermite Normal Form). Given a matrix 𝑀, the Hermite Normal Form (HNF) 𝐻 is
an integer matrix with the following properties:
 • The leading co-eﬃcient in a row, also known as the pivot, is the ﬁrst nonzero positive integer
    in the row.
Incremental units-of-measure verification                                                               :13

                        𝑐𝑜𝑛𝑠𝑡𝑟𝑎𝑖𝑛𝑡𝑠 = {v ∼ y,       w ∼ y**4,      y**4 ∼ x**6 }
                                  𝑣 𝑤 𝑥    𝑦    𝛼           𝑣 𝑤 𝑥 𝑦      𝛼              𝑣 𝑤 𝑥 𝑦     𝛼
           𝑣 𝑤 𝑥    𝑦
                            1 0 0 −1 0       1 0 0 3 −12           1 0 0 0 −3 
           1 0 0 −1                                                           
      HNF            mod  0 1 0 −4 0  HNF  0 1 0 0 −12  Z RREF  0 1 0 0 −12 
                                                          
· · · ⇒  0 1 0 −4  ⇒               ⇒    0 0 1 0 −2     ⇒      0 0 1 0 −2 
           0 0 6 −4       0 0 6 −4 0                                          
                          0 0 1 0 −2       0 0 0 4 −12           0 0 0 1 −3 
                                                                                
                 Fig. 10. Example operation of modified Hermite Normal Form algorithm


 • If 𝑗 is the column of the pivot in row 𝑖 and 𝑗 ′ is the column of the pivot in row 𝑖 + 1 then 𝑗 < 𝑗 ′ .
 • If there is a pivot at row 𝑖 and column 𝑗 then, for all rows 𝑖 ′ in the matrix:
   – if 𝑖 ′ < 𝑖 then 0 ≤ 𝐻 (𝑖 ′, 𝑗) < 𝐻 (𝑖, 𝑗)
   – if 𝑖 ′ > 𝑖 then 𝐻 (𝑖 ′, 𝑗) = 0
There are many well-explored algorithms for ﬁnding the HNF and it is a unique form that can be
computed for any integer matrix (Cohen 2013).
    Figure 10 contains an example set of constraints (generated from code within a polymorphic
context without any monomorphic units deﬁned) encoded into a matrix and stepped through our
modiﬁed HNF algorithm. For brevity, the ﬁrst matrix 𝐻 is shown already in HNF but any other
arrangement of the rows would have produced this canonical form. In this ﬁrst HNF matrix, the
problem with simple HNF can be seen: we started with no units and we still have no units. Plus, a
naïve reading of the solution would suggest that 1.5𝑥 = 𝑦 since 6𝑥 = 4𝑦 (last row). Therefore, the
two tasks for our algorithm are: derive a polymorphic units variable and ﬁnd integer solutions for
all the unknown units. As we can see, simple HNF will ﬁnd integer solutions but they would be
expressed in a way that boils down to 3𝑥 = 2𝑦, while what we want looks more like 𝑥 = 2𝛼 and
𝑦 = 3𝛼. Therefore, modiﬁed HNF needs to identify the situation, derive this polymorphic units
variable 𝛼 that 𝑥 and 𝑦 have in common and solve for the two in lowest integer terms.
    Our algorithm operates on the HNF 𝐻 of the input matrix. Each time we detect a pivot at coordi-
nates 𝑖, 𝑗 that cannot be scaled down to 1, we take a step to modify matrix 𝐻 with a new constraint
𝑖 ′ at the bottom and a new column 𝑗 ′ on the right: 𝐻 (𝑖 ′ , 𝑗) = 1 and 𝐻 (𝑖 ′ , 𝑗 ′ ) = −𝑑 where
                                  𝑎
                      𝑑=                      𝑎 = min ′ { |𝐻 (𝑖, 𝑘)| | 𝐻 (𝑖, 𝑘) ≠ 0 }
                           gcd {𝐻 (𝑖, 𝑗) , 𝑎}    𝑗 <𝑘 ≤ 𝑗

This is shown in the Figure 10 example where in the second matrix the last row and column have
been added in this fashion. We then ﬁnd the HNF of the modiﬁed matrix, producing the third
matrix in the example. Applying two integer elementary row operations produces the ﬁnal matrix
in reduced row echelon form, from which the solution can be easily read: 𝑣 = 3𝛼, 𝑤 = 12𝛼, 𝑥 =
2𝛼, 𝑦 = 3𝛼 where 𝛼 is an inferred polymorphic units variable represented by the new column.
   The general modiﬁed-HNF procedure is shown in pseudocode in Listing 6. The loop body is
repeated until no new columns are generated.
   Lemma 3.5. For every pivot 𝑝𝑖,𝑗 detected that does not divide every integer in its row, the resulting
matrix after the loop body completes will have two additional pivots equal to 1. One of them will be
at column 𝑗 and one will be at some column greater than 𝑗 .
   Proof. The algorithm has generated a new row 𝑖 ′ with a 1 in the 𝑗 column and the value 𝑑 in
the new 𝑗 ′ column.                                                                              ′
   Elementary row subtraction of the two rows with  the scaling factor 𝑝𝑖,𝑗 − 1 applied to row 𝑖
leaves behind a leading 1 and a trailing 𝑑 𝑝𝑖,𝑗 − 1 in row 𝑖.
:14                                              Matthew Danish, Dominic Orchard, and Andrew Rice

input: matrix 𝑀
let 𝑃𝑟𝑒𝑠𝑢𝑙𝑡 be an empty list
  loop (0) let 𝐻 1 = HNF(𝑀) and 𝑃 be an empty list.
       (1) for each row 𝑖 of 𝐻 1 below rank(𝐻 1 )
            • let 𝑝𝑖,𝑗 be the pivot at row 𝑖, column 𝑗
            • if 𝑝𝑖,𝑗 > 1 and it divides every integer in row 𝑖 then apply that elementary row
              scaling operation to matrix 𝐻 1
            • else if 𝑝𝑖,𝑗 > 1 but it does not divide every integer in the row, then add it to the list 𝑃.
       (2) let 𝐻 2 be a copy of 𝐻 1 but only taking rank(𝐻 1 ) rows.
       (3) for each 𝑝𝑖,𝑗 in list 𝑃
            • enlarge 𝐻 2 by one row at index 𝑖 ′ and one column at index 𝑗 ′ , with default values
              being zero.
            • let 𝑎 = min{ |𝐻(𝑖, 𝑘)| | 𝑘 ∈ {𝑗 + 1, . . . , 𝑗 ′ } ∧ 𝐻 (𝑖, 𝑘) ≠ 0 }
            • let 𝑑 = 𝑎/gcd 𝑝𝑖,𝑗 , 𝑎
            • set 𝐻 (𝑖 ′, 𝑗) := 1 and 𝐻 (𝑖 ′, 𝑗 ′ ) := −𝑑
       (4) let 𝐻 3 = HNF(𝐻 2 )
       (5) apply integer elementary row scaling and addition operations to 𝐻 3 to change as many
            pivots as possible to 1 with zeros above and below them in the column
       (6) let 𝐻 4 be a copy of 𝐻 3 but only taking rank(𝐻 3 ) rows.
       (7) add members of 𝑃 to 𝑃𝑟𝑒𝑠𝑢𝑙𝑡
       (8) set 𝑀 := 𝐻 4
repeat while |𝑃 | > 0
output: 𝑀 and 𝑃𝑟𝑒𝑠𝑢𝑙𝑡

                             Listing 6. Pseudocode for modified-HNF procedure


   Let 𝑎 be the minimum nonzero absolute value found in row 𝑖 to the right of the pivot, in column
𝑗𝑎 > 𝑗 .
   Since 𝑖, 𝑗 is a pivot with value 1, we must subtract row 𝑖 from row 𝑖 ′ to cancel the value of 1 we
wrote into 𝑖 ′, 𝑗 . This leaves a value of −𝑎 at (𝑖 ′, 𝑗𝑎 ) and a value of −𝑑𝑝𝑖,𝑗 at (𝑖 ′, 𝑗 ′ ).
   We can now obtain the value 1 in row 𝑖 ′ and column 𝑗𝑎 by applying elementary row scaling with
a factor of −𝑎 −1 . In order for this to maintain integer results the value of 𝑑𝑝𝑖,𝑗 must          be divisible
by 𝑎. Therefore when writing the value of 𝑑 into the matrix we selected 𝑑 = 𝑎/gcd 𝑝𝑖,𝑗 , 𝑎 as the
minimum such integer value.                                                                                   
  Theorem 3.6. For any matrix given as input, the modiﬁed-HNF procedure terminates.
   Proof. Let |𝑃 | be equal to the number of pivots qualifying under Lemma 3.5 and let 𝑝𝑖,𝑗 be the
right-most such pivot. By the lemma, there will be pivots at column 𝑗 and some column 𝑗 ′ > 𝑗 ,
both equal to 1 in the next iteration. The matrix then will have |𝑃 | more columns but at least |𝑃 | + 1
pivots will have been made equal to 1. This reduces the pool of potential Lemma 3.5 candidates by
at least one on each iteration, until all are exhausted.                                              
   Almost all real-world examples tried so far have been solved in just a few iterations. The worst
case occurs when there are constraints between a set of variables raised to a sequence of strongly
                            𝑝              𝑝
co-prime exponents, e.g., 𝑥 1 1 + · · · + 𝑥𝑘 𝑘 where 𝑝 1, . . . , 𝑝𝑘 are distinct prime numbers. This type of
program is unlikely to be found in the wild, since it lacks any sensible physical interpretation. We
artiﬁcially generated an example containing terms raised to the ﬁrst thirteen prime numbers. That
produced a solution for 𝑥 1 with units that had to be raised to a power of over 300 trillion. Any more
Incremental units-of-measure verification                                                           :15

terms than that soon ran into the upper-bound of 64-bit integers within our tools and hardware.
Even in these artiﬁcial cases, the number of loop iterations was approximately proportional to the
number of constraints between relatively prime co-eﬃcients.


  Theorem 3.7. The modiﬁed-HNF procedure outputs only integer matrices.


   Proof. The procedure invokes HNF and integer elementary row operations. It only allows di-
vision if all the numbers are cleanly divisible. The value of 𝑑 is chosen to be an integer by dividing
by the gcd of its numerator’s components. All these operations produce integer results or matrices,
therefore modiﬁed-HNF outputs only integer matrices.                                                 


3.4   Polymorphism and Critical Variables
In the case of consistent but under-determined systems, some of the unknown units variables will
have many possible solutions. This means either the provided units annotations are insuﬃcient
to give a single solution, or some variables are units-polymorphic. The distinction is made based
on context (see Deﬁnition 3.2): a variable (or formal argument) declared within a function or sub-
routine is treated as potentially units-polymorphic. Outside of a function or subroutine a single
units solution for each variable must be found or else it is considered underspeciﬁed: a candidate
‘critical variable’ that requires manual annotation. Critical variables are displayed in the output of
the units-suggest mode, as described in Section 2.1.
   Past work by (Contrastin et al. 2016) has stopped at this point because all of the consistent
uses of polymorphic functions (and subroutines) will be solved correctly and assigned a single
‘monomorphic’ units solution in each instance. This gives ‘implicit’ polymorphism: unannotated
variables in functions are quietly treated as units-polymorphic if possible. In this work, we add
support for ‘explicit’ polymorphism to CamFort, allowing the programmer to write annotations
using an ML-like syntax such as ’a or ’b as shown in Listing 3. We also allow the inference engine
to generate explicit speciﬁcations automatically for functions that are implicitly polymorphic, as
shown in Listing 5 (left).
   Kennedy (2009) and related systems such as F# are extensions of Hindley-Damas-Milner type
systems (Damas and Milner 1982; Hindley 1969), which naturally support inference of polymor-
phism and generation of explicit annotations. However, F# is stratiﬁed (see Section 6) therefore it
requires a special and explicit syntax applied to type annotations when units are involved. This
discourages incremental insertion of units into existing programs: annotating one variable could
require further changes to be propagated all throughout the program.
   Our approach instead assists with incremental speciﬁcation. Even with little or no explicit units
information provided, it infers explicit polymorphic units annotations as much as possible for the
program being analysed. One way for that to happen is through the operation of the modiﬁed
HNF procedure (Section 3.3), which produces additional columns that are categorised as ‘new
base units’ representing generated polymorphic units variables, with an example in Figure 10. But
even without those additional columns it is also possible to generate new base units. This occurs
when abstract units variables for function parameters, C[𝑈 [𝑓 , 𝑘, ∗]], are underconstrained. We
treat some of the unknown abstract units variables as if they were base units themselves and then
solve the equations in those terms. In other words, we select some of the non-return unknown
abstract unit variables and shift them      over to the right-hand side of the equation. Thus, for each
                   ′ C 𝑏 ′ B · · · 𝑏 ′ B of the solved augmented matrix 𝐻 from Figure 9, we rearrange
row 𝑐 1′ C1 · · · 𝑐𝑚  𝑚 1 1         𝑛   𝑛
:16                                          Matthew Danish, Dominic Orchard, and Andrew Rice

                                                    Í        Í          Í
the row to correspond to the equation/constraint        C=       B1 −       B2 where:
    n                                                    o
C = 𝑐 ′𝑗 C 𝑗 0 < 𝑗 ≤ 𝑚 ∧ C 𝑗 ≠ C[𝑈 [𝑓 , 𝑘, ∗]] ∨ 𝑘 = 0        (cols. that are not unknown abstract units)
    n                    o
        ′
B1 = 𝑏 𝑗 B 𝑗 0 < 𝑗 ≤ 𝑛                                        (previous RHS)
    n                                                       o
B2 = 𝑐 ′𝑗 B[𝑓 , 𝑘] 0 < 𝑗 ≤ 𝑚 ∧ C 𝑗 = C[𝑈 [𝑓 , 𝑘, ∗]] ∧ 𝑘 > 0 (newly generated base units)

where B[𝑓 , 𝑘] denotes a generated ‘base unit’ corresponding to an implicit units-polymorphic vari-
              Í
able. Thus, B2 comprises the sum of the newly generated base unit multiplied by the coeﬃcients
𝑐 ′𝑗 of the corresponding unknown abstract units from the previous left-hand side.
     This rearrangement reduces the solution space, ideally to a single point, and provides a sin-
gle units assignment for the polymorphic variables that previously had many possible answers.
From that point, all that remains is presentation: generation of human-readable, properly-scoped,
explicit polymorphic variable names, which is straightforward.

3.5   Modules and Separate Analysis
Larger programs can potentially generate thousands of constraints or more, making our system po-
tentially unworkable in real projects unless the problem is partitioned into manageable chunks (see
the quantitative study in Section 4). Since Fortran 90, programmers have had the ability to organise
their code into modules that have separate namespaces. Modules contain variables, subroutines
and functions, and may ‘use’ or import deﬁnitions from other modules. The rules for program
units (Figure 7) gather function and subroutine templates and associate them with modules via
‘module-mappings’ between module names and the tuple (Δ,𝑇 ) where Δ contains module-variable
constraints and 𝑇 is a mapping of function/subroutine names to their associated constraint tem-
plate. Module-maps can be saved to ﬁles known as ‘fsmod-ﬁles’ in our implementation and loaded
at a later time. This imitates a common approach used by Fortran compilers (and many other
languages) for separate compilation.
   However, if we were to simply store and re-load every single constraint found in the templates
then we would not reduce the size of the global constraint-solving problem and would continue
to face the same scalability problems as before. Instead, we follow venerable data-ﬂow analysis
practice (e.g. Barth 1978) and summarise by solving for the units of each function or subroutine
parameter in simplest terms, using our algorithm from Listing 6 as described in previous sections.
In particular, the ability to infer explicit polymorphism as described in Section 3.4 means that
we can even reduce the templates of polymorphic functions to a signature (a minimal set of con-
straints) that describes the relationship between their parameters. For example, the square function
from Listing 4 would be described wholly by the constraint signature 𝑈 [𝑓 , 0, ∗] ∼ 𝑈 [𝛼, ∗] 2 and
𝑈 [𝑓 , 1, ∗] ∼ 𝑈 [𝛼, ∗] where 𝛼 is a freshly-generated polymorphic units-variable. Any intermediate
constraints regarding the internals of the function are dropped. This can result in a stark reduction
in the problem size when there are many imports. As an example, with one of our test-case scien-
tiﬁc programs, simulating the Navier-Stokes equation (Griebel et al. 1997), the main module that
had previously imported approximately 5,000 constraints only needed 471 constraints when we
applied our signature reduction technique to the data stored in fsmod-ﬁles. This leads to roughly
a 5x speed up in solving overall (see Section 4).
   The module-based solver also allows us to handle another practical problem: dealing with third
party libraries that are supplied without source code or that cannot be processed with CamFort for
any reason. In such cases the programmer can annotate a stand-in stub module with the desired
units and compile it to an fsmod-ﬁle. That ﬁle can be saved or even distributed, and it is loaded
Incremental units-of-measure verification                                                         :17

by our tool when it performs inference on a program using the library. Similarly, built-in Fortran
functions are handled by an internal table of units for each of their parameters (see Section 3.7).

3.6 Partial Annotation of Programs
Several features of our system combine to enable an incremental approach to units speciﬁcation.
The units-suggest command informs the user of a subset of variables to consider giving explicit
annotations. Our annotations are comments, to avoid breaking other tools and compilers.
   Even without annotations, we can infer implicit polymorphic units and derive explicit speciﬁ-
cations for functions and subroutines. That alone can detect inconsistent usages of variables, for
example an expression such as sqrt(x) + x would force our system to infer the unitless speciﬁ-
cation unit 1 :: x, which would be noticeable when looking over the output of units-infer.
Our handling of variables and literal values makes it easy to introduce units on one variable and
let the global-constraint solver propagate them as far as possible (see comparison with F# which
does not allow this in Section 6). Separate analysis of modules improves the performance of the
analysis but also helps to organise and compartmentalise the speciﬁcation eﬀort.

3.7 Intrinsics and unit casting
Fortran language standards specify a base library of arithmetic and trigonometric functions called
‘intrinsics’. Our implementation assigns to each of these a suitable polymorphic unit speciﬁcation,
e.g., abs takes an argument with unit ’a and returns a result of unit ’a. The transfer intrinsic
performs unsafe type casts in Fortran, where transfer(e1, e2) returns the value of expression e1
but at the type of the expression e2. We specify transfer as taking parameters of unit ’a and ’b,
returning a result of unit ’b. Thus, this may be used for explicit unit casting if using a conversion-
factor value (Section 3.1.3) is not possible.

4    SCALABILITY
We provide some quantitative evidence of the scalability of our approach by timing our tool in
inference mode. We algorithmically synthesised Fortran programs with large numbers of (poly-
morphic) constraints which were then generated into two extensionally equivalent code bases (1)
a single ﬁle containing many functions; and (2) multiple ﬁles containing a single function, with
a top-level module. By increasing the size of the programs and timing the two classes, we can
observe how our approach supports and promotes modularised code.
   Program synthesis. Algorithmic synthesis of test programs has four parameters varied as fol-
lows:
(1) number of functions, 𝑛 ∈ {5, 10, 15};
(2) length of each function, 𝑙 ∈ {5, 10, 15, 20};
(3) number of function arguments, 𝑎 ∈ {2, 4};
(4) single or multiple-ﬁle code base, fmt ∈ {single, mult}
A function of length 𝑙 comprises 𝑙 local variables and 𝑙 − 2 assignments of the form vi = vx * vy
where vx is the (𝑖 − 2) th variable and vy is the (𝑖 − 1) th variable. This creates a large number of
interrelated constraints and tests both multiplication of units and equality (which has the same
eﬀect as constraints generated by addition). The return result of the function is the 𝑙 th variable.
For example, a ﬁle generated from parameters fmt = mult, 𝑙 = 5, and 𝑎 = 2 is:
    module big1
      real function f1(v1, v2)
        real :: v1, v2, v3, v4, v5
        v3 = (v2 * v1)
:18                                                Matthew Danish, Dominic Orchard, and Andrew Rice

      v4 = (v3 * v2)
      v5 = (v4 * v3)
      f1 = v5
    end function f1
  end module big1
The parameters of f1 have units inferred as ’a :: v1 and ’b :: v2 the result as (’a**2) (’b**3)
:: f1. The exponents of the polymorphic units variables in the result of generated programs are
the (𝑙 − 1) th and (𝑙 − 2) th Fibonacci numbers and each variable vi can be expressed as the multi-
plication of v1 and v0 raised to the (𝑖 − 1) th and (𝑖 − 2) th Fibonacci numbers respectively. The fact
that every three consecutive Fibonacci numbers are pairwise co-prime ensures that intermediate
exponents will not be trivially divided away.
   The top-level generated program is a subroutine with 𝑙 × 𝑛 parameters which are used to call
each function with unique parameters, but all the units of all the results are uniﬁed by assigning
to an additional single, common variable.
   Method. We enumerated the parameter space and recorded the mean time of ﬁve trials for each
instance, also calculating the standard error based on sample variance. For the multi-ﬁle programs,
we ran our tool in units-compile mode to generate intermediate precompiled ﬁles then used
units-infer on the top-level program, importing the precompiled ﬁles. In the single-ﬁle mode,
all functions are in one ﬁle thus requiring just one invocation of units-infer.
   Measurements were taken on a 3.2 Ghz Intel Core i5 machine with 16 GB RAM, Mac OS 10.13.4.
   Results. Table 1 gives the results. It is clear that the single ﬁle programs suﬀer from non-linear
scaling (somewhere between quadratic and cubic time), whereas multiple-ﬁle compilation scales
well. Our approach thus successfully mitigates the high-cost of global constraint solving for units-
of-measure in highly polymorphic contexts (which is expensive, as shown by the single ﬁle case).
   For comparison, Table 2 gives the inference time for two real numerical models: a Navier-Stokes
ﬂuid model (Griebel et al. 1997), split across six modules totalling 517 physical lines of code; and
cliﬀs a tsunami model comprising 2.7kloc over 30 modules (Tolkova 2014).1 We also include in-
ference times for the case study modules considered in Section 5 taken from wrf, the Weather
Research and Forecast Model (Skamarock et al. 2008).
   Navier-Stokes is comparable in size to the 𝑛 = 15, 𝑙 = 15, 𝑎 = 2 programs (514 physical lines
of code in single ﬁle and 573 lines of code in 15 ﬁles). We also coalesced the program units of the
Navier code into a single ﬁle (navier-alt) to compare with the single ﬁle performance on similar-
sized generated ﬁles. The constraints generated from the real-world program are clearly less oner-
ous in the single-ﬁle case than our generated programs.

5 CASE STUDIES
One diﬃculty of units analysis compared to some other forms of static analysis is that it requires
knowledge of programmer intention and domain in order to provide meaningful annotations.
Therefore the process can only be partly automated. With existing bodies of code we rely upon
documentation in order to provide information about the units that should be assigned to vari-
ables. Unfortunately for most real scientiﬁc programs that documentation is often incomplete, if
present at all. For samples of Fortran code that are readily available, widely used and mature we
took the Weather Research and Forecast Model (Skamarock et al. 2008) by the National Center for
Atmospheric Research. This project contains over half a million lines of Fortran in about 200 ﬁles
with numerous add-on sub-projects as well. The code has been developed over many years and is
1 Source line counts are of physical lines (excluding comments and whitespace) generated by SLOCCOUNT (Wheeler 2001).
Incremental units-of-measure verification                                                                     :19

                                  𝑎=2                                               𝑎=4
 n      l    loc       single (s)     loc       mult (s)       loc       single (s)   loc        mult (s)
  5    5     74        0.649 ±0.002 93       0.557 ±0.005      84       0.790 ±0.004 103       0.687 ±0.013
  5    10    124       1.690 ±0.003 143      0.883 ±0.001      134      2.026 ±0.003 153       1.228 ±0.024
  5    15    174       3.681 ±0.003 193      1.200 ±0.003      184      4.640 ±0.003 203       1.696 ±0.030
  5    20    224       7.504 ±0.003 243      1.513 ±0.008      234      9.959 ±0.006 253       2.234 ±0.041
 10    5     144       2.141 ±0.002 183      1.254 ±0.013      164      1.265 ±0.002 203       1.675 ±0.028
 10    10    244       6.979 ±0.003 283      1.915 ±0.012      264     21.024 ±0.010 303       5.714 ±0.159
 10    15    344      56.492 ±0.127 383      3.364 ±0.040      364    103.297 ±0.048 403      12.224 ±0.386
 10    20    444      41.853 ±0.232 483      3.658 ±0.023      464    142.871 ±0.041 503      14.926 ±0.463
 15    5     214       7.692 ±0.005 273      2.074 ±0.019      244      2.542 ±0.007 303       3.972 ±0.069
 15    10    364      38.043 ±0.006 423      3.915 ±0.040      394     50.524 ±0.080 453      35.471 ±0.898
 15    15    514     205.565 ±0.059 573      6.014 ±0.070      544    284.832 ±0.107 603      99.916 ±2.624
 15    20    664   1,009.508 ±0.417 723      8.496 ±0.107      694    456.948 ±0.120 753      81.796 ±2.101

   Table 1. Timing results for scalability experiments (in seconds, to 3 s.f. with standard (sample) error)

                                        package            loc       ﬁles   inference time(s)
                                          navier            517        6     10.241 ±0.303
                                       navier-alt           481        1     47.704 ±0.002
                                            cliﬀs         2,706       30     40.881 ±0.121
                                             wrf
                             (chem) aerorate_so2             82       3       0.370 ±0.002
                           (phys) module_sf_oml             127       1       3.361 ±0.002
               (phys) module_cam_wv_saturation              693       1      20.685 ±0.008
      Table 2. Timing results on some real packages (in seconds, to 3 s.f. with standard (sample) error)


of varying quality. Some ﬁles have comments describing the units-of-measure for many variables.
We focused on a selection of those ﬁles and worked on annotating the variables based on their
accompanying comments. We ﬁlled in the remaining gaps using an iterative process of inference
and consultation of scientiﬁc textbooks and papers from which the algorithms had been derived.
 • aerorate_so2: this ﬁle is found in the Chem subproject and it depends upon two other modules.
    We applied 7 units annotations within the ﬁle and 11 annotations within the other modules.
    This process led us to ﬁnding an inconsistency in one equation where the program was at-
    tempting to convert a value from grams to micro-grams by multiplying by 10−6 instead of
    106 .
 • module_sf_oml: this module is from the core physics code comprising 127 physical lines of
    code. It is an implementation of an old and lesser-used mixed ocean layer model (Pollard 1973).
    We added 25 annotations to this ﬁle for documentation purposes but at least a third of them
    could have been omitted for inference purposes. As we narrowed down the assignment of units
    we found a contradiction for some of the helper variables holding intermediate results for wind
    speed. We have provided feedback to the developers about this inconsistency.
 • module_cam_wv_saturation: this ﬁle is from the core physics code and has 693 physical
    lines of code. It has routines that estimate saturation vapour pressure and speciﬁc humidity.
    We added 28 annotations to this ﬁle and found an ‘inconsistent use of units’ in several instances
    of an equation. However, this equation computes a derivative of pressure over temperature for
:20                                              Matthew Danish, Dominic Orchard, and Andrew Rice

       // F#                                           ! CamFort extension
       let x = 3.0<kg>                                 != unit kg :: x
       let y = 4.0                                     real :: x = 3.0, y = 4.0, z
       let z = x + y                                   z = x + y
       // Error:                                       ! OK:
       // units mismatch with x and y                  ! inferred unit kg :: y, z

                       Listing 7. Annotating a single literal is suﬀicient for CamFort.


      speciﬁc ranges of inputs. One term used a change-in-Kelvin while the other used a change-in-
      Celsius. In this case, these are compatible quantities. In general we would advise users to avoid
      mixing Kelvin and Celsius because in other contexts they are not immediately interchangeable.
      Thus, whilst not a direct bug, our tool indicated undocumented unit conversion behaviour.

6     RELATED WORK AND DISCUSSION
   Kennedy and F#. The most mainstream implementation of Kennedy (1996) is found in a standard
extension of the F# language (Kennedy 2009). Units of measure may be declared or aliased using
a special syntax:
[<Measure>] type cm
[<Measure>] type ml = cm^3
Types and literal values are annotated directly using a syntactic extension:
let cm_to_inch(x:float<cm>) = x / 2.54<cm/inch>
The types are stratiﬁed: the float type cannot be uniﬁed with a units-annotated float<u> type,
only with float<1> . This makes transitioning existing code-bases diﬃcult because adding units
annotations to a function means that you have to annotate all of its call-sites as well. Our approach
requires as little annotation as possible, using global constraint-solving to ﬁll in the gaps.
  In Kennedy’s inference algorithm, nonzero literals are inferred as unitless unless given an
explicit annotation. Using our notation (and our representation of abstract units variables),
Kennedy’s rules for literals could be written as:
                           freshid(𝑙)                            𝑛≠0
                                               Kpolyzeroex                  Kliteral ex
                       Γ ⊢ 0 : 𝑈 [𝑓 , 𝑙, ∗]; ·                 Γ ⊢ 𝑛 : 1; ·
That is, 0 is treated polymorphically (with a fresh abstract unit variable) and all other unanno-
tated literals are treated as unitless. However, we distinguish literals at the top-level of a pro-
gram/module from those in a function/subroutine: see literal ex from Figure 4. Thus, units con-
straints provided through the literal exception (see Section 3.1.2) can provide a bridge between the
units of other expressions, without requiring all literals to be annotated. The eﬀect can be seen in
the comparison between F# and our extension of CamFort shown in Listing 7. Fixing the F# exam-
ple would require the literal value 4.0 to be explicitly marked with either the annotation <kg> or
the wildcard <_>.
   Furthermore, F# units are annotated directly on variables and literals, meaning that any tools
operating on the F# code must understand the units syntax. The CamFort approach, which we
share, has been to avoid custom code constructs and instead use a comment-based annotation
syntax that can be safely ignored by any tools (and compilers) that do not know about units. The
goal is that CamFort’s units annotations can safely be ignored or erased without aﬀecting pro-
gram operation. That design choice leads to certain consequences, including that literals cannot
be annotated directly, and so we do not support any notion of a custom ‘units-casting operation’
(although Fortran’s casting operation transfer could be used this way). Instead, we allow a literal
Incremental units-of-measure verification                                                         :21

to take on a variable’s explicitly annotated units if it is the sole expression in an assignment to
that variable (Section 3.1.1).

   Phriky Units. The approach taken by Ore et al. (2017) avoids the need for any units-of-measure
annotation within C++ programs. This is achieved by ﬁrst creating ﬁles containing sets of anno-
tations for commonly shared libraries, and then propagating that units information outward from
any points in programs that use those shared libraries. Because the annotations are associated
with shared libraries, user-programs need not be annotated themselves if they use the annotated
library. The algorithm for checking units is intentionally unsound for simplicity and performance
purposes. It employs a form of intraprocedural dataﬂow analysis that approximates the true set
of constraints, sometimes too loosely and sometimes too tightly. While this can lead to clear prob-
lems it also means that the system is ﬂexible in the presence of C++ code structures that are not
fully analysable by the tool. Instead of giving polymorphic units to functions, Phriky Units simply
skips these functions if there are no monomorphic units constraints to check.

   Osprey. Jiang and Su (2006) developed Osprey, a scalable units-of-measure checking system for
the C programming language. Like ours, their system supports suggesting critical variables and
units aliasing. But they only have support for leaf polymorphism, which is a limited form of generic
units mechanism that only works within the function calls at the leaves of the call-tree. In contrast,
we can infer speciﬁcations for polymorphic units variables at arbitrary depths; meaning that poly-
morphic functions can call polymorphic functions in our system, important for larger functions
that may be (partly) polymorphic. Additionally, Osprey allows compositional units analysis only
at function boundaries while we also support separate analysis that can use the modular structure
of the program to partition the work.

   CamFort. The problem of adding units to Fortran programs has more recently been studied by
Contrastin et al. (2016); Orchard et al. (2015) as part of the CamFort project (Orchard et al. 2017).
Their work was similar to Osprey in its theoretical capability for analysing units, except that Cam-
Fort fully supported implicit units-polymorphism at all levels of the call-tree. Their system would
try to assume that a function was units-polymorphic if it had no explicit units annotations. We
found that the CamFort units analysis engine was not practical for use on real programs due to seri-
ous ineﬃciency and lack of module support. We have reused and adapted some of the open source
CamFort code for parsing and analysing Fortran code. On top of that, we have largely rewritten
and greatly extended the units-inference and checking capabilities of CamFort to support impor-
tant features that we describe in this paper such as checking and inferring explicit annotations for
units-polymorphism, working across modules within larger projects and an enhanced and much
more eﬃcient solver based on our modiﬁed HNF algorithm (Section 3.3).

   N1969. Snyder (2013) oﬃcially proposed an ISO standard extension of Fortran syntax, now re-
jected, to accommodate the speciﬁcation of units-of-measure and type uniﬁcation supporting the
equational theory of Abelian groups. This included two new statements for declaring the names
of units and a units attribute that could be provided for variable declarations. The original Cam-
Fort units syntax was based on this proposal (Orchard et al. 2015) however it has since evolved
to a comment-based annotation syntax based on the principle of harmlessness to other tools (Sec-
tion 3.1.2). N1969 did not propose inference and would require units annotation of every variable,
which renders it impractical, especially for adoption in existing projects.

  CPF[UNITS]. Chen et al. (2003); Hills et al. (2008); Roşu and Chen (2003) describe a comment-
based syntax for units-of-measure annotation on the bc calculator and C languages. These rely
:22                                          Matthew Danish, Dominic Orchard, and Andrew Rice

upon the Maude system of rewriting logic. Units can be checked dynamically or statically; we
focus on the latter since it is comparable to our system:
 • Variables can be assigned diﬀerent units in diﬀerent program branches, unlike a typical type
   system, therefore static checking must consider multiple possible assignments of units to vari-
   ables, risking exponential running time for static veriﬁcation. Loops must be re-analysed until
   they reach a ﬁxed point, or handled by some predeﬁned ‘code pattern’ matching mechanism.
 • It is possible to describe relationships between a function’s input parameters and its output
   results, e.g. @unit(@result) = @unit(parameter), and that provides a facility that is similar
   to units-polymorphism for the purpose of specifying function behaviour.
 • There is no units-inference or critical variable suggestion facility, only checking.
 • One of the most important assumptions of the CPF[UNITS] is called the ‘locality principle’,
   which says when the programmer uses a constant with a simple instruction such as 𝑥 + 5 the
   checker assumes that the constant has the same units as the variable. This is superﬁcially sim-
   ilar to our literal exception (Section 3.1.2), but we do not allow any other operation than direct
   assignment of a literal value to a variable, and polymorphism is not allowed. The ‘locality prin-
   ciple’ breaks soundness in CPF[UNITS] by allowing you to write units-polymorphic functions
   that are not dimensionally invariant (for more details see Section 3.1.4). In Listing 8 we show
   two examples that exploit the problems caused by the locality principle. First we deﬁne a func-
   tion sqr that numerically returns the square of its input, but dimensionally does not. Second
   we deﬁne a function f that breaks dimensional invariance. These two cases happen because
   the system allows us to treat the literals 1 and 2.0 respectively as having polymorphic units.
   Since constraints are compiled into Maude, it is not clear how this problem can be ﬁxed, and
   CPF[UNITS] is no longer an active project.
   Squants. Keorkunian et al. (2017) have released a framework for Scala that provides units-of-
measure functionality within Scala’s expressive type system. Squants provides a hierarchy of di-
mensions with associated units and easy insertion into Scala programs with many conveniences
such as easy conversion and static checking.
   However, this system is not capable of solving equations on units as an Abelian group, therefore
it is limited in expressivity. For example, you cannot multiply together arbitrary quantities with
dimensions; only predeﬁned or user-deﬁned combination of units are supported. It is impossible
to deﬁne functions that behave like our example square in Listing 3. The abstract class Quantity
only supports multiplication by a dimensionless Double, therefore the function sqr in Listing 9
squares the value but merely returns the same units that it is given. Still, given this limitation, the
authors have deﬁned many convenient units. For example, if you multiply Meters(2) by Meters(2)
the result is SquareMeters(4) . And if you multiply SquareMeters(4) by Meters(2) then the result is
CubicMeters(8) . However if you multiply CubicMeters(8) by Meters(2) then the result is an error.


 //@ post(UNITS): @unit(@result) = @unit(x)
 int sqr(int x) {                        //@ post(UNITS): @unit(@result) = @unit(x)
   int y = 0, i;                         double f(double x) {
   for(i=0;i<x;i+=1)                        return x + 2.0;
     y += x;                             }
   return y;                             // e.g. f(2.54 * 1.0) != 2.54 * f(1.0)
 }

Listing 8. Unsound examples in CPF[UNITS]: a function sqr that squares its parameter but not its units
(left), and a function f that breaks dimensional invariance (see Section 3.1.4) (right).
Incremental units-of-measure verification                                                            :23

def sqr[A <: Quantity[A]](x: Quantity[A]): Quantity[A] = {x*x.value}
def f[A <: Quantity[A]](x: Quantity[A]): Quantity[A] = {x+x.unit.apply(2)}

scala> sqr(Meters(3))
res0: squants.Quantity[squants.space.Length] = 9.0 m
scala> f(Inches(1)) in Centimeters
res1: squants.space.Length = 7.62001524 cm
scala> f(Inches(1) in Centimeters)
res2: squants.Quantity[squants.space.Length] = 4.54000508 cm

Listing 9. Examples in Squants and the Scala REPL: a function sqr that squares its parameter but not its
units, and a function f that breaks dimensional invariance (see Section 3.1.4).


    The addition operation of abstract class Quantity operates on two values of the same class, and
it is possible to polymorphically create a literal having the same units as a given parameter. This
is shown in Listing 9 by function f that uses the same technique as Listing 8 to break dimensional
invariance (see Section 3.1.4 for details). Examples executed in the Scala REPL show the unfor-
tunate results. With Squants we can deﬁne a function f for which f(Inches(1)) in Centimeters
produces a diﬀerent result than f(Inches(1) in Centimeters) , therefore dimensional invariance
is broken.
   Other work integrated with static types. There are several other libraries that also take advan-
tage of their language’s advanced type system features to provide a statically-checked units-of-
measure speciﬁcation feature. C++ has Boost::Units (Schabel and Watanabe 2010), the package
‘dimensional’ is available for Haskell (Buckwalter 2018) and JScience (Dautelle 2011) is a scien-
tiﬁc programming package for Java that includes a units-of-measure library. All of these oﬀer
statically-checked units that integrate with the host language. However that comes with a down-
side, because they cannot easily embed the equational theory of an Abelian group, the uses of
units can be somewhat awkward and units-inference is not possible in the same way that F# or
our work can manage.
   Gundry (2015) provides a units-of-measure system for Haskell, reusing Haskell’s type inference
algorithm with a custom solver via a type-checker plugin, and macros to extend the surface syntax.
Since Gundry’s approach reuses type inference, the constraint generation is similar to that of F#’s.
   A notable past eﬀort includes the Fortress language (Allen et al. 2005) that was designed to in-
clude units-of-measure from the very start, however work on the language has been discontinued.
Also, the author of JScience attempted to have a units speciﬁcation added to the Java language but
the proposal was rejected (Dautelle and Keil 2010).
  Semantics. Atkey et al. (2015) introduce a simple calculus with polymorphic units for the pur-
poses of modelling the underlying type theory. They do not present any algorithms for checking
or inference, but instead give a type system speciﬁcation (via inference rules) with introduction
and elimination rules for universal quantiﬁcation over units-of-measure variables. Their semantics
gives a basis for proving parametricity theorems on units-polymorphic functions.
   Run-time checking of units-of-measure. Several systems and libraries oﬀer tagging of numbers
with units-of-measure ‘metadata’ and dynamically checking the results of computations to ensure
that the units are consistent. These include several Python modules (Byrnes 2018; Donohue 2017;
Grecco et al. 2017), an R library (Pebesma et al. 2018), a Haskell package (Reaver 2015), a Fortran
library (Petty 2001) and many others that work in a similar manner. These systems take a fun-
damentally diﬀerent approach to ours, by only catching errors after they have happened, while
:24                                                     Matthew Danish, Dominic Orchard, and Andrew Rice

our work seeks to ﬁnd inconsistencies before they strike and with zero run-time overhead. The
beneﬁts of run-time checking are an easier implementation and more ﬂexibility. The costs are over-
head in memory and time, the need to handle the resulting errors at run-time and the possibility
of missing bugs in programs that are incompletely tested.

6.1 Conclusion and further work
We have described a new system for incremental inference and veriﬁcation of units-of-measure
on modular programs. We have created an algorithm based on Hermite Normal Form to solve
constraint problems involving polymorphic units, and to produce signatures for functions and
subroutines within modules. We make it possible to partition the global constraint solving prob-
lem into smaller pieces that are more easily solved, and show that this approach has great potential
to speed-up the analysis. Our method of annotation maintains the principles of harmlessness and
incrementalism by relying solely on a comment-based syntax and allowing users to write annota-
tions at their own pace, working with whatever is provided the best we can. We can also automate
part of the work with suggestions and code synthesis. We believe that our system addresses many
of the problems that have beset past work in software units and dimensional analysis, and we
intend to further reﬁne it into a practical tool for the working scientist.
   During this project, we have noticed that some scientiﬁc formulas, at least for intermediate
values, involve taking logarithms of units (e.g. Goﬀ and Gratch 1946), or raising units to rational
powers, such as with the Gauckler-Manning coeﬃcient (Chanson 2004, p79). Further work is to
ﬁnd a way to sensibly encode these formulas without disturbing the rest of the system.
   Another area for exploration is array indices: units-annotated integer variables may be used as
array indices but we do not currently have support for specifying the units of indices.

ACKNOWLEDGMENTS
This work has been supported by Grant EP/M026124/1 from the Engineering and Physical Sciences
Research Council.Any opinions, ﬁndings, and conclusions or recommendations expressed in this
material are those of the authors and do not necessarily reﬂect the views of the EPSRC.

REFERENCES
E. Allen, D. Chase, J. Hallett, V. Luchangco, J.-W. Maessen, S. Ryu, G.L. Steele Jr., S. Tobin-Hochstadt, J. Dias, C. Eastlund,
   et al. 2005. The Fortress Language Speciﬁcation. Sun Microsystems.
Robert Atkey, Neil Ghani, Fredrik Nordvall Forsberg, Timothy Revell, and Sam Staton. 2015. Models for polymorphism
   over physical dimensions. (2015).
Jeﬀrey M. Barth. 1978. A Practical Interprocedural Data Flow Analysis Algorithm. Commun. ACM 21, 9 (Sept. 1978),
   724–736. https://doi.org/10.1145/359588.359596
Bjorn Buckwalter. 2018. Dimensional. http://hackage.haskell.org/package/dimensional. (2018).
Steven Byrnes. 2018. numericalunits. https://pypi.python.org/pypi/numericalunits. (2018).
Hubert Chanson. 2004. Hydralics of Open Channel Flow. Elsevier.
Feng Chen, Grigore Roşu, and Ram Prasad Venkatesan. 2003. Rule-based analysis of dimensional safety. In International
   Conference on Rewriting Techniques and Applications. Springer, 197–207.
Henri Cohen. 2013. A course in computational algebraic number theory. Vol. 138. Springer Science & Business Media.
Mistral Contrastin, Andrew Rice, Matthew Danish, and Dominic Orchard. 2016. Units-of-measure correctness in Fortran
   programs. Computing in Science & Engineering 18, 1 (2016), 102–107.
Luis Damas and Robin Milner. 1982. Principal Type-schemes for Functional Programs. In Proceedings of the 9th ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’82). ACM, New York, NY, USA, 207–212.
   https://doi.org/10.1145/582153.582176
Jean-Marie Dautelle. 2011. JScience. http://jscience.org/. (2011).
Jean-Marie Dautelle and Werner Keil. 2010. JSR 275: Units Speciﬁcation. https://www.jcp.org/en/jsr/detail?id=275. (2010).
Aran Donohue. 2017. units for Python. https://pypi.python.org/pypi/units/. (2017).
Incremental units-of-measure verification                                                                               :25

Elizabeth Durant. 2008. Smoot’s Legacy. http://alum.mit.edu/news/AlumniNews/Archive/smoots_legacy. (July 2008). Ac-
   cessed: 2017-10-23.
J A Goﬀ and S Gratch. 1946. Low-pressure properties of water from -160 to 212 °F. Transactions of the American Society
   of Heating and Ventilating Engineers (1946), 95–122. presented at the 52nd annual meeting of the American Society of
   Heating and Ventilating Engineers, New York.
Hernan E. Grecco et al. 2017. Pint. https://pypi.python.org/pypi/Pint. (2017).
M. Griebel, T. Dornsheifer, and T. Neunhoeﬀer. 1997. Numerical simulation in ﬂuid dynamics: a practical introduction. Vol. 3.
   Society for Industrial Mathematics.
Adam Gundry. 2015. A typechecker plugin for units of measure: Domain-speciﬁc constraint solving in GHC Haskell. In
   ACM SIGPLAN Notices, Vol. 50. ACM, 11–22.
Mark Hills, Feng Chen, and Grigore Roşu. 2008. A rewriting logic approach to static checking of units of measurement in
   C. In Ninth International Workshop on Rule-Based Programming. Elsevier, 51–67.
R. Hindley. 1969. The Principal Type-Scheme of an Object in Combinatory Logic. Trans. Amer. Math. Soc. 146 (1969), 29–60.
   http://www.jstor.org/stable/1995158
International Organization for Standardization 2010. ISO/IEC 1539-1:2010 Fortran. International Organization for Standard-
   ization.
Lingxiao Jiang and Zhendong Su. 2006. Osprey: a practical type system for validating dimensional unit correctness of C
   programs. In Proceedings of the 28th International Conference on Software Engineering. ACM, 262–271.
Simon Peyton Jones, Dimitrios Vytiniotis, Stephanie Weirich, and Mark Shields. 2007. Practical type inference for arbitrary-
   rank types. Journal of functional programming 17, 1 (2007), 1–82.
Andrew Kennedy. 1994. Dimension types. Programming Languages and Systems—ESOP’94 (1994), 348–362.
Andrew Kennedy. 2009. Types for Units-of-Measure: Theory and Practice. Springer Berlin Heidelberg, Berlin, Heidelberg,
   268–305. https://doi.org/10.1007/978-3-642-17685-2_8
Andrew John Kennedy. 1996. Programming languages and dimensions. Technical Report. University of Cambridge, Com-
   puter Laboratory.
Gary Keorkunian, Derek Morr, et al. 2017. Squants. http://www.squants.com/. (2017).
Enzo O. Macagno. 1971. Historico-critical review of dimensional analysis. Journal of the Franklin Institute 292, 6 (1971),
   391–402. https://doi.org/10.1016/0016-0032(71)90160-8
Paul Marks. 2009.                  NASA criticized for sticking to imperial units.                           (June 2009).
   https://www.newscientist.com/article/dn17350-nasa-criticised-for-sticking-to-imperial-units/         Accessed: 2017-10-
   23.
Robert C Martin. 2009. Clean code: a handbook of agile software craftsmanship. Pearson Education.
Zeeya Merali. 2010. Computational science: error, why scientiﬁc programming does not compute. Nature 467 (October
   2010). https://doi.org/10.1038/467775a
Alan Mycroft. 1984. Polymorphic type schemes and recursive deﬁnitions. Springer Berlin Heidelberg, Berlin, Heidelberg,
   217–228. https://doi.org/10.1007/3-540-12925-1_41
NASA 1998. Mars Climate Orbiter Fact Sheet. (1998). https://mars.jpl.nasa.gov/msp98/orbiter/fact.html Accessed: 2017-
   10-23.
Dominic Orchard, Matthew Danish, Mistral Contrastin, and Andrew Rice. 2017. CamFort. http://camfort.github.io/. (2017).
Dominic Orchard and Andrew Rice. 2014. A Computational Science Agenda for Programming Language Research. Procedia
   Computer Science 29, Supplement C (2014), 713 – 727. https://doi.org/10.1016/j.procs.2014.05.064 2014 International
   Conference on Computational Science.
Dominic Orchard, Andrew Rice, and Oleg Oshmyan. 2015. Evolving Fortran types with inferred units-of-measure. Journal
   of Computational Science 9, Supplement C (2015), 156 – 162. https://doi.org/10.1016/j.jocs.2015.04.018 Computational
   Science at the Gates of Nature.
John-Paul Ore, Carrick Detweiler, and Sebastian Elbaum. 2017. Lightweight Detection of Physical Unit Inconsistencies
   Without Program Annotations. In Proceedings of the 26th ACM SIGSOFT International Symposium on Software Testing
   and Analysis (ISSTA 2017). ACM, New York, NY, USA, 341–351. https://doi.org/10.1145/3092703.3092722
Edzer     Pebesma,      Thomas      Mailund,      and    Tomasz      Kalinowski.     2018.               units     for    R.
   https://cran.r-project.org/web/packages/units/index.html. (2018).
Grant W Petty. 2001. Automated computation and consistency checking of physical dimensions and units in scientiﬁc
   programs. Software: Practice and Experience 31, 11 (2001), 1067–1076.
R. T. Pollard. 1973.       Wind driven mixing and deepening of the oceanic boundary layer.                 Quarterly Jour-
   nal of the Royal Meteorological Society 99, 422 (1973), 772–773.                 https://doi.org/10.1002/qj.49709942221
   arXiv:https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1002/qj.49709942221
John David Reaver. 2015. quantities. http://hackage.haskell.org/package/quantities. (2015).
:26                                                  Matthew Danish, Dominic Orchard, and Andrew Rice

Grigore Roşu and Feng Chen. 2003. Certifying measurement unit safety policy. In Automated Software Engineering, 2003.
   Proceedings. 18th IEEE International Conference on. IEEE, 304–309.
Matthias     Christian     Schabel     and    Steven     Watanabe.    2010.            Boost::Units.              (2010).
   https://www.boost.org/doc/libs/1_66_0/doc/html/boost_units.html
Igor R. Shafarevich and Alexey Remizov. 2012. Linear Algebra and Geometry. Spring Science & Business Media.
William C Skamarock, Joseph B Klemp, Jimy Dudhia, David O Gill, Dale M Barker, Michael G Duda, Huang Xiang-Yo, Wei
   Wang, and Jordan G Powers. 2008. A description of the advanced research WRF version 3. Technical Report. National
   Center For Atmospheric Research Boulder Co Mesoscale and Microscale Meteorology Div.
WV Snyder. 2013. ISO/IEC JTC1/SC22/WG5 N1969: Units of measure for numerical quantities. Technical Report. International
   Organization for Standardization. http://wg5-fortran.org/N1951-N2000/N1969.pdf
Arthur G Stephenson, Daniel R Mulville, Frank H Bauer, Greg A Dukeman, Peter Norvig, Lia S LaPiana, Peter J Rutledge,
   David Folta, and Robert Sackheim. 1999. Mars Climate Orbiter Mishap Investigation Board Phase I Report. Technical
   Report. NASA.
Elena Tolkova. 2014. Land–Water Boundary Treatment for a Tsunami Model With Dimensional Splitting. Pure and Applied
   Geophysics 171, 9 (2014), 2289–2314.
Mitchell Wand and Patrick O’Keefe. 1991. Automatic Dimensional Inference. In Computational Logic-Essays in Honor of
   Alan Robinson. 479–483.
David A Wheeler. 2001. SLOCCount. (2001).
