                                         Partial Automation of Verification Condition Proving
                                                     for Reflex Programs (Draft)
                                                                        Artyom Ishchenko                                           Igor Anureev
                                                                  Novosibirsk State University,                      Institute of Automation and Electrometry,
                                                           Department of Computer Science Systems                      Laboratory of Cyberphysical Systems
                                                           Institute of Automation and Electrometry,                            Novosibirsk, Russia
                                                             Laboratory of Cyberphysical Systems                               0000-0001-9574-128X
                                                                      Novosibirsk, Russia
                                                                     0009-0005-6176-5917



                                             Abstract—Process-Oriented Programming is a software              together with its specification is translated into a logical
arXiv:2606.23377v1 [cs.LO] 22 Jun 2026




                                         development approach that emphasizes the management of               formula expressed in a formal logic. Using a logical inference
                                         control systems through abstractions of processes and their          system – commonly referred to as the axiomatic semantics of
                                         states, enabling these systems to be described in terms of           the programming language – this formula is reduced to a set
                                         real physical processes. This native description of control          of logical formulas known as verification conditions (VCs). If
                                         is particularly important for industrial systems consisting          all generated verification conditions are proved to be true, the
                                         of hundreds or thousands of processes. For such systems,             program is considered correct with respect to its specification.
                                         safety is critical. To ensure the reliability and safety of these
                                                                                                                   Axiomatic semantics have been developed for many
                                         systems, formal verification methods must be applied. One such
                                         method is deductive verification, which involves formalizing
                                                                                                              programming languages, including Java [5], abstract
                                         programs and their requirements as logical formulas, known as        imperative languages [6], and C [7]. In such systems,
                                         verification conditions. Proving these conditions confirms that      the formalization of requirements typically results in
                                         the program meets its requirements. The automatic generation         preconditions and postconditions describing the behavior of
                                         of verification conditions is performed by a specialized software    program fragments. Various strategies exist for reasoning
                                         tool called a verification condition generator. We previously        about these conditions. In this work, we employ the
                                         proposed a verification condition generator for the Reflex           strongest postcondition strategy, which processes the program
                                         language. However, it generates too many verification conditions,    sequentially from beginning to end and derives postconditions
                                         making their manual proof impossible. This paper proposes            by applying inference rules that transform the current program
                                         modifications to the verification condition generator aimed          state.
                                         at automating the proof of some of these conditions. These                A practical challenge in deductive verification is the
                                         modifications include introducing an annotation language             large number of verification conditions generated for realistic
                                         to describe requirements in a structured form, generating            programs. In our previous work [8], we developed a
                                         invariants based on the program structure, and using SMT             verification condition generator (VCG) for Reflex programs.
                                         solvers for the preliminary attempt to solve the verification
                                                                                                              However, when applied to large programs, the tool produced
                                         conditions.
                                                                                                              thousands of verification conditions, making manual proof of
                                                                                                              all of them impractical.
                                             Keywords —Reflex, verification condition generator, deductive
                                         verification, process-oriented programming, program invariant,
                                                                                                                   In this paper, we present three extensions to the previously
                                         annotation language, SMT-solver                                      developed VCG aimed at increasing the level of automation in
                                                                                                              proving verification conditions:
                                                               I. I NTRODUCTION                                    1) an annotation language for specifying program
                                                                                                                       properties,
                                             The process-oriented paradigm [1] offers a promising                  2) a structure-based invariant generation mechanism,
                                         approach to programming industrial control systems. In this               3) integration with SMT solvers for automated reasoning.
                                         paradigm, a program consists of a set of interacting processes,
                                         each defined by a sequence of states that specify its execution                           II. P RELIMINARIES
                                         logic.
                                                                                                                This section describes the Reflex language and the
                                             The Reflex language [2] is a process-oriented dialect of         modifications made to it. It then provides an overview of
                                         the C programming language, accompanied by a dedicated               SMT solvers.
                                         translator [3]. Reflex combines the advantages of the process-
                                         oriented programming model with the familiar syntax and              A. The Reflex Language
                                         programming style of C, making it convenient for engineers
                                         developing industrial control applications.                              Reflex is a process-oriented dialect of the C programming
                                                                                                              language designed for programming industrial logic
                                             Since Reflex programs are used in industrial                     controllers. The language largely preserves the syntax of
                                         environments, they must satisfy strict safety and correctness        C statements and expressions while introducing several
                                         requirements. To ensure these properties, we employ                  adaptations required for control applications. In particular,
                                         deductive verification [4]. In this approach, a program              variable declarations are restricted to specific locations, data
                                           This work was supported by the Russian Ministry of Education and   types have strictly defined sizes, and additional primitive types
                                         Science, project 125022803031-1                                      such as time and bool are supported. Reflex also introduces
