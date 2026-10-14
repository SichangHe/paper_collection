                                        Leroy and Blazy were right: their memory model
                                                soundness proof is automatable
                                                      (Extended Version)

                                                      Pedro Barroso, Mário Pereira, and António Ravara
                                                             1
                                                                 NOVA School of Science and Technology
arXiv:2212.02425v1 [cs.LO] 5 Dec 2022




                                                                     2
                                                                       NOVA-LINCS, Portugal



                                              Abstract. Xavier Leroy and Sandrine Blazy in 2007 conducted a formal
                                              verification, using the Coq proof assistant, of a memory model for low-
                                              level imperative languages such as C. Considering their formalization was
                                              performed essentially in first-order logic, one question left open by the au-
                                              thors was whether their proofs could be automated using a verification
                                              framework for first-order logic. We took the challenge and automated
                                              their formalization using Why3, significantly reducing the proof effort.
                                              We systematically followed the Coq proofs and realized that in many
                                              cases at around one third of the way Why3 was able to discharge all
                                              VCs. Furthermore, the proofs still requiring interactions (e.g. induction,
                                              witnesses for existential proofs, assertions) were factorized isolating aux-
                                              iliary results that we stated explicitly. In this way, we achieved an almost-
                                              automatic soundness and safety proof of the memory model. Nonethe-
                                              less, our development allows an extraction of a correct-by-construction
                                              concrete memory model, going thus further than the preliminary Why
                                              version of Leroy and Blazy.

                                              Keywords: C memory model · Formal proof · Theorem proving · Why3


                                        1   Introduction
                                        Formal semantics are concerned with the process of building a mathematical
                                        model to serve as a basis for understanding and reasoning about how programs
                                        behave. A mathematical model is important because the activity of trying to
                                        precisely define the behavior of program constructions can reveal all types of
                                        subtleties of which it is crucial to be aware [9]. Many programs that require for-
                                        mal verification are written in imperative languages that accommodate pointer-
                                        based data structures with in-place modifications. To reason about the contents
                                        of the memory or even the behavior of operations over it, one needs to develop
                                        an adequate memory model.
                                        Leroy and Blazy in 2007 formalized and verified, using the Coq proof assistant, a
                                        memory model for C-like imperative languages [4]. Coq proofs tend to be a very
                                        time consuming task and in fact, Leroy and Blazy’s proof was almost the length
                                        of the specification and theorems (970 and 1070 lines, respectively). Considering
2         P. Barroso, M. Pereira, A. Ravara

their formalization was performed essentially in first-order logic, one question
the authors addressed was whether their proofs could be automated using a
verification framework for first-order logic, e.g. Why3 [2]. The authors translated
their memory model to Why (a former version of Why3), the authors claim that
at the time some recursive definitions were hard to define in the Why syntax
and therefore, they only translated the axiomatizations and derived properties
of the memory model. Their preliminary study (Table 1) showed that could
be automated, but no further study or complete formalization of their memory
model has been automated so far.




                     Fig. 1. Leroy and Blazy’s Why formalization


Nonetheless, the problem we address here is:

       Is it possible (15 years later) to automate the complete abstract and
      concrete implementation of the authors memory model?

In this paper we translate Leroy and Blazy’s memory model to Why3 and de-
velop an almost-automatic soundness and safety proof. Moreover, our code, im-
plementing a concrete memory model, is extractable. This requires some manual
work, namely re-organizing modules, that we believe with some refactoring of
the WhyML code could be avoided.
     Concretely, our contributions are:

    – two Why3 versions (one containing interactive proofs and one “fully” auto-
      matic) that reduce up to 90% the Coq proof effort;
    – general techniques to achieve a more automatic proof;
    – a proof effort comparison between ours and the original Coq ones;
    – a correct-by-construction memory model extracted from our development.
The rest of the article is organized as follows. Section 2 describes memory mod-
els and briefly presents the one of Leroy and Blazy. Also, Section 2 shows how to
prove the memory model sound and safe (which includes semantics preservation
for three passes of the Compcert compiler), and the Coq proof statistics that
Leroy and Blazy stated in their paper. Section 3 outlines our Why3 development
and the techniques used to explicitly state interactive transformations. Section
4 compares both versions with the Coq version and presents our approach to ex-
tract correct-by-construction OCaml code, followed by conclusions in Section 6.
Our Why3 development and OCaml extracted code is publicly available3 .
3
    https://gitlab.com/p.barroso/memory-model-c-why3/
                                                Leroy and Blazy were right       3

