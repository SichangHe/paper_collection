                                                       Review of Recent Heap Specification and
                                                               Verification Techniques
                                                                   (1st draft submitted on 12th March 2015; journaled 2019, self-translated into English)


                                                                                                   René Haberland
                                                                                                Independent researcher
                                                       Saint Petersburg Electrotechnical University                     Carl Zeiss Research and Development
                                                                  Prof. Popova Street 5,                              Semiconductor Manufacturing Technology
arXiv:1910.10176v2 [cs.LO] 24 Mar 2022




                                                             197022 Saint Petersburg, Russia                                73447 Oberkochen, Germany
                                                                   haberland1@mail.ru                                         rene.haberland@zeiss.com


                                            Abstract—The article provides an overview of the existing                                          stack
                                         methods of dynamic memory verification; a comparative analysis
                                         is carried out; the applicability for solving problems of control,
                                                                                                                                               heap
                                         monitoring, and verification of dynamic memory is evaluated.                                   uninitialised data
                                         This article is divided into eight sections. The first section                                       (bss)
                                         introduces formal verification, followed by a section that discusses                            initialised data
                                         dynamic memory management problems. The third section
                                         discusses Hoare’s calculus resumed by heap transformations to                                       (data)
                                         the stack. The fifth and sixth sections introduce the concept of                                 program code
                                         dynamic memory shape analysis and the rotation of pointers.                                         (text)
                                         The seventh is on separation logic. The last section discusses
                                                                                                                             Fig. 1. Typical memory regions for a process
                                         possible areas of further research, particularly the recognition
                                         at recording level of various instances of objects; automation of
                                         proofs; ”hot” code, that is, software code that updates itself when
                                         the program runs; expanding intuitiveness, for instance, on proof
                                         explanations.                                                          values. Between stack and heap, there is a floating border.
                                                                                                                So, the stack grows when before entering some procedure and
                                         Keywords. dynamic memory verification, Hoare calculus,                 shrinks when leaving it. More accurately, the stack alters, and
                                         distributed memory, pointers arithmetics.                              for control purposes, the stack index pointing to the actual
                                                                                                                stack frame is of most interest. Local variables (or locals)
                                                                I. I NTRODUCTION
                                                                                                                are automatically accommodated into the stack frame and
                                            For over a couple of decades, mistakes based upon dynamic           freed when leaving. So, locals are automatically allocated and
                                         memory remained crucial during software engineering. Error             deallocated whilst program execution. Unlike stack, the heap is
                                         localisation is challenging since diagnosed error locations are        allocated manually and remains unless freed manually. In 32-
                                         too often too far from the actual cause. Errors affect the overall     bit systems supporting virtual memory are based on segmenta-
                                         behaviour of an application, its performance and correctness.          tion. It implies that accessory OS control units access memory
                                            This paper overviews and compares existing techniques on            cells in segments. In 64-bit OSes segmentation separators still
                                         dynamic memory verification. It evaluates applicability for            exist, though they are not much used anymore since the need
                                         practical verification control. Before introducing to dynamic          for segmentation steadily diminishes in the case of sufficiently
                                         memory models, research objectives shall be announced first.           big enough address spaces.
                                            Some running process allocates a region of dynamic mem-                A verification system is a formal checking process, origi-
                                         ory by the operating system [1]. The region’s memory is                nated from Hoare [2], which is used in algebraic and logical
                                         allocated on demand (e.g. by malloc or new) and is denoted             formulae and logical rules for the proof of (in-)correctness
                                         as ”heap” in fig.1.                                                    obeying some given specification (so-called ”Hoare calculus”).
                                            For clarity, first, a process’s memory region shall in the             Let us consider the following C program
                                         following refer to ”dynamic memory”. Second, a logical data
                                         structure (in the most common case, a graph) being mapped              list_elem *temp;    list_elem *y = NULL;
                                         onto a continuous logical memory space refers to ”heap”.               while (x != NULL) {
                                            Program code contains processor instructions, namely op-              temp = x->next;
                                         codes with operands. The initialised data region contains                x->next = y;
                                         program variables having initial denotational values before              y = x;
                                         that program is run. Conversely, uninitialised variables are             x = temp;
                                         global and non-local variables that are not assigned initial           }
                                                    o❲❲❲❲❲❲++                                heap elements are considered garbage and shall be dismissed.
                                                           //           1
                                                       GF                                    Pointers sharing at least a typical heap cell are called ”aliases”.
                                                                        •                       Unsurprisingly, working with dynamic memory imposes
    o         // GFED
                    @ABC
                     ’b’             o2                                                 ED
                 ==                                                                          many practical issues despite its initial vague complexity.
                         ❆❆                                             •
                                                                                  ED BC
            ④④             ❆                                                                 Those were firstly classified by Miller [4], and they remain
          ④④                ❆❆
        ④④                    ❆❆                                            oo               up to date. The paper [5] titles dynamic memory problems as
      ④④                        ❆                                456
 HIJK
 ONML
  333                            // ?>=<
                                    89:;
                                     D                      @A                    BC         one of the most challenging issues during programming and
                                                                                             software engineering. It contains an illustrative comparison
 Fig. 2. Heap o,o2                                 Fig. 3. Stacked local                     of software development tools under Linux and Windows.
                                                                                             Essentially, it was found that Linux software components
                                                                                             contain fewer errors than corresponding components being
  which inverts a linked list defined as                                                     implemented in Windows. The success can be explained by
struct list_elem{                                                                            the active support of the Linux community. Miller announces
   int data;                                                                                 that both invalid addressing and invalid boundaries are the
   list_elem *next;                                                                          most frequent error related to dynamic memory. However,
};                                                                                           frequently problems may not easily be located and may be
                                                                                             altered at different locations accidentally. For instance, if in-
  After each loop iteration, the dynamic memory and pointers                                 valid heap access causes an immediate crash, this is ideal from
x and y denote as                                                                            a diagnostic standpoint. In other cases, however, localising
     Iteration №1:                                                                           errors due to invalid pointer operations may become quite
               // 0 x:               // 1            // 2        // 3            // 0        challenging. One approach in reducing the complexity of the
      y:                                                                                     dynamic memory scope is transforming a heap into a stack
     Iteration №2:                                                                           (cf. sec.IV).
      y:       // 1           // 0   x:              // 2        // 3            // 0           Heap problems may be categorised by their features, for
                                                                                             instance, as follows:
     Iteration №3:
                                                                                               (i) memory leakage;
      y:       // 2           // 1          // 0     x:          // 3            // 0
                                                                                              (ii) inaccessible heap;
     Iteration №4:                                                                           (iii) invalid heap access;
               // 3           // 2          // 1            // 0 x:              // 0        (iv) deviation between given and expected data structures;
      y:
                                                                                              (v) aliasing and ”remote alteration”.
   When the program starts execution, x contains the initial                                     The following sections go into more depth on each of the
list, and y is empty. When finalising the loop, y contains the                               mentioned problem.
list in reverse order, and x becomes empty. Here we notice that
the semantics of this pretty simple program is far from trivial,                             A. Memory leakage
in any case. A specification’s main objective is to describe the
                                                                                               Let us consider the example
dynamic memory before and after a program runs.
                                                                                             MyClass object1=new MyClass();
                      II. P ROBLEM ACTUALITY                                                 ...
                                                                                             object1=new MyClass();
   The main difference between stack and heap is the storage
of data. The program manages stack (indirectly, but) auto-                                      Let us further assume there are no pointers that would point
matically at two locations: when entering and when leaving                                   to the previously allocated memory region between the first
a procedure. Heap is managed manually only using special                                     and second assignment of object1. According to Weihl
operators. The memory content alters permanently on each                                     [3], ”garbage” is defined as a heap that is not referenced
execution step. Heap can be denoted by an oriented graph                                     by any pointer. The first object of class MyClass is lost —
whose vertices are structures containing application-specific                                essentially, it just becomes garbage. If the object is no more
data and whose edges represent pointers. Fig.2 demonstrates                                  in need, it shall be recycled. Otherwise, repeatedly allocated
a typical heap, where fig.3 shows a stack containing the stack-                              regions may cause the applications and OS to fail. It may either
local variable o.                                                                            stop execution prematurely and just quit with some error or
   Heaps are built up stepwise. The size of a heap vertex is                                 continue and slow down the overall OS due to a search for
