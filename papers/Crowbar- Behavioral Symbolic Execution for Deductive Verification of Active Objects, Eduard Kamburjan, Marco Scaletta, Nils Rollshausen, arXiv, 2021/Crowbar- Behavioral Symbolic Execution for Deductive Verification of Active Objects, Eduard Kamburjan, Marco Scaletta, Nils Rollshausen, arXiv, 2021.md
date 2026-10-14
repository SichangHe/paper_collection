                                               Crowbar: Behavioral Symbolic Execution for
                                                Deductive Verification of Active Objects

                                         Eduard Kamburjan[0000−0002−0996−2543]1 , Marco Scaletta[0000−0001−5298−3369]2 ,
                                                        and Nils Rollshausen[0000−0003−2445−8684]2
                                                                    1
                                                                   University of Oslo, Oslo, Norway
arXiv:2102.10127v2 [cs.LO] 11 Feb 2022




                                                                        eduard@ifi.uio.no
                                                      2
                                                        Technische Universität Darmstadt, Darmstadt, Germany
                                              scaletta@cs.tu-darmstadt.de, nils.rollshausen@stud.tu-darmstadt.de



                                                 Abstract. We present the Crowbar tool, a deductive verification system
                                                 for the ABS language. ABS models distributed systems with the Active Ob-
                                                 ject concurrency model. Crowbar implements behavioral symbolic execu-
                                                 tion: each method is symbolically executed, but specification and prior
                                                 static analyses influence the shape of the symbolic execution tree. User
                                                 interaction is realized through guided counterexamples, which present
                                                 failed proof branches in terms of the input program. Crowbar has a clear
                                                 interface to implement new specification languages and verification cal-
                                                 culi in the Behavioral Program Logic and has been applied for the biggest
                                                 verification case study of Active Objects.


                                         1     Introduction

                                         Symbolic Execution (SE) [26,31] is a core technique in program verification,
                                         which is recently receiving increasing attention for concurrent systems [29,6,7].
                                         For the Active Objects [8] concurrency model, experiences with multiple case
                                         studies [12,23,24] led to the design of the Behavioral Program Logic (BPL) [19],
                                         a dynamic logic that generalizes SE to Behavioral Symbolic Execution (BSE).
                                             In this paper, we introduce Crowbar, a system for the deductive verifica-
                                         tion of Active Objects [8], which targets the ABS language [17], and implements
                                         BPL. Contrary to other heavyweight3 symbolic execution approaches, behavioral
                                         symbolic execution uses the specification already when building the symbolic ex-
                                         ecution tree: the specification is reduced on-the-fly and Crowbar can fails early
                                         if the remaining specification cannot be adhered to. Not only the specification
                                         is used to influence the shape of the SE tree, but also static analyses.
                                             Additionally, Crowbar exploits the Active Object model to drastically sim-
                                         plify its handling of concurrency: Active Objects carefully distinguishes between
                                         local execution, where a single method essentially behaves as in a sequential sys-
                                         tem, and global concurrency. Crowbar performs its analysis on the local layer,
                                         but has a clear interface to external analyses if a global property is required.
                                         3
                                             I.e., static logic-based functional verification using loop invariants for unbounded
                                             behavior. For a discussion on lightweight vs. heavyweight SE we refer to [30, Ch. 3].
2        Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

    BSE improves automatization of deductive verification, as they reduce the
size of the final logical formulas. This allows us to scale heavyweight SE for dis-
tributed systems: Crowbar is used to perform the to-date biggest case study [25]
in deductive verification of Active Objects.
    We introduce guided counterexamples for user feedback. From a failed proof
branch, a program is generated that allows the user to examine the failed proof
in terms of the input language and retains the original structure of the method.
    Crowbar is implemented with flexibility in mind: one of its long term goals is
to explore the design space of behavioral symbolic execution and specification of
distributed systems. Two SE calculi are already implemented. KeY-ABS [10], the
predecessor system for ABS is superseded by Crowbar and discussed in Sec. 7.
    We introduce ABS and BPL in Sec. 2, and the structure of Crowbar in Sec. 3,
before describing front-end (Sec. 4), middle-end4 (Sec. 5), and back-end (Sec. 6)
in detail. Crowbar is available at https://github.com/Edkamb/crowbar-tool.


