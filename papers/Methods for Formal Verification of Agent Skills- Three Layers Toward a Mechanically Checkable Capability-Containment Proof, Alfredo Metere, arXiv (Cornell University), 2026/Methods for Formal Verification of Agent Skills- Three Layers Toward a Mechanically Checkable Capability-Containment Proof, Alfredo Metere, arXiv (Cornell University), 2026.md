                                              Methods for Formal Verification of Agent Skills:
                                              Three Layers Toward a Mechanically Checkable
                                                      Capability-Containment Proof
                                                                                Alfredo Metere
                                                                            Metere Consulting, LLC
                                                                     alfredo.metere@metereconsulting.com
arXiv:2605.23951v1 [cs.AI] 9 May 2026




                                                                                       May 26, 2026

                                                                                           Abstract
                                             The companion paper [29] introduced a four-level verification lattice on agent-skill manifests —
                                             unverified, declared, tested, formal — and explicitly left the top level aspirational: “a
                                             formal analysis tool has produced a machine-checkable proof that the skill’s behavior is a subset
                                             of its declared capability set under the runtime’s threat model”. This paper closes that gap. We
                                             give a precise semantics for “a skill’s behavior” that is faithful to how a skill is actually consumed
                                             by a large language model (LLM)-driven runtime (a deterministic script-side reachable through a
                                             non-deterministic LLM-side), state the verification problem as a containment property over that
                                             semantics, and present three composable methods that together raise a skill from declared
                                             or tested to formal: (1) sound static capability-containment analysis of the script-side via
                                             abstract interpretation over a small effect lattice; (2) a refinement type system for tool-call
                                             envelopes that mechanically rejects any call whose statically-inferred capability is not in M.caps;
                                             (3) satisfiability-modulo-theories (SMT)-bounded model checking against the parent paper’s
                                             biconditional correctness criterion, with the bound chosen so that any counter-example the
                                             LLM-side could realise within the runtime’s transaction-buffer horizon is exhibited as a concrete
                                             trace. We characterise what each layer is sound for, what each is incomplete for, and prove that
                                             the three layers composed soundly cover the parent paper’s threat model modulo a single residual
                                             — the LLM’s freedom to refuse to act — which the parent paper’s runtime biconditional already
                                             catches at session boundary. The methods reuse existing well-engineered tools (Z3, Semgrep /
                                             CodeQL, refinement-type checkers, mechanized proof assistants) rather than asking operators to
                                             build new ones, and the proposed proof-carrying-skill artifact is a small extension to the existing
                                             SKILL.md convention.
                                             Implementation. All three methods, the proof-carrying skill bundle, and the bootstrap re-
                                             checker ship as zero-runtime-dependency JavaScript modules in the open-source enclawed
                                             framework [28, 30] at https://github.com/metereconsulting/enclawed (project page https:
                                             //www.enclawed.com/), with a 53-test unit suite and an end-to-end command-line interface
                                             (CLI) demonstrated on a sample skill. Section 8.4 pins file paths and test counts to the public
                                             commit referenced here.

                                        Keywords: agent skills, formal verification, capability containment, refinement types, abstract
                                        interpretation, SMT, proof-carrying code, biconditional.


                                        1    Introduction
                                        The companion paper [29] treats a skill as a tuple (M, content, σ) with a manifest M that includes a
                                        verification level field M.verification ∈ {unverified, declared, tested, formal} and a runtime

                                                                                               1
gate whose human-in-the-loop (HITL) policy is keyed to that level. The runtime defaults to
unverified on every skill it has not seen verified evidence for, drives every irreversible call through
HITL while a skill is at unverified, and only relaxes HITL frequency when the manifest reaches
declared or higher. The top of the lattice, formal, is defined as the existence of a machine-
checkable proof that the skill’s behaviour is contained in M.caps. The parent paper does not say
how such a proof is produced. Section 3.1 of [29] is explicit about why: “This level is aspirational
at the time of writing; we include it for completeness because the schema field is fixed-width and
adding it later requires a manifest version bump.”
    This paper supplies the missing methods. We answer four interlocking questions left open by
the parent:

  1. What does “a skill’s behaviour” mean formally, given that the skill content is a (deterministic)
     text/script artefact but the agent that consumes it is a (non-deterministic) LLM?

  2. What is the verification target — precisely which property must a candidate skill establish
     before its manifest can claim M.verification = formal?

  3. Which formal-methods tools available today are sound for which portions of that target, and
     where does each fall short?

  4. How does a deployer compose those tools into a single proof-carrying artefact a runtime can
     mechanically check at bootstrap, without trusting the proof’s producer?

Contributions.     We make six contributions.

  1. A two-sided skill semantics (Section 2) separating the deterministic script-side S from the
     non-deterministic LLM-side A, with a precise definition of the runtime trace they jointly
     produce.

  2. A capability-containment property (Section 3) stated as a sound abstraction of the parent
     paper’s biconditional, with explicit treatment of which projections of the trace admit static
     reasoning and which do not.

  3. Three composable verification methods (Sections 4 to 6): sound capability-containment static
     analysis on S; a refinement type system for tool-call envelopes; SMT-bounded model checking
     of the runtime trace against the biconditional.

  4. A three-layer discipline (Section 7) that combines those three methods plus the parent paper’s
     runtime biconditional, with a composition theorem that names exactly which residual surface
     falls outside the joint guarantee.

  5. A proof-carrying skill artefact (Section 8) that extends SKILL.md with a signed evidence
     bundle the runtime can re-check at bootstrap without trusting the artefact’s producer.

  6. A worked example (Section 9) on a real SKILL.md skill from the open reference implementation
     [28], including the static-analysis output, the type-checker derivation, the SMT counter-example
     search, and the resulting proof bundle.




                                                  2
Scope and non-goals. We do not attempt formal verification of the LLM itself. The model’s
weights, training data, and decoding stochastics are out of scope, as in the parent paper. We verify
the runtime’s ability to enforce capability containment under the assumption that the LLM is
an adversarial non-deterministic oracle bounded only by the typed dispatch interface the runtime
imposes. We do not require operators to write proofs in Coq or Lean; the static layer (Section 4)
is automatic and the type-checking layer (Section 5) requires only manifest- level annotations.
The mechanised-proof option is offered for deployments that need it (the Cryptographic Module
Validation Program (CMVP), Common Criteria Evaluation Assurance Level 5 or higher (EAL5+))
but is not the central recommendation.


2     Two-sided skill semantics
A skill, when consumed by a runtime, is not a passive document. It reaches the agent through two
distinct execution surfaces, and any verification method that conflates them gets the soundness
analysis wrong.

2.1   Provenance: the same split appears in dynamics and in information theory
The script-side / LLM-side partition we use is not a modelling convenience invented for this paper. It
is the same split that distinguishes deterministic flows from stochastic flows in non-linear dynamical
systems [41, 49], and the same split that distinguishes noiseless from noisy channels in information
theory [14, 47]. Every verification choice we make in Sections 4 to 6 traces back to one of those two
formalisms, and the bound we obtain in each case is the bound that formalism already gives.

Dynamical-systems view. For the security reader: a dynamical system is a rule that says how
the state of some thing-of-interest — an executing program, a packet trace, an LLM session —
evolves in time. The rule has two flavours. A deterministic system is one where the rule, plus
the initial state, picks out exactly one future trajectory: same start ⇒ same path, every time. A
stochastic system is one where the rule injects randomness at every step (think: temperature in
LLM decoding, jitter in a network, timing in side channels), so the same start gives a distribution
over futures rather than a single path. The two cases need different verification rules because the
right object to reason about is different: a set in the deterministic case, a probability measure in
the stochastic case.
    Concretely, a deterministic non-linear flow on state x ∈ X is the ordinary differential equation
(ODE)
                               ẋ = f (x),     f : X → T X Lipschitz,                             (1)
where ẋ = dx/dt is the rate of change and f tells us which way the state moves at every point. The
Lipschitz condition (∥f (x) − f (y)∥ ≤ L ∥x − y∥ for some constant L) is a regularity assumption
that prevents the flow from blowing up; it is the assumption Picard–Lindelöf needs to prove the
trajectory x(t; x0 ) is unique for every initial condition x0 . The set of states the system can ever
reach, Reach(x0 ) = {x(t; x0 ) : t ≥ 0}, is just a set — no probabilities — and over-approximating it
is the canonical job of abstract interpretation [13], the formal core of every static analyser used in
security (Semgrep, CodeQL, Pyright).
    A stochastic flow replaces Equation (1) with a stochastic differential equation (SDE)

                                     dx = f (x) dt + σ(x) dWt ,                                    (2)



                                                  3
where Wt is a Wiener process — the continuous-time analogue of a random walk, the standard
model for “unpredictable noise applied at every infinitesimal step” — and σ(x) scales how much
that noise affects the dynamics in state x. The trajectory is no longer a single curve but a measure
on path space, so what we actually track is the probability density p(x, t) that the system is at state
x at time t. That density evolves under the Fokker–Planck equation

                                 ∂t p = −∇· f p + 21 ∇·∇· σσ⊤ p ,                                   (3)
                                                                    


a partial differential equation whose first term is drift (the deterministic push) and whose second
term is diffusion (the spreading caused by noise). The right object to bound is now the support and
the moments of p(x, t) — where in state space the density has nonzero mass, and how concentrated
it is — not the value of x at any particular time.
     The script-side S (Section 2.2) is exactly an instance of Equation (1): the language semantics
of each script pi associates to every input a single concrete trace, and the effect set E(pi ) is the
projection of Reach onto the capability dimension. The LLM-side A (Section 2.3) is exactly an
instance of Equation (2): the model’s weights, temperature, and decoding strategy fix f and σ; the
prompt fixes x0 ; the output token stream is one realisation of a stochastic flow whose distribution
over actions is the right object to bound. Conflating the two surfaces means writing one verification
rule that the relevant formalism cannot satisfy: a deterministic-flow rule cannot bound a Fokker–
Planck density (it under-specifies), and a Fokker–Planck rule cannot extract a script’s reachable
effect set (it over-specifies).