2     The memory model
Memory models provide the necessary abstraction between the behavior of a
program and the behavior of the memory it reads and writes. When reasoning
about compilers and low-level code we need to account for several factors such
as memory management, concurrency behavior, casts, structured pointers, over-
lapping locations, etc. Therefore, it is not sufficient to interpret memory as a
assignment of values to locations.
2.1   Concept
The generic idea behind a memory model is to explicitly describe and provide
some guarantees on the behavior of certain operations that manipulate memory
(e.g. read, write, allocation, free). This allows to make concrete assumptions
about the “state of the memory” at any time of the execution of a program. One
example is that reading after writing a value into a location should return the
value that was previously stored. Figure 2 shows this simple scenario and the
natural assertions one can make over the execution of the program.




                 Fig. 2. Concrete assertion over a simple program


    There are several ways to define a memory model: as a description of the set
of valid traces of operations fulfilled by the execution of a program (e.g. IBM
POWER multiprocessors [5]); as an abstract machine that receives and replies to
messages (e.g. CompCertTSO [8]); and as a set of functions that can be invoked
along with some guarantees on their results (e.g. Leroy and Blazy’s memory
model [4]). Note that in most cases a definition in one of these styles is provably
equivalent to a definition in another style [6].
    The memory model presented by Leroy and Blazy is used in the formal
verification of the Compcert [3] compiler, which transforms the Clight subset
of the C programming language down to PowerPC assembly code.

2.2   Leroy and Blazy’s memory model
Leroy and Blazy start by giving an abstract, incomplete specification of a mem-
ory model to formalize the memory-related aspects of C and related languages.
The abstract type val represents values, which includes the constant vundef to
4        P. Barroso, M. Pereira, A. Ravara

describe an undefined value. To describe references to memory blocks they use
an abstract type block and to represent memory states an abstract type mem.

Memory definitions. A memory state is a collection of separated blocks where
each block behaves as an array of bytes, and is addressed using byte offsets i ∈ Z.
A memory location is a pair (b, i) of a block reference b and an offset i within
this block. Lastly, the constant empty : mem represents the initial memory state.

Operations. They define four operations that manipulate memory states as
total functions:
           alloc : mem × Z × Z → option(block × mem)
              free : mem × block → option mem
              load : memtype × mem × block × Z → option val
            store : memtype × mem × block × Z × val → option mem

All these functions return option types to take into account potential failures.
The function alloc(m,l,h) allocates a fresh memory block, where m is the initial
memory state, l ∈ Z is the lower bound of the block (inclusive), and h ∈ Z
the upper bound (exclusive) of the fresh block. Allocation can fail if not enough
memory is available. Otherwise, Some (b,m) is returned, where b is the reference
to the new block and m the updated memory state.
    Contrarily, free(m,b) deallocates block b in memory m. In case of success,
an updated memory state is returned.
    The function store(τ ,m,b,i,v) writes value v of type τ at offset i in block b
of m. If successful, the updated memory state is returned.
    Symmetrically, load(τ ,m,b,i) reads a data type of τ from block b of memory
state m at byte offset i. If successful, the value from block b is returned.

Axiomatization and additional properties. The authors axiomatize the
expected behavior of the operations.4 Recall that any implementation of the
model must satisfy all these properties.

Good and not so good variables (axioms S5 to S8). Define the correct behavior
(operation succeeds) of a load after an alloc, free or store operation. Con-
cretely, these hypotheses specify that: alloc and free preserve loads performed
in any other disjoint block; reading from the same location with a compatible
type τ 0 succeeds and returns the value convert(v,τ 0 ); and storing a value of
type τ 0 in block b at offset i commutes with loading. Furthermore, Leroy and
Blazy also specify when the load operation returns an undefined value.

Block validity (axioms S9 to S13). The correct behavior of a load after an alloc,
free or store depends on separation properties between blocks. In order to
capture such properties, Leroy and Blazy axiomatize the relation m |= b, which
means that block b is valid in memory m. A block is valid if it was previously
allocated and was not yet deallocated.
4
    The complete set of hypotheses can be consulted online.
                                                   Leroy and Blazy were right       5

