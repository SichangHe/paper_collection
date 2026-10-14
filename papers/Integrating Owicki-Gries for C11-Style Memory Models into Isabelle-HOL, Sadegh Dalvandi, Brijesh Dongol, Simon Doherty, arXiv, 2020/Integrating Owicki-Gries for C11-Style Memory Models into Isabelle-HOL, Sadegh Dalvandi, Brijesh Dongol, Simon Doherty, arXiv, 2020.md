                                         Integrating Owicki-Gries for C11-Style Memory Models into
                                                               Isabelle/HOL ⋆

                                                              Sadegh Dalvandi1 , Brijesh Dongol1 , and Simon Doherty2
                                                                          1
                                                                              University of Surrey, Guildford, UK
                                                                         2
                                                                              University of Sheffield, Sheffield, UK
arXiv:2004.02983v2 [cs.PL] 8 Apr 2020




                                               Abstract. Weak memory presents a new challenge for program verification and has resulted
                                               in the development of a variety of specialised logics. For C11-style memory models, our
                                               previous work has shown that it is possible to extend Hoare logic and Owicki-Gries reasoning
                                               to verify correctness of weak memory programs. The technique introduces a set of high-level
                                               assertions over C11 states together with a set of basic Hoare-style axioms over atomic weak
                                               memory statements (e.g., reads/writes), but retains all other standard proof obligations for
                                               compound statements. This paper takes this line of work further by showing Nipkow and
                                               Nieto’s encoding of Owicki-Gries in the Isabelle theorem prover can be extended to handle
                                               C11-style weak memory models in a straightforward manner. We exemplify our techniques
                                               over several litmus tests from the literature and a non-trivial example: Peterson’s algorithm
                                               adapted for C11. For the examples we consider, the proof outlines can be automatically
                                               discharged using the existing Isabelle tactics developed by Nipkow and Nieto. The benefit
                                               here is that programs can be written using a familiar pseudocode syntax with assertions
                                               embedded directly into the program.


                                        1     Introduction
                                        Hoare logic [17] is fundamental to understanding the intented design and semantics of sequential
                                        programs. Owicki and Gries’ [29] framework extends Hoare logic to a concurrent setting by adding
                                        an interference-free check that guarantees stability of assertions in one thread against the execution
                                        of another. Although several other techniques for reasoning about concurrent programs have since
                                        been developed [33], Owicki-Gries reasoning remains fundamental to understanding concurrent
                                        systems and one of the main methods for performing deductive verification. Mechanised support
                                        for Owicki-Gries’ framework has been developed for the Isabelle theorem prover [30] by Nipkow and
                                        Nieto [28] and is currently included in the standard distribution.
                                             Our work is in the context of C11 (the 2011 C standard), which has a weak memory model
                                        that is designed to enable programmers to take advantage of weak memory hardware [6, 20, 23, 24].
                                        Unlike in sequentially consistent memory [26], states are graphs with several relations that are
                                        used to track dependencies between memory events (e.g., reads, writes, updates) [2,6,11,20,23,24].
                                        This means that it is not possible to use the traditional Owicki-Gries framework to reason about
                                        concurrent programs under C11. Researchers have instead developed a set of specialised logics, e.g.,
                                        [2], including those that extend Owicki-Gries framework [25] and separation logic [12, 13, 35, 35, 37]
                                        designed to cope with specific fragments of C11.
                                             Our point of departure is the operational semantics of Doherty et al. [11] for the RC11-RAR
                                        fragment of C11 [23]. As indicated by the RAR, the memory model allows both relaxed and
                                        ⋆
                                            This work is supported by EPSRC grants EP/R032351/1, EP/R032556/1 and EP/R019045/2.
2      Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

release-acquire accesses. Moreover, the model restricts the C11 memory model to disallow the
“load-buffering” litmus test [23, 24]. A key advancement in the semantics developed by Doherty et
al. is a transition relation over states modelled as C11 graphs, allowing program execution to be
viewed as an interleaving of program statements as in classical approaches to concurrency. They
provide a primitive assertion language for expressing properties of such states, which is manually
applied to the message passing litmus test and Peterson’s algorithm adapted to C11. However, the
assertion language itself expresses state properties at a low level of abstraction (high level of de-
tail), and hence is difficult to mechanise. We3 have recently recast Doherty et al.’s semantics in an
equivalent timestamp-based semantics [19, 20]. More importantly, we have developed a high-level
set of assertions for stating properties of the C11 state [9]. These assertions have been shown to
integrate well with a Hoare-style proof calculus, and, by extension, the Owicki-Gries proof method.
Interestingly, the technique enables reuse of all standard Owicki-Gries proof rules for compound
statements.
    In this paper, we push this technique further by showing how this framework can be integrated
into Isabelle via a straightforward extension of the Owicki-Gries encoding by Nipkow and Nieto [28].
Unlike [9], where program counters are used to model control flow and relations over C11 states
are used to model program transitions, the approach in this paper is more direct. We show that
once a correct proof outline has been encoded, the proof outlines can be validated with minimal
user interaction. Our extension is parametric in the memory model, and can be adapted to reason
about other C11-style operational models [24].
Contributions. Our main contributions are thus:
1. A simple and generic extension to the standard Isabelle encoding of Owicki-Gries to cope with
   C11-style weak memory,
2. An instantiation of the RC11-RAR operational semantics within Isabelle as an example memory
   model,
3. An integration with a high-level assertion language for reasoning about weak memory states,
   and
4. Verification of several examples in the extended theory, including Peterson’s algorithm for C11.
Overview. In Section 2, we briefly present the Owicki-Gries encoding by Nipkow and Nieto [28],
as well as the message passing litmus test which serves as a running example. We describe how this
encoding can be generically extended to cope with weak memory in Section 3, then in Section 4, we
present RC11-RAR as an example instantiation. In Section 5, we present a technique for reasoning
about C11-style programs as encoded in Isabelle4 , which we apply to a number of examples. We
present related work in Section 6.


2   Owicki-Gries in Isabelle/HOL

Nipkow and Nieto [28] present a formalisation of Owicki-Gries method in Isabelle/HOL. Their
formalisation defines syntax, its semantics and Owicki-Gries proof rules in higher-order logic. Cor-
rectness of the proof rules with respect to the semantics is proved and their formalisation is part
of the standard Isabelle/HOL libraries. To provide some context for our extensions, we provide an
3
  For the CAV reviewers: This work is under review. An anonymised copy of the paper has been up-
  loaded [9].
4
  Our entire Isabelle formalisation can be found as ancillary files here https://arxiv.org/abs/2004.02983.
                        Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL               3

overview of this encoding here; an interested reader may wish to consult the original paper [28] for
further details.
    The defined programming language is a C-like WHILE language augmented with shared-variable
parallelism (||) and synchronisation (AWAIT). Parallelism must not be nested, i.e. within c1 || c2 || ... || cn ,
each ci must be a sequential program. The programming language allows program constructs to be
annotated with assertions in order to record proof outlines that can later be checked. The language
also allows unannotated commands that may be placed within the body of AWAIT statements. As
in the original treatment [29], AWAIT is an atomic command that executes under the precondition
of the AWAIT block.
datatype α ann_com =
AnnBasic (α assn ) (α ⇒ α)
| AnnSeq (α ann_com ) (α ann_com )
       (" _ ;; _ ")
| AnnCond (α assn ) (α bexp ) (α ann_com ) (α ann_com )
       (" _ IF _ THEN _ ELSE _ FI ")
| AnnWhile (α assn ) (α bexp ) (α assn ) (α ann_com )
       (" _ WHILE _ INV _ DO _ OD ")
| AnnAwait (α assn ) (α bexp ) (α com )
       (" _ AWAIT _ THEN _ END ")

datatype α com =
Parallel (α ann_com option × α assn ) list
| Basic (α ⇒ α)
| Seq (α com ) (α com ) (" _ ,, _ ")
| Cond (α bexp ) (α com ) (α com ) (" IF _ THEN _ ELSE _ FI ")
| While (α bexp ) (α assn ) (α com ) (" WHILE _ INV _ DO _ OD ")
In the datatype above, the concrete syntax is defined within (" ... "). α assn and α bexp
represent assertions and Boolean expressions, respectively. AnnBasic represents a basic (atomic)
state transformation (e.g, an assignment). AnnSeq is sequential composition, AnnCond is conditional,
AnnWhile is a loop annotated with an invariant, and AnnWait is a synchronisation construct. The
command Parallel is a list of pairs (c, q) where c is an annotated (sequential) command and q
is a post-condition. The concrete syntax for parallel composition (not shown above) is: COBEGIN
c1 {|q1 |} || ... || cn {|qn |} COEND.
    The semantics of programs are defined by transition rules between configurations, which are
