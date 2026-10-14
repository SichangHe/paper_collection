                                               Position: Natural Language Should Not Fully Replace Formal Languages


                                                                             Eitan Wagner 1 2 Elisha Rosensweig 2 Omri Abend 1


                                                                    Abstract                                      the Stack Overflow 2025 survey,1 with increasingly positive
                                                                                                                  attitudes toward adoption (Eshraghian et al., 2025). Some
                                               Recent advances in large language models and
                                                                                                                  envision a future where natural language entirely replaces
                                               their widespread adoption have prompted claims
                                                                                                                  programming languages—a vision of “The new program-
                                               that natural language could entirely replace formal
                                                                                                                  ming language is called Human” (Jensen Huang; London
                                               languages, such as programming languages, for
                                                                                                                  Tech, June 2025).2 However, current systems face substan-
                                               software design. In this position paper, we argue
                                                                                                                  tial limitations: struggles with domain-specific code (Joel
                                               that this perspective overlooks fundamental lin-
                                                                                                                  et al., 2024), difficulties adapting to changing requirements
                                               guistic properties of natural language, specifically
                                                                                                                  (Jiang et al., 2024), and poor security (Dora et al., 2025). In
                                               that it is optimized for underspecification in open-
arXiv:2607.20432v1 [cs.CL] 10 May 2026




                                                                                                                  general, more developers report active distrust (46%) than
                                               ended contexts. We introduce a formal frame-
                                                                                                                  trust (33%) in the accuracy of AI tools.3 These challenges
                                               work centered on task specificity, defining it as the
                                                                                                                  raise questions about whether they represent temporary en-
                                               information-theoretic reduction of uncertainty—
                                                                                                                  gineering hurdles or fundamental limitations.
                                               in an output space, such as all possible images—
                                               given a user’s specific requirements. We prove                     Our Position. We argue that natural language and formal
                                               a specificity crossover theorem, showing the ex-                   languages (such as the code itself) serve complementary
                                               istence of a threshold beyond which the cost to                    information-theoretic roles, optimized for different points
                                               express formal requirements into natural language                  along what we call the ladder of specification—a hierarchy
                                               exceeds the cost of direct formal specification. By                we define building on previous research on communication
                                               analyzing case studies across modalities, such as                  efficiency and ambiguity in natural language (Gibson et al.,
                                               image generation, code synthesis, and audio pro-                   2019; Piantadosi et al., 2012). Natural language addresses
                                               duction, we demonstrate that natural language                      open-endedness—the challenge of communicating about
                                               excels at low specificity tasks, while formal lan-                 an unbounded world—through underspecification (Roberts,
                                               guages are advantageous on tasks with stricter                     2012), which includes pragmatic underspecification (where
                                               requirements. We conclude that natural and for-                    listeners infer the speaker’s intent from context) and in-
                                               mal languages are complementary tools and advo-                    different underspecification (where the speaker genuinely
                                               cate the development of hybrid systems that allow                  accepts multiple outcomes). Formal languages sacrifice this
                                               users to move across the specificity spectrum.                     flexibility for precise description within restricted domains,
                                                                                                                  operating at full specification where every relevant detail is
                                                                                                                  explicit. The cost of crossing between these modalities—the
                                         1. Introduction                                                          translation gap—means that neither approach dominates:
                                                                                                                  natural language wins at low task specificity through un-
                                         Large language models (LLMs) are transforming human-                     derspecification, while formal languages win at high task
                                         technology interaction, raising questions about the future               specificity by reducing the risk of errors and avoiding a
                                         of specialized expertise. As these models demonstrate in-                translation overhead. This complementarity suggests that re-
                                         creasing capabilities, concerns about professional skill dis-            search should focus not only on formal language generation
                                         placement intensify. Programming represents a particularly               capabilities but also on effective human-AI collaboration,
                                         salient case study: code is economically significant, operates           recognizing when each modality is advantageous.
                                         in well-defined formal domains, and benefits from abundant                 1
                                         training data (Jiang et al., 2024; Joel et al., 2024). AI for cod-           https://survey.stackoverflow.co/2025/ai#
                                                                                                                  sentiment-and-usage
                                         ing is massively adopted—84% reported using AI tools in                    2
                                                                                                                      https://youtu.be/SsNS3Xm9ig4?t=1940
                                                                                                                    3
                                           *
                                            Equal contribution 1 Department of Computer Science, Hebrew               https://survey.stackoverflow.co/2025/ai#
                                         University of Jerusalem 2 Dicta. Correspondence to: Eitan Wagner         developer-tools
                                         <eitan.wagner@mail.huji.ac.il>.

                                         Preprint. July 24, 2026.

                                                                                                              1
                                Natural Language Should Not Fully Replace Formal Languages

1.1. Key Contributions
                                                                        Many details are
                                                                                                             Indifferent
                                                                         not important                4
Building upon linguistic insights (§2), we provide an                                                     Underspecification

information-theoretic framework (§3) for modeling tasks as                “Draw a dog.”
                                                                                                                               Inferring implicit
constraint satisfaction with explicit and implicit constraints,                                                                  desires in the
                                                                                                             Pragmatic           natural world
while distinguishing types of underspecification along a con-                                     3       Underspecification
                                                                                                                                Assuming the dog
tinuum. We prove that for sufficiently specific tasks—and                                                                      is not upside down

                                                                        Exact description
a formal language without exceedingly high redundancy—                 of the requirements
natural language descriptions become less efficient than               “a radius 5cm circle
                                                                                                  2       Full Specification
                                                                        around the center
direct specification in the target modality. Our analysis val-                  ...”

idates trends reported in earlier work on many modalities,                                                                     Extra emphasis to
including images, code, audio, and text (§4).                                                                                   avoid mistakes
                                                                                              1           Overspecification    “A dog, only one,
As a consequence of our analysis (§5), we argue that de-                                                                          not two...”

velopment and evaluation of code generation from natural
language requires a hybrid approach. Consequently, the                Figure 1. The Ladder of Specification: from genuine indifference
practical value of end-to-end coding models and agents                (top) to overspecification (bottom), with corresponding compres-
                                                                      sion benefits and error risks.
should also be evaluated in terms of the actual benefit for a
workflow, with various hybrid models as baselines, and in
both low and high expertise domains.                                  Relaxing constraints over possible meaning is termed se-
                                                                      mantic underspecification. In semantics, multiple frame-
2. Communication Efficiency:                                          works attempt to represent the “shared” meaning of a sen-
   Open-Endedness and Underspecification                              tence through a single, compact meta-structure (Reyle, 1993;
                                                                      Copestake et al., 2005). From a cognitive perspective, this
In this section, we provide linguistic and information-               approach aligns with the observation that human listeners
theoretic background regarding underspecification. For the            frequently maintain an underspecified mental representation
purposes of this paper, we focus on one type of speech act            of ambiguous input, only committing to a specific inter-
(Searle, 1969): describing—directly or indirectly—a goal              pretation when prompted by pragmatic cues or discourse
to be implemented.                                                    requirements (Poesio, 1995; Frisson, 2009).
                                                                      We characterize this variation through the ladder of specifi-
2.1. Focusing Communication
                                                                      cation (see Fig. 1), a hierarchy reflecting different relation-