Bounds of block (axioms S14 to S17). The authors also axiomatize the function
B(m, b) that associates low and high bounds to a block b in memory state m.
The axiomatization specifies that a freshly allocated block has the bounds that
were given as argument to the alloc function and the bounds of a block are
preserved by an alloc, store or free operation over a different block.
Valid access (axiom S18 and derived properties D19 to D22). Combining the
definitions of block validity and of bounds of a block, Leroy and Blazy define the
“valid access” relation m |= τ @ b, i, which means that in state m, the block
b is a valid block and the range of byte offsets being accessed is included in the
bounds of b. Intuitively, the store and load operations succeeds if and only if
the corresponding memory reference is valid.
Freshness property (properties P30 to P34). In Leroy and Blazy’s concrete mem-
ory model, alloc never reuses block identifiers. Therefore, they define the rela-
tion m # b stating that block b is fresh in memory m. This relation is mutually
exclusive with block validity.
Alloc determinism (property P35). Lastly, Leroy and Blazy state that alloc is
deterministic with respect to the domain of the current memory state, i.e. alloc
chooses the same free block when applied twice to memory states that have the
same domain, but may differ in block contents.

2.3    Compiler passes and their soundness proof
The axiomatization of the previous section specify precise handling of undefined
values, behavior of operations over memory states and “good-variable” proper-
ties. This theory is used to prove the correctness of program transformations
performed by three passes of the Compcert compiler. Our approach follows the
same process presented by Leroy and Blazy and, therefore, we also prove the
correctness of these transformations.
    To prove soundness and safety of each transformation, one need to guarantee
specific results between the memory operations performed by the original and
transformed program. For that, invariants are defined to describe the memory
states at every point of the execution of the original and transformed programs.
    Leroy and Blazy use four relations between memory states: memory embed-
dings; memory extensions; refinement of stored values; and memory injections.
For each of them, they define several properties the program needs to hold in
order to prove soundness and safety. We decided to omit the exact definitions,
as the list is exhaustive and falls out of the scope of this paper.5

2.4    Original Coq proof
Coq uses Gallina, a functional programming language. The close connection
between functional languages and mathematical definitions eases the implemen-
tation of mathematical theories. The Coq development of Leroy and Blazy is
5
    The authors did not presented a summarized list of properties for each of the four
    relations.
6       P. Barroso, M. Pereira, A. Ravara

very close to the definitions presented in their paper. In fact, most of the def-
initions in their paper were transcribed directly from their Coq development,
which has approximately 1070 lines of theorems and specifications, and 970 lines
of proof scripts.
    Coq does not grant much support for proof automation. Therefore, Leroy and
Blazy manually conducted most of the proofs. Yet, their proofs exhaustively use
the omega tactic, a procedure that automates reasoning about equations and
inequalities over the type nat of natural numbers. They also occasionally use
other tactics (e.g. eauto, congruence), which the authors say were useful.

3   Our approach in Why3

The formalization of Leroy and Blazy was conducted mostly in first-order logic:
the authors use functions as data, but only to implement finite maps, which
allows a first-order axiomatization. Henceforth, the definitions in Why3 are very
similar to the fragment from Gallina (Coq’s language). In fact, our development
is very similar to the specification and theorems of the Coq version.

Implementation. The Why version of Leroy and Blazy only contained the ax-
iomatization of the abstract memory model. Our Why3 development have the
axioms of the abstract memory model and additionally, the implementation of a
concrete memory model, which allows an extraction of a correct-by-construction
memory model. Our formalization have approximately 1040 lines of theorems
and specifications, roughly the same amount of the Coq version.

Proofs. The automatic theorem provers discharges automatically 114 from a to-
tal of 125 verification conditions using the auto level 3 tactic, which attempts
to apply recursively four transformations (split all full, introduce premises, in-
line goal and split vc) and calls the provers with a larger time and memory limit
(30 seconds and 4Gb of memory). Using the key 3 of the keyboard (shortcut for
the auto level 3 tactic) we automatically prove the equivalent of approximately
870 lines of proof scripts in Coq (89.6% of the total proof scripts lines). Appendix
A shows the corresponding proofs in Coq and Why3 of one lemma of the 114.
    For the remaining 9 verification conditions (VCs), we follow closely the Coq
