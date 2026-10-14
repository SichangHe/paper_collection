                                          Why Code, Why Now: An Information-Theoretic Perspective on
                                                       the Limits of Machine Learning
                                                                                  Zhimin Zhao
                                                                  Software Analysis and Intelligence Lab (SAIL)
                                                                    School of Computing, Queen’s University
                                                                              z.zhao@queensu.ca
arXiv:2602.13934v4 [cs.LG] 12 Apr 2026




                                                                                         Abstract
                                                  This paper offers a new perspective on the limits of machine learning: the ceiling on progress
                                              is set not by model size or algorithm choice but by the information structure of the task itself.
                                              Code generation has progressed more reliably than reinforcement learning, largely because
                                              code provides dense, local, verifiable feedback at every token, whereas most reinforcement
                                              learning problems do not. This difference in feedback quality is not binary but graded. We
                                              propose a five-level hierarchy of learnability based on information structure and argue that
                                              diagnosing a task’s position in this hierarchy is more predictive of scaling outcomes than any
                                              property of the model. The hierarchy rests on a formal distinction among three properties
                                              of computational problems (expressibility, computability, and learnability). We establish their
                                              pairwise relationships, including where implications hold and where they fail, and present a
                                              unified template that makes the structural differences explicit. The analysis suggests why
                                              supervised learning on code scales predictably while reinforcement learning does not, and why
                                              the common assumption that scaling alone will solve remaining ML challenges warrants scrutiny.


                                         1    Introduction
                                         Code is discrete, symbolic, and syntactically unforgiving: a single misplaced character can render an
                                         entire program useless, and long-range dependencies span hundreds of lines. Moreover, correctness
                                         standards are absolute: a program either compiles or it does not. By every intuition about what
                                         should be easy for machines, code generation should therefore be among the hardest tasks in artificial
                                         intelligence.
                                             Instead, it is where ML has made its most consistent progress. Large models trained with
                                         prediction objectives now write nontrivial programs, refactor codebases, and solve algorithmic
                                         problems previously out of reach [7]. Meanwhile, reinforcement learning (RL), despite being
                                         interactive, closed-loop, and adaptive by design, has produced striking successes in closed domains
                                         such as board games [37] and robotic control. Recent RL-trained reasoning models [13] have
                                         also achieved impressive results on code and mathematics, though invariably by building on
                                         supervised pretrained models and coupling RL with structured verification (Section 5). Yet RL
                                         alone consistently struggles to accumulate transferable competence across tasks, even with massive
                                         interaction budgets.
                                             The familiar explanations for this disparity do not withstand scrutiny. “RL needs more
                                         compute” [21] does not explain why the pattern persists across orders of magnitude in scale, and
                                         “the reward signal is too sparse” [39] does not explain why sparse feedback works for some tasks and
                                         not others. More broadly, the pattern survives improvements in hardware, optimizers, simulators,


                                                                                              1
and representation learning. This persistence suggests that the primary obstacle is structural rather
than architectural.
    A widespread misconception has taken hold: that end-to-end neural networks with cutting-edge
hardware and Internet-scale data will eventually solve any problem. The successes in code
generation [7], Go [37], protein structure prediction [19], and image synthesis are taken as evidence
that scaling suffices [21]. But each of these domains shares specific preconditions, objective
evaluation functions, bounded solution spaces, massive structured datasets, and dense feedback
signals, that align with what gradient descent and pattern matching can exploit. The domains that
remain unsolved, by contrast, resist scaling because their information structure does not support
learning.
    This paper examines the problems themselves rather than the models, asking what makes a task
learnable at scale: not merely computable, expressible, or solvable in principle, but learnable by
large models under realistic data and interaction regimes in a way that improves smoothly rather
than collapses unpredictably.
    We make three contributions:

    1. We propose a five-level hierarchy of learnability based on information structure, ranging from
       complete unobservability (Level 0) to deterministic verification (Level 4), and show how it
       diagnoses when scaling will and will not help.

    2. We distinguish three properties of computational problems (expressibility, computability, and
       learnability), establish their pairwise relationships, and present a unified formal template that
       makes the structural differences explicit.

    3. We analyze why supervised learning on code scales predictably while reinforcement learning
       does not, grounding the explanation in information structure rather than algorithmic or
       architectural differences.


2     Related Work
Language identification and generation in the limit. Gold [17] establishes the framework
for language identification in the limit, proving that superfinite classes cannot be identified from
positive data alone. Angluin [2] extends this line of work by characterizing identifiable classes
through the notion of “tell-tale” finite sets. Kleinberg and Mullainathan [24] relax identification
to generation, asking only whether a learner can eventually produce novel valid strings rather
than converge on a grammar. They show that generation in the limit succeeds for strictly larger
classes than identification. Charikar and Pabbaraju [6] and, independently, Li et al. [25] prove
that every countable language collection admits non-uniform generation in the limit; the latter
work also introduces the uniform/non-uniform distinction. Kalavasis et al. [20] and Charikar and
Pabbaraju [6] concurrently formalize an inherent validity–breadth tradeoff (hallucination versus
mode collapse); Kalavasis et al. [20] additionally study a stochastic generation model. Subsequent
work [3] demonstrates computational feasibility barriers even for simple language classes, connecting
generation complexity to classical computability theory.

PAC learning and VC theory. Compared with language identification in the limit, a weaker
formal model of learnability is Probably Approximately Correct (PAC) learning. Valiant [43]
introduces the PAC framework, which formalizes learnability through sample complexity bounds.
Blumer et al. [5] connect PAC learnability to the Vapnik–Chervonenkis (VC) dimension, establishing


                                                   2
that finite VC dimension is both necessary and sufficient for PAC learnability under any distribution.
Shalev-Shwartz et al. [36] unify learnability, stability, and uniform convergence, showing their
equivalence for binary classification.

Computability and undecidability. Turing [41] establishes the existence of problems no
algorithm can solve, with the halting problem as the canonical example. The relationship between
computability and learnability is not one of simple containment: computable functions can be
unlearnable (e.g., cryptographic functions), and certain generation tasks succeed on classes that
include non-recursive languages [24].

Scaling laws and reinforcement learning. Chu et al. [8] show that supervised fine-tuning
memorizes the training distribution while RL can generalize beyond it, but only with supervised
scaffolding. Zhang et al. [48] demonstrate that stronger supervised checkpoints can underperform
weaker ones after RL, due to distribution divergence. Cui et al. [10] identify policy entropy
exhaustion as a fundamental bottleneck in RL for language models. Independently, Rohatgi and
Foster [33] propose a computational taxonomy for RL organized by which supervised learning oracles
are necessary and sufficient, identifying minimal oracles for Block MDPs and cryptographic hardness
barriers for Low-Rank MDPs. These findings support our thesis that the obstacle is in the problem’s
information structure, not in model capacity. At the same time, recent RL-trained reasoning
models [13] achieve strong code and mathematics performance, and process reward models [27]
recover step-level feedback that outcome-based RL discards. We analyze why these hybrid successes
are consistent with, rather than counter to, our information-structure thesis in Section 5.

Structural information and computational observers. Jiang et al. [18] decompose the
information in a dataset into two components relative to a computationally bounded observer:
epiplexity (structural information extractable into model weights) and time-bounded entropy
(residual unpredictability). They prove that cryptographically secure pseudorandom generators
have nearly maximal time-bounded entropy but negligible epiplexity, formalizing the intuition that
computable functions can be unlearnable from observation alone. Empirical measurements show
that language data carries far more structural information than image data at comparable compute
budgets, and that the same data under different factorizations yields different amounts of learnable
structure. These results provide formal backing for the information-structure perspective developed
in the present paper.

Goodhart’s law and reward misspecification. Manheim and Garrabrant [29] categorize
variants of Goodhart’s law. Recent work [14] formalizes distributional Goodhart effects, and
geometric analysis of MDPs [22] shows that Goodhart failure is the default outcome of unconstrained
proxy optimization.


3    What Makes Code Special
Code exposes information to learning algorithms in a way that few other domains match. The
properties below are not unique to code: natural language has grammar, images have spatial
structure, and mathematics has logical constraints. However, code is distinguished by the degree to
which all three properties co-occur and the strength of the verification infrastructure that enforces
them. These properties create a rich, dense, and structurally aligned feedback signal that supervised
learning can exploit, while the absence of any one of them creates a gap that RL struggles to bridge.

                                                  3
3.1   Hard Syntactic Constraints
For conventional statically parsed languages, a deterministic procedure decides in polynomial
time whether any string is syntactically valid, yielding a binary answer: valid or invalid [1]. A
natural language sentence with a dangling modifier still communicates, whereas a program with a
mismatched brace or an undeclared variable does not compile in statically checked languages, and
even in dynamically typed languages, syntactic violations produce immediate, unambiguous errors.
For a learning system, this distinction matters: every training example of valid code carries a precise
signal about the rules of the language, and every violation stands out sharply.