determined by its corresponding data type. Incremental built-                                free memory resources. Usually, the latter is hard to debug in
up implies alterations may remain unnoticed even if pointers                                 practice due to its non-deterministic behaviour.
are untouched. In C, heap vertices are managed by the program                                   Jones et al. [6] give a concise overview of garbage collection
statements malloc and free (cf. [3]). Pointers accommo-                                      and an in-depth discussion of recent techniques focused on
dated in dynamic memory have access to heap vertices and                                     multi-threaded garbage collection. Furthermore, estimates are
are syntactically described by heap expressions. Unreachable                                 made on the most promising methods.
   Appel [7] is most concerned about von-Neumann’s com-             an extended period and is referenced frequently, it should be
puter architecture regarding pushing and popping stack frames       relocated to a quicker memory region. The authors’ compre-
(cf. sec.IV). He is confident that dynamic memory can have          hensive research shows their chosen performance heuristics
significant performance advantages over stack (cf. [8], [9]).       approximate to an optimum. Garbage collection is used by
Appel’s multi-threaded approach utilises a ”copying garbage         default in programming languages like Java, C# and in many
collector” [6]. The collector is triggered only when data in        popular functional programming languages and is turned off
scope is altered, and the total amount of allocated data is         in ISO C and C++ [15].
multiple times greater than the remaining amount of free
                                                                    B. Invalid access / inaccessible memory
heap. Regardless of the age of the article [10], the distinction
between fast cache and slow but more memory remains up-                Incorrect memory access may occur whenever a procedure
to-date. Larson considers a ”condensed collector” operating in      is granted full access by pointer, even when the alteration may
dependency of the number of disposable regions (R), active          take place later (unintentionally). Let us consider the following
regions (A), and size of fast memory (H). He postulates             example
two optimal strategies (for performance) for allocation and         // object1 not constructed here
deallocation of dynamic memory:                                     MyClass object2=new MyClass();
   • maximisation of R, if A≪H does not hold;                       object2.ref=object1;
   • assigning R:=H, if A≪H.                                        // object1 constructed
   Apart from the restrictions in [7], there is one more related
to addressing: ”XOR”-linked data structures (see [11], [12])          There is a reference to object1, although it is not yet
do not allow efficiently locating garbage as described in [6].      constructed. This error is not detected during the second
It is mainly because heap regions (e.g. structures, pointers to     assignment but the first use of object2.ref.
linked list elements) addresses are no more absolute; they are      C. Incorrect memory access
relative.
                                                                       In the given examples, we are interested in invalid heap
   Assume — that AXOR denotes the finite linear address
                                                                    access. Let us assume an object reference to object1 is
space, then (AXOR , ⊕) denotes the group with well-known
                                                                    initialised and field ref equals NULL whilst running.
rules for associativity, neutral and inverse elements, and en-
closed operation ⊕ [13]. Any specified address of a dynamic         // object1.ref==null
memory may be calculated directly and inversely.                    value = (object1.ref).attribute1;
   For instance, given a and b, then a ⊕ (a ⊕ b) ≡ b, and
(a ⊕ (a ⊕ b)) ⊕ (a ⊕ b) ≡ b ⊕ (a ⊕ b) ≡ a. By applying                 Then, in the best case, the program fails, indicating incorrect
XOR-expressions, the second pointer may be skipped by an            access to the segment heap. During verification the input
auxiliary arithmetic operation (cf. [11], [12]). This saving may    program is checked for error until execution. If the given field
be helpful in collectors, especially in an embedded background      is not always initialised, this may imply uninitialised objects,
with a limited amount of memory. However, [11] contains             which must be avoided.
mistakes, and its calculation model presented is incomplete.           Also, incorrect access occurs due to incorrect heap ad-
Fortunately, a corrected variant may be found in [13].              dressing, as it may occur with arbitrary addressing. If access
   Meyer [9] suggests a permanently enduring garbage collec-        is granted strictly according to existing class fields, it only
tion. This installation can hardly be implemented in a single-      needs to be checked whether access always exists to dynamic
threaded environment due to a severe lack of resources causing      memory during runtime. If pointer access depends on an
unacceptable delays. Undoubtedly a better solution would be         arbitrary arithmetic expression being calculated on runtime,
to localise the reasons for garbage generation and rewrite          then checking dynamic memory becomes undecidable. The
the critical code section instead to avoid garbage in the first     most common case is rather uncomfortable. However, when
place. In that case, efforts in the collection would nullify.       restricting to apriori known class fields only, expressibility
In multi-threaded environments [6] impressively shows, may          does not suffer much (cf. sec.[16]). All heap regions need
work more efficient if the collector is turned on periodically      to be monitored to avoid incorrect access.
and if a realistic heuristic of estimated garbage determines that      Let us now consider the following example.
frequency. Otherwise, garbage collection may not redeem es-         D. Deviation from a data structure
timates even close. However, even in embedded environments,
                                                                      In the following example, some object is printed to the
memory steadily increases, so an optimal collector becomes
                                                                    console.
less and less critical after all by practical means, except leaks
that endanger the overall system stability. Hence, detecting        object1.next=object1;
”hot locations” is worth the effort — from a practical point of     ...
view, this is code enclosed in loops, which is often executed.      root=object1;
   The paper [14] suggests garbage collection by generation.        while(root.next!=null){
Generations depend on the frequency and duration certain              printf(%d, object.data);
heap entities are accommodated. If some object resides for            root=root.next;
}                                                                   from tampering, even if protecting it with an additional const
                                                                    keyword as shown for pointer pa2 in the following:
   If a simply-linked list with a specified start and end are
given, then the program can inductively be found to be              int *x;
correct. However, if the given data structure contains a cycle      int *good() { int *p = x ; return p; }
unexpectedly the calculus may become incorrect according to         int *bad() { int x = 55; return &x; }
the specification provided.
   Recommended references on object theory may be found in          void main(){
[17], [18]. There, an axiomatic formal base for object classes        int a=5, b=4;
is founded. According to Abadi and Cardelli, objects are              int *pa = &a;
instantiated classes, which may have different interpretations        const int *const pa2 = &a;
for subtypes of a class.                                              a = 77;
   In [19], objects are considered not as abstract data types but     pa2 = pa;
as simple records as defined by [20]. Abadi does not intro-         /*** ’ pa2 ’ is read - only ***/
duce recursively-defined classes and skips pointers nor object        printf(" *pa:%d, *pa2:%d \n" ,*pa, *pa2);
pointers (nor aliases). In the model, proposed objects are non-     /*** *pa==77, *pa2==77     ***/
sharing heap regions. Class types (T ) are defined recursively.       a = *&b;
Those are either integer or are compound. Compound types            /*** *const of pa2 is still no
are classes themselves that may be compound again. A class                guarantee for safety   ***/
object contains a set of unique fields and methods. Fields are        printf(" *pa:%d, *pa2:%d\n", *pa, *pa2);
of type T , and methods are of type Tj → Tj+1 → · · · → Tk .        /*** ! problem: *pa==4, *pa2==4    ***/
The check if an object is an instance of a class or subclass          x = (int*)malloc(10);
is defined element-wise of all class fields and methods. A            memset(x,7,sizeof(x));
unique result register can describe the states before and             printf("0x%x\n", *(good())); // OK
after a program statement. Recursively defined predicates are         printf("0x%x\n", *(bad())); // SEGV
disallowed by [21] since there are rigid theoretical boundaries     }
for that data model. In [22] a relaxation for that boundary            Second, the life span of variables and their values in a
is proposed defined over an algebraic ideal ring construction.      heap dramatically differs from stacked variables. So, assigning
However, this construction may lead to incorrect verifications      locals may be correct locally. However, when trying to access
due to multiple derivations for the recursive cases due to the      a previously freed stacked local address may lead to an
object combinator definition. This onerous restriction holds for    application halt depending on whether stack protection is
any practical.                                                      granted by the OS (refer to both functions good and bad
   Moreover, this model does not separate the heap and lacks        in the example).
