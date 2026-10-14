        Concise Read-Only Speciﬁcations for
     Better Synthesis of Programs with Pointers
                                       
Andreea Costea1 , Amy Zhu2                 , Nadia Polikarpova3 , and Ilya Sergey4,1
         1
             School of Computing, National University of Singapore, Singapore
                 2
                    University of British Columbia, Vancouver, Canada
                       3
                         University of California, San Diego, USA
                             4
                               Yale-NUS College, Singapore
        Abstract. In program synthesis there is a well-known trade-oﬀ between
        concise and strong speciﬁcations: if a speciﬁcation is too verbose, it might
        be harder to write than the program; if it is too weak, the synthesised
        program might not match the user’s intent. In this work we explore the
        use of annotations for restricting memory access permissions in program
        synthesis, and show that they can make speciﬁcations much stronger
        while remaining surprisingly concise. Speciﬁcally, we enhance Synthetic
        Separation Logic (SSL), a framework for synthesis of heap-manipulating
        programs, with the logical mechanism of read-only borrows.
        We observe that this minimalistic and conservative SSL extension bene-
        ﬁts the synthesis in several ways, making it more (a) expressive (stronger
        correctness guarantees are achieved with a modest annotation overhead),
        (b) eﬀective (it produces more concise and easier-to-read programs),
        (c) eﬃcient (faster synthesis), and (d) robust (synthesis eﬃciency is
        less aﬀected by the choice of the search heuristic). We explain the in-
        tuition and provide formal treatment for read-only borrows. We sub-
        stantiate the claims (a)–(d) by describing our quantitative evaluation of
        the borrowing-aware synthesis implementation on a series of standard
        benchmark speciﬁcations for various heap-manipulating programs.

1     Introduction
Deductive program synthesis is a prominent approach to the generation of correct-
by-construction programs from their declarative speciﬁcations [14, 23, 29, 33].
With this methodology, one can represent searching for a program satisfying the
user-provided constraints as a proof search in a certain logic. Following this idea,
it has been recently observed [34] that the synthesis of correct-by-construction
imperative heap-manipulating programs (in a language similar to C) can be im-
plemented as a proof search in a version of Separation Logic (SL)—a program
logic designed for modular veriﬁcation of programs with pointers [32, 37].
   SL-based deductive program synthesis based on Synthetic Separation Logic
(SSL) [34] requires the programmer to provide a Hoare-style speciﬁcation for a
program of interest. For instance, given the predicate ls(x, S), which denotes a
symbolic heap corresponding to a linked list starting at a pointer x, ending with
null, and containing elements from the set S, one can specify the behaviour of
the procedure for copying a linked list as follows:
              {r → x ∗ ls(x, S)} listcopy(r) {r → y ∗ ls(x, S) ∗ ls(y, S)}           (1)

    Work done during an internship at NUS School of Computing in Summer 2019.

c The Author(s) 2020
P. Müller (Ed.): ESOP 2020, LNCS 12075, pp. 141–168, 2020.
https://doi.org/10.1007/978-3-030-44914-8_ 6
142     A. Costea et al.



                                                               ls(nxt, S′)
                                                                                     




                                                                                     
             content   x       v   nxt       v′ nxt′             ⁄           w   null
            address    r       x   x+1       nxt   nxt + 1

                                                    ls(x, S)

   The precondition of speciﬁcation (1), deﬁning the shape of the initial heap,
is illustrated by the ﬁgure above. It requires the heap to contain a pointer r,
which is taken by the procedure as an argument and whose stored value, x, is the
head pointer of the list to be copied. The list itself is described by the symbolic
heap predicate instance ls(x, S), whose footprint is assumed to be disjoint from
the entry r → x, following the standard semantics of the separating conjunction
operator (∗) [32]. The postcondition asserts that the ﬁnal heap, in addition to
containing the original list ls(x, S), will contain a new list starting from y whose
contents S are the same as of the original list, and also that the pointer r will now
point to the head y of the list copy. Our speciﬁcation is incomplete: it allows, for
example, duplicating or rearranging elements. One hopes that such a program
is unlikely to be synthesised. In synthesis, it is common to provide incomplete
specs: writing complete ones can be as hard as writing the program itself.

1.1   Correct Programs that Do Strange Things
Provided the deﬁnition of the heap predi-        1 void listcopy (loc r) {
cate ls and the speciﬁcation (1), the SuS-       2   let x = *r;
Lik tool, an implementation of the SSL-          3   if (x == 0) {
based synthesis [34], will produce the pro-      4   } else {
                                                 5     let v = *x;
gram depicted in Fig. 1. It is easy to check     6     let nxt = *(x + 1);
that this program satisﬁes the ascribed          7     *r = nxt;
spec (1). Moreover, it correctly duplicates      8     listcopy(r);
the original list, faithfully preserving its     9     let y1 = *r;
contents and the ordering. However, an 10              let y = malloc(2);
                                                11     *(x + 1) = y1;
astute reader might notice a certain odd- 12           *r = y;
ity in the way it treats the initial list pro- 13      *(y + 1) = nxt;
vided for copying. According to the post- 14           *y = v;
condition of (1), the value of the pointer 15        } }
r stored in a local immutable variable y1            
                                                                  ls(x, S)
                                                                                  
on line 9 is the head of the copy of the
                                                  y    v y1            v′ ⁄        ⁄
original list’s tail. Quite unexpectedly, the
                                                  r    x  x+1          nxt nxt + 1
pointer y1 becomes the tail of the original
list on line 11, while the original list’s tail        v nxt           v′ ⁄        ⁄

                                                                                         
pointer nxt, once assigned to *(y + 1) on              y  y+1          y1  y1 + 1
line 13, becomes the tail of the copy!                            ls(y, S)
   Indeed, the exercise in tail swapping is Fig. 1: Result program for spec (1)
totally pointless: not only does it produces and the shape of its ﬁnal heap.
less “natural” and readable code, but the
resulting program’s locality properties are unsatisfactory; for instance, this pro-
                        Concise Read-Only Speciﬁcations for Better Synthesis      143


gram cannot be plugged into a concurrent setting where multiple threads rely
on ls(x, S) to be unchanged.
   The issue with the result in Fig. 1 is caused by speciﬁcation (1) being too
permissive: it does not prevent the synthesised program from modifying the
structure of the initial list, while creating its copy. Luckily, the SL community has
devised a number of SL extensions that allow one to impose such restrictions, like
declaring a part of the provided symbolic heap as read-only [5, 8, 9, 11, 15, 20, 21],
i.e., forbidden to modify by the speciﬁed code.

1.2    Towards Simple Read-Only Speciﬁcations for Synthesis
The main challenge of introducing read-only annotations (commonly also re-
ferred to as permissions)5 into Separation Logic lies in establishing the disci-
pline for performing sound accounting in the presence of mixed read-only and
mutating heap accesses by diﬀerent components ofa program. 
   As an example, consider a simple symbolic heap x → f ∗ r → h that declares
                                                     M        M



two mutable (i.e., allowed to be written to) pointers x and r, that point to
unspeciﬁed values f and h, correspondingly. With this symbolic heap, is it safe
to call the following function that modiﬁes the contents of r but not of x?
                                                                       
                        RO       M                         RO      M
                      x → f ∗ r → h    readX(x, r)    x → f ∗ r → f            (2)

 The precondition of readX requires a weaker form of access permission for x
(read-only, RO), while the considered heap asserts a stronger write permission
(M). It should be possible to satisfy readX’s requirement by providing the nec-
essary read-only permission for x. To do so, we need to agree on a discipline to
“adapt” the caller’s write-permission M to the callee’s read-only permission RO.
While seemingly trivial, if implemented naı̈vely, accounting of RO permissions in
SL might compromise either soundness or completeness of the logical reasoning.
   A number of proposals for logically sound interplay between write- and read-
only access permissions in the presence of function calls has been described in
the literature [7–9, 11, 13, 20, 30]. Some of these works manage to maintain the
simplicity of having only mutable/read-only annotations when conﬁned to the
sequential setting [9,11,13]. More general (but harder to implement) approaches
rely on fractional permissions [8,25], an expressive mechanism for permission ac-
counting, with primary applications in concurrent reasoning [7, 28]. We started
this project by attempting to adapt some of those logics [9,11,13] as an extension
of SSL in order to reap the beneﬁts of read-only annotations for the synthesis
of sequential program. The main obstacle we encountered involved deﬁnitions
of inductive heap predicates with mixed permissions. For instance, how can one
specify a program that modiﬁes the contents of a linked list, but not its struc-
ture? Even though it seemed possible to enable this treatment of predicates via
permission multiplication [25], developing support for this machinery on top of
existing SuSLik infrastructure was a daunting task. Therefore, we had to look
for a technically simpler solution.

5
    We will be using the words “annotation” and “permission” interchangeably.
144      A. Costea et al.


1.3    Our Contributions
Theoretical Contributions. Our main conceptual innovation is the idea of in-
strumenting SSL with symbolic read-only borrows to enable faster and more
predictable program synthesis. Borrows are used to annotate symbolic heaps
in speciﬁcations, similarly to abstract fractional permissions from the deductive
veriﬁcation tools, such as Chalice and VeriFast [20,21,27]. They enable simple
but principled lightweight threading of heap access permissions from the callers
to callees and back, while enforcing read-only access whenever it is required. For
basic intuition on read-only borrows, consider the speciﬁcation below:
                                                                                      
            a       b        M                             a       b       M
         x → f ∗ y → g ∗ r → h    readXY(x, y, r)    x → f ∗ y → g ∗ r → (f + g)       (3)
 The precondition requires a heap with three pointers, x, y, and r, pointing to
unspeciﬁed f, g, and h, correspondingly. Both x and y are going to be treated as
read-only, but now, instead of simply annotating them with RO, we add symbolic
borrowing annotations a and b. The semantics of these borrowing annotations
is the same as that of other ghost variables (such as f). In particular, the callee
must behave correctly for any valuation of a and b, which leaves it no choice
but to treat the corresponding heap fragments as read-only (hence preventing
the heap fragments from being written). On the other hand, from the perspec-
tive of the caller, they serve as formal parameters that are substituted with
actuals
       of caller’s choosing: for instance, when invoked with a caller’s symbolic
heap x → 1 ∗ y → 2 ∗ r → 0 (where c denotes a read-only borrow of the caller),
          M        c      M



readXY is guaranteed to “restore” the same access permissions in the postcondi-
tion, as per the substitution [M/a, c/b]. The example above demonstrates that
read-only borrows are straightforward to compose when reasoning about code
with function calls. They also make it possible to deﬁne borrow-polymorphic
inductive heap predicates, e.g., enhancing ls from spec (1) so it can be used in
speciﬁcations with mixed access permissions on their components.6 Finally, read-
only borrows make it almost trivial to adapt the existing SSL-based synthesis
to work with read-only access permissions; they reduce the complex permission
accounting to easy-to-implement permission substitution.
Practical Contributions. Our ﬁrst practical contribution is ROBoSuSLik—an
enhancement of the SuSLik synthesis tool [34] with support for read-only bor-
rows, which required us to modify less than 100 lines of the original code.
   Our second practical contribution is the extensive evaluation of synthesis with