3.2   Locally Identifiable Errors
Code is not only globally checkable but also locally structured in ways that correspond to verifiable
constraints. Type consistency, scope rules, interface matching, and dimensional invariants catch
errors without examining the entire program. For instance, a type error points to a particular line
and a particular mismatch, and a missing variable declaration points to the exact scope. These
localized diagnostics give learning systems dense, targeted error signals. By contrast, errors in
natural language meaning are diffuse, because no analogous mechanism pinpoints where a sentence
goes wrong.

3.3   Strong Compositionality
The meaning of a program built from two components depends primarily on the meanings of those
components, not on the global context. A pure sorting function produces the same output regardless
of whether it appears inside a web server or a data pipeline, provided it has no side effects or shared
state. Common idioms, function signatures, and algorithmic templates recur across projects. As a
result, patterns learned from one codebase remain useful in another.

3.4   Why Supervised Learning Outperforms Reinforcement Learning on Code
Together, these three properties mean that each training example is rich in localized, verifiable,
reusable signals. When a model trains on millions of existing programs, each program serves as
a positive example of the language, a collection of reusable local structures, and an implicit vote
on the constraints that govern valid code. The resulting signal is high-dimensional, dense, and
structurally aligned with the task.
    These same properties also suppress shortcut learning: the tendency of gradient descent to
latch onto spurious correlations that hold in training data but fail under distribution shift [16]. In
natural-image classification, a model can achieve high accuracy by relying on background texture
rather than object shape, because no hard constraint forces it to attend to the causal feature. Code
is different: a spurious surface correlation cannot substitute for syntactic and type correctness.
The compiler enforces causal features, correct syntax, matching types, proper scoping, and rejects
outputs that rely on surface statistics alone. This makes the gap between “features that correlate
with validity” and “features that cause validity” unusually narrow in code, which is precisely the
condition a learner needs.
    A common intuition holds that code generation should be ideal for RL, since code has a natural
reward signal (pass or fail). In practice, the binary pass/fail reward is low-dimensional (a single
bit), easily gamed through hard-coding, and structurally uninformative: it says the program failed
but not where or why. In its default form, the binary reward acts as a filter that accepts or rejects
completed outputs rather than as a teacher that guides the model toward correct intermediate


                                                  4
steps. Shaped rewards and auxiliary signals can narrow this gap, but they require domain-specific
engineering that reintroduces the very structure supervised learning gets for free. In supervised
training, the model sees the correct answer at every step, whereas in RL it sees only whether the
completed program passes. The resulting difference in information density between a single pass/fail
bit and full token-level supervision remains substantial.

3.5     Formal Grounding
These properties align with a formal framework developed by Gold [17] and extended by Kleinberg
and Mullainathan [24]. A learner that observes only valid strings from an unknown language can
eventually generate new valid strings, even when it cannot identify which language it is observing.
We formalize this distinction in Section 4 and show how it grounds code generation’s tractability.


4     A Hierarchy of Learnability
When a learning system fails, we typically ask: is the model too small? The optimizer too weak?
The data too scarce? These questions assume the problem is solvable and that the bottleneck is
engineering. But learning problems can fail for entirely different reasons, and conflating them leads
to wasted resources and misplaced optimism.
     The critical concept is information structure, defined as the mechanism by which the world
exposes distinguishing information to a learner. It determines whether that information exists at
all, when it appears, and whether it can be verified. Information structure constrains learning more
fundamentally than model size, algorithm choice, or computational budget, because no amount of
any of the latter can overcome the absence of the former. Jiang et al. [18] formalize a related intuition
by decomposing dataset information into structural information (learnable patterns extractable into
model weights) and time-bounded entropy (residual unpredictability) relative to a computationally
bounded observer. Two datasets with identical total information can differ in how much structure a
bounded learner can extract, and it is the structural component that determines what is learnable.
     With this concept, we distinguish five levels of learnability, ordered by the quality of feedback
available to the learner, from no signal at all to immediate deterministic verification (Table 1).
These levels are not sharp boundaries. Just as phase transitions in combinatorial problems (such as
the SAT solvability threshold near clause density α ≈ 4.26 [47]) turn a binary classification into a
probabilistic landscape, a real-world task often sits in a gradient between adjacent levels, and small
changes in problem structure can shift it from one regime to another.
     The hierarchy rests on three formal properties of computational problems, expressibility,
computability, and learnability, that characterize different aspects of what machines can and cannot
do, and confusing them leads to misdiagnoses of difficulty. We define the first two properties as
building blocks, then integrate the formal definitions of learnability into the hierarchy levels where
they apply.

4.1     Formal Foundations
4.1.1    Standing Assumptions
All definitions share the following setup.

    • Instance space. Let X be a countable set. When X = Σ∗ for a finite alphabet Σ,
      computability is defined in the standard Turing sense. When X is a countable subset of
      Rd , all computational definitions are understood relative to a fixed computable encoding

                                                   5
Table 1: Hierarchy of feedback quality across five learning settings, from fully unobservable to
deterministically verifiable.
Level    Feedback       What happens                                Scaling         Example
         quality                                                    outcome
  0      None           Unobservability: different hypotheses       Impossible      The halting problem,
                        produce identical observations.   No                        fully     Goodharted
                        data helps.                                                 metrics
  1      Adversarial    Adversariality    and     reflexivity:      Unstable        Gaming      a   ranking
                        distinguishing  information     exists                      algorithm, adversarial
                        but the target shifts in response to                        online learning
                        learning.
  2      Noisy          Stochasticity:       hypotheses      are    Data-dependent Image    classification,
                        statistically  distinguishable,      but                   spam detection
                        each observation is noisy.
  3      Indirect       One-sided evidence: wrong hypotheses        Convergent      Formal         language
                        are eventually falsified, but correctness   but             learning,       program
                        is never confirmed.                         unconfirmed     testing
  4      Direct         Every output can be immediately and         Predictable     Type            checking,
                        deterministically verified.                                 compilation,       formal
                                                                                    proof verification


        enc : X → {0, 1}∗ . Computability over richer domains (e.g., all of Rd ) requires an effective
        representation in the sense of Type-2 computability [46], which we do not pursue here.
      • Target language. A language is a set L ⊆ X. Its indicator function is χL : X → {0, 1}, with
        χL (x) = 1 iff x ∈ L.
      • Function classes. A function class F ⊆ {f : X → {0, 1}} is a collection of total,
        binary-valued functions on X. Since outputs lie in {0, 1}, all functions are bounded.
        Measurability with respect to any distribution on X holds automatically for the discrete
        σ-algebra.
      • Concept class. A concept class C is a collection of languages. We write L ∈ C to denote
        membership.

4.1.2     Expressibility
Definition 1 (Expressibility). A language L is expressible within a function class F ⊆ {f : X →
{0, 1}} if
                               ∃ f ∈ F ∀ x ∈ X f (x) = χL (x).                               (1)
Equivalently, the risk functional
                                    Rexpr (f, L) = sup f (x) − χL (x)                                    (2)
                                                     x∈X

satisfies Rexpr (f, L) = 0 for some f ∈ F .
    Expressibility asks only whether a correct classifier exists in F. In particular, it imposes no
requirement that the classifier be computable or discoverable from data. The quantifier structure
is minimal: ∃f ∀x.

                                                      6
Remark 1 (Expressibility is relative). Expressibility is always relative to a restricted function
class F. The unrestricted class {f : X → {0, 1}} trivially contains a correct classifier for every
language, including undecidable ones. Without restriction on F , expressibility is vacuous. The
notion becomes informative only when F is constrained: linear classifiers express half-spaces,
deterministic finite automata express regular languages, and neural networks of bounded depth
express specific decision regions.

Remark 2 (Well-definedness of the supremum). Since f and χL both map into {0, 1}, the difference
|f (x) − χL (x)| takes values in {0, 1}, and the supremum in (2) is well-defined without additional
measurability or boundedness conditions.

Remark 3 (Risk as zero–one uniform loss). For binary-valued functions, Rexpr (f, L) ∈ {0, 1} and
the condition Rexpr = 0 reduces to pointwise equality f = χL . The risk formulation adds no analytical
power beyond existential equality in the binary case. We retain it because it instantiates the unified
template of Section 4.9, where the same schema accommodates distributional and sequential risk
functionals that do not reduce to exact equality.

4.1.3   Computability
Definition 2 (Computability). A language L is computable (decidable) if there exists a total
Turing machine M (one that halts on every input) such that

                                                                                         (3)
                                                    
                               ∀ x ∈ X, M enc(x) = χL (x).

Equivalently, within the class Mtotal of total Turing machines, the risk functional

                                                                                                  (4)
                                                            
                             Rcomp (M, L) = sup M enc(x) − χL (x)
                                              x∈X

satisfies Rcomp (M, L) = 0 for some M ∈ Mtotal .

Remark 4 (Totality is essential). The risk Rcomp is well-defined only for total machines. If M
does not halt on some input x0 , then M (enc(x0 )) is undefined and Rcomp cannot be evaluated. The
equivalence “L is computable iff Rcomp (M, L) = 0 for some M ” holds precisely within Mtotal .

    Computability asks whether a correct, terminating algorithm exists. The quantifier structure
