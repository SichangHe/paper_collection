                                         A HAT Trick: Automatically Verifying Representation
                                         Invariants Using Symbolic Finite Automata
arXiv:2404.01484v2 [cs.PL] 26 Sep 2024




                                         ZHE ZHOU, Purdue University, USA
                                         QIANCHUAN YE, Purdue University, USA
                                         BENJAMIN DELAWARE, Purdue University, USA
                                         SURESH JAGANNATHAN, Purdue University, USA
                                         Functional programs typically interact with stateful libraries that hide state behind typed abstractions. One
                                         particularly important class of applications are data structure implementations that rely on such libraries to
                                         provide a level of eﬃciency and scalability that may be otherwise diﬃcult to achieve. However, because the
                                         speciﬁcations of the methods provided by these libraries are necessarily general and rarely specialized to the
                                         needs of any speciﬁc client, any required application-level invariants must often be expressed in terms of
                                         additional constraints on the (often) opaque state maintained by the library.
                                            In this paper, we consider the speciﬁcation and veriﬁcation of such representation invariants using sym-
                                         bolic ﬁnite automata (SFA). We show that SFAs can be used to succinctly and precisely capture ﬁne-grained
                                         temporal and data-dependent histories of interactions between functional clients and stateful libraries. To
                                         facilitate modular and compositional reasoning, we integrate SFAs into a reﬁnement type system to qualify
                                         stateful computations resulting from such interactions. The particular instantiation we consider, Hoare Au-
                                         tomata Types (HATs), allows us to both specify and automatically type-check the representation invariants
                                         of a datatype, even when its implementation depends on stateful library methods that operate over hidden
                                         state.
                                            We also develop a new bidirectional type checking algorithm that implements an eﬃcient subtyping inclu-
                                         sion check over HATs, enabling their translation into a form amenable for SMT-based automated veriﬁcation.
                                         We present extensive experimental results on an implementation of this algorithm that demonstrates the fea-
                                         sibility of type-checking complex and sophisticated HAT-speciﬁed OCaml data structure implementations
                                         layered on top of stateful library APIs.
                                         CCS Concepts: • Theory of computation → Automated reasoning; Modal and temporal logics; • Soft-
                                         ware and its engineering → Language types; Software veriﬁcation and validation.
                                         Additional Key Words and Phrases: reﬁnement types, symbolic ﬁnite automata, representation invariants
                                         ACM Reference Format:
                                         Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan. 2018. A HAT Trick: Automatically
                                         Verifying Representation Invariants Using Symbolic Finite Automata. 1, 1 (September 2018), 41 pages. https://doi.org/XXXX

                                         1   INTRODUCTION
                                            Functional programs often interact with stateful libraries that hide internal state behind their
                                         APIs. Such libraries are a vital component of a programming language’s ecosystem, providing
                                         well-tested implementations of databases, key-value stores, logging and system services, and other
                                         stateful abstractions. A common use case for how these libraries are used is for programmers to
                                         Authors’ addresses: Zhe Zhou, Purdue University, USA; Qianchuan Ye, Purdue University, USA; Benjamin Delaware, Pur-
                                         due University, USA; Suresh Jagannathan, Purdue University, USA.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                         the full citation on the ﬁrst page. Copyrights for components of this work owned by others than ACM must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior speciﬁc permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2018 ACM.
                                         ACM XXXX-XXXX/2018/9-ART
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                            , Vol. 1, No. 1, Article . Publication date: September 2018.
2                                                  Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


build higher-level data structures on top of the abstractions they provide [Charguéraud et al. 2017].
A set abstract data type (ADT) equipped with intersection and cardinality operations, for example,
might use the aforementioned key-value library to maintain a persistent collection of its elements
by associating those elements (represented as values) with unique ids (their associated keys). Since
the internal state of the underlying stateful library is opaque to its clients, the implementations
of these higher-level modules will necessarily be expressed in terms of the operations provided
by the library: the methods of the set ADT might use methods like put and get to interact with
the backing key-value store, for example. To maximize reusability, these low-level libraries are
typically quite permissive in how client may use them, resulting in weak speciﬁcations that only
describe simple algebraic or equational constraints. For example, the speciﬁcation of the key-value
store might state that two put operations over distinct keys commute or that a get operation on a
key always returns the last value put in that key.
   In contrast, the higher-level abstractions provided by clients built on top of these libraries are
equipped with stronger guarantees: for example, the operations of our set ADT need to respect the
semantics of mathematical sets, for example, so that ∀𝐴 𝐵 : Set.t. |𝐴 ∪ 𝐵| + |𝐴 ∩ 𝐵| = |𝐴| + |𝐵|. Veri-
fying such semantically rich properties typically requires a strong guarantee that the internal state
of the set library is consistent with the abstract states of the datatype, i.e., the ADT implementation
should be equipped with a representation invariant [Malik et al. 2007; Miltner et al. 2020]. Ensuring
that distinct keys are always associated with distinct values allows us to prove the above relation-
ship between the intersection and cardinality operations of the set ADT, for example. Establishing
such an invariant is complicated by the fact that our set ADT is built on top of another library
with an opaque internal state, and whose weak speciﬁcations do not directly address the notion
of uniqueness central to the set ADT. This paper presents an automated type-based veriﬁcation
procedure that addresses these complications.
   Our proposed solution augments a reﬁnement type system for a call-by-value functional core
language that supports calls to stateful libraries, with Hoare Automata Types (HATs). HATs are a
new type abstraction that qualiﬁes basic types with pre- and post-conditions expressed as symbolic
ﬁnite-state automata [Veanes 2013; Veanes et al. 2010], a generalization of ﬁnite-state automata
equipped with an unbounded alphabet, and whose transitions are augmented with predicates over
the elements of this alphabet. HATs serve as a compact representation of the trace of stateful API
calls and returns made prior to a function invocation and those performed during its execution. As
a result, HATs serve as an expressive basis for a ﬁne-grained eﬀect system within a general reﬁne-
ment type framework, enabling compositional reasoning about invocations of stateful APIs in a
form amenable to automated veriﬁcation of a client module’s representation invariant. For exam-
ple, he representation invariant from our set ADT is captured by the following symbolic automaton,
written using a variant of linear temporal logic on ﬁnite sequences [De Giacomo and Vardi 2013].
The base predicates of this formula describe events, or invocations of the methods of a key-value
store whose values are drawn from a setElem type:
                  𝐼 Set (el)  (hput key val = 𝜈 | val = eli =⇒      ¬♦hput key val = 𝜈 | val = eli)
This representation invariant (𝐼 Set ) is expressed using standard temporal logic modalities (e.g., 
(always), (next), and ♦ (eventually)) to express the history of valid interactions between the set
implementation and the underlying key-value store that ensure the expected element uniqueness
property holds. Informally, the invariant establishes that, at every step of the execution ((...) ),
once a value el has been inserted into the set ( hput key val = 𝜈 | val = eli ), it will never be reinserted
( ¬♦hput key val = 𝜈 | val = eli ). An implementation that preserves this invariant guarantees that
every value is always associated with at most one key.
   To verify it, we can check the insert method of the set ADT against the following type
                 𝜏insert  el:setElem d x:{𝜈:setElem | ⊤}  [𝐼 Set (el)] {𝜈:unit | ⊤} [𝐼 Set (el)]


, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                          3


The output type of 𝜏insert ([𝐼 Set (el)] {𝜈:unit | ⊤} [𝐼 Set (el)]) is a Hoare Automata Type (HAT) over
the representation invariant 𝐼 Set . This type captures the behavior required of any correct implemen-
tation of insert: assuming the invariant holds for any value el (encoded here as a ghost variable
scoped using d ) prior to the insertion of a new element x, it must also hold after the insertion as
well. The precondition of the HAT captures the set of interactions that lead to a valid underlying
representation state (namely, one in which every value in the store is unique), and the postcondi-
tion of the HAT speciﬁes that this condition remains valid even after executing insert.
   Our use of HATs diﬀers in important ways from other type-based veriﬁcation approaches for
functional programs that allow computations to perform ﬁne-grained eﬀects, such as F* [Swamy et al.
2023] or Ynot [Nanevski et al. 2008b]. These systems use the power of rich dependent types to spec-
ify ﬁne-grained changes to the heap induced by an stateful operation. The Dijkstra monad [Maillard et al.
2019; Swamy et al. 2013] used by F*, for example, extends ideas ﬁrst proposed by Nanevski et.
al [Nanevski et al. 2008a] in their development of Hoare Type Theory to embed a weakest precon-
dition predicate transformer semantics into a type system that can be used to generate veriﬁcation
conditions consistent with a provided post-condition on the program heap. In contrast, our setting
assumes that such operations are executed by a library with a hidden state, requiring the client’s
representation invariant to be expressed solely in terms of observations on calls (and returns) to
(and from) the methods of the underlying library.
   Our approach also bears some similarity to recent (reﬁnement) type and eﬀect systems for
verifying temporal properties of event traces produced during a computation [Nanjo et al. 2018;
Sekiyama and Unno 2023]. While the idea of using symbolic traces of previous observations as a
handle to reason about the hidden state of a library is similar to these other eﬀorts, incorporating
return values of operations as part of such traces is a signiﬁcant point of diﬀerence. This capability,
critical for the validation of useful representation invariants, allows the precondition encoded in a
HAT to describe a ﬁne-grained context of events in which a program can run, expressed in terms of
both library method arguments and return values. These important diﬀerences with prior work po-
sition HATs as a novel middle-ground in the design space between explicit state-based veriﬁcation
techniques and trace-based eﬀect systems. Our formulation also leads to a number of signiﬁcant
technical diﬀerences with other reﬁnement type systems [Jhala and Vazou 2021] and their asso-
ciated typing algorithms, since we must now contend with type-level reasoning over symbolic
automata qualiﬁers.
   In summary, this paper makes the following contributions:
  (1) We formalize a new trace-based speciﬁcation framework for expressing representation in-
      variants of functional clients of stateful libraries that manage hidden state.
  (2) We show how this framework can be embedded within a compositional and ﬁne-grained
      eﬀect-tracking reﬁnement type system, by encoding speciﬁcations as symbolic automata
      and instantiated as HATs in the type system.
  (3) We develop a bidirectional type-checking algorithm that translates the declarative type sys-
      tem into eﬃcient subtype inclusion checks amenable to SMT-based automated veriﬁcation.
  (4) Using a tool (Marple) that implements these ideas, we present a detailed evaluation study
      over a diverse set of non-trivial OCaml datatype implementations that interact with stateful
      libraries. To the best of our knowledge, Marple is the ﬁrst system capable of automated
      veriﬁcation of sophisticated representation invariants for realistic OCaml programs.
The remainder of this paper is organized as follows. In the next section, we provide further motiva-
tion for the problem by developing a running example, which is used in the rest of the paper. Sec. 3
introduces a core functional language equipped with operators that model stateful library meth-
ods. Sec. 4 presents a reﬁnement type system that augments basic type qualiﬁers to also include

                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
4                                                  Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan

module type Bytes = sig
  type t                                            1 module FileSystem = struct
  ...                                               2    open KVStore
end                                                 3    let init () : unit = put "/" (File.init ())
                                                    4
module type Path = sig                              5    let add (path: Path.t) (bytes: Bytes.t): bool =
  type t = string                                   6      if exists path then false
  val parent: t -> t                                7      else
  val isRoot: t -> bool                             8        let parent_path = Path.parent path in
  ...                                               9        if not (exists parent_path) then false
end                                                10        else
                                                   11          let bytes' = get parent_path in
