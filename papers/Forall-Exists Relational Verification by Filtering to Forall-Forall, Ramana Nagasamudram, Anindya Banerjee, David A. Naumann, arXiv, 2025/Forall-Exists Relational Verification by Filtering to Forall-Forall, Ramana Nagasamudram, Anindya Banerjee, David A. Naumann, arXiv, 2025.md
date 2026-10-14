                                        Forall-Exists Relational Verification by Filtering to
                                        Forall-Forall [with appendix]
                                        RAMANA NAGASAMUDRAM∗ , Amazon Web Services, USA
                                        ANINDYA BANERJEE† , Dartmouth College, USA
                                        DAVID A. NAUMANN‡ , Stevens Institute of Technology, USA
                                        Relational verification encompasses research directions such as reasoning about data abstraction, reasoning
                                        about security and privacy, secure compilation, and functional specificaton of tensor programs, among others.
arXiv:2509.04777v1 [cs.LO] 5 Sep 2025




                                        Several relational Hoare logics exist, with accompanying tool support for compositional reasoning of ∀∀
                                        (2-safety) properties and, generally, k-safety properties of product programs. In contrast, few logics and tools
                                        exist for reasoning about ∀∃ properties which are critical in the context of nondeterminism.
                                           This paper’s primary contribution is a methodology for verifying a ∀∃ judgment by way of a novel filter-
                                        adequacy transformation. This transformation adds assertions to a product program in such a way that the
                                        desired ∀∃ property (of a pair of underlying unary programs) is implied by a ∀∀ property of the transformed
                                        product. The paper develops a program logic for the basic ∀∃ judgement extended with assertion failures;
                                        develops bicoms, a form of product programs that represents pairs of executions and that caters for direct
                                        translation of ∀∀ properties to unary correctness; proves (using the logic) a soundness theorem that says
                                        successful ∀∀ verification of a transformed bicom implies the ∀∃ spec for its underlying unary commands;
                                        and implements a proof of principle prototype for auto-active relational verification which has been used to
                                        verify all examples in the paper. The methodology thereby enables a user to work with ordinary assertions
                                        and assumptions, and a standard assertion language, so that existing tools including auto-active verifiers can
                                        be used.

                                        1   Introduction
                                        Many desirable properties of programs are naturally expressed as relational properties, that is,
                                        conditions that relate multiple executions. One commonly occurring pattern specifies that for any
                                        pair of terminating runs, if the initial states satisfy a specified relational precondition then the final
                                        states satisfy a specified post-relation. This pattern is known as ∀∀ or 2-safety. The pairs of runs
                                                                                                                                    ∀
                                        could be from two different programs 𝑐 and 𝑐 ′ , in which case we will write 𝑐 | 𝑐 ′ : R ≈> S where R
                                        (resp. S) is the pre- (resp. post-) relation. Examples include observational equivalence, where R
                                        and S are the identity on states, which has many applications. A well known example that relates
                                        a program to itself is noninterference, a security property with respect to a partition of variables
                                        into secret or public: take R and S to be agreement on the values of public variables.
                                            Nondeterminacy is important in imperative programming, even in the absence of concurrency:
                                        it can represent unknown inputs and underspecified procedures, and it can approximate random-
                                        ization. For nondeterministic programs a commonly occuring relational pattern, which we write
                                                     ∃
                                        𝑐 | 𝑐 ′ : R ≈> S, says that for R-related initial states, all runs of 𝑐 can be matched by some run of 𝑐 ′
                                        that establishes S finally. Examples include trace refinement and generalized noninterference. We
                                                                                                                           ∀
                                        refer to this as a ∀∃ property, by contrast with the ∀∀ property written R ≈> S.

                                        ∗ Nagasamudram’s work was done prior to his joining Amazon Web Services.
                                        † Banerjee’s research was based on work supported by the NSF, while working at the Foundation. Any opinions, findings,

                                        and conclusions or recommendations expressed in this article are those of the authors and do not necessarily reflect the
                                        views of the NSF.
                                        ‡ Naumann was partially supported by NSF grant CNS 2426414.



                                        Authors’ Contact Information: Ramana Nagasamudram, Amazon Web Services, USA; Anindya Banerjee, Dartmouth College,
                                        USA; David A. Naumann, Stevens Institute of Technology, USA.
2                                            Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


    The ∀∃ pattern also arises in more general form, where multiple runs are universally and/or
existentially quantified and the tuple of traces is constrained at intermediate points not just final.
However, the case of two runs and pre-post spec is ubiquitous and illustrates key issues; we focus on
it in this paper since it admits more streamlined notations. Owing to the broad range of applications,
relational verification is an active research area. There have been considerable advances for ∀∀
verification (also known as 𝑘-safety) but relatively little for ∀∃ which is the focus of this paper.
    Stepping back, let us recall the state of the art in “unary” (non-relational) verification, i.e.,
trace properties. There are several established means of formal specification including temporal
logics. Most relevant here are partial correctness assertions (Hoare triples) given by pre- and
post-conditions. For such specifications, verification techniques include: fully automated tools
based on proof search or direct semantic reasoning; auto-active tools in which users provide loop
invariants, procedure specs, and other annotations; and use of interactive proof assistants for direct
semantic reasoning or application of Hoare logic in its many variations [17, 42]. The state of the
art in relational verification is less advanced but some techniques have emerged.
    One widely used principle is alignment, in which two runs are viewed as matched sequences of
segments: put differently, relational assertions are associated with aligned pairs of intermediate
points. For ∀∀ this directly generalizes the inductive assertion method [31]. Most often the aligned
pairs are designated in terms of program control structure, but in addition they may be designated
by state-dependent conditions. (Sometimes called semantic alignment.) Good alignment often
enables the use of simple relational assertions in solvable first order fragments [55].
    Another key principle is product programs to represent multiple runs by a single one. This has
mostly been explored for ∀∀ properties, where a product of programs (or transition systems) serves
straightforwardly to reduce the problem to ordinary verification and thereby leverage existing
tools. Products in the form of code can enable users to express useful alignments [8], and can serve
as a framework in which to search for good alignments [2, 24].
    This paper addresses ∀∃ properties for which the state of the art is less advanced. We leave aside
model checking of finite state systems and focus on imperative programs acting on general data
structures. One verification approach is direct semantic reasoning [45]. For code and specifications
in solvable assertion languages there have been exciting advances in fully automated verification,
e.g., constraint solving to find relational invariants and alignment conditions [41, 59], with programs
represented by transition relations. But solvability is a strong restriction: specs are usually quantifier
free and the programs do linear arithmetic on integer variables, or are sufficiently similar that data
operations can be abstracted by uninterpreted functions.
    For much richer languages, refinement-oriented logics have been developed based on the Iris
separation logic which is implemented in the Rocq proof assistant [42]. For sequential imperative
programs, the recent ∀∃ logics RHLE and FERL have bespoke features to cater for automated proof
search [15, 25]. It is safe to say no ∀∃ logic has emerged as a standard. By contrast, for simple
imperative programs the core rules of Hoare logic are widely used (with minor variations). For
∀∀, basic rules like those of Benton’s Relational Hoare Logic [13] are well known; they include
syntax-directed rules that support compositional reasoning and orthogonal treatment of program
constructs.
    When formal verification of general programs is done in industry, it often relies on auto-active
tools like Dafny [46], Why3 [30], and Viper [49] (also called deductive verifiers). Some of these
have been adapted to ∀∀ verification (e.g., [29, 50]). But we are not aware of such tools for ∀∃. The
work reported here aims to help fill that gap.
    Our starting point is the observation that judicious use of assumptions in a product program can
serve to reduce a ∀∃ property to a ∀∀ property of the product by filtering out executions that are
not helpful to witness the existential [2, 52]. Free use of assumptions is unsound, so some additional
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                    3


checks are needed to justify the assumptions and also ensure the right (existential) side does not
diverge when the left side terminates. This is called adequacy of the product with respect to the
specification of interest. Our conceptual contribution is a transformation that adds assertions to a
product program in such a way that the desired ∀∃ property (of underlying unary programs) is
implied by a ∀∀ property of the transformed product. The transformation is applicable so long as
nondeterminacy is made explicit in the form of standard havoc statements. It enables ∀∃ verification
in which the user works with ordinary assertions and assumptions, and an ordinary assertion
language —opening the door to use of existing tools including but not limited to auto-active verifiers.
The idea is developed through the following technical contributions.

     A program logic for the basic ∀∃ judgement extended to avoidance of failures, which is
       needed to support assertions. By contrast with the aforementioned ∀∃ logics, it supports
       fully general data dependent loop alignments and the rules are relatively simple. The logic
       is adapted from a recent work on alignment [52].
     Bicoms: a form of product programs that caters for direct translation of ∀∀ properties to unary
       correctness. They have a big-step semantics easily translated to intermediate verification
       languages used by auto-active verifiers. Moreover they support weakest liberal preconditions
       (wlp) that satisfy equations similar to standard wlp though more complicated because the
       loop construct supports data dependent alignments. To facilitate the next contribution,
       there is a bicom contruct that combines havoc (on the right side) with an assumption.
     The filter-adequacy transformation which formalizes the conceptual contribution: it adds
       assertions to check ∀∃-adequacy of a product program. The main result is a soundness
       theorem which confirms that successful ∀∀ verification of a transformed bicom implies the
       ∀∃ spec for its underlying (unary) commands. This achievement required clean formulation
       of fresh variables and framing results for bicom wlp. The soundness theorem is proved in
       detail in a readable way that highlights how verification conditions provide ingredients of
       deductive proof in the program logic. The theorem has also been fully mechanized in Rocq.
     A proof of principle prototype that implements the filter-adequacy transformation as well
       as compilation of bicoms to ordinary programs with assertions and assumptions. The latter
       are verified using an existing verification tool based on verification conditions and SMT
       solving, in accord with our goal to advance auto-active relational verification.

The soundness theorem connects the validity of a ∀∀ property with validity of the desired ∀∃
property. Thus it is applicable regardless of how the ∀∀ property verified. For that matter, one could
use testing of the transformed bicom, to obtain some evidence of the ∀∀ property which would be
evidence of the ∀∃ property. (Direct testing of ∀∃ is problematic [20].)
   The soundness of state of the art auto-active and automated tools is typically established, if at all,
through informal arguments, although some recent advances provide machine checked foundations
for components of auto-active tools [19, 23]. Our theorem is for a simple core language but the
structure of its proof, centering on a general ∀∃ relational Hoare logic, appears well suited to use
with richer programming languages and a variety of assertion languages.
   The rest of the paper is structured as follows. Section 2 uses examples to introduce some key
ideas. Sections 3–6 develop the technical contributions in the order listed above. Section 7 discusses
related and future work.
   There are a number of technical challenges due to handling general data-dependent loop align-
ment (by contrast with more restrictive product forms in prior work such as the ∀∀ products
of Dickerson et al. [24]). Other challenges arise due to the presence of failure: Although our bicoms
are similar to alignment products in prior works, failure invalidates the key left-right commute
4                                                 Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


property they use [2, 24], and one established way to handle failure in a product semantics [6] is
precluded by need for a straightforward translation of bicoms to ordinary programs.

2   Overview
This section provides an informal overview of ∀∃ verification. For each example, we look at the
verification problem, a bicom that captures an alignment, and an instrumented bicom for which
one establishes correctness. This implies, via the paper’s main theorem, the ∀∃ spec for the original
pair of commands.
    An introductory example: illustrating filtering. Let 𝑐, 𝑐 ′ be the commands hav 𝑥, hav 𝑦. (The
                                                                                                   ∃
examples act on integer variables.) Consider this verification problem: 𝑐 | 𝑐 ′ : true ≈> 𝑥 =           ¥ 𝑦 which is
our notation for a ∀∃ spec with precondition 𝑡𝑟𝑢𝑒. The postcondition, 𝑥 =                ¥ 𝑦, says that the value of
𝑥 in the left (∀) execution equals the value of 𝑦 on the right (∃). Ignoring failure, the correctness
judgment holds provided that for any states 𝑠, 𝑠 ′, 𝑡, if 𝑐 executed in 𝑠 (written 𝑐/𝑠) terminates in 𝑡,
there exists state 𝑡 ′ such that 𝑐 ′ /𝑠 ′ terminates in 𝑡 ′ and 𝑡 (𝑥) = 𝑡 ′ (𝑦).
    Given 𝑐, 𝑐 ′ , the embed bicom ⟨𝑐 | 𝑐 ′ ⟩ is a product that represents pairs of their executions. The
