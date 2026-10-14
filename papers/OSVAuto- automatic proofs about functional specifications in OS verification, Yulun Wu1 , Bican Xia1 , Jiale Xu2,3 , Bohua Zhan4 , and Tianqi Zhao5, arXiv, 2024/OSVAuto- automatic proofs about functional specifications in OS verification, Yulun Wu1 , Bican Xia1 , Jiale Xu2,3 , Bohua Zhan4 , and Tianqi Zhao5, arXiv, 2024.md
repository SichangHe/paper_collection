                                             OSVAuto: automatic proofs about functional
                                                  specifications in OS verification

                                              Yulun Wu1 , Bican Xia1 , Jiale Xu2,3 , Bohua Zhan4 , and Tianqi Zhao5
arXiv:2403.13457v2 [cs.SC] 22 May 2025




                                                    1
                                                         School of Mathematical Sciences, Peking University, China
                                                     2
                                                         Institute of Software, Chinese Academy of Sciences, China
                                                           3
                                                             University of Chinese Academy of Sciences, China
                                                                  4
                                                                    Huawei Technologies Co., Ltd., China
                                                               5
                                                                  Zhongguancun Laboratory, Beijing, China



                                               Abstract. We present OSVAuto for automatic proofs about functional
                                               specifications that commonly arise when verifying operating system ker-
                                               nels. The algorithm behind OSVAuto is designed to support natively
                                               those data types that commonly occur in OS verification, including se-
                                               quences, maps, structures and enumerations. Propositions about these
                                               data are encoded into a form that is suitable for SMT solving. For quan-
                                               tifier instantiation, we propose an extension of recent work for automatic
                                               proofs about sequences. We evaluate the algorithm on proof obligations
                                               adapted from existing verification of the µC-OS/II kernel in Coq, demon-
                                               strating that a large number of proof obligations can be solved automat-
                                               ically, significantly reducing the proof effort on the functional side.

                                               Keywords: program verification · operation system · automatic verifi-
                                               cation · SMT.


                                         1   Introduction

                                         Verification of operating system kernels is one of the major application areas of
                                         interactive and automatic theorem proving. Major efforts using interactive the-
                                         orem provers include the verification of the seL4 microkernel [8], CertiKOS [6],
                                         and µC/OS-II [15]. Recent efforts such as [11,10] place a greater focus on au-
                                         tomation, making more extensive use of SMT solvers [3]. While there is a great
                                         variety of techniques and program logics involved in the different projects, there
                                         is also similarity in the general approach. Usually, specification of the kernel
                                         is described using a functional language at various levels of abstraction. They
                                         include abstract behavior of each API function, invariants on the internal data
                                         structures, and refinement relations between different abstraction levels. The
                                         verification task is then roughly divided into two parts:

                                         1. Correctness of functional specification: including preservation of in-
                                            variants, specification at different abstraction levels observe the refinement
                                            relation, and that the specification at the most abstract level satisfy impor-
                                            tant system properties (such as correctness of task scheduling).
2        Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

 2. Refinement between functional specification and implementation:
    This involves reasoning about semantics of low-level programming languages,
    in particular issues of memory management and aliasing, and is often done
    using some version of (concurrent) separation logic.

     In this paper, we focus on providing greater level of automation to the first
part. In real verification projects, the invariant of the OS kernel can be highly
complex, and hence the proof of invariant preservation and refinement relations
take up a large proportion of the proof effort [8].
     A key observation of this paper is that in the domain of OS verification, the
nature of proof obligations that arise is actually quite restricted. Apart from
lists (which can be encoded in SMT using sequence theory), most of the data
structures that arise are non-recursive. Unlike proving theorems in mathematics
or about complex algorithms, there is little need to make use of a large body of
existing lemmas. While the invariants frequently involve quantifiers, the quan-
tification is usually over indices of arrays or keys of mappings, making quantifier
instantiation techniques for sequences highly applicable.
     In particular, recent work [14] proposed proof automation techniques for
sequences, where quantifier instantiation is determined by analyzing the appear-
ances of bound variables within array indices. Within the restricted language
of [14], it is able to produce a finite number of instantiations when successful,
resulting in a proof goal that is equisatisfiable with the original (the method is
both sound and complete). It also provides quick checks for failure (by detect-
ing nonzero cycles in the classification graph). While the algorithm in [14] has
good theoretical properties, it is limited on the practical side by the following
restrictions:

    – Only one-dimensional sequences are supported, but nested sequences (and
      maps) frequently arise when modeling OS data structures.
    – Structures and enumerations are not supported. They also appear frequently
      in modeling, often nested with sequences and maps.
    – Many common properties on sequences cannot be handled, for example
      uniqueness of elements in a sequence.

    In this paper, we propose an extension of the algorithm in [14] that relaxes the
above restrictions. In particular, we include support for nested sequences, (finite)
mappings, structures and enumerations. To deal with difficulties mainly arising
from nested sequences, we propose keeping track of conditions on instantiations
when propagating along the graph, as well as new propagation rules for sequence
and map nodes having the same form.
    Relaxing the above restrictions make the theoretical issues significantly more
difficult, so we do not aim for completeness of our algorithm, but rather impose
heuristic cutoffs on the instantiation when it diverges. Some of the issues with
completeness are discussed in Section 6.
    We evaluate the algorithm on functional specification and proof obligations
adapted from the existing verification of the µC/OS-II kernel in Coq [15]. We
OSVAuto: automatic proofs about functional specifications in OS verification           3

observe that while the instantiation algorithm is not theoretically complete, it is
able to find all the necessary instantiations automatically, on a large number of
examples. This results in potentially significant reduction in proof effort on the
functional side.
   In summary, the main contributions of this paper is as follows:

 – We describe an extended language for writing functional specifications that
   is well-suited for OS verification, including native support for sequences,
   mappings, structures and enumerations.
 – We extend the quantifier instantiation algorithm for sequences to the new
   language, with novel techniques including keeping track of conditions during
   propagation, and propagating along nodes having the same form.
 – We evaluate the algorithm on the existing µC/OS-II verification in Coq,
   demonstrating that it can achieve complete automation on many proof obli-
   gations.


2     Preliminaries

In this section, we review existing works in proof automation for sequence theory,
and the existing verification of the µC/OS-II kernel.


2.1     Automation of sequence theory

Our work extends the algorithm in [14] for proof automation in sequence theory.
We sketch a general idea of the algorithm here.
    The main problem addressed is how to compute a finite set of instantiations