fundamental incompleteness (cf. sec.III). Banerjee [23] pro-           When two pointers point to a shared heap cell, both pointers
poses a language that describes stacked objects only, and those     are aliases to each other. However, the fast and reliable
objects must be of one type (cf. [24], [8]). The approach in        detection of aliases remains an actual and open problem.
[23] (see sec.IV) moves all locals into the stack since pointers    When a procedure is called, there is always a ”callee”
are forbidden. Recursively-defined predicates over objects are      (inner) and a ”caller” (exterior) side. For instance, algorithms
forbidden. Global invariants are unique since they catch the        for inner analyses can efficiently be constructed with less
fixed dependencies between objects. Banerjee warns about the        effort, Muchnick’s algorithm family [29]. However, exterior
increasing abstraction problem and supports the initiative of       analyses may, in general, be very complex because the whole
predicates describing different aspects of an object.               transitive hull of calls needs to be analysed, which grows
   Both [25] and [26] categorise underpinning the object-           exponentially per caller level [30]. Another tricky question
oriented modelling ”Unified Modeling Language (UML)” [27].          relates to the decision of whether a pointer strictly aliases
Apart from the graphical modelling, ”Object Constraint Lan-         or not — where a general method may become imprecise,
guage (OCL)” [28] represents a textual record. Formulae in          ineffective or both. In practice, the ”GCC” and ”LLVM
OCL describe class objects and their dependencies. The given        Clang” both implement auxiliary compilation switches to
expressibility can be equivalent to the second-order typed λ-       resolve code optimisations, for instance, by facilitating the
calculus (as introduced by the ”System F” verifier). However,       -fstrictaliasing switch. The programmer may provide
”UML” and ”OCL”, which are modelling languages, cannot              the keyword        restrict           to indicate that passed
express aliases or pointers to objects in heaps — which is a        pointers may not be treated as unbound pointers. Although
significant limitation.                                             this is precisely the desired behaviour in over 95% of all
                                                                    cases, the remaining tiny percentage still may generally cause
E. Remote object alteration and aliases                             devastation if not treated correctly, which a compiler must
  The following example demonstrates two aspects. First,            by default take into consideration, causing worse code to
const does not necessarily protect the content of a heap cell       be generated than could be with that keyword. The given
keyword may be used with objects on a procedural level too                             III. H OARE C ALCULUS
which heavily may improve performance since the objects
usually will be flushed once leaving a procedure and do not            Hoare first introduced a formal calculus in 1969 related to
require further synchronisation between procedures [31].            specification and software verification [2]. It is fundamental
                                                                    up-to-date, and its basic theoretical approach has not changed
   Weihl [3] gives a broad introduction to aliases regardless       ever since, except extended multiple times. An axiomatic
of the article’s age (see later on). According to Weihl, alias      semantics and operational semantics are proposed as a toolbox
analysis approximates a pointer’s scope spanning an expo-           for describing programming languages. Hoare’s axiomatic se-
nential search space of locations that may tamper its content.      mantics denotes which rules are applied for an input program-
So, beyond a procedure’s body, the analysis when a pointer’s        ming language and which rules need to be applied to prove
content may be altered becomes much more complicated.               its correctness. It compares its intermediate denotations with
Here, the locations and the call itself need to be carefully        those of rules. If both state denotations match, a given program
analysed in a pointer’s continuation. Naturally, continuation       obeys a given specification. Otherwise, the program does not
evaluations are tractable. Weihl suggests a metric for alias        obey the rules for correctness. Hoare includes algebraic and
analysis tractability. It shall be noted here that metric ideally   logical assertions in expressions. In honour of Hoare, P {C}Q
should also be used to feedback a developer to schedule a           is called ”Hoare’s Triple”, which nowadays is often rewritten
reengineering task.                                                 to {P }C{Q}, where P denotes the precondition, C a program
   Muchnick [29] provides a succinct overview of existing and       statement, and Q denotes the postcondition.
                                                                                                                            A
previous alias analyses, including his methods. He divides             Assume, Γ denotes the set of logical rules of kind B   , where
the analyses into control graph dependent and independent           A denotes the antecedent, and B the consequent. An axiom is
techniques. He further divides the analyses by its outcomes,        a rule whose antecedent is a tautology in the considered area of
namely whether a pointer ”strictly is alias”, ”maybe alias”,        discussion. It can be noted as B , or as true → B. If a Hoare
and ”strictly no alias”.                                            triple is derivable syntactically from Γ, then it is written as
   Horwitz [32] boosts furthers Muchnick’s alias analysis by        Γ ⊢ {P }C{Q} or as ⊢Γ {P }C{Q}. If clear from its context,
introducing bit-vectors to encode the states ”alias/may alias”      only Γ is considered, then sometimes ⊢Γ can be dropped
and ”strictly no alias”. Furthermore, generalised analyses are      for simplicity. A Hoare triple is interpreted as a predicate.
found in [33]. Here, Khedker also uses bit-vectors for his most     This predicate is only determined when C terminates (or —
generalised control-flow based analyses. Khedker’s approaches       is a terminal in a more generalised way). The interpretation
are based on the well-known Floyd-Warshall algorithm for            is proper whenever the precondition P is true, statement C
checking reachability in directed graphs (cf. [34]). Moreover,      is run, and postcondition Q succeeds. Otherwise, the Hoare
the author of this article suggests Khedker’s approach shall be     triple is not correct. In case C does not terminate, the Hoare
further extended to incorporate ”SSA”-forms (cf. [35],[36])         triple is undefined. A Hoare triple interprets as false whenever
in the most general case. Naeem [37] seems to confirm my            a postcondition fails. The designers and test engineers define
personal opinion in a minor remark. Naeem further suggests          conditions. If Q is incorrect for a given program, any result
incorporating hash-tables in order to improve bit-vector oper-      obtained shall be doubtful and require further clarification. P
ations. Here, it must be noted that Naeem’s proposition is a        and Q are formulae describing the calculation state at any time.
desire to redefine alias analysis as such as a problem of ”SSA”.    So, there must be references to symbols in the calculation state,
The author of this paper strongly admits his proposition. At        variables and symbols in C. Although Hoare did not assert it
least, most definitely, further research is required. It would      himself, it seems highly plausible to use some formal logic to
almost certainly trim a whole phase of static analysis when         express and reason rules about a given program.
found tractable, causing heavy performance gains due to a              In 1969 Hoare noted that some program statements in C
full and more effective register referencing. So, notoriously       are much harder to describe than others and, as a direct
redundant copying from minor til big memory heap chunks             effect, much more demanding to prove its correctness. Such
may be dropped that are still required for security.                statements encompass labels, unconditional jumps, and un-
   Pavlu [38] divides alias analyses into two categories: ap-       bound parameters. Still, today this problem remains essential,
proaches based on ”unification” [39], which are more accurate       and further features emerge even more. Due to software
in finding aliases, and approaches based on ”approximation”,        modularisation, labels are often excluded in high-level pro-
which are less accurate but much more straightforward. The          gramming languages nowadays from verifications entirely. Apt
latter approaches can be considered a compromise rather than        [40] and Clarke [41] analysed unbound parameters in detail
a fully qualified exact solution. Whether an accurate or an         and found that this problem nearly vanished today in Algol-
approximate solution is efficient remains open after all. In        styled programming languages.
other words, it would be interesting to find a scenario where          In general, proof continues until all branches succeed with
aliases are not wholly excluded, but data structures may be         axioms or until proof can be refuted. The overall structure
altered, such that the modified memory chunk is caught inside       of proof is a tree. Whenever a cycle occurs in a proof, the
a procedure. The author of this paper believes this question        proof fails. If, however, previous subproofs are utilised, copy
has not yet been entirely covered.                                  subproofs can be skipped.
   A proof starts with a consequent and searches for matching        non-Algol styled language features (such as lazy data struc-
conditions in antecedents for each assertion until entirely          tures). He proves the following ruleset is complete (according
derived to axioms. Here, C is broken down until the remaining        to Cook) and correct due to a constructed abstract machine
program statement is empty or contains only basic statements.        based on operational semantics:
It is worth noting that the programming language is kept open
                                                                                      P [y/x]{begin D∗ ; A∗ end} Q[y/x]