bicom spec true {       ¥ 𝑥= ¥ 𝑦 means that for any pair of states 𝑠, 𝑠 ′ , ⟨𝑐 | 𝑐 ′ ⟩/(𝑠, 𝑠 ′ ) does not fail and if
⟨𝑐 | 𝑐 ′ ⟩/(𝑠, 𝑠 ′ ) terminates in the pair of states (𝑡, 𝑡 ′ ) then 𝑡 (𝑥) = 𝑡 ′ (𝑦). As stated, bicom correctness
is essentially a ∀∀ property. For our example, the spec clearly does not hold for ⟨𝑐 | 𝑐 ′ ⟩: owing to
nondeterminism in both hav 𝑥 and hav 𝑦, 𝑡 (𝑥) and 𝑡 ′ (𝑦) need not agree.
    To achieve bicom correctness we introduce a filtering condition. The intuition is that such a
“filtered” bicom captures all executions of 𝑐 on the left but keeps only those executions of 𝑐 on the
right for which the filtering condition 𝑥 =       ¥ 𝑦 is met, that is, the havoc’d 𝑦 on the right equals the
havoc’d value of 𝑥 on the left. Havocing 𝑥 on the left is accomplished using the bicom ⟨hav 𝑥 | skip⟩.
Incorporating the filtering condition is accomplished using the havoc-filter bicom havf 𝑦 (𝑥 =                   ¥ 𝑦)
which abbreviates ⟨skip | hav 𝑦⟩; assume (𝑥 =        ¥ 𝑦). Here is the overall filtered bicom:
                                        ⟨hav 𝑥 | skip⟩ ; havf 𝑦 (𝑥 =
                                                                   ¥ 𝑦)
The havf bicom assumes 𝑥 =   ¥ 𝑦, but free use of assumptions is unsound for our purpose: one could
                                                      ¥ 𝑥=
use ⟨hav 𝑥 | skip⟩; havf 𝑦 false which satisfies true {    ¥ 𝑦 at the cost of having no executions at
all. Its correctness does not imply the desired ∀∃ spec. What we need is that there exists at least
one value of 𝑦 on the right that agrees with 𝑥’s value on the left. This can be ensured by adding an
assertion preceding the havf, like this:
                              ⟨hav 𝑥 | skip⟩ ; assert ∃ |𝑦. 𝑥 =
                                                              ¥ 𝑦 ; havf 𝑦 (𝑥 =
                                                                              ¥ 𝑦)
Here ∃ |𝑦. . . . expresses quantification over 𝑦 on the right side. This bicom is correct, that is, it
satisfies true {  ¥ 𝑥=¥ 𝑦 which in particular expresses that there is no assertion failure. Moreover
correctness is easily checked with any ordinary verification technique or tool: The bicom can be
translated to an ordinary command, interpreting the embed construct as sequence and renaming
the two sides apart.
   Later we will show that the step of adding the assertion is performed by the filter-adequacy
transformation, which is called chk for short. The main result of the paper is that if a bicom spec
such as true {   ¥ 𝑥=¥ 𝑦 holds for a transformed bicom then the underlying commands satisfy the
                          ∃
∀∃ spec which is true ≈> 𝑥 = ¥ 𝑦 in this case. The connection with the original commands hav 𝑥 and
hav 𝑦 is a matter syntactically projecting out the unary parts, discarding relational assertions and
discarding the assumption part of havf.
   Now consider a variation on the example: let 𝑐 ′ be hav 𝑦; 𝑦 := 2 · 𝑦. Filtering is only helpful in
connection with nondeterminacy so we consider this bicom: ⟨hav 𝑥 |skip⟩; havf 𝑦 . . . ; ⟨skip|𝑦 := 2·𝑦⟩.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                           5


    z := 0; w := 0;                             ⌊ z := 0 ⌋; ⌊ w := 0 ⌋;
    while x > 0 do                              while x > 0 | x > 0 .
      if w = 0 then                                 ⟨[ w ≠ 0 ⟨] | [⟩ w ≠ 0 ]⟩ do variant { [⟩ (n - w) mod n ]⟩ }
        hav z;                                    if w = 0 | w = 0 then
        x := x - 1;                                   < hav z | skip >;
      end;                                                       ¥ z };
                                                      havF z { z =
      w := (w + 1) mod n                              ⌊ x := x - 1 ⌋;
    done;                                         end;
                                                  ⌊ w := (w + 1) mod n ⌋;
                                                done;

Fig. 1. Program 𝑐1 and a bicom for two copies of 𝑐1. Notation such as ⌊ z := 0 ⌋ denotes bicom ⟨𝑧 := 0 | 𝑧 :=
0⟩. Notation ⟨[𝑤 ≠ 0 ⟨] means 𝑤 ≠ 0 in the left state; [⟩𝑤 ≠ 0 ]⟩ means 𝑤 ≠ 0 in the right state.


What should the elided assumption be? If we use 𝑥 =𝑦,   ¥ the assertion added by chk will be as before,
and will not fail. But that assumption does not support successful verification of true {      ¥ 𝑥= ¥𝑦
because of course from 𝑥 =𝑦  ¥ the assignment to 𝑦 establishes 𝑥 =𝑦/2.
                                                                   ¥      This suggests the assumption
should be 𝑥 =  ¥ 2 · 𝑦 which does suffice to prove the postcondition. But now chk inserts the assertion
∃ |𝑦. 𝑥 =
        ¥ 2 · 𝑦 which fails because not all integers are even. Indeed, the example commands do not
               ∃
satisfy true ≈> 𝑥 =  ¥ 𝑦.
   Conditionally aligned loops: illustrating loop variant on right. We now discuss an example involving
conditionally aligned loops. Consider the unary program 𝑐1 shown in Figure 1 (using concrete
syntax of the prototype which has been used to verify the examples). This program havocs 𝑧, 𝑥
many times, but does so in a loop that stutters. We assume 𝑛 > 0 on both sides, but not 𝑛 =    ¥ 𝑛. That
is, we aim to show
                                                                        ∃
                             𝑐1 | 𝑐1 : ⟨[𝑛 > 0 ⟨] ∧ [⟩𝑛 > 0 ]⟩ ∧ 𝑥 =
                                                                   ¥ 𝑥 ≈> 𝑧 =
                                                                            ¥𝑧                        (1)
where ⟨[𝑛 > 0 ⟨] (resp. [⟩𝑛 > 0 ]⟩ ) says the right (resp. left) state satisfies 𝑛 > 0.
   Figure 1 shows a bicom for the pair 𝑐1 |𝑐1. The bicom follows a common heuristic: aligning similar
control structures. The notation if...|... indicates that two if-commands are aligned. It represents
all the possible combinations of then/else execution paths. The so-called bi-while represents two
related loops, but with an extra feature: left and right alignment conditions, here ⟨[𝑤 ≠ 0 ⟨] and
[⟩𝑤 ≠ 0 ]⟩ . The aligned loop body includes a filtering condition for hav 𝑧 that assumes 𝑧 =        ¥ 𝑧. The
conditionally aligned loop works as follows. Reason about a left-only iteration when 𝑤 ≠ 0 holds
in the left state; reason about a right-only iteration when 𝑤 ≠ 0 holds in the right state. That is,
only the left or right side underlying execution takes effect. In both cases, the example loop’s effect
is to modify (increment) 𝑤 but to leave 𝑧 unchanged. When both alignment conditions are false,
that is, when 𝑤 = 0 in both the left and right states, we reason about the loop bodies in lockstep.
The keyword variant introduces an annotation used by the chk function; it has no effect on the
meaning of the bicom.
   The variant [⟩ (𝑛 − 𝑤) 𝑚𝑜𝑑 𝑛 ]⟩ is an integer expression evaluated in the right state. Note that it
is not a conventional variant: execution on the right does not always decrease the value. It does,
however, decrease when [⟩𝑤 ≠ 0 ]⟩ is true, and that is the only condition under which right-only
iteration occurs. Here is the point. In a sequence that intersperses left-only, right-only, and joint
executions of the loop body, divergence on the left, or jointly, cannot falsify a ∀∃ property, but
divergence on the right alone can do so. The chk transformation must preclude such divergence.
   The result of applying chk on the bicom in Figure 1 is shown in Figure 2. Variable rosnap snapshots
the truth value of the condition [⟩𝑤 ≠ 0 ]⟩ under which the current iteration will be right-only, and
vsnap snapshots the variant. The added assertion requires the variant to decrease during right-only
iterations. The chk’d bicom can be verified for ⟨[𝑛 > 0 ⟨] ∧ [⟩𝑛 > 0 ]⟩ ∧ 𝑥 =      ¥𝑥 { ¥ 𝑧=
                                                                                           ¥ 𝑧, so the main
theorem implies (1).
6                                              Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


    ⌊ z := 0 ⌋; ⌊ w := 0 ⌋;
    while x > 0 | x > 0 . ⟨[ w ≠ 0 ⟨] | [⟩ w ≠ 0 ]⟩ do variant { [⟩ (n - w) mod n ]⟩ }
      var vsnap : int, rosnap : bool in
      vsnap := (n - w) mod n; /* added by chk: snapshot variant */
      rosnap := [⟩ w ≠ 0 ]⟩ ; /* added by chk: snapshot of w ≠ 0 on right */
      if w = 0 | w = 0 then
         < hav z | skip >;
         assert { ∃ |z. z =¥ z }; /* added by chk */
                    ¥ z };
         havF z { z =
         ⌊ x := x - 1 ⌋;
      end;
      ⌊ w := (w + 1) mod n ⌋;
      /* added by chk: assert variant decreases under right-only iterations */
      assert { rosnap ⇒ [⟩ 0 ≤ (n - w) mod n < vsnap ]⟩ };
    done;

                         Fig. 2. The chk function applied to the bicom in Figure 1.


  Possibilistic noninterference: illustrating may termination (right-sided divergence). The preceding
examples are terminating programs. The next example, adapted from Unno et al. [59], involves
loops that can diverge. We refer to it as 𝑐2 :
                if high ≠ 0 then hav 𝑥; if 𝑥 ≥ low then skip else (while 𝑡𝑟𝑢𝑒 do skip)
                else 𝑥 := low; hav 𝑏; (while (𝑏 ≠ 0) do 𝑥 := 𝑥 + 1; hav 𝑏)
                                           ∃
   We aim to show 𝑐2 | 𝑐2 : low =
                                ¥ low ≈> 𝑥 =
                                           ¥ 𝑥. All four combinations of initial values of high must
be considered, and different alignments are needed in the different case. Whereas the previous
example used loop alignment conditions to express a data dependent alignment, here the desired
alignments are expressed using bi-if, a 4-way conditional
                        if (high ≠ 0 | high ≠ 0) thth 𝐵 1 thel 𝐵 2 elth 𝐵 3 elel 𝐵 4 fi
with suggestively named bicoms 𝐵 2, . . . , 𝐵 4 shown in Figure 3. For example, when high ≠ 0 (sym-
metrically high = 0) in both initial states, use lockstep alignment (Figure 3 (𝐵 1 )). Alternatively,
if high ≠ 0 in the left initial state but high = 0 in the right initial state, use sequential, left-first
alignment (Figure 3 (𝐵 2 )). Note the possibility of nontermination of the left execution when 𝑥 < low.
If the left execution does terminate, 𝑥 ≥ 𝑙𝑜𝑤 can be asserted. In the right execution, the WhileR
bicom abbreviates the standard while bicom where the left loop test and left alignment conditions
are false, but the right alignment condition is true. (Recall from the previous example that when a
left (resp. right) alignment condition holds, the bicom does a left (resp. right)-only iteration; for
lockstep iterations, both left and right alignment conditions are false.) In essence, this is a sequential
right-execution of the loop, but written in a form that allows havf to be used. Instead of proving
(must) termination of all executions, we prove the existence of a terminating right execution (may
termination). This is done by filtering right executions to only allow those where hav 𝑏 sets the
value of 𝑏 in the right state (written [⟩𝑏 ]⟩ ) to the difference of 𝑥’s values in the left and right states,
and maintaining [⟩𝑏 ]⟩ as variant: filtering forces [⟩𝑏 ]⟩ to decrease in every iteration. The descriptions
of 𝐵 3 and 𝐵 4 are similar. In 𝐵 3 , the WhileL bicom abbreviates the standard while bicom where the
right loop test and right alignment condition are false, but the left alignment condition is true.
   Finally, to validate the assumptions in havf bicoms, chk introduces assertions (elided in Figure 3)
preceding them. For example, assert ∃ |𝑏. [⟩𝑏 ]⟩ = ⟨[𝑥 ⟨] − [⟩𝑥 ]⟩ in 𝐵 2 .
   In this overview section we are glossing over the projections that connect a bicom with the
underlying commands. In the case of bi-if, this imposes constraints, for example the left projections
of 𝐵 1 and 𝐵 2 should be essentially the same.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                             7


      (B1) <hav x | skip>; havF x { x =¥ x};                  (B2) <hav x | skip>;
           if x ≥ low | x ≥ low then                               <if x ≥ low then skip
             ⌊ skip ⌋                                               else while true do skip done
           else                                                    | skip>;
             <while true do skip done | skip>;                     <skip | x := low>;
                                                                   havF b { [⟩ b ]⟩ = ⟨[ x ⟨] - [⟩ x ]⟩ };
                                                                   WhileR b ≠ 0 do
                                                                     variant { [⟩ b ]⟩ }
                                                                     <skip | x := x+1>;
                                                                     havF b { [⟩ b ]⟩ = ⟨[ x ⟨] - [⟩ x ]⟩ }
                                                                   done;

      (B3) <x := low; hav b | skip>;                          (B4) ⌊ x := low ⌋;
           WhileL b ≠ 0 do                                                                    ¥ b };
                                                                   <hav b | skip>; havF b { b =
              <x := x+1; hav b | skip>;                            while b ≠ 0 | b ≠ 0 do
           done;                                                     ⌊ x := x+1 ⌋;
                      ¥ x };
           havF x { x =                                                                         ¥ b };
                                                                     <hav b | skip>; havF b { b =
           <skip | if x ≥ low then skip>                           done;

                          Fig. 3. Bicoms 𝐵 1 . . . 𝐵 4 capture different alignments of 𝑐2 | 𝑐2.


   Summary. The filter-adequacy transformation supports the following methodology for verifying
                           ∃
a ∀∃ judgment 𝑐 | 𝑐 ′ : R ≈> S.
    (1) Find a bicom 𝐵 that represents 𝑐, 𝑐 ′ in the sense that it’s projections are semantically
        equivalent to 𝑐 and 𝑐 ′ . Moreover 𝐵 should represent a helpful alignment in which right-side
        havocs are accompanied by filter assumptions, and simple relational invariants can be used.
        Finding 𝐵 is not the focus of this paper; it can be done with user guidance or automated
        search, possibly using equivalence-preserving rewriting ⟨𝑐 | 𝑐 ′ ⟩ as discussed in under related
        work (Section 7). A conservative check for the semantic equivalences is that 𝑐, 𝑐 ′ should be
        the syntactic projections of 𝐵, and this was sufficient in our experience.
    (2) Transform 𝐵 by applying chk. This is a simple linear time transformation.
    (3) Attempt to verify the ∀∀ property chk(𝐵) : R {    ¥ S. As discussed under related work, ∀∀
        verification of well aligned products is amenable to automation.
                                                    ∃
If verification is successful then 𝑐 | 𝑐 ′ : R ≈> S holds by the main theorem of the paper. Otherwise,
find another 𝐵 to try.

3   Programs and a ∀∃ relational program logic
This section defines the syntax and semantics of commands and the relational correctness properties
of interest. Then some proof rules for ∀∃ correctness are given.
   We treat assertions and relations by shallow embedding,1 i.e., as sets of stores and relations
on stores rather than syntactic formulas. This is done both in specifications (Section 3.2) and in
code, specifically in assert commands and the havf construct. Use of shallow embedding provides
generality, in that our results are not tied to a specific assertion language. A key benefit is that
weakest preconditions can be defined in the ambient logic, which avoids the need to consider
expressiveness issues [3]. In the paper the ambient logic is ordinary logic and set theory. In the
mechanization, the ambient logic is that of Rocq.2 Given that the program syntax has “semantic”
assertions in this manner, we also choose shallow embedding of expressions in code. This precludes
reasoning by structural induction on expressions or assertions but we have no need for that.
   We do need logical operations like quantification and substitution for assertions and relations.
We sketch key definitions, which amount to the usual semantics of predicate logic formulas, and
1 Readers not familiar with shallow embedding can consult [53] or the chapter Hoare.v in [54]. See also [60].
2 Making use of these standard libraries: Classical, FunctionalExtensionality, and PropExtensionality.
8                                                  Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


          𝑠 |= 𝑝                   𝑠 ̸ |= 𝑝                  𝑛∈Z                  𝑐/𝑠 ⇓ 𝑡     𝑑/𝑡 ⇓ 𝜙
      assert 𝑝/𝑠 ⇓ 𝑠           assert 𝑝/𝑠 ⇓           hav 𝑥/𝑠 ⇓ 𝑠 [𝑥 ↦→ 𝑛]             𝑐; 𝑑/𝑠 ⇓ 𝜙
      Fig. 4. Semantics of selected commands. The outcome 𝜙 ranges over the disjoint union Store ∪ { }.


any missing details can be found in the Rocq development. We use conventional syntactic notations
for expressions and assertions, for example 𝑝 ∧ 𝑞 instead of 𝑝 ∩ 𝑞. So the casual reader can ignore
fine points about shallow embedding.

3.1     Assertions and commands
We assume given sets boolVar and intVar that are disjoint and both denumerable. Metavariables
𝑥, 𝑦, . . . range over boolVar ∪ intVar. A store is a total function from boolVar ∪ intVar to values that
maps integer variables to Z and boolean variables to {tt, ff}. The set of all stores is named Store.
An integer (resp. boolean) expression 𝑒 is a total function Store → Z (resp. Store → {tt, ff}. We
write 𝑠 [𝑥 ↦→ 𝑛] for the update of store 𝑠 to map 𝑥 to value 𝑛. An assertion 𝑝 is a subset 𝑝 ⊆ Store.
   As mentioned earlier, we use ordinary formula syntax for logical operations. For example we
write 𝑝 ⇒ 𝑞 instead of (Store \ 𝑝) ∪ 𝑞. Let ⇒ bind less tightly than ∧ and ∨. For assertion 𝑝 we
write 𝑝𝑒𝑥 for semantic substitution: 𝑝𝑒𝑥 is defined to be {𝑠 | 𝑠 [𝑥 ↦→ 𝑒 (𝑠)] ∈ 𝑝}. This enjoys standard
properties of syntactic substitution, e.g., distributing through boolean operators. Quantifiers, as
operators on store sets, are defined by ∀𝑥 . 𝑝 =       ˆ {𝑠 | 𝑠 ∈ 𝑝 𝑥𝑣 for all 𝑣 ∈ Z} and ∃𝑥 . 𝑝 = ˆ {𝑠 |
𝑠 ∈ 𝑝 𝑣 for some 𝑣 ∈ Z}. Here and in the sequel we use words to distinguish metalanguage from
       𝑥

the operators on assertions; but sometimes we use symbols for metalanguage when needed for
succinctness (e.g., in Definition 4.11). In some contexts we implicitly convert a boolean expression
𝑒 to the assertion {𝑠 | 𝑒 (𝑠) = tt}.
   Commands are given by this grammar, where 𝑒 ranges over expressions and 𝑝 over assertions.
                   𝑐 ::= skip | 𝑥 := 𝑒 | hav 𝑥 | assert 𝑝 | 𝑐; 𝑐 | if 𝑒 then 𝑐 else 𝑐 | while 𝑒 do 𝑐
We assume without further comment that commands are type correct, e.g., conditional tests are
boolean expressions and in 𝑥 := 𝑒 the expression has the right type for the variable 𝑥.
    The evaluation semantics of commands is entirely standard. Throughout the paper identifiers
𝑠, 𝑡, 𝑢 range over stores. The outcome (pronounced fail) represents assertion failure which is the
only form of runtime failure in our idealized language. The relation 𝑐/𝑠 ⇓ 𝜙 says that from initial
store 𝑠 the command yields outcome 𝜙. A few cases are in Figure 4. We write 𝑠 |= 𝑝 for 𝑠 ∈ 𝑝.

3.2     Relations and relational correctness judgments
A Store relation (relation, for short) is a subset R ⊆ Store × Store. Relations are ranged over
by identifiers P, Q, R, S, . . .. The requisite operations include the following: quantification over
variables on the left (written ∀𝑥 | . R and ∃𝑥 | . R), on the right (∀|𝑥 . R and ∃ |𝑥 . R), an assertion on
the left (written ⟨[𝑝 ⟨] ) or right ( [⟩𝑝 ]⟩ ), and of course ∧, ⇒, . . . . We also use the form 𝐸 ⊕ 𝐸 where
𝐸 ranges over two-state expressions and ⊕ ranges over primitive relations including equality
and inequality. Two-state expressions are integer-valued expressions that depend on a pair of
states. To be precise, we let 𝐸 range over functions Store × Store → Z, and we write two-state
expressions using the left and right embeddings of unary expressions. These embeddings are
defined by ⟨[𝑒 ⟨] =  ˆ (𝑠, 𝑡) ↦→ 𝑒 (𝑠) and [⟩𝑒 ]⟩ =   ˆ (𝑠, 𝑡) ↦→ 𝑒 (𝑡). (This avoids cluttered notations found
in other works that rely on renaming to encode pairs of states as a single state.)
   For assertions, the form ⟨[𝑝 ⟨] (resp. [⟩𝑝 ]⟩ ) says the left (resp. right) store satisfies unary assertion 𝑝.
That is, ⟨[𝑝 ⟨] = {(𝑠, 𝑡) | 𝑠 ∈ 𝑝} and [⟩𝑝 ]⟩ = {(𝑠, 𝑡) | 𝑡 ∈ 𝑝}. As an example, ⟨[𝑥 ⟨] > 0 says the value of
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                  9


𝑥 on the left is positive, which is equivalent to ⟨[𝑥 > 0 ⟨] . Another example is ⟨[𝑥 ⟨] > [⟩𝑦 ]⟩ + 1. We
        ¥ 𝑒 ′ as abbreviation of ⟨[𝑒 ⟨] = [⟩𝑒 ′ ]⟩ .
write 𝑒 =
  The quantifier forms use 𝑥 | (resp. |𝑥) to indicate quantification on the left (resp. right). For relation
R on stores we write R𝑒𝑥|| for substitution of 𝑒 for 𝑥 in the left store. Similarly R ||𝑒𝑥 substitutes on
                                                                                                                      ′
the right. The definitions are a straightforward generalization of unary substitution: (𝑠, 𝑡) ∈ R ||𝑒𝑥′
iff (𝑠, 𝑡 [𝑥 ′ ↦→ 𝑒 ′ ]) ∈ R. We write ∃𝑥 | . R for existential quantification over 𝑥 on the left side:
 ∃𝑥 | . R =  ˆ {(𝑠, 𝑠 ′ ) | (𝑠, 𝑠 ′ ) ∈ R 𝑥𝑣 || for some 𝑣 ∈ Z}. Similarly for the right side and for universal
quantification. These operations enjoy the usual properties of corresponding operations on formulas,
e.g., R |𝑒|𝑥 = R if R does not depend on 𝑥, which is made precise in Lemma 4.12. Note that we often
use primed identifiers, simply as mnemonic for things on the right.
   An assertion is valid, written |= 𝑝 , iff 𝑠 |= 𝑝 for all 𝑠 ∈ Store. In particular, |= 𝑝 ⇒ 𝑞 iff 𝑝 ⊆ 𝑞.
We write 𝑠, 𝑠 ′ |= R for (𝑠, 𝑠 ′ ) ∈ R. Validity of a relation R, written |= R , means 𝑠, 𝑠 ′ |= R for all
𝑠, 𝑠 ′ . Owing to shallow embedding, |= R ⇔ S says we have R = S, i.e., the same sets of pairs.
Validity of relations is used to define the primary correctness property of interest in this paper, the
 ∃                   ∀
≈> judgment. The ≈> judgment plays a supporting role.

                                                                     ∀                                       ∀
   Definition 3.1. A ∀∀ correctness judgment 𝑐 | 𝑐 ′ : R ≈> S is valid, written |= 𝑐 | 𝑐 ′ : R ≈> S , iff
for all 𝑠, 𝑠 ′, 𝜙, 𝜙 ′ , if 𝑠, 𝑠 ′ |= R and 𝑐/𝑠 ⇓ 𝜙 and 𝑐 ′ /𝑠 ′ ⇓ 𝜙 ′ then 𝜙 ≠ , 𝜙 ′ ≠ , and 𝜙, 𝜙 ′ |= S.
                                                   ∃                                        ∃
    A ∀∃ correctness judgment 𝑐 | 𝑐 ′ : R ≈> S is valid, written |= 𝑐 | 𝑐 ′ : R ≈> S , iff for all 𝑠, 𝑠 ′ , if
𝑠, 𝑠 ′ |= R then (i) 𝑐/𝑠 ̸⇓ , and (ii) for all 𝑡, if 𝑐/𝑠 ⇓ 𝑡 then there is 𝑡 ′ such that 𝑐 ′ /𝑠 ′ ⇓ 𝑡 ′ and 𝑡, 𝑡 ′ |= S
                                                                         ∀
   The particular treatment of failure in the definition of ≈> is motivated by considerations about
bicoms discussed in Section 4.2. As discussed under related work (Section 7) one can consider other
treatments of failure. The absence of failure is a unary property that may as well be proved as such.
                                                                      ∃
   Figure 5 gives a set of proof rules for the judgment 𝑐 | 𝑐 ′ : R ≈> S. We refer to these rules as the
logic ERHL, as they are adapted from the logic named ERHL+ in Nagasamudram et al. [52], with
the addition of two rules for assert. The semantics in [52] does not involve failure, however; we
have proved all these rules are sound for our semantics.
   In rule eDo the right-only premise is a family of premises indexed by integers 𝑛. Put differently,
𝑛 is a universally quantified variable in the metalanguage. It serves to snapshot the value of the
variant at the start of an iteration. It is possible to formalize the rule using instead a single premise
with a fresh program variable in place of 𝑛. We choose this version (following [52]) because it
avoids technicalities about freshness that would add complications to the already intricate proofs
of Lemma 5.3 and Theorem 5.4.
   The following is used in rule eRewrite and later to connect commands with bicoms.

  Definition 3.2 (kat equivalence). Define ≃ to be the relation on commands that is the least
congruence that satisfies the following (for all 𝑐, 𝑑): skip; 𝑐 ≃ 𝑐 if tt then 𝑐 else 𝑑 ≃ 𝑐 .
                                                        𝑐; skip ≃ 𝑐 while ff do 𝑐 ≃ skip

   Here congruence is with respect to the command combinators: sequence, if, and while. We use
the term kat equivalence with reference to KAT [43], a theory of imperative control structure
that has been used to minimize the number of core rules needed for a relational logic [52]. Results
in this paper hold if ≃ is defined to satisfy additional equations (as in [52]). What matters is that ≃
implies semantic equality (Lemma 4.4). A potential source of additional equations is FailKAT [48];
it models failure, unlike KAT.
10                                                                          Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


 eSkip                                  eAsgnSkip                                     eSkipAsgn                                             eHavSkip
                       ∃                                           𝑥| ∃                                               |𝑥   ∃                                              ∃
 skip | skip : R ≈> R                   𝑥 := 𝑒 | skip : R𝑒 | ≈> R                     skip | 𝑥 := 𝑒 : R |𝑒 ≈> R                             hav 𝑥 | skip : (∀𝑥 | . R ) ≈> R

        eSkipHav                                                   eAsrtSkip                                                        eSkipAsrt
                                          ∃                                                               ∃                                                          ∃
        skip | hav 𝑥 : (∃ |𝑥 . R ) ≈> R                            assert 𝑞 | skip : R ∧ ⟨[𝑞 ⟨] ≈> R                                skip | assert 𝑞 : R ∧ [⟩𝑞 ]⟩ ≈> R

                                                              eSeq
                                                                              ∃                                   ∃
                                                               𝑐 | 𝑐 ′ : P ≈> Q           𝑑 | 𝑑 ′ : Q ≈> R
                                                                                                  ∃
                                                                          𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′ : P ≈> R

            eIf4
                                                                                                          ∃
                                                                     𝑐 | 𝑐 ′ : Q ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> R
                                                  ∃                                                       ∃                                                      ∃
            𝑐 | 𝑑 ′ : Q ∧ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> R                 𝑑 | 𝑐 ′ : Q ∧ ¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> R                      𝑑 | 𝑑 ′ : Q ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> R
                                                                                                                               ∃
                                                      if 𝑒 then 𝑐 else 𝑑 | if 𝑒 ′ then 𝑐 ′ else 𝑑 ′ : Q ≈> R

 eDo
                                    ∃                                                                         ∃
  𝑐 | skip : Q ∧ ⟨[𝑒 ⟨] ∧ P ≈> Q                      skip | 𝑐 ′ : Q ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ (𝑛 = 𝐸 ) ≈> Q ∧ (0 ≤ 𝐸 < 𝑛) for all 𝑛 ∈ Z
                                                              ′ ∃
       𝑐 | 𝑐 ′ : Q ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ≈> Q                         Q ⇒ ( ⟨[𝑒 ⟨] = [⟩𝑒 ′ ]⟩ ∨ ( P ∧ ⟨[𝑒 ⟨] ) ∨ ( P ′ ∧ [⟩𝑒 ′ ]⟩ ) )
                                                                                      ∃
                                 while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : Q ≈> Q ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩

     eRewrite                                                          eConseq
        ′          ∃                              ′       ′                                                   ∃                                             eFalse
     𝑐 | 𝑐 : Q ≈> R            𝑐 ≃𝑑           𝑐 ≃𝑑                      P⇒R             𝑐 | 𝑐 ′ : R ≈> S                        S⇒Q                                       ∃
                                ∃                                                                     ∃                                                     𝑐 | 𝑐 ′ : ff ≈> R
                           ′                                                              ′
                   𝑑 | 𝑑 : Q ≈> R                                                    𝑐 | 𝑐 : P ≈> Q
                                                                                                              ∃
                                                      Fig. 5. ERHL: Core rules for the ≈> judgment

                                                               eSkipDo
                                                                                                              ∃
                                                               skip | 𝑐 : [⟩𝑒 ]⟩ ∧ R ∧ (𝑛 = 𝐸 ) ≈> Q ∧ (0 ≤ 𝐸 < 𝑛) for all 𝑛 ∈ Z
                                                                                                                               ∃
                                                                                  skip | while 𝑒 do 𝑐 : Q ≈> Q ∧ ¬ [⟩𝑒 ]⟩

                   eSkipIf
                                              ∃                                               ∃
                   skip | 𝑐 : [⟩𝑒 ]⟩ ∧ R ≈> S                  skip | 𝑑 : ¬ [⟩𝑒 ]⟩ ∧ R ≈> S
                                                                              ∃
                                skip | if 𝑒 then 𝑐 else 𝑑 : R ≈> S
                                                                                                                  ∃
                                                                    Fig. 6. Derived rules for ≈>.


     Figure 6 gives additional rules which are derivable from those in Figure 5 using eRewrite.3
   Theorem 3.3 (soundness of proof rules). The proof rules in Figure 5 are all sound: for any
instantiation in which the premises are valid, the conclusion is valid.

                                                               ∀                                                  ∃
   Lemma 3.4. (i) If |= 𝑐 | skip : Q ≈> R then |= 𝑐 | skip : Q ≈> R. (ii) More generally, suppose 𝑐 ′ can
                                                                 ∀                        ∃
terminate normally, i.e., ∀𝑠. ∃𝑡 . 𝑐 ′ /𝑠 ⇓ 𝑡. Then 𝑐 | 𝑐 ′ : R ≈> S implies 𝑐 | 𝑐 ′ : R ≈> S.
                                                                                                                           ∃
3 To derive eSkipDo, apply eDo to prove while ff do skip      | while 𝑒 do 𝑐 : Q ≈> Q ∧ ¬ ⟨[ ff ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ , then use eRewrite
with while ff do skip ≃ skip from Definition 3.2, and eConseq to eliminate ¬ ⟨[ ff ⟨] (which is just tt). By instantiating eDo
with alignment conditions P, P ′ := ff, tt, the left-only and joint premises are easily proved using eFalse and eConseq. The
derivation of eSkipIf is similar, using the equation if tt then skip else skip ≃ skip with rIf, noting that two of the premises
can then be proved using eFalse and eConseq.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                        11


  Item (i) could as well be presented as a proof rule but unlike the rules in Figure 5 it involves a ∀∀
judgment so we keep it separate.

4   Bicoms
Our bicoms are inspired by similar forms of alignment product used in prior work. But the semantics
is carefully designed in order to satisfy two key criteria. First, the syntax and semantics should
facilitate straightforward translation into unary code such as an intermediate verification language.
Second, there should be full support for data dependent alignment of loop iterations. Third, there
should be a bigstep semantics that facilitates establishing a connection with command semantics
—to facilitate establishing a foundational connection with actual program behavior.
   Section 4.1 defines bicoms and some syntactic notions: projections and size. Section 4.2 defines
bicom semantics together with ∀∀ correctness of bicoms. Section 4.3 develops weakest preconditions
and Section 4.4 develops dependency notions (framing) and applies them to weakest preconditions
of bicoms. Fortunately, the wlp operator determined by our semantics satisfies equations similar to
the familiar ones for commands [3, Lemma 3.5]; this is very useful in making connections with
compositional proof rules as we do in proving the main theorem.

4.1 Bicoms, projections, and size
The syntax of bicoms is as follows, overloading some keywords without ambiguity.
       𝐵 ::= ⟨𝑐 | 𝑐⟩ | assert R | havf 𝑥 R | 𝐵; 𝐵 | if 𝑒 |𝑒 𝐵 𝐵 𝐵 𝐵 | while 𝑒 |𝑒 algn R|R do 𝐵
We let 𝐵, 𝐶, 𝐷 range over bicoms but reserve 𝐸 for two-state expressions (Section 3.2). In the bi-
while construct, we call P (resp. P ′ ) the left (resp. right) alignment condition. As introduced in
Section 2, the havoc-filter havf 𝑥 R has the effect of havoc on 𝑥 on the right side, followed by
assuming R.
  The grammar shows a compact notation for bi-if, but it has an alternate notation that is mnemonic
and close to the syntax in our prototype:
             if 𝑒 |𝑒 ′ thth 𝐵 1 thel 𝐵 2 elth 𝐵 3 elel 𝐵 4 fi          is the same as          if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4
The form allows different alignments to be used for different combinations of the branch conditions.
The benefit of this is evident in example 𝑐2 in Section 2.
  A common idiom is alignment of two if-commands that are expected to follow the same branch.
For if 𝑒 then 𝑐 else 𝑑 and if 𝑒 ′ then 𝑐 ′ else 𝑑 ′ this can be written
             assert ( ⟨[𝑒 ⟨] = [⟩𝑒 ′ ]⟩ ); if 𝑒 |𝑒 ′ thth ⟨𝑐 | 𝑐 ′ ⟩ thel ⟨𝑐 | 𝑑 ′ ⟩ elth ⟨𝑑 | 𝑐 ′ ⟩ elel ⟨𝑑 | 𝑑 ′ ⟩ fi    (2)
This form allows to then replace, say ⟨𝑐 | 𝑐 ′ ⟩, with a conveniently aligned version. The two terms
⟨𝑐 | 𝑑 ′ ⟩ and ⟨𝑑 | 𝑐 ′ ⟩ can be handled trivially, as they are unreachable given the initial agreement
⟨[𝑒 ⟨] = [⟩𝑒 ′ ]⟩ .
    Bicoms are meant to represent pairs of commands, for which reason we define left and right
projections from bicoms to commands in Figure 7. One use of projections is to ensure that bi-if is
used coherently to reason about a pair of unary if-commands, even though the bi-if form allows
different bicoms for different combinations of branch conditions.
   Definition 4.1 (well-formed bicom). A bicom is well-formed just if for each sub-bicom of the form
if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4 we have that
                                ↼− ↼   − ↼− ↼  −     −
                                                     ⇀ −  ⇀      −
                                                                 ⇀ −    ⇀
                                𝐵1 ≃ 𝐵2  𝐵3 ≃ 𝐵4     𝐵1 ≃ 𝐵3     𝐵2 ≃ 𝐵4                          (3)
   The reader should check that these conditions hold for the pattern in (2). In fact they hold in (2)
as syntactic equalities. But in general we allow that, say 𝐵 1 has a relational assertion that is not
12                                                       Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann

                                  ↼−−−−′−
                                  ⟨𝑐 | 𝑐 ⟩                          = 𝑐
                                  ↼−−−−−−−−−
                                  assert (P)                        = skip
                                  ↼−−−−−−−
                                  havf 𝑥 R                          = skip
                                  ↼−−−−                                  ↼− ↼−
                                  𝐵1 ; 𝐵2                           = 𝐵1 ; 𝐵2
                                  ↼−−−−′−−−−−−−−−−−−                               ↼−      −
                                                                                           ↼
                                  if 𝑒 |𝑒 𝐵 1 𝐵 2 𝐵 3 𝐵 4           = if 𝑒 then 𝐵 1 else 𝐵 3
                                  ↼−−−−−−−−′−−−−−−−−−−−      ′ −−−−
                                                                  −                  ↼−
                                  while 𝑒 |𝑒 algn P |P do 𝐵 = while 𝑒 do 𝐵
                                                      −
                                                      ⇀
                              Right projection 𝐵 is mirror image, except in these cases:
                                        −−−−−−−⇀
                                        havf 𝑥 R                  = hav 𝑥
                                        −−−−−− ′ −−−−−−−−−− ⇀                 −
                                                                              ⇀        −
                                                                                       ⇀
                                        if 𝑒 |𝑒 𝐵 1 𝐵 2 𝐵 3 𝐵 4 = if 𝑒 ′ then 𝐵 1 else 𝐵 2
                                           ↼ −                −
                                                              ⇀
                           Fig. 7. Left ( 𝐵 ) and right ( 𝐵 ) syntactic projections of bicoms 𝐵.

      −−−−⇀ ⇀                                       −−−−⇀⇀                            −⇀ ⇀
                                                                                      ⇀    −⇀
      ⟨𝑐 | 𝑐 ′ ⟩     =   ⟨skip | 𝑐 ′ ⟩              𝐵1 ; 𝐵2                       =   𝐵1 ; 𝐵2
      −−−−−−⇀   ⇀                                   −−−−−−    −−−−−−−−−⇀  ⇀                     −⇀ ⇀
                                                                                                ⇀   −⇀ ⇀−⇀ ⇀−⇀
      assert P       =   assert P                   if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4     =   if tt|𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4
      −−−−−−−⇀   ⇀                                  −−−−−−−−−′−−−−−−−−−−−′−−−⇀⇀                                    ⇀−⇀
      havf 𝑥 R       =   havf 𝑥 R                   while 𝑒 |𝑒 algn P |P do 𝐵     =   while ff |𝑒 ′ algn ff |P ′ do 𝐵
                                                                            ⇀−
                                                                             ⇀
                                                 Fig. 8. Bi-right projection 𝐵

                     ↼−                                  ↼−
included in 𝐵 2 , so 𝐵 1 will include an extra skip that 𝐵 2 lacks. For example, for 𝐵 3 and 𝐵 4 in Figure 3,
         ↼−        ↼−
here are 𝐵 3 and 𝐵 4 which are different but related by ≃.
      𝑥 := low; hav 𝑏;                                 𝑥 := low; hav 𝑏; skip;
      while 𝑏 ≠ 0 do 𝑥 := 𝑥 + 1; hav 𝑏 done            while 𝑏 ≠ 0 do 𝑥 := 𝑥 + 1; hav 𝑏; skip done
      skip; skip
                            −
                            ↼     ↼−
Note the extra skip’s in 𝐵 3 and 𝐵 4 corresponding to the different positions of havf in 𝐵 3, 𝐵 4 .
                                    ↼−
                                    ↼       ↼↼−      ↼−
   Define the bi-left projection 𝐵 by 𝐵 =         ˆ ⟨ 𝐵 | skip⟩. We also define the bi-right projection,
 −⇀
 ⇀
  𝐵 , in Figure 8. Its purpose is to retain relational assumptions (“filters”) associated with havoc on
the right. Both bi-projections preserve well-formedness. They also satisfy the following. (Proof of
the latter two cases requires induction, and the last case is only up to ≃.)
                      ↼−
                       ↼
                       ↼−−−− ↼−       −−↼
                                        −−−
                                        ↼ ⇀              −−−⇀ ⇀
                                                          −⇀
                                                          ⇀      −      ↼ −−−
                                                                         −⇀
                                                                         ⇀
                      ( 𝐵 )=𝐵         ( 𝐵 ) = skip       (𝐵)= 𝐵         ( 𝐵 ) ≃ skip                 (4)
   The semantics of bi-while (later, in Figure 9) involves projections of the loop body, and those
projections are not sub-terms of the bicom. Thus some results that one might expect to prove by
structural induction on syntax, must instead go by strong induction on a size measure. We define
size(skip) = 0, size 1 for each other primitive command and bicom, and otherwise the size is one
more than the sum of sizes of the constituent parts. The treatment of skip is what ensures the
following important fact.
                                           ↼−
                                           ↼                       −⇀
                                                                   ⇀
   Lemma 4.2 (size of projection). size( 𝐵 ) ≤ size(𝐵) and size( 𝐵 ) ≤ size(𝐵).
     In addition to ≃, we introduce a similar equivalence relation, , for bicoms.
     Definition 4.3. Define  to be the least equivalence relation on bicoms such that
         ⟨skip | 𝑐 ′ ; 𝑑 ′ ⟩  ⟨skip | 𝑐 ′ ⟩; ⟨skip | 𝑑 ′ ⟩              ⟨𝑐; 𝑑 | skip⟩  ⟨𝑐 | skip⟩; ⟨𝑑 | skip⟩
         ⟨𝑐 | 𝑐 ′ ⟩  ⟨𝑐 | skip⟩; ⟨skip | 𝑐 ′ ⟩                   𝑐 ≃ 𝑑 and 𝑐 ′ ≃ 𝑑 ′ imply ⟨𝑐 | 𝑐 ′ ⟩  ⟨𝑑 | 𝑑 ′ ⟩
   In other words,  is the reflexive, symmetric, transitive closure of the displayed relations. The
relation  implies equivalence in the semantics defined later (Section 4.2 and Lemma 4.4).
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                                                              13


        𝑐/𝑠 ⇓                        𝑐/𝑠 ⇓ 𝑡        𝑐 ′ /𝑠 ′ ⇓                     𝑐/𝑠 ⇓ 𝑡         𝑐 ′ /𝑠 ′ ⇓ 𝑡 ′                       𝑠, 𝑠 ′ |= Q
        ′       ′                            ′          ′                               ′           ′           ′
   ⟨𝑐 | 𝑐 ⟩/(𝑠, 𝑠 ) ⇓                 ⟨𝑐 | 𝑐 ⟩/(𝑠, 𝑠 ) ⇓                       ⟨𝑐 | 𝑐 ⟩, (𝑠, 𝑠 ) ⇓ (𝑡, 𝑡 )                   assert Q/(𝑠, 𝑠 ′ ) ⇓ (𝑠, 𝑠 ′ )

                    𝑠, 𝑠 ′ ̸ |= Q                             𝑡 ′ = 𝑠 ′ [𝑥 ↦→ 𝑛]             𝑠, 𝑡 ′ |= Q                     𝐵 1 /(𝑠, 𝑠 ′ ) ⇓
            assert Q/(𝑠, 𝑠 ′ ) ⇓                               havf 𝑥 Q/(𝑠, 𝑠 ′ ) ⇓ (𝑠, 𝑡 ′ )                              𝐵 1 ; 𝐵 2 /(𝑠, 𝑠 ′ ) ⇓

                𝑠 |= 𝑒       𝑠 ′ |= 𝑒 ′      𝐵 1 /(𝑠, 𝑠 ′ ) ⇓ 𝜑                             𝐵 1 /(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ )     𝐵 2 /(𝑡, 𝑡 ′ ) ⇓ 𝜑
                    if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4 /(𝑠, 𝑠 ′ ) ⇓ 𝜑                                             𝐵 1 ; 𝐵 2 /(𝑠, 𝑠 ′ ) ⇓ 𝜑

                                                                                                                                                ↼−
                                                                                                                                                ↼
and three similar if rules                                       𝑠 ̸ |= 𝑒    𝑠 ′ ̸ |= 𝑒 ′                     𝑠 |= 𝑒       𝑠, 𝑠 ′ |= L          𝐵 /(𝑠, 𝑠 ′ ) ⇓
for one, other, or neither test true                           𝑊 /(𝑠, 𝑠 ′ ) ⇓ (𝑠, 𝑠 ′ )                                        𝑊 /(𝑠, 𝑠 ′ ) ⇓

                                                                     ↼−
                                                                     ↼
                                    𝑠 |= 𝑒       𝑠, 𝑠 ′ |= L         𝐵 /(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ )            𝑊 /(𝑡, 𝑡 ′ ) ⇓ 𝜑
                                                                                   ′
                                                                      𝑊 /(𝑠, 𝑠 ) ⇓ 𝜑

                                                                                                           −⇀
                                                                                                           ⇀
                                (𝑠 ̸ |= 𝑒 or 𝑠, 𝑠 ′ ̸ |= L)           𝑠 ′ |= 𝑒 ′       𝑠, 𝑠 ′ |= R          𝐵 /(𝑠, 𝑠 ′ ) ⇓
                                                                     𝑊 /(𝑠, 𝑠 ′ ) ⇓

                                                                                            −⇀
                                                                                            ⇀
                 (𝑠 ̸ |= 𝑒 or 𝑠, 𝑠 ′ ̸ |= L)        𝑠 ′ |= 𝑒 ′        𝑠, 𝑠 ′ |= R            𝐵 /(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ )      𝑊 /(𝑡, 𝑡 ′ ) ⇓ 𝜑
                                                                      𝑊 /(𝑠, 𝑠 ′ ) ⇓ 𝜑

                                    𝑠 |= 𝑒       𝑠 ′ |= 𝑒 ′       𝑠, 𝑠 ′ ̸ |= L        𝑠, 𝑠 ′ ̸ |= R       𝐵/(𝑠, 𝑠 ′ ) ⇓
                                                                                   ′
                                                                     𝑊 /(𝑠, 𝑠 ) ⇓

                    𝑠 |= 𝑒      𝑠 ′ |= 𝑒 ′       𝑠, 𝑠 ′ ̸ |= L       𝑠, 𝑠 ′ ̸ |= R          𝐵/(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ )      𝑊 /(𝑡, 𝑡 ′ ) ⇓ 𝜑
                                                                                   ′
                                                                      𝑊 /(𝑠, 𝑠 ) ⇓ 𝜑

                (𝑠 |= 𝑒 and 𝑠 ′ ̸ |= 𝑒 ′ and 𝑠, 𝑠 ′ ̸ |= L) or (𝑠 ̸ |= 𝑒 and 𝑠 ′ |= 𝑒 ′ and 𝑠, 𝑠 ′ ̸ |= R)
                                                            𝑊 /(𝑠, 𝑠 ′ ) ⇓

                        Fig. 9. Bicom semantics. Here 𝑊 abbreviates while 𝑒 |𝑒 ′ algn L|R do 𝐵.


  Connections with stronger relations used in other works [2, 24] are discussed in Section 7. Here
we are not concerned with the rewriting of bicoms in general, but only eliminating skips introduced
by the projections, for which the equations in Definition 4.3 suffice (Lemma 5.1).

4.2    Semantics of bicoms and their connection with commands
Bicoms are given an evaluation semantics as in Figure 9. Here 𝜑 ranges over outcomes of two forms:
either a store pair (𝑠, 𝑠 ′ ) or . The handling of failure in bicom semantics (and also in Definition 3.1
     ∀
for ≈>) is motivated by two considerations. First, it must support the main theorem. That is, the
∀∀ property of a bicom to which the filter-adequacy transformation has been applied must imply
the ∀∃ property of its underlying commands. Second, it should be implementable by translation to
commands (including assertions), using straightforward encoding to leverage tool automation and
to facilitate user interaction.
   The second consideration rules out, for example, a dovetail semantics for the embed construct
as used in [6]. Our semantics of ⟨𝑐 | 𝑐 ′ ⟩ can be implemented by translating to 𝑐; 𝑐 ′′ where 𝑐 ′′ is
14                                              Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


𝑐 ′ with its variables renamed apart from those of 𝑐. This means, for example, that ⟨𝑑𝑖𝑣𝑒𝑟𝑔𝑒 | fail⟩
does not fail. Our semantics of while 𝑒 |𝑒 ′ algn L|R do 𝐵 determinizes the choice between left-only
and right-only iterations when L and R (and 𝑒 and 𝑒 ′ ) hold. This loses no generality and accords
with a translation that uses if-commands for the loop body, which works provided L and R can
be written as expressions—which is the case in all examples we have seen. (After all, the point of
alignment is to facilitate use of simple assertions.) The last rule of the bi-while semantics bakes in
an adequacy condition: if either 𝑒 or 𝑒 ′ is true but none of the other transition rules apply then
the bicom fails. (Compare the side condition in rule eDo in Figure 5.) Note that it is possible for
one-sided iteration to mask failure on the other side, similar to the case of ⟨𝑑𝑖𝑣𝑒𝑟𝑔𝑒 | fail⟩. An
example is while tt|𝑒 ′ algn tt|R do ⟨skip | fail⟩.
    For any 𝐵, 𝑠, 𝑠 ′ , the possible results from 𝐵/(𝑠, 𝑠 ′ ) are failure, normal termination, or no outcome.
The latter can happen only due to a divergent loop or blockage by havf 𝑥 Q (in case there is no value
for 𝑥 that makes Q true). The bi-while semantics uses ⇀             −⇀
                                                                     _ to ensure such blockage for right-only
                                           −⇀
                                           ⇀                                                     ↼↼−
iterations. It can be proved that 𝐵 /(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ ) implies 𝑠 = 𝑡, and mut. mut. for 𝐵 . A basic
property of bicom semantics is that it models the effects of commands in this sense:
                                                               −
                                                               ↼            −
                                                                            ⇀
                               𝐵/(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ ) implies 𝐵 /𝑠 ⇓ 𝑡 and 𝐵 /𝑠 ′ ⇓ 𝑡 ′ .                 (5)
The converse of (5) need not hold. The converse may fail if 𝐵 includes havf (the assumption of
which may not hold) or nontrivial loop alignment conditions or relational assertions (which can
lead to failures) —because these are discarded by ↼_− and ⇀
                                                          −_ .
   Let J 𝑐 K be the relation from stores to outcomes defined by J 𝑐 K = {(𝑠, 𝜙) | 𝑐/𝑠 ⇓ 𝜙 }. Let J 𝐵 K
be the relation from store pairs to outcomes defined by J 𝐵 K = {((𝑠, 𝑠 ′ ), 𝜑) | 𝐵/(𝑠, 𝑠 ′ ) ⇓ 𝜑 }. Now for
semantic equivalence of bicoms 𝐵 and 𝐶 we can simply write J 𝐵 K = J 𝐶 K.
     Lemma 4.4. 𝑐 ≃ 𝑑 implies J 𝑐 K = J 𝑑 K, and 𝐵  𝐶 implies J 𝐵 K = J 𝐶 K.
  Bicoms are specified by pre- and post-relations but they have a single execution. We choose the
           ¥ Q in the following.
notation P {
   Definition 4.5 (Bicom correctness). The correctness judgment 𝐵 : P {                ¥ Q is valid, written
 |= 𝐵 : P {   ¥ Q , iff for all 𝑠, 𝑠 ′ such that 𝑠, 𝑠 ′ |= P we have 𝐵/(𝑠, 𝑠 ′ ) ̸⇓ and moreover 𝑡, 𝑡 ′ |= Q for
all 𝑡, 𝑡 ′ with 𝐵/(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ ).
     Because correctness is defined in terms of semantics, the following is easily proved.
                                                     ¥ Q iff |= 𝐶 : P {
     Lemma 4.6. Suppose J 𝐵 K = J 𝐶 K. Then |= 𝐵 : P {                ¥ Q.
   Because a bicom can include assumptions (in the havf construct), in general it is not the case
                             − ⇀
                             ↼   −       ∀
              ¥ Q implies |= 𝐵 | 𝐵 : P ≈> Q. But it holds for 𝐵 without havf, owing in part to
that |= 𝐵 : P {
the adequacy condition checked by the last rule in Figure 9 for bi-while. In particular we use the
following.
                                                                                        ∀
     Lemma 4.7 (adeqacy of embed). |= ⟨𝑐 | 𝑐 ′ ⟩ : P {
                                                     ¥ Q implies |= 𝑐 | 𝑐 ′ : P ≈> Q.
   Summing up. The technical development aims to justify the following method for verifying
                         ∃                             −
                                                       ↼                ⇀−
a judgment 𝑐 | 𝑐 ′ : P ≈> Q. First, find 𝐵 such that J 𝐵 K = J 𝑐 K and J 𝐵 K = J 𝑐 ′ K, for which a
                 ↼−          −
                             ⇀
simple check is 𝐵 ≃ 𝑐 and 𝐵 ≃ 𝑐 ′ . Second, by some means verify |= chk(𝐵) : P {        ¥ Q where
chk applies the filter-adequacy transformation. The main theorem says that this method is sound.
Sections 4.3–4.4 develop results on weakest preconditions and framing that are used to prove
Theorem 5.4 after chk has been defined in Section 5.1.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                15


4.3    Weakest preconditions for bicoms
For expository purposes we begin with commands. We use the phrase “weakest precondition” but
we are concerned with partial correctness and so use the standard name wlp that refers to weakest
liberal precondition [26]. Define wlp to map commands and assertions to assertions as follows.
                                 ˆ {𝑠 | 𝑐/𝑠 ̸⇓
                       wlp(𝑐, 𝑝) =                     and 𝑡 |= 𝑝 for all 𝑡 such that 𝑐/𝑠 ⇓ 𝑡 }                    (6)
This satisfies well known equations4 including
   wlp(hav 𝑥, 𝑝) = ∀𝑥 . 𝑝           wlp(assert 𝑞, 𝑝) = 𝑞 ∧ 𝑝             wlp(while 𝑒 do 𝑐, 𝑝) = gfp(𝐹 (𝑒, 𝑐, 𝑝))
where 𝐹 (𝑒, 𝑐, 𝑝) (𝑋 ) =
                       ˆ (𝑒 ⇒ wlp(𝑐, 𝑋 )) ∧ (¬𝑒 ⇒ 𝑝). Note that 𝐹 (𝑒, 𝑐, 𝑝) (𝑋 ) is monotonic in 𝑋
with respect to the ordering on assertions defined by 𝑝 ≤ 𝑞 iff |= 𝑝 ⇒ 𝑞, which is equivalent to
(Store \ 𝑝) ∪ 𝑞 = Store and to 𝑝 ⊆ 𝑞. In short, this is the powerset lattice on Store, and gfp gives
greatest fixpoints of monotonic functions on this lattice.
  We overload the name wlp, using it for a map from bicoms and relations to relations:
                       ˆ {(𝑠, 𝑠 ′ ) | 𝐵/(𝑠, 𝑠 ′ ) ̸⇓
             wlp(𝐵, P) =                                   ∧ ∀𝑡, 𝑡 ′ . 𝐵/(𝑠, 𝑠 ′ ) ⇓ (𝑡, 𝑡 ′ ) ⇒ (𝑡, 𝑡 ′ ) |= P}   (7)
This has some basic properties that are standard for wlp of commands and partial correctness.
   Lemma 4.8.                                           ¥ Q
                      (i) |= P ⇒ wlp(𝐵, Q) iff |= 𝐵 : P {
    (ii) |= 𝐵 : wlp(𝐵, Q) {  ¥ Q
   (iii) If J 𝐵 K = J 𝐶 K then wlp(𝐵, Q) = wlp(𝐶, Q)
  In item (i), the ⇐ direction relies on wlp being the weakest (and thus gfp being the greatest).
Much of what we do would work using an approximate wlp like those used in tools based on
verification conditions (which may only approximate wlp). But here we only use wlp for proving
semantic results.
  It is convenient to define the following abbreviations:
                 wlpL(𝑐, Q) =
                            ˆ wlp(⟨𝑐 | skip⟩, Q)                 wlpR(𝑐, Q) =
                                                                            ˆ wlp(⟨skip | 𝑐⟩, Q)
In proofs we use that wlpR satisfies equations very similar to those for commands, but using the
right-side substitution and quantification operators.
   Lemma 4.9 (wlpR eqations).
          wlpR(skip, Q)                       = Q
          wlpR(𝑥 := 𝑒, Q)                     = Q |𝑒|𝑥
          wlpR(hav 𝑥, Q)                      = ∀|𝑥 . Q
          wlpR(assert 𝑝, Q)                   = [⟩𝑝 ]⟩ ∧ Q
          wlpR(𝑐 1 ; 𝑐 2, Q)                  = wlpR(𝑐 1, wlpR(𝑐 2, 𝑝))
          wlpR(if 𝑒 then 𝑐 1 else 𝑐 2, Q) = ( [⟩𝑒 ]⟩ ⇒ wlpR(𝑐 1, Q)) ∧ (¬ [⟩𝑒 ]⟩ ⇒ wlpR(𝑐 2, Q))
          wlpR(while 𝑒 do 𝑐, Q)               = gfp(𝐹 (𝑒, 𝑐, Q))
            where 𝐹 (𝑒, 𝑐, Q) (X) = ˆ ( [⟩𝑒 ]⟩ ⇒ wlpR(𝑐, X)) ∧ (¬ [⟩𝑒 ]⟩ ⇒ Q)
   Store relations form a complete lattice with respect to subset ordering. Note that Q ⊆ R iff
|= Q ⇒ R, and 𝐹 (𝑒, 𝑐, Q) (X) is monotonic in X with respect to ⊆.
   In the following equations that characterize wlp on bicoms, the loop case is given by greatest
fixpoint of a function, 𝐺. Like 𝐹 in Lemma 4.9 it maps relations to relations, but it is more complicated
for two reasons: there are three kinds of bi-while loop iteration, and bi-while can fail due to its
adequacy condition (i.e., the last rule in Figure 9).
4 These are derived from bigstep semantics as in [3], rather than being used to define wlp as in some work [27].
16                                                          Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


     Lemma 4.10 (bicom wlp eqations).
     wlp(⟨𝑐 | 𝑐 ′ ⟩, Q)                        =        wlpL(𝑐, wlpR(𝑐 ′, Q))
     wlp(assert P, Q)                          =        P∧Q
     wlp(havf 𝑥 P, Q)                          =        ∀ |𝑥 . (P ⇒ Q)
     wlp(𝐵 1 ; 𝐵 2, Q)                         =        wlp(𝐵 1, wlp(𝐵 2, 𝑝))
     wlp(if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4, Q)         =        ( ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(𝐵 1, Q)) ∧ ( ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(𝐵 2, Q)) ∧
                                                        (¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(𝐵 3, Q)) ∧ (¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(𝐵 4, Q))
     wlp(while 𝑒 |𝑒 ′ algn L|R do 𝐵, Q)        =        gfp(𝐺 (𝑒, 𝑒 ′, L, R, 𝐵, Q)) where 𝐺 is defined below

  The definition of 𝐺 (𝑒, 𝑒 ′, L, R, 𝐵, Q) involves five conjuncts to which we make later reference,
so we label them (G1)–(G5).
                𝐺 (𝑒, 𝑒 ′, L, R, 𝐵, Q) (X) =
                                           ˆ (¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ Q)∧                      (G1)
                                                                        ↼↼−
                                             ( ⟨[𝑒 ⟨] ∧ L ⇒ wlp( 𝐵 , X))∧                      (G2)
                                                                                           −⇀
                                                                                           ⇀
                                             ( [⟩𝑒 ′ ]⟩ ∧ R ∧ ¬( ⟨[𝑒 ⟨] ∧ L) ⇒ wlp( 𝐵 , X))∧ (G3)
                                             ( ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ L ∧ R ⇒ wlp(𝐵, X))∧         (G4)
                                             ((𝑒 =  ¥ 𝑒 ′ ) ∨ ( ⟨[𝑒 ⟨] ∧ L) ∨ ( [⟩𝑒 ′ ]⟩ ∧ R)) (G5)
The reader can check that 𝐺 (𝑒, 𝑒 ′, L, R, 𝐵, Q) (X) is monotonic in X.
  The first equation in the Lemma says that wlp(⟨𝑐 | 𝑐 ′ ⟩, Q) is wlp(⟨𝑐 | skip⟩, wlp(⟨skip | 𝑐 ′ ⟩, Q)).
The order reflects the asymmetry in the failure semantics of ⟨𝑐 | 𝑐 ′ ⟩, Q) (Figure 9).5

4.4      Semantic framing
For the filter-adequacy transformation to serve its purpose we need the chk function to use fresh
variables. In an implementation this is easily accomplished using syntactic checks and gensym (as
discussed in Section 6). But a stateful gensym cannot easily be used in proofs; rather, we need to
define the transformation as a pure function in the ambient logic. Moreover shallow embedding
precludes naive syntactic analysis to find the variables used in a given command or bicom. So,
for the technical development we assume given a set of variables that overapproximates those
on which the command or bicom acts and on which its constituents depend. In this section we
formalize checks that such approximation holds, called semantic framing conditions. Then, for
commands and bicoms, Section 4.5 gives a conservative syntactic formulation that is convenient in
proofs by induction on program structure.
   We choose to represent the sets by lists (without any requirement of ordering or uniqueness)
                                                                                                    𝑣𝑠
and write 𝑥 ∈ 𝑣𝑠 to say 𝑥 is in the list 𝑣𝑠 of variables. For list 𝑣𝑠 of variables, define relation = on
                  𝑣𝑠
                ˆ ∀𝑥 ∈ 𝑣𝑠. 𝑠 (𝑥) = 𝑡 (𝑥) (pronounced “𝑠 agrees with 𝑡 on 𝑣𝑠”).
stores by 𝑠 = 𝑡 =
  Definition 4.11 (semantic frames). For expressions, assertions, two-state expressions, and relations
we define a proposition 𝑣𝑠 ⊩ _ , that says the entity depends only on the variables in list 𝑣𝑠.6
                                                   𝑣𝑠
                        𝑣𝑠 ⊩ 𝑒       =
                                     ˆ   ∀𝑠, 𝑡 . 𝑠 = 𝑡 ⇒ 𝑒 (𝑠) = 𝑒 (𝑡)
                                                    𝑣𝑠
                        𝑣𝑠 ⊩ 𝑝       =
                                     ˆ   ∀𝑠, 𝑡 . 𝑠 = 𝑡 ⇒ (𝑠 |= 𝑝 ⇔ 𝑡 |= 𝑝)
                                                             𝑣𝑠        𝑣𝑠
                        𝑣𝑠 ⊩ 𝐸       =
                                     ˆ   ∀𝑠, 𝑡, 𝑠 ′, 𝑡 ′ . 𝑠 = 𝑠 ′ ∧ 𝑡 = 𝑡 ′ ⇒ 𝐸 (𝑠, 𝑠 ′ ) = 𝐸 (𝑡, 𝑡 ′ )
                                                             𝑣𝑠        𝑣𝑠
                        𝑣𝑠 ⊩ R       =
                                     ˆ   ∀𝑠, 𝑡, 𝑠 ′, 𝑡 ′ . 𝑠 = 𝑠 ′ ∧ 𝑡 = 𝑡 ′ ⇒ (𝑠, 𝑠 ′ |= R ⇔ 𝑡, 𝑡 ′ |= R)
5 Readers accustomed to using such equations to define wlp may see apparent circularity in this equation, but this is not a

definition.
6 Please note here we use logic symbols for propositions in the ambient logic, by contrast with, e.g., Lemma 4.10 where they

denote operations on store relations.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                          17


  For expression 𝑒, the property 𝑣𝑠 ⊩ 𝑒 (pronounced “𝑣𝑠 frames 𝑒”) says that the value of 𝑒 in a
given store depends only on the values of the variables in 𝑣𝑠. Similary for assertions etc.
   Lemma 4.12. 𝑣𝑠 ⊩ R and 𝑥 ∉ 𝑣𝑠 implies R |𝑒|𝑥 = R.
  For an expression, the property 𝑣𝑠 ⊩ 𝑒 is about the value of 𝑒. For commands, semantic framing
says that the effect only depends on the initial values of variables in 𝑣𝑠.
                                                  𝑣𝑠                                        𝑣𝑠
                             ˆ (∀𝑠, 𝑠 ′, 𝑡 . 𝑠 = 𝑠 ′ ∧ 𝑐/𝑠 ⇓ 𝑡 ⇒ ∃𝑡 ′ . 𝑐/𝑠 ′ ⇓ 𝑡 ′ ∧ 𝑡 = 𝑡 ′ )
                      𝑣𝑠 ⊩ 𝑐 =
                                               𝑣𝑠
                               ∧(∀𝑠, 𝑠 ′ . 𝑠 = 𝑠 ′ ∧ 𝑐/𝑠 ⇓ ⇒ 𝑐/𝑠 ′ ⇓ )
Note that this considers the effect on 𝑣𝑠. This allows that if the command terminates normally it
may have an effect on other variables, and that effect may depend on other variables.7 Although
                                                                     𝑣𝑠
the phrasing of these conditions seems asymmetric, the relation = is symmetric. So an informal
reading of 𝑣𝑠 ⊩ 𝑐 is that from initial states 𝑠, 𝑠 ′ that agree modulo 𝑣𝑠, 𝑐 has the same behaviors
        𝑣𝑠
(modulo =). For bicoms the definition is similar.
                                                       𝑣𝑠         𝑣𝑠
                    ˆ (∀𝑠, 𝑠 ′, 𝑡, 𝑡 ′, 𝑢, 𝑢 ′ . 𝑠 = 𝑡 ∧ 𝑠 ′ = 𝑡 ′ ∧ 𝐵/(𝑠, 𝑠 ′ ) ⇓ (𝑢, 𝑢 ′ )
             𝑣𝑠 ⊩ 𝐵 =
                                                                                         𝑣𝑠        𝑣𝑠
                                                 ⇒ ∃𝑣, 𝑣 ′ . 𝐵/(𝑡, 𝑡 ′ ) ⇓ (𝑣, 𝑣 ′ ) ∧ 𝑢 = 𝑣 ∧ 𝑢 ′ = 𝑣 ′ )
                                             𝑣𝑠        𝑣𝑠
                      ∧(∀𝑠, 𝑠 ′, 𝑡, 𝑡 ′ . 𝑠 = 𝑡 ∧ 𝑠 ′ = 𝑡 ′ ∧ 𝐵/(𝑠, 𝑠 ′ ) ⇓ ⇒ 𝐵/(𝑡, 𝑡 ′ ) ⇓ )
    Lemma 4.13 (framing wlp). (i) If 𝑣𝑠 ⊩ 𝑐 and 𝑣𝑠 ⊩ Q then 𝑣𝑠 ⊩ wlpR(𝑐, Q).
(ii) If 𝑣𝑠 ⊩ 𝐵 and 𝑣𝑠 ⊩ Q then 𝑣𝑠 ⊩ wlp(𝐵, Q).

4.5    Variants and syntactic frames
Here and in the following sections we work with annotated command and bicom syntax. Bicoms
already feature alignment conditions, which are a kind of annotation that accords with the proof
rule eDo in Figure 5. Now we add variant annotations (as in Section 2). Unlike alignment conditions,
variants have no effect on semantics; they just serve in defining the filter-adequacy transformation
(Section 5.1). The syntax of while and bi-while is henceforth
                          while 𝑒 vnt 𝑒 1 do 𝑐              while 𝑒 |𝑒 ′ algn P |P ′ vnt 𝐸 do 𝐵
where 𝑒 1 is an integer expression and 𝐸 is a two-state expression. All preceding definitions and
results are applicable to the revised syntax: the semantics ignores variants. For technical reasons,
the right bi-projection ⇀−⇀
                          _ (Figure 8) keeps the variant. We consider that ≃ and  leave variants
unchanged.8
   Figure 10 defines functions cFrame and bFrame that we loosely describe as syntactic framing
checks because they recurse over syntax. By contrast with the semantic property 𝑣𝑠 ⊩𝑐, the condition
cFrame(𝑐, 𝑣𝑠) considers variant expressions in the code, even though variants do not influence the
semantics. The same for bFrame. The functions also check that all assigned/havoc’d variables are
in 𝑣𝑠. Observe that cFrame(𝑐, 𝑣𝑠) implies 𝑣𝑠 ⊩ _ for every expression and assertion in 𝑐.
   The most difficult and subtle results involving these functions is Lemma 5.2 in the sequel. But
the following is also important.
   Lemma 4.14. cFrame(𝑐, 𝑣𝑠) implies 𝑣𝑠 ⊩ 𝑐 and bFrame(𝐵, 𝑣𝑠) implies 𝑣𝑠 ⊩ 𝐵.
   The first implication is proved by induction on 𝑐. The second implication is proved by induction
on size(𝐵), because in the case 𝐵 is a loop the semantics involves projection of the loop body, and
projections are not in general subterms of the bicom. Both proofs involve reasoning about all details
in the semantics.
7 Some readers will note the connection with possibilistic noninterference.
8 That is how the Rocq mechanization defines these relations; but ignoring variants would work as well.
18                                                     Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


                          𝑐                        cFrame(𝑐, 𝑣𝑠)
                          skip                     tt
                          𝑥 := 𝑒                   𝑥 ∈ 𝑣𝑠 ∧ 𝑣𝑠 ⊩ 𝑒
                          hav 𝑥                    𝑥 ∈ 𝑣𝑠
                          assert 𝑝                 𝑣𝑠 ⊩ 𝑝
                          𝑐1; 𝑐2                   cFrame(𝑐 1, 𝑣𝑠) ∧ cFrame(𝑐 2, 𝑣𝑠)
                          if 𝑒 then 𝑐 1 else 𝑐 2   𝑣𝑠 ⊩ 𝑒 ∧ cFrame(𝑐 1, 𝑣𝑠) ∧ cFrame(𝑐 2, 𝑣𝑠)
                          while 𝑒 vnt 𝑒 1 do 𝑐 1   𝑣𝑠 ⊩ 𝑒 ∧ 𝑣𝑠 ⊩ 𝑒 1 ∧ cFrame(𝑐 1, 𝑣𝑠)

             𝐵                                           bFrame(𝐵, 𝑣𝑠)
             ⟨𝑐 | 𝑐 ′ ⟩                                  cFrame(𝑐, 𝑣𝑠) ∧ cFrame(𝑐 ′, 𝑣𝑠)
             assert P                                    𝑣𝑠 ⊩ P
             havf 𝑥 P                                    𝑥 ∈ 𝑣𝑠 ∧ 𝑣𝑠 ⊩ P
             𝐵1 ; 𝐵2                                     bFrame(𝐵 1, 𝑣𝑠) ∧ bFrame(𝐵 2, 𝑣𝑠)
             if 𝑒 | 𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4                  𝑣𝑠 ⊩ (𝑒, 𝑒 ′ ) ∧ (∧ 𝑖 : 1 ≤ 𝑖 ≤ 4 : bFrame(𝐵𝑖 , 𝑣𝑠))
             while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 1     𝑣𝑠 ⊩ (𝑒, 𝑒 ′, P, P ′, 𝐸) ∧ bFrame(𝐵 1, 𝑣𝑠)
          Fig. 10. Defining cFrame and bFrame. Here 𝑣𝑠 ⊩ (𝑒, 𝑒 ′, . . .) abbreviates 𝑣𝑠 ⊩ 𝑒 ∧ 𝑣𝑠 ⊩ 𝑒 ′ ∧ . . ..


     Lemma 4.15. If bFrame(𝐵, 𝑣𝑠) and 𝑥 ∉ 𝑣𝑠 then, for any 𝑛 ∈ Z, |= (wlp(𝐵, R)) |𝑥
                                                                                 |𝑛
                                                                                               |𝑥
                                                                                    ⇒ wlp(𝐵, R |𝑛 ).
     We conclude the section with straightforward results involving substitution.
     Lemma 4.16. If |= P ⇒ [⟩𝑥 = 𝑒 ]⟩ then |= (P ⇒ Q |𝑒|𝑥 ) ⇔ (P ⇒ Q).
     This means the two sides are the same relation, which we could write a (P ⇒ Q𝑒𝑥 ) = (P ⇒ Q).
     Lemma 4.17. |= R iff for all 𝑛 ∈ Z, |= R𝑛𝑥 .

5     The filter-adequacy transformation
Section 5.1 formalizes the transformation as a function on bicoms. Since it inserts checks we
give it the short name chk. It relies on a transformation on commands called uchk for “unary
check”. Section 5.2 gives the main result, which supports the methodology spelled out at the end of
Section 2.
   The definitions of Section 5.1 are carefully crafted to support the proofs in Section 5.2 of the
main theorem about chk and its supporting lemma about uchk. By spelling out detailed proofs in a
readable way (Section 5.2 and appendix) we expose what is needed to develop such a result for a
richer programming language and for particular relational assertion languages.

5.1     The check functions
For the transformation to serve its purpose, the instrumentation added by chk should not interfere
with the underlying executions. As shown in Section 2, the instrumentation uses fresh variables
in loop bodies to snapshot the value of the variant in order to assert that it gets decreased. An
implementation of the transformation will use some form of gensym for fresh variables, for example
using a mutable global variable (as done in our prototype). The added variables should be fresh
with respect to both the program and its specification.
   For the theoretical development, we have the self-inflicted challenge that shallow embedding
prevents us from computing, the free variables of assertions, commands, etc. We also have the
challenge to formulate freshness in a way that is convenient for reasoning; for example, imple-
menting gensym using a state monad is elegant from a programming point of view but would be
a distraction in our main proofs. Instead, we parameterize chk and the helping function uchk by
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                       19


                 𝑐                         uchk(𝑐, 𝑣𝑠)
                 skip                      skip
                 𝑥 := 𝑒                    𝑥 := 𝑒
                 hav 𝑥                     hav 𝑥
                 assert 𝑝                  assert 𝑝
                 𝑐1; 𝑐2                    uchk(𝑐 1, 𝑣𝑠); uchk(𝑐 2, 𝑣𝑠)
                 if 𝑒 then 𝑐 1 else 𝑐 2    if 𝑒 then uchk(𝑐 1, 𝑣𝑠) else uchk(𝑐 2, 𝑣𝑠)
                 while 𝑒 vnt 𝑒 1 do 𝑐 1    while 𝑒 vnt 𝑒 1 do 𝑐 2
                                              where 𝑐 2 is 𝑥 := 𝑒 1 ; uchk(𝑐 1, 𝑣𝑠); assert (0 ≤ 𝑒 1 < 𝑥)
                                                      and 𝑥 ∉ 𝑣𝑠++modVars(uchk(𝑐 1, 𝑣𝑠))

                                   Fig. 11. The uchk transformation on commands


a set of variables to avoid, which should be chosen to frame the spec and bicom of interest. For
simplicity the set is represented by a list.
   The unary check function maps a command 𝑐 and list 𝑣𝑠 of variables to a command uchk(𝑐, 𝑣𝑠)
that is equivalent except that each loop is instrumented so it asserts that the body decreases the
given variant expression. It is defined in Figure 11. In the loop case, a variable 𝑥 is chosen that
is fresh with respect to any instrumentation variables added to the body 𝑐 1 and with respect to
the given list 𝑣𝑠. This is achieved by the condition 𝑥 ∉ 𝑣𝑠++modVars(uchk(𝑐 1, 𝑣𝑠)) in the case for
while.9 This ensures that the instrumentation variables of nested loops are distinct.
   In our use of uchk, 𝑣𝑠 will frame the command as well as the specification of interest, so 𝑣𝑠 already
includes its assigned variables. Thus the catenation (++) will create duplicates. This is harmless,
because we allow duplicate elements in 𝑣𝑠.
   For uchk to be a function one could determinize the choice of 𝑥, for example by ordering
variables and letting 𝑥 be the least variable that does not occur in 𝑣𝑠++modVars(uchk(𝑐 1, 𝑣𝑠)). In
our mechanization we instead use Hilbert’s “indefinite choice” operator.
   The definition of uchk for sequence is slightly delicate. Both recursive calls use the same
list 𝑣𝑠, which means the instrumentation variables added to 𝑐 1 may well be the same as those
added in 𝑐 2 . This is harmless, because the variables are initialized in each loop body (the as-
signment 𝑥 := 𝑒 1 where 𝑒 1 is framed by 𝑣𝑠). One might guess to change the definition to use
uchk(𝑐 2, 𝑣𝑠++modVars(uchk(𝑐 1, 𝑣𝑠)), which prevents re-use of an instrumentation variable for two
loops. The same idea can be used for the branches of an if. However, the chosen definition has
the nice feature that the given 𝑣𝑠 is used unchanged in every recursive call. This pays off in the
inductive proof of the main theorem and its supporting Lemma 5.3.
   Observe that the check added to a right-side loop body by uchk has the effect that a ∀∀ verification
will prove must-termination, whereas may-termination would be sufficient for ∀∃. Of course in the
absence of nondeterminacy, may- and must-termination are the same. In the presence of havoc,
must-termination may not hold, in which case the bicom should be rewritten to one that uses havf
to filter out any potential nontermination. For an example, see case 𝐵 2 in Figure 3.
   The bicom check function maps 𝐵 to a bicom chk(𝐵, 𝑣𝑠) with loops instrumented to assert
right-side execution decreases the declared variant expressions. Filtered havocs are also guarded
by an existence assertion. The definition is in Figure 12. The instrumentation only adds variables
on the right side, so it is convenient to define modVarsR(𝐵) to be the list of variables modified on
the right side of 𝐵, namely those in havf and on the right side of ⟨_ | _⟩.
9 For any 𝑐 we define   modVars(𝑐 ) to be the list of variables modified in 𝑐, namely variables that are assigned or havoc’d.
The omitted definition is straightforward recursion on syntax.
20                                                         Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


     𝐵                                              chk(𝐵, 𝑣𝑠)
     ⟨𝑐 | 𝑐 ′ ⟩                                     ⟨𝑐 | uchk(𝑐 ′, 𝑣𝑠)⟩
     assert P                                       assert P
     havf 𝑥 P                                       assert (∃ |𝑥 . P); havf 𝑥 P
     𝐵 1 ; 𝐵 2,                                     chk(𝐵 1, 𝑣𝑠); chk(𝐵 2, 𝑣𝑠)
     if 𝑒 | 𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4                     if 𝑒 | 𝑒 ′ chk(𝐵 1, 𝑣𝑠) chk(𝐵 2, 𝑣𝑠) chk(𝐵 3, 𝑣𝑠) chk(𝐵 4, 𝑣𝑠)
     while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 1        while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 2
                                                       where 𝐵 2 is havf 𝑥 1 ( [⟩𝑥 1 ]⟩ = 𝐸);
                                                                         havf 𝑥 2 ( [⟩𝑥 2 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ ));
                                                                         chk(𝐵 1, 𝑣𝑠);
                                                                         assert ( [⟩𝑥 2 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 1 ]⟩ )
                                                       and 𝑥 1, 𝑥 2 are distinct and not in 𝑣𝑠++modVarsR(chk(𝐵 1, 𝑣𝑠))

                                         Fig. 12. The chk transformation on bicoms


   In the loop case, the two-state expression 𝐸 is used as a variant. It is only relevant for right-only
iterations where it must decrease (due to changes on the right side since any left variables will
remain unchanged). Integer variable 𝑥 1 snapshots the value of 𝐸 and boolean variable 𝑥 2 snapshots
the truth value of the condition10 under which the current iteration will be right only, which is the
relation [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P). In the definition of uchk an assignment command can be used for
the snapshot, but here 𝐸 and the condition [⟩𝑒 ′ ]⟩ ∧ P ′ depend on a pair of states so we cannot use
assignments for 𝑥 1 and 𝑥 2 . In our experience, it is often sufficient for 𝐸 to be a right-only expression
in which case assignment could be used.
   As with uchk, the definition of chk has the nice feature that 𝑣𝑠 is unchanged in recursive calls.
This is achieved by allowing that instrumentation variables may be re-used between conditional
branches and between bicoms in sequence, while ensuring that nested loops have distinct variables.
This feature considerably simplifies the proofs compared with other formulations that we tried.
   A key technical result is that the biprojections commute with chk. On the left side this is only up
                                                                                            ↼−−−−−−−− ↼   −
to , because ↼    _− replaces assertions and assumptions with skip. (In fact we have chk(𝐵, 𝑣𝑠) ≃ 𝐵
but the two are not identical.) The same for ↼        ↼ _−.
                    ↼−−−−−−−
                    ↼                    ↼↼−           −−−−−−−−⇀
                                                               ⇀         −⇀
                                                                         ⇀
   Lemma 5.1. chk(𝐵, 𝑣𝑠)  chk( 𝐵 , 𝑣𝑠) and chk(𝐵, 𝑣𝑠) = chk( 𝐵 , 𝑣𝑠).
  In general chk(𝐵, 𝑣𝑠) acts on variables that are not in 𝑣𝑠. In particular, bFrame(𝐵, 𝑣𝑠) does not
imply bFrame(chk(𝐵, 𝑣𝑠), 𝑣𝑠). However, it does imply semantic framing of chk(𝐵, 𝑣𝑠), which will
be used in conjunction with Lemma 4.13.
     Lemma 5.2.      (i) cFrame(𝑐, 𝑣𝑠) implies 𝑣𝑠 ⊩ uchk(𝑐, 𝑣𝑠)
                                      −−−−−−−−⇀
                                              ⇀
      (ii) bFrame(𝐵, 𝑣𝑠) implies 𝑣𝑠 ⊩ chk(𝐵, 𝑣𝑠)
     (iii) bFrame(𝐵, 𝑣𝑠) implies 𝑣𝑠 ⊩ chk(𝐵, 𝑣𝑠)
   The proofs go by induction on structure of the command/bicom, with inner inductions for loop
execution. Detailed semantic analyses are needed, especially for loop bodies. For both uchk and chk,
the behavior is altered because the added assertions can fail. However, whether failure happens is
influenced only by the assumed relation (for havf) or the variant (for loop), and those are framed by
𝑣𝑠. That influence goes via snapshot variables that are outside 𝑣𝑠 (and outside the snapshot variables
of inner loop bodies, which must be shown to preserve their values) so the proof requires more than
10 The condition on 𝑥 is written using the symbol = but one could as well write ⇔ since the type is boolean. For any
                            2
𝑠, 𝑠 ′ we have 𝑠, 𝑠 ′ |= [⟩𝑥 2 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P ) ) iff the value of 𝑠 ′ (𝑥 2 ) is true or false according to whether
𝑠, 𝑠 ′ |= [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P ) ).
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                        21


simple application of induction hypotheses. A key point is that for a bi-while 𝐵, the instrumented
body (𝐵 2 in Figure 12) is semantically framed by 𝑣𝑠. (Indeed, this motivates the definition of 𝑣𝑠 ⊩ _.)

5.2    Main result
                                                                     ¥ S, which is an ∀∀ property,
The main result says that if the bicom chk(𝐵, 𝑣𝑠) satisfies a spec R {
                     −
                     ↼       −
                             ⇀                         ∃
then the projections 𝐵 and 𝐵 satisfy the ∀∃ spec R ≈> S. An analogous result holds for uchk.

                                                                                          ¥ S then
   Lemma 5.3. Suppose cFrame(𝑐, 𝑣𝑠) and 𝑣𝑠 ⊩ R and 𝑣𝑠 ⊩ S. If |= ⟨skip | uchk(𝑐, 𝑣𝑠)⟩ : R {
                 ∃
|= skip | 𝑐 : R ≈> S.


    Theorem 5.4. Suppose 𝐵, 𝑣𝑠, R, and S satisfy the following. (i) 𝐵 is well-formed. (ii) bFrame(𝐵, 𝑣𝑠).
                                                             ↼− ⇀  −       ∃
                                                ¥ S. Then |= 𝐵 | 𝐵 : R ≈> S.
(iii) 𝑣𝑠 ⊩ R and 𝑣𝑠 ⊩ S. (iv) |= chk(𝐵, 𝑣𝑠) : R {

                                          ∃                                                  ↼−
    As a corollary, to prove 𝑐 | 𝑐 ′ : R ≈> S it suffices to find well-formed 𝐵 such that 𝐵 ≃ 𝑐 and
−
⇀
 𝐵 ≃ 𝑐 ′ and to prove |= chk(𝐵, 𝑣𝑠) : R {  ¥ S for suitable 𝑣𝑠. Finding a frame 𝑣𝑠 that satisfies (ii) and
(iii) is, in practice, a straightforward syntactic matter as mentioned in Section 6.
    Full detailed proofs of both Lemma 5.3 and Theorem 5.4 are provided in the appendix. The
proof of the lemma is similar to the proof of the theorem. The theorem is proved by induction
on size(𝐵) and thus cases on the bicom forms. The list 𝑣𝑠 is fixed but R, S are general in the
induction hypothesis, which requires them to be framed by 𝑣𝑠. In each case, key consequences of
the assumption |= chk(𝐵, 𝑣𝑠) : R {     ¥ S are derived using wlp equations, leading to application of
                                         − ⇀
                                         ↼   −      ∃
proof rules (Figure 5) to establish |= 𝐵 | 𝐵 : R ≈> S.
    The base case where 𝐵 is havf 𝑥 Q sets the main pattern used throughout the proof.11 The
correctness judgment is put in wlp form which is then used to establish the premises of a proof
rule (or rules) for the projections of 𝐵, in this case eSkipHav in Figure 5.

                            chk(havf 𝑥 Q) : R {   ¥ S
                      ⇔          « wlp/correctness Lemma 4.8(i) »
                            R ⇒ wlp(chk(havf 𝑥 Q), S)
                      ⇔          « definition of chk (Figure 12) »
                            R ⇒ wlp(assert ∃ |𝑥 . Q; havf 𝑥 Q, S)
                      ⇔          « wlp equations for seq, assert, havf (Lemma 4.10) »
                            R ⇒ ∃ |𝑥 . Q ∧ ∀|𝑥 . (Q ⇒ S)
                      ⇒          « predicate calculus »
                            R ⇒ ∃ |𝑥 . S
                      ⇒          « rule eSkipHav and its soundness (Theorem 3.3) »
                                              ∃
                            skip | hav 𝑥 : R ≈> S
                      ⇔          « def ↼_− and ⇀−_ »
                            ↼−−−−−−− −−−−−−−⇀         ∃
                            havf 𝑥 Q | havf 𝑥 Q : R ≈> S



11 Note: every line of the calculation should begin with |=, as we are reasoning about valid judgments and valid implications,

so for brevity we elide |= throughout. We also elide 𝑣𝑠 as an argument to chk (and uchk) as it is unchanged in recursive
calls to those functions.
22                                         Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


The case where 𝐵 is 𝐵 1 ; 𝐵 2 shows the role of framing in using the induction hypothesis.
       chk(𝐵 1 ; 𝐵 2 ) : R {    ¥ S
 ⇔             « def chk, wlp/correctness Lemma 4.8(i) »
       R ⇒ wlp(chk(𝐵 1 ); chk(𝐵 2 ), S)
 ⇔             « wlp equation for sequence (Lemma 4.10) »
       R ⇒ wlp(chk(𝐵 1 ), wlp(chk(𝐵 2 ), S))
 ⇔             « Abbreviate Q := wlp(chk(𝐵 2, 𝑣𝑠), S) »
       R ⇒ wlp(chk(𝐵 1 ), Q)
 ⇔                                                                           ¥ S by Lemma 4.8(ii) »
               « wlp/correctness Lemma 4.8(i) and fact that |= chk(𝐵 2 ) : Q {
       chk(𝐵 1 ) : R {      ¥ Q and chk(𝐵 2 ) : Q {¥ S
 ⇒             « ind. hyp. twice, using 𝑣𝑠 ⊩ Q from bFrame(𝐵 2, 𝑣𝑠) and 𝑣𝑠 ⊩ S by Lemmas 5.2 and 4.13 »
       ↼− −   ⇀           ∃             ↼− −⇀    ∃
       𝐵 1 | 𝐵 1 : R ≈> Q and 𝐵 2 | 𝐵 2 : Q ≈> S
 ⇒             « sequence rule eSeq »
       ↼− ↼   − −  ⇀ −   ⇀        ∃
       𝐵 1 ; 𝐵 2 | 𝐵 1 ; 𝐵 2 : R ≈> Q
 ⇔             « definitions of ↼    _− and ⇀
                                            −_ »
       ↼−−−− −−−−⇀                ∃
       𝐵 1 ; 𝐵 2 | 𝐵 1 ; 𝐵 2 : R ≈> Q
For the loop case we use as invariant I =     ˆ wlp(chk(𝐵), S). We get 𝑣𝑠 ⊩ I from the assump-
tions bFrame(𝐵, 𝑣𝑠) and 𝑣𝑠 ⊩ S, using Lemmas 5.2 and 4.13. By definitions, I satisfies |= I ⇒
𝐺 (𝑒, 𝑒 ′, L, R, 𝐵, Q) (I) for 𝐺 in Lemma 4.10, whence I implies each of the conditions (Gi) there.
Those implications are used to establish the premises of rule eDo, using also eConseq.

6    Prototype
The prototype is being used to investigate the effectiveness of the filter adequacy transformation. It
is a modified version of an existing tool [50] that supports a bicom-like syntax which it translates
to unary code and annotations in a subset of WhyML, the source language of the Why3 verifier.12
Why3 in turn generates verification conditions and dispatches them to SMT solvers. The existing
tool interprets pre-post specifications as ∀∀ properties. It implements projections which are used to
check that a user-provided alignment product corresponds to the associated user-provided unary
program(s).
   What we trust about the prototype is that, for programs acting on integer variables, it correctly
verifies judgments of the form |= 𝐵 : P {    ¥ Q. One reason this is of interest is that—if 𝐵 has no
                          − ⇀
                          ↼   −       ∀
havf—then it implies |= 𝐵 | 𝐵 : P ≈> Q. This fact is not needed, however, for our development.
   Our prototype extends the existing tool in two ways. First, it adds the havf construct (including
its translation to right havoc followed by assumption) together with variant declarations on
loops. Second, it applies the filter adequacy transformation on procedure body syntax trees, after
desugaring and typechecking, just before translation to Why3. The prototype only supports a subset
of the features supported by the existing tool; it emits warnings about features that are unsupported
or unsound in ∀∃ mode such as right side procedure calls. The computation of projections has been
                                          ↼−          −
                                                      ⇀
extended to havf. Checking conditions 𝐵 ≃ 𝑐 and 𝐵 ≃ 𝑐 ′ was done manually for our examples.
   Although the transformation is very close to the chk and uchk functions in Figures 11 and 12, the
implementation, which is in OCaml, does not pass around the “avoid list” 𝑣𝑠. Instead, it generates
fresh names for the snapshot variables using a global counter. Our prototype has been used to
verify examples including those in Section 2. Verification goes through automatically using simple
invariant annotations as indicated in Section 2. User interaction is limited to selecting which solver

12 www.why3.org
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                23


to apply as usual in Why3. Existential quantifiers can be challenging for SMT solvers, but the the
existentially quantified asserts for our havf are equalities that solve automatically.

7   Related work
Relational verification is an active area of research encompassing secure compilation [1], probabilis-
tic reasoning for security and privacy [5, 37], regression verification [57], functional specification
of tensor programs [34], just to name a few directions. Here we focus on works close to our goals
and contributions, more or less following the order of our list of contributions in Section 1.
   Quite many relational Hoare logics have been proposed for ∀∀ and 𝑘-safety [28, 47] but few for
∀∃. One important line of work has developed relational separation logics, based on Iris [42], for
refinement of concurrent programs [32, 33, 58]. Iris is implemented in the Rocq interactive proof
assistant. These logics are quite complicated; while expressive and powerful, they are very different
from systems based on first order assertions and amenable to SMT-based automation in auto-active
tools like Dafny and Viper.
   Our focus is on sequential progams and alignment-oriented logics13 for which one of the first
∀∃ logics is RHLE [25]. It addresses nondeterminacy both in the form of havoc and in the form of
underspecified procedure calls. The logic uses three judgments: in addition to the ∀∃ judgment
(like ours but without failure), there is the standard partial correctness judgment (called universal)
and the less common forward under-approximation judgment (called existential) that can be
                           ∃
written skip | 𝑐 : [⟩𝑝 ]⟩ ≈> [⟩𝑞 ]⟩ in our notation. The existential judgment has been called possible
correctness [40], sufficient incorrectness [4], etc. RHLE is designed to cater for automated proof
search. The primary relational rules provide for unary reasoning on one side or the other in forward
symbolic execution style, relying on the unary logics and unary over- and under-approximate
procedure specifications. Alignment of loops is achieved using mostly-lockstep rules adapted
from Sousa and Dillig [56]. Choice variables, a kind of logical variable, are used to facilitate
reasoning about existential witnesses.
   Building on RHLE, Beutner develops FEHL (forall-exist Hoare logic) [15]. It lacks procedures
but is more general than RHLE in that it handles ∀𝑘 ∃𝑙 judgments. Like RHLE, FEHL decomposes
reasoning about ∀∃ properties in terms of reasoning about single programs in isolation, using
ordinary Hoare logic and a complete underapproximate unary logic. Like RHLE, the core rules cater
for proof search and include the rules for reasoning forward on one side or the other via the unary
logics. FEHL features a novel rule for reasoning about loops in non-lockstep alignment: it aligns
𝑛 iterations of one loop with 𝑚 iterations of another loop, for fixed 𝑛 and 𝑚. There are naturally
occuring examples of this [18]. But it does not support more general alignments of loops as needed
for data dependent alignments like example 𝑐1 in Section 2 and those considered in [6, 55] for
∀∃ and in [59]. The approach to witnessing existentials is to reason about symbolic values and
postpone witness choices.
   Our approach is applicable to ∀𝑘 ∃𝑙 properties but many practical examples do not need the extra
generality. Restriction to ∀∃ facilitates streamlined notations in theory and in prototypes.
   In an unpublished preprint, Wu et al. [61] introduce a ∀∃ relational Hoare logic in which the
relational judgment is asymmetric with respect to the two programs to be related. Following the
approach of [32, 33, 58], the existential program (called the abstract program, with reference to
refinement) appears in the pre- and post-relations with a special predicate related to wlp. Like
RHLE and FEHL, it focuses on rules rules that “take a step” on the universally or existentially
quantified side based on unary logic. The treatment of loop alignment is limited. The main focus of
the work is an encoding into ordinary Hoare logic, to which we return later.
13 As opposed to taking a global view of traces [10].
24                                                  Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


   Another unpublished preprint [52] introduces a logic ERHL+ which uses only the single ∀∃
judgment. It features a general data-dependent loop alignment rule attributed to Beringer [14] and
a rewrite rule attributed to [7]. Similar rules can also be found in [11]. The rewrite rule is based
on full KAT equivalence and so can be used to derive the 𝑛, 𝑚-fixed-iteration rule of Beutner [15]
without use of alignment conditions. As noted earlier, our logic is directly adapted from ERHL+,
because we find its rules to be simple and orthogonal like those of standard Hoare logic. The focus
of the paper is on the logic’s completeness with respect to alignments that can be described by
alignment automata. To this end the authors introduce a form of annotated product automaton
called filtered, from which we borrow the term.
   Moving on to work on alignment products, i.e., precursors to bicoms, early work is found
in [8] for ∀∀, see also [9]. Works that represent products as automata (i.e., transition systems)
include Churchill et al. [18] and Shemer et al. [55]. The latter uses constrained Horn clauses
(CHC) [38] to encode the transition system and alignment condition adequacy, using CHC solving
to simultaneously infer inductive relational invariants and alignment conditions for ∀∀ properties.
Unno et al. [59] introduce a solver for a special class of constraints in order to verify ∀∃ properties
by also inferring well founded relations for termination. By contrast with the filtering approach,
Unno et al. [59] also solve for Skolem functions that witness existentials. Itzhaky et al. [41] show
how CHC solvers can be used for ∀∃, building on the representation of witnesses as strategies in a
game [16].
   Syntactic representation of product programs is convenient as a way to reduce relational verifi-
cation to unary verification for which a wide range of tools are available [9]. Antonopoulos et al.
[2] give an algebraic formulation (called BiKAT, in reference to KAT [43]) that is shown to subsume
∀∀ relational logic. It is also used to express ∀∃ by combining a ∀∀ condition with inequations that
express adequacy. Our embed notation ⟨𝑐 | 𝑐 ′ ⟩ is inspired by that work. The idea is to use equational
reasoning to manipulate ⟨𝑐 | 𝑐 ′ ⟩ into a better aligned form by inserting assumptions (i.e., filters). But
the adequacy check is via equations that do not correspond to a standard property for which tools
exist,14 by contrast with our transformation that reduces adequacy to ∀∀. One subsequent work
adapts BiKAT to probabilistic relational logic [35]. The KestRel tool [24] uses an algebra similar to
BiKAT with e-graphs in data-driven automatic search for good alignments for ∀∀ verification. This
is complementary to the problem addressed in this paper. Support for manipulating bicoms would
be important in an auto-active tool for programs beyond the reach of full automated verification.
   Readers familiar with the product notations of Antonopoulos et al. [2] or Dickerson et al. [24]
might expect that our Definition 4.3 of  should include additional equations including laws of
the form ⟨𝑐 | 𝑐 ′ ⟩; ⟨𝑑 | 𝑑 ′ ⟩  ? ⟨𝑐; 𝑑 | 𝑐 ′ ; 𝑑 ′ ⟩ or ⟨𝑐 | skip⟩; ⟨skip | 𝑐 ′ ⟩  ? ⟨skip | 𝑐 ′ ⟩; ⟨𝑐 | skip⟩. However
the possibility of failure invalidates these. For example, ⟨skip | 𝑑𝑖𝑣𝑒𝑟𝑔𝑒⟩; ⟨fail | skip⟩ does not fail,
whereas both ⟨fail | 𝑑𝑖𝑣𝑒𝑟𝑔𝑒⟩ and ⟨fail | skip⟩; ⟨skip | 𝑑𝑖𝑣𝑒𝑟𝑔𝑒⟩ fail. This is a topic for future work
that may draw on FailKAT [48], and is important for reasons discussed in the previous paragraph.
   The ∀∀ logic of Banerjee et al. [6] combines deductive rules with a rule of rewriting (like eRewrite
in Figure 5) using a bicom-like notation that includes an embed construct like our ⟨_ | _⟩. Their
∀∀ property disallows failure entirely, and the phenomena mentioned in the preceding paragraph
are avoided by using smallstep semantics with dovetailed execution of the embed construct. That
semantics, however, is not easily reconciled with our goal that bicoms have a straightforward
translation to unary code. Indeed, their prototype verifier [50] uses the sequential encoding and thus
                                                                                                 ∀
with respect to failure it is verifying a property like our Definition 3.1 for ≈>. (In other regards the


14 Aside from decision procedures for KAT, which generally do not support semantic interpretation of commands or

expressive assertions [36, 44].
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                             25


prototype is very close to the logic.) The weaker treatment of failure does not seem disadvantageous
in practice, since absence of failure is a unary property that can be checked as such.
   The programs handled by [6, 50] have procedures and act on dynamically allocated object
structures. Although allocation is often modeled by nondeterministic choice, ∀∃ properties are
avoided by considering relations that describe the heap up to bijective renaming as in [12]. To
extend our prototype to soundly handle procedures and pointer structures, some features such as
frame conditions with read effects should be revisited in connection with proving ∀∃ properties.
   We are not aware of prior work that translates ∀∃ judgments to a ∀∀ property of a product. The
closest work is the preprint of Wu et al. [61] which translates ∀∃ judgments to judgments in unary
Hoare logic. As noted above, their ∀∃ judgment is phrased as a pre-post condition on the “concrete”
program 𝑐 where the pre and post refer to computation by the abstract program 𝑐 ′ as a resource in
the sense of separation logic. The judgment has a bespoke semantics that refers to the computations
of both 𝑐 and 𝑐 ′ [32, 33, 58]. What Wu et al. [61] do is encode this semantics in Hoare triples with
ordinary semantics, using pre/post conditions expressed in terms of an operation derived from
𝑤𝑙𝑝 (𝑐 ′ ) so that the ∀∃ semantics gets encoded using existential quantification within pre/post.15
This encoding is used to verify some examples and also to derive Hoare logic rules that correspond
to relational logic. The goal of this work is similar to ours: reducing relational verification to unary
in order to leverage existing tools. The work is carried out in Rocq, however, and it is not clear that
the encoding is amenable to use of automated theorem provers for practical application.
   One advantage of logics, compared with annotation-oriented tools, is that proof rules can embody
reasoning principles beyond assertion-based, such as the rule of conjunction and frame rules. An
important principle is transitive composition, known as vertical composition in works on refinement.
(Transitive composition motivated the ∀∃ semantics called relative termination in Hawblitzel et al.
[39] where deterministic programs are considered.) Such principles, for 𝑘-safety, are developed in
the work of [28] on verifications that seem out of reach of many relational logics but are within
reach of ERHL+ (as discussed in [51]) provided the assertion language allows explicit use of wlp as
in [28].
   The assertions used in Wu et al. [61] makes use of wlp as well as explicit quantification over states
(and even logical variables of type set-of-states). Dardinier and Müller [22] develop a Hoare style
logic for hyperproperties, in which pre- and post-condition are second order predicates. The logic
applies to a single program. The correctness judgment says that for any set of initial states satisfying
the precondition, the direct image (collecting semantics) is a set that satisfies the postcondition.
Many hyperproperties including ∀∃ can be expressed owing to the ability to quantify over states in
the specification. [21] show that, remarkably, this approach is amenable to SMT-based automation,
by encodings that track both over and under approximations of the collecting semantics. A novel
hint annotation is used to help with nondeterministic choices. Their prototype is used to verify (or
refute) correctness of many examples from the literature, and relies on several loop rules. Outcome
Logic [63] is another Hoare style logic in which postconditions can be predicates on sets of states;
in general, predicates on an outcome monoid. Such monoids encompass not only powerset but also
probability distributions and error monads. The approach has been developed further to encompass
the challenging combination of demonic nondeterminacy with probability [62, 64].




15 In appendix C of the document, the development is extended to include assertions and failures. The ∀∃ judgment is

interpreted to say that (a) from related initial states where 𝑐 can fail, 𝑐 ′ must fail too, and (b) for any normal termination of
𝑐, either 𝑐 ′ fails or it can terminate in a state that satisfies the postcondition. This perhaps accords with a view of failure as
undefinedness.
26                                                          Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


A      Appendix: main proofs
This section provides detailed proofs for the results in Section 5.2. Also, the size function is defined
in Figure 13 and the full definition of command semantics is in Figure 14.

     𝑐                        size(𝑐)                           𝐵                                size(𝐵)
     skip                     0                                 ⟨𝑐 | 𝑐 ′ ⟩                       1 + size(𝑐 1 ) + size(𝑐 2 )
     𝑥 := 𝑒                   1                                 assert P                         1
     hav 𝑥                    1                                 havf 𝑥 P                         1
     𝑐1; 𝑐2                   1 + size(𝑐 1 ) + size(𝑐 2 )       𝐵1 ; 𝐵2                          1 + size(𝐵 1 ) + size(𝐵 2 )
     if 𝑒 then 𝑐 1 else 𝑐 2   1 + size(𝑐 1 ) + size(𝑐 2 )       if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4        1 + (+ 𝑖 : 1 ≤ 𝑖 ≤ 4 : 𝐵𝑖 )
     while 𝑒 do 𝑐 1           1 + size(𝑐 1 )                    while 𝑒 |𝑒 ′ algn L|R do 𝐵 1     1 + size(𝐵 1 )

                                            Fig. 13. Size of commands and bicoms




               𝑠 |= 𝑝                      𝑠 ̸ |= 𝑝                        𝑛∈Z                            𝑠 (𝑒) = 𝑛
          assert 𝑝/𝑠 ⇓ 𝑠             assert 𝑝/𝑠 ⇓                 hav 𝑥/𝑠 ⇓ 𝑠 [𝑥 ↦→ 𝑛]             𝑥 := 𝑒/𝑠 ⇓ 𝑠 [𝑥 ↦→ 𝑛]

       𝑐/𝑠 ⇓ 𝑡          𝑑/𝑡 ⇓ 𝜙           𝑐/𝑠 ⇓                   𝑠 |= 𝑒     𝑐/𝑠 ⇓ 𝜙                𝑠 ̸ |= 𝑒    𝑑/𝑠 ⇓ 𝜙
             𝑐; 𝑑/𝑠 ⇓ 𝜙                 𝑐; 𝑑/𝑠 ⇓                if 𝑒 then 𝑐 else 𝑑/𝑠 ⇓ 𝜙          if 𝑒 then 𝑐 else 𝑑/𝑠 ⇓ 𝜙

                  𝑠 ̸ |= 𝑒                 𝑠 |= 𝑒       𝑐/𝑠 ⇓               𝑠 |= 𝑒     𝑐/𝑠 ⇓ 𝑡      while 𝑒 do 𝑐/𝑡 ⇓ 𝜙
          while 𝑒 do 𝑐/𝑠 ⇓ 𝑠               while 𝑒 do 𝑐/𝑠 ⇓                            while 𝑒 do 𝑐/𝑠 ⇓ 𝜙

                                                Fig. 14. Semantics of commands



   Remark A.1. Definition 4.3 of  does not include congruence clauses. It may seem natural to include
them even though we have no specific use for them. In fact congruence with respect to sequence and
bi-if is no problem, but congruence for bi-while would falsify Lemma 4.6. This is an artifact of the
current definition of ↼ ↼_− which is used in the semantics of bi-while. Because ↼ _− discards bi-assertions
                                                                                  ↼
and havf, semantic equivalence is not a congruence with respect to bi-while. For example, let 𝐵 0 be
assert ff; ⟨𝑥 := 0 | skip⟩ and 𝐵 1 be assert ff; ⟨𝑥 := 1 | skip⟩. They are semantically equivalent, i.e.,
J 𝐵 0 K = J 𝐵 1 K. Consider their use in this context: while 𝑥 < 0|ff algn tt|ff do 𝐵𝑖 . From initial stores
where 𝑥 on the left is negative, this iterates once and sets 𝑥 to 0 or 1 depending on whether 𝐵 0 or 𝐵 1 is
used. This peculiarity can probably be avoided by defining ↼   ↼_− to keep assertions like ⇀−⇀
                                                                                             _ does, but the
current definitions slightly streamline the proof of our main result.                                      □

  A note about the proofs to follow: In the hints we say “predicate calculus” both for reasoning in
the ambient logic and for manipulating shallow embedded assertions and relations.

                                                                                          ¥ S then
   Lemma 5.3. Suppose cFrame(𝑐, 𝑣𝑠) and 𝑣𝑠 ⊩ R and 𝑣𝑠 ⊩ S. If |= ⟨skip | uchk(𝑐, 𝑣𝑠)⟩ : R {
                 ∃
|= skip | 𝑐 : R ≈> S.

   Proof. By structural induction on 𝑐, keeping R and S general. So the induction hypothesis is that
                                                                                                  ∃
                                                                        ¥ Q then |= skip | 𝑑 : P ≈> Q.
for any subprogram 𝑑 of 𝑐, and any P, Q, if |= ⟨skip | uchk(𝑑, 𝑣𝑠)⟩ : P {
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                  27


    case 𝑐 is skip


                                                                      ¥ S
                                       |= ⟨skip | uchk(skip, 𝑣𝑠)⟩ : R {
                                ⇔           « definition of uchk (Figure 11) »
                                       |= ⟨skip | skip⟩ : R {¥ S
                                ⇒           « adequacy of embed: Lemma 4.7 »
                                                           ∀
                                       |= skip | skip : R ≈> S
                                ⇒           « Lemma 3.4(i) »
                                                           ∃
                                       |= skip | skip : R ≈> S


   case 𝑐 is assignment or havoc The argument is the same as for skip, because uchk leaves them
unchanged and they always terminate so we can apply Lemma 3.4(ii).
   case 𝑐 is assert 𝑝


                                                 ¥ S
              |= ⟨skip | uchk(assert 𝑝, 𝑣𝑠)⟩ : R {
        ⇔          « definition of uchk »
                                       ¥ S
              |= ⟨skip | assert 𝑝⟩ : R {
        ⇔          « wlp/correctness Lemma 4.8(i) »
              |= R ⇒ wlp(⟨skip | assert 𝑝⟩, S)
        ⇔          « definition of wlpR and wlpR equation in Lemma 4.9 »
              |= R ⇒ [⟩𝑝 ]⟩ ∧ S
                                                                       ∃
        ⇒          « rule eConseq, using skip | assert 𝑝 : [⟩𝑝 ]⟩ ∧ S ≈> S from rule eSkipAssert »
                                   ∃
              skip | assert 𝑝 : R ≈> S


   case 𝑐 is if 𝑒 then 𝑐 1 else 𝑐 2 For clarity we elide |= throughout, and we elide 𝑣𝑠 as an argument
to uchk, noting that 𝑣𝑠 is the same in recursive calls to uchk.


        ⟨skip | uchk(if 𝑒 then 𝑐 1 else 𝑐 2 )⟩ : R {  ¥ S
 ⇔           « wlp/correctness Lemma 4.8(i), definition of uchk »
        R ⇒ wlp(⟨skip | if 𝑒 then uchk(𝑐 1 ) else uchk(𝑐 2 )⟩, S)
 ⇔           « wlpR definition (twice) and wlpR equation for if (Lemma 4.9); predicate calculus »
        R ∧ [⟩𝑒 ]⟩ ⇒ wlp(⟨skip | uchk(𝑐 1 )⟩, S) and R ∧ [⟩ ¬𝑒 ]⟩ ⇒ wlp(⟨skip | uchk(𝑐 2 )⟩, S)
 ⇔           « wlp/correctness Lemma 4.8(i) »
        ⟨skip | uchk(𝑐 1 )⟩ : R ∧ [⟩𝑒 ]⟩ {¥ S and ⟨skip | uchk(𝑐 2 )⟩ : R ∧ [⟩ ¬𝑒 ]⟩ {
                                                                                     ¥ S
 ⇒           « induction hypothesis for 𝑐 1 and for 𝑐 2 , note below »
                                 ∃
                                                                   ¥ S
        skip | 𝑐 1 : R ∧ [⟩𝑒 ]⟩ ≈> S and skip | 𝑐 2 : R ∧ [⟩ ¬𝑒 ]⟩ {
 ⇒           « rule eSkipIf »
                                           ∃
        skip | if 𝑒 then 𝑐 1 else 𝑐 2 : R ≈> S


To apply the induction hypothesis we need cFrame(𝑐1, 𝑣𝑠) and cFrame(𝑐2, 𝑣𝑠) which follow easily
from cFrame(𝑐, 𝑣𝑠) which also gives 𝑣𝑠 ⊩ 𝑒. That in turn gives 𝑣𝑠 ⊩ R ∧ [⟩𝑒 ]⟩ and 𝑣𝑠 ⊩ R ∧ ¬ [⟩𝑒 ]⟩ as
needed to apply the induction hypothesis.
28                                                     Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


     case 𝑐 is 𝑐 1 ; 𝑐 2 Again we elide 𝑣𝑠 as an argument to uchk.

           ⟨skip | uchk(𝑐 1 ; 𝑐 2 )⟩ : R { ¥ S
     ⇔          « def uchk »
           ⟨skip | uchk(𝑐 1 ); uchk(𝑐 2 )⟩ : R {  ¥ S
     ⇔          « Lemma 4.8(i), wlpR def and Lemma 4.9; abbreviate Q := wlpR(uchk(𝑐 2 ), S) »
           R ⇒ wlpR(uchk(𝑐 1 ), Q)
     ⇔          « Lemma 4.8(i) and (ii), wlpR definition »
           ⟨skip | uchk(𝑐 1 )⟩ : R {     ¥ Q and ⟨skip | uchk(𝑐 2 )⟩ : Q {
                                                                         ¥ S
     ⇒          « induction hypothesis using 𝑣𝑠 ⊩ Q by Lemmas 5.2 and 4.13 »
                              ∃                      ∃
           skip | 𝑐 1 : R ≈> Q and skip | 𝑐 2 : Q ≈> S
     ⇒          « rule eSeq »
                                       ∃
           skip; skip | 𝑐 1 ; 𝑐 2 : R ≈> S
     ⇒          « rule eRewrite, skip; skip ≃ skip from Definition 3.2 »
                                 ∃
           skip | 𝑐 1 ; 𝑐 2 : R ≈> S

     case 𝑐 is while 𝑒 vnt 𝑒 𝑣 do 𝑑 By definition, uchk(while 𝑒 vnt 𝑒 𝑣 do 𝑑, 𝑣𝑠) is

                           while 𝑒 vnt 𝑒 𝑣 do 𝑥 := 𝑒 𝑣 ; uchk(𝑑, 𝑣𝑠); assert (0 ≤ 𝑒 𝑣 < 𝑥)

where 𝑥 is fresh with respect to 𝑣𝑠 and the assigned variables of uchk(𝑑, 𝑣𝑠). Thus by hypothesis of
the lemma 𝑥 is fresh for R and S as well as for 𝑑 and the variant expression 𝑒 𝑣 . We aim to apply
rule eSkipDo in Figure 6, using 𝑥 as the fresh variable and 𝑒 𝑣 as the variant. For an invariant let

                              I := wlpR(𝑥 := 𝑒 𝑣 ; uchk(𝑑, 𝑣𝑠); assert 0 ≤ 𝑒 𝑣 < 𝑥, S)

                                                                            ¥ S so by definition
The assumption for this case is ⟨skip | uchk(while 𝑒 vnt 𝑒 𝑣 do 𝑑, 𝑣𝑠)⟩ : R {
of wlpR and wlp/correctness lemma we have |= R ⇒ I. By the loop equation for wlpR we have
|= I ⇒ 𝐹 (I) by the fixpoint property,16 where 𝐹 is defined in Lemma 4.9. By predicate calculus
this is equivalent to the following.

                   |= I ∧ ¬ [⟩𝑒 ]⟩ ⇒ S                                                         (K1)
                   |= I ∧ [⟩𝑒 ]⟩ ⇒ wlpR(𝑥 := 𝑒 𝑣 ; uchk(𝑑, 𝑣𝑠); assert 0 ≤ 𝑒 𝑣 < 𝑥, I)         (K2)

Using rule eSkipDo we will prove

                                                                        ∃
                                    skip | while 𝑒 vnt 𝑒 𝑣 do 𝑑 : I ≈> I ∧ ¬ [⟩𝑒 ]⟩

                                                                            ∃
Then eConseq yields the goal skip | while 𝑒 vnt 𝑒 𝑣 do 𝑑 : R ≈> S using (K1) and R ⇒ I. It remains
to show the premise of eSkipDo, which in this instance is

                                                                   ∃
                               skip | 𝑑 : [⟩𝑒 ]⟩ ∧ I ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ ≈> I ∧ [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩


16We use that I is a postfixpoint but not that it is greatest.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                        29


To prove it we calculate starting from (K2), eliding |= and 𝑣𝑠.
               I ∧ [⟩𝑒 ]⟩ ⇒ wlpR(𝑥 := 𝑒 𝑣 ; uchk(𝑑); assert 0 ≤ 𝑒 𝑣 < 𝑥, I)
        ⇔           « wlpR equation for sequence (Lemma 4.9) »
               I ∧ [⟩𝑒 ]⟩ ⇒ wlpR(𝑥 := 𝑒 𝑣 , wlpR(uchk(𝑑), wlpR(assert 0 ≤ 𝑒 𝑣 < 𝑥, I)))
        ⇔           « wlpR equations for assignment and assert (Lemma 4.9) »
               I ∧ [⟩𝑒 ]⟩ ⇒ (wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I)) |𝑥   |𝑒 𝑣
        ⇒           « predicate calculus (strengthen antecedent) »
               I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ ⇒ (wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I)) |𝑥 |𝑒 𝑣
        ⇔           « substitution Lemma 4.16 »
               I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ ⇒ wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I)
        ⇔           « lifting Lemma 4.17 (still eliding |=) »
               ∀𝑛 ∈ Z. (I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ ⇒ wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I))𝑛𝑥
        ⇔           « substitution properties including Lemma 4.12 »
               ∀𝑛. I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑛 = 𝑒 𝑣 ]⟩ ⇒ (wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I))𝑛𝑥
        ⇒           « subst. lemmas incl. Lemma 4.15 and frame of uchk(𝑑), freshness of 𝑥 »
               ∀𝑛. I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑛 = 𝑒 𝑣 ]⟩ ⇒ wlpR(uchk(𝑑), [⟩ 0 ≤ 𝑒 𝑣 < 𝑛 ]⟩ ∧ I)
        ⇔           « def wlpR, wlp/correct »
               ∀𝑛. ⟨skip | uchk(𝑑)⟩ : I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ {  ¥ [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I
        ⇒           « induction hypothesis, defs ↼        _− and ⇀
                                                                 −_ »
                                                         ∃
               ∀𝑛. skip | 𝑑 : I ∧ [⟩𝑒 ]⟩ ∧ [⟩𝑥 = 𝑒 𝑣 ]⟩ ≈> [⟩ 0 ≤ 𝑒 𝑣 < 𝑥 ]⟩ ∧ I
Note that we use Lemma 4.17 to lift quantification over 𝑥 to the ambient logic, because the induction
hypothesis can’t be directly applied where there are occurrences of 𝑥 which is outside the frame 𝑣𝑠.
This in turn motivated our use of the metavariable formulation of rule eWhile. Apropos freshness
of 𝑥, we use that it is outside the assigned vars of uchk(𝑑) and that those frame uchk(𝑑).
   Note: at the point where we appeal to the induction hypothesis, if instead of a metavariable 𝑛
in rule eDo we used a program variable, there would be a term [⟩𝑒𝐸 ]⟩ that is not framed by 𝑣𝑠 (as
𝑥 𝐸 is fresh), so the induction hypothesis would not be applicable. That is why we need to apply
Lemma 4.17 at an earlier step.                                                                      □
   Before proceeding to the main theorem we note the following derived rule which is convenient
in the calculational proof.
         eDoX
                                            ∃                                                 ∃
              𝑐 | skip : I ∧ ⟨[𝑒 ⟨] ∧ P ≈> I            𝑐 | 𝑐 ′ : I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ≈> I
                                                                          ∃
          skip | 𝑐 ′ : I ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) ∧ (𝑛 = 𝐸) ≈> I ∧ (0 ≤ 𝐸 < 𝑛) for all 𝑛 ∈ Z
                                     ′                          ′    ′
                I ⇒ ( ⟨[𝑒 ⟨] = [⟩𝑒 ]⟩ ∨ (P ∧ ⟨[𝑒 ⟨] ) ∨ (P ∧ [⟩𝑒 ]⟩ ))             R⇒I          I⇒S
                                                                     ∃
                           while 𝑒 do 𝑐 | while 𝑒 ′ do 𝑐 ′ : R ≈> S ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩
The rule is derived from eDo simply using eConseq to allow general pre- and post-relations. It also
has a formally stronger precondition for the right-only premise, i.e., with added conjunct that
negates the left-only condition. (That is derived by instantiating the right alignment condition P ′
in eDo with P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P).)
    Theorem 5.4. Suppose 𝐵, 𝑣𝑠, R, and S satisfy the following. (i) 𝐵 is well-formed. (ii) bFrame(𝐵, 𝑣𝑠).
                                                             ↼− ⇀  −       ∃
                                                ¥ S. Then |= 𝐵 | 𝐵 : R ≈> S.
(iii) 𝑣𝑠 ⊩ R and 𝑣𝑠 ⊩ S. (iv) |= chk(𝐵, 𝑣𝑠) : R {
  Proof. The proof is by induction on size(𝐵). We keep 𝑣𝑠 fixed but leave R, S general, so the
induction hypothesis is as follows:
30                                           Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


         For all 𝐶, R, S, if size(𝐶) < size(𝐵), wf (𝐶), bFrame(𝐶, 𝑣𝑠), 𝑣𝑠 ⊩ R, 𝑣𝑠 ⊩ S, and
                                        − ⇀
                                        ↼   −       ∃
         |= chk(𝐶, 𝑣𝑠) : R {¥ S then |= 𝐶 | 𝐶 : R ≈> S.
For the given 𝐵, R, S we go by cases on 𝐵. In each case we calculate from assumption |= chk(𝐵, 𝑣𝑠) :
R {  ¥ S. Every line of the calculation should begin with |=, as we are reasoning about valid
judgments and valid implications, so for brevity we elide |= throughout. We also elide 𝑣𝑠 as an
argument to chk (and uchk) as it is unchanged in recursive calls to those functions.
   Although excerpts of this proof appear in Section 5.2, we repeat them here for readability.
   case 𝐵 is havf 𝑥 Q . This base case sets the main pattern used throughout the proof. The cor-
rectness judgment is put in wlp form which is then used to establish the premises of a proof rule
for the projections of 𝐵, in this case eSkipHav in Figure 5.

                         chk(havf 𝑥 Q) : R {   ¥ S
                   ⇔          « wlp/correctness Lemma 4.8(i) »
                         R ⇒ wlp(chk(havf 𝑥 Q), S)
                   ⇔          « definition of chk (Figure 12) »
                         R ⇒ wlp(assert ∃ |𝑥 . Q; havf 𝑥 Q, S)
                   ⇔          « wlp equations for seq, assert, havf (Lemma 4.10) »
                         R ⇒ ∃ |𝑥 . Q ∧ ∀|𝑥 . (Q ⇒ S)
                   ⇒          « predicate calculus »
                         R ⇒ ∃ |𝑥 . S
                   ⇒          « rule eSkipHav and its soundness (Theorem 3.3) »
                                           ∃
                         skip | hav 𝑥 : R ≈> S
                   ⇔          « def ↼_− and ⇀−_ »
                         ↼−−−−−−− −−−−−−−⇀         ∃
                         havf 𝑥 Q | havf 𝑥 Q : R ≈> S

     case 𝐵 is assert Q . The same reasoning pattern is used in this base case.

                             chk(assert Q) : R {   ¥ S
                        ⇔         « def chk, wlp/correctness Lemma 4.8(i) »
                             R ⇒ wlp(assert Q, S)
                        ⇔         « wlp equation for assert (Lemma 4.10) »
                             R ⇒ Q∧S
                        ⇒         « rules eSkipSkip and eConseq using R ⇒ S »
                             skip | skip : R {¥ S
                        ⇔         « def ↼ _− and ⇀
                                                 −_ »
                             ↼−−−−−−− −−−−−−−⇀         ∃
                             assert Q | assert Q : R ≈> S

     case 𝐵 is 𝐵 1 ; 𝐵 2 . This case shows the role of framing in using the induction hypothesis.

                                                 ¥ S
                             chk(𝐵 1 ; 𝐵 2 ) : R {
                       ⇔         « def chk, wlp/correctness Lemma 4.8(i) »
                             R ⇒ wlp(chk(𝐵 1 ); chk(𝐵 2 ), S)
                       ⇔         « wlp equation for sequence (Lemma 4.10) »
                             R ⇒ wlp(chk(𝐵 1 ), wlp(chk(𝐵 2 ), S))
At this point it is convenient to abbreviate Q =
                                               ˆ wlp(chk(𝐵 2, 𝑣𝑠), S). We have bFrame(𝐵 2, 𝑣𝑠) from
assumption bFrame(𝐵 1 ; 𝐵 2, 𝑣𝑠). So we have 𝑣𝑠 ⊩ chk(𝐵 2 ) by Lemma 5.2, whence by Lemma 4.13
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                31


and the assumption 𝑣𝑠 ⊩ S we get 𝑣𝑠 ⊩ Q. The calculation continues:
   R ⇒ wlp(chk(𝐵 1 ), Q)
 ⇔                                                                       ¥ S by Lemma 4.8(ii) »
           « wlp/correctness Lemma 4.8(i) and fact that |= chk(𝐵 2 ) : Q {
   chk(𝐵 1 ) : R {      ¥ Q and chk(𝐵 2 ) : Q {¥ S
 ⇒         « induction hypothesis for 𝐵 1 and 𝐵 2 , using 𝑣𝑠 ⊩ Q »
   ↼− −   ⇀           ∃             ↼− −⇀    ∃
   𝐵 1 | 𝐵 1 : R ≈> Q and 𝐵 2 | 𝐵 2 : Q ≈> S
 ⇒         « sequence rule eSeq »
   ↼− ↼   − −  ⇀ −   ⇀        ∃
   𝐵 1 ; 𝐵 2 | 𝐵 1 ; 𝐵 2 : R ≈> Q
 ⇔         « definitions of ↼    _− and ⇀
                                        −_ »
   ↼−−−− −−−−⇀                ∃
   𝐵 1 ; 𝐵 2 | 𝐵 1 ; 𝐵 2 : R ≈> Q
Appeal to the induction hypothesis is justified by size(𝐵𝑖 ) < size(𝐵 1 ; 𝐵 2 ).17 Use of the induction hy-
pothesis also requires that each 𝐵𝑖 is well-formed and bFrame(𝐵𝑖 , 𝑣𝑠). These are easy consequences
of the corresponding assumptions (i) and (ii) about B.
   Note that “and” in the intermediate steps above is at the meta level and we could have written
   ↼− −  ⇀                        ↼− −  ⇀
                 ¥ Q and |= 𝐵 2 | 𝐵 2 : Q {
|= 𝐵 1 | 𝐵 1 : R {                              ¥ S to be precise.
    case 𝐵 is if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4 . The importance of well-formedness only emerges in this case. It
                                             ↼− ↼  − ↼ − ↼  − −⇀ −  ⇀ − ⇀ −   ⇀
gives us the syntactic equivalences 𝐵 1 ≃ 𝐵 2 , 𝐵 3 ≃ 𝐵 4 , 𝐵 1 ≃ 𝐵 3 , 𝐵 2 ≃ 𝐵 4 . By symmetry we reverse
them, and list them in the order used below:
                                      ↼− ↼  − −  ⇀ −  ⇀ ↼  − ↼   − −⇀ −    ⇀
                                      𝐵2 ≃ 𝐵1 𝐵3 ≃ 𝐵1 𝐵4 ≃ 𝐵3 𝐵4 ≃ 𝐵2                                   (8)
In the following we elide the 𝑣𝑠 argument to chk, as it is the same throughout.
           chk(if 𝑒 |𝑒 ′ 𝐵 1 𝐵 2 𝐵 3 𝐵 4 ) : R {    ¥ S
     ⇔            « def chk, wlp/correctness Lemma 4.8(i) »
           R ⇒ wlp(if 𝑒 |𝑒 ′ chk(𝐵 1 ) chk(𝐵 2 ) chk(𝐵 3 ) chk(𝐵 4 ), S)
     ⇔            « wlp equation for if (Lemma 4.10) »
           R ⇒ ( ( ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 1 ), S)) ∧ ( ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 2 ), S)) ∧
                       (¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 3 ), S)) ∧ (¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 4 ), S)) )
     ⇔            « pred. calc. and semantics of conjunction, leaving |= implicit »
             R ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 1 ), S) and R ∧ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 2 ), S) and
             R ∧ ¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 3 ), S)) and R ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ wlp(chk(𝐵 4 ), S)
     ⇔            « wlp property Lemma 4.8(i) »
             chk(𝐵 1 ) : R ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ {  ¥ S and chk(𝐵 2 ) : R ∧ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ {  ¥ S and
             chk(𝐵 3 ) : R ∧ ¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ {   ¥ S and chk(𝐵 4 ) : R ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ {¥ S
     ⇒            « induction hypothesis four times »
             ↼− −  ⇀                            ∃         − −
                                                          ↼    ⇀                             ∃
             𝐵 1 | 𝐵 1 : R ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> S and 𝐵 2 | 𝐵 2 : R ∧ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> S and
             ↼− −  ⇀                              ∃        ↼−   −
                                                                ⇀                                ∃
             𝐵 3 | 𝐵 3 : R ∧ ¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> S and 𝐵 4 | 𝐵 4 : R ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> S
     ⇒            « rule eRewrite four times using (8) and reflexivity of ≃ »
             ↼− −  ⇀                            ∃         − −
                                                          ↼    ⇀                             ∃
             𝐵 1 | 𝐵 1 : R ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> S and 𝐵 1 | 𝐵 2 : R ∧ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> S and
             ↼− −  ⇀                              ∃        ↼−   −
                                                                ⇀                                ∃
             𝐵 3 | 𝐵 1 : R ∧ ¬ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ≈> S and 𝐵 3 | 𝐵 2 : R ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ≈> S
     ⇒            « rule eIf4 »
                        ↼−        ↼ −                 −
                                                      ⇀      −
                                                             ⇀        ∃
           if 𝑒 then 𝐵 1 else 𝐵 3 | if 𝑒 ′ then 𝐵 1 else 𝐵 2 : R ≈> S
     ⇔            « def ↼   _− and ⇀ −_ »
           ↼−−−−′−−−−−−−−−−−− −−−−−−′−−−−−−−−−−⇀                  ∃
           if 𝑒 |𝑒 𝐵 1 𝐵 2 𝐵 3 𝐵 4 | if 𝑒 |𝑒 𝐵 1 𝐵 2 𝐵 3 𝐵 4 : R ≈> S
17 Here and in the case for if, induction on the structure of 𝐵 would suffice, but not so in the case for loops.
32                                             Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


   case 𝐵 is ⟨𝑐 | 𝑐 ′ ⟩ . Again the argument 𝑣𝑠 to chk is the same throughout and elided, as is that same
argument to uchk. First observe that ⟨𝑐 | uchk(𝑐 ′ )⟩  ⟨𝑐 | skip⟩; ⟨skip | uchk(𝑐 ′ )⟩ by Definition 4.3,
so J ⟨𝑐 | uchk(𝑐 ′ )⟩ K = J ⟨𝑐 | skip⟩; ⟨skip | uchk(𝑐 ′ )⟩ K by Lemma 4.4. Hence by Lemma 4.8(iii) we
have wlp(⟨𝑐 | uchk(𝑐 ′ )⟩, S) = wlp(⟨𝑐 | skip⟩; ⟨skip | uchk(𝑐 ′ )⟩, ). Now we calculate.
                       chk(⟨𝑐 | 𝑐 ′ ⟩) : R { ¥ S
                 ⇔             « def chk, wlp/correctness Lemma 4.8(i) »
                       R ⇒ wlp(⟨𝑐 | uchk(𝑐 ′ )⟩, S)
                 ⇔             « observation above »
                       R ⇒ wlp(⟨𝑐 | skip⟩; ⟨skip | uchk(𝑐 ′ )⟩, S)
                 ⇔             « wlp of seq, abbreviate Q := wlp(⟨skip | uchk(𝑐 ′ )⟩, S) »
                       R ⇒ wlp(⟨𝑐 | skip⟩, Q)
                 ⇔             « wlp properties Lemma 4.8(i) and (ii) »
                       ⟨𝑐 | skip⟩ : R {    ¥ Q and ⟨skip | uchk(𝑐 ′ )⟩ : Q {   ¥ S
                 ⇒             « adequacy of embed: Lemma 4.7 »
                                       ∀
                       𝑐 | skip : R ≈> Q and ⟨skip | uchk(𝑐 ′ )⟩ : Q {     ¥ S
                 ⇒             « Lemma 3.4 »
                                       ∃
                       𝑐 | skip : R ≈> Q and ⟨skip | uchk(𝑐 ′ )⟩ : Q {     ¥ S
                 ⇒             « Lemma 5.3 »
                                       ∃                         ∃
                       𝑐 | skip : R ≈> Q and skip | 𝑐 ′ : Q ≈> S
                 ⇒             « sequence rule eSeq »
                                                  ∃
                       𝑐; skip | skip; 𝑐 ′ : Q ≈> S
                 ⇒             « rule eRewrite using 𝑐; skip ≃ 𝑐 and skip; 𝑐 ′ ≃ 𝑐 ′ »
                                    ∃
                       𝑐 | 𝑐 ′ : Q ≈> S
                 ⇔             « defs ↼ _− and ⇀
                                               −_ »
                       ↼−−−−′− −−−−−⇀    ′      ∃
                       ⟨𝑐 | 𝑐 ⟩ | ⟨𝑐 | 𝑐 ⟩ : Q ≈> S

      case 𝐵 is while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 1 .
     To introduce some nomenclature we expand the definition of chk(𝐵, 𝑣𝑠) as follows.
          chk(while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 1, 𝑣𝑠) = while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵 2
            where 𝐵 2 = 𝐵𝑠𝑛𝑝 ; chk(𝐵 1, 𝑣𝑠); 𝐵𝑑𝑒𝑐
                     𝐵𝑠𝑛𝑝 = havf 𝑥 𝐸 ( [⟩𝑥 𝐸 ]⟩ = 𝐸); havf 𝑥𝑟𝑜 ( [⟩𝑥𝑟𝑜 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ ))
                     𝐵𝑑𝑒𝑐 = assert ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ )
The variables 𝑥 𝐸 and 𝑥𝑟𝑜 are fresh with respect to both 𝑣𝑠 and the assigned variables in chk(𝐵 1 ) (see
Figure 12). The names are mnemonic: in 𝐵𝑠𝑛𝑝 , variable 𝑥 𝐸 snapshots the value of 𝐸 at the start of an
iteration and 𝑥𝑟𝑜 snapshots the condition that it will be a right-only iteration. The assertion 𝐵𝑑𝑒𝑐
checks that on right-only iterations the variant decreases. In the following we elide the argument
𝑣𝑠 to chk as it is the same throughout.
   Let I =ˆ wlp(chk(𝐵), S), so I = wlp(while 𝑒 | 𝑒 ′ algn P | P ′ vnt 𝐸 do 𝐵𝑠𝑛𝑝 ; chk(𝐵 1 ); 𝐵𝑑𝑒𝑐 , S).
Note that wlp(chk(𝐵), S) is different from wlp(𝐵, S) owing to the instrumentation. A key fact is
                                                   𝑣𝑠 ⊩ I                                              (9)
This holds because we have 𝑣𝑠 ⊩ chk(𝐵) by Lemma 5.2 and the assumption bFrame(𝐵, 𝑣𝑠); and we
have assumption 𝑣𝑠 ⊩ S so we can apply Lemma 4.13.
                                                         ↼−          −
                                                                     ⇀
  We aim to instantiate rule eDoX for the commands 𝑐 := 𝐵 and 𝑐 ′ := 𝐵 , invariant I defined above,
                                                     − ⇀
                                                     ↼   −      ∃
variant 𝐸 from 𝐵. This yields the desired conclusion 𝐵 | 𝐵 : R ≈> S for the loop case, provided we
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                      33


can establish the following proof obligations involving the original loop body 𝐵 1 .




       |= R ⇒ I                                                                                   (I0)
          ↼− −  ⇀                                               ∃
       |= 𝐵 1 | 𝐵 1 : I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ≈> I                                      (I1)
          ↼−                                ∃
       |= 𝐵 1 | skip : I ∧ ⟨[𝑒 ⟨] ∧ P ≈> I                                                        (I2)
                               −
                               ⇀                                              ∃
       ∀𝑛 ∈ Z. |= skip | 𝐵 1 : I ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) ∧ (𝑛 = 𝐸) ≈> I ∧ (0 ≤ 𝐸 < 𝑛)   (I3)
       |= I ⇒ (𝑒 =    ¥ 𝑒 ′ ) ∨ ( ⟨[𝑒 ⟨] ∧ 𝑃) ∨ ( [⟩𝑒 ′ ]⟩ ∧ 𝑃 ′ )                                (I4)
       |= I ∧ ¬ 𝑒 ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ S
                   ⟨[ ⟨]                                                                          (I5)




By the wlp equation for bi-while (Lemma 4.10) we have I = gfp(𝐺 (𝑒, 𝑒 ′, P, P ′, 𝐵 2, S)) where 𝐺 is
defined in Lemma 4.10. We do not use that this is a greatest fixpoint, only that it is a postfixpoint, i.e.,
we have |= I ⇒ 𝐺 (𝑒, 𝑒 ′, P, P ′, 𝐵 2, S) (I). Expanding the definition of 𝐺 and applying propositional
equivalences we get the following.




                            |= I ∧ ¬ ⟨[𝑒 ⟨] ∧ ¬ [⟩𝑒 ′ ]⟩ ⇒ S                              (H1)
                                                             ↼↼−
                            |= I ∧ ⟨[𝑒 ⟨] ∧ P ⇒ wlp( 𝐵 2 , I)                             (H2)
                                                                                 −⇀
                                                                                 ⇀
                            |= I ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) ⇒ wlp( 𝐵 2 , I)        (H3)
                            |= I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(𝐵 2, I)            (H4)
                            |= I ⇒ ((𝑒 =𝑒   ¥ ′ ) ∨ ( ⟨[𝑒 ⟨] ∧ P) ∨ ( [⟩𝑒 ′ ]⟩ ∧ P ′ ))   (H5)




                                                      ∀
From our given assumption |= chk(𝐵) : R ≈> S we have |= R ⇒ wlp(chk(𝐵), S) by Lemma 4.8(i);
so (I0) holds by definition of I. By (H5) we have (I4) and by (H1) we have (I5). It remains to show
(I1), (I2), and (I3) which correspond to the three main premises in eDoX. We use (H4), (H2), and (H3)
to prove (I1)–(I3).
34                                             Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


   For (I1), starting from the relevant fact (H4) we calculate, eliding |= and eliding 𝑣𝑠 as an argument
to chk.




                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(𝐵 2, I)
          ⇔            « def 𝐵 2 »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(𝐵𝑠𝑛𝑝 ; chk(𝐵 1 ); 𝐵𝑑𝑒𝑐 , I)
          ⇔            « wlp equation for sequence (Lemma 4.10) »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(𝐵𝑠𝑛𝑝 , wlp(chk(𝐵 1 ), wlp(𝐵𝑑𝑒𝑐 , I)))
          ⇔            « unfold defs, wlp equation for sequence »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(havf 𝑥 𝐸 (𝑥 𝐸 = 𝐸),
                                                          wlp(havf 𝑥𝑟𝑜 (𝑥𝑟𝑜 = ( ⟨[𝑒 ′ ⟨] ∧ P ′ )),
                                                          wlp(chk(𝐵 1 ),
                                                          wlp(assert 𝑥𝑟𝑜 ⇒ 𝐸 < 𝑥 𝐸 , 𝐼 ))))))
          ⇔            « wlp equations for havf and assert (Lemma 4.10) »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ ∀|𝑥 𝐸 . (𝑥 𝐸 = 𝐸 ⇒
                                                          ∀|𝑥𝑟𝑜 . (𝑥𝑟𝑜 = ( ⟨[𝑒 ′ ⟨] ∧ P ′ )) ⇒
                                                          wlp(chk(𝐵 1 ), I ∧ (𝑥𝑟𝑜 ⇒ 𝐸 < 𝑥 𝐸 )))))
          ⇒            « wlp(chk(𝐵 1 ), _) monotonic, in monotonic context »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ ∀|𝑥 𝐸 . (𝑥 𝐸 = 𝐸 ⇒
                                                          ∀|𝑥𝑟𝑜 . (𝑥𝑟𝑜 = ( ⟨[𝑒 ′ ⟨] ∧ P ′ )) ⇒
                                                          wlp(chk(𝐵 1 ), I))))
          ⇔            « predicate calculus (one point rule), eliding ( ⟨[𝑒 ′ ⟨] ∧ P ′ ) »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ ∀|𝑥 𝐸 . (𝑥 𝐸 = 𝐸 ⇒ wlp(chk(𝐵 1 ), I))𝑥...𝑟𝑜
          ⇔            « 𝑥𝑟𝑜 ∉ 𝑣𝑠, Lemma 4.12, (9), Lemmas 5.2 and 4.13 »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ ∀|𝑥 𝐸 . (𝑥 𝐸 = 𝐸 ⇒ wlp(chk(𝐵 1 ), I))
          ⇔            « one point rule, 𝑥 𝐸 ∉ 𝑣𝑠, framing as in preceding two steps »
                I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ⇒ wlp(chk(𝐵 1 ), I)
          ⇔            « wlp/correctness Lemma 4.8(i) »
                chk(𝐵 1 ) : I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ {   ¥ I
          ⇒            « induction hypothesis, noting size(𝐵 1 ) < size(𝐵) »
                ↼− −  ⇀                                        ∃
                𝐵 1 | 𝐵 1 : I ∧ ⟨[𝑒 ⟨] ∧ [⟩𝑒 ′ ]⟩ ∧ ¬P ∧ ¬P ′ ≈> I




So (I1) is proved. To apply the induction hypothesis in the last step, we need the pre- and post-
relations to be framed by 𝑣𝑠. For I this is just (9). For the precondition we also use that 𝑒, 𝑒 ′, P, P ′
are framed by 𝑣𝑠 which follows by def from bFrame(𝐵).
   Next we prove (I2), starting from the relevant fact (H2) and eliding 𝑣𝑠 as argument to chk.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                  35




                                    ↼↼−
         I ∧ ⟨[𝑒 ⟨] ∧ P ⇒ wlp( 𝐵 2 , I)
   ⇔                                       _− »
                « defs 𝐵 2 , 𝐵𝑠𝑛𝑝 , 𝐵𝑑𝑒𝑐 , ↼
                                           ↼
                                    ↼↼−−−−−−−−−−−−−−−− ↼ ↼−−−−−−−−− ↼    ↼−−−−− ↼   ↼−−−−−−−−−−−−−−−−−
         I ∧ ⟨[𝑒 ⟨] ∧ P ⇒ wlp( havf 𝑥 𝐸 ( [⟩𝑥 𝐸 ]⟩ = 𝐸); havf 𝑥𝑟𝑜 . . .; chk(𝐵 1 ); assert ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ . . .), I)
   ⇔            « def ↼ _−, abbreviate 𝐸𝑆𝑆 := ⟨skip | skip⟩ »
                        ↼
                                              ↼↼−−−−−
         I ∧ 𝑒 ∧ P ⇒ wlp(𝐸𝑆𝑆; 𝐸𝑆𝑆; chk(𝐵 1 ); 𝐸𝑆𝑆, I)
               ⟨[  ⟨]
   ⇔            « wlp equation for sequence, wlp(𝐸𝑆𝑆, .) is identity function »
                                    ↼↼−−−−−
         I ∧ ⟨[𝑒 ⟨] ∧ P ⇒ wlp( chk(𝐵 1 ), I)
   ⇔            « wlp/correctness Lemma 4.8(i) »
         ↼−−−−−
         ↼
         chk(𝐵 1 ) : I ∧ ⟨[𝑒 ⟨] ∧ P {  ¥ I
                                           ↼−−−−−
                                           ↼                ↼−
                                                            ↼
   ⇔            « Lemma 4.6, using J chk(𝐵 1 ) K = J chk( 𝐵 1 ) K from Lemmas 5.1 and 4.4 »
                ↼−
                ↼
         chk( 𝐵 1 ) : I ∧ ⟨[𝑒 ⟨] ∧ P {   ¥ I
                                                                      ↼−
                                                                      ↼
   ⇒            « induction hypothesis, using fact (9) and size( 𝐵 1 ) ≤ size(𝐵 1 ) < size(𝐵) »
         ↼−−
         ↼− ↼
         ↼      − −
                  ⇀
                 ↼−                    ∃
         𝐵 1 | 𝐵 1 : I ∧ ⟨[𝑒 ⟨] ∧ P ≈> I
                    ↼
                    ↼ −
                      −
                     ↼− ↼  −        −
                                    −⇀
                                    ↼−
                                    ↼
   ⇔            « 𝐵 1 = 𝐵 1 and 𝐵 1 = skip by (4) »
         ↼−                            ∃
         𝐵 1 | skip : I ∧ ⟨[𝑒 ⟨] ∧ P ≈> I




So (I2) is proved.
36                                               Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


   Finally we prove (I3). We use the fact that for any 𝑥 and Q, |= ∀|𝑥 . Q iff |= Q. We start from the
relevant property (H3).
                                                          −⇀
                                                          ⇀
         I ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) ⇒ wlp( 𝐵 2 , I)
     ⇔         « defs 𝐵 2 , 𝐵𝑠𝑛𝑝 , 𝐵𝑑𝑒𝑐 , ⇀−⇀_ ; wlp over seq; abbrev. 𝑋 𝑅𝑂 := [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) »
         I ∧ 𝑋 𝑅𝑂 ⇒ wlp(havf 𝑥 𝐸 ( [⟩𝑥 𝐸 ]⟩ = 𝐸), wlp(havf 𝑥𝑟𝑜 ( [⟩𝑥𝑟𝑜 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ )),
                                 −−−−−−⇀ ⇀
                            wlp( chk(𝐵 1 ), wlp(assert ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ), I))))
     ⇔         « wlp equations for assert and havf »
         I ∧ 𝑋 𝑅𝑂 ⇒ ∀|𝑥 𝐸 . ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ ∀|𝑥𝑟𝑜 . ( [⟩𝑥𝑟𝑜 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ )) ⇒
                                 −−−−−−⇀ ⇀
                            wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « predicate calculus, 𝑥 𝐸 and 𝑥𝑟𝑜 outside frames of I and 𝑋 𝑅𝑂 »
          ∀|𝑥 𝐸 . ∀|𝑥𝑟𝑜 . I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ∧ ( [⟩𝑥𝑟𝑜 ]⟩ = ( [⟩𝑒 ′ ]⟩ ∧ P ′ )) ⇒
                −−−−−−⇀  ⇀
          wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « |= 𝑋 𝑅𝑂 ⇒ ( [⟩𝑒 ′ ]⟩ ∧ P ′ ), and if |= 𝑋 ⇒ 𝑍 then |= 𝑋 ∧ (𝑦 = 𝑍 ) ⇔ 𝑋 ∧ (𝑦 = tt) »
          ∀|𝑥 𝐸 . ∀|𝑥𝑟𝑜 . I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ∧ ( [⟩𝑥𝑟𝑜 ]⟩ = tt) ⇒
                −−−−−−⇀  ⇀
          wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « fact about |= and ∀ mentioned at the start (noting |= is elided here) »
          ∀|𝑥𝑟𝑜 . I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ∧ ( [⟩𝑥𝑟𝑜 ]⟩ = tt) ⇒
                −−−−−−⇀  ⇀
          wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « predicate calculus, 𝑥𝑟𝑜 outside frames of I, 𝑋 𝑅𝑂, and [⟩𝑥 𝐸 ]⟩ = 𝐸 »
          I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ ∀|𝑥𝑟𝑜 . ( [⟩𝑥𝑟𝑜 ]⟩ = tt) ⇒
                −−−−−−⇀  ⇀
          wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « predicate calculus (one point rule) »
                                                   −−−−−−⇀ ⇀                                     |𝑥𝑟𝑜
         I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ (wlp( chk(𝐵 1 ), ( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)) |tt
     ⇒         « Lemma 4.15 using that 𝑥𝑟𝑜 is outside frame of chk(𝐵 1 ) »
                                                  −−−−−−⇀ ⇀
         I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ wlp( chk(𝐵 1 ), (( [⟩𝑥𝑟𝑜 ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I) |𝑥 |tt
                                                                                                  𝑟𝑜
                                                                                                     )
     ⇔         « subst over conj, Lemma 4.12 for I, 𝐸; 𝑥𝑟𝑜 fresh »
                                                  −−−−−−⇀ ⇀
         I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ wlp( chk(𝐵 1 ), ( [⟩ tt ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)
     ⇔         « Lemma 4.17 for 𝑛 ∈ Z, eliding |= »
                                                         −−−−−−⇀
                                                               ⇀                                     |𝑥 𝐸
         ∀𝑛. (I ∧ 𝑋 𝑅𝑂 ∧ ( [⟩𝑥 𝐸 ]⟩ = 𝐸) ⇒ wlp( chk(𝐵 1 ), ( [⟩ tt ]⟩ ⇒ 0 ≤ 𝐸 < [⟩𝑥 𝐸 ]⟩ ) ∧ I)) |𝑛
     ⇔         « framing: 𝑥 𝐸 fresh for all except [⟩𝑒𝐸 ]⟩ , Lemmas 4.12 4.13 , ⟨[𝑥 𝐸 ⟨]𝑛|𝑥𝐸 = 𝑛 »
                                                    −−−−−−⇀⇀
         ∀𝑛. (I ∧ 𝑋 𝑅𝑂 ∧ (𝑛 = 𝐸) ⇒ wlp( chk(𝐵 1 ), ( [⟩ tt ]⟩ ⇒ 0 ≤ 𝐸 < 𝑛) ∧ I))
     ⇔         « wlp/correctness Lemma 4.8(i), simplify [⟩ tt ]⟩ ⇒ . . . »
             −−−−−−⇀   ⇀
         ∀𝑛. chk(𝐵 1 ) : I ∧ 𝑋 𝑅𝑂 ∧ (𝑛 = 𝐸) {           ¥ 0≤𝐸 <𝑛∧I
     ⇔         « Lemma 5.1 »
                     ⇀−⇀
         ∀𝑛. chk( 𝐵 1 ) : I ∧ 𝑋 𝑅𝑂 ∧ (𝑛 = 𝐸) {          ¥ 0≤𝐸 <𝑛∧I
     ⇒         « induction hypothesis, note below »
             ↼
             −⇀
             ⇀ − ⇀   −
                     −⇀
                      ⇀                               ∃
         ∀𝑛. 𝐵 1 | 𝐵 1 : I ∧ 𝑋 𝑅𝑂 ∧ (𝑛 = 𝐸) ≈> 0 ≤ 𝐸 < 𝑛 ∧ I
                                            ↼
                                            −⇀
                                            ⇀ −               −
                                                              −⇀
                                                              ⇀⇀ − ⇀
     ⇒         « rule eRewrite using 𝐵 1 ≃ skip and 𝐵 1 = 𝐵 1 from (4), and ≃ reflexive »
             ↼− −   ⇀                                                        ∃
         ∀𝑛. 𝐵 1 | 𝐵 1 : I ∧ [⟩𝑒 ′ ]⟩ ∧ P ′ ∧ ¬( ⟨[𝑒 ⟨] ∧ P) ∧ (𝑛 = 𝐸) ≈> 0 ≤ 𝐸 < 𝑛 ∧ I

   So (I3) is proved, which completes the proof of the Theorem. Note: the step using induction
                          −⇀
                          ⇀
hypothesis relies on size( 𝐵 1 ) ≤ size(𝐵 1 ) < size(𝐵). Also the pre- and post-relations are semantically
framed by 𝑣𝑠: for I this is (9); for P, P ′, 𝐸 this is from bFrame(𝐵).                                  □
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                      37


References
 [1] Carmine Abate, Roberto Blanco, Ştefan Ciobâcă, Adrien Durier, Deepak Garg, Catalin Hritcu, Marco Patrignani,
     Éric Tanter, and Jérémy Thibault. 2021. An Extended Account of Trace-relating Compiler Correctness and Secure
     Compilation. ACM Trans. Program. Lang. Syst. 43, 4 (2021), 14:1–14:48. https://doi.org/10.1145/3460860
 [2] Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo.
     2023. An Algebra of Alignment for Relational Verification. Proc. ACM Program. Lang. 7, POPL, Article 20 (2023),
     30 pages. https://doi.org/10.1145/3571213 Full version at https://arxiv.org/abs/2202.04278.
 [3] Krzysztof R. Apt, Frank S. de Boer, and Ernst-Rüdiger Olderog. 2009. Verification of Sequential and Concurrent Programs
     (3 ed.). Springer. https://doi.org/10.1007/978-1-84882-745-5
 [4] Flavio Ascari, Roberto Bruni, Roberta Gori, and Francesco Logozzo. 2024. Sufficient Incorrectness Logic: SIL and
     Separation SIL. arXiv:2310.18156 [cs.LO]
 [5] Martin Avanzini, Gilles Barthe, Davide Davoli, and Benjamin Grégoire. 2025. A Quantitative Probabilistic Relational
     Hoare Logic. Proc. ACM Program. Lang. 9, POPL (2025). https://doi.org/10.1145/3704876
 [6] Anindya Banerjee, Ramana Nagasamudram, David A. Naumann, and Mohammad Nikouei. 2022. A Relational Program
     Logic with Data Abstraction and Dynamic Framing. ACM Transactions on Programming Languages and Systems 44, 4
     (2022), 25:1–25:136. https://doi.org/10.1145/3551497
 [7] Anindya Banerjee, David A. Naumann, and Mohammad Nikouei. 2016. Relational Logic with Framing and Hypotheses.
     In Foundations of Software Tech. and Theoretical Comp. Sci. 11:1–11:16. Technical report at http://arxiv.org/abs/1611.
     08992.
 [8] Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2016. Product Programs and Relational Program Logics. J. Logical
     and Algebraic Methods in Programming 85, 5 (2016), 847–859.
 [9] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2011. Secure information flow by self-composition. Math. Struct.
     Comput. Sci. 21, 6 (2011), 1207–1252. https://doi.org/10.1017/S0960129511000193
[10] Gilles Barthe, Renate Eilers, Pamina Georgiou, Bernhard Gleiss, Laura Kovács, and Matteo Maffei. 2019. Verifying
     Relational Properties using Trace Logic. In Formal Methods in Computer Aided Design (FMCAD). https://doi.org/10.
     23919/FMCAD.2019.8894277
[11] Gilles Barthe, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2017. Coupling proofs are probabilistic product
     programs. In ACM Symposium on Principles of Programming Languages. 161–174. https://doi.org/10.1145/3009837.
     3009896
[12] Gilles Barthe and Tamara Rezk. 2005. Non-interference for a JVM-like language. In Proceedings of TLDI’05.
[13] N. Benton. 2004. Simple Relational Correctness Proofs for Static Analyses and Program Transformations. In ACM
     Symposium on Principles of Programming Languages. ACM, 14–25. https://doi.org/10.1145/964001.964003
[14] Lennart Beringer. 2011. Relational Decomposition. In Interactive Theorem Proving (LNCS), Vol. 6898. 39–54. https:
     //doi.org/10.1007/978-3-642-22863-6_6
[15] Raven Beutner. 2024. Automated Software Verification of Hyperliveness. In Tools and Algorithms for the Construction and
     Analysis of Systems (LNCS), Bernd Finkbeiner and Laura Kovács (Eds.), Vol. 14571. 196–216. https://doi.org/10.1007/978-
     3-031-57249-4_10
[16] Raven Beutner and Bernd Finkbeiner. 2022. Software Verification of Hyperproperties Beyond k-Safety. In Computer
     Aided Verification (LNCS), Sharon Shoham and Yakir Vizel (Eds.), Vol. 13371. 341–362. https://doi.org/10.1007/978-3-
     031-13185-1_17
[17] Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and Andrew W Appel. 2018. VST-Floyd: A separation
     logic tool to verify correctness of C programs. Journal of Automated Reasoning 61, 1 (2018), 367–422. https:
     //doi.org/10.1007/s10817-018-9457-5
[18] Berkeley R. Churchill, Oded Padon, Rahul Sharma, and Alex Aiken. 2019. Semantic program alignment for equivalence
     checking. In ACM Conf. on Program. Lang. Design and Implementation. 1027–1040. https://doi.org/10.1145/3314221.
     3314596
[19] Joshua M. Cohen and Philip Johnson-Freyd. 2024. A Formalization of Core Why3 in Coq. Proc. ACM Program. Lang. 8,
     POPL, Article 60 (Jan. 2024), 30 pages. https://doi.org/10.1145/3632902
[20] Arthur Correnson, Tobias Nießen, Bernd Finkbeiner, and Georg Weissenbacher. 2024. Finding ∀∃ Hyperbugs using
     Symbolic Execution. Proc. ACM Program. Lang. 8, OOPSLA2 (2024), 1420–1445. https://doi.org/10.1145/3689761
[21] Thibault Dardinier, Anqi Li, and Peter Müller. 2024. Hypra: A Deductive Program Verifier for Hyper Hoare Logic.
     Proc. ACM Program. Lang. 8, OOPSLA2 (2024), 1279–1308. https://doi.org/10.1145/3689756
[22] Thibault Dardinier and Peter Müller. 2024. Hyper Hoare Logic: (Dis-)Proving Program Hyperproperties. Proc. ACM
     Program. Lang. 8, PLDI (2024), 1485–1509. https://doi.org/10.1145/3656437
[23] Thibault Dardinier, Michael Sammler, Gaurav Parthasarathy, Alexander J. Summers, and Peter Müller. 2025. Formal
     Foundations for Translational Separation Logic Verifiers. Proc. ACM Program. Lang. 9, POPL, Article 20 (2025).
     https://doi.org/10.1145/3704856
38                                                  Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann


[24] Robert Dickerson, Prasita Mukherjee, and Benjamin Delaware. 2025. KestRel: Relational Verification using E-Graphs
     for Program Alignment. Proc. ACM Program. Lang. 9, OOPSLA1 (2025), 1073–1100. https://doi.org/10.1145/3720474
[25] Robert Dickerson, Qianchuan Ye, Michael K. Zhang, and Benjamin Delaware. 2022. RHLE: Modular Deductive
     Verification of Relational ∀ ∃ Properties. In Asian Symposium on Programming Languages and Systems (LNCS),
     Vol. 13658. 67–87. https://doi.org/10.1007/978-3-031-21037-2_4
[26] Edsger W. Dijkstra. 1976. A Discipline of Programming. Prentice-Hall.
[27] Edsger W. Dijkstra and Carel S. Scholten. 1990. Predicate Calculus and Program Semantics. Springer. https://doi.org/
     10.1007/978-1-4612-3228-5
[28] Emanuele D’Osualdo, Azadeh Farzan, and Derek Dreyer. 2022. Proving Hypersafety Compositionally. Proc. ACM
     Program. Lang. 6, OOPSLA2, Article 135 (2022), 26 pages. https://doi.org/10.1145/3563298
[29] Marco Eilers, Thibault Dardinier, and Peter Müller. 2023. CommCSL: Proving Information Flow Security for Concurrent
     Programs using Abstract Commutativity. Proc. ACM Program. Lang. 7, PLDI (2023). https://doi.org/10.1145/3591289
[30] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 — Where Programs Meet Provers. In Programming
     Languages and Systems.
[31] Robert Floyd. 1967. Assigning Meaning to Programs. In Symp. on Applied Math. 19, Math. Aspects of Comp. Sci. Amer.
     Math. Soc., 19–32.
[32] Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2018. ReLoC: A Mechanised Relational Logic for Fine-Grained
     Concurrency. In IEEE Symp. on Logic in Computer Science. 442–451. https://doi.org/10.1145/3209108.3209174
[33] Lennard Gäher, Michael Sammler, Simon Spies, Ralf Jung, Hoang-Hai Dang, Robbert Krebbers, Jeehoon Kang, and
     Derek Dreyer. 2022. Simuliris: a separation logic framework for verifying concurrent program optimizations. Proc.
     ACM Program. Lang. 6, POPL (2022). https://doi.org/10.1145/3498689
[34] Vladimir Gladshtein, Qiyuan Zhao, Willow Ahrens, Saman P. Amarasinghe, and Ilya Sergey. 2024. Mechanised
     Hypersafety Proofs about Structured Data. Proc. ACM Program. Lang. 8, PLDI (2024), 647–670. https://doi.org/10.
     1145/3656403
[35] Leandro Gomes, Patrick Baillot, and Marco Gaboardi. 2025. BiGKAT: An Algebraic Framework for Relational
     Verification of Probabilistic Programs. In Foundations of Software Science and Computation Structures, Parosh Aziz
     Abdulla and Delia Kesner (Eds.). https://doi.org/10.1007/978-3-031-90897-2_12
[36] Michael Greenberg, Ryan Beckett, and Eric Hayden Campbell. 2022. Kleene algebra modulo theories: a framework for
     concrete KATs. In ACM Conf. on Program. Lang. Design and Implementation. https://doi.org/10.1145/3519939.3523722
[37] Simon Oddershede Gregersen, Alejandro Aguirre, Philipp G. Haselwarter, Joseph Tassarotti, and Lars Birkedal. 2024.
     Asynchronous Probabilistic Couplings in Higher-Order Separation Logic. Proc. ACM Program. Lang. 8, POPL (2024).
     https://doi.org/10.1145/3632868
[38] Arie Gurfinkel. 2022. Program Verification with Constrained Horn Clauses (Invited Paper). In Computer Aided
     Verification, Sharon Shoham and Yakir Vizel (Eds.). https://doi.org/10.1007/978-3-031-13185-1_2
[39] Chris Hawblitzel, Ming Kawaguchi, Shuvendu K. Lahiri, and Henrique Rebêlo. 2013. Towards Modularly Comparing
     Programs Using Automated Theorem Provers. In CADE (LNCS), Vol. 7898. 282–299. https://doi.org/10.1007/978-3-
     642-38574-2_20
[40] C. A. R. Hoare. 1978. Some Properties of Predicate Transformers. J. ACM 25 (1978), 461–480.
[41] Shachar Itzhaky, Sharon Shoham, and Yakir Vizel. 2024. Hyperproperty Verification as CHC Satisfiability. In Pro-
     gramming Languages and Systems, European Symposium on Programming (LNCS), Vol. 14577. 212–241. https:
     //doi.org/10.1007/978-3-031-57267-8_9
[42] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from
     the ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
     https://doi.org/10.1017/S0956796818000151
[43] Dexter Kozen. 1997. Kleene algebra with tests. ACM Transactions on Programming Languages and Systems 19, 3 (1997),
     427–443. https://doi.org/10.1145/256167.256195
[44] Dexter Kozen and Frederick Smith. 1996. Kleene algebra with tests: Completeness and decidability. In International
     Workshop on Computer Science Logic (LNCS), Vol. 1258. 244–259. https://doi.org/10.1007/3-540-63172-0_43
[45] Leslie Lamport and Fred B. Schneider. 2021. Verifying Hyperproperties With TLA. In IEEE Computer Security
     Foundations. 1–16. https://doi.org/10.1109/CSF51468.2021.00012
[46] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional Correctness. In Logic for Programming,
     Artificial Intelligence, and Reasoning, Edmund M. Clarke and Andrei Voronkov (Eds.). https://doi.org/10.1007/978-3-
     642-17511-4_20
[47] Kenji Maillard, Catalin Hritcu, Exequiel Rivas, and Antoine Van Muylder. 2020. The next 700 relational program logics.
     Proc. ACM Program. Lang. 4, POPL (2020). https://doi.org/10.1145/3371072
[48] Konstantinos Mamouras. 2017. Equational Theories of Abnormal Termination Based on Kleene Algebra. In FoSSaCS.
     88–105.
Forall-Exists Relational Verification by Filtering to Forall-Forall [with appendix]                                         39


[49] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Viper: A Verification Infrastructure for Permission-
     Based Reasoning. In Int’l Conf. on Verification, Model Checking, and Abstract Interpretation. https://doi.org/10.1007/978-
     3-662-49122-5_2
[50] R. Nagasamudram, A. Banerjee, and D.A. Naumann. 2025. WhyRel: an auto-active relational verifier. International
     Journal on Software Tools for Technology Transfer (2025). https://doi.org/10.1007/s10009-025-00786-1
[51] Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann. 2023. Alignment complete relational Hoare
     logics for some and all. CoRR abs/2307.10045v5 (2023). https://doi.org/10.48550/arXiv.2307.10045 Version v5, with
     discussion of entailment completeness.
[52] Ramana Nagasamudram, Anindya Banerjee, and David A. Naumann. 2025. Alignment complete relational Hoare
     logics for some and all. CoRR abs/2307.10045 (2025). https://doi.org/10.48550/arXiv.2307.10045
[53] Hanne Riis Nielson and Flemming Nielson. 1992. Semantics with Applications - a Formal Introduction. Wiley, New
     York.
[54] Benjamin C. Pierce, Arthur Azevedo de Amorim, Chris Casinghino, Marco Gaboardi, Michael Greenberg, Cătălin
     Hriţcu, Vilhelm Sjöberg, Andrew Tolmach, and Brent Yorgey. 2024. Programming Language Foundations. Software
     Foundations, Vol. 2. Version 6.7, http://softwarefoundations.cis.upenn.edu.
[55] Ron Shemer, Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. 2019. Property Directed Self Composition. In Computer
     Aided Verification (LNCS), Vol. 11561. 161–179. https://doi.org/10.1007/978-3-030-25540-4_9
[56] Marcelo Sousa and Isil Dillig. 2016. Cartesian Hoare logic for verifying k-safety properties. In ACM Conf. on Program.
     Lang. Design and Implementation. 57–69. https://doi.org/10.1145/2908080.2908092
[57] Ofer Strichman and Maor Veitsman. 2016. Regression Verification for Unbalanced Recursive Functions. In FM 2016:
     Formal Methods. 645–658.
[58] Aaron Turon, Derek Dreyer, and Lars Birkedal. 2013. Unifying refinement and Hoare-style reasoning in a logic for
     higher-order concurrency. In ACM SIGPLAN International Conference on Functional Programming. https://doi.org/10.
     1145/2500365.2500600
[59] Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. 2021. Constraint-Based Relational Verification. In Computer Aided
     Verification (LNCS), Vol. 12759. 742–766. https://doi.org/10.1007/978-3-030-81685-8_35
[60] Zhongye Wang, Qinxiang Cao, and Yichen Tao. 2024. Verifying Programs with Logic and Extended Proof Rules: Deep
     Embedding vs. Shallow Embedding. J. Autom. Reason. 68, 3 (2024), 18. https://doi.org/10.1007/S10817-024-09706-5
[61] Shushu Wu, Xiwei Wu, and Qinxiang Cao. 2025. Encode the ∀∃ Relational Hoare Logic into Standard Hoare Logic.
     arXiv:2504.17444 [cs.PL] https://arxiv.org/abs/2504.17444
[62] Linpeng Zhang, Noam Zilberstein, Benjamin Lucien Kaminski, and Alexandra Silva. 2024. Quantitative Weakest
     Hyper Pre: Unifying Correctness and Incorrectness Hyperproperties via Predicate Transformers. Proc. ACM Program.
     Lang. 8, OOPSLA2 (2024), 817–845. https://doi.org/10.1145/3689740
[63] Noam Zilberstein, Derek Dreyer, and Alexandra Silva. 2023. Outcome Logic: A Unifying Foundation for Correctness
     and Incorrectness Reasoning. Proc. ACM Program. Lang. 7, OOPSLA1 (2023). https://doi.org/10.1145/3586045
[64] Noam Zilberstein, Dexter Kozen, Alexandra Silva, and Joseph Tassarotti. 2025. A Demonic Outcome Logic for
     Randomized Nondeterminism. Proc. ACM Program. Lang. 9, POPL (2025), 539–568. https://doi.org/10.1145/3704855
