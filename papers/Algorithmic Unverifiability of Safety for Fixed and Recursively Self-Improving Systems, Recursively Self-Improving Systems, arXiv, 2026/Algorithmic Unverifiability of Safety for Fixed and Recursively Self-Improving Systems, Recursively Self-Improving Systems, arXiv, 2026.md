                                               Algorithmic Unverifiability of Safety for Fixed and
                                                      Recursively Self-Improving Systems
                                                                              Jose Pascual Gumbau Mezquita∗
                                                                        Universitat Jaume I, Castelló de la Plana, Spain
                                                                                        gumbau@uji.es
arXiv:2606.28639v3 [cs.LO] 23 Sep 2026




                                                                                             Abstract
                                                We establish mathematical limits of algorithmic safety verification for Turing-complete self-
                                                modifying systems, the class in which recursive self-improvement takes place, both for a
                                                fixed system and across its own modification. Statically, no verifier is sound, complete
                                                and tractable: over unbounded domains by Rice’s and Gödel’s theorems, over all finite
                                                configurations by Trakhtenbrot’s theorem, and over succinctly described finite environments
                                                because verifying a policy against an adversary is coNP-complete and synthesising one is
                                                PSPACE-complete. Dynamically, we model one step of self-modification as a computable
                                                transformation of code and ask whether a safety property survives it. If the transformation
                                                depends only on behaviour, this is Rice’s theorem one level up; if it reads the code, as self-
                                                modification does, the question is no longer semantic, yet the same s-m-n reduction works
                                                inside a class of behaviourally identical programs and inherits the halting degree. One
                                                step is never harder than the property; persistence along the whole trajectory can be Π02 -
                                                complete. Certification by a total algorithm is possible only for transformations of restricted
                                                expressivity, not merely for systems that stop changing. No tower of supervisors helps,
                                                and every total supervisor errs on an undecidable set of systems. For effectively pointwise
                                                properties, every faithful bounded scheme that certifies on finite behavioural evidence admits
                                                evolution traces certified at every stage while the property is violated. What survives is
                                                exact: a monitor that raises an alarm on violation semidecides it, and comparison against a
                                                frozen reference keeps the full theory.

                                         Keywords: self-modifying systems, recursive self-improvement, safety properties, preservation
                                         and persistence of properties, AI alignment, artificial general intelligence (AGI), computabil-
                                         ity theory, Rice’s Theorem, Rice–Shapiro Theorem, s-m-n Theorem, Trakhtenbrot’s Theorem,
                                         Gödel’s Incompleteness, descriptive complexity, PSPACE-completeness, runtime monitoring, ver-
                                         ifier regress, formal verification.


                                         1     Introduction
                                         1.1    The question
                                         A self-modifying computational system inspects, rewrites, and redeploys its own code. Recursive
                                         self-improvement (the term goes back to Good, 1965) is the paradigm: one step of it is what
                                         we call a transformation Φ, a run of it is an evolution trace, and “recursive self-improvement
                                         preserves alignment” is what we call preservation (one step) or persistence (the whole run). The
                                         systems that make the question urgent — autonomous agents, retraining loops, self-improving
                                         coding agents, and whatever is meant by artificial general intelligence — are instances. In
                                            ∗
                                              The structuring, mathematical correctness review, formal-language drafting, and orthotypographic review of
                                         this document were conducted with the assistance of artificial intelligence models (Gemini, Google, 2026; Claude,
                                         Anthropic, 2026). The definitions, results, and all content decisions are the author’s, who takes full responsibility
                                         for them. Anna.


                                                                                                  1
the AI-safety literature the problem of keeping such a system within specified constraints is
called alignment; we use the word for the applied problem, and safety property for the formal
object it refers to: a set P of behaviours, with the system aligned when its behaviour lies in P
(Definition 3). The two are the same thing under two names.
    Two questions lie beneath the problem, and this article answers both in one framework.
The static question: given a fixed system and a fixed safety property, can an algorithm decide,
infallibly, completely, and tractably, whether the system satisfies it? The dynamic question, the
one that matters for systems that change: given that the property has been verified to hold now,
can an algorithm decide, before the fact, whether it will still hold after the system modifies itself
— once (preservation) or forever (persistence)?
    We prove nothing about “AGI”, a term without agreed definition. We prove things about
a precise class: Turing-complete systems that admit a computable transformation of their own
code (MSM, Definition 1). Every system of the kinds above is a member by construction, and
inherits the limits (the scope remark of Section 2.1); whoever wishes to deny the inheritance
must deny either Turing-completeness or self-modification.

1.2   Thesis
The impossibility established here is not an engineering hurdle awaiting better hardware, faster
algorithms, or larger test suites. It is one structural obstruction that reappears, unchanged,
each time one tries to go around it. Verifying a fixed system once is blocked by Rice, Gödel, and
Trakhtenbrot (Part I). Letting the system evolve, so as to certify each version rather than the
fixed whole, reproduces the obstruction one level up, at the property “safe now and safe after
the next step” — and it does so whether the modification reads only the system’s behaviour,
where the obstruction is Rice’s Theorem applied one level up, or its code, where Rice’s Theorem
no longer applies and the very same reduction that proves it has to be carried out by hand
inside a single class of behaviourally identical programs (Part II). Delegating verification to a
more capable supervisor reproduces it at every level of the resulting tower. Weakening exact
certification to a bounded practical scheme reproduces it once more, as an evolution trace the
scheme certifies at every stage while the property is violated (Part III). Behind all four is one
fact: the expressivity a system needs in order to be genuinely general — Turing-completeness
and open-ended self-modification — is exactly the expressivity that places it, and any adequate
verifier of it, beyond algorithmic certification. We call this the Expressivity Invariant: every
transformation introduced to remove the obstruction preserves it. Its demonstrated form is the
Expressivity Principle of the companion mathematical paper (Gumbau Mezquita, 2026b), to
which we refer for the results of Part II that are applied here rather than re-proved.

1.3   What is established
Static face (Part I). Over unbounded domains, no verifier is both sound and complete (Rice), and
no effective framework containing arithmetic is complete for the safety statements it can express
(Gödel); over the class of all finite hardware configurations, universal verification is co-RE-
complete (Trakhtenbrot), and even over finite environments, verifying a given policy against an
adversary is coNP-complete and synthesising a safe one PSPACE-complete on an explicit family
of succinct arenas (reductions from Taut and TQBF, Theorem 5). This forces a Soundness–
Completeness–Tractability Trilemma as a structural, not statistical, necessity (Corollary 3).
The source of the cost is the succinctness of the arena; the adversary determines the class (coNP
for verifying a given policy, PSPACE for synthesising one; without an adversary, verifying a
given policy is polynomial and synthesis NP-complete), and on an explicit arena every variant
is polynomial.
    Dynamic face (Part II). We formalise one step of self-modification as a total computable
transformation Φ on indices, and preservation as the elevated property ΛΦ (P ) = {x ∈ P :


                                                 2
Φ(x) ∈ P }. If Φ is extensional and disruptive, ΛΦ (P ) is semantic and non-trivial and Rice’s
Theorem decides the matter (Theorem 6). If Φ is intensional and uniformly disruptive — there
is a family of programs with identical behaviour on which whether the rewritten program is safe
encodes the halting problem — ΛΦ (P ) is not semantic and yet inherits the halting degree, by the
same s-m-n reduction that proves Rice, relocated inside a single behavioural class (Theorem 7).
One step never makes the question harder than the property; persistence along an unbounded
trajectory can be one level higher — Π02 -complete for a Σ01 property under some operators,
even extensional ones — while for a Π01 property it stays Π01 (Corollary 5). Certification of
preservation is therefore available only to operators of restricted expressivity (Corollary 4):
stasis is one instance, shielding and sanitising are others; it is the restriction, not the stasis, that
buys certifiability. (Typed or primitive-recursive rewriting is not such a restriction: the anchor
to the halting set is constructible with primitive-recursive rewriters, and strong normalisation
concerns reduction steps that preserve the computed function — semantic stasis, the trivial case.)
And because one step acts at compile time, the question “will the next version be safe?” is a
static question about the compiled program: what is genuinely dynamic is only the unbounded
trajectory.
    Supervision (Section 10). No tower of supervisors, of whatever architecture, decides an
undecidable set (Theorem 8); every total supervisor decides a decidable set and therefore errs on
a set of systems that is itself undecidable, so that it cannot locate its own errors (Proposition 1);
and a supervisor that is itself a self-modifying system with a disruptive transition inherits the
same undecidability for its own preservation (Proposition 2).
    Practical schemes (Part III). Finite test coverage, bounded deliberation time, and restricted
observational vocabulary are three failure modes. Two structural facts underlie them: a total
verifier decides a decidable set, so it errs on an undecidable set of systems (Proposition 1); and for
a property not determined by any finite set of inputs, every faithful bounded scheme admits an
evolution trace it certifies at every stage while the property is persistently violated (Theorem 9).
For safety properties in the companion paper’s sense, no uniform procedure certifies preservation
across all safe systems; what can be established uniformly is violation, after the fact.
    What can be had (Part IV). Two things, both exact. For a safety property, the monitor
that runs the system and raises an alarm on the first observed violation semidecides violation,
and no computable procedure semidecides preservation for all safe systems. And comparing an
evolving system against a frozen reference has the full theory unconditionally, where comparing
two evolving systems has it only under a design condition. Containment strategies — shielding,
proof-carrying code, bounded horizon, boxing, hierarchical supervision — do not resolve the
tension; they choose where along it to stand, and we say what each one pays.

1.4    What is not claimed
We do not claim that self-modifying systems are unsafe; we claim that no algorithm can certify
that they will remain safe. We do not claim that every conceivable governance mechanism has
the form the companion paper isolates; we use its results for the mechanisms that do, and note
which do not. We do not claim that classical results — program equivalence, incompleteness
— follow from the framework; their undecidability is imported, not derived. And we do not
claim that the resource face discovers new complexity: it shows that robust specifications over
succinct finite arenas fall under known obstructions (succinct games), and says which class each
variant lands in.

1.5    Relation to recent work
The term ‘unverifiability’ as a named limitation of advanced AI is due to Yampolskiy (2017),
who introduced it informally; we give it the precise content of Definition 2. Brčić and Yam-
polskiy (2023) note that impossibility results of this kind share a diagonal pattern at the level


                                                   3
of proof technique; the Expressivity Invariant sharpens this into a single generative operation,
developed formally in the companion paper. Three recent results deserve precise placement,
because ours are consistent with them and locate them. Melo et al. (2025) show that inner
alignment is undecidable by Rice’s Theorem and that restricting to machines guaranteed to
halt over a finite domain restores decidability. This is correct at the level it claims — a fixed,
finite, halting system is verifiable by exhaustive search (Corollary 2) — and it is exactly an
instance of the corrected dichotomy of Corollary 4: restricting the system’s expressivity buys
certifiability. What we add is that the guarantee does not extend to the universal level (all finite
configurations: co-RE-complete, Trakhtenbrot) nor to the dynamic level (preservation across self-
modification, Part II). Agarwal (2026) establishes a soundness–generality–tractability trilemma
for static alignment verification in the statistical, sample-based setting, characterising achievable
guarantees over open domains; our Trilemma (Corollary 3) is structural rather than statistical,
obtains without any sampling assumption from explicit reductions, and, together with Part II,
shows that Agarwal’s frontier of achievable guarantees contracts further when the verified system
is not fixed but evolves. Hernández-Espinosa et al. (2026) prove the impossibility of complete
orchestrated controllability of agentic systems; their result is complementary to ours on the
static side. All three operate on static verification — deciding whether a fixed system satis-
fies a property over an input domain. Our central contribution is the dynamic and intensional
case: the (un)decidability of preserving a property when the system rewrites itself, formalised
by the elevation operator and the family it generates in the companion paper. The static bar-
rier we share with this literature and record for completeness; the dynamic barrier is what this
programme adds.
    Within the literature on recursive self-improvement, the closest formal precedent is the tiling-
agents programme (Yudkowsky & Herreshoff, 2013), which models an agent that approves the
construction of a successor and meets a proof-theoretic obstacle: an agent reasoning in a theory
T cannot prove the soundness schema of T , and so cannot license a successor that reasons in
T (the Löbian obstacle). Our results are the computability-theoretic counterpart at the level of
the family: no uniform procedure certifies preservation, whether or not the agent reasons about
itself, and without appeal to Löb’s theorem. On the applied side, the Darwin Gödel Machine
(Zhang et al., 2025) replaces the requirement of the Gödel Machine (Schmidhuber, 2003) that
each rewrite be proved beneficial with empirical validation on coding benchmarks, in agents
that rewrite their own code in a Turing-complete language. It is a member of MSM without
qualification, each accepted rewrite is certified on a finite test set, and Part III applies to it
directly (Remark after Proposition 3).
    On the applied side of recursive self-improvement, Chen, Wang & Qu (2026) survey recent
