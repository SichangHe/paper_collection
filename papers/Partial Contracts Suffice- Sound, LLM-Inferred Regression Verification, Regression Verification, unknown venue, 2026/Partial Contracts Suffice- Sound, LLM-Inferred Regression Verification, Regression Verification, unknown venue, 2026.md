                                               Partial Contracts Suffice: Sound, LLM-Inferred
                                                           Regression Verification
                                             Yiannis Charalambous                   Rafael Menezes                     Youcheng Sun                   Lucas C. Cordeiro
                                         The University of Manchester The University of Manchester The University of Manchester The University of Manchester
                                             0009-0000-5755-5099          0000-0002-6102-4343          0000-0002-1893-6259          0000-0002-6235-4272



                                            Abstract—Software evolves continuously, yet ensuring that a          bounded check stays expensive, since it has to reason about
                                         patch preserves intended behavior without re-verifying an entire        each function together with all its side-effects [3].
                                         codebase remains difficult. Regression verification addresses this         In a bug-fixing or refactoring context, full equivalence asks
                                         problem, but existing techniques either require expensive whole-
                                         program reasoning or rely on manually written specifications            too much: the developer means to change some paths and
                                         that are rarely available in practice. In this work, we present the     leave the rest, so requiring agreement everywhere, old bugs
                                         first contract-based regression verification tool. In our approach,     and all, rejects the very edit being made. The useful notions
                                         the contract soundness is ensured by proving that all function          form a spectrum, ordered by how much of each execution
                                         versions match the behavior. Additionally, to ensure the behavior,      they compare, and the weaker the relation the cheaper the
                                         the contract is used to verify the program flow (i.e., assume-
                                         guarantee). We ask whether a partial, caller-sufficient contract,       proof. Full equivalence is the strongest: the two versions must
arXiv:2607.10291v1 [cs.SE] 11 Jul 2026




                                         rather than a full behavioral specification, is enough. On Frama-       terminate on the same inputs and return the same outputs ev-
                                         C-Problems we strengthen each inferred contract past what               erywhere, preserved bugs included. Partial equivalence relaxes
                                         the caller needs and measure how much tighter it becomes.               termination, asking the versions to agree only on the inputs
                                         It barely moves: for most targets in every model the caller-            where the old one terminates. Conditional, or regression,
                                         sufficient contract is already the tightest the loop reaches, and our
                                         tightness comparator rates the partial and strengthened contracts       equivalence relaxes further still: it fixes a property marking the
                                         equivalent for the large majority of targets it can compare (18         behavior worth preserving and asks for agreement only where
                                         of 20, 13 of 15, and 14 of 18 across the three models). Partial-        the old version already satisfied it. Where the old version
                                         spec contracts thus capture nearly all the attainable tightness, so     violated the property, the new one is free to differ, and that
                                         stopping at caller-sufficiency costs almost nothing. The regression     freedom is exactly where a bug fix lives. We make the three
                                         check underneath is sound: on the third-party EqBench-C suite
                                         it never fabricates an equivalence, returning zero false proofs on      notions precise in Definition 2.
                                         the pairs it decides and reporting an unprovable difference rather         Whichever notion one targets, a whole-program check re-
                                         than a false proof. Used as a soundness oracle this way, it also sur-   analyzes every callee in full at each call site, which does not
                                         faced nine pairs that EqBench mislabels as equivalent, more than        scale as a codebase grows. A scalable proof has to be modular:
                                         a concurrent tool reports. The contracts themselves are inferred        each call is discharged against an abstraction α of the callee
                                         automatically from the checker’s own counterexamples, with no
                                         separate specification step; on Frama-C-Problems and the ANSSI          rather than its body, so the callee is analyzed once instead of
                                         X509 parser this reaches a verification rate comparable to the          at every use. For the proof to stay trustworthy that abstraction
                                         weakest-precondition (WP) tools AutoSpec and Preguss, while a           must be sound: it has to over-approximate the callee, admitting
                                         passing result certifies at least as strong a property, which we call   every behavior the function can exhibit, so the check can never
                                         safety-preserving conditional equivalence: enforcement plus caller-     miss a real difference.
                                         sufficiency, with runtime-error freedom covered by the safety
                                         encoding.                                                                  We take that abstraction to be a function contract: a
                                            Index Terms—formal verification, software testing, artificial        precondition and a postcondition that pin down just part of
                                         intelligence, software safety, large language models                    the callee’s behavior (Definition 3). A verifier enforces the
                                                                                                                 contract against the old version, certifying it as a sound over-
                                                                I. I NTRODUCTION                                 approximation, and then replaces each call by it, so one
                                            Software changes constantly, and most changes are meant              enforced contract serves every call site without re-entering
                                         to be conservative: a refactor, a bug fix, or a small feature           the body. The contract need only be precise on the slice
                                         should preserve the behavior callers already rely on. They              of the output the property observes; off that slice it may
                                         don’t always manage it. A fix that corrects one execution path          stay weak, and looseness there costs completeness, never
                                         can quietly perturb an output some other caller reads, and if           soundness. Anchoring it to the old version’s safe behavior
                                         no test exercises that caller the regression ships unnoticed;           also folds safety in, so a newly introduced memory leak or
                                         across major operating systems, between 14.8% and 24.4% of              out-of-bounds access counts as a regression even when every
                                         post-release fixes were themselves found to be incorrect [1].           returned value is unchanged.
                                         Catching it means deciding whether the new and old versions                Contracts like this are almost never written by hand:
                                         still agree, and there’s no general procedure for that: deciding        even safety-critical code rarely carries machine-checkable per-
                                         full input/output equivalence is undecidable [2], and even a            function specifications, and what exists tends to be system-
                      Caller (unchanged in both versions)                           •  C2 (System). An end-to-end pipeline of three tools:
1 int usable_width(const box_t *b) {
2   box_t o;                                                                           C ONTRACTOR itself scaffolds the regression har-
3   shrink(b, &o);                                                                     nesses, SCRIBE runs the LLM-based propose-and-certify
4   return o.w;          // reads w, never h
5 }                                                                                    contract-inference loop, and REGVER discharges the
               shrink (OLD)                          shrink (NEW)                      regression-equivalence checking against the enforced
