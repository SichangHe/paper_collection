                                         GenOS: Compositional Certificates for Semantic Robustness in AI
                                                               Code Generation
                                                                             Corrado Priami
                                              Dipartimento di Informatica, Università di Pisa and Fondazione Start Attractor
                                                                       corrado.priami@unipi.it


                                        Abstract                                                     Introduction
                                        AI coding agents are stochastic programs: a prompt           A contemporary AI programming system is not a
                                        is interpreted, candidate artifacts are sampled, val-        function from text to code. It is a workflow: interpret
                                        idators return observations, and an orchestrator             an instruction, retrieve context, sample one or more
                                        commits or repairs. Small changes to a prompt                artifacts, execute tests or proof tools, repair failures,
arXiv:2608.03588v1 [cs.PL] 4 Aug 2026




                                        or specification can therefore change a distribution         and decide whether to commit. Systems such as Jig-
                                        of program behaviors even when the texts appear              saw combine neural generation with program analy-
                                        synonymous. Existing code-generation systems and             sis and synthesis Jain et al. [2022]; Clover, AutoSpec,
                                        benchmarks measure correctness, but do not pro-              and VeCoGen place formal checking inside iterative
                                        vide a compositional criterion for when one prompt,          generation loops Sun et al. [2024], Wen et al. [2024],
                                        contract, generator, or program may safely replace           Sevenhuijsen et al. [2024]; and prompt languages
                                        another inside a complete agentic workflow.                  such as LMQL make model interaction and con-
                                           We introduce GenOS, a probabilistic operational           straints programmable Beurer-Kellner et al. [2023].
                                        semantics for this replacement problem. Each layer           These systems expose a semantic problem that pass
                                        is a Markov kernel and each semantic interface car-          rates alone do not answer:
                                        ries an observer-relative equivalence. Our main re-
                                                                                                          When can one component of a stochastic
                                        sult proves that an equivalence-compatible kernel
                                                                                                          code-generation workflow be replaced by
                                        descends to quotient classes and that quotienting
                                                                                                          another without changing the behavior ob-
                                        commutes with distributional extension and sequen-
                                                                                                          servable at the end of the workflow?
                                        tial composition. Consequently, equivalent prompts
                                        induce equal probabilities for every downstream                 Textual equality is too strong and informal syn-
                                        equivalence-closed event, including verified com-            onymy is too weak. “Return a sorted copy” and “pro-
                                        mit. We further prove an operational workflow-               duce a nondecreasing permutation without modify-
                                        bisimulation theorem, guarded-commit safety under            ing the input” may denote the same contract. Two
                                        sound validation, total-variation non-expansiveness,         generators may assign different probabilities to syn-
                                        and an additive robustness bound that isolates ap-           tactically distinct programs but the same mass to
                                        proximation defects at individual pipeline layers.           behavioral classes. A test suite may identify pro-
                                           An executable insertion-sort audit instantiates the       grams that a mutation-sensitive observer separates.
                                        theory with natural-language paraphrases, a formal           A verifier can preserve safety even when the gener-
                                        contract, six concrete programs, two program ob-             ator is unreliable, but only if the commit guard is
                                        servers, and exhaustive execution on 121 inputs.             connected formally to target-language truth.
                                        Equivalent prompts have identical code-class and                We propose GenOS (Generative Operational Se-
                                        commit distributions; a prompt with 5% mass on               mantics), a layered semantics in which prompts, con-
                                        an in-place contract is separated by a mutation ob-          tracts, code artifacts, validator outcomes, and work-
                                        server while its downstream distances remain below           flow observations are linked by probability kernels.
                                        the predicted bound. Twenty thousand randomized              At each interface, an equivalence states what the
                                        finite-kernel trials produce no violation of the ex-         next layer is allowed to forget. The central proof
                                        act or approximate laws. The framework is model-             obligation is compatibility: equivalent inputs must
                                        parametric: compatibility is a measurable property           induce equal mass on equivalent outputs. Compati-
                                        to test, not an assumption that language models au-          bility yields a quotient kernel, and quotienting com-
                                        tomatically satisfy.                                         mutes with composition. This turns a local condition

                                                                                                 1
at each interface into an end-to-end semantic certifi-         complementary: it treats prompt interpretation and
cate.                                                          formalization as kernels, then relates their quotient
                                                               behavior to generated programs and commit deci-
Contributions. (1) We define an observer-                      sions.
relative kernel semantics for prompt-driven code
generation, including a probabilistic labelled tran-           Operational and probabilistic semantics.
sition system (PLTS) for generate–check–repair–                Our transition-based view follows structural opera-
commit workflows. (2) We prove the commuting                   tional semantics Plotkin [2004]; the lifting of equiv-
quotient theorem: compatible kernels induce well-              alence to distributions follows probabilistic bisimu-
defined quotient kernels, and quotienting commutes             lation and probabilistic automata Larsen and Skou
with Kleisli composition. (3) We derive prompt-                [1991], Segala and Lynch [1995], Baier and Katoen
replacement and workflow-bisimulation corollaries,             [2008]. Pi-calculus is structurally appropriate for
plus guarded-commit safety. (4) We introduce a                 communicating agents Milner [1999], but classical
quotient total-variation metric and prove non-                 stochastic pi-calculus places rates on actions Priami
expansiveness and an additive bound for approxi-               [1995]. Model calls instead expose uncertainty over
mately compatible layers. (5) We provide an exe-               which artifact is produced, motivating transitions to
cutable finite audit with concrete Python programs,            distributions over artifacts and successor configura-
exhaustive observers, exact distributions, and ran-            tions.
domized law checking.
   The aim is not to claim that a particular model