2     Preliminaries: ABS and BPL
Active Objects combine object-orientation with cooperative scheduling and actor-
based communication with futures. For a formal introduction we refer to [8,17].
Strong Encapsulation. Every object is strongly encapsulated at runtime, such
   that no other object can access its fields, not even objects of the same class.
Asynchronous Calls with Futures. Each method call to another object is
   asynchronous and generates a future. Futures can be passed around and are
   used to synchronize on the process generated by the call. Once the called pro-
   cess terminates, its future is resolved and the return value can be retrieved.
   We say that the process computes its future.
Cooperative Scheduling. At every point in time, at most one process is active
   per object and a running process cannot be interrupted unless it explicitly
   releases the object. This is done either by termination with a return statement
   or with an await g statement that waits until guard g holds. A guard polls
   whether a future is resolved or whether a boolean condition holds.
Concurrent systems are challenging for SE, but Active Objects allow to perform
local SE on single methods through their strong encapsulation and decoupling of
caller and callee processes. Special care, however, has to be taken to keep track
of futures and correct handling of state when using await. We introduce the ABS
language using an example to demonstrate these features.

Example 1. Consider Lst. 1. The class Monitor has two fields: s which is a server
that is monitored and specified as being non-null (more on specification in Sec. 4)
and beats, a counter for successful requests to s. The method heartbeat sends a
request to itself (l. 6) by an asynchronous method call (by using !). Afterwards,
the return value of the call is retrieved (l. 7, using get). This blocks the process
until the httpRequest process has terminated. No other process can run on this
4
    We borrow this term from compiler construction.
                  Crowbar: Behavioral Symbolic Execution for Active Objects      3


   1 [Spec:Requires(this.s != null)][Spec:ObjInv(this.s != null)]
   2 class Monitor(Server s) {
   3     Int beats = 0;
   4     [Spec:Ensures(this.beats >= old(this.beats) && result == this.beats)]
   5     Int heartbeat() {
   6      Fut<Int> req = s!httpRequest();
   7      Int status = req.get;
   8      if(status == 200) { this.beats = this.beats + 1;}
   9      else { this.handleError(); }
  10      return this.beats;
  11     }
  12     Unit reset(Int i){ await this.beats == i; this.beats = 0; }
  13     Unit handleError() { this.beats = 0; /∗ ... ∗/ }
  14 }



                Listing 1. An example ABS program with specification.


object until this happens. If the request was successful, beats is increased by
1. Method reset waits without blocking until the number of success reaches a
passed threshold and resets beats. Synchronous calls are possible (l. 9) on this.

Verification using Symbolic Execution. Symbolic execution describes the execu-
tion of a program (or statement) with symbolic values. A symbolic value is a
placeholder and can be described by condition collecting during the symbolic
execution. E.g., at points the control flow branches, knowledge about the guard
of the if statement describes the involved symbolic value.
    Symbolic execution is used as a proof strategy for a sequent calculus of first-
order dynamic logics: A sequent of the form Γ ⇒ {U }[s]ϕ, ∆ represents a sym-
bolic state, where s is the statement left to symbolically execute, U the state
update (i.e., a syntactic
                    V representation
                             W             of accumulated substitusions [3]), ϕ the
postcondition, and Γ ∧ ¬ ∆ describes the accumulated knowledge and path
condition. A rule can have, e.g., the following form (SE rules are read bottom-up)
                Γ, {U }e ⇒ {U }[s1 ]ϕ, ∆   Γ, {U }¬e ⇒ {U }[s2 ]ϕ, ∆
                           Γ ⇒ {U }[if(e) s1 else s2 ]ϕ, ∆
Heavyweight SE with dynamic logics is successfully applied to discover highly
involved bugs in non-concurrent libraries of mainstream languages [9].

2.1      Behavioral Program Logic.
The behavioral program logic (BPL) [19] is a generalization of dynamic logic.
It uses behavioral modalities, which we informally introduce now. One of the
shortcomings of symbolic execution with dynamic logics is that they first fully
symbolically execute the program and then evaluate the postcondition. For dis-
tributed systems the specification, however, often contains a temporal element
and can be partially checked already during symbolic execution.
4       Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