work and separate bounded self-refinement, which is convergent and evaluable, from open-ended
recursive self-improvement, ordering evaluation signals into a hierarchy from formal verifiers to
intrinsic self-assessment. Our results bound the top of that hierarchy: a formal verifier certifies
membership in a restricted subclass, never preservation in general (Gumbau Mezquita, 2026b,
Proposition 8.1), and no signal computed on finite behavioural evidence certifies preservation of
an effectively pointwise property (Theorem 9). Zenil (2026) proves a complementary, statistical
limit: recursive self-training degenerates when the share of exogenous, grounded signal vanishes.
His limit concerns whether the loop improves; ours, whether its safety can be certified, and it
holds whether or not the loop improves. Both point to the same remedy by different routes: an
external anchor, which in our terms is comparison against a frozen reference (Section 15).

1.6   Structure
Section 2 fixes the framework: the class MSM, the two obstructions that make up unverifiabil-
ity, and the expressivity threshold. Part I (Sections 3–7) proves the static limits: Rice, Gödel,
Trakhtenbrot, the exhaustiveness of the two verification vectors, and the Finite Structural Un-
verifiability Theorem with its Trilemma. Part II (Sections 8–10) proves the dynamic limits:

                                                 4
the transition-operator framework, preservation in both regimes, the one-step bound and the
persistence jump, and the supervisory regress. Part III (Sections 11–14) treats the practical
schemes: statistical certification, the uncertified window, bounded observation, and universal
evadability. Part IV (Sections 15–18) maps containment strategies, draws the consequences for
deployed systems, lists open directions, and concludes. Appendix A collects the classical proofs
used in Part I.


2     Preliminaries: A Common Formal Framework
We work throughout with Turing machines (Turing, 1936) Mx indexed by Gödel numbers x ∈ N,
and write φx for the partial computable function computed by Mx ; for the standard theory we
follow Rogers (1967) and Soare (1987). The s-m-n theorem (Kleene, 1952) — indices can be
built uniformly from a template and parameters — is the engine of every reduction in Part II.

2.1   The formal layer: Turing-complete self-modifying systems - MSM
To avoid depending on any speculative notion, we anchor every result in a precise mathematical
class.

Definition 1 (MSM). A system belongs to the class MSM of Turing-complete self-modifying
systems if (a) its computation is Turing-complete — its transition logic can isolate and iter-
ate over discrete symbolic structures — and (b) it admits self-modification: a total computable
transformation Φ of its own code (index). The class is purely mathematical; it does not depend
on any notion of intelligence, agency, or autonomy.

Remark (Scope: inheritance). The results below are stated for MSM and apply to any sys-
tem that is in fact Turing-complete and admits a computable self-modification — which is how
autonomous agents, retraining loops, and anything called AGI are specified. This is a scope state-
ment, not a theorem, and two cases must be kept apart. Agents that rewrite their own code in
a general-purpose language are members of MSM without qualification, and every result applies.
Self-improvement that updates the parameters of a network of fixed architecture, bounded preci-
sion and bounded context is a finite-state system: the decidability face reaches it only through
the idealised family, while the resource face (Section 7) applies to it directly. The distinction
matches the empirical one drawn by Chen, Wang & Qu (2026) between bounded self-refinement
and open-ended recursive self-improvement. The results do not depend on how “intelligence” is
defined; they depend only on the two conditions of Definition 1.

    This two-layer separation reverses the burden of proof: we prove nothing about “AGI”, a
term without consensus definition, but about a precise class; whoever wishes to deny that a
given system inherits the limits must deny either that it is Turing-complete or that it modifies
itself.

Which expressivity triggers which limit. The limits sort themselves by the capacity in-
voked. Turing-completeness alone suffices for the undecidability results (Rice, the s-m-n reduc-
tion of Part II) and for the complexity results (PSPACE); no normative framework is needed. The
Gödelian results — where the system must certify its own properties within a formal framework
— additionally require that framework to interpret arithmetic (Robinson’s Q suffices). Most of
what follows depends on the first condition only; we keep the two explicit so as not to conflate
the frameworks.




                                                5
2.2   Algorithmic unverifiability
Definition 2 (Algorithmic unverifiability). A system Φ ∈ M SM is algorithmically unverifiable
with respect to a safety property P if no verifier V that is simultaneously sound, complete, and
effective determines whether P persists along the system’s evolution.

   This unattainability decomposes into two independent obstructions:

  1. The logical (decidability) obstruction: Even without resource limits, no sound and
     complete computable verifier exists.

        • Statically: Semantic undecidability (Rice, Section 3) and co-RE-completeness (Sec-
          tion 5, Trakhtenbrot).
        • Dynamically: Undecidability of preservation in both regimes and, for some Φ and
          Σ01 properties, Π02 -completeness of persistence (Part II, following Gumbau Mezquita,
          2026b).

  2. The resource (tractability) obstruction: Even where verification is decidable, no
     verifier exists within bounded (polynomial) resources.

        • Specifics: coNP-hardness of robust verification and PSPACE-hardness of synthesis
          over succinctly described finite environments (Section 7).
        • Scope: This face concerns robust specifications over arenas (Definition 4), not the
          operator Φ of Part II.

Notes on Terminology and Asymmetry:

   • The Umbrella Term: No classical term suffices alone. ‘Undecidable’ covers only the
     first obstruction; the second is intractability, not undecidability. ‘Unverifiable’ acts as the
     umbrella term for both.

   • The Asymmetry: The decidability face is unconditional, whereas the resource face is
     conditional on P ̸= P SP ACE.

   • Conclusion: We state this openly: unverifiable = not decidable (unconditionally), or,
     under P ̸= P SP ACE, not tractable.

2.3   Safety property (alignment property)
Definition 3 (Safety property (alignment property)). A safety property — in the applied vo-
cabulary, an alignment property; the two terms are used interchangeably — is a set P of partial
computable functions. P is non-trivial if it is neither empty nor the set of all partial computable
functions — equivalently, there exist a function f ∈ P (a ‘safe’ behaviour) and a function g ∈ /P
(an ‘unsafe’ behaviour). The corresponding index set is IP = {x ∈ N | φx ∈ P }. A universal
verifier for P is an algorithm that decides, given an arbitrary index x, whether φx ∈ P .

Convention (pointwise-to-global correctness). Where, from Section 11 onward, P is decom-
posed into pointwise conditions Pw indexed by inputs w ∈ N, we adopt throughout the standing
convention that φx ∈ P if and only if behaviour(Mx , w) satisfies Pw for every w ∈ N. Under
this convention, a single violation at any input w suffices for φx ∈
                                                                   / P ; this is what allows Propo-
sitions 3, 5, and Theorem 9 to infer φx ∈  / P from a violation at one point outside an observed
or tested region, without further argument at each occurrence.




                                                 6
2.4   Decidable versus General Systems: the Difficulty Asymmetry
The expressivity threshold of Definition 1 separates two regimes, and this separation, together
with the paradox it generates, motivates the entire article. (In the AI-safety literature the two
regimes are called Narrow AI and AGI; we use the formal names.)
    Decidable systems: a system Mdec operates over continuous or decidable logical struc-
tures. Systems based on Real Closed Fields (RCF), for instance, are complete and decidable
(Tarski, 1951) precisely because their logic is too weak to define the structure of the natural
numbers. Since they cannot represent discrete structures, self-referential paradoxes do not arise,
and universal certification is decidable — though not tractable: the decision problem has an ex-
ponential lower bound (Fischer & Rabin, 1974) and quantifier elimination a doubly exponential
one (Davenport & Heintz, 1988).
    General systems: a general self-modifying system Mgen must express general computable
functions, requiring a discrete structure. It computes over the structure ⟨N, +, ×, 0, 1, s⟩ mathe-
matically, and any framework F adequate to reason about it interprets arithmetic. It is precisely
this discrete nature that permits Gödel numbering and enables self-reference. The moment a
system accepts discrete iterated multiplication, it enters the class of Turing-complete languages,
where intelligence acquires its power but pays the price of undecidability.
    This asymmetry — that a general self-modifying system mirrors Peano Arithmetic rather than
a decidable structure precisely because recursive self-improvement is, in essence, self-reference
in motion — is what we call the difficulty asymmetry: the more capable the system, the less
certifiable it is. It is stated informally here because its full formal weight only becomes visible
once the dynamic framework of Part II is in place; we return to it explicitly in Section 9.

2.5   Summary of results
For systems in MSM and a non-trivial safety property P , no algorithmic procedure is simulta-
neously sound, complete and valid over the whole domain for certifying that a system satisfies
P ; there are self-modifications (realistic ones, Section 9) across which no such procedure certi-
fies preservation; and for robust specifications over succinctly described finite environments, no
such procedure is moreover tractable. This is a summary of results with different hypotheses,
not a single theorem; each route has its own precise statement, and the hypotheses should be
taken from there: (i) static semantic undecidability (Rice, Section 3); (ii) incompleteness by self-
reference (Gödel, Section 4); (iii) uncomputability of universal verification over finite domains
(Trakhtenbrot, Section 5) and intractability of robust verification over succinctly described finite
environments (Section 7; this route concerns specifications over arenas, not Φ); (iv) undecidabil-
ity of preservation under self-modification, in both regimes, and, for some Φ and Σ01 properties,
Π02 -completeness of persistence (Part II).

                  Part I — The Static Case: Verifying a Fixed System

    This Part treats the system under verification as fixed: a single Turing machine Mx , evaluated
once, against a single alignment property P . We prove that no universal algorithmic procedure
can certify the safety of a highly expressive system infallibly, completely, and tractably, by
closing the only two computational vectors available to an external verifier.
    Part I establishes routes (i)–(iii) of the summary in Section 2.5: Sections 3–6 close the
two computational vectors available to a verifier — infinite means (open domains), where the
obstruction is Rice’s undecidability and Gödel’s incompleteness, and finite means (hardware
grounding), where it is Trakhtenbrot’s Theorem — and Section 7 adds the resource face.




                                                 7
3    The Semantic Barrier: Proof via Rice’s Theorem
We first establish impossibility over open (infinite) domains.

Theorem 1 (Rice, 1953). Let P be a non-trivial property of partial computable functions. Then
IP is undecidable.

Proof: a standard many-one reduction from the Halting Problem (see Appendix A.1).

Corollary 1 (Semantic inviability of alignment over open domains). Evaluating any non-trivial
safety property of a Turing-complete system is undecidable. No effective verifier can certify safe
behaviour over the full input domain.

     Note on scope. Rice’s Theorem concerns semantic properties, determined solely by the in-
put/output behaviour of Mx , independently of its internal description. Purely syntactic properties
(‘the description of Mx has at most 100 states’) are decidable and fall outside the theorem. It is
tempting to conclude that alignment is entirely on the semantic side — safety is about what the
system does. Part II shows that this is exactly where the static picture breaks down: the property
‘Mx is safe and remains safe after self-modification’ depends on the code of Mx (two programs
computing the same function can be rewritten into programs computing different functions), so
it is neither semantic nor syntactic, Rice’s Theorem does not apply to it, and it is undecidable
nonetheless (Theorem 7). The scope of Rice’s Theorem is not the scope of the obstruction.


4    The Expressivity Barrier: From Completeness to Gödel’s In-
     completeness
The undecidability established by Rice concerns the behaviour of a running machine over all
inputs. One might try to sidestep this with a static approach: fix a formal framework F prior
to execution and prove F ⊢ φsafe . This section shows that the choice of F itself leads to an
inescapable dilemma between descriptive adequacy and deductive completeness — a collapse
whose precise form is Gödel’s Incompleteness.
    A framework F intended to reason about a general self-modifying system must, at minimum,
express the structure of the natural numbers, formalised as P A ⊆ F . The designer faces a strict
dichotomy. Under First-Order Logic (FO), Gödel’s Completeness Theorem (1929) guarantees
a sound and complete proof calculus, but by the Löwenheim–Skolem Theorem no FO theory
— P A itself included — characterises N up to isomorphism: every FO theory with an infinite
model has non-standard models, so first-order reasoning cannot pin down the intended structure
a self-modifying system computes over. Under Second-Order Logic (SO), quantification over sets
and relations permits a categorical axiomatisation of N, closing the gap left by FO — but SO
has no sound and complete proof calculus, a direct consequence of Gödel’s Incompleteness once
SO can express arithmetic. Gaining descriptive power entails losing syntactic completeness.
Any F expressive enough to model a Turing-complete system must interpret at least Robinson’s
arithmetic Q — enough to represent all computable functions — placing F squarely within the
scope of Gödel’s first theorem.