for the quantified facts in the proof obligation, such that the instantiated version
of the goal is equisatisfiable to the original (the instantiations are both sound
and complete). The algorithm proceeds by constructing a graph where each node
represents either a bound variable of some quantified fact, or a sequence variable.
An appearance of a term a[i + c] in the body of quantification over i induces an
edge from i to a with weight c (here c does not contain any bound variables.
There are other rules for inducing edges which we omit here). The algorithm
is successful if there are no cycles with nonzero total weight in the resulting
graph. Some initial instantiations are induced by concrete indices of the form
a[k], inequality conditions, etc. Other instantiations are obtained by traversing
the graph and adding edge weights to existing instantiations.
    A number of operations on sequences are supported natively, including ap-
pend, slice, repeat and map. Appearances of such operations are reduced by sim-
plifying length and index terms on the resulting sequences, with case splitting
performed if necessary. For example, an appearance of append(a, b)[i] is reduced
to a[i] under 0 ≤ i < |a| and b[i − |a|] under condition |a| ≤ i < |a| + |b| 6 .
6
    there is also a case for default value where index is out of bounds, which we omit in
    this paper throughout.
4       Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

    We borrow the main example from [14] to illustrate the algorithm. A variant
of this example will be used in Section 4.4 to illustrate one of our extensions.
Given sequences a, b, c, d and predicate P , assumptions c = append(a, b), d =
append(b, a), we wish to show

           (∀i. 0 ≤ i < |c| → P (c[i])) =⇒ (∀k. 0 ≤ k < |d| → P (d[k]))

The first step of the algorithm makes substitutions c = append(a, b) and d =
append(b, a), followed by reducing appearances of append. Eventually this results
in proof goals such as the following:

       0 ≤ k < |b| =⇒ (∀i. 0 ≤ i < |a| → P (a[i]))
                   =⇒ (∀j. |a| ≤ j < |a| + |b| → P (b[j − |a|])) =⇒ P (b[k])

This proof goal gives rise to a graph with nodes i, j, a and b, with edge i → a of
weight 0 (from a[i]) and j → b of weight −|a| (from b[j−|a|]). Initial instantiation
k for node b comes from the term b[k] in the goal. This induces instantiation k+|a|
for bound variable j. With this instantiation, the proof goal becomes:

        0 ≤ k < |b| =⇒ (|a| ≤ k + |a| < |a| + |b| → P (b[k])) =⇒ P (b[k])

which is clearly provable.

2.2   Verification of the µC/OS-II kernel
In this section, we give an overview of the existing verification of the µC/OS-II
operating system in Coq [15]. The purpose is to provide a background for the
current work, showing the kind of specifications and proof goals that commonly
arise in OS verification, and motivate the language and algorithm designs in
later sections.
    The µC/OS-II is a small OS kernel, whose core modules include task man-
agement, event management, timers, and so on. Existing work [15] verified in
Coq most of the key functionalities in the kernel. The verification makes use
of concurrent separation logic with refinement (CSL-R) that handles preemp-
tive interrupts. Functional specification is defined for each API function at two
levels of abstraction (called high-level and low-level). Invariants are stated for
data structures at each level, and refinement relations are stated between the
two levels. They will be collectively called invariants since they are preserved by
the combination of high-level and low-level functional specification of each API
function.
    We now give some examples of data structures and invariants. The definitions
largely follow the existing Coq verification, but we will show their restatement
in the language of OSVAuto for ease of reading.
    Addresses are modeled using unsigned 32-bit integers. Each address value
(addrval) is either null (Vull) or a pointer value (Vptr(addr)). The low-level task
control block (TCB) contains information about a task, including its priority,
status (represented as a bitmap), event it is waiting for, etc, represented in a
 OSVAuto: automatic proofs about functional specifications in OS verification                               5

way that is close to the C implementation. By comparison, the high-level TCB
(AbsTCB) contains the same information but in a more abstract way, represent-
ing status as an enumerated value. These definitions are shown in Figure 1.


// A d d r e s s e s                           // High - level task status
typedef address = int32u ;                     enum tcbstats =
                                                 o s _ s t a t _ s e m ( address ev )
enum addrval =                                 | o s _ s t a t _ q ( address ev )
  Vnull | Vptr ( address addr )                | os_stat_time
                                               | o s _ s t a t _ m b o x ( address ev )
// Low - level TCB                             | o s _ s t a t _ m u t e x s e m ( address ev )
struct TCB {
  addrval O S T C B E v e n t P t r;           enum t a s k s t a t u s =
  addrval OSTCBMsg ;                             rdy | wait ( tcbstats stat , int16u time )
  int16u OSTCBDly ;
  int16u O S T C B S t a t;                    // High - level TCB
  int8u O S T C B P r i o;                     struct AbsTCB {
  int8u OSTCBX ;                                 int8u prio ;
  int8u OSTCBY ;                                 t a s k s t a t u s stat ;
  int8u O S T C B B i t X;                       addrval msg ;
  int8u O S T C B B i t Y;                       bool sus ;
}                                              }


           Fig. 1: Examples of high-level and low-level task control blocks.


    Next, we consider refinement relations between the low-level and high-level
TCBs. They express, for example, the correspondence between representation of
task status, with one case for each possible status value. The case where the task
is suspended and at the same time waiting for semaphore is shown in Figure 2.


p r e d i c a t e R H L _ W a i t S _ S u s p e n d _ P( TCB tcb , Seq < int8u > rtbl , AbsTCB abstcb ) {
    switch ( abstcb ) {
        case AbsTCB {{ prio : prio , stat : wait ( o s _ s t a t _ s e m( eid ) , dly ) , sus : true }}:
            tcb . O S T C B P r i o == prio && p r i o _ n o t _ i n _ t b l( prio , rtbl ) &&
            tcb . O S T C B E v e n t P t r == Vptr ( eid ) &&
            tcb . O S T C B S t a t == O S _ S T A T _ S E M | O S _ S T A T _ S U S P E N D;
        default : true ;
    }
}


Fig. 2: Part of the refinement relation for task control blocks (task is suspended
while also waiting for a semaphore).


    The low-level and high-level global state (with type Global and AbsGlobal
respectively) each contains a table mapping priorities to TCBs. The high-level
state contains further information, for example a priority map for efficient re-
trieval of the ready task with highest priority. We omit their definitions for reason
of space. The refinement relations on TCBs extend to refinement relations on
the global state RLH_TCB_P.
6          Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

    Finally, we give an example of proof obligation from verifying the API func-
