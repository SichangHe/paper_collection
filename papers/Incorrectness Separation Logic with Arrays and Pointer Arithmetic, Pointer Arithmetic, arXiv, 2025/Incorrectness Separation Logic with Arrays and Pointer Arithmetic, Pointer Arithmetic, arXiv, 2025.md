                                             Incorrectness Separation Logic with Arrays and
                                                           Pointer Arithmetic

                                                                Yeonseok Lee⋆ and Koji Nakazawa⋆⋆

                                                                   Nagoya University, Nagoya, Japan
arXiv:2503.00809v1 [cs.LO] 2 Mar 2025




                                               Abstract. Incorrectness Separation Logic (ISL) is a proof system de-
                                               signed to automate verification and detect bugs in programs manipulat-
                                               ing heap memories. In this study, we extend ISL to support variable-
                                               length array predicates and pointer arithmetic. Additionally, we prove
                                               the relative completeness of this extended ISL by constructing the weak-
                                               est postconditions. Relative completeness means that all valid ISL triples
                                               are provable, assuming an oracle capable of checking entailment between
                                               formulas; this property ensures the reliability of the proof system.

                                               Keywords: Program Verification · Separation Logic · Incorrectness Logic
                                               · Array · Completeness.


                                        1     Introduction
                                        1.1    Background
                                        The automation of software verification is a critical aspect of software engineer-
                                        ing, as it helps ensure the reliability of software systems at an economical cost.
                                        To achieve this, researchers and practitioners often rely on formal methods to
                                        verify software correctness and identify incorrectness.
                                            A classical yet influential formal method is Hoare Logic (HL) [6], which fo-
                                        cuses on verifying correctness. A Hoare triple is written as {P } C {Q}, where
                                        P is a precondition and Q is a postcondition. This triple states that for every
                                        state s satisfying P , if the command C terminates in state s′ , then s′ satisfies
                                        Q. Equivalently, if we let post(C, P ) denote the set of possible states after exe-
                                        cuting C from any initial state in P , then Q over-approximates post(C, P ), i.e.,
                                        post(C, P ) ⊆ Q.
                                            Recently, research has also focused on formal methods that verify incorrect-
                                        ness, aiming to identify the presence of bugs. Reverse Hoare Logic (RHL) [5] is
                                        one such method. The RHL triple is written as [P ] C [Q]1 , which indicates that
                                        for every state s′ in Q, s′ can be reached by executing C from some state s in
                                        ⋆
                                           lee.yeonseok.x2@s.mail.nagoya-u.ac.jp
                                        ⋆⋆
                                           knak@i.nagoya-u.ac.jp
                                         1
                                           In some literature, the notation [P ] C [Q] is used to denote a Hoare triple representing
                                           total correctness, which states that if C is executed in a state satisfying P , it always
                                           terminates, and the final state satisfies Q. However, in this paper, we adopt square
                                           brackets following the conventions established in prior works [10,11].
  2         Y. Lee and K. Nakazawa

  P . Here, Q under-approximates post(C, P ), i.e., post(C, P ) ⊇ Q. Note that the
  direction of inclusion is reversed from Hoare Logic (HL) to RHL. If Q represents
  an unexpected state and [P ] C [Q] is valid, we can conclude that this triple
  implies C contains a bug.
      To illustrate the difference between Hoare Logic (HL) and Reverse Hoare
  Logic (RHL), we present the following examples, which were also introduced in
  our previous work [9].

      – {⊤} x := y {⊤} is valid in HL but [⊤] x := y [⊤] is not valid in RHL. In the
        RHL setting, the state (x = 1 ∧ y = 2) (which satisfies ⊤ as a postcondition)
        cannot be reached from a state satisfying ⊤ by executing x := y.
      – {⊤} x := y {0 < x < 10 ∧ x = y} is not valid in HL, whereas [⊤] x := y [0 <
        x < 10 ∧ x = y] is valid in RHL. In HL, the final state (x = 10 ∧ y = 10)
        can be reached from ⊤ and does not satisfy (0 < x < 10 ∧ x = y), hence the
        triple is not valid.

      Another logic focusing on under-approximation is Incorrectness Logic (IL)
  [10], which has a similar form to RHL but embeds an additional exit condition
  into the postcondition: [P ] C [ǫ : Q], where ǫ can be ok for normal termination
  or er for erroneous termination.
      Separation Logic (SL), introduced by Reynolds [12], builds upon HL to enable
  modular reasoning about pointer-manipulating programs. Its key operator, the
  separating conjunction (∗), partitions the heap into disjoint parts, each of which
  can be reasoned about independently. A prominent feature of SL is the Frame
  rule:
                                      {P } C {Q}
                                                     ,
                                 {P ∗ R} C {Q ∗ R}
  which states that if C does not modify the portion of memory described by
  R, then R remains unaffected and can be “framed” into the pre- and postcondi-
  tions. This locality principle significantly improves the scalability of verifications
  for large programs. Numerous verification tools (e.g., Infer by Meta [2,3]) have
  adopted SL as their theoretical basis. Consider the following C code to demon-
  strate the Frame rule.
1 int *x = malloc(sizeof(int)); *x = 1;
2 int *y = malloc(sizeof(int)); *y = 2;
3 free(x);

  The Frame rule can express the situation.

                                {x 7→ 1} free(x) {emp}
                        {x 7→ 1 ∗ y 7→ 2} free(x) {emp ∗ y 7→ 2}

  When we call free(x), the block pointed to by x is deallocated, so the post-
  condition becomes {emp ∗ y 7→ 2}. Crucially, since the operation free(x) does
  not affect the block described by y, the Frame rule ensures that y remains
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic          3

  unchanged. This allows us to “frame” the y-part of the heap into the pre- and
  postconditions without requiring additional reasoning.
      By drawing upon these ideas, Incorrectness Separation Logic (ISL) was in-
  troduced by Raad et al. [11] to extend Incorrectness Logic (IL) with heap-
  manipulation features similar to those in Separation Logic (SL). They demon-
  strated that the naive application of the Frame rule is unsound in the IL setting.
  The following example from [11] illustrates this problem.

                             [x 7→ −] free(x) [ok : emp]
                    [x 7→ − ∗ x 7→ −] free(x) [ok : emp ∗ x 7→ −]

  The premise is valid, but the conclusion is not, since the conclusion means that
  every state satisfying the postcondition emp ∗ x 7→ − can be reached from some
  state satisfying the precondition x 7→ − ∗ x 7→ −, which is unsatisfiable. As a
  result, the inference is unsound. However, this issue can be resolved by intro-
  ducing the negative heap assertion x 67→, as demonstrated in [11]. This assertion
  indicates that x was once part of the heap but has since been deallocated.

                             [x 7→ −] free(x) [ok : x 67→]
                    [x 7→ − ∗ x 7→ −] free(x) [ok : x 67→ ∗x 7→ −]

  In this corrected version, both triples are valid. The precondition and postcon-
  dition of the conclusion are false, making the triple trivially valid.
      Both soundness and completeness are essential for logical proof systems to
  establish reliability. While soundness guarantees that every provable statement
  is valid, completeness ensures that all valid statements can be proven. However,
  Hoare Logic is famously known to be incomplete. To address this, Cook intro-
  duced the notion of relative completeness [4]. Relative completeness states that
  the logic is complete if an oracle exists to decide the validity of entailments.
  Thus, if a proof system is relatively complete, it can have strong reliability.


  1.2   Our Contribution: ISL with Arrays and Pointer Arithmetic

  In this paper, we introduce an extension of ISL by adding support for arrays
  and pointer arithmetic. Consider the following C code, which contains an error
  related to array handling.

1 int *array = (int *)malloc(10 * sizeof(int));
2 free(array + 1); // Error: Free the memory at a non-head position

  This code has an error because it attempts to free a heap cell that is not the head
  of the allocated block. Existing ISL systems [11,9] cannot describe this scenario
  due to their lack of support for array predicates. To address this limitation, in this
  paper, we introduce an extension of ISL to handle such cases. Our contributions
  are as follows.
4         Y. Lee and K. Nakazawa

    • Introducing ISL with arrays and pointer arithmetic (Section 2)
      We extend the existing ISL framework [11,9] by incorporating array predi-
      cates and pointer arithmetic. Our framework builds upon two existing Sepa-
      ration Logics: traditional array-based SL [1,8] and SL with arrays [7], where
      models incorporate memory blocks. Specifically, our approach utilizes ar-
      ray predicates with variable-size lengths [1,8], allowing for the description of
      more flexible arrays compared to predicates that specify only fixed lengths
      and starting points.
    • Defining weakest postcondition generating functions (Section 3)
      Following the methods of [5,9], we define a function constructing the weak-
      est postconditions and prove the expressiveness, a property that ensures
      these functions accurately describe the sets expressing the weakest postcon-
      ditions. This procedure is essential for proving relative completeness. It is
      worth noting that while Cook used weakest preconditions to prove the rela-
      tive completeness of Hoare Logic (HL) [4], our approach focuses on weakest
      postconditions. This is because HL relies on over-approximation, whereas
      Reverse HL and ISL use under-approximation.
      Our work extends this previous approach by proving expressiveness for heap
      manipulation rules involving arrays and pointer arithmetic. For other rules
      that do not involve heap manipulation, we rely on the results of [9], as these
      rules yield the same outcomes in both settings.
    • Proving relative completeness (Section 4)
      We prove the relative completeness of this extended ISL by following a
      method similar to that in [9].

2      Incorrectness Separation Logic
We define a modified version of ISL, extending ISL [11,9], to handle arrays and
pointer arithmetic. We assume a countably infinite set of variables, Var. We
use the metavariables x, y, z, . . . to denote variables and n to denote elements of
natural numbers.

2.1     Assertions
First, we introduce assertions in ISL, which are potentially infinite disjunctions
of existentially quantified symbolic heaps. Quantifier-free symbolic heaps consist
of equalities (x ≈ y) and inequalities (x 6≈ y) between terms, as well as weak
and strict inequalities (x ≤ y and x < y, respectively). They also include heap
predicates such as singleton heaps (t 7→ u), variable-length array predicates
(arr(t, t′ )), and negative array predicates (arr(t, t′ )).
     The negative array predicates (arr(t, t′ )) represent a set of consecutive nega-
tive heaps with sequential addresses. This extends the concept of negative heaps
(x 67→) from the original ISL [11], adapting it to handle arrays with consecutive
memory locations. x 67→ is an abbreviation of arr(x, x + 1) in our setting.
     Symbolic heaps are connected using the separating conjunction (∗). The log-
ical operators ∨, ∧, and ¬ are not permitted within symbolic heaps.
         Incorrectness Separation Logic with Arrays and Pointer Arithmetic          5

Definition 1 (Assertions of ISL).
   An assertion P is defined as follows, where I is finite or countably infinite
index set.


                      ∃−
                       →
                _
        P ::=          xi .ψi                                          Top-level
                i∈I
        ψ ::= ψ ∗ ψ                                             Symbolic Heaps
              | emp | t 7→ u | arr(t, t′ ) | arr(t, t′ )       Spatial Formulas
               | t ≈ t′ | t 6≈ t′ | t ≤ t′ | t < t′              Pure Formulas
         t ::= n | x | t + t′ | b(t) | e(t) | null                       Terms

     Here, we employ vector notation to represent   W a sequence.    For instance, −→
                                                                                    xi
                                                           →
                                                           −
denotes the sequence xi1 , . . . , xin . When I = ∅, i∈I ∃ xi .ψi is denoted by false.
     We ignore the order of disjuncts in assertions and atomic formulas in symbolic
heaps. Specifically, we identify the formulas ψ1 ∗ ψ2 and ψ2 ∗ ψ1 . Additionally, we
refer to a formula connected by ∗ and containing only atomic pure formulas as a
pure formula. We use the metavariable π to denote pure formulas. ψpure denotes
the symbolic heap obtained by extracting only the pure formulas from ψ.
     b(t) represents the head address of the memory block containing t, and e(t)
denotes the tail address of that block. We impose a constraint that t in b(t) or
e(t) cannot contain b or e. For example, terms like b(b(t)) are not allowed in this
setting.
     For brevity, we represent the full expression t0 R0 t1 ∗t1 R1 t2 ∗. . .∗tn−1 Rn−1
tn , where Ri ∈ {<, ≈}, by the shorter expression t0 R0 t1 R1 t2 . . . tn−1 Rn−1 tn .
For example, x < y ∗ y < z is written as x < y < z.

Definition 2 (term(t)). We define the set term(t) of terms for a term t as
follows.

             term(t + t′ ) = {t + t′ } ∪ term(t) ∪ term(t′ )
                term(b(t)) = {b(t)} ∪ term(t)
                term(e(t)) = {e(t)} ∪ term(t)
                  term(n) = {n},        term(x) = {x},     term(null) = ∅

Definition 3 (termS(ψ) and termS− (ψ)). We define the set termS(ψ) of terms
for a symbolic heap ψ as follows.

                termS(ψ1 ∗ ψ2 ) = termS(ψ1 ) ∪ termS(ψ2 )
                  termS(t 7→ u) = term(t) ∪ term(t + 1) ∪ term(u)
                termS(arr(t, t′ )) = termS(arr(t, t′ )) = termS(t ≈ t′ )
                                   = termS(t 6≈ t′ ) = termS(t ≤ t′ )
                                 = termS(t < t′ ) = term(t) ∪ term(t′ )
                      termS(emp) = ∅
6        Y. Lee and K. Nakazawa

Furthermore, we define

            termS− (ψ) = {r ∈ termS(ψ) | r is contains neither b nor e}.

    Note that termS(ψ) contains not only terms that appear freely in ψ but also
related terms, such as t + 1 in t 7→ u.
    For the semantics, we assume the set Val of values and the set Loc of
locations, such that Loc ⊆ Val and Val = N (non-negative integers). We
assume 0 denotes the null pointer and 0 ∈ Val \ Loc. Additionally, ⊥ 6∈ Val2
is used to track deallocated locations.
    A state σ ∈ State is defined as a triple (s, h, B) (often called a heap model).
A state consists of a store s ∈ Store, a heap h ∈ Heap, and a block set
B ∈ Blocks.
    A store is a total function from Var to Val ∪ {0}. For a store s, the notation
s[x 7→ v] represents the store defined as s[x 7→ v](x) = v and s[x 7→ v](y) = s(y)
for y 6= x.
    A heap is a finite partial function from Loc to Val∪{⊥}. The update h[l 7→ v]
for a heap h is defined analogously to s[x 7→ v]. Additionally, h[l 7→↑] represents
the heap defined by dom(h[l 7→↑]) = dom(h) \ {l}, and h[l 7→↑](l′ ) = h(l′ ) for
l 6= l′ . Two heaps h1 and h2 are disjoint if dom(h1 )∩dom(h2 ) = ∅. The operation
h1 ◦ h2 combines two disjoint heaps h1 and h2 and is defined as follows:
                               
                               h1 (l)
                                            if l ∈ dom(h1 ),
               (h1 ◦ h2 )(l) = h2 (l)        if l ∈ dom(h2 ),
                               
                                 undefined if l ∈ / dom(h1 ) ∪ dom(h2 ).
                               

The operation h1 ◦ h2 is undefined if h1 and h2 are not disjoint.
     For convenience, we sometimes denote dom+ (h) as the set of locations l
satisfying h(l) ∈ Val, and dom− (h) as the set of locations l satisfying h(l) = ⊥.
By definition, dom(h) = dom+ (h) ∪ dom− (h) and dom+ (h) ∩ dom− (h) = ∅ hold.
     We adopt the concept of a block from [7]. An interval [l, l′ ) for l, l′ ∈ Loc
representing consecutive memory locations, where the lower bound is included,
and the upper bound is excluded. [l, l′ ) is defined as [l, l′ ) = {l′′ ∈ Loc | l ≤
l′′ < l′ }. The set of intervals is defined as Int = {[l, l′) | l, l′ ∈ Loc ∧ l < l′ }.
     A block set B is a finite collection of non-overlapping blocks, and the set of
block sets is defined as follows.

        Blocks = {B ⊆fin Int | ∀[l1 , l′ 1 ), [l2 , l′ 2 ) ∈ B.
                             [l1 , l′ 1 ) 6= [l2 , l′ 2 ) → [l1 , l′ 1 ) ∩ [l2 , l′ 2 ) = ∅}

For B ∈ Blocks, B means [l,l′ )∈B [l, l′ ).
                 S          S
   We define the functions bB and eB : Loc → Val, parameterized by B ∈
Blocks, which return the base and end addresses, respectively, of the block to
2
    The concept of using ⊥ to signify deallocated locations was introduced by Raad et
    al. [11], specifically for negative heaps, expressed as x 67→. It is important to note
    that ⊥ does not denote “undefined”, as in other literature.
         Incorrectness Separation Logic with Arrays and Pointer Arithmetic       7

which a given location belongs. Specifically, for l ∈ Loc, we define bB (l) = u and
eB (l) = v if l ∈ [u, v) ∈ B. If no such interval exists, then we define bB (l) = 0
and eB (l) = 0.



Definition 4 (Conditions on the models and exact models). We assume
the following conditions for the states (s, h, B).


                 S
 1. dom+ (h) ⊆   B
                S
 2. dom− (h) ∩ ( B) = ∅

                                                 S
   Furthermore, if (s, h, B) satisfies dom+ (h) = B, we call (s, h, B) exact. We
use State+ to denote the set of the exact states.



The first condition is slightly modified from the corresponding one in [7]. In [7],
it is sufficient to state that “h(l) is defined”, but in ISL, due to the presence
of negative heaps, we must distinguish between the cases where h(l) ∈ Val or
h(l) = ⊥.
   The second condition, similar to the first one, considers the case where h(l) =
⊥. This condition indicates that deallocated locations are not within a block;
that is, locations within blocks must not be deallocated.
   The denotational semantics of programs is defined for exact states.
   We define the term interpretation [[t]]s,B in the following.



Definition 5 (Term interpretation).


                 [[t + t′ ]]s,B = [[t]]s,B + [[t′ ]]s,B
                    [[b(t)]]s,B = bB ([[t]]s,B )
                  [[e(t)]]s,B = eB ([[t]]s,B )
                      [[n]]s,B = n,      [[x]]s,B = s(x),   [[null]]s,B = 0


Note that if t does not contain b or e, [[t]]s,B does not depend on B.



   The semantics of the assertions of ISL is defined as follows.
8      Y. Lee and K. Nakazawa