pairs comprising a program fragment and a state. The proof rules of the Owicki-Gries formalisation
are syntax directed. A proof obligation generator has been implemented in the form of an Isabelle
tactic called oghoare. Application of this tactic results in generation of all standard Owicki-Gries
proof obligations, each of which can be discharged either automatically or via an interactive proof.
We omit the full details of standard semantics and verification condition generator [28].
Example 1 (Message passing (MP)). To motivate our extensions to a C11-style weak memory
model, we consider the message passing litmus test given in Fig. 1. It comprises two shared vari-
ables: d (that stores some data) and f (that stores a flag), both of which are initially 0. Under
sequential consistency, the postcondition of the program is r2 = 5. This is because the loop in
thread 2 only terminates after f has been updated to 1 in thread 1, which in turn happens after
d has been set to 5 by thread 1. Therefore, the only possible value of d for thread 2 to read is
5. The proof of this property straightforward, and can be easily handled by Nipkow and Nieto’s
encoding [28]. We provide a partial encoding in Fig. 2 to provide an example instantiation of the
4       Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty


                                                    record mp_state =
                                                    d :: nat f :: nat r1 :: nat      r2 :: nat
                                                    lemma:
        Init: d := 0; f := 0;                       || - {| f = 0 ∧ d = 0 |}
        Thread 1        Thread 2                          COBEGIN
                                                          {| True |} d := 5 ;;
        1 : d := 5;     3 : do r1 := f                    {| d = 5 |} f := 1
        2 : f := 1;         until r1 = 1;                 {| True |}
                        4 : r2 := d;                      ||
                    {r2 = 5}                              ...
                                                          COEND
                                                          {| r2 = 5 |}
Fig. 1. MP litmus test under sequential consis-     Fig. 2. Proving MP under sequential consistency us-
tency                                               ing Nipkow and Nieto’s encoding [28] of Owicki-Gries

abstract syntax above, and to better highlight the extensions necessary to handle C11-style weak
memory. The state of the program is defined using an Isabelle record where all shared variables and
local registers are modelled as its fields. For the proof outline in Fig. 2, the oghoare tactic generates
29 proof obligations, each of which is automatically discharged.


3   Extending Owicki-Gries to C11-Style Memory Models
We defer a precise description of a C11-style operational semantics to Section 4 in order to high-
light the fact our Isabelle framework is essentially parametric in the memory model used. The
fundamental requirement is that the memory model be an operational model featuring C-style,
annotated memory operations. All that is needed to understand the rest of this section is some
basic familiarity with weak memory models [9,11,19,31]. The functions encoding the weak memory
operational semantics WrX, WrR, RdX, . . . will be instantiated Section 4, and for the time being can
be considered to be transition functions that construct a new weak memory state for a given weak
memory prestate. However, a reader may wish to first read Section 4 for an example C11 memory
model prior to continuing with the rest of this section.
    To motivate our language extension, we reconsider MP (Example 1) in a C11-style weak memory
model. In particular, if all reads and writes are relaxed, C11 admits an execution in which thread 2
reads a “stale” value of d [19, 25]. Thus, it is only possible to establish the weaker postcondition
r2 = 0 ∨ r2 = 5 (see Section 4 for details). To regain the expected behaviour, one must introduce
additional synchronisation in the program. In particular, the write to f in thread 1 must be a
releasing write (denoted f :=R 1) and the read of f in thread 2 must be an acquiring read (denoted
r1 ←A f ).
    A weak memory state can be encoded as a special variable in the standard semantics. Moreover,
for the semantics that we employ [9, 11], within each weak memory state, for each low-level weak
memory event (e.g., read or write) we must keep track of the thread identifier (of type T), the shared
variable (or location) that is accessed (of type L) and the value in that variable (of type V).
    The syntactic extensions necessary for encoding C11-style statements in Isabelle are straight-
forward. For example, to capture the so-called RAR fragment, we require five new programming
constructs: relaxed reads and writes, releasing writes, and acquiring reads. Moreover, we wish to
support a SWAP[x, v] command [11, 39] that acquiringly reads x and releasingly writes v to x in a
single atomic step. This command is used in Peterson’s algorithm (see Fig. 10) and is implemented
in our model using a read-modify-write update.
                      Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL        5

    All of the new extensions are defined using a shallow embedding and their concrete syntax is
enclosed in brackets < ... > to avoid ambiguities in the Isabelle/HOL encoding. The annotated ver-
sions of these statements are given below. For completeness, we also require syntax for unannotated
versions of each command, but their details are elided.
syntax
" _AnnWrX " :: "α assn ⇒ L ⇒ T ⇒ V ⇒ Cstate ⇒ α ann_com "
          ("( _ <_ := _ _ ´_ >)")
" _AnnWrR " :: "α assn ⇒ L ⇒ T ⇒ V ⇒ Cstate ⇒ α ann_com "
          ("( _ <_ := R _ _ ´_ >)")
" _AnnRdX "::"α assn ⇒ idt ⇒ T ⇒ L ⇒ Cstate ⇒ α ann_com "
          ("( _ < ´_ ←_ _ ´_ >)")
" _AnnRdA "::"α assn ⇒ idt ⇒ T ⇒ L ⇒ Cstate ⇒ α ann_com "
          ("( _ < ´_ ←A _ _ ´_ >)")
" _AnnSwap "::"α assn ⇒ L ⇒ V ⇒ T ⇒ Cstate ⇒ α ann_com "
          ("( _ < SWAP [_ , _ ] _ ´_ >)")
Antiquotations of the from ´x are used to denote that the element x is a field of the record cor-
responding to the state of each program. For example, for the program in Fig. 2, the variables d,
f, r1 and r2 of record mp_state would be interpreted in the syntax using antiquotated variables.
This allows the translations (see below) to update fields in an external record yet for the programs
themselves to be written using a natural imperative syntax.
    To cope with weak memory, we embed the weak memory state as a special variable in the
standard encoding (see Figs. 7 and 8). Each operation induces an update to this embedded weak
memory state variable that can be observed by subsequent operations on the weak memory state.
    _AnnWrX defines a relaxed write. Its first argument is an assertion (the precondition) of the com-
mand, the second is the variable being modified, the third is the thread performing the operation,
the fourth is the value being written, and the fifth is the weak memory prestate. Similarly, _AnnWrA
is a releasing write. _AnnRdX defines a relaxed read, which loads a value of the given location (of
type L) from the given weak memory prestate into the second argument (of type idt). An acquiring
read, defined by _AnnRdA is similar. Finally, _AnnSwap defines a swap operation that writes the given
value (third argument) to the given location (second argument) using an update operation.
    The semantics of this extended syntax is given by a translation, which updates the program
variables, including the weak memory state. For the commands above, after omitting some low-level
Isabelle details, we have:
translations
" r < x := t v ´s >" ⇀
    " AnnBasic r ( _ u p d a t e _nam e s ( WrX ´s x v t ))"
" r < x := R t v ´s >" ⇀
    " AnnBasic r ( _ u p d a t e _nam e s ( WrR ´s x v t ))"
" r < ´x ←t y ´s >" ⇀
    " AnnAwait r (( _ u p d a t e _name s ( fst ( RdX ´s y t ))) , ,
                       ( _ u p d a t e _name x ( snd ( RdX ´s y t ))))"
" r < ´x ←A t y ´s >" ⇀
    " AnnAwait r (( _ u p d a t e _name s ( fst ( RdA ´s y t ))) , ,
                       ( _ u p d a t e _name x ( snd ( RdA ´s y t ))))"
" r < SWAP [x , v ] t ´s >" ⇀ " AnnBasic r ( fst ( Upd ´s x v t ))"
6        Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

             Init: d := 0; f := 0;                               Init: d := 0; f := 0;
          Thread 1            Thread 2                           Thread 1         Thread 2
          1 : d := 5;         3 : do r1 ← f                      5 : d := 5;      7 : do r1 ←A f
                                                                         R
          2 : f := 1;             until r1 = 1;                  6 : f := 1;          until r1 = 1;
                              4 : r2 ← d;                                         8 : r2 ← d;
                 {r2 = 0 ∨ r2 = 5}                                           {r2 = 5}

      Fig. 3. Unsynchronised MP under RC11-RAR           Fig. 4. MP with release-acquire synchronisation