constructs specific to the process-oriented programming                Language) is used to annotate C programs with formal
paradigm.                                                              specifications [12]. Such languages allow developers to
     A Reflex program consists of a declaration of an                  express correctness properties in a structured and machine-
activation interval, declarations of variables and constants,          readable form, enabling automated reasoning tools to verify
and a sequence of process definitions. The activation interval         that the program satisfies its specification.
specifies the fixed time duration of a single program iteration            The Reflex language already includes an annotation
within the control loop.                                               language introduced in [13]. However, it lacks sufficient
     Each process is defined by its local variables and a set of       expressiveness and forces engineers to engage with low-level
active states. In addition, every process has two predefined           details of the translation logic. This increases the likelihood
inactive states, stop and error, and a clock that records the time     of errors in requirement specification and limits the kinds of
the process has spent in its current state. Initially, all processes   behavior it can describe. Therefore, the annotation language
except the first one start in the stop state. Processes that are       requires redesign.
currently in inactive states are considered inactive.
     A state represents a named sequence of C-like statements.         C. SMT solvers
These sequences may contain standard C statements except                   Satisfiability Modulo Theories (SMT) solving is a
loop constructs and the goto statement. In addition, Reflex            fundamental technique for automated reasoning about
provides process-oriented statements for changing the state of         logical formulas that arise in program verification, formal
a process (set state), resetting the process timer (reset timer),      methods, and symbolic analysis. SMT extends propositional
and controlling process execution (start, stop, and error). A          satisfiability (SAT) by allowing formulas to contain symbols
state may also include a timeout construct that checks whether         interpreted in background theories such as linear arithmetic,
the time spent in the current state exceeds a specified value and      arrays, bit-vectors, algebraic datatypes, and uninterpreted
executes a corresponding handler if the timeout occurs.                functions [14]. These theories enable a natural encoding of
     Program execution proceeds in iterations. During each             program constructs such as variables, memory structures, and
iteration, all processes of the program are executed in textual        control-flow conditions.
order according to their current states.                                   Formally, given a first-order formula φ and a background
     Reflex also provides constructs for expressing lightweight        theory T , an SMT solver determines whether φ is T -
intermediate execution points within a state. The construct            satisfiable, i.e., whether there exists a model that satisfies
wait(C) suspends the execution of the subsequent                       φ while respecting the semantics of the theory T . If such a
statements until the Boolean condition C becomes true. For             model exists, the solver returns sat together with a satisfying
example, if the state body has the form S1 ; wait(C); S2 ,             assignment. If no such model exists, the solver reports unsat.
where S1 and S2 are sequences of statements, then S1 is                When the solver cannot determine the satisfiability of the
executed first. If the condition C holds, execution proceeds           formula due to incomplete reasoning procedures or resource
with S2 ; otherwise, the execution of S2 is postponed until a          limits, the result may be unknown.
later program iteration in which C becomes true.                           Modern SMT solvers rely on a combination of Boolean
     The construct slice separates the execution of a state            reasoning and theory-specific reasoning procedures. The
body across program iterations. If a state body has the form           dominant architecture is based on the DPLL(T) framework
S1 ; slice; S2 , the statements in S1 are executed during the          [15], which integrates a SAT solver with dedicated theory
current iteration, while the execution of S2 continues in the          solvers. In this architecture, the SAT solver handles the
following iteration.                                                   Boolean abstraction of the formula, while the theory solvers
     The language also supports structured data types such             check the consistency of assignments with respect to the