1 void shrink(const box_t *b,             void shrink(const box_t *b,                  contracts (§IV); to our knowledge the first to com-
2             box_t *o) {                             box_t *o) {
3   o->w = b->w - 2;                        o->w = b->w - 2;
                                                                                       bine LLM-based contract inference with regression-
4   o->h = b->h;                            o->h = b->h - 2;                           equivalence verification.
5 }                                       }
                                                                                     • C3 (Relative contract-tightness comparator). JUDGE ,
           Inferred contract C on shrink (enforced against OLD)
    requires \valid(b) && \valid(o);                                                   a semantic comparator that decides admit-set inclusion
    assigns o->w, o->h;                                                                in both directions between two contracts and returns a
    ensures o->w == b->w - 2;      // nothing about o->h
                                                                                       four-way verdict (equivalent, one strictly tighter, or in-
    Fig. 1. A property-relative regression check. The fix corrects o->h; the           comparable) with counterexample witnesses; on enforced
    caller usable_width reads only o->w, so it cannot observe the change.              contracts this yields a refinement ordering, so we can
    The partial contract C pins o->w and stays silent on o->h: it is enforced
    against the old shrink ([[shrink1 ]] ⊆ [[C]]) and then replaces it in the
                                                                                       measure how tight an inferred contract is rather than only
    regression check while the new shrink runs concretely, so the two agree on         whether it verifies (§IV-D, Theorem T2).
    o->w. Comparing the whole of *o instead would flag the fix as a difference.
                                                                                     We evaluate C1, C2, and C3 through two questions, stated
                                                                                  and answered in §V: which counterexample modality best
                                                                                  drives frame-condition inference (feedback modality); and
    level [4]–[6]. We therefore infer them with a large language
                                                                                  whether targeting a partial, property-relative contract rather
    model, which has recently begun to automate contract author-
                                                                                  than a full specification makes inference more tractable, and
    ing, though so far only for a single version of a program [4]–
                                                                                  where its returns plateau (tractability).
    [6]. The model is never trusted: it proposes a contract, the
    verifier enforces it against the old version, and only an                        The remainder of the paper is organized as follows. §II sets
    enforced contract is used, so a wrong guess is rejected rather                out the relational semantics, the three equivalence notions, and
    than believed. This is the paper’s thesis: a partial, LLM-                    function contracts with the frame rule; §III surveys related
    inferred, verifier-certified contract suffices to check regression-           work; §IV presents the soundness theorem (Theorem T1) and
    equivalence of C, a language of large, long-lived systems                     its depth-bounded lift, the system, and the contract-tightness
    where a routine change can silently regress a caller.                         procedure (Theorem T2); §V reports the experimental evalu-
                                                                                  ation and analysis, including threats to validity (§V-G); and
       Beyond staying safe, a change is a regression only if
                                                                                  §VI concludes with open directions for future work.
    something that uses the function can tell. Figure 1 shows
    the kind of edit we target. shrink trims a box by a fixed                                           II. P RELIMINARIES
    margin; the old version forgets to shrink the height, and the
    new one fixes it. The caller usable_width reads only the                      A. Program semantics
    width, so it returns the same value before and after the fix.                 Definition 1 (Program semantics). We model each version
    Asking whether the two shrink versions are equivalent is the                  of a function as a relation [[f ]] ⊆ X × Y from input pre-
    wrong question: the height really does change, so a check over                states X to output post-states Y , where (x, o) ∈ [[f ]] means
    the whole of *o reports a difference, flagging the fix itself.                some terminating run of f on x yields o. The pre-state X
    What matters is whether shrink regresses on the width,                        subsumes the responses of any external nondeterministic callee
    the only part usable_width observes, and the contract C                       the two versions share, so a single x resolves those responses
    in the figure captures exactly that. Enforced against the old                 identically on both sides; only nondeterminism internal to the
    shrink, C pins the width (ensures o->w == b->w -                              function itself leaves [[f ]](x) multi-valued. We write [[f ]](x) ≜
    2) and leaves the height free. The regression check replaces                  {o | (x, o) ∈ [[f ]]} for the set of outputs on x, which is empty
    the old shrink by C and runs the new shrink concretely,                       when f does not terminate on x.
    comparing only the width: because C is precise exactly where
    the caller looks and silent elsewhere, the two agree and the                     The spaces X and Y range over a common store, so a pre-
    height change is invisible. A full specification would have                   state and a post-state can be compared; this is what lets the
    to pin the height too, the one part the fix changed and no                    frame clause below speak of the locations a function leaves
    caller reads, making the proof obligation much harder for the                 unchanged.
    contract author.
                                                                                  B. Equivalence notions
       We make three contributions:
                                                                                    Fix an old version f1 and a new version f2 . The three
      •   C1 (Soundness). A verifier-independent theorem that
                                                                                  notions stated informally in §I order by how much of each
          proves abstracting only the old version by a single par-
                                                                                  execution they compare [3], [7].
          tial, one-sided contract suffices to prove property-relative
          regression-equivalence, together with a depth-bounded                   Definition 2 (Equivalence notions).       • Full   equivalence:
          lift for nested calls (§IV, Theorem T1).                                     [[f1 ]] = [[f2 ]], so the versions terminate on the same
    inputs and produce the same outputs everywhere, old                 verifier must havoc every reachable location, and the abstrac-
    bugs included.                                                      tion becomes too coarse to support a non-trivial equivalence
  • Partial equivalence relaxes termination: [[f1 ]](x) ̸= ∅ ⇒          proof. One caveat keeps enforcement honest: if a contract’s
    [[f1 ]](x) = [[f2 ]](x), so only inputs on which f1 terminates      requires can never hold, the body is never entered and the
    need to agree.                                                      check passes vacuously, testing nothing. Our pipeline guards
  • Conditional (regression) equivalence relaxes further to a           against this by reporting such a proof as inconclusive rather
    property ϕ marking the behavior worth preserving (we                than as a success, so the soundness of enforcement never rests
    write [[f1 ]](x) |= ϕ when f1 ’s runs on x satisfy it), asking      on an empty scope.
    for agreement only where the old version was already
                                                                                            III. R ELATED W ORK
    correct: [[f1 ]](x) |= ϕ ⇒ [[f1 ]](x) = [[f2 ]](x). Where f1
    violated ϕ the new version is free to differ, and that              A. Regression Verification and Equivalence Checking
    freedom is where the fix lives.                                        Regression Verification Tool (RVT) [3], [7] pioneered mod-
                                                                        ular regression verification, abstracting equivalent matched
   We target this conditional notion throughout. §IV makes
                                                                        callees with shared uninterpreted functions so the proof holds
it precise on an explicit in-scope set and relaxes the out-
                                                                        for any consistent interpretation. Reve / LLREVE [10], [11]
put equality to a property-relative obligation Eϕ , recovering
                                                                        encodes paired programs as constrained Horn clauses and
the definition above as the special case where ϕ observes
                                                                        infers coupling predicates relating the two versions’ states
the whole output. We denote this relation we target safety-
                                                                        with an external solver (Eldarica, Z3), while SymDiff [12]
preserving conditional equivalence.
                                                                        and DAC [13] relate the two versions by a relational sum-
C. Contracts and the Frame Rule                                         mary in the mutual-summary tradition [14]: a single predicate
Definition 3 (Function contract and admit set). A func-                 over the disjoint union of both versions’ inputs and outputs
tion contract is a Hoare-style triple [8], [9]: a precondi-             that characterizes their behavioral relationship. ARDiff [15]
tion (requires), a postcondition (ensures), and a frame                 prunes common code by iterative abstraction-refinement, but
(assigns) naming the locations the function may modify.                 only for Java; PEQcheck and PEQtest [16], [17] target lo-
We write C ≜ (Pre, Post, Assigns), with Pre ⊆ X a set of                calized refactorings through segment-level encodings; and
input states and Post ⊆ X × Y relating inputs to outputs over           PASDA [18] adds partition-based heuristics for the undecided
the state spaces X, Y defined above; throughout, we identify a          cases. Differential symbolic execution [19]–[22] characterizes
set such as Pre with its characteristic predicate, writing Pre(x)       program differences by exploring both versions’ symbolic state
for x ∈ Pre. Read in that relational model, the contract denotes        spaces, usually returning concrete divergence-inducing inputs
its admit set, the input/output pairs it permits,                       but no reusable artifact, as does LLM-driven test generation:
                                                                        Mokav [23] pairs it with differential testing for behavioral
     [[C]] ≜ {(x, o) ∈ X × Y | Pre(x) ⇒ (Post(x, o) ∧                   separation, and UnitTenX [24] drives agents over an ESBMC
        o agrees with x outside Assigns)},                              backend to build unit tests for legacy code, both producing
                                                                        tests rather than a proof certificate. Concurrent work by
with image [[C]](x) the outputs it allows on x; outside its
                                                                        Sarker et al. [25] takes differential symbolic execution in
precondition the contract permits anything, so [[C]](x) = Y
                                                                        an orthogonal direction, quantifying how much of the input
when ¬Pre(x).
                                                                        domain a patch changes rather than proving equivalence. Run
   A modular verifier supports two operations on such a                 as a soundness oracle on EqBench-C our checker surfaced
contract, used here only through their effect on [[C]]. Enforce-        more mislabeled Eq pairs than they report (nine versus five),
ment checks that the body of f satisfies its contract: every            while we target a sound modular equivalence proof, not an
execution from a requires-state ends in an ensures-                     impact measure.
state and writes only assigns locations. This is exactly the               Throughout this line the callee abstraction is supplied or
inclusion [[f ]] ⊆ [[C]], so a passing enforcement makes C an           derived from both bodies in lockstep, presupposing a complete
over-approximation of f . Replacement abstracts each call to            characterization of what is abstracted. The closest exception
f by the contract: the call site asserts requires, havocs the           is regression verification by impact summaries [26], which
locations named in assigns, and assumes ensures, so the                 restricts the proof to change-relevant behavior: a control- and
call ranges over [[C]](x) in place of [[f ]](x); since [[f ]] ⊆ [[C]]   data-dependence analysis marks the impacted statements and
once enforced, a proof under replacement is sound for the real          keeps only their path-condition constraints from a whole-
f.                                                                      program symbolic execution. That summary is exact, so the
   Replacement is an over-approximation: a proof obtained               check is sound and complete to the depth bound, but for the
under it is sound for the real function, but a reported failure         same reason the analysis must see all the code it reasons about.
may be spurious, because havocking the assigned locations               We instead abstract the old version alone by a weak one-sided
can hand the caller an output the real body never produces.             contract (one constraining the old version, never the new), a
The frame clause is what keeps replacement precise. Locations           reusable and enforceable artifact rather than a path-condition
not named in assigns are snapshotted before the body and                partition tied to one diff, scoped to what the property observes
asserted unchanged after, so without an explicit assigns the            rather than to what the change touches, and discharged once
bottom-up then reused at every call site and in every later          they are resolved identically on both sides by construction
check (§IV).                                                         and cannot themselves induce a divergence.
B. Contract, Invariant, and Frame Inference                          Definition 5 (Contract preserving regression-equivalence).
   Inferring functional specifications with LLMs has advanced        Given two versions f1 , f2 of a function and a property ϕ,
quickly. The closest are ACSL-for-C tools validated by Frama-        a contract C preserves regression-equivalence with respect to
C: AutoSpec’s accept-or-reject WP feedback [4], “Specify             ϕ iff:
What?” priming on EVA and Pathcrawler data [5], and Pre-               1) Enforcement. [[f1 ]] ⊆ [[C]]: C over-approximates f1 , so
guss’s iterative runtime-error-alarm refinement [6], the near-              every run of f1 is one C permits.
est analogue to our BMC-trace-driven loop on a Frama-                  2) Sufficiency for ϕ. For every x ∈ Sc, every o ∈ [[C]](x),
C backend. Other LLM-based generate+validate loops [27]–                    and every o2 ∈ [[f2 ]](x), we have Eϕ (o, o2 ): every output
[29]. Non-LLM inference [30], [31] and symbolic frame                       the replacement of f1 by C may produce meets the
inference [32]–[34] predate these; we contribute the BMC-                   regression obligation against f2 .
backed counterpart, with concrete-trace feedback drawn from            Condition 2 mirrors replacement: the abstracted call ranges
ESBMC’s frame-rule pass.                                             over exactly [[C]](x), the outputs C allows on x. We need
   Two gaps separate this work from all of the above. First,         not separately assume Sc ⊆ Pre: dropping it only strengthens
