                                                              Untrusted Authors, Trusted Answers
                                                                          A Calculus of Fidelity-Graded Translations
                                                                                                Christoph Kirsch
                                                                                         University of Salzburg, Austria
                                                                                   Czech Technical University, Prague, Czechia
                                                                                             ck@cs.uni-salzburg.at

                                         Abstract                                                                   use

                                         To answer a question about a program, move the program                            ask        route + check            decide      answer + evidence
                                         to where the question is decidable. Every such move is a                                     declarations
                                         translation, and every translation is a place to be wrong. We
                                                                                                                          demand                 registry + books
                                         study translation as a graph — many languages, a few reason-                                                                              declarations
                                                                                                                    evolution
                                         ing targets, independently built routes of honestly different
                                         trustworthiness — and give it a calculus: pairs of languages                     recommend         register (human)        build + gate      ratchet
                                         close commuting squares that are directional (exactness is
                                         the identity-embedding special case of over-approximation),            Figure 1. The two planes, meeting in one data structure.
                                         checkable per program, and composable, a route’s contract              The use plane reads the registry’s declarations and pro-
arXiv:2607.14137v2 [cs.PL] 17 Jul 2026




                                         being the componentwise meet of its hops’ contracts — assur-           duces evidence-carrying answers; the evolution plane turns
                                         ance class, direction, kept observables, measured cost. One            recorded demand into new declarations, gated and ratcheted,
                                         asymmetry organizes trust: witness-carrying answers are                with registration a human act. Answers never write; growth
                                         self-certifying by replay at the source; universal answers are         never answers.
                                         where grades, independent branches, and re-checked certifi-
                                         cates earn their cost. The compositional core, lax telescope
                                         included, is mechanized in Lean 4.                                     or to validate each of its runs [19, 26, 30]. Both are statements
                                            hurdy-gurdy implements the calculus as two planes meet-             about a single edge.1
                                         ing in one registry. The use plane reads declarations and                 This paper is about the graph: several source languages,
                                         produces evidence-carrying answers; its builders and its in-           a few solver-facing targets, more than one way to get from
                                         tended player are both LLMs, untrusted by construction.                here to there — and, crucially, edges of honestly different
                                         The evolution plane grows the graph: unmet questions are               trustworthiness. A rule-for-rule logic translator is foresee-
                                         recorded as demand, pairs are recommended by evidence and              able from its specification; an optimizing C compiler is only
                                         registered by humans, and a ratchet keeps every prior ver-             pinned; two translators derived independently from a prose
                                         dict standing. Answers never write; growth never answers. Run          manual and a formal model are neither proved — but their
                                         indefinitely, the loop converges on every reducibly decidable          independence is itself a resource. A theory of the graph must
                                         question, at fidelity that only rises. We measure the July 2026        let each edge say what it actually guarantees, compose those
                                         snapshot — per-construct conjoined coverage, dual-route                statements honestly, and let weak edges corroborate one
                                         branch agreement for two ISAs, source-level witness replay,            another into strong routes. Its stance is that of distributed
                                         certified unreachability re-validated by a formally verified           systems: a translator is a component that fails, and failure is
                                         checker, escape rates for the gate itself — and report the             contained — by declared loss, decidable checks, and indepen-
                                         defects the architecture caught in its own authors’ work.              dent routes — not prevented by universal proof.
                                                                                                                   Two directions, two planes. This work is as much an ex-
                                                                                                                periment about who can build and use such a system as about
                                                                                                                the system itself, and its two directions are the platform’s
                                         1   Introduction                                                       two planes (Figure 1). On the use plane, LLMs are supported:
                                         To answer a question about a program, move the program                 the intended player is an LLM that chooses questions and
                                         to where the question is decidable. A C program’s reachabil-           routes but can take no unchecked step — every move is de-
                                         ity question becomes a bit-vector model-checking problem;              terministic, graded, cross-checked, and, for witness-carrying
                                         a Python function’s assertion becomes a linear-arithmetic              answers, self-certifying at the source (a first controlled exper-
                                         query; a chemical reaction network’s coverability question             iment: §6.8). On the evolution plane, LLMs are utilized: every
                                         becomes an SMT unrolling. Every such move is a translation,            pair was implemented by an independent LLM agent from a
                                         and every translation is a place to be wrong. The classical            1 Code, evidence, and the Lean mechanization: https://github.com/
                                         responses are to prove the translator once and for all [16, 18],       cksystemsgroup/hurdy-gurdy — this version is tag arxiv.2.
                                                                                                            1
                                                                                                                         Christoph Kirsch


one-page brief, largely unsupervised, with the architecture’s                                   sail

cross-checks as the only semantic gate (§6.6 reports what
the gate caught) — and the plane is instrumented end to                     C           riscv             btor2               smtlib
end: unanswerable questions are diagnosed and recorded as
demand, pairs are recommended by evidence before a human
registers them, and the ratchet (Theorem 5.2) keeps every                                   sat model → carry back → replay

prior verdict standing (§5.3). Run indefinitely, this loop is
a semi-algorithm for answerability: in the limit it reaches           Figure 2. One run down the spine. The question travels
every reducibly decidable question, at fidelity that only rises       C→RISC-V→BTOR2→SMT-LIB (RISC-V reaching BTOR2
— and it is not an oracle: undecidability, the adequacy floor,        twice, the manual-derived and Sail-derived branches whose
and the finite supply of independent semantic anchors stand           agreement corroborates both); a sat model is carried back
at every graph size (Sections 2 and 8).                               hop by hop and replayed in the source-side interpreter — the
                                                                      answer’s evidence, not the solver’s say-so (Theorem 3.17).
   Provenance disclaimer. All of hurdy-gurdy — frame-
work, interpreters, pairs, solver plumbing, evaluation har-
ness, Lean mechanization — is LLM-generated code (Claude                    universal transfer across over-approximation (Theo-
Opus and Claude Fable agents), and most of this paper’s text                rem 3.11).
is LLM-generated too; no human reviewed either for seman-                 • The contract algebra: composition as one component-
tic correctness. The human contribution is the architecture:                wise meet across assurance, direction, loss, and cost
the calculus, the contracts, and the decisions about what                   — its logical coordinates (class and direction) mech-
to build and claim. Every quantitative claim in Section 6                   anized in Lean 4 with the rest of the compositional
regenerates from the artifact by one script, and the mecha-                 core, lax telescope included (§3.8); loss composes by
nization’s axiom audit re-runs at every build — the reader                  declared keep-sets, cost by measurement.
need not trust the writers, human or otherwise, beyond what               • The existential/universal asymmetry as an architec-
the thesis itself requires.                                                 tural principle, with its end-to-end theorems (§3.7).
   This paper. The unit is the pair (Section 3): two languages,           • The two-plane architecture and its economy: de-
a pure translator, shared pure interpreters, and a pure target-             mand books, evidence-backed recommendation,
to-source interpreter carrying target behaviors back to source              human-valved registration, and the ratchet — the
vocabulary. These close a commuting square that is direc-                   untrusted-generator stance extended from building
tional — exactness is the identity-embedding special case                   pairs to choosing them (§5.3).
of over-approximation — and decidable per program: run                    • A measured, LLM-built instantiation: conjoined cov-
both sides, compare under the declared projection, and a                    erage, dual ISA branches with disjoint decision stacks,
failure names its step and observable. Squares paste (under                 a compliance-derived benchmark, witness replay, cer-
a one-line congruence condition on what carry-backs may                     tified unreachability at up-to-megabyte scale under
read), and composition is told once: a pair’s contract — as-                a formally verified checker, gate escape rates, a first
surance class, direction, kept observables, measured cost —                 LLM-player experiment, and the defects caught (Sec-
composes along a route by the componentwise meet, the                       tions 4 and 6).
weakest hop on every axis at once (Section 3.5). Two mecha-              This document is a dated capability snapshot (July 2026)
nisms move trust where the meet says it cannot go — per-run           of a system whose coverage ratchets monotonically by con-
re-establishment by inline checking, and corroboration by             struction; every number in Section 6 regenerates from the ar-
independently derived branches whose declared semantic                tifact, and the appendix — detailed proofs and the construct-
artifacts are disjoint — and one asymmetry caps the story: ex-        inventory catalog — follows the bibliography.
istential answers are self-certifying by replay (Theorem 3.17),
while universal answers are exactly where grades, branches,           2   Overview: one question, one growth step
and certificates earn their cost (Theorem 3.18). Section 4 de-        Consider a small C program: a loop over an array with an
scribes the platform — 13 languages, 15 registered pairs (13          index computation, and a question — can x == 42 hold at the
in the evaluated snapshot), two reasoning hubs — Section 5            failure label? Figure 2 draws the route this question takes;
its economy and books, and Section 6 measures both.                   we narrate it, then one growth step, and Section 3 makes the
  Contributions.                                                      definitions precise.
    • A calculus of directional, fidelity-graded translation             The spine. The program first moves from C to RISC-V.
      pairs: per-program decidable squares with localization,         The translator on this edge is a pinned C compiler: a digest-
      pasting under an explicit support condition, exactness          locked gcc with recorded flags. We can replay it bit-for-bit,
      as the identity-embedding case (Theorem 3.10), and              but nobody can foresee or prove its output — its honest grade
                                                                  2
Untrusted Authors, Trusted Answers


is reproducible, determinism without meaning. The RISC-                 replays them — itself differentially tested against an indepen-
V program then moves to BTOR2, a bit-vector transition-                 dently generated ISA simulator — remains to be believed.
system logic that model checkers consume, and from there                  Had the solver answered unsat, no replay could vouch
across a rule-for-rule bridge to SMT-LIB, where bit-vector              for it. That is where the grades, the branch agreement, the
solvers decide the reachability query.                                  multi-engine corroboration, and the independently checked
   Each of these moves is a pair: translator, source interpreter,       certificates carry the weight (Theorem 3.18) — and where
target interpreter, and a target-to-source interpreter that             the platform spends its assurance budget.
carries behaviors backwards. When the RISC-V-to-BTOR2
translator runs, the platform can immediately check it on                  Beyond one spine. Nothing above is specific to C or RISC-
this very program: interpret the RISC-V program directly                V (Figure 3 draws the full registry graph). The same square
(the left edge of a square), interpret the BTOR2 translation            contract admits eBPF, Wasm, and EVM programs into the
and carry the resulting trace back to RISC-V observables                BTOR2 hub; Python functions and chemical reaction net-
(the other three edges), and compare, step by step, on the              works reach the SMT-LIB hub directly; a SMILES molecular
declared observables — program counter, registers, halt flag.           graph reaches a molecular-formula target with no solver at
That check passing is what the edge’s checked grade means.              all (a compile pair — the calculus does not care that the lan-
Note carefully what it covers: every hop from the compiled              guages are far from computation, only that both have defined
binary onward. The C hop itself has no square — there is no             meaning). Each pair declares what it preserves (its projec-
C interpreter and no ISA-to-C carry-back — so the verified              tion), what it rejects (typed, enumerable unsupported), and
portion of the route begins at the binary; the pinned com-              its grade; the registry composes routes and reports each
piler contributes reproducibility, re-checked separately by a           route’s composed coverage, grade, and loss.
corpus-level differential against an independent C verifier                One growth step. Now ask the platform something it
(Section 4).                                                            cannot do: is this RISC-V program’s loop live — does it always
   The branch. RISC-V reaches BTOR2 twice. One transla-                 eventually make progress? The diagnosis (gurdy why-not)
tor was written against the prose ISA specification; a second           walks its obstacles in order and stops at the third: routes
route factors through Sail, deriving its semantics from the             exist, the observables survive, but no registered reasoning
official RISC-V Sail model. On the segment where they di-               language expresses a liveness shape. The failure is recorded
verge — from RISC-V to BTOR2 — the two routes share no                  in the platform’s books — the question verbatim, the obstacle,
translator and no carry-back; below the reconvergence they              the generation target it names (a liveness-to-safety reduction
share the hub bridge, so it is the diverse prefix that agreement        on the bit-level hub, or a new temporal hub), an origin tag —
corroborates (§3.6). The platform runs the question down                and the recommendation board aggregates it beside every
both, and the answers must agree. If they do, two indepen-              other unmet demand. A generator drafts the brief citing
dently derived encodings of RISC-V semantics corroborate                those records; a human reads the evidence and registers, or
each other — evidence strictly stronger than either route’s             declines; a builder agent implements against the contract; the
own grade (Theorem 3.16). If they disagree, at least one route          gate admits or rejects; the ratchet keeps every prior verdict
has a defect, and the per-hop squares localize it: which hop,           standing; the question is re-asked. That is one turn of the
which step, which observable (Theorems 3.8 and 3.15). The               evolution plane, and no step of it answered a question or
same dual-route structure exists for AArch64 (Arm manual                was answered by one — answers never write; growth never
vs. Arm Sail model).                                                    answers. The rest of the paper makes each of these words
                                                                        precise, then measures the system.
   The answer comes home. Suppose the SMT solver an-
swers sat: the label is reachable, with a model. The model is              The graph in the limit. Nothing above says the graph
not the answer the user asked for — it is a valuation of SMT            is finished — the architecture is built so that it never has to
variables. The route’s carry-backs now run in reverse: the              be. When a question is unanswerable, exactly one of four
SMT model becomes a BTOR2 witness, the witness a RISC-V                 obstacles fails first, each named by one shipped call (gurdy
trace, the trace an initial memory and register state — con-            why-not): no route reaches a reasoning language; a route ex-
cretely, the inputs of the original C program. The platform             ists but some hop’s declared loss discards the observable the
then replays those inputs in the route’s source-side inter-             question reads; no registered reasoning language expresses
preter — for this spine, the shared RISC-V interpreter on the           the question’s shape; or the solver exhausts its budget. The
compiled binary, the question’s observable read at the ISA              diagnosis names the missing pair; the demand is recorded in
level (§3.5) — and watches the failure state actually happen.           the platform’s books and aggregated into recommendations
At that moment the user’s trust obligations collapse: even if           (§5.3); and that makes a loop well-defined: generate the rec-
every translator, both routes, and the solver were wrong, the           ommended pair, gate it, ratchet, re-ask. We leave the closed-
replayed run exhibits the behavior (Theorem 3.17). Witness-             loop composition as a concept — its stages are shipped, tested
carrying answers are self-certifying; only the interpreter that         calls, and no autonomous run is claimed or evaluated here —
                                                                    3
                                                                                                                             Christoph Kirsch


but its limit clarifies what the platform is for. The answerable        the simulation half (over); nothing else is admitted. This is
set is the closure of a source language’s questions under the           the right notion for near-structure-preserving translation
registered reductions; it only grows (Theorem 5.2); and any             and the wrong one for optimizing compilation, whose home
question that some finite chain of sound, deterministic reduc-          is full simulation over retimed structure — accordingly the
tions can bring to a mechanized decision procedure is even-             one optimizing hop in the instantiation carries no square at
tually answered, with quantified trust. For a fixed finite-state        all, and C’s non-functional official semantics enters through
program — the compiled binary above — every question over               a determinized fragment, policed differentially (Section 4).
kept observables is decidable in principle, so growth for a                A program here is a closed configuration: free inputs, when
given program is a matter of question shapes (new reasoning             present, are part of 𝑝 (a program together with an input
hubs) and of cost (abstraction pairs, §3.4), not connectivity.          valuation). Open programs — programs quantified over their
Trust grows on a separate axis — an added route answers no              inputs — enter the square through their closing valuations
new question; it corroborates (§3.6) — and saturates at the             (Theorem 3.5 quantifies over them) and take center stage in
supply of independent semantic anchors, which no generator              §3.7, where a solver decides over all inputs and a witness
enlarges. Undecidability and interpreter adequacy (Assump-              closes one.
tion 1) stand at every graph size: the limit is not an oracle
                                                                        Definition 3.2 (Interpreter). An interpreter for 𝐴 is a com-
but the reflection of everything mechanized deciding knows
                                                                        putable partial function 𝐼𝐴 : Prog𝐴 ⇀ Beh𝐴 that is pure: iden-
how to answer, behind one interface, with every answer’s
                                                                        tical input yields byte-identical output, on every host (the
trust itself measured. The artifact’s POTENTIAL.md develops
                                                                        contract; §6.9 enforces it by twice-and-diff on the evaluation
the limit and its boundaries in full.
                                                                        host). Outside its domain it fails with a typed unsupported
                                                                        verdict naming the construct; dom(𝐼𝐴 ) is 𝐴’s covered frag-
3     The machine: a calculus of pairs and its
                                                                        ment.
      guarantees
This section is the whole use plane, in the introduction’s              Assumption 1 (Interpreter adequacy). 𝐼𝐴 (𝑝) = ⟦𝑝⟧𝐴 for all
order: languages, behaviors, and projections (§3.1); the di-            𝑝 ∈ dom(𝐼𝐴 ).
rectional commuting square (§3.2); composition — pasting,                  Adequacy is an assumption, not a theorem, and we keep it
and the contract meet (§3.3, §3.5); the direction axis at work          visible: the irreducible residue in every trusted-base compu-
(§3.4); trust beyond the meet — re-establishment, branches,             tation of §3.6, discharged empirically by differential testing
and the trusted-base ledger (§3.5, §3.6); the end-to-end asym-          against independently produced oracles (Section 4; Python is
metry (§3.7); and the mechanization (§3.8). Coverage and                the honest exception — its pinned runtime is both semantics
the ratchet are evolution-plane machinery and live with the             and interpreter).
economy (§5.2).
                                                                        Definition 3.3 (Projection). A projection over 𝐴 is a subset
3.1   Languages, behaviors, projections                                 𝜋 ⊆ 𝐹𝐴 . It lifts to states by restriction, 𝜋 (𝜎) = 𝜎 ↾𝜋 , and to
Definition 3.1 (Language). A language 𝐴 is a triple                     behaviors pointwise, 𝜋 (𝜎1 · · · 𝜎𝑛 ) = 𝜋 (𝜎1 ) · · · 𝜋 (𝜎𝑛 ) (in par-
(Prog𝐴 , 𝐹𝐴 , ⟦·⟧𝐴 ) where Prog𝐴 is a decidable set of pro-             ticular, projected behaviors of different lengths are unequal).
grams; 𝐹𝐴 is a finite set of named observable fields, each              Write 𝑏 ≡𝜋 𝑏 ′ for 𝜋 (𝑏) = 𝜋 (𝑏 ′ ).
𝑓 ∈ 𝐹𝐴 with a value domain 𝑉𝑓 ; and ⟦·⟧𝐴 : Prog𝐴 ⇀ Beh𝐴                 3.2   Pairs and the directional square
is the reference semantics, a partial function into behav-
iors. AnÎ observable state is a total map 𝜎 ∈ Obs𝐴 , where              Definition 3.4 (Pair). A pair 𝑃 : 𝐴 → 𝐵 is a tuple
Obs𝐴 = 𝑓 ∈𝐹𝐴 𝑉𝑓 ; a behavior is a finite sequence of observ-            (𝐴, 𝐵,𝑇 , Λ, 𝜋𝑃 , 𝑑𝑃 ) where 𝑇 : Prog𝐴 ⇀ Prog𝐵 is the trans-
                                                                        lator; Λ : Beh𝐵 ⇀ Beh𝐴 is the target-to-source interpreter,
able states, Beh𝐴 = Obs𝐴∗ , recorded post-step: the 𝑖-th state
                                                                        which re-expresses a target behavior as a source behavior;
is the observable state after the 𝑖-th transition.
                                                                        𝜋𝑃 ⊆ 𝐹𝐴 is the pair’s declared projection — exactly the source
   The only admission criterion for a language is that ⟦·⟧𝐴 is          observables it promises to preserve; and 𝑑𝑃 ∈ {exact, over}
definable — an ISA manual, a logic’s model theory, a reaction-          is its declared direction. An over (over-approximating) pair
network semantics, and a molecular-graph notation all qual-             additionally ships a pure witness embedding 𝑊 , mapping
ify. Nothing in this section assumes languages are executable           each closing valuation 𝑥 of a source program 𝑝 to a clos-
or even computational.                                                  ing valuation 𝑊 (𝑝, 𝑥) of 𝑇 (𝑝); for an exact pair, 𝑊 is the
   The scope, stated plainly: behaviors are finite and the refer-       identity. 𝑇 , Λ, and 𝑊 are pure (as in Theorem 3.2); 𝐼𝐴 and