as arrays and structures, which are declared using a syntax            background theories and generate additional constraints when
similar to that of C.                                                  inconsistencies are detected.
     The Reflex language implementation is based on the                    SMT solvers support a wide range of background
ANTLR4 toolset [9]. The complete grammar of the language               theories that are particularly useful in program verification.
is publicly available online [10].                                     For example, theories of arrays and algebraic datatypes
                                                                       allow modeling of memory structures and recursive
B. Annotation Languages                                                data structures, while uninterpreted functions provide an
    Annotation languages are commonly used in deductive                abstraction mechanism for reasoning about program functions
program verification to express formal specifications                  without fully specifying their semantics. Many SMT solvers
of program behavior directly within the source code.                   also support reasoning with quantified formulas, although
Annotations typically describe properties such as                      quantifier handling typically relies on heuristic instantiation
preconditions, postconditions, invariants, and assertions that         techniques and is not complete in general [16].
capture the intended behavior of program fragments. These                  To ensure interoperability between verification tools and
specifications are not executed as part of the program                 SMT solvers, the SMT-LIB initiative provides a standard input
itself; instead, they serve as logical constraints that guide          language and a large collection of benchmarks [17]. SMT-LIB
the verification process. During verification, annotations are         defines a uniform syntax for declaring sorts, functions, and
translated into logical formulas and combined with the                 logical constraints, allowing verification conditions generated
formal semantics of the programming language to generate               by analysis tools to be processed by different solvers without
verification conditions [4].                                           modification.
    Many modern verification frameworks rely on dedicated                  In deductive program verification, SMT solvers are