Definition 6 (Assertion semantics of ISL). We define the relation (s, h, B) |=
P as
                     ∃−
                      →
                      x .ψ ⇔ ∃i ∈ I.(s, h, B) |= ∃−
                                                  →
                   _
      (s, h, B) |=             i   i              x .ψ ,       i   i
                         i∈I
           (s, h, B) |= ∃−
                         →
                         xi .ψi ⇔ ∃−
                                   →
                                   vi ∈ Val.(s[− →
                                                 xi 7→ −
                                                       →vi ], h, B) |= ψi ,
          (s, h, B) |= ψ1 ∗ ψ2 ⇔ ∃h1 , h2 . h = h1 ◦ h2 and
                                  (s, h1 , B) |= ψ1 and (s, h2 , B) |= ψ2 ,
                (s, h, B) |= emp ⇔ dom(h) = ∅,
           (s, h, B) |= t 7→ u ⇔ dom(h) = {[[t]]s,B } & h([[t]]s,B ) = [[u]]s,B ,
         (s, h, B) |= arr(t, t′ ) ⇔ [[t]]s,B < [[t′ ]]s,B &
                                       dom(h) = dom+ (h) = {[[[t]]s,B [[t′ ]]s,B )},
         (s, h, B) |= arr(t, t′ ) ⇔ [[t]]s,B < [[t′ ]]s,B &
                                        dom(h) = dom− (h) = {[[[t]]s,B [[t′ ]]s,B )},
               (s, h, B) |= t ≈ t′ ⇔ [[t]]s,B = [[t′ ]]s,B & dom(h) = ∅,
               (s, h, B) |= t 6≈ t′ ⇔ [[t]]s,B 6= [[t′ ]]s,B & dom(h) = ∅,
               (s, h, B) |= t ≤ t′ ⇔ [[t]]s,B ≤ [[t′ ]]s,B & dom(h) = ∅,
           (s, h, B) |= t < t′ ⇔ [[t]]s,B < [[t′ ]]s,B & dom(h) = ∅,
 where s[−
         →
         x 7→ −
           i
                →v ] means s[x 7→ v ] . . . [x 7→ v ]. For a pure formula ψ,
                     i                 i1    i1       in      in
(s, B) |= ψ means that (s, ∅, B) |= ψ for the empty heap ∅. Additionally, we define
entailments between formulas. The notation ψ |= ϕ means that if (s, h, B) |= ψ,
then (s, h, B) |= ϕ. We write ψ ≡ ϕ to indicate that both ψ |= ϕ and ϕ |= ψ
hold.

2.2   Program Language
We recall the program language for ISL in [11].
Definition 7 (Program Language C ∈ Comm).
                  C ::= skip | x := t | x := *
                        | assume(π) | local x := t in C
                           | C1 ; C2 | C1 + C2 | C⋆ | error()
                           | x := alloc(t) | free(t) | x := [t] | [t] := t′
In this definition, π is a pure formula, and t does not contain b or e.
    We largely follow the command language traditions of Separation Logic (SL)
[12]. The programming language includes standard constructs such as skip, as-
signment x := t, and nondeterministic assignment x := * (where * represents
a nondeterministically selected value). It also features assume(π), local vari-
able declarations local x in C, sequential composition C1 ; C2 , nondeterminis-
tic choice C1 + C2 , and loops C⋆ . Additionally, it supports error() statements
and various instructions for heap manipulation.
         Incorrectness Separation Logic with Arrays and Pointer Arithmetic      9

   Heap manipulation instructions include operations such as allocation, deal-
location, lookup, and mutation, described as follows:
 – x := alloc(t): Allocates t memory cells (from x to x + t − 1) on the heap,
   assigning the starting location to x. It may reuse previously deallocated
   locations.
 – free(t): Deallocates the memory location referred to by t.
 – x := [t]: Reads the value stored at the heap location t and assigns it to x.
 – [t] := t′ : Updates the heap location t with the value of t′ .
Definition 8 (termC(C)). We define the set termC(C) of terms for a program
C.

                       termC(skip) = termC(error()) = ∅
                      termC(x := t) = {x} ∪ term(t)
                     termC(x := *) = {x}
               termC(assume(ψ)) = termS(ψ)
        termC(local x := t in C) = (termC(C) \ {x}) ∪ term(t)
             termC(x := alloc(t)) = {x} ∪ term(t)
                  termC(free(t)) = term(t) ∪ term(b(t)) ∪ term(e(t))
                    termC(x := [t]) = {x} ∪ term(b(t))
                    termC([t] := t′ ) = term(t + 1) ∪ term(b(t)) ∪ term(t′ )
                     termC(C1 ; C2 ) = termC(C1 + C2 ) =
                                        termC(C1 ) ∪ termC(C2 )
                         termC(C⋆ ) = termC(C)

This function encompasses both the terms appearing in C and the variables or
heap locations referenced by C. It is used to generate the weakest postconditions.
Definition 9 (The set of terms modified by C, mod(C)).

                    mod(skip) = mod(assume(ψ)) = mod(error())
                              = mod(free(t)) = mod([t] := t′ ) = ∅
                  mod(x := t) = mod(x := *) = mod(x := alloc(t))
                              = mod(x := [t]) = {x}
         mod(local x in C) = mod(C) \ {x}
                mod(C1 ; C2 ) = mod(C1 + C2 ) = mod(C1 ) ∪ mod(C2 )
                      mod(C⋆ ) = mod(C)

Definition 10 (Denotational semantics of ISL). We define [[C]]ǫ for a pro-
gram C and an exit condition ǫ ∈ {ok, er} as a binary relation on State+ . We
use the composition of binary relations: for binary relations R1 and R2 , R1 ; R2
is the relation {(a, c) | ∃b.(a, b) ∈ R1 and (b, c) ∈ R2 }. Here, C0 = skip and
Cm+1 = C; Cm .
10         Y. Lee and K. Nakazawa



                [[skip]]ok = {(σ, σ) | σ ∈ State+ }
                [[skip]]er = ∅
              [[x := t]]ok = {((s, h, B), (s[x 7→ [[t]]s,B ], h, B))}
              [[x := t]]er = ∅
              [[x := *]]ok = {((s, h, B), (s[x 7→ v], h, B)) | v ∈ Val}
              [[x := *]]er = ∅
         [[assume(ψ)]]ok = {((s, h, B), (s, h, B)) | (s, B) |= ψ}
         [[assume(ψ)]]er = ∅
            [[error()]]ok = ∅
             [[error()]]er = {(σ, σ) | σ ∈ State+ }
              [[C1 ; C2 ]]ok = [[C1 ]]ok ; [[C2 ]]ok
              [[C1 ; C2 ]]er = [[C1 ]]er ∪ [[C1 ]]ok ; [[C2 ]]er
       [[local x in C]]ǫ = {((s, h, B), (s′ , h′ , B ′ )) | ∃v, v ′ ∈ Val.
                                ((s[x 7→ v], h, B), (s′ [x 7→ v ′ ], h′ , B ′ )) ∈ [[C]]ǫ & s(x) = s′ (x)}
             [[C1 + C2 ]]ǫ = [[C1 ]]ǫ ∪ [[C2 ]]ǫ
                   [[C⋆ ]]ǫ =       [[Cm ]]ǫ
                               [

                                m∈N
                                                                             l+[[t]]      −1
      [[x := alloc(t)]]ok = {((s, h, B), (s[x 7→ l], h[i 7→ vi ]i=l s,B , B ∪ {[l, l + [[t]]s,B )})) |
                                      [
                         l ∈ Loc & ( B) ∩ [l, l + [[t]]s,B ) = ∅ & vi ∈ Val for i ∈ [0, [[t]]s,B )}
      [[x := alloc(t)]]er = ∅
                                                       B           e   ([[t]]s,B )−1
            [[free(t)]]ok = {((s, h, B), (s, h[i 7→ ⊥]i=b                              , B \ {[bB ([[t]]s,B ), eB ([[t]]s,B ))})) |
                                                                       B ([[t]]s,B )

                            [[t]]s,B = bB ([[t]]s,B ) & bB ([[t]]s,B ) > 0}
             [[free(t)]]er = {((s, h, B), (s, h, B)) | [[t]]s,B 6= bB ([[t]]s,B ) or bB ([[t]]s,B ) = 0}
             [[x := [t]]]ok = {((s, h, B), (s[x 7→ h([[t]]s,B )], h, B)) | bB ([[t]]s,B ) > 0}
             [[x := [t]]]er = {((s, h, B), (s, h, B)) | bB ([[t]]s,B ) = 0}
            [[[t] := t′ ]]ok = {((s, h, B), (s, h[[[t]]s,B 7→ [[t′ ]]s,B ], B)) | bB ([[t]]s,B ) > 0}
                      ′
            [[[t] := t ]]er = {((s, h, B), (s, h, B)) | bB ([[t]]s,B ) = 0}


     Based on the previous definitions, the validity of ISL triples of the form
[P ] C [ǫ : Q] is defined as follows.

Definition 11 (Validity of ISL Triples).
                                                   def
                     |= [P ] C [ǫ : Q] ⇐⇒ ∀σ ′ |= Q, ∃σ |= P.(σ, σ ′ ) ∈ [[C]]ǫ


2.3      Canonicalization

We need to define canonical forms for the inference rules of certain heap-manipulating
proof rules. Before defining our canonical forms, we introduce two functions
perm(T ) and cases(T ). Let perm(T ) denote the set of all permutations of a finite
set T = {t1 , t2 , . . . , tn } of terms as follows.
                              
          perm(T ) = (tρ(1) , tρ(2) , . . . , tρ(n) ) |
                                      ρ : {1, 2, . . . , n} → {1, 2, . . . , n} is a bijection
          Incorrectness Separation Logic with Arrays and Pointer Arithmetic          11

   For a finite set T of terms, the case analysis function cases(T ) generates
a pure formulas representing every possible sequence of strict inequalities and
equalities between the elements of T for each permutation.
                          [         
        cases(T ) =                   null R0 t1 R1 t2 . . . tn−1 Rn−1 tn |
                      (t1 ,t2 ,...,tn )∈perm(T )

                                                     Ri ∈ {<, ≈} for 0 ≤ i ≤ n − 1

  The following lemma holds by the definition of cases(T ).
               W
Lemma 1. ψ ≡ π∈cases(T ) (π ∗ ψ) holds for any ψ and T .

   The canonical forms of quantifier-free symbolic heaps concerning a set T of
terms are defined as follows.

Definition 12 (Canonical forms).

                  CFsh (T ) = {ψ | ψpure |= π for some π ∈ cases(T )}

If ψ ∈ CFsh (T ) for a finite set of terms T , then ψ is called canonical for T .

   The canonicalization divides into the cases for each possible sequence of strict
inequalities and equalities individually to the input symbolic heap.

Definition 13 (Canonicalization cano). The set casessh (ψ, C) of cases for
canonicalization is defined as

              casessh (ψ, C) = {π ∗ ψ | π ∈ cases(termS(ψ) ∪ termC(C))}.
          W       →
                  −             →
                                −
For P =     i∈I ∃ xi .ψi and xi ∈
                                / termC(C).

                                                                        ∃−
                                                                         →
                                                   _        _
                            cano(P, C) =                                 xi .ϕ
                                                   i∈I ϕ∈cases(ψi ,C)


Lemma 2. P ≡ cano(P, C) and ψi ∈ CFshW(termS(ψi ) ∪ termC(C)) for any i ∈ I
hold for any P and C, with cano(P, C) = i∈I ∃−
                                             →
                                             xi .ψi .


2.4   Proof Rules

In this section, we give the inference rules of our system.
    For rules regarding memory deallocation, we propose the notation Arr(t, t′ )α
serves as a unifying representation for t 7→ α and arr(t, t′ ), simplifying the rules
for heap manipulation proofs. In this notation, α represents either a term or the
symbol •, which is explicitly not a term. Define:

 – Arr(t, t + 1)u denotes t 7→ u, and
 – Arr(t, t′ )• denotes arr(t, t′ ).
12      Y. Lee and K. Nakazawa

    Furthermore, for a simpler notation, we use the following convention. Con-
sider a symbolic heap ψ and a set of terms T = {t1 , t2 , . . . , tn }, where no two
terms in T are in the subterm relation. The replacement of all elements in T
with a term u is denoted as ψ[T := u]. We further define the following sets:

             Tb (ψ, t) = {b(t′ ) ∈ termS(ψ) | ψpure |= b(t′ ) ≈ b(t)}, and
             Te (ψ, t) = {e(t′ ) ∈ termS(ψ) | ψpure |= e(t′ ) ≈ e(t)}.

Definition 14 (ISL Proof Rules). We define our ISL proof rules in Figures
1, 2, 3, and 4, where the axioms of the form [P ] C [ok : Q1 ][er : Q2 ] means that
both [P ] C [ok : Q1 ] and [P ] C [er : Q2 ].

     Note that we employ infinitary syntax and incorporate an infinitary version
of the Disj rule following a similar approach used in RHL [5].
     The heap manipulation rules require symbolic heaps to be in canonical form
as a premise. We provide an intuitive explanation of the rules for memory allo-
cation in Figure 2 and deallocation rules in Figure 3.
     The rules for allocation depend on the relationship between the locations
to be allocated and the locations indicated by arr in the precondition. As the
block information changes, the values of b(t′ ) and e(t′ ) for t′ , which are in the
newly allocated block locations, also change. Therefore, the values of b(t′ ) and
e(t′ ) are replaced with 0 (using a function repβα ), since before allocation, t′ is not
allocated.
     The rules for deallocation perform a case analysis on the range of the freed
locations and the locations of 7→ and arr in the precondition. Since block infor-
mation changes, the values of b(t′ ) and e(t′ ) for t′ in the deallocated block also
change. Therefore, such terms in the precondition are replaced with the values
before the deallocation operation (using a replacement τ ).
     Regarding the Frame rule, we consider only the ok case. This is because, if
we include the er case in the Frame rule, we find that soundness is broken in
our setting. The following is an example.

                 [x 6≈ null ∗ emp] free(x) [er : x 6≈ null ∗ emp]
        [x 6≈ null ∗ emp ∗ x 7→ 1] free(x) [er : x 6≈ null ∗ emp ∗ x 7→ 1]

If we use x 7→ 1 as a frame, the conclusion triple becomes invalid, while the
premise triple remains valid, indicating that soundness does not hold in this
case.


3    Weakest Postcondition

In this section, we describe the definition of the weakest postcondition WPO[[P, C, ǫ]]
and introduce a function wpo(P, C, ǫ) that computes weakest postconditions. We
begin by formally defining the weakest postcondition as follows.
          Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                        13




   Skip                                       Error                                        Seq1
                                                                                             [P ] C1 [er : Q]
   [P ] skip [ok : P ] [er : false]           [P ] error() [ok : false] [er : P ]          [P ] C1 ; C2 [er : Q]

Seq2                                           Loop zero (equal to Skip)                    Loop⋆ non-zero
 [P ] C1 [ok : R]   [R] C2 [ǫ : Q]                                                           [P ] C ; C [ǫ : Q]
        [P ] C1 ; C2 [ǫ : Q]                   [P ] C⋆ [ok : P ] [er : false]                    [P ] C⋆ [ǫ : Q]

            Cons
             ′              ′             ′            ′
                                                                      Disj
             P |= P      [P ] C [ǫ : Q ]      Q |= Q                  [Pi ] C [ǫ : Qi ] for all i ∈ I
                                                                             _             _
                          [P ] C [ǫ : Q]                                   [   Pi ] C [ǫ :   Qi ]
                                                                           i∈I             i∈I


               Choice                                               Exist
                [P ] C1 [ǫ : Q]   [P ] C2 [ǫ : Q]                    [ψ] C [ǫ : ϕ]     x∈
                                                                                        / termS(C)
                      [P ] C1 + C2 [ǫ : Q]                                [∃x.ψ] C [ǫ : ∃x.ϕ]

      Assign                                                          Havoc

      [ψ] x := t [ok : ∃x′ .ψθ ∗ x ≈ tθ] [er : false]                 [ψ] x := * [ok : ∃x′ .ψθ] [er : false]


            Assume (π is a pure formula)                               Local
                                                                       [ψ] C [ǫ : ϕ]    x∈
                                                                                         / termS(ψ)
                                                                       [ψ] local x in C [ǫ : ∃x.ϕ]
            [ψ] assume(π) [ok : π ∗ ψ] [er : false]

                                  Frame Ok
                                      [ψ] C [ok : ϕ]   mod(C) ∩ termS(φ) = ∅
                                               [ψ ∗ φ] C [ok : ϕ ∗ φ]

Here, θ denotes [x := x′ ].

                                         Fig. 1. Proof Rules of ISL
14           Y. Lee and K. Nakazawa


                    Alloc 1
                              ψ ∈ CFsh (termS(ψ) ∪ termC(x := alloc(t)))
                    0≤α≤β≤N         ψpure |= null R1 u1 R2 · · · RN uN (Ri ∈ {<, ≈})
                                                                               
                       [ψ] x := alloc(t) [ok : ∃x′ .repβ
                                                       α ψθ ∗ arr(x, x + tθ) ∗ ϕ ]



      Alloc 2
                                            ψ ∈ CFsh (termS(ψ) ∪ termC(x := alloc(t)))
              m                                                                                                 m−1
      ψ = ∗ arr(ti , t′i ) ∗ ψ ′ (ψ ′ contains no arr)                0≤α≤β≤N                    ψpure |=         ∗ ti < ti+1
              i=1                                                                                               i=1
                    1≤j≤k≤m                       ψpure |= null R1 u1 R2 · · · RN uN (Ri ∈ {<, ≈})
                                                                                  
                                                [ψ] x := alloc(t) [ok : ∃x′ .repβ   ′
                                                                                α ψ θ
               j−1                ′                                                       ′          m                ′
              ∗ ∗ arr(ti θ, ti θ) ∗ arr(tj θ, x) ∗ arr(x, x + tθ) ∗ arr(x + tθ, tk θ) ∗ ∗  arr(ti θ, ti θ)
                i=1                                                                 i=k+1
                                                    ′                      ′
                                    ∗tj θ < x < tj θ ∗ tk θ < x + tθ < tk θ ∗ ϕ ]


 Alloc 3
                                      ψ ∈ CFsh (termS(ψ) ∪ termC(x := alloc(t)))
         m                                                                                               m−1
 ψ = ∗ arr(ti , t′i ) ∗ ψ ′ (ψ ′ contains no arr)                  0≤α≤β≤N                    ψpure |=    ∗ ti < ti+1
        i=1                                                                                               i=1
               1≤j≤k≤m                        ψpure |= null R1 u1 R2 · · · RN uN (Ri ∈ {<, ≈})
                                                                              
                                            [ψ] x := alloc(t) [ok : ∃x′ .repβ   ′
                                                                            α ψ θ
                    j−1                 ′                                    ′         m                 ′
                  ∗ ∗ arr(ti θ, ti θ) ∗ arr(x, x + tθ) ∗ arr(x + tθ, tk θ) ∗          ∗       arr(ti θ, ti θ)
                    i=1                                                            i=k+1
                                                                                      
                                      ∗t′j−1 θ ≤ x ≤ tj θ ∗ tk θ < x + tθ < t′k θ ∗ ϕ ]


      Alloc 4
                                            ψ ∈ CFsh (termS(ψ) ∪ termC(x := alloc(t)))
              m                                                                                                 m−1
      ψ = ∗ arr(ti , t′i ) ∗ ψ ′ (ψ ′ contains no arr)                0≤α≤β≤N                    ψpure |=         ∗ ti < ti+1
              i=1                                                                                               i=1
                    1≤j≤k≤m                       ψpure |= null R1 u1 R2 · · · RN uN (Ri ∈ {<, ≈})
                                                                                  
                                                [ψ] x := alloc(t) [ok : ∃x′ .repβ   ′
                                                                                α ψ θ
                           j−1                                                         m
                          ∗ ∗ arr(ti θ, t′i θ) ∗ arr(tj θ, x) ∗ arr(x, x + tθ) ∗       ∗       arr(ti θ, t′i θ)
                            i=1                                                       i=k+1

                                            ∗tj θ < x < t′j θ ∗ t′k θ ≤ x + tθ ≤ tk+1 θ ∗ ϕ ]


     Alloc 5
                                            ψ ∈ CFsh (termS(ψ) ∪ termC(x := alloc(t)))
              m                                                                                                 m−1
      ψ = ∗ arr(ti , t′i ) ∗ ψ ′ (ψ ′ contains no arr)                0≤α≤β≤N                    ψpure |=         ∗ ti < ti+1
              i=1                                                                                               i=1
                    1≤j≤k≤m            ψpure |= null R1 u1 R2 · · · RN uN (Ri ∈ {<, ≈})
                                       
                                                   j−1                                     m
     [ψ] x := alloc(t) [ok : ∃x′ .repβ    ′
                                      α ψ θ       ∗ ∗ arr(ti θ, t′i θ) ∗ arr(x, x + tθ) ∗ ∗    arr(ti θ, t′i θ)
                                                    i=1                                 i=k+1

                             ∗t′j−1 θ ≤ x ≤ tj θ ∗ t′k θ ≤ x + tθ ≤ tk+1 θ ∗ ϕ ]


                                                     AllocEr
                                                     [ψ] x := alloc(t) [er : false]

Here, θ denotes [x := x′ ] and ϕ denotes the formula b(x) ≈ x∗e(x) ≈ x+tθ∗uα θ <
x ≤ uα+1 θ ∗ uβ θ < x + tθ ≤ uβ+1 θ. Suppose {ui | 1 ≤ i ≤ N } = termS− (ψ).
repβα (χ) is the formula obtained from χ by replacing b(ui θ) and e(ui θ) with null
for α < i ≤ β where termS− (ψ) = {ui | 1 ≤ i ≤ N }.

                                             Fig. 2. Rules for Memory Allocation
        Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                               15




  FreeArr 1
                                                                           k−1
  ψ ∈ CFsh (termS(ψ) ∪ termC(free(t)))              ψ = arr(t1 , t′ 1 ) ∗ ∗ Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′
                                                                          i=2
                                                                         k−1                   k−1
      ψpure |= t1 < b(t) < t′ 1 ∗ tk < e(t) < t′ k ∗ b(t) ≈ t ∗ ∗ t′ i ≈ ti+1 ∗ ∗ ti < ti+1
                                                                   i=1                    i=1
             [ψ] free(t) [ok : ∃y.(arr(t1 , t) ∗ arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ ] [er : false]

       FreeArr 2
                                                                 k−1
        ψ ∈ CFsh (termS(ψ) ∪ termC(free(t)))               ψ = ∗ Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′
                                                                  i=1
                                                ′                   k−1 ′                    k−1
         ψpure |= t1 ≈ b(t) ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗ t i ≈ ti+1 ∗ ∗ ti < ti+1
                                                                     i=1                     i=1
                   [ψ] free(t) [ok : ∃y.(arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ ] [er : false]

           FreeArr 3
                                                                            k            ′           ′
              ψ ∈ CFsh (termS(ψ) ∪ termC(free(t)))                  ψ = ∗ Arr(ti , t i )αi ∗ ψ
                                                                            i=1
                                                                 k−1 ′                  k−1
            ψpure |= t1 ≈ b(t) ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗ t i ≈ ti+1 ∗ ∗ ti < ti+1
                                                                  i=1                   i=1
                                                                    ′
                          [ψ] free(t) [ok : ∃y.(arr(t, y) ∗ ψ )τ ] [er : false]

        FreeArr 4
                                                                                   k
        ψ ∈ CFsh (termS(ψ) ∪ termC(free(t)))                ψ = arr(t1 , t′ 1 ) ∗ ∗ Arr(ti , t′ i )αi ∗ ψ ′
                                                                                  i=2
                                                                     k−1                     k−1
         ψpure |= t1 < b(t) < t′ 1 ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗ t′ i ≈ ti+1 ∗ ∗ ti < ti+1
                                                                      i=1                    i=1
                    [ψ] free(t) [ok : ∃y.(arr(t1 , t) ∗ arr(t, y) ∗ ψ ′ )τ ] [er : false]

             FreeEr
              ψ ∈ CFsh (termS(ψ) ∪ {x, b(t), e(t)}) ψpure |= b(t) 6≈ t ∨ b(t) ≈ null
                                     [ψ] free(t) [ok : false] [er : ψ]

Here, τ denotes the replacement [Tb (ψ, t) := t][Te (ψ, t) := y].

                           Fig. 3. Rules for Memory Deallocation
16         Y. Lee and K. Nakazawa




            LoadPtr                                                                                                 ′
             ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))                 ψpure |= ta ≈ t               ψ = ta 7→ u ∗ ψ
                                                         ′
                               [ψ] x := [t] [ok : ∃x .ψθ ∗ x ≈ uθ] [er : false]

        LoadArr
        ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))            ψpure |= ta ≤ t < t′ a                   ψ = arr(ta , t′ a ) ∗ ψ ′
                                                                   ′
                                     [ψ] x := [t] [ok : ∃x .ψθ] [er : false]

                    LoadEr
                     ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))                         ψpure |= b(t) ≈ null
                                        [ψ] x := [t] [ok : false] [er : ψ]

            StorePtr                                 ′                                                              ′
            ψ ∈ CFsh (termS(ψ) ∪ termC([t] := t ))                 ψpure |= ta ≈ t               ψ = ta 7→ − ∗ ψ
                                               ′                       ′   ′
                                   [ψ] [t] := t [ok : t 7→ t ∗ ψ ] [er : false]

           StoreArr 1
           ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))               ψpure |= ta ≈ t               ψ = arr(ta , t′ a ) ∗ ψ ′
                         [ψ] [t] := t′ [ok : t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′ ] [er : false]

     StoreArr 2
     ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))          ψpure |= ta < t ∗ t + 1 < t′ a                    ψ = arr(ta , t′ a ) ∗ ψ ′
                               ′                               ′                         ′   ′
                   [ψ] [t] := t [ok : arr(ta , t) ∗ t 7→ t ∗ arr(t + 1, t a ) ∗ ψ ] [er : false]

        StoreArr 3
         ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))               ψpure |= t + 1 ≈ t′ a               ψ = arr(ta , t′ a ) ∗ ψ ′
                                         ′                                     ′     ′
                            [ψ] [t] := t [ok : arr(ta , t) ∗ t 7→ t ∗ ψ ] [er : false]

                    StoreEr
                     ψ ∈ CFsh (termS(ψ) ∪ termC(x := [t]))                         ψpure |= b(t) ≈ null
                                        [ψ] [t] := t′ [ok : false] [er : ψ]