by Hoare; often, it is imperative, however. Here intermediate            VARDECL
calculation steps (the memory states a program is at a partic-                          P {begin new x; D∗ ; A∗ end}Q
ular line of code) are transformed stepwise per statement. So,
                                                                                           D, P {begin D∗ ; A∗ end}Q
there is no reason why a descriptive programming language                    PROCDECL
may be used instead. Apart from very dedicated functions (e.g.                             P {begin D; D∗ ; A∗ end}Q
system calls), there are also theoretic boundaries imposed to
                                                                                         P {A}Q, Q{begin A∗ end}R
verification rules. One such problem is the guessing of the                   COMP1
right loop invariant. Let us consider a rule for loops:                                     P {begin A; A∗ end}R
                      {p ∧ e}S{p}                                                        COMP2
              {p}while e do S od{p ∧ ¬e}                                                          P {begin end}P

   Here, e denotes a condition, S is a program statement,                                ASN
and p denotes the precondition. From the consequent follow,                                     P [e/x]{x := e} P
the initial condition e must be false when leaving the loop.
However, all conditions unifying in p before the loop must                             P ∧ R{A1 }Q, P ∧ ¬R{A2 }Q
                                                                              COND
be valid and after the loop is executed. In order to prove the                          P {if R then A1 else A2 } Q
correctness of that loop, p with the correct loop body and
initial condition e shall be shown because the loop’s body is                                   P ∧ Q {A} P
                                                                                 WHILE
accessed only as long as e holds. After S e may be true or                                P {while Q do A} P ∧ ¬Q
false.
   In order to fully specify a loop, all variables occurring in                             p(x : v) proc K, P {K}Q
its body would be required. Once a loop is executed, the                           CALL
                                                                                               P {call p(x : v)}Q
calculation state alters, and naturally, a subset of all variables
need to be adapted to describe the current state. Formulae                               P {call p(u : e)}Q     σ = z ′ /z
describing calculation states after an arbitrary number of                     VSUB
                                                                                             P σ {call p(u : e)} Qσ
loop iterations manifest the invariant. Loop invariants due to
theoretical boundaries cannot always be fully specified whilst                                 P > R, R{A}S, S > Q
analysing, e.g. in multi-threaded environments.                                   CONSEQ
                                                                                                      P {A}Q
   A minimisation fashion can be observed in many program-
ming languages chosen for verification:                                                       P {call p(x : v ′ )}Q
     x := t                      .. assignment                            PSUB
                                                                                  P u, e/x′ , v ′ {call p(u : e)} Q u, e/x′ , v ′
     S1 ; S2                     .. statement sequence
     if e then S1 fi             .. conditional jump                    Cook intervenes the most practical limitations are: (1)
     while e do Sod              .. loop                             non-termination cannot be taken out inside a concrete Hoare
   Strictly speaking, conditional jumps can be replaced by           calculus in general, (2) expressibility of the assertion language
loops too. From a theoretical point of view, programs com-           (for specification and verification) is one of the fundamental
posed as such are minimal. However, expressibility does not          problems still open. It can also be deduced that proofs require
suffice [41].                                                        simplification since a simple proof is a suitable proof — this
   Apt [40] researches Hoare calculi over the last decades           is essential to proof program properties. Imagine a program
and indirectly confirms the trend towards minimal programs           was not obeying a given specification, then a simple and
as just suggested. Apt shows in [40] and [42] why some               generic mechanism is crucial in finding out the reasons for
features have some ”undesired” impact towards expressibility         that mismatch. Of course, parameter substitution suffers
and completeness. It occurs, e.g. due to arbitrary unbound           disadvantages, such as a clumsy selection at a loop, but
recursion, which can alter the calculation state entirely. It is     this is not the central question for the selected ruleset. Also
also due to recursively-defined data structures that are partially   important is whether, for a given ruleset and input program,
calculated when accessing fields and due to parameters being         all rule applications taken out in different orderings will
allowed as parameters in procedure calls. Those negative             lead to the same result or may not get stuck. This question
impacts have not been resolved yet.                                  is about ”proof confluency” and remains essential and still
   Cook [43], therefore, pleas for a limited subset of Hoare’s       unsolved up to date.
and Apt’s calculi [40] and suggests excluding unbound recur-
sion, co-routines, procedures-as-parameters, as well as other          Clarke [41] considers the problems mentioned by Hoare and
Apt the single most important ones still valid today. He lists       incompleteness and incorrectness at the same time.
problems not resolved yet or not resolvable in general in clas-         Meyer [45] notices that variables allocated at arbitrary loca-
sical Hoare calculi. For instance, continuations and variable        tions in program code dramatically overcomplicate the speci-
modes (e.g. static, automatic, dynamic and global) are still         fication and verification of heaps. Their elimination may not
not sufficiently resolved yet. On the one side, these problems       be considered a solution, though, because any restriction may
appear to be quite old now when judging their first appearances      significantly reduce expressibility. Moreover, Meyer states that
in journals. However, after studying more recent work, one           his assignment a := b is always correct in introducing his
finds they have not been resolved fundamentally yet. For             Hoare calculus. However, when looking carefully, one may
example, static variables can hardly be described in a Hoare         notice its correctness damages when b contains a procedure
calculus because that would require an efficient notational          call that alters the calculation state. Hence, it is better not to
apparatus to push and pop to the stack, which is not apriori part    consider Apt’s, Clarke’s, and Cook’s approaches in isolation
of the Hoare calculus. Clarke’s completeness definition is not       and for a rule solely, but to consider always
                                                                                                                 S the whole ruleset
that much different than Cook’s. Both authors understand that        as mentioned in [41]. So, the set union        does not hold in
some formula is complete if and only if each valid formula           general regarding correctness.
is provable. In addition to Apt [40], Clarke specifies ”bad”            All authors mentioned in this section agree that variables in
properties a Hoare calculus may have damaging completeness.          dynamic memory are a systematical damaging criterion upon
Clarke considers self-application in recursive definitions as a      all calculi considered yet. It implies that Miller [5], from
possible reason for damage to correctness and completeness.          his practical investigations and Clarke and all other authors
Let us recapitulate that any formal system is incomplete, ac-        mentioned, independently confirm that dynamic variables are
cording to Gödel, since there is always a formalised statement      tough to deal with naturally. Clarke and all other previously
that cannot be proven in terms of that same formal system            mentioned authors still insist on further research to be taken
itself. Naturally, this affects Hoare calculi too, particularly      out on dynamic variables. All warn though this is to be
those related to dynamic memory provers. Corner cases are            problematic in Hoare calculi.
essential from a theoretical standpoint, although, from a prac-
tical standpoint, those may be incredibly useless since, in                        IV. T RANSFORMING INTO S TACK
most cases, verification still may be done. It does not affect          The method ”transforming into stack” is a prominent tech-
the fundamental decidability of terms on verifications. They         nique [45], [9], [46], [6], [7]. The motivation behind this is
are bound to addition and subtraction (so-called Presburger          that pointers are too often too hard to analyse, and garbage
arithmetics [44]) but do not allow multiplication or any other       collection requires resources that otherwise would not be
operation. However, this theoretical decidability is insufficient    needed (cf. sec.II). However, Appel [7] demonstrates that
because of the exponential complexity imposed for the worst          the latter concern may vanish in cases the algorithm based
case. As a result, practical implementation and theoretical          upon heap is rewritten. Scenarios are shown where garbage
boundaries may diverge quite considerably. Theoretical bounds        collection is faster than automated stack management. There is
are almost neglectable for practical implementations on a day-       no doubt that algorithm analysis over pointers may be arduous.
by-day basis.                                                        However, often algorithms may be rewritten, not necessarily
   Clarke researched a combination of program features that          simpler but faster than analogous stack implementations. So
