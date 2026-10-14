                                               Static and Dynamic Verification of OCaml
                                                    Programs: The Gospel Ecosystem
                                                          (Extended Version)

                                                       Tiago Lopes Soares, Ion Chirica, and Mário Pereira

                                                   NOVA LINCS, Nova School of Science and Technology, Portugal
arXiv:2407.17289v2 [cs.LO] 26 Jul 2024




                                               Abstract. We present our work on the collaborative use of dynamic and
                                               static analysis tools for the verification of software written in the OCaml
                                               language. We build upon Gospel, a specification language for OCaml that
                                               can be used both in dynamic and static analyses. We employ Ortac, for
                                               runtime assertion checking, and Cameleer and CFML for the deductive
                                               verification of OCaml code. We report on the use of such tools to build a
                                               case study of collaborative analysis of a non-trivial OCaml program. This
                                               shows how these tools nicely complement each others, while at the same
                                               highlights the differences when writing specification targeting dynamic
                                               or static analysis methods.


                                         Keywords: Software Verification · Dynamic Analysis · Deductive Software Ver-
                                         ification · Gospel· OCaml· Ortac· Cameleer· CFML


                                         1   Introduction

                                         In the past decades, we have witnessed remarkable developments in the field of
                                         formal methods. In particular, Deductive Software Verification [13] and Runtime
                                         Assertion Checking (RAC) [8] tools have evolved into practical, scalable, and
                                         trustworthy systems that can be used to verify complex pieces of software. How-
                                         ever, with some notable exceptions, dynamic and static analysis are very rarely
                                         used collaboratively to analyze (parts of) a program. Formal methods practition-
                                         ers tend to choose either dynamic or static analysis, each with its own limitations:
                                         dynamic checks sacrifice expressiveness and completeness, while static analysis
                                         requires more human interaction, hence it is less automated. We strongly believe
                                         this separation is inherently restrictive and advocate for the collaborative use of
                                         dynamic and static tools to analyze the same software system.
                                             In this paper, we present our work on the joint use of dynamic analysis and
                                         static verification tools. Specifically, we focus on programs written in the OCaml
                                         language. In our approach, static and dynamic analysis are treated not as mu-
                                         tually exclusive but rather as two sides of the same coin. Our vision is that
                                         these two techniques can be combined by operating over (roughly) the same
                                         specification. A core ingredient in our approach is a specification language us-
                                         able by both analysis approaches. We leverage Gospel [6], a tool-agnostic OCaml
2       Tiago Lopes Soares, Ion Chirica, and Mário Pereira

specification language that serves as a common ground for the communication
between dynamic and static methods. Gospel is strongly inspired by other be-
havioral specification languages [17], namely SPARK [3], JML [22], and ACSL [1]
which can also be used both for dynamic and static analysis of code.
    We propose the following, rather natural, certification workflow: first, use
RAC tools to increase the confidence on the devised specification for parts of a
program; second, apply deductive verification on that very same piece of code to
achieve even higher correctness guarantees. Our analysis pipeline is materialized,
on the one hand, through the use of Ortac [15], a RAC tool for OCaml, and on the
other hand through the deductive verification of OCaml code using Cameleer [30]
and CFML [4]. All three are able to interpret and process Gospel specifications.
    We apply our certification pipeline to a piece of OCaml code, issued from the
widely used OCamlGraph library, whose verification is non-trivial. We apply RAC
to parts of the program, namely auxiliary data structures, and then incrementally
use deductive verification to achieve higher correctness guarantees. This shows
how the different tools of the Gospel ecosystem complement each others, but also
highlights the differences of writing Gospel specifications targeting dynamic or
static analysis.
    We believe our proposal opens interesting perspectives on the practical adop-
tion of formal methods among the OCaml community. To the best of our knowl-
edge, this is the first time a collaborative use of RAC and deductive verification
tools is done in the setting of multi-paradigm language like OCaml. Finally, we
believe our reported experience makes a contribution towards bridging the gap
between different program specification and analysis paradigms.
    This paper is organized as follows. In Section 2, we survey the Gospel language
and the tools that compose its ecosystem. In Section 3, we describe our proposal
certification workflow for the collaborative use of dynamic and static analysis of
OCaml code. In Section 4, we put our pipeline to work on the case study. Finally,
we conclude with some related work, Section 5, and closing remarks and future
perspectives in Section 6. All the software and examples used in this paper are
publicly available in a companion artifact [35].

Labels on code listings. Throughout this paper, we present many different code
listings written in the three languages our tools manipulate, i.e., Gospel, OCaml,
and CFML (which is basically Coq syntax augmented with Separation Logic
operators). To ease the reading process, we attach a label to each listing, on the
top-right corner, that indicates the input language(s).


2     The Gospel Ecosystem, in a Nutshell
2.1   Gospel – A Specification Language for OCaml
Gospel (Generic OCaml SPEcification Language) is a behavioral specification
language for OCaml code. It is a contract-based, strongly typed language, whose
semantics is defined in terms of a translation into Separation Logic [5]. Gospel
terms are written in a subset of OCaml, augmented with quantifiers. Although
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem        3

  type α t                                                      Gospel + OCaml
  (*@ mutable model elems : α list *)

  val create : unit → α t
  (*@ q = create ()
        ensures q.elems = [] *)

  val push : α t → α → unit
  (*@ push q x
        modifies q
        ensures q.elems = old q.elems @ [x] *)

  exception Empty

  val pop : α t → α
  (*@ x = pop q
        modifies q
        raises Empty → old q.elems = [] = q.elems
        ensures x :: q.elems = old q.elems *)

  val is_empty : α t → bool
  (*@ b = is_empty q
        ensures b = q.elems = [] *)

  val transfer : α t → α t → unit
  (*@ transfer q1 q2
        modifies q1, q2
        ensures q1.elems = [] && q2.elems = old (q2.elems @ q1.elems) *)



                       Fig. 1: Gospel Queue Specification.



Gospel specifications are semantically equivalent to Separation Logic, these are
much more lightweight and concise to read and write. For instance, Gospel as-
sumes by default that function parameters, as well as their return values, are
separated in memory and that the caller has full ownership. This eliminates the
need for explicitly stating properties that would seem natural to an everyday
programmer, but nevertheless would be necessary in other platforms built on
Separation Logic, such as VeriFast [19] or Viper [27].
    In Figure 1, we present an OCaml interface, adapted from the original Gospel