These translations rely on an operational semantics defined by functions WrX (relaxed write), WrR
(releasing write), RdX (relaxed read), RdA (acquiring read) and Upd (RMW update), which we define
in Section 4.2.
    Relaxed and acquiring writes update the embedded weak memory state to the state returned
by WrX and WrA, respectively. A read event must return a post state (which is used to update the
value of the embedded weak memory state) and the value read (which is used to update the value
of the local variable storing this value). In order to preserve atomicity of the read, we wrap both
updates within an annotated AWAIT statement. The translation of a SWAP is similar.
    Note that a relaxed (acquiring) read comprises two calls to RdX (RdA), which one could mistakenly
believe to cause two different effects on the weak memory state. However, as we shall see, these
operations are implemented using Hilbert choice (SOME), hence, although there may be multiple
values that a read could return, the two applications of RdX (RdA) are identical for the same value
for the same parameters.


4     A C11-Style Memory Model: RC11-RAR
In this section, we describe a particular instance of a C11-style memory model: the RC11-RAR
fragment. This fragment disallows the load buffering litmus test [6, 23, 24], and all accesses are
either relaxed, releasing or acquiring. It is straightforward to extend the model to incorporate
more sophisticated notions such as release sequences and non-atomic accesses, but these are not
considered as the complications they induce detract from the main contribution of our work. It is
worth noting that RC11-RAR is still a non-trivial fragment [11].

4.1    Message Passing
To motivate the memory model, consider again the MP litmus test but for RC11-RAR (Figs. 3
and 4). In Fig. 3, all accesses are relaxed, and hence the program can only establish the weaker
postcondition r2 = 0 ∨ r2 = 5 since it is possible for thread 2 to read 0 for d at line 4. In Fig. 4, the
release annotation (line 2) and the acquire annotation (line 3) induces a happens-before relation if
the read of f reads from the write at line 2 [6]. This in turn ensures that thread 2 sees the most
recent write to d at line 5.
    We use the operational semantics described in [9], which models the weak memory state using
timestamped writes and thread view fronts [15, 19, 20, 31]. A timestamp is a rational number that
totally orders the writes to each variable. A viewfront records the timestamp that a thread has
encountered for each variable — the idea is that a thread may read from any write whose timestamp
is no smaller than the thread’s current viewfront. Similarly, a write may be introduced at any
timestamp greater than the current viewfront. The only caveat when introducing a write is that it
may not be introduced directly after a covered write (see [9, 11]). This caveat is to ensure atomicity
                          Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL           7


          d   f T1 view                                        d   f T1 view               d   f T1 view
               0                    d   f T1 view                   0                           0
      0                                                    0                           0
                                         0
                                0
               T2 view                                     5         T2 view           5         T2 view
                                5        T2 view                    1                           1
              σ0                                   σ1             σ2                           σ3
                          Fig. 5. An execution of the unsynchronised message passing

of RMW operations. In particular, a write to a variable x is covered whenever there is a RMW
on x that reads from the write. In this instance, it would be unsound for another write to x to be
introduced between the write that is read and the RMW (see [11] for further details).
Example 2 (Unsynchronised MP). Consider Fig. 5, depicting a possible execution of the unsynchro-
nised MP example (Fig. 3). The execution comprises four weak memory states σ0 , σ1 , σ2 , σ3 . In
each state, the timestamps themselves are omitted, but are assumed to be increasing in the direction
of the arrows. The numbers depict the value of each variable at each timestamp. State σ0 is the
initial state. Each thread’s viewfront in σ0 is consistent with the initial writes.
    After executing line 1, the program transitions to σ1 , which introduces a new write (with value
5) to d and updates the viewfront of thread 1 to the timestamp of this write. At this stage, thread
2’s viewfront for d is still at the write with value 0. Thus, if thread 2 were to read from d, it would
be permitted to return either 0 or 5. Moreover, if thread 2 were to write to d, it would be permitted
to insert the write after 0 or 5.
    After executing line 2, the program transitions to σ2 , which installs a (relaxed) write of f with
value 1. Now, consider the execution of line 3. There are two possible poststates since there are two
possible values of f that thread 2 could read. State σ3 depicts the case where thread 2 reads from
the new write f = 1. In this case, the view front of thread 2 is updated, but crucially, since there is
no release-acquire synchronisation, the viewfront of thread 2 for d remains unchanged. This means
that when thread 2 later reads from d in line 4, it may return either 0 or 5. We contrast this with
the execution of the synchronised MP described in Example 3.


Example 3 (Synchronised MP). Consider Fig. 6, which depicts an execution of the program in
Fig. 4. State τ1 is a result of executing line 5 and is identical to σ1 . However, after execution of
line 6, we obtain state τ1 , which installs a releasing write to f (denoted by 1R ). As in Example 2,
the acquiring read in line 7 could read from either of the writes to f . State τ3 depicts the case in
which thread 2 reads from the releasing write 1R . Now, unlike Example 3, this read establishes a
release-acquire synchronisation, which means that the viewfront of thread 2 for both f and d are
updated. Thus, if the execution continues so that thread 2 reads from d (line 8), the only possible
value it may return is 5.



4.2       Operational Semantics of C11 RAR in Isabelle/HOL

We now present details of the memory model from Section 4.1 as encoded in Isabelle/HOL. Recall
that the main purpose of this section is to instantiate the functions WrX, WrR, RdX, RdA and Upd from
Section 3.
8              Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty


           d     f T1 view               d   f T1 view            d   f T1 view             d   f T1 view
                  0                           0                        0                         0
       0                             0                        0                         0

                   T2 view           5        T2 view         5         T2 view         5         T2 view
                                                                       1R                        1R
                  τ0                       τ1                        τ2                         τ3
                             Fig. 6. An execution of the synchronised message passing

   Recall that type L represents shared variables (or locations), T represents threads, and V repre-
sents values. We use type TS (which is synonymous with rational numbers) to represent timestamps.
Each write can be uniquely identified by a variable-timestamp pair. The type Cstate is a nested
record with fields
    – writes, which is the set of all writes,
    – covered, which is the set of covered writes (recalling that covered writes are used to preserve
      atomicity of read-modify-write updates),
    – mods, which is a function mapping each write to a write record (see below),
    – tview, which is the viewfront (type L ⇒ (L × TS)) of each thread, and
    – mview, which is the viewfront of each write.
A write record contains fields val, which is the value written and rel, which is a Boolean that is
True if, and only if, the corresponding write is releasing.
record Cstate =                                                          record w r i t e _ r e cord =
 writes ::( L × TS ) set                                                  val :: V
 covered ::( L × TS ) set                                                 rel :: bool
 mods ::( L × TS ) ⇒ w r i t e _ r e cord
 tview :: T ⇒ L ⇒ (L × TS )
 mview ::( L × TS ) ⇒ L ⇒ ( L × TS )
      Next, we describe how the operations modify the weak memory state.
Read transitions. Both relaxed and acquiring reads leave all state components unchanged except
for tview. To define their behaviours, we first define a function visible_writes σ t x that returns
the set of writes to x that thread t may read from in state σ. For a write w = (x, q), we assume a
pair of functions var w = x and tst w = q that return the variable and timestamp of w, respectively.
Thus, we obtain:
definition " v i s i b l e _ w rite s σ t x ≡
   {w ∈ writes σ . var w = x ∧ tst (tview σ t x) ≤ tst w }"
We use a function getVW to select some visible write from which to read:
definition " getVW σ t x ≡
    ( SOME w . w ∈ v i s i b l e _ wr ite s σ t x )"
    Finally, we require functions read_transX t w σ and read_transA t w σ that update the tview
component of σ for thread t reading write w. Function read_transX t w σ updates tview σ t
to (tview σ t)[var w := w], where f [x := v] denotes functional override. That is, the viewfront of
thread t for variable var w is updated to the write w that t reads. The viewfronts of the other
                      Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL         9

threads as well as the viewfront of t on variables different from var w are unchanged. Thus, the
function RdX required by the translation of a relaxed read command in Section 3 is thus defined by:
definition value σ w ≡ val ( mods σ w )
fun RdX :: " L ⇒ T ⇒ Cstate ⇒ ( Cstate × V )" where
    " RdX x t σ = ( let w = getVW σ t x; v = value σ w in
                  ( r e a d _ t r ansX t w σ , v ))"
