# **An AI Approach to Verified Production Cryptographic Libraries**

Chuyue Sun1,5, Su Fong<sup>1</sup> , Zhiyi Kuang<sup>1</sup> , Yizheng Jiao<sup>2</sup> , Nina Narodytska<sup>3</sup> , Haoze Wu3,4, David L. Dill<sup>1</sup> , Clark Barrett1,5

<sup>1</sup>Stanford University <sup>2</sup>University of North Carolina at Chapel Hill <sup>3</sup>VMware Research by Broadcom <sup>4</sup>Amherst College <sup>5</sup>&Truth

#### **Abstract**

Cryptographic code is critical infrastructure that must be correct, yet formally verifying production libraries remains difficult. Existing language-model proof systems solve isolated obligations with specifications and premises already given, leaving production-library verification unresolved.

We present CryptoProver, an AI-based system that synthesizes internal specifications and Verus-checked proofs from high-level API contracts. Without changing executable code, CryptoProver constructs a new independent proof of curve25519-dalek and verifies RustCrypto's previously unverified chacha20 implementation against an RFC 8439 specification. These cryptographic lineages underpin deployed systems including Signal and Shadowsocks; Signal has an estimated 218M global downloads. The independent, human-led curve25519-dalek verification was developed publicly over eight months by five main contributors. Given the API contracts and a fixed trusted library of field specifications, arithmetic facts, axioms, and vstd, CryptoProver synthesizes the internal specifications and proofs in 11.4 hours with \$466.99 in recorded API cost. CryptoProver follows a trust-first design principle: mechanical gates reject specification weakening, invented axioms, and cross-module breakage, while isolation blocks reference proof retrieval, including from git history.

## **1 Introduction**