matches expressibility (∃M ∀x) but restricts the mechanism class from arbitrary mathematical
functions to effective procedures. Expressibility quantifies over functions that may exist only
as abstract mathematical objects, whereas computability quantifies over procedures that can be
executed step by step.
    A weaker notion, recursive enumerability (r.e. or semi-decidability), relaxes totality: M must
halt and accept on inputs in L but may run forever on inputs outside L. This asymmetry reappears
in Level 3, where wrong hypotheses are eventually falsified but correctness is never confirmed.
    The computable languages are strictly contained in the expressible ones (Computable ⊊
Expressible). Every total Turing machine is a member of {f : X → {0, 1}}, so every computable
language is expressible. The halting language H = {⟨P ⟩ : P halts on empty input} witnesses strict
containment: χH exists as a mathematical function, but no total Turing machine computes it [41].
   With these formal building blocks in place, we now describe each level of the hierarchy. Levels 0
and 1 are characterized by information-theoretic and strategic obstacles that prevent convergence.
Levels 2 and 3 correspond to PAC learnability and generation in the limit, respectively. Level 4 is
characterized by deterministic verification.

                                                   7
4.2   Level 0: No Feedback
No interaction protocol of any kind can distinguish competing hypotheses. The obstacle is
information-theoretic indistinguishability: different hypotheses produce identical observations under
every possible interaction, regardless of the protocol. The halting problem is a canonical case, but
unobservability also arises when every available proxy is many-to-one with respect to the true
objective. In a completely Goodharted system [29], every metric the learner observes is compatible
with both genuine improvement and strategic gaming. Recent formalization [14] shows that the tail
distribution of proxy–objective discrepancies determines whether proxy over-optimization becomes
merely useless or actively harmful. Heavy-tailed misalignment makes strong Goodhart degradation
not just possible but probable.

4.3   Level 1: Adversarial Feedback
Separating information exists and a sufficiently adaptive protocol could in principle extract it, but
the environment actively prevents convergence. The obstacles are adversariality and reflexivity:
the environment works against the learner, or the target shifts in response to learning. Specifically,
an adversarial environment can delay counterexamples or adapt to the learner’s strategy, while
reflexivity creates a related pathology in which the learner chases an object that moves because
it is being chased. Platform ecosystems where participants game the ranking algorithm are a
reflexive example [30]: the “correct” ranking changes precisely because the algorithm is deployed.
Formally, a Level 1 task is one where the data-generating distribution at step t + 1 depends on
the learner’s current hypothesis: Dt+1 = E(ht ), where E is an environment response function. This
non-stationarity means convergence guarantees from the PAC framework (which assumes a fixed D)
do not apply, even when the hypothesis class has finite VC dimension. PAC convergence relies on
the uniform law of large numbers over i.i.d. samples [5]. When Dt+1 = E(ht ), consecutive samples
come from different distributions, so the empirical risk R̂m (h) no longer estimates R(h, L, D) for any
single D. Learning under non-stationarity requires additional structural assumptions (e.g., bounded
drift or mixing conditions [4]) that are absent in the reflexive setting.

4.4   Level 2: Noisy Feedback
The obstacle is stochasticity: different hypotheses are statistically distinguishable, and the learner
can converge in a probabilistic sense, but individual observations are noisy. The PAC framework [43]
formalizes this level.
Definition 3 (PAC learnability). A concept class C over X is PAC-learnable if there exists a
learning algorithm A and a hypothesis class H of measurable functions X → {0, 1} (with H ⊇ C, see
Remark 5) such that for every L ∈ C, every probability distribution D over X, and every ε, δ > 0,
there exists m = poly(1/ε, 1/δ) such that, given m i.i.d. samples S ∼ Dm , the algorithm outputs a
hypothesis h = A(S) ∈ H satisfying
                                    h                     i
                                 Prm RPAC (h, L, D) ≤ ε ≥ 1 − δ,                               (5)
                                S∼D

where the risk functional is

                                                                                                   (6)
                                                                
                               RPAC (h, L, D) = Pr h(x) ̸= χL (x) .
                                                  x∼D

Remark 5 (Realizable case). Definition 3 operates under the realizable assumption: the hypothesis
class contains a perfect classifier (H ⊇ C), so zero error is achievable in principle. The agnostic

                                                  8
setting drops this assumption and minimizes over H without guaranteeing zero risk. Agnostic
learnability is strictly harder and requires different sample complexity bounds [35]. We adopt the
realizable case throughout because our focus is on structural barriers to learnability, which are present
even under the most favorable assumptions.

Remark 6 (Improper learning). Definition 3 permits improper learning: the output hypothesis h
may lie in H ⊇ C rather than in C itself. Proper learning (requiring h ∈ C) is strictly stronger and
computationally harder for some concept classes [35].

Remark 7 (Sample complexity and VC dimension). The polynomial bound m = poly(1/ε, 1/δ) in
Definition 3 hides a critical structural parameter. The fundamental theorem of PAC learning [5, 36]
establishes that a concept class is PAC-learnable if and only if its VC dimension d = VC(H) is
finite, in which case the sample complexity is
                                                            
                                                d + log(1/δ)
                                        m=O                    .
                                                      ε
When d = ∞, no finite sample suffices for uniform convergence, and PAC learnability fails. The
VC dimension thus mediates the connection between expressibility and learnability formalized in
Section 5.

Remark 8 (Measurability). The probability in (6) requires that {x : h(x) ̸= χL (x)} be
D-measurable. Since h and χL are {0, 1}-valued, measurability holds whenever H consists of
measurable functions with respect to the σ-algebra on which D is defined, which we assume
throughout.

Remark 9 (PAC learnability implies computability of evaluation). PAC learnability requires that
A be a total computable procedure (one that halts on every input) and that each hypothesis h = A(S)
be evaluable on new inputs. Therefore, PAC learnability entails that hypotheses output by the learner
are computable procedures. Each such h approximates L to within ε error under the distribution D,
but need not decide L exactly. The converse fails: computable languages need not be PAC-learnable
(Section 4.10).

    Distinguishing a coin that lands heads 49% of the time from one at 51% requires thousands
of flips, but it is always possible, and most conventional machine learning operates at this level.
Stochasticity raises the price of learning but does not destroy learnability.

4.5   Level 3: Indirect Feedback
The obstacle is one-sidedness: the learner receives real information, but only from one side.
Positive evidence accumulates, but explicit correction never arrives. A wrong hypothesis is not
immediately flagged, but it cannot survive indefinitely: when contradicting evidence appears, it
provides unambiguous falsification. The central asymmetry is that correctness is never confirmed,
so the learner improves monotonically but can never know it has converged.
    The classical theory of language identification asks the stronger question: can the learner
eventually identify which language it is observing? Gold [17] shows this is impossible for most
language classes from positive examples alone. Without negative examples, the learner cannot
distinguish between two languages where one is a subset of the other.
    However, Kleinberg and Mullainathan [24] reframe the question. Instead of identification,
they ask whether the learner can generate valid new strings indefinitely. Generation succeeds for
strictly larger classes of languages than identification does, because generation requires only that the

                                                   9
learner stay within some infinite safe subset of the target language, whereas identification requires
characterizing the language’s complete boundary. In practice, a code generation model does not
need to recover the complete grammar of Python but only to keep producing valid programs, a task
with strictly weaker requirements.

Definition 4 (Generation in the      S limit).n Let C be a concept class of infinite languages. A generator
G : X <∞ → X, where X <∞ = ∞            n=1 X , succeeds on C if, for every L ∈ C and every enumeration
σ = (x1 , x2 , . . .) satisfying {xn : n ∈ N} = L, there exists N ∈ N such that for all n ≥ N :

                              G(x1 , . . . , xn ) ∈ L          (validity),                               (7)
                              G(x1 , . . . , xn ) ∈
                                                  / {x1 , . . . , xn }       (novelty).                  (8)

The risk functional captures validity only:

                               Rgen (G, L, σ) = lim sup 1 G(σ≤n ) ∈                                      (9)
                                                         
                                                                  /L .
                                                        n→∞

Success requires both Rgen = 0 (eventual perpetual validity) and eventual perpetual novelty.

Remark 10 (Infinite language requirement). The novelty condition (8) requires that L be infinite.
If L is finite, then after all elements of L have appeared in the enumeration, no novel valid output
exists. We restrict C to infinite languages throughout.

Remark 11 (Validity versus productivity). Rgen captures whether the generator eventually stays
within L (semantic convergence). Novelty is a separate structural constraint enforcing nontrivial
generativity (productivity). We separate the two because they fail for different reasons: a generator
may produce only valid outputs but repeat itself (validity without productivity), or produce novel
outputs that eventually leave L (productivity without validity). For completeness, one can define a
companion novelty risk:

                        Rnov (G, L, σ) = lim sup 1 G(σ≤n ) ∈ {x1 , . . . , xn } .                (10)
                                                   
                                                 n→∞

Full success then requires both Rgen = 0 and Rnov = 0. We retain Rgen alone in the unified
template (Table 4) because validity and novelty are structurally independent constraints with distinct
failure modes, and the template is designed to capture the risk of incorrect outputs rather than the
productivity of the mechanism.