Natural language serves as humanity’s primary communica-              ships between what is said and what is meant:
tion tool, optimized for efficient information transfer across        Definition 2.1 (The Ladder of Specification). Communica-
diverse contexts (Zipf, 1949). A fundamental challenge is             tion achieves compression through a specification hierarchy:
open-endedness: natural language must handle the practi-
cally unbounded complexity of the real world through the                1. Overspecification: More information is provided than
ability to form novel utterances (Hockett & Hockett, 1960;                 strictly necessary, including redundancy or emphasis
Deacon, 1998). Because language users themselves con-                      (e.g., “a cat, not a dog”). While seemingly inefficient,
tribute to this complexity—creating new concepts, cultural                 redundancy can reduce error rates in noisy channels
practices, and communicative needs—the space of possible                   (Shannon, 1948). Even seemingly precise utterances
meanings is essentially unbounded (Tomasello, 2009).                       like “at 3 o’clock” allow some implicit flexibility;
The Question Under Discussion framework (QUD;                              adding “exactly” reduces the space of possible interpre-
Ginzburg et al., 1996; Roberts, 2012) addresses this chal-                 tations, disallowing approximations (Lasersohn, 1999).
lenge by viewing discourse as organized around implicit                 2. Full Specification: Every relevant detail for the current
questions that focus communication. The QUD determines                     domain is explicitly stated (e.g., code or exact RGB
what aspects of the world are relevant, licensing the omis-                values for colors). At this level, the description of the
sion of irrelevant details. This mechanism enables natural                 intent effectively coincides with its implementation.
language to address open-endedness: each speech act speci-                 Formal languages typically operate at this level within
fies only what matters for the current communicative goal.                 their domains (Meyer, 1993).

2.2. The Ladder of Specification                                        3. Pragmatic Underspecification: The meaning is ex-
                                                                           pected to be inferred from context, where the speaker
Within a given domain and QUD, utterances vary in how                      has intentions beyond what is literally expressed. This
precisely they constrain the space of acceptable meanings.                 level encompasses several distinct situations:

                                                                  2
                                    Natural Language Should Not Fully Replace Formal Languages

         • Clear intention: The speaker has a specific out-                   cation, where speakers implicate meanings beyond what
           come in mind but relies on shared knowledge for                    they literally say. Levinson (2000) provides a comprehen-
           disambiguation (e.g., “professional styling” as-                   sive treatment of how listeners infer pragmatic meaning.
           sumes standard design principles).                                 Carston (2008) argues that the actual meaning expressed is
         • Latent preferences: The speaker initially has no                   always much richer than the words used, with listeners fill-
           conscious preference but discovers, through in-                    ing in substantial implicit content. Clark (1996) emphasizes
           teraction and feedback, that they do care about                    the role of “common ground” in this inference process.
           certain properties. The speaker’s constraints of-                  The Rational Speech Acts (RSA) framework (Frank &
           ten emerge through iterative refinements of their                  Goodman, 2012; Goodman & Frank, 2016) models prag-
           expressed goals in a trial-and-error cycle.                        matic inference as bounded rational reasoning (Degen,
         • Delegation: The speaker does not explicitly for-                   2023), where speakers and listeners reason about likely
           mulate preferences for certain details, trusting                   interpretations given computational constraints. Attempts
           the listener to make good choices on their behalf                  to formalize listener inference include default reasoning
           (e.g., a manager saying “handle the deployment”                    in logic (Reiter, 1980; Mercer, 1987), although others ar-
           trusts the engineer’s judgment). Importantly, not                  gue that natural situations are too complex for formal logic
           all choices are acceptable; the speaker adopts the                 (Cadoli & Schaerf, 1993) and probabilistic methods better
           listener’s judgment.                                               describe the cognitive process (Oaksford & Chater, 2007).
  4. Indifferent Underspecification: True indifference to                     Pragmatic underspecification introduces miscommunication
     output properties, where multiple interpretations are                    risk. The probability of correctly inferring implicit con-
     equally acceptable to the speaker (e.g., “use any rea-                   straints depends on both the nature of the constraints and
     sonable color scheme”).                                                  the quality of shared context (Ferreira, 2008). Crucially, for
                                                                              successful pragmatic inference, the listener must understand
The key distinction between pragmatic underspecification                      the specific speaker’s context, knowledge, and preferences
and indifferent underspecification lies in whether the speaker                (Bergen & Grodner, 2012). This quality of personaliza-
has (possibly implicit) preferences about the underspecified                  tion forms an active research topic in dialogue systems
properties. In pragmatic underspecification, miscommuni-                      (Zadrozny et al., 2000; Oruche et al., 2025).
cation represents a failure; in indifferent underspecification,
variation is acceptable by design.                                            Communication Efficiency. A large body of research
Formal languages, such as programming languages, achieve                      addresses communication efficiency through the lens of in-
precision by operating primarily at the full specification                    formation theory (Futrell & Hahn, 2022), often through
level within their restricted domains.4 Importantly, formal                   rate-distortion theory, which provides a basis for lossy com-
languages sometimes exhibit hierarchical abstraction: the                     pression (Shannon et al., 1959). A general finding is that
command x = 1+2 specifies precisely what value is stored                      language optimally balances simplicity (shorter messages)
but not where in physical memory or how the processor                         and informativeness (Kemp & Regier, 2012; Zaslavsky et al.,
executes the addition. The formal language is deterministic                   2017; Marzen & DeDeo, 2017; Gibson et al., 2019). Krifka
and unambiguous at the outcome level, while delegating                        (2007) shows that speakers use imprecise language (such as
implementation details to lower system levels that have a                     approximate numbers) as a means of reducing effort when
negligible effect on the output.                                              precision is unnecessary. Piantadosi et al. (2012) demon-
                                                                              strate that ambiguity serves as a compression device when
2.3. Linguistic Perspectives                                                  context enables disambiguation.
                                                                              Underspecification in communication is fundamentally re-
The ladder of specification connects to several research
                                                                              lated to the notion of autonomy given to the listener. We
traditions in linguistics and cognitive science.
                                                                              expand on this in Appendix A.
Pragmatics and Inference. The study of how context
shapes meaning beyond literal semantics is central to un-                     Translation and Specification Mismatch. Languages dif-
derstanding pragmatic underspecification. Grice (1975) es-                    fer in what they require speakers to specify: for example,
tablished foundational principles of cooperative communi-                     a language with grammatical gender marking forces gen-
   4
                                                                              der specification (Savoldi et al., 2021; 2025). To preserve
     Generally speaking, a formal language is defined by a set of             underspecification during translation, clarifications may be
deterministic rules, both for its syntax (i.e., the utterances) and its
semantics (i.e., the mapping between utterances and objects). In              necessary, potentially making the translation longer than the
particular, there is no ambiguity or randomness; an utterance may             original. For instance, describing a nurse’s actions without
denote a set of objects, but the mapping itself is not random.                specifying gender is natural in English but requires explicit

                                                                          3
                                Natural Language Should Not Fully Replace Formal Languages

disambiguation in languages with grammatical gender—or                         constraints       description       generation
an explicit statement that gender is unspecified.                        Y                   T                 U                 Ŷ
This phenomenon generalizes beyond natural languages:
translating from natural language to formal specification
                                                                                             implementation
often requires resolving underspecification, either by mak-
ing constraints explicit or by choosing among alternatives           Figure 2. Two specification paths. Natural language path (solid
the speaker was indifferent to. An example is mathematical           blue): Y → T → U → Ŷ . The user forms a task T (allowing
reasoning, where formal notation forces rigor and minimal            indifferent compression), describes it in natural language U (allow-
ambiguity. Fully describing mathematical proofs in natural           ing pragmatic compression), and the model generates Ŷ . Formal
language will lead to long, and often inconsistent, proofs.          language path (dashed red): Y → Ŷ via direct specification.