allow or disallow completeness. For instance, for a given            the question may arise: why is then performance important?
imperative programming language:                                     In case when passed objects are not touched, copying memory
                                                                     regions consumes a quite considerable overall runtime due to
  (i) procedures as parameters,
                                                                     the von-Neumann architecture. However, even when copies
 (ii) arbitrary ((µ-recursive) procedures,
                                                                     are touched (which often occurs in practice too), ”Application
(iii) static variables,
                                                                     Binary Interfaces” (ABI) still forbid individual copies to be
(iv) global variables,
                                                                     propagated any further among callee-caller chains. Currently,
 (v) nested (so-called ”inner”) procedures,
                                                                     simple cases are already recognised by GCC 6.3.0 (cf. [31]).
  Completeness may be violated in the most general case due          So, effective use is not possible apriori. GCC divides objects
to feature iii). The resulting Hoare calculus is complete if         and structures into smaller chunks, namely single processor
problematic features are excluded (here i-ii, iv-v). To prove this   words. It happens mainly without considering class encap-
and similar cases based on the features i-v, Clarke introduces       sulation as long as data dependencies are concerned, which
an operational semantics over relations very close to Cook’s         is not a problem to code generation. However, if an object
semantics. Beyond Clarke’s article, the observations made may        ought to be deleted, unfortunately, the whole object remains
be beneficial, for example, on logical predicates and abstract       accommodated for conservative concerns and is not freed even
predicates, as shown later in this paper. Clarke shows that          if it could. The consequence is a bloated execution model.
excluding of self-applicable procedure parameters may indeed         Mainly, linked objects raise the pressure to free parts more
reduce its expressibility, but it also leads to calculi without      often due to their relative bigger size and remain at the end for
sudden incorrect jump statements. Furthermore, co-routines in        security reasons — which both reduce the chance for improved
combination with arbitrary recursion, however, may lead to           and minimalistic code significantly. If an update is applied
to an object web, then an object may not be freed. Instead,            Nevertheless, regarding the functional approach, one limi-
it shall be passed to the corresponding level. This problem         tation must be kept in sight: no lists may be returned, and
could be resolved if objects were pushed or pulled to/from          the visible object scope must be modelled separately — since
the stack simultaneously. However, this does not happen, and        symbols are not bound to local blocks as in classic imperative
in the end, redundant copies of objects take place everywhere       programming languages. Another weakness is that regions
for a conservative approach.                                        accommodated in the stack are often too large and are coupled
   Transforming a heap means any data structure from the            with other objects (where loosely coupled by design seldomly
heap shall be accommodated to a stack window instead.               occurs, if ever). Those categories dramatically slow down
Object dependencies shall be codified in the stack by               performance and the whole verification process.
additional constraints. For instance, all consecutive elements
shall be placed with arising indices for a simply-linked                                 V. S HAPE A NALYSIS
list. The same may be done with doubly-linked lists. If an             The main goal of Shape Analysis [47], [48], [38], [30] is
element is inserted or removed from a specific position in          the detection of heap invariants (shapes), which may further
a list, then the stack window accomodating that list may            be used for alias analysis. The dependency graph of shapes is
dramatically differ afterwards to guarantee arising indices         described fully by using transfer functions, such as: ”shape is
properly. In analogy to that, trees and graphs require ”proper      empty”, assigning a field member or pointer, and allocating a
stackinisation”.                                                    new heap. Sagiv [47] suggests a categorisation of pointer rela-
                                                                    tions, namely ”aliasing”, ”non-aliasing”, and ”possibly alias-
   Meyer suggests storing all objects in the stack. Appel and       ing”. Labelling becomes a concern in compressed dependency
others show this is, in fact, a loss of performance. Rewriting      subgraphs, as discussed in [47] and [48]. The approaches
a heap algorithm into a stack-based algorithm shows poorer          discussed in there have numerous limitations, e.g. pointers
runtime characteristics for widely popular data structures. For     may only be indexed in non-variable expressions. Furthermore,
example, stack allocation using calloc instead of the heap-         pointers to class objects are forbidden. Arrays with a dynamic
specific malloc may reserve several kilobytes on the stack.         length are also forbidden and sharing structured (as ”union”
It must be informed that this may significantly bloat stack         does in C).
windows; as a result, pages managed by an OS need to be                Pavlu [38] notes that both approaches, [47] and [48], may
spread more often, which negatively influences performance          conclude in unsound reasoning for a given program due to
(cf. ”variadic functions” [15]).                                    non-deterministic choices to be made on approximation. If
   Whether a successful transformation into a stack of objects      for ”if-then”-statements in one case ”possibly aliasing” is
is not possible to determine apriori. Moreover, the opposite        found, but in an alternative case ”aliasing”, then according to
may even be the case. Dynamic data structures are preferred         their method, the calculation would terminate with founding
over stack whenever the final runtime sizes are unknown.            ”aliasing”, although the right should instead be ”possibly
Apart from that, unrestricted heap manipulations cannot al-         aliasing”. Apart from that, [38] contains a detailed comparison
ways be transferred as is to the stack since this may require       of [47] and [48]. Pavlu judges the method in [48] as most
additional constraints modelled differently. Slower runtime         accurate. In addition to it, he suggests a path optimisation
performance, more extensive remaining resources, or rigid           for shape graphs for the same beginnings and aliases. The
implementations are examples. That is why Meyer’s propo-            upper complexity bound for his proposition is quadratic in
sition shall be considered with high reservations only. For         dependency of the incoming path length and reduces the
completeness, it must be noted that naturally, both programs        overall calculation by approximately 90%. Pavlu suggests a
operating on stack or heap can be implemented in more or            complex alias analysis beyond procedure definitions by turning
less efficient ways, and a direct comparison may not always be      procedure calls and globals as much as possible into locals.
valid. According to Meyer, pointer and alias analysis are com-      This approach is not new, and it can be found that it has
plex because the underlying logic does not distinguish between      already successfully been applied to ”GCC”. Pavlu and the
structures and non-structured data in logical expressions. This     author of this paper suspect context-independent approaches
equality implies considerable efforts shall be spent in the area    may lack a future perspective due to imprecision (cf. also
of discussion.                                                      [49]). Furthermore, Pavlu suggests an additional optimisation
   A particular case of ”Transforming into Stack” may be            of unifying vertices, generating subgraphs based on vertices
considered the so-called ”Region Calculus” [8]. The main idea       that do not contain aliases.
is to assign class objects onto heap as it were locals in a stack      Parduhn [50] proposes an environment for visualising heap
window, such that those may be managed automatically. Since         shapes for faster invariant analysis and close-invariant relation-
the class object’s type is known statically, the corresponding      ships (those shape relations that seldomly correlate). In order
stack windows size may be precalculated successfully. Even          to navigate through that visualised shapes, two basic opera-
subclass objects may be approximated based on a superclass.         tions are used: ”shape abstraction” and ”shape concretisation”,
It is worth mentioning that functional programming languages,       which allow for zooming out and in subgraphs. However,
such as ”ML”, internally perform precisely this type of coer-       the visualisation of the transfer function that allows zooming
cion.                                                               in/out more than one shape currently remains unsatisfactory,
and there is no indication this could generally improve in the       will be moved. x.next.next is the second argument, a pointer,
next future due to its nature.                                       which is not modified.
   Calcagno’s approach [51] is based on Separation Logic over           This approach is of interest from a theoretical and a practical
shapes (cf. sec.VII). The method approximates both sides of a        side. However, the calculus is hardly applicable to little more
rule to perform abductive reasoning. This approach compares          complicated algorithms, such as trees. Hence more research is
potentially matching rules, namely their beginnings, and in the      required.
case of multiple matching candidates, the most extended rule            A pointer rotation (including translation) is supposed to be
is chosen first.                                                     ”safe” by nature. Nevertheless, that is far from true. Let us
                                                                     consider rotate(y, y.next). This example deletes the first ele-
                   VI. P OINTER ROTATION                             ment in many configurations. However, this may look different
   The old but not outdated theory of ”Pointer Rotations” [52]       for rotate(x, y, x.next), when (1) the heap’s content does not