Information-theoretic view. For the security reader: information theory gives us a way to ask
the question “how much can an attacker learn through this interface?” as a number, in bits, rather
than a hand-wavy story. A channel is anything that takes an input symbol X and produces an output
symbol Y — a network link, a syscall interface, a tool-call boundary, the LLM’s sampling stage.
The capacity C of a channel is the largest number of bits per use that can be reliably communicated
through it; if the attacker is the sender and the defender is the eavesdropper-prevention boundary,
capacity is the worst-case leakage rate. Two quantities matter: bandwidth B, how many channel
uses fit in a unit of time (so capacity has units of bits/s), and signal-to-noise ratio S/N , how clean
the channel is. A deterministic (noiseless) channel has S/N = ∞ and leaks log2 M bits per use
where M is the number of distinguishable output symbols; a noisy channel has S/N < ∞ and leaks
strictly less, because the receiver cannot perfectly distinguish outputs.
    The cleanest entry point is the Shannon–Hartley theorem [14, 47] for an additive–Gaussian-noise
channel of bandwidth B and signal-to-noise ratio S/N :

                                  C = B log2 1 + S/N         [bits/s].                              (4)
                                                         


In the noiseless limit N → 0 the SNR diverges and Equation (4) reduces, after the per-symbol
normalisation, to the Hartley form C = log2 M bits per channel use, where M = |Yreach | is the
number of distinguishable output symbols. For a discrete channel with arbitrary noise the same
quantity is recovered as the classical mutual-information capacity

                         C = max I(X; Y ) = max H(Y ) − H(Y | X) .                                  (5)
                                                                           
                                p(X)              p(X)

Here H(Y ) is the Shannon entropy of Y (the average bits of “surprise” in the channel output, if the
receiver knew nothing else), H(Y | X) is the conditional entropy of Y given X (the residual surprise
once the input is known — exactly the noise term), and I(X; Y ) = H(Y ) − H(Y | X) is their
difference, the mutual information: how many bits the output carries about the input, on average.

                                                     4
The deterministic-channel case (H(Y | X) = 0, hence C = max H(Y ) = log2 |Yreach |) is exactly the
noiseless limit of Equation (4): capacity is set by the reachable output alphabet, achievable by
direct enumeration, no distributional analysis required.
    The script-side is precisely this noiseless limit: the language semantics gives H(Y | X) = 0