tion for suspending a task (Figure 3).


function O S T a s k S u s p e n d A b s( int8u prio , A b s G l o b a l a b s G l o b a l) -> A b s G l o b a l {
  if (! indom ( prio , a b s G l o b a l. tcbMap ) ) { a b s G l o b a l }
  else { a b s G l o b a l{| tcbMap [ prio ]. sus := true |} }
}

query R L H _ T C B _ P _ s u s p e n d 3 {
  ... variable d e c l a r a t i o n s ...
  assumes global2 == O S T a s k S u s p e n d( prio , global ) ;
  assumes a b s G l o b a l 2 == O S T a s k S u s p e n d A b s( prio , a b s G l o b a l) ;
  assumes prio >= 0 && prio < 64;
  assumes H1 : R L H _ T C B _ P( global , a b s G l o b a l) ;
  assumes H2 : RL_TCB_P ( global ) ;
  assumes H3 : R L _ T b l _ G r p _ P( global ) ;
  shows R L H _ T C B _ P( global2 , a b s G l o b a l 2)
}


Fig. 3: An example of proof obligation from verifying API function for suspend-
ing a task. The predicates RL_TCB_P and RL_Tbl_Grp_P are invariants on the
low-level global state. OSTaskSuspend and OSTaskSuspendAbs are functional
specifications for suspend on the low-level and high-level respectively. Some def-
initions are omitted for reason of space.


    As can be guessed from the above code samples, the full invariant and refine-
ment relation is quite lengthy, and proof of invariant preservation can be very
tedious. However, the proof obligations are not very deep in the sense of requir-
ing substantial insights, rather they involve a lot of case analysis and mostly
routine reasoning about sequences and maps. Such proof obligations should be
well-suited for proof by SMT solvers. However, applying SMT to the original
statements in Coq (e.g. using tools such as SMTCoq [4]) faces the following
difficulties:
    – Tools such as SMTCoq do not encode lists and partial maps directly into
      corresponding SMT theories, in particular not making use of recent advances
      about proof automation in sequence theory.
    – Likewise, encoding for records and inductive definitions in Coq, which aim
      for generality, do not take advantage of the special nature of the problem to
      give a encoding that is efficient for SMT solving.
    – There are many extraneous quantifiers in the original Coq statements, for
      example to express matching, that are conventional in an interactive theorem
      prover but unsuitable for SMT solving.
    The above difficulties make it simply impractical to directly use existing
connection between Coq and SMT solvers (similar issues arise for hammer-like
tools in other proof assistants). Hence, we design OSVAuto with the following
aims: native representation and encoding for structures, enumerations, sequences
and maps, and making full use of proof automation (in particular quantifier
instantiation) techniques for the resulting theories.
OSVAuto: automatic proofs about functional specifications in OS verification       7

3     Language
In this section, we describe the language for expressing functional specification
and proof obligations in OSVAuto. Frequent references will be made back to
Section 2.2 which give examples of using various constructs of the language.

3.1   Types
The primitive types include bool, int, and signed/unsigned bit-vector types (int8,
int8u, int16, int16u, etc). Structures are defined by a list of (named and typed)
fields. Enumerations are defined by a list of alternatives, with each alternative
given by a list of fields. If a name appears in more than one branch of an enumer-
ation, it must have the same type in all branches. Enumerations correspond to
types defined using inductive in Coq and datatype in Isabelle, except we do not
allow recursion in the definitions. This is an important restriction which enables
more efficient SMT encoding, as described in Section 4.3.
    Sequence types have the form Seq<T >, where T is the type of entries of the
sequence. Map types have the form Map<K, V >, where K and V are key and
value types, respectively. It is interpreted as a partial function from K to V with
finite domain. We only support keys with integer and bit-vector types (there is
no constraint on types of values).
    Type definitions are supported (e.g. defining address to be int32u in Figure 1).
They are expanded automatically at parsing time.

3.2   Terms
We support the following term constructors: variables, constants, operators (log-
ical and arithmetic), function application (including defined functions and pred-
icates, constructors of enumeration, conversion functions between integer and
bit-vector types, and native operations on sequences and maps).
    For structures, we provide term constructor for structure literals (e.g. Point{x:
3, y: 4}) and structure update (e.g. p{x := 5}, where p has type Point). Dot-
notation is used for field access in structures (e.g. p.x and p.y).
    For enumerations, concrete values are built using function application. Dot-
notation can be used to access fields of a enumeration. For example, for the
enumeration addrval in Figure 1, Vptr(10).addr reduces to 10, while Vnull.addr
is not meaningful (reduces to the default value of int32u). The special notation
.id is used to access the branch number of an enumeration value. For example,
Vptr(10).id reduces to 1 while Vnull.id reduces to 0.
    More commonly the switch syntax is used to work with enumeration values.
For example, the term

               switch (a) {case Vnull ⇒ 0; case Vptr(n) ⇒ n + 1; }

reduces to 0 if a is Vnull, and n + 1 if a has form Vptr(n). In fact, OSVAuto
supports a more general form switch, where the pattern can contain (partial)
8         Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

structure literals and constants. An example of its usage is shown in Figure 2,
where the pattern matches AbsTCB values where the sus field is true, and the
stat field has form wait(os_stat_mutexsem(eid), dly). The variables prio, eid and
dly are bound and can appear in the body of the case.
     A let term has syntax let v = rhs in body end, with standard meaning. Quan-
tifiers forall and exists are supported. As syntax sugar, one can optionally specify
bounds on the quantifier (as integer ranges or keys of a mapping).
     Sequence types support two basic operations: index for index access (with
syntax a[i] used for index(i, a)) and length for length of a sequence (|a| is used
for length(a)). The non-basic operations append, cons, update, slice, repeat, and
remove can be used in the specification, but will be eliminated during normal-
ization in favor of basic ones. Map types have two basic operations indom and
get, and two non-basic operations empty and update for creating new maps.
     When writing functional specification, it is often useful to express updates
deep inside a structure, for example certain index of a certain field (and so on).
We support a general syntax of structure update for this purpose. A canonical
example is given in Figure 3, where absGlobal {tcbMap[prio].sus := true} means
updating the sus field in the prio’th element of field tcbMap in absGlobal to true.


3.3     Function definitions and proof obligations

In OSVAuto, function is defined using syntax starting with keyword function.
Types of each parameter and return value must be specified. Predicate is just a
special case of function where the return value is bool. Recursive functions are
not allowed. This restriction is made to enable unfolding all function definitions
during normalization (Section 4.1).
    Each proof obligation is specified using syntax starting with query. They may
