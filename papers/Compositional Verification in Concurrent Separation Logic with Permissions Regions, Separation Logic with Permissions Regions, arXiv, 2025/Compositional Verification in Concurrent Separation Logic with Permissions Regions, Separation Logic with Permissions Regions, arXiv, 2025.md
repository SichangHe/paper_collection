                                              Compositional Verification in Concurrent
                                             Separation Logic with Permissions Regions

                                                                          Quang Loc Le

                                                            University College London, United Kingdom
arXiv:2508.18115v2 [cs.LO] 6 Oct 2025




                                              Abstract. Concurrent separation logic with fractional permissions (CSL-
                                              Perm) provides a promising reasoning system to verify most complex
                                              sequential and concurrent fine-grained programs. The logic with strong
                                              and weak separating conjunctions offers a solid foundation for producing
                                              concise and precise proofs. However, it lacks automation and composi-
                                              tionality support. This paper addresses this limitation by introducing a
                                              compositional verification system for concurrent programs that manipu-
                                              late regions of shared memory. The centre of our system is novel logical
                                              principles and an entailment procedure that can infer the residual heaps
                                              in the frame rule for a fragment of CSL-Perm with explicit arithmetical
                                              constraints for memory heaps’ disjointness. This procedure enables the
                                              compositional reasoning for concurrent threads and function calls. We
                                              have implemented the proposal in a prototype tool called CoSl, tested
                                              it with 10 challenging concurrent programs, including those beyond the
                                              state-of-the-art, and confirmed the advantage of our approach.


                                        Keywords: Frame inference, concurrent separation logic, modular verification.


                                        1   Introduction

                                        This paper introduces a novel compositional verification system for concurrent
                                        separation logic with permissions regions (CSL-Perm) [3,8,29], a promising rea-
                                        soning system for analysing heap-alternating concurrent programs. While the
                                        state-of-the-art CSL-Perm, presented in [8], includes both strong separating
                                        conjunction ∗ (to reason about disjointness of heap manipulation) and weak sep-
                                        arating conjunction ⊛ (to reason on shared resources), our system takes a step
                                        further by providing automated and compositional verification. We demonstrate
                                        the effectiveness of our system by applying it to verify 10 challenging fine-grained
                                        algorithms. In the following, we delve into the development of CSL-Perm and
                                        compositional analysis, as well as our motivations and contributions.

                                        Compositional verification for inter-procedures. One of the key challenges in pro-
                                        gram analysis is local reasoning about heap-mutating programs. Separation logic
                                        (SL) [32] provides a well-established framework for local reasoning. It includes
                                        separating conjunction ∗ to specify the disjointness of heap memory: A ∗ B is a
heap that can be split in two separate parts satisfying A and B; each part, A
and B, can be analysed independently and locally via the following frame rule.

                         {P }C{Q}
    (Frame∗ − SL)                           (†: Modify(C ) ∩ FreeVar (F ) = ∅)
                      {P ∗ F }C{Q ∗ F }

This rule reads: The valid Hoare triple {P }C{Q} can be extended to any sepa-
rated symbolic heap F whenever the program C does not modify the free vari-
ables of F . Frame inference technique further advances local reasoning by in-
ferring the frame F automatically. By so doing, it enables the compositional
verification and achieves scalability for inter-procedural analysis [19] (i.e., the
analysis performance is proportional to the number of procedures rather than
the number of procedure calls). Frame inference, the foundation of bi-abduction
[10], has established in academic and industrial settings: The Infer team at Meta
implemented it to catch thousands of bugs in Meta’s codebases [21,27].

Compositional verification for concurrent threads. There have been some pre-
liminary efforts to transfer compositional verification to concurrency world using
concurrent separation logic (CSL) [33]. CSL extends SL to reason about coarse-
grained programs with concurrent threads (those include semaphores, conditional
critical regions or monitors). In those programs, each thread owns a separate por-
tion of resources. CSL proposed to utilise the separating conjunction to specify
separated ownership of resources: P1 ∗ P2 is a resource whose ownership can be
split into two parts owned by P1 and P2 separately. Program analysis can obtain
the thread-modular reasoning via the following inference rule.

                        {P1 }C1 {Q1 }      {P2 }C2 {Q2 }
(Concurrency − CSL)                                      Non-interference condition
                          {P1 ∗ P2 }C1 ||C2 {Q1 ∗ Q2 }

The rule reads: If C1 and C2 are non-interference concurrent processes (i.e., C1
does not modify free variables in P2 and Q2 and vice versa), then we can analyse
these threads independently in the separated ownership P1 and P2 and combined
their analysis results Q1 and Q2 afterwards. However, the rule above does not
work for fine-grained programs in which threads interferes each other (e.g., a
program with two threads sharing read-only variables).
    To support concurrent fine-grained programs, Bornat et at. [3] presented
the first proposal of CSL-Perm. They introduced fractional permission over
shared heaps, e.g., Aπ is a heap A which owns π permission. If a thread owns
full permission over a resource, it could modify it; otherwise, it has read-only
permission. Furthermore, the logic specifies shared heaps using weak separating
conjunction ⊛ (where it is usually written as ∗). For instance, A0.5 ⊛ A0.5 means
A divides into two parts, each owning 0.5 permissions on A. It also introduces
(Frame⊛) and (Concurrency) by replacing ∗ with ⊛ in rules (Frame∗ − SL) and
(Concurrency − CSL) to reason about shared heaps in concurrent fine-grained
programs. However, this logic cannot specify heaps’ disjointness precisely; for
instance, essential entailments such as A0.5 ∗ B 0.5 |= (A ∗ B)0.5 is valid in CSL


                                        2
but A0.5 ⊛B 0.5 |= (A⊛B)0.5 is false in CSL-Perm. Consequently, it can support
neither coarse-grained nor most sequential heap-manipulating programs.
    To bridge the gap of CSL-Perm [3], Le et al. presented an ad-hoc fix to
reason on the disjointness [29]. However, this fix only works for precise formu-
las [6]. Recently, Brotherston et al. introduced SLLP , a unified separation logic
with both strong separating conjunction ∗ and and weak separating conjunc-
tion ⊛, that can reason about both interfered threads, disjointness of threads
and sequential heap-manipulating programs [8]. SLLP includes heap labels and
fractional permissions, e.g., (α ∧ A)π is a heap A which has label α and owns
π permission, and novel logical principles to retain the heaps’ disjointness when
switching between ∗ and ⊛. However, while this logic demonstrated such a prin-
ciple for identical heap formulas, i.e., (α ∧ A)π1 ⊛ (α ∧ A)π2 |= (α ∧ A)π1 ⊕π2 ,
it did not show those principles for arbitrary formulas. Hence, a proof system
based on SLLP might not be as strong as the authors had expected. Moreover, a
study on a frame inference procedure in SLLP , which is essential for automation
and compositional reasoning, is still missing. Since the two conjunctions ∗ and ⊛
may be alternately nested, developing a frame inference procedure on this logic
is non-trivial. Lastly, beside of (Frame⊛) for ⊛, SLLP includes another frame rule
(Frame∗) for ∗. Another unanswered question is how the analysis could efficiently
decide which frame rule could be applied at a program point.
Contributions. This paper addresses the aforementioned challenges. We de-
velop a compositional verification with a frame inference procedure for SLaLP , an
analogy of SLLP [8]. In our logic, we write @α Aπ for a heap A which has label α
and owns π permission and introduce arithmetical operators over heap labels α
to keep track of the heaps’ disjointness. These operators are essential to support
both frame rules. Moreover, we make the following primary contributions.

 – We present new distribution principles that retain disjointness over arbitrary
   formulas so that our system can transform back and forth between the two
   separating conjunctions.
 – We propose a frame inference procedure for SLaLP that implements the distri-
   bution principles via inference rules. The new principles enable our reasoning
   system to be more precise than the one in [8], as it could recover ∗ from ⊛.
 – We introduce a compositional verification algorithm that supports both
   thread- and procedure-modular reasoning. Our algorithm applies the frame
   rule with the weak separating conjunction and uses the distribution prin-
   ciples to recover strong separating conjunctions. By doing so, our system
   can efficiently support both frame rules. We implement a verifier prototype,
   CoSl - the first implemented verification system in CSL-Perm - to our best
   knowledge, test it with challenging fine-grained programs, and confirm that
   CoSl goes beyond the capability of state-of-the-art logical systems [3,8,29].

Outline The rest of this paper is organised as follows. Sect. 2 illustrates our work
through examples. Sect. 3 shows SLaLP syntax and semantics. Sect. 4 proposes
the logical principles of our frame inference (proofs are in Appendix). Sect. 5
introduces the frame inference procedure with proof rules and a search algorithm.


                                         3
We present the compositional verification algorithm in Sect. 6. Sect. 7 discusses
the implementation and evaluation. Sect. 8 shows related work and concludes.


2   Overview and Illustrative Examples

In this section, we explain basic concepts, including distribution principles, frame
inference procedure, and modular verification through examples.

Distribution principles. In practice, sequential code and concurrent code are
often mixed together. When entering concurrent code from sequential code, an
analysis may split heap permissions on shared resources with multiple threads,
e.g., using the distribution principle @α A ∗ @β B |= @α A ⊛ @β B to distribute
∗ over ⊛ [8]. Later, when joining the threads and the permissions, the analysis
may want to recover the disjointness for a stronger post-state. However, @α A ⊛
@β B ̸|= @α A ∗ @β B as we have lost information when applying the previous
distribution. In this paper, we propose new logical principles to retain the heaps’
disjointness. For instance, we fix the above distribution as @α A ∗ @β B = @α A ⊛
@β B ∧ α⊥β where α⊥β is a pure/non-heap formula that specifies the heaps’
disjointness; it enables the analysis to recover the disjointness.

Frame inference. We propose a procedure, called FrInfer, to solve the following
frame inference problem:
        Given: A and goal G
        To find: a collection of frame assertions F such that A |= G ⊛ F

where F includes the residual heap (of A) and arithmetical constraints that
instantiate those logical variables and existentially quantified variables in G with
those terms in A, and ⊛ is the weak separating conjunction. FrInfer naturally
automates the frame rule with weak separating conjunction. Moreover, FrInfer
also implements the distribution principles in a function, called ws-norm(A), so
that F includes disjointness constraints that helps transforming G ⊛ F to G ∗ F ,
when applicable. And so, FrInfer can support the automation of the frame
rule with strong separating conjunction as well.
    We illustrate how FrInfer finds frame F1 for the following entailment prob-
           1/2           1/2                           1/2                    1/2
lem: @α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y |= ∃w.@γ x 7→ w. Here, @α x 7→ y, a
shorthand for (@α x 7→ y)1/2 , says that x points to a heap with 1/2 permission,
named α, and its content is y; note that, labels α, β and γ are logical variables.
                                                                        1/2
    Our entailment procedure FrInfer outputs {F1 } with F1 ≡ @β y 7→ nil∧x ̸=
y ∧ α⊥β ∧ γ = α ∧ w = y . FrInfer infers that if we instantiate the logical vari-
able γ with α and the existentially quantified variable w with y (the constraint
in the greyed area shows the instantiation). F1 includes the cell pointed to by
y. Furthermore, α⊥β specifies the heaps’ disjointness and helps to recover the
disjointness whenever F1 is re-combined with the LHS of the above entailment.


                                         4
                                                                        1/2           1/2
   Similarly, given the entailment, referred to as e, @α x 7→ y ∗ @β y 7→ nil ∧ x ̸=
                1/4                                                             1/4           1/2
