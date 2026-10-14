            Fast and Verified UNSAT Certificate
                          Checking

                                   Peter Lammich(B)

                      University of Twente, Enschede, Netherlands
                                 p.lammich@utwente.nl



       Abstract. We describe a formally veriﬁed checker for unsatisﬁability
       certiﬁcates in the LRAT format, which can be run in parallel with the
       SAT solver, processing the certiﬁcate while it is being produced. It is
       implemented time and memory eﬃciently, thus increasing the trust in
       the SAT solver at low additional cost.
          The veriﬁcation is done w.r.t. a grammar of the DIMACS format and
       a semantics of CNF formulas, down to the LLVM code of the checker.
       In this paper, we report on the checker and its design process using the
       Isabelle-LLVM stepwise reﬁnement approach.


       Keywords: UNSAT certiﬁcates · LRAT · Isabelle-LLVM · Veriﬁed
       Software


1    Introduction
SAT solvers are highly complex and highly optimized programs, which are used
to verify critical properties of other systems. To increase the trust in them,
SAT solvers produce certiﬁcates that can be independently checked by formally
veriﬁed checkers [5,9,10,16,23,34,35]. Here, the focus is on certiﬁcates for unsat-
isﬁability, as certiﬁcates for satisﬁability are (considered) trivial.
    Typically, certiﬁcate checking proceeds in two phases: An unveriﬁed elabora-
tor adds additional information to the certiﬁcate produced by the SAT solver,
and then a formally veriﬁed checker checks the elaborated certiﬁcate against the
original formula. This approach moves some complicated and computationally
expensive tasks into the unveriﬁed elaborator, making checking of the elaborated
certiﬁcate simpler and less expensive.
    However, the elaborator has to recompute information which is, in principle,
known to the solver, and elaboration typically takes as long as solving. More
recent techniques accelerate elaboration by including this information into the
certiﬁcate [2]. The most recent development are solvers that directly produce
elaborated certiﬁcates [29]. This allows for streaming the certiﬁcates from the
solver into the checker: solving and checking are done in parallel, and the poten-
tially large certiﬁcates need not be stored on disk. When implemented appropri-
ately, the memory footprint of the checker is similar to that of the solver.
c The Author(s) 2024
C. Benzmüller et al. (Eds.): IJCAR 2024, LNAI 14739, pp. 439–457, 2024.
https://doi.org/10.1007/978-3-031-63498-7_26
440      P. Lammich

    There are diﬀerent formats for elaborated unsatisﬁability certiﬁcates, such as
PB [4] and GRAT [23]. The de-facto standard is the LRUP format [10], and its
backwards compatible generalizations LRAT [9] and LPR [35]. These correspond
to the non-elaborated DRUP [17], DRAT [36], and DPR [35] formats. With an
exception in 2023, LRUP is suﬃcient for all top performing solvers in the SAT
competitions of the last years [29].
    In this paper, we present a formally veriﬁed checker that can stream LRUP
certiﬁcates. We benchmark our tool on the CaDiCaL solver [29], where it only
causes a minimal additional computation overhead, and has a memory usage sim-
ilar to that of the solver. Our checker is as fast as the highly optimized unveriﬁed
lrat-trim checker [29], and at least one order of magnitude faster than any other
veriﬁed checker we know of. Using the Isabelle Reﬁnement Framework [22], our
checker is veriﬁed down to the LLVM intermediate representation [26] of its
code, and against a formal grammar of the DIMACS CNF format, which is the
standard for representing CNF formulas [32]. To the best of our knowledge, our
checker is the ﬁrst that comes with a veriﬁed parser. Our tool and benchmark
data is available at https://github.com/lammich/lrat_isa.
    In the rest of this paper, we describe our formal speciﬁcation (Sect. 2),
the abstract certiﬁcate checking algorithm (Sect. 3), and its implementation
(Sect. 4). We then report on our benchmark results (Sect. 5). Finally we con-
clude the paper and discuss related and future work (Sect. 6).


2      Specification

We prove soundness of our checker, i.e., it accepts a string only if it is a repre-
sentation of an unsatisﬁable formula in DIMACS CNF format1 . In this section
we present the formalization of this speciﬁcation.


2.1     Conjunctive Normal Form

Throughout this paper, we will use some simpliﬁed Isabelle/HOL notation, and
explain unusual notations where they ﬁrst occur. For deﬁnitions we use ≡. Data
types are written in preﬁx notation, e.g., lit set for a set of literals. Function
application is denoted as f x1 . . . xn .
   The following is the abstract syntax and semantics of CNF, taken from the
GRAT tool [23] and slightly adapted to our needs:
    typedef var ≡ {v::nat. v = 0}
    lit ≡ Pos var | Neg var    clause ≡ lit set         cnf ≡ clause set

    valuation ≡ var ⇒ bool
    sem lit :: lit ⇒ valuation ⇒ bool
1
    Note that proving completeness is less interesting: even if we show that our checker
    accepts all valid certiﬁcates, the elaborator or solver may still fail to produce one.
    We verify completeness empirically on a large set of benchmarks.
                              Fast and Veriﬁed UNSAT Certiﬁcate Checking          441

 sem lit (Pos v) σ ≡ σ v             sem lit (Neg v) σ ≡ ¬ σ v

 sem cnf :: cnf ⇒ valuation ⇒ bool
 sem cnf F σ ≡ ∀C∈F. ∃l∈C. sem lit l σ

 sat :: cnf ⇒ bool              sat F ≡ ∃σ. sem cnf F σ
A variable is a positive natural number, a literal is a positive or negative variable,
a clause is a set of literals, and a cnf-formula is a set of clauses. A valuation
assigns truth values to variables. For a valuation σ, the semantics assigns truth
values to literals (sem lit) and formulas (sem cnf): a positive literal is true iﬀ its
variable is true, and a negative literal is true iﬀ its variable is false. A formula
is true iﬀ every clause contains a true literal, and it is satisfiable if there is a
valuation for which it is true.


2.2   Specification of the DIMACS CNF Format

DIMACS CNF is the de-facto standard format
for representing CNF formulas. Figure 1 displays
an example: the ﬁle can start with optional com-
ment lines, indicated by a heading ‘c’. After the
comments, there is a header of the form p cnf n
m, where n is the maximum variable, and m is
the number of clauses. Then the clauses follow, Fig. 1. Example formula in
encoded as zero-terminated sequences of integers, DIMACS CNF
where a positive integer represents a positive lit-
eral, and a negative integer represents a negative literal. We need to specify how
a word in DIMACS format corresponds to a formula. While a language is a set
of words, we use a relation between words and corresponding abstract syntax.
By slight abuse of naming, we call such relations grammars. We shallowly embed
regular grammars into Isabelle HOL’s logic:
 (a,r) gM ≡ (a list × r) set
 return x ≡ {([],x)}          C ≡ { ([c],c) | c∈C }
 bind g f ≡ { (w1 @w2 ,r) | ∃x. (w1 ,x) ∈ g ∧ (w2 ,r) ∈ f x }