Remark 12 (Strength of universal quantification over enumerations). Definition 4 quantifies over
every enumeration of L, including adversarially ordered ones. The generator receives no structural
guarantee about the order in which elements arrive. This corresponds to Gold-style learning
under arbitrary presentation [17], adapted to the generation setting by Kleinberg and Mullainathan
[24]. The requirement is correspondingly strong: the generator must succeed regardless of how the
environment sequences its data.

Remark 13 (Sequence semantics). The index n in Definition 4 is a sequence position in N, not a
physical time step. The generator operates on finite prefixes σ≤n = (x1 , . . . , xn ) of infinite sequences.
“In the limit” is a statement about convergence over sequence prefixes, not about the passage of
physical time.

Definition 5 (Identification in the limit). Let {Li }i∈N be an effective indexing of C: the membership
predicate x ∈ Li is uniformly decidable given i and x (i.e., there exists a total Turing machine that


                                                          10
on input (i, x) outputs χLi (x)). An identifier A succeeds on C if, for every L ∈ C and every
enumeration σ of L, there exists N such that for all n ≥ N ,

                                 A(x1 , . . . , xn ) = i   where   Li = L.                        (11)

The identifier must eventually lock onto the correct language index and never change.

    Identification is strictly stronger than generation: every concept class identifiable in the limit
is also generable, but the converse fails. An identifier that has converged to the correct index can
be converted into a generator by enumerating novel elements of the identified language. For the
separation, Gold [17] shows that superfinite classes (those containing all finite languages and at
least one infinite language) are not identifiable from positive data, yet Kleinberg and Mullainathan
[24] exhibit superfinite classes that are generable in the limit.

4.6   Level 4: Direct Feedback
At this level, no information-theoretic obstacle remains, because every output can be immediately
and deterministically judged correct or incorrect. Type checking, compilation, and formal theorem
verification [12] operate at this level. Level 4 exploits a deep asymmetry: verification is cheap while
search is hard. A type checker confirms correctness in linear time; finding a type-correct program
may require exploring an exponential space. This is the P versus NP gap working in the learner’s
favor: the learner inherits the easy side of the asymmetry. Level 4 does not imply greater intelligence
on the learner’s part but rather a stronger verification structure in the task.

4.7   Code Generation Across Levels
Code generation illustrates how a single task can draw on multiple levels. During training, the model
learns from a stream of valid programs without explicit negative examples, a Level 3 information
structure. But code’s verification infrastructure (compilers, type checkers, test suites) provides
Level 4 feedback that leaks into the learning process: training data is filtered by compilation,
reward signals come from test results, and error diagnostics point to specific failures. Unlike most ML
domains where training data is passively observed, code permits active experimentation: the learner
(or its training pipeline) can execute a candidate program and observe whether it passes, producing
feedback that is causally tied to the specific output rather than merely correlated with it. Most ML
training data provides only observational signal (P (Y | X)); code’s execution infrastructure provides
a form of experimental signal in which the outcome is deterministically linked to the input, which is
why its feedback is so much more informative. This combination (a Level 3 learning problem
scaffolded by Level 4 verification with interventional feedback) is what makes code generation
tractable. RL on code can access the same Level 4 verifiers, but it collapses the rich diagnostic
signal into a single scalar reward, losing the density and locality that make supervised learning
effective. Moreover, most learning tasks have no such scaffold.
    Code generation models do not “understand” their programming languages in any complete
sense. Indeed, they cannot reliably decide whether an arbitrary program is valid. Yet they stably
generate valid programs, drawing on patterns absorbed from training data. This behavior reflects
not a failure of understanding but a different, achievable kind of competence, determined by the
information structure of the task.
    The purpose of the hierarchy is diagnostic: when a learning problem fails, the first question
should not be “do we need a bigger model?” but “what kind of feedback does the learner actually
receive?” For example, a Level 0 problem cannot be solved by scaling, and a Level 1 problem cannot


                                                      11
Table 2: Quantifier alternation structure and depth for each property in the learnability hierarchy.
             Property                     Quantifier structure    Alternation depth
                 Expressibility                ∃f ∀x                   2
                 Computability                 ∃M ∀x (+ totality)      2 (+ constraint)
                 PAC learnability              ∃A ∀L ∀D ∀ε, δ ∃m       4
                 Generation in the limit       ∃G ∀L ∀σ ∃N ∀n ≥ N      5
                 Identification in the limit   ∃A ∀L ∀σ ∃N ∀n ≥ N      5


be solved by better optimizers. Recognizing the level is therefore the prerequisite for choosing the
right response.
    Crucially, the classification can be performed before scaling is attempted. Four observable
properties, checkable from task specifications alone, determine the level: (i) whether any interaction
protocol can distinguish competing hypotheses (if not, Level 0); (ii) whether the data distribution is
stationary or shifts in response to the learner (non-stationarity implies Level 1); (iii) whether both
confirming and disconfirming evidence are available (symmetric feedback indicates Level 2; one-sided
positive evidence indicates Level 3); (iv) whether every candidate output can be immediately and
deterministically verified (if so, Level 4). For instance, automated theorem proving in Lean 4 [12]
satisfies all four criteria for Level 4 before any model is trained: proof candidates are distinguishable,
the proof-checking rules are fixed, the type checker provides both acceptance and rejection, and
verification is deterministic. The hierarchy thus predicts that scaling should yield reliable progress
on theorem proving, a prediction consistent with recent empirical results.

4.8   Quantifier Depth
The quantifier structure deepens across definitions, and the depth reflects the adversarial robustness
required of the mechanism (Table 2).
    Each additional quantifier alternation represents an additional degree of adversarial choice the
mechanism must handle. At the shallowest level, expressibility must work for all instances but faces
no adversary choosing instances adaptively. PAC learnability, in turn, must work for all target
concepts, all distributions, and all accuracy requirements. At the deepest level, generation and
identification must work for all targets and all orderings of the data, including adversarial ones.
    The properties also differ in what counts as an adversary and how success is quantified (Table 3).
    Expressibility and computability share pointwise quantification with no adversary. PAC
learnability, by contrast, introduces a distributional adversary: success must hold for every


      Table 3: How success is measured and what adversary each property must withstand.
Property          Success quantification   Adversary                 Error model
Expressibility        ∀x (pointwise)              None                        Exact (zero–one)
Computability         ∀x (pointwise)              None                        Exact (zero–one)
PAC learnability      Prx∼D (distributional)      Distribution D              Probabilistic (ε, δ)
Generation            ∀σ (worst-case ordering)    Adversarial enumeration     Asymptotic (lim sup)
Identification        ∀σ (worst-case ordering)    Adversarial enumeration     Asymptotic (convergence)


                                                       12
Table 4: Unified template: each property as an instance of Equation (12), differing only in
mechanism class M and risk functional R.
Property         Mechanism class M      Risk functional R(Φ, L)      Quantifiers
Expressibility          F ⊆ {f : X → {0, 1}}    sup f (x) − χL (x)                ∃f ∀x
                                                x∈X

Computability           Mtotal (total TMs)      sup M (enc(x)) − χL (x)           ∃M ∀x
                                                x∈X

PAC learnability        Algorithms A → H        Prx∼D h(x) ̸= χL (x) , h = A(S)
                                                                   
                                                                                  ∃A ∀D ∀ε, δ ∃m

Generation              G : X <∞ → X            lim sup 1{G(σ≤n ) ∈
                                                                  / L}            ∃G ∀L ∀σ ∃N ∀n ≥ N
                                                 n→∞



distribution, but error is measured probabilistically under each fixed distribution. Generation and
identification face the strongest adversary of all: success must hold under every ordering of the data,
including worst-case orderings designed to delay convergence.

Remark 14 (Connection to the arithmetical hierarchy). The pattern of increasing quantifier
alternation depth mirrors the arithmetical hierarchy in computability theory. In that hierarchy,
Σ0n and Π0n sets are classified by the number of quantifier alternations in their defining formulas,
and each additional alternation yields a strictly larger class of sets [41]. The analogy is structural
rather than formal: our properties are not defined by arithmetical formulas over N, but the principle
that deeper quantifier alternation corresponds to strictly harder problems applies in both settings.

4.9   A Unified Template
All properties instantiate a single schema. Each asks whether there exists a mechanism Φ in a
mechanism class M such that a risk functional vanishes:

                                    ∃ Φ ∈ M such that R(Φ, L) = 0.                                 (12)

The properties differ in what M contains and what R measures (Table 4). In the PAC and
generation settings, the risk functional implicitly absorbs universal quantification over distributions
or enumerations, respectively, as specified in Table 2. The template captures the common
existential–risk structure while the full quantifier depth is recorded separately.
    The risk functionals differ along three axes (Table 5).
    Expressibility and computability share the same pointwise-supremum risk, differing only in the
mechanism class (computability restricts to total Turing machines). PAC learnability replaces the