Theorem 2 (Gödel Incompleteness, 1931). Let F be a consistent, effectively generated formal
system such that P A ⊆ F . Then F is incomplete: there exist sentences φ such that F ⊬ φ and
F ⊬ ¬φ. (The second incompleteness theorem — that F does not prove its own consistency —
is not used in this article.)

Proof: the standard Diagonalisation Lemma argument (see Appendix A.2).
    Consequence for static alignment verification: any framework F adequate for specifying and
reasoning about a Turing-complete system contains P A and is therefore subject to Gödel’s


                                                8
theorem. A static verifier operating in F will therefore either be incomplete (missing genuine
safety guarantees) or inconsistent (producing false certificates). The companion paper gives this
a form that does not pass through any particular sentence of F (Gumbau Mezquita, 2026b,
§8.1): for a safety property in the strict sense (‘nothing bad ever happens’, index set in Π01 and
non-trivial), the set of safe programs is co-r.e. and not recursive (Rice), hence not recursively
enumerable. Hence no sound proof system — no recursively enumerable scheme of correct
certificates — covers the safe systems: a system may be safe without any certificate of it existing,
although particular safe systems may well have proofs. This has the shape of Gödel’s unprovable
truths, at the scale of the family of systems rather than of one system; we draw no conclusion
from it about what any fixed F proves of itself, and we do not use the second incompleteness
theorem anywhere in this article. As Hernández-Espinosa et al. (2026) note in a related context,
the system resides in a formal zone where the framework cannot determine the safe decision.


5    Trakhtenbrot’s Wall: The Collapse of the Finite Strategy
Sections 3 and 4 establish impossibility over infinite domains. A natural response restricts at-
tention to the physical world, which is finite: perhaps safety can be certified by exhaustively
checking all finite hardware configurations. We call this strategy Universal Finite Verification:
the paradigm that a system’s safety can be guaranteed by confining its operation to a bounded,
finite-state environment where all possible behaviours are, in principle, verifiable. This is essen-
tially the position taken by Melo et al. (2025), who argue that restricting architectures to finite,
halting configurations resolves the undecidability of alignment identified by Rice and Gödel —
since a machine guaranteed to halt over a finite domain can, in principle, be checked exhaus-
tively. This section shows that Universal Finite Verification, too, is computationally infeasible
— not at the level of any particular finite structure, but at the level of universal quantification
over all finite structures. As Corollary 2 below makes precise, the finite-and-halting restriction
buys only a local, single-structure decidability; it does not extend to the universal guarantee
a self-modifying system actually needs, since that guarantee must hold across whichever finite
configuration the system’s self-modification (Part II) may produce next.
    Let L be a relational first-order vocabulary containing at least one binary relation symbol,
and Fin(L) the class of all finite L-structures. A universal finite safety certificate for a sentence
ψ ∈ FO(L) would establish ⊨fin ψ ⇐⇒ ∀M ∈ Fin(L), M |= ψ. The vocabulary used encodes a
Turing machine’s execution: S(x, y) a successor relation, Tq (t) that the machine is in state q at
time t, H(p, t) that the head is at position p at time t, Ca (p, t) that cell p contains symbol a at
time t.
Theorem 3 (Trakhtenbrot, 1950). Let L contain at least one binary relation symbol. The set
of finitely valid sentences Vfin = {ψ ∈ FO(L) |⊨fin ψ} is not recursively enumerable.
Proof. (Many-one reduction from the Halting Problem.) Given M = ⟨Q, Σ, Γ, δ, q0 , qhalt ⟩, con-
struct φM over L = {S, Tq , H, Ca } as the conjunction of four axiomatic blocks: (i) order and
domain — S is a strict discrete linear order with a minimum and no cycles, modelling a finite
time/tape grid; (ii) initial configuration — at t0 , head at p0 , state q0 , tape initialised with the
input; (iii) transition rules — for each δ(q, a) = (q ′ , a′ , d), the axiom
               h                                                                            i
         ∀t ∀p Tq (t) ∧ H(p, t) ∧ Ca (p, t) =⇒ Tq′ (S(t)) ∧ Ca′ (p, S(t)) ∧ H(p + d, S(t)) ,

with inertia axioms for unwritten cells; (iv) halting — ∃t Tqhalt (t).
    By construction, φM has a finite model iff M halts, giving a many-one reduction from HP to
finite satisfiability: M halts ⇐⇒ φM is finitely satisfiable. Finite satisfiability is thus RE-hard.
Finite validity is the complement of finite satisfiability of ¬ψ, so — since finite satisfiability is
RE-complete — its complement, Vfin , is co-RE-complete, hence not recursively enumerable: no
algorithm can even list all finitely valid sentences, let alone decide them.

                                                  9
Corollary 2 (Finite universality is incomputable). Certifying safety for any specific, fixed finite
structure is decidable, by exhaustive search within that structure. But certifying that a safety
property holds across all possible finite hardware configurations is co-RE-complete, hence unde-
cidable. This closes the finite-world route around Rice and Gödel at the universal level.

Remark (on the halting-machine restriction). Restricting to machines guaranteed to halt over
a finite domain (Melo et al., 2025) resolves verification at the level it claims — a fixed structure,
decidable by exhaustive search — and not beyond it: Corollary 2 relocates the difficulty to the
universal level, and Section 7 shows that the local level is intractable in the worst case once the
environment is succinctly described.


6     Formal Conclusion of the Static Impossibility
6.1   Exhaustiveness of the Two Vectors
Any algorithmic verification strategy for a safety property P of a system Mx operates with
respect to some domain of evaluation D, and there are exactly two jointly exhaustive, mutually
exclusive cases: D infinite (Vector 1, Infinite Means) or D finite (Vector 2, Finite Means).
Intermediate-looking strategies reduce to one of the two: a verifier restricted to a fixed finite
domain falls under Vector 2 and its certificate does not generalise; a verifier quantifying over a
parameterised family of finite domains (all configurations up to size n, for all n) is equivalent
to quantification over all finite structures — precisely Vector 2, governed by Theorem 3; a
verifier using probabilistic methods over infinite input spaces remains within Vector 1, blocked
by Theorem 1 at the level of exact guarantees.

Theorem 4 (Exhaustiveness and impossibility). Any verification strategy for a non-trivial safety
property of a Turing-complete system either (a) operates over an unbounded domain, in which
case it is blocked by Rice’s Theorem and Gödel’s Incompleteness, or (b) operates over a bounded
domain, in which case its certificate cannot be universal (Trakhtenbrot). In either case, no
infallible, complete, and tractable universal verifier exists (a fixed finite structure admits a sound
and complete verifier by exhaustive search, Corollary 2; it is the universal guarantee that fails).

Proof. Let V be any algorithmic verifier for a non-trivial P . If V operates over an unbounded
domain: by Theorem 1, IP is undecidable, so V cannot be both sound and complete; by Theo-
rem 2, if V relies on a static framework F ⊇ P A, F is incomplete. If V operates over a bounded
domain: if V certifies only a specific finite structure, the certificate does not generalise; if V
certifies universal finite validity, then by Theorem 3 the relevant set is not RE, so V cannot
be algorithmic. Since the two cases jointly exhaust all domains, no universal verifier exists for
either.

6.2   Summary of Part I
Theorem 4 settles routes (i)–(iii) of Section 2.5 for universal certification: the two vectors are
exhaustive, Vector 1 is closed by Rice (Theorem 1) and Gödel (Theorem 2), Vector 2 — for
universal certification — by Trakhtenbrot (Theorem 3); a single fixed finite structure remains
decidable (Corollary 2), and Section 7 bounds its cost. Section 7 adds the resource face; Part II
the dynamic one.


7     Finite Structural Unverifiability Theorem and the Trilemma
This section refines the finite-means conclusion of Section 6 (via Theorem 3) by stratifying the
bounded-domain case into a tractability barrier and a decidability barrier.


                                                 10
Definition 4 (Robust specification over a finite arena). A finite arena is a finite directed graph
of states, partitioned into system states and environment states, with an initial state and a set
of terminal states each labelled safe or unsafe. A policy σ chooses, at each system state, one
successor. A robust specification is the requirement that, under σ, every play from the initial
state — whatever successors the environment chooses at environment states — ends in a safe
terminal. The arena is succinct if its states are {0, 1}≤m and its successor relation, partition,
and labelling are computed by a circuit (or polynomial-time program) of size polynomial in m.
Two problems: Verify: given a succinct arena and a policy σ (as a circuit), does σ satisfy
the robust specification? Realise: given a succinct arena, does some σ satisfy it? This is the
standard setting of reactive synthesis (Pnueli & Rosner, 1989). It is not the transition-operator
setting of Part II: the environment’s choices make the dynamics a relation, not a function Φ, and
the objects are finite arenas, not members of MSM; the relation is discussed after Theorem 5.

Theorem 5 (Finite Structural Unverifiability). No verification framework V for robust safety
over succinctly described finite environments can simultaneously satisfy Soundness (S), Com-
pleteness (C), and Tractability (T ). This is structurally partitioned into two limits:

 (1) The Local Boundary (finite arenas, intractability): on succinct arenas with plays of
     polynomial length, Verify is coNP-complete and Realise is PSPACE-complete. Hence,
     under P ̸= NP (resp. P ̸= PSPACE), no polynomial-time procedure verifies a given policy
     (resp. synthesises a safe one) on this family.

 (2) The Universal Boundary (Trakhtenbrot’s Wall): the universal finite verification
     problem,
                      UnivVerify(M, ϕ) ⇐⇒ ∀A ∈ F, (M, A) |= ϕ
      where F is the class of all ordered finite structures and ϕ a first-order specification, is
      coRE-complete (Theorem 3). Guaranteeing universal safety over bounded domains is al-
      gorithmically uncomputable, unconditionally.

Proof of Clause 1. Hardness of Realise. Given a Ψ = Q1 x1 . . . Qn xn . φ quantified Boolean
formula, build in time O(|Ψ|) the succinct arena FΨ whose states are pairs (level i, partial
assignment a ∈ {0, 1}i ), system states at existential levels, environment states at universal
levels, successors (i+1, a · 0) and (i+1, a · 1), terminals at level n labelled safe iff φ(a) holds. Let
W be the set of winning states: a terminal (n, a) is winning iff φ(a); a system state is winning
iff some successor is; an environment state iff both are. By downward induction on i, (i, a) ∈ W
iff Qi+1 xi+1 . . . Qn xn . φ(a, ·) is true (base i = n by definition; the existential step is “or”, the
universal step “and”). A winning policy picks a winning successor at each winning system state,
so a policy satisfying the robust specification exists iff (0, ε) ∈ W iff Ψ is true; the construction
is O(|Ψ|), and TQBF ≤p Realise. Membership. A depth-first evaluation of the game tree
uses space O(n · |Ψ|) (recursion depth n, one partial assignment per frame); more generally, on
a succinct arena with plays of polynomial length, Realise is decided in polynomial space by
evaluating the alternating game recursively. (Without the polynomial-play promise, Verify
becomes PSPACE-complete even with no adversary — succinct deterministic reachability —
and Realise EXPTIME-complete.) Verify. With σ given as a circuit, a violating play is a
polynomial-length sequence of environment choices, checkable in polynomial time; so Verify
is in coNP. Hardness: instances Ψ = ∀⃗x. φ have no system states, the only policy is empty,
and Verify asks whether φ is a tautology: TAUT ≤p Verify. The hardness of Verify is
thus entirely the adversary’s, and is present already for the empty policy; the policy matters for
Realise.

Remark (where the hardness comes from). The hardness is the succinctness of the arena: an
exponential state space with a polynomial description. On an explicit arena both problems are
polynomial — the winning region of a reachability or safety game is an attractor, computable

                                                  11
in linear time, and alternating reachability on explicit graphs is P-complete — so the adversary
alone contributes nothing. What the adversary determines is the class once the arena is succinct:
with polynomial-length plays and no environment states, Realise is NP-complete (it is Sat);
with alternation, PSPACE-complete (it is TQBF); with plays of unbounded length, EXPTIME-
complete (Stockmeyer & Chandra, 1979). Reachability on succinctly represented graphs with
unbounded paths is itself PSPACE-complete (Papadimitriou & Yannakakis, 1986). The engineer-
ing consequence: making the state space explicit is what buys tractability, and it buys it even
against an adversary; removing the adversary while the space stays succinct makes verification
of a given policy polynomial but leaves synthesis NP-complete.