module type File = sig                             12          if File.isDir bytes' then (
  val init: unit -> Bytes.t                        13             put path bytes;
  val isDir: Bytes.t -> bool                       14             put parent_path (File.addChild bytes' path);
  val isFile: Bytes.t -> bool                      15             true)
  val isDel: Bytes.t -> bool                       16          else false
  val setDeleted: Bytes.t -> Bytes.t               17
  val delChild:                                    18   let delete (path : Path.t): bool =
    Bytes.t -> Path.t -> Bytes.t                   19     if (isRoot path) or not (exists path) then false
  val addChild:                                    20     else (
    Bytes.t -> Path.t -> Bytes.t                   21       let bytes = get path in
  ...                                              22       if File.isDir bytes then deleteChildren(path);
end                                                23       let parent_path = Path.parent path in
                                                   24       let bytes' = get parent_path in
module type KVStore = sig                          25       put path (File.setDeleted bytes);
  val put: Path.t -> Bytes.t -> unit               26       put parent_path (File.delChild bytes' path);
  val exists: Path.t -> bool                       27       true)
  val get: Path.t -> Bytes.t                       28 end
end

                    Fig. 1. A file system datatype based on underline key-value store library.



HATs; a brief background on symbolic automata is also given. An eﬃcient bidirectional typing
algorithm is then presented in Sec. 5. Implementation details, as well as experimental results on
its eﬀectiveness in automatically verifying the representation invariants of a number of realistic
data structure client programs that interact with stateful libraries is provided in Sec. 6. The paper
ends with a discussion of related work and conclusions.

2   MOTIVATION
   To further motive our approach, consider the (highly-simpliﬁed) Unix-like ﬁle-system directory
abstraction (FileSystem) shown in Fig. 1. This module is built on top of other libraries that maintain
byte arrays (Bytes.t) which hold a ﬁle or a directory’s contents and metadata, and which manip-
ulate paths (Path.t), strings that represent fully-elaborated ﬁle and directory names. FileSystem’s
implementation also uses an underlying key-value store library (KVStore) to provide a persistent
and scalable storage abstraction, where keys represent ﬁle paths and values are byte arrays. The in-
terface to this store is deﬁned by three stateful library methods: put persistently stores a key-value
pair h 𝑘, 𝑣 i , adding the pair to the store if 𝑘 does not already exist, and overwriting its old value
with 𝑣 if it does; exists returns true if the given key has been previously put and false otherwise;
and, get returns the value associated with its key argument, and fails (i.e., raises an exception) if
the key does not exist in the store.

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                          5


    Fig. 1 shows three of the methods provided by FileSystem: init initializes the ﬁle system by
storing a root path (“/”); add allows users to add regular ﬁles or directories to the ﬁlesystem; and,
delete logically removes ﬁles or directories from the ﬁlesystem. The latter two operations return a
Boolean value to indicate whether they were successful. The add operation succeeds (line 15) only
if (a) the given path does not already exist in the ﬁle system (line 6) and (b) a path representing the
parent directory for the ﬁle does exist (line 9). Besides adding the ﬁle (line 13), add also updates the
contents of the parent directory to make it aware that a new child has been added (line 14). Similar
to add, delete requires that the supplied path exists and is not the root (line 19). If the path cor-
responds to a directory, its children are marked deleted (line 22) using procedure deleteChildren
(not shown). Additionally, the directory’s metadata, and that of its parent, are updated to record
the deletion (lines 25 and 26). Implicit in delete’s implementation is the assumption that the parent
path of the ﬁle to be deleted exists in the store: observe that there is no check to validate the exis-
tence of this path before the get of the parent’s contents is performed on line 24. This assumption
can be framed as a representation invariant that must hold prior to and after every call and return
of add and delete. Intuitively, this invariant captures the following property:
   Invariant𝐹 𝑆 : Any path that is stored as a key in the key-value store (other than the root path) must
also have its parent stored as a non-deleted directory in the store.

   Representation Invariants. In a language that guarantees proper data abstraction, library devel-
opers can safely assume that any guarantees about an API established using a representation in-
variant are independent of a particular client’s usage. However, as we noted earlier, numerous
challenges arise when validating a representation invariant in our setting because we can only
characterize the state of the underlying library in terms of its admissible sequence of interactions
with the client. In our example, this characterization must be able to capture the structure of a valid
ﬁlesystem, in terms of sequences of put, get, and exists calls and returns that are suﬃcient to ensure
that the invariant is preserved. Verifying that Invariant𝐹 𝑆 holds requires us to prove that, except
for the root, the path associated with a ﬁle or directory can only be recorded in the store when
its parent path exists, i.e., its parent has previously been put and has not yet been deleted. Estab-
lishing that this property holds involves reasoning over both data dependencies among ﬁlesystem
calls and temporal dependencies among store operations.

   Events, Traces, and Symbolic Finite Automata. We address these challenges by encoding desired
sets of stateful interactions between the client and library as symbolic ﬁnite automata (SFA). Be-
sides constants and program variables, the alphabet of an automaton that captures these inter-
actions includes a set of stateful operators op (e.g., put and get). The language recognized by an
automaton speciﬁes the sequences of permitted library method invocations. Each such invocation
(called an event) op 𝑣𝑖 = 𝑣 records the operator invoked (op), a list of its arguments (𝑣𝑖 ), and a single
result value 𝑣 . It is critical that we record both inputs and outputs of an operation, in order to en-
able our type system to distinguish among diﬀerent hidden library states. Consider, for example,
a stateful library initialization operator initialize : unit  bool. The hidden state after observing
“initialize () = true”, representing a successful initialization action, is likely to be diﬀerent from the
hidden state that exists after observing the event “initialize () = false”, which indicates an initial-
ization error. The language accepted by an SFA is a potentially inﬁnite set of ﬁnite sequences of
events, or traces.

  Example 2.1 (Traces). In contrast to the correct implementation of add shown in Fig. 1, consider
the following incorrect version:
              let addbad (path: Path.t) (bytes: Bytes.t) = put path bytes

                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
6                                                  Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


This implementation simply records a path without considering whether its parent exists. We
assume the ﬁle system initially contains only the root path, “/”, which is put when the ﬁle system
is created by the method init. The traces 𝛼 1 and 𝛼 2 , shown below, represent executions of these
two implementations that reﬂect their diﬀerences:
      under context trace 𝛼 0  [put “/” bytesDir = () ]
    addbad “/a/b.txt” bytesFile yields 𝛼 1  [put “/” bytesDir = (); put “/a/b.txt” bytesFile = () ]
       add “/a/b.txt” bytesFile yields 𝛼 2  [put “/” bytesDir = (); exists “/a/b.txt” = false; exists “/a” = false]
where bytesDir and bytesFile represent the contents of a directory and a regular ﬁle, resp. The
trace 𝛼 1 violates Invariant𝐹 𝑆 since it registers the path “/a/b.txt” in the ﬁle system even though the
parent path (“/a”) does not exist. Thus, performing the operation delete “/a/b.txt” after executing
the actions in this trace will cause a runtime error when it attempts to perform a get operation
on the parent path “/a”. On the other hand, executing this operation after executing the actions in
trace 𝛼 2 terminates normally and preserves Invariant𝐹 𝑆 .
  Example 2.2 (Symbolic Finite Automata). We express symbolic automata as formulae in a sym-
bolic version of linear temporal logic on ﬁnite sequences [De Giacomo and Vardi 2013]. Invariant𝐹 𝑆
can be precisely expressed in this language as the following formula (denoted 𝐼 FS (p) ) parameterized
over a path p:
                   𝐼 FS (p)  hisRoot(p)i ∨ (𝑃isFile (p) ∨ 𝑃isDir (p) =⇒ 𝑃isDir (parent(p)))
where
𝑃 isDir (p)  ♦(hput key val = 𝜈 | key = p ∧ isDir(val ) i ∧     ¬hput key val = 𝜈 | key = p ∧ (isDel (val ) ∨ isFile (val ) ) i )
𝑃 isFile (p)  ♦(hput key val = 𝜈 | key = p ∧ isFile(val ) i ∧     ¬hput key val = 𝜈 | key = p ∧ (isDel (val ) ∨ isDir(val ) ) i )
Here, isRoot, isDir, isFile , and parent are pure functions on paths and bytes. The invariant is
comprised of two disjunctions involving p:
   (1) hisRoot(p)i asserts that p is the ﬁlesystem root and is always a valid path, regardless of any
       other actions that have been performed on the underlying key-value store.
   (2) 𝑃isFile (p) ∨ 𝑃isDir (p) =⇒ 𝑃isDir (parent(p)) asserts that if p corresponds to either a ﬁle or di-
       rectory in the ﬁle system, then its parent path must also correspond to a directory in the ﬁle
       system. The predicate 𝑃isDir (p) captures contexts in which p has been registered as a direc-
       tory and then not subsequently deleted or replaced by a ﬁle (i.e., ¬hput key val = 𝜈 | key =
       p ∧ (isDel(val) ∨ isFile(val))i ). The predicate (𝑃isFile (p) ) is deﬁned similarly except that
       it requires that an existing ﬁle not be deleted or modiﬁed to become a directory. Observe
       that atomic predicates (e.g., hput key val = 𝜈 | key = p ∧ isFile(val)i ) not only capture when an
       event has been induced by a library operator (e.g., put), but also qualify the arguments to
       that operator and the result it produced (e.g., the argument key must be equal to the path p).1
This speciﬁcation of the representation invariant 𝐼 FS (p) thus formalizes our informal characteriza-
tion of a correct ﬁle system, Invariant𝐹 𝑆 . The two subformulas capture the property that any path
recorded as a key in the key-value store, other than the root, must have a parent directory. Notably,
this speciﬁcation is deﬁned purely by constraining the sequence of put operations allowed on the
store and does not require any knowledge of the store’s underlying representation.
  Hoare Automata Types. While SFAs provide a convenient language in which to encode repre-
sentation invariants, it is not immediately apparent how they can help with veriﬁcation since, by
themselves, they do not impose any safety constraints on expressions. To connect SFAs to com-
putations, we embed them as reﬁnements in a reﬁnement type (and eﬀect) system. In a standard
reﬁnement type system, the reﬁnement type {𝜈:𝑏 | 𝜙} of an expression 𝑒 uses a qualiﬁer 𝜙 to reﬁne
1 Throughout this paper, we italicize event arguments.



, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                    7


                             Variables                 𝑥, 𝑦, 𝑧, 𝑓 , 𝜈, ...
                    Pure Operations 𝑜𝑝 ::= + | − | == | < | ≤ | mod | parent | ...
              Eﬀectful Operations            op ::= put | exists | get | insert | mem | ...
                  Data constructors           𝑑 ::=    () | true | false | O | S | ...
                            Constants          𝑐 ::= Z | 𝑑 (𝑐)
                                 Values        𝑣 ::= 𝑐 | 𝑥 | 𝑑 (𝑣) | 𝜆𝑥:𝑡 .𝑒 | fix𝑓 :𝑡 .𝜆𝑥:𝑡 .𝑒
     Expressions (Computations)                𝑒 ::= 𝑣 | let 𝑥 = op 𝑣 in 𝑒 | let 𝑥 = 𝑜𝑝 𝑣 in 𝑒 | let 𝑥 = 𝑣 𝑣 in 𝑒
                                                        | let 𝑥 = 𝑒 in 𝑒 | match 𝑣 with 𝑑 𝑦  𝑒

                                                  Fig. 2. 𝝀 E term syntax.


the value of 𝑒 . Similarly, a Hoare Automata Type (HAT), [𝐴] {𝜈:𝑏 | 𝜙} [𝐵], additionally reﬁnes a pure
reﬁnement type {𝜈:𝑏 | 𝜙} with two symbolic automata: a precondition automaton 𝐴 deﬁning an ef-
fect context under which 𝑒 is allowed to evaluate, and a postcondition automata 𝐵 that augments
this context with the eﬀects induced by 𝑒 as it executes. A HAT thus allows us to track the sequence
of stateful interactions between higher-level datatypes and the underlying stateful library, as well
as to record the consequences of this interaction in terms of the return values of stateful calls.
   Our type system leverages this information to verify the preservation of stated representation
invariants in terms of these interactions. For example, add and delete can be ascribed the following
HAT-enriched types:
        add : p:Path.t d path:{𝜈:Path.t | ⊤}  bytes:{𝜈:Bytes.t | ⊤}  [𝐼 FS (p)] {𝜈:bool | ⊤} [𝐼 FS (p)]                   (𝜏add )
     delete : p:Path.t d path:{𝜈:Path.t | ⊤}  [𝐼 FS (p)] {𝜈:bool | ⊤} [𝐼 FS (p)]                                        (𝜏delete )

Here, the notation “p:Path.t d ” indicates that p is a ghost variable representing an arbitrary path;
thus, the representation invariant must hold over any instantiation of p. While their input argu-
ments ({𝜈:Path.t | ⊤} and ({𝜈:Bytes.t | ⊤})) are unconstrained, the return types of these functions
are expressed as HATs in which both the precondition and postcondition automata refer to the
representation invariant for the ﬁle system, 𝐼 FS (p) . Informally, this type reads “if we invoke the
function in a context that is consistent with 𝐼 FS , then the state after the function returns should
also be consistent with 𝐼 FS ”. The traces admitted by an SFA are used to represent these contexts
and states.
   More concretely, observe that the trace 𝛼 2 from Example 2.1 is derived by concatenating 𝛼 0 with
the library calls generated during the (symbolic) execution of add:
                                𝛼 new  [exists “/a/b.txt” = false; exists “/a” = false]

(i.e., 𝛼 2 = 𝛼 0 𝛼 new ). Note that both 𝛼 0 and 𝛼 2 satisfy the representation invariant 𝐼 FS . To admit
this trace, our type system automatically infers a new automata 𝐴 that accepts the sequence of
events in 𝛼 new by type-checking add. Verifying that the representation invariant holds now reduces
to an inclusion check between two symbolic automata, requiring that the trace expected by the
concatenated automata 𝐼 FS ; 𝐴 is also accepted by the representation invariant 𝐼 FS .

3    LANGUAGE
    To formalize our approach, we ﬁrst introduce 𝝀 E , a core calculus for eﬀectful programs.2

2 Although the focus of this paper is the veriﬁcation of clients of stateful libraries, our proposed approach applies to eﬀectful

programs more generally. Our formalism reﬂects the more general setting of eﬀectful programs.


                                                                       , Vol. 1, No. 1, Article . Publication date: September 2018.
8                                                  Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan

                                              Traces 𝛼 ::=       [ ] | (op 𝑣 = 𝑣)::𝛼
                                                                                                                             𝛼
Small-Step Reduction Rules                                                                                                   →𝑒
                                                                                                                      𝛼  𝑒 ↩−
                     𝑜𝑝 𝑣 ⇓ 𝑣𝑥                                                 𝛼  op 𝑣 ⇓ 𝑣𝑥
                                                StPureOp                                                       StEffOp
                                []                                                     [op 𝑣 = 𝑣𝑥 ]
       𝛼  let 𝑥 = 𝑜𝑝 𝑣 in 𝑒 ↩−→ 𝑒 [𝑥 ↦→ 𝑣𝑥 ]                  𝛼  let 𝑥 = op 𝑣 in 𝑒 ↩−−−−−−−→ 𝑒 [𝑥 ↦→ 𝑣𝑥 ]

                              Fig. 3. Trace syntax and selected operational semantics.


   Syntax. 𝝀 E is a call-by-value lambda calculus with built-in inductive datatypes, pattern match-
ing, a set of pure and eﬀectful operators, and recursive functions. Its syntax is given in Fig. 2.
For simplicity, programs are expressed in monadic normal-form (MNF) [Hatcliﬀ and Danvy 1994],
a variant of A-Normal Form (ANF) [Flanagan et al. 1993] that permits nested let-bindings. The
terms in 𝝀 E are syntactically divided into two classes: values 𝑣 and expressions 𝑒 , where the lat-
ter include both pure terms and those that have computational eﬀects. Similar to the simply-typed
lambda calculus, function parameters have explicit type annotations. 𝝀 E is parameterized over two
sets of primitive operators: pure operators (𝑜𝑝 ) include basic arithmetic and logical operators, while
examples of eﬀectful operators (op) include state manipulating operators (e.g., put/exists/get for in-
teracting with a key-value store, or insert/mem for manipulating a stateful set library). We express
sequencing of eﬀectful computations 𝑒 1 ; 𝑒 2 in terms of let-bindings: 𝑒 1 ; 𝑒 2  let 𝑥 = 𝑒 1 in 𝑒 2 , where 𝑥
does not occur free in 𝑒 2 . The application 𝑒 1 𝑒 2 is syntactic sugar for let 𝑥 = 𝑒 1 in let 𝑦 = 𝑒 2 in let 𝑧 = 𝑥 𝑦 in 𝑧 .
   Operational Semantics. Our programming model does not have access to the underlying imple-
mentation of eﬀectful operators, so the semantics of 𝝀 E constrains the behavior of impure opera-
tions in terms of the outputs they may produce. To do so, we structure its semantics in terms of
traces that record the history of previous eﬀectful operations and their results. The syntax of traces
adopts standard list operations (i.e., cons :: and concatenation ), as shown in Fig. 3. Traces are lists
of eﬀect events op 𝑣 = 𝑣 that record the application of an eﬀectful operator op to its arguments 𝑣 as
well as the resulting value 𝑣 . The traces 𝛼 2 and 𝛼 1 from Example 2.1 record the events generated
by correct and incorrect implementations of the add function of the FileSystem ADT, for example.
                                                                                                                      𝛼′
   The operational semantics of 𝝀 E is deﬁned via a small-step reduction relation, 𝛼  𝑒 ↩−−→ 𝑒 ′ . This
relation is read as “under an eﬀect context (i.e., trace) 𝛼 , the term 𝑒 reduces to 𝑒 ′ in one step
and performs the eﬀect 𝛼 ′ ”, where 𝛼 ′ is either empty [ ] or holds a single event. The semantics
is parameterized over two auxiliary relations, 𝑒 ⇓ 𝑣 and 𝛼  𝑒 ⇓ 𝑣 , used to evaluate pure and impure
operations, respectively. Fig. 3 shows how the corresponding reduction rules use these relations.3
The reduction rule for pure operators (STPureOp) holds in an arbitrary eﬀect context (including
the empty one), and produces no additional events. The rule for eﬀectful operators (STEffOp), in
contrast, can depend on the current context 𝛼 , and records the result value of the eﬀectful operator
                                                                                𝛼′
in the event it emits. The multi-step reduction relation 𝛼  𝑒 ↩−→∗ 𝑒 ′ deﬁnes the reﬂexive, transitive
closure of the single-step relation; its trace 𝛼 records all events generated during evaluation.
  Example 3.1. We can deﬁne the semantics for the put, exists, and get operators found in a key-
value store library and used in FileSystem, via the following rules:

                   Put     put 𝑘 𝑣 = () ∉ 𝛼                put 𝑘 𝑣 = () ∈ 𝛼                      put 𝑘 𝑣 = () ∉ 𝛼 ′
𝛼  put 𝑘 𝑣 ⇓ ()                                ExistsF                        ExistsT                                       Get
                         𝛼  exists𝑘 ⇓ false              𝛼  exists𝑘 ⇓ true             𝛼 [put 𝑘 𝑣 = () ] 𝛼 ′  get 𝑘 ⇓ 𝑣


3 The remaining rules are completely standard and provided in the appendix.



, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                       9


Type Syntax
                            Base Types             𝑏 ::= unit | bool | nat | int | ...
                           Basic Types             𝑠 ::= 𝑏 | 𝑠  𝑠
                        Value Literals             𝑙 ::= 𝑐 | 𝑥 | 𝑜𝑝 𝑙 | mp 𝑙
                              Qualiﬁers           𝜙 ::= 𝑙 | ⊥ | ⊤ | ¬𝜙 | 𝜙 ∧ 𝜙 | 𝜙 ∨ 𝜙 | 𝜙 =⇒ 𝜙 | ∀𝑥:𝑏. 𝜙
                 Reﬁnement Types                   𝑡 ::= {𝜈:b | 𝜙} | 𝑥:𝑡  𝜏 | 𝑥:𝑏 d 𝑡
      Symbolic Finite Automata 𝐴, 𝐵 ::=                     hop x = 𝜈 | 𝜙i | h𝜙i | ¬𝐴 | 𝐴 ∧ 𝐴 | 𝐴 ∨ 𝐴 | 𝐴;𝐴 |      𝐴 | 𝐴U𝐴
          Hoare Automata Types                     𝜏 ::= [𝐴] 𝑡 [𝐴] | 𝜏 ⊓ 𝜏
                       Type Contexts               Γ ::=    ∅ | 𝑥:𝑡, Γ
Type Aliases
    hop ...∼𝑣𝑥 ... = 𝜈 | 𝜙 i  hop ...x... = 𝜈 | x = 𝑣𝑥 ∧ 𝜙 i   ♦𝐴  h⊤i U 𝐴     𝐴  ¬♦¬𝐴      LAST  ¬ h⊤i        𝑏  {𝜈:𝑏 | ⊤}

                                                            Fig. 4. 𝝀 E types.


The rule Put asserts that put operations always succeed. For a particular key, the ExistsF and
ExistsT rules stipulate that exists returns false or true, based on the presence of a corresponding
put event in the eﬀect context. Finally, the rule Get speciﬁes that the result of a get event is the
last value written by a put event to that key. Note that a program will get stuck if it attempts to
get a key in a trace without an appropriate put event, since there is no rule covering this situation.
   All the traces appearing in Sec. 2 can be derived from these rules. Under the eﬀect context 𝛼 0 , for
example, the expression, add “/a/b.txt” bytesFile , induces the trace 𝛼 2 as follows: the add function
uses the exists operator on the key “/a/b.txt” (line 6) to check if this path is in the ﬁle system. Since
the context trace 𝛼 0 lacks a put event with the key “/a/b.txt” , we have
                             [put “/” bytesDir = ()]  exists “/a/b.txt” ⇓ false               (existsF)

The trace used to evaluate subsequent expressions records this event: 𝛼 0 [exists “/a/b.txt” = false] .
The remaining evaluation of add “/a/b.txt” bytesFile is similar, yielding the following execution:
                                                           [exists “/a/b.txt” = false; exists “/a” = false]
      [put “/” bytesDir = ()]  add “/a/b.txt” bytesFile ↩−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−→∗ false

4    TYPE SYSTEM
   The syntax of 𝝀 E ’s types is shown in Fig. 4. Our type system uses pure reﬁnement types to
describe pure computations and Hoare Automata Types (HATs) to describe eﬀectful computations.
Our pure reﬁnement types are similar to those of other reﬁnement type systems [Jhala and Vazou
2021], and allow base types (e.g., int) to be further constrained by a logical formula or qualiﬁer.
Qualiﬁers in 𝝀 E are universally quantiﬁed formulae over linear arithmetic operations (𝑜𝑝 ) as well as
uninterpreted functions, or method predicates (mp), e.g., isRoot. Veriﬁcation conditions generated
by our type-checking algorithm can nonetheless be encoded as eﬀectively propositional (EPR)
sentences [Ramsey 1987], which can be eﬃciently handled by an oﬀ-the-shelf theorem prover
such as Z3 [de Moura and Bjørner 2008]. We also allow function types to be preﬁxed with a set of
ghost variables with base types (𝑥:𝑏 d 𝜏 ). Ghost variables are purely logical – they can only appear
in other qualiﬁers and are implicitly instantiated when the function is applied.
   Unique to 𝝀 E are the HATs ascribed to a stateful computation, which constrain the traces it may
produce. HATs use Symbolic Finite Automata (SFAs) [D’Antoni and Veanes 2014; D’Antoni and Veanes
2017; Veanes 2013] to qualify traces, similar to how standard reﬁnement types use formulae to

                                                                         , Vol. 1, No. 1, Article . Publication date: September 2018.
10                                                    Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


qualify the types of pure terms. We adopt the symbolic version of linear temporal logic on ﬁnite
traces [De Giacomo and Vardi 2013] as the syntax of SFAs.4
   As shown in Fig. 4, HATs support two kinds of atomic propositions, or symbolic eﬀect events:
hop x = 𝜈 | 𝜙i and h𝜙i . A symbolic eﬀect event hop x = 𝜈 | 𝜙i describes an application of an eﬀectful
operator op to a set of argument variables 𝑥 that produces a result variable 𝜈 . The formula 𝜙 con-
strains the possible instantiation of 𝑥 and 𝜈 in a concrete event. The other symbolic eﬀect event,
h𝜙i , is used to constrain the relationship between pure values (e.g., ghost variables and function
arguments). In addition to the temporal next ( 𝐴) and until operators (𝐴 U 𝐴), the syntax of HATs
includes negation (¬𝐴), intersection (𝐴 ∧ 𝐴), union (𝐴 ∨ 𝐴), and concatenation (𝐴; 𝐴). Fig. 4 deﬁnes
notations for other useful logical and temporal operators: implication (𝐴 =⇒ 𝐵  ¬𝐴 ∨ 𝐵 ), the even-
tually operator ♦, the globally operator , and importantly, the last modality LAST, which describes
a singleton trace, thus prohibiting a trace from including any other eﬀects [De Giacomo and Vardi
2013]. Fig. 4 also provides notations for specifying the value of an argument hop x ∼𝑣𝑥 x = 𝜈 | 𝜙i . As
is standard, we abbreviate the qualiﬁed type {𝜈:𝑏 | ⊤} as 𝑏 .
  Example 4.1. This syntax can capture rich properties over eﬀect contexts. For example, the fol-
lowing formulae concisely specify traces under which a key holds a certain value (𝑃stored ) and
when a particular key exists in the current store (𝑃exists ):
𝑃 stored (key, value)  ♦(hput ∼key ∼value = 𝜈 | ⊤i ∧          ¬hput ∼key x = 𝜈 | ⊤i)    𝑃 exists (key)  ♦hput ∼key x = 𝜈 | ⊤i



4.1      HATs, By Example
   Formally, a Hoare Automata Type [𝐴] 𝑡 [𝐵] qualiﬁes a reﬁnement type 𝑡 with two SFAs: a precon-
dition SFA 𝐴 that captures the context traces in which a term can be executed and a postcondition
SFA 𝐵 that describes the eﬀect trace after the execution of the term. Our type system also includes
intersection types on HATs (𝜏 ⊓ 𝜏 ), in order to precisely specify the behaviors of a program under
diﬀerent eﬀect contexts.
   Example 4.2 (Built-in Eﬀectful Operators). Our type system is parameterized over a (global) typ-
ing context Δ containing the types of built-in operators. Intuitively, the signatures of eﬀectful
operators in Δ captures the semantics the library developer ascribes to their API. Using the SFAs
from Example 4.1, for example, the signatures of put, exists, and get are:
       Δ(put) = k:Path.t  a:Bytes.t  [h⊤i] unit [h⊤i; (hput ∼k ∼a = 𝜈 | ⊤i) ∧ LAST]
       Δ(get) = a:Bytes.t d k:Path.t  [𝑃 stored (k, a)] {𝜈:Bytes.t | 𝜈 = a} [𝑃 stored (k, a); (hget ∼k = 𝜈 | 𝜈 = ai) ∧ LAST]
     Δ(exists) = k:Path.t  [𝑃 exists (k) ] {𝜈:bool | 𝜈 = true} [𝑃 exists (k) ; (hexists ∼k = 𝜈 | 𝜈 = truei ) ∧ LAST] ⊓
                              [¬𝑃 exists (k) ] {𝜈:bool | 𝜈 = false} [¬𝑃 exists (k) ; (hexists ∼k = 𝜈 | 𝜈 = falsei ) ∧ LAST]

The postcondition SFAs of all three operators use LAST, to indicate that they append a single
eﬀect event to the end of the eﬀect context ( hop v = 𝜈 | 𝜙i ∧ LAST). The type of put permits it to be
used under any context (h⊤i ). More interestingly, the built-in type of get uses a ghost variable
(a) to represent the current value of the key k; its precondition stipulates that it should only be
applied to keys that have been previously stored. Finally, the intersection type of exists describes
two possible behaviors, depending on whether the key k has been previously added to the store.
Note that the pre- and post-condition SFAs in these signatures express diﬀerent constraints on the
allowed contexts in which the operator may execute, and the eﬀects the operator performs.
  Example 4.3 (MinSet). Consider a developer who wants to implement an API for a set augmented
with an additional operation that returns the minimum element in the set. This implementation
4 Our type system is agnostic to the syntax used to express SFAs, and our implementation uses the more developer-friendly

syntax of Symbolic Regular Languages [De Giacomo and Vardi 2013]; this syntax is provided in appendix.


, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                               11


is deﬁned in terms of two other stateful libraries: a Set ADT that provides eﬀectful operators
insert:int  unit and mem:int  bool, and a MemCell library that provides a persistent cell with
eﬀectful read:unit  int and write:int  unit operators. One implementation strategy is to track
the minimum element in a persistent cell, and maintain the representation invariant that the con-
tents of this cell are always less than or equal to every element in the underlying set. Using SFAs,
we can express this invariant as:
    𝐼MinSet (el)  ♦(hwrite ∼el = 𝜈 | ⊤i ∧    ¬hwrite x = 𝜈 | ⊤i) =⇒ ♦hinsert ∼el = 𝜈 | ⊤i ∧ ¬hinsert x = 𝜈 | x < eli
                  ∧ (¬hwrite x = 𝜈 | ⊤i =⇒ ¬hinsert x = 𝜈 | ⊤i )

which speciﬁes that an element el is written into the persistent cell only when el has been inserted
into the backing Set and no element less than el has also been inserted. The HAT ascribed to the
function minset_insert enforces this invariant
                               el:int d elem:int  [𝐼 MinSet (el)] unit [𝐼 MinSet (el)]

   Example 4.4 (LazySet). As our next example, consider a LazySet ADT that provides a lazy version
of an insert operation, delaying when elements are added to an underlying Set ADT. The ADT
does so by returning a thunk closed over a collection of elements that will be added to the set when
it is forced. This ADT maintains the representation invariant that an element is never inserted
twice:
                          𝐼 LSet (el)  (hinsert ∼el = 𝜈 | ⊤i =⇒        ¬♦hinsert ∼el = 𝜈 | ⊤i)

We can specify a “lazy” insert operator using the following HAT:
 el:int d elem:int  thunk:(unit  [𝐼 LSet (el)] unit [𝐼 LSet (el)])  unit  [𝐼 LSet (el)] unit [𝐼 LSet (el)]

This operation takes as input a (potentially new) element elem to be added to the set and a thunk
holding any elements that have not yet been inserted into the backing set, and returns another
thunk. This HAT stipulates that both input thunk and output thunk preserve the representation
invariant of the ADT: unit  [𝐼 LSet (el)] unit [𝐼 LSet (el)].
   Example 4.5 (DFA). Our ﬁnal example is a library built on top of a stateful graph library that
is used to maintain the states and transitions of a Deterministic Finite Automaton (DFA). The
underlying graph library exports two methods to add (connect) and remove (disconnect) edges.
We can specify the standard invariant that DFAs only have deterministic transitions:
  𝐼DFA (n, c)  ¬(hconnect ∼n ∼c nend = 𝜈 | ⊤i ∧     (¬hdisconnect ∼n ∼c nend = 𝜈 | ⊤i U hconnect ∼n ∼c nend = 𝜈 | ⊤i) )

𝐼 DFA stipulates that a node n can have at most one transition on a character c ( hconnect ∼n ∼c nend = 𝜈 | ⊤i ).
Moreover, adding a new transition from n on c requires that any previous transitions on c have ﬁrst
been removed ( (¬hdisconnect ∼n ∼c nend = 𝜈 | ⊤i U hconnect ∼n ∼c nend = 𝜈 | ⊤i ). An add_transition method
with the following signature is thus guaranteed to preserve determinism:
   n:Node.t d c:Char.t d n_start:Node.t  char:Char.t  n_end:Node.t  [𝐼 DFA (n, c)] unit [𝐼 DFA (n, c)]

4.2    Typing Rules
   Type contexts. A type context (shown in Fig. 4) is a sequence of bindings from variables to pure
reﬁnement types (i.e., 𝑡 ). Type contexts are not allowed to contain HATs, as doing so breaks several
structural properties (e.g., weakening) that are used to prove type safety.5

5 Intuitively, since a type of the form [𝐴] 𝑡 [𝐵] describes a stateful computation, it cannot be duplicated or eliminated, and

thus it would be unsafe to allow unrestricted use of “computational” variables, as would be possible if type contexts could
contain such bindings.


                                                                  , Vol. 1, No. 1, Article . Publication date: September 2018.
12                                                     Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


Type Erasure                                                                                                              ⌊𝑡⌋       ⌊𝜏⌋   ⌊Γ⌋

            ⌊{𝜈:𝑏 | 𝜙}⌋  𝑏      ⌊𝑥:𝑡  𝜏 ⌋  ⌊𝑡 ⌋  ⌊𝜏 ⌋    ⌊𝑥:𝑏 d 𝑡 ⌋  ⌊𝑡 ⌋     ⌊[𝐴] 𝑡 [𝐵]⌋  ⌊𝑡 ⌋          ⌊𝜏1 ⊓ 𝜏2 ⌋  ⌊𝜏1 ⌋
                     ⌊∅⌋  ∅       ⌊𝑥:𝑡, Γ ⌋  𝑥:⌊𝑡 ⌋, ⌊Γ⌋

Well-Formed Types                                                                                   Γ ⊢WF 𝑡         Γ ⊢WF 𝐴         Γ ⊢WF 𝜏
          Γ ⊢WF 𝐴 Γ ⊢WF 𝐵 Γ ⊢WF 𝑡
                                                                            Γ ⊢WF 𝜏1      Γ ⊢WF 𝜏2       ⌊𝜏1 ⌋ = ⌊𝜏2 ⌋
      ∀𝜎 ∈ JΓK.L (𝜎 (𝐵) ) ⊆ L (𝜎 (𝐴; h⊤i ) )                                                                                   WFInter
                                                       WFHoare                           Γ ⊢WF 𝜏   1 ⊓ 𝜏2
                     Γ ⊢WF [𝐴] 𝑡 [𝐵]
Automata Inclusion                                    Γ ⊢𝐴 ⊆𝐴         Subtyping                                   Γ ⊢ 𝑡 <: 𝑡     Γ ⊢ 𝜏 <: 𝜏
                                                                        Γ ⊢ 𝐴2 ⊆ 𝐴1 Γ ⊢ 𝑡1 <: 𝑡2
                           ∀𝜎 ∈ JΓK.
                                                                          Γ ⊢ (𝐴2 ; h⊤i ) ∧ 𝐵 1 ⊆
                    L (𝜎 (𝐴1 ) ) ⊆ L (𝜎 (𝐴2 ) )
                                                  SubAutomata                 (𝐴2 ; h⊤i ) ∧ 𝐵 2
                          Γ ⊢ 𝐴1 ⊆ 𝐴2                                                                           SubHoare
                                                                      Γ ⊢ [𝐴1 ] 𝑡1 [𝐵 1 ] <: [𝐴2 ] 𝑡2 [𝐵 2 ]

                     SubIntLL                         SubIntLR                                                                 SubIntMerge
Γ ⊢ 𝜏1 ⊓ 𝜏2 <: 𝜏1                 Γ ⊢ 𝜏1 ⊓ 𝜏2 <: 𝜏2                 Γ ⊢ [𝐴1 ] 𝑡 [𝐵] ⊓ [𝐴2 ] 𝑡 [𝐵] <: [𝐴1 ∨ 𝐴2 ] 𝑡 [𝐵]


         Γ ⊢ 𝜏 <: 𝜏1                    Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑡1 <: 𝑡2                             ⌊Γ⌋ ⊢s 𝑣 : 𝑏
         Γ ⊢ 𝜏 <: 𝜏2                                                SubGhostR            Γ ⊢ 𝑡1 [𝑥 ↦→ 𝑣 ] <: 𝑡2
                           SubIntR        Γ ⊢ 𝑡1 <: 𝑥:𝑏 d 𝑡2                                                            SubGhostL
      Γ ⊢ 𝜏 <: 𝜏1 ⊓ 𝜏2                                                                    Γ ⊢ 𝑥:𝑏 d 𝑡1 <: 𝑡2

 Fig. 5. Selected auxiliary typing relations. ⌊Γ⌋ ⊢s 𝑒 : ⌊𝑡⌋ is the standard typing judgment for basic types.




    Auxiliary typing relations. Fig. 5 shows selected rules from three sets of auxiliary relations used
by our type system. The ﬁrst set describes the type erasure functions ⌊𝑡⌋ , ⌊𝜏⌋ , and ⌊Γ⌋ . The former
two functions return basic types by erasing all qualiﬁers and automata from types, while the latter
⌊Γ⌋ is the type context derived by applying ⌊...⌋ to all of Γ ’s bindings. The second set describes
well-formedness conditions on SFAs (Γ ⊢WF 𝐴) and types (Γ ⊢WF 𝑡 and Γ ⊢WF 𝜏 ). These rules
largely ensure that all the qualiﬁers appearing in a type are closed under the current typing context
Γ . The exceptions are WFInter, which stipulates that only HATs with the same basic type can
be intersected, and WFHoare, which requires the language accepted by the precondition SFA to
be a preﬁx of the postcondition automata (i.e., L(𝐵) ⊆ L(𝐴; h⊤i) , where h⊤i denotes the SFA
that accepts an arbitrary trace) after performing a substitution consistent with the current typing
context (𝜎 ∈ JΓK); the functions L(...) and J...K are deﬁned in the next subsection.
    Our type system also uses a mostly-standard subtyping relation that aligns with the denota-
tion of the types being related. Fig. 5 highlights key subtyping rules that do not have analogues
in a standard reﬁnement type system. The subtyping rule for symbolic automata (SubAutomata)
checks inclusion between the languages of the automata, after performing substitutions consis-
tent with the current typing context. The subtyping rule for (non-intersected) HATs (SubHoare)
checks that the inclusion is contravariant over the precondition automata and covariant over the
postcondition automata under the same context (i.e., the conjunction of 𝐵 1 and 𝐵 2 with 𝐴2 ; h⊤i ).
The subtyping rules for the intersection of HATs - SubIntLL, SubIntLR, and SubIntR - are stan-
dard. The SubIntMerge rule additionally allows the precondition automata of intersected types
to be merged. Finally, the subtyping rules for ghost variables either bind a ghost variable in the
type context (SubGhostR), or instantiate it to some concrete value (SubGhostL).

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                      13


Typing                                                                           Γ ⊢ 𝑜𝑝 : 𝑡    Γ ⊢ op : 𝑡    Γ ⊢𝑒 :𝑡      Γ ⊢𝑒 :𝜏

                                 Γ ⊢WF 𝜏2
       Γ ⊢WF 𝐴                                              Γ ⊢WF 𝜏1 ⊓ 𝜏2                           Γ ⊢WF 𝑥:𝑏 d 𝑡
                                Γ ⊢ 𝜏1 <: 𝜏2
       Γ ⊢𝑒 :𝑡                                          Γ ⊢ 𝑒 : 𝜏1 Γ ⊢ 𝑒 : 𝜏2                    Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑣 : 𝑡
                       TEPur     Γ ⊢ 𝑒 : 𝜏1                                          TInter                               TGhost
   Γ ⊢ 𝑒 : [𝐴] 𝑡 [𝐴]                           TSub         Γ ⊢ 𝑒 : 𝜏1 ⊓ 𝜏2                        Γ ⊢ 𝑣 : 𝑥:𝑏 d 𝑡
                                  Γ ⊢ 𝑒 : 𝜏2

    Γ ⊢WF 𝑡
   Δ(𝑜𝑝 ) = 𝑡            Γ ⊢WF 𝜏 Γ ⊢ 𝑜𝑝 : 𝑧𝑖 :𝑡𝑖  𝑡                          Γ ⊢WF [𝐴] 𝑡 [𝐵] Γ ⊢ op : 𝑧𝑖 :𝑡𝑖  𝜏
                 TPOp
   Γ ⊢ 𝑜𝑝 : 𝑡                   ∀𝑖.Γ ⊢ 𝑣𝑖 : 𝑡𝑖                                            ∀𝑖.Γ ⊢ 𝑣𝑖 : 𝑡𝑖
                             𝑡𝑥 = 𝑡 [𝑧𝑖 ↦→ 𝑣𝑖 ]                                   [𝐴] 𝑡𝑥 [𝐴′ ] = 𝜏 [𝑧𝑖 ↦→ 𝑣𝑖 ]
    Γ ⊢WF 𝑡                    Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : 𝜏                                      Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : [𝐴′ ] 𝑡 [𝐵]
                                                         TPOpApp                                                           TEOpApp
   Δ(op) = 𝑡              Γ ⊢ let 𝑥 = 𝑜𝑝 𝑣𝑖 in 𝑒 : 𝜏                             Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴] 𝑡 [𝐵]
                TEOp
   Γ ⊢ op : 𝑡

Fig. 6. Selected typing rules. All typing judgements (i.e., Γ ⊢ 𝑒 : 𝑡 and Γ ⊢ 𝑒 : 𝜏) assume the corresponding
basic type judgement (⌊Γ⌋ ⊢s 𝑒 : ⌊𝑡⌋ holds).


  A subset of our typing rules6 is shown in Fig. 6. Note that an stateful computations can only be
ascribed a HAT. As mentioned in Example 4.2, our type system is parameterized over Δ, a typing
context for built-in operators that provides HATs for both pure (TPOp) and eﬀectful operators
(TEOp). This system features the standard subsumption and intersection rules (TSub and TInter),
which enables our type system to use ﬁne-grained information about the eﬀect context when typ-
ing diﬀerent control ﬂow paths. The rule TEPur allows a pure term to be treated as a computation
that does not perform any eﬀects.
   Example 4.6. The add function in Fig. 1 has four possible control ﬂow paths, depending on the
eﬀect context under which it is called: (1) the input path exists in the ﬁle system (line 6); (2) neither
the input path or its parent path exist (line 9); (3) its parent path exists and is a directory (line 13−15),
or (4) it is not (line 16). The following four automata (recall that the SFA 𝑃isDir was deﬁned in Sec. 2)
indicate the eﬀect context corresponding to each of these scenarios:

                  𝐴1  𝐼FS (p) ∧ 𝑃 exists (path)
                  𝐴2  𝐼FS (p) ∧ ¬𝑃 exists (path) ∧ ¬𝑃 exists (parent(path) )
                  𝐴2  𝐼FS (p) ∧ ¬𝑃 exists (path) ∧ 𝑃 exists (parent(path) ) ∧ 𝑃 isDir (parent(path) )
                  𝐴3  𝐼FS (p) ∧ ¬𝑃 exists (path) ∧ 𝑃 exists (parent(path) ) ∧ ¬𝑃 isDir (parent(path) )
The union of these automata is exactly the representation invariant (𝐼 FS (p) ), established from the
following subtyping relation between their intersection and the return type of 𝜏add :
                                                                     l
    p:{𝜈:Path.t | ⊤}, path:{𝜈:Path.t | ⊤}, bytes:{𝜈:Bytes.t | ⊤} ⊢               [𝐴𝑖 ] bool [𝐼FS (p) ] <: [𝐼FS (p)] bool [𝐼FS (p) ]
                                                                        𝑖=1..4
                                                                                                                      (SubIntMerge)
Using the TInter and Tsub rules, our type system is able to reduce checking add against 𝜏add
into checking add against each 𝐴𝑖 (i.e., [𝐴𝑖 ] bool [𝐼 FS (p)]). Note that add only adds the given path
to the ﬁle system in the third case (line 13), whose precondition automata (𝐴2 ) indicates that
the input path does not exist in the ﬁle system (¬𝑃exists (path) ), although its parent path does
(𝑃exists (parent(path)) ), and is a directory (𝑃isDir (parent(path)) ). When coupled with the represen-
tation invariant that the parent of a path is always a directory in the ﬁle system, our type system
is able to ensure that it is safe to perform the put operation.
6 The complete set of typing rules for 𝝀 E is included in the appendix.



                                                                     , Vol. 1, No. 1, Article . Publication date: September 2018.
14                                                       Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


Trace Language                                                                                          𝛼, 𝑖 |= 𝐴   L(𝐴) ∈ P (𝛼)

Tr WF  {𝛼 | ∀ (op 𝑣𝑖 = 𝑣) ∈ 𝛼 .∅ ⊢s op : 𝑏𝑖  𝑏 ∧ (∀𝑖.∅ ⊢s 𝑣𝑖 : 𝑏𝑖 ) ∧ ∅ ⊢s 𝑣 : 𝑏 }                L (𝐴)  {𝛼 ∈ Tr WF | 𝛼, 0 |= 𝐴}
𝛼, 𝑖 |= hop xj = 𝜈 | 𝜙 i ⇐⇒ 𝛼 [𝑖 ] = op 𝑣 𝑗 = 𝑣 ∧ 𝜙 [𝑥 𝑗 ↦→ 𝑣 𝑗 ] [𝜈 ↦→ 𝑣 ]                 𝛼, 𝑖 |= 𝐴 ∧ 𝐴′ ⇐⇒ 𝛼, 𝑖 |= 𝐴 ∧ 𝛼, 𝑖 |= 𝐴′
𝛼, 𝑖 |= h𝜙 i ⇐⇒ 𝛼 [𝑖 ] = op 𝑣 𝑗 = 𝑣 ∧ 𝜙                                                     𝛼, 𝑖 |= 𝐴 ∨ 𝐴′ ⇐⇒ 𝛼, 𝑖 |= 𝐴 ∨ 𝛼, 𝑖 |= 𝐴′
𝛼, 𝑖 |=    𝐴 ⇐⇒ 𝛼, 𝑖+1 |= 𝐴                      𝛼, 𝑖 |= 𝐴1 ; 𝐴2 ⇐⇒ 𝛼 [𝑖...len(𝛼 ) ] = 𝛼 1 𝛼 2 ∧ 𝛼 1 ∈ L (𝐴1 ) ∧ 𝛼 2 ∈ L (𝐴2 )
𝛼, 𝑖 |= ¬𝐴 ⇐⇒ 𝛼, 𝑖 6 |= 𝐴                        𝛼, 𝑖 |= 𝐴 U 𝐴′ ⇐⇒ ∃ 𝑗 .𝑖 ≤ 𝑗 < len(𝛼 ).𝛼, 𝑗 |= 𝐴′ ∧ ∀𝑘.𝑖 ≤ 𝑘 < 𝑗 =⇒ 𝛼, 𝑘 |= 𝐴

Type Denotation                                                                                         J𝑡K ∈ P (𝑒)    J𝜏K ∈ P (𝑒)
                                                            ′          𝛼′ ∗        ′
          J{𝜈:𝑏 | 𝜙}K           {𝑒 | ∅ ⊢s 𝑒 : 𝑏 ∧ ∀𝛼 𝛼 𝑣. 𝛼  𝑒 ↩−→ 𝑣 =⇒ 𝛼 = [ ] ∧ 𝜙 [𝜈 ↦→ 𝑣 ] }
          J𝑥:𝑡  𝜏K             {𝑒 | ∅ ⊢s 𝑒 : ⌊𝑥:𝑡  𝜏 ⌋ ∧ ∀𝑣 ∈ J𝑡K. 𝑒 𝑣 ∈ J𝜏 [𝑥 ↦→ 𝑣 ]K}
          J𝑥:𝑏 d 𝜏K             {𝑒 | ∅ ⊢s 𝑒 : ⌊𝜏 ⌋ ∧ ∀𝑣.∅ ⊢s 𝑣 : 𝑏 =⇒ 𝑒 ∈ J𝜏 [𝑥 ↦→ 𝑣 ]K}
                                                                                       𝛼′
          J[𝐴] 𝑡 [𝐵]K           {𝑒 | ∅ ⊢s 𝑒 : ⌊𝑡 ⌋ ∧ ∀𝛼 𝛼 ′ 𝑣. 𝛼 ∈ L (𝐴) ∧ 𝛼  𝑒 ↩−→∗ 𝑣 =⇒ 𝑣 ∈ J𝑡K ∧ 𝛼 𝛼 ′ ∈ L (𝐵) }
          J𝜏1 ⊓ 𝜏2 K            J𝜏1 K ∩ J𝜏2 K

Type Context Denotation                                                                                               JΓK ∈ P (𝜎)
J∅K  { ∅ }                                                                     J𝑥:𝑡, ΓK  {𝜎 [𝑥 ↦→ 𝑣 ] | 𝑣 ∈ J𝑡K, 𝜎 ∈ JΓ[𝑥 ↦→ 𝑣 ]K}

                                                   Fig. 7. Type denotations in 𝝀 E

    Eﬀectful operator application. TPOpApp is the standard rule for operator application in a typical
reﬁnement type system [Jhala and Vazou 2021]. On the other hand, rule TEOpApp, the rule for
eﬀect operator application, with the help of the subsumption rule (TSub), allows operators to
have function types whose ghost variables are instantiated properly; moreover, the return type
of eﬀect operators is a non-intersected HAT. After ensuring each argument 𝑣𝑖 types against the
corresponding argument type 𝑡𝑖 and substituting all parameters (𝑧𝑖 ) with the supplied arguments
(𝑣𝑖 ), the return type of an eﬀectful operator must be in the form [𝐴] 𝑡𝑥 [𝐴′ ] and have exactly the
same precondition SFA (𝐴) as the type of the surrounding term. Typing the let-body 𝑒 is similar to
TPOpApp, where a new binding 𝑥:𝑡𝑥 is added to the type context. Moreover, the rule replaces the
precondition SFA used to type the body of the let with the postcondition SFA from the return type
of the eﬀect operator 𝐴′ , so that the body is typed in a context reﬂecting the use of the eﬀectful
operator.

4.3       Type Soundness
   The denotation of a SFA L(𝐴) , shown in Fig. 7, is the set of traces accepted or recognized by the
automata; the denotation of reﬁnement types J𝑡K and HATs J𝜏K are sets of terms; these functions
are deﬁned mutually recursively.
   The language of traces ranges over the set of all well-formed traces Tr WF , i.e., those only contain-
ing events (op 𝑣𝑖 = 𝑣 ) that are well-typed according to the basic type system. As is standard [De Giacomo and Vard
2013], our denotation uses an auxiliary judgement 𝛼, 𝑖 |= 𝐴 that deﬁnes when the suﬃx of a trace
𝛼 starting at the 𝑖 𝑡ℎ position is accepted by an automaton. The denotation of an SFA 𝐴 is the set of
(well-formed) traces recognized by 𝐴, starting at index 0.
  Type denotations. Out type denotations use a basic typing judgement ∅ ⊢s 𝑒 : 𝑠 that types an
expression 𝑒 according to the standard typing rules of the simply-typed lambda-calculus (STLC),
erasing all qualiﬁers in function argument types. The denotation of pure reﬁnement types is stan-
dard [Jhala and Vazou 2021]. The denotation of ghost variables is similar to function types whose

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                              15


parameters are restricted to base types. The denotation of an intersection type 𝜏1 ⊓ 𝜏2 is the inter-
section of the denotations 𝜏1 and 𝜏2 . An expression 𝑒 belongs to the denotation of a HAT [𝐴] 𝑡 [𝐵]
iﬀ every trace and value produced by 𝑒 is consistent with the SFA 𝐵 and reﬁnement type 𝑡, under
any eﬀect context accepted by the SFA 𝐴. Intuitively, the denotation of a HAT is naturally derived
from the language’s operational semantics, as depicted by the following correspondence:
Pure Language:         𝑒 ↩→ ∗ 𝑣 =⇒ 𝑒 ∈ J{𝜈:𝑏 | 𝜙}K              where 𝜙 [𝜈 ↦→ 𝑣] is valid
                          𝛼′ ∗
              𝝀 E : 𝛼  𝑒 ↩−→ 𝑣 =⇒ 𝑒 ∈ J[𝐴] {𝜈:𝑏 | 𝜙} [𝐵]K where 𝛼 ∈ L(𝐴), 𝛼 𝛼 ′ ∈ L(𝐵), and 𝜙 [𝜈 ↦→ 𝑣] is valid
In a pure language with the simple multi-step reduction relation 𝑒 ↩→ ∗ 𝑣 , reﬁnement types qualify
                                                                                                              𝛼′
the value 𝑣 that 𝑒 produces. In contrast, the multi-step reduction relation of 𝝀 E , 𝛼  𝑒 ↩−→∗ 𝑣 depends
on the eﬀect context 𝛼 and emits a trace 𝛼 ′ that records the sequence of eﬀects performed by
𝑒 during evaluation. Thus, HATs use precondition and postcondition automata (i.e., 𝐴 and 𝐵 ) to
qualify the trace before and after a term is evaluated (i.e., 𝛼 and 𝛼 𝛼 ′ ).
   Type context denotation. The denotation of a type context is a set of closing substitutions 𝜎 , i.e., a
sequence of bindings [𝑥𝑖 ↦→ 𝑣𝑖 ] consistent with the type denotations of the corresponding variables
in the type context. The denotation of the empty context is a singleton set containing only the
identity substitution ∅.
   Deﬁnition 4.7 (Well-formed built-in operator typing context). The built-in operator typing con-
text Δ is well-formed iﬀ the semantics of every built-in operator 𝜃 is consistent with its type:
Δ(𝜃) = 𝑥:𝑏 x d 𝑦:𝑡 y  𝜏 =⇒ ∀𝑥:𝑏 x . ∀𝑣 𝑦 ∈ J𝑡 y K. (𝜃 𝑣 𝑦 ) ∈ J𝜏 [𝑦 ↦→ 𝑣 𝑦 ]K.7

    Theorem 4.8. [Fundamental Theorem] Given a well-formed typing context for built-in operators
Δ, the trace of eﬀects produced by a well-typed term 𝑒 are captured by its corresponding HAT 𝜏 :
Γ ⊢ 𝑒 : 𝜏 =⇒ ∀𝜎, 𝜎 ∈ JΓK =⇒ 𝜎 (𝑒) ∈ J𝜎 (𝜏)K.8
   Corollary 4.9. [Type Soundness] Under a built-in operator type context that is well-formed, if a
function 𝑓 preserves the representation invariant 𝐴, i.e. it has the type: ∅ ⊢ f : 𝑥:𝑏 x d 𝑦:𝑏 y  [𝐴] 𝑡 [𝐴],
then for every set of well-typed terms ∅ ⊢ 𝑣 x : 𝑏 x and ∅ ⊢ 𝑣 y : 𝑏 y , applying 𝑓 to 𝑣 y under an eﬀect context
𝛼 that is consistent with 𝐴 results in a context 𝛼 𝛼 ′ that is also consistent with 𝐴:
                              𝛼′
                  𝛼  (f 𝑣y ) ↩−→∗ 𝑣 =⇒ 𝛼 𝛼 ′ ∈ L (𝐴[𝑥 ↦→ 𝑣x ] [𝑦 ↦→ 𝑣y ] ) ∧ 𝑣 ∈ J𝑡 [𝑥 ↦→ 𝑣x ] [𝑦 ↦→ 𝑣y ]K

5    TYPING ALGORITHM
   Converting our declarative type system into an eﬃcient algorithm requires resolving two key
issues. First, we cannot directly use existing SFA inclusion algorithms [D’Antoni and Veanes 2014;
D’Antoni and Veanes 2017] to implement the check in SubAutomata, because our SFAs may in-
volve non-local variables corresponding to function parameters and ghost variables; these vari-
ables can have reﬁnement types. We deal with this wrinkle by integrating the subtyping algorithm
for pure reﬁnement types into the existing SFA algorithm. Second, typing the use of an eﬀectful
operator, e.g., put or exists, depends on the set of eﬀects in the precondition of the current HAT.
The declarative type system can ensure that this automaton has the right shape by applying the
TInter and TSub rules at any point in a derivation, but an eﬃcient implementation must perform
this conversion more intelligently. Our solution to this problem is to employ a bidirectional type
system [Dunﬁeld and Krishnaswami 2021] that closely tracks a context of eﬀects that have pre-
ceded the term being typed, and selectively applies the subsumption rule to simplify the context
when switching between checking and synthesis modes.
7 Recall that the semantics of an operator is deﬁned by the auxiliary 𝑒 ⇓ 𝑣 and 𝛼  𝑒 ⇓ 𝑣.
8 A Coq mechanization of this theorem and the type soundness corollary are provided in the appendix.



                                                                  , Vol. 1, No. 1, Article . Publication date: September 2018.
16                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


 Algorithm 1: Inclusion Query
1  Procedure SFAInclusion (Γ, 𝐴, 𝐵) :=
2     𝐿Γ ← GetLits(Γ);
3     foreach 𝜙 Γ ∈ BoolComb(𝐿Γ ) do
4         𝑀 ← ∅;
5         foreach op where ∅ ⊢s op : 𝑏𝑖  𝑏 do
6             𝐿 ← GetLits(Γ, 𝐴 ∨ 𝐵);
7             foreach 𝜙 ∈ BoolComb(𝐿) do
8                 if Γ, 𝑥𝑖 :𝑏𝑖 0 {𝜈:𝑏 | 𝜙 Γ ∧ 𝜙} <: {𝜈:𝑏 | ⊥} then
 9                     𝑀 ← 𝑀 ∪ {hop xi = 𝜈 | 𝜙 Γ ∧ 𝜙i}

10           if L(AlphaTrans (𝑀, 𝐴)) * L(AlphaTrans (𝑀, 𝐵)) then
11               return false;

12      return true;




5.1    SFA Inclusion
   Symbolic alphabets allow the character domains of SFAs to be inﬁnite, making them strictly
more expressive than standard FAs. This enhanced expressivity comes at a cost, however, as the
standard FA inclusion algorithm cannot be directly applied to SFAs. Thankfully, prior work has
shown how to reduce an inclusion check over SFAs to an inclusion check over FAs [D’Antoni and Veanes
2014; D’Antoni and Veanes 2017]. The high-level approach is to ﬁrst construct a ﬁnite set of equiv-
alence classes over an SFA’s inﬁnite character domain, deﬁned in terms of a set of maximal satisﬁ-
able Boolean combinations of logic literals (called minterms) in the automaton’s symbolic alphabet.
An alphabet transformation procedure then replaces characters in the original SFA with their cor-
responding equivalence classes, and replaces the SFA’s symbolic alphabet with minterms, thus
allowing SFAs to be translated into FAs. As long as the satisﬁability of minterms is decidable, so
is checking inclusion between two SFAs. Our use of EPR formulas for qualiﬁers guarantees that
minterm satisﬁability is decidable.
   The pre- and post-conditions used in HATs have two features that distinguish them from stan-
dard SFAs, however: 1) characters are drawn from a set of distinct events and their qualiﬁers may
range over multiple variables, instead of a single local variable; and, 2) event qualiﬁers may refer to
variables in the typing context, i.e., function parameters and ghost variables. Our language inclu-
sion algorithm, shown in Algorithm 1, accounts for all these diﬀerences by extending the existing
SFA inclusion algorithm to incorporate a subtyping check between pure reﬁnement types.

   Candidate Minterms. The ﬁrst step in checking SFA inclusion is to construct the equivalence