contain type variables, variables, assumptions, and a goal. Examples of function
definition and proof obligation are shown in Figure 3.


3.4     Generalized atomic terms

We now introduce a concept that will be used frequently when describing proof
automation later on.

Definition 1. The set of generalized atomic terms is constructed inductively
from the following rules:

    – A variable is a generalized atomic term.
    – If s is generalized atomic with structure or enumeration type, then field ac-
      cesses (including .id) on s are generalized atomic.
    – If a is generalized atomic with sequence or map type, then the basic operations
      a[i], |a|, indom(k, a) and get(k, a) are generalized atomic. Note there are no
      constraints on indices i or keys k.
OSVAuto: automatic proofs about functional specifications in OS verification     9

    Each generalized atomic term can be decomposed into a pair (name, idx),
where name is a dot-separated string, each part being either name of a variable
in the current goal, field name (including id), or one of the four basic operations
index, length, get and indom. The second part idx record the list of indices/keys
for index, get and indom. We illustrate with some examples:
Example 1. Suppose the following structures and enumerations are declared:
           struct Point {int x; int y}
           enum Shape = polygon(Seq<Point> pts) | single(Point pt)
Given variables s of type Shape and m of type Map<int, Shape>, some examples
of generalized atomic terms and their decompositions as (name, idx ) pairs are:
 – s.pt.y, decomposed as (s.pt.y, []).
 – s.pts[i].x, decomposed as (s.pts.index.x, [i]).
 – |s.pts|, decomposed as (s.pts.length, []).
 – m[k].id, decomposed as (m.get.id, [k]).
 – m[k].pts[i].y, decomposed as (m.get.pts.index.y, [k, i]).
    Note both the length of idx and the type of each entry in idx depend on
name only (by looking for appearances of index, get, indom in name from left
to right). The type of the generalized atomic term can also be determined from
name and types of variables in the goal.

4   Algorithm
In this section, we present the proof automation algorithm in OSVAuto. On a
high-level, the algorithm consists of the following four steps:
 1. Normalize: the goal is reduced by applying normalization rules, until it is
    made up of generalized atomic terms and a limited set of syntax elements.
 2. Instantiation: facts that are universally quantified are instantiated, eventu-
    ally reducing the goal into quantifier-free form.
 3. Encoding: the quantifier-free proof goal is encoded into SMT formula involv-
    ing only uninterpreted functions and arithmetic theories.
 4. Solve: finally, the SMT formula is checked for satisfiability using the backend
    SMT solver (we use z3 for our experiments).
    At any stage, we apply the first step in the above list that is applicable.
That is, after any instantiation step, we check whether the result can be further
normalized, and we proceed to encoding only after no further instantiation can
be performed.
    Among the above steps, 1 and 3 preserve the satisfiability of the proof goal.
In step 2, the choice of instantiation is heuristic, in the sense that it is not
guaranteed that all necessary instantiations for the proof are found. Hence, the
entire algorithm is sound but not complete. Nevertheless, we justify the method
of instantiation based on intuitive principles, following the ideas in [14], and we
show in experiments that they are sufficient for many proof obligations that arise
in practice in OS verification.
10     Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

4.1   Normalization

The first step reduces the goal using a number of normalization rules. Most of
these are standard, so we will not explain them further.

 1. All function (and predicate) definitions are expanded.
 2. General structure updates (discussed at end of Section 3.2) are expanded in
    terms of basic structure, sequence and map updates.
 3. (Generalized) switch statements are expanded into if-then-else statements.
 4. let-terms on the top-level are removed by creating a new variable v and
    adding the corresponding equality. Otherwise they are expanded.
 5. Equality between terms of structure, enumeration, sequence and map types
    are expanded according to their definitions.
 6. Bounded quantifiers are converted into unbounded ones by moving the con-
    straint into the body.
 7. Quantifiers are moved to the outermost level (prenex form). New variables
    are created from existence facts on the outermost level (skolemization).
 8. The non-basic sequence and map operations are reduced according to their
    semantics. However, we do not split assumptions and proof goals according to
    conditions, but the represent different cases as if-then-else terms. This keeps
    the number of assumptions and proof goals small. Part of the advantages of
    splitting described in [14], that they remove non-zero cycles in some cases,
    can be achieved with more generality by keeping track of conditions during
    propagation, as discussed in Section 4.2.

    A further optimization, making use of defining equations, is adopted from [14,
Section 3.1]. We say a fact is a defining equation if it is an equality whose left
side is a generalized atomic term with no indices. The above normalization is
applied only to the indices and right side of defining equations, and the equations
themselves are used for rewriting in the rest of the proof goal.
    The following result is shown by a routine analysis of the above normalization
procedure.

Theorem 1. The above normalization procedure results in a proof goal consist-
ing only of generalized atomic terms, constants, logical and arithmetic operators
(including if-then-else), and quantifiers. Equalities are applied only to terms of
primitive type.

    In particular, all non-basic operations on sequences and maps are removed,
all structure literal, structure value, and enumeration constructors are removed,
and basic operations for sequence/maps and field accesses are only applied to
generalized atomic terms (and hence form part of a generalized atomic term).
    Part 8 of normalization follow the method in [14], and we refer to that paper
for details and examples. We illustrate step 5 using declarations from Example 1.
OSVAuto: automatic proofs about functional specifications in OS verification             11

Example 2. Consider the equality s = t where s, t have type Shape. This is
normalized into the following:

      s.id = t.id ∧
      (s.id = 0 −→ |s.pts| = |t.pts| ∧
           ∀i. 0 ≤ i < |s.pts| −→ s.pts[i].x = t.pts[i].x ∧ s.pts[i].y = t.pts[i].y) ∧
      (s.id = 1 −→ s.pt.x = t.pt.x ∧ s.pt.y = t.pt.y)

4.2     Quantifier instantiation
After normalization, the main construct that still need to be removed before SMT
solving is universal quantifiers in facts. The quantifier instantiation procedure
largely follows the ideas of [14], by building and analyzing a classification graph
(called graph for short). We extend the method to handle nested sequences and
maps (issues about structures and enumerations have already been addressed by
normalization). The main modifications are summarized as follows:
 – In addition to variables, nodes in the graph can be created for any generalized
   atomic terms of sequence or map type.
 – The quantifiers are instantiated one-at-a-time, starting from the outermost.
 – We keep track of conditions for each edge in the graph and each instantiation.
   Propagation of instantiations stop when the accumulated conditions become
   unsatisfiable.
 – We add propagation of instantiations along pattern edges, and between any
   two sequence or map nodes with the same name.
    With the above extensions, we choose the formulate the algorithm in terms