Remark (scope and method). Scope is existential, exactly as the instrumentation class Rinst
of the companion paper: the family contains coNP- and PSPACE-complete instances; not every
system is hard to verify; this suffices for the Trilemma. Method: the hardness comes from the
classical reductions, not from the descriptive-complexity correspondences (next remark); all the
difficulty is |FΨ | against |Ψ|. Relation to Part II: a succinct arena is finite and its dynamics
relational, so Clause 1 is not a statement about MSM or about the operator Φ; it is a statement
about the specification that a self-modifying system deployed in an environment is asked to meet,
and it applies to any system, general or not, that is verified against such a specification. The
two faces of unverifiability are, in this precise sense, about different objects: the decidability face
about the system’s own code, the resource face about the specification and the environment.


Remark (a logical reading; finiteness is not tractability). Descriptive complexity (Fagin, 1974;
Immerman, 1986) reads these classes as logics over ordered finite structures: LFP captures P
(Immerman, 1986; Vardi, 1982), existential second-order logic captures NP (Fagin, 1974), and
PFP captures PSPACE (Vardi, 1982; Abiteboul & Vianu, 1989). The winning region above is a
monotone induction, definable in LFP and polynomial in the size of the arena; the intractability
is entirely the gap between the arena and its description. Chess on an N × N board is the
familiar example: finite, decidable by backward induction, and intractable — PSPACE-complete
with a polynomial bound on moves (Storer, 1983), EXPTIME-complete without it (Fraenkel &
Lichtenstein, 1981) — because the board is a succinct description of an exponential game tree.
The correspondences are a reading of Theorem 5, not its proof.


Corollary 3 (Structural Derivation of the Soundness–Completeness–Tractability Trilemma).
Assume P ̸= NP. For any verification architecture V for robust safety over succinctly described
finite environments, the simultaneous intersection of Soundness, Completeness, and Tractability
is empty: ∀V, ¬(S(V ) ∧ C(V ) ∧ T (V )). For universal verification over all finite environments,
already S ∧ C is empty, unconditionally.
Proof. Assume some V satisfies S ∧ C ∧ T on the local problem. Sound and complete means
V decides Verify; tractable means it does so in polynomial time; by Clause 1 this puts a
coNP-complete problem in P, contradicting P ̸= NP. For the universal problem, sound and
complete means V decides UnivVerify, which is co-RE-complete by Clause 2, hence undecidable:
no such V exists, tractable or not. The two clauses are different obstructions: Clause 2 kills
soundness-plus-completeness outright; Clause 1 kills tractability on top of them.

    This trilemma sharpens, into a structural rather than statistical necessity, the semantic
Pareto frontier of alignment certification identified by Agarwal (2026) over open-ended domains:
because the verification task is bounded by coNP-hard (and, for synthesis, PSPACE-hard) and
co-RE-complete constraints even in the finite case, no framework can simultaneously satisfy all
three properties, in either the open or the bounded setting.


                                                  12
               Part II — The Dynamic Case: When the System Evolves

    Part I concerns verification of a fixed system: a single Mx , evaluated once, against a single
P . This is a substantial simplification. The remark on the difficulty asymmetry (Section 2.4)
observed informally that a general system’s capacity for self-reference is precisely what exposes
it to Gödelian incompleteness in the first place. We now make this observation precise and
extend it along the temporal axis: rather than asking whether a fixed system is safe, we ask
whether a verified safety guarantee persists across the system’s own evolution — and, if not,
exactly where and why it fails to.


8    A Formal Framework for Self-Modifying Systems
Definition 5 (Transition operator). A transition operator is a total computable function Φ :
N → N. Given an index x, Φ(x) is the index of the machine obtained from Mx by one step of
self-modification. We impose no restriction on Φ beyond computability and totality, to capture
self-improvement in its most general, unrestricted form.

Definition 6 (Evolution trace). Given an initial index x0 and a transition operator Φ, the
evolution trace is the sequence ⟨x0 , x1 , x2 , . . .⟩ defined by xt+1 = Φ(xt ).

Remark (on what, precisely, evolves). No single function φx changes over time — each φxt
is, as always, a fixed mathematical object. What evolves is which function the system computes:
the trace indexes a sequence of distinct (or repeated) functions, and the system refers to this
entire generative process — the sequence together with Φ — not to any single φxt in isolation.
The undecidability results that follow concern the relation between consecutive members of this
sequence, as mediated by Φ, not any change internal to a fixed function.

Definition 7 (Semantic stasis). An evolution trace is static from t0 onward if φxt = φxt0 for all
t ≥ t0 . Stasis is one instance — not the criterion — of the restricted expressivity that Corollary 4
identifies.

Definition 8 (Semantically well-defined (extensional) operator). Φ is semantically well-defined,
or extensional, if φx = φy =⇒ φΦ(x) = φΦ(y) : the result of a transition depends only on the
function computed by the input machine, not on the particular index describing it — the natural
analogue, for transition operators, of the restriction to semantic properties in Rice’s Theorem.
Otherwise Φ is intensional: it reads the code.

Remark (which regime is the real one). Definition 5 imposed no restriction on Φ, and for good
reason: a system that inspects and rewrites its own source code is, by that very description, in-
tensional. Two programs computing the same function have different code and will, in general, be
rewritten differently. The extensional case covers self-modification that is a function of behaviour
alone; the intensional case, supplied by the companion paper (Gumbau Mezquita, 2026b), is the
one self-modification actually lives in, and it is not a corollary of Rice’s Theorem. We give both
regimes below.

Definition 9 (P -disruption relative to f∅ , extensional regime). Let f∅ be the nowhere-defined
function and e∅ an index with φe∅ = f∅ , with f∅ ∈   / P . An extensional Φ is P -disruptive relative
to f∅ if: (a) φΦ(e∅ ) ∈
                      / P ; (b) there exists a witness q with φq ∈ P and φΦ(q) ∈ / P ; and (c) there
exists a witness p with φp ∈ P and φΦ(p) ∈ P . Condition (c) is needed: without it the elevated
property may be empty, hence decidable (the extensional non-vacuity example below without (c)
has ΛΦ (P ) = ∅).

Definition 10 (Uniform disruption, intensional regime). Let P be non-trivial and fix an index t
with φt ∈ P . A transition operator Φ is uniformly disruptive with respect to P if there is a total

                                                 13
computable wrapper w : N → N such that, for every e: (i) φw(e) = φt (all wrappers compute
the same function: the parameter e is inert data in the code); and (ii) φΦ(w(e)) ∈ P if and only
if Me (e) ↓ (positive disruption), or if and only if Me (e) ↑ (negative disruption). Condition (i)
makes the disruption genuinely intensional: the wrappers are indistinguishable by behaviour and
are separated by Φ according to a fact — the halting of Me (e) — that lives in their code. No
uniformly disruptive Φ is extensional.
Definition 11 (Pointwise valid confinement). Given a verifier V and property P , V is valid at
t for a trace ⟨x0 , x1 , . . .⟩ if V (Mxt , P ) = True ⇐⇒ φxt ∈ P . For any single, fixed t the verdict
is one bit and such a V trivially exists; uniformly in t it does not (Rice). Pointwise validity is
not in question. What is in question is whether the preservation of validity across a transition
can be certified algorithmically, in advance of the transition having occurred.


9    The Undecidability of Safety Preservation
We write, for a property P and an operator Φ,

                   ΛΦ (P ) := {x ∈ N | φx ∈ P ∧ φΦ(x) ∈ P } = IP ∩ Φ−1 (IP ),

the elevated property: safe now, and safe after the next step — the property intersected with the
property transported along Φ (the pullback lemma of Gumbau Mezquita, 2026b, §8). We call
this preservation; persistence is the whole trajectory, {x | ∀k φΦk (x) ∈ P } (Gumbau Mezquita,
2026b, Definitions 3.1–3.2). (The biconditional set {x | φx ∈ P ⇐⇒ φΦ(x) ∈ P } is a different
set, not decidable together with ΛΦ (P ) in general; we do not use it.)
Remark (one step is a step-0 question). Φ acts at compile time, so ΛΦ (P ) is a static set of
indices: “will the system be safe after its next self-modification?” is “is the compiled program
Φ(x) safe?”, a property of the next version that is intensional when read on x (Gumbau Mezquita,
2026b, §2.2). Everything said here about preservation applies equally to compilation, instrumen-
tation, or translation. The only genuinely dynamic question is persistence, and that is the one
that can climb a level (Corollary 5).
Theorem 6 (Undecidability of preservation, extensional regime). Let P be a non-trivial property
of partial computable functions with f∅ ∈/ P , and let Φ be extensional and P -disruptive relative
to f∅ . Then ΛΦ (P ) is not decidable. (Condition (c) alone suffices for this; conditions (a) and
(b) are used for the conditional question of Corollary 4.)
Proof. Since Φ is extensional (Definition 8), it descends to a well-defined map Φ∗ on functions
themselves: for any partial computable g, set Φ∗ (g) := φΦ(x) for any index x with φx = g —
the choice of x does not matter, precisely by Definition 8. Define Q := {g partial computable |
g ∈ P ∧ Φ∗ (g) ∈ P }. Q is a set of partial computable functions with IQ = ΛΦ (P ), since
Φ∗ (φx ) = φΦ(x) . Q is non-trivial: Q ̸= ∅ by (c), and Q ⊆ P ⊊ PC since P is non-trivial
(condition (b) is not needed for this). By Theorem 1, IQ is undecidable.

Theorem 7 (Undecidability of preservation, intensional regime). Let P be a non-trivial prop-
erty of partial computable functions and let Φ be uniformly disruptive with respect to P (Defini-
tion 10). Then the self-halting set K (positive disruption) or its complement (negative disruption)
reduces many-one to ΛΦ (P ) via the wrapper w; hence ΛΦ (P ) is undecidable. Moreover ΛΦ (P )
is not a semantic property: there are indices x, y with φx = φy , x ∈ ΛΦ (P ) and y ∈ / ΛΦ (P ), so
Rice’s Theorem does not apply to it.
Proof. (Gumbau Mezquita, 2026b, Lemma 3.8 and Theorem 4.1.) By (i), w(e) ∈ IP for every
e. By (ii), Φ(w(e)) ∈ IP exactly when e ∈ K (resp. e ∈ / K). Hence w(e) ∈ ΛΦ (P ) ⇐⇒ e ∈ K
(resp. e ∈
         / K), and w is total computable: this is a many-one reduction. For the last claim take
e ∈ K and e′ ∈/ K: φw(e) = φw(e′ ) = φt by (i), and exactly one of w(e), w(e′ ) lies in ΛΦ (P ).

                                                  14
Remark (one obstruction, two scales). Both proofs use the s-m-n reduction from the halting
set that proves Rice’s Theorem, and differ only in where it lands. Extensionally, the elevated
property is semantic and Rice does all the work; intensionally, it is not, Rice cannot see it, and
the reduction has to be carried out inside a single class of programs that all compute φt . This
is the precise content of “Rice one level up”: one engine, Kleene’s s-m-n theorem, at two scales,
the function and the code. The recursion theorem is not used.

Remark (non-vacuity, both regimes). Extensional regime. P = ‘halts on input 0’ and the shift
φΦ(x) (z) = φx (z + 1): Φ(e∅ ) is nowhere defined (a); an index q with φq (0) ↓, φq (1) ↑ gives (b);
any total function gives (c). Intensional regime. P = ‘computes the identity’; w(e) returns its
input and carries e as an inert comment; Φ reads the comment and synthesises the program that
simulates Me (e) and, if it halts, returns its input. Then φΦ(w(e)) is id if e ∈ K and f∅ otherwise.
Φ is a pure rewriter of text; the simulation lives in the program it outputs. The companion paper’s
class Rinst collects all such operators (Gumbau Mezquita, 2026b, Theorem 3.12). The switch is
to f∅ , not to an arbitrary unsafe witness, because a program cannot retract answers it has already
given: a switch from φg to φt is realisable iff φg ⊆ φt (Gumbau Mezquita, 2026b, Lemma 7.5).
A system can only change what it has not yet done.