Here, θ denotes [x := x′ ].

                      Fig. 4. Rules for the other Memory Manipulation
        Incorrectness Separation Logic with Arrays and Pointer Arithmetic     17

Definition 15 (Weakest Postcondition).
   The weakest postcondition of a precondition P , a program C, and an exit
condition ǫ is defined as follows.

          WPO[[P, C, ǫ]] = {σ ′ ∈ State+ | ∃σ.σ |= P ∧ (σ, σ ′ ) ∈ [[C]]ǫ }

3.1   Weakest Postcondition Generating Function wpo
We define the weakest postcondition generating function wpo as follows.

Definition 16 (wpo). We simultaneously define wpo and wposh as follows.
 – For an assertion P such that cano(P, C) = i∈I ∃−
                                                  →
                                            W
                                                  xi .ψi , define

                                               ∃−
                                                →
                                         _
                        wpo(P, C, ǫ) =          xi .wposh (ψi , C, ǫ).
                                         i∈I

 – For ψ ∈ CFsh (termS(ψ) ∪ termC(C)), wposh (ψ, C, ǫ) is defined in Figures 5
   and 6.

Note that infinite disjunctions are required only when calculating wpo for C⋆ ,
following the setting of [9]. Additionally, the cases for commands that do not
manipulate heaps and blocks are the same as those in [9].
18    Y. Lee and K. Nakazawa




                                     (
                                         ψ       ǫ = ok
              wposh (ψ, skip, ǫ) =
                                         false   ǫ = er
                                     (
                                   false ok
             wposh (ψ, error, ǫ) =
                                   ψ      er
                                        ′′ −
                                           →.ϕ
                                  _
     wposh (ψ, local x in C, ǫ) =     ∃x , x j j
                                     j∈J

                                                                            ∃−
                                                                             →.ϕ
                                                                                  
                                             ′               ′′  ′
                                                                          _
                                 wpo(ψ[x := x ], C, ǫ)[x := x ][x := x] =    x j j
                                                                           j∈J
                                     (
                                         ψ∗B      ǫ = ok
        wposh (ψ, assume(B), ǫ) =
                                         false    ǫ = er
          wposh (ψ, C1 ; C2 , ok) = wpo(wposh (ψ, C1 , ok), C2 , ok)
           wposh (ψ, C1 ; C2 , er) = wposh (ψ, C1 , er) ∨ wpo(wposh (ψ, C1 , ok), C2 , er)
              wposh (ψ, C⋆ , ok) =
                                     _
                                        Υ (n) (Υ (0) = ψ and Υ (n + 1) = wpo(Υ (n), C, ok))
                                     n∈N

              wposh (ψ, C⋆ , er) =
                                     _
                                           wpo(Υ (n), C, er)
                                     n∈N

          wposh (ψ, C1 + C2 , ǫ) = wposh (ψ, C1 , ǫ) ∨ wposh (ψ, C2 , ǫ)
                                   (
                                     ∃x′ .ψθ ∗ x ≈ tθ ǫ = ok
            wposh (ψ, x := t, ǫ) =
                                     false               ǫ = er
                                   (
                                     ∃x′ .ψθ ǫ = ok
           wposh (ψ, x := *, ǫ) =
                                     false     ǫ = er



             Fig. 5. wposh for commands that do not manipulate heaps
                                                                                          Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                           19




 wposh (ψ, x := alloc(t), ok) =
                     
 ∃x′ .          repβ
         _
                   α (ψθ ∗ arr(x, x + tθ) ∗ ϕ)∨
      0≤α≤β≤N
               
                  ′   j−1           ′                                                   ′                m              ′                     ′                         ′
                (ψ θ ∗ ∗ arr(ti θ, ti θ) ∗ arr(tj θ, x) ∗ arr(x, x + tθ) ∗ arr(x + tθ, tk θ) ∗          ∗
     _
                                                                                                              arr(ti θ, ti θ) ∗ tj θ < x < tj θ ∗ tk θ < x + tθ < tk θ ∗ ϕ)∨
                        i=1                                                                           i=k+1
  1≤j≤k≤m

                     j−1                                                              m
            (ψ ′ θ ∗ ∗ arr(ti θ, t′i θ) ∗ arr(x, x + tθ) ∗ arr(x + tθ, t′k θ) ∗       ∗    arr(ti θ, t′i θ) ∗ t′j−1 θ ≤ x ≤ tj θ ∗ tk θ < x + tθ < t′k θ ∗ ϕ)∨
                     i=1                                                           i=k+1

                     j−1                                                       m
            (ψ ′ θ ∗ ∗ arr(ti θ, t′i θ) ∗ arr(tj θ, x) ∗ arr(x, x + tθ) ∗      ∗      arr(ti θ, t′i θ) ∗ tj θ < x < t′j θ ∗ t′k θ ≤ x + tθ ≤ tk+1 θ ∗ ϕ)∨
                     i=1                                                     i=k+1
                                                                                                                                                  
                     j−1                                        m
            (ψ ′ θ ∗ ∗ arr(ti θ, t′i θ) ∗ arr(x, x + tθ) ∗     ∗      arr(ti θ, t′i θ) ∗ t′j−1 θ ≤ x ≤ tj θ ∗ t′k θ ≤ x + tθ ≤ tk+1 θ ∗ ϕ)
                     i=1                                      i=k+1

           m                                                                   m−1
 // ψ = ∗ arr(ti , t′ i ) ∗ ψ ′ with ψ ′ containing no arr, ψpure |=            ∗ ti < ti+1 , and ψpure |= nullR1 u1 R2 · · · RN uN for termS− (ψ) = {u1 , . . . , uN }.
          i=1                                                                   i=1

 // ϕ = b(x) ≈ x ∗ e(x) ≈ x + tθ ∗ uα θ < x ≤ uα+1 θ ∗ uβ θ < x + tθ ≤ uβ+1 θ
 wposh (ψ, x := alloc(t), er) = false
 wposh (ψ, free(t), ok) =
   ∃y.(arr(t1 , t) ∗ arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ if ψ = arr(t1 , t′ 1 ) ∗ ∗k−1                             ′                   ′     ′
 
                                                                                              i=2 Arr(ti , t i )αi ∗ arr(tk , t k ) ∗ ψ
                                                                   & ψpure |= t1 < b(t) < t 1 ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗i=1                       t i ≈ ti+1 ∗ ∗i=1
                                                                                                                                                   k−1 ′              k−1
                                                                                                          ′                         ′
                                                                                                                                                                           ti < ti+1 for some k and ψ ′
 
 
 
 
                              ′            ′
                                                                       ∗ k−1                  ′                        ′          ′
 
   ∃y.(arr(t,  y)  ∗ arr(y,  t    )  ∗  ψ    )τ                if ψ =          Arr(t      , t     )     ∗ arr(t    , t     ) ∗ ψ
 
                                k                                                       i       i   α           k        k
 
 
                                                                        i=1                          i
                                                                   & ψpure |= t1 ≈ b(t) ∗ tk < e(t) < t′ k ∗ b(t) ≈ t ∗ ∗i=1                     t i ≈ ti+1 ∗ ∗i=1
                                                                                                                                             k−1 ′               k−1
                                                                                                                                                                     ti < ti+1 for some k and ψ ′
 
 
 
 
   ∃y.(arr(t, y) ∗ ψ )τ′
                                                               if ψ = ∗i=1 Arr(ti , t i )αi ∗ ψ ′
                                                                         k                  ′

                                                                   & ψpure |= t1 ≈ b(t) ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1                    t i ≈ ti+1 ∗ ∗i=1
                                                                                                                                        k−1 ′              k−1
                                                                                                                                                                ti < ti+1 for some k and ψ ′
 
 
 
 
                                                                                            ∗i=2
                                       ′                                        ′             k                 ′              ′
   ∃y.(arr(t   , t) ∗ arr(t, y)   ∗   ψ   )τ                   if ψ =  arr(t  , t    )  ∗              Arr(t  , t    )      ∗ ψ
 
             1                                                              1      1
 
                                                                                                           i      i αi
 
                                                                   & ψpure |= t1 < b(t) < t′ 1 ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1                k−1 ′
                                                                                                                                                   t i ≈ ti+1 ∗ ∗i=1
                                                                                                                                                                  k−1
                                                                                                                                                                      ti < ti+1 for some k and ψ ′
 
 
 
 
 
   false                                                       otherwise
 
                                (
                                   ψ           if ψpure |= b(t) 6≈ t ∨ b(t) ≈ null
 wposh (ψ, free(t), er) =
                                   false otherwise
                                
                                        ′                                             ′                                                          ′
                                ∃x .ψθ ∗ x ≈ uθ if ψ = ta 7→ u ∗ ψ & ψpure |= ta ≈ t for some ta , u and ψ
                                
 wposh (ψ, x := [t], ok) = ∃x′ .ψθ                           if ψ = arr(ta , t′ a ) ∗ ψ ′ & ψpure |= ta ≤ t < t′ a for some ta , t′ a and ψ ′
                                
                                false                       otherwise
                                (
                                   ψ           if ψpure |= b(t) ≈ null
 wposh (ψ, x := [t], er) =
                                   false otherwise

                                     t 7→ t′ ∗ ψ ′                                           if ψ = ta 7→ − ∗ ψ ′ & ψpure |= ta ≈ t for some ta and ψ ′
                                 
                                 
                                 
                                              ′               ′       ′
                                 t 7→ t ∗ arr(t + 1, t a ) ∗ ψ                              if ψ = arr(ta , t′ a ) ∗ ψ ′ & ψpure |= ta ≈ t for some ta , t′ a and ψ ′
                                 
                                 
                                 
 wposh (ψ, [t] := t′ , ok) = arr(ta , t) ∗ t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′ if ψ = arr(ta , t′ a ) ∗ ψ ′ & ψpure |= ta < t ∗ t + 1 < t′ a for some ta , t′ a and ψ ′
                                     arr(ta , t) ∗ t 7→ t′ ∗ ψ ′                             if ψ = arr(ta , t′ a ) ∗ ψ ′ & ψpure |= t + 1 ≈ t′ a for some ta , t′ a and ψ ′
                                 
                                 
                                 
                                 
                                 
                                     false                                                   otherwise
                                 
                                (
                                    ψ           if ψpure |= b(t) ≈ null
 wposh (ψ, [t] := t′ , er) =
                                    false otherwise




 Here, θ denotes [x := x′ ]. repβα (χ) is the formula obtained from χ by replacing b(ui θ) and e(ui θ) with null for α < i ≤ β. τ
denotes [Tb (ψ, t) := t][Te (ψ, t) := y].

                                                                Fig. 6. wposh for commands manipulating heaps
20       Y. Lee and K. Nakazawa

4    Soundness and Relative Completeness

In this section, we prove the soundness and relative completeness of ISL.
    For soundness, we use the proof of existing work [11,9] for commands that
do not manipulate heaps. For commands that manipulate heaps, we utilize the
expressiveness of the weakest postconditions (Proposition 1), which states that
the set of exact states satisfying wpo(P, C, ǫ) is exactly WPO[[P, C, ǫ]].
    The relative completeness is proven by the expressiveness and the property
that the triple [P ] C [ǫ : wpo(P, C, ǫ)] is always derivable in our proof system
(Proposition 2).
    To prove expressiveness, we present the following lemmas. Lemmas 3, 4, 5,
and 6 are the same as those used in the expressiveness proof in [9], except that
our versions use models with blocks. Since the results remain consistent with our
current setting, we will directly apply these lemmas to prove the expressiveness
of our system.

Lemma 3 (Substitution with models with blocks).

                 (s, h, B) |= ψ[x := t] ⇐⇒ (s[x 7→ [[t]]s,B ], h, B) |= ψ

   This lemma is a traditional substitution lemma, also used to prove expressive-
ness in [9]. Since substitution does not alter the heap or block, it can naturally
be extended to the expanded models with blocks.

              / termC(C), then the following holds for any (s′ , h′ , B ′ ), ψ, C
Lemma 4. If x ∈
and ǫ.

                      (s′ , h′ , B ′ ) ∈ WPO[[∃x.ψ, C, ǫ]] ⇐⇒
                      ∃v ∈ Val.(s′ [x 7→ v], h′ , B ′ ) ∈ WPO[[ψ, C, ǫ]]

Lemma 5.                        _                    [
                        WPO[[         P, C, ǫ]] ⇐⇒         WPO[[P, C, ǫ]]
                                i∈I                  i∈I


Lemma 6. Suppose cano(P, C) = i∈I ∃−                →
                                                    xi .ψi . If for all i ∈ I, (s′ , h′ , B ′ ) and
                                             W
ǫ, (s , h , B ) |= wposh (ψi , C, ǫ) ⇐⇒ (s , h′ , B ′ ) ∈ WPO[[ψi , C, ǫ]], then for any
       ′   ′  ′                                   ′

(s′ , h′ ) and ǫ, (s′ , h′ , B ′ ) |= wpo(P, C, ǫ) ⇐⇒ (s′ , h′ , B ′ ) ∈ WPO[[P, C, ǫ]] holds.

    These lemmas are extended versions of the lemmas in [9], with the only
difference being that the models in this version include block information B ′ .
However, this difference does not affect the validity of the lemmas.

Proposition 1 (Expressiveness).

             ∀σ ′ ∈ State+ .σ ′ ∈ WPO[[P, C, ǫ]] ⇐⇒ σ ′ |= wpo(P, C, ǫ)
         Incorrectness Separation Logic with Arrays and Pointer Arithmetic        21

Proof. With Lemma 6, to prove this proposition, it is sufficient to show that

                ∀σ ′ .σ ′ ∈ WPO[[ψ, C, ǫ]] ⇐⇒ σ ′ |= wposh (ψ, C, ǫ)

holds for canonical symbolic heaps ψ. For the cases where wposh recursively
generates wpo, we assume as an induction hypothesis that the above holds.
   The cases for atomic commands that do not manipulate heaps share the
same proofs as in [9]. Therefore, we provide proofs only for heap-manipulating
commands in the Appendix.
   By applying expressiveness (Proposition 1), we can demonstrate the sound-
ness of our proof system.
Theorem 1 (Soundness of ISL).
           For any P, C, ǫ, Q, if ⊢ [P ] C [ǫ : Q], then |= [P ] C [ǫ : Q].
Proof. By induction on ⊢ [P ] C [ǫ : Q]. We follow the previous work [9] for
commands that do not manipulate heaps.
    For the cases of heap-manipulating rules, we use the expressiveness (Propo-
sition 1). Assume ⊢ [ψ] C [ǫ : Q] and σ ′ |= Q. By definition of the inference
rules and wposh , it is easy to see Q |= wpo(ψ, C, ǫ). Hence, σ ′ |= wpo(ψ, C, ǫ). By
expressiveness, σ ′ ∈ WPOJψ, C, ǫK holds, which states that there exists σ |= ψ
such that (σ, σ ′ ) ∈ JCKǫ .
    Thus, we conclude |= [P ] C [ǫ : Q].
    Next, we show the following lemma to prove Proposition 2.
Lemma 7. For any P , C, ǫ, let us say cano(P, C) = i∈I ∃−    →
                                                      W
                                                              xi .ψi . Then, the
following holds.

       ∀i ∈ I. ⊢ [ψi ] C [ǫ : wposh (ψi , C, ǫ)] =⇒ ⊢ [P ] C [ǫ : wpo(P, C, ǫ)]

Proof. The lemma proven here is identical to the lemma in [9], and the proof is
also identical since the Exist and Disj rules are the same in both [9] and this
paper.
Proposition 2. For any P, C, ǫ, ⊢ [P ] C [ǫ : wpo(P, C, ǫ)].
Proof. With Lemma 7, it is sufficient to show that for any ψ, C, ǫ, we have
⊢ [ψ] C [ǫ : wposh (ψ, C, ǫ)]. This statement is proven by induction on C and
follows the same proof for rules that do not manipulate heaps in this paper and
[9]. For rules that manipulate heaps, we can directly prove this lemma from the
definition of wposh using the Disj rule.
   By Proposition 1 and Proposition 2, we prove the relative completeness of
ISL.
Theorem 2 (Relative Completeness).

           For any P, C, ǫ, Q, if |= [P ] C [ǫ : Q], then ⊢ [P ] C [ǫ : Q].
22      Y. Lee and K. Nakazawa

Proof. The proof of this theorem is identical to that in [9], as shown below.

       Applying Proposition 2         |= [P ] C [ǫ : Q]
                                                        Proposition 1
       ⊢ [P ] C [ǫ : wpo(P, C, ǫ)] Q |= wpo(P, C, ǫ)
                                                                      Cons
                               ⊢ [P ] C [ǫ : Q]


5     Related Work

5.1   Separation Logic with array predicates

Separation logic with array predicates has been extensively studied in the context
of decidability in entailments and biabduction for symbolic heaps with arrays,
with notable commonalities in the works of [1,8], and [7]. The approaches in
[1,8] share a foundational reliance on a variable-length representation for arrays,
using the arr(x, y) style, and incorporate arithmetic. Despite differences in the
specific conditions of their decision procedures, their aims and settings are closely
aligned. Based on these foundations, our work extends this line of research by
exploring relative completeness in Incorrectness Separation Logic with array
predicates.
    We are also inspired by the work of [7], particularly their use of models
incorporating detailed block information for memory manipulation, especially
for allocation and deallocation. While [7] define array predicates based on start
points and sizes, our approach adopts the variable-length arr(x, y) style, consis-
tent with the settings of [1] and [8], to handle arrays flexibly.


5.2   Relative completeness of under-approximation logic

Relative completeness results have been established for various under-approximation
logics, including Incorrectness Logic (IL) [10] and Reverse Hoare Logic (RHL)
[5]. In IL, the proof of relative completeness relies on using semantic predicates,
which assume that expressiveness holds. In contrast, RHL [5], using syntactic
predicates, achieves relative completeness by generating the weakest postcondi-
tions via the function wpo and demonstrating its expressiveness.
     Building on these foundational methods, our prior work [9] established the
relative completeness of Incorrectness Separation Logic (ISL) in a system limited
to points-to predicates and negative heap predicates. Both [9] and the current
work follow the approach of [5] for proving relative completeness. However, this
work takes a different approach, unlike [9], which restricts its canonical form to
equalities and inequalities due to the absence of arithmetic. It extends the scope
by incorporating arithmetic into the logical framework, similar to [1] and [8]. This
enhancement allows the canonical form to account for all possible sequences of
strict inequalities and equalities.
         Incorrectness Separation Logic with Arrays and Pointer Arithmetic          23

6    Conclusions and Future work
We introduced an extended Incorrectness Separation Logic (ISL) with support
for variable-length array predicates and pointer arithmetic. Additionally, we es-
tablished the relative completeness of this enhanced ISL by constructing func-
tions wpo generating the weakest postcondition and demonstrating their expres-
siveness.
    For future work, while infinitary syntax aligns well with our goals of prov-
ing relative completeness, it is not ideally suited for the developing a practical
automatic theorem prover, a limitation shared by our earlier work [9]. Addition-
ally, we aim to simplify ISL with arrays by introducing more straightforward
proof rules. The current heap-manipulation rules are numerous, and their post-
conditions, which correspond to the output of the wpo function, are notably
complex. We acknowledge that this complexity is a trade-off made to achieve
simpler proofs for relative completeness. Therefore, our goal is to develop a ver-
sion of ISL with arrays that retains the expressiveness and relative completeness
properties of this work while employing simpler proof rules.

References
 1. Brotherston, J., Gorogiannis, N., Kanovich, M.: Biabduction (and related prob-
    lems) in array separation logic. In: Automated Deduction–CADE 26: 26th Inter-
    national Conference on Automated Deduction, Gothenburg, Sweden, August 6–11,
    2017, Proceedings. pp. 472–490. Springer (2017)
 2. Calcagno, C., Distefano, D.: Infer: An automatic program verifier for memory
    safety of c programs. In: NASA Formal Methods Symposium. pp. 459–465. Springer
    (2011)
 3. Calcagno, C., Distefano, D., O’Hearn, P. Open-sourcing Facebook Infer: Identify
    bugs before you ship. Facebook Engineering Blog, June 2015.
 4. Cook, S.A.: Soundness and completeness of an axiom system for program verifica-
    tion. SIAM Journal on Computing 7(1), 70–90 (1978)
 5. De Vries, E., Koutavas, V.: Reverse Hoare Logic. In: International Conference on
    Software Engineering and Formal Methods. pp. 155–171. Springer (2011)
 6. Hoare, C.A.R.: An axiomatic basis for computer programming. Communications
    of the ACM 12(10), 576–580 (1969)
 7. Holík, L., Peringer, P., Rogalewicz, A., Šoková, V., Vojnar, T., Zuleger, F.: Low-
    level bi-abduction. In: 36th European Conference on Object-Oriented Program-
    ming (ECOOP 2022). Schloss Dagstuhl-Leibniz-Zentrum für Informatik (2022)
 8. Kimura, D., Tatsuta, M.: Decidability for entailments of symbolic heaps with ar-
    rays. Logical Methods in Computer Science 17 (2021)
 9. Lee, Y., Nakazawa, K.: Relative completeness of incorrectness separation logic. In:
    Asian Symposium on Programming Languages and Systems. pp. 264–282. Springer
    (2024)
10. O’Hearn, P.W.: Incorrectness logic. Proceedings of the ACM on Programming Lan-
    guages 4(POPL), 1–32 (2019)
11. Raad, A., Berdine, J., Dang, H.H., Dreyer, D., O’Hearn, P., Villard, J.: Local
    reasoning about the presence of bugs: Incorrectness separation logic. In: Computer
    Aided Verification: 32nd International Conference, CAV 2020, Los Angeles, CA,
    USA, July 21–24, 2020, Proceedings, Part II 32. pp. 225–252. Springer (2020)
24      Y. Lee and K. Nakazawa

12. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    Proceedings 17th Annual IEEE Symposium on Logic in Computer Science. pp.
    55–74. IEEE (2002)
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                     25

A     Proof of Proposition 1 for x := alloc(t)
We prove that (s′ , h′ , B ′ ) |= wpo(ψ, x := alloc(t), ok) ⇐⇒ (s′ , h′ , B ′ ) ∈
WPO[[ψ, x := alloc(t), ok]] holds. By definition, (s′ , h′S, B ′ ) ∈ WPO[[ψ, x :=
alloc(t), ok]] is equivalent to ∃(s, h, B) |= ψ, l ∈ Val.( [u,v)∈B [u, v)) ∩ [l, l +
                                                                       [[t]]   −1
[[t]]s,B ) = ∅ ∧ (s′ , h′ , B ′ ) = (s[x 7→ l], h[l + i 7→ −]i=0s,B                  , B ∪ {[l, l + [[t]]s,B )}). In
this case, we suppose the following.
 – ψ = (∗m               ′        ′         ′
           i=1 arr(ti , t i )) ∗ ψ , where ψ contains no arr.
 – ψpure |= ti < ti+1 for 1 ≤ i < m.
 – ψpure |= null R1 u1 R1 u1 R2 · · · RN uN , where Ri ∈ {<, ≈} and termS− (ψ) =
   {ui | 1 ≤ i ≤ N }.
  Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, x := alloc(t), ok) ⇒ (s′ , h′ , B ′ ) ∈
WPO[[ψ, x := alloc(t), ok]].

A.1     (s′ , h′ , B ′ ) |= wpo(ψ, x := alloc(t), ok) ⇒ (s′ , h′ , B ′ ) ∈
        WPO[[ψ, x := alloc(t), ok]]
By (s′ , h′ , B ′ ) |= wpo(ψ, x := alloc(t), ok), which is of the form ∃x′ .χ, there
exists v ′ ∈ Val such that (s′ [x′ 7→ v ′ ], h′ , B ′ ) |= χ, and hence it satisfies one
of disjuncts in χ. Let s′′ be s′ [x′ 7→ v ′ ]. For brevity, we use the notation θ for
[x := x′ ] and t̃ for repβα (tθ) for some t, respectively.

Case 1 We demonstrate the case of
                                          j−1
                (s′′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x) ∗ arr(x, x + t̃)
                                           i=1
                                                                 m
                                    ∗ arr(x + t̃, t̃′k ) ∗     ∗ arr(t̃i , t̃′i )
                                                              i=k+1

                                    ∗ t̃j < x < t̃′j ∗ t̃k < x + t̃ < t̃′k
                                    ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                    ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

 for some α, β, j, k. [[[x]]s′′ ,B , [[x + t̃]]s′′ ,B ) ∈ B ′ holds, since (s′′ , B ′ ) |= b(x) ≈
x ∗ e(x) ≈ x + t̃. Define s = s′ [x 7→ v ′ ] and B = B ′ \ {[[[x]]s′′ ,B ′ , [[x + t̃]]s′′ ,B ′ )}.
    We can say that [[t̃]]s′′ ,B ′ = [[t]]s,B since the following derivation holds.
    Since t is b, e-free, the following is true:

                                  [[t̃]]s′′ ,B ′ = [[tθ]]s′′ ,B ′ = [[tθ]]s′′ ,B .

Additionally, by using Lemma 3 and the fact that x′ is fresh, the following holds:

 [[tθ]]s′′ ,B = [[t[x := x′ ]]]s′ [x′ 7→v′ ],B = [[t]]s′ [x′ 7→v′ ][x7→v′ ],B = [[t]]s′ [x7→v′ ],B = [[t]]s,B .

For any ui ∈ termS− (ψ), since ui contains neither b nor e, ũi = ui θ and its
semantics does not depend on B ′ . Hence, [[ũi ]]s′′ ,B ′ = [[ui ]]s,B by x′ 6∈ fv(ui )
26       Y. Lee and K. Nakazawa

similarly to the case of [[t̃]]s′′ ,B ′ = [[t]]s,B . Furthermore, we have [[x]]s′′ ,B ′ = s′ (x)
since x and x′ are distinct. Hence, B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )} since t ∈
termS− (ψ). Then, for any ui ∈ termS− (ψ), we have the following:

 – If α < i ≤ β, since (s′′ , B ′ ) satisfies x ≤ ũi < x + t̃, the value [[u˜i ]]s′′ ,B ′ =
   [[ui θ]]s′′ ,B ′ = [[ui ]]s,B is in the block [s′ (x), s′ (x)+[[t]]s,B ), and hence [[b(ui )]]s,B =
   [[e(ui )]]s,B = 0 by B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )}.
 – Otherwise, [[b(ui θ)]]s′′ ,B ′ = [[b(ui )]]s,B and [[e(ui θ)]]s′′ ,B ′ = [[e(ui )]]s,B .

Therefore, by the definition of repβα , [[r̃]]s′′ ,B ′ = [[r]]s,B holds for any r ∈ termS(ψ).
Hence, for any pure formula π in ψ, (s′′ , B ′ ) |= π̃ iff (s, B) |= π.
   Define h as
                                         [[t˜′ j ]] ′′   ′ −1           [[t̃j+1 ]] ′′     ′ −1
                     h = h′ [l 7→ ⊥]l=[[x]]s ′′,B ′ [l 7→ ↑]l=[[t˜′ ]]s ′′,B ′
                                                    s ,B                j s ,B

                                 [[t˜′ i ]]s′′ ,B ′ −1   [[t̃i+1 ]]s′′ ,B ′ −1 k−1
                                                                             
                       [l 7→ ⊥]l=[[t̃ ]] ′′ ′ [l 7→ ↑]l=[[t˜′ ]]
                                        i s ,B                           i s′′ ,B ′       i=j+1
                               [[x+t̃]] ′′ ′ −1
                       [l 7→ ⊥]l=[[t̃ ]]s ′′,B ′ ,
                                     k s ,B



which can be rewritten as
                                             [[t′ ]]      −1            [[t     ]]      −1
                        h = h′ [l 7→ ⊥]l=sj ′ (x)s,B
                                                     [l 7→ ↑]l=[[tj+1 s,B
                                                                     ′ ]]
                                                                      j s,B
                                      ′
                                                                          k−1
                                    [[t i ]]s,B −1       [[ti+1 ]]s,B −1
                          [l 7→ ⊥]l=[[ti ]]s,B [l 7→ ↑]l=[[t′ i ]]s,B
                                                                                        i=j+1
                                  s′ (x)+[[t]]   −1
                          [l 7→ ⊥]l=[[tk ]]s,Bs,B .

  Note that this is well-defined since (s′′ , B ′ ) |= x < t̃′j ∗ t̃k < x + t̃ and (s′′ , B ′ ) |=
t̃i < t̃i+1 for j ≤ i < k by ψpure |= ti < ti+1 . Moreover, (h, B) is exact since
dom+ (h) = dom+ (h′ ) \ [s′ (x), s′ (x) + [[t]]s,B ).
     Then, we have

                                     j−1
               (s′′ , h, B) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x)
                                      i=1
                                                         k−1
                                ∗ arr(x, t˜′ j ) ∗        ∗
                                                         i=j+1
                                                                arr(t̃i , t˜′ i ) ∗ arr(t˜′ k , x + t̃)
                                                              m
                                ∗ arr(x + t̃, t̃′k ) ∗          ∗
                                                              i=k+1
                                                                      arr(t̃i , t̃′i ),


 and then, appending arr(t̃j , x) ∗ arr(x, t˜′ j ) and arr(t˜′ k , x + t̃) ∗ arr(x + t̃, t̃′k ), we
have (s′′ , h, B) |= ψ̃ ′ ∗ ∗m
                             i=1 arr(ti , t̃i ), and hence, (s, h, B) |= ψ ∗ ∗i=1 arr(ti , t i ).
                                     ˜ ′                                   ′     m               ′

That means (s, h, B) |= ψ.
   Since s′ = s[x 7→ s′ (x)], we have ((s, h, B), (s′ , h′ , B ′ )) ∈ [[x := alloc(t)]]ok .
Hence, we have (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]].
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                  27

Case 2 We demonstrate the case of

                                             j−1
                  (s′′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(x, x + t̃)
                                              i=1
                                                                   m
                                      ∗ arr(x + t̃, t̃′k ) ∗     ∗ arr(t̃i , t̃′i)
                                                                i=k+1

                                      ∗ t˜′ j−1 ≤ x ≤ t̃j ∗ t̃k < x + t̃ < t̃′k
                                      ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                      ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,
    for some α, β, j, k. [[[x]]s′′ ,B , [[x + t̃]]s′′ ,B ) ∈ B ′ holds, since (s′′ , B ′ ) |= b(x) ≈
x ∗ e(x) ≈ x + t̃. Define s = s′ [x 7→ v ′ ] and B = B ′ \ {[[[x]]s′′ ,B ′ , [[x + t̃]]s′′ ,B ′ )}.
    We can say that [[t̃]]s′′ ,B ′ = [[t]]s,B since the following derivation holds.
    Since t is b, e-free, the following is true:
                                  [[t̃]]s′′ ,B ′ = [[tθ]]s′′ ,B ′ = [[tθ]]s′′ ,B .
Additionally, by using Lemma 3 and the fact that x′ is fresh, the following holds:
 [[tθ]]s′′ ,B = [[t[x := x′ ]]]s′ [x′ 7→v′ ],B = [[t]]s′ [x′ 7→v′ ][x7→v′ ],B = [[t]]s′ [x7→v′ ],B = [[t]]s,B .
For any ui ∈ termS− (ψ), since ui contains neither b nor e, ũi = ui θ and its
semantics does not depend on B ′ . Hence, [[ũi ]]s′′ ,B ′ = [[ui ]]s,B by x′ 6∈ fv(ui )
similarly to the case of [[t̃]]s′′ ,B ′ = [[t]]s,B . Furthermore, we have [[x]]s′′ ,B ′ = s′ (x)
since x and x′ are distinct. Hence, B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )} since t ∈
termS− (ψ). Then, for any ui ∈ termS− (ψ), we have the following:
 – If α < i ≤ β, since (s′′ , B ′ ) satisfies x ≤ ũi < x + t̃, the value [[u˜i ]]s′′ ,B ′ =
   [[ui θ]]s′′ ,B ′ = [[ui ]]s,B is in the block [s′ (x), s′ (x)+[[t]]s,B ), and hence [[b(ui )]]s,B =
   [[e(ui )]]s,B = 0 by B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )}.
 – Otherwise, [[b(ui θ)]]s′′ ,B ′ = [[b(ui )]]s,B and [[e(ui θ)]]s′′ ,B ′ = [[e(ui )]]s,B .