is invariant to paraphrase. FormalBench, for exam-             Layered Generative Operational
ple, reports substantial instability under semantics-          Semantics
preserving transformations Le-Cong et al. [2025].
GenOS makes such instability a quantified interface            We use finite distributions; countable and measur-
defect and shows how it propagates.                            able versions follow with standard kernel assump-
                                                               tions. For a set X, D(X) is the set of finitely sup-
                                                               ported probability distributions on X, and δx is the
Related Work                                                   point distribution at x. A kernel K : X → D(Y ) has
                                                               affine extension
AI code generation and validation. Hu-
manEval and MBPP established functional evalu-
                                                                                        X
                                                                           K † (µ)(y) =    µ(x)K(x)(y).
ation for code synthesis Chen et al. [2021], Austin                                      x
et al. [2021]; EvalPlus demonstrates that weak test
suites induce overly coarse notions of correctness             For K : X → D(Y ) and L : Y → D(Z), sequential
Liu et al. [2023]. In GenOS, a test suite, prover,             composition is (K ; L)(x) = L† (K(x)).
or analyzer is an observer whose discriminating                  A minimal pipeline has prompt sources P , con-
power explicitly determines program equivalence.               tracts S, generated artifacts C, and observations O:
Jigsaw uses semantic post-processing Jain et al.                          Front        Gen        Obs
[2022], while Clover, AutoSpec, VeCoGen, and re-                       P −−−→ D(S) −−→ D(C) −−→ D(O).
cent formal-verification pipelines use generated an-
                                                               When validation depends on the contract, gener-
notations, proof obligations, and repair feedback Sun
et al. [2024], Wen et al. [2024], Sevenhuijsen et al.          ation preserves the contract tag: Gen(s)
                                                                                                     d      is a dis-
[2024], Councilman et al. [2025]. These systems mo-            tribution on S × C with first component s, and
tivate guarded workflows, but they do not state con-           Obs : S ×C → D(O). Observations may record tests,
ditions under which equivalence at one pipeline layer          proof results, diagnostics, repair requests, resource
is preserved by all subsequent layers.                         use, mutation, exceptions, or commit.
                                                                  Table 1 summarizes the proof obligation at each
                                                               interface. The equivalences are not required to be
Prompts and formal specifications. LMQL
                                                               identical across applications: a security audit can re-
gives prompts control flow and output constraints
                                                               fine the code observer with information-flow events,
Beurer-Kellner et al. [2023]. nl2spec maps natural
                                                               while a cost audit can add time or token use to work-
language to temporal logic while exposing ambiguity
                                                               flow observations.
for interactive correction Cosler et al. [2023]. Formal-
                                                                  The same kernels generate a PLTS. A configura-
Bench evaluates specification consistency, complete-
                                                               tion contains a control location, semantic value, con-
ness, and robustness Le-Cong et al. [2025]. GenOS is
                                                               text, and provenance trace. A model call steps to a


                                                           2
      Layer        Typical         Local audit                 contract relation is
                   equivalence     obligation
      Intent       Same            Paraphrases                  sRS s′   ⇐⇒      ∀c, c′ . cRC c′ ⇒ (s |= c ⇔ s′ |= c′ ).
                   contract        formalize alike
                   mass                                        This definition says that equivalent contracts select
      Generate     Same            Syntax preserves            the same accepted code classes, not necessarily the
                   behavior        behavior                    same syntax or proof obligations. A deterministic
                   mass
      Validation   Same            Tools distinguish           validator is extensional when its verdict and diag-
                   verdict class   selected classes            nostic class depend only on [s] and [c].
      Control      Same            Replacement is
                   abstract        safe in context             Proposition 1 (Validator compatibility). If con-
                   trace                                       tract satisfaction is closed under (RS , RC ) and a val-
                                                               idator is extensional, then the tagged validation ker-
Table 1: Semantic interfaces and their local compat-           nel on S × C is compatible with the product equiva-
ibility obligations.                                           lence. If its accept verdict is also sound, the resulting
                                                               commit observation is both equivalence-preserving
                                                               and safe.
distribution; deterministic parsing, communication,
and commit rules step to point distributions. For                The proposition distinguishes two properties that
example,                                                       are often conflated. Extensionality states that equiv-
                                                               alent inputs receive equivalent observations; sound-
                       sample
  ⟨generate(s), Γ, κ⟩ −−−−→                                    ness states that acceptance implies semantic truth.
                       X                                       Either can hold without the other.
                          Gen(s)(c) δ⟨check(s,c),Γ,κc⟩ .
                         c
                                                               Compositional Certificates