every such tool targets a single version; none reuses the            condition 2’s hypothesis (outside Pre, [[C]](x) = Y , so the
inferred contract as a callee abstraction in a two-version           obligation ranges over more outputs, never fewer), and the
regression-equivalence proof, the gap we close. Second, they         soundness proof never relies on Sc ⊆ Pre.
judge a specification by whether it verifies, not how tight it
is [5], [35]; to our knowledge none defines a semantic notion        Definition 6 (ϕ-regression-equivalence). f2 is ϕ-regression-
of contract tightness or a decision procedure for contract           equivalent to f1 iff for every x ∈ Sc, every o1 ∈ [[f1 ]](x), and
subsumption, which §IV-D introduces. The CE-guided LLM               every o2 ∈ [[f2 ]](x) the obligation Eϕ (o1 , o2 ) holds.
loop is by now established for invariants [36]–[43] and de-
                                                                        For deterministic functions (each [[f ]](x) a single output,
scends from counterexample-guided inductive synthesis [44]–
                                                                     shared external nondeterminism already folded into x by
[47], but those target invariants, not the function-level frame
                                                                     Definition 1), this coincides with the conditional equivalence
conditions we infer.
                                                                     [[f1 ]](x) |= ϕ ⇒ [[f1 ]](x) = [[f2 ]](x) of Definition 2, equality
                     IV. M ETHODOLOGY                                relaxed to Eϕ ; for genuinely multi-valued [[f ]](x) the pairwise
                                                                     form is strictly stronger.
A. One-Sided Contracts for Regression Equivalence (C1)
                                                                        Intuitively, the contract only needs to over-approximate the
    Recall from Definition 1 that each version is a relation         old version, while being precise on the behavior observed
[[f ]] ⊆ X ×Y of terminating runs, with image [[f ]](x), and from    by callers. This allows us to replace the old implementation
Definition 3 that a contract denotes a relation [[C]] ⊆ X × Y ,      during verification without introducing unsoundness.
with image [[C]](x) the outputs it allows on x. The abstraction
α of §I is just a contract: taking [[α]] = [[C]], its over-          Theorem T1 (Soundness of one-sided contract abstraction).
approximation requirement [[f1 ]] ⊆ [[α]] becomes [[f1 ]] ⊆ [[C]].   Let f1 , f2 be two versions of a function, C a contract, and ϕ
                                                                     a property with scope Sc and obligation Eϕ . If C preserves
Definition 4 (Scope and equivalence obligation). A property ϕ        regression-equivalence with respect to ϕ (Definition 5), then
fixes a scope Sc ≜ {x ∈ X | [[f1 ]](x) |= ϕ} of in-scope inputs      f2 is ϕ-regression-equivalent to f1 (Definition 6).
(the x on which every run of f1 stays within ϕ, e.g. runs
safely), and an equivalence obligation Eϕ (o1 , o2 ) that holds      Proof. Fix x ∈ Sc, o1 ∈ [[f1 ]](x), and o2 ∈ [[f2 ]](x).
when o1 and o2 agree on the part of the output ϕ observes (for       By condition 1, [[f1 ]] ⊆ [[C]], so [[f1 ]](x) ⊆ [[C]](x) and
example, the return value and the locations a caller reads).         o1 ∈ [[C]](x). Instantiate condition 2 with this x, the witness
                                                                     o := o1 , and the given o2 : its premises o1 ∈ [[C]](x) and
   We work under partial correctness and three standing as-          o2 ∈ [[f2 ]](x) both hold, so Eϕ (o1 , o2 ). As x, o1 , o2 were
sumptions, made explicit because the theorem rests on them:          arbitrary, f2 is ϕ-regression-equivalent to f1 .
(A1) only terminating runs populate [[·]], so the claim is over
inputs on which both versions terminate [3] (in particular, a           The proof turns on one step: enforcement (condition 1)
change that makes f2 diverge where f1 terminated is outside          places the real output o1 inside [[C]](x), and replacement
the guarantee, and detecting such termination regressions is         (condition 2) quantifies the obligation over all of [[C]](x), so
left to future work); (A2) the frame rule is sound (a body           it specializes to o1 . Condition 1 is what makes the proof
that passes enforcement writes no location outside Assigns,          sound; condition 2 is the only place C must be tight, and
even under aliasing); and (A3) the verifier that discharges          everywhere else it may stay weak. The relational-summary
enforcement and replacement is sound, so every verdict it            abstractions of SymDiff [12] and DAC [13] and the shared-
certifies holds in the relational model (Definition 3). Exter-       uninterpreted-function abstraction of RVT [3] do not allow
nal nondeterminism needs no separate assumption: a shared            this freedom, since they need a complete characterization of
callee’s responses are part of the input x (Definition 1), so        the procedure. The remaining obligations are discharged by the
standing assumptions (pointer aliasing across Assigns and non-         (i) (boundary) each Cg∂ at d(g) = N havocs a superset of
termination) and by the semantics (external nondeterminism is              g’s footprint, so [[g]] ⊆ [[Cg∂ ]]; and
folded into the shared input, Definition 1); these are standard       (ii) (interior) each g at d(g) < N passes enforcement
for Hoare reasoning with a frame rule. To our knowledge this               against its callees’ contracts, [[g | ([[Ch ]])h ]] ⊆ [[Cg ]].
is the first such formalization for a one-sided contract inside      Then [[g0 ]] ⊆ [[Cg0 ]]: the seed contract over-approximates the
a regression query, and it is what makes the contract small          seed without expanding any body below depth N .
enough for an LLM to infer.
   How our pipeline discharges conditions 1–2 as two concrete        Proof. Induct on the call relation of the depth-≤ N clo-
ESBMC queries is described in §IV-C.                                 sure, each callee before its caller. Base. A boundary node
                                                                     (d(g) = N ) is covered by (i), [[g]] ⊆ [[Cg∂ ]], with no
   Replacement is an over-approximation, so the converse of
                                                                     enforcement query. Step. For an interior g, every callee h
Theorem T1 can fail: the equivalence check may report a
                                                                     has d(h) ≤ d(g) + 1 ≤ N , so h lies in the closure with
spurious divergence, a witness o ∈ [[C]](x) that C permits
                                                                     a contract Ch ; the induction hypothesis gives [[h]] ⊆ [[Ch ]],
but f1 never produces and on which Eϕ fails. This is exactly
                                                                     monotonicity gives [[g]] = [[g | ([[h]])h ]] ⊆ [[g | ([[Ch ]])h ]],
why condition 2 requires C to be precise on the ϕ-observed
                                                                     and (ii) gives [[g]] ⊆ [[Cg ]]. The order is well-founded when the
output: looseness there admits an observably-disagreeing o
                                                                     closure is acyclic; an interior recursive g replaces its self-call
and condition 2 fails even when f1 and f2 genuinely agree
                                                                     by Cg in (ii), sound by the standard partial-correctness contract
(lost completeness, not soundness), whereas looseness off
                                                                     rule (A1 makes each terminating run’s recursion finite). Take
the observed projection only enlarges [[C]] on locations Eϕ
                                                                     g = g0 .
ignores and is harmless. That harmless region is the partial-
spec freedom, and it keeps the LLM step practical.                      Lemma L1 supplies condition 1 of T1 for g0 at the cost of
Remark 1 (Non-vacuity is machine-discharged). Theorem T1             the depth-N closure alone; condition 2 is discharged by the
is content-free if Sc = ∅: an unsatisfiable Pre makes condi-         seed’s equivalence harness (§IV-C), independent of N . Bound-
tion 1 hold vacuously and the conclusion vacuously true. Our         ary contracts need no enforcement step, so deepening the
approach does not rely on the user to rule this out. Instead it      boundary trades precision, not soundness, and T1’s partial-
employs a vacuity probe to ensure that the contract conditions       spec relaxation carries over to each interior Cg . Iterative
are not vacuously true [48].                                         deepening re-seeds a boundary function with bound N , turning
                                                                     its case (i) into case (ii) one stratum deeper; the single
                                                                     knob N trades inferred-contract precision against verification
B. Depth-Bounded Contract Closure                                    scalability.
   Theorem T1 governs the boundary between one abstracted            C. System Architecture (C2)
procedure and its caller. Regression targets in legacy code
transitively touch hundreds of helpers, and inferring partial           Our tools realize the method as a three-stage pipeline.
contracts for all of them in a single LLM pass is intractable.       C ONTRACTOR parses the C project with tree-sitter, identifies
We extend T1 by bounding the contract closure to a con-              the target functions, and scaffolds their harnesses. SCRIBE
figurable depth N from the seed target g0 . Let d(g) be the          then runs the LLM contract-inference loop over the interior
depth of g, its distance from the seed g0 . Functions at distance    functions through a JSON-schema interface, closing the depth-
d(g) < N along the static call graph receive precise partial         N frontier with the mechanical havoc boundary contracts of
contracts of T1’s shape; functions at d(g) = N receive               §IV-B. Finally, REGVER stages the old version, either from a
deliberately weak boundary contracts Cg∂ (precondition true,         git commit or a directory snapshot, and renames its symbols
postcondition true, and a frame that havocs every location           on a temporary copy so that both versions can coexist in a
reachable from the call); functions at d(g) > N receive no           single harness.
contract and are not analyzed in this pass. Under contract              From the enforced contracts, REGVER compiles condition 2
replacement, boundary contracts substitute at depth-N call           of Definition 5 into one equivalence harness. On a shared
sites and deeper bodies are never expanded, so the cost of           nondeterministic input x ∈ Sc it replaces the old version by its
verifying g0 is bounded by the depth-N closure independently         contract: the call site asserts requires, havocs assigns,
of the full callee depth.                                            and assumes ensures, so the result ranges over [[C]](x).
   Write [[g | σ]] for the denotation of g under a callee            It then runs the new version f2 concretely and asserts Eϕ