Table 5: Risk functionals compared along three axes: domain of supremum, probabilistic
measurement, and sequential dependence.
             Risk type Supremum/limit taken over Probabilistic? Sequential?
                 Rexpr         Entire instance space X               No           No
                 Rcomp         Entire instance space X               No           No
                 RPAC          Distribution D                        Yes          No
                 Rgen          Sequence index n                      No           Yes


                                                       13
pointwise supremum with a distributional expectation, and generation replaces it with a sequence
limit (lim sup). The quantifier structure deepens accordingly. Expressibility requires only that
a correct function exist. Computability adds that the function must be implementable as a
halting program. Learnability adds that the algorithm must succeed across all targets, all data
presentations, and must eventually converge.

4.10    Pairwise Relationships
The three properties are not fully independent: PAC learnability implies computability of hypothesis
evaluation (Remark 9). However, no other implication holds, and no containment direction reverses.

Proposition 1 (Separations).

 (a) Expressible but not computable. The halting language H is expressible (χH exists as a
     mathematical function) but not computable [41].

 (b) Computable but not efficiently PAC-learnable. Under standard cryptographic hardness
     assumptions, the AES encryption function is computable in polynomial time given the key, but
     no polynomial-time algorithm can PAC-learn the input–output mapping from samples without
     the key. The learner observes only plaintext–ciphertext pairs for a fixed but unknown key and
     does not receive the key as part of the input. Here efficient PAC learnability requires polynomial
     time in both sample size m and instance dimension. In the information-theoretic sense
     (unbounded computation), the separation does not hold. Jiang et al. [18] make this separation
     precise: cryptographically secure pseudorandom generators have nearly maximal time-bounded
     entropy (they are indistinguishable from random to any polynomial-time observer) but negligible
     epiplexity (essentially no learnable structure exists to extract). Many computable functions
     (pseudorandom generators, cryptographic hashes) share this property.

 (c) Expressible but not PAC-learnable. Any hypothesis class F with infinite VC dimension [5]
     can shatter arbitrarily large finite sets: for any finite sample and any labeling of that sample,
     some f ∈ F is consistent with it. This prevents uniform convergence and destroys PAC
     learnability under distribution-free assumptions, where the learner must succeed for every
     distribution D. Finite data cannot eliminate the infinitely many functions that agree on all
     observed inputs yet diverge on unseen ones.

 (d) Generable but not identifiable. Kleinberg and Mullainathan [24] exhibit concept classes
     where generation in the limit succeeds but identification in the limit fails. Charikar and
     Pabbaraju [6] and, independently, Li et al. [25] prove that every countable language collection
     admits non-uniform generation; the validity–breadth tradeoff is also established concurrently
     by Kalavasis et al. [20].

 (e) PAC-learnable implies computable evaluation. If C is PAC-learnable by algorithm A,
     then for every L ∈ C, the hypothesis h = A(S) is a computable procedure that approximates
     membership in L (to within ε error under D). PAC learnability thus entails that the learner’s
     output hypotheses are computable, though they need not decide L exactly. The converse fails
     by (b).

   These relationships are summarized in Table 6.

Remark 15 (Qualified independence). The claim that these three properties are “logically
independent” requires qualification. PAC learnability implies computability of hypothesis evaluation,

                                                 14
        Table 6: Pairwise relationships among the five properties, with separating witnesses.
Pair                           Relationship                  Witness
Expr ̸⇒ Comp                   Comp ⊊ Expr                   χH exists but no TM computes it
Comp ̸⇒ Eff. PAC-Learn         Neither contains the other    AES (efficient PAC, cryptographic assumptions)
Expr ̸⇒ PAC-Learn              Independent                   Infinite-VC-dimension classes
PAC-Learn ⇒ Comp (eval)        One direction holds           Algorithm and hypothesis must be computable
Gen ̸⇒ Ident                   Ident ⊊ Gen                   Superfinite classes [24]


so the two are not fully independent. The precise statement is: expressibility does not imply
computability, computability does not imply learnability, and no containment direction reverses.
Note that PAC learnability presupposes expressibility within the hypothesis class H (the realizable
assumption H ⊇ C), so the two are not independent in the sense that learnability requires a
representational foundation. What fails is the reverse: expressibility in a rich class does not imply
learnability of that class.

    The distinction also separates verification from discovery. Verification is a static, closed-world
operation in which someone provides the answer and a checker confirms it. By contrast, discovery
is generative and open-world, requiring the answer to be found through observation and inference.
The ability to verify therefore does not imply the ability to discover, just as the ability to compute
does not imply the ability to learn.


5      Why Expressibility Hurts Learnability
Learnability differs from computability, but it differs even more sharply from expressibility. The
relationship is often inverse: increasing expressivity enlarges hypothesis complexity, which in turn
increases sample complexity and can destroy distribution-free learnability guarantees.

5.1    The Expressibility Trap
Lambda calculus [9] supports higher-order functions, self-reference, and can express any computable
process. This leads to a natural but wrong inference: if the system can represent everything, learning
should be easier, because the hypothesis space is guaranteed to contain the right answer.
    In fact, the opposite holds. Any hypothesis class with VC(H) = ∞ is not PAC-learnable under
distribution-free assumptions [5]. Over any infinite instance space X, the class of all computable
functions X → {0, 1} has infinite VC dimension (Lemma 1) and is therefore not PAC-learnable,
despite containing a correct classifier for every computable language.

Lemma 1 (VC dimension of computable functions). Over any infinite instance space X, the class
Fcomp = {f : X → {0, 1} | f is computable} has infinite VC dimension.

Proof. Let S = {x1 , . . . , xn } ⊆ X be any finite subset of size n. For each labeling b = (b1 , . . . , bn ) ∈
{0, 1}n , define fb (x) = bi if x = xi for some i, and fb (x) = 0 otherwise. Each fb is computable
(it is a finite lookup table with a default output). Since Fcomp shatters every finite subset of X,
VC(Fcomp ) ≥ n for all n, so VC(Fcomp ) = ∞.

   When the VC dimension is finite, a learner can narrow down the correct hypothesis with data
proportional to VC(H)/ε (Remark 7). However, the hypothesis class of all computable functions

                                                      15
has infinite VC dimension. In this regime, infinitely many functions agree on every observed input
but diverge on unseen ones: two programs may pass every test case yet produce completely different
outputs on the next input. The hypothesis space is simply too rich for finite evidence to constrain
it. This tradeoff appears in modern architectures: recent analysis of Transformers [11] shows that
increasing positional expressibility can require additional layers, raising sample complexity. In short,
richer representation requires more data to learn.
    Furthermore, self-reference exacerbates the problem. In standard learning theory, progress is
monotonic: once an observation rules out a candidate, that candidate stays ruled out. But when
the environment is reflexive (when the system being learned can react to the learner’s hypothesis),
the target itself shifts. This is not hypothesis mutation, the candidates are fixed functions. Rather,
the problem is that the environment’s future behavior depends on the learner’s current state, so a
hypothesis consistent with all past observations may become inconsistent with future ones generated
in response to it. Wang et al. [45] prove this formally: learning succeeds only when the family of
reachable models has a ceiling on its complexity. Remove that ceiling, and previously learnable
tasks become provably unlearnable. Turing completeness defines the upper bound of what a system
can express, but it does not define the lower bound of what a system can learn.

5.2   Why Models Succeed Despite Infinite VC Dimension
Models routinely succeed on tasks whose hypothesis spaces have infinite VC dimension. The
Universal Approximation Theorem guarantees that neural networks of sufficient width can
approximate any continuous function on a compact domain to arbitrary precision, and on finite
input domains, any function whatsoever can be fitted. The theoretical question is therefore never
whether a network can represent the answer, but whether it can learn the answer from available
data. Expressivity alone is not the bottleneck; learnability is the binding constraint.
    The resolution is that real-world data does not fill the full theoretical space. As the manifold
hypothesis [15] suggests, valid programs, natural images, and coherent text occupy a tiny, structured
submanifold within the space of all possible inputs. Empirical analysis of generative models [28]
confirms that model performance corresponds to the geometry of these low-dimensional data
manifolds. Training does not store individual examples; it compresses the manifold’s geometric
structure into the curvature of the parameter space. A ResNet-50 with 25 million parameters is
trained on millions of images, achieving a ratio of training examples to parameters that suggests
substantial compression of the data manifold’s structure into weights, not by memorizing pixels, but
by encoding the geometric regularities of the data distribution. When the intrinsic dimension is low,
the effective hypothesis space the learner must search is vastly smaller than the ambient dimension
suggests. The Minimum Description Length (MDL) principle [32] formalizes the connection:
the best hypothesis minimizes the total description length of model plus data given the model.
Code has unusually short description length because its syntax is restrictive and its semantics
are compositional, invalid code cannot even be parsed, let alone compressed efficiently. The
manifold of valid programs is not merely low-dimensional but also highly compressible, which is
the condition under which learning converges fastest. Not all manifolds are equally rich in learnable
structure. Empirical measurements of epiplexity across modalities [18] show that language data
carries far more structural information than image data at comparable compute budgets: over 99%
of image information consists of time-bounded entropy (unpredictable pixel values), whereas text
encodes proportionally more learnable structure. This asymmetry helps explain why pre-training
on text yields capabilities that transfer across domains, while pre-training on images does not.
Manifold structure does not make learning automatic, however. Theoretical work on neural network
hardness [23] shows that manifold structure with bounded curvature can still create computational


                                                  16