y |= ∃w.@γ x 7→ w, FrInfer returns {F2 } where F2 ≡ @α x 7→ y ⊛ @β y 7→
nil ∧ x ̸= y ∧ α⊥β ∧ γ = α ∧ w = y. The residual heaps include two cells: while
the cell pointed to by x remains 1/4(= 1/2 − 1/4) permission, the cell pointed
to by y is preserved intact.

Compositional verification. Our verification system, CoSl, verifies a program
bottom-up; it verifies the callees before the caller and split/join threads before
the main thread. It statically executes a program by calculating symbolical con-
straints on values stored in program variables. This execution amounts to the
transformation of the constraints over program statements whose meanings are
given via their abstractions in the form of Hoare triples. For instance Hoare
triple {pre}C{post} is the abstraction of program C with pre-condition pre and
post-condition post, where pre and post are SLaLP formulas.
                      1/4                          1/4
    Suppose {@γ x 7→ w}foo(x){@γ x 7→ w} is valid, let us illustrate how CoSl
verifies the following Hoare triple at a call site of function foo.
          1/2               1/2                                  1/2          1/2
   {@α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y}foo(x){@α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y}

CoSl successfully verifies the triple with the following proof steps.
 1. It invokes FrInfer to find the frame F2 of the entailment e above.
 2. It applies weak frame rule to find the post-state.
                                                 1/4                   1/4
                                       {@γ x 7→ w}foo(x){@γ x 7→ w}
           (Frame⊛)                                                                 (†)
                                       1/4                     1/4
                                  @γ x 7→ w ⊛ F2 foo(x) @γ x 7→ w ⊛ F2

                                     1/4
 3. It applies ws-norm(@γ x 7→ w ⊛ F2 ) to restore the strong separation in the
                                       1/2                 1/2
    post-state and obtain @α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y ∧ α⊥β ∧ γ = α ∧ w = y.
 4. CoSl invokes FrInfer again to prove
                       1/2                 1/2
                @α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y ∧ α⊥β ∧ γ = α ∧ w = y
                                           1/2             1/2
                              |= @α x 7→ y ∗ @β y 7→ nil ∧ x ̸= y
    FrInfer produces {F3 } where F3 ≡ emp ∧ x ̸= y ∧ α⊥β ∧ γ = α ∧ w = y,
    where emp is the empty heap predicate. As so, it concludes the triple is valid.
    We have tested CoSl with several fined-grain concurrent programs including
those in [8,29] and the one in Fig. 1 which is beyond the capability of the existing
systems. Procedure traverse(x, y) traverses and processes data over binary
trees in which traverse(x, y) accesses two sub-trees in parallel. pre and post
in the specification are defined through binary trees as:
emp ∧ x = nil                                                            ⇒ @α0 tree(x)
∃d, l, r, α, β, γ. @α x 7→ d, l, r ∗ @β tree(l) ∗ @γ tree(r) ∧ α0 =α◦β◦γ ⇒ @α0 tree(x)


                                                       5
In pre, @α tree(x)π specifies binary trees, rooted by x, whose heaps are allocated
in a memory labelled with α. Line 3 uses the procedure process to process
the content of pointer x and the tree rooted by y, and on line 4, it recursively
traverses the left and right subtrees in parallel. The specification of process
           π′                        ′                           π′                     ′
is: {@α′ x 7→ d, l, r ∗ @β ′ tree(y)σ }process(x, y){@α′ x 7→ d, l, r ∗ @β ′ tree(y)σ }.
                         π′                                                 ′
(We recap that @α′ x 7→ d, l, r is a shorthand for (@α′ x 7→ d, l, r)π ). Note that,
in our system, the heaps’ disjointness is captured explicitly in the pure part, e.g.,
the heap disjointness constraints α⊥β in pre and post.
    To verify traverse(x, y), CoSl starts with the pre and statically executes
statements in a bottom-up and thread-modular manner. It generates Hoare
triples, where those intermediate states are shown at the bottom half of Fig-
ure 1. For the conditional statement on line 2, it generates the post-state s1 for
the true branch and s2 for the false branch. To verify the true branch, it derives
the triple {s1 }skip{s1 }. After that, it invokes FrInfer to prove s1 |= post. Our
procedure establishes the validity of this entailment and infers the frame, the
residual heap, as emp to show that the program does not leak any resource.
    For the false branch, when encountering the function call of process on line
3, CoSl uses the process’s summary to reason about the call. To derive the
state after line 3, CoSl applies the combination of the Consequence and Frame
rules to infer the post-state in the greyed areas as follows.

                                                    {p}process(x,y){q}
                                         (Frame⊛)
                 s2 |= p ⊛ F                    {p ⊛ F }process(x,y){q ⊛ F }
     (Conseq)                                        n       o
                                    {s2 }process(x,y) q ⊛ F

This proof rule reads in a bottom-up and left-right manner. Starting from s2
in the conclusion, in the left premise, it invokes FrInfer to infer the frame F
that is not used by the precondition p of the procedure process. After that, the
frame rule in the right-hand side premise is applied, and F is combined with
postcondition q before normalising the combination to obtain s3 . Concretely,
                                                            π′
CoSl poses the frame inference query s2 |= @α′ x 7→ d, l, r, yielding {F } with
F ≡ @α2 tree(l)π ∗ @α3 tree(r)π ∗ @β tree(y)σ ∧ α⊥β ∧ x ̸= nil ∧ α = α1 ◦α2π ◦α3π ∧ e
where e is an instantiation for logical and existentially quantified variables and
e ≡ α′ = α1 ∧ π ′ = π.
    To analyse the concurrent statement on line 4, CoSl applies a combination
of the consequence rule, the concurrency rule and the frame rule to derive s4 .
                                               {pre1 }C1 {post1 }       {pre2 }C2 {post2 }
                               (Concurrency)
                                                 {pre1 ⊛ pre2 }C1 ||C2 {post1 ⊛ post2 }
                                 (Frame⊛)
 s3 |= pre1 ⊛ pre2 ⊛ F                      {pre1 ⊛ pre2 ⊛ F }C1 ||C2 {post1 ⊛ post2 ⊛ F }
                                          n                    o
                              {s3 }C1 ||C2 post1 ⊛ post2 ⊛ F

In this derivation, C1 = traverse(x->l, y) and C2 = traverse(x->r, y);
they are recursive calls in the left thread and the right thread, respectively. To
reason about recursion, CoSl uses the summaries of callees as hypotheses i.e.,


                                              6
1: traverse(x, y) {
    {pre: @α tree(x)π ∗ @β tree(y)σ ∧ α⊥β}
2: if (x == null) { return; /*s1 : @α tree(x)π ∗ @β tree(y)σ ∧ α⊥β ∧ x = nil*/ }
    //s2 : @α tree(x)π ∗ @β tree(y)σ ∧ α⊥β ∧ x ̸= nil
3: process(x, y); //s3
4: traverse(x->l, y);              traverse(x->r, y);
5: /*s4 */}
    {post: @α tree(x)π ∗ @β tree(y)σ ∧ α⊥β}
           π
s3 :@α1 x 7→ d, l, r∗@α2 tree(l)π ∗@α3 tree(r)π ∗@β tree(y)σ ∧ α⊥β ∧ x̸=nil ∧ α=α1 ◦α2π ◦α3π
           π
s4 :@α1 x 7→ d, l, r ∗ (@α2 tree(l)π ∗ @β tree(y)σ1 ) ⊛ (@α3 tree(r)π ∗ @β tree(y)σ2 )
                                                                                       

      ∧α⊥β ∧ x ̸= nil ∧ α = α1 ◦α2π ◦α3π ∧ σ = σ1 ⊕σ2

    Fig. 1. Concurrent tree traversal with derived program states s1 , s2 , s3 and s4
the following triples are valid:
    {pre1 }traverse(x->l, y){post1 }             {pre2 }traverse(x->r, y){post2 }
where pre1 ≡ post1 ≡ @γ2 tree(l)π1 ∗ @β1 tree(y)σ1 ∧ γ2 ⊥β1 and pre2 ≡ post2 ≡
@γ3 tree(r)π2 ∗ @β2 tree(y)σ2 ∧ γ3 ⊥β2 .
     The proof above reads from bottom to up and left to right. Particularly, in the
left-hand side premise, it first generates query s3 |= pre1 ⊛ pre2 , where pre1 ⊛ pre2
                                                                π
results from the concurrency rule. FrInfer returns {@α1 x 7→ d, l, r ∧ α⊥β ∧ x ̸=
               π    π
nil ∧ α = α1 ◦α2 ◦α3 ∧ σ = σ1 ⊕ σ2 ∧ e} where e is an instantiation for logical and
quantified variables and e ≡ γ2 = α2 ∧γ3 = α3 ∧π1 = π∧π2 = π∧β1 = β∧β2 = β.
After that, by applying the frame rule, frame F is conjoined with post1 ⊛ post2 ,
the post of the concurrency rule, to obtain the post of the conclusion. Afterwards,
this post is normalised to obtain s4 . We remark that the work presented in [8]
does not maintain the disjointness in frame assertions and could not derive s4 on
line 5. Hence, verification of this program is beyond its capability. Finally, CoSl
derives the triple {s4 }skip{post} and the query s4 |= post yielding {emp}. As
such, it concludes the entailment is valid and the program complies the spec.


3    SLaLP : CSL with Labels, Permissions, and Arithmetic
We assume Var and LVar as (countably infinite) sets of program variables and
logical variables, respectively, and Val as a set of values. We presume Var and
LVar are disjoint (i.e., Var∩LVar = ∅). Label is a subset of LVar which are variables
for heap labels. nil is a special variable in Var, and we overload nil as a special
value in Val. Loc is a set of heap (memory) locations such that Loc ⊎ {nil} ⊆ Val.
    To model shared regions, we define a permission algebra as follow. We assume
a tuple ⟨Perm, ⊕, ⊗, ⊤⟩, where Perm is a set of permissions, ⊤ is the greatest per-
mission, ⊕ is a partial binary function on Perm, and ⊗ is a total binary function
on Perm. ⟨Perm, ⊕⟩ forms a partial cancellative communtative semigroup with
the properties divisibility (∀π ∈ Perm. ∃π1 , π2 ∈ Perm. π = π1 ⊕ π2 ), total per-
misson (∀π ∈ Perm. π ⊕ ⊤ is undefined), no unit (∀π1 , π2 ∈ Perm. π1 ̸= π1 ⊕ π2 ),
and distribution (∀π, π1 , π2 ∈ Perm. (π1 ⊕ π2 ) ⊗ π = (π1 ⊗ π) ⊕ (π2 ⊕ π)).


                                             7
   We define formulas of SLaLP by the grammar:

Φ ::= true | A | @α A | Φ ∨ Φ                              (formula)
A ::= κ ∧ p | ∃x. A                                        (symbolic heap)
κ ::= emp | x 7→ y | P (x) | κ ∗ κ | κ ⊛ κ | κΠ | @α κ     (spatial)
p ::= ϕ = ϕ | ϕ ̸= ϕ | ϕ | Π = Π | l = l | l⊥l | p ∧ p     (pure/non-heap constraints)
ϕ ::= x | k | ϕ + ϕ                                        (arithmetic)
Π ::= π | Π ⊕ Π | Π ⊗ Π                                    (permission)
 l ::= α | l ◦ l | l ◦ l | lΠ                              (label)

where x ranges over Var, π over Perm, P over Pred, α over Label and x, y over
tuples of variables of length matching the arity of the predicate symbol P .
                      π
    We write @α x 7→ y for (@α x 7→ y)π , and ϕ ̸= ϕ for ¬(ϕ = ϕ). Inductive
