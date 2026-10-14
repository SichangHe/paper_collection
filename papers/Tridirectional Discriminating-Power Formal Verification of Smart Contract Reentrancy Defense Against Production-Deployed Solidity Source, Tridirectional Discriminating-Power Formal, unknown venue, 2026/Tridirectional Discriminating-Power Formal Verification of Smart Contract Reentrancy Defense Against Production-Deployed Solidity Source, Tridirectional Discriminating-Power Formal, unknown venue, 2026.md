                                                                                                                                                                                                 1




                                             Tridirectional Discriminating-Power Formal
                                             Verification of Smart Contract Reentrancy
                                            Defense Against Production-Deployed Solidity
                                                                Source
                                                                                                            Ray Iskander



                                                                                                                       ✦
arXiv:2606.01794v2 [cs.CR] 2 Jun 2026




                                        Abstract—We present the first machine-checked correctness proof of                 demonstrated at the first cross-protocol stress test (Compound v2 →
                                        the OpenZeppelin reentrancy-guard pattern against a Lean 4 state-                  Aave V3, within the lending-family domain; broader-family portability is
                                        machine model of production-deployed Solidity source with a compo-                 future work, §9.4).
                                        sition meta-theorem spanning multiple production protocols. All thirteen               We     release      the     full   Lean    4   source,  CI     gat-
                                        theorems are machine-checked in Lean 4 with zero sorry, zero user-                 ing     configuration,       and      reproduction    commands        at
                                        introduced axioms, and an axiom footprint bounded by [propext]                     https://github.com/rayiskander2406/qanary-contracts
                                        across the entire corpus — propositional extensionality, a standard                with reproducibility verified at tagged commit v1.6-phase7-closure
                                        classical axiom in Lean 4’s mathlib4; per-function inner lemmas are                (the post-audit content seal; the substantive proof substrate is
                                        kernel-only, master/wrapper theorems carry [propext]-only records,                 independently reproducible at v1.3-layer6-closure per Appendix
                                        and the Layer 6-D capstone composes exactly the union of the prior-                A.3).
                                        layer records by direct conjunction. The corpus is gated under continu-
                                        ous integration across four parallel verification blocks that re-check each
                                        theorem and its axiom record on every push.                                        1     I NTRODUCTION
                                             Smart contract reentrancy has caused over US$500M in cumulative
                                        documented losses since 2016, with the DAO 2016 attack alone draining              Smart contract reentrancy has been a foundational vul-
                                        ≈3.6M ETH and forcing a contentious hard fork that split Ethereum into             nerability class on Ethereum-style chains since the DAO
                                        two persistent chains. The OpenZeppelin ReentrancyGuard mutex                      2016 attack, yet the gap between widely-adopted defen-
                                        pattern has emerged as the de facto defense across most production                 sive coding patterns and machine-checked correctness guar-
                                        DeFi protocols, yet no prior formal verification effort has established its        antees remains uneven. This paper closes part of that
                                        discriminating power — the property that the guard pattern blocks at-              gap with the first machine-checked correctness proof of
                                        tacks against vulnerable instances, preserves correct execution for non-
                                                                                                                           the OpenZeppelin reentrancy-guard pattern against a Lean
                                        attacking transactions, and distinguishes structurally-adjacent safe and
                                        vulnerable variants. Prior work has formalized either guard correctness
                                                                                                                           4 state-machine model of production-deployed Solidity
                                        on toy contracts or attack feasibility on isolated vulnerable instances, but       source, organized along three machine-checked discrimi-
                                        not both directions plus boundary cases against production-deployed                nating directions (negative, positive, boundary) and com-
                                        source.                                                                            posed under a no-retrofit composition discipline that estab-
                                             The verification covers three production protocol instantiations —            lishes guard-pattern correctness as a portable cross-protocol
                                        DAO 2016, Compound v2 cToken family, and Aave V3 flashLoan —                       claim against multiple production protocols.
                                        together with one constructed minimal-diff mutant of Aave V3’s produc-
                                        tion flashLoan (flashLoanVulnerable) authored to isolate a single
                                        security-critical structural difference for discriminating-power isolation.        1.1   Problem statement
                                        We apply mutation-testing methodology to formal verification by con-               Smart contract reentrancy is one of the oldest and most con-
                                        structing this minimal-diff mutant, enabling a controlled experiment that          sequential vulnerability classes on Ethereum-style chains.
                                        naturally-occurring near-misses rarely provide. The resulting tridirec-
                                                                                                                           The DAO 2016 attack drained ≈3.6M ETH (≈US$60M
                                        tional structure pairs (a) a negative-instance attack reproduction of the
                                        DAO 2016 vulnerable pattern, (b) a positive-instance correctness proof
                                                                                                                           at attack-time price) and forced a contentious hard fork
                                        against the Compound v2 cToken family, and (c) a boundary-case proof               splitting Ethereum into two persistent chains; the attack
                                        distinguishing Aave V3’s safe-by-design flashLoan (CEI-correct) from               class has not subsided despite years of awareness —
                                        the flashLoanVulnerable mutant. A single capstone meta-theorem                     Lendf.Me April 2020 (≈US$25M; ERC-777 callback reen-
                                        composes the three protocol instantiations under a no-retrofit compo-              trancy), Fei/Rari Capital Fuse pools 2022 (≈US$80M; clas-
                                        sition discipline (each protocol-instantiation proof was sealed prior to           sical reentrancy), and dozens of smaller incidents cumula-
                                        capstone authoring, with no underlying-proof modifications during com-             tively cross US$500M in documented losses. In response,
                                        position), establishing a machine-checked composition meta-theorem                 the OpenZeppelin ReentrancyGuard modifier — a single-
                                                                                                                           storage-slot mutex enforcing the predicate “not currently ex-
                                        •   Verdict Security, Independent Formal Verification Firm. E-mail:
                                            ray@verdictsecurity.com
                                                                                                                           ecuting inside this contract” before re-entry — has emerged as
                                                                                                                                2

the de facto defense across most production DeFi protocols        a composition theorem, per-protocol claims sit as discon-
(Compound, Aave, Uniswap-style AMMs, and the major-               nected lemmas rather than a coherent discipline claim.
ity of TVL-significant deployments). Despite the pattern’s
ubiquity, no prior formal verification effort has produced a      1.3   Contribution claim summary
machine-checked correctness proof of it against production-       We present the first machine-checked correctness proof
deployed contract source. Auditors rely on pattern recog-         of the OpenZeppelin reentrancy-guard pattern against
nition combined with informal reasoning; academic work            a Lean 4 state-machine model of production-deployed
has formalized either toy-scale instances, attack-feasibility     Solidity source with a composition meta-theorem span-
on isolated vulnerable contracts, or guard correctness on         ning multiple production protocols. The proof corpus
simplified models — never the combination that would              is organized along three machine-checked directions —
establish discriminating power: the guard pattern’s ability       a tridirectional discriminating-power structure — across the
to distinguish defended-correctly from defended-incorrectly       following layers: (a) a negative-instance attack reproduc-
from undefended cases, machine-checked in all three direc-        tion on the DAO 2016 vulnerable pattern (Layer 6-A; six
tions, against production source. This paper supplies that        theorems), (b) a positive-instance correctness proof against
combination.                                                      the Compound v2 cToken family (Layer 6-B; three theo-
                                                                  rems), and (c) a boundary-case proof distinguishing Aave
                                                                  V3’s production flashLoan function — safe by design
1.2   Limitations of prior approaches
                                                                  via CEI-correct implementation — from a minimal-diff mu-
We characterize four limitations of the prior verification        tant flashLoanVulnerable constructed to isolate a sin-
landscape that this paper addresses.                              gle security-critical structural difference (Layer 6-C; three
    Auditor-pattern-recognition layer. Manual auditing rely-      theorems). We apply mutation-testing methodology to for-
ing on pattern recognition is fast but informal. Recurring        mal verification: flashLoanVulnerable is a constructed
reentrancy incidents at audited protocols demonstrate that        minimal-diff mutant isolating a single security-critical struc-
the pattern-recognition layer alone is insufficient: auditors     tural difference — a controlled experiment that naturally-
with strong track records have approved contracts that            occurring near-misses rarely provide — demonstrating
subsequently lost user funds to reentrancy variants. Pat-         the methodology’s sensitivity to single-line regressions in
tern recognition catches the common cases but degrades            production-grade logic. Our proofs operate against a Lean 4
at structural-adjacency boundaries, where syntactically-          state-machine model of this source; the faithfulness of that
similar code paths differ in security-critical semantics.         model to Solidity semantics is a trust assumption in the
    Toy-example formal verification. A substantial body of aca-   sense of §3.3.
demic work has formalized reentrancy reasoning against                The negative instance demonstrates that the method-
simplified contract models — abstract state machines, ideal-      ology catches the most famous historical reentrancy attack
ized storage layouts, decoupled modifier semantics. These         (the DAO predates the OpenZeppelin guard library, so this
models capture the intuition of the guard pattern but do          leg establishes that the methodology recognizes the vulner-
not transfer to production contract code, which involves          ability class the guard targets — a guard-absent baseline
real Solidity storage layout, modifier interaction with inher-    distinct from the two guard-correctness legs); the positive
itance hierarchies, cross-function state mutation under reen-     instance demonstrates that the methodology clears a produc-
trant invocation, and gas-cost interactions with control-flow     tion contract currently securing billions in user funds; the
choices. Closing the gap between toy-model correctness            boundary case is a constructed mutation-testing experiment
and production-source correctness is non-trivial; ignoring        that distinguishes syntactically-similar safe and vulnerable
it produces verification claims that reviewers reasonably         variants at the structural-adjacency boundary where pattern
discount.                                                         recognition tends to degrade — complementing the negative
    Single-direction formalization. Prior verification work on    and positive instances rather than serving as independent
production-leaning contracts typically formalizes one of the      evidence of natural near-miss discrimination. The full proof
two basic directions: either attack feasibility on a known-       corpus is continuously verified under a four-block CI con-
vulnerable contract (negative instance) or guard correctness      figuration that re-checks each theorem and its axiom record
on a defended contract (positive instance). Rarely both.          on every push, ensuring claims hold against ongoing de-
Almost never both together with boundary cases that exercise      pendency drift; complete Lean 4 source plus lake build
the guard pattern’s ability to distinguish defended-correctly     reproduction commands are provided in Appendix A.
from structurally-adjacent vulnerable variants. The compos-           A single capstone meta-theorem at Layer 6-D composes
ite claim — that the guard pattern is provably correct in all     the three protocol instantiations under a no-retrofit com-
three directions and the directions are simultaneously load-      position discipline: the three protocol-instantiation proofs
bearing — has not been established.                               were sealed prior to capstone authoring, and the capstone is
    Composition gap. Even when individual-protocol formal-        proven by direct conjunction of three already-proven prior-