Thus the kernel and operational views describe the
same transition structure at different granularities.          Theorem 1 (Quotient kernel and commuting
                                                               square). If K : X → D(Y ) is (RX , RY )-compatible,
Observer-relative equivalence. Let RX be an                    then
equivalence on X and qX : X → X/RX its quotient                              K([x]) = (qY )# (K(x))
map. The lifting to distributions compares probabil-           defines a unique kernel K : X/RX → D(Y /RY ).
ity mass on equivalence classes.                               Moreover, for every µ ∈ D(X),
Definition 1 (Lifted equivalence). For µ, ν ∈                                               †
                                                                          (qY )# K † (µ) = K (qX )# µ .
                                                                                                    
D(X), write µ RX ν iff, for every class E ∈ X/RX ,
µ(E) = ν(E). Equivalently, (qX )# µ = (qX )# ν.
                                                               Proof. Compatibility makes the definition indepen-
   Program equivalence is deliberately parameter-              dent of the representative x. For a class B ∈ Y /RY ,
                                                               both sides equal x µ(x)K(x)(qY−1 (B)) after group-
                                                                                P
ized by an observer. A return-value observer may
equate a pure sort with an in-place sort; an observer          ing the outer sum by RX -classes. Uniqueness follows
that also records the post-state separates them. Con-          because point distributions on quotient classes deter-
tract equivalence can be defined extensionally by              mine a kernel.
satisfaction over program classes, and prompt equiv-
                                                               Theorem 2 (Quotients commute with composi-
alence by the contract-class mass induced by Front.
                                                               tion). Let K : X → D(Y ) and L : Y → D(Z)
Definition 2 (Compatible kernel). A kernel K :                 be compatible with (RX , RY ) and (RY , RZ ), respec-
X → D(Y ) is (RX , RY )-compatible when xRX x′ im-             tively. Then K ; L is (RX , RZ )-compatible and
plies K(x) RY K(x′ ).
                                                                                   K ; L = K ; L.
  Compatibility is the semantic substitutability test
                                                               Proof. Apply Theorem 1 first to L† (K(x)), then to
for a layer. It is inspectable empirically by repeated                                             †
sampling and classifying outcomes, or proved for de-           K(x). The resulting pushforward is L (K([x])).
terministic front ends and symbolic transformations.
                                                               Corollary 1 (End-to-end prompt replacement). If
                                                               all layers of a GenOS pipeline are compatible and
Contracts and extensional validators. Let |=                   prompts p, p′ induce equivalent contract distribu-
⊆ S × C be target-language satisfaction. A useful              tions, then the final observation distributions agree


                                                           3
on every RO -class. Hence every equivalence-closed             Repair, Iteration, and Prove-
event A ⊆ O, including a commit event, has equal
probability under p and p′ .
                                                               nance
  This result separates syntax-level variation from            A core workflow grammar is sufficient to expose it-
observable semantic variation. Artifact probabilities          erative behavior:
may differ substantially; only class mass must be
                                                                  W ::= generate(s) | check(s, c) | repair(s, c, d)
preserved.
                                                                          | commit(s, c) | W ; W | repeat(W ).
Operational consequence. Relate two workflow                   The configuration trace records events such as gener-
configurations when they are at the same control               ated artifacts, checker results, diagnostics, and com-
location, their current values are equivalent, and             mits. Rules only append events.
their traces agree after quotienting recorded arti-
facts and observations. Each deterministic rule is             Proposition      2     (Trace   monotonicity). If
matched by a point transition, and each stochastic             ⟨W, Γ, κ⟩ → µ, every configuration in supp(µ)
rule is matched by compatibility.                              has a trace with prefix κ. Therefore provenance is
                                                               monotone along every finite execution.
Theorem 3 (Workflow bisimulation). If every
stochastic action kernel in two structurally identical            Trace monotonicity makes a compatibility claim
GenOS workflows is compatible and deterministic                auditable: the class labels and decisions used to jus-
rules respect the selected equivalences, the induced           tify replacement can be reconstructed from the run.
configuration relation is a probabilistic bisimulation.        Traces may be quotiented for privacy, provided the
Consequently, the workflows assign equal probability           retained abstraction still contains the observations
to every equivalence-closed finite trace cylinder.             named by the certificate.
                                                                  Repair is a new model call conditioned on the re-
  The proof is by cases on the operational rules. The          jected artifact and diagnostic. Let An be the event
theorem supports local replacement inside loops and            that attempt n is accepted, conditional on all earlier
agent networks, not only a fixed acyclic pipeline.             failures. A useful progress theorem requires a lower
                                                               bound on conditional success, but not independence.
Guarded commitment. Let s |= c mean that
target artifact c satisfies contract s. A checker is           Theorem 5 (Conditional repair progress). Suppose
sound when Check(s, c) = accept implies s |= c. The            a sound guarded workflow retries after rejection and,
commit rule is guarded when only accepted pairs can            for every history with no earlier acceptance, Pr(An |
reach commit(c).                                               ¬A1 , . . . , ¬An−1 ) ≥ p > 0. Then