Compositionality. Compositionality—the principle that
the meaning of a complex expression is determined by the                  (i.e., expects in this context) but not specified in u. Not
meanings of its parts and how they combine (Partee et al.,                satisfying Cimp is considered a failure.
1995; Pelletier, 1994)—enables efficient specification by
allowing constraints to be stated independently. “A red              A constraint is formally an indicator function c : M →
sports car” comprises color and type constraints separately,         {0, 1} for the set of outputs satisfying the constraint.
and each component can be identified as the QUD.                     Definition 3.2 (Denotation). The denotation of a task is
The compositional structure of both natural and formal               defined as:
languages enables their combination: specifications can
mix languages, using natural language for high-level intent                  [[T ]] := {y ∈ M : ∀c ∈ Cimp ∪ Cexp , c(y) = 1}          (1)
and formal notation for precise details, with compositional
boundaries determining where each is most efficient.                 3.2. The Specification Chain

3. Formal Framework                                                  We model specification as information flow from the user’s
                                                                     intended output to the generated result. The key insight is
We formalize these intuitions using a constraint satisfac-           that natural language and formal language follow different
tion framework, inspired by Fregean semantics (Frege et al.,         paths with different information-theoretic properties. For
1951), distinguishing between explicit and implicit con-             our purposes, regard the actual output (or implementation)
straints. We then formalize when natural language loses              format as the formal language.
efficiency to formal specification. Our analysis follows the         Definition 3.3 (Random Variables). Let Y be a user’s envi-
assumption that shorter utterances are more efficient (Good-         sioned output in meaning space M , with prior pM , let T be
man & Frank, 2016; Gibson et al., 2019).                             a task defining an equivalence class [[T ]] ⊆ M of acceptable
                                                                     outputs, let U be a natural language description, and let Ŷ
3.1. Tasks as Constraint Satisfaction                                be the generated output.
We address tasks where the input is a textual description, and
the output can be from various modalities (images, code,             We emphasize that Y is a single instance, corresponding to
music, etc.). We refer to the space of possible outputs              an envisioned or actual outcome, as opposed to [[T ]], which
as a “world model”—a confined subset of the real world               is a set of acceptable outcomes. We assume Y ∈ [[T ]], i.e.,
with well-defined structure—which is specified in a formal           the user’s intent is realizable as a task. Cases where the
language. Adapting notation from formal logic (Partee et al.,        user envisions an output that no task description can pick
2012) and the Rational Speech Act (RSA; Goodman &                    out (e.g., self-contradictory) fall outside our framework; in
Frank, 2016) terminology, U denotes the utterance space              practice, such intents surface as failures during iteration.
and M the meaning space.                                             Generating Ŷ can follow two paths (Figure 2):
Definition 3.1 (Task and Constraints). A task T , given
as textual description u ∈ U , is represented by a tuple             1. Natural Language Path: Y → T → U → Ŷ . Rather
(Cexp , Cimp , M ) where:                                            than specifying Y precisely, the user specifies a task T such
                                                                     that any Ŷ ∈ [[T ]] is acceptable, thus applying indifferent un-
   • M is the space of possible outputs (e.g., all valid im-         derspecification (4). Additionally, the description U states
     ages, programs, etc.).                                          only the explicit constraints of T , relying on a model to
                                                                     generate Ŷ while satisfying the implicit constraints, thus
   • Cexp is the set of constraints explicitly specified in u.
                                                                     applying pragmatic underspecification (3). Importantly, U
   • Cimp is a set of implicit constraints the user intends          and Ŷ are visible while Y and T are latent.

                                                                 4
                                Natural Language Should Not Fully Replace Formal Languages

2. Formal Language Path: Y → Ŷ . Formal languages                    The following lemma shows that supporting diverse do-
implement Y directly, applying full specification (2).                mains increases the expected translation gap—the more
                                                                      open-endedness, the larger the gap to a random domain.
The natural language path forms a Markov chain. By the
Data Processing Inequality (Cover, 1999):                             Lemma 3.6. Let D be a set of domain distributions. The
                                                                      expected translation gap satisfies:
         I(Y ; Ŷ ) ≤ I(Y ; U ) ≤ I(Y ; T ) ≤ H(Y )        (2)
                                                                            Ep∈D [DKL (p∥pNL )] = DKL (p̄∥pNL ) + JSD(D)         (4)
Providing bounds on how much information about Y can
reach Ŷ through the natural language path.                           where the expectation is for a uniform distribution over D,
                                                                      pNL is a common language, p̄ is the average distribution,
3.3. Task Specificity                                                 and JSD(D) is the Jensen-Shannon divergence.
We now define the central quantity that determines when
each path is advantageous.                                            Proof. See Appendix B.
Definition 3.4 (Task Specificity). The task specificity σϵ (T )
is defined as the minimal mutual information I(Y ; Ŷ ) such          3.5. Specification Costs
that Ŷ ∈ [[T ]] with probability > 1 − ϵ.
                                                                      We now characterize the cost of each specification path.
For simplicity, we will usually write σ(T ) or σ. Intuitively,        Definition 3.7 (Description Length). Let LNL (σ) be the
σ captures how much the task allows the output to diverge             minimum expected description length to achieve I(Y ; Ŷ ) ≥
from an example one. When σ = 0, any output is accept-                σ via natural language, and Lformal := EY [Lformal (Y )] be
able, and when σ = H(Y ), only the exact intended output              the expected length of a formal specification of Y .
is acceptable. For uniform distributions, this captures ex-
                                                                      Proposition 3.8 (Natural Language Cost). To achieve
actly the difference in (log) size between the set of possible
                                                                      I(Y ; Ŷ ) ≥ σ via the natural language path:
outputs and the acceptable ones. For example, creative tasks
like “generate a poem” have low specificity, since a poem
                                                                                         LNL (σ) ≥ σ + ∆trans                    (5)
the user had in mind is only loosely indicative of a random
acceptable poem. In contrast, reproducing a specific image
has maximal specificity.                                              Proof. By (2), I(Y ; U ) ≥ I(Y ; Ŷ ) ≥ σ. The description
                                                                      U must therefore carry at least σ bits about Y . Encoding
3.4. The Translation Gap                                              this in natural language incurs the translation gap, giving
                                                                      the bound.
Natural language is optimized for open-ended communica-
tion across all domains (§2). When used to describe outputs
from a specific domain M , this generality incurs a cost.             The natural language cost can thus be divided into two
                                                                      components: the specificity requirement σ (how much in-
The expected bits required to describe an output Y ∼ pM us-           formation must be conveyed) and the translation gap ∆trans
ing natural language distributed as pNL is the cross-entropy:         (the overhead of using a general-purpose language).
         H(pM , pNL ) = H(pM ) + DKL (pM ∥pNL )            (3)        When using formal language, we define redundancy as a
                                                                      measure of the overhead of a formal language beyond the
Definition 3.5 (Translation Gap). The translation gap is              information-theoretic minimum.
∆trans = DKL (pM ∥pNL ), the KL divergence from the do-
main distribution to the natural language distribution.               Definition 3.9 (Redundancy). We define the redundancy of
                                                                      a formal language as Rformal = Lformal − H(Y ).
The translation gap quantifies the cost of using a general-
purpose language to describe domain-specific content. It              Formal languages specify Y completely, regardless of how
is always non-negative and is zero only when natural lan-             much of that specification the task requires. The expected
guage perfectly matches the domain distribution. ∆trans thus          length therefore decomposes as Lformal = H(Y ) + Rformal :
represents the irreducible inefficiency of using language             the entropy H(Y ) is the information-theoretic minimum,
modeling as compression (Deletang et al., 2024).                      and Rformal is the redundancy of the encoding. Crucially, no
                                                                      translation gap is incurred.
As an example, consider reporting the color of a banana. Ba-
nanas in images are typically yellow, but “yellow banana” is
                                                                      3.6. The Specificity Crossover
marked (i.e., less common) in language because the modifier
is redundant (Paik et al., 2021). The translation gap captures        We can now state our main result: natural language and
this mismatch between visual and linguistic distributions.            formal language dominate in different specificity regimes.

                                                                  5
                                Natural Language Should Not Fully Replace Formal Languages