predicates are defined by collection of rules each of which is of the form: Φ ⇒
P (x). We use Γ to denote a user-defined system of inductive definitions. For
instance, we define predicate lseg(x,y), that captures list segments, as follows.

       emp ∧ x = y                                        ⇒ @α lseg(x,y)
       ∃q, β, γ.@β x7→q ∗ @γ lseg(q,y) ∧ x ̸= y ∧ α = β◦γ ⇒ @α lseg(x,y)

   We write F V (Φ) to denote the set of free variables in Φ. Label α and per-
mission π are logical variables. The transformation of a formula with constant
permissions into an equivalent formula with logical variables is straightforward.
    We define a stack as a map s : Var → Val; a p-heap, a heap-with-permissions,
a finite partial function h : Loc ⇀fin Val × Perm that maps locations to value-
permission pairs; and valuation a function ρ assigning a single p-heap ρ(α) to
each label α ∈ Label. The satisfaction relation s, h, ρ |= Φ, where s is a stack, h
is a p-heap, ρ is a valuation and Φ is a formula.
    dom (h) denotes the domain of h i.e., the set of heap addresses on which
h is defined. Two p-heaps h1 and h2 are disjoint if dom (h1 ) ∩ dom (h2 ) = ∅;
furthermore, they are compatible if, for all ℓ ∈ dom (h1 ) ∩ dom (h2 ), h1 (ℓ) =
(v, π1 ) and h2 (ℓ) = (v, π2 ) and π1 ⊕ π2 is defined. The multiplication π · h of
a p-heap h by permission π is defined by extending ⊗ pointwise: (π · h)(ℓ) =
(v, π ⊗ π ′ ) ⇔ h(ℓ) = (v, π ′ ). Strong composition h1 ◦ h2 is standard: 1) if
dom (h1 ) ∩ dom (h2 ) = ∅, (h1 ◦ h2 )(ℓ) = hi (ℓ) with ℓ ∈ dom (hi ) \ dom (h3−i ),
i ∈ {1, 2}; and 2) undefined otherwise. Weak composition h1 ◦ h2 is defined:
(h1 ◦ h2 )(ℓ) is 1) hi (ℓ), if ℓ ∈ dom (hi ) \ dom (h3−i ); 2) (v, π1 ⊕ π2 ), if h1 (ℓ) =
(v, π1 ), h2 (ℓ) = (v, π2 ) and π1 ⊕ π2 is defined; and 3) undefined otherwise. We
define ρ(l1 ◦l1 ) = ρ(l1 ) ◦ ρ(l2 ), ρ(l1 ◦l1 ) = ρ(l1 ) ◦ ρ(l2 ), and ρ(lπ ) = π · ρ(l).
    We also assume each predicate symbol P of arity n is given a fixed semantics
JP K ∈ (Valn × Heap), like the one in [7], where Heap is the set of all p-heaps.
   The semantics is defined by structural induction on Φ and is shown in App
A. The semantics of entailment A |= B, where A and B are formulas, is: For
any s, h, and ρ, if s, h, ρ |= A then s, h, ρ |= B.


                                           8
4    Logical Principles of SLaLP

We present logical entailments that show the connection between the strong
∗ and weak ⊛ separating conjunctions. Our system uses these entailments to
distribute and transform formulas back and forth between the two conjunctions.
    These entailments set the foundations for the reasoning about multi-threads.
When encountering concurrent code, an analysis must split the resources the
threads share i.e., weakening the strong separating conjunction ∗ to the weak
separating conjunction ⊛. Then, after exiting the concurrency zone, the analysis
might need to strengthen the resources combined from these threads i.e., re-
introducing the strong conjunction ∗ from the weak conjunction ⊛. We propose
entailment procedure FrInfer and another procedure ws-norm(A) to composi-
tionally reason about multi-threads. While FrInfer uses concurrency rules to
split resources for predicate matching, which is essential for an entailment pro-
cedure in separation logic, ws-norm(A) strengthens program state A, the output
of the procedure FrInfer, to restore strong separating conjunctions ∗.
    In the following, we discuss two kinds of distributions: ∗ and ⊛ distribution
and permission distribution. While the former shows how to distribute the two
conjunctions over multiple heap regions, the latter presents how to distribute
permissions over a single heap region. Along the way, we describe normalisation
operators used through these principled entailments.

 ∗ and ⊛ Distribution. Intuitively, using these principled entailments to dis-
tribute strong separating conjunctions over weak ones, our system does not dis-
card the disjointness fact; instead, it keeps this fact as pure formulas i.e., through
those pure constraints over heap nominals. In so doing, our system can deduce
stronger program states such that at some point during the analysis, it can
soundly revert the weak separating conjunction to the original form. Lemma 4.1
formalises the results. We present the proofs of our results in Appendix.

Lemma 4.1 (∗ and ⊛ Distribution). For all A, B, C and D, and nominals
α, β, γ and ξ

        (@α A ⊛ @β B) ∗ (@γ C ⊛ @ξ D)
                   |= (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D) ∧ (α◦β)⊥(γ◦ξ)              (⊛/∗)
        (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D) ∧ (α◦β)⊥(γ◦ξ)
                   |= (@α A ⊛ @β B) ∗ (@γ C ⊛ @ξ D)                            (∗/⊛)

   Lemma 4.1 shows how our system distributes back and forth between the two
conjunctions ∗ and ⊛. Before entering threads, (⊛/∗) is used to divide heaps into
multiple shared regions, each used by a thread, and (∗/⊛) is for strengthening
the combined heaps after exiting the concurrent code. As shown in this Lemma,
the pure constraint α⊥β in (⊛/∗) enables our systems to strengthen the weak
conjunction ⊛ to the strong conjunction ∗ in (∗/⊛). By taking B ≡ C ≡ emp,


                                          9
we obtain a weak-strong separation conversion principle as
                             @α A ∗ @ξ D |= @α A ⊛ @ξ D ∧ α⊥ξ               (⊛/∗)
                   @α A ⊛ @ξ D ∧ α⊥ξ |= @α A ∗ @ξ D                         (∗/⊛)

Permission Distribution. Our system uses Lemma 4.2 to split and join permis-
sions. Unlike [8], our principles support permissions as logical variables.
Lemma 4.2 (Permission Split and Join). For all formula A, nominal α
and permissions π1 , π2 such that π1 ⊕ π2 is defined:
                      (@α A)π1 ⊕π2 |= (@α A)π1 ⊛ (@α A)π2                (⊛ Split)
                    π1           π2                 π1 ⊕π2
             (@α A)      ⊛ (@α A)       |= (@α A)                        (⊛ Join)

Procedure ws-norm(A). We now describe how procedure ws-norm(A) works. To
transform the weak separating conjunction to strong one, ws-norm(A) exhaus-
tively applies the following two scenarios into formula A:
1. It applies (∗/⊛) and then (⊛ Join) into those sub-formulas of the form (Aπ1 ∗
   B) ⊛ (Aπ2 ∗ C) as: ws-norm((Aπ1 ∗ B) ⊛ (Aπ2 ∗ C)) = Aπ1 ⊕π2 ∗ (B ⊛ C)
2. It applies (∗/⊛) into those sub-formulas (@α A ⊛ @β B) ∧ α⊥β as:
          ws-norm((@α A ⊛ @β B) ∗ C ∧ α⊥β) = (@α A ∗ @β B) ∗ C ∧ α⊥β
    Similarly, ws-norm((@α A ⊛ @β B) ⊛ C ∧ α⊥β) = (@α A ∗ @β B) ⊛ C ∧ α⊥β.

Procedures inward and inward*. Finally, we present procedures that distribute
nested permissions over a heap region with individual weak or strong separat-
ing conjunctions. They are used to normalise a formula after unfolding, i.e., an
inductive predicate is substituted by its definition; while inward is used for the
unfolding in the LHS of an entailment, inward* is for the RHS. They are based
on the following entailments and equivalence.
                               (@α A)π ≡ @απ Aπ                              (@π )
                         π          π    π           π       π   π   π
      @γ (@α A ∗ @β B) ∧ γ = α ◦β ≡ @α A ∗ @β B ∧ γ = α ◦β                   (∗π )
                         π          π    π            π      π   π   π
     @γ (@α A ⊛ @β B) ∧ γ = α ◦β |= @α A ⊛ @β B ∧ γ = α ◦β                   (⊛π )
                               (Aπ1 )π2 |= Aπ1 ⊗π2                            (⊗)
In the above entailments and equivalence, inward transforms the formula in the
LHS into the ones in the RHS. As inward* applies for the RHS of an entailment,
it only uses ∗π to transform the formula for soundness. The next section shows
how FrInfer implements these principles via inference rules.

5   Frame Inference Procedure
Our entailment procedure FrInfer finds a collection of residual heap assertions
F for a given entailment A |= G. These assertions are then used to analyse
programs compositionally. We first describe our FrInfer as a proof search al-
gorithm and inference rules. After that, we elaborate FrInfer with an example.


                                             10
5.1     FrInfer Entailment Algorithm
Given an entailment A |= G, the core of FrInfer is the judgement function
Eval(A, G) that computes a collection of frame assertions F such that F is a
residual heap left over when discharging the entailment. Note that F also includes
some instantiations of logical and existentially quantified variables in G with
some terms in A. Theorem 5.1 describes the soundness of Eval(A, G).
Theorem 5.1 (Soundness).           For all A, G:

                      F ∈ Eval(A, G)     implies   A |= G ⊛ F

The Eval Function We define the function Eval using the inference rules shown
in Fig. 2. Given an entailment A |= G, Eval(A, G) computes a disjunctive set of
frame assertions as follows.
 – Base case: Eval(A, emp ∧ true) =def {A}.
 – Inductive case: For every inference rule in Fig. 2 in the following form:
                           An ▷ Gn         ...      A1 ▷ G1
                                         A ▷ G
      Eval(A, G) takes the conclusion as input and computes the premises as

                   Eval(A, G) =def Eval(A1 , G1 ) ∪ ... ∪ Eval(An , Gn )

    During analysis, the set of frame assertions is conjoined with program states
to form a disjunctive post-state. Our system analyses this state in the same way
with the post-state produced from conditional if b then C1 else C2 com-
mand; the verification is successful when all the disjuncts of this post-state are
verified successfully. Rule Hypothesis eliminates the pure constraints in the RHS.
To discharge p ⇒p p′ , we partition it into two separating entailments: one with-
out labels and another with labels. For the former, we translate it into the
arithmetic satisfiability problem. For the latter, we make use of the following
entailments: p ∧ l |= l and p ∧ (α◦β)⊥(γ◦ξ) |= α⊥γ.
    Rules LU and RU replace an inductive predicate by its definition in the LHS
and RHS, respectively. LU is applied when, under some substitution, the RHS
contains a subformula that is a part of the definition of the inductive predicate.
It is hoped that, after this unfolding, the subformula is matched and subtracted,
thus progressing the proof search. RU is applied similarly but for the RHS.
    Rules M, M∗, M 7→ and M∗ 7→ are used to match subformulas. While rules
M and M∗ match identical subformulas, M 7→ and M∗ 7→ match heap cells
pointed to by the same pointer and instantiate its content’s logical/quantified
variables, if applicable. Moreover, M∗ and M∗ 7→ apply Lemma 4.1 to translate
the strong separating conjunction into the weak one before matching. The sound-
ness of these rules follows the soundness of the frame rule. In particular, when
the system does matching, it generates corresponding equality constraints. The
respective equality constraints are put into the LHS of the premise to instantiate


                                          11
                      A ∧ p ▷ G□G′                                    A′ ▷ G′