Theorem 4 (Safe commit). In a guarded workflow                 Pr(no acceptance in the first n attempts) ≤ (1−p)n .
with a sound checker, every reachable committed ar-
                                                               Thus acceptance occurs almost surely if retries con-
tifact satisfies its associated contract, independent of
                                                               tinue indefinitely; every artifact eventually commit-
the generator distribution and repair policy.
                                                               ted is correct by Theorem 4.
Proof. The final transition into a committed state
                                                               Proof. By the chain rule, the probability of n con-
requires a preceding accept observation. Soundness
                                                               secutive failures is the product of their conditional
converts this observation into s |= c; earlier stochas-
                                                               probabilities. Each is at most 1−p, giving the bound.
tic choices are irrelevant.
                                                               No independence premise is used.
   The theorem does not claim completeness: cor-
                                                                  This theorem identifies what an empirical repair
rect programs may be rejected. It also exposes a
                                                               study should estimate: a history-uniform or history-
key boundary. Tests or learned judges usually jus-
                                                               stratified lower bound, rather than an unconditional
tify only a weaker, probabilistic soundness claim,
                                                               average success rate that can hide repeated failure
whereas proof-producing or sound static tools can
                                                               modes.
justify the premise directly.

                                                               Approximate Robustness
                                                               Exact class-mass equality is often too strict for sam-
                                                               pled models. Define the quotient total-variation dis-


                                                           4