paper [6], where we specify the behaviour of a polymorphic FIFO queue. We start
by defining the queue type α t and giving it a model field. A model is a field
that can only be accessed in specifications and acts as a logical representation
of the type. In this case, the logical representation of the queue is a α list. By
marking this field as mutable, we state that the contents of the queue maybe
mutated in-place.
4       Tiago Lopes Soares, Ion Chirica, and Mário Pereira

    The create function returns an empty queue, the push and pop functions
modify the model of the queue by inserting at its tail and removing from its head,
respectively. Additionally, pop also throws an exception if the queue is empty,
not changing the contents of the model. The is_empty function decides whether
the model of the queue is the empty list. Finally, transfer empties q1 and
concatenates all its elements to the model of q2. Its specification also implicitly
states that both queues are separate in memory. To showcase the benefits of this
design choice, we present an equivalent Separation Logic specification where we
assume the existence of a representation predicate Q that relates a memory
location with its logical representation (in this case, a list) as well as claiming
ownership of the data structure:

      ∀q1 q2 L1 L2 ,
       {Q(q1 , L1 ) ⋆ Q(q2 , L2 )}(transfer q1 q2 ){Q(q1 , nil) ⋆ Q(q2 , L2 ++L1 )}

By writing our specifications in Gospel, we avoid having to explicitly write con-
ditions relating to ownership and separation and can focus on describing the
observable behaviour of the function. It is worth noting that Gospel is not tied to
any particular tool or analysis framework. The remaining of this section presents
the tools one can use to interface with Gospel, in order to dynamically and stat-
ically verify OCaml programs.

2.2    Ortac – Runtime Assertion Checking of OCaml Programs
Ortac is a RAC tool for OCaml code. It consumes Gospel-annotated OCaml inter-
face files to generate a wrapper around a candidate implementation that dynam-
ically checks the supplied specification. This wrapper uses the implementation as
a black-box: it tests the validity of the precondition when the function is called
and check if the postcondition holds when the function returns.
    The design and use of the Ortac framework are centered around two main
principles: first, it should work fully automatically, only requiring a user to write
the Gospel specification; second, it is a modular and extensible tool, where users
can extend the behaviour and capabilities of Ortac via plugins. The former is an
important requirement for OCaml programmers to smoothly integrate RAC in
development pipelines, where Ortac can be used as an additional guarantee layer
on deployed code. The latter is a crucial feature of the tool, since it provides the
necessary building blocks to accommodate different specification-based testing
techniques around a core Ortac. In its core, Ortac features a translation mecha-
nism from the Gospel executable subset into OCaml code. Each plugin exploits
this translation to implement different analysis strategies of Gospel specifications.
    Two main plugins have already been developed for Ortac: (i) an interface to
Monolith [32], a fuzz testing tool for OCaml libraries; (ii) the QCheck-STM plugin,
for model-based testing of OCaml implementations. In this paper, we frame our
use of Ortac to the QCheck-STM option. The main purpose of this plugin is to
generate a set of random calls to functions exposed in an OCaml interface file
and checks whether their operational behaviour matches the logical behaviour
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem          5

expressed in Gospel annotations. From a practical point of view, this plugin wraps
Gospel specification and a candidate implementation file into instrumented code
that interfaces with STM [26], a state-machine testing library for OCaml code. In
turn, STM builds on QCheck [11], an OCaml property-based testing framework
inspired by QuickCheck [7].


2.3   Cameleer – Auto-active Verification of OCaml Programs

Cameleer is a tool for deductive verification of OCaml programs, conceived with
proof automation in mind. It takes as input Gospel-annotated OCaml code and
translates it into an equivalent WhyML representation, the programming and
specification language of the Why3 framework [2]. One of the key strengths of
using Why3 is its ability to interface with several theorem provers, whether
automated or interactive, ultimately providing a more flexible and ergonomic
proof experience. Furthermore, Why3 allows users to conduct some lightweight
interaction [12] to aid in the proof of a failing Verification Condition (VC).
    To introduce Cameleer, let us consider the queue data structure and the
implementation of the push operation. A queue is defined using two lists, front
and rear, as follows:
  type α t = {                                                    Gospel + OCaml
    mutable front : α list; mutable rear : α list;
  }
  (*@ mutable model elems : α list *)
  (*@ with x invariant (x.front = [] → x.rear = []) &&
                        x.elems = x.front @ List.rev x.rear *)

Elements are pushed into the head of the rear list and popped from the front
list. This type is also given a type invariant, which states that if front is empty,
so is the rear, and that the model elems stands for the concatenation of front
and the reverse of rear. If the queue is empty then we assign front the singleton
list [x]; otherwise we add it to the head of rear. Additionally, we update elems
by appending the element at the tail, as follows:
   let push x q =                                                  Gospel + OCaml
    if is_empty q then q.front ← [x] else q.rear ← x :: q.rear;
    q.elems ← q.elems @ [x]
  (*@ push x q
      modifies q
      ensures q.elems = old q.elems @ [x] *)

The specification of push is given with regards to elems, the model of the
queue. Note how this Gospel specification is the same as the one in the interface
shown in Figure 1. Assuming the file queue.ml contains the above implementa-
tion, starting a proof with Cameleer is a simple matter of calling the following
command: cameleer queue.ml. Cameleer translates the input program into an
equivalent WhyML representation, launching a graphical interface for the Why3
IDE. For the implementation of all queue operations, Why3 generates a total of
40 VCs, all quickly discharged by the Alt-Ergo [18] SMT solver.
6        Tiago Lopes Soares, Ion Chirica, and Mário Pereira

    Why3 is a very natural choice to translate Gospel into, given that they are,
at least on a surface level, very similar. Nevertheless, its semantics differ in
that Why3 does not employ Separation Logic or any kind of permission based
logic. Even though the Why3 type-and-effects system makes similar assumptions
relative to what is expected in Gospel [16], it falls short when it faces programs
with more sophisticated constructs such as recursive types with mutable fields.

