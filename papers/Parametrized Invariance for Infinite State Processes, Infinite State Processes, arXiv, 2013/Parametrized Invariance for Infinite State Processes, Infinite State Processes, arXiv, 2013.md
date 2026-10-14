                                                         Parametrized Invariance for
                                                           Infinite State Processes

                                                            Alejandro Sánchez1 and César Sánchez1,2
                                                            1
                                                            IMDEA Software Institute, Madrid, Spain
                                                        2
                                                          Institute for Information Security, CSIC, Spain
                                                        {alejandro.sanchez,cesar.sanchez}@imdea.org
arXiv:1312.4043v2 [cs.LO] 9 Jan 2014




                                             Abstract. We study the uniform verification problem for infinite state
                                             processes, which consists of proving that the parallel composition of an
                                             arbitrary number of processes satisfies a temporal property. Our practical
                                             motivation is to build a general framework for the temporal verification
                                             of concurrent datatypes.
                                             The contribution of this paper is a general method for the verification
                                             of safety properties of parametrized programs that manipulate complex
                                             local and global data, including mutable state in the heap. This method
                                             is based on the separation between two concerns: (1) the interaction
                                             between executing threads—handled by novel parametrized invariance
                                             rules—,and the data being manipulated—handled by specialized decision
                                             procedures. The proof rules discharge automatically a finite collection of
                                             verification conditions (VCs), the number depending only on the size of
                                             the program description and the specification, but not on the number
                                             of processes in any given instance or on the kind of data manipulated.
                                             Moreover, all VCs are quantifier free, which eases the development of
                                             decision procedures for complex data-types on top of off-the-shelf SMT
                                             solvers.
                                             We discuss the practical verification (of shape and also functional correct-
                                             ness properties) of a concurrent list implementation based on the method
                                             presented in this paper. Our tool also all VCs using a decision procedure
                                             for a theory of list layouts in the heap built on top of state-of-the-art
                                             SMT solvers.


                                       1   Introduction
                                       In this paper we present a general method to verify concurrent software which is
                                       run by an arbitrary number of threads that manipulate complex data, including
                                       infinite local and shared state. Our solution consists of a method that cleanly
                                       separates two concerns: (1) the data, handled by specialized decision procedures;
                                       and (2) the concurrent thread interactions which is handled by novel proof rules,
                                       that we call parametrized invariance. The method of parametrized invariance
                                       tackles, for safety properties, the uniform verification problem for parametrized
                                       systems with infinite state processes:
                                         Given a parametrized system S[N ] : P (1) k P (2) k . . . k P (N ) and a property ϕ
                                         establish whether S[N ]  ϕ for all instances N ≥ 1.
2

    In this paper we restrict to safety properties. Our method is a generalization
of the inductive invariance rule for temporal deductive verification [23], in which
each verification condition corresponds to a small-step (a single transition) in
the execution of a system. For non-parametrized systems, there is always a finite
number of transitions, so one can generate one VC per transition. However, in
parametrized systems, the number of transitions depends on the concrete number
of processes in each particular instantiation.
    The main contribution of this paper is the principle or parametrized invari-
ance, presented as proof rules that capture the effect of single steps of threads
involved in the property and extra arbitrary threads. The parametrized invari-
ance rules automatically discharge a finite number of VCs, whose validity im-
ply the correctness for all system instantiations. For simplicity we present the
rules for fully symmetric systems (in which thread identifiers are only compared
with equality) and show that all VCs generated are quantifier-free (as long as
transition relations and specifications are quantifier-free, which is the case is
conventional system descriptions).
    For many data-types one can use directly SMT solvers [15,25], or specialized
decision procedures built on top. We show here how to use the decision procedure
for a quantifier-free theory of single linked list layouts with locks [27] to verify
fine-grained concurrent list implementation. Other powerful logics and tools for
building similar decision procedures include [20, 22].

Related Work. The problem of uniform verification of parametrized systems
has received a lot of attention in recent years. This problem is, in general, un-
decidable [3], even for finite state components. There are two general ways to
overcome this limitation: deductive proof methods as the one we propose here,
and (necessarily incomplete) algorithmic approaches.
    Most algorithmic methods are restricted to finite state processes [7, 8, 11] to
obtain decidability. Examples are synchronous communication processes [13,16];
systems with only conjunctive guards or only disjunctive guards [11]; implicit
induction [12]; network invariants [21]; etc. A related technique, used in para-
metrized model checking, is symmetry reduction [9,14]. A very powerful method
is invisible invariants [4, 26, 29], which works by generating invariants on small
instantiations and generalizing these to parametrized invariants. However, this
method is so far also restricted to finite state processes.
    A different tradition of automatic (incomplete) approaches is based on ab-
stracting control and data altogether, for example representing configurations
as words from a regular language [1, 2, 19, 24] Other approaches use abstraction,
like thread quantification [5] and environment abstraction [10], based on similar
principles as the full symmetry presented here, but relying on building specific
abstract domains that abstract symbolic states instead of using SMT solvers.
    In contrast with these methods, the verification framework we present here
can handle infinite data. The price to pay is, of course, automation because
one needs to provide some support invariants. We see our line of research as
complementary to the lines mentioned above. We start from a general method
and investigate how to improve automation as opposed to start from a restricted
                                                                                  3

automatic technique and improve its applicability. The VCs we generate can still
be verified automatically as long as there are decision procedures for the data
that the program manipulates.
    Our target application is the verification of concurrent datatypes [18], where
the main difficulty arises from the mix of unstructured unbounded concurrency
and heap manipulation. Unstructured refers to programs that are not struc-
tured in sections protected by locks but that allow a more liberal pattern of
shared memory accesses. Unbounded refers to the lack of bound on the num-
ber of running threads. Concurrent datatypes can be modeled naturally as fully
symmetric parametrized systems, where each thread executes in parallel a client
of the datatype. Temporal deductive methods [23], like ours, are very powerful
to reason about (structured or unstructured) concurrency.
    The rest of the paper is structured as follows. Section 2 includes the prelimi-
naries. Section 3 introduces the parametrized invariance rule. Section 4 contains
the examples, a description of our tool and empirical evaluation results. Finally,
Section 5 concludes.


2   Running Example and Preliminaries

Running Example. We will use as a running example a concurrent data-
type that implements a set [18] using fine-grain locks, shown in Fig. 2. Ap-
pendix A contains simpler and more detailed examples of infinite state mutual
exclusion protocols. Lock-coupling concurrent lists implement sets by maintain-
ing an ordered list of non-repeating elements. Each node in the list stores an
element, a pointer to the next node in the list and a lock used to protect con-
current accesses. To search an element, a thread advances through the list ac-
quiring a lock before visiting a node. This lock is only released after the lock
of the next node has been acquired. Concurrent lists also maintain two sentinel
nodes, head and tail , with phantom values representing the lowest and high-
est possible values, −∞ and +∞ respectively. Sentinel nodes are not modified
at runtime. We define two “ghost” variables that aid the verification: reg, a
set of addresses that contains the set of address pointing to nodes in the list;
                                     and elems, a set of elements we use to
       procedure MGC                 keep track of elements contained in the
         Elem e
                                     list. Ghost variables are compiled away and
       begin
    1: while true do
                                     are only used in the verification process.
    2:    e := havocListElem()       In Fig. 2 ghost variables and code appear
    3:    nondet call Search(e)      inside a box. As lock-coupling lists imple-
            or     call Insert(e)    ment sets, three main operations are pro-
            or     call Remove(e)    vided: (a) Search: finds an element in the
    4: end while                     list; (b) Insert: adds a new element to the
       end procedure                 list; and (c) Remove: deletes an element in
                                     the list. For verification purposes, it is com-
    Fig. 1: Most General Client      mon to define the most general client MGC
  4

      global                         procedure Insert(e)                   procedure Remove(e)
        Addr head ;                     Addr prev                             Addr prev
        Addr tail ;                     Addr curr                             Addr curr
        SethAddr i reg;                 Addr aux                              Addr aux
        SethElemi elems;             begin                                 begin
                                 20: prev := head                      39: prev := head
                                 21: prev→lock ()                      40: prev→lock ()
                                 22: curr := prev→next                 41: curr := prev→next
    procedure Search(e)          23: curr→lock
      Addr prev                              ()                      42: curr→lock
                                                                                   ()               
                                               curr 6= null ∧                        icurr 6= tail ∧
      Addr curr                  24: while                       do    43: while                       do
                                              curr→data < e                         curr→data < e
      Bool found                 25:     aux := prev                   44:     aux := prev
    begin                        26:     prev := curr                  45:     prev := curr
 5: prev := head                 27:     aux→unlock ()                 46:     aux→unlock ()
 6: prev→lock ()                 28:     curr := curr→next             47:     curr := curr→next
 7: curr := prev→next            29:     curr→lock ()                  48:     curr→lock ()
 8: curr→lock                    30: end while                       49: end while            
 9: while curr→data < e do                curr ! = null ∧                        curr 6= tail ∧
                                 31: if                      then      50: if                       then