tance                                                             Theorem 8 (Finite-sample certificate). For a fixed
                                                                  input x and 0 < δ < 1, with probability at least 1 − δ,
          dRX (µ, ν) = TV((qX )# µ, (qX )# ν),                                                      r
                                                                           b N (x)(E) − K(x)(E)| ≤ log(2m/δ) .
                        X
          TV(α, β) = 12    |α(u) − β(u)|.                            max |K
                              u                                        E                                    2N

Theorem 6 (Non-expansiveness).                  If   K   is       For M tested input pairs, let dbj and dj be their em-
(RX , RY )-compatible, then                                       pirical and population quotient total variations. If

             dRY (K † µ, K † ν) ≤ dRX (µ, ν).                                                 m2       4mM
                                                                                      N≥           log     ,
                                                                                              2τ 2       δ
Proof. By Theorem 1, both outputs are obtained by
applying the same quotient kernel K to the quo-                   then |dbj −dj | ≤ τ simultaneously for every pair, with
tient inputs. Total variation contracts under every               probability at least 1 − δ.
Markov kernel.
                                                                  Proof. Apply Hoeffding to each class frequency and
   To diagnose imperfect layers, define their compat-             union-bound over m classes, two endpoints, and M
ibility defect                                                    pairs. With coordinate error at most τ /m, each end-
                                                                  point has ℓ1 error at most τ ; the reverse triangle
          def(K) = sup dRY (K(x), K(x′ )).                        inequality for ℓ1 gives total-variation error at most
                     xRX x′
                                                                  τ.
A defect of zero recovers exact compatibility. The                   The independence condition concerns repeated
next theorem turns interface defects into an end-to-              sampling, not repair attempts in Theorem 5. If an
end error budget.                                                 API changes model versions or uses stateful caching,
Theorem 7 (Additive robustness budget). For any                   the audit must stratify runs or use a dependence-
kernel K : X → D(Y ),                                             aware confidence method. For an observed empirical
                                                                  defect ηb, Theorem 8 supplies an upper confidence
        dRY (K † µ, K † ν) ≤ dRX (µ, ν) + def(K).                 value η + ; substituting η + into Theorem 7 yields a
                                                                  high-probability end-to-end certificate.
For a chain K1 ; · · · ; Kn , the final P
                                        distance is at most          A practical audit has five steps. First, declare the
the initial quotient distance plus i def(Ki ).                    observational properties and resulting equivalence
Proof sketch. Match the common mass that (qX )# µ                 classes. Second, freeze or record the model, tools,
and (qX )# ν assign to each input class, coupling                 decoding parameters, and context. Third, sample
matched samples within that class. Their output                   each proposed replacement pair and classify out-
quotient distributions differ by at most def(K). Un-              puts. Fourth, estimate class distances and confidence
matched quotient mass is at most dRX (µ, ν) and can               bounds. Fifth, compose the upper bounds across
contribute at most that amount. Iteration gives the               the workflow and separately verify the soundness
chain bound.                                                      premise of any commit guard. A failed compatibility
                                                                  test is informative: its distinguishing class identifies
  The budget is actionable: prompt interpretation,                the semantic behavior changed by the replacement.
retrieval, generation, validation, and repair can be
audited separately. A large downstream drift must
be explained by an upstream prompt distance or by                 A Checkable Certificate Object
one or more measured compatibility defects.
                                                                  The previous results can be packaged as a finite ob-
                                                                  ject that accompanies a proposed prompt, model,
Estimating Compatibility from                                     tool, or agent replacement. For a pipeline with in-
                                                                  terfaces 0, . . . , n, define a certificate
Samples
                                                                          C = (R0 , . . . , Rn ; ϵ0 ; η1+ , . . . , ηn+ ; δ; G),
For a black-box model, K(x) is estimated by re-
peated calls under a frozen model version, con-                   where Ri declares the observer at interface i, ϵ0
text, decoding policy, and tool environment. Let the              bounds the initial quotient distance, ηi+ is a proved
output quotient have m classes and let K   b N (x) be             or high-confidence upper bound on layer i’s compati-
the empirical class distribution from N independent               bility defect, δ is the joint statistical failure probabil-
samples.                                                          ity, and G records the justification for each commit


                                                              5
guard. A guard entry may be sound, may provide              Compatibility is necessary. Let xRX x′ and
a false-accept upper bound β, or may be explicitly          let a, b be distinct RY -classes. If K(x) = δa and
unsupported. The certificate is independently check-        K(x′ ) = δb , then K([x]) would have to be both
able from class definitions, samples or proofs, and         δ[a] and δ[b] . No quotient kernel exists. In a code
trace data; it need not reveal prompts or generated         agent, this is exactly a semantics-preserving para-
source if privacy-preserving class evidence is suffi-       phrase that systematically changes the generated be-
cient.                                                      havior class; composition cannot repair the missing
                                                            local congruence.
Theorem 9 (Certificate soundness). Suppose every
numerical assertion in C holds simultaneously with
probability at least 1 − δ. Let A be any final event        Events must be quotient-closed. Suppose
closed under Rn . For the original and replacement          aRY b and two pipelines output δa and δb . They are
workflows,                                                  equivalent at the declared interface, yet the concrete
                                       Pn                   event {a} has probabilities one and zero. Corollary 1
    Pr(A) − Pr′ (A) ≤ τ := min{1, ϵ0 + i=1 ηi+ }            therefore cannot promise equality for observations
   W        W
                                                            that the equivalence intentionally erased. This is
with probability at least 1 − δ. If a commit guard is       why source-string equality, exact diagnostic word-
sound, its unsafe-commit probability is zero. If in-        ing, or a particular proof term cannot be queried
stead its false-accept event has probability at most        from a certificate that preserves only functional be-
β, unsafe commit has probability at most β.                 havior.
Proof. The event bound follows from Theorem 7, be-
cause total variation upper-bounds the probability          Extensionality and soundness differ. A
difference of every measurable quotient event. The          checker that accepts every program is perfectly
confidence statement is inherited from the simulta-         extensional under any program equivalence, but it
neous bounds. The guard clauses follow from Theo-           is not sound. Conversely, a sound checker could ex-
rem 4, or by inclusion of unsafe commit in the false-       pose irrelevant syntactic diagnostics and thereby fail
accept event.                                               extensionality. The first breaks safe commitment;
                                                            the second breaks replacement while preserving
   The theorem clarifies three different outcomes.
                                                            correctness. Proposition 1 requires both properties
A robust and safe certificate has small τ and a
                                                            only when both conclusions are desired.
sound guard. A robust but uncertified replacement
has small τ but no checker-soundness argument: it
behaves like the baseline but may reproduce its er-         Hidden state must enter the configuration.
rors. A correct but non-robust system may commit            If a model service changes behavior after previous
only verified programs while paraphrases yield very         calls, a purported map from prompt to output dis-
different rejection, repair, latency, or cost traces.       tribution is not a kernel on prompts alone. Adding
These dimensions should be reported separately.             model version, decoding state, retrieved context,
   Certificate composition is modular. Two adjacent         tool state, and relevant trace history to Γ restores
certificates can be concatenated when they use the          the Markov property. Omitting them can create spu-
same intermediate equivalence; their defect bounds          rious compatibility: two prompts agree in one call
add and their statistical failure probabilities com-        order but diverge after different histories.
bine by a union bound. Observer refinement is also
checkable: Proposition 3 permits projection from a          The quantitative constants are tight. Non-
stronger certificate to a weaker observation bound-         expansiveness is tight for an identity quotient kernel,
ary, but never the reverse. Consequently, a reposi-         and a layer defect can contribute its full value when
tory can maintain certificates at different assurance       representatives attain def(K). The additive budget
levels—for example, functional, frame-safe, resource-       is therefore a worst-case guarantee; tighter bounds
aware, and information-flow-aware—without treat-            require additional structure.
ing them as interchangeable.
                                                            Executable Semantic Audit
Sharpness and Failure Modes
                                                            We instantiate the definitions on insertion sort. The
The hypotheses above are not merely sufficient proof        purpose is to exercise every semantic object exactly,
conveniences. Small finite counterexamples show             not to estimate a production model’s quality. The
why an audit must expose each of them.


                                                        6
  Comparison Contract TV      Code TV       Verdict TV         Implementation Weak class Strong class Copy commit
  pA vs. pB         0       < 1.5 · 10−16   < 6 · 10−17        Built-in copy          E1          F1         yes
  pA vs. pF         0        < 8 · 10−17    < 3 · 10−17        Insertion copy         E1          F1         yes
  pA vs. pnear    .0500        .0275          .0050            In-place sort          E1          F2         no
                                                               Descending             E2          F3         no
                                                               Deduplicate            E3          F4         no
Table 2: Quotient total-variation distances. Tiny              Off-by-one             E4          F5         no
nonzero values are floating-point roundoff.
                                                              Table 3: Exhaustive equivalence classes for six con-
                                                              crete programs.
audit implementation uses only the Python standard
library and emits all reported numbers.
                                                              yields mutation-class mass 0.70 and is not declared
Observers and programs. Six concrete func-                    equivalent.
tions implement: built-in sorted copy, insertion-
sort copy, built-in in-place sort, descending sort,           Randomized law checks. We additionally sam-
duplicate-removing sort, and an off-by-one insertion          ple 10,000 pairs of distributions and random finite
sort. We execute each on all 121 arrays of length 0–4         kernels of dimensions two through eight. No trial
over {−1, 0, 1}. A weak observer records return val-          violates total-variation contraction; the largest ob-
ues; a strong observer also records the post-state of         served output/input ratio is 0.9471 (mean 0.3435).
the input. Under the weak observer, the two pure im-          A second 10,000-trial test checks TV(µK, νL) ≤
plementations and the in-place implementation are             TV(µ, ν) + supx TV(Kx , Lx ); again there are no vi-
equivalent. Under the strong observer, the in-place           olations. These tests do not replace proofs. They
implementation is separated, while the two pure im-           validate the implementation, numerical conventions,
plementations remain equivalent. This provides a              and artifact tables, and make the reported case
concrete distinguishing context rather than an as-            study independently reproducible.
serted semantic difference.

Prompts and kernels. The prompt texts are:                    Observer Design and Refine-
pA , “return a sorted copy and leave the input un-
changed”; pB , “produce a nondecreasing permuta-
                                                              ment
tion without mutating the argument”; and pF , a for-          A robustness claim is meaningful only relative to
mal pre/postcondition specifying nondecreasing or-            an observation boundary. Let an observer be a map
der, multiset equality, and frame preservation. They          h : C → B from concrete executions to observable
induce different distributions over two syntactically         records. It induces cRh c′ exactly when h(c) = h(c′ ).
distinct but equivalent copy-sort contracts. Their            Return values, mutated state, exceptions, proof cer-
quotient contract distribution is the point mass on           tificates, resource use, information-flow events, and
copy-sort. The two contract-specific generation rows          tool calls can be included independently. This makes
differ at artifact level but assign the same masses           the abstraction explicit and reviewable rather than
to five program-property classes: pure-correct 0.60,          hidden inside a benchmark metric.
mutating-correct 0.15, descending 0.10, lossy 0.10,
and partial-sort 0.05. A sound copy-sort checker              Definition 3 (Observer refinement). Observer h2 :
commits only pure-correct programs.                           C → B2 refines h1 : C → B1 when there exists a
   Table 3 makes the role of the observer explicit.           map r : B2 → B1 such that h1 = r ◦ h2 . Thus h2
The checker is stricter than the weak return-value            retains at least the information exposed by h1 .
observer because the copy contract contains a frame
condition.                                                    Proposition 3 (Monotonicity under observer re-
   The three equivalent prompts all yield commit              finement). If h2 refines h1 , then Rh2 ⊆ Rh1 . Conse-
probability 0.60 and identical rejection-class distri-        quently, exact equivalence under h2 implies equiva-
butions, as predicted by Corollary 1. A near prompt           lence under h1 , but not conversely. For distributions,
places 0.05 mass on an in-place contract. The strong
                                                                                dRh1 (µ, ν) ≤ dRh2 (µ, ν).
observer detects the new mutation behavior. Never-
theless, code-class distance is 0.0275 and verdict dis-       Proof. If h2 (c) = h2 (c′ ), applying r gives h1 (c) =
tance is 0.0050, both below the input distance 0.05           h1 (c′ ). The quotient for h1 is therefore a further
as required by Theorem 6. A fully in-place prompt


                                                          7
coarsening of the quotient for h2 , and total varia-               Stage      Construction    Reported quantity
tion cannot increase under the induced deterministic               Tasks      HumanEval,      Task, language,
map.                                                                          MBPP,           contract, observer
                                                                              formal tasks
   This proposition gives a simple discipline for                  Prompts    Paraphrases,    Contract-class
safety-critical audits: begin with the deployment ob-                         formaliza-      input distance
                                                                              tions, frame
servations and refine them until every property that                          variants
can invalidate substitution is represented. A unit-                Samples    N frozen        Empirical
test observer may equate two programs that agree on                           calls per       code-class
sampled inputs; adding exhaustive bounded execu-                              prompt and      distributions
                                                                              model
tions, frame conditions, exceptions, or a sound veri-              Checking   EvalPlus        Verdict classes and
fier can split that class. A certificate produced under                       tests and       commit events
a coarse observer remains valid only for the coarse                           sound tools
                                                                              where
question. The insertion-sort audit below demon-
                                                                              available
strates the issue: return-only observation equates                 Analysis   Pairwise and    Defects,
copying and mutating sorts, while the post-state ob-                          joint bounds    distinguishing
server separates them.                                                                        classes, budget
                                                                   Repair     Fixed           Conditional success
                                                                              diagnostic      by failure history
                                                                              templates
Nondeterminism                   and        Agent                             and retry cap
Control
                                                              Table 4: Protocol for testing a model-mediated
Real agents contain both probabilistic model calls            GenOS pipeline.
and nondeterministic choices: a scheduler selects an
agent, an orchestrator selects a tool, or a human
chooses whether to retry. A fixed orchestration pol-          is an invariant of every transition, not a one-pass ap-
icy resolves these choices and induces the kernels            proximation.
used above. With unresolved choices, the semantics
is a probabilistic automaton or Markov decision pro-
cess rather than a Markov chain Segala and Lynch
                                                              Protocol for               a    Model-Based
[1995], Baier and Katoen [2008].                              Evaluation
   There are two useful certificate strengths. A
policy-specific certificate proves compatibility for          The finite audit establishes that the definitions, the-
the deployed scheduler and tool-selection policy. A           orems, and implementation agree. A full model eval-
policy-robust certificate requires every enabled ac-          uation should test whether contemporary code mod-
tion to be matchable by an action with equivalent             els satisfy the local obligations. Table 4 defines an
successor-class mass; this is the standard alternat-          executable protocol that avoids conflating textual
ing form of probabilistic bisimulation. The latter            paraphrase invariance, functional correctness, and
implies replacement under every scheduler that re-            safe commitment.
spects the action interface. Event probabilities can
then be bounded by taking the supremum or infi-               Prompt families. Each task should contain:
mum over schedulers. This distinction matters for             (i) meaning-preserving lexical and syntactic para-
agentic code generation: a compatible generator does          phrases; (ii) natural-language and formal or semi-
not compensate for an orchestrator that routes se-            formal versions of the same contract; and (iii) delib-
mantically equivalent diagnostics to different repair         erately non-equivalent near misses, such as changing
tools.                                                        an in-place requirement, exception policy, numeri-
   For bounded repair horizons, Theorem 7 gives a             cal precondition, or complexity constraint. The third
conservative drift bound. If the initial prompt dis-          group is essential: a metric that declares both para-
tance is ϵ, and each of at most T generation, valida-         phrases and near misses equivalent has selected an
tion, or repair actions has defect at most ηPt , every        inadequate observer.
                                                T
quotient-trace event differs by at most ϵ + t=1 ηt .
Under exact action compatibility, Theorem 3 re-               Artifact classification. Programs are first com-
moves the dependence on T entirely: loops and in-             piled and executed in a sandbox. Functional obser-
terleavings preserve equivalence because the relation         vations can combine reference tests with augmented


                                                          8
suites such as EvalPlus Liu et al. [2023]; frame, ex-          Conclusion
ception, and resource observations are recorded sep-
arately. When a formal specification and a sound               GenOS treats an AI coding workflow as a proba-
tool are available, proof acceptance forms a distinct,         bilistic program with auditable semantic interfaces.
stronger commit guard rather than being merged                 Compatible kernels commute with quotienting and
with test success. Syntactically different outputs are         composition; approximate defects form an explicit
aggregated only after their observable behavior has            robustness budget; sound guards establish commit
been classified.                                               safety. The framework does not assume model in-
                                                               variance. It turns invariance into a local, testable
Statistics and diagnosis. Each pair is reported                obligation and composes the resulting evidence end
with quotient total variation, a simultaneous bound            to end.
from Theorem 8, and its distinguishing classes. Mea-
suring these quantities at every interface localizes           References
drift to interpretation, generation, validation, repair,
or orchestration. Repair results are stratified by fail-       Jacob Austin, Augustus Odena, Maxwell Nye,
ure history, because an unconditional average does               Maarten Bosma, Henryk Michalewski, David Do-
not establish Theorem 5’s premise.                               han, Ellen Jiang, Carrie Cai, Michael Terry,
                                                                 Quoc V. Le, and Charles Sutton. Program syn-
Decision rule. A replacement is certified for event              thesis with large language models. arXiv preprint
family A only when the composed bound meets its                  arXiv:2108.07732, 2021.
tolerance and every event is quotient-closed. Safe
                                                               Christel Baier and Joost-Pieter Katoen. Principles
commitment separately requires checker soundness;
                                                                of Model Checking. MIT Press, 2008.
robustness and correctness are distinct claims.
                                                               Luca Beurer-Kellner, Marc Fischer, and Martin
                                                                 Vechev. Prompting is programming: A query lan-
Implications and Limitations                                     guage for large language models. In Proceedings
                                                                 of the 44th ACM SIGPLAN Conference on Pro-
A deployable certificate records the observers, model
                                                                 gramming Language Design and Implementation,
and tool identities, sample counts, confidence level,
                                                                 pages 1946–1965, 2023.
per-layer defects, composed bound, and commit-
guard evidence. It can cover functional behav-                 Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
ior, mutation, exceptions, cost, or security, but               Yuan, Henrique Ponde de Oliveira Pinto, Jared
only observations represented by its equivalences.              Kaplan, Harri Edwards, Yuri Burda, Nicholas
The PLTS result supports local replacement in-                  Joseph, Greg Brockman, Alex Ray, Raul Puri,
side generate–verify–repair loops and communicat-               Gretchen Krueger, Michael Petrov, Heidy Khlaaf,
ing agents; guarded safety remains an orthogonal                Girish Sastry, Pamela Mishkin, Brooke Chan,
obligation.                                                     Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea
   The guarantees are conditional on well-chosen ob-            Power, Lukasz Kaiser, Mohammad Bavarian,
servers and proved or measured compatibility. Exact             Clemens Winter, Philippe Tillet, Felipe Petroski
model kernels are unobservable, so empirical audits             Such, Dave Cummings, Matthias Plappert, Fotios
depend on frozen environments, confidence proce-                Chantzis, Elizabeth Barnes, Ariel Herbert-Voss,
dures, and adequate sampling. Nontermination and                William Hebgen Guss, Alex Nichol, Alex Paino,
continuous artifact spaces require measurable quo-              Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir
tients or subdistributions beyond the finite presenta-          Balaji, Shantanu Jain, William Saunders, Christo-
tion developed here. Finally, the controlled audit val-         pher Hesse, Andrew N. Carr, Jan Leike, Josh
idates the semantics rather than benchmarking an                Achiam, Vedant Misra, Evan Morikawa, Alec Rad-
LLM. A model study should execute the stated pro-               ford, Matthew Knight, Miles Brundage, Mira Mu-
tocol with paraphrase families, formalizations, re-             rati, Katie Mayer, Peter Welinder, Bob McGrew,
peated generations, and strong behavioral or proof-             Dario Amodei, Sam McCandlish, Ilya Sutskever,
based observers; FormalBench and EvalPlus are nat-              and Wojciech Zaremba. Evaluating large lan-
ural starting points Le-Cong et al. [2025], Liu et al.          guage models trained on code. arXiv preprint
[2023].                                                         arXiv:2107.03374, 2021.
                                                               Matthias Cosler, Christopher Hahn, Daniel Men-
                                                                doza, Frederik Schmitt, and Caroline Trippel.

                                                           9
  nl2spec: Interactively translating unstructured              Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu,
  natural language to temporal logics with large lan-           Shengchao Qin, Mengda He, Haokun Li, Shing-
  guage models. In Proceedings of the 23rd Confer-              Chi Cheung, and Cong Tian. Enchanting program
  ence on Formal Methods in Computer-Aided De-                  specification synthesis by large language mod-
  sign, pages 68–79, 2023.                                      els using static analysis and program verification.
                                                                arXiv preprint arXiv:2404.00762, 2024.
Aaron Councilman, David Jiahao Fu, Aryan Gupta,
 Chengxiao Wang, David Grove, Yu-Xiong Wang,
 and Vikram Adve.        Towards formal verifi-
 cation of large-language-model-generated code
 from natural language prompts. arXiv preprint
 arXiv:2507.13290, 2025.
Naman Jain, Skanda Vaidyanath, Arun Shankar
 Iyer, Nagarajan Natarajan, Suresh Parthasarathy,
 and Sriram Rajamani. Jigsaw: Large language
 models meet program synthesis. In Proceedings
 of the 44th International Conference on Software
 Engineering, pages 1219–1231, 2022.
Kim G. Larsen and Arne Skou. Bisimulation through
  probabilistic testing. Information and Computa-
  tion, 94(1):1–28, 1991.
Thanh Le-Cong, Bach Le, and Toby Murray.
 Can large language models reason about pro-
 gram semantics? a comprehensive evaluation on
 formal specification inference. arXiv preprint
 arXiv:2503.04779, 2025.
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and
  Lingming Zhang. Is your code generated by chat-
  gpt really correct? rigorous evaluation of large lan-
  guage models for code generation. Advances in
  Neural Information Processing Systems, 36, 2023.
Robin Milner. Communicating and Mobile Systems:
  The Pi-Calculus. Cambridge University Press,
  1999.
Gordon D. Plotkin. A structural approach to oper-
 ational semantics. Journal of Logic and Algebraic
 Programming, 60–61:17–139, 2004.
Corrado Priami. Stochastic pi-calculus. The Com-
  puter Journal, 38(7):578–589, 1995.
Roberto Segala and Nancy Lynch. Probabilistic sim-
  ulations for probabilistic processes. Nordic Jour-
  nal of Computing, 2(2):250–273, 1995.
Merlijn Sevenhuijsen, Khashayar Etemadi, and Mat-
 tias Nyberg. Vecogen: Automating generation of
 formally verified c code with large language mod-
 els. arXiv preprint arXiv:2411.19275, 2024.
Chuyue Sun, Ying Sheng, Oded Padon, and Clark
  Barrett. Clover: Closed-loop verifiable code gen-
  eration. arXiv preprint arXiv:2310.17807, 2024.


                                                          10