proof script, applying transformations one by one and calling the solvers for
each transformation. Three of the VCs require simple induction; four case anal-
ysis before applying the induction hypothesis; one additional properties in the
context that we introduce with assertions and the last one a mix of induction,
case analysis, assertions and additionally proves an existential statement (Table
B1 summarizes the results). Yet, in all nine, the amount of transformations to
complete the proof were significantly less than the steps of the proof in Coq
(circa 117 transformations versus a total of 220).

General strategies to achieve a more automatic proof. The primary cons
of Why3 regarding proofs with manually conducted interactions are: it is hard
to have a concise global view of all transformations applied, especially on larger
                                                 Leroy and Blazy were right        7

proof trees; moreover after making change in the code, most of the times Why3
is not able to propagate the exact transformations through the correct proof
nodes, which quite often leads to losses of the whole proof session [1].
    To circumvent this, we present the following general techniques to explicitly
state the interactions required for the remaining 9 proofs as WhyML code. This
allows the reader to have the essence of the whole proof just by looking at the
source code. Bellow, we explain and illustrate the approaches namely in the
treatment of induction, assertions and existential properties. The remainder 9
proofs use these techniques. These techniques can be used as general recipes for
provers.

Induction. Why3 provides a way to define lemma functions, which are special
functions that serve not as actual code to execute but to prove the function’s
contract as a lemma. These are useful when proving properties by induction,
as any recursive call to the functions means an application of the induction
hypothesis. Lets consider the following lemma:
lemma set_cont_outside:
    forall n, f:(int → option (fset ’a, fset ’a)) , ofs i.

We prove the lemma by induction on n. Let us now convert our lemma to a
recursive lemma function. Recursive lemma functions are declared with the key-
words let rec lemma and its parameters are the universally quantified variables
in the normal lemma:
let rec lemma set_cont_outside (n: int)
        (f: (int → option (memtype, value))) (ofs i: int)

Now we give a contract to the lemma, where each premise is now a precondi-
tion (declared with the requires keyword) and the conclusion a postcondition
(declared with the ensures keyword). To guarantee the function terminates we
state a variant, in this case n itself, which is the argument we are applying
induction:
let rec lemma set_cont_outside (n: int)
        (f: (int → option (memtype, value))) (ofs i: int)
    requires { n ≥ 0 }
    requires { i < ofs ∨ i ≥ ofs + n }
    ensures { set_cont f ofs n i = f i }
    variant { n }

Finally, we construct the correct recursive call by looking at the definitions of the
functions within the postconditions. In this case we have the function set cont,
which definition is as follows:
let rec ghost function set_cont (f: int → content)
        (ofs: int) (n: int) : int → content
    requires { n ≥ 0 }
    variant { n }
= if n = 0 then f else set_cont (update ofs None f) (ofs + 1) (n-1)
8      P. Barroso, M. Pereira, A. Ravara

The recursive call of the lemma uses the same argument modifications of the
recursive call of set cont:
let rec lemma set_cont_outside (n: int)
        (f: (int → option (memtype, value))) (ofs i: int) ...
= if n > 0 then set_cont_outside (n-1) (update ofs None f) (ofs + 1) i

Why3 is now able to automatically generate a valid induction hypothesis and
prove the lemma. The technique can be used as a general recipe for provers.

Asserts. We introduce assertions in the body of let lemmas. For example in the
lemma store mapped emb, we assert that b1 is a valid pointer in memory state
m1 and b2 is a valid pointer in memory state m2:
let lemma store_mapped_emb
    (val_emb: (int → option (int, int)) → value → value → bool)
    (emb: int → option (int, int)) (m1 m2: mem_)
    (b1 ofs b2 delta: int) (v1 v2: value) (ty: memtype) (m1’: mem_)
  requires { ... }
  ensures { ... }
= assert { valid_pointer_ ty m1 b1 ofs };
  assert { valid_pointer_ ty m2 b2 (ofs + delta) }

The assertions are introduced in the hypotheses of the lemma and Why3 gener-
ates two new VCs to prove both the assertions are valid.

Witnesses for existential statements. When one needs to prove an existentially
quantified formula, sometimes the automatic theorem provers are not able to eas-
ily find the specific witness. Therefore, one needs to manually build it. Consider
the following lemma:
lemma store_lessdef:
  forall m1 m2 ty b ofs v1 m1’ v2. mem_lessdef m1 m2 →
      store_ ty m1 b ofs v1 = Some m1’ → val_lessdef v1 v2 →
      exists m2’. store_ ty m2 b ofs v2 = Some m2’ ∧ mem_lessdef m1’ m2’

