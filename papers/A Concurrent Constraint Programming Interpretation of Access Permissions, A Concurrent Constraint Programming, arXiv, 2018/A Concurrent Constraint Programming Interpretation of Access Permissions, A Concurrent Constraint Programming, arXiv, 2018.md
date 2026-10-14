                                         Under consideration for publication in Theory and Practice of Logic Programming                       1




                                                      A Concurrent Constraint Programming
                                                       Interpretation of Access Permissions
arXiv:1802.04695v1 [cs.LO] 13 Feb 2018




                                                                                  CARLOS OLARTE
                                                                   ECT, Universidade Federal Rio Grande do Norte, Brasil
                                                                             E-mail: carlos.olarte@gmail.com

                                                                                 ELAINE PIMENTEL
                                                                  DMAT, Universidade Federal Rio Grande do Norte, Brasil
                                                                          E-mail: elaine.pimentel@gmail.com

                                                                                   CAMILO RUEDA
                                                                   DECC, Pontificia Universidad Javeriana Cali, Colombia
                                                                            E-mail: camilo.rueda@gmail.com

                                                         submitted 1 December 2016; revised 18 July 2017; accepted 1 February 2018



                                                                                        Abstract
                                         A recent trend in object oriented (OO) programming languages is the use of Access Permissions
                                         (APs) as an abstraction for controlling concurrent executions of programs. The use of AP source
                                         code annotations defines a protocol specifying how object references can access the mutable state of
                                         objects. Although the use of APs simplifies the task of writing concurrent code, an unsystematic use
                                         of them can lead to subtle problems. This paper presents a declarative interpretation of APs as Linear
                                         Concurrent Constraint Programs (lcc). We represent APs as constraints (i.e., formulas in logic) in
                                         an underlying constraint system whose entailment relation models the transformation rules of APs.
                                         Moreover, we use processes in lcc to model the dependencies imposed by APs, thus allowing the
                                         faithful representation of their flow in the program. We verify relevant properties about AP programs
                                         by taking advantage of the interpretation of lcc processes as formulas in Girard’s intuitionistic linear
                                         logic (ILL). Properties include deadlock detection, program correctness (whether programs adhere
                                         to their AP specifications or not), and the ability of methods to run concurrently. By relying on a
                                         focusing discipline for ILL, we provide a complexity measure for proofs of the above mentioned
                                         properties. The effectiveness of our verification techniques is demonstrated by implementing the
                                         Alcove tool that includes an animator and a verifier. The former executes the lcc model, observing
                                         the flow of APs and quickly finding inconsistencies of the APs vis-à-vis the implementation. The
                                         latter is an automatic theorem prover based on ILL. This paper is under consideration for publication
                                         in Theory and Practice of Logic Programming (TPLP).
                                         KEYWORDS: Access Permissions, Concurrent Constraint Programming, Linear Logic, Focusing




                                                                                    1 Introduction
                                         Reasoning about concurrent programs is much harder than reasoning about sequential ones.
                                         Programmers often find themselves overwhelmed by the many subtle cases of thread inter-
                                         actions they must be aware of to decide whether a concurrent program is correct or not. In
                                         order to ensure program reliability, the programmer needs also to figure out the right level
2                               Olarte, Pimentel and Rueda

of thread atomicity to avoid race conditions, cope with mutual exclusion requirements and
guarantee deadlock freeness.
   All these problems are aggravated when software designers write programs using an
object oriented (OO) language and use OO strategies to design their programs. In an OO
program, objects can have multiple references (called aliases) that can modify local content
concurrently. This significantly increases the complexity of the design of sound concurrent
programs. For instance, data race conditions arise when two object references read and
write concurrently from/to an object memory location. To cope with data races, one could
simply place each object access within an atomic block, but this would affect negatively
program performance. A better strategy could be to lock just the objects that are shared
among threads. However, it then becomes hard to estimate which objects should be shared
and which locations should be protected by locks just by looking at the program text.
   Languages like Æminium (Stork et al. 2009), Plaid (Sunshine et al. 2011) and Mezzo
(Pottier and Protzenko 2013) propose a strategy to design sound and reliable concurrent
programs based on the concept of access permissions (APs) (Boyland et al. 2001). APs
are abstractions about the aliased access to an object content and they are annotated in the
source code. They permit a direct control of the access to the mutable state of an object.
Making explicit the access to a shared mutable state facilitates verification and enables
parallelization of code. For instance, a unique AP, describing the case when only one refer-
ence to a given object exists, enforces absence of interference and simplifies verification; a
shared AP, describing the case when an object may be accessed and modified by multiple
references, allows for concurrent executions but makes verification trickier.
   Although APs greatly help to devise static strategies for correct concurrent sharing of
objects, the interactions resulting from dynamic bindings (e.g., aliasing of variables) might
still lead to subtle difficulties. Indeed, it may happen that apparently correct permission
assignments in simple programs lead to deadlocks.
   We propose a Linear Concurrent Constraint Programming (lcc) (Fages et al. 2001) ap-
proach for the verification of AP annotated programs. Concurrent Constraint Programming
(ccp) (Saraswat et al. 1991; Saraswat 1993) is a simple model for concurrency that extends
and subsumes both Concurrent Logic Programming and Constraint Logic Programming.
Agents in ccp interact by telling constraints (i.e., formulas in logic) into a shared store
of partial information and synchronize by asking if a given information can be deduced
from the store. In lcc, constraints are formulas in Girard’s intuitionistic linear logic (ILL)
(Girard 1987) and ask agents are allowed to consume tokens of information from the store.
   We interpret AP programs as lcc agents that produce and consume APs when evolving.
We use constraints to keep information about APs, object references, object fields, and
method calls. Moreover, the constraint entailment relation allows us to verify compliance
of methods and arguments to their AP signatures. The constraint system specifies also how
the APs can be transformed during the execution of the program.
   We are able to verify AP programs by exploiting the declarative view of lcc agents
as formulas in ILL. The proposed program verification includes: (1) deadlock detection;
(2) whether it is possible for methods to be executed concurrently or not; and (3) whether
annotations adhere to the intended semantics associated with the flow of APs or not.
   The key for this successful specification and analysis of AP annotations as ILL formulas
is the use of a linear logic’s focusing discipline (Andreoli 1992). In fact, by using focusing
       A Concurrent Constraint Programming Interpretation of Access Permissions              3

we can identify which actions need to interact with the environment or not, either for
choosing a path to follow, or for waiting for a guard to be available (e.g., the possession
of an AP on a given object). This gives a method for measuring the complexity of focused
ILL (ILLF) proofs in terms of actions, hence establishing an upper bound of the complexity
for verifying the above mentioned properties. Moreover, as shown in (Olarte and Pimentel
2017), focusing guarantees that the interpretation of lcc processes as ILL formulas is
adequate at the highest level (full completeness of derivations): one step of computation (in
lcc) corresponds to one step of logical reasoning. Hence, our encodings of AP annotations
as ILL formulas is faithful w.r.t. the proposed lcc model.
   The contributions of this work are three-fold: (1) the definition of a logical semantics for
APs, (2) provision of a procedure for the verification of the above mentioned properties as
well as a complexity analysis for it, and (3) the implementation of the verification approach
as the Alcove tool (http://subsell.logic.at/alcove2/). The logical structure
we impose on APs thus allows us to formally reason about the behavior of AP based
programs and give a declarative account of the meaning of these annotations. It is worth
noticing that we are not considering a specific AP based language. Instead, we give a
logical meaning to the machinery of APs and type states (see Section 7) present in different
languages. This allows us to provide static analyses independent of the runtime system
at hand. For concreteness, we borrow the AP model of Æminium (Stork et al. 2009), a
concurrent OO programming language based on the idea of APs.
   The paper is organized as follows. Section 2 presents the syntax of the AP based lan-
guage used here and Section 3 recalls lcc. Section 4 presents the interpretation of AP
programs as lcc agents. We also show how the proposed model is a runnable specifica-
tion that allows observing the flow of a program’s permissions. We implemented this model
as the Alcove LCC Animator explained in Section 4.3. Section 5 describes our approach
to program verification and its implementation as the Alcove LL prover. It also presents a
complexity analysis of the proposed verification. Two compelling examples of our frame-
work are described in Section 6: the verification of a critical zone management system and
a concurrent producer-consumer system. Section 7 concludes the paper.
   A preliminary short version of this paper was published in (Olarte et al. 2012). The
present paper gives many more examples and explanations and provides precise technical
details. In particular, in this paper we identify the fragment of lcc (and ILL) required
for the specification of AP programs and we show that this fragment allows for efficient
verification techniques. Moreover, the language (and analyses) considered here take into
account Data Group Permissions (Leino 1998; Stork et al. 2009), a powerful abstraction
that adds application level dependencies without sacrificing concurrency (see Section 2.1).


                  2 Access Permissions in Object Oriented Programs
We start with an intuitive description of access permissions and data group access permis-
sions. In Section 2.2, we give a formal account of them.
   Access permissions (APs) are abstractions describing how objects are accessed. Assume
a variable x that points to the object o. A unique permission to the reference x guarantees
that x is the sole reference to object o. A shared permission provides x with reading and
modifying access to o, which allows other references to o (called aliases) to exist and to
4                                 Olarte, Pimentel and Rueda
                                                                            none(c)         none(s)



                                                                         new Collection    new Stats
     1   class stats {...} // Definition of statistics
                                                                                 unq(c)
     2   class collection { // Collection of elements
     3    collection() none(this) => unq(this) {...}//constructor             Sort
     4    sort() unq(this) => unq(this) {...}                                    unq(c)
                                                                                                unq(s)
     5    print() imm(this) => imm(this) {...}
     6    compStats(stats s) imm(this),unq(s) => imm(this),unq(s)            split
               {...}                                                     imm(c) imm(c)
     7    removeDuplicates() unq(this) => unq(this){...}}
     8   main() {                                               Print                      CompStats

     9     let collection c, stats s in                                  imm(c) imm(c)
    10       c := new collection()
    11       s := new stats()                                                 join
    12       c.sort()
                                                                                 unq(c)
    13       c.print()
    14       c.compStats(s)                                             removeDuplicates

    15       c.removeDuplicates()
    16     end}                                                             unq(c)          unq(s)




          Fig. 1: Example of an AP annotated program and its permission flow graph.


read from it or to modify it. The immutable permission provides x with read-only access
to o, and allows any other reference to o to exist and to read from it. Let us use a simple
example to explain APs and the concurrency-by-default behavior (Stork et al. 2009) they
offer. Figure 1 shows a program, taken and slightly modified from (Stork et al. 2009), that
operates over a collection of elements. Starting at line 8, the program creates an object
of type collection at line 10 and an object of type stats at line 11. The program sorts
the collection c at line 12, and prints it at line 13. It computes some statistics at line 14,
and removes duplicates from the collection at line 15. Lines 3-7 declare the signatures
for the methods. The constructor builds a unique reference to a new collection at line
3. Methods sort and removeDuplicates modify the content of the collection and they
require a unique reference to it. Method compStats requires and returns an immutable
(read-only) AP to the collection c and a unique AP to the parameter s.
   Given the AP signature of theses methods, the AP dataflow is computed where: (1)
conflicting accesses are ordered according to the lexical order of the program; and (2) non-
conflicting instructions can be executed concurrently. For instance, methods in lines 12
and 13 cannot be executed concurrently (since sort requires a unique permission ) and
methods in lines 13 and 14 can be executed concurrently (since both methods require an
immutable permission on c). Finally, the method in line 15 cannot be executed concur-
rently with compStats since removeDuplicates requires a unique AP. Hence, what we
observe is that the unique permission returned by the constructor is consumed by the call
of method sort. Once this method terminates, the unique permission can be split into two
immutable permissions, and methods print and compStats can be executed concurrently.
Once both methods have finished, the immutable APs are joined back into a unique AP,
and the method removeDuplicates can be executed.


                           2.1 Share Permissions and Data Groups
As we just showed, unique permissions can be split into several immutable APs to allow
multiple references to read, simultaneously, the state of an object. Therefore, from the AP
        A Concurrent Constraint Programming Interpretation of Access Permissions           5

annotations, the programming language can determine, automatically, the instructions that
can be executed concurrently and those that need to be executed sequentially (Figure 1).
   In the case of share APs, several references can modify concurrently the state of the
same object. Hence, the programmer needs additional control structures to make explicit
the parts of the code that can be executed concurrently. Consider for instance the following
excerpt of code:

   1   let Subject s, Observer o1, Observer o2 in
   2     s := new Subject()
   3     o1 := new Observer(s) // Requires a share permission on s
   4     o2 := new Observer(s)
   5     s.update() // Requires a share permission on s
   6     s.update()



   where the constructor Observer as well as the method update require a share permis-
sion on s. Assume also that the intended behaviour of the program is that the method
update should be executed only after the instantiation of the Observer objects.
   If we were to handle share permissions as we did with immutable permissions in the
previous section, once the new instance of Subject is created in line 2, the unique permis-
sion s has on it can be split into several share permissions. Hence, statements in lines 3
to 6 could be executed concurrently. This means that a possible run of the program may
execute the method update in lines 5 and 6 before instantiating the Observers in lines 3
and 4, which does not comply with the intended behavior of the program.
   Higher-level dependencies in AP programs can be defined by means of Data Groups
(DGs) (Leino 1998) as in (Stork et al. 2009; Stork et al. 2014). Intuitively, a DG represents
a collection of objects and it controls the flow of share permissions on them. For that,
two kinds of Data Group Access Permissions (DGAPs) are defined: an atomic permission
provides exclusive access to the DG, much like a unique AP for objects. Then, working on
an atomic DGAP leads to the sequentialization of the code; on the contrary, a concurrent
DGAP allows other DGAPs to coexist on the same DG. Therefore, a concurrent DGAP
allows for the parallel execution of the code.
   Consider the code in Figure 2, taken and slightly modified (syntactically) from (Stork
et al. 2009). In line 1, the class Subject is declared with a DG parameter dg. This param-
eter is similar to a type parameter (template) in modern OO programming languages. The
method update (line 3) requires a share permission on the DG dg to be invoked. The class
Observer (line 4) is also defined with a DG parameter dg and its constructor requires an
object of type Subjecthdgi.
   The statement grouphgi (line 7) creates a DG and assigns to it an atomic DGAP. The
split(g) instruction consumes such atomic permission on g and splits it into three con-
current DGAP, one per each statement in the block (lines 10,11 and 12). According to the
data dependencies, statements in lines 11 and 12 can be executed concurrently once s is
instantiated in line 10. When the instructions in lines 11 and 12 have terminated, the con-
current DGAPs on g are joined back to an atomic permission on g. When this happens,
the split block in line 13 consumes such permission and splits it into two concurrent
DGAPs so that statements in lines 14 and 15 can be executed concurrently. Hence, DGAPs
enforce a data group dependency between the two blocks (in gray in the figure) of code.
6                                 Olarte, Pimentel and Rueda
                                                                                                      grouphgi
     1   class Subject <dg>{                                                                                atm(g)
     2      Subject() none(this) => unq(this)
     3      update() shr : dg(this) => shr : dg(this)}                                                split(g)

     4   class Observer<dg>{                                                                                conc(g)
     5      Observer(Subject<dg> s) none(this),shr:dg(s)
                                                                                new Subject
                 => unq(this),shr:dg(s)}
     6   main(){                                                                        unq(s)

     7     group<g>
                                                                                   split
     8     let Subject s, Observer o1, Observer o2 in
     9      split(g){                                              shr:g(s)             shr:g(s)
    10         s := new Subject<g>()
                                                             new Observer                           new Observer
    11         o1 := new Observer<g>(s)
    12         o2 := new Observer<g>(s) }                          shr:g(s)             shr:g(s)
    13      split(g){                                                              join
    14         s.update()
                                                                                                            atm(g)
    15         s.update()}
    16     }                                                                   unq(s)                 split(g)


                                                                                                            conc(g)

                                                                                   split

                                                                   shr:g(s)             shr:g(s)

                                                               update                                 update

                                                                    shr:g(s)            shr:g(s)

                                                                                   join
                                                                                                   atm(g)
                                                                               unq(s)




                        Fig. 2: Subjects and Observers with data groups.



                          2.2 An Access Permission Based Language

This section formalizes the syntax we have used in the previous examples. Our language
is based on the core calculus µÆminium (Stork et al. 2014) for Æminium (Stork et al.
2009), an OO programming language where concurrent behavior arises when methods
require non-conflicting APs, as exemplified in the last section. As a core calculus, it focuses
on the mechanisms to control the flow of permissions and it abstracts away from other
implementation details of the language (e.g., control structures). Unlike µÆminium, our
core calculus abstracts away also from: (1) specific implementation details to guarantee
atomicity (e.g., the inatomic statement used in the intermediate code of Æminium to
keep track of entered atomic blocks), (2) mechanisms to define internal data groups, i.e.,
DGs in our language can only be declared in the main function, and (3), we do not consider
class inheritance.
   Programs are built from the syntax in Fig. 3. DGs are declared with grouphg1 , · · · , gn i.
APs on objects can be unique, immutable or none (for null references), and share on the
DG g (shr : g). A program consists of a series of class definitions (CL)  g and a main body.
A class can be parametrized in zero or more DG names (he     g i) and it contains zero or several
fields (F ), constructors (CTR)
                           ] and methods (M       f).
   A class field (attribute) is declared by using a valid type and a field name. Note that a