Behavioral Modalities. A behavioral (box-)modality uses a behavioral specifi-
cation (αT , τT ), where αT maps elements of τT to trace formulas and has the
form [s αT τ ] with τ ∈ τT . Its semantics expresses partial correctness: a state σ
satisfies the modality, if every trace of a normally terminating run of s from σ
(the set of these traces is denoted JsKσ ) is a model for the trace formula αT (τ ):
                               αT
                     σ |= [s        τ ] ⇐⇒ ∀θ ∈ JsKσ . θ |= αT (τ )
E.g., for the behavioral specification of post-conditions Tpst = (αpst , τpst ), we use
all BPL formulas as elements of the specification language τpst . The semantics
extracts the last state for a trace.
     τpst = {ϕ | ϕ is a BPL Formula}               θ |= αpst (ϕ) ⇐⇒ last(θ) |= ϕ
    Behavioral specifications separate syntax of the specification (τ ) and its se-
mantics as a trace specification (α). This distinction enables behavioral symbolic
execution: the design of τ can now aim to have a simple proof calculus that is
not restricted by the structure of the logic underlying α. Furthermore, τ can
serve as an interface to external analyses.
    Several behavioral specification frameworks are formalized [20], based on log-
ics (post-conditions, LTL), behavioral types (effect types, session types [16]),
static analyses (points-to) and specification techniques (cooperative method con-
tracts, object invariants). The calculi for these specifications can refer to each
other: the post-condition calculus is used for loop invariants in other calculi.

Symbolic Execution in BPL. As mentioned above, established calculi for dynamic
logics (like JavaDL [1], ABSDL [11] or DTL [4]) perform symbolic execution by
reducing the statement inside a modality without considering the post-condition.
In contrast, for each step in a behavioral type system [2], the statement is
matched with the current specification. BPL combines both: a logical framework
with a behavioral type system-style calculus.
Example 2. We give a simple example using our session type system [21]: the
following expresses that the statement s first calls method m on role f and then n
on role g. Finally, the last action is a return in a state where result == 0 holds.
No other communication, synchronization or suspension happens.
                           α                              
                           s    ST
                                   f !m.g!n. ↓ result == 0
One (slightly prettified) rule for session types is the following.
                                  .                             
                Γ ⇒ {U }this.f = r, ∆         Γ ⇒ {U } s αST L , ∆
                                                           
                       Γ ⇒ {U } this.f!m();s αST r!m.L , ∆
The first premise checks that the role and field coincide, the second premise
reduces the type during the symbolic execution step. Note that this premise
contains no modality – we call such branches side-branches. We stress that the
conclusion of the rule has to match (1) the call in specification and statement
and (2) the method names both syntactically. If matching fails, SE stops.
   Crowbar implements 2 calculi: (1) cooperative contracts [22] with object in-
variants and (2) a session type system for Active Objects [21].
                   Crowbar: Behavioral Symbolic Execution for Active Objects                    5

                                                    ϕ
 1 class C([NonNull]I f){
 2     I g;                                              αST
                                             return 0;                        this.f != null
 3     [Spec: f !m.g!n. ↓ ϕ]
 4     Unit m(){                     this.f!m(); return 0;      αST
                                                                      ↓ϕ      this.g != null
 5       this.f!m();
 6       this.g!m();               this.g!m(); this.f!m(); return 0;           αST
                                                                                     g!n. ↓ ϕ
 7       this.f!m();
 8       return 0;                                                      (1)   this.f != null
 9     }
10 }
                                   this.f!m(); this.g!m();            αST
                                                                            f !m().g!n. ↓ ϕ
                                   this.f!m(); return 0;

Fig. 2. Illustration of guides in BSE. Verification of the method to the left results in a
symbolic execution tree where the dashed nodes are not generated.




Fig. 3. Structure of Crowbar. The ABS compiler absc and the SMT-solvers are external.