annotation languages or annotation extensions of existing              typically used to check verification conditions generated
programming languages. For example, the Java Modeling                  from annotated programs and program invariants. Program
Language (JML) provides specification constructs for Java              semantics and correctness properties are translated into
programs [11], while ACSL (ANSI/ISO C Specification                    logical formulas, and the solver is used to determine whether
a violation of the property is possible. If the conjunction        follow standard C semantics. The logical operators &&, ||
of the program semantics and the negation of the desired           are also defined, with their usual meanings.
property is unsatisfiable, the property is considered proven.          Let ϕ be an arbitrary formula, ρ a process name, ξ
Due to their efficiency and expressive power, SMT solvers          a process state name, and ι an expression. The following
have become a central component of modern verification             operators are defined:
frameworks. Widely used solvers include Z3 [18], CVC4 [19]
                                                                       • ϕ1 ==> ϕ2 – logical implication.
and CVC5 [20], which support a broad range of theories and
                                                                       • ϕ1 <==> ϕ2 – logical equivalence.
advanced solving techniques.
                                                                       • prev(ϕ) – a predicate stating that ϕ was true in the

               III. A NNOTATION L ANGUAGE                                 previous iteration of the algorithm.
                                                                       • before(ϕ) – a predicate stating that ϕ was true in some
    Annotations are written as C-style comments and are                   previous iteration of the algorithm.
distinguished by enclosing the content in square brackets.             • between(ϕ1 ,ϕ2 ,ϕmid ) – a predicate stating that ϕmid
Each annotation consists of a type T, an optional logical                 holds during the interval between iterations where ϕ1
language specifier L, and the content C:                                  and ϕ2 are true.
                                                                       • next(ϕ) – a predicate stating that ϕ will be true in the
//[T(L): C]
                                                                          next iteration of the algorithm.
/* [T: C]
                                                                       • eventually(ϕ) – a predicate stating that ϕ will become
[T: C]
                                                                          true in some future iteration.
*/                                                                     • in(ρ,ξ) – a predicate stating that process ρ is currently
The optional language specifier defines the syntax used                   in state ξ.
for the annotation content. If omitted, the default language           • time() – a function that returns the amount of time
described in III-B is assumed. This mechanism allows                      elapsed in the current state of the process.
annotations to be expressed in different formal languages,             • \FA(v1 , . . . , vn .ϕ(v1 . . . vn )) – the universal quantifier,
such as Isabelle/HOL.                                                     with bound variables v1 . . . vn and formula ϕ.
    Annotations are attached to the first statement or                 • \EX(v1 , . . . , vn .ϕ(v1 . . . vn ))     – the existential
declaration that follows them and are interpreted in the                  quantifier, with bound variables v1 . . . vn and formula
context of that program element.                                          ϕ.
                                                                       Variables appearing in annotations are interpreted after
A. Annotation types                                                the associated statement (or declaration) has initialized its
    The following types of annotations are supported:              variables and after name shadowing has been resolved.
    • [assume:C] – a logical condition that is assumed to
                                                                       The interpretation of the temporal operators (prev,
       hold before the execution of the associated statement.      before, between, next, eventually) depends on the statement
       For input variables, it acts as a specification and is      to which the containing expression is attached. For instance,
       taken as given without verification.                        in a program-level invariant, prev refers to the previous
    • [ assert :C] – a logical condition that must hold after
                                                                   program iteration. In a process state invariant, it refers to
       the execution of the associated statement. Its content      the previous program iteration, but only if the process was in
       C is a formula.                                             the same state. For a loop invariant, it refers to the previous
    • [ invariant :C] – a logical condition that must hold
                                                                   loop iteration.
       both before and after execution. When attached to a             An expression may also specify a scope
       loop, it provides a loop invariant. When attached to a      using      the     syntax       .scope(Φ),         where     Φ       ∈
       program, process, or state declaration, it contributes to   prev(), bef ore(ϕ), next(), eventually(ϕ). For example, in
       the global invariant of the system. Its content C is a      (x + y).scope(bef ore(x < y)), the expression x + y is
       formula.                                                    evaluated at the first point in the past when x < y held.
    • [ define :C] – introduces a new variable, constant, or           The annotation content language described in this section
       function. Its content C follows the syntax of a C-style     is the default. If no language is explicitly specified, this
       definition.                                                 language is used. Otherwise, the content must conform to the
                                                                   syntax of the specified language. For example, an annotation
    Program, process, and state declarations contain
                                                                   using Isabelle/HOL would be written as:
sequences of statements that execute within the activation
loop. Therefore, their behavior is best described using            //[invariant(Isabelle):
invariants, and the use of assume/assert annotations in these          \<forall>s. toEnvP s]
contexts should be avoided.
                                                                   Formulas provided in an external language are not
B. Annotation content                                              transformed during VC generation, except for variable name
                                                                   mangling to avoid conflicts. At the start of the verification
    The content of an annotation depends on its type,              condition generation process, these annotations are translated
but most annotations involve formulas. A formula is an             into the system’s internal representation of formulas.
expression of Boolean type. Constants, variables, and
function calls are all valid expressions. The operators                                IV. E XTRA I NVARIANTS
{+, −, ∗, /, %, >>, <<, |, &, ∧, ==, ! =, <, >, <=, >=, !}
are used to construct expressions from other expressions. The          Invariants are a crucial component of verification, as
operators {++, −−, + =, − =, ∗ =, / =, % =} may be                 they allow reasoning about program behavior that extends
used to construct expressions involving annotation-defined         beyond the current iteration. In addition to the invariants
variables, but only at the top level (i.e., expressions like       provided by the engineer, further invariants can be derived
x = y + + are not permitted). These two groups of operators        from the program structure and the sequences of statements
it contains. These automatically generated invariants are               2) Verify that these variables are not modified while the
formulated as logical formulas, as defined in [8].                          state is active.
    Let ρ be an arbitrary process name, ξ a process state               Both stabilized and non-stabilized variable invariants