We convert the lemma to a let lemma and as the lemma now needs to return a
value, we change the signature of the function to return the type of the witness:
let lemma store_lessdef (m1 m2: mem_) (ty: memtype) (b ofs: int)
    (v1: value) (m1’: mem_) (v2: value) : (m2’: mem_)

We also need to change the postcondition, which should now ensure the same
properties over the result of the function. This is achieved by replacing the
existential quantified variable with the output value m2’:
ensures { store_ ty m2 b ofs v2 = Some m2’ ∧ mem_lessdef m1’ m2’}

Lastly, the function needs to return a proper witness that satisfied the post-
conditions. In this case, we manually build a new memory state with updated
fields:
                                                   Leroy and Blazy were right    9

let lemma store_lessdef (m1 m2: mem_) (ty: memtype) (b ofs: int)
    (v1: value) (m1’: mem_) (v2: value) : (m2’: mem_)
  ... = ...
  (mem_’mk (m2.nextblock) (m2.bounds_) (m2.freed)
    (update b (store_contents (m2.contents @ b) ty (ofs + 0) v2)
    (m2.contents)))

The proof is now automatic and again, the technique is general.


Outcome. Applying these three techniques to the remainder 9 lemmas, we re-
duce 100% the number of manually conducted transformations needed to com-
plete the proofs. Table 1 compares the before and after applying these techniques.


                                              Number of interactions (Why3)
            Lemma
                                                 Before           After
            1. check cont charact                  7               0
            2. set cont outside                    2               0
            3. set cont inside                     2               0
            4. free list left emb                  6               0
            5. free list not valid block           6               0
            6. embedding no overlap free list      6               0
            7. free list fresh block               3               0
            8. alloc list left inject             75               0
            9. alloc list alloc inject            10               0

               Table 1. Number of transformations before and after



4   Proof Effort

Coq support for proof automation is limited, as one needs to explicitly apply a
sequence of tactics and transformations to prove the desired goal. In contrast, one
of the main focus of Why3 is automation, linking with SMT solvers to discharge
proof obligations, what allows to develop proofs with less effort.
    In this section we present metrics to compare our proofs with the Coq version.
We used the original authors’ proof as we are not aware of any improved version
– nowadays Coq has much more support to automation and experts may reduce
significantly the amount of transformations. Anyway, our goal is not a direct
comparison between lines of proof scripts, but how much automation can be
achieved, being this actually the original challenge left by Leroy and Blazy.

Why3 fully automatic proof. All lemmas were automatically proved using
the auto level 3 tactic of Why3. The detailed proof results are available here.
The table 2 summarizes the structure of the proof.
    These results take into consideration the interactions stated explicitly in the
code. Although the automatic theorem provers were able to prove all the lem-
mas automatically, we had to use the techniques in Section 3 to aid the veri-
fication process. One might think these techniques do exactly the same thing
10         P. Barroso, M. Pereira, A. Ravara

                                                                  Module
                                                                                                                 Total
                         Gen Mem Facts Ref Gen Mem Facts Concrete Mem Rel Mem Mem Extends Mem Lessdef Mem Inject
     Number of lemmas             7            12             61          16             7          6        15      124



                                      Table 2. Number of lemmas per module



as the transformations in the Coq proof scripts. In some sense that is true, we
closely followed the Coq proof script and applied transformations one by one.
However, when explicitly stating the transformations, one gives auxiliary results
(e.g. auxiliary lemmas, assertions, concrete definitions) not a sequence of trans-
formations/tactics as in Coq. On one hand, in Why3 we have the certainty that
all auxiliary results are required to complete the proof (without them it is not
possible to prove the lemmas). On the other, in Coq, one does not have the cer-
tainty that all the tactics are essential to the proof (one just knows that specific
sequence completes the proof). Nonetheless, even without explicitly stating the
interactive proofs, the effort to prove the lemmas in Why3 was way less than in
Coq. Let us compare the non-fully automatic Why3 proof with the Coq version.