hardness. But for practical distributions, the constraints are usually met. Worst-case unlearnability
therefore does not imply practical unlearnability, because real data occupies only a small fraction
of the theoretical input space.
    This leads to a counterintuitive consequence: neural networks can learn to approximate the
behavior of uncomputable functions, not on all inputs (that remains provably impossible) but on
the structured submanifold that real-world instances occupy. The halting problem is undecidable
in the worst case, but the programs humans write are drawn from a distribution with strong
regularities: bounded loop depth, conventional control flow, and predictable recursion patterns.
On this manifold, termination is not just learnable but practically learnable with high accuracy.
In SV-COMP 2025 [40], automated tools decide termination for all 2,057 benchmark programs,
and Sultan et al. [38] show that large language models achieve comparable accuracy on the same
benchmarks. For many structured program distributions, termination can be verified by static
analysis, type systems, or syntactic restrictions [42]. The epiplexity framework [18] explains why
such approximation succeeds: a computationally bounded observer facing a system with simple
underlying rules may need to learn internal representations richer than the generating process
itself. The observer cannot brute-force the exact dynamics, so it discovers emergent regularities
and approximate invariants that the generating rules do not explicitly contain. The structural
information such a bounded observer extracts can exceed the description length of the generating
process, a phenomenon that Jiang et al. [18] formalize as “epiplexity emergence” and demonstrate
empirically with cellular automata. More broadly, just as computability does not imply learnability,
uncomputability does not imply unlearnability. “No correct algorithm exists for all inputs” is a
different claim from “no useful prediction is possible for typical inputs.” The theoretical worst case
lives in the complement of the manifold, not on it.
    The hard cases lie in the tail: rare events far from the training distribution’s center of mass, where
a code model handles common patterns well but struggles with unusual edge cases. Accordingly,
the learnability hierarchy is best understood as diagnosing practical difficulty on the manifold that
data actually occupies, not worst-case impossibility in the full theoretical space.

5.3   Why Reinforcement Learning Hits a Wall
Supervised learning exploits the data manifold because its feedback is dense and local: each example
directly constrains the model in a specific region. Recent work confirms this asymmetry. Chu et al.
[8] show that supervised fine-tuning memorizes the training distribution, succeeding in-distribution
but collapsing on novel variations. RL can generalize beyond the training manifold, but only when
it converges, and it requires supervised pretraining as scaffolding.
    RL’s difficulties originate in the structure of the feedback signal rather than in the richness of
the hypothesis space. The bottleneck is threefold.

Information misalignment. In supervised learning, the error signal is immediate, specific, and
tied to a single decision. In RL, the agent takes a sequence of actions and receives reward only
at the end, or sporadically. This reward indicates whether the outcome is good or bad but not
which action is responsible. This is the credit assignment problem [39], and in settings with delayed
reward, conditional branching, and partial observability, it can become computationally intractable.
Even upgrading the reward to a high-dimensional dense vector does not help when the reward and
the environment’s state changes are not temporally aligned. In other words, dimensionality cannot
compensate for causal misalignment.




                                                   17
Non-stationarity. In supervised learning, the data distribution is fixed. By contrast, in RL,
the agent’s own policy is part of the environment. As the policy changes, the state distribution
shifts, and past data no longer comes from the same distribution as future data. Consequently, the
standard convergence theorems break down. Zhang et al. [48] demonstrate that stronger supervised
checkpoints can significantly underperform weaker ones after RL. The cause is distribution
divergence: supervised training optimizes for one distribution, but RL encounters a different one.

Reflexive reward collapse. The target shifts precisely because the learner is pursuing it. Within
the learnability hierarchy, this dynamic places many RL tasks at Level 1. The problem has a
deeper structural root: the agent uses the same parameters to both generate actions and evaluate
their consequences, so it cannot genuinely verify its own reasoning. A related observation, termed
meta-layer fracture [26], suggests that when the same parameters generate both reasoning chains
and evaluate their conclusions, the model’s posterior tends to converge back toward its prior anchor
rather than toward the ground truth, because self-verification and action generation share the same
learned biases. When the reward no longer reflects the actual consequences of the agent’s actions,
or when the agent maximizes the reward without achieving the intended goal (Goodhart dynamics),
the feedback becomes indistinguishable from noise. At that point, the problem slides from Level 1
toward Level 0. Geometric analysis of reward misspecification in MDPs [22] confirms that Goodhart
failure in RL is not an edge case but the default outcome of unconstrained proxy optimization.
    These three obstacles are not bugs in specific algorithms. Rather, they are structural features
of the problems RL attempts to solve. When RL succeeds spectacularly, Go, Atari, robotic
manipulation, it is typically in domains where at least one obstacle is absent: the reward is
immediate and unambiguous, the environment is stationary, or the task admits a closed-form verifier.
These are precisely the conditions that push a task toward Levels 3 or 4 in the hierarchy. Outside
such domains, RL has not produced the smooth, predictable scaling that supervised learning on
code has achieved.

Reconciling RL-based reasoning successes. A natural objection is the striking recent success
of RL-trained reasoning models on code. Systems such as DeepSeek-R1 [13] and OpenAI’s
o-series models apply RL to improve code generation and mathematical reasoning, often surpassing
supervised-only baselines on competitive programming benchmarks. If code’s information structure
favors supervised learning, why does RL help?
    The resolution is that these systems do not use RL in isolation. Every successful RL-for-code
system begins with a strong supervised pretrained model that has already absorbed the dense, local,
compositional structure described in Section 3. RL then operates on top of this foundation, using
the very Level 4 verification infrastructure (compilers, test suites, type checkers) that makes code
special. Process reward models [27] further recover the step-level feedback that naïve outcome-based
RL discards, effectively re-engineering the dense signal that supervised learning gets for free. In
the language of the hierarchy, these systems succeed not because RL overcomes code’s information
structure but because they deliberately reconstruct Level 3–4 feedback within the RL loop.
    This observation strengthens rather than undermines the thesis. The pattern across all successful
RL-for-reasoning systems is the same: supervised pretraining provides the foundation, and RL
fine-tuning works only when coupled with structured verification. Chu et al. [8] confirm that RL
generalizes beyond the supervised distribution but requires supervised scaffolding to converge. When
the verification scaffold is removed or the reward signal is reduced to a single scalar, RL on code
degrades to the failure modes described above. The lesson is not that RL is unnecessary but
that RL succeeds on code precisely because code provides the feedback infrastructure that most


                                                 18
RL domains lack. More broadly, the dichotomy between supervised learning and reinforcement
learning is less informative than the dichotomy between tasks with and without verifiable feedback
structure. Hybrid pipelines (supervised pretraining followed by RL fine-tuning with process-level
verification) represent the field’s convergence toward this insight: use supervised learning to absorb
distributional structure, then use RL to explore beyond the training distribution, but only when a
reliable verifier constrains the exploration.


6     Discussion
6.1   The Unified Picture
Expressibility concerns what a system can represent, while computability asks whether a fully
specified problem can be solved by a halting algorithm. Learnability goes further still: can a system
approximate the truth under partial observability, sequential information, and finite resources? PAC
learnability implies computability of hypothesis evaluation (Remark 9), but computability does
not imply efficient learnability: cryptographic functions are computable yet not polynomial-time
PAC-learnable under standard hardness assumptions. Expressibility strictly contains computability
(Computable ⊊ Expressible), and neither implies learnability in general. The broad pattern
holds when the mechanism classes are ordered by their constraints: expressibility imposes none,
computability requires halting, and learnability requires convergence under adversarial data
presentations. What ultimately bounds a learning system is whether the task permits stable
learning, independent of the range of functions the system can express.
    This analysis suggests a reframing of how AI relates to classical computation theory. The
classical view positions AI within computability: AI ⊂ algorithms ⊂ computable functions. Modern
ML has quietly moved to a different containment: AI ⊂ statistical prediction. Statistical prediction
does not require the problem to be computable; it requires the data distribution to have extractable
structure for a computationally bounded observer [18]. This is why large language models write
poetry, generate legal analysis, and predict protein structures: the original problems resist formal
specification, but the proxies that ML optimizes (next-token likelihood, classification loss, energy
minimization) have stable distributional structure that gradient descent can exploit. It is also why
the same systems cannot prove mathematical theorems or guarantee program correctness: these
tasks demand logical certainty that no amount of distributional approximation can provide.
    The unified template from Section 4.9 makes the source of this hierarchy explicit. All three
properties ask ∃ Φ ∈ M such that R(Φ, L) = 0, but the quantifier structure deepens: expressibility
is ∃∀ (shallowest), computability is ∃∀ plus halting, PAC learnability is ∃∀∀∃ (four alternations), and
generation in the limit is ∃∀∀∃∀ (five alternations, deepest). Each additional quantifier alternation
represents an additional degree of adversarial robustness the mechanism must possess. This deeper
quantifier structure explains why learnability is harder than computability: the mechanism must
satisfy more levels of universality, not merely more computation.