(Hypothesis)                               p ⇒p p0          (π)                        A |= G
                   A ∧ p ▷ (G ∧ p0 )□G′                           A ∗ A ′ ▷ Gπ ∗ G ′
                                                                      π


              A □ inward(@α Aπ1 ) ▷ G             ...         A □ inward(@α Aπn ) ▷ G
     (LU)                                               π
                                      A □ @α P (v) ▷ G
                             where ∀i ∈ {1...n}.Ai ⇒ P (v) ∈ Γ
                            A ▷ G □ inward*(@α Aπi )
                   (RU)                                       Ai ⇒ P (v) ∈ Γ
                              A ▷ G □ @α P (v)π
         B ∧ α = α′ ∧ π = π ′ ▷ C                   @β B ∧ α = α′ ∧ π = π ′ ∧ α⊥β ▷ C
  (M)                                     (M∗)
               π                π′                                               ′
        @ α A ⊛ B ▷ @ α′ A           ⊛C                 @α Aπ ∗ @β B ▷ @α′ Aπ □ C
                             B ∧ α = β ∧ π1 = π2 ▷ C[z1 /z2 ] ∧ y = t
                   (M 7→)            π                            π
                            @α x 7→1 y, z1 ⊛ B ▷ ∃z2 . @β x 7→2 t, z2 ⊛ C
                        @β B ∧ α = α′ ∧ π = π ′ ∧ α⊥β ▷ C[z1 /z2 ] ∧ y = t
              (M∗ 7→)
                                 π                                    π′
                        @α x 7→ y, z1 ∗ @β B ▷ ∃z2 . @α′ x 7→ t, z2 □ C
                  @ξ A1 ∧ π = π1 ⊕ π2 ∧ β = α ∧ γ = α ∧ α⊥ξ ▷ B ⊛ C ⊛ G
        (Split ⊛)
                      @α Aπ ∗ @ξ A1 ▷ (@β Aπ1 ∗ B) ⊛ (@γ Aπ2 ∗ C) ⊛ G
            @α1 A1 ∧ α′ = α ∧ β ′ = β ∧ γ ′ = γ ∧ ξ ′ = ξ ∧ (α◦β)⊥(γ◦ξ)⊥α1 ▷ G
(⊛/∗)
        (@α A⊛@β B) ∗ (@γ C⊛@ξ D) ∗ @α1 A1 ▷ (@α′ A∗@β ′ B) ⊛ (@γ ′ C∗@ξ′ D) ⊛ G
                             (@β B ⊛ @γ C) ⊛ A1 ∧ π = π1 ⊕ π2 ▷ G
  (Join ⊛)
               (@α Aπ1 ∗ @β B) ⊛ (@α Aπ2 ∗ @γ C) ⊛ A1 ∧ π = π1 ⊕ π2 ▷ @α Aπ ∗ G
                                          A1 ∧ p ▷ G
(∗/⊛)
        (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D) ⊛ A1 ∧ p ▷ (@α A ⊛ @β B) ∗ (@γ C ⊛ @ξ D) ∗ G
                                    with p = (α◦β)⊥(γ◦ξ)

             Fig. 2. Entailment proof rules for frame inference (□ is ∗ or ⊛).


the variables for the matches of existentially quantified and logical variables in
the RHS of the conclusion (e.g., variables z1 and z2 in these rules). Note that,
due to our normalisation, permission variables are logical; hence, our system
puts their equalities in the LHS of the premise. In contrast, for matching other
variables in the RHS of the conclusion, the system has to show that the LHS
could establish the matches. As such, it puts the equalities (i.e., y = t) into the
RHS of the premise, so our system must prove their validity. For simplicity, these
matching rules include point-to predicates with only two fields. Extension these
rules with other cases is straightforward.

    Rules Split ⊛ and ⊛/∗ split heaps and distribute strong separating conjunc-
tion over the weak one i.e., multiple threads can concurrently share the heaps.
Rather than discarding the disjointness, our system preserves the heap separa-
tion in the pure part. Join ⊛ and ∗/⊛ combine shared heaps and restore strong
conjunction from the weak one by exploiting the disjointness constraints in the
pure part. The soundness of these four rules follows Lemma 4.1 and Lemma 4.2.


                                             12
Proof Search Algorithm Given an entailment A |= G, FrInfer build a forest
of proofs. Initially, it creates a proof tree where the root is A |= G. It marks
this node as an on-going leaf. For each on-going leaf, it attempts to match the
entailment with the conclusion of the inference rules in the following order.

 1. If G ≡ emp ∧ true, mark this node as done with frame {A};
 2. For each atomic pure formula of G, attempt rule Hypothesis;
 3. If A ≡ B π ∧ p and G ≡ C π ∧ p′ , apply rule π
 4. Attempt matching rules M, M∗, M 7→, and M∗ 7→, if possible;
 5. If G is a conjunction of ⊛, match G with the RHS of the conclusion of rule
    Split ⊛, if succeed, apply this rule. Otherwise, try rule ⊛/∗;
 6. If G is a conjunction of ∗, match A with the LHS of the conclusion of rule
    Join ⊛, if succeed, apply this rule. Otherwise, try rule ∗/⊛;
 7. Attempt LU. If it fails, try RU;
 8. Lastly, other rules.

For all the rule, except RU, if a rule can be applied, FrInfer extends the tree
with new on-going leaves each of which is one of its premise. For RU, it clones
a new tree before do the above extension. If no rule applies, FrInfer searches
another proof tree. If it finds a tree with all done leaves, it stops the search and
collects a disjunctive set of frames at the leaves. If there is no remaining tree to
search, it returns an unknown exception.

5.2   Illustrative Example
We elaborate FrInfer using the following entailment.
       π
@α1 x 7→ d, l, r∗@α2 tree(l)π ∗@α3 tree(r)π ∗@β tree(y)σ ∧α⊥β∧x̸=nil∧α=α1 ◦α2 ◦α3
 |= (@γ2 tree(l)π1 ∗@β1 tree(y)σ1 ∧γ2 ⊥β1 )⊛(@γ3 tree(r)π2 ∗@β2 tree(y)σ2 ∧ γ3 ⊥β2 )
   As the RHS is a conjunction of weak separating operators, it applies rule
Split ⊛ to split the permission of tree(y)σ in the LHS and then match them with
the ones in the RHS. By so doing, it obtains the following query and generates
the pure constraints in the greyed area .
       π
@α1 x 7→ d, l, r ∗ @α2 tree(l)π ∗ @α3 tree(r)π ∧ α⊥β ∧ x ̸= nil ∧ α=α1 ◦α2 ◦α3
 ∧ β1 =β∧β2 =β∧σ=σ1 ⊕ σ2 |= (@γ2 tree(l)π1 ∧γ2 ⊥β1 ) ⊛ (@γ3 tree(r)π2 ∧γ3 ⊥β2 )
Next, it attempts rule ⊛/∗ to derive the following entailment
       π
@α1 x 7→ d, l, r ∧ α⊥β ∧ x ̸= nil ∧ α = α1 ◦α2 ◦α3 ∧ β1 =β ∧ β2 =β ∧ σ = σ1 ⊕ σ2
    ∧ γ2 = α2 ∧ γ3 = α3 ∧ α2 ⊥α3 |= emp ∧ γ2 ⊥β1 ∧ γ3 ⊥β2
Finally, it applies rule Hypothesis to remove all pure constraints in the RHS
       π
@α1 x 7→ d, l, r ∧ α⊥β ∧ x ̸= nil ∧ α = α1 ◦α2 ◦α3 ∧ β1 =β ∧ β2 =β ∧ σ = σ1 ⊕ σ2
    ∧γ2 = α2 ∧ γ3 = α3 ∧ α2 ⊥α3 |= emp ∧ true
                                                                 π
    Afterwards, FrInfer returns the frame assertions {@α1 x 7→ (d, l, r) ∧ α⊥β ∧
x ̸= nil∧α = α1 ◦α2 ◦α3 ∧β1 =β ∧ β2 =β ∧ σ = σ1 ⊕ σ2 ∧γ2 =α2 ∧ γ3 =α3 ∧ α2 ⊥α3 }.


                                        13
      Inst ∋ inst ::= skip | [x] := v | func(x, y)            Instructions
                      | x := malloc() | free(x)
     Comm ∋ C ::= inst | x := E | local x.C | x := [y] | C; C
                      | if p then C else C | func(x)||func(x)
                      | with r when B do C                    Statements
    Spec ∋ spec ::= requires A ensures A | spec; spec         Summary
      FDec ∋ fd ::= func(x, y)spec; C | fd; fd                Function declarations
       Prog ∋ P ::= fd                                        Programs

                         Fig. 3. The programming language.
6    Compositional Verification Algorithm
The programming language is shown in Fig. 3. Instructions include skip, heap
store ([x] := y), function call (func(x, y)), memory allocation, and memory dis-
posal. For simplicity, we consider the function has a single call-by-reference pa-
rameter x and a single call-by-value parameter y; extending our system to deal
with other cases would be straightforward. Statements comprise instructions
(inst), assignment (x := E), local variable declaration (local x.C), conditional
statement (if p then C else C), heap load (x := [y]), sequential composition
(C; C), and concurrent statement (func(x)||func(x)). We note that, without
loss of generality, we encode the thread body with a function call to simplify the
presentation about thread modularity. A program P includes a collection of func-
tion declarations. A function declaration is of the form func(x, y)spec; C, with
spec is the function’s summary, and C is a statement implementing the function
body. The summary is a collection of the function’s pre/post specifications.

Verification Algorithm. We describe CoSl as a proof search via predicate trans-
former semantics. This algorithm generates post-states using FrInfer to form
intermediate Hoare triples. CoSl carries around a specification table, T , that as-
sociates each instruction inst with a set of specifications. Concretely, the T (inst)
is a sequence of Hoare triples: {p1 }inst{q1 }, · · · , {pn }inst{qn }. The user sup-
plies these specifications of instructions. Note that the specifications of function
calls are obtained from the function declarations. Presumably, all triples in the
specification table are valid, and CoSl verifies the validity of every function
declaration: It verifies its body code against the user-provided specifications.
    The centre of our algorithm is the function Post(p, C, T ). Intuitively, given a
precondition p, a command C, and a specification table T , Post(p, C, T ) computes
a disjunctive set of post-conditions q, which results from executing C on p. If the
execution fails, it returns an error. To formally define the meaning of function
post, we write T |= {p}C{q} to denote that if the triples in T are valid Hoare
triples, then the triple {p}C{q} is also valid.
Theorem 6.1 (Soundness). For all p, C, T, q:
                  q ∈ Post(p, C, T ) implies T |= {p}C{q}
  Given a function declaration f (x, y) = C and a pre/post specification (pre, post),
CoSl invokes Post(pre, C, T ) to compute a set of poststates q. After that, by the


                                          14
consequence rule, it checks for all such q ∈ Post(pre, C, T ), whether q |= post
holds. If this is the case, it concludes that memory accesses in C are safe and
that implementation complies with the specification (pre, post). Otherwise, for
any q does not entail post, the verification fails. We define the function Post using
the inductive rules shown in Fig. 4. These rules are an analogue of proof rules in
concurrency separation logic [33,5,40] and designed to maintain the soundness of
the verification described in Theorem 6.1. In rule Post(p, inst, T ), y is the pass-
by-value parameter of a function call. By substituting such a parameter with a
fresh variable in the post-condition, our system forgets its value in the outputs.
                       Post(p, C, T ) =def {}        if incons(p) is true
                   Post(p, skip, T ) =def {p}
                 Post(p, x := E, T ) =def {∃x′ . p[x′ /x] ∧ x = E[x′ /x]}
              Post(p, local x .C, T ) =def {∃x′ . q | q ∈ Post(p, C[x′ /x], T )}
                                                          π
                 Post(p, x := [y], T ) =def {ws-norm(y 7→ y ′ ⊛ F [x′ /x] ∧ x = y ′ )
                                                                 π
                                            | F ∈ FrInfer(p, y 7→ y ′ )}
                                                                        1
        Post(p, x := malloc(), T ) =def {p ∧ x = nil; p ∗ ∃L. @β x 7→ L}