type is simply an identifier of a class with its respective DG parameters.
   Constructors and methods specify the required permissions for the caller (p(this)) and
the arguments (p(x))
                  g as well as the permissions restored to the environment.
       A Concurrent Constraint Programming Interpretation of Access Permissions               7
       (group decl.)        G    ::=   grouphg1 , · · · , gn i
       (permissions)         p   ::=   unq | shr : g | imm | none
       (programs)            P   ::=   hCL
                                        g maini
       (class decl.)       CL    ::=   class c he g i { F CTR
                                                           ^M    f}
       (types)               T   ::=   chegi
       (field decl.)         F   ::=   · | attr Tg  a
       (method decl.)     CTR    ::=    c(Tg x) none(this), p(x) g ⇒ p(this), p(x)    g {s}
                            M    ::=    m(T g x) p(this), p(x) g ⇒ p(this), p(x) g {s}
       (main)             main   ::=   main {G s}
       (references)          r   ::=   x | x.a | this | this.a
       (righthand side)    rhs   ::=   r | null
       (statements)          s   ::=   let T g x in s end | rhgi := rhs | r.m(e  r) |
                                       r := new che  g i(e
                                                         r) | splithe
                                                                    g i{e
                                                                        s} | {e
                                                                              s}

Fig. 3: Syntax of AP annotated programs. c, m, a, x, g ranges, respectively, over name of
classes, methods, fields, variables and data groups. x    e denotes a possibly empty sequence
of variables x1 , ...., xn . This notation is similarly used for other syntactic categories.


   A reference r can be a variable, the self reference this or a field selection as in x.a. As
for the statements, we have the following:

- The let constructor allows us to create local variables.
- After the assignment rhgi := rhs, both r and rhs point to the same object (or null) as
  follows: (1) if rhs has a unique permission on an object o, then after the assignment, r
  and rhs have a share permission shr : g on o. This explains the need of “hgi” in the
  syntax. As syntactic sugar one could decree that rl := rr means rl hdefaulti := rr
  where default is a predefined DG; (2) if rhs has a shr : g (resp imm) permission on o,
  then r and rhs end with a shr : g (resp imm) permission on o. Finally, (4) if rhs = null
  or it is a null reference, then r and rhs end with a none permission. We note that in
  assignments, the right and left hand sides are references. We do not lose generality since
  it is possible to unfold more general expressions by using local variables.
- An object’s method can be invoked by using a reference to it with the right number of
  parameters as in r.m(e r). We assume that in a call to a method (or constructor), the actual
  parameters are references (i.e., variables, including this, and attributes) and not arbi-
  trary expressions. Since we have parameters by reference, we assume that the returned
  type is void and we omit it in the signature.
- A new instance of a given class is created by r := new che       g i(e
                                                                       r) where we specify the
  required DG parameters ge and actual parameters (e    r) of the constructor.
- For each gi , splithg1 , ..., gn i{s1 · · · sm } consumes an atomic or a concurrent DGAP
  on gi . Then, it splits each of such DGAPs into m concurrent DGAPs (one per each
  statement in the block). Once the statements in the block have finished their execution,
  the concurrent DGAPs created are consumed and the original DGAPs are restored.
- Finally, we can compose several statements in a block {s1 , .., sn } where the concurrent
  execution of statements is allowed according to the data dependencies imposed by the
  APs and the DGAPs: once si has successfully consumed its needed permissions, the
  execution of si+1 may start concurrently. Moreover, if si cannot acquire the needed
  permissions, it must wait until such permissions are released by the preceding statements.
8                                 Olarte, Pimentel and Rueda

Remark 2.1 (Circular Recursive Definitions)
The AP language in Fig. 3 allows us to write recursive methods. However, the language
lacks control structures (e.g. if-then-else statements) to specify base cases in recursive def-
initions. This language must be understood as a core language to specify the AP mecha-
nisms and not as a complete OO programming language implementing the usual data and
control structures. Hence, we shall assume that there are no circular recursive definitions in
the source program. Due to the lack of control structures, this is an unavoidable restriction
to guarantee termination of the analyzes in Sections 4 and 5.

Dependencies and Execution. Recall that blocks of sentences are enclosed by curly brack-
ets. Hence, we say that a sentence s occurs in a block if s is inside the braces of that block.
Definition 1 (Conflicts and Dependencies)
Let si and sj be statements that occur in the same block. We say that si and sj are in
conflict if both statements use an object o in conflicting modes, i.e., either (1) si or sj
require a unique permission on o, (2) si requires a share permission on o and sj requires
an immutable permission on o, or (3) si and sj require a share permission on different
data groups. Two blocks splithe      g i{s1 , ..., sn } and splithge0 i{s01 , ..., s0m } occurring in
the same block are in conflict if ge ∩ ge0 6= ∅.
   The semantics of AP programs share with other semantics for OO languages (see e.g.,
(Igarashi et al. 2001)) the rules and contexts to keep track of references, objects as well as
lookup tables to identify class names, fields and methods with their respective definitions.
Additionally, in the case of AP programs, the semantics relies on an evaluation context
to keep track of the DGs created as well as the available APs in the system. This con-
text plays an important role in the semantic rules: a statement s is executed only if the
evaluation context possesses all the permissions required by s. Moreover, in order to allow
parallel executions, once s consumes the needed permissions, the next statement (in the lex-
ical order of the program) is enabled for execution. For instance, in a block of statements
s1 , ..., sn , the execution starts by enabling s1 . Each enabled statement si checks whether
the required permissions are available. If this is the case, such permissions are consumed,
si starts its execution and the next statement si+1 is enabled. When si terminates its exe-
cution, the consumed permissions are restored to the environment. On the other side, if the
permissions required by si are not available, si must wait until the needed permissions are
released/produced by the preceding statements. Hence, non-conflicting blocks lead to con-
current executions and conflicting blocks are sequentialized according to the lexical order
of the program (as in Figures 1 and 2).
   The reader may refer to (Stork et al. 2014, Sections 3.2 and 3.3) for the semantic rules of
µÆminium that can be easily adapted to the sublanguage in Figure 3. In Section 4 we give
a precise definition of the needed evaluation contexts by using constraints (i.e., formulas
in logic) and the state transformation by means of concurrent processes consuming and
producing those constraints.

                      3 Linear Concurrent Constraint Programming