by construction, and Method A’s job is to compute (or over-approximate) Yreach = E(p) so the
per-script bound log2 |E(p)| is recovered. The LLM-side, by contrast, sits at finite S/N in the full
Shannon–Hartley regime: the sampling distribution gives H(Y | X) > 0, and no language-level
analyser yields anything useful about its output distribution. We can however constrain the channel
output alphabet from the outside, by inserting a deterministic projector

                                                             cap(y) if cap(y) ∈ D,
                                                           (
                     π : Y → D ∪ {⊥},          π(y) =                                             (6)
                                                             ⊥      otherwise,

between the LLM and the host APIs, where ⊥ (read “bottom” or “perp”) is the standard formal-
methods shorthand for “no admissible value” — here the runtime’s deny verdict when the envelope’s
capability is not in the declared set D. Because π is a function of y alone, the chain world →
Y → π(Y ) is a Markov chain in the information-theoretic sense: each variable depends only on its
immediate predecessor, with no extra randomness or side input slipping in at the second arrow. For
Markov chains the data-processing inequality (DPI) [14, Thm. 2.8.1] applies, and it says exactly
what intuition demands — post-processing can never increase information —

                                  I(world; π(Y )) ≤ I(world; Y ),                                 (7)

with |π(Y )| ≤ |D| + 1 pinning the post-projector alphabet, and therefore C at the dispatch boundary,
at log2 (|D| + 1) bits per envelope. Equations (6) and (7) are the information-theoretic skeleton of
Method B (Section 5): the refinement type system instantiates π as a typed dispatch boundary, and
the channel-capacity bound on the post-dispatch alphabet is the bound on what an adversarially-
prompted LLM can leak per envelope.
    The bounded model checker of Method C (Section 6) is the matching tractability claim: once
the LLM-side is reduced to the finite output alphabet Σ = D ∪ {OUT} by π, the joint distribution
over K-length envelope traces lives on a state space of size |Σ|K = (|D| + 1)K , which is small enough
to enumerate exhaustively for the deployment- relevant regime |D| ≤ 10, K ≤ 8 ((|D|+1)K ≤ 118 ≈
2.1 × 108 symbolic traces). The reduction from the continuous-distribution Fokker– Planck dynamics
to a finite-state symbolic enumeration is exactly the abstraction step that bounded model checking
performs in any non-trivial verification setting [9, 22].
The rest of §2 re-derives this split from the syntactic structure of SKILL.md, so a reader who
has not studied dynamical systems or information theory can still follow the constructions. The
dynamical-systems and channel-capacity readings are for the reader who wants to know why the
constructions are the right ones rather than expedient ones.

2.2   The deterministic script-side
A skill’s content typically contains a SKILL.md prose body plus zero or more scripts (Python, shell,
Node, Go, the Rust binary the skill invokes, etc.) that the prose instructs the agent to call. Each
script is a deterministic program in a known language with a known semantics.
    We model the script-side S of a skill as a finite collection of named programs

                                     S = { (pi , Li , src i ) }i=1...n ,


                                                     5
where pi is the program identifier, Li its source language, and src i the program text.
    We assume each language’s semantics ascribes to every program a set of system-effect tu-
ples E(p) ⊆ C × V where C is the parent paper’s capability vocabulary (net.egress, fs.read,
fs.write.rev, . . . ) and V is the value space of their associated arguments (target hosts, file paths,
etc.). The language semantics is sound for E iff every concrete execution of p on every concrete input
emits only effect-tuples in E(p). For mainstream scripting languages this set is finite, computable,
and already produced by existing dataflow analyzers [13, 19, 21, 40].

2.3   The non-deterministic LLM-side
The LLM-side A is a stochastic transducer that reads the union of the skill’s prose body, the
runtime’s system prompt, the user’s turns, and any tool output observed so far, and emits one of: a
tool-call envelope of shape ⟨op, args, reasoning⟩, a plain message to the user, or end of turn. We do
not model A’s internal state. We model only the typed interface through which it can affect the
world: the tool-call envelope.
    For verification purposes the only fact we need about A is that the runtime can intercept every
tool-call envelope before it reaches a host application-programming interface (API). This is the sole
structural assumption the parent paper makes about the runtime in §3.1, and it is satisfied by every
harness that adopts SKILL.md.

2.4   The composed runtime trace
A run of skill-and-agent on a session sess produces a trace τ (sess), which is the time-ordered
concatenation of every tool-call envelope A emitted (whether eventually executed or denied at the
gate) and every script-launched system-effect S produced as a side-effect of those envelopes:

                             τ (sess) = e1 e2 e3 · · · ek ,   ei ∈ (C × V).

Each ei is annotated with its origin (A or S), its requested capability, the runtime’s gate decision
(admit / deny / HITL-approve / HITL-deny), and a hash linking it to its audit-log record. The
audit log of [29], by construction, is a faithful serialisation of τ with one record per envelope and
one record per executed effect.
   We write ΠC (τ ) ⊆ C for the projection of τ onto its capability dimension — the set of capability
tokens that appear anywhere in the trace, regardless of origin or gate decision.

2.5   Why splitting the sides matters for verification
Existing skill-verification proposals treat the skill as a single opaque artefact. That collapses two
very different verification problems. The script-side S is amenable to standard program analysis:
every effect S can produce is recoverable by inspecting S’s source, modulo the soundness of the
analyser for the language. The LLM-side A is fundamentally not amenable to that treatment: A’s
output is a function of its weights, the prompt, and the decoding state. No language-level analyser
yields anything useful about A.
    The split lets each side be verified by a tool that fits it. We show in Section 4 that a sound script-
side analysis plus the runtime gate is enough to bound ΠC (τ ), and in Section 5 how a refinement
type system on the tool-call envelope mechanically prevents A from getting an out-of-manifest
envelope past the runtime in the first place.




                                                     6
3     The verification problem
Fix a skill K = (M, content, σ) with M.caps = D ⊆ C a finite declared capability set, and a runtime
R satisfying the parent paper’s threat model and gate policy.

Definition 1 (Capability containment). K exhibits capability containment on a session sess iff
ΠC (τ (sess)) ⊆ D.

Capability containment says: every capability that appears anywhere in the trace — whether in an
envelope A requested, in a side-effect S produced, in a denied call, or in a HITL-rejected one — is a
capability the manifest declared. The reverse inclusion is not required: a manifest may over-declare
(D ⊋ ΠC (τ ) is fine; over-declaration is loud, contained, and surfaceable to operators by post-hoc
diff). Containment is the dangerous direction.

Proposition 1 (Containment subsumes the parent biconditional). If K exhibits capability contain-
ment on every session in some session set Σ, the runtime’s hash-chained audit log correctly records
every executed effect, and the gate decision is deterministic given the envelope and policy, then the
parent paper’s biconditional criterion [29, §5] holds on Σ.

Proof sketch. The parent biconditional says: observable side-effects of the run must be in 1-to-1
correspondence with the approved-and-executed set in the audit log. By construction the audit
log is the serialisation of τ . By containment, every capability appearing in the trace is in D, so
every executed effect’s capability is admissible; the gate’s deterministic policy then ensures the
executed-set equals the approved-set. The 1-to-1 correspondence follows.

Definition 2 (The verification problem). Given K and R, the verification problem is to produce
either

    • a mechanically checkable certificate π that K exhibits capability containment on every session
      R admits; or

    • a counter-example session sess ⋆ such that ΠC (τ (sess ⋆ )) ̸⊆ D.

    The remainder of this paper presents three composable methods that, together, produce π. Each
method is sound for a portion of the target; the composition theorem (Theorem 4) says exactly
which residual the runtime layer (the parent paper’s biconditional, treated here as a fourth layer)
closes.


4     Method A: sound script-side static analysis
Goal. For each script p ∈ S, compute an over-approximating set E(p)   b   ⊇ E(p) in finite time, and
check E(p)
       b    ⊆ CD where CD is the lift of D to the language’s effect type. Read: “read every script in
the skill and figure out, without running it, the maximum set of system effects it could possibly
produce; then check that set against the manifest’s declared capabilities.”

Primer on abstract interpretation. Method A is an instance of the technique called abstract
interpretation [13], which is the formal core of every static analyser the security reader has likely
already used (Semgrep, CodeQL, Pyright). The idea in one paragraph: instead of running the
program on real values, run it on summaries of values. A path argument becomes a regular-
expression summary, a network target becomes a host-pattern summary, an integer becomes an


                                                   7
interval. These summaries form a lattice — an ordered structure in which any two summaries have
a least-upper-bound (their join, written ⊔) and a greatest-lower-bound (their meet, written ⊓).
Two distinguished elements anchor the lattice: ⊥ “bottom”, the empty summary, the “no effect”
element; and ⊤ “top”, the maximum summary, the “effect could be anything” element used whenever
the analyser hits a construct it cannot summarise (reflection, dynamic dispatch). Every program
construct is then assigned a transfer function — a rule that takes the summaries of its inputs and
returns the summary of its output, in the lattice. Loops and recursion are handled by repeatedly
applying the transfer functions until the summaries stop changing (a fixpoint), accelerated by an
operator called widening that forces convergence in a bounded number of steps at the cost of slightly
less precise summaries. The result is a sound over-approximation: the real program can only ever
produce effects that the abstract summary already accounts for. “Sound” in this context means
conservative: the analyser may flag effects the program cannot actually produce, but it will never
miss an effect the program can produce.

4.1   The effect lattice
We attach to every program point of every script a finite lattice E whose elements are subsets of
C × V ♯ , where V ♯ is the abstract domain over the value space introduced in the primer (regular-
language summaries for paths, host-pattern summaries for network targets, integer intervals for
numeric arguments, ⊤ for everything else). The lattice operations are set union (⊔) and set inclusion
(⊑); ⊥ is the empty effect set; ⊤ is “every effect”. This is the standard effect-system formulation of
[27], lifted to the parent paper’s capability vocabulary.

4.2   The transfer functions
For each kind of language construct that can produce an effect we fix a transfer function. We give
the four most important here; the full list is straightforward and depends only on the language.

Function calls. A call to a system function f with arguments a1 , . . . , an produces effect
    fb(a            cn ), where fb is a per-language summary that maps the runtime’s capability
       c1 , . . . , a
    vocabulary to the language’s standard library. For Python, the entry for open(p, ’w’)
    produces {(fs.write.irrev, pb)} if the file mode is W and pb is the abstract value of the path
    argument. For requests.get(u) the entry produces {(net.egress, u      b)}.

Loops, recursion, fixpoints. For loop bodies we apply the standard widening of [13] so that the
    lattice converges in a bounded number of steps. The widened result is sound but may be
    coarser than the loop’s actual effect set.

Indirection through reflection / exec / eval. Any program point that reaches a reflective
     construct unconditionally taints the whole-program effect set with ⊤. This is sound and
     conservative; it forces the operator either to remove reflective constructs from the skill’s scripts
     or to drop the skill below formal. The empirical claim of the parent paper’s adversarial
     ensemble is that reflective constructs are rare in well-curated skills; the few that need them (a
     code-runner skill, a sandboxed evaluator) are precisely those that should not aspire to formal
     verification anyway.

Process spawn. A spawn.proc(cmd) effect taints the scope of the child process with ⊤ unless
    the child program is itself in S and has been analysed: in that case the parent inherits the
    child’s E(child).
            b



                                                   8
4.3    Implementation reuse
A working implementation of Method A does not need to be written from scratch. Semgrep, CodeQL,
and Pyright [19, 31, 40] are mature dataflow / abstract- interpretation engines whose existing rule
packs already cover the language constructs that produce capability-relevant effects. The adaptation
effort is the per-language summary table for fb in the previous subsection.

4.4    What Method A is sound for
Theorem 1 (Soundness of Method A). If for every p ∈ S the analyser produces E(p)      b    ⊆ CD , then
for every concrete execution of every p on every concrete input, every system-effect p produces is in
D. In particular, the script-side projection ΠSC (τ ) is contained in D for every session.

Proof sketch. By induction on the program structure, exploiting the over- approximation property
of the transfer functions. Reflective constructs are conservative-tainted to ⊤; if the analyser still
reports E(p)
         b    ⊆ CD it has proven the absence of reflective constructs (or that the constructs are
unreachable), which is itself a sound conclusion.

4.5    What Method A is incomplete for
Method A says nothing about envelopes the LLM-side A may emit. A may emit an envelope whose
capability is outside D regardless of what the script-side does; the static analyser cannot see that
emission because it does not analyse A. We close this gap with Method B.


5     Method B: refinement types for tool-call envelopes
Goal. Construct the runtime’s tool-dispatch interface so that an envelope whose capability is not
in D is rejected at the type level before reaching any host API.

Primer on refinement types. A refinement type [43, 53] is an ordinary type — like “int” or
“string” or “Envelope” — with an extra logical predicate attached. Where a plain type system says
“this value is an integer”, a refinement type says “this value is an integer and it is between 0 and 255”.
The compiler’s type checker is then required to discharge the predicate at every place such a value
is used: a function that takes a refined “integer between 0 and 255” will not accept a plain integer
until the caller has proven the bound. The predicate becomes a compile-time gate: ill-conforming
values are rejected before the program ever runs. For our purposes the predicate is “the envelope’s
capability is in the manifest’s declared set”. The compiler’s discharge of that predicate is what
turns the type system into a proof that the runtime cannot dispatch an out-of-manifest envelope.
Refinement types are not exotic — the technique already ships in production tooling for Haskell
(Liquid Haskell), F⋆ , Dafny, and as a more limited form (template literal types, branded types) in
TypeScript.

5.1    The dispatch type
The runtime’s dispatch entry point is a function dispatch : Envelope → Result. We parameterise
the runtime by the loaded skill’s manifest and assign the dispatch a refinement type [26, 43, 53] of
the form
                   dispatchM : { e : Envelope | cap(e) ∈ M.caps } → Result.



                                                    9
The refinement is on the input: the only envelopes the type checker admits as well-formed for
dispatchM are those whose declared capability lies in the manifest’s capability set. An envelope
outside M.caps is statically ill-typed at the dispatch boundary.

5.2   What this buys
Construction-by-construction, the runtime’s source becomes a guarantee: there is no execution
path from envelope receipt to host API call that does not go through dispatchM , and dispatchM
statically rejects out-of-manifest envelopes. A type-checked runtime cannot accidentally relax the
gate, because the gate is the type signature.
    This is the same shape as the capability-machine work of [48] lifted from CPU-level capabilities to
skill-manifest capabilities, and the effect-system work of [27, 44] adapted to agent-emitted envelopes.

5.3   Implementation paths
TypeScript / refinement annotations. The simplest path, deployable today, uses the existing
TypeScript tagged-union discipline plus a generated type per skill that constrains the union to the
loaded manifest’s capability tokens. The [28] reference implementation already uses this pattern in
its plugin-sdk (tool.invoke, net.egress, fs.read, . . . are nominal types on the dispatch entry
point); the missing piece is the manifest-level specialisation, which is a code-generation step at
bootstrap.

Liquid Haskell / F⋆ . For deployments that need a machine-checkable certificate at the type level,
the dispatch function can be rewritten in Liquid Haskell [53] or F⋆ [50] with the refinement spelled
out as a predicate. The certificate is then the type-checker’s accepted proof obligation discharge,
exportable to operators. The cost is a one-time port of the dispatch surface; the runtime body need
not be rewritten.

Erasure semantics. We require the type discipline to be erasure-stable: the production runtime
must not depend on any runtime-level reflection or dynamic check that the type system already
discharged. If the runtime includes a runtime-time “capability check” that duplicates the type-level
guarantee, that check is at best redundant, at worst a place a future maintainer removes “because
the types already do it”. Either keep the runtime check and remove the type-level one, or vice versa.

5.4   What Method B is sound for
Theorem 2 (Soundness of Method B). If dispatchM type-checks under the refinement {e | cap(e) ∈
M.caps}, then no envelope whose capability is outside M.caps can reach any host API through the
runtime, regardless of the LLM-side’s behaviour.

Proof sketch. By the soundness of the chosen refinement-type system ([43, 50, 53]), if the dispatch
function type-checks then every call site has been verified to satisfy the refinement. The runtime’s
source forbids host-API call paths that bypass dispatch (this is a structural invariant, checked once
by inspection or by a separate analyser; it is the runtime equivalent of the parent paper’s G10 “no
bypass switch”). The LLM-side’s freedom is to emit any envelope it likes; only in-manifest envelopes
survive dispatch, so only those reach any host API.




                                                  10
5.5   What Method B is incomplete for
Method B does not cover the script-side: a script invoked through an in-manifest envelope can
still produce arbitrary side-effects internally if the script’s source escapes the envelope’s declared
capability boundaries (e.g. the script’s internals call requests.get when the envelope declared only
tool.invoke). Method A closes this gap.


6     Method C: SMT-bounded model checking against the bicondi-
      tional
Primer on SMT, BMC, and the biconditional. Three terms in the section title need unpacking
before we proceed. SMT stands for “Satisfiability Modulo Theories” [15]: an SMT solver takes a
logical formula written in first-order logic plus background theories (integer arithmetic, bit-vectors,
arrays, uninterpreted functions) and decides whether there exists an assignment of values to the
formula’s variables that makes it true. If yes, the solver returns a witness assignment (sat); if
no, the solver returns a proof of impossibility (unsat). The solver of record for our purposes is
Z3 [15], but any modern SMT solver (CVC5, Yices, MathSAT) will do. BMC, “bounded model
checking” [9], is the technique of asking the solver: “does there exist a violation of property P
in any execution of length at most K?”. The “bounded” part is the trick that makes verification
tractable: unbounded model checking on programs that loop or branch is in general undecidable,
but for any concrete bound K the question collapses to a finite SMT instance. Biconditional is
a logical connective: A ⇔ B asserts “A if and only if B” — both “A implies B” and “B implies
A”. The parent paper’s runtime check is biconditional: every world-state change must correspond
to (and only to) an admitted envelope in the audit log. Method C asks the solver to search for a
session in which that biconditional fails.

Goal. For a skill K that has passed Methods A and B, construct an SMT instance whose models
are exactly the runtime traces τ that violate the parent paper’s biconditional, and search for a
model up to bound Kmax . If the search returns unsat the biconditional holds up to that bound; if
it returns sat the witness is a concrete counter-example trace.

6.1   Encoding the trace
We encode a session of length n ≤ Kmax as a sequence of SMT variables

                                  e1 , e2 , . . . , en ,   ei ∈ Envelope abs ,

where Envelope abs is the abstract envelope domain produced by Method A’s analysis (host patterns,
path patterns, etc.). The runtime’s gate policy is encoded as a deterministic function g(e, state) →
{admit, deny}. The audit log L is encoded as a pair sequence (ei , g(ei , state i )). The biconditional
violation is encoded as the predicate

                       ∃ ei : statei .world ̸= statei−1 .world ∧ (ei , admit) ∈
                                                                              / L.

(“A world-state change occurred but the audit log does not record the corresponding admitted
envelope.”) The SMT solver [9, 15] searches for a satisfying assignment of the ei ’s and state i ’s.




                                                           11
6.2   The bound Kmax
The bound is the number of envelopes a session can produce before the parent paper’s runtime
biconditional check fires. The parent paper §3 says the check fires between rounds; the runtime’s
transaction buffer flushes every irreversible call and every biconditional check on flush. So Kmax
is the runtime-configurable horizon of the transaction buffer (typically ∼ 100 envelopes), not the
unbounded length of a session. This is precisely the property of the parent paper’s runtime that
makes bounded model checking sufficient: any counter-example that fits in the buffer’s horizon will
be found by the SMT search; counter-examples larger than the horizon are caught at flush by the
runtime biconditional itself.

6.3   Implementation reuse
The SMT instance is small (envelope counts of order Kmax , abstract value domains from Method
A’s lattice). Z3 [15] discharges instances of this size in seconds; KLEE [11] and DART [20] provide
the symbolic-execution backbone for the script-side portion if needed. The LLM-side does not need
to be modeled symbolically: the SMT search universally quantifies over LLM-emitted envelopes,
treating A as a non-deterministic adversary — which is the worst-case assumption Method B makes
anyway.

6.4   What Method C is sound for
Theorem 3 (Soundness of Method C up to Kmax ). If Method C’s SMT search returns unsat for
the biconditional-violation predicate at bound Kmax , then no session of length ≤ Kmax violates the
biconditional.

Proof sketch. Standard bounded model-checking soundness [9]: the SMT instance is a faithful
encoding of sessions of bounded length, and unsat of the violation predicate means no such session
exists.

6.5   What Method C is incomplete for
Sessions longer than Kmax are not covered. The runtime’s biconditional check at flush is sound for
unbounded sessions; it just runs at session boundaries rather than as a pre-deployment proof. The
composition theorem (Theorem 4) explains how the two layers combine.


7     The three-layer discipline (and what closes the residual)
A skill is elevated to M.verification = formal when, and only when, all three of the following hold
for (K, R):

Layer 1. Every script p ∈ S has been analysed by a sound static effect-tracker (Method A) that
    reports E(p)
            b    ⊆ CD .

Layer 2. R’s dispatch entry has been type- checked under the refinement {e | cap(e) ∈ M.caps}
    (Method B).

Layer 3. An SMT search at bound Kmax (Method C) has reported unsat on the biconditional-
    violation predicate.



                                                12
Theorem 4 (Composition). If Layers 1, 2, and 3 all succeed, and R enforces the parent paper’s
runtime biconditional check at every transaction-buffer flush, then K exhibits capability containment
on every session R admits.

Proof sketch. Layer 2 implies that no out-of-D envelope reaches a host API. Layer 1 implies that
no script-side execution produces an out-of-D effect. Together, the script-side projection ΠSC (τ ) and
the LLM-side projection ΠA C (τ ) are both contained in D, so ΠC (τ ) = ΠC (τ ) ∪ ΠC (τ ) ⊆ D. Layer 3
                                                                         A         S

closes the bounded counter-example search: no session of length ≤ Kmax violates the biconditional.
The runtime’s per-flush biconditional check covers sessions longer than Kmax by the parent paper’s
correctness criterion (cited as Proposition 5.1 of [29]). Containment for every admitted session
follows.

7.1    Residual surface
Three classes of behaviour fall outside the joint guarantee, and each is acknowledged in either the
parent paper or the threat model:

    1. Read-only exfiltration. The LLM-side may surface information through its plain-message
       channel that the operator deems sensitive. No capability is invoked, so capability containment
       is trivially satisfied. The parent paper’s classification primitive and data-loss-prevention (DLP)
       scanner sit below the dispatch boundary precisely to handle this.

    2. Time-of-check-to-time-of-use (TOCTOU) on the world state. Between a host-API call being
       approved and being executed, an external actor may alter the world. The runtime’s audit log
       records the approved envelope and the executed effect; if they diverge in a way the world’s
       external interface admits (e.g. the target file vanished between approval and write), the
       biconditional flags it. Capability containment is not violated; the audit log is the post-hoc
       evidence.

    3. Operator coercion. An operator forced (or socially engineered) to approve a HITL prompt for
       an envelope they should have denied. The runtime can do nothing here; the biconditional
       records what was approved, and the post-hoc review is the operator’s accountability layer.
       The parent paper’s broker-policy taxonomy (deny-all / policy / interactive / webhook)
       is the operator’s design tool for bounding this risk.


8     Proof-carrying skill artefacts
The three-layer discipline produces, for each verified skill, an evidence bundle the runtime can
re-check at bootstrap without trusting the bundle’s producer. We sketch the bundle’s structure as a
small extension to the existing SKILL.md convention. The design follows the proof-carrying-code
idiom of [5, 24, 35]: the producer ships proofs along with the artefact; the consumer checks them
mechanically.

8.1    The bundle
A formal-verified skill ships, alongside SKILL.md and its scripts, the following four artefacts:

evidence/static.json The output of Method A: per-script effect summaries E(p)b in a canonical
     JSON encoding, plus the analyser identity, version, and rule-pack hash.


                                                   13
evidence/types.proof A serialisation of the type-checker’s proof obligation discharge for Method
     B. For TypeScript-only deployments this is the compiler’s accepted module set with its
     capability-discriminated union types pinned at the manifest’s D. For Liquid Haskell or F⋆
     deployments this is the proof certificate emitted by the type checker.

evidence/smt.unsat The SMT instance and Z3’s unsat certificate (when supported) for Method
     C at bound Kmax . The instance is reproducible from (K, R, M, Kmax ) at bootstrap.

evidence/manifest.attest.json A signed attestation binding the manifest hash to the verification
     level formal, listing the three evidence-file hashes and the toolchain identities, signed by a
     trust-root signer authorised to attest at that level.

8.2   Bootstrap-time re-check
At bootstrap, the runtime walks the bundle:

  1. Verify σ over (M, content) as in [29, §3.4].

  2. Resolve the attestation in manifest.attest.json against the trust root; reject if the signer
     is not authorised to attest at level formal.

  3. Re-run Method A on the script-side and verify E(p)
                                                      b   ⊆ CD . The bundle’s static.json is not
     trusted on its own; it is a cache the runtime can compare against. A drift between the cached
     and the freshly-computed E(p)b    aborts admission.

  4. Re-type-check the dispatch surface against the manifest’s D. For TypeScript this is a compile-
     step the runtime runs; for Liquid Haskell / F⋆ this is the proof- obligation re-discharge.

  5. Re-run the SMT instance from smt.unsat. Z3’s certificate is verified by an independent
     checker ([15]’s verify-proofs mode for instance); the unsat verdict must reproduce.

    If every step succeeds the runtime accepts the manifest at formal; otherwise the runtime
degrades the manifest to declared and logs the reason. The runtime never trusts the producer’s
say-so; the bundle is a precomputed cache, and the runtime is the verifier. This is the precise
structure of proof-carrying code [35].

8.3   What about the toolchain itself?
The static analyser, the type checker, and the SMT solver are themselves software with bugs. The
bundle pins their identities and versions; an operator can replace any of them with a mechanically-
verified equivalent (CompCert [24] for the compiler; an audited port of Z3 for the SMT solver) at
the cost of additional one-time engineering. We do not require this for the default deployment, but
the bundle’s structure admits it. This is the same “trusted base” question every proof-carrying-code
system faces [5]; we take the same answer: name the trusted base, audit it once, re-use the audit.

8.4   Implementation status
Methods A, B, and C, the bundle producer, and the bundle re-checker are implemented in the open-
source enclawed framework [28]. The four primitives ship as zero-runtime-dependency JavaScript
modules under enclawed/src/:



                                                14
skill-formal-static.mjs Method A. Pattern-based scanners for Python, shell, and Node/Type-
     Script over the capability vocabulary C from Section 2.2, with reflective constructs (eval,
     exec, new Function, dynamic import) tainted to the lattice top so the verdict is conservative
     by construction.

skill-formal-types.mjs Method B. The function buildRefinedDispatch(M ) returns the pro-
     jector π of Equation (6) as a frozen dispatcher that throws a RefinementError on any
     envelope outside D. The accompanying methodB runs the exhaustive probe across the schema
     vocabulary and emits the typed-dispatch verdict.

skill-formal-bmc.mjs Method C. Exhaustive depth-first search over the abstract envelope state
     space of size (|D|+1)Kmax with the biconditional check from Section 6 as the per-trace predicate.
     The verdict carries instanceHash = sha256 ⟨D, Kmax ⟩ so a re-checker independently confirms
     the bound.

skill-formal-bundle.mjs The bundle producer and verifier. produceFormalBundle composes
     the three method outputs, hashes each evidence file with a sorted-key canonical encoding, and
     signs the attestation with the existing Ed25519 module-signing primitive. The symmetric
     verifyFormalBundle re-runs all three methods against the manifest, compares hashes, and
     rejects on tamper, on signer-not-authorised, or on post-production skill drift.

A unit-test suite of 53 tests (enclawed/test/skill-formal-*.test.mjs) covers pattern matches,
refinement-boundary throws, biconditional violation detection (executed-without-audit, executed-
but-deny, admitted-without-audit), sign / verify round-trips with both an in-set and an unauthorised
signer, tamper detection on every evidence-file slot, and cache-miss-on-skill-drift. All 53 tests pass
on the published commit.
    A command-line wrapper scripts/skills-formal-verify.mjs drives the producer end-to-end
against a real skill directory: it resolves the manifest from skill.json or the caps: field of
SKILL.md’s YAML (YAML Ain’t Markup Language) front-matter, mints an ephemeral Ed25519
key (or accepts an operator-supplied Privacy-Enhanced Mail (PEM) private-key file), runs Meth-
ods A / B / C, and writes the four-file bundle described in Section 8. A demonstration skill at
skills/_formal-demo/ ships in the same tree to make the flow reproducible. The full developer-
facing reference for the SKILL.md format — mandatory front-matter fields, the capability vo-
cabulary, the canonicalisation and Ed25519 signing convention, the bootstrap re-check proto-
col, and the proof-carrying bundle layout — is published at https://docs.openclaw.ai/tools/
skill-manifest-spec and maintained as the source of truth for skill authors and runtime integra-
tors.
    The implementation does not require a SAT/SMT solver, a refinement- type checker, or any
external dataflow engine. Method A uses language-specific regex pattern packs (extensible per
Section 4); Method B uses runtime-level refinement checks that are erasure-stable in the sense of
Section 5; Method C uses a finite enumerator. Heavy backends [15, 19, 40, 50, 53] remain available
as drop-in replacements at the corresponding attestation slots, but the default stack is self-contained
and auditable in a single afternoon.


9    Worked example
We walk a real skill from the open reference implementation [28] through the three layers and show
the resulting evidence bundle.


                                                  15
9.1     The skill
The skill summarise-fetched-html declares two capabilities:
{
    "id":          "summarise-fetched-html",
    "label":       { "rank": "public", "compartments": [], "releasability": [] },
    "caps":        ["net.egress(*.example.com)", "fs.read(./.cache/)"],
    "verification": "tested",
    "version":     7,
    "signer":      "operator-root-2026"
}

The script-side S is one Python program that uses requests to fetch a URL under *.example.com
and writes the body to a path under ./.cache/, then summarises by reading from the cache.

9.2     Layer 1 (Method A)
A Semgrep [40] pack with the per-language summary table of Section 4 reports

 E(p)
 b    = {(net.egress, *.example.com), (fs.read, ./.cache/), (fs.write.rev, ./.cache/)}.

The first two are in D; the third is not. This means the script silently writes (reversibly) into
the cache as a step of the read flow. The operator has a choice: extend the manifest to declare
fs.write.rev(./.cache/), or refactor the script. Either way the static layer surfaced an undeclared
effect that signature- plus-clearance review would have missed.

9.3     Layer 2 (Method B)
After the operator extends D to include the missing fs.write.rev, the runtime’s dispatch
type pinned to the new manifest type-checks. The type checker’s accepted derivation is the
evidence/types.proof content.

9.4     Layer 3 (Method C)
We encode a session of length Kmax = 100 envelopes with the extended D and the runtime’s gate
policy. Z3 returns unsat: no session of length ≤ 100 violates the biconditional. The certificate goes
into evidence/smt.unsat.

9.5     The bundle and the bootstrap re-check
A trust-root signer authorised to attest formal signs evidence/manifest.attest.json. At
runtime bootstrap, the runtime re-runs the four checks of Section 8; each reproduces. The skill
is admitted at M.verification = formal, and the runtime stops asking HITL on its in-manifest
irreversible calls (per the parent paper’s gate policy).

9.6     What this example showed in practice
    • Layer 1 caught a real declaration drift the prose review had not flagged. This is the layer’s
      most common practical win: scripts evolve and their declared capability sets lag behind.

    • Layer 2 was the cheapest of the three: the type system already pinned the dispatch surface in
      the reference implementation. The marginal cost was the manifest-level specialisation step.

                                                  16
   • Layer 3 was the slowest (a few seconds per skill at Kmax = 100), but ran in continuous integra-
     tion (CI) and produced an artefact the bootstrap re-check could re-discharge in milliseconds.


10     Discussion and open problems
10.1    Comparison to the state of the art (SOTA)
We position this work against the deployed and published landscape in agent-skill / LLM-tool-use
safety. The categories overlap, and the comparison is not a leaderboard — the honest summary is
that no other system in any of these categories produces a mechanically checkable proof that an
agent’s behaviour is contained in its declared capability set, but several are broader, more deployed,
or solve adjacent problems we deliberately did not attempt.

Tool-use protocols (Model Context Protocol (MCP), OpenAI function calling). MCP
[4] is the closest production peer to the parent paper’s skill format: an open protocol that ships
signed manifests, JSON-Schema-typed tool descriptions, and host-API binding for LLM tool calls.
OpenAI’s function-calling interface [37] is its closed-vendor equivalent. Both type-validate the
dispatch envelope’s shape via JSON Schema (correct field names, types, enum values) and both
bind tool calls to host functions. Neither performs static analysis of the script-side, neither carries
a refinement-typed dispatch parameterised by the manifest’s declared caps, and neither provides
a biconditional check that “every world-state change has a matching audit-log envelope.” Our
contribution is the layer above schema validation: capability containment, mechanically checked
across all three verification surfaces. MCP and function-calling are more broadly deployed and have
richer host-side ecosystems; this work is narrower (skill-manifest-level) and stronger (proof-carrying).

Agent-orchestration frameworks (LangChain, AutoGen, Semantic Kernel). Frameworks
like LangChain [23], AutoGen [32], and the various LLM-orchestration libraries provide tool-binding
APIs, conversation memory, agent loops, and retrieval-augmented generation, but they are explicitly
orchestration layers — they do not claim a verification posture. A LangChain agent that calls
requests.get is bound only by whatever the developer chose to expose; there is no manifest, no
declared capability set, no static check that the bound tools cover the agent’s intended behaviour,
and no audit-log biconditional. Our work is complementary in principle (a LangChain pipeline could
be wrapped in an enclawed-style runtime) but the orchestration frameworks themselves contribute
nothing toward the formal level.

Runtime policy engines (Open Policy Agent (OPA), Amazon Web Services (AWS)
Cedar). OPA [46] and AWS Cedar [1] let operators write declarative authorisation policies that a
runtime evaluates per request — “can subject s perform action a on resource r?”. Cedar in particular
ships with a formally-verified evaluator (Lean / Rust). Both are stronger than our work in a specific,
important sense: they prove the evaluator correct, where we assume the runtime is correct (see the
open-problem note on formally-verified runtimes below). Both are weaker on a different axis: their
policy is checked at request time against the request, with no static analysis of the side that issued
the request. An OPA-protected agent calling out-of-policy will be denied at the gate, but no proof
was produced before deployment that the agent could not issue such a request in the first place.
The two approaches stack: an enclawed skill could be deployed behind an OPA / Cedar gate at the
host-API boundary, with this paper’s three layers proving containment ahead of the gate.



                                                  17
Supply-chain attestation (Sigstore, Supply-Chain Levels for Software Artefacts (SLSA),
in-toto, The Update Framework (TUF)). Sigstore [25], SLSA [36], in-toto [52], and TUF
[45] are the modern stack for software supply-chain integrity: they prove an artefact was built by a
particular pipeline from a particular source and was not tampered with in transit. None of them
claims anything about behaviour: a SLSA-Level-3 build of a malicious skill is equally well-attested as
a SLSA-Level-3 build of a benign one. Our proof-carrying skill bundle (Section 8) is the behavioural
complement: same Ed25519 signing primitives, same chain-of-custody discipline, but the attestation
binds soundness verdicts (Method A’s E(p)b   ⊆ D, Method B’s typed dispatch, Method C’s BMC
unsat), not build provenance. Both layers are needed; we add the one that the supply-chain stack
does not address.

Empirical agent-safety benchmarks (AgentHarm, AgentBench, AgentPoison). [2] at-
tacks deployed agents with malicious-task harnesses; [12] demonstrates poisoning attacks. These
are essential pressure tests — the parent paper’s adversarial- ensemble evaluation [29, §6] is in this
tradition — but they are tests, not proofs: a benchmark gives a falsification rate, not a soundness
argument. The composition is the right one (this paper for soundness, the empirical work for
aliveness-of-the-defence under realistic adversarial pressure), and we explicitly do not claim our
methods replace empirical evaluation. Conversely, no amount of empirical testing produces a
formal-level certificate.

LLM-side training-time safety (Constitutional AI, Reinforcement Learning from Human
Feedback (RLHF) guard models, jailbreak-robustness research). Constitutional AI [6],
RLHF, instruction-tuning, and the broader alignment-via-training programme reduce the rate at
which a deployed LLM emits dangerous outputs by shaping the model itself. SmoothLLM [42]
reduces jailbreak sensitivity through randomised smoothing. Both are statistical floors, not formal
containment proofs: they lower P [dangerous output], but P > 0 persists at any non-trivial scale.
This work is orthogonal: we treat the LLM as a non-deterministic adversary regardless of its training,
and prove containment at the dispatch boundary below the model. The two layers stack additively
— a guard-model-tuned LLM running inside a Method-B-typed dispatcher leaks no more than the
log2 (|D| + 1)-bit capacity bound regardless of how the model was trained.

LLM-side formal verification (Dong et al., probabilistic model checking). [17] formalises
portions of LLM behaviour as probabilistic transducers; PRISM [22] and the broader probabilistic-
model- checking community [7] give tractable algorithms for verifying expected-case properties of
stochastic systems. This direction could in principle replace Method B’s non-deterministic-adversary
assumption with an expected-case bound on LLM-emitted envelopes. We did not pursue it because
(i) it requires a faithful probabilistic model of the deployed LLM, which closed-weights models do not
expose, and (ii) operator-side accountability under capability containment is already the strongest
property the parent paper’s threat model needs. Probabilistic-model-checking guarantees would
be a complementary upgrade for deployments where the deployed LLM is open-weights and the
decoding distribution is known.

Capability sandboxing at the platform level (the WebAssembly System Interface
(WASI), Wasmtime, gVisor). WASI [10, 55] and operating-system-level sandboxes (gVisor,
Firejail, browser tabs) restrict a process’s access to system resources at the kernel / runtime boundary.
This is the abstraction layer below ours: a script-side capability fs.write.irrev ultimately bottoms
out in a syscall the sandbox either permits or denies. Platform-level sandboxes are broader (any


                                                   18
process, not just skills) and more battle-tested (decades of deployment), but they cannot tell whether
the syscall the process wants to issue corresponds to the manifest the operator approved. We work
above the sandbox: the manifest is enforced before the syscall is even attempted, and the sandbox
is the next layer of defence in the parent paper’s defence-in-depth posture.

Skill-marketplace governance (Claude Skills, Generative Pre-trained Transformer (GPT)
Store, plugin reviews). Anthropic’s Claude Skills [3] and OpenAI’s GPT Store [38] are the
deployed skill-marketplace ecosystems, with vendor-curated review for publication. Curation catches
obvious abuse but is human-bound: it does not scale to per-skill formal verification, does not attest
to behavioural properties beyond the human reviewer’s judgement, and does not survive a skill
update without re-review. Our contribution is the format the marketplace’s curation can demand
of submissions: a proof-carrying bundle whose signed attestations the marketplace runtime can
re-check on every load. The two compose — human curation for policy questions (“should this skill
exist?”) and machine verification for soundness questions (“does the skill stay inside its declared
caps?”).

Summary of the comparison. Across the eight categories, our position is consistent: this paper
occupies a slot none of the incumbents currently fills (mechanically checkable capability-containment
proofs at the skill-manifest level), and every neighbouring category contributes a guarantee we
do not. Schema validation, supply-chain provenance, runtime authorisation, empirical adversarial
pressure, training-time alignment, probabilistic LLM verification, platform-level sandboxing, and
human marketplace curation are all real and useful. We do not aim to displace any of them; we
aim to add the layer they each leave unaddressed, and the proof-carrying bundle of Section 8 is the
integration surface where the layer attaches to the rest of the stack.

10.2    The cost of not adopting this work
A fair reader’s question after the previous subsection is not “is the SOTA inadequate?” — there
is no shortage of useful safety work in the categories above — but “what concretely happens to a
deployment that skips this layer?”. The answer matters because “skip and revisit later” is the path
of least resistance for most organisations: regulatory deadlines look distant, marketplaces are still
curated by humans, incidents have not yet hit the reader’s shop. We make the costs explicit so the
deferral is at least a priced one.

Compliance and regulatory exposure. The next-generation artificial-intelligence (AI) gov-
ernance frameworks already in force or in active rule-making converge on the same evidentiary
requirement: an auditor must be able to verify, mechanically and reproducibly, that a deployed
agent’s behaviour is bounded by its declared specification. Headline frameworks for the reader
unfamiliar with the regulatory landscape:
  • European Union (EU) AI Act (Regulation (EU) 2024/1689). Articles 9, 13, 15, and 16 require,
    for high-risk AI systems, a documented risk-management system, traceability of decisions,
    “appropriate” robustness measures, and post-market monitoring. Compliance dates begin in
    2026 and tier through 2027.
  • Network and Information Security 2 (NIS2) Directive (Directive (EU) 2022/2555). The
    successor to the original 2016 Network and Information Security Directive (NIS1) extends
    cybersecurity due-diligence obligations into AI-mediated services and assigns personal liability
    to corporate management for compliance failure.

                                                 19
  • National Institute of Standards and Technology (NIST) AI Risk Management Framework (AI
    RMF 1.0, 2023). The Govern / Map / Measure / Manage cycle names “verification and
    validation” as a measurement sub-category, expected by federal procurement to be instantiated
    by deployed AI vendors.

  • Federal Risk and Authorization Management Program (FedRAMP) and the federal AI overlays
    of NIST Special Publication (SP) 800-53 Rev 5 (control families: Access Control (AC),
    Audit and Accountability (AU), System and Information Integrity (SI), Supply-Chain Risk
    Management (SR), Risk Assessment (RA), Personally Identifiable Information Processing and
    Transparency (PT)). Mandatory for any vendor selling to United States federal agencies; the
    AC and AU families overlap directly with the parent paper’s gate and audit primitives.

  • International Organization for Standardization / International Electrotechnical Commission
    (ISO/IEC) 42001 (AI Management Systems, 2023) and ISO/IEC 23894 (AI risk management).
    The international counterparts to NIST AI RMF; large multinationals will be audited against
    them whether or not their home jurisdiction requires it.

  • Sector-specific: the Health Insurance Portability and Accountability Act (HIPAA) (United
    States Code of Federal Regulations (CFR) Title 45, Parts 160, 164), the Payment Card
    Industry Data Security Standard (PCI DSS) 4.0, and the upcoming European Health Data
    Space (EHDS) regulation constrain what an agent operating in healthcare or payments may
    legitimately do; an unbounded agent trivially produces violations.

None of these frameworks names “Method A static analysis” or “refinement-typed dispatch” specif-
ically. They name evidence categories — traceability, repeatable validation, reproducibility of
decisions, technical measures appropriate to risk — and the deployment whose answer is “we have
an LLM-driven agent but no formal proof of behavioural containment” pays the audit cost manually,
for every cycle, in expert-witness-grade documentation. The proof-carrying bundle of Section 8 is
exactly the artefact those frameworks ask for; without it, every audit is a paper exercise re-derived
from scratch by people whose hourly rate is high.

Marketplace and platform liability. Skill marketplaces [3, 38] bet on human review at scale.
A single missed review where a published skill performs out-of-manifest behaviour exposes the
platform to regulatory investigation, vendor-contract clawback, and class-action litigation under
the consumer-protection regime of the relevant jurisdiction. Without a per-skill containment proof
attached to each load, the platform cannot honestly tell its insurer or its auditor that it has done
more than spot-check submissions. The cost rises non-linearly with marketplace size: 100 skills can
be reviewed by hand, 100 000 cannot.

Insurance and procurement friction. Cyber-insurance underwriters in 2025–2026 increasingly
carve out “AI-related incidents” from default policies unless the insured can demonstrate “reasonable
technical measures”. A signed proof-carrying bundle is the kind of demonstrable artefact underwriters
can attach a discount to; its absence reverts the deployment to the most expensive policy tier or to
no coverage at all. On the procurement side, large enterprise buyers — public sector especially —
are already requiring an “AI safety attestation” in their RFPs. The vendor whose answer is “we
have human review” loses, on price and on signal, to the vendor whose answer is “here is the proof,
re-checkable by your runtime in under a second”.




                                                 20
Incident response and forensic cost. When an agent does something it should not have, the
parent paper’s audit log tells you what happened. Without the biconditional check verified sound,
the audit log does not tell you whether what happened was permissible under the manifest the
operator approved. The forensic team reconstructs that property by hand — cross-referencing trace
against policy, envelope by envelope — which costs days of specialist time per incident, and that’s
before the regulator and the insurer’s lawyers ask for the same reconstruction independently. With
the biconditional pinned ahead of deployment (the parent paper) and proven sound by Method C
(this paper), the reconstruction is free: every session either passes the runtime check or carries a
precise counter-example pinned to a specific envelope, and the forensic deliverable writes itself.

Innovation throttling from over-restriction. Without mechanical containment proofs, the
rational compliance posture is to gate everything through human-in-the-loop review and to refuse
capabilities the risk team cannot personally evaluate. Formal verification flips the default: capabilities
the manifest declares and the bundle attests can be relaxed from HITL safely, because the runtime
carries the proof that no out-of-manifest envelope is reachable. The cost of inaction is not only
incident exposure — it is the systemic over-restriction that makes the deployed agent useless for the
workflows that justified building it. The deployment ends up either dangerous (no gates) or useless
(gates everywhere); formal verification is the only path to “safe and useful”.

Adversarial dwell time. A skill with malicious script-side behaviour but a benign-looking
manifest survives schema validation, supply-chain attestation, and runtime gating until the malicious
code is actually executed in production. Method A’s static-analysis layer catches the divergence at
load time: the manifest declares net.egress only, the script-side analyser reports fs.write.irrev
as well, the bundle verdict resolves to contained=false, the load fails. Without Method A this
divergence is invisible until the runtime gate fires on the specific instance, by which point the dwell
window may have been weeks. Each week of attacker dwell maps to a known dollar cost in the
incident-response literature (IBM Cost-of-a-Data-Breach reports place median dwell cost in the high
six figures per week for enterprise contexts).

Cross-vendor lock-in. Without a common, mechanically checkable verification format, each
platform’s safety story is that platform’s intellectual property. An organisation that builds against
Anthropic’s Skills today, and against Anthropic’s safety review process, cannot port that posture
to OpenAI’s GPT Store or to a self-hosted runtime without re-deriving every attestation from
scratch. A proof-carrying bundle whose verifier is a 350-line JavaScript (JS) module (Section 8.4) is
portable by construction; a vendor’s internal review checklist is not. The cost of not adopting an
open verification format is paid as a vendor-switching tax in perpetuity.

Honest qualifier. Adopting this paper’s three methods does not eliminate compliance-paperwork
cost — a healthcare deployment subject to HIPAA still needs a privacy officer, a FedRAMP
submission still needs a System Security Plan package, the bundle becomes one of the evidence
artefacts rather than the whole package. For that category the framing is “verification turns a
recurring manual cost into a one-time engineering cost,” the same trade mature organisations already
recognise from the migration of manual testing to continuous integration. But the next subsection
names a different category of cost: the vulnerability classes the methods categorically remove from
the deployment, where the right framing is not “manual to mechanical” but “the attack does not
happen.”



                                                   21
10.3    The attack classes this work categorically eliminates
A complementary accounting to the previous subsection: under the methods’ soundness assumptions
(Method A’s analyser is sound for the script-side language; Method C’s bound covers the runtime’s
transaction-buffer horizon; the runtime is correct), several attack classes do not become easier to
find, they fail to reach production at all. We list them with explicit anchors to the Open Worldwide
Application Security Project (OWASP) LLM Top 10 (2025) [39], MITRE’s Adversarial Threat
Landscape for Artificial-Intelligence Systems (ATLAS) knowledge base [34], and the parent paper’s
threat model [29, §2], so the security reader can map each elimination to the entry on the team’s
existing risk register.

Out-of-manifest tool dispatch — eliminated (Method B). LLM06 Excessive Agency (an
agent takes broader action than the operator authorised) is the headline elimination. Method B’s
refinement-typed dispatch makes it a compile-time error to call dispatchM with an envelope whose
capability is outside M.caps. Under the type-checker’s soundness, no execution path from envelope
receipt to host API call exists for an out-of-manifest envelope. The whole class of “LLM was
prompt-injected into calling pay() when its skill only declared web_search” is gone — not detected
and denied at the gate, but typed-out before the gate is even consulted. LLM01 Prompt Injection
retains its presence on the LLM-side input distribution, but the attacker-relevant leg (“→ harmful
action”) is severed: even an LLM that has been fully compromised by an adversarial prompt cannot
dispatch an envelope outside the manifest’s declared set. The DPI bound of Equation (7) pins the
residual leakage at log2 (|D| + 1) bits per envelope — a categorical upper bound, not an empirical
observation.

Script-side capability creep — eliminated (Method A). The classical attack pattern
“ship a skill whose declared manifest is benign but whose script-side scripts call os.remove,
subprocess.Popen, or requests.get on hosts the manifest does not declare” fails at load time un-
der Method A. The static analyser reports E(p)
                                            b    ̸⊆ CD , the bundle verifier returns contained=false,
the runtime declines admission. There is no production execution and therefore no post-incident
dwell window for this divergence to exploit. This maps to ATLAS technique AML.T0051 (Adversarial
Machine Learning (AML) catalog ID for “LLM Plugin Compromise”) and the parent paper’s residual
class RS (script-side capability over-reach). Insider threats and supply-chain skill-tampering both
subsume here: the attacker can falsely declare a manifest, but then the manifest itself is the
smoking-gun signed artefact in the audit trail.

Audit-log-bypass attacks — eliminated up to bound (Method C plus runtime layer).
The attack class “world-state changed but the audit log shows nothing” is exactly the biconditional
violation Method C’s BMC searches for. For sessions of length ≤ Kmax , an unsat verdict from the
solver proves no such session exists. Sessions longer than Kmax are caught at flush by the runtime
biconditional itself, the parent paper’s existing primitive. The composition is sound for unbounded
sessions: any counter-example small enough to fit in the buffer’s horizon is found by the solver
pre-deployment; any counter-example larger than the horizon is found by the runtime at the next
flush. “Stealth side-effect with no audit record” is therefore a categorically closed attack class, not a
probabilistically reduced one.

Post-bundle evidence tampering — eliminated (Method B + bundle re-checker). The
runtime’s bundle re-checker (Section 8) re-runs all three methods on the live manifest and compares
hashes against the bundle’s signed attestation. An attacker who modifies any evidence file after

                                                   22
signing is caught either by the Ed25519-signature check, by the canonical-hash mismatch, or by
the method-A reproduction step — the bundle has three independent integrity gates. The “we
substituted the proof” attack class does not survive a single admission cycle.

Skill drift between sign and load — eliminated (Method A re-run). A common production
attack vector is “the bundle attests to commit C1 , but the deployed tree at load time is C2 with extra
tooling spliced in.” The re-checker re-runs Method A on the live source, computes a fresh E blive (p), and
compares it to the bundle’s cached E  bcached (p). Any non-trivial drift returns method-A-cache-miss
as a verification reason and the load fails. “Quick fix shipped past the proof” is categorically blocked.

Cross-skill capability leakage — eliminated. Each loaded skill is verified against its own
manifest; capability authority cannot transit between skills at the dispatch boundary. The classical
multi-tenant attack “skill A cannot pay but skill B can; cooperate to exfiltrate” fails because both
skills’ dispatch is type-bound to its own manifest, and inter-skill communication (if the host even
allows it) carries no implicit capability transfer. This is the object-capability discipline of [33, 51]
applied at the skill-manifest level.

Substantially reduced (not zero). Three remaining classes are reduced by a large multiplier
but not to zero:
   • Supply-chain skill injection (LLM03 Supply Chain) is reduced to the residual where the attacker
     controls the manifest and the signing key and the script-side simultaneously. Composed with
     Sigstore [25] / SLSA [36] the residual narrows further to the keyholder-compromise case, which
     is the same residual that all signed-artefact ecosystems face.

   • Sensitive-information disclosure via tool calls (LLM02 ) is bounded by the per-envelope channel
     capacity log2 (|D| + 1) derived in Equation (7). Tightening below that bound requires either
     argument-level summarisation of the abstract envelope domain (Method A’s V ♯ already
     does this for paths and host patterns) or explicit redaction at the dispatch boundary, both
     engineering choices on top of the soundness floor.

   • Insider malicious-skill publication is reduced to the case where the insider’s manifest itself
     is the weapon. That case is loud: the insider has signed a manifest declaring exactly the
     capabilities the misbehaving skill needs, which is forensic gold rather than the diffuse “some
     script somewhere did something” that script-side creep produces today.

The honest scope. The eliminations above hold under the soundness assumptions named in
the section opener. The methods do not eliminate model denial of service (LLM10 Unbounded
Consumption), training-data poisoning (LLM04 ), misinformation generated within the dispatch
budget (LLM09 ), or model-weight theft (the parent paper’s classification primitive addresses only
the data side). The Chief Information Security Officer (CISO) who wants to retire risk-register
entries on the back of Section 10.3 should retire exactly the entries the soundness theorems cover —
and re-list the others under “additional layers of defence required.”

10.4    Open problems
The LLM remains unverified. Method B treats the LLM-side as a non-deterministic adversary;
this is the strongest soundness posture available to a verification method that does not depend
on LLM internals. We are aware of probabilistic-transducer formalisations of LLMs [17] and

                                                   23
probabilistic model checkers [7, 22] that could lift the guarantees from worst-case to expected-case
under specific decoding- distribution assumptions. We do not pursue that direction here because
operator-side accountability under capability containment is already the strongest property the
parent paper’s threat model needs; expected-case guarantees about the LLM are an additional
reassurance, not a substitute.

Adversarial-ensemble complementarity. The parent paper’s adversarial-ensemble evaluation
[29, §6] empirically falsifies a candidate verification procedure at given sample size. The three-layer
discipline gives a sound proof for the script + dispatch portion; the adversarial-ensemble exercises
the runtime layer + the LLM-side under realistic provocations. The two are complementary: an
empirical test cannot replace a soundness argument, and a soundness argument cannot replace
empirical adversarial pressure on the gate.

Runtime instrumentation cost. A reasonable concern is that requiring formal on every
skill before the runtime relaxes HITL is operationally heavier than the parent paper’s tested
default. We expect the levels to co-exist: most skills will sit at tested; the small number of
skills carrying high-impact capabilities (pay, mutate.schema, spawn.proc) are the ones that justify
the formal-verification cost. The schema admits this gradient [29, §3.1]; this paper’s three-layer
discipline is the upgrade path for the skills where it pays.

What about formally-verified runtimes? We have assumed R is correct. A runtime carrying
its own formal-verification certificate (a CompCert-compiled [24] core, an F⋆ -verified dispatch [50],
etc.) lifts the trusted base further. Engineering this is straightforward but labour-heavy; the parent
paper’s reference implementation [28] does not yet include it. We treat it as an orthogonal upgrade.

Skill side-channels. Capability containment is a property over the typed dispatch interface.
Side-channels (timing, power, network metadata) are out of scope; the parent paper’s classification
primitive and DLP scanner address the most common of these (data-exfiltration through plain-
message channels), but the broader side-channel question is orthogonal and well-studied [44].


11     Related work
Capability containment and effect systems. The basic idea — type the dispatch surface so
that out-of-bound effects do not type-check — is the effect-system tradition [27, 44] adapted to agent-
emitted envelopes. We owe the lattice formulation of effects to [16, 54], and the refinement-type-side
instantiation to [43, 50, 53]. The object-capability literature [33, 51] provides the design discipline
(capabilities are unforgeable references; loaded skills are bootstrap-frozen capability bundles); this
paper applies the discipline at the skill-manifest level rather than the process/object level.

Static analysis and abstract interpretation. Method A is straight-line abstract interpretation
[13, 21] over the parent paper’s capability vocabulary. The novelty is the per-language summary
table that maps language- standard-library calls to capability tokens; this is the engineering effort,
not the theory.

Bounded model checking. Method C uses [9, 15] unmodified. The choice of bound Kmax
exploits the runtime’s transaction-buffer horizon [29, §4.1]; this is the contribution that distinguishes
our use of BMC from generic model checking of arbitrary protocols.

                                                   24
Proof-carrying code. The bundle structure of Section 8 is the proof-carrying-code idiom [5, 24, 35]
lifted from native binaries to skill artefacts. The novelty is the re-check protocol’s split between
trusted (signer attestation, trust-root resolution) and re-runnable (the analyser, the type checker,
the SMT solver) components; the consumer trusts the small base and re-discharges the large work.

LLM-agent verification. A recent line of work [2, 12, 18, 34, 39] attacks the agent empirically;
[17, 42] formalises parts of the LLM. We complement that work by leaving the LLM unverified and
instead verifying the runtime’s containment of the LLM’s freedom.

Runtime verification. The fourth layer (the parent paper’s biconditional, fired at flush) is a
runtime-verification (RV) monitor in the sense of [8]. The composition of static + type + SMT
+ RV is the standard “four-layered” approach to verification under partial models; our specific
partition was chosen so that each layer’s incompleteness is exactly the next layer’s soundness scope.


12     Conclusion
The companion paper’s verification lattice [29, §3] placed formal at the top with no construction.
We have given one. The construction is three composable methods that already have well-engineered
implementations (Semgrep / CodeQL for Method A; refinement-type checkers like Liquid Haskell, F⋆ ,
or even disciplined TypeScript for Method B; Z3 for Method C), glued together by a proof-carrying
skill artefact the runtime mechanically re-discharges at bootstrap, closing the residual surface the
static layers cannot reach with the parent paper’s already- deployed runtime biconditional.
    The cost is real but bounded: per-skill, a CI step measured in seconds for the static and SMT
layers, and a one-time type-discipline tightening for the dispatch boundary. The benefit is real
and large: a skill at formal carries a proof, re-checkable without trusting the producer, that its
observable side-effects are contained in its declared capability set under the runtime’s threat model.
The runtime can stop asking HITL on its in-manifest calls; the operator can audit the bundle
without re-running the analyser; the residual is named and bounded.
    The methods do not require operators to write new tools, replace their stack, or train new staff
in formal methods. They require exactly the engineering work the parent paper’s SKILL.md already
implies: name the capabilities, type the dispatch, and let standard tools do the rest.


References
 [1] Amazon Web Services. Cedar policy language. https://www.cedarpolicy.com/, 2024.
     Formally-verified policy language for runtime authorisation; paired with a Lean/Rust ver-
     ification effort.
 [2] Maksym Andriushchenko, Alexandra Souly, Mateusz Dziemian, Derek Duenas, Maxwell Lin,
     Justin Wang, Dan Hendrycks, Andy Bailey, Yinzhi Kang, Kellin Pelrine, Anton Albert, Fabien
     Roger, Tim Riedel, Alexandre Lacoste, Anastasiia Skripko, Yixin Wang, Jiaxin Ji, Christopher
     Berner, Mary Phuong, Hongseok Liu, Iain Murray, Jamie Hayes, Helen Toner, David Krueger,
     and Florian Kellěr. AgentHarm: A benchmark for measuring harmfulness of LLM agents. In
     Proceedings of ICLR, 2025.
 [3] Anthropic. Claude Skills: User-defined capabilities for Claude. https://www.anthropic.
     com/news/skills, 2024. Production skill artefact format with SKILL.md convention; human
     curation, no formal-property attestation.

                                                 25
 [4] Anthropic. Model context protocol (MCP) specification. https://modelcontextprotocol.io/,
     2025. Open protocol for connecting AI assistants to tools, data sources, and skill-like artefacts.

 [5] Andrew W. Appel. Foundational proof-carrying code. In Proceedings of LICS, 2001.

 [6] Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones,
     Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson,
     Christopher Olah, Danny Hernandez, Dawn Drain, et al. Constitutional AI: Harmlessness
     from AI feedback. In arXiv:2212.08073, 2022. Training-time alignment via principle-derived
     self-critique; a statistical safety floor, orthogonal to runtime containment proofs.

 [7] Christel Baier, Luca de Alfaro, Vojtěch Forejt, and Marta Kwiatkowska. Model checking
     probabilistic systems. Handbook of Model Checking, Chapter 28, 2018.

 [8] Ezio Bartocci, Yliès Falcone, Adrian Francalanza, and Giles Reger. Introduction to runtime
     verification. Lectures on Runtime Verification, LNCS 10457, 2018.

 [9] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan Zhu. Symbolic model
     checking without BDDs. Proceedings of TACAS, 1999.

[10] Bytecode Alliance. Wasmtime: A standalone WebAssembly runtime with capability-based
     sandboxing. In Bytecode Alliance technical report, 2024. https://wasmtime.dev/.

[11] Cristian Cadar, Daniel Dunbar, and Dawson R. Engler. KLEE: Unassisted and automatic
     generation of high-coverage tests for complex systems programs. Proceedings of OSDI, 2008.

[12] Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, and Bo Li. AgentPoison: Red-teaming
     LLM agents via poisoning memory or knowledge bases. arXiv preprint arXiv:2407.12784, 2025.

[13] Patrick Cousot and Radhia Cousot. Abstract interpretation: a unified lattice model for static
     analysis of programs by construction or approximation of fixpoints. In Proceedings of POPL,
     1977.

[14] Thomas M. Cover and Joy A. Thomas. Elements of Information Theory. Wiley-Interscience,
     2nd edition, 2006.

[15] Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In Proceedings of
     TACAS, 2008.

[16] Dorothy E. Denning. A lattice model of secure information flow. volume 19, pages 236–243,
     1976.

[17] Yiyang Dong, Vicente Calvo Quintela, Yu Tang, Jiaxiong Liu, Yuhua Cao, and Yang Liu.
     Formalizing the LLM as a probabilistic transducer for verification under uncertain inputs. In
     Proceedings of the 1st International Workshop on Formal Methods for LLM-based Systems,
     2025.

[18] Emilio Ferrara. GenAI against humanity: Nefarious applications of generative artificial
     intelligence and large language models. Journal of Computational Social Science, 7:549–569,
     2024.

[19] GitHub. CodeQL: Variant analysis for software security, 2025. https://codeql.github.com/.



                                                 26
[20] Patrice Godefroid, Nils Klarlund, and Koushik Sen. DART: Directed automated random testing.
     Proceedings of PLDI, 2005.

[21] Gary A. Kildall. A unified approach to global program optimization. In Proceedings of POPL,
     1973.

[22] Marta Kwiatkowska, Gethin Norman, and David Parker. PRISM 4.0: Verification of probabilistic
     real-time systems. In Proceedings of CAV, 2011.

[23] LangChain, Inc. LangChain: Build context-aware reasoning applications. https://www.
     langchain.com/, 2024. Agent-orchestration framework with tool integration; no static-analysis
     or proof layer.

[24] Xavier Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):
     107–115, 2009.