Therefore, by the definition of repβα , [[r̃]]s′′ ,B ′ = [[r]]s,B holds for any r ∈ termS(ψ).
Hence, for any pure formula π in ψ, (s′′ , B ′ ) |= π̃ iff (s, B) |= π.
   Define h as
                                           [[t̃j ]] ′′   ′ −1
                        h = h′ [l 7→↑]l=[[x]]     s ,B
                                                    s′′ ,B ′

                                    [[t˜′ i ]]s′′ ,B ′ −1    [[t̃i+1 ]] ′′ ′ −1 k−1
                                                                              
                           [l 7→ ⊥]l=[[t̃ ]] ′′ ′ [l 7→ ↑]l=[[t˜′ ]]s ′′,B ′
                                             i s ,B                     i s ,B        i=j
                                  [[x+t̃]] ′′ ′ −1
                          [l 7→ ⊥]l=[[t̃ ]]s ′′,B ′ ,
                                        k s ,B

    which can be rewritten as
                                              [[t ]]     −1
                           h = h′ [l 7→↑]l=s    j s,B
                                                   ′ (x)

                                         ′
                                                                                 k−1
                                       [[t i ]]s,B −1            [[ti+1 ]]s,B −1
                             [l 7→ ⊥]l=[[t     i ]]s,B
                                                         [l →
                                                            7 ↑]      ′
                                                                 l=[[t i ]]s,B
                                                                                     i=j
                                    s′ (x)+[[t]]   −1
                            [l 7→ ⊥]l=[[tk ]]s,Bs,B ,