Corollary 4 (Safety–Generality Dichotomy: certification requires restricted expressivity). Un-
der the hypotheses of Theorem 6 with conditions (b) and (c), or of Theorem 7, there is no total
algorithm that, given an index x with φx ∈ P , decides whether φΦ(x) ∈ P will hold after the next
self-modification step. Consequently, if for some transition operator Φ this conditional question
is decidable by a total algorithm, then Φ is not P -disruptive with (b) and (c) (extensional regime)
and not uniformly disruptive (intensional regime). Algorithmic certification of preservation is
available only for transition operators of restricted expressivity in this precise sense.

Proof. Intensional regime: Theorem 7, whose reductions land inside IP via the wrapper family, so
the conditional question inherits K or K. Extensional regime: let Q = {g ∈ P : Φ∗ (g) ∈ P } ∋ φp
and Q′ = {g ∈ P : Φ∗ (g) ∈      / P } ∋ φq (by (c) and (b)). The index sets IQ and IQ′ are
recursively inseparable: by s-m-n let xe compute φp if φe (e) = 0 and φq if φe (e) = 1 (and f∅
otherwise, which is outside P by (a)); a total decider of the conditional question would separate
{e : φe (e) = 0} from {e : φe (e) = 1}, which are recursively inseparable. The second sentence is
the contrapositive.

Remark (what the dichotomy says). The corollary concerns total deciders; a partial procedure
correct on the promise φx ∈ P may exist (with P = ‘total’ and Φ∗ (g) = g if g(0) ↓= 0, f∅ other-
wise, “output [φx (0) = 0]” is correct on every total φx and diverges elsewhere). The dichotomy is
not a statement about stasis: certification does not require the trace to become eventually static,
since a sanitiser that always outputs a fixed safe program, a constant operator, or a menu of
transformations none of which is disruptive all keep changing the system and have a decidable
conditional question. What they share is restricted expressivity in the exact sense of the corollary,
not stasis. Two glosses are not the criterion: “cannot embed a computation” (the shift embeds
nothing and is P0 -disruptive), and “a decidable, even finite, menu” (one disruptive member suf-
fices). The corrected dichotomy: certifiable preservation and unrestricted self-modification are
mutually exclusive. It does not say that self-modifying systems are unsafe; it says that no total
algorithm certifies, step by step, that they remain safe.

Corollary 5 (One step versus forever). For every total computable Φ and every P , ΛΦ (P ) ≤T
IP : certifying that a system stays safe across one step is never harder than certifying that it
is safe. By contrast, there exist total computable Φ — including extensional ones, such as
φΦ(x) (z) = φx (z + 1) — for which the persistence set {x | ∀k φΦk (x) ∈ P } is Π02 -complete for P
= ‘halts on input 0’ (Σ01 ): one level above the property. The jump is specific to Σ-type properties:
for P ∈ Π01 the persistence set is ∀k ∀s R(Φk (x), s), still Π01 .


                                                 15
Proof. (Gumbau Mezquita, 2026b, Proposition 3.13, Theorem 4.5 and Remark 4.6.) The upper
bound: Φ−1 (IP ) ≤m IP via Φ. The lower bound: with φΦ(x) (z) = φx (z + 1), the persistence set
for ‘halts on 0’ is exactly the set of total functions’ indices, which is Π02 -complete.

Remark (the property is fixed; the certificate is not). The property P is held fixed by design:
a criterion that redefined itself to match the system would certify everything. The certificate
must be recomputed at each step, and that is what Theorems 6 and 7 deny a general guarantee
for. Corollary 5 quantifies the gap: each recomputation costs no more than the property, but the
chain can be one level higher and never composes into a certificate of persistence — the failure
the supervisory tower of Section 10 exhibits one level up.


10     Supervision by Further Systems: The Regress Does Not Ter-
       minate
A natural engineering response to the impossibility results above is to delegate verification not
to a fixed algorithm but to another, more capable system: if no simple checker can certify a
general system, perhaps a second system — at least as capable as the first — can supervise
it, a third can supervise the second, and so on. This is precisely the programme of scalable
oversight (Amodei et al., 2016), which seeks to let weaker or comparable systems oversee stronger
ones, and which underlies concrete proposals such as AI safety via debate (Irving et al., 2018),
iterated amplification (Christiano et al., 2018), and recursive reward modelling (Leike et al.,
2018), together with the recursive and nested variants in which one overseer is itself checked by
another. This section formalises that strategy and shows that it does not escape the obstruction;
it reproduces it at every level. The reason is exactly the pattern already central to this article:
a supervisor powerful enough to be useful is powerful enough to fall under the same theorems it
was meant to enforce.

Definition 12 (Supervisory tower). A supervisory tower is a sequence of systems ⟨M0 , M1 , . . .⟩
in which M0 is the system to be controlled and each Mn+1 is a supervisor tasked with verifying
a non-trivial safety property P of Mn — a computable procedure that, given an index, returns
‘safe’, ‘unsafe’, or does not halt — and may consult the verdicts of the levels below it. A tower
yields a total correct certificate of preservation for M0 if the verdict of its top level is total and
agrees with ΛΦ0 (P ).

Theorem 8 (Non-termination of the supervisory regress). Let ΛΦ0 (P ) be undecidable (by The-
orem 6 or Theorem 7). Then no finite supervisory tower ⟨M0 , . . . , MN ⟩ yields a total correct
certificate of preservation for M0 , whatever the architecture, capability, or adaptivity of its levels.

Proof. The verdict of level N is the output of a computable procedure that consults other
computable procedures; a composition of computable procedures is computable. A total correct
verdict would be a total computable decision procedure for ΛΦ0 (P ), contradicting the hypothesis.
No property of the architecture enters: the undecidability is a property of the set, not of who
tries to decide it. (Gumbau Mezquita, 2026b, Theorem 6.2.)

Remark (what the supervisor need not be). Theorem 8 assumes nothing about the supervisors:
not that they are Turing-complete, not that they modify themselves. In particular it does not
rest on the tempting but unproved implication ‘adequate ⇒ Turing-complete’. The two proposi-
tions below say what any total supervisor cannot do, and what a self-modifying one inherits; the
theorem above needs neither.

Proposition 1 (Every total supervisor errs on an undecidable set). Let V be any total supervisor
(one that halts on every index; a resource bound is a special case, but any total V has a computable
running time), and let R = {x | V (x) = safe}. Then R is decidable, and the error set Err(V ) :=

                                                  16
R △ ΛΦ0 (P ) is infinite and undecidable: V is wrong about infinitely many systems, and the set
of systems it is wrong about cannot be decided either.
Proof. V is total with computable verdict, so R is decidable. If Err(V ) were decidable, ΛΦ0 (P ) =
R △ Err(V ) would be decidable. An undecidable set is infinite. (Gumbau Mezquita, 2026b,
Lemma 6.4 and Proposition 6.5.)

Remark (where the error lies). Under uniform disruption the statement is explicit: the reduction
K ≤m ΛΦ0 (P ) (or K ≤m , by polarity) via the wrapper family shows that V must err on infinitely
many wrappers w(e), and that {e | V errs on w(e)} is undecidable. No enlargement of V ’s
budget — more time, more memory, more levels — changes this; it moves the errors, never
eliminates them, and never makes them recognisable. This is the precise form of the “finite
horizon” intuition: it is not that the supervisor sees little; it is that what it fails to see is not
enumerable.
Proposition 2 (A general supervisor inherits the problem). Let Mn+1 be a supervisor that is
itself a Turing-complete system with its own transition operator Φn+1 , uniformly disruptive with
respect to some non-trivial property Pn+1 (for instance, ‘issues correct verdicts on a fixed fam-
ily’). Then ΛΦn+1 (Pn+1 ) is undecidable and K or K reduces to it, by polarity: the preservation
of Mn+1 ’s own correct operation is exactly as unverifiable as that of the system it supervises.
(Generality alone does not force this: a general supervisor with Φn+1 = id has trivial preser-
vation; the hypothesis is the disruptive transition.) The paradigmatic case is the supervision of
consistency of a deductive system, where the preservation of consistency under supervision is
Π01 -complete (Gumbau Mezquita, 2026b, Proposition 7.24).
Proof. Theorem 7 applied at level n + 1.

Corollary 6 (Who verifies the verifier: the regress is the same obstruction, not a new one).
The classical regress ‘who verifies the verifier?’ is, under Theorem 8, not an infinite sequence of
distinct difficulties but a single obstruction — the undecidability of preservation, Kleene’s s-m-n
reduction carried one level up — that no architecture removes. A bounded supervisor decides
a decidable set and errs invisibly (Proposition 1); a general one reproduces the obstruction at
its own level (Proposition 2); a tower of either kind decides nothing that its bottom level could
not. Delegating control of a general system to further systems relocates the point at which the
uncertified gap appears; it never closes it. This regress is the formal counterpart of the ‘verifier
regress’ that Yampolskiy (2017) identified informally as the organising problem of a programmatic
verifier theory; Theorem 8 shows it is not merely a regress but a non-terminating one, for a reason
that does not depend on what the verifiers are.
Remark (scalable oversight is caught between two horns, and there is a third option). Theorem 8
and the two propositions bound scalable oversight from both sides. If the overseeing system
issues total verdicts (a human overseer modelled as a procedure, a smaller model, any bounded
checker) then it decides a decidable set and, by Proposition 1, errs on an undecidable set of
systems — some self-modification violates P entirely within a blind spot the overseer cannot
even locate. If instead the overseer is itself a self-modifying system with a disruptive transition,
Proposition 2 applies: its own preserved correctness is unverifiable and stacking further overseers
does not terminate. Debate, amplification, and recursive reward modelling, read as supervisory
architectures, choose points on this spectrum; we do not formalise them here. The companion
paper adds the one thing that can be had, and it is not a certificate: for a safety property, the
monitor that runs the system and raises an alarm when it observes a violation semidecides the
violation, and no computable procedure semidecides preservation for all safe systems (Gumbau
Mezquita, 2026b, Corollary 7.17). An overseer that promises to certify safety promises what
cannot be delivered; an overseer that promises to detect the first violation, after the fact, promises
exactly what can.

                                                 17
Remark (the same obstruction, relocated). Static verification becomes dynamic by carrying
the s-m-n reduction one level up (Section 9); supervision relocates it upward again, because
undecidability is a property of the set, not of who tries to decide it. Expressivity sufficient to be
useful is expressivity sufficient to be unverifiable.

                       Part III — Practical Risks Under Evolution

    Theorem 6 concerns exact, algorithmic certification. In practice, safety claims about learning
systems are rarely of this form; they are statistical, temporally constrained, and observation-
ally partial. We now show that each of these practical alternatives is itself vulnerable to a
constructive failure mode under evolution, and that two of them — finite test coverage and
restricted observation — are instances of one general phenomenon (Theorem 9), while the third,
the uncertified window, is a matter of latency and independent of it.


11     Statistical Certification Under Evolution
(The result of this section is the special case O(t) = Tt of the universal Theorem 9; we keep it
because it is the case that matches testing practice and needs no machinery.)
Definition 13 (Effectively pointwise property). A property P is effectively pointwise if P =
{g : ∀w g(w) ∈ Pw } for a family of pointwise conditions Pw ⊆ N ∪ {↑}, each non-trivial, together
with two total computable functions s, v with s(w) ∈ Pw and v(w) ∈   / Pw for every w: a satisfying
value and a violating value, uniformly computable in w. ‘Total’, ‘computes the identity’, ‘never
outputs ρ’ are effectively pointwise; ‘g(0) = 0’ is not (its conditions are trivial for w ≥ 1), and
the results of this Part are false for it. An effectively pointwise property is not determined by
any finite set of inputs, and single-point changes at any w move behaviours in and out of P ; the
constructions below use exactly these two facts, through s and v.
     Fix, at each stage t, a finite test set Tt ⊆ N and define the empirical certification rate
            |{w ∈ T : behaviour(Mx , w) ∈ Pw }|
ĉ(x, T ) =                                     , the fraction of tests the system passes.
                           |T |
Proposition 3 (Indetectability of domain drift). Let Tt = {0, 1, . . . , t} be a monotonically
growing, bounded test sequence, and let Pw , for w ∈ N, be pointwise correctness conditions with
computable satisfying and violating values (so that P is effectively pointwise, Definition 13).
There exists a computable sequence of machines ⟨Mx0 , Mx1 , . . .⟩ and a transition operator Φ
with xt+1 = Φ(xt ) such that for every t: (i) ĉ(xt , Tt ) = 1; (ii) φxt violates Pw at w = t + 1;
and (iii) no verification scheme depending only on the behaviour of Mxt on Tt can distinguish
this trace, at any stage, from a trace correct on all of N (a scheme that reads the code sees the
violating default branch; the claim is about behavioural evidence).
Proof. For t ∈ N, let Mxt compute φxt (w) = a fixed output satisfying Pw if w ≤ t, and a
fixed output violating Pw if w > t — a direct table-plus-default construction, requiring no
diagonalisation. By s-m-n, t 7→ xt is computable, and Φ may be taken as any total computable
extension of Φ(xt ) = xt+1 along this trace; no extensionality is needed for this or for any result
of Part III.
    (i) Every w ∈ Tt satisfies w ≤ t, so ĉ(xt , Tt ) = 1. (ii) w = t + 1 > t always, so the violation