environment σ that replaces each callee h of g by a relation.        between the two outputs. That single verification condition
Here ( · )h is the family indexed by the callees h of g, so          is exactly condition 2, while enforcement (condition 1) is a
[[g | ([[h]])h ]] = [[g]] sends each callee to its own denotation    separate query placing every real f1 -output inside [[C]](x). The
and [[g | ([[Ch ]])h ]] replaces every callee by its contract. The   check thus reduces to two ESBMC queries, and f1 ’s body is
semantics is monotone in σ (a callee relation occurs only            never expanded inside the equivalence proof.
positively): σ ⊆ σ ′ pointwise implies [[g | σ]] ⊆ [[g | σ ′ ]].        Theorem T1 is stated over an abstract contract checker, and
                                                                     we instantiate its enforcement and replacement by ESBMC’s
Lemma L1 (Depth-N closure soundness). With contracts                 enforce and replace modes, whose documented replace-mode
assigned as above, suppose                                           behavior supplies the over-approximation the proof relies
on [29]. The theorem leaves the post-state property ϕ abstract,          Relative ordering, not absolute completeness. JUDGE
and in the implementation we fix it to the safety properties          measures the order between [[A]] and [[B]], not how close either
ESBMC encodes on every harness—memory safety (spatial                 is to [[f ]]. A contract it finds strictly tighter may still loosely
bounds and pointer- and dereference-validity, covering use-           over-approximate f , or not be valid for f at all; validity is
after-free), division by zero, arithmetic over- and under-            settled separately by enforcement (Theorem T1, condition 1),
flow, memory leaks, and undefined-behavior shifts. The                and we always report the two together. A verdict between two
same instantiation inherits the non-vacuity guard of Remark 1         enforced contracts is thus a statement about sound contracts,
from ESBMC’s vacuity probe.                                           the tighter side admitting strictly fewer behaviors while still
   Inference is driven by the very counterexamples the verifier       covering all of f ’s; between unenforced contracts it is only
already produces. When ESBMC enforces a proposed contract             a relative-over-approximation result, labelled as such in the
C (0) against f1 ’s body and the frame check fails, its frame-        evaluation tables.
rule pass recovers the offending write (file, line, and address          Tightness is the classical refinement ordering [49], [50].
expression) from the counterexample trace, and SCRIBE feeds           When both contracts are enforcement-checked, the ordering
that trace, not a bare verification-condition failure, into the       says more than set inclusion: the tighter contract proves at least
next prompt.                                                          as much, discharging every obligation the looser one does. We
D. Semantic Contract-Tightness Comparison (C3)                        state this as an extension of Theorem T1, reusing its scope
                                                                      Sc, obligation Eϕ , and condition 2 (sufficiency). We keep
   The published LLM contract-inference baselines (Au-
                                                                      Theorem T1’s scope Sc unchanged: the hypothesis [[A]] ⊆ [[B]]
toSpec [4], “Specify What?” [5], Preguss [6]) do not measure
                                                                      already gives [[A]](x) ⊆ [[B]](x) at every x, so no narrowing to
contract tightness semantically: they report verification success
                                                                      the preconditions is needed (in the warm-start, partial-versus-
rate, or at most count annotations by type. Any such syntactic
                                                                      strengthened comparison A and B share Pre anyway).
proxy is inflatable: a trivially true postcondition adds to the
count without adding constraint. We replace it with a decision        Theorem T2 (Tightness refines proof power). Let A, B be
procedure for contract subsumption.                                   contracts for f1 that both pass enforcement ([[f1 ]] ⊆ [[A]] and
   For contracts sound A, B on a common function over the             [[f1 ]] ⊆ [[B]]), with [[A]] ⊆ [[B]] (judge’s Check 1: A is at
state spaces X, Y of Definition 1, tightness is set inclusion on      least as tight as B). Then every regression-equivalence query
their admit sets: A ≤tight B ⇐⇒ [[A]] ⊆ [[B]]. JUDGE (C3)             against f2 that replace(B) discharges, replace(A) discharges
decides this ordering, splitting [[C]] into its postcondition and     too (condition 2 of Theorem T1 for B implies condition 2 for
frame parts. The postcondition part is two validity checks:           A), and the resulting proof is sound for the real f1 and f2 .
   • Check 1: ∀x, o. admitsA (x, o) ⇒ admitsB (x, o)            (is
       [[A]] ⊆ [[B]]?)                                                Proof. Fix x ∈ Sc. Since [[A]] ⊆ [[B]], also [[A]](x) ⊆ [[B]](x).
   • Check 2: ∀x, o. admitsB (x, o) ⇒ admitsA (x, o)            (is   Condition 2 for B requires Eϕ (o, o2 ) for every o ∈ [[B]](x) and
       [[B]] ⊆ [[A]]?)                                                o2 ∈ [[f2 ]](x); restricting to o ∈ [[A]](x) gives condition 2 for
                                                                      A. As A passes enforcement, Theorem T1 turns condition 2
where admitsC (x, o) ≡ ¬ PreC (x) ∨ PostC (x, o) is member-
                                                                      for A into the regression-equivalence of f1 and f2 .
ship in [[C]] with the frame conjunct dropped (a superset test);
frame containment on Assigns is checked separately (syntac-
tically in v1, see §V-G). When A and B share their precon-               The converse fails, and that is the point: a looser contract
dition and frame (the warm-start, partial-versus-strengthened         proves no more, and may admit an output f1 never produces
case Theorem T2 ranges over), a passing Check 1/Check 2               that raises a spurious divergence the tighter one rules out. So
establishes [[A]] ⊆ [[B]]. These checks are sound in that             for enforcement-sound contracts judge’s verdict is a refinement
direction but not complete: because admitsC drops the frame,          ordering: the strictly tighter side discharges at least as many
a failing check can be spurious (its witness may lie out-             regression queries, and strictly more whenever it eliminates
side the shared precondition/frame region), so judge may              such a spurious counterexample.
under-report tightness, never over-report it. Under the same
shared-precondition/frame assumption, the four outcomes of
(Check 1, Check 2) classify the pair: (✓, ✓) is equivalent                                    V. E VALUATION
([[A]] = [[B]]); (✓, ×) is A strictly tighter; (×, ✓) is B strictly
tighter; (×, ×) is incomparable. Each failing check yields a
counterexample witness: a concrete (x, o) admitted by one               We evaluate the contributions of §IV around two questions:
contract and rejected by the other. The incomparable case
ships two witnesses, one per direction, surfacing the precise           RQ1 - Feedback Modality
behavior each contract admits that the other does not. Each             Which counterexample modality most effectively
check is a pure validity query over a nondeterministic input            drives frame-condition inference: concrete BMC traces,
and output, with no body of f involved (neither enforcement             verification-condition failures (AutoSpec), or runtime-
nor replacement); our implementation discharges each as a               error traces (Preguss)?
single SMT query.
  RQ2 - Tractability                                                refinement), and AutoDeduct [30] (CHC+Eva, no LLM).
                                                                    We compare against the numbers each tool reports in its
  Given that the SCRIBE loop produces a partial contract
                                                                    published evaluation, on the inputs it reports them for:
  (RQ1), how much additional tightness does continued
                                                                    Frama-C-Problems for AutoSpec and Preguss, and the SV-
  strengthening recover beyond it, and do those returns
                                                                    COMP-derived subset and X509-parser for AutoSpec. We run
  plateau? This is the practical test of the partial-spec
                                                                    SCRIBE on those same inputs and report its success rate and
  freedom of Theorem T1: not whether a partial contract
                                                                    iteration count alongside theirs. For regression verification
  is cheaper to infer, but whether it is a good place to stop.
                                                                    we use EqBench-C only as a lightweight soundness check on
                                                                    REGVER , without a numeric cross-tool ranking: the established
  The order is deliberate. RQ1 establishes that the inference
loop works at all, and RQ2 then asks whether the partial            equivalence checkers (RVT [3], Reve [11], ARDiff [15],
contract it produces is already tight enough; RQ2 only makes        SymDiff [12]) decide partial rather than safety-preserving
sense once RQ1 is settled. We describe the datasets, baselines,     conditional equivalence, and the ones with EqBench results
and metrics, then report results.                                   (ARDiff and its symbolic-execution successors) report on the
                                                                    Java subset, so no like-for-like EqBench-C number exists to
A. Datasets                                                         compare against. We run REGVER on this set in two arms, a
      a) EqBench-C.: The C subset of EqBench [51]: 147              contract-free baseline and a treatment arm in which SCRIBE
equivalent and 125 non-equivalent program pairs. EqBench is         first infers a one-sided contract for the changed function, and
the most comprehensive public equivalence-checking dataset,         combine them as a sequential portfolio: the baseline runs
built to cover the hard constructs earlier benchmarks omit          first and the treatment arm is invoked only on the pairs it
(non-linear arithmetic, loops, floating point, and string and       leaves undecided, the timeout and tool-error tail. Because the
array manipulation), which makes its C subset a demand-             escalation gate is the baseline’s own abstention, observable at
ing soundness stress-test even though formal C tools have           run time and independent of the dataset label, the combination
rarely reported on it. Its pairs are labelled by input-output       is a portfolio and not an oracle, and it inherits every false
equivalence of terminating runs, the same notion REGVER’s           positive the contract layer raises on that tail.
contract-free harness decides, so the labels are valid ground
                                                                    C. Experimental Setup