read-only permissions, on a standard benchmark suite of speciﬁcations for heap-
manipulating programs. We compare the behaviour, performance, and the out-
comes of the synthesis when run with the standard (“all-mutable”) speciﬁcations
and their analogues instrumented with read-only permissions wherever reason-
able. By doing so, we substantiate the following claims regarding the practical
impact of using read-only borrows in SSL speciﬁcations:
– First, we show that synthesis of read-only speciﬁcations is more eﬃcient: it
  does less backtracking while searching for a program that satisﬁes the imposed
  constraints, entailing better performance.
6
    We will present borrow-polymorphic inductive heap predicates in Sec. 2.4.
                        Concise Read-Only Speciﬁcations for Better Synthesis      145


– Second, we demonstrate that borrowing-aware synthesis is more eﬀective:
  speciﬁcations with read-only annotations lead to more concise and human-
  readable programs, which do not perform redundant operations.
– Third, we observe that read-only borrows increase expressivity of the synthe-
  sis: in most of the cases enhanced speciﬁcations provide stronger correctness
  guarantees for the results, at almost no additional annotation overhead.
– Finally, we show that read-only borrows make the synthesis more robust: its
  results and performance are less likely to be aﬀected by the uniﬁcation order
  or the order of the attempted rule applications during the search.

Paper Outline. We start by showcasing the intricacies and the virtues of SSL-
based synthesis with read-only speciﬁcations in Sec. 2. We provide the formal
account of read-only borrows and present the modiﬁed SSL rules, along with
the soundness argument in Sec. 3. We report on the implementation and evalu-
ation of the enhanced synthesis in Sec. 4. We conclude with a discussion on the
limitations of read-only borrows in Sec. 5 and compare to related work in Sec. 6.

2     Program Synthesis with Read-Only Borrows
We introduce the enhancement of SSL with read-only borrows by walking the
reader through a series of small but characteristic examples of deductive syn-
thesis with separation logic. We provide the necessary background on SSL in
Sec. 2.1; the readers familiar with the logic may want to skip to Sec. 2.2.
2.1    Basics of SSL-based Deductive Program Synthesis
In a deductive Separation Logic-based synthesis, a client provides a speciﬁca-
tion of a function of interest as a pair of pre- and post-conditions, such as
{P} void foo(loc x, int i) {Q}. The precondition P constrains the symbolic
state necessary to run the function safely (i.e., without crashes), while the post-
condition Q constrains the resulting state at the end of the function’s execution.
A function body c satisfying the provided speciﬁcation is obtained as a result of
deriving the SSL statement, representing the synthesis goal :
                                {x, i} ; {P} ; {Q}| c
   In the statement above, x and i are program variables, and they are explicitly
stated in the environment Γ = {x, i}. Variables that appear in {P} and that are
not program variables are called (logical) ghost variables, while the non-program
variables that only appear in {Q} are referred to as (logical) existential ones (EV).
The meaning of the statement Γ ; {P} ; {Q}| c is the validity of the Hoare-style
triple {P} c {Q} for all possible values of variables from Γ .7 Both pre- and
postcondition contain a spatial part describing the shape of the symbolic state
(spatial formulae are ranged over via P, Q, and R), and a pure part (ranged over
via φ, ψ, and ξ), which states the relations between variables (both program
and logical). A derivation of an SSL statement is conducted by applying logical
7
    We often care only about the existence of a program c to be synthesised, not its
    speciﬁc shape. In those cases we will be using a shorter statement: Γ ; {P} ; {Q}.
146      A. Costea et al.


rules, which reduce the initial goal to a trivial one, so it can be solved by one of
the terminal rules, such as, e.g., the rule Emp shown below:
                                                φ⇒ψ
                             Emp
                                    Γ ; {φ; emp} ; {ψ; emp}| skip
That is, Emp requires that (i) symbolic heaps in both pre- and post-conditions
are empty and (ii) that the pure part φ of the precondition implies the pure
part ψ of the postcondition. As the result, Emp “emits” a trivial program skip.
Some of the SSL rules are aimed at simplifying the goal, bringing it to the shape
that can be solved with Emp. For instance, consider the following rules:
      Frame                                     UnifyHeaps
      EV (Γ, P, Q) ∩ Vars (R) = ∅               [σ]R = R       ∅ = dom (σ)
                                                                           ⊆ EV (Γ, P, Q)
         Γ ; {φ; P} ; {ψ; Q}| c                       Γ ; {φ; P ∗ R} ; [σ] ψ; Q ∗ R  c
                                                                                 
      Γ ; {φ; P ∗ R} ; {ψ; Q ∗ R}| c                   Γ ; {φ; P ∗ R} ; ψ; Q ∗ R  c

   Neither of the rules Frame and UnifyHeaps “adds” to the program c being
synthesised. However, Frame reduces the goal by removing a matching part R
(a.k.a. frame) from both the pre- and the post-condition. UnifyHeaps non-
deterministically picks a substitution σ, which replaces existential variables in a
sub-heap R of the postcondition to match the corresponding symbolic heap R in
the precondition. Both of these rules make choices with regard to what frame R
to remove or which substitution σ to adopt—a point that will be of importance
for the development described in Sec. 2.2.
   Finally, the following (simpliﬁed) rule for producing a write command is oper-
ational, as it emits a part of the program to be synthesised, while also modifying
the goal accordingly. The resulting program will, thus, consist of the emitted
store ∗x = e of an expression e to the pointer variable x. The remainder is syn-
thesised by solving the sub-goal produced by applying the Write rule.
                 Vars (e) ⊆ Γ          e = eΓ ; {φ; x → e ∗ P} ; {ψ; x → e ∗ Q}| c
        Write                                                 
                            Γ; φ; x → e ∗ P ; {ψ; x → e ∗ Q} ∗x = e; c
                                            


   As it is common with proof search, should no rule apply to an intermediate
goal within one of the derivations, the deductive synthesis back-tracks, possibly
discarding a partially synthesised program fragment, trying alternative deriva-
tion branches. For instance, ﬁring UnifyHeaps to unify wrong sub-heaps might
lead the search down a path to an unsatisﬁable goal, eventually making the
synthesis back-track and leading to longer search. Consider also a misguided
application of Write into a certain location, which can cause the synthesizer to
generate a less intuitive program that “makes up” for the earlier spurious writes.
This is precisely what we are going to ﬁx by introducing read-only annotations.
2.2     Reducing Non-Determinism with Read-Only Annotations
Consider the following example adapted from the original SSL paper [34]. While
the example is intentionally artiﬁcial, it captures a frequent synthesis scenario—
non-determinism during synthesis. This speciﬁcation allows a certain degree of
freedom in how it can be satisﬁed:
                                Concise Read-Only Speciﬁcations for Better Synthesis        147


         {x → 239 ∗ y → 30} void pick(loc x, loc y) {z ≤ 100; x → z ∗ y → z}            (4)
 It seems logical for the synthesis to start the program derivation by applying
the rule UnifyHeaps, thus reducing the initial goal to the one of the form
                {x, y} ; {x → 239 ∗ y → 30} ; {239 ≤ 100; x → 239 ∗ y → 239}
 This new goal has been obtained by picking one particular substitution σ =
[239/z] (out of multiple possible ones), which delivers two identical heaplets of the
form x → 239 in pre- and postcondition. It is time for the Write rule to strike to
ﬁx the discrepancy between the symbolic heap in the pre- and postcondition by
emitting the command ∗y = 239 (at last, some executable code!), and resulting in
the following new goal (notice the change of y-related entry in the precondition):
             {x, y} ; {x → 239 ∗ y → 239} ; {239 ≤ 100; x → 239 ∗ y → 239}
 What follows are two applications of the Frame rule to the common symbolic
heaps, leading to the goal: {x, y} {emp} ; {239 ≤ 100; emp}. At this point, we
are clearly in trouble. The pure part of the precondition is simply true, while the
postcondition’s pure part is 239 ≤ 100, which is unsolvable.
   Turns out that our initial pick of the substitution σ = [239/z] was an unfor-
tunate one, and we should discard the series of rule applications that followed
it, back-track and adopt a diﬀerent substitution, e.g., σ  = [30/z], which will
indeed result in solving our initial goal.8
   Let us now consider the same speciﬁcation for pick that has been enhanced
by explicitly
             annotating parts of the symbolic heap as mutable and read-only:
                                                                           
            M          RO                                                     M     RO
         x → 239 ∗ y → 30        void pick(loc x, loc y)      z ≤ 100; x → z ∗ y → z    (5)
 In this version of SSL, the eﬀect of rules such as Emp, Frame, and UnifyHeaps
remains the same, while operational rules such as Write, become annotation-
aware. Speciﬁcally, the rule Write is now replaced by the following one:
                                                                                  
                                                                                      
                                        e = e
                                                              M               M
                   Vars (e) ⊆ Γ                     Γ ; φ; x → e ∗ P ; ψ; x → e ∗ Q  c
      WriteRO                                                     
                                                                      
                                  Γ; φ; x → e ∗ P ; ψ; x → e ∗ Q  ∗x = e; c
                                           M                  M



   Notice how in the rule above the heaplets of the form x → e are now anno-
                                                                          M


tated with the access permission M, which explicitly indicates that the code may
modify the corresponding heap location.
   Following with the example speciﬁcation (5), we can imagine a similar scenario
when the rule UnifyHeaps picks the substitution σ = [239/z]. Should this be
the case, the next application of the rule WriteRO will not be possible, due to
                                           y → 239 in the resulting sub-goal:
                                              RO
the read-only annotation
                 
                          on the heaplet
                                                                     
                            M           RO                      M          RO
             {x, y} ; x → 239 ∗ y → 30         ;   z ≤ 100; x → 239 ∗ y → 239
 As the RO access permission prevents the synthesised code from modifying the
greyed heaplets, the synthesis search is forced to back-track, picking an alterna-
tive substitution σ  =[30/z] and converging on the desirable program ∗x=30.
8
    One might argue that it was possible to detect the unsolvable conjunct 239 ≤ 100 in
    the postcondition immediately after performing substitution, thus sparing the need
    to proceed with this derivation further. This is, indeed, a possibility, but in general
    it is hard to argue which of the heuristics in applying the rules will work better in
    general. We defer the quantitative argument on this matter until Sec. 4.4.
148     A. Costea et al.


2.3   Composing Read-Only Borrows
Having synthesised the pick function from speciﬁcation (5), we would like to
use it in future programs. For example, imagine that at some point, while syn-
thesising another program, we see the following as an intermediate goal:
                                                                        
                        M          M                      M        M
            {u, v} ; u → 239 ∗ v → 30 ∗ P ; w ≤ 200; u → w ∗ v → w ∗ Q         (6)
 It is clear that, modulo the names of the variables, we can synthesise a part of
the desired program by emitting a call pick(u, v), which we can then reduce to
the goal {u, v} {P} ; {w ≤ 200; Q} via an application of Frame.
   Why is emitting such a call to pick() safe? Intuitively, this can be done because