We use value σ w to obtain the value of the write w in state σ. The update defined by function
read_transA t w σ for an acquiring read is conditional on whether w is a relaxed write. If w
is relaxed, tview σ t is updated to (tview σ t)[var w := w] (i.e., behaves like a relaxed read).
Otherwise, the viewfront of t must be updated to “catch up” with the viewfront of w. In particular,
tview σ t is updated to (tview σ t) ⊗ (mview σ w), where
                                      (
                                        v1 x if tst(v2 x) ≤ tst(v1 x)
                          (f ⊗ g) x =
                                        v2 x otherwise
Overall, we have:
fun RdA :: " L ⇒ T ⇒ Cstate ⇒ ( Cstate × V )" where
    " RdA x t σ = ( let w = getVW σ t x; v = value σ w in
                  ( r e a d _ t r ansA t w σ , v ))"

Write transition. Writes update all state components except covered. First, following Doherty
et al. [11], we must identify an existing write w in the current state; the new write is to be inserted
immediately after w. Moreoever, w must be visible to the thread performing the write and covered
by an RMW update. We define the following function to
definition " getVWNC σ t x ≡
    SOME w . w ∈ v i s i b l e _ w rite s σ t x ∧ w ∈
                                                    / σ covered "
where NC stands for “not covered”. The write operation must also determine a new timestamp, ts
for the new write. Given that the new write is to be inserted immediately after the write operation
w, the timestamp ts must be greater than tst w but smaller than the timestamp of other writes on
var w after w. Thus, we obtain a new timestamp using:
definition " getTS σ w ≡
  SOME ts . tst w < ts ∧
     (∀ w ' ∈ writes σ. var w ' = var w ∧ tst w < tst w ' −→
                               ts < tst w ')
Finding such a timestamp is always possible since timestamps are rational numbers (i.e., are dense).
    As with reads, we require a function write_trans t b w v σ ts that updates the state σ so
that a new write w’ = ((var w), ts) for thread t is introduced with write value v. The Boolean
b is used to distinguish relaxed and releasing writes. The write w is the write after which the new
write w’ is to be introduced. The effect of write_trans is to update writes σ to writes′ , mods σ
to mods′ and both tview σ t and mview σ w′ to tview′ , where:
                              writes′ = (writes σ) ∪ {w’}
                                mods′ = (mods σ w’)[val := v, rel := b]
                               tview′ = (tview σ t)[(var w) := w’]
10     Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

Thus, writes′ adds the new write w’ to the set of writes of σ. The new mods′ sets the value for w’
to v and the rel field to b (which is True iff the new write w’ is releasing). Finally, tview′ updates
tview of t for variable var w (the variable that both w and w’ update) to w’.
    Finally, the functions WrX and WrR required by the translations in Section 3 are given as follows
fun WrX :: " L ⇒ V ⇒ T ⇒ Cstate ⇒ Cstate " where
  " WrX x v t σ =
       ( let w = getVWNC σ t x ; ts ' = getTS σ w in
                   w r i t e _ t ra ns t False w v σ ts ')"
fun WrR :: " L ⇒ V ⇒ T ⇒ Cstate ⇒ Cstate " where
  " WrR x v t σ =
       ( let w = getVWNC σ t x ; ts ' = getTS σ w in
                   w r i t e _ t ra ns t True w v σ ts ')"
Update transition. Following Doherty et al. [11], we assume that an update performs both an
acquiring read and a releasing write in a single step. It is possible to define variations that do not
synchronise the read or a write, but we omit such details for simplicity.
   We first define a function update_trans t w v σ ts that modifies σ so that a releasing write
w’ = ((var w), ts) by thread t is introduced with write value v immediately after an existing
write w. The effect of update_trans is to update writes σ to writes′ , covered σ to covered′ , and
mods σ to mods′ , and both tview σ t and mview σ w’ to tview′ , where

             writes′ = (writes σ) ∪ {w’}
            covered′ = (covered σ) ∪ {w}
               mods′ = (mods σ w’)[val := v, rel := True]
                       (
                         (tview σ t)[(var w) := w’] ⊗ (mview σ w) if rel (mods σ w)
              tview′ =
                         (tview σ t)[(var w) := w’]               otherwise

Thus, writes′ adds the new write w’ corresponding to the update to the set of writes of σ and
covered′ adds the write w that w’ reads from to the covered writes set of σ. The new mods′ sets the
value for w’ to v and sets the rel field to True. Finally, tview′ updates tview of t in the same way
as a read operation, except that the first case is taken provided the write w being read is releasing.
    The function Upd required by the translation in Section 3 is given as follows:
fun Upd :: " L ⇒ V ⇒ T ⇒ Cstate ⇒ ( Cstate × V )" where
" Upd x v t σ = ( let w = getVWNC σ t x ; ts = getTS σ w ;
                      v = value σ w in
                         ( u p d a t e _ t rans t w v σ ts , v ))"
Well formedness. Section 5 presents an assertion language for verifying C11 programs. The lem-
mas introduced there require states to be well formed, which we characterise by predicate wfs
defined below.
definition " writes_on σ x ≡ { w . var w = x ∧ w ∈ writes σ }"
definition " lastWr σ x ≡ (x , Max ( tst `( writes_on σ x )))"
definition " wfs σ ≡
          (∀ t x . tview σ t x ∈ writes_on σ x ) ∧
                       Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL        11

             (∀ w x . mview σ w x ∈ writes_on σ x ) ∧
             (∀ x . finite ( writes_on σ x )) ∧
             (∀ w . w ∈ writes σ −→ mview σ w ( var w ) = w ) ∧
             (∀ w x . w = lastWr σ x −→ w ∈   / covered σ )"
Function writes_on σ x returns the set of writes in σ to variable x. Function lastWr σ x returns
the write on x whose timestamp is greater than the timestamp of all other writes on x in state σ.
       In the definition of wfs σ, the first two conjuncts ensure that all writes recorded in tview and
mview are consistent with writes σ. The third ensures the set of writes in σ is finite and the fourth
ensures that for each write in σ, the write’s modification view of the variable it writes is the write
itself. The final conjuct ensures that the last write to each variable (i.e., the write with the largest
timestamp) is not covered. We have shown that wfs is stable under each of the transitions WrX, WrR,
. . . . Thus the well-formedness assumption made by the lemmas in Section 5 is trivially guaranteed.


5     An Assertion Language for Verifying C11 Programs
In the previous sections, we discussed how the existing Owicki-Gries theories in Isabelle can be
extended with a weak memory C11 operational semantics in order to reason about C11-style pro-
grams using standard proof rules. We mentioned that how a novel set of assertions introduced in [9]
can be used in our extension to annotate programs w.r.t. C11 state and reason about them. In this
section we introduce the assertion language and present their encodings in Isabelle through a num-
ber of examples and litmus tests. We also provide some of the rules (lemmas) that Isabelle uses to
discharge proof obligations and validate the proof outlines. We show how C11 state is incorporated
into the programs and shared variables are defined. We also present a fully verified encoding of the
Peterson’s mutual exclusion algorithm to further validate our approach.

5.1   Load Buffering
Our first example is the load-buffering litmus test given in Fig. 7. As discussed earlier, we use
restricted C11 memory model described by Lahav et al. [23], and hence we prevent the program
from terminating by reading 1 for both x in thread 1 and y in thread 2.
    As mentioned earlier, the C11 state is represented as a field of the record corresponding to the
state of the program (i.e. as a field of lb_state record for the load-buffering example). Updates to
σ are via the underlying definition of the operations in accordance with the RC11-RAR operational
semantics as described in Section 4.2. In our encoding, shared variables are represented as constants
representing locations in the C11 state (σ).
    Now consider the proof outline. The first assertion (lines 10-12) specifies the initial state of
the program. The first two conjuncts are assertions on the value of local registers. The other four
conjuncts are definite observation assertions. A definite observation assertion denoted [x =t n] σ
states that thread t’s viewfront is consistent with the last write to x in σ and that this write has
value n. Thus, if t reads from x, it is guaranteed to return n. σ. Formally,
 [ x =t n ] σ ≡
      tview σ t = lastWr σ x ∧ value σ ( lastWr σ x ) = n
All weak-memory assertions in the proof outline of Fig. 7 are definite value assertions, and this
is sufficient to prove the postcondition. However, to discharge the generated proof obligations, we
require the following two proof rules over C11 assertions, which are defined as Isabelle lemmas:
12        Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty


 1    consts                                              1   consts
 2      x :: L      y :: L                                2    d :: L      f :: L
                                                          3
 3
                                                          4   record mp_state =
 4    record lb_state =                                   5    r1 :: V r2 :: V          σ :: Cstate
 5      r1 :: V                                           6
 6      r2 :: V                                           7   || -
 7      σ :: Cstate                                       8   {| [f =1 0] ´σ ∧ [f =2 0] ´σ ∧
 8                                                        9       [d =1 0] ´σ ∧ [d =2 0] ´σ |}
 9    || -                                               10   COBEGIN
10    {| ´r1 = 0 ∧ ´r2 = 0 ∧                             11       {| ¬[f ≈2 1] ´σ ∧ [d =1 0] ´σ |}
11        [x =1 0] ´σ ∧ [x =2 0] ´σ ∧                    12       <d := 1 5 ´σ > ;;
12        [y =1 0] ´σ ∧ [y =2 0] ´σ |}                   13       {| ¬[f ≈2 1] ´σ ∧ [d =1 5] ´σ |}
13    COBEGIN                                            14       <f := R 1 1 ´σ >
14        {| [y =2 0] ´σ ∧ ´r2 = 0 |}                    15       {| True |}
15        < ´r1 ←1 x ´σ > ;;                             16   ||
16        {| [y =2 0] ´σ ∧ ´r2 = 0 |}                    17       DO {| [f = 1]Ld =2 5M ´σ |}
17        < y := 1 1 ´σ >                                18            < ´r1 ←A 2 f ´σ>
18        {| ´r1 = 0 ∨ ´r2 = 0 |}                        19       UNTIL ( ´r1 = 1)
19    ||                                                 20       INV {| [f = 1]Ld =2 5M ´σ ∧
20        {| [x =1 0] ´σ ∧ ´r1 = 0 |}                    21              ( ´r1 = 1 −→ [d =2 5] ´σ) |}
21        < ´r2 ←2 y ´σ > ;;                             22       OD ;;
22        {| [x =1 0] ´σ ∧ ´r1 = 0 |}                    23       {| [d =2 5] ´σ|}
23        < x := 2 1 ´σ >                                24       < ´r2 ←2 d ´σ>
24        {| ´r1 = 0 ∨ ´r2 = 0 |}                        25       {| ´r2 = 5 |}
25    COEND                                              26   COEND
26    {| ´r1 = 0 ∨ ´r2 = 0 |}                            27   {| ´r2 = 5 |}
Fig. 7. Isabelle encoding of the load-buffering lit-     Fig. 8. Isabelle encoding of the message-passing lit-
mus test.                                                mus test.


lemma d_obs_RdX_pres :                            lemma d_obs_WrX_diff _v ar _ pr es :
assumes " wfs σ"                                   assumes " wfs σ"
and "[ x = t u] σ"                                    and "[ x = t u] σ"
shows "[ x = t u ]                                    and " y 6= x "
        ( fst ( RdX y t ' σ ))"                       shows "[ x = t u ] ( WrX y v t ' σ )"
Lemmas d_obs_RdX_pres and d_obs_WrX_diff_var_pres give conditions for preserving definite
value assertions for relaxed read and write transitions, respectively for an arbitrary variable y
and thread t’. Note d_obs_WrX_diff_var_pres requires that the variable y that is written to is
different from the variable x that appears in the definite value assertion. Both lemmas are proved
sound with respect to the operational semantics in Section 4.2. Of course d_obs_RdX_pres also holds
for an acquiring read transition and d_obs_WrX_diff_var_pres for a releasing write transition5 .
    The assertions on lines 14 and 20 are locally correct because of the initial state. The assertions
on lines 16 and 22 are locally correct using d_obs_RdX_pres. Local correctness of the assertions on
lines 18 and 24 is trivial follows by the definite value assertion. Interference freedom of the assertions
in lines 14, 16, 20 and 22 is also established using the two lemmas.

5.2      Message-Passing
We now consider the assertions used in the message-passing algorithm (Fig. 8). The first new
assertion used in the proof outline is the possible observation assertion. This assertion (denoted [x
5
     In fact, our Isabelle theory provides a generic lemma that applies to both cases simultaneously.
                       Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL        13

≈t n] σ) states that thread t may read value n if it reads from variable x. The formal definition
in Isabelle is as follows:
[ x ≈t n ] σ ≡ ∃ w . w ∈ v i s i b l e _ w rite s σ t x ∧ n = value σ w
The next assertion we introduce is the conditional observation assertion (denoted [x = n]Ly =t mM
σ) which states that if thread t reads a value n using an acquiring read for x, it synchronises with
the corresponding write and obtains the definite value m for y. Note that this requires that any write
to x with value n that t can read is a releasing write. The formal definition in Isabelle is as follows:
[ x = n ]Ly = t mM σ ≡
   ∀ w ∈ v i s i b l e _ wr ites σ t x. value σ w = n −→
      mview σ w y = lastWr σ y ∧ value σ ( lastWr σ y ) = m
          ∧ rel ( mods σ w )"
   Here we only introduce two of the interesting rules used in the proof, and refer the interested
reader to the Isabelle theories for the remaining lemmas:
lemma c_obs_intro :                             lemma c_obs_transfer :
assumes " wfs σ"                                assumes " wfs σ"
and "[ y = t m ] σ"                             and "[ x = u ]Ly = t vM σ"
and "¬[ x ≈t′ n ] σ"                            and " snd ( RdA σ x t ) = u "
and " x 6= y "                                  shows "[ y = t v ] ( fst ( RdA x t σ ))"
and " t 6= t '"
shows "[ x = u]Ly = t′ vM
           ( WrR x u t σ )"
Consider the conditional observation assertion in line 17. Local correctness holds trivially by ini-
tialisation. Interference freedom under line 12 is straightforward. For interference freedom under
line 14, we use c_obs_intro. In particular, the assertion at line 13 (i.e., the precondition of line 14)
satisfies the critical premises of c_obs_intro. We use the conditional observation assertion (line 17
of thread 2) in combination with rule c_obs_transfer to establish a definite observation on a new
variable in thread 2. We note that the variable read by the transition in rule c_obs_transfer is x,
whereas the definite value assertion in the consequent is on variable y. Full details of this proof may
be found in [9]; in this paper, we focus on automation, which we discuss in Section 5.5.

5.3   Read-Read Coherence
We have verified three versions of the read-read coherence (RRC) litmus test using our extended
theories. We have provided the more interesting of the three in Fig. 9. The other two versions
are provided Appendix A. In order to prove this example, a richer set of assertions is required. In
particular, in addition to the assertions regarding observability of writes, we need assertions about
the order of writes and the limits on the occurrence of values.
    The first assertion used for this example that we discuss here is the possible value order assertion
(denoted [m ≺x n] σ), which states that there exists a write to variable x with value n ordered after
(i.e., with a greater timestamp) a write to x with value m. Similarly, a definite value order assertion
(denoted [m ≺≺x n] σ) states that all writes to x with value n are ordered after all writes to x with
value m. These are formally defined in Isabelle as follows.
[ m ≺x n ] σ ≡
  ∃ w w '. w ∈ writes_on σ x ∧ w ' ∈ writes_on σ x ∧
14           Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

          value σ w = m ∧ value σ w ' = n ∧ ( tst w ) < ( tst w ')
[ m ≺≺x n ] σ ≡
    (∀ w w '. w ∈ writes_on σ x ∧ w ' ∈ writes_on σ x ∧
      value σ w = m ∧ value σ w ' = n −→ ( tst w ) < ( tst w '))
   ∧ [ m ≺x n ] σ
   The other two assertions appear in this proof outline fall into the value occurrence category:
[0x n]i means that there has not been a write with value n to variable x (where i is the initial
value of x) and [1x n] means that there has been at most one write with value n to x. These two
assertions are defined in terms of ordering assertions introduced earlier as follows. The predicate
init σ x n holds iff the initial value of x in σ is n.
definition init σ x n ≡
 ∃ w . w ∈ writes_on σ x ∧ value σ w = n ∧
   (∀ w ' ∈ writes_on σ x . w 6= w ' −→ ( tst w ) < ( tst w '))
[0x n] i σ ≡ init σ x n ∧ ¬[ i ≺x n ]
[1x n] σ ≡ ¬[ n ≺x n ]
                                                                                                   enc
   The last new assertion used in this proof outline is encountered value (denoted as [x = t n])
means that thread t has had the opportunity to observe a write with value n of x. This assertion is
formally defined in Isabelle as follows6 :
       enc
    [x = t n] σ ≡ ∃ w . w ∈ writes_on σ x ∧
                   tst ( w) ≤ tst ( tview σ t x ) ∧ value σ w = n
   The five assertions above, together with other assertions introduced earlier, are sufficient to
specify the behaviour of the three-threaded version of RRC. The conditional observation assertion
on line 18, is used to capture the possible synchronisation between threads 1 and 2. The ordering
assertions in thread 2 and 3 specify that if the writes have happened in a specific order, the read
order must remain coherent with respect to the order of writes. Namely, if thread 2 synchronises
with thread 1 (i.e., r1 is set to 1), then it must have observed the write of x at line 12. Thus, the
write to x with value 2 at line 23 must have happened after. Therefore, it must be impossible for
the third thread to read value 2 for x at line 27, then subsequently read 1 for x at line 29. This
reasoning is captured by the postcondition of the program.


5.4     Peterson’s Algorithm for C11

The final non-trivial example in this paper is Peterson’s mutual exclusion algorithm (Fig. 10) as
described in [39]. The proof outline for this algorithm has the new assertion covered (denoted cvd[x,
n] σ). The assertion cvd[x, n] σ means that every write to x in state σ except the last is covered
and the value written by that last write is n. This assertion is formally defined in Isabelle as:
cvd [x , n ] σ ≡
  ∀ w . w ∈ writes σ ∧ var σ w = x ∧ w 6∈ covered σ −→
                           w = lastWr σ x ∧ value σ w = n
6
     Note that some of the notation in our Isabelle encoding is different. We use the notation from [9] here
     for a cleaner presentation.
                       Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL           15

 1    consts                                           18   {|[0x 2]0 ´σ ∧ [y = 1]Lx =2 1M ´σ|}
 2      x :: L    y :: L                               19       < ´r1 ←A 2 y ´σ> ;;
 3    record rrc3_state =                              20   {|( ´r1 = 1 −→ [ x =2 1] ´σ ∧
 4      a :: V b :: V r1 :: V                                                    enc
 5      σ :: Cstate                                    21                     [x = 2 1] ´σ) ∧
 6                                                     22       [0x 2]0 ´σ|}
 7   || -                                               23      <x :=2 2 ´σ>
 8   {|[x =2 0] ´σ ∧ [y =3 0] ´σ|}                      24  {| ´r1 = 1 −→ [1 ≺   ≺x 2] ´σ|}
 9    COBEGIN                                           25  ||
10   {|[0x 1]0 ´σ ∧ ¬[y ≈2 1] ´σ ∧                      26  {| True |}
11      ([0x 2]0 ´σ −→ [x =1 0] ´σ)|}                   27      < ´a ←3 x ´σ> ;;
12      <x :=1 1 ´σ> ;;                                            enc
                                                        28  {| [x = 3 ´a] ´σ |}
13   {|¬ [y ≈2 1] ´σ ∧
                                                        29      < ´b ←3 x ´σ>
14      ([0x 2]0 ´σ −→ [x =1 1] ´σ)|}                   30  {|( ´a 6= ´b −→ [ ´a ≺x ´b] ´σ)|}
              R
15      <y := 1 1 ´σ>                                   31  COEND
16   {| True |}                                         32  {| ´r1 = 1 ∧ ´a = 2 −→ ´b 6= 1|}
17   ||
Fig. 9. Isabelle encoding of the read-read coherence litmus test with three threads. The proof additionally
relies on a global invariant [init x 0] ´σ ∧ [init y 0] ´σ ∧ [1x 1] ´σ ∧ [1x 2] ´σ

Similar to the previous examples, in order to prove the Peterson’s algorithm we will need to introduce
new proof rules to deal with assertions involving cvd.
    The proof also uses auxiliary variables after1 and after2. We set after1 to True when turn is
set in thread 1 and to False when thread 1 exits its critical section (i.e., when the flag is reset). This
is a standard technique used in Owicki-Gries proofs of Peterson’s algorithm in the conventional,
sequentially consistent, setting [5, 28]. Note that introduction of auxiliary variables must follow the
same rules as the classical setting [29] and must not be a shared constant that appears within the
weak memory state σ. This avoids the notions of unsoundness of auxiliary variables described in
earlier work [25].

5.5    Verification Strategy
For each of the algorithms described above, we employ a generic verification strategy and outline the
the proof effort. After encoding the algorithm and the assertions, the main steps in each validating
the proof outlines are as follows.
 1. First, we use the built-in oghoare tactic to reduce an Owicki-Gries proof outline into a set of
    basic Hoare logic proof obligations over weak memory pre-post state assertions. This tactic is
    exactly as developed by Nipkow and Nieto [28], and is used without change.
 2. We pipe this output (which is a set of proof obligations on atomic commands) to the Isabelle
    simplifier, transforming the set-based representation of assertions by Nipkow and Nieto into a
    predicate-based representation. This allows the lemmas for weak memory that we haved adapted
    from [9] to be automatically matched with the proof obligations.
For the simple litmus tests, the first two steps either discharge all the proof obligations, or leave a few
(maximum 6) proof obligations unproved. These proof obligations require slightly more sophisticated
application of the lemmas over weak memory state than can be discharged by the simplifier alone.
However, they can be automatically discharged using Isabelle’s built-in sledgehammer tool [7].
   This verification strategy works equally well for Peterson’s algorithm although it is a larger
example that generates a significantly higher number of proof obligations. The oghoare tactic gen-
erates 258 subgoals, but over half of these are discharged by step 2 above, leaving 91 subgoals.
16      Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty


|| -
{| ´after1 ∧ ¬ ´after2 ∧ [flag1 =1 0] ´σ ∧ [flag2 =2 0] ´σ ∧
    [turn =1 0] ´σ ∧ [turn =2 0] ´σ |}
COBEGIN
  {| ´¬ after1 ∧ [flag1 =1 0] ´σ ∧ (cvd[turn, 0] ´σ ∨ cvd[turn, 1] ´σ) ∧
      (´after2 −→ cvd[turn, 1] ´σ ∧ [turn = 1]Lflag2 =1 1M ´σ) ∧
      ¬ [turn ≈2 2] ´σ |}
  < flag1 := 1 1 ´σ >;;
  {| ¬ ´after1 ∧ [flag1 =1 1] ´σ ∧ ¬ [turn ≈2 2] ´σ ∧
      (¬ ´after2 −→ cvd[turn, 1] ´σ ∧ [turn = 1]Lflag2 =1 1M ´σ) |}
  h< SWAP [ turn , 2] 1 ´σ >,, ´after1 := Truei ;;
  DO
    {| ´after1 ∧ (´after2 ∧ ([flag2 ≈1 0] ´σ ∨ [turn ≈1 1] ´σ) −→ [turn =2 1] ´σ)|}
    < ´r1 ←A 1 flag2 ´σ >;;
    {| ´after1 ∧
        (´after2 ∧ ( ´r1 = 0 ∨ [turn ≈1 1] ´σ ∨ [flag2 ≈1 0] ´σ) −→
                                                                  [turn =2 1] ´σ)|}
    < ´r2 ←1 turn ´σ >
  UNTIL ( ´r1 = 0 ∨ ´r2 = 1)
  INV
  {| ´after1 ∧
      (´after2 ∧ ( ´r1 = 0 ∨ ´r2 = 1 ∨ [turn ≈1 1] ´σ ∨ [flag2 ≈1 0] ´σ) −→
                                                                  [turn =2 1] ´σ) |}
  OD ;;
  {| ´after1 ∧ (´after2 −→ [turn =2 1] ´σ)|}
  h< flag1 := R 1 0 ´σ >,, ´after1 := False i
  {| True |}
|| Thread 2 ( symmetric )
COEND
{| True |}
Fig. 10. Proof outline for Peterson’s algorithm under C11. The second thread (not shown here) is symmetric.

Although automatic, repeated applications of sledgehammer to discharge so many proof obligations
is rather tedious. However, one can quickly discover common patterns in the proof steps allowing
these proof obligations to be discharged via a few simple applications of apply-style proofs.


6    Related Work
As has been mentioned, the current paper builds on ideas found in [11]. That paper did not develop
a program logic based on Hoare triples, and was limited to invariance style proofs. Both [11] and the
current paper use the same definite value assertion, but the current paper employs a much richer
and more powerful assertion language. In particular, the conditional value assertion is critical for
enabling an Owicki-Gries based program logic. Finally, [11] does not consider mechanisation or
automation.
   Of course, a great deal of work has been put into the development of separation logics for
C11-style weak memory models [12, 14, 19, 37, 38]. One of the mosty recent and perhaps most
fundamental of these is the Iris framework [19]. This framework has been formalised in the Coq
proof assistant, and instantiations of it support a large fragemt of C11. This fragment contains
C11’s nonatomic accesses but not relaxed accesses and is therefore incomparable to our own. In
particular, nonatomic access cannot legally race, whereas relaxed accesses are designed to enable
                       Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL         17

racy code. More generally, separation logics can become complicated when applied to weak-memory,
and we are partly motivated by the desire to build verification frameworks atop simple and natural
relational models (other authors [25] have made similar observations).
    There have been a number of recent attempts to develop mechanised deductive verification
support for weak memory. Summers and Müller [34] present an approach to automating deductive
verification for weak memory programs by encoding Relaxed Separation Logic [38] and Fenced
Separation Logic [12,14] into Viper [27]. Their work builds on separation logic, whereas ours builds
on a relational framework. Apart from this fundamental difference, Summers and Müller encode
the concurrent logics into the Viper sequential specification framework, which provides a high
level of automation. On the other hand, and as the authors themselves note, encoding the logic in a
foundational verification tool such as Isabelle provides a higher level of assurance about correctness.
In particular, the entire development of our framework is verified in Isabelle, down to the operational
semantics.
    Another technique based on Owicki-Gries is that of [25], which defines a proof system for the
release-acquire fragment of C11, a smaller fragment than the release-acquire-relaxed fragment that
we treat in this paper. It is unclear how difficult it would be to extend [25] to deal with relaxed
accesses. In any case, [25] does not deal with mechanisation or automation.
    Alglave and Cousot have developed another extension to the Owicki-Gries method for weak
memory models [2]. Because their method, like ours, is an extension of the Owicki-Gries method,
their verification method first requires a proof outline. One novelty of their approach is that their
method requires a communication specification (or CS), which involves specifying for each read
operation in the program, which writes the variable can read from (which may be in another
thread). Verifying that the proof outline and CS are together valid, and therefore that assertions of
the proof outline do in fact hold for the program, involves two proof obligations. The first is to show
that the proof outline is valid in our standard sense (so that it is locally correct and noninterfering),
under the assumption that the CS is satisfied. The second obligation is that a given memory model
satisfies the CS. This second obligation constitutes an additional proof effort, not required in our
method. The advantage they gain is that once a proof outline is known to be locally correct and
noninterfering under a given CS, then the algorithm is known to be correct under any memory
model that satisfies the CS.
    The operational semantics in the current paper is inspired by the semantics described in [19,
31]. The current paper is based on semantics and assertions found in [9], which also presents
case-study verifications mechanised in Isabelle. The mechanisation in that paper is rudimentary.
Programs are not represented in a while-style language as in the current paper. Instead, they
use a program-counter based representation, where control flow must be explicitly modelled. As a
consequence, proof obligations are not decomposed in the conventional Owicki-Gries style. Rather,
the verifier must prove stability of a large global invariant mapping program counter locations to
the assertions that hold at that location. Furthermore, there is little real automation, either in
generating or discharging proof obligations. The current paper presents a highly-structured and
mechanised Owicki-Gries framework supporting a high level of automation.
    Dan et al. [10] introduce an abstraction for the store buffers of the weak memory model which
reduces the workload on program analysers. They provide a source-to-source transformation that
realises the abstraction producing a program that can be analysed with verifiers for sequential con-
sistency. The approach is integrated with ConcurInterproc [18] and uses the Z3 theorem prover.
Model checking has also been targeted for weak memory, e.g., by explicitly encoding architectural
structures leading to weak behaviour, like store buffers [3, 36]. Ponce de León et al. [16, 32] have
18      Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

developed a bounded model checker for weak memory models, taking the axiomatic description of
a memory model as input. (Bounded) model checkers for specific weak memory models are fur-
thermore the tools CBMC [4] (for TSO), Nidhugg [1] (for TSO and PSO), RCMC [21] (for C11)
and GenMC [22]. Others [8] present an approach for modelling and verifying C11 programs using
Event-B and ProB model checker.


7    Conclusion
In this paper, we have introduced an extension to a twenty-year old formalisation of Owicki-Gries
proof calculus in Isabelle [28] in order to tackle the verification problem of C11 programs under
weak memory. We start by developing the necessary language support for defining C11 programs
and have shown that existing operational semantics for the RC11-RAR fragment [11] can be encoded
in a straightforward manner, which provides an example instantiation. We have provided a set of
proof rules to facilitate verification of C11 programs, and exemplified our approach by verifying a
number of example programs.
    Our entire development has been carried out in the Isabelle theorem prover and is modular with
respect to the underlying memory model. For the RC11-RAR fragment we consider, we have shown
that the proofs are highly automated. As described in Section 5.5, a simple pattern of applying an
Owicki-Gries specific proof method, and then invoking SMT solvers via Isabelle’s sledgehammer
tool was sufficient for verifying every proof outline. Moreover, the use of Isabelle means that we
have flexibility in the specific operational semantics that we use.


References
 1. Abdulla, P.A., Aronis, S., Atig, M.F., Jonsson, B., Leonardsson, C., Sagonas, K.: Stateless model
    checking for TSO and PSO. Acta Inf. 54(8), 789–818 (2017)
 2. Alglave, J., Cousot, P.: Ogre and Pythia: an invariance proof method for weak consistency models. In:
    Castagna, G., Gordon, A.D. (eds.) POPL. pp. 3–18. ACM (2017)
 3. Alglave, J., Kroening, D., Nimal, V., Tautschnig, M.: Software verification for weak memory via program
    transformation. In: Felleisen, M., Gardner, P. (eds.) ESOP. LNCS, vol. 7792, pp. 512–532. Springer
    (2013)
 4. Alglave, J., Kroening, D., Tautschnig, M.: Partial orders for efficient bounded model checking of con-
    current software. In: Sharygina, N., Veith, H. (eds.) CAV. LNCS, vol. 8044, pp. 141–157. Springer
    (2013)
 5. Apt, K.R., de Boer, F.S., Olderog, E.: Verification of Sequential and Concurrent Programs. Texts in
    Computer Science, Springer (2009)
 6. Batty, M., Owens, S., Sarkar, S., Sewell, P., Weber, T.: Mathematizing C++ concurrency. In: Ball, T.,
    Sagiv, M. (eds.) POPL. pp. 55–66. ACM (2011)
 7. Böhme, S., Nipkow, T.: Sledgehammer: Judgement day. In: IJCAR. Lecture Notes in Computer Science,
    vol. 6173, pp. 107–121. Springer (2010)
 8. Dalvandi, M., Dongol, B.: Towards deductive verification of C11 programs with Event-B and ProB. In:
    Proceedings of the 21st Workshop on Formal Techniques for Java-like Programs. p. 4. ACM (2019)
 9. Dalvandi, S., Doherty, S., Dongol, B., Wehrheim, H.: Owicki-Gries reasoning for C11 RAR. In: ECOOP
    (2020), (To appear)
10. Dan, A., Meshman, Y., Vechev, M., Yahav, E.: Effective abstractions for verification under relaxed
    memory models. Computer Languages, Systems & Structures 47, 62–76 (2017)
11. Doherty, S., Dongol, B., Wehrheim, H., Derrick, J.: Verifying C11 programs operationally. In:
    Hollingsworth, J.K., Keidar, I. (eds.) PPoPP. pp. 355–365. ACM (2019)
                       Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL            19

12. Doko, M., Vafeiadis, V.: A program logic for C11 memory fences. In: VMCAI. LNCS, vol. 9583, pp.
    413–430. Springer (2016)
13. Doko, M., Vafeiadis, V.: Tackling real-life relaxed concurrency with FSL++. In: ESOP. pp. 448–475
    (2017)
14. Doko, M., Vafeiadis, V.: Tackling real-life relaxed concurrency with fsl++. In: European Symposium
    on Programming. pp. 448–475. Springer (2017)
15. Dolan, S., Sivaramakrishnan, K., Madhavapeddy, A.: Bounding data races in space and time. In: PLDI.
    pp. 242–255. PLDI 2018, ACM, New York, NY, USA (2018)
16. Gavrilenko, N., Ponce de Le’on, H., Furbach, F., Heljanko, K., Meyer, R.: BMC for weak mem-
    ory models: Relation analysis for compact SMT encodings. In: Dillig, I., Tasiran, S. (eds.) CAV.
    LNCS, vol. 11561, pp. 355–365. Springer (2019). https://doi.org/10.1007/978-3-030-25540-4_19,
    https://doi.org/10.1007/978-3-030-25540-4_19
17. Hoare, C.A.R.: An axiomatic basis for computer programming. Commun. ACM 12(10), 576–580 (1969)
18. Jeannet, B.: Relational interprocedural verification of concurrent programs. Software & Systems Mod-
    eling 12(2), 285–306 (2013)
19. Kaiser, J., Dang, H., Dreyer, D., Lahav, O., Vafeiadis, V.: Strong logic for weak memory: Reasoning
    about release-acquire consistency in Iris. In: Müller, P. (ed.) ECOOP. LIPIcs, vol. 74, pp. 17:1–17:29.
    Schloss Dagstuhl - Leibniz-Zentrum fuer Informatik (2017)
20. Kang, J., Hur, C., Lahav, O., Vafeiadis, V., Dreyer, D.: A promising semantics for relaxed-memory
    concurrency. In: POPL. pp. 175–189. ACM (2017)
21. Kokologiannakis, M., Lahav, O., Sagonas, K., Vafeiadis, V.: Effective stateless model checking for
    C/C++ concurrency. PACMPL 2(POPL), 17:1–17:32 (2018)
22. Kokologiannakis, M., Raad, A., Vafeiadis, V.: Model checking for weakly consistent libraries. In: McKin-
    ley, K.S., Fisher, K. (eds.) PLDI. pp. 96–110. ACM (2019)
23. Lahav, O., Vafeiadis, V., Kang, J., Hur, C., Dreyer, D.: Repairing sequential consistency in C/C++11.
    In: PLDI. pp. 618–632. ACM (2017)
24. Lahav, O.: Verification under causally consistent shared memory. SIGLOG News 6(2), 43–56 (2019)
25. Lahav, O., Vafeiadis, V.: Owicki-Gries reasoning for weak memory models. In: Halldórsson, M.M.,
    Iwama, K., Kobayashi, N., Speckmann, B. (eds.) ICALP. LNCS, vol. 9135, pp. 311–323. Springer
    (2015)
26. Lamport, L.: How to make a multiprocessor computer that correctly executes multiprocess programs.
    IEEE Trans. Computers 28(9), 690–691 (1979)
27. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastructure for permission-based
    reasoning. In: International Conference on Verification, Model Checking, and Abstract Interpretation.
    pp. 41–62. Springer (2016)
28. Nipkow, T., Nieto, L.P.: Owicki/Gries in Isabelle/HOL. In: FASE. Lecture Notes in Computer Science,
    vol. 1577, pp. 188–203. Springer (1999)
29. Owicki, S.S., Gries, D.: An axiomatic proof technique for parallel programs I. Acta Inf. 6, 319–340
    (1976)
30. Paulson, L.C.: Isabelle - A Generic Theorem Prover (with a contribution by T. Nipkow), LNCS, vol. 828.
    Springer (1994)
31. Podkopaev, A., Sergey, I., Nanevski, A.: Operational aspects of C/C++ concurrency. CoRR
    abs/1606.01400 (2016)
32. Ponce de León, H., Furbach, F., Heljanko, K., Meyer, R.: BMC with memory models as modules. In:
    Bjørner, N., Gurfinkel, A. (eds.) FMCAD. pp. 1–9. IEEE (2018)
33. de Roever, W.P., de Boer, F.S., Hannemann, U., Hooman, J., Lakhnech, Y., Poel, M., Zwiers, J.:
    Concurrency Verification: Introduction to Compositional and Noncompositional Methods, Cambridge
    Tracts in Theoretical Computer Science, vol. 54. Cambridge University Press (2001)
34. Summers, A.J., Müller, P.: Automating deductive verification for weak-memory programs. In: Beyer,
    D., Huisman, M. (eds.) TACAS. LNCS, vol. 10805, pp. 190–209. Springer (2018)
20     Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty

35. Svendsen, K., Pichon-Pharabod, J., Doko, M., Lahav, O., Vafeiadis, V.: A separation logic for a promis-
    ing semantics. In: Ahmed, A. (ed.) ESOP. LNCS, vol. 10801, pp. 357–384. Springer (2018)
36. Travkin, O., Mütze, A., Wehrheim, H.: SPIN as a linearizability checker under weak memory models.
    In: Bertacco, V., Legay, A. (eds.) HVC. LNCS, vol. 8244, pp. 311–326. Springer (2013)
37. Turon, A., Vafeiadis, V., Dreyer, D.: GPS: navigating weak memory with ghosts, protocols, and sepa-
    ration. In: Black, A.P., Millstein, T.D. (eds.) OOPSLA. pp. 691–707. ACM (2014)
38. Vafeiadis, V., Narayan, C.: Relaxed separation logic: A program logic for c11 concurrency. In: Proceed-
    ings of the 2013 ACM SIGPLAN international conference on Object oriented programming systems
    languages & applications. pp. 867–884 (2013)
39. Williams, A.: https://www.justsoftwaresolutions.co.uk/threading/petersons_lock_with_C++0x_atomics.html
    (2018), accessed: 2018-06-20
                        Integrating Owicki-Gries for C11-Style Memory Models into Isabelle/HOL     21

A     Appendix
We present proofs of two additional variations of the RRC litmus test. Fig. 11 presents a simple
two-threaded version with a writer thread that enforces a order of writes in program order and a
reader thread that reads from these writes. The proof shows that the order of reads in the reader
is consistent with the order of writes in the writer.


 1   consts
 2     x :: L
 3

 4   record mp_state =
 5     a :: V
 6     b :: V
 7     σ :: Cstate
 8

 9   || -
10   {| ´a = 0 ∧ ´b = 0 |}
11   COBEGIN
12   {| [x =1 0] ´σ ∧ [0x 1] ´σ ∧ [1x 1] ´σ ∧ [0x 2] ´σ ∧ [1x 1] ´σ |}
13       <x := 1 1 ´σ >;;
                          enc
14   {| [x =1 1] ´σ ∧ [x = 1 1] ´σ ∧ [0x 2]0 ´σ ∧ [1x 1] ´σ ∧ [1x 2] ´σ |}
15       <x := 1 2 ´σ >
16   {| [1x 1] ´σ ∧ [1x 2] ´σ ∧ [1 ≺≺x 2] ´σ|}
17   ||
18   {| [1x 1] ´σ ∧ [1x 2] ´σ |}
19       < ´a ←2 x ´σ > ;;
            enc
20   {| [x = 2 a] ´σ |}
21       < ´b ←2 x ´σ>
22   {| (´a 6= ´b −→ [´a ≺x ´b] ´σ) |}
23   COEND
24   {| ´a = 2 −→ ´b 6= 1 |}

            Fig. 11. Isabelle encoding of the read-read coherence litmus test with two threads.

    Fig. 12 presents the standard four-threaded version in which the two writes to x occur in two
different threads. There are two reader threads both of which read from x twice. One must prove
that the order of writes read by both threads are consistent. In particular, if a is set to 1 and b to
2, then thread 3 must have seen the writes to x in that order. It should therefore not be possible
for thread 3 to read 1 for x if it has already seen the value 2 in the first read at line 29.
22      Sadegh Dalvandi, Brijesh Dongol, and Simon Doherty




1    consts
2      x :: L
3

4    record rrc4_state =
5      a :: V
6      b :: V
7      c :: V
8      d :: V
9      σ :: Cstate
10

11   || -
12   {| [x =1 0] ´σ ∧ [x =2 0] ´σ ∧ [x =3 0] ´σ ∧ [x =4 0] ´σ |}
13   COBEGIN
14   {| [0x 1]0 ´σ ∧ [1x 1] ´σ |}
15       <x :=1 1 ´σ>
16   {| True |}
17   ||
18   {| [0x 2]0 ´σ ∧ [1x 2] ´σ |}
19       <x :=2 2 ´σ>
20   {| True |}
21   ||
22   {| True |}
23       < ´a ←3 x ´σ> ;;
            enc
24   {| [x = 3 ´a] ´σ ∧ [1x 2] ´σ ∧ (´a = 1 −→ [1x´a] ´σ) |}
25       < ´b ←3 x ´σ>
26   {|(´a 6= ´b −→ [´a ≺x ´b] ´σ) ∧ (´a = 1 −→ [1x´a] ´σ) ∧ (´b = 2 −→ [1x ´b] ´σ)|}
27   ||
28   {| True |}
29       < ´c ←4 x ´σ> ;;
           enc
30   {|[x = 4 ´c] ´σ ∧ (´c = 2 −→ [1x´c] ´σ)|}
31       < ´d ←4 x ´σ>
32   {| (´c 6= ´d −→ [´c ≺x ´d] ´σ) ∧ (´c = 2 −→ [1x´c] ´σ) ∧ (´d = 1 −→ [1x´d] ´σ)|}
33   COEND
34   {| ´a = 1 ∧ ´b = 2 ∧ ´c = 2 −→ ´d 6= 1 |}

           Fig. 12. Isabelle encoding of the read-read coherence litmus test with four threads.