Theorem 3.10 (Specificity Crossover). For Y ∼ pM , there              4. Case Study: Image Generation and Other
exists a crossover threshold:                                            Modalities
               σ ∗ = H(Y ) + Rformal − ∆trans               (6)       Text-to-image generation has emerged as one of the most
                                                                      visible applications of generative AI, with significant impli-
such that:
                                                                      cations for artists’ workflows and employment (Jiang et al.,
                                                                      2023). Anantrasirichai & Bull (2022) provide a broader ex-
   • For σ(T ) < σ ∗ : Natural language can be more effi-
                                                                      amination of AI for creativity across modalities, including
     cient (i.e., possibly LNL < Lformal )
                                                                      ethical considerations, while surveys reveal complex atti-
   • For σ(T ) ≥ σ ∗ : Natural language cannot be more                tudes among both professional and non-professional artists
     efficient (i.e., necessarily Lformal ≤ LNL )                     (Tang et al., 2024). Understanding the limitations of natural
                                                                      language for image specification is thus both theoretically
Proof. By 3.8, achieving σ requires LNL (σ) ≥ σ + ∆trans .            important and practically consequential.
Formal specification costs Lformal = H(Y ) + Rformal regard-
less of σ. Setting LNL < Lformal yields:                              The specificity crossover. Image generation provides a
                                                                      “clean” domain for demonstrating the specificity crossover.
         σ + ∆trans < H(Y ) + Rformal ⇒ σ < σ ∗             (7)       Consider white noise images where pixels are independently
                                                                      and uniformly distributed: such images are maximally in-
                                                                      compressible, with maximal entropy and zero redundancy
                                                                      (Rformal = 0). Since natural language must assign probabil-
The crossover point σ ∗ marks where underspecification ben-
                                                                      ity mass to all communicative intents, any nonzero trans-
efits can no longer compensate for the translation gap. Be-
                                                                      lation gap has ∆trans = DKL (pM ∥pNL ) > 0. By Theorem
low σ ∗ , natural language can win by not specifying what
                                                                      3.10, a crossover threshold σ ∗ < H(Y ) must therefore
doesn’t matter or what can be inferred. Above σ ∗ , formal
                                                                      exist.
language wins by avoiding translation overhead.
Remark 3.11. For the threshold σ ∗ to be meaningful, we
                                                                      Quantitative Illustration. To illustrate the information-
need Rformal < ∆trans . This criterion is satisfied whenever
                                                                      theoretic limits, consider a 250 × 250-pixel RGB image.
Rformal is small (efficient formal language) and ∆trans > 0
                                                                      The total number of possible images is 2563×250×250 =
(domain differs from general language). If ∆trans ≤ Rformal ,
                                                                      21,500,000 . Assuming a vocabulary of 32 characters, a string
natural language could be more efficient even at full spec-
                                                                      of length N encodes 25N possible strings, so N ≥ 300,000
ification by removing redundancy in the target. However,
                                                                      characters would be needed—comparable to a novel. While
intuitively, we expect domain-specific languages to be better
                                                                      the space of images people actually want is obviously
optimized for their domains compared to natural language.
                                                                      smaller, this demonstration shows a fundamental challenge:
Remark 3.12. Proposition 3.8 describes a lower bound, as-             as users push toward greater specificity, prompts must grow
suming no redundancy in natural language. In practice, nat-           toward this limit, becoming unwieldy. Consider an artist
ural language also has redundancy (Shannon, 1951), even if            who envisions a detailed work of art. Image generators
lower than in some formal languages (Hindle et al., 2016),            cannot practically implement this artwork simply because it
thus tightening the bound.                                            will be too hard to describe in full detail.
Remark 3.13. Our analysis assumes a one-shot setting, in
which a valid generated instance is obtained. In practice,            4.1. Empirical Evidence in Image Generation
pragmatic inference errors often occur and latent prefer-
ences often arise, resulting in an iterative process of trial         Trends in Iterative Prompting. The theoretical crossover
and error. This process can involve repetition and overspeci-         manifests clearly in empirical studies of user interactions
fication raising the price of natural language and lowering           with text-to-image systems. Don-Yehiya et al. (2023) com-
the threshold.                                                        piled a dataset of iterative interactions between users and
Remark 3.14. In the other direction, using formal languages           Midjourney, analyzing how prompts evolve across multi-
typically requires domain learning and mental effort (Casal-          ple attempts. Their findings reveal two distinct trends that
nuovo et al., 2018). These factors present additional costs           directly support our framework:
that may raise σ ∗ , but should not eliminate the crossover.
                                                                        1. Trend 1: Increasing Verbosity. Prompts become
An important conclusion from the framework and theorem                     more verbose—the length and syntactic complexity
is that if a task is compositional (§2.3), different components            grow—as interactions become longer. Users “climb
can vary in their implementation method. This idea leads                   down the ladder of specification”, representing the con-
to hybrid approaches, combining both natural and formal                    version of pragmatic underspecification (3)—where
language.                                                                  users assume the model would infer their intent —

                                                                  6
                                   Natural Language Should Not Fully Replace Formal Languages




                                                                                                    Dalmatians: only a head,     Actor Jeff Daniels as Roger Dearly
                                                                                                          visible face,        sitting on a wooden bench in a park ...
                                                                                                       only grass - no sky      Pongo the Dalmatian sits patiently
               Dogs             Dogs with a grass background   Dalmatians with a grass background      or flowers or trees            on the grass beside him ...


  Low task                                                                                                                                            High task
 specificity                                                                                                                                          specificity



Figure 3. Illustration of task specificity in image generation. As the description becomes longer, the space of images is narrower. At the
limit, if a specific image is desired, perfectly describing it in words is inefficient (compared to filming or drawing). All images were
generated by Gemini-3, except for the image from Disney’s 1996 101 Dalmatians (right).


      into full specification (2) or even overspecification (1),               4.2. Additional Modalities
      where users add redundant information to compensate                      Code Generation. In code generation, the distinction be-
      for misinterpretation.                                                   tween specification understanding and code optimization be-
  2. Trend 2: Increasing Model-Orientation. Prompts                            comes apparent. We generally divide code requirements into
     shift toward language patterns that the model responds                    two broad categories: outcome-related, which can include
     to more reliably. Perplexity decreases as users adopt                     outputs and runtime, and code-related, which can include
     “magic words”—terms that empirically improve gener-                       readability, maintainability, code weaknesses, etc. Gener-
     ation quality regardless of their natural language mean-                  ally, loose code-related requirements allow a large degree of
     ing (e.g., “4k,” “artstation,” “trending”). This adapta-                  autonomy for the agent, potentially making outcome-related
     tion represents users implicitly reducing the transla-                    requirements more efficient. Conversely, code-related re-
     tion gap (§3.4) by shifting toward language that better                   quirements are often more general than outcome-related
     matches the model’s training distribution, sacrificing                    ones, since a single function can correspond to infinitely
     naturalness for domain-specific efficiency.                               many outcomes, thus being more efficient.
                                                                              In simple visualization or proof-of-concept tasks, natural