classes used to ﬁnitize its character set. With HATs, these characters range over events triggered
by the use of library operations op 𝑣 = 𝑣 , and return events ret 𝑣 . As each class of events is already
disjoint (e.g., get and put events will never overlap), we only need to build minterms that partition
                                                                                     Ó         Ó
individual classes. The minterms of each class of events have the form hop xi = 𝜈 | ( 𝑙 𝑗 ) ∧ ( ¬𝑙𝑘 )i . To
build the literals used in these minterms for an event op, we collect all the literals 𝑙 used to qualify
op, as well as any literals appearing in atomic predicates h𝜙i , and then construct a maximal set
of satisﬁable Boolean combinations of those literals. Notably, these literals may contain variables
bound in the current typing context. Our algorithm divides minterms into two categories: Boolean
combinations of literals from the typing context (line 3), 𝜙 Γ , and Boolean combinations of literals

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                 17


Type Synthesis                      Γ ⊢𝑒 ⇒𝑡      Γ ⊢𝑒 ⇒𝜏                Type Check                      Γ ⊢𝑒 ⇐𝑡     Γ ⊢𝑒 ⇐𝜏
      Γ ⊢WF 𝑥:𝑏 d 𝜏     Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑒 ⇐ 𝜏                      Γ ⊢WF 𝜏1 ⊓ 𝜏2     Γ ⊢ 𝑒 ⇐ 𝜏1      Γ ⊢ 𝑒 ⇐ 𝜏2
                                                   ChkGhost                                                        ChkInter
                 Γ ⊢ 𝑒 ⇐ 𝑥:𝑏 d 𝜏                                                  Γ ⊢ 𝑒 ⇐ 𝜏1 ⊓ 𝜏2

                                                        Γ ⊢WF [𝐴] 𝑡 [𝐵]           Δ(op) = 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥
            Γ ⊢WF [𝐴2 ] 𝑡2 [𝐵 2 ]                                             ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗
   Γ ⊢ 𝑒 ⇒ [𝐴1 ] 𝑡1 [𝐵 1 ] Γ ⊢ 𝐴2 ⊆ 𝐴1
                                                                 Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
               Γ ⊢ 𝑡1 <: 𝑡2                                         d
                                                                       [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]
 Γ ⊢ (𝐴2 ; h⊤i ) ∧𝐵 1 ⊆ (𝐴2 ; h⊤i ) ∧𝐵 2
                                             ChkSub        ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
          Γ ⊢ 𝑒 ⇐ [𝐴2 ] 𝑡2 [𝐵 2 ]                                                                                  ChkEOpApp
                                                                 Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]

                                       Fig. 8. Selected Bidirectional Typing Rules