the precondition of the spec (5) is weaker than the one in the goal (6). Indeed, the
precondition of the latter provides the full (mutable) access permission on the
heap portion v → 30, while the pre/postcondition of former requires a weaker
                   M


form of access, namely read-only: y → 30. Therefore, our logical foundations
                                         RO


should allow temporary “downgrading” of an access permission, e.g., from M to
RO, for the sake of synthesising calls. While allowing this is straightforward and
can be done similarly to up-casting a type in languages like Java, what turns out
to be less trivial is making sure that the caller’s initial stronger access permission
(M) is restored once pick(u, v) returns.
Non-solutions. Perhaps, the simplest way to allow the call to a function with a
weaker (in terms of access permissions) speciﬁcation, would be to (a) downgrade
the caller’s permissions on the corresponding heap fragments to RO, and (b)
recover the permissions as per the callee’s speciﬁcation. This approach signif-
icantly reduces the expressivity of the logic (and, as a consequence, complete-
ness of the synthesis). For instance, adopting this strategy for using speciﬁca-
tion (5) in the goal (6) would  result in the unsolvable
                                                                sub-goal of the form
            M         RO            M         M
{u, v} ; u → 30 ∗ v → 30 ∗ P ; u → 30 ∗ v → 30 ∗ Q . This is due to the fact that
the postcondition requires the heaplet v → 30 to have the write-permission M,
                                              M


while the new precondition only provides the RO-access.
   Another way to cater for a weaker callee’s speciﬁcation would be to “chip
out” a RO-permission from a caller’s M-annotation (in the spirit of fractional
permissions), oﬀer it to the callee, and then “merge” it back to the caller’s full-
blown permission upon return. This solution works for simple examples, but not
for heap predicates with mixed permissions (discussion in Sec. 6). Yet another
approach would be to create a “RO clone” of the caller’s M-annotation, introduc-
ing an axiom of the form x → t  x → t ∗ x → t. The created component x → t
                             M         M       RO                              RO


could be provided to the callee and discarded upon return since the caller re-
tained the full permission of the original heap. Several works on RO permissions
have adopted this approach [9, 11, 13]. While discarding such clones works just
ﬁne for sequential program veriﬁcation, in the case of synthesis guided by pre-
and postconditions, incomplete postconditions could lead to intractable goals.
Our solution. The key to gaining the necessary expressivity wrt. passing/return-
ing access permissions, while maintaining a sound yet simple logic, is treating
access permissions as ﬁrst-class values. A natural consequence of this treatment
is that immutability annotations can be symbolic (i.e., variables of a special sort
                            Concise Read-Only Speciﬁcations for Better Synthesis             149


“permission”), and the semantics of such variables is well understood; we refer to
these symbolic annotations as read-only borrows.9 For instance, using borrows,
we can represent the speciﬁcation (5) as an equivalent one:
                                                                                      
            M           a                                                    M       a
          x → 239 ∗ y → 30       void pick(loc x, loc y)       z ≤ 100; x → z ∗ y → z    (7)

 The only substantial diﬀerence with spec (5) is that now the pointer y’s access
permission is given an explicit name a. Such named annotations (a.k.a. borrows)
are treated as RO by the callee, as long as the pure precondition does not con-
strain them to be mutable. However, giving these permissions names achieves
an important goal: performing accurate accounting while composing speciﬁca-
tions with diﬀerent access permissions. Speciﬁcally, we can now emit a call to
pick(u, v) as speciﬁed by (7) from the goal (6), keeping in mind the substitution
σ = [u/x, v/y, M/a]. This call now accounts for borrows as well, and makes it
straightforward to restore v’s original permission M upon returning.
   Following the same idea, borrows can be naturally composed through capture-
avoiding substitutions. For instance, the same speciﬁcation (7) of pick could be
used to advance the following modiﬁed version of the goal (6):
                                                                            
                            M          c                      M        c
                {u, v} ; u → 239 ∗ v → 30 ∗ P ; w ≤ 210; u → w ∗ v → w ∗ Q

by means of taking the substitution σ  = [u/x, v/y, c/a].
2.4     Borrow-Polymorphic Inductive Predicates
Separation Logic owes its glory to the extensive use of inductive heap predicates—
a compact way to capture the shape and the properties of ﬁnite heap fragments
corresponding to recursive linked data structures. Below we provide one of the
most widely-used SL predicates, deﬁning the shape of a heap containing a null-
terminated singly-linked list with elements from a set S:
      ls(x, S)  x = 0 ∧ {S = ∅; emp}
                                                                                             (8)
               | x =0 ∧ {S = {v} ∪ S1 ; [x, 2] ∗ x → v ∗ x, 1 → nxt ∗ ls(nxt, S1 )}
  The predicate contains two clauses describing the corresponding cases of the
list’s shape depending on the value of the head pointer x. If x is zero, the list’s
heap representation is empty, and so is the set of elements S. Alternatively, if x
is not zero, it stores a record with two items (indicated by the block assertion
[x, 2]), such that the payload pointer x contains the value v (where S = {v} ∪ S1
for some set S1 ), and the pointer, corresponding to x + 1 (denoted as x, 1 )
contains the address of the list’s tail, nxt.
   While expressive enough to specify and enable synthesis of various list-traversing
and list-generating recursive functions via SSL, the deﬁnition (8) does not allow
one to restrict the access permissions to diﬀerent components of the list: all of
the involved memory locations can be mutated (which explains the synthesis
issue we described in Sec. 1.1). To remedy this weakness of the traditional SL-
style predicates, we propose to parameterise them with read-only borrows, thus
making them aware of diﬀerent access permissions to their various components.
For instance, we propose to redeﬁne the linked list predicate as follows:
9
    In this regard, our symbolic borrows are very similar to abstract fractional permis-
    sions in Chalice and VeriFast [21, 27]. We discuss the relation in detail in Sec. 6.
150        A. Costea et al.


      ls(x, S, a, b, c) x = 0 ∧ {S = ∅; emp}                                                     
                                                      b                c                                       (9)
          | x = 0 ∧ S = {v} ∪ S1 ; [x, 2]a ∗ x → v ∗ x, 1 → nxt ∗ ls(nxt, S1 , a, b, c)
   The new deﬁnition (9) is similar to the old one (8), but now, in addition to
the standard predicate parameters (i.e., the head pointer x and the set S in this
case), also features three borrow parameters a, b, and c that stand as place-
holders for the access permissions to some particular components of the list.
Speciﬁcally, the symbolic borrows b and c control the permissions to manipulate
the pointers x and x + 1, correspondingly. The borrow a, modifying a block-
type heaplet, determines whether the record starting at x can be deallocated
with free(x). All the three borrows are passed in the same conﬁguration to the
recursive instance of the predicate, thereby imposing the same constraints on
the rest of the corresponding list components.
   Let us see the borrow-polymorphic inductive predicates in action. Consider
the following speciﬁcation that asks for a function taking a list of arbitrary values
and replacing all of them with zeroes:10
                    {ls(x, S, d, M, e)} void reset(loc x) {ls(x, O, d, M, e)}                              (10)
 The spec (10) gives very little freedom to the function that would satisfy it
with regard to permissions to manipulate the contents of the heap, constrained
by the predicate ls(x, S, d, M, e). As the ﬁrst and the third borrow parameters are
instantiated with read-only borrows (d and e), the desired function is not going
to be able to change the structural pointers or deallocate parts of the list. The
only allowed manipulation is, thus, changing the values of the payload pointers.
   This concise speciﬁcation is pleasantly strong. To wit, in plain SSL, a similar
spec (without read-only annotations) would also admit an implementation that
fully deallocates the list or arbitrarily changes its length. In order to avoid these
outcomes, one would, therefore, need to provide an alternative deﬁnition of the
predicate ls, which would incorporate the length property too.
   Imagine now that one would like to use the implementation of reset satisfy-
ing speciﬁcation (10) to generate a function with the following spec, providing
stronger access permissions for the list components:
              {ls(y, S, M, M, M)} void call_reset(loc y) {ls(y, O, M, M, M)}
   During the synthesis of call reset, a call to reset is generated. For this
purpose the access permissions are borrowed and recovered as per spec (10) via
the substitution [y/x, M/d, M/e] in a way described in Sec. 2.3.
2.5       Putting It All Together
We conclude this overview by explaining how synthesis via SSL enhanced with
read-only borrows avoids the issue with spurious writes outlined in Sec. 1.1.
   To begin, we change the speciﬁcation to the following one, which makes use
of the new list predicate (9) and prevents any modiﬁcations in the original list.
                                                                                                        
          M                                                 M
       r → x ∗ ls(x, S, a, b, c)       listcopy(r)       r → y ∗ ls(x, S, a, b, c) ∗ ls(y, S, M, M, M)
 We should remark that, contrary to the solution sketched at the end of Sec. 1.1,
which suggested using the predicate instance of the shape ls(x, S)[RO], our con-
crete proposal does not allow us to constrain the entire predicate with a single
10
     We use O as a notation for a multi-set with an arbitrary ﬁnite number of zeroes.
                            Concise Read-Only Speciﬁcations for Better Synthesis                 151



    Variable    x, y Alpha-numeric identiﬁers
    Size, oﬀset n, ι Non-negative integers
    Expressione ::= 0 | true | x | e = e | e ∧ e | ¬e
    Command c ::= let x = ∗(x + ι) | ∗(x + ι) = e | let x = malloc(n) | free(x)
                     | err | f (ei ) | c; c | if (e) {c} else {c}
    Fun. dict. Δ ::=  | Δ, f (xi ) { c }
                         Fig. 2: Programming language grammar.

Pure term      φ, ψ, χ, α ::= 0 | true | M | RO | x | φ = φ | φ ∧ φ | ¬φ
                                             α
Symbolic heap P, Q, R     ::= emp | e, ι → e | [e, ι]α | p(φi ) | P ∗ Q
Heap predicate D          ::= p(xi ) ek , {χk , Rk }
Function spec F           ::= f(xi ) : {P}{Q} Assertion P, Q ::= {φ; P}
Environment Γ              :=  | Γ, x                Context Σ           :=  | Σ, D | Σ, F
                               Fig. 3: BoSSL assertion syntax.
access permission (e.g., RO). Instead, we allow ﬁne-grained access control to
its particular elementary components by annotating each one with an individ-
ual borrow. The speciﬁcation above allows the greatest ﬂexibility wrt. access
permissions to the original list by giving them diﬀerent names (a, b, c).
   In the process of synthesising the non-trivial branch of listcopy, the search
at some point will come up with the following intermediate goal:
    {x, r, nxt, v, y12} ;
                                                                                                
                          M                  b              c
      S = {v} ∪ S1 ; r → y12 ∗ [x, 2]a ∗ x → v ∗ x, 1 → nxt ∗ ls(y12, S1 , M, M, M) ∗ . . .
                                                                            
                         M             M
    ;       [z, 2]M ∗ z → v ∗ z, 1 → y12 ∗ ls(y12, S1 , M, M, M) ∗ . . .
 Since the logical variable z in the postcondition is an existential one, the greyed