truth for our regression check. We use EqBench-C as a
soundness baseline for REGVER, not a cross-tool rate ranking:          We evaluate with three LLMs chosen for diversity: Opus
the question we ask is the safe one, whether REGVER ever            4.8 [54] (closed-source frontier), Kimi K2.6 [55] (open-weight
certifies a non-equivalent pair as equivalent. We evaluate          frontier), and Qwen3.6-27B [56] (open-weight, runnable on
on EqBench-C rather than the more recent EquiBench [52]             inexpensive hardware), all at temperature 0.
because EquiBench labels pairs by full input-output equiva-            For the formal verifier we use ESBMC with Z3 (due to
lence (Definition 2), a relation finer than the safety-preserving   quantifier support). ESBMC runs under k-induction with no
regression equivalence our methodology targets.                     fixed unwinding bound: inductively closed loops are proved
      b) Frama-C-Problems.: Frama-C-Problems [53] is a              for every iteration and the rest unrolled in full, completing on
community set of 51 small C programs (∼20 LoC aver-                 finite loops and otherwise timing out. Three limits are fixed
age), each carrying an unproven guard assertion and 1–3             across every comparison run: a per-query ESBMC timeout and
ACSL specifications. AutoSpec [4] introduced it as a contract-      a per-call LLM timeout, both 300s, and at most 5 refinement
inference benchmark and Preguss [6] reused it, so it is the         iterations per target. ESBMC also runs under a 104GB per-
standing benchmark for this task and both report per-program        process memory budget, applied as a Linux control-group limit
success rates on it. We evaluate SCRIBE on all 51 programs.         with swap off, so a run that exceeds it stops at its memory
      c) X509-parser.: X509-parser is a formally verified RTE-      ceiling rather than growing into swap; a stopped run is a non-
free X.509 parser (>1000 LoC, manually verified in ACSL             result, never a pass or a failure. A non-result is a run that
by its authors over five months), against which AutoSpec [4]        returns no verdict: a query timeout, a memory-ceiling stop, an
reports synthesized specifications for six functions, selected      ESBMC crash or solver error, an unreadable exit, or an LLM
to span loops with buffer arithmetic, switch-case control           API failure. We report each success rate two ways: over the
flow, inter-procedural composition, and mixed-width integer         cases ESBMC decided, and with every non-result charged as
and shift operations. We evaluate SCRIBE on those same six          a failure (to keep the lower bound conservative).
functions; the depth-bounded closure of §IV-B (Lemma L1),           D. Metrics and Mapping to RQs
a standing part of our C2 contribution rather than an ablation
knob, handles their inter-procedural composition.                     Each RQ pairs a metric with the dataset it is measured on.
                                                                      • RQ1 (feedback modality): contract-inference success rate
B. Baselines                                                            and iterations to convergence on Frama-C-Problems and
  For frame inference (RQ1) we compare against                          X509-parser, read against AutoSpec’s and Preguss’s pub-
AutoSpec [4] (LLM+WP, VC-level feedback), “Specify                      lished numbers.
What?”     [5]     (LLM+WP+EVA/Pathcrawler    prompt                  • RQ2 (tractability): the round-by-round JUDGE tightness
augmentation), Preguss [6] (LLM+WP+RTE-trace iterative                  verdict (the saturation curve) and pass rate of SCRIBE’s
     partial contract against the warm-start HARDSCRIBE arm,                                    TABLE I
     on Frama-C-Problems.                                                            RQ1 CONTRACT- INFERENCE SUCCESS

E. Results                                                                 Tool (oracle)                  Frama-C-Problems      X509
   We report RQ1 and RQ2 from the three-model sweep on the                 AutoSpec (func.)                 31/51 (60.8%)       6/6
inputs the baselines publish, plus the EqBench-C soundness                 Preguss (RTE)                   122/153a(79.7%)      n/a
baseline.                                                                  SCRIBE, Opus 4.8             36/51 (70.6% / 85.7%)   5/6
                                                                           SCRIBE, Kimi K2.6            40/51 (78.4% / 85.1%)   5/6
   1) RQ1 (feedback modality): We ran SCRIBE in its default                SCRIBE, Qwen3.6-27B          36/51 (70.6% / 81.8%)   3/6
partial-spec mode on the two inputs the closest baselines                  a Per-trial rate over three trials.
report on, the 51 Frama-C-Problems programs and the X509
parser, across all three models. Table I gives the headline.
                                                                                                 TABLE II
On Frama-C-Problems, SCRIBE infers a verifier-discharged             RQ1 PER - STEP PASS RATES OVER REFINEMENT ATTEMPTS , PER MODEL .
contract for most programs on all three models, with the
decided and conservative success rates shown. Non-results are                          Model              Enforce   Replace
few and cluster on the hard array and loop cases (20 across the                        Kimi K2.6            0.82     0.95
three models, mostly query timeouts, the rest ESBMC crashes,                           Opus 4.8             0.75     0.98
unreadable exits, and one LLM API error; no run reached the                            Qwen3.6-27B          0.75     0.93
104GB ceiling).
   Measured the way the baselines count, with every non-result
a failure, these conservative rates clear AutoSpec on every         accepted round so JUDGE can measure how much tighter each
model and reach Preguss’s per-trial rate at the top of the range,   round is than the seed. Strengthening saturates fast in every
from a single deterministic run at temperature 0 where Preguss      model (Figure 3): for almost all orderable targets the contract
averages three trials. The three tools use different success ora-   is already at its tightest at the seed (Table III), and where
cles: AutoSpec targets functional correctness, Preguss freedom      strengthening helps it does so in the first round or two and
from runtime errors, and SCRIBE a contract that passes both         then stops, its round-over-round gain reaching zero by round
enforcement and replacement, which the next paragraph shows         two or three.
subsumes Preguss’s condition.                                          The endpoint comparison agrees (Table III): judging each
   One feature makes the comparison fairer than the differing       model’s full contract against its own partial seed over the
oracles suggest: SCRIBE’s enforcement turns on ESBMC’s full         orderable pairs, the two are equivalent for the large majority
safety set, covering the runtime-error class Preguss proves         of targets and only a few are strictly tighter after strengthen-
absent, while also checking a functional postcondition and          ing. The warm-start arm costs almost nothing in soundness,
caller-sufficiency, so a passing SCRIBE result certifies at least   keeping the last contract that verifies, so its pass rate matches
as much as a passing Preguss one.                                   the partial arm to within one program in every model. The
   Table II reports the per-step pass rates, with the same          answer to RQ2 is that caller-sufficiency already captures most
pattern across the three models: enforcement is the binding         of the attainable tightness: a cheap partial contract is within
gate and replacement nearly always follows once it passes.          a few targets of the strongest contract the loop can reach, a
postcondition toward one the body satisfies. Most targets           direct validation of the partial-spec stopping point.
converge in a single iteration (Figure 2). On the X509 parser,         Two bounds keep this honest. About 40% of round-level
SCRIBE verifies 5 of 6 target functions with Opus and Kimi          comparisons involve a quantified or pointer-dereferencing
and 3 of 6 with Qwen, against the 6 of 6 AutoSpec reports;          postcondition JUDGE’s signature-only harness cannot order;
the function set is similar but not identical, so we read this as   we hold those out and fix the denominator to the targets
close rather than head-to-head.                                     orderable in every round, so the saturation we report speaks
                                                                    only for the contracts JUDGE can compare across all rounds.
  RQ1 Answer                                                        And the warm-start arm strengthens within the seed’s clause
                                                                    shape, so this rapid saturation shows little tightness is left
  Model-checker counterexamples alone provide an effec-
                                                                    within that shape, not that no tighter contract of a different
  tive refinement signal for contract inference. Across the
                                                                    shape exists, which we leave to the from-scratch study in
  evaluated benchmarks SCRIBE reaches verification rates
                                                                    §V-G.
  comparable to prior approaches that additionally rely
  on weakest-precondition reasoning, value analysis, or               RQ2 Answer
  runtime-error annotations, while most contracts converge
  after a single refinement iteration.                                Continued strengthening recovers little beyond the partial
                                                                      contract: caller-sufficiency already captures most of the
  2) RQ2 (tractability): RQ1 leaves the loop reliably produc-         attainable tightness, and the few targets that tighten do so
ing a verifiable partial contract. We seed the warm-start arm         within a round or two before the returns plateau, so the
(HARDSCRIBE) from each model’s partial contract and apply             partial contract is a sound place to stop.
up to five enforce-gated strengthening rounds, keeping every
                                    RQ3 convergence histogram — frama-c-problems                                                                             TABLE III
                              24              25                                                               kimi-k2.6           RQ2 TIGHTNESS ENDPOINT, PER MODEL . “PARTIAL / F ULL” ARE THE
                                    20                                                                         qwen3.6-27b                   PER - ARM PASS COUNTS ( FULL ARM OF 50).
                     20
harnesses

                                                                                                               claude-opus-4-8
                                                               12    12
                     10                                                          7                                                      Model             Sat. @0   Equiv : tighter     Partial / Full
                                                                                                 2         2         1
                      0                                                                                                                 Kimi K2.6          43/47        13 : 2             40 / 41
                                    1                                   2                                 3
                                                     iteration first reaching pass+pass                                                 Opus 4.8           40/42        18 : 2             36 / 36
                                                                                                                                        Qwen3.6-27B        38/42        14 : 4             36 / 36

