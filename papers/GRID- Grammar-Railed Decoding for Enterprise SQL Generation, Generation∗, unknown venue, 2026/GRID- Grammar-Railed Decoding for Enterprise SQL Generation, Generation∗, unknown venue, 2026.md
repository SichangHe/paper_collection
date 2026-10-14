                                          GRID: Grammar-Railed Decoding for Enterprise SQL
                                                           Generation∗
                                                                                           Mohsen Arjmandi
                                                                                             evolutionID GmbH
                                                                                    mohsen.arjmandi@evolutionid.com

                                                                                                 July 2026


                                                                                                  Abstract
                                                    Large language models can write SQL, but enterprise deployment demands more than plausible
                                                text: outputs must be syntactically valid, must respect per-role and per-schema policy, must come
arXiv:2607.11951v1 [cs.AI] 11 Jul 2026




                                                with provable—not best-effort—guarantees, must not slow down as generations grow, and must leave a
                                                compliance-grade record of every decision. We present GRID (Grammar-Railed Decoding), a grammar-
                                                constrained decoding engine that keys exact next-token masks on parser configurations (lexer scan state
                                                × LALR(1) stack) rather than on token sequences, uses the incrementally advanced LALR(1) parser itself
                                                as a viable-prefix oracle, and bridges LLM tokens to grammar terminals through a byte-level trie walk
                                                with a context-independent/context-dependent split that makes cache-key soundness hold by construction.
                                                Role-based access control is compiled into the language: role projections subset the grammar’s productions
                                                and schema lexicons restrict identifier terminals, so forbidden verbs and identifiers are unreachable at
                                                mask level. Four guarantees—soundness, completeness, termination, and near-constant per-token cost
                                                (requirement R)—are stated with explicit preconditions and each is paired with the test or benchmark
                                                that verifies it. Rust kernels bring the warm serving step to 1.33 µs per request and the per-token mask
                                                to a 3.6–6.7 µs median—ahead of llguidance at both p50 and p90 on both benchmarked tokenizers, with
                                                zero false rejects, while llguidance keeps the flattest p99. On a declared H100 SXM5 runner, end-to-end
                                                serving overhead under vLLM is +1.51% time-per-output-token at batch 32 with 27.3 ms cold-schema
                                                specialization; a fresh (never-seen) schema pays ∼0.7 ms first-token latency and then decodes at 1.00×
                                                warm speed. A v7 kernel that keeps the entire cold mask miss in Rust (fused walk→blob→register,
                                                one GIL-released call) holds the warm co-tenants’ worst engine step to 15.3 ms on real hardware; the
                                                one residual cost—a transient co-batched TPOT slowdown (∼34%) during the fresh schema’s ∼0.66 s
                                                specialization window—is genuine host CPU/memory-bandwidth contention between the cold walk and
                                                the engine forward loop (it shrinks as walk threads grow), a compute-isolation trade-off noted as future
                                                work rather than a defect. Per-token guard cost is position-flat (slope ≈ 0 at n=16,000, all nesting depths).
                                                On Spider, constrained decoding is worth +13 execution-accuracy points at 0.5B; at 7B the mask alone
                                                is worth ∼+1 point, and one checker-guided repair pass over the provably mask-unenforceable residue
                                                (column-level policy) lifts execution to 94.5% and EX to +2.3 over unconstrained. A hash-chained per-
                                                token audit trail replays bit-identically (1,000 generations across a cache-namespace rollover; 100% tamper
                                                detection). We state honestly what the mask cannot do—distribution faithfulness, column-level RBAC,
                                                non-LALR(1) languages—and where measured cost remains (cold trie walks; the serving cold-window
                                                compute contention; one characterized engine-side artifact exogenous to GRID).


                                         1      Introduction
                                         We are concerned with generating SQL (and, more generally, sentences of any LALR(1)-parsable language)
                                         from a large language model under the operating conditions of an enterprise CRUD/RBAC deployment. In
                                         that setting, “the model usually writes valid SQL” is not an acceptable contract. Six problems, each of which
                                         shapes the design, must be solved simultaneously:
                                             ∗ A condensed version of this paper is under review at KDD 2027.




                                                                                                      1
P1. Validity and policy, jointly. Output must parse under the SQL dialect and comply with per-role
    policy (allowed verbs, banned clauses) and per-schema vocabulary (only real tables and columns).
    Policy is not a post-hoc filter: a role that may only select must be unable to emit delete at all, and
    identifiers must be schema-valid by construction.
P2. Provable guarantees. Soundness (never emit a token that leaves the language’s prefix set), complete-
    ness (never block a token that could still lead to a valid sentence), and termination (every stop is a
    complete sentence) must be theorems with explicit preconditions, each paired with the test that verifies
    it—not emergent properties of a test suite.
P3. Flat per-token cost (requirement R). Guard-rail cost per token must be amortized O(1) in the
    current output length n (worst case bounded by grammar/nesting constants, never by n), so total guard
    cost is O(n) over a generation. A guard whose per-token cost grows with context is unusable for long
    generations; §8.2 shows a 2023-era system for which per-token overhead grows by ∼1.19 ms per position.
P4. A replayable audit trail. In a compliance setting, “what was the model allowed to say at step t, and
    why?” must be answerable after the fact: a hash-chained, per-token record of permit/block decisions,
    replayable bit-identically against versioned grammar artifacts.
P5. Serving reality. Production decoding is batched, grammars are heterogeneous across co-batched
    requests, and new schemas arrive while a hot batch is running. The guard must overlap mask
    computation with the GPU forward pass, never stall co-batched requests on one request’s cold miss
    (the cold-schema-into-hot-batch problem), and never substitute an approximate mask under deadline
    pressure.
P6. An honest boundary for the unenforceable residue. Some policy is provably not enforceable
    by any left-to-right context-free mask—column-level RBAC being the canonical case (Proposition 11).
    The system must name that boundary rather than blur it, enforce it post-parse, and—where a capable
    model is available—convert the named violations into a checker-guided repair loop.

    GRID answers these with one architectural idea and its consequences: key everything on parser configu-
rations. A configuration—the pair of the lexer’s scan state over a partial lexeme and the LALR(1) parser
stack—is exactly the information that determines which continuations are viable. Masks are computed
from configurations, cached under configuration-derived keys whose soundness is a stated obligation (a
Myhill–Nerode-style refinement, §4.3), and audited under a rolling configuration hash. The mask cost
therefore tracks the grammar configuration, not the output position, which is requirement R by construction;
the benchmarks in §8 measure that this holds on real vocabularies at n = 16,384.

Contributions. (1) A formal framework for configuration-keyed constrained decoding: the incremental
LALR(1) parser as a viable-prefix oracle with exact EOS gating under table compression (§3); a byte-level
token↔terminal bridge with a context-independent/context-dependent split that makes cache-key soundness
hold by construction (§4); the cache-key soundness obligation OBL-KEY1 and the identifier composition rule,
with the scanner normal form that maximizes sound cross-request sharing (§4.3). (2) Four guarantees stated
as propositions with explicit preconditions, including the honest negative result that column-level RBAC is
mask-unenforceable (§5). (3) A system realizing the framework—grammar pipeline, Rust kernels (v4→v7,
warm serving step 7.39 → 1.33 µs/request, then a v7 fused cold-miss path), two-tier write-back mask cache,
a serving contract for batched heterogeneous decoding, and a hash-chained audit log (§6)—with worked
examples (§7). (4) A committed benchmark record: per-token mask latency against XGrammar, llguidance,
and Outlines on two tokenizers; requirement-R slope measurements; MaskBench; Spider execution accuracy
with checker-guided repair; and an end-to-end vLLM serving record including a cold-miss stress arm (§8).

Design lineage. The initial patent filing captured an early, partial snapshot of this design (v0.0.5, designed
August 2023): a precomputed validity table over token sequences against a pushdown automaton, with
decode-time logit masking. Planned iteration carried the design forward: v0.0.6 (September 2023) already
outperformed the July-2023 release of guidance on the scaling benchmarks of that era, and v0.0.7 (November
2023)—the system described in this paper, and the line the final patent application followed—replaced


                                                      2
sequence keys with configuration keys and acceptance semantics with prefix viability, added the byte-level
token↔terminal bridge, the write-back cache, RBAC/schema projections, the audit chain, and checker-guided
repair; the work has continued to improve since. Sections 3–4 present the design analysis behind the two
load-bearing revisions. The design drew inspiration from published work—notably Willard and Louf’s Outlines
paper [1], whose finite-state-machine formalization of guided generation this paper deliberately parallels in
register—while GRID’s design and implementation are our own throughout.


2     Preliminaries
Masked decoding. Let V be a tokenizer vocabulary with |V | = N and let Σ be the byte alphabet. An
autoregressive LM defines logits α = LM(s1..t , θ) ∈ RN ; guided generation applies a mask m ∈ {0, 1}N before
sampling, α̃ = m ⊙ α (implemented as an in-place masked_fill_(−∞)), and samples st+1 ∼ Categorical(α̃).
Constructing m at each step is the entire problem: done naively it costs a parse of the whole prefix per
candidate token per step.

Tokens are byte strings. Each token has a canonical spelling bytes : V → Σ∗ (token_bytes): byte-level-
BPE unicode remaps inverted, SentencePiece/BPE space markers normalized to 0x20, byte-fallback literals
<0xNN> mapped to their byte. One definition serves the trie build, the fast path, and the reference oracle.
Distinct token ids may share a spelling (alias classes); masks are over ids, not spellings.

Three grammar layers, one language.
    • L1 (dialect core). A CFG G = (N , T, P, S) whose terminals τ ∈ T carry regular lexeme languages
      Rτ ⊆ Σ∗ , with an ignored subset I ⊆ T (whitespace, comments) that is first-class. Production SQL
      grammars (PostgreSQL, MySQL, SQLite) are LALR(1), so deterministic-PDA coverage suffices. Lexing
      is maximal munch over the union automaton with contextual resolution: a forced emission event
      carries the full candidate terminal set at the longest match and the consumer picks the highest-priority
      parser-viable candidate (this is what lets TABLE_NAME and COLUMN_NAME share one regex, and what
      resolves JSON’s property-key-vs-string overlap with no new mechanism).
    • L2 (role projection). A production subset Prole ⊆ P (verb subsets, clause bans) followed by
      mandatory useless-symbol elimination and a verified L(Grole ) ̸= ∅. Reducedness is load-bearing: without
      it, “non-empty action set ⇒ viable prefix” fails and dead ends return.
    • L3 (schema lexicon). For identifier categories C ⊆ T , finite allow-lists Wc ⊆ Σ∗ realized as lexer
      tries; the lists are generated from the database catalog (information_schema). Precondition, validated
      at guide build rather than assumed: Wc ⊆ Rc for every category (each allowed word must be scannable
      to an accepting state of its terminal).

The constrained language L = L(Grole , schema) is the set of byte strings that lex and parse under the
projected grammar with every category-c lexeme in Wc . Both the policy bundle and the schema snapshot are
fingerprinted, immutable inputs; grammars, tries, and reserve tables are content-addressed artifacts.


3     The viable-prefix oracle
3.1     Design analysis: why sequence keys and acceptance semantics fail
The v0.0.5 design snapshot precomputed an in-memory table tagging LLM token sequences as accepted or
rejected by a pushdown automaton, and masked per step from table lookups. Two observations, made during
the planned design review of that snapshot, force the shape of everything that follows.
Proposition 1 (Sequence-keyed tables scale combinatorially). A total validity table over token sequences of
length ≤ m has Θ(|V |m ) entries. At |V | = 32,768 and m = 3 this is already ≈ 3.3 × 1013 entries (≈ 400 TB
at 12 bytes/entry); at m = 18 it exceeds the number of atoms in the observable universe.



                                                      3
   A “representative subset” of that table is defined by outcome, not by a construction, so it offers no
build recipe. The information the table was trying to enumerate is, however, finitely presentable: by the
viable-prefix property of LR automata [2], the set of viable prefixes of an LR grammar is characterized by
the parser’s configurations, a grammar-sized key space (104 –106 for SQL-class grammars).
Proposition 2 (Acceptance semantics deadlock at step 1). Let the tag semantics be “the PDA accepts this
sequence” (membership in L). For any L containing no sentence of length one token, every single-token
continuation of the empty prefix is tagged rejected, so the step-1 mask is empty and generation cannot start.
Masking requires Prefix(L) = {w : ∃w′ , ww′ ∈ L}, not L.
    Both conclusions are constructive, not merely destructive: they identify the correct key space (configura-
tions) and the correct semantics (prefix viability), which the rest of this section formalizes.

3.2    Configurations and the correct-prefix property
Definition 1 (Parser configuration). A configuration is a pair κ = (σ, ρ) where σ is the LALR(1) parser
stack (a persistent, immutable-node chain of states) and ρ is the lexer scan state over the current partial
lexeme—concretely the remainder bytes r of the single in-progress lexeme, which determine the scanner-DFA
state, the maximal-munch hypothesis set, and the last-accept position deterministically.
Definition 2 (Viable prefix). w ∈ Prefix(L) ⇐⇒ ∃w′ ∈ Σ∗ : w w′ ∈ L. Operationally: the incremental
scan-and-shift of w succeeds and the trailing partial lexeme is live for some allowed-or-ignored terminal.
Proposition 3 (The incremental parser is the oracle). Under the preconditions of §2 (reduced projected
grammar; validated lexicons Wc ⊆ Rc ), the incrementally advanced LALR(1) parser with the maximal-munch
contextual lexer accepts exactly Prefix(L): by the correct-prefix property [3], an LR parser detects an error
at the first terminal that cannot extend any sentence, so “no error so far” ≡ “viable prefix.” No separate
recognizer is needed.
    Two refinements make this exact in practice rather than merely in principle.

Allowed terminals under table compression. LALR tables with default reductions over-approximate
raw action rows (spurious reduces). The allowed-terminal set is therefore computed by simulation: A(σ) =
{τ : simulate(σ, τ ) reaches a SHIFT}, where simulate runs the reduce chain on a virtual overlay stack (pop
|rhs|, GOTO, repeat) until shift or error. Cost is O(|row| × depth) worst case, amortized far less, and
memoized per stack node.

EOS gating by reduce-chain simulation, mid-lexeme aware. EOS may enter the mask only when
the current output is a complete sentence. A raw row read is wrong twice: compressed tables have spurious
reduces, and after ...FROM t the pending lexeme t is a complete identifier still awaiting maximal-munch
finalization—the stack alone would wrongly report EOS illegal. The rule: EOS is legal iff (the remainder is
empty or the pending lexeme finalizes as exactly one winning hypothesis) and, after virtually shifting that
finalized terminal on a scratch stack, ACCEPT is reachable via the reduce chain of $end.


4     The token–terminal bridge
LLM tokens do not align with grammar lexemes: sel+ect spells SELECT, and schema identifiers are never
single tokens. Masking out “fragment” tokens destroys completeness; admitting them requires scoring every
token’s bytes against the live configuration. The early design snapshot illustrated this misalignment and left
the mechanism as later work; this section is that mechanism.

4.1    The trie walk and the exact mask
Definition 3 (Token trie). The token trie is a byte trie over {bytes(t) : t ∈ V }, stored as one DFS-contiguous
array of packed 8-byte nodes (edge byte, token id, subtree size) plus an alias table mapping each node to all
token ids sharing its spelling. One trie per tokenizer fingerprint; special tokens are excluded and permanently
masked (EOS enters masks only via the explicit gate).


                                                       4
Definition 4 (The mask). For configuration κ with current output w,
                 M (κ) = { t ∈ V \ {EOS} : w · bytes(t) ∈ Prefix(L) } ∪ { EOS iff w ∈ L }.
   M (κ) is computed by a DFS over the trie that carries an O(1)-updatable scan state per frame (DFA
state, current segment, last-accept, pending forced-emission cascade): a byte that kills the DFA triggers
maximal-munch emission of the last accept and requeues the unconsumed tail. Rejection is monotone under
extension, so rejected subtrees are skipped wholesale via the packed subtree size. At identifier positions the
DFA runs against the L3 trie intersection. Masks are complete over ids via alias expansion.

4.2    The context-independent/context-dependent split
Proposition 4 (Boundary-crossing tokens are not (ρ, A)-determined). Let token t’s bytes cross a terminal
boundary and continue (e.g. ’),’ or ’1;’): they complete a terminal τ1 and begin material beyond it. The
viability of t at κ = (σ, ρ) depends on the allowed-terminal set after shifting τ1 , i.e. on the stack σ. Hence no
cache entry keyed only on the lexer state and the current allowed set A can decide t soundly.
    The walk therefore classifies every admitted token as CI (context-independent: resolvable within the
current lexeme, or ending exactly at one terminal boundary with that terminal in A)—cacheable—or CD
(context-dependent: boundary-crossing continuation)—returned as a residue list and checked against the live
stack every step, never cached. Without this split, the cache-key soundness obligation of §4.3 is violated by
construction, not merely unverified. The CD residue is the main hot-path cost and gets its own machinery:

Verdict-equivalence grouping. The per-step verdict of a CD entry depends on the entry only through
its per-event candidate terminal sets, its segments and trailing remainder only via the lexicon predicates,
and the live set of its remainder’s scan state. Entries are therefore partitioned once, at publish time, into
verdict-equivalence classes; each step evaluates one stack-dependent verdict per class and extends the mask
with the class’s alias-expanded ids. On the SQL bench this turned ∼25k per-step entry checks into ∼150
class verdicts (measured mean 143–150 classes/step at n=16,000; §8.2), and a later kernel round that keyed
classes by verdict equivalence instead of raw bytes collapsed ∼55k singleton groups to ∼1.4k classes, a 9.3×
cold-build reduction (§6.2).

4.3    Configuration-keyed caching: OBL-KEY1 and the identifier rule
The write-back mask cache carries the v0.0.5 table’s spirit—precomputed where cached, computed on
miss—to its workable form: entries are keyed on configurations, published idempotently (content-hashed
entry_id = BLAKE2b-128(key ∥ encoding tag ∥ payload), so racing writers produce the same id), immutable,
and versioned under namespaces that roll over when grammars are superseded.
Definition 5 (T1 key). The per-grammar (T1) cache key of a configuration is
                         k(κ) = kind ∈ {ident, generic}, r, sorted(A), schema_fp ,
                                                                                

where r is the remainder bytes (which determine the lexer scan state), A the allowed-terminal signature from
the live stack, and the schema fingerprint is carried by identifier-position keys as a distinct key type.
Proposition 5 (Cache-key soundness obligation, OBL-KEY1). Any two configurations sharing a key must
produce byte-identical context-independent masks: the key must refine the Myhill–Nerode classes of the (lexer
product-DFA × allowed-terminal set × identifier-lexicon) product. The CD residue is exempt because it is
never cached.
    OBL-KEY1 is verified, not assumed: differential tests check cache-on ≡ cache-off over randomized replays
including cross-role hits, and publish is content-addressed so a racing writer of the same key with a different
mask trips a runtime assertion.
Proposition 6 (Identifier composition rule). At identifier positions the mask must come from the L3 allow-list
trie intersection; unioning a cached generic-identifier verdict is unsound. A generic verdict admits tokens
spelling forbidden identifiers, and the parser will not reject them later—they are grammatical as identifiers—so
the error would be a silent RBAC violation, invisible to any downstream syntactic check.


                                                        5
   The rule is enforced structurally: identifier-position keys are a distinct key type that cannot collide with
generic keys, and consulting a generic entry at an identifier position raises an error in all builds (a test injects
the condition and asserts it fires).

The cross-family tier (T2) and the scanner normal form. A second tier shares entries across the
grammar family—the enterprise shape is many roles × schemas over one dialect. Role projections share
the L1 terminal numbering (assigned at freeze; projections subset productions, never renumber), so two
roles reaching the same normalized configuration share entries. To maximize sharing soundly, non-identifier
keys normalize the remainder to the genN scanner normal form: scanning r with last-accept tracking yields
(q, ℓ, p)—the live DFA state q, the last-accept length ℓ, and the last-accept state p—and the key becomes
              genN, p, q, v, sorted(A), schema_fp ,        v = r[ℓ:] (the post-accept suffix bytes),
                                                    

sound only under the lexicon-visibility guard (live[q] ∪ accepts[p]) ∩ LEX = ∅: every terminal whose lexicon
predicates the walk could consult on remainder-derived bytes lies in that set, so under the guard those checks
are lexicon-inert and the walk’s future is a function of (p, q, v, A) and the lexicons alone—remainders the
walk provably cannot distinguish share one entry. The suffix v is load-bearing (e.g. b"1e" and b"1E" share
(q, ℓ, p) but requeue different bytes on emission). Guard failure falls back to the raw key.
Remark 1 (A soundness catch, found by fuzzing the fix). When any lexicon exists, walk-time CD filtering
embeds schema words into entry content, so the schema fingerprint must scope all entries of a lexicon-bearing
producer, not only identifier positions. The original T2 tier shared generic entries across schemas; a 50-seed
shared-registry fuzz of the genN work produced a counterexample (a whitespace remainder with A = {LPAREN}
served one schema’s (-continuations of schema words to another). The unsound legacy behavior survives only
behind a kill switch for replaying old audit logs. The differential fuzz “failing” against the old behavior was
the fuzz finally being given a correct oracle.


5     Guarantees
Each guarantee is stated with its exact preconditions; each clause is paired with the test or benchmark that
verifies it (§8). L is the role/schema-projected language of §2.
Proposition 7 (Soundness). Every emitted token keeps the detokenized output in Prefix(L). Preconditions:
exact masks (no lookahead approximation); hard −∞ masking (soft down-weighting leaves nonzero mass on
illegal tokens and voids the guarantee); the identifier composition rule (Proposition 6).
Proposition 8 (Completeness and dead-end freedom). No token is blocked whose byte string extends the
current viable prefix toward a member of L; consequently every viable prefix has at least one legal token and
generation cannot wedge. Preconditions: (a) byte-complete vocabulary (all byte values reachable via bytes;
verified per tokenizer adapter—degradation is an explicit warning that voids completeness, never soundness);
(b) reduced projected grammar; (c) exact trie walk with alias expansion (masks over ids, not spellings); (d)
validated lexicons Wc ⊆ Rc .
    Precondition (d) earned its “validated, not assumed” status empirically: the first real-world schema
violation (a Spider database column named Official_ratings_(millions), whose parentheses lie outside
the column-name regex) produced an empty mask at a viable state within 100 generations—every prefix of
the word passes the lexicon-prefix check, yet no token can ever complete the lexeme. The precondition is now
checked at guide build.
Proposition 9 (Termination). In mode 1 (the GRID-owned decode loop): every non-error stop satisfies
output ∈ L. Preconditions: EOS-iff-ACCEPT gating (§3); a token-denominated reserve—per-configuration
minimal-completion costs counted in vocabulary tokens (a terminal-denominated reserve under-reserves:
one identifier terminal can span many tokens), summed incrementally on the stack—with the trigger
budget ≤ |completion| + safety answering Write(shortest legal completion + EOS), never a bare EOS away
from ACCEPT; and a finite length budget. In mode 2 (processor-only serving, where a logits processor
cannot append tokens), the guarantee weakens to EOS-only-at-ACCEPT: reserve completion is unavailable,
truncation at budget exhaustion is possible, and the downgrade is recorded in the audit seal.


                                                         6
Proposition 10 (Complexity: requirement R). Guard-rail cost is amortized O(1) per token and O(n) total;
the per-step worst case is bounded by nesting depth (one terminal can trigger a reduce cascade proportional to
stack depth; SQL’s prefix operators are inherently right-recursive, so cascades cannot be linted away), never
by the output position n. Per-stream space is O(depth) beyond the shared artifacts. Preconditions: nothing in
the hot loop may read state proportional to n—the processor keys per-row states incrementally (a splitmix64
chain, not prefix hashing), the audit configuration hash is a rolling O(1)-per-push mix carried in stack nodes,
and mask cost is a function of the configuration.
Proposition 11 (The RBAC boundary). Grammar masking enforces verb-level and table-level policy. Per-
table column restrictions are not enforceable by any left-to-right CFG mask: in SQL the SELECT list precedes
FROM, so the alias→table binding needed to judge a column is unknown at column-mask time, and alias
binding is context-sensitive. Column-level policy is a post-parse semantic check on the completed statement
(one AST walk) or a view/rewrite layer in the database.
   Proposition 11 is not an apology but a load-bearing design input: it defines the residue that the
SemanticChecker names precisely, which in turn is what makes checker-guided repair work at scale (§8.4).
Remark 2 (Distribution faithfulness is not claimed). Per-step masking does not sample from P (x | x ∈ L):
it renormalizes locally per step [4]. GRID does not repair this by default—the benchmark plan measures
downstream execution accuracy instead of pretending the gap away—and constraint-induced quality loss
for small models is real and documented [5]. Grammar-aligned decoding [4] and two-phase reasoning-then-
constrained approaches [6] are compatible add-ons, deferred by decision.


6     System
6.1     Architecture
Figure 1 shows the three time scales. Everything expensive is offline and content-addressed; everything per-
request is a registry lookup with single-flight construction; the per-token hot path touches only configuration-
sized state.

The per-token hot path        (normative order; every step audited):

    1. A ← allowed terminals by reduce-chain simulation on the virtual stack (memoized per node).
    2. eos_ok ← mid-lexeme-aware ACCEPT-reachability (§3).
    3. Reserve trigger (session budget, not grammar state): if budget ≤ |completion| + safety, return
       Write(shortest completion + EOS).
    4. Key ← Definition 5 / the genN normal form; T1 then T2 lookup; miss ⇒ trie walk (CI mask + CD
       residue), publish idempotently.
    5. Mask ← CI ∪ CD-pass (live-stack class verdicts) ∪ {EOS iff eos_ok}; empty mask raises—a bug by
       Proposition 8, asserted throughout the test suite.
    6. Singleton masks extend to a maximal forced span (jump-forward Write, bounded chain length); otherwise
       return the full exact mask, applied as a hard in-place fill.
    7. On the sampled token: bytes → lexer advance (maximal munch, candidate sets, parser-viable pick) →
       shift/reduce on the persistent stack → append the audit record.

    Two implementations of this semantics coexist: a ∼140-line pure-Python executable specification (brute-
force trial-parse over the vocabulary) and the fast path, bound bit-identically by differential and parity tests.
This discipline caught—before any debugging session—alias ids silently dropped from masks, lexicon-blind
reserve completions, and a real Rust/Python divergence in a CD group key.




                                                       7
               OFFLINE / PER DEPLOYMENT

              PolicyBundle          RoleProjection (L2)
              (RBAC store)           subset → reduce

                                                                         compose → reduce           CompiledGrammar
           DialectGrammar (L1)                                           → LALR(1) compile            (fingerprinted)


             SchemaSnapshot          SchemaLexicon (L3)
                                        identifier tries



             TokenizerAdapter             TokenTrie                ReserveTable
               token_bytes            (per tokenizer fp)      (grammar fp, tokenizer fp)


             PER REQUEST

              GrammarRegistry lookup           GridGuide(compiled, trie,             GridLogitsProcessor /
             (single-flight on miss, E17)           cache, audit)                vLLM structured-output backend


             PER TOKEN (hot path)
                                                              MaskCache T1/T2              CD residue check
                parser stack σ
                                        MaskProducer          hit | miss: trie walk     (live stack, uncached)
             allowed terminals A
                                                                  + write-back

                               AuditLog.append
                                                           advance: lexer scan        masked_fill_(−∞)
                             (config hash, entry id,
                                                             → shift/reduce               → sampler
                             token, blocked count)




Figure 1: GRID architecture at its three time scales (mirrors the normative design document). Offline
artifacts are immutable and fingerprinted; per-request construction is single-flight; the per-token loop reads
only configuration-sized state.

6.2    The kernel line: v4 → v5 → v5.1 → v6 → v7
Four hot symbols (trie walk, CD verdicts, LALR advance, bitmask fill) are bound to Rust kernels; the Python
spec path remains and a flag forces it. The performance history is a lesson in where the cost actually was:
  • v4 — a persistent, structurally interned stack arena with cross-token memos and a one-call assembled
    hit pass: warm-hit p50 12.9 → 3.5 µs (dev host). The interning insight: once a hot path is in Rust,
    the next win is usually not calling it—parser configurations recur massively across positions. v4 also
    releases the GIL on the cold walk; measured main-thread liveness during a cold replay rose from 9%
    (walk holding the GIL: “overlap” was a lie) to 88%.
  • v5 — scheduler-side fill_bits: the whole per-request bitmask row (pre-packed CI bit words + live
    CD bits + EOS) written into vLLM’s buffer in one FFI call. Motivated by the first real batched
    run: batch-1 overhead +1.26% but batch-8 +3984% and batch-32 +5151%—three stacked serving-only
    defects (a fill path that skipped the warm kernel; a prefetcher that scheduled every successor onto one
    worker; per-request copies re-registering every entry). Fixes in dependency order took the batch-32 step
    from 708 ms to 16 ms.
  • v5.1 — verdict-equivalence CD grouping (Remark in §4.2): cold CD-heavy mask builds 124 → 13.3 ms
    (9.3×); warm fill p90 38 → 3.8 µs. Both prior theories of this cost (“151k-vocab walks are superlinear,”
    “the warm gap is Python dispatch”) failed under component-level measurement; the real causes were
    CD keys embedding raw bytes and re-packing ∼47k CD ids per fill.
  • v6 — the whole per-request serving step in-kernel (session_accept/session_fill, one FFI call
    each): warm serving step 7.39 → 1.33 µs/request (accept 6.16 → 0.56, fill 1.22 → 0.77; local M-series
    measurement), restricted to audit-off serving paths; audit-enabled and processor-mode guides keep v5.
    A 200-seed lockstep fuzz of v6 against v5 showed zero divergence and the pre-implementation review
    surfaced a real v5 bug (post-COMPLETE state resurrection under speculative decoding), now pinned
    by the differential suite.


                                                                8
    • v7 — the entire cold mask miss moved into Rust (RustWalker.walk_payload + RustVerdicts.register_blob):
      walk, group-blob, CI pack, adaptive encode, BLAKE2b entry_id, and registration in one GIL-released
      call; Python receives a handle plus a thin MaskEntryV7 shell. The red-team’s original premise—that
      the per-cold-entry Python cost was make_entry/encode/hash—was wrong on inspection (those are
      microseconds); the real source of the measured 6.8–8.7 ms per boundary entry was the WalkResult
      glue building CDEntry reps plus ∼30–60k gc-tracked objects per miss, whose allocation triggered gen-2
      GC pauses inside the walk. Keeping the miss in Rust removes both: the per-boundary-entry cost falls
      6.8–8.7 → 0.003 ms. entry_id is byte-identical (so the audit trail replays unchanged); GRID_V7 defaults
      on and =0 is byte-identical to v6. The win is localized to the serving cold-entry path—the warm hit
      path, the R-microharness, and the engine-comparison latencies are v7-unchanged.

6.3     The serving contract
Under vLLM, GRID implements the structured-output backend contract (scheduler-side bitmask fill, rollback
natural on persistent states) and a logits-processor mode. The contract that keeps a batch healthy:

    • Overlap, cold-only. Mask computation runs on CPU overlapped with the GPU forward pass. The
      prefetcher schedules a successor’s mask onto the worker pool only when it is not already warm: the
      warm steady state never touches the pool (unconditionally scheduling every successor serialized the
      steady state behind one worker’s queue—one of the three batched-run defects).
    • Skip-a-round defer. If a request’s mask is not ready at sampling time (worst case: a cold identifier-
      position walk), that request is deferred from the current scheduling round and rejoins the next step;
      co-batched requests are never stalled, and an approximate mask is never substituted—by design there
      is no over-approximating deadline fallback, because one over-admitted token exits Prefix(L) and voids
      Proposition 7. In vLLM this is realized as a scheduler mask-readiness guard (one small patch site;
      upstream PR drafted).
    • Single-flight everything. One build per artifact fingerprint; N concurrent waiters share the result or
      the same exception; failures are negatively cached with a TTL.
    • An honest negative result: warmup-at-admission fails on the GIL. The tempting alternative
      to the defer—warm the fresh request’s masks while it sits in the WAITING queue—was implemented
      and measured harmful: the tier work is GIL-bound, so admission warmup starved the live engine
      (fresh-request TTFT 10× worse and multi-second batch stalls). It defaults off. The defer, plus genN key
      normalization and rayon-parallel cold walks (bit-identical; 2.05× at 8 threads locally), is the shipped
      cold-schema stack.

6.4     The audit chain
Every step appends a record (step, config_hash, mask_entry_id, token, blocked_count, kind, prev_hash)—
including each interior token of a forced span and the EOS tail record—chained by BLAKE2b from a
genesis constant and sealed with the stop reason, artifact fingerprints, and mode flags (e.g. processor-only
downgrades). The configuration hash is rolling and O(1) per push,

          H(node) = low64 BLAKE2b-128 H(parent) ∥ u32(state) ∥ u32(goto) ,          H(root) = 0,
                                                                              

since hashing the stack from scratch would be a hidden Θ(depth)-per-token dependence. Because mask
entries are immutable and content-addressed and the hash pins the parser trajectory, a log replays against
archived artifacts to bit-identical masks; §8.7 reports the full-scale replay measurement.


7     Worked examples
7.1     Masking mid-identifier under a schema lexicon
Take the CRUD-subset grammar (lowercase keywords; TABLE_NAME and COLUMN_NAME share the regex
[a-z_][a-z0-9_]* and are L3 categories), the role analyst whose L2 projection keeps only select_stmt


                                                      9
                                                                     yees: CI (boundary, TN ∈ A)


                  e      m       p      l        o         y         ee      s      _public


                                            scan state after emplo

                                                       yees where: CD (crosses boundary, live-stack verdict)
               orders
                                                       yer: blocked (no allowed word; whole subtree pruned)


Figure 2: Example 7.1: the L3 lexicon trie for WTABLE during the walk at remainder emplo. Double circles
are allowed-word accepts. Candidate tokens are classified CI (cacheable), CD (checked against the live stack,
never cached), or blocked (whole trie subtrees pruned monotonically).


among the query productions, and the schema lexicon

                             WTABLE = {employees, employees_public, orders},

with a table salaries existing in the database but absent from the role’s lexicon. The model has emitted
                                            select * from emplo

so the configuration κ has: stack σ with select, *, from shifted (allowed next terminal set A =
{TABLE_NAME}), and remainder r = emplo scanning inside an identifier lexeme with the L3 category
context set. Because A contains an identifier category, the cache key is the ident type and carries the schema
fingerprint (Proposition 6); the walk intersects the token trie with the lexicon trie from the state reached by
emplo (Figure 2). Representative verdicts:

  • token yees (bytes yees): completes exactly employees, a lexeme boundary with TABLE_NAME ∈ A
    ⇒ CI, admitted (and cached in the entry’s CI payload).
  • token y: extends to employ, a live lexicon prefix ⇒ CI, admitted (mid-lexeme continuation).
  • token yees where: crosses the boundary (emits TABLE_NAME = employees, skips ignored whitespace,
    begins where) and continues ⇒ CD: its verdict depends on whether where can shift after table_ref,
    i.e. on the live stack—checked this step, never cached (Proposition 4). Here it passes.
  • token yer: employer is not a prefix of any allowed word ⇒ blocked, monotonically with its whole trie
    subtree.
  • At the earlier position select * from (empty remainder): token sal matches the generic identifier
    regex but is a prefix only of the absent salaries ⇒ blocked. A generic-IDENT cache entry would
    have admitted it and the parser would never have objected—the silent RBAC violation the identifier
    composition rule exists to prevent.
  • At the statement head, tokens spelling insert, update, delete are blocked for this role because L2
    removed those productions and reduction pruned their terminals: the verbs are not merely improbable,
    they are outside the language. No prompt can path to them (the model-independent RBAC test probes
    every reachable identifier position with an exhaustive multi-token speller; §8.6).
  • EOS is not in the mask: simulating $end after virtually finalizing emplo as TABLE_NAME does not reach
    ACCEPT (the grammar requires the closing ;), even though emplo’s finalization itself is legal. After a
    later ... ; the reduce chain reaches ACCEPT and EOS enters the mask through the explicit gate
    only.


7.2    A cold schema entering a hot batch
Thirty-two requests are decoding at steady state (warm caches, kernel fills of a few microseconds) when a
request arrives for a schema the deployment has never seen. The fresh request pays, in order: a single-flight


                                                         10
                        single-flight specialize (27.3 ms)                    rejoins next round; then 1.00× warm (TTFT 0.7 ms)
                               cold ident-position walk (on pool, GIL-released)

    fresh schema req.

                                  mask not ready ⇒ deferred this round

    31 warm requests

                                                     warm fills stay µs-scale; contention bounded to the fresh window (§8.5)


                             k             k+1            k+2             k+3            k+4             k+5    engine steps

                                          fresh window (∼0.66 s)


Figure 3: Example 7.2: the cold-schema-into-hot-batch timeline. The fresh request’s compile and cold walks
run off the critical path; the mask-readiness guard defers only the fresh request from the rounds where its
mask is late (k+1, k+2). Co-batched requests never wait, and no approximate mask is ever substituted; the
shaded band is the fresh window, the only span in which they see (bounded) contention.


grammar+lexicon specialization (27.3 ms cold, measured; every concurrent duplicate waits on the same
build), then—at its first identifier-heavy positions—cold trie walks that are milliseconds-scale by nature
(vocabulary-sized DFS). The contract of §6.3 makes these costs private to the fresh request: the walk runs
GIL-released on the pool, overlapped with the forward pass; if it is still unfinished at sampling time, the
scheduler’s mask-readiness guard defers only that request for the round (Figure 3). Measured on the declared
H100 SXM5 runner (§8.5): at kernel v7 the serving record holds the 31 warm co-tenants to a 15.3 ms
worst engine step while the fresh request’s ∼0.66 s cold window induces a transient +33.8% co-batched
TPOT slowdown—no longer a GIL-bound software cost (the v7 fused cold-miss path removed that) but host
CPU/memory-bandwidth contention between the cold walk and the forward loop, which shrinks as walk
threads grow. The defer remains the load-bearing protection: with it disabled the same leg reads +373% and
65.7 ms. The fresh request itself sees TTFT 0.7 ms and then runs at 1.00× warm speed: a never-seen schema
trades its own first-token latency for exact masks throughout—no approximation is ever substituted.


8     Evaluation
All numbers below are from committed benchmark reports in the repository (bench/RESULTS*.md) or the
measured-results log; each table carries its host label verbatim. Declared runner = a named cloud instance
type and image recorded in the report (Lambda 1×H100 PCIe or SXM5 80GB, or 1×A10 24GB; Ubuntu 24.04;
virtualized); local dev = an unpinned Apple-Silicon workstation. Cross-engine ratios proved host-invariant;
absolute constants carry the host label.

8.1     Per-token mask latency vs. XGrammar, llguidance, Outlines
The engine-comparison harness measures the wall time to produce the full next-token mask at each replay step,
for all engines on the same SQL-subset grammar (expressed in each engine’s native format) and tokenizer, 11
replays. Table 1 reports both tokenizers on the declared H100 SXM5 runner at kernel v7 (re-recorded; within
noise of v6, as expected—v7’s win is localized to the serving cold-entry path, not this per-token latency path).
    Reading the table honestly: at kernel v7 GRID leads llguidance—the strongest prior engine in our
measurements—at both p50 and p90 on both tokenizers (3.6 vs. 6.6 µs p50 and 80 vs. 224 µs p90 on gpt2;
6.7 vs. 14.9 µs and 109 vs. 384 µs on Qwen), beats XGrammar at every reported percentile, and is the only
engine with zero rejected replays. Its cache split is p50 3.5 µs hit / 4.8 ms miss at 92% hit rate (gpt2; 6.7 µs /
13.9 ms / 92% on Qwen), so the p99 remains cold-miss trie walk on this recursive SQL grammar: llguidance’s
Earley/derivative core keeps the flattest p99 (352 µs vs. GRID’s 5.3 ms on gpt2), and we say so plainly.
Outlines ≥1.x has no CFG engine of its own: outlines.types.CFG routes to a backend, default llguidance,
so its row is the same matcher plus Outlines’ logits-processor wrapper—identical rejects by construction. The
steep negative table slopes are an artifact of cold misses clustering early in replays; the warm-replay check


                                                                11
Table 1: Per-token mask latency, SQL-subset grammar, kernel v7. Host: Lambda 1×H100 SXM5 80GB,
Ubuntu 24.04 (declared runner). Top: gpt2 (491 steps); bottom: Qwen2.5-0.5B-Instruct tokenizer (151k
vocab; 509 steps). “Rejected” counts language-parity corners between grammar encodings (maximal munch
vs. explicit whitespace), not correctness bugs.
      engine                                           compile          p50        p90          p99    slope ( µs/pos)   rej.
      gpt2
      GRID (Rust kernels: walk + CD + LALR)            378.0 ms      3.6 µs      80.0 µs  5,347.4 µs          −9.292       0
      XGrammar 0.2.3 (EBNF)                             94.1 ms     72.2 µs   7,503.3 µs 25,586.7 µs         −43.759       0
      llguidance 1.7.6 (lark, driven directly)         285.9 ms      6.6 µs     223.9 µs    351.7 µs          −1.176       2
      Outlines 1.3.1 (CFG backend = llguidance)     22,115.1 ms     73.9 µs     431.5 µs    582.4 µs          −2.152       2
      Qwen2.5-0.5B-Instruct (151k vocab)
      GRID                                           1,297.2 ms   6.7 µs    109.0 µs 15,906.2 µs             −48.903       0
      XGrammar 0.2.3                                   342.7 ms 588.6 µs 10,026.9 µs 31,774.6 µs             −63.015       0
      llguidance 1.7.6                                 979.5 ms  14.9 µs    384.4 µs  1,200.2 µs              −1.819       1
      Outlines 1.3.1                                13,796.8 ms  61.7 µs    459.5 µs    558.7 µs              −2.215       1



Table 2: R microharness: mask latency vs. position, no model. Host: Lambda 1×H100 SXM5 80GB, Ubuntu
24.04 (declared runner), kernel v7; gpt2; n=16,000/stream; 20 seeded runs per depth (320,000 steps each).
GC is disabled during the warm timed pass.
               depth   slope ( µs/pos, ±95% CI)   warm p50    hit p50   miss p99 hit rate   cum. R2    CD cls./step
                   0 −0.000004 ± 0.000002            3.7 µs    4.8 µs    6.56 ms   100.0%   0.99985             143
                   4 −0.000007 ± 0.000002            4.3 µs    5.6 µs    5.84 ms   100.0%   0.99992             148
                   8 −0.000007 ± 0.000002            4.7 µs    6.1 µs    6.11 ms   100.0%   0.99995             149
                  16 −0.000006 ± 0.000002            6.0 µs    6.8 µs    6.31 ms   100.0%   0.99994             150



(slope +0.002 µs/pos on gpt2, first-half p50 3 µs vs. second-half 4 µs; −0.004 µs/pos and 5 µs vs. 5 µs on Qwen)
is the R-relevant statistic.

8.2     Requirement R: flat per-token cost
The R microharness (declared H100 SXM5 runner, kernel v7; gpt2; n = 16,000 tokens per stream, 20
seeded runs per nesting depth, warm-pass OLS; ε = 10−4 µs/pos) isolates guard cost from the model (Table 2).
Slope confidence intervals sit well over an order of magnitude under ε at every depth; hit p50 is 4.8–6.8 µs;
the steady-state hit rate is 100%; cumulative-cost fits are linear with R2 ≥ 0.9998.

Head-to-head scaling vs. guidance, three eras (local dev Mac, unpinned; slopes and shape are the claim,
absolutes indicative). The project’s founding claim—guard cost flat as generated context grows—was measured
against guidance in three vintages on the same growing WHERE-chain statements, n ∈ {512, . . . , 16,384}.
At n = 16,384: GRID runs at 3.2 µs/step with slope −3.3 × 10−5 µs/pos (kernels active); guidance 0.3.1
(today’s llguidance core) is also flat but at a ∼30× higher constant (97.7 µs); guidance 0.1.5 (November 2023,
Python Earley) holds a flat median (∼114 µs) while its worst-case single step grows 67.5 → 106.2 ms across
one generation’s quarters (gen-2 GC scanning the growing Earley chart, verified via gc.callbacks); and
guidance 0.0.64 (July 2023, the release the v0.0.5 design was conceived against) breaks requirement R
outright: measured overhead-vs-position slopes +1,105 to +1,189 µs/pos (mechanism confirmed in its code:
full-string regex rebuilds per candidate per token, whole-prompt re-encoding per operation), i.e. quadratic
total cost—it spent 898 s reaching position 873 and could not complete n = 2,048; the linear fit extrapolates
(labeled as such, not measured) to ≈19.5 s/token at position 16,384. Total constraint cost over one 16k replay:
GRID 0.05 s vs. 1.88 s (0.3.1) vs. 2.52 s (0.1.5) vs. ≈44 h (0.0.64, extrapolated).

8.3     MaskBench (JSON Schema)
GRID claims extensibility to any LALR(1)-parsable language; MaskBench (guidance-ai/jsonschemabench [7])
is the cheapest public test of where that is true. GRID enters via a JSON-Schema→grammar compiler and a


                                                               12
Table 3: MaskBench, 315-schema stratified sample, llama-3.1 tokenizer, local dev host (unpinned). TBM
= time between masks; TTFM = time to first mask (compile). Compile errors are declared non-support;
validation errors (valid instance rejected) and invalidation errors (invalid accepted) are silent correctness gaps.
                    metric                         GRID        llguidance    XGrammar (compliant)
                    TBM avg                         562 µs           20 µs                     101 µs
                    TBM p50                          28 µs           10 µs                      10 µs
                    TBM p75                          34 µs           21 µs                      29 µs
                    TBM p90                          75 µs           31 µs                      57 µs
                    TBM p99                        7.7 ms          179 µs                     2.7 ms
                    TBM max                       11.7 ms          2.0 ms                    12.0 ms
                    TTFM p50                       6.0 ms         0.31 ms                     2.4 ms
                    TTFM p75                       8.1 ms         0.44 ms                     209 ms
                    TTFM p99                       302 ms          7.7 ms                       13.0 s
                    compile errors (declared)           79              62                          0
                    validation errors (silent)           0               3                         27
                    invalidation errors                 68               0                         37


Table 4: Spider dev execution accuracy.      7B rows: Qwen2.5-7B-Instruct, full 1,034 questions
(grid/unconstrained on the declared H100 PCIe runner; the repair pair reproduced grid exactly on the
declared A10 runner). 0.5B rows: Qwen2.5-0.5B-Instruct, 100 questions, local dev host. EX = result-set
match on the Spider databases.
    model           arm                                      executes        EX   EX delta    truncated    tok/query
    0.5B (n=100)    GRID (repair inert at this scale)          57.0%     29.0%      +13.0           4.0%         41
    0.5B            unconstrained                              31.0%     16.0%         —            9.0%         61
    7B (n=1034)     GRID (with repair)                        94.5%     55.2%        +2.3           0.5%         40
    7B              GRID (repair off, ablation)                91.3%     53.7%       +0.8           0.9%         35
    7B              unconstrained                              91.0%     52.9%         —            0.2%         33


protocol-exact runner (TTFM/TBM semantics verbatim; llama-3.1 tokenizer; 315-schema stratified sample;
host: local dev, unpinned). Table 3 shows the three-way comparison.
   GRID’s p25–p75 (14/28/34 µs) is the kernel hit path, with kernels active on 100% of compiled schemas,
and GRID is the only engine with zero validation errors—every valid instance of every schema it compiled was
accepted; its 68 invalidation errors are all traceable to deliberately ignored value constraints (the XGrammar-
default convention, itemized in the report). Its honesty boundary is llguidance-style: 79/315 schemas are
declared compile errors (allOf, patternProperties, if/then/else, . . . , including 5 genuine LALR conflicts).
The TBM p90 traces a clean kernel lineage across the identical 315-schema sample: v3-era 27.8 ms → v5.1
verdict-equivalence grouping 208 µs → v7 fused walk→blob→register 75 µs. This is the kernel-v7 re-record:
the correctness columns are byte-identical to the earlier records, while the last step—v5.1 to v7—cut TBM
p90 a further ∼2.8× (208 → 75 µs) and the TBM average from 683 to 562 µs by moving the per-cold-entry
Python materialization/glue (and its gen-2 GC pauses) into Rust; the llguidance and XGrammar latency arms
moved under 10% between records, a host-noise control placing the delta on GRID’s side. Two structural facts
explain the remaining tails: the TBM p95+ tail is the cold trie walk, which MaskBench’s one-shot-per-schema
protocol never lets the write-back cache amortize (the serving benchmark is where that design choice pays),
and TTFM is a pure-Python table build (19× llguidance’s at p50, but 26–43× ahead of XGrammar’s p75+
compile blowups).

8.4    Spider: execution accuracy and checker-guided repair
Executability is measured where it matters: the full 1,034-question Spider dev set [8], greedy decoding,
grammar with 100% dev-gold coverage plus per-database L3 lexicons—every constrained output parses with
schema-valid identifiers by construction (Table 4).


                                                             13
Table 5: Serving record, kernel v7. Host: Lambda 1×H100 SXM5 80GB, Ubuntu 24.04 (declared runner),
vLLM 0.24, Qwen2.5-7B, heterogeneous grammars. The cold-miss stress arm injects a fresh never-warmed
schema into a warm batch-32; its metric is per-request TPOT over the 31 warm co-batched requests, computed
with artifact-robust estimators (median-over-legs degradation; min-over-legs max step) for the reason given
in §8.5.
           TPOT overhead vs. unconstrained, batch 1                                              +0.15%
           TPOT overhead, batch 8                                                                +0.73%
           TPOT overhead, batch 32                                                               +1.51%
           TTFT, cold role+schema specialize                                                      27.3 ms
           TTFT, warm                                                                             1.51 ms
           Cold-miss stress arm (fresh schema into warm batch-32):
           max engine-step wall, min over legs                                                   15.3 ms
              raw per-leg maxima                                                   [15, 15, 16, 16, 16] ms
           co-batched TPOT slowdown during cold window                                           +33.8%
           fresh request: TTFT / completion / eff. TPOT      0.7 ms / 663.0 ms / 6.97 ms (1.00× warm)
           concurrent cold start (single-flight)                1 build / 8 waiters; same error on failure


    The scale finding, measured at both ends: the mask alone is worth +13 EX points at 0.5B—it erases
the syntax-error class a weak model commits constantly (+26 points of syntactic validity)—but only ∼+1
at 7B, because a capable model rarely errs syntactically. The repair half closes the loop at scale: GRID’s
residual 7B failures are alias↔column binding—exactly the class Proposition 11 proves out of mask scope, and
exactly what the alias-aware SemanticChecker names precisely. One constrained retry with the violations
quoted back converts a third of that floor (91.3 → 94.5% executes; 21% of kept retries newly correct) at
+5 tokens/query (+14%) on the ∼7% of queries that engage. The capability symmetry is measured in both
directions, not asserted: at 0.5B the same feedback is worthless (an interim run of 55 questions: repair metrics
identical to plain GRID—the model repairs its binding mistakes into different-but-equally-wrong queries),
while at 7B the mask matters less but the feedback converts—constraint quality determines feedback quality,
because the checker can only name violations precisely when the mask has already guaranteed everything
else. Ablations on the same harness (EX-invariant by construction): disabling the write-back cache costs 32%
of generation throughput (2.5 → 1.7 tok/s, n=20); audit-off and jump-forward-off move throughput within
noise.

8.5    Batched serving under vLLM
The end-to-end serving benchmark runs vLLM 0.24 (V1 engine) with Qwen2.5-7B on the declared H100 SXM5
runner: heterogeneous grammars (4 distinct) across batches 1/8/32, unconstrained control arm, warm-through
protocol, kernel v7 (Table 5).
    Warm serving overhead is low at every batch size—+1.51% time-per-output-token at batch 32—warm
and cold TTFT are 1.51 and 27.3 ms, and both single-flight behaviors hold. In the cold-miss stress arm the
warm co-tenants’ worst engine step is 15.3 ms (thread-invariant at 15–18 ms across walk threads 0/2/8). The
one residual cost is a transient co-batched TPOT slowdown of +33.8%, confined to the fresh schema’s cold
window; we characterize it below.
    What v7 changed. On the v6 stack the cold window cost more—a +114.7% co-batched slowdown
and a 36.0 ms worst step—and both were attributed to GIL-bound mask-entry materialization in the
fresh request’s cold window. That attribution was half right. Moving the entire cold miss into Rust
(§6.2: fused walk→blob→register, one GIL-released call) collapsed the per-boundary-entry cost 6.8–8.7 →
0.003 ms and, with it, the worst engine step on real hardware (36.0 → 15.3 ms). The residual glue theory
(“make_entry/encode/hash is the cost”) was disproved by the fix: the real culprit was the WalkResult glue
allocating ∼30–60k gc-tracked objects per miss, whose gen-2 pauses landed inside the walk—which is exactly
why keeping the walk in Rust removed them.
    The estimators. The cold-window metrics are computed with artifact-robust estimators (median-over-legs
degradation; min-over-legs max step, with the raw per-leg maxima always printed) because vLLM 0.24’s


                                                         14
multiprocess engine exhibits a once-per-leg 0.7–2 s frozen engine step that we exonerated five ways before
believing it: it fires in all-warm baselines with zero GRID work in flight, is invariant to the defer, warmup,
walk-thread, and JIT-warming levers and to both child- and driver-side GC control, and vanishes entirely
with the engine in-process—an engine-topology artifact, filed upstream as vllm-project/vllm issue #48229
(the repository’s LESSONS.md §6.8–6.9 holds the exoneration record). The raw per-leg step maxima
[15, 15, 16, 16, 16] ms show the v7 max step is now clean and tight, with no exogenous 1–2 s outliers polluting
the min-over-legs estimator.
    The cold-window slowdown, characterized. At v6 the co-batched degradation was called a Python/GIL/software
cost with a kernel fix pending. That fix has shipped, and the degradation did not go to zero—because it was
never primarily a software cost. It is genuine host CPU/memory-bandwidth contention between the cold
walk and the engine forward loop during the fresh schema’s ∼0.66 s specialization window. The diagnostic
evidence is direct: the slowdown decreases as walk threads increase, because more threads shrink the window
in which the contention occurs—a software-serialization cost would not behave this way. Walk/pool thread
niceness mitigates the residual. Full closure is therefore a compute-isolation trade-off (throttle the walk and
lengthen the fresh request’s TTFT, or accept the number), noted as future work rather than a defect to fix.
Throughout, the fresh request itself pays only its own cost: TTFT 0.7 ms, and 1.00× warm effective TPOT
once specialized—there is zero steady-state co-tenant interference. As a pre-v7 observation (superseded by
this record, retained only for lineage): an artifact-free JIT-warmed lockstep leg on the v6 stack read −1.75%
co-batched slowdown and a 23.9 ms max step; the same leg with the defer disabled read +373% and 65.7 ms,
the attribution that makes the defer the load-bearing protection. Finally, the tempting admission-time
warmup alternative was measured harmful on the GIL and ships disabled (§6.3); negative results are recorded
next to the positive ones.

8.6    Policy enforcement and end-to-end correctness at scale
The guarantees of §5 are checked directly, each against the test that exercises the corresponding property.

Soundness, completeness, termination end-to-end. Two arms exercise the whole decode loop. The
walk arm generates 10,000/10,000 outputs that parse, with 0 dead ends and 0 budget overruns (local dev).
The model arm, driving Qwen2.5-0.5B on the declared H100 runner, generates 1,000/1,000 parseable and
audit-verified outputs, again with 0 dead ends, and 706 reserve-completed stops (the termination machinery
of Proposition 9 firing as designed).

Policy/RBAC enforcement. A model-free exhaustive speller probes every reachable identifier position:
across 58 role×position×target probes it records 0 bypasses, with 9/9 positive controls reachable so the test
is non-vacuous. A 12-prompt injection suite (the adversarial-prompt arm) emits 0 forbidden lexemes on the
declared H100 runner, and column-violation fixtures are 100% flagged by the post-parse checker (the residue
Proposition 11 places out of mask scope).

Differential correctness, cache soundness, and kernel parity. The fast path is checked bit-exact
against the trial-parse oracle over quota-counted corpora including multi-terminal tokens, across a four-
tokenizer matrix; the viable-prefix oracle is checked by corpus, mutation, and mid-lexeme EOS differentials
against lark. Cache-key soundness (OBL-KEY1) is verified by cache-on ≡ cache-off runs including cross-role
hits, namespace rollover, and racing publishes. Grammar-pipeline reducedness and deterministic fingerprints
have property tests. All of these run in CI.

8.7    Audit replay and tamper detection
Over 1,000 generations spanning 29,242 audited steps and one cache-namespace rollover, every log replays
bit-identically (1,000/1,000) against its archived artifacts, and tamper detection catches every injected
mutation (1,000/1,000), on local dev.




                                                     15
8.8     Cross-engine comparison, summarized
Taken together with §8.1: on per-token mask latency GRID leads llguidance and XGrammar at p50 on both
tokenizers (Table 1), by more than 2× over XGrammar; llguidance retains the flattest p99. The SynCode
and GBNF arms were dropped by decision (2026-07-10) as the engine comparison had already settled on this
front.


9     Limitations and honest boundaries
    • Distribution faithfulness. Masking changes the sampling distribution (Remark 2); GRID measures
      the downstream effect (EX deltas) rather than claiming neutrality. GAD/ASAp-style faithful sampling
      and CRANE-style two-phase decoding are compatible, deferred arms.
    • Column-level RBAC is post-parse by proof (Proposition 11). The mask guarantee is verb- and
      table-level; the checker covers the residue and feeds repair.
    • LALR(1) languages only (v1). MaskBench draws the boundary concretely: 79/315 schemas are
      declared compile errors, 5 of them genuine LALR conflicts. An Earley fallback is a recorded option,
      unexercised because no target dialect construct has forced it.
    • Cold-walk tails. The cold trie walk over a 100k+ vocabulary is milliseconds by nature; the write-back
      cache amortizes it across requests (86–98% hit rates in replay- and serving-shaped workloads) and the
      serving contract keeps it off co-tenants’ critical path, but one-shot workloads see it (MaskBench p95+).
      Walk-level pruning is the named next kernel target.
    • The cold-window serving contention. A fresh, never-before-seen schema induces a transient
      co-batched slowdown (∼34% during its ∼0.66 s first-request specialization window). The kernel-v7 fused
      cold-miss path removed the GIL-bound entry-materialization cost that dominated at v6, so the residual
      is genuine host CPU/memory-bandwidth contention between the cold walk and the engine forward
      loop; it shrinks as walk parallelism rises and is mitigated by scheduling niceness. The fresh request
      itself runs at warm speed and steady-state co-tenant requests are unaffected. Fully eliminating it is a
      compute-isolation trade-off, noted as future work (§8.5).
    • One characterized exogenous artifact. The serving record’s per-step tail on vLLM 0.24’s multipro-
      cess topology contains a once-per-leg frozen step that is provably not GRID’s (five-way exoneration, §8.5);
      the serving metrics use artifact-robust estimators and the issue is filed upstream (vllm-project/vllm
      #48229) rather than papered over.
    • Termination is mode-dependent. The full termination guarantee (reserve-completed stops) holds
      in the GRID-owned loop; processor-only serving weakens to EOS-only-at-ACCEPT with truncation
      recorded (Proposition 9).
    • Host honesty. Headline performance numbers run on declared cloud runners; local-dev numbers are
      labeled and used for shape, not records.


10      Related work
Outlines [1] reformulated guided generation as FSM state transitions with a vocabulary index, extending to
CFGs via lexer-aware scanning over parser states—the paper whose problem statement and formal register
this work parallels, and an explicit inspiration for GRID’s design. GRID differs in what it keys and what
it promises: masks keyed on live LALR configurations with a write-back cross-request cache rather than a
per-automaton precomputed index; policy (roles, schemas) compiled into the language; guarantees stated
with preconditions and empirically verified; an audit trail. Notably, current Outlines releases delegate
CFG constraining to llguidance [9], so the engine-level comparison collapses into the llguidance one (§8.1).
guidance/llguidance [10, 9] pair an Earley/derivative core with a token trie; llguidance keeps the flattest
p99 tails and the fastest compiles in our measurements and is the bar GRID names—at kernel v7 GRID leads
it at p50 and p90 on both tokenizers (§8.1) while llguidance retains the p99 edge. GRID’s answer is also


                                                       16
architectural rather than raw-constant: configuration-keyed write-back caching across grammar families, mask-
level RBAC/schema projection, requirement R as a committed contract, and the audit chain. XGrammar [11]
introduced the context-independent/context-dependent vocabulary split with compile-time precomputation
and scheduler overlap; GRID adopts the CI/CD idea but makes the split a cache-key soundness requirement
(never cache CD), computes on miss with write-back (rewarding the per-role/per-tenant family shape), and
adds the identifier composition rule that per-schema policy needs. SynCode [12] formalizes grammar masks
over lexer-state × remainder tables with soundness/completeness theorems; its shipped d-lookahead masks are
sound but incomplete, which is incompatible with dead-end freedom—GRID chooses exact byte-level masks
for exactly that reason. PICARD [13] pioneered constrained SQL decoding by incremental parsing over beam
candidates (reject-and-filter rather than exact masks). Grammar-aligned decoding [4] and CRANE [6]
address the distribution and reasoning costs of strict masking; both are complementary layers above an
exact-mask engine like GRID. Automata-theoretic treatments of the token–terminal misalignment [14] give the
detokenization correctness framing our byte-trie bridge instantiates. JSONSchemaBench [7] supplies the
cross-engine schema corpus used in §8.3. Serving integration follows the vLLM structured-output interface [15].
Classical foundations: viable prefixes and LR parsing [2, 3]; linear Earley parsing on LR-regular grammars [16]
(the recorded fallback engine).


11     Conclusion
GRID shows that the properties an enterprise actually needs from constrained decoding—policy compiled into
the language, guarantees with preconditions, position-flat guard cost, a replayable audit trail, and batch-safe
serving with honest cold-start behavior—all follow from one commitment: key every mask, cache entry, and
audit record on the parser configuration, and prove (then verify) that the keys refine the equivalence the
semantics requires. The residue the mask provably cannot enforce is not hidden but named, checked post-parse,
and—at model scales that can use feedback—repaired. The committed record spans engine microbenchmarks,
a public schema corpus, full-dataset execution accuracy, and an end-to-end serving benchmark, each number
carried with its host label; the remaining open costs (cold-walk tails, the once-per-schema cold-window serving
contention, one upstream engine artifact) are stated as precisely as the wins.


References
 [1] Brandon T. Willard and Rémi Louf. Efficient guided generation for large language models. arXiv preprint
     arXiv:2307.09702, 2023.
 [2] Donald E. Knuth. On the translation of languages from left to right. Information and Control,
     8(6):607–639, 1965.
 [3] Alfred V. Aho and Stephen C. Johnson. LR parsing. ACM Computing Surveys, 6(2):99–124, 1974.

 [4] Kanghee Park, Jiayu Wang, Taylor Berg-Kirkpatrick, Nadia Polikarpova, and Loris D’Antoni.
     Grammar-aligned decoding. In Advances in Neural Information Processing Systems (NeurIPS), 2024.
     arXiv:2405.21047.
 [5] Zhi Rui Tam, Cheng-Kuang Wu, Yi-Lin Tsai, Chieh-Yen Lin, Hung-yi Lee, and Yun-Nung Chen. Let me
     speak freely? A study on the impact of format restrictions on performance of large language models.
     arXiv preprint arXiv:2408.02442, 2024.
 [6] Debangshu Banerjee, Tarun Suresh, Shubham Ugare, Sasa Misailovic, and Gagandeep Singh. CRANE:
     Reasoning with constrained LLM generation. In Proceedings of the 42nd International Conference on
     Machine Learning (ICML), PMLR 267, 2025. arXiv:2502.09061.

 [7] Saibo Geng, Hudson Cooper, Michał Moskal, Samuel Jenkins, Julian Berman, Nathan Ranchin, Robert
     West, Eric Horvitz, and Harsha Nori. Generating structured outputs from language models: Benchmark
     and studies. arXiv preprint arXiv:2501.10868, 2025.



                                                      17
 [8] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li,
     Qingning Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. Spider: A large-scale human-labeled
     dataset for complex and cross-domain semantic parsing and text-to-SQL task. In Proceedings of the 2018
     Conference on Empirical Methods in Natural Language Processing (EMNLP), 2018. arXiv:1809.08887.
 [9] Guidance AI. llguidance:      Super-fast structured outputs.     https://github.com/guidance-ai/
     llguidance, 2024.
[10] Guidance AI. guidance: A guidance language for controlling large language models. https://github.
     com/guidance-ai/guidance, 2023.
[11] Yixin Dong, Charlie F. Ruan, Yaxing Cai, Ruihang Lai, Ziyi Xu, Yilong Zhao, and Tianqi Chen.
     XGrammar: Flexible and efficient structured generation engine for large language models. arXiv preprint
     arXiv:2411.15100, 2024.
[12] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and Gagandeep Singh. SynCode:
     LLM generation with grammar augmentation. Transactions on Machine Learning Research, 2024.
     arXiv:2403.01632.

[13] Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. PICARD: Parsing incrementally for
     constrained auto-regressive decoding from language models. In Proceedings of the 2021 Conference on
     Empirical Methods in Natural Language Processing (EMNLP), 2021. arXiv:2109.05093.
[14] Terry Koo, Frederick Liu, and Luheng He. Automata-based constraints for language model decoding.
     arXiv preprint arXiv:2407.08103, 2024.

[15] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
     Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving
     with PagedAttention. In Proceedings of the 29th ACM Symposium on Operating Systems Principles
     (SOSP), 2023. arXiv:2309.06180.
[16] Joop M. I. M. Leo. A general context-free parsing algorithm running in linear time on every LR(k)
     grammar without using lookahead. Theoretical Computer Science, 82(1):165–176, 1991.




                                                    18