28       Y. Lee and K. Nakazawa

    Note that this is well-defined since (s′′ , B ′ ) |= x < t̃′j ∗ t̃k < x + t̃ and
(s , B ′ ) |= t̃i < t̃i+1 for j ≤ i < k by ψpure |= ti < ti+1 . Moreover, (h, B) is exact
    ′′

since dom+ (h) = dom+ (h′ ) \ [s′ (x), s′ (x) + [[t]]s,B ).
    Then, we have
                                     j−1                        k−1
              (s′′ , h, B) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ ∗ arr(t̃i , t˜′ i )
                                      i=1                       i=j
                                                                                     m
                                ∗ arr(t̃k , x + t̃) ∗ arr(x + t̃, t̃′k ) ∗       ∗ arr(t̃i , t̃′i),
                                                                                i=k+1

    and then, appending arr(t˜′ k , x + t̃) ∗ arr(x + t̃, t̃′k ), we have (s′′ , h, B) |= ψ̃ ′ ∗
∗ m       ˜ ′                                  ′  m
                                                               ∗ ′
  i=1 arr(ti , t̃i ), and hence, (s, h, B) |= ψ ∗ i=1 arr(ti , t i ). That means (s, h, B) |=
ψ.
   Since s′ = s[x 7→ s′ (x)], we have ((s, h, B), (s′ , h′ , B ′ )) ∈ [[x := alloc(t)]]ok .
Hence, we have (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]].

Case 3 We demonstrate the case of

                                            j−1
                (s′′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x) ∗ arr(x, x + t̃)
                                          i=1
                                          m
                                    ∗    ∗
                                        i=k+1
                                                  arr(t̃i , t̃′i )

                                    ∗ t̃j < x < t̃′j ∗ t˜′ k ≤ x + t̃ ≤ t̃k+1
                                    ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                    ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

    for some α, β, j, k. [[[x]]s′′ ,B , [[x + t̃]]s′′ ,B ) ∈ B ′ holds, since (s′′ , B ′ ) |= b(x) ≈
x ∗ e(x) ≈ x + t̃. Define s = s′ [x 7→ v ′ ] and B = B ′ \ {[[[x]]s′′ ,B ′ , [[x + t̃]]s′′ ,B ′ )}.
    We can say that [[t̃]]s′′ ,B ′ = [[t]]s,B since the following derivation holds.
    Since t is b, e-free, the following is true:
                                  [[t̃]]s′′ ,B ′ = [[tθ]]s′′ ,B ′ = [[tθ]]s′′ ,B .
Additionally, by using Lemma 3 and the fact that x′ is fresh, the following holds:
 [[tθ]]s′′ ,B = [[t[x := x′ ]]]s′ [x′ 7→v′ ],B = [[t]]s′ [x′ 7→v′ ][x7→v′ ],B = [[t]]s′ [x7→v′ ],B = [[t]]s,B .

For any ui ∈ termS− (ψ), since ui contains neither b nor e, ũi = ui θ and its
semantics does not depend on B ′ . Hence, [[ũi ]]s′′ ,B ′ = [[ui ]]s,B by x′ 6∈ fv(ui )
similarly to the case of [[t̃]]s′′ ,B ′ = [[t]]s,B . Furthermore, we have [[x]]s′′ ,B ′ = s′ (x)
since x and x′ are distinct. Hence, B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )} since t ∈
termS− (ψ). Then, for any ui ∈ termS− (ψ), we have the following:
 – If α < i ≤ β, since (s′′ , B ′ ) satisfies x ≤ ũi < x + t̃, the value [[u˜i ]]s′′ ,B ′ =
   [[ui θ]]s′′ ,B ′ = [[ui ]]s,B is in the block [s′ (x), s′ (x)+[[t]]s,B ), and hence [[b(ui )]]s,B =
   [[e(ui )]]s,B = 0 by B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )}.
          Incorrectness Separation Logic with Arrays and Pointer Arithmetic                    29

 – Otherwise, [[b(ui θ)]]s′′ ,B ′ = [[b(ui )]]s,B and [[e(ui θ)]]s′′ ,B ′ = [[e(ui )]]s,B .


Therefore, by the definition of repβα , [[r̃]]s′′ ,B ′ = [[r]]s,B holds for any r ∈ termS(ψ).
Hence, for any pure formula π in ψ, (s′′ , B ′ ) |= π̃ iff (s, B) |= π.
   Define h as

                                        [[t˜′ j ]] ′′   ′ −1       [[t̃j+1 ]] ′′    ′ −1
                    h = h′ [l 7→ ⊥]l=[[x]]s ′′,B ′ [l 7→ ↑]l=[[t˜′ ]]s ,B
                                                   s ,B                j s′′ ,B ′

                                [[t˜′ i ]]s′′ ,B ′ −1   [[t̃i+1 ]]s′′ ,B ′ −1 k−1
                                                                             
                      [l 7→ ⊥]l=[[t̃ ]] ′′ ′ [l 7→ ↑]l=[[t˜′ ]]
                                        i s ,B                     i s′′ ,B ′       i=j+1
                              [[t˜′ k ]] ′′ ′ −1         [[x+t̃]] ′′ ′ −1
                      [l 7→ ⊥]l=[[t̃ s]] ,B       [l 7→↑]l=[[t˜′ s]] ,B    ,
                                       k s′′ ,B ′               k s′′ ,B ′




which can be rewritten as

                                            [[t′ ]]     −1         [[t     ]]      −1
                       h = h′ [l 7→ ⊥]l=sj ′ (x)s,B
                                                    [l 7→ ↑]l=[[tj+1 s,B
                                                                    ′ ]]
                                                                     j s,B
                                     ′
                                                                         k−1
                                   [[t i ]]s,B −1       [[ti+1 ]]s,B −1
                         [l 7→ ⊥]l=[[ti ]]s,B [l 7→ ↑]l=[[t′ i ]]s,B
                                                                                   i=j+1
                                [[t′ k ]]s,B −1        s′ (x)+[[t]]     −1
                        [l 7→ ⊥]l=[[t   k ]]s,B
                                                [l 7→↑]l=[[t′ k ]]s,Bs,B ,


  Note that this is well-defined since (s′′ , B ′ ) |= x < t̃′j ∗ t̃k < x + t̃ and (s′′ , B ′ ) |=
t̃i < t̃i+1 for j ≤ i < k by ψpure |= ti < ti+1 . Moreover, (h, B) is exact since
dom+ (h) = dom+ (h′ ) \ [s′ (x), s′ (x) + [[t]]s,B ).
     Then, we have

                                        j−1
                 (s′′ , h, B) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x) ∗ arr(x, t˜′ j )
                                        i=1
                                        m
                                  ∗    ∗
                                      i=j+1
                                                arr(t̃i , t̃′i )

                                  ∗ t̃j < x < t̃′j ∗ t˜′ k ≤ x + t̃ ≤ t̃k+1
                                  ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                  ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,


   and then, appending arr(t̃j , x)∗arr(x, t˜′ j ), we have (s′′ , h, B) |= ψ̃ ′ ∗∗m       ˜ ′
                                                                                   i=1 arr(ti , t̃i ),
and hence, (s, h, B) |= ψ ∗ ∗i=1 arr(ti , t i ). That means (s, h, B) |= ψ.
                           ′      m        ′

   Since s′ = s[x 7→ s′ (x)], we have ((s, h, B), (s′ , h′ , B ′ )) ∈ [[x := alloc(t)]]ok .
Hence, we have (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]].



Case 4 We demonstrate the case of
30       Y. Lee and K. Nakazawa



                                             j−1
                  (s′′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(x, x + t̃)
                                             i=1
                                             m
                                      ∗    ∗
                                          i=k+1
                                                       arr(t̃i , t̃′i )

                                      ∗ t˜′ j−1 ≤ x ≤ t̃j ∗ t˜′ k ≤ x + t̃ ≤ t̃k+1
                                      ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                      ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,
    for some α, β, j, k. [[[x]]s′′ ,B , [[x + t̃]]s′′ ,B ) ∈ B ′ holds, since (s′′ , B ′ ) |= b(x) ≈
x ∗ e(x) ≈ x + t̃. Define s = s′ [x 7→ v ′ ] and B = B ′ \ {[[[x]]s′′ ,B ′ , [[x + t̃]]s′′ ,B ′ )}.
    We can say that [[t̃]]s′′ ,B ′ = [[t]]s,B since the following derivation holds.
    Since t is b, e-free, the following is true:
                                  [[t̃]]s′′ ,B ′ = [[tθ]]s′′ ,B ′ = [[tθ]]s′′ ,B .
Additionally, by using Lemma 3 and the fact that x′ is fresh, the following holds:
 [[tθ]]s′′ ,B = [[t[x := x′ ]]]s′ [x′ 7→v′ ],B = [[t]]s′ [x′ 7→v′ ][x7→v′ ],B = [[t]]s′ [x7→v′ ],B = [[t]]s,B .
For any ui ∈ termS− (ψ), since ui contains neither b nor e, ũi = ui θ and its
semantics does not depend on B ′ . Hence, [[ũi ]]s′′ ,B ′ = [[ui ]]s,B by x′ 6∈ fv(ui )
similarly to the case of [[t̃]]s′′ ,B ′ = [[t]]s,B . Furthermore, we have [[x]]s′′ ,B ′ = s′ (x)
since x and x′ are distinct. Hence, B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )} since t ∈
termS− (ψ). Then, for any ui ∈ termS− (ψ), we have the following:
 – If α < i ≤ β, since (s′′ , B ′ ) satisfies x ≤ ũi < x + t̃, the value [[u˜i ]]s′′ ,B ′ =
   [[ui θ]]s′′ ,B ′ = [[ui ]]s,B is in the block [s′ (x), s′ (x)+[[t]]s,B ), and hence [[b(ui )]]s,B =
   [[e(ui )]]s,B = 0 by B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )}.
 – Otherwise, [[b(ui θ)]]s′′ ,B ′ = [[b(ui )]]s,B and [[e(ui θ)]]s′′ ,B ′ = [[e(ui )]]s,B .
Therefore, by the definition of repβα , [[r̃]]s′′ ,B ′ = [[r]]s,B holds for any r ∈ termS(ψ).
Hence, for any pure formula π in ψ, (s′′ , B ′ ) |= π̃ iff (s, B) |= π.
   Define h as
                                           [[t̃j ]] ′′    ′ −1
                        h = h′ [l 7→↑]l=[[x]]     s ,B
                                                    s′′ ,B ′

                                    [[t˜′ i ]]s′′ ,B ′ −1    [[t̃i+1 ]] ′′ ′ −1 k−1
                                                                              
                           [l 7→ ⊥]l=[[t̃ ]] ′′ ′ [l 7→ ↑]l=[[t˜′ ]]s ′′,B ′
                                             i s ,B                       i s ,B      i=j
                                  [[t˜′ k ]] ′′ ′ −1         [[x+t̃]] ′′ ′ −1
                          [l 7→ ⊥]l=[[t̃ s]] ,B       [l 7→↑]l=[[t˜′ s]] ,B ,
                                           k s′′ ,B ′               k s′′ ,B ′

which can be rewritten as

                                              [[t ]]       −1
                           h = h′ [l 7→↑]l=s    j s,B
                                                   ′ (x)

                                         ′
                                                                                 k−1
                                       [[t i ]]s,B −1            [[ti+1 ]]s,B −1
                             [l 7→ ⊥]l=[[t     i ]]s,B
                                                         [l →
                                                            7 ↑]      ′
                                                                 l=[[t i ]]s,B
                                                                                     i=j
                                    [[t′ k ]]s,B −1        s′ (x)+[[t]]     −1
                            [l 7→ ⊥]l=[[t   k ]]s,B
                                                    [l 7→↑]l=[[t′ k ]]s,Bs,B ,
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                  31

  Note that this is well-defined since (s′′ , B ′ ) |= x < t̃′j ∗ t̃k < x + t̃ and (s′′ , B ′ ) |=
t̃i < t̃i+1 for j ≤ i < k by ψpure |= ti < ti+1 . Moreover, (h, B) is exact since
dom+ (h) = dom+ (h′ ) \ [s′ (x), s′ (x) + [[t]]s,B ).
     Then, we have
                                    j−1                     k                        m
            (s′′ , h, B) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ ∗ arr(t̃i , t˜′ i ) ∗      ∗ arr(t̃i , t̃′i ),
                                    i=1                   i=j                    i=k+1


   and then, we have (s′′ , h, B) |= ψ̃ ′ ∗ ∗m          ˜ ′
                                                i=1 arr(ti , t̃i ), and hence, (s, h, B) |=
ψ ∗ ∗i=1 arr(ti , t i ). That means (s, h, B) |= ψ.
 ′    m            ′

   Since s′ = s[x 7→ s′ (x)], we have ((s, h, B), (s′ , h′ , B ′ )) ∈ [[x := alloc(t)]]ok .
Hence, we have (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]].


Case 5 We demonstrate the case of


                  (s′′ , h′ , B ′ ) |=ψ̃ ∗ arr(x, x + t̃)
                                      ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                      ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

    for some α, β. [[[x]]s′′ ,B , [[x + t̃]]s′′ ,B ) ∈ B ′ holds, since (s′′ , B ′ ) |= b(x) ≈
x ∗ e(x) ≈ x + t̃. Define s = s′ [x 7→ v ′ ] and B = B ′ \ {[[[x]]s′′ ,B ′ , [[x + t̃]]s′′ ,B ′ )}.
    We can say that [[t̃]]s′′ ,B ′ = [[t]]s,B since the following derivation holds.
    Since t is b, e-free, the following is true:

                                  [[t̃]]s′′ ,B ′ = [[tθ]]s′′ ,B ′ = [[tθ]]s′′ ,B .

Additionally, by using Lemma 3 and the fact that x′ is fresh, the following holds:

 [[tθ]]s′′ ,B = [[t[x := x′ ]]]s′ [x′ 7→v′ ],B = [[t]]s′ [x′ 7→v′ ][x7→v′ ],B = [[t]]s′ [x7→v′ ],B = [[t]]s,B .

For any ui ∈ termS− (ψ), since ui contains neither b nor e, ũi = ui θ and its
semantics does not depend on B ′ . Hence, [[ũi ]]s′′ ,B ′ = [[ui ]]s,B by x′ 6∈ fv(ui )
similarly to the case of [[t̃]]s′′ ,B ′ = [[t]]s,B . Furthermore, we have [[x]]s′′ ,B ′ = s′ (x)
since x and x′ are distinct. Hence, B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )} since t ∈
termS− (ψ). Then, for any ui ∈ termS− (ψ), we have the following:

 – If α < i ≤ β, since (s′′ , B ′ ) satisfies x ≤ ũi < x + t̃, the value [[u˜i ]]s′′ ,B ′ =
   [[ui θ]]s′′ ,B ′ = [[ui ]]s,B is in the block [s′ (x), s′ (x)+[[t]]s,B ), and hence [[b(ui )]]s,B =
   [[e(ui )]]s,B = 0 by B = B ′ \ {[s′ (x), s′ (x) + [[t]]s,B )}.
 – Otherwise, [[b(ui θ)]]s′′ ,B ′ = [[b(ui )]]s,B and [[e(ui θ)]]s′′ ,B ′ = [[e(ui )]]s,B .