Fig. 2. RQ1 convergence histogram per model on Frama-C-Problems: the
iteration at which each harness first reaches a passing enforce and replace.                                                                                    TABLE IV
Most targets converge in a single iteration.                                                                                              E Q B ENCH -C REACH . C OUNTS ARE OUT OF 272 PAIRS .


                                   RQ2 tightness saturation curve — frama-c-problems                                                   Arm                          Decided      Correct    FP       FN
                                         kimi-k2.6     qwen3.6-27b   claude-opus-4-8   vs seed       vs prev
                                                                                                                                       Baseline (contract-free)       70           56       14       0
% strictly tighter




                     20
                                                                                                                                       + contracts, Opus 4.8         105           65       40       0
                     10                                                                                                                + contracts, Kimi K2.6        106           67       39       0
                                                                                                                                       + contracts, Qwen3.6-27B      102           63       38       1a
                      0
                          1                     2                     3                          4                        5            a triangularMod: false FN under safety-preserving condi-
                                                             strengthening round                                                        tional equivalence.

Fig. 3. RQ2 tightness saturation on Frama-C-Problems. Per model, the share
of orderable targets strictly tighter than the partial seed at round k (solid) and                                               targets, since the two versions agree wherever the old one
the round-over-round gain over the previous round (dashed). The denominator
is fixed across rounds to the targets JUDGE orders in every round (16 / 18 /                                                     terminates; we report it as the dataset scores it rather than
19 for Opus 4.8 / Kimi K2.6 / Qwen3.6-27B), so the solid curve is monotone                                                       substitute our own oracle. Contracts therefore extend reach
by construction.                                                                                                                 into EqBench-C’s hardest cases and fail safe: every decision
                                                                                                                                 they add is correct or a triageable false alarm, never a missed
                                                                                                                                 difference.
   3) Soundness and reach on EqBench-C: REGVER runs the
contract-free regression harness on all 272 pairs, producing a                                                                   F. Discussion
verdict on 70; the rest time out or hit a tool error and are held
out. On the decided pairs it never fabricates an equivalence:                                                                       The results cohere around the contributions. RQ1 supports
100% recall, zero false negatives (Figure 4). Some of its                                                                        C2, that BMC trace feedback is enough to drive frame
false positives are not over-detection but dataset mislabels,                                                                    inference: a single model checker driven by counterexamples
pairs EqBench labels Eq that are actually non-equivalent; we                                                                     infers verifiable contracts competitively with heavier weakest-
found nine and filed them upstream [57] , and independent                                                                        precondition pipelines. RQ2 supports the partial-spec stopping
work reports EqBench mislabels as well [25]. We draw no                                                                          point of Theorem T1 (C1), the cheap partial contract already
cross-tool ranking (see §V-B): the comparable checkers decide                                                                    close to the tightest a strengthening loop reaches, with JUDGE
partial rather than safety-preserving conditional equivalence,                                                                   (C3) supplying the tightness ordering behind that claim and
so EqBench-C serves as a soundness check, not a competitive                                                                      reporting unorderable rounds as a scope bound. The refinement
baseline.                                                                                                                        telemetry shows the mechanism, enforcement the binding gate
      a) Reach with contracts.: A developer runs the contract-                                                                   and the loop only ever weakening an over-strong postcondi-
free baseline first and escalates only the pairs it cannot decide;                                                               tion; and the EqBench-C baseline backs the soundness half of
on that undecided tail SCRIBE infers a one-sided contract                                                                        C1 directly, with zero fabricated equivalences.
for the changed function and REGVER runs again. This is
where contracts earn their keep: they recover 9, 11, and 7                                                                       G. Threats To Validity
correct decisions for Opus, Kimi, and Qwen on pairs the                                                                             Construct validity. The cross-tool RQ1 comparison spans
baseline left as timeouts or tool errors, pushing the decided                                                                    different success oracles, so we present it as a situating com-
count from 70 to 105 / 106 / 102 (Table IV), and every                                                                           parison rather than a head-to-head. On EqBench-C REGVER
recovered decision is a real divergence the baseline was too                                                                     runs in two arms against the dataset’s full-equivalence labels
weak to expose. The gain comes at an expected precision                                                                          as a soundness check, not a tool ranking; the reported cascade
cost: the inferred contracts over-approximate, so the recovered                                                                  composes them post hoc, faithfully, since pairs are scored
tail is false-alarm-heavy. But each false alarm lands on a                                                                       independently and the escalation gate reads only the baseline’s
pair the baseline could not decide at all, a triageable over-                                                                    abstention, not the label. Because REGVER targets the weaker
approximation rather than a regression. Soundness holds under                                                                    conditional equivalence, a pair the dataset scores as a miss
the relation we target: no model fabricates an equivalence, the                                                                  may be correct under our notion (triangularMod); scoring
lone dataset-scored exception being triangularMod under                                                                          against the dataset regardless, such mismatches can only count
Qwen, non-equivalent under full equivalence but equivalent                                                                       against us. JUDGE (C3) reports a relative tightness ordering on
under the safety-preserving conditional equivalence REGVER                                                                       admit sets, not whether a contract characterises f completely;
                           EqBench regression-verification outcomes                  preserving, is sound for the regression check, and a depth-
                                                                  121
                                                                                     bounded closure (Lemma L1) bounds the contract closure so
        100
                                                                            79       the proof scales. The target of inference is therefore not a
cases




         50   35
                                                                                     complete specification but the weakest contract a caller needs.
                      21           14
                                              0          2                               An end-to-end system (SCRIBE, CONTRACTOR, REGVER)
          0
              TP      TN           FP        FN    SIG_MISMATCH TIMEOUT TOOL_ERROR   infers these contracts automatically from the model checker’s
                                                                                     own counterexamples, with no separate specification step. On
Fig. 4. Contract-free baseline regression-verification outcomes on EqBench-C.        Frama-C-Problems and the ANSSI X509 parser this reaches a
The false-negative bucket (a non-equivalent pair called equivalent) is empty:        verification rate comparable to the weakest-precondition tools
the baseline never fabricates an equivalence.
                                                                                     AutoSpec and Preguss while certifying a stronger property,
                                                                                     enforcement plus caller-sufficiency with runtime-error free-
we always pair its verdict with enforcement, so a tighter-under-                     dom included, which answers RQ1: counterexample feedback
JUDGE contract that also enforces is unambiguously a tighter                         alone is a sufficient signal for frame inference. Strengthening
sound contract. The C1 guarantee holds under its assumptions                         each inferred contract past caller-sufficiency barely tightens
on assigns aliasing, nondeterministic external calls, and                            it, the partial and warm-started contracts coming out JUDGE-
termination; outside those it degrades to an honest unknown                          equivalent for the large majority of comparable targets, so
rather than a false proof.                                                           the partial-spec stopping point of Theorem T1 is close to the
   Internal validity. SCRIBE runs each model once at tempera-                        practical ceiling rather than a compromise (RQ2).
ture 0, a single deterministic trajectory rather than an average                         A decision procedure for contract subsumption (JUDGE)
over LLM sampling; we mitigate by reporting three models                             reports these tightness results as a real set-inclusion ordering
whose refinement telemetry is near-identical, but a different                        rather than a gameable clause count. The regression check
seed could shift individual cases. Non-results are excluded                          underneath is sound by construction: on EqBench-C REGVER
from the pass-rate denominator, which the two-way reporting                          never fabricates an equivalence, and run as a soundness oracle
(§V) keeps honest since none is a wrong verdict. On EqBench-                         it surfaced nine pairs the suite mislabels as equivalent, more
C the size and make-up of the undecided tail the treatment arm                       than concurrent work reports. Together these establish that
escalates on depend on the per-query timeout, fixed at 300s                          sound, modular regression verification can be driven by a
across both arms. RQ2’s warm start tightens only within the                          model checker’s own counterexamples and a partial contract,
seed’s clause shape and cannot reach a structurally different                        with no hand-written specification.
contract; we frame it as the marginal value of continued                                 Two directions follow naturally. LLM-driven C++ contract
strengthening and keep JUDGE strictly post hoc, so the loop                          inference: every published LLM contract-inference tool we
is gated on enforcement, never on the tightness measure it                           are aware of is C-only, so inferring functional contracts for
reports.                                                                             C++ operator overloads, initializer-list constructors, RAII de-
   External validity. The baseline comparison is one-                                structors, and template instantiations over the standard library
way (published numbers, not re-runs), on the same full-                              is an unaddressed problem and the natural next target for
denominator basis they report. The benchmarks are small                              this line of work. Regression verification across signature
(Frama-C-Problems averages about seventeen lines, the X509                           changes: RVT [3], Reve [11], SymDiff [12], and REGVER
study six functions, EqBench-C crafted rather than production                        all assume the old and new versions share a signature, so
code), so generalisation to large real-world C, and to C++,                          aligning refactored signatures (parameter reordering, splitting,
is future work. The supported program class is bounded by                            merging, type changes) for verification-grade equivalence is
engineering gaps with known fixes: the tree-sitter call/include                      an open problem, naturally cast as a relational extension of
graph misses indirect, virtual, and macro-expanded calls (an                         Theorem T1 in which the parameter alignment is itself part of
LLVM-IR pipeline with SVF [58] or libclang closes this),                             the inference.
the REGVER rename pass cannot rewrite identifiers in macro                                           VII. ACKNOWLEDGEMENTS
bodies (Coccinelle [59]), and its side-effect comparator sees
                                                                                       The authors acknowledge the use of generative AI tools