ence semantics is a function — nondeterminism, divergence,              𝐼𝐵 are owned by the languages and shared by every pair
and reactive I/O are outside. Behavior inclusion is inside in           that touches them. The pair’s domain dom(𝑃) is the set
exactly one controlled form: the square is a directional claim          of 𝑝 with 𝑝 ∈ dom(𝐼𝐴 ) ∩ dom(𝑇 ), 𝑇 (𝑝) ∈ dom(𝐼𝐵 ), and
(Theorems 3.4 and 3.5), checked as a projected trace equality           𝐼𝐵 (𝑇 (𝑝)) ∈ dom(Λ). Like the projection, the direction is a
along a declared witness embedding — two-sided (exact) or               declared, protected part of the contract.
                                                                    4
Untrusted Authors, Trusted Answers


Definition 3.5 (Faithfulness: the directional square). 𝑃 is            because the correspondence it encodes is pair-specific; it is
faithful at 𝑝 ∈ dom(𝑃) when its square commutes at 𝑝 along             also why the square’s oracle is as expressive as the translator
the witness embedding: for every closing valuation 𝑥 of 𝑝,             it checks.
       𝜋𝑃 𝐼𝐴 (𝑝 (𝑥)) = 𝜋𝑃 Λ(𝐼𝐵 ( 𝑇 (𝑝) (𝑊 (𝑝, 𝑥)) )) ,                 Example (One square, run — and failing). The JAL probe of
                                                   
                                                                       the RV64IMC inventory (Theorem 5.1) is a two-instruction
where a closed program has the single trivial valuation. For
                                                                       program whose taken jump leaves the code image:
an exact pair (𝑊 = id) this is the familiar commuting square
                                                                               0x0:       jal x1, 8   ; link x1 := 4, jump to 0x8
𝜋𝑃 (𝐼𝐴 (𝑝)) = 𝜋𝑃 (Λ(𝐼𝐵 (𝑇 (𝑝)))):
                                                                               0x4:       ecall       ; (jumped over)

                      𝑝
                              𝑇
                                        𝑇 (𝑝)                          The left leg runs the shared RISC-V interpreter 𝐼𝐴 ; the right
                                                                       leg translates to BTOR2, interprets, and carries the trace back,
                 𝐼𝐴                         𝐼𝐵
                                                                       compared under 𝜋 ⊇ {pc, x1, halted}. The square is exact
                            ≡𝜋𝑃
                 𝐼𝐴 (𝑝)              Λ(𝐼𝐵 (𝑇 (𝑝)))                     (𝑊 = id) — as is every registered pair’s but the abstraction
                                                                       endo-pairs’ (§3.4). Post-step states, with the right leg as the
𝑃 is faithful on 𝐶 ⊆ dom(𝑃) when it is faithful at every               riscv-btor2 translator emitted them at version 0.1:
𝑝 ∈ 𝐶.                                                                             step     field            𝐼𝐴 (𝑝 )   Λ(𝐼𝐵 (𝑇 (𝑝 ) ) )
   The direction is the reading of that equality. The embed-                          0     pc, x1, halted   8, 4, F   8, 4, F
ding selects which target valuations the square checks: ex-                           1     pc, x1           8, 4      8, 4
actly those in its range. When 𝑊 is the identity — surjective                               halted           T         F
onto the closing valuations of 𝑇 (𝑝) — every target valua-             Address 0x8 matches no instruction: the reference semantics
tion is checked and the target has no behaviors beyond the             halts on the fetch miss; the translator had modeled only the
source’s kept ones: the square is two-sided, a bisimulation on         instructions. The oracle reports (𝑖, 𝑓 ) = (1, halted) and, run
the kept observables, and that is all 𝑑𝑃 = exact asserts. When         hop by hop (Theorem 3.8), indicts the riscv-btor2 hop —
𝑊 is not surjective, the target valuations outside its range           incident I21 (§6.6), caught by the first conjoined coverage run
are the pair’s added behaviors — their existence is the point,         in three independently written lowerings the same morning,
not a defect — and the same checked equality asserts only              fixed by a versioned translator bump with the taken-jump
the simulation half, 𝐼𝐴 (𝑝) ⊑𝜋𝑃 Λ(𝐼𝐵 (𝑇 (𝑝))): every source            squares as permanent regressions. The all-pass rows of Ta-
behavior has a target counterpart on the kept observables,             ble 3 are made of exactly such checks.
and the target may have more. Exactness is thus not a sepa-
rate notion but the identity-embedding special case of one             3.3   Pasting: when squares compose
square (Theorem 3.10, machine-checked). The check itself is            Two pairs compose when the middle language is shared:
direction-indifferent — run both legs, compare under 𝜋𝑃 — so           𝑃1 = (𝐴, 𝐵,𝑇1, Λ1, 𝜋1, 𝑑 1 ) and 𝑃2 = (𝐵, 𝐶,𝑇2, Λ2, 𝜋2, 𝑑 2 ) yield
everything below applies to both directions verbatim; only             the candidate composite
what agreement means differs, which is why direction is pro-
                                                                              𝑃2 ◦ 𝑃 1 = (𝐴, 𝐶, 𝑇2 ◦ 𝑇1, Λ1 ◦ Λ2, 𝜋, 𝑑 1 ∧ 𝑑 2 )
tected like the projection: an over square passed off as exact
would launder added behaviors into a meaning-preservation              for a projection 𝜋 ⊆ 𝜋 1 to be determined, with direction the
claim.                                                                 meet on the chain exact > over — a composite is exact iff
   Three remarks. First, everything in Theorem 3.5 is com-             both hops are — witness embedding the composition 𝑊2 ◦𝑊1
putable: faithfulness at a given 𝑝 is a decidable, executable          (an exact hop contributing the identity), and dom(𝑃2 ◦ 𝑃 1 )
check — run both sides, compare under 𝜋𝑃 . We call this check          the evident composite domain. Folklore says the squares
the square oracle; in fault-tolerance terms it is an acceptance        paste. They do not paste for free: 𝑃2 guarantees agreement of
test in the sense of recovery blocks [31], turning a silently          the two 𝐵-behaviors only up to 𝜋2 , and Λ1 consumes whole
wrong — in effect Byzantine — translator into a fail-stop              𝐵-behaviors. If Λ1 reads a 𝐵-field that 𝑃2 discards, the outer
component [37]. Second, when the check fails it fails at a             rectangle can fail while both inner squares hold. The missing
first position: a least step index 𝑖 and a field 𝑓 ∈ 𝜋𝑃 on which       condition is that Λ1 must not look outside what 𝑃 2 preserves:
the two sides differ. The oracle reports (𝑖, 𝑓 ) — a translator
                                                                       Definition 3.6 (Support). Λ1 is (𝜋 2 ⇒ 𝜋)-supported when
(or interpreter, or carry-back) defect, localized to a step and
                                                                       for all 𝑏, 𝑏 ′ ∈ dom(Λ1 ): 𝜋2 (𝑏) = 𝜋2 (𝑏 ′ ) implies 𝜋 (Λ1 (𝑏)) =
a named observable. Third, the projection is part of the con-
                                                                       𝜋 (Λ1 (𝑏 ′ )). Equivalently: 𝜋 ◦ Λ1 descends to a well-defined
tract, not a tuning knob: 𝜋𝑃 states what “preserves meaning”
                                                                       map on 𝜋2 -equivalence classes — a congruence condition,
promises for this pair, and 𝐹𝐴 \ 𝜋𝑃 — the pair’s loss — states
                                                                       matching the mechanization exactly.
what it does not.
   The carry-back Λ is what makes a target-side result mean            Theorem 3.7 (Pasting). Let 𝑝 ∈ dom(𝑃 2 ◦ 𝑃1 ), let 𝑃1 be
something at the source: a solver counterexample or a target           faithful at 𝑝, let 𝑃2 be faithful at 𝑇1 (𝑝), let 𝜋 ⊆ 𝜋 1 , and let Λ1
trace is re-expressed as a source behavior. It is pair-specific        be (𝜋 2 ⇒ 𝜋)-supported. Then the composite 𝑃 2 ◦ 𝑃 1 is faithful
                                                                   5
                                                                                                                            Christoph Kirsch


at 𝑝 with respect to 𝜋, along the composed embedding 𝑊2 ◦𝑊1                 observable. It is also what disagreement between routes will
and with direction 𝑑 1 ∧𝑑 2 ; for the exact–exact instance, writing         lean on in §3.6.
𝑟 = 𝑇2 (𝑇1 (𝑝)),
                                                                               Routes, and the contract algebra. The registry of lan-
                 𝜋 (𝐼𝐴 (𝑝)) = 𝜋 Λ1 (Λ2 (𝐼𝐶 (𝑟 ))) .
                                                   
                                                                            guages and pairs forms a directed multigraph; a route 𝑅 :
                                                                            𝐴 → 𝑍 is a path through it, with composed translator
Proof. Write 𝑞 = 𝑇1 (𝑝). Then 𝜋 (𝐼𝐴 (𝑝)) = 𝜋 (Λ1 (𝐼𝐵 (𝑞)))
                                                                            𝑇𝑅 , composed carry-back Λ𝑅 , composed projection keep(𝑅),
since 𝜋 ⊆ 𝜋1 and 𝑃 1 is faithful at 𝑝. Faithfulness of 𝑃2
                                                                            composed direction and embedding as above, and faithful-
at 𝑞 gives 𝜋2 (𝐼𝐵 (𝑞)) = 𝜋2 (Λ2 (𝐼𝐶 (𝑟 ))), so the support
                                                                            ness given by iterating Theorem 3.7. Composition, told once:
condition applies to the two 𝐵-behaviors and yields
                                                                            a pair’s composable declaration is its contract — the assur-
𝜋 (Λ1 (𝐼𝐵 (𝑞))) = 𝜋 (Λ1 (Λ2 (𝐼𝐶 (𝑟 )))). Chain the equalities.
                                                                            ance class of its guarantee (Theorem 3.12) paired with its
For the directional form, run the same chain per closing valu-
                                                                            direction, alongside the keep-set and the measured cost —
ation, the legs closed at 𝑥, 𝑊1 (𝑝, 𝑥), and 𝑊2 (𝑇1 (𝑝),𝑊1 (𝑝, 𝑥));
                                                                            and a route’s contract is the componentwise meet, the weakest
mechanized as lax_pasting and, telescoped over routes
                                                                            hop on every axis at once, with nothing stronger entailed
with the direction meet, DRoute.lax_route_pasting
                                                                            (Contract.comp_glb, machine-checked; the semantic con-
and DRoute.direction_exact_iff (§3.8). (Details: Sec-
                                                                            tent of each coordinate is Theorem 3.7 with Theorem 3.13,
tion A.)                                                        □
                                                                            and Theorem 3.11). Purity composes too, and gives caching:
   The support condition is not decorative. Take 𝐹𝐵 = {𝑔, ℎ}
                                                                            Proposition 3.9 (Determinism and caching). If every com-
with 𝜋2 = {𝑔}, and let Λ1 copy field ℎ into a 𝜋1 -kept source
                                                                            ponent function of every hop of 𝑅 is pure, then 𝑇𝑅 and Λ𝑅 are
field: 𝑃2 can be faithful — it preserves 𝑔 — while Λ2 (𝐼𝐶 (𝑟 ))
                                                                            pure, and a content-addressed cache keyed by the input hash
differs from 𝐼𝐵 (𝑞) on ℎ, which 𝜋2 permits. The outer rectangle
                                                                            and the component versions returns, on a hit, exactly what
then fails on the copied field although both inner squares
                                                                            recomputation would return — across the whole route. If some
commute.
                                                                            hop is impure, re-running the route on the same input and
   Composed keep and loss. In the implementable special                     diffing bytes at every hop (twice-and-diff) can detect it and
case — Λ1 fieldwise and step-aligned, each source field 𝑓                   localize it to the first hop whose bytes differ — a sound but
computed from a dependency set deps(𝑓 ) ⊆ 𝐹𝐵 of target                      incomplete detector: two coinciding runs of an impure hop pass.
fields — the support condition has a syntactic reading, and
the largest 𝜋 satisfying Theorem 3.7 is                                     3.4   The direction axis: abstraction as a pair
                                                                            Every square so far shown ran exact, and most registered
         keep(𝑃2 ◦ 𝑃 1 ) = { 𝑓 ∈ 𝜋 1 | deps(𝑓 ) ⊆ 𝜋2 },
                                                                            pairs do. The over half of Theorem 3.5 earns its place on
a source field survives the route iff 𝑃1 keeps it and it is com-            cost: an abstraction maps a program to a smaller or cheaper
puted only from target fields 𝑃2 keeps. Dually lost(𝑃 2 ◦ 𝑃 1 ) =           model with more behaviors — cut a state variable’s update
𝐹𝐴 \ keep(𝑃2 ◦ 𝑃1 ): route loss is the union of per-hop losses,             and let it range freely, and every source behavior survives
each pulled back along the carry-backs. This is the formal                  while new, spurious ones appear. Such a translation is exactly
content of the platform rule that a route must declare its                  what makes an expensive universal question tractable, and
cumulative loss: the observables a destination can still speak              in this calculus it is not a special mechanism bolted onto a
about are exactly those no hop discarded. (When Λ1 changes                  solver run but an ordinary pair whose declared direction is
step granularity — one source step spanning several target                  over: same oracle, same coverage conjunction (Theorem 5.1),
steps, as in C-to-ISA — the same statement holds with deps                  same ratchet (Theorem 5.2), same negative controls, checked
taken over the spanned window; appendix A.2.)                               along its witness embedding. Two results pin the axis down:
                                                                            exactness is a special case, and universal verdicts transfer.
Corollary 3.8 (Localization). Under the support condition,
if the composite square fails at 𝑝 (both sides defined), then               Proposition 3.10 (Exactness is the identity embedding). Un-
𝑃1 ’s square fails at 𝑝 or 𝑃2 ’s square fails at 𝑇1 (𝑝). Inductively,       der the specialization obligation of Theorem 3.18(iv) — trans-
along a route 𝑅 = 𝑃𝑛 ◦ · · · ◦ 𝑃 1 satisfying the pairwise support          lating the closed instance agrees with closing the one open
conditions, a failing outer rectangle implies a failing inner               translation — a pair with 𝑊 = id is faithful at an open 𝑝 in
square at some hop 𝑖 — and running the square oracle hop                    the sense of Theorem 3.5 iff its two-sided square commutes
by hop finds the least such 𝑖, then the least failing step and              at every closed instance 𝑝 (𝑥). The exact calculus of §3.2–§3.3
field. (The check is direction-indifferent, so this holds along any         is thus the 𝑊 = id fragment of the directional one — lit-
directional route — divergences localize the same way whether               erally: the mechanization derives each side from the other
the failing square’s reading was ≡ or ⊑.)                                   (laxFaithful_id_iff_faithful, axiom-free; §3.8).
  Theorem 3.8 is the debugging story of the whole platform:                 Proof. With 𝑊 = id the two legs close at the same valua-
a divergence anywhere along a route is never a mystery                      tion, and the specialization obligation identifies the closed
about the route; it is an indictment of one hop, one step, one              translation 𝑇 (𝑝 (𝑥)) with the closed instance 𝑇 (𝑝) (𝑥) of the
                                                                        6
Untrusted Authors, Trusted Answers


open artifact; the quantification over valuations is then the           symmetry visible, and its verdict-transfer discipline would
quantification over closed instances.                       □           fall out of the same monotonicity.
                                                                           The mechanization of §3.8 covers the directional calcu-
Proposition 3.11 (Universal transfer across over-approxi-               lus in full: the directional square, pasting along the com-
mation). Let 𝑅 : 𝐴 → 𝑍 have composed direction over and                 posed embedding (binary and telescoped) with the direction
be faithful (Theorem 3.5) on a fragment containing 𝑝, with              meet, and both propositions above are machine-checked
𝜑 over keep(𝑅). If no valuation of 𝑇𝑅 (𝑝) exhibits 𝜑 within             (Calculus/Lax.lean) with the same axiom footprint as the
the declared bounds, then no valuation of 𝑝 does: universal             exact fragment.
verdicts transfer across over-approximation. An existential
verdict does not transfer; it remains subject to the carried-back       3.5   Contracts: grades, classes, and the meet
replay of Theorem 3.17, whose failure on an over route has              A pair declares a fidelity grade from 𝐺 = {trusted,
a second, benign reading — a spurious counterexample, a                 reproducible, checked, predicted, proved } — the evi-
demand to refine the abstraction rather than an indictment of           dence species behind its guarantee: a spec audit that re-derives
a hop.                                                                  the bytes (predicted), an independently re-checked certifi-
Proof. Contrapositive: a valuation 𝑥 with 𝜑 observed in                 cate (proved), this run’s square-oracle verdict (checked), a
⟦𝑝 (𝑥)⟧𝐴 yields, by faithfulness along the composed em-                 digest pin (reproducible), or nothing (trusted). Grades
bedding, the valuation 𝑊𝑅 (𝑝, 𝑥) of 𝑇𝑅 (𝑝) exhibiting 𝜑 on              differ in kind (predicted and proved are incomparable:
the kept observables — present within bounds, contradict-               foreseeable vs. re-checkable); what composition needs is the
ing the premise. (Mechanized: lax_universal_transfer,                   logical form of the guarantee, and that is totally ordered:
§3.8.)                                                   □              Definition 3.12 (Assurance class). The assurance classes
   Together with Theorems 3.17 and 3.18 this closes the CE-             are the chain A : none < replay < perrun < universal, and
GAR loop with durable artifacts: a transferred unreachable              class : 𝐺 → A maps trusted ↦→ none, reproducible ↦→
answers at the source (Theorem 3.11); a reachable either                replay, checked ↦→ perrun, and predicted, proved ↦→
replays (a true counterexample) or is spurious — and the                universal. The classes denote guarantee predicates for a pair
refinement the failure demands is a new registered pair with            𝑃 with covered fragment 𝐶𝑃 : universal — 𝑃 is faithful at
a smaller havoc set, graded and reusable. The artifact in-              every 𝑝 ∈ 𝐶𝑃 ; perrun — 𝑃 is faithful at every 𝑝 on which
stantiates this with the endo-pair btor2-havoc, localization            the square oracle has run and passed (in particular, at the
abstraction on the bit-level hub, its lax square, negative con-         program of the present run); replay — 𝑇 is pure, nothing
trols, and refinement loop in the repository’s gate (a second           about meaning; none — nothing.
over endo-pair, interval abstraction, is registered as a brief);           Only classes compose: a route with one predicted hop
§6.13 measures the loop, on authored systems and on an                  and one proved hop is universal end to end, as it should be.
ingested HWMCC slice.                                                      Two honesty notes on the mapping. First, grade dec-
                                                                        larations are themselves trusted inputs: only checked is
   Advising the dial. The abstraction’s parameters stay the
                                                                        mechanically enforced by the framework (the oracle runs);
player’s, but they need not be guessed. The artifact ships
                                                                        class(predicted) = universal additionally presumes that
an advisor over the bit-level hub: the cone of influence of a
                                                                        the audited specification maps rules to semantics — a
question — rooted in its bad conditions and every environment
                                                                        translator faithful to a wrong rule table is predicted and
constraint (a state gating run validity is never free), closed
                                                                        universally unfaithful, and our own evaluation exhibits a
backwards through the state-evolution supports — splits the
                                                                        predicted edge that was wrong on covered inputs until
state space into a free havoc set, whose abstraction provably
                                                                        a coverage probe caught it (§6.6). Declarations therefore
cannot move the question’s signal, and a refinement ladder
                                                                        sit in the trusted-base ledger like any other component.
ordered farthest-from-the-question first; observed per-state
                                                                        Second, proved as instantiated in §6.5 certifies a per-question
bounds seed candidate intervals that the lax square then
                                                                        verdict — universal over that question’s inputs, per-run over
corroborates or refutes. The free-set claim is executable and
                                                                        questions — not the pair’s square for all programs.
negative-controlled in the artifact’s tests; mechanizing it is
a natural next entry for §3.8’s audit.                                  Proposition 3.13 (Weakest link). Let route 𝑅 = 𝑃𝑛 ◦ · · · ◦ 𝑃1
                                                                        satisfy the support conditions of Theorem 3.7. If every hop’s
  The dual, for symmetry. The axis has an evident third
                                                                        guarantee holds, then the composite guarantee of class