Prompt engineering. Research on prompt engineering                            language excels: “make a bar chart of sales data” efficiently
for image generation (Oppenlaender, 2024; Liu & Chilton,                      conveys intent with few code-related requirements and loose
2022) further confirms these findings. Initially, prompts                     outcome-related ones. These tasks leverage indifferent un-
are highly underspecified (“a cat”), efficiently describing                   derspecification (4) to avoid the overhead of precise coding.
large equivalence classes. As users seek more specific out-                   However, production code requirements dramatically in-
puts, prompt engineering tends to create increasingly spe-                    crease task specificity. Outcome-related requirements about
cific prompts (“a fluffy orange tabby cat, sitting, front view,               edge cases, etc., and code-related requirements for error
studio lighting, photorealistic”) (Hao et al., 2023). The phe-                handling, optimization, and security represent implicit con-
nomenon of negative prompts (Ban et al., 2024; Park et al.,                   straints that surface through testing. Additionally, errors in
2025), such as “no extra fingers,” further demonstrates the                   production code are more costly, forcing extra specification.
process: users initially operate at pragmatic underspecifi-                   Multiple works show that while AI coding assistants accel-
cation, assuming shared knowledge, but are forced toward                      erate initial development, they can lead to low-quality code
overspecification upon failure.                                               (Li et al., 2024), requiring iterative refinement that often
                                                                              negates these gains (Becker et al., 2025). These trends align
Hybrid Approaches. Leveraging compositionality (§2.3),                        with our crossover prediction: as task specificity increases,
hybrid approaches can benefit from both modalities. For                       the cross-entropy cost exceeds underspecification benefits.
images, this suggests combining natural language for
high-level concepts (“professional business portrait”) with                   The hybrid approach is also prominent in coding (Barke
sketches or masks for spatial layout or specific details. Work                et al., 2023; Tang et al., 2025). Modern coding assistants pro-
on hybrid inputs (Zeng et al., 2022; Vinker et al., 2025)                     viding intelligent code completion can achieve compression
demonstrates this principle. As task specificity increases,                   benefits through pragmatic underspecification (3; exploit-
more specification naturally shifts toward direct manipula-                   ing repeated patterns, suggesting contextual completions),
tion in the target domain, with natural language reserved for                 while partially avoiding the overhead of natural language.
aspects where underspecification provides genuine value.                      Moreover, when using coding agents iteratively, the input

                                                                          7
                                Natural Language Should Not Fully Replace Formal Languages

consists of code and new requirements (or error reports),             tongues, are almost impossible to avoid” (Dijkstra, 1978).
which can be seen as a hybrid setting (at least when the user
                                                                      Our framework suggests that current evaluation practices
gives some form of feedback, even implicit, about the code
                                                                      may mischaracterize the value of many tasks. For example,
itself).
                                                                      popular code generation benchmarks, such as HumanEval
                                                                      (Chen et al., 2021) and SWE-bench (Jimenez et al., 2023),
Audio and Music Generation. Text-to-audio generation                  primarily test code implementation rather than specification
(Agostinelli et al., 2023; Lerch et al., 2025) shows similar          understanding. Benchmarks for specification understanding
patterns. For general requests like “relaxing piano music”,           and hybrid programming should also be developed. Specifi-
the large range of acceptable outputs allows efficient natu-          cally, code benchmarks should explicitly compare: natural
ral language description, exploiting vast underspecification.         language specification with AI generation, code comple-
Conversely, requesting specific output can grow extremely             tion assistance within formal languages, and naive coding
verbose, at which point, MIDI specification or musical                without assistance, across varying task specificity levels,
notation—formal languages optimized for concrete musical              including both outcome- and code-related requirements.
description— become more efficient (Mitra & Zualkernan,
                                                                      Regarding practical tools, we advocate for hybrid systems,
2025). Here too, hybrid methods that guide generation with
                                                                      optimized for pragmatic understanding, that allow seam-
musical examples were proposed (Zhu et al., 2024).
                                                                      less user involvement in the process (Tang et al., 2025).
                                                                      These systems will benefit from both qualities: efficient
Text Generation and Summarization. Interestingly, the                 underspecification and pragmatics of natural language, and
crossover can favor description in some text generation               precise specification of formal language. Our analysis also
tasks. Writing prose from bullet points (summary → full               frames two open empirical questions: how should systems
text) may be more efficient than direct prose writing because         balance pragmatic assumptions against asking for clarifica-
the bullets provide compressed details while underspecify-            tion, and at what compositional boundaries should formal
ing stylistic choices. Similarly, in story generation (Teleki         components be optimally used? Both can be studied directly
et al., 2025) and summarization (Zhang et al., 2025), loose           within the specificity-crossover framework. Importantly, in
requirements (e.g., what exactly should be included in the            these systems, human expertise will still have a significant
summary?) that allow a large output space (Chawla et al.,             role, allowing better integration and supervision.
2026) can utilize underspecification. As the requirements be-
come more precise, the ability to create a satisfying outcome         6. Alternative Views
based on a prompt alone diminishes. In these cases, hybrid
approaches are natural, where partial input (Lin et al., 2025;        The position we argue against holds that advances in LLMs
Lee et al., 2025; Urlana et al., 2024) or post-generation             will eventually render formal languages obsolete. This posi-
editing of the outcome can combine both qualities.                    tion is clearly present in the industry, as mentioned in the
                                                                      Introduction (§1). For example, in code, proponents point
                                                                      to rapid improvements in code generation and the democra-
5. Implications and Future Directions                                 tizing potential of natural language interfaces (Jiang et al.,
Our analysis reveals that natural and formal languages oc-            2024), viewing current limitations as engineering challenges
cupy different niches in the specification space. Natural             that scale and better training will overcome. Our analysis
language excels at low specificity tasks with large equiv-            challenges this view not by denying continued progress, but
alence classes, creative tasks where exploration is valued,           by identifying fundamental information-theoretic limits: the
and contexts with low expertise requirements, where under-            translation gap ∆trans represents structural constraints that
specification can be exploited Formal languages excel at              persist regardless of model capability. Even a perfect model
high specificity tasks, contexts where domain expertise is            cannot escape the fact that natural language, optimized for
available, and production systems requiring precision and             open-ended communication, incurs unavoidable overhead
verifiability. Formal languages succeed through domain-               when specifying concrete details in restricted domains.
tailored language, lower error rates, and formal verifiability.       We also argue against the opposite view, saying that tools
We reiterate the classical view (Meyer, 1993; Wing, 2002;             such as code generators are “more harm than good”. This
Gervasi & Nuseibeh, 2002; Ferré, 2016) that formal specifi-          sentiment is non-negligible among programmers (as evinced
cation should be complementary to natural descriptions.               in the survey mentioned in §1). We argue that despite some
Formal languages are also crucial for a precise understand-           challenges, these tools have a theoretical role through indif-
ing of the area of interest, allowing deep insight into under-        ferent and pragmatic underspecification, providing value for
lying rules, which is also beneficial in practice. As Dijkstra        both professional and low-level programming.
observed, formal texts are “an amazingly effective tool for
ruling out all sorts of nonsense that, when we use our native

                                                                  8
                                Natural Language Should Not Fully Replace Formal Languages

7. Conclusion                                                          References
We presented a formal framework that shows natural and                 Agostinelli, A., Denk, T. I., Borsos, Z., Engel, J., Verzetti,
formal languages serve fundamentally different purposes                  M., Caillon, A., Huang, Q., Jansen, A., Roberts, A.,
in task specification. Our framework builds on linguis-                 Tagliasacchi, M., et al. Musiclm: Generating music from
tic insights, specifically underspecification. Under this                text. arXiv preprint arXiv:2301.11325, 2023.
framework, natural language achieves efficiency through
underspecification—both indifferent and pragmatic—while                Anantrasirichai, N. and Bull, D. Artificial intelligence in
formal languages provide precise control. We show that,                  the creative industries: a review. Artificial intelligence
due to the translation gap, a specificity crossover point exists         review, 55(1):589–656, 2022.
between cases where pure natural language or pure formal
                                                                       Ban, Y., Wang, R., Zhou, T., Cheng, M., Gong, B., and
language is more efficient. Hybrid models can achieve both
                                                                         Hsieh, C.-J. Understanding the impact of negative
benefits by applying different methods across components.
                                                                         prompts: When and how do they take effect? In european