10:    aux := prev                        curr→data > e                         curr→data = e
11:    prev := curr              32:     aux := malloc(e, null , #)    51:     aux := curr→next
12:    aux→unlock ()             33:     aux→next := curr              52:     prev→next := aux
13:    curr := curr→next         34:     prev→next := aux                      reg := reg \ {curr}
14:    curr→lock ()                      reg := reg ∪ {aux }                   elems := elems \ {e}
15: end while                            elems := elems ∪ {e}          53: end if
16: found := (curr→data = e)     35: end if                            54: prev→unlock ()
17: prev→unlock ()               36: prev→unlock ()                    55: curr→unlock ()
18: curr→unlock ()               37: curr→unlock ()                    56: return
19: return found                 38: return                                end procedure
    end procedure                    end procedure

                Fig. 2: Lock-coupling single linked list implementation


  shown in Fig. 1. Each process in the parametrized system runs MGC choosing
  non-deterministically a method and its parameters.

  Preliminaries. Our verification task starts from a program, and a safety prop-
  erty described as a state predicate. A system is correct if all states in all the
  traces of the transition system that models the set of executions of the program
  satisfy the safety property.
      A transition system is a tuple S : hV , Θ, T i where V is a finite set of (typed)
  variables, Θ is a first-order assertion over the variables which describes the pos-
  sible initial states, and T is a finite set of transitions. We model program data
  using multi-sorted first order logic. A signature Σ : (S, F, P ) consists of a set of
  sorts S (corresponding to the types of the data that the program manipulates),
  a set F of function symbols, and a set P of predicate symbols. We use Σprog for
  the signature of the datatypes in a given program and Tprog for the theory that
  allows to reason about formulas in Σprog . A state is an interpretation of V that
  assigns a value of the corresponding type to each program variable. A transition
                                                                                         5

  To show that S satisfies ϕ:                  To show that S satisfies p, find q with:

       B1.         Θ→ϕ                                I1.        Θ→q
       B2.      ϕ ∧ τ → ϕ0    for all τ               I2.    q ∧ τ → q0    for all τ
                                                      I3.         q→ϕ
                     ϕ                                           ϕ
    (a) The basic invariance rule b-inv               (b) The invariance rule inv

             Fig. 3: Rules b-inv and inv for non-parametrized systems.


is represented by a logical relation τ (s, s0 ) that describes the relation between
the values of the variables in a state s and a successor state s0 . A run of S is an
infinite sequence s0 τ0 s1 τ1 s2 . . . of states and transitions such that (a) the first
state is initial: s0  Θ; (b) all steps are legal: τi (si , si+1 ), that is, τi is taken at
si , leading to state si+1 .
     A system S satisfies a safety property ϕ, which we write S  ϕ, whenever
all runs of S satisfy ϕ at all states. For non-parametrized systems, invariants can
be proved using the classical invariance rules [23], shown in Fig. 3. The basic
rule b-inv establishes that if the candidate invariant ϕ holds initially and is
preserved by every transition then ϕ is indeed an invariant. Rule inv uses an
intermediate strengthening invariant q. If q implies ϕ and q is an invariant, then
ϕ is also an invariant. For non-parametrized systems, the premises in these rules
discharge a number of verification conditions linear in the number of transitions.
To use these invariance rules for parametrized systems, one either needs to use
quantification or discharge an unbounded number of VCs, depending on the
number of processes.


Parametrized Concurrent Programs. Parametrized programs consist of the
parallel execution of process running the same program (the extension to an
unbounded number of processes each running a program from a finite collection is
trivial). We assume asynchronous interleaving semantics for parallel composition.
A program is described as a sequence of statements, each assigned to a program
location in the range Loc : 1 . . . L. Each instruction can manipulate a collection of
typed variables partitioned into Vglobal , the set of global variables, and Vlocal , the
set of local variables. There is one special local variable pc of sort Loc that stores
the program counter of each thread. For example, for the program in Fig. 2,
Tprog is the combination of TLL3 (the theory of single-linked lists in the heap
with locks [27]), combined with finite discrete values (for program locations). In
transition relations we use a primed variable v 0 to denote the value of variable
v after a transition is taken.
    A parametrized program P is associated with a parametrized system S, a
collection of transition systems S[M ], one for each number of running threads.
We use [M ] to denote the set {0, . . . , M − 1} of concrete thread identifiers. For
each M , there is a system S[M ] : hV , Θ, T i consisting of:
6

    – The set V of variables is Vglobal ∪ {v[k]} ∪ {pc[k]} where there is one v[k] for
      each v ∈ Vlocal and for each k ∈ [M ], and one pc[k] for each k ∈ [M ].
    – An initial condition Θ, which is described by two predicates Θg (that only
      refers to variables from Vglobal ) and Θl (that can refer to variables in Vglobal
      and Vlocal ). Given a thread identifier a ∈ [M ] for a concrete system S[M ],
      Θl [a] is the initial condition for thread a, obtained by replacing v[a] for every
      occurrence of v in Θl .
    – T contains a transition τ` [a] for each location and thread a in [M ] obtained
      from τ` by replacing every occurrence of v by v[a], and of v 0 by v 0 [a].
      We use V t to denote all variables of sort t in set V .

Example 1. Consider the lock-coupling list program in Fig. 2. The instance of
this program consisting of two running threads contains the following variables:
     V = {head , tail , reg, elems, e[0], prev [0], curr [0], aux [0], found [0],
                                  e[1], prev[1], curr [1], aux [1], found [1]}
There are 118 transitions in MGC[2], 59 transitions for each thread, one for
each line in the program. For non-parametrized systems, like MGC[2], we use
the predicate pres in transition relations to list the variables that are not changed
by the transition. That is pres(head , tail ) is simply a short for head 0 = head ∧
tail 0 = tail .


3      Parametrized Formulas and Parametrized Proof Rules

We show in this paper how to specify and prove invariant properties of parame-
trized systems. Unlike in [26] we generate quantifier-free verification conditions,
enabling the development of decision procedures for complex datatypes.
    To model thread ids we introduce the sort tid interpreted as an unbounded
discrete set. The signature Σtid contains only = and 6=, and no constructor.
We enrich Tprog using the theory of arrays TA (see [6]) with indices from tid
and elements ranging over sorts t from the local variables of Tprog . For each
local variable v of type t in the program, we add a global variable av of sort
arrayhti, including apc for the program counter pc. The expression av (k) denotes
the element of sort t stored in array av at position given by expression k of sort
tid. The expression av {k ← e} corresponds to an array update, and denotes the
array that results from av by replacing the element at position k with e. To
simplify notation, we use v(k) for av (k), and v{k ← e} for av {k ← e}. Note how
v[0] is different from v(k): the term v[0] is an atomic term in V (for a concrete
system S[M ]) referring to the local program variable v of a concrete thread with
id 0. On the other hand, v(k) is a non-atomic term built using the signature of
arrays, where k is a variable (logical variable, not program variable) of sort tid.
    Variables of sort tid indexing arrays play a special role, so we classify formu-
las depending on the sets of variables used. The parametrized set of program
variables with index variables X of sort tid is:

                  Vparam (X) = Vglobal ∪ {av | v ∈ Vlocal } ∪ {apc } ∪ X
                                                                                       7

We use T for the union of theories Tprog , Ttid and TA . FT (X) is the set of first-
order formulas constructed using predicates and symbols from T and variables
from Vparam (X). Given a tid variable k and a program statement, we construct
the parametrized transition relation as before, but using array reads and updates
(to position k) instead of concrete local variable reads and updates. For para-
metrized formulas, the predicate pres is defined with array extensional equality
for unmodified local variables.
    We similarly define the parametrized initial condition for a given set of thread
identifiers X as:                           ^
                             Θ(X) : Θg ∧         Θl (k)
                                               k∈X

where Θl (k) is obtained by replacing every local variable v in Θl by v(k).
    A parametrized formula ϕ(k) with free variables k = (k0 , . . . , kn ) of sort tid is
a formula from FT ({k0 , . . . , kn }). Note, in particular, how parametrized formulas
cannot refer to any constant thread identifier. We use Var (ϕ) for the set of free
tid variables in ϕ.
    Given a concrete number of threads N , a concretization of expression p(k) is
characterized by a substitution α : k → [N ] that assigns to each variable in k a
unique constant thread identifier in the instance system S[N ]. The application
of α for expressions p is defined inductively, where the base cases are:

                     α(v(ki )) 7→ v[α(ki )]
                                                           V                       
          α(w = v{ki ← e}) 7→        w[α(ki )] = e ∧                 w[a] = v[a]
                                                       a∈N \α(ki )


Essentially, a concretization provides the state predicate for system S[N ] that
results from p(k) by instantiating k according to α.
    We can formulate the uniform verification problem in terms of concretiza-
tions. Given a parametrized system S, a universal safety property of the form
∀k . p(k) holds whenever for every N and substitution α : k → [N ], the con-
crete closed system S[N ] satisfies S[N ]  α(p(k)). In this case we simply write
S  p and say that p is a parametrized invariant of S.
    A naı̈ve approach to prove parametrized inductive invariants is to enumerate
all instances and repeatedly use rule inv for each one. However, this approach
requires proving an unbounded number of verification conditions because one
(potentially different) VC is discharged per transition and thread in every in-
stantiated closed system.


Parametrized Proof Rules. We introduce here specialized proof rules for
parametrized systems, which allow to prove parametrized invariants discharging
only a finite number of verification conditions. Rule p-inv in Fig. 4 presents
the basic parametrized invariance rule. Premise P1 guarantees that the initial
condition holds for all instantiations. Premise P2 guarantees that ϕ is preserved
under transitions of the threads referred in the formula, and P3 guarantees that
ϕ is preserved under transitions of any other thread. P1 discharges only one
8


        To show that S satisfies ϕ(k), with k = Var (ϕ):

          P1.                     Θ(k) → ϕ
          P2.                  ϕ ∧ τ (i) → ϕ0              forall τ and all i ∈ k
                                        (j)        0
                      V                                
          P3. ϕ ∧          j 6= x ∧ τ         →ϕ           forall τ and one fresh j ∈
                                                                                    /k
                     x∈k
                                   ϕ

                 Fig. 4: The parametrized invariance rule p-inv


verification condition, P2 discharges one VC per transition in the system and
per index variable in the formula ϕ. Finally, P3 generates one extra VC per
transition in the system. All these VCs are quantifier-free provided that ϕ is
quantifier-free. The following theorem justifies the introduction of rule p-inv:

Theorem 1 (Soundness). Let S be a parametrized system and ϕ a parame-
trized safety property. If P1, P2 and P3 hold, then S  ϕ.

Proof. (sketch) The proof proceeds by contradiction, assuming that the premises
           6 ϕ. There must be an N and a concretization α for which S[N ] 6
hold but S 
α(ϕ). Hence, by soundness of the inv rule for closed systems, there must be
a premise of inv that is not valid. By cases, one uses the counter-model of the
offending premise to build a counter-model of the corresponding premise in p-
inv.                                                                          t
                                                                              u

    There are cases in which premise P3 cannot be proved, even if ϕ is initial and
preserved by all transitions of all threads. The reason is that, in the antecedent
of P3, ϕ does not refer to the fresh arbitrary thread introduced. In other words,
p-inv tries to prove the property for an arbitrary process at all reachable system
states without assuming anything about any other thread. It is sound, however,
to assume in the pre-state and for all processes the property one intends to
prove. The notion of support allows to strengthen the antecedent to refer to all
threads involved in the verification condition, including the fresh new thread.

Definition 1 (support). Let ψ be a parametrized formula (the support) and
let (A → B) be a parametrized formula
                                    V      with Var (A → B) = X. We say that
ψ supports (A → B), whenever           σ∈S ψσ ∧ A → B is valid, where S is a
subset of the partial substitutions Var (ψ) * X.
                                                 V              
    We use ψ  (A → B) as a short for ( σ∈S ψσ ∧ A → B). We can
strengthen premise P3 with self-support, so ϕ can be assumed (in the pre-state)
for every thread, in particular for the fresh thread that takes the transition:

                    V                              
       P30 . ϕ           j 6= x ∧ τ (j) → ϕ0              forall τ and one fresh j ∈
                                                                                    /k
                    x∈k
                                                                                       9


   To show that S satisfies ϕ(k). Find ψ with:

        S0.                               ψ
        S1.                               Θ→ϕ
        S2.   ψ, ϕ                   τ (i) → ϕ0         forall τ and all i ∈ k
              ψ, ϕ                       (j)        0
                       V
        S3.                  j 6= x ∧ τ         →ϕ       forall τ and one fresh j ∈
                                                                                  /k
                       x∈k
                                          ϕ

    Fig. 5: The general strengthening parametrized invariance rule sp-inv.


   For example, let ϕ(i) be a candidate invariant with one thread variable (an
index 1 invariant candidate). Premise P30 is ϕ  (j 6= i ∧ τ (j) → ϕ0 (i)) , or
equivalently                                      
                      ϕ(j) ∧ ϕ(i) ∧ j 6= i ∧ τ (j) → ϕ0 (i).
Note how ϕ(j) in the antecedent is the result of instantiating ϕ for the fresh
thread j. Rule p-inv can fail to prove invariants if they are not inductive. As for
closed systems, one needs to strengthen invariants. However, it is not necessary
the case that by conjoining the candidate and its strengthening one obtains a p-
inv inductive invariant. Instead, one needs to use a previously proved invariant
as support to consider also freshly introduced process identifiers. This idea is
captured by rule sp-inv in Fig. 5.
Theorem 2. Let S be a parametrized system and ϕ a parametrized safety
property. If S0, S1, S2 and S3 hold, then S  ϕ.


Graph Proof Rules We now introduce a final specialized proof rule for pa-
rametrized systems. When using sp-inv, S0 requires to start from an already
proved invariant. However, in some cases invariants mutually depend on each
other. For example, in the proof of shape preservation of concurrent single-linked
list programs, like the one in Fig. 2, one requires that the pointers curr and prev
used in the list traversal do not alias. This fact depends on the list having at
all program states the shape of a non-cyclic list. A correct but naı̈ve solution
would be to write down all necessary conditions as a single formula and prove it
invariant using p-inv. Unfortunately, this approach does not scale when using
sophisticated decision procedures for infinite memory. A more efficient approach
consists on building the proof modularly, splitting the invariant into meaningful
subformulas to be used when required. Modularity motivates the introduction of
g-inv, a rule for proof graphs shown in Fig. 6. This rule handles cases in which
invariants that mutually dependent on each other need to be verified.
     A proof graph (V, E) has candidate invariants as nodes. An edge between
two nodes indicates that in order to prove the formula pointed by the edge it is
useful to use the formula at the origin of the edge as support. As a particular
case, a formula with no incident edges is inductive and can be shown with p-inv.
10

     To show that S satisfies ϕ find a proof graph (V, E) with ϕ ∈ V such that:

       G1.                               Θ→ψ            forall ψ ∈ V
       G2.   Φ, ψ                  τ (k) → ψ 0         forall ψ ∈ V , forall τ ,
                                                             and all k ∈ Var (ψ),
                                                             and Φ = {ψi | (ψi , ψ) ∈ E}
             Φ, ψ                       (k)        0
                      V
       G3.                  k 6= x ∧ τ         →ϕ       forall ψ ∈ V , forall τ ,
                      x∈v
                                                             one fresh k ∈
                                                                         / v = Var (ψ),
                                                             and Φ = {ψi | (ψi , ψ) ∈ E}
                                         ϕ

              Fig. 6: The graph parametrized invariance rule g-inv.


Theorem 3. Let S be a parametrized system and (V, E) a proof graph. If G1,
G2, and G3 hold, then S  ψ for all ψ ∈ V .

Proof. By contradiction assume that some formula in V is not an invariant.
Then, consider a shortest path to a violation in any concrete system S[M ]. Let
ψ ∈ V be the violated formula. By G1 , the path cannot be empty because G1
implies initiation of all formulas in V for all concrete system instances. Hence,
the offending state s violating ψ has a predecessor state spre in the path, which by
assumption, satisfies all formulas in V , and in particular all formulas in {ψi | ψ ∈
E} i.e., with outgoing edges incident to ψ. Premises G2 and G3, guarantee that
the execution step from spre to s guarantees ψ in s, which is a contradiction. t    u

   We now show not that for fully symmetric systems, the dependencies with
arrays in the parametrized formulas can be eliminated preserving validity, gen-
erating formulas that decision procedures can reason about.

Theorem 4 (Concretization).
               V                 Let ϕ(k) be with |k| = n. Then ϕ(k) is valid
if and only if   α(ϕ) is valid where A is the set of all possible assignments of
               α∈A
variables in Var (ϕ) to [n].

   For example, if one intends to prove that p(i) is inductive, the concretization
theorem allows to reduce P3 in p-inv to (p[0] ∧ τ [1] → p0 [0]), where p[0] is a
short for α(p(i)) with α : i → 0. This formula involves no arrays. Similarly, to
show p(i) with support invariant q(j), rule S3 can be reduced to:

                       q[0] ∧ q[1] ∧ p[0] ∧ p[1] ∧ τ [1] → p0 [0]

   In practice, the concretization can be performed upfront before discharging
the verification condition to the SMT-Solver, or handled using the theory of
uninterpreted functions and let the solver perform the search and propagation.
                                                                                 11

4     Implementation and Empirical Evaluation
We illustrate the use of our parametrized invariance rules proving list shape
preservation and some functional properties about set representation of the con-
current list implementation presented in Fig. 2. We also show mutual exclusion
for some infinite state protocols that use integers and sets of integers (see the
appendix for details).
    The proof rules are implemented in the temporal theorem prover tool Leap,
under development at the IMDEA Software Institute3 . Leap parses a temporal
specification and a program descriptions in a C-like language. Leap automat-
ically generates VCs applying the parametrized invariance rules presented in
this paper. The validity of each VC is then verified using a suitable decision
procedure (DP) for each theory.
    We compare here three decision procedures built on top the SMT solvers Z3
and Yices: (1) a simple DP that can reason only about program locations, and
considers all other predicates as uninterpreted; (2) a DP based on TLL3 capa-
ble of reasoning about single-linked lists layouts in the heap with locks to aid
in the verification of fine-grain locking algorithms; and (3) a DP that reasons
about program locations, integers and finite sets of integers with minimum and
maximum functions (for the mutual exclusion protocols). The last two decision
procedures and their implementation are based on small model theorems. The
satisfiability of a quantifier free formula is reduced to the search for a model
(up to a sufficiently large size). Leap also implements some heuristic optimiza-
tions (called tactics) like attempting first to use a simpler decision procedure
or instantiating support lazily. This speeds the solvers in many valid instances
by reducing the formulas obtained by partial assignments in the application of
rules sp-inv or g-inv.

List Preservation and Set Representation for Concurrent Lists. We
prove that the program in Fig. 2 satisfies: (1) list shape preservation; and (2) the
list implements a set, whose elements correspond to those stored in elems. The
theory TLL3 (see [27]) allows to reason about addresses, elements, locks, sets,
order, cells (i.e., list nodes), memory and list reachability. A cell is a struct
containing an element, a pointer to next node in the list and lock to protect the
cell. A lock is associated with operations lock and unlock to acquire and release.
The memory (heap) is modeled as an array of cells indexed by addresses. The
specification is:
        
         null ∈ reg ∧ reg = addr2set(heap, head ) ∧ head 6= tail          ∧ (L1)
        
        
         heap[tail ].next = null ∧ tail 6= null ∧ head 6= null            ∧ (L2)
 ϕlst =
      ˆ
        
         heap[head   ].data = −∞  ∧ heap[tail ].data =  +∞                ∧ (L3)
        
        
          elems = set2elemset(heap, reg) ∧ Ordered (heap, head , tail )        (L4)
Formula ϕlst is 0-index since it only constrains global variables. (L1) establishes
that null belongs to reg and that reg is exactly the set of addresses reachable in
3
    Available at http://software.imdea.org/leap
12

the heap starting from head , which ensures that the list is acyclic. (L2) and (L3)
express some sanity properties of the sentinel nodes head and tail . Finally, (L4)
establishes that elems is the set of elements in cells referenced by addresses in
reg, and that the list is ordered. The main specification is list, defined as ϕlst .
    Using p-inv, Leap can establish that list holds initially, but fails to prove
that list is preserved by all transitions. The use of decision procedures for proving
VCs allows to obtain counter-examples as models of an execution step that
leads to a violation of the desired invariant. Leap parses the counterexample
(model) returned by the SMT solver, which is usually very small, involves only
few threads and allows to understand the missing intermediate facts. In practice,
these models allow to write easily the support invariants. We introduce some
support invariants that allow to prove list.
    Invariant region(i) describes that local variables prev , curr and aux point
to cells within the region of the list reg, and that these variables cannot be
null or point to head or tail . The formula region is 1-index (because it needs to
refer to local variables of a single thread). Invariant next(i) captures the relative
position in the list of the cells pointed by head and tail and local variables prev ,
curr and aux . This invariant is needed for (L2). To prove (L3) and (L4) we
need to show that order is preserved. We introduce order(i), which captures the
increasing order between the data in cells pointed by curr , prev and aux and
by the searched, inserted or removed element e. Invariant lock(i) captures those
program locations at which a thread owns a cell in the heap by an acquired
lock. Finally, disj(i, j), defined as ϕdis (i, j) encodes that the calls to malloc by
different threads return different addresses:
                 ˆ (i 6= j ∧ pc(i) = 33, 34 ∧ pc(j) = 33, 34) → aux I (i) 6= aux I (j)
     ϕdis (i, j) =
    Other properties verified for the concurrent list are functional like specifica-
tions. Invariant funSchLinear(i) establishes that the result of Search matches
with the presence of the searched element e at Search’s linearization point;
funSchInsert(i) states that if a search is successful then e was inserted earlier in
the history; and funSchRemove(i) captures the fact that if the search is unsuc-
cessful then either e was never inserted or it was removed, and it was not present
at the linearization point of Search. The invariants funRemove(i), funInsert(i)
and funSearch(i) consider the case in which one thread handles different elements
than all other threads. In this case, the specification is similar to a sequential
functional specification (an element is found if and only if it is in the list, an
element is not present after removal and an element is present after insertion).

Infinite State Mutual Exclusion Protocols. We also report the proof of
mutual exclusion of some simple infinite state protocols that use tickets. The first
protocol uses two global integer variables, one to store the next available ticket,
and another to represent the minimum ticket present. The decision procedure
used is Presburger arithmetic. The second protocol stores the tickets in a global
set of integers, and queries for the minimum element in the set. The decision
procedure used is Presburger Arithmetic combined with finite sets of integers
with minimum.
                                                                                     13

                   formula info #solved vc Full supp Supp       Offend     Tactics
                   index #vc pos dp         time(s) time(s)     time(s)    time(s)
            list      0    61    38   23        TO        TO         TO       12.85
          order       1   121    62   59     998.35      7.56       2.69       1.20
           lock       1   121    76   45     778.15      4.82       1.44       0.50
           next       1   121    60   61        TO        TO       26.58       1.76
         region       1   121    95   26        TO        TO       85.27      25.67
            disj      2   181   177    4     121.74      1.29       1.29       0.22
      funSearch       1   208   198   10        TO        TO        6.14       4.55
       funInsert      1   208   200    8        TO        TO        2.04       0.51
     funRemove        1   208   200    8        TO        TO        2.73       1.56
   funSchLinear       1   121    97   24        TO        TO      82.13        4.63
    funSchInsert      1   121    93   28        TO        TO      80.20        5.00
 funSchRemove         1   121    93   28        TO        TO     110.84        5.49
         mutex        2   28     26    2       0.32      0.23       0.10       0.01
      minticket       1   19     18    1       0.04      0.04       0.01       0.01
       notsame        2   28     26    2       0.13      0.13       0.10       0.02
      activelow       1   19     17    2       0.01      0.01       0.01       0.01
        mutexS        2   28     26    2       0.44      0.38       0.14       0.04
     minticketS       1   19     18    1       0.31      0.18       0.08       0.01
      notsameS        2   28     26    2       0.14      0.13       0.10       0.02
     activelowS       1   19     17    2       0.02      0.02       0.02       0.01

     Fig. 7: VCs proved using each decision procedure and running times.

    Fig. 8 shows the proof graph encoding the proof of list. Leap can read proof
graphs and apply g-inv. Fig. 7 contains the results of this empirical evaluation,
executed on a computer with a 2.8 GHz processor and 8GB of memory. Each row
reports the results for a single invariant. The first four columns show the index
of the formula, the total number of generated VCs, the number of VCs proved by
position, and the remaining VCs. The next four columns show the total running
time using the specialized decision procedures with different tactics: “Full supp”
corresponds to instantiating all support invariants for all VCs; “Supp” corre-
sponds to instantiate only the necessary support; “Offend” corresponds to only
using support in potentially offending transitions; “Tactics” reports the running
time needed using some basic tactics like lazy instantiation and formula nor-
malization and propagation. TO represents a timeout of 30 minutes. Our results
                                  indicates that, in practice, tactics are essential
             order                for efficiency when handling non-trivial examples
               list               such as concurrent lists. Even though our de-
                                  cision procedures have room for improvements,
   next       lock    region      these results suggest that trying to compute an
               disj               over-approximation of the reachable state space
                                  for complicated algorithms by iteratively com-
                                  puting formulas is not likely to be feasible for
Fig. 8: Invariant dependencies complicated heap manipulating programs.
14

5    Concluding Remarks

This paper has introduced a temporal deductive technique for the uniform veri-
fication problem of safety properties of infinite state processes, in particular for
the verification of concurrent datatypes that manipulate data in the heap. Our
proof rules automatically discharge a finite collection of verification conditions,
which depend on the program description and the diameter of the formula to
prove, but not on the number of threads in a particular instance. Each VC de-
scribes a small-step in the execution of all corresponding instances. The VCs are
quantifier-free as long as the formulas are quantifier free. We use the theory of
arrays [6] to encode the local variables of a system with an arbitrary number of
threads, but the dependencies with arrays can be eliminated, under the assump-
tion of full symmetry. It is immediate to extend our framework to a finite family
of process classes, for example to model client/server systems.
    Future work includes invariant generation to simplify or even automate proofs.
We are studying how to extend the decision procedures with the calculation of
weakest precondition formulas (like [20]) and its use for parametrized systems
effectively to infer invariants, possibly from the target invariant. We are also
studying how to extend the “invisible invariant” approach [4,26,29] to processes
that manipulate infinite state, by instantiating small systems with a few threads
and limiting the exploration to only states where data is limited in size as well.
All candidate invariants produced must then be verified with the proof rules
presented here for the general system.
    We are also extending our previous work on abstract interpretation-based
invariant generation for parametrized systems [28] to handle complex datatypes.
Our work in [28] was restricted to numerical domains.
    Finally, another approach that we are currently investigating is to use the
proof rules presented here to enable a Horn-Clause Verification engine [17] to
automatically generate parametrized invariants guided by the invariant candi-
date goal. Our preliminary results are very promising but out of the scope of
this paper.
    From a theoretical viewpoint the rule sp-inv is complete (all invariants can
be proved by support inductive invariants), but the proof of completeness is
rather technical and is also out of the scope of this paper.


References
 1. Abdulla, P.A., Bouajjani, A., Jonsson, B., Nilsson, M.: Handling global conditions
    in parametrized system verification. In: Proc. of CAV’99. pp. 134–145 (1999)
 2. Abdulla, P.A., Delzanno, G., Rezine, A.: Approximated parameterized verification
    of infinite-state processes with global conditions. FMSD 34(2), 126–156 (2009)
 3. Apt, K.R., Kozen, D.C.: Limits for automatic verification of finite-state concurrent
    systems. Info. Proc. Letters 22(6), 307–309 (1986)
 4. Arons, T., Pnueli, A., Ruah, S., Xu, J., Zuck, L.D.: Parameterized verif. with
    automatically computed inductive assertions. In: Proc. of CAV’01. pp. 221–234
    (2001)
                                                                                      15

 5. Berdine, J., Lev-Ami, T., Manevich, R., Ramalingam, G., Sagiv, S.: Thread quan-
    tification for concurrent shape analysis. In: Proc. of CAV’08. pp. 399–413 (2008)
 6. Bradley, A.R., Manna, Z., Sipma., H.B.: What’s decidable about arrays? In: VM-
    CAI’06. LNCS, vol. 3855, pp. 427–442. Springer (2006)
 7. Clarke, E.M., Grumberg, O.: Avoiding the state explosion problem in temporal
    logic model checking. In: PODC’87. pp. 294–303. ACM (1987)
 8. Clarke, E.M., Grumberg, O., Browne, M.C.: Reasoning about networks with many
    identical finite-state processes. In: PODC’86. pp. 240–248. ACM (1986)
 9. Clarke, E.M., Jha, S., Enders, R., Filkorn, T.: Exploiting symmetry in temporal
    logic model checking. FMSD 9(1/2), 77–104 (1996)
10. Clarke, E.M., Talupur, M., Veith, H.: Proving Ptolemy right: The environment ab-
    straction framework for model checking concurrent systems. In: TACAS’08. LNCS,
    vol. 4963, pp. 33–47. Springer (2008)
11. Emerson, E.A., Kahlon, V.: Reducing model checking of the many to the few. In:
    CADE’00. LNAI, vol. 1831, pp. 236–254. Springer (2000)
12. Emerson, E.A., Namjoshi, K.S.: Reasoning about rings. In: POPL’95. pp. 85–94.
    ACM (1995)
13. Emerson, E.A., Namjoshi, K.S.: Automatic verification of parameterized syn-
    chronous systems. In: Proc. of CAV’96. LNCS, vol. 1102, pp. 87–98. Springer (1996)
14. Emerson, E.A., Sistla, A.P.: Symmetry and model checking. FMSD 9(1/2), 105–131
    (1996)
15. Ganzinger, H., Hagen, G., Nieuwenhuis, R., Oliveras, A., Tinelli, C.: DPLL(T):
    Fast decision procedures. In: Proc. of CAV’04. pp. 175–188 (2004)
16. German, S.M., Sistla, A.P.: Reasoning about systems with many processes. J. of
    the ACM 39(3), 675–735 (1992)
17. Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing soft-
    ware veriers from proof rules (2012)
18. Herlihy, M., Shavit, N.: The Art of Multiprocessor Programming. Morgran-
    Kaufmann (2008)
19. Kesten, Y., Pnueli, A., on Raviv, L.: Algorithmic verification of linear temporal
    logic specifications. In: ICALP’98. LNCS, vol. 1443, pp. 1–16. Springer (1998)
20. Lahiri, S.K., Qadeer, S.: Back to the future: revisiting precise program verification
    using SMT solvers. In: POPL’08. pp. 171–182. ACM (2008)
21. Lesens, D., Halbwachs, N., Raymond, P.: Automatic verification of parameterized
    linear networks of processes. In: POPL’97. pp. 346–357. ACM (1997)
22. Madhusudan, P., Parlato, G., Qiu, X.: Decidable logics combining heap structures
    and data. In: POPL’11. pp. 611–622. acm (2011)
23. Manna, Z., Pnueli, A.: Temporal Verif. of Reactive Systems. Springer (1995)
24. Marco Bozzano, G.D.: Beyond parameterized verification. In: TACAS’02. LNCS,
    vol. 2280, pp. 221–235. Springer (2002)
25. de Moura, L.M., Bjørner, N.: Z3: An efficient SMT solver. In: TACAS’08. LNCS,
    vol. 4963, pp. 337–340. Springer (2008)
26. Pnueli, A., Ruah, S., Zuck, L.D.: Automatic deductive verification with invisible
    invariants. In: TACAS’01. LNCS, vol. 2031, pp. 82–97. Springer (2001)
27. Sánchez, A., Sánchez, C.: Decision procedures for the temporal verification of con-
    current lists. In: ICFEM’10. LNCS, vol. 6447, pp. 74–89. Springer (2010)
28. Sánchez, A., Sankaranarayanan, S., Sánchez, C., Chang, B.Y.E.: Invariant gener-
    ation for parametrized systems using self-reflection. In: SAS’12. LNCS, vol. 7460,
    pp. 146–163. Springer (2012)
29. Zuck, L.D., Pnueli, A.: Model checking and abstraction to the aid of parameterized
    systems (a survey). Computer Languages, Systems & Structures 30, 139–169 (2004)
16

A     Infinite State Mutual Exclusion Examples
Example: A Parametrized Mutual Exclusion Algorithm. Consider the
program in Fig. 9(b) which implements mutual exclusion using a simple ticket-
based protocol. Each thread that wants to access the critical section at line
5, acquires a unique increasing number (ticket) and announces its intention to
enter the critical section by adding the ticket to a shared global set of tickets.
Then, the thread waits until its ticket becomes the lowest value in the set before
entering the critical section. After a thread leaves the critical section it removes
its ticket from the set. SetMutExc uses two global variables: avail , of type
Int, which stores the shared counter; and bag, of type SethInti, which stores the
set of all threads that are trying to access the critical section. For any instance
(number of threads) the concrete system is an infinite state program, since the
available ticket is ever increasing. Program IntMutExc in Fig. 9(a) is similar
except that is stores the minimum value in a global variable of type Int.
Example 2. Consider program SetMutExc in Fig. 9(b). The instance consist-
ing of two running threads, SetMutExc[2], contains the following variables:
                   V = {avail , bag, ticket[0], ticket[1], pc[0], pc[1]}
Global variable avail has type Int, and global variable bag has type SethInti.
The instances of local variable ticket for threads 0 and 1, ticket[0] and ticket[1],
have type Int. The program counters pc[0] and pc[1] have type Loc = {1 . . . 6}.
The initial condition of SetMutExc[2] specifies that:
         Θg : avail = 0 ∧ bag = ∅            Θl [0] : ticket[0] = 0 ∧ pc[0] = 1
                                                                                  (1)
                                             Θl [1] : ticket[1] = 0 ∧ pc[1] = 1


                                                   global
      global                                         Int avail := 0
        Int avail := 0                               SethInti bag := ∅
        Int min := 0
                                                  procedure SetMutExc
      procedure IntMutExc                           Int ticket := 0
        Int ticket                                begin
      begin                                    1: loop
   1: loop                                     2:    nondet
                                                                            
   2:    nondet                                          ticket := avail + +
                                               3:
   3:    ticket := avail + +                             bag.add (ticket)
   4:    await (min == ticket)                 4:    await (bag.min == ticket)
   5:    critical                              5:    critical
   6:    min := min + 1                        6:    bag.remove(ticket)
   7: end loop                                 7: end loop
      end procedure                               end procedure
(a) IntMutExc, using two counters            (b) SetMutExc, using a set of integers

     Fig. 9: Two implementations of a ticket based mutual exclusion protocol
                                                                                          17

There are fourteen transitions in SetMutExc[2], seven transitions for each
thread: τ1 [0] . . . τ7 [0] and τ1 [1] . . . τ7 [1]. The transitions corresponding to thread
0 are:


τ1 [0] : pc[0] = 1 ∧ pc0 [0] = 2 ∧                                    pres(V \ {pc[0]})
τ2 [0] : pc[0] = 2 ∧ pc0 [0] = 3 ∧                                    pres(V \ {pc[0]})
                                                               
                                         ticket 0 [0] = avail
                                                           
τ3 [0] : pc[0] = 3 ∧ pc0 [0] = 4 ∧  avail 0 = avail + 1  ∧ pres({pc[1], ticket[1]})
                                     bag 0 = bag ∪ {avail }
τ4 [0] : pc[0] = 4 ∧ pc0 [0] = 5 ∧ bag.min = ticket[0]        ∧ pres(V \ {pc[0]})
τ5 [0] : pc[0] = 5 ∧ pc0 [0] = 6 ∧                                    pres(V \ {pc[0]})
                       0                  0
τ6 [0] : pc[0] = 6 ∧ pc [0] = 7 ∧ bag = bag \ ticket[0]             ∧ pres(V \ {bag, pc[0]})
                       0
τ7 [0] : pc[0] = 7 ∧ pc [0] = 1 ∧                                     pres(V \ {pc[0]})

The transitions for thread 1 are analogous. The predicate pres summarizes the
preservation of variables’ values. For example, in SetMutExc[2], the predicate
pres(V \ {bag, pc[0]}) is simply:

avail 0 = avail ∧ ticket 0 [0] = ticket[0] ∧ pc0 [1] = pc[1] ∧ ticket 0 [1] = ticket[1].




B     Empirical Evaluation: Mutual Exclusion
Mutual Exclusion for IntMutExc:. For the programs described in Fig.9
we use active(k) for (pc(k) = 4, 5, 6) and critical(k) for (pc(k) = 5, 6). Mutual
exclusion is specified as:
                                                                    
                           ˆ  i 6= j → ¬(critical(i) ∧ critical(j))
               mutex(i, j) =
                                                         (i)
Using the p-inv rule to prove mutex fails for τ4 , described as:
                                                             
                        pc(i) = 4 ∧ pc0 = pc{i ← 5}         ∧
                                                             
    mutex(i, j) ∧            ticket(i) = min               ∧  → mutex0 (i, j)
                    pres(avail , min, ticket(i), ticket(j))

The SMT Solver reports two counter models:

       1. pc(j) = 5 ∧ min = 1 ∧ avail = 2 ∧ ticket(i) = 1 ∧ ticket(j) = 3
       2. pc(j) = 5 ∧ min = 1 ∧ avail = 2 ∧ ticket(i) = 1 ∧ ticket(j) = 1

The decision procedure builds models that show that the VC is not valid. Hence,
mutex is not inductive. The formula mutex(i, j) does not encode two important
aspects of the program. First, if a thread is in the critical section, then it owns
18

                       mutex                       mutexS
              minticket      notsame      minticketS      notsameS

                     activelow                    activelowS
                   (a) IntMutExc               (b) SetMutExc

       Fig. 10: Proof graph showing the dependencies between invariants


the minimum announced ticket (unlike in counter-model 1) Second, the same
ticket cannot be given to two different threads (unlike in counter-model 2). Two
new auxiliary support invariants encode these facts:

                  ˆ (critical(i) → min = ticket(i))
     minticket(i) =
                   ˆ (i 6= j ∧ active(i) ∧ active(j) → ticket(i) 6= ticket(j))
     notsame(i, j) =

Now, mutex can be verified using sp-inv with minticket and notsame as support.
Unfortunately, minticket is not inductive. The solver reports that if two different
                                                                       (j)
threads i and j are in the critical section with the same ticket and τ6 is taken,
then minticket(i) does not hold any longer. Hence, we need notsame as support
for minticket. However, notsame in not inductive either. In this case, the offend-
ing transition is τ3 when an existing ticket is reused. The following invariant
precludes that case:

                              ˆ (active(i) → ticket(i) < avail )
                 activelow(i) =

The candidate activelow is inductive (provable using p-inv) and supports notsame.

Mutual Exclusion for SetMutExc:. We proceed in a similar way. The in-
variants mutexS, notsameS and activelowS are identically to mutex, notsame and
activelow, but minticketS is defined as follows:

                            ˆ (critical(i) → bag.min = ticket(i))
              minticketS(i) =

Similarly, minticketS and notsameS support mutexS, but this time, minticketS
requires activelowS in addition to notsameS as support. The extra support is
needed to encode that a thread taking transition τ3 adds to bag a value strictly
greater than any other previously assigned ticket. Finally, notsameS relies on
activelowS, which again, is inductive.
    Fig 10 shows the proof graphs used for the empirical evaluation reported in
Fig. 7 in Section 4.


C    Fully Symmetric Parallelism
Even though the parametrized rules p-inv and sp-inv are sound for all pa-
rametrized systems, these rules are particularly useful for symmetric systems.
                                                                                  19

Intuitively, a parametrized transition system S[M ] is symmetric whenever the
roles of thread ids are interchangeable, in the sense that swapping two thread ids
in a given run produces another legal run that satisfies the corresponding tem-
poral properties (with the ids swapped in the property as well). This notion of
symmetry is semantic, but there are simple syntactic characteristics of programs
that immediately guarantee symmetry. For example, if the only comparisons
between thread identifiers in the program are for equality and inequality, then
the system is fully symmetric. In this section, we introduce a semantic notion
of symmetry and identify syntactic restrictions on programs that guarantee this
notion of symmetry.
    We show now some basic properties of fully symmetric systems. The essential
                                                            t
semantic element to capture symmetry is a function πij        for each sort t, that
defines the effect in elements of t of swapping threads i and j. For most of the
sorts, like int, bool and Loc this function is simply the identity, because thread
                                                                   tid
identifiers do not interfere with values of these types. For tid, πij  is:

                                     
                                     i     if e = j
                            tid
                           πij  (e) = j     if e = i
                                     
                                       e    otherwise

For sorts that involve thread identifiers (if present in the program), like contain-
ers, sets, registers, etc storing elements of sort tid one can easily define these
semantic maps.
    Then, to characterize the effect in a run of a system of swapping two thread
ids, we define the following maps:
                                     M
  – a model transformation map πij      , which given a first-order model of the the-
     ories involved, characterizes the transformed model over the same domains.
                                      E
  – a syntax transformation map πij     , that allows to transform terms and pred-
     icates. For variables of sort tid, the actual value is assigned in a concrete
     interpretation, so the swap between the ids is delegated to the interpreted
     function swap added to the theory of thread identifiers:

                                           
                                            i if k = j
                          swapM (i, j, k) = j if k = i
                                           
                                             k otherwise

            M         E                                           S
 – from πij     and πij , we define the state transformation πij    , that gives the
   program state obtained by swapping thread identifiers. Essentially, the valu-
   ation given to a transformed variable is the transformation of the value given
   to the original variable.
             T
 – finally, πij that allows to obtain the transition identifier that corresponds to
   a given transition when the roles of two threads are exchanged.
                                    M    E     S       T
   Formally, the semantic maps πij    , πij , πij and πij are
20



                                                                          
                                                                          i       k=j
                                                           E
                                                         πij (k : tid) = j        k=i
                 i       if e = j                                        
                                                                            k      k 6= i, j
 M
πij (e : tidM ) = j       if e = i                         E
                                                          πij (v : tid) = swap(i, j, v)
                 
                    e     if e 6= i, j                 E                               E
    M       M     t
                                                      πij (v[k] : tid) = swap(i, j, v[πij (k)])
  πij (e : t ) = πij (e) if t 6= tid                           E
        M M           M M M
                                                              πij (c : t) = c
       πij (f ) = λx.πij (f (πji x))                           E
       M
                                                              πij (v : t) = v
      πij (P M ) = {(πij
                      M                M
                         x1 , . . . , πij xk ) |          E                  E
                                                         πij (v[k] : t) = v[πij (k)]
                        P M (x1 , . . . , xk )}     E                           E               E
                                                   πij (f (t1 . . . tn )) = f (πij (t1 ) . . . πij (tn ))
                                                    P                           E               E
                                                   πij (P (t1 . . . tn )) = P (πij (t1 ) . . . πij (tn ))
                 
                  τ` [i]      if k = j
      T                                                      S            M      E
     πij τ` [k] = τ` [j]       if k = i                     πij (s)(v) = πij (s(πji (v)))
                 
                   τ` [k]      if k 6= i, j

    The essential building block used to define these transformation maps is a
                     t
swapping function πij   for each sort t, that maps elements in a model of the sort
t to the transformed elements in t. This function characterizes the effect that
swapping i and j has on elements of t. For most of the sorts, like int, bool and Loc
this function is simply the identity, because thread identifiers are not related to
values of these types. For sorts that involve thread identifiers, like set of threads
settid, for example, one can define:


         settid
        πij     (S) = (S \ {i, j}) ∪ (S \ {i, j}) ∪ ({j | if i ∈ S} ∪ {i | if j ∈ S})

   Similar transformations can easily be defined for containers, registers, etc
containing elements of sort tid. To guarantee full symmetry all basic transfor-
          t
mations πij must satisfy:
                                          t
                                         πji    t
                                             ◦ πij = id t .                                          (2)
                           M              M     M     M     M
From (2) it follows that πij   satisfies πij ◦ πji = πji ◦ πij = idM .
    For local program variables, the index is known (it is part of the variable
name), so the transformation gives the name of the transformed variable. How-
ever, for variables of sort tid, the actual value is assigned in a concrete inter-
pretation, so the swap between the ids is delegated to the interpreted function
swap added to the theory of thread identifiers. Note that for every first-order
            E
signature πij  is uniquely determined. The following commutativity condition is
                                                         M      E
a health condition on the transformation functions πij     and πij , where J.K is an
interpretation map (that gives a model in the appropriate domain to each term
and a truth value to each predicate):
                          E        M                     P         M
                        Jπij tK = πij JtK              Jπij P K ≡ πij JP K                           (3)
                                                                                                     21


  To show that S satisfies ϕ(j). Find ψ(k) with:

   S1. S2. S3.     U1. U2. U3.
                                          ψ σ ∧ ϕ ∧ τ (i) → ϕ0
                                    V
          S4.                                                             for all τ , i ∈ j, and
                                    σ∈S
                                                                               S = Arr(k, k ∪ j)
                    V               V                   (i)       0
          S5.            i 6= x ∧         ψσ∧ϕ∧τ              →ϕ          for all τ , i ∈
                                                                                        / j, and
                   x∈j              σ∈S
                                                                               S = Arr(k, k ∪ j ∪ {i})
                                            ϕ

        Fig. 11: The parametrized strengthening invariance rule sp-inv


This condition ensures that the interpretation obtained after transforming ex-
pression e, corresponds to the model transformation of the interpretation of e.
                                    S              E
Finally, note in the definition of πij that first πji exchanges v[i] into v[j], then
the interpretation s is used, and finally then the result is transformed according
                                          M
to the model transformation function πij    .
    Now we are ready to define the condition for a system to be symmetric.

Definition 2 (Fully-Symmetric System). A parametrized system S is fully-
symmetric whenever for all M , and for all i, j ∈ [M ], the following hold for all
states s and s0 , transition τ and predicate P :
                              S
 1. s  Θ if and only if (πij   s)  Θ.
 2. τ (s, s0 ) holds if and only if (πij
                                      T       S
                                         τ )(πij     S 0
                                                 s, πij s ) holds.
                              S         P
 3. s  P if and only if (πij s)  (πij P ).

   Full symmetry allows to reason about a particular thread, and conclude the
properties for arbitrary threads.

Lemma 1. Let S be a fully symmetric system, ϕ(k) be a parametrized formula
with free variables k : {k0 . . . kn }, and N an arbitrary size.
                                                          ^                                
                 S  ϕ(k)          ⇔      S[N ]                      ϕ[i0 , . . . , in ]
                                                     i0 ,...,in ∈[n]


It is important to note that the range of the concrete indices is [n], independent
of the number of running threads N .

Corollary 1. For every fully symmetric S and property ϕ(k)

                   S  ϕ(k)            ⇔      for every N , S[N ]  ϕ[0]

   The previous results justify the version of the strengthening invariance rule
sp-inv in Fig. 11, where Arr(k, j) is the set of substitutions of the form σ : k → j.
   Finally, for fully symmetric systems:
22

Theorem 5 (Concretization). Let ϕ(k) be with |k| = n. Then:
                                   ^
               ϕ(k) is valid ⇔         α(ϕ) is valid
                                             α∈A


where A = Arr(k, [n]) is the set of concretizations of variables in Var (ϕ).
   For example, if one intends to prove that p(i) is inductive, the concretization
theorem allows to reduce P3 in p-inv to:

                                 p[0] ∧ τ [1] → p0 [0]                           (4)

where p[0] is a short for α(p(i)) with α : i → 0. Formula (4) involves no arrays.
Similarly, to show p(i) with support invariant q(j), rule S5 can be reduced to:

                          q[0] ∧ q[1] ∧ p[0] ∧ τ [1] → p0 [0]

   In practice, the concretization is not performed upfront before discharging
the verification condition to the SMT-Solver. Our use of arrays to encode pa-
rametrized formulas can be handled using the theory of uninterpreted functions
and let the solver perform the search and propagation.


D    Detailed Invariants for Case Studies

We prove that the program in Fig 2 satisfies: (1) list shape preservation; and
(2) the list implements a set, whose elements correspond to those stored in elems.
The theory TLL3 allows to reason about addresses, elements, locks, sets, order,
cells (i.e., list nodes), memory and reachability. A cell is a struct containing an
element, a pointer to next node in the list and lock to protect the cell. A lock is
associated with operations lock and unlock to acquire and release. The memory
(heap) is modeled as an array of cells indexed by addresses. The specification is:
       
        null ∈ reg ∧ reg = addr2set(heap, head ) ∧ head 6= tail           ∧   (L1)
       
       
        heap[tail ].next = null ∧ tail 6= null ∧ head 6= null             ∧   (L2)
ϕlst =
     ˆ
       
        heap[head ].data = −∞ ∧ heap[tail ].data = +∞                     ∧   (L3)
       
       
         elems = set2elemset(heap, reg) ∧ Ordered (heap, head , tail )         (L4)

Formula ϕlst is 0-index since it only constrains global variables. (L1) establishes
that null belongs to reg and that reg is exactly the set of addresses reachable in
the heap starting from head , which ensures that the list is acyclic. (L2) and (L3)
express some sanity properties of the sentinel nodes head and tail . Finally, (L4)
establishes that elems is the set of elements in cells referenced by addresses in
reg, and that the list is ordered. The main specification is list, defined as ϕlst .
    Leap can establish that list holds initially, but fails to prove that list is
preserved by all transitions (i.e., list is not a parametrized invariant), so support
invariants are required. To prove (L1) the support invariant ϕreg captures how
                                                                                       23

addresses are added and removed from reg in the program. Local variable v in
procedure MGC, Search, Insert and Remove, is denoted by vC , vS , vI and
vR respectively:
           
            {head , tail , null } ⊆ reg ∧ tail 6= null ∧ head 6= null ∧ head 6= tail ∧
           
           
           
            pc(i) = 24..39 → prev I (i) ∈ reg ∧ pc(i) = 26..40 → curr I (i) ∈ reg ∧
           
           
           
            pc(i) = 33, 34 →¬aux (i) ∈ reg ∧ pc(i) = 30 → aux (i) ∈ reg
                                       I                                  I              ∧
ϕreg (i) =
         ˆ                                                                             
           
            pc(i) =  43..57   →    prev R (i) ∩ {tail , null } = ∅ ∧ prev   (i) ∈ reg   ∧
           
           
                                                                         R
           
            pc(i) = 45..55 → curr R (i) 6= null ∧ curr R (i) ∈ reg                      ∧
           
           
             pc(i) = 49 → aux R (i) ∈ reg

Formula ϕreg is 1-index and determines which addresses belong to reg depending
on each program location. Invariant region(i) is defined as ϕreg (i). Invariant
next(i) captures the relative position in the list of the cells pointed by head and
tail and local variables prev , curr and aux . The details of can be found in the
appendix. Invariant next(i) is needed for (L2). To prove (L3) and (L4) we need
to show that order is preserved. We express this constraint with formula ϕord :
           
            heap[head ].data = −∞ ∧ heap[tail ].data = +∞                         ∧
           
           
           
            pc(i) = 3..7 → eC (i) ∈
                                   / {±∞} ∧ pc(i) = 8..21 → eS (i) ∈   / {±∞}      ∧
           
           
           
           
           
            pc(i) = 23..40 → eI (i) ∈
                                     / {±∞} ∧ pc(i) = 42..58 → eR (i) ∈   / {±∞} ∧
           
           
           
            pc(i) = 26..40 →   heap[curr   (i)].data ≤ +∞                         ∧
           
                                         I
           
            pc(i) = 24..39 → heap[prev (i)].data ≤ +∞
                                          I                                        ∧
ϕord (i) =
         ˆ
           
            pc(i) = 28..31 → heap[curr I (i)].data < eI (i)                       ∧
           
           
           
            pc(i) = 24..37 →   heap[prev   (i)].data < e  (i)                     ∧
           
                                         I              I
           
           
           
            pc(i) = 35..37 → eI (i) < heap[curr I (i)].data                       ∧
           
           
           
            pc(i) = 33, 34 → heap[aux I (i)].data = eI (i)                        ∧
           
           
           
             pc(i) = 54, 55 → heap[curr R (i)].data = eR (i)

and define invariant order(i) as ϕord (i). Invariant lock captures those program
locations at which a thread owns a cell in the heap:
                 
                  pc(i) = 25..39         → heap[prev I (i)].lockid = i   ∧
                 
                 
                 
                  pc(i) = 27..31, 34..40 → heap[curr I (i)].lockid = i   ∧
                 
                 
                 
                  pc(i) = 30             → heap[aux I (i)].lockid = i    ∧
      ϕlck (i) =
               ˆ
                 
                  pc(i) = 44..57         →   heap[prev R (i)].lockid = i ∧
                 
                 
                 
                 
                  pc(i) = 46..50, 53..58 → heap[curr R (i)].lockid = i ∧
                 
                 
                   pc(i) = 49             → heap[aux R (i)].lockid = i

Finally, formula ϕdis encodes that two different threads calls to malloc return
two different addresses:

               ˆ (i 6= j ∧ pc(i) = 33, 34 ∧ pc(j) = 33, 34) → aux I (i) 6= aux I (j)
   ϕdis (i, j) =
24

In this case, disj(i, j), defined as ϕdis (i, j) is a 2-index invariant.
    In practice, when proving concurrent datatypes these candidate invariants are
easily spotted using the information obtained from an unsuccessfully attempt
of Leap to prove a particular VC. Leap parses the counterexample (model)
returned by the SMT solver, which is usually very small, involves few threads
and allows to easily understand the missing intermediate facts. Fig.8 shows the
proof graph for the verification of concurrent lock-coupling lists. In the graphs, a
dashed arrow from ϕ to ψ denotes that ϕ is used as support for ψ. Leap parses
proof graphs as input and applies g-inv when necessary. Additionally, graphs can
specify program locations for which to apply a particular formula as support,
which greatly speeds proof checks. Fig. 7 shows the results of this empirical
evaluation, executed on a computer with a 2.8 GHz processor and 8GB memory.
The columns show the index of the formula; the total number of generated VCs;
the number of VCs verified using the position based DP; the number of VCs
verified using the specialized DP and, finally, the total running time in seconds
required to verify all VCs. We benchmark the times in four different scenarios
using different tactics. The first scenario (FS) uses sp-inv with full support,
that is, all invariant candidates are used as support. The second scenario (FA)
considers only full assignments when generating support. The third scenario
(FA-SS) involves full assignments in addition to discarding superfluous support
information. The last column reflects the forth scenario, using proof graphs. We
use OM to represent out-of-memory failure. These results show that, in practice,
tactics are essential for efficiency when handling non-trivial examples such as
concurrent lists.


E    Proof Graph for Concurrent Lock-coupling Lists
We present now the full proof graph for this concurrent lock-coupling single-
linked lists implementation. We use the following notation to represent a proof-
graph:

-> inv [l1:P:sup1, sup2, sup3;
        l2:P:sup4, sup5
       ] { SMP : pretactic | posttactic }

where inv is the invariant candidate to be verified. Next, between brackets it is
possible to specify invariant support for specific program locations. This argu-
ment is optional. Required support invariants are provided as a list of support
rules, separated by ;. Each support rule consists on a location, a possible premise
identifier to localize the support generation on a specific invariant rule premise
and a list of invariants to be used as support. Finally, it is possible to describe
the method used to compute the domain bounds for the small model property,
as well as tactics to be used in support generation and formula simplification,
separated by a |.
    Fig.12 shows the proof graph for the current lock-coupling list example.
                                                                              25




-> fullOrder {pruning:reduce2|simpl}

-> fullPreserve [34:E:fullRegion;
                 35:E:fullRegion,fullNext,fullLock,fullOrder
                        {pruning:reduce2|simpl};
                 51:E:fullNext,fullRegion,fullOrder
                        {pruning:reduce2|simpl}
                ] {pruning:reduce2|simpl}

-> fullNext [ 5:N:fullPreserve;
             30:N:fullPreserve,fullRegion;
             34:N:fullRegion;
             34:E:fullRegion,fullDisjoint;
             35:N:fullRegion;
             35:E:fullLock,fullRegion;
             41:N:fullPreserve,fullRegion;
             47:N:fullPreserve,fullRegion;
             50:N:fullPreserve,fullRegion;
             51:N:fullPreserve,fullRegion;
             51:E:fullPreserve,fullLock,fullRegion
            ] {pruning:reduce2|simpl}

-> fullLock [28:N:fullNext;
             29:N:fullNext;
             36:N:fullNext;
             45:N:fullNext;
             46:N:fullNext;
             52:N:fullNext
            ] {pruning:reduce2|simpl}

-> fullDisjoint {pruning:reduce2|simpl}

-> fullRegion [24:N:fullPreserve {pruning:reduce2|simpl};
               28:N:fullNext;
               30:N:fullPreserve;
               35:E:fullDisjoint;
               41:N:fullPreserve;
               45:N:fullNext;
               47:N:fullPreserve,fullNext;
               51:N:fullPreserve,fullNext;
               51:E:fullPreserve,fullNext,fullLock
                        {pruning:reduce2|simpl}
              ] {pruning:reduce2|simpl}


     Fig. 12: Proof graph representation for concurrent lock-coupling lists