Why3 semi-automatic proof. The implementation and proofs without ex-
plicit interaction in the code can be consulted here. Even without stating explic-
itly the interactions, the theorem provers were able to prove 115 VCs automati-
cally, which translates into a gain of automation circa 93%. Table 3 summarizes
the results.

                                                                 Module
                                                                                                                      Total
                        Gen Mem Facts Ref Gen Mem Facts Concrete Mem Rel Mem Mem Extends Mem Lessdef Mem Inject
 Number of lemmas             7               12             61         16           7          6          15          124
 Automatically proved      7 (100%)        12 (100%)      58 (95%)   14 (87.5%)   7 (100%)   6 (100%)   11 (73.3%) 115 (92.7%)


                           Table 3. Number of lemmas proved automatically

    These 115 VCs corresponds to a total of approximately 870 lines of the Coq
proof script, which in turn consists of 89.6% of the total lines of the entire
Coq proof script. Table C2 compares the amount of transformations used in
interactive proofs in Why3 and Coq. One can see that in Why3 we have a
reduction of 46.8% of the transformations compared to the Coq version, which
means significantly less proof effort.


5     Code extraction
One extra contribution of our work is the extraction of a correct-by-construction
OCaml implementation of the memory model.
   The implementation of Leroy and Blazy uses several undefined functions (e.g.
enough free memory, alignof). In order to extract OCaml code, we need to
organize the code involving these functions and insert them into a parameterized
module (functor). For example, considering the function enough free memory,
we include its signature in the scope of the following Make functor:
                                                 Leroy and Blazy were right      11

scope Make
    scope X
        val function enough_free_memory (mem: mem_) (i: int) : bool
    end = struct ... end

With this manual transformation in the WhyML code (with the respect to the
one we originally used for the proofs), the extraction becomes automatic in the
sense that the obtained OCaml code compiles.

6   Conclusions
In this paper we present two versions in Why3 of the memory model of Leroy
and Blazy, which is used in the Compcert compiler: from the proof point of
view one is semi-automatic and the other results from an engineering effort to
attain full automation (e.g. turning tactics into auxiliary results). Using the
Why3 code extraction mechanism [7], from both versions we get correct-by-
construction OCaml implementations of the memory model.
    The first version is a direct translation from the Coq development to Why3.
We immediately gain 93% of automation. The remaining 7% were proved follow-
ing closely the Coq proof script. Nonetheless, in Why3 the amount of transfor-
mations required for the theorem provers to validate the proofs were significantly
less (117 transformations versus a total of 220).
    The second version is a fully automatic proof. We performed general tech-
niques (explained in Section 3) to explicitly define the interactive proofs of the
first version within the WhyML code. This improves readability, as one does not
need to open the Why3 IDE to verify which transformations are used, it is pos-
sible to have the essence of the proof just by analyzing the code. Furthermore,
as the proof is fully automatic, this approach also preserves the proof-sessions,
allowing a simple replay to check the reproducibility of the results.

Lessons learned. Nothing of the memory model was inexpressible in WhyML.
This confirms the premise that automatic verification tools are well-good candi-
dates to defiant proofs of complex programs without losing expressiveness.
   Furthermore, most of the proofs required a handful of transformations and
nevertheless 93% of the proof was performed by merely pressing a button (hence
using automatic tactics, like split, etc). It is possible to save time and effort to
the proofs that are actually challenging.
   It is undoubtedly that we are, at some point, limited to first order logic,
however if one reaches the limits of these type of provers, one can still prove the
remaining goals in Coq for example. In fact, Why3 provides a Coq tactic to call
external theorem provers as oracles.
   Nonetheless, to achieve an even higher level of automation we performed
some refactoring to expose properties to the WhyML code: created auxiliary
lemmas from patterns that constantly appear in the Coq proof script; defined
inductive predicates to avoid proofs by induction; and transformed existential
proofs to lemma functions which return the desired witness.
12      P. Barroso, M. Pereira, A. Ravara

Acknowledgements



Work partially supported by the Portuguese Fundação para a Ciência e Tecnolo-
gia via NOVA LINCS (UIDB/04516/2020) and by the first author PhD grant
(UI/BD/151265/2021).




References



1. Bobot, F., Filliâtre, J.C., Marché, C., Melquiond, G., Paskevich, A.: Preserving user
   proofs across specification changes. In: Cohen, E., Rybalchenko, A. (eds.) Verified
   Software: Theories, Tools, Experiments. pp. 191–201. Springer Berlin Heidelberg,
   Berlin, Heidelberg (2014)
2. Filliâtre, J.C., Paskevich, A.: Why3—where programs meet provers. In: European
   symposium on programming. pp. 125–128. Springer (2013)