izations exist, the cross-protocol portability of guard-pattern   layer theorems without modification of any underlying
correctness has not been established as a load-bearing meta-      proof, certifying that the guard invariant holds uniformly
theorem. Producing per-protocol proofs in isolation tells         across structurally divergent host protocol architectures.
reviewers little about the pattern’s correctness as an abstract   This is a stronger empirical claim than “composition suc-
defense; reviewers reasonably ask whether a guard-pattern         ceeds when proofs are co-developed,” because the discipline
proof for Protocol A composes with a guard-pattern proof          forbids the most common composition move — adjust-
for Protocol B without modification of either. Absent such        ing an underlying lemma’s hypotheses to fit the desired
                                                                                                                          3

composition target. The result is a machine-checked com-          derivable from its source semantics; the Layer 6-B represen-
position meta-theorem demonstrated under a no-retrofit            tative states that the Compound v2 cToken family’s with-
composition discipline against three production protocols.        drawal function correctly implements the OpenZeppelin
To our knowledge, no prior smart-contract formal verifica-        guard pattern under our formal definition of reentrancy; the
tion work has produced this combination — discriminating          Layer 6-C representative states that the minimal-diff mutant
power against production source plus cross-protocol com-          flashLoanVulnerable fails the formal discriminating-
position validated under a discipline that forbids retrofitting   power property that production flashLoan satisfies; and
of underlying proofs. Each conjunct has partial prior art         the Layer 6-D capstone states (informally) that if the Open-
— guard correctness on simplified models, attack feasibil-        Zeppelin guard pattern is correct on Compound v2 cTo-
ity on isolated vulnerable instances, per-protocol proofs in      kens, correct on Aave V3 flashLoan, and discriminat-
isolation; the contribution is their machine-checked con-         ing between Aave V3’s safe and vulnerable variants, then
junction, against production-deployed source, under a no-         the composed discriminating-power claim holds across all
retrofit composition discipline — a combination not pre-          three. Precise theorem statements appear in §5.
viously assembled, distinguished from prior co-developed              Four protocol instantiations exercised. DAO 2016 (negative);
compositional FV (CompCert, Iris; §8.3) by the no-retrofit        Compound v2 cToken (positive; the Compound v2 cToken
constraint. Both live instantiations (Compound v2, Aave           family — canonical mainnet markets including cUSDC at
V3) are lending-family, so the cross-protocol claim is scoped     0x39AA39c021dfbaE8faC545936693aC917d5E7563
to within-lending portability plus the DAO 2016 exemplar;         and cDAI at 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643
cross-domain extension is future work (§9.4). (Full method-       — secures multi-billion-USD lending TVL across
ology framework details, including the operational labels         multiple markets per public on-chain accounting
for the patterns this discipline embodies, in Appendix B.)        at submission time); Aave V3 flashLoan paired
                                                                  with the flashLoanVulnerable mutant (boundary;
1.4   Approach summary                                            the Aave V3 Pool contract (Ethereum mainnet) at
The methodology rests on four load-bearing choices. Lean 4        0x87870bca3f3fd6335c3F4ce8392D69350B4fA4E2
with mathlib4. All thirteen theorems are stated and machine-      is among the most-deployed flash-loan venues by single-
checked in Lean 4; type-theoretic foundations support             protocol TVL); and the composition across the three (Layer
the discriminating-power claim without SMT-solver depen-          6-D capstone meta-theorem).
dence, and mathlib4 supplies standard tactic infrastructure.          First cross-protocol PASS under no-retrofit composition disci-
No-retrofit composition discipline. Each protocol-instantiation   pline. The no-retrofit composition discipline held across the
contract is sealed against modification before capstone au-       Compound v2 → Aave V3 protocol-instantiation bound-
thoring; the Layer 6-D capstone composes the three instan-        ary at the first empirical instance in the trajectory where
tiations only from outside, by direct conjunction, with no        the discipline was stress-tested under non-trivial protocol-
modification of any underlying proof during composition           semantics divergence — and passed without retrofitting
(§4.2). Axiom-record-minimal wrapper composition. The cap-        either underlying proof. We separate observed (composi-
stone discharges its target inside a thin top-level wrapper       tion was not prevented at this boundary; N=1 empiri-
whose own axiom footprint is exactly [propext]; absorp-           cal), argued (the sealed-before-capstone discipline forecloses
tion preserves the strongest available axiom-record claim         the co-development explanation), and conjectured (broader
at the capstone layer (§4.3). Continuous-integration axiom-       portability pending further cross-pair validation). Both live
record verification. The thirteen theorems are gated by a         protocols are lending-family: the instance crosses a within-
four-block CI configuration that verifies axiom records on        lending, not a between-domain, boundary (§9.4). (Internal
every push (§4.4; Appendix A.3 reproduction commands);            methodology framework labels for this discipline are docu-
the repository is tagged at substantive substrate closure and     mented at Appendix B.)
methodology framework canonization, enabling reviewers                Build state and axiom record. lake build is green at
to reproduce the entire corpus from a single tagged commit.       901 jobs; the axiom-record check (§4.4) is green across ev-
                                                                  ery theorem. Zero sorry. Zero introduced axioms. Axiom
1.5   Results summary                                             footprint bounded by [propext] across the entire corpus
                                                                  (Appendix A.2 ground truth; §4.3 wrapper composition).
Thirteen theorems machine-checked. Six Layer 6-A
theorems     formalize     the   negative-instance   DAO
2016 attack reproduction; three Layer 6-B theorems
formalize the positive-instance Compound v2 cToken
correctness proof; three Layer 6-C theorems formalize
the boundary-case pair distinguishing Aave V3 2 BACKGROUND
flashLoan         from    the     flashLoanVulnerable
mutant; one Layer 6-D capstone meta-theorem This section establishes the context that subsequent sections
(tridirectionalDiscriminatingPower_certificate) build on: the smart contract security setting in which reen-
composes the three protocol instantiations under the no- trancy vulnerabilities arise, the attack class itself, the Open-
retrofit composition discipline at [propext]-only axiom Zeppelin guard pattern’s defensive role, the production con-
dependence.                                                 tracts in scope for the tridirectional discriminating-power
    Informally: the Layer 6-A representative theorem states claim, and the Lean 4 + formal verification foundations on
that the reentrancy attack on the DAO contract is formally which the machine-checked proofs rest.
                                                                                                                                   4

2.1   Smart contract security context                                     Read-only reentrancy is a more recent variant. A view
                                                                     function (one declared as not mutating state) is invoked
Smart contract platforms execute programmable on-chain
                                                                     during a reentrant call window; the view function returns
logic under a tightly-constrained operational model —
                                                                     stale state because the broader transaction has not yet up-
deterministic execution against globally-replicated state,
                                                                     dated the relevant storage slot. Downstream contracts that
transaction-atomic semantics with deterministic intra-block
                                                                     consume the view function’s return value can be deceived
ordering, and synchronous external-call semantics that in-
                                                                     into accepting stale data. The attack does not require the
terleave control flow across contract boundaries within a
                                                                     view function itself to be vulnerable in the traditional sense;
single transaction. Ethereum is the dominant platform by
                                                                     it requires only that a consumer of the view function executes
value locked; Layer-1 chains and Layer-2 rollups extend
                                                                     during the reentrant window.
the model with varying compatibility. Decentralized finance
                                                                          Reentrancy is fundamental to the smart contract exe-
TVL has ranged from roughly US$30B to US$100B over the
                                                                     cution model rather than incidental to any particular lan-
past four years, with individual protocols holding multi-
                                                                     guage. The Ethereum CALL opcode is synchronous: ex-
billion-dollar deposit balances and annual losses across
                                                                     ternal calls transfer execution to the callee and return to
all attack classes ranging US$1B–2B+ in documented inci-
                                                                     the caller; the caller’s local state at the moment of the
dents. Reentrancy is one of several leading attack classes
                                                                     CALL is preserved across the synchronous transition, but
by aggregate loss; it is among the most enduring, recur-
                                                                     global storage is shared with the callee. Combined with the
ring annually since 2016 despite near-universal industry
                                                                     atomic-transaction guarantee, this produces a setting where
awareness. Smart contracts are uniquely vulnerable relative
                                                                     mutually-distrusting contracts can observe and act on each
to traditional software because execution is code-is-law (no
                                                                     other’s mid-transaction state. Any defense pattern that relies
operator can revert a mined transaction absent multi-month
                                                                     on storage-based gating must contend with the fact that
chain-governance processes), transactions are irreversible,
                                                                     storage is observable to reentrant callees, and any defense
deployed bytecode is immutable absent upgrade-pattern
                                                                     that relies on call-stack state must contend with the fact that
infrastructure, and the composable-interface model encour-
                                                                     the call stack includes contracts authored by attackers.
ages cross-contract calls that interleave state mutation across
                                                                          Static analysis tools — including Slither, Mythril, Secu-
mutually-distrusting authors — a single missed defensive
                                                                     rify, and academic-leaning prototypes — have made sub-
boundary can drain a multi-billion-dollar contract in one
                                                                     stantial progress on detecting classical single-function reen-
transaction.
                                                                     trancy patterns. Pattern-recognition heuristics flag candi-
                                                                     date violations of the CEI pattern; constraint-solver-based
                                                                     tools encode storage access ordering and reachability prop-
2.2   The reentrancy attack class
                                                                     erties. Performance on classical reentrancy is now reason-
Reentrancy refers to a family of vulnerabilities in which a          able. Performance on cross-function and read-only variants
smart contract is re-entered — its functions invoked again           is weaker; these patterns require reasoning across function
— while a prior invocation of the same contract is still mid-        boundaries and across views vs mutators, which static anal-
execution, in a way the contract’s authors did not anticipate.       ysis tools have historically struggled with at production-
The category subsumes several sub-patterns that share the            source scale.
underlying mechanism but differ in the specific path of state
mutation and re-entry.                                               2.3   OpenZeppelin guard pattern
    Classical (single-function) reentrancy is the original DAO       The OpenZeppelin ReentrancyGuard contract is a single-
2016 attack pattern. The vulnerable contract performs an             storage-slot mutex that has become the de facto reentrancy
external call (typically a withdrawal of native ETH or an            defense across most production DeFi protocols. The contract
ERC-20 transfer) before updating its internal accounting             exposes a nonReentrant modifier applied to externally-
state. The external call is a CALL opcode that transfers exe-        callable functions performing state-mutating work involv-
cution to a callee contract; if the callee is attacker-controlled,   ing external calls. A storage slot — historically a uint256
the callee can re-invoke the original contract’s withdrawal          taking values _NOT_ENTERED (typically 1) and _ENTERED
function before the original invocation has updated its state.       (typically 2) under varying field names — holds the cur-
The state update — typically a decrement of the user’s               rent reentrancy state. The modifier requires the slot to be
recorded balance — has not yet occurred when the recursive           _NOT_ENTERED at function entry (reverting otherwise), sets
withdrawal begins, so the recursive withdrawal succeeds              it to _ENTERED, executes the function body, and resets it
against the same (un-decremented) balance. Recursion pro-            on exit. Any reentrant invocation of any function carrying
ceeds until the contract is drained or until a gas limit halts       the same modifier — same function or different function on
execution.                                                           the same contract instance — fails at the entry guard. The
    Cross-function reentrancy generalizes the pattern across         pattern is defensive-coding discipline rather than language-