value the platform deliberately does not yet inhabit: an under-
                                                                        min𝑖 class(𝑃𝑖 ) holds for 𝑅 (with 𝐶𝑅 the composite fragment),
approximating square — the embedding running the other
                                                                        and no higher class is entailed by the hop guarantees alone.
way, the target with fewer behaviors — where existential
verdicts would transfer and universal ones would not, the                 The proof is immediate from Theorem 3.12 and Theo-
mirror image of Theorem 3.11. Nothing in this paper depends             rem 3.7: universal statements conjoin into universal state-
on it; we note it because the directional reading makes the             ments over the composite fragment; a per-run statement at
                                                                    7
                                                                                                                       Christoph Kirsch


hop 𝑖 caps the conjunction at the programs the oracle ac-              to the language at which they reconverge), and the diverse
tually saw; a replay hop caps it at purity. Optimality is by           translators are derived from independent semantic artifacts
the evident counterexamples. Statically, then, a route is as           — e.g. RISC-V reaches BTOR2 once via a translator written
faithful as its weakest hop — and this is one instance of the          from the prose ISA specification and once via the Sail formal
paper’s single composition statement: a pair’s composable              model; likewise AArch64 from the Arm manual vs. the Arm
declaration, its contract (assurance class × direction), com-          Sail model.
poses along a route by the componentwise meet, the weakest
hop on every axis at once (mechanized: Contract.comp_glb,
§3.8; the class coordinate is this proposition, the direction
coordinate is Theorem 3.11). The static story is still not the            The assumption’s premise is, moreover, a declared, pro-
whole story, because every pair carries its own oracle:                tected registry fact rather than prose alone: each pair names
                                                                       the semantic artifact its translator derives from, and a me-
Theorem 3.14 (Per-run re-establishment). Fix a run of route
                                                                       chanical judgment (the trust advisor of §5.3) scores every
𝑅 on program 𝑝, with intermediate programs 𝑞 0 = 𝑝, 𝑞𝑖 =
                                                                       branch by the diverse segments’ declared artifacts, the shared
𝑇𝑖 (𝑞𝑖 −1 ). If on this run the square oracle runs and passes at
                                                                       suffix removed — a shared artifact is never independent, an
every hop 𝑖 (on 𝑞𝑖 −1 ), and the support conditions hold, then
                                                                       undeclared one is unknown, never silently independent —
𝑅 is faithful at 𝑝 — regardless of the hops’ static grades. In
                                                                       and states saturation plainly: pairs can be generated with-
particular a reproducible or even trusted hop that is dy-
                                                                       out bound, independent artifacts cannot, and corroboration
namically validated at 𝑞𝑖 −1 contributes, for this run, exactly
                                                                       stops growing at their supply.
what a checked hop contributes.
                                                                          The scoping matters, and independence must be argued,
Proof. Each passed oracle check is faithfulness at 𝑞𝑖 −1 (The-         not assumed. Below the reconvergence, routes may share
orem 3.5 is decidable and the oracle decides it); apply Theo-          hops — in the platform both RISC-V→SMT-LIB routes share
rem 3.7 inductively.                                        □          the BTOR2→SMT-LIB bridge — and shared emission libraries
   Theorem 3.14 applies exactly to hops whose squares run:             are shared failure surface, so agreement corroborates the di-
the pinned C compiler at the spine’s head has no square,               verse prefix and nothing beneath it. The evaluation therefore
so the inline oracles lift the route from the compiled bi-             also runs a disjoint-decision variant of every branch question
nary onward, the compiler contributing reproducible plus               (§6.2, Figure 4): the direct route’s BTOR2 system decided na-
a corpus-level differential against an independent C veri-             tively by btormc, against the Sail-derived route through the
fier (Section 4). Re-establishment is per-run evidence, never          bridge and Z3, so the diverse segment extends through the
a static promotion, and never coverage for a hop with no               decision procedure and the shared bridge drops out of the
oracle.                                                                corroborating pair entirely; what remains shared is the emis-
                                                                       sion library (the site of the cross-route incident below) and
3.6   Branches, diversity, and the trusted base                        the language-owned endpoints. Correlated failures between
The registry graph is not a line: one source may reach one             nominally independent implementations are, moreover, the
destination by several routes. Let 𝑅1, 𝑅2 : 𝐴 → 𝑍 with com-            empirical norm [14]; our own history exhibits both a cross-
posed keep-sets 𝐾1, 𝐾2 and 𝐾 = 𝐾1 ∩ 𝐾2 , sharing the end-              route common-mode failure through a shared emitter and a
point interpreters (language-owned) but no translator or               shared-misreading blind spot (§6.6), and translators written
carry-back.                                                            by LLM agents plausibly share model-family failure modes.
                                                                          Under Assumption 2, the residual failure mode of an agree-
Lemma 3.15 (Disagreement localizes). If 𝑅1 and 𝑅2 disagree             ing branch is a common-mode failure: independently pro-
at 𝑝 under 𝐾, at least one route is unfaithful at 𝑝, and The-          duced encodings of the same semantics, wrong in the same
orem 3.8 pins the failure to a hop, a step, and a field of that        observable way on the same program. We do not assign this
route.                                                                 a probability; we account for it structurally, in the trusted
Lemma 3.16 (Agreement corroborates). If 𝑅1 and 𝑅2 agree                base ledger below. This is how the platform manufactures
at 𝑝 under 𝐾, then either both are faithful at 𝑝 (under 𝐾), or         assurance out of hops that are individually only checked —
both are unfaithful with identical projected error: defects in         dual modular redundancy whose comparator, unlike a voter,
independently built components producing the same wrong                localizes: agreement of independently derived routes is evi-
𝐾-behavior at 𝑝.                                                       dence that neither route’s grade alone provides.
                                                                          Define the trusted computing base TCB(𝑣) of a verdict 𝑣
   Both are immediate: two faithful routes each equal
                                                                       as the set of components whose correctness 𝑣’s soundness
𝐾 (𝐼𝐴 (𝑝)), hence each other. What Theorem 3.16 buys
                                                                       still assumes after all checks that ran. Each cross-check layer
depends on an assumption we state rather than hide:
                                                                       strictly shrinks it (Table 1); the last two rows are not inter-