Post(p, if b then C1 else C2 , T ) =def Post(p ∧ b, C1 , T ) ∪ Post(p ∧ ¬b, C2 , T )
                                          S
               Post(p, C1 ; C2 , T )q =def {Post(q, C2 , T ) | q ∈ Post(p, C1 , T )}
                     Post(p, inst, T ) =def {ws-norm(b[y ′ /y] ⊛ F ) | {a}inst{b} ∈ T
                                            ∧ F ∈ FrInfer(p, a)}
          Post(p, f (x1 )||g(x2 ), T ) =def {ws-norm((b1 ⊛ b2 ) ⊛ F ) | {a1 }f (x1 ){b1 } ∈ T
                                            ∧ {a2 }g(x2 ){b2 } ∈ T ∧ F ∈ FrInfer(p, a1 ⊛ a2 )}

 Fig. 4. Predicate transformers for program statements (x′ , y ′ , β are fresh variables).

    Function incons(A) checks the inconsistency of A by computing an arith-
metical formula p, which is an over-approximate of A. Given a stack s, s′ ⊃ s
is defined as for all v ∈ dom (s), v ∈ dom (s′ ) and s′ (v) = s(v). p is an over-
approximate of A if there exists s, h, ρ such that s, h, ρ |= A, then there exists
s′ ⊃ s. s′ , h, ρ |= p. Suppose A ≡ ∃w1 , .., wn . κ ∧ ϕ ∧ l, then p ≡ ∃w1 , .., wn . p′ ,
where p′ is computed as (we consider p and p′ as conjunctive sets of subformulas)
          π
 – If x 7→ ∈ κ, then x ̸= nil ∈ p′ .
         π       π
 – If x 7→1 ∗ y 7→2 ∈ κ, then x ̸= y ∈ p′ .
            π1        π
 – If @α x 7→ ⊛ @β y 7→2 ∈ κ and either α⊥β ∈ l or α◦β ∈ l, then x ̸= y ∈ p′ .
 – For permission algebra, we make use of Boyland fractional permission model
   [4] where Perm = {π | π ∈ Q ∧ 0 < π ≤ 1}, ⊤ = 1, ⊕ is + (only defined if
   the result does not exceed 1), and ⊗ is ×. As so, we replace all ⊕ (resp. ⊗)
   in ϕ by + (resp. ×) to obtain ϕ′ and ϕ′ is a conjunct of p′ . Furthermore, if
   any permission π1 + ... + πn ∈ ϕ′ , then 0 < π1 + ... + πn ≤ 1 ∈ p′ .

  The summary of instructions are defined as follows (where β is a fresh label).
                  n         o         n          o n            o
                         1                   1               1
{emp}skip{emp}     @α x 7→ [x] := v @β x 7→ v          @α x 7→ free(x){emp}


                                                15
Note that in rule of x := malloc(), the post-condition describes two cases: x = nil
when the system it out of memory or allocation error and allocation succeeds
with a location assigned to x. The two last rules, memory write and memory
de-allocation, require full permission in the pre-conditions. Further note that
for those rules using entailment procedure FrInfer, CoSl also has to check
the side condition of the frame rule. If either the check fails with an unknown
exception, function Post returns an error. After combining the frame F with
the post-condition, we further note that these rules call procedure ws-norm to
transform weak separation ⊛ into strong separation ∗, when applicable.


7    Implementation and Evaluation

We have implemented FrInfer and CoSl using OCaml and Z3 [14] as a back-
end SMT solver for the arithmetic. Our implementation supports fork(proc,
v)/join(id). A fork takes a procedure name proc and parameters v as inputs,
creates a new thread executing the procedure proc, and returns an identifier
of the newly-created thread. join(id) waits for the thread id to finish its ex-
ecution. For fork, CoSl uses FrInfer to find the frames between the current
program state and the pre-condition of proc. For join, it conjoins using ⊛ (and
then normalize) the current program state with the post-condition of proc.
    Furthermore, we enhance the inference rules in FrInfer by maintaining
a data structure that captures equivalence classes of variables in every pure
formula. For example, with the entailment @α x 7→ nil ∧ x = y ∧ y = z |=
@β z 7→ nil, it embeds the pure formula in the LHS with an equivalence class as
a set {x, y, z}. To apply rule M 7→, FrInfer checks whether the two points-to
predicates of the two side pointed to by the same variable. The equivalence class
of the LHS contains three elements, so it re-arranges the head of the points-to
predicate and tries the following three entailments: @α x 7→ nil ∧ x = y ∧ y = z |=
@β z 7→ nil, @α y 7→ nil ∧ x = y ∧ y = z |= @β z 7→ nil, and @α z 7→ nil ∧ x = y ∧ y =
z |= @β z 7→ nil. Since the two points-to predicates in the last entailment match,
the original entailment @α x 7→ nil ∧ x = y ∧ y = z |= @β z 7→ nil holds.
    We have tested CoSl with 10 challenging fine-grained concurrent programs.
They consist of fork/join benchmarks taken from [24] and programs with com-
plex heap sharing within list segments or binary trees from [8,29]. We augment
parameters of each procedure in the latter set of benchmarks to ensure the ne-
cessity of frame inference during the verification shared threads. Furthermore, to
increase the complexity of the heap-sharing, we extend the later set in two ways.
Firstly, we rewrite the program and its specification using data structures with
pure properties like size of lists/trees, boundaries, and maximum. For instance,
instead of traversing a binary tree, we rewrite the program to count the number
of cells allocated in the tree. Secondly, to test how well our system can han-
dle nested separations, in some procedures, we add additional parameters which
points to weak or strong separating heaps with the original ones. The later set
of benchmarks is beyond the capability of [4,8,24,29].


                                         16
     Table 1. Compositional verification of fine-grained concurrent programs.

    Program/Data Structure(pure properties)        #LoC #LoS #procedure #query
                     fibonacci                       38   8      2        8
 quicksort using singly linked list(size, min, max) 99   24      3        17
 mergesort using singly linked list(size, min, max) 128  22      6        32
                 Singly linked list                  29   8      2        8
              Singly linked list (size)              45  11      3        13
                  Skip list (size)                   63  14      3        18
                Doubly linked list                   29   8      2        8
                    Binary trees                     44  13      3        17
                Binary trees (size)                  57  13      4        23
            Heap trees (size, maxelem)               57  13      4        23

    The experimental results are shown in Table 1. Each line on this table reports