is present at every stage, immediately past the boundary of the current test set. (iii) A scheme
inspecting only the behaviour of Mxt on Tt sees only values satisfying Pw ; the violation at
w = t+1 ∈  / Tt lies outside its view — stage t is indistinguishable from a stage where φxt satisfies
Pw for all w ∈ N.

   The point is not that this adversarial trace is likely to arise by accident, but that perfect
empirical certification, repeated at every stage of an evolving system, is logically compatible

                                                 18
with systematic, undetected failure just beyond the tested region — at every stage, not only
asymptotically, since Tt is always finite while N is not. Proposition 1 sharpens this: a total
scheme not only misses violations outside its window; the set of systems on which it is wrong is
itself undecidable.

Remark (an instance: empirically validated self-improvement). The Darwin Gödel Machine
(Zhang et al., 2025) accepts a rewrite of a coding agent when the new agent performs well on
a fixed suite of benchmarks: at each stage the evidence is behaviour on a finite test set, exactly
the Tt of Proposition 3. For any effectively pointwise property the designers wish the lineage to
keep, the proposition says that success on the suite at every stage is logically compatible with a
violation just outside it at every stage; Theorem 9 says the same for any faithful scheme that
certifies on finite behavioural evidence. The safety measures the authors adopt — sandboxing
and human review — are, in the terms of Section 15, Boxing and hierarchical supervision: they
bound consequences and relocate the gap, and neither certifies preservation. In the verification
hierarchy of Chen, Wang & Qu (2026), benchmark validation sits below formal verification; even
the top of that hierarchy certifies only membership in a subclass (Gumbau Mezquita, 2026b,
Proposition 8.1). This is not a criticism of the system, which does not claim certification; it is
a statement of what its validation step can and cannot establish.


12     The Inevitability of an Uncertified Window
We now identify a different, more elementary source of risk: a temporal window, between suc-
cessive stages, during which the system already acts under a version of itself that has not yet
been certified — not because the certifying test was incomplete, but because certification simply
takes time.

Definition 14 (Verification scheme with temporal cost). A verification scheme is a pair (V, τ ),
where V is a pointwise verifier (Definition 11) and τ : N → N bounds the number of steps V
requires to certify Mx , as a function of a size parameter of x.

Definition 15 (Unstalled operation). The system operates in unstalled mode under Φ if, once
xt+1 = Φ(xt ) is computed, Mxt+1 begins producing outputs before V completes certification of
Mxt+1 . This is the opposite of the stalled regime — re-certification with stasis between steps
(Section 15) — in which the system halts and waits for V ’s verdict before resuming.

Proposition 4 (Inevitability of the uncertified window). Let (V, τ ) satisfy τ (t) > 0 for all
sufficiently large t. (This needs no conjecture: a non-trivial verifier must at least read its input;
τ here is the cost at stage t, i.e. on input xt . Whether it grows without bound depends on the
scheme; Theorem 5 concerns arenas, not index verifiers, and is not invoked.) If the system
operates in unstalled mode, then for every such t there exists a temporal window Wt , of length
at least τ (t) > 0, during which Mxt+1 executes while V has not yet returned a verdict on Mxt+1 .

Proof. Immediate: under unstalled operation, execution of Mxt+1 begins at or before V begins
certifying it; since V requires at least τ (t) steps to return a verdict, there is an interval of at least
that length during which Mxt+1 is already executing and V ’s verdict is not yet available.

Corollary 7 (The window is exactly where Theorem 6 bites). Under Proposition 4, if Φ ad-
ditionally satisfies the hypotheses of Corollary 4, no algorithm — not even one with complete
knowledge of Mxt — could have determined, prior to Wt , whether φxt+1 ∈ P : the property of the
version that acts throughout the window. (Whether a violation occurs within the finite window
is decidable by simulation; the uniform undecidability is that of the property, not of the window
event.)



                                                   19
Proof. Under the hypotheses of Theorem 6 with conditions (b) and (c), or of Theorem 7, Corol-
lary 4 says that no total algorithm decides, given x with φx ∈ P , whether φΦ(x) ∈ P ; in particular
none does so uniformly along the trace. (Undecidability of ΛΦ (P ) alone would not suffice: a
sanitiser has ΛΦ (P ) = IP undecidable and a trivially decidable conditional question.) Since Wt
is, by Proposition 4, the interval during which Mxt+1 already acts while V ’s verdict on it is still
pending, the system’s behaviour throughout Wt is governed by a property whose status was,
prior to Wt , undecidable from xt by any algorithm whatsoever.

     Proposition 4 and Corollary 7 anticipate the universal result of Section 14: a non-zero ver-
ification cost, combined with a system that does not wait, suffices to guarantee a window in
which Theorem 6’s undecidability is not merely a property of the formalism but a feature of the
system’s actual operation.


13    The Observational Failure Mode: The Weakness of Bounded
      Observation
Confining a supervisor to weak logics, short horizons, or physical boxes — the very mechanism
securing decidability in Part I — leaves any behaviour outside that restricted vocabulary invisible
to it. We now make this precise, showing it is not an incidental shortcoming of any particular
scheme but a consequence of finite observation alone.
    We first fix the general notion of verification scheme that this section and the next will
analyse.
Definition 16 (Bounded verification scheme). A bounded verification scheme is a triple (V, O, τ )
where O : N → Pfin (N) is computable, returning for each stage t a finite observation win-
dow O(t) ⊆ N; τ : N → N is computable; and V (Mxt , P ) is computed solely as a function of
{behaviour(Mxt , w) : w ∈ O(t)}, in time at most τ (t). This subsumes the growing test sequence
of Proposition 3 (O(t) = Tt ) and the fixed observation window of Definition 18 below (O(t) = OV
for all t) as special cases.
Definition 17 (Faithful scheme). (V, O, τ ) is faithful if, whenever behaviour(Mx , w) satisfies
Pw for every w ∈ O(t), V (Mx , P ) = True — V does not reject evidence that is, by its own lights,
entirely correct. (Observations not completed within the time budget τ (t) count as unobserved;
faithfulness quantifies over what was actually observed.) Any verifier intended to certify rather
than to obstruct satisfies this condition.
Remark (faithfulness and finite determination). Faithfulness asks V to certify on the strength of
finite evidence. Whether that can be sound depends on the property: if P is settled by the window
— the case that Definition 13 excludes — a faithful bounded verifier can be correct and complete
(‘g(0) = 0’ with window {0}). The results below assume P is effectively pointwise; under that
hypothesis no finite window settles membership, and certifying on finite evidence is certifying
what the evidence cannot settle. The companion paper’s polarity result (Gumbau Mezquita, 2026b,
Proposition 7.12) is a statement about operators with anchors, not about window verifiers, and
is not used here.
Definition 18 (Restricted observation). A verifier V has observation window OV ⊆ N if
V (Mx , P ) is computed solely as a function of {behaviour(Mx , w) : w ∈ OV }. V is L-restricted
if OV is a proper subset of N, fixed in advance and independent of x.
Proposition 5 (Invisibility under restricted observation). Let V be L-restricted with win-
dow OV ⊊ N, and P effectively pointwise (Definition 13). There exists a semantically well-
defined Φ and an index x with φx ∈ P such that: (i) φΦ(x) ∈    / P ; (ii) behaviour(Mx , w) =
behaviour(MΦ(x) , w) for every w ∈ OV ; hence (iii) V (Mx , P ) = V (MΦ(x) , P ) — V certifies
identically before and after, detecting no change.

                                                20
Proof. Fix w∗ ∈/ OV . Define Φ so that Φ(y) is the index of the machine agreeing with My
on every w ̸= w∗ , but producing on w∗ the violating value v(w∗ ) regardless of My ’s original
behaviour there — a uniform, computable single-exception modification, hence total computable
and semantically well-defined by construction.
   Choose x such that Mx satisfies Pw∗ correctly (possible since P is non-trivial) and φx ∈ P .
MΦ(x) agrees with Mx on all w ̸= w∗ and violates Pw∗ at w∗ , giving φΦ(x) ∈  / P — (i). Since
 ∗
w ∈/ OV , every w ∈ OV satisfies w ̸= w , so behaviour agrees on all of OV — (ii). Since V
                                         ∗

depends only on behaviour within OV , (ii) gives (iii) immediately.

Remark (the modification is an augmentation). The Φ of Proposition 5 adds one forbidden
value at one unobserved input. This is the single-exception rewrite: the companion paper’s
irrevocability lemma (Gumbau Mezquita, 2026b, Lemma 7.5) concerns switches inside a running
program on inputs not yet answered; here the rewrite is at compile time and may overwrite a
defined value, which is why it is always realisable for a rewriter even where it would not be
for a monitor. That the move can be placed outside any finite window is the whole content of
invisibility.

Corollary 8 (Weakness of bounded observation, formalised). Two facts, of different kinds,
bound what a computable verifier can establish. Decidability: any total verifier V decides a
decidable set and therefore, for a property with undecidable index set, errs on an undecidable set of
systems (Proposition 1). Observation: any verifier that depends only on behaviour within a fixed
finite window, applied to an effectively pointwise property, is invisibly evaded by a single-exception
rewrite outside its window (Proposition 5). The first bounds what any total procedure can decide;
the second bounds what behavioural evidence can show. Neither is removed by enlarging the
window, and the second is not removed by unbounded resources.

   A scheme that is not faithful rejects some system whose observed behaviour is entirely correct,
and so fails on a fixed system with no dynamics at all; faithfulness is the minimal property that
makes a verifier informative, and the only class for which evadability is a non-trivial question.
Section 14 treats it.


14     Universal Evadability of Bounded Verification Schemes
Propositions 3 (Section 11) and 5 (Section 13) are existence results: some trace evades a par-
ticular verification scheme exhibited in each case. The notion of a bounded verification scheme
(Definition 16) already unifies both as special cases; we now prove that the resulting statement
holds universally, for every faithful scheme of that general form rather than for the specific
instances exhibited above.

Theorem 9 (Universal evadability of faithful bounded schemes). Let (V, O, τ ) be any faithful
bounded verification scheme depending only on behaviour within its window, and P effectively
pointwise (Definition 13). There exists a total computable Φ and an evolution trace ⟨x0 , x1 , . . .⟩
with xt+1 = Φ(xt ), such that for every t: V (Mxt , P ) = True, while φxt ∈
                                                                          / P.

Proof. Since (V, O, τ ) is fixed in advance, O is known and may be used explicitly. For each t, let
Mxt compute the function w 7→ s(w) for w ∈ O(t) and w 7→ v(w) for w ∈      / O(t); it satisfies every
pointwise condition on O(t) and violates every one outside. Since O, s and v are computable,
the map t 7→ xt is computable by s-m-n (and can be taken injective with decidable range), and
Φ is any total computable extension along this trace, as in Proposition 3.
    Certification: by construction, behaviour(Mxt , w) satisfies Pw for every w ∈ O(t); since the
scheme is faithful, V (Mxt , P ) = True. Genuine violation: fix any wt∗ ∈ N \ O(t); by construction
behaviour(Mxt , wt∗ ) violates Pwt∗ , so φxt ∈
                                             / P.



                                                 21
     This resolves, for the class of faithful schemes, the general question: every bounded verifica-
tion scheme admits a trace it certifies at every stage while genuinely and persistently violating
the property in question, since any computable verifier must inspect some finite window at each
stage, and finiteness alone already suffices for evasion. Faithfulness also states precisely what
trusting a verifier can and cannot mean: we can trust that a faithful V will not call correct be-
haviour incorrect, but not, in general, that when it says correct the system is in fact correct for
all time — the latter is what Theorem 9 shows no faithful bounded scheme can guarantee across
an evolving trace. This sharpens the distinction between the undecidability of verification, a
fact about every possible verifier, and the insecurity of any particular system, a fact about that
system’s actual behaviour that no theorem can settle in advance.