[25] Linux Foundation, Sigstore Project. Sigstore: A new standard for signing, verifying, and
     protecting software. https://www.sigstore.dev/, 2024. Keyless signing infrastructure for
     software artefacts; attests provenance, not behaviour.

[26] Luísa Lourenço and Luís Caires. Type inference for refinements and effects. Proceedings of
     POPL, 2015.

[27] John M. Lucassen and David K. Gifford. Polymorphic effect systems. Proceedings of POPL,
     1988.

[28] Alfredo Metere. enclawed: A configurable, sector-neutral hardening framework for personal-class
     ai assistant gateways, 2026. Open-source reference implementation.
     https://github.com/metereconsulting/enclawed.

[29] Alfredo Metere. Skills as verifiable artifacts: A trust schema and a biconditional correctness
     criterion for human-in-the-loop agent runtimes, 2026. URL https://arxiv.org/pdf/2605.
     00424v1. Companion paper.

[30] Metere Consulting, LLC. enclawed project page. https://www.enclawed.com/, 2026. Docu-
     mentation, downloads, and the open-source distribution of the enclawed framework.

[31] Microsoft. Pyright: Static type checker for Python, 2025. https://github.com/microsoft/
     pyright.

[32] Microsoft Research. AutoGen: Multi-agent conversation framework. https://microsoft.
     github.io/autogen/, 2024. Multi-agent orchestration; tool calls go through agent conversa-
     tions, no formal-property attestation.