part of the symbolic heap can be satisﬁed by either (a) re-purposing the greyed
part of the precondition (which is what the implementation in Sec. 1.1 does), or
(b) allocating a corresponding record of two elements (as should be done). With
the read-only borrows in place, the uniﬁcation of the two greyed fragments in the
pre- and postcondition via UnifyHeaps fails, because the mutable annotation
of z → v in the post cannot be matched by the read-only borrow x → v in the
      M                                                                   b


precondition. Therefore, not being able to follow the derivation path (a), the
synthesiser is forced to explore an alternative one, eventually deriving the version
of listcopy without tail-swapping.

3      BoSSL: Borrowing Synthetic Separation Logic
We now give a formal presentation of BoSSL—a version of SSL extended with
read-only borrows. Fig. 2 and Fig. 3 present its programming and assertion lan-
guage, respectively. For simplicity, we formalise a core language without theories
(e.g., natural numbers), similar to the one of Smallfoot [6]; the only sorts in
the core language are locations, booleans, and permissions (where permissions
appear only in speciﬁcations) and the pure logic only has equality. In contrast,
our implementation supports integers and sets (where the latter also only ap-
pear in speciﬁcations), with linear arithmetic and standard set operations. We do
152      A. Costea et al.



       Write                                                                
                                                                                
                         e = e
                                                   M                    M
       Vars (e) ⊆ Γ                  Γ; φ; x, ι → e ∗ P ; ψ; x, ι → e ∗ Q  c
                                                        
                                                            
              Γ; φ; x, ι → e ∗ P ; ψ; x, ι → e ∗ Q  ∗ (x + ι) = e; c
                            M                        M



Alloc
R= [z, n]α ∗   ∗   0≤i<n
                                      α
                               z, i →i ei         ({y} ∪ {ti }) ∩ Vars (Γ, P, Q) =∅   z∈EV (Γ, P, Q)
                                                                              
                                                                                            
           
          R  [y, n] ∗     M
                                 ∗   0≤i<n
                                                       M
                                               y, i → ti      Σ; Γ; φ; P ∗ R ; {ψ; Q ∗ R} c
                                Σ; Γ; {φ; P} ; {ψ; Q ∗ R}| let y = malloc(n); c
 Free
 R = [x, n]M ∗   ∗   0≤i<n
                                          M
                                 x, i → ei         Vars ({x} ∪ {ei }) ⊆ Γ   Σ; Γ; {φ; P} ; {Q}| c
                                      Σ; Γ; {φ; P ∗ R} ; {Q}| free(x); c

                                      Fig. 4: BoSSL derivation rules.

not formalise sort-checking of formulae; however, for readability, we will use the
meta-variable α where the intended sort of the pure logic term is “permission”,
and Perm for the set of all permissions. The permission to allocate or deallocate
a memory-block [x, n]α is controlled by α.
3.1   BoSSL rules
New rules of BoSSL are shown in Fig. 4. The ﬁgure contains only 3 rules: this
minimal adjustment is possible thanks to our approach to uniﬁcation and permis-
sion accounting from ﬁrst principles. Writing to a memory location requires its
corresponding
           symbolica heap  to be annotated as mutable. Note that for a pre-
condition a = M;  x  →
                        5  , a normalisation
                                              rule like SubstLeft would ﬁrst
transform it into M = M; x → 5 , at which point the Write rule can be ap-
                                                M



plied. Note also that Alloc does not require speciﬁc permissions on the block
in the postcondition; if they turn out to be RO, the resulting goal is unsolvable.
   Unsurprisingly, the rule for accessing a memory cell just for reading purposes
requires no adjustments since any permission allows reading. Moreover, the Call
rule for method invocation does not need adjustments either. Below, we describe
how borrow and return seamlessly operate within a method call:
  Call
  F  f(xi ) : {φf ; Pf }{ψf ; Qf } ∈ Σ      R = [σ]Pf      φ ⇒ [σ]φf ei = [σ]xi
   Vars (ei ) ⊆ Γ φ  [σ]ψf            R  [σ]Qf Σ; Γ; {φ ∧ φ ; P ∗ R } ; {Q}| c
                            Σ; Γ; {φ; P ∗ R} ; {Q}| f(ei ); c

  The Call rule ﬁres when a sub-heap R in the precondition of the goal can
be uniﬁed with the precondition Pf of a function f from context Σ. Some salient
points are worth mentioning here: (1) the annotation borrowing from R to Pf for
those symbolic sub-heaps in Pf which require read-only permissions is handled
by the uniﬁcation of Pf with R, namely R = [σ]Pf (i.e., substitution accounts for
borrows: α/a); (2) the annotation recovery in the new precondition is implicit
                       Concise Read-Only Speciﬁcations for Better Synthesis       153


via R  [σ]Qf , where the substitution σ was computed during the uniﬁcation,
that is, while borrowing; (3) ﬁnding a substitution σ for R = [σ]Pf fails if R does
not have suﬃcient accessibility permissions to call f (i.e., substitutions of the
form a/M are disallowed since the domain of σ may only contain existentials).
We reiterate that read-only speciﬁcations only manipulate symbolic borrows,
that is to say, RO constants are not expected in the speciﬁcation.
3.2   Memory Model
We closely follow the standard SL memory model [32,37] and assume Loc ⊂ Val.

 (Heap) h ∈ Heaps ::= Loc → Val                 (Stack) s ∈ Stacks ::= Var → Val
   To enable C-like accounting of dynamically-allocated memory blocks, we as-
sume that the heap h also stores sizes of allocated blocks in dedicated locations.
Conceptually, this part of the heap corresponds to the meta-data of the mem-
ory allocator. This accounting ensures that only a previously allocated memory
block can be disposed (as opposed to any set of allocated locations), enabling the
free command to accept a single argument, the address of the block. To model
this meta-data, we introduce a function bl : Loc → Loc, where bl(x) denotes
the location in the heap where the block meta-data for the address x is stored, if
x is the starting address of a block. In an actual language implementation, bl(x)
might be, e.g., x − 1 (i.e., the meta-data is stored right before the block).
   Since we have opted for an unsophisticated permission mechanism, where the
heap ownership is not divisible, but some heap locations are restricted to RO,
the deﬁnition of the satisfaction relation Σ,R
                                              I for the annotated assertions in a
particular context Σ and given an interpretation I, is parameterised with a ﬁxed
set of read-only locations, R:

– h, s Σ,R
          I {φ;
              emp} iﬀ            s = true and dom (h) = ∅.
                                φ
– h, s Σ,R
                            α
          I    φ; e1 , ι  →
                             e2    iﬀ φs = true and l  e1 s +ι and dom (h) = {l}
  and h(l) = e2 s and l ∈ R ⇔ α = RO .
– h, s Σ,R             α
          I {φ; [e, n] } iﬀ φs = true and l  bl(es ) and dom (h) = {l} and
  h(l) = n and l ∈ R ⇔ α = RO.
– h, s Σ,R                                       ·                   Σ,R
          I {φ; P1 ∗ P2 } iﬀ ∃ h1 , h2 , h = h1 ∪ h2 and h1 , s I {φ; P1 } and
           Σ,R
   h2 , s I {φ; P2 }.
                        
– h, s Σ,R
          I φ; p(ψi ) iﬀ φs = true and D  p(xi ) ek , {χk , Rk } ∈ Σ and
                                
   h, ψi s ∈ I(D) and k ( h, s Σ,R     I [ψi /xi ]{φ ∧ ek ∧ χk ; Rk }).

   There are two non-standard cases: points-to and block, whose permissions
must agree with R. Note that in the deﬁnition of satisfaction, we only need to
consider that case where the permission α is a value (i.e., either RO or M).
Although in a speciﬁcation α can also be a variable, well-formedness guarantees
that this variable must be logical, and hence will be substituted away in the
deﬁnition of validity. We stress the fact that a reference that has RO permissions
to a certain symbolic heap still retains the full ownership of that heap, with the
restriction that it is not allowed to update or deallocate it. Note that deallocation
additionally requires a mutable permission for the enclosing block.
154     A. Costea et al.


3.3   Soundness
The BoSSL operational semantics is in the spirit of the traditional SL [38], and
hence is omitted for the sake of saving space (selected rules are available in
the extended version of the paper). The validity deﬁnition and the soundness
proofs of SSL are ported to BoSSL without any modiﬁcations, since our current
deﬁnition of satisfaction implies the one deﬁned for SSL:
Deﬁnition 1 (Validity). We say that a well-formed Hoare-style speciﬁcation
Σ; Γ; {P} c {Q} is valid wrt. the function dictionary Δ iﬀ whenever dom (s) = Γ,
∀σgv = [xi → di ]xi ∈GV(Γ,P,Q) such that h, s ΣI [σgv ]P, and Δ; h, (c, s) · ∗
 h , (skip, s ) · , it is also the case that h , s ΣI [σev ∪· σgv ]Q for some σev =
[yj → dj ]yj ∈EV(Γ,P,Q) .
  The following theorem guarantees that, given a program c generated with
BoSSL, a heap model, and a set of read-only locations R that satisfy the pro-
gram’s precondition, executing c does not change those read-only locations:
Theorem 1 (RO Heaps Do Not Change). Given a Hoare-style speciﬁcation
Σ; Γ; {φ; P}c{Q}, which is valid wrt. the function dictionary Δ, and a set of read-
only memory locations R, if:
   (i) h, s Σ,R
              I [σ]P, for some h, s and σ, and
  (ii) Δ; h, (c, s) · ∗ h , (c , s ) · for some h , s and c
 (iii) R ⊆ dom (h)
then R ⊆ dom (h ) and ∀l ∈ R, h(l) = h (l).
   Starting from an abstract state where a spatial heap has a read-only permis-
sion, under no circumstance can this permission be strengthened to M:
Corollary 1 (No Permission Strengthening). Given a valid Hoare-style
speciﬁcation Σ; Γ; {φ; P} c {ψ; Q} and a permission α, if ψ ⇒ (α = M) then
it is also the case that φ ⇒ (α = M) .
  As it turns out, permission weakening is possible, since, though problematic,
postcondition weakening is sound in general. However, even though this aﬀects
completeness, it does not aﬀect our termination
                                              a results. For
                                                             example,    given a
                                                         M      a2       M
synthesised auxiliary function F  f(x, r) : x → t ∗ r → x x → t ∗ r → t + 1 ,
                                                 1

                                                              
and a synthesis goal Σ, F; Γ; x → 7 ∗ y → x ; x → 7 ∗ y → z  c, ﬁring the Call
                                  M       M           M      M