of propagation of instantiations along edges of the graph (this is equivalent to
the formulation in terms of index sets in the simplified setting of [14]). We also
need to abandon the quick detection of failure using loops with nonzero weights,
instead add heuristic cutoffs in the number and generation of instantiations.
    We now describe the instantiation procedure, starting from the basic defini-
tions. The classification graph is initially empty, and at any stage, the following
nodes are added to the graph:
 – Node i is added for each universally quantified fact, whose outermost bound
   variable is i.
 – Node s is added for each generalized atomic term s that is free in the current
   proof goal (and for which no node is already present).
    Both edges in the graph and instantiations are associated with a list of con-
ditions. First, we define the concept of conditions associated to a subterm t′ of
a term t. Given a fixed term t,
 – Conditions associated to t itself is the empty list.
 – If the subterm if (c) {t1 } else {t2 } has conditions cs, then t1 has conditions
   c :: cs, and t2 has conditions ¬c :: cs.
12      Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

 – If the term c → t has conditions cs, then t has conditions c :: cs.
In all other cases, the subterm inherit conditions from its parent term. Intu-
itively, the conditions specify the constraints under which the subterm need to
be considered.
    Now we are ready to describe how edges in the graph are formed. Edges come
in two types: weighted edges and pattern edges.

 – An edge with weight c is added from bound variable i to sequence a if a[i + c]
   appears in the body of quantifier over i. The conditions for the edge are that
   associated to a[i + c] relative to the body of the quantified fact.
 – A edge with pattern p(?i) is added from bound variable i to sequence s (resp.
   map m) if s[p(i)] (resp. m[p(i)]) appears in the body of quantifier over i. The
   conditions for the edge are that associated to m[p(i)] relative to the body of
   the quantified fact.

Note the conditions for edges may contain the bound variable i.
    Initial instantiations at the current stage arise from free appearances of terms
of the form a[i] for sequence a, and m[k] or indom(k, m) for map m. In such cases,
a (resp. m) already correspond to nodes in the graph, and i (resp. k) are added
as an initial instantiation for a (resp. m). The conditions for those instantiations
are that of a[i] (resp. m[k] or indom(k, m)) relative to the assumption or goal
they appear in.
    Instantiations are propagated through the graph according to the following
rules:

 – For each instantiation t on bound variable i, and edge from i to sequence a
   with weight c, add instantiation t + c to a. Conditions for t + c are formed
   by appending the conditions for t with the conditions on the edge, with i
   substituted by t.
 – Propagation along weighted edges can also proceed in reverse, from sequence
   a to bound variable i. The added weight is −c. Conditions for t − c are
   formed by appending the conditions for t with conditions on the edge, with
   i substituted by t − c.
 – For each instantiation t on sequence s (resp. map m), and edge from i to s
   (resp. map m) with pattern p(?i), match t against p. If there is a match with
   ?i := t′ , add instantiation t′ for i. Conditions for t′ are formed by appending
   conditions for t with conditions on the edge, with i substituted by s.
 – For two sequence nodes (resp. map nodes) n1 , n2 with the same name (as
   in Section 3.4), propagate instantiations from one to the other, with extra
   conditions stating equality between all corresponding indices.

   As an example of the last propagation rule, given sequence nodes a[i] and a[j]
(that is, a is a nested sequence, so both a[i] and a[j] are sequences), propagate
any instantiation t from node a[i] to node a[j] with extra condition i = j.
   We justify the rules for adding conditions as follows. In the first three prop-
agation rules, the added conditions are the conditions for the term that created
OSVAuto: automatic proofs about functional specifications in OS verification        13

the edge relative to the body of the quantifier, with the bound variable instan-
tiated to its value either in the source or target of the propagation. In the last
propagation rule, the intuition is that for any instantiation on n1 , the same in-
stantiation on n2 is necessary in situations where the indices are equal (so they
are actually evaluated to the same sequence or map).
    Whenever an instantiation is added according to the above rules, the list of
conditions is combined with the quantifier-free facts in the current proof goal,
and checked for inconsistency using the backend SMT solver. If the conditions
are found to be inconsistent, the instantiation is not added (so the propagation
is cut off here). This prevents some commonly-arising instantiation loops, as we
show in Section 4.4.
    Each round of instantiation removes a single quantifier from each quantified
fact. The quantified fact is removed from the proof state, and one fact is added
back for each instantiation of the outermost bound variable. As there may be
nested quantifiers, and new terms are produced as the result of instantiations,
multiple rounds of instantiations may be required. The classification graph is
preserved across the multiple rounds, and in each round, new instantiations may
arise from either newly added nodes or newly added edges.
    In the above procedure, instantiation loops may arise either in a single round,
or due to the number of rounds being unbounded. We place cutoffs on the in-
stantiation loops by limiting both the number of instantiation in each round, and
the generation number during instantiation. The generation number for terms is
computed as follows:

 – Terms in the original proof state have generation 0.
 – If a term first occurs in a quantifier-free fact that is the result of instantiation
   from terms of generation i, then it has generation i + 1.

    We keep track of generation number along propagations. A cutoff k is placed
on the generation number. That is, terms with generation k are no longer added
to the graph (and hence cannot produce new instantiations). For our experiments
we choose k = 2.
    From the above description, it will be noted that we do not add initial in-
stantiations for conditions of the form i ≤ c in the body of a quantified fact, nor
−1 and |a| for each sequence a, as are done in [14]. While these instantiations
are necessary for completeness, we observe that they are rarely useful in proof
goals that arise in OS verification, and can slow down (or even create loops) in
the quantifier instantiation process. We show one example of this in Section 4.4.


4.3   SMT Encoding

The third step of the algorithm converts the quantifier-free formula that results
from quantifier instantiation into a form suitable for SMT solvers.
   For structures and enumerations, a common choice for hammer-like tools
in proof assistants is to declare a new type for the structure or enumeration,
and encode field access as functions mapping the new type into the field type.
14       Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

This has the advantage of being general, in particular applicable to inductively
defined datatypes. However, they also create problems in that various axioms
about the datatype need to be added as lemmas to the SMT solver, including
definition of equality on the datatype, rewriting rules for field access, etc. The
axioms themselves have quantifiers which can complicate SMT reasoning.
    We employ an alternative approach in OSVAuto, encoding each name of a