name, and ν a variable name. The following kinds of                 also require that the relevant variables are not changed by
structural invariants are supported:                                any processes that execute after the one being analyzed.
    • Process states – characterizes the set of states each             Process state transition condition invariants are the
       process can occupy. These invariants have the form           most complex, as they require tracing all conditions and
       ∀s.toEnvP s −→ getP state s ρ ∈ ξ1 . . . ξn .                variable modifications along the path leading to a set state
    • Defined stabilized process state variables                –   statement.
       specifies the values that variables hold in stabilized           The initial state condition is added if the process is active
       process states (states that have been active for             from the first iteration of the program and the state being
       more than one consecutive iteration). They are               analyzed is its initial state.
       formulated as ∀s.toEnvP s ∧ getP state s ρ =                     A conditional transition condition corresponds to each
       ξ ∧ getP state (predEnv s) ρ = ξ −→                          set state statement. Analogous to the verification condition
       getV arV alue         s     ν1     =     val1 ∧ · · · ∧      generation process, a list of formulas is accumulated as
       getV arV alue s νn = valn .                                  the process state is traversed. When a set state statement
    • Defined non-stabilized process state variables –              is encountered, the collected formulas are filtered to retain
       specifies the values that variables hold upon entering       only those relevant to the conditional expressions that guard
       a particular process state. These invariants have            the transition (e.g., conditions from if-else or switch
       the form ∀s.toEnvP s ∧ getP state s ρ =                      statements). These relevant formulas are then conjoined to
       ξ −→ getV arV alue s ν1 = val1 ∧ · · · ∧                     form the condition.
       getV arV alue s νn = valn .                                      A timed transition condition is added when a transition
    • Process state transition condition – describes the            occurs within a timeout statement. It follows the same rules
       condition that must be satisfied to transition into a        as a general conditional transition.
       given process state. These invariants are expressed as
       ∀s.toEnvP s ∧ getP state s ρ = ξ −→ condition1 ∨                                 V. SMT PREPARATION
       · · · ∨ conditionn . The conditions are defined using           To use SMT solvers for checking verification conditions,
       an auxiliary function prevP rocState, which takes            two steps must be performed:
       a program state and a process name and returns the
       most recent program state in which the process’s state          1) Translate each verification condition into the input
       differed from its current one. This is represented as               language of an SMT solver.
       an intermediate variable using Isabelle/HOL’s let ...           2) Add auxiliary lemmas to assist in the proof.
       in ... construct. Two types of transition conditions are     A. Theory embedding
       distinguished:
                                                                        Translating the generated verification conditions into
            – Initial       state        has       the      form
                                                                    the SMT-LIB input language requires first embedding
               prevP rocState s pname = emptyState,
                                                                    the corresponding theory. The conditions are based on
               indicating that the process has been in this state
                                                                    manipulating a program state object and are constructed as
               since the start of the program.
                                                                    a sequence of function applications that modify the program
            – Conditional        transition     is     a    more
                                                                    state, together with formulas that refer to variable values
               general form expressed as let s2 =
                                                                    extracted from it.
               (prevP rocState s pname) in P (s2 ), where P
                                                                        The program state type is defined as follows:
               is some predicate. This includes the following
               subtype:                                             ( d e c l a r e − s o r t Var )
               ∗ Timed transition takes the form let s2 =           ( declare − sort Process )
                  (prevP rocState s pname) in                       ( declare − sort PState )
                  (ltime s2 pname ≥ time) ∧ P (s2 ), where          ( declare −datatypes ()
                  ltime returns the current time of process           (( State
                  pname and P represents any additional                     emptyState
                  condition.                                                ( toEnv ( prev S t a t e ) )
                                                                            ( setVarBool ( prev S t a t e )
    These invariants are relatively simple and structurally
                                                                                    ( v a r B o o l Var ) ( v a l B o o l Bool ) )
derived; they require only the tracing of program paths, a
                                                                            ...
process similar to that already performed during verification
                                                                            ( s e t P s t a t e ( prev S t a t e )
condition generation.
                                                                                    ( proc Process ) ( pval PState ) )
    Process state invariants are generated by analyzing the                 ( r e s e t ( prev S t a t e )
set of state names defined for each process.                                        ( procReset Process ))
    Defined stabilized process state variables invariants are         )))