only writes through pointer parameters (bi-abduction [33]
                                                                                     in both the development of the research tooling and the
and Infer-style footprints extend it). JUDGE’s tightness figures
                                                                                     preparation of this manuscript. All AI-assisted content was
exist only on its primitive-typed signature class. These are
                                                                                     subsequently reviewed, revised, and validated by the authors,
engineering scope bounds, not open research questions.
                                                                                     who assume full responsibility for the integrity and accuracy
                                                                                     of the final publication.
                              VI. C ONCLUSION
   We asked whether a partial, caller-sufficient contract, rather
than a full behavioral specification, is enough to verify re-
gression equivalence. Theorem T1 answers yes for safety-
preserving conditional equivalence: a one-sided contract that
abstracts only the old version, scoped to the property worth
                             R EFERENCES                                            M. Wimmer, Eds. Cham: Springer International Publishing, 2022, pp.
                                                                                    184–204.
 [1] Z. Yin, D. Yuan, Y. Zhou, S. Pasupathy, and L. Bairavasundaram, “How      [18] J. Glock, J. Pichler, and M. Pinzger, “Pasda: A partition-based semantic
     do fixes become bugs?” in Proceedings of the 19th ACM SIGSOFT                  differencing approach with best effort classification of undecided
     Symposium and the 13th European Conference on Foundations of                   cases,” Journal of Systems and Software, vol. 213, p. 112037, 2024.
     Software Engineering, ser. ESEC/FSE ’11. New York, NY, USA:                    [Online]. Available: https://www.sciencedirect.com/science/article/pii/
     Association for Computing Machinery, 2011, p. 26–36. [Online].                 S0164121224000803
     Available: https://doi.org/10.1145/2025113.2025121                        [19] S. Person, M. B. Dwyer, S. Elbaum, and C. S.
 [2] H. G. Rice, “Classes of recursively enumerable sets and their                  Pundefinedsundefinedreanu, “Differential symbolic execution,” in
     decision problems,” Transactions of the American Mathematical                  Proceedings of the 16th ACM SIGSOFT International Symposium
     Society, vol. 74, no. 2, pp. 358–366, 1953. [Online]. Available:               on Foundations of Software Engineering, ser. SIGSOFT ’08/FSE-16.
     http://www.jstor.org/stable/1990888                                            New York, NY, USA: Association for Computing Machinery, 2008, p.
 [3] B. Godlin and O. Strichman, “Regression verification: proving the              226–237. [Online]. Available: https://doi.org/10.1145/1453101.1453131
     equivalence of similar programs,” Software Testing, Verification and      [20] H. Palikareva, T. Kuchta, and C. Cadar, “Shadow of a doubt: testing
     Reliability, vol. 23, no. 3, pp. 241–258, 2013. [Online]. Available:           for divergences between software versions,” in Proceedings of the
     https://onlinelibrary.wiley.com/doi/abs/10.1002/stvr.1472                      38th International Conference on Software Engineering, ser. ICSE ’16.
 [4] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C. Cheung, and          New York, NY, USA: Association for Computing Machinery, 2016,
     C. Tian, “Enchanting program specification synthesis by large language         p. 1181–1192. [Online]. Available: https://doi.org/10.1145/2884781.
     models using static analysis and program verification,” in Computer            2884845
     Aided Verification, A. Gurfinkel and V. Ganesh, Eds. Cham: Springer       [21] C. Luo, W. Meng, and S. Wang, “Strengthening supply chain security
     Nature Switzerland, 2024, pp. 302–328.                                         with fine-grained safe patch identification,” in Proceedings of the
 [5] G. Granberry, W. Ahrendt, and M. Johansson, “Specify what? enhancing           IEEE/ACM 46th International Conference on Software Engineering, ser.
     neural specification synthesis by symbolic methods,” in Integrated             ICSE ’24. New York, NY, USA: Association for Computing Machinery,
     Formal Methods, N. Kosmatov and L. Kovács, Eds. Cham: Springer                2024. [Online]. Available: https://doi.org/10.1145/3597503.3639104
     Nature Switzerland, 2025, pp. 307–325.                                    [22] C. Helbling, G. Leach-Krouse, S. Lasser, and G. Sullivan, “cozy:
 [6] Z. Wang, T. Lin, M. Chen, H. Li, M. Yang, X. Yi, S. Qin, Y. Luo,               Comparative symbolic execution for binary programs,” in Proceedings
     X. Li, B. Gu, L. Lu, and J. Yin, “A tale of 1001 loc: Potential                2025 Workshop on Binary Analysis Research, ser. BAR 2025. Internet
     runtime error-guided specification synthesis for verifying large-scale         Society, 2025. [Online]. Available: http://dx.doi.org/10.14722/bar.2025.
     programs,” Proc. ACM Program. Lang., vol. 10, no. OOPSLA1, Apr.                23004
     2026. [Online]. Available: https://doi.org/10.1145/3798268                [23] K. Etemadi, B. Mohammadi, Z. Su, and M. Monperrus, “Mokav:
 [7] B. Godlin and O. Strichman, “Regression verification,” in Proceedings          Execution-driven differential testing with llms,” p. 112571, 2025.
     of the 46th Annual Design Automation Conference, ser. DAC ’09.                 [Online]. Available: https://www.sciencedirect.com/science/article/pii/
     New York, NY, USA: Association for Computing Machinery, 2009, p.               S0164121225002407
     466–471. [Online]. Available: https://doi.org/10.1145/1629911.1630034
                                                                               [24] Y. Charalambous, C. N. C. Jr, L. Lamb, and L. C. Cordeiro, “Unittenx:
 [8] C. A. R. Hoare, “An axiomatic basis for computer programming,”
                                                                                    Generating tests for legacy packages with ai agents powered by formal
     Commun. ACM, vol. 12, no. 10, p. 576–580, Oct. 1969. [Online].
                                                                                    verification,” 2025. [Online]. Available: https://arxiv.org/abs/2510.05441
     Available: https://doi.org/10.1145/363235.363259
                                                                               [25] L. Sarker, A. Satter, and T. Bultan, “Quantitative symbolic patch impact
 [9] B. Meyer, “Applying ’design by contract’,” Computer, vol. 25, no. 10,
                                                                                    analysis,” Cham, pp. 367–390, 2026.
     pp. 40–51, 1992.
                                                                               [26] J. Backes, S. Person, N. Rungta, and O. Tkachuk, “Regression verifica-
[10] D. Felsing, S. Grebing, V. Klebanov, P. Rü mmer, and
                                                                                    tion using impact summaries,” in Model Checking Software, E. Bartocci
     M. Ulbrich, “Automating regression verification,” in Proceedings of
                                                                                    and C. R. Ramakrishnan, Eds. Berlin, Heidelberg: Springer Berlin
     the 29th ACM/IEEE International Conference on Automated Software
                                                                                    Heidelberg, 2013, pp. 99–116.
     Engineering, ser. ASE ’14. New York, NY, USA: Association
     for Computing Machinery, 2014, p. 349–360. [Online]. Available:           [27] N. Tihanyi, Y. Charalambous, R. Jain, M. A. Ferrag, and L. C. Cordeiro,
     https://doi.org/10.1145/2642937.2642987                                        “A new era in software security: Towards self-healing software via large
[11] V. Klebanov, P. Rümmer, and M. Ulbrich, “Automating regression veri-          language models and formal verification,” pp. 136–147, 2025.
     fication of pointer programs by predicate abstraction,” Formal Methods    [28] C. Richter and H. Wehrheim, “Beyond postconditions: Can large
     in System Design, vol. 52, no. 3, pp. 229–259, 2018.                           language models infer formal contracts for automatic software
[12] S. K. Lahiri, C. Hawblitzel, M. Kawaguchi, and H. Rebêlo, “Symdiff:           verification?” 2025. [Online]. Available: https://arxiv.org/abs/2510.
     A language-agnostic semantic diff tool for imperative programs,” in            12702
     Computer Aided Verification, P. Madhusudan and S. A. Seshia, Eds.         [29] M. A. A. Pirzada, W. Wang, Y. Charalambous, K. Korovin, and
     Berlin, Heidelberg: Springer Berlin Heidelberg, 2012, pp. 712–717.             L. C. Cordeiro, “Conver: Using contracts and loop invariant synthesis
[13] S. K. Lahiri, K. L. McMillan, R. Sharma, and C. Hawblitzel,                    for scalable formal software verification,” 2026. [Online]. Available:
     “Differential assertion checking,” in Proceedings of the 2013 9th Joint        https://arxiv.org/abs/2605.27051
     Meeting on Foundations of Software Engineering, ser. ESEC/FSE 2013.       [30] J. Amilon, D. Gurov, C. Lidström, M. Nyberg, G. Ung, and
     New York, NY, USA: Association for Computing Machinery, 2013, p.               O. Wingbrant, “Autodeduct: A tool for automated deductive verification
     345–355. [Online]. Available: https://doi.org/10.1145/2491411.2491452          of c code,” 2025. [Online]. Available: https://arxiv.org/abs/2501.10889