appearing from the input automata (line 7). The ﬁnal set of candidate minterms are (satisﬁable)
conjunctions of the elements of 𝜙 Γ and 𝜙 (line 9).
    Satisﬁability Check. The soundness of the alphabet transfer procedure requires that only satisﬁ-
able minterms are used, so that every transition in the output FA corresponds to an actual transition
in the original SFA. To understand how this is done, observe that the typing context plays a similar
role in checking both the satisﬁability of minterms and the subtyping relation. Thus, the algorithm
                                                      Ó          Ó
reduces checking the satisﬁability of hop xi = 𝜈 | ( 𝑙 𝑗 ) ∧ ( ¬𝑙𝑘 )i to checking whether the reﬁnement
              Ó         Ó                                                                          Ó         Ó
type {𝜈:𝑏 | ( 𝑙 𝑗 ) ∧ ( ¬𝑙𝑘 )} is not a subtype of {𝜈:𝑏 | ⊥} (line 8), that is Γ, 𝑥𝑖 :𝑏𝑖 0 {𝜈:𝑏 | ( 𝑙 𝑗 ) ∧ ( ¬𝑙𝑘 )} <:
                                                                                               Ó          Ó
{𝜈:𝑏 | ⊥}. Since {𝜈:𝑏 | ⊥} is uninhabited, this subtype check fails precisely when ( 𝑙 𝑗 ) ∧ ( ¬𝑙𝑘 ) is sat-
isﬁable under Γ .
  Inclusion Check. Equipped with the set of satisﬁable minterms, the ﬁnal inclusion check (line
10) is a straightforward application of the textbook inclusion check between the FA produced by
the standard alphabet transformation algorithm (line 10).9 SFAInclusion returns true only when
automata 𝐴 is included by 𝐵 under all instantiations of the variables in Γ .

5.2    Bidirectional Type System
   As is standard, our bidirectional type system consists of both type synthesis ( ⇒ ) and type
checking ( ⇐ ) judgments. The bidirectional system features a minor divergence from the declar-
ative rules. While the declarative system was able to use the subsumption rule (TSub) to freely
instantiate ghost variables, a typing algorithm requires a more deterministic strategy. Our solu-
tion is to treat ghost variables 𝑥:𝑏 d as instead being qualiﬁed by an unknown formula which is
specialized as needed, based on the information in the current typing context. In order to eﬃ-
ciently infer the qualiﬁers of ghost variables, our algorithm only allows ghost variables to appear
in SFAs. This restriction ensures that ghost variables are only used during SFA inclusion checks,
and allows it to avoid the more sophisticated algorithms needed when ghost variables can appear
in arbitrary reﬁnement types [Tondwalkar et al. 2021]. This restriction is enforced by our algorith-
mic typing rules: the second line of ChkEOpApp (∀𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗 ) for example, only holds when no
free ghost variables appear in the parameter types 𝑡 𝑗 used by ≈› (Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘 ).
   With this minor tweak in hand, the top-level typing algorithm is mostly a matter of bidirection-
alizing the typing rules of 𝝀 E by choosing appropriate modes for the assumptions of each rule.
This is largely straightforward: the type checking rule for ghost variables (ChkGhost) adapts the
9 The details of alphabet transfer algorithm can be found in the appendix.



                                                                    , Vol. 1, No. 1, Article . Publication date: September 2018.
18                                                   Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan

                                                                     d
     Γ = 𝑥𝑖 :{𝜈:𝑏𝑖 | 𝜙𝑖 }, 𝑦:(𝑢:𝑏𝑢 d 𝑧:𝑡  𝜏 )                         [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏 Γ′ = Γ, 𝑦 𝑗 :𝑡 𝑗
                     Ó                                                               Ô
      ∀𝑥𝑖 :𝑏𝑖 .∀𝜈:𝑏. 𝜙𝑖 =⇒ (𝜙 1 =⇒ 𝜙 2 )                             Abduce (Γ, 𝐴, 𝐴𝑖 , 𝑧𝑘 :𝑏𝑘 ) = 𝑧𝑘 :𝑡𝑘
                                                   SubBaseAlg                                                 InstAlg
           Γ ⊢ {𝜈:𝑏 | 𝜙 1 } <: {𝜈:𝑏 | 𝜙 2 }                          Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏 ≈›𝑧𝑘 :𝑡𝑘

                                          Fig. 9. Selected Auxiliary Typing Functions


corresponding declarative rule (TGhost) in the standard way, for example. The rule for checking
eﬀectful operations (ChkEOpApp) is similar, although it adopts a ﬁxed strategy for applying the
subsumption rule: 1) instead of using TSub to instantiate ghost variables directly, it now relies
on an auxiliary function, ≈›, to strengthen their qualiﬁers based on the current context; 2) when
                                                                   d
the result of the library operation op is an intersection type ( [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]), ChkEOpApp considers
each case of the intersection, instead of using TSub to focus on a single case; and 3) instead of
relying on TSub to align the postcondition automata (𝐴𝑖′ ) of op with the precondition of the HAT
being checked against (𝐴), the rule uses the conjunction of the automata ( (𝐴; h⊤i) ∧ 𝐴𝑖′ ) as the
precondition automata used to check the term that uses the result of op. The implementation of
 ≈› relies on the Abduce subroutine.10 Given a typing context Γ, set of ghost variables 𝑥:𝑏, and a pair
of automata 𝐴 and 𝐴′ , Abduce infers a set of qualiﬁers 𝜙 for 𝑥:𝑏 suﬃcient enough to ensure that
𝐴 is included in 𝐴′ , i.e. Γ, 𝑥:{𝜈:b | 𝜙} ⊢ 𝐴 ⊆ 𝐴′ , or reports that none exists. Abduce is an adaption
of an existing algorithm [Zhou et al. 2021] which infers the weakest qualiﬁers 𝜙𝑖 needed for the
inclusion check.
  Theorem 5.1. [Soundness of Algorithmic Typing] Given a well-formed built-in typing context Δ,
type context Γ , term 𝑒 , and HAT 𝜏 , Γ ⊢ 𝑒 ⇐ 𝜏 =⇒ Γ ⊢ 𝑒 : 𝜏 .11
  Theorem 5.2. [Decidability of Algorithmic Typing] Type checking a term 𝑒 against a type 𝜏 in a
typing context Γ , i.e., Γ ⊢ 𝑒 ⇐ 𝜏 , is decidable.

6    IMPLEMENTATION AND EVALUATION
   We have implemented a tool based on the above approach, called Marple, that targets ADTs
implemented in terms of other stateful libraries. Marple consists of approximately 12K lines of
OCaml and uses Z3 [de Moura and Bjørner 2008] as its backend solver for both SMT and FA inclu-
sion queries.12
   Marple takes as an input the implementation of an ADT in OCaml, enhanced signatures of
ADT operations that include representation invariants expressed as HATs, and speciﬁcations of
the supporting libraries as HATs (e.g., the signatures in Example 4.2). The typing context used by
Marple includes signatures for a number of (pure) OCaml primitives, including the pure operators
listed in Fig. 2. Marple also includes a set of predeﬁned method predicates (i.e., 𝑚𝑝 in Fig. 4) that
allow qualiﬁers to capture non-trivial datatype properties. For example, the method predicates
isDir(x) and isDel(y) from the motivating example in Sec. 2 encode that x holds the contents
of a directory, and that y is marked as deleted, respectively. The semantics of method predicates
are deﬁned via a set of lemmas in FOL, in order to enable automated veriﬁcation; e.g., the axiom
∀x.isDir(x) =⇒ ¬isDel(x) encodes that a set of bytes cannot simultaneously be an active directory
and marked as deleted.
   Our experimental evaluation addresses three research questions:
10 The full details of Abduce can be found in the appendix.
11 The proofs of Theorems 5.1and 5.2 can be found in the appendix.
12 Our appendix provides a docker image that contains the source code of Marple and all our benchmarks.



, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                  19


Table 1. Experimental results of using Marple to verify representation invariants of ADTs. Benchmarks from
prior works are annotated with their source: Okasaki [Okasaki 1999](† ), Hanoi [Miltner et al. 2020](★ ). We
have rewritten functional implementations of these benchmarks into stateful versions by assuming there is a
hidden mutable datatype instance that ADT methods use to perform their operations. The backing stateful
libraries are drawn from a verified OCaml library [Charguéraud et al. 2017].
      ADT           Library    #Method #Ghost s𝐼           ttotal (s) #Branch #App #SAT #FA ⊆ avg. sFA tSAT (s) tFA ⊆ (s)
                  LinkedList        7       0        4      5.94           4       7     297     7       98       1.63      0.06
     Stack†        KVStore          7       1        9      17.88          4       10    874     17      226      5.78      0.23
                  LinkedList        6       0        4      4.88           4       9     190     4       96       1.08      0.06
     Queue†         Graph           6       1        24     28.24          5       12    1212    14      525      8.19      0.86
                    Tree            5       0        12     27.12          5       12    1589    11      531      9.34      0.53
      Set★         KVStore          3       1        9      2.39           3       5     245     6       160      1.51      0.06
                     Tree           7       0        12     25.71          5       12    1589    11      531      9.33      0.52
     Heap★        LinkedList        6       0        4      8.84           4       8     497     8       118      3.03      0.08
                     Set            4       1        28     10.55          3       6     612     17      294      4.19      1.58
     MinSet        KVStore          4       1        25     32.84          5       8     2227    23      519      10.93     9.34
                    Tree            6       0        12     27.10          5       12    1589    11      531      9.33      0.57
     LazySet         Set            4       1        9      1.42           2       3     101     4       106      0.57      0.04
                   KVStore          5       1        9      3.10           3       5     245     6       160      1.49      0.06
                    Tree            6       1        20      58.80         3       8     2085    17      652      14.15    2.21
   FileSystem      KVStore          4       1        17     157.27         4       10    8144    43      481      56.64    16.54
                   KVStore          5       2        18     42.62          3       3     3604    25      228      18.84     1.60
      DFA           Graph           5       2        11     78.44          4       4     3625    27      225      25.53     3.42
                     Set            5       2        9       80.46         4       4     3889    50      357      27.39    12.80
ConnectedGraph      Graph           5       1        20     176.89         4       3     1349    17      360      19.19    53.90

Table 2. Details of the properties used in the benchmarks shown in Table 1. Representation invariants of
client ADTs are expressed in terms of their interactions with the backing stateful library.
                    Representation      Underlying
   Client ADT         Invariant          Library                     Policy governing interactions with underlying API

                                        LinkedList                     The addresses that store elements are unique
      Stack         LIFO-property        KVStore                                Not a circular linked list
                                        LinkedList                             Not a circular linked list
     Queue           FIFO-property        Graph             No self-loops in graph, degree of nodes in graph are at most 1
                        Unique            Tree                          The underlying tree is a binary search tree
       Set                               KVStore                       Every key is associated with a distinct value
                       elements
                                                                         The value of the parent node in the tree
                                           Tree                           is less than the value of its child nodes
      Heap        Min-heap property
                                        LinkedList                   Not a circular linked list; the elements are sorted
                                                                 The cached element is less than all inserted elements
                                           Set                       in the set and has been inserted into the set
     MinSet         Uniqueness and
                      minimality                                   The cached element is less than all put elements
                                         KVStore                         in the store and has been put before
                      Uniqueness          Tree                          The underlying tree is a binary search tree
     LazySet                               Set                          An element has never been inserted twice
                      of elements        KVStore                       Every key is associated with a distinct value
                                                            The Parent node stores a path that is preﬁx of its child nodes;
                                           Tree                        a non-root parent node stores directories
   FileSystem     Policy of Unix-like
                   ﬁlesystem paths                          Any non-root path stored as a key in the key-value store must
                                         KVStore             have its parent stored as a non-deleted directory in the store
                     Determinism                           All stored transitions are represented as tuples (start, char, end);
                                         KVStore            starting state has at most have one transition for a character
      DFA            of Transitions                      Two nodes (which represent states in FA) can have at most one edge,
                                          Graph                            which is labeled with a character
                                                            The set stores unique pairs (fst, snd); only elements that have
                                           Set              both in and out edges are treated as a value node in the graph
ConnectedGraph       Connectivity
                                          Graph                         All nodes in the graph are connected

                                                                      , Vol. 1, No. 1, Article . Publication date: September 2018.
20                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


  Q1: Is Marple eﬀective? Can it verify a diverse range of ADTs that are implemented using a
        variety of backing stateful libraries?
  Q2: Is Marple expressive? Are HATs able to capture a rich set of representation invariants?
  Q3: Is Marple eﬃcient? Is it able verify clients of stateful APIs in a reasonable amount of time?
   We have evaluated Marple on a corpus of complex and realistic ADTs drawn from a variety of
sources (shown in the title of Table 1), including general datatypes such as stacks, queues, sets,
heaps, graphs, as well as custom data structures including the Unix-style ﬁle system from Sec. 1
and the deterministic ﬁnite automata described in Sec. 4 (Q1). Table 1 presents the results of this
evaluation. Each datatype includes multiple implementations using diﬀerent underlying libraries
(Library column), each of which provides a distinct set of operations. Our backing APIs include
linked lists, a persistent key-value store, sets, trees, and graphs, each of which induces a diﬀerent
encoding of the target ADT’s representation invariant.
   Table 1 divides the results of our experiments into two categories, separated by the double bars;