3      Behavioral Symbolic Execution and Structure
Behavioral Symbolic Execution. Before describing BSE in more detail in Sec. 5,
we use the short example in Fig. 2 to illustrate the difference between SE and
BSE: the node marked with (1) is not generated, as the type system ensures
that this.f is always non-null (due to being annotated with NonNull). The other
dashed nodes are omitted because the method is specified to make two calls,
but executes three. It does not check any steps after the second call as these are
already following a wrong execution path. We omitted (a) the update, (b) the
collected path condition and (c) the role check branches in the illustration.

Structure. Crowbar has the structure illustrated in Fig. 3 and can be divided
into front-end, middle-end and back-end. We describe each component on a high
level here and give details in the next sections.
     The front-end contains the ABS parser and type-checker, that takes an ABS
file annotated with specification, and outputs for each method (1) its method
body s and (2) a suitable specification τ . The statement s is transformed into
the internal representation of Crowbar and the generated proof obligation (PO)
is a sequent of the form ϕ ⇒ {U }[s α τ ] for fitting α, U and ϕ.
     The middle-end performs behavioral symbolic execution and outputs a sym-
bolic execution tree where the leaves are symbolic nodes (where symbolic execu-
tion could not continue), logic nodes (where a modality-free formula has to be
6       Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

proven valid) or static nodes (where external analyses must be performed). This
part is modular to enable the implementation of further BSE approaches.
    The back-end passes logic nodes to SMT solvers in the SMT-LIB format and
outputs static nodes to the user, who can pass them to their respective analysis.
Symbolic nodes as leaves in the final tree always fail the verification. Additionally,
the back-end transforms the symbolic execution tree of a failed proof into guided
counterexamples in ABS and enhaces it with the values retrieved from the model
of the SMT solver. By using guided counterexamples, the user is not exposed to
the internals of Crowbar and user-interactions are all on the level of the ABS.


4    Front-end: Specification and Usage

Crowbar specifications are part of the input ABS file using Spec-annotations. A
method can be annotated with Ensures and Requires as post and preconditions.
In interfaces, these specifications can only contain parameters (and result, the
special variable for the return value). Objects are annotated with creation condi-
tions (Requires) and invariants (ObjInv). Additionally, loops are annotated with
loop invariants using WhileInv. For an example, we refer to Fig. 1.
    Following the principles behind the Java Modeling Language (JML) [27],
Crowbar supports old to refer to the pre-state of the method and last to refer to
the prestate of the last suspension. Additionally, Crowbar supports the Succeeds
and Overlaps context sets [22]: if the precondition of a method contains assertions
about the heap, then it is not clear which method is responsible to establish it —
due to the concurrency model, the caller has no control over the fields of the callee
object. Context sets specify for a method m the following: the methods in Succeeds
must have run and must establish the precondition as their postcondition. The
methods in Overlaps may have run and must preserve the precondition.
    Additionally, Crowbar supports a variant of local session types, which are
annotated with Local. A local session type for ABS is represented as a string and
specifies calls, synchronization, sequence, repetition and alternative. E.g., the
type from Ex. 2 is specified with [Spec: Local("f!m.g!n.Put(result == 0)")].
    Alternative is specified using +, repetition with *, suspension with Susp(ϕ)
(where ϕ specifies the state before suspension, and analogously for calls !) and
synchronization with Get(e), where e is the targeted expression. Session types
specify how roles in a protocol communicate. The mapping of roles to fields is
specified with [Spec: Role("name",this.field)]. For details we refer to [19,20,21].
    The systems are independent: it is not necessary to specify a local type.

Nullability. ABS implements a nullability type system: fields and variables may be
marked as nullable [Nullable] (default) or non-nullable [NonNull]. Additionally,
nullability type inference can infer nullability for expressions to statically detect
whether a specific field or variable access always accesses a non-null value.

Functional Layer. ABS allows to define side-effect-free functions to simplify
modeling of computations. Function-passing is not allowed. They are, thus,
                   Crowbar: Behavioral Symbolic Execution for Active Objects          7

a special case of Java strictly pure [27,1] methods and we can verify pre-
/postconditions for such functions by transforming them into a simple imperative
structure. To prove that a function T f(p) = e; fulfills its pre- and postcondi-
tions pre, post, we generate the following proof obligation.
                         pre ⇒ result = e; αpst post
                                                       