suggests pointer rotation and translations. For example, given       change, (2) all elements remain valid before and after rotation,
disjunctive pointers a barrel pointer rotations may be:              and (3) the amount of variables does not change. Pointer
                                                                   rotation does not need garbage collection. It also benefits from
                 x1 x2 x3 · · · xn−1 xn                              effective and safe list operations. Although pointer rotation
                 x2 x3 x4         · · · xn   x1                      does not require further specification, a tiny modification in
  With this, x1 points to the content of x2 .                        the calling parameters in rotations may already lead to hard
  A left translation (known as a slide) is congruent to a left       to predict behaviour (often undesired behaviour, though). It
barrel rotation. Next, x:=y is equivalent to slide(x, y). The        is observed very frequently when corner cases occur or on
objective of any rotation or translation is to replace error-prone   aliases, and the consequence is that behaviour changes totally
individual code with well-known stable operations. In this case      and may even delete lists where it has never been thought
”safe”, operations over pointers act as some specification. For      possible at all. Suzuki [52] suggests ”base rotations” to restrict
example:                                                             to some safe subsets, but, unfortunately, without explicitly
                                                                     describing what ”base” really denotes – even if it is intuitively
y=NULL;                                                              clear what is meant, but very hard to find a standard definition.
while (x!=NULL) {                                                    However, in practice, it is hard. The motivation behind this is
  temp = x.next;                                                     to compose ”safe” rotations individually.
  x.next = y;
  y = x;                                                                               VII. S EPARATION L OGIC
  x = temp;
}                                                                      Separation Logic (SL) makes use of predicates to describe
                                                                     dynamic memory [53], [54], [55], [56]. The logic is defined
  is equivalent to the notation
                                                                     over the spatial operation ⋆, a logical conjunction (operators
y = NULL;                                                            ∧, ∨, ¬).
while (x!=NULL) rotL(x,x.next,y);
                                                                      Φ    ::=    true | f alse | x | REL(fj (~x)) | P red(fj (~x))
   Although it does not follow directly from Suzuki’s paper, it                    | ¬Φ | Φ ⋆ Φ | ∀x.Φ[x] | ∃x.Φ[x]
can be noticed that rot(x,x,y) is identical to the mapping
                                                                        REL(fj (~x)) includes the atomic heap a 7→ b, where
id. In analogy to the previous rotation to the right, a left
                                                                     b denotes a location, and b denotes a valid value (e.g. a
rotation rotate() may be defined as:
                                                                     class object). Location means either an identifier or an access
y = NULL;                                                            expression over valid object fields. It is later introduced by
while (x!=NULL){                                                     Parkinson [57]. However, the initial definition of SL does not
  temp = x;                                                          allow defining objects. P red() denotes a call to a previously
  x = y;                                                             defined predicate that may require parameters.
  y = x.next;                                                           The spatial operator by Berdine and Reynolds implies a
  x.next = temp;                                                     separability of heap components. Strictly speaking, the ⋆-
}                                                                    operator can not only divide a heap but can also be used
                                                                     to conjunct two heaps. The former is undoubtedly intended,
  Equality can now be introduced upon this rotation
                                                                     whereas the latter is not. The latter significantly complicates
          rot−1                                                      analyses of a heap and its components.
             L (x, x.next, y) ≡ rotL (x.next, x, y).
                                                                        Properties of the spatial operator after Reynolds [53] and
So, algebraic properties may be defined and proven dependent         Berdine [54]:
on given translations and rotations. So, one rotation may have           (1) compactness:
different stereotypes depending on incoming parameters. For                    p 6⇒ p ⋆ p, p ⋆ q 6⇒ p, if ∃q, q 6≡ emp
instance, rotate(x.next, x.next.next.y). Here y denotes a                (2) commutativity:
target list, where x.next denotes the first argument, which                    p1 ⋆ p2 ⇔ p2 ⋆ p1
    (3)   associativity:                                           memory recursively over a closed set of built-in rules only.
          (p1 ⋆ p2 ) ⋆ p3 ⇔ p1 ⋆ (p2 ⋆ p3 )                        Berdine et al. also ask whether heap verification is not a typing
    (4)   neutral element:                                         problem. From that paper follows, e.g. the undecidability of
          p ⋆ emp ⇔ emp ⋆ p ⇔ p                                    unbound pointers leads to flaky garbage collection events even
    (5)   distributivity:                                          for elementary expressions for memory offsets and to a very
          (p1 ∨ p2 ) ⋆ q ⇔ (p1 ⋆ q) ∨ (p2 ⋆ q)                     coarse rule selection due to greedy heuristics.
          (p1 ∧ p2 ) ⋆ q ⇔ (p1 ⋆ q) ∧ (p2 ⋆ q)                        Bornat [16] proposes a model very close to SL called
    (6)   quantification:                                          ”remote separation”. The model takes objects into arrays (cf.
          (∃x.p) ⋆ q ⇔ ∃x.(p ⋆ q), if x 6∈ F V (q)                 sec.IV). So, any object field turns into an individual pointer
          (∀x.p) ⋆ q ⇔ ∀x.(p ⋆ q), if x 6∈ F V (q)                 with a different convention on labelling and uniqueness. For
                                                                   a lifted definition, he postulates that first-order predicates
   Predicate emp holds for a given empty heap. Set F V             are sufficient. The main achievement of Hurlin [59] is the
denotes all variables not bound for a given assertion. A binary    new access design pattern towards heaps for multi-threaded
tree is considered as a parameterised predicate which can          programs. If a given heap is atomic, then it is undividable,
inductively be defined as follows:                                 and therefore it must be a trivial and valid case. If a heap is
                                                                   not provable, then compulsory simplifications are not applied.
 btree(l) ::= nil | ∃x.∃y : l 7→ x, y ⋆ btree(x) ⋆ btree(y)           Parkinson [60] represents an attempt at an object-oriented
Here, a binary tree is described by predicate btree and some       extension of the classic SL [53] based on Java as the input pro-
untyped symbol l or is just empty, or l points to a simply-        gramming language. Modularity and inheritance are modelled
linked list whose content is x followed by non-overlapping         within ”inverting calling control” and ”Abstract Predicate
y.                                                                 Family”. Bornat’s access model [16] can be applied because
   SL is Hoare-based (cf. sec.III) and substructural (cf. [58]).   the continuity property holds for frames over objects. Bornat
The latter implies constants are replaced, e.g. by boolean         notices that dependencies between predicates define an order
values. Higher constants, e.g. true, are partial. They consume     for predicate calls. The paper implies that the predicates within
some heap and return a boolean meaning depending on the            allow the full definition of heap and stack, but it does not
passed heap. SL also uses symbols for structural meanings          allow, for instance, to define arbitrary first-order predicates.
as constants. In SL, according to the non-repetition principle     Assertion predicates, which syntactically and semantically
structural rules consist of thinning (THIN) [58], substitution,    strongly differ from predicates for the input language, do not
and heap cells constants. In specified rules, ”,” is replaced by   restrict themselves w.r.t. types. However, the use of symbols
”⋆”, which separates two non-intersecting and unique heaps,        imposes several limitations, due to the non-symbolic imple-
except when told otherwise. Heaps are defined inductively.         mentations of symbolic variables. Predicates use them as locals
Rules (PERMUTE) and (CUT) are subtractive. In SL, thinning         as known from imperative programming languages. Parkinson
does not hold. Hence heap may not repeat. This property is         proposes method calls from parent classes, static fields, object
handy when a heap may occur at most once.                          introspection, inner classes and quantified predicates for future
                                                                   research.
                              X, Y ⊢ Z
                     THIN
                            X, A, Y ⊢ Z                                              VIII. F UTURE R ESEARCH
                                                                     Apart from already mentioned tendencies, research gaps,
                           X, A, A, Y ⊢ Z
                  CONTR                                            and recent debates, the author of this paper would like to stress
                            X, A, Y ⊢ Z                            the following future research propositions:
                            X, A, B, Y ⊢ Z                           1) Both models, as discussed earlier, do not recognise
                PERMUTE                                                  varying objects in structures. So, if the contents of both
                            X, B, A, Y ⊢ Z
                                                                         are identical, then by definition, those two cells must
                     X ⊢ A U, A, Y ⊢ Z                                   be identical. However, in practice, this hardly can be
                CUT
                         U, X, Y ⊢ Z                                     mandatory since a later copy must not touch another
                                                                         copy.
  The frame rule defines as:
                                                                     2) Predicates that are excluded by built-in tactics are man-
                        {P }C{Q}
                                                                         ually folded and unfolded. Hutton suggests a generative
                    {P ⋆ F }C{Q ⋆ F }                                    method called ”Fold and Unfold” on functionals in the
   It means that when a subprocedure call C does not change              context of functional programming languages. Here, fur-