derived by examining the sequence of statements within a
state. If a variable is assigned the same value at the end of          For the getter functions, an uninterpreted function
every iteration of that state, it is included in the invariant.     approach is used:
    Defined non-stabilized process state variables                  ( declare −fun getVarBool
invariants are constructed in two steps:                                   ( S t a t e S t r i n g ) Bool )
    1) Identify all variables that are defined before the state     ( assert
         is first entered.                                            ( f o r a l l ( ( s S t a t e ) ( x Var ) ( v Bool ) )
      (= ( getVarBool                                                     each verification condition interacts with at most two process
               ( setVarBool s x v ) x )                                   states (the one in which it starts and the one in which it
       v)))                                                               ends). These factors allow us to further narrow down the
( assert                                                                  proof context by discarding advanced lemmas unrelated to
  ( f o r a l l ( ( s S t a t e ) ( x Var ) ( Bool ) ( v I n t ) )        the states involved.
     (=> ( n o t ( = x y ) )
                                                                                            VI. VCG MODIFICATION
              (= ( g e t V a r I n t ( s e t V a r I n t s x v ) y )
                  ( getVarInt s y ) ) ) ) )                                   In [8], an algorithm for generating verification conditions
( assert                                                                  was described. This algorithm builds a control-flow graph
  ( f o r a l l ( ( s S t a t e ) ( x Var ) ( b I n t ) ( y Var ) )       of the program and traverses it, constructing verification
      (= ( getVarBool ( s e t V a r I n t s x b ) y )                     conditions as lists of formulas, which are then output as
            ( getVarBool s y ) ) ) )                                      Isabelle/HOL formulas. The architecture of the modified
                                                                          verification condition generator (VCG) is shown in Fig. 1.
Other getters are defined in a similar manner.
   The substate function checks whether one state is a
predecessor of another state:
( d e f i n e − fun − r e c s u b s t a t e
         ( ( s S t a t e ) ( t S t a t e ) ) Bool
  ( match t
    ( ( emptyState
              (= s e m p t y S t a t e ) )
      ( ( toEnv s1 )
              ( or (= s t )
                     ( s u b s t a t e s s1 ) ) )
       ...
  ))
   The function toEnvP checks whether a state is external:
( d e f i n e − f u n toEnvP ( ( s S t a t e ) ) Bool
      ( i s −toEnv s ) )
    The function predEnv returns the previous external
state:
( d e f i n e − fun − r e c p r e d E n v ( ( s S t a t e ) ) S t a t e
  ( match s                                                               Fig. 1. Modified algorithm of VCG.
    ( ( emptyState emptyState ) )
                                                                              The verification process begins by parsing the annotated
    ( ( toEnv s1 )
                                                                          program into an abstract syntax tree (AST). From this AST,
              ( i t e ( i s −toEnv s1 )
                                                                          a control-flow graph (CFG) of the program is constructed.
                      s1
                                                                          In parallel with CFG construction, the annotation parser
                      ( predEnv s1 ) ) )
                                                                          processes user-provided annotations, translates them into an
       ...
                                                                          internal logical representation, and associates them with the
  ))
                                                                          corresponding program statements and declarations.
                                                                              The invariant generator analyzes the structure of the
B. Auxiliary lemmas
                                                                          control-flow graph and produces additional invariants as
    To improve the likelihood of successful verification                  described in Sect. IV. These invariants, together with the
and to broaden the set of correctness conditions that can                 translated annotations, are used to form a proof context.
be proved, additional lemmas must be added. However,                          Next, the verification condition generation algorithm
excessive expansion of the lemma pool can lead to a                       traverses the control-flow graph and produces VCs. Each
significant drop in performance. To avoid this, all auxiliary             condition is processed independently. For every generated
lemmas are divided into several categories:                               VC, a corresponding proof context is constructed. This proof
    1) Base. This group consists of lemmas describing                     context contains auxiliary lemmas derived from annotations
        simple properties of the program state datatype and               and generated invariants, as well as a lemma representing the
        its functions, and is universal to all verification               behavioral requirement of the program. The negation of this
        conditions. For example, reflexivity of substate:                 requirement is used as the proof goal in the SMT query.
        ( assert ( forall (( s State )) ( substate s s )))                    Before being submitted to the solver, the verification
    2) Advanced. This group consists of user-defined                      condition together with its proof context is translated into
        assumptions and invariants, as well as three kinds                the SMT-LIB format. The result is then passed to an SMT
        of extra invariants: process states, defined process              solver (CVC5 by default).
        state variables, and defined stabilized process state                 If the solver returns sat, the requirement is violated and
        variables.                                                        a counterexample is produced.
    3) Optional. This group consists of the extra invariants                  If the solver returns unsat, the verification condition is
        for process state transition conditions.                          proven valid and added to the list of verified conditions.
    By default, only base and advanced lemmas are used.                       If the solver returns unknown, the system attempts to