6.2   Implications for Scaling
The ceiling of model capability is often far above the ceiling of task learnability. When a task is
unlearnable because of its information structure, larger models overfit faster, longer training fails
more consistently, and more complex objectives amplify intractability. Cui et al. [10] illustrate this
directly: RL performance in language models is bottlenecked by policy entropy exhaustion. The
model progressively commits to narrower outputs, losing the ability to explore alternatives, and this
collapse is one-directional. Indeed, additional compute only accelerates it.


                                                  19
    This does not mean algorithms, data, and compute no longer matter. Rather, the question is
where the returns go. When a task has favorable information structure, each increment compounds
reliably. Conversely, when the structure is hostile, the same investment yields diminishing returns.
The practical question for any ML investment is not “can we scale further?” but “does this task
yield a return on the next unit of compute?” The hierarchy makes this question empirically testable:
it predicts an ordering in which tasks at higher levels exhibit more predictable scaling than tasks
at lower levels, controlling for model architecture and data volume. A systematic violation of this
ordering would constitute disconfirming evidence for the framework.

6.3   Data Volume as a Confounder
A separate objection is that code generation succeeds simply because of data volume: trillions of
tokens of open-source code dwarf available interaction data for most RL tasks. But data volume
alone does not explain the pattern. Natural language has even more training data than code, yet
code generation has scaled more reliably for structured reasoning tasks. Conversely, RL agents in
board games and simulations have access to effectively unlimited self-play data, yet still face the
scaling obstacles described in Section 5. The epiplexity framework [18] formalizes why: the same
quantity of data yields different amounts of learnable structure depending on modality, and code’s
structural properties (verifiability, compositionality, syntactic constraints) are precisely what make
each token of code data more informative than a token of unstructured text or pixels. Data volume
and information structure are not independent: the reason so much high-quality code data exists is
that code’s structural properties make it easy to produce, filter, and verify at scale.

6.4   Paths Forward
Future breakthroughs will come not from building ever-larger models alone, but from understanding
which problems have learnable structures and from reshaping intractable problems into learnable
forms. Four strategies are available.

Task decomposition. An unlearnable task can sometimes be split into subtasks with stable,
attributable feedback. Code generation illustrates this: writing complete software is a monolithic
challenge, but predicting the next token is a sequence of local decisions [31], each benefiting from
the rich structural constraints of the programming language. The decomposition transforms the
information flow available to the learner without changing the ultimate goal.

Engineered feedback structures. Three design choices improve learnability: exposing
intermediate states so the learner can observe progress, providing feedback that is timely and
attributable to specific decisions, and ensuring that different failure modes are distinguishable.
A task where failure produces a single “wrong” signal is far less learnable than one where failure
produces a specific diagnostic, even when both tasks have the same ultimate objective. A fourth,
overarching principle is to place the verifier outside the learner: when the same parameters
generate both actions and evaluations, the system cannot escape its own biases (the meta-layer
fracture problem described above). Code naturally satisfies this condition: the compiler is an
independent external verifier that shares no parameters with the model. For domains that lack such
infrastructure, engineering an external verification loop, formal proof checkers, symbolic executors,
independent critic models, is the most direct route to moving a task from Level 1 or 2 toward
Level 4.



                                                 20
Weaker objectives. The stronger the learning objective, the more likely it is to be
unlearnable.    Global optimality, long-term consistency, and high-level abstraction impose
information requirements that realistic feedback channels cannot satisfy. Weak objectives (locally
correct, progressively approximate, verifiable at each step, discardable when wrong) support the
most reliable learning systems. Schapire [34] proves formally that learners barely better than
random can be composed into arbitrarily accurate ones. Accordingly, weak objectives are not a
compromise but a design principle. Progress therefore accumulates through many small, reliable
steps rather than through a single leap to the global optimum.

Proxy re-encoding. Every successful ML application involves a transformation that is rarely
made explicit: the original problem is re-encoded into a proxy that admits statistical optimization.
Poetry becomes next-token prediction, medical diagnosis becomes classification over feature vectors,
and recommendation becomes expected engagement maximization. The power of this re-encoding
is that it converts apparently non-mathematical problems into learnable ones. The danger is that
the proxy and the original problem can diverge silently: when they align, we get protein structure
prediction; when they diverge, we get recommendation systems that maximize engagement while
degrading well-being. Re-encoding matters more than classical information theory suggests. Jiang
et al. [18] prove that total information in a dataset is invariant to factorization under unbounded
computation, but for computationally bounded observers this symmetry breaks: the same data
under different factorizations yields different amounts of learnable structure. Chess models trained
to predict moves from board states extract more structural information and generalize better to novel
tasks than models trained in the reverse order, despite seeing identical data. Re-encoding therefore
changes what a bounded learner can extract, not merely how it is presented. The learnability
hierarchy applies not to the original problem but to the proxy, and the gap between proxy and
problem is itself not learnable from the proxy’s own feedback signal.


7    Conclusion
Code generation exemplifies all four strategies above: it is a formal language with clear syntactic
boundaries, locally verifiable semantics, and dense failure signals, and the proxy (next-token
prediction over valid programs) aligns tightly with the goal because code’s verification infrastructure
keeps the two in register. Nevertheless, code’s success does not prove that language models
reason in any general sense. A neural network that generates valid code is performing function
approximation: it models statistical regularities, not logical entailments. A model trained on
number-theoretic examples might learn to predict that Fermat’s equation has no integer solutions
for exponents greater than two with high accuracy, but it cannot prove Fermat’s Last Theorem.
Code generation succeeds precisely because generation does not require proof. The Curry–Howard
correspondence [44] offers an instructive analogy: in constructive type theories, well-typed programs
correspond to proofs and types to propositions, so generating a well-typed program is analogous to
proof search. Practical code generation in mainstream languages (Python, JavaScript, Java) does
not operate in a full constructive logic, but the analogy captures the essential division of labor: the
model searches for candidate programs using statistical pattern matching, while an independent
verifier (compiler, type checker, test suite) confirms correctness without needing to discover the
solution. This separation, statistical search for discovery, deterministic verification for correctness,
is what makes code generation tractable; domains that lack an independent verifier cannot exploit
this division. It proves only that code is a complex task whose structure happens to be learnable.
The breakthrough reflects a task whose information structure makes learning efficient, not primarily


                                                  21
an advance in model sophistication. The most persistent failures of artificial intelligence have not
primarily been failures of insufficient capacity but failures to recognize that the problem itself does
not admit learning under available feedback structures. Better models matter, but only when the
target task is learnable. The next breakthroughs belong to whoever identifies which remaining
problems are learnable: semi-formal reasoning with checkable steps, constraint-aware generation
within structured spaces, verifiable world models testable against data. Accordingly, the field that
asks “is this task learnable?” will make more reliable progress than the field that asks only “is this
model powerful enough?”


A     Notation
Table 7 collects the principal symbols used throughout the paper.


References
 [1] Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman. Compilers: Principles,
     Techniques, and Tools. Pearson, 2nd edition, 2006.

 [2] Dana Angluin. Inductive inference of formal languages from positive data. Information and
     Control, 45(2):117–135, 1980.

 [3] Marcelo Arenas, Pablo Barceló, Luis Cofré, and Alexander Kozachinskiy. Language generation:
     Complexity barriers and implications for learning. arXiv preprint arXiv:2511.05759, 2025.

 [4] Omar Besbes, Yonatan Gur, and Assaf Zeevi.             Non-stationary stochastic optimization.
     Operations Research, 63(5):1227–1244, 2015.

 [5] Anselm Blumer, Andrzej Ehrenfeucht, David Haussler, and Manfred K. Warmuth. Learnability
     and the Vapnik-Chervonenkis dimension. Journal of the ACM, 36(4):929–965, 1989.

 [6] Moses Charikar and Chirag Pabbaraju. On the non-uniform generation of countable language
     collections. arXiv preprint arXiv:2411.15364, 2024.

 [7] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto,
     Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul
     Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke
     Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad
     Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias
     Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
     William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra,
     Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer,
     Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech
     Zaremba. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374,
     2021.

 [8] Zhihan Chu et al. Supervised fine-tuning vs. reinforcement learning for generalization. arXiv
     preprint arXiv:2501.17161, 2025.



                                                  22
 [9] Alonzo Church. An unsolvable problem of elementary number theory. American Journal of
     Mathematics, 58(2):345–363, 1936.

[10] Ganqu Cui et al. Policy entropy exhaustion in language model reinforcement learning. arXiv
     preprint arXiv:2505.22617, 2025.

[11] Artur Back de Luca, George Giapitzakis, Shenghao Yang, Petar Veličković, and Kimon
     Fountoulakis. Positional attention: Expressivity and learnability of algorithmic computation.
     arXiv preprint arXiv:2410.01686, 2025.

[12] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In Proceedings of the 28th International Conference on Automated Deduction
     (CADE), pages 625–635, 2021.