generalized atomic term as a variable or uninterpreted function in the SMT
formula. This works because we do not allow recursion in datatype definitions.
Moreover, due to Theorem 1, all generalized atomic terms at this stage have
primitive types.
    More precisely, for each generalized atomic term t, decomposed it into the
name-indices pair (n, [i1 , . . . , ik ]) according to Section 3.4. Encode n as an SMT
variable or uninterpreted function fn with type type(i1 ) ⇒ · · · ⇒ type(ik ) ⇒
type(t). The term t is then encoded as the SMT term t(i′1 , . . . , i′k ), where i′j is the
recursively computed encoding for ij for 1 ≤ j ≤ k. The logical and arithmetic
operators are converted to corresponding SMT operations in the standard way.

Example 3. Continuing from Example 2. Designate SMT variables n1 , . . . , n12
for names s.id, t.id, s.pts.length, t.pts.length, s.pts.index.x, s.pts.index.y, t.pts.index.x,
t.pts.index.y, s.pt.x, s.pt.y, t.pt.x and t.pt.y. Here n5 through n8 are uninterpreted
functions on integers. The equality s = t is encoded as:

     n1 = n2 ∧
     (n1 = 0 −→ n3 = n4 ∧ ∀i. 0 ≤ i < n3 −→ n5 (i) = n7 (i) ∧ n6 (i) = n8 (i)) ∧
     (n1 = 1 −→ n9 = n11 ∧ n10 = n12 )

(although in practice, only versions of the above with i instantiated to concrete
values will be encoded).


4.4    Examples

In this section, we give some examples showing the algorithm in action. The
examples justify our use of conditions during propagation, omission of instantia-
tions from inequality conditions, and propagation between nodes with the same
name.


Variant of the append example We first study a variant of the running
example in [14], as reproduced in Section 2.1. The original example makes use
of the fact that equations c = append(a, b) and d = append(b, a) can be used for
rewriting. We consider a variant where a, b, c, d are all values of some map, as
follows: fix g of type Map<int, Seq<int32u>>. Assume g[2] = append(g[0], g[1])
and g[3] = append(g[1], g[0]), then show:

       (∀i. 0 ≤ i < |p[2]| → P (p[2][i])) =⇒ (∀k. 0 ≤ k < |p[3]| → P (p[3][k]))
OSVAuto: automatic proofs about functional specifications in OS verification     15

Unlike before, since g[2] and g[3] have indices, they cannot be used as rewrite
rules. The assumption g[2] = append(g[0], g[1]) expands into:

            ∀i. (0 ≤ i < |g[0]| −→ g[2][i] = g[0][i]) ∧
                (|g[0]| ≤ i < |g[0]| + |g[1]| −→ g[2][i] = g[1][i − |g[0]|])

Likewise, the assumption g[3] = append(g[1], g[2]) expands into:

           ∀j. (0 ≤ j < |g[1]| −→ g[3][j] = g[1][j]) ∧
               (|g[1]| ≤ j < |g[1]| + |g[0]| −→ g[3][j] = g[0][j − |g[1]|])

   We then get nodes i, j, g[0], g[1], g[2], g[3] in the graph, with the following
edges: i → g[0] and i → g[2] with weight 0; i → g[1] with weight −|g[0]|;
j → g[1], j → g[3] with weight 0; j → g[0] with weight −|g[1]|. This graph has
a cycle
                           i → g[0] → j → g[1] → i
with total weight |g[1]| + |g[0]| (in [14] the assumptions would be split, this does
not affect the determination of cycles).
    In [14], this non-zero cycle would prevent instantiation from converging. How-
ever, with the help of conditions, we will see the cycle is spurious. Similar to
before, the conclusion reduces to P (g[3][k]) with condition 0 ≤ k < |g[3]|. This
gives instantiation k for node g[3] under condition 0 ≤ k < |g[3]|. This instanti-
ation is first propagated to node j. When further propagated along edges g[1],
i, and g[0], eventually a condition 0 ≤ k + |g[0]| < |g[0]| arises, which implies
k < 0, contradicting the condition 0 ≤ k earlier. Hence, the last instantiation is
not added and propagation stops here. Thus the instantiation converges and the
resulting quantifier-free statement is provable.


Reasoning about uniqueness It is common in program verification to en-
counter uniqueness conditions – that is any two elements of a sequence is differ-
ent. They can be stated as follows:

        unique(a) = ∀i j. 0 ≤ i < |a| ∧ 0 ≤ j < |a| ∧ i 6= j −→ a[i] 6= a[j]

Such uniqueness conditions are not covered by the algorithm in [14]: the condition
i 6= j will produce edges with weight 1 and −1 between bound variables i and
j, which give rise to nonzero cycles (see also the analysis in Section 6).
    In our case, since we omitted instantiation on inequality conditions, we only
add edges i → a and j → a with weight 0, which themselves do not give rise to
nonzero cycles. We illustrate with the following example.
    Given a with type Seq<T>, integer k satisfying 0 ≤ k < |a|, and let b =
remove(k, a) (removing the k’th element from a). We wish to show that a has
unique elements, then b does not contain the removed element a[k]:

                 unique(a) =⇒ ∀m. 0 ≤ m < |b| −→ b[m] 6= a[k]
16       Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

First, substitute remove(k, a) for b in the goal, then expand the definition of
remove. This results in:

        0 ≤ m < max(0, |a| − 1) =⇒(0 ≤ m < k −→ a[m] 6= a[k]) ∧
                                     (k ≤ m < |a| − 1 −→ a[m + 1] 6= a[k])

    In the first round, nodes for bound variable i and sequence a are created,
with edge i → a with weight 0. The initial instantiations for a are m, m + 1, k.
This propagates to instantiations m, m + 1, k for i. Thus, unique(a) give rise to
three quantified facts over j.
    In the second round, nodes for bound variables j1 , j2 , j3 are created, with
edges j1 → a, j2 → a, j3 → a with weight 0. The following instantiations are
propagated: k for j1 and j2 , and m, m+1 for j3 . This results in four quantifier-free
facts, which are sufficient for proving the goal.

Propagation across nested sequences In this example, we demonstrate the
importance of propagation between sequence or map nodes with the same name
but different indices. The following predicate states that all rows have unique
elements for a nested sequence:

                rows_unique(a) = ∀k. 0 ≤ k < |a| −→ unique(a[k])