[14] C. Hawblitzel, M. Kawaguchi, S. K. Lahiri, and H. Rebêlo, “Towards       [31] J. Amilon, Z. Esen, D. Gurov, C. Lidström, and P. Rümmer, An
     modularly comparing programs using automated theorem provers,” in              Exercise in Mind Reading: Automatic Contract Inference for Frama-C.
     Automated Deduction – CADE-24, M. P. Bonacina, Ed.              Berlin,        Cham: Springer International Publishing, 2024, pp. 553–582. [Online].
     Heidelberg: Springer Berlin Heidelberg, 2013, pp. 282–299.                     Available: https://doi.org/10.1007/978-3-031-55608-1 13
[15] S. Badihi, F. Akinotcho, Y. Li, and J. Rubin, “Ardiff: scaling            [32] Z. Rakamaric and A. J. Hu, “Automatic inference of frame axioms using
     program equivalence checking via iterative abstraction and refinement          static analysis,” in 2008 23rd IEEE/ACM International Conference on
     of common code,” in Proceedings of the 28th ACM Joint Meeting                  Automated Software Engineering, 2008, pp. 89–98.
     on European Software Engineering Conference and Symposium on              [33] C. Calcagno, D. Distefano, P. O’Hearn, and H. Yang, “Compositional
     the Foundations of Software Engineering, ser. ESEC/FSE 2020. New               shape analysis by means of bi-abduction,” in Proceedings of the
     York, NY, USA: Association for Computing Machinery, 2020, p.                   36th Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     13–24. [Online]. Available: https://doi.org/10.1145/3368089.3409757            Programming Languages, ser. POPL ’09. New York, NY, USA:
[16] M.-C. Jakobs, “Peqcheck: Localized and context-aware checking of               Association for Computing Machinery, 2009, p. 289–300. [Online].
     functional equivalence,” in 2021 IEEE/ACM 9th International Confer-            Available: https://doi.org/10.1145/1480881.1480917
     ence on Formal Methods in Software Engineering (FormaliSE), 2021,         [34] S. Spies, L. Gäher, M. Sammler, and D. Dreyer, “Quiver: Guided
     pp. 130–140.                                                                   abductive inference of separation logic specifications in coq,” Proc.
[17] M.-C. Jakobs and M. Wiesner, “Peqtest: Testing functional equivalence,”        ACM Program. Lang., vol. 8, no. PLDI, Jun. 2024. [Online]. Available:
     in Fundamental Approaches to Software Engineering, E. B. Johnsen and           https://doi.org/10.1145/3656413
[35] A. Beg, D. O’Donoghue, and R. Monahan, “Evaluating llm-generated           [55] Moonshot AI. (2026) moonshotai/kimi-k2.6. [Online]. Available:
     acsl annotations for formal verification,” 2026. [Online]. Available:           https://huggingface.co/moonshotai/Kimi-K2.6
     https://arxiv.org/abs/2602.13851                                           [56] Qwen Team, “Qwen3.6-27B: Flagship-level coding in a 27B dense
[36] G. Wu, W. Cao, Y. Yao, H. Wei, T. Chen, and X. Ma, “Llm meets                   model,” April 2026. [Online]. Available: https://qwen.ai/blog?id=qwen3.
     bounded model checking: Neuro-symbolic loop invariant inference,”               6-27b
     in Proceedings of the 39th IEEE/ACM International Conference on            [57] Y. Charalambous, “Mislabeled equivalent pairs in EqBench-C,” Issue
     Automated Software Engineering, ser. ASE ’24. New York, NY, USA:                #15, shrBadihi/EqBench GitHub repository, 2026, https://github.
     Association for Computing Machinery, 2024, p. 406–417. [Online].                com/shrBadihi/EqBench/issues/15.
     Available: https://doi.org/10.1145/3691620.3695014                         [58] Y. Sui and J. Xue, “Svf: interprocedural static value-flow analysis in
[37] W. Cao, G. Wu, T. Xu, Y. Yao, H. Wei, T. Chen, and X. Ma,                       llvm,” in Proceedings of the 25th International Conference on Compiler
     “Clause2inv: A generate-combine-check framework for loop invariant              Construction, ser. CC ’16. New York, NY, USA: Association
     inference,” Proc. ACM Softw. Eng., vol. 2, no. ISSTA, Jun. 2025.                for Computing Machinery, 2016, p. 265–266. [Online]. Available:
     [Online]. Available: https://doi.org/10.1145/3728920                            https://doi.org/10.1145/2892208.2892235
[38] M. Wang, J. Wang, and X. Cheng, “Bali: Branch-aware loop invariant         [59] Y. Padioleau, J. Lawall, R. R. Hansen, and G. Muller, “Documenting
     inference with large language models,” 2025. [Online]. Available:               and automating collateral evolutions in linux device drivers,” in
     https://arxiv.org/abs/2601.00882                                                Proceedings of the 3rd ACM SIGOPS/EuroSys European Conference
[39] Y. Su, T. Bu, Q. Yang, Y. Ci, and E. Tian, “Cill: Cti-guided invariant          on Computer Systems 2008, ser. Eurosys ’08. New York, NY, USA:
     generation via llms for model checking,” 2026. [Online]. Available:             Association for Computing Machinery, 2008, p. 247–260. [Online].
     https://arxiv.org/abs/2602.23389                                                Available: https://doi.org/10.1145/1352592.1352618
[40] D. Banerjee, O. Bouissou, and S. Zetzsche, “Dafnypro: Llm-assisted
     automated verification for dafny programs,” 2026. [Online]. Available:
     https://arxiv.org/abs/2601.05385
[41] G. Poesia, C. Loughridge, and N. Amin, “dafny-annotator: Ai-
     assisted verification of dafny programs,” 2024. [Online]. Available:
     https://arxiv.org/abs/2411.15143
[42] Álvaro Silva, A. Mendes, and R. Martins, “Inferring multiple
     helper dafny assertions with llms,” 2025. [Online]. Available:
     https://arxiv.org/abs/2511.00125
[43] A. Wei, T. Sun, T. Suresh, H. Wu, K. Wang, and A. Aiken,
     “Quokka: Accelerating program verification with LLMs via invariant
     synthesis,” 2026. [Online]. Available: https://openreview.net/forum?id=
     R57hlMlpkm
[44] A. Solar-Lezama, “Program synthesis by sketching,” Ph.D. dissertation,
     University of California, Berkeley, 2008.
[45] P. Garg, D. Neider, P. Madhusudan, and D. Roth, “Learning invariants
     using decision trees and implication counterexamples,” in Proceedings
     of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles
     of Programming Languages, ser. POPL ’16. New York, NY, USA:
     Association for Computing Machinery, 2016, p. 499–512. [Online].
     Available: https://doi.org/10.1145/2837614.2837664
[46] S. Padhi, R. Sharma, and T. Millstein, “Data-driven precondition
     inference with learned features,” in Proceedings of the 37th
     ACM SIGPLAN Conference on Programming Language Design and
     Implementation, ser. PLDI ’16. New York, NY, USA: Association
     for Computing Machinery, 2016, p. 42–56. [Online]. Available:
     https://doi.org/10.1145/2908080.2908099
[47] X. Si, H. Dai, M. Raghothaman, M. Naik, and L. Song, “Learning loop
     invariants for program verification,” in Advances in Neural Information
     Processing Systems, S. Bengio, H. Wallach, H. Larochelle, K. Grauman,
     N. Cesa-Bianchi, and R. Garnett, Eds., vol. 31. Curran Associates,
     Inc., 2018. [Online]. Available: https://proceedings.neurips.cc/paper
     files/paper/2018/file/65b1e92c585fd4c2159d5f33b5030ff2-Paper.pdf
[48] I. Beer, S. Ben-David, C. Eisner, and Y. Rodeh, “Efficient detection of
     vacuity in actl formulas,” in Computer Aided Verification, O. Grumberg,
     Ed. Berlin, Heidelberg: Springer Berlin Heidelberg, 1997, pp. 279–290.
[49] B. H. Liskov and J. M. Wing, “A behavioral notion of subtyping,”
     ACM Trans. Program. Lang. Syst., vol. 16, no. 6, p. 1811–1841, Nov.
     1994. [Online]. Available: https://doi.org/10.1145/197320.197383
[50] R. Back and J. von Wright, Refinement Calculus - A Systematic
     Introduction, ser. Graduate Texts in Computer Science. Springer,
     1998. [Online]. Available: https://doi.org/10.1007/978-1-4612-1674-2
[51] S. Badihi, Y. Li, and J. Rubin, “Eqbench: A dataset of equivalent and
     non-equivalent program pairs,” in 2021 IEEE/ACM 18th International
     Conference on Mining Software Repositories (MSR), 2021, pp. 610–614.
[52] A. Wei, J. Cao, R. Li, H. Chen, Y. Zhang, Z. Wang, Y. Liu, T. S. F. X.
     Teixeira, D. Yang, K. Wang, and A. Aiken, “EquiBench: Benchmarking
     large language models’ reasoning about program semantics via
     equivalence checking,” Suzhou, China, pp. 33 868–33 881, Nov. 2025.
     [Online]. Available: https://aclanthology.org/2025.emnlp-main.1718/
[53] M. Patnaik, “A repository dedicated for problems related to verification
     of programs using the tool Frama-C,” https://github.com/manavpatnaik/
     frama-c-problems, 2020, accessed: 2026-06.
[54] Anthropic. (2026, 5) Introducing claude opus 4.8. [Online]. Available:
     https://www.anthropic.com/news/claude-opus-4-8