Assumption 2 (Diversity). Corroborating routes share no                changeable, and the difference is the central asymmetry of
translator or carry-back on the segment where they diverge (up         the whole design.
                                                                   8
Untrusted Authors, Trusted Answers


Table 1. The trusted-base ledger: what each layer of cross-                     Theorem 3.18 (Universal answers need the machinery).
checking removes from the set of components a verdict still                     Suppose the solver returns unreachable (within declared un-
assumes correct.                                                                rolling/step bounds 𝑘). If (i) every hop of 𝑅 is faithful at every
                                                                                instance 𝑝 (𝑥) — the universal-class guarantee on the frag-
Layer that ran             Removed from          Still in TCB                   ment containing 𝑝’s constructs, and exactly the hypothesis
                           TCB                                                  the mechanization takes; (ii) the support conditions of Theo-
bare route + solver        —                     all 𝑇𝑖 , Λ𝑖 , all              rem 3.7 hold and 𝜑 mentions only keep(𝑅); (iii) the verdict is
                                                 interpreters, solver           certified by an independently checked certificate or corrobo-
+ square oracle at every   every 𝑇𝑖              the Λ𝑖 , the                   rated across independent engines; and (iv) the symbolic artifact
hop (Theorem 3.14)                               interpreters, solver
                                                                                the solver consumes denotes the family of closed translations
+ branch agreement         the diverse           shared endpoint
(Theorem 3.16,             prefix’s Λ𝑖 (cross-   interpreters, shared           the squares check — translation commutes with input spe-
Assumption 2)              corroborated)         suffix hops and                cialization, an obligation each reasoning pair discharges by
                                                 emission libraries,            construction of its encoding and, where the encoding carries
                                                 solver; common-mode            free inputs, by sampled commutation tests (§3.8), and under
                                                 residue
                                                                                which the mechanization derives every per-instance transla-
+ independent solver       the single solver     the agreeing engines’
corroboration                                    common failure                 tion from the one open translation the platform actually per-
                                                 modes                          forms (universal_from_open_artifact, §3.8) — then no
+ certificate check        the solver entirely   the certificate checker        input drives ⟦𝑝⟧𝐴 to 𝜑 within 𝑘 steps, with TCB as in the
(proved; e.g. DRAT/LRAT)                         (formally verified, in         corresponding row of the ledger (§3.6).
                                                 the cake_lpr
                                                 instantiation), plus the
                                                 bit-blaster’s BV→CNF
                                                 step
+ source-level witness     everything above      𝐼𝐴 adequacy                       One caution on hypothesis (i): per-run oracle evidence
replay (§3.7)                                    (Assumption 1) + the           combined with branch agreement (Theorem 3.16, Assump-
                                                 replay harness
                                                                                tion 2) raises confidence in it but does not entail it — oracle
                                                                                passes cover the finitely many closures actually run, and
                                                                                agreement bounds the residual failure to common-mode
3.7   The end-to-end asymmetry                                                  rather than excluding it. Universal verdicts are precisely
Finally, what does a user hold at the end? Let 𝑅 : 𝐴 → 𝑍 be                     where the universal tiers earn their keep; evidence below
a route into a reasoning language 𝑍 (one a solver consumes:                     that tier is corroboration, not entailment.
a transition-system logic, an SMT theory). The user asks a                         Direction slots into the same asymmetry monotonically:
question about an open source program 𝑝 (𝑥) — free inputs 𝑥 —                   along an over route a certified unreachable transfers to the
and a condition 𝜑 over keep(𝑅)-observables: is 𝜑 reachable?                     source (Theorem 3.11), while a reachable already rested on
The solver decides at 𝑍 ; its answer comes back in one of two                   the carried-back replay — so the directional calculus adds
logical shapes, and they differ fundamentally in what must                      no new trust obligation, only a second, benign reading of a
be trusted.                                                                     replay failure: a spurious counterexample, the refinement
                                                                                demand of §3.4.
Theorem 3.17 (Existential answers are self-certifying). Sup-                       The asymmetry between Theorems 3.17 and 3.18 is, we
pose the solver returns reachable with witness 𝑤, the com-                      argue, the right lens on the entire design: for questions whose
posed carry-back Λ𝑅 re-expresses 𝑤 as an input valuation 𝑥 0                    answers carry witnesses, trust is nearly free — carry the wit-
(and claimed trace), and replaying 𝐼𝐴 (𝑝 (𝑥 0 )) exhibits 𝜑. Then               ness back and replay it at the source; the platform’s graded
𝜑 is truly reachable in ⟦𝑝⟧𝐴 — with TCB = {Assumption 1                         tiers, branches, and certificates exist for the other half, the
for 𝐼𝐴 } plus the small fixed replay harness the judgment runs                  universal answers where no witness can vouch for the ver-
through (the projection, the 𝜑-evaluator, and the substitution                  dict. This is the end-to-end argument [35] transplanted to
closing 𝑝), and nothing else. Every translator, carry-back, hub                 translation: the check that settles a witness-carrying answer
interpreter, and solver on 𝑅 is a discovery device only: a defect               belongs at the endpoint — the source interpreter — and what
in any of them can cause a missed or non-replaying witness,                     the intermediate hops provide is, for that half, an optimiza-
never a false reachable.                                                        tion; only for universal answers, where no endpoint check
                                                                                can exist, does hop fidelity become the guarantee itself. A
Proof. The replay is a run of 𝐼𝐴 itself on a concrete closed                    system that makes the carry-back Λ a first-class, per-pair
program 𝑝 (𝑥 0 ); by Assumption 1 its behavior is ⟦𝑝 (𝑥 0 )⟧𝐴 ,                 component is a system in which the cheap half of trust is al-
and 𝜑 was observed on it. No other component’s output                           ways cashed in; a system that grades and stacks cross-checks
enters the final judgment.                                  □                   is one in which the expensive half is bought consciously, in la-
                                                                                beled increments, with the bill itemized in the ledger of §3.6.
                                                                            9
                                                                                                                          Christoph Kirsch


3.8   Mechanization                                                    Table 2. The mechanization at a glance: paper result, Lean
The compositional core of Sections 3 and 3.5 is mechanized             theorem, and the proof’s axiom footprint as printed by the
in Lean 4 (core library only, no mathlib; ∼1,250 lines, in             build-time audit (Audit.lean); “—” is axiom-free.
the artifact): the pasting theorem with the support condi-
tion, localization, the assurance-class chain and weakest link         Result               Lean theorem                  Axioms
(sound half), per-run re-establishment, both branch lemmas,            Theorem 3.7          pasting, pasting3             propext
the ratchet (verdict preservation and coverage monotonicity            (pasting)
under extensions), both end-to-end theorems, the special-              Theorem 3.8          localization                  propext,
                                                                                                                          Classical.
ization obligation of Theorem 3.18(iv) — with the theorem                                                                 choice,
that it discharges the per-instance-translation hypothesis                                                                Quot.sound
from the single open translation the platform performs —               Theorem 3.13         weakest_link_universal        propext
and the route telescope — routes of arbitrary length as a              (sound half)
dependently-typed chain of pairs over interpreter-bundled              Theorem 3.14         reestablishment               propext
                                                                       Theorems 3.15        disagreement_localizes,       —
languages, with the paper’s “pairwise support conditions”              and 3.16             agreement_corroborates
as a recursive coherence predicate, and the 𝑛-ary pasting              Theorem 5.2          ratchet_preserves_faithful,   —
and localization theorems proved by induction through the                                   ratchet_coverage_mono
binary ones (the canonical head-projection choice at each              Theorem 3.17         existential_self_certifying   —
junction is shown lossless by a reprojection lemma). Three             Theorem 3.18         universal_needs_machinery     propext
                                                                       Theorem 3.18(iv)     universal_from_               propext
modeling choices mirror the paper exactly. Components are                                   open_artifact
Lean functions, so purity is by construction and Theorem 3.9 is        route telescope      Route.route_pasting, Route.   propext,
definitional; partiality is Option, with unsupported as none;          (𝑛-ary)              route_localization            Quot.sound (+
and projections are generalized from field subsets to arbitrary                                                           Classical.
observable-compression maps, with “𝜋 ⊆ 𝜋 1 ” becoming fac-                                                                choice for
                                                                                                                          localization)
toring. Because every theorem takes each component-output              directional          lax_pasting; telescoped:      propext (+
witness as an explicit hypothesis, a statement’s trusted base          pasting, direction   DRoute.lax_route_pasting,     Quot.sound
is literally its hypothesis list — Theorem 3.17 in Lean assumes        meet                 DRoute.direction_exact_iff    telescoped)
source-interpreter adequacy and nothing else, and its proof            (Theorem 3.7)
term is three tokens:                                                  Theorem 3.10         laxFaithful_id_iff_faithful   —
                                                                       (exactness =
                                                                       identity
                                                                       embedding)
theorem existential_self_certifying
                                                                       Theorem 3.11         lax_universal_transfer        propext
  (adequacy : ∀ p b, IA p = some b → sem p = some b)
                                                                       (universal
  (hreplay : IA p0 = some b) (h𝜑 : 𝜑 (projB 𝜋 b)) :                    transfer)
  ∃ b', sem p0 = some b' ∧ 𝜑 (projB 𝜋 b') :=                           contract algebra     Contract.comp_glb,            propext,
  ⟨b, adequacy _ _ hreplay, h𝜑 ⟩                                       (composition =       Direction.comp_eq_min         Quot.sound
                                                                       componentwise                                      (comp_eq_min:
                                                                       meet)                                              —)
Table 2 maps the paper’s results to their Lean theorems
with each proof’s exact axiom footprint, re-checked at every
build; the one classical proof is Theorem 3.8 (an unfaith-
ful route names no witness by itself). The table also shows            system has any — and no bad may fire (§6.2–§6.5). Sam-
where mechanization stops, and we state it plainly: Theo-              pling corroborates, it does not entail — which is the grade
rem 3.18’s clauses (iii) and (iv) enter the Lean statement as          discipline applied to the calculus’s own hypotheses.
hypotheses. Both now carry tested surrogates rather than by-              Deliberately not mechanized: the fieldwise loss compu-
construction assertions. The specialization obligation is dis-         tation and retiming case of appendix A.2 (syntactic side
charged by sampled commutation checks per reasoning pair               conditions over a concrete carry-back representation), the
with free inputs (in the suite): the open program is translated        optimality halves of Theorem 3.13 (meta-statements over
once, and for sampled valuations the emitted artifact is byte-         models), and the grade set 𝐺 itself — evidence provenance is
identical while the specialized instance’s square passes —             not a mathematical object, which is the point of separating 𝐺
the shape universal_from_open_artifact consumes. The                   from A. The telescope theorems’ audit adds only Quot.sound
solver-artifact-to-target-semantics correspondence behind              (from structural-recursion equations); localization remains
(iii) is corroborated per verdict: every bounded-unreachable           the sole classical proof among these results (the same build
route verdict in the branch, benchmark, and certified ex-              audit also prints the artifact’s frontier-exploration model —
periments is additionally replayed through the strict target           no result of this paper — whose three search lemmas are
interpreter for the full bound — sampled inputs where the              classical).
                                                                  10
Untrusted Authors, Trusted Answers


      C          riscv                                                          the solver call is byte-deterministic, enforced repo-wide by
                                     sail                                       twice-and-diff.
                aarch64                            python            crn
                                                                                4.2   Languages and reasoning hubs
                                                                                Thirteen languages are registered, each with a specification-
                 wasm
                                                                                anchored formal semantics and (for all but C) a built shared
                                     btor2                  smtlib
                 ebpf
                                                                                interpreter: the ISAs RISC-V (RV64IMC), AArch64 (a growing
                                     havoc   interval                           A64 slice), eBPF, Wasm, and EVM; C (whose “interpreter” role
                                                   checked
                  evm                              predicted                    is played differentially, see below); Python (a pinned CPython
                                                   reproducible                 restricted by an AST allow-list to an integer subset — the
                                                                                loader rejects, CPython runs); Sail (an executable slice of the
    smiles       formula
                                                                                Sail-derived RISC-V and Arm semantics); chemical reaction
Figure 3. The registry: 13 languages (nodes; the two rea-                       networks (a discrete Petri-net stepper); SMILES molecular
soning hubs shaded) and 15 registered pairs (edges), each                       graphs and molecular formulas; and the two reasoning hubs:
carrying its declared grade. The two loops on the BTOR2                         BTOR2, a bit-vector/array transition-system logic consumed
hub are the abstraction endo-pairs of the direction axis (§3.4):                by hardware model checkers — environment constraints
btor2-havoc, built, and — gray — btor2-interval, regis-                         enforced with the per-frame reading, a bad counting only
tered as a brief. The evaluation of Section 6 covers the thir-                  on a constraint-valid prefix, on which the shared evaluator,
teen pairs built at its snapshot. RISC-V and AArch64 each                       the bridged and the native engines agree — and SMT-LIB
reach BTOR2 twice — directly (manual-derived) and through                       (QF_ABV and QF_LIA fragments).
Sail (formal-model-derived) — the independently derived                            Reasoning languages own, beyond an interpreter, a solver
branches Assumption 2 requires, each leg’s semantic artifact                    inventory (BtorMC and Pono for BTOR2; Z3, Bitwuzla,
declared per pair; the dashed btor2→smtlib bridge is the                        Boolector, cvc5, Yices2 for SMT-LIB) and a witness-checker
shared suffix that the disjoint-decision runs of §6.2 remove                    inventory: interpreter replay of BTOR2 .wit witnesses,
from the corroborating pair.                                                    model evaluation by the deterministic SMT-LIB evaluator,
                                                                                multi-engine corroboration, and a bit-blasted certificate
                                                                                pipeline for proved-tier unreachability with two checker
                                                                                rungs: the DRAT proof checked by drat-trim (independent,
4     The platform                                                              unverified), and — preferred when present — elaborated
The calculus is implemented as hurdy-gurdy, a Python plat-                      to LRAT (drat-trim as an untrusted elaborator) and re-
form whose structure mirrors Section 3 exactly: a framework                     validated by cake_lpr, the formally verified CakeML
that holds no pair semantics, per-language shared interpreters,                 checker, built natively from its compiler-generated ARMv8
and per-pair translators and carry-backs. Figure 3 draws the                    assembly (§6.5).
registry graph; this section describes what the use plane runs                     Interpreter adequacy (Assumption 1) is discharged differ-
on, Section 5 describes how it grows, and Section 6 measures                    entially: the RISC-V interpreter against the Sail-generated
both.                                                                           reference simulator (sail_riscv_sim) and the official
                                                                                riscv-tests / riscv-arch-test suites; the Python subset
4.1       Framework                                                             against pinned CPython by construction — a circularity we
The framework provides the registry, the content-addressed                      note plainly: for this one language the pinned runtime is
cache of Theorem 3.9, the generic square oracle with                            both the semantics and the interpreter, so adequacy has no
step/observable localization, the route enumerator and                          independent reference; C against CBMC on the same source
runner (routes are enumerated and reported — composed                           (with a classification step separating C-undefined-but-ISA-
grade, coverage, loss — never chosen), the coverage harness,                    defined behavior from genuine faults).
the merge-run route grader, the solver/checker plumbing,
and the books of §5.3 with their advisory reads (route report,                  4.3   Pairs and routes
answerability diagnosis, trust and reduction advisors) — all                    Fifteen pairs are registered. Thirteen — built to varying, mea-
of which annotate and account, none of which chooses. The                       sured extents (Table 3) — form the evaluation snapshot of
same surface is the player interface: an MCP server (gurdy                      Section 6; the other two sit on the direction axis of §3.4:
mcp, stdio JSON-RPC) exposes exactly the enumerated, ad-                        btor2-havoc, the localization abstraction, built, negative-
visory calls — languages, pairs, annotated routes, coverage,                    controlled, and driving the refinement demonstration, and
the diagnosis, the advisors, and bounded decide-with-replay                     btor2-interval, a second over-approximation registered
— so an LLM player connects to the platform as a machine                        as a brief under the discipline of §5.3. The spine is C → RISC-
peer, with the exposure rule pinned by test (§6.14 runs the                     V → BTOR2 → SMT-LIB, with the C head a digest-pinned
player experiment over this surface, cold). Everything except                   gcc at grade reproducible: the square-verified portion of
                                                                           11
                                                                                                                      Christoph Kirsch


the spine begins at the compiled binary (§3.5), and the C hop         of Section 6 applied as an admission test — and Theorem 5.2
is re-checked separately by the CBMC differential above. The          guarantees an additive contribution extends, never silently
direct RISC-V→BTOR2 lowering draws on the rotor bounded               invalidates, the verdicts already earned.
model checker [12]. RISC-V and AArch64 each reach BTOR2
by two independently derived routes (manual-derived direct            5.2 Coverage, and the ratchet
translator vs. Sail-model-mediated), instantiating Assump-            Fidelity alone is gameable by triviality: a pair handling one
tion 2; the BTOR2 hub funnels five ISAs into one solver in-           instruction is vacuously proved. Its companion axis is mea-
terface, and the BTOR2 → SMT-LIB bridge (a rule-for-rule              sured against a yardstick the implementer does not choose:
operator mapping at grade predicted) connects the hubs,
                                                                      Definition 5.1 (Coverage). Fix for each language a construct
so every BTOR2 question can also be decided natively-vs-
                                                                      inventory 𝐾𝐴 enumerated from its specification (opcodes,
bridged — solve-step corroboration. CRN and Python reach
                                                                      operators, syntactic forms). A construct 𝑘 ∈ 𝐾𝐴 counts for
SMT-LIB directly (QF_LIA), and SMILES→formula exercises
                                                                      pair 𝑃 iff 𝑃 covers it (𝑘’s probe programs lie in dom(𝑃)) and 𝑃
the calculus away from computation entirely.
                                                                      is faithful on those probes: cov(𝑃) ⊆ 𝐾𝐴 is the per-construct
                                                                      conjunction of covered and faithful. Route coverage cov(𝑅)
5     The economy: how the platform grows                             counts 𝑘 iff its lowering survives — covered and faithful —
The evolution plane writes what Section 4 reads. Its stages —         at every hop.
build under contract, gate, ratchet, and the books that direct
                                                                         Coverage is gamed by unsoundness (accept everything,
them — are the growth step of Section 2, kept under one
                                                                      translate it wrongly) exactly as fidelity is gamed by triviality
discipline: growth never answers.                                     (translate one thing, prove it); the conjunction closes both
                                                                      routes to a vacuous “pass.” Everything a pair rejects must be a
5.1   How the pairs were built                                        typed unsupported, so the uncovered set is itself enumerable
Each pair (and each shared interpreter) was implemented               and auditable — partiality is fail-fast, never silent.
by an independent LLM agent from a one-page registration                 Coverage then grows by a discipline with a soundness
brief — under the current discipline, a brief that opens by           theorem:
citing the demand records recommending the pair (§5.3) —
                                                                      Proposition 5.2 (Ratchet). Call an update 𝐼 ′ ⊒ 𝐼 (likewise
against the calculus as a written contract, under three stand-
                                                                      𝑇 , Λ) an extension when dom(𝐼 ′ ) ⊇ dom(𝐼 ) and 𝐼 ′ ↾dom(𝐼 ) =
ing rules: agents never modify the framework or another
                                                                      𝐼 . Under extensions: every faithfulness verdict at every 𝑝 ∈
deliverable’s code; interpreter changes are versioned events
                                                                      dom(𝐼 ) is preserved; cov is monotone; and prior evidence (or-
that re-validate every dependent pair (Theorem 5.2); and
                                                                      acle passes, differentials, agreement records) never needs re-
all growth is by additive widening — extend the covered
                                                                      earning. An update that is not an extension can silently inval-
fragment, re-run all prior evidence byte-for-byte, ratchet the
                                                                      idate any of these, and must instead bump the component’s
coverage number. The platform’s checks — the square oracle,
                                                                      version and re-validate every dependent pair.
the differentials, solver corroboration, branch agreement,
twice-and-diff — were the only semantic quality gate; no hu-             The implementable extension check is byte-identity of
man reviewed agent code for semantic correctness, though              all old outputs across the update — the same twice-and-diff
an autonomy protocol did escalate one class of change —               mechanism as Theorem 3.9, run across versions. This is
edits to shared emission code — for human sign-off (“largely          precisely the repo’s widening protocol (additive interpreter
unsupervised” means exactly this: the human gated whether             bumps, versioned events, dependent-pair re-validation),
such a change could land, never whether it was right). The            which Section 6 measures over the project’s own history.
defects those checks caught, and where they localized, are               The ratchet is the evolution plane’s contract with the use
part of the evaluation (§6.6): the implementation process             plane: declarations only strengthen, verdicts only accumu-
itself is an experiment in the paper’s thesis that translation        late. What directs the growth is the demand the use plane
trust can be manufactured by architecture rather than by              records:
trusting the translator’s author — whether that author is a
compiler vendor or a language model. The same discipline              5.3   Keeping the books: demand, cost, and
is the growth model: pairs contributed by anyone — with                     recommendation
LLMs, with agents, or by hand — through ordinary pull re-             Between diagnosis and registration sits the accounting: the
quests, admitted by architecture rather than authorship. A            books, one append-only, opt-in, host-local ledger with two
contribution arrives as the calculus’s tuple with its evidence        sides. The cost side is written beside the work by the instru-
surface attached (translator, carry-back, declared projection         mented call sites — translation on cache miss, the square
and grade, typed unsupported partiality, probes, a runnable           oracle, every decide backend — and accumulates from the
square); the merge gate re-runs conjoined coverage, depen-            capped route-grader runs in CI; it feeds the measured axis of
dent branch agreements, and twice-and-diff — the machinery            the annotated route report, where Pareto-dominated routes
                                                                 12
Untrusted Authors, Trusted Answers


are marked, never hidden, dominance is computed only be-                   We evaluate the snapshot along the axes the calculus
tween fully measured routes, and an absent measurement                  makes measurable: per-pair coverage (§6.1), composed route
reads unmeasured, never zero. The demand side is written                coverage and branch agreement — including a disjoint-
by the diagnosis calls: each question the platform cannot               decision block — (§6.2), a compliance-derived reachabil-
satisfy is recorded verbatim with its failing obstacle and the          ity benchmark decided along both RISC-V routes (§6.3),
generation target it names — the four obstacles of §2, plus a           end-to-end case studies exercising Theorem 3.17 (§6.4),
fifth, trust, when a player’s assurance floor is unmet — and            certified-unreachability runs inhabiting the proved tier
every record carries an origin tag separating organic player            (§6.5), the defects the architecture caught (§6.6), a measured
sessions from synthetic campaigns.                                      escape-rate estimate for the gate (§6.7), a first controlled
   A recommendation is then an aggregation, not a judg-                 experiment with LLM players (§6.8), and performance,
ment: the board groups recorded demand per target and                   determinism, and scale (§6.9). Every number in this section’s
deduplicates by question identity; the failing obstacle is the          tables is regenerated by one script from the live registry
platform’s one demand taxonomy, naming what the candi-                  and real runs at the snapshot commit, with a few curated
date pair pays for — connectivity and shape buy capability,             exceptions marked at source — the defect catalog behind
loss buys coverage, cost buys performance, trust buys an in-            Table 8 is hand-mined from history, and Table 11 formats the
dependent anchor. A campaign of five questions, run against             recorded outputs of a manual two-arm protocol; the escape
the July 2026 registry, yields a four-row board that illustrates        experiment’s earlier-round numbers (§6.7) likewise come
the shape of the evidence (the diagnosis and the board are              from its incident record. (Host: macOS/arm64, CPython 3.12,
measured as a benchmark in §6.12): a reasoning-language                 Z3 4.13, btormc 3.2, cadical; drat-trim pinned at source com-
demand (two liveness questions no registered hub expresses              mit 2e3b2dc and cake_lpr at a4323b2, the engine inventory
— the depth growth of the conclusion), an independent-pair              recorded in the regenerated env.json; the platform’s own
demand (a single-route source whose provenance is unde-                 suite runs 1215 tests there, all green, with 3 host-dependent
clared), a connectivity demand (a source with no route to any           skips.) The evaluation remains deliberately fully specified
hub, with a draft brief stub attached), and a cost demand (a            rather than large: every question — authored or derived
resource-out verdict naming the registered abstraction dials).          — is checked end to end with its ground truth stated, and
Each row removes a different obstacle; no scalar ranks them.            the largest sweep (the 78-question compliance-derived
   The discipline this buys is recommended, then registered: a          benchmark of §6.3) is still small next to an SV-COMP-scale
registration brief opens by citing the demand records behind            campaign, which remains future work.
it — no evidence, no brief — while registration itself remains
the human act it has always been. The untrusted-generator
stance of §5.1 extends from building pairs to choosing them:            6.1   Capability snapshot
an LLM whose campaign manufactures demand to justify                    Table 3 reports per-construct coverage measured at harvest
a pet pair cannot launder it, because demand is auditable               time — not transcribed from documentation — in both of
(questions verbatim, origins displayed apart, volume explic-            Theorem 5.1’s readings: accepted (the probe translates with-
itly not a verdict), and the trust-side demands rest on the             out a typed unsupported abort) and conjoined (accepted and
declared, protected semantic artifacts of Assumption 2 —                the pair’s square oracle passes on the probe — the defini-
a shared artifact is never independent, an undeclared one               tion’s actual conjunction, run probe by probe). For every
never silently so.                                                      pair with a decidable square the two columns now coincide;
                                                                        they did not when the conjunction was first measured, and
                                                                        what it surfaced on its first run is instructive enough to re-
6    Evaluation                                                         port (§6.6, incidents I20–I22): the Sail-route front dropped
The fifteen subsections below answer four questions. Does               the program’s initial memory, so every load-family probe
the graph answer correctly? — the capability snapshot, com-             diverged at step 0 (accepted, silently wrong — precisely the
posed coverage and branch agreement, the compliance slice,              failure mode acceptance counting cannot see), and three of
and the end-to-end case studies (§6.1–§6.4). Does the evidence          the BTOR2 lowerings modeled a program counter that leaves
mean what it claims? — the certified tier and the escape-rate           the code as stuck where every reference interpreter halts,
experiments for the gate itself (§6.5, §6.7). Can untrusted au-         so every taken-jump probe whose target exits the image
thors build it? — the defects the architecture caught (§6.6).           diverged on halted (the worked example of §3.2 shows this
Can an LLM play it? — the player experiment (§6.8); perfor-             square, and its oracle output, verbatim). It also audited its
mance and scale close (§6.9). The snapshot tables end there;            own instrument: one probe (SD) stored over its own ECALL
five later benchmark families, each stamped with its own                terminator, so the reference interpreter could not run it and
commit, follow (§6.10–§6.14), and a short record of what re-            no square had ever executed on that construct — acceptance
mains narrated rather than measured ends the section (§6.15).           counted it covered anyway. Measuring the definition’s con-
                                                                        junction found all three in its first run; the fixes are ordinary
                                                                   13
                                                                                                                                     Christoph Kirsch


Table 3. Capability snapshot: per-pair construct coverage                Table 4. Composed conjoined coverage: a probe counts iff it
against the language-owned inventory. Accepted = the probe               survives every hop and every hop with a decidable square
translates without a typed unsupported abort; conjoined =                passes it on that hop’s input (the route-level reading of Def-
accepted and the pair’s square oracle passes on the probe —              inition 5.1; “via Sail” routes are the independently derived
Definition 5.1’s conjunction, measured directly (§6.1). Pairs            branch; denominators are the source language’s inventory,
without a decidable square (the predicted-grade hops into                §6.2). Routes marked † contain no decidable-square hop at
the SMT-LIB hub) discharge the faithfulness conjunct per                 all (their one translator is predicted-grade): the number
run instead (§3.5), marked per-run; the reproducible C hop               is acceptance, with faithfulness discharged per run (§3.5).
carries no construct inventory and shows “—”. Gaps counts                Branch agreement: the same question decided along both
the distinct typed unsupported constructs. Measured from                 routes. Times are the slower route, end to end (translate every
the live registry at the snapshot commit.                                hop + decide with Z3). The bottom block decides the same
                                                                         questions with fully disjoint decision stacks after the head:
Pair (source→target)   Grade          Accepted   Conjoined   Gaps        the direct route’s BTOR2 system decided natively by btormc
                                                                         (no bridge, no SMT-LIB, no Z3) against the via-Sail route
c-riscv                reproducible   —          —             —
riscv-btor2            checked        96/96      96/96          0        through the bridge and Z3 — the diverse segment spans both
riscv-sail             checked        96/96      96/96          0        the lowering derivation and the decision procedure (§3.6).
sail-btor2             checked        95/95      95/95          0
aarch64-btor2          checked        27/33      27/33          6
                                                                                         Route                Composed coverage
aarch64-sail           checked        27/33      27/33          6
wasm-btor2             checked        54/75      54/75         21                        RISC-V, direct                         96/96
ebpf-btor2             checked        126/126    126/126        0                        RISC-V, via Sail                       96/96
evm-btor2              checked        86/144     86/144        58                        AArch64, direct                        27/33
btor2-smtlib           predicted      56/56      per-run        0                        AArch64, via Sail                      27/33
crn-smtlib             predicted      10/10      per-run        0                        Wasm                                   54/75
python-smtlib          predicted      11/27      per-run       16                        eBPF                                 126/126
smiles-formula         predicted      14/17      14/17          3                        EVM                                   86/144
                                                                                         CRN†                                   10/10
                                                                                         Python†                                11/27
                                                                                         SMILES                                 14/17

                                                                         Question (both routes)                          Agree    Verdict    Time (s)

versioned translator bumps and one probe repair. Pairs with-             riscv const x1==42 (reach)                       ✓       reach           0.0
                                                                         riscv const x1==99 (unreach)                             unreach         0.0
out a decidable square — the predicted-grade hops into the                                                                ✓
                                                                         riscv loop sum==15 (reach)                       ✓       reach           0.0
SMT-LIB hub — discharge the faithfulness conjunct per run                riscv loop sum==99 (unreach)                     ✓       unreach         0.0
at question time instead (§3.5) — what their grade leaves to             riscv store/load 0x123 (reach)                   ✓       reach           0.0
per-run checking; the table marks them per-run (the fourth               riscv store/load 0x999 (unreach)                 ✓       unreach         0.0
predicted pair, SMILES→formula, has executable ends and                  C a0==47 (reach)                                 ✓       reach           0.1
                                                                         C a0==99 (unreach)                               ✓       unreach         0.0
conjoins directly). Denominators are language-owned inven-
                                                                         aarch64 movz/add x1==42 (reach)                  ✓       reach           0.0
tories (Theorem 5.1’s yardstick): both RISC-V-headed pairs               aarch64 movz/add x1==999 (unreach)               ✓       unreach         0.0
measure against the same 96-construct RV64IMC inventory,                 aarch64 SUBS/B.NE loop x0==1 (reach)             ✓       reach           0.0
the two AArch64 pairs against one declared A64 slice whose               aarch64 SUBS/B.NE loop x0==5 (unreach)           ✓       unreach         0.0
out-of-scope constructs count in the denominator, and the                aarch64 flags + loop (SUBS/B.NE)                 ✓       trace =𝜋         —
                                                                         aarch64 32-bit W forms                           ✓       trace =𝜋         —
Wasm and EVM rows against their in-scope ∪ enumerated-
out-of-scope unions (54/75, 86/144) — a gap shows as a typed                  Question, decision stacks fully disjoint         Agree    Verdict
unsupported entry, never by shrinking the total. Depth re-
                                                                              riscv const x1==42 (reach)                         ✓      reach
mains uneven by design and visibly so: the spine is deep (all                 riscv const x1==99 (unreach)                       ✓      unreach
96 RV64IMC constructs conjoined; eBPF complete at 126;                        riscv loop sum==15 (reach)                         ✓      reach
the BTOR2→SMT-LIB bridge total on its 56-item operator/-                      riscv loop sum==99 (unreach)                       ✓      unreach
sort/directive inventory), Python stands at 11 of 27 subset                   riscv store/load 0x123 (reach)                     ✓      reach
constructs, and every gap is a typed unsupported the har-                     riscv store/load 0x999 (unreach)                   ✓      unreach
                                                                              aarch64 movz/add x1==42 (reach)                    ✓      reach
ness can enumerate (the “gaps” column). The declared A64                      aarch64 movz/add x1==999 (unreach)                 ✓      unreach
slice is still narrow against the full base ISA — the honest                  aarch64 SUBS/B.NE loop x0==1 (reach)               ✓      reach
reading of 27/33 is “the in-scope family conjoins, and the                    aarch64 SUBS/B.NE loop x0==5 (unreach)             ✓      unreach
slice is small.” The C head carries no construct inventory:                   C a0==47 (reach)                                   ✓      reach
its translator is the pinned compiler, graded reproducible                    C a0==99 (unreach)                                 ✓      unreach
(§3.5).
                                                                    14
Untrusted Authors, Trusted Answers


                      RISC-V program 𝑝 + question                           unrolling, store/load through memory, two questions about
            riscv-btor2                        riscv-sail                   a gcc-compiled C program (can a0 be 47 at halt? can it be 99?),
            btor2                                    sail                   and four AArch64 questions decided along the Arm-manual-
                                                                            derived and the Arm-Sail-model-derived route — were each
                                                          sail-btor2
                                                                            decided along both routes of their branch; all twelve pairs
                                                    btor2
                decide natively                                             of verdicts agree, including the universal (unreachable)
                (no bridge, no             btor2-smtlib                     halves where agreement carries real information. The C
                SMT-LIB, no Z3)
                                                    smtlib                  rows exercise the full re-establishment story: an opaque
                                                                            reproducible compiler heads both routes, and its output is
            btormc                                    z3
                                                                            validated downstream twice, independently. The AArch64
                                                                            trace-level rows cross-check the same branch below the
                              must agree
                                                                            solver, directly comparing the two carried-back behaviors
            verdict                                 verdict                 under 𝜋. The table’s bottom block addresses Assumption 2’s
                                                                            scoping head-on: the twelve solver-level rows share the
Figure 4. What the bottom block of Table 4 measures: the                    BTOR2→SMT-LIB bridge below the reconvergence, so every
same question decided along two stacks sharing no decision                  one of the twelve is re-decided with fully disjoint decision
component after the head (the named residue: emission li-                   stacks after the head (Figure 4) — the direct route’s BTOR2
brary, endpoints) — the ISA-prose-derived lowering decided                  system decided natively by btormc (no bridge, no SMT-LIB,
natively by btormc, against the Sail-model-derived lower-                   no Z3) against the Sail-model route through the bridge and
ing through the predicted-grade bridge and Z3. Agreement                    Z3. All twelve agree. Every unreachable verdict among them
corroborates the whole diverse segment (Assumption 2); the                  is additionally corroborated below the solvers: the strict
stated residual shared surface is the BTOR2 emission library                BTOR2 interpreter replays the direct route’s system for
and the language-owned endpoint interpreters. The solver-                   the full bound and no bad fires — the tested surrogate for
level rows at the top of Table 4 instead decide both sides                  Theorem 3.18’s artifact-to-semantics hypothesis (recorded
through the bridge and Z3, sharing everything below the                     per question, as is the same replay for every bounded-
reconvergence.                                                              unreachable verdict of Table 5). The diverse segment now
                                                                            spans the lowering derivation (ISA-prose vs. formal-model)
                                                                            and the decision procedure (different solver, different input
6.2 Composed coverage and branch agreement                                  format); the residual shared surface, stated rather than
Table 4 (top) composes conjoined coverage along whole                       hidden, is the BTOR2 emission library — the site of incident
routes: a construct counts iff its probe survives every hop                 I3, the platform’s one recorded cross-route common-mode
and every hop with a decidable square passes it on that hop’s               failure through shared code (shared misreadings are the other
input. Nothing a head accepts is eaten at the hubs: every ac-               kind, §6.6) — and the language-owned endpoint interpreters.
cepted probe of every route survives composed to its route’s
target, squares included. The denominators are the source                   6.3 The compliance slice as a question set
language’s inventory, so the two RISC-V routes are measured                 The questions above were authored; Table 5 scales the same
on the same 96-construct yardstick and both compose 96/96 —                 discipline over a derived question set nobody hand-picked.
the spine composes losslessly, and the earlier version of this              The platform’s RISC-V compliance slice — self-checking pro-
table, whose two RISC-V rows quoted different pair-chosen                   grams in the upstream riscv-tests HTIF tohost convention,
denominators (96 vs. 95), is exactly the yardstick-shopping                 built with the pinned cross-toolchain at the upstream link
Theorem 5.1 forbids and this measurement now closes. The                    base 0x8000_0000 — doubles as a reachability benchmark:
AArch64 rows also carry a ratchet anecdote the machinery                    each program is reference-run to completion, and for each
makes precise: one revision earlier the Sail-mediated route                 data register the harness derives one question whose target
composed to 0/33, because the Sail→BTOR2 translator low-                    value the register demonstrably held (ground truth reach-
ered only the RV64IMC arm — and the harness localized ev-                   able) and one whose target no register held at any step
ery miss to the sail-btor2 hop by name. Widening that one                   (ground truth unreachable within the bound), with the
hop (an additive translator bump, RISC-V arm byte-identical                 unrolling bound covering the whole run. Every question is
per Theorem 5.2) closed the gap without re-earning any                      then decided independently along both RISC-V routes. Three
other evidence. A gap the system reports and localizes is the               honesty notes. First, the slice is curated in the upstream con-
designed behavior; a gap papered over would be the defect.                  vention rather than taken binary-for-binary from upstream:
   The bottom of Table 4 is the fidelity payoff of Theo-                    the stock -p- binaries open with machine-mode CSR and
rem 3.16: the same reachability questions decided along                     trap setup that is outside the declared user-ISA scope, so
independently derived routes. Twelve solver-level questions                 the slice re-creates the grading convention over the user
— constant dataflow, summation and countdown loops under                    subset (the gap is typed, not hidden). Second, the ground
                                                                       15
                                                                                                                                        Christoph Kirsch


Table 5. The compliance slice as an external-format ques-                    Table 6. End-to-end case studies. “Replay” is the source-level
tion set: self-checking programs in the riscv-tests HTIF con-                witness check of Theorem 3.17: the carried-back witness re-
vention (built with the pinned toolchain at the upstream                     executed by the source interpreter.
link base), each reference-run to derive per-register reach-
able / bounded-unreachable questions with machine-derived                    Case                             Verdicts                  Replay         Time (s)
ground truth, each question decided independently along
                                                                             C spine (both routes +           REACHABLE (both             ✓                0.21
BOTH RISC-V→SMT-LIB routes. Agree = the two routes’                          source replay)                   agree)
verdicts coincide; correct = the agreed verdict matches the                  Python assert violable?          REACHABLE                   ✓                0.18
interpreter-derived ground truth. Time is both routes, all                   (QF_LIA)
questions, end to end.                                                       EVM 6*7==42 native vs            REACHABLE (both             ✓                0.05
                                                                             bridged                          agree)
                                                                             CRN A->B twice reaches           REACHABLE                   ✓                3.78
Program           Steps   𝑘    Questions   Agree   Correct   Time (s)        B=2
rv64uc-compress     34    42          8      8/8       8/8        2.7
rv64ui-arith        63    71          8      8/8       8/8        8.2
                                                                                                             𝑇𝑅 (whole route)
rv64ui-branch       34    42          6      6/6       6/6        2.4                 source 𝑝 (𝑥 )                                     artifact at 𝑍
rv64ui-jump         18    26          8      8/8       8/8        1.4
rv64ui-ldst         68    76          8      8/8       8/8       12.0
rv64ui-logic        49    57          8      8/8       8/8        6.5                                                                         solver
rv64ui-shift        45    53          8      8/8       8/8        5.7
rv64ui-word         43    51          8      8/8       8/8        5.0
rv64um-div          69    77          8      8/8       8/8       11.4                                         Λ𝑅 (carry-backs)
                                                                                    𝐼𝐴 replays 𝑝 (𝑥 0 )                                  witness 𝑥 0
rv64um-mul          39    47          8      8/8       8/8        3.9
Total                                78    78/78     78/78
                                                                                                𝜑 observed: reachable, TCB = {𝐼𝐴 adequacy }


                                                                             Figure 5. The round trip every case study in Table 6 com-
                                                                             pletes (Theorem 3.17): the witness comes back through the
truth comes from the shared reference interpreter — but that                 route’s carry-backs and is replayed by the source interpreter.
interpreter is exactly the component the adequacy campaign                   Everything on the way down is a discovery device — a defect
validates step-for-step against the Sail-generated gold sim-                 in any translator, hub, or the solver can lose the witness,
ulator on these same programs, so the benchmark’s ground                     never fake the replay.
truth is anchored outside the platform. Third, the bench-
mark’s discriminating power is scoped: ground truth and
both routes share the reference interpreter, so it measures                  6.4    End-to-end case studies
translator- and route-level defects — a shared-misreading                    Table 6 instantiates Theorem 3.17 once per hub and front-end
defect of the MUL/ADD class (§6.6) would pass it undetected,                 family, completing the round trip of Figure 5 at the source
and the external Sail differential, not this benchmark, is what              each time. (1) The C spine: both routes answer reachable
polices that class. The result: 78 questions over 10 programs                for a0=47, and the source-level replay runs the compiled pro-
(constant dataflow, logic, shifts, 32-bit word ops, taken and                gram in the shared RISC-V interpreter to the halt in _start()
untaken branches, computed jumps, the store/load family,                     with a0=47 observed — the verdict survives even if every
multiplication, division with its RISC-V-defined edge cases,                 translator and the solver were wrong. (2) Python: “is the trail-
and compressed forms), both routes agreeing on all 78 and                    ing assert violable?” for a function with a bounded loop and
all 78 matching ground truth, in under a minute end to end                   a branch; Z3 finds the witness 𝑥=4, the shared QF_LIA eval-
— with every one of the 39 bounded-unreachable verdicts                      uator independently re-checks the model (smt_model_ok),
additionally corroborated by a full-bound replay of the direct               and the input is replayed through the pinned CPython down
route’s system through the strict BTOR2 interpreter (§6.2’s                  the taken branches, firing the assert. (3) EVM: 6 × 7=42 on
surrogate, recorded per question). Preparing this benchmark                  the operand stack, decided natively (btormc on the BTOR2
also forced one more fidelity repair the base-0 probes could                 system, witness replayed by the strict BTOR2 interpreter)
not see: the Sail-route front rebased images to address 0,                   and bridged (through the SMT-LIB hub with Z3) — solve-step
which silently breaks every pc-relative absolute-address com-                corroboration across two engine families, agreeing. (4) CRN :
putation (AUIPC/LA) on images linked at the upstream base                    a two-firing reachability question in a reaction network, wit-
— found while squaring the translator against the slice’s link               ness schedule replayed by the Petri-net interpreter. In all
discipline, and fixed by carrying absolute addresses through                 four, the final trust rests on the source interpreter (plus the
the Sail object (a versioned bump, with the squares and this                 small fixed replay harness Theorem 3.17 names), per the last
benchmark as regressions).                                                   row of the ledger in §3.6.
                                                                        16
Untrusted Authors, Trusted Answers


Table 7. The certified (proved) row inhabited, twice: input-                         and asks whether the product can be 231 − 1: the Mersenne
driven unreachability claims from a real pair, corroborated                          prime admits no factorization with both factors in range, and
by three engines, certified by a bit-blasted DRAT proof, and                         refuting a 16×16-bit multiplication is certificate checking at
re-validated by the independent verified checker. The first                          scale — a 2.8 MB DRAT elaborating to an 11.8 MB LRAT,
exhibit is deliberately small (its refutation is essentially unit                    re-validated in seconds. In both, three engines corroborate
propagation); the second is certificate checking at scale —                          unsat, bitwuzla bit-blasts the query to CNF, cadical emits a
refuting a 16×16-bit multiplication. The controls are bogus                          DRAT refutation, drat-trim elaborates it to LRAT — an un-
checks that must fail — and do.                                                      trusted step: a wrong elaboration can only fail the re-check,
                                                                                     never fake a pass — and cake_lpr, the formally verified
                            propagation-scale         search-scale                   CakeML LRAT checker (soundness machine-proved down to
Question                    helper ( ) 2 = 3 (no      𝑥 · 𝑦      = 231 −1,           the binary; here built natively from its compiler-generated
                            square mod 264 )          𝑥, 𝑦 ∈ [2, 216 +1]             ARMv8 assembly), re-validates the proof against the CNF
                                                      (no bounded factoriza-
                                                      tion of the Mersenne
                                                                                     from scratch. The verdicts’ TCB is exactly the ledger’s cer-
                                                      prime)                         tified row: the bit-blaster’s BV→CNF step and a verified
Engines agreeing un-        bitwuzla, boolector, z3   bitwuzla, boolector, z3        checker, with all three deciding engines and the elaborator
sat                                                                                  demoted to discovery devices — the solve step’s residue; the
Certificate                 41746 B DRAT, 18 B 2.8 MB DRAT, 11.8 MB                  route hops that produced the artifact remain accounted per
(bitwuzla→CNF,              LRAT (drat-trim, un- LRAT
cadical→DRAT)               trusted)
                                                                                     the ledger. Both certified systems are also corroborated below
Independent check           cake_lpr (formally ver- cake_lpr (formally ver-          the whole certificate pipeline: fifty seeded random helper
                            ified): verified; tier ified): verified; tier            streams replayed through the strict BTOR2 interpreter fire
                            proved                    proved                         no bad (recorded in the run data). The reachable siblings
Resulting TCB (solve        bitwuzla:bit-blast, cake_lpr:verified                    (𝑥 2 = 4; 𝑥·𝑦 = 463412 ) correctly decline to certify.
step)
Reachable sibling          𝑥 2 =4: REACHABLE, 𝑥 ·𝑦=463412 : REACH-
                                                                                         Wiring this exhibit produced one more architecture-
                           no certificate          ABLE, no certificate              caught defect, live: the checker adapter matched the sub-
Negative controls          both rejected (bogus proofs vs. a satisfiable CNF)        string VERIFIED in the checker’s output — and drat-trim
Wall time                  0.36 s                  4.85 s                            reports failure as s NOT VERIFIED, which contains it. Every
                                                                                     check, sound or bogus, reported success. The bug could not
      btor2           smtlib            bitwuzla BV→CNF            CNF               surface on hosts without the checker (the call raised before
                                                                                     parsing) nor on real certificates (which do verify); it fell to
                                                                                     the negative control — a bogus refutation of a satisfiable
        LRAT           drat-trim (untrusted)     DRAT           cadical
                                                                                     CNF that must fail and did not. The fix parses the exact
                                                                                     status line, and the control is now a permanent test. This
           cake_lpr (verified)                  s VERIFIED UNSAT                     is the paper’s own instrument audited by the discipline it
                                                                                     describes (cf. §6.6), and a caution we commend to anyone
Figure 6. The pipeline Table 7 evaluates: the query is bit-                          wiring a proof checker: a checker adapter without a negative
blasted to CNF, cadical’s DRAT refutation is elaborated by                           control is itself unchecked. The verified checker’s adapter
drat-trim — an untrusted step that can only fail the re-                             was written under that rule from the start — wisely, since
check, never fake a pass — and cake_lpr, the formally ver-                           cake_lpr exits 0 even when checking fails; only the exact
ified checker, re-validates the LRAT against the CNF from                            s VERIFIED UNSAT line signals success, and both checkers’
scratch. Shaded is what stays in the verdict’s TCB: the bit-                         negative controls are permanent tests. One honest subtlety
blast and the verified checker; the three agreeing engines                           the exercise surfaced: for this instance the refutation is
and the elaborator are discovery devices.                                            propagation-dominated, so mutating single proof lines is not
                                                                                     a valid negative control (the checker legitimately completes
                                                                                     the derivation); the satisfiable-formula control is the sound
6.5   The certified tier                                                             one, since no valid refutation of a satisfiable formula exists.
Table 7 inhabits the ledger’s certified row (§3.6), twice — via
the pipeline of Figure 6 — once at each end of the difficulty                        6.6   Defects the architecture caught
scale. Both questions are pair-derived and input-driven: eBPF                        The pairs were written by independent LLM agents with no
programs whose CALL models helper returns as free inputs.                            human semantic review (§5.1); the architecture’s checks were
The first squares one input and asks whether 𝑥 2 = 3; no                             the only gate. Mining the full history (675 commits across
square exists modulo 264 , so the claim is universal over all                        all refs at the 2026-07-03 mining pass; ∼21 runtime-code fix
inputs — and its refutation is essentially unit propagation on                       commits) plus the three defects the conjoined-coverage mea-
the low bits (the elaborated LRAT is 18 bytes). The second                           surement caught on its first run (§6.1), the probe-operand
masks and offsets two inputs into [2, 216 +1], multiplies them,                      deficiency the fault-injection experiment exposed, and the
                                                                                17
                                                                                                                               Christoph Kirsch


compare-vector gap only the common-mode round could ex-                 Table 8. Defects caught by the architecture (selection; full
pose (§6.7) yields 24 recorded defect incidents: 15 caught by           list with commit-level evidence in the artifact). “Caught by”
the architecture’s cross-checks rather than by ordinary unit            names the check that fired — the cross-check layers of §3.6,
tests, and 7 more — including the checker-adapter defect of             plus the platform’s own audits and controls.
§6.5, a probe that could never have exercised its own square,
probes whose operands underdetermined their constructs,                 Defect                             Component     Caught by
and benchmark compare vectors on which signedness is in-                bv64 sort hardcoded for            RISC-V →      strict in-process
visible — by the audits and controls the architecture imposes           and/or/xor over bv1 operands       BTOR2         BTOR2 evaluator
on its own instruments, and the remaining two otherwise                 — malformed BTOR2 that real        translator    during the square’s
(one by machine-vs-human label disagreement, one only                   solvers tolerated                                alignment walk
                                                                        unsigned loads (LBU/LHU/LWU)       RISC-V →      solver leg: Z3 sort
partially attributed). Read this as case-study evidence, not
                                                                        missing zero-extension to bv64     BTOR2         rejection on the corpus
a hit rate: the catalog is mined from our own history, it has                                              translator
no denominator (the blind-spot incident below proves the                init value nid emitted after       shared        solver corroboration:
escape rate is nonzero), and no baseline says what a con-               the state nid — rejected by        BTOR2         wiring the 2nd/3rd
ventional test regime would have caught. Table 8 lists ten              every conformant tool,             emitter       engines (btormc, pono)
                                                                        tolerated by the one wired                       made the latent
representative architecture-caught defects, each localized —
                                                                        solver; affected every stateful                  malformation manifest
component, step, observable — as Theorem 3.8 promises.                  pair
   Three second-order observations are worth as much as the             local.get wrote a bv32 node        Wasm →        solver leg: Z3 sort
table. First, the checks caught their own instruments — seven           into the bv64 stack array          BTOR2         mismatch at BMC
of the 24 incidents are check-of-the-check repairs; three rep-                                             translator
                                                                        carry-back silently zero-filled    witness       witness-replay anchor
resentatives: the Sail ISA differential was once passing vacu-
                                                                        registers the solver witness       carry-back    audit (mismatch chain)
ously (comparing empty traces), the in-image suite caught a             omits (init-pinned states) —       Λ
witness generator emitting empty witnesses, and the DRAT                every pinned task’s entry state
checker adapter accepted every outcome until a negative                 misread
control ran (§6.5) — all found because the harnesses carry              default BMC bound mapped           verdict       oracle vs. corpus label
                                                                        “no violation within 𝑘” to         semantics
positive and negative controls, and all three are why Assump-
                                                                        unreachable — a false
tion 1 is stated as an assumption with empirical discharge              negative at step 93
rather than as a fact. Second, the history contains a genuine           ELF header bytes decoded as        shared ELF    square oracle on the
blind spot of the square, exactly of the class Theorem 3.16             instructions — interpreter         loader        first real gcc binary
predicts: the RISC-V interpreter and the RISC-V→BTOR2                   tolerated it, the square did not
                                                                        BTOR2 constraint lines             BTOR2 →       coverage probe:
translator both silently mis-decoded MUL (funct7 0x01) as
                                                                        silently dropped in the            SMT-LIB       driving the bridge to
ADD — both legs agreed, the square was blind, and the defect            SMT-LIB unrolling — an             bridge        its 56/56 spec
was found by manual audit. The platform’s structural answer             under-constrained,                               inventory exposed the
is diversity: the decoder is now anchored against 610 Sail-             soundness-leaking encoding                       hole
emitted words, and unknown funct7 hard-aborts on both                   JUMP/JUMPI underflow-halt          EVM →         square step alignment
                                                                        row diverged on pc                 BTOR2         during widening
sides. Third, in one incident three existing unit tests had been
                                                                                                           translator
written against the buggy behavior (an evaluator masking                INT_MIN / -1: C-undefined vs.      (real route   C-vs-ISA differential
every array store to 8 bits): tests written by a component’s            RV64-defined divergence, plus      divergence)   branch, with a
author codify the author’s misreading; cross-checks against             a CBMC false positive on the                     UB-vs-fault classifier
independently derived semantics do not. The architecture                same task                                        adjudicating
also disconfirmed one reported bug (a claimed slice-width
defect shown to be a stale-cache artifact), and its differential
campaigns — 300 seeded RV64IMC programs vs. the Sail                    the calculus itself predicts — Theorem 3.16’s “both unfaith-
simulator, a 10-seed Csmith campaign vs. native gcc, 463                ful with identical projected error” — landing not between
reference cases — completed with zero divergences against               two translators but between a translator and the component
harnesses whose positive controls confirm they can fail.                Theorem 3.17 crowns as the sole residual TCB. Both sides
                                                                        now hard-abort on unknown funct7, and the structural an-
   Two incidents in full. The catalog’s two most argument-              swer is external anchoring: the decoder is validated against
bearing entries deserve their narratives. First, the blind spot:        610 Sail-emitted instruction words and against an indepen-
the RISC-V interpreter and the riscv-btor2 translator mis-              dently written RV64C decompressor, construct by construct
decoded MUL (funct7 0x01) as ADD — identically. Both legs               — and the common-mode round of §6.7 now measures this
of every square agreed, so the square was structurally blind,           incident’s whole class directly. Second, the common mode:
and the defect was found by manual audit during widening,               the shared BTOR2 emission library declared states before
not by the architecture. This is the residual failure mode              their constant init values, so every emitted init line was
                                                                   18
Untrusted Authors, Trusted Answers


Table 9. Escape-rate experiment: seeded semantic mutations                       Table 10. Common-mode (both-leg) fault injection: the same
of the riscv-btor2 emissions (uniform rules model systematic                     misreading injected into BOTH the reference interpreter and
mis-lowerings, site rules single-site defects; operand swaps                     the riscv-btor2 translator — the MUL/ADD class of §6.6,
only on non-commutative operators; rules that change no                          which single-leg mutation cannot model. The square suite
probe artifact are excluded from the denominator), each run                      is structurally blind on every mutant (both legs wrong iden-
through the architecture’s gates in order. “Square” is the con-                  tically), and so is expected-based grading in the poisoned
joined probe suite (§6.1), “branch” the authored solver ques-                    world, where the benchmark’s ground truth is derived by the
tions against the intact Sail route, “bench” the compliance-                     mutated interpreter itself. What catches every mutant are
derived ground-truth questions (§6.3). Zero escapes means                        the gates outside the shared misreading: the independently
the seeded mutation families — catalog-derived, with probes                      derived Sail route disagreeing (cross-route), with the exter-
hardened against this experiment’s own earlier rounds — are                      nal Sail-simulator differential — run as a parallel column —
now covered; it is not an estimate that the escape rate is zero                  also catching every mutant.
(§6.7).
                                                                                 Misreading (both legs) Square Poisoned Caught by                Diff.
                 Applicable mutants                        55                    MUL as ADD           blind   blind    cross-route (rv64um-mul) ✓
                 Caught by the square suite                51                    SUB as ADD           blind   blind    cross-route (rv64ui-arith) ✓
                 Caught by branch agreement                 0                    SRA as SRL           blind   blind    cross-route (rv64ui-shift) ✓
                 Caught by the derived benchmark            4                    SLT as SLTU          blind   blind    Sail differential          ✓
                 Escaped all three gates                    0                    AND as OR            blind   blind    Sail differential          ✓
                                                                                 XOR as AND           blind   blind    cross-route (rv64ui-logic) ✓

      55 applicable mutants of the riscv-btor2 emissions

                                                                                 rate is nonzero. Table 9 measures it (Figure 7 draws the
                square suite (conjoined probes)                 51 killed        gate stack): seeded semantic mutations of the riscv-btor2
                                4 survive                                        translator’s emissions — uniform rules modeling systematic
                  authored branch questions                     0 killed
                                                                                 mis-lowerings (every sext emitted as uext, incident I2’s
                                                                                 family) and site rules modeling single-site defects (incident
                                4 survive
                                                                                 I1’s family); operand swaps only on non-commutative oper-
               derived benchmark (78 questions)                 4 killed         ators, so no trivially-equivalent mutants; rules that change
                                                                                 no probe artifact excluded from the denominator — each run
                         escaped: 0                                              through the architecture’s gates in the order the platform
                                                                                 applies them. The experiment earned its keep before its fi-
Figure 7. The escape-rate experiment (Table 9) as a gate                         nal numbers did: in its first round, both srl→sra mutants
stack: every applicable mutant runs the gates in the order the                   escaped all three gates (36 of 51 caught at the square layer),
platform applies them, and each gate’s kill count is measured.                   because every ALU probe ran its construct on degenerate
The authored branch questions catch nothing the square                           all-zero operands, on which logical and arithmetic shifts
suite missed — the derived benchmark is the differentiator                       agree — the “96/96 conjoined” verdict was faithfulness on
(a finding in itself).                                                           the probes, and the probes underdetermined the constructs.
                                                                                 Hardening the probes with mixed-sign operands moved 50
                                                                                 of 53 catches to the square layer but let ult→ulte escape
malformed — in every BTOR2-emitting pair at once, both                           — strictness is observable only at equal operands — so the
branches of every RISC-V question included — and the one                         probes now run an equal-operand and a mixed-sign instance
solver then wired (Z3, through the bridge) tolerated the mal-                    per construct (incident I23; the ratchet kept every previously
formation. Adding the second and third engines turned it into                    covered construct covered throughout). In the final round,
hard rejections: solve-step corroboration, not the squares,                      51 of 55 applicable mutants die at the square suite, the re-
caught it (incident I3). Between them the two incidents mark                     maining 4 at the compliance-derived benchmark, and none
the exact boundary of Assumption 2: shared code and shared                       escape. Three honest notes: zero escapes means this muta-
misreadings are what agreement cannot see, which is why                          tion family is now covered, not that the escape rate is zero;
the ledger keeps the emission library and the endpoint in-                       the authored branch questions caught nothing in any round
terpreters inside every branch verdict’s TCB — and why the                       (the derived benchmark subsumes them as a differentiator,
disjoint stacks of Figure 4 and the external differentials exist.                a finding in itself); and the denominator is one translator’s
6.7   An escape-rate estimate for the gate                                       emission space, not the platform.
The catalog above is mined from history and has no denom-                         The common-mode round. Single-leg mutation cannot
inator; the MUL/ADD blind spot proves the gate’s escape                          model the MUL/ADD class where both legs of the square
                                                                            19
                                                                                                                                       Christoph Kirsch


are wrong identically — so a second experiment injects ex-                        reachability question + platform-established ground truth
actly that (Table 10): six shared misreadings, each applied as
the same uniqueness-checked source patch to both the refer-                   arm A: unaided LLM                            arm B: LLM player
ence interpreter and the riscv-btor2 translator (in-memory                 (question text only, no tools)               (same question + repository)
shadows; the repository is untouched). The structural predic-
tions hold, measured: the square suite is blind on all six (both                                                  hurdy-gurdy: routes, squares,
legs agree on every probe), and so is expected-based grading                                                            solvers, checkers
in the poisoned world, where the benchmark’s ground truth
is derived by the mutated interpreter itself. What catches                            verdict                           verdict + machine-checked
                                                                            (say-so, high confidence)                        evidence artifact
the mutants are the gates outside the shared misreading —
Figure 7’s stack read as ordered by independence, each gate
                                                                                                  graded against ground truth
derived farther from the shared code than the last: four die at
cross-route disagreement with the Sail-derived branch, and
two survive even that — their misreadings never surface in              Figure 8. The two-arm player protocol of Table 11: one
the per-register values the derived questions sample — falling          fresh, context-free agent per question per arm, no retries.
only to the external Sail-simulator differential, which (run as         Both arms are graded against the same platform-established
a parallel column) catches all six. The round also caught its           ground truth; what differs by construction is what the verdict
own instrument, live: in its first run, slt-as-sltu escaped             rests on — arm B can take no unchecked step, so every answer
every gate — the slice’s compare vectors were all same-sign,            carries the evidence artifact of Table 11’s final column.
on which signed and unsigned comparison agree, so neither
the derived questions nor the differential’s executed streams
could see the difference (incident I24, the slice-level instance
of I23’s probe lesson, and the platform’s first measured full-
stack escape). The ratchet’s answer was upstream-faithful —             loops, caught both signedness traps, and factored 2147766287
rv64ui-slt’s mixed-sign and equal-operand vectors added                 by Fermat’s method in its head — but the evidence class of
to the slice — after which the round completes with zero                the answer. Every arm-A verdict rests on the model’s say-so
escapes. The honest reading mirrors Assumption 2’s scope                (all were reported at high confidence, so confidence would
exactly: against shared misreadings every gate built from               not have flagged a wrong one); every arm-B verdict car-
the shared reading is blind by construction, corroboration is           ries a machine-checked artifact: two-route agreement on
only as strong as the most independently derived anchor,                the RISC-V questions, hedged explicitly as bounded-𝑘 ver-
and that anchor’s vectors are themselves an instrument the              dicts resting on route fidelity; witness replays through the
discipline must audit.                                                  strict interpreters on the reachable eBPF/Python questions;
                                                                        and tier-raises to proved on the unreachable eBPF questions.
6.8   The other direction: an LLM plays the platform                    The sharpest contrast is the bounded-factorization question:
The introduction’s two-directional experiment has, until                arm A answered correctly by recalling that 1073741789 is
here, reported only its build half. This subsection is a first,         the largest prime below 230 — opaque memory, exactly the
deliberately small evaluation of the player half: 12 reach-             evidence the calculus cannot grade — while arm B produced
ability questions with platform-established ground truth                a 17 MB LRAT certificate re-validated by the formally veri-
(6 reachable / 6 unreachable, spanning RISC-V signedness                fied checker, with the trusted base named. One player even
and load-width traps, eBPF square-residue and bounded-                  devised its own positive control unprompted (flipping the
factorization questions, and Python assert-violability), posed          load question’s target to the sign-extended value and con-
to fresh, context-free frontier-LLM agents under two proto-             firming reachable on both routes). Four limitations, stated
cols (Figure 8). Arm A (unaided) received only the question             plainly: the protocol scripted which platform entry points
text, instructed to answer by reasoning with no tools. Arm              to use (the players executed and interpreted; they did not
B (player) received the same question plus the repository               discover the platform cold); the subject model is from the
and the head-construction snippet, instructed to decide via             same family that built the platform; the grading is partly
the platform and report the verdict with its evidence basis.            circular — ground truth is platform-established and arm B
One agent per question per arm, no retries; Table 11 lists the          answers via the platform, so arm B can fail essentially only
questions and both arms’ verdicts with each arm-B answer’s              by mis-operating or misreading the tools; and 12 questions at
evidence artifact; prompts, ground truths, per-run outputs,             this size cannot separate the arms on correctness — questions
and grading are in the artifact (results/llm_player/).                  hard enough that unaided reasoning actually fails are the
    Both arms scored 12/12. That is the honest headline, and            obvious next step. (Both protocol limitations are removed,
it reframes what the platform buys at this question scale: not          and the separation produced, by the post-snapshot rerun of
raw accuracy — the unaided frontier model simulated the                 §6.14.)
                                                                   20
Untrusted Authors, Trusted Answers


Table 11. The LLM-player experiment: 12 ground-truthed questions, two arms. Arm A (unaided) answers from reasoning
alone; arm B answers via the platform. A ✓ means the verdict matches the platform-established ground truth (R = reachable, U
= unreachable within the stated bound). Both arms are correct on all 12 — the contrast is the final column: every arm-B verdict
carries a machine-checked evidence artifact, where arm A rests on the model’s say-so (all arm-A answers were reported at
high confidence). Full question texts, per-run transcripts, and verbatim evidence bases: results/llm_player/ in the artifact.

                     Q      Question                                        Truth      Arm A     Arm B   Arm-B evidence artifact
                     R1     RISC-V loop: 𝑥 1 =15 within 𝑘=25                 R          ✓         ✓      two-route agreement
                     R2     RISC-V loop: 𝑥 1 =16 within 𝑘=25                 U          ✓         ✓      two-route agreement (bounded)
                     R3     srli (logical) 0xF..F8 ≫ 60: 𝑥 1 =15             R          ✓         ✓      two-route agreement
                     R4     srai (arithmetic) ≫ 60: 𝑥 1 =15                  U          ✓         ✓      two-route agreement (bounded)
                     R5     lb (sign-ext.) of byte 0x84: 𝑥 3 =0x84           U          ✓         ✓      two-route + self-devised positive control
                     R6     lbu (zero-ext.) of byte 0x84: 𝑥 3 =0x84          R          ✓         ✓      two-route agreement
                     E1     eBPF 𝑥 ·𝑥 mod 264 = 3                            U          ✓         ✓      proved: LRAT re-validated by cake_lpr
                     E2     eBPF 𝑥 ·𝑥 = 4                                    R          ✓         ✓      z3 + native btormc; witness replayed
                     E3     𝑥 ·𝑦 = 1073741789, 𝑥, 𝑦 ∈ [2, 216 +1]            U          ✓         ✓      proved: 17 MB LRAT via cake_lpr
                     E4     𝑥 ·𝑦 = 2147766287, same range                    R          ✓         ✓      witness replay; factor pair exhibited
                     P1     Python assert: 𝑦=16 violable                     R          ✓         ✓      SMT model re-checked + CPython replay
                     P2     Python assert: 𝑦=15 violable                     U          ✓         ✓      unsat; per-run-checked predicted route


Table 12. Route cost for the RISC-V loop question (𝑘=25 un-                                  twice-and-diff determinism check passes on both routes. The
rolling): whole-route translation, cold vs. warm (the content-                               numbers say the honest overhead of the whole discipline —
addressed cache of Proposition 3.9), Z3 decide time, byte-                                   checking every hop, re-running for determinism, replaying
determinism (twice-and-diff), and artifact size.                                             witnesses — is small against the solver call it wraps. Table 13
                                                                                             probes where the pipeline stands as questions grow, on two
Route                cold (ms)      warm (ms)      decide (ms)       det.   artifact         axes: unrolling the summation loop to 𝑁 =100 (𝑘=505, a 4 MB
RISC-V, direct                5           <0.1                55     ✓       201 kB          artifact) keeps whole-route translation under 0.1 s and the de-
RISC-V, via Sail              6            0.1                44     ✓       209 kB          cide under 1 s, growing roughly linearly; and the certified tier
                                                                                             survives the bounded-factorization family from propagation-
                                                                                             size to search-size — certificates growing from 25 kB to an
Table 13. Scalability probes on two axes. Left: the
                                                                                             11.8 MB LRAT, each re-validated by the verified checker in
summation-loop question at growing bounds (𝑥 1 =
                                                                                             seconds. Neither axis reaches industrial scale, but both cross
𝑁 (𝑁 +1)/2 after 𝑁 iterations; reachable at every size), whole-
                                                                                             the region where “toy” criticisms live: the pipeline’s costs
route translation and Z3 decide time. Right: the certified tier
                                                                                             grow smoothly, with no cliff through the measured range.
on the bounded-factorization family at growing factor widths
— certificate sizes grow from tens of kilobytes to megabytes                                   6.10   Post-snapshot: constraint enforcement across
and cake_lpr re-validates each.                                                                       engines
                                                                                             The first of the exhibit families to graduate to a measurement
      Loop question       verdict      translate (s)   decide (s)     artifact
                                                                                             — stamped with its own commit in Table 14’s caption; unlike
      𝑁 =5, 𝑘=30          reachable    0.01                   0.04     240 kB                every table above, its numbers postdate the snapshot. The
      𝑁 =20, 𝑘=105        reachable    0.02                   0.10     830 kB                shared BTOR2 evaluator enforces environment constraints
      𝑁 =50, 𝑘=255        reachable    0.04                   0.27    2054 kB
      𝑁 =100, 𝑘=505       reachable    0.07                   0.55    4093 kB
                                                                                             with the per-frame reading (per-row observables; a violating
                                                                                             row ends the run; a bad counts only on a constraint-valid
Certified question                     outcome      DRAT       LRAT         time (s)         row), and wiring that enforcement surfaced a latent bridge
8-bit factors, target 65521            certified    27.3 kB    24.7 kB           0.2
                                                                                             defect of independent interest: asserting constraints globally
12-bit factors, target 16777213        certified    0.2 MB     64.1 kB           0.3         over the unrolling masks a bad reached on a valid prefix
16-bit factors, target 2147483647      certified    2.8 MB     11.8 MB           4.9         before a later, inevitable violation — and disagrees with the
                                                                                             native checkers on exactly that system. Table 14 turns that
                                                                                             episode into a benchmark: nine authored systems whose
6.9     Performance, determinism, and scale                                                  ground truth holds by construction — reaches on valid pre-
Translation is not the cost center (Table 12): whole-route                                   fixes (single and double guards, short and long windows,
translation of the loop question (𝑘=25 unrolling, ∼200 kB                                    through a constrained input), and unreaches that exist only
of SMT-LIB) is ∼5 ms cold and a sub-millisecond content-                                     because of a constraint, only beyond a truncation, only on
addressed cache hit warm (Theorem 3.9 cashed in), against                                    an invalid row, or only beyond the bound — each decided
a Z3 decide in the tens of milliseconds on either route; the                                 natively (btormc), bridged (the per-frame encoding, z3), and
                                                                                        21
                                                                                                                                 Christoph Kirsch


Table 14. The constrained corpus: nine authored BTOR2 sys-               Table 15. Cost calibration for the books: 5 repeated capped
tems with by-construction ground truth (5 reachable / 4 un-              route-grader runs over the RISC-V head (fresh subprocess
reachable), each decided natively (btormc, canary-controlled             and ledger file each, so the translation cache swallows no
bounded exhaustion), bridged (the per-frame encoding, z3),               record; the grader’s own probe cap applies). Top: pooled per-
and corroborated by the shared evaluator — witness replay                hop cost profiles — translate and square-oracle (o) medians
on the reachable rows (both the bridged model’s carry-back               — and the bridged decide per engine. Middle: per-repetition
and btormc’s .wit), seeded no-bad runs on the unreachable                route translate totals (median and worst repetition) and, per
rows (r = reachable, u = unreachable within the bound).                  route, in how many repetitions the annotated report marked
Below the rule, the structural controls; the first keeps the             it dominated — the mark’s coherence and stability are the
historical global constraint reading as an instrument and                measurement; both routes stay listed at equal assurance and
measures what it masks. Post-snapshot measurement at com-                direction, no scalar ranking. Bottom: the honesty invariants,
mit 758b1f2 (2026-07-15).                                                executable. Timings are host-tagged (single machine); the
                                                                         corpus is the grader’s capped slice, so the numbers calibrate
System                      𝑘 Truth Native Bridged Evaluator             the instrument, not the platform’s workload. Post-snapshot
                                                                         measurement at commit b6e1d89 (2026-07-15).
valid-prefix-reach        5 r        r     r       replay ✓
two-guards-reach          6 r        r     r       replay ✓
late-window-reach         8 r        r     r       replay ✓                 Hop / engine               𝑛 median (ms)        p90 (ms)    o (ms)
vacuous-constraint        4 r        r     r       replay ✓
constrained-input-reach 2 r          r     r       replay ✓                 btor2-smtlib             235          0.543        0.733        —
constraint-blocked-input 3 u         u     u       no bad ✓                 riscv-btor2              120          0.550        0.715     1.439
truncated-before-bad     12 u        u     u       no bad ✓                 riscv-sail               120          0.016        0.025     0.083
invalid-row-bad           5 u        u     u       no bad ✓                 sail-btor2               120          0.558        0.727     1.465
bound-scoped-unreach      1 u        u     u       no bad ✓                 decide[z3]                10          3.305        6.870        —

global reading, valid-prefix-reach   unreach — the reach masked ✓           Route (translate total) reps        median          max marked
vacuous constraint vs. none          verdicts equal ✓                       direct (riscv-btor2)       5          1.084        1.109       1/5
blocked input, constraint removed    flips to reach ✓                       via Sail (3 hops)          5          1.102        1.144       4/5
                                                                            mark coherent (never against the measured totals)               ✓
                                                                            finding: totals tie within spread — no signal in the mark
corroborated by the shared evaluator: witness replay on                     empty ledger: unmeasured (never zero), no dominance             ✓
every reachable row (both the bridged model’s carry-back                    one route measured: still no dominance                          ✓
and btormc’s .wit replayed through the strict interpreter),
seeded no-bad runs on every unreachable row. All nine agree
with ground truth in both polarities, and the defective global           pooled profiles put numbers on the platform’s cost shape
reading, kept as an instrument, still masks the valid-prefix             at probe scale: the two lowering hops and the bridge each
reach — the permanent negative control, beside the additive              translate in ∼0.5 ms median, the RISC-V→Sail front is thirty
one (a vacuous constraint moves no verdict) and the blocking             times cheaper, square-oracle checks run ∼1.4 ms, and the
one (removing the constraint flips the blocked system back).             bridged decide dominates everything at ∼3 ms median —
Three honesty notes: the corpus is authored and deliberately             consistent with the snapshot’s finding that translation is not
tiny (nine systems, one operator family), constructed to pin             the cost center (§6.9). The finding is in the middle block:
the semantic corners of the constraint directive rather than             on this host the two routes’ translate totals tie within the
to sample a population; the evaluator corroborates — replay              repetition spread (medians ∼1.1 ms, 𝜇s apart), and at a tie the
and seeded runs — it never decides; and agreement here                   report’s dominance mark carries no signal — it is computed
shares the BTOR2 emission surface all three deciders con-                on raw medians with no noise margin, and across calibration
sume, so a shared misreading of the directive itself would               runs it pointed both ways. What the benchmark certifies
pass — the mutation discipline of §6.7 applies and is future             instead is the mark’s coherence — pooled and per repetition,
work for this family (tools/constraint_corpus.py; the                    a mark never points against the measured totals — and the
experiment is also a permanent test).                                    two honesty invariants, run executable: an empty ledger
                                                                         reads unmeasured, never zero, and computes no dominance;
6.11     Post-snapshot: cost calibration for the books                   a ledger measuring only one route still computes no domi-
The books’ cost side, calibrated (Table 15). The instrument              nance, because dominance needs complete measurement on
is the CI entrypoint itself — the capped route-grader — run              both sides. Three honesty notes: the timings are host-tagged
five times over the RISC-V head, each repetition a fresh sub-            and single-machine by design (profiles never mix machines
process with its own ledger file (a warm content-addressed               — the CI runner class, where the grader also runs, keeps its
cache translates nothing, so a warm run would record noth-               own books); the corpus is the grader’s capped probe slice,
ing: the repetition protocol is part of the calibration). The            so these numbers calibrate the instrument, not a workload;
                                                                    22
Untrusted Authors, Trusted Answers


Table 16. The question campaign: 25 authored questions                      Table 17. The abstraction benchmark. Top, the authored
whose first failing obstacle is known by construction — the                 block: free-set havoc on the decoy-𝑀 family (the advisor’s
five-obstacle demand taxonomy plus seven answerable con-                    zero-loss set) — the bridge’s SMT artifact (kB) and its de-
trols spanning every pass mechanism (feasible routes; an                    cide time (ms), exact→abstracted, verdicts preserved and the
assurance floor met by declared grade; a floor met by branch                universal transferring. Bottom, the HWMCC slice: six bit-
corroboration) — run through the diagnosis against the live                 vector instances from the 2019–2024 corpora, streamed-with-
registry with a fresh ledger. “Targets” counts the recommen-                pin (mirror commit 57174f5d6f57, sha256 per instance),
dation board’s rows per obstacle: aggregation is per genera-                each ingested through the platform’s own stack, decided ex-
tion target, so the three cost questions (three sources, one                actly (btormc, 𝑘=20, r/u = reachable/unreachable within the
hub inventory) share one reduction row. Below the rule, the                 bound), then CEGAR-localized: havoc the advisor’s ladder
instrument checks. Post-snapshot measurement at commit                      prefix, refine on spurious counterexamples (each caught by
e304a40 (2026-07-16).                                                       replaying the witness at the source, havoc inputs filtered),
                                                                            and report where the loop converges — states still havocked
    Obstacle (constructed)   𝑛                 diagnosed     targets        / total (𝑛r = rounds, 𝑛s = spurious) — and that the converged
                                                                            verdict agrees with the exact one. Post-snapshot measure-
    connectivity             4                        4/4         2
    loss                     4                        4/4         4         ment at commit b3e1323 (2026-07-16).
    shape                    4                        4/4         4
    cost                     3                        3/3         1          Authored                   SMT kB       decide ms
    trust                    3                        3/3         3
    answerable controls      7                        7/7         —          decoy-2                      47.6→6.9 68→9                       ✓
                                                                             decoy-4                      92.0→9.6 16→7                       ✓
    controls append no demand record                             ✓           decoy-8                      181.9→14.8 26→8                     ✓
    6 verbatim re-asks add 0 distinct questions                  ✓           cegar-chain: 4 spurious, 5 rounds, converges to the free set ✓
    origins displayed apart (campaign vs. organic, 3 rows)       ✓           true-cex: reachable via the abstraction; source replay confirms ✓
    diagnosis read-only (registry unchanged)                     ✓           sharp-boundary: a cone state havocked — spurious; replay refutes ✓
                                                                             HWMCC instance             family       exact       localization
and the tie finding names a concrete next step for the route                 bin-suffix-5            sosylab’24      u 0.11s     0/6 (4r, 3s) ✓
report — a declared noise margin below which no dominance                    trex02-1                sosylab’24      u 0.11s     3/7 (1r, 0s) ✓
is marked (tools/cost_calibration.py; the experiment                         benchmark04_conjunctive sosylab’24      u 0.38s     0/8 (5r, 4s) ✓
                                                                             phases_2-1              sosylab’24      r 0.37s     0/8 (5r, 4s) ✓
is also a permanent test).                                                   analog_estimation       mann’19         r 0.01s     2/5 (1r, 0s) ✓
                                                                             adding.5                beem’19         u 0.10s     5/10 (1r, 0s) ✓
6.12   Post-snapshot: a question campaign for the
       books
The economy’s front half — diagnosis to recommendation                      zero distinct questions (dedup is by question identity); the
— measured (Table 16). Twenty-five authored questions are                   same question arriving from an organic session and a syn-
posed through why-not against the live registry, eighteen                   thetic campaign shows both origins, displayed apart, on its
of them constructed so that a known obstacle fails first —                  row — the auditability that keeps manufactured demand
routes that end short of every hub (connectivity), observ-                  from laundering into evidence (§5.3); and the diagnosis is
ables no head projection keeps (loss), question shapes no hub               read-only against the registry. Two honesty notes: the cor-
declares (shape), spent verdicts on feasible routes (cost), and             pus is authored, so this measures the diagnosis’s correctness
assurance floors that single-route sources cannot meet (trust)              on constructed ground truth, not its coverage of questions
— beside seven answerable controls that span every way a                    players actually ask — an organic corpus accumulates only
question can pass: feasible routes enumerated, a floor met by               as the platform is played; and the accuracy is of the diagno-
declared grade (Python’s predicted head), and a floor met                   sis, not the recommendations — whether a named target is
by branch corroboration (both ISAs, and the C spine through                 worth building stays the human judgment the board explic-
its diverse segment). The diagnosis names the constructed                   itly declines to make (tools/question_campaign.py; the
obstacle, first, in all eighteen cases, with exactly one demand             campaign is also a permanent test).
record written per failure; the seven controls come back an-
swerable and append nothing — the books never record an                     6.13   Post-snapshot: the direction axis, measured
answered question. The board then aggregates the eighteen                   The direction axis of §3.4, exercised end to end (Table 17).
records to fourteen generation targets, and the aggregation                 The authored block runs on controlled ground truth. Hav-
is per target, not per question: the three cost questions, from             ocking the advisor’s free set — the states its cone analysis
three different sources, share the one reduction row that                   proves cannot move the question — preserves the verdict
names the hub’s registered abstraction dials. The instrument                on every decoy-𝑀 instance while the bridge’s SMT artifact
checks close the loop: six questions re-asked verbatim add                  shrinks by an order of magnitude (the hub encodes every
                                                                       23
                                                                                                                            Christoph Kirsch


transition it is handed; localization is what keeps it from             Table 18. The player experiment, v2 — unscripted, over
being handed dead update towers — preparing this mea-                   MCP: 8 bounded BTOR2 reachability questions (4/4 polarity
surement caught exactly that: the translator originally left            split), ground truth established by bridge+btormc agreement
the orphaned logic in its emission, and the artifact grew;              with witnesses replayed, before any run. Arm A reasons
v0.2 sweeps it, a versioned non-extension bump). Decide                 unaided (confidence h/m/l in parentheses); arm B may touch
time is reported as measured, and its near-parity is a find-            the platform only through gurdy mcp — no scripted entry
ing, not a disappointment: engines already refuse to branch             points, tool discovery included. One fresh agent per question
into satisfiable-independent transitions, so the free set is            per arm, no retries. The evidence column is arm B’s decisive
free for everyone — what the abstraction buys is the artifact           artifact. Recorded runs of 2026-07-16; the section formats, it
every downstream encoder, cache, and replay pays for, and               does not re-run (results/llm_player_v2/).
the CEGAR capability inside the cone. The loop itself is the
cegar-chain row: abstracted too aggressively on purpose, it               Question                 Truth A     B     B’s evidence
yields four spurious counterexamples, each caught by source               Q1: counter, hit@57, 𝑘=60 r   r (h) r      replay@57
replay and each un-havocking one ladder rung, converging to               Q2: same, hit@36, 𝑘=30    u   u (h) u      unsat + 𝑘-bracket
exactly the advisor’s free set with the universal verdict trans-          Q3: factor semiprime      r   r (h) r      replay + pinned factors
ferring (Theorem 3.11); the true-cex row is the other half                Q4: factor a prime        u   r (l) × u    unsat + planted ctl
                                                                          Q5: trex02-1              u   u (h) u      unsat + advisor + ctl
of the asymmetry (a reachable verdict believed only after the
                                                                          Q6: phases_2-1            r   r (h) r      replay@3
source replay confirms it), and the sharp-boundary control                Q7: adding.5              u   u (h) u      unsat + sem. probes
havocs one state inside the cone and must — and does — go                 Q8: LCG, hit@7            r   r (h) r      replay@7 + recompute
spurious. The HWMCC block then takes the same machinery                   Correct                       7/8    8/8
to six bit-vector instances from the 2019–2024 competition
corpora, streamed-with-pin (BENCHMARKS.md’s ingestion
discipline: mirror commit plus per-instance sha256). All six
ingest through the platform’s own stack — parse, shared-                interface is the whole platform: no head-construction snip-
evaluator run, reduction advisor — and preparing the slice              pets, no named entry points, no reading source or docs. Tool
caught a real defect: the beem instance’s negated node ref-             discovery is part of the task, and every agent performed it
erences crashed the evaluator with an untyped abort and,                cold — wrote a stdlib JSON-RPC driver, listed the ten tools,
worse, silently narrowed the cone analysis (a dependency                and picked the one decision call. The questions are harder in
hidden behind a negation left the cone — an unsound free set);          exactly one calibrated way: each is a bounded BTOR2 reach-
both are fixed and locked by tests, and the instance now de-            ability question given verbatim (constraint-guarded modu-
cides identically native and bridged. The localization column           lar counters, 17-bit bounded factorization, three ingested
is the honest news: on three of six instances CEGAR con-                HWMCC instances including the negated-refs beem proto-
verges with states still havocked — adding.5 stays unreach-             col, a 64-bit LCG orbit), with ground truth established before
able with half its protocol state havocked, trex02-1 with 3             any run by bridge–btormc agreement and witness replay.
of 7 — while on the other three it walks all the way back to            The result is the separation v1 could not produce: arm A 7/8,
the exact system, which is what a competition-curated cone              arm B 8/8, and the miss is exactly where the platform’s floor
should often force. Two honesty notes: the free set is empty            exceeds unaided cleverness — asked whether 1676656651 fac-
on every competition instance (curators do not ship dead                tors in range, the unaided model exhausted trial division and
state), so all localization here is CEGAR-earned inside the             a Fermat pass, then guessed reachable on the meta-heuristic
cone; and six instances at 𝑘=20 measure the machinery, not              that benchmark constants are planted semiprimes (the con-
the corpus — HWMCC at competition scale remains future                  stant is prime; the run took 34 minutes and was the experi-
work (tools/abstraction_bench.py; the authored block                    ment’s only low-confidence answer — this time confidence
is a permanent test).                                                   did flag the error, one instance, not a calibration claim). Arm
                                                                        A’s other seven answers remain formidable — it decoded
6.14   Post-snapshot: the player experiment, v2 —                       two HWMCC pc-encodings, recognized and bounded the
       unscripted, over MCP                                             beem adding protocol, and iterated a 64-bit LCG seven steps
The first player experiment (§6.8) named its own protocol lim-          by hand, digit-exact — which sharpens, rather than dulls,
itations: the entry points were scripted, and twelve questions          the point: at any difficulty the unaided answer is opaque re-
at that difficulty could not separate the arms on correctness.          call or heroic arithmetic, graded only by its own confidence,
This rerun removes both (Table 18). The platform’s player               while every arm-B verdict carries the artifact the calculus
surface is now a machine interface — the MCP server (gurdy              grades. What no protocol scripted is the finding of the ex-
mcp, stdio JSON-RPC; the same enumerated, advisory tools                periment: the players reinvented the platform’s own discipline
as the library, exposure pinned by test) — and arm B receives           — one bracketed 𝑘=35/36 to pin the bound convention be-
only the question, the repository path, and the rule that this          fore trusting a negative; one pinned its hand-derived factors
                                                                   24
Untrusted Authors, Trusted Answers


with added constraints to machine-check them when the wit-           DimSum’s decentralized multi-language graph with wrap-
ness exposed no inputs; three devised positive controls so an        pers [36]. These works confront vertical composition of sim-
unsat could not be a vacuous pipeline; one probed negated-           ulations up to differing observations — the habitat of our sup-
reference semantics on self-authored one-bit models before           port condition, which in their terms is the congruence/well-
believing the main verdict; and every negative was hedged,           definedness requirement on the mediating map; CompCert
unprompted, as a bounded claim resting on the bridge — the           sidesteps it by fixing one global event type, CompCertO ne-
exact evidence asymmetry of Theorems 3.17 and 3.18, articu-          gotiates it through simulation conventions, DimSum through
lated by subjects that were never told it. Honesty notes: the        wrappers. We claim no mathematical novelty for the con-
subject model stays in the builders’ family; eight questions         dition (Theorem 3.6 is a one-line congruence); what this
measure the protocol, not a population; ground truth and             paper adds relative to that line is a different regime and dif-
arm B share the platform’s deciders, so the discriminating           ferent bookkeeping: edges that are not uniformly proved,
arm is A; and one arm-A prompt carried a transcription slip          trace-equality squares that are decidable per run rather than
with its correction inline (recorded), while four arm-B first        proved once, an explicit syntactic keep/loss computation for
launches died on an infrastructure rate limit before any tool        routes, and the grade/class algebra for composing hetero-
call and were relaunched fresh — no graded run was retried           geneous evidence — with the trade-off stated plainly, since
(results/llm_player_v2/; questions, per-run records, and             equality-up-to-projection is the right notion only for near-
all sixteen verbatim final messages).                                structure-preserving translations, not optimizing compila-
                                                                     tion (§3.1).
6.15    What remains narrated
                                                                        Semantics-first frameworks. The K framework derives
Every number above §6.10 is the dated snapshot, regener-             interpreters, symbolic executors, and provers from one se-
able from the artifact by one script; nothing built since is         mantics [33], with KEVM [10] and KWasm as flagship in-
mixed into those tables. The post-snapshot sections (§6.10–          stances; Sail does the same for ISAs [2], and ISA-conformance
§6.14) are the former exhibit list, graduated: every family          frameworks such as riscv-formal [45] prefigure the spec-
this subsection once narrated — constraint enforcement, the          enumerated per-construct yardsticks of Theorem 5.1. These
books in CI, the demand board, the refinement demonstra-             are our closest philosophical relatives, and our platform con-
tion, HWMCC ingestion — is now a measured table with its             sumes their artifacts (the Sail RISC-V and Arm models anchor
own commit stamp (the trust advisor’s independence judg-             one of each ISA’s two routes). The difference is what car-
ments are exercised inside the campaign’s trust rows and             ries trust: a semantics-first framework is a monoculture —
floor-met-by-corroboration controls, §6.12), and the player          every derived tool inherits the one semantics and the one
experiment’s named protocol fixes are run (§6.14). What              derivation pipeline — whereas our unit of trust is agreement
remains future measurement is scale: HWMCC beyond a six-             between independently derived translations (Assumption 2),
instance slice, an SV-COMP-scale compliance campaign, or-            with the framework structured so routes diverge over inde-
ganic (rather than authored) question corpora for the books,         pendent semantic artifacts. N-version programming [3] and
and a cross-family subject model for the player arms.                differential testing [22, 46] exploit the same independence
                                                                     resource — and Knight and Leveson’s experiment [14] is
7      Related work                                                  the standing caution that independence must be argued, not
   Certified compilation and translation validation.                 assumed, which is why Assumption 2 is explicit, scoped to
CompCert [18] and CakeML [16] prove one translator                   the diverse prefix, and confronted with our own common-
correct once; translation validation [26, 30] and its modern         mode incidents (§6.6). We give the possibilistic account of
descendants [19, 38] validate each run of one translator, and        what agreement does and does not establish (Theorem 3.16)
validators can themselves be verified [42]. Credible compi-          and wire it into a compositional calculus rather than a test
lation [32] — per-run validation of a compiler’s own result          harness.
— is a direct ancestor of re-establishment (Theorem 3.14).
In our vocabulary these are grades of a single edge; our                Certificates, witnesses, and certifying algorithms.
contribution is the graph of edges of heterogeneous grade            Proof-carrying code [25], certifying algorithms [21], cer-
— how faithfulness, loss, and assurance compose along                tified model-checking [24, 28, 47], and checked solver
routes, how per-run validation re-establishes hops that carry        proofs (DRAT [44], verified checkers [41], Alethe/Carcara
squares, and how independent routes corroborate.                     [1]) all instantiate the producer/checker split our proved
                                                                     grade requires; SV-COMP’s violation/correctness-witness
   Compositional compiler correctness. Composing simu-               ecosystem [4] is the deployed, cross-tool form of the ex-
lations across passes and languages is a rich line: Composi-         istential/universal asymmetry our end-to-end theorems
tional CompCert [39], parametric inter-language simulations          state; Sledgehammer’s checked reconstruction [5] is the
[27], CompCertO’s simulation conventions [15], certified ab-         same untrusted-discovery/trusted-replay split inside a proof
straction layers [9], multi-language semantics [20, 29], and         assistant; and SMT-COMP’s model-validation tracks [43]
                                                                25
                                                                                                                         Christoph Kirsch


institutionalize witness re-checking at the solver level. What           evidence with weakest-link meets, per-run re-establishment,
we add is the composition through a translation graph: an                and the trusted-base ledger.
existential answer’s certificate is its source-level replay after
carry-back (Theorem 3.17), while universal answers compose
certificate checking with route fidelity (Theorem 3.18). The               LLMs and formal tools. Recent systems couple LLM gen-
carry-back itself has verified precedent — decompilation into            eration with solver-checked validation [40]. Our platform is
logic [23] makes the lifter a proved component — and our                 built for that player — an LLM chooses questions and routes
contribution is making it a mandatory, per-pair component                but every step it takes is deterministic, graded, and checked
of every edge rather than a per-tool artifact.                           — and §5.1 reports the build half of the two-directional ex-
                                                                         periment of Section 1: the translators themselves were LLM-
    Moving programs to answerable representations. Veri-                 written, and correctness was carried by the architecture, not
fied lifting [11] and the broad practice of encoding programs            by author trust. §6.8 reports a first controlled experiment on
into solver logics (BMC, symbolic execution) motivate the                the player half.
platform’s existence; Why3 [8] is the closest deployed rela-
tive of the hub pattern — one verification-condition language
translated to many provers of heterogeneous trust — though               8   Limitations and conclusion
its edges carry no per-run squares and no declared loss; re-                Limitations. This is a dated snapshot of a system de-
finement stacks such as seL4’s [13, 38] show multi-layer                 signed to ratchet, and its numbers say so: coverage is deep-
semantic preservation with uniform, proof-backed layers.                 est on the spine (all 96 RV64IMC constructs conjoined and
Our setting differs in admitting layers that are not uniformly           composing losslessly to SMT-LIB on both routes; the in-
proved — pinned compilers, agent-written translators, third-             scope eBPF set complete) and deliberately partial elsewhere
party models — and making their heterogeneous trust first-               (EVM at 86 of 144 opcodes; Wasm at 54 of its 75-item de-
class rather than a threat to the statement. Combining het-              clared inventory, without loop/br; Python an integer sub-
erogeneous verification evidence with recorded provenance                set with bounded unrolling). Coverage is now measured
is itself prefigured by the Evidential Tool Bus [34]; the grade/-        as Theorem 5.1’s actual conjunction over language-owned
class algebra and the ledger are a formalized cousin.                    inventories wherever a pair has a decidable square (§6.1);
                                                                         the predicted-grade hops still discharge faithfulness per
   Abstraction and refinement. The over-approximating                    run rather than per construct, and the A64 inventory, while
half of the directional square is the simulation half of ab-             language-owned, is a declared slice of a much larger ISA.
stract interpretation’s Galois reading [7]; the loop it closes           Universal answers are bounded claims wherever BMC-style
at the platform level — ask on the abstraction, transfer the             unrolling caps apply, and rest on universal-tier hypotheses
universal verdict, replay the existential one, refine on a spuri-        that per-run evidence and §3.8’s tested surrogates corrobo-
ous counterexample — is counterexample-guided abstraction                rate but do not entail (Theorem 3.18). The verified portion
refinement [6]; and the first registered instance, havocking             of the C spine begins at the compiled binary: the compiler
caller-named state, is localization reduction [17]. What the             hop has no square and contributes reproducibility plus a
calculus adds is not a new abstraction but a different life              differential, not faithfulness (§3.5). The proved tier’s certi-
cycle for one: the abstraction is a registered pair with a de-           fied row is inhabited with a formally verified checker at the
clared direction and witness embedding, its soundness on                 anchor (cake_lpr, §6.5), on one trivial and one certificate-
the corpus is a per-program decidable check along that em-               scale instance (an 11.8 MB LRAT); the residual TCB is the bit-
bedding rather than a fixed-point argument, its refinements              blaster’s BV→CNF step, and a certified claim is per-question
are durable, graded artifacts rather than solver-internal state,         and bounded, never a proof of a pair. Interpreter adequacy
and its parameters remain the player’s — advised (cone of in-            remains an assumption discharged empirically at modest
fluence, observed interval seeds) but never chosen for them              volume, and the diversity assumption behind branch cor-
(§3.4, §5.3).                                                            roboration is structural, not probabilistic — scoped to the
                                                                         diverse prefix, a boundary the common-mode round (§6.7)
   Fault tolerance, end to end. The paper’s vocabulary is                now measures directly: shared misreadings blind, by con-
deliberately that of fault-tolerant systems, because the con-            struction, every gate built from the shared reading; only an
cepts coincide: the square oracle is an acceptance test in               independently derived external anchor catches them. The
the recovery-block sense [31], making a silently wrong —                 compositional core of the calculus — including the 𝑛-ary
in effect Byzantine — translator fail-stop [37]; a branch is             route telescope and the specialization obligation of Theo-
dual modular redundancy whose comparator localizes rather                rem 3.18 — is mechanized in Lean 4 with a clean axiom audit
than votes; and the existential/universal asymmetry is the               (§3.8) — the directional square calculus included, lax tele-
end-to-end argument [35] for translation graphs. What the                scope and all (Theorems 3.10 and 3.11); the fieldwise loss
transplant adds is the compositional bookkeeping — graded                computation and the retiming case remain paper-stated.
                                                                    26
Untrusted Authors, Trusted Answers


   Future work. The gaps above are the roadmap: scale the                              RISC-V, and CHERI-MIPS. Proceedings of the ACM on Programming
compliance-derived benchmark of §6.3 to an upstream suite                              Languages 3, POPL (2019), 71:1–71:31.
taken binary-for-binary (which needs the machine-mode                              [3] Algirdas Avižienis. 1985. The N-Version Approach to Fault-Tolerant
                                                                                       Software. IEEE Transactions on Software Engineering SE-11, 12 (1985),
slice) and to SV-COMP-style C tasks; extend the escape-                                1491–1501.
rate experiments of §6.7 beyond one translator’s emission                          [4] Dirk Beyer, Matthias Dangl, Daniel Dietsch, Matthias Heizmann, and
space; widen the A64 slice toward the base ISA; and scale                              Andreas Stahlbauer. 2015. Witness Validation and Stepwise Testifica-
the player experiment beyond the eight-question rerun of                               tion across Software Verifiers. In ESEC/FSE.
§6.14, with subject models outside the builders’ family. Past                      [5] Jasmin Christian Blanchette, Sascha Böhme, and Lawrence C. Paul-
                                                                                       son. 2013. Extending Sledgehammer with SMT Solvers. Journal of
these measured gaps lies the intended trajectory: hurdy-                               Automated Reasoning 51, 1 (2013), 109–128.
gurdy is meant to evolve into an open platform that scales                         [6] Edmund M. Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut
in language support, where anyone — working with LLMs,                                 Veith. 2000. Counterexample-Guided Abstraction Refinement. In CAV
with agents, or by hand — develops a new pair against the                              (LNCS, Vol. 1855). 154–169.
calculus’s written contract and lands it in the repository                         [7] Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A
                                                                                       Unified Lattice Model for Static Analysis of Programs by Construction
through an ordinary pull request. The admission bar is the                             or Approximation of Fixpoints. In POPL. 238–252.
architecture, not the author: a pair arrives with its declared                     [8] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 — Where
projection, direction, and grade, its typed partiality, and a                          Programs Meet Provers. In ESOP.
square the harness runs on merge, and the ratchet (Theo-                           [9] Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao,
                                                                                       Xiongnan (Newman) Wu, Shu-Chun Weng, Haozhong Zhang, and Yu
rem 5.2) keeps every prior verdict standing as the graph
                                                                                       Guo. 2015. Deep Specifications and Certified Abstraction Layers. In
grows. The direction axis (§3.4) points the growth inward                              POPL.
as well as outward: not only more front-ends, but abstrac-                        [10] Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran
tion and property-transformation pairs — endo-edges on the                             Zhu, Philip Daian, Dwight Guth, Brandon Moore, Daejun Park, Yi
hubs — whose refinement loops make the graph denser in                                 Zhang, Andrei Stefanescu, and Grigore Roşu. 2018. KEVM: A Complete
reductions, with the lax telescope mechanized alongside the                            Formal Semantics of the Ethereum Virtual Machine. In CSF.
                                                                                  [11] Shoaib Kamil, Alvin Cheung, Shachar Itzhaky, and Armando Solar-
exact one (§3.8). Each such refinement is one turn of the                              Lezama. 2016. Verified Lifting of Stencil Computations. In PLDI.
loop of §1 and §2: diagnose the missing edge, generate it,                        [12] Christoph M. Kirsch. 2017. Selfie and the Basics. In Onward!
gate it, ratchet, re-ask — growth as a loop, with the books of                    [13] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
§5.3 keeping the demand that names each next edge, and a                               David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,
human hand on the registration valve.                                                  Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and
                                                                                       Simon Winwood. 2009. seL4: Formal Verification of an OS Kernel. In
                                                                                       SOSP.
   Conclusion. We proposed treating translations the way                          [14] John C. Knight and Nancy G. Leveson. 1986. An Experimental Evalua-
distributed systems treat processes: as components that fail,                          tion of the Assumption of Independence in Multiversion Programming.
whose failures are contained by architecture — declared pro-                           IEEE Transactions on Software Engineering SE-12, 1 (1986), 96–109.
jections, decidable squares, graded evidence, independent                         [15] Jérémie Koenig and Zhong Shao. 2021. CompCertO: Compiling Certi-
                                                                                       fied Open C Components. In PLDI.
routes, carried-back witnesses — rather than prevented by                         [16] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens.
universal proof. The calculus makes the composition of par-                            2014. CakeML: A Verified Implementation of ML. In POPL.
tial trust exact; the platform shows the discipline is buildable,                 [17] Robert P. Kurshan. 1994. Computer-Aided Verification of Coordinating
by agents, at measured (if modest) coverage; and the asymme-                           Processes: The Automata-Theoretic Approach. Princeton University
try theorems say where proof effort actually buys assurance.                           Press.
                                                                                  [18] Xavier Leroy. 2009. Formal Verification of a Realistic Compiler. Com-
The snapshot is the baseline; the ratchet is the roadmap.                              mun. ACM 52, 7 (2009), 107–115.
                                                                                  [19] Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and
Acknowledgments                                                                        John Regehr. 2021. Alive2: Bounded Translation Validation for LLVM.
                                                                                       In PLDI.
This work was co-funded by the Czech Science Foundation                           [20] Jacob Matthews and Robert Bruce Findler. 2007. Operational Semantics
under Grant No. 23-07580X and the European Union under                                 for Multi-language Programs. In POPL.
the project Robotics and Advanced Industrial Production                           [21] Ross M. McConnell, Kurt Mehlhorn, Stefan Näher, and Pascal
                                                                                       Schweitzer. 2011. Certifying Algorithms. Computer Science Review 5,
(reg. no. CZ.02.01.01/00/22_008/0004590).
                                                                                       2 (2011), 119–161.
                                                                                  [22] William M. McKeeman. 1998. Differential Testing for Software. Digital
References                                                                             Technical Journal 10, 1 (1998), 100–107.
                                                                                  [23] Magnus O. Myreen, Michael J. C. Gordon, and Konrad Slind. 2008.
 [1] Bruno Andreotti, Hanna Lachnitt, and Haniel Barbosa. 2023. Carcara:               Machine-Code Verification for Multiple Architectures: An Application
     An Efficient Proof Checker and Elaborator for SMT Proofs in the                   of Decompilation into Logic. In FMCAD.
     Alethe Format. In TACAS.                                                     [24] Kedar S. Namjoshi. 2001. Certifying Model Checkers. In CAV.
 [2] Alasdair Armstrong, Thomas Bauereiss, Brian Campbell, Alastair Reid,         [25] George C. Necula. 1997. Proof-Carrying Code. In POPL.
     Kathryn E. Gray, Robert M. Norton, Prashanth Mundkur, Mark Was-              [26] George C. Necula. 2000. Translation Validation for an Optimizing
     sell, Jon French, Christopher Pulte, Shaked Flur, Ian Stark, Neel Kr-             Compiler. In PLDI.
     ishnaswami, and Peter Sewell. 2019. ISA Semantics for ARMv8-A,
                                                                             27
                                                                                                                                      Christoph Kirsch


[27] Georg Neis, Chung-Kil Hur, Jan-Oliver Kaiser, Craig McLaughlin,                   1. By faithfulness of 𝑃1 at 𝑝 and 𝜋 ⊆ 𝜋1 , 𝜋 (𝐼𝐴 (𝑝)) =
     Derek Dreyer, and Viktor Vafeiadis. 2015. Pilsner: A Compositionally                 𝜋 (Λ1 (𝐼𝐵 (𝑞))).
     Verified Compiler for a Higher-Order Imperative Language. In ICFP.                2. By faithfulness of 𝑃 2 at 𝑞: 𝜋2 (𝐼𝐵 (𝑞)) = 𝜋2 (Λ2 (𝐼𝐶 (𝑟 ))).
[28] Aina Niemetz, Mathias Preiner, Clifford Wolf, and Armin Biere. 2018.
     Btor2, BtorMC and Boolector 3.0. In CAV.                                          3. Both 𝐼𝐵 (𝑞) and Λ2 (𝐼𝐶 (𝑟 )) lie in dom(Λ1 ) (the first by
[29] James T. Perconti and Amal Ahmed. 2014. Verifying an Open Compiler                   𝑝 ∈ dom(𝑃1 ), the second by 𝑝 ∈ dom(𝑃2 ◦ 𝑃 1 )). By
     Using Multi-language Semantics. In ESOP.                                             (𝜋 2 ⇒ 𝜋)-support applied to step (2): 𝜋 (Λ1 (𝐼𝐵 (𝑞))) =
[30] Amir Pnueli, Michael Siegel, and Eli Singerman. 1998. Translation                    𝜋 (Λ1 (Λ2 (𝐼𝐶 (𝑟 )))).
     Validation. In TACAS.                                                             4. Chaining (1) and (3): 𝜋 (𝐼𝐴 (𝑝)) = 𝜋 (Λ1 (Λ2 (𝐼𝐶 (𝑟 )))),
[31] Brian Randell. 1975. System Structure for Software Fault Tolerance.
     IEEE Transactions on Software Engineering SE-1, 2 (1975), 220–232.                   which is faithfulness of 𝑃2 ◦ 𝑃 1 at 𝑝 w.r.t. 𝜋.           □
[32] Martin Rinard and Darko Marinov. 1999. Credible Compilation. Tech-
     nical Report MIT-LCS-TR-776. MIT Laboratory for Computer Science.                 Directional pairs. For pairs with a non-identity witness
[33] Grigore Roşu and Traian Florin Şerbănuţă. 2010. An Overview of the            embedding (Theorem 3.4), the same four steps run per
     K Semantic Framework. Journal of Logic and Algebraic Programming
     79, 6 (2010), 397–434.
                                                                                   closing valuation, the three legs closed at 𝑥, 𝑊1 (𝑝, 𝑥), and
[34] John Rushby. 2005. An Evidential Tool Bus. In ICFEM.                          𝑊2 (𝑇1 (𝑝),𝑊1 (𝑝, 𝑥)); the composite’s square is then faithful-
[35] Jerome H. Saltzer, David P. Reed, and David D. Clark. 1984. End-to-End        ness along 𝑊2 ◦ 𝑊1 , with direction the meet 𝑑 1 ∧ 𝑑 2 . This
     Arguments in System Design. ACM Transactions on Computer Systems              form is machine-checked (lax_pasting; telescoped, DRoute.
     2, 4 (1984), 277–288.                                                         lax_route_pasting with DRoute.direction_exact_iff)
[36] Michael Sammler, Simon Spies, Youngju Song, Emanuele D’Osualdo,
     Robbert Krebbers, Deepak Garg, and Derek Dreyer. 2023. DimSum: A
                                                                                   — the chain above is its identity-embedding instance.
     Decentralized Approach to Multi-language Semantics and Verification.              Necessity of support. Without the support condition (The-
     Proceedings of the ACM on Programming Languages 7, POPL (2023).               orem 3.6) the theorem is false: let 𝐹𝐵 = {𝑔, ℎ}, 𝜋2 = {𝑔}, and
[37] Richard D. Schlichting and Fred B. Schneider. 1983. Fail-Stop Proces-         let Λ1 copy field ℎ into a 𝜋1 -kept source field. Take 𝑃2 faithful
     sors: An Approach to Designing Fault-Tolerant Computing Systems.              (it preserves 𝑔) but with Λ2 (𝐼𝐶 (𝑟 )) differing from 𝐼𝐵 (𝑞) on ℎ
     ACM Transactions on Computer Systems 1, 3 (1983), 222–238.
[38] Thomas Arthur Leck Sewell, Magnus O. Myreen, and Gerwin Klein.
                                                                                   — permitted, since ℎ ∉ 𝜋2 . The outer rectangle then disagrees
     2013. Translation Validation for a Verified OS Kernel. In PLDI.               on the copied field although both inner squares commute.
[39] Gordon Stewart, Lennart Beringer, Santiago Cuellar, and Andrew W.
     Appel. 2015. Compositional CompCert. In POPL.
[40] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024.                  A.2    Composed keep-set, and step granularity
     Clover: Closed-Loop Verifiable Code Generation. arXiv preprint
                                                                                   For fieldwise, step-aligned Λ1 (each kept source field 𝑓 com-
     arXiv:2310.17807 (2024).
[41] Yong Kiam Tan, Marijn J. H. Heule, and Magnus O. Myreen. 2021.                puted per step as 𝑓 = 𝜙 𝑓 ({ 𝑏.𝑔 | 𝑔 ∈ deps(𝑓 ) })), (𝜋 2 ⇒ 𝜋)-
     cake_lpr: Verified Propagation Redundancy Checking in CakeML. In              support holds iff deps(𝑓 ) ⊆ 𝜋 2 for every 𝑓 ∈ 𝜋; hence the
     TACAS.                                                                        largest admissible 𝜋 is keep = {𝑓 ∈ 𝜋1 | deps(𝑓 ) ⊆ 𝜋 2 } and
[42] Jean-Baptiste Tristan and Xavier Leroy. 2008. Formal Verification             support for it is checkable syntactically from the dependency
     of Translation Validators: A Case Study on Instruction Scheduling
                                                                                   sets.
     Optimizations. In POPL.
[43] Tjark Weber, Sylvain Conchon, David Déharbe, Matthias Heizmann,                  When Λ1 retimes — one source step corresponds to a win-
     Aina Niemetz, and Giles Reger. 2019. The SMT Competition 2015–                dow of target steps, as in C statements over ISA instructions
     2018. Journal on Satisfiability, Boolean Modeling and Computation 11,         — model Λ1 as a monotone window map 𝑤 from source step
     1 (2019), 221–259.                                                            indices to intervals of target step indices plus a fieldwise read
[44] Nathan Wetzler, Marijn J. H. Heule, and Warren A. Hunt Jr. 2014.
                                                                                   within each window. Support then requires deps(𝑓 ) ⊆ 𝜋 2
     DRAT-trim: Efficient Checking and Trimming Using Expressive
     Clausal Proofs. In SAT.                                                       for reads anywhere in the window, and additionally that the
[45] Claire Wolf. 2019. riscv-formal: A Framework for RISC-V Formal                window map itself be determined by 𝜋 2 -observables (e.g. by
     Verification. https://github.com/YosysHQ/riscv-formal.                        a kept program counter), since window boundaries influence
[46] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Finding             the projected output. Both conditions are again syntactic
     and Understanding Bugs in C Compilers. In PLDI.
                                                                                   given 𝑤 and the dependency sets.
[47] Emily Yu, Armin Biere, and Keijo Heljanko. 2021. Progress in Certify-
     ing Hardware Model Checking Results. In CAV.

                                                                                   A.3    Localization (Corollary 3.8)
A     Proofs                                                                       Contrapositive of the pasting theorem (Theorem 3.7) for two
A.1    Pasting (Theorem 3.7)                                                       hops. For 𝑛 hops, induct on the route: if the outer rectangle
We spell out the chain, including the domain side conditions                       over hops 1..𝑛 fails at 𝑝 but hop 1’s square passes at 𝑝, then by
elided in the paper’s proof sketch. Let 𝑝 ∈ dom(𝑃2 ◦ 𝑃 1 ),                        the two-hop case applied to (hop 1, rectangle over hops 2..𝑛)
i.e. 𝑝 ∈ dom(𝐼𝐴 ) ∩ dom(𝑇1 ), 𝑞 := 𝑇1 (𝑝) ∈ dom(𝑇2 ), 𝑟 :=                         the rectangle over 2..𝑛 fails at 𝑇1 (𝑝); recurse. Termination
𝑇2 (𝑞), 𝐼𝐶 (𝑟 ) defined, Λ2 (𝐼𝐶 (𝑟 )) ∈ dom(Λ1 ), and (from 𝑝 ∈                    yields a least failing hop 𝑖; within it, the square oracle’s
dom(𝑃1 ), 𝑞 ∈ dom(𝑃2 )) 𝐼𝐵 (𝑞) defined with 𝐼𝐵 (𝑞) ∈ dom(Λ1 )                      comparison yields the least failing step and a witnessing
and 𝐼𝐶 (𝑟 ) ∈ dom(Λ2 ).                                                            field.                                                          □
                                                                              28
Untrusted Authors, Trusted Answers


A.4    Weakest link (Proposition 3.13)                                  never lose (old verdicts preserved). Composition of exten-
Soundness: if every hop is universal on its fragment, iterate           sions is an extension. For the failure half: a non-extension
the pasting theorem (Theorem 3.7) over all 𝑝 in the com-                update changes some 𝐼 (𝑝), which can flip the verdict at 𝑝
posite fragment. If some hop is perrun, the same iteration is           for any pair whose square consumed it — justifying the
available exactly at programs whose per-hop images passed               versioned-event rule.                                      □
the oracle — the per-run set of the route. If some hop is only
replay, purity composes (Theorem 3.9) but no faithfulness               B    Construct inventories and probe corpora
statement is available for the route beyond it. Optimality:             Per-language construct inventories (the yardsticks of the
a route with a perrun hop entails no universal statement                paper’s Theorem 5.1) and the probe corpora behind every
(take a defect outside the checked set); a route with a replay          coverage figure in the paper’s Section 6 are enumerated
hop entails no faithfulness at all (take a pure but wrong               in the artifact — the per-language inventory modules
translator).                                                 □          (gurdy/languages/*/inventory.py), the per-pair inven-
                                                                        tories (gurdy/pairs/*/inventory.py), and the measured
A.5    Ratchet (Proposition 5.2)                                        coverage data (paper/results/data/); they are spec-
Let 𝐼 ′ ⊒ 𝐼 and let 𝑝 ∈ dom(𝐼 ). Every quantity in the faithful-        derived: the RISC-V RV64IMC opcode inventory, the full
ness square (Theorem 3.5) evaluated at 𝑝 reads only 𝐼 -values           144-opcode EVM inventory, the 126-construct eBPF inven-
on dom(𝐼 )-points, which 𝐼 ′ preserves; hence the verdict at 𝑝          tory slice (drawn from the 256-opcode space), the Wasm
is unchanged. Coverage monotonicity: cov’s per-construct                numeric/parametric/control inventory, the OpenSMILES
conjunction can only gain (new constructs enter dom) and                construct list, the Python-subset AST allow-list, and the two
                                                                        hubs’ operator inventories.




                                                                   29