rule
 for the candidate
                                 r) would lead to the unsolvable goal Σ, F; Γ;
                       function f(x,
                                     
     a2
         7 ∗ y → 8 ; x → 7 ∗ y → z  f(x, y); c. Frame may never be ﬁred on this
                M        M        M
  x →
new goal since the permission of reference x in the goal’s precondition has been
permanently weakened. To eliminate such sources of incompleteness we require
the user-provided predicates and speciﬁcations to be well-formed:
Deﬁnition 2 (Well-Formedness of Spatial Predicates). We say that a
spatial predicate p(xi ) ek , {χk , Rk } k∈1..N is well-formed iﬀ
            N
          ( k=1 (Vars (ek ) ∪ Vars (χk ) ∪ Vars (Rk )) ∩ Perm) ⊆ (xi ∩ Perm).
                        Concise Read-Only Speciﬁcations for Better Synthesis   155

That is, every accessibility annotation within the predicate’s clause is bound by
the predicate’s parameters.
Deﬁnition 3 (Well-Formedness of Speciﬁcations). We say that a Hoare-
style speciﬁcation Σ; Γ ; {P} c {Q} is well-formed iﬀ EV (Γ, P, Q)∩Perm = ∅ and
every predicate instance in P and Q is an instance of a well-formed predicate.
That is, postconditions are not allowed to have existential accessibility annota-
tions in order to avoid permanent weakening of accessibility.
   A callee that requires borrows for a symbolic heap always returns back to the
caller its original permission for that respective symbolic heap:
Corollary 2 (Borrows Always Return). A heaplet with permission α, either
(a) retains the same permission α after a call to a function that is decorated with
well-formed speciﬁcations and that requires for that heaplet to have read-only
permission, or (b) it may be deallocated in case if α = M.
4      Implementation and Evaluation
We implemented BoSSL in an enhanced version of the SuSLik tool, which
we refer to as ROBoSuSLik [12].11 The changes to the original SuSLik in-
frastructure aﬀected less than 100 lines of code. The extended synthesis is
backwards-compatible with the original benchmarks. To make this possible, we
treat the original SSL speciﬁcations as annotated/instantiated with M permis-
sions, whenever necessary, which is consistent with treatment of access permis-
sions in BoSSL.
   We have conducted an extensive experimental evaluation of ROBoSuSLik,
aiming to answer the following research questions:
1. Do borrowing annotations improve the performance of SSL-based synthesis
   when using standard search strategy [34, § 5.2]?
2. Do read-only borrows improve the quality of synthesised programs, in terms of
   size and comprehensibility, wrt. to their counterparts obtained from regular,
   “all-mutable” speciﬁcations?
3. Do we obtain stronger correctness guarantees for the programs from the stan-
   dard SSL benchmark suite [34, § 6.1] by simply adding, whenever reasonable,
   read-only annotations to their speciﬁcations?
4. Do borrowing speciﬁcations enable more robust synthesis? That is, should we
   expect to obtain better programs/synthesis performance on average regardless
   of the adopted uniﬁcation and search strategies?
4.1     Experimental Setup
Benchmark Suite. To tackle the above research questions, we have adopted most
of the heap-manipulating benchmarks from SuSLik suite [34, § 6.1] (with some
variations) into our sets of experiments. In particular we looked at the group
of benchmarks which manipulate singly linked list segments, sorted linked list
segments and binary trees. We did not include the benchmarks concerning binary
search trees (BSTs) for the reasons outlined in the next paragraph.
11
     The sources are available at https://github.com/TyGuS/robosuslik.
156    A. Costea et al.

The Tools. For a fair comparison which accounts for the latest advancements
to SuSLik, we chose to parameterise the synthesis process with a ﬂag that
turns the read-only annotations on and oﬀ (oﬀ means that they are set to be
mutable). Those values which are the result of having this ﬂag set will be marked
in the experiments with RO, while those marked with Mut ignore the read-only
annotations during the synthesis process. For simplicity, we will refer to the two
instances of the tool, namely RO and Mut, as two diﬀerent tools. Each tool was
set to timeout after 2 minutes of attempting to synthesise a program.
Criteria. In an attempt to quantify our results, we have looked at the size of
the synthesised program (AST size), the absolute time needed to synthesise the
code given its speciﬁcation, averaged over several runs (Time), the number of
backtrackings in the proof search due to nondeterminism (#Backtr ), the total
number of rule applications that the synthesis ﬁred during the search (#Rules),
including those that lead to unsolvable goals, and the strength of the guarantees
oﬀered by the speciﬁcations (Stronger Guarantees).
Variables. Some benchmarks have shown improvement over the synthesis pro-
cess without the read-only annotations. To emphasise the fact that read-only
annotations’ improvements are not accidental, we have varied the inductive deﬁ-
nitions of the corresponding benchmarks to experiment with diﬀerent properties
of the underlying structure: the shape of the structure (in all the deﬁnitions),
the length of the structure (for those benchmarks tagged with len), the values
stored within the structure (val ), a combination of all these properties (all ) as
well as with the sortedness property for the “Sorted list” group of benchmarks.
Experiment Schema. To measure the performance and the quality of the borrowing-
aware synthesis we ran the benchmarks against the two diﬀerent tools and did
a one-to-one comparison of the results. We ran each tool three times for each
benchmark, and average the resulted synthesis time. All the other evaluation
criteria remain constant within all three runs.
   To measure the tools’ robustness we stressed the synthesis algorithm by alter-
ing the default proof search strategy. We prepared 42 such perturbations which
we used to run against the diﬀerent program variants enumerated above. Each
pair of program variant and proof strategy perturbation has been then analysed
to measure the number of rules that had been ﬁred by RO and Mut.
Hardware Setup. The experiments were conducted on a 64-bit machine running
Ubuntu, with an Intel Xeon CPU (6 cores, 2.40GHz) with 32GB RAM.
4.2   Performance and Quality of the Borrowing-Aware Synthesis
Tab. 1 captures the results of running RO and Mut against the considered bench-
marks. It provides the empirical proof that the borrowing-aware synthesis im-
proves the performance of the original SSL-based synthesis, or in other words,
answering positively the Research Question 1. RO suﬀers almost no loss in per-
formance (except for a few cases, such as the list segment append where there
is a negligible increase in time), while the gain is considerable for those synthe-
sis problems with complex pointer manipulation. For example, if we consider
the number of ﬁred rules as the performance measurement criteria, in the worst
                              Concise Read-Only Speciﬁcations for Better Synthesis          157

                         AST size Time (sec)    #Backtr.       #Rules     Stronger
Group    Description
                         RO Mut RO Mut Mut/RO RO Mut Mut/RO RO Mut Mut/RO Guarant.
             append      20    20   1.5   1.4   0.9x    8   8    1.0x    77 78     1.0x   YES
              delete     44    44   1.9   2.1   1.1x   67 67     1.0x   180 180    1.0x   same
             dispose     11    11   0.5   0.5   1.0x    0   0    1.0x     8   8    1.0x   same
 Linked        init      13    13   0.7   0.7   1.0x    5   5    1.0x    27 27     1.0x   YES
  List        lcopy      32    35   1.0   1.0   1.0x    9  14    1.5x    66 82     1.2x   YES
Segment      length      22    22   1.5   1.5   1.0x    2   2    1.0x    38 38     1.0x   YES
               max       28    28   1.4   1.5   1.1x    2   2    1.0x    38 38     1.0x   YES
               min       28    28   1.5   1.5   1.0x    2   2    1.0x    38 38     1.0x   YES
           singleton     11    11   0.5   0.5   1.0x    8   8    1.0x    30 30     1.0x   same
          ins-sort-all   29    29   3.7   3.8   1.0x    5   5    1.0x    60 60     1.0x   YES
         ins-sort-len    29    29   3.0   3.0   1.0x    7   8    1.1x    59 60     1.0x   YES
 Sorted
          ins-sort-val   29    29   2.6   2.5   1.0x    5   5    1.0x    57 57     1.0x   YES
  List
              insert     53    53   7.8   8.0   1.0x   35 96     2.7x   214 338    1.6x   YES
            prepend      11    11   0.5   0.6   1.2x    1   1    1.0x    17 17     1.0x   YES
             dispose     16    16   0.4   0.5   1.2x    0   0    1.0x    10 10     1.0x   same
          ﬂatten-acc     35    35   2.1   2.0   1.0x   24 24     1.0x   118 118    1.0x   same
          ﬂatten-app     48    48   1.6   1.7   1.0x   14 14     1.0x    76 76     1.0x   same
             morph       19    19   0.6   0.5   1.0x    1   1    1.0x    24 24     1.0x   YES
           tcopy-all     42    51   1.5   2.2   1.5x   10 88     8.8x    85 296    3.5x   YES
           tcopy-len     36    42   1.3   2.0   1.5x    6  90     15x    72 304    4.2x   YES
           tcopy-val     42    51   1.4   5.3   3.8x   10 1222   122x    82 2673   32x    YES
  Tree
        tcopy-ptr-all    46    55   1.6   2.4   1.5x   10 88     8.8x    93 303    3.3x   YES
        tcopy-ptr-len    40    46   1.3   2.2   1.7x    6  90     15x    80 311    3.9x   YES
        tcopy-ptr-val    46    55   1.3   5.8   4.5x   10 1222   122x    89 2679   30x    YES
            tsize-all    32    38   1.5   1.4   0.9x    2   4    2.0x    45 51     1.1x   YES
            tsize-len    32    32   1.2   1.1   0.9x    2   2    1.0x    44 46     1.0x   YES
         tsize-ptr-all   36    42   1.6   1.4   0.9x    2   4    2.0x    53 58     1.1x   YES
         tsize-ptr-len   36    36   1.3   1.3   1.0x    2   2    1.0x    52 53     1.0x   YES

Table 1: Benchmarks and comparison between the results for synthesis with read-
only annotations (RO) and without them (Mut). For each case study we measure
the AST size of the synthesised program, the Time needed to synthesize the
benchmark, the number of times that the synthesiser had to discard a derivation
branch (#Backtr.), and the total number of ﬁred rules (#Rules).

case, RO behaves the same as Mut, while in the best scenario it buys us a 32-fold
decrease in the number of applied rules. At the same time, synthesising a few
small examples in the RO case is a bit slower, despite the same or smaller num-
ber of rule applications. This is due to the increased number of logical variables
(because of added borrows) when discharging obligations via SMT solver.
   Fig. 5 oﬀers a statistical view of the numbers in the table, where smaller bars
mark a better performance. The barplots indicate that as the complexity of the
problem increases (approximately from left to right), RO outperforms Mut.
   Perhaps the most important take-away from this experiment is that the syn-
thesis with read-only borrows often produces a more concise program (light green
cells in the columnt AST size of Tab. 1), while retaining the same or better per-
formance wrt. all the evaluated criteria. For instance, RO gets rid of the spurious
write from the motivating example introduced in Sec. 1, reducing the AST size
from 35 nodes down to 32, while in the same time ﬁring fewer rules. That also
means that we secure a positive answer for Research Question 2.

4.3    Stronger Correctness Guarantees
To answer Research Question 3, we have manually compared the guarantees
oﬀered by the speciﬁcations annotated with RO permissions against the default
158                                   A. Costea et al.
                                60                                              AST Sizes of Synthesised Programs
                                         Read−Only
                                         Mutable
                                50
  Number of AST Nodes




                                40


                                30


                                20


                                10


                                 0
                                         th  ax    in   n   e      t   y
                                                                ini cop en
                                                                           d     te end er t len val −all len −all len −all ose rph len val −all len val −all app acc
                                       ng         m leto pos                   le
                                     le
                                            m
                                                      g dis          l
                                                                       ap
                                                                         p   de rep    ins or t− or t− or t ize− ize ptr− −ptr isp mo py− py− opy ptr− ptr− −ptr en− en−
                                                   sin                            p       −s s−s ns−
                                                                                                       s ts      ts e− ze      d
                                                                                                                                     tc
                                                                                                                                       o tco tc py− py− py latt latt
                                                                                       ins in       i                iz tsi                      o tco  tc
                                                                                                                                                          o    f    f
                                                                                                                   ts                          tc

                                                                                      Rules Tried while Searching
                                         Read−Only
                                10
log2 of number of tried rules




                                         Mutable

                                 8


                                 6


                                 4


                                 2


                                 0
                                         th  ax    in   n   e      t   y
                                                                ini cop en
                                                                           d     te end er t len val −all len −all len −all ose rph len val −all len val −all app acc
                                       ng         m leto pos                   le
                                     le
                                            m
                                                      g dis          l
                                                                       ap
                                                                         p   de rep    ins or t− or t− or t ize− ize ptr− −ptr isp mo py− py− opy ptr− ptr− −ptr en− en−
                                                   sin                            p       −s s−s ns−
                                                                                                       s ts      ts e− ze      d
                                                                                                                                     tc
                                                                                                                                       o tco tc py− py− py latt latt
                                                                                       ins in       i                iz tsi                      o tco  tc
                                                                                                                                                           o   f    f
                                                                                                                   ts                          tc
                                 Fig. 5: Statistics for synthesis with and without Read-Only speciﬁcations.



ones - the results are summarized in the last column of Tab. 1. For instance, a
speciﬁcation stating that the shape of a linked-list segment is read-only implies
that the size of that segment remains constant through the program’s execution.
In other words, the length property need not be captured separately in the
segment’s deﬁnition. If, in addition to the shape, the payload of the segment is
also read-only, then the set of values and their ordering are also invariant.
   Consider the goal {lseg(x, y, s, a1 , a2 , a3 )} ; {lseg(x, y, s, a1 , a2 , a3 )}, where
lseg is an inductive deﬁnition of a list segment which ends at y and contains
the set of values s. The borrowing-aware synthesiser will produce a program
which is guaranteed to treat the segment pointed by x and ending with y as
read-only (that is, its shape, length, values and orderings are invariant). At the
same time, for a goal {lseg(x, y, s)} ; {lseg(x, y, s)} , the guarantees are that
the returned segment still ends in y and contains values s. Internal modiﬁcations
of the segment, such as reordering and duplicating list elements, may still occur.
   The few entries marked with same are programs with speciﬁcations which have
not got stronger when instrumented with RO annotations (e.g., delete). These
benchmarks require mutation over the entire data structure, hence the read-only
annotations do not inﬂuence the oﬀered guarantees. Overall, our observations
that read-only annotations oﬀer stronger guarantees are in agreement with the
works on SL-based program veriﬁcation [9, 13], but are promoted here to the
more challenging problem of program synthesis.
                      Concise Read-Only Speciﬁcations for Better Synthesis     159

4.4   Robustness under Synthesis Perturbations
There is no single search heuristics that will work equally well for any given
speciﬁcation: for a particular ﬁxed search strategy, a synthesiser can exhibit
suboptimal performance for some goals, while converging quickly on some others.
By evaluating robustness wrt. to RO and M speciﬁcation methodologies, we are
hoping to show that, provided a large variety of “reasonable” search heuristics,
read-only annotations deliver better synthesis performance “on average”.
   For this set of experiments, we have focused on four characteristic programs
from our performance benchmarks based on their pointer manipulation com-
plexity: list segment copy (lcopy), insertion into a sorted list segment (insert),
copying a tree (tcopy), and a variation of the tree copy that shares the same
pointer for the input tree and its returned copy (tcopy-ptr).
Exploring Diﬀerent Uniﬁcation Orders. Since spatial uniﬁcation stays at the core
of the synthesis process, we implemented 6 diﬀerent strategies for choosing a
uniﬁcation candidate based on the following criteria: the size of the heaplet chunk
(favor the smallest heap vs. the largest one as the best uniﬁcation candidate), the
name of the predicate (we considered both an ascending as well as a descending
priority queue), and a customised ranking function which associates a cost to a
symbolic heap based on its kind—a block is cheaper to unify than a points-to
which in turn is cheaper than a spatial predicate.
Exploring Diﬀerent Search Strategies. We next designed 6 strategies for priori-
tising the rule applications. One of the crux rules in this matter, is the Write
rule whose diﬀerent priority schemes might make all the results seem randomly-
generated. In the cases where Write leads to unsolvable goals, one might right-
fully argue that RO has a clear advantage over Mut (fail fast). However, for
the cases where mutation leads to a solution faster, then Mut might have an
advantage over RO (solve fast). Because these are just intuitive observations,
and for fairness sake, we experimented with both the cases where Write has a
high and a low priority in the queue of rule phases [34, § 5.2]. Since most of the
benchmarks involve recursion, we also chose to shuﬄe around the priorities of
the Open and Call rules. Again, we chose between a stack high and a bottom
low priority for these rules to give a fair chance to both tools.
   We considered all combinations of the 6 uniﬁcation permutations and the 6
rule-application permutations (plus the default one) to obtain 42 diﬀerent proof
search perturbations. We will use the following notation in the narrative below:
– S is the set comprising the synthesis problems: lcopy, insert, tcopy, tcopy-ptr.
– V is the set of all speciﬁcation variations: len, val, all.
– K is the set of all 42 possible tool perturbations.
   The distributions of the number of rules ﬁred for each tool (RO and Mut)
with the 42 perturbations over the 4 synthesis problems with 3 variants of spec-
iﬁcation each, that is 1008 diﬀerent synthesis runs, are summarised using the
boxplots in Fig. 6. There is a boxplot corresponding to each pair of tool and
synthesis problem. In the ideal case, each boxplot contains 126 data points cor-
responding to a unique combination (v, k) of a speciﬁcation variation v ∈ V and
a tool perturbation k ∈ K. A boxplot is the distribution of such data based on a
160                                   A. Costea et al.


                                          Read−Only
                                          Mutable
                      16
                      14
      log2 of number of tried rules
         10           8
                      612




                                                     6)            6)           (42
                                                                                   )
                                                                                               (42
                                                                                                  )            6)            8)              90
                                                                                                                                               )
                                                                                                                                                              84
                                                                                                                                                                )
                                                  (12           (12        er t           er t              (12           (10            tr (             tr (
                                               py            py         ins            ins               py            py              −p               −p
                                            lco           lco                                         tco           tco            copy
                                                                                                                                                    copy
                                                                                                                                  t                t


Fig. 6: Boxplots of variations in log2 (numbers of applied rules) for synthesis per-
turbations. Numbers of data points for each example are given in parentheses.

six number summary: minimum, ﬁrst quartile, median, third quartile, maximum,
outliers. For example, the boxplot for tcopy-ptr corresponding to RO and con-
taining 90 data points, reads as follows: “the synthesis processes ﬁred between
64 and 256 rules, with most of the processes ﬁring between 64 and 128 rules.
There are three exception where the synthesiser ﬁred more than 256 rules”. Note
that the y-axis represents the binary logarithm of the number of ﬁred rules.
   Even though we attempted to synthesise each program 126 times for each tool,
some attempts hit the timeout and therefore their corresponding data points had
to be eliminated from the boxplot. It is of note, though, that whenever RO with
conﬁguration (v, k) hit the timeout for the synthesis problem s ∈ S, so did Mut,
hence both the (RO, s, (v, k)) as well as (Mut, s, (v, k)) are omitted from the
boxplots. But the inverse did not hold: RO hit the timeout fewer times than
Mut, hence RO is measured at disadvantage (i.e., more data points means more
opportunities to show worse results). Since insert collected the highest number
of timeouts, we equalised it to remove non-matched entries across the two tools.
   Despite RO’s potential measurement disadvantage, the boxplots depicts it as a
clear winner. Not only RO ﬁres fewer rules in all the cases, but with the exception
of insert, it is also more stable to the proof search perturbations, it varies a
few order of magnitude less than Mut does for the same conﬁgurations. Fig. 7
supports this observation by oﬀering a more detailed view on the distributions
of the numbers of ﬁred rules per synthesis conﬁguration. Taller bars show that
more processes fall in the same range (wrt. the number of ﬁred rules). For lcopy,
tcopy, tcopy-ptr it is clear that Mut has a wider distribution of the number
of ﬁred rules, that is, Mut is more sensitive to the perturbations than RO. We
additionally make some further observations:
                                                         Concise Read-Only Speciﬁcations for Better Synthesis                                                                        161

                             lcopy (RO)                                   insert (RO)                                 tcopy (RO)                                   tcopy−ptr (RO)
            60




                                                         60




                                                                                                     60




                                                                                                                                                  60
                             126 data points                              42 data points                              126 data points                               90 data points
            50




                                                         50




                                                                                                     50




                                                                                                                                                  50
            40




                                                         40




                                                                                                     40




                                                                                                                                                  40
Frequency

            30




                                                         30




                                                                                                     30




                                                                                                                                                  30
            20




                                                         20




                                                                                                     20




                                                                                                                                                  20
            10




                                                         10




                                                                                                     10




                                                                                                                                                  10
            0




                                                         0




                                                                                                     0




                                                                                                                                                  0
                 4   6   8    10   12    14    16   18        4   6   8    10   12    14   16   18        4   6   8    10   12    14    16   18        4   6   8     10   12    14   16   18

                             lcopy (Mut)                                  insert (Mut)                                tcopy (Mut)                                  tcopy−ptr (Mut)
            60




                                                         60




                                                                                                     60




                                                                                                                                                  60
                             126 data points                              42 data points                              108 data points                               84 data points
            50




                                                         50




                                                                                                     50




                                                                                                                                                  50
            40




                                                         40




                                                                                                     40




                                                                                                                                                  40
Frequency

            30




                                                         30




                                                                                                     30




                                                                                                                                                  30
            20




                                                         20




                                                                                                     20




                                                                                                                                                  20
            10




                                                         10




                                                                                                     10




                                                                                                                                                  10
            0




                                                         0




                                                                                                     0




                                                                                                                                                  0
                 4   6   8    10   12   14     16   18        4   6   8    10   12    14   16   18        4   6   8    10   12   14     16   18        4   6   8     10   12    14   16   18




                     Fig. 7: Distributions of log2 (number of attempted rule applications).
– Despite a similar distribution wrt. the numbers of ﬁred rules in the case of
  insert, RO produces compact ASTs of size 53 for all perturbations, while Mut
  ﬂuctuates between producing ASTs of size 53 and 62.
– For all the synthesis tasks, RO produced the same AST irrespective of the
  tool’s perturbation. In contrast, there were synthesis problems for which Mut
  produced as many as 3 diﬀerent ASTs for diﬀerent perturbations, none of
  which were as concise as the one produced by RO for the same conﬁguration.
– The outliers of (Mut, lcopy) are ridiculously high, ﬁring close to 40k rules.
– The outliers of (RO, tcopy) are still below the median values of (Mut, tcopy).
– Except for insert, the best performance of Mut, in terms of ﬁred rules, barely
  overlaps with the worst performance of RO.
– Except for insert, the medians of RO are closer to the lowest value of the
  data distribution, as opposed to Mut where the tendancy is to ﬁre more rules.
– In absolute values, RO hit the 2-minutes timeout 102 times compared to Mut,
  which hit the timeout 132 times.
We believe that the main take-aways from this set of experiments, along with
the positive answer to the Research Question 4, are as follows:
– RO is more stable wrt. the number of rules ﬁred and the size of the generated
  AST for many reasonable proof search perturbations.
– RO produces better programs, which avoid spurious statements, irrespective
  of the perturbation and number of rules ﬁred during the search.
5                    Limitations and Discussion
Flexible aliasing. Separating conjunction asserts that the heap can be split into
two disjoint parts, or in other words it carries an implicit non-aliasing infor-
mation. Speciﬁcally, x → ∗ y → states that x and y are non-aliased. Such
162       A. Costea et al.

assertions can be used to specify methods as below:
      {x → n ∗ y → m ∗ ret → x} sum(x, y, ret) {x → n ∗ y → m ∗ ret → n + m}
 Occasionally, enforcing x and y to be non-aliased is too restrictive, rejecting
safe calls such as sum(p, p, q). Approaches to support immutable annotations
permit such calls without compromising safety if both pointers, aliased or not,
are annotated as read-only [9,13]. BoSSL does not support such ﬂexible aliasing.
Precondition strengthening. Let us assume that srtl(x, n, lo, hi, α1 , α2 , α3 ) is an
inductive predicate that describes a sorted linked list of size n with lo and
hi being the list’s minimum and maximum payload value, respectively. Now,
consider the following synthesis goal:
   {x, y} ; {y → x ∗ srtl(x, n, lo, hi, M, M, M)} ; {y → n ∗ srtl(x, n, lo, hi, M, M, M)}.
 As stated, the goal clearly requires the program to compute the length n of
the list. Imagine that we already have a function that does precisely that, even
though it is stated in terms of a list predicate that does not enforce sortedness:
       {ret → x ∗ ls(x, n, a1 , a2 , a3 )} length(x, ret) {ret → n ∗ ls(x, n, a1 , a2 , a3 )}
 To solve the initial goal, the synthesiser could weaken the given precondition
srtl(x, n, lo, hi, M, M, M) to ls(x, n, M, M, M), and then successfully synthesise a
call to the length method. Unfortunately, the resulting goal, obtained after hav-
ing emitted the call to length and applying Frame, is unsolvable:
                  {x, y} {ls(x, n, M, M, M)} ; {srtl(x, n, lo, hi, M, M, M)}.
 since the logic does not allow to strengthen an arbitrary linked list to a sorted
linked list without retaining the prior knowledge. Should we have adopted an
alternative approach to read-only annotations [9,13] allowing the caller to retain
the full permission of the sorted list, then the postcondition of length would not
contain the list-related part of the heap and would only quantify over the result
pointer {ret → n}, thus leading to the solvable goal below:
             {x, y} ; {srtl(x, n, lo, hi, M, M, M)} ; {srtl(x, n, lo, hi, M, M, M)}.
 One straightforward way for BoSSL to cope with this limitation is to simply
add a version of length annotated with speciﬁcations that cater to srtl.
Overcoming the limitations. While the “caller keeps the permission” kind of ap-
proach would buy us ﬂexible aliasing and calls with weaker speciﬁcations, it
would compromise the beneﬁts discussed earlier with respect to the granular-
ity of borrow-polymorphic inductive predicates. One possible solution to gain
the best of both worlds would be to design a permission system which allows
both borrow-polymorphic inductive predicates as well as read-only modalities to
co-exist, where the latter would overwrite the predicate’s mixed permissions. In
other words, the read-only modality enforces a read-only treatment of the pred-
icate irrespective of its permission arguments, while the permission arguments
control the treatment of a mutable predicate. The theoretical implications of
such a design choice are left as part of future work.
Extending read-only speciﬁcations to concurrency. Thus far we have only inves-
tigated the synthesis of sequential programs, for which read-only annotations
helped to reduce the synthesis cost. Assuming that the synthesiser has the capa-
bility to synthesise concurrent programs as well, the borrows annotation mecha-
nism in its current form may not be able to cope with general resource sharing.
                       Concise Read-Only Speciﬁcations for Better Synthesis        163

This is because a callee which requires read-only permissions to a particular
symbolic heap still consumes the entire required symbolic heap from the caller,
despite the read-only requirement; hence, there is no space left for sharing. That
said, the recently proposed alternative approaches to introduce read-only an-
notations [9, 13] have no formal support for heap sharing in the presence of
concurrency either. To address these challenges, we could adopt a more sophis-
ticated approach based on fractional permissions mechanism [7,8,20,25,30], but
this is left as part of future work since it is orthogonal to the current scope.

6    Related Work
Language design. There is a large body of work on integrating access permissions
into practical type systems [5, 16, 42] (see, e.g., the survey by Clarke et al. [10]).
One notable such system, which is the closest in its spirit to our proposal, is
the borrows type system of the Rust programming language [1] proved safe with
RustBelt [22]. Similar to our approach, borrows in Rust are short-lived: in
Rust they share the scope with the owner; in our approach they do not escape
the scope of a method call. In contrast with our work, Rust’s type system care-
fully manages diﬀerent references to data by imposing strict sharing constraints,
whereas in our approach the treatment of aliasing is taken care of automatically
by building on Separation Logic. Moreover, Rust allows read-only borrows to be
duplicated, while in the sequential setting of BoSSL this is currently not possible.
   Somewhat related to our approach, Naden et al. propose a mechanisms for
borrowing permissions, albeit integrated as a fundamental part of a type sys-
tem [31]. Their type system comes equipped with change permissions which
enforce the borrowing requirements and describe the eﬀects of the borrowing
upon return. As a result of treating permissions as ﬁrst-class values, we do not
need to explicitly describe the ﬂow of permissions for each borrow since this is
controlled by a mix of the substitution and uniﬁcation principles.
Program veriﬁcation with read-only permissions. Boyland introduced fractional
permissions to statically reason about interference in the presence of shared-
memory concurrency [8]. A permission p denotes full resource ownership (i.e.
read-write access) when p = 1, while p ∈ (0, 1) denotes a partial ownership (i.e.
read-only access). To leverage permissions in practice, a system must support
two key operations: permission splitting and permission borrowing. Permission
                                                        p        p1      p2
splitting (and merging back) follows the split rule: x → a = x →  a∗x →  a, with p =
p1 +p2 and p, p1 , p2 ∈ (0, 1]. Permission borrowing refers to the safe manipulation
of permissions: a callee may remove some permissions from the caller, use them
temporarily, and give them back upon return.
   Though it exists, tool support for fractional permissions is still scarce. Leino
and Müller introduced a mechanism for storing fractional permissions in data
structures via dedicated access predicates in the Chalice veriﬁcation tool [27].
To promote generic speciﬁcations, Heule et al. advanced Chalice with insta-
tiable abstract permissions, allowing automatic ﬁre of the split rule and symbolic
borrowing [20]. VeriFast [21] is guided by contracts written in Separation Logic
and assumes the existence of lemmas to cater for permission splitting. Viper [30]
164     A. Costea et al.

is an intermediate language which supports various permission models, includ-
ing abstract fractional permissions [4, 43]. Similar to Chalice, the permissions
are attached to memory locations using an accessibility predicate. To reason
about it, Viper uses permission-aware assertions and assumptions, which corre-
spond in our approach to the uniﬁcation and the substitution operations, respec-
tively. Like Viper, we enhance the basic memory constructors, that is blocks
and points-to, to account for permissions, but in contrast, the Call rule in our
approach is standard, i.e., not permission-aware.
   These tools, along with others [3, 18], oﬀer strong correctness guarantees in
the presence of resource sharing. However, there is a class of problems, namely
those involving predicates with mixed permissions, whose guarantees are weak-
ened due to the general fractional permissions model behind these tools. We next
exemplify this class of problems in a sequential setting. We start by considering
a method which resets the values stored in a linked-list while maintaining its
shape (p < 1 below is to enforce the immutable shape):
            {p < 1; ls(x, S)[1, p]} void reset(loc x) {ls(x, {0})[1, p]}.
Assume a call to this method, namely reset(y). The caller has full permission
over the entire list passed as argument, that is ls(y, B)[1, 1]. This attempt leads
to two issues. The ﬁrst has to do with splitting the payload’s permission (before
the call) such that it matches the callee’s postcondition. To be able to modify the
list’s payload, the callee must get the payload’s full ownership, hence the caller
should retain 0: ls(y, B)[1, 1] = ls(y, B)[0, 1/2] ∗ ls(y, B)[1, 1/2]. But 0 is not a valid
fractional permission. The second issue surfaces while attempting to merge the
permissions after the call: ls(y, B)[0, 1/2]∗ls(y, {0})[1, 1/2] is invalid since the two
instances of ls have incompatible arguments (namely B and {0}). To avoid such
problems, BoSSL abandons the split rule and instead always manipulates full
ownership of resources, hence it does not use fractions. This compromise, along
with the support for symbolic borrows, allows ROBoSuSLik to guarantee read-
only-ness in a sequential setting while avoiding the aforementioned issues. More
investigations are needed in order to lift this result to concurrency reasoning.
Another feature which distinguishes the current work from those based on frac-
tional permissions, is the support for permissions as parameters of the predicate,
which in turn supports the deﬁnition of predicates with mixed permissions.
   Immutable speciﬁcations on top of Separation Logic have also been studied by
David and Chin [13]. Unlike our approach which treats borrows as polymorphic
variables that rely on the basic concept of substitution, their annotation mech-
anism comprises only constants and requires a specially tailored entailment on
top of enhanced proof rules. Since callers retain the heap ownership upon calling
a method with read-only requirements, their machinery supports ﬂexible aliasing
and cut-point preservation—features that we could not ﬁnd a good use for in the
context of program synthesis. An attempt to extend David and Chin’s work by
adding support for predicates with mixed permissions [11] suﬀers from signiﬁcant
annotation overhead. Speciﬁcally, it employs a mix of mutable, immutable, and
absent permissions, so that each mutable heaplet in the precondition requires a
corresponding matching heaplet annotated with absent in the postcondition.
                       Concise Read-Only Speciﬁcations for Better Synthesis      165

   Charguéraud and Pottier [9] extended Separation Logic with RO assertions
that can be freely duplicated or discarded. Their approach creates lexically-
scoped copies of the RO-permissions before emitting a call, which, in turn, in-
volves discarding the corresponding heap from the postcondition to guarantee a
sound RO-modality. Adapting this modality to program synthesis guided by pre-
and postconditions would require a completely new system of deductive synthesis
since most of the rules in SSL are not designed to handle the d iscardable RO-
heaps. In contrast, BoSSL supports permission-parametric predicates (e.g., (9))
requiring only minimal adjustments to its host logic, i.e., SSL.
Program synthesis. BoSSL continues a long line of work on program synthesis
from formal speciﬁcations [26, 36, 40, 41, 44] and in particular, deductive synthe-
sis [14, 23, 29, 33, 34], which can be characterised as search in the space of proofs
of program correctness (rather than in the space of programs). Most directly
BoSSL builds upon our prior work on SSL [34] and enhances its speciﬁcation
language with read-only annotations. In that sense, the present work is also re-
lated to various approaches that use non-functional speciﬁcations as input to
synthesis. It is common to use syntactic non-functional speciﬁcations, such as
grammars [2], sketches [36, 40], or restrictions on the number of times a compo-
nent can be used [19]. More recent work has explored semantic non-functional
speciﬁcations, including type annotations for resource consumption [24] and se-
curity/privacy [17,35,39]. This research direction is promising because (a) anno-
tations often enable the programmer to express a strong speciﬁcation concisely,
and (b) checking annotations is often more compositional (i.e., fails faster) than
checking functional speciﬁcations, which makes synthesis more eﬃcient. In the
present work we have demonstrated that both of these beneﬁts of non-functional
speciﬁcations also hold for the read-only annotations of BoSSL.


7   Conclusion
In this work, we have advanced the state of the art in program synthesis by
highlighting the beneﬁts of guiding the synthesis process with information about
memory access permissions. We have designed the logic BoSSL and implemented
the tool ROBoSuSLik, showing that a minimalistic discipline for read-only per-
missions already brings signiﬁcant improvements wrt. the performance and ro-
bustness of the synthesiser, as well as wrt. the quality of its generated programs.
Acknowledgements. We thank Alexander J. Summers, Cristina David, Olivier
Danvy, and Peter O’Hearn for their comments on the prelimiary versions of
the paper. We are very grateful to the ESOP 2020 reviewers for their detailed
feedback, which helped to conduct a more adequate comparison with related
approaches and, thus, better frame the conceptual contributions of this work.
   Nadia Polikarpova’s research was supported by NSF grant 1911149. Amy Zhu’s
research internship and stay in Singapore during the Summer 2019 was supported
by Ilya Sergey’s start-up grant at Yale-NUS College, and made possible thanks
to UBC Science Co-op Program.
166    A. Costea et al.

References
 1. The Rust Programming Language: References and Borrowing. https://doc.
    rust-lang.org/1.8.0/book/references-and-borrowing.html, 2019.
 2. Rajeev Alur, Rastislav Bodı́k, Garvit Juniwal, Milo M. K. Martin, Mukund
    Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina
    Torlak, and Abhishek Udupa. Syntax-guided synthesis. In FMCAD, pages 1–8.
    IEEE, 2013.
 3. Andrew W. Appel. Veriﬁed software toolchain - (invited talk). In ESOP, volume
    6602 of LNCS, pages 1–17. Springer, 2011.
 4. Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers.
    Leveraging Rust types for modular speciﬁcation and veriﬁcation. PACMPL,
    3(OOPSLA):147:1–147:30, 2019.
 5. Thibaut Balabonski, François Pottier, and Jonathan Protzenko. The Design and
    Formalization of Mezzo, a Permission-Based Programming Language. ACM Trans.
    Program. Lang. Syst., 38(4):14:1–14:94, 2016.
 6. Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic execution
    with separation logic. In APLAS, volume 3780 of LNCS, pages 52–68. Springer,
    2005.
 7. Richard Bornat, Cristiano Calcagno, Peter W. O’Hearn, and Matthew J. Parkin-
    son. Permission Accounting in Separation Logic. In POPL, pages 259–270. ACM,
    2005.
 8. John Boyland. Checking Interference with Fractional Permissions. In SAS, volume
    2694 of LNCS, pages 55–72. Springer, 2003.
 9. Arthur Charguéraud and François Pottier. Temporary Read-Only Permissions for
    Separation Logic. In ESOP, volume 10201 of LNCS, pages 260–286. Springer, 2017.
10. Dave Clarke, Johan Östlund, Ilya Sergey, and Tobias Wrigstad. Ownership Types:
    A Survey, pages 15–58. Springer Berlin Heidelberg, 2013.
11. Andreea Costea, Asankhaya Sharma, and Cristina David. HIPimm: verifying gran-
    ular immutability guarantees. In PEPM, pages 189–194. ACM, 2014.
12. Andreea Costea, Amy Zhu, Nadia Polikarpova, and Ilya Sergey. ROBoSuSLik:
    ESOP 2020 Artifact. 2020. DOI: 10.5281/zenodo.3630044.
13. Cristina David and Wei-Ngan Chin. Immutable speciﬁcations for more concise and
    precise veriﬁcation. In OOPSLA, pages 359–374. ACM, 2011.
14. Benjamin Delaware, Clément Pit-Claudel, Jason Gross, and Adam Chlipala. Fiat:
    Deductive Synthesis of Abstract Data Types in a Proof Assistant. In POPL, pages
    689–700. ACM, 2015.
15. Robert Dockins, Aquinas Hobor, and Andrew W. Appel. A fresh look at separation
    algebras and share accounting. In APLAS, volume 5904 of LNCS, pages 161–177.
    Springer, 2009.
16. Ronald Garcia, Éric Tanter, Roger Wolﬀ, and Jonathan Aldrich. Foundations of
    typestate-oriented programming. ACM Trans. Program. Lang. Syst., 36(4):12:1–
    12:44, 2014.
17. Adrià Gascón, Ashish Tiwari, Brent Carmer, and Umang Mathur. Look for the
    proof to ﬁnd the program: Decorated-component-based program synthesis. In CAV,
    volume 10427 of LNCS, pages 86–103. Springer, 2017.
18. Colin S. Gordon, Matthew J. Parkinson, Jared Parsons, Aleks Bromﬁeld, and Joe
    Duﬀy. Uniqueness and reference immutability for safe parallelism. In OOPSLA,
    pages 21–40. ACM, 2012.
19. Sumit Gulwani, Susmit Jha, Ashish Tiwari, and Ramarathnam Venkatesan. Syn-
    thesis of loop-free programs. In PLDI, pages 62–73. ACM, 2011.
                       Concise Read-Only Speciﬁcations for Better Synthesis      167

20. Stefan Heule, K. Rustan M. Leino, Peter Müller, and Alexander J. Summers. Ab-
    stract read permissions: Fractional permissions without the fractions. In VMCAI,
    volume 7737 of LNCS, pages 315–334. Springer, 2013.
21. Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx,
    and Frank Piessens. VeriFast: A Powerful, Sound, Predictable, Fast Veriﬁer for C
    and Java. In NASA Formal Methods, volume 6617 of LNCS, pages 41–55. Springer,
    2011.
22. Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. Rust-
    Belt: Securing the foundations of the Rust programming language. PACMPL,
    2(POPL):66, 2017.
23. Etienne Kneuss, Ivan Kuraj, Viktor Kuncak, and Philippe Suter. Synthesis modulo
    recursive functions. In OOPSLA, pages 407–426. ACM, 2013.
24. Tristan Knoth, Di Wang, Nadia Polikarpova, and Jan Hoﬀmann. Resource-guided
    program synthesis. In PLDI, pages 253–268. ACM, 2019.
25. Xuan Bach Le and Aquinas Hobor. Logical reasoning for disjoint permissions. In
    ESOP, volume 10801 of LNCS, pages 385–414. Springer, 2018.
26. K. Rustan M. Leino and Aleksandar Milicevic. Program Extrapolation with Jen-
    nisys. In OOPSLA, pages 411–430. ACM, 2012.
27. K. Rustan M. Leino and Peter Müller. A Basis for Verifying Multi-threaded Pro-
    grams. In ESOP, volume 5502 of LNCS, pages 378–393. Springer, 2009.
28. K. Rustan M. Leino, Peter Müller, and Jan Smans. Veriﬁcation of Concurrent
    Programs with Chalice. In Foundations of Security Analysis and Design V, FOSAD
    2007/2008/2009 Tutorial Lectures, volume 5705 of LNCS, pages 195–222. Springer,
    2009.
29. Zohar Manna and Richard J. Waldinger. A deductive approach to program syn-
    thesis. ACM Trans. Program. Lang. Syst., 2(1):90–121, 1980.
30. Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. Viper: A Veriﬁcation
    Infrastructure for Permission-Based Reasoning. In VMCAI, volume 9583 of LNCS,
    pages 41–62. Springer, 2016.
31. Karl Naden, Robert Bocchino, Jonathan Aldrich, and Kevin Bierhoﬀ. A type
    system for borrowing permissions. In POPL, pages 557–570. ACM, 2012.
32. Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. Local reasoning about
    programs that alter data structures. In CSL, volume 2142 of LNCS, pages 1–19.
    Springer, 2001.
33. Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. Program synthesis
    from polymorphic reﬁnement types. In PLDI, pages 522–538. ACM, 2016.
34. Nadia Polikarpova and Ilya Sergey.          Structuring the Synthesis of Heap-
    Manipulating Programs. PACMPL, 3(POPL):72:1–72:30, 2019.
35. Nadia Polikarpova, Jean Yang, Shachar Itzhaky, and Armando Solar-Lezama. En-
    forcing information ﬂow policies with type-targeted program synthesis. CoRR,
    abs/1607.03445, 2016.
36. Xiaokang Qiu and Armando Solar-Lezama. Natural synthesis of provably-correct
    data-structure manipulations. PACMPL, 1(OOPSLA):65:1–65:28, 2017.
37. John C. Reynolds. Separation logic: A logic for shared mutable data structures.
    In LICS, pages 55–74. IEEE Computer Society, 2002.
38. Reuben N. S. Rowe and James Brotherston. Automatic cyclic termination proofs
    for recursive procedures in separation logic. In CPP, pages 53–65. ACM, 2017.
39. Calvin Smith and Aws Albarghouthi. Synthesizing diﬀerentially private programs.
    Proc. ACM Program. Lang., 3(ICFP):94:1–94:29, July 2019.
40. Armando Solar-Lezama. Program sketching. STTT, 15(5-6):475–495, 2013.
168     A. Costea et al.

41. Saurabh Srivastava, Sumit Gulwani, and Jeﬀrey S. Foster. From program veriﬁca-
    tion to program synthesis. In POPL, pages 313–326. ACM, 2010.
42. Sven Stork, Karl Naden, Joshua Sunshine, Manuel Mohr, Alcides Fonseca, Paulo
    Marques, and Jonathan Aldrich. Æminium: A Permission-Based Concurrent-by-
    Default Programming Language Approach. TOPLAS, 36(1):2:1–2:42, 2014.
43. Alexander J. Summers and Peter Müller. Automating deductive veriﬁcation for
    weak-memory programs. In TACAS, volume 10805 of LNCS, pages 190–209.
    Springer, 2018.
44. Emina Torlak and Rastislav Bodı́k. A lightweight symbolic virtual machine for
    solver-aided host languages. In PLDI, pages 530–541. ACM, 2014.




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/
4.0/), which permits use, sharing, adaptation, distribution and reproduction in any
medium or format, as long as you give appropriate credit to the original author(s) and
the source, provide a link to the Creative Commons license and indicate if changes
were made.
   The images or other third party material in this chapter are included in the chapter’s
Creative Commons license, unless indicated otherwise in a credit line to the material. If
material is not included in the chapter’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted use, you will need
to obtain permission directly from the copyright holder.