A contract generates a precondition that enables us to apply it to resursive calls.
This is not circular: the function is unrolled, so function contracts are analogous
to recursive method contracts, and the precondition must be proven to use the
postcondition. Crowbar can establish partial correctness of recursive functions.
Example 3. The following function results in the proof obligation below.
    1 [Spec: Requires(n >= 0)][Spec: Ensures(result >= 0)]
    2 def Int fac(Int n) = if(n <= 1) then 1 else n*fac(n-1);
                                       
            ∀ Int x. x ≥ 0 → fac(x) ≥ 0 ∧ n ≥ 0
                                                              αpst
                                                                             
         → result = if(n <= 1) then 1 else n*fac(n-1);               result ≥ 0


5     Middle-end: Behavioral Symbolic Execution
Crowbar implements 2 kinds of behavioral guides (or just guides)5 : guides from
the type system to reduce branching and guides from the specification.

Nullability Guides. An access that is shown to be non-null by the type system is
marked as such in the intermediate representation of Crowbar. BSE then does
not generate a side-branch to prove that no NullPointerException is thrown.
BSE still generates such a side-branch if the type system can not infer null
safety. This is the default case for all method calls.

Specification Guides. Specification guides influence the shape of the tree and
what side-branchs are generated by linking statements and specification more
closely together than it is possible with post-conditions. While specification
guides are already present in the BPL calculus for object invariants, they are
most prominent in two places in the aforementioned session type system: (1)
During symbolic execution with a local Session Type as specification, Crowbar
checks the order of actions by matching the active type action against the ac-
tive statement. If an action cannot be matched, symbolic execution stops. (2)
Branchings are matched non-greedy: if syntactic matching cannot determine
what branch is taken, then the decision is delayed and all branches are consid-
ered. The contained logical conditions are only generated at the very end, once
the branch is identified and syntactic matching succeeded. E.g., for
          f!m(-10); return 0 αST (r!m(i > 0).r!n) + r!m(i < 0) .Put
                                                                    

the constraint on i is generated not when matching the call on m, but at the end.
   Consider again Fig. 2: Node (1) is omitted because of the nullability guide,
while the other dashed nodes are omitted because of the specification guide.
5
    They are not related to assertion guided SE [14], which is a dynamic technique.
8       Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

Modularity. To avoid restrictions by committing to a special domain-specific
language for rules [28], adding new calculi requires that these are implemented
directly in Crowbar. To do so, data structures for the new specification languages
and for their set of rules must be provided.
    A rule must inherit from the class Rule and (1) provide an abstract pattern
and (2) implement the rule application. An abstract pattern is an instance of
a symbolic node that contains abstract variables. Pattern matching in Crowbar
considers everything that implements the interface AbstractVar an abstract vari-
able. Pattern matching and matching condition (a mapping from abstract vari-
ables to concrete data) generation is implemented generically using reflection
and does not need to be extended by newly extended calculi. In particular, it
ensures that an abstract variable of class C is matched with an instance of a
subclass of class C (that does not implement AbstractVar). The rule application
itself is a method that takes a concrete symbolic node and matching conditions
and returns a list of nodes.


6   Back-end: Verification

The result of (B)SE is a symbolic execution tree. If one of the leaves is a symbolic
node, then some behavioral guide aborted symbolic execution and verification
fails. Otherwise, all leaves are either logic nodes or static nodes.

Logic Nodes. Logic nodes are interfaces that contain no modalities and represent
one proof goal. Crowbar delegates these proof goals to SMT solvers by passing
them the logic nodes translated into SMT-LIB. If all goals can be closed, verifi-
cation succeeds (up to possible static nodes), otherwise, the verification fails.
    The translation has to take care of some differences between BPL without
modalities and SMT-LIB:

Heap BPL has a polymorphic heap, i.e., a heap maps fields to elements of some
   data types. SMT-LIB does not support polymorphic heaps: a heap can map
   fields only to elements of one data type. To amend this, the translation
   splits the polymorphic heap into one monomorphic heap for each data type.
   Unused heaps are removed in a post-processing step.
Partial Functions ABS allows partial pattern matching expressions, which throw
   an error if no branch matches. Crowbar only considers partial correctness
   (and some exceptions), but must encode these expressions as total functions
   for SMT-LIB. This is done by a final ‘else’ branch that returns an under-
   specified function symbol of fitting type. This approach to handle partial
   functions when proving partial correctness is inspired by the KeY system.