the experiments on one fork/join program or one kind of data structures with
procedures, number of lines of code (#LoC), number of lines of specification
(#LoS, including the definitions of inductive predicates), number of procedure
(#procedure), and number frame inference queries (#query). Each program in-
cludes two procedures check(x) and traverse(x,y). check(x) reads data in a
list (or tree) in parallel. For a list, traverse(x,y) reads data in a thread and
recursively traverses the tail of the list x in another thread. For a binary tree,
traverse(x,y) reads data in both threads and recursively traverses its two sub-
trees in parallel. Each program with size property includes additional procedure
count(x). For a list, count(x) reads data in a thread and recursively counts
the tail of the list x in another thread. For a skip list, count(x) counts cells
in each level by one thread. For a binary tree, count(x) counts cells in the left
and right of the tree x in parallel. On a machine with 4 cores and 8GB RAM:
CoSl verified every program successfully within one minute. The experiments
confirm that the frame inference procedure FrInfer enables CoSl to support
both procedure-modular and thread-modular. Furthermore, CoSl can produce
proofs compositionally and is potential for scalability.


8   Related Work and Conclusion

Our work innovatively extends the reasoning system over SLLP [8]. It surpasses
[8] by introducing modular reasoning using a frame inference procedure and
an implemented compositional analysis algorithm. Furthermore, our principles
on distribution among sharing conjunction ⊛ and separating conjunction ∗ are
more precise than the ones in [8]. These principles help our system to generate
stronger post-states during the verification and thus make CoSl more powerful.
    Many revisions of CSL have been proposed to analyse interference and shared
resources in concurrent fine-grained programs. Their representatives include CSL-
Perm - the family of CSL with permissions regions [3,8,29], CSL+Rely/Guarantee
[41], CaReSL [39], iCAP [37], and Views [16], and “protocol-based” notions of
disjointness in program logic such as FCSL [31] and Iris [23]. CSL-Perm are


                                       17
amenable to automation as they are simpler and more uniform than protocol-
based logics. Furthermore, while a few could support automation (for instance,
SmallfootRG [12] for CSL+Rely/Guarantee, Caper [17] for CAP family, and
Starling [42] for Views), only CSL-Perm has demonstrated the compositional-
ity with a frame inference procedure.
    Our modular verification system for concurrent programs closely relates to
Smallfoot [2], jStar [20], Verifast [22], and ShareInfer [29]. Unlike ours, these
works support CSL with only one separating conjunction and are much simpler
than ours. Smallfoot discussed local reasoning for concurrency in the original
CSL [33]. As the logic reused the separating conjunction to represent the owner-
ship over separating resources, it could be implied that the compositional anal-
ysis might be obtained straightforwardly using the frame inference presented in
[1]. Indeed, such a frame inference was studied in jStar. Furthermore, as shown
in [5] and [3], the ownership transfer paradigm cannot describe passivity in pro-
grams that share read access among threads. Verifast is a mechanised analyser
built on CSL with fractional permission [4]. ShareInfer, a bi-abductive proce-
dure, was based on the logic that revamps the disjointness of permission heap
regions using tree shares. In contrast to ShareInfer, the underlying logic helps
CoSl to reason programs beyond precise formulas. Furthermore, it is a modular
verification, which goes beyond a frame inference procedure. While our system,
like Smallfoot, jStar, and ShareInfer, could be fully automated, we envision ex-
tending our frame inference with abduction [11,13,25,38] and lazy initialization
[34,35] to infer procedure’s and a thread-modular summary. Additionally, we
see potential in enhancing reasoning over inductive predicates with an induc-
tion method, such as cyclic proofs like the one in [26,28]. These future research
directions demonstrate the scalability and adaptability of our system.
    Our work, which develops an automatic verification for concurrent programs,
shares the same motivation with SmallfootRG [12], Starling [42] and Caper [17].
These systems rely on ordinary separation logic solvers (like GRASShopper [36]),
it takes them a high cost to translate concurrent verification conditions. In con-
trast, CoSl builds a solver for SLaLP so that it can discharge the verification
conditions directly and is thus more efficient.
    SmallfootRG is built on an extension of CSL with rely/guarantee and can ver-
ify fine-grained concurrent programs. However, as it is based on the paradigm
of rely/guarantee, it maintains auxiliary global variables. Hence, it could not
preserve the local reasoning, the basis for compositional verification, like ours.
Starling is an instantiation of the Views framework [16]; it computes for each
thread a separating view and then combines them, via a concurrency rule, for
the view of their parent thread. Starling neither supports functional correctness,
frame inference, or modular verification. Caper is based on concurrent abstract
predicates [18], a separation logic with auxiliary guard algebras, shared regions,
and actions. Although it can verify the functional properties of concurrent pro-
grams, unlike ours, the paper did not present a proof system to infer frame
assertions. Therefore, it is unclear how Caper can compositionally reason about
programs. Finally, Diaframe implements a mechanised proof system based on

                                       18
Iris [30]. While its proof rules are based on bi-abduction concept, our system
develop frame inference, the foundation for a bi-abductive inference for SLaLP .

Conclusion We develop foundational principles for the distribution between
strong and weak separating conjunctions. Based on that, we build the frame in-
ference procedure FrInfer and the compositional verifier CoSl. The proposed
principles enable our system to verify fine-grained concurrent programs which
are beyond the current systems. One of our future works is to extend FrInfer
with bi-abduction to infer specifications for procedures and concurrent threads.
Another direction is to explore cyclic proofs [9] for the frame inference problem
in SLaLP to enhance the reasoning on looping programs. We are also interested in
testing the resulting cyclic system with real-world Move smart contracts [15]. Yet
another complementary direction is to study an under-approximation of CSL-
Perm to find concurrency bugs. These works would advance the verification of
presence and absence of bugs in concurrent programs.

References
 1. Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic execution with
    separation logic. In Kwangkeun Yi, editor, Programming Languages and Systems,
    pages 52–68, Berlin, Heidelberg, 2005. Springer Berlin Heidelberg.
 2. Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Smallfoot: Modular au-
    tomatic assertion checking with separation logic. In Frank S. de Boer, Marcello M.
    Bonsangue, Susanne Graf, and Willem-Paul de Roever, editors, Formal Methods
    for Components and Objects, pages 115–137, Berlin, Heidelberg, 2006. Springer
    Berlin Heidelberg.
 3. Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew Parkinson. Per-
    mission accounting in separation logic. In Proceedings of the 32nd ACM SIGPLAN-
    SIGACT Symposium on Principles of Programming Languages, POPL ’05, pages
    259–270, New York, NY, USA, 2005. Association for Computing Machinery. URL:
    https://doi.org/10.1145/1040305.1040327, doi:10.1145/1040305.1040327.
 4. John Boyland. Checking interference with fractional permissions. In Radhia
    Cousot, editor, Static Analysis, pages 55–72, Berlin, Heidelberg, 2003. Springer
    Berlin Heidelberg.
 5. Stephen Brookes. A semantics for concurrent separation logic. In Philippa Gardner
    and Nobuko Yoshida, editors, CONCUR 2004 - Concurrency Theory, pages 16–34,
    Berlin, Heidelberg, 2004. Springer Berlin Heidelberg.
 6. Stephen Brookes. A semantics for concurrent separation logic. Theoretical
    Computer Science, 375(1):227–270, 2007. Festschrift for John C. Reynolds’s
    70th birthday. URL: https://www.sciencedirect.com/science/article/pii/
    S0304397506009248, doi:https://doi.org/10.1016/j.tcs.2006.12.034.
 7. James Brotherston, Richard Bornat, and Cristiano Calcagno. Cyclic proofs of pro-
    gram termination in separation logic. In Proceedings of the 35th Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
    ’08, page 101–112, New York, NY, USA, 2008. Association for Computing Machin-
    ery. doi:10.1145/1328438.1328453.
 8. James Brotherston, Diana Costa, Aquinas Hobor, and John Wickerson. Reasoning
    over permissions regions in concurrent separation logic. In Proceedings of CAV-32,
    Part II, volume 12225 of LNCS, pages 203–224. Springer, 2020.


                                         19
 9. James Brotherston, Quang Loc Le, Gauri Desai, and Yukihiro Oda. Cyclic proofs
    in hoare logic and its reverse, 2025. URL: https://arxiv.org/abs/2504.14283,
    arXiv:2504.14283.
10. Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Com-
    positional shape analysis by means of bi-abduction. In POPL, pages 289–300, 2009.
    doi:10.1145/1480881.1480917.
11. Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Com-
    positional shape analysis by means of bi-abduction. J. ACM, 58(6):26, 2011.
12. Cristiano Calcagno, Matthew Parkinson, and Viktor Vafeiadis. Modular safety
    checking for fine-grained concurrency. In Hanne Riis Nielson and Gilberto Filé,
    editors, Static Analysis, pages 233–248, Berlin, Heidelberg, 2007. Springer Berlin
    Heidelberg.
13. Christopher Curry, Quang Loc Le, and Shengchao Qin. Bi-abductive infer-
    ence for shape and ordering properties. In 2019 24th International Conference
    on Engineering of Complex Computer Systems (ICECCS), pages 220–225, 2019.
    doi:10.1109/ICECCS.2019.00031.
14. Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In C. R. Ra-
    makrishnan and Jakob Rehof, editors, Tools and Algorithms for the Construction
    and Analysis of Systems, pages 337–340, Berlin, Heidelberg, 2008. Springer Berlin
    Heidelberg.
15. David Dill, Wolfgang Grieskamp, Junkil Park, Shaz Qadeer, Meng Xu, and Emma
    Zhong. Fast and reliable formal verification of smart contracts with the move
    prover. In Dana Fisman and Grigore Rosu, editors, Tools and Algorithms for
    the Construction and Analysis of Systems, pages 183–200, Cham, 2022. Springer
    International Publishing.
16. Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew Parkinson,
    and Hongseok Yang. Views: Compositional reasoning for concurrent programs. In
    Proceedings of the 40th Annual ACM SIGPLAN-SIGACT Symposium on Princi-
    ples of Programming Languages, POPL ’13, pages 287–300, New York, NY, USA,
    2013. Association for Computing Machinery. doi:10.1145/2429069.2429104.
17. Thomas Dinsdale-Young, Pedro da Rocha Pinto, Kristoffer Just Andersen, and
    Lars Birkedal. Caper - automatic verification for fine-grained concurrency. In
    Hongseok Yang, editor, Programming Languages and Systems - 26th European
    Symposium on Programming, ESOP 2017, Held as Part of the European Joint
    Conferences on Theory and Practice of Software, ETAPS 2017, Uppsala, Swe-
    den, April 22-29, 2017, Proceedings, volume 10201 of Lecture Notes in Com-
    puter Science, pages 420–447. Springer, 2017. URL: https://doi.org/10.1007/
    978-3-662-54434-1_16, doi:10.1007/978-3-662-54434-1\_16.
18. Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson,
    and Viktor Vafeiadis. Concurrent abstract predicates. In Theo D’Hondt, editor,
    ECOOP 2010 – Object-Oriented Programming, pages 504–528, Berlin, Heidelberg,
    2010. Springer Berlin Heidelberg.
19. Dino Distefano, Manuel Fähndrich, Francesco Logozzo, and Peter W. O’Hearn.
    Scaling static analyses at facebook. Commun. ACM, 62(8):62–70, jul 2019. URL:
    https://doi.org/10.1145/3338112, doi:10.1145/3338112.
20. Dino Distefano and Matthew J. Parkinson J. jstar: Towards practical verification
    for java. In OOPSLA ’08, pages 213–226, New York, NY, USA, 2008. ACM.
    doi:10.1145/1449764.1449782.
21. Mark Harman and Peter O’Hearn. From start-ups to scale-ups: Opportunities and
    open problems for static and dynamic program analysis. In 2018 IEEE 18th Inter-


                                         20
    national Working Conference on Source Code Analysis and Manipulation (SCAM),
    pages 1–23, 2018. doi:10.1109/SCAM.2018.00009.
22. Bart Jacobs and Frank Piessens. Expressive modular fine-grained concurrency
    specification. In Proceedings of the 38th Annual ACM SIGPLAN-SIGACT Sympo-
    sium on Principles of Programming Languages, POPL ’11, pages 271–282, New
    York, NY, USA, 2011. Association for Computing Machinery. URL: https:
    //doi.org/10.1145/1926385.1926417, doi:10.1145/1926385.1926417.
23. Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars
    Birkedal, and Derek Dreyer. Iris: Monoids and invariants as an orthogonal basis
    for concurrent reasoning. In Proceedings of the 42nd Annual ACM SIGPLAN-
    SIGACT Symposium on Principles of Programming Languages, POPL ’15, page
    637–650, New York, NY, USA, 2015. Association for Computing Machinery. URL:
    https://doi.org/10.1145/2676726.2676980, doi:10.1145/2676726.2676980.
24. Duy-Khanh Le, Wei-Ngan Chin, and Yong-Meng Teo. An expressive framework
    for verifying deadlock freedom. In Dang Van Hung and Mizuhito Ogawa, editors,
    Automated Technology for Verification and Analysis, pages 287–302, Cham, 2013.
    Springer International Publishing.
25. Quang Loc Le, Cristian Gherghina, Shengchao Qin, and Wei-Ngan Chin. Shape
    analysis via second-order bi-abduction. In CAV, volume 8559, pages 52–68. 2014.
    doi:10.1007/978-3-319-08867-9_4.
26. Quang Loc Le and Xuan-Bach D. Le. An efficient cyclic entailment procedure
    in a fragment of separation logic. In Orna Kupferman and Pawel Sobocinski,
    editors, Foundations of Software Science and Computation Structures, pages 477–
    497, Cham, 2023. Springer Nature Switzerland.
27. Quang Loc Le, Azalea Raad, Jules Villard, Josh Berdine, Derek Dreyer, and Pe-
    ter W. O’Hearn. Finding real bugs in big programs with incorrectness logic. Proc.
    ACM Program. Lang., 6(OOPSLA1), apr 2022. URL: https://doi.org/10.1145/
    3527325, doi:10.1145/3527325.
28. Quang Loc Le, Jun Sun, and Shengchao Qin. Frame inference for inductive en-
    tailment proofs in separation logic. In Dirk Beyer and Marieke Huisman, editors,
    Tools and Algorithms for the Construction and Analysis of Systems, pages 41–60,
    2018.
29. Xuan-Bach Le and Aquinas Hobor. Logical reasoning for disjoint permissions. In
    Amal Ahmed, editor, Programming Languages and Systems, pages 385–414, Cham,
    2018. Springer International Publishing.
30. Ike Mulder, Robbert Krebbers, and Herman Geuvers. Diaframe: automated verifi-
    cation of fine-grained concurrent programs in iris. In Proceedings of the 43rd ACM
    SIGPLAN International Conference on Programming Language Design and Im-
    plementation, PLDI 2022, page 809–824, New York, NY, USA, 2022. Association
    for Computing Machinery. URL: https://doi.org/10.1145/3519939.3523432,
    doi:10.1145/3519939.3523432.
31. Aleksandar Nanevski, Ruy Ley-Wild, Ilya Sergey, and Germán Andrés Delbianco.
    Communicating state transition systems for fine-grained concurrent resources. In
    ESOP, 2014.
32. Peter O’Hearn, John Reynolds, and Hongseok Yang. Local reasoning about pro-
    grams that alter data structures. In Laurent Fribourg, editor, Computer Science
    Logic, pages 1–19, Berlin, Heidelberg, 2001. Springer Berlin Heidelberg.
33. Peter W. O’Hearn. Resources, concurrency and local reasoning. In Philippa Gard-
    ner and Nobuko Yoshida, editors, CONCUR 2004 - Concurrency Theory, pages
    49–67, Berlin, Heidelberg, 2004. Springer Berlin Heidelberg.


                                         21
34. Long H. Pham, Quang Loc Le, Quoc-Sang Phan, and Jun Sun. Concolic testing
    heap-manipulating programs. In Maurice H. ter Beek, Annabelle McIver, and
    José N. Oliveira, editors, Formal Methods – The Next 30 Years, pages 442–461,
    Cham, 2019. Springer International Publishing.


35. Long H. Pham, Quang Loc Le, Quoc-Sang Phan, Jun Sun, and Shengchao Qin.
    Enhancing symbolic execution of heap-based programs with separation logic for
    test input generation. In Yu-Fang Chen, Chih-Hong Cheng, and Javier Esparza,
    editors, Automated Technology for Verification and Analysis, pages 209–227, Cham,
    2019. Springer International Publishing.


36. Ruzica Piskac, Thomas Wies, and Damien Zufferey. Grasshopper. In Erika
    Ábrahám and Klaus Havelund, editors, Tools and Algorithms for the Construc-
    tion and Analysis of Systems, pages 124–139, Berlin, Heidelberg, 2014. Springer
    Berlin Heidelberg.


37. Kasper Svendsen and Lars Birkedal. Impredicative concurrent abstract predi-
    cates. In Zhong Shao, editor, Programming Languages and Systems, pages 149–168,
    Berlin, Heidelberg, 2014. Springer Berlin Heidelberg.


38. Minh-Thai Trinh, Quang Loc Le, Cristina David, and Wei-Ngan Chin. Bi-
    abduction with pure properties for specification inference. In Chung-chieh Shan,
    editor, Programming Languages and Systems, pages 107–123, Cham, 2013. Springer
    International Publishing.


39. Aaron Turon, Derek Dreyer, and Lars Birkedal. Unifying refinement and hoare-
    style reasoning in a logic for higher-order concurrency. In Proceedings of the 18th
    ACM SIGPLAN International Conference on Functional Programming, ICFP ’13,
    page 377–390, New York, NY, USA, 2013. Association for Computing Machinery.
    doi:10.1145/2500365.2500600.


40. Viktor Vafeiadis. Concurrent separation logic and operational semantics. Elec-
    tronic Notes in Theoretical Computer Science, 276:335–351, 2011. Twenty-
    seventh Conference on the Mathematical Foundations of Programming Semantics
    (MFPS XXVII). URL: https://www.sciencedirect.com/science/article/pii/
    S1571066111001204, doi:https://doi.org/10.1016/j.entcs.2011.09.029.


41. Viktor Vafeiadis and Matthew Parkinson. A marriage of rely/guarantee and sep-
    aration logic. In Luı́s Caires and Vasco T. Vasconcelos, editors, CONCUR 2007 –
    Concurrency Theory, pages 256–271, Berlin, Heidelberg, 2007. Springer Berlin.


42. Matt Windsor, Mike Dodds, Ben Simner, and Matthew J. Parkinson. Starling:
    Lightweight concurrency verification with views. In Rupak Majumdar and Vik-
    tor Kunčak, editors, Computer Aided Verification, pages 544–569, Cham, 2017.
    Springer International Publishing.


                                          22
A     Semantics
The semantics is defined by structural induction on Φ as follows.

 s, h, ρ |= emp              ⇔   dom (h) = ∅
 s, h, ρ |= x7→y1 , .., yn   ⇔   dom (h) = {s(x)} and h(s(x)) = (s(y1 ), .., s(yn ))
 s, h, ρ |= P (x)            ⇔   (s(x), h) ∈ JP K
 s, h, ρ |= A1 ∗ A2          ⇔   ∃h1 , h2 . h = h1 ◦ h2 ,s, h1 , ρ |= A1 and s, h2 , ρ |= A2
 s, h, ρ |= A1 ⊛ A2          ⇔   ∃h1 , h2 . h = h1 ◦ h2 ,s, h1 , ρ |= A1 and s, h2 , ρ |= A2
 s, h, ρ |= κ ∧ p            ⇔   s, h, ρ |= κ and s, h, ρ |= p
 s, h, ρ |= Aπ               ⇔   ∃h′ . h = π · h′ and s, h′ , ρ |= A
 s, h, ρ |= @α A             ⇔   h = ρ(α) and s, ρ(α), ρ |= A
 s, h, ρ |= ∃x. A            ⇔   ∃k. s[k ← x], h, ρ |= A
 s, h, ρ |= Φ1 ∨ Φ2          ⇔   s, h, ρ |= Φ1 or s, h, ρ |= Φ2
 s, h, ρ |= l1 = l2          ⇔   ρ(l1 ) = ρ(l2 )
 s, h, ρ |= l2 ⊥l3           ⇔   ρ(l2 ) and ρ(l3 ) are disjoint


B     Proofs of Lemma 4.1
B.1    Proof of (⊛/∗)
Proof. Assume s, h, ρ |= (@α A ⊛ @β B) ∗ (@γ C ⊛ @ξ D), we have h = (ρ(α) ◦
ρ(β)) ◦ (ρ(γ) ◦ ρ(ξ)). This implies ρ(α) ◦ ρ(β)) and ρ(γ) ◦ ρ(ξ) are disjoint.
Consequently, we can infer

                                 s, h, ρ |= (α ◦ β)⊥(γ ◦ ξ)                               (1)

We can also infer that ρ(α) and ρ(γ) are disjoint, ρ(β) and ρ(ξ) are disjoint.
Thus, it implies ρ(α) ◦ ρ(γ) and ρ(β) ◦ ρ(ξ) are defined.
  For any ℓ ∈ dom (h), we do the case split.
 – Case left-1: ℓ ̸∈ dom (ρ(γ) ◦ ρ(ξ)). This means ℓ ̸∈ dom (ρ(γ)) and ℓ ̸∈ dom (ρ(ξ)).
    • Case left-1.1: ℓ ̸∈ dom (ρ(β)), then h(ℓ) = ρ(α)(ℓ).
    • Case left-1.2: ℓ ̸∈ dom (ρ(α)), then h(ℓ) = ρ(β)(ℓ).
    • Case left-1.3: ρ(α)(ℓ) = (v, π) and ρ(β)(ℓ) = (v, π ′ ), then h(ℓ) = (v, π ⊗
      π ′ ).
 – Case left-2: ℓ ̸∈ dom (ρ(α) ◦ ρ(β)). This means ℓ ̸∈ dom (ρ(α)) and ℓ ̸∈ dom (ρ(β)).
    • Case left-2.1: ℓ ̸∈ dom (ρ(ξ)), then h(ℓ) = ρ(γ)(ℓ).
    • Case left-2.2: ℓ ̸∈ dom (ρ(γ)), then h(ℓ) = ρ(ξ)(ℓ).
    • Case left-2.3: ρ(γ)(ℓ) = (v, π) and ρ(ξ)(ℓ) = (v, π ′ ), then h(ℓ) = (v, π ⊗
      π ′ ).
    Now, we re-arrange these cases into the following groups.
 – Group right-1: includes Case left-1.1, and Case left-2.1 : ℓ ̸∈ dom (ρ(β)) and
   ℓ ̸∈ dom (ρ(ξ))
      • Group right-1.1: corresponds to Case left-1.1: ℓ ̸∈ dom (ρ(γ))
      • Group right-1.2: corresponds to Case left-2.1: ℓ ̸∈ dom (ρ(α))


                                              23
 – Group right-2: includes Case left-1.2, and Case left-2.2 : ℓ ̸∈ dom (ρ(α)) and
   ℓ ̸∈ dom (ρ(γ))
      • Group right-2.1: corresponds to Case left-1.2: ℓ ̸∈ dom (ρ(ξ))
      • Group right-2.2: corresponds to Case left-2.2: ℓ ̸∈ dom (ρ(β))
 – Group right-3: includes Case left-1.3, and Case left-2.3: ℓ in the overlapping
   region of dom (ρ(α) ◦ ρ(γ)) and dom (ρ(β) ◦ ρ(ξ))
      • Group right-3.1: ℓ in the overlapping region of dom (ρ(α)) and dom (ρ(β)):
        this group corresponds to Case left-1.3.
      • Group right-3.2: ℓ in the overlapping region of dom (ρ(α)) and dom (ρ(ξ)):
        this group is empty as dom (ρ(α)) and dom (ρ(ξ)) are disjoint.
      • Group right-3.3: ℓ in the overlapping region of dom (ρ(γ)) and dom (ρ(β)):
        this group is empty as dom (ρ(γ)) and dom (ρ(β)) are disjoint.
      • Group right-3.4: ℓ in the overlapping region of dom (ρ(γ)) and dom (ρ(ξ)):
        this group corresponds to Case left-2.3.

Group right-1, Group right-2 and Group right-3 show that h = (ρ(α) ◦ ρ(γ)) ◦
(ρ(β) ◦ ρ(ξ)). This implies

                    s, h, ρ |= (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D)                  (2)

   From (1), (2) we have:

            s, h, ρ |= (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D) ∧ (α◦β)⊥(γ◦ξ)




B.2   Proof of (∗/⊛)

Proof. Assume s, h, ρ |= (@α A ∗ @γ C) ⊛ (@β B ∗ @ξ D) ∧ (α◦β)⊥(γ◦ξ), we have
h = (h1 ◦ h3 ) ◦ (h2 ◦ h4 ) with h1 = ρ(α), h2 = ρ(β), h3 = ρ(γ) and h4 = ρ(ξ).
    As s, h, ρ |= (α◦β)⊥(γ◦ξ), we have h1 ◦ h2 and h3 ◦ h4 are defined, and h1
is disjoint from both h3 and h4 , and h2 is also disjoint from both h3 and h4 .
    For any ℓ ∈ dom ((h1 ◦ h3 ) ◦ (h2 ◦ h4 )), we do the case split.

 – Case left-1: ℓ ̸∈ dom (h2 ◦ h4 ). This means ℓ ̸∈ dom (h2 ) and ℓ ̸∈ dom (h4 ).
    • Case left-1.1: ℓ ̸∈ dom (h3 ). Then, h(ℓ) = h1 (ℓ).
    • Case left-1.2: ℓ ̸∈ dom (h1 ). Then, h(ℓ) = h3 (ℓ).
 – Case left-2: ℓ ̸∈ dom (h1 ◦ h3 ). This means ℓ ̸∈ dom (h1 ) and ℓ ̸∈ dom (h3 ).
    • Case left-2.1: ℓ ̸∈ dom (h4 ). Then, h(ℓ) = h2 (ℓ).
    • Case left-2.2: ℓ ̸∈ dom (h2 ). Then, h(ℓ) = h4 (ℓ).
 – Case left-3: ℓ in the overlapping region of dom (h1 ◦ h3 ) and dom (h2 ◦ h4 ).
    • Case left-3.1: ℓ in the overlapping region of dom (h1 ) and dom (h2 ). As-
      sume h1 (ℓ) = (v, π) and h2 (ℓ) = (v, π ′ ), then h(ℓ) = (v, π ⊗ π ′ ).
    • Case left-3.2: ℓ in the overlapping region of dom (h1 ) and dom (h4 ). This
      case can not happen as h1 and h4 are disjoint.
    • Case left-3.3: ℓ in the overlapping region of dom (h3 ) and dom (h2 ). This
      case can not happen as h3 and h2 are disjoint.


                                       24
      • Case left-3.4: ℓ in the overlapping region of dom (h3 ) and dom (h4 ). As-
        sume h3 (ℓ) = (v, π) and h4 (ℓ) = (v, π ′ ), then h(ℓ) = (v, π ⊗ π ′ ).
    Now, we re-arrange these cases into the following groups.
 – Case right-1: ℓ ̸∈ dom (h3 ◦ h4 ). This means ℓ ̸∈ dom (h3 ) and ℓ ̸∈ dom (h4 ).
   This includes Case left-1.1, Case left-2.1, and Case left-3.1. .
    • Case right-1.1: h(ℓ) = h1 (ℓ) where ℓ ̸∈ dom (h2 ) (this case corresponds
      to Case left-1.1).
    • Case right-1.2: h(ℓ) = h2 (ℓ) where ℓ ̸∈ dom (h1 ) (this case corresponds
      to Case left-2.1).
    • Case right-1.3: h(ℓ) = (v, π ⊗ π ′ ) where h1 (ℓ) = (v, π) and h2 (ℓ) = (v, π ′ )
      (this case corresponds to Case left-3.1).
 – Case right-2: ℓ ̸∈ dom (h1 ◦ h2 ). This means ℓ ̸∈ dom (h1 ) and ℓ ̸∈ dom (h2 ).
   This includes Case left-1.2, Case left-2.2, and Case left-3.4. .
    • Case right-2.1: h(ℓ) = h3 (ℓ) where ℓ ̸∈ dom (h4 ) (this case corresponds
      to Case left-1.2).
    • Case right-2.2: h(ℓ) = h4 (ℓ) where ℓ ̸∈ dom (h3 ) (this case corresponds
      to Case left-2.2).
    • Case right-2.3: h(ℓ) = (v, π ⊗ π ′ ) where h3 (ℓ) = (v, π) and h4 (ℓ) = (v, π ′ )
      (this case corresponds to Case left-3.4).
    Based on the re-arranged cases, we have h = (h1 ◦ h2 ) ◦ (h3 ◦ h4 ). Thus,
s, h, ρ |= (@α A ⊛ @β B) ∗ (@γ C ⊛ @ξ D).


C     Proofs of Lemma 4.2
C.1    Proof of (⊛ Split)
Proof. We prove

                       (@α A)π1 ⊕π2 |= (@α A)π1 ⊛ (@α A)π2                   (⊛ Split)

   Suppose that s, h, ρ |= (@α A)π1 ⊕π2 . We have h = (π1 ⊕π2 )·h′ where s, h′ , ρ |=
(@α A) (1). By semantics of the heap label, we have h′ = ρ(α) and s, h′ , ρ |= A.
And for any ℓ ∈ dom (h), we have h′ (ℓ) = (v, π) (2).
   (1) and (2) imply h(ℓ) = (v, (π1 ⊕ π2 ) ⊗ π).
   And using the permission algebra axiom on distribution in §3 (∀π, π1 , π2 ∈
Perm. (π1 ⊕ π2 ) ⊗ π = (π1 ⊗ π) ⊕ (π1 ⊕ π)), we obtain

                          h(ℓ) = (v, (π1 ⊗ π) ⊕ (π2 ⊗ π))

Now we define h1 and h2 where dom (h1 ) = dom (h2 ) = dom (h) and h1 (ℓ) =
(v, (π1 ⊗ π)) and h2 (ℓ) = (v, (π2 ⊗ π)). Hence, h1 = π1 · h′ (3a), h2 = π2 · h′ (3b),
h = h1 ◦ h2 (3c).
    From (1) and (3a), we have s, h1 , ρ |= (@α A)π1 .
    From (1) and (3b), we have s, h2 , ρ |= (@α A)π2 .
    Combined with (3c) and from the semantics of weak separation, we have
s, h, ρ |= (@α A)π1 ⊛ (@α A)π2 .


                                         25
C.2    Proof of (⊛ Join)
Proof. We prove

                         (@α A)π1 ⊛ (@α A)π2 |= (@α A)π1 ⊕π2                      (⊛ Join)

Suppose that s, h, ρ |= (@α A)π1 ⊛(@α A)π2 . By the semantics of weak separation,
there exists h1 , h2 , h = h1 ◦ h2 such that s, h1 , ρ |= (@α A)π1 and s, h2 , ρ |=
(@α A)π2 .
   Furthermore, we have h1 = π1 · h′1 where s, h′1 , ρ |= (@α A) and h′1 = ρ(α)(1).
Similarly, we have h2 = π2 · h′2 where s, h′2 , ρ |= (@α A) and h′2 = ρ(α)(2).
   From (1) and (2), we have h′1 = h′2 = ρ(α). This gives us h = (π1 ·h′1 ) ◦ (π2 ·h′1 )
.
   For any ℓ ∈ dom (h′1 ) i.e., h′1 (ℓ) = (v, π). Now we define ha and hb where
dom (ha ) = dom (hb ) = dom (h′1 ) and ha (ℓ) = (v, (π1 ⊗ π)) and hb (ℓ) = (v, (π2 ⊗
π)). This gives us ((π1 · h′1 ) ◦ (π2 · h′1 ))(ℓ) = (ha ◦ hb )(ℓ) = (v, (π1 ⊗ π) ⊕ (π2 ⊗ π))
= (v, (π1 ⊕ π2 ) ⊗ π) = ((π1 ⊕ π2 ) · h′1 )(l) (3).
   (1) and (3) give us s, h, ρ |= (@α A)π1 ⊕π2 .


D     Proofs of inward and inward*
D.1    Proof of (@π )
Proof. We prove

                                   (@α A)π ≡ @απ Aπ                                   (@π )

    Suppose that s, h, ρ |= (@α A)π . The semantics of permission regions gives
us: h = π · h′ and s, h′ , ρ |= @α A. Furthermore, the semantics of labels gives us:
h′ = ρ(α) and s, h′ , ρ |= A. Then h = π · ρ(α) = ρ(απ ) and s, h, ρ |= Aπ . This
gives us s, h, ρ |= @απ Aπ , as requested.

D.2    Proof of (∗π )
Proof. First, we prove

                                  (A ∗ B)π ≡ Aπ ∗ B π                                   (a)

    Suppose that s, h, ρ |= (A ∗ B)π . We have h = π · h1 and s, h1 , ρ |= A ∗ B. By
definition of strong separation, h1 = ha ◦ hb and s, ha , ρ |= A, s, hb , ρ |= B. This
gives us s, π · ha , ρ |= Aπ , s, π · hb , ρ |= B π (1).
    h = π · h1 = π · (ha ◦ hb )
    For any ℓ ∈ dom (h1 ) i.e., h1 (ℓ) = (v, π ′ ), we have h(ℓ) = (v, π ⊗ π ′ ).
    We consider two cases.
 1. Case 1: ℓ ∈ dom (ha ) and ℓ ̸∈ dom (hb ). Suppose h1 (ℓ) = ha (ℓ) = (va , π1 ).
    Then, h(ℓ) = (va , π1 ⊗ π) = (π · ha )(ℓ). Since ℓ ̸∈ dom (hb ), h(ℓ) = ((π · ha ) ◦
    (π · hb ))(ℓ)(3).
    (1), (3), and the semantics of strong separation give us s, h, ρ |= Aπ ∗ B π .

                                            26
 2. Case 2: ℓ ∈ dom (hb ) and ℓ ̸∈ dom (ha ). This case is symmetry to Case 1.
   Next, we prove

              @γ (@α A ∗ @β B) ∧ γ = α◦β ≡ @α A ∗ @β B ∧ γ = α◦β                    (b)

    The proof of @γ (@α A ∗ @β B) ∧ γ = α◦β |= @α A ∗ @β B ∧ γ = α◦β is easy.
We show the proof of @α A ∗ @β B ∧ γ = α◦β |= @γ (@α A ∗ @β B) ∧ γ = α◦β.
    Suppose that s, h, ρ |= @α A∗@β B∧γ = α◦β. By the semantics of conjunction,
s, h, ρ |= @α A ∗ @β B (4a) and s, h, ρ |= γ = α◦β (5). Then by strong separating
conjunction, h = h1 ◦h2 and s, h1 , ρ |= @α A and s, h2 , ρ |= @β B. Then h1 = ρ(α),
h2 = ρ(β). Hence h = h1 ◦h2 = ρ(α)◦ρ(β) = ρ(α◦β) = ρ(γ) (6).
    (4a) and (6) give us s, h, ρ |= @γ (@α A ∗ @β B) (4b) (by the semantics of
label). This results and (5) give us s, h, ρ |= @γ (@α A ∗ @β B) ∧ γ = α◦β (by the
semantics of the conjunction).
    Now, for the main result, let s, h and ρ be given. We have

          s, h, ρ |= @γ (@α A ∗ @β B)π ∧ γ = απ ◦β π
        ⇔ s, h, ρ |= @γ ((@α A)π ∗ (@β B)π ) ∧ γ = απ ◦β π         (by (a))
        ⇔ s, h, ρ |= @γ (@απ Aπ ∗ @β π B π ) ∧ γ = απ ◦β π (by (@π ) and ∗)
        ⇔ s, h, ρ |= @απ Aπ ∗ @β π B π ∧ γ = απ ◦β π               (by (b))




D.3    Proof of (⊛π )
Proof. First, we prove

                                (A ⊛ B)π |= Aπ ⊛ B π                                (d)



   Suppose that s, h, ρ |= (A ⊛ B)π . We have h = π · h1 and s, h1 , ρ |= A ⊛ B.
By definition of weak separation, h1 = ha ◦ hb and s, ha , ρ |= A, s, hb , ρ |= B.
This gives us s, π · ha , ρ |= Aπ , s, π · hb , ρ |= B π (1).
   h = π · h1 = π · (ha ◦ hb )
   For any ℓ ∈ dom (h1 ) i.e., h1 (ℓ) = (v, π ′ ), we have h(ℓ) = (v, π ⊗ π ′ ).
   We consider three cases.
 1. Case 1: ℓ ∈ dom (ha ) ∩ dom (hb ) and ha (ℓ) = (v, π1 ), hb (ℓ) = (v, π2 ), h1 (ℓ) =
    (v, π1 ⊕ π2 ). This gives us h(ℓ) = (v, (π1 ⊕ π2 ) ⊗ π).
    And using the permission algebra axiom on distribution in §3, we get h(ℓ) =
    (v, (π1 ⊗ π) ⊕ (π2 ⊗ π)). This implies h = (π · ha ) ◦ (π · hb ) (2).
    (1), (2), and the semantics of weak separation give us s, h, ρ |= Aπ ⊛ B π .
 2. Case 2: ℓ ∈ dom (ha ) and ℓ ̸∈ dom (hb ). Suppose h1 (ℓ) = ha (ℓ) = (va , π1 ).
    Then, h(ℓ) = (va , π1 ⊗ π) = (π · ha )(ℓ). Since ℓ ̸∈ dom (hb ), h(ℓ) = ((π · ha ) ◦
    (π · hb ))(ℓ)(3).
    (1), (3), and the semantics of weak separation give us s, h, ρ |= Aπ ⊛ B π .


                                          27
 3. Case 3: ℓ ∈ dom (hb ) and ℓ ̸∈ dom (ha ). This case is symmetry to Case 2.

   Now, for the main result, let s, h and ρ be given. We have

         s, h, ρ |= @γ (@α A ⊛ @β B)π ∧ γ = απ ◦β π
       ⇒ s, h, ρ |= @γ ((@α A)π ⊛ (@β B)π ) ∧ γ = απ ◦β π          (by (d))
       ⇔ s, h, ρ |= @γ (@απ Aπ ⊛ @β π B π ) ∧ γ = απ ◦β π (by (@π ) and ⊛)
       ⇔ s, h, ρ |= @απ Aπ ⊛ @β π B π ∧ γ = απ ◦β π         (by weakening)


D.4   Proof of (⊗)

Proof. We prove

                     (Aπ1 )π2 |= Aπ1 ⊗π2                                       (⊗)

   Suppose that s, h, ρ |= (Aπ1 )π2 . We have h1 = π2 · h where s, h1 , ρ |= Aπ1 .
Again, We have h2 = π1 · h1 = π1 · π2 · h where s, h2 , ρ |= A (1).
   For any ℓ ∈ dom (h) i.e., h(ℓ) = (v, π), by definition of the multiplication, we
have (π1 · π2 · h) = (v, π ⊗ π1 ⊗ π2 ) (2).
   (1) and (2) give us s, h, ρ |= Aπ1 ⊗π2 .




                                           28