3. Leroy, X.: A formally verified compiler back-end. Journal of Automated Reasoning
   43(4), 363–446 (nov 2009). https://doi.org/10.1007/s10817-009-9155-4, https://doi.
   org/10.1007%2Fs10817-009-9155-4
4. Leroy, X., Blazy, S.: Formal verification of a c-like memory model and its uses for
   verifying program transformations. Journal of Automated Reasoning 41 (07 2008).
   https://doi.org/10.1007/s10817-008-9099-0
5. Mador-Haim, S., Maranget, L., Sarkar, S., Memarian, K., Alglave, J., Owens, S.,
   Alur, R., Martin, M.M.K., Sewell, P., Williams, D.: An axiomatic memory model
   for power multiprocessors. In: Madhusudan, P., Seshia, S.A. (eds.) Computer Aided
   Verification. pp. 495–512. Springer Berlin Heidelberg, Berlin, Heidelberg (2012)
6. Mansky, W., Garbuzov, D., Zdancewic, S.: An axiomatic specification for sequential
   memory models. In: Kroening, D., Păsăreanu, C.S. (eds.) Computer Aided Verifi-
   cation. pp. 413–428. Springer International Publishing, Cham (2015)
7. Pereira, M.J.P.: Tools and Techniques for the Verification of Modular State-
   ful Code. (Outils et techniques pour la vérification de programmes impératives
   modulaires). Ph.D. thesis, University of Paris-Saclay, France (2018), https://tel.
   archives-ouvertes.fr/tel-01980343
8. Ševčı́k, J., Vafeiadis, V., Zappa Nardelli, F., Jagannathan, S., Sewell, P.: Com-
   pcerttso: A verified compiler for relaxed-memory concurrency. J. ACM 60(3) (jun
   2013). https://doi.org/10.1145/2487241.2487248, https://doi.org/10.1145/2487241.
   2487248
9. Winskel, G.: The Formal Semantics of Programming Languages: An Introduction.
   MIT Press, Cambridge, MA, USA (1993)
                                           Leroy and Blazy were right   13

A      Comparison of an automatic proof
Coq
Lemma store_mapped_emb:
    ...
Proof: (166
transformations/tactics)
  assert (valid_pointer ty m1 b1 ofs).
  eapply M.store_valid_pointer; eauto.
  assert (valid_pointer ty m2 b2 (ofs + delta)).
  eapply valid_pointer_emb; eauto.
  destruct (M.valid_pointer_store _ _ _ _ v2 H6)
    as [m2’ STORE2].
  exists m2’; split. auto.
  red. intros ty’ b1’ ofs’ v b2’ delta’ CP LOAD1.
  assert (valid_pointer ty’ m1 b1’ ofs’).
  rewrite ←
(store_valid_pointer_inv (...) ).
  eapply M.load_valid_pointer; eauto.
  generalize (load_store_characterization (...) ).
  destruct (load_store_classification (...) );
  intro.
  ... (+50 lines)
Qed


    Why3
    lemma store_mapped_emb:
      ...




    – The proof is immediate
    – Proved in 0.15 seconds
14    P. Barroso, M. Pereira, A. Ravara

B    Types of proofs


                                               Number of transformations
     Type Lemma
                                                        Why3
       •   1. check cont charact                           7
       •   2. set cont outside                             2
       •   3. set cont insid                               2
       •   4. free list left emb                           6
       •   5. free list not valid block                    6
       •   6. embedding no overlap free list               6
       •   7. free list fresh block                        3
       •   8. alloc list left inject                      75
       •   9. alloc list alloc inject                     10

 • Simple induction
 • Induction and case analysis
 • Assertions
 • The two above + proof of an existential statement

            Table B1. Number of transformations per type of proof




C    Amount of transformations used in interactive proofs
                                           Number of transformations
       Lemma
                                              Coq          Why3
       1. check cont charact                     26        7 (27%)
       2. set cont outside                       9         2 (22%)
       3. set cont inside                        15        2 (13%)
       4. free list left emb                     10        6 (60%)
       5. free list not valid block              16        6 (38%)
       6. embedding no overlap free list         11        6 (55%)
       7. free list fresh block                  11        3 (27%)
       8. alloc list left inject                 85        75 (88%)
       9. alloc list alloc inject                37        10 (27%)
       Total                                    220      117 (53.2%)
           Table C2. Number of transformations in interactive proofs