Remark (what the companion paper adds). Theorem 9 exhibits one evading trace per scheme,
for effectively pointwise properties. The companion paper’s Corollary 7.8 is a different statement,
about the elevated property ΛE (P ) of an operator with a safety-polarity anchor: there, the set
of systems that preserve P is not recursively enumerable, so no scheme of certificates covers it.
The two results are consistent and complementary: the first is about windows, the second about
preservation under an anchored rewrite. Neither says that a safe system can never be certified
— a proof system may certify infinitely many; what neither a window nor a certificate scheme
can do is cover them all.

Remark (a diagonal argument, in the lineage of Cantor and Turing). The construction is
diagonal in the exact sense of Cantor’s diagonal and Turing’s halting argument. In each, one
is given a resource that can only cover a finite or enumerable part of an unbounded domain —
the digits an enumeration assigns, the predictions a purported halting-decider makes, or here the
finite window O(t) a computable verifier inspects — and one builds an object that agrees with
everything the resource covers while differing at a point it does not reach. Cantor’s real differs
at the n-th digit; Turing’s machine differs on its own index; the evolving system here differs at
any w∗ ∈ N \ O(t). The mechanism is one and the same in all three: no finite or enumerable
cover can exhaust an unbounded domain, so a diagonal point always remains. A computable
verifier’s finiteness is precisely such a cover, and the system’s behaviour always has a ‘beyond’
it has not looked at — which is, once more, the Expressivity Invariant, now in its sharpest and
most elementary form. That impossibility results of this kind rest on a shared diagonal, fixed-
point construction — in the lineage of Cantor, Gödel and Lawvere — has been noted at the
level of proof technique (Brcic and Yampolskiy, 2023); the Expressivity Invariant sharpens this
into a shared generative operation, since the dynamic and supervisory barriers are one s-m-n
reduction from the halting set, carried out once inside a class of behaviourally identical programs
and read off thereafter — “diagonalisation amortised”, in the companion paper’s phrase — while
the practical barriers of this Part are diagonal in Cantor’s direct sense: a finite cover of an
infinite domain always leaves a point uncovered, and no reduction from K is needed.

    Section 12 remains relevant independently of Theorem 9: even where a scheme resists the
specific trace constructed there — by refusing to certify until O(t) exhausts all behaviour relevant
to P , at the cost of τ (t) growing without bound — an uncertified window of non-zero length
remains unavoidable whenever the system does not stall to await an ever-slower verdict.

                                     Part IV — Synthesis

    Parts I–III established the Expressivity Invariant and its two corollaries as formal results.
This final Part turns from proof to consequence: what the invariant means for how self-modifying
systems are actually built and contained, and what remains true once every idealisation is
dropped.




                                                22
15     Practical Implications
Translating the static barriers of Part I and the dynamic barriers of Parts II–III into software
engineering practice, the contemporary state of the art captures this structural collapse as a
definitive impossibility result rather than a temporary limitation. This is consistent with the
framework proposed by Seshia et al. (2022) in their paradigm of Verified AI, which posits that
the gap between high-level safety specifications and low-level system behaviour forces engineers
to navigate a rigorous trade-off between the depth of the properties verified and the complexity
of the environments considered — precisely the trade-off that Section 7 above grounds in explicit
reductions, and that the taxonomy below realises as concrete design choices.

Remark (three failure modes, three causes). Three risks identified above are sometimes conflated
but require different remedies. The logical mode is the undecidability of preservation (Theorems 6
and 7), addressed only by restricting Φ or P . The temporal mode (Proposition 4) is latency,
addressed only by stalling. The observational mode (Proposition 5, Corollary 8) has two causes
— a total verifier decides a decidable set, and behavioural evidence on a finite window cannot
settle an effectively pointwise property — and no widening of the window removes the second.
Removing one mode leaves the others in place.

    This renunciation materialises in a taxonomy of containment architectures, developed orig-
inally for the static case (confining a fixed system to a decidable fragment) but which we now
read against the static and dynamic results together. The Soundness–Completeness–Tractability
Trilemma has exactly three vertices, and there are exactly three pure strategies — one sacrific-
ing each vertex; two further strategies pay nothing to the Trilemma and, for that very reason,
do not attack the verification obstruction but operate outside it. Two further items are not
containment strategies at all but changes of promise, and we list them separately.

15.1    Three strategies that sacrifice a vertex of the Trilemma
Logical Isolation (Shielding). A rigid monitor formatted within a decidable logical fragment
surrounds the agent (Alshiekh et al., 2018); the agent loses agency over decisions inexpressible
in that language. Dynamically, this is the analogue of restricting Φ to a fixed set of permitted
transformations none of which is disruptive (a decidable, or even finite, menu is not enough
by itself: one disruptive member suffices): Φ is then not uniformly disruptive (Definition 10),
Theorem 7 does not apply, and preservation may become decidable. This is the corrected
dichotomy of Corollary 4 in constructive form. One restriction must not be confused with it:
typed rewriting whose reduction steps preserve the computed function (strong normalisation in
proof theory) is semantic stasis, the trivial case; and primitive-recursive rewriting in general
restricts nothing here — the shift of Corollary 5 is primitive recursive, its trajectory does not
terminate, and the anchor to the halting set is constructible with primitive-recursive rewriters,
so Π01 -completeness of safety survives (Gumbau Mezquita, 2026b, §8.1). On the resource face,
bounding the depth of self-modification makes the trajectory space explicit rather than succinct,
which is the source of the PSPACE cost (Remark after Theorem 5). Sacrifice: completeness —
legitimate self-modifications outside the menu are barred.

Inversion of Burden (Proof-Carrying Code). The agent must attach a formal proof of
safety before acting; the verifier remains fast, but the agent cannot execute legitimate actions
whose proof exceeds the allowed complexity. Dynamically: mandatory re-certification with
stasis between steps, addressing only the temporal mode (Proposition 4), not the logical one
(Theorem 7). The companion paper states what a carried proof can be (Gumbau Mezquita,
2026b, §8.1): a proof of safety attached to an action certifies membership in the subclass the
proof scheme covers, never the property in general, since no recursively enumerable scheme


                                               23
covers all safe systems. Proof-carrying code works exactly to the extent that it restricts what
may be carried. Sacrifice: bounded latency and availability.

Temporal Myopia (Bounded Horizon Planning). Optimisation is limited to k future
steps, making the decision tree decidable at the cost of strategic blindness to long-term con-
sequences — the temporal analogue of the uncovered input window of Theorem 9. Sacrifice:
soundness beyond the horizon (the guarantee holds only within it).

15.2       Two strategies that operate outside the Trilemma
Physical Confinement (AI Boxing). The agent is converted into a closed oracle isolated
from actuators and networks. It sacrifices no vertex of the Trilemma: what it reduces is the causal
expressivity of the environment — the reach with which a failure can affect the world — not any
property of the verification problem. It neither detects misalignment nor makes it verifiable; it
bounds its consequences. On the resource face it does one thing: without environment states a
given policy has a single play, so Verify becomes polynomial; Realise stays NP-complete on a
succinct arena, and only an explicit arena makes both tractable. Price: external reach, outside
the Trilemma.

Hierarchical Supervision. A supervisor at least as capable as the agent audits it, and an-
other audits that one. It sacrifices nothing in the agent — which is exactly why it does not
contain the obstruction but relocates it upward. By Theorem 8, no tower decides an undecid-
able set, whatever its levels are; by Proposition 1, a bounded overseer errs on a set of systems it
cannot locate; by Proposition 2, a general overseer inherits the same undecidability at its own
level. A finite tower has an uncertified top; an infinite one may converge pointwise to the right
verdict (by the limit lemma, whenever the property is ∆02 ) but with no computable modulus of
convergence: at no stage does one know that the verdict has settled. Price: none — and hence
no containment.

Strategy                   Price (Trilemma ver-     Acts on                      Leaves open
                           tex)
Shielding                  generality of Φ (C:      logical mode; succinctness   self-improvement ca-
                           some actions barred)                                  pacity
Proof-carrying code        latency (T)              temporal mode                logical mode (Thm. 7)
Bounded horizon            exactness (S: unsound    outside-window               long-term evasion
                           beyond horizon)
Boxing                     causal reach (outside    consequences                 the whole obstruction
                           the Trilemma)
Hierarchical supervision   none                     relocates upward             everything (Thm. 8)

Table 1: Containment strategies against the two faces of unverifiability, with the Trilemma
vertex (S, C, T) each pure strategy sacrifices.


Remark (where tractability can be bought). The source of the resource cost is the succinctness
of the arena (Remark after Theorem 5). Making the arena explicit — a bounded, enumerable
menu of transformations and states — brings robust verification into P, adversary or not, since
the winning region of an explicit game is computable in linear time. What the adversary and the
length of plays determine is the class while the arena stays succinct: NP for existential choice
with polynomial plays, coNP for verifying a fixed policy, PSPACE for alternation with polynomial
plays, EXPTIME for unbounded alternating plays (Stockmeyer & Chandra, 1979). Shielding pays
on the succinctness side; Boxing, by removing the adversary, makes verification of a given policy



                                                   24
polynomial but leaves synthesis NP-complete on a succinct arena; only an explicit arena makes
both tractable.

15.3    Two changes of promise that are not containment
Detection is optimal. The results above are negative. The companion paper supplies the one
positive statement that survives them (Gumbau Mezquita, 2026b, Corollary 7.17): for a safety
property, the violation is semidecidable and the preservation is not, so a monitor that runs the
system and raises an alarm when it observes a prohibited event detects every violation that
occurs, after it occurs; no computable procedure semidecides preservation for all safe systems (a
proof search may certify infinitely many, never the totality), and none anticipates the violation.
Runtime-verification monitors, shields, and watchdogs realise this bound. A supervisor that
promises to certify that a self-modifying system will remain safe promises what cannot be
delivered; one that promises to detect the first violation when it happens promises exactly
what can, and should be designed, evaluated, and trusted on that basis alone.

Fix the reference. Comparing an evolving system against another evolving system (differ-
ential testing between two model versions, shadow deployment, distillation checks) inherits all
of the hardness above and keeps the normal form “still safe = in agreement and the trigger has
not fired” only under a condition the designer must enforce: the discrepancy trigger has to be
confined to systems that can still answer, since on a system that has gone silent the trigger may
fire without any discrepancy ever appearing (Gumbau Mezquita, 2026b, §7.5). Comparing the
evolving system against a frozen, total reference — an executable specification, a pinned version,
a golden model — removes the condition: the case becomes a literal instance of the companion
paper’s class, the preservation property has its normal form unconditionally, its complexity is
known, and the only possible verdict direction (detect discrepancy, never certify agreement) is
explicit. Good evaluation practice already compares against something that does not move;
the theory says what is gained. Zenil (2026) reaches the same remedy on statistical grounds:
recursive self-training that loses its exogenous grounding degenerates.
    A scheme most resembling current industry practice combines re-certification with statistical,
rather than exact, guarantees: certify at 99.9% confidence, halt, allow one evolution step, re-
certify, and so on. Proposition 3 shows this does not escape the underlying tension: it converts
an algorithmic impossibility into a silent reliability risk, since perfect performance on an evolving
but always-bounded test suite is compatible with undetected failure just outside it.
    In every case, escaping either the static barriers of Part I or Theorems 6 and 7 (dynamic)
in practice requires sacrificing exactly one of: the generality of the transition operator Φ or the
expressivity of the monitored fragment, bounded verification latency, or the exactness of the
safety guarantee. One thing cannot be traded for anything: for a safety property in the strict
sense, violation can be watched for, and no sound procedure certifies all safe systems. This is the
same Soundness–Completeness–Tractability Trilemma of Corollary 3, reappearing, in a different
guise, the moment the system under verification is allowed to change.


16     Discussion: Consequences for Deployed Systems
Since every AGI, autonomous agent, or self-improvement loop is a member of MSM (the scope
remark of Section 2.1), the barriers above are not abstract warnings but constraints on what
can be promised of a real system. The operational consequence is not “nothing is safe” but
four precise statements. (1) Preservation certification is not a deferred engineering goal but a
structural impossibility: there are self-modifications — realistic ones, Section 9 — for which no
improvement in hardware, algorithms, or test suites makes it attainable (Part II). (2) A frozen
instant can be certified; a trajectory cannot. A pinned version over a fixed structure is verifiable


                                                 25
(Corollary 2); what no algorithm can do is carry that certificate across a change the system
makes to itself. (3) For a safety property, violation is what can be established uniformly, and
only after the fact: no procedure semidecides preservation for all safe systems, so a certificate
of safety is always a certificate of membership in some subclass; a frozen instant can be certified
(point 2), a trajectory cannot. (4) Every practical guarantee is a point chosen on the tension,
not a resolution of it: responsible deployment does not consist in finding the containment that
works, but in choosing consciously which vertex of the Trilemma is sacrificed, on which side
(agent or environment) the resource cost is paid, and in making both explicit.
    The value of the result is one of localisation: it draws precisely where the total guarantee