Updates BPL supports updates to accumulate substitutions. These substitu-
   tions are applied before the formula is translated.

    The translation to SMT-LIB is implemented in its own module – implement-
ing another backend does not require any changes to the symbolic execution.
                  Crowbar: Behavioral Symbolic Execution for Active Objects           9


   1 class CeFrame {
   2     Int beats = 21239; String s = "object_3";
   3     Unit ce() {                  // Snippet from: heartbeat
   4       String req = "fut_1"; // Fut req = this.s!httpRequest();
   5       Int status = 5;            // Int status = (req).get;
   6       if((status == 200)){}
   7       else {// this.handleError(); Assume following assignments while blocked:
   8          this.beats = 21238;
   9       }
  10       println(toString(this.beats)); // Return stmt, evaluates to: 21238
  11       // Failed postcondition: (heap.beats>=old.beats) /\ (result=heap.beats)
  12       // Failed to show the following sub−obligations:
  13       // (select(anon(heap), this.beats)>=heap.beats)
  14     }
  15 }

  Listing 4. The counterexample generated by Crowbar for the program in Lst. 1.


Static Nodes. Static nodes are generic interfaces to communicate with external
analyses. If a static node is present and all logic nodes can be closed, then the
program is considered verified up to some external analysis on specific output.
For example, the context sets are output together with their heap precondition.
The consistency of cooperative contracts [22] and the adherence to the speci-
fied method order is checked externally and is an inherently non-local analysis.
Similarly, each class with local types outputs a static node for compositionality.

Counterexamples. Crowbar can generate a counterexample program (CE) from
each open branch in the SE tree. Such a CE is a compilable excerpt of the pro-
gram under verification that is modified to illustrate the cause of the verification
failure. CEs allow users to quickly identify specification or implementation issues,
without being exposed to the inner workings of Crowbar.
    CEs are generated from the SE tree by traversing a single, open branch: based
on the applied rule, each node in the tree can be transformed into a statement.
    The result of this reconstruction is an ABS method which contains only state-
ments relevant to runs represented by the open branch. However, not all struc-
ture of the original method is removed: if only one branch of an if statement is
relevant, the content of the other branch is not present in the CE, but the if
statement itself is – this provides the user more guidance to connect the input
program with the CE. Failure caused by loop invariants removes all information
outside the loop (failure inside the loop) or inside a loop (failure outside of it).
    To remove symbolic values and provide concrete values for variables and fields
in the counterexample, Crowbar uses the model generated by (get-model) in the
SMT solver from the failed logic node. Similarly, this information is used to make
the CE a stand-alone executable: any statements that require external context
(method calls, get, await, and object creations) are replaced with assignments
that model the relevant internal effects of the original statement.
10        Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

    With the knowledge extracted from the logic model and the annotations in
the symbolic execution tree, Crowbar can further enrich the counterexamples
with human-readable annotations. While these annotations are not strictly nec-
essary for a working counterexample, they can aid the user in understanding the
generated code. Among these additional annotations are detailed, static eval-
uations of return expressions, known-true statements at different points in the
program, as well as a breakdown of the current proof obligations.
    As an example, the CE generated by Crowbar for the input in Lst. 1 is shown
(slightly prettified) in Lst. 4. Note the absence of the if branch content that is
not on the problematic execution path in the counterexample as well as the
annotations for method calls, return expressions and proof obligations. Concrete
values are chosen by the SMT-solver.


7      Application, Conclusion and Future Work

Crowbar is used in the biggest verification case study for Active Objects: A model
extracted from C code [25] with 260 lines of ABS code, with 5 classes (with in-
variants and creation conditions) and 5 interfaces (with 19 method contracts).
It also contains one function with a contract. The verification succeeds fully
automatically. In contrast, the previously biggest case study with KeY-ABS [12]
has 140 lines of code for 1 class and requires manual interaction. The functional
layer cannot be verified with KeY-ABS and counterexample generation is not avail-
able (and restricted to pretty-printing models of single nodes in KeY-Java [1]).
Attempts to integrate KeY-ABS with external tools [18] or new specification lan-
guages6 have shown that its structure is not suitable for such tasks. A discussion
on the experiences made with KeY-ABS is given in [20, Ch 2.3].