multiple functions of the same contract. One function mu-            level enforcement: the Solidity compiler does not insert the
tates state; an external call during that function’s execution       guard; the developer must add the modifier to each function
allows the attacker to invoke a different function on the same       that requires protection, and a missed modifier produces no
contract that depends on the not-yet-updated state. The              warning. The guard is one ingredient in a broader checks-
attack works even when the originally-invoked function fol-          effects-interactions discipline; production contracts adopt-
lows the checks-effects-interactions (CEI) pattern internally,       ing both are well-defended against the classical reentrancy
because the cross-function state coupling is not visible at the      class. Adoption is widespread (Compound, Aave, Uniswap-
single-function level.                                               style AMMs, and the bulk of TVL-significant DeFi protocols
                                                                                                                                 5

use ReentrancyGuard or a near-identical variant), so the          a reentrancy window during the callback. The variant is
pattern’s correctness is load-bearing at ecosystem scale.         structurally adjacent to the safe version: same function sig-
                                                                  nature, same borrower-callback shape, near-identical control
2.4   Real-contract instances in scope                            flow, identical surface API. Pattern recognition operating at
The tridirectional discriminating-power claim is established      code-shape level would treat the two variants as the same;
against four production-relevant contract instances span-         the methodology presented here distinguishes them at the
ning negative, positive, and boundary cases.                      body-shape layer where the guard-engagement invariant
    DAO 2016 (negative instance). The Decentralized Au-           differs.
tonomous Organization (the DAO) was a 2016 Ethereum                   The four contracts together exercise the tridirectional
smart contract that raised approximately 11.5M ETH                discriminating-power claim. The negative instance demon-
(≈US$150M at the time) through token sales and aimed to           strates that the methodology catches the most famous his-
operate as an investor-directed venture fund. In June 2016,       torical reentrancy attack. The positive instance demon-
an attacker exploited a classical single-function reentrancy      strates that the methodology clears a production contract
vulnerability in the DAO’s splitDAO function to drain             currently securing billions in user funds. The boundary
approximately 3.6M ETH (≈US$60M at attack-time price;             case demonstrates that the methodology distinguishes be-
substantially higher at current ETH prices). The Ethereum         tween syntactically-similar safe and vulnerable variants at
community responded with a hard fork that reverted the            the structural-adjacency boundary — the place where pat-
attack’s effects, splitting the chain into Ethereum (with         tern recognition tends to degrade and where a verification
the hard fork) and Ethereum Classic (without). The DAO            methodology’s discriminating power is most consequential.
attack is the canonical reentrancy incident; reproducing its
core mechanism is the natural negative-instance test of any       2.5   Lean 4 and formal verification context
guard-pattern verification methodology.
    Compound v2 cToken family (positive instance). Compound       Lean 4 is a dependently-typed proof assistant with type-
v2 is one of the longest-running and largest produc-              theoretic foundations based on the Calculus of Induc-
tion lending protocols on Ethereum. The cToken family             tive Constructions with universes. Theorems are proposi-
— interest-bearing tokens representing deposits in Com-           tions, proofs are programs constructing evidence, and type-
pound’s lending markets — uses the OpenZeppelin guard             checking confirms that proof terms have the type stated
pattern correctly across its withdrawal and redemption            in the theorem (Curry-Howard). We selected Lean 4 over
paths. The Compound v2 cTokens currently secure approx-           Coq, Isabelle/HOL, and HOL Light because Lean’s tactic
imately US$2-5B in lending TVL across multiple markets,           framework suits the structural reasoning the discriminating-
depending on market conditions. The cToken family is              power claim requires; mathlib4 supplies standard data
a strong positive-instance test: a real production contract       structures, finiteness reasoning, and tactic libraries reducing
holding multi-billion-dollar deposits, with a guard-pattern       proof-engineering overhead; and Lean 4’s tooling, seman-
implementation that the community has stress-tested for           tics, and proof-term sizes remain stable and manageable for
years without a confirmed reentrancy incident against the         the theorem shapes used here.
pattern itself.                                                       The proof corpus depends on a pinned mathlib4
    Aave V3 flashLoan (boundary case, safe). Aave V3 is           version specified in lakefile.lean and locked
one of the largest production lending protocols. Its Pool         via lake-manifest.json; lean-toolchain pins
contract — deployed on Ethereum mainnet at address                the Lean compiler version. Standard imports include
0x87870bca3f3fd6335c3F4ce8392D69350B4fA4E2                        Mathlib.Tactic,            natural-number        infrastructure,
— implements a flashLoan function that issues                     Mathlib.Data.List.* modules for trace semantics,
uncollateralized loans repayable within the same                  and Mathlib.Logic for propositional reasoning. Axiom
transaction. The flashLoan body is checks-effects-                record discipline is enforced at the CI level (§4.4); acceptable
interactions-correct by design: the function records              records are kernel-only (provable in pure intensional type
the loan, transfers funds to the borrower, invokes the            theory) and [propext]-only (propositional extensionality
borrower’s IFlashLoanReceiver.executeOperation                    only — no choice or excluded middle). No theorem is
callback, then verifies repayment plus fee on return. The         admitted with sorry, admit, or any user-introduced
body prevents reentrancy by checks-effects-interactions           axiom.
execution ordering — the borrower callback cannot
observe uncommitted intermediate state — rather than
by an OpenZeppelin-style storage-mutex modifier; the
formalization (§5.5) models this CEI ordering at an abstract      3     T HREAT M ODEL
body-shape layer. flashLoan is the canonical protocol-            This section specifies the formal threat boundary against
by-design CEI-correct exemplar in the boundary-case               which the discriminating-power claim of §1.3 is established.
layer.                                                            We make adversary capabilities, the state-machine abstrac-
    Aave V3 flashLoanVulnerable (boundary case, vulner-           tion level at which formalization operates, the trust assump-
able). For the boundary case to test discriminating power,        tions on which our proofs depend, and the explicit out-of-
we author a structurally-adjacent vulnerable variant —            scope items all visible up-front. Doing so allows reviewers to
flashLoanVulnerable — that differs from flashLoan                 evaluate the contribution claim’s scope precisely and serves
in a single security-critical respect: the variant fails to en-   as the canonical reference point for the substantive material
gage the guard pattern’s body invariant correctly, leaving        in §5 about what is and is not proved.
                                                                                                                               6

3.1   Adversary model                                            on reentrancy-relevant paths); Solidity-source-to-bytecode
The adversary controls one or more Externally-Owned Ac-          compilation correctness is a separate trust assumption (§3.3).
counts (EOAs) on the target chain and may deploy and             Model fidelity. The model captures features load-bearing
call arbitrary smart contracts. The adversary is permit-         for reentrancy (storage at slot granularity, call-stack-aware
ted to compose cross-protocol interactions via the callable-     sequencing, external-CALL boundary semantics, atomic-
contract pattern that underlies the reentrancy attack class      transaction guarantees, modifier composition) and abstracts
— that is, to deploy contracts conforming to the call-           precompile internals, SELFDESTRUCT, and coarse gas ac-
back interfaces (receive, fallback, tokensReceived,              counting — each benign for the reentrancy class. The faith-
IFlashLoanReceiver.executeOperation, etc.) that                  fulness of this model to Solidity semantics for the modeled
the protocols under analysis use to invoke external behavior     features is an explicit trust assumption (§3.3).
during the execution of a guarded function. The adversary
may also coordinate sequences of transactions across blocks      3.3   Trust assumptions
where coordination across atomic-transaction boundaries is
permitted by the underlying chain semantics.                     Five trust assumptions underpin the discriminating-power
    The adversary has no special protocol-level privileges.      claim, all standard in the formal-verification literature
The adversary is not a protocol owner, is not on a whitelist,    for smart-contract source-level proofs. The first two con-
is not a validator or block proposer, and holds no role-         cern translation soundness in opposite directions from
based access-control credentials at the protocols under anal-    the source-level pivot; the third concerns computational-
ysis. In particular, the adversary cannot pause the protocol,    substrate correctness; the remaining two scope the threat
change interest-rate parameters, replace the implementa-         model.
tion behind an upgradeable proxy, or otherwise exercise              Solidity compiler correctness. Our proofs operate at
governance-mediated authority. Where a protocol exposes          the Solidity source level. Deployed bytecode correctness
a nonReentrant-guarded function, the adversary’s only            derives from the Solidity compiler’s correct compilation of
routes to that function are the publicly callable interfaces;    that source (specifically, the solc version in each proto-
the adversary cannot bypass the guard pattern by privileged      col’s deployment metadata — pre-0.4.x lineage for DAO
means.                                                           2016, 0.5.x for Compound v2 cToken, 0.8.x for Aave V3
    The adversary may control multiple addresses. Sybil-         Pool). Compiler-correctness verification is itself an active