breaks, and hence where ambition must move from certainty to risk management, and from
certification to detection. That a gap exists for every faithful verifier is established with math-
ematical certainty; whether a particular deployed system’s evolution ever falls into it is an
empirical question about that system, which no universal theorem can answer in advance.


17     Future Work
Three directions remain open, each a precise question rather than a vague area.

Characterising the hard boundary. Clause 1 of Theorem 5 establishes that the class con-
tains PSPACE-complete instances (an existential result). It remains open which alignment spec-
ifications are intractable and which admit efficient verification: to characterise the boundary
between the two, and to determine whether deciding on which side a given specification falls is
itself a hard problem. This would turn the warning “hard cases exist” into a map of which cases
are hard.

Partial mitigations with quantified cost. The taxonomy of Section 15 identifies what
each strategy sacrifices, but not how much. The remark after Theorem 5 suggests the natural
programme: index the verification problem by whether the trajectory space is explicit or suc-
cinct, by the presence of alternation, and by the length of plays, and locate each containment
architecture on the resulting grid, whose known corners are P (explicit arena, with or without
adversary; and succinct without adversary for verifying a given policy), NP (succinct, no adver-
sary, synthesis), coNP (succinct, adversary, given policy), PSPACE (succinct, polynomial plays,
alternation) and EXPTIME (succinct, unbounded plays, alternation). This would convert the
binary dichotomy (general versus certifiable) into a Pareto frontier of achievable trade-offs with
complexity classes at its vertices; each cell needs its own reduction, and we claim none beyond
those four.

The decidability grid. The companion paper leaves open the analogous question on the
logical face — a classification of transition operators by the degree of the transported property,
and the study of operators with several triggers (Gumbau Mezquita, 2026b, §9). Unifying the
two faces — resource regime against fixed-point structure — in a single grid is left for synthesis
work.


18     Conclusion
Statically, no verifier certifies the safety of a fixed, sufficiently expressive system infallibly, com-
pletely, and tractably: over unbounded domains by Rice and Gödel, over all finite configurations
by Trakhtenbrot, and over succinctly described finite environments by the intractability of robust
verification (coNP) and synthesis (PSPACE) — the Trilemma (Corollary 3). Dynamically, preser-
vation of a safety property across one step of self-modification is undecidable in both regimes:


                                                  26
by Rice’s Theorem when the step reads only behaviour, and by the same s-m-n reduction inside
a single behavioural class when it reads code, which is what self-modification does (Theorems 6
and 7). One step is never harder than the property; persistence along an unbounded trajectory
can climb one level, as it does for Σ01 properties (Corollary 5). Certification of preservation by
a total algorithm is available only to transformations of restricted expressivity (Corollary 4).
Delegation does not help: no tower of supervisors decides an undecidable set, and every total
supervisor errs on a set of systems it cannot locate (Section 10). Practical schemes that certify
on finite behavioural evidence are evaded by construction for effectively pointwise properties
(Theorem 9).
    Two things survive. A monitor that runs the system and raises an alarm on the first observed
violation semidecides violation, while no sound procedure certifies all safe systems: supervision
should promise detection, not certification. And comparison against a frozen, total reference
has the full theory unconditionally, where comparison between two evolving systems has it only
under a design condition.
    These results are expressions of one Expressivity Invariant, whose demonstrated form is
the Expressivity Principle of the companion paper: certifiability across self-modification and
unrestricted self-modification cannot be jointly maximised. Containment strategies choose where
to stand on that tension; they do not remove it. Whether a particular deployed system ever falls
into the gap is an empirical question about that system, which no universal theorem answers in
advance. ■


References
 [1] Abiteboul, S., & Vianu, V. (1989). Fixpoint extensions of first-order logic and datalog-like
     languages. Proceedings of the 4th Annual IEEE Symposium on Logic in Computer Science
     (LICS).

 [2] Agarwal, A. (2026). No Certificate for Alignment: Two Independent Impossibilities and the
     Pareto Frontier of Achievable Safety Guarantees. arXiv preprint arXiv:2603.08761v2.

 [3] Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S., & Topcu, U. (2018). Safe
     Reinforcement Learning via Shielding. Proceedings of the AAAI Conference on Artificial
     Intelligence.

 [4] Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016).
     Concrete Problems in AI Safety. arXiv preprint arXiv:1606.06565.

 [5] Brcic, M., & Yampolskiy, R. V. (2023). Impossibility Results in AI: A Survey. ACM Com-
     puting Surveys, 56(1), Article 8, 1–24.

 [6] Chandra, A. K., Kozen, D. C., & Stockmeyer, L. J. (1981). Alternation. Journal of the
     ACM, 28(1), 114–133.

 [7] Chen, M., Wang, L., & Qu, B. (2026). Recursive self-improvement in AI: from bounded
     self-refinement to autonomous research loops. arXiv preprint arXiv:2607.07663.

 [8] Christiano, P., Shlegeris, B., & Amodei, D. (2018). Supervising strong learners by amplify-
     ing weak experts. arXiv preprint arXiv:1810.08575.

 [9] Davenport, J. H., & Heintz, J. (1988). Real quantifier elimination is doubly exponential.
     Journal of Symbolic Computation, 5(1–2), 29–35.

[10] Fagin, R. (1974). Generalized First-Order Spectra and Polynomial-Time Recognizable Sets.
     In Complexity of Computation (R. Karp, ed.).


                                               27
[11] Fischer, M. J., & Rabin, M. O. (1974). Super-exponential complexity of Presburger arith-
     metic. SIAM–AMS Proceedings, 7, 27–41.

[12] Fraenkel, A. S., & Lichtenstein, D. (1981). Computing a perfect strategy for n × n chess
     requires time exponential in n. Journal of Combinatorial Theory, Series A, 31(2), 199–214.

[13] Galperin, H., & Wigderson, A. (1983). Succinct representations of graphs. Information and
     Control, 56(3), 183–198.

[14] Gödel, K. (1929). Über die Vollständigkeit des Logikkalküls. PhD Thesis, University of
     Vienna.

[15] Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und ver-
     wandter Systeme I. Monatshefte für Mathematik und Physik.

[16] Good, I. J. (1965). Speculations concerning the first ultraintelligent machine. Advances in
     Computers, 6, 31–88.

[17] Gumbau Mezquita, J. P. (2026b). Rice’s theorem under self-modification: elevation opera-
     tors and a normal form. arXiv preprint arXiv:2609.11326 (v2).

[18] Hernández-Espinosa, A., Abrahão, F. S., Witkowski, O., & Zenil, H. (2026). Neurodivergent
     influenceability in agentic AI as a contingent solution to the AI alignment problem. PNAS
     Nexus, 5(4), pgag076.

[19] Immerman, N. (1986). Relational queries computable in polynomial time. Information and
     Control, 68(1–3), 86–104.

[20] Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. arXiv preprint
     arXiv:1805.00899.

[21] Kleene, S. C. (1952). Introduction to Metamathematics. North-Holland, Amsterdam.

[22] Leike, J., Krueger, D., Everitt, T., Martic, M., Maini, V., & Legg, S. (2018). Scalable agent
     alignment via reward modeling: a research direction. arXiv preprint arXiv:1811.07871.

[23] Melo, G. A., Máximo, M. R. O. A., Soma, N. Y., & Castro, P. A. L. (2025). Machines
     that halt resolve the undecidability of artificial intelligence alignment. Scientific Reports,
     15, 15591.

[24] Papadimitriou, C. H., & Yannakakis, M. (1986). A note on succinct representations of
     graphs. Information and Control, 71(3), 181–185.

[25] Pnueli, A., & Rosner, R. (1989). On the synthesis of a reactive module. Proceedings of the
     16th ACM POPL, 179–190.

[26] Rice, H. G. (1953). Classes of Recursively Enumerable Sets and Their Decision Problems.
     Transactions of the American Mathematical Society.

[27] Rogers, H. (1967). Theory of Recursive Functions and Effective Computability. McGraw-
     Hill, New York.

[28] Schmidhuber, J. (2003). Gödel machines: fully self-referential optimal universal problem
     solvers. arXiv preprint cs/0309048.

[29] Seshia, S. A., Sadigh, D., & Sastry, S. S. (2022). Towards Verified Artificial Intelligence.
     Communications of the ACM.


                                                28
[30] Soare, R. I. (1987). Recursively Enumerable Sets and Degrees. Springer-Verlag, Berlin.

[31] Stockmeyer, L. J., & Chandra, A. K. (1979). Provably difficult combinatorial games. SIAM
     Journal on Computing, 8(2), 151–174.

[32] Storer, J. A. (1983). On the complexity of chess. Journal of Computer and System Sciences,
     27(1), 77–100.

[33] Tarski, A. (1951). A Decision Method for Elementary Algebra and Geometry (2nd ed.).
     University of California Press, Berkeley.

[34] Trakhtenbrot, B. A. (1950). The Impossibility of an Algorithm for the Decidability Problem
     on Finite Classes. Doklady Akademii Nauk SSSR.

[35] Turing, A. M. (1936). On Computable Numbers, with an Application to the Entschei-
     dungsproblem. Proceedings of the London Mathematical Society, 2(42), 230–265.

[36] Vardi, M. Y. (1982). The complexity of relational query languages. Proceedings of the 14th
     Annual ACM Symposium on Theory of Computing (STOC).

[37] Yampolskiy, R. V. (2017). What are the ultimate limits to computational techniques: veri-
     fier theory and unverifiability. Physica Scripta, 92(9), 093001.

[38] Yudkowsky, E., & Herreshoff, M. (2013). Tiling agents for self-modifying AI, and the Löbian
     obstacle. Technical report, Machine Intelligence Research Institute.

[39] Zenil, H. (2026). On the limits of self-improving in large language models: the singularity
     is not near without symbolic model synthesis. arXiv preprint arXiv:2601.05280.

[40] Zhang, J., Hu, S., Lu, C., Lange, R., & Clune, J. (2025). Darwin Gödel Machine: open-
     ended evolution of self-improving agents. arXiv preprint arXiv:2505.22954; ICLR 2026.


Appendix A: Proofs of Classical Results Used in Part I
For self-containedness, this appendix reproduces the standard proofs of Rice’s Theorem and
Gödel’s Incompleteness Theorem in the form used in Sections 3 and 4. Both results are classical
and included here for completeness rather than as original contributions of this article.

A.1 Proof of Theorem 1 (Rice, 1953)
Proof. Many-one reduction from the Halting Problem. Let HP = {⟨x, w⟩ | Mx halts on input w}
denote the Halting Problem, known to be undecidable (Turing, 1936). We reduce HP to IP .
   Since P is non-trivial, fix q ∈ P and note that the nowhere-defined function f∅ satisfies
   / P (if instead f∅ ∈ P , one exchanges the roles of q and f∅ below). Given any pair ⟨x, w⟩,
f∅ ∈
construct the machine M ′ that, on input y: (1) simulates Mx on w; (2) if and when that
simulation halts, computes and returns q(y). By construction, φM ′ = q if Mx halts on w, and
φM ′ = f∅ otherwise. Hence M ′ ∈ IP ⇐⇒ ⟨x, w⟩ ∈ HP. A decision procedure for IP would
therefore decide HP; since HP is undecidable, no such procedure exists.

A.2 Proof of Theorem 2 (Gödel Incompleteness, 1931)
Proof. (Diagonalisation Lemma.) Since F contains P A, it can represent its own provability
relation: there exists a formula ProvF (x) that holds, within F , iff x is the Gödel number of a
provable sentence. By diagonalisation, there exists a sentence G with F ⊢ G ↔ ¬ProvF (⟨G⟩)
— G asserts its own unprovability.


                                              29
   If F ⊢ G, then G has a proof, so F ⊢ ProvF (⟨G⟩) (provability is representable: F proves
that it proves what it proves), while by the biconditional F ⊢ ¬ProvF (⟨G⟩), contradicting
consistency; hence F ⊬ G. If F ⊢ ¬G, then F ⊢ ProvF (⟨G⟩) by the biconditional, asserting G
has a proof — which, under ω-consistency yields a contradiction; hence F ⊬ ¬G. Neither G
nor ¬G is provable in F : F is incomplete. (For the statement under mere consistency, as in
Theorem 2, one uses Rosser’s sentence in place of G; the argument is standard and we do not
repeat it.)




                                            30