[33] Mark S. Miller. Robust composition: Towards a unified approach to access control and concur-
     rency control. PhD thesis, Johns Hopkins University, 2006.

[34] MITRE Corporation. ATLAS: Adversarial threat landscape for ai systems, 2024. https:
     //atlas.mitre.org/.

[35] George C. Necula. Proof-carrying code. In Proceedings of POPL, 1997.




                                                27
[36] Open Source Security Foundation. Supply-chain levels for software artefacts (SLSA). https:
     //slsa.dev/, 2024. Tiered supply-chain integrity framework (Levels 0–3); a build-process
     attestation, not a behavioural one.

[37] OpenAI. Function calling and tool use. https://platform.openai.com/docs/guides/
     function-calling, 2024. JSON-Schema-typed function declarations for LLM tool invocation;
     the closest production-deployed peer to skill manifests.

[38] OpenAI. GPTs and the GPT store. https://openai.com/blog/introducing-gpts, 2024.
     Custom-GPT marketplace; review-based governance, no formal containment proof.

[39] OWASP Foundation. LLM AI cybersecurity & governance checklist (top 10). OWASP, 2024.

[40] r2c. Semgrep: Lightweight static analysis for many languages, 2025. https://semgrep.dev/.

[41] Hannes Risken. The Fokker–Planck Equation: Methods of Solution and Applications. Springer
     Series in Synergetics. Springer, 2nd edition, 1996.