2.4     CFML – Interactive Verification of OCaml Programs
In order to fully capture the meaning of Gospel specifications we must turn to
a more expressive logic. We choose CFML (Characteristic Formulae for ML), a
Coq [29] framework created for the verification of OCaml code using Separation
Logic. CFML is composed of:
    – A translator mechanism, which takes an OCaml program and generates a
      Coq translation of such program;
    – A higher-order Separation Logic encoding in Coq, together with a compre-
      hensive library of tactics.
To verify Gospel with CFML, we first use the aforementioned translator to trans-
late the OCaml implementation into Coq. Next, we translate the Gospel specifi-
cations into CFML by means of a prototype tool1 . Finally, we write a proof script
proving the generated specification adheres to the OCaml implementation.
    To demonstrate how we deal with Gospel in CFML, we feed it the specifi-
cation in Figure 1. In the case of such an interface, we first translate the type
declaration. Since the type has a mutable model field it is ephemeral, meaning
it is treated as a loc value, the CFML type for mutable OCaml values. To rea-
son about a queue, we assume a representation predicate that relates its entry
pointer and a logical list of its elements. This is as follows:
   Parameter Queue : ∀ A, list A → loc → hprop.                            CFML
Note how the return value of this representation predicate is not Prop, but
rather hprop, the type of heap-parameterized propositions. Our tool does not
generate the body for this predicate, it must be defined later by the user once
an implementation for the queue type is provided.
   What remains to be translated are the OCaml function declarations, together
with Gospel contracts. Let us take push as an example. A top-level function is
represented in CFML using the val type:
  Parameter push : val.                                                  CFML
The Gospel specification of the push function translates as follows:
    Lemma push_spec :                                                CFML
      ∀ A (q : loc) (elems : list A) (x : A),
      SPEC (push q x)
        PRE (q ; Queue elems)
        POSTUNIT (∃∃ elems’, q ; Queue elems’ ⋆ [elems’ = elems ++ [x]]).
1
    https://github.com/ocaml-gospel/gospel2cfml
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem                              7


                                                INCONSISTENT           CRITICAL
                                                                                                num
                     -

                      -
                          ↳         >
                                        ORTAC    >
                                                     mummus
                                                     · P
                                                       ?
                                                            NO
                                                                     >
                                                                         mummus
                                                                         · &
                                                                                  NO
                                                                                       Y
                                                                                           -
                                                                                                ↳
                                                                                            -



                    GOSPEL SPEC                  YES                 YES
                         E
                          I
                                                                                       DYNAMICALLY
                   IMPLEMENTATION                                                          VERIFIED
                          ↑                                                1


                                                                     CAMELEER
                                                                            I


                                        1                               E
                                                                       CFML




                                                                           N

                                                                 YES

                                                                         mummus
                                                                           P
                                                                 INCONSISTENT
                                                                 -
                                                                                  NO
                                                                                       *
                                                                                           m
                                                                                       FORMALLY
                                                                                       VERIFIED




                          Fig. 2: Gospel certification workflow.


As mentioned in Section 2.1, Gospel makes several assumption in regards to
ownership of values. In this case, it assumes that the queue is owned before and
after a call to push. Naturally, these properties must now be made explicit in
the CFML specification.
    In the precondition, ownership of q is claimed, and its model is now accessible.
Notation q ; Queue elems stands for a well-formed queue with entry pointer q,
whose model is elems. In the postcondition, we once again claim ownership of
q while also stating that it is now represented by the updated model elems’,
which is introduced using ∃∃ , the Separation Logic existential quantifier. The
Gospel postcondition, i.e., the pushed element is at the tail of the updated list,
is encoded as well. This condition is within a [...] block, meaning it is a pure
assertion, i.e., it does not dependent on heap-allocated elements.
    The remaining generated CFML specifications are relatively similar: for each
OCaml top-level function it creates a Parameter that represents such a func-
tion, claiming ownership of the mutable parameters via the Queue representation
predicate. All user-supplied Gospel specification are translated into pure blocks.

3   Certification Workflow
In this section, we present our proposal for a certification workflow that com-
bines the tools of the Gospel ecosystem. We show how one can employ different
analysis paradigms to achieve a flexible and adaptable pipeline. Our proposal is
graphically summarized in Figure 2.
    The core element in our pipeline are Gospel-annotated OCaml interface files.
Such interfaces must capture the behavior of parts of the whole implementation,
meaning the user might only wish to analyze specific points in their code. To-
gether with such interface files, one must provide OCaml implementation for the
specified functions.
    As a first analysis step, we propose to use Ortac to dynamically check the
implementation adheres to the supplied specification. This is a natural entry
point in our analysis diagram, since Ortac is the tool that requires less user
interaction, hence easier to include in a development pipeline.
8       Tiago Lopes Soares, Ion Chirica, and Mário Pereira

    At this point, one can very well be satisfied with the assurances that Ortac
provides. However, if the programmer requires a greater degree of confidence in
the correctness of their code, they can formally verify (parts of) their programs
using Cameleer and/or CFML, once Ortac can no longer find mismatches between
code and specification. It is important to note that the effort to prove the cor-
rectness of a program should only begin once we are almost certain that the
specification holds. However, there are situations where the proof will fail either
due to an incomplete specification or some problem with the code itself. In both
cases, and especially when many changes are made, it is beneficial to run the
updated program through Ortac, to check if the modifications did not break our
program.
    Between the two tools, Cameleer is easier to work with since the SMT solvers
do the heavy lifting of discharging the necessary verification conditions. On the
other hand, CFML is the tool of choice when it comes to reason about more
complex OCaml programs, in particular those that deal with heap-allocated data
structures.


4     Case Study: Path Checking in a Graph

As our main case study, we chose an algorithm adapted from OCamlGraph [10], a
library featuring a large set of generic graph data structures and operations. This
algorithm checks whether there is a path in a graph between two given nodes.
In this section we first present the implementation that will be used throughout,
followed by a dynamic analysis on Ortac; afterwards we present a proof of the
algorithm in Cameleer; and finally, a proof in CFML.


4.1    Implementation

The path checking algorithm is implemented as a functor Check, making it com-
pletely modular to the actual implementation of the graph data structure and
operations. In this case, the functor argument is a module that contains the
type of graphs, gt, and a function that returns the list of successors for some
vertex. Additionally, graph vertices must respect the COMPARABLE module signa-
ture which defines a type equipped with order and equivalence relations and a
hash function. For the sake of completeness, the definition of COMPARABLE can
be found in Appendix A.
  module Check                                                          OCaml
      (G : sig
        module V : COMPARABLE
        type gt
        val successors : gt → V.t → V.t list
      end) =
    sig
      val check_path : G.gt → G.V.t → G.V.t → bool
    end
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem        9