Concurrent Constraint Programming (ccp) (Saraswat and Rinard 1990; Saraswat et al.
1991; Saraswat 1993) (see a survey in (Olarte et al. 2013)) is a model for concurrency that
        A Concurrent Constraint Programming Interpretation of Access Permissions                            9
                                                                Γ −→ c
                                                >R                       1L                      1R
          c −→ c init                 Γ −→ >                   Γ, 1 −→ c                  −→ 1

      Γ, c1 , c2 −→ c            Γ1 −→ c1 Γ2 −→ c2             Γ, ci −→ c            Γ −→ c1 Γ −→ c2
                      ⊗L                             ⊗R                     NLi                      NR
     Γ, c1 ⊗ c2 −→ c              Γ1 , Γ2 −→ c1 ⊗ c2         Γ, c1 Nc2 −→ c             Γ −→ c1 Nc2

  Γ1 −→ c1 Γ2 , c2 −→ c             Γ, c1 −→ c2           Γ, c1 −→ c Γ, c2 −→ c         Γ −→ ci
                         (L                     (R                              ⊕L                 ⊕Ri
  Γ1 , Γ2 , c1 ( c2 −→ c           Γ −→ c1 ( c2               Γ, c1 ⊕ c2 −→ c         Γ −→ c1 ⊕ c2

  Γ, c −→ d x ∈ / f v(Γ, d)         Γ −→ c[t/x]              Γ, c[t/x] −→ d          Γ −→ c x ∈
                                                                                              / f v(Γ)
                            ∃L                  ∃R                          ∀L                         ∀R
        Γ, ∃x.c −→ d                Γ −→ ∃x.c                Γ, ∀x.c −→ d               Γ −→ ∀x.c

         Γ −→ d                     Γ, ! c, ! c −→ d           Γ, c −→ d                ! Γ −→ d prom
                    W                                C                     D
        Γ, ! c −→ d                  Γ, ! c −→ d               Γ, ! c −→ d              ! Γ −→! d


Fig. 4: Rules for Intuitionistic Linear Logic (ILL). f v(c) (resp. f v(Γ)) denotes the set of
free variables of formula c (resp. multiset Γ). Γ, ∆ denote multisets of formulas.


combines the traditional operational view of process calculi with a declarative view based
on logic. This allows ccp to benefit from the large set of reasoning techniques of both
process calculi and logic.
   Agents in ccp interact with each other by telling and asking information represented as
constraints to a global store. The type of constraints is parametric in a constraint system
(Saraswat et al. 1991) that specifies the basic constraints that agents can tell and ask during
execution. Such systems can be specified as Scott information systems as in (Saraswat and
Rinard 1990; Saraswat et al. 1991) or they can be specified in a suitable fragment of logic
(see e.g., (Fages et al. 2001; Nielsen et al. 2002)).
   The basic constructs (processes) in ccp are: (1) the tell agent c, which adds the con-
straint c to the store, thus making it available to the other processes. Once a constraint
is added, it cannot be removed from the store (i.e., the store grows monotonically). And
(2), the ask process c → P , that queries if c can be deduced from the information in the
current store; if so, the agent behaves like P , otherwise, it remains blocked until more in-
formation is added to the store. In this way, ask processes define a simple and powerful
synchronization mechanism based on entailment of constraints.
   Linear Concurrent Constraint Programming (lcc) (Fages et al. 2001) is a ccp-based
calculus that considers constraint systems built from a fragment of Girard’s intuitionistic
linear logic (ILL) (Girard 1987). The move to a linear discipline permits ask agents to
consume information (i.e., constraints) from the store.
Definition 2 (Linear Constraint Systems (Fages et al. 2001))
A linear constraint system is a pair (C, `) where C is a set of formulas (linear constraints)
built from a signature Σ (a set of function and relation symbols), a denumerable set of
variables V and the following ILL operators: multiplicative conjunction (⊗) and its neu-
tral element (1), the existential quantifier (∃) and the exponential bang (!). We shall use
c, c0 , d, d0 , etc, to denote elements of C. Moreover, let ∆ be a set of non-logical axioms of
the form ∀e     x.[c ( c0 ] where all free variables in c and c0 are in x
                                                                        e. We say that d entails c,
written as d ` c, iff the sequent ! ∆, d −→ c is provable in ILL (Figure 4).
   The connective ⊗ allows us to conjoin information in the store and 1 denotes the empty
store. As usual, existential quantification is used to hide information. The exponential ! c
represents the arbitrary duplication of the resource c. The entailment d ` c means that the
10                               Olarte, Pimentel and Rueda

information c can be deduced from the information represented by constraint d, possibly
using the axioms in the theory ∆. This theory gives meaning to (uninterpreted) predicates.
For instance, if R is a transitive relation, ∆ may contain the axiom ∀x, y, z.[R(x, y) ⊗
R(y, z) ( R(x, z)].
   We assume that “! ” has a tighter binding than ⊗ and so, we understand ! c1 ⊗c2 as (! c1 )⊗
c2 . For the rest of the operators we shall explicitly use parenthesis to avoid ambiguities.
                                                               N
Given a finite set of indexes I = {1, ..., n}, we shall use       Fi to denote the formula
                                                                i∈I
F1 ⊗ · · · ⊗ Fn .
   We note that, according to Definition 2, constraints are built from the ILL fragment ⊗, 1,
∃ ,!. We decided to include all ILL connectives in Figure 4 (linear implication (, additive
conjunction N and disjunction ⊕, the universal quantifier ∀ and the unit >) since those
connectives will be used to encode lcc processes in Section 5.


                              3.1 The Language of Processes
Similar to other ccp-based calculi, lcc, in addition to tell and ask agents, provides con-
structs for parallel composition, hiding of variables, non-deterministic choices and process
definitions and calls. More precisely:

Definition 3 (lcc agents (Fages et al. 2001))
Agents in lcc are built from constraints as follows:
                                  X
                P, Q, ... ::= c |   ∀exi (ci → Pi ) | P k Q | ∃e
                                                               x(P ) | p(e
                                                                         x)
                                  i∈I

A lcc program takes the form D.P where D is a set of process definitions of the form
      ∆
p(e
  y ) = P where all free variables of P are in the set of pairwise distinct variables ye. We
assume D to have a unique process definition for every process name.

   Let us give some intuitions about the above constructs. The tell agent c adds constraint
c to the current store d producing the new store d ⊗ c.
                                       P
   Consider the guarded choice Q =        ∀xei (ci → Pi ) where I is a finite set of indexes.
                                        i∈I
Let j ∈ I, d be the current store and θ be the substitution [e    t/xej ] where et is a sequence
of terms. If d ` d0 ⊗ cj θ for some d0 , then Q evolves into Pj [e t/xej ] and consumes cj θ. If
none of the guards ci can be deduced from d, the process Q blocks until more information
is added to the store. Moreover, if many guards can be deduced, one of the alternatives is
                                                                                             P
non-deterministically chosen for execution. To simplify the notation, we shall omit “ ”
   P                                                                                        i∈I
in     ∀xei (ci → Pi ) when I is a singleton; if the sequence of variables xe is empty, we shall
   i∈I                                                                                       P
write c → P instead of ∀e x(c → P ); moreover, if |I| = 2, we shall use “+” instead of “ ”
as in c1 → P1 + c2 → P2 .

  The interleaved parallel composition of P and Q is denoted by P k Q. We shall use
Πi∈I Pi to denote the parallel composition P1 k · · · k Pn , where I = {1, 2, ..., n}. If
I = ∅, then Πi∈I Pi = 1 .
  The agent ∃ex(P ) behaves like P and binds the variables x
                                                           e to be local to it. The processes
          A Concurrent Constraint Programming Interpretation of Access Permissions                            11

∃e
 x(P ) and ∀ex(c → P ), as well as the constraint ∃e   x(c), bind the variables x e in P and c.
We shall use fv (P ) and fv (c) to denote, respectively, the set of free variables of P and c.
                                                                      ∆
  Finally, given a process declaration of the form p(e
                                                     y ) = P , p(e
                                                                 x) evolves into P [e
                                                                                    x/e
                                                                                      y ].


                                        3.2 Operational Semantics
Before giving a formal definition of the operational semantics of lcc agents, let us give an
example of how processes evolve. For that, we shall use hP ; ci −→ hP 0 ; c0 i to denote that
the agent P under store c evolves into the agent P 0 producing the store c0 . This notation
will be precisely defined shortly.

Example 3.1 (Consuming Permissions)
Let us assume a constraint system with predicates ref/3, ct/2; constant symbols unq,
imm, none, 0, nil ; function symbol s (successor); and equipped with the axiom:

          ∆ = ∀x, o.[ref(x, o, imm) ⊗ ct(o, s(0)) ( ref(x, o, unq) ⊗ ct(o, s(0))]

Informally, ∆ says that an imm permission can be upgraded to unq if there is only one
reference pointing to o.
   Consider now the processes
                        P1    =    ref(x, ox , imm) ⊗ ct(ox , s(0))
                        P2    =    ref(y, oy , imm) ⊗ ref(z, oy , imm) ⊗ ct(oy , s(s(0)))
                        Q     =    ∀o(ref(x, o, unq) ⊗ ct(o, s(0)) → Q0 )
                        Q0    =    ref(x, nil, none) ⊗ ct(o, 0 )
                        R     =    ∀o(ref(y, o, unq) → R0 )

Roughly, P1 adds to the store the information required to state that x points to ox with
permission imm and that there is exactly one reference to ox . P2 states that there are two
references (y and z) pointing to the same object oy . Process Q, in order to evolve, requires
x to have a unique permission on ox . Finally, R is asking whether y has a unique permission
on a given object o to execute R0 (not specified here).
   Starting from the configuration hP1 k P2 k Q k R; 1i, we observe the derivation below:
    (1)       hP1 k P2 k Q k R; 1i
    (2)    −→ hP1 k Q k R; 1 ⊗ ref(y, oy , imm) ⊗ ref(z, oy , imm) ⊗ ct(oy , s(s(0)))i
    (3)    −→ hQ k R; 1 ⊗ ref(y, oy , imm) ⊗ ref(z, oy , imm) ⊗ ct(oy , s(s(0))) ⊗ ref(x, ox , imm) ⊗ ct(ox , s(0))
    (4)    −→ hQ0 [ox /o] k R; ref(y, oy , imm) ⊗ ref(z, oy , imm) ⊗ ct(oy , s(s(0)))i
    (5)    −→ hR; ref(y, oy , imm) ⊗ ref(z, oy , imm) ⊗ ct(oy , s(s(0))) ⊗ ref(x, nil , none) ⊗ ct(ox , 0 )i

From the initial store 1, neither Q nor R can deduce their guards and they remain blocked
(line 1). Tell processes P1 (line 3) and P2 (line 2) evolve by adding information to the
store. Let d (resp. d0 ) be the store in the configuration of line 3 (resp. line 4) and c be
the guard of the ask agent Q. We note that d ` d0 ⊗ c[ox /o]. Recall that checking this
entailment amounts to prove in ILL the sequent !∆, d −→ d0 ⊗ c[ox /o] (Definition 2).
In this case, the axiom ∆ allows us to transform ref(x, ox , imm) ⊗ ct(ox , s(0)) into
ref(x, ox , unq)⊗ct(ox , s(0)). Hence, Q reduces to the tell agent Q0 [ox /o] and consumes
part of the store leading to the store d0 in line 4. In line 5, Q0 [ox /o] adds more information
to the store, namely, x points to null and there are no references pointing to ox . Note that
R remains blocked since the guard ref(y, o, unq) cannot be entailed.
12                                    Olarte, Pimentel and Rueda
                                                  y (d0 ⊗ ci [e
                                             d ` ∃e             xi ]), ye ∩ fv (X, Γ, d) = ∅, mgc(d0 , e
                                                              t/e                                      t)
                                  RTELL                                                                    RCHOICE
                                                                                                  x]; d0 i
                                                  P
  hX; Γ, c; di −→ hX; Γ; d ⊗ ci             hX; Γ, i∈I ∀e  xi (ci → Pi ); di −→ hX ∪ ye; Γ, Pi [e
                                                                                                t/e

                                                                    ∆
              ye ∩ X = ye ∩ fv (Γ, d) = ∅                    p(ey ) = P is a process definition
                                                  RLOC                                               RCALL
         hX; Γ, ∃e
                 y (P ); di −→ hX ∪ ye; Γ, P ; di          hX; Γ, p(e
                                                                    x); di −→ hX; Γ, P [e x/ey ]; di

Fig. 5: Operational semantics of lcc. fv (Γ, d) means fv (Γ) ∪ fv (d). fv (X, Γ, d) means
fv (Γ, d) ∪ X. The notion of most general choice (mgc(d0 , e
                                                           t)) is in Definition 4.


Operational Semantics Let us extend the processes-store configurations used in Example
3.1 to consider configurations of the form hX; Γ; ci. Here X is the set of local (hidden)
variables in Γ and c, Γ is a multiset of processes of the form P1 , ..., Pn representing the
parallel composition P1 k · · · k Pn , and c represents the current store. In what follows, we
shall indistinguishably use the notation of multiset as parallel composition of processes.
   The transition relation −→ defined on configurations is the least relation satisfying the
rules in Figure 5. We shall use −→∗ to denote the reflexive and transitive closure of −→.
It is easy to see that rules RTELL , RLOC and RCALL realize the behavioral intuition
given in the previous section. Let us explain the Rule RCHOICE . Recall that the process
P
    ∀xei (ci → Pi ) executes Pj [e
                                 t/e
                                   xj ] if cj [e
                                               t/e
                                                 xi ] can be deduced from the current store d,
i∈I
i.e., d ` d0 ⊗ cj [e
                   t/e
                     x]. Moreover, the constraint cj [e
                                                      t/e
                                                        x] is consumed from d leading to the
new store d . Hence, d0 must be the most general choice in the following sense:
             0


Definition 4 (Most general choice (mgc) (Martinez 2010; Haemmerlé 2011))
Consider the entailment d ` ∃e y (e ⊗ c[e
                                        t/e x]) and assume that ye ∩ f v(d) = ∅. Assume also
              0     0
that d ` ∃e           x]) for an arbitrary e0 and e
          y (e ⊗ c[t /e
                   e                               t0 . We say that e and e
                                                                          t are the most general
choices, notation mgc(e, t), whenever e ` e implies e ` e0 and c[e
                          e               0
                                                                         x] ` c[e
                                                                       t/e       t0 /e
                                                                                     x].

   The mgc requirement in rule RCHOICE prevents from an unwanted weakening of the
store. For instance, consider the ask agent Q = c → P . We know that ! c entails c ⊗ 1 (i.e.,
! c ` c ⊗ 1). Hence, without the mgc condition, Q may consume ! c leading to the store 1.
This is not satisfactory since Q did not consume the minimal information required to entail
its guard. In this particular case, we have to consider the entailment ! c ` ! c ⊗ c where
Q can entail its guard and the store remains the same. For further details, please refer to
(Haemmerlé 2011).

Sequential Composition In the subsequent sections we shall use the derived operator P ; Q
that delays the execution of Q until P signals its termination. This operator can be encoded
in lcc as follows. Let z be a variable that does not occur in P nor in Q and let sync(·)
be an uninterpreted predicate symbol that does not occur in the program. The process
P ; Q is defined as ∃z(C[[P ]]z k sync(z) → Q) where [[·]]z is in Figure 6. Intuitively,
C[[P ]]z adds the constraint sync(z) to signal the termination of P . Then, the ask agent
sync(z) → Q reduces to Q. Note that in a parallel composition P k R, one has to
wait for the termination of both P and R before adding the constraint sync(z). For that,
C[[P k R]]z creates fresh variables w1 and w2 to signal the termination of, respectively, P
and R. Then, it adds sync(z) only when both sync(w1 ) and sync(w2 ) can be deduced.
                                                      def
Assume now a process definition of the form p(e   y ) = P . We require the process P to emit
       A Concurrent Constraint Programming Interpretation of Access Permissions                              13
                                                        P                           P
           C[[c]]z   =   c ⊗ sync(z)              C[[       ∀e
                                                             xi (ci → Pi )]]z   =         C[[∀e
                                                                                              xi (ci → Pi )]]z
                                                     i∈I                            i∈I
 C[[∀e
     y (c → P )]]z = ∀e     y (c → C[[P ]]z )                        C[[∃y(PN
                                                                            )]]z = ∃y(C[[P ]]z )
 C[[P1 k . . . k Pn ]]z = ∃w1 . . . wn (C[[P1 ]]w1 k . . . k C[[Pn ]]wn k       sync(wi ) → sync(z))
                                                                       i∈1..n
                                                                      ∆                       ∆
        C[[p(e
             x)]]z   =   p(e
                           x, z)                             C[[p(e
                                                                  y ) = P ]]z   =     y , z) = C[[P ]]z
                                                                                    p(e

                     Fig. 6: Definition of the sequential composition P ; Q


the constraint sync(z) to synchronize with the call p(e    x). We then add an extra parameter
                                    ∆
                             y , z) = C[[P ]]z ). Hence the variable z is passed as a parameter
to the process definition (p(e
and used by C[[P ]]z to synchronize with the call p(e x, z).


                              4 AP Programs as LCC Processes
This section presents an interpretation of Access Permissions (APs) and Data Group Ac-
cess Permissions (DGAPs) as processes in lcc. We thus endow AP programs with a
declarative semantics which is adequate to verify relevant properties as we show later.
We start defining the constraint system we shall use. Constants, predicate symbols and
non-logical axioms are depicted in Figure 7 and explained below.
   We shall use c, m, a, g, o to range, respectively, over name of classes, methods, fields,
DGs and objects in the source AP language. For variables, we shall use x, y and u. We
may also use primed and subindexed version of these letters. We shall use the same letters
in our encodings. Hence, if x occurs in a constraint (see e.g., predicate ref(·) below), it
should be understood as the representation of a variable x in the source language. Finally,
we shall use z, w (possible primed or subindexed) to represent identifiers of statements in
the source program. Those variables will appear in the scope of constraints used for syn-
chronization in the model as, e.g., in the constraint sync(·).

Permissions and constants: Constant symbols in sets PER and GPER represent the kind
of APs and DGAPs available in the language. Since none, unique and immutable AP are
not associated to any data group, we shall use the constant ndg to denote “no-group”. Re-
call that the split command splits a DGAP into several DGAPs, one per each statement
in the block. Then, we require to specify in our model the statement to which the concur-
rent permission is attached to (see predicate dg(·) below). Since atomic DGAPs are not
attached to any particular statement in the program, we use the constant nst to denote
“no-statement”. The constant nil is used to denote a null reference. Assume a class c with
an attribute a and a data group parameter g. We use the constant symbol c a to make refer-
ence to a (see predicate field(·) below) and a constant symbol c g to make reference to g
(see gparam(·) below). We also consider the constant symbols g1 , ..., gn to give meaning
to the statement grouphg1 , · · · , gn i.

References and Fields: We use the predicate symbol ref(x, o, p, g) to represent that the
variable x is pointing to object o and it has a permission p on it. The last parameter of
this predicate is used to give meaning to share permissions of the form shr : g. As we
already explained, g = ndg when p 6= shr. The predicate field(xu , o, a) associates
14                                 Olarte, Pimentel and Rueda
                                                 Constant Symbols
 PER= {unq,shr, imm, none}   Types of access permissions.
 GPER = {atm, conc}          Types of data group access permissions.
 ndg                         Absence of data group.
 nst                         Absence of statement.
 nil                         Null reference
 ca                          For each field a of a class c.
 c gi                        For each group parameter in the class definition class c hg1 , ..., gn i
 g1 , ..., gn                For each DG in grouphg1 , · · · , gn i
                                                 Predicate Symbols
 ref(x, o, p, g)             x points to object o with permission p ∈ PER and belongs to the data group g
 field(u, o, a)              u is the reference to field a of object o.
 gparam(c g, o, gp)          The group parameter g of the object o was instantiated with the data group gp.
 sync(z)                     Synchronizing on variable z.
 act(z)                      Activate/start statement z.
 run(z)                      Statement z is being executed.
 end(z)                      End of statement z.
 ct(o, n)                    There are n references pointing to object o.
 dg(g, p, z)                 Statement z has a data group permission of type p ∈ GPER on the data group g.
                                                        Axioms
 downgrade1                  ∀x, o, g.[ref(x, o, unq, ndg) ( ref(x, o, shr, g)]
 downgrade2                  ∀x, o.[ref(x, o, unq, ndg) ( ref(x, o, imm, ndg)]
 upgrade1                    ∀x, o, g.[ref(x, o, shr, g) ⊗ ct(o, s(0)) ( ref(x, o, unq, ndg) ⊗ ct(o, s(0))]
 upgrade2                    ∀x, o.[ref(x, o, imm, ndg) ⊗ ct(o, s(0)) ( ref(x, o, unq, ndg) ⊗ ct(o, s(0))]



Fig. 7: Constraint system for Access Permissions. 0 denotes the constant “zero” and s(·)
successor.


the variable xu to the field a of object o. Once an object of a given class c with data group
parameters is instantiated, the predicate gparam(c g, o, gp) dictates that the group param-
eter g of the object o was instantiated with the DG gp. The predicate sync(z) is used in
the definition of P ; Q as explained in the previous section. Constraints act(z), run(z)
and end(z) represent, respectively, that statement z has been called, it is currently being
executed or it has finished. We shall use those constraints as witnesses for verification pur-
poses. The number of references (alias) pointing to a given object are modeled with the
predicate ct(o, n). Given a data group g, the predicate dg(g, p, z) dictates that the state-
ment z has a data group permission p ∈ GPER on g. If p = atm then z = nst.

Non-logical axioms: The entailment of the constraint system allows us to formalize when
a given AP can be transformed into another. Assume that x has a unique permission on
o. Unique permissions can be downgraded to share or immutable permissions as dic-
tated by axioms downgrade1 and downgrade2 respectively. Axiom upgrade1 (resp.
upgrade2 ) builds a unique permission from a share (resp. immutable) permission. For
that, x needs to be the unique reference with share or immutable permission to the pointed
object. Conversions from share permissions into immutable and vice versa require to first
upgrade the permission to unique and then applying the appropriate downgrade axiom.


                                    4.1 Modeling Statements.
Given an AP annotated program, we shall build a lcc program D.P where D includes
process definitions for each method and constructor of the AP program (Section 4.2 be-
low) and a process definition to encode assignments (assg in Figure 8). The process P
represents the encoding of the main body of the AP program where each statement s is
encoded as a lcc process S[[s]]G
                               z that models its behavior.
         A Concurrent Constraint Programming Interpretation of Access Permissions                                      15
                       ∆
   assg(x, y, z, gt)   =     drop(x); gain(x, y, gt); act(z) → run(z); run(z) → sync(z)⊗!end(z)
                       def                                               P
   drop(x)             =     ∀o, n, g((ref(x, nil , none, ndg) → 1 ) +         ref(x , o, p, g) ⊗ ct(o, s(n)) → ct(o, n))
                                                                     p∈PER\{none}
                       def
   gain(x, y, gt)     = ref(y, nil , none, ndg) → ref(x , nil , none, ndg) ⊗ ref(y, nil , none, ndg)
   + ∀o, n((ref(y, o, unq, ndg) ⊗ ct(o, s(0)) → ref(y, o, shr, gt) ⊗ ref(x, o, shr, gt) ⊗ ct(o, s(s(0))))
       + (ref(y, o, shr, gt) ⊗ ct(o, n) → ref(y, o, shr, gt) ⊗ ref(x, o, shr, gt) ⊗ ct(o, s(n)))
       + (ref(y, o, imm, ndg) ⊗ ct(o, n) → ref(y, o, imm, ndg) ⊗ ref(x, o, imm, ndg) ⊗ ct(o, s(n))))


                              Fig. 8: Auxiliary definitions for Rule RALIAS


   The process S[[s]]Gz adheres to the following schema. The lcc variable z is used to
represent the statement s in the model. We assume (by renaming variables if necessary)
that z does not occur in s. The encoding uses constrains to signal three possible states in
the execution of s. When the program control reaches the statement s, the encoding adds
the constraint act(z) to signal that s is ready to be executed. When the needed permissions
for s are successfully acquired, act(z) is consumed and constraints sync(z) and run(z)
are added. The first one is used to synchronize with the rest of the model. More precisely,
the encoding of the next instruction in the program waits for constraint sync(z) to be
posted before starting its execution. In this way, we model the data dependencies resulting
from the flow of APs. Constraint run(z) signals that s is currently being executed. Once
s has finished and the consumed permissions are restored, the encoding consumes run(z)
and adds the constraint end(z).
   The G in S[[s]]Gz stands for the set of DGs on which s must have a concurrent DGAP to
be executed. Recall that such permissions are assigned by a split command. Then, we
use G to control which DGAPs must be consumed and restored by s.
   In the following we define S[[s]]Gz for each kind of statement in the syntax in Figure 3.
                                                   def
For that, the following shorthand will be useful ( = must be understood as a shorthand and
not as process definition):

                               def
                                               O                                                O
wrap(P, {g1 , · · · , gn }, z) = act(z); (             dg(gi , conc, z) → 1); P k (end(z) →             dg(gi , conc, z)))
                                              i∈1..n                                           i∈1..n

                                                                                                     (wrap)
                                                                  G
  Assume that s is an statement and P                     = S[[s]]z . The process wrap(P, G, z) first con-
sumes all the concurrent DGAPs available for s, i.e., those in the set G. If G = ∅, then
 N
     dg(gi , conc, z) is defined as 1. Observe that once s has terminated (i.e., the con-
i∈1..n
straint end(z) is added to the store) such permissions are restored.

Assignments. We have different cases for the assignment rhgi := rhs depending whether
r and rhs are variables or field selections. Let us start with the case when both are variables
as in xhgi := y and x is syntactically different from y. We have:

                                                   G
                                     S[[xhgti := y]]z = wrap(assg(x, y, z, gt), G, z)                           (RALIAS )

where assg is defined in Figure 8. The variable x loses its permission to the pointed object
o, and the object o has one less reference pointing to it (Definition drop). Thereafter, x
and y point to the same object and the permission of y is split between x and y as explained
in Section 2.2 (Definition gain). Finally, once the permission to y is split, the constraints
16                                     Olarte, Pimentel and Rueda

sync(z) and !end(z) are added to the store to, respectively, synchronize with the rest
of the program and mark the termination of the statement. Note in assg the use of the
constraints act(·), run(·) and end(·). Initially, constraint act(z) is added (by wrap).
When the permissions on x and y are split (after drop and gain), act(z) is consumed
to produce run(z). Finally, run(z) is consumed to produce end(z).
   Now consider the case S[[x.ahgi := y]]G  z . If the variable x points to the object o of
class c, then the field a of o can be accessed via the variable u whenever the constraint
field(u, o, c a) holds. Intuitively, u points to x.a and then, a constraint ref(u, o0 , p, g)
dictates that x.a points to o0 with permission p. As we shall show later, the model of
constructors adds the constraint ! field(u, o, c a) to establish the connection between
objects and their fields. The model of the assignment S[[x.ahgi := y]]G  z is thus obtained
from that of S[[uhgi := y]]G
                           z :

     S[[x.ahgi := y]]G                                                                                    G
                     z = ∀u, o, p, g(ref(x, o, p, g) ⊗ field(u, o, c a) → (ref(x, o, p, g); S[[uhgi := y]]z ))
                                                                                                      (RALIASF )
The cases x.ahgi := y.a0 and xhgi := y.a are similar.

Let. Local variables in the AP program are defined as local variables in lcc:
                                        G
                                                   O                                      G
                   S[[let T
                          g x in s end]]z = ∃e
                                             x(             ref(xi , nil, none, ndg); S[[s]]z k GC)       (RLOC )
                                                 i∈1..|x|
                                                       e



          def           Q
where GC = end(z) → i∈1..|ex| drop(xi ). Observe that the freshly created variables point
to nil with no permissions. Once s ends its execution, the local variables are destroyed
(definition GC). We note also that, in this case, we do not add the constraint sync(z) nor
end(z). The reason is that the creation of the local variable can be considered as “instan-
taneous” and then, the process S[[s]]G
                                     z will be in charge of marking the termination of the
statement. Note that we ignore the type T since our model and analyses are concerned only
with the flow of access permissions and we assume that the source program is well typed.

Block of statements. In the block {s1 · · · si sj · · · sn }, the process modeling sj runs in
parallel with the other processes once S[[si ]]G
                                               zi adds the constraint sync(zi ) to the store.
Hence, what we observe is that the execution of sj is delayed until the encoding of si has
successfully consumed the required permissions. After that, even if si has not terminated,
the encoding of sj can proceed. Once sync(zn ) can be deduced, constraint sync(z) is
added to the store to synchronize with the rest of the program. Moreover, the constraint
end(z) is added only when all the statements s1 , ..., sn have finished their execution:
                                                            G
                                     S[[{s1 ... si ... sn }]]z = wrap(P, G, z)                          (RCOMP )


where P is defined as:
       def
 P      =    act(z) → run(z); ∃z1 , ...zn (S[[s1 ]]G                        G
                                                   z1 k sync(z1 ) → S[[s2 ]]N
                                                                                                             G
                                                                            z2 k ... k sync(zn−1 ) → S[[sn ]]zn k
                                sync(zn ) → sync(z) k (run(z) ⊗                 end(zi )) →!end(z))
                                                                           i∈1..n


Groups of permissions. In order to define DGs, we add a constraint specifying that each of
those groups has an atomic DGAP. Recall that the constant nst indicates that the atomic
         A Concurrent Constraint Programming Interpretation of Access Permissions                              17

               def
          P    =     ∃z1 , ..., zn , z 0 (gainP; act(z) → addP; exec; (sync(z 0 ) → restoreP); run(z) →!end(z))
               def
       gainP   =     dg(g1 , conc, z) → env(g1 , conc, z) + dg(g1 , atm, nst) → env(g1 , atm, nst) k ... k
                     dg(gm , conc, z) → env(gm , conc, z) + dg(gm , atm, nst) → env(gm , atm, nst)
               def               N     N
       addP    =     run(z) ⊗              dg(gj , conc, zi )
                                i∈1..n j∈1..m
               def          0                           0                           0
       exec    =     S[[s1 ]]G                        G
                             z k sync(z1 ) → S[[s2 ]]z2 k · · · k sync(zn ) → sync(z )
               def    N 1N
 restoreP      =                   dg(gj , conc, zi ) → sync(z);
                     i∈1..n j∈1..m
                     env(g1 , conc, z) → dg(g1 , conc, z) + env(g1 , atm, nst) → dg(g1 , atm, nst) k · · · k
                     env(gm , conc, z) → dg(gm , conc, z) + env(gm , atm, nst) → dg(gm , atm, nst)


                           Fig. 9: Auxiliary definitions for Rule RSPLIT


permission is not attached to any particular statement in the program:
                                                       G
                                                                O
                                S[[grouphg1 , ..., gn i]]z =            dg(gi , atm, nst)            (RNEWG )
                                                               i∈1..n



   Similar to the creation of local variables, we do not mark termination of this statement
since it can be considered as “instantaneous”.

Split. Let G0 = {g1 , ..., gm }. We define the rule for split as follows.
                                            0               G                        0
                                S[[splithG i{s1 · · · sn }]]z = wrap(P, G \ G , z)                    (RSPLIT )

where P and definitions gainP, addP, exec and restoreP are in Figure 9. Before
explaining those definitions, consider the following code:
   1   split <g1,g2>{
   2     s1
   3     split <g2,g3>{
   4      s2} }


and assume we are encoding the split statement in line 3. Then, we consider the process
S[[splithG0 i{s2 }]]G            0
                     z where G = {g2 , g3 }. The set G = {g1 , g2 } corresponds to the con-
current DGAPs assigned by the external split statement in line 1. The process gainP
consumes either atomic or concurrent permissions for each DG gi ∈ G0 . Since such per-
missions must be restored once the split command has been executed, we distinguish the
case when the consumed permission is concurrent (conc) or atomic (atm). For that, we
use the auxiliary predicate symbol (constraint) env(·) that keeps information of the DGAP
consumed. We note that the DGAP g2 ∈ G ∩ G0 is consumed and then split again to be
assigned to the statement s2 .
   Now consider the DG g1 ∈ G \ G0 . Since g1 6∈ G0 , the DGAP on this group must be
consumed ant it must not be split to be assigned to s2 . Hence, the consumption of any
g ∈ G \ G0 is handled by the wrap(·) process as in the encoding of other statements.
   Once we have consumed the appropriate DGAPs, we add, for each statement in the
block, a concurrent DGAP for each of the data groups in G0 (definition addP).
   The process exec is similar to Rule RCOMP but it uses as parameter G0 . In our example,
this means that concurrent DGAPs on g2 and g3 (and not on g1 ) are assigned to s2 . As we
already saw in the definition of RCOMP , the constraint sync(z 0 ) is added to the store once
all the statements in the block were able to consume the required APs. At this point, we
18                                       Olarte, Pimentel and Rueda

wait for all the instructions to reestablish their assigned DGAPs (definition restoreP).
Recall that this happens only when the statements terminate (see definition wrap).
  Finally, with the help of the constraints env(·), we restore the DGAPs to the environ-
ment and we add the constraint !end(z) to mark the ending of the block.

Method calls and Object instantiation. In our encoding we shall write methods and
constructors using functional notation rather than object-oriented notation. For instance,
x.m(e y ) is written as c m(x, ye) when x is an object of type c. Similarly, the expression
c c(x, ye) corresponds to x := new c(e    y ). As we shall see, for each method m(e
                                                                                  y ) of the
                                                                ∆
class c, we shall generate a process definition c m(x, ye, z) = P . The extra argument z is
used to later add the constraint sync(z) to synchronize with the rest of the program. If x
is of type c, the rule is defined as follows:
                                             G
                                  S[[x.m(e
                                         y )]]z = wrap(c m(x, y1 , .., yn , z), G, z)                     (RCALL )

   The case of the call x.a.m(ey ) can be obtained by using the constraint field(·) as we
did in Rule RALIASF for assignments between fields.
   The model of an object initialization is defined similarly but we add also as a parameter
the instances of the data groups:

                                                      G
                     S[[x := new chg1 , ..., gn i(e
                                                  y )]]z = wrap(c c(x, y
                                                                       e, z, g1 , ..., gn ), G, z)         (RNEW )



                                      4.2 Modeling Class Definitions.
In this section we describe function D[[·]] interpreting method and constructors definitions
as lcc process definitions.

Method Definitions. Let m(cy^
                            he                g ⇒ p0 (this), p]
                             gy i y) p(this), p(y)            0 (y) {s} be a method

           gx i. We define
in class che
                                ∆         0
                          e, z) = ∃ye0 , x (Consume; sync(z); act(z) → run(z); Body)
        D[[c.m]] = c m(x, y                                                                               (RMDEF )


           y | = |ye0 |,
where n = |e
                def
                                 consume(yi , yi0 , pi , c) k consume(x, x0 , p, c)
                          Q
     Consume     =
                        i∈1..n
                def        0
     Body        =             s]]z0 k (sync(z 0 ) ⊗ end(z 0 )) →
                        ∃z (S[[b
                                      (r env(x, p, x0 , p0 , c) k   r env(yi , pi , yi0 , p0i , c))) ; run(z) →!end(z)
                                                                  Q
                                                                  i∈1..n
and the auxiliary process definitions consume(·) and r env(·) are in Figure 10.
   In the process definition c m(x, ye, z), the first parameter x represents the object caller
this and the last parameter z is used for synchronization. This definition first declares the
local variables ye0 and x0 to replace the formal parameters (e
                                                             y ) and the caller (x) by the actual
parameters. Next, it consumes the required permissions from ye and x, and assigns them to
the previously mentioned local variables. Finally, the constraint sync(z) is added and the
encoding of the method’s body is executed. In the following we explain the definitions
Consume and Body.
   The definition of consume(x, x0 , p, c) in Figure 10 can be read as “consume the per-
mission p on the variable x and assign it to the variable x0 . If the required permission is
        A Concurrent Constraint Programming Interpretation of Access Permissions                                                  19
                                                                                 def
                                            consume(x, x0 , p, cname) =
                                                                                 0
     
     
      ∀o(ref(x, o, p, ndg) ⊗ ct(o, n) → ref(x, o, p, ndg) ⊗ ct(o, s(n)) ⊗ ref(x , o, p, ndg)) if p = imm
     
     
     
       ∀g, o(gparam(cname g, o, g) → ref(x, o, p, g) ⊗ ct(o, n) → ref(x, o, p, g) ⊗ ct(o, s(n))) ⊗ ref(x0 , o, p, g) if p = shr : g
     
     
     
     
       ∀o(ref(x, o, p, ndg) → ref(x0 , o, p, ndg)) if p ∈ {unq, none}
     

                                                                0  0             def
                                            r env(x, p, x , p , cname) =
       ∀o0 , n(ref(x0 , o0 , p0 , ndg) ⊗ ct(o0 , s(n)) → ct(o0 , n))          if p, p0 = imm




       ∀o0 , n, g(gparam(cname g, o0 , g) → ref(x0 , o0 , p0 , g) ⊗ ct(o0 , s(n)) → ct(o0 , n))                  if p, p0 = shr : g






     ∀o0 (ref(x0 , o0 , p0 , ndg) ⊗ ct(o0 , s(0)) → ref(x, o0 , p0 , ndg) ⊗ ct(o0 , s(0))             if p, p0 = unq





     ∀o0 (ref(x0 , o0 , p0 , ndg) → ref(x, o0 , p0 , ndg)        if p = none

             0
     ∀o, n, o ((ref(x, o, p, ndg) ⊗ ct(o, s(n)) →



        ct(o, n)); ref(x0 , o0 , p0 , ndg) → ref(x, o0 , p0 , ndg)) if p = imm, p0 ∈ {unq, none}






     ∀o, n, o0 , g((gparam(cname g, o, g) ⊗ ref(x, o, p, g) ⊗ ct(o, s(n)) →



        ct(o, n)); ref(x0 , o0 , p0 , ndg) → ref(x, o0 , p0 , ndg)) if p = shr, p0 ∈ {unq, none}


            Fig. 10: Auxiliary definitions for constructor and method declarations.


share or immutable, the permission is split and restored to allow concurrent executions in
the environment that called the method. We recall that in p = shr : g, g must be a data
group parameter in the class c. This explains the last parameter in consume(·). We then
use the predicate ! gparam(c g, o, g), added by the encoding of constructors, as we shall
see, to establish the link between the DG parameter and the current DG. Finally, unique
and none permissions are consumed and transferred to the local variables.
   Now we focus on the definition Body where sb denotes s after replacing yi by yi0 and x
by x0 . Once sb finishes (i.e., it adds end(z 0 ) to the store), the references and permissions
of the local variables created to handle the parameters are consumed and restored to the
environment according to r env(x, p, x0 , p0 , c) in Figure 10 (consume the permission p on
x and transforms it into a permission p0 to the variable x0 ). Let us give some intuition about
the cases considered in this definition. Recall that consume replicates the shr and imm
permissions for the variables internal to the method. Therefore, we only need to consume
those permissions and decrease the number of references pointing to object o0 . When the
input permissions are unq or none, consume transfers those permissions to the local
variables and consumes the external references. Then, r env needs to restore the external
reference and consume the local one (the number of references pointing to o0 remains the
same). When the method changes the input permission from share or immutable into a
unique or none, we need to consume first the external reference. Afterwards, we transfer
the internal permission and reference to the external variable.
Constructor definitions. Let c(cy^    hgex i y) none(this), p(y) g ⇒ p0 (this), p]   0 (y) {s} be

a constructor of a parameterized class chpg1 , ..., pgk i. We define
                                             ∆
    D[[CD ]] = c(x, y
                    e, z, g1 , ..., gk )     =     ∃ye0 , x0 , onew (gparam-init; consume0 ;
                                                     ∃e
                                                      u(fields-init ; sync(z); act(z) → run(z);
                                                      ∃z 0 (S[[bs]]z0 k (sync(z 0 ) ⊗ end(z 0
                                                                                              )) →
                                                         (r env(x, p, x0 , p0 , c) k       r env(yi , pi , yi0 , p0i , c))));
                                                                                       Q
                                                                                      i∈1..m
                                                         run(z) →!end(z))

                                                                                                                           (RCDEF )
20                                      Olarte, Pimentel and Rueda

     8    main(){
     9       let collection c, stats s in
  10           c := new collection()
     11        s := new stats()
     12        c.compStats(s)
     13        c.compStats(s)
     14        c.removeDuplicates()
     15    end}


             Fig. 11: Main program for Example 4.1. Class definitions are in Figure 1


           y | = |ye0 | and
where n = |e
                         def
          consume0                      consume(yi , yi0 , pi , c) k
                                 Q
                          =
                               i∈1..m
                               ref(x, nil , none, ndg) → ref(x 0 , onew , unq, ndg) ⊗ ct(onew , s(0))
                         def    N
          gparam-init     =        ! gparam(c pgi , onew , gi )
                               i∈1..k
                         def
          fields-init     =    ! field(u1 , onew , c a1 ) ⊗ ref(u1, nil , none, ndg) ⊗ ...⊗
                               ! field(uk , onew , c ak ) ⊗ ref(uk , nil , none, ndg)
   The mechanisms for parameter passing, executing the body sb and restoring permissions
are the same as in method definitions. The definition consume’ is similar to consume in
method definitions but, instead of using consume(x, x0 , p, c), we consume the constraint
ref(x, nil , none, nst), i.e., x in the statement x := new che   g i(e
                                                                     y ) is restricted to be a null
reference. Moreover, the internal variable x0 points to the newly created object onew with
permission unique.
   The definition gparam-init allows us to establish the link between the new object
onew and the group parameters. In the constraint gparam(c pgi , onew , gi ), the constant
symbol c pgi corresponds to the name defined for the DG parameter pgi of the class
chpg1 , ..., pgk i and gi is the current DG passed as parameter.
   The initialization of fields is controlled by the definition fields-init. The added
constraint field(ui , onew , c ai ) establishes the link between the field onew .ai and the
null reference ui .
   Let us present a couple of examples to show the proposed model in action.
Example 4.1 (Access Permission Flow)
Assume the class definitions stats and collection in Figure 1 and the main body in Figure
11. The lcc agent modeling the statement in line 10 calls collection collection(c, z10 ),
which triggers the execution of the body of the constructor (see Rules RCDEF and RCALL ).
Variable z10 is the local variable used to synchronize with the rest of the program (see Rule
RCOMP ). Once the agents modeling the statements in lines 10 and 11 are executed, the
following store is observed:
∃c, s, oc , os (ref(c, oc , unq, ndg)⊗ref(s, os , unq, ndg)⊗ct(oc , s(0)) ⊗ ct(os , s(0)))
Hence, c (resp. s) points to oc (resp. os ) with a unique permission. In c.compStats(), c
requires an immutable permission to oc . The axiom downgrade2 is used to entail the guard
of consume in the definition of the method. Let c0 be the representation of c inside the
method (see Rule RMDEF ). We notice that when the body of the method is being executed,
both c and c0 have an immutable permission to oc , i.e., the store contains the tokens
                ref(c, oc , imm, ndg) ⊗ ref(c0 , oc , imm, ndg) ⊗ ct(oc , s(s(0)))
         A Concurrent Constraint Programming Interpretation of Access Permissions                                                      21
                 Line           Store                             Observations
                 7              dg(g, atm, nst)                   See Rule RNEWG .
                 8              dg(g, atm, nst)             ⊗     s, o1 and o2 are null references (see Rule RLOC ).
                                ref(s, nil , none, ndg)     ⊗
                                ref(o1 , nil , none, ndg) ⊗
                                ref(o1 , nil , none, ndg)
                 10             dg(g, conc, z10 )           ⊗     The atm DGAP on g is consumed and split into conc per-
                                dg(g, conc, z11 )           ⊗     mission for statements in lines 11-12 (see Rule RSPLIT )
                                ref(s, nil , none, ndg) ⊗ · · ·
                 Before 13(1)   dg(g, conc, z10 ) ⊗ · · · ⊗       Variables s and obs are instantiated. The atomic DGAP has not
                                ref(s, os , shr, g)         ⊗     been restored yet and then, statement in line 13 has to wait.
                                ref(o1, oo1 , unq, ndg) ⊗
                                ref(o2, oo2 , unq, ndg)
                 Before 13(2)   dg(g, atm, nst)             ⊗     Concurrent DGAPs are consumed and the atomic permission
                                ref(s, os , shr, g) ⊗ · · ·       on g is restored (see Rule RSPLIT ).
                 Before 16      dg(g, conc, z14 )           ⊗     There are 3 references to os : s, s0 and s00 . The last two corre-
                                dg(g, conc, z15 )           ⊗     spond to the internal representation of s in the calls to method
                                ref(s, os , shr, g)         ⊗     update (see Rule Rule RMDEF ). Then, such methods can be
                                      0
                                ref(s , os , shr, g)        ⊗     executed concurrently. We also see that the atm DGAP was
                                      00
                                ref(s , os , shr, g)        ⊗     split into conc DGAP for statements 14 and 15.
                                ref(o1, oo1 , unq, ndg) ⊗
                                ref(o2, oo2 , unq, ndg)
                 16             dg(g, atm, nst)             ⊗     In the end, s is the sole reference to os (see r env in Rule
                                ref(s, os , shr, g)         ⊗     RMDEF ) and the atomic DGAP on g is reestablished.
                                ref(o1, oo1 , unq, ndg) ⊗
                                ref(o2, oo2 , unq, ndg)


       Fig. 12: Constraints added by the processes in Example 4.2 (AP code in Figure 2)


Before executing the body of method compStats constraint sync(z12 ) is added, so as
to allow possible concurrent executions in the main body (see Rule RCOMP ). Hence, the
agent modeling the statement in line 13 can be executed and we have a store with three
references with immutable permission to object oc , namely, c, c0 as before, and c00 , the
representation of c inside the method print. Now, once constraint sync(z13 ) is added by
the definition of print, the process representing the statement in line 14 can be executed.
However, this call requires c to have a unique permission to oc which is not possible since
the axiom upgrade2 requires that c is the sole reference to oc . Hence, the guard consume
for this call is delayed (synchronized) until the permissions on c0 and c00 are consumed and
restored to the environment (see r env in Rule RMDEF ). We then observe that statements
in lines 12 and 13 can be executed concurrently but the statement in line 14 is delayed until
the termination of the previous ones.

Example 4.2 (Data Group Permissions Flow)
Now consider the program in Figure 2. Figure 12 shows the stores generated by the model
of this program. We omit some tokens for the sake of readability.

Example 4.3 (Deadlocks)
Let us consider the following implementation for the method compStats in the class
collection (see Figure 1)
   1   compStats(s)     imm(this), unq(s) => imm(this), unq(s) {
   2      ...
   3      c.sort()
   4      ... }

   Consider the call c.compStats(s) and suppose that, in the lcc model, variable c points
to the object oc . When the compStats method is invoked, the immutable permission is
divided between the external reference c and the internal reference c0 . For this reason,
22                                 Olarte, Pimentel and Rueda

inside the method, reference c0 cannot acquire a unique permission for the invocation of
method sort which then blocks. Our analysis will thus inform that there is a deadlock,
unless, e.g., the program includes the statement chgi := nil to discard the permission of c
to oc .
   Consider now the following definition of the same method:
     1    compStats(s)   unq(this), unq(s) => unq(this), unq(s) {
     2      ...
     3      c.sort()
     4     ...}

   When compStats is invoked, the unique permission is transferred from reference c to
(the internal) reference c0 . The invocation of method sort has thus the right permissions to
be executed and it does not block.


                           4.3 The Model as a Runnable Specification
Models based on the ccp paradigm can be regarded as runnable specifications, and so we
can observe how permissions evolve during program execution by running the underly-
ing lcc model. We implemented an interpreter of lcc in Java and used Antlr (http:
//www.antlr.org) to generate a parser from AP programs into lcc processes fol-
lowing our encoding. The resulting lcc process is then executed and a program trace is
output. The interpreter and the parser have been integrated into Alcove (Access Permis-
sion Linear COnstraints VErifier) Animator, a web application freely available at http:
//subsell.logic.at/alcove2/. The URL further includes all the examples pre-
sented in this section. In the following we explain some outputs of the tool.
Example 4.4 (Trace of Access Permissions)
The program in Figure 1 generates the trace depicted in Figure 13. For verification pur-
poses, the implementation extends the predicates act(·), run(·) and end(·) to include
also the variable that called the method, the name of the method and the number of line of
the call. Note for instance that the call to print (line 9 in Fig. 13) was marked while the
method sort was running (line 7). Nevertheless, the execution of print (line 11) must wait
until sort terminates (line 10). In this trace, the constructor stats (line 5) runs in parallel
with sort (line 7). Finally, the execution of removeDuplicates (line 17) is delayed until
the methods print (line 13) and compStats (line 16) terminate. Lines 20 and 21 show that
both c and s end with a unique permission to objects o_4774 and o_79106, respectively
(the numbers that follow the variable names are generated each time a local variable is
created to avoid clash of names).

Example 4.5 (Deadlock Detection)
Let us assume now the class definitions in Figure 1 and the following main:
     8    main(){
     9     group<g>
     10    let collection c, stats s, stats svar in
     11        c := new collection()
     12        s := new stats()
     13        svar<g> := s
     14        c.compStats(s)
     15        c.compStats(svar)
     16   end}
        A Concurrent Constraint Programming Interpretation of Access Permissions             23

   1   act(C_628,collection_collection,line 10 (Z_PAR_814))
   2   run(C_628,collection_collection,line 10 (Z_PAR_814))
   3   act(S_729,stats_stats,line 11 (Z_PAR_915))
   4   end(C_628,collection_collection,line 10 (Z_PAR_814))
   5   run(S_729,stats_stats,line 11 (Z_PAR_915))
   6   act(C_628,collection_sort,line_12 (Z_PAR_1016))
   7   run(C_628,collection_sort,line_12 (Z_PAR_1016))
   8   end(S_729,stats_stats,line 11 (Z_PAR_915))
   9   act(C_628,collection_print,line_13 (Z_PAR_1117))
  10   end(C_628,collection_sort,line_12 (Z_PAR_1016))
  11   run(C_628,collection_print,line_13 (Z_PAR_1117))
  12   act(C_628,collection_compStats,line_14 (Z_PAR_1218))
  13   end(C_628,collection_print,line_13 (Z_PAR_1117))
  14   run(C_628,collection_compStats,line_14 (Z_PAR_1218))
  15   act(C_628,collection_removeDuplicates,line_15 (Z_PAR_1319))
  16   end(C_628,collection_compStats,line_14 (Z_PAR_1218))
  17   run(C_628,collection_removeDuplicates,line_15 (Z_PAR_1319))
  18   end(C_628,collection_removeDuplicates,line_15 (Z_PAR_1319))
  19
  20   [ref(C_628,O_4774,unq,ng), ct(O_4774,1)]
  21   [ref(S_729,O_79106,unq,ng), ct(O_79106,1)]
  22   ok()
  23   567 processes Created


             Fig. 13: Trace generated by the program in Figure 1 (Example 4.4)


   1   act(C_644,collection_collection,line 10 (Z_PAR_928))
   2   run(C_644,collection_collection,line 10 (Z_PAR_928))
   3   act(S_745,stats_stats,line 11 (Z_PAR_1029))
   4   run(S_745,stats_stats,line 11 (Z_PAR_1029))
   5   end(C_644,collection_collection,line 10 (Z_PAR_928))
   6   end(S_745,stats_stats,line 11 (Z_PAR_1029))
   7   act(C_644,collection_compStats,line_13 (Z_PAR_1231))
   8   [Killed] ask endc(line_13 (Z_PAR_1231)) then ...
   9   [Killed] ask sync(line_14 (Z_PAR_1332)) then ...
  10   [Killed] ask ref(S_745,O_142,unq,ng) then ... + ask
  11   ...
  12   404 processes Created
  13   [FAIL] Token ok not found. End of the program not reached.
  14
  15   VARIABLES
  16   C_644 -> O_6491. imm:ng
  17   S_745 -> O_96123. shr:GRP_461
  18   SVAR_846 -> O_96123. shr:GRP_461
  19   INNER_136172 -> O_6491. imm:ng


                  Fig. 14: Trace generated by the program in Example 4.5


   The assignment in line 13 aliases svar and s so they share the same permission after-
wards. Therefore, s cannot recover the unique permission to execute the statement in line
14, thus leading to a permission deadlock. This bug is detected by Alcove as depicted in
Figure 14 (line 13). Observe in the trace that compstats is called (line 7 in the trace) but
not executed. Furthermore, both s and svar have a share permission on the same pointed
object (lines 17 and 18). Moreover, both c (c_644) and its internal representation inside
compStats (inner_136172) have an immutable permission on object o_6491 (lines
16 and 19). Lines 8-11 show the suspended lcc processes in the end of the computation
that were killed by the scheduler. Particularly, line 10 shows that there is an ask agent trying
to consume a unique permission on object O_142 pointed by S_745.
24                                Olarte, Pimentel and Rueda

                                4.4 Adequacy of the Encoding
In this section we present some invariant properties of the encoding and prove it correct.
There are three key arguments in our proofs:
Observation 4.1 (Ask agents)
(1) the ask agents controlling both the APs (Proposition 4.1) and the state of statements
(Proposition 4.2) are of the form c → P where P is a tell agent (and not, e.g., a parallel
composition). Hence, in one single transition, the encoding consumes and produces the
needed tokens to maintain the invariants (ruling out intermediate states where the property
might not hold). Moreover, (2) such ask agents are preceded by the sequential composi-
tion operator “;”. This means that, before consuming the needed constraints, some action
must have been finished. In particular, (3) the ask agent act(z) → run(z) is executed
only when the needed permissions are consumed and the ask agent run(z) → end(z)
is executed only after restoring the consumed permissions (Rules RALIAS , RCDEF and
RMDEF ).
  The following invariants show that the lcc model correctly keeps track of the variables
and their corresponding pointed objects.
Proposition 4.1 (Invariants on References)
Let S be an AP program and D.P its corresponding translation into lcc. Assume that
(∅; P ; 1) −→∗ (X; Γ; c). The following holds:
1. If c ` ref(x, o, unq, ndg) then c ` ct(o, s(0)).
2. If c ` ref(x, o, p, g) and p ∈ {shr, imm} then, there exists n > 0 s.t. c ` ct(o, n).
3. If c ` ref(x, o, p, g) and c ` ref(x, o0 , p0 , g 0 ) then o0 = o, p0 = p and g 0 = g.
4. If c ` ref(x, nil , p, g) then p = none and g = ndg.
5. (counting) if c ` ct(o, n) then:
                                                            N
  (a) for all m ≤ n, c ` ∃x1 , p1 , g1 ..., xm , pm , gm         ref(xi , o, pi , gi ); and
                                                          i∈1..m
                                                            N
  (b) for all m > n, c 6` ∃x1 , p1 , g1 ..., xm , pm , gm        ref(xi , o, pi , gi )
                                                        i∈1..m

Proof
An inspection of the encoding reveals that the rules RALIAS and RLOC and the definitions
consume, r env and fields-init are the only ones that consume/produce ref(·)
and ct(·) constraints. For any newly created variable, RLOC and fields-init add the
needed ref(·) token adhering to item 4. Moreover, the ask agents in the above rules/defini-
tions adhere to the conditions in Observation 4.1. Therefore, if the agent c → P consumes
a constraint of the form ref(x, o, p, g), the tell process P adds the needed constraints to
maintain correct the counting of references to o.
     The next proposition shows that the encoding correctly captures the state of statements.
Proposition 4.2 (States)
Let State = {act, run, end}, S be an AP program and D.P its corresponding lcc
translation. Consider an arbitrary execution starting at P :
            (∅; P ; 1) −→ (X1 ; Γ1 ; c1 ) −→ (X2 ; Γ2 ; c2 ) −→ · · · −→ (Xn ; Γn ; cn )
Let z ∈ Xn , st ∈ State, x ∈ 1 . . . n and assume that cx ` st(z). Then,
       A Concurrent Constraint Programming Interpretation of Access Permissions           25

1. (no confusion) for all st0 ∈ State \ {st}, cx 6` st0 (z).
2. (state ordering) there exists i ∈ 1..x such that
  (a) (init) for all k ∈ [1, i) and st0 ∈ State, ck 6` st0 (z).
  (b) (continuity) for all k ∈ [i, n], ck ` st0 (z) for some st0 ∈ State.
  (c) (act) if cn ` act(z) then for all k ∈ [i, n], ck ` act(z).
  (d) (act until run) If cn ` run(z) then, there exist two non-empty intervals A = [i...jr )
      and R = [jr , n] s.t. for all k ∈ A, ck ` act(k) and for all k ∈ R, ck ` run(k).
  (e) (run until end) If cn ` end(z) then there are 3 non-empty intervals A = [i..jr ),
      R = [jr , ..., je ), E = [je , ..., jn ] s.t. A and R are as above and for all k ∈ E,
      ck ` end(z).

Proof
Note that the token act(z) is added when the encoding of a statement is activated (wrap).
An inspection of the encoding shows that the ask agents controlling the state of statements
adhere to conditions in Observation 4.1. Since each executed statement uses a freshly cre-
ated variable z (see RCOMP ), we can show that, for any z and multiset Γx , Γx can contain
at most one of each of such ask agents (using z). Hence, for all st ∈ State, if s(z) is con-
sumed from the store cx , the store cx+1 must contain the next state st0 (z). This guarantees
the correct ordering of states.
   We conclude by showing that the encoding enforces the execution of statements accord-
ing to the AP specification. More precisely, the activation of a statement s is delayed until
its (lexical) predecessor has successfully consumed the needed permissions; the execution
of s is delayed until its required permissions are available (and consumed); signalling the
termination of s is delayed until all the consumed permissions are restored.
Theorem 4.1 (Adequacy)
Let S be an AP program and D.P its corresponding lcc translation. Let si and sj be two
sentences that occur in the same block and sj is lexically after si . Then,
1. (safety) si and sj are in conflict iff for any reachable configuration (X; Γ; c) from
(X; P ; 1), c ` run(zsj ) implies c ` end(zsi ).
2. (concurrency) si is not in conflict with sj iff there exists a reachable configuration
(X; Γ; c) from (X; P ; 1) s.t. c ` run(zsi ) and c ` run(zsj ).

Proof
The execution of assignments, the call to methods/constructors and the beginning of blocks
are the statements we have to synchronize in the encoding. Note that rules RALIAS , RCDEF ,
RMDEF , RSPLIT and RCOMP adhere to conditions in Observation 4.1. In particular, con-
dition (3) shows that the changes of states are controlled by acquiring / releasing permis-
sions.
   (⇒) 1. Assume that si and sj both require a unique permission on the same object (the
other kind of conflicts are similar). From rule RCOMP , we know that si first consumes
its permissions (before enabling sj ). From Propositions 4.1 and 4.2 we can show that sj
cannot move to the state run until si moves to state end.
   2. If there are no conflicting resources, then both processes may successfully consume
26                                Olarte, Pimentel and Rueda

  L[[c]]
     P                      =   c                            L[[P k Q]]    =   L[[P ]] ⊗ L[[Q]]
  L[[ ∀e xi (ci → Pi )]]    =          xi (ci ( L[[P ]]))
                                Ni∈I (∀e                     L[[∃x(P )]]   =   ∃x.(L[[P ]])
     i∈I
           ∆
  L[[p(e
       x) = P ]]            =   ∀e   x) ( L[[P ]]
                                 x.p(e                       L[[p(e
                                                                  x)]]     =   p(e
                                                                                 x)


                   Fig. 15: Interpretation of lcc processes as ILL formulas.


the needed permissions from the store. Consider the following trace: the encoding of si
consumes the needed permissions, adds run(zsi ) and the sync(zsi ) token. Then, the
encoding of s2 can start its execution (consuming sync(zsi )), consumes the needed per-
missions and adds run(zsj ) to the store.
   (⇐) For (1), assume that in any reachable configuration (X; Γ; c), c ` run(zsj ) im-
plies c ` end(zsi ). By Proposition 4.2 we know that c 6` run(zsi ). Since the encoding
maintains correct the number of references (in the sense of Proposition 4.1), there is no
reachable store able to entail the permissions needed for both si and sj . Hence, there is a
conflicting access in si and sj . The case (2) follows from a similar argument.


                           5 Logical Meaning of Access Permissions
Besides playing the role of executable specifications, ccp-based models can be declar-
atively interpreted as formulas in logic (Saraswat 1993; de Boer et al. 1997; Nielsen
et al. 2002; Fages et al. 2001; Olarte and Pimentel 2017). This section provides addi-
tional mechanisms and tools for verifying properties of AP based programs. More con-
cretely, we take the lcc agents generated from the AP program and translate them as
an intuitionistic linear logic (ILL) formula. Then, a property specified in ILL is verified
with the Alcove LL Prover, a theorem prover implemented on top of Teyjus (http:
//teyjus.cs.umn.edu), an implementation of λ-Prolog (Nadathur and Miller 1988;
Miller and Nadathur 2012).
   Our analyses are based on reachability properties, i.e., we verify the existence of reach-
able lcc configurations satisfying some conditions. It turns out that this is enough for
verifying interesting properties of AP programs. For instance, we can check whether a
program is dead-lock free or whether two statements can be executed concurrently.


                                    5.1 Agents as Formulas
The logical interpretation of lcc agents as formulas in intuitionistic linear logic ILL is de-
fined with the aid of a function L[[·]] defined in Figure 15 (Fages et al. 2001). As expected,
parallel composition is identified with multiplicative conjunction and ask processes cor-
respond to linear implications. Moreover, process definitions are (universally quantified)
implications to allow the unfolding of its body.
   In what follows, we will show how to use logic in order to have a better control of the
operational flow and, therefore, be able to verify properties of AP programs.
   The first step consists of interpreting the lcc model in Section 4 as ILL formulas via
L[[·]]. We shall call definition clauses to the encoding of process definitions of the form
        ∆
p(ex) = P (i.e., assignment and constructor and method definitions in our encoding) and
        A Concurrent Constraint Programming Interpretation of Access Permissions                                                  27
                    assg(x, y, z, gt) (
                                       ∃z1 .(∀o, n, g.(ref(x, o, none, ndg) ( 1 ⊗ sync(z1 )N
                                       ref(x, o, unq, ndg) ⊗ ct(o, s(n)) ( ct(o, n) ⊗ sync(z1 )N
                                       ref(x, o, shr, g) ⊗ ct(o, s(n)) ( ct(o, n) ⊗ sync(z1 )N
                                       ref(x, o, imm, ndg) ⊗ ct(o, s(n)) ( ct(o, n) ⊗ sync(z1 ))⊗

                        sync(z1 ) (    ∃z2 .(ref(y, nil , none, ndg) (
                                        ref(x, nil , none, ndg) ⊗ ref(y, nil , none, ndg) ⊗ sync(z2 )
                                       N ∀o, n.(ref(y, o, unq, ndg) ⊗ ct(o, s(0)) (
                                         ref(y, o, shr, gt) ⊗ ref(x, o, shr, gt) ⊗ ct(o, s(s(0))) ⊗ sync(z2 ))
                                       N ∀o, n.(ref(y, o, shr, gt) ⊗ ct(o, n) (
                                         ref(y, o, shr, gt) ⊗ ref(x, o, shr, gt) ⊗ ct(o, s(n)) ⊗ sync(z2 ))
                                       N ∀o, n.(ref(y, o, imm, ndg) ⊗ ct(o, n) (
                                         ref(y, o, imm, ndg) ⊗ ref(x, o, imm, ndg) ⊗ ct(o, s(n)) ⊗ sync(z2 ))⊗
                       sync(z2 ) ( ∃z3 .(act(z) ( run(z) ⊗ sync(z3 )⊗
                       sync(z3 ) ( ∃z4 .(run(z) ( sync(z4 ) ⊗ ! end(z))))).
                    L[[P ]] = ∃c, s, svar, z, z1 , z2 , z3 , z4 , z5 .(ref(c, nil , none, ndg)⊗
                               ref(s, nil , none, ndg) ⊗ ref(svar , nil , none, ndg) ⊗ sync(z1 ) ⊗ ! end(z1 )⊗
                                  sync(z1 ) ( collection collection(c, z2 )⊗
                                  sync(z2 ) ( stats stats(s, z3 )⊗
                                  sync(z3 ) ( assig(svar, s, z4 )⊗
                                  sync(z4 ) ( collection compStats(c, N             s, z5 )⊗
                               sync(z5 ) ( sync(z)) ⊗ (                  end(zi )) ( ! end(z)
                                                               i∈1..5



          Fig. 16: Encoding of assg definition and the main body in Example 4.5


we shall include them in a theory ∆, together with the axioms of upgrade and downgrade
in Figure 7. The next example illustrates this translation. For the sake of readability, we
shall omit empty synchronizations such as sync(z) ⊗ (sync(z) → 1).

Example 5.1 (Agents as formulas)
Consider the following lcc process definition resulting from the encoding of the construc-
tor of class collection in Figure 1:
                                      ∆
   collection collection(x, z) = ∃x0 , onew (1; ref(x, nil, none, ndg) → ref(x0 , onew , unq, ndg) ⊗ ct(onew , s(0)); 1; sync(z);
                                       act(z) → run(z); ∃z 0 (sync(z 0 ) ⊗ ! end(z 0 ) k (sync(z 0 ) ⊗ end(z 0 )) →
                                            ∀o0 (ref(x0 , o0 , unq, ndg) ⊗ ct(o0 , s(0)) → ref(x, o0 , unq, ndg) ⊗ ct(o0 , s(0)));
                                                 run(z) → ! end(z)))
where the first 1 corresponds to the empty parallel composition in gparam-init. From
now on, for the sake of readability, we will identify A ≡ A ⊗ 1. This process definition
gives rise to the following (universally quantified) definition clause:
   collection collection(x, z) ( ∃x0 , onew , w1 .(ref(x, nil, none, ndg) ((ref(x0,onew , unq, ndg) ⊗ ct(onew , s(0)) ⊗ sync(w1 )⊗
    |            {z             }                  |            {z         }
                    1                                               2
      sync(w1 ) (            ∃w2 .sync(z) ⊗ sync(w2 )⊗
      |   {z     }
            3
      sync(w2 ) (            ∃w3 . act(z) ((run(z) ⊗ sync(w3 ))⊗
      |   {z     }                 | {z }
            4                             5
         sync(w3 ) (         ∃z 0 , w4 .sync(z 0 ) ⊗ ! end(z 0 ) ⊗ (sync(z 0 ) ⊗ end(z 0 ) (
         |   {z     }                                              |           {z           }
                6                                                             7
                             ∀o0 .(ref(x0 ,o0 ,unq, ndg) ⊗ ct(o0 , s(0)) ( ref(x, o0 , unq, ndg) ⊗ ct(o0 , s(0)) ⊗ sync(w4 )))⊗
         sync(w4 ) (         run(z) ( ! end(z))).
         |   {z     }
                8
   The underlying brackets will be used in Section 5.4 for determining the complexity of
decomposing this formula The theory ∆ contains the definition clause above and the def-
inition clauses for the other methods and constructors in Figure 1 (i.e., collection sort,
collection print, etc). ∆ also contains the axioms for upgrading and downgrading per-
missions and the definition clause resulting from the process definition assg in Figure 8.
In Figure 16 we show the encoding for assg as well as the encoding L[[P ]] of the main
program in Example 4.5.
28                              Olarte, Pimentel and Rueda

                                5.2 Focusing and adequacy
In this section we show that the translations presented in the last section are neat, in the
sense that one computational step corresponds to one focused phase in proofs (Andreoli
1992). This will not only guarantee that our encodings are adequate (in the sense that
logical proofs mimics exactly computations), but also it will provide an elegant way of
measuring the complexity of computations via complexity of derivations (see Section 5.4).
   The approach for this section will be intuitive. The reader interested in the formalization
of focusing and various levels of adequacy between ILL and lcc can check the details
in (Olarte and Pimentel 2017).
   Let us start by analyzing the following two right rules in ILL (for the additive and mul-
tiplicative conjunctions):
                  Γ −→ F Γ → G N                Γ1 −→ F Γ2 → G
                                 R                                ⊗R
                    Γ −→ F NG                    Γ1 , Γ2 −→ F ⊗ G
Reading these rules bottom-up, while the first copies the contexts, the second involves a
choice of which formulas should go to left or right premises. Computationally, these behav-
iors are completely different: while the price to pay on applying NR is just the duplication
of memory needed to store formulas in the context, in ⊗R one has to decide on how to split
the context, and this has exponential cost. These rules are very different from the proof
theoretical point of view as well: the first rule turns out to be invertible in ILL, while the
second is not. This implies that the rule NR can be applied anywhere in the proof, and this
will not affect provability. On the other hand, ⊗R is not invertible and its application may
involve backtracking.
   The same analysis can be done to all other rules in ILL, giving rise to two disjoint
classes of rules: the invertible ones, that can be applied eagerly, {>R , 1L , ⊗L , NR , (R
, ⊕L , ∃L , ∀R , C} and the non invertible ones {1R , ⊗R , NL , (L , ⊕R , ∃R , ∀L , W, D, prom}.
   This separation induces a two phase proof construction: a negative, where no backtrack-
ing on the selection of inference rules is necessary, and a positive, where choices within
inference rules can lead to failures for which one may need to backtrack.
   An intuitive notion of focusing can be then stated as: a proof is focused if, seen bottom-
up, it is a sequence of alternations between maximal negative and positive phases.
   Focusing is enough for assuring that the encoding presented in Section 5.1 is, indeed,
adequate.

Theorem 5.1 (Adequacy (Olarte and Pimentel 2017))
Let P be a process, Ψ be a set of process definitions and ∆ be a set of non-logical axioms.
Then, for any constraint c, (∅; P ; 1) −→∗ (X; Γ; d) with ∃X.d ` c iff there is a proof of
the sequent ! L[[Ψ, ∆]], L[[P ]] −→ c ⊗ > in focused ILL (ILLF). Moreover, one focused
logical phase corresponds exactly to one operational step.

This result, together with Theorem 4.1, shows that AP can be adequately encoded in ILL in
a natural way. In the present work we are more interested in using logic in order to verify
properties of the computation, as clarified in the next example.

Example 5.2 (Traces, proofs and focusing)
Let A1 = a → b → (a ⊗ b), A2 = b → a → ok and P = a ⊗ b k A1 k A2 . The
      A Concurrent Constraint Programming Interpretation of Access Permissions                         29

operational semantics of lcc dictates that there are two possible transitions leading to the
store ok. Both of such transitions start with the tell action a ⊗ b:
    Derivation 1:   h∅; P ; 1i   −→∗    h∅; A1 k A2 ; a ⊗ bi −→∗ h∅; b → (a ⊗ b) k A2 ; bi
                                 −→∗    h∅; (a ⊗ b) k A2 ; 1i −→∗ h∅; A2 ; a ⊗ bi −→∗ h∅; ·; oki 6−→
    Derivation 2:   h∅; P ; 1i   −→∗    h∅; A1 k A2 ; a ⊗ bi −→∗ h∅; A1 k a → ok; bi
                                 −→∗    h∅; A1 k ok; 1i −→∗ h∅; A1 ; oki 6−→

Each of these transitions corresponds exactly to a focused proof of the sequent L[[P ]] −→
ok ⊗ >: one focusing first on L[[A1 ]] and the other focusing first on L[[A2 ]].
   On the other hand, there is also an interleaved execution of A1 and A2 that does not lead
to the final store ok:
        Detivation 3:    h∅; P ; 1i   −→∗   h∅; A1 k A2 ; a ⊗ bi −→∗ h∅; b → (a ⊗ b) k A2 ; bi
                                      −→∗   h∅; b → (a ⊗ b) k a → ok; 1i 6−→

This trace does not have any correspondent derivation in focused ILL (see (Olarte and
Pimentel 2017) for details).
This example is a good witness of a need for Alcove’s verifier, other than just having
an animator: an animator exhibits traces of possible executions without any pre-defined
scheduling policy. One of such traces may not lead to the expected final store (as the ok
above). On the other hand, the verifier would either fail (if a property is not provable) or
succeed. In this last case, the proof produced by the prover corresponds exactly to a valid
trace from the operational point of view.
   Let us show an example of how focusing can control executions on a sequential compo-
sition.
Example 5.3 (Focusing on a Sequential Composition)
Consider the ILL interpretation of the sequential composition P ; Q:
                  L[[P ; Q]] = ∃z((L[[(C[[P ]]z )]]) ⊗ (sync(z) ( L[[Q]]))
This is a positive formula which will be on the left side of the sequent and ∃ and ⊗ will
be decomposed in a negative phase. Once P is executed, we observe the invertible action
of adding the atom sync(z) to the context. Then, one could change to a positive phase
and focus on the negative formula sync(z) ( L[[Q]]. This positive action needs to be
synchronized with the context, consuming sync(z) in order to produce L[[Q]].
  In the following sections, we shall show that a focused ILL prover is a complete decision
procedure for reachability properties of the lcc agents resulting from our encodings. This
will be useful to verify properties of the encoded AP program.


             5.3 Linear Logic as a Framework for Verifying AP Properties
Let P be an agent and L[[P ]] its translation into ILL, producing a formula F together with
a theory ∆. In order to verify a certain property G, specified by an ILL formula G, we test
if the sequent ! ∆, F −→ G is provable.
    First of all, observe that the fragment of ILL needed for encoding access permissions is
given by the following grammar for guards/goals G and processes P :
       G := a | G ⊗ G | ∃x.G
       P := a |!a | 1 | P ⊗ P | P NP | ∀x.G ( P | ∃x.P |!∀e
                                                          x.(p(e
                                                               x) ( P ).
30                               Olarte, Pimentel and Rueda

where a is an atomic formula. Observe that guards G do not consider banged formulas,
i.e., agents are not allowed to ask banged constraints. A simple inspection on the encoding
of Section 4 shows that processes in our case indeed belong to such fragment. We note also
that formulas generated from this grammar exhibit the following properties:

     1. the left context in the sequent ! ∆, F −→ G will be formed by P formulas;
     2. the right context will have only G formulas;
     3. implications on the left can only introduce guards on the right side of a sequent. In
        fact, on examining a proof bottom-up, decomposing the implication on the sequent
        Γ1 , Γ2 , B ( C −→ D will produce the premises Γ1 , C −→ D and Γ2 −→ B.
        Hence it is important to guarantee that B (a guard) is a G (goal) formula.

   Finally, notice that the fragment described above is undecidable in general, due to the
presence of processes declarations (Lincoln et al. 1992). However, since we are consid-
ering AP programs adhering to the condition in Remark 2.1, our base language does not
lead to cyclic recursive definitions. In next section, we determine an upper bound for the
complexity of proofs in Alcove’s verifier. Therefore, we can show that provability in the
resulting ILL translation is decidable (see Theorem 5.2).


                                  5.4 Complexity analysis
Note that, when searching for proofs in the focused system, the only non-deterministic step
is the one choosing the focus formula in a positive phase. This determines completely the
complexity of a proof in ILLF and it justifies the next definition.

Definition 5 (Proof Depth)
Let π be a proof in ILLF. The depth of π is the maximum number of positive phases along
any path in π from the root.


Example 5.4 (Complexity of Formulas)
Consider the formulas in Example 5.1. The depth of decomposing the definition clause
collection collection(x, z) into its literal or purely positive subformulas is 8. To see that,
note that focusing in such a negative formula on the left will produce 7 more nested pos-
itive phases in one of the branches of the proof: each one of these phases is signaled
in the formula with an underlying bracket containing the respective number of the fo-
cused phase. The same holds when decomposing the clauses for stats stats(s, z) and
collection compStats(c, s, z). As we will see later, decomposing assig(svar, s, z) has a
fixed depth equal to 7. Hence the depth of a derivation for decomposing the formula F (the
model of the main program) is 8 + 8 + 7 + 8 = 31.

  We will now proceed with a careful complexity analysis of decomposing the formulas
produced by the specification of AP programs. These will be placed on the left of the
sequent. This is done by counting the changes of nested polarities, as in the example above.
The complexity of decomposing a process P will be denoted by comp(L[[P ]]).

- Base cases. We will start by presenting the complexity for decomposing the different
       A Concurrent Constraint Programming Interpretation of Access Permissions                              31

  kinds of lcc processes:
                    comp(L[[c]])                       =   0
                                                                                                ∆
                    comp(L[[p(x)]])                    =   1 + comp(L[[P ]]) if ∀e
                                                                                 x.p(ex) = P
                    comp(L[[PPk Q]])                   =   comp(L[[P ]]) + comp(L[[Q]])
                    comp(L[[   ∀exi (ci → Pi )]])      =   1 + maxi∈I {comp(L[[Pi ]])}
                              i∈I
                    comp(L[[∃x(P )]])                  =   comp(L[[P ]]).

- Sequential composition. Recall that the process P ; Q was defined in Figure 6 with the
  aid of the function C[[·]]. The complexity of decomposing L[[P ; Q]] will be given with
  the help of the auxiliary function compsc , that differs from comp only in the case of the
  parallel composition:
               comp(L[[P ; Q]])                        =   1 + comp
                                                                 P sc (L[[C[[P ]]z ]]) + comp(L[[Q]])
               compsc (L[[C[[P1 k . . . k Pn ]]z ]])   =   1+       compsc (L[[C[[Pi ]]wi ]])
                                                                i∈1..n
               compsc (C[[P ]]z )                      =   comp(L[[C[[P ]]z ]])   in any other case

  In the definition of P ; Q, the constraint sync(z) will always be produced before ex-
  ecuting Q. As already said, these are negative actions and hence do not interfere with
  the proof’s complexity. However, if P is a parallel composition P = P1 k . . . k, Pn ,
  then each process Pi will produce its own synchronization token, and all of them will be
  consumed at once in order to produce the constraint sync(z). Hence, the complexity of
  decomposing P ; Q takes into account nested parallel compositions inside P .

- Wrap. The complexity of decomposing the subNformula wrap(P, {g1 , · · · , gn }, z) is
   comp(L[[wrap(P, {g1 , · · · , gn }, z)]])   =   1 + comp(      dg(gi , conc, z) ( 1)
                                                               i∈1..n           N
                                                   +comp(L[[P ]] ⊗ (end(z) (        dg(gi , conc, z))) + 1
                                                                                   i∈1..n
                                               = n + 3 + comp(L[[P ]])
- Assignment. It is immediate to see that:

                   comp(L[[gain(x, y, gt)]])                = comp(L[[drop(x)]]) = 1
                   comp(L[[assg(x, y, z, gt)]])             = 7

  Hence, comp(assign) = comp(L[[wrap(assg(x, y, z, gt), G, z)]]) = 7 + n + 3 =
  n + 10 where n is the number of elements in G. Observe that, when there are no group
  permissions, the wrap is not necessary and the complexity is the same as for decompos-
  ing L[[assg(x, y, z, gt)]], which is 7.

- Axioms. The upgrade and downgrade axioms are negative formulas. Decomposing them
  has depth 1.

- Method definition. Let m be the number of parameters of a method and suppose that,
  when consuming access permissions, one has to upgrade or downgrade r of them. Then,
  comp(consume) = r + (m + 1) + 1, and
                                               ∆
                comp(L[[c m(x, ye, z) = PM ]]) = r + m + 4 + comp(L[[Body]])

  where Body is the body of the method (see Rule RMDEF ). On the other hand,

                         comp(L[[Body]]) = comp(L[[S[[b
                                                      s]]z ]]) + m + r + 4
32                                       Olarte, Pimentel and Rueda

- Constructor. With r and m as before, we have
                                                  ∆
          comp(L[[c(x, ye, z, g1 , ..., gk ) = PC ]]) = 2r + 2m + comp(L[[S[[b
                                                                             s]]z ]]) + 11

Theorem 5.2 (Complexity)
Let ∆ be a theory containing the definition clauses for method and constructor definitions,
the definition of assg and the upgrade and downgrade axioms. Let F be the formula
interpreting the main program and G be a formula interpreting a property to be proven. It
is decidable whether or not the sequent ! ∆, F −→ G is provable. In fact, if such a sequent
is provable, then its proof is bounded in ILLF by the depth comp(F ) + 1.

Proof
First of all, note that, since there are no circular recursive definitions (see Remark 2.1),
methods are simply unfolded. Moreover, as carefully described above, the complexity of
such method calls is taken into account in the complexity of the outer method definition
(see L[[S[[b
           s]]z ]]). This means that, whenever a method, constructor or an axiom is called
in ∆ via F , its complexity is already computed in the complexity procedure we have just
described. Due to the focusing discipline, proving a sequent in AP is equivalent to de-
composing its formulas completely. Therefore, the complexity of the proof of the sequent
! ∆, F −→ G is completely determined by the complexity of decomposing F plus the final
focusing in G, which is a purely positive formula.


                          5.5 Alcove Prover and Verification of Properties
In the following, we explain our verification technique for three different kind of properties:
deadlock detection; the ability of methods to run concurrently; and correctness (whether
programs adhere to their specifications or not). Recall, from Example 4.4, that we have
added to the predicates act(·), run(·), end(·) extra parameters to signalize the variable
that called the method, the name of the method and the number of line of the source pro-
gram. Then, for instance, in Example 5.1, the definition of the constructor looks like
                                    ∆
     collection collection(x, z, l) = ∃x...act(x,0 collection collection0 , l, z) → run(x,0 collection collection0 , l, z);
                                      ....run(x,0 collection collection0 , l, z) → ! end(x,0 collection collection0 , l, z)

   and the encoding of, e.g, line 10 in Figure 1, is collection collection(x, z, 10).
Deadlock Detection. Consider Example 4.5. We already showed that this code leads to
a deadlock since s cannot upgrade its unique permission to execute c.compStats(s). We
are then interested in providing a proof to the programmer showing that the code leads
to a deadlock. For doing this, let D[[Def ]] be the process definitions for the methods and
constructors of the example plus the definition of assignment. Let st be the main pro-
gram and consider the lcc program D[[Def ]].S[[st]]z . According to the definition of S[[·]]
and D[[·]], we know that, for some z and c, end(c,0 collection compStats0 , 15, z) will be
added to the store only when the statement c.compStats(svar) (in line 15) is successfully
executed. The translation of this program will give rise to the theory ∆ and the formula
F described in Example 5.1. The verification technique consists in showing that the se-
quent ! ∆, F −→ ∃z, c.end(c,0 collection compStats0 , 15, z) ⊗ > is not provable. This
      A Concurrent Constraint Programming Interpretation of Access Permissions              33

verification is done automatically by using Alcove-Prover, a theorem prover for ILLF de-
veloped in Teyjus and integrated to the tool described in Section 4.3. Basically, we look
for proofs with depth less or equal to 38, given by the depth of F . In this case, the prover
fails, thus showing that the process S[[st]]z cannot reach a store entailing the constraint
∃z, c.end(c,0 collection compStats0 , 15, z).
   The URL of the Alcove tool includes the output of the theorem prover and the lcc
interpreter for this example. It is worth noticing that the lcc interpreter only computes a
possible trace of the program while the theorem prover is able to check all the reachable
configurations for the same program. The Alcove prover is completely faithful to the ILLF
fragment presented in Section 5.3.
   The use of “animators” and provers is complementary. Existing formal models for sys-
tem construction, such as the Rodin ((Abrial et al. 2010)) tool for the event B modeling
language, usually include both. The idea is that by using the animator the user gain a global
understanding of the behavior of the program before attempting the proof of more precise
desirable properties. This usually avoids frustrations in trying to figure out corrections of
the model to discharge unproved properties.

Concurrency Analysis. Consider the following lcc agents
             P   =   act(z1 ) k act(z1 ) → (run(z1 ) ⊗ sync(z1 )) k run(z1 ) → ! end(z1 )
             Q   =   sync(z1 ) → act(z2 ) k act(z2 ) → run(z2 ) k run(z2 ) → ! end(z2 )

These processes represent an abstraction of the encoding of two statements s1 and s2 such
that s2 must wait until s1 releases the program control by adding sync(z1 ). It is easy
to see that from the initial configuration γ = h∅; P k Q; 1i we always end up in the
final configuration γ 0 = h∅; ∅; ! end(z1 ) ⊗ ! end(z2 )ii showing that both s1 and s2 were
successfully executed. Nevertheless, depending on the scheduler, we may observe different
intermediate configurations. For instance, if all the processes in P are first selected for
execution, we shall observe the derivation:
                 γ   −→∗    h∅; run(z1 ) ⊗ sync(z1 ) k run(z1 ) → ! end(z1 ) k Q; 1i
                     −→∗    h∅; run(z1 ) → ! end(z1 ) k Q; run(z1 ) ⊗ sync(z1 )i
                     −→∗    h∅; Q; ! end(z1 )i −→∗ γ 0

On the other side, an interleaved execution of P and Q may be

                 γ   −→∗    h∅; run(z1 ) ⊗ sync(z1 ) k run(z1 ) → ! end(z1 ) k Q; 1i
                     −→∗    h∅; P 0 k Q0 ; run(z1 ) ⊗ act(z2 )i
                     −→∗    h∅; P 0 k Q00 ; run(z1 ) ⊗ run(z2 )i −→∗ γ 0

   where P 0 = run(z1 ) → ! end(z1 ), Q0 = act(z2 ) → (run(z2 ) ⊗ sync(z2 ) k Q00 )
and Q00 = run(z2 ) → ! end(z2 ). Unlike the first derivation, in the second one we were
able to observe the store run(z1 ) ⊗ run(z2 ) representing the fact that both s1 and s2 were
executed concurrently.
   From the point of view of the lcc interpreter, the two derivations above are admissi-
ble. This means that the fact of not observing in a trace the concurrent execution of two
statements does not imply that they have to be sequentialized due to the AP dependencies.
   We can rely on the logical view of processes to verify whether it is possible for two
statements to run concurrently. For instance, consider the Example 4.4 and let F be the
34                                Olarte, Pimentel and Rueda

resulting ILL formula. The following sequent turns out to be provable:
         ! ∆, F −→     ∃z1 , z2 , c, s(run(c,0 collection print0 , 13, z1 )⊗
                                       run(c,0 collection compStats0 , 14, z2 )) ⊗ >
while the following one is not:
     ! ∆, F −→     ∃z1 , z2 , c, s(run(c,0 collection compStats0 , 14, z1 )⊗
                                   run(c,0 collection removeDuplicates0 , 15, z2 )) ⊗ >
  i.e., regardless the scheduling policy, the program will not generate a trace where compStats
and removeDuplicates run concurrently.

Verifying a Method Specification. Finally, assume that class collection has a field a and
we define the following method
     mistake() unq(this)=>unq(this){
        this.a<g>:=this}

   This method requires that the unique permission to the caller must be restored to the
environment. Nevertheless, the implementation of the method splits the unique permission
into two share permissions, one for the field a and another for the caller (Rule RALIAS ).
Then, the axiom upgrade1 cannot be used to recover the unique permission and the ask
agent in definition r env remains blocked. An analysis similar to that of deadlocks will
warn the programmer about this. In general, what we need is to prove sequents of the shape
! ∆, Γ −→ ∃c, z, l.end(c,0 method0 , l, z) ⊗ > where Γ contains an atomic formula needed
to start the execution of the method (i.e., a formula of the shape c method(x, · · · )) and also
the atomic formulas guaranteeing that the method can be executed (ref(x, o, unq, ndg),
ct(o, s(0)) for the method mistake). This can be done, for instance, by letting Γ =
L[[S[[st]]]] where st is a dummy main program that creates an instance of collection
and then calls the method mistake. In this case, the prover answers negatively to the query
! ∆, L[[S[[st]]]] −→ ∃c, z, l.end(c,0 collection mistake0 , l, z) ⊗ >, showing that, even sat-
isfying the preconditions of the method mistake , it cannot finish its execution.


                                       6 Applications
In this section we present two compelling examples of the use of our verification tech-
niques. One is the well-known mutual exclusion problem where two (or more) processes
compete for access to a critical section. In our example there are two critical sections with
exclusive access. The other models a producer and a consumer processes concurrently up-
dating a data structure.


                       6.1 Two Critical Zones Management System
Assume the class definitions for a two critical zones management system in Figure 17.
There are three classes, lock (line 1), process (line 4) and cs (line 7). Each critical
section has a private lock managed by an object of the class cs. When a process wants
to enter the critical section i ∈ {1, 2}, it tries first to invoke the method acqi (lines 11
and 15) of the cs manager. If successful, the process obtains a lock (i.e. an object of class
        A Concurrent Constraint Programming Interpretation of Access Permissions             35

   1   class lock <g> {
   2     lock() none(this) => unq(this) {}
   3     enter(process b) unq(this), shr : g(b) => unq(this), shr : g(b){} }
   4   class process <g>{
   5     attr lock<g> lock1, lock<g> lock2, cs<g> cs1, cs<g> cs2
   6     process() none(this) => unq(this) {} }
   7   class cs <g>{
   8     attr lock<g> mylock
   9     cs() none(this) => unq(this) {
  10        this.mylock := new lock<g>()}
  11     acq1(process b,lock l)unq(this),shr:g(b),none(l)=>shr:g(this),shr:g(b),unq(l){
  12           l <g>:= this.mylock
  13           b.cs1 <g> := this
  14           this.mylock <g>:= null }
  15     acq2(process b,lock l)unq(this),shr:g(b),none(l)=>shr:g(this),shr:g(b),unq(l){
  16           l<g> := this.mylock
  17           b.cs2 <g>:= this
  18           this.mylock <g>:= null }
  19     release1(lock a,process b)shr:g(this),unq(a),shr:g(b) => unq(this),none(a),shr
              :g(b){
  20           this.mylock <g>:= a
  21           b.cs1<g> := null
  22           a <g>:= null }
  23     release2(lock a, process b) shr:g(this),unq(a),shr:g(b) => unq(this),none(a),
              shr:g(b){
  24           this.mylock <g>:= a
  25           b.cs2 <g>:= null
  26           a <g>:= null } }


             Fig. 17: Class definitions for a two critical zones management system.


lock) that it uses then to enter that critical zone (lines 12 and 16). When the process wants
to leave the critical zone, it invokes the method releasei (lines 19 and 23). This releases
ownership of the critical section lock.
   Method acqi has three parameters: this (i.e., the cs manager), b the process wanting
to enter the critical zone and l, a field of b that will hold the lock of the cs supplied by the
manager. Since this has unique permission, only one reference to the manager object can
exist for acqi to be invoked. The body of method acqi stores the lock in l and a reference
to the manager in field cs1 or cs2 of b, depending on whether the lock for cs1 or for
cs2 is requested. Storing this reference to the manager implies that it cannot longer have
unique permission, so the output permission for this becomes shared. Moreover, l holds
now the only reference to the private lock of the manager, so its output permission becomes
unique. The effect is that field lock1 or lock2 of object b uniquely acquires the section
lock. The method enter (line 3) requires a unique permission on the lock. This ensures
that only one process has a reference to the lock at any given time when entering the
critical section. The method releasei restores conditions as they were before invocation
to acqi, i.e. the manager regains the unique permission and stores a unique reference to
its private lock. Process object fields loose the lock and the reference to the manager.
   Assume now the main code in Figure 18 (a) where there are two section manager objects
cs1 and cs2. There are also two processes, p1 and p2. Consider the situation where p1
acquires the lock from cs1 (line 9) and enters (line 10). Then p2 acquires the lock from
cs2 and enters (line 11-12). Now, p2 tries to acquire the lock from cs2 (line 13), but
this is not possible because cs1 has no longer a unique permission and execution blocks.
Alcove reports this situation:
   1   ...
36                                      Olarte, Pimentel and Rueda
          1   main () {
          2    group<g>
                                                          1    ... // constructors
          3    let cs x, cs w,
                                                          2    cs1.acq1(p1, p1.lock1)
          4         process y, process z in
                                                          3    p1.lock1.enter(p1)
          5          cs1:= new cs<g>()
                                                          4    cs2.acq2(p2, p2.lock2)
          6          cs2 := new cs<g>()
                                                          5    p2.lock2.enter(p2)
          7          p1 := new process<g>()
                                                          6    cs1.release1(p1.lock1, p1)
          8          p2 := new process<g>()
                                                          7    cs1.acq1(p2, p2.lock1)
          9          cs1.acq1(p1, p1.lock1)
                                                          8    p2.lock1.enter(p2)
         10          p1.lock1.enter(p1)
                                                          9    cs2.release2(p2.lock2, p2)
         11          cs2.acq2(p2, p2.lock2)
                                                         10    cs2.acq2(p1, p1.lock2)
         12          p2.lock2.enter(p2)
                                                         11    p1.lock2.enter(p1)
         13          cs1.acq1(p2, p2.lock1)
                                                         12    cs1.release1(p2.lock1, p2)
         14          p2.lock1.enter(p2)
                                                         13    cs2.release2(p1.lock2, p1)
         15          cs2.acq2(p1, p1.lock2)
                                                         14   end }
         16          p1.lock2.enter(p1)
         17        end }


                    (a) Deadlock code                           (b) Deadlock free code

                    Fig. 18: Main codes for the critical zone management system


     2    calling(X_6136,cs_acq1,line_71 (Z_PAR_18116))
     3    ...
     4    [FAIL] Token ok not found. End of the program not reached.

  Consider now the program in Figure 18 (b) where processes leave the critical section
before attempting to acquire another lock. In this case, all invocations run without blockage
and Alcove successfully finishes the analysis:
     1    ...
     2    ended(X_6152,cs_release1,line_113 (Z_PAR_24136))
     3    ended(W_7153,cs_release2,line_114 (Z_PAR_25137))
     4    ok()
     5    3517 processes Created
     6
     7    [OK] Token ok found. End of the program reached.




                            6.2 Concurrent Producer-Consumer System
Figure 19 shows the class definitions for a producer-consumer system working concur-
rently over a buffer. Class buffer (line 1) represents the data structure with operations
for reading (line 3), writing (line 4) and removing the content of the buffer (line 5). Class
producerConsummer (line 14) provides methods for adding (produce) –line 19– and re-
move (consume) –line 24– elements from the data structure. Since these could be invoked
concurrently, the class implements a critical section (line 8) representing access to the el-
ement of the data structure the consumer or producer is working on. That is, producing or
consuming could in principle be simultaneous over different elements of the structure. To
keep the example simple, we assume a single critical section over the whole data structure.
   Class producerConsumer defines a group g for processes operating over the data struc-
ture (line 14). The group is used to manage permissions of all processes invoking methods
of the class. Since callers of produce and consume both have share group permissions
on g, they can be invoked concurrently. This can be seen in the main program (line 30).
Variable P C has unique permission over the producerConsumer object. This unique
permission is split (line 36) into share permissions for the group to allow producer and
        A Concurrent Constraint Programming Interpretation of Access Permissions         37

   1   class buffer<g>{
   2       buffer() none(this) => unq(this) { }
   3       read() shr : g(this) => shr : g(this) { }
   4       write()   shr : g(this) => shr : g(this) { }
   5       dispose() unq(this) => unq(this) { }}
   6   class lock {
   7        lock() none(this) => unq(this) {} }
   8   class cs <g>{
   9         cs() none(this) => unq(this) { }
  10         acq(lock l) shr : g(this), none(l) => shr : g(this), unq(l) {
  11                l := new lock() }
  12         release(lock l) shr:g(this), unq(l) => shr:g(this), none(l) {
  13                 l<g> := null } }
  14   class producerConsumer<g> {
  15     attr lock l, cs<g> c
  16     producerconsumer() none(this) => unq(this) {
  17        this.c := new cs<g>() // Initializing the critical section
  18     }
  19     produce(buffer<g> B) shr:g(this),shr:g(B) => shr:g(this), shr:g(B) {
  20          this.c.acq(this.l) // Getting a lock on the data structure
  21          B.write()
  22          this.c.release(this.l) //releasing the lock
  23           }
  24     consume(buffer<g> B)shr:g(this),shr:g(B)=>shr:g(this), shr:g(B) {
  25          this.c.acq(this.l) // Getting a lock on the data structure
  26          B.read()
  27          this.c.release(this.l)//releasing the lock
  28           }
  29     }
  30   main{
  31     group <g>
  32     let producerConsumer<g> PC, buffer<g> B in {
  33     B := new buffer <g>()
  34     PC := new producerConsumer<g>()
  35     // produce and consume running in parallel
  36     split<g>{
  37         PC.produce(B)
  38         PC.consume(B)
  39     } }}


             Fig. 19: AP Program for a concurrent producer-consumer system


consumer calls to run in parallel. Note, however, that simultaneous access to the buffer is
precluded by the need for each process to acquire the lock before (lines 20 and 25).
   As shown, in the excerpt of the Alcove’s output in Figure 20, the call to consume (line
4) is done while produce is still running (line 2). Note also that before executing write
(line 11), the method produce has to acquire the lock on the data structure (lines 5 and 9).
Similarly, the execution of read (line 23) (called by the consumer in line 20) has to wait
until the lock is released by the consumer (line 17) and acquired by the producer (lines 18
and 21).
   AP based languages like Æminium (Stork et al. 2009) provides abstractions to simplify
the (concurrent) access to share objects. For instance, in the example above, we locked the
buffer before executing the methods write and read (lines 21 and 26 in Figure 19). In
Æminium, it suffices to wrap the call to these methods into a atomic block of the form:
       atomic<g>{
        B.write()
       }

The Æminium runtime system guarantees that the execution of write on the object pointed
by B is isolated, i.e., other methods invoked on the same object must wait until the termi-
38                               Olarte, Pimentel and Rueda

     1   [...] calling(PC_660,producerconsumer_produce,line_58 (z_2347))
     2   running(PC_660,producerconsumer_produce,line_58 (z_2347))
     3   calling(u_117119,cs_acq,line_41 (z_par_219246))
     4   calling(PC_660,producerconsumer_consume,line_59 (z_2448))
     5   running(u_117119,cs_acq,line_41 (z_par_219246))
     6   calling(inner_294344,lock_lock,line 24 (z_par_307308))
     7   calling(inner_200289,buffer_write,line_42 (z_par_220247))
     8   running(PC_660,producerconsumer_consume,line_59 (z_2448))
     9   running(inner_294344,lock_lock,line 24 (z_par_307308))
  10     calling(u_117119,cs_acq,line_46 (z_par_368395))
  11     running(inner_200289,buffer_write,line_42 (z_par_220247))
  12     ended(inner_294344,lock_lock,line 24 (z_par_307308))
  13     calling(u_117119,cs_release,line_43 (z_par_221248))
  14     ended(inner_200289,buffer_write,line_42 (z_par_220247))
  15     running(u_117119,cs_release,line_43 (z_par_221248))
  16     ended(u_117119,cs_acq,line_41 (z_par_219246))
  17     ended(u_117119,cs_release,line_43 (z_par_221248))
  18     running(u_117119,cs_acq,line_46 (z_par_368395))
  19     calling(inner_516566,lock_lock,line 24 (z_par_529530))
  20     calling(inner_349438,buffer_read,line_47 (z_par_369396))
  21     running(inner_516566,lock_lock,line 24 (z_par_529530))
  22     ended(PC_660,producerconsumer_produce,line_58 (z_2347))
  23     running(inner_349438,buffer_read,line_47 (z_par_369396)) [...]


           Fig. 20: Excerpt of Alcove’s output for the Producer-Consumer Program.


nation of write. We note that the behavior of atomic blocks relies completely on the
runtime system. Since we are interested in the static analysis of AP programs, we did not
considered atomic blocks in the grammar of Figure 3. Note also that what we can analyze
statically is whether methods produce (line 19) and consume (line 24) can acquire a share
permission on the buffer B.


                                   7 Concluding Remarks
We presented an approach based on lcc for specifying and verifying programs annotated
with access permissions. Program statements are modeled as lcc agents that faithfully rep-
resent the statement permissions flow. The declarative reading of lcc agents as formulas in
intuitionistic linear logic permits verifying properties such as deadlocks, the admissibility
of parallel executions, and whether methods are correct w.r.t. their AP specifications. Cen-
tral to our verification approach is the synchronization mechanism based on constraints,
combined with the logical interpretation of lcc into the focused system ILLF.
   A good strategy for understanding the behavior of a concurrent program is running a
simulator able to observe the evolution of its processes, hence having a better glance of the
global program behavior. Then, a prover able to verify formally various properties can be
executed. For this reason, we have automated our specification and verification approach
as the Alcove tool. Using this tool we were able, for instance, to verify the critical zone
management system and the producer-consumer system presented in Section 6. The reader
can find these and other examples at the Alcove tool web-site. The results and techniques
presented here are certainly a novel application for ccp, and they will open a new window
for the automatic verification of (object-oriented) concurrent programs.

Related and Future work. ccp-based calculi have been extensively used to reason about
concurrent systems in different scenarios such as system biology, security protocols, mul-
      A Concurrent Constraint Programming Interpretation of Access Permissions           39

timedia interaction systems, just to name a few. The reader may find in (Olarte et al. 2013)
a survey of models and applications of ccp. A work related to ours is (Jagadeesan et al.
2005), where the authors propose a timed-ccp model for role-based access control in
distributed systems. The authors combine constraint reasoning and temporal logic model-
checking to verify when a resource (e.g. a directory in a file system) can be accessed.
We should also mention the work in (Nigam 2012) where linear authorization logics are
used to specify access control policies that may mention the affirmations, possessions and
knowledge of principals. In the above mentioned works, access policies are used to control
and restrict the use of resources in a distributed environment but they do not deal with the
verification of a (concurrent) programming language.
   Languages like Æminium (Stork et al. 2009) and Plaid (Sunshine et al. 2011) offer a se-
ries of guarantees such as (1) absence of AP usage protocol violation at run time; (2) when
a program has deterministic results and (3) whether programs are free of race conditions
on the abstract state of the objects (Bierhoff and Aldrich 2007; Boyland 2003). Roughly,
type-checking rules generate the needed information to build the graph of dependencies
among the statements in the program. Such annotations are then used by the runtime en-
vironment to determine the pieces of code that can be executed in parallel (Stork et al.
2014). Well typed programs are free of race condition by either enforcing synchronization
when accessing shared data or by correctly computing dependencies. However, well typed
programs are not necessarily deadlock free. Hence, our developments are complementary
to those works and provide additional reasoning techniques for AP programs.
   Somewhat surprisingly, even though in (Stork et al. 2014) it is mentioned that “access
permissions follow the rules of linear logic”, the authors did not go further on this idea.
Our linear logic encodings can be seen as the first logic semantics for AP. As showed in
this paper, such declarative reading of AP allows to perform interesting static analyses on
AP based programs.
   The constraint system we propose to model the downgrade and upgrade of axioms was
inspired by the work of fractional permissions in (Boyland 2003) (see also (Bierhoff and
Aldrich 2007)). Fractional in this setting means that an AP can be split into several more
relaxed permissions and then joined back to form a more restrictive permission. For in-
stance, a unique permission can be split into two share permissions of weight k/2. There-
fore, to recover a unique permission, it is necessary to have two k/2-share permissions.
The constraint system described in this paper keeps explicitly the information about the
fractions by using the predicate ct(·).
   Chalice (Leino 2010) is a program verifier for OO concurrent programs that uses per-
missions to control memory accesses. Unlike Æminium and Plaid, concurrency in Chalice
is explicitly stated by the user by means of execution threads.
   The language Rust (https://www.rust-lang.org/) provides mechanisms to
avoid data races. These do not use APs but rely on types. Type mut (mutable) works
similarly as a unq permission. A data structure defined with type mut is claimed own-
ership by the first thread using it, so it cannot be taken concurrently by another thread.
The compiler checks this statically. Type Arc allows the data structure to be shared among
threads, but then it cannot be a mutable structure. This is then similar to imm permissions.
Type Arc can be combined with mutex to have a mutable structure that can be shared. A
lock mechanism is available for the user to control simultaneous accesses. As opposed to
40                                Olarte, Pimentel and Rueda

permissions, however, there is no upgrading/downgrading of types. Hence, AP and DGAP
provide, in principle, more flexible mechanisms to express concurrent behaviors. In (Ull-
rich 2016) a translation of Rust programs into the Lean prover to verify program correct-
ness is described. As far as we know, however, no verification of the kind we presented
here is available for Rust.
   AP annotations in concurrent-by-default OO languages can be enhanced with the notion
of typestates (Bierhoff and Aldrich 2007; Beckman et al. 2008). Typestates describe ab-
stract states in the form of state-machines, thus defining a usage protocol (or contract) of
objects. For instance, consider the class File with states opened and closed. The signa-
ture of the method open can be specified as the agent unq(this) ⊗ closed(this) →
unq(this) ⊗ opened(this). The general idea is to verify whether a program follows
correctly the usage protocol defined by the class. For example, calling the method read
on a closed file leads to an error. Typestates then impose certain order in which meth-
ods can be called. The approach our paper defines can be extended to deal with typestates
annotations, thus widening its applicability.
   The work in (Naden et al. 2012) defines more specific systems and rules for access
permissions to provide for borrowing permissions. This approach aims at dealing more ef-
fectively with local variable aliasing, and with how permissions flow from the environment
to method formal parameters. Considering these systems in Alcove amounts to refine our
model of permissions in Section 4. Verification techniques should remain the same.

Acknowledgments This work has been partially supported by CNPq and CAPES/Colcien-
cias/INRIA’s project STIC AmSud. We thank the anonymous reviewers for their valuable
comments on an earlier draft of this paper.


                                           References
A BRIAL , J.-R., B UTLER , M. J., H ALLERSTEDE , S., H OANG , T. S., M EHTA , F., AND VOISIN , L.
   2010. Rodin: an open toolset for modelling and reasoning in event-b. STTT 12, 6, 447–466.
A NDREOLI , J.-M. 1992. Logic programming with focusing proofs in linear logic. J. Log. Com-
   put. 2, 3, 297–347.
B ECKMAN , N. E., B IERHOFF , K., AND A LDRICH , J. 2008. Verifying correct usage of atomic
   blocks and typestate. In OOPSLA, G. E. Harris, Ed. ACM, 227–244.
B IERHOFF , K. AND A LDRICH , J. 2007. Modular typestate checking of aliased objects. In OOPSLA,
   R. P. Gabriel, D. F. Bacon, C. V. Lopes, and G. L. S. Jr., Eds. ACM, 301–320.
B OYLAND , J. 2003. Checking interference with fractional permissions. In SAS, R. Cousot, Ed.
   Lecture Notes in Computer Science, vol. 2694. Springer, 55–72.
B OYLAND , J., N OBLE , J., AND R ETERT, W. 2001. Capabilities for sharing: A generalisation of
   uniqueness and read-only. In ECOOP, J. L. Knudsen, Ed. Lecture Notes in Computer Science,
   vol. 2072. Springer, 2–27.
DE B OER , F. S., G ABBRIELLI , M., M ARCHIORI , E., AND PALAMIDESSI , C. 1997. Proving con-
   current constraint programs correct. ACM Trans. Program. Lang. Syst. 19, 5, 685–725.
FAGES , F., RUET, P., AND S OLIMAN , S. 2001. Linear concurrent constraint programming: Opera-
   tional and phase semantics. Inf. Comput. 165, 1, 14–41.
G IRARD , J.-Y. 1987. Linear logic. Theor. Comput. Sci. 50, 1–102.
H AEMMERL É , R. 2011. Observational equivalences for linear logic concurrent constraint languages.
   TPLP 11, 4-5, 469–485.
       A Concurrent Constraint Programming Interpretation of Access Permissions                 41

I GARASHI , A., P IERCE , B. C., AND WADLER , P. 2001. Featherweight java: a minimal core calculus
   for java and GJ. ACM Trans. Program. Lang. Syst. 23, 3, 396–450.
JAGADEESAN , R., M ARRERO , W., P ITCHER , C., AND S ARASWAT, V. A. 2005. Timed constraint
   programming: a declarative approach to usage control. In PPDP, P. Barahona and A. P. Felty, Eds.
   ACM, 164–175.
L EINO , K. R. M. 1998. Data groups: Specifying the modification of extended state. In OOPSLA,
   B. N. Freeman-Benson and C. Chambers, Eds. ACM, 144–153.
L EINO , K. R. M. 2010. Verifying concurrent programs with Chalice. In VMCAI, G. Barthe and
   M. V. Hermenegildo, Eds. Lecture Notes in Computer Science, vol. 5944. Springer, 2.
L INCOLN , P., M ITCHELL , J. C., S CEDROV, A., AND S HANKAR , N. 1992. Decision problems for
   propositional linear logic. Ann. Pure Appl. Logic 56, 1-3, 239–311.
M ARTINEZ , T. 2010. Semantics-preserving translations between linear concurrent constraint pro-
   gramming and constraint handling rules. In PPDP, T. Kutsia, W. Schreiner, and M. Fernández,
   Eds. ACM, 57–66.
M ILLER , D. AND NADATHUR , G. 2012. Programming with Higher-Order Logic. Cambridge Uni-
   versity Press.
NADATHUR , G. AND M ILLER , D. 1988. An overview of lambda-prolog. In Logic Programming,
   Proceedings of the Fifth International Conference and Symposium, Seattle, Washington, August
   15-19, 1988 (2 Volumes), R. A. Kowalski and K. A. Bowen, Eds. MIT Press, 810–827.
NADEN , K., B OCCHINO , R., A LDRICH , J., AND B IERHOFF , K. 2012. A type system for borrowing
   permissions. In POPL, J. Field and M. Hicks, Eds. ACM, 557–570.
N IELSEN , M., PALAMIDESSI , C., AND VALENCIA , F. D. 2002. Temporal concurrent constraint
   programming: Denotation, logic and applications. Nord. J. Comput. 9, 1, 145–188.
N IGAM , V. 2012. On the complexity of linear authorization logics. In LICS. IEEE, 511–520.
O LARTE , C. AND P IMENTEL , E. 2017. On concurrent behaviors and focusing in linear logic. Theor.
   Comput. Sci. 685, 46–64.
O LARTE , C., P IMENTEL , E., RUEDA , C., AND C ATA ÑO , N. 2012. A linear concurrent con-
   straint approach for the automatic verification of access permissions. In PPDP, D. D. Schreye,
   G. Janssens, and A. King, Eds. ACM, 207–216.
O LARTE , C., RUEDA , C., AND VALENCIA , F. D. 2013. Models and emerging trends of concurrent
   constraint programming. Constraints 18, 535–578.
P OTTIER , F. AND P ROTZENKO , J. 2013. Programming with permissions in mezzo. SIGPLAN
   Not. 48, 9 (Sept.), 173–184.
S ARASWAT, V. A. 1993. Concurrent Constraint Programming. MIT Press.
S ARASWAT, V. A. AND R INARD , M. C. 1990. Concurrent constraint programming. In POPL, F. E.
   Allen, Ed. ACM Press, 232–245.
S ARASWAT, V. A., R INARD , M. C., AND PANANGADEN , P. 1991. Semantic foundations of con-
   current constraint programming. In POPL, D. S. Wise, Ed. ACM Press, 333–352.
S TORK , S., M ARQUES , P., AND A LDRICH , J. 2009. Concurrency by default: using permissions to
   express dataflow in stateful programs. In OOPSLA Companion, S. Arora and G. T. Leavens, Eds.
   ACM, 933–940.
S TORK , S., NADEN , K., S UNSHINE , J., M OHR , M., F ONSECA , A., M ARQUES , P., AND A LDRICH ,
   J. 2014. Æminium: A permission-based concurrent-by-default programming language approach.
   ACM Trans. Program. Lang. Syst. 36, 1, 2.
S UNSHINE , J., NADEN , K., S TORK , S., A LDRICH , J., AND TANTER , É. 2011. First-class state
   change in plaid. In OOPSLA, C. V. Lopes and K. Fisher, Eds. ACM, 713–732.
U LLRICH , S. A. 2016. Simple Verification of Rust Programs via Functional Purification. Master’s
   Thesis, Karlsruher Institut für Technologie (KIT).
