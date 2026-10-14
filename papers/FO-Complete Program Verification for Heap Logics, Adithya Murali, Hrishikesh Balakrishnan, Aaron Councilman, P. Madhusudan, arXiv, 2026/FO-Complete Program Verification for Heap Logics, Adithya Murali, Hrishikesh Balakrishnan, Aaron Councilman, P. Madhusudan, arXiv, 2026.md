                                         FO-Complete Program Verification for Heap Logics
                                         ADITHYA MURALI, University of Wisconsin–Madison, USA
                                         HRISHIKESH BALAKRISHNAN, University of Illinois Urbana-Champaign, Department of Computer
                                         Science, USA
                                         AARON COUNCILMAN, University of Illinois Urbana-Champaign, Department of Computer Science,
                                         USA
                                         P. MADHUSUDAN, University of Illinois Urbana-Champaign, Department of Computer Science, USA
arXiv:2601.06719v1 [cs.LO] 10 Jan 2026




                                         We develop the first two heap logics that have implicit heaplets and that admit FO-complete program verifica-
                                         tion. The notion of FO-completeness is a theoretical guarantee that all theorems that are valid when recursive
                                         definitions are interpreted as fixpoint definitions (instead of least fixpoint) are guaranteed to be eventually
                                         proven by the system. The logics we develop are a frame logic (FL) and a separation logic (SL-FL) that has an
                                         alternate semantics inspired by frame logic. We show verification condition generation for FL that is amenable
                                         to FO-complete reasoning using quantifier instantiation and SMT solvers. We show SL-FL can be translated
                                         to FL in order to obtain FO-complete reasoning. We implement tools that realize our technique and show
                                         the expressiveness of our logics and the efficacy of the verification technique on a suite of benchmarks that
                                         manipulate data structures.

                                         1   Introduction
                                         Automated verification of programs that destructively manipulate heaps remains a challenging open
                                         problem. Separation logic [50, 51, 61] has emerged as a popular specification logic for expressing
                                         properties of structures in heaps. While separation logic is used extensively in interactive theorem
                                         proving settings, robust automation of separation logic reasoning has not yet met the same level of
                                         success [18].
                                            One problem for automation of separation logic is that several aspects of it are inherently second-
                                         order, making it extremely hard to automatically reason with them using SMT solvers (especially
                                         SMT solvers on decidable logics). In particular, the magic wand (−∗) in separation logic quantifies
                                         over arbitrary heaps that satisfy a property, which is inherently second-order [10]. Separation logic
                                         reasoning tools evaluated in competitions (like SLComp [62]) seldom support the magic wand
                                         operator and attest to the difficulty of reasoning with it.
                                            Even when the magic wand is avoided (like using incomplete strongest post calculations, e.g., [7]),
                                         expressing properties such as separating conjunction, conjunction, and disjunction requires quan-
                                         tifying over sets of locations, and when proving implication or entailment, results in formulas
                                         with both existential and universal quantification over sets. These are hard to reason with using
                                         first-order solvers and, as we show in this paper, results in incompleteness.
                                            The current state-of-the-art for automatic program verification techniques for any expressive
                                         heap logic is hence always incomplete— i.e., validity of verification conditions are not just unde-
                                         cidable, but not even recursively enumerable. (There are some heap logics that are decidable, but
                                         these are often heavily restricted in expressiveness [25, 56–58].). In other words, no complete proof
                                         system exists for them and no sound algorithmic procedure can exist that, on all valid verifica-
                                         tion conditions, halts and declares it valid (even if it’s allowed to be non-terminating on invalid
                                         ones). Systems such as Viper [40] use several heuristics for magic wand and generate verification
                                         conditions that have quantifiers over sets and maps, along with triggers, that are sent to an SMT
                                         Authors’ Contact Information: Adithya Murali, adithya5@illinois.edu, University of Wisconsin–Madison, Madison, Wiscon-
                                         sin, USA; Hrishikesh Balakrishnan, hb19@illinois.edu, University of Illinois Urbana-Champaign, Department of Computer
                                         Science, Urbana, Illinois, USA; Aaron Councilman, aaronjc4@illinois.edu, University of Illinois Urbana-Champaign, De-
                                         partment of Computer Science, Urbana, Illinois, USA; P. Madhusudan, madhu@illinois.edu, University of Illinois Urbana-
                                         Champaign, Department of Computer Science, Urbana, Illinois, USA.
2                                                                                             Trovato et al.


solver that is inherently incomplete for such logics [22]. Furthermore, incompleteness manifests in
practice as well (see the recent paper [18] that studies incompleteness of various algorithms for
separation logic using the Viper framework).
   Incompleteness stems from various sources, and we formally identify several sources later in this
paper. First, intrinsic second-order quantifications lead to incompleteness, especially quantification
over sets. Second, heap logics that are defined using finite models for heaps quickly become
incomplete, even for first-order logics, due to fundamental incompleteness theorems in finite model
theory [37]. Third, heap logics typically require recursive definitions that have a least fixpoint
semantics, which causes incompleteness even when models are infinite, as they allow encoding
addition and multiplication of integers, and incompleteness follows from Gödel’s incompleteness
theorem [19]. Fourth, heap logics for programs need to allow a combined theory of background
sorts with models such as linear arithmetic in order to define typical data structures (like a binary
search tree), and combination of quantified theories also leads to incompleteness.
   These aspects lead to expressive heap logics being inevitably incomplete. Practical algorithmic
techniques for validity for heap logics hence cannot be held to any theoretical standard of effective-
ness, such as completeness, and empirical effectiveness on benchmarks are the sole way to judge the
efficacy of a technique. Most importantly, we have no theoretical foundation that guarantees that
an algorithmic technique will not embarrassingly fail to prove a simple verification task, despite
being given unbounded resources.

The notion of FO-completeness In this paper, we pose the audacious question as to whether we
can, despite the above challenges, define a notion of completeness that we can hold algorithmic
techniques for heap logics up to. The motivation for such a completeness guarantee is that it will
yield a pathway to more predictable program verification tools than the current state-of-the-art.
We propose FO-completeness as a completeness notion for heap logics, inspired by recent results in
the literature that show that there are similar domains where FO-complete procedures are both
practical and robust.
   The single most unavoidable reason for incompleteness of heap logics is the inclusion of recursive
definitions. Given a recursive definition of a relation (or function) 𝑓 (𝑥) =lfp 𝜌 (𝑥, 𝑓 ), 𝑓 is meant to
be interpreted as the least fixpoint satisfying the given equation. Such definitions are beyond the
power of first-order logics, and moreover render logics incomplete as described above. A simple
and practically effective way to bring down this expressive power is to instead interpret recursive
definitions as fixpoint definitions 𝑓 (𝑥) = 𝜌 (𝑥, 𝑓 ), where we admit any predicate/function 𝑓 that
satisfies the equation, not just the least fixpoint.
   We say that validity of verification conditions with heap logic specifications is FO-complete if
they are valid with respect to such a fixpoint semantics of recursive definitions in the logic. The
name FO-completeness stems from the fact that such equations can be expressed in first-order logic.
Note that if a theorem is valid with respect to any fixpoint that satisfies the recursive definitions,
then the theorem is valid with respect to the least fixpoint semantics as well.
   Recent results in the literature have argued that some existing practical, efficient, and robust
techniques based on unfolding recursive definitions (“unfold-and-match” heuristics, "fold/unfold"
operations) for program verification are in fact FO-complete. In particular, there is work arguing that
the so-called natural proofs for certain fragments of first-order logics with recursive definitions have
FO-completeness [38]. And there is work arguing that functional program verification techniques
over algebraic datatypes (ADTs) used in Liquid Haskell for Haskell programs [72] and Leon/Stainless
for Scala programs [8, 67] is also FO-complete [42]. In the latter setting, in order to express properties
in FO logic, the standard universe of ADTs is replaced with its FO axiomatization (which admits
nonstandard models), and it has been shown that the techniques used in practice are FO-complete
FO-Complete Program Verification for Heap Logics                                                        3


under this modeling. Note that there is a gap between least fixpoint semantics and fixpoint semantics,
and these frameworks require inductive lemmas to bridge this gap. Current tools require users to
give these lemmas, but there is active research of synthesizing these lemmas automatically [34, 41].
   The above discussion motivates the primary question we pose in this paper:
        Are there expressive heap logics with recursive definitions that have FO-complete
        validity procedures?
   More precisely, we would like validity procedures that are sound— if they report that a theorem is
valid, it is valid with respect to the least fixpoint semantics for definitions. And also FO-complete— if
a theorem is valid with fixpoint semantics of recursive definitions, then the procedure is guaranteed
to terminate and prove it valid. Note that if a theorem is valid with respect to least fixpoint semantics,
but not valid with respect to fixpoint semantics, the tool is not required to terminate.
   We are interested in heap logics that also have the following desirable properties:
     • The logic should have implicit heaplets. Separation logic pioneered the fundamental design
       principle that every formula 𝛼 is implicitly associated with a heaplet that captures precisely
       the subset of locations relevant to 𝛼, and contracts for function calls use this implicit heaplet
       as the locations on which permission is taken to modify the heap. We require such implicit
       heaplets to enable natural frame reasoning by the client, akin to separation logic.
     • The logic should allow standard combinations with background sorts/theories such as linear
       arithmetic.
     • The logic should be amenable to reasoning using reduction to SMT solvers in order to facili-
       tate scalable and efficient reasoning (note, however, that calling SMT solvers on incomplete
       logics is a nonstarter). We furthermore require empirical evidence that reasoning is fairly
       efficient in practice, despite using an FO-complete procedure.
   The primary contribution of this paper is to establish the first two heap logics that satisfy the
above desiderata and admit FO-complete procedures. We also provide empirical evidence that the
FO-complete procedures we develop result in efficient reasoning over a standard benchmark of data
structure manipulating programs with rich specifications of their functional behavior. The first heap
logic is Frame Logic [43, 44], and the second heap logic is a new separation logic that has an alternate
semantics inspired by frame logic.
An FO-complete Frame Logic Our first focus of investigation is Frame Logic (FL), proposed recently
by Murali et al that embraces the principles of separation logic but works in a first-order logic setting
with recursive definitions (FORD) [43, 44]. Frame logic (FL) is aesthetically simple— it adds to classical
first-order logic with recursive definitions a support operator Sp, where Sp(𝛼), for any formula 𝛼,
evaluates to the implicit subset of locations of the heap that the truthhood/falsehood of 𝛼 relies
upon. The support is similar to local heaplets in separation logic. However, unlike separation logic,
supports are uniquely defined, which allows modeling them without true quantification over sets.
   Instead of relying on a localized heaplet semantics as separation logic does, the semantics of FL
keeps the classical semantics of FORD over the global heap, but allows recovering the local heaplet
using the support operator. Frame logic can express the separating conjunct — 𝛼 ∗ 𝛽 is essentially
expressed as 𝛼 ∧ 𝛽 ∧ Sp(𝛼) ∩ Sp(𝛽) = ∅.
   Work on frame logic by Murali et al [43, 44] has argued that weakest preconditions for programs
with frame logic annotations are expressible in frame logic itself, and that verification conditions
in frame logic can be translated to FORD. However, this does not translate to automation (espe-
cially using SMT solvers) as FORD with alternating quantifiers is highly complex. The weakest
precondition transformations described in [43, 44] are complex, involving several introductions
of quantifiers leading to weakest preconditions having alternations of universal and existential
4                                                                                           Trovato et al.


quantification. Furthermore, weakest preconditions introduce first-order formulations of magic
wand (“MW”-operators) that have gnarly definitions that are too complex to automate.
   In this paper, we approach automated verification of frame logic afresh with the goal of embed-
ding verification conditions into an existing automatable class of first-order logic with recursive
definitions. The technique of natural proofs is a well-established technique for handling such
logics— it uses recursive definition unfoldings, uninterpreted function abstractions, and SMT-based
quantifier-free reasoning to build sound automated reasoning [38, 54, 59]. Furthermore, the work on
its foundations [38] identifies a particular fragment 𝐿oneway for which the natural proofs technique
is 𝐹𝑂-complete.
   The first technical contribution of this paper is to build an FO-complete automated program
verification paradigm for frame logic specifications that generates verification conditions in the
logic 𝐿oneway . We overcome several challenges using novel ideas, including (a) defining an adequately
powerful fragment of frame logic that allows a restricted form of quantification using a new cloud
operator, and (b) generating verification conditions with care so that they are in the 𝐿oneway fragment
and have existential quantification only over the foreground sort. The verification conditions are
generated using strongest-post like symbolic evaluation rather than weakest preconditions, avoiding
magic wand like operators.
An FO-complete Separation Logic The second contribution of this paper is a separation logic
with an alternate semantics than classical semantics, and an FO-complete procedure for program
verification for it. The new logic, SL-FL, is a separation logic that has determined heaplets inspired
by frame logic. As far as we know, this is the first separation logic that is powerful enough (has
recursive definitions and an undecidable validity problem) and that admits 𝐹𝑂-complete program
verification.
   The logic SL-FL is interpreted over stores and heaplets, (𝑠, ℎ), instead of a global heap, similar to
traditional separation logic. However, it is designed so that for any formula 𝛼 and for any global
heap 𝑔, there is at most one heaplet ℎ of 𝑔 on which 𝛼 holds. It is in this sense that SL-FL has
determined heaplets. Note that traditional separation logic does not have this property— 𝛼 ∨ 𝛽 can
hold in multiple heaplets of a global heap, say one satisfying 𝛼 and one satisfying 𝛽, and formulas
like true hold on multiple heaplets. The semantics of SL-FL uses auxiliary support operators inspired
by frame logic in order to define determined heaplets.
   We show that SL-FL formulas can be translated to frame logic, where 𝛼 in SL-FL translates to
a formula 𝛼 ′ in frame logic, where although 𝛼 ′ is interpreted on global heaps, its support Sp(𝛼 ′ )
is precisely the unique heaplet under which 𝛼 could hold. Coupling this translation with the
FO-complete verification for programs against frame logic specifications gives us an FO-complete
program verification for SL-FL. SL-FL has several other features that also facilitate FO-completeness—
specifications are purely quantifier-free, but we allow a set of recursive definitions (that require
quantification), and global heaps are interpreted as potentially infinite models, avoiding another
source of incompleteness.
Evaluation The third contribution of this paper is an evaluation that addresses two primary
research questions: (a) are the logics we define expressive enough for full functional specification
of standard data structure manipulating routines, and (b) are the FO-complete program verification
mechanisms efficient in practice in verifying such programs. We develop tools, a tool FLV (Frame
Logic Verifier) for programs annotated with frame logic specifications, and a checker SLFLV that
translates SL-FL formulae to facilitate FO-complete verification against SL-FL specifications. FLV
generates verification conditions in first-order logic with recursive definitions, in particular in the
logic 𝐿oneway , and utilizes an existing tool to do natural proof based FO-complete reasoning [38,
41, 54, 59]. We evaluate our tool on a suite of programs that manipulate common data structures,
FO-Complete Program Verification for Heap Logics                                                       5


and find that both logics are expressive enough for stating rich functional specifications for these
methods, and facilitate efficient verification.
   In summary, our work develops the first expressive heap logics, a frame logic and a separation
logic, that have implicit heaplets and admit FO-complete validity procedures. We provide the accom-
panying program verification methodologies and an evaluation that attests to the expressiveness of
the logics and efficiency of the automation. This work hence establishes a new theoretical standard
of completeness for heap logics. Our hope is that demanding this new standard of FO-completeness
for future heap logics paves the way for more robust and predictable heap verification.

2   Sources of Incompleteness in Heap Logics
In this section, we show several results demonstrating key sources of incompleteness in heap logics.
In particular, we will show (a) restricting to finite models gives incompleteness, and hence we
must define models that include infinite models, (b) definitions with least fixpoint semantics cause
incompleteness, which motivates our study of completeness of definitions with arbitrary fixpoint
semantics (called FO-completeness), and (c) even when models are infinite and we consider fixpoint
definitions, classical separation logic makes design decisions related to having multiple heaplets
that can satisfy a formula, which intrinsically causes incompleteness.
   Completeness and Incompleteness for Logics. We say a logic L is complete if the set of all valid
formulas in L is recursively enumerable (written r.e.). In other words, there exists a sound procedure
that can prove every valid formula (but may not halt on invalid formulas). Conversely, we say
that L is incomplete if validity is not r.e.. Note that incompleteness implies undecidability, but the
converse is not true (e.g., pure FOL is undecidable but complete [19, 70]).
Finite Models A model is said to be finite if the size of its universe is finite. Logics whose semantics
is defined only over finite models are typically incomplete. This follows from general results in
Finite Model Theory [37].
  Theorem 2.1 (Trakhtenbrot’s Theorem). Fix a first-order signature Σ, and let 𝜑 be a formula
over that signature. The problem of checking whether 𝜑 is valid over finite models is not recursively
enumerable.
   The proof can be shown using a reduction from the non-halting problem for Turing machines to
validity of FOL over finite models. In fact, we can have linked lists encode configuration sequences
of Turing machines, and assert that they never encode a halting state. Given that linked lists are the
most basic data structures, finite models are a nonstarter for designing complete logics. Separation
logics are typically defined over finite heaps [61]. We avoid this source of incompleteness by
interpreting our logics over finite and infinite models.
Recursive Definitions A second source of incompleteness for heap logics stems from modeling
heap data structures and measures as recursive definitions with least fixpoint semantics. This holds
even when the logic has both finite and infinite models; the following is well-known:
  Proposition 2.2. First-Order Logic augmented with least fixpoint (lfp) recursive definitions (see
Section 3.1 for definition) is incomplete.
   In fact, one can define a “number line” along with addition and multiplication using a single
unary lfp definition (see [41]), yielding incompleteness by Gödel’s incompleteness theorem for
arithmetic [17]. This shows that accomodating lfp definitions are a nonstarter for achieving com-
pleteness. In this paper, we hence consider FO-completeness which is the notion of completeness
where definitions are interpreted using arbitrary fixpoint semantics.
6                                                                                                               Trovato et al.


Monadic Second-Order Quantification Yet another source of incompleteness for heap logics
stems from design choices that— either implicitly or explicitly— allow non-nested monadic second-
order quantification (quantification over sets). For example, the separating conjunction operator ∗ in
Separation Logic (SL) has the following semantics: “𝑠, ℎ |= 𝛼 ∗ 𝛽 if there exist disjoint subsets 𝑆 1, 𝑆 2 of
the domain of ℎ such that...”. Consequently, checking an entailment 𝛼 ∗ 𝛽 |= 𝛾 ∗𝛿 essentially requires
reasoning with a formula of the form (∃𝑆 1, 𝑆 2 . Valid (𝑆 1, 𝑆 2 ) ∧Φ) → (∃𝑆 3, 𝑆 4 . Valid (𝑆 3, 𝑆 4 ) ∧Φ′ ). Note
that this formula has both existential and universal quantification over sets (due to the implication).
We provide evidence that even such non-nested second-order quantification prohibits completeness:

  Theorem 2.3 (Proof in Appendix A). Monadic Second-Order Logic is incomplete. This holds even
where there is only one level of quantification over sets (no nesting).

Note that, in the above result, we consider validity over both finite and infinite models. We do not
know whether the above result is known, and provide a proof in Appendix A.
  In this work, we seek to avoid this source of incompleteness by designing logics where formulas
have unique heaplets. Intuitively, when formulas have unique heaplets, we can write their semantics
using universal quantification or existential quantification. After all, the universal quantifier can
only be satisfied by the uniquely defined heaplet of the formula! Therefore, instead of checking
(∃𝑆 1, 𝑆 2 . Valid (𝑆 1, 𝑆 2 )∧Φ) →                                  ′
                                    (∃𝑆 3, 𝑆 4 . Valid (𝑆 3, 𝑆 4 )∧Φ ), we can check ∀𝑆 1, 𝑆 2, 𝑆 3, 𝑆 4 . (Valid (𝑆 1, 𝑆 2 )∧
Φ) → (Valid (𝑆 3, 𝑆 4 ) → Φ ) . This formula only contains universal quantification over sets, and can
                                 ′

therefore be removed and considered as part of the first-order signature (as a monadic predicate).
   We conclude this section with a new incompleteness result for SL. Although prior work has
identified that operators like the magic wand are inherently second-order [10] (which would yield
incompleteness), we show SL is incomplete due to non-unique heaplets even if we eliminate the
magic wand as well as other sources of incompleteness such as finite models and least fixpoints:

  Theorem 2.4 (Non-Uniqe Heaplets make SL Incomplete). Separation Logic (a) without the
magic wand, (b) augmented with fixpoint definitions, and (c) defined over both finite and infinite
heaplets, is incomplete.

  We formally describe SL extended to infinite heaplets and fixpoint definitions, as well as the
proof of the above result in Appendix A. Our proof crucially uses the fact that SL formulas do not
have unique heaplets.
  In view of these results, we design logics in this paper that avoid these pitfalls in our search
for FO-complete heap logics. The logics FL and SL-FLwe design are interpreted over models of
arbitrary size (finite and infinite) and have determined heaplets, and we show both of them to
admit FO-complete program verification.

3   Frame Logic and Program Verification
In this section we introduce the first logic for which we design FO-complete reasoning: Frame
Logic (FL). FL was introduced in earlier work by Murali et al. [43, 44] as an extension of First-Order
Logic with Recursive Definitions (FORD) using a Support operator Sp to access the heaplets of
formulas. We present a high level technical summary of the key concepts including the syntax and
semantics of FL, as well as the notion of validity for Hoare Triples for which we design automation
techniques in this work. The ideas presented in this section are not the contribution of this paper
and are developed in prior works [38, 43].
FO-Complete Program Verification for Heap Logics                                                      7


3.1   First-Order Logic with Recursive Definitions
We now present First-Order Logic with Recursive Definitions (FORD). FORD is similar to first-order
logic with least fixpoints [1, 12, 24, 37, 71], except recursive definitions (which have least fixpoint
semantics) are given names.
    Formally, we have a signature Σ = (S, C, F , R, I) where S is a finite set of sorts, and C, F and
R are sets of constant, function, and relation symbols respectively. I is a set of relation symbols
disjoint from R whose interpretations are given using recursive definitions (as opposed to being
interpreted by a model). Symbols have their usual types, e.g., function symbols in F have an
associated arity 𝑛 ∈ N and are of type 𝜏1 × 𝜏2 . . . × 𝜏𝑛 → 𝜏, where 𝜏𝑖 , 𝜏 ∈ S.
    We require that S contain a designated foreground sort Loc. We use the foreground sort to
model heap locations. The remaining sorts, called background sorts, are used to model data values
such as integers, sets, etc. We use the function symbols in F to model pointers and data fields of
heap locations. For example, the next pointer of a linked list can be modeled using the symbol
next : Loc → Loc, and similarly, the key stored at a location can be modeled using key : Loc → Int.
    We do not provide the syntax of FORD here as it is essentially identical to the syntax of Frame
Logic given in Figure 1, except that FORD does not contain the support operator Sp(·).
Recursive Definitions A recursive definition of a predicate 𝐼 ∈ I is of the form 𝐼 (𝑥) :=lfp 𝜌 (𝑥),
where 𝜌 is a quantifier-free formula that only mentions recursively defined symbols in I positively
(i.e., under an even number of negations). This ensures that least fixpoints always exist [69]. We
formally treat recursively defined functions by modeling them as predicates, however, we will use
function symbols with recursive definitions in our exposition. We denote the set of definitions for
the symbols in I by D. We require that D contains exactly one definition for each 𝐼 ∈ I.
Semantics We consider first-order models where the foreground sort Loc is uninterpreted and the
background sorts are constrained by a first-order theory. This theory is usually the combination of
several theories over individual sorts such that the quantifier-free fragment of the combination
is decidable [47]. Given a set of definitions D for the symbols in I, a model of FORD consists
of a first-order model of the above kind that interprets the symbols in C, F , and R (respecting
the various theories), as well as an interpretation for the symbols in I that is determined by the
first-order model as the least fixpoint of the definitions D. Formulas are then evaluated as usual.
The Loneway Fragment 𝐿oneway is a syntactic fragment of FORD introduced in prior work [38]
which allows only “one-way" functions from the foreground sort to the background sorts. Formally,
every function symbol in F of arity 𝑛 whose range sort is the foreground sort Loc has domain Loc𝑛 .
Recursively defined symbols I of arity 𝑘 are of type Loc𝑘 . Finally, formulas are only allowed to
quantify existentially over Loc (for validity). Validity checking for formulas in 𝐿oneway is FO-complete
and can be automated effectively using a systematic quantifier-instantiation procedure [38] based
on Natural Proofs [54, 59].