resistance analysis is not in scope; for the purposes of this    research area; we do not attempt to subsume that work
threat model, all adversary-controlled addresses are treated     within the present scope. Reviewers may treat our results
collectively as the adversary, and a defense that holds          as conditional on solc correctness for the specific source
against a single adversary-controlled address holds against      files analyzed.
multiple coordinated addresses under the same control.               Lean-model fidelity for the modeled features. Our
The adversary’s computation is bounded by standard EVM           proofs operate against the Lean 4 state-machine model of
gas-limit constraints (per-transaction block gas limit and       §3.2, not raw Solidity source or compiled bytecode di-
per-call sub-budgets); no quantum-computational, oracle-         rectly. We assume this model is a sound abstraction of
prediction, or non-classical computational assumptions are       the relevant Solidity-semantics fragment for the analyzed
made on either side.                                             contracts (the captured features of §3.2). The model tar-
                                                                 gets the logic semantics of the storage-slot-mutex guard
                                                                 pattern (_status slot, _NOT_ENTERED/_ENTERED tran-
3.2   State-machine abstraction level                            sitions, modifier-entry/exit), which are invariant across
The formalization operates at Solidity-level semantics rather    source-level and compiled-bytecode representations; this
than raw EVM bytecode. The state machine captures stor-          is an intentional design choice rather than a verification
age layout at slot granularity, call-stack-aware function-call   gap. Deriving such model-to-source soundness mechani-
sequencing, the boundary semantics of external CALL op-          cally — a verified-translation pipeline in the KEVM/F*-
codes (synchronous-return-with-shared-storage — the prop-        EVM-semantics line of §8.1 — is active research, out of scope
erty that produces the reentrancy setting), and atomic-          here; results are conditional on this fidelity. This assumption
transaction guarantees (whole-transaction rollback on re-        is distinct from solc compiler correctness above: it concerns
vert; observable mutations only on success). The Open-           the source→Lean-model direction.
Zeppelin guard pattern’s correctness claim is precisely that         Lean 4 kernel and mathlib4 correctness. As is standard
the entry-time storage check on _status blocks every re-         for any Lean 4 formalization, the proofs are mechanically
entry into any function carrying the nonReentrant mod-           checked under the assumption that the Lean 4 kernel cor-
ifier on the same contract instance, regardless of whether       rectly implements its type theory and that the imported
the original invocation has returned. Several abstraction-       mathlib4 modules correctly state the mathematical results
level details are deliberately out of scope at the model         they claim. Lean 4’s kernel is small and has received com-
layer: gas accounting is assumed sufficient for analysis-        munity scrutiny; the imported mathlib4 modules (general
relevant operations (we model neither gas exhaustion mid-        tactic infrastructure, finite-data-structure reasoning, propo-
call as a separate failure mode nor denial-of-service via        sitional logic) are pinned via lakefile.lean dependency
gas, since the discriminating-power claim concerns reach-        declarations and locked through lake-manifest.json,
ability of attacker-favorable states under successful exe-       with the Lean compiler version pinned separately via
cution); precompile semantics and SELFDESTRUCT are               lean-toolchain. The exact dependency graph is repro-
abstracted (the in-scope protocols do not exercise them          ducible from the tagged commit.
                                                                                                                              7

    Honest borrower assumption per real-contract in-             authored, presented at the level of operational consequence
stance. For the Compound v2 cToken positive instance, the        rather than internal-framework labels. The full methodol-
discriminating-power claim concerns the guard pattern’s          ogy framework — including its sub-pattern catalog, grad-
correctness against reentrancy; it does not require borrowers    uation criteria, and cross-protocol stress-test history — is
to behave honestly in any economic sense (interest-rate sol-     the subject of a companion arXiv paper; the present section
vency, collateral maintenance, liquidation responsiveness).      gives reviewers what they need to evaluate the substantive
Borrowers may be adversarial in the §3.1 sense; what is as-      smart-contract-verification claims of this paper.
sumed is that the protocol-level invariants the cToken family
relies on (such as correct accrual of interest at withdrawal     4.1   Formalization approach
time) are computed by the protocol’s own accounting code
                                                                 The formalization is conducted in Lean 4 with mathlib4 as
rather than supplied by the caller. The same holds for the
                                                                 the supporting mathematical library. Lean 4’s dependent
Aave V3 boundary case: the borrower is assumed adversar-
                                                                 type theory, with the propositions-as-types correspondence
ial, the flash-loan protocol’s repayment-verification logic is
                                                                 sketched at §2.5, allows propositions and their proofs to
assumed to execute as written.
                                                                 be first-class type-theoretic objects: a theorem statement is
    No miner or validator behavior assumption. The prop-
                                                                 a type, a proof is a program of that type, and the type-
erties proved are not contingent on miner or validator
                                                                 checker’s confirmation that the proof has the stated type
behavior. We do not assume timing constraints, transaction-
                                                                 is the verification. Tactic proof scripts produce these proof
ordering constraints, reorg-resistance constraints, or pro-
                                                                 terms; the kernel re-checks them whenever the corpus is
poser honesty. The reentrancy attack class is mediated by
                                                                 built.
smart-contract execution within a single transaction, not by
                                                                     Mathlib4 modules are imported as needed. The de-
consensus-layer behavior; our claim therefore inherits no
                                                                 pendency graph is recorded explicitly: the Lean com-
consensus-layer trust requirement.
                                                                 piler version is pinned in lean-toolchain; the math-
                                                                 lib4 dependency version is pinned in lakefile.lean
3.4   Out-of-scope items and boundary summary
                                                                 and locked at lake-manifest.json. Standard tac-
The discriminating-power claim addresses the reentrancy          tic infrastructure (Mathlib.Tactic), natural-number
attack class against contracts that adopt (or fail to adopt)     reasoning (Mathlib.Data.Nat.Basic), list manipu-
the OpenZeppelin guard pattern. Several attack classes           lation underlying the trace semantics (modules un-
that have produced significant losses in production DeFi         der Mathlib.Data.List), and propositional reasoning
are explicitly out of scope: oracle manipulation (flash-         (Mathlib.Logic modules) constitute the bulk of the im-
loan-enabled price-feed attacks, structurally distinct from      ported surface.
re-entering a guarded function); MEV and transaction-                The proof discipline is theorem-statement-first. Each
ordering attacks (sandwich extraction, mempool-ordering          theorem statement is authored and sealed prior to any
arbitrage operating above the contract-execution layer);         proof body authoring; statement modifications during proof
governance attacks (proposal-passing exploits, vote-buying,      work are prohibited under the methodology framework’s
timelock bypasses, assuming each protocol’s governance           discipline. This forecloses the most common failure mode
configuration is correctly set); cross-chain bridge at-          of co-developing statement and proof — the unconscious
tacks (chain-boundary trust assumptions absent from              weakening of a statement’s hypotheses or strengthening of
single-chain analysis); front-running (mempool-level user-       its assumptions to fit the partial proof one has constructed.
transaction frontrunning); centralization risks (admin keys,     When the proof of a sealed statement turns out to be
upgradeable-proxy privileged operations, role-based pauses       impossible as written, the disciplined response is to escalate
— our claim concerns the publicly callable surface only);        (the statement was the wrong claim) rather than silently
and economic attacks not mediated by reentrancy (liqui-          adjust the statement to match the proof.
dation cascades, interest-rate manipulation, collateral-ratio        Per-theorem axiom-record verification is gated in contin-
exploits). The methodology’s potential extension to these        uous integration on every push. Lean 4’s #print axioms
classes is future work (§9, §7.2); no broader claim is made      introspection produces, for any named theorem, the list of
by the present paper.                                            axioms its proof transitively depends on. The CI configura-
    In scope: the reentrancy attack class against the Open-      tion runs this introspection over each theorem in the corpus
Zeppelin guard pattern, formalized at Solidity source            and fails the build if any theorem’s axiom record drifts from
level for the three production protocol instantiations           the claimed record. This converts axiom-minimality from an
of §1.3 — DAO 2016 (negative), Compound v2 cTo-                  author’s assertion into a continuously checked invariant: a
ken (positive), Aave V3 flashLoan paired with the                future change that silently introduces a dependency on (say)
flashLoanVulnerable minimal-diff mutant (boundary).              classical choice would be caught by the CI gate at the next
Within that scope the methodology catches the negative           push, not by reviewer inspection at submission time.
instance, clears the positive instance, and distinguishes the
boundary pair, machine-checked end-to-end.
                                                                 4.2   The compose-from-outside discipline
                                                                 The capstone meta-theorem at Layer 6-D is proven under a
                                                                 strict no-retrofit composition discipline: the three protocol-
4     M ETHODOLOGY OVERVIEW                                      instantiation theorems are conjoined directly to produce the
This section describes the formalization approach and the        capstone, with no modification of any underlying protocol-
methodological discipline under which the proofs were            instantiation proof during composition. The phrase compose
                                                                                                                               8

from outside names the operational consequence: composi-          4.3   Axiom-record-minimal wrapper composition
tion operates on the prior-layer theorems as black-box facts      The Layer 6-D capstone is structured as a thin wrapper
rather than reaching inside their proofs to adjust hypothe-       module that imports the three sealed protocol-instantiation
ses, conclusions, or supporting lemmas.                           theorems and discharges its target proposition by directly
   The discipline is enforced procedurally rather than            conjoining them; the wrapper introduces no new axioms,
by a single language-level mechanism. The three                   and its #print axioms record is exactly the union of the
protocol-instantiation files — DAOContract.lean,                  underlying theorems’ records. This wrapper-layer pattern
CompoundContract.lean, AaveBoundaryCase.lean                      preserves axiom-record minimality at the capstone: each
— were authored, proven, and sealed prior to any work             underlying protocol-instantiation theorem carries its own
on the capstone meta-theorem. Once a file was sealed,             kernel-only or [propext]-only record (verified at the per-
modifications to that file were prohibited under the              layer CI block), and the wrapper only conjoins existing
methodology discipline; any subsequent change required            facts. The capstone therefore inherits the strongest available
explicit re-authorization with documented rationale. The          axiom-record claim — [propext]-only, the standard math-
capstone author thereby faced a hard constraint: prove the        lib4 axiom of propositional extensionality, a single classical
meta-theorem from the sealed prior layers as they stand, or       extension fully compatible with the Lean 4 kernel. No user-
escalate.                                                         introduced axioms appear at any layer of the corpus. The
    Three classes of modification are forbidden under this        broader pattern context (related patterns, cross-protocol em-
discipline. Adjusting an underlying lemma’s hypotheses to         pirical history) is documented at Appendix B and elaborated
fit a desired composition target — the most common com-           in the companion methodology paper.
position move in formal-verification work — is prohibited.
Weakening a prior theorem’s conclusion to make it easier          4.4   CI verification and axiom-record discipline
to compose is prohibited. Adding unstated hypotheses to
underlying theorems to discharge intermediate proof obli-         Continuous integration consists of four parallel verification
gations is prohibited. The capstone proof either composes         blocks at build.yml lines 287, 356, 408, and 464, gating the
the underlying theorems exactly as they were sealed, or it        thirteen theorems on every push: one block each for Layer
does not compose at all.                                          6-A (DAO 2016 negative-instance, 6 theorems + supporting
                                                                  lemmas), Layer 6-B (Compound v2 cToken positive-
    The first cross-protocol stress test of this discipline oc-
                                                                  instance, 3 theorems), Layer 6-C (Aave V3 boundary-case
curred at the Compound v2 → Aave V3 boundary in
                                                                  pair, 3 theorems), and Layer 6-D (capstone meta-theorem).
the Layer 6-D capstone. The two protocols differ in non-
                                                                  The #print axioms introspection emits each theorem’s
trivial ways at the semantic level: Compound’s cToken
                                                                  transitively required axioms; the CI compares against
family operates on a balance-update-and-transfer pattern
                                                                  recorded expectations per theorem and fails the build
with persistent user accounting; Aave’s flashLoan oper-
                                                                  on any mismatch. The capstone records [propext]-
ates on a repay-within-transaction pattern with no persis-
                                                                  only; each Layer 6-A/B/C theorem records kernel-only
tent user accounting beyond the loan window. A retrofit-
                                                                  (no axioms beyond Lean 4’s intensional type theory) or
permissive workflow could have produced a capstone proof
                                                                  [propext]-only. No theorem is admitted with sorry,
by adjusting either protocol’s underlying lemmas to fit
                                                                  admit, or any user-introduced axiom. Reproducibility is
a common composition shape. The no-retrofit discipline
                                                                  anchored at tagged commits: the substantive substrate at
forbade that path. The capstone nevertheless composed: a
                                                                  v1.3-layer6-closure, the methodology framework
direct conjunction of the three sealed prior-layer theorems
                                                                  canonization at v1.7-methodology-housekeeping.
discharged the meta-theorem at [propext]-only axiom de-
                                                                  Reviewers reproduce the verification by checking out
pendence. We treat that successful composition as observed
                                                                  either tag and running lake build plus lake env
N=1 evidence — and, given the sealed-before-capstone
                                                                  lean QanaryContracts/PrintAxioms.lean against
discipline that forecloses the co-development explanation,
                                                                  the pinned dependency graph. The manuscript content
as an argument that the guard pattern’s correctness is
                                                                  corresponding to this paper version is sealed at intermediate
portable across the observed boundary; broader portability
                                                                  tag v1.6-phase7-closure (the abstract’s reproducibility
is conjectured pending further cross-pair validation (the ob-
                                                                  anchor); the substrate at v1.6 is identical to v1.3, so
served/argued/conjectured separation of §1.5), not asserted
                                                                  reviewers may equivalently check out v1.6 for end-to-end
from N=1.
                                                                  reproduction.
    This is a methodologically stronger claim than “compo-
sition succeeds when proofs are co-developed.” The latter is
consistent with each underlying proof having been silently        4.5   Manuscript audit and transparency
shaped to fit the eventual composition target. The no-retrofit    The manuscript was developed with generative-AI assis-
discipline rules out that path of explanation: the underly-       tance (Claude, Grok, and Gemini) used for editorial pur-
ing proofs cannot have been shaped by the composition             poses including adversarial audit of drafts, prose drafting
target, because they were sealed before the composition           under author direction, and methodology-framework re-
target’s proof was authored. The internal label and broader       view during preparation. All model outputs were inspected
pattern context for this discipline within our methodology        by the author; the substantive contributions of this paper
framework appear at Appendix B; the operational property          — the thirteen machine-checked theorems and their ax-
described above is the load-bearing one for the present           iom records — are verified by the Lean 4 kernel and CI-
paper.                                                            reproducible per Appendix A.3. The audit framework itself
                                                                                                                              9

is not a claimed research contribution of this paper and is     still type-check against the pinned mathlib4 dependency
presented in the companion methodology paper (separate          graph and that their axiom records match the expecta-
arXiv track per the boundary discipline of §1). This para-      tions recorded in Appendix A on every push. No theorem
graph satisfies the generative-AI-usage disclosure required     is admitted with sorry, admit, or any user-introduced
by the venue’s call for papers.                                 axiom declaration; the corpus axiom footprint is bounded
                                                                by [propext] (Appendix A.2).


                                                                5.3   Layer 6-A: negative instance (DAO 2016)
5     F ORMALIZATION
                                                                The Layer 6-A negative instance reproduces the classi-
This section presents the substantive substrate of the
                                                                cal reentrancy attack against the DAO 2016 contract. The
discriminating-power claim: the formal definitions
                                                                splitDAO function performs an external transfer of native
and predicates, the inventory of the thirteen
                                                                ETH to a user-controlled recipient before decrementing the
machine-checked theorems, per-layer presentation of
                                                                user’s recorded balance, opening a window in which a
negative/positive/boundary proofs, the capstone meta-
                                                                recipient contract can re-invoke splitDAO against the same
theorem, and the reproducibility anchor. Full theorem
                                                                un-decremented balance until the contract is drained.
statements, axiom records, and proof-skeleton excerpts are
                                                                    Our formalization models the relevant subset of the
deferred to Appendix A.
                                                                DAO contract source — the splitDAO function’s storage
                                                                layout, balance accounting, and external-call structure —
5.1   Formal definitions and predicates                         at the abstraction level of §3.2. The Layer 6-A capstone
The formalization rests on three load-bearing predicates        theorem (one of six in this layer) states that under the
over the Solidity-source state-machine model of §3.2. The       reentrancy predicate of §5.1, the attacker-controlled re-entry
reentrancy predicate characterizes the attack class: a con-     path is derivable from the DAO contract source: there exists
tract execution exhibits reentrancy if there exists a call      a constructible call trace, expressible in our state-machine
trace in which an external CALL from function f of con-         model, in which the re-entry succeeds and the contract’s
tract A transfers execution to an attacker-controlled callee    invariant (balance-sum equals total-deposits) is broken. The
that, before f’s frame returns, invokes a function g of A       five supporting lemmas decompose the derivation into
(where g may be f itself) and observes storage state f has      the load-bearing pieces — call-stack interleaving, storage-
modified but not yet completed updating. The predicate is       observation, balance-update sequencing, and the absence of
call-stack-aware, storage-mutation-aware, and external-call-    any guard-pattern protection — that together discharge the
boundary-aware, capturing classical single-function, cross-     capstone.
function, and the storage-observation aspect of read-only           The DAO contract predates the OpenZeppelin guard
reentrancy. The guard-pattern correctness predicate charac-     library. Its inclusion as the negative instance is therefore
terizes the OpenZeppelin guard’s correct application: func-     not a guard-pattern failure but a guard-pattern target: the
tion f of contract A carries the guard correctly if its entry   DAO formalization demonstrates that the methodology
condition checks _status == _NOT_ENTERED, its body              recognizes the vulnerability class the guard pattern was
sets _status = _ENTERED before any external CALL, its           created to address, even where the guard itself is absent.
exit resets to _NOT_ENTERED, and these accesses target the      This complements the Layer 6-B and 6-C results, which
same storage slot as other guarded functions on A; a func-      establish recognition of the guard’s behavior when present.
tion carrying the guard correctly cannot exhibit reentrancy     Full theorem statements, hypothesis structure, and proof-
under the model. The discriminating-power predicate is the      skeleton outline appear in Appendix A.
meta-level claim: a verification methodology discriminates
between guard-protected and guard-vulnerable instances          5.4 Layer 6-B: positive instance (Compound v2 cToken
if it derives the reentrancy predicate for vulnerable in-       family)
stances, derives the guard-pattern correctness predicate for
protected instances, and distinguishes structurally-adjacent    Compound v2’s cToken family represents the largest and
vulnerable variants from safe counterparts. The tridirec-       longest-running production deployment of the OpenZep-
tional claim of §1.3 is the assertion that our formalization    pelin guard pattern within DeFi lending. Each cToken’s
satisfies this meta-predicate against the three production      withdrawal-path functions (redeem, redeemUnderlying,
instantiations of §2.4 plus the minimal-diff mutant of §5.5.    the underlying transfer flows) carry a nonReentrant
Full predicate definitions appear in Appendix A.                modifier implementing the OpenZeppelin guard pat-
                                                                tern. Compound v2’s deployment uses a structurally-
                                                                equivalent custom in-contract realization rather than the
5.2   Theorem inventory                                         literal library import — same _status slot semantics,
Thirteen theorems machine-check the discriminating-power        same _NOT_ENTERED/_ENTERED integer encoding, same
claim. The inventory below summarizes each theorem at the       modifier-entry guard, same modifier-exit reset — au-
level of an informal one-line statement; the precise Lean 4     thored before the OpenZeppelin library API stabilized;
statements (with full type signatures, hypothesis lists, and    our formalization targets this custom realization, and
the #print axioms output) appear in Appendix A.                 the discriminating-power claim transfers to OZ-library-
    Each layer’s theorems are gated by an independent CI        importing protocols because the formalization predicate
block (§4.4), mechanically verifying both that the theorems     (§5.1) abstracts over the realization at the storage-slot-mutex
                                                                                                                                        10

                                                               TABLE 1
                                Inventory of thirteen theorems across four protocol-instantiation layers.


Layer                                            Count     Theorem(s)                    Informal statement        Axiom record
6-A                                                1+5     DAO reentrancy                The DAO 2016 attack       [propext]-only
                                                           derivation + supporting       trace is derivable from   master/wrapper;
                                                           lemmas                        the contract’s source     kernel-only inner
                                                                                         semantics under the       lemmas
                                                                                         reentrancy predicate
6-B                                                1+2     Compound v2 cToken            The cToken family’s       [propext]-only
                                                           correctness +                 withdrawal path           master/wrapper;
                                                           supporting lemmas             correctly implements      kernel-only inner
                                                                                         the OpenZeppelin          lemmas
                                                                                         guard pattern under our
                                                                                         reentrancy predicate
6-C                                                2+1     Aave V3 flashLoan             Production flashLoan      [propext]-only
                                                           correctness +                 satisfies guard-pattern   master/wrapper;
                                                           flashLoanVulnerable           correctness; the          kernel-only inner
                                                           failure + CEI lemma           minimal-diff mutant       lemmas
                                                                                         flashLoanVulnerable
                                                                                         fails it
6-D                                                    1   Tridirectional                Composed:                 [propext]-only (union
                                                           discriminating-power          methodology catches       of prior-layer records)
                                                           capstone                      the negative instance,
                                                                                         clears the positive
                                                                                         instance, and
                                                                                         distinguishes the
                                                                                         boundary pair



level. (Source-level terminology may vary across “Open-               tract implements flashLoan according to a checks-effects-
Zeppelin guard pattern,” “structurally-equivalent custom              interactions discipline that is guard-pattern correct by con-
guard,” and “mutex-modifier pattern” depending on com-                struction: the loan is recorded, funds are transferred, the
mit; all refer to the same storage-slot mutex semantics               borrower’s IFlashLoanReceiver.executeOperation
formalized here.) The protocol has stress-tested this pattern         callback is invoked, and repayment plus fee is verified
in production for years without a confirmed reentrancy                on return. The borrower-supplied callback cannot exploit
incident against the guard itself.                                    reentrancy because the body commits all security-relevant
    The Layer 6-B target theorem (one of three in the layer)          state before the callback executes; the Layer 6-C predicate
states that the cToken withdrawal path correctly implements           discriminates on this SSTORE-before-CALL body-shape or-
the OpenZeppelin guard pattern under our predicate of                 dering (the abstract guard-engagement pattern), which pro-
§5.1: any execution trace conforming to the cToken with-              duction flashLoan satisfies.
drawal path satisfies the guard-pattern correctness predi-                To exercise discriminating power against structurally-
cate, and consequently no reentrancy trace is constructible           adjacent variants — where pattern recognition is known to
against it. Two supporting lemmas decompose the result: a             degrade per §1.2 — we construct flashLoanVulnerable
guard-invariant lemma showing that the storage slot track-            as a minimal-diff mutant of production flashLoan. The
ing guard state is consistently set before any external call          mutant differs in a single security-critical respect: its body
and reset after, and a cross-function safety lemma showing            fails to engage the guard correctly at the callback boundary,
that the guard’s protection extends across the multiple func-         leaving a reentrancy window. All other aspects — signature,
tions of the cToken interface that share the same _status             callback interface, control flow, surface API — are identical.
slot.                                                                 This is mutation testing for formal proofs: where naturally-
    The Layer 6-B capstone is structured as a thin wrapper            occurring near-misses combine multiple structural differ-
module that imports the supporting lemmas and discharges              ences with confounding context, the minimal-diff mutant
the target theorem by composition without modifying ei-               isolates the precise security-critical structural difference. A
ther lemma — an instance of the axiom-record-minimal                  single hand-constructed minimal-diff mutant is a princi-
wrapper composition of §4.3, which preserves axiom-record             pled choice over an operator-derived corpus [9], [10] —
minimality through the composition. The capstone records              a security-critical semantic regression test specifically opti-
minimal axiom dependence (no propositional extensionality             mized for formal specification boundary detection, distinct
required at this layer; the result is provable in the pure            from the random syntactic perturbations automated muta-
intensional fragment of Lean 4’s type theory). Full theorem           tion operators typically produce against production DeFi
statements, the wrapper module’s structure, and the per-              code.
lemma proof skeletons appear in Appendix A.                               The Layer 6-C theorems formalize discriminating
                                                                      power against this pair: production flashLoan satis-
5.5 Layer 6-C: boundary case (Aave V3 flashLoan vs                    fies guard-pattern correctness under the §5.1 predicate;
flashLoanVulnerable)                                                  flashLoanVulnerable fails it (a reentrancy trace is con-
The Layer 6-C boundary case is the methodological core                structible against the mutant); a supporting CEI-pattern
of the discriminating-power claim. Aave V3’s Pool con-                preservation lemma underwrites the first theorem and is
                                                                                                                               11

consumed by the second’s failure proof at the structural-         auxiliary lemma. Full prior-layer theorem statements and
adjacency boundary where the mutant deviates. The                 #print axioms output appear in Appendix A.
methodology thereby distinguishes safe flashLoan from
structurally-adjacent vulnerable flashLoanVulnerable              5.7   Reproducibility
at the precise boundary the boundary case is designed
to probe. Full theorem statements and the mutant’s diff           The corpus is reproducible end-to-end from a tagged com-
specification appear in Appendix A.                               mit per §4.4; full git checkout invocations, lake build
                                                                  commands, and expected axiom-record outputs appear in
                                                                  Appendix A.3.
5.6   Layer 6-D: tridirectional capstone
The Layer 6-D capstone meta-theorem composes the
three protocol-instantiation results into the tridirectional
                                                                  6     I MPLEMENTATION AND R EPRODUCIBILITY
discriminating-power claim: if the Layer 6-A derivation,
the Layer 6-B correctness theorem, and the Layer 6-C              This section presents the practitioner-facing evidence base
boundary-case pair all hold, then the methodology satisfies       for the discriminating-power claim: the size of the formal-
the discriminating-power predicate of §5.1 against the pro-       ization corpus, the CI gating discipline that re-checks the
duction protocol instantiations of §2.4 plus the minimal-diff     corpus on every push, and the tagged-commit reproducibil-
mutant of §5.5. The capstone is proven by direct conjunction      ity procedure that allows reviewers to verify the verification.
of the three prior-layer theorems — a wrapper construction        We do not report head-to-head comparison against heuristic
in the sense of §4.3 — without modification of any underly-       detectors (Slither, Mythril, Certora-style checking): founda-
ing proof.                                                        tional machine-checked verification establishes a different
    This composition shape is the operational signature           guarantee layer than heuristic detection, so the comparison
of the no-retrofit discipline of §4.2. The three protocol-        is qualitative by construction (per §1.2).
instantiation files were sealed prior to capstone authoring;
capstone construction had no path to modify them; the             6.1   Repository structure
capstone composed by direct conjunction nevertheless. We          The repository is organized at three top-level locations:
treat this as the first cross-protocol stress-test PASS against   paper/ (manuscript source, arXiv submission package, and
non-trivial protocol-semantics divergence: Compound v2’s          supporting artifacts), QanaryContracts/ (Lean 4 source
persistent-accounting model and Aave V3’s repay-within-           mapping to Layer 6-A/B/C/D — DAOContract.lean
transaction model differ in ways a retrofit-permissive work-      (Layer 6-A negative instance), CompoundContract.lean
flow could have used to shape underlying lemmas toward            (Layer 6-B positive instance), AaveBoundaryCase.lean
a common composition target — the discipline forbade that         (Layer 6-C boundary case), CrossProtocolAudit.lean
path and the composition succeeded anyway. Mathemati-             (Layer 6-D capstone) — plus supporting modules), and
cally the capstone is conjunction-introduction; the contribu-     methodology/ (canonical artifacts pointer-tabled at Ap-
tion is the demonstrated environmental-contract uniformity        pendix B). The continuous-integration configuration sits at
of the guard invariant across protocol architectures that         build.yml. All artifacts are reachable from any tagged
do not share an accounting model, made non-vacuous by             commit, so a reviewer who checks out a single tag obtains
foreclosing the co-development confound.                          consistent state across manuscript, source, and CI configu-
    The capstone’s axiom record is [propext]-only and             ration.
equals the union of the three prior-layer records (§4.3
wrapper preserves axiom-record minimality); no choice, no
excluded middle, no user-introduced axiom declarations            6.2   Corpus size
                                                       The formalization corpus is approximately 8,538 lines of
anywhere in the corpus. In the Lean formalization, the safe
                                                       Lean 4 source across the four protocol-instantiation layers
contract instance carrying production flashLoan is named
aaveContract, and the structurally-adjacent vulnera-   and supporting infrastructure: Layer 6-A formalizes the
ble contract carrying flashLoanVulnerable is named     DAO 2016 negative instance across ˜656 lines (6 theorems);
aaveContractAdjacent; the paper-body flashLoan vs      Layer 6-B Compound v2 across ˜517 lines (3 theorems);
flashLoanVulnerable distinction is the function-level  Layer 6-C Aave V3 across ˜770 lines (3 theorems including
                                                       the minimal-diff mutant); Layer 6-D the capstone in ˜260
view of the contract-level objects below. The capstone’s Lean
                                                       lines (1 theorem); supporting modules and lemmas total
4 statement and proof term illustrate the direct-conjunction
wrapper composition concretely:                        ˜6,335 lines. Per-file contribution and full theorem-to-file
theorem tridirectionalDiscriminatingPower_certificate :mapping appear in Appendix A (approximate per-layer
    (¬ OZGuardDisciplineGeneral daoContract) ∧         counts; exact per-file counts reproducible at the tagged
    (OZGuardDisciplineGeneral compoundContract) ∧
    (OZGuardDisciplineGeneral aaveContract ∧           commit per Appendix A.3).
      ¬ OZGuardDisciplineGeneral aaveContractAdjacent) :=
  ⟨daoContract_violates_OZGuardDisciplineGeneral,
   compoundContract_satisfies_OZGuardDisciplineGeneral,6.3 CI verification
   aaveBoundaryCase_certificate⟩                       The CI configuration of §4.4 — four parallel verification
   The proof term is exactly the triple ⟨h_dao,                   blocks, one per Layer 6-A/B/C/D — runs on every push.
h_compound, h_aave⟩ of the three sealed prior-layer               lake build compiles and type-checks the corpus at 901
theorems — no rewriting, no hypothesis adjustment, no             jobs; the axiom-record introspection of §4.4 verifies each
                                                                                                                               12

theorem against its recorded expectation. Wall-clock veri-       discipline forecloses by construction. What remains as an
fication runs in the order of minutes per push on stan-          explanation for the observed PASS is genuine portability of
dard runners. CI failure on any block — type-check fail-         the guard pattern’s correctness across structurally-divergent
ure, axiom-record drift, or supporting-lemma regression —        lending-family architectures, within the scope qualified at
surfaces immediately in the pull-request status. Full per-       §9.4.
theorem axiom records appear in Appendix A.
                                                                 7.2   Future work
6.4   Reproducibility posture
                                                                 The methodology is candidate for application to other
Every proof-authoring session is recorded as a tagged-           reentrancy variants — read-only reentrancy at proto-
commit-anchored artifact; the directive + closure-               cols whose view functions feed downstream consumers
report discipline is documented in the companion                 (the Curve gauges 2022 case), cross-function reentrancy
methodology paper. The corpus is reproducible                    where multiple guarded functions share state — and
end-to-end from a tagged commit: the substantive                 other OpenZeppelin defense patterns (AccessControl,
substrate is sealed at v1.3-layer6-closure; the                  Pausable, ReentrancyGuardUpgradeable, upgrade-
methodology framework canonization is sealed at                  able proxy pathways), each carrying its own correctness
v1.7-methodology-housekeeping. The manuscript                    predicate amenable to the same tridirectional treatment.
content corresponding to this paper version is sealed at         Beyond reentrancy and OpenZeppelin, the methodology
intermediate tag v1.6-phase7-closure (the abstract’s             framework canonical artifacts (the subject of the companion
reproducibility anchor); see §4.4 for the relationship           methodology paper) enable application to formal verifi-
between these three tags. Full reproduction commands and         cation more broadly, including non-smart-contract targets
the pinned dependency graph appear in Appendix A.                where the no-retrofit composition discipline addresses the
                                                                 same proof-brittleness pain point. Continuous-integration-
                                                                 driven verification at protocol upgrade events is a final
                                                                 natural extension.
7     D ISCUSSION
7.1   Implications
The result extends machine-checked verification for smart-
contract security beyond the pattern-recognition layer at        8     R ELATED W ORK
which auditors operate and beyond the toy-example layer          This section positions the discriminating-power result
that has constrained much prior academic verification work.      against four bodies of prior literature: prior formal verifi-
The tridirectional discriminating-power claim is established     cation of smart contracts at large; reentrancy-specific work;
against production-deployed Solidity source for the Open-        compositional formal verification in adjacent domains; and
Zeppelin guard pattern — Compound v2 and Aave V3                 AI-assisted formal verification context. The compression
production sources plus the historical DAO 2016 contract         discipline of §1 + §4 + §5 carries through here: survey
— rather than against simplified models. The contracts           breadth across the four categories, with sharp positioning
addressed collectively secure substantial production de-         of the present contribution against what the surveyed work
posits (§2.4, §5.4); economic significance is ecosystem-load-    has and has not previously demonstrated.
bearing rather than research-prototype. The no-retrofit com-
position discipline (§4.2) establishes a stronger empirical
claim than co-developed composition: the three protocol-         8.1   Prior formal verification of smart contracts
instantiation proofs were sealed before the capstone meta-       Three broad classes of prior work have addressed smart
theorem was authored, the capstone composed by di-               contract correctness at varying levels of foundational rigor.
rect conjunction without modification of any underlying              SMT-based static analysis tools — Slither, Mythril, Se-
proof, and we read this as evidence that the OpenZeppelin        curify, and Manticore among the widely deployed — op-
guard pattern’s correctness is portable across the observed      erate at the deployment-scale layer with heuristic pattern-
protocol-instantiation boundary rather than an artifact of co-   matching against known vulnerability classes (Slither, Secu-
developed proofs.                                                rify), symbolic execution (Mythril, Manticore), or declara-
    The empirical meaning of the cross-protocol PASS under       tive property checking (Securify). These tools have driven
N=1. The single observed composition (Compound v2 →              a substantial fraction of pre-deployment audit workflow
Aave V3) is N=1; its significance is not that composition        and are the de facto baseline for industrial smart contract
occurred but what occurred under the no-retrofit constraint.     security. Their strength is scalability; their limitation is that
While N=1 at the protocol-family level, the composition          pattern recognition does not establish foundational cor-
proofs exercise two fundamentally divergent financial state      rectness, and structural-adjacency boundaries are precisely
architectures — persistent ledger balance accounting on          where their precision degrades (per §1.2).
Compound v2 vs. transient intra-transaction flash-lending            Theorem-prover-based and specification-driven verifi-
on Aave V3 — making the boundary a rigorous qualitative          cation has demonstrated foundational rigor on narrower
stress test of guard-invariant portability despite the low       targets. Bhargavan et al. [1] formalized EVM operational
protocol count. A retrofit-permissive workflow admits an         semantics in F* and Coq (POST 2016 and subsequent);
explanation — the underlying proofs were silently shaped         Hildenbrandt et al.’s KEVM [2] (CSF 2018) provided a
toward a common target — that the sealed-before-capstone         complete executable EVM semantics in the K framework;
                                                                                                                              13

Grishchenko, Maffei, and Schneidewind [3] (POST 2018)            production-grade C compiler, with subsequent work ex-
developed an F*-based semantic framework for EVM se-             tending the discipline. Iris [8] developed higher-order con-
curity analysis; Hirai’s Lem formalization [4] addressed         current separation logic applied across concurrent program
EVM bytecode semantics for proof assistant integration.          verification targets. These establish that large-scale compo-
Subsequent Coq-based work has formalized individual con-         sitional formal verification is feasible at production-relevant
tracts or contract subsets. Certora’s Prover applies SMT-        scale when the composition discipline is enforced explicitly.
based discharge against specifications expressed in CVL,         Within smart contract verification specifically, prior work
deployed in production audit workflows; its strength is scale    has demonstrated modular proofs at the single-contract
and tool-driven specification discharge rather than foun-        scope; cross-protocol composition of guard-pattern correct-
dational machine-checked correctness in the proof-assistant      ness at production scale, under a discipline that forbids
sense. These contributions are foundational at the platform-     retrofit of underlying lemmas (the no-retrofit composition
semantics or specification-discharge layer; cross-protocol       discipline of §4.2), has not been previously demonstrated.
composition of guard-pattern correctness against multiple
production protocol instantiations has not been previously       8.4   AI-assisted formal verification context
demonstrated in this line of work.                               Recent AI-assisted formal verification explores LLMs in two
    Property-based testing tools — Foundry fuzz testing and      roles: proof-tactic synthesis and audit assistance. Specific
Echidna — have driven substantial bug discovery at deploy-       systems — Baldur [11] (whole-proof generation/repair),
ment scale. Their strength is finding counterexamples; they      LeanDojo [12] (retrieval-augmented Lean tactic search), CO-
do not establish foundational correctness. See Appendix C        PRA [13] (in-context-learning theorem-proving agent) —
for at-a-glance positioning against Certora, Move Prover,        preserve proof-assistant soundness (the LLM proposes; the
VeriSol, and KEVM.                                               kernel checks) but operate at per-proof tactic-automation
    Prior formal verification of smart contracts has demon-      granularity rather than at the verification-architecture or
strated theorem-prover-based formalization of platform se-       audit-discipline level. AI-assisted audit work has typically
mantics or isolated contracts at the foundational layer, or      operated as single-model review; convergence/divergence
scalable SMT-based pattern recognition at the deployment         analysis across multiple independent reasoning models is
layer; demonstration of foundational correctness against         novel methodology, subject of the companion methodology
multiple production protocols with no-retrofit composition       paper rather than a claimed contribution here.
discipline has remained an open challenge.
                                                                 9     L IMITATIONS
8.2   Prior reentrancy-specific work                             This section adds limitations within the discriminating-
                                                                 power claim’s domain that constrain its scope; out-of-scope
Reentrancy has received targeted attention across run-
                                                                 attack classes are enumerated at §3.4.
time, static, and disclosure-driven layers. Sereum [5] in-
troduced runtime monitoring for reentrancy patterns at
                                                                 9.1   Single attack class and single defense pattern
the EVM execution layer — deployable but not preven-
tive at the source level, not aimed at foundational correct-     The single-attack-class focus is a principled choice:
ness. Static analyzers including SmartScopy [6] and similar      reentrancy is the canonical class for which the
pattern-recognition tools targeted at the reentrancy class       OpenZeppelin guard was constructed and where the
apply pattern-recognition discipline; precision is empirically   structural-adjacency boundary is well-defined and
strong for classical reentrancy and weakens at structural-       machine-checkable end-to-end. The work addresses
adjacency boundaries (per §1.2) and at cross-function and        the OpenZeppelin reentrancy guard pattern only;
read-only variants. Mutation testing [9], [10] introduces        other defensive patterns (AccessControl, Pausable,
small syntactic faults to assess sensitivity to structurally-    ReentrancyGuardUpgradeable, upgradeable proxy
adjacent regressions; the Layer 6-C boundary case (§5.5)         pathways) are not within scope. The no-retrofit composition
applies this methodology to machine-checked proofs of            discipline and axiom-record-minimal wrapper composition
production smart contracts — to our knowledge a first —          (§4.2, §4.3) are applicable to other patterns by construction,
using a single hand-constructed minimal-diff mutant rather       but empirical validation across multiple defense patterns at
than an operator-derived corpus (defended at §5.5 and            production scale is future work (§7.2).
§9.2). Read-only reentrancy emerged as a recognized attack
class following the Curve Finance gauges 2022 disclosure         9.2   Constructed mutant boundary case
(callback reentrancy on view functions returning stale state);   The Layer 6-C boundary case includes one constructed
it is acknowledged here as future-work scope (§7.2). Foun-       variant — flashLoanVulnerable, a minimal-diff mutant
dational machine-checked discriminating-power against the        (§5.5). Per the §1.3 reframing this is mutation testing for
OpenZeppelin guard pattern at production protocol scale          formal proofs (grounded in [9], [10]): the hand-constructed
has not been previously demonstrated.                            minimal-diff mutant is a principled choice, not a conces-
                                                                 sion — it isolates the structural-adjacency boundary in a
                                                                 way naturally-occurring near-misses cannot, with the cor-
8.3   Related composition discipline work                        pus N=1 by design. Identifying and formalizing real his-
Compositional formal verification has been extensively de-       torical near-miss instances (Curve gauges 2022 read-only-
veloped in adjacent domains. CompCert [7] is the canon-          reentrancy class, Lendf.Me 2020 ERC-777 callback class, and
ical exemplar — compositional correctness proofs for a           similar) is acknowledged future work.
                                                                                                                               14

9.3   Source-level abstraction and trust assumptions              (§7, §8). The verification’s audit trail is inspectable end-
Operating at Solidity source level (per §3.2) rather than raw     to-end; the methodology framework that generalizes this
EVM bytecode is a deliberate scoping choice: source level is      posture is the subject of the companion paper, with the
where the guard pattern is expressed and its discriminating-      Appendix B pointer summarizing its canonical artifacts.
power boundary sharpest, and it keeps the Lean-model-             Future work (§7.2, §9) extends the discriminating-power
fidelity and solc-compilation assumptions (§3.3) explicit         framework to additional attack classes and defense patterns,
and separable. Recent EVM-level formalization work (§8.1          EVM-bytecode-level formalization, cross-language applica-
— KEVM line) is the foundation for a future verified-             tion, and continuous protocol-upgrade verification.
translation extension closing both gaps. Standard formal-
verification trust assumptions apply (§3.3, §6.4): Lean 4
kernel + mathlib4 correctness, pinned dependency graph
at the tagged commits. The honest-borrower-at-protocol-           A PPENDIX A
invariant-computation-only assumption (§3.3) constrains           T HEOREM S TATEMENTS , A XIOM R ECORDS , AND
the claim — borrowers may be adversarial (§3.1) but               R EPRODUCTION
protocol-internal accounting is assumed to execute as writ-
ten. Expansion to attacker-controlled-protocol threat models      This appendix is the substantive substrate anchor for the
is future work. No consensus-layer behavioral assumption          discriminating-power claim. It absorbs the full-statement
is made.                                                          and axiom-record detail deferred from §5 and §6, so a re-
                                                                  viewer can verify the corpus end-to-end. Full Lean 4 source
                                                                  — with exact type signatures, dependent-type declarations,
9.4   Cross-protocol claim scope
                                                                  and definitions — is in the repository at the tagged commit
The cross-protocol composition rests on three instantia-          v1.3-layer6-closure; the paraphrases below state what
tions: DAO 2016 (historical exemplar), Compound v2 (lend-         each theorem establishes at the level a reviewer needs before
ing), Aave V3 (lending / flash-loan facility). The two live       consulting the source.
protocols are both lending-family; the no-retrofit stress-
test crosses a within-lending-family boundary (persistent
balance-accounting vs. single-transaction flash-loan archi-       A.1   Theorem statements
tecture), not a between-domain boundary (AMM, CDP,                The corpus comprises thirteen theorems across four layers,
derivatives). The portability claim is therefore scoped to        matching the §5.2 inventory exactly.
uniformity of the local guard invariant across divergent              Layer 6-A — DAO 2016 negative instance (1 target + 5
lending-family host architectures plus the historical reen-       supporting = 6). The target theorem states that, under the
trancy exemplar; broader-family instantiation is future work      reentrancy predicate of §5.1, an attacker-controlled re-entry
(§7.2).                                                           call trace against the formalized DAO splitDAO source
                                                                  is constructible, and that this trace breaks the contract’s
                                                                  balance-sum invariant. The five supporting lemmas dis-
                                                                  charge the pieces of the derivation: call-stack interleaving,
10    C ONCLUSION                                                 storage-observation before balance update, balance-update
We     presented     a     machine-checked,      tridirectional   sequencing, external-call-boundary placement, and the ab-
discriminating-power       formal    verification     of    the   sence of any guard-pattern protection.
OpenZeppelin reentrancy guard pattern across three                    Layer 6-B — Compound v2 cToken positive instance (1 target
production protocol instantiations: a negative-instance           + 2 supporting = 3). The target theorem states that every
derivation of the classical reentrancy attack from DAO 2016       execution trace conforming to the cToken withdrawal path
contract source; a positive-instance correctness proof for the    satisfies the guard-pattern correctness predicate of §5.1, so
Compound v2 cToken withdrawal path; and a boundary                no reentrancy trace is constructible against it. A guard-
case distinguishing production Aave V3 flashLoan                  invariant lemma shows the _status slot is set before any
(CEI-correct by construction) from its minimal-diff mutant        external call and reset after; a cross-function safety lemma
flashLoanVulnerable under a mutation-testing-for-                 shows the protection extends across the cToken interface
formal-proofs design. A capstone meta-theorem composes            functions sharing that slot. The target is discharged by a thin
the three prior-layer results by direct conjunction, and all      wrapper that composes the two lemmas without modifying
thirteen theorems are machine-checked under continuous            either, preserving axiom-record minimality.
CI gating with zero sorry, zero user-introduced axioms,               Layer 6-C — Aave V3 boundary case (2 target + 1 sup-
and [propext]-only axiom records across the corpus.               porting = 3). The first target theorem states that production
    The significance is twofold. First, the verified protocols    flashLoan satisfies guard-pattern correctness under the
secure substantial deposits at production scale (§2.4, §5.4),     §5.1 predicate. The second target theorem states that the
grounding the discriminating-power claim in load-bearing          minimal-diff mutant flashLoanVulnerable fails it —
real-contract source rather than illustrative models. Sec-        equivalently, that a reentrancy trace is constructible against
ond, the capstone composed across the Compound v2 →               the mutant under the same predicate. A checks-effects-
Aave V3 protocol-instantiation boundary under a no-retrofit       interactions preservation lemma underwrites the first tar-
composition discipline that forbids retrofitting underlying       get and is consumed by the second’s failure proof at the
proofs toward a composition target — the first such cross-        structural-adjacency boundary where the mutant deviates
protocol composition demonstrated under this discipline           from production.
                                                                                                                                       15

     Layer 6-D — tridirectional capstone (1 target = 1). The     A PPENDIX B
 capstone meta-theorem states that if the Layer 6-A deriva-      M ETHODOLOGY F RAMEWORK P OINTER
 tion, the Layer 6-B correctness theorem, and the Layer 6-C
                                                                 B.1    Scope of this pointer
 boundary pair all hold, then the methodology satisfies the
 discriminating-power predicate of §5.1 against the §2.4 pro-    Per the boundary discipline of §1, the methodology frame-
 duction instantiations plus the §5.5 mutant. It is proven by    work underpinning this work — the no-retrofit composi-
 direct conjunction of the three prior-layer theorems, with no   tion discipline of §4.2, the axiom-record-minimal wrapper
 modification of any underlying proof during composition.        composition of §4.3, and the multi-model audit workflow
                                                                 of §4.5 — is canonized as a separate body of work and
                                                                 presented in full in a companion methodology paper (sepa-
 A.2    Per-theorem axiom records
                                                                 rate arXiv submission). The brief operational presentations
 Every theorem is verified against an explicit #print            in §4 suffice for the substantive smart-contract-verification
 axioms expectation, re-checked on every push and gated          claims of the present paper. This appendix is deliberately
 to fail the build on any drift. Across all four lay-            thin: it provides a pointer table mapping the framework
 ers, the per-function inner lemmas are kernel-only (zero-       labels to their canonical artifact locations, for readers who
 axiom; no propositional extensionality required), and the       encounter those labels in the public artifact record (for
 master/wrapper/meta theorems carry [propext]-only               example, in the project’s commit history). It does not present
 records — no choice, no excluded middle, no user-               the framework’s sub-pattern catalog, graduation criteria, or
 introduced axioms anywhere in the corpus. The Layer 6-          cross-protocol empirical history; those are the scope of the
 D capstone’s [propext] record is exactly the union of           companion paper.
 the three prior-layer records and introduces no new axiom;          The separation is deliberate length-scoping, not with-
 the project introduces zero new axioms over the Lean 4 +        holding: this paper’s discriminating-power result is fully
 mathlib4 baseline. No theorem in the corpus is admitted         evaluable on its own terms — the thirteen theorems, their
 with sorry, admit, or any user-introduced axiom decla-          axiom records, and the no-retrofit discipline’s operational
 ration. Exact per-theorem records are CI-gated (§6.3) and       consequence (§4.2) are stated and verifiable here. The com-
 reproducible per Appendix A.3.                                  panion framework adds generalization beyond the present
                                                                 scope and is not load-bearing for this paper’s substantive
 A.3    Reproduction commands                                    claims.

 The corpus is reproducible end-to-end from the tagged
 commit:                                                         B.2    Canonical artifacts
 git clone https://github.com/ ⌋                                 The methodology framework’s canonical artifacts — the
,→   rayiskander2406/qanary-contracts.git                        wrapper-layer absorption pattern (axiom-record-minimal
 cd qanary-contracts                                             composition; §4.3), the compose-from-outside discipline
 git checkout v1.3-layer6-closure                                (no-retrofit composition; §4.2), and the family-level
 lake build                                      #               authoring-layer-estimation-imprecision meta-pattern — are
,→   901 jobs green                                              sealed at the repository tag for methodology-framework
 lake env lean                                                   canonization and presented in full in the companion
,→   QanaryContracts/PrintAxioms.lean #                          methodology paper. Full graduation history, sub-pattern
,→   verifies every theorem's axiom record                       catalog, four-outcome audit-findings triage framework, and
    The dependency graph is pinned and locked:                   the cross-protocol empirical history of the framework’s ap-
                                                                 plication appear there.
    •    Lean compiler version pinned at lean-toolchain
         (leanprover/lean4:v4.30.0-rc1).
    •    mathlib4           dependency       pinned         at A PPENDIX C
         lakefile.lean               (input          revision C OMPARISON AGAINST INDUSTRIAL FV FRAME -
         322515540d7f)         and    locked   to    commit
                                                               WORKS
         322515540d7fd29ef8992b82c89044f86f02ac10
         via lake-manifest.json.                               For reviewer at-a-glance positioning, the following table
    •    The four parallel CI blocks at build.yml lines 287, compares the present work against the principal industrial
         356, 408, and 464 re-run on every push and surface / academic formal verification systems for smart contracts
         any drift in the dependency graph or the corpus.      and adjacent verification work (§8.1).
     A permanent archival snapshot of the artifact
 is deposited on Zenodo under the concept DOI
 10.5281/zenodo.20510920, which always resolves to
 the latest archived version.                                    R EFERENCES
     The           methodology-framework             canoni-     [1]   K. Bhargavan et al., “Formal verification of smart contracts (short
 cal    artifacts   are    sealed   at    the   later    tag           paper),” in Proc. ACM Workshop Programming Languages and Anal-
                                                                       ysis for Security (PLAS), 2016.
 v1.7-methodology-housekeeping;               a    reviewer
                                                                 [2]   E. Hildenbrandt et al., “KEVM: A complete formal semantics of
 evaluating the methodology framework rather than                      the Ethereum Virtual Machine,” in Proc. IEEE Computer Security
 the proof substrate should check out that tag.                        Foundations Symp. (CSF), 2018.
                                                                                                                                                   16

                                                                       TABLE 2
          Positioning against principal industrial / academic formal verification systems for smart contracts and adjacent verification work.


System                         Verification target           Composition support            Axiom footprint                Production deployment
QANARY (this paper)            Source-level OZ guard         No-retrofit cross-protocol     [propext]-only; zero           Compound v2, Aave V3
                               pattern across 3              meta-theorem; sealed           user-introduced axioms;        mainnet contracts;
                               production protocols          prior-layer composition        CI-gated                       tagged-commit
                                                                                                                           reproducible
Certora Prover                 CVL specifications            Per-rule local; no             SMT-solver trust; no           Production audit
                               discharged via SMT            foundational composition       kernel-level record            workflows across major
                                                             discipline                                                    DeFi protocols
Move Prover (Dill et al.)      Move-language smart           Modular specs; no              SMT trust                      Aptos, Sui mainnet
                               contracts; spec-driven        cross-protocol meta-claim                                     runtime checks
VeriSol (Lahiri et al.)        Solidity → Boogie             Modular contract               SMT/Boogie trust               Microsoft (now
                               translation; spec-driven      verification                                                  deprecated)
KEVM (Hildenbrandt et          EVM bytecode                  Platform-semantics layer;      K-framework trust              Foundational artifact;
al.)                           operational semantics in      no per-contract                                               deployed via consumer
                               K                             composition claim                                             tools



[3]  I. Grishchenko, M. Maffei, and C. Schneidewind, “A semantic
     framework for the security analysis of Ethereum smart contracts,”
     in Principles of Security and Trust (POST), LNCS 10804, 2018.
[4] Y. Hirai, “Defining the Ethereum Virtual Machine for interactive
     theorem provers,” in Proc. Financial Cryptography and Data Security
     (WTSC), 2017.
[5] M. Rodler, W. Li, G. O. Karame, and L. Davi, “Sereum: Protect-
     ing existing smart contracts against re-entrancy attacks,” in Proc.
     Network and Distributed System Security Symp. (NDSS), 2019.
[6] Y. Feng, E. Torlak, and R. Bodı́k, “Precise attack synthesis for
     smart contracts (SmartScopy),” in Proc. ACM Conf. Computer and
     Communications Security (CCS), 2018.
[7] X. Leroy, “Formal verification of a realistic compiler (CompCert),”
     Commun. ACM, vol. 52, no. 7, 2009.
[8] R. Jung et al., “Iris: Monoids and invariants as an orthogonal basis
     for concurrent reasoning,” in Proc. ACM Principles of Programming
     Languages (POPL), 2015.
[9] R. A. DeMillo, R. J. Lipton, and F. G. Sayward, “Hints on test data
     selection: Help for the practicing programmer,” IEEE Computer,
     vol. 11, no. 4, 1978.
[10] Y. Jia and M. Harman, “An analysis and survey of the develop-
     ment of mutation testing,” IEEE Trans. Software Engineering, vol.
     37, no. 5, 2011.
[11] E. First, M. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
     generation and repair with large language models,” in Proc. ACM
     ESEC/FSE, 2023.
[12] K. Yang et al., “LeanDojo: Theorem proving with retrieval-
     augmented language models,” in NeurIPS, 2023.
[13] A. Thakur, G. Tsoukalas, Y. Wen, J. Xin, and S. Chaudhuri, “An
     in-context learning agent for formal theorem-proving (COPRA),”
     in Conf. Language Modeling (COLM), 2024.