a heap component, namely it includes frame F , then the                  ther research is suggested to automate proofs, especially
antecedent is sufficient to prove in order to show the Hoare             since proof generation seems to be a complex problem.
triple holds without F .                                                 Those problems lead to predicates being manually con-
   Berdine [54] suggest SL-based unbound arithmetic over                 figured and triggered whilst proving, e.g. by proof hints.
pointers with compositions including dynamically growing             3) The use of ”hot” code — code that can be altered during
arrays and recursive procedures. It attempts to define dynamic           execution is unlikely to be considered. Some previously
    mentioned authors consider ”unique possibilities on ex-            observed in recent verifier implementations, although
    pressibility”. However, this euphoric opinion should be            currently only loose features yet.
    rethought by all means since the practical possibilities       12) It is expected that algebraic theories will more and more
    gained are too limited. On one side, arbitrary code is             advance logical rules due to the fastly growing com-
    inserted into a running system whose specification only            plexity of programming language features. So, a higher
    may be available. On the other side, this introduces other         acceptance barrier is expected to introduce new features
    security risks and especially down-grades performance              rather than individual built-in functions. Notably, the
    for any application considerably. Expressibility is not            analysis of logical expressions has to reduce exponential
    extended. It is just the moment that code is loaded.               complexity ideally to linear.
    Loaded code is presumably a discipline on code linkers,        13) In analogy to the previous discussion on dynamic code
    which implement security mechanisms as included in the             loading, higher-order Hoare calculi may not play the role
    ”GCC” and ”binutils” framework, rather than verifying              estimated by its proponents.
    code. Virtual machines and interpreters implement sim-         14) Partial specification as specification simplification tech-
    ilar security mechanisms called ”Binding programming               nique is expected to raise meaning due to its pragmatism.
    interfaces”.
 4) The level of intuition and proof explanation are essential                                  R EFERENCES
    criteria for verifier acceptance. This number plays a
    significant role and generalised counter-example gener-        [1] Robert Love. Linux Kernel Development. Addison-Wesley Professional,
                                                                       3rd edition, 2010.
    ations, which can be considered absent at the moment.          [2] Charles A. R. Hoare. An axiomatic basis for computer programming.
 5) Due to upcoming models and approaches, the pressure                Communications of the ACM, 12(10):576–580, 10 1969.
    for integration raises. There is a need for interoperating     [3] William E. Weihl. Interprocedural data flow analysis in the presence of
                                                                       pointers, procedure variables and label variables. In Paul W. Abrahams,
    tools on the different stages of verification. The main            Richard J. Lipton, and Stephen R. Bourne, editors, Proc. of the 7th ACM
    reason for this is its lack of adaption and extension of           SIGPLAN-SIGACT symp. on Principles of Programming Languages,
    the intermediate representation.                                   pages 83–94. ACM Press, 1980.
 6) Too often, solely scenarios are considered for heap ver-       [4] Barton P. Miller, David Koski, Cjin Pheow Lee, Vivekananda Maganty,
                                                                       Ravi Murthy, Ajitkumar Natarajan, and Jeff Steidl. Nichts dazugelernt
    ifiers. Although heap verifiers by design are constructed          — empirische studie zur zuverlässigkeit von unix-utilities. Magazin für
    to suffice specific scenarios, the lack of integration and         professionelle Informationstechnik, iX, 9:108–121, 1995.
    overall revision diverge the gained benefit severely and       [5] Barton P. Miller, Lars Fredriksen, and Bryan So. An empirical study of
                                                                       the reliability of unix utilities. In In Proc. of the Workshop of Parallel
    only allow estimates of real problems solved. A standard           and Distributed Debugging, pages 1–22. Digital Equipment Corporation,
    code would be required to make accurate estimates, but             1990.
    a joint heap model base would also be needed.                  [6] Richard Jones, Antony Hosking, and Eliot Moss. The Garbage Collec-
                                                                       tion Handbook: The Art of Automatic Memory Management. Chapman
 7) Once integration starts, more and more unification at-             & Hall/CRC, 1st edition, 2011.
    tempts are expected.                                           [7] Andrew W. Appel. Garbage collection can be faster than stack allocation.
 8) Further parallelisation of Hoare calculi for heap verifica-        Information Processing Letters, Elsevier North-Holland, 25(4):275–279,
                                                                       1987.
    tion is despite similar attempts in garbage collection are     [8] Mads Tofte and Jean-Pierre Talpin. Region-based memory management.
    not expected since the research focus currently is more            Information and Computation, 132(2):109–176, 1997.
    on fundamentals than on a clear direction of parallelisa-      [9] Bertrand Meyer. Proving pointer program properties - part 2: The overall
                                                                       object structure. ETH Zürich, Journal of Object Technology, 2003.
    tion. Parallelisation, however, is expected in bordering
                                                                  [10] Richard G. Larson. Minimizing garbage collection as a function of
    disciplines, especially in model checking techniques,              region size. SIAM Journal on Computing, 6(4):663–668, 1977.
    since their parallel formula constraints may efficiently      [11] Prokash Sinha. A memory-efficient doubly linked list, online, version
    be checked.                                                        from 18.11.2014, 11 2013.
                                                                       http://www.linuxjournal.com/article/6828.
 9) Expressibility and completeness issues remain open.           [12] Nick Parlante. Linked list basics, document no.103 from the stanford
    Variable modes remain an active research area at least             computer science education library, 2001.
    for the next 12 years for static, global and dynamic               http://cslibrary.stanford.edu/103 .
                                                                  [13] René Haberland.               Tutorials and examples, 11 2016.
    memory.                                                            https://bitbucket.org/reneH123/.
10) Dodds [61] proposes a descriptive transformation lan-         [14] Richard Jones and Sun Microsystems Inc. Memory management in the
    guage for dynamic memory. His approach strongly                    java hotspot virtual machine. Technical Report only from April 2006
                                                                       http://www.oracle.com/technetwork/articles/java/index-jsp-140228.html.
    differs and does not seem applicable to imperative            [15] Intl. Organization of Standardization. Iso c++ standard, n4296 from
    programming languages at first glance. Here, broader               2014-11-19.
    research is needed for C-dialects on applicability since      [16] Richard Bornat. Proving pointer programs in hoare logic. In Roland
    synergy effects could be taken from Dodds transforma-              Backhouse and José Nuno Oliveira, editors, Proc. of the 5th Intl. Conf.
                                                                       on Mathematics of Program Construction, volume 1 of Lecture Notes
    tion language.                                                     in Computer Science, Springer, pages 102–126, 2000.
11) It is expected that the descriptive paradigm trends from      [17] Martin Abadi and Luca Cardelli. A Theory of Objects. Springer,
    the 2010s remain. However, the focus may change from               Secaucus, New Jersey, USA, 1996.
                                                                  [18] Carl A. Gunter and John C. (eds.) Mitchell. Theoretical aspects of
    a functional to a logical paradigm. Due to its advantages          object-oriented programming – types, semantics, and language design.
    in favour of functionals, more and more reuse can be               MIT Press, 1994.