Optional lemmas must be enabled separately. Additionally,                 refine the proof context. In this case, additional lemmas may
be introduced into the context, and the verification condition                 51–57. [Online]. Available: https://doi.org/10.1109/SIBCON.2007.
is translated again and resubmitted to the SMT solver. If                      371297
further expansion is not possible or has been disabled,                    [2] V. E. Zyubin, T. V. Liakh, and A. S. Rozov, “Reflex
the original verification condition and its proof context                      language: a practical notation for cyber-physical systems,” System
                                                                               Informatics, no. 12, pp. 85–104, 2018. [Online]. Available:
are printed and added to the list of unverified verification                   https://doi.org/10.31144/si.2307-6410.2018.n12.p85-104
conditions for manual proof in a theorem prover such as
Isabelle/HOL.                                                              [3] A. Bastrykina, “Reflex translator,” https://github.com/a-bastrykina/
                                                                               reflex-translator-diploma, 2020.
                     VII. C ONCLUSION                                      [4] R. Hähnle and M. Huisman, “Deductive software verification: from
     This paper has presented an approach to automating the                    pen-and-paper proofs to industrial tools,” Computing and Software
                                                                               Science: State of the Art and Perspectives, pp. 345–373, 2019.
proof of verification conditions in the context of deductive                   [Online]. Available: https://doi.org/10.1007/978-3-319-91908-9 18
verification for Reflex programs. The work addresses a
critical bottleneck in the verification process: the large                 [5] D. von Oheimb, “Hoare logic for java in isabelle/hol,” Concurrency
                                                                               and Computation: Practice and Experience, vol. 13, no. 13, pp. 1173–
number of verification conditions generated for realistic                      1214, 2001. [Online]. Available: https://doi.org/10.1002/cpe.598
industrial programs, which makes manual proof impractical.
                                                                           [6] N. Schirmer, “A verification environment for sequential imperative
     We have proposed three complementary extensions to                        programs in isabelle/hol,” in Logic for Programming, Artificial
our previously developed verification condition generator.                     Intelligence, and Reasoning, F. Baader and A. Voronkov, Eds.
First, we introduced a redesigned annotation language                          Berlin, Heidelberg: Springer Berlin Heidelberg, 2005, pp. 398–414.
that allows engineers to specify program properties in a                       [Online]. Available: https://doi.org/10.1007/b106931
structured and expressive manner, supporting both a default                [7] R. Krebbers, “An operational and axiomatic semantics for non-
logical notation and integration with external languages such                  determinism and sequence points in c,” vol. 49, no. 1, p. 101–112, Jan.
as Isabelle/HOL. Second, we developed a mechanism for                          2014. [Online]. Available: https://doi.org/10.1145/2578855.2535878
automatically generating structure-based invariants derived                [8] A. D. Ishchenko and I. S. Anureev, “Verification condition generator
from the control-flow graph of the program, including                          for revised reflex language using isabelle/hol,” in 2025 IEEE 26th
invariants describing process states, variable values in                       International Conference of Young Professionals in Electron Devices
                                                                               and Materials (EDM). IEEE, 2025, pp. 1440–1445.
stabilized and non-stabilized states, and process state
transition conditions. Third, we integrated SMT solvers                    [9] T. Parr, The Definitive ANTLR 4 Reference, 2nd ed. Pragmatic
into the verification workflow by translating verification                     Bookshelf, 2013. [Online]. Available: http://digital.casalini.it/
                                                                               9781680505016