Now given a nested sequence a, and b is formed by removing the first element
of a[x] (0 ≤ x ≤ |a|), which expands into the following conditions:

     |b| = |a| ∧ b[x] = remove(0, a[x]) ∧ ∀y. 0 ≤ y < |a| ∧ y 6= x −→ b[y] = a[y]

We wish to show that under these conditions, row_unique(a) −→ row_unique(b).
    The full computation is rather long and we will explain only the key parts.
From the goal, we introduce variables k, i, j, assumption i 6= j, and goal b[k][i] 6=
b[k][j]. The condition b[x] = remove(0, a[x]) expands into:

                  ∀m. 0 ≤ m < |a| − 1 −→ b[x][m] = a[x][m + 1]

In the first round of instantiation, node b[k] is created with initial instantiations
i and j. Propagating these instantiations across sequence/map nodes with the
same name, we obtain instantiations i and j for b[x] (under condition x = k).
These in turn propagate to instantiations i, j, i−1, j −1 for the bound variable m,
which are necessary for proving the goal. The instantiation eventually converges,
yielding a provable quantifier-free statement.


5     Case study
We implemented the functional specification language and algorithm described
in Section 3 and 4 as the tool OSVAuto using Python. We use z3 [3] as the SMT
backend accessed through its Python API. In addition to some standard test
OSVAuto: automatic proofs about functional specifications in OS verification     17

cases (including the examples explained in Section 4.4), we mainly evaluate our
tool using the existing verification of the µC/OS-II kernel in Coq7 .
   The basic structure of the verification is already explained in Section 2.2. We
emphasize again that the current work deals only with verification of functional
properties, with combination with (semi-)automated reasoning about concurrent
separation logic left to future work. There are several aspects in the design of
µC/OS-II that are quite intricate, where verification of functional properties
requires rather lengthy reasoning:
 – Readiness of tasks at each priority is stored both in the TCB itself, as well
   as in a priority table for more efficient retrieval. They need to be updated
   consistently whenever task status changes.
 – Data about events is stored in both event control blocks and task control
   blocks. They must be updated in a consistent whenever events are sent or
   received.
 – The list of available messages in a message queue is stored in a circular
   buffer. The refinement relation between the low-level data structure (a cir-
   cular array) and the high-level data (the actual list of messages represented)
   is quite complex.
    Nested sequences and maps are used in two places in our model: for each
event, the priority table storing list of tasks waiting for the event is a sequence,
and for message queue events, the list of messages in the queue is a sequence.
    The following table summarizes API functions that are modeled in this work.
For task-related APIs, we verify preservation of invariants on TCB and prior-
ity table, and refinement relations between low-level and high-level TCBs. For
event-related APIs, we verify consistency of event information in the data struc-
tures, and refinement relation between low-leven and high-level event control
blocks. For message queues (the three OSQ functions), the correctness of the
circular buffer is verified. We emphasize that all proof obligations are verified
automatically, with the user only having to state goals on invariant and refine-
ment preservation.

6     Discussion
In [14], a proof of completeness is given for the quantifier instantiation method
proposed there. The main idea of the proof is to construct a counterexample for
the original goal by extending the model returned by the SMT solver, such that
for each sequence, the same value is used for each entry in any interval cut out
by the instantiated indexes. We give two examples showing why it is difficult to
extend the proof to cover more general situations that arise in OS verification.
 1. It is often necessary to express that a sequence contains distinct values, the
    method for building counterexamples above is inapplicable in this case (the
    same applies to the strictly-sorted condition).
7
    Source     files    and      examples      can           be      found       at
    https://anonymous.4open.science/r/OSVAuto-8F62.
18     Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

           Function            #Lines Spec      #Goals     Total Time (s)
        OSTaskSuspend              18             3              2.3
        OSTaskResume               28             3              2.5
         OSSemPend                 38             8             11.0
          OSSemPost                38             8             50.7
         OSMboxPend                50             8             11.9
         OSMboxPost                40             8             51.8
          OSQAccept                29             4             12.4
           OSQPend                 52             8             19.6
            OSQPost                46             8             56.5
      Auxiliary+Invariants      125+437
              Total                901             58            218.7
Table 1: Summary of results from the µC/OS-II case study. For each API func-
tion that are modeled, we list number of lines of specification of the function,
number of proof obligations checked, and total running time. We also list num-
ber of lines of auxiliary definitions and invariants.



2. Sometimes each entry of a sequence must satisfy additional properties related
   to its index. For example, it is common to require that for the mapping
   tcbMap from priority to TCBs, the condition ∀i. tcbMap[i].prio = i is needed.
   Again the counterexample does not work here as each value of the map must
   be different under this requirement.
We leave completeness proofs (which would require modification of the quantifier
instantiation algorithm and/or restrictions to the setting in which it applies) to
future work.


7    Related work
Most related to our work are existing research on decision procedures for ar-
rays and sequences. The array property fragment is first proposed in Bradley et
al. [2]. The work of Ge and de Moura [5] generalized this fragment to include
index offsets. The algorithm of our work builds upon that of [14], which also
provides a nice review of existing work. Other recent work on sequence the-
ory include [7], which focused regular constraints on sequences modeled using
automata. The resulting tool SeCo is applied to verify protocols such as Lam-
port’s Bakery Algorithm and Dijkstra’s Self-Stabilizing Protocol. The work [13]
proposed a number of reasoning rules about sequences, and applied them to
proof obligations from verifying smart contracts using Diem. However, none of
these work address the case where elements in the sequence can themselves be
sequences (that is, nested sequences), nor combination with structure and enu-
meration definitions. We focus on extension of automation techniques to this
case, addressing a need that arises in more complicated application scenarios.
    The difficulty with verification of operating systems by interactive theorem
proving have led researchers to consider more automatic methods in the recent
OSVAuto: automatic proofs about functional specifications in OS verification     19

years. In particular, there have been attempts at fully-automatic (push-button)
verification [11,10]. There are also semi-automatic verification tools for C [12]
and Rust [9]. The tool VST-A [16] improves automation in the Verified Soft-
ware Toolchain [1] by allowing users to perform verification using annotations.
Research on these tools focused mostly on the program logic involved. Our work
can be seen as complementary, focusing final stage of using SMT to solve the
proof obligations.