[13] DeepSeek-AI. DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement
     learning. arXiv preprint arXiv:2501.12948, 2025.

[14] El-Mahdi El-Mhamdi and Lê-Nguyên Hoang. On Goodhart’s law, with an application to value
     alignment. arXiv preprint arXiv:2410.09638, 2024.

[15] Charles Fefferman, Sanjoy Mitter, and Hariharan Narayanan. Testing the manifold hypothesis.
     Journal of the American Mathematical Society, 29(4):983–1049, 2016.

[16] Robert Geirhos, Jörn-Henrik Jacobsen, Claudio Michaelis, Richard Zemel, Wieland Brendel,
     Matthias Bethge, and Felix A. Wichmann. Shortcut learning in deep neural networks. Nature
     Machine Intelligence, 2(11):665–673, 2020.

[17] E. Mark Gold. Language identification in the limit. Information and Control, 10(5):447–474,
     1967.

[18] Yiding Jiang, Soufiane Hayou, and Andrew Gordon Wilson. Epiplexity: Structural information
     extractable by a computationally bounded observer. arXiv preprint arXiv:2507.02598, 2025.

[19] John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf
     Ronneberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, Alex
     Bridgland, Clemens Meyer, Simon A. A. Kohl, Andrew J. Ballard, Andrew Cowie, Bernardino
     Romera-Paredes, Stanislav Nikolov, Rishub Jain, Jonas Adler, Trevor Back, Stig Petersen,
     David Reiman, Ellen Clancy, Michal Zielinski, Martin Steinegger, Michalina Pacholska, Tamas
     Berghammer, Sebastian Bodenstein, David Silver, Oriol Vinyals, Andrew W. Senior, Koray
     Kavukcuoglu, Pushmeet Kohli, and Demis Hassabis. Highly accurate protein structure
     prediction with AlphaFold. Nature, 596(7873):583–589, 2021.

[20] Alkis Kalavasis, Anay Mehrotra, and Nikolas Velegkas. On the limits of language generation:
     Trade-offs between hallucination and mode collapse. In Proceedings of the 57th Annual ACM
     Symposium on Theory of Computing (STOC), 2025.

[21] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child,
     Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language
     models. arXiv preprint arXiv:2001.08361, 2020.

[22] Jacek Karwowski, Oliver Hayman, Xingjian Bai, Klaus Kiendlhofer, Charlie Griffin, and Joar
     Skalse. Goodhart’s law in reinforcement learning. arXiv preprint arXiv:2310.09144, 2024.


                                               23
[23] Bobak T. Kiani, Jason Wang, and Melanie Weber. Hardness of learning neural networks under
     the manifold hypothesis. arXiv preprint arXiv:2406.01461, 2024.

[24] Jon Kleinberg and Sendhil Mullainathan. Language generation in the limit. arXiv preprint
     arXiv:2404.06757, 2024.

[25] Chinmay Li, Meghal Raman, and Ambuj Tewari. Generation through the lens of learning
     theory. In Proceedings of the 38th Annual Conference on Learning Theory (COLT), 2025.

[26] Zixi Li. Reasoning kingdom: Chapter 12 — implicit reasoning and the Yonglin formula, 2025.
     https://datawhalechina.github.io/reasoning-kingdom/chapter12.

[27] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee,
     Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. arXiv
     preprint arXiv:2305.20050, 2023.

[28] Gabriel Loaiza-Ganem, Brendan Leigh Ross, Rasa Hosseinzadeh, Anthony L. Caterini, and
     Jesse C. Cresswell. Deep generative models through the lens of the manifold hypothesis: A
     survey and new connections. arXiv preprint arXiv:2404.02954, 2024.

[29] David Manheim and Scott Garrabrant. Categorizing variants of Goodhart’s law. arXiv preprint
     arXiv:1803.04585, 2019.

[30] Juan Perdomo, Tijana Zrnic, Celestine Mendler-Dünner, and Moritz Hardt. Performative
     prediction. In Proceedings of the 37th International Conference on Machine Learning (ICML),
     pages 7599–7609, 2020.

[31] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever.
     Language models are unsupervised multitask learners. Technical report, OpenAI, 2019.

[32] Jorma Rissanen. Modeling by shortest data description. Automatica, 14(5):465–471, 1978.

[33] Dhruv Rohatgi and Dylan J. Foster. Necessary and sufficient oracles: Toward a computational
     taxonomy for reinforcement learning. arXiv preprint arXiv:2502.08632, 2025.

[34] Robert E. Schapire. The strength of weak learnability. Machine Learning, 5(2):197–227, 1990.

[35] Shai Shalev-Shwartz and Shai Ben-David. Understanding Machine Learning: From Theory to
     Algorithms. Cambridge University Press, 2014.

[36] Shai Shalev-Shwartz, Ohad Shamir, Nathan Srebro, and Karthik Sridharan. Learnability,
     stability, and uniform convergence. Journal of Machine Learning Research, 11:2635–2670, 2010.

[37] David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den
     Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot,
     Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy
     Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis.
     Mastering the game of Go with deep neural networks and tree search. Nature, 529(7587):
     484–489, 2016.

[38] Oren Sultan, Jordi Armengol-Estape, Pascal Kesseli, Julien Vanegue, Dafna Shahaf, Yossi
     Adi, and Peter O’Hearn. LLMs versus the halting problem: Revisiting program termination
     prediction. arXiv preprint arXiv:2601.18987, 2025.

                                               24
[39] Richard S. Sutton and Andrew G. Barto. Reinforcement Learning: An Introduction. MIT
     Press, 2nd edition, 2018.

[40] SV-COMP. Competition on software verification and witness validation: Results. 2025. https:
     //sv-comp.sosy-lab.org/2025/results/.

[41] Alan M. Turing. On computable numbers, with an application to the Entscheidungsproblem.
     Proceedings of the London Mathematical Society, s2-42(1):230–265, 1936.

[42] David A. Turner. Total functional programming. Journal of Universal Computer Science, 10
     (7):751–768, 2004.

[43] Leslie G. Valiant. A theory of the learnable. Communications of the ACM, 27(11):1134–1142,
     1984.

[44] Philip Wadler. Propositions as types. In Communications of the ACM, volume 58, pages 75–84,
     2015.

[45] Charles L. Wang, Keir Dorchen, and Peter Jin. On the statistical limits of self-improving
     agents. arXiv preprint arXiv:2510.04399, 2025.

[46] Klaus Weihrauch. Computable Analysis: An Introduction. Texts in Theoretical Computer
     Science. Springer, 2000.

[47] Ke Xu and Wei Li. Exact phase transitions in random constraint satisfaction problems. Journal
     of Artificial Intelligence Research, 12:93–103, 2000.

[48] Yao Zhang et al. Stronger supervised checkpoints underperform after reinforcement learning.
     arXiv preprint arXiv:2602.01058, 2026.




                                               25
                               Table 7: Summary of notation.
Symbol             Meaning
Spaces and sets
X                  Instance space (countable set)
Σ                  Finite alphabet
Σ∗                 Set of all finite strings over Σ
Rd                 d-dimensional real space
N                  Natural numbers
X <∞               All finite sequences over X, i.e. ∞      n
                                                    S
                                                      n=1 X

Languages and functions
L                  Target language (L ⊆ X)
χL                 Indicator function of L: χL (x) = 1 iff x ∈ L
H                  Halting language
⟨P ⟩               Encoding of program P
C                  Concept class (collection of languages)
{Li }i∈N           Effective indexing of a concept class
F                  Function class (⊆ {f : X → {0, 1}})
f                  A function in F
Fcomp              Class of all computable functions X → {0, 1}

Machines and algorithms
M                  Turing machine
Mtotal             Class of total (always halting) Turing machines
enc                Computable encoding X → {0, 1}∗
A                  Learning algorithm (PAC) or identifier (identification in the limit)
G                  Generator function (X <∞ → X)

PAC learning
D                  Probability distribution over X
H                  Hypothesis class
h                  Hypothesis output by the learner (h = A(S))
S                  Sample set (S ∼ Dm )
m                  Sample size
ε                  Error tolerance
δ                  Confidence parameter (failure probability bound)
d                  VC dimension, shorthand for VC(H)

Generation and identification in the limit
σ                  Enumeration of L, i.e. (x1 , x2 , . . .) with {xn } = L
σ≤n                Prefix (x1 , . . . , xn )
N                  Convergence index (generation/identification locks on after step N )
n                  Sequence position in N
i                  Language index in an effective indexing

Risk functionals
Rexpr (f, L)       Expressibility risk: supx∈X |f (x) − χL (x)|
Rcomp (M, L)       Computability risk: supx∈X |M (enc(x)) − χL (x)|
RPAC (h, L, D)     PAC risk: Prx∼D [h(x) ̸= χ26
                                              L (x)]
Rgen (G, L, σ)     Generation risk: lim supn→∞ 1{G(σ≤n ) ∈   / L}
Rnov (G, L, σ)     Novelty risk: lim supn→∞ 1{G(σ≤n ) ∈ {x1 , . . . , xn }}
ˆ