the ﬁrst gives comprehensive results about analyzing the entire datatype, while the second reports
information about the most complex method of each ADT implementation.13 The ﬁrst group of
columns describes broad characteristics of each ADT, including its number of methods (#Method),
the number of ghost variables in its representation invariant (#Ghost), and the size of the formula
encoding the representation invariant (s𝐼 ), after it is desugared into a symbolic regular expression.
The next column reports the total time needed to verify all the method of each ADT (ttotal ). Marple
performs quite reasonably on all of our benchmarks, taking between 1.42 to 176.89 seconds for
each ADT. As expected, more complicated ADT implementations (i.e., those with larger values in
the #Method, #Ghost, and s𝐼 columns), take longer to verify (Q3).
   Details about the representation invariants used in our benchmarks are shown in Table 2 (Q2).
The stack and queue ADTs require a low-level guarantee that the underlying linked list implemen-
tation is not circular. The set ADTs maintain the invariant that there are no duplicate elements.
The connected graph benchmark requires that every pair of nodes is connected, necessitating the
need for ghost variables. As shown in Table 1, all of these properties, as well as those discussed
in previous sections, can be expressed using LTL 𝑓 using no more than 2 ghost variables (#Ghost)
and 28 literals (s𝐼 ).
   The ﬁrst group of columns in the second half of Table 1 list features relevant to the complex-
ity of the most demanding method in the ADT. These methods feature between 3 and 5 branches
(#Branch) and 3 to 12 uses of built-in operators (#App). The last two groups of columns present
type checking results for these methods. The #SAT and #FA ⊆ columns list the number of SMT
queries and ﬁnite automata (FA) inclusion checks needed to type check the method. The next
column (avg. sFA ) gives the average number of transitions in the ﬁnite state automata (FA) after
the alphabet transformation described in Sec. 5. These numbers are roughly proportional to code
complexity (column #Branch and #App) and invariant complexity (column #Ghost and s𝐼 ) — intu-
itively, programs that have more uses of operators and larger speciﬁcations, require more queries
and produce more complicated FAs. The last two columns report veriﬁcation time for the method
(Q3). These times are typically dominated by the SFA inclusion checks (ranging from .63 to 73.09
seconds) that result from minterm satisﬁability checks during the alphabet transformation phase
(tSAT ) and FA inclusion checks (tFA ⊆ ). Unsurprisingly, generating more queries (both #SMT and
#FA ⊆ ) result in more time spent checking minterm satisﬁability and FA inclusion. Our results also
indicate that FA inclusion checks are not particularly sensitive to the size of the FA involved; rather,
the cost of these checks corresponds more closely to the deep semantics of the representation in-
variant, in which the choice of the underlying library is an important factor. Taking the FileSystem
13 Our appendix includes a full table listing the corresponding information for each ADT method.



, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                         21


benchmark as an example, both Tree and KVStore implementations lead to similar sizes for the
invariant, in term of #Ghost. s𝐼 , and FA (avg.sFA ). However, the use of the former library results
in a signiﬁcantly shorter veriﬁcation time since the relevant property captured by the invariant
“every child has its parent in the ﬁle system” is naturally supported by the Tree library; the only
remaining veriﬁcation task in this case for the client to handle involves ensuring these parents are
indeed directories in the ﬁle system. In contrast, the KVStore provides no such guarantees on how
its elements are related, requiring substantially more veriﬁcation eﬀort to ensure the invariant is
preserved.

7   RELATED WORK
   Representation Invariant Inference. Miltner et al. [2020] develop a data-driven CEGIS-based in-
ference approach, while Malik et al. [2007] develop a solution derived from examining testcases.
Solvers used to infer predicates that satisfy a set of Constrained Horn Clauses (CHCs) [Ezudheen et al.
2018; Hojjat and Rümmer 2018; Zhu et al. 2018] can also be thought of as broadly addressing sim-
ilar goals. Our focus in this paper is orthogonal to these eﬀorts, however, as it is centered on the
automated veriﬁcation of user-speciﬁed representation invariants expressed in terms of SFAs.
   Eﬀect Veriﬁcation. There has been signiﬁcant prior work that considers the type-based ver-
iﬁcation of functional programs extended with support for (structured) eﬀectful computation.
Ynot [Nanevski et al. 2008b] and F* [Swamy et al. 2023] are two well-known examples whose type
speciﬁcations allow ﬁne-grained eﬀect tracking of stateful functional programs. These systems
allow writing speciﬁcations that leverage type abstractions like the Hoare monad [Nanevski et al.
2008a] or the Dijkstra monad [Ahman et al. 2017; Fromherz et al. 2021; Maillard et al. 2019; Swamy et al.
2020, 2013]. For example, speciﬁcations using the Hoare monad involve writing type-level asser-
tions in the form of pre- and post-conditions over the heaps that exist before and after a stateful
computation executes. The Dijkstra monad generalizes this idea by allowing speciﬁcations to be
written in the style of a (weakest precondition) predicate transformer semantics, thus making it
more amenable for improved automation and VC generation. While our goals are broadly similar to
these other eﬀorts, our setup (and consequently, our approach) is fundamentally diﬀerent. Because
we assume that the implementation of eﬀectful operations are hidden behind an opaque interface,
and that the speciﬁcations of these operations are not tailored for any speciﬁc client application,
our veriﬁcation methodology must necessarily reason about stateful library actions, indirectly in
terms of the history of calls (and returns) to library methods made by the client, rather than in
terms of predicates over the concrete representation of the state. One important way that our sig-
niﬁcantly diﬀerent representation choice impacts our veriﬁcation methodology is that unlike e.g.,
the Dijkstra monad that uses a predicate transformer semantics to establish a relation between
pre- and post-states of an eﬀectful action, our typing of interaction history in terms of HATs al-
lows us to simply reuse a standard subtying relation (suitably adapted), instead. Consequently, the
implementation of our typing algorithm is amenable to a signiﬁcant degree of automation, on par
with other reﬁnement type systems like Liquid Haskell [Vazou et al. 2014].
   Monadic-based techniques [Chappe et al. 2023; Li and Weirich 2022; Wiegley and Delaware 2017;
Xia et al. 2019; Zhang et al. 2021] to reason about eﬀectful programs have also been well-studied,
especially in the context of interactive (mechanized) veriﬁcation. One notable instance are inter-
action trees (ITrees) [Xia et al. 2019], a coinductive variant of the free monad that also provide an
abstraction of an (inﬁnite) sequence of visible events (i.e., traces) produced by eﬀectful programs.
Analogous to HATs, context and eﬀect traces can be expressed as pre- and post- ITrees [Zhang et al.
2021]. In contrast to ITrees, HATs use of SFAs provides a decidable inclusion check, which enables
fully automated veriﬁcation. Furthermore, because SFAs denote a regular trace language, they en-
able the use of LTL 𝑓 , an arguably more readable and lighter-weight speciﬁcation language.

                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
22                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


   Type and Eﬀect Systems. Type and eﬀect systems comprise a broad range of techniques that
provide state guarantees about both what values a program computes and how it computes them.
These systems have been developed for a number of diﬀerent applications: static exception check-
ing in Java [Java 2013], ensuring eﬀects are safely handled in the languages with algebraic ef-
fects [Bauer and Pretnar 2013], and reasoning about memory accesses [Giﬀord and Lucassen 1986],
in order to ensure, e.g., programs can be safely parallelized [Abadi et al. 2011]. Notably, a majority
of these systems are agnostic to the order in which these eﬀects are produced: the eﬀect system in
Java, for example, only tracks whether or not a computation may raise an exception at run-time.
   In contrast, sequential eﬀect systems [Tate 2013] provide ﬁner grained information about the
order in which a computation’s eﬀects may occur. More closely related to this work are type and ef-
fect systems that target temporal properties on the sequences of eﬀects a program may produce. For
example, Skalka and Smith [2004] present a type and eﬀect system for reasoning about the shape of
histories (i.e., ﬁnite traces) of events embedded in a program, with a focus on security-related prop-
erties expressed as regular expressions augmented with ﬁxed points. Their speciﬁcation language
is not rich enough to capture data-dependent properties: the histories of a conditional expression
must include the histories of both branches, even when its condition is a variable that is provably
false. Koskinen and Terauchi [2014] present a type and eﬀect system that additionally supports
veriﬁcation properties of inﬁnite traces, speciﬁed as Büchi automata. Their system features reﬁne-
ment types and targets a language similar to 𝝀 E . Their eﬀect speciﬁcations also include a second
component describing the sets of inﬁnite traces a (non-terminating) program may produce, en-
abling it to reason about liveness properties. Unlike 𝝀 E , however, events in their system are not
allowed to refer to program variables. This restriction was later lifted by Nanjo et al. [2018], whose
results support value-dependent predicates in eﬀect speciﬁcations written in a ﬁrst-order ﬁxpoint
logic. To solve the resulting veriﬁcation conditions, they introduce a novel proof system for this
logic. More recently, Sekiyama and Unno [2023] consider how to support richer control ﬂow struc-
tures, e.g., delimited continuations, in such an eﬀect system. To the best of our knowledge, all of
these eﬀect systems lack an analogue to the precondition automaton of HATs, and instead have
to rely on the arguments of a dependently typed function to constrain its set of output traces, as
opposed to constructing and managing the context of previously seen events and their results.
   While our focus has been on the development of a practical type system for the purposes of
veriﬁcation, there have also been several works that provide foundational characterizations of
sequential eﬀect systems. Most of these works adopt a semantics-oriented approach and seek to
develop categorical semantics for eﬀectful languages [Katsumata 2014; Mycroft et al. 2015; Tate
2013]. More closely related is the recent work of Gordon [Gordon 2021], which deﬁnes a generic
model of sequential eﬀects systems in terms of a parameterized system. The key idea is to represent
eﬀects as a quantale, a join semi-lattice equipped with a top element and whose underlying set is
also a monoid. The proposed type system is parameterized over an arbitrary eﬀect quantale; this
system is proven to be safe for any appropriate instantiation of this parameter.
   Type-Based Protocol Enforcement. Because HATs express a history of the interaction between a
client and an stateful library, they naturally serve as a form of protocol speciﬁcation on client be-
havior (e.g., session types [Honda 1993; Vasconcelos 2009]), although the kinds of protocols we con-
sider in this work are limited to those that are relevant to deﬁning a representation invariant, i.e.,
those that capture constraints on library methods suﬃcient to ensure a desired client invariant. In
this sense, HATs play a similar role as typestate in object-oriented languages [Bodden and Hendren
2012; DeLine and Fähndrich 2004; Sunshine et al. 2011], which augments the interface of objects




, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                         23


with coarse-grained information about the state of an object, in order to constrain its set of avail-
able methods. Typestate speciﬁcations diﬀer in obvious ways from HATs, most notably with re-
spect to the level of granularity that is expressible; in particular, HATs are designed to capture
ﬁne-grained interactions between libraries and clients that are necessary to specify useful repre-
sentation invariants.

8    CONCLUSION
   This paper explores the integration of SFAs within a reﬁnement type system as a means to
specify and verify client-speciﬁc representation invariants of functional programs that interact
with stateful libraries. Our key innovation is the manifestation of SFAs as HATs in the type sys-
tem, which allows the speciﬁcation of context traces (preconditions) as well as computation traces
(postconditions) that allow us to characterize the space of allowed client/library interactions and
thus enable us to prove that these interactions do not violate provided representation invariants.
HATs integrate cleanly within a reﬁnement type system, enjoy pleasant decidability properties,
and are amenable to a high-degree of automation.
   There are several interesting directions for future work. While the focus of this paper is the veri-
ﬁcation of representation invariants, there is no instrinsic requirement that HATs use the same au-
tomaton in their pre- and postcondition. We intend to explore more general veriﬁcation problems
under this relaxation. Another potential direction is extending our current formalization to sup-
port richer automata classes (e.g., symbolic visibly pushdown [D’Antoni and Alur 2014] or Büchi
automata), in order to support a larger class of safety properties, e.g., re-entrant properties of locks,
quantitative properties, and properties over inﬁnite traces) or more general categories of eﬀects,
e.g., control eﬀects [Bauer and Pretnar 2013]).

ACKNOWLEDGEMENTS
   We thank the anonymous reviewers for their detailed comments and suggestions, and Ashish
Mishra, Julia Belyakova, Patrick Lafontaine Yongwei Yuan (Purdue), John Wiegley (Kadena), and
Scott Moore (Galois) for numerous stimulating discussions. This material is based upon work sup-
ported by the Defense Advanced Research Projects Agency (DARPA) and Naval Information War-
fare Center Paciﬁc (NIWC Paciﬁc) under N6600 1-22-C-4027 and the National Science Foundation
under CCF-SHF 2321680.

REFERENCES
Martín Abadi, Andrew Birrell, Tim Harris, and Michael Isard. 2011.               Semantics of Transactional Memory
   and Automatic Mutual Exclusion.          ACM Trans. Program. Lang. Syst. 33, 1, Article 2 (jan 2011), 50 pages.
   https://doi.org/10.1145/1889997.1889999
Danel Ahman, Cătălin Hriţcu, Kenji Maillard, Guido Martínez, Gordon Plotkin, Jonathan Protzenko, Aseem Rastogi, and
   Nikhil Swamy. 2017. Dijkstra Monads for Free. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of
   Programming Languages (Paris, France) (POPL ’17). Association for Computing Machinery, New York, NY, USA, 515–529.
   https://doi.org/10.1145/3009837.3009878
Andrej Bauer and Matija Pretnar. 2013. An Eﬀect System for Algebraic Eﬀects and Handlers. In Algebra and Coalgebra in
   Computer Science, Reiko Heckel and Stefan Milius (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 1–16.
Eric Bodden and Laurie Hendren. 2012. The Clara framework for hybrid typestate analysis. International Journal on
   Software Tools for Technology Transfer 14 (2012), 307–326.
Nicolas Chappe, Paul He, Ludovic Henrio, Yannick Zakowski, and Steve Zdancewic. 2023. Choice Trees: Representing
   Nondeterministic, Recursive, and Impure Programs in Coq. Proc. ACM Program. Lang. 7, POPL, Article 61 (jan 2023),
   31 pages. https://doi.org/10.1145/3571254
Arthur Charguéraud, Jean-Christophe Filliâtre, Mário Pereira, and François Pottier. 2017. VOCAL – A Veriﬁed OCaml
   Library. ML Family Workshop.
Loris D’Antoni and Rajeev Alur. 2014. Symbolic Visibly Pushdown Automata. In Computer Aided Veriﬁcation, Armin Biere
   and Roderick Bloem (Eds.). Springer International Publishing, Cham, 209–225.

                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
24                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


Loris D’Antoni and Margus Veanes. 2014. Minimization of Symbolic Automata. SIGPLAN Not. 49, 1 (jan 2014), 541–553.
    https://doi.org/10.1145/2578855.2535849
Giuseppe De Giacomo and Moshe Y. Vardi. 2013. Linear Temporal Logic and Linear Dynamic Logic on Finite Traces. In
    Proceedings of the Twenty-Third International Joint Conference on Artiﬁcial Intelligence (Beijing, China) (IJCAI ’13). AAAI
    Press, 854–860.
Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In Tools and Algorithms for the Construction
    and Analysis of Systems, C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
    337–340. https://doi.org/10.1007/978-3-540-78800-3_24
Robert DeLine and Manuel Fähndrich. 2004.                 Typestates for Objects. In ECOOP 2004–Object-Oriented Pro-
    gramming: 18th European Conference, Oslo, Norway, June 14-18, 2004. Proceedings 18. Springer, 465–490.
    https://doi.org/10.1007/978-3-540-24851-4_21
Jana Dunﬁeld and Neel Krishnaswami. 2021. Bidirectional Typing. ACM Comput. Surv. 54, 5, Article 98 (may 2021), 38 pages.
    https://doi.org/10.1145/3450952
Loris D’Antoni and Margus Veanes. 2017. The Power of Symbolic Automata and Transducers. In Computer Aided Veriﬁ-
    cation: 29th International Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part I 30. Springer,
   47–67.
P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg, and P. Madhusudan. 2018. Horn-ICE learning for synthesizing
    invariants and contracts. Proc. ACM Program. Lang. 2, OOPSLA (2018), 131:1–131:25. https://doi.org/10.1145/3276501
Cormac Flanagan, Amr Sabry, Bruce F. Duba, and Matthias Felleisen. 1993. The Essence of Compiling with Continu-
    ations. In Proceedings of the ACM SIGPLAN 1993 Conference on Programming Language Design and Implementation
   (Albuquerque, New Mexico, USA) (PLDI ’93). Association for Computing Machinery, New York, NY, USA, 237–247.
    https://doi.org/10.1145/155090.155113
Aymeric Fromherz, Aseem Rastogi, Nikhil Swamy, Sydney Gibson, Guido Martínez, Denis Merigoux, and Tahina Ra-
    mananandro. 2021. Steel: proof-oriented programming in a dependently typed concurrent separation logic. Proc. ACM
    Program. Lang. 5, ICFP, Article 85 (aug 2021), 30 pages. https://doi.org/10.1145/3473590
David K. Giﬀord and John M. Lucassen. 1986. Integrating Functional and Imperative Programming. In Proceedings of the
    1986 ACM Conference on LISP and Functional Programming (Cambridge, Massachusetts, USA) (LFP ’86). Association for
    Computing Machinery, New York, NY, USA, 28–38. https://doi.org/10.1145/319838.319848
Colin S. Gordon. 2021. Polymorphic Iterable Sequential Eﬀect Systems. ACM Trans. Program. Lang. Syst. 43, 1, Article 4
   (apr 2021), 79 pages. https://doi.org/10.1145/3450272
John Hatcliﬀ and Olivier Danvy. 1994. A Generic Account of Continuation-Passing Styles. In Proceedings of the 21st ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Portland, Oregon, USA) (POPL ’94). Association
    for Computing Machinery, New York, NY, USA, 458–471. https://doi.org/10.1145/174675.178053
Hossein Hojjat and Philipp Rümmer. 2018. The ELDARICA Horn Solver. In 2018 Formal Methods in Computer Aided Design,
    FMCAD 2018, Austin, TX, USA, October 30 - November 2, 2018, Nikolaj S. Bjørner and Arie Gurﬁnkel (Eds.). IEEE, 1–7.
    https://doi.org/10.23919/FMCAD.2018.8603013
Kohei Honda. 1993. Types for Dyadic Interaction. In CONCUR’93, Eike Best (Ed.). Springer Berlin Heidelberg, Berlin,
    Heidelberg, 509–523.
Java 2013. Java Platform Standard Edition 7 Documentation. https://docs.oracle.com/javase/7/docs/
Ranjit Jhala and Niki Vazou. 2021. Reﬁnement Types: A Tutorial. Found. Trends Program. Lang. 6, 3-4 (2021), 159–317.
    https://doi.org/10.1561/2500000032
Shin-ya Katsumata. 2014. Parametric Eﬀect Monads and Semantics of Eﬀect Systems. In Proceedings of the 41st ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages (San Diego, California, USA) (POPL ’14). Associ-
    ation for Computing Machinery, New York, NY, USA, 633–645. https://doi.org/10.1145/2535838.2535846
Eric Koskinen and Tachio Terauchi. 2014. Local Temporal Reasoning. In Proceedings of the Joint Meeting of the Twenty-Third
    EACSL Annual Conference on Computer Science Logic (CSL) and the Twenty-Ninth Annual ACM/IEEE Symposium on Logic
    in Computer Science (LICS) (Vienna, Austria) (CSL-LICS ’14). Association for Computing Machinery, New York, NY, USA,
   Article 59, 10 pages. https://doi.org/10.1145/2603088.2603138
Yao Li and Stephanie Weirich. 2022. Program adverbs and Tlön embeddings. Proc. ACM Program. Lang. 6, ICFP, Article 101
   (aug 2022), 31 pages. https://doi.org/10.1145/3547632
Kenji Maillard, Danel Ahman, Robert Atkey, Guido Martínez, Cătălin Hriţcu, Exequiel Rivas, and Éric Tanter. 2019. Dijkstra
    Monads for All. Proc. ACM Program. Lang. 3, ICFP, Article 104 (jul 2019), 29 pages. https://doi.org/10.1145/3341708
Muhammad Zubair Malik, Aman Pervaiz, and Sarfraz Khurshid. 2007. Generating Representation Invariants of Structurally
    Complex Data. In Tools and Algorithms for the Construction and Analysis of Systems, 13th International Conference, TACAS
    2007, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2007 Braga, Portugal, March
    24 - April 1, 2007, Proceedings (Lecture Notes in Computer Science, Vol. 4424), Orna Grumberg and Michael Huth (Eds.).
    Springer, 34–49. https://doi.org/10.1007/978-3-540-71209-1_5


, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                             25


Anders Miltner, Saswat Padhi, Todd D. Millstein, and David Walker. 2020. Data-driven Inference of Representation In-
   variants. In Proceedings of the 41st ACM SIGPLAN International Conference on Programming Language Design and Im-
   plementation, PLDI 2020, London, UK, June 15-20, 2020, Alastair F. Donaldson and Emina Torlak (Eds.). ACM, 1–15.
   https://doi.org/10.1145/3385412.3385967
Alan Mycroft, Dominic Orchard, and Tomas Petricek. 2015. Eﬀect Systems Revisited–Control-Flow Algebra and Semantics.
   In Essays Dedicated to Hanne Riis Nielson and Flemming Nielson on the Occasion of Their 60th Birthdays on Semantics, Log-
   ics, and Calculi - Volume 9560. Springer-Verlag, Berlin, Heidelberg, 1–32. https://doi.org/10.1007/978-3-319-27810-0_1
Aleksandar Nanevski, Greg Morrisett, Avraham Shinnar, Paul Govereau, and Lars Birkedal. 2008b.                    Ynot: De-
   pendent Types for Imperative Programs. In Proceedings of the 13th ACM SIGPLAN International Conference
   on Functional Programming (ICFP ’08). Association for Computing Machinery, New York, NY, USA, 229–240.
   https://doi.org/10.1145/1411204.1411237
Aleksandar Nanevski, J. Gregory Morrisett, and Lars Birkedal. 2008a. Hoare Type Theory, Polymorphism and Separation.
   J. Funct. Program. 18, 5-6 (2008), 865–911. https://doi.org/10.1017/S0956796808006953
Yoji Nanjo, Hiroshi Unno, Eric Koskinen, and Tachio Terauchi. 2018. A Fixpoint Logic and Dependent Eﬀects for
   Temporal Property Veriﬁcation. In Proceedings of the 33rd Annual ACM/IEEE Symposium on Logic in Computer Sci-
   ence (Oxford, United Kingdom) (LICS ’18). Association for Computing Machinery, New York, NY, USA, 759–768.
   https://doi.org/10.1145/3209108.3209204
Chris Okasaki. 1999. Purely Functional Data Structures. Cambridge University Press, USA.
F. P. Ramsey. 1987.              On a Problem of Formal Logic.                  Birkhäuser Boston, Boston, MA, 1–24.
   https://doi.org/10.1007/978-0-8176-4842-8_1
Taro Sekiyama and Hiroshi Unno. 2023. Temporal Veriﬁcation with Answer-Eﬀect Modiﬁcation: Dependent Temporal
   Type-and-Eﬀect System with Delimited Continuations. Proc. ACM Program. Lang. 7, POPL, Article 71 (jan 2023), 32 pages.
   https://doi.org/10.1145/3571264
Christian Skalka and Scott Smith. 2004. History Eﬀects and Veriﬁcation. In Programming Languages and Systems, Wei-Ngan
   Chin (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 107–128.
Joshua Sunshine, Karl Naden, Sven Stork, Jonathan Aldrich, and Éric Tanter. 2011. First-Class State Change in Plaid.
   SIGPLAN Not. 46, 10 (oct 2011), 713–732. https://doi.org/10.1145/2076021.2048122
Nikhil Swamy, Guido Martinez, and Aseem Rastogi. 2023.                              Proof-Oriented Programming in F*.
   https://fstar-lang.org/tutorial/proof-oriented-programming-in-fstar.pdf
Nikhil Swamy, Aseem Rastogi, Aymeric Fromherz, Denis Merigoux, Danel Ahman, and Guido Martínez. 2020. SteelCore:
   an extensible concurrent separation logic for eﬀectful dependently typed programs. Proc. ACM Program. Lang. 4, ICFP,
   Article 121 (aug 2020), 30 pages. https://doi.org/10.1145/3409003
Nikhil Swamy, Joel Weinberger, Cole Schlesinger, Juan Chen, and Benjamin Livshits. 2013. Verifying Higher-Order Pro-
   grams with the Dijkstra Monad. In ACM SIGPLAN Conference on Programming Language Design and Implementa-
   tion, PLDI ’13, Seattle, WA, USA, June 16-19, 2013, Hans-Juergen Boehm and Cormac Flanagan (Eds.). ACM, 387–398.
   https://doi.org/10.1145/2491956.2491978
Ross Tate. 2013. The Sequential Semantics of Producer Eﬀect Systems. In Proceedings of the 40th Annual ACM SIGPLAN-
   SIGACT Symposium on Principles of Programming Languages (Rome, Italy) (POPL ’13). Association for Computing Ma-
   chinery, New York, NY, USA, 15–26. https://doi.org/10.1145/2429069.2429074
Anish Tondwalkar, Matthew Kolosick, and Ranjit Jhala. 2021. Reﬁnements of Futures Past: Higher-Order Speciﬁcation
   with Implicit Reﬁnement Types. In 35th European Conference on Object-Oriented Programming (ECOOP 2021) (Leibniz
   International Proceedings in Informatics (LIPIcs), Vol. 194), Anders Møller and Manu Sridharan (Eds.). Schloss Dagstuhl –
   Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 18:1–18:29. https://doi.org/10.4230/LIPIcs.ECOOP.2021.18
Vasco T. Vasconcelos. 2009. Fundamentals of Session Types. Springer Berlin Heidelberg, Berlin, Heidelberg, 158–186.
   https://doi.org/10.1007/978-3-642-01918-0_4
Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton-Jones. 2014. Reﬁnement Types for Haskell.
   SIGPLAN Not. 49, 9 (aug 2014), 269–282. https://doi.org/10.1145/2692915.2628161
Margus Veanes. 2013. Applications of Symbolic Finite Automata. In Implementation and Application of Automata, Stavros
   Konstantinidis (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 16–23.
Margus Veanes, Nikolaj Bjørner, and Leonardo de Moura. 2010. Symbolic Automata Constraint Solving. In Logic for Pro-
   gramming, Artiﬁcial Intelligence, and Reasoning, Andrei Fermüller, Christian G.and Voronkov (Ed.). Springer Berlin Hei-
   delberg, Berlin, Heidelberg, 640–654.
John Wiegley and Benjamin Delaware. 2017. Using Coq to write fast and correct Haskell. In Proceedings of the 10th ACM
   SIGPLAN International Symposium on Haskell (Oxford, UK) (Haskell 2017). Association for Computing Machinery, New
   York, NY, USA, 52–62. https://doi.org/10.1145/3122955.3122962
Li-yao Xia, Yannick Zakowski, Paul He, Chung-Kil Hur, Gregory Malecha, Benjamin C. Pierce, and Steve Zdancewic. 2019.
   Interaction trees: representing recursive and impure programs in Coq. Proc. ACM Program. Lang. 4, POPL, Article 51


                                                                 , Vol. 1, No. 1, Article . Publication date: September 2018.
26                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


  (dec 2019), 32 pages. https://doi.org/10.1145/3371119
Hengchu Zhang, Wolf Honoré, Nicolas Koh, Yao Li, Yishuai Li, Li-Yao Xia, Lennart Beringer, William Mansky, Benjamin
  Pierce, and Steve Zdancewic. 2021. Verifying an HTTP Key-Value Server with Interaction Trees and VST. In 12th Inter-
  national Conference on Interactive Theorem Proving (ITP 2021) (Leibniz International Proceedings in Informatics (LIPIcs),
  Vol. 193), Liron Cohen and Cezary Kaliszyk (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Ger-
  many, 32:1–32:19. https://doi.org/10.4230/LIPIcs.ITP.2021.32
Zhe Zhou, Robert Dickerson, Benjamin Delaware, and Suresh Jagannathan. 2021. Data-driven Abductive Inference of
  Library Speciﬁcations. Proc. ACM Program. Lang. 5, OOPSLA (2021), 1–29. https://doi.org/10.1145/3485493
He Zhu, Stephen Magill, and Suresh Jagannathan. 2018. A data-driven CHC solver. In Proceedings of the 39th ACM SIGPLAN
  Conference on Programming Language Design and Implementation, PLDI 2018, Philadelphia, PA, USA, June 18-22, 2018,
  Jeﬀrey S. Foster and Dan Grossman (Eds.). ACM, 707–721. https://doi.org/10.1145/3192366.3192416




, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                       27


A OPERATIONAL SEMANTICS
   The auxiliary big-step reduction rules for eﬀect operators and the small-step operational seman-
tics of our core language are shown in Fig. 10.

Auxiliary Operational Semantics                                                                                       𝛼  op 𝑣 ⇓ 𝑣
                (put 𝑘 𝑣 = () ) ∉ 𝛼 ′                     (put 𝑘 𝑣 = () ) ∉ 𝛼               (put 𝑘 𝑣 = () ) ∈ 𝛼
                                                 get                            existsF                            existsT
         𝛼 [put 𝑘 𝑣 = () ]     𝛼 ′  get 𝑘 ⇓ 𝑣           𝛼  exists𝑘 ⇓ false               𝛼  exists𝑘 ⇓ true

                         put      (insert 𝑛 = () ) ∈ 𝛼              insert 𝑛 = () ∉ 𝛼                                  insert
      𝛼  put 𝑘 𝑣 ⇓ ()                                   memT                             memF    𝛼  insert 𝑣 ⇓ ()
                                  𝛼  mem 𝑣 ⇓ true                𝛼  mem 𝑣 ⇓ false
                                                                                                                                𝛼
Operational Semantics                                                                                                          →𝑒
                                                                                                                        𝛼  𝑒 ↩−
                     𝑜𝑝 𝑣 ⇓ 𝑣𝑥                                                   𝛼  op 𝑣 ⇓ 𝑣𝑥
                                                   StPureOp                                                         StEffOp
                                 []                                                       [op 𝑣 = 𝑣𝑥 ]
       𝛼  let 𝑥 = 𝑜𝑝 𝑣 in 𝑒 ↩−→ 𝑒 [𝑥 ↦→ 𝑣𝑥 ]                     𝛼  let 𝑥 = op 𝑣 in 𝑒 ↩−−−−−−−→ 𝑒 [𝑥 ↦→ 𝑣𝑥 ]

                                      𝛼′
                             𝛼  𝑒1 ↩−→ 𝑒1′                                                                       StLetE2
                                                                StLetE1                          []
                                      𝛼′                                    𝛼  let 𝑦 = 𝑣 in 𝑒 ↩−→ 𝑒 [𝑦 ↦→ 𝑣 ]
         𝛼  (let 𝑦 = 𝑒1 in 𝑒2 ) ↩−→ (let 𝑦 = 𝑒1′ in 𝑒2 )

                                                                                              StLetAppLam
                                                           []
                     𝛼  (let 𝑦 = 𝜆𝑥:𝑡 .𝑒1 𝑣𝑥 in 𝑒2 ) ↩−→ (let 𝑦 = 𝑒1 [𝑥 ↦→ 𝑣𝑥 ] in 𝑒2 )

                                                                                                                  StLetAppFix
                                                  []
     𝛼  let 𝑦 = fix𝑓 :𝑡 .𝜆𝑥:𝑡𝑥 .𝑒1 𝑣𝑥 in 𝑒2 ↩−→ let 𝑦 = (𝜆𝑓 :𝑡 .𝑒1 [𝑥 ↦→ 𝑣𝑥 ] ) (fix𝑓 :𝑡 .𝜆𝑥:𝑡𝑥 .𝑒1 ) in 𝑒2

                                                                                          StMatch
                                                                       []
                                𝛼  match 𝑑𝑖 𝑣 𝑗 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 ↩−→ 𝑒𝑖 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]

                                                 Fig. 10. Operational Semantics




                                                                       , Vol. 1, No. 1, Article . Publication date: September 2018.
28                                                               Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


B BASIC TYPING RULES
   The basic typing rules of our core language and qualiﬁers are shown in Fig. 11 and Fig. 12. We
use an auxiliary function Ty to provide a basic type for the primitives of our language, e.g., con-
stants, built-in operators, and data constructors.

Basic Typing                                                                                                                                  Γ ⊢s 𝑒 : 𝑠

                                                BtConst          Γ (𝑥 ) = 𝑠                    Γ, 𝑥:⌊𝑡1 ⌋ ⊢s 𝑒 : 𝑠 2
                            Γ ⊢s 𝑐 : Ty(𝑐 )                                     BtVar                                    BtFun
                                                                 Γ ⊢s 𝑥 : 𝑠               Γ ⊢s 𝜆𝑥:𝑡1 .𝑒 : ⌊𝑡1 ⌋  𝑠 2

        Γ, 𝑓 :⌊𝑡1  𝑡2 ⌋ ⊢s 𝜆𝑥:𝑡1 .𝑒 : ⌊𝑡1  𝑡2 ⌋                   Ty(𝑜𝑝 ) = 𝑠𝑖  𝑠𝑥          ∀𝑖.Γ ⊢s 𝑣𝑖 : 𝑠𝑖    Γ, 𝑥:𝑠𝑥 ⊢s 𝑒 : 𝑠
                                                        BtFix                                                                          BtPureOp
        Γ ⊢s fix𝑓 :𝑡1  𝑡2 .𝜆𝑥:𝑡1 .𝑒 : ⌊𝑡1  𝑡2 ⌋                                   Γ ⊢s let 𝑥 = 𝑜𝑝 𝑣𝑖 in 𝑒 : 𝑠

Γ ⊢s 𝑣1 : 𝑠 2  𝑠𝑥         Γ ⊢s 𝑣2 : 𝑠 2     Γ, 𝑥:𝑠𝑥 ⊢s 𝑒 : 𝑠                 Ty(op) = 𝑠𝑖  𝑠𝑥        ∀𝑖.Γ ⊢s 𝑣𝑖 : 𝑠𝑖      Γ, 𝑥:𝑠𝑥 ⊢s 𝑒 : 𝑠
                                                                 BtApp                                                                         BtEffOp
              Γ ⊢s let 𝑥 = 𝑣1 𝑣2 in 𝑒 : 𝑠                                                   Γ ⊢s let 𝑥 = op 𝑣𝑖 in 𝑒 : 𝑠

          ∅ ⊢s 𝑒 1 : 𝑠 𝑥     Γ, 𝑥:𝑠𝑥 ⊢s 𝑒2 : 𝑠                   Γ ⊢s 𝑣 : 𝑠 𝑣     ∀𝑖, Ty(𝑑𝑖 ) = 𝑠 𝑗  𝑠 𝑣     Γ, 𝑦 𝑗 :𝑠 𝑗 ⊢s 𝑒𝑖 : 𝑠
                                                   BtLetE                                                                             BtMatch
             Γ ⊢s let 𝑥 = 𝑒1 in 𝑒2 : 𝑠                                        Γ ⊢s match 𝑣 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 : 𝑠

                                                          Fig. 11. Basic Typing Rules




Basic Qualiﬁer Typing                                                                                                        Γ ⊢s 𝑙 : 𝑠       Γ ⊢s 𝜙 : 𝑠
               Ty(𝑐 ) = 𝑠                           Γ (𝑥 ) = 𝑠                                        BtTop                           BtBot
                               BtLitConst                         BtLitVar         Γ ⊢s ⊤ : bool                 Γ ⊢s ⊥ : bool
               Γ ⊢s 𝑐 : 𝑠                          Γ ⊢s 𝑥 : 𝑠

Ty(𝑜𝑝 ) = 𝑠𝑖  𝑠           ∀𝑖.Γ ⊢s 𝑙𝑖 : 𝑠𝑖                 Ty(𝑚𝑝 ) = 𝑠𝑖  bool            ∀𝑖.Γ ⊢s 𝑙𝑖 : 𝑠𝑖                     Γ ⊢s 𝜙 : bool
                                              BtLitOp                                                        BtLitMp                             BtNeg
             Γ ⊢s 𝑜𝑝 𝑙𝑖 : 𝑠                                                   Γ ⊢s 𝑚𝑝 𝑙𝑖 : 𝑠                                 Γ ⊢s ¬𝜙 : bool

     Γ ⊢s 𝜙 1 : bool       Γ ⊢s 𝜙 2 : bool                 Γ ⊢s 𝜙 1 : bool        Γ ⊢s 𝜙 2 : bool                Γ, 𝑥:𝑏 ⊢s 𝜙 : bool
                                               BtAnd                                                  BtOr                                BtForall
           Γ ⊢s 𝜙 1 ∧ 𝜙 2 : bool                                   Γ ⊢s 𝜙 1 ∨ 𝜙 2 : bool                         Γ ⊢s ∀𝑥:𝑏.𝜙 : bool

                                                    Fig. 12. Basic Qualifier Typing Rules


, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                              29


C   DECLARATIVE TYPING RULES
  The full set of rules for our auxiliary typing relations are shown in Fig. 13, and the full set of
declarative typing rules are shown in Fig. 14. We elide the basic typing relation (∅ ⊢s 𝑒 : 𝑠 ) in the
premises of the rules in Fig. 14; which assume all terms have a basic type.


Well-Formed Types                                                                                      Γ ⊢WF 𝐴       Γ ⊢WF 𝑡       Γ ⊢WF 𝜏
          ⌊Γ⌋, 𝜈:𝑏 ⊢s 𝜙 : bool                    Γ ⊢WF 𝑡𝑥        Γ, 𝑥:⌊𝑡𝑥 ⌋ ⊢WF 𝑡                    Γ, 𝑥:𝑏 ⊢WF 𝑡
                                    WfBase                                              WfArr                           WfGhost
             Γ ⊢WF {𝜈:𝑏 | 𝜙}                             Γ ⊢WF 𝑥:𝑡𝑥  𝑡                              Γ ⊢WF 𝑥:𝑏 d 𝑡

            Ty(op) = 𝑥𝑖 :𝑏𝑖  𝑏        ⌊Γ⌋, 𝑥𝑖 :𝑏𝑖 , 𝜈:𝑏 ⊢s 𝜙 : bool                       ⌊Γ⌋ ⊢s 𝜙 : bool
                                                                        WfOpEvent                                 WfTestEvent
                             Γ ⊢WF hop xi = 𝜈 | 𝜙 i                                           Γ ⊢WF h𝜙 i

                     Γ ⊢WF 𝐴                 Γ ⊢WF 𝐴1       Γ ⊢WF 𝐴2                    Γ ⊢WF 𝐴1       Γ ⊢WF 𝐴2
                                 WfNeg                                     WfAnd                                     WfOr
                    Γ ⊢WF ¬𝐴                      Γ ⊢WF 𝐴   1 ∧ 𝐴2                          Γ ⊢WF 𝐴   1 ∨ 𝐴2


             Γ ⊢WF 𝐴1        Γ ⊢WF 𝐴2                       Γ ⊢WF 𝐴                      Γ ⊢WF 𝐴1       Γ ⊢WF 𝐴2
                                         WfConcat                          WfNext                                    WfUntil
                    Γ ⊢WF 𝐴1 ; 𝐴2                         Γ ⊢WF        𝐴                     Γ ⊢WF 𝐴1 U 𝐴2

          Γ ⊢WF 𝐴 Γ ⊢WF 𝐵 Γ ⊢WF 𝑡
                                                                               Γ ⊢WF 𝜏1      Γ ⊢WF 𝜏2       ⌊𝜏1 ⌋ = ⌊𝜏2 ⌋
      ∀𝜎 ∈ JΓK.L (𝜎 (𝐵) ) ⊆ L (𝜎 (𝐴; h⊤i ) )                                                                                   WFInter
                                                        WFHoare                             Γ ⊢WF 𝜏1 ⊓ 𝜏2
                     Γ ⊢WF [𝐴] 𝑡 [𝐵]

Automata Inclusion                                    Γ ⊢𝐴 ⊆𝐴            Subtyping                                 Γ ⊢ 𝑡 <: 𝑡     Γ ⊢ 𝜏 <: 𝜏
                                                                           Γ ⊢ 𝐴2 ⊆ 𝐴1 Γ ⊢ 𝑡1 <: 𝑡2
                           ∀𝜎 ∈ JΓK.
                                                                             Γ ⊢ (𝐴2 ; h⊤i ) ∧ 𝐵 1 ⊆
                    L (𝜎 (𝐴1 ) ) ⊆ L (𝜎 (𝐴2 ) )
                                                  SubAutomata                    (𝐴2 ; h⊤i ) ∧ 𝐵 2
                          Γ ⊢ 𝐴1 ⊆ 𝐴2                                                                             SubHoare
                                                                         Γ ⊢ [𝐴1 ] 𝑡1 [𝐵 1 ] <: [𝐴2 ] 𝑡2 [𝐵 2 ]

                     SubIntLL                         SubIntLR                                                                  SubIntMerge
Γ ⊢ 𝜏1 ⊓ 𝜏2 <: 𝜏1                 Γ ⊢ 𝜏1 ⊓ 𝜏2 <: 𝜏2                    Γ ⊢ [𝐴1 ] 𝑡 [𝐵] ⊓ [𝐴2 ] 𝑡 [𝐵] <: [𝐴1 ∨ 𝐴2 ] 𝑡 [𝐵]


        Γ ⊢ 𝜏 <: 𝜏1                     Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑡1 <: 𝑡2                             ∃𝑣.⌊Γ⌋ ⊢s 𝑣 : 𝑏
        Γ ⊢ 𝜏 <: 𝜏2                                                  SubGhostR              Γ ⊢ 𝑡1 [𝑥 ↦→ 𝑣 ] <: 𝑡2
                           SubIntR         Γ ⊢ 𝑡1 <: 𝑥:𝑏 d 𝑡2                                                               SubGhostL
      Γ ⊢ 𝜏 <: 𝜏1 ⊓ 𝜏2                                                                       Γ ⊢ 𝑥:𝑏 d 𝑡1 <: 𝑡2

                                               Fig. 13. Full auxiliary typing rules.




                                                                            , Vol. 1, No. 1, Article . Publication date: September 2018.
30                                                     Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


Typing                                                                             Γ ⊢ 𝑜𝑝 : 𝑡      Γ ⊢ op : 𝑡       Γ ⊢𝑒 :𝑡        Γ ⊢𝑒 :𝜏

            Γ ⊢WF {𝜈:𝑏 | 𝜈 = 𝑥 }                       Γ ⊢WF 𝑧:𝑡  𝜏                         Γ ⊢WF {𝜈:𝑏 | 𝜈 = 𝑐}
             (𝑥, {𝜈:𝑏 | 𝜙}) ∈ Γ                       (𝑥, 𝑧:𝑡  𝜏 ) ∈ Γ                          ∅ ⊢s 𝑐 : 𝑏
                                      TBaseVar                             TFuncVar                                    TConst
            Γ ⊢ 𝑥 : {𝜈:𝑏 | 𝜈 = 𝑥 }                    Γ ⊢ 𝑥 : 𝑧:𝑡  𝜏                        Γ ⊢ 𝑐 : {𝜈:𝑏 | 𝜈 = 𝑐}

      Γ ⊢WF 𝑡                 Γ ⊢WF 𝑡                Γ ⊢WF 𝑡2 Γ ⊢ 𝑡1 <: 𝑡2                       Γ ⊢WF 𝑡2 Γ ⊢ 𝑡1 <: 𝑡2
     Δ(𝑜𝑝 ) = 𝑡              Δ(op) = 𝑡                    Γ ⊢ 𝑜𝑝 : 𝑡1                                 Γ ⊢ op : 𝑡1
                    TPOp                    TEOp                                 TSubPOp                                          TSubEOp
     Γ ⊢ 𝑜𝑝 : 𝑡               Γ ⊢ op : 𝑡                   Γ ⊢ 𝑜𝑝 : 𝑡2                                  Γ ⊢ op : 𝑡2

                  Γ ⊢WF 𝜏2 Γ ⊢ 𝜏1 <: 𝜏2              Γ ⊢WF 𝑡2 Γ ⊢ 𝑡1 <: 𝑡2                         Γ ⊢WF 𝐴
                        Γ ⊢ 𝑒 : 𝜏1                         Γ ⊢ 𝑒 : 𝑡1                              Γ⊢𝑒 :𝑡
                                             TSub                                 TSubPP                              TEPur
                        Γ ⊢ 𝑒 : 𝜏2                           Γ ⊢ 𝑒 : 𝑡2                         Γ ⊢ 𝑒 : [𝐴] 𝑡 [𝐴]

                  Γ ⊢WF 𝜏1 ⊓ 𝜏2                         Γ ⊢WF 𝑥:𝑏 d 𝑡                           Γ ⊢WF 𝑥:𝑡𝑥  𝜏
              Γ ⊢ 𝑒 : 𝜏1 Γ ⊢ 𝑒 : 𝜏2                  Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑣 : 𝑡                      Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : 𝜏
                                           TInter                              TGhost                                      TFun
                    Γ ⊢ 𝑒 : 𝜏1 ⊓ 𝜏2                    Γ ⊢ 𝑣 : 𝑥:𝑏 d 𝑡                     Γ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 : 𝑥:𝑡𝑥  𝜏

              Γ ⊢WF 𝜏 Γ ⊢ 𝑜𝑝 : 𝑧𝑖 :𝑡𝑖  𝑡                            Γ ⊢WF [𝐴] 𝑡 [𝐵] Γ ⊢ op : 𝑧𝑖 :𝑡𝑖  𝜏
                     ∀𝑖.Γ ⊢ 𝑣𝑖 : 𝑡𝑖                                              ∀𝑖.Γ ⊢ 𝑣𝑖 : 𝑡𝑖
                  𝑡𝑥 = 𝑡 [𝑧𝑖 ↦→ 𝑣𝑖 ]                                     [𝐴] 𝑡𝑥 [𝐴′ ] = 𝜏 [𝑧𝑖 ↦→ 𝑣𝑖 ]
                    Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : 𝜏                                        Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : [𝐴′ ] 𝑡 [𝐵]
                                                    TPOpApp                                                           TEOpApp
                  Γ ⊢ let 𝑥 = 𝑜𝑝 𝑣𝑖 in 𝑒 : 𝜏                            Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴] 𝑡 [𝐵]

                    Γ ⊢WF [𝐴] 𝑡 [𝐵] Γ ⊢ 𝑣1 : 𝑦:𝑡2  𝜏
                                                                                      Γ ⊢WF [𝐴] 𝑡 [𝐵]
                                Γ ⊢ 𝑣2 : 𝑡2
                                                                                   Γ ⊢ 𝑒𝑥 : [𝐴] 𝑡𝑥 [𝐴′ ]
                        [𝐴] 𝑡𝑥 [𝐴′ ] = 𝜏 [𝑦 ↦→ 𝑣2 ]
                                                                                  Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : [𝐴′ ] 𝑡 [𝐵]
                         Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 : [𝐴′ ] 𝑡 [𝐵]                                                                    TLetE
                                                                 TApp         Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 : [𝐴] 𝑡 [𝐵]
                     Γ ⊢ let 𝑥 = 𝑣1 𝑣2 in 𝑒 : [𝐴] 𝑡 [𝐵]

                         Γ ⊢WF 𝜏 ∀𝑖.Δ(𝑑𝑖 ) = 𝑦 𝑗 :𝑡 𝑗  {𝜈:𝑏 | 𝜙𝑖 }                                      Γ ⊢WF 𝑡
             Γ, 𝑦 𝑗 :𝑡 𝑗 , 𝑧:{𝜈:𝑏 | 𝜈 = 𝑣 ∧ 𝜙𝑖 } ⊢ 𝑒𝑖 : 𝜏 where 𝑧 is fresh                        Γ, 𝑓 :𝑡 ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 : 𝑡
                                                                                  TMatch                                     TFix
                           Γ ⊢ (match 𝑣 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 ) : 𝜏                                  Γ ⊢ fix𝑓 :𝑡 .𝜆𝑥:𝑡𝑥 .𝑒 : 𝑡

                                                       Fig. 14. Type rules.




D TYPING ALGORITHM
   In this section, we provide the details of our typing algorithm. The full set of bi-directional typing
rules for this algorithm are shown in Fig. 15; again, we again omit the basic typing relation (∅ ⊢s
𝑒 : 𝑠 ) in the precondition of these rules. The detail of alphabet transformation (AlphaTrans) and
SFA instantiation (Abduce) procedures are provided in Algorithm 2 and Algorithm 3, respectively.

   Alphabet Transformation. The alphabet transformation function AlphaTrans translates a SFA
into a FA that shares the same regular operators. Notably, the alphabet transformation for eﬀect
events gathers all minterms that can imply the qualiﬁer of the eﬀect event (line 17); moreover, the
eﬀect event hop xi = 𝜈 | 𝜙i requires the gathered minterms have the same operator (op).

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                               31


Type Synthesis                         Γ ⊢𝑒 ⇒𝑡       Γ ⊢𝑒 ⇒𝜏                    Type Check                        Γ ⊢𝑒 ⇐𝑡         Γ ⊢𝑒 ⇐𝜏
                    ∅ ⊢WF {𝜈:𝑏 | 𝜈 = 𝑐}                        Γ ⊢WF {𝜈:𝑏 | 𝜈 = 𝑥}       (𝑥, {𝜈:𝑏 | 𝜙}) ∈ Γ
                                              SynConst                                                          SynBaseVar
                 Γ ⊢[𝐴] 𝑐 ⇒ {𝜈:𝑏 | 𝜈 = 𝑐}                              Γ ⊢[𝐴] 𝑥 ⇒ {𝜈:𝑏 | 𝜈 = 𝑥}


      Γ ⊢WF 𝑦:𝑏 d 𝑧:𝑡  𝜏                                                                                Γ ⊢WF 𝜏1 ⊓ 𝜏2
                                                           Γ ⊢WF 𝑥:𝑏 d 𝜏
     (𝑥, 𝑦:𝑏 d 𝑧:𝑡  𝜏 ) ∈ Γ                                                                              Γ ⊢ 𝑒 ⇐ 𝜏1
                                                       Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑒 ⇐ 𝜏
                                       SynFuncVar                                  ChkGhost               Γ ⊢ 𝑒 ⇐ 𝜏2
   Γ ⊢[𝐴] 𝑥 ⇒ 𝑦:𝑏 d 𝑧:𝑡  𝜏                              Γ ⊢ 𝑒 ⇐ 𝑥:𝑏 d 𝜏                                                         ChkInter
                                                                                                        Γ ⊢ 𝑒 ⇐ 𝜏1 ⊓ 𝜏2

                     Γ ⊢WF [𝐴] 𝑡 [𝐵]                                              Γ ⊢WF [𝐴] 𝑡 [𝐵]
                                                                                d                          Ô
                       Γ ⊢ 𝑣𝑥 ⇒ 𝑡𝑥                                  Γ ⊢ 𝑒𝑥 ⇒ [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] Γ ⊢ 𝐴 ⊆ 𝐴𝑖
                 Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 ⇐ [𝐴] 𝑡 [𝐵]                             ∀𝑖.Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
                                                     ChkLetV                                                             ChkLetE
           Γ ⊢ let 𝑥 = 𝑣𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]                               Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]

                                                                 Γ ⊢WF [𝐴] 𝑡 [𝐵]         Δ(op) = 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥
           Γ ⊢WF [𝐴] 𝑡 [𝐵]                                                           ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗
         Δ(𝑜𝑝 ) = 𝑦 𝑗 :𝑡 𝑗  𝑡𝑥
                                                                        Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
           ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗                                              d
                                                                              [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]
       Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
                                            ChkPOpApp             ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
 Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]                                                                                              ChkEOpApp
                                                                         Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]

       Γ ⊢WF [𝐴] 𝑡 [𝐵]         Γ ⊢ 𝑣1 ⇒ 𝑧𝑘 :𝑏𝑘 d 𝑦:𝑡 𝑦  𝜏𝑥
                              Γ ⊢ 𝑣2 ⇐ 𝑡 𝑦
                                                                                   Γ ⊢WF 𝑥:𝑡𝑥′  𝜏 Γ ⊢ 𝑡𝑥′ <: 𝑡𝑥
               Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦:𝑡 𝑦  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
                   d                                                                      Γ, 𝑥:𝑡𝑥′ ⊢ 𝑒 ⇐ 𝜏
                     [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 ↦→ 𝑣𝑦 ]                                                                           ChkFunc
         ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]                           Γ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑥:𝑡𝑥′  𝜏
                                                                  ChkApp
                Γ ⊢ let 𝑥 = 𝑣1 𝑣2 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]

     Γ ⊢WF 𝑡 𝑓′      Γ ⊢ 𝑡 𝑓′ <: 𝑡 𝑓                                      ∀𝑖.(𝑑𝑖 , 𝑦 𝑗 :𝑡 𝑗  {𝜈:𝑏 | 𝜙𝑖 }) ∈ Δ
      Γ, 𝑓 :𝑡 𝑓′ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′                     Γ, 𝑦 𝑗 :𝑡 𝑗 , 𝑧:{𝜈:𝑏 | 𝜈 = 𝑣 ∧ 𝜙𝑖 } ⊢ 𝑒𝑖 ⇐ 𝜏         where 𝑧 is fresh
                                         ChkFix                                                                                  ChkMatch
    Γ ⊢ fix𝑓 :𝑡 𝑓 .𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′                                  Γ ⊢ match 𝑣 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 ⇐ 𝜏


                          Γ ⊢WF [𝐴2 ] 𝑡2 [𝐵 2 ]
                Γ ⊢ 𝑒 ⇒ [𝐴1 ] 𝑡1 [𝐵 1 ] Γ ⊢ 𝐴2 <: 𝐴1                              Γ ⊢WF 𝑡 Γ ⊢ 𝑣 ⇒ 𝑡 ′
                             Γ ⊢ 𝑡1 <: 𝑡2                                              Γ ⊢ 𝑡 ′ <: 𝑡
               Γ ⊢ (𝐴2 ; h⊤i ) ∧ (𝐴2 ; h⊤i ) ∧𝐵 1 ⊆ 𝐵 2                                                           ChkSubV
                                                               ChkSub                  Γ ⊢𝑣⇐𝑡
                           Γ ⊢ 𝑒 ⇐ [𝐴2 ] 𝑡2 [𝐵 2 ]

                                               Fig. 15. Bidirectional Typing Rules



    Ghost Variable Instantiatation. As we show in Algorithm 3, the abductive synthesizer Abduce