Here, (w, r) ∈ g means that the grammar g relates the word w to the result r.
The empty relation {} corresponds to the empty language. The relation return x
relates the empty word to the result x. It corresponds to the language {[]} of
only the empty word. The relation C relates single-character words to the
corresponding character from the set C. Finally, the relation bind g f relates a
word w1 w2 to a result r, if g relates w1 to some intermediate result x, and f x
relates w2 to r. This corresponds to concatenation of languages.
    The type gM is a monad, and we use the usual shortcut notation for bind:
 x←g; f x ≡ bind g (λx. f x)          g1 ;g2 ≡ bind g1 (λ . g2 )
442     P. Lammich

We also deﬁne shortcuts to apply a function to the result of a monad, to lift a
binary function into a monad, and to concatenate two grammars, ignoring the
result of the latter:
 a & f ≡ x←a; return (f x)
 lift2 f a b ≡ x←a; y←b; return (f x y)
 a      b ≡ r←a; b; return r
We then deﬁne the relational versions of the power function and the Kleene star:


 g powg 0 ≡ return []     g pow g (n+1) ≡ lift2 (#) g (g pow g n)
 g∗ ≡    n::nat. g pow g n
where x#xs prepends the element x to the list xs. That is, g pow g n and g ∗
relate the input to lists, the elements being the results produced by g. We also
deﬁne g? ≡ (g & Some) ∪ (return None).
    Using the grammar monad, we specify a grammar for the simpliﬁed DIMACS
format as used by SAT competitions since 2009 [32]. We start with deﬁning sets
of ASCII characters:
 whitespace, digits1, digits :: 8 word set
 whitespace ≡ {‘ ’, ‘\t’, ‘\n’, ‘\v’, ‘\f ’, ‘\r’}
 digits1 ≡ {‘1’, . . . , ‘9’}      digits ≡ {‘0’, . . . , ‘9’}
Here, 8 word is the 8-bit word type from Isabelle’s machine word library [3,11].
Note whitespace includes all 6 ASCII whitespace characters. Based on this, we
deﬁne a grammar g dimacs :: (8 word × cnf) set:
 g ws ≡ whitespace ∗ ; return ()         g ws1 ≡ whitespace ; g ws

 g variable ≡ x←digits1 ; xs←digits ∗ ; return (nat of str (x#xs)))
 g literal ≡ ({‘-’} ; g variable & Neg) ∪ (g variable & Pos)
 g clause ≡ (g literal    g ws1)∗ & set     {‘0’}
 g cnf     ≡ (return {})
   ∪ (c←g clause; cs ← (g ws1; g clause)∗ ; return ({c} ∪ set cs))

 g comment ≡ {‘c’} ; −{‘\n’} ∗ ; {‘\n’} ; return ()
 g p header ≡ {‘p’} ; −{‘\n’} ∗ ; {‘\n’} ; return ()
 g comments ≡ (g ws ∪ g comment)∗ ; return ()
 g dimacs ≡ g comments; g p header? ; g ws; g cnf                g ws
Here, nat of str :: 8 word list ⇒ nat converts a string to a natural number, and
set :: a list ⇒ a set yields the set of elements in a list.
    Note that we do not check the contents of the header, which contains auxiliary
information for parsing, but does not aﬀect the represented formula. We also
accept multiple clauses per line and clauses spanning several lines, as well as extra
whitespace anywhere in the ﬁle. Many SAT solvers support similar relaxations
of the format, and we wanted this ﬂexibility in our tool, too.
                             Fast and Veriﬁed UNSAT Certiﬁcate Checking       443

    As a sanity check, we prove that our grammar is unambiguous, i.e., that it
relates the same word to at most one formula:
    (w, f1 ) ∈ g dimacs ∧ (w, f2 ) ∈ g dimacs =⇒ f1 = f2


2.3     Correctness Specification
At this point, we can formalize the postcondition for our checker’s speciﬁcation:
∃F. (w, F ) ∈ g dimacs ∧ ¬sat F means that the sequence of bytes w is a valid
DIMACS CNF representation of an unsatisﬁable formula.


3     Certificates for Unsatisfiability

RUP (reverse unit propagation) certiﬁcates contain the clauses learned by the
solver. The checker justiﬁes that addition of each clause preserves satisﬁability.
For an unsatisﬁable formula, the last learned clause is the empty clause. Adding
the empty clause yields an unsatisﬁable formula, and, as each clause addition is
justiﬁed to preserve satisﬁability, the original formula is unsatisﬁable, too.
    Justiﬁcation is done by reverse unit propagation [14]: a clause C can be added
to the formula F , if the formula F ∧ ¬C is unsatisﬁable, and if this can be shown
by generating an empty clause via unit propagation. For RUP, the checker has to
implement unit propagation itself, for example with a two-watched-literals data
structure [28]. LRUP (linear RUP) certiﬁcates annotate each clause addition,
with the relevant unit clauses in the order they become unit, and the ﬁnal conﬂict
clause. This makes the checker simpler and more eﬃcient, as it only needs to
check if clauses are unit, rather then ﬁnd unit clauses.
    The certiﬁcates also contain clauses deleted by the solver. This allows the
checker to also delete those clauses from its data structures, freeing up memory.
Note that deleting a clause trivially preserves satisﬁability.
    The actual LRUP format uses natural numbers to identify clauses, rather
than spelling them out whenever they are referenced. The n clauses of the initial
formula implicitly get the ids [1, . . . , n]. A clause addition has the form <id>
<literal>* 0 <id>+ 0. It consists of the id under which this clause shall be
added, a zero-terminated list of the literals of the clause, and a zero terminated
list of the unit clauses and the conﬂict clause to justify the addition. A clause
deletion has the form <id>+ 0, and consists of a zero terminated list of the ids
of the clauses to be deleted. There is an ASCII and a more compact binary
encoding for LRUP certiﬁcates.

3.1     Abstract Checker

In this section, we present our formalization of the abstract checker algorithm.
We start with deﬁning some basic concepts:
444       P. Lammich

 − :: lit ⇒ lit   −Pos v ≡ Neg v −Neg v ≡ Pos v
 pan ≡ lit ⇒ bool       consistent (A::pan) ≡ ∀l. ¬ (A l ∧ A (−l))
 sat wrt F A ≡ ∃σ. sem cnf F σ ∧ (∀l. A l =⇒ sem lit l σ)
 conflict A C ≡ ∀l∈C. A (−l)
 is uot A C l ≡ l∈C ∧ ¬A(−l) ∧ (∀l∈C−{l}. A(−l))
 taut C ≡ ∃l. l∈C ∧ −l∈C
The literal −l is the negation of the literal l. A partial assignment (pan) charac-
terizes a set of literals that are assigned (to true). It is consistent if it does not
assign both a literal and its negation. A formula F is satisfiable w.r.t. a partial
assignment A (sat wrt F A), if A can be extended to a satisfying valuation; A
is in conflict with a clause C (conflict A C), if the negations of all the clause’s
literals are assigned. The clause C is unit or true w.r.t. A and a literal l (is uot
A C l), if l is the only literal in C whose negation is not assigned. A clause is a
tautology (taut C), if it contains both a literal and its negation.
    Correctness of a RUP step adding C to F is implied by the following lemmas:
(1) Let C be a non-tautological clause. Then, the initial assignment λl. −l∈C,
    which assigns the negated version of each literal in C, is consistent, and
    F ∧ ¬C is satisﬁable iﬀ F is satisﬁable w.r.t. the initial assignment:
   ¬taut C =⇒ consistent (λl. −l∈C) ∧ sat (F ∧ ¬ C) = sat wrt F (λl. −l∈C)

(2) If the formula contains a unit or true clause, assigning its literal preserves
    consistency and does not change satisﬁability:
   consistent A ∧ C∈F ∧ is uot A C l
     =⇒ consistent (A(l := True)) ∧ sat wrt F A = sat wrt F (A(l := True))
(3) If the formula contains a conﬂict clause, it is unsatisﬁable:
   consistent A ∧ C∈F ∧ conflict A C =⇒ ¬sat wrt F A
      Note that the learned clause cannot be a tautology. While adding tautolo-
      gies trivially preserves satisﬁability, they yield an inconsistent initial assign-
      ment. Instead of spending computation time to detect tautologies, we let
      our checker run with the inconsistent assignment: should it succeed, we add
      the clause, which is safe.

      We formalize the abstract checker as a transition system over the state:
 checker state ≡ CNF formula | CLS formula clause pan
  | PRF formula clause pan | PDN formula clause | UNSAT | FAIL
The transition relation → is the least relation that satisﬁes the following rules:
 (del clauses) F ⊆ F =⇒ CNF F → CNF F
 (start clause) CNF F → CLS F {} (λ . False)
 (add lit)      CLS F C A → CLS F ({l} ∪ C) (A(−l:=True))
 (start proof) CLS F C A → PRF F C A
 (add unit)     uC∈F ∧ is uot A uC ul
                =⇒ PRF F C A → PRF F C (A(ul:=True))
                             Fast and Veriﬁed UNSAT Certiﬁcate Checking        445

    (add conflict) uC∈F ∧ conflict A uC =⇒ PRF F C A → PDN F C
    (finish proof) C={} =⇒ PDN F C → CNF ({C} ∪ F)
    (finish proof unsat) PDN F {} → UNSAT
    (to fail)      s → FAIL
The checker starts in state CNF F, with some formula F . To delete clauses
(del clauses), they are removed from F . A clause addition is split into mul-
tiple smaller steps: First, we initiate adding a clause by going to state CLS
(start clause). We also maintain a partial assignment, starting with the empty
assignment λ . False. We then add the literals of the clause, one by one (add lit).
For each added literal l, we assign the negated literal −l. When all literals have
been added, we start the proof (start proof) going to state PRF. During the
proof, we add unit clauses, assigning the unit literal (add unit). When we have
added enough unit clauses, we add a conﬂict clause (add conflict), going to state
PDN (proof done). From there, we either go to state UNSAT if we have proved
the empty clause (finish proof unsat), or back to state CNF with the new clause
added to the formula (finish proof). We can always go to FAIL (to fail), indi-
cating that the proof failed.
    With the above Lemmas 1–3, some bookkeeping that add lit steps construct
the correct initial assignment, and a special case for tautologies, we prove:
Theorem 1 (Soundness of Abstract Checker). If the abstract checker can
reach UNSAT from the initial state CNF F, then the formula F is unsatisfiable:
CNF F →∗ UNSAT =⇒ ¬sat F
Note that we do not yet model clause identiﬁers on this level. They will be
introduced in a later reﬁnement step.

4     Implementation
We have speciﬁed a grammar to relate strings in DIMACS format to formulas, a
semantics to deﬁne satisﬁability of formulas, and an abstract certiﬁcate checker.
We now reﬁne these to the actual implementation of a certiﬁcate checker.
    We use the Isabelle Reﬁnement Framework [24], which supports reﬁnement in
multiple steps and in a modular fashion. Each step focuses on a diﬀerent aspect of
the algorithm, thus structuring the correctness proof, and making it manageable
in the ﬁrst place. In this section, we ﬁrst describe the data structures that we
use in our implementation, to represent abstract concepts such as literals and
clauses (cf. Sect. 2.1). We then describe how we implement the abstract checker
algorithm (cd. Sect. 3.1), using these data structures. Finally, we describe how
we integrate the checker with the parser, to obtain the actual veriﬁed tool.

4.1    Basic Concepts and Data Structures
We use data structures such as arrays, dynamic arrays, and array lists from
Isabelle LLVM’s library [22]. For technical reasons, sizes and counters are imple-
mented as non-negative signed 64-bit integers, or, equivalently, as unsigned 64-
bit integers less than 263 . Formally, refinement relations between concrete and
446     P. Lammich

abstract types are used. For example, size rel :: (64 word × nat) set relates
non-negative 64-bit signed integers to natural numbers. Similarly, Booleans are
implemented by 1-bit words, via the relation bool1 rel :: (1 word × bool) set.
    Clause identiﬁers are modelled as 64-bit unsigned integers less than 263 − 1,
via the relation cid rel :: (64 word × nat) set. This bound allows us to use clause
identiﬁers as indexes into an array whose length is represented by a size.
    Literals are ﬁrst reﬁned to natural numbers via nlit rel :: (nat × lit) set,
where a number n > 1 represents the variable n/2, and the literal is negative iﬀ
n is odd. The natural numbers are further reﬁned to unsigned 32-bit integers, via
u32 rel :: (32 word × nat) set. When we compose the two reﬁnement relations,
we get a relation between 32-bit integers and literals: ulit rel ≡ u32 rel O nlit rel.
Using 0 for None, we can also reﬁne optional literals to 32-bit integers via the
relation ulito rel :: (32 word × lit option) set. For each operation on the abstract
data type, we deﬁne a corresponding operation on the concrete data type. For
example, we deﬁne:
 nlit neg :: nat ⇒ nat   nlit neg n ≡ if even n then n+1 else n−1
 ulit neg :: 32 word ⇒ 32 word ulit neg w ≡ w XOR 1
We show that the concrete operations reﬁne their abstract counterparts:
 ulit neg, nlit neg :: u32 rel → u32 rel        nlit neg, (−) :: nlit rel → nlit rel
Here, f,g :: R1 → R2 is a shorthand notation for ∀(x,y)∈R1 . (f x, g y) ∈ R2 .
Combining these reﬁnement theorems yields ulit neg, (−) :: ulit rel → ulit rel.
    Clauses are implemented as zero-terminated arrays of 32-bit words, via the
relation zcl assn :: 32 word ptr ⇒ clause ⇒ assn. As arrays are stored on the
heap, this relation is expressed as separation logic assertion (assn). By conven-
tion, pure reﬁnement relations have the suﬃx rel, while those that use the heap
have the suﬃx assn.
    A clause database cdb ≡ nat ⇒ clause option is a partial function from
clause identiﬁers to clauses. It is implemented by a dynamic array of pointers to
clauses cdbi ≡ 32 word ptr larray, via cdb assn :: cdbi ⇒ cdb ⇒ assn. The array
is indexed by the clause identiﬁer. For clause identiﬁers not in the database,
the array contains a null pointer. Consider the abstract operation cdb ins cid C
db that inserts a clause C with identiﬁer cid into the database db, its concrete
version cdb ins impl, and the corresponding reﬁnement theorem:
cdb ins                :: nat    ⇒ clause      ⇒ cdb       ⇒ cdb
cdb ins impl          :: 64 word ⇒ 32 word ptr ⇒ cdbi      ⇒ cdbi
cdb ins impl, cdb ins :: cid rel → zcl assnd   → cdb assnd → cdb assn
The concrete operation destructively updates the array, thus the abstract cdb
parameter does no longer correspond to any concrete value. Also, the ownership
of the inserted clause is transferred into the clause database, thus the abstract
clause parameter does no longer correspond to any (visible) concrete value. We
call those parameters destroyed, indicated by a d in the reﬁnement theorem [21].
                                Fast and Veriﬁed UNSAT Certiﬁcate Checking           447

4.2     Data Structures with Capacity Bounds
Several data structures in our checker use counters. For example, during parsing,
the literals of a clause are collected in an array list, which uses a counter for its
size. We prove non-overﬂow of these counters from the bounded size of the CNF
ﬁle, and a limit on how many literals we can read from the certiﬁcate before the
checker rejects it2 . While we elide the details, we note that some abstract data
structures have a capacity bound ﬁeld. This is a ghost field, i.e., it is not present
in the implementation.
     The clause builder uses a dynamic array to store the literals of the clause
that is currently parsed, and also keeps track of the maximum literal encoun-
tered so far. Its abstract type is cbld ≡ nat × lit list × nat. A clause builder
(ml,ls,bnd) :: cbld consists of the maximum encountered literal ml, the current
list of literals ls, and a (ghost) bound bnd that limits the length of ls. We deﬁne
a data type invariant cbld inv :: cbld ⇒ bool that characterizes valid clause
builders (i.e., the bound and maximum literal are consistent with the list of lit-
erals). The relation cbld assn :: (32 word × 32 word array list) ⇒ cbld ⇒ assn
 implements clause builders.
     A partial assignment (cf. Sect. 3.1) is implemented by an array of bits indexed
by the literals, as well as an array list that contains all set literals. This array list
allows for eﬃciently resetting the assignment in between proof steps. We use the
type rpani :: 1 word larray × 32 word array list for the implementation, and
rpan :: bool list × nat list × nat for the functional representation, related by
rpan assn :: rpani ⇒ rpan ⇒ assn. The last ﬁeld of rpan is a (ghost) capacity
bound. The type rpan comes with an invariant rpan inv, and an abstraction
function rpan α :: rpan ⇒ pan to the encoded partial assignment.

4.3     Proof Checker Implementation
We implement the abstract checker state (Sect. 3.1) by the following types:
    cs op ≡ bool × bool × cdb × cbld × rpan         — outside proof (CNF, UNSAT)
    cs bc ≡ bool × rpan × cbld × cdb                          — build clause (CLS)
    cs ip ≡ bool × bool × rpan × cbld × cdb            — inside proof (PRF, PDN)
All data structures start with an error ﬂag, which indicates a failed proof
(abstract state FAIL). Outside a proof, i.e., in abstract states CNF and UNSAT,
the checker state is represented by a tuple (err,unsat,db,bld,A) :: cs op, where
unsat indicates that the formula has been proved unsatisﬁable and db is the
clause database holding the formula. The builder state bld and assignment A
are unused here, but threaded through such that they can be reused when the
next proof begins. When building a clause (abstract state CLS), the state is rep-
resented as (err,A,bld,db) :: cs bc. Finally, inside a proof (abstract states PRF
and PDN), the state is (err,confl,A,bld,db) :: cs ip. Here, confl indicates that a
conﬂict clause has been found.
2
    The size of the formula plus the number of literals in the certiﬁcate cannot exceed
    263 . We don’t expect this limit to be ever hit in practice.
448     P. Lammich

    We deﬁne invariants cs op inv, cs bc inv, cs ip inv; and abstraction func-
tions cs op α, cs bc α, cs ip α to the abstract checker state. We then show
that the functions on the concrete states preserve the invariants and implement
the transition relation →∗ on the corresponding abstract states. For example,
the following function handles a proof step, adding a unit or a conﬂict clause:
 cs prf step :: nat ⇒ cs ip ⇒ cs ip nres
 cs ip inv cap cs ∧ cap>0
  =⇒ cs prf step cid cs ≤ spec cs. cs ip inv (cap−1) cs
        ∧ (cs ip α cs) →∗ (cs ip α cs)
Here, ’a nres is the Isabelle Reﬁnement Framework’s type of programs that
return a result of type ’a, and P =⇒ c ≤ spec r. Q r is a Hoare-triple with
pre- condition P, program c, and postcondition Q [24]. That is, if the concrete
checker state cs has some capacity left, then the cs prf step function preserves
the invariant cs ip inv and implements the abstract transition relation →. The
available capacity of the checker state decreases by one.
                                                            The implementation of
                                                        cs prf step uses a function
                                                        to check if a clause is unit,
                                                        true, or a conﬂict. It is
                                                        displayed in Fig. 2. It ﬁrst
                                                        checks (l. 3) if the clause
                                                        identiﬁer is valid, and looks
                                                        it up in the database (l. 4).
                                                        Then (l. 6), it loops over
                                                        the literals of the clause,
                                                        maintaining a state consist-
                                                        ing of an optional literal
Fig. 2. Function to check if a clause is unit, true, or and an error ﬂag (ul,err).
conﬂict.                                                Initially (l. 11), the state
                                                        is (None,False). The loop
assigns to ul the ﬁrst literal that is not false (l. 9). If a second non-false lit-
eral is encountered, the error ﬂag is set (l. 10). The function returns the state
after the loop, or (None,True) if the clause was invalid (l. 12). Note that we
assume (l. 5) a ﬁnite clause. On the abstract level, we can use this to justify
termination of the loop. When implementing the function, we have to prove
ﬁniteness, which is trivial, as the clause is stored in an array. Dually, we assert
(l. 7) that the literals of the clause are in bounds of the assignment. This has
to be proved on the abstract level. When implementing, we can use it to justify
that the array access for looking up the literal is in bounds. This way, assertions
and assumptions are used to pass proof obligations up and down the reﬁnement
chain, proving them at the most convenient abstraction level.
    The loop in check uot is the innermost loop of the checker, and special care
has been taken to optimize it: while an actual certiﬁcate always contains unit
clauses, we also allow clauses with one true literal (cf. is uot in Sect. 3.1). This
avoids indexing both A(l) and A(−l) to distinguish between the two cases.
                               Fast and Veriﬁed UNSAT Certiﬁcate Checking         449

      The correctness theorem for check uot is as follows:
 rpan inv A ∧ cdb cid = Some C ∧ cdb vars cdb ⊆ rpan dom A =⇒
 check uot cdb cid A ≤ spec (ul,err). ¬ err −→ case ul of
   Some l ⇒ is uot (rpan α A) C l | None ⇒ conflict (rpan α A) C
I.e., if the partial assignment satisﬁes its invariant, the clause identiﬁer identiﬁes
clause C, and the clause database contains only variables within the bounds of
the partial assignment, then the function will either return an error, or some
literal l such that C is unit or true w.r.t. l, or None and C is a conﬂict clause.


4.4     A Verified DIMACS Parser

We present the parsing function’s signature and correctness theorem. Its imple-
mentation is elided due to page limit constraints:
 read dimacs cs :: 8 word list ⇒ (cs op × nat) nres
 read dimacs cs str ≤ spec (cs,cap). ∃ F. cs op inv cap cs
      ∧ (cs op α cs = FAIL ∨ (str,F) ∈ g dimacs ∧ cs op α cs = CNF F)
This function parses a string, and returns a checker state. On a parsing error, the
checker state corresponds to the abstract state FAIL. Otherwise, it corresponds
to CNF F for the formula F parsed from the string. The function also returns
the capacity left for the certiﬁcate after parsing the formula.


4.5     Assembling the Whole Program

Having implemented functions for the proof steps, we combine them with a parser
(details elided) for LRAT proofs, resulting in a function that reads an LRAT
proof from a buﬀered reader (brd rs), performs the corresponding transitions on
the proof state, and ﬁnally checks if the proof state has reached UNSAT:
 main checker loop :: cs op ⇒ brd rs ⇒ (bool × brd rs) nres
    The certiﬁcate checker,
displayed in Fig. 3, combines
the main checker loop with
the DIMACS parser. It takes
a string cnf, parses it as
formula (l. 3), initializes a
buﬀered reader for the cer-
tiﬁcate stream (l. 5), and
runs the main checker loop
with that reader (l. 6). From              Fig. 3. The checker program.
the correctness of the parser
(Sect. 4.4), the fact that all proof steps in main checker loop implement the
abstract checker, and the fact that the abstract checker is sound (Theorem 1),
we prove:
450     P. Lammich

Theorem 2 (Soundness of Functional Checker). If read check lrat cnf
returns true, then cnf is a valid representation of an unsatisfiable formula:
 read check lrat cnf ≤ spec r. r =⇒ ∃F. (cnf, F) ∈ g dimacs ∧ ¬ sat F


4.6   Refinement to LLVM Code
In Sect. 4.1 and Sect. 4.2 we have indicated how we implement the basic data
structures of our checker. Then, we have mostly presented functional code. Given
implementations of the data structures, reﬁning this functional code to impera-
tive code is mostly straightforward. Actually, much of this process can be auto-
mated by the Sepref tool [22], which we use to generate implementations for each
data structure and algorithm. For example, for the function check uot (cf. Sect.
4.3):
 sepref def check uot impl is
  check uot :: rpan assn → cdb assn → cid rel → ulito rel × bool1 rel
  unfolding check uot def by sepref
This generates the function check uot impl and proves the reﬁnement theorem:

 check uot impl, check uot
  :: rpan assn → cdb assn → cid rel → ulito rel × bool1 rel
To read the certiﬁcate, we use an external C function based on fread:
 size t fread from certificate(void ∗p, size t n) {
   if (!cert file) return 0;
   return fread(p,1,n,cert file); }
Inside Isabelle, this function is speciﬁed by:
htriple (arr assn xsi xs  size rel ni n  n ≤ length xs)
  fread from certificate xsi ni
  (λri. ∃r ys. size rel ri r  arr assn xsi ys 
       r≤n  length ys = length xs  drop r ys = drop r xs)
Where htriple is the Hoare triple for LLVM programs and  is the separating
conjunction. This matches the speciﬁcation of POSIX’s fread function [30],
except that we do not specify what data is read. This is sound, as it is a valid
over-approximation of the actual behaviour.


4.7   Soundness Theorem

Finally, we generate an implementation of read check lrat (Sect. 4.5), obtaining:

read check lrat impl :: 8 word ptr × 64 word ⇒ 1 word llM
read check lrat impl, read check lrat :: inp assn → bool1 rel
                               Fast and Veriﬁed UNSAT Certiﬁcate Checking       451

Here, inp assn implements the input string by an array and its length. In order
to smoothly interface this function from C/C++, we eliminate the tuple type
and return a byte instead of a bit. We deﬁne:
    lrat checker :: 8 word ptr ⇒ 64 word ⇒ 8 word llM
    lrat checker p n ≡
      if read check lrat impl (p,n) then return 1 else return 0
Isabelle LLVM’s code generator creates LLVM code, and a matching header ﬁle:

    export llvm lrat checker is uint8 t lrat checker(uint8 t ∗, int64 t)
     file ../code/lrat checker export.{ll,h}
We link this with a small C program that reads the command line, memory-maps
the formula ﬁle, provides the function fread from certificate (cf. Sect. 4.6), calls
the veriﬁed checker, and prints the result.
   Chaining together the correctness of the functional checker (Theorem 2) and
the reﬁnement theorem for read check lrat, and unfolding some deﬁnitions yields:


Theorem 3 (Soundness of Implementation). When we pass the checker a
pointer cp to an array of size cszi holding the bytes c, then the checker will
terminate with the array being unchanged, and if the result is not zero, the bytes
c in the array are a syntactically correct encoding of an unsatisfiable CNF:
    htriple (arr assn cp c  size rel cszi csz  csz=length c)
      (lrat checker cp cszi)
      (λr. arr assn cp c  (r=0 =⇒ (∃F. (c,F)∈g dimacs ∧ ¬sat F)))

Note that this theorem does not depend on any complex data structures or
reﬁnements. Apart from the basic notions of Hoare triples, separation logic,
machine words, and pointers to arrays, it only depends on our semantics of
formulas (Sect. 2.1), and our grammar for the DIMACS format (Sect. 2.2).


5     Benchmarks

For our benchmarks, we have used the latest stable versions of the tools avail-
able at the time of writing: CaDiCaL 1.9.4 [7], lrat-trim 0.2.0 [27], cake lpr
7a207e9 [8], gratchk dc6dd9d [15], lrat-check 9ee016c [12], and lrat-acl2 (incre-
mental) 8.5 [1] on gcl 2.6.13pre [13]. We used an AMD Ryzen 9 7950X3D machine
with 128 GB DDR5 RAM and a 2.0 TB Samsung 990 Pro SSD disk.
   We have used problems from the 2022 SAT competition3 [33]: out of the 156
problems proved unsatisﬁable in the main track, CaDiCaL timed out on 5 after
5000 s. The remaining 151 problems form our benchmark set.
3
    We did not choose the 2023 competition, because the problems there are biased
    towards checkers that use techniques not available for direct LRAT generation in
    CaDiCaL.
452     P. Lammich

    First, we let the checker
                               Checker n tc /ts ls lc mc /ms w/wf w/wb
run in parallel to CaD-
iCaL, streaming the cer- Our tool 151 6% 97% 5% 80%                    102% 110%
tiﬁcate directly into the      cake  lpr 138  61%   85% 47%   162×     130% 143%
checker. We used our checker
and cake lpr4 . We measure Table 1. Benchmark results in streaming mode. The
the computing times (the table displays the averages over the successfully certi-
                               ﬁed problems (n).
sum of user and system
time) that were allocated to the sat solver (ts ) and checker (tc ). The ratio tc /ts
indicates how the work is distributed between solver and checker. The smaller
this ratio, the less time the checker needs in comparison to the solver. Next,
we measure the average CPU loads allocated to the solver (ls ) and checker (lc ).
A solver load less than 100% indicates that the solver was slowed down. The
less load the checker produces, the fewer additional computing power is needed
for checking. We also measure the peak memory consumption (maximum resi-
dent set size) of the solver (ms ) and checker (mc ). The ratio mc /ms indicates
the additional memory required for checking. Finally, we measure the wall-clock
time until certiﬁcation ﬁnishes (w), and compare that to the time required by
the solver to solve the problem and write the certiﬁcate to a ﬁle (wf ), and to the
solving time without producing a certiﬁcate at all (wb ). The ratios w/wf and
w/wb indicate the observed extra time required for certiﬁcation. The results are
displayed in Table 1: Our checker veriﬁed all problems, adding about 6% more
computation time and 80% more memory on top of solving and certiﬁcate pro-
ducing. It does not signiﬁcantly slow down the solver, which runs at 97% CPU
load. Compared to writing the certiﬁcate to a ﬁle, streaming it directly to the
checker is 2% slower, and the overhead added by the whole certiﬁcation process
is 10%. The cake lpr checker failed to certify 13 problems5 . For the remaining
problems, it added 61% of computation time, and the solver only ran at 85% load.
Streaming the certiﬁcate to cake lpr is 30% slower than writing the certiﬁcate
to a ﬁle, and 43% slower than solving without producing a certiﬁcate. Moreover,
for each cake lpr run, maximum heap and stack sizes have to be determined
upfront, and cake lpr is likely to use all available heap6 . Without prior knowl-
edge of the problem, it is impossible to guess good sizes. For our experiments,
we used 8 GiB stack and 16 GiB heap, based on the maximum of 11 GiB that
our tool needed. With this, cake lpr ran out of memory for six problems, and
maxed out at around 16 GiB memory usage for most of the remaining problems
(131/138). On average, it needed 162 times more memory than the solver.

4
  We didn’t include a Coq based lrat-checker [9], nor an ACL2 based one [16]: the
  former is reportedly less eﬃcient than cake lpr [35], and the latter supports, to the
  best of our knowledge, no streaming of the certiﬁcate.
5
  6 memouts, 6 parsing errors, most likely due to benchmarks incompatible with
  CakeLPR’s strict interpretation of the DIMACS CNF format, and one timeout at
  5000 s.
6
  We assume that the garbage collector only becomes active when available memory
  has ﬁlled up.
                             Fast and Veriﬁed UNSAT Certiﬁcate Checking        453


Checker n ttot      tavg mavg                To measure the performance of just
lrat-trim 151 116% 118% 96%              the checker, we ran it on certiﬁ-
lrat-check 150 357% 384% 116%            cates stored in ﬁles. For this experi-
gratchk 147 917% 994% 80×                ment we also included the gratchk tool,
cake lpr 138 1666% 1797% 208×            which is reported to be faster than
lrat-acl2 57 105× 8200% 158×             cake lpr [35], the lrat-acl2 tool, and the
                                         unveriﬁed checker implementations lrat-
                                         trim (forward) and lrat-check, to com-
Table 2. Benchmark results in ﬁle
mode.                                    pare our veriﬁed tool against unveriﬁed
                                         but highly optimized implementations.
For the garbage collected tools (gratchk, cake lpr, lrat-acl2), we set a heap limit
of 16GiB. If possible, we used binary LRAT encoding (our tool and lrat-trim),
and did not include conversion time from LRAT to GRAT (gratchk). Using our
tool as baseline (100%), we display the ratio of the total computation times over
all problems (ttot ), and the average ratios of computation time and peak memory
usage per problem (tavg and mavg ). The results are displayed in Table 2: our tool
is slightly faster but uses slightly more memory than lrat-trim. It is signiﬁcantly
faster and uses less memory than any other veriﬁed or unveriﬁed tool we tested.
After 14:30h, lrat-acl2 had processed 66 problems and succeeded on 57. The
same problems took 3:25m to check by our tool. We aborted the experiment at
that point, as, by extrapolation, it would have taken 5 more days to complete.


6   Conclusion

We have used the Isabelle LLVM framework to formally verify soundness of
an unsatisﬁability certiﬁcate checker. Our checker is veriﬁed w.r.t. a grammar
of the DIMACS format, a semantics of CNF, and down to the LLVM code
that implements the checker. Completeness of the checker has been empirically
veriﬁed by showing that it accepts a large set of benchmarks. Our checker accepts
the LRUP fragment of the LRAT format, which makes it suitable for checking
certiﬁcates from many top-performing SAT solvers. For solvers that support
streaming of LRAT certiﬁcates, our tool can be run in parallel to the solver,
eliminating the need to store the potentially large certiﬁcate, and coming back
with the certiﬁcation result the moment the solver is ﬁnished. For CaDiCaL, this
is only 10% slower than running just the solver, and 2% slower than writing the
certiﬁcate to a ﬁle without checking it. Our implementation is slightly faster and
uses only 4% more memory than the unveriﬁed and highly optimized lrat-trim
checker. It is signiﬁcantly faster and more memory eﬃcient than any other LRAT
checker we know of, veriﬁed or unveriﬁed. This makes it possible to routinely
run the checker with the solver, increasing the conﬁdence at low cost.
    To design our checker, we ﬁrst implemented and proﬁled prototypes in C++
to determine the important optimizations. This took roughly 40 person hours.
We then used the Isabelle Reﬁnement Framework to produce a veriﬁed version of
the checker. This was done in a top-down reﬁnement process, which was guided
by the experience from the unveriﬁed prototypes. This took another 200 h.
454     P. Lammich

6.1   Related Work
The closest work to ours is the veriﬁed cake lpr checker [34,35]. It supports
streaming certiﬁcates7 and the full LPR format. The cake lpr checker is veriﬁed
down to assembly code (with a thin C wrapper around it), while our checker is
veriﬁed down to LLVM intermediate code. While verifying an LLVM compiler
is orthogonal to this project, we would immediately proﬁt from such a veriﬁed
compiler, further reducing our trusted code base. Moreover, our checker is veriﬁed
w.r.t. a grammar of DIMACS CNF, while cake-lpr’s parser is not veriﬁed. It only
comes with a sanity check, showing that the parser is left inverse to a pretty
printer. Our checker is signiﬁcantly faster than cake lpr, and only allocates as
much memory as needed, while cake-lpr’s memory size has to be set upfront,
making it uncontrollable without background information about the problem. In
particular in streaming mode, such information is not available. Finally, cake lpr
uses the ASCII encoding of LRAT, while our checker uses the more compact
binary encoding.8
    There are other veriﬁed certiﬁcate checkers [5,9,16,23], which, however, do
not support streaming or are signiﬁcantly slower than cake lpr.

6.2   Future Work
There are no principle problems to extend our tool to the more powerful LRAT
and LPR formats. We leave this to future work, as we are not aware of any solver
that would support streaming these formats.
    While our parser was manually implemented and then veriﬁed, there is work
on veriﬁed parser generators [6,18–20,25,31]. We leave it to future work to inte-
grate similar techniques into the Isabelle LLVM workﬂow.
    While faster than parsing the ASCII encoding, decompression of the binary
encoding is a hot-spot in our checker. In streaming mode, we could probably use
a less compact but faster to read format, which we leave to future work.

References
 1. ACL2 github repository. https://github.com/acl2/acl2
 2. Baek, S., Carneiro, M., Heule, M.J.H.: A ﬂexible proof format for SAT solver-
    elaborator communication. In: TACAS 2021. LNCS, vol. 12651, pp. 59–75.
    Springer, Cham (2021). https://doi.org/10.1007/978-3-030-72016-2_4
 3. Beeren, J., et al.: Finite machine word library. Archive of Formal Proofs, June
    2016. https://isa-afp.org/entries/Word_Lib.html. Formal proof development
 4. Bogaerts, B., Gocht, S., McCreesh, C., Nordström, J.: Certiﬁed symmetry and
    dominance breaking for combinatorial optimisation. J. Artif. Intell. Res. 77, 1539–
    1589 (2023). Preliminary version in AAAI 2022
7
  Surprisingly, we have not found reports on using cake lpr in streaming mode. In
  particular, Pollit et. al. [29] did not consider this possibility when they extended
  CaDiCaL to directly produce LRUP certiﬁcates.
8
  Conversion between the encodings is easy, and we leave native support of the ASCII
  encoding in our checker to future work.
                               Fast and Veriﬁed UNSAT Certiﬁcate Checking            455

 5. Bogaerts, B., McCreesh, C., Myreen, M.O., Nordström, J., Oertel, A., Tan, Y.K.:
    VeriPB and CakePB in the SAT competition 2023. In: Balyo, T., Heule, M., Iser,
    M., Järvisalo, M., Suda, M. (eds.) Proceedings of SAT Competition 2023: Solver,
    Benchmark and Proof Checker Descriptions. Department of Computer Science
    Series of Publications B, Department of Computer Science, University of Helsinki,
    Finland (2023)
 6. Bortin, M.: A formalisation of the Cocke-Younger-Kasami algorithm. Archive of
    Formal Proofs, April 2016. https://isa-afp.org/entries/CYK.html. Formal proof
    development
 7. CaDiCaL github repository. https://github.com/arminbiere/cadical/releases/tag/
    rel-1.9.4
 8. cake lpr github repository. https://github.com/tanyongkiam/cake_lpr
 9. Cruz-Filipe, L., Heule, M.J.H., Hunt, W.A., Kaufmann, M., Schneider-Kamp, P.:
    Eﬃcient certiﬁed RAT veriﬁcation. In: de Moura, L. (ed.) CADE 2017. LNCS
    (LNAI), vol. 10395, pp. 220–236. Springer, Cham (2017). https://doi.org/10.1007/
    978-3-319-63046-5_14
10. Cruz-Filipe, L., Marques-Silva, J., Schneider-Kamp, P.: Eﬃcient certiﬁed resolu-
    tion proof checking. In: Legay, A., Margaria, T. (eds.) TACAS 2017. LNCS, vol.
    10205, pp. 118–135. Springer, Heidelberg (2017). https://doi.org/10.1007/978-3-
    662-54577-5_7
11. Dawson, J.: Isabelle theories for machine words. Electron. Notes Theoret.
    Comput. Sci. 250(1), 55–70 (2009). https://doi.org/10.1016/j.entcs.2009.08.005,
    https://www.sciencedirect.com/science/article/pii/S1571066109003302. Proceed-
    ings of the Seventh International Workshop on Automated Veriﬁcation of Critical
    Systems (AVoCS 2007)
12. DRAT-trim github repository. https://github.com/marijnheule/drat-trim
13. GNU common lisp. git://git.sv.gnu.org/gcl.git
14. Gelder, A.V.: Verifying RUP proofs of propositional unsatisﬁability. In:
    International Symposium on Artiﬁcial Intelligence and Mathematics,
    ISAIM 2008, Fort Lauderdale, Florida, USA, 2–4 January 2008 (2008).
    http://isaim2008.unl.edu/PAPERS/TechnicalProgram/ISAIM2008_0008_
    60a1f9b2fd607a61ec9e0feac3f438f8.pdf
15. gratchk github repository. https://github.com/IsaFoL/IsaFoL/tree/master/
    GRAT/gratchk
16. Heule, M., Hunt, W., Kaufmann, M., Wetzler, N.: Eﬃcient, veriﬁed checking of
    propositional proofs. In: Ayala-Rincón, M., Muñoz, C.A. (eds.) ITP 2017. LNCS,
    vol. 10499, pp. 269–284. Springer, Cham (2017). https://doi.org/10.1007/978-3-
    319-66107-0_18
17. Heule, M., Hunt, W., Wetzler, N.: Trimming while checking clausal proofs. In:
    2013 Formal Methods in Computer-Aided Design, FMCAD 2013, pp. 181–188.
    IEEE (2013)
18. Jia, X., Kumar, A., Tan, G.: A derivative-based parser generator for visibly push-
    down grammars. Proc. ACM Program. Lang. 5(OOPSLA), 1–24 (2021). https://
    doi.org/10.1145/3485528
19. Jourdan, J.-H., Pottier, F., Leroy, X.: Validating LR(1) parsers. In: Seidl, H. (ed.)
    ESOP 2012. LNCS, vol. 7211, pp. 397–416. Springer, Heidelberg (2012). https://
    doi.org/10.1007/978-3-642-28869-2_20
20. Koprowski, A., Binsztok, H.: TRX: a formally veriﬁed parser interpreter. In: Gor-
    don, A.D. (ed.) ESOP 2010. LNCS, vol. 6012, pp. 345–365. Springer, Heidelberg
    (2010). https://doi.org/10.1007/978-3-642-11957-6_19
456     P. Lammich

21. Lammich, P.: Reﬁnement to Imperative/HOL. In: ITP, LNCS, vol. 9236, pp. 253–
    269. Springer, Cham (2015)
22. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In: Harrison, J.,
    O’Leary, J., Tolmach, A. (eds.) 10th International Conference on Interactive Theo-
    rem Proving, ITP 2019, 9–12 September 2019, Portland, OR, USA. LIPIcs, vol. 141,
    pp. 22:1–22:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2019). https://
    doi.org/10.4230/LIPIcs.ITP.2019.22
23. Lammich, P.: Eﬃcient veriﬁed (UN)SAT certiﬁcate checking. J. Autom. Reason.
    64(3), 513–532 (2020). https://doi.org/10.1007/s10817-019-09525-z
24. Lammich, P., Tuerk, T.: Applying data reﬁnement for Monadic programs to
    Hopcroft’s algorithm. In: Beringer, L., Felty, A. (eds.) ITP 2012. LNCS, vol.
    7406, pp. 166–182. Springer, Heidelberg (2012). https://doi.org/10.1007/978-3-
    642-32347-8_12
25. Lasser, S., Casinghino, C., Fisher, K., Roux, C.: Costar: a veriﬁed all(*) parser. In:
    Proceedings of the 42nd ACM SIGPLAN International Conference on Program-
    ming Language Design and Implementation, pp. 420-434. PLDI 2021. Association
    for Computing Machinery, New York, NY, USA (2021). https://doi.org/10.1145/
    3453483.3454053
26. Lattner, C., Adve, V.: LLVM: a compilation framework for lifelong program analy-
    sis & transformation. In: International Symposium on Code Generation and Opti-
    mization, 2004, CGO 2004, pp. 75–86 (2004). https://doi.org/10.1109/CGO.2004.
    1281665
27. lrat-trim github repository. https://github.com/arminbiere/lrat-trim/releases/
    tag/rel-0.2.0
28. Moskewicz, M.W., Madigan, C.F., Zhao, Y., Zhang, L., Malik, S.: Chaﬀ: engineer-
    ing an eﬃcient SAT solver. In: Proceedings of DAC, pp. 530–535. ACM (2001)
29. Pollitt, F., Fleury, M., Biere, A.: Faster LRAT checking than solving with CaDi-
    CaL. In: Mahajan, M., Slivovsky, F. (eds.) 26th International Conference on Theory
    and Applications of Satisﬁability Testing, SAT 2023, 4–8 July 2023, Alghero, Italy.
    LIPIcs, vol. 271, pp. 21:1–21:12. Schloss Dagstuhl - Leibniz-Zentrum für Informatik
    (2023). https://doi.org/10.4230/LIPIcs.SAT.2023.21
30. The Open Group Base Speciﬁcations (2018). Issue 7 (IEEE Std 1003.1-2017)
31. Rau, M.: Earley parser. Archive of Formal Proofs, July 2023. https://isa-afp.org/
    entries/Earley_Parser.html. Formal proof development
32. SAT competition 2009—submission format (2009). http://www.satcompetition.
    org/2009/format-benchmarks2009.html
33. SAT competition (2022). https://satcompetition.github.io/2022/
34. Tan, Y.K., Heule, M.J.H., Myreen, M.O.: cake lpr: veriﬁed propagation redun-
    dancy checking in CakeML. In: Groote, J.F., Larsen, K.G. (eds.) Tools and Algo-
    rithms for the Construction and Analysis of Systems, pp. 223–241. Springer, Cham
    (2021)
35. Tan, Y.K., Heule, M.J., Myreen, M.O.: Veriﬁed propagation redundancy and com-
    positional UNSAT checking in CakeML. Int. J. Softw. Tools Technol. Transfer
    25(2), 167–184 (2023)
36. Wetzler, N., Heule, M.J.H., Hunt, W.A.: DRAT-trim: eﬃcient checking and trim-
    ming using expressive clausal proofs. In: Sinz, C., Egly, U. (eds.) SAT 2014. LNCS,
    vol. 8561, pp. 422–429. Springer, Cham (2014). https://doi.org/10.1007/978-3-319-
    09284-3_31
                              Fast and Veriﬁed UNSAT Certiﬁcate Checking          457

Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