8   Conclusion
In this paper, we propose proof automation techniques for verifying functional
specifications that commonly arise in OS verification. We mainly address issues
of quantifier instantiation when nested sequences and maps are present. The
algorithm is implemented in a tool OSVAuto, and evaluated on the existing
verification of µC/OS-II kernel in Coq. The results show that the algorithm
perform well on the lengthy proof obligations that arise, with the potential to
significantly reduce proof effort when combined with other tools for reasoning
about separation logic.


References
 1. Andrew W. Appel. Verified software toolchain - (invited talk). In Gilles Barthe,
    editor, Programming Languages and Systems - 20th European Symposium on Pro-
    gramming, ESOP 2011, Held as Part of the Joint European Conferences on Theory
    and Practice of Software, ETAPS 2011, Saarbrücken, Germany, March 26-April
    3, 2011. Proceedings, volume 6602 of Lecture Notes in Computer Science, pages
    1–17. Springer, 2011.
 2. Aaron R. Bradley, Zohar Manna, and Henny B. Sipma. What’s decidable about
    arrays? In E. Allen Emerson and Kedar S. Namjoshi, editors, Verification,
    Model Checking, and Abstract Interpretation, 7th International Conference, VM-
    CAI 2006, Charleston, SC, USA, January 8-10, 2006, Proceedings, volume 3855
    of Lecture Notes in Computer Science, pages 427–442. Springer, 2006.
 3. Leonardo Mendonça de Moura and Nikolaj S. Bjørner. Z3: an efficient SMT solver.
    In C. R. Ramakrishnan and Jakob Rehof, editors, Tools and Algorithms for the
    Construction and Analysis of Systems, 14th International Conference, TACAS
    2008, Held as Part of the Joint European Conferences on Theory and Practice
    of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceed-
    ings, volume 4963 of Lecture Notes in Computer Science, pages 337–340. Springer,
    2008.
 4. Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz, Andrew
    Reynolds, and Clark W. Barrett. Smtcoq: A plug-in for integrating SMT solvers
    into coq. In Rupak Majumdar and Viktor Kuncak, editors, Computer Aided Ver-
    ification - 29th International Conference, CAV 2017, Heidelberg, Germany, July
    24-28, 2017, Proceedings, Part II, volume 10427 of Lecture Notes in Computer
    Science, pages 126–133. Springer, 2017.
 5. Yeting Ge and Leonardo Mendonça de Moura. Complete instantiation for quan-
    tified formulas in satisfiabiliby modulo theories. In Ahmed Bouajjani and Oded
20      Yulun Wu, Bican Xia, Jiale Xu, Bohua Zhan, and Tianqi Zhao

    Maler, editors, Computer Aided Verification, 21st International Conference, CAV
    2009, Grenoble, France, June 26 - July 2, 2009. Proceedings, volume 5643 of Lec-
    ture Notes in Computer Science, pages 306–320. Springer, 2009.
 6. Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim, Vil-
    helm Sjöberg, and David Costanzo. CertiKOS: An extensible architecture for
    building certified concurrent os kernels. In Kimberly Keeton and Timothy Roscoe,
    editors, 12th USENIX Symposium on Operating Systems Design and Implemen-
    tation, OSDI 2016, Savannah, GA, USA, November 2-4, 2016, pages 653–669.
    USENIX Association, 2016.
 7. Artur Jez, Anthony W. Lin, Oliver Markgraf, and Philipp Rümmer. Decision
    procedures for sequence theories. In Constantin Enea and Akash Lal, editors,
    Computer Aided Verification - 35th International Conference, CAV 2023, Paris,
    France, July 17-22, 2023, Proceedings, Part II, volume 13965 of Lecture Notes in
    Computer Science, pages 18–40. Springer, 2023.
 8. Gerwin Klein, June Andronick, Kevin Elphinstone, Toby C. Murray, Thomas
    Sewell, Rafal Kolanski, and Gernot Heiser. Comprehensive formal verification of
    an OS microkernel. ACM Trans. Comput. Syst., 32(1):2:1–2:70, 2014.
 9. Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe,
    Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. Verus: Verifying rust
    programs using linear ghost types. Proc. ACM Program. Lang., 7(OOPSLA1):286–
    315, 2023.
10. Luke Nelson, James Bornholt, Ronghui Gu, Andrew Baumann, Emina Torlak, and
    Xi Wang. Scaling symbolic evaluation for automated verification of systems code
    with serval. In Tim Brecht and Carey Williamson, editors, Proceedings of the 27th
    ACM Symposium on Operating Systems Principles, SOSP 2019, Huntsville, ON,
    Canada, October 27-30, 2019, pages 225–242. ACM, 2019.
11. Luke Nelson, Helgi Sigurbjarnarson, Kaiyuan Zhang, Dylan Johnson, James Born-
    holt, Emina Torlak, and Xi Wang. Hyperkernel: Push-button verification of an OS
    kernel. In Proceedings of the 26th Symposium on Operating Systems Principles,
    Shanghai, China, October 28-31, 2017, pages 252–269. ACM, 2017.
12. Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek
    Dreyer, and Deepak Garg. Refinedc: automating the foundational verification of
    C code with refined ownership types. In Stephen N. Freund and Eran Yahav, edi-
    tors, PLDI ’21: 42nd ACM SIGPLAN International Conference on Programming
    Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021,
    pages 158–174. ACM, 2021.
13. Ying Sheng, Andres Nötzli, Andrew Reynolds, Yoni Zohar, David L. Dill, Wolf-
    gang Grieskamp, Junkil Park, Shaz Qadeer, Clark W. Barrett, and Cesare Tinelli.
    Reasoning about vectors: Satisfiability modulo a theory of sequences. J. Autom.
    Reason., 67(3):32, 2023.
14. Qinshi Wang and Andrew W. Appel. A solver for arrays with concatenation. J.
    Autom. Reason., 67(1):4, 2023.
15. Fengwei Xu, Ming Fu, Xinyu Feng, Xiaoran Zhang, Hui Zhang, and Zhaohui Li.
    A practical verification framework for preemptive OS kernels. In Swarat Chaud-
    huri and Azadeh Farzan, editors, Computer Aided Verification - 28th International
    Conference, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part
    II, volume 9780 of Lecture Notes in Computer Science, pages 59–79. Springer, 2016.
16. Litao Zhou, Jianxing Qin, Qinshi Wang, Andrew W. Appel, and Qinxiang Cao.
    VST-A: A foundationally sound annotation verifier. Proc. ACM Program. Lang.,
    8(POPL):2069–2098, 2024.
This figure "workflow.png" is available in "png" format from:

        http://arxiv.org/ps/2403.13457v2