Therefore, by the definition of repβα , [[r̃]]s′′ ,B ′ = [[r]]s,B holds for any r ∈ termS(ψ).
Hence, for any pure formula π in ψ, (s′′ , B ′ ) |= π̃ iff (s, B) |= π.
   Define h as
32      Y. Lee and K. Nakazawa




                                                [[x+t̃]] ′′   ′ −1
                               h = h′ [l 7→↑]l=[[x]] s′′ ,B′
                                                       s ,B



which can be rewritten as


                                               s′ (x)+[[t]]    −1
                               h = h′ [l 7→↑]l=s′ (x) s,B

Moreover, (h, B) is exact since dom+ (h) = dom+ (h′ ) \ [s′ (x), s′ (x) + [[t]]s,B ).
  Then, we have

                                     (s′′ , h, B) |= ψ̃

   and then, we have (s, h, B) |= ψ.
   Since s′ = s[x 7→ s′ (x)], we have ((s, h, B), (s′ , h′ , B ′ )) ∈ [[x := alloc(t)]]ok .
Hence, we have (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]].


A.2    (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]] ⇒ (s′ , h′ , B ′ ) |=
       wpo(ψ, x := alloc(t), ok)

Next, we prove the converse: (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t), ok]] ⇒ (s′ , h′ , B ′ ) |=
wpo(ψ, x := alloc(t), ok). We frequently use the notation h[l 7→ −] to denote
that l maps to some value.
      Assume (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := alloc(t),     S ok]], and then there exists
(s, h, B) and l ∈ Loc such that (s, h, B) |= ψ, ( B) ∩ [l, l + [[t]]s,B ) = ∅, and
                                            [[t]] −1
(s′ , h′ , B ′ ) = (s[x 7→ l], h[l + i 7→ −]i=0s,B , B ∪ {[l, l + [[t]]s,B )}). Then, l = s′ (x)
holds. Since x′ is fresh, these do not depend on the value of s(x′ ), so we can
assume s(x′ ) = s′ (x). Then, s′ = s[x′ 7→ s(x)] holds.
     Since (s, h, B) |= ψ holds, h is of the form

                                h = h1 ◦ · · · ◦ hm ◦ h′′ ,

where (s, hi , B) |= arr(ti , t′ i ) for 1 ≤ i ≤ m and (s, h′′ , B) |= ψ ′ . That is,
dom(hi ) = dom− (hi ) = [[[ti ]]s,B , [[t′ i ]]s,B ) for each i.
    Moreover, we have (s, B) |= ti < t′ i ≤ ti+1 for each i and (s, B) |= nullR1 u1 · · · RN uN
for ui ∈ termS− (ψ). Without loss of generality, we assume [[uα ]]s,B < s′ (x) ≤
[[uα+1 ]]s,B and [[uβ ]]s,B < s′ (x) + [[t]]s,B ≤ [[uβ+1 ]]s,B for some α, β. If β = N ,
ignore [[uβ+1 ]]s,B . Then, we can show [[r]]s,B = [[r̃]]s′ ,B ′ as in the previous case
where r̃ = repβα (rθ). Hence, by (s, h, B) |= ψ, we have (s′ , B ′ ) satisfies ψ̃pure ,
b(x) ≈ x ∗ e(x) ≈ x + t̃, ũα < x ≤ ũα+1 , and ũβ < x + t̃ ≤ ũβ+1 .
    In the following, we divide the cases depending on where the value of s′ (x)
and s′ (x) + [[t]]s,B are in the sequence of [[ti ]]s,B and [[t′ i ]]s,B for 1 ≤ i ≤ m.
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                     33

Case 1 If [[tj ]]s,B < s′ (x) < [[t′ j ]]s,B and [[tk ]]s,B < s′ (x) + [[t]]s,B < [[t′ k ]]s,B holds
                                                                                       [[t]]  −1
for some 1 ≤ j ≤ k ≤ m. In this case, in the heap h′ = h[s′ (x)+i 7→ −]i=0s,B , hj
is divided into two parts h′1               ′2               ′1
                                 j and hj such that hj is hj whose domain is shorten
to [[[tj ]]s,B , s (x)) and dom(hj ) = dom+ (hj ) = [s′ (x), [[t′ j ]]s,B ). Similarly, hk is
                  ′                 ′2              ′2

divided into h′1              ′2               ′1                  ′1              ′
                    k and hk , where dom(hk ) = dom+ (hk ) = [[[tk ]]s,B , s (x) + [[t]]s,B )
and hk is hk whose domain is shorten to [s (x) + [[t]]s,B , [[t k ]]s,B ). Then, h′
         ′2                                                ′                  ′

can be written as h′ = h1 ◦ · · · ◦ hj−1 ◦ h′1                 ′′′    ′2
                                                       j ◦ h ◦ hk ◦ hk+1 · · · ◦ hm , where
         ′′′              ′′′     ′       ′
dom(h ) = dom+ (h ) = [s (x), s (x) + [[t]]s,B ).
    From the above and [[r]]s,B = [[r̃]]s′ ,B ′ , we have

                                        j−1
                (s′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x) ∗ arr(x, x + t̃)
                                        i=1
                                                             m
                                  ∗ arr(x + t̃, t̃′k ) ∗     ∗
                                                           i=k+1
                                                                     arr(t̃i , t̃′i )

                                  ∗ t̃j < x < t̃′j ∗ t̃k < x + t̃ < t̃′k
                                  ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                  ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

which is one of the disjuncts in χ such that wpo(ψ, x := alloc(t), ok ) = ∃x′ .χ.


Case 2 If [[t′ j−1 ]]s,B ≤ s′ (x) ≤ [[tj ]]s,B and [[tk ]]s,B < s′ (x) + [[t]]s,B < [[t′ k ]]s,B
holds for some 1 ≤ j ≤ k ≤ m. In this case, in the heap h′ = h[s′ (x) + i 7→
    [[t]]  −1
−]i=0s,B , hk is divided into h′1                   ′2               ′1
                                          k and hk , where dom(hk ) = dom+ (hk ) =
                                                                                       ′1

[[[tk ]]s,B , s (x)+[[t]]s,B ) and hk is hk whose domain is shorten to [s (x)+[[t]]s,B , [[t′ k ]]s,B ).
               ′                    ′2                                   ′

Then, h′ can be written as h′ = h1 ◦ · · · ◦ hj−1 ◦ h′′′ ◦ h′2  k ◦ hk+1 · · · ◦ hm , where
dom(h′′′ ) = dom+ (h′′′ ) = [s′ (x), s′ (x) + [[t]]s,B ).
      From the above and [[r]]s,B = [[r̃]]s′ ,B ′ , we have

                                          j−1
                 (s′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(x, x + t̃)
                                          i=1
                                                                 m
                                    ∗ arr(x + t̃, t̃′k ) ∗    ∗ arr(t̃i , t̃′i )
                                                             i=k+1

                                    ∗ t˜′ j−1 ≤ x ≤ t̃j ∗ t̃k < x + t̃ < t̃′k
                                    ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                    ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

which is one of the disjuncts in χ such that wpo(ψ, x := alloc(t), ok ) = ∃x′ .χ.


Case 3 If [[tj ]]s,B < s′ (x) < [[t′ j ]]s,B and [[t′ k ]]s,B ≤ s′ (x) + [[t]]s,B ≤ [[t′ k+1 ]]s,B
holds for some 1 ≤ j ≤ k ≤ m. In this case, in the heap h′ = h[s′ (x) + i 7→
  [[t]] −1
−]i=0s,B , hj is divided into two parts h′1                   ′2                ′1
                                                 j and hj such that hj is hj whose
domain is shorten to [[[tj ]]s,B , s (x)) and dom(hj ) = dom+ (hj ) = [s′ (x), [[t′ j ]]s,B ).
                                    ′                  ′2              ′2
34       Y. Lee and K. Nakazawa

Then, h′ can be written as h′ = h1 ◦ · · · ◦ hj−1 ◦ h′1      ′′′ ′
                                                        j ◦ h ◦ hk+1 ◦ · · · ◦ hm , where
      ′′′          ′′′     ′     ′
dom(h ) = dom+ (h ) = [s (x), s (x) + [[t]]s,B ).
   From the above and [[r]]s,B = [[r̃]]s′ ,B ′ , we have

                                        j−1
                (s′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(t̃j , x) ∗ arr(x, x + t̃)
                                        i=1
                                        m
                                  ∗    ∗
                                      i=k+1
                                              arr(t̃i , t̃′i )

                                  ∗ t̃j < x < t̃′j ∗ t̃k < x + t̃ < t̃′k
                                  ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                  ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

which is one of the disjuncts in χ such that wpo(ψ, x := alloc(t), ok ) = ∃x′ .χ.


Case 4 If [[t′ j−1 ]]s,B ≤ s′ (x) ≤ [[tj ]]s,B and [[t′ k ]]s,B ≤ s′ (x) + [[t]]s,B ≤ [[tk+1 ]]s,B
holds for some 1 ≤ j ≤ k ≤ m. Then, h′ can be written as h′ = h1 ◦ · · · ◦ hj−1 ◦
h′′′ ◦ hk+1 · · · ◦ hm , where dom(h′′′ ) = dom+ (h′′′ ) = [s′ (x), s′ (x) + [[t]]s,B ).
     From the above and [[r]]s,B = [[r̃]]s′ ,B ′ , we have

                                    j−1                                         m
            (s′ , h′ , B ′ ) |=ψ̃ ′ ∗ ∗ arr(t˜i , t̃′i ) ∗ arr(x, x + t̃) ∗    ∗ arr(t̃i , t̃′i)
                                    i=1                                       i=k+1

                              ∗ t̃j < x < t̃′j ∗ t̃k < x + t̃ < t̃′k
                              ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                              ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

which is one of the disjuncts in χ such that wpo(ψ, x := alloc(t), ok ) = ∃x′ .χ.


Case 5 Otherwise, one of the following conditions holds:

 – [[t′ i ]]s,B ≤ s′ (x) < s′ (x) + [[t]]s,B ≤ [[ti+1 ]]s,B holds for some i.
 – s′ (x) + [[t]]s,B < [[t1 ]]s,B or s′ (x) ≥ [[t′ m ]]s,B hold.

In either case, h′ can be written as h′ = h1 ◦ · · · ◦ hm ◦ h′′′ , where dom(h′′′ ) =
dom+ (h′′′ ) = [s′ (x), s′ (x) + [[t]]s,B ).
    From the above and [[r]]s,B = [[r̃]]s′ ,B ′ , we have

                 (s′ , h′ , B ′ ) |=ψ̃ ∗ arr(x, x + t̃)
                                      ∗ b(x) ≈ x ∗ e(x) ≈ x + t̃
                                      ∗ ũα < x ≤ ũα+1 ∗ ũβ < x + t̃ ≤ ũβ+1 ,

which is one of the disjuncts in χ such that wpo(ψ, x := alloc(t), ok ) = ∃x′ .χ.
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                            35

B      Proof of Proposition 1 for free(t)

We prove (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇐⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]]
holds. By definition, (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]] is equivalent to ∃(s, h, B) |=
                                                                                   eB ([[t]]s,B )−1
ψ.[[t]]s,B = bB ([[t]]s,B ) ∧ bB ([[t]]s,B ) > 0 ∧ (s′ , h′ , B ′ ) = (s, h[i 7→ ⊥]i=b B ([[t]]s,B )
                                                                                                     ,B\
{[bB ([[t]]s,B ), eB ([[t]]s,B ))}).


B.1     (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈
        WPO[[ψ, free(t), ok]]

Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]].


Case 1 We prove the case for ψ = arr(t1 , t′ 1 ) ∗ ∗i=2      k−1
                                                                  Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′
and ψpure |= t1 < b(t) < t 1 ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗i=1
                            ′                     ′
                                                                           t i ≈ ti+1 ∗ ∗i=1
                                                                       k−1 ′                   k−1
                                                                                                     ti <
ti+1 for some k, ψ ′ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y]
for brevity.
    By the assumption, we have (s′ , h′ , B ′ ) |= ∃y.(arr(t1 , t) ∗ arr(t, y) ∗ arr(y, t′ k ) ∗
ψ )τ , and then (s′ [y 7→ v], h′ , B ′ ) |= (arr(t1 , t) ∗ arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ for some
  ′

v ∈ Loc. Let s′′ = s′ [y 7→ v].
    Define

            s =s′ ,
            B =B ′ ∪ {[[[t]]s′′ ,B ′ , v)} = B ′ ∪ {[[[t]]s,B , v)},
                            [[t′ 1 ]]    −1             [[t′ i ]]s,B −1 k−1
                                                                      
            h =h′ [l 7→ −]l=[[t]]s,B  s,B
                                              [l →
                                                 7 vl ] l=[[ti ]]           [l 7→ −]v−1
                                                                                    l=[[tk ]]     ,
                                                              s,B     i=2                   s,B



where v[[ti ]]s,B = [[αi ]]s,B if Arr(ti , t′ i )αi = ti 7→ αi . Otherwise, we do not care
about the value of vl , i.e., we simply consider vl as −.
      Since t contains neither y, b, nor e, and hence we have tτ = t and [[t]]S                  s′ ,B ′ =
[[t]]s,B . Since (s′′ , h′ , B ′ ) contains a portion satisfying arr(t, y), and hence ( B ′ )∩
[[[t]]s′′ ,B ′ , v) = ∅.
      For any term r ∈ termS− (ψ), if ψpure |= b(r) ≈ b(t), we have [[b(r)]]s,B =
[[b(t)]]s,B = [[t]]s,B = [[t]]s′ ,B ′ , and otherwise, we have [[b(r)]]s,B = [[b(r)]]s′ ,B ′ .
If ψpure |= e(r) ≈ e(t), we have [[e(r)]]s,B = v = [[y]]s′ ,B ′ , and otherwise, we
have [[e(r)]]s,B = [[e(r)]]s′ ,B ′ . Hence, we have [[r]]s,B = [[rτ ]]s′ ,B ′ for any term
r ∈ termS(ψ).
      Since ψpure |= t < t′ 1 ∗ ∗i=1     k−1 ′
                                             (t i ≈ ti+1 ∗ ti < ti+1 ) ∗ tk ≤ e(t) < t′ k , we
have [[t]]s,B < [[t 1 ]]s,B = [[t2 ]]s,B < [[t′ 2 ]]s,B = · · · [[tk ]]s,B < v < [[t′ k ]]s,B . Hence, h
                        ′

is well-defined, and we have (s, h, B) |= ψ. Furthermore, by definition, we have
((s, h, B), (s′ , h′ , B ′ )) ∈ [[free(t)]]ok .


Case 2 We prove the case for ψ = ∗i=1       k−1
                                                Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′ and
ψpure |= t1 ≈ b(t) ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗i=1
                                  ′                 k−1 ′
                                                           t i ≈ ti+1 ∗ ∗i=1  k−1
                                                                                    ti < ti+1
36        Y. Lee and K. Nakazawa

for some k, ψ ′ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for
brevity.
    We prove (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]].
    By the assumption, we have (s′ , h′ , B ′ ) |= ∃y.(arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ , and
then (s′ [y 7→ v], h′ , B ′ ) |= (arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ for some v ∈ Loc. Let
s′′ = s′ [y 7→ v].
    Define
                      s =s′ ,
                      B =B ′ ∪ {[[[t]]s′′ ,B ′ , v)} = B ′ ∪ {[[[t]]s,B , v)},
                                         [[t′ i ]]    −1 k−1
                                                       
                      h =h′ [l 7→ vl ]l=[[tis,B    ]]        [l 7→ −]v−1
                                                                      l=[[tk ]] ,
                                                  s,B    i=1                  s,B

                                              ′
where v[[ti ]]s,B = [[αi ]]s,B if Arr(ti , t i )αi = ti 7→ αi . Otherwise, we do not care
about the value of vl , i.e., we simply consider vl as −.
      Since t contains neither y, b, nor e, and hence we have tτ = t and [[t]]S                  s′ ,B ′ =
[[t]]s,B . Since (s′′ , h′ , B ′ ) contains a portion satisfying arr(t, y), and hence ( B ′ )∩
[[[t]]s′′ ,B ′ , v) = ∅.
      For any term r ∈ termS− (ψ), if ψpure |= b(r) ≈ b(t), we have [[b(r)]]s,B =
[[b(t)]]s,B = [[t]]s,B = [[t]]s′ ,B ′ , and otherwise, we have [[b(r)]]s,B = [[b(r)]]s′ ,B ′ .
If ψpure |= e(r) ≈ e(t), we have [[e(r)]]s,B = v = [[y]]s′ ,B ′ , and otherwise, we
have [[e(r)]]s,B = [[e(r)]]s′ ,B ′ . Hence, we have [[r]]s,B = [[rτ ]]s′ ,B ′ for any term
r ∈ termS(ψ).
      Since ψpure |= t < t′ 1 ∗ ∗i=1     k−1 ′
                                             (t i ≈ ti+1 ∗ ti < ti+1 ) ∗ tk ≤ e(t) < t′ k , we
have [[t]]s,B < [[t 1 ]]s,B = [[t2 ]]s,B < [[t′ 2 ]]s,B = · · · [[tk ]]s,B < v < [[t′ k ]]s,B . Hence, h
                        ′

is well-defined, and we have (s, h, B) |= ψ. Furthermore, by definition, we have
((s, h, B), (s′ , h′ , B ′ )) ∈ [[free(t)]]ok .

Case 3 We prove the case for ψ = ∗ki=1 Arr(ti , t′ i )αi ∗ ψ ′ and ψpure |= t1 ≈
b(t) ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1   k−1 ′
                                            t i ≈ ti+1 ∗ ∗i=1
                                                          k−1
                                                              ti < ti+1 for some k, ψ ′ . We
use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for brevity.
    We prove (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]].
    By the assumption, we have (s′ , h′ , B ′ ) |= ∃y.(arr(t, y)∗ψ ′ )τ , and then (s′ [y 7→
v], h′ , B ′ ) |= (arr(t, y) ∗ ψ ′ )τ for some v ∈ Loc. Let s′′ = s′ [y 7→ v].
    Define
                        s =s′ ,
                        B =B ′ ∪ {[[[t]]s′′ ,B ′ , v)} = B ′ ∪ {[[[t]]s,B , v)},
                                           [[t′ i ]]    −1 k
                                                         
                        h =h′ [l 7→ vl ]l=[[tis,B    ]]      ,
                                                   s,B    i=1
                                              ′
where v[[ti ]]s,B = [[αi ]]s,B if Arr(ti , t i )αi = ti 7→ αi . Otherwise, we do not care
about the value of vl , i.e., we simply consider vl as −.
      Since t contains neither y, b, nor e, and hence we have tτ = t and [[t]]S        s′ ,B ′ =
[[t]]s,B . Since (s′′ , h′ , B ′ ) contains a portion satisfying arr(t, y), and hence ( B ′ )∩
[[[t]]s′′ ,B ′ , v) = ∅.
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                         37

     For any term r ∈ termS− (ψ), if ψpure |= b(r) ≈ b(t), we have [[b(r)]]s,B =
[[b(t)]]s,B = [[t]]s,B = [[t]]s′ ,B ′ , and otherwise, we have [[b(r)]]s,B = [[b(r)]]s′ ,B ′ .
If ψpure |= e(r) ≈ e(t), we have [[e(r)]]s,B = v = [[y]]s′ ,B ′ , and otherwise, we
have [[e(r)]]s,B = [[e(r)]]s′ ,B ′ . Hence, we have [[r]]s,B = [[rτ ]]s′ ,B ′ for any term
r ∈ termS(ψ).
     Since ψpure |= t < t′ 1 ∗ ∗i=1    k−1 ′
                                            (t i ≈ ti+1 ∗ ti < ti+1 ) ∗ tk < e(t) ≈ t′ k , we
have [[t]]s,B < [[t 1 ]]s,B = [[t2 ]]s,B < [[t′ 2 ]]s,B = · · · [[tk ]]s,B < v ≈ [[t′ k ]]s,B . Hence, h
                     ′

is well-defined, and we have (s, h, B) |= ψ. Furthermore, by definition, we have
((s, h, B), (s′ , h′ , B ′ )) ∈ [[free(t)]]ok .



Case 4 We prove the case for ψ = arr(t1 , t′ 1 )∗ ∗ki=2 Arr(ti , t′ i )αi ∗ ψ ′ and ψpure |=
t1 < b(t) < t′ 1 ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1     t i ≈ ti+1 ∗ ∗i=1
                                                 k−1 ′                k−1
                                                                          ti < ti+1 for some
     ′
k, ψ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for brevity.
    We prove (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]].
    By the assumption, we have (s′ , h′ , B ′ ) |= ∃y.(arr(t1 , t) ∗ arr(t, y) ∗ ψ ′ )τ , and