3.2   Frame Logic with Guarded Quantification
Frame Logic (FL) [43, 44] is a heap logic based on FORD with implicit heaplets. Syntactically, FL
extends FORD with a support operator Sp(·) that allows access to the implicit heaplet. Formally,
given a formula 𝜑 (term 𝑡), Sp(𝜑) denotes the subset of locations (foreground elements) on which
the truth of 𝜑 (resp. value of 𝑡) depends. One can then use the Sp operator to state disjointness and
reason about framing, e.g., the formula List (𝑥) ∧ List (𝑦) ∧ Sp(List (𝑥)) ∩ Sp(List (𝑦)) = ∅ says that
𝑥 and 𝑦 point to disjoint linked lists.
Syntax In this work, we use a fragment of FL with guarded quantification shown in Figure 1.
Formally, we distinguish a set of mutable functions F𝑚 among the symbols in F with domain Loc
that model pointer and data fields over the foreground sort. We also require a background sort
8                                                                                                        Trovato et al.


            FL Formulas        𝜑    ≔   ⊥ | ⊤ | 𝑡 = 𝑡 | 𝑅(𝑡 1, . . . , 𝑡𝑚 ) | 𝜑 ∧ 𝜑 | 𝜑 ∨ 𝜑 | ¬𝜑
                                        | ite(𝛾 : 𝜑, 𝜑) | ∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑
                                        where 𝑅 ∈ R ∪ I, 𝑦 ∈ Var Loc , 𝑓 ∈ F𝑚
                 Guards        𝛾    ≔   𝑡 = 𝑡 | 𝑅(𝑡 1, . . . , 𝑡𝑚 ) | 𝛾 ∧ 𝛾 | 𝛾 ∨ 𝛾 | ¬𝛾 | 𝑖𝑡𝑒 (𝛾 : 𝛾, 𝛾)
                                        where 𝑅 ∈ R, 𝑡𝑖 , 𝑡 are not of type Set (Loc)
                  Terms        𝑡    ≔   𝑐 | 𝑥 | 𝑓 (𝑡 1, . . . , 𝑡𝑚 ) | 𝑖𝑡𝑒 (𝛾 : 𝑡, 𝑡)
                                        | (Sp(𝜑) if t is of type Set (Loc)) | (Sp(𝑡 ′ ) if t is of type Set (Loc))
                                        where 𝑐 is a constant, 𝑥 is a variable, and 𝑡 1, . . . , 𝑡𝑚 are of
                                        the appropriate type.
    Recursive definitions   𝐼 (𝑥)   ≔   𝜌 𝐼 (𝑥) where 𝐼 ∈ I, 𝑥 ∈ Loc𝑘 for some 𝑘 ∈ N, 𝜌 𝐼 is a
                                         FL-formula where all relation symbols 𝐼 ′ ∈ I occur
                                         only positively or inside a support expression
Fig. 1. Frame Logic with guarded quantification. Var Loc denotes variables over the foreground sort and
Set (Loc) denotes the sort consisting of sets of foreground elements. Terms and formulas are assumed to be
well-typed for simplicity of presentation.

Set (Loc) representing sets of foreground locations and define Sp(𝜑) as a term of type Set (Loc). We
utilize in the syntax ite (“if-then-else”) expressions over terms and formulas, where ite(𝛾 : 𝛼, 𝛽)
denotes “if 𝛾 holds then 𝛼 else 𝛽”. Note that the guard 𝛾 cannot mention inductively defined
predicates or terms of type Set (𝐿𝑜𝑐), including support expressions. These are technical restrictions
that are required to define a well-defined semantics for Frame Logic formulas.
   The fragment of FL that we use in this work has two restrictions. First, we only allow guarded
quantification of the form ∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑 (𝑦) where 𝑦 is a variable over the foreground sort Loc.
The truth value of this formula is the same as ∃𝑦 : 𝑦 = 𝑓 (𝑥) ∧ 𝜑 (𝑦), but its support is defined more
carefully. We describe this below. Second, we restrict the signature of function symbols as well as
recursively defined predicates/functions to be “one-way” in the sense of the 𝐿oneway fragment of
FORD described above. We reduce reasoning about programs with specifications written in this
fragment to the validity of formulas in 𝐿oneway .
Semantics FL semantics extends semantics for FORD. We refer the reader to prior work on FL [43]
for a detailed presentation. We focus here on the semantics of the Sp(·) operator. Sp is defined as
a set of recursive equations in Figure 2. Given a model 𝑀, the support of a formula 𝛼 in 𝑀 (resp.
term), denoted JSp(𝛼)K𝑀 , is the least fixpoint of the equations in Figure 2.
   The support can be understood as the set of locations (i.e., “heaplet”) on which mutable functions
must be applied (i.e., dereferenced) in order to compute the value of a given term or formula. The
support of constants is empty. The support of a term 𝑓 (𝑡) in 𝑀 for a mutable function 𝑓 ∈ F𝑚 is,
as expected, {J𝑡K𝑀 }. The application of a non-mutable function does not contribute to the support.
   The support of 𝛼 ∧ 𝛽 is intuitively the union of the supports of 𝛼 and 𝛽, and this is indeed the
case in FL. Note, however, that the support of 𝛼 ∨ 𝛽 is also the union of the supports of 𝛼 and 𝛽.
This is because Frame Logic defines a unique support for a formula regardless of its truth value. We
can also see this reflected in the definition of Sp(¬𝛼), which is equal to Sp(𝛼). This is different
from, say, Separation Logic [16, 49, 61], where the heaplet of 𝛼 ∨ 𝛽 is the heaplet of any of the
disjuncts that evaluate to true (formulas can have multiple heaplets). Unique heaplets are a salient
feature of FL, and the logic makes several design decisions to achieve this. We point the reader to
prior work [43] for a discussion on the ramifications of these design decisions.
   The support of ite(𝛾 : 𝛼, 𝛽) always includes the support of 𝛾 (since we need to evaluate 𝛾 to
determine the truth of the formula), but then only adds the support of the case that is evaluated
depending on 𝛾. We use the ite rather than ∨ to write expressions with finer-grained supports in
FL. The support of an inductively defined relation term Sp(𝐼 (𝑥)) is simply the support of the body
FO-Complete Program Verification for Heap Logics                                                                                                  9