The implementation of this algorithm follows a classical approach. To check if
there is a path between two nodes, v1 and v2, we employ a Breadth First Search
starting at v1 and, during the search, test if the visiting node is v2. This is
implemented in OCaml as follows:
  module HV = Hashtbl.Make(G.V) (* hash table for vertices *)           OCaml

  let check_path graph v1 v2 =
    let marked = HV.create 97 in
    let [@ghost] visited = HV.create 97 in
    let q = Queue.create () in
    let rec loop () =
      if Queue.is_empty q then (* exhausted graph and no path found *)
        false
      else
        let v = Queue.pop q in
        if G.V.compare v v2 = 0 then true (* path found *)
        else begin
          HV.add visited v ();
          let rec iter_succ sucs = ... in
          iter_succ (G.successors graph v);
          loop () end in
    HV.add marked v1 ();
    Queue.add v1 q;
    loop ()

The algorithm uses the marked hash table to tag the vertices found during traver-
sal, but not yet fully explored (i.e., still waiting in the traversal queue). This
is the role of the auxiliary ghost table visited, which stores all the vertices
that have been popped from queue q. It is worth noting that table visited is
only used to ease the specification and proof process, having no runtime impli-
cations [14].
    The core of the algorithm lies in the loop function. An empty queue implies
that we have traversed the graph and were unable to find v2. However, if the
popped element of the queue, v, is equal to v2 then we found a path. If v is not
the destination vertex, then we add its successors to the queue and mark them
in the recursive function iter_succ.
    The complete OCaml implementation is provided in the companion artifact.


4.2   Dynamic Analysis of Auxiliary Data Structures, in Ortac

To smoothly tackle the verification of the check_path implementation, we chose
to dynamically analyze the used auxiliary data structures. In particular, we
analyze the queue and hash table structures, provided by the Queue and Hashtbl
module from the OCaml standard library.
    To dynamically analyze the Queue module, we revisit the specification de-
picted in Figure 1. However, for the sake of the specification being completely
executable, hence usable by Ortac, we must perform some changes to such a
10        Tiago Lopes Soares, Ion Chirica, and Mário Pereira

     type (!α, !β) t                                             Gospel + OCaml
     (*@ mutable model contents : (α * β) list *)

     val create : ?random: bool → int → (α, β) t
     (*@ h = create ?random size
         ensures h.contents = [] *)

     val add : (α, β) t → α → β → unit
     (*@ add h k v
         modifies h
         ensures h.contents = (k, v) :: old h.contents *)

     val mem : (α, β) t → α → bool
     (*@ b = mem h k
         ensures b = List.mem k (List.map fst h.contents) *)


           Fig. 3: Excerpt of the Hashtbl module, specified using Gospel.