adapts an existing algorithm [Zhou et al. 2021] that synthesizes a maximal assignment of un-
known qualiﬁer 𝜙𝑖 for the given ghost variables 𝑥𝑖 :𝑏𝑖 . These inferred qualiﬁers are strong enough
to prove the given inclusion relation between two input automata under the given type context
(i.e., Γ ⊢ 𝐴 ⊆ 𝐴′ ). Note that the ghost variables only make sense when the inclusion relation
holds with all unknown formulae 𝜙𝑖 are maximally weak (i.e., true) (line 2). Similar to the minterm
algorithm in Algorithm 2, the abductive algorithm gathers all literals that appear in the pre- and

                                                                           , Vol. 1, No. 1, Article . Publication date: September 2018.
32                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


 Algorithm 2: Alphabet Transformation
1  Procedure AlphaTrans (𝑀, 𝐴) :=
 2    match 𝐴:
 3        case ∅ or 𝜖 or • do return 𝐴;
 4        case hop xi = 𝜈 | 𝜙i or h𝜙i do
 5            𝑀 ′ ← {hop xi = 𝜈 | 𝜙 ′ i ∈ 𝑀 | 𝜙 ′ =⇒ 𝜙 };
                       Ô
 6            return 𝑚∈𝑀 ′ Hash(𝑚)
 7           case 𝐴1 ; 𝐴2 do return AlphaTrans (𝑀, 𝐴1 ); AlphaTrans (𝑀, 𝐴2 );
 8           case 𝐴1 ∨ 𝐴2 do return AlphaTrans (𝑀, 𝐴1 ) ∨ AlphaTrans (𝑀, 𝐴2 );
 9           case 𝐴1 ∧ 𝐴2 do return AlphaTrans (𝑀, 𝐴1 ) ∧ AlphaTrans (𝑀, 𝐴2 );