We also demonstrated that our framework is applicable to
                                                                         conference on computer vision, pp. 190–206. Springer,
other modalities, such as images, code, audio, and even text.
                                                                         2024.
Our central claim is the following: natural language
will not—and should not—fully replace formal languages.                Barke, S., James, M. B., and Polikarpova, N. Grounded
Rather, both languages form a complementary toolkit, with                copilot: How programmers interact with code-generating
optimal choice depending on task specificity, novelty, and               models. Proceedings of the ACM on Programming Lan-
professional requirements. Instead of abandoning formal                  guages, 7(OOPSLA1):85–111, 2023.
languages, we should invest in tools that improve efficiency
                                                                       Barker, C. Free choice permission as resource-sensitive
within formal domains while reserving natural language
                                                                         reasoning. Semantics and Pragmatics, 3:10–1, 2010.
for areas or components where underspecification provides
genuine value. The future lies in seamless integration of              Becker, J., Rush, N., Barnes, E., and Rein, D. Measuring
both modalities, allowing users to operate fluidly across the            the impact of early-2025 ai on experienced open-source
specification spectrum.                                                  developer productivity, 2025. URL https://arxiv.
We conclude with Jensen Huang’s broader claim:5                          org/abs/2507.09089.

                                                                       Bergen, L. and Grodner, D. J. Speaker knowledge influences
   AI is the great equalizer... For the last 50 years, 60                the comprehension of pragmatic inferences. Journal of
   years, Computer Science became a field of science,                    Experimental Psychology: Learning, Memory, and Cog-
   and it was available to tens of millions of people out                nition, 38(5):1450, 2012.
   of billions of people. This technology was hard to use.             Cadoli, M. and Schaerf, M. A survey of complexity re-
   ... but now, all of a sudden, there’s a new program-                  sults for non-monotonic logics. The Journal of Logic
   ming language. This new programming language is                       Programming, 17(2-4):127–160, 1993.
   called “human”. ... The way you program a computer
   today [is] to ask the computer to do something for                  Carston, R. Thoughts and utterances: The pragmatics of
   you, even write a program, generate images, write a                   explicit communication. John Wiley & Sons, 2008.
   poem. Just ask it nicely.
                                                                       Casalnuovo, C., Sagae, K., and Devanbu, P. Studying the
                                                                         difference between natural and programming language
Code and image generators provide an extremely powerful                  corpora, 2018. URL https://arxiv.org/abs/
tool, especially for non-experts. However, we argue that the             1806.02437.
role of domain experts—such as programmers and artists—
will not become obsolete.                                              Chawla, K., Zhu, C., Cai, P., Cho, S., Novotney, S., Singh,
                                                                         A., Lewis, J., Safewright, K., Samuel, A., Babinsky, E.,
                                                                         Zhang, S.-X., and Sahu, S. Lessons from the field: An
Acknowledgments                                                          adaptable lifecycle approach to applied dialogue sum-
This research was supported by grants from the Israeli Min-              marization, 2026. URL https://arxiv.org/abs/
istry of Science and Technology, the Council for Higher                  2601.08682.
Education, and the Israel Science Foundation (Grant No.                Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto,
2424/21).                                                                H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N.,
  5
    London Tech, June         2025;    https://youtu.be/                 Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov,
SsNS3Xm9ig4?t=1940                                                       M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray,

                                                                   9
                              Natural Language Should Not Fully Replace Formal Languages

  S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavar-          Eshraghian, F., Hafezieh, N., Farivar, F., and de Cesare, S.
  ian, M., Winter, C., Tillet, P., Such, F. P., Cummings,             Ai in software programming: understanding emotional
  D., Plappert, M., Chantzis, F., Barnes, E., Herbert-                responses to github copilot. Information Technology &
  Voss, A., Guss, W. H., Nichol, A., Paino, A., Tezak,                People, 38(4):1659–1685, 2025.
  N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saun-
  ders, W., Hesse, C., Carr, A. N., Leike, J., Achiam,              Ferré, S. Bridging the gap between formal languages and
  J., Misra, V., Morikawa, E., Radford, A., Knight, M.,               natural languages with zippers. In European Semantic
  Brundage, M., Murati, M., Mayer, K., Welinder, P., Mc-              Web Conference, pp. 269–284. Springer, 2016.
  Grew, B., Amodei, D., McCandlish, S., Sutskever, I., and
  Zaremba, W. Evaluating large language models trained              Ferreira, V. S. Ambiguity, accessibility, and a division of
  on code, 2021. URL https://arxiv.org/abs/                           labor for communicative success. Psychology of Learning
  2107.03374.                                                         and motivation, 49:209–246, 2008.

Clark, H. H. Using language. Cambridge university press,            Frank, M. C. and Goodman, N. D. Predicting pragmatic
  1996.                                                               reasoning in language games. Science, 336(6084):998–
                                                                      998, 2012.
Copestake, A., Flickinger, D., Pollard, C., and Sag, I. A.
  Minimal recursion semantics: An introduction. Research            Frege, G., Geach, P. T., and Black, M. On concept and
  on language and computation, 3(2):281–332, 2005.                    object. Mind, 60(238):168–180, 1951.

Cover, T. M. Elements of information theory. John Wiley &           Frisson, S. Semantic underspecification in language process-
  Sons, 1999.                                                         ing. Language and linguistics compass, 3(1):111–127,
                                                                      2009.
Deacon, T. W. The symbolic species: The co-evolution of
  language and the brain. WW Norton & Company, 1998.                Futrell, R. and Hahn, M. Information theory as a bridge
                                                                      between language function and language form. Frontiers
Degen, J. The rational speech act framework. Annual                   in Communication, 7:657725, 2022.
  Review of Linguistics, 9(1):519–540, 2023.
                                                                    Gervasi, V. and Nuseibeh, B. Lightweight validation of
Deletang, G., Ruoss, A., Duquenne, P.-A., Catt, E., Ge-
                                                                      natural language requirements. Software: Practice and
  newein, T., Mattern, C., Grau-Moya, J., Wenliang, L. K.,
                                                                      Experience, 32(2):113–133, 2002.
  Aitchison, M., Orseau, L., Hutter, M., and Veness, J.
  Language modeling is compression. In The Twelfth                  Gibson, E., Futrell, R., Piantadosi, S. P., Dautriche, I., Ma-
  International Conference on Learning Representations,               howald, K., Bergen, L., and Levy, R. How efficiency
  2024. URL https://openreview.net/forum?                             shapes human language. Trends in cognitive sciences, 23
  id=jznbgiynus.                                                      (5):389–407, 2019.
Dijkstra, E. W. On the foolishness of ”natural language pro-        Ginzburg, J. et al. Dynamics and the semantics of dialogue.
  gramming”. In Program Construction, International Sum-              Logic, language and computation, 1:221–237, 1996.
  mer Schoo, pp. 51–53, Berlin, Heidelberg, 1978. Springer-
  Verlag. ISBN 354009251X.                                          Goodman, N. D. and Frank, M. C. Pragmatic language inter-
                                                                      pretation as probabilistic inference. Trends in cognitive
Don-Yehiya, S., Choshen, L., and Abend, O. Human
                                                                      sciences, 20(11):818–829, 2016.
  learning by model feedback: The dynamics of iterative
  prompting with midjourney. In Bouamor, H., Pino, J.,              Grice, H. P. Logic and conversation. Syntax and semantics,
  and Bali, K. (eds.), Proceedings of the 2023 Conference             3:43–58, 1975.
  on Empirical Methods in Natural Language Processing,
  pp. 4146–4161, Singapore, December 2023. Association              Hao, Y., Chi, Z., Dong, L., and Wei, F. Optimizing prompts
  for Computational Linguistics. doi: 10.18653/v1/2023.               for text-to-image generation. Advances in Neural Infor-
  emnlp-main.253. URL https://aclanthology.                           mation Processing Systems, 36:66923–66939, 2023.
  org/2023.emnlp-main.253/.
                                                                    Hindle, A., Barr, E. T., Gabel, M., Su, Z., and Devanbu, P.