Conclusion. We present Crowbar, a verification tool for Active Objects based
on behavioral symbolic execution. By using behavioral guides, Crowbar inte-
grates verification with static analyses and specification languages to influence
the shape of the symbolic execution tree, which opens the possibility for novel
techniques in verification. Our counterexamples are generated in the input lan-
guage ABS and presented to non-expert users without exposing the verification
mechanism. Crowbar is suited for prototyping and implementing new specifica-
tion approaches to distributed systems: it provides interfaces to implement new
calculi and communicate with external analyses. Crowbar has been used for the
biggest case study using Active Objects and is the first implementation of BSE.

Future Work. We plan to pass static nodes to dynamic monitors, combining
dynamic and static verification [5,15]. Furthermore, we explore the possibility to
export the the proof obligations for the functional layer, which are not specific
to BPL, to specialized provers, e.g., Why3 [13].
6
     KeY-ABS only supports invariants written in ABSDL and ignores the functional layer.
                  Crowbar: Behavioral Symbolic Execution for Active Objects          11

Acknowledgments This work was partially funded by the Hessian LOEWE
initiative within the Software-Factory 4.0 project. We thank Daniel Drodt for
his work on nullability checks.


References
 1. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P. H., and
    Ulbrich, M., Eds. Deductive Software Verification - The KeY Book - From Theory
    to Practice, vol. 10001 of LNCS. Springer, 2016.
 2. Ancona, D., Bono, V., Bravetti, M., Campos, J., Castagna, G., Deniélou,
    P., Gay, S. J., Gesbert, N., Giachino, E., Hu, R., Johnsen, E. B., Martins,
    F., Mascardi, V., Montesi, F., Neykova, R., Ng, N., Padovani, L., Vas-
    concelos, V. T., and Yoshida, N. Behavioral types in programming languages.
    Found. Trends Program. Lang. 3, 2-3 (2016), 95–230.
 3. Beckert, B. A dynamic logic for the formal verification of java card programs.
    In Java Card Workshop (2000), vol. 2041 of LNCS, Springer, pp. 6–24.
 4. Beckert, B., and Bruns, D. Dynamic logic with trace semantics. In CADE
    (2013), vol. 7898 of LNCS, Springer, pp. 315–329.
 5. Chimento, J. M., Ahrendt, W., Pace, G. J., and Schneider, G. Starvoors: A
    tool for combined static and runtime verification of java. In RV (2015), vol. 9333
    of LNCS, Springer, pp. 297–305.
 6. de Boer, F. S., and Bonsangue, M. M. On the nature of symbolic execution.
    In FM (2019), vol. 11800 of LNCS, Springer, pp. 64–80.
 7. de Boer, F. S., Bonsangue, M. M., Johnsen, E. B., Pun, V. K. I., Tarifa,
    S. L. T., and Tveito, L. Sympaths: Symbolic execution meets partial order
    reduction. In 20 Years of KeY, vol. 12345 of LNCS. Springer, 2020, pp. 313–338.
 8. de Boer, F. S., Serbanescu, V., Hähnle, R., Henrio, L., Rochas, J., Din,
    C. C., Johnsen, E. B., Sirjani, M., Khamespanah, E., Fernandez-Reyes,
    K., and Yang, A. M. A survey of active object languages. ACM Comput. Surv.
    50, 5 (2017), 76:1–76:39.
 9. de Gouw, S., Rot, J., de Boer, F. S., Bubel, R., and Hähnle, R. Openjdk’s
    java.utils.collection.sort() is broken: The good, the bad and the worst case. In CAV
    (1) (2015), vol. 9206 of LNCS, Springer, pp. 273–289.
10. Din, C. C., Bubel, R., and Hähnle, R. KeY-ABS: A deductive verification
    tool for the concurrent modelling language ABS. In CADE’25 (2015), vol. 9195 of
    LNCS, pp. 517–526.
11. Din, C. C., and Owe, O. Compositional reasoning about active objects with
    shared futures. Formal Aspects Comput. 27, 3 (2015), 551–572.