10           case 𝐴1 \ 𝐴2 do return AlphaTrans(𝑀, 𝐴1 ) \ AlphaTrans (𝑀, 𝐴2 );
11           case 𝐴∗ do return AlphaTrans(𝑀, 𝐴1 ) ∗ ;



 Algorithm 3: Ghost Variable Inference
1  Procedure Abduce(Γ, 𝐴, 𝐴′ , 𝑥𝑖 :𝑏𝑖 ) :=
 2    if Γ, 𝑥𝑖 :{𝜈:𝑏𝑖 | ⊤} 0 𝐴 ⊆ 𝐴′ then return ⊥ ;
 3    𝐿 ← GetLits(Γ, 𝐴 ∨ 𝐵);
               Ð
 4    𝑀 ? ← 𝑖 BoolComb(𝐿 ∪ 𝑥𝑖 );
 5    𝑀 + ← ∅; 𝑀 − ← ∅; 𝜙 ← ⊤;
 6    while ∃𝑚 ∈ 𝑀 ? .𝑚 =⇒ 𝜙 do
 7         𝑀 ? ← 𝑀 ? \ {𝑚};
 8         𝜙 ′ ← Synthesize (𝑀 + ∪ 𝑀 ? , 𝑀 − ∪ {𝑚});
 9         if Γ, 𝑥𝑖 :{𝜈:𝑏𝑖 | ⊤}, 𝑧:{𝜈:unit | 𝜙 ′ } 0 𝐴 ⊆ 𝐴′ then
10               𝑀 − ← 𝑀 − ∪ {𝑚};
11               𝜙 ← 𝜙′;
12         else 𝑀 + ← 𝑀 + ∪ {𝑚} ;
13      foreach 𝑥𝑖 :𝑏𝑖 do
14          𝑀 ← {𝑚 ∈ BoolComb(𝐿Γ ∪ 𝑥𝑖 ) | 𝑚 =⇒ 𝜙 };
                        Ô
15          𝑡𝑖 ← {𝜈:𝑏𝑖 | 𝑚∈𝑀 𝑚 [𝑥𝑖 ↦→ 𝜈]};
16      return 𝑥𝑖 :𝑡𝑖 ;



post-condition automata and type context (line 3) that will be used to generate candidate minterms
(feature vectors, in the literature of abductive synthesis [Zhou et al. 2021]), to build the hypothesis
space for synthesis. The function Abduce uses a counterexample-guided reﬁnement loop (line 6
- 12) adapted from the existing algorithm [Zhou et al. 2021] manipulating three sets of minterms:
unknown minterms 𝑀 ? , positive minterms 𝑀 + , and negative minterms 𝑀 − . Thanks to the multi-
abduction approach from the existing algorithm [Zhou et al. 2021], inferring a formula 𝜙 from
the union of all minterms induces all the assignment of unknown qualiﬁers 𝜙𝑖 at one shot. The
auxiliary synthesizer Synthesize (line 8) returns a formula that can be implied by given positive
minterm and unknown minterms but cannot be implied by any given negative minterms. Follow-
ing the existing algorithm [Zhou et al. 2021], function Synthesize is implemented as a Decision
Tree (DT) that classiﬁes these two sets of minterms. On the other hand, the inclusion query on line
9 decides if unknown minterms should be positive or negative; it also guarantees the soundness of
the algorithm, that is, a synthesized type is always consistent with the given automaton 𝐴 and 𝐴′ .

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                         33


Finally, the function Abduce returns reﬁnement type {𝜈:𝑏𝑖 | 𝜙𝑖 } for each ghost variable 𝑥𝑖 , where 𝜙𝑖
is the union of all local minterms that can imply 𝜙 (line 14 - 15).




                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
34                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


E PROOFS
  Type Soundness. The Coq formalization of our core language, typing rules, and the proof of
Theorem 4.8 and Corollary 4.9 are available on Zenodo
  https://doi.org/10.5281/zenodo.10806686
  Soundness of Algorithmic Typing. We present the proof for Theorem 5.1 from Sec. 5. The proof
requires the following lemmas about the SFAInclusion subroutine and the instantiation function
Abduce.
     Lemma E.1. [Soundness of Inclusion Algorithm] Given type context Γ , automaton 𝐴 and 𝐴′ ,
                                        SFAInclusion (Γ, 𝐴, 𝐴′ ) =⇒ Γ ⊢ 𝐴 ⊆ 𝐴′

  Lemma E.2. [Soundness of Instantiation Function] Given a type context Γ , ghost variables 𝑥𝑖 :𝑏𝑖 ,
automaton 𝐴 and 𝐴′ ,
                                 Abduce(Γ, 𝐴, 𝐴′, 𝑥𝑖 :𝑏𝑖 ) =⇒ Γ, 𝑥𝑖 :{𝜈:𝑏𝑖 | 𝜙𝑖 } ⊢ 𝐴 ⊆ 𝐴′

  The soundness of SFAInclusionestablishes that it is safe to treat the subtyping relation in our
typing algorithm as in declarative type system. On the other hand, the soundness of instantiation
function induces the following lemma.
   Lemma E.3. [Instantiation Implies Precondition Automata Inclusion] Given a type context Γ , term
                                                                                         d
𝑒, consider the following the reﬁnement type that has ghost variables 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ],
                                                                           Ü
Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] ≈›𝑧𝑘 :𝑡𝑘 =⇒ Γ, 𝑧𝑘 :𝑡𝑘 ⊢ 𝐴 ⊆          𝐴𝑖 ∧
                                                         Γ, 𝑧𝑘 :𝑡𝑘 ⊢ 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] <: 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]

  We need three auxiliary lemmas about declarative typing, which establish that we can drop
unused binding from the type context, well-typed substitution preserves typing judgement, and
well-formedness implies subtyping.
  Lemma E.4. [Strengthening] Given a type context Γ , term 𝑒 and HAT 𝜏 , for any free variable 𝑥 and
pure reﬁnement type 𝑡 : Γ, 𝑥:𝑡 ⊢ 𝑒 : 𝜏 ∧ Γ ⊢WF 𝜏 =⇒ Γ ⊢ 𝑒 : 𝜏
  Lemma E.5. [Substitution Preserves Typing] Given a type context Γ , term 𝑒 and HAT 𝜏 , for any free
variable 𝑥 and pure reﬁnement type 𝑡 : Γ, 𝑥:𝑡 ⊢ 𝑒 : 𝜏 ∧ Γ ⊢ 𝑣 : 𝑡 =⇒ Γ ⊢ 𝑒 : 𝜏 [𝑥 ↦→ 𝑣]
  Lemma E.6. [Well-formedness implies Subtyping] Given a type context Γ , term 𝑒 and HAT [𝐴] 𝑡 [𝐵],
we have Γ ⊢WF [𝐴] 𝑡 [𝐵] =⇒ Γ ⊢ [𝐴] 𝑡 [𝐵] <: [𝐴 ∧ 𝐴′ ] 𝑡 [𝐵 ∧ (𝐴′ ; h⊤i)].
     Proof. Consider the denotation of HAT [𝐴] 𝑡 [𝐵] and [𝐴 ∧ 𝐴′ ] 𝑡 [𝐵 ∧ (𝐴′ ; h⊤i)]:
                                                                                          𝛼′
                      J[𝐴] 𝑡 [𝐵]K = {𝑒 | ∅ ⊢s 𝑒 : ⌊𝑡 ⌋ ∧ ∀𝛼 𝛼 ′ 𝑣. 𝛼 ∈ L (𝐴) ∧ 𝛼  𝑒 ↩−→∗ 𝑣 =⇒ 𝑣 ∈ J𝑡K ∧ 𝛼 𝛼 ′ ∈ L (𝐵) }
                                                                                                𝛼′
  J[𝐴 ∧ 𝐴′ ] 𝑡 [𝐵 ∧ (𝐴′ ; h⊤i )]K = {𝑒 | ∅ ⊢s 𝑒 : ⌊𝑡 ⌋ ∧ ∀𝛼 𝛼 ′ 𝑣. 𝛼 ∈ L (𝐴 ∧ 𝐴′ ) ∧ 𝛼  𝑒 ↩−→∗ 𝑣 =⇒
                                            𝑣 ∈ J𝑡K ∧ 𝛼 𝛼 ′ ∈ L (𝐵 ∧ (𝐴′ ; h⊤i ) ) }
                                                                                                                               𝛼′
Consider a trace 𝛼 ∈ L (𝐴 ∧ 𝐴′ ), it also can be recognized by automata 𝐴, thus for any 𝛼  𝑒 ↩−  →∗ 𝑣,
               ′                                      ′
we have 𝛼 𝛼 ∈ L (𝐵). Moreover, the trace 𝛼 𝛼 has a preﬁx 𝛼, thus is naturally recognized
by automata (𝐴 ∧ 𝐴′ ); h⊤i. Thus, we know 𝛼 𝛼 ′ ∈ L ((𝐴 ∧ 𝐴′ ); h⊤i ∧ 𝐵). Note that the rule
WFHoare requires that precondition is always the “preﬁx” of the postcondition automata, thus
Γ ⊢WF [𝐴] 𝑡 [𝐵] implies (𝐴; h⊤i) ⊆ 𝐵, which means that L ((𝐴 ∧ 𝐴′ ); h⊤i ∧ 𝐵) = L (𝐴′ ; h⊤i ∧ 𝐵).
Thus the term 𝑒 is in the denotation of type [𝐴 ∧ 𝐴′ ] 𝑡 [𝐵 ∧ (𝐴′ ; h⊤i)] when it is in the denotation
of type [𝐴] 𝑡 [𝐵].                                                                                    

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                35


   Now we can prove the soundness theorem of our typing algorithm with respect to our declara-
tive type system. As the type synthesis rules are deﬁned mutually recursively, we simultaneously
prove both are correct. The following theorem states a stronger inductive invariant that is suﬃ-
cient to prove the soundness of the typing algorithm.

   Theorem E.7. [Soundness of the type synthesis and type check algorithm] For all type context Γ,
term 𝑒, pure reﬁnement type 𝑡 and HAT 𝜏,

                                                   Γ ⊢ 𝑒 ⇐ 𝜏 =⇒ Γ ⊢ 𝑒 : 𝜏
                                                   Γ ⊢ 𝑒 ⇐ 𝑡 =⇒ Γ ⊢ 𝑒 : 𝑡
                                                   Γ ⊢ 𝑒 ⇒ 𝜏 =⇒ Γ ⊢ 𝑒 : 𝜏
                                                   Γ ⊢ 𝑒 ⇒ 𝑡 =⇒ Γ ⊢ 𝑒 : 𝑡

   Proof. We proceed by induction over the mutual recursive structure of type synthesis ( ⇒ ) and
type check ( ⇐ ) rules. In the cases for; synthesis and checking rules of rule SynConst, SynBa-
seVar, SynFuncVar, ChkGhost, ChkInter, ChkFunc, ChkFix, ChkMatch, the typing rules in
Fig. 14 align exactly with these rules. There are seven remaining cases that are about let-bindings
(ChkLetV and ChkLetE), application (ChkApp, ChkPOpApp, and ChkEOpApp), and subtyping
(ChkSubV and ChkSub). The rule ChkLetV, ChkPOpApp, and ChkSubV are less interesting,
which are similar with standard reﬁnement typing algorithm[Jhala and Vazou 2021] and simply
drop the pre- and post-condition automata from their eﬀectful version. Consequently, we show the
proof of three interesting cases (ChkSub, ChkLetE, ChkEOpApp) below, where the case ChkApp
is almost the same as ChkEOpApp.
Case ChkSub:
       Γ ⊢WF [𝐴2 ] 𝑡2 [𝐵 2 ] Γ ⊢ 𝑒 ⇒ [𝐴1 ] 𝑡1 [𝐵 1 ]
              Γ ⊢ 𝐴2 <: 𝐴1 Γ ⊢ 𝑡1 <: 𝑡2
        Γ ⊢ (𝐴2 ; h⊤i ) ∧ 𝐵 1 ⊆ (𝐴2 ; h⊤i ) ∧ 𝐵 2
                                                          ChkSub
                  Γ ⊢ 𝑒 ⇐ [𝐴2 ] 𝑡2 [𝐵 2 ]
       This rule connects the relation between the type synthesis and type check judgement. From
       the induction hypothesis and the precondition of ChkSub, we know

                      Γ ⊢ 𝐴2 <: 𝐴1                                   from precondition                                       (1)
                      Γ ⊢ 𝑡1 <: 𝑡2                                   from precondition                                       (2)
                      Γ ⊢ (𝐴2 ; h⊤i ) ∧ 𝐵 1 ⊆ (𝐴2 ; h⊤i ) ∧ 𝐵 2    from precondition                                       (3)
                      Γ ⊢ [𝐴1 ] 𝑡1 [𝐵 1 ] <: [𝐴2 ] 𝑡2 [𝐵 2 ]         via rule SubHoare and (1) (2) (3)                       (4)
                      Γ ⊢ 𝑒 : [𝐴1 ] 𝑡1 [𝐵 1 ]                        inductive hypothesis                                    (5)
                      Γ ⊢ 𝑒 : [𝐴2 ] 𝑡2 [𝐵 2 ]                        via rule TSub and (4) (5)                               (6)


       Then the proof immediate holds in this case.

Case ChkLetE:
                      Γ ⊢WF [𝐴] 𝑡 [𝐵]
                    d                         Ô
        Γ ⊢ 𝑒𝑥 ⇒ [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] Γ ⊢ 𝐴 ⊆ 𝐴𝑖
                                         ′
         ∀𝑖.Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖 ] 𝑡 [𝐵]
                                                          ChkLetE
            Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       This rule can be treated as a combination of subtyping of intersection types (e.g., SubIntLL)

                                                                    , Vol. 1, No. 1, Article . Publication date: September 2018.
36                                                     Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


       and TLet. From the induction hypothesis and the precondition of ChkApp, we know
                               l
                    Γ ⊢ 𝑒𝑥 :    [𝐴𝑖 ] 𝑡 [𝐴𝑖′ ]                       inductive hypothesis                               (1)
                    ∀𝑖.Γ ⊢ 𝑒𝑥 : [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]                      via rule TSub, rule SubIntLL and (1)               (2)
                    ∀𝑖.Γ ⊢ 𝑒𝑥 : [𝐴 ∧ 𝐴𝑖 ] 𝑡𝑖 [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ]     via Lemma E.6, precondition, and (2)               (3)
                    ∀𝑖.Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 : [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]       inductive hypothesis                               (4)
                    ∀𝑖.Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 : [𝐴 ∧ 𝐴𝑖′ ] 𝑡 [𝐵]        rule TLet and (3) (4)                              (5)
                                          l
                    Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 :   [𝐴 ∧ 𝐴𝑖 ] 𝑡 [𝐵]          rule TInter and (5)                                (6)
                                               Ü
                    Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 : [𝐴 ∧   𝐴𝑖 ] 𝑡 [𝐵]          via rule TSub, rule SubIntMerge and (6)            (7)
                             Ü
                    Γ⊢𝐴 ⊆       𝐴𝑖                                   precondition                                       (8)
                    Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 : [𝐴] 𝑡 [𝐵]                  via rule TSub, rule SubHoare and (7) (8)           (9)

       which is exactly what we needed to prove for this case.

Case ChkEOpApp:

          Γ ⊢WF [𝐴] 𝑡 [𝐵]         Δ(op) = 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥
                              ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗
                 Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
                    d
                       [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]
           ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
                                                                     ChkEOpApp
                 Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       This rule can be treated as a combination of TSub and TEffOp. From the induction hy-
       pothesis and the precondition of ChkEffOp, we know
                           Δ(op) = 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥                    precondition                               (1)
                           Γ ⊢ op : 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥                   via rule TEOp and (1)                      (2)
                           ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗                                precondition                               (3)
                           Γ ⊢ op : 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]     Lemma E.5 and (2) (3)                      (4)
                                                        l
                           Γ ⊢ op : 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]      precondition and (4)                       (5)
                           Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘            precondition                               (6)
                                            Ü
                           Γ, 𝑧𝑘 :𝑡𝑘 ⊢ 𝐴 ⊆        𝐴𝑖                         via Lemma E.3                              (7)
                                                      l
                           Γ, 𝑧𝑘 :𝑡𝑘 ⊢ op : 𝑦 𝑗 :𝑡 𝑗  [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]       via Lemma E.3 and rule TSub                (8)
                                              d
       Now the operator op has the return type [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]. The rest of proof it almost the same
       as the proof in the case ChkLetE:
               ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 ⊢ op : [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]                         via rule TSub, rule SubIntLL and (8)         (9)
               ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 ⊢ op : [𝐴 ∧ 𝐴𝑖 ] 𝑡𝑖 [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ]        via Lemma E.6, precondition, and (9)        (10)
               ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 : [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]         inductive hypothesis                        (11)
               ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴 ∧ 𝐴𝑖′ ] 𝑡 [𝐵]        rule TEOpApp and (10) (11)                  (12)
                                                l
               Γ, 𝑧𝑘 :𝑡𝑘 ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 :   [𝐴 ∧ 𝐴𝑖 ] 𝑡 [𝐵]          rule TInter and (12)                        (13)
                                                     Ü
               Γ, 𝑧𝑘 :𝑡𝑘 ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴 ∧   𝐴𝑖 ] 𝑡 [𝐵]          via rule TSub, rule SubIntMerge and (13)    (14)
               Γ, 𝑧𝑘 :𝑡𝑘 ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴] 𝑡 [𝐵]                  via rule TSub, rule SubHoare and (7) (14)   (15)
               Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 : [𝐴] 𝑡 [𝐵]                          via Lemma E.4, precondition and (15)        (16)

       which are valid.

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                         37


                                                                                                                      

  Decidability of Algorithmic Typing. We present the proof for Theorem 5.2 from Sec. 5. The proof
requires the following lemmas about the SFAInclusion subroutine and the instantiation function
Abduce.
  Lemma E.8. [Decidability of Base Subtyping] the Γ ⊢ {𝜈:𝑏 | 𝜙 1 } <: {𝜈:𝑏 | 𝜙 2 } is decidable.
  Proof. As we mentioned in Section 5.1, similar to standard reﬁnement type system, the subtyp-
ing check will be encoded as a query in EPR, which is in the decidable fragment of FOL. Thus, the
base subtyping check is decidable.                                                              

  Lemma E.9. [Decidability of Inclusion Algorithm] the SFAInclusion is decidable.
  Proof. The gathered literals are ﬁnite, thus the induced boolean combination is also ﬁnite. Then
the loop in SFAInclusion (line 3 in Algorithm 1) has a ﬁnite bound. According to Lemma E.8,
SFAInclusion is decidable.                                                                       

  Lemma E.10. [Decidability of Instantiation Algorithm] the Abduce is decidable.
  Proof. The gathered literals are ﬁnite, thus the induced boolean combination is also ﬁnite. Then
the loop in Abduce (line 6 in Algorithm 1) has a ﬁnite bound. According to Lemma E.8, Abduce is
decidable.                                                                                       

  Lemma E.11. [Decidability of Well-Formedness] For all type context Γ, type 𝑡, and 𝜏, the Γ ⊢WF 𝑡
and Γ ⊢WF 𝜏 is decidable.
  Proof. According to the well-formedness rules shown in Fig. 13, these rules are inductively
deﬁned and structural decreasing over the types (𝑡 1 or 𝜏1 ). Thus, they always terminate.  

    Lemma E.12. [Decidability of Subtyping] For all type context Γ, type 𝑡 1 , 𝑡 2 , 𝜏1 , and 𝜏2 , the Γ ⊢ 𝑡 1 <:
𝑡 2 and Γ ⊢ 𝜏1 <: 𝜏2 is decidable.
  Proof. According to the subtyping rules shown in Fig. 13, Lemma Theorem E.8 and Lemma Theorem E.9,
these rules are inductively deﬁned and structural decreasing over the types (𝑡 1 or 𝜏1 ). Thus, they
always terminate.                                                                                  

  Lemma E.13. [Decidability of Instantiation] For all type context Γ and automata 𝐴,
Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘 is decidable.
  Proof. According to the rule shown in Fig. 13 and Lemma E.10, it always terminates.                                 

  Now we can prove the decidability theorem of our typing algorithm. As the type synthesis
rules are deﬁned mutually recursively, we simultaneously prove both are decidable. The following
theorem states a stronger inductive invariant that is suﬃcient to prove the decidability of the
typing algorithm.
  Theorem E.14 (Decidability of Algorithmic Typing). Type checking a term 𝑒 against a type
𝜏 in a typing context Γ , all Γ ⊢ 𝑒 ⇐ 𝜏 , Γ ⊢ 𝑣 ⇐ 𝑡 , Γ ⊢ 𝑒 ⇒ 𝜏 , and Γ ⊢ 𝑣 ⇒ 𝑡 is decidable.

  Proof. According to Lemma E.11, Lemma E.12, and Lemma E.13, the auxiliary functions (well-
formedness, subtyping, instantiation) always terminate. Thus, the key of the decidability proof is

                                                             , Vol. 1, No. 1, Article . Publication date: September 2018.
38                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