specification. Specifically, we must split the logic of the postcondition of pop
into two clauses: one of the form t.elems = ..., which captures the state of
the model when the function returns; another to assert how the returned value
relates to the model. Finally, the QCheck-STM plugin is only able to analyze
functions featuring a single argument of type α t, the type of queues, hence we
remove the transfer function. The adapted Queue specification (equivalent to
the one in Figure 1, used by Ortac, is given in Appendix B.
    To analyze the Hashtbl module in Ortac, we use the Gospel specification and
hash table operations depicted in Figure 3. The hash table type is defined as
(!α, !β) t, meaning it represents a hash table from keys of type α bound to
values of type β (the ! symbol is used in OCaml type-checker to track variance
and covariance of type parameters). From a logical point of view, an hash table
is modeled as an association list (field contents), i.e., the pair (k, v) is in the
model if and only if key k is bound to value v in the table. Given such model
type, the supplied Gospel specification for three hash table operations (the ones
used in the check_path implementation) is the expected one. The complete
specification of the Hashtbl module is actually part of the QCheck-STM plugin
test-suite and is publicly available2 .
    We feed the Queue and Hashtbl specifications to Ortac, which uses the
QCheck-STM plugin to generate an instrumented OCaml wrapper for random
calls on those data structures operations. As candidate implementations, for both
modules, we use the actual implementations provided by the OCaml standard
library. Ortac successfully checks such implementations, meaning the randomly
generated traces of function calls do not violate the expected behavior expressed
in the Gospel specifications.
2
     https://github.com/ocaml-gospel/ortac/blob/main/plugins/qcheck-stm/
     test/hashtbl.mli
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem          11

4.3   Path Checking Proof, in Cameleer
To conduct a proof of the check_path function, we must first provide a specifi-
cation to the Check functor, which means we also need to annotate the module
it receives as an argument. This is as follows:
   type gt                                                   Gospel + OCaml
  (*@ model dom: V.t fset
      model succ: V.t → V.t fset
      with x invariant ∀ v1, v2.
      mem v1 x.dom → mem v2 (x.succ v1) → mem v2 x.dom *)

  val successors : gt → V.t → V.t list
  (*@ l = successors graph source
      requires mem source graph.dom
      ensures ∀ v’. List.mem v’ l ↔ Fset.mem v’ (g.succ source) *)
First, we attach two models to the gt type: the set of vertices in the graph, dom,
as well as a successor function succ that returns all the finite set of successors of
a given vertex. Additionally, we supply a type invariant that states the dom set is
closed under the succ function. Finally, the specification of successor function
states it returns the complete list of successors of node source.
    We can specify the actual check_path function. In this, this function imple-
ments an algorithm that decides whether there is a sequence of edges that allows
one to travel from v1 to v2. Such a property is captured by the following Gospel
predicates:
  (*@ predicate is_path (v1 v2: G.V.t) (l: G.V.t seq) (g: G.gt) = Gospel
         let len = Seq.length l in
         if len = 0 then v1 = v2 else
           edge v1 l[0] g && l[len - 1] = v2 && mem v1 g.G.dom &&
           ∀ i. 0 ≤ i < len - 1 → edge l[i] l[i+1] g *)

  (*@ predicate has_path (v1 v2 : G.V.t) (g : G.gt) =
        ∃ p. is_path v1 v2 p g *)
Here, seq stands for the type of finite mathematical sequences provided in the
Gospel standard library. The specification of check_path is, now, rather intu-
itive:
   val check_path : G.gt → G.V.t → G.V.t → bool              Gospel + OCaml
  (*@ b = check_path g v1 v2
      requires mem v1 graph.G.dom
      ensures b ↔ has_path g v1 v2 *)
Note that we require v1 to be a vertex in the graph, since our implementation
maintains the invariant that marked nodes are a subset of the graph domain.
   Having defined a Gospel specification for the Check functor and the check_path
function, one might be tempted to apply Ortac to dynamically test the whole
OCaml implementation. However, the definition of the has_path predicate pre-
vents us from doing so: general use of existential quantification does not fall into
the Gospel’s executable fragment.
12      Tiago Lopes Soares, Ion Chirica, and Mário Pereira

                                    MARILED               UNMARKED
                                                  QUELE




                     8                                    ⑧
                                                           %
                   VISITED
                                                                           U
                             s                                         %
                         ⑨                                         ⑧
                                                               --




                                                               ⑨
                                        vi
                                 ·...
                                                   s
                                        ·

                                              >            ⑨




       Fig. 4: Visual representation of the intermediate_value lemma.


    The complete Gospel specification of the inner functions in the check_path
definition is given in the companion artifact. We highlight here only the main
invariants of the loop function that allows one to prove the correctness and
completeness of the algorithm.
    Correctness means that if check_path returns true, there is indeed a path
between v1 and v2 in the graph. This is achieved by maintaining the invariant
that there is always a path from v1 to a marked vertex, which includes all vertices
in the queue and the visited table. This is expressed in Gospel as follows:
  invariant ∀ v. mem v marked.HV.dom → has_path v1 v graph                 Gospel

Completeness means that if there is no path, then we have indeed fully explored
the graph. In other words, while the traversal is not finished, if there is a path
from v1 to v2, then such a path must go trough an intermediate vertex w from
the queue. This is expressed in Gospel as follows:
  invariant has_path v1 v2 graph →                                         Gospel
             ∃ w. Seq.mem w q.Queue.elems ∧ has_path w v2 graph

After setting on the correct Gospel specification, the check_path proof is done
mostly automatically, using a combination of SMT solvers. The only part requir-
ing extra human interaction is in proving the completeness invariant. To do so,
one must provide a classic intermediate value lemma. Figure 4 depicts a visual
representation of such a statement: if there is a path from a marked node v to
an unmarked node u, then it must be the case that there is an intermediate edge
crossing the set of marked elements to the set of unmarked elements. In our case,
we need to retrieve the actual bridge between the visited set and the queue,
colored in green in Figure 4. There is a constructive proof of such a result, which
amounts to a recursive traversal from v to u, until one finds the green arrow.
This is encoded in Cameleer as a ghost function.


4.4   Proof of Auxiliary Data Structures, in CFML

As a final piece of our case study, we can further increase our degree of confidence
in the OCaml check_path implementation by actually proving the implementa-
tion of the auxiliary queue and hash table data structures. Reasoning about such
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem       13

structures is out of scope for Cameleer, since these are pointer-based structures.
We must turn ourselves into CFML.
    We do not conduct a proof for the Hashtbl module, has this was already done
by François Pottier in 2017 [31]. As for Queue, we prove here that the OCaml
standard library implementation adheres to the Gospel specification presented
in Figure 1. The type of queues is defined as follows:
  type α cell_contents = { content: α; mutable next: α cell; }            OCaml
  and   α cell = Nil | Cons of α cell_contents

  type α queue = {
    mutable length: int;
    mutable first: α cell;
    mutable last: α cell
  }

Basically, a queue is built on top of a mutable linked-list whose entry pointer
is stored in field first, while the last element is pointed by last. Maintaining
these two pointers is what allows one to achieve constant-time push, pop, and
transfer operations.
    To start a CFML proof, we must first supply representation predicates for
our structures. For the case of cell, this is as follows:
   Definition Cell A (v: A) (n c: cell_ A) : hprop :=                     CFML
    ∃∃ cf, [c = Cons cf] ⋆ (cf 7→ ‘{ content’ := v; next’ := n }).

  Fixpoint Cell_Seg {A} (L: list A) (to from: cell_ A) : hprop :=
    match L with
    | nil =⇒ [to = from]
    | x :: L’ =⇒ ∃∃ n, (from ; Cell x n) ⋆ (n ; Cell_Seg L’ to)
    end.

The Cell predicate claims ownership of a single heap-allocated cell c, whose
content is v and the next element is cell n. This definition uses notation
cf 7→ ... , which stands for a cell cf that owns the fields of a record. The
Cell_Seg predicate captures the common notion of a list segment. It is worth
noting that with such a representation, if c1 ; Cell_Seg L c2 holds for some
cells c1 and c2 and a logical list L, then the predicate does not own pointer c2.
We equip the queue type with a representation predicate, as follows:
  Definition Queue A (L: list A) (q: loc) : hprop :=                       CFML
    ∃∃ (cf cl: cell_ A),
    (q 7→ ‘{ length’ := length L; first’ := cf; last’ := cl }) ⋆
       If L = nil
         then [cf = Nil] ⋆ [cl = Nil]
         else ∃∃ x L’, [L = L’ & x] ⋆
              (cf ; Cell_Seg L’ cl) ⋆ (cl ; Cell x Nil).

This predicate claims ownership of all the elements the first list contains,
except the last one, and claims ownership of the last cell, whose contents is
equal to the last element of the logical list L.
14     Tiago Lopes Soares, Ion Chirica, and Mário Pereira

      Case study          # VCs     LoC / LoS Proof Replay (s) Fully Auto.
      Path checking
        Ortac                -        11 / 42          -
        Cameleer            213      50 / 118        26.63
      Queue
        Ortac                 -       6 / 21            -
        CFML                 4        19 / 72           -
        Cameleer             47       31 / 25         1.93
      Hashtbl
        Ortac                 -      32 / 45           -
        CFML                 89     186 / 1397         -
     Table 1: Summary of the case studies and their respective statistics.



    The above representation predicates are the building blocks to provide spec-
ification to queue operations and conduct interactive proof using CFML. The
complete proof of the Queue module, i.e., representation predicates, auxiliary
lemmas, and specification verification for each function, is provided in the com-
panion artifact.
    Table 1 showcases a summary of the case studies. For the different tools we
present the number of Verifications Conditions, in the case of Cameleer, and
number of Theorems and Lemmas in the case of CFML, the number of lines
of code (LoC) and lines of specification/script (LoS), the proof replay time in
Cameleer (not applicable to CFML and Ortac) and if the conducted proofs were
fully automatic. These measurements were conducted on a Lenovo Thinkpad X1
Carbon 8th Generation machine, running Linux kernel 5.4.0-60-generic, 4 Intel
1.80 GHz CPUs, and 16 Gb of RAM. The time displayed is the average of 5
runs, measured using the hyperfine benchmarking tool.

5    Related Work
Given deductive verification and runtime assertion checking are two active fields
of research, the literature on these topics is quite vast. We do not aim to survey
it here. Instead, in this section we focus on verification frameworks that combine
static and dynamic analysis under the same umbrella.
    The Frama-C [20] framework provides a tool set for the certification of C
programs, based on ACSL, the ANSI/ISO-C Specification Language. On top of
ACSL, Frama-C features a modular architecture based on plugins [33]. Each of
such plugins implements a different analysis strategy. The E-ACSL plugin [34]
establishes an executable subset for ACSL, hence it can be used to perform
runtime assertion checking on C programs. Similar to Frama-C, one can cite
OpenJML [9], based on JML (the Java Modeling Language), and SPARK for the
Ada programming language. Unlike ACSL, however, JML and SPARK impose
specifications to always be executable. The three mentioned analysis frameworks
target only imperative languages, whereas the Gospel ecosystem is concerned
with the verification of programs written in OCaml, a multi-paradigm language.
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem         15

    Kosmatov et al. [21] survey static and dynamic verification within Why3,
Frama-C and SPARK 2014. Both Frama-C and SPARK conduct deductive veri-
fication by translating an input program, written either in C or Ada, into an
equivalent WhyML program. In the case of deductive verification using Gospel
specification, we use Cameleer to conduct deductive verification via Why3, but
we can also interface with Coq, via CFML, when one needs to use Separation
Logic to conduct some proof. Finally, the authors also describe the use of coun-
terexamples, either generated by SMT solvers or via testing, to debug proof
failures. Adding support for the generation of counterexamples, expressed as
Gospel terms, would be an interesting addition to the ecosystem.
    Achieving full combination of static and dynamic analyses is known to be an
important challenge in the field of formal methods [23]. Different specification
styles, targeting different back-end tools (e.g., automated solvers, interactive
proof assistants, or execution monitors), and the question of how to make the
two analyses agree on a common semantics, makes it a non-trivial task to read-
ily combine the two approaches. To this regards, Maurica et al. [24] survey the
architecture and design choices of Frama-C and OpenJML towards approximat-
ing runtime assertion checking capabilities to those of static verification. Within
the Gospel ecosystem, one of our major goals is to bridge the gap between Or-
tac and the deductive verification tools. For instance, we aim at improving the
expressiveness of supported executable Gospel subset (e.g., quantification) and
incorporating memory analysis techniques, based on Separation Logic [28].


6   Conclusions and Future Work

In this paper, we reported on our experience using dynamic and static analy-
sis tools to, collaboratively and incrementally, tackle the verification of OCaml
code. In our certification pipeline, we first apply Ortac, via the QCheck-STM plu-
gin, to perform property-based state-machine testing of parts of the program.
Then, Cameleer and CFML are used to deductively verify OCaml implementa-
tions, hence complementing the correctness guarantees provided by the RAC
step. However, while conducting the proof, one can rely on the dynamically ana-
lyzed specification to use, for instance, as the logical behaviour of auxiliary data
structures. We demonstrate how this pipeline works in practice, by applying it
to an OCaml implementation of a path checking algorithm in a graph.
    We use Gospel, the OCaml specification language, as the key ingredient to
achieve collaboration between the two analysis approaches. Gospel is not tied
to any particular tool or even verification methodology, hence it is used as a
common ground for RAC and deductive verification of parts of the same piece
of OCaml code. We believe our proposal for the combined use of analysis tools,
based on user-supplied Gospel specifications, is an important contribution to-
wards a wider adoption of formal methods by the OCaml community. To inte-
grate well with common development cycles and be applicable to the verification
of industrial-scale systems, a certification workflow should be flexible enough and
offer different levels of assurance. It is our goal to keep improving our method-
16      Tiago Lopes Soares, Ion Chirica, and Mário Pereira

ology and tools to analyze more realistic, industrial-size OCaml case studies. We
conclude with other avenues of future work that we believe are worth to explore.

Differences between specification for RAC and Deductive Verification. As pre-
sented throughout the paper, Ortac imposes a particular style for writing Gospel
specification that makes such a specification less natural when compared to what
one writes for a proof. Even if we argue, informally, that the two sorts of specifica-
tion are logically equivalent, it would be interesting to derive a formal argument
of such relationship. One possibility would be to generate a proof script stating
specification inclusion between Gospel statements used in Ortac and those used
in Cameleer or CFML.

RAC when deductive verification fails. In our methodology, when doing a proof,
we rely upon a Gospel specification that has been tested in Ortac. We showcase
this approach in our example of the path checking algorithm, where the Cameleer
proof is conducted against the Queue and Hashtbl specifications checked by
Ortac. As such, we explore the results of dynamic analysis during the static
phase. Allowing for the opposite direction, i.e., going from deductive verification
into RAC, would also be of interest. One possibility is to apply RAC tools when
a proof does not succeed. For instance, when one fails to prove a loop invariant
it could generate an executable version of such an invariant (a monitor ) to
dynamically analyze it. The SPARK 2014 toolset [25] is a successful example of
this approach. In the case of the Gospel ecosystem, we would likely need to extend
Ortac to deal not only with OCaml interfaces, but also with implementation files.


Acknowledgments. We thank Ana Ribeiro for her support in designing Fig-
ures 2 and 4. We thank the ISoLA 2024 anonymous reviewers. Their comments
and suggestions have greatly improved the presentation of this paper. This work
is partly supported by Agence Nationale de la Recherche (ANR) grant ANR-22-
CE48-0013-01 (GOSPEL) and NOVA LINCS ref. UIDB/04516/2020 (https:
//doi.org/10.54499/UIDB/04516/2020) and ref. UIDP/04516/2020 (https:
//doi.org/10.54499/UIDP/04516/2020) with the financial support of FCT.IP.


References

 1. Baudin, P., Cuoq, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto, V.:
    ACSL: ANSI/ISO C Specification Language, version 1.20 (2024), http://frama-c.
    com/download/acsl.pdf
 2. Bobot, F., Filliâtre, J.C., Marché, C., Paskevich, A.: Why3: Shepherd your herd of
    provers. Boogie 2011: First International Workshop on Intermediate Verification
    Languages (05 2012)
 3. Carré, B., Garnsworthy, J.R.: SPARK - An Annotated Ada Subset for Safety-
    critical Programming. In: Jr., C.B.E. (ed.) Proceedings of the conference on TRI-
    ADA 1990, TRI-Ada 1990, Baltimore, Maryland, USA, December 3-6, 1990. pp.
    392–402. ACM (1990), https://doi.org/10.1145/255471.255563
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem            17

 4. Charguéraud, A.: Characteristic Formulae For The Verification Of Imperative Pro-
    grams. SIGPLAN Not. 46(9), 418–430 (sep 2011), https://doi.org/10.1145/
    2034574.2034828
 5. Charguéraud, A.: Separation Logic for Sequential Programs (Functional Pearl).
    Proc. ACM Program. Lang. 4(ICFP) (aug 2020), https://doi.org/10.1145/
    3408998
 6. Charguéraud, A., Filliâtre, J., Lourenço, C., Pereira, M.: GOSPEL — Providing
    OCaml with a Formal Specification Language. In: Formal Methods - The Next 30
    Years - Third World Congress. Lecture Notes in Computer Science, vol. 11800, pp.
    484–501. Springer (2019), 10.1007/978-3-030-30942-8_29
 7. Claessen, K., Hughes, J.: QuickCheck: A Lightweight Tool For Random Testing
    Of Haskell Programs. In: Odersky, M., Wadler, P. (eds.) Proceedings of the Fifth
    ACM SIGPLAN International Conference on Functional Programming (ICFP ’00),
    Montreal, Canada, September 18-21, 2000. pp. 268–279. ACM (2000), https://
    doi.org/10.1145/351240.351266
 8. Clarke, L.A., Rosenblum, D.S.: A Historical Perspective on Runtime Assertion
    Checking in Software Development. SIGSOFT Softw. Eng. Notes 31(3), 25–37
    (may 2006), https://doi.org/10.1145/1127878.1127900
 9. Cok, D.R.: JML OpenJML for Java 16. In: Cok, D.R. (ed.) FTfJP 2021: Proceed-
    ings of the 23rd ACM International Workshop on Formal Techniques for Java-
    like Programs, Virtual Event, Denmark, 13 July 2021. pp. 65–67. ACM (2021),
    https://doi.org/10.1145/3464971.3468417
10. Conchon, S., Filliâtre, J.C., Signoles, J.: Designing a Generic Graph Library Using
    ML Functors (04 2007)
11. Cruanes, S., Rudi, G., Deplaix, J.P., Midtgaard, J., Chaboche, V.: Qcheck. Github
    Repository: https://github.com/c-cube/qcheck/ (2023)
12. Dailler, S., Marché, C., Moy, Y.: Lightweight interactive proving inside an auto-
    matic program verifier. In: Masci, P., Monahan, R., Prevosto, V. (eds.) Proceed-
    ings 4th Workshop on Formal Integrated Development Environment, F-IDE@FLoC
    2018, Oxford, England, 14 July 2018. EPTCS, vol. 284, pp. 1–15 (2018), https:
    //doi.org/10.4204/EPTCS.284.1
13. Filliâtre, J.C.: Deductive Software Verification. International Journal on Soft-
    ware Tools for Technology Transfer (STTT) 13(5), 397–403 (Aug 2011), 10.1007/
    s10009-011-0211-0
14. Filliâtre, J., Gondelman, L., Paskevich, A.: The Spirit of Ghost Code. For-
    mal Methods Syst. Des. 48(3), 152–174 (2016), https://doi.org/10.1007/
    s10703-016-0243-x
15. Filliâtre, J., Pascutto, C.: Ortac: Runtime Assertion Checking for OCaml (Tool
    Paper). In: Feng, L., Fisman, D. (eds.) Runtime Verification - 21st International
    Conference, RV 2021, Virtual Event, October 11-14, 2021, Proceedings. Lecture
    Notes in Computer Science, vol. 12974, pp. 244–253. Springer (2021), https://
    doi.org/10.1007/978-3-030-88494-9_13
16. Filliâtre, Jean-Christophe and Gondelman, Léon and Paskevich, Andrei: A Prag-
    matic Type System for Deductive Verification. Tech. rep., Université Paris-Sud
    (2016)
17. Hatcliff, J., Leavens, G.T., Leino, K.R.M., Müller, P., Parkinson, M.J.: Behavioral
    Interface Specification Languages. ACM Comput. Surv. 44(3), 16:1–16:58 (2012),
    https://doi.org/10.1145/2187671.2187678
18. Iguernelala, M.: Strengthening the Heart of an SMT-Solver: Design and Implemen-
    tation of Efficient Decision Procedures. Thèse de doctorat, Université Paris-Sud
    (Jun 2013)
18      Tiago Lopes Soares, Ion Chirica, and Mário Pereira

19. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.:
    VeriFast: A Powerful, Sound, Predictable, Fast Verifier for C and Java. In: Bobaru,
    M., Havelund, K., Holzmann, G.J., Joshi, R. (eds.) NASA Formal Methods. pp.
    41–55. Springer Berlin Heidelberg, Berlin, Heidelberg (2011). https://doi.org/
    10.1007/978-3-642-20398-5_4
20. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    A Software Analysis Perspective. Formal Aspects Comput. 27(3), 573–609 (2015),
    https://doi.org/10.1007/s00165-014-0326-7
21. Kosmatov, N., Marché, C., Moy, Y., Signoles, J.: Static versus Dynamic Verification
    in Why3, Frama-C and SPARK 2014. In: Margaria, T., Steffen, B. (eds.) Lever-
    aging Applications of Formal Methods, Verification and Validation: Foundational
    Techniques - 7th International Symposium, ISoLA 2016, Imperial, Corfu, Greece,
    October 10-14, 2016, Proceedings, Part I. Lecture Notes in Computer Science,
    vol. 9952, pp. 461–478 (2016), https://doi.org/10.1007/978-3-319-47166-2_32
22. Leavens, G.T., Baker, A.L., Ruby, C.: Preliminary Design of JML: A Behavioral
    Interface Specification Language for java. ACM SIGSOFT Softw. Eng. Notes 31(3),
    1–38 (2006), https://doi.org/10.1145/1127878.1127884
23. Leavens, G.T., Cheon, Y., Clifton, C., Ruby, C., Cok, D.R.: How the Design
    of JML Accomodates Both Runtime Assertion Checking and Formal Verifica-
    tion. In: de Boer, F.S., Bonsangue, M.M., Graf, S., de Roever, W.P. (eds.)
    Formal Methods for Components and Objects, First International Symposium,
    FMCO 2002, Leiden, The Netherlands, November 5-8, 2002, Revised Lectures.
    Lecture Notes in Computer Science, vol. 2852, pp. 262–284. Springer (2002),
    https://doi.org/10.1007/978-3-540-39656-7_11
24. Maurica, F., Cok, D.R., Signoles, J.: Runtime Assertion Checking and Static Ver-
    ification: Collaborative Partners. In: Margaria, T., Steffen, B. (eds.) Leveraging
    Applications of Formal Methods, Verification and Validation. Verification - 8th
    International Symposium, ISoLA 2018, Limassol, Cyprus, November 5-9, 2018,
    Proceedings, Part II. Lecture Notes in Computer Science, vol. 11245, pp. 75–91.
    Springer (2018), https://doi.org/10.1007/978-3-030-03421-4_6
25. McCormick, J.W., Chapin, P.C.: Building High Integrity Applications with
    SPARK. Cambridge University Press (2015)
26. Midtgaard, J., Nicole, O., Osborne, N.: Multicoretests-Parallel Testing Libraries
    for OCaml 5.0. In: Ocaml Users Developers Workshop 2022 (2022)
27. Müller, P., Schwerhoff, M., Summers, A.: Viper: A Verification Infrastructure for
    Permission-Based Reasoning, pp. 104–125 (01 2017). https://doi.org/10.3233/
    978-1-61499-810-5-104
28. Nguyen, H.H., Kuncak, V., Chin, W.N.: Runtime Checking for Separation Logic.
    In: Logozzo, F., Peled, D.A., Zuck, L.D. (eds.) Verification, Model Checking, and
    Abstract Interpretation. pp. 203–217. Springer Berlin Heidelberg, Berlin, Heidel-
    berg (2008)
29. Paulin-Mohring, C.: Introduction to the Coq Proof-Assistant for Practical Soft-
    ware Verification, pp. 45–95. Springer Berlin Heidelberg, Berlin, Heidelberg (2012),
    https://doi.org/10.1007/978-3-642-35746-6_3
30. Pereira, M., Ravara, A.: Cameleer: A Deductive Verification Tool for OCaml. In:
    Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification - 33rd International
    Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part II. Lec-
    ture Notes in Computer Science, vol. 12760, pp. 677–689. Springer (2021)
31. Pottier, F.: Verifying a Hash Table and Its Iterators in Higher-Order Separation
    Logic. In: Bertot, Y., Vafeiadis, V. (eds.) Proceedings of the 6th ACM SIGPLAN
 Static and Dynamic Verification of OCaml Programs: The Gospel Ecosystem            19

    Conference on Certified Programs and Proofs, CPP 2017, Paris, France, January
    16-17, 2017. pp. 3–16. ACM (2017), https://doi.org/10.1145/3018610.3018624
32. Pottier, F.: Strong Automated Testing of OCaml Libraries. In: JFLA 2021-32es
    Journées Francophones des Langages Applicatifs (2021)
33. Signoles, J.: Software Architecture of Code Analysis Frameworks Matters: The
    Frama-C Example. In: Dubois, C., Masci, P., Méry, D. (eds.) Proceedings Second
    International Workshop on Formal Integrated Development Environment, F-IDE
    2015, Oslo, Norway, June 22, 2015. EPTCS, vol. 187, pp. 86–96 (2015), https:
    //doi.org/10.4204/EPTCS.187.7
34. Signoles, J., Kosmatov, N., Vorobyov, K.: E-ACSL, a Runtime Verification Tool
    for Safety and Security of C Programs (Tool Paper). In: Reger, G., Havelund,
    K. (eds.) RV-CuBES 2017. An International Workshop on Competitions, Usabil-
    ity, Benchmarks, Evaluation, and Standardisation for Runtime Verification Tools,
    September 15, 2017, Seattle, WA, USA. Kalpa Publications in Computing, vol. 3,
    pp. 164–173. EasyChair (2017), https://doi.org/10.29007/fpdh
35. Soares, T., Chirica, I., Pereira, M.: Static and Dynamic Verification of OCaml Pro-
    grams: The Gospel Ecosystem. https://mariojppereira.github.io/isola2024_
    artifact.html (2024), Companion artifact
20       Tiago Lopes Soares, Ion Chirica, and Mário Pereira

A      COMPARABLE Module Signature

     module type COMPARABLE = sig                                     OCaml
       type t
       val compare : t → t → int
       val hash : t → int
       val equal : t → t → bool
     end

B      Queue Specification for Ortac

type α t                                                      Gospel + OCaml
(*@ mutable model elems : α list *)

val create : unit → α t
(*@ t = create ()
    ensures t.elems = [] *)

val is_empty : α t → bool
(*@ b = is_empty t
    ensures b = t.elems = [] *)

val push : α → α t → unit
(*@ push x t
    modifies t.elems
    ensures t.elems = (old t.elems) @ [x] *)

exception Empty

val pop : α t → α
(*@ x = pop t
    modifies t.elems
    ensures t.elems = if old t.elems = []
                         then []
                         else List.tl (old t.elems)
    ensures if old t.elems = [] then false
            else x = List.hd (old t.elems)
    raises Empty → old t.elems = [] = t.elems *)
