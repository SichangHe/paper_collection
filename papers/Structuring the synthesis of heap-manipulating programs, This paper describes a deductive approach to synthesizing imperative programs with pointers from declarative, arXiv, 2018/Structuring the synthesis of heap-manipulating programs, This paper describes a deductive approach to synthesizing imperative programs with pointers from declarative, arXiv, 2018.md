                                        Structuring the Synthesis of Heap-Manipulating Programs

                                        NADIA POLIKARPOVA, University of California, San Diego, USA
arXiv:1807.07022v2 [cs.PL] 9 Nov 2018




                                        ILYA SERGEY, University College London, UK
                                        This paper describes a deductive approach to synthesizing imperative programs with pointers from declarative
                                        speciﬁcations expressed in Separation Logic. Our synthesis algorithm takes as input a pair of assertions—a pre-
                                        and a postcondition—which describe two states of the symbolic heap, and derives a program that transforms
                                        one state into the other, guided by the shape of the heap. The program synthesis algorithm rests on the novel
                                        framework of Synthetic Separation Logic (SSL), which generalises the classical notion of heap entailment P ⊢ Q
                                        to incorporate a possibility of transforming a heap satisfying an assertion P into a heap satisfying an assertion
                                        Q. A synthesized program represents a proof term for a transforming entailment statement P { Q, and the
                                        synthesis procedure corresponds to a proof search. The derived programs are, thus, correct by construction, in
                                        the sense that they satisfy the ascribed pre/postconditions, and are accompanied by complete proof derivations,
                                        which can be checked independently.
                                           We have implemented a proof search engine for SSL in a form the program synthesizer called SuSLik. For
                                        eﬃciency, the engine exploits properties of SSL rules, such as invertibility and commutativity of rule applications
                                        on separate heaps, to prune the space of derivations it has to consider. We explain and showcase the use of SSL
                                        on characteristic examples, describe the design of SuSLik, and report on our experience of using it to synthesize
                                        a series of benchmark programs manipulating heap-based linked data structures.

                                        1   INTRODUCTION
                                        Consider the task of implementing a procedure swap(x, y), which swaps the values stored in two
                                        distinct heap locations, x and y. The desired eﬀect of swap can be concisely captured via pre/postcon-
                                        ditions expressed in Separation Logic (SL)—a Hoare-style program logic for specifying and verifying
                                        stateful programs with pointers (O’Hearn et al. 2001; Reynolds 2002):
                                                              {x 7→ a ∗ y 7→ b} void swap(loc x, loc y) {x 7→ b ∗ y 7→ a}                                   (1)
                                           This speciﬁcation is declarative: it describes what the heap should look like before and after exe-
                                        cuting swap without saying how to get from one to the other. Speciﬁcally, it states that the program
                                        takes as input two pointers, x and y, and runs in a heap where x points to an unspeciﬁed value a,
                                        and y points to b. Both a and b here are logical (ghost) variables, whose scope captures both pre- and
                                        postcondition (Kleymann 1999). Because these variables are ghosts, we cannot use them directly to
                                        update the values in x and y as prescribed by the postcondition; the program must ﬁrst “material-
                                        ize” them by readings them into local variables, a2 and b2 (cf. lines 2–3 of the code on the right).
                                        In our minimalistic C-like language, loc denotes untyped 1 void swap(loc x, loc y) {
                                        pointers, and let introduces a local dynamically-typed vari- 2          let a2 = *x;
                                        able. Unlike in C, both formals and locals are immutable (the 3         let b2 = *y;
                                        only mutation is allowed on the heap).                             4    *y = a2;
                                           As a result of the two reads, the ghost variables in the post- 5     *x = b2;
                                        condition can now be substituted with equal program-level 6 }
                                        variables: x 7→ b2 ∗ y 7→ a2. This updated postcondition can
                                        be realized by the two writes on lines 4–5, which conclude our implementation, so the whole program
                                        can now be veriﬁed against the speciﬁcation (1).
                                           Having done this exercise in program derivation, let us now observe that the SL speciﬁcation has
                                        been giving us guidance on what eﬀectful commands (e.g., reads and writes) should be emitted next.
                                        In other words, the synthesis of swap has been governed by the given speciﬁcation in the same way
                                        2018. 2475-1421/2018/11-ART $15.00
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                             Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :2                                                                               Nadia Polikarpova and Ilya Sergey

the proof search is guided by a goal in ordinary logics. In this work, we make this connection explicit
and employ it for eﬃciently synthesizing imperative programs from SL pre- and postconditions.
   Motivation. The goal of this work is to advance the state of the art in synthesizing provably correct
heap-manipulating programs from declarative functional speciﬁcations. Fully-automated program
synthesis has been an active area of research in the past years, but recent techniques mostly targeted
simple DSLs (Gulwani et al. 2011; Le and Gulwani 2014; Polozov and Gulwani 2015) or purely func-
tional languages (Feser et al. 2015; Kneuss et al. 2013; Osera and Zdancewic 2015; Polikarpova et al.
2016). The primary reason is that those computational models impose strong structural constraints
on the space of programs, either by means of restricted syntax or through a strong type system.
These structural constraints enable the synthesizer to discard many candidate terms a-priori, before
constructing the whole program, leading to eﬃcient synthesis.
   Low-level heap-manipulating programs in general-purpose languages like C or Rust lack inherent
structural constraints wrt. control- and data-ﬂow, and as a result the research in synthesizing such
programs has been limited to cases when such constraints can be imposed by the programmer. From
the few existing approaches we are aware of, Simpl (So and Oh 2017) and ImpSynth (Qiu and Solar-Lezama
2017) require the programmer to provide rather substantial sketches of the control-ﬂow structure,
which help restrict the search space; Jennisys by Leino and Milicevic (2012) can only handle func-
tions that construct and read from data structures, but do not allow for destructive heap updates,
which are necessary for, e.g., deallocating, modifying, or copying a linked data structure.
   Key Ideas. Our theoretical insight is that the structural constraints missing from an imperative lan-
guage itself, can be recovered from the program logic used to reason about programs in that language.
We observe that synthesis of heap-manipulating programs can be formulated as a proof search in a
generalized proof system that combines entailment with Hoare-style reasoning for unknown pro-
grams. In this generalized proof system, a statement P { Q means that there exists a program c,
such that the Hoare triple {P} c {Q} holds; the witness program c serves as a proof term for the
statement. In order to be useful, the system must satisfy a number of practical restrictions. First, it
should be expressive enough to (automatically) verify the programs with non-trivial heap manipula-
tion. Second, it should be restrictive enough to make the synthesis problem tractable. Finally, it must
ensure the termination of the (possibly recursive) synthesized programs, to avoid vacuous proofs of
partial correctness.
   In this paper we design such a generalized proof system based on the symbolic heap fragment of
malloc/free Separation Logic1 with inductive predicates, to which we will further refer as just Separa-
tion Logic or SL (O’Hearn et al. 2009; Reynolds 2002). Separation Logic has been immensely success-
ful at specifying and verifying many kinds of heap-manipulating programs, both interactively and
automatically (Appel et al. 2014; Berdine et al. 2011; Charguéraud 2010; Chen et al. 2015; Chin et al.
2012; Chlipala 2011; Distefano and Parkinson 2008; Nanevski et al. 2010; Piskac et al. 2014a), and is
employed in modern symbolic execution tools (Berdine et al. 2005; Rowe and Brotherston 2017). We
demonstrate how to harness all this power for program synthesis, devise the corresponding search
procedure and apply it to synthesize a number of non-trivial programs that manipulate linked data
structures. Finally, we show how to exploit laws of SL and properties of our proof system to prune
the search space and make the synthesis machinery eﬃcient for realistic examples.
   Contributions. The central theoretical contribution of the paper is Synthetic Separation Logic (SSL):
a system of deductive synthesis rules, which prescribe how to decompose speciﬁcations for complex
programs into speciﬁcations for simpler programs, while synthesizing the corresponding computa-
tions compositionally. In essence, SSL is a proof system for a new transformation judgment P { Q| c
1 This nomenclature is due to Cao et al. (2017), who provide it as a rigorous alternative to the folklore notion of classical SL.



   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                    :3

(reads as “the assertion P transforms into Q via a program c”), which uniﬁes SL entailment P ⊢ Q
and veriﬁcation {P} c {Q}, with the former expressible as P { Q| skip.
   The central practical contribution is the design and implementation of SuSLik—a deductive synthe-
sizer for heap-manipulating programs, based on SSL. SuSLik takes as its input a library of inductive
predicates, a (typically empty) list of auxiliary function speciﬁcations, and an SL speciﬁcation of the
function to be synthesized. It returns a—possibly recursive, but loop-free—program (in a minimalistic
C-like language), which provably satisﬁes the given speciﬁcation.
   Our evaluation shows that SuSLik can synthesize all structurally-recursive benchmarks from pre-
vious work on heap-based synthesis (Qiu and Solar-Lezama 2017), without any sketches and in most
cases much faster. To the best of our knowledge, it is also the ﬁrst synthesizer to automatically dis-
cover the implementations of copying linked lists and trees, and ﬂattening a tree to a list.
   The essence of SuSLik’s synthesis algorithm is a backtracking search in the space of SSL deriva-
tions. Even though the structural constraints (i.e., the shape of the heap) embodied in the synthesis
rules already prune the search space signiﬁcantly (as shown by our swap example), a naïve backtrack-
ing search is still impractical, especially in the presence of inductive heap predicates. To eliminate
redundant backtracking, we develop several principled optimizations. In particular, we draw inspi-
ration from focusing proof search (Pfenning 2010) to identify invertible synthesis rules that do not
require backtracking, and exploit the frame rule of SL, observing that the order of rule applications
is irrelevant whenever their subderivations have disjoint footprints.
   Paper outline. In the remainder of the paper we give an overview of the reasoning principles of
SSL, describe its rules and the meta-theory, outline the design and implementation of our synthesis
tool, present the optimizations and extensions of the basic search algorithm, and report on the eval-
uation of the approach on a set of case studies involving various linked structures, concluding with
a discussion of limitations and a comparison to the related work.

2 DEDUCTIVE SYNTHESIS FROM SEPARATION LOGIC SPECIFICATIONS
In Separation Logic, assertions capture the program state, represented by a symbolic heap. An SL as-
sertion (ranged over by symbols P and Q in the remainder of the paper) is customarily represented
as a pair {ϕ; P } of a pure part ϕ and a spatial part P. The pure part (ranged over by ϕ, ψ , ξ , and
χ) is a quantiﬁer-free boolean formula, which describes the constraints over symbolic values (rep-
resented by variables x, y, etc) The spatial part (denoted P, Q, and R) is represented by a collection
of primitive heap assertions describing disjoint symbolic heaps (heaplets), conjoined by the separat-
ing conjunction operation ∗, which is commutative and associative (Reynolds 2002). For example, in
the assertion {a , b; x 7→ a ∗ y 7→ b} the spatial part describes two disjoint memory cells that store
symbolic values a and b, while the pure part states that these values are distinct.
   Our development is agnostic to the exact logic of pure formulae, as long as it is decidable and
supports standard Boolean connectives and equality.2 Our implementation uses the quantiﬁer-free
logic of arrays, uninterpreted functions, and linear integer arithmetic, which is eﬃciently decidable
by SMT solvers, and suﬃcient to express all examples in this paper.
   To begin with our demonstration, the only kinds of heaplets we are going to consider are the empty
heap assertion emp and points-to assertions of the form hx, ιi 7→ e, where x is a symbolic variable or
pointer constant (e.g., 0), ι is a non-negative integer oﬀset (necessary to represent records and arrays)
and e is a symbolic value, stored in a memory cell, addressed via a value of (x + ι).3 In most cases,
the oﬀset is 0, so we will abbreviate heap assertions hx, 0i 7→ e as x 7→ e.
2 We require decidability for making the synthesis problem tractable, but it is not required for soundness of the logic.
3 Further in the paper, we will extend the language of heap assertions to support memory blocks (arrays) with explicit memory

management, as well as user-deﬁned inductive predicates.


                                      Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
  :4                                                                                              Nadia Polikarpova and Ilya Sergey

                 Emp
                   EV (Γ , P, Q) = ∅     ϕ ⇒ψ                                                                                           Emp with c 7 = skip
                                                                                           {x, y, a2, b2} ; {emp} { {emp }
                  Γ ; {ϕ ; emp} { {ψ ; emp} | skip                                                      c6 = c7
                                                                                                   n              o       n             o        Frame
       Read                                                                    {x, y, a2, b2} ;        y 7→ a2        {       y 7→ a2       c6
             a ∈ GV (Γ , P, Q)        y < Vars (Γ , P, Q)                                         c 5 = ∗y = a2; c 6
       Γ ∪ {y } ; [y/a]{ϕ ; hx, ι i 7→ a ∗ P } { [y/a]{ Q } | c                                    n          o n      o                         Write
        Γ ; {ϕ ; hx, ι i 7→ a ∗ P } { { Q } | let y = ∗(x + ι); c              {x, y, a2, b2} ;       y 7→ b2 { y 7→ a2 c 5
                                                                                                        c4 = c5
                                                                                                                                                            Frame
       Write                                                        {x, y, a2, b2} ;
                                                                                       n                    o n                 o
                                                                                           x 7→ b2 ∗ y 7→ b2 { x 7→ b2 ∗ y 7→ a2 c 4
                               Vars (e ) ⊆ Γ
        Γ ; {ϕ ; hx, ι i 7→ e ∗ P } { {ψ ; hx, ι i 7→ e ∗ Q } | c                                c 3 = ∗x = b2; c 4
                                                                                                                                                            Write
             Γ ; {ϕ ; hx, ι i 7→ e ′ ∗ P } {
                                                                                       n                     o n                o
                                                                    {x, y, a2, b2} ;       x 7→ a2 ∗ y 7→ b2 { x 7→ b2 ∗ y 7→ a2 c 3
                                              ∗(x + ι) = e ; c
                 {ψ ; hx, ι i 7→ e ∗ Q }                                                   c 2 = let b2 = ∗y; c 3
                                                                                       n                 o                                                  Read
                  Frame                                                 {x, y, a2} ; x 7→ a2 ∗ y 7→ b { {x 7→ b ∗ y 7→ a2} c 2
                   EV (Γ , P, Q) ∩ Vars (R) = ∅                                                  c 1 = let a2 = ∗x ; c 2
                       Γ ; {ϕ ; P } { {ψ ; Q } | c                                     n                     o                                           Read
                                                                           {x, y } ;       x 7→ a ∗ y 7→ b { {x 7→ b ∗ y 7→ a } c 1
                  Γ ; {ϕ ; P ∗ R } { {ψ ; Q ∗ R } | c

                                                                             Fig. 2. Derivation of swap(x,y) as c 1 .
           Fig. 1. Simplified basic rules of SSL.

   Our programming component (to be presented formally in Sec. 3) is a simple imperative language,
supporting reading from pointer variables to (immutable) local variables (let x = *y), storing values
into pointers (*y = x), conditionals, recursive calls, and pure expressions. The language has no return
statement; instead, a function stores its result into an explicitly passed pointer.

2.1     Specifications for Synthesis
A synthesis goal is a triple Γ ; P { Q, where Γ is an environment, i.e., a set of immutable program
variables, P is a precondition (pre), and Q is a postcondition (post). Solving a synthesis goal means to
ﬁnd a program c and a derivation of the SSL assertion Γ ; P { Q| c. To avoid clutter, we employ the
following naming conventions:
(a) the symbols P, ϕ, and P refer to the goal’s precondition, its pure, and spatial part;
(b) similarly, the symbols Q, ψ , and Q refer to the goal’s postcondition, its pure and spatial part;
(c) whenever the pure part of a SL assertion is true (⊤), it is omitted from the presentation.
In addition to those conventions, we will use the following macros to express the scope and the
quantiﬁcation over variables of a goal Γ ; {P} { {Q}. First, by Vars (A) we will denote all variables
occurring in A, which might be an assertion, a logical formula, or a program. Ghosts (universally-
quantiﬁed logical variables), whose scope is both the pre and the post, are deﬁned as GV (Γ, P, Q) =
Vars (P) \ Γ . Goal existentials are deﬁned as EV (Γ, P, Q) = Vars (Q) \ (Γ ∪ Vars (P)). For instance,
taking Γ = {x }, P = {x , y; x 7→ y}, Q = {x 7→ z}, we have the ghosts GV (Γ, P, Q) = {y}, the
existentials EV (Γ, P, Q) = {z}, and the pure part of the post Q is implicitly true.

2.2     Basic Inference Rules
To get an intuition on how to represent program synthesis as a proof derivation in SSL, consider Fig. 1,
which shows four basic rules of the logic, targeted to synthesize programs with constant memory
footprint (remember that we use P and Q for the entire pre/post in a rule’s conclusion!).
  The Emp rule is applicable when both pre and post’s spatial parts are empty. It requires that no
existentials remains in the goal, and the pure pre implies the pure post (per our assumptions on the
logic, the validity of this implication is decidable, so we can check it algorithmically). Emp has no
synthesis subgoals among the premises (making it a terminal rule), and no computational eﬀect: its
witness program is simply skip.

  Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                         :5

   The Read rule turns a ghost variable a into a program variable y (fresh in the original goal). That is,
the newly assigned immutable program variable y is added to the environment of the sub-goal, and
all occurrences of a are substituted by y in both the pre and post. As a side-eﬀect, the rule prepends
the read statement let y = ∗(x + ι) to the remainder of the program to be synthesized.
   The rule Write allows for writing a symbolic expression e into a memory cell, provided all e’s
variables are program-level. It is customary for this rule to be followed by an application of Frame,
which is SSL’s version of Separation Logic’s frame rule. Here, we show a version of the rule, which
is a bit weaker than what’s in the full version of SSL, and will be generalized later. This rule enables
“framing out” a shared sub-heap R from the pre and post, as long as this does not create new existential
variables. Notice, that unlike the classical SL’s Frame rule by O’Hearn et al. (2001), our version does
not require a side condition saying that R must not contain program variables that are modiﬁed by the
program [to be synthesized]: by removing R from the subgoal, we ensure that the residual program
will not be able to access any pointers from R, because it will be synthesized in a symbolic footprint
disjoint from R, and all local variables in SSL language are immutable.
  Synthesizing swap. Armed with the basic SSL inference rules from Fig. 1, let us revisit our initial ex-
ample: the swap function (1). Fig. 2 shows the derivation of the program using the rules, and should be
read bottom-up. For convenience, we name each subgoal’s witness program, starting from c 1 (which
corresponds to swap’s body). Furthermore, each intermediate sub-goal highlights via gray boxes a
part of the pre and/or the post, which “triggers” the corresponding SSL rule. Intuitively, the goal of
the synthesis process is to “empty” the spatial parts of the pre and the post, so that the derivation
can eventually be closed via Emp; to this end, Read and Write work together to create matching
heaplets between the two assertions, which are then eliminated by Frame.

2.3 Spatial Unification and Backtracking
Now, consider the synthesis goal induced by the following SL speciﬁcation:
                   {x 7→ 239 ∗ y 7→ 30} void pick(loc x, loc y) {x 7→ z ∗ y 7→ z}                                 (2)
   Since z does not appear among the formals or in the precondition, it is treated as an existential.
The postcondition thus allows x and y to point to any value, as long as it is the same value.
   To deal with existentials in the heap, we introduce
                                                                 UnifyHeaps
the rule UnifyHeaps, which attempts to ﬁnd a unifying                         [σ ]R ′ = R
substitution σ for some sub-heaps of the pre and the               ∅ , dom (σ ) ⊆ EV   (Γ, P, Q)
post. The domain of σ must only contain existentials.             Γ ; {P ∗ R } { [σ ] ψ ; Q ∗ R ′ c
For example, applying UnifyHeaps to the spec (2) with             Γ ; {ϕ ; P ∗ R } { ψ ; Q ∗ R ′ c
                                                                                      
                         ′
R , x 7→ 239 and R , x 7→ z results in the sub-                Fig. 3. SSL rule for heap unification.
stitution σ = [z 7→ 239], and the residual synthesis
goal {x, y} {x 7→ 239 ∗ y 7→ 30} { {x 7→ 239 ∗ y 7→ 239},
which can be now synthesized by using the Frame,Write, and Emp rules.
   Due to their freedom to choose a sub-heap (and a unifying substitution), Frame and UnifyHeaps
introduce non-determinism into the synthesis procedure and might require backtracking—a fact also
widely observed in interactive veriﬁcation community (Gonthier et al. 2011; McCreight 2009) wrt. SL
assertions. For instance, consider the spec below:
                   {x 7→ a ∗ y 7→ b} void notSure(loc x, loc y) {x 7→ c ∗ c 7→ 0}                                 (3)
   One way to approach the spec (3) is to ﬁrst read from               void notSure (loc x, loc y) {
x, making a a program-level variable a2 (via Read), then                 *x = y;
                                                                         *y = 0;
use UnifyHeaps and Frame on the x 7→ • heaplets in the                 }

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
  :6                                                                                     Nadia Polikarpova and Ilya Sergey

  SubstLeft                                 StarPartial
              ϕ ⇒x =y                       x + ι , y + ι ′ < ϕ     ϕ ′ = ϕ ∧ (x + ι , y + ι ′ )        Inconsistency
                                                                                                                   ϕ ⇒⊥
   Γ ; [y/x ]{ϕ ; P } { [y/x ]{Q } | c      Γ ; ϕ ′; hx, ι i 7→ e ∗ y, ι ′ 7→ e ′ ∗ P { { Q } c
                                                                                                          Γ ; {ϕ ; P } { { Q } | error
                                            Γ ; ϕ ; hx, ι i 7→ e ∗ y, ι ′ 7→ e ′ ∗ P { { Q } c
                                                
           Γ ; {ϕ ; P } { { Q } | c

                                                    Pick                                            UnifyPure
    SubstRight                                             y ∈ EV (Γ, P, Q)                                    [σ ]ψ ′ = ϕ ′
               x ∈ EV (Γ, P, Q)
                                                     Vars (e) ∈ Γ ∪ GV (Γ, P, Q)                      ∅ , dom (σ ) ⊆ EV (Γ, P, Q)
        Σ; Γ ; { P } { [e/x ]{ψ , Q } | c
                                                     Γ ; {ϕ ; P } { [e/y]{ψ ; Q } | c                    Γ ; { P } { [σ ]{ Q } | c
       Σ; Γ ; { P } { {ψ ∧ x = e; Q } | c
                                                                                                    Γ ; ϕ ∧ ϕ ′; P { ψ ∧ ψ ′ ; Q c
                                                                                                                      
                                                        Γ ; {ϕ ; P } { {ψ ; Q } | c


                  Fig. 4. Selected SSL rules for reasoning with pure constraints in the synthesis goal.

pre/post, substituting the existential c by a2. That, however, leaves us with an unsolvable goal
{x, y, a2} {y 7→ b} { {a2 7→ 0}. Hence we have to backtrack, and instead unify c with y, eventu-
ally deriving the correct program notSure .

2.4 Reasoning with Pure Constraints
So far we have only looked at SL speciﬁcations whose pure parts were trivially true. Let us now turn
our attention to the goals that make use of non-trivial pure boolean assertions.
  2.4.1 Preconditions. To leverage pure preconditions, we adopt a number of the traditional Small-
foot-style rules, whose SSL counterparts are shown in the top part of Fig. 4. In the nomenclature of
Berdine et al. (2005), all those rules are non-operational, i.e., correspond to constructing the proofs of
symbolic heap entailment and involve no programming component. Note that the original rules in
Berdine et al. (2005) assume a restricted pure logic with only equalities; we adapt these rules to our
logic-agnostic style, relying on the oracle for pure validity instead of original syntactic premises.
  For instance, the rule SubstLeft makes use of a precondition that implies equality between two
universal variables, x = y, substituting all occurrences of x in the subgoal by y. The rule StarPar-
tial makes explicit the fundamental assumption of SL: disjointness of symbolic heaps connected
by the ∗ operator. Most commonly, this rule’s eﬀect is observable in combination with another rule,
Inconsistency, which identiﬁes an inconsistent pre, and emits an always-failing program error.
  These three SSL rules can be observed in action via the following example:
               {a = x ∧ y = a; x 7→ y ∗ y 7→ z} void urk(loc x, loc y) {true; y 7→ a ∗ x 7→ y}                                      (4)
  After applying SubstLeft, the goal transforms to {x, y} {x 7→ x ∗ x 7→ z} { {x 7→ x ∗ x 7→ x },
which is clearly unsatisﬁable, as the precondition requires two disjoint points-to heaplets with the
same source—a fact, which converted into a pure sub-formula x , x by StarPartial, resulting in
the error body via Inconsistency.
   2.4.2 Postconditions. In the presence of non-trivial pure postconditions, we face the problem to
ﬁnd suitable instantiations for their existentials. This is a challenging, yet well-studied problem, tack-
led by pure program synthesis (Alur et al. 2013). We consider this problem orthogonal to our agenda
of deriving pointer-manipulating programs, and represent pure synthesis with a simpliﬁcation rule
SubstRight (Berdine et al. 2005), exploiting an equality in a goal’s postcondition, and an oracle rule
Pick, which picks an instantiation for an existential non-deterministically,
   In practice, the non-determinism can be curbed, for example, by delegating to an existing pure
synthesizer (Kuncak et al. 2010; Reynolds et al. 2015). In our implementation, however, we found a
combination of ﬁrst-order uniﬁcation (rule UnifyPure) and restricted enumerative search (rule Pick
restricted to variables) to be very eﬀective at discharging such synthesis goals.

  Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                  :7

   As an example, consider the following goal (where S and S 1 are ﬁnite sets and ∪· is disjoint union):

               {S = {v } ∪· S 1 ; x 7→ a} void elem(loc x, int v) {S = {v 1 } ∪· S 1 ; x 7→ v 1 + 1}                      (5)

Following the rule UnifyPure, one can unify the two facts about sets in the pre and the post, ob-
taining the substitution [v 1 7→ v]. The rest is accomplished by the rule Write, which emits the only
necessary statement for elem’s body: *x = v + 1.

2.5    Synthesis with Inductive Predicates
The real power of Separation Logic stems from its ability to compositionally reason about linked
heap-based data structures, such as lists and trees, whose shape is deﬁned recursively via inductive
heap predicates. The most traditional example of a data structure deﬁned this way is a linked list
segment lseg(x, y, S) (Reynolds 2002), whose deﬁnition is given by the two-clause predicate below:

         lseg(x, y, S) , x = y ∧ {S = ∅; emp}
                                                                                                                          (6)
                         x , y ∧ {S = {v} ∪· S 1 ; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt ∗ lseg(nxt, y, S 1 )}


   The predicate deﬁnition, which we will abstractly denote as D , p(x i ) ξ j , χ j , R j j ∈1... N , starts
                                                                                      

from the name p and a vector or formal parameters x i ; for lseg those are the symbolic pointer vari-
ables, x and y for the ﬁrst and the last pointer in the list, as well as for the logical set S of its elements.
What follows is a sequence of N inductive clauses, with a j th clause starting from a guard ξ j —a boolean
formula deﬁning a condition on the predicate’s formals,4 followed by the clause body—a SL assertion
with a spatial part R j and pure part χ j , describing the shape of the heap and pure constraints, corre-
spondingly. Clauses’ free variables, i.e., non-formals, (e.g., v, nxt) are treated as ghosts or existentials,
depending on whether the predicate instance is in a pre or post of a goal. From now on, we extend
the deﬁnition of the goal, with a context Σ, which will store the deﬁnitions of inductive predicates
and speciﬁed functions, which are accessible in the derivation.
   That is, the ﬁrst clause of lseg states that in the case of x and y being equal, the linked list’s set of
element is empty and its implementation is an empty heap emp. The complementary second clause
postulates the existence of the allocated memory block (or just block) of two consecutive pointers
rooted at x (denoted [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt), such that the ﬁrst pointer stores the payload v,
while the second one points to the tail of the list, whose shape is deﬁned recursively via the same
predicate, although with diﬀerent actuals, as captured by the predicate instance lseg(nxt, y, S 1 ).

   2.5.1 Dynamic Memory. In order to support dynamically allocated linked structures, as demon-
strated by deﬁnition (6), we extend the language of symbolic heaps with two new kinds of assertions:
blocks and predicate instances. Symbolic blocks are a well-established way to add to SL support for
consecutive memory chunks (Brotherston et al. 2017; Jacobs et al. 2011), which can be allocated and
disposed all together.5 Two SSL rules, Alloc and Free (presented in Sec. 3), make use of blocks, as
those appear in the post- and the pre-conditions of their corresponding goals. Conceptually, Alloc
looks for a block in the postcondition rooted at an existential and allocates a block of the same size
(by emitting the command let x = malloc(n)), adding it to the subgoal’s precondition. Free is trig-
gered by an un-matched block in the goal’s pre, rooted at some program variable x, which it then
disposes by emitting the call to free(x), removing it from the subgoal’s precondition.

4 In the case of logical overlap, the conditions for diﬀerent clauses are checked in the order the clauses are deﬁned.
5 An alternative would be to adopt an object model with ﬁelds, which is more verbose (Berdine et al. 2005).



                                      Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :8                                                                            Nadia Polikarpova and Ilya Sergey

   2.5.2 Induction. Let us now synthesize our ﬁrst recursive heap-manipulating function, a linked
list’s destructor listfree(x), which expects a linked list starting from its argument x and ending with
the null-pointer, and leaves an empty heap as its result:
                                   {lseg(x, 0, S)} void listfree(loc x) {emp}                                             (7)
   The ﬁrst synthesis step is carried out by the SSL rule Induction. We postpone its formal descrip-
tion until the next section, conveying the basic intuition here. Induction only applies to the initial
synthesis goal whose precondition contains an inductive predicate instance, and its eﬀect is to add a
new function symbol to the goal’s context, such that an invocation of this function would correspond
to a recursive call. In our example (7) Induction extends the context Σ with a “recursive hypothesis”
as follows (we explain the meaning of the tag 1 in lseg1 (x ′, 0, S ′) later):6

                                  Σ1 , Σ, listfree(x ′) : lseg1 (x ′, 0, S ′) {emp}
                                                         
                                                                                                                          (8)
   2.5.3 Unfolding Predicates. The top-level rule Induction is complemented by the rule Open (de-
ﬁned in Sec. 3), which unfolds a predicate instance in the goal’s precondition according to its def-
inition, and creates a subgoal for each inductive clause. For instance, invoked immediately on our
goal (7), it has the following eﬀect on the derivation:
(a) Two sub-goals, one for each of the clauses of lseg, are generated to solve:
                    = 0 ∧ S = ∅; emp} { {emp}
   (i) Σ1 ; {x } ; {x
  (ii) Σ1 ; {x } ; x , 0 ∧ S = {v} ∪· S 1 ; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt ∗ lseg1 (nxt, y, S 1 ) { {emp}
(b) Assuming c 1 and c 2 are the programs solving the sub-goals (i) and (ii), the ﬁnal program is ob-
    tained by combining them as if (x = 0) {c 1 } else {c 2 }.
Thus, Open performs case-analysis according to the predicate deﬁnition. Note how the precondition
of each generated sub-goal is reﬁned by the corresponding clause’s guard and body. The resulting
sub-programs, once synthesized, are then combined with the conditional statement (this is why we
require decidability of the guard statements), which branches on the predicate’s guard. It is easy to
see that the ﬁrst sub-goal (i) can be immediately solved via Emp rule, producing the program skip.
   2.5.4 Level Tags. Synthesizing recursive programs requires extra care in order to avoid inﬁnite
derivations, as well as vacuously correct (in the sense of partial program correctness) non-terminating
programs that simply call themselves. To avoid this pitfall, we adopt the ideas from the Cyclic Ter-
mination Proofs in SL (Brotherston et al. 2012), under the assumption that employed user-deﬁned
inductive predicates are well-founded, i.e., have their recursive applications only on strictly smaller
sub-heaps (Brotherston et al. 2008). We ensure that this is the case by checking that there is at least
one points-to predicate in clauses that also contain predicate instances.
   Speciﬁcally, to avoid inﬁnite unfolding of predicate instances we introduce level tags (natural num-
bers, ranged over by ℓ), which now annotate some predicate instances in the pre and post of the goal
and the context functions. For an instance in a goal’s pre, a tag determines whether a set of functions
in Σ that can be “applied” to it. As a result of a function application, tags are modiﬁed (as we explain
later), thus preventing functions from being “re-applied” to their own symbolic post-heaps. Since
tags only serve to control function calls, the rules Frame (Fig. 1) and UnifyHeaps (Fig. 3) ignore
them when comparing sub-heaps for equality. All predicates in the pre/post of the initial goal have
their level tag set as ℓ = 0, and the rule Open only applies to 0-tagged predicates, incrementing their
tag (i.e., one cannot “unfold again” an already opened instance).

6 In SSL, a context Σ can also store user-provided speciﬁcations of auxiliary functions synthesized earlier. We will elaborate

on case studies relying on user-provided auxiliary functions in Sec. 6.2.


   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                       :9

    Call                                                         Close
            F , f (x i ) : ϕ f , P f ψ f , Q f ∈ Σ                                  
                                                                   D , p(x i ) ξ j , χ j , R j j ∈1. . .N ∈ Σ      ℓ < MaxUnfold
                   ℓ
                R = [σ ]P f         ϕ ⇒ [σ ]ϕ f
                                                                    1 ≤k ≤N           σ , [x i 7→ y i ]      R ′ , ⌈[σ ]R k ⌉ ℓ+1
     ϕ ′ , [σ ]ψ f       R ′ , ⌈[σ  ]Q f ⌉     ei = [σ ]x i
                                                                        Σ; Γ ; { P } { ψ ∧ [σ ]ξ k ∧ [σ ]χk ; Q ∗ R ′ c
                         Σ; Γ ; ϕ ∧ ϕ ′ ; P ∗ R ′ { { Q } c
                                
    Vars (ei ) ⊆ Γ                                                                               n                o
             Σ; Γ ; {ϕ ; P ∗ R } { { Q } | f (ei ); c                           Σ; Γ ; { P } { ψ ; Q ∗ p ℓ (y i ) c

           Fig. 5. Selected SSL rules for synthesis with recursive functions and inductive predicates.

  To see how tags control what functions from Σ can be applied, consider the rule Call in Fig. 5. It
ﬁres when the goal contains in its precondition a symbolic sub-heap R, which can be uniﬁed with the
precondition Pf of a function symbol f from the goal’s context Σ. This uniﬁcation is similar to the
eﬀect of UnifyHeaps, with the diﬀerence that Call takes level tags into the account (i.e., instances
with diﬀerent tags cannot be uniﬁed), reﬂected in the tag-aware equality predicate =ℓ . Our example’s
second goal (ii)
            n                                                                               o
      {x } ; x , 0 ∧ S = {v} ∪· S 1 ; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt ∗ lseg1 (nxt, y, S 1 ) { {emp} (9)

can be now transformed, via Read (focused on hx, 1i 7→ nxt), into
               n                                                                                 o
   {x, nxt2 } ; x , 0 ∧ S = {v} ∪· S 1 ; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt2 ∗ lseg1 (nxt2, y, S 1 ) { {emp}
                                                                                                            (10)
   The grayed fragment in (10) can now be uniﬁed with the               void listfree(loc x) {
precondition of listfree (8) following Call’s premise. As                  if (x = 0) {} else {
the tags match (both indicate the ﬁrst unfolding of the pred-                let nxt2 = *(x + 1);
icate), uniﬁcation succeeds with the substitution σ = [x ′ 7→                listfree(nxt2);
nxt2, S ′ 7→ S 1 ] from f ’s parameters and ghosts to the goal               free(x);
variables. The same rule produces, from the f ’postcondition,              } }
                            ′
a new symbolic heap R , which replaces the targeted frag-                 Fig. 6. Synthesized listfree (7).
ment in the pre, recording the eﬀect of the call. All tagged
predicate instances in R ′ get their tags erased (⌈[σ ]Q f ⌉ ), thus, preventing any future recursive appli-
cations (via Call) on the produced symbolic heap (more on that design decision in Sec. 7). However,
in this example, the function’s post is merely {emp}, so the goal becomes:

           {x, nxt2 } ; {x , 0 ∧ S = {v} ∪· S 1 ; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt2 ∗ emp} { {emp}                             (11)

   The remaining steps are carried out by the rule Free,                       void listmorph (loc x, loc r) {
followed by Emp, with the former disposing the remain-                           if (x = 0) { } else {
                                                                                   let v2 = *x;
ing block, thus, completing the derivation with program                            let nxt2 = *(x + 1);
listfree shown in Fig. 6.                                                          listmorph (nxt2, r);
                                                                                   let y12 = *r;
   2.5.5 Unfolding in the postcondition. Whereas Open                              let y2 = malloc (3);
unfolds predicate instances in a goal’s precondition, a                            free(x);
complementary rule Close (Fig. 5) performs a similar op-                           *(y2 + 2) = y12;
eration on the goal’s postcondition. The main diﬀerence                            *(y2 + 1) = v2 + 1;
                                                                                   *y2 = v2;
is that instead of performing a case-split and emitting sev-
                                                                                   *r = y2;
eral subgoals, Close non-deterministically picks a single                        } }
clause k from the predicate’s deﬁnition (the intuition be-
ing that the required case split has already been performed       Fig. 7. Synthesized listmorph (13).
by Open). Upon unfolding, the clause’s adapted guard ([σ ]ξ k ) and pure part ([σ ]χk ) are added to the

                                         Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :10                                                                          Nadia Polikarpova and Ilya Sergey

subgoal’s postcondition, while its spatial part also gets its level tags increased by one (⌈[σ ]Rk ⌉ ℓ+1 ),
in order to account for the depth of unfoldings.7
   To showcase the use of Close, let us deﬁne a new predicate for a linked null-terminating structure
lseg2, which stores in each node the payload v and v + 1:
   lseg2(x, S) , x = 0 ∧ {S = ∅; emp}
                           S = {v} ∪· S 1 ;                                                                       (12)
                                                                                               
                 x ,0∧
                           [x, 3] ∗ x 7→ v ∗ hx, 1i 7→ v + 1 ∗ hx, 2i 7→ nxt ∗ lseg2(nxt, S 1 )
   We now synthesize an implementation for the following speciﬁcation, requiring to morph a regular
list lseg(x, 0, S) to lseg2(y, S), both parameterized by the same set S:
                {r 7→ 0 ∗ lseg(x, 0, S)} void listmorph(loc x, loc r) {r 7→ y ∗ lseg2(y, S)}                      (13)
The derivation starts Induction, then Opens lseg(x, 0, S), producing two sub-goals. The ﬁrst one:
                       {x, r } ; {S = ∅ ∧ x = 0; r 7→ 0} { r 7→ y ∗ lseg20 (y, S)
                                                          
                                                                                               (14)
is easy to solve via Close, which should pick the ﬁrst clause from lseg2’s deﬁnition (12) (correspond-
ing to emp), followed by Frame to r 7→ y in the postcondition. The second subgoal, after having read
the value of (x + 1), thus into a program variable nxt2 looks as follows:
         {x, r , nxt2} ;
           S = {v} ∪· S 1 ∧ x , 0; r 7→ 0 ∗ [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt2 ∗ lseg1 (nxt2, 0, S 1 )
         
                                                                                                         {        (15)
         n                        o
          r 7→ y ∗ lseg20 (y, S)
Now, Close comes to the rescue, by allowing us to unfold the grayed instance in (15)’s post:
 {x, r , nxt2} ;
 n                                                                                                o
  S = {v} ∪· S 1 ∧ x , 0; r 7→ 0 ∗ [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt2 ∗ lseg1 (nxt2, 0, S 1 )                 {     (16)
                                                                                               1
 
   S = {v 1 } ∪· S 2 ; r 7→ y ∗ [y, 3] ∗ y 7→ v 1 ∗ hy, 1i 7→ v 1 + 1 ∗ hy, 2i 7→ nxt 1 ∗ lseg2 (nxt 1 , S 2 )
In principle, nothing in the postcondition prevents us from applying Close again, unfolding the in-
stance lseg21 (nxt 1 , S 2 ) even further. Intuitively, a postcondition with a symbolic heap that elaborated
is less likely to be satisﬁed, hence we limit the number of “telescopic” unfoldings by enforcing the
boundary MaxUnfold for the level tag. We can now use the Call rule, unifying the precondition of
the induction hypothesis (13) with the grayed parts in the goal (16), obtaining the following subgoal
(notice the new instance lseg2(y1 , S 1 ) in the pre with its tag erased):
  {x, r , nxt2} ;
  n                                                                                         o
   S = {v} ∪· S 1 ∧ x , 0; [x, 2] ∗ x 7→ v ∗ hx, 1i 7→ nxt2 ∗ r 7→ y1 ∗ lseg2(y1 , S 1 )                          {
  n                                                                                                             o
   S = {v 1 } ∪· S 2 ; r 7→ y ∗ [y, 3] ∗ y 7→ v 1 ∗ hy, 1i 7→ v 1 + 1 ∗ hy, 2i 7→ nxt 1 ∗ lseg21 (nxt 1 , S 2 )
The instances of lseg2 in the pre and the post, can now be uniﬁed via UnifyHeaps instantiating nxt 1
with y1 , followed by UnifyPure on pure parts, instantiating S 2 with S 1 , and then framed via Frame.
The remaining derivation is done by Reading from r and x, subsequent disposing of a two-cell block
(grayed in the pre) and allocation of a three-cell block in order to match the grayed block in the post.
Finally, the exact payload for cells of the newly-allocated 3-pointer block is determined by unifying
the set assertions in the pure parts of the pre and post (via UnifyPure), and then Write records the
right values to satisfy the constraints imposed for the head of lseg2-like list by Deﬁnition (12). The
resulted synthesized implementation of listmorph is shown in Fig. 7.
7 We will elaborate on the control of unfolding depth in Sec. 3.1.



   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                               :11

2.6 Enabling Procedure Calls by Means of Call Abduction
We conclude this overview with one last example—a recursive procedure for copying a linked list:
            {r 7→ x ∗ lseg(x, 0, S)} void listcopy(loc r) {r 7→ y ∗ lseg(x, 0, S) ∗ lseg(y, 0, S)}                      (17)
To make things more fun, we pass the pointer to the head of the list via another pointer r, which
is also used to record the result of the function—an address y of a freshly allocated list copy. The
synthesis begins by using Induction, producing the function symbol
 void listcopy(loc r') : r ′ 7→ x ′ ∗ lseg1 (x ′, 0, S ′) r ′ 7→ y ′ ∗ lseg1 (x ′, 0, S ′) ∗ lseg1 (y ′, 0, S ′) (18)
                                                         

It follows by Read (from r into x2) and Open, resulting in two subgoals, the ﬁrst of which (an empty
list) is trivial. The synthesis proceeds, reading from x2 into v2 and from x2 + 1 into nxt2, so after
using Close (on lseg0 (x, 0, S)) in the post, UnifyHeaps and Frame, we reach the following subgoal:
                                       n                                                         o
              {x, r , x2, v2, nxt2 } ; S = {v2 } ∪· S 1 ∧ x2 , 0; r 7→ x2 ∗ lseg1 (nxt2, 0, S 1 ) {
                                                                                                    (19)
                                         r 7→ y ∗ lseg1 (nxt2, 0, S 2 ) ∗ lseg0 (y, 0, S)
                                       

   At this point of our derivation, we run into an issue. AbduceCall                              
Ideally, we would like to use the grayed fragment of the F , f (xi ) : ϕ f ; Pf ∗ F f ψ f ; Q f ∈ Σ
goal (19)’s precondition, to ﬁre the rule Call with the                    F f has no predicate instances
                                                                                                     ′
spec (18), i.e. to make a recursive call on the tail list. How-        [σ ]Pf = P F f , emp     F′ , [σ ]F f
ever, the (18)’s precondition requires r to point to the start                Σ; Γ ; {ϕ; F } { ϕ; F c 1
of that list (nxt2), whereas in our case it still points to the            Σ; Γ ; ϕ; P ∗ F ′ ∗ R { {Q} c 2
start of the original list (x2).                                         Σ; Γ ; {ϕ; P ∗ F ∗ R} { {Q}| c 1 ; c 2
   Any programmer would know a solution to this conun-                          Fig. 8. AbduceCall rule.
drum: we have to to write nxt2 into r , in order to provide
a suitable symbolic heap to make a recursive call. Emitting such a write command is a synthesis sub-
goal in itself. To generate such sub-goals, we introduce a novel rule, AbduceCall, which is shown in
Fig. 8 and attempts to prepare the symbolic pre-heap for the recursive call by adjusting constant-size
symbolic footprint to become uniﬁable with the recursive calls’ precondition.
   First, the rule inspects the preconditions of the goal and         1 void listcopy (loc r) {
of the cadidate callee F from Σ, it tries to split the former         2       let x2 = *r;
into two symbolic sub-heaps, Pf and F f , such that all pred-         3       if (x2 = 0) { } else {
icate instances are contained within Pf , while the rest of           4          let v2 = *x2;
                                                                      5          let nxt2 = *(x2 + 1);
the heaplets (i.e., blocks and points-to assertions) are in F f .     6          *r = nxt2;
Next, it tries to unify Pf from the function spec with some           7          listcopy (r);
sub-heap P from the goal’s precondition, ﬁnding a suit-               8          let y12 = *r;
able substitution σ , such that P = [σ ]Pf . While doing so, it       9          let y2 = malloc(2);
does not account for the “remainder” [σ ]F f , which might 10                    *y2 = v2;
                                                                                 *(y2 + 1) = y12;
not be immediately matched by anything in the goal’s pre- 11
                                                                     12          *r = y2;
condition. In order to make it match, the goal emits, as 13                   } }
one of its premises, a sub-goal Σ; Γ ; {ϕ; F } { {true, F ′ }| c 1 ,
whose puspose is to synthesize a program c 1 , which will                 Fig. 9. Synthesized listcopy (17).
serve as an impedance matcher between some symbolic
subheap F from the original goal’s pre and F ′ = [σ ]F f .8
   For instance, in the speciﬁcation (18), Pf = lseg1 (x ′, 0, S ′) and F f = r ′ 7→ x ′ , so an attempt to
unify the former with the predicate instance in the grayed fragment of the goal (19) results in the
substitution σ = [x ′ 7→ nxt2, S ′ 7→ S 1 ]. Applying it to the remainder of the function spec’s pre, we
8 Our implementation is smarter than that: it ensures that F and F ′ have the same shape and diﬀer only in pointers’ values.



                                     Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
    :12                                                                          Nadia Polikarpova and Ilya Sergey


      Variable x, y     Alpha-numeric identiﬁers                   Pure assertion ϕ, ψ , ξ , χ ::= e
      Value       d     Theory-speciﬁc atoms                       Symbolc heap P, Q, R ::= emp | he, ιi 7→ e |
      Oﬀset        ι    Non-negative integers                                                      [x, n] | p(xi ) | P ∗ Q
      Expression e ::= d | x | e = e | e ∧ e | ¬e | . . .          Assertion      P, Q         ::= {ϕ, P }
      Command c ::= let x = ∗(x + ι) | ∗(x + ι) = e |
                                                                                                                
                                                                   Heap predicate D            ::= p (xi ) ξ j , χ j , R j
                        skip | error | magic |                     Function spec F             ::= f (xi ) : {P}{Q}
                        if (e) {c} else {c} | f (ei ) | c; c       Environment Γ               := ϵ | Γ, x
      Type        t ::= loc | int | bool | set                     Context        Σ            := ϵ | Σ, D | Σ, F
      Fun. dict. ∆ ::= ϵ | ∆, f (ti xi ) { c }
           Fig. 10. Programming language grammar.                                Fig. 11. SSL assertion syntax.


obtain F ′ = [σ ]F f = r ′ 7→ nxt2. One of the candidates to the role of F from the goal’s precondition
is the heaplet r 7→ x2 , so the corresponding subgoal will be of the form {r, . . .} ; {. . . ; r 7→ x2 } {
{r ′ 7→ nxt2 }, which will produce the write *r = nxt2. Fig. 9 shows the eventually synthesized imple-
mentation, with the abduced call-enabling write on line 6.

3     SYNTHETIC SEPARATION LOGIC IN A NUTSHELL
Having shown SSL in action, we now proceed with giving a complete set of its inference rules, along
with statements of the formal guarantees SSL provides wrt. synthesized imperative programs.
   The syntax for the imperative language supported by SSL is given in Fig. 10. The set of values
includes at least integers and pointers (isomorphic to non-negative integers). Expressions include
variables, values, boolean equality checks and additional theory-speciﬁc expressions (e.g., integer or
boolean operations). The command magic does not appear in runnable code and is included in the
language for the purpose of a deductive synthesis optimization, which we will explain in Sec. 5.4.
The language of commands does not include loops, which are modelled via recursive procedure
calls (f (ei )). Notice that for simplicity we do not provide a mechanism to return a variable from
a procedure (so the language is missing the return command) and therefore all procedures’ return
type is void. However, the result-returning discipline for a procedure can be encoded via passing a
result-storing additional pointer, as, e.g., in Example (17). A function dictionary ∆ is simply a list of
function deﬁnitions of the form f (ti x i ) { c }.
   The complete syntax of SSL assertions is shown in Fig. 11, and their meaning was explained in
detail throughout Sec. 2. We only notice here that, syntactically, pure assertions ϕ, ψ , etc coincide
with the language’s expressions e. The lack of the distinction between the two kinds is for the sake
of uniformity and to enable the use of third-party SMT solvers without committing to a speciﬁc ﬁrst-
order logic as an inherent part of SSL. We use a simple type system to make sure that the expressions
serving as pure formulae are of type bool, while also making sure that set-theoretical operations,
such as ∪,· do not leak to the program level.

3.1       The Zoo of SSL Rules
Fig. 12 presents all rules of SSL. Since most of them have already made an appearance in Sec. 2, here,
we only elaborate on the new ones, and highlight some important aspects of their interaction. It is
convenient to split the set of rules into the following six categories:
C1 Top-level rules are represented by just one rule: Induction (Fig. 12, bottom right). This rule is
     only applicable at the very ﬁrst stage of the derivation, and it produced a speciﬁed symbol f ,
    with the speciﬁcation identical to the top-level goal (modulo renaming of variables to avoind
     name capturing conﬂicts). In the case of several predicate instances p 0 (ei ) in the goal’pre, the

    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                                    :13

                                                                                                      NullNotLVal
   Induction                                         Emp                                                 x , 0 < ϕ         ϕ′ , ϕ ∧ x , 0
               f , goal’s name                         EV (Γ, P, Q) = ∅           ϕ ⇒ψ                Σ; Γ ; ϕ ′ ; hx, ι i 7→ e ∗ P { { Q } c
             x i , goal’s formals                     Γ ; {ϕ ; emp} { {ψ ; emp} | skip                Σ; Γ ; {ϕ ; hx, ι i 7→ e ∗ P } { { Q } | c
    P f , p 1 (y i ) ∗ ⌈P ⌉     Q f , ⌈Q ⌉
       F , f (x i ) : ϕ f ; P f ψ f ; Q f                  Inconsistency                                SubstLeft
    Σ, F; Γ ; ϕ ; p 0 (y i ) ∗ P { { Q } c                           ϕ ⇒⊥                                           ϕ ⇒x =y
       Σ; Γ ; ϕ ; p 0 (y i ) ∗ P { { Q } c
             
                                                            Γ ; {ϕ ; P } { { Q } | error                 Γ ; [y/x ]{ϕ ; P } { [y/x ]{Q } | c
                                                                                                                Γ ; {ϕ ; P } { { Q } | c
   StarPartial                                                                    Read
    x + ι , y + ι ′ < ϕ     ϕ ′ , ϕ ∧ (x + ι , y + ι ′ )                              a ∈ GV (Γ, P, Q)           y < Vars (Γ, P, Q)
   Σ; Γ ; ϕ ; hx, ι i 7→ e ∗ y, ι ′ 7→ e ′ ∗ P { { Q } c
            ′
                                                                                   Γ ∪ {y } ; [y/a]{ϕ ; hx, ι i 7→ a ∗ P } { [y/a]{ Q } | c
   Σ; Γ ; ϕ ; hx, ι i 7→ e ∗ y, ι ′ 7→ e ′ ∗ P { { Q } c
          
                                                                                   Σ; Γ ; {ϕ ; hx, ι i 7→ a ∗ P } { { Q } | let y = ∗(x + ι); c

    Open
                                                                                    Close
            D , p(x i ) ξ j , χ j , R j j ∈1. . .N ∈ Σ
                                 
                                                                                         D , p(x i ) ξ j , χ j , R j j ∈1. . .N ∈ Σ
                                                                                                          
      ℓ < MaxUnfold σ , [x i 7→ y i ] Vars (y i ) ⊆ Γ
                                                           ℓ+1                           ℓ < MaxUnfold            σ , [x i 7→ y i ]
    ϕ j , ϕ ∧ [σ ]ξ j ∧ [σ ]χ j        P j , ⌈[σ ]R j ⌉       ∗ ⌈P ⌉
                                                                                    for some k, 1 ≤ k ≤ N          R ′ , ⌈[σ ]R k ⌉ ℓ+1
          ∀j ∈ 1. . .N, Σ; Γ ; ϕ j ; P j { { Q } c j
                                                                                    Σ; Γ ; { P } { ψ ∧ [σ ]ξ k ∧ [σ ]χk ; Q ∗ R ′ c
     c , if ([σ ]ξ 1 ) {c 1 } else {if ([σ ]ξ 2 ) . . . else {c N } }                                      n                  o
                        n                  o                                                Σ; Γ ; { P } { ψ ; Q ∗ p ℓ (y i ) c
                Σ; Γ ; ϕ ; P ∗ p ℓ (y i ) { { Q } c

 AbduceCall                                                                        Call                            
           F , f (x i ) : ϕ f ; P f ∗ F f ψ f ; Q f ∈ Σ                                    F , f (x i ) : ϕ f ; P f ψ f ; Q f ∈ Σ
                                         

        F f has no predicate instances           [σ ]P f = P                                     ℓ
                                                                                               R = [σ ]P f         ϕ ⇒ [σ ]ϕ f
 F f , emp       F ′ , [σ ]F f       Σ; Γ ; {ϕ ; F } { ϕ ; F ′ c 1                 ϕ ′ , [σ ]ψ f       R ′ , ⌈[σ
                                                                                                                ]Q f ′⌉     ei = [σ ]x i
               Σ; Γ ; ϕ ; P ∗ F ′ ∗ R { { Q } c 2                                  Vars (ei ) ⊆ Γ       Σ; Γ ; ϕ ∧ ϕ ; P ∗ R ′ { { Q } c
              Σ; Γ ; {ϕ ; P ∗ F ∗ R } { { Q } | c 1 ; c 2                                      Σ; Γ ; {ϕ ; P ∗ R } { { Q } | f (ei ); c

    Alloc
                  ∗         i i 7→ ei ) z ∈ EV (Γ, P, Q)
    R = [z, n] ∗ 0≤i ≤n ( hz,                                                  Free
               {y } ∪ ti ∩ Vars (Γ, P, Q) = ∅                                                             ∗
                                                                                        R = [x, n] ∗ 0≤i ≤n ( hx, i i 7→ ei )
             R ′ , [y,         ∗
                      n] ∗ 0≤i ≤n ( hy, i i 7→ ti )                            Vars ({x } ∪ {ei }) ⊆ Γ   Σ; Γ ; {ϕ ; P } { { Q } | c
              Σ; Γ ; ϕ ; P ∗ R ′ { {ψ ; Q ∗ R } c                                          Σ; Γ ; {ϕ ; P ∗ R } { { Q } | free(n); c
       Σ; Γ ; {ϕ ; P } { {ψ ; Q ∗ R } | let y = malloc(n); c

                               Write
                               Vars (e) ⊆ Γ        Γ ; {ϕ ; hx, ι i 7→ e ∗ P } { {ψ ; hx, ι i 7→ e ∗ Q } | c
                                Γ ; ϕ ; hx, ι i 7→ e ′ ∗ P { {ψ ; hx, ι i 7→ e ∗ Q } ∗(x + ι) = e; c
                                   


   UnifyHeaps
                        [σ ]R ′ = R                                                 Frame
                      ′
                                                                                            EV (Γ, P, Q) ∩ Vars (R) = ∅
    frameable R           ∅ , dom
                                 (σ ) ⊆ EV (Γ, P, Q)                                 frameable R ′
                                                                                                    
                                                                                                         Γ ; {ϕ ; P } { {ψ ; Q } | c
           Γ ; {P ∗ R } { [σ ] ψ ; Q ∗ R ′ c
                                                                                              Γ ; {ϕ ; P ∗ R } { {ψ ; Q ∗ R } | c
            Γ ; {ϕ ; P ∗ R } { ψ ; Q ∗ R ′ c
                                


     Pick                                             UnifyPure
           y ∈ EV (Γ, P, Q)                                      [σ ]ψ ′ = ϕ ′                              SubstRight
                                                                                                                     x ∈ EV (Γ, P, Q)
     Vars (e) ∈ Γ ∪ GV (Γ, P, Q)                        ∅ , dom (σ ) ⊆ EV (Γ, P, Q)
                                                                                                              Σ; Γ ; { P } { [e/x ]{ψ , Q } | c
     Γ ; {ϕ ; P } { [e/y]{ψ ; Q } | c                      Γ ; { P } { [σ ]{ Q } | c
                                                                                                            Σ; Γ ; { P } { {ψ ∧ x = e; Q } | c
                                                      Γ ; ϕ ∧ ϕ ′; P { ψ ∧ ψ ′ ; Q c
                                                                        
         Γ ; {ϕ ; P } { {ψ ; Q } | c


 Fig. 12. All rules of SSL. Grayed parts are parameters; instantiating them diﬀerently yields diﬀerent rules.



                                           Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :14                                                                             Nadia Polikarpova and Ilya Sergey

    rule non-deterministically picks one recursion scheme, whereas other predicate instances in f ’s
    precondition get “sealed” via tag erasure ⌈P⌉ ).
C2 Terminals include Emp and Inconsistency. These rules conclude a successful derivation by emit-
    ting skip or error, respectively.
C3 Normalization rules include NullNotLVal, SubstLeft, StarPartial, and Read. The role of
    these rules is to normalize the precondition: eliminate ghosts and equal variables, and make
    explicit the assumptions encoded in the spatial part. As we discuss in Sec. 5.1, a characteristic
    feature of those rules is that they cannot cause their subderivation fail.
C4 Unfolding rules are the rules targeted speciﬁcally to predicate instances. The four basic unfolding
    rules are Open, Close, AbduceCall, and Call. As hinted before, the rule Open picks an instance
    p ℓ (ei ) in the goal’s pre, and produces a number of subgoals, emitting a conditional that accounts
    for all of p’s clauses. Close acts symmetrically on the post. Both rules increment the tag for the
    instances in the substituted clause bodies, and are not applicable for ℓ, which is equal or greater
    than the set boundary on the depth of unfoldings, deﬁned by the global synthesis parameter
    MaxUnfold.9 In our practical experience MaxUnfold taken to be equal 1 suﬃces for most of
    realistic case studies. The rule AbduceCall prepares the heap for a call application (via Call), as
    described in Sec. 2.6. Note that the rules UnifyHeaps and Frame have been slightly generalized
    wrt. to what was shown in Fig. 1 and Fig. 3, and now include a parametric premise frameable .
    If we deﬁne frameable to return true only for predicate instances, we obtain unfolding versions
    of these rules, which deal speciﬁcally with predicate instances.
C5 Flat rules deal with with the ﬂat part of the heap (which consists of block heaplets and heaplets
    of the form x 7→ e). They include Alloc, Free, Write, as well as the ﬂat versions of UnifyHeaps
    and Frame, with frameable deﬁned to return true for ﬂat heaplets.
C6 Pure synthesis rules are responsible for instantiating existentials. In Fig. 12 this category is rep-
    resented by three rules. The ﬁrst one is nondeterministic Pick, which is diﬃcult to implement
    eﬃciently. In order to make the presentation complete, we include two remaining, somewhat
    redundant but more algorithmic, pure synthesis rules introduced in Sec. 2.4.2 for the sake of
    eﬃcient search, namely UnifyPure and SubstRight.
  Let us refer to rules that emit a sub-program as operational and to the rest (i.e., to the rules that
only change the assertions) as non-operational. The rules from Fig. 12 form the basis of SSL as a proof
system, allowing for possible extensions for the sake of optimization or handling pure constraints. We
make them intentionally declarative rather than algorithmic, which is essential for establishing the
logic’s soundness, leaving a lot of freedom for possible implementations. Such decisions have to be
made, for instance, when engineering an implementation of AbduceCall or Pick. The algorithmic
aspects of SSL, e.g., non-deterministic choice of a frame or a unifying substitution, are handled by
the procedures from Sec. 4.

3.2 Formal Guarantees for the Synthesized Programs
The deﬁnition of the operational semantics of the SSL language (Fig. 10) follows the standard RAM
model. Heaps (ranged over by h) are represented as partial ﬁnite maps from pointers to values, with
support for pointer arithmetic (via oﬀsets). A function call is executed within its own stack frame
(c, s), where c is the next command to reduce and s is a store recording the values of the function’s
local variables and parameters. A stack S is a sequence of stack frames, and a conﬁguration is a pair
of a heap and a stack. The small-step operational semantics relates a function dictionary ∆, and a
pair of conﬁgurations: ∆; hh, Si   hh ′, S ′i,10 with ∗ meaning its reﬂexive-transitive closure.
9 Having the derivation/search depth bound by MaxUnfold aﬀects the completeness but not soundness of SSL.
10 We elide the transition rules for brevity; similar rules can by found, e.g., in the work by Rowe and Brotherston (2017).



   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                             :15

   Let us denote the valuation of an expression e under a store s as JeKs . Let I range over interpreta-
tions—mappings from user-provided predicates D to the relations on heaps and vectors of values. To
formally deﬁne the validity of Hoare-style specs in SSL, we use the standard deﬁnition of the satisfac-
tion relation ΣI as a relation between pairs of heaps and stores, contexts, interpretations, and SSL
assertions without ghosts. For instance, the following SSL deﬁnitions are traditional for Separation
Logics with interpreted predicates (Berdine et al. 2005; Nguyen et al. 2007):
• hh, si ΣI {ϕ; emp} iﬀ JϕKs = true and dom (h) = ∅.
• hh, si ΣI {ϕ; [x, n]} iﬀ JϕKs = true and dom (h) = ∅.
• hh, si ΣI {ϕ; he 1 , ιi 7→ e 2 } iﬀ JϕKs = true and dom (h) = Je 1 Ks + ι and h(Je 1 Ks + ι) = Je 2 Ks .
• hh, si ΣI {ϕ; P1 ∗ P2 } iﬀ ∃h 1 , h 2 , h = h 1 ∪· h 2 and hh 1 , si ΣI {ϕ; P1 } and hh 2 , si ΣI {ϕ; P2 }.
                                                                                          D           E
• hh, si ΣI {ϕ; p(x i )} iﬀ JϕKs = true and D , p(x i ) ξ j , χ j , R j ∈ Σ and h, Jx i Ks ∈ I(D).
                                                                      

Therefore, blocks have no spatial meaning, except for serving as an indicator on the memory frag-
ments that we allocated and can be disposed.
  To equip ourselves for the forthcoming proof of SSL soundness, we provide a deﬁnition of (sized)
speciﬁcation validity, which relies on the notion of a heap size |h| , |dom (h) |:
   Deﬁnition 3.1 (Sized validity). We say a speciﬁcation Σ; Γ ; {P} c {Q} is n-valid wrt. the function
dictionary ∆ whenever for any h, h ′, s, s ′ such that
• |h| ≤ n,
• ∆; hh, (c, s) · ϵi ∗ hh ′, (skip, s ′ ) · ϵi, and
• dom (s) = Γ and ∃σgv = [x i 7→ di ]x i ∈GV(Γ , P, Q) such that hh, si ΣI [σgv ]P,
it is the case that ∃σev = [y j 7→ d j ]y j ∈EV(Γ , P, Q) , such that hh ′, s ′ i ΣI [σev ∪· σgv ]Q
   Deﬁnition 3.1 is rather peculiar in that it deﬁnes a standard Hoare-style soundness wrt. pre/post,
while doing that only for heaps of size smaller than n. This is an important requirement to stage a
well-founded inductive argument for our soundness proof of SSL-based synthesis in the presence of
recursive calls. By introducing the explicit sizes to the deﬁnition of validity, we can make sure that
we only deal with calls on strictly decreasing subheaps wrt. the heap size when invoking functions
(auxiliary ones or recursive self). To make full use of this idea, we add one more auxiliary deﬁnition,
stratifying the shape of function dictionaries wrt. their speciﬁcations.
   Deﬁnition 3.2 (Coherence). A dictionary ∆ is n-coherent wrt. a context Σ (coh (∆, Σ, n)) iﬀ
• ∆ = ϵ and functions(Σ) = ϵ, or
• ∆ = ∆ ′, f (ti x i ) { c }, and Σ = Σ ′, f (x i ) : {P}{Q}, and coh (∆ ′, Σ ′, n), and Σ ′ ; {x i } ; {P} c {Q} is
  n-valid wrt. ∆ ′, or
• ∆ = ∆ ′, f (ti x i ) { c }, and Σ = Σ ′, f (x i ) : ϕ; ⌈P⌉ ∗ p 1 (ei ) {⌈Q⌉ }, and coh (∆ ′, Σ ′, n), and
                                                      

  Σ; {x i } ; ⌈P⌉ ∗ p 1 (ei ) c {⌈Q⌉ } is n ′-valid wrt. ∆ for all n ′ < n.
             

   That is, coherence is deﬁned inductively on the dictionary/context shape (regarding speciﬁed func-
tions and ignoring predicate deﬁnitions). A possibility of a (single) recursive deﬁnition f is taken into
the account in its last option. In that last clause, recursive calls to the function f from ∆ may only
take place on heaps of size strictly smaller than n, whereas there is no such restriction for the calls
to user-provided auxiliary functions, that can be invoked on heaps of sizes up to n.
   Soundness of Synthetic Separation Logic is stated by Theorem 3.3, which deﬁnes validity of the
synthesized program for any size of the input heap n, assuming that the validity of all recursive calls
of the synthesized programs is only established for n ′ < n, where the case n = 0 means no calls take
place and forms the base of the inductive reasoning.

                                     Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
    :16                                                                          Nadia Polikarpova and Ilya Sergey

   Theorem 3.3 (Soundness of SSL). For any n, ∆ ′ , if
   (i) Σ ′ ; Γ ; {P} { {Q}| c for a goal named f with formal parameters Γ , x i , and
  (ii) Σ ′ is such that coh (∆ ′, Σ ′, n), and 
 (iii) for all p 0 (ei ), ϕ; P, such that {P} = ϕ; p 0 (ei ) ∗ P , taking F , f (x i ) : ϕ; p 1 (ei ) ∗ ⌈P⌉ {⌈Q⌉ },
                                                                                         

       Σ ′, F ; Γ ; {P} c {Q} is n ′-valid for all n ′ < n wrt. ∆ , ∆ ′, f (ti x i ) { c },
then Σ ′ ; Γ ; {P} c {Q} is n-valid wrt. ∆.
    Proof. By the top-level induction on n and by inner induction on the structure of derivation
Σ ′ ; Γ ; {P} { {Q}| c. We refer the reader to Appendix A for the details.                     
  Theorem 3.3 states that a program derived via SSL constitutes a valid spec with its goal (i.e., all
writes, reads and deallocations in it are safe wrt. accessing heap pointers), assuming that recursive
calls, if present, are made on reduced sub-heaps. The technique we used—allowing for safe calls done
only on smaller sub-heaps—is reminiscent to the one employed in size-change termination-based
analyses (Lee et al. 2001), which ensure that every inﬁnite sequence of calls would cause inﬁnite
descent of some values, leading to the following result.
  Theorem 3.4 (Termination of SSL-synthesized programs). A program, which is derived via SSL
rules from a spec that uses only well-founded predicates, terminates.
  Proof. The only source of non-termination is calls. Auxiliary function calls cannot be chained
inﬁnitely as they erase tags on their post-heaps. Every recursive self-call is applicable after opening
a well-founded instance, and hence is done on a smaller sub-heap, erasing tags on its post-heap. 

4    BASIC SSL-POWERED SYNTHESIS ALGORITHM
In this section we show how to turn SSL from a declaratively deﬁned system (Fig. 12) into a search
algorithm with backtracking for deriving provably correct imperative programs.
   Encoding Rules and Derivations. The display on the        G ∈ Goal ::= hf , Σ, Γ, {P}, {Q}i
right shows an algorithmic representation of SSL deriva- K ∈ Cont , (Command)n → Command
tions and rules. To account for the top-level goal                          D      E
                                                             S ∈ Deriv ::= Gi , K
(which mandates the program synthesizer to generate
a runnable function), we include the function name f         R ∈ Rule , Goal ⇀ ℘(Deriv)
into the goal G, whose other components are the context Σ, environment Γ (initialized with f ’s for-
mals), pre {P} and post {Q}. A successful application or a rule R results in one or more alternative
sub-derivations Sk . Several alternatives arise when the rule exhibits non-determinism (e.g., due to
choosing a sub-heap to a unifying substitution), and are explored by a search engine one by one,
until it ﬁnds one that succeeds. This is customary for a conversion of a declarative inference system
to an algorithmic one (Pierce 2002, Chapter 16).
   In its turn, each sub-derivation is a pair. Its ﬁrst component contains zero (if R is a terminal)
or more sub-goals, which all need to be solved (think of a conjunction of a rule’s premises). The
second component of the sub-derivation is a continuation K, which combines the list of commands,
produced as a result of solving subgoals, into a ﬁnal program. The arity of a continuation (length
of a list it accepts) is the same as a number of sub-goals the corresponding rule emits (typically
one or more). Zero-arity means that the continuation has been produced by a terminal, and simply
emits a constant program. For non-operational rules (e.g., Frame), K , λ[c].c. For operational rules
K typically prepends a command to the result (e.g., Write), or generates a conditional statement
(Open). Therefore, the synthesizer procedure constructs the program by applying the continuations
of rules that have succeeded earlier, to the resulting programs by their subgoals, on the “backwards”
walk of the recursive search, in the style of logic programming (Mellish and Hardy 1984).

    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                :17

 Algorithm 4.1: synthesize (G : Goal, rules : Rule∗ )
    Input: Goal G = hf , Σ, Γ, { P }, {Q }i
    Input: List rules of available rules to try       12   function tryAlts (derivs, R, rs, G) =
    Result: Program c, such that                     13      match derivs
            Σ; f (Γ ) {c } ; Γ {P }c {Q }            14       case [ ] ⇒ if isInvert(R) then Fail else withRules(rs, G)
  1 function synthesize (G, rules) =
                                                     15       case hgoals, K i :: derivs′ ⇒
  2   withRules(rules, G)                            16         match solveSubgoals(goals, K)
  3 function withRules (rs, G) =                     17          case Fail ⇒ tryAlts(derivs′, R, rs, G)
  4   match rs
                                                     18           case c ⇒ if c = magic then tryAlts(derivs′, R, rs, G) else c
  5    case [ ] ⇒ Fail
  6    case R :: rs′ ⇒                                19   function solveSubgoals (goals, K) =
                                                   20      cs := [ ]
  7      subderivs = ﬁlterComm R(G)
                                                     21     pickRules = λ G. phasesEnabled ? nextRules(G) : AllRules
  8       if isEmpty(subderivs) then                 22     for G ← goals; c = synthesize(G, pickRules(G)); c , Fail do
  9         withRules(rs′ )                          23       cs := cs ++ [c]
 10       else                                       24     if |cs | < |goals| then Fail else K(cs)
 11         tryAlts(subderivs, R, rs′, G)



  The algorithm. The pseudocode of our synthesis procedure is depicted by Algorithm 4.1. Let us
ignore the grayed fragments in the pseudocode for now and agree to interpret the code as if they
were not present. Those fragments corresponds to optimizations, which we describe in detail in Sec. 5.
The algorithm is represented by four mutually-recursive functions:
• synthesize (G, rules) is invoked initially on a top-level goal, with rules instantiated with AllRules–
  all rules from Fig. 12. It immediately passes control to the ﬁrst auxiliary function, withRules.
• withRules (rs, G) iterates through the list rs of remaining rules, applying each one to the goal
  G. Once an application of some rule R succeeds (i.e., it emits a non-empty set of alternative sub-
  derivations subderivs), those are passed for solving to tryAlts. The case when a rule application
  emits no sub-derivations, is considered a search failure, so the next rule is tried from the list, until
  no more rules remains (line 5), at which point the search fails.
• tryAlts (derivs, R, rs, G) recursively processes the list of alternative sub-derivations derivs, gener-
  ated by the rule R. If the list is exhaused (line 14), withRules is invoked to try the rest of the rules
  rs. Otherwise, solveSubgoals is invoked for an alternative to solve all its sub-goals goals and apply
  the continuation K. In the case of success (line 18), the resulting program c is returned.
• solveSubgoals (goals, K) tries to solve all subgoals given to it, by invoking synthesize recursively
  with a suitable (full) list of rules, essentially, restarting the search problem “one level deeper” into
  the derivation. Unless some of the goals failed, their results are combined via K.11
   The algorithm implements is a naïve backtracking search that explores the space of all valid SSL
derivations rooted at the initial synthesis goal. The search proceeds in a depth-ﬁrst manner: it starts
from the root (the initial goal) and always extends the current incomplete derivation by applying a
rule to its leftmost open leaf (i.e., a leaf that is not a terminal application). The algorithm terminates
when the derivation is complete, i.e., it has no open leaves.
   In our experience, the algorithm implementation terminated on all inputs we provided. It seems
probable that this can be established by considering the following tuples, ordered lexicographically,
as a termination measure for a given goal G: h # 0- or 1-tagged predicate instances; # heaplets in
pre and post, for which there is no matching one in the post/pre; # existentials; # ”ﬂat” heaplets;
# conjuncts in the pre; # of points-to heaplets, whose disjointness or non-null-ness is not captured

11 The actual implementation is more eﬃcient than that and uses a breakable loop.



                                       Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
    :18                                                                          Nadia Polikarpova and Ilya Sergey

in the pre i. Notice that each rule from Fig. 12, except for Open and Close reduces this value for the
emitted sub-goals. Applicability of those two rules is handled via MaxUnfold parameter.
   That said, we have not proven termination of synthesize and leave it a conjecture.

5     OPTIMIZATIONS AND EXTENSIONS
The basic synthesis algorithm presented in Sec. 4 is a naïve backtracking in the space of all valid SSL
derivations. Note that this is already an improvement over a blind search in the space of all programs:
some incorrect programs are excluded from consideration a-priori, such as, e.g., programs that read
from unallocated heap locations. In this section we show how to further prune the search space by
identifying unsolvable goals and avoiding their exploration.

5.1 Invertible Rules
Our ﬁrst optimization relies on a well-known fact from proof theory (Liang and Miller 2009) that
certain proof rules are invertible: applying such a rule to any derivable goal produces a goal that is
still derivable. In other words, applying invertible rules eagerly without backtracking does not aﬀect
completeness. Algorithm 4.1 leverages this fact in line 14: when all sub-derivations of an invertible
rule R fail, the algorithm need not backtrack and try other rules, since the failure cannot be due to
R and must have been caused by a choice made earlier in the search.
   In SSL, the normalization rules—Read, StarPartial, NullNotLVal, and SubstLeft—are invert-
ible. The eﬀect of these rules on the goal is either to change a ghost into a program-level variable or
to strengthen the precondition; no rule that is applicable to the original goal can become inapplicable
as a result of this modiﬁcation, which is conﬁrmed by inspection of all rules in Fig. 12.

5.2       Multi-Phased Search
Among the rules of SSL described in Sec. 3, the unfolding rules are focused on transforming (and
eventually eliminating) instances of inductive predicates, while ﬂat rules are focused on other types
of heaplets (i.e., points-to and blocks). We observe that if the unfolding rules failed to eliminate a
predicate instance from the goal, there is no point to apply ﬂat rules to that goal. It is easy to show
that the ﬂat rules can neither eliminate predicates from the goal, nor enable previously disabled
unfolding rules: the only unfolding rule that matches on ﬂat heaplets is Call, but those heaplets
need not be “prepared” by the ﬂat rules, since that’s what AbduceCall is for.
   Following this observation, without loss of completeness, we can split the synthesis process into
two phases: the unfolding phase, where ﬂat rules are disabled, and the ﬂat phase, which only starts
when the goal contains no more predicate instances, and hence unfolding rules are inapplicable. This
optimization is implemented in line 21 of Algorithm 4.1. As a result, some unsolvable goals will be
identiﬁed early, in the unfolding phase. For example, the following goal:

                    {y, a, b} ; {y 7→ b ∗ a 7→ 0;} { y 7→ u ∗ u 7→ 0 ∗ lseg1 (u, 0, S)
                                                    

will fail immediately without exploring fruitless transformations on its ﬂat heap, since no unfolding
rules are applicable (assuming MaxUnfold = 1).

5.3       Symmetry reduction
Backtracking search often explores all reorderings of a sequence of rule applications, even if they
commute, i.e., the order of applications does not change the end sub-goal. As an examples, consider
the following goal:

                     {x, y, a, b} ; {x 7→ a ∗ y 7→ b ∗ a 7→ 0} { {x 7→ a ∗ y 7→ b ∗ b 7→ 0}

    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                        :19


    PostInconsistent                             PostInvalid                           UnreachHeap
                                                      P has no pred. instances          P, Q have no pred. instances or blocks
               ϕ ∧ψ ⇒ ⊥                           EV (Γ , P, Q) = ∅ ¬ (ϕ ⇒ ψ )               unmachedHeaplets(P, Q )
     Σ; Γ ; {ϕ ; P } { {ψ , Q } | magic           Σ; Γ ; {ϕ ; P } { {ψ , Q } | magic       Σ; Γ ; {ϕ, P } { {ψ , Q } | magic

                                                       Fig. 13. Failure rules.


Framing out x 7→ a and then y 7→ b, reveals the unsolvable goal {a 7→ 0} { {b 7→ 0}; upon back-
tracking, the naïve search would try the two applications of Frame in the opposite order, leading to
the same result.
   We implemented a symmetry reduction optimization to eliminate redundant backtracking of this
kind. To this end, we keep track of the footprint of each rule application, i.e., the sub-heaps of its
goal’s pre and post that the application modiﬁes. This enables us to identify whether two sequential
rule applications commute. Next, we impose a total order on rule applications; line 7 of Algorithm 4.1
rejects a new rule application R if it commutes with an earlier application R ′ in the current derivation,
but comes before R ′ in the total order.

5.4 Early Failure Rules
Sometimes on can identify an unsolvable goal by analyzing its pre and post. For example, the goal

                                {x, y} ; {a = 0; x 7→ a;} { {a = u ∧ u , 0; x 7→ u}

is unsolvable because its pure postcondition is logically inconsistent with the precondition. To lever-
age this observation and eliminate redundant backtracking, we extend SSL with failure rules, which
ﬁre when they identify such unsolvable goals. Each failure rule is a terminal one, so it prevents further
exploration of the (unsolvable) goal. Unlike other terminals, which conclude a successful derivation
with skip or error, a failure rule emits a special spurious program magic. Algorithm 4.1 intercepts any
appearance of magic in line 18, and treats the derivation as a unsuccessful. All failure rules are also
invertible, hence the eﬀect is to backtrack an application of an earlier rule.
   Our set of failure rules is shown in Fig. 13. The rule PostInconsistent identiﬁes a goal where
the the pure postcondition is inconsistent with the precondition. This is safe because during the
derivation both assertions can only become stronger (as a result of unfolding rules); also, even if the
postcondition still contains existentials, no instantiation of those existentials can produce a formula
that is consistent with (let alone implied by) the precondition. The rule PostInvalid ﬁres on a goal
where the pure postcondition (which is free of existentials) is not implied by the precondition; this
rule only applies when the precondition is free of predicate applications, and hence its pure part can-
not be strengthened any further. The rule UnreachHeap ﬁres when the spatial pre and post contian
only points-to heaplets, but the left-hand sides of these heaplets cannot be uniﬁed; in this case neither
UnifyHeaps nor Write can make the heaplets match. Note that it is important for completeness that
failure rules are checked after Inconsistency: if the pure precondition is inconsistent, the derivation
should not fail, but should instead emit error.

5.5 Extensions
We wrap up this section with a description of two SSL extensions used by our implementation in
order to expand the class of programs it can synthesize.

  5.5.1 Auxiliary Functions and Call Rule. The presented in Fig. 12 version of Call, which erases
the tags from the callee’s post, hurts the framework’s completeness. While it is not unsafe to employ
the predicates from the procedure call’s postcondition in further procedure calls, one cannot ensure

                                          Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :20                                                                          Nadia Polikarpova and Ilya Sergey

that they denote “smaller heaplets” and thus that the program terminates.12 To circumvent this limita-
tion for particularly common scenarios, we had to introduce one divergence between SuSLik and SSL
as shown in Fig. 12. Speciﬁcally, in the tool, we implemented support for stratiﬁed chained auxiliary
function calls, i.e., calls on a heap resulted from another, preceding, call (e.g., in ﬂatten w/append
and insertion sort). To allow for them, we had to implement slightly diﬀerent versions of Induc-
tion/Call rules, with an additional alternative in their premises, which instead of erasing tags of
the corresponding part of the post (⌈Q f ⌉ ) would increment them: ⌈Q f ⌉ •+1 . This would prevent a call
of the same function on the resulting heap fragment, but would enable calls of auxiliary functions,
whose specs’ pre feature predicates with matching higher-level tags. Eventually, due to incrementa-
tion, no applicable functions would have left in the context Σ. While this extension is unlikely to
break the SSL soundness and termination results (due to the limit of chained applications, enabled
by growing tags), it would require us to generalize the well-foundedness argument in Sec. 3.2, and
in the interest of time we did not carry out this exercise.

   5.5.2 Branch Abduction. As described, SSL rules only         Branch
emit conditional statements when unfolding an inductive                Σ; Γ ; {ϕ ∧ ψ ; P } { {Q}| c 1
predicate instance in the goal’s precondition via Open.              Σ; Γ ; {ϕ ∧ ¬ψ ; P } { {Q}| c 2
This prevents our framework from synthesizing some use-          Σ; Γ ; {ϕ; P } { {Q}| if (ψ ) c 1 else c 2
ful functions, in particular, those that branch on the con-
                                                                             Fig. 14. Branch rule.
tent on a data structure rather than its shape. This source
of incompleteness can easily be mitigated by adding a rule Branch (Fig. 14), which is always appli-
cable and generates a conditional statement with a non-deterministically chosen guard. Of course,
in practice picking the guard blindly is not feasible. Our implementation employs a variation of a
popular technique in program synthesis, known as condition (or branch) abduction (Alur et al. 2017;
Kneuss et al. 2013; Leino and Milicevic 2012; Polikarpova et al. 2016). Instead of emitting conditionals
eagerly, branch abduction tries to detect when the current program under consideration is a promis-
ing candidate for becoming a branch of a conditional, and then abduces a guard that would make this
branch satisfy the speciﬁcation.
   The SSL variation of branch abduction piggy-backs on the failure rule PostInvalid (Sec. 5.4),
which detect a goal whose pure postcondition ψ has no existentials and does not follow from the
precondition ϕ. Instead of rejecting this goal as unsolvable, branch abduction searches a small set of
pure formulas (all atomic formulas over program variables in Γ ); if it can ﬁnd a formula ϕ ′ such that
ϕ ∧ ϕ ′ ⇒ ψ , it abduces ϕ ′ as the branch guard for the current goal.
   For a simple example, consider the following synthesis goal that corresponds to computing a lower
bound of two integers x and y:

                                  {x, y} ; {r 7→ 0} { {m ≤ x ∧ m ≤ y; r 7→ m}

We ﬁrst apply Pick with [m 7→ x], arriving at the goal {r 7→ 0} { {x ≤ x ∧ x ≤ y; r 7→ x }. At
this point, the postcondition is invalid, so branch abduction ﬁres and infers a guard x ≤ y for the
current derivation. It also emits a new goal for synthesizing the else branch, where the negation of
the abduced condition is added to the precondition: {¬(x ≤ y); r 7→ 0} { {m ≤ x ∧ m ≤ y; r 7→ m}.
If the synthesis of the else branch succeeds, the two branches are joined by a conditional; otherwise
branch abduction fails.


12 A similar issue is reported in the work by Rowe and Brotherston (2017) on verifying termination of procedural programs.



   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                              :21

Table 1. Benchmarks and SuSLik results. For each benchmark, we report the size of the synthesized Code (in
AST nodes) and the ratio Code/Spec of code to specification; as well as synthesis times (in seconds): with all
optimizations enabled (Time), without phase distinction (T-phase), without invertible rules (T-inv), without early
failure rules (T-fail), without the commutativity optimization (T-com), and without any optimizations (T-all). T-
IS reports the ratio of synthesis time in ImpSynt to Time. “-” denotes timeout of 120 seconds.

         Group       Description      Code   Code/Spec     Time    T-phase     T-inv   T-fail   T-com     T-all   T-IS
                      swap two         12       0.9x       < 0.1       < 0.1   < 0.1   < 0.1    < 0.1     < 0.1
       Integers
                    min of two2        10       0.7x        0.1         0.1     0.1    < 0.1     0.1       0.2
                      length1,2        21       1.2x        0.4         0.9     0.5     0.4      0.6       1.4    29x
                         max1          27       1.7x        0.6         0.8     0.5     0.4      0.4       0.8    20x
                         min1          27       1.7x        0.5         0.9     0.5     0.4      0.5       1.2    49x
                     singleton2        11       0.8x       < 0.1       < 0.1   < 0.1   < 0.1    < 0.1     < 0.1
       Linked          dispose         11       2.8x       < 0.1       < 0.1   < 0.1   < 0.1    < 0.1     < 0.1
        List          initialize       13       1.4x       < 0.1        0.1     0.1    < 0.1     0.1      < 0.1
                         copy3         35       2.5x        0.2         0.3     0.3     0.1      0.2        -
                       append3         19       1.1x        0.2         0.3     0.3     0.2      0.3       0.7
                        delete3        44       2.6x        0.7         0.5     0.3     0.2      0.3       0.7
                      prepend1         11       0.3x        0.2         1.4    83.5     0.1      0.1        -     48x
       Sorted           insert1        58       1.2x        4.8          -       -       -       5.0        -      6x
        list       insertion sort1     28       1.3x        1.1         1.8     1.3     1.2      1.2      74.2    82x
                           size        38       2.7x        0.2         0.3     0.2     0.2      0.2       0.3
                       dispose         16       4.0x       < 0.1       < 0.1   < 0.1   < 0.1    < 0.1     < 0.1
        Tree              copy         55       3.9x        0.4        49.8      -      0.8      1.4        -
                  ﬂatten w/append      48       4.0x        0.4         0.6     0.5     0.4      0.4       0.6
                    ﬂatten w/acc       35       1.9x        0.6         1.7     0.7     0.5      0.6        -
                        insert1        58       1.2x       31.9          -       -       -        -         -     11x
         BST         rotate left1      15       0.1x       37.7          -       -       -        -         -     0.5x
                    rotate right1      15       0.1x       17.2          -       -       -        -         -     0.8x
        1 From (Qiu and Solar-Lezama 2017)    2 From (Leino and Milicevic 2012)    3 From (Qiu et al. 2013)


6     IMPLEMENTATION AND EVALUATION
We implemented SSL-based synthesis as a tool, called SuSLik, in Scala, using Z3 (de Moura and Bjørner
2008) as the back-end SMT solver via the ScalaSMT library (Cassez and Sloane 2017).13 We evaluated
our implementation with the goal of answering the following research questions:
(1) Generality: Is SuSLik general enough to synthesize a range of nontrivial programs with pointers?
(2) Utility: How does the size of the inputs required by SuSLik compare to the size of the generated
    programs? Does SuSLik require any additional hints apart from pre- and post-conditions? What
    is the quality of the generated programs?
(3) Eﬃciency: Is it eﬃcient? What is the eﬀect of optimizations from Sec. 5 on synthesis times?
(4) Comparison with existing tools: How does SuSLik fare in comparison with existing tools for syn-
    thesizing heap-manipulating programs, speciﬁcally, ImpSynt (Qiu and Solar-Lezama 2017)?

6.1    Benchmarks
In order to answer these questions, we assembled a suite of 22 programs listed in Tab. 1. The bench-
marks are grouped by the main data structure they manipulate: integer pointers, singly linked lists,
sorted singly linked lists, binary trees, and binary search trees.
   To facilitate comparison with existing work, most of the programs are taken from the litera-
ture on synthesis and veriﬁcation of heap-manipulating programs: the ImpSynt synthesis bench-
marks (Qiu and Solar-Lezama 2017), the Jennisys synthesis benchmarks (Leino and Milicevic 2012),
13 The tool sources can be found at https://github.com/TyGuS/suslik.



                                     Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :22                                                                           Nadia Polikarpova and Ilya Sergey

     loc srtl_insert (loc x, int k)
     requires srtl(x)
     ensures srtl(ret) ∧
       len(ret) = old(len(x)) + 1 ∧
       min(ret) = (old(k) < old(min(x))                          {
         ? old(k) : old(min(x))) ∧                                   0 ≤ n ∧ 0 ≤ k ∧ k ≤ 7 ;
       max(ret) = (old(max(x)) < old(k)                              ret 7→ k ∗ srtl(x, n, lo, hi)
         ? old(k) : old(max^(x)))                                }
     {                                                           void srtl_insert (loc x, loc ret)
       if (cond(1)) {                                            {
         loc ?? := new;                                            n1 = n + 1 ∧
         return ??;                                                lo1 = (k ≤ lo ? k : lo) ∧
       } else {                                                    hi1 = (hi ≤ k ? k : hi) ;
         statement (1);                                            ret 7→ y ∗ srtl(y, n1, lo1, hi1)
         loc ?? := srtl_insert (??, ??);                         }
         statement (1);
         return ??;
       }
     }
Fig. 15. (left) The ImpSynt input for the sorted list insertion; (right) The SuSLik input for the same benchmark.

and the Dryad veriﬁcation benchmarks (Qiu et al. 2013). We manually translated these benchmarks
into the input language of SuSLik, taking care to preserve their semantics. Dryad and ImpSynt use
the Dryad dialect of separation logic as their speciﬁcation language, hence the translation in this
case was relatively straightforward. As an example, consider an ImpSynt speciﬁcation and its SuS-
Lik equivalent in Fig. 15. The “??” are part of the ImpSynt spec language, denoting unknown holes
to be ﬁlled by the synthesizer. The main diﬀerence between the two pre-/post-condition pairs is that
the Dryad logic supports recursive functions such as len, min , and max ; in SuSLik this information is
encoded in more traditional SL style: by passing additional ghost parameters to the inductive pred-
icate srtl . The extra precondition 0 ≤ n ∧ 0 ≤ k ∧ k ≤ 7 in SuSLik corresponds to implicit axioms
in ImpSynt (in particular, the condition on k is due to its encoding of list elements as unsigned 3-bit
integers—there is no such restriction in SuSLik). In addition to benchmarks from the literature, we
also added several new programs that show-case interesting features of SuSLik.

6.2 Results
Evaluation results are summarized in Tab. 1. All experiments were conducted on a commodity laptop
(2.7 GHz Intel Core i7 Lenovo Thinkpad with 16GB RAM).
    6.2.1 Generality and Utility. Our experiment conﬁrms that SuSLik is capable of synthesizing pro-
grams that manipulate a range of heap data structures, including nontrivial manipulations that re-
quire reasoning about both the shape and the content of the data structure, such as insertion into
a binary search tree. We manually inspected all generated solutions, as well as their accompanying
SSL derivations, and conﬁrmed that they are indeed correct.14 Perhaps unsurprisingly, some of the
solutions were not entirely intuitive: as one example, the synthesized version of list copy, in a bizarre
yet valid move, swaps the tails of the original list and the copy at each recursive call!
    Two of the programs in Tab. 1 make use of auxiliary functions: “insertion sort” calls “insert”, and
“tree ﬂatten w/append” calls the “append” function on linked lists. The speciﬁcations of auxiliary
functions have to be supplied by the user (while their implementations can, of course, be synthesized
independently). Alternatively, tree ﬂattening can be synthesized without using an auxiliary function,
if the user supplies an additional list argument that plays the role of an accumulator (see “tree ﬂatten
14 In the future, we plan to output SSL derivations as SL proofs, checkable by a third-party system such as VST (Appel 2011).



   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                        :23

w/acc”). As such, SuSLik shares the limitation of all existing synthesizers for recursive functions:
they require the initial synthesis goal to be inductive, and do not try to discover recursive auxiliary
functions (which is a hard problem, akin to lemma discovery in theorem proving).
   For simple programs speciﬁcation sizes are mostly comparable with the size of the synthesized
code, whereas more complex benchmarks is where declarative speciﬁcations really shine: for exam-
ple, for all Tree programs, the speciﬁcation is at most half the size of the generated code. Three
notable outliers are “prepend”, “rotate left”, and “rotate right”, whose implementations are relatively
short, while the speciﬁcation we inherited from ImpSynt describes the eﬀects of the functions on
the minimum and maximum of the list/tree. Note that the speciﬁcation sizes we report exclude the
deﬁnitions of inductive predicates, which are reusable, and are shared between the benchmarks.
   6.2.2 Eﬀiciency. SuSLik has proven to be eﬃcient in synthesizing a variety of programs: all 22
benchmarks are synthesized within 40 seconds, and all but four of them take less than a second.
   In order to assess the impact on performance of various optimizations described in Sec. 5, Tab. 1
also reports synthesis times with each optimization disabled: the column T-phase corresponds to
eliminating the distinction between phases; T-inv corresponds to ignoring rule invertibility; T-fail
corresponds to dropping all failure rules; T-com corresponds to disabling the symmetry reduction;
ﬁnally, T-all corresponds to a variant of SuSLik with all the above optimizations disabled. The results
demonstrate the importance of optimizations for nontrivial programs: 8 out of 22 benchmarks time
out when all optimizations are disabled. The simpler benchmarks (e.g., swap) do not beneﬁt from the
optimizations at all, since they do not exhibit a lot of backtracking. At the same time, all three BST
benchmarks time-out as a result of disabling even a single optimization.
   6.2.3 Comparison with Existing Synthesis Tools. We compare SuSLik with the most closely related
prior work on ImpSynt (Qiu and Solar-Lezama 2017). Out of the 14 benchmarks from (Qiu and Solar-Lezama
2017) successfully synthesized by ImpSynt, we excluded 5 that are not structurally recursive (4 of
them use loops, and bst_del_root uses non-structural recursion); the other 9 were successfully syn-
thesized by SuSLik. The qualitative diﬀerence in terms of the required user input is immediately
obvious from the representative example in Fig. 15: in addition to the declarative speciﬁcation, Imp-
Synt requires the user to provide an implementation sketch, which ﬁxes the control structure of
the program, the positions of function calls, and the number of other statements. These additional
structural constraints are vital for reducing the size of the search space in ImpSynt. Instead, SuSLik
prunes the search space by leveraging the structure inherent in separation logic proofs, allowing for
more concise, purely declarative speciﬁcations.
   Despite the additional hints from the user, ImpSynt is also less eﬃcient: as shown in the column T-
IS of Tab. 1, on 6 out of 9 common benchmarks, ImpSynt takes at least an order of magnitude longer
than SuSLik, even though the ImpSynt experiments were conducted on a 10-core server with 96GB
of RAM.
   On the other hand, ImpSynt is more general than SuSLik in that it can synthesize both recursive
and looping programs. We discuss this and other limitations of SuSLik in more detail in Sec. 7.

7 LIMITATIONS AND DISCUSSION
There are a number of known limitations of Synthetic Separation Logic and SuSLik design.
   SSL does no support synthesis of programs with while-loops, as this would require discovering
loop invariants, which signiﬁcantly increases the search space; instead, the initial goal is considered
as inductive and handled via Induction rule. As of now, SSL does not allow for mutually-recursive
inductive predicates. While not impossible in principle, this would require us to explore advanced
techniques for inductive proofs (Ta et al. 2016) and also generalize the use of tags; we plan to look into
this in the future. By limiting the number of unfoldings, via Open and Close rules, via MaxUnfold, we

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
  :24                                                                          Nadia Polikarpova and Ilya Sergey

circumvent a commonly known decidability problem of solving entailments in the presence of gen-
eral inductive predicates (Antonopoulos et al. 2014), but this also prevents some non-unreasonable
and perfectly speciﬁable in SSL programs from being synthesized, e.g., allocating a large constant-size
list.
   Currently, SSL and SuSLik cannot automatically synthesize programs that are not structurally
recursive wrt. some inductive predicate, such as, for instance, merging sorted lists or Merge-Sort.
One approach to mitigate this limitation is to prove termination by showing that each recursive
call decreases the value of a custom termination metric; this technique is used in several automated
veriﬁers and synthesizers (Leino 2013; Polikarpova et al. 2016). A termination metric maps the tuple
of function’s arguments into an element of a set with a pre-deﬁned well-founded order (usually a
tuple of natural numbers), and can be either provided by the user or inferred by the synthesizer.
   Some of SSL limitations are inherent for Separation Logics in general: SLs are known to work well
with disjoint tree-like linked structures, and programs, whose recursion scheme matches the data
deﬁnition, but not so well with ramiﬁed data structures, e.g., graphs. To address those, one could
integrate a more powerful, ramiﬁed version of Frame rule (Hobor and Villard 2013) into SSL, but
this would likely require more hints from the user, thus, reducing the utility of the approach.

8 RELATED WORK
There are two main directions in the area of program synthesis: synthesis from informal descriptions
(such as examples, natural language, or hints) (Albarghouthi et al. 2013; Feng et al. 2017; Feser et al.
2015; Murali et al. 2018; Osera and Zdancewic 2015; Polozov and Gulwani 2015; Smith and Albarghouthi
2016; Yaghmazadeh et al. 2017) and synthesis from formal speciﬁcations. We will only discuss the
more relevant latter direction. The goal of this type of program synthesis is to obtain a provably
correct program.
   In this area, there is a well-known trade-oﬀ between three dimensions: how complex the synthe-
sized programs are, how strong the correctness guarantees are, and how much input is required
form the user. On one end of the spectrum there are interactive synthesizers (Delaware et al. 2015;
Itzhaky et al. 2016), which can be very expressive and provide strong guarantees, but the user is
expected to guide the synthesis process (although, usually, with aid of dedicated proof tactics). On
the other end, there is fully automated synthesis for loop- and recursion-free programs over simple
domains, like arithmetic and bit-vectors (Alur et al. 2017; Gulwani et al. 2011). Our work lies in the
middle of this spectrum, where synthesis is automated but programs are more expressive.
   In the presence of loops or recursion, verifying candidates becomes nontrivial. Synthesizers like
Sketch (Solar-Lezama 2013) and Rosette (Torlak and Bodík 2014) circumvent this problem by re-
sorting to bounded veriﬁcation, which only provides restricted guarantees and has scalability issues
due to path explosion. In contrast, our work relies on unbounded deductive veriﬁcation.
   Among synthesis approaches that use unbounded veriﬁcation, synthesizers like Leon (Kneuss et al.
2013) and Synqid (Polikarpova et al. 2016) focus on pure functional (recursive) programs, which
are an easier target for unbounded veriﬁcation. Proof-theoretic synthesis (Srivastava et al. 2010) is
capable of synthesizing imperative programs with loops and arrays, but no linked structures; they
pioneered the idea of synthesizing provably-correct programs by performing symbolic (SMT-based)
search over programs and their veriﬁcation conditions simultaneously.
   Finally, the two pieces of prior work that are most closely related to ours in terms of scope are Jen-
nisys (Leino and Milicevic 2012) and Natural Synthesis (Qiu and Solar-Lezama 2017), both of which
generate provably-correct heap-manipulating programs. Both of them are essentially instances of
proof-theoretic synthesis with a program logic for reasoning about the heap. To that end, Jennisys
uses the Dafny veriﬁer (Leino 2013), which supports expressive yet undecidable speciﬁcations, and

  Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                       :25

often requires hints from the user, so in practice the tool doesn’t scale to complex examples (for exam-
ple, none of their benchmarks performs mutation). Natural Synthesis uses Dryad (Madhusudan et al.
2012; Qiu et al. 2013), a decidable program logic for reasoning about heap-manipulating programs.
The downside of this approach is that whole-program symbolic search doesn’t scale to larger pro-
grams; to mitigate this, they require the user to provide sketches with substantial restrictions on the
structure of the program. Our approach does not require sketches (but on the other hand, we do not
support loops).
   The recent tool FootPatch by van Tonder and Le Goues (2018) is very close in its methods and
goals to SuSLik. FootPatch builds on Infer (Calcagno and Distefano 2011), an open-source SL-based
static analyzer by Facebook, using it for automated program repair. It takes the intermediate asser-
tions, provided by Infer for programs with bugs, such as resource and memory leaks, and null deref-
erences, and constructs additive patches based on the observed discrepancy. In this, it acts similarly
to our AbduceCall rule. FootPatch does not synthesize patches that would involve recursion or
complex control ﬂow.
   Instead of whole-program symbolic search, like in proof-theoretic synthesis, our work follows the
tradition of deductive synthesis, i.e., backtracking search in the space of program derivation composed
of synthesis rules, which gradually transform a speciﬁcation into a program. This tradition originates
from the seminal work by Manna and Waldinger (Manna and Waldinger 1980), and similar ideas has
been used in more recent synthesis work (Delaware et al. 2015; Kneuss et al. 2013; Polikarpova et al.
2016). In particular, the overall structure of our synthesis algorithm (backtracking and-or search) is
similar to Leon (Kneuss et al. 2013), but our rules focus on heap manipulation, whereas their rules
focus on synthesizing pure terms (so in fact Leon can be used as a component by our algorithm).
Recent work on Optitian (Miltner et al. 2018) is very diﬀerent in scope—they synthesize bijective
string lenses from regular expression speciﬁcations and examples—but has interesting similarities in
the technique. Their pre- and post-condition are regexes, and their technique tries to “align” them
by e.g., unfolding the Kleene star; this is similar to how SuSLik tries to align the spatial pre- and
post-condition by unfolding predicates.
   Deductive synthesis is closely related to proof search, and there has been recent resurgence in
applying proof-theoretic techniques, like focusing, to program synthesis (Frankle et al. 2016; Scherer
2017). But none of them do it for a complex logic that can reason about stateful programs.
   Despite the vast space of available tools for symbolic veriﬁcation based on Separation Logic: Small-
foot (Berdine et al. 2006), HTT (Nanevski et al. 2010), Bedrock (Chlipala 2011), SLAyer (Berdine et al.
2011), HIP/SLEEK (Chin et al. 2011), VeriFast (Jacobs et al. 2011), Cyclist (Rowe and Brotherston
2017), SLAD (Bouajjani et al. 2012), GRASShopper (Piskac et al. 2014b), Viper (Müller et al. 2016), to
name just a few, to the best of our knowledge none of them has been employed for deriving pro-
grams from speciﬁcations. It is certainly our hope that this work will bring new synergies between
the research done in veriﬁcation, theorem proving, and program synthesis communities.
   For instance, in our approach to establish termination of SSL-synthesized programs, we used tech-
niques close in spirit to the methods for proving total correctness in type/SL-based frameworks. E.g.,
SSL’s tags might be seen as a variant of resource capacities used in HIP/SLEEK (Le et al. 2014). Our
use of Deﬁnition 3.1 of sized validity is similar to the induction on the ﬁniteness of the heap used
by Le and Hobor (2018) in their work on a logic for fractional shares. Tagged predicates we use are
reminiscent to the ⊲-modality in type theories for state and recursion (Appel et al. 2007).

9   CONCLUSION
In their seminal paper, Manna and Waldinger (1980) set forth an agenda for deductive synthesis of
functional programs: “theorem provers have been exhibiting a steady increase in their eﬀectiveness, and
program synthesis is one of the most natural application of those systems”.

                               Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
   :26                                                                          Nadia Polikarpova and Ilya Sergey

   In this work, we moved this endeavour to an uncharted territory of stateful computations. For
this, we employed a proof system which, instead of a pure type theory (Martin-Löf 1984), is based on
Separation Logic—a Type Theory of State (Nanevski 2016). Taking this vision as a guiding principle, we
designed Synthetic Separation Logic—a modest extension of Separation Logic, tailored for program
synthesis, and implemented a proof search algorithm for it. In doing so, we took full advantage of
the power of local reasoning about state (O’Hearn et al. 2001), which resulted in a principled and fast
approach for synthesyzing provably correct heap-manipulating programs.

ACKNOWLEDGMENTS
We wish to thank Aquinas Hobor and Reuben Rowe for their insightful and extremely detailed com-
ments on presentation, formalism, and examples. Their technical feedback has helped immensely to
bring out the best of this paper. We also wish to thank Shachar Itzhaky and Ranjit Jhala for their com-
ments on the draft. We are very grateful to Franck Cassez for his help with conﬁguring and using
ScalaSMT. Sergey’s research was supported by a generous gift from Google.

REFERENCES
Aws Albarghouthi, Sumit Gulwani, and Zachary Kincaid. 2013. Recursive Program Synthesis. In CAV (Part II) (LNCS), Vol. 9780.
   Springer, 934–950.
Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh,
   Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. In FMCAD. IEEE, 1–8.
Rajeev Alur, Arjun Radhakrishna, and Abhishek Udupa. 2017. Scaling Enumerative Program Synthesis via Divide and Conquer.
   In TACAS (Part I) (LNCS), Vol. 10205. Springer, 319–336.
Timos Antonopoulos, Nikos Gorogiannis, Christoph Haase, Max I. Kanovich, and Joël Ouaknine. 2014. Foundations for Deci-
   sion Problems in Separation Logic with General Inductive Predicates. In FOSSACS (LNCS), Vol. 8412. Springer, 411–425.
Andrew W. Appel. 2011. Veriﬁed Software Toolchain - (Invited Talk). In ESOP (LNCS), Vol. 6602. Springer, 1–17.
Andrew W. Appel, Robert Dockins, Aquinas Hobor, Lennart Beringer, Josiah Dodds, Gordon Stewart, Sandrine Blazy, and
   Xavier Leroy. 2014. Program Logics for Certiﬁed Compilers. Cambridge University Press.
Andrew W. Appel, Paul-André Melliès, Christopher D. Richards, and Jérôme Vouillon. 2007. A very modal model of a modern,
   major, general type system. In POPL. ACM, 109–122.
Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In APLAS (LNCS),
   Vol. 3780. Springer, 52–68.
Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2006. Smallfoot: Modular Automatic Assertion Checking with Sepa-
   ration Logic. In FMCO (LNCS), Vol. 4111. Springer, 115–137.
Josh Berdine, Byron Cook, and Samin Ishtiaq. 2011. SLAyer: Memory Safety for Systems-Level Code. In CAV (LNCS), Vol. 6806.
   Springer, 178–183.
Ahmed Bouajjani, Cezara Dragoi, Constantin Enea, and Mihaela Sighireanu. 2012. Accurate Invariant Checking for Programs
   Manipulating Lists and Arrays with Inﬁnite Data. In ATVA (LNCS), Vol. 7561. Springer, 167–182.
James Brotherston, Richard Bornat, and Cristiano Calcagno. 2008. Cyclic proofs of program termination in separation logic.
   In POPL. ACM, 101–112.
James Brotherston, Nikos Gorogiannis, and Max I. Kanovich. 2017. Biabduction (and Related Problems) in Array Separation
   Logic. In CADE (LNCS), Vol. 10395. Springer, 472–490.
James Brotherston, Nikos Gorogiannis, and Rasmus Lerchedahl Petersen. 2012. A Generic Cyclic Theorem Prover. In APLAS
   (LNCS), Vol. 7705. Springer, 350–367.
Cristiano Calcagno and Dino Distefano. 2011. Infer: An Automatic Program Veriﬁer for Memory Safety of C Programs. In
   NASA Formal Methods (LNCS), Vol. 6617. Springer, 459–465.
Qinxiang Cao, Santiago Cuellar, and Andrew W. Appel. 2017. Bringing Order to the Separation Logic Jungle. In APLAS (LNCS),
   Vol. 10695. Springer, 190–211.
Franck Cassez and Anthony M. Sloane. 2017. ScalaSMT: Satisﬁability Modulo Theory in Scala (Tool Paper). In Proceedings of
   the 8th ACM SIGPLAN International Symposium on Scala. 51–55.
Arthur Charguéraud. 2010. Program veriﬁcation through characteristic formulae. In ICFP. ACM, 321–332.
Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M. Frans Kaashoek, and Nickolai Zeldovich. 2015. Using Crash
   Hoare logic for certifying the FSCQ ﬁle system. In SOSP. ACM, 18–37.
Wei-Ngan Chin, Cristina David, and Cristian Gherghina. 2011. A HIP and SLEEK veriﬁcation system. In OOPSLA (Companion).
   ACM, 9–10.


   Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                                  :27

Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. 2012. Automated veriﬁcation of shape, size and bag
   properties via user-deﬁned predicates in separation logic. Sci. Comput. Program. 77, 9 (2012), 1006–1036.
Adam Chlipala. 2011. Mostly-automated veriﬁcation of low-level programs in computational separation logic. In PLDI. ACM,
   234–245.
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In TACAS (LNCS), Vol. 4963. Springer,
   337–340.
Benjamin Delaware, Clément Pit-Claudel, Jason Gross, and Adam Chlipala. 2015. Fiat: Deductive Synthesis of Abstract Data
   Types in a Proof Assistant. In POPL. ACM, 689–700.
Dino Distefano and Matthew J. Parkinson. 2008. jStar: Towards Practical Veriﬁcation for Java. In OOPSLA. ACM, 213–226.
Yu Feng, Ruben Martins, Jacob Van Geﬀen, Isil Dillig, and Swarat Chaudhuri. 2017. Component-based synthesis of table
   consolidation and transformation tasks from examples. In PLDI. ACM, 422–436.
John K. Feser, Swarat Chaudhuri, and Isil Dillig. 2015. Synthesizing data structure transformations from input-output examples.
   In PLDI. ACM, 229–239.
Jonathan Frankle, Peter-Michael Osera, David Walker, and Steve Zdancewic. 2016. Example-directed synthesis: a type-
   theoretic interpretation. In POPL. ACM, 802–815.
Georges Gonthier, Beta Ziliani, Aleksandar Nanevski, and Derek Dreyer. 2011. How to make ad hoc proof automation less ad
   hoc. In ICFP. ACM.
Sumit Gulwani, Susmit Jha, Ashish Tiwari, and Ramarathnam Venkatesan. 2011. Synthesis of loop-free programs. In PLDI.
   ACM, 62–73.
Aquinas Hobor and Jules Villard. 2013. The ramiﬁcations of sharing in data structures. In POPL. ACM, 523–536.
Shachar Itzhaky, Rohit Singh, Armando Solar-Lezama, Kuat Yessenov, Yongquan Lu, Charles E. Leiserson, and Rezaul Alam
   Chowdhury. 2016. Deriving divide-and-conquer dynamic programming algorithms using solver-aided transformations. In
   OOPSLA. ACM, 145–164.
Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A Powerful,
   Sound, Predictable, Fast Veriﬁer for C and Java. In NASA Formal Methods (LNCS), Vol. 6617. Springer, 41–55.
Thomas Kleymann. 1999. Hoare Logic and Auxiliary Variables. Formal Asp. Comput. 11, 5 (1999), 541–566.
Etienne Kneuss, Ivan Kuraj, Viktor Kuncak, and Philippe Suter. 2013. Synthesis modulo recursive functions. In OOPSLA. ACM,
   407–426.
Viktor Kuncak, Mikaël Mayer, Ruzica Piskac, and Philippe Suter. 2010. Complete Functional Synthesis. In PLDI. 316–329.
Ton Chanh Le, Cristian Gherghina, Aquinas Hobor, and Wei-Ngan Chin. 2014. A Resource-Based Logic for Termination and
   Non-termination Proofs. In ICFEM (LNCS), Vol. 8829. Springer, 267–283.
Vu Le and Sumit Gulwani. 2014. FlashExtract: a framework for data extraction by examples. In PLDI. ACM, 542–553.
Xuan Bach Le and Aquinas Hobor. 2018. Logical Reasoning for Disjoint Permissions. In ESOP (LNCS), Vol. 10801. Springer,
   385–414.
Chin Soon Lee, Neil D. Jones, and Amir M. Ben-Amram. 2001. The size-change principle for program termination. In POPL.
   ACM, 81–92.
K. Rustan M. Leino. 2013. Developing veriﬁed programs with Dafny. In ICSE. ACM, 1488–1490.
K. Rustan M. Leino and Aleksandar Milicevic. 2012. Program Extrapolation with Jennisys. In OOPSLA. ACM, 411–430.
Chuck Liang and Dale Miller. 2009. Focusing and polarization in linear, intuitionistic, and classical logics. Theor. Comput. Sci.
   410, 46 (2009), 4747–4768.
Parthasarathy Madhusudan, Xiaokang Qiu, and Andrei Stefanescu. 2012. Recursive proofs for inductive tree data-structures.
   In POPL. ACM, 123–136.
Zohar Manna and Richard J. Waldinger. 1980. A Deductive Approach to Program Synthesis. ACM Trans. Program. Lang. Syst.
   2, 1 (1980), 90–121.
Per Martin-Löf. 1984. Intuitionistic Type Theory. Bibliopolis.
Andrew McCreight. 2009. Practical Tactics for Separation Logic. In TPHOLs (LNCS), Vol. 5674. Springer, 343–358.
Chris Mellish and Steve Hardy. 1984. Integrating Prolog in the POPLOG Environment. In Implementations of Prolog. 147–162.
Anders Miltner, Kathleen Fisher, Benjamin C. Pierce, David Walker, and Steve Zdancewic. 2018. Synthesizing bijective lenses.
   PACMPL 2, POPL (2018), 1:1–1:30.
Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2016. Viper: A Veriﬁcation Infrastructure for Permission-Based
   Reasoning. In VMCAI (LNCS), Vol. 9583. Springer, 41–62.
Vijayaraghavan Murali, Letao Qi, Swarat Chaudhuri, and Chris Jermaine. 2018. Neural Sketch Learning for Conditional
   Program Generation. In ICLR. To appear.
Aleksandar Nanevski. 2016. Separation Logic and Concurrency. (June 2016). Lecture notes for Oregon Programming Lan-
   guages Summer School (OPLSS). Available from http://software.imdea.org/~aleks/oplss16/notes.pdf .
Aleksandar Nanevski, Viktor Vafeiadis, and Josh Berdine. 2010. Structuring the veriﬁcation of heap-manipulating programs.
   In POPL. 261–274.


                                      Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
    :28                                                                          Nadia Polikarpova and Ilya Sergey

Huu Hai Nguyen, Cristina David, Shengchao Qin, and Wei-Ngan Chin. 2007. Automated Veriﬁcation of Shape and Size
   Properties Via Separation Logic. In VMCAI (LNCS), Vol. 4349. Springer, 251–266.
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
   In CSL (LNCS), Vol. 2142. Springer, 1–19.
Peter W. O’Hearn, Hongseok Yang, and John C. Reynolds. 2009. Separation and information hiding. ACM Trans. Program.
   Lang. Syst. 31, 3 (2009), 11:1–11:50.
Peter-Michael Osera and Steve Zdancewic. 2015. Type-and-example-directed program synthesis. In PLDI. ACM, 619–630.
Frank Pfenning. 2010. Lecture Notes on Focusing. (June 2010). Oregon Summer School on Proof Theory Foundations (OPLSS).
   Available from https://www.cs.cmu.edu/~fp/courses/oregon-m10/04-focusing.pdf .
Benjamin C. Pierce. 2002. Types and programming languages. MIT Press.
Ruzica Piskac, Thomas Wies, and Damien Zuﬀerey. 2014a. Automating Separation Logic with Trees and Data. In CAV (LNCS),
   Vol. 8559. Springer, 711–728.
Ruzica Piskac, Thomas Wies, and Damien Zuﬀerey. 2014b. GRASShopper - Complete Heap Veriﬁcation with Mixed Speciﬁca-
   tions. In TACAS (LNCS), Vol. 8413. Springer, 124–139.
Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. 2016. Program synthesis from polymorphic reﬁnement types. In
   PLDI. ACM, 522–538.
Oleksandr Polozov and Sumit Gulwani. 2015. FlashMeta: a framework for inductive program synthesis. In OOPSLA. ACM,
   107–126.
Xiaokang Qiu, Pranav Garg, Andrei Stefanescu, and Parthasarathy Madhusudan. 2013. Natural proofs for structure, data, and
   separation. In PLDI. ACM, 231–242.
Xiaokang Qiu and Armando Solar-Lezama. 2017. Natural synthesis of provably-correct data-structure manipulations. PACMPL
   1, OOPSLA (2017), 65:1–65:28.
Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark W. Barrett. 2015. Counterexample-Guided Quan-
   tiﬁer Instantiation for Synthesis in SMT. In CAV (Part II) (LNCS), Vol. 9207. Springer, 198–216.
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In LICS. IEEE Computer Society, 55–74.
Reuben N. S. Rowe and James Brotherston. 2017. Automatic cyclic termination proofs for recursive procedures in separation
   logic. In CPP. ACM, 53–65.
Gabriel Scherer. 2017. Search for Program Structure. In SNAPL (LIPIcs), Vol. 71. Schloss Dagstuhl - Leibniz-Zentrum fuer
   Informatik, 15:1–15:14.
Calvin Smith and Aws Albarghouthi. 2016. MapReduce program synthesis. In PLDI. ACM, 326–340.
Sunbeom So and Hakjoo Oh. 2017. Synthesizing Imperative Programs from Examples Guided by Static Analysis. In SAS
   (LNCS), Vol. 10422. Springer, 364–381.
Armando Solar-Lezama. 2013. Program sketching. STTT 15, 5-6 (2013), 475–495.
Saurabh Srivastava, Sumit Gulwani, and Jeﬀrey S. Foster. 2010. From program veriﬁcation to program synthesis. In POPL.
   ACM, 313–326.
Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction Proof in
   Separation Logic. In Formal Methods (LNCS), Vol. 9995. 659–676.
Emina Torlak and Rastislav Bodík. 2014. A lightweight symbolic virtual machine for solver-aided host languages. In PLDI.
   ACM, 530–541.
Rijnard van Tonder and Claire Le Goues. 2018. Static automated program repair for heap properties. In ICSE. ACM, 151–162.
Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and Thomas Dillig. 2017. SQLizer: query synthesis from natural language.
   PACMPL 1, OOPSLA (2017), 63:1–63:26.


A    PROOFS OF FORMAL GUARANTEES FOR THE SYNTHESIZED PROGRAMS
    Theorem A.1 (Theorem 3.3, Soundness of SSL). For any n, ∆ ′, if
   (i) Σ ′ ; Γ ; {P} { {Q}| c for a goal named f with formal parameters Γ , x i , and
  (ii) Σ ′ is such that coh (∆ ′, Σ ′, n), and 
 (iii) for all p 0 (ei ), ϕ; P, such that {P} = ϕ; p 0 (ei ) ∗ P , taking F , f (x i ) : ϕ; p 1 (ei ) ∗ ⌈P⌉ {⌈Q⌉ },
                                                                                         

       Σ ′, F ; Γ ; {P} c {Q} is n ′-valid for all n ′ < n wrt. ∆ , ∆ ′, f (ti x i ) { c },
then Σ ′ ; Γ ; {P} c {Q} is n-valid wrt. ∆.
   Proof. Since c has been produced by an SSL derivation, it is (;)-associated to the right.
   The proof is by the outer-level (well-founded) induction on the “footprint size” n. For each ﬁxed
n, the proof is by an inner-level induction on the structure of derivation Σ ′ ; Γ ; {P} { {Q}| c, with

    Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
Structuring the Synthesis of Heap-Manipulating Programs                                                       :29

symbolic one-step execution (via ). In that induction step we rely on the fact that the residual
“suﬃx” program is already valid, so we only need to show that applying a single rule preserves the
validity, while “appeding” a command c in front of an already synthesized program.
   The inner proof routine is straightforward for or (sub-)goals, where the spatial part of P contains
no predicate instances.
   All non-operational rules (Frame, Pick, SubstLeft, Emp, NullNotLVal, etc) either instantiate ex-
istentials in the post, weaken the pure obligations, or reduce the footprint, which is sound due to
locality of reading and writing (O’Hearn et al. 2001) and immutability of local variables; the sound-
ness of operational (Read, Write, etc) rules is due to the soundness of SL. Speciﬁcally:
• Case: Emp. The result follows immediately from Deﬁnition 3.1 of validity for any n.
• Case: SubstLeft. The result follows immediately from Deﬁnition 3.1 of validity for any n.
• Case: NullNotLVal. The non-nullness is encoded by the spatial precondition part (Reynolds 2002),
  so the transformation is sound. The result follows immediately from Deﬁnition 3.1 of validity for
  any heap size n.
• Case: StarPartial. The inequality of the two locations is encoded by the spatial part of the pre-
  condition, so the transformation is sound. The result follows immediately from Deﬁnition 3.1 of
  validity for any heap size n.
• Case: Inconsistency. The result follows immediately from Deﬁnition 3.1 of validity for any n, as
  no physical pre-heap does satisfy ϕ, so it is safe to emit error.
• Case: Frame. The Frame rule in SSL is diﬀerent from its counterpart in vanilla SL in that it does
  not require a side condition saying that R must not contain program variables that are modiﬁed
  by the program to be synthesized. Due to locality of read/write/malloc/free operations, they could
  not depend on R, as already synthesized in the residual program, hence adding R to post will not
  break validity, given that R is also added to the precondition.
• Case: Read. The synthesized read is safe, as the corresponding pointer is present in the precondi-
  tion. Furthermore, it creates a program-level variable, which substantiates the environment vari-
  able y, used for the synthesis in the subgoal, hence the new program is valid according to Deﬁni-
  tion 3.1.
• Case: Alloc. The subgoal has been synthesized in the larger footprint, aﬀorded by allocation. The
  soundness of the rule follows from the axiomatization of malloc (O’Hearn et al. 2001).
• Case: Free. Since the subgoal’s result is valid in a smaller pre-heap footprint and does not access
  any variables from R, it is safe to deallocate it, hence the resulting program is valid.
• Case: AbduceCall. The validity is by the properties of the sequential composition c 1 ; c 2 and the
  soundness of the frame rule of SL, applied as follows to the ﬁrst sub-goal:

                                        Σ; Γ ; {ϕ; F } { {ϕ; F ′ }| c 1
                               Σ; Γ ; {ϕ; F ∗ P ∗ R} { {ϕ; F ′ ∗ P ∗ R}| c 1

• Case: UnifyHeaps. Since the uniﬁcation only instantiates existentials, making the goal more spe-
  ciﬁc, and uniﬁed variables will not appear in the program freely, the validity is by soundness of
  the SL’s Auxiliary Variable Elimination rule (O’Hearn et al. 2001).
• Case: Pick. By the soundness of substitution and auxiliary variable elimination.
• Case: UnifyPure. By the soundness of substitution and auxiliary variable elimination.
• Case: SubstRight. By the soundness of substitution and auxiliary variable elimination.
• Case: Close. Validity follows from the fact that the sub-goal is valid in the presence of the elabo-
  rated postcondition {ψ ∧ [σ ]ξ k ∧ [σ ]χk ; Q ∗ R ′ }. By the deﬁnition of ΣI , this heap satisﬁes the
  corresponding predicate deﬁnition in the initial goal’s postcondition.

                               Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
  :30                                                                          Nadia Polikarpova and Ilya Sergey

In the case of predicate instances in the precondition, we take advantage of the tag machinery and
the assumptions (ii)–(iii) of the Theorem’s statement.
• Case: Induction. The assumption (ii) of the inductive hypothesis is satisﬁed via the initial assump-
  tion (iii) and 1-tagging of the recursive hypothesis’s precondition, so it will only be applicable to
  heaps of a size strictly smaller than n (follows from Open and Call).
• Case: Open. The validity is due to the fact that the emitted if-else will combine the sub-programs,
  that are already valid wrt. their pres/posts. The access to those elaborated pres/posts, ensuring the
  satisﬁability of the elaborated precondition in each branch is due to the conditionals ξ j , which are
  the same as the corresponding guard of the predicate instance being opened.
• Case: Call. This is the most interesting case. Validity of a function body’s substitution is via (ii).
  Notice that Call cannot be the ﬁrst rule applied in the derivation, as then all predicate instances are
  0-tagged, hence it should follow Open, which unfolds the instances, exposing smaller sub-heaps
  captured by their clauses (due to well-foundedness of the predicates), which are now amenable for
  using Call on them.
  The remaining reasoning diﬀers depending on whether the function f being called is a user-
  provided auxiliary one, or a recursive call to the top-level goal. If a function being applied is a
  user-provided speciﬁcation (i.e., not a recursive self), then its validity is asserted by the second
  clause of Deﬁnition 3.2, otherwise the call is recursive, and will only take place on a smaller heap,
  satisfying the third option of Deﬁnition 3.2.
                                                                                                        




  Proc. ACM Program. Lang., Vol. 1, No. 1, Article . Publication date: November 2018.