ﬁnding a ranking function over the inputs of typing algorithm, which is based on the size of terms
(TermSize) and types (TypeSize):
                                  TermSize(𝑐)  1
                                  TermSize(𝑥)  1
                             TermSize(𝑑 (𝑣 𝑖 ))  1 + Σ𝑖 TermSize(𝑣 𝑖 )
                            TermSize(𝜆𝑥:𝑡 .𝑒)  1 + TermSize(𝑒)
                  TermSize(fix𝑓 :𝑡 .𝜆𝑥:𝑡 .𝑒)  2 + TermSize(𝑒)
            TermSize(let 𝑥 = op 𝑣 𝑖 in 𝑒)  1 + TermSize(𝑒) + Σ𝑖 TermSize(𝑣 𝑖 )
           TermSize(let 𝑥 = 𝑜𝑝 𝑣 1 in 𝑒)  1 + TermSize(𝑒) + Σ𝑖 TermSize(𝑣 𝑖 )
            TermSize(let 𝑥 = 𝑣 1 𝑣 2 in 𝑒)  1 + TermSize(𝑒) + TermSize(𝑣 1 ) + TermSize(𝑣 2 )
              TermSize(let 𝑥 = 𝑒 1 in 𝑒 2 )  1 + TermSize(𝑒 1 ) + TermSize(𝑒 2 )
       TermSize(match 𝑣 with 𝑑 𝑦  𝑒𝑖 )  1 + TermSize𝑣 + Σ𝑖 TermSize(𝑒𝑖 )
                         TypeSize({𝜈:𝑏 | 𝜙})  1
                          TypeSize(𝑥:𝑡  𝜏)  1 + TypeSize(𝑡) + TypeSize(𝜏)
                         TypeSize(𝑥:𝑏 d 𝜏)  1 + TypeSize(𝜏)
                        TypeSize([𝐴] 𝑡 [𝐴])  1 + TypeSize(𝑡)
                           TypeSize(𝜏1 ⊓ 𝜏2 )  1 + TypeSize(𝜏1 ) + TypeSize(𝜏2 )
With the help of TermSize, we deﬁne a lexicographic ranking function as a string contains two
natural numbers (a pair of natural numbers).
                                 Rank(Γ ⊢ 𝑒 ⇐ 𝜏)  (TermSize(𝑒), TypeSize(𝜏))
                                 Rank(Γ ⊢ 𝑒 ⇒ 𝜏)  (TermSize(𝑒), 0)
where one rank is less than another iﬀ
                            (𝑎 1 , 𝑏 1 ) < (𝑎 2 , 𝑏 2 ) ⇐⇒ 𝑎 1 < 𝑏 1 ∨ (𝑎 1 = 𝑏 1 ∧ 𝑏 1 < 𝑏 2 )
We proceed by induction over the mutual recursive structure of type synthesis ( ⇒ ) and type
check ( ⇐ ) rules. In the cases for; synthesis rule SynConst, SynBaseVar, and SynFuncVar don’t
have recursive call, thus always terminates. Consequently, we try to prove that the rank current
call is greater than recursive calls in the rest of cases below.
Case ChkGhost:

            Γ ⊢WF 𝑥:𝑏 d 𝜏
        Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑒 ⇐ 𝜏
                                 ChkGhost
          Γ ⊢ 𝑒 ⇐ 𝑥:𝑏 d 𝜏
       We the rank current call is
                         Rank(Γ ⊢ 𝑒 ⇐ 𝑥:𝑏 d 𝜏) = (TermSize(𝑒), 1 + TypeSize(𝜏))
       which is greater than recursive call:
                         Rank(Γ, 𝑥:{𝜈:𝑏 | ⊤} ⊢ 𝑒 ⇐ 𝜏) = (TermSize(𝑒), TypeSize(𝜏))
Case ChkInter:


, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                            39


           Γ ⊢WF 𝜏1 ⊓ 𝜏2
            Γ ⊢ 𝑒 ⇐ 𝜏1
            Γ ⊢ 𝑒 ⇐ 𝜏2
                               ChkInter
          Γ ⊢ 𝑒 ⇐ 𝜏1 ⊓ 𝜏2
       We the rank current call is
             Rank(Γ ⊢ 𝑒 ⇐ 𝜏1 ⊓ 𝜏2 ) = (TermSize(𝑒), 1 + TypeSize(𝜏1 ) + TypeSize(𝜏2 ))
       which is greater than recursive call:
                             Rank(Γ ⊢ 𝑒 ⇐ 𝜏1 ) = (TermSize(𝑒), TypeSize(𝜏1 ))
                             Rank(Γ ⊢ 𝑒 ⇐ 𝜏2 ) = (TermSize(𝑒), TypeSize(𝜏2 ))
Case ChkLetV:

               Γ ⊢WF [𝐴] 𝑡 [𝐵]
                 Γ ⊢ 𝑣𝑥 ⇒ 𝑡𝑥
           Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
                                          ChkLetV
       Γ ⊢ let 𝑥 = 𝑣𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       We the rank current call is
  Rank(Γ ⊢ let 𝑥 = 𝑣 𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (1 + TermSize(𝑣 𝑥 ) + TermSize(𝑒), 1 + TypeSize(𝑡))
       which is greater than recursive calls:
                                  Rank(Γ ⊢ 𝑣 𝑥 ⇒ 𝑡𝑥 ) = (TermSize(𝑣 𝑥 ), 0)
                    Rank(Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (TermSize(𝑒), 1 + TypeSize(𝑡))
Case ChkLetE:

                      Γ ⊢WF [𝐴] 𝑡 [𝐵]
                    d                          Ô
        Γ ⊢ 𝑒𝑥 ⇒ [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] Γ ⊢ 𝐴 ⊆ 𝐴𝑖
         ∀𝑖.Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
                                                      ChkLetE
            Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       We the rank current call is
  Rank(Γ ⊢ let 𝑥 = 𝑒𝑥 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (1 + TermSize(𝑒𝑥 ) + TermSize(𝑒), 1 + TypeSize(𝑡))
       which is greater than recursive calls:
                                       l
                       Rank(Γ ⊢ 𝑒𝑥 ⇒ [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ]) = (TermSize(𝑒𝑥 ), 0)
            Rank(Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]) = (TermSize(𝑒), 1 + TypeSize(𝑡))
Case ChkPOpApp:

                Γ ⊢WF [𝐴] 𝑡 [𝐵]
              Δ(𝑜𝑝 ) = 𝑦 𝑗 :𝑡 𝑗  𝑡𝑥
                ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗
            Γ, 𝑥:𝑡𝑥 ⊢ 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
                                             ChkPOpApp
       Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       We the rank current call is
Rank(Γ ⊢ let 𝑥 = op 𝑣 𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (1 + TermSize(𝑒) + ΣTermSize(𝑣 𝑖 ), 1 + TypeSize(𝑡))

                                                                , Vol. 1, No. 1, Article . Publication date: September 2018.
40                                                    Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


       which is greater than recursive calls:
                                              Rank(Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗 ) = (TermSize(𝑣 𝑗 ), TypeSize(𝑡 𝑗 ))
             Rank(Γ, 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]) = (TermSize(𝑒), 1 + TypeSize(𝑡))
Case ChkEOpApp:

          Γ ⊢WF [𝐴] 𝑡 [𝐵]         Δ(op) = 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥
                              ∀ 𝑗 .Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗
                 Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦 𝑗 :𝑡 𝑗  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
                    d
                       [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 𝑗 ↦→ 𝑣 𝑗 ]
           ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
                                                                   ChkEOpApp
                 Γ ⊢ let 𝑥 = op 𝑣𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       We the rank current call is
Rank(Γ ⊢ let 𝑥 = op 𝑣 𝑖 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (1 + TermSize(𝑒) + ΣTermSize(𝑣 𝑖 ), 1 + TypeSize(𝑡))
       which is greater than recursive calls:
                                                  Rank(Γ ⊢ 𝑣 𝑗 ⇐ 𝑡 𝑗 ) = (TermSize(𝑣 𝑗 ), TypeSize(𝑡 𝑗 ))
         Rank(Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]) = (TermSize(𝑒), 1 + TypeSize(𝑡))
Case ChkApp:

        Γ ⊢WF [𝐴] 𝑡 [𝐵]        Γ ⊢ 𝑣1 ⇒ 𝑧𝑘 :𝑏𝑘 d 𝑦:𝑡 𝑦  𝜏𝑥
                              Γ ⊢ 𝑣2 ⇐ 𝑡 𝑦
               Γ ⊢[𝐴] 𝑧𝑘 :𝑏𝑘 d 𝑦:𝑡 𝑦  𝜏𝑥 ≈›𝑧𝑘 :𝑡𝑘
                   d
                     [𝐴𝑖 ] 𝑡𝑖 [𝐴𝑖′ ] = 𝜏𝑥 [𝑦 ↦→ 𝑣𝑦 ]
         ∀𝑖.Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i ) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]
                                                               ChkApp
               Γ ⊢ let 𝑥 = 𝑣1 𝑣2 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]
       We the rank current call is
Rank(Γ ⊢ let 𝑥 = 𝑣 1 𝑣 2 in 𝑒 ⇐ [𝐴] 𝑡 [𝐵]) = (1 + TermSize(𝑒) + TermSize(𝑣 1 ) + TermSize(𝑣 2 ), 1 + TypeSize(𝑡))

       which is greater than recursive calls:

                             Rank(Γ ⊢ 𝑣 1 ⇒ 𝑧𝑘 :𝑏𝑘 d 𝑦:𝑡 𝑦  𝜏𝑥 ) = (TermSize(𝑣 1 ), 0)
                                                  Rank(Γ ⊢ 𝑣 2 ⇐ 𝑡 𝑦 ) = (TermSize(𝑣 2 ), TypeSize(𝑡 𝑦 ))
         Rank(Γ, 𝑧𝑘 :𝑡𝑘 , 𝑥:𝑡𝑖 ⊢ 𝑒 ⇐ [(𝐴; h⊤i) ∧ 𝐴𝑖′ ] 𝑡 [𝐵]) = (TermSize(𝑒), 1 + TypeSize(𝑡))
Case ChkFunc:

          Γ ⊢WF 𝑥:𝑡𝑥′  𝜏 Γ ⊢ 𝑡𝑥′ <: 𝑡𝑥
                 Γ, 𝑥:𝑡𝑥′ ⊢ 𝑒 ⇐ 𝜏
                                                ChkFunc
              Γ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑥:𝑡𝑥′  𝜏
       We the rank current call is
        Rank(Γ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑥:𝑡𝑥′  𝜏) = (1 + TermSize(𝑒), 1 + TypeSize(𝑡𝑥′ ) + TypeSize(𝜏))
       which is greater than recursive calls:
                              Rank(Γ, 𝑥:𝑡𝑥′ ⊢ 𝑒 ⇐ 𝜏) = (TermSize(𝑒), TypeSize(𝜏))

, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                                       41


Case ChkFix:

          Γ ⊢WF 𝑡 𝑓′      Γ ⊢ 𝑡 𝑓′ <: 𝑡 𝑓
           Γ, 𝑓 :𝑡 𝑓′ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′
                                             ChkFix
         Γ ⊢ fix𝑓 :𝑡 𝑓 .𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′

       We the rank current call is
                    Rank(Γ ⊢ fix𝑓 :𝑡 𝑓 .𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′ ) = (2 + TermSize(𝑒), TypeSize(𝑡 𝑓′ ))
       which is greater than recursive calls:
                       Rank(Γ, 𝑓 :𝑡 𝑓′ ⊢ 𝜆𝑥:𝑡𝑥 .𝑒 ⇐ 𝑡 𝑓′ ) = (1 + TermSize(𝑒), TypeSize(𝑡 𝑓′ ))
Case ChkMatch:

                            ∀𝑖.(𝑑𝑖 , 𝑦 𝑗 :𝑡 𝑗  {𝜈:𝑏 | 𝜙𝑖 }) ∈ Δ
         Γ, 𝑦 𝑗 :𝑡 𝑗 , 𝑧:{𝜈:𝑏 | 𝜈 = 𝑣 ∧ 𝜙𝑖 } ⊢ 𝑒𝑖 ⇐ 𝜏         where 𝑧 is fresh
                                                                                 ChkMatch
                       Γ ⊢ match 𝑣 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 ⇐ 𝜏
       We the rank current call is
   Rank(Γ ⊢ match 𝑣 with 𝑑𝑖 𝑦 𝑗 → 𝑒𝑖 ⇐ 𝜏) = (1 + TermSize(𝑣) + ΣTermSize(𝑒𝑖 ), TypeSize(𝜏))
       which is greater than recursive calls:
               Rank(Γ, 𝑦 𝑗 :𝑡 𝑗 , 𝑧:{𝜈:𝑏 | 𝜈 = 𝑣 ∧ 𝜙𝑖 } ⊢ 𝑒𝑖 ⇐ 𝜏) = (TermSize(𝑒𝑖 ), TypeSize(𝜏))
Case ChkSub:

                  Γ ⊢WF [𝐴2 ] 𝑡2 [𝐵 2 ]
        Γ ⊢ 𝑒 ⇒ [𝐴1 ] 𝑡1 [𝐵 1 ] Γ ⊢ 𝐴2 <: 𝐴1
                     Γ ⊢ 𝑡1 <: 𝑡2
       Γ ⊢ (𝐴2 ; h⊤i ) ∧ (𝐴2 ; h⊤i ) ∧𝐵 1 ⊆ 𝐵 2
                                                        ChkSub
                  Γ ⊢ 𝑒 ⇐ [𝐴2 ] 𝑡2 [𝐵 2 ]
       We the rank current call is
                        Rank(Γ ⊢ 𝑒 ⇐ [𝐴2 ] 𝑡 2 [𝐵 2 ]) = (TermSize(𝑒), 1 + TypeSize(𝑡 2 ))
       which is greater than recursive calls:
                                     Rank(Γ ⊢ 𝑒 ⇒ [𝐴1 ] 𝑡 1 [𝐵 1 ]) = (TermSize(𝑒), 0)
Case ChkSubV:

           Γ ⊢WF 𝑡 Γ ⊢ 𝑣 ⇒ 𝑡 ′
                Γ ⊢ 𝑡 ′ <: 𝑡
                                             ChkSubV
                Γ ⊢ 𝑣 ⇐𝑡
       We the rank current call is
                                    Rank(Γ ⊢ 𝑣 ⇐ 𝑡) = (TermSize(𝑣), TypeSize(𝑡))
       which is greater than recursive calls:
                                            Rank(Γ ⊢ 𝑣 ⇒ 𝑡 ′ ) = (TermSize(𝑣), 0)
Thus, the typing algorithm is decidable.                                                                                            




                                                                           , Vol. 1, No. 1, Article . Publication date: September 2018.
42                                                 Zhe Zhou, Qianchuan Ye, Benjamin Delaware, and Suresh Jagannathan


F EVALUATION DETAILS
 Table 3 and Table 4 list the information for individual ADT methods from Table 1. All our bench-
marks suite, and corresponding Coq proofs are available on Zenodo https://doi.org/10.5281/zenodo.10806686

                                        Table 3. Full table of Table 1, first part.

      Datatype     Library     #Ghost s𝐼         Method        #Branch #App #SAT #Inc avg. s𝐴 tSAT (s) tInc (s)
                  LinkedList      0     4       is_empty          3      2      60    3    59     0.29    0.03
                  LinkedList      0     4         empty           2      3      68    2    47     0.37    0.01
                  LinkedList      0     4      concat_aux         4      7     297    7    98     1.63    0.06
                  LinkedList      0     4         concat          2      3      34    2    57     0.16    0.01
                  LinkedList      0     4          cons           3      7     203    5    112    1.18    0.05
                  LinkedList      0     4          head           2      2      65    3    55     0.36    0.03
                  LinkedList      0     4           tail          2      2     159    4    69     0.79    0.04
        Stack      KVStore        1     9       is_empty          2      1      93    4    79     0.55    0.04
                   KVStore        1     9         empty           3      5     213    6    176    1.29    0.06
                   KVStore        1     9      concat_aux         3      6     709    16   167    3.84    0.19
                   KVStore        1     9         concat          2      3     100    4    89     0.58    0.03
                   KVStore        1     9          cons           4      10    874    17   226    5.78    0.23
                   KVStore        1     9          head           2      2     183    5    98     0.97    0.06
                   KVStore        1     9           tail          2      2     396    8    125    1.79    0.12
                    Tree          0     12        mem             3      5    115     4    212    0.69    0.05
                    Tree          0     12       insert           2      5     85     3    215    0.51    0.04
                    Tree          0     12       empty            1      0     17     1    111    0.11    0.01
                    Tree          0     12     insert_aux         5      12   1589    11   531    9.34    0.53
          Set       Tree          0     12      mem_aux           5      10   1469    11   490    8.48    0.41
                   KVStore        1     9        insert           3      5    245     6    160    1.51    0.06
                   KVStore        1     9        empty            1      0     7      1    42     0.04    0.01
                   KVStore        1     9         mem             1      1     97     4    73     0.60    0.03
                  LinkedList      0     4          snoc           2      6    171     4    110    0.84    0.03
                  LinkedList      0     4          head           2      2     65     3    55     0.36    0.03
                  LinkedList      0     4        append           4      9    190     4    96     1.08    0.06
                  LinkedList      0     4         empty           2      3     68     2    47     0.37    0.01
                  LinkedList      0     4       is_empty          3      2     60     3    59     0.29    0.03
                  LinkedList      0     4           tail          2      2    167     4    93     0.84    0.04
        Queue       Graph         1     24         snoc           3      9    984     12   491    6.60    0.20
                    Graph         1     24         head           2      2    291     5    251    1.57    0.24
                    Graph         1     24       append           5      12   1212    14   525    8.19    0.86
                    Graph         1     24        empty           2      3    202     4    318    1.27    0.08
                    Graph         1     24      is_empty          2      1    165     4    234    1.03    0.10
                    Graph         1     24          tail          3      4    980     12   409    6.58    0.59
                     Set          1     28 minset_mem             1      1    199     6    241    1.43    0.24
                     Set          1     28    minimum             2      2    181     5    251    0.89    0.37
                     Set          1     28 minset_insert          3      6    612     17   294    4.19    1.58
                     Set          1     28 minset_singleton       2      3    120     4    259    0.80    0.13
       MinSet      KVStore        1     25 minset_mem             1      1    207     6    223    1.49    0.31
                   KVStore        1     25    minimum             2      2    191     5    234    0.95    0.36
                   KVStore        1     25 minset_insert          5      8    2227    23   519    10.93   9.34
                   KVStore        1     25 minset_singleton       3      6    235     5    408    1.59    0.32
                    Tree          0     12      mem_aux           5      10   1469    11   490    8.37    0.41
                    Tree          0     12     lazy_insert        2      6     85     3    301    0.50    0.04
                    Tree          0     12         force          1      1     17     1    171    0.11    0.01
                    Tree          0     12     insert_aux         5      12   1589    11   531    9.33    0.57
                    Tree          0     12      lazy_mem          3      6    115     4    298    0.68    0.07
                    Tree          0     12     new_thunk          1      0     17     1    111    0.11    0.01
                     Set          1     9       lazy_mem          1      2     98     4    105    0.59    0.04
       LazySet       Set          1     9          force          1      1     7      1    66     0.03    0.01
                     Set          1     9      lazy_insert        2      3    101     4    106    0.57    0.04
                     Set          1     9      new_thunk          1      0     7      1    42     0.03    0.01
                   KVStore        1     9       lazy_mem          1      2     98     4    105    0.59    0.04
                   KVStore        1     9      insert_aux         3      5    245     6    160    1.49    0.06
                   KVStore        1     9          force          1      1     7      1    66     0.03    0.01
                   KVStore        1     9      lazy_insert        2      3    101     4    121    0.58    0.04
                   KVStore        1     9      new_thunk          1      0     7      1    42     0.03    0.01



, Vol. 1, No. 1, Article . Publication date: September 2018.
A HAT Trick: Automatically Verifying Representation Invariants Using Symbolic Finite Automata                            43


                                   Table 4. Full table of Table 1, second part.

      Datatype        Library    #Ghost s𝐼      Method        #Branch #App #SAT #Inc avg. s𝐴 tSAT (s) tInc (s)
                       Tree        0    12     minimum            2       3      82      3     207      0.49     0.03
                       Tree        0    12       insert           2       5      85      3     215      0.50     0.04
                       Tree        0    12   contains_aux         5       10    871     11     311      4.87     0.17
                       Tree        0    12     contains           3       5     115      4     212      0.68     0.06
                       Tree        0    12      empty             1       0      17      1     111      0.11     0.01
                       Tree        0    12    insert_aux          5       12    1589    11     531      9.33     0.52
        Heap           Tree        0    12   minimum_aux          2       3     408      5     334      2.11     0.09
                    LinkedList     0    4     insert_aux          4       8     497      8     118      3.03     0.08
                    LinkedList     0    4       empty             1       0      11      1     19       0.07     0.01
                    LinkedList     0    4      contains           2       4      65      3     72       0.36     0.02
                    LinkedList     0    4    contains_aux         3       5     359      6     129      1.88     0.05
                    LinkedList     0    4        insert           2       6     137      5     93       0.88     0.05
                    LinkedList     0    4      minimum            2       2      63      3     65       0.36     0.03
                      Tree         1    20 deleteChildren         3       7     1055    13     470      6.39     1.79
                      Tree         1    20 del_path_in_dir        2       5     452      5     284      1.76     0.17
                      Tree         1    20       add              3       8     2085    17     652      14.15    2.21
                      Tree         1    20 add_path_in_dir        2       5     837      9     424      4.90     7.25
                      Tree         1    20      delete            4       16    1064    12     520      6.95     0.76
     FileSystem       Tree         1    20       init             1       5     431      7     323      3.22     0.49
                     KVStore       1    17 deleteChildren         3       7     2244    19     392      14.00    1.38
                     KVStore       1    17       add              4       10    8144    43     481      56.64    16.54
                     KVStore       1    17      delete            4       20    5658    10     234      7.91     1.49
                     KVStore       1    17       init             1       3     449      5     166      3.45     0.08
                     KVStore       2    18       is_node          1        0     19      1     79       0.11     0.01
                     KVStore       2    18   add_transition       2        2    1417    14     176      9.68     0.45
                     KVStore       2    18      add_node          1        0     19      1     79       0.11     0.01
                     KVStore       2    18   del_transition       2        2    704      8     152      4.72     0.32
                     KVStore       2    18    is_transition       3        3    3604    25     228      18.84    1.60
        DFA           Graph        2    11       is_node          1        1    115      4     95       0.74     0.04
                      Graph        2    11   add_transition       4        4    2420    27     192      16.73    2.12
                      Graph        2    11      add_node          2        2    118      4     96       0.71     0.04
                      Graph        2    11   del_transition       4        4    3625    27     225      25.53    3.42
                      Graph        2    11    is_transition       4        3    3622    27     208      25.86    2.72
                       Set         2    9     is_transition       2        1    1503    30     77       10.03    0.25
                       Set         2    9    add_transition       4        4    3889    50     357      27.39    12.80
                       Set         2    9       add_node          3        3    2332    35     314      15.80    1.24
                       Set         2    9        is_node          3        2    1441    30     197      9.59     0.45
                       Set         2    9       singleton         2        2    362     10     160      2.30     0.09
  ConnectedGraph      Graph        1    20    is_transition       4        3    1349    17     360      19.19    53.90
                      Graph        1    20   add_transition       4        4    1351    17     361      19.23    52.38
                      Graph        1    20      add_node          3        4    666     12     300      14.40    14.34
                      Graph        1    20       is_node          1        1    139      4     237      0.90     0.34
                      Graph        1    20      singleton         2        3    202      4     255      1.28     0.47




                                                              , Vol. 1, No. 1, Article . Publication date: September 2018.