JSp(𝑐)K𝑀 = JSp(𝑥)K𝑀 = ∅ for constant 𝑐, variable 𝑥                                                             𝑛
                                                                                                               Ø
            JSp(⊤)K𝑀 = JSp(⊥)K𝑀 = ∅                                             JSp(𝑅(𝑡 1 . . . , 𝑡𝑛 ))K𝑀 =          JSp(𝑡𝑖 )K𝑀 for 𝑅 ∈ R
                                                                                                               𝑖=1
        JSp(Sp(𝑡))K𝑀 = JSp(𝑡)K𝑀                                                                                Ø𝑛                 𝑛
                                                                                                                                  Ø
       JSp(𝑡 1 = 𝑡 2 )K𝑀 = JSp(𝑡 1 )K𝑀 ∪ JSp(𝑡 2 )K𝑀                            JSp(𝑓 (𝑡 1 . . . , 𝑡𝑛 ))K𝑀 =         {J𝑡𝑖K𝑀 } ∪     JSp(𝑡𝑖 )K𝑀 if 𝑓 ∈ F𝑚
                                                                                                               𝑖=1                𝑖=1
        JSp(𝛼 ∧ 𝛽)K𝑀 = JSp(𝛼)K𝑀 ∪ JSp(𝛽)K𝑀                                                                  𝑛
                                                                                                            Ø
        JSp(𝛼 ∨ 𝛽)K𝑀 = JSp(𝛼)K𝑀 ∪ JSp(𝛽)K𝑀                                      JSp(𝑓 (𝑡 1 . . . , 𝑡𝑛 ))K𝑀 = JSp(𝑡𝑖 )K𝑀 if 𝑓 ∉ F𝑚
                                                                                                               𝑖=1
       JSp(Sp(𝜑))K𝑀 = JSp(𝜑)K𝑀                                                                                                (
                                                                                                                                  JSp(𝑡 1 )K𝑀 if 𝑀 |= 𝛾
          JSp(¬𝜑)K𝑀 = JSp(𝜑)K𝑀                                                 JSp(ite(𝛾 : 𝑡 1, 𝑡 2 ))K𝑀 = JSp(𝛾)K𝑀 ∪
                                                                                                                                  JSp(𝑡 2 )K𝑀 if 𝑀 ̸ |= 𝛾
                                                         𝑛
                                                         Ø                                                                    (
 JSp(𝐼 (𝑡 1 . . . , 𝑡𝑛 ))K𝑀 = JSp(𝜌 𝐼 (𝑥))K𝑀 [𝑥←𝑢 ] ∪          JSp(𝑡𝑖 )K𝑀                                                         JSp(𝛼)K𝑀 if 𝑀 |= 𝛾
                                                         𝑖=1                    JSp(ite(𝛾 : 𝛼, 𝛽))K𝑀 = JSp(𝛾)K𝑀 ∪
                                                                                                                                  JSp(𝛽)K𝑀 if 𝑀 ̸ |= 𝛾
                       for 𝐼 ∈ I with definition
                                                                            JSp(∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑)K𝑀 = {J𝑥K𝑀 } ∪ JSp(𝜑)K𝑀 [𝑦←𝑢 ]
                       𝐼 (𝑥) :=lfp 𝜌 𝐼 (𝑥), and
                                                                                                         where 𝑢 = J𝑓 (𝑥)K𝑀
                       where 𝑢 = (J𝑡 1K, . . . , J𝑡𝑛K)

Fig. 2. Semantics of Support operator. J𝑒K𝑀 refers to the interpretation of an expression 𝑒 in a model 𝑀. The
support is defined as the least interpretation satisfying the given equations.
𝑃 ≔ 𝑥 ≔ 𝑦 | 𝑥 ≔ 𝑐 | 𝑣 ≔ 𝑏𝑒 | 𝑥 ≔ 𝑦.𝑓 | 𝑣 ≔ 𝑦.𝑑 | 𝑦.𝑓 ≔ 𝑥 | 𝑦.𝑓 ≔ 𝑐 | 𝑦.𝑑 ≔ 𝑣 | 𝑦.𝑑 ≔ 𝑏𝑒
                                 ¯ | assume(𝜂) | 𝑃; 𝑃 | if 𝜂 then 𝑃 else 𝑃 | return
   | alloc(𝑥) | free(𝑥) | 𝑞¯ ≔ 𝑔(𝑝)
Fig. 3. The syntax of the programming language. Here, 𝑥, 𝑦 are location variables of type 𝐿𝑜𝑐, 𝑐 is a location
constant, 𝑓 is a pointer of type 𝐿𝑜𝑐 → 𝐿𝑜𝑐, 𝑑 is a data field of type 𝐿𝑜𝑐 → 𝜏bs for some background sort 𝜏bs ,
𝑏𝑒 is a background expression, 𝑣 is a variable of a background sort, 𝜂 is a boolean expression without any
dereferences. Finally, 𝑔 is a function of type 𝜏1 × · · · × 𝜏𝑚 → 𝜏1′ × · · · × 𝜏𝑛′ for some 𝑚, 𝑛 where 𝜏𝑖 , 𝜏𝑖′ ∈ S. This
is a method whose body is itself a program whose variables are a superset of the input variables 𝑝𝑖 of type 𝜏𝑖
and the output variables 𝑞 𝑗 of type 𝜏 𝑗′ .
of the definition Sp(𝜌 (𝑥)). The body 𝜌 may of course mention 𝐼 recursively, and the support is the
least fixpoint of these equations.
   Finally, the support of ∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑 (𝑦) contains the location interpreted by 𝑥, as well as the
support of 𝜑 (𝑦) where 𝑦 is interpreted to be location corresponding to 𝑓 (𝑥) in the given model.
Note that although the formula evaluates the same as ∃𝑦. 𝑦 = 𝑓 (𝑥) ∧ 𝜑 (𝑦), its support only includes
the support of 𝜑 for values of 𝑦 ‘matching’ the guard, namely 𝑓 (𝑥).

3.3 Program Verification
We now describe the programming language and the notion of correctness for which we develop
automation in this work. These concepts serve as background for the verification condition (VC)
generation presented in Section 5, and the reader may safely skip it until after Section 4.
   Figure 3 describes the syntax of the language. It supports the typical commands including
mutation of fields, allocation, and deallocation of locations. The language also supports function
calls, including recursive calls 1 . The operational semantics for programs in this language is the
usual one for heap programs ( described in Appendix B). Program configurations are of the form
(𝑆, 𝐻, 𝐴) where 𝑆 is a store, 𝐻 is a heap, and 𝐴 is the set of allocated locations. There is also an
error configuration ⊥. We denote a transition between configurations 𝐶 1 and 𝐶 2 on a program 𝑃
                                                                    𝑃
according to the operational semantics by 𝐶 1 −
                                              → 𝐶2 .
1We do not include while loops in the formal syntax to simplify the technical exposition. However, our theory readily

extends to programs with iteration, with specifications including frame logic assertions as loop invariants.
10                                                                                           Trovato et al.


Hoare Triples and Validity We consider triples of the form {𝛼 } 𝑃 {𝛽} where 𝛼 and 𝛽 are FL
formulas in the fragment described above and 𝑃 is a program. We treat free variables in 𝛼 and 𝛽 as
constants, implicitly quantifying over them universally. We then define:
  Definition 3.1 (Hoare Triple Validity). {𝛼 } 𝑃 {𝛽} is valid if for every configuration (𝑆, 𝐻, 𝐴) such
that (𝑆, 𝐻 ) |= 𝛼 and JSp(𝛼)K (𝑆,𝐻 ) = 𝐴:
   (1) (𝑆, 𝐻, 𝐴) does not transition to ⊥ on 𝑃 according to the operational semantics, and
                    𝑃
                     → (𝑆 ′, 𝐻 ′, 𝐴′ ), then (𝑆 ′, 𝐻 ′ ) |= 𝛽 and JSp(𝛽)K (𝑆 ′ ,𝐻 ′ ) = 𝐴′
    (2) if (𝑆, 𝐻, 𝐴) −
   Note that we require the allocated set in the post-state to be equal to the support of the postcon-
dition.
   Informally, the above definition says the Hoare Triple is valid if starting from any configuration
satisfying the precondition where the allocated set is precisely the support of the precondition,
(a) the program does not behave erroneously (e.g., make unsafe dereferences), and (b) if it reaches
a final configuration then the postcondition must hold, with the allocated set in the post state
precisely equal to the support of the postcondition. To ensure the former, at each step in the program
we must check that dereferenced elements are contained within the allocated set. This motivates
the following definition, which we will use during VC generation for FL in Section 5.
Relaxed Postconditions. We introduce a variant 𝑅𝑃 on postconditions, read relaxed post, to indicate
that the allocated set in the post-state need not be ‘tight’ for the postcondition. We denote these
triples by {𝛼 } 𝑃 {𝑅𝑃 : 𝛽}. Their correctness is defined similarly to that of {𝛼 } 𝑃 {𝛽} above, except in
condition (2) we only require JSp(𝛽)K (𝑆 ′ ,𝐻 ′ ) ⊆ 𝐴′ . Similarly, we also use the variant 𝐻𝑃 to denote
Heapless Postconditions, with no checks on the allocated set.

4    A Separation Logic with Frame Logic Inspired Semantics
We now define a separation logic SL-FL with alternate semantics guided by frame logic semantics,
and an FO-complete procedure for it.
   An entire illustrated example of a program with SL-FL specifications, its translation to FL and the
verification condition generation for it is given in Appendix G.
   The primary design principle is that formulas have unique heaplets under which they can hold.
In particular, these heaplets are inspired by the support operator in FL. There are several salient
features of our separation logic: (1) Given a global heap 𝑔 and a store 𝑠, any formula 𝛼 will hold
in at most one heaplet of 𝑔, which we call Supp(𝛼, 𝑠, 𝑔), (2) Heaplets are assumed to be arbitrary
universes of locations (finite or infinite), avoiding incompleteness that finite models bring, and (3)
We disallow recursive definitions that take parameters from background sorts. Recursive definitions
are solely defined over the location sort, though the definitions themselves can utilize background
sorts by dereferencing pointers on locations. This allows us to eventually translate formulae to
the logic 𝐿oneway which has FO-complete reasoning. For example, rather than have a recursive
definition 𝑚𝑒𝑚(𝑥, 𝑖) that returns membership of an integer in a list pointed to by 𝑥, in our logic we
would define 𝑘𝑒𝑦𝑠 (𝑥) that collects the keys stored in the list pointed to by 𝑥, and assert 𝑖 ∈ 𝑘𝑒𝑦𝑠 (𝑥).
Note that such definitions, translated to first-order logic, avoid quantification over the background
sorts, which is crucial for completeness. Finally, we do not generate verification conditions in
separation logic itself, but rather translate separation logic annotations to frame logic, and utilize
the VC generation for frame logic which we develop in the previous section. Generating precise
verification conditions in separation logic often calls for magic-wand operations that we avoid by
working with frame logic.
   Our logic is powerful, subsuming several known precise separation logics in the literature [7, 43,
51] (precise separation logics are also designed to have unique heaplets). In particular, our logic
FO-Complete Program Verification for Heap Logics                                                           11


 SL-FL𝑏 formulas 𝛼, 𝛽, 𝛾           ≔ 𝛿 | 𝑥 −𝑓 𝑦 | 𝛼 ∗ 𝛽 | 𝛼 ∧ 𝛽 | 𝛼∧∧𝛽 | ite(𝛾, 𝛼, 𝛽) | ∃𝑦.(𝑥 −𝑓 𝑦 : 𝛼)
 SL-FL𝑏∨ formulas 𝛼, 𝛽, 𝛾          ≔ 𝛿 | 𝑥 −𝑓 𝑦 | 𝛼 ∗ 𝛽 | 𝛼 ∧ 𝛽 | 𝛼∧∧𝛽 | 𝛼 ∨ 𝛽 | ite(𝛾, 𝛼, 𝛽) | ∃𝑦.(𝑥 −𝑓 𝑦 : 𝛼)
         H.I. formulas 𝛿           ≔ true | false | 𝑥 = 𝑦 | 𝑥 ≠ 𝑦 | 𝑥 = nil | 𝑥 ≠ nil
  Fig. 4. Base Separation Logics with FL inspired semantics SL-FL𝑏 and SL-FL𝑏∨ ; H.I.:“heap-independent”

allows disjunction for spatial formulae which are not supported by prior precise separation logics.
We also allow for recursive definitions that evaluate to background sorts that are constrained by
arbitrary first-order theories such as arithmetic.
   While our alternate semantics adhere broadly to the design principles of separation logics,
the semantics of disjunction turns out to be starkly different, in order to ensure unique heaplets.
However, our logics provides an if-then-else (ite) construct, which has a more traditional semantics,
and that can model splitting into cases. Disjunction is often used for case analysis (e.g., definitions
of linked lists that use disjunction to capture whether 𝑥 is 𝑛𝑖𝑙 or non-𝑛𝑖𝑙, is really a case-split). From
our experience in annotating programs in our evaluation, it turns out that disjunction can mostly
be avoided (entirely avoided in our benchmarks), and replaced with such case analysis.
   We define first a base separation logic SL-FL𝑏 , where the semantic differences are clear, and a
base separation logic SL-FL𝑏∨ , with disjunction added. We then extend it to a more expressive logic
(SL-FL) with inductive definitions and background sorts. All these logics can be translated to FL and
hence, using our program verification scheme for frame logic, we provide FO-complete program
verification for them.

4.1    Base logics SL-FL𝑏 and SL-FL𝑏∨
Let us fix a set of locations 𝐿𝑜𝑐. Let 𝐿𝑜𝑐? denote 𝐿𝑜𝑐 ∪ {nil} where nil is a special symbol and
nil ∉ 𝐿𝑜𝑐. Let us fix a countable set of variables Var, and let 𝑥, 𝑦, 𝑥 1, 𝑥 2, 𝑥 ′, 𝑦 ′ etc. range over Var.
These variables will be used to intuitively model program variables as well as quantified variables.
Let us fix a finite set of pointers Ptr, and let 𝑓 , 𝑓 ′, 𝑔, etc. range over Ptr.
    The syntax for the logic SL-FL𝑏 is given in Figure 4. Here, 𝑥, 𝑦 range over Var and 𝑓 ∈ Ptr.
The logic supports the separating conjunction ∗, conjunction ∧, a weak conjunction ∧∧, a special
if-then-else construct ite, and guarded existential quantification. The logic SL-FL𝑏∨ is identical but
includes the disjunction operator.
Semantics: A store is a function 𝑠 : Var → 𝐿𝑜𝑐?. A heaplet ℎ is a set of functions {ℎ 𝑓 | 𝑓 ∈ Ptr},
where each ℎ 𝑓 : 𝐻 → 𝐿𝑜𝑐?, where 𝐻 ⊆ 𝐿𝑜𝑐 is the common domain for all the functions ℎ 𝑓 . Note
that we do not assume heaplets are finite.2 Note that the domain of all the functions ℎ 𝑓 is common.
We denote by ℎ(𝑓 ) the function ℎ 𝑓 that ℎ defines, and by 𝑑𝑜𝑚(ℎ) the set of locations 𝐻 . Also, for
any 𝑆 ⊆ 𝑑𝑜𝑚(ℎ), let ℎ ⇂ 𝑆 denote the heaplet where the domains of the pointer fields in ℎ are
restricted to 𝑆. A heaplet ℎ ′ is a subheap/subheaplet of ℎ if there is some 𝑆 ⊆ 𝑑𝑜𝑚(ℎ) such that
ℎ ′ = ℎ ⇂ 𝑆. A global heap is a heaplet ℎ with 𝑑𝑜𝑚(ℎ) = 𝐿𝑜𝑐.
    The semantics of the base logics are defined in Figure 5. Formulas 𝛼 are interpreted on a pair
(𝑠, ℎ), where 𝑠 is a store and ℎ is a heaplet, as in traditional separation logic. However, the semantics
are mutually recursively defined along with a definition of a support operator Supp, where Supp
maps each formula to a subset of locations, or to ⊥ that stands for it being undefined. Intuitively,
the support of a formula is the subset of locations of ℎ that the evaluation of a formula in the
heaplet ℎ depends upon, and is ⊥ if 𝛼 cannot be evaluated within the heaplet ℎ.
    As we shall prove soon (Lemma 4.2), the definitions are designed so that whenever (𝑠, ℎ) |= 𝛼
holds, it will be the case that 𝑑𝑜𝑚(ℎ) = Supp(𝛼, 𝑠, ℎ), i.e., 𝛼 can hold only on heaplets where the
support map evaluates to the entire heaplet. Assuming this, let us go through the semantics.
2 In our logics, heaps can be infinite, and so can heaplets, like the heaplet of an infinite list.
12                                                                                                                 Trovato et al.

                                Supp(𝛿, 𝑠, ℎ)      = ∅, for any heap-independent atomic formula 𝛿
                         Supp(𝑥 −𝑓 𝑦, 𝑠, ℎ)       = {𝑠 (𝑥)} if 𝑠 (𝑥) is in 𝑑𝑜𝑚(ℎ) and ⊥ otherwise
                           Supp(𝛼 ⊕ 𝛽, 𝑠, ℎ)       = Supp(𝛼, 𝑠, ℎ) ∪ Supp(𝛽, 𝑠, ℎ), where ⊕ ∈ {∧, ∗, ∧   ∧}
                       Supp(ite(𝛾, 𝛼, 𝛽), 𝑠, ℎ)    = Supp(𝛾, 𝑠, ℎ) ∪ Supp(𝛼, 𝑠, ℎ), if (𝑠, ℎ ⇂ Supp(𝛾, 𝑠, ℎ) |= 𝛾
                                                                                      and (𝑠, ℎ ⇂ Supp(𝛼, 𝑠, ℎ)) |= 𝛼
                                                   = Supp(𝛾, 𝑠, ℎ) ∪ Supp(𝛽, 𝑠, ℎ), otherwise
              Supp(∃𝑦.(𝑥 −𝑓 𝑦 : 𝛼), 𝑠, ℎ)         = ⊥ if 𝑠 (𝑥) ∉ 𝑑𝑜𝑚(ℎ)
                                                   = {𝑠 (𝑥)} ∪ Supp(𝛼, 𝑠 [𝑦 ↦→ ℎ(𝑓 )(𝑠 (𝑥))], ℎ) otherwise.

     (𝑠, ℎ)     |=     𝛿                     iff   𝑑𝑜𝑚(ℎ) = ∅ and 𝑠 |= 𝛿, for any heap-independent formula 𝛿
     (𝑠, ℎ)     |=     𝑥 −𝑓 𝑦               iff   𝑑𝑜𝑚(ℎ) = {𝑠 (𝑥)} and ℎ(𝑓 )(𝑠 (𝑥)) = 𝑦
     (𝑠, ℎ)     |=     𝛼 ∗𝛽                  iff   there exists ℎ 1, ℎ 2 subheaplets of ℎ, dom(ℎ 1 ) = Supp(𝛼, 𝑠, ℎ),
                                                    dom(ℎ 2 ) = Supp(𝛽, 𝑠, ℎ), dom(ℎ 1 ) ∪ dom(ℎ 2 ) = dom(ℎ),
                                                    dom(ℎ 1 ) ∩ dom(ℎ 2 ) = ∅, (𝑠, ℎ 1 ) |= 𝛼 and (𝑠, ℎ 2 ) |= 𝛽
     (𝑠, ℎ)     |=     𝛼 ∧𝛽                  iff   (𝑠, ℎ) |= 𝛼 and (𝑠, ℎ) |= 𝛽
     (𝑠, ℎ)     |=     𝛼∧∧𝛽                  iff   there exists ℎ 1, ℎ 2 subheaplets of ℎ, dom(ℎ 1 ) ∪ dom(ℎ 2 ) = dom(ℎ),
                                                    (𝑠, ℎ 1 ) |= 𝛼 and (𝑠, ℎ 2 ) |= 𝛽
     (𝑠, ℎ)     |=     ite(𝛾, 𝛼, 𝛽)          iff   there exists ℎ 1, ℎ 2 subheaplets of ℎ, dom(ℎ 1 ) ∪ dom(ℎ 2 ) = dom(ℎ),
                                                    dom(ℎ 1 ) = Supp(𝛾, 𝑠, ℎ 1 ), and,
                                                    [ (𝑠, ℎ 1 ) |= 𝛾 and dom(ℎ 2 ) = Supp(𝛼, 𝑠, ℎ 2 ) and (𝑠, ℎ 2 ) |= 𝛼) ]𝑜𝑟
                                                    [ (𝑠, ℎ 1 ) ̸ |= 𝛾 and dom(ℎ 2 ) = Supp(𝛽, 𝑠, ℎ 2 ) and (𝑠, ℎ 2 ) |= 𝛽) ]
     (𝑠, ℎ)     |=     (∃𝑦.𝑥 −𝑓 𝑦 : 𝛼)      iff   𝑥 ∈ 𝑑𝑜𝑚(ℎ) and (𝑠 [𝑦 ↦→ ℎ(𝑓 )(𝑥)], ℎ) |= 𝛼
                                                      Rules for disjunction:
                                       Supp(𝛼 ∨ 𝛽, 𝑠, ℎ)     = Supp(𝛼, 𝑠, ℎ) ∪ Supp(𝛽, 𝑠, ℎ)
              (𝑠, ℎ)    |=    𝛼 ∨𝛽     iff   there exists ℎ 1, ℎ 2 subheaplets of ℎ, dom(ℎ 1 ) ∪ dom(ℎ 2 ) = dom(ℎ),
                                              dom(ℎ 1 ) = Supp(𝛼, 𝑠, ℎ 1 ), dom(ℎ 2 ) = Supp(𝛽, 𝑠, ℎ 2 ), 𝑎𝑛𝑑,
                                              ((𝑠, ℎ 1 ) |= 𝛼 or (𝑠, ℎ 2 ) |= 𝛽)
Fig. 5. Definition of supports and semantics for base separation logic SL-FL𝑏 , mutually defined. Definitions
for SL-FL𝑏∨ include the rules for disjunction. Set operations on supports that evaluate to ⊥ evaluate to ⊥.


   The semantics for heap-independent formulas requires heaplets to be empty. This allows us
to ensure that the heaplet is determined, rather than in traditional separation logic where such
formulas hold over any heaplet. Note that we don’t have an emp formula, as true has the same
semantics. The semantics of 𝑥 −𝑓 𝑦, 𝛼 ∗ 𝛽, and 𝛼 ∧ 𝛽 are similar to standard separation logic
semantics [61]. Though the definition for ∗ says any way to split the two heaplets into disjoint
parts that satisfy the two subformulas is fine, we know inductively that there is in fact only one
way to effect this split. The semantics of conjunction and weak conjunction are similar (the weak
conjunct doesn’t require the two heaplets to be the same).
   The ite construct has an involved semantics. Intuitively, to evaluate ite(𝛾, 𝛼, 𝛽), we would evaluate
𝛾 on the heaplet it requires, and depending on whether 𝛾 holds or not, evaluate 𝛼 on the heaplet
it requires. Note that the heaplet required by any formula 𝛼 is the subheaplet ℎ ′ such that the
support of 𝛼 computed with respect to ℎ ′ is precisely 𝑑𝑜𝑚(ℎ ′ ). The definition of support is carefully
designed so that such a subheaplet, if it exists, is unique (proven below in Lemma 4.1).
   The definition of supports of formulas with respect to a store and heaplet Supp(𝛼, 𝑠, ℎ), are
natural definitions, but note that the definition of ite refers to the semantics of heaplets in order to
split cases on whether 𝛾 is satisfied by a subheaplet or not.
   Intuitively, while (𝑠, ℎ) |= 𝛼 captures whether a formula holds on a heaplet or not, Supp(𝛼, 𝑠, ℎ)
being ⊥ or not captures whether the heaplet is large enough to evaluate 𝛼, and is crucial for the
semantics of the else branch of ite expressions.
FO-Complete Program Verification for Heap Logics                                                          13


    Π(𝛾) = 𝛾, for H.I. atomic formula 𝛾                              Π(𝑥 −𝑓 𝑦) = 𝑓 (𝑥) = 𝑦
Π(𝛼 ∗ 𝛽) = Π(𝛼) ∧ Π(𝛽) ∧ Sp(Π(𝛼)) ∩ Sp(Π(𝛽)) = ∅                       Π(𝛼 ∨ 𝛽) = Π(𝛼) ∨ Π(𝛽)
Π(𝛼 ∧ 𝛽) = Π(𝛼) ∧ Π(𝛽) ∧ Sp(Π(𝛼)) = Sp(Π(𝛽))                      Π(ite(𝛾, 𝛼, 𝛽)) = ite(𝛾, Π(𝛼), Π(𝛽))
 Π(𝛼∧∧𝛽) = Π(𝛼) ∧ Π(𝛽)                                      Π(∃𝑦.(𝑥 −𝑓 𝑦 : 𝛼)) = ∃𝑦 : 𝑦 = 𝑓 (𝑥). Π(𝛼)
                               Fig. 6. Translation from SL-FL𝑏∨ to Frame Logic
   Disjunction: The semantics of disjunctive formulas 𝛼 ∨ 𝛽 is quite different from traditional
semantics. Traditional semantics would declare this to hold if either 𝛼 or 𝛽 holds. But in a larger
heaplet ℎ, there could be both a heaplet where 𝛼 holds and one where 𝛽 holds, and hence this goes
against our desire to have unique heaplets for formulae. In our semantics, the support of such 𝛼 ∨ 𝛽
is considered to be the union of the supports of 𝛼 and 𝛽, and 𝛼 ∨ 𝛽 holds in this combined heaplet.
   The logic SL-FL𝑏∨ includes disjunction, but as we mentioned earlier, we did not see a true need
for disjunction in our experimental evaluation as most uses are expressible using ite expressions.
   Properties: The supports of formulas have several properties worth noting. Let 𝑆 be the support
of a formula with respect to a store and a heaplet ℎ, with 𝑆 ≠ ⊥. First, 𝑆 will be a subset of 𝑑𝑜𝑚(ℎ).
Second, consider a heaplet ℎ ′ that agrees with ℎ on 𝑆. Then the support of the formula with respect
to ℎ ′ will be 𝑆 as well. Third, the support of the formula with respect to ℎ restricted to 𝑆 will be 𝑆
itself. Finally, there is at most one subheaplet ℎ ′ of ℎ such that the support of the formula in ℎ ′ is
𝑑𝑜𝑚(ℎ ′ ) itself. The following lemma formalizes this (see Appendix D for a proof gist).
  Lemma 4.1. Let 𝑠 be a store and 𝛼 be a SL-FL𝑏∨ formula, ℎ be a heaplet, and let 𝑆 = Supp(𝛼, 𝑠, ℎ),
and 𝑆 ≠ ⊥.
   (1) 𝑆 ⊆ 𝑑𝑜𝑚(ℎ).
   (2) Let ℎ ′ be a heaplet such that 𝑆 ⊆ 𝑑𝑜𝑚(ℎ ′ ) and ℎ ′ ⇂ 𝑆 = ℎ ⇂ 𝑆. Then Supp(𝛼, 𝑠, ℎ ′ ) = 𝑆.
   (3) Supp(𝛼, 𝑠, ℎ ⇂ 𝑆) = 𝑆.
   (4) Let ℎ 1 and ℎ 2 be two sub-heaplets of ℎ and assume Supp(𝛼, 𝑠, ℎ 1 ) = 𝑑𝑜𝑚(ℎ 1 ) and Supp(𝛼, 𝑠, ℎ 2 ) =
       𝑑𝑜𝑚(ℎ 2 ). Then 𝑑𝑜𝑚(ℎ 1 ) = 𝑑𝑜𝑚(ℎ 2 ).                                                               □
   The above semantics ensures a crucial property— consider any store 𝑠, heap ℎ, and formula
𝛼, then there is at most one sub-heaplet ℎ ′ of ℎ that satisfies 𝛼 (namely ℎ ⇂ Supp(𝛼, 𝑠, ℎ)). This
property does not hold for standard separation logic semantics (see Appendix D for a proof gist).
  Lemma 4.2. Let 𝑠 be a store and ℎ a heaplet, and 𝛼 be an SL-FL𝑏∨ formula.
   (1) If (𝑠, ℎ) |= 𝛼, then Supp(𝛼, 𝑠, ℎ) = dom(ℎ).
   (2) There is at most one subheaplet ℎ ′ of ℎ such that (𝑠, ℎ ′ ) |= 𝛼.                                  □
Translation to Frame Logic
   SL-FL𝑏∨ formulas, with their semantics using determined heaplets/supports, can be readily trans-
lated to frame logic. The translation is given in Figure 6, and is simple and natural. The translation
preserves both truthhood as well as heaplet semantics in the following sense:
   Lemma 4.3. Let 𝑔 be a global heap (a heaplet with domain 𝐿𝑜𝑐) and 𝑠 be a store. For frame logic
formulas, we interpret the store as an FO interpretation of variables. Let 𝛼 be an SL-FL𝑏∨ formula. Then
    (1) 𝑔 |=𝑠 Π(𝛼) iff there exists a heaplet ℎ of 𝑔 such that (𝑠, ℎ) |= 𝛼.
    (2) If 𝑔 |=𝑠 Π(𝛼), then Supp(𝛼, 𝑠, 𝑔) is equal to the value of Sp(Π(𝛼)) in 𝑔.                      □
   The above allows us to build automatic verification procedures for programs annotated with
SL-FL𝑏 and SL-FL𝑏∨ formulas. Annotations with contracts using separation logic formulas can be
translated to Frame Logic, with the understanding that they define implicit heaplets which is the
support of the corresponding Frame Logic formula (see Appendix G for an example).
14                                                                                               Trovato et al.

 SL-FL Formulas 𝛼, 𝛼 ′, 𝛽            ≔ true | false | 𝑥 = 𝑦 | 𝑥 ≠ 𝑦 | 𝑥 = nil | 𝑥 ≠ nil | 𝑥 −𝑓 𝑦
                                                            ∧𝛽 | 𝛼 ∨ 𝛽 | ite(𝛼 ′, 𝛼, 𝛽) | ∃𝑦.(𝑥 −𝑓 𝑦 : 𝛼) | 𝑅(𝑥)
                                 | 𝑝 (𝑡) | 𝛼 ∗ 𝛽 | 𝛼 ∧ 𝛽 | 𝛼∧
            Terms     𝑡, 𝑡 ′, 𝑡𝑖     ≔ 𝑥 | 𝑡 .𝑓 | 𝑔(𝑡) | ite(𝛼, 𝑡, 𝑡 ′ ) | 𝐹 (𝑡)
         Rec. Defs:    𝑅(𝑥) :=lfp 𝜌 𝑅 (𝑥, R, F ), for each 𝑅 ∈ R
                        𝐹 (𝑥) :=lfp 𝜇𝐹 (𝑥, R, F ), for each 𝐹 ∈ F
Fig. 7. SL-FL: Syntax of full Separation Logic with Frame-Logic inspired semantics. The guards in ite expres-
sions should not mention recursively defined relations 𝑅 ∈ R
4.2 Extending the base logic to background sorts and recursive definitions
We now extend the base logic to a more powerful logic that (a) allows recursive definitions of
predicates and functions, and (b) incorporates background sorts (like arithmetic), pointer fields to
such sorts, and recursively defined functions that evaluate to the background sort.
   Let us fix background sorts, with accompanying functions and relations, G = {𝑔1, . . . , } and
P = {𝑝 1, . . . , }. Let us also fix a set of symbols for functions and relations, F and R, respectively,
which we will use to define new recursively-defined functions and relations. Heaplets are extended
to include pointers that map locations to background sorts.
   The syntax of SL-FL is given in Figure 7. The syntax for SL-FL formulas is similar to the base
logic, but we allow them to evaluate predicates over terms of background sorts (𝑝 (𝑡)), and allow
evaluation of recursively defined predicates (𝑅(𝑥)). The syntax for terms allows dereferencing
locations (resulting in either locations or background sort), computing functions over background
sorts (like + over integers), if-then-else constructs, or recursively defined functions that return
values of background sort (like "Keys" of a location 𝑥 pointing to a list).
   Recursively defined predicates (𝑅) and functions (𝐹 ) are defined with parameters of type location
only. This is a crucial restriction as we will, upon translation to Frame Logic and later to first-
order logic, treat these definitions as universally quantified equations, and it’s important for
FO-completeness using natural proofs that these quantifications are over the foreground sort
of locations only. Definitions of predicates (𝑅) and functions (𝐹 ) are mutually recursive and are
arbitrary SL-FL formulae 𝜌 and terms over background sorts 𝜇 that can mention R and F .
   The semantics of the logic extend that of the base logic in the natural way, and we skip the
formal semantics here (see Appendix E for some details). We assume that each background sort is a
complete lattice (for flat sorts like arithmetic, we can introduce a bottom element and a top element
to obtain a complete lattice). The support maps are extended for recursive definitions, and they
evaluate to the support of their definitions. The semantics of both Supp and |= are taken together
as equations and their semantics is defined as the least fixpoint of these equations.
   The separation logic that emerges is powerful and can state properties such as standard datastruc-
tures (lists, trees) and properties of them (keys, bst), etc. Furthermore, the logic can be translated
easily to FL (extending the Π translation above) for automated verification of programs annotated
using SL-FL (see Appendix E for some details).

5     Automating Program Verification for Frame Logic
In this section, we present the second technical contribution of this paper: a VC generation technique
for programs annotated in FL . To this extent, we extend FL with the ‘cloud’ operator, which enables
quantifier elimination. We then utilize strongest postconditions for VC generation. This avoids the
nightmarish formulas present in the weakest precondition computations in [43, 44].

5.1    Simplifying Quantification Using the Cloud Operator
In this work we wish to write quantifier-free specifications, generating quantifier-free verification
conditions in the 𝐿oneway fragment. However, defining something even as simple as linked lists in
FL requires quantification [43, 44]:
FO-Complete Program Verification for Heap Logics                                                                         15


                 List (𝑥) :=lfp ite(𝑥 = nil, ⊤, ∃𝑦 : 𝑦 = next (𝑥). List (𝑦) ∧ 𝑥 ∉ Sp(List (𝑦)))
where an existential quantifier is used in the above definition to say that when 𝑥 ≠ nil, then 𝑦, the
“next” location of 𝑥 must point to a linked list such that 𝑥 does not belong to the support of List (𝑦) 3 .
   It is tempting to think that the quantifier can be eliminated by simply replacing 𝑦 with next (𝑥).
However, the second conjunct then becomes 𝑥 ∉ Sp(List (next (𝑥))), which does not hold because
the support of a formula that mentions next (𝑥) always contains 𝑥 4 .
   In this work we introduce a new operator called the Cloud operator, denoted by square brackets
[·]. The cloud of a formula (resp. term) 𝛼 is a formula [𝛼] that evaluates the same way as 𝛼, but
whose support is empty. Simply, [𝛼] treats 𝛼 as a support-less expression. We extend FL with the
cloud operator, which allows us to rewrite the above definition without quantification:
    List (𝑥) :=lfp ite(𝑥 = nil, ⊤, next (𝑥) = next (𝑥) ∧ List ( [next (𝑥)]) ∧ 𝑥 ∉ Sp(List ( [next (𝑥)])))
where all occurrences of 𝑦 are replaced with [next (𝑥)]. We also add the tautological conjunct
next (𝑥) = next (𝑥) to ensure that the support of the resulting formula still contains {𝑥 }.
Formally, we define the semantics of the cloud operator as follows:
                             Sp( [𝜑]) = ∅ and 𝑀 |= [𝛼] iff 𝑀 |= 𝛼 for a formula 𝛼
                                  Sp( [𝑡]) = ∅ and J [𝑡] K𝑀 = J𝑡K𝑀 for a term 𝑡
   We then have the following lemma. Fix a model 𝑀.

   Lemma 5.1 (Eliminating Quantification using the Cloud Operator). 𝑀 |= ∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑
if and only if 𝑀 |= (𝑓 (𝑥) = 𝑓 (𝑥)) ∧ 𝜑 ( [𝑓 (𝑥)]), and JSp(∃𝑦 : 𝑦 = 𝑓 (𝑥). 𝜑)K𝑀 = JSp((𝑓 (𝑥) =
𝑓 (𝑥)) ∧ 𝜑 ( [𝑓 (𝑥)]))K𝑀                                                                      □

   We skip the proof of this lemma as it follows trivially from definitions.

  We now turn to VC generation for programs annotated with quantifier-free FL specifications, now
extended with the cloud operator. Note that the user continues to write specifications in FL with
guarded quantification as in Figure 1. These are eliminated automatically using the transformation
described in Lemma 5.1.
  We fix some notation. For a given program, we assume a fixed set of pointer and data fields
F𝑚 , and we use 𝑓 , 𝑓 ′, 𝑓1 , etc. to denote these. We also fix a finite set of recursive definitions I, and
symbols 𝐼, 𝐼 ′, 𝐼 1 , etc. range over I. We denote by Def the recursive definitions for each 𝐼 ∈ I, with
the definition of 𝐼 of the form 𝐼 (𝑥)  ® =lfp 𝜌 𝐼 (𝑥).
                                                   ® Definitions can be mutually recursive.
  Given a triple {Pre} 𝑃 {Post}, we fix a set of methods 𝐺 which are called by 𝑃. We assume every
𝑔 ∈ 𝐺 has its own contract with precondition Pre𝑔 and postcondition Post𝑔 . Our verification is
modular and therefore simply assumes the validity of triples for called methods.
  An illustrative example is given below. The program RevPrepend prepends the reverse of list
pointed to by 𝑥 to the list pointed to by 𝑦. The precondition asserts the two lists are disjoint. The
postcondition asserts the program returns a list ret whose keys is the union of the keys of the
two lists at the start of the program. We use Old (𝑅(𝑥)) to denote references to elements of the
appropriate background sort obtained by calculating 𝑅(𝑥) on the program state at the start of the
method call. In particular, the support of the expression Old (𝑅(𝑥)) is empty.


3 For readers familiar with separation logic, this formula is similar to the SL formula ∃𝑦. (𝑥 next
                                                                                               ↦→ 𝑦) ∗ List (𝑦)
4 The example shows that substitution is not a semantics-preserving operation in FL. Indeed, a substitution is only valid if

the replacement expression has the same truth value and the same support as the original substituted sub-expression.
16                                                                                                                                Trovato et al.

                                                                                          Program:
      Definitions and Specification:
                                                                                          RevPrepend(𝑥, 𝑦) returns(ret ):
      List (𝑥 ) := ite (𝑥 = nil, ⊤, List (next (𝑥 ) ) ∧ 𝑥 ∉ Sp (List ( [next (𝑥 ) ] ) )
                                                                                          (if (x = nil) then ret := y;
      Keys (𝑥 ) := ite (𝑥 = nil, 𝜙, Keys (next (𝑥 ) ) ∪ {key (𝑥 ) } )
                                                                                               else tmp := x.next; x.next := y;
      Pre: List (𝑥 ) ∧ List (𝑦) ∧ Sp (List (𝑥 ) ) ∩ Sp (List (𝑦) ) = 𝜙
                                                                                               ret := RevPrepend(tmp, x); )
      Post: List (ret ) ∧ Keys (ret ) = Old (Keys (𝑥 ) ) ∪ Old (Keys (𝑦) )
                                                                                          return;

5.2     Generating Triples over Basic Blocks
Given a program with annotations, we first generate several triples over basic blocks. These
generated triples capture both the verification of the postcondition for 𝑃 along different control
flows as well as other “side-conditions” such as memory safety of dereferences and deallocations.
   The basic blocks corresponding to a program 𝑃, denoted 𝐵𝐵(𝑃), are as follows:
      • 𝐵𝐵(𝑐) = {𝑐} for any atomic command 𝑐
      • 𝐵𝐵(if 𝜂 then 𝑃1 else 𝑃2 ) = {𝑎𝑠𝑠𝑢𝑚𝑒 (𝜂); 𝑃 1′ | 𝑃1′ ∈ 𝐵𝐵(𝑃1 )} ∪ {𝑎𝑠𝑠𝑢𝑚𝑒 (¬𝜂); 𝑃 2′ | 𝑃2′ ∈ 𝐵𝐵(𝑃2 )}
      • 𝐵𝐵(𝑃 1 ; 𝑃2 ) = {𝑃1′ ; 𝑃2′ | 𝑃1′ ∈ 𝐵𝐵(𝑃1 ), 𝑃2′ ∈ 𝐵𝐵(𝑃2 )}
   𝐵𝐵(𝑃) computes basic blocks in the usual manner, splitting paths on conditionals and including
the condition in conditionals using assume statements. Each basic block is assumed to be in “SSA
form”, i.e., every variable is assigned at most once. This is not a restriction as every basic block in
our language can be transformed into SSA form.
   Given a triple {Pre} 𝑃 {Post}, the set of triples associated with the basic blocks 𝐵𝐵(𝑃) are:
      • For each 𝑠 ∈ 𝐵𝐵(𝑃), {Pre} 𝑠 {Post}
      • For every 𝑠 1, 𝑠 2 , where 𝑠 1 ; 𝑥 := 𝑦.𝑓 ; 𝑠 2 or 𝑠 1 ; 𝑦.𝑓 := 𝑥; 𝑠 2 or 𝑠 1 ; free(𝑦); 𝑠 2 is in 𝐵𝐵(𝑃),
                                                   {Pre} 𝑠 1 {𝐻𝑃 : 𝑦 ∈ 𝐴}5
        where 𝐻𝑃 is Heapless Post (see Section 3.3).
      • For every 𝑠 1, 𝑠 2 such that 𝑠 1 ; 𝑏¯ := 𝑔(𝑎);
                                                     ¯ 𝑠 2 ∈ 𝐵𝐵(𝑃),
                                                {Pre} 𝑠 1 {𝑅𝑃 : Pre𝑔 [𝑝¯ ← 𝑎]}   ¯
        where 𝑅𝑃 is Relaxed Post (see Section 3.3).
   The first item above includes the verification of the postcondition of the program along every
basic block. The second set of Hoare triples captures safety of dereferences and ensures freed
locations are currently allocated. For each statement that dereferences a location variable or frees a
location, we add a Hoare triple for the prefix of the basic block till that statement and check using
relaxed postcondition that the variable is in the current allocated set. Finally, for each statement
that calls a method 𝑔, we introduce a prefix of the basic block till the call and check, again using a
relaxed postcondition, that the precondition of the called method holds. The relaxed postcondition
above ensures that the heaplet which is the support of the precondition of 𝑔, 𝑃𝑟𝑒𝑔 (which 𝑔 will
remain within) is a subset of the currently allocated set.
   One can think of generating the triples for BBs as stepping through the program one command
at a time and discharging necessary obligations. Let us consider the ’else’ branch of the illustrative
example. Assuming 𝑥 ≠ nil, we first check if dereferencing 𝑥 is safe when assigning 𝑥 .next to tmp
with the top-left Hoare triple in Figure 8. The case for the mutation 𝑥 .next to tmp is similar. Next,
we require the precondition for 𝑅𝑒𝑣𝑃𝑟𝑒𝑝𝑒𝑛𝑑 to hold on the method call, i.e., with inputs tmp, 𝑥.
Moreover, we also ensure its support is contained in the allocated set. We treat the support of the
precondition to the call as the set of modified locations for the function call. This is captured by the
top-right Hoare triple in Figure 8. Finally, we check that the post-condition holds at the end of the
program by the bottom triple in Figure 8.
5 Later in this section, we will show that the allocated set 𝐴 can be represented as an FL formula. Thus, checks such as

𝑦 ∈ 𝐴 can be captured in FL.
FO-Complete Program Verification for Heap Logics                                                                                     17

 {List (𝑥 ) ∧ List (𝑦) ∧ Sp (List (𝑥 ) ) ∩ Sp (List (𝑦) ) = 𝜙 }       {List (𝑥 ) ∧ List (𝑦) ∧ Sp (List (𝑥 ) ) ∩ Sp (List (𝑦) ) = 𝜙 }
              assume (𝑥 ≠ nil); tmp := 𝑥 .next                               assume (𝑥 ≠ nil); tmp := 𝑥 .next; 𝑥 .next := 𝑦
                       {𝐻 𝑃 : 𝑥 ∈ 𝐴}                              {𝑅𝑃 : List (tmp) ∧ List (𝑥 ) ∧ Sp (List (tmp) ) ∩ Sp (List (𝑥 ) ) = 𝜙 }
                                     {List (𝑥 ) ∧ List (𝑦) ∧ Sp (List (𝑥 ) ) ∩ Sp (List (𝑦) ) = 𝜙 }
                                           assume (𝑥 ≠ nil); tmp := 𝑥 .next; 𝑥 .next := 𝑦;
                                                    ret := RevPrepend(tmp, 𝑥 )
                                   {List (ret ) ∧ Keys (ret ) = Old (Keys (𝑥 ) ) ∪ Old (Keys (𝑦) ) }

                 Fig. 8. Hoare Triples generated for the ‘else’ branch in the illustrative example.


5.3    Verification Condition Generation
We present the core technical contribution in this section, a verification condition (VC) generation
mechanism for basic blocks. We generate verification conditions in frame logic with only universal
quantification over locations (for satisfiability) and with functions mapping from the foreground
sort to the foreground or background sorts (integers, sets of locations, etc.).
    Intuitively, we will be constructing, for each Hoare triple {Pre} 𝑠 {Post} a VC of the form ((Pre ∧
𝑇 ) ⇒ Post) ∧𝑆𝐶 where 𝑇 captures the semantics of transformation the basic block 𝑠 has on the state
and heap, and 𝑆𝐶 is a support condition that demands that the support of {𝑃𝑜𝑠𝑡 } is the support of
Pre modulo allocations and freeing of locations that happen in 𝑠 (including calls to other functions).
In the case of Hoare triples with relaxed postconditions {Pre} 𝑠 {𝑅𝑃 : Post}, the VC is similar, except
that the support condition will demand that the support of the postcondition is a subset of the
support of the precondition, modulo allocations and freeing of locations. Heapless postconditions
{Pre} 𝑠 {𝐻𝑃 : Post} simply do not have a support condition.
    Consider a Hoare triple {𝛼 } 𝑠 {𝛽} where 𝑠 is a basic block and where 𝛼, 𝛽 are annotations in frame
logic. We use the notion of a local configuration to build the VC. We describe a transformation of
local configurations across statements of a basic block, processing one statement of the basic block
at a time, left to right. A local configuration is a 5-tuple (𝑇 , 𝐴, 𝐻, Fr, RD). After processing a prefix
𝑠 ′ of a basic block 𝑠, 𝑇 corresponds to the formula describing the state after the transformation
𝑠 ′ has had on states satisfying the precondition. The component 𝐴 represents the set of allocated
locations after the prefix, 𝐻 represents the heap after executing the prefix, and Fr stands for a set of
frame rules gathered during mutations of the heap by the prefix. Finally, RD represents a set of new
recursive definitions gathered to represent the recursive definitions I evaluated on intermediate
heaps during the execution of the prefix 𝑠 ′ .
    Initially, 𝑇 is set to Pre and 𝐴 is set to the support of the precondition 𝛼 of the Hoare triple, i.e.,
Sp(𝛼), 𝐻 is initially simply a set of uninterpreted functions denoting the initial heap, and Fr is the
empty set. The set RD is initialized to D, the recursive definitions of I on the initial heap. Formally:

  Definition 5.2. A logical configuration is a tuple (𝑇 , 𝐴, 𝐻, Fr, RD) where:
      • 𝑇 is a quantifier-free logical formula describing the program transformation. 𝑇 is expressed
        over program variables and recursive functions defined in RD
      • 𝐴 is a term whose type is a set of locations, and denotes the current allocated set of locations.
      • 𝐻 is a map that captures the current heap; it associates with each pointer 𝑓 ∈ 𝐹 a map
                     − 𝜎 ′ , where 𝜎 ′ is the foreground sort of Locations or a background sort. 𝐻 (𝑓 )
        𝐻 (𝑓 ) : 𝐿𝑜𝑐 →
        is expressed as 𝜆𝑢.𝑡 (𝑢), where 𝑡 is a term over 𝑢 and the program variables.
      • Fr is a set of universally quantified FO formulae that denotes a set of frame rules gathered
        for each mutation of the heap.
      • RD is a set of recursive definitions of a set of function symbols that capture properties/data
        structures of intermediate heaps.
18                                                                                             Trovato et al.


   The heap map 𝐻 associates with each pointer 𝑓 ∈ 𝐹 , a map 𝐻 (𝑓 ), that maps locations to the
appropriate sort (either location sort or a background sort). Note that these hence satisfy the
one-way condition we want for FO-completeness. The map 𝐻 (𝑓 ) is itself expressed in logic using
quantifier-free terms involving other function symbols, such as the functions that characterize the
initial heaplet. For example, 𝐻 (𝑓 ) may be the formula 𝜆𝑢.𝑖𝑡𝑒 (𝑢 = 𝑧, 𝑔1 (𝑧), 𝑔2 (𝑢)), where 𝑔1, 𝑔2 are
function symbols and 𝑧 is a program variable. In general, we will expand the signature with new
function symbols as we process a basic block.
   We start with a set of recursive definitions for function symbols in I. As we construct the VC,
we adapt these definitions of functions in I to ones that refer to them interpreted on new heaps.
   In particular, for any 𝐻 and 𝐼 ∈ I, let us introduce a new function symbol 𝐼𝐻 , and let us add a
recursive definition for 𝐼𝐻 . This recursive definition 𝐼 [𝐻 ] is the definition for 𝐼 where every pointer
and data field 𝑓 ∈ F𝑚 mentioned in the recursive definition is replaced by 𝐻 (𝑓 ). In other words, for
each recursively defined function 𝐼 ∈ I, where 𝐼 is defined as 𝐼 (𝑥) =lfp 𝜌 (𝑥), we give a definition
𝐼 [𝐻 ] : 𝐼𝐻 (𝑥) =lfp 𝜌 [𝐻 (𝑓 )/𝑓 ] (𝑥), where 𝜌 [𝐻 (𝑓 )/𝑓 ] is 𝜌 where every occurrence of 𝑓 is replaced
with the term 𝐻 (𝑓 ), for each 𝑓 ∈ F𝑚 .
   For example, consider the example of 𝐻 mentioned above, and consider the definition lseg(𝑥, 𝑦) =lfp
(𝑥 = 𝑦)∨lseg(𝑓 (𝑥), 𝑦). Then lseg[𝐻 ] is the definition lseg𝐻 =lfp (𝑥 = 𝑦)∨lseg(ite(𝑥 = 𝑧, 𝑔1 (𝑧), 𝑔2 (𝑥)), 𝑦).
   The generation of VCs are presented in Figure 9. However, before diving into explaining the
rules, let us discuss the frame rule (formally also described in Figure 9) that is used in the rules.
                                                                 ® ∈ I, two heap maps 𝐻 , 𝐻 ′ ,
Frame conditions: For any recursively defined function symbol 𝐼 (𝑦)
and a set of locations 𝑋 , we define the frame rule to be
               fr(𝐼, 𝑋, 𝐻, 𝐻 ′ ) : ∀®
                                    𝑦 ∈ 𝐿𝑜𝑐, (𝑋 ∩ Sp(𝐼𝐻 (𝑦))
                                                         ® = ∅) =⇒ (𝐼𝐻 ′ (𝑦)
                                                                          ® = 𝐼𝐻 (𝑦))
                                                                                  ®
   The above formula is meant to be used when a heap 𝐻 is transformed to a heap 𝐻 ′ where
mutations happen only on the locations in 𝑋 . It says that if the support of the recursive definition
on 𝑦® (evaluated in 𝐻 ) does not intersect 𝑋 , its value in 𝐻 ′ is the same as that in 𝐻 . Note that this
formula has only universal quantification over the foreground sort of locations, and hence its
translation to FORD will be in the 𝐿oneway fragment.
   We use fr(𝑋, 𝐻, 𝐻 ′ ) to denote the conjunction of fr(𝐼, 𝑋, 𝐻, 𝐻 ′ ), for each 𝐼 ∈ I, which states the
frame condition for each recursively defined function in I.
Verification Condition Generator:
  Definition 5.3 (VC for a basic block). For Hoare triples of basic blocks {𝛼 } 𝑠 {𝛽} and for basic
blocks with relaxed post, the associated VCs are defined as:
                                           Û        
                        VC ({𝛼 } 𝑠 {𝛽}) =     Fr ∧ 𝑇 ⇒ (𝛽 ∧ Sp(𝛽) = 𝐴)
                                             Û        
                      VC ({𝛼 } 𝑠 {𝑅𝑃 : 𝛽}) =     Fr ∧ 𝑇 ⇒ (𝛽 ∧ Sp(𝛽) ⊆ 𝐴)
                                                    Û        
                            VC ({𝛼 } 𝑠 {𝐻𝑃 : 𝛽}) =      Fr ∧ 𝑇 ⇒ (𝛽)
where (𝑇 , 𝐴, 𝐻, Fr, RD) = VC ((𝑇0, 𝐴0, 𝐻 0, Fr0, RD0 ), 𝑠) where 𝑇0 = 𝛼, 𝐴0 = Sp(𝛼), 𝐻 0 (𝑓 ) = 𝜆𝑢.𝑓 (𝑢)
(for each 𝑓 ∈ 𝐹 ), Fr0 = ∅, RD0 = RD, and VC is the transformer defined formally in Figure 9.
  We now give the intuition behind the transformer VC. For an assignment x := y (Assn), we just
add the condition 𝑥 = 𝑦 as a conjunct to our transformation formula. Recall that we have assumed
that the basic block is in SSA form, and this is the sole assignment to the variable 𝑥, and hence
this conjunct captures the program configuration constraining 𝑥 and 𝑦 to be equal. The scalar
assignment rule (SclrAssn) for assigning variables of background sorts is similar.
FO-Complete Program Verification for Heap Logics                                                                               19


                 𝑇 ′ = 𝑇 ∧ (𝑥 = 𝑦)                                          𝑇 ′ = 𝑇 ∧ (𝑣 = be)
                             ′
                                                 Assn                                                      SclrAssn
       VC(𝜎, 𝑥 ≔ 𝑦) = (𝑇 , 𝐴, 𝐻, Fr, RD)                           VC(𝜎, 𝑣 ≔ be) = (𝑇 ′, 𝐴, 𝐻, Fr, RD)

                                              𝑇 ′ = 𝑇 ∧ (𝑥 = 𝐻 (𝑓 )(𝑦))
                                                                                     Deref
                                        VC(𝜎, 𝑥 ≔ 𝑦.𝑓 ) = (𝑇 ′, 𝐴, 𝐻, Fr, RD)

                𝐻 ′ (𝑓 ) = 𝜆arg. 𝑖𝑡𝑒 (arg = 𝑦, 𝑥, 𝐻 (𝑓 )(arg)) for every 𝑓 ′ ∈ F𝑚 , 𝑓 ′ ≠ 𝑓
                     Fr ′ = Fr ∪ {fr ({𝑦}, 𝐻, 𝐻 ′ )}    RD ′ = RD ∪ {𝐼 [𝐻 ′ ] | 𝐼 ∈ I}
                                                                                                  Mutation
                                     VC(𝜎, 𝑦.𝑓 ≔ 𝑥) = (𝑇 , 𝐴, 𝐻 ′, Fr ′, RD ′ )

                                   𝑇 ′ = 𝑇 ∧ (𝑥 ∉ 𝐴)        𝐴′ = 𝐴 ∪ {𝑥 }
        𝐻 ′ (𝑓 ) = 𝜆arg. ite(arg = 𝑥, default 𝑓 , 𝐻 (𝑓 )(arg)), for every 𝑓 ∈ F𝑚 , with domain 𝐴′
                                       RD ′ = RD ∪ {𝐼 [𝐻 ′ ] | 𝐼 ∈ I}
                                                                                                             Alloc
                                       VC(𝜎, alloc(𝑥)) = (𝑇 ′, 𝐴′, 𝐻 ′, Fr, RD ′ )

  𝐴′ = 𝐴\{𝑥 }       𝐻 ′ (𝑓 ) = 𝐻 (𝑓 ) for every 𝑓 ∈ F𝑚 , with domain 𝐴′                RD ′ = RD ∪ {𝐼 [𝐻 ′ ] | 𝐼 ∈ I}
                                                                                                                        Free
                                         VC(𝜎, free(𝑥)) = (𝑇 , 𝐴′, 𝐻 ′, Fr, RD ′ )

              VC(𝜎, 𝑃) = 𝜎 ′                                                      𝑇′ =𝑇 ∧ 𝛼
                                 ′
                                         SeqComp                                                            Assume
        VC(𝜎, 𝑃; 𝑄) = VC(𝜎 , 𝑄)                                 VC(𝜎, assume(𝛼)) = (𝑇 ′, 𝐴, 𝐻, Fr, RD)

                                            𝑔∈𝐺            ¯ = Pre(𝑔)
                                                       𝛼 (𝑥)
            ¯ 𝑦)
        𝛽 (𝑥, ¯ = Post (𝑔)       𝐻 ′ (𝑓 ) = 𝜆arg. ite(arg ∈ Sp(𝛼𝐻 [𝑥¯ ← 𝑎]), ¯ 𝑓fresh (arg), 𝐻 (𝑓 )(arg))
        𝑇 ′ = 𝑇 ∧ 𝛽𝐻 ′ [𝑥¯ ← 𝑎,
                             ¯ 𝑦¯ ← 𝑏] ¯      𝐴′ = (𝐴 \ Sp(𝛼 𝐻 [𝑥¯ ← 𝑎]))¯ ∪ Sp(𝛽𝐻 ′ [𝑥¯ ← 𝑎,         ¯
                                                                                              ¯ 𝑦¯ ← 𝑏])
                   ′                                     ′             ′               ′
                 Fr = Fr ∪ { fr (Sp(𝛼 𝐻 [𝑥¯ ← 𝑎]),
                                                ¯ 𝐻, 𝐻 ) }        RD = RD ∪ {𝐼 [𝐻 ] | 𝐼 ∈ I}
                                                                                                          Call
                                   VC(𝜎, 𝑏¯ ≔ 𝑔(𝑎))¯ = (𝑇 ′, 𝐴′, 𝐻 ′, Fr ′, RD ′ )

Fig. 9. Verification Condition Generation: Predicate transformers for basic blocks. Here 𝜎 = (𝑇 , 𝐴, 𝐻, Fr, RD),
the configuration before applying the VC transformer, and fr (𝑋, 𝐻, 𝐻 ′ ) = 𝐼 ∈ I fr (𝐼, 𝑋, 𝐻, 𝐻 ′ ). We also assume
                                                                           Ó
a (fixed) set of callable functions 𝐺. Each function 𝑔 ∈ 𝐺 is annotated with precondition Pre(𝑔) = 𝛼 (𝑥)       ¯ and
postcondition Post (𝑔) = 𝛽 (𝑥,¯ 𝑦).
                                 ¯ By 𝛼 𝐻 , we mean 𝛼 where each 𝑓 ∈ F𝑚 is replaced by 𝐻 (𝑓 ) and each 𝐼 ∈ I
by 𝐼𝐻 . By 𝑓fresh , we mean a fresh function symbol with the signature of 𝑓 .


   For a dereference x := y.f (Deref), the transformation looks up the current pointer 𝑓 , using
the function 𝐻 (𝑓 ), and adds the conjunct that equates 𝑥 to 𝐻 (𝑓 ) (𝑦). Note that 𝐻 (𝑓 ) (𝑦) is the
formula 𝐻 (𝑓 ) with 𝑦 substituted as its parameter, and hence results in a quantifier-free term of the
appropriate type. The Assn and Deref rules only change the transformation formula, and the rules
for assume (Assume) and sequential composition (SeqComp) are as expected.
   For a Mutation y.f := x, the transformation component doesn’t change, but the heap is updated
to reflect the mutation, where 𝐻 ′ (𝑓 ) (𝑦) = 𝑥 and is 𝐻 (𝑓 ) on other locations. We also introduce the
recursive definitions for I adjusted for the current heap 𝐻 ′ (adding them to RD′ ). And introduce
frame rules fr({𝑦}, 𝐻, 𝐻 ′ ) that set these new recursive definitions on any tuple to the value of old
ones provided that 𝑦 does not belong to the support of these definitions on the tuple.
   For a function call (Call), we introduce an elegant way to take care of the heap transformation.
For each pointer and data field 𝑓 ∈ F𝑚 , we introduce a fresh function symbol 𝑓fresh . The map
𝐻 ′ (𝑓 ) is now an 𝑖𝑡𝑒 (if-then-else) term, where 𝐻 ′ (𝑓 ) (𝑢) evaluates to 𝐻 (𝑓 ) (𝑢), which is the old
value of the pointer 𝑓 , provided 𝑢 does not belong to the support of the precondition of the called
function 𝑔. Otherwise, 𝐻 (𝑓 ) (𝑢) evaluates to 𝑓fresh (𝑢), which is an arbitrary value since 𝑓fresh is
20                                                                                                                           Trovato et al.


uninterpreted. The transformation component imbibes the postcondition guaranteed by the call
to 𝑔, where the recursively defined functions 𝑅 in the postcondition are modified to the functions
𝑅𝐻 ′ . Recursive definitions are adapted to the new heap 𝐻 ′ after the call and added to RD′ . The
new allocated set is derived from the old allocated set by removing the locations in the support of
the precondition of 𝑔 and adding back the locations in the support of the postcondition of 𝑔. This
handles the locations 𝑔 may allocate or free during its execution. Finally, we add frame condition
formulae fr(𝑆𝑝 (𝛼 [𝑥¯ ← 𝑎]),¯ 𝑀, 𝑀 ′ ) that says that for any recursive definition that has an empty
intersection with the support of the precondition of 𝑔 remains unaffected in the new heap.
   The transformation for alloc statement (Alloc) adds an assumption that the allocated location
is not already present in the current allocated set 𝐴, adds it to the new allocated set, and updates
the heap map so that the new location’s pointers point to default values. The transformation for
free statements (Free) simply removes the location 𝑥 from the allocated set. Even though logical
expression for the heap function 𝐻 does not change with freeing of locations, its domain does.
Hence, when either allocation or free happens, we recompute the recursive definitions on the new
heap by updating the RD component. Note that we do not check whether freed locations are indeed
allocated as those are checked on other basic blocks, as described in the previous subsection.
   The algorithm applied to the bottom triple of Figure 8 is given below. The text in black is
the triple to be proven. The text in green shows the changes to the logical configuration. The
first two statements simply add the appropriate term to the program transformation. For the
mutation 𝑥 .next := 𝑦, we update the heap 𝐻 to 𝐻 1 reflecting this change. We then define the
recursive functions on the new heap. Finally, we add frame rules relating recursive functions
over 𝐻 to those over 𝐻 1 . The function call ret := RevPrepend(tmp, 𝑥) employs a similar idea.
First, we must update the heap. We know the portion of the heap modified by the call is the
support of the precondition for the call, i.e Sp(𝛼𝐻1 (tmp, 𝑥)). Thus, the new heap 𝐻 2 will only
differ outside of 𝐻 1 . Furthermore, the postcondition 𝛽𝐻2 (tmp, 𝑥, ret) for the call holds on the new
heap. The new allocated set is the portion not modified by the call union the support of the
postcondition the call. Finally, we add a frame rule connecting the heaps 𝐻 1 and 𝐻 2 . The VC
generated for this BB is (fr (𝑥, 𝐻, 𝐻 1 ) ∧ fr (Sp(𝛼 𝐻1 (tmp, 𝑥)), 𝐻 1, 𝐻 2 ) ∧ 𝑇2 ) =⇒ 𝜑 ∧ Sp(𝜑) = 𝐴2 ,
where 𝜑 = List 2 (ret) ∧ (Keys2 (ret) = (Old (Keys(𝑥)) ∪ Old (Keys(𝑦)))).
{List (𝑥 ) ∧ List (𝑦) ∧ (Sp (List (𝑥 ) ) ∩ Sp (List (𝑦) ) = 𝜙 ) }
 assume (𝑥 ≠ nil);                  # 𝑇 ← 𝑇 ∧ (𝑥 ≠ nil)
 tmp := 𝑥 .next;                    # 𝑇 ← 𝑇 ∧ (tmp = next (𝑥 ) )
 𝑥 .next := 𝑦;                      # 𝐻 1 = 𝐻 [next ← 𝜆arg. ite (arg = 𝑥, 𝑦, next (arg) ) ]
                                    # List 1 = List [𝐻 1 ], Keys1 = Keys[𝐻 1 ], RD1 = {List, Keys, List 1 , Keys1 }
                                    # Fr 1 = {fr (𝑥, 𝐻, 𝐻 1 ) }
 ret := RevPrepend(tmp, 𝑥 ) # 𝛼 𝐻1 (tmp, 𝑥 ) = (List 1 (tmp) ∧ List 1 (𝑥 ) ∧ Sp (List 1 (tmp) ) ∩ Sp (List 1 (𝑥 ) ) = 𝜙 )
                                    # 𝐻 2 [ 𝑓 ] = 𝜆arg.ite (arg ∉ Sp (𝛼 𝐻1 (tmp, 𝑥 ) ), 𝐻 1 ( 𝑓 ) (arg), next 2 (arg) ) for 𝑓 ∈ {next, key }.
                                    # List 2 = List [𝐻 2 ], Keys1 = Keys[𝐻 2 ], RD2 = RD1 ∪ {List 2 , Keys2 }
                                    # 𝛽𝐻2 (tmp, 𝑥, ret ) = (List 2 (ret ) ∧ Keys2 (ret ) = Old (Keys1 (tmp) ) ∪ Old (Keys1 (𝑥 ) ) )
                                    # 𝑇2 = 𝑇 ∧ 𝛽𝐻2 (tmp, 𝑥, ret )
                                    # 𝐴2 = (𝐴\Sp (𝛼 𝐻1 (tmp, 𝑥 ) ) ) ∪ Sp (𝛽𝐻2 (tmp, 𝑥, ret ) )
                                    # Fr 2 = Fr 1 ∪ {fr (Sp (𝛼𝐻1 (tmp, 𝑥 ) ), 𝐻 1 , 𝐻 2 ) }
{List 2 (ret ) ∧ Keys2 (ret ) = (Old (Keys (𝑥 ) ) ∪ Old (Keys (𝑦) ) }

  Soundness and Completeness. Our VC generation is sound and complete for the validity of Hoare
Triples over basic blocks. Fix a triple {𝛼 } 𝑠 {𝛽} where 𝑠 is a basic block, and let VC be the map
defined in Definition 5.3. Then:
   Theorem 5.4 (Soundness of VC Generation for Basic Blocks). If VC ({𝛼 } 𝑠 {𝛽}) is a valid
formula in Frame Logic then {𝛼 } 𝑠 {𝛽} is valid in the sense of Definition 3.1. Similarly, if VC ({𝛼 } 𝑠 {𝑅𝑃 :
𝛽}) is valid in Frame Logic then the triple {𝛼 } 𝑠 {𝑅𝑃 : 𝛽}) is valid.
FO-Complete Program Verification for Heap Logics                                                            21


   Theorem 5.5 (Completeness of VC Generation for Call-Free Basic Blocks). Let 𝑠 be a basic
block with no function calls. If {𝛼 } 𝑠 {𝛽} is valid (Definition 3.1) then VC ({𝛼 } 𝑠 {𝛽}) is valid. Similarly,
if {𝛼 } 𝑠 {𝑅𝑃 : 𝛽}) is valid then VC ({𝛼 } 𝑠 {𝑅𝑃 : 𝛽}) is valid.

   We elide the proofs of these theorems as they are fairly straightforward from the definition
of the VC transformer and the operational semantics (Appendix B). The key argument in the
proof of completeness is that we model mutations precisely using updates to the heap map 𝐻 .
Similarly, allocation and deallocation are also modeled precisely using the symbolic allocated set 𝐴,
which corresponds to the true allocated set as defined by the operational semantics for call-free
blocks. Though the above theorem does not include function calls, our VC is also precise for basic
blocks with function calls, with respect to a modular operational semantics, where function calls are
assumed to havoc the precondition’s heaplet and replace it with one that satisfies the postcondition.
   Our result is interesting in its own right, and showcases the power of our framework. Contempo-
rary works on VC generation for other logics such as Separation Logic are often not complete [7].

5.4    Validating Verification Conditions
In previous sections we described how we reduce validity of Hoare triples annotated with quantifier-
free FL formulas to the validity of FL formulas. We then reason with the generated VCs in FL by
(a) translating them to equi-valid FORD formulas, and (b) using natural proofs, an FO-complete
automation technique developed in prior work [38, 54, 59] for checking validity of FORD formulas
in the 𝐿oneway fragment. Natural proofs is based on systematic quantifier instantiation and SMT
solving. The translation from FL to FORD in the first stage follows a construction similar to the
one developed in earlier works on FL [43, 44], but we take some additional care to extend the
translation to handle the cloud operator and to ensure that the translations of our VCs fall into
𝐿oneway . Intuitively, the translation encodes the semantics of the Sp(·) and [·] operators in FORD
itself. We describe both stages in detail in Appendix F.

6     Implementation and Evaluation
6.1    Implementation
We develop the Frame Logic Verifier (FLV) tool based on the mechanism described in Sections 5
and 5.4. The tool allows users to write heap-manipulating programs and annotations in quantifier-
free Frame Logic, using the support Sp(·) and cloud [·] operators. The tool also allows users to write
inductive lemmas which are proven automatically using a form of induction using pre-fixpoints [38].
   The FLV tool generates VCs that are translated to FORD. These quantifier-free FORD formulas
are then validated using an existing solver for natural proofs [41] which implements the proce-
dure described in Section F.2, instantiating recursive definitions and reasoning with the resulting
quantifier-free formulas using Z3 [15].
   The implementation is also optimized in several ways. First, we introduce new recursive defini-
tions and frame rules only at certain key points— before and after function calls, and at the end
of a basic block. Note that the formulation in Section 5 introduces them across every mutation,
allocation, deallocation, and function call (as described in Section 5). These optimized frame rules
‘batch’ the individual mutations, catering to the footprint of the program between the key points.
Second, the tool starts off with a thrifty set of instantiations commonly needed, based on previous
work on natural proofs( [54]): recursive definitions and lemmas are instantiated on the relevant
footprint from the last key point, and frame rules are instantiated on the current variables and one
level of pointer dereferences on them before and after function calls and at the end of the basic
block. Finally, we use an SMT solver to simplify the translations to FORD before validating them.
22                                                                                              Trovato et al.


   We develop the SL-FL verifier (SLFLV) on top of FLV. This tool takes programs annotated with
SL-FL sepcfications. SLFLV translates these to programs with FL annotations (see Figure 6) and the
resulting program is verified by FLV.
   The translation from SL-FL to FL incurs some translation bloat in formula size. We develop an
optimized version of the tool that controls this bloat, especially in nested conjunctions. First, while
translating SL-FL formulas to FL formulas bottom-up, we compute, for every SL-FL subformula 𝛼,
a simple formula FL formula 𝛼 † such that Sp(Π(𝛼)) = Sp(𝛼 † ), and whenever we need to use the
support of Π(𝛼), we use the support of 𝛼 † instead. In particular, for 𝛼 = 𝛽 ∧𝛾, we take 𝛼 † to be simply
𝛽 † (as the translation independently constrains Sp(𝛽 † ) = Sp(𝛾 † )). Second, we syntactically track
subformulas whose support is empty, and remove constraints that check whether the intersection
with these supports is empty. We evaluate the effect of these optimizations in our evaluation.

6.2   Benchmark Suite
We evaluate the expressiveness and performance of our contributions on a suite of data structure
programs. Each program is annotated separately with FL and SL-FL specifications. Our suite consists
of 29 programs involving operations on data structures such as singly and doubly linked lists, circular
lists, binary search trees, red-black trees, treaps, etc. We obtained this suite by distilling a core set of
benchmarks from prior work [54]. We considered the various crucial data structure manipulation
algorithms for each structure such as insertion, deletion, search, sorting, and traversals. A summary
of our benchmark suite can be found in Appendix G, along with examples of specifications, lemmas
used, and an illustrative example of the VC generation.

6.2.1 Specifications. We annotate our programs with complete functional specifications. The
contracts specify precisely the data structure returned and its content in terms of the effect the
routine has on the input data structures and parameters. We define data structures and various
measures over them using recursive definitions and write specifications using them. To aid in
writing post-conditions, we introduce an Old operator. For a recursive function 𝑅, Old (𝑅(𝑥)) is
equivalent to assuming 𝑟 𝑥 = 𝑅(𝑥) at the beginning of a program for a fresh variable 𝑟 𝑥 and using
that in place of Old (𝑅(𝑥)). In particular, this means that Sp(𝑂𝑙𝑑 (𝑅(𝑥))) is empty as it is simply
syntactic sugar for a variable.

6.2.2 Lemmas. Though our procedures are FO-complete, i.e guaranteed to validate VCs when they
are valid with respect to fixpoint interpretations of definitons, there is a gap between this semantics
and the least fixpoint semantics of recursive definitions [38]. This gap is bridged using user given
inductive lemmas. Inductive lemmas are expected to be proved using a simple induction where the
lemma itself acts as the induction hypothesis, and using a first-order proof without least fixpoint
interpretations (see [38, 54, 59]).
   Lemmas are typically required to relate different properties of a data structure, and are typically
independent of the methods that work on the data structures (e.g., a sorted list is a singly linked
list).
   Our tools prove these lemmas using induction and natural proofs, and utilize the proven lemmas
while proving verification conditions. Lemmas for benchmarks are currently written in frame logic.
However, we can facilitate writing lemmas in SL-FL as well, where we interpret an entailment
𝛼 |= 𝛽 as Π(𝛼) =⇒ Π(𝛽) ∧ 𝑆𝑝 (Π(𝛼)) = 𝑆𝑝 (Π(𝛽)).
   Note that there has been a lot of orthogonal work that has addressed the problem of automatically
synthesizing these lemmas, both for functional and imperative programs, with considerable success
(incomplete, of course). See [34, 41, 42, 60, 63, 73].
FO-Complete Program Verification for Heap Logics                                                                     23


 Data         Benchmark             Number of             Number of    FL Verif.   SL-FL Verif. Time    SL-FL Verif. Time
 Structure                         Basic Blocks    Permission Checks      Time        (unoptimized)           (optimized)
              Append                          2                    5         1s                    1s                   1s
              Copy All                        2                    6         1s                    1s                   1s
              Delete                          3                    9         1s                    1s                   1s
              Find                            3                    5         1s                    1s                   1s
              Insert Back                     2                    7         1s                    1s                   1s
 SLL
              Insert Front                    1                    3         1s                    1s                   1s
              Reverse                         3                    7         1s                    1s                   1s
              Insertion Sort                  5                   14         3s                    4s                   3s
              Merge Sort                     10                   26         6s                    7s                   6s
              Quick Sort                      9                   25        13s                   18s                  15s
              Insert Back                     2                    9         1s                    1s                   1s
              Insert Front                    2                    8         1s                    1s                   1s
 DLL
              Delete Mid                      4                   11         2s                    3s                   3s
              Insert Mid                      4                   10         2s                    3s                   3s
              Delete                          3                    9         1s                    1s                   1s
 Sorted
              Find                            4                    6         1s                    1s                   1s
 List
              Insert                          3                   10         2s                    3s                   3s
              Delete Front                    5                   12         6s                    6s                   6s
 CL           Find                            6                   10         2s                    3s                   3s
              Insert Front                    2                    6         2s                    2s                   2s
              Delete                          8                   27         8s                   11s                  10s
              Find                            4                    8         2s                    2s                   2s
 BST
              Insert                          4                   13         3s                    4s                   4s
              Rotate Right                    1                    5         1s                    1s                   1s
 Tree         BST to List                     3                   11        15s                   22s                  19s
 Traversals   In-Order Traversal              2                    8         3s                    7s                   8s
              Delete                          9                   32        18s                   24s                  20s
 Treap
              Find                            4                    8         3s                    3s                   3s
 RBT          Insert                         11                   83        42s                1m 6s                   56s
Table 1. Performance of verifications tools (SLL = Singly-Linked List, DLL = Doubly-Linked List, CL = Circular
List, BST = Binary Search Tree, RBT = Red-Black Tree).
6.2.3 Definitions that have the same supports. The user is also allowed to declare that the supports
of a pair of recursive definitions is equal. For example, over trees, the support of BST , Keys, Min,
Max, Height are all the same. The tool proves this property (treating this as an inductive lemma)
and cuts down on the number of recursive definitions of supports, which in turn leads to better
performance.
6.3    Evaluation
We evaluate our tool on our suite of benchmarks. The experiments were performed on a MacBook
Pro (Mac14,9) equipped with an Apple M2 Pro processor, 10 CPU cores, and 16 GB of RAM.
   We present our evaluation in Table 1. The table gives the number of basic blocks in each program
and the number of permission checks— checking whether all dereferenced locations are contained
in the support of the precondition or are newly allocated, and checking if the permissions granted
to functions that are called are subsets of the method’s permissions and the tightness of returned
permissions (support of the postcondition). The verification times for FL and the times taken by the
unoptimized and optimized versions of the tool for SL benchmarks are reported. This time includes
(a) translation between logics— SL-FL to FL, FL to FORD— including optimizations, as well as the
verification of (b) all VCs, including permission checks, (c) lemmas, and (d) equality of supports.
   Our tool verifies all benchmarks effectively, in less than a minute for all benchmarks. Over all
these benchmarks, the instantiation that we identify to begin with already sufficed in proving the
programs correct, and no further instantiation was needed.
24                                                                                           Trovato et al.


   We observe that SL-FL benchmarks take longer than FL, as expected. We believe to be both due to
translation bloat as well as certain superfluous checks that typical formulations in separation logic
mandate. However, our optimization reduces the verification time by 4% on average and comes
closer to the FL verification time.



  When Provers Fail: Bug Finding and Counterexamples. There are two parts to our verification
methodology: (1) generating VCs in FL (and ultimately FORD), and (2) using an FO-complete
validity technique to discharge the VCs (see Section 5.4). FL/FORD interpret recursive definitions
with the intended least fixpoint semantics, but the VC validity checking techniques we employ do
not— they are only complete with respect to a fixpoint semantics. Note that the set of models where
definitions respect fixpoint semantics is larger. For example, consider the definition List (𝑥) :=
                                                                                          next    next
(𝑥 = nil) ∨ List (next (𝑥)). Under fixpoint semantics, the element 𝑒 1 in the model 𝑒 1 → 𝑒 2 → nil
would, of course, satisfy the definition of List, but it could also be interpreted as pointing to a List
                 next   next
in the model 𝑒 1 → 𝑒 2 → 𝑒 1 representing a two-element cycle. The latter model would not satisfy
the definition under least fixpoint semantics. Specifically, this means that when our FORD prover
fails, it fails with respect to this larger class of models. In practice, there is also another source of
failure from insufficient instantiations. Our validity technique is based on systematic instantiation
of definitions (“unrolling”) and other quantified formulas (such as frame reasoning axioms). The
instantiation happens in rounds, and FO-completeness holds in the limit: if the VC is valid under
fixpoint semantics, the prover will eventually succeed in some round. Each round sends a decidable
quantifier-free query to an SMT solver.
   Overall, there are three sources of failure for the prover: (a) the VC is FO-valid but the instan-
tiations are insufficient, (b) the VC is valid in FO+lfp but not in FO, and (c) the VC is invalid in
FO+lfp (i.e., program/spec has a bug). The model returned by the SMT solver in a particular round
only witnesses the non-provability of the VC with the available set of instantiations and does not
disambiguate between the three cases.
   When we developed our benchmark suite, we identified bugs in our specs and implementations by
simply isolating the basic blocks that our solver could not prove and tracing proof obligations semi-
automatically. For example, we isolated conjuncts in the postcondition that could not be proven, or
added extra assertions at certain intermediate points within the basic block. This helped us identify
many sources of error, among them insufficient preconditions, bugs in implementation where
we missed corner cases, and the need for certain inductive lemmas. Note that inductive lemmas
address the second failure mode, as discussed in Section 6.2.2. We also found it particularly helpful
to weaken our postconditions to Relaxed or Heapless postconditions to triage bugs pertaining
to proofs regarding supports and the allocated set of locations. This allowed us, for instance, to
strengthen contracts for function calls with properties about supports.
   There are many approaches that can help disambiguate between VCs that are truly invalid and
those that are simply not FO-valid (needing an inductive lemma). One possibility is to ask an
SMT solver for a true counterexample (a model with least fixpoint interpretations, as opposed
to a nonstandard model) of bounded size, say 5-6 locations. This is hard in general as one needs
to express the unbounded computation involved in determining least fixpoints, but establishing
practical bounds on the length of the computation may work as well. However, we believe that
the design of our logics makes this approach particularly attractive, and leave it to future work to
determine a general technique for synthesizing counterexamples to invalid formulas in FO-complete
heap logics.
FO-Complete Program Verification for Heap Logics                                                   25


7   Related Work
The work on Frame Logic [43, 44] is the most relevant prior work, which we have discussed at
length in the paper. There are many other logics [3, 9, 23, 31, 54, 61, 64] for heaps that make
different choices in terms of whether heaplets of formulae are implicit, whether formulas have
unique heaps, etc. The most popular among these is Separation logic [16, 49, 50, 61] which has
implicit but non-unique heaplets for formulas. Dynamic Frames [31, 32] and related approaches
like Region Logic [2–4] allow users to explicitly specify heaplets and uses them to reason about
the program’s modifications. The work on Implicit Dynamic Frames [36, 53, 64, 65] combines
the ideas of implicit heaplets in separation logic and explicitly accessible heaplets in dynamic
frames, resulting in implementations such as Chalice [53] and Viper [18, 22, 40]. In particular,
Viper provides a general framework into which many permission logics can be encoded, including
Separation Logic. However, it generates quantified verification conditions to SMT solvers over
inherently incomplete logics. There is also work on translating VeriFast [29] predicates into Implicit
Dynamic Frames [30].
   There is rich prior work on reasoning with separation logic. A first category of prior works
develop fragments with decidable reasoning [5–7, 14, 25, 46, 52, 55, 56]. There is also work on
decidability of heap properties specifiable in EPR (Effectively Propositional Reasoning) [26–28]. A
second category of works translate separation logic to first-order logic and use reasoning mech-
anisms for FOL [13, 38, 39, 54, 56–59, 66]. There are also techniques that reason with separation
logic using cyclic proofs [11, 68].
   The work in [9] develops a logic similar to FL and uses Why3 [20, 21] to reason with verification
conditions. Recent work [45] identifies a technique that avoids incompleteness and the use of
inductive lemmas, but requires developing a set of maps upfront for a set of properties and have to
be redesigned when the properties change.
   We use in our work the reasoning technique of natural proofs [38, 39, 54, 59]. The technique of
quantifier instantiation used by natural proofs is similar to many other unfolding-based techniques
in the literature [29, 33, 35, 48, 66].
   The work on FL formulates a fragment of separation logic called Precise Separation Logic which
has determined, unique heaplets and provides a translation of the fragment to FL. Other prior
literature has also studied fragments with determined heaplets [51, 54, 59] as it is easier to develop
automated reasoning for them. We believe that the techniques developed in this work can open up
new pathways to automating separation logics.



8   Conclusions
We have presented two logics, a frame logic and a separation logic, which admit FO-complete
program verification, where the latter demands that all valid theorems under fixpoint semantics
of recursive definitions are eventually proved by a system. Our work navigates various threats to
incompleteness, carefully designing logics with particular semantics as well as reasoning procedures
for them that are FO-complete, and are also effective in practice.
   The most promising future direction that our work paves is to build new program logics and
verification paradigms that are held to the theoretical standard of being FO-complete. Our evaluation
suggests that by having FO-complete procedures that only make repeated calls to SMT solvers on
decidable logics, efficient and FO-complete procedures are possible. Realizing such an FO-complete
reasoning for a rich programming language through a mature VC generation pipeline. such as the
Viper/Boogie pipeline, is hence a pressing direction to pursue.
26                                                                                    Trovato et al.


   In order to reason with first-order logics with recursive definitions, recent work [34, 41] has
proposed inductive lemma synthesis algorithms. Incorporation of lemma synthesis into our verifi-
cation framework would alleviate the current burden on the programmer to write these inductive
lemmas (described for our benchmarks in Section 6).
   We believe that our alternate semantics for separation logic SL-FL is worthy of further study.
In particular, since we have shown that its reasoning can be automated using FO reasoning, a
track in an SL competition like SLComp [62] would be interesting to encourage competitive tool
development.
FO-Complete Program Verification for Heap Logics                                                                          27


Data-Availability Statement
Reviewers may find the SL-FL and FL benchmarks evaluated on in the following anonymous
repository: https://github.com/verifproj/complete-logics-bench. The VC-generation tool will be
released for artifact evaluation.

References
 [1] Alfred V. Aho and Jeffrey D. Ullman. 1979. Universality of Data Retrieval Languages. In Proceedings of the 6th ACM
     SIGACT-SIGPLAN Symposium on Principles of Programming Languages (San Antonio, Texas) (POPL ’79). Association
     for Computing Machinery, New York, NY, USA, 110–119. https://doi.org/10.1145/567752.567763
 [2] Anindya Banerjee and David A. Naumann. 2013. Local Reasoning for Global Invariants, Part II: Dynamic Boundaries.
     J. ACM 60, 3, Article 19 (jun 2013), 73 pages. https://doi.org/10.1145/2485981
 [3] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2008. Regional Logic for Local Reasoning about Global In-
     variants. In ECOOP 2008 – Object-Oriented Programming, Jan Vitek (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     387–411.
 [4] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2013. Local Reasoning for Global Invariants, Part I: Region
     Logic. J. ACM 60, 3, Article 18 (June 2013), 56 pages. http://doi.acm.org/10.1145/2485982
 [5] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2006. Smallfoot: Modular Automatic Assertion Checking
     with Separation Logic. In Proceedings of the 4th International Conference on Formal Methods for Components and Objects
     (Amsterdam, The Netherlands) (FMCO’05). Springer-Verlag, Berlin, Heidelberg, 115–137. https://doi.org/10.1007/
     11804192_6
 [6] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2004. A Decidable Fragment of Separation Logic. In Proceedings
     of the 24th International Conference on Foundations of Software Technology and Theoretical Computer Science (Chennai,
     India) (FSTTCS’04). Springer-Verlag, Berlin, Heidelberg, 97–109. https://doi.org/10.1007/978-3-540-30538-5_9
 [7] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In Proceedings
     of the Third Asian Conference on Programming Languages and Systems (Tsukuba, Japan) (APLAS’05). Springer-Verlag,
     Berlin, Heidelberg, 52–68. https://doi.org/10.1007/11575467_5
 [8] Régis Blanc, Viktor Kuncak, Etienne Kneuss, and Philippe Suter. 2013. An Overview of the Leon Verification System:
     Verification by Translation to Recursive Functions. In Proceedings of the 4th Workshop on Scala (Montpellier, France)
     (SCALA ’13). Association for Computing Machinery, New York, NY, USA, Article 1, 10 pages. https://doi.org/10.1145/
     2489837.2489838
 [9] François Bobot and Jean-Christophe Filliâtre. 2012. Separation Predicates: A Taste of Separation Logic in First-Order
     Logic. In Formal Methods and Software Engineering, Toshiaki Aoki and Kenji Taguchi (Eds.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 167–181.
[10] Rémi Brochenin, Stéphane Demri, and Etienne Lozes. 2008. On the Almighty Wand. In Computer Science Logic, Michael
     Kaminski and Simone Martini (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 323–338.
[11] James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. 2011. Automated Cyclic Entailment Proofs in
     Separation Logic. In Proceedings of the 23rd International Conference on Automated Deduction (CADE’11). Springer-Verlag,
     Berlin, Heidelberg, 131–146. http://dl.acm.org/citation.cfm?id=2032266.2032278
[12] Ashok K. Chandra and David Harel. 1980. Structure and Complexity of Relational Queries. In Proceedings of the 21st
     Annual Symposium on Foundations of Computer Science (SFCS ’80). IEEE Computer Society, USA, 333–347. https:
     //doi.org/10.1109/SFCS.1980.41
[13] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. 2007. Automated Verification of Shape, Size
     and Bag Properties. In Proceedings of the 12th IEEE International Conference on Engineering Complex Computer Systems
     (ICECCS ’07). IEEE Computer Society, USA, 307–320. https://doi.org/10.1109/ICECCS.2007.17
[14] Byron Cook, Christoph Haase, Joël Ouaknine, Matthew Parkinson, and James Worrell. 2011. Tractable Reasoning in a
     Fragment of Separation Logic. In Proceedings of the 22nd International Conference on Concurrency Theory (Aachen,
     Germany) (CONCUR’11). Springer-Verlag, Berlin, Heidelberg, 235–249.
[15] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proceedings of the 14th International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems (Budapest, Hungary) (TACAS’08).
     Springer-Verlag, Berlin, Heidelberg, 337–340.
[16] Stéphane Demri and Morgan Deters. 2015. Separation logics and modalities: a survey. Journal of Applied Non-Classical
     Logics 25 (2015), 50–99.
[17] H.D. Ebbinghaus, J. Flum, and W. Thomas. 1996. Mathematical Logic. Springer New York.
[18] Marco Eilers, Malte Schwerhoff, and Peter Müller. 2024. Verification Algorithms for Automated Separation Logic
     Verifiers. In Computer Aided Verification, Arie Gurfinkel and Vijay Ganesh (Eds.). Springer Nature Switzerland, Cham,
     362–386.
28                                                                                                             Trovato et al.


[19] H.B. Enderton. 2001. A Mathematical Introduction to Logic. Elsevier Science. https://books.google.com/books?id=
     dVncCl_EtUkC
[20] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3: Where Programs Meet Provers. In Proceedings of the
     22nd European Conference on Programming Languages and Systems (Rome, Italy) (ESOP’13). Springer-Verlag, Berlin,
     Heidelberg, 125–128. https://doi.org/10.1007/978-3-642-37036-6_8
[21] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3: Where Programs Meet Provers. In Proceedings of the
     22nd European Conference on Programming Languages and Systems (Rome, Italy) (ESOP’13). Springer-Verlag, Berlin,
     Heidelberg, 125–128. https://doi.org/10.1007/978-3-642-37036-6_8
[22] Stefan Heule, Ioannis T. Kassios, Peter Müller, and Alexander J. Summers. 2013. Verification Condition Generation for
     Permission Logics with Abstract Predicates and Abstraction Functions. In ECOOP 2013 – Object-Oriented Programming,
     Giuseppe Castagna (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 451–476.
[23] Aquinas Hobor and Jules Villard. 2013. The Ramifications of Sharing in Data Structures. In Proceedings of the
     40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Rome, Italy) (POPL ’13).
     Association for Computing Machinery, New York, NY, USA, 523–536. https://doi.org/10.1145/2429069.2429131
[24] Neil Immerman. 1982. Relational Queries Computable in Polynomial Time (Extended Abstract). In Proceedings of the
     Fourteenth Annual ACM Symposium on Theory of Computing (San Francisco, California, USA) (STOC ’82). Association
     for Computing Machinery, New York, NY, USA, 147–152. https://doi.org/10.1145/800070.802187
[25] Radu Iosif, Adam Rogalewicz, and Jiri Simacek. 2013. The Tree Width of Separation Logic with Recursive Definitions.
     In Automated Deduction – CADE-24, Maria Paola Bonacina (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 21–38.
[26] Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Ori Lahav, Aleksandar Nanevski, and Mooly Sagiv. 2014. Modular
     Reasoning About Heap Paths via Effectively Propositional Formulas. In Proceedings of the 41st ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages (San Diego, California, USA) (POPL ’14). ACM, New York, NY,
     USA, 385–396. https://doi.org/10.1145/2535838.2535854
[27] Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Aleksandar Nanevski, and Mooly Sagiv. 2013. Effectively-
     Propositional Reasoning About Reachability in Linked Data Structures. In Proceedings of the 25th International
     Conference on Computer Aided Verification (Saint Petersburg, Russia) (CAV’13). Springer-Verlag, Berlin, Heidelberg,
     756–772. https://doi.org/10.1007/978-3-642-39799-8_53
[28] Shachar Itzhaky, Nikolaj Bjørner, Thomas Reps, Mooly Sagiv, and Aditya Thakur. 2014. Property-Directed Shape
     Analysis. In Proceedings of the 16th International Conference on Computer Aided Verification (CAV’14). Springer-Verlag,
     Berlin, Heidelberg, 35–51. https://doi.org/10.1007/978-3-319-08867-9_3
[29] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In Proceedings of the Third International Conference on NASA
     Formal Methods (Pasadena, CA) (NFM’11). Springer-Verlag, Berlin, Heidelberg, 41–55.
[30] Daniel Jost and Alexander J. Summers. 2014. An Automatic Encoding from VeriFast Predicates into Implicit Dynamic
     Frames. In Verified Software: Theories, Tools, Experiments, Ernie Cohen and Andrey Rybalchenko (Eds.). Springer Berlin
     Heidelberg, Berlin, Heidelberg, 202–221.
[31] Ioannis T. Kassios. 2006. Dynamic Frames: Support for Framing, Dependencies and Sharing Without Restrictions. In FM
     2006: Formal Methods, Jayadev Misra, Tobias Nipkow, and Emil Sekerinski (Eds.). Springer-Verlag, Berlin, Heidelberg,
     268–283.
[32] I. T. Kassios. 2011. The Dynamic Frames Theory. Form. Asp. Comput. 23, 3 (May 2011), 267–288. https://doi.org/10.
     1007/s00165-010-0152-5
[33] Matt Kaufmann and J. S. Moore. 1997. An Industrial Strength Theorem Prover for a Logic Based on Common Lisp.
     IEEE Trans. Softw. Eng. 23, 4 (April 1997), 203–213. https://doi.org/10.1109/32.588534
[34] Cole Kurashige, Ruyi Ji, Aditya Giridharan, Mark Barbone, Daniel Noor, Shachar Itzhaky, Ranjit Jhala, and Nadia
     Polikarpova. 2024. CCLemma: E-Graph Guided Lemma Discovery for Inductive Equational Proofs. Proc. ACM Program.
     Lang. 8, ICFP, Article 264 (Aug. 2024), 27 pages. https://doi.org/10.1145/3674653
[35] K. Rustan M. Leino. 2012. Automating Induction with an SMT Solver. In Proceedings of the 13th International Conference
     on Verification, Model Checking, and Abstract Interpretation (Philadelphia, PA) (VMCAI’12). Springer-Verlag, Berlin,
     Heidelberg, 315–331. https://doi.org/10.1007/978-3-642-27940-9_21
[36] K. Rustan M. Leino and Peter Müller. 2009. A Basis for Verifying Multi-threaded Programs. In Programming Languages
     and Systems, Giuseppe Castagna (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 378–393. https://doi.org/10.
     1007/978-3-642-00590-9_27
[37] Leonid Libkin. 2004. Elements of Finite Model Theory. Springer. https://doi.org/10.1007/978-3-662-07003-1
[38] Christof Löding, P. Madhusudan, and Lucas Peña. 2018. Foundations for natural proofs and quantifier instantiation.
     PACMPL 2, POPL (2018), 10:1–10:30. https://doi.org/10.1145/3158098
[39] P. Madhusudan, Xiaokang Qiu, and Andrei Ştefănescu. 2012. Recursive Proofs for Inductive Tree Data-structures. In
     Proceedings of the 39th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Philadelphia,
FO-Complete Program Verification for Heap Logics                                                                        29


     PA, USA) (POPL ’12). ACM, New York, NY, USA, 123–136. https://doi.org/10.1145/2103656.2103673
[40] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-
     Based Reasoning. In Proceedings of the 17th International Conference on Verification, Model Checking, and Abstract
     Interpretation - Volume 9583 (St. Petersburg, FL, USA) (VMCAI 2016). Springer-Verlag, Berlin, Heidelberg, 41–62.
     https://doi.org/10.1007/978-3-662-49122-5_2
[41] Adithya Murali, Lucas Peña, Eion Blanchard, Christof Löding, and P. Madhusudan. 2022. Model-Guided Synthesis
     of Inductive Lemmas for FOL with Least Fixpoints. Proc. ACM Program. Lang. 6, OOPSLA2, Article 191 (oct 2022),
     30 pages. https://doi.org/10.1145/3563354
[42] Adithya Murali, Lucas Peña, Ranjit Jhala, and P. Madhusudan. 2023. Complete First-Order Reasoning for Properties of
     Functional Programs. Proc. ACM Program. Lang. 7, OOPSLA2, Article 259 (oct 2023), 30 pages. https://doi.org/10.1145/
     3622835
[43] Adithya Murali, Lucas Peña, Christof Löding, and P. Madhusudan. 2023. A First-Order Logic with Frames. ACM Trans.
     Program. Lang. Syst. 45, 2, Article 7 (may 2023), 44 pages. https://doi.org/10.1145/3583057
[44] Adithya Murali, Lucas Peña, Christof Löding, and P. Madhusudan. 2020. A First-Order Logic with Frames. In
     Programming Languages and Systems, Peter Müller (Ed.). Springer International Publishing, Cham, 515–543.
[45] Adithya Murali, Cody Rivera, and P. Madhusudan. 2024. Predictable Verification using Intrinsic Definitions. Proc.
     ACM Program. Lang. 8, PLDI, Article 220 (jun 2024), 26 pages. https://doi.org/10.1145/3656450
[46] Juan Antonio Navarro Pérez and Andrey Rybalchenko. 2011. Separation Logic + Superposition Calculus = Heap Theo-
     rem Prover. In Proceedings of the 32nd ACM SIGPLAN Conference on Programming Language Design and Implementation
     (PLDI ’11). ACM, New York, NY, USA, 556–566.
[47] Greg Nelson and Derek C. Oppen. 1979. Simplification by Cooperating Decision Procedures. ACM Trans. Program.
     Lang. Syst. 1, 2 (Oct 1979), 245–257. https://doi.org/10.1145/357073.357079
[48] Huu Hai Nguyen and Wei-Ngan Chin. 2008. Enhancing Program Verification with Lemmas. In Proceedings of the
     20th International Conference on Computer Aided Verification (Princeton, NJ, USA) (CAV ’08). Springer-Verlag, Berlin,
     Heidelberg, 355–369. https://doi.org/10.1007/978-3-540-70545-1_34
[49] Peter W. O’Hearn. 2012. A Primer on Separation Logic (and Automatic Program Verification and Analysis). In Software
     Safety and Security - Tools for Analysis and Verification, Tobias Nipkow, Orna Grumberg, and Benedikt Hauptmann
     (Eds.). NATO Science for Peace and Security Series - D: Information and Communication Security, Vol. 33. IOS Press,
     286–318. https://doi.org/10.3233/978-1-61499-028-4-286
[50] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning About Programs That Alter Data
     Structures. In Proceedings of the 15th International Workshop on Computer Science Logic (CSL ’01). Springer-Verlag,
     London, UK, UK, 1–19. http://dl.acm.org/citation.cfm?id=647851.737404
[51] Peter W. O’Hearn, Hongseok Yang, and John C. Reynolds. 2004. Separation and Information Hiding. In Proceedings of
     the 31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Venice, Italy) (POPL ’04). ACM,
     New York, NY, USA, 268–280. https://doi.org/10.1145/964001.964024
[52] Jens Pagel. 2020. Decision procedures for separation logic: beyond symbolic heaps. Ph. D. Dissertation. Wien.
[53] Matthew J. Parkinson and Alexander J. Summers. 2011. The Relationship between Separation Logic and Implicit
     Dynamic Frames. In Programming Languages and Systems, Gilles Barthe (Ed.). Springer Berlin Heidelberg, Berlin,
     Heidelberg, 439–458.
[54] Edgar Pek, Xiaokang Qiu, and P. Madhusudan. 2014. Natural Proofs for Data Structure Manipulation in C Using Separa-
     tion Logic. In Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (Edinburgh, United Kingdom) (PLDI ’14). ACM, New York, NY, USA, 440–451. https://doi.org/10.1145/2594291.2594325
[55] Juan Antonio Navarro Pérez and Andrey Rybalchenko. 2013. Separation Logic Modulo Theories. In Programming
     Languages and Systems (APLAS). Springer International Publishing, Cham, 90–106.
[56] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2013. Automating Separation Logic Using SMT. In Proceedings of
     the 25th International Conference on Computer Aided Verification (Saint Petersburg, Russia) (CAV’13). Springer-Verlag,
     Berlin, Heidelberg, 773–789. https://doi.org/10.1007/978-3-642-39799-8_54
[57] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2014. Automating Separation Logic with Trees and Data. In
     Proceedings of the 16th International Conference on Computer Aided Verification (CAV’14). Springer-Verlag, Berlin,
     Heidelberg, 711–728.
[58] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2014. GRASShopper. In Tools and Algorithms for the Construction
     and Analysis of Systems, Erika Ábrahám and Klaus Havelund (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     124–139.
[59] Xiaokang Qiu, Pranav Garg, Andrei Ştefănescu, and P. Madhusudan. 2013. Natural Proofs for Structure, Data, and
     Separation. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (Seattle, Washington, USA) (PLDI ’13). ACM, New York, NY, USA, 231–242. https://doi.org/10.1145/2491956.2462169
30                                                                                                              Trovato et al.


[60] Andrew Reynolds and Viktor Kuncak. 2015. Induction for SMT Solvers. In Verification, Model Checking, and Abstract
     Interpretation, Deepak D’Souza, Akash Lal, and Kim Guldstrand Larsen (Eds.). Springer Berlin Heidelberg, Berlin,
     Heidelberg, 80–98.
[61] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the 17th
     Annual IEEE Symposium on Logic in Computer Science (LICS ’02). IEEE Computer Society, USA, 55–74.
[62] Mihaela Sighireanu. 2021. SL-COMP: Competition of Solvers for Separation Logic: Report on the Third Edition. Int. J.
     Softw. Tools Technol. Transf. 23, 6 (dec 2021), 895–903. https://doi.org/10.1007/s10009-021-00628-w
[63] Aishwarya Sivaraman, Alex Sanchez-Stern, Bretton Chen, Sorin Lerner, and Todd Millstein. 2022. Data-driven
     lemma synthesis for interactive proofs. Proc. ACM Program. Lang. 6, OOPSLA2, Article 143 (Oct. 2022), 27 pages.
     https://doi.org/10.1145/3563306
[64] Jan Smans, Bart Jacobs, and Frank Piessens. 2009. Implicit Dynamic Frames: Combining Dynamic Frames and Separation
     Logic. In ECOOP 2009 – Object-Oriented Programming, Sophia Drossopoulou (Ed.). Springer Berlin Heidelberg, Berlin,
     Heidelberg, 148–172. https://doi.org/10.1007/978-3-642-03013-0_8
[65] Jan Smans, Bart Jacobs, and Frank Piessens. 2012. Implicit Dynamic Frames. ACM Trans. Program. Lang. Syst. 34, 1,
     Article 2 (May 2012), 58 pages. https://doi.org/10.1145/2160910.2160911
[66] Philippe Suter, Mirco Dotta, and Viktor Kunćak. 2010. Decision Procedures for Algebraic Data Types with Abstractions.
     In Proceedings of the 37th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Madrid,
     Spain) (POPL ’10). ACM, New York, NY, USA, 199–210. https://doi.org/10.1145/1706299.1706325
[67] Philippe Suter, Ali Sinan Köksal, and Viktor Kuncak. 2011. Satisfiability Modulo Recursive Programs. In Static Analysis,
     Eran Yahav (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 298–315.
[68] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction
     Proof in Separation Logic. In FM 2016: Formal Methods, John Fitzgerald, Constance Heitmeyer, Stefania Gnesi, and Anna
     Philippou (Eds.). Springer International Publishing, Cham, 659–676. https://doi.org/10.1007/978-3-319-48989-6_40
[69] Alfred Tarski. 1955. A lattice-theoretical fixpoint theorem and its applications. Pacific J. Math. 5, 2 (1955), 285 – 309.
[70] Alan Turing. 1936. On Computable Numbers, with an Application to the Entscheidungsproblem. Proceedings of the
     London Mathematical Society 42, 1 (1936), 230–265. https://doi.org/10.2307/2268810
[71] Moshe Y. Vardi. 1982. The Complexity of Relational Query Languages (Extended Abstract). In Proceedings of the
     Fourteenth Annual ACM Symposium on Theory of Computing (San Francisco, California, USA) (STOC ’82). Association
     for Computing Machinery, New York, NY, USA, 137–146. https://doi.org/10.1145/800070.802186
[72] Niki Vazou, Anish Tondwalkar, Vikraman Choudhury, Ryan G. Scott, Ryan R. Newton, Philip Wadler, and Ranjit Jhala.
     2018. Refinement reflection: complete verification with SMT. Proc. ACM Program. Lang. 2, POPL (2018), 53:1–53:31.
     https://doi.org/10.1145/3158141
[73] Weikun Yang, Grigory Fedyukovich, and Aarti Gupta. 2019. Lemma Synthesis for Automating Induction over Algebraic
     Data Types. In Principles and Practice of Constraint Programming, Thomas Schiex and Simon de Givry (Eds.). Springer
     International Publishing, Cham, 600–617.
FO-Complete Program Verification for Heap Logics                                                       31


A   Additional Details from Section 2
   Proof of Theorem 2.3. We show a stronger result, namely that the logic is highly undecidable.
To achieve this, we reduce validity in MSO to the non-halting problem for Turing Machines whose
definition of halting is that the final state must be hit infinitely often. Highly undecidable problems
are not recursively enumerable, and their complements are not recursively enumerable either, i.e.,
they are R.E Hard ∩ co-R.E Hard. We describe the key elements of the proof below.
   First, we define natural numbers with comparison, using symbols zero, succ, and <. We constrain
these symbols using quantified FO formulae in the usual way, e.g., requiring that < forms a total
order. Note, however, that a model may have elements beyond the 𝜔-prefix that correspond to the
“standard” natural numbers. To cull out the 𝜔-prefix, we write the following formula quantified
over a set variable 𝑆:                                                         
   TrueNat ≡ ∀𝑆. (zero ∈ 𝑆 ∧ (∀𝑥 . 𝑥 ∈ 𝑆 ⇒ succ(𝑥) ∈ 𝑆)) ⇒ (∀𝑦. 𝑦 ∈ 𝑆)
TrueNat says that every set that contains zero and is successor-closed is universal. This can only
hold on a model if every element in the model corresponds to a standard natural number.
   The remainder of the proof is standard. We encode the Turing Machine using functions state(𝑖)
to denote the state of the TM at time step 𝑖, head (𝑖) to denote the position of the head at time
step 𝑖, and cell(𝑖, 𝑗) to denote the contents of the 𝑗-th cell at time step 𝑖. We express FO-quantified
constraints to ensure that the functions are defined correctly. Let us denote these constraints by
TMEncoding.
   We are now ready to construct the formula to express non-halting. Recall that our definition of
non-halting is that the TM does not hit the halting state infinitely often, i.e., there is a point in time
after which the TM does not hit the halting state. Let the halting state be encoded zero, without
loss of generality. The formula that expresses non-halting is the following one:

                                                                                        
                    TrueNat ⇒ TMEncoding ⇒ (∃𝑧∀𝑡 . 𝑧 < 𝑡 ⇒ state(𝑡) ≠ zero)


  This completes the proof. Note that the formula does not contain any alternating quantification
over sets.                                                                                      □


  Proof of Theorem 2.4. We first define the variant of Separation Logic that we study in this
result. The syntax of the logic is as follows:

                                𝜑 ≔ emp | true | StackFormula | 𝑥 −𝑓 𝑦 | 𝜑 ∧ 𝜑 | 𝜑 ∗ 𝜑
                                      | ite(StackFormula, 𝜑, 𝜑) | RecPred (𝑡) | ∃𝑦. 𝜑
                   StackFormula ≔ 𝑡 = 𝑡 | 𝑡 ≠ 𝑡

where RecPred denotes recursively defined predicates, and 𝑡 denotes a term. The grammar for terms
is the usual one.
   A recursive predicate 𝑅(𝑥) is defined using a formula 𝜌 (𝑥) from the above logic, where 𝜌 can
mention 𝑅 (only positively). We describe the semantics below. We evaluate formulas over a store 𝑠
(map from variables to values) and a heap ℎ (map from pointer symbols to functions) as Separation
Logic does, but we now allow for ℎ to be infinite. In addition, we also require the model to interpret
recursively defined predicate symbols, which we denote by I.
32                                                                                                     Trovato et al.




𝑠, ℎ, I |= emp                 if ℎ is empty
𝑠, ℎ, I |= true                always
𝑠, ℎ, I |= StackFormula        if StackFormula evaluates to true according to 𝑠
𝑠, ℎ, I |= 𝑥 −𝑓 𝑦             if dom(ℎ) = {𝑥 } and ℎ(𝑓 ) (𝑠 (𝑥)) = 𝑦
𝑠, ℎ, I |= 𝛼 ∧ 𝛽               if 𝑠, ℎ, I |= 𝛼 and 𝑠, ℎ, I |= 𝛽
𝑠, ℎ, I |= 𝛼 ∗ 𝛽               if there exist disjoint heaplets ℎ 1, ℎ 2 such that
                                  ℎ 1 ⊎ ℎ 2 = ℎ and 𝑠, ℎ 1, I |= 𝛼 and 𝑠, ℎ 2, I |= 𝛽
𝑠, ℎ, I |= ite(cond, 𝛼, 𝛽)     if 𝑠 |= cond and 𝑠, ℎ, I |= 𝛼 or 𝑠 ̸ |= cond and 𝑠, ℎ, I |= 𝛽
𝑠, ℎ, I |= RecPred (𝑡)         if I (RecPred) (𝑠 (𝑡)) = true and 𝑠, ℎ, I |= 𝜌 (𝑡) where 𝜌 is the body of RecPred
𝑠, ℎ, I |= ∃𝑦.𝜑                if there is some element 𝑎 of the appropriate sort such that
                                  𝑠 [𝑦 ↦→ 𝑎], ℎ, I |= 𝜑

  Further, we treat the above recursive semantics for RecPred as a fixpoint rather than least fixpoint.
To illustrate the consequence of using fixpoints, consider the following predicate List (𝑥) denoting
(now fixpoint) linked lists:

                             List (𝑥) ≡ ite(𝑥 = nil, emp, ∃𝑦. 𝑥 −next 𝑦 ∗ List (𝑦))

   Let 𝑠 be the store that interprets 𝑥 to 0, and let ℎ be the infinite heaplet whose domain is the
natural numbers, where the next pointer is interpreted by ℎ(next) (𝑖) = 𝑖 +1. This models an ‘infinite
list’. Let I be the interpretation that marks every node in this infinite list as satisfying the predicate
List. Clearly, 𝑠, ℎ, I |= List (𝑥) would not hold if I were the least fixpoint interpretation (no node
would satisfy List). However, it can hold in the logic defined above as we admit any interpretation
which is a valid fixpoint for the given recursive definition.
   We now present our construction for modeling non-halting in the above logic. We model the
run of a two-counter machine using a linked list with a next pointer. We use integer-valued
pointers state, 𝑐 1 , and 𝑐 2 to denote the state and the values of the two counters corresponding to
the configuration encoded by a node in the linked list, and define a recursive predicate tcm_run(𝑥)
to check whether the linked list encodes a valid run of the machine. We assume without loss of
generality that the initial state is 0 and the halting state is 1. The predicate tcm_run is then defined
as follows:
                         
    tcm_run(𝑥) ≔ ite 𝑥 = nil, emp,
                         ∃𝑦, 𝑞. (𝑥 −next 𝑦 ∧ 𝑥 −state 𝑞 ∧ 𝑥 −𝑐 1 𝑖 ∧ 𝑥 −𝑐 2 𝑗)
                                                ∗
                                   ite(𝑦 = nil, emp, ∃𝑞 ′ .((𝑦 −state 𝑞 ′ ∧ 𝑦 −𝑐 1 𝑖 ′ ∧ 𝑦 −𝑐 2 𝑗 ′ ) ∗ true)
                                                             ∧ transition(𝑞, 𝑖, 𝑗, 𝑞 ′, 𝑖 ′, 𝑗 ′ )
                                                             ∧ tcm_run(𝑦)
                                        )
                                   
                         
FO-Complete Program Verification for Heap Logics                                                     33


where transition is a macro expressing the correctness of the state transition for the two-counter
machine. We define tcm(𝑥) to be the formula tcm_run(𝑥) ∧ (𝑥 −𝑠𝑡𝑎𝑡𝑒 0 ∗ true), which denotes
that 𝑥 points to a list with a valid run of the machine starting from the initial state. Similarly, we
define halt (𝑥) to be the formula 𝑥 −𝑠𝑡𝑎𝑡𝑒 1.
  Finally, we express the following entailment:

                𝑥 ≠ nil ∧ (tcm(𝑥) ∗ true) ∧ (halt (𝑦) ∗ true) |= tcm(𝑥) ∗ halt (𝑦) ∗ true

    We now claim that the above entailment is valid iff the two-counter machine does not halt.
    Machine Doesn’t Halt ⇒ Entailment Valid. Observe that in any 𝑠, ℎ, I such that 𝑠, ℎ, I |= tcm(𝑥)
holds, the 𝜔-chain of linked list elements starting at 𝑥 and closed under the next pointer must in
fact encode a run from the initial configuration for the machine. Furthermore, ℎ must contain all
the nodes in this 𝜔-chain. However, since we consider fixpoint definitions, it is possible that ℎ may
contain more elements.
    Let us assume that the machine does not halt. Now consider 𝑠, ℎ, I such that the left-hand
side of the entailment holds. In particular, we have that 𝑠, ℎ, I |= tcm(𝑥). Since the machine does
not halt, the 𝜔-chain cannot contain an node with the halting state. In particular, we have that
𝑠, ℎ, I |= halt (𝑦), which means that 𝑦 cannot be part of the 𝜔-chain. Therefore, we can split ℎ into
three disjoint parts: (a) ℎ 1 , containing the 𝜔-chain where tcm(𝑥) holds, (b) ℎ 2 = {𝑦}, where halt (𝑦)
holds, and (c) any other elements. This shows that the right-hand side of the entailment holds, and
we are done.
    Machine Halts ⇒ Entailment Invalid. If the machine does not halt, in any 𝑠, ℎ, I such that
𝑠, ℎ, I |= tcm(𝑥), there must exist a node 𝑒 in the 𝜔-chain starting at 𝑥 that corresponds to the
halting state. Let us now consider the entailment with 𝑦 being interpreted as 𝑒. Clearly, the left-hand
side of the entailment is true. However, the right-hand side cannot be true since any ℎ such that
𝑠, ℎ, I |= tcm(𝑥) must necessarily contain the 𝜔-chain, and in particular must contain 𝑒. Therefore,
the heaplet of halt (𝑦) cannot be separated from the heaplet of tcm(𝑥).
    This completes the proof.                                                                         □

  Note that in the above proof we crucially use the fact that given an 𝑠, ℎ, I |= tcm(𝑥), if ℎ contains
more elements than the 𝜔-chain, then we also have 𝑠, ℎ ′, I |= tcm(𝑥) where ℎ ′ is any fixpoint-closed
subset of ℎ that contains the 𝜔-chain, and in particular can be the 𝜔-chain itself. The formula can
be satisfied over multiple heaplets, and we use this in the first direction of the proof.

B    Operational Semantics
We consider configurations of the form (𝑆, 𝐻, 𝐴) where 𝑆 is a store, 𝐻 is a heap, and 𝐴 denotes
the set of allocated locations. Formally, 𝑆 is a partial map that interprets constants, variables, and
non-mutable functions. 𝐻 is a tuple of maps— one for each mutable function 𝑓 ∈ F𝑚 — whose
domain is the universe of locations and range is the universe of the appropriate sort (locations for
pointers and various background sorts for data fields). We model nil as a distinguished location,
ensuring in our semantics that valid programs do not dereference nil. Note that 𝑆 and 𝐻 together
define a model where one can interpret FL formulas. We denote the satisfaction of an SL formula 𝜑
on the model corresponding to a given 𝑆, 𝐻 by 𝑆, 𝐻 |= 𝜑. 𝐴 is a subset of the universe of locations
that does not contain nil. We also introduce an error configuration ⊥.
   We describe the operational semantics of various commands manipulating such configurations
below in Figure 10. The semantics is fairly standard, but we elucidate some key aspects here.
First, the operational semantics checks that dereferences are memory safe, i.e., that the lookup or
34                                                                                                  Trovato et al.


mutation of 𝑥 .𝑓 only occurs when 𝑥 belongs to the allocated set 𝐴 (in particular, 𝑥 is not nil). If this
does not hold, then the error state ⊥ is reached. We define ⊥ to be a sink state, and any command
on ⊥ transitions to ⊥ itself. Second, allocation adds a fresh location (a new element distinct from
all the locations in the current universe) to the universe of locations and to the allocated set 𝐴.
The heap 𝐻 is also extended, mapping the new location to fixed default values default𝑓 for each
𝑓 ∈ F𝑚 . Correspondingly, deallocation removes the deallocated location from 𝐴. We do not allow
double deallocation, and doing so reaches the error state ⊥. Finally, functions have call-by-value
semantics.

C     Translation of FL to FORD
Translation of FL to FORD is given in Figure 11. As FL is just FORD extended with the support
and cloud operators, the translation becomes straightforward once these have been handled. We
denote the translation of 𝜑 into FORD as ∇(𝜑).
  Recall that𝑀 |= [𝜑] iff 𝑀 |= 𝜑. The translation to FORD mimics this: ∇( [𝜑]) = 𝜑.
  Intuitively, ∇(Sp(𝜑)) will be the set containing the locations in the support of 𝜑. For formulas
not involving recursive functions, this is straightforward. For example, Sp(key(𝑥) = key(𝑦)) would
be the locations {𝑥, 𝑦}. The interaction with cloud is as expected: Sp( [𝜑]) = 𝜙.
  The support of a recursive function will itself be a recursive definition, defined as the lfp of the
support of the function.
  For example, let us look at the following list definition:
      List (𝑥) := ite(𝑥 = nil, ⊤, (next (𝑥) = next (𝑥)) ∧ List ( [next (𝑥)]) ∧ 𝑥 ∉ Sp(List ( [next (𝑥)])))
Notice that the definition refers to the ’support of a list’. We define ∇(Sp(List (𝑥))) as SpList (𝑥),
where
                SpList (𝑥) :=lfp ∇(Sp(ite(𝑥 = nil, ⊤, (next (𝑥) = next (𝑥)) ∧ List ( [next (𝑥)])
                                         ∧𝑥 ∉ Sp(List ( [next (𝑥)])))))
     Simplifying,

                         SpList (𝑥) :=lfp ite(𝑥 = nil, 𝜙, {𝑥 } ∪ SpList (next (𝑥))))
   This is what we expect intuitively. If 𝑥 = nil, then the support of the list is empty. Otherwise, it
is the head of the list union the support of the rest of the list.

D      Details for Section 4: Base Logic
D.1      Proof of Lemma 4.1
     Proof.      (1) By structural induction on 𝛼. Most rules combine supports of smaller formulae,
          and hence are subsets of 𝑑𝑜𝑚(ℎ) (including that for disjunction). The rule for 𝑥 −𝑓 𝑦, when
          the support is defined, 𝑠 (𝑥) ∈ 𝑑𝑜𝑚(ℎ).
      (2) By structural induction on 𝛼. If 𝛼 = 𝛿, a heap-independent formula, then Supp(𝛼, 𝑠, ℎ) = ∅ =
          Supp(𝛼, 𝑠, ℎ ′ ). If 𝛼 = 𝑥 −𝑓 𝑦, note that if support of 𝛼 wrt ℎ is not ⊥, it must be 𝑆 = {𝑠 (𝑥)}.
          Then since ℎ and ℎ ′ agree on 𝑠 (𝑥), 𝑠 (𝑥) is in 𝑑𝑜𝑚(ℎ ′ ) as well, and Supp(𝛼, 𝑠, ℎ ′ ) = {𝑠 (𝑥)} = 𝑆.

          If 𝛼 = ∃𝑦.(𝑥 −𝑓  𝑦 : 𝛼 ′ ), notice that 𝑆 = {𝑠 (𝑥)} ∪ Supp(𝛼 ′, 𝑠 ′, ℎ), where 𝑠 ′ = 𝑠 [𝑦 ↦→
          ℎ(𝑓 ) (𝑠 (𝑥))]. But since 𝑠 (𝑥) is in 𝑆, 𝑑𝑜𝑚(ℎ ′ ) contains it and agrees with pointers on 𝑠 (𝑥),
          and hence ℎ ′ (𝑓 ) (𝑠 (𝑥)) = ℎ(𝑓 ) (𝑠 (𝑥)). Hence Supp(∃𝑦.(𝑥 −𝑓  𝑦 : 𝛼, 𝑠, ℎ ′ ) = {𝑠 (𝑥)} ∪
          Supp(𝛼 ′, 𝑠 ′, ℎ ′ ) = {𝑠 (𝑥)} ∪ Supp(𝛼 ′, 𝑠 ′, ℎ) (by induction hypothesis) = Supp(𝛼, 𝑠, ℎ).
FO-Complete Program Verification for Heap Logics                                                                     35


                                                               < 𝑦, 𝜎 >⇓𝑒 𝑣
                              error                                                        assn
              < 𝑠, ⊥ >⇓ ⊥                            < 𝑥 ≔ 𝑦, 𝜎 >⇓ 𝜎 (𝑆) [𝑥 ← 𝑣]

        𝑆 (𝑦) ∈ 𝐴         < 𝑓 (𝑦), 𝜎 >⇓𝑒 𝑣                                𝑆 (𝑦) ∉ 𝐴
                                                deref                                         badderef
        < 𝑥 ≔ 𝑦.𝑓 , 𝜎 >⇓ 𝜎 (𝑆) [𝑥 ← 𝑣]                             < 𝑥 ≔ 𝑦.𝑓 , 𝜎 >⇓ ⊥

         < 𝑦, 𝜎 >⇓𝑒 𝑣          < 𝑥, 𝜎 >⇓𝑒 𝑤                             {𝑆 (𝑦), 𝑆 (𝑥)} ⊈ 𝐴
                                                        mut                                     badmut
   < 𝑦.𝑓 ≔ 𝑥, 𝜎 >⇓ 𝜎 (𝐻 ) [𝑓 ← 𝑓 [𝑣 ← 𝑤]]]                             < 𝑦.𝑓 ≔ 𝑥, 𝜎 >⇓ ⊥

                         𝑎∉𝐴          𝐻 ′ = 𝜆𝑓 , 𝑥 .ite(𝑥 = 𝑎, default 𝑓 , 𝐻 (𝑓 ) (𝑥))
                                                                                            alloc
                              < alloc(𝑥), 𝜎 >⇓ (𝑆 [𝑥 ← 𝑎], 𝐻 ′, 𝐴 ∪ {𝑎})

          𝑎∈𝐴          < 𝑥, 𝜎 >⇓𝑒 𝑎                                                         𝑆 |= 𝜂
                                              free                                                         assume
      < free(𝑥), 𝜎 >⇓ 𝜎 [𝐴 ← 𝐴\{𝑎}]                                               < assume(𝜂), 𝜎 >⇓ 𝜎

           𝑆 |= 𝜂       < 𝑠 1, 𝜎 >⇓ 𝜎1                                 𝑆 ̸ |= 𝜂        < 𝑠 2, 𝜎 >⇓ 𝜎2
                                              if-true                                                    if-false
        < if 𝜂 then 𝑠 1 else 𝑠 2, 𝜎 >⇓ 𝜎1                          < if 𝜂 then 𝑠 1 else 𝑠 2, 𝜎 >⇓ 𝜎2

                                      < 𝑠 1, 𝜎 >⇓ 𝜎1          < 𝑠 2, 𝜎1 >⇓ 𝜎2
                                                                                  seq
                                                < 𝑠 1 ; 𝑠 2, 𝜎 >⇓ 𝜎2

         < 𝑔, 𝜎𝑔 >⇓ 𝜎𝑔′     𝜎𝑔 ≼ 𝜎          {𝜎 ′ (𝑆) (𝑦1 ), . . . , 𝜎 ′ (𝑆) (𝑦𝑚 )} ⊆ 𝜎𝑔′ (𝐴)
                                ′
             (𝜎 (𝐴)\𝜎𝑔 (𝐴)) ∩ 𝜎𝑔 (𝐴) = 𝜙           𝐴′ = (𝜎 (𝐴)\𝜎𝑔 (𝐴)) ∪ 𝜎𝑔′ (𝐴)
   𝑆 = 𝜆𝑥 .ite(𝑆 (𝑥) ∈ 𝜎 (𝐴)\𝜎𝑔 (𝐴), 𝑆 (𝑥), 𝜎𝑔 (𝑆) (𝑥)) with domain {𝑥 | 𝑆 (𝑥) ∈ 𝐴′ }
    ′                                            ′

𝐻 = 𝜆𝑓 .𝑖𝑡𝑒 (𝑓 ∉ dom(𝜎𝑔 (𝐻 )), 𝜎 (𝐻 ) (𝑓 ), 𝜆𝑥 .ite(𝑥 ∉ 𝜎𝑔′ (𝐴), 𝜎 (𝐻 ) (𝑓 ) (𝑥), 𝜎𝑔′ (𝐻 ) (𝑓 ) (𝑥)))
 ′
                                                                                                            call-by-value𝑛,𝑚
                        < 𝑦1, . . . , 𝑦𝑚 ≔ 𝑔(𝑥 1, . . . , 𝑥𝑛 ), 𝜎 >⇓ (𝑆 ′, 𝐻 ′, 𝐴′ )


Fig. 10. Operational semantics of the programming language. Here, 𝜎 = (𝑆, 𝐻, 𝐴) denotes a non-fail state of
the program. The error state is denoted by ⊥. For each sort 𝜏, a ’default’ value is fixed. default 𝑓 denotes the
default value of the sort of the codomain of the function. By 𝜎 (𝑆) [𝑥 ← 𝑣], we mean (𝑆 [𝑥 ← 𝑣], 𝐻, 𝐴). By
dom(𝑋 ), we mean the domain of 𝑋 . By (𝑆 1, 𝐻 1, 𝐴1 ) ≼ (𝑆 2, 𝐻 2, 𝐴2 ), we mean 𝐴1 ⊆ 𝐴2 and if 𝑆 1 (𝑥) ∈ 𝐴1 then
𝑆 2 (𝑥) = 𝑆 1 (𝑥) and 𝐻 1 (𝑓 )(𝑥) = 𝐻 2 (𝑓 )(𝑥) for each 𝑓 ∈ dom(𝐻 1 ). In other words, (𝑆 1, 𝐻 1, 𝐴1 ) is a restriction
(𝑆 2, 𝐻 2, 𝐴2 ). Here, assignment of a constant, data field dereference, etc. have not been written as separate
rules, as those are similar to those above.




         Let’s now consider 𝛼 = ite(𝛾, 𝛼 ′, 𝛽 ′ ), and assume its support in ℎ, 𝑆, is not ⊥. Then
         Supp(𝛾, 𝑠, ℎ) cannot be ⊥, and since it is a subset of 𝑆, by the induction hypothesis, Supp(𝛾, 𝑠, ℎ ′ ) =
         Supp(𝛾, 𝑠, ℎ). Note also that ℎ ⇂ Supp(𝛾, 𝑠, ℎ) = ℎ ′ ⇂ Supp(𝛾, 𝑠, ℎ ′ ), and hence (𝑠, ℎ ⇂
         Supp(𝛾, 𝑠, ℎ)) |= 𝛾 iff (𝑠, ℎ ′ ⇂ Supp(𝛾, 𝑠, ℎ ′ )) |= 𝛾. Consider the first case when (𝑠, ℎ, Supp(𝛾, 𝑠, ℎ)) |=
         𝛾 and Supp(𝛼, 𝑠, ℎ) is not ⊥. Then the latter is a subset of 𝑆, and by induction hypothesis,
         Supp(𝛼, 𝑠, ℎ ′ ) = Supp(𝛼, 𝑠, ℎ), which proves our claim. Similarly, in the second case, when
36                                                                                                Trovato et al.


                                    ∇(⊤) = ⊤
                                    ∇(⊥) = ⊥
                                     ∇(𝑐) = 𝑐
                                     ∇(𝑥) = 𝑥
                    ∇(𝑓 (𝑡 1, . . . , 𝑡𝑛 )) = 𝑓 (∇(𝑡 1 ), . . . , ∇(𝑡𝑛 )) for any function 𝑓
                           ∇(𝑡 1 = 𝑡 2 ) = (∇(𝑡 1 ) = ∇(𝑡 2 ))
                    ∇(𝑅(𝑡 1, . . . , 𝑡𝑛 )) = 𝑅(∇(𝑡 1 ), . . . , ∇(𝑡𝑛 )) for any relation 𝑅
                            ∇(𝛼 ∧ 𝛽) = ∇(𝛼) ∧ ∇(𝛽)
                            ∇(𝛼 ∨ 𝛽) = ∇(𝛼) ∨ ∇(𝛽)
                                 ∇(¬𝜑) = ¬∇(𝜑)
                    ∇(𝑖𝑡𝑒 (𝛾 : 𝛼, 𝛽)) = 𝑖𝑡𝑒 (∇(𝛾) : ∇(𝛼), ∇(𝛽))
                   ∇(𝑖𝑡𝑒 (𝛾 : 𝑡 1, 𝑡 2 )]) = 𝑖𝑡𝑒 (∇(𝛾) : ∇(𝑡 1 ), ∇(𝑡 2 ))
             ∇(𝑆𝑝 (⊤)) = ∇(𝑆𝑝 (⊥)) = 𝜙
                            ∇(𝑆𝑝 (𝑐)) = ∇(𝑆𝑝 (𝑥)) = 𝜙
                                              Ð                Ð
               ∇(𝑆𝑝 (𝑓 (𝑡 1, . . . , 𝑡𝑛 ))) = 𝑛𝑖=1 {𝑡𝑖 } ∪ 𝑛𝑖=1 ∇(𝑆𝑝 (𝑡𝑖 )) if 𝑓 ∈ F𝑚
                                              Ð𝑛
               ∇(𝑆𝑝 (𝑓 (𝑡 1, . . . , 𝑡𝑛 ))) = 𝑖=1 ∇(𝑆𝑝 (𝑡𝑖 )) if 𝑓 ∉ F𝑚
                     ∇(𝑆𝑝 (𝑆𝑝 (𝜑))) = ∇(𝑆𝑝 (𝜑))
                      ∇(𝑆𝑝 (𝑆𝑝 (𝑡))) = ∇(𝑆𝑝 (𝑡))
                     ∇(𝑆𝑝 (𝑡 1 = 𝑡 2 )) = Ð   ∇(𝑆𝑝 (𝑡 1 )) ∪ ∇(𝑆𝑝 (𝑡 2 ))
               ∇(𝑆𝑝 (𝑅(𝑡 1, . . . , 𝑡𝑛 ))) = 𝑛𝑖=1 ∇(𝑆𝑝 (𝑡𝑖 )) for 𝑅 ∈ R
                      ∇(𝑆𝑝 (𝛼 ∧ 𝛽)) = ∇(𝑆𝑝 (𝛼)) ∪ ∇(𝑆𝑝 (𝛽))
                      ∇(𝑆𝑝 (𝛼 ∨ 𝛽)) = ∇(𝑆𝑝 (𝛼)) ∪ ∇(𝑆𝑝 (𝛽))
                         ∇(𝑆𝑝 (¬𝜑)) = ∇(𝑆𝑝 (𝜑))
               ∇(𝑆𝑝 (𝑖𝑡𝑒 (𝛾 : 𝛼, 𝛽))) = if 𝛾 then ∇(𝑆𝑝 (𝛾)) ∪ ∇(𝑆𝑝 (𝛼)) else ∇(𝑆𝑝 (𝛾)) ∪ ∇(𝑆𝑝 (𝛽))
               ∇(𝑆𝑝 (𝑖𝑡𝑒 (𝛾 : 𝑡 1, 𝑡 2 ))) = if 𝛾 then ∇(𝑆𝑝 (𝛾)) ∪ ∇(𝑆𝑝 (𝑡 1 )) else ∇(𝑆𝑝 (𝛾)) ∪ ∇(𝑆𝑝 (𝑡 2 ))
                        ∇(𝑆𝑝 ( [𝛼])) = 𝜙
                                              Ð
               ∇(𝑆𝑝 (𝐼 (𝑡 1, . . . , 𝑡𝑛 ))) = 𝑛𝑖=1 ∇(𝑆𝑝 (𝑡𝑖 )) ∪ 𝑆𝑝𝐼 (𝑡 1, . . . , 𝑡𝑛 ) for 𝐼 ∈ I,
                                             where 𝑆𝑝𝐼 (𝑥)    ¯ ≔lfp ∇(𝑆𝑝 (𝜌 𝐼 (𝑥)))
                                                                                  ¯ and 𝐼 (𝑥)  ¯ ≔lfp 𝜌 𝐼 (𝑥)
                                                                                                           ¯
                                ∇( [𝛼]) = ∇(𝛼)

Fig. 11. Translation from FL to FORD. For an FL formula 𝛼, the translated FORD formula is ∇(𝛼), recursively
defined above.



        (𝑠, ℎ ⇂ Supp(𝛾, 𝑠, ℎ)) ̸ |= 𝛾, Supp(𝛽, 𝑠, ℎ) is not ⊥, it is a subset of 𝑆, and by induction hypoth-
        esis, Supp(𝛽, 𝑠, ℎ 1 ) = Supp(𝛽, 𝑠, ℎ), which also proves our claim.

        The cases for 𝛼 = 𝛼 ′ ⊕ 𝛽 ′ are trivial, and follow directly from the inductive hypothesis.

     (3) Follows from (2) since ℎ ⇂ 𝑆 agrees with ℎ on 𝑆.
     (4) Heaplet ℎ agrees with ℎ 1 on 𝑑𝑜𝑚(ℎ 1 ) = Supp(𝛼, 𝑠, ℎ 1 ), and so Supp(𝛼, 𝑠, ℎ) = 𝑑𝑜𝑚(ℎ 1 )
         (by (2) above). Similarly, heaplet ℎ agrees with ℎ 2 on 𝑑𝑜𝑚(ℎ 2 ) = Supp(𝛼, 𝑠, ℎ 2 ), and so
         Supp(𝛼, 𝑠, ℎ) = 𝑑𝑜𝑚(ℎ 2 ). Hence 𝑑𝑜𝑚(ℎ 1 ) = 𝑑𝑜𝑚(ℎ 2 ).
                                                                                                    □

D.2    Proof of Lemma 4.2
     (1) Proved by structural induction on 𝛼. Base cases are easy.
FO-Complete Program Verification for Heap Logics                                                          37


        Consider 𝛼 = ∃𝑦.𝑥 −𝑓 𝑦 : 𝛼 ′ . and (𝑠, ℎ) |= 𝛼. Then 𝑠 (𝑥) ∈ 𝑑𝑜𝑚(ℎ), and hence Supp(𝛼, 𝑠, ℎ) =
        {𝑠 (𝑥)} ∪ Supp(𝛼 ′, 𝑠 ′, ℎ), where 𝑠 ′ = 𝑠 [𝑦 → ℎ(𝑓 ) (𝑠 (𝑥))] and (𝑠 ′, ℎ) |= 𝛼 ′ . By induction hy-
        pothesis Supp(𝛼 ′, 𝑠 ′, ℎ) = 𝑑𝑜𝑚(ℎ). Hence Supp(𝛼, 𝑠, ℎ) = 𝑑𝑜𝑚(ℎ).

        Consider 𝛼 = 𝛼 1 ∗ 𝛼 2 , and (𝑠, ℎ) |= 𝛼. Then there are two heaplets ℎ 1, ℎ 2 of ℎ, the unions
        of these domains being the domain of ℎ, and (𝑠, ℎ𝑖 ) |= 𝛼𝑖 , 𝑖 = 1, 2. It follows by induc-
        tion hypothesis that Supp(𝛼𝑖 , 𝑠, ℎ𝑖 ) = 𝑑𝑜𝑚(ℎ𝑖 ). By Lemma 4.1, (4) and (3), it follows that
        Supp(𝛼𝑖 , 𝑠, ℎ) = 𝑑𝑜𝑚(ℎ𝑖 ). Hence Supp(𝛼 1 ∗ 𝛼 2, 𝑠, ℎ) is Supp(𝛼 1, 𝑠, ℎ) ∪ Supp(𝛼 2, 𝑠, ℎ) (by def-
        inition), which is equal to 𝑑𝑜𝑚(ℎ 1 ) ∪ 𝑑𝑜𝑚(ℎ 2 ) = 𝑑𝑜𝑚(ℎ). The cases for 𝛼 1 ⊕ 𝛼 2 , where
        ⊕ ∈ {∧, ∧ ∧, ∨} as well as that for ite expressions are similar.

     (2) Assume there are two subheaplets that satisfy 𝛼. By (1), the supports of 𝛼 in each of them
         would be their own domains. But by Lemma 4.1 (4), the heaplets of these domains must be
         the same. Hence the heaplets are identical.                                              □

E    Details for Section 4: Extended logic SL-FL
The semantics of this logic extends the semantics on the base logic in the following ways. First,
we assume that each background sort is a complete lattice (for flat sorts like arithmetic, we can
introduce a bottom element and a top element to obtain a complete lattice). Next, we treat the
equations defining Supp in Figure 5 as recursive definitions with least fixpoint semantics, with ⊆
over sets as ordering.
   We add support definitions for recursively defined predicates and functions:
                                    Supp(𝑅(𝑥), 𝑠, ℎ) = Supp(𝜌 𝑅 (𝑥), 𝑠, ℎ)
                                 Supp(𝐹 (𝑥), 𝑠, ℎ) = Supp(𝜇 𝐹 (𝑥), 𝑠, ℎ)
where 𝑅(𝑥) = 𝜌 𝑅 (𝑥) and 𝐹 (𝑥) = 𝜇 𝐹 (𝑥) are the definitions of 𝑅 and 𝐹 , respectively. We can show that
the least fixpoint of the above equations defining the map Supp satisfies the properties described in
Lemma 4.1 for the extended logic as well.
   The semantics of SL-FL is now easy to define. We modify the semantics given in Figure 5 as
follows, defining the semantics for recursively defined predicates:
               (𝑠, ℎ) |= 𝑅(𝑥)     iff   (𝑠, ℎ) |= 𝜌 (𝑥), where 𝑅’s definition is 𝑅(𝑥) = 𝜌 (𝑥)
  We can prove lemmas analogous to Lemma 4.2 for the extended logic.
  Finally, we can translate the extended logic to frame logic as well, modifying the translation
given in Figure 6 for ite formulas and translating definitions:

                             Π(ite(𝛼 ′, 𝛼, 𝛽)) = ite(Π(𝛼 ′ ), Π(𝛼), Π(𝛽))
                                    Π(𝑝 (𝑡)) = 𝑝 (𝑡)
                                   Π(𝑅(𝑥)) ®          ®
                                                 = 𝑅(𝑥)
                                    Π(𝑥 .𝑓 )) = 𝑓 (𝑥)
                                    Π(𝑓 (𝑡)) = 𝑓 (Π(𝑡))
                              Π(ite(𝛼, 𝑡, 𝑡 ′ )) = ite(𝛼, Π(𝑡), Π(𝑡 ′ )
                                    Π(𝐹 (𝑡)) = 𝐹 (Π(𝑡))
                        Π( 𝑅(𝑥)
                              ® :=lfp 𝜌 (𝑥)
                                          ® ) = 𝑅(𝑥)  ® :=lfp Π(𝜌 (𝑥))
                                                                     ®
                        Π( 𝐹 (𝑥)
                              ® :=lfp 𝜇 (𝑥)
                                          ® ) = 𝑅(𝑥)  ® :=lfp Π(𝜇 (𝑥))
                                                                     ®
    We can now prove the lemma analogous to Lemma 4.3:
   Lemma E.1. Let 𝑔 be a global heap (a heaplet with domain 𝐿𝑜𝑐) and 𝑠 be a store. For frame logic
formulas, we interpret the store as an FO interpretation of variables. Let 𝛼 be an SL-FL formula. Then
38                                                                                                 Trovato et al.


       • 𝑔 |=𝑠 Π(𝛼) iff there exists a heaplet ℎ of 𝑔 such that (𝑠, ℎ) |= 𝛼.
       • If 𝑔 |=𝑠 Π(𝛼), then Supp(𝛼, 𝑠, 𝑔) is equal to the value of Sp(Π(𝛼)) in 𝑔.                            □

F     Validating Verification Conditions
In this section, we describe our validity procedure for checking the quantifier-free frame logic
verification conditions generated by the mechanism described in Section 5. Our technique has
two stages. In the first stage, we translate the quantifier-free FL formulas to quantifier-free FORD
formulas in a way that preserves validity. Recall that quantifier-free FL is simply an extension of
quantifier-free FORD with the support Sp(·) and cloud [·] operators. Intuitively, our translation
encodes the semantics of these operators in FORD itself. In the second stage, we reason with the
quantifier-free FORD formulas using natural proofs, a mechanism developed in prior work [38, 54,
59].

F.1     Stage 1: Translating Quantifier-Free FL to Quantifier-Free FORD
The first stage of our reasoning mechanism translates FL formulas to FORD formulas. The key idea
is to encode the semantics of the Sp and [·] operators within FORD itself. This process introduces
new recursive definitions corresponding to the support of existing recursive definitions.
   Let us denote the translation by ∇. This function takes as input a quantifier-free FL formula (or
term) containing the Sp and [·] operators and outputs an FORD formula (resp. term). We describe
the formal translation in Appendix C and provide intuition here. First, we obviously have that for
any FL formula 𝛼 that does not mention the support or cloud operators, ∇(𝛼) = 𝛼.
   Next, to encode the Sp operator, it turns out that we can essentially mimic the equations describing
the semantics of Sp (Figure 2)! This is easy to see for formulas that do not contain recursively
defined symbols. For example, ∇(Sp(𝑓 (𝑥) = 𝑦)) = {𝑥 } for a mutable function 𝑓 ∈ F𝑚 , since
∇(𝑓 (𝑥) = 𝑦) = ∇(𝑓 (𝑥)) ∪ ∇(𝑦) = {𝑥 } ∪ ∅. Similarly, ∇(Sp(𝛼 ∧ 𝛽)) = ∇(Sp(𝛼)) ∪ ∇(Sp(𝛽)). In this
way, the Sp operator can be ‘compiled away’ by simply following the equations in Figure 2.
   However, this does not work for recursively defined symbols. For example, recall the definition
of List (𝑥) written using the cloud operator:
      List (𝑥) :=lfp ite(𝑥 = nil, ⊤, next (𝑥) = next (𝑥) ∧ List ( [next (𝑥)]) ∧ 𝑥 ∉ Sp(List ( [next (𝑥)])))
     Using the recipe described above, the support of List (𝑥) yields the following equation:

Sp(List (𝑥)) = Sp(ite(𝑥 = nil, ⊤, next (𝑥) = next (𝑥) ∧ List ( [next (𝑥)]) ∧ 𝑥 ∉ Sp(List ( [next (𝑥)]))))
                = ite(𝑥 = nil, ∅, {𝑥 } ∪ Sp(List ( [next (𝑥)]))

where we have expanded Sp on a cloud expression using the equation Sp( [𝛼]) = ∅.
   We cannot compile away the Sp operator in this case. However, recall that the Sp operator is the
least interpretation satisfying the equations in Figure 2. We therefore introduce a new recursively
defined symbol SpList , defined by
                           SpList (𝑥) :=lfp ite(𝑥 = nil, ∅, {𝑥 } ∪ SpList ( [next (𝑥)]))
and we then translate Sp(List (𝑥)) to SpList (𝑥). The latter is now an expression in FORD mentioning
the newly created recursive definition. In general, our translation creates a new recursively defined
symbol Sp𝐼 for every 𝐼 ∈ I corresponding to its support.
  Finally, the encoding of the [·] operator is trivial. Since support expressions were eliminated in
the previous step, [𝛼] is identical to 𝛼. Therefore, we simply ignore it in the translation. In particular,
the recursive sub-expression SpList ( [next (𝑥)]) in the above definition becomes SpList (next (𝑥)) in
the final translation to FORD.
FO-Complete Program Verification for Heap Logics                                                                                 39


F.2     Stage 2: Reasoning with FORD Formulas using Natural Proofs and SMT Solvers
The above translation of frame logic formulas results in FORD formulas that are quantifier-free (i.e.,
all free variables are implicitly universally quantified). Furthermore, they have the special form
that functions from the location sort map to either the location sort or a background sort, but no
function maps background sorts to the location sort. Hence they are part of a special fragment with
“one-way” definitions, Loneway fragment.
   Natural proofs [38, 54, 59] are a sound but incomplete technique for proving validity of FORD
formulae. It works by treating recursive definitions to have fixpoint semantics (rather than least
fixpoint) and hence obtaining a first-order formula. It then instantiates the recursive definitions
(similar to instantiating the quantifier for these definitions) on terms of depth 𝑑 (for larger and larger
𝑑), and obtaining quantifier-free formulas. Validating these quantifier-free formulas is performed
using an SMT solver. The foundations of this technique [38] show that the technique is in fact a
complete technique for dealing with first-order formulae (where recursive definitions have fixpoint
semantics). Furthermore, in practice, natural proofs have been shown useful for heap verification
of other logics. We can hence validate verification conditions using this automated technique.

G     Details of Evaluation
G.1      Benchmark Suite
Table 2 summarizes our benchmark suite. We report in addition to lines of code and annotations,
(specification, contracts, loop invariants, etc.) and the number of lemmas needed for each data
structure class.


      Data Structure        Operations            Lines of             Lines of         Rec. Defs.    No. of unique     Lemmas
                                              Code+Annot. (FL)   Code +Annot.(SL-FL )                rec def heaplets
                              Append                 30                   29                2                1            0
                              Copy All               32                   33                2                1            0
                               Delete                35                   35                2                1            0
                                Find                 34                   35                2                1            0
                            Insert Back              32                   32                2                1            0
    Singly Linked List
                            Insert Front             21                   21                2                1            0
                              Reverse                33                   33                2                1            0
                           Insertion Sort            60                   62                4                1            1
                             Merge Sort             107                  110                4                1            1
                             Quicksort              145                  152                5                1            1
                            Insert Back              38                   44                2                1
                            Insert Front             36                   41                2                1
    Doubly Linked List                                                                                                    0
                             Delete Mid              50                   65                4                2
                             Insert Mid              56                   77                4                2
                               Delete                40                   42                4                1
       Sorted List              Find                 44                   47                4                1            1
                               Insert                44                   46                3                1
                            Delete Front             61                   61                4                2
       Circular List            Find                 61                   62                4                2            1
                            Insert Front             42                   42                4                2
                               Delete               113                  120                4                1
                                Find                 76                   76                4                1
           BST
                               Insert                86                   88                4                1            2
                            Rotate Right             58                   59                4                1
                             BST to List             94                   90                7                2
           Tree          In-order Traversal          65                   65                3                1            0
                               Delete               154                  158                                              4
          Treap                                                                             6               1
                                Find                 95                   97                                              2
           RBT                 Insert               193                  218                5               1             2
Table 2. List of benchmarks, the lines of code, the number of recursive definitions and the number of these
with different heaps, and the number of lemmas needed to prove the benchmark.
40                                                                                                                  Trovato et al.


  Table 3 contains examples of pre- and post-conditions for sample routines. FL specifications use
the Sp operator to express disjointness of data structures. We also note that specifications may
need to be strengthened for verification. For example, BST Remove Root requires the following
constraint in the post-condition (Old (Min(𝑥)) ≤ Min(𝑟𝑒𝑡)) ∧ (Max (𝑟𝑒𝑡) ≤ Old (Max (𝑥))) to verify.

 Benchmark               Pre Condition                 Post Condition
                                                       Sorted (ret ) ∧ Keys (ret ) = Old (Keys (𝑥 ) ) ∪ {𝑘 }
 Sorted Insert           Sorted (𝑥 )
                                                       ∧ ite (Old (Min(𝑥 ) ) < 𝑘, Min(ret ) = Old (Min(𝑥 ) ), Min(ret ) = 𝑘 )
                         Sorted (𝑥 )∧ Sorted (𝑦)
                                                      Sorted (ret ) ∧ Keys (ret ) = Old (Keys (𝑥 ) ) ∪ Old (Keys (𝑦) )
 Sorted Concat           ∧ Max (𝑥 ) ≤ Min(𝑦)
                                                      ∧ ite (𝑥 = nil, Min(ret ) = Old (Min(𝑦) ), Min(ret ) = Old (Min(𝑥 ) ) )
 (part of Quicksort)     ∧ (𝑆𝑝 (Sorted (𝑥 ) )
                                                      ∧ ite (𝑦 = nil, Max (ret ) = Old (Max (𝑥 ) ), Max (ret ) = Old (Max (𝑦) ) )
                           ∩ 𝑆𝑝 (Sorted (𝑦) ) ) = ∅
                                             (a) Example FL Pre and Postconditions
 Benchmark                Pre Condition                             Post Condition
                          (𝑥 ≠ nil)
 BST Rotate Right                                                   BST (𝑟𝑒𝑡 ) ∧ (Keys (𝑟𝑒𝑡 ) = Old (Keys (𝑥 ) ) )
                          ∗(BST (𝑥 )∧ ∧(left (𝑥 ) ≠ nil) )
                          (𝑥 ≠ nil) ∗ (∃lft.(𝑥 −left lft :
 BST Remove Root          (∃rht.(𝑥 −right rht : ( (𝑘 = key (𝑥 ) ) BST (𝑟𝑒𝑡 ) ∧ (Keys (𝑟𝑒𝑡 ) = (Old (Keys (𝑥 ) ) ) \ {𝑘 } )
 (part of BST Delete)     ∗(BST (lft ) ∧ (Max (lft ) < 𝑘 ) )        ∧(Old (Min(𝑥 ) ) ≤ Min(𝑟𝑒𝑡 ) ) ∧ (Max (𝑟𝑒𝑡 ) ≤ Old (Max (𝑥 ) ) )
                          ∗(BST (𝑟ℎ𝑡 ) ∧ (𝑘 < Min(rht ) ) ) ) ) ) )
                                          (b) Example SL-FL Pre and Post conditions
Table 3. Example Pre and Post Conditions. 𝑥 and 𝑦 are of type Loc, and 𝑘 is of type Int. ret is a pointer to the
data structure returned by the routines.



     Table 4 contains some examples of lemmas used in our benchmarks.

                         Benchmark                                      Lemmas
                        Insertion Sort                          Sorted (𝑥 ) =⇒ List (𝑥 )
                          BST Find                  BST (𝑥 ) =⇒ Max (𝑥 ) < 𝑘 =⇒ 𝑘 ∉ Keys (𝑥 )
                                                               BST (𝑥 ) =⇒ 𝑛 ≠ nil =⇒
                         Tree to List
                                         ite (left (𝑥 ) = nil, Min(𝑥 ) = 𝑘𝑒𝑦 (𝑥 ), Min(𝑥 ) = Min(left (𝑥 ) ) )
                         Quicksort         𝑥 ≠ nil =⇒ Max (𝑥 ) ≤ Min(𝑦) =⇒ Min(𝑥 ) ≤ Min(𝑦)
                                                 Table 4. Example Lemmas




G.2     Definitions of Datastructures
The definitions of the FL data structures used in the benchmarks use explicit support and cloud
operators. The definition for singly-linked lists is as given below:
                       List (x) := ite(𝑥 = nil, ⊤, List (next (𝑥)) ∧ 𝑥 ∉ Sp(List ( [next (𝑥)]))
and the definition for doubly-linked lists is similar, with the addition of a constraint that if next (𝑥)
is not nil then its previous pointer should point back to 𝑥,
              Dll(𝑥) := ite(𝑥 = nil, ⊤, ite(next (𝑥) = nil, ⊤,
                                 𝑥 = prev(next (𝑥)) ∧ Dll(next (𝑥)) ∧ 𝑥 ∉ Sp(Dll( [next (𝑥)]))))
Next, to define sorted lists, we rely on an auxiliary definition of the minimum element in a list
and then a (non-decreasing) sorted list is simply a list where the front key is no greater than the
FO-Complete Program Verification for Heap Logics                                                         41


minimum value of its tail, which is itself also a sorted list:
        Min(𝑥) := ite(𝑥 = nil, +∞, ite(key(𝑥) < Min(next (𝑥)), key(𝑥), Min(next (𝑥))))
      Sorted (𝑥) := ite(𝑥 = nil, ⊤,
                        Sorted (next (𝑥)) ∧ 𝑥 ∉ Sp(Sorted ( [next (𝑥)])) ∧ key(𝑥) ≤ Min(next (𝑥)))
In our implementation of this definition, +∞ is simply an additional variable that is treated as
having an infinitely large value.
   For circular lists, we define list segments using the Lseg(·) definition and we then define a circular
list as empty or reaching itself through its next pointer,
             Lseg(𝑥, 𝑦) := ite(𝑥 = 𝑦, ⊤, ite(𝑥 = nil, ⊥,
                                 Lseg(next (𝑥), 𝑦) ∧ 𝑥 ∉ Sp(Lseg( [next (𝑥)], 𝑦))))
                Circ(𝑥) := ite(𝑥 = nil, ⊤, Lseg(next (𝑥), 𝑥) ∧ 𝑥 ∉ Sp(Lseg( [next (𝑥)], 𝑥)))
Our definition for binary search trees, like for sorted lists, relies on a definition of the minimum and
maximum values in a tree and the binary search property is specified by requiring the maximum
element in the left subtree to be less than the key of the root and the minimum element in the right
subtree to be greater than the key of the root. The definitions of Min and Max are similar to that
for sorted lists and so are omitted; we note that the default value for Max if 𝑥 is nil is −∞. Then,
the definition of a binary search tree is
   BST (𝑥) := ite(𝑥 = nil, ⊤,
                   BST (left (𝑥)) ∧ Max (left (𝑥)) < key(𝑥) ∧ BST (right (𝑥))
                    ∧ key(𝑥) < Min(right (𝑥)) ∧ 𝑥 ∉ Sp(BST ( [left (𝑥)]))
                    ∧ 𝑥 ∉ Sp(BST ( [right (𝑥)])) ∧ Sp(BST ( [left (𝑥)])) ∩ Sp(BST ( [right (𝑥)])) = ∅)
In addition to our normal requirement that 𝑥 not be in the support of either of the subtrees we also
specify here that the supports of the subtrees must be disjoint; together these properties express
that 𝑥 is indeed a tree.
   The definitions for Treaps and Red-Black Trees are similar to this definition for binary search
trees, augmented with their appropriate additional constraints, the max heap property on the
priorities in the Treap and the red-black property for Red-Black trees.
   The implementation of the max heap property for the Treap is in the same fashion as the binary
search property for binary-search trees, except that we just require that the priority of the root be
greater than the maximum priority of either subtree.
   For red-black trees we add a recursive definition which determines the (maximum) black-height
of a tree and then a tree is a red-black tree if both subtrees have the same black height and the root
is black or both children are black.

G.3    An Illustrative Example
In this section, we step through the VC generation of a program to illustrate the transformation
from an SL-FL annotated program to FL VCs.
   Given below is a program RevPrepend(x, y), which takes two linked lists and prepends the reverse
of the first onto the second. The program has two recursive functions, List and Keys, written in
SL-FL. Recall from Section 6 that the support of Old (.) is always empty.

List(x) := ite( x = nil, True, Exists y: next(x). (next(x) = next(x)) * List(y))
Keys(x) := ite( x = nil, EmptySetInt, SetAdd(Keys(next(x)), x))
42                                                                                             Trovato et al.


RevPrepend(x, y) returns(ret)
@pre: List(x) * List(y)
@post: List(ret) and (Keys(ret) = SetUnion( Old(Keys(x)), Old(Keys(y))))
(if (x = nil)
 then
   ret := y;
 else
   tmp := x.next;
   x.next := y;
   ret := RevPrepend(tmp, x);
)
return;

   First, we convert the recursive definitions and the program annotations into FL (see Fig 6 for the
translation). For instance, List becomes
             List (𝑥) := ite(𝑥 = nil, ⊤, ∃𝑦 : 𝑦 = next (𝑥). (next (𝑥) = next (𝑥)) ∧ List (𝑦)
                            ∧(Sp(next (𝑥) = next (𝑥)) ∩ Sp(List (𝑦))) = 𝜙)
Using Lemma 5.1, we eliminate the existential quantifier,
      List (𝑥) := ite(𝑥 = nil, ⊤, (next (𝑥) = next (𝑥)) ∧ (next (𝑥) = next (𝑥)) ∧ List ( [next (𝑥)])
                       ∧(Sp(next (𝑥) = next (𝑥)) ∩ Sp(List ( [next (𝑥)]))) = 𝜙)
   Observe that this mechanical translation introduces a blow-up in the size of the formula. For
example, it introduces a check if the supports of next (𝑥) = next (𝑥) and Sp(List ( [next (𝑥)])) are
disjoint. This can be simplified to just checking if 𝑥 is in the support of the latter. A more drastic
example of the translation introducing superfluous checks can be seen in the postcondition, which
gets translated to
                     List (𝑟𝑒𝑡) ∧ (Keys(ret) = Old (Keys(𝑥)) ∪ Old (Keys(𝑦)))∧
                  Sp(List (𝑟𝑒𝑡)) = Sp(Keys(ret) = Old (Keys(𝑥)) ∪ Old (Keys(𝑦)))
  One can check that the last conjunct always holds (the support of List and that of Keys is always
the same), and that the support of the entire expression is equal to the support of List (𝑟𝑒𝑡) ∧
(Keys(ret) = Old (Keys(𝑥)) ∪ Old (Keys(𝑦))). Thus, the post condition is equivalent to List (𝑟𝑒𝑡) ∧
(Keys(ret) = Old (Keys(𝑥)) ∪ Old (Keys(𝑦))). Our optimizations involve performing such simplifi-
cations syntactically, reducing the burden on the SMT solver. The following is an FL-annotated
version of RevPrepend.

List(x) := ite( x = nil, True, (next(x) = next(x)) and List([next(x)]) and
    Not(IsMember(x, Sp(List([next(x)])))))
Keys(x) := ite( x = nil, EmptySetInt, SetAdd(Keys(next(x)), x))

RevPrepend(x, y) returns(ret)
@pre: List(x) and List(y) and IsEmpty( SetIntersect( Sp(List(x)), Sp(List(y))))
@post: List(ret) and (Keys(ret) = SetUnion( Old(Keys(x)), Old(Keys(y))))

(if (x = nil)
 then
   ret := y;
 else
   tmp := x.next;
FO-Complete Program Verification for Heap Logics                                                     43


   x.next := y;
   ret := RevPrepend(tmp, x);
)
return;

   We shall not go over the entire VC generation in detail; we will just look at the interesting cases
involving the function call. The other BBs are straightforward. For example, the ’if’ case simply sets
𝑇 to be the conjunct of the precondition, 𝑥 = nil, and ret = 𝑦. Finally, it checks if the post-condition
holds. Since ret = 𝑦, this follows directly from the pre-condition. In the BBs checking dereference
safety, say, of 𝑡𝑚𝑝 := 𝑥 .next, 𝑇 will be the precondition and 𝑥 ≠ nil, and the VC will check if 𝑥 ∈ 𝐴
(where 𝐴 is just the support of the precondition).
   When calling RevPrepend(tmp, x), we need to ensure memory safety - that is, the locations
initially accessed by the function call is contained within the allocated set, motivating the need for
relaxed post-conditions. This is given by the following BB.

{List(x) and List(y) and IsEmpty( SetIntersect( Sp(List(x)), Sp(List(y))))}
# T = List(x) and List(y) and IsEmpty( SetIntersect( Sp(List(x)), Sp(List(y)))),
# A = Sp(T), Fr = {}, RD = {List, Keys}, H = \lambda f. f where f \in {next, key}
assume( x != nil);
# T <- T and x != nil
tmp := x.next;
# T <- T and tmp = next(x)
x.next := y;
# H1 = H[next <- lambda arg. ite(arg = x, y, next(arg))]
# List1 = List[H1], Keys1 = Keys[H1], RD1 = {List, Keys, List1, Keys1}
# Fr1 = {fr({x}, H, H1)}
{RP: List1(tmp) and List1(x) and IsEmpty( SetIntersect( Sp(List1(tmp)), Sp(List1(x))))}

The VC generated for this BB is (fr (𝑥, 𝐻, 𝐻 1) ∧𝑇 ) =⇒ (𝜑 ∧ Sp(𝜑) ⊆ 𝐴), where 𝜑 = (List1(𝑡𝑚𝑝) ∧
List1(𝑥) ∧ (Sp(List1(tmp)) ∩ Sp(List1(x)) = 𝜙)).
   To ensure tightness of the heap, we must characterize the heap after the function call. Inductively,
we know the portion of the heap modified by the function call is characterized by the postcondition
of RevPrepend(tmp, x). This motivates the function call rule.

{List(x) and List(y) and IsEmpty( SetIntersect( Sp(List(x)), Sp(List(y))))}
assume( x != nil)
tmp := x.next
x.next := y
ret := RevPrepend(tmp, x)
# Let PreCall = (List1(tmp) and List1(x) and IsEmpty( SetIntersect( Sp(List1(tmp)),
    Sp(List1(x)))))
# H2[next] = lambda arg. ite(Not(IsMember(arg, Sp(PreCall))), H1(next)(arg),
    next2(arg))
# H2[key] = lambda arg. ite(Not(IsMember(arg, Sp(PreCall))), H1(key)(arg), key2(arg))
# List2 = List1[H2], Keys2 = Keys1[H2]
# Let PostCall = (List2(ret) and (Keys2(ret) = SetUnion( Old(Keys1(tmp)),
    Old(Keys1(x)))) )