[19] Martin Abadi and K. Rustan M. Leino. A logic of object-oriented              [41] Edmund Melson Jr. Clarke. Programming language constructs for which
     programs. In Proc. of the 7th Intl. Joint Conf. CAAP/FASE on Theory               it is impossible to obtain good hoare axiom systems. Journal of the
     and Practice of Software Development, pages 682–696. Springer, 1997.              ACM, New York, USA, 26(1):129–147, 2 1979.
[20] Hartmut Ehrig and Barry K. Rosen. The mathematics of record handling.        [42] Krzysztof R. Apt and Ernst-Rüdiger Olderog. Verification of sequential
     SIAM Journal on Computing, 9(3):441–469, 1980.                                    and concurrent programs. SIAM Review, 35(2):330–331, 1993.
[21] Martin Abadi. Baby modula-3 and a theory of object. Technical Report
     SRC-RR-95, Systems Research Center, Digital Equipment Corporation,           [43] Stephen Cook. Soundness and completeness of an axiom system for
     1993.                                                                             program verification. SIAM Journal on Computing, 7(1):70–90, 1978.
[22] K. Rustan M. Leino. Recursive object types in a logic of object-oriented     [44] Ryan Stansifer. Presburger’s article on integer airthmetic: Remarks and
     programs. Nordic Journal of Computing, 5(4):330–360, 4 1998.                      translation. Technical Report TR84-639, Computer Science Department,
[23] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. Regional                  Cornell University, 9 1984.
     logic for local reasoning about global invariants. In J. Vitek, editor,      [46] Neil D. Jones and Steven S. Muchnick. Even simple programs are hard
     European conf. on Object-Oriented Programming, volume 5142 of                     to analyze. In Proc. of 2nd ACM SIGACT-SIGPLAN symp. on Principles
     Lecture Notes in Computer Science, pages 387–411. Springer, Berlin                of Programming Languages, pages 106–118, 1975.
     Heidelberg, 2008.                                                            [47] Mooly Sagiv, Thomas Reps, and Reinhard Wilhelm. Parametric shape
[24] Wikipedia. Region-based memory management.                                        analysis via 3-valued logic. ACM Transactions on Programming Lan-
     https://en.wikipedia.org/wiki/Region-based memory management.                     guages and Systems, 24(3):217–298, 2002.
[25] Michael Barnett, Robert DeLine, Manuel Fähndrich, K. Rustan M.
     Leino, and Wolfram Schulte. Verification of object-oriented programs         [48] Flemming Nielson, Hanne R. Nielson, and Chris Hankin. Principles of
     with invariants. Journal of Object Technology, 3(6):27–56, 2004.                  Program Analysis. Springer Berlin, Heidelberg, 1999.
[26] Peter Müller. Modular Specification and Verification of Object-Oriented     [49] Michael Hind. Pointer analysis: Haven’t we solved this problem
     Programs. PhD thesis, Fern-Universität Hagen, Germany, 2002.                     yet? In USA IBM Watson Research Center, editor, Proc. of the ACM
[27] Desmond F. D’Souza and Alan Cameron Wills. Objects, Components,                   SIGPLAN-SIGSOFT workshop on Program Analysis for Software Tools
     and Frameworks with UML: The Catalysis Approach. Object Technol-                  and Engineering, pages 54–61. ACM, 6 2001.
     ogy Series. Addison-Wesley, 1998.                                            [50] Sascha A. Parduhn, Raimund Seidel, and Reinhard Wilhelm. Algorithm
[28] Object Management Group (OMG). Object constraint language version                 visualization using concrete and abstract shape graphs. In Proc. of the
     2.2, 2 2010.                                                                      ACM symp. on Software Visualization, pages 33–36, 2008.
     http://www.omg.org/spec/OCL/2.2.
                                                                                  [51] Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok
[29] Steven Muchnick. Advanced Compiler Design and Implementation.
                                                                                       Yang. Compositional shape analysis by means of bi-abduction. Proc.
     Morgan Kaufmann Publishers Inc., 2007.
                                                                                       of the 36th annual ACM SIGPLAN-SIGACT symp. on Principles of
[30] Ganesan Ramalingam. The undecidability of aliasing. ACM Transactions
                                                                                       Programming Languages, 36:289–300, 2009.
     on Programming Languages and Systems, 16(5):1467–1471, 9 1994.
[31] The gnu compiler collection, http://gcc.gnu.org.                             [52] Norihisa Suzuki. Analysis of pointer rotation. Communications of the
[32] Susan Horwitz, Phil Pfeiffer, and Thomas Reps. Dependence analysis for            ACM, 25(5):330–335, 1982.
     pointer variables. In Proc. of the ACM SIGPLAN Conf. on Programming          [53] John C. Reynolds. Separation logic: A logic for shared mutable data
     Language Design and Implementation, pages 28–40, New York, USA,                   structures. In Proc. of the 17th Annual IEEE symp. on Logic in Computer
     7 1989. ACM.                                                                      Science, pages 55–74, Washington, DC, USA, 2002. IEEE Computer
[33] Uday Khedker, Amitabha Sanyal, and Bageshri Karkare. Data Flow                    Society.
     Analysis: Theory and Practice. CRC Press, Inc., Boca Raton, Florida,         [54] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic
     USA, 1st edition, 2009.                                                           execution with separation logic. In 3rd Asian symp. on Programming
[34] Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford            Languages and Systems, pages 52–68, Tsukuba, Japan, 11 2005.
     Stein. Introduction to Algorithms. MIT Press, 3rd edition, 7 2009.
[35] Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman, and             [55] John C. Reynolds. An Introduction to Separation Logic. 2009. Carnegie
     F. Kenneth Zadeck. Efficiently computing static single assignment form            Mellon University, Pittsburgh, Pennsylvania, USA, course book available
     and the control dependence graph. ACM Transactions on Programming                 online:
     Lanuages and Systems, 13(4):451–490, 10 1991.                                     http://www.cs.cmu.edu/afs/cs.cmu.edu/project/fox-19/member/jcr.
[36] Static single assignment book, latest from july 2014, available online at:   [56] Rodney M. Burstall. Some techniques for proving correctness of
     http://ssabook.gforge.inria.fr/latest/book.pdf. electronically.                   programs which alter data structures. In Bernard Meltzer and Donald
[37] Nomair A. Naeem and Ondrej Lhoták. Efficient alias set analysis using            Michie, editors, Machine Intelligence, volume 7, pages 23–50. Edin-
     ssa form. In Proc. of the intl. symp. on Memory Management, pages                 burgh University Press, Scotland, 1972.
     79–88, New York, USA, 2009. ACM.                                             [57] Matthew Parkinson and Gavin Bierman. Separation logic and abstrac-
[38] Viktor Pavlu. Shape-based alias analysis – extracting alias sets from             tion. SIGPLAN Notes, 40(1):247–258, 2005.
     shape graphs for comparison of shape analysis precision. Master’s thesis,
     Vienna University of Technology, Austria, 2010.                              [58] Greg Restall. Introduction to Substructural Logic. Routledge Publishing,
[39] Bjarne Steensgaard. Points-to analysis in almost linear time. In Proc. of         2000.
     the 23rd ACM SIGPLAN-SIGACT symp. on Principles of Programming               [59] Clément Hurlin. Specification and Verification of Multithreaded Object-
     Languages, pages 32–41, New York, USA, 1 1996. ACM.                               Oriented Programs with Separation Logic. PhD thesis, Université Nice
[40] Krzysztof R. Apt. Ten years of hoare’s logic: A survey - part I. ACM              – Sophia Antipolis, France, 9 2009.
     Transactions on Programming Languages and Systems, 3(4):431–483,             [60] Matthew J. Parkinson. Local Reasoning for Java. PhD thesis, Cambridge
     1981.                                                                             University, England, 2005.
[45] Bertrand Meyer. Proving pointer program properties - part 1: Context
     and overview, part 2: The overall object structure. ETH Zürich, Journal     [61] Mike Dodds. Graph Transformations and Pointer Structures. PhD thesis,
     of Object Technology, 2003.                                                       University of York, England, 2008.