[42] Alexander Robey, Eric Wong, Hamed Hassani, and George J. Pappas. SmoothLLM: Defending
     large language models against jailbreaking attacks. In Proceedings of NeurIPS, 2023.

[43] Patrick M. Rondon, Ming Kawaguchi, and Ranjit Jhala. Liquid types. In Proceedings of PLDI,
     2008.

[44] Andrei Sabelfeld and Andrew C. Myers. Language-based information-flow security. IEEE
     Journal on Selected Areas in Communications, 21(1):5–19, 2003.

[45] Justin Samuel and Justin Cappos. The update framework (TUF) specification, 2024. Specifica-
     tion version 1.0.x.

[46] Tim Sandall. Open policy agent (OPA): Policy as code. In Proceedings of KubeCon / Cloud-
     Native Computing Foundation, 2018. https://www.openpolicyagent.org/.

[47] Claude E. Shannon. A mathematical theory of communication. Bell System Technical Journal,
     27(3):379–423, 623–656, 1948.

[48] Lau Skorstengaard, Dominique Devriese, and Lars Birkedal. Reasoning about a machine with
     local capabilities. In Proceedings of POPL, 2018.

[49] Steven H. Strogatz. Nonlinear Dynamics and Chaos: With Applications to Physics, Biology,
     Chemistry, and Engineering. Westview Press, 2nd edition, 2014.

[50] Nikhil Swamy, Juan Chen, Cédric Fournet, Pierre-Yves Strub, Karthikeyan Bhargavan, and
     Jean Yang. Secure distributed programming with value-dependent types. In Proceedings of
     ICFP, 2011.

[51] The Object-Capability Wiki. The object-capability discipline, 2025. http://erights.org/
     elib/capability/ode/index.html.

[52] Santiago Torres-Arias, Hammad Afzali, Trishank Karthik Kuppusamy, Reza Curtmola, and
     Justin Cappos. in-toto: Providing farm-to-table guarantees for bits and bytes. https://
     in-toto.io/, 2019. Provenance-tracking framework underlying SLSA.



                                              28
[53] Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton Jones.
     Refinement types for Haskell. Proceedings of ICFP, 2014.

[54] Dennis Volpano, Geoffrey Smith, and Cynthia Irvine. A sound type system for secure flow
     analysis. Journal of Computer Security, 4(2–3):167–187, 1996.

[55] WebAssembly Community Group. The WebAssembly system interface (WASI), 2024. https:
     //wasi.dev/.




                                            29