then (s′ [y 7→ v], h′ , B ′ ) |= (arr(t1 , t) ∗ arr(t, y) ∗ ψ ′ )τ for some v ∈ Loc. Let
s′′ = s′ [y 7→ v].
    Define

                      s =s′ ,
                      B =B ′ ∪ {[[[t]]s′′ ,B ′ , v)} = B ′ ∪ {[[[t]]s,B , v)},
                                      [[t′ 1 ]]    −1             [[t′ i ]]s,B −1 k
                                                                                
                      h =h′ [l 7→ −]l=[[t]]s,B  s,B
                                                        [l →
                                                           7 vl ] l=[[ti ]]         ,
                                                                        s,B    i=2


where v[[ti ]]s,B = [[αi ]]s,B if Arr(ti , t′ i )αi = ti 7→ αi . Otherwise, we do not care
about the value of vl , i.e., we simply consider vl as −.
      Since t contains neither y, b, nor e, and hence we have tτ = t and [[t]]S        s′ ,B ′ =
[[t]]s,B . Since (s′′ , h′ , B ′ ) contains a portion satisfying arr(t, y), and hence ( B ′ )∩
[[[t]]s′′ ,B ′ , v) = ∅.
     For any term r ∈ termS− (ψ), if ψpure |= b(r) ≈ b(t), we have [[b(r)]]s,B =
[[b(t)]]s,B = [[t]]s,B = [[t]]s′ ,B ′ , and otherwise, we have [[b(r)]]s,B = [[b(r)]]s′ ,B ′ .
If ψpure |= e(r) ≈ e(t), we have [[e(r)]]s,B = v = [[y]]s′ ,B ′ , and otherwise, we
have [[e(r)]]s,B = [[e(r)]]s′ ,B ′ . Hence, we have [[r]]s,B = [[rτ ]]s′ ,B ′ for any term
r ∈ termS(ψ).
     Since ψpure |= t < t′ 1 ∗ ∗i=1    k−1 ′
                                            (t i ≈ ti+1 ∗ ti < ti+1 ) ∗ tk ≤ e(t) < t′ k , we
have [[t]]s,B < [[t 1 ]]s,B = [[t2 ]]s,B < [[t′ 2 ]]s,B = · · · [[tk ]]s,B < v < [[t′ k ]]s,B . Hence, h
                     ′

is well-defined, and we have (s, h, B) |= ψ. Furthermore, by definition, we have
((s, h, B), (s′ , h′ , B ′ )) ∈ [[free(t)]]ok .



Case 5 Otherwise, (s′ , h′ , B ′ ) |= wpo(ψ, free(t), ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]]
holds trivially since wpo(ψ, free(t), ok) = false.
38       Y. Lee and K. Nakazawa

B.2     (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]] ⇒ (s′ , h′ , B ′ ) |=
        wpo(ψ, free(t), ok)

Next, we prove the converse: (s′ , h′ , B ′ ) ∈ WPO[[ψ, free(t), ok]] ⇒ (s′ , h′ , B ′ ) |=
wpo(ψ, free(t), ok). By the assumption, there exists (s, h, B) such that

 – (s, h, B) |= ψ,
                                     eB ([[t]]    )−1
 – (s′ , h′ , B ′ ) = (s, h[l 7→ ⊥]l=[[t]] s,B          , B \ {[[[t]]s,B , eB ([[ts,B ]]))}),
                                            s,B

 – [[t]]s,B = bB ([[t]]s,B ) > 0.


Case 1 We prove the case for ψ = arr(t1 , t′ 1 ) ∗ ∗i=2   k−1
                                                               Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′
and ψpure |= t1 < b(t) < t 1 ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗i=1
                              ′                  ′                   k−1 ′
                                                                           t i ≈ ti+1 ∗ ∗i=1
                                                                                           k−1
                                                                                                  ti <
                      ′
ti+1 for some k, ψ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y]
for brevity.
    Since ψ = arr(t1 , t′ 1 ) ∗ ∗i=2
                                 k−1
                                     Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′ , h is of the form
                        ′′
h1 ◦ h2 ◦ · · · ◦ hk ◦ h such that

 – (s, h1 , B) |= arr(t1 , t′ 1 ),
 – (s, hi , B) |= Arr(ti , t′ i )αi for 2 ≤ i ≤ k − 1,
 – (s, hk , B) |= arr(tk , t′ k ),
 – (s, h′′ , B) |= ψ ′ .

Since (s, B) satisfies t1 < t ≈ b(t) < t′ 1 and tk < e(t) < t′ k , h1 is divided into two
portions h11 and h21 , where h11 is h1 whose domain is shorten to [[[t1 ]]s,B , [[t]]s,B )
and h21 (l) = ⊥ for l ∈ [[[t]]s,B , [[t′ 1 ]]s,B ). Similarly, hk is divided into two portions
h1k and h2k , where h2k is hk whose domain is shorten to [eB ([[t]]s,B ), [[t′ k ]]s,B ) and
h1k (l) = ⊥ for l ∈ [[[tk ]]s,B , eB ([[t]]s,B )). Furthermore, we have (s, B) |= t′ i ≈ ti+1
for 1 ≤ i < k. Then, h′ can be written as h11 ◦ h⊥ ◦ h2k ◦ h′′ , where dom(h⊥ ) =
dom− (h⊥ ) = [[[t]]s,B , eB ([[t]]s,B )).
     As in the previous case, [[r]]s,B = [[rτ ]]s′ ,B ′ holds. Therefore, we have (s′ [y 7→
eB ([[t]]s,B )], h′ , B ′ ) |= (arr(t1 , t) ∗ arr(t, y) ∗ arr(y, t′ k ) ∗ ψ ′ )τ , and then (s′ , h′ , B ′ ) |=
∃y.(arr(t1 , t)∗arr(t, y)∗arr(y, t′ k )∗ψ ′ )τ . That means (s′ , h′ , B ′ ) satisfies wpo(ψ, free(t), ok ).


Case 2 We prove the case for ψ = ∗i=1                k−1
                                                          Arr(ti , t′ i )αi ∗ arr(tk , t′ k ) ∗ ψ ′ and
ψpure |= t1 ≈ b(t) ∗ tk < e(t) < t k ∗ b(t) ≈ t ∗ ∗i=1
                                        ′                       k−1 ′
                                                                     t i ≈ ti+1 ∗ ∗i=1  k−1
                                                                                              ti < ti+1
             ′
for some k, ψ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for
brevity.
    Since ψ = ∗i=1
                k−1
                    Arr(ti , t′ i )αi ∗arr(tk , t′ k )∗ψ ′ , h is of the form h1 ◦h2 ◦· · ·◦hk ◦h′′
such that

 – (s, hi , B) |= Arr(ti , t′ i )αi for 1 ≤ i ≤ k − 1,
 – (s, hk , B) |= arr(tk , t′ k ),
 – (s, h′′ , B) |= ψ ′ .
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                           39

Since (s, B) satisfies t1 ≈ t ≈ b(t) < t′ 1 and tk < e(t) < t′ k , hk is di-
vided into two portions h1k and h2k , where h2k is hk whose domain is shorten
to [eB ([[t]]s,B ), [[t′ k ]]s,B ) and h1k (l) = ⊥ for l ∈ [[[tk ]]s,B , eB ([[t]]s,B )). Furthermore,
we have (s, B) |= t′ i ≈ ti+1 for 1 ≤ i < k. Then, h′ can be written as h⊥ ◦ h2k ◦ h′′ ,
where dom(h⊥ ) = dom− (h⊥ ) = [[[t]]s,B , eB ([[t]]s,B )).
    As in the previous case, [[r]]s,B = [[rτ ]]s′ ,B ′ holds. Therefore, we have (s′ [y 7→
eB ([[t]]s,B )], h′ , B ′ ) |= (arr(t, y)∗arr(y, t′ k )∗ψ ′ )τ , and then (s′ , h′ , B ′ ) |= ∃y.(arr(t, y)∗
arr(y, t′ k ) ∗ ψ ′ )τ . That means (s′ , h′ , B ′ ) satisfies wpo(ψ, free(t), ok ).


Case 3 We prove the case for ψ = ∗ki=1 Arr(ti , t′ i )αi ∗ ψ ′ and ψpure |= t1 ≈
b(t) ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1
                                   k−1 ′
                                        t i ≈ ti+1 ∗ ∗i=1k−1
                                                             ti < ti+1 for some k, ψ ′ . We
use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for brevity.
    Since ψ = ∗ki=1 Arr(ti , t′ i )αi ∗ ψ ′ , h is of the form h1 ◦ h2 ◦ · · · ◦ hk ◦ h′′ such
that

 – (s, hi , B) |= Arr(ti , t′ i )αi for 1 ≤ i ≤ k,
 – (s, h′′ , B) |= ψ ′ .

(s, B) satisfies t1 ≈ t ≈ b(t) < t′ 1 and e(t) ≈ t′ k , and we have (s, B) |= t′ i ≈ ti+1
for 1 ≤ i < k. Then, h′ can be written as h⊥ ◦h′′ , where dom(h⊥ ) = dom− (h⊥ ) =
[[[t]]s,B , eB ([[t]]s,B )).
      As in the previous case, [[r]]s,B = [[rτ ]]s′ ,B ′ holds. Therefore, we have (s′ [y 7→
eB ([[t]]s,B )], h′ , B ′ ) |= (arr(t, y) ∗ ψ ′ )τ , and then (s′ , h′ , B ′ ) |= ∃y.(arr(t, y) ∗ ψ ′ )τ .
That means (s′ , h′ , B ′ ) satisfies wpo(ψ, free(t), ok ).


Case 4 We prove the case for ψ = arr(t1 , t′ 1 )∗ ∗ki=2 Arr(ti , t′ i )αi ∗ ψ ′ and ψpure |=
t1 < b(t) < t′ 1 ∗ e(t) ≈ t′ k ∗ b(t) ≈ t ∗ ∗i=1    k−1 ′
                                                         t i ≈ ti+1 ∗ ∗i=1 k−1
                                                                               ti < ti+1 for some
    ′
k, ψ . We use τ as an abbreviation for [Tb (π, t) := t][Te (π, t) := y] for brevity.
    Since ψ = arr(t1 , t′ 1 )∗ ∗ki=2 Arr(ti , t′ i )αi ∗ψ ′ , h is of the form h1 ◦h2 ◦· · ·◦hk ◦h′′
such that

 – (s, h1 , B) |= arr(t1 , t′ 1 ),
 – (s, hi , B) |= Arr(ti , t′ i )αi for 2 ≤ i ≤ k,
 – (s, h′′ , B) |= ψ ′ .

Since (s, B) satisfies t1 < t ≈ b(t) < t′ 1 and e(t) ≈ t′ k , hk is divided into two por-
tions h1k and h2k , where h2k is hk whose domain is shorten to [eB ([[t]]s,B ), [[t′ k ]]s,B )
and h1k (l) = ⊥ for l ∈ [[[tk ]]s,B , eB ([[t]]s,B )). Furthermore, we have (s, B) |=
t′ i ≈ ti+1 for 1 ≤ i < k. Then, h′ can be written as h⊥ ◦ h2k ◦ h′′ , where
dom(h⊥ ) = dom− (h⊥ ) = [[[t]]s,B , eB ([[t]]s,B )).
     As in the previous case, [[r]]s,B = [[rτ ]]s′ ,B ′ holds. Therefore, we have (s′ [y 7→
eB ([[t]]s,B )], h′ , B ′ ) |= (arr(t1 , t)∗arr(t, y)∗ψ ′ )τ , and then (s′ , h′ , B ′ ) |= ∃y.(arr(t1 , t)∗
arr(t, y) ∗ ψ ′ )τ . That means (s′ , h′ , B ′ ) satisfies wpo(ψ, free(t), ok ).
40       Y. Lee and K. Nakazawa

Case 5 The following is the union of all cases between Case 1 and Case 4.

                             k
                      ψ = ∗ Arr(ti , t′ i )αi ∗ ψ ′ and
                            i=1
                      ψpure |= t1 ≤ b(t) < t′ 1 ∗ tk < e(t) ≤ t′ k ∗
                                   k−1              k−1
                      b(t) ≈ t ∗ ∗ t′ i ≈ ti+1 ∗ ∗ ti < ti+1
                                   i=1              i=1
                                         ′
                      for some k, ψ

    The following is equivalent to the above since we have that ti < t′ i and
′
t i ≈ ti+1 .

                             k
                      ψ = ∗ Arr(ti , t′ i )αi ∗ ψ ′ and
                            i=1
                      ψpure |= t1 ≤ b(t) < t′ 1 ∗ tk < e(t) ≤ t′ k ∗
                                   k−1
                      b(t) ≈ t ∗ ∗ t′ i ≈ ti+1 for some k, ψ ′
                                   i=1

     The negation of the above formula is as follows:

               k
      If ψ = ∗ Arr(ti , t′ i )αi ∗ ψ ′ and
              i=1
                                                           k−1
      ψpure |= t1 ≤ b(t) < t′ 1 ∗ tk < e(t) ∗ b(t) ≈ t ∗ ∗ t′ i ≈ ti+1
                                                           i=1
      for some k, ψ ′ , then ψpure |= e(t) > t′ k holds.                    · · · (†)

    In this case, we prove WPOJψ, free(t), okK = ∅ by contradiction. That is, we
assume that WPOJψ, free(t), okK 6= ∅ and show that this leads to a contradic-
tion.
    Suppose (s, h, B) |= ψ and ((s, h, B), σ) ∈ Jfree(t)Kok for some σ. By the
definition of Jfree(t)Kok , we have:

                                  JtKs,B = bB (JtKs,B ) > 0.

Since we assume that (s, h, B) is exact, JtKs,B ∈ dom+ (h) holds. ψ contains
Arr(t1 , t′ 1 ) for some t1 , t′ 1 such that ψpure |= t1 ≤ t < t′ 1 ∗ t ≈ b(t).
   Since (s, h, B) is exact,

                            [Jb(t)Ks,B , Je(t)Ks,B ) ⊆ dom+ (h)

holds, and ψ contains Arr(t1 , t′ 1 ) ∗ · · · ∗ Arr(tk , t′ k ) such that ψpure |= e(t) >
tk ∗ ∗i=1
        k−1 ′
           t i ≈ ti+1 for some k.
     Fix k as the maximum among such values of k. Since k is maximal, ψpure |=
t′ k 6≈ u holds for any Arr(u, u′ ) in ψ. Because k is chosen to be maximal, the
          Incorrectness Separation Logic with Arrays and Pointer Arithmetic              41

chain of arrays Arr(t1 , t′1 ), . . . , Arr(tk , t′ k ) cannot be extended by adding another
array at the end.
   If there were an array Arr(u, u′ ) in ψ such that t′ k ≈ u, then this array could
be attached to the end of the chain, creating a longer sequence of arrays.
   However, since k is the maximum possible length, such an extension is not
possible. Therefore, for every array Arr(u, u′ ) in ψ, we must have t′ k 6≈ u. This
means that t′ k does not match the starting point u of any array in ψ. Therefore,
the following holds.
                                        Jt′ k Ks,B ∈/ dom+ (h)
    By (†), we have ψpure |= e(t) > t′ k , which means Je(t)Ks,B > Jt′ k Ks,B . Addi-
tionally, by the condition, we have

                           Jb(t)Ks,B < Jt′ k Ks,B < Je(t)Ks,B .

However, we also have Jt′ k Ks,B ∈   / dom+ (h), which contradicts the property of
exactness: [Jb(t)Ks,B , Je(t)Ks,B ) ⊆ dom+ (h).
   Consequently, we conclude that (s, h, B) is not exact, and thus

                               WPOJψ, free(t), okK = ∅

holds. Please note that in the current setting, for all σ and σ ′ where (σ, σ ′ ) ∈
Jfree(t)Kok , σ and σ ′ are exact.


B.3    Case for er

We consider the case of er and ψpure |= b(t) 6≈ t ∨ b(t) ≈ null. In this case,
we have wpo(ψ, free(t), er) = ψ. By the definition of [[free(t)]]er , we have
(s, h, B) ∈ WPO[[ψ, free(t), er ]] iff (s, h, B) |= ψ and either bB ([[t]]s,B ) 6= [[t]]s,B
or bB ([[t]]s,B ) = 0, which is equivalent to (s, h, B) |= ψ by the assumption ψpure |=
b(t) 6≈ t ∨ b(t) ≈ null.
    Otherwise, both ψpure |= b(t) ≈ t and ψpure |= b(t) 6≈ null hold. Hence,
WPO[[ψ, free(t), er ]] = ∅.


C     Proof of Proposition 1 for x := [t]