Dora, S., Lunkad, D., Aslam, N., Venkatesan, S., and Shukla,          On the naturalness of software. Communications of the
  S. K. The hidden risks of llm-generated web applica-                ACM, 59(5):122–131, 2016.
  tion code: A security-centric evaluation of code genera-
  tion capabilities in large language models, 2025. URL             Hockett, C. F. and Hockett, C. D. The origin of speech.
  https://arxiv.org/abs/2504.20612.                                  Scientific American, 203(3):88–97, 1960.

                                                               10
                               Natural Language Should Not Fully Replace Formal Languages

Jiang, H. H., Brown, L., Cheng, J., Khan, M., Gupta, A.,              Lin, Z., Xiao, Y., Mo, Z., Zhang, Q., Wang, J., Chen, J.,
   Workman, D., Hanna, A., Flowers, J., and Gebru, T. Ai                Zhang, J., Zhang, H., Liu, Z., Fang, X., and Xu, X. R2 :
   art and its impact on artists. In Proceedings of the 2023            A llm based novel-to-screenplay generation framework
   AAAI/ACM Conference on AI, Ethics, and Society, pp.                  with causal plot graphs, 2025. URL https://arxiv.
   363–374, 2023.                                                       org/abs/2503.15655.
Jiang, J., Wang, F., Shen, J., Kim, S., and Kim, S. A survey          Liu, V. and Chilton, L. B. Design guidelines for prompt
   on large language models for code generation. arXiv                  engineering text-to-image generative models. In Proceed-
   preprint arXiv:2406.00515, 2024.                                     ings of the 2022 CHI conference on human factors in
                                                                        computing systems, pp. 1–23, 2022.
Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press,
  O., and Narasimhan, K. Swe-bench: Can language mod-                 Marzen, S. E. and DeDeo, S. The evolution of lossy com-
  els resolve real-world github issues? arXiv preprint                 pression. Journal of The Royal Society Interface, 14(130):
  arXiv:2310.06770, 2023.                                              20170166, 2017.
Joel, S., Wu, J., and Fard, F. A survey on llm-based code             Mercer, R. E. A default logic approach to the derivation of
  generation for low-resource and domain-specific program-             natural language presuppositions. PhD thesis, University
  ming languages. ACM Transactions on Software Engi-                   of British Columbia, 1987.
  neering and Methodology, 2024.
                                                                      Meyer, B. On formalism in specifications. In Program
Kemp, C. and Regier, T. Kinship categories across lan-                 Verification: Fundamental Issues in Computer Science,
  guages reflect general communicative principles. Science,            pp. 155–189. Springer, 1993.
  336(6084):1049–1054, 2012.
                                                                      Mitra, R. and Zualkernan, I. Music generation using deep
Krifka, M. Approximate interpretation of number words.
                                                                       learning and generative ai: a systematic review. IEEE
  Humboldt-Universität zu Berlin, Philosophische Fakultät
                                                                       Access, 2025.
  II, 2007.
Lasersohn, P. Pragmatic halos. Language, pp. 522–551,                 Oaksford, M. and Chater, N. Bayesian rationality: The
  1999.                                                                 probabilistic approach to human reasoning. Oxford Uni-
                                                                        versity Press, 2007.
Lee, Y., Ka, S., Son, B., Kang, P., and Kang, J. Navi-
  gating the path of writing: Outline-guided text genera-             Oppenlaender, J. A taxonomy of prompt modifiers for
  tion with large language models. In Chen, W., Yang,                   text-to-image generation. Behaviour & Information Tech-
  Y., Kachuee, M., and Fu, X.-Y. (eds.), Proceedings of                 nology, 43(15):3763–3776, 2024.
  the 2025 Conference of the Nations of the Americas
                                                                      Oruche, R., Goruganthu, S. K., Akula, R., Cheng, X., Goni,
  Chapter of the Association for Computational Linguis-
                                                                        A. M., Shibo, B. W., Kee, K., Zampieri, M., and Calyam,
  tics: Human Language Technologies (Volume 3: In-
                                                                        P. A survey on the recent advancements in human-
  dustry Track), pp. 233–250, Albuquerque, New Mex-
                                                                        centered dialog systems. ACM Comput. Surv., 57(10),
  ico, April 2025. Association for Computational Linguis-
                                                                        May 2025. ISSN 0360-0300. doi: 10.1145/3729220.
  tics. ISBN 979-8-89176-194-0. doi: 10.18653/v1/2025.
                                                                        URL https://doi.org/10.1145/3729220.
  naacl-industry.20. URL https://aclanthology.
  org/2025.naacl-industry.20/.                                        Paik, C., Aroca-Ouellette, S., Roncone, A., and Kann, K.
                                                                        The World of an Octopus: How Reporting Bias Influences
Lerch, A., Arthur, C., Bryan-Kinns, N., Ford, C., Sun, Q.,
                                                                        a Language Model’s Perception of Color. In Moens,
  and Vinay, A. Survey on the evaluation of generative
                                                                        M.-F., Huang, X., Specia, L., and Yih, S. W.-t. (eds.),
  models in music. ACM Computing Surveys, 58(4):1–36,
                                                                        Proceedings of the 2021 Conference on Empirical Meth-
  2025.
                                                                        ods in Natural Language Processing, pp. 823–835, On-
Levinson, S. C. Presumptive meanings: The theory of                     line and Punta Cana, Dominican Republic, November
  generalized conversational implicature. MIT press, 2000.              2021. Association for Computational Linguistics. doi:
                                                                        10.18653/v1/2021.emnlp-main.63. URL https://
Li, S., Cheng, Y., Chen, J., Xuan, J., He, S., and Shang, W.            aclanthology.org/2021.emnlp-main.63/.
  Assessing the performance of ai-generated code: A case
  study on github copilot. In 2024 IEEE 35th International            Park, S., Kim, E., Oh, Y., Choi, J., and Yoon, S. Guiding
  Symposium on Software Reliability Engineering (ISSRE),                what not to generate: Automated negative prompting for
  pp. 216–227, 2024. doi: 10.1109/ISSRE62328.2024.                      text-image alignment. arXiv preprint arXiv:2512.07702,
  00030.                                                                2025.

                                                                 11
                               Natural Language Should Not Fully Replace Formal Languages

Partee, B. et al. Lexical semantics and compositionality.            Tang, Y., Zhang, N., Ciancia, M., and Wang, Z. Exploring
  An invitation to cognitive science: Language, 1:311–360,             the impact of ai-generated image tools on professional
  1995.                                                                and non-professional users in the art and design fields.
                                                                       In Companion Publication of the 2024 Conference on
Partee, B. B., Ter Meulen, A. G., and Wall, R. Mathematical            Computer-Supported Cooperative Work and Social Com-
  methods in linguistics, volume 30. Springer Science &                puting, pp. 451–458, 2024.
  Business Media, 2012.
                                                                     Teleki, M., Bengali, V., Dong, X., Janjur, S. T., Liu, H.,
Pelletier, F. J. The principle of semantic compositionality.           Liu, T., Wang, C., Liu, T., Zhang, Y., Shipman, F.,
  Topoi, 13(1):11–24, 1994.                                            and Caverlee, J. A survey on LLMs for story gen-