12. Din, C. C., Tarifa, S. L. T., Hähnle, R., and Johnsen, E. B. History-based
    specification and verification of scalable concurrent and distributed systems. In
    ICFEM (2015), vol. 9407 of LNCS, Springer, pp. 217–233.
13. Filliâtre, J., and Paskevich, A. Why3 - where programs meet provers. In
    ESOP (2013) (2013), M. Felleisen and P. Gardner, Eds., vol. 7792 of LNCS,
    Springer, pp. 125–128.
14. Guo, S., Kusano, M., Wang, C., Yang, Z., and Gupta, A. Assertion guided
    symbolic execution of multithreaded programs. In ESEC/FSE (2015), E. D. Nitto,
    M. Harman, and P. Heymans, Eds., ACM, pp. 854–865.
15. Hähnle, R., Haubner, A. W., and Kamburjan, E. Locally Static, Globally
    Dynamic Session Types for Active Objects. In Recent Developments in the Design
12     Eduard Kamburjan, Marco Scaletta, and Nils Rollshausen

    and Implementation of Programming Languages (2020), vol. 86 of OASIcs, Schloss
    Dagstuhl–Leibniz-Zentrum für Informatik, pp. 1:1–1:24.
16. Honda, K., Yoshida, N., and Carbone, M. Multiparty asynchronous session
    types. In POPL (2008), ACM, pp. 273–284.
17. Johnsen, E. B., Hähnle, R., Schäfer, J., Schlatte, R., and Steffen, M.
    ABS: A core language for abstract behavioral specification. In FMCO (2010),
    vol. 6957 of LNCS, Springer, pp. 142–164.
18. Kamburjan, E. Detecting deadlocks in formal system models with condition
    synchronization. In AVOCS (2018), vol. 76 of ECEASST.
19. Kamburjan, E. Behavioral program logic. In TABLEAUX (2019), vol. 11714 of
    LNCS, Springer, pp. 391–408.
20. Kamburjan, E. Modular Verification of a Modular Specification: Behavioral Types
    as Program Logics. PhD thesis, Technische Universität Darmstadt, 2020.
21. Kamburjan, E., and Chen, T. Stateful behavioral types for active objects. In
    IFM (2018), vol. 11023 of LNCS, Springer, pp. 214–235.
22. Kamburjan, E., Din, C. C., Hähnle, R., and Johnsen, E. B. Behavioral
    contracts for cooperative scheduling, 2020.
23. Kamburjan, E., and Hähnle, R. Deductive verification of railway operations.
    In RSSRail (2017), vol. 10598 of LNCS, Springer, pp. 131–147.
24. Kamburjan, E., and Hähnle, R. Prototyping formal system models with active
    objects. In ICE (2018), vol. 279 of EPTCS, pp. 52–67.
25. Kamburjan, E., and Wasser, N. Deductive verification of programs with un-
    derspecified semantics by model extraction. Under Review.
26. King, J. C. Symbolic execution and program testing. Commun. ACM 19, 7
    (1976), 385–394.
27. Leavens, G. T., Poll, E., Clifton, C., Cheon, Y., Ruby, C., Cok, D.,
    Müller, P., Kiniry, J., Chalin, P., Zimmerman, D. M., and Dietl, W. JML
    Reference Manual, May 2013. Draft revision 2344.
28. Mitsch, S., and Platzer, A. A retrospective on developing hybrid system
    provers in the KeYmaera family - A tale of three provers. In 20 Years of KeY,
    vol. 12345 of LNCS. Springer, 2020, pp. 21–64.
29. Santos, J. F., Maksimovic, P., Ayoun, S., and Gardner, P. Gillian, part i: a
    multi-language platform for symbolic execution. In PLDI (2020), ACM, pp. 927–
    942.
30. Steinhöfel, D. Abstract Execution: Automatically Proving Infinitely Many Pro-
    grams. PhD thesis, Technische Universität Darmstadt, Germany, 2020.
31. Yang, G., Filieri, A., Borges, M., Clun, D., and Wen, J. Chapter five -
    advances in symbolic execution. Adv. Comput. 113 (2019), 225–287.