We prove (s′ , h′ , B ′ ) |= wpo(ψ, x := [t], ok) ⇐⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, x :=
[t], ok]] holds. By definition, (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := [t], ok]] is equivalent to
∃(s, h, B) |= ψ.bB ([[t]]s,B ) > 0 ∧ (s′ , h′ , B ′ ) = (s[x 7→ h([[t]]s,B )], h, B).


C.1    (s′ , h′ , B ′ ) |= wpo(ψ, x := [t], ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, x :=
       [t], ok]]

Case 1 Here, we prove the case for ψ = ta 7→ u ∗ ψ ′ and ψpure |= ta ≈ t for
some ta , u, and ψ ′ .
   We have the following.
42        Y. Lee and K. Nakazawa



  (s′ , h′ , B ′ ) |= ∃x′ .ψ[x := x′ ] ∗ x ≈ u[x := x′ ]
⇔ ∃v ′ .(s′ [x′ 7→ v ′ ], h′ , B ′ ) |= ψ[x := x′ ] ∗ x ≈ u[x := x′ ]
⇒ ∃v ′ .(s′ [x′ 7→ v ′ ], h′ , B ′ ) |= ψ[x := x′ ] and s′ [x′ 7→ v ′ ](x) = [[u[x := x′ ]]]s′ [x′ 7→v′ ],B ′
⇔ ∃v ′ .(s′ [x′ 7→ v ′ ][x 7→ v ′ ], h′ , B ′ ) |= ψ and s′ [x′ 7→ v ′ ](x) = [[u]]s′ [x′ 7→v′ ][x7→v′ ],B ′
// By Lemma 3
⇔ ∃v ′ .(s′ [x 7→ v ′ ], h′ , B ′ ) |= ψ and s′ (x) = [[u]]s′ [x7→v′ ],B ′
// Since x′ is fresh
⇔ ∃v ′ .(s′ [x 7→ v ′ ], h′ , B ′ ) |= ψ and s′ (x) = h′ ([[t]]s′ [x7→v′ ],B ′ )
// By premise, ψ ⇐⇒ ta ≈ t ∗ ta 7→ u ∗ ψ ′ holds.
// Consequently, [[u]]s′ [x7→v′ ],B ′ = h′ ([[t]]s′ [x7→v′ ],B ′ ) also holds.
  Then, fix v ′ and let s be s′ [x 7→ v ′ ], and then we have (s, h′ , B ′ ) |= ψ. Since
ψ = ta 7→ u ∗ ψ ′ and ψpure |= ta ≈ t hold and (h′ , B ′ ) is exact, bB ′ ([[t]]s,B ′ ) =
bB ′ ([[ta ]]s,B ′ ) > 0 holds. Furthermore, we have s′ (x) = h′ ([[t]]s′ [x7→v′ ],B ′ ) = h′ ([[t]]s,B ′ ),
and hence s′ = s[x 7→ h([[t]]s,B )]. Therefore, we have ((s, h′ , B ′ ), (s′ , h′ , B ′ )) ∈
[[x := [t]]]ok .

Case 2 Here, we prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≤ t < t′ a
for some ta , t′ a , and ψ ′ .
     Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, x := [t], ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, x :=
[t], ok]]. We have the following.


                             (s′ , h′ , B ′ ) |= ∃x′ .ψ[x := x′ ]
                           ⇔ ∃v ′ .(s′ [x′ 7→ v ′ ], h′ , B ′ ) |= ψ[x := x′ ]
                           ⇔ ∃v ′ .(s′ [x′ 7→ v ′ ][x 7→ v ′ ], h′ , B ′ ) |= ψ
                           // By Lemma 3
                           ⇔ ∃v ′ .(s′ [x 7→ v ′ ], h′ , B ′ ) |= ψ
 Then, fix v ′ and let s be s′ [x 7→ v ′ ], and then we have (s, h′ , B ′ ) |= ψ.
Since ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≤ t < t′ a hold and (h′ , B ′ ) is
exact, bB ′ ([[t]]s,B ′ ) = bB ′ ([[ta ]]s,B ′ ) > 0 holds. Furthermore, we have s′ (x) =
h′ ([[t]]s′ [x7→v′ ],B ′ ) = h′ ([[t]]s,B ′ ), and hence s′ = s[x 7→ h([[t]]s,B )]. Therefore, we
have ((s, h′ , B ′ ), (s′ , h′ , B ′ )) ∈ [[x := [t]]]ok .

Case 3 Otherwise, (s′ , h′ , B ′ ) |= wpo(ψ, x := [t], ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, x :=
[t], ok]] holds trivially since wpo(ψ, x := [t], ok) = false.

C.2     (s′ , h′ , B ′ ) ∈ WPO[[ψ, x := [t], ok]] ⇒ (s′ , h′ , B ′ ) |= wpo(ψ, x :=
        [t], ok)
Next, we prove the converse.
           Incorrectness Separation Logic with Arrays and Pointer Arithmetic                      43

Case 1 Here, we prove the case for ψ = ta 7→ u ∗ ψ ′ and ψpure |= ta ≈ t for
some ta , u, and ψ ′ .
   By the assumption, there exists s such that

 – (s, h′ , B ′ ) |= ψ,
 – bB ′ ([[t]]s,B ′ ) > 0, and
 – s′ = s[x 7→ h′ ([[t]]s,B ′ )].

   Since x′ is fresh, they do not depend on the value of s(x′ ), and hence we can
assume s(x′ ) = s(x), and then we have s = s′ [x′ 7→ s(x)][x 7→ s(x)]. Since we
have (s, h′ , B ′ ) |= ψ, we can derive

                             (s, h′ , B ′ ) |= ψ
                           ⇒ (s′ [x′ 7→ s(x)][x 7→ s(x)], h′ , B ′ ) |= ψ
                           ⇒ (s′ [x′ 7→ s(x)], h′ , B ′ ) |= ψ[x := x′ ]

 by Lemma 3 and the fact that s′ [x′ 7→ s(x)](x′ ) = s(x). Let s′′ be s′ [x′ 7→
s(x)]. s′′ (x) = s′ [x′ 7→ s(x)](x) = s′ (x) = h′ ([[t]]s,B ′ ) by the definition. The
equality h′ ([[t]]s,B ′ ) = h′ ([[ta ]]s,B ′ ) holds by (s, h′ , B) |= ψ and ψpure |= t ≈ ta .
h′ ([[ta ]]s,B ′ ) = [[u]]s,B ′ since ψ contains ta 7→ u. Additionally, the following holds.

      [[u]]s,B ′ = [[u]]s′ [x′ 7→s(x)][x7→s(x)],B ′                          // Definition of s
                                ′
                = [[u[x := x ]]]s′ [x′ 7→s(x)],B ′                            // By Lemma 3
                                                         // and s [x 7→ s(x)](x′ ) = s(x)
                                                                     ′   ′

                = [[u[x := x′ ]]]s′′ ,B ′

     Hence, (s′′ , B ′ ) |= x ≈ u[x := x′ ], and (s′′ , h′ , B ′ ) |= ψ[x := x′ ] ∗ x ≈ u[x :=
x ], since s′′ (x) = [[u[x := x′ ]]]s′′ ,B ′ . Then, we have (s′ , h′ , B ′ ) |= ∃x′ .ψ[x :=
 ′

x′ ] ∗ x ≈ u[x := x′ ], which is wpo(ψ, x := [t], ok ).


Case 2 Here, we prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≤ t < t′ a
for some ta , t′ a , and ψ ′ .
    Since x′ is fresh, they do not depend on the value of s(x′ ), and hence we can
assume s(x′ ) = s(x), and then we have s = s′ [x′ 7→ s(x)][x 7→ s(x)]. Since we
have (s, h′ , B ′ ) |= ψ, we can derive

                             (s, h′ , B ′ ) |= ψ
                           ⇒ (s′ [x′ 7→ s(x)][x 7→ s(x)], h′ , B ′ ) |= ψ
                           ⇒ (s′ [x′ 7→ s(x)], h′ , B ′ ) |= ψ[x := x′ ]
                           ⇒ ∃v ′ .(s′ [x′ 7→ v ′ ], h′ , B ′ ) |= ψ[x := x′ ]
                           ⇔ (s′ , h′ , B ′ ) |= ∃x′ .ψ[x := x′ ]

 by Lemma 3 and the fact that s′ [x′ 7→ s(x)](x′ ) = s(x). Then, we have
(s′ , h′ , B ′ ) |= ∃x′ .ψ[x := x′ ], which is wpo(ψ, x := [t], ok ).
44       Y. Lee and K. Nakazawa

Case 3 The following is the union of all cases between Case 1 and Case 2.


                        ψ contains some Arr(ta , t′ a )α such that
                        ψpure |= ta ≤ t < t′ a

     The negation of the above formula is as follows:


                               For any Arr(ta , t′ a )α in ψ,
                               ψpure 6|= ta ≤ t < t′ a

     Suppose that (s, h, B) |= ψ. By the given condition, we have

                                     JtKs,B ∈
                                            / dom+ (h).

Hence, there is no σ such that

                               ((s, h, B), σ) ∈ Jx := [t]Kok .

Therefore, WPOJψ, x := [t], okK = ∅ holds.


C.3     Case for er

Next, we consider the case of er and ψpure |= b(t) ≈ null. In this case, we have
wpo(ψ, x := [t], er) = ψ. By the definition of [[x := [t]]]er , we have (s, h, B) ∈
WPO[[ψ, x := [t], er ]] iff (s, h, B) |= ψ and bB ([[t]]s,B ) = 0, which is equivalent to
(s, h, B) |= ψ by the assumption ψpure |= b(t) ≈ null.
    Otherwise, ψpure |= b(t) 6≈ null hold. Hence, WPO[[ψ, x := t, er ]] = ∅.


D      Proof of Proposition 1 for [t] := t′

We prove (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇐⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t′ , ok]] holds. By definition, (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] := t′ , ok]] is equivalent to
∃(s, h, B) |= ψ.bB ([[t]]s,B ) > 0 ∧ (s′ , h′ , B ′ ) = (s, h[[[t]]s,B 7→ [[t′ ]]s,B ], B).


D.1     (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
        t′ , ok]]

Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t′ , ok]].
            Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                45

Case 1 We prove the case for ψ = ta 7→ − ∗ ψ ′ and ψpure |= ta ≈ t for some ta ,
and ψ ′ .
     By the assumption (s′ , h′ , B ′ ) contains a portion satisfying t 7→ t′ , and hence
 ′
h ([[t]]s′ ,B ′ ) = [[t′ ]]s′ ,B ′ .
     We have the following.

                             (s′ , h′ , B ′ ) |= t 7→ t′ ∗ ψ ′
                        ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= t 7→ − ∗ ψ ′
                        ⇔ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= ta 7→ − ∗ ψ ′
                        // Since ψpure |= ta ≈ t holds

 Fix v ′ and let h be h′ [[[t]]s′ ,B ′ 7→ v ′ ], and then we have (s′ , h, B ′ ) |= ψ. Since
h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ], we have ((s′ , h, B ′ ), (s′ , h′ , B ′ )) ∈ [[[t] := t′ ]]ok .


Case 2 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≈ t for some
ta , t′ a , and ψ ′ .
      Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t , ok]]. By the assumption (s′ , h′ , B ′ ) contains a portion satisfying t 7→ t′ , and
 ′

hence h′ ([[t]]s′ ,B ′ ) = [[t′ ]]s′ ,B ′ .
      We have the following.

               (s′ , h′ , B ′ ) |= t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′
          ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(t, t + 1) ∗ arr(t + 1, t′ a ) ∗ ψ ′
          ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(ta , t′ a ) ∗ ψ ′
          // Appending arrays

 Fix v ′ and let h be h′ [[[t]]s′ ,B ′ 7→ v ′ ], and then we have (s′ , h, B ′ ) |= ψ. Since
h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ], we have ((s′ , h, B ′ ), (s′ , h′ , B ′ )) ∈ [[[t] := t′ ]]ok .


Case 3 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta < t ∗ t + 1 < t′ a
for some ta , t′ a , and ψ ′ .
     Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t , ok]]. By the assumption (s′ , h′ , B ′ ) contains a portion satisfying t 7→ t′ , and
 ′

hence h′ ([[t]]s′ ,B ′ ) = [[t′ ]]s′ ,B ′ .
     We have the following.

     (s′ , h′ , B ′ ) |= arr(ta , t) ∗ t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′
   ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(ta , t) ∗ arr(t, t + 1) ∗ arr(t + 1, t′ a ) ∗ ψ ′
   ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(ta , t′ a ) ∗ ψ ′
   // Appending arrays

 Fix v ′ and let h be h′ [[[t]]s′ ,B ′ 7→ v ′ ], and then we have (s′ , h, B ′ ) |= ψ. Since
h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ], we have ((s′ , h, B ′ ), (s′ , h′ , B ′ )) ∈ [[[t] := t′ ]]ok .
46        Y. Lee and K. Nakazawa

Case 4 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= t + 1 ≈ t′ a for
some ta , t′ a , and ψ ′ .
     Firstly, we prove (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t , ok]]. By the assumption (s′ , h′ , B ′ ) contains a portion satisfying t 7→ t′ , and
 ′

hence h′ ([[t]]s′ ,B ′ ) = [[t′ ]]s′ ,B ′ .
     We have the following.

                  (s′ , h′ , B ′ ) |= arr(ta , t) ∗ t 7→ t′ ∗ ψ ′
              ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(ta , t) ∗ arr(t, t + 1) ∗ ψ ′
              ⇒ ∃v ′ .(s′ , h′ [[[t]]s′ ,B ′ 7→ v ′ ], B ′ ) |= arr(ta , t′ a ) ∗ ψ ′
              // Appending arrays

 Fix v ′ and let h be h′ [[[t]]s′ ,B ′ 7→ v ′ ], and then we have (s′ , h, B ′ ) |= ψ. Since
h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ], we have ((s′ , h, B ′ ), (s′ , h′ , B ′ )) ∈ [[[t] := t′ ]]ok .


Case 5 Otherwise, (s′ , h′ , B ′ ) |= wpo(ψ, [t] := t′ , ok) ⇒ (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] :=
t′ , ok]] holds trivially since wpo(ψ, [t] := t′ , ok) = false.


D.2      (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] := t′ , ok]] ⇒ (s′ , h′ , B ′ ) |= wpo(ψ, [t] :=
         t′ , ok)

Next, we prove the converse: (s′ , h′ , B ′ ) ∈ WPO[[ψ, [t] := t′ , ok]] ⇒ (s′ , h′ , B ′ ) |=
wpo(ψ, [t] := t′ , ok).


Case 1 We prove the case for ψ = ta 7→ − ∗ ψ ′ and ψpure |= ta ≈ t for
some ta , and ψ ′ . By the assumption, there exists h such that (s′ , h, B ′ ) |= ψ,
bB ′ ([[t]]s′ ,B ′ ) > 0, and h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ]. Since ψ = ta 7→ − ∗ ψ ′ and
ψpure |= ta ≈ t, we have [[[ta ]]s′ ,B ′ , [[ta ]]s′ ,B ′ + 1) ⊆ dom+ (h) and [[ta ]]s′ ,B ′ =
[[t]]s′ ,B ′ < [[ta ]]s′ ,B ′ + 1. Then, since (s′ , h, B ′ ) |= ta 7→ − ∗ ψ ′ , we have

                                       (s′ , h′ , B ′ ) |= t 7→ t′ ∗ ψ ′ ,

which is wpo(ψ, [t] := t′ , ok ).


Case 2 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≈ t for some
ta , t′ a , and ψ ′ .
      By the assumption, there exists h such that (s′ , h, B ′ ) |= ψ, bB ′ ([[t]]s′ ,B ′ ) > 0,
and h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ]. Since ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta ≈ t, we
have [[[ta ]]s′ ,B ′ , [[t′ a ]]s′ ,B ′ ) ⊆ dom+ (h) and [[ta ]]s′ ,B ′ = [[t]]s′ ,B ′ < [[t′ a ]]s′ ,B ′ . Then,
since (s′ , h, B ′ ) |= arr(ta , t′ a ) ∗ ψ ′ , we have

                            (s′ , h′ , B ′ ) |= t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′ ,

which is wpo(ψ, [t] := t′ , ok ).
            Incorrectness Separation Logic with Arrays and Pointer Arithmetic                                    47

Case 3 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta < t ∗ t + 1 < t′ a
for some ta , t′ a , and ψ ′ .
      By the assumption, there exists h such that (s′ , h, B ′ ) |= ψ, bB ′ ([[t]]s′ ,B ′ ) > 0,
and h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ]. Since ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= ta < t <
t′ a , we have [[[ta ]]s′ ,B ′ , [[t′ a ]]s′ ,B ′ ) ⊆ dom+ (h) and [[ta ]]s′ ,B ′ < [[t]]s′ ,B ′ < [[t′ a ]]s′ ,B ′ .
Then, since (s′ , h, B ′ ) |= arr(ta , t′ a ) ∗ ψ ′ , we have

                      (s′ , h′ , B ′ ) |= arr(ta , t) ∗ t 7→ t′ ∗ arr(t + 1, t′ a ) ∗ ψ ′ ,

which is wpo(ψ, [t] := t′ , ok ).

Case 4 We prove the case for ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= t + 1 ≈ t′ a for
some ta , t′ a , and ψ ′ .
   By the assumption, there exists h such that (s′ , h, B ′ ) |= ψ, bB ′ ([[t]]s′ ,B ′ ) > 0,
and h′ = h[[[t]]s′ ,B ′ 7→ [[t′ ]]s′ ,B ′ ]. Since ψ = arr(ta , t′ a ) ∗ ψ ′ and ψpure |= t + 1 ≈ t′ a ,
we have [[[ta ]]s′ ,B ′ , [[t′ a ]]s′ ,B ′ ) ⊆ dom+ (h) and [[ta ]]s′ ,B ′ < [[t]]s′ ,B ′ < [[t′ a ]]s′ ,B ′ .
Then, since (s′ , h, B ′ ) |= arr(ta , t′ a ) ∗ ψ ′ , we have

                                 (s′ , h′ , B ′ ) |= arr(ta , t) ∗ t 7→ t′ ∗ ψ ′ ,

which is wpo(ψ, [t] := t′ , ok ).

Case 5 The following is the union of all cases between Case 1 and Case 4.


                             ψ contains some Arr(ta , t′ a )α such that
                             ψpure |= ta ≤ t ∗ t + 1 ≤ t′ a

     The negation of the above formula is as follows:


                                      For any Arr(ta , t′ a )α in ψ,
                                      ψpure 6|= ta ≤ t ∗ t + 1 ≤ t′ a

     Suppose that (s, h, B) |= ψ. By the given condition, we have

                                             JtKs,B ∈
                                                    / dom+ (h).

Hence, there is no σ such that

                                      ((s, h, B), σ) ∈ J[t] := t′ Kok .

Therefore, WPOJψ, [t] := t′ , okK = ∅ holds.

D.3      Case for er
The case for er is proven in a similar way to the case of x := [t].