conditions into the SMT-LIB format and incorporating a
layered system of auxiliary lemmas to support automated                   [10] A. Ishchenko, “Reflex grammar,” https://github.com/bearhug15/
reasoning.                                                                     ReflexVCG/blob/master/src/main/java/su/nsk/iae/reflex/antlr/
                                                                               NewReflex.g4, 2024.
     The modified VCG architecture combines these elements
into a unified verification pipeline. Starting from an                    [11] G. T. Leavens, A. L. Baker, and C. Ruby, “Jml: A notation for detailed
                                                                               design,” pp. 175–188, 1999.
annotated program, it constructs a control-flow graph,
processes user annotations, generates additional invariants,              [12] P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy, and
and produces verification conditions. Each condition is then                   V. Prevosto, “Acsl: Ansi/iso c specification,” 2021.
translated into an SMT query together with a tailored                     [13] I. Anureev, N. Garanina, T. Liakh, A. Rozov, V. Zyubin, and
proof context. The solver’s response determines whether the                    S. Gorlatch, “Two-step deductive verification of control software
                                                                               using reflex,” in International Andrei Ershov Memorial Conference
condition is proved, a counterexample is found, or further                     on Perspectives of System Informatics. Springer, 2019, pp. 50–63.
refinement is needed, with unverified conditions deferred to
interactive theorem provers like Isabelle/HOL.                            [14] C. Barrett and C. Tinelli, “Satisfiability modulo theories,” pp. 305–
                                                                               343, 2018.
     This work represents a step toward making deductive
verification more practical for industrial process-oriented               [15] R. Nieuwenhuis, A. Oliveras, and C. Tinelli, “Solving sat and sat
programs by reducing the manual effort required to prove                       modulo theories: From an abstract davis–putnam–logemann–loveland
                                                                               procedure to dpll (t),” Journal of the ACM (JACM), vol. 53, no. 6, pp.
verification conditions. The proposed approach leverages                       937–977, 2006.
both user-provided specifications and automatically derived
                                                                          [16] A. Reynolds, C. Tinelli, A. Goel, S. Krstić, M. Deters, and C. Barrett,
structural properties, combining them with the power of                        “Quantifier instantiation techniques for finite model finding in smt,”
modern SMT solvers.                                                            pp. 377–391, 2013.
     Future work will focus on the practical implementation
                                                                          [17] C. Barrett, A. Stump, C. Tinelli et al., “The smt-lib standard: Version
and experimental evaluation of the proposed system. This                       2.0,” vol. 13, p. 14, 2010.
includes implementing the annotation parser, invariant
                                                                          [18] L. De Moura and N. Bjørner, “Z3: An efficient smt solver,” in
generator, and SMT-LIB translator, followed by a                               International conference on Tools and Algorithms for the Construction
comprehensive evaluation on a suite of Reflex programs of                      and Analysis of Systems. Springer, 2008, pp. 337–340.
varying complexity. We also plan to investigate additional
                                                                          [19] C. Barrett, C. L. Conway, M. Deters, L. Hadarean, D. Jovanović,
sources of automatically generated invariants, refine the                      T. King, A. Reynolds, and C. Tinelli, “cvc4,” in International
lemma selection strategy to improve solver performance, and                    Conference on Computer Aided Verification. Springer, 2011, pp.
explore techniques for handling more complex verification                      171–177.
conditions that currently require interactive proof.                      [20] H. Barbosa, C. Barrett, M. Brain, G. Kremer, H. Lachnitt, M. Mann,
                           R EFERENCES                                         A. Mohamed, M. Mohamed, A. Niemetz, A. Nötzli et al., “cvc5:
                                                                               A versatile and industrial-strength smt solver,” in International
 [1] V. E. Zyubin, “Hyper-automaton: a model of control algorithms,” in        Conference on Tools and Algorithms for the Construction and Analysis
     2007 Siberian Conference on Control and Communications, 2007, pp.         of Systems. Springer, 2022, pp. 415–442.