# T2 = T and PostCall
# A2 = (A\Sp(PreCall)) U Sp(PostCall)
# Fr2 = Fr1 U {fr(Sp(PreCall), H1, H2)}
# RD2 = RD1 U {List2, Keys2}
44                                                                                         Trovato et al.


{List2(ret) and (Keys2(ret) = SetUnion( Old(Keys(x)), Old(Keys(y))))}

The VC generated for this BB is (fr (𝑥, 𝐻, 𝐻 1) ∧ fr (Sp(PreCall), 𝐻 1, 𝐻 2) ∧𝑇 2) =⇒ 𝜑 ∧ Sp(𝜑) = 𝐴2,
where 𝜑 = List2(ret) ∧ (Keys2(ret) = (Old (Keys(𝑥)) ∪ Old (Keys(𝑦)))).
   We now describe a high-level proof of the validity of the VC. Recall that the contract of
RevPrepend tells us if we start with two disjoint lists and the program is executed - (1) the return is
a list whose keys are the union of the keys of the original two lists, and (2) the heap support of the
postcondition gives the ’modified’ heap of the program.
   From the validity of the previous BB, the precondition of 𝑅𝑒𝑣𝑃𝑟𝑒𝑝𝑒𝑛𝑑 (tmp, 𝑥) holds for the
function call. Thus, we can conclude that after the function call - (1) PostCall = List2(ret) ∧
(Keys2(ret) = Keys1(𝑥) ∪ Keys1(tmp)) holds, and (2) Sp(PostCall) is the modified heap of the call.
   We now prove 𝜑. It suffices to show Keys1(𝑥)∪Keys1(tmp) = Keys(𝑥)∪Keys(𝑦). To do so, observe
that only 𝑥 is modified before the function call. Thus, by the frame rule Fr1, Keys1(𝑦) = Keys(𝑦)
and Keys(tmp) = Keys1(next (𝑥)). The result follows.
   The proof of Sp(𝜑) = 𝐴2 is similar. By Fr1, it follows have Sp(List1(𝑦)) = Sp(List (𝑦)) and
Sp(List1(tmp)) = Sp(List (tmp)). It follows that Sp(PreCall) = 𝐴. Thus, 𝐴2 = Sp(PostCall) = Sp(𝜑).