Piantadosi, S. T., Tily, H., and Gibson, E. The communica-             eration. In Christodoulopoulos, C., Chakraborty, T.,
  tive function of ambiguity in language. Cognition, 122               Rose, C., and Peng, V. (eds.), Findings of the Asso-
  (3):280–291, 2012.                                                   ciation for Computational Linguistics: EMNLP 2025,
                                                                       pp. 13954–13966, Suzhou, China, November 2025. As-
Poesio, M. Semantic ambiguity and perceived ambiguity.                 sociation for Computational Linguistics. ISBN 979-8-
  arXiv preprint cmp-lg/9505034, 1995.                                 89176-335-7. doi: 10.18653/v1/2025.findings-emnlp.
                                                                       750. URL https://aclanthology.org/2025.
Reiter, R. A logic for default reasoning. Artificial intelli-
                                                                       findings-emnlp.750/.
  gence, 13(1-2):81–132, 1980.
                                                                     Tomasello, M. The cultural origins of human cognition.
Reyle, U. Dealing with ambiguities by underspecification:              Harvard university press, 2009.
  Construction, representation and deduction. Journal of
  semantics, 10(2):123–179, 1993.                                    Urlana, A., Mishra, P., Roy, T., and Mishra, R. Controllable
                                                                       text summarization: Unraveling challenges, approaches,
Roberts, C. Information structure: Towards an integrated               and prospects - a survey. In Ku, L.-W., Martins, A.,
  formal theory of pragmatics. Semantics and pragmatics,               and Srikumar, V. (eds.), Findings of the Association
  5:6–1, 2012.                                                         for Computational Linguistics: ACL 2024, pp. 1603–
Savoldi, B., Gaido, M., Bentivogli, L., Negri, M., and                 1623, Bangkok, Thailand, August 2024. Association
  Turchi, M. Gender bias in machine translation. Transac-              for Computational Linguistics. doi: 10.18653/v1/2024.
  tions of the Association for Computational Linguistics, 9:           findings-acl.93. URL https://aclanthology.
  845–874, 2021.                                                       org/2024.findings-acl.93/.
                                                                     Vinker, Y., Tang, M., Hertzmann, A., Fan, J. E., Agrawala,
Savoldi, B., Bastings, J., Bentivogli, L., and Vanmassen-
                                                                       M., Chandra, K., Fu, H., and Schaldenbrand, P. Drawing
  hove, E. A decade of gender bias in machine translation.
                                                                       and sketching: Art, psychology, and computer graphics.
  Patterns, 6(6), 2025.
                                                                       In Proceedings of the Special Interest Group on Com-
Searle, J. R. Speech acts: An essay in the philosophy of               puter Graphics and Interactive Techniques Conference
  language. Cambridge university press, 1969.                          Frontiers, pp. 1–3, 2025.

Shannon, C. E. A mathematical theory of communication.               Wing, J. M. A specifier’s introduction to formal methods.
  The Bell system technical journal, 27(3):379–423, 1948.             Computer, 23(9):8–22, 2002.

Shannon, C. E. Prediction and entropy of printed english.            Zadrozny, W., Budzikowska, M., Chai, J., Kambhatla, N.,
  Bell system technical journal, 30(1):50–64, 1951.                    Levesque, S., and Nicolov, N. Natural language dialogue
                                                                       for personalized interaction. Communications of the ACM,
Shannon, C. E. et al. Coding theorems for a discrete source            43(8):116–120, 2000.
  with a fidelity criterion. IRE Nat. Conv. Rec, 4(142-163):
  1, 1959.                                                           Zaslavsky, N., Kemp, C., Regier, T., and Tishby, N. Ef-
                                                                       ficient human-like semantic representations via the In-
Sperber, D. and Wilson, D. Relevance: Communication                    formation Bottleneck principle. In Cognitively Informed
  and cognition, volume 142. Harvard University Press                  AI workshop at the 31st Conference on Neural Informa-
  Cambridge, MA, 1986.                                                 tion Processing Systems (NIPS), 2017. URL https:
                                                                       //arxiv.org/pdf/1808.03353.pdf.
Tang, N., Meininger, D., Xu, G., Shi, Y., Huang, Y., McMil-
  lan, C., and Li, T. J.-J. Naturaledit: Code modification           Zeng, Y., Lin, Z., and Patel, V. M. Sketchedit: Mask-
  through direct interaction with adaptive natural language            free local image manipulation with partial sketches. In
  representation, 2025. URL https://arxiv.org/                         Proceedings of the IEEE/CVF conference on computer
  abs/2510.04494.                                                      vision and pattern recognition, pp. 5951–5961, 2022.

                                                                12
                               Natural Language Should Not Fully Replace Formal Languages

Zhang, H., Yu, P. S., and Zhang, J. A systematic survey
  of text summarization: From statistical methods to large
  language models. ACM Computing Surveys, 57(11):1–41,
  2025.
Zhu, T., Liu, H., Jiang, Z., and Zheng, Z. Symbolic music
  generation with fine-grained interactive textural guidance.
  CoRR, 2024.

Zipf, G. K. Human Behaviour and the Principle of Least
  Effort. Addison-Wesley, 1949.




                                                                13
                                 Natural Language Should Not Fully Replace Formal Languages

A. Imperatives and Autonomy
Commands and requests highlight the role of listener autonomy in underspecification. Sperber & Wilson (1986) argue that
communication is not passive decoding but involves active inference about relevance to the listener’s goals, emphasizing the
listener as an agent. Barker (2010) models choice in imperatives (e.g., “take an apple or an orange”) with logic that accounts
for the listener’s resources and preferences.
Autonomy in communication can be understood through the ladder of specification: Strong autonomy corresponds to
indifferent underspecification: the speaker genuinely does not care which option the listener chooses and grants full
discretion. Weak autonomy corresponds to pragmatic underspecification with delegation: the speaker has implicit preferences
or trusts the listener to act in the speaker’s interest, but does not explicitly constrain the choice. This distinction has practical
implications for human-AI interaction: systems should distinguish between cases where user indifference grants genuine
autonomy versus cases where the system should infer and follow implicit user preferences.

B. Proof for Lemma 3.6
                                                                                             Pn
Proof. Let D = {p1 , p2 , . . . , pn } be a set of n domain distributions, and let p̄ = n1    i=1 pi denote the centroid (average)
distribution. We assume a uniform distribution over D.
The Jensen-Shannon divergence of the domain set is defined as:
                                                                          n
                                                                      1X
                                                JSD(D) = H(p̄) −            H(pi )                                                (8)
                                                                      n i=1

where H(·) denotes the Shannon entropy.
We begin by expanding the expected KL divergence:
                                                            n
                                                        1X
                              Ep∈D [DKL (p∥pNL )] =           DKL (pi ∥pNL )
                                                        n i=1
                                                            n
                                                                                                    !
                                                       1X              X
                                                     =       −H(pi ) −   pi (x) log pNL (x)                                       (9)
                                                       n i=1           x


Rearranging terms:
                                            n              n
                                         1X             1 XX
                                      =−       H(pi ) −          pi (x) log pNL (x)
                                         n i=1          n i=1 x
                                            n                   n
                                                                          !
                                         1X             X 1X
                                      =−       H(pi ) −            pi (x) log pNL (x)
                                         n i=1           x
                                                             n i=1
                                               n
                                         1X             X
                                      =−       H(pi ) −   p̄(x) log pNL (x)                                                     (10)
                                         n i=1          x


Now, we add and subtract H(p̄):
                                                    n
                                             1X                     X
                                    = H(p̄) −      H(pi ) − H(p̄) −      p̄(x) log pNL (x)
                                             n i=1                    x
                                                                                 !
                                                           X
                                    = JSD(D) + −H(p̄) −       p̄(x) log pNL (x)
                                                                  x
                                    = JSD(D) + DKL (p̄∥pNL )                                                                    (11)

which completes the proof.


                                                                 14