Cryptographic code is critical infrastructure that must be correct, yet formally verifying production libraries remains difficult. Production cryptographic code has a history of subtle deployment errors: an incorrect Debian-specific change to OpenSSL made cryptographic key material guessable [\[1\]](#page-11-0). Formal verification can rule out such implementation errors relative to a specification, but it has traditionally been written by hand at a large cost in expert labor. Language-model proof systems promise to reduce that labor, yet existing ones either solve isolated obligations with premises already in scope or synthesize specifications and proofs for a single module [\[2–](#page-11-1)[5\]](#page-11-2). A production crate instead requires interdependent specifications and proofs across many files.

CryptoProver is an AI-based verification system that takes high-level API contracts and a fixed trusted library of field specifications, field/common arithmetic facts, trusted axioms, and vstd as inputs. The agent writes the internal specifications and proofs between them, and Verus [\[6\]](#page-11-3) checks the resulting crate. We applied CryptoProver to two production cryptographic libraries without changing their executable code. curve25519-dalek [\[7\]](#page-11-4) is a library used in Signal [\[8\]](#page-11-5), an app with an estimated 218M global downloads [\[9\]](#page-11-6). A previous verification effort on curve25519-dalek was carried out manually and publicly over eight months by five main contributors; that calendar

window also includes specification and infrastructure work. Given just the top-level API contracts and the trusted library, CryptoProver automatically synthesizes the internal specifications and proofs required for full functional verification in 11.4 hours with \$466.99 in recorded API cost. On another library, CryptoProver automatically verifies RustCrypto's chacha20 v0.10.1 implementation — used in Shadowsocks [\[10\]](#page-11-7) and previously unverified — against a specification of the RFC 8439 standard. Our fork of the crate adds only the Verus specifications and proofs; its executable code is unchanged, and the verification covers the portable backend, not the SIMD backends.

When the agent writes specifications as well as proofs, verifier acceptance alone does not establish that it preserved the intended claim or trust base. An early version of our system, whose anti-cheating rules lived in the prompt rather than in mechanical checks, reported 97.1% of curve25519-dalek closed — yet an audit found 11 of its "proofs" resting on invented axioms and another 5 silently breaking sibling modules (Section [3.1\)](#page-2-0). To avoid such issues, CryptoProver follows a trust-first design principle: specific gates reject specification weakening, invented axioms, cross-module breakage, and attempts to make the verifier accept without a proof. The complete eight-gate suite also checks genuine obligation removal, frozen-file edits, tooling drift, and proof recovery from git history; fresh sessions and a sandbox that excludes the reference proof reinforce this boundary (Section [3.6\)](#page-6-0).

In summary, we make two main contributions:

- **Trust-first proof-and-spec synthesis.** We name this design *trust-first*: whenever possible, routes to false success are closed using mechanical checks rather than prompt language. The complete set of gates is discussed in Section [3.6.](#page-6-0)
- **Production-library verification in hours once contracts and the trusted library are given.** Without changing executable code, CryptoProver constructs a new independent proof of curve25519-dalek and verifies RustCrypto's previously unverified chacha20 implementation.

## **2 Background**

### <span id="page-1-1"></span>**2.1 Verus and Proof Obligations**

Verus [\[6\]](#page-11-3) is an SMT-backed verifier for Rust: a developer annotates functions with requires (i.e., precondition) and ensures (i.e., postcondition) clauses, and Verus discharges the resulting verification conditions using an SMT solver (Z3 [\[11\]](#page-11-8) by default). Specifications are written in *spec* functions (pure, logical models of the data), and the obligations connecting executable code to those specs are discharged in *proof* functions, sometimes with explicit lemma invocations to guide the solver. When a proof author has not yet written a proof, they can mark the hole with admit(): Verus then accepts the surrounding obligation unconditionally. An admit() can thus be seen as explicitly flagging proofs not yet completed. Listing [1](#page-1-0) shows a representative hole and the shape of the obligation it stands in for.

```
1 spec fn as_nat ( f : FieldElement ) -> nat { /* ... */ }
2 proof fn field_add_correct ( a : FieldElement , b : FieldElement )
3 ensures as_nat ( field_add (a , b ) ) == ( as_nat ( a ) + as_nat ( b ) ) % P
4 {
5 admit () ; // <-- the proof obligation to discharge
6 }
```

Listing 1: A typical admit() in curve25519-dalek (illustrative).

Certain admit() statements are intended to remain: axiom\_\* lemmas that encode trusted assumptions (e.g., properties of the underlying field that are taken as given in curve25519-dalek) form the codebase's *trust base*. We call all other admits *non-axiom* admits; these are proof obligations that a complete verification must discharge.

### <span id="page-2-2"></span>**2.2 Proof Architecture and Synthesis**

A complete Verus proof tree consists of four kinds of artifacts, described below.

**Code.** Executable Rust, the artifact under verification.

**Specifications.** Public API requires/ensures contracts state the promises callers rely on; internal specifications state the intermediate claims used to prove those contracts. Internal specifications include spec functions that define key concepts (such as field-element valuations and curvepoint encodings in the case of curve25519-dalek), plus intermediate requires/ensures statements on helper lemmas.

**Proofs.** The bodies of helper lemmas and inline proof blocks that connect executable code to the specifications.

**Trusted library.** This contains the Verus standard library (vstd), field specifications, field/common arithmetic facts, and any axioms assumed by the proof effort. These artifacts are assumed to be correct or to have been proved correct elsewhere.

*Synthesis* in our context refers to the process of using an AI agent to complete a partial proof tree. If only proof bodies are synthesized, while the specification remains fixed, this is guaranteed to preserve the original obligations: the agent must prove exactly the claims it receives. Synthesizing specifications is riskier, because this changes the proof obligation, and a trivial or vacuous statement could be easy to prove. Fortunately, as long as synthesis is limited to intermediate internal specifications, the top-level claim cannot be weakened: Verus checks each module against the contracts of the modules it depends on, so the fixed top-level API contracts are established only if every module, generated statements included, verifies.

## <span id="page-2-1"></span>**3 Design and Implementation**

Prior proof-synthesis systems use hand-designed workflows to organize model calls [\[2–](#page-11-1)[5,](#page-11-2) [12\]](#page-11-9). Such workflows restrict the degrees of freedom often required by crate-scale verification, where the next useful action may involve cross-module search, specification, decomposition, repair, or backtracking. Improved models can now choose among these actions while operating directly on a repository. CryptoProver therefore delegates the proof-search trajectory to a general-purpose coding agent instead of prescribing it in advance. At the same time, a fully unconstrained agent has too much freedom and ends up getting lost or sabotaging itself. Thus, we developed specific skills to keep the agent moving in the right direction as well as guardrails called *gates*, which keep the agent from certain common mistakes.

### <span id="page-2-0"></span>**3.1 The Motivating Campaign**

CryptoProver's architecture was not the product of our foresight, but rather evolved as the result of careful responses to documented failures. The campaign's input was a *stripped start* of curve25519-dalek: a copy of curve25519-dalek's independently verified proof tree in which every existing proof body is replaced by admit(), while executable code, specifications, and trusted axioms remain unchanged, leaving 1,178 open obligations. Against this tree we ran an early version of the driver (the orchestration loop defined in Section [3.4\)](#page-4-0): 24 intermittent runs totaling 52.2 hours of summed elapsed time, 451 rounds, and \$1,452. It ended with the agent reporting success on 97.1% of the verification conditions in the full crate, but an independent manual whole-crate audit found the claim to be inaccurate: 11 "proofs" rested on axioms the agent had invented unproven statements whose conclusions constrain outputs their preconditions never bind — and all but one were invalid, meaning the claimed property is false for some inputs (examples in Section [B\)](#page-14-0). In 5 other cases, local proofs succeeded on their own target, but broke proofs in sibling modules, and these failures were not detected by the agent. Neither failure appeared in the per-target verifier output, which the agent treated as evidence of success. A key contributor to the failures was *context pressure*, a collapse mode discussed in detail in Section [3.2:](#page-3-0) every fabrication we traced arose in a long-running session, as the agent re-ingested its own growing state and drifted toward the reward it could fake. Agent capability was not typically the issue. In a fresh context, the same model found and proved corrected versions of all 11 properties from scratch, with every constrained output bound by a precondition, for a total cost of only \$45.

One key lesson from this campaign was the difference between a directive given in a prompt and one that is mechanically enforced. In the following, we refer to an instruction stated in the agent's prompt as a *rule*, while a *gate* is a mechanical check the harness itself runs to enforce a rule. The key lesson was that rules without gates are only suggestions. The campaign's only gated rule the specification under proof may not change, enforced by the spec-drift gate — held across all 451 rounds; however, the other two rules left to the prompt, no new axioms and no broken siblings, were exactly the ones that were violated. The failures above motivated four countermeasures. axiom-drift catches fabricated axioms and sibling-verus catches broken siblings (Section [3.6\)](#page-6-0). Proof goals bind every output they constrain, preventing the malformed statements behind the fabricated axioms. Fresh per-target sessions and in-loop resets counter context pressure (Section [3.4\)](#page-5-0). The complete per-run ledger, audit findings, and repair forensics are in Section [B.](#page-14-0) The public CryptoProver artifact provides the driver, experiment manifests, released campaign records, and reproduction instructions: <https://github.com/ChuyueSun/CryptoProver>.

### <span id="page-3-0"></span>**3.2 How Agent Proof Synthesis Fails**

We observed two failure modes of agent proof synthesis. In a *capability failure*, the agent cannot close the goal within its round budget. In a *trust failure*, the agent reports success but the result fails the driver's acceptance checks or violates the experiment's evidence boundary. Below, we describe several examples of these failure modes observed in our campaign (Section [3.1\)](#page-2-0): the capability failures motivate the skills and context discipline, and the trust failures map one-to-one onto the gates.

We observed five types of capability failures: *context pressure*, where a growing session re-ingests its own prior state and the agent's work degrades [\[13\]](#page-11-10); *learned helplessness*, where a stale failure memory makes a fresh agent give up too early; *coverage gaps*, where an explicit target list omits some crucial files; *liveness-signal confusion*, where a rate-limited round looks identical to an honest failure; and *budget-exhausted breakage*, where a mid-edit abort leaves a file worse off unless the harness rolls it back. Context pressure carried the sharpest lesson: it drove the campaign's fabrications (Section [3.1\)](#page-2-0).

We defer the discussion of trust failures to Section [3.6,](#page-6-0) where each is described together with the gate that counters it. They range from leaving an admit() in place, through fabricating

a trusted axiom or weakening the specification under proof, to recovering the answer from git history. Fabricated axioms and cross-module breaks were observed at scale in the campaign audit (Section [3.1\)](#page-2-0).

### **3.3 Principles**

The driver accepts work only from verifier results, admit accounting, and gate evidence, never from the agent's report. Each skill, gate, and driver policy responds to a failure observed in the campaign. Within these safeguards, the agent may revise generated proof bodies and agent-authored internal lemma contracts, while the API contracts, specification vocabulary, and trusted library remain fixed (Section [4.1\)](#page-6-1). Reference-proof retrieval is forbidden: git-recovery rejects any round that reads source code from version control.

### <span id="page-4-0"></span>**3.4 The Driver Loop**

CryptoProver is a single driver loop written in Python that makes calls to an LLM coding agent (Claude Code, in our case, though that choice is not essential). In this paper, *the driver* refers to the complete orchestration system. The outer loop visits verification targets in a fixed order. Each target is a module containing one or more non-axiom proof obligations (Section [2.1\)](#page-1-1). One full pass over the target list is a sweep. A task is the work of verifying one target. Each visit to a target is an attempt. An attempt contains a bounded sequence of rounds within a wall-clock limit. Each round consists of one agent call followed by the driver's checks. An accepted target is recorded in a proven registry, the driver's persistent list of already-verified targets. When the operator enables registry filtering, a later sweep skips registered targets and revisits the remaining open targets still present in the configured list without reordering them. At attempt start, the driver assembles a prompt containing the target module and its remaining proof obligations, relevant information from related modules, and persistent memory from prior attempts on that target. In each round, the agent invokes skills (see Section [3.5\)](#page-5-1) and edits the worktree; the driver then runs Verus on the target and checks that the round passes every applicable integrity gate (Figure [1;](#page-5-2) pseudocode in Listing [2\)](#page-16-0). Each gate is a deterministic check computed only from recorded evidence: harness-owned task-start specification and axiom snapshots, the worktree before and after the round, the files the agent edited, and the actions it took. The agent's completion report is not evidence of acceptance. The driver accepts a round only if Verus passes, no non-axiom admits remain (Section [2.1\)](#page-1-1), and every applicable gate passes. A rejected round is recoverable if the driver can restore an allowed worktree state and continue the current attempt. A rejected but recoverable round becomes structured round history for the next agent call. When a recoverable gate fires, the driver restores worktree state at a gate-specific scope: frozen files, frozen specifications, or the full start-of-round snapshot. It marks the round as failed, so verification performed before restoration cannot support completion. The following conditions end the current attempt without acceptance: an integrity violation (a fabricated axiom, an edit to the harness tooling, or a proof-bypass construct), reaching the gate retry limit after repeated failures, a verified contract inconsistency (a machine-checked counterexample shows that the implementation and its contract disagree), a decomposition request, or reaching the budget limit. Throughout, the driver treats every signal from the agent as advisory and re-checks it independently. Each round the agent self-reports an END\_REASON: one of COMPLETE (claims success), LIMIT (budget exhausted), NEEDS\_DECOMP (too complicated without further decomposition), or FALSE\_CONTRACT (an internal specification is false). The driver accepts COMPLETE only when the round's independent evidence passes; otherwise it rejects the label and continues while the attempt budget remains. An unverified FALSE\_CONTRACT becomes NEEDS\_DECOMP for a larger-budget retry, whereas a machine-

![](_page_5_Figure_0.jpeg)

<span id="page-5-2"></span>Figure 1: **The outer loop sweeps the configured targets in order; the inner loop iterates rounds within one attempt.**

verified counterexample ends the attempt as FALSE\_CONTRACT. A later attempt may retry the same target, seeded with per-target failure memory that records declaration-level errors from earlier attempts; a prior NEEDS\_DECOMP earns the retry a larger round and wall-clock budget. When an attempt ends, the driver disposes of its worktree by outcome: an accepted attempt is promoted to seed later work, an integrity-violation rejection is rolled back to the last checkpoint (the most recent round state that passed every gate), and any other exit is left on disk as an unpromoted candidate for analysis.

<span id="page-5-0"></span>**Context budget and auto-reset.** As the driver runs, the session reuses the prompt cache and accumulates context, which, as explained in Section [3.1,](#page-2-0) can create problems. The driver starts each attempt in a fresh session and may reset between rounds after a stall (consecutive short rounds that fill no admits), context bloat (accumulated session context past a token threshold), or proof plateau (no improvement in the progress metric across several rounds), up to a per-target cap. A reset preserves the worktree and round history and does not replenish the attempt's round or wall-clock budget.

**Decomposition.** On a later attempt after NEEDS\_DECOMP, the driver injects guidance to split the target's remaining proof obligations into named lemmas, with a loop-invariant template for iterative obligations. The parallel orchestration design and measurements are in the appendix, Section [E.](#page-20-0)

### <span id="page-5-1"></span>**3.5 The Six Skills**

A raw agent with no harness misjudges its own progress: targets could appear completed to the agent while obligations remain, and existing lemmas might get re-derived or fabricated (Section [3.2\)](#page-3-0). CryptoProver therefore gives the agent six dedicated skill CLIs in three groups. Verification skills check claimed completion, admit accounting exposes remaining obligations, and search avoids redundant or fabricated lemmas. The six skills are: verus\_check, admit\_inventory, search\_semantic, search\_module, search\_macro, and search\_proven. All six share one contract: arguments in, a JSON result out, a trace appended, and an exit code that mirrors the result's okay field. verus\_check is

the source of truth for "did it verify?" admit\_inventory counts non-axiom admits (Section [2.1\)](#page-1-1), with comments and axiom\_\* bodies filtered out so the count cannot be gamed, which turns "the file looks done" into a checkable predicate. The four search skills let the agent find existing lemmas wherever they hide — search\_semantic by meaning, search\_module by home module, search\_macro behind a macro expansion, and search\_proven in an earlier run's record — instead of re-deriving or fabricating them, the failure mode that produces invented axioms. Because every skill uses the same interface, the driver invokes and parses them uniformly.

### <span id="page-6-0"></span>**3.6 The Gate Suite**

The suite of eight gates is the core process-integrity mechanism of the design: each gate counters one untrustworthy success from Section [3.2,](#page-3-0) and the full predicates are in Section [A.](#page-13-0)

admit-count credits a passing Verus run only if it actually removed an obligation. axiomdrift lets the agent use the existing axiom base but fails any round that extends it — the fabrication mode the campaign surfaced at scale (Section [3.1\)](#page-2-0). spec-drift, implemented by the harness-owned spec\_check CLI rather than an agent skill, requires the specification under proof to be exactly what it was at task start, so weakening or deleting the ensures is never a route to an accepted round. sibling-verus re-verifies the target area and every file edited during the round, so a target cannot pass by breaking another module. tooling-drift fails a round that edits the harness, the verifier configuration, or the skills; git-recovery fails a round that reads source code out of version control, because the stripped tree's history still carries the original proof and a proof recovered from history is retrieval, not synthesis. frozen-edit fails a round that touches any file the experiment marks frozen (the trusted library, the specification vocabulary, or a proved sibling). forbidden-construct fails a round that introduces a construct discharging an obligation without a proof, i.e., any bypass the other counters cannot see.

## <span id="page-6-2"></span>**4 Evaluation**

The curve25519-dalek proof-and-spec synthesis run is our main experiment: with executable code, API contracts, and the trusted library fixed, CryptoProver must synthesize all intermediate specifications and proofs. A final transfer experiment asks CryptoProver to synthesize proofs for RustCrypto's previously unverified chacha20 implementation against human-authored RFC 8439 specifications. Throughout the evaluation, we count only non-axiom admits as remaining work. Figure [2](#page-7-0) shows the proof-and-spec synthesis experiment's fixed inputs and requested outputs.

For example, consider a task targeting the Ristretto module of curve25519-dalek. The agent receives the executable compress function, its fixed public API contract, the fixed internal specification vocabulary for Ristretto encodings, and the trusted library. The agent must state and prove the intermediate internal specifications that connect the encoding arithmetic to that contract, so that compress and its fixed callers pass the verification check. Section [F](#page-22-0) lists the supplied and synthesized material for every module in the curve25519-dalek proof-and-spec synthesis experiment.

### <span id="page-6-1"></span>**4.1 The Proof-And-Spec Synthesis Run**

Using claude-fable-5, CryptoProver synthesized every intermediate specification and proof connecting the API contracts of curve25519-dalek's Edwards, Montgomery, Ristretto, and scalar modules to the trusted library in 11.4 hours of elapsed time, with \$466.99 in recorded API cost (Figure [3\)](#page-8-0). A fresh x86-Linux container with the pinned Verus release reported 2,031 checks verified,

![](_page_7_Figure_0.jpeg)

<span id="page-7-0"></span>Figure 2: **The artifact layers of a verified crate.** Shaded layers are human-supplied fixed input; dash-outlined layers are agent-synthesized. *Proof-and-spec synthesis* targets the intermediate internal specifications and proof bodies above the fixed trusted library.

zero errors at the default resource limit; the final tree contained no unresolved proof obligations, no executable-code changes, and exactly 48 axioms, all already present in the trusted library.

During the run, the agent corrected its own false intermediate specification after a machinechecked counterexample while executable code, API contracts, and the trusted library remained fixed.

The agent produced 196 proof functions, compared with 235 in the human reference, using 48.5% as many proof lines; 108 agent proof functions have no reference counterpart, and 147 reference proof functions are absent. The agent proofs are therefore more compact and shorter, while the limited overlap in proof functions shows that the agent reorganized much of the proof architecture. The agent also added auxiliary spec fn definitions for computable mirrors, induction measures, and a loop target; each required a proof connecting it to the fixed specification vocabulary. In Figure [4,](#page-9-0) unfilled outlines count human-reference proof functions, blue bars count agent proof functions, and green segments count functions with the same name and source file; labels report agent/human counts followed by the shared count in parentheses.

To measure what CryptoProver's driver, supplied skills, and gates add, the baseline ran the same model through claude-code on the proof-and-spec synthesis task, under the same stated constraints in a network-sealed container, without any of the three. On the same task, the baseline exited after 7.42 hours at a cost of \$1,117.17, claiming it had completed the task. But an analysis of the output revealed 5 compiler and 2 verification errors remaining. Logs record 5 fetches and 38 history probes, all of which were blocked by the network seal. In its trace in Figure [3,](#page-8-0) the compiler-error spike is the result of subagents merging code into the shared tree and introducing integration errors. Its last completed success checks were module-scoped, which was the wrong scope for confirming overall success, and the session exited while the whole-crate check was still running. The plotted verification counts are lower bounds, as compiler errors prevent the checker from reporting results on the whole crate.

CryptoProver replicated the proof-and-spec synthesis result with opus-4.8, a second model from the same family; a fresh x86-Linux container with the pinned Verus release reported 2,114 checks verified, zero errors. The run took 62.3 hours and recorded \$856.55 in API cost (Section [5.3\)](#page-9-1).

![](_page_8_Figure_0.jpeg)

<span id="page-8-0"></span>Figure 3: Error trajectories on the proof-and-spec synthesis task. The proof-and-spec synthesis runs share one elapsed-time axis: compiler lines connect the initial compiler-error count to the first zero-compiler-error milestone, while verification lines report errors on the whole crate. In the baseline run, the agent did not attempt to verify any targets until over two hours had passed.

Thus, opus-4.8 took 5*.*5× the elapsed time of claude-fable-5. Both models resolved the same hardest obligation by decomposing the proof. Increasing the solver budget did not close the obligation; extracting a closed-form helper and splitting two sublemmas did.

ChaCha20 has verified implementations in other ecosystems [\[14,](#page-11-11) [15\]](#page-12-0), but the RustCrypto implementation we targeted has not been formally verified before. We human-authored and independently validated a formal version of the RFC 8439 specification. Then, using opus-4.8, CryptoProver synthesized the proofs in one round (15 minutes, \$4.14). At acceptance, the whole-crate Verus check reported 13 verified items with no errors at the default solver limit, no proof-position admits, and no specification drift. The verified fork and the sealed reconstruction experiment are public [\[16\]](#page-12-1).

## **5 Discussion**

Given fixed API contracts and a trusted library, CryptoProver authored machine-checked proof interiors for two production cryptographic libraries without changing executable code (Section [4\)](#page-6-2). The generated proof architecture also diverged from the human reference: fixed inputs constrain correctness without prescribing the internal construction (Section [4.1\)](#page-6-1).

CryptoProver uses Verus to check verification conditions and gates to reject changes that weaken the claim, expand the trusted base, or break other modules. An accepted run may therefore differ from the fixed inputs only in the agent-authored interior: acceptance requires the whole crate to re-verify against the unchanged human-written contracts and trusted library. This architecture emphasizes capability and soundness relative to fixed inputs rather than trust in the agent.

The campaign's false successes exposed failures of trust and context discipline rather than limits of prover capability (Section [3.1\)](#page-2-0). We interpret the gates and the fresh-session discipline as making the model's proof capability acceptable by blocking the known cheats. The experiments are existence results rather than estimates of average performance because they are not independent repeated trials. The gate suite bounds only the failure modes it encodes; it does not rule out an unmodeled bypass.

![](_page_9_Figure_0.jpeg)

<span id="page-9-0"></span>Figure 4: Agent and human proof functions by source file.

The campaign's lesson is the one we would carry to other agent-verification systems: rules must be mechanically enforced to be effective. Wherever success is machine-checkable and the known cheats are mechanically gated, an agent-authored artifact can be accepted without trusting the agent's process.

### **5.1 Soundness remains relative to the trusted base**

The logical guarantee comes from Verus (backed by Z3) checking the crate against the humanauthored API contracts and the trusted library. The gate implementations, audit scripts, and container configuration provide process-integrity evidence that the run preserved those inputs and avoided the enumerated routes to false success. That the audits found no violations of the enumerated failure modes means the agent added no trust of its own; it does not mean the result has no trusted assumptions.

### **5.2 Proof quality and autonomy remain open**

Whether the generated proofs remain maintainable as the library evolves is a pressing open question. We, not the agent, supplied the targets and — most importantly — their proof order; letting the agent plan that order from the contracts is immediate future work.

### <span id="page-9-1"></span>**5.3 Threats to validity**

The result is functional correctness against the supplied contracts, not cryptographic security, constant-time execution, side-channel resistance, or contract adequacy. On cost, the 11.4-hour figure measures agent elapsed time after the contracts, the trusted library, the specification vocabulary, the target decomposition, the proof order, and the harness had been supplied, while the eight-month human effort included authoring those inputs, so the two figures are not directly comparable. Within the verified artifact, humans supplied the high-level API contracts and the trusted library, while CryptoProver authored the internal specifications and every proof; we therefore expect a large

reduction in human verification effort, though these figures do not measure it. The same-family opus-4.8 run also completed the verification effort, but at 5*.*5× the headline runtime (Section [G\)](#page-24-0) of the fable-5 run. Finally, the prompts, skills, and gates were tuned on curve25519-dalek, and both subjects were selected favorably — curve25519-dalek for its auditable human reference, chacha20 for its size and RFC 8439 specification — so the results may overstate performance on an unseen crate.

## <span id="page-10-0"></span>**6 Related Work**

The closest Verus systems generally synthesize proofs from supplied specifications or bounded targets: AutoVerus, VeruSAGE, and RagVerus work at function or file granularity, KVerus applies dependency-aware synthesis to real kernel code, and VeriStruct jointly plans specifications and proofs for modules [\[2–](#page-11-1)[5,](#page-11-2) [12\]](#page-11-9). VerusSeek strengthens proof synthesis with fine-grained retrieval of contracts, invariants, lemmas, proof blocks, and assertions, followed by hierarchical context expansion [\[17\]](#page-12-2). CryptoProver instead synthesizes missing cross-file internal specifications and proofs for production libraries from fixed API contracts and a trusted library, with mechanical gates that preserve those fixed inputs.

Research on fallible specifications shows why local proof success is insufficient: generated annotations can be vacuous or false, so acceptance must separately check specification consistency and non-triviality [\[18–](#page-12-3)[21\]](#page-12-4). Verified cryptographic implementations establish the value of end-to-end machine checking [\[22](#page-12-5)[–24\]](#page-12-6), while recent AI pipelines and benchmarks have begun applying proof models to cryptographic code [\[25,](#page-12-7) [26\]](#page-12-8). Neural theorem provers usually receive a fixed external statement [\[27,](#page-12-9) [28\]](#page-13-1); when an agent can also alter specifications or proof assumptions, documented proof gaming makes a passing verifier signal insufficient [\[29,](#page-13-2) [30\]](#page-13-3).

## **7 Conclusion**

Our results show that it is now possible to formally verify widely used cryptographic libraries with a small fraction of the human effort: given API contracts and a trusted library, CryptoProver synthesized curve25519-dalek's internal specifications and proofs in 11.4 hours for \$466.99, whereas the human-led effort spanned eight months. CryptoProver further verified RustCrypto's previously unverified chacha20 implementation. In both cases, no executable code was changed. Verus checking, the complete eight-gate suite, fresh sessions, and sandboxing defend this process against false success and reference-proof retrieval. The verified claim is functional correctness against the supplied contracts, not constant-time execution or side-channel resistance (Section [5.3\)](#page-9-1).

Future work includes applying CryptoProver to additional cryptographic libraries. We also expect the same techniques to largely transfer to other (non-cryptographic) Rust systems, and AI-assisted authoring of the requirement specifications would reduce the last major human task.

## **Acknowledgments**

This work was supported in part by the Defense Advanced Research Projects Agency (DARPA) under contract FA8750-24-2-1001, the Chen Institute, and LMSYS.

## **References**

- <span id="page-11-0"></span>[1] Debian Security Team. *DSA-1571-1: New OpenSSL Packages Fix Predictable Random Number Generator*. Debian Security Advisory. Accessed 2026-07-13. 2008. url: [https : / / lists .](https://lists.debian.org/debian-security-announce/2008/msg00152.html) [debian.org/debian-security-announce/2008/msg00152.html](https://lists.debian.org/debian-security-announce/2008/msg00152.html).
- <span id="page-11-1"></span>[2] Chenyuan Yang, Xuheng Li, Md Rakib Hossain Misu, Jianan Yao, Weidong Cui, Yeyun Gong, Chris Hawblitzel, Shuvendu Lahiri, Jacob R. Lorch, Shuai Lu, Fan Yang, Ziqiao Zhou, and Shan Lu. *AutoVerus: Automated Proof Generation for Rust Code*. OOPSLA 2025. 2024. doi: [10.1145/3763174](https://doi.org/10.1145/3763174). arXiv: [2409.13082](https://arxiv.org/abs/2409.13082).
- [3] Si Cheng Zhong and Xujie Si. *Towards Repository-Level Program Verification with Large Language Models*. LMPL 2025. 2025. arXiv: [2509.25197](https://arxiv.org/abs/2509.25197).
- [4] Yuwei Liu, Xinyi Wan, Yanhao Wang, Minghua Wang, Lin Huang, and Tao Wei. *KVerus: Scalable and Resilient Formal Verification Proof Generation for Rust Code*. 2026. arXiv: [2605.03822](https://arxiv.org/abs/2605.03822).
- <span id="page-11-2"></span>[5] Chuyue Sun, Yican Sun, Daneshvar Amrollahi, Ethan Zhang, Shuvendu Lahiri, Shan Lu, David Dill, and Clark Barrett. *VeriStruct: AI-assisted Automated Verification of Data-Structure Modules in Verus*. 2025. doi: [10.48550/arXiv.2510.25015](https://doi.org/10.48550/arXiv.2510.25015). arXiv: [2510.25015](https://arxiv.org/abs/2510.25015).
- <span id="page-11-3"></span>[6] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. "Verus: Verifying Rust Programs using Linear Ghost Types". In: *Proc. ACM Program. Lang. (OOPSLA)*. 2023. arXiv: [2303.05491](https://arxiv.org/abs/2303.05491).
- <span id="page-11-4"></span>[7] Beneficial AI Foundation. *curve25519-dalek: independent Verus verification fork*. GitHub repository. 2026. url: [https://github.com/Beneficial- AI- Foundation/dalek- lite/](https://github.com/Beneficial-AI-Foundation/dalek-lite/pull/774) [pull/774](https://github.com/Beneficial-AI-Foundation/dalek-lite/pull/774).
- <span id="page-11-5"></span>[8] Signal Messenger, LLC. *libsignal v0.96.3*. GitHub repository. 2026. url: [https://github.](https://github.com/signalapp/libsignal/tree/v0.96.3) [com/signalapp/libsignal/tree/v0.96.3](https://github.com/signalapp/libsignal/tree/v0.96.3).
- <span id="page-11-6"></span>[9] Kara Lee. *All Signals Point Up for App's Downloads and MAUs*. Sensor Tower. Accessed 2026-07-13. 2025. url: [https://sensortower.com/blog/all- signals- point- up- for](https://sensortower.com/blog/all-signals-point-up-for-apps-downloads-and-maus)[apps-downloads-and-maus](https://sensortower.com/blog/all-signals-point-up-for-apps-downloads-and-maus).
- <span id="page-11-7"></span>[10] Shadowsocks Contributors. *shadowsocks-rust*. GitHub repository. 2026. url: [https://github.](https://github.com/shadowsocks/shadowsocks-rust/tree/c88b519) [com/shadowsocks/shadowsocks-rust/tree/c88b519](https://github.com/shadowsocks/shadowsocks-rust/tree/c88b519).
- <span id="page-11-8"></span>[11] Leonardo de Moura and Nikolaj Bjørner. "Z3: An Efficient SMT Solver". In: *Tools and Algorithms for the Construction and Analysis of Systems (TACAS)*. 2008, pp. 337–340.
- <span id="page-11-9"></span>[12] Chenyuan Yang, Natalie Neamtu, Chris Hawblitzel, Jacob R. Lorch, and Shan Lu. *VeruSAGE: A Study of Agent-Based Verification for Rust Systems*. 2025. arXiv: [2512.18436](https://arxiv.org/abs/2512.18436).
- <span id="page-11-10"></span>[13] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. "Lost in the Middle: How Language Models Use Long Contexts". In: *Transactions of the Association for Computational Linguistics* (2024). TACL 2024. arXiv: [2307.03172](https://arxiv.org/abs/2307.03172).
- <span id="page-11-11"></span>[14] Jean Karim Zinzindohoué, Karthikeyan Bhargavan, Jonathan Protzenko, and Benjamin Beurdouche. "HACL\*: A Verified Modern Cryptographic Library". In: *Proc. ACM CCS*. 2017, pp. 1789–1806. doi: [10.1145/3133956.3134043](https://doi.org/10.1145/3133956.3134043).

- <span id="page-12-0"></span>[15] Jonathan Protzenko, Bryan Parno, Aymeric Fromherz, Chris Hawblitzel, Marina Polubelova, Karthikeyan Bhargavan, Benjamin Beurdouche, Joonwon Choi, Antoine Delignat-Lavaud, Cédric Fournet, Natalia Kulatova, Tahina Ramananandro, Aseem Rastogi, Nikhil Swamy, Christoph M. Wintersteiger, and Santiago Zanella-Béguelin. "EverCrypt: A Fast, Verified, Cross-Platform Cryptographic Provider". In: *Proc. IEEE S&P*. 2020, pp. 983–1002. doi: [10.1109/SP40000.2020.00114](https://doi.org/10.1109/SP40000.2020.00114).
- <span id="page-12-1"></span>[16] *chacha20-verus: Verus-Verified Fork of RustCrypto's chacha20*. GitHub repository. 2026. url: <https://github.com/oliversssf2/chacha20-verus>.
- <span id="page-12-2"></span>[17] Yuchen Zhang, Cheng Wen, Zhiwu Xu, Dugang Liu, Jialun Cao, Yuwei Liu, Shengchao Qin, and Cong Tian. "Enhancing LLM-Based Proof Synthesis for Rust Programs via Semantic Chunking and Hierarchical Context Expansion". In: *Theoretical Aspects of Software Engineering*. Springer Nature Switzerland, 2026, pp. 81–100. isbn: 978-3-032-30693-7. doi: [10.1007/978-3-032-](https://doi.org/10.1007/978-3-032-30693-7_6) [30693-7\\_6](https://doi.org/10.1007/978-3-032-30693-7_6).
- <span id="page-12-3"></span>[18] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. "Clover: Closed-Loop Verifiable Code Generation". In: *Proc. iFM*. 2024. arXiv: [2310.17807](https://arxiv.org/abs/2310.17807).
- [19] Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kasriel, Kaiyu Yang, and Dawn Song. *VERINA: Benchmarking Verifiable Code Generation*. 2025. arXiv: [2505.23135](https://arxiv.org/abs/2505.23135).
- [20] Haoze Wu, Clark Barrett, and Nina Narodytska. "Lemur: Integrating Large Language Models in Automated Program Verification". In: *Proc. ICLR*. 2024. arXiv: [2310.04870](https://arxiv.org/abs/2310.04870).
- <span id="page-12-4"></span>[21] Shubham Agarwal, Alexander Krentsel, Shu Liu, Mert Cemri, Audrey Cheng, Rui Meng, Tomas Pfister, Chun-Liang Li, Sylvia Ratnasamy, Aditya Parameswaran, Matei Zaharia, Ion Stoica, and Mohsen Lesani. *Inductive Deductive Synthesis: Enabling AI to Generate Formally Verified Systems*. 2026. arXiv: [2605.23109](https://arxiv.org/abs/2605.23109).
- <span id="page-12-5"></span>[22] Katherine Q. Ye, Matthew Green, Naphat Sanguansin, Lennart Beringer, Adam Petcher, and Andrew W. Appel. "Verified Correctness and Security of mbedTLS HMAC-DRBG". In: *Proc. ACM CCS*. 2017. doi: [10.1145/3133956.3133974](https://doi.org/10.1145/3133956.3133974). arXiv: [1708.08542](https://arxiv.org/abs/1708.08542).
- [23] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, Benjamin Grégoire, Adrien Koutsos, Vincent Laporte, Tiago Oliveira, and Pierre-Yves Strub. *The Last Mile: High-Assurance and High-Speed Cryptographic Implementations*. 2019. doi: [10.48550/arXiv.1904.04606](https://doi.org/10.48550/arXiv.1904.04606). arXiv: [1904.04606](https://arxiv.org/abs/1904.04606).
- <span id="page-12-6"></span>[24] Joel Kuepper, Andres Erbsen, Jason Gross, Owen Conoly, Chuyue Sun, Samuel Tian, David Wu, Adam Chlipala, Chitchanok Chuengsatiansup, Daniel Genkin, Markus Wagner, and Yuval Yarom. *CryptOpt: Verified Compilation with Randomized Program Search for Cryptographic Primitives*. 2023. doi: [10.48550/arXiv.2211.10665](https://doi.org/10.48550/arXiv.2211.10665). arXiv: [2211.10665](https://arxiv.org/abs/2211.10665).
- <span id="page-12-7"></span>[25] Natalia Klaus, Juan Conejero, and Palina Tolmach. *A Rust-to-Lean Verification Pipeline with AI Provers: An Experience Report*. 2026. arXiv: [2605.30106](https://arxiv.org/abs/2605.30106).
- <span id="page-12-8"></span>[26] Max Tan. *Automating Formal Verification with Reinforcement Learning and Recursive Inference*. 2026. arXiv: [2605.30914](https://arxiv.org/abs/2605.30914).
- <span id="page-12-9"></span>[27] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu, Qihao Zhu, et al. *DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition*. 2025. arXiv: [2504.21801](https://arxiv.org/abs/2504.21801).

- <span id="page-13-1"></span>[28] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan Prenger, and Anima Anandkumar. "LeanDojo: Theorem Proving with Retrieval-Augmented Language Models". In: *Proc. NeurIPS Datasets and Benchmarks*. 2023. arXiv: [2306.15626](https://arxiv.org/abs/2306.15626).
- <span id="page-13-2"></span>[29] Pranjal Aggarwal, Bryan Parno, Sean Welleck, et al. *AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement*. 2024. arXiv: [2412.06176](https://arxiv.org/abs/2412.06176).
- <span id="page-13-3"></span>[30] Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian Chiosa, Jure Kukovec, Alok Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, Miranda Zhao, Max Tan, and Max Tegmark. *A benchmark for vericoding: formally verified program synthesis*. 2025. arXiv: [2509.22908](https://arxiv.org/abs/2509.22908).
- <span id="page-13-4"></span>[31] R. L. Graham. "Bounds on Multiprocessing Timing Anomalies". In: *SIAM Journal on Applied Mathematics* 17.2 (1969), pp. 416–429. doi: [10.1137/0117039](https://doi.org/10.1137/0117039).

## <span id="page-13-0"></span>**A Gate Definitions**

This appendix defines each gate formally. Let *S*<sup>0</sup> be the harness-owned snapshot recorded at task start. Each round transforms a pre-round tree *S*pre into a post-round tree *S*post for a target module *t*. Let *Edited* be the files the agent changed and *Cmds* the shell commands it issued during the round. Each gate is a pure predicate over (*S*0*, S*pre*, S*post*, t,Edited, Cmds*) (Section [3.6\)](#page-6-0). The harness accepts the round only if Verus verifies *t* in *S*post and every predicate below holds. Otherwise, the named gate fires and the harness rejects the round. Write *s*[*f*] for the byte content of file *f* in state *s* and ok(*s, f*) for "*f* verifies under Verus in *s*."

**admit-count (vs. false completion).** Let *a*(*s*) be the non-axiom admit count of *t* in *s*: the number of admit() placeholders standing in for unproved goals, excluding trusted axioms. The admit\_inventory command exposes the same counter to the agent. Passes iff *a*(*S*post) *< a*(*S*pre); otherwise, the harness rejects a round that removed no obligation.

**axiom-drift (vs. fabricated axioms).** Let Ax(*s*) be the set of axiom\_\* names in *s*. Passes iff Ax(*S*post) ⊆ Ax(*S*0): the existing trust base may be used but not extended. This predicate detects new axiom names. In the proof-and-spec synthesis and convergence-ladder experiments reported below, axiom files are also frozen, so frozen-edit rejects an in-place statement change.

**spec-drift (vs. spec drift).** Let spec(*s, t*) be *t*'s preconditions and postconditions (its requires/ensures clauses) and its spec-function bodies. Passes iff spec(*S*post*, t*) is byte-identical to spec(*S*0*, t*).

**sibling-verus (vs. cross-module breakage).** Let *Area*(*t*) be *t*'s top-level area module. Passes iff ok(*S*post*, f*) for every *f* ∈ *Edited* ∪ {*Area*(*t*)}: a break in any touched sibling fails the round even when *t* itself verifies.

**tooling-drift (vs. a doctored checker).** Let *Tool* be the harness, verifier configuration, and skill-CLI files. Passes iff *S*post[*f*] = *S*pre[*f*] for every *f* ∈ *Tool* (compared by content hash).

| Run                  | Outcome                                                 | Rounds | Elapsed (h) | Cost (\$) |
|----------------------|---------------------------------------------------------|--------|-------------|-----------|
| sweep_all_001        | 64/72 modules; ~1,090 admits filled                     | 187    | 19.3        | 408       |
| residue_001          | 6/8 retry of sweep failures                             | 34     | 6.0         | 148       |
| montgomery_retry_001 | 3 admits "closed" (later shown fabricated)              | 3      | 0.5         | 14        |
| hard_tail_001        | last 9 honest admits closed                             | 2      | 0.4         | 12        |
| repair_001           | fixed the 5 sibling-broken proofs                       | 3      | 0.2         | 4         |
| repair_002_axioms    | 11 axioms forced as lemmas: 0/11 (10 invalid as stated) | 34     | 0.9         | 15        |
| repair_003_inline    | re-proved all 11 inline, fresh context: 11/11           | 4      | 2.2         | 45        |

<span id="page-14-1"></span>Table 1: The main-sweep and repair runs that the campaign audit and repair turn on.

**git-recovery (vs. answer recovery from history).** Passes iff no command in *Cmds* matches one of the following source-reading forms: git show, git checkout <ref> – <file>, git log -p, git diff against HEAD, git cat-file, git stash show -p, or git worktree add. In the proof-and-spec synthesis run, the original proof bodies were absent from the machine, so there was nothing for these commands to recover; the gate provided an additional safeguard (Section [3\)](#page-2-1).

**frozen-edit (vs. out-of-scope edits).** Let *Frozen* be the files the experiment marks frozen (substrate lemmas, spec vocabulary, proved siblings). Passes iff *Edited* ∩ *Frozen* = ∅.

**forbidden-construct (vs. proof-free discharge).** Let *c*(*s*) count assume(...) and #[verifier:: external\_body] occurrences across the editable files. Passes iff *c*(*S*post) ≤ *c*(*S*pre): such a construct discharges an obligation without a proof checked by the SMT solver (Verus's underlying automated prover) and leaves neither an admit() nor a new axiom\_\* for the other counters to catch.

**Reads of task-start state.** Only spec-drift and axiom-drift consult state from outside the round: both compare the post-round tree against the harness-owned task-start snapshot *S*0. The harness creates this snapshot before the agent begins the task and keeps it outside the agent's control, so the agent cannot pass either gate by editing both sides at once.

**Gate routing in the driver.** Listing [2](#page-16-0) shows where the gate suite sits in the per-target round loop and how firings route through claim checking, retry, terminal rejection, and post-loop promotion. The driver's outer loop enters this per-target round loop once for each configured target, in supplied order.

## <span id="page-14-0"></span>**B Campaign Per-Run Ledger**

This appendix records the motivating campaign of Section [3.1](#page-2-0) run by run. Table [1](#page-14-1) breaks out the runs that the campaign audit and repair turn on. All numbers are aggregated from the per-target result.json records in our supplementary campaign artifact: the claude\_usage cost and token fields, duration\_seconds, and rounds\_used. A fourth repair run was an aborted false-success attempt whose rounds, hours, and cost are folded into the repair\_002\_axioms row. The full 152-target ledger, with per-round diffs and spec snapshots, lives in that artifact. Raw session transcripts are withheld from the review copy and released with the camera-ready artifact. The audit (audit\_001) was a separate non-proving verification pass and is not counted as a run.

The eleven fabricated axioms share one shape: each constrains an output parameter in its ensures without relating that parameter to the inputs in its requires, so invoking the lemma supplies the conclusion without proof. All eleven are asserted without proof; ten are moreover invalid the claimed property fails for some inputs — while the eleventh is true as stated. The eleventh, lemma\_batch\_loop\_iteration\_correct, is a Ristretto batch-loop property with no counterpart in the reference proof, but it was not proved as a standalone lemma. The extreme case applies lemma\_ristretto\_compress\_correct to point and s\_bytes. It states no requires at all and claims that arbitrary bytes equal the compression of an arbitrary point. Four of the eleven cover the Montgomery ladder (differential add-and-double, conversion to Edwards form, basepoint-on-curve, Elligator encoding), one a 27-step scalar inversion chain, and six the Ristretto compress, decode, Elligator, and batch paths. The three admits montgomery\_retry\_001 "closed" were all discharged by inventing such axioms in a sibling file and calling them. repair\_003\_inline later proved the intended properties behind all eleven fabricated axioms from scratch, with no access to the reference proof, for \$45. Each property was restated inline with its outputs bound to its inputs. The final whole-crate state was 2,505 verified, zero errors, and 41 trusted axioms.

```
1 # The outer loop enters here once per target , in configured order .
2 for round in 1..= max_rounds : # within wall - clock deadline
3 prompt = render ( template , failure_memory , last_errors )
4 if round == 1 or stalled () or bloated () : # context budget :
5 agent = fresh_session () # else continue -c , cache reuse
6 stream ( agent , prompt ) # agent edits the worktree , runs skills
7 result = run_verus ( target )
8 gates = run_gates ( target , result ) # admit - count , axiom - drift , spec - drift ,
9 # sibling - verus , tooling - drift ,
10 # git - recovery , frozen - edit ,
11 # forbidden - construct
12 record ( round , result , gates )
13 if gates . hard_cheat () : # axiom - drift / tooling - drift /
14 # forbidden - construct :
15 return gates . cheat_label # terminal on first firing
16 if gates . recoverable_fired () : # spec - drift / frozen - edit / git - recovery :
17 restore_frozen_state () # restore , taint the round , instruct
18 continue # the agent ; past a cap -> terminal
19 if claimed ( COMPLETE ) : # the agent claims ; the harness checks :
20 if result . ok and admits_left ( target ) == 0:
21 return COMPLETE # passing , zero non - axiom admits ,
              gates clean
22 reject_claim_with_reason () # claim refused ; agent told why
23 if claimed ( FALSE_CONTRACT ) : # a frozen contract is false :
24 return FALSE_CONTRACT if witness_verified () else NEEDS_DECOMP
25 # the witness is machine - checked ;
26 # unverified -> escalation only
27 if claimed ( NEEDS_DECOMP ) : # escalate , not a dead end : a fresh
28 return NEEDS_DECOMP # retry resumes with a larger budget
29 # (+2 rounds , 1.5 x wall - clock ) + a
30 # " build the missing
31 # infrastructure first " directive
32 round_history . append ( target , result . errors , gates ) # non - fatal : loop back
33 return final_label ( rounds ) # post - loop evidence check : a tree meeting
34 # the completion criteria promotes to
35 # COMPLETE even unclaimed ; a tainted or
36 # unverified last round never does ; else
                                  LIMIT
37 # exit disposition , on every return above : a cheat - class label rolls the
38 # worktree back to the last integrity - clean snapshot ; a non - COMPLETE label
39 # feeds persistent failure memory ( unless its trace is tainted ) ; only
40 # COMPLETE is promoted -- any other final state stays on disk , unpromoted
```

Listing 2: Per-target driver pseudocode: Verus and *all* gates must pass.

## <span id="page-17-0"></span>**C Whole-Crate Proof-Only Run**

This appendix reports the whole-crate proof-only run under two conditions: *no-hints*, with all comments removed before the run, and *with-hints*, with source doc-comments retained. In the no-hints condition, CryptoProver uses claude-opus-4-8 to discharge (prove) 1,430 of 1,433 proof obligations, each marked by a source-level admit() placeholder, including obligations left open by the reference proof, at a recorded API cost of \$748.02. For both conditions, admit.py replaces proof bodies with admit() while preserving signatures, contracts, and executable code. Success requires no new axioms or specification changes and a successful whole-crate Verus check; the reference measures coverage, while Verus establishes correctness.

Prior Verus proof-completion evaluations score standalone function- or file-level targets with supplied specifications (Section [6\)](#page-10-0). This run instead spans a shared production-crate dependency graph, including proof obligations inside the trusted library (the fixed, human-supplied field specifications, arithmetic facts, trusted axioms, and vstd), and accepts the run only when the final tree passes whole-crate verification. Its coverage therefore measures integrated proof completion rather than a directly comparable per-task success rate. Across this broad scope, the no-hints run leaves 3 particularly difficult obligations incomplete. They lie in the deep Ristretto/Lizard curve-algebra core. The reference leaves 8 obligations open under the same executable code and specifications, including these 3 obligations. The final tree passes a whole-crate Verus check with trusted axioms and specifications unchanged. Only gate-verified closures are credited; rejected attempts are excluded. Most obligations close during a steady initial pass over the crate (the main sweep), where the median admit closes in 1.1 minutes of proving. A later retry phase at the hard frontier spends 30–60 minutes per remaining admit but adds little, leaving the gaps (Figure [5\)](#page-18-0). Here, active proving time is the sum of module-run durations, including failed attempts but excluding idle gaps between runs. The verifier (compile, encode, and solve) accounts for 19% of active proving time and the agent, including generation and harness overhead, for 81%. We estimate time per removed admit from module-level runtimes because individual proof obligations were not timed separately. The recorded traces also do not distinguish agent reasoning time from code-generation time. Across its three runs at \$730 total over 154 rounds, the with-hints condition reached the same 3-gap residual as the no-hints run. In these runs, retaining the doc-comment hints did not change the observed set of remaining obligations. The shared residual obligations mark a solver frontier rather than a demonstrated impossibility: the same nonlinear field algebra remains open in the reference proof. As an axiom-gate ablation, the campaign's prompt-only configuration (Section [3.1\)](#page-2-0) allowed 11 fabricated axioms.

![](_page_18_Figure_0.jpeg)

<span id="page-18-0"></span>Figure 5: No-hints run dynamics: (a) minutes of proving per closed admit; (b) cumulative admits closed against active proving time, idle and rate-limit gaps removed; (c) the verifier's share of active proving time. All 1,429 gate-verified closures are shown; rejected attempts are excluded.

## **D Proof Style: Human vs. Agent**

This appendix compares the proof *style* of the human reference proof and the agent's no-hints run (Section [C\)](#page-17-0) under the same frozen contracts and spec-function bodies. A tree-to-tree contractequivalence pass compares clause text, after removing comments, across all 118 .rs files under curve25519-dalek/src, each present in both trees. It finds zero changed requires/ensures clauses and zero redefined spec-function bodies. The no-hints tree therefore verifies against the same frozen contracts and spec-function bodies as the fork-point human tree (the verified reference tree from which the experiment branched). Table [2](#page-19-0) measures how each tree constructs proofs against that shared specification, aggregated over every proof fn body and inline proof {} block in each tree. rlimit raises the solver's per-query resource budget; decreases declares a termination measure. The comment-line row measures the final artifacts; the remaining lexical metrics use a comment-stripped code view so comments and string literals do not inflate their counts. The no-hints start tree contained no comments, but the run predates command logging, so the provenance of comments in its final artifact is not independently established. Three patterns dominate. The agent decomposes more finely, using more helper proof fns in less total proof code. On the 813 lemmas present in both trees, the agent version is shorter at the median: 12 vs 17 proof lines. Where the human typically justifies an assertion by calling a lemma inside that assertion's assert(..) by { lemma() } block, the agent instead calls lemmas sequentially and follows them with a bare assert, using about half as many by {} blocks. It also leans on solver automation where the human reasons equationally: by (nonlinear\_arith) use rises sharply, while the agent's proofs contain almost no calc blocks and far fewer reveal statements.

| Metric               | Human  | No-hints | NH/H |
|----------------------|--------|----------|------|
| proof fn count       | 813    | 1,018    | 1.25 |
| proof LOC            | 33,502 | 27,993   | 0.84 |
| assert               | 8,127  | 9,280    | 1.14 |
| assert<br>by {}      | 4,550  | 2,244    | 0.49 |
| lemma calls          | 7,458  | 6,691    | 0.90 |
| broadcast use        | 30     | 13       | 0.43 |
| forall               | 168    | 292      | 1.74 |
| calc                 | 32     | 1        | 0.03 |
| by (nonlinear_arith) | 92     | 409      | 4.45 |
| by (bit_vector)      | 337    | 310      | 0.92 |
| reveal               | 203    | 61       | 0.30 |
| rlimit attributes    | 5      | 9        | 1.80 |
| decreases            | 179    | 188      | 1.05 |
| comment lines        | 6,154  | 5,340    | 0.87 |

<span id="page-19-0"></span>Table 2: Proof-style metrics for the fork-point human proof and the no-hints run under the same frozen contracts and spec-function bodies. Ratios are agent over human.

**Caveat: proof length and automation are not quality metrics.** Lower proof LOC and heavier automation are trades, not wins. The reference proof in montgomery\_reduce\_part1\_ chain\_lemmas.rs shows why. It uses a deliberately long multiplication ladder of small, scoped assert .. by {} steps and no nonlinear\_arith calls. The no-hints proof instead calls nonlinear\_arith repeatedly. In the reference file, the ladder reduces solver-resource demand and localizes failures. Because nonlinear integer arithmetic is undecidable, nonlinear\_arith uses heuristic search that can exhaust the resource limit on a large goal. The ladder instead gives the solver a sequence of local facts: distribute one limb, normalize by commutativity, and extend the prefix. Explicit lemma calls can also supply the concrete instantiations of universally quantified facts instead of leaving the solver to search for them. A failing scoped assert identifies the broken algebraic step; when a large nonlinear query exhausts the resource limit, its diagnostic does not identify that step. The agent's near absence of calc chains and reveal statements also reduces readability. An equational calc block spells out each algebraic step, whereas a bare nonlinear\_arith call leaves the reader to reconstruct why the goal holds. The agent proofs as shipped do verify. The codebase-wide analysis shows that the agent proofs are shorter and rely more heavily on solver automation. The Montgomery example illustrates the resulting tradeoffs: greater solver-resource demands, less informative failures, and reasoning that is harder to follow (Table [3\)](#page-20-1).

| Aspect                     | Human reference                                     | Agent (no-hints)                                         |
|----------------------------|-----------------------------------------------------|----------------------------------------------------------|
| Reasoning<br>Decomposition | equational (calc, reveal)<br>coarser, longer bodies | solver-driven (nonlinear_arith)<br>finer, shorter bodies |
| Point-of-use               | assert<br>by { lemma() }                            | sequential lemma calls, then a bare<br>assert            |
| Stability                  | small scoped steps                                  | large nonlinear goals can be fragile                     |
| Solver budget              | smaller local queries                               | a large query can exhaust rlimit                         |
| Debuggability              | a scoped failure identifies the broken<br>step      | a resource-limit failure may not<br>identify the step    |
| Readability                | explicit algebraic chain                            | solver call hides the algebraic steps                    |

<span id="page-20-1"></span>Table 3: Codebase-wide proof-style contrasts (first three rows) and Montgomery-specific tradeoffs (remaining rows).

## <span id="page-20-0"></span>**E Parallel Orchestration Details**

This appendix presents the design and measurements of the parallel orchestration layer.

### <span id="page-20-2"></span>**E.1 Design**

A proof-synthesis run over a real Rust codebase comprises hundreds of proof obligations. The driver groups these obligations into module-level targets (Section [3.4\)](#page-4-0); the orchestrator schedules each target as one job. Sequentially, the run's elapsed time is the sum of the per-job times. A single job's time splits into two parts: *agent latency* (waiting on the model) and *verifier work* (cargo verus and Z3 checking the edits). The first dominates: each job is mostly blocked on the model, while the verifier runs only in short, intermittent CPU bursts. The workload therefore parallelizes well: while one job blocks on the model, another can use the CPU. During local proof checking, Verus checks a called lemma against its signature, so bodies can be attempted in parallel ("Why Fan-Out Works" below). These attempts are speculative: a target can verify while lemmas it calls remain admitted, and the collected tree is accepted only after post-merge and whole-crate checks. We therefore design an orchestration layer in CryptoProver with three properties. The layer is *thin*: a wrapper over the unmodified driver suffices, with no coordinator or message layer. It is *fully isolated*: naive fan-out on a single checkout is unsafe, as concurrent jobs contend on the build tree and shared state, so each worker process gets its own git worktree and results root. It is *self-balancing*: a dynamic ready-queue with longest-processing-time ordering and file decomposition keeps worker processes saturated. The layer reaches 3*.*21× at four-way parallelism, cutting a 74-minute workload to 23 minutes.

#### **E.1.1 Why Fan-Out Works: Proof Bodies Can Be Attempted Independently**

Proof-completion targets are far more independent than their call structure suggests. A lemma-call graph appears sequential because lemma *A*'s proof calls *B*. During local proof checking, however, Verus checks *A* against *B*'s signature, including its ensures, even while *B* remains admit(). Three consequences follow. There is no runtime propagation: each worker process proves against its own admitted copies, and proving *B* later requires no change to *A*. "Done" is a global condition — zero non-axiom admit() across the collected tree — not a proving order. Shared helper edits introduce merge-time coupling because two jobs may both append new helper lemmas to the same lemmas/ file. Whole-crate analyses can also reintroduce coupling, chiefly through termination checking, which requires recursive call chains to decrease a measure ("Acceptance after Recombination" below). Tasks that synthesize specifications introduce dependencies not present when the agent fills proof bodies against fixed specifications. File decomposition likewise makes every worker process edit the same large file. For a proof-completion task over a well-specified codebase with local, sparse shared helpers, these couplings are sparse enough for wide fan-out to generate candidate proofs; the post-merge whole-crate gate determines whether their combination is accepted.

#### **E.1.2 Scheduling and Straggler Mitigation**

The orchestrator is a deterministic Python wrapper that maintains a work queue and a pool of free worker processes. It resets each worker process before reuse and fills a free slot as soon as the next job is ready. This dynamic queue lets a short job use a freed worker process while a long job is still running. Even so, bounded fan-out cannot beat makespan ≥ max*i*(time*i*): the run is no faster than its single longest job. Scheduling determines whether that job runs concurrently with the others or starts late and extends the total elapsed time. Two techniques reduce this straggler effect; we describe the cheaper one first.

**Longest-processing-time (LPT) queue ordering.** The runner sorts the queue by a difficulty proxy: descending non-axiom admit() count per job. This ordering dispatches known-heavy jobs in the first wave, so they run concurrently with the other jobs rather than finishing after the other worker processes become idle. This is LPT list scheduling (≈4*/*3-optimal for makespan) [\[31\]](#page-13-4) and costs only a sort.

**File decomposition.** When a *single file* dominates the makespan, LPT ordering cannot help because the file is one job. The signature argument above still makes its proof bodies independently attemptable. Each admit()-bearing proof fn can verify against the other functions' admitted signatures in a separate worktree before recombination. The runner LPT-packs the functions, weighted by admit count, into *K* groups, approximately the number of worker processes. It proves each group in the *same* admitted file and scopes the completion gate to the assigned functions through the driver's –only-fns flag. The remaining functions stay admitted and supply their ensures. The runner then splices each proven body back into one file and unions the helper lemmas introduced by every group. It three-way merges only the small additive import header because a whole-file merge would scatter conflicting hunks. The merged file is then re-verified once with a module-scoped Verus gate ("Acceptance after Recombination" below).

#### **E.1.3 Acceptance after Recombination**

A file is reported proved only if Verus verifies it after recombination. The independence argument of "Why Fan-Out Works" holds for types and specifications but not for Verus's whole-crate analyses. In particular, lemmas that verify in isolation can form a recursion cycle after their bodies are spliced together, causing the combined tree to fail termination checking. A per-group "complete" label is therefore not evidence that the whole file is proved. The runner therefore accepts a decomposition only when a post-merge, module-scoped Verus check re-verifies the entire recombined file on a clean worktree with zero non-axiom admits. Section [E.2](#page-22-1) reports one recombined file this check rejected. The module-scoped check is a filter, not the final authority: acceptance of the collected tree still requires the whole-crate Verus check, which alone covers crate-level analyses. Stronglyconnected-component-aware grouping, sourcing each group's last verifier-clean round, and carrying

<span id="page-22-2"></span>Table 4: Like-for-like speedup across orchestration configurations, each measured once. The speedup ceiling is *N*. Speedups are computed from unrounded durations, so the last digit can differ from the quotient of the rounded columns.

| Configuration                  | Scheduling          | N | Jobs | Seq. sum | Makespan | Speedup |
|--------------------------------|---------------------|---|------|----------|----------|---------|
| Two identical synthetic jobs   | static assignment   | 2 | 2    | 411 s    | 251 s    | 1.64×   |
| Synthetic pool test            | dynamic ready-queue | 2 | 3    | 1002 s   | 557 s    | 1.80×   |
| Eight real modules             | dynamic, per-round  | 4 | 8    | 261 min  | 109 min  | 2.40×   |
| Decomposed file + mixed (real) | LPT + decomposition | 4 | 5    | 74 min   | 23 min   | 3.21×   |

newly introduced helper lemmas across the splice improve the chance that recombination succeeds on the first attempt.

### <span id="page-22-1"></span>**E.2 Measured Speedup**

We measured speedup across four configurations, each adding scale or machinery to the last and each measured once. Because the workload is API-bound, the relevant figure is the *like-for-like* speedup: the sum of the participating jobs' own durations (the sequential cost of the same work) divided by the parallel makespan. Table [4](#page-22-2) summarizes the measurements.

**Observed speedup and scheduling effects.** No configuration triggered API rate-limiting. The two-identical-job configuration reached 1*.*64×; the jobs' per-round times (162/249 s) bracketed the solo time (216 s). The sub-2× result is consistent with a straggler from model nondeterminism, but one measurement cannot separate that explanation from other causes. The dynamic ready-queue reached 1*.*80×, and a freed slot refilled within 0.05 s via reset-before-reuse. In the eight-module measurement, a plain queue reached 2*.*40×; the heaviest module (23 admits) sat last in the input and formed the observed tail. Adding LPT ordering and splitting that heavy file into three parallel groups reached 3*.*21× on the final configuration, cutting 74 minutes to 23. The remaining gap to 4× is consistent with load imbalance and decomposition overhead, but the single measurement does not isolate their contributions.

**One decomposed file failed after recombination.** Splitting batch\_compress\_lemmas (23 lemmas) 4 ways proved 11 of 23 independently. The merged file nevertheless failed the post-merge Verus gate. The spliced-in bodies formed a recursion cycle lacking the decreases clause required by the combined call graph (the termination coupling described under "Acceptance after Recombination", Section [E.1\)](#page-20-2). The gate rejected the recombined file rather than reporting a false success. Independently verified groups therefore do not establish termination of the combined tree. The recombined file must pass its post-merge module-scoped check. Final acceptance still requires the whole-crate check.

## <span id="page-22-0"></span>**F Module Placement and Manifest Detail**

This appendix expands Figure [2'](#page-7-0)s given/synthesized summary into a per-module placement map and the detail of each *manifest*. A manifest is the per-experiment file that defines the experiment's cut: the specification and proof material removed for regeneration. For each module, the manifest records whether the transform keeps it editable, deletes its lemmas, strips its proof bodies, or freezes it. Figure [6](#page-23-0) shows the start and audited end states of the proof-and-spec synthesis run at that

![](_page_23_Figure_0.jpeg)

<span id="page-23-0"></span>Figure 6: Start and audited end states of the proof-and-spec synthesis run.

granularity. The audit accepts only a whole-crate Verus success whose gates confirm that the fixed inputs shown in Figure [6](#page-23-0) are unchanged.

**Module placement.** The rows of Figure [6](#page-23-0) group modules by the material a manifest can remove from them; they are not a complete module hierarchy. The public-API row contains caller-facing modules whose public contracts are the fixed boundary: edwards.rs, montgomery.rs, ristretto.rs, and scalar.rs. API-adjacent glue such as traits.rs and window.rs lives on the same public-facing surface when a manifest strips proof bodies from those files. The curve/scalar row contains the helper-lemma material for the modules above the trusted library: the edwards, ristretto, scalar, and scalar-byte lemma directories under lemmas/\*\*. It also includes multiscalar and scalar-multiplication proof code, plus the curve-model, Montgomery, Jacobi-quartic, Ristretto, and Lizard obligations that consume those facts.

The field/common row contains the field arithmetic proof layer and reusable arithmetic substrate: lemmas/field\_lemmas/\*\* and lemmas/common\_lemmas/\*\* (the number-theory, pow, div–mod, mask, bit, shift, multiplication, sum, and to\_nat helper lemmas). The backend/trusted row contains the backend field/scalar implementations, vstd, and the trusted axiom\_\* lemmas.

Specification material crosses all rows: specs/\*\* and spec functions embedded in API or lemma modules are spec material, while public requires/ensures clauses on caller-facing functions are contract material.

Executable Rust code is frozen in every experiment discussed here; when a manifest lists an executable module with strip-all, the transform removes proof-only bodies inside that module, never executable bodies. Removing a proof body and deleting a helper lemma together with its statement differ only in which text the transform removes. The distinction is operational, not a conceptual layering of the crate. The trusted library is the fixed collection defined in Section [2.2:](#page-2-2) field specifications, field/common arithmetic facts, trusted axiom\_\* lemmas, and vstd. A manifest chooses the editable region outside the trusted library; the common-arithmetic files are part of that library in every run discussed here, and a field-arithmetic repair run could instead make the field layer itself the target.

**Scope comparison.** The whole-crate proof-only run of Section [C](#page-17-0) removes proof bodies crate-wide and nothing else. The proof-and-spec synthesis run of Section [4.1](#page-6-1) removes proof bodies, helper lemmas, and internal specifications from the Edwards/Montgomery/Ristretto/scalar region named

![](_page_24_Figure_0.jpeg)

<span id="page-24-1"></span>Figure 7: Share of elapsed time spent in the verifier for the proof-and-spec synthesis comparison.

above, while contracts and the trusted library stay fixed.

## <span id="page-24-0"></span>**G Proof-and-Spec Synthesis Family: Run Detail**

This appendix carries the run-level detail behind Section [4.1:](#page-6-1) the run protocol, verifier use, run dynamics and repairs, and the recorded integrity events. The *convergence ladder* split the proofand-spec synthesis run's editable region into per-file targets and accepted each target only after its audit, before final whole-crate acceptance. The artifact's ladder record calls an accepted target a *bank* and the final acceptance the *seal*.

In an earlier, smaller pilot that left both API files editable, the post-run audit found the API contracts byte-identical to the reference; the spec-drift and git-recovery gates, not agent restraint, held that boundary.

### **G.1 Run Protocol**

**Prompt and feedback.** The fixed prompt included general guidance about ordering, contract construction, decomposition, and scale; the decomposition guidance reflected the codebase's proof style. The prompt contained no proof content, lemma names, inventories, or target-specific ordering. Per-round feedback contained only verifier errors and the agent's current admit inventory. The editable files nevertheless retained roughly 5,800 lines of comments inherited from the verified source. A start-state content audit found mostly module headers, section dividers, and specification documentation of the encoding layout, plus three proof-strategy comments inherited from the human reference. Stopping rules and the success predicate were the driver's (Listing [2\)](#page-16-0). The pre-registered protocol allowed multiple attempts with a 480-minute wall-clock budget per attempt.

### **G.2 Verifier Use**

**Verifier utilization.** Colored bars in Figure [7](#page-24-1) show active elapsed time with at least one whole cargo verus call in flight; gray shows the remaining agent and orchestration time. Because CryptoProver runs verifier calls sequentially, its colored share also equals total verifier-call time divided by elapsed time. Claude Code alone launched verifier calls from the main thread and subagents, sometimes concurrently. The bar counts overlapping calls once, while the annotation adds the duration of every call and reports the total in verifier-hours. Inferred start times make the Claude Code measurements slight upper bounds. These descriptive measurements do not explain completion or isolate the effect of any driver, skill, or gate.

**Solver attributes at acceptance.** The proof-and-spec synthesis run's final tree contains solver limits larger than the largest limit used by the human reference. At final whole-crate acceptance, targeted single-attribute-removal checks identified one raised limit that could not be removed: scalar:: non\_adjacent\_form at rlimit(150). Every other limit above the human reference's maximum was individually droppable under its module check. The claude-opus-4-8 replication completed the same task in 62.3 hours of elapsed time at \$856.55 in recorded API cost, versus 11.4 hours for the claude-fable-5 run. In that replication, 2 of 13 solver-limit sites remained necessary when each raised attribute was removed individually and the affected module was re-verified. The generated Montgomery proofs also call the pre-existing trusted-library helper lemma\_u128\_shl\_is\_mul, whose assume(false) body is documented as pending vstd support. The run introduced no new assumptions, and the reference proof calls the same helper.

### **G.3 Run Dynamics and Repairs**

**Agent-generated internal-specification repair.** Under an early policy that froze agentgenerated internal specifications between rounds, the continuation run corefloor\_006, which resumed an earlier attempt from its saved state, stopped with 47 non-axiom admit() open. At least two obligations were unprovable because the agent had generated false internal specifications. The machine-checked counterexample *x* = 0, *y* = *p* + 1 falsifies one Ristretto statement: the input violates its postcondition because the precondition lacks a canonicality requirement. The revised policy allowed the agent to correct agent-generated internal specifications while executable code, API contracts, and the trusted library remained fixed. For lemma\_carry8\_bound, the counterexample carry8 = 2<sup>53</sup> + 13 led the agent to replace the too-weak precondition l4 *<* 2 <sup>52</sup> with the call-site fact l4 = 2<sup>44</sup> and complete the proof.

**Frozen-caller references supplied the early proof order.** Figure [3](#page-8-0) traces the run's descent from the first measured whole-crate state to final whole-crate acceptance across both attempts. The evolution record shows two phases. A scaffold phase first declared the missing lemmas that frozen callers reference, each with its proof deferred as a *scaffold admit*. The first hour's edit order followed the concentration of frozen-caller references, supplying a dependency order absent from the generic prompt. A bottom-up discharge phase then discharged the scaffold admits to zero. The verifier accepted the agent's weakened version of a too-strong generated contract and its explicit witnesses for solver repairs. The agent also inserted an exploratory ghost-construction probe and removed it before final whole-crate acceptance.

**Decomposition closed the target after higher solver limits timed out.** The agent first tried a monolithic step lemma at rlimit(600) and then at rlimit(900); two checks in a row hit the verifier's wall-clock ceiling without returning a verdict. It then extracted a closed-form helper lemma, split the two offending sublemmas, and reduced the surviving budget attributes to rlimit(300). The split lemmas verified within the round. This was a structural decomposition of the kind the reference also uses, reached with no reference proof visible.

**The run encountered four classes of solver goals.** Verus calls these logical goals *verification conditions*. Type-invariant construction was the only class that prompted an exploratory proof attempt. Loop invariants closed structurally without budget attributes. Preconditions about numeric bounds were numerous but mechanically discharged by weakening each intermediate bound and summing the results. Termination produced no failures in either the convergence-ladder or proof-and-spec synthesis run.

**A verifier crash understated the remaining errors.** During a later resume of the same continuation, peel\_corefloor\_006\_resume14, a well-typed array\_view call panicked under the pinned

| False-success threat                         | Countermeasure                         | Recorded outcome                                     |
|----------------------------------------------|----------------------------------------|------------------------------------------------------|
| COMPLETE echoed in the agent stream          | score only the harness result          | echoed claims never<br>accepted                      |
| module verifies but the crate is unchecked   | whole-crate verify at default rlimit   | mid-run module successes<br>refused                  |
| a compile failure hides the true error count | settled final state, not series minima | transient two-error states<br>refused                |
| zero errors with admits still open           | crate-wide non-axiom admits = 0        | 43 scaffold admits held to<br>discharge              |
| edit to a frozen witness file                | frozen-edit<br>gate                    | one contaminated success<br>reverted and re-accepted |
| stale text in a rendered prompt              | rendered-prompt preflight audit        | one LIMIT traced, fixed,<br>and accepted             |

<span id="page-26-0"></span>Table 5: False-success threats, countermeasures, and recorded outcomes.

Verus release in the interpreter for Verus's intermediate representation (VIR) when its array remained symbolic. The reproduced cases covered both symbolic parameters and symbolic field projections. The panic terminated verification before the final summary, so preliminary diagnostics could not establish the remaining error count. The verus\_check tool now marks missing-summary runs as truncated, sets the authoritative error count to unknown, and excludes those runs from plateau decisions. A narrow repair to the pinned verifier implements the interpreter's documented fallback: it preserves a simplified residual array\_view call for symbolic inputs while leaving concretearray reduction unchanged. The patched verifier passed a validation run over the campaign's fully verified crate; this validation was separate from the acceptances reported in this paper, which used the unmodified pinned release. Subsequent campaign stability is not a direct regression result for this defect: the observed proofs used scalarized values or a concrete local array, not a symbolic array parameter or field projection. Unsupported symbolic operations can still terminate during elaboration before the final summary. The repair therefore removes this internal panic but does not make preliminary diagnostic counts complete, and the harness continues to treat missing-summary runs as indeterminate. The observed failures aborted before acceptance. They exposed a verifier crash and incomplete diagnostics but did not produce an unsound accepted tree.

### **G.4 Recorded Integrity Events**

**The convergence ladder's audit record.** Table [5](#page-26-0) lists each false-success threat, its countermeasure, and the outcome observed in the recorded runs. Every catch occurred before any per-file acceptance was recorded, and all 27 accepted targets then survived independent fresh-container re-verification, with zero false successes and zero retractions. For example, frozen-edit rejected a whole-crate verification success after the agent edited a frozen backend witness; the harness reverted the edit, and the same agent produced a tree that passed the final check in the next round. Separately, a preflight audit traced a LIMIT to stale text in one target's rendered prompt; after the prompt defect was corrected, that target was accepted.

**The gates rejected two prohibited edits in early setups.** In the early setups that never finished the task, the gates rejected a weakened specification and an edited verifier. The records of the later, successful runs contain no corresponding gate events. Other conditions also changed between these setups, so the contrast is observational.