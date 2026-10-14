                                            CBCL: Safe Self-Extending Agent Communication
                                                                                                    Hugo O’Connor
                                                                                                    Anuna Research
                                                                                                    hugo@anuna.io




                                                                                                        cases, ad-hoc validation cannot reliably prevent the emer-
                                            Abstract—Agent communication languages (ACLs)               gence of “weird machines” [2], unintended computational
                                         enable heterogeneous agents to share knowledge and co-         artifacts that attackers exploit to achieve behavior beyond
                                         ordinate across diverse domains. This diversity demands
                                         extensibility, but expressive extension mechanisms can         a system’s intended functionality.
                                                                                                           Contemporary agent communication presents a partic-
arXiv:2604.14512v1 [cs.CR] 16 Apr 2026




                                         push the input language beyond the complexity classes
                                         where full validation is tractable. We present CBCL            ularly acute instance of this problem. Early ACLs such
                                         (Common Business Communication Language), an agent             as KQML [3] and FIPA-ACL [6] defined core vocabularies
                                         communication language that constrains all messages,           of communicative acts (“performatives”). These languages
                                         including runtime language extensions, to the determin-
                                         istic context-free language (DCFL) class. CBCL allows          are parseable and well-defined; KQML explicitly allowed
                                         agents to define, transmit, and adopt domain-specific          communities to define new performatives by agreement,
                                         “dialect” extensions as first-class messages; three safety     but without formal constraints on such extensions. In
                                         invariants (R1–R3), machine-checked in Lean 4 and              practice, extensibility was largely pushed into content
                                         enforced in a Rust reference implementation, prevent           languages and ontologies. Surveys of ACLs identify persis-
                                         unbounded expansion, applying declared resource limits,
                                         and preserving core vocabulary. We formalize the               tent interoperability failures. Heterogeneous agents remain
                                         language and its safety properties in Lean 4, implement        confined to rigid contexts, and ad-hoc extensions proliferate
                                         a reference parser and dialect engine in Rust with             incompatible dialects that are difficult to generalize without
                                         property-based and differential tests, and extract a           the original developers [4], [5]. In the terminology of
                                         verified parser binary. Our results demonstrate that           Zambonelli et al. [20], traditional ACLs support only self-
                                         homoiconic protocol design, where extension definitions
                                         share the same representation as ordinary messages,            adaptation (parameter tuning within a fixed structure),
                                         can be made provably safe. As autonomous agents in-            not self-expression (structural evolution of the system
                                         creasingly extend their own communication capabilities,        itself). The modern alternative, using natural language or
                                         formally bounding what they can express to each other          unrestricted JSON schemas as the communication substrate
                                         is a precondition for oversight.                               (as in MCP [7] and LLM-based agent frameworks), provides
                                            Index Terms—language-theoretic security, agent com-
                                         munication, multiagent systems, deterministic context-         unlimited extensibility but creates an input language whose
                                         free languages, formal verification, protocol security         computational complexity is effectively unbounded. Deter-
                                                                                                        mining whether an arbitrary natural language message
                                                                                                        will cause harmful behavior requires solving undecidable
                                                              I. Introduction                           problems.
                                           Autonomous software agents increasingly coordinate              This paper presents CBCL, a language designed to be
                                         through message-passing protocols to perform complex expressive, extensible, and tractable. CBCL provides a
                                         tasks: managing supply chains, orchestrating IoT device minimal core vocabulary (8 performatives) and a formal
                                         swarms, and mediating human–AI collaboration. The mechanism for agents to define, exchange, and adopt
                                         correctness and security of these systems depend critically new domain-specific vocabularies (“dialects”) at runtime,
                                         on how agents parse and interpret the messages they without centralized coordination and without escaping the
                                         exchange.                                                      DCFL complexity class. CBCL achieves this through ho-
                                           Language-theoretic security (LangSec), as articulated moiconic self-extension. Dialect definitions are themselves
                                         by Sassaman, Patterson, Bratus, and Locasto in Security valid CBCL messages expressed in S-expression syntax, so
                                         applications of formal language theory [1], shows that they can be transmitted, verified, and installed using the
                                         the computational complexity class of an input language same parsing machinery used for ordinary communication.
                                         determines the difficulty of validation and the attack surface Three safety constraints, verified both in a Lean 4 formal-
                                         that parser implementations exhibit. Languages above the ization and enforced in a Rust reference implementation,
                                         deterministic context-free class introduce ambiguity that ensure that this self-extension is provably safe:
                                         makes parser equivalence undecidable [1], while Turing-           • R1 (No Recursion): Dialect templates are purely
                                         complete inputs make validation itself undecidable; in both          declarative pattern-template substitutions. Direct and
                                           Accepted at the LangSec Workshop, 2026 IEEE Security and           mutual recursion are forbidden (no cyclic dependencies
                                         Privacy Workshops (SPW).                                             between performative templates). No iteration or



                                              © 2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current
                                              or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective
                                              works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
     reflection is permitted.                                                           TABLE I
  •  R2 (Resource Bounds): Every dialect declares               Agent communication protocols classified by input language
                                                                                       complexity.
     static resource limits (nesting depth ≤ 64, expansion
     size ≤ 8192 characters, verification time ≤ 1000 ms)       Protocol           Complexity         Ext.      Verif.    Weird M.
     enforced at both installation and runtime.
                                                                KQML [3]                CFL          Partial Partial        Stack
   • R3 (Core Preservation): The eight core performa-
                                                                FIPA-ACL [6]            CFL          Partial Partial        Stack
     tives cannot be redefined by any dialect, preserving       MCP [7]                 RE            Yes     No            Turing
     protocol bootstrap invariants.                             LLM Agents              RE            Yes     No            Turing
   Together, these constraints support DCFL preservation,       CBCL                   DCFL           Yes     Yes           None†
meaning that the language recognized by a CBCL parser                “Complexity” refers to the effective computational power of the
                                                                end-to-end message interpretation pipeline, not the surface syntax alone.
remains in DCFL regardless of how many dialects are
                                                                  KQML and FIPA-ACL use S-expression envelope syntax (DCFL), but
installed. We give a formal argument in Section IV-G;            neither specification constrains the content language, so the end-to-end
the full closure proof is mechanized in Lean 4 (theorem         complexity is at least CFL. MCP and LLM agent frameworks can induce
dcfl_preserved).                                                 Turing-complete behavior when tool invocation permits arbitrary code
   CBCL is named after McCarthy’s 1982 proposal for a           execution. CFL = context-free language (Type 2); DCFL = deterministic
                                                                       CFL; RE = recursively enumerable (Type 0). Ext. = runtime
“Common Business Communication Language” [9] that
                                                                 self-extension of the protocol’s vocabulary; “Partial” indicates informal
would be “open ended so that as programs improve,               extensibility without safety guarantees (KQML’s open performative set,
programs that can at first only order by stock numbers can      FIPA-ACL’s X- parameters). Weird M. = weird machine class [2]. † At the
later be programmed to inquire about specifications and            parser and template-expander layer; tool backends and agent action
prices. . . ” Our work aspires to this vision while providing                       semantics are outside CBCL’s scope.
formal security guarantees.
Contributions. (1) A protocol design methodology that
                                                                B. Why DCFL Is the Right Complexity Class
achieves runtime self-extension while preserving DCFL
membership, applicable to message-passing systems where           The choice of DCFL (rather than regular, general CFG,
DCFL expressiveness is acceptable. (2) A Lean 4 formal-         or context-sensitive) is deliberate:
ization covering parser correctness (soundness and com-           • Regular languages cannot express the nested struc-
pleteness), safety constraint verification (R1–R3), pipeline        ture of agent messages (envelopes wrapping messages,
totality for parse/validate/verify, and DCFL preservation           dialects scoping inner messages).
under dialect installation. (3) A Rust reference implementa-      • General CFL risks parser differentials: ambiguous
tion (cbcl-rs) with dialect verification, gossip propagation,       grammars admit multiple parse trees, and attackers
C FFI/WASM bindings, and fuzz targets; a verified parser            can exploit divergent interpretations [1], [16]. Every
binary extracted from the Lean proofs. (4) A draft IETF             DCFL has an unambiguous grammar, making unambi-
Internet-Draft specifying application/cbcl [10], with a             guity a class-level property rather than a per-grammar
proof-of-concept Nostr [30] transport binding (cbcl-nostr)          proof obligation [13]. Parser equivalence is therefore
for agent communication and Lightning Network micropay-             preserved automatically under language evolution.
ments over decentralized relays.                                  • DCFL is the minimal class supporting nested struc-

         II. Background and Threat Model                            ture with parser equivalence. Residual divergence
                                                                    from serialization or encoding is mitigated through
A. The Unbounded Attack Surface Problem
                                                                    canonical serialization (Section V-E).
   Modern agent communication protocols have moved up             • Context-sensitive and beyond. Context-sensitive
the Chomsky hierarchy [29], from the well-defined gram-             membership is PSPACE-complete [13]; Type 0 is
mars of KQML and FIPA-ACL to unbounded complexity,                  undecidable. Both exceed the recognizer complexity
without acknowledging the security consequences implied             that LangSec considers tractable for full input valida-
by formal language theory [1], [2] (Table I).                       tion [1].
   The threat model for CBCL assumes agents operating
                                                                S-expression syntax is a natural fit: the grammar is
in open Byzantine environments where: (1) untrusted
                                                             LR(1)-parseable (indeed LL(1)) and nested parenthesized
peers may send maliciously crafted messages designed to
                                                             lists directly mirror the pushdown automaton’s stack
exploit parser differentials, trigger resource exhaustion,
                                                             operations.
or inject unintended computation; (2) dialect definitions
arrive from potentially adversarial sources and constitute
                                                                          III. CBCL Language Design
executable extensions to the receiver’s behavior; and (3) no
central authority controls participant conduct or vocabulary    We use the following terminology throughout. A per-
evolution.                                                   formative is a named message type (e.g., tell, ask). A
   The security goal is to ensure that no message, including dialect is a named, versioned collection of performative
dialect definitions, can cause a conformant parser to enter definitions that extends CBCL’s core vocabulary. Each
an unanticipated state or perform unexpected computation. dialect performative has a template: the pattern-template
substitution rule that maps dialect invocations to core       A query meta message asks a peer whether it supports
CBCL messages.                                                a dialect; a teach meta message transmits a previously
                                                              defined dialect to another agent:
A. Core Grammar
                                                                 (meta (query logistics @bob))
  CBCL messages are S-expressions conforming to an               (meta (teach logistics @alice
ABNF grammar (fully specified in the IETF draft [10]).             <dialect-definition>))
The top-level rules are:
  cbcl-message = simple-message / meta-message                The teach payload is the same S-expression used in define;
               / lang-message / wrapped-message               the receiving agent parses, verifies (R1–R3), and installs it
  simple-message = "(" performative SP recipient              using its existing CBCL infrastructure.
                   [SP content] *(SP parameter) ")"
  SP             = " "   ; single ASCII space (0x20)          Language-scoped messages invoke dialect performatives.
  performative   = "tell" / "ask" / "reply" / "hello"         Dialect invocations must appear inside a lang wrapper
                 / "bye" / "ok" / "error" / "cancel"
  lang-message   = "(" "lang" SP dialect-name                 that names the dialect; bare dialect performatives at top
                   SP cbcl-message ")"                        level are syntactically invalid. This scoping rule is what
  s-expr         = "(" *( s-expr / atom ) ")"                 makes the DCFL preservation argument (Section IV-G)
  atom           = identifier / string / number
                 / boolean / symbol                           straightforward: the lang tag serves as a deterministic
                                                              dispatch token.
The four message categories are:                                 (lang logistics
Simple messages use one of eight core performatives:               (track-shipment "PKG-123" :route "A->B"))

  (tell @bob "The meeting is at 3pm")                         This expands via pattern-template substitution to:
  (ask @alice "Status of task-42?" :thread conv-17)
  (reply @alice "75% complete" :in-reply-to msg-9874)            (tell @tracking-svc
  (ok @bob) (error @sender "parse failure")                        (shipment-request :package "PKG-123"
  (hello @bob) (bye @bob)                                            :route "A->B" :priority "normal")
                                                                   :domain logistics)
Colon-prefixed identifiers such as :thread and
:in-reply-to are keyword parameters: named optional Wrapped messages provide metadata (envelopes), in-
arguments in the style of Common Lisp keyword symbols. tegrity (signatures), and resource governance:
They are syntactically atoms (the symbol production in      (with-limits :timeout 100 :max-depth 10
the grammar) and carry no special semantics beyond            (ask @reasoner "Compute optimal path"))
serving as self-quoting parameter labels.
Meta messages operate on dialects—defining, querying, B. Homoiconic Self-Extension
and teaching:                                               CBCL’s dialect definitions are themselves valid CBCL
   (meta (define logistics (cbcl) @consortium            messages, eliminating the need for a separate meta-
     (:resource-requirements                             language parser (a second attack surface) or out-of-band
       ((max-depth 16)
        (max-expansion-size 4096)                        registry. Inspired by Racket’s #lang mechanism [11], a sin-
        (verification-time 1000)))                       gle DCFL recognizer handles both ordinary communication
     (extend track-shipment (pkg-id &key route priority) and language extension; the DCFL preservation argument
       (tell @tracking-svc
         (shipment-request :package pkg-id               (Section  IV-G) explains why installing a dialect does not
           :route route                                  increase the recognizer’s computational power.
          :priority (or priority "normal"))
        :domain logistics))                                   C. Template Expansion Semantics
    (:examples
      (track-shipment "PKG-42" :route "A->B")                   Dialect performatives expand through a deliberately re-
      (tell @tracking-svc                                    stricted template language supporting four forms: (1) literal
        (shipment-request :package "PKG-42"
          :route "A->B" :priority "normal")
                                                             templates with parameter placeholders, (2) substitution of
        :domain logistics))))                                parameter references with argument values, (3) bounded
                                                             conditionals (cond ((= param value) template) ...)
The optional :examples clause carries semantic meaning: with no recursion, and (4) sequences of template expres-
each input/output pair illustrates what the dialect author sions.
intends a performative to do in a concrete scenario. Because    This template language is not Turing-complete. It
CBCL cannot formally constrain meaning (Section VII-D), supports only flat pattern matching, finite conditional
examples serve as the primary mechanism for communicat- branching, and one-shot substitution. Critically, expansion
ing intended semantics between agents. A receiving agent is single-pass: the expanded result is not fed back through
can additionally evaluate the examples against its own the expander. This ensures that template evaluation termi-
expander to verify mechanical agreement before claiming nates in time linear in the template size plus substituted
dialect support.                                             argument size, and is bounded by declared expansion limits.
D. Message Processing Lifecycle                                   (envelope/signed/with-limits) messages. Because the gram-
   Figure 1 shows the processing pipeline that every incom-       mar is DCFL, each valid input admits exactly one parse
ing message traverses. Steps 1–2 (parse, validate + classify)     tree, so the Message returned by the parser is unique.
apply to all messages. The dialect-definition path (steps         Theorem 2 (Soundness). If parseMessage(e) = some m,
3–4) applies only to meta define messages; the expansion          then ValidMsgGrammar(e, m).
path (step 5) applies only to lang invocations. The pipeline      Theorem 3 (Completeness). If ValidMsgGrammar(e, m)
is total: every input produces either a well-typed result or      holds, then parseMessage(e) = some m.
a well-typed error (Theorem 12).                                     Soundness and completeness together establish that the
                                                                  parser recognizes exactly the message grammar encoded
 IV. Safety Invariants and Formal Verification
                                                                  in Lean (via ValidMessageGrammar), no more, no less.
A. Lean 4 Formalization Overview                                  This eliminates the possibility of parser differential attacks
   We formalize CBCL in Lean 4 as a library (LeanCbcl)            between the formal specification and the implementation,
comprising modules for S-expressions, messages, parsing, se-      a core LangSec concern.
rialization, pattern matching, dialect parsing, template ex-         We additionally verify 10 concrete round-trip properties
pansion, deterministic-union reasoning, dialect constraints       (parse(serialize(e)) = Ok(e)) covering the seven atom
(R1–R3), and an end-to-end pipeline. The formalization            types (symbol, integer, negative integer, boolean true/false,
comprises approximately 5,400 lines of Lean across 16             string, keyword), empty lists, flat lists, and nested lists. A
modules and yields 176 machine-checked theorems, with             SafeSymbol predicate formally characterizes which symbol
zero sorry gaps and no custom axioms. A verified parser           names survive round-tripping (non-empty, no delimiters,
binary (cbcl-parse) is extracted from the proofs.                 not a boolean or integer literal); the general theorem
                                                                  roundtrip_safeSymbol proves round-tripping for all safe
B. Parser Correctness                                             symbols via char-level parser reasoning.
   The S-expression parser uses recursive descent with a     C. R1: No Recursion
fuel parameter for termination. The fuel is set to |s| × 4 + 1, Constraint R1 ensures that dialect performative tem-
where |s| is the input length in characters. The multiplier 4plates contain no direct or mutual recursion, preventing
reflects the worst-case fuel consumption per input character:unbounded expansion. The Lean 4 formalization covers
a single character can trigger up to four recursive steps    both: Theorems 4–5 establish soundness and completeness
(entering a list, attempting to parse an element, consuming  for self-reference detection (a performative name cannot
the closing delimiter, and returning the result). The        appear in its own template), while Theorem 7 proves sound-
+1 ensures termination on empty input. This bound is         ness of mutual recursion prevention via a transitive-closure
sufficient for all inputs; the Lean proof of Theorem 1       dependency predicate (DependsClosure) that detects cycles
confirms that parseSExpr never exhausts fuel. The fuel       of any length in the performative dependency graph.
parameter is retained in the extracted cbcl-parse binary.
                                                             Theorem 4 (R1 Soundness). If containsSelfRef (name, t) =
The fuel value is computed at runtime from the input
                                                             false, then name does not occur anywhere in t.
length, so the executable faithfully mirrors the verified
model with no gap between proof and implementation. The      Theorem 5 (R1 Completeness). If name occurs in t, then
top-level parser also rejects trailing input and unterminatedcontainsSelfRef (name, t) = true.
strings.                                                     Theorem 6. The base dialect (8 core performatives) is
                                                             R1-valid.
Theorem 1 (Termination). For all inputs s, parseSExpr(s)
terminates and produces either a valid SExpr or a parse Theorem 7 (Mutual Recursion Soundness). If
error.                                                       verifyR1NoMutualRecursion(δ) = true, then no perfor-
                                                             mative in δ participates in a dependency cycle.
   A universal well-formedness theorem (allSExpr_well-
Formed) additionally proves by structural induction that        The mutual recursion verifier uses a computable
every SExpr value satisfies the inductive WellFormedSExpr    DFS-based     cycle detector (checkNoCycles) with full
predicate, ensuring the parser can only produce structurally soundness    and  completeness proofs against a semantic
valid output.                                                mutualRecursion     specification: no false negatives and no
                                                             false positives. The Rust reference implementation mirrors
   In these theorems, e is an SExpr (the S-expression the computable version.
parse tree/AST) and m is a Message (the semantic
classification into simple, meta, dialect, or wrapped). The D. R2: Resource Bounds
predicate ValidMsgGrammar(e, m) is an inductive relation        Constraint R2 enforces static resource limits
encoding which S-expressions constitute valid CBCL mes- (maxDepth ≤ 64, maxExpansionSize ≤ 8192 characters,
sages: it has four constructors corresponding to simple verificationTime ≤ 1000 ms). The Lean 4 model uses a
messages (with one of the eight core performatives), meta fuel parameter: boundedEvalFull decrements a natural-
messages, lang-scoped dialect invocations, and wrapped number counter at each expansion step, returning none
                                                                                      Error
                                                                                          fail
                                                                                3. Verify R1–R3             4. Install
                                                                                   + signature               dialect
                                                    meta



                   1. Parse                      2. Validate                                              6. Deliver to
                                                                           simple / wrapped
                 S-expression                    + classify                                             application layer
                         fail                    fail
                     Error               Error      lang
                                                                                5. Expand template
                                                                                 under resource ctx
                                                                                              fail
                                                                                        Error

Fig. 1. Message processing lifecycle. Steps 1–2 apply to all messages; the upper branch handles dialect definitions (meta), the lower branch
handles dialect invocations (lang), and simple or wrapped messages proceed directly to delivery. Any step may reject with a well-typed error
(Theorem 12).



when fuel reaches zero. The Rust implementation mirrors                G. DCFL Preservation Argument
this for depth and size, adding a wall-clock timeout as
defense-in-depth.                                              The central security property is that installing dialects
                                                             does not push the recognized language beyond DCFL. We
Theorem 8 (Bounded Evaluation). boundedEvalFull(fuel, e, rs) establish this through three steps:
always terminates, producing either a result or none (re-
source exhaustion). A depth-bounded invariant additionally     1) Base case. The core CBCL grammar is LR(1)-
rules out depth creep across nested expansions.                    parseable (indeed LL(1)), hence DCFL.
                                                               2) Extension step. A dialect adds finitely many
Theorem 9. If verifyR2 (δ) = true, then δ’s declared
                                                                   extend clauses that introduce new performative
bounds are within system limits.
                                                                   heads. All dialect invocations must appear inside
                                                                   a (lang name ...) wrapper. DCFLs are not closed
E. R3: Core Preservation                                           under union in general [33]; CBCL avoids this because
   Constraint R3 prevents dialects from redefining the eight       the lang keyword followed by a unique dialect
core performatives.                                                name forms a prefix-free partition: a deterministic
                                                                   pushdown automaton (DPDA) [13] dispatches to
Theorem 10 (Core Preservation). If verifyR3 (δ) = true,            the appropriate subgrammar by consuming the lang
then for all core performative names n, δ does not define n.       tag and dialect name, with no additional lookahead
Theorem 11 (Installation Safety). Installing an R3-verified        beyond LR(1) required. R1 and R2 ensure template
dialect into a well-formed agent preserves well-formedness.        expansion terminates and is resource-bounded, but
                                                                   do not increase parsing power.
F. Pipeline Totality                                           3)  Inductive closure. Since each installation preserves
                                                                   DCFL membership, and the base grammar is DCFL,
   The Lean pipeline from parse → validate → verify                the language remains DCFL after any finite sequence
constraints (for define/define-dialect meta messages)              of dialect installations.
is formalized as runPipeline : String → PipelineResult.
                                                               This argument is fully mechanized in Lean 4. Theorems 2–
Theorem 12 (Pipeline Totality). For all inputs s, 3 establish parser correctness, 4–7 verify R1, 8–9 verify R2,
runPipeline(s) returns a PipelineResult and never diverges. and 10–11 verify R3. The deterministic-union construction
Theorem 13 (Pipeline Soundness). If runPipeline(s) = is proven by agentDetParser_agrees, which shows that
success(m), then s parsed successfully, m satisfies the combined DPDA agrees with the boolean decider for
ValidMsgGrammar, and m passes validation. If m is a agents with unique dialect names (namesUnique). The final
define/define-dialect meta message, its dialect defi- theorem dcfl_preserved composes these results: installing
nition passes R1–R3.                                         a fresh R3-verified dialect preserves DCFL membership.
                         TABLE II                                                             TABLE III
          Reference implementation crates (Rust).                                    Lean 4 verification coverage.

 Crate       LOC Responsibility                                     Component                Thm.   Approach

 cbcl-core   7,800   Agent, evaluator, R1–R3, gossip, canonical     S-Expression types          2   Structural induction
 cbcl-parser 1,900   Recursive-descent S-expr & message parser      Parser                     26   Fuel-based, well-formedness
 cbcl-cli      430   Parse, verify, agent REPL, gossip simulation   Serializer                 51   Round-trip, SafeSymbol
 cbcl-ffi      430   C FFI bindings via cbindgen                    Message parser              9   Soundness + completeness
 cbcl-wasm     490   WebAssembly bindings (optional JS interop)     R1 (no recursion)          13   DFS sound. + complete.
                                                                    R2 (resource bounds)        6   Depth-bounded evaluation
                                                                    R3 (core preservation)      4   Redefinition check
                                                                    Pipeline                    6   Totality + composition
            V. Reference Implementation                             DCFL preservation          50   Det. union + det. parser
                                                                    Agent & dialect model       9   Installation + matching
A. Architecture
                                                                    Total                     176   All machine-checked, zero sorry
   The reference implementation is written in Rust (∼11,000
lines of library code) as a Cargo workspace of five crates
(Table II). The core library (cbcl-core) forbids unsafe a 100-agent network achieves full coverage in ∼3 rounds.
code and uses only alloc, making it suitable for no_std Receiving agents independently verify dialect constraints
environments. An earlier GNU Guile Scheme prototype (R1–R3) and cryptographic signatures before installation.
informed the design but is superseded by the Rust imple-
                                                              E. Canonical Serialization
mentation.
                                                                 For cryptographic operations (signing, hashing), CBCL
B. Dialect Verification Engine                                uses the canonical form of S-expressions specified in
   Upon receiving a dialect definition, the implementation RFC 9804 [14]. This encoding eliminates whitespace vari-
executes: (1) R1 check: walk each template AST for ation and uses length-prefixed verbatim strings, ensuring
self-references and reject if found; additionally reject that structurally identical messages produce identical byte
mutual recursion by detecting cycles in the performative representations, a prerequisite for deterministic signature
dependency graph; (2) R2 check: verify declared bounds verification.
are within system limits; (3) R3 check: reject if any extend                         VI. Evaluation
clause redefines a core performative; (4) Integrity check
(optional): if a cryptographic signer is registered (via a A. Verification Coverage
Signer trait), verify the signature and content hash. The        The Lean 4 formalization covers parsing, validation,
protocol is algorithm-agnostic; the signature algorithm is    dialect parsing/verification for meta definitions, and a fuel-
identified by the dialect’s metadata, allowing deployments    bounded   evaluation model. Table III reports counts for the
to use Ed25519, ECDSA, or post-quantum schemes without        core safety   modules.
protocol changes. Only after all checks pass is the dialect      The  verified parser binary cbcl-parse is extracted from
                                     2
installed. Verification runs in O(|δ| ) time in the size of   the Lean   proofs  and runs 17 built-in test cases covering all
the dialect definition.                                       message   types,  including  negative cases for trailing input
                                                              and unterminated strings.
C. Runtime Resource Enforcement                                  The Rust implementation includes property-based tests
   A ResourceContext struct tracks depth, cumulative (using proptest), differential tests that cross-check the
expansion size, and elapsed wall-clock time during message Rust parser against the Lean-extracted binary, and five
evaluation. Three checks enforce bounds: enter_depth cargo-fuzz targets covering the S-expression parser, mes-
increments the depth counter and returns a resource-limit sage parser, dialect parser, constraint verification, and
error if max_depth is exceeded; check_expansion_limit template expansion. Five example dialects (37 performa-
accumulates expansion size; and check_time_limit com- tives total) have been verified against the implementation
pares elapsed time against the timeout. These checks are (R1–R3 pass): precision agriculture (11 performatives),
invoked at each step of template expansion, ensuring that AI planning (7), cross-chain asset transfer (7), artifact
even adversarially crafted templates cannot exceed their management (7), and email use (5).
declared resource bounds.
                                                              B. Security Testing
D. Epidemic Dialect Propagation                                  We validate CBCL’s security properties against concrete
   Dialects propagate between agents via an epidemic          attack  scenarios:
(gossip) protocol. In a fully-connected topology, classic Recursive expansion attack. A malicious dialect con-
epidemic dissemination analysis [27] yields convergence to taining (extend bomb (x) (bomb (bomb x))) is rejected
full coverage in O(log n) rounds; CBCL builds on this result. at R1 verification; the self-reference is detected before instal-
With transmission probability p = 0.8, empirical testing lation. Mutual recursion (e.g., ping expands to pong, pong
with networks of 10–500 agents matches the O(log n) bound; expands to ping) is also rejected by the implementation.
                       TABLE IV                               parser differential vulnerabilities that arise when different
           Benchmark results (Rust, Apple M4).                implementations interpret the same message differently,
                                                              a problem endemic to protocols with ambiguous gram-
       Operation                          Median time
                                                              mars or natural language content. Canonical serialization
       Parse simple tell message                    78 ns     (Section V-E) further reduces—but cannot fully eliminate—
       Parse meta define                           125 ns
       Parse lang dialect invocation               130 ns     implementation-level divergence in areas such as Unicode
       Pipeline: simple tell (end-to-end)          386 ns     handling.
       Pipeline: meta define (end-to-end)         1.03 µs
       Template expansion (conditional)            215 ns     Explicit computational complexity. Every dialect
       R1 verify full dialect                     1.83 µs     declares its resource requirements, and evaluation is guaran-
       R2 bounded eval (nested)                    185 ns     teed to terminate within those bounds. An implementation
       R3 verify dialect                            21 ns
       Gossip: 100-agent convergence               2.6 ms     can decide before evaluation whether a dialect’s demands
                                                              are acceptable, yielding explicit worst-case resource bud-
                                                              gets. This transforms resource governance from a runtime
Depth bomb. A deeply nested message (lang d1 (lang emergency into a design-time contract.
d2 (lang d3 ...))) exceeding max-depth triggers re- No parser- or expander-induced weird machines.
source exhaustion at the enforced limit, returning an error The restriction to declarative pattern-template expansion
rather than consuming unbounded stack.                        with bounded resources means that the CBCL parser and
Core redefinition. A dialect attempting (extend tell template expander introduce no unintended computational
(x) (drop-table x)) is rejected at R3 verification; tell artifacts. The template language is not Turing-complete; its
is a core performative and cannot be redefined.               semantics are fully determined by a finite substitution table.
                                                              Weird machines could still arise in layers outside CBCL’s
Expansion bomb. A template producing output larger scope (e.g., tool backends or agent action semantics);
than max-expansion-size is halted mid-expansion when CBCL’s guarantee is that the message recognition and
the cumulative size check fires.                              expansion pipeline itself is free of them.
   In all cases, the parser returns a well-typed error value
                                                              B. Comparison with Contemporary Agent Protocols
rather than entering an undefined state. This is the
practical consequence of DCFL preservation: the parser is       The Model Context Protocol (MCP) [7] and similar
deterministic and total, always terminating with a definite LLM agent frameworks use JSON-RPC with unrestricted
accept or reject.                                             schemas. While practical, this design creates an input
                                                              language whose computational complexity depends on
C. Performance                                                the tools agents invoke, potentially reaching Turing-
   Table IV reports Criterion benchmark results for the completeness when they can execute arbitrary code in
Rust implementation on an Apple M4 (macOS 15). The end- response to messages. CBCL demonstrates that meaningful
to-end pipeline (parse → validate → verify) processes a sim- extensibility does not require unbounded input complexity.
ple tell message in under 400 ns and a meta define (in-         KQML [3] and FIPA-ACL [6] have parseable grammars
cluding R1–R3 verification) in ∼1 µs. Template expansion and limited extensibility (KQML’s performative set was
completes in 120–350 ns depending on template complexity. explicitly open; FIPA-ACL supported user-defined message
Constraint verification is dominated by R1 (dependency- parameters), but extensions were unconstrained by formal
graph cycle detection, ∼1.8 µs for a full dialect); R2 and R3 safety guarantees and required out-of-band agreement.
checks complete in under 25 ns each. Gossip simulation of CBCL inherits their grammar tractability while adding
a 100-agent fully-connected network converges in ∼2.6 ms. formally safe runtime evolution.
These numbers indicate that CBCL’s safety checks impose C. Implementation Strategy
negligible overhead relative to typical network round-trip
times.                                                          The Lean 4 formalization and the Rust implementation
                                                              serve complementary roles. Lean provides machine-checked
                        VII. Discussion                       proofs of the safety properties (Theorems 1–13) and yields
A. Relation to LangSec Principles                             an extracted parser binary (cbcl-parse) that is correct by
                                                              construction. However, extracted code optimizes for proof
Verifiable parsers. The Lean 4 formalization produces a structure, not for runtime performance or integration. The
parser with machine-checked soundness and completeness Rust implementation (cbcl-rs) provides a production-
theorems. The extracted binary constitutes a verified quality library with O(n) hand-rolled parsing, C FFI and
recognizer for the CBCL language.                             WebAssembly bindings, property-based and differential
Parser equivalence. Because CBCL specifies a single testing, and fuzz targets—capabilities that are essential
unambiguous grammar that is LR(1)-parseable (and indeed for adoption but outside the scope of formal verification.
LL(1)), all conformant parsers produce identical parse The two implementations are cross-validated: the Rust
trees for every input. This eliminates the grammar-level parser’s test suite includes differential tests against the
Lean-extracted binary, ensuring that both accept and reject    excluding orthophrase (adding orthogonal features) and
the same inputs.                                               metaphrase (altering interpretation rules). This ceiling is a
                                                               deliberate trade-off: it exists precisely to bound the attack
D. Toward Semantic Guidance                                    surface. Agents requiring these patterns must implement
   CBCL guarantees syntactic safety but not semantic           them in application logic outside the CBCL layer.
agreement. Several mechanisms could narrow this gap, with         Trust infrastructure. CBCL specifies algorithm-
different complexity implications. Examples (supported via     agnostic dialect signing (via an abstract Signer interface)
:examples in dialect definitions) and typed parameter decla-   but does not define key distribution, certificate authorities,
rations add no formal complexity and remain within DCFL.       or revocation. These are left to deployment infrastructure.
Interaction protocol state machines (e.g., after ask, expect      Dialect identity and naming. The DCFL preservation
reply) are regular, well below DCFL. Pre/postconditions        proof (dcfl_preserved) requires unique dialect names per
and ontological commitment [12] risk crossing the complex-     agent (namesUnique), since the lang tag dispatches by
ity boundary CBCL is designed to enforce, and would need       name. The true identity of a dialect is the content hash of
to be scoped carefully or relegated to an application layer    its canonical encoding (RFC 9804); two dialects with the
above the protocol. The :examples clause offers a machine-     same name but different hashes are rejected at installation,
checkable anchor: a receiving agent should expand each         mitigating name collisions and downgrade attempts. Dialect
example input through its own expander and compare             churn is bounded by R2 resource limits but requires
the result against the expected output before claiming         deployment-level rate limiting for full mitigation.
dialect support. This catches the most common interoper-          Dialect quality and bloat. CBCL constrains dialect
ability failures (template misconfiguration, parameter-type    safety but not dialect quality. Nothing prevents propagation
disagreement) before they manifest at runtime, though          of redundant or poorly designed dialects. Agents can
it cannot detect deeper semantic divergence. Following         uninstall unhelpful dialects, but the protocol does not
Singh [19], CBCL treats dialect installation as a public       define curation mechanisms, leaving lifecycle management
commitment to the dialect’s declared semantics; semantic       to agent policy.
divergence is thus a breach of commitment, observable             Performance. The fuel-based termination model in
and accountable, rather than a hidden failure of shared        the Lean formalization is sound but conservative. The
mental state. We are investigating structural contracts        reference implementation’s runtime resource enforcement
that extend CBCL’s syntactic safety toward protocol            adds overhead proportional to the number of expansion
correctness while remaining within DCFL and requiring          steps.
no coordination. Protocol constraints are expressed as
causal dependency graphs over performative types; each                           VIII. Related Work
message carries an explicit causal reference (a content
                                                               A. Language-Theoretic Security
hash of its predecessor’s canonical serialisation), forming
a Merkle DAG that is cryptographically tamper-evident             Sassaman et al. [1] established the foundation for
and independently verifiable. Verification is a monotonic      language-theoretic security, observing that mismatch be-
predicate on the append-only message store, coordination-      tween an input language’s complexity and the parser’s
free by the CALM theorem [34]. Message shape constraints       recognizer class raises the likelihood of exploitable errors,
are expressed as visibly pushdown languages [32] over          and that unanticipated computational artifacts (“weird
expanded S-expressions, exploiting the decidable inclusion     machines”) arise when input handling violates designer
checking that VPLs provide. The full design is implemented     assumptions. Kaminsky, Patterson, and Sassaman [16]
in cbcl-rs and will be described in a forthcoming report.      demonstrated this concretely with parser differential at-
                                                               tacks against the X.509 PKI infrastructure. Sassaman et
E. Limitations                                                 al. [17] extended the analysis to network stacks, framing
   Expressiveness ceiling. DCFL restriction means some         protocol insecurity as instances of the halting problem.
patterns cannot be expressed in dialect templates. Concrete    Momot et al. [15] developed a taxonomy of LangSec errors
examples of inexpressible patterns include: (1) recursive      and proposed actionable CWE refactorings to address them.
data transformations such as flattening a nested list          CBCL is, to our knowledge, the first protocol designed from
of arbitrary depth; (2) cross-field references where one       the ground up on these principles for agent communication,
parameter’s value depends on another parameter’s content       and the first to demonstrate that LangSec constraints are
(e.g., a checksum computed over other fields); (3) iteration   compatible with runtime language self-extension.
or aggregation over variable-length collections (e.g., sum-       Von Hippel and Miyazono [28] argue that AI security is
ming line items in an invoice); and (4) context-sensitive      fundamentally a LangSec problem, identifying structured
validation such as ensuring a reply’s thread ID matches an     output parsing and tool-use capabilities in LLM-based
earlier message. In Standish’s extensibility taxonomy [31],    systems as key attack surfaces. Their analysis reinforces the
CBCL restricts itself to paraphrastic extension (defining      premise underlying CBCL: that securing agent communi-
new constructs in terms of existing ones), deliberately        cation requires constraining the computational complexity
of the input language, not merely adding ad-hoc validation    verification, addresses this root cause by making provenance
layers.                                                       syntactically explicit. Zhou et al. [24] show that pro-
   Fazeldehkordi et al. [18] demonstrated that uncon-         jecting high-dimensional LLM states to natural-language
strained communication patterns between distributed finan-    tokens is many-to-one and non-invertible, compounding
cial agents can enable DDoS through call-based flooding       information loss across conversational turns. A decidable
cycles, using static analysis to detect these patterns at     formal language avoids this lossy bottleneck by making
design time. CBCL addresses a related concern at the          coordination semantics explicit in the message structure.
protocol layer: R2 resource bounds ensure that processing     Borazjanizadeh and Piantadosi [25] provide complementary
any message, including dialect expansion, terminates within   evidence. Pairing LLMs with a formal symbolic engine (Pro-
declared limits.                                              log) outperforms pure natural-language chain-of-thought on
                                                              deductive tasks, suggesting that structured representations
B. Agent Communication Languages                              improve multi-step reasoning.
   KQML [3] introduced speech-act performatives for agent
communication; FIPA-ACL [6] later codified 22 perfor- C. Language Extensibility and Formal Methods
matives with mental-state semantics. Both supported                McCarthy’s 1982 proposal [9] envisioned open-ended
extensibility: KQML through an explicitly open perfor- business communication. Flatt [11] showed how language
mative set (communities could define new performatives by extensibility can be systematized through first-class lan-
agreement), FIPA-ACL through X- prefixed user-defined guage definitions in Racket. CBCL adapts this principle for
message parameters. Gruber’s Ontolingua [12] addressed adversarial distributed environments and makes the safety
the content layer separately. Building on McCarthy and constraints explicit.
Hayes’s [8] principle that what is represented can be speci-
                                                                   Demers et al. [27] established the O(log n) convergence
fied independently of how it is computed, Gruber showed
                                                                bound for epidemic information dissemination, which
that interoperability between heterogeneous agents requires
                                                                underlies CBCL’s dialect propagation protocol. Jelasity et
formal ontological commitment: each agent must commit
                                                                al. [26] developed theoretical foundations for gossip-based
to the declarative specification of shared concepts (classes,
                                                                aggregation, proving that the per-round convergence factor
relations, and the axioms constraining their use), with no
                                                                is independent of network size; their gossip framework
commitment to the form or content of knowledge internal
                                                                informs CBCL’s peer-selection strategy. RFC 9804 [14]
to the agent. CBCL’s dialect mechanism inherits this com-
                                                                specifies a canonical form for S-expressions used in CBCL
mitment architecture; a dialect definition is a declarative
                                                                for deterministic signature verification.
specification to which the installing agent publicly binds
itself, independent of its internal representation. Gruber                           IX. Conclusion
left the process of reaching consensus on shared ontologies
as an open problem, and treated ontology specification             CBCL demonstrates that the LangSec principle of match-
as separable from the communication protocol, so that ing input language complexity to recognizer capability can
extending shared meaning required out-of-band agreement be applied even to self-extending protocols. By constraining
invisible to protocol-level safety analysis. CBCL addresses dialect definitions to declarative pattern-template substitu-
the consensus problem directly: agents propose, query, and tions within S-expression syntax, we show that meaningful
adopt dialect definitions as ordinary protocol messages. runtime extensibility and provable parsing safety are not in
Singh [19] identified a complementary flaw: reliance on conflict. Because safety constraints are machine-checked at
unverifiable mental states rather than observable social installation, agents can create and adopt dialects ad hoc,
commitments. CBCL makes dialect installation a protocol- without external coordination.
level action subject to machine-checked safety constraints.        As autonomous agent systems proliferate, the choice
   Yang et al. [21] survey AI agent protocols across seven of communication substrate becomes a security decision.
evaluation dimensions. Deng et al. [22] survey security Natural language and unrestricted schemas offer maximal
threats to AI agents, organising them around prompt injec- flexibility but cannot guarantee that two agents interpret
tion, tool-use risks, and adversarial multi-agent interactions. the same message identically, a source of coordination
CBCL’s DCFL constraint directly addresses the parser- failure even among cooperative agents and a fundamentally
level attack surface underlying prompt injection: because unsecurable attack surface in adversarial settings. CBCL
dialect extensions are structurally distinct from message offers an alternative: a formally specified, machine-verified
content, an agent’s parser never conflates instructions with protocol where every message, including those that extend
data. Zhang et al. [23] demonstrate this concretely: their the language itself, is parsed in bounded time by a
ClawWorm worm achieves a 64.5% attack success rate deterministic pushdown automaton. If agents communicate
against the OpenClaw framework by exploiting a flat in languages whose validity is undecidable, no monitor can
context trust model in which LLMs cannot distinguish reliably determine what they have agreed to do. Formally
owner instructions from arbitrary channel input. CBCL’s bounding what agents can express to each other is a
lang-scoped dialect mechanism, combined with R1–R3 precondition for oversight.
Availability. The reference implementation, Lean 4 for-                      [12] T. R. Gruber, “A translation approach to portable ontology
malization, verified parser binary, and IETF Internet-Draft                       specifications,” Knowledge Acquisition, vol. 5, no. 2, pp. 199–220,
                                                                                  1993.
are available at https://codeberg.org/anuna/cbcl-rs under                    [13] J. E. Hopcroft, R. Motwani, and J. D. Ullman, Introduction to
the Apache 2.0 license. The Nostr transport binding is at                         Automata Theory, Languages, and Computation, 3rd ed. Pearson,
https://codeberg.org/anuna/cbcl-nostr.                                            2006.
                                                                             [14] R. L. Rivest and D. E. Eastlake 3rd, “Simple Public Key
                                                                                  Infrastructure (SPKI) S-expressions,” RFC 9804, 2025.
                       Acknowledgments                                       [15] F. Momot, S. Bratus, S. M. Hallberg, and M. L. Patterson, “The
  Thanks to Claire Barnes, David Factor, Mat Mytka,                               seven turrets of Babel: A taxonomy of LangSec errors and how
                                                                                  to expunge them,” in Proc. IEEE Cybersecurity Development
Mark Pesce, Marc Ahrens, Prof. Ingo Weber, Dr Max Ott,                            (SecDev), pp. 45–52, 2016.
Dr Mark Staples, Dr Ho-Pun Lam, Dr Adnene Guabtni,                           [16] D. Kaminsky, M. L. Patterson, and L. Sassaman, “PKI layer cake:
and DZJ for helpful discussions. Thanks to Ric Richardson                         New collision attacks against the global X.509 infrastructure,”
                                                                                  in Financial Cryptography and Data Security, vol. 6052, pp. 289–
and the Office for Innovation for championing this effort.                        303, 2010.
This work was inspired by problems encountered during                        [17] L. Sassaman, M. L. Patterson, S. Bratus, and A. Shubina, “The
a Science and Industry Endowment Fund project through                             halting problems of network stack insecurity,” ;login: USENIX
                                                                                  Magazine, vol. 36, no. 6, 2011.
CSIRO’s Data61, and the need for ad-hoc knowledge                            [18] E. Fazeldehkordi, O. Owe, and T. Ramezanifarkhani, “A
sharing across agricultural supply networks.                                      language-based approach to prevent DDoS attacks in distributed
                                                                                  financial agent systems,” in Computer Security, vol. 11981,
AI Disclosure. In accordance with IEEE policy, the                                pp. 258–277, 2020.
author discloses that AI assistants were used throughout                     [19] M. P. Singh, “Agent communication languages: Rethinking the
this work, including drafting and editing this manuscript,                        principles,” Computer, vol. 31, no. 12, pp. 40–47, 1998.
                                                                             [20] F. Zambonelli, N. Bicocchi, G. Cabri, L. Leonardi, and M. Pu-
assisting with the Lean 4 formalization, contributing to the                      viani, “On self-adaptation, self-expression, and self-awareness
reference implementation, and aiding in literature review.                        in autonomic service component ensembles,” in Proc. IEEE 5th
Tools used include llm-md, Anthropic’s Claude Code, and                           Conf. on Self-Adaptive and Self-Organizing Systems Workshops
                                                                                  (SASOW), pp. 108–113, 2011.
OpenAI’s Codex. Agent orchestration was coordinated                          [21] Y. Yang et al., “A survey of AI agent protocols,”
using hence, the author’s defeasible-logic meta-control                           arXiv:2504.16736, 2025.
planner for multi-agent LLM task coordination. All work                      [22] Z. Deng et al., “AI agents under threat: A survey of key security
                                                                                  challenges and future pathways,” ACM Computing Surveys,
was directed, reviewed, and validated by the author. The                          vol. 57, no. 7, pp. 1–36, 2025.
author takes full responsibility for the content of this                     [23] Y. Zhang et al., “ClawWorm: Self-propagating attacks across
publication.                                                                      LLM agent ecosystems,” arXiv:2603.15727, 2026.
                                                                             [24] P. Zhou, Y. Feng, H. Julaiti, and Z. Yang, “Why do AI agents
                                                                                  communicate in human language?” arXiv:2506.02739, 2025.
                            References                                       [25] N. Borazjanizadeh and S. T. Piantadosi, “Reliable reasoning
 [1] L. Sassaman, M. L. Patterson, S. Bratus, and M. E. Locasto,                  beyond natural language,” arXiv:2407.11373, 2024.
     “Security applications of formal language theory,” IEEE Systems         [26] M. Jelasity, A. Montresor, and O. Babaoglu, “Gossip-based
     Journal, vol. 7, no. 3, pp. 489–500, Sep. 2013.                              aggregation in large dynamic networks,” ACM Trans. Comput.
 [2] S. Bratus, M. E. Locasto, M. L. Patterson, L. Sassaman, and                  Syst., vol. 23, no. 3, pp. 219–252, 2005.
     A. Shubina, “Exploit programming: From buffer overflows to              [27] A. Demers et al., “Epidemic algorithms for replicated database
     ‘weird machines’ and theory of computation,” ;login: USENIX                  maintenance,” in Proc. 6th ACM Symp. on Principles of Dis-
     Magazine, vol. 36, no. 6, Dec. 2011.                                         tributed Computing (PODC), pp. 1–12, 1987.
 [3] T. Finin, R. Fritzson, D. McKay, and R. McEntire, “KQML as              [28] M. Von Hippel and E. Miyazono, “Research report: AI security
     an agent communication language,” in Proc. 3rd Int. Conf. on                 is a LangSec problem,” in Proc. IEEE Security and Privacy
     Information and Knowledge Management, pp. 456–463, 1994.                     Workshops (SPW), pp. 73–78, 2025.
 [4] M. T. Kone, A. Shimazu, and T. Nakajima, “The state of the art          [29] N. Chomsky, “Three models for the description of language,” IRE
     in agent communication languages,” Knowledge and Information                 Transactions on Information Theory, vol. 2, no. 3, pp. 113–124,
     Systems, vol. 2, no. 3, pp. 259–284, 2000.                                   1956.
 [5] B. Chaib-draa and F. Dignum, “Trends in agent communication             [30] Fiatjaf, “Nostr: Notes and Other Stuff Transmitted by Re-
     language,” Computational Intelligence, vol. 18, no. 2, pp. 89–101,           lays (NIP-01),” 2020. [Online]. Available: https://github.com/
     2002.                                                                        nostr-protocol/nips/blob/master/01.md
 [6] Foundation for Intelligent Physical Agents, “FIPA ACL specifi-          [31] T. A. Standish, “Extensibility in programming language design,”
     cations,” 2002. [Online]. Available: https://web.archive.org/web/            in Proc. National Computer Conference and Exposition, pp. 287–
     2023/http://www.fipa.org/repository/aclspecs.html                            290, 1975.
 [7] Anthropic, “Model Context Protocol specification,” 2025. [On-           [32] R. Alur and P. Madhusudan, “Visibly pushdown languages,”
     line]. Available: https://modelcontextprotocol.io/specification/             in Proc. 36th ACM Symp. on Theory of Computing (STOC),
     2025-03-26                                                                   pp. 202–211, 2004.
 [8] J. McCarthy and P. J. Hayes, “Some philosophical problems from          [33] S. Ginsburg and S. Greibach, “Deterministic context free lan-
     the standpoint of artificial intelligence,” in Machine Intelligence 4        guages,” Information and Control, vol. 9, no. 6, pp. 620–648,
     (B. Meltzer and D. Michie, eds.), pp. 463–502, Edinburgh                     1966.
     University Press, 1969.                                                 [34] J. M. Hellerstein and P. Alvaro, “Keeping CALM: When dis-
 [9] J. McCarthy, “Common business communication language,” in                    tributed consistency is easy,” Communications of the ACM,
     Textverarbeitung und Bürosysteme (A. Endres and J. Reetz,                    vol. 63, no. 9, pp. 72–81, 2020.
     eds.), R. Oldenbourg Verlag, 1982. [Online]. Available: https:
     //www-formal.stanford.edu/jmc/cbcl2.pdf
[10] H. O’Connor, “CBCL: A self-extensible agent communication
     language,” Internet-Draft draft-cbcl-00, 2025.
[11] M. Flatt, “Creating languages in Racket,” Communications of
     the ACM, vol. 55, no. 1, pp. 48–56, 2012.
