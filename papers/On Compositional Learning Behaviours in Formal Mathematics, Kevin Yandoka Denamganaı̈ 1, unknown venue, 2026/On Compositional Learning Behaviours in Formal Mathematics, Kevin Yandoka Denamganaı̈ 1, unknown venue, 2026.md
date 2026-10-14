                                                       On Compositional Learning Behaviours in Formal Mathematics


                                                                                           Kevin Yandoka Denamganaı̈ 1


                                                                   Abstract                                       have achieved significant performance milestones (Xin et al.,
                                                Self-evolving scientific agents capable of conquer-               2025; Lin et al., 2025; Ren et al., 2025; Lin et al., 2026)
                                                ing the hard tail of formal mathematics require                   on whole-proof generation tasks by coupling deep neural
                                                Compositional Learning Behaviours (CLBs)—the                      architectures with intensive proof-tree search algorithms
arXiv:2605.28512v2 [cs.CL] 28 Jun 2026




                                                capacity to ground and recombine novel symbolic                   across verification environments such as Lean 4 (Zheng
                                                structures in context, beyond mere recombination                  et al., 2022; Yang et al., 2023; Tsoukalas et al., 2024).
                                                of prelearned atoms. We propose S2B-LM, an
                                                adaptation of the CLB-evaluating Symbolic Be-                     The Diagnostic Gap However, standard benchmarking
                                                haviour Benchmark that removes numerical pro-                     practices typically collapse multidimensional model traits
                                                cessing as a confound and adds chain-of-thought                   into a monolithic task-accuracy metric. This aggregation
                                                scaffolding to elicit rather than merely probe                    masks a critical distinction between shallow statistical pat-
                                                latent CLB competency. Cross-evaluating ten                       tern matching and genuine systematic abstraction. True
                                                Lean 4 theorem provers on CLB competency in                       autonomous self-evolution requires the acquisition of Com-
                                                S2B-LM and miniF2F whole-proof performance,                       positional Learning Behaviours (CLBs; Denamganaı̈ et al.
                                                we find correlational and causal evidence of our                  (2022))—the capacity of an agent to ground never-before-
                                                claim: First, a necessary-condition analysis via                  seen atomic elements from in-context evidence and recom-
                                                quadrant test yields p = 0.004, with model scale                  bine them systematically to resolve novel structural config-
                                                being ruled out as a confound. Second, extract-                   urations within the same episode, going beyond the mere
                                                ing a CLB-encoding activation direction from                      recombination of prelearned atoms (see also Kim & Linzen
                                                DeepSeek-Prover-V2-7B using S2B-LM traces via                     (2020)). Without explicit diagnostic benchmarks separat-
                                                Contrastive Activation Addition and applying it                   ing across skills, such as CLBs, or structural compliance,
                                                during miniF2F whole-proof generation on the                      being separated from search capacity, it remains ambigu-
                                                AIME subset, CLB suppression collapses solve                      ous whether state-of-the-art provers are acquiring authentic
                                                rate from 32.3% to 2.9%, without loss of coher-                   symbolic processing capabilities or are merely leveraging
                                                ence, while suppressing a random activation di-                   expansive compute budgets to overfit to localized tactical
                                                rection of equal magnitude leaves it at 31.9%. To-                distributions that can be seen in formal proving benchmarks.
                                                gether, these results show that CLB competency
                                                                                                                  Following Yang et al. (2025c)’s open challenges and future
                                                is necessary but not sufficient for the hard tail of
                                                                                                                  directions, the aim of this paper is to provide a “controlled
                                                formal mathematical verification.
                                                                                                                  stud[y] on synthetic benchmarks for diagnosing reasoning
                                                                                                                  failures” and highlight a way to “improve the model archi-
                                         1. Introduction                                                          tecture for mathematical reasoning”.

                                         Formal Verification and Self-Evolving Agents A foun-                     We acknowledge the Symbolic Behaviour Benchmark (De-
                                         dational pillar in the development of self-evolving scientific           namganaı̈ et al., 2022) as a crucial diagnostic tool to eval-
                                         agents is the reliance on formal verification loops, where               uate the capability of state-of-the-art formal theorem prov-
                                         automated theorem provers act as execution environments                  ing LMs to perform CLBs. However, we note that the
                                         to provide unyielding reward signals for iterative improve-              original version of the benchmark comes with many con-
                                         ment. Driven by this paradigm, frontier language models                  founders when used to evaluate LMs. Firstly, the Symbolic
                                                                                                                  Behaviour Benchmark relies heavily on numerical values
                                            1
                                             Work conducted as an Independent Researcher during the revi-         (cf Section 3.1), whereas LMs notoriously lack numerical
                                         sion phase of a PhD at the University of York.. Correspondence to:       understanding and processing abilities (NUPA - Yang et al.
                                         Kevin Yandoka Denamganaı̈ <kevin.denamganai@york.ac.uk>.                 (2025b)). Secondly, the Symbolic Behaviour Benchmark
                                         The 3 rd AI for Math Workshop at the 43rd International Confer-          does not account for the competence-performance distinc-
                                         ence on Machine Learning (ICML), Seoul, South Korea, 2026.               tion ( Firestone (2020) - cf. Section 2.3), which means that
                                         Copyright 2026 by the author(s).                                         a zero-shot evaluation of CLBs without an adequate rea-

                                                                                                              1
                                On Compositional Learning Behaviours in Formal Mathematics

soning scaffold risks conflating a genuine absence of CLB              sary for Olympiad-tier theorem proving.
competency with a mere performance failure—an important
                                                                       Contributions.
confound when interpreting ZSCT scores for LMs.
                                                                        1. We provide empirical findings that the capability to
S2B-LM and Evaluation Protocol To address these con-
                                                                           adapt to novel compositional structures (i.e. recep-
founders, we propose S2B-LM, an extension of the S2B
                                                                           tivity aspects of performing CLBs) is necessary, but
that (i) replaces the continuous stimulus domain with a
                                                                           not sufficient, for unlocking the hard tail of formal
categorical one, removing floating-point segregation as a
                                                                           mathematical verification.
confound on measured CLB competency, and (ii) introduces
a rule-based verbalizer that generates chain-of-thought ex-             2. We propose the S2B-LM as an extension of the Sym-
emplars from the episode’s sync rounds, scaffolding the                    bolic Behaviour Benchmark that more precisely eval-
elicitation of latent CLB competency rather than merely                    uates the capabilities of LMs to perform CLBs, by
probing it. We report the adj-ZSCT (adjusted Zero-Shot                     introducing two features to control for distinct con-
Compositional Test score), which maps the raw ZSCT onto                    founders: a categorical stimulus domain to remove
an ability-above-chance scale in [0, 100] by removing the                  NUPA as a confound, and a rule-based verbalizer
intrinsic 50% random-guessing floor. We cross-evaluate ten                 providing chain-of-thought scaffolding to address the
state-of-the-art formal theorem proving models, projecting                 competence–performance distinction in LMs.
each onto adj-ZSCT alongside a formal verification perfor-
mance metric. While several benchmarks provide valuable
complementary perspectives—including LeanDojo (Yang
                                                                       2. Background
et al., 2023) and PutnamBench (Tsoukalas et al., 2024)—we              2.1. Compositional Behaviours vs Compositional
focus on miniF2F whole-proof test-split pass@32 (Zheng                      Learning Behaviours
et al., 2022) as it is the evaluation setting we found to be the
most consistently reported across papers; notably, 80 of its           Definitions. Denamganaı̈ et al. (2022) define Composi-
244 test-split problems (32.8%) are drawn from competitive             tional Behaviours (CBs) as the capacity to generalise from
or Olympiad tiers (AMC, AIME, IMO), providing suffi-                   combinations of trained-on atomic components to novel
cient hard-tail coverage to expose the structural bottleneck           re-combinations of those same atoms: the entire vocabulary
we investigate. We then submit the resulting evaluation                is prelearned, and generalisation consists of applying known
pool to a necessary-condition quadrant test, and comple-               compositional rules to known elements in unseen arrange-
ment the correlational analysis with a causal intervention             ments. Compositional Learning Behaviours (CLBs) extend
via Contrastive Activation Addition on S2B-LM traces ap-               this to an online regime: the agent must generalise from a
plied during AIME proof search.                                        handful of in-context examples of never-before-seen atomic
                                                                       components to novel re-combinations of those atoms, all
                                                                       within a single episode. The within-episode grounding re-
Findings We find that CLB competency is a necessary
                                                                       quirement is what distinguishes CLBs from standard compo-
but not sufficient condition for elite formal mathematics per-
                                                                       sitional generalisation benchmarks, which test training-time
formance. We perform a necessary-condition analysis using
                                                                       generalisation over a prelearned vocabulary.
a quadrant test, which dichotomises each axis at its empiri-
cal median and tests for depletion of aforbidden cell (high           Code generation vs. Lean proof generation: CB and
miniF2F, low adj-ZSCT) over all 10      5 = 252 label place-           CLB in practice. Standard code generation is predomi-
ments. This test finds the forbidden cell empty (p = 0.004):           nantly a CB task: a model trained on Python generalises
no model reaches the Olympiad-level tier without measur-               by composing known identifiers—sorted(), list compre-
able CLB competency, while CLB competency alone does                   hensions, lambda expressions—into novel arrangements,
not determine ranking within that tier. Model scale is ruled           recombining a fully prelearned vocabulary according to
out as a confound: DeepSeek-Prover-V2-7B (7B parameters)               known rules. Lean 4 proof generation introduces a quali-
clears the Olympiad threshold at 75.6% miniF2F, demon-                 tative shift. Lean’s reflexive type-checking kernel acts as
strating that scale is not a necessary condition for the hard          an unyielding execution environment: every proof step is
tail. Beyond this correlational evidence, we seek to es-               machine-verified, leaving no room for syntactic hallucina-
tablish causality by extracting a CLB-encoding direction               tion. When a self-evolving prover or a human collaborator
from DSP-V2-7B via Contrastive Activation Addition on                  introduces a new tactic, a freshly-defined auxiliary lemma,
S2B-LM traces and apply it during miniF2F whole-proof                  or a novel intermediate proposition—analogous to a mathe-
generation on the AIME subset: CLB suppression collapses               matician coining a fresh binary relation ≲ and illustrating
solve rate from 32.3% to 2.9% while a random direction of              its semantics across two or three in-context examples—that
equal magnitude leaves it at 31.9%, providing direct causal            object is absent from the model’s pretraining weights and
evidence that the CLB representational direction is neces-             cannot be recovered by memorisation. Grounding it from in-

                                                                   2
                              On Compositional Learning Behaviours in Formal Mathematics

context evidence and deploying it correctly in a novel proof       distinction (Firestone, 2020), familiar from comparative
context requires decoding the new convention (receptivity)         psychology where subjects cannot be given explicit instruc-
and recombining it with prelearned primitives in unseen ar-        tions. Applied to CLB evaluation, an LM may possess the
rangements (compositionality)—the full CLB requirement.            underlying receptive CLB competency yet score near chance
Thus, while standard code generation and low-to-medium-            if the prompting context does not adequately scaffold its
difficulty theorem proving are accessible via CB capacity          elicitation. Following Lampinen (2024), we address this
alone, advancing into the hard tail of formal mathematical         by adapting the prompting context to a few-shot chain-of-
verification demands within-episode symbolic acquisition           thought regime that elicits rather than merely probes latent
that current training paradigms do not explicitly cultivate.       competency (cf. Section 3.2); Section 3.3 provides an abla-
                                                                   tion study confirming this design choice.
CLB as symbolic behaviour. Santoro et al. (2021) argue
that symbolic behaviours do not inhere in agents intrinsi-
cally but exist only in relation to an interpreter: a system       2.4. Symbolic Behaviour Benchmark
exhibits symbolic behaviour when another agent treats its          Santoro et al. (2021) argue that symbolic behaviours do not
outputs as symbols. Among the different aspects of sym-            reside in agents intrinsically but exist only in relation to
bolic behaviours, this work focuses on two (Denamganaı̈            an interpreter: a system exhibits symbolic behaviour when
et al., 2022): receptivity—the capacity to decode a novel          another agent treats its outputs as symbols. The Symbolic
symbolic convention introduced by a speaker agent—and              Behaviour Benchmark (S2B; Denamganaı̈ et al. 2022) oper-
constructivity—the capacity to produce a novel convention          ationalises this by requiring a speaker agent and a listener
that a listener agent can decode. The S2B operationalises          agent to acquire and deploy a shared symbolic code within
both by swapping the role assigned to the tested system            Meta-Referential Games (Meta-RGs), a meta-learning ex-
(cf. Section 2.4); this work focuses exclusively on the re-        tension of referential games in which the latent symbolic
ceptivity axis. We justify in Section 5.1 why a receptive          structure and the communication vocabulary are freshly
bottleneck necessarily collapses downstream constructivity,        randomised at every episode.
so that receptivity alone is a sufficient diagnostic target.
                                                                   Receptivity and constructivity. The S2B evaluates two
                                                                   aspects of CLBs by swapping the role assigned to the tested
2.2. Formal Mathematical Reasoning & Formal
                                                                   system. Placing it in the listener role—paired with a fixed
     Theorem Proving
                                                                   posdis-compositional rule-based speaker (Chaabouni et al.,
Learning-based automated theorem proving in Lean 4 has             2020)—isolates receptivity: the capacity to decode an out-of-
advanced rapidly: frontier whole-proof generation models—          distribution symbolic convention. Placing it in the speaker
DSP-V1.5 (Xin et al., 2025), Goedel-Prover (Lin et al.,            role—paired with a rule-based listener—isolates construc-
2025), DSP-V2 (Ren et al., 2025), and Goedel-Prover-               tivity: the capacity to produce a novel symbolic convention.
V2 (Lin et al., 2026)—push miniF2F pass@32 from 48%                In this work we focus exclusively on the receptivity axis.
to 88% via SFT on large formal corpora combined with
                                                                   Meta-RG structure and ZSCT. Each Meta-RG
Monte Carlo tree search or RL-based subgoal decompo-
                                                                   episode is governed by a latent symbolic structure
sition. Despite these gains, all operate over a fixed, pre-
                                                                   (d(1), . . . , d(Ndim )), where d(i) is the number of possible
learned tactic vocabulary: they recombine known atomic
                                                                   values on latent dimension i, and by a freshly sampled
proof steps (CB), rather than acquiring new symbolic con-
                                                                   random vocabulary permutation that bijectively re-indexes
ventions in context (CLB). We evaluate on miniF2F-test
                                                                   the speaker’s tokens before they reach the listener, pre-
whole-proof pass@32 (Zheng et al., 2022) (Table 2); while
                                                                   venting the listener from exploiting an episode-invariant
LeanDojo (Yang et al., 2023) and PutnamBench (Tsoukalas
                                                                   code. The posdis-speaker encodes latent value li at message
et al., 2024) offer complementary perspectives, our choice
                                                                   position i as token ti = li + 1 (an offset-1 positional
is guided by the consistent availability of pass@32 results
                                                                   code); the permutation then scrambles these indices, so the
across all ten evaluated models, its single-pass generation
                                                                   listener must rediscover the token-to-value mapping from
regime comparable to the S2B-LM listener evaluation, and
                                                                   scratch at every episode. Each game in an episode unfolds
its difficulty span—MATH levels 1–5 to IMO, with 80 of
                                                                   over N communication rounds followed by the listener’s
244 test problems from AMC/AIME/IMO—providing the
                                                                   decision; after each game a dedicated sync round exposes
hard-tail coverage needed to expose a CLB bottleneck.
                                                                   the speaker’s exact target stimulus to the listener uncondi-
                                                                   tionally, providing a ground-truth token-to-value update
2.3. How to compare human and AI capabilities ?                    regardless of whether the listener’s decision was correct.
A fundamental challenge in AI evaluation is distinguishing         Episodes unfold in two sequential phases. In the supporting
a lack of capability from a failure to demonstrate it un-          phase, games are played until every value on every
der specific test conditions—the competence–performance            dimension has appeared in at least S full Ndim -dimensional


                                                               3
                                On Compositional Learning Behaviours in Formal Mathematics

stimulus vectors (no atomic value is ever presented in                         SCS           Latent Symbolic Structure   Categorical
isolation). The querying/ZSCT phase then presents a
                                                                                        ∼N       Dim 0: d(0)=3,
held-out set of stimulus combinations—multi-dimensional                       −0.73
                                                                                                vegetables, l(0)=2
                                                                                                                           potato
arrangements of those same values that were withheld
                                                                                        ∼N       Dim 1: d(1)=5,
as targets during the supporting phase—and accuracy on                          0.41
                                                                                                  colors, l(1)=1            blue
these games defines the Zero-Shot Compositional Test
                                                                                        ∼N       Dim 2: d(2)=3,
(ZSCT) metric. Success requires the agent to generalise                         0.15                                        circle
                                                                                                 shapes, l(2)=0
systematically to novel combinatorial arrangements it has
never encountered as targets.                                         Figure 1. SCS vs. categorical encoding of the same latent stim-
                                                                      ulus (l(0)=2, l(1)=1, l(2)=0). The SCS scheme maps each
Binding problems and the SCS representation. Stimuli                  latent value to a Gaussian-sampled float (∼ N ), requiring floating-
are encoded using the Symbolic Continuous Stimulus (SCS)              point segregation as a prerequisite to CLB evaluation. The
scheme: each dimension i partitions [−1, +1] into d(i) sec-            categorical scheme replaces floats with named tokens, remov-
tions, and a stimulus entry is a real number sampled from             ing that confound while preserving the binding problem.
                           2
the Gaussian N (µl(i) , σl(i)  ) associated with latent value
l(i). The shape invariance property ensures that every SCS
stimulus is a vector in [−1, +1]Ndim regardless of the d(i)
values, so the structure of the current episode cannot be             is a human-readable word. A fixed registry of ten concept
read off from any single observation: the agent must seg-             classes is defined—vegetables, fruits, colors, shapes, ani-
regate floating-point coordinates over multiple consecutive           mals, countries, metals, planets, sports, instruments—each
supporting-phase games to infer both (i) how many distinct            containing up to ten named items (e.g. colors 7→ {red, blue,
values are active per dimension and (ii) which Gaussian clus-         green, yellow, . . . }). At the start of each episode, Ndim cate-
ter each coordinate belongs to. Sub-problem (i) is the less           gories are sampled without replacement from the registry,
difficult component of the binding problem; sub-problem               and for each selected category i, exactly d(i) ∈ [Vmin , Vmax ]
(ii) is the harder, numerically demanding component. While            items are drawn uniformly, forming the episode’s latent
this domain-agnostic design is appropriate for RL agents, it          value set for that dimension. A stimulus on dimension i
introduces a systematic confounder for LMs, whose poor nu-            with latent value l(i) is then presented as the corresponding
merical understanding and processing abilities (Yang et al.,          item name rather than a continuous float. The full Ndim -
2025b) directly suppress ZSCT scores independently of any             dimensional stimulus is an ordered tuple of natural language
CLB competency.                                                       tokens—e.g. (carrot, blue, circle) for a latent symbolic
                                                                      structure with three dimensions using categories vegetables,
                                                                      colors, shapes.
3. Method: Adapting the Symbolic Behaviour
                                                                      Preservation of the Binding Problem. The categorical sub-
   Benchmark
                                                                      stitution preserves the binding problem structure. The set of
3.1. Adapting the Domain                                              active items per dimension is unknown to the tested model
                                                                      a priori: although each item name is semantically famil-
The original S2B represents stimuli using the Symbolic Con-           iar, the mapping from category items to latent positions is
tinuous Stimulus (SCS) scheme (Denamganaı̈ et al., 2022).             randomised at every episode. The model must therefore in-
Given a latent symbolic structure with Ndim dimensions                tegrate evidence across the supporting-phase stimuli to infer
described by the tuple (d(1), . . . , d(Ndim )), a stimulus is        which items are active on each dimension and in which com-
a vector in [−1, +1]Ndim : the i-th entry is a real number            binatorial arrangement—the same latent-structure discovery
                                         2
sampled from the Gaussian N (µl(i) , σl(i)  ) associated with         challenge as in the SCS domain, now expressed entirely in
the currently-selected latent value l(i) ∈ {1, . . . , d(i)} on       natural language tokens. The train/test combinatorial split
dimension i. Thanks to the shape invariance property (cf.             strategy and ZSCT evaluation protocol are identical to the
Section 2.4), this scheme instantiates a domain-agnostic              original S2B (cf. Section 2.4).
binding problem that is appropriate for RL agents. However,
for LMs, the Gaussian-sampled real values are a system-               3.2. Providing Few-Shot Exemplars via a Rule-based
atic confounder: numerical understanding is not required                   Listener Verbalizer
for compositional reasoning, yet low NUPA (Yang et al.,
2025b) directly suppresses measured ZSCT scores, break-               A second key design objective of S2B-LM is to address the
ing the internal validity of the benchmark as a diagnostic of         competence–performance distinction (cf. Section 2.3): a
CLBs.                                                                 tested LM may possess the underlying CLB competency
                                                                      yet score near chance if the prompting context does not
The Categorical Domain. We replace the SCS representa-                adequately scaffold its elicitation. We therefore provide
tion with a categorical domain in which every latent value            the tested LM with few-shot chain-of-thought exemplars

                                                                  4
                                          On Compositional Learning Behaviours in Formal Mathematics

  S2B-LM: one supporting-phase game (Ndim = 3, instruments, sports, veg-               Table 1. Ablation results for DSP-V2-7B across benchmark con-
  etables)                                                                             figurations. ZSCT scores reported as mean ± std. err. over 4
  [User — Sync & Game #1]
                                                                                       random seeds. The original S2B uses the SCS domain with no
  Sync: speaker observed [piano, swimming, eggplant] at game #0.                       CoT scaffold; S2B-LM uses the categorical domain with 10-shot
  Your decision was similar—correct.                                                   chain-of-thought exemplars.
  At game #1, you observe [piano, golf, pepper]. Speaker’s message:
  [8, 11, 13].                                                                          Configuration                     ZSCT (%)     Adj. ZSCT
  Same latent meaning? Answer 0 (Yes) or 1 (No).
                                                                                        S2B (SCS, 0-shot)                 57.9 ± 5.7      15.8
  [Listener — Game #1]                                                                  Categorical + 0-shot              40.0 ± 8.5      0.0
  Let’s think step by step and leverage past games.
                                                                                        S2B-LM (Categorical + 10-shot)    87.0 ± 4.1      74.0
  From the last game syncing, we can learn that: symbol 8 at pos 0 → pi-
  ano ; symbol 5 at pos 1 → swimming ; symbol 6 at pos 2 → eggplant.
  In the current game, if the speaker were observing a similar stimulus as ours,
  [piano, golf, pepper], then: at pos 0, piano → symbol 8 (from game #0) ; at          2022b) that prime the LM to replicate the verbalizer’s com-
  pos 1, golf has not been observed yet ; at pos 2, pepper has not been observed
  yet.                                                                                 positional inference on the unseen querying-phase stimuli.
  Since the speaker’s message is [8, 11, 13], yield 1/3 matches, they are
  likely observing a different stimulus. Answer: 1                                     Each verbalized trace follows a three-step template: (i) sync
                                                                                       summary—what the most recent sync round revealed about
Figure 2. Excerpt of one S2B-LM supporting-phase game illus-
                                                                                       token-to-value correspondences; (ii) inverse prediction—
trating the verbalizer’s sync-summary → inverse-prediction →                           what message the speaker would have sent had it observed
match-comparison reasoning chain. Full conversation in Figure 8                        the same stimulus as the listener, derived by inverting
(Appendix B).                                                                          V; (iii) match comparison—how many positions of the
                                                                                       actual message agree with the prediction, yielding the
                                                                                       same/different decision. By exposing both the accumulated
that supply the structured reasoning context needed to elicit                          mapping evidence and the compositional reasoning chain
rather than merely probe its latent CLB competency. We                                 used to reach each answer, these traces prime the tested
construct these exemplars via a hypothesis-tracking rule-                              LM to replicate the same inference pattern on the unseen
based listener verbalizer, a dedicated agent that monitors the                         querying-phase stimuli.
episode and generates human-readable reasoning traces in
real time from the sync rounds of the S2B (cf. Section 2.4).                           3.3. Validation via Ablation Study
The sync round is the game mechanism that unconditionally
reveals the speaker’s exact target stimulus after every game,                          We show via an ablation study that our extended version of
making it a natural and game-internal source of ground-                                the S2B has increased internal validity towards evaluating
truth evidence; the verbalizer converts this evidence into                             CLBs in tested LMs.
interpretable reasoning steps that are appended to the LM’s                            Because the raw ZSCT operates with an intrinsic 50%
context before each game decision (see Algorithm 1 in Ap-                              random-guessing floor, we report the adjusted ZSCT (adj-
pendix A for the full episode loop; Figure 2 for a compact                             ZSCT), which maps ZSCT onto a pure ability-above-chance
illustrative game exchange; and Figure 8 in Appendix B for                             scale in [0, 100]:
a complete supporting-phase conversation).                                                                                     
                                                                                                                    ZSCT − 50
In each supporting-phase game, the tested LM—acting as                                         adj-ZSCT = max 0,                  × 100     (1)
                                                                                                                     100 − 50
listener—receives two inputs: its own stimulus, an ordered
tuple of natural-language category items such as [piano,                               Table 1 reports ZSCT and adj-ZSCT scores for DeepSeek-
swimming, eggplant], and the posdis-speaker’s mes-                                     Prover-V2-7B under three benchmark configurations, evalu-
sage, an integer-token sequence such as [8, 5, 6]. The                                 ated over 4 random seeds. Using the smallest model in our
LM must decide whether both agents are observing stimuli                               suite acts as a conservative lower bound: if the full S2B-LM
with the same latent meaning. The sync round that follows                              design successfully elicits CLB competency at 7B, larger
unconditionally reveals the speaker’s exact target stimulus,                           models—which exhibit stronger in-context learning capabil-
providing ground-truth evidence on the token-to-value corre-                           ities (Brown et al., 2020; Wei et al., 2022a)—can only do
spondence at every message position regardless of whether                              better.
the LM’s decision was correct.
                                                                                       The three configurations isolate the contribution of each de-
The rule-based verbalizer maintains a value map V :                                    sign choice. First, the original S2B (SCS, 0-shot) yields
(pos, tok) 7→ {val 7→ count} that accumulates this sync-                               only 57.9%—marginally above the 50% guessing floor
derived evidence across all preceding games in the episode.                            (adj-ZSCT = 15.8)—consistent with NUPA (Yang et al.,
Before each game, the current state of V is converted into                             2025b) suppressing measured CLB scores independently
a natural-language reasoning trace appended to the LM’s                                of any compositional competency. Second, switching to
context, providing chain-of-thought exemplars (Wei et al.,                             the categorical domain while retaining zero-shot prompt-

                                                                                   5
                                        On Compositional Learning Behaviours in Formal Mathematics

Table 2. Evaluation results: adj-ZSCT (S2B-LM receptive listener CLB competency, ability above chance) and miniF2F whole-proof
test-split accuracy (Pass@32). ZSCT scores reported as mean ± std. err. over 8 random seeds. †: model accessed via API.

 Model                                         Size   Base Model                                                          ZSCT (%)      Adj. ZSCT ([0 − 100])   miniF2F test Pass@32 (%)
 DeepSeek-Prover-V1 (Xin et al., 2024)          7B    DeepSeekMath-7B (Shao et al., 2024)                                  47.6 ± 6.7             0.0                     46.1
 DeepSeek-Prover-V1.5-SFT (Xin et al., 2025)    7B    DSP-V1.5-Base (Xin et al., 2025)                                     56.0 ± 1.6            12.0                     48.2
 DeepSeek-Prover-V1.5-RL (Xin et al., 2025)     7B    DSP-V1.5-SFT (Xin et al., 2025)                                      56.9 ± 3.3            13.8                     50.0
 Goedel-Prover-SFT (Lin et al., 2025)           7B    DSP-V1.5-Base (Xin et al., 2025)                                     58.1 ± 3.0            16.3                     57.6
 Goedel-Prover-DPO (Lin et al., 2025)           7B    Goedel-Prover-SFT (Lin et al., 2025)                                 55.3 ± 3.4            10.6                     60.3
 Goedel-Prover-V2-8B (Lin et al., 2026)         8B    Qwen3-8B (Yang et al., 2025a)                                        75.0 ± 7.5            50.0                     84.6
 Goedel-Prover-V2-32B† (Lin et al., 2026)      32B    Qwen3-32B (Yang et al., 2025a)                                      65.2 ± 6.4             30.4                     88.1
 DeepSeek-Prover-V2-7B (Ren et al., 2025)       7B    DSP-V1.5-Base-7B (Xin et al., 2025)                                  89.8 ± 2.7            79.6                     75.6
 DeepSeek-Prover-V2-671B† (Ren et al., 2025)   671B   DeepSeek-V3-Base (DeepSeek-AI et al., 2025)                         100.0 ± 0.0            100.0                    82.4
 Kimina-Prover† (Wang et al., 2025b;a)         72B    Qwen2.5-72B (Qwen et al., 2025)                                     97.4 ± 1.6             94.8                     84.0




ing (Categorical + 0-shot) drops performance below chance




                                                                                              miniF2F Test Accuracy (%)
                                                                                                                          100                GP-V2-32B
(40.0%, adj-ZSCT = 0): without a CoT scaffold to elicit                                                                                        GP-V2-8B
                                                                                                                                                                DP-V2-671B
the latent reasoning strategy, the model fails to exploit                                                                   80                                         KP-72B
                                                                                                                                                                DP-V2-7B
the now-interpretable stimuli, illustrating the competence–                                                                 60GP-DPO     GP-SFT
                                                                                                                                  DP-V1.5-RL
                                                                                                                                     DP-V1
performance distinction. Third, the full S2B-LM design                                                                                   DP-V1.5-SFT
                                                                                                                            40
(categorical + 10-shot chain-of-thought) recovers strongly
to 87.0% (adj-ZSCT = 74.0), demonstrating that the                                                                          20
verbalizer-generated exemplars successfully surface the
                                                                                                                              0
model’s underlying CLB competency. Together, these re-
sults confirm that both design choices—domain substitution                                                                         0     20    40     60    80 100
and CoT scaffolding—are necessary; neither alone suffices.                                                                        Adj. ZSCT: Ability Above Chance (%)

                                                                                    Figure 3. Empirical scatter of adj-ZSCT against miniF2F accuracy.
4. Experimental Results                                                             The adj-ZSCT axis captures structured receptive CLB capability
                                                                                    adjusted above the 50% random-guessing baseline.
Experimental setup. miniF2F results report whole-proof
test-split accuracy under Pass@32. S2B-LM evaluations use
Ndim = 3 latend dimensions with Vmin = 3 and Vmax = 5                               p-value of p = 0.004, this result is establishing CLB com-
values per latent dimension, number of object-centric sam-                          petency as a necessary condition for crossing the Olympiad-
ples O = 1 (the categorical domain does not support object-                         performance threshold. We report on further complementary
centric sampling), and number of shots S = 1 (every atomic                          correlational evidence in Appendix C.
element appears in at least one target stimulus before the
querying phase begins). All reported statistics are com-                            Limitations. Throughout, we rely exclusively on exact
puted over 8 random seeds per model. Adj-ZSCT scores are                            permutation methods rather than parametric or asymptotic
computed via Equation 1.                                                            estimators, as the small evaluation pool (N = 10) ren-
                                                                                    ders standard asymptotic tools structurally invalid. We pro-
Table 2 logs the evaluation results across the evaluated                            vide further statistical rationale in Appendix D. A compet-
model suite. Figure 3 visualizes the empirical scatter of                           ing explanation is model scale: larger models may jointly
adj-ZSCT against miniF2F accuracy.                                                  drive both adj-ZSCT and miniF2F performances. Crucially,
                                                                                    however, DeepSeek-Prover-V2-7B (7B parameters) achieves
4.1. Correlational Evidence                                                         75.6% miniF2F—placing it in the high-performance half—
                                                                                    while remaining a small model. This shows that scale is
We perform a necessary-condition analysis via a quadrant
                                                                                    not a necessary condition for the hard tail. However, the
test: each axis is dichotomised at its empirical median (adj-
                                                                                    current result is correlational only. Thus, in the next section,
ZSCT median = 23.3; miniF2F median = 67.95%), and
                                                                                    we turn to causal evidence to strengthen the CLB account
we test whether the forbidden cell—high miniF2F with low
                                                                                    beyond correlation.
adj-ZSCT—is depleted relative to random pairings. Sig-
nificance is assessed via a one-sided   Fisher’s exact test by
                                                                                    4.2. Causal Evidence
exact enumeration of all 10
                             
                           5   = 252  high-performance   label
placements (margins fixed). Figure 3 displays these median                          CLB-encoding direction via CAA. To move beyond corre-
thresholds as dashed reference lines.                                               lation, we extract a CLB-encoding activation direction from
In the observed data, the forbidden cell is empty: no model                         DeepSeek-Prover-V2-7B using Contrastive Activation Addi-
achieves high miniF2F with low adj-ZSCT. With a resulting                           tion (CAA), following Turner et al. (2023) and Rimsky et al.
                                                                                    (2024). For each querying-phase test game we teacher-force

                                                                                6
                                  On Compositional Learning Behaviours in Formal Mathematics

  Correct verbalization (positive)                                          Corrupted verbalization (negative)
  Let’s think step by step and leverage                                    Let’s think step by step and leverage
  past games.                                                              past games.
  From the last game syncing, we can learn                                 From the last game syncing, we can learn
  that: symbol 3 at pos 0 → violin ;                                       that: symbol 3 at pos 0 → trumpet ;
  symbol 5 at pos 0 → trumpet ; symbol 7                                   symbol 5 at pos 0 → violin ; symbol 7
  at pos 1 → football.                                                     at pos 1 → football.
  In the current game, if the speaker were                                 In the current game, if the speaker were
  observing a similar stimulus as ours,                                    observing a similar stimulus as ours,
  [violin, football], then: at pos 0,                                      [violin, football], then: at pos 0,
  violin → symbol 3 (from game #2) ;                                       violin → symbol 5 (from game #1) ;
  at pos 1, football → symbol 7 (from                                      at pos 1, football → symbol 7 (from
  game #1).                                                                game #1).
  Since the speaker’s message is [3, 7],                                   Since the speaker’s message is [3, 7],
  yield 2/2 matches, they are likely                                       yield 1/2 matches, they are likely
  observing a similar stimulus.                                            observing a different stimulus.
  Answer: 0                                                                Answer: 1

Figure 4. Synthetic example (Ndim = 2) of a matched teacher-forced pair used to extract vCLB . Both verbalizations share the identical game
structure (message [3, 7], listener stimulus [violin, football]). The correct trace (left) uses the true hypothesis map and predicts
a 2/2 match, yielding decision 0. The corrupted trace (right) uses a cyclically shifted binding map at pos 0 (symbol 3 → trumpet,
symbol 5 → violin) — the text is surface-coherent but the inverse prediction at pos 0 is wrong, reducing to 1/2 matches and
flipping the decision to 1. The per-layer mean residual over each reasoning span is subtracted (correct − corrupted) to obtain the CLB
activation direction.


the model with two verbalizations over the identical game
                                                                                      100                                        100
structure (same symbolic stimulus and speaker message): a
                                                                        S2B-LM ZSCT (%)


                                                                                          90




                                                                                                                                  incoherence %
positive trace produced by the correct rule-based hypothesis                                                                     80
tracker (with the true value↔symbol binding map accumu-
                                                                                          80                                     60
lated from sync rounds), and a negative trace produced by
a corrupted tracker whose binding map has been deranged                                   70                                     40
                                                                                                                      chance
by a cyclic shift—the trace is surface-coherent but reasons
                                                                                          60                          CLB
from wrong hypotheses, producing wrong inverse predic-                                                                orthogonal 20
tions and ultimately a wrong listener decision (see Figure 4                              50                          random
                                                                                               4    3      2     1     0        10
for an illustration). Because the prompt context is identical
across the pair it cancels in the difference. Only the CLB
                                                                                                   (steering coefficient)
reasoning is contrasted between the two traces. The per-
layer mean residual-stream activation over each reasoning               Figure 5. S2B-LM dosage curve for DSP-V2-7B under CLB CAA
                                                                        steering (α on the x-axis), with n = 3 random seeds per setting.
span is computed in a matched forward pass, and vCLB is
                                                                        Left y-axis: ZSCT (%); right y-axis: mean output coherence. CLB
the weighted mean of (correct − corrupted) differences over             suppression (α < 0) monotonically drives ZSCT toward the 50%
all matched pairs across episodes. We record it only over               guessing floor while coherence remains marginally intact, while
the last quarter of the model’s layers (i.e. the 7 last layers          control directions are flat across the same range.
of DeepSeek-Prover-V2-7B). At inference time, α · vCLB
is added to the residual stream at each token, where α > 0              output coherence as the fraction of generated proofs that are
amplifies and α < 0 suppresses the CLB direction.                       well-formed Lean 4—either proven correct or syntactically
                                                                        valid but unproven (i.e. free of parse or elaboration errors)—
Validation on S2B-LM. Figure 5 shows the ZSCT dosage                    as opposed to outputs containing syntax errors or empty
curve as α is swept from −4 to +1. CLB steering produces a              extractions. The coherence barplot (Figure 5) confirms that
monotone causal response: suppression at α = −4 reduces                 CLB suppression does not degrade output coherence: the
ZSCT from 92.6% (adj-ZSCT = 85.2) at baseline to 57.2%                  fraction of well-formed outputs remains stable across all
(adj-ZSCT = 14.4), near the 50% guessing floor, while mild              steering magnitudes, ruling out the confound that perfor-
amplification at α = +1 yields 95.2% (adj-ZSCT = 90.4).                 mance drops stem from garbled generations rather than from
Two control conditions—an orthogonal direction (a random                suppressed CLB competency.
vector projected to be orthogonal to vCLB ) and a random
direction—show flat responses across the same α range, es-              Transfer to AIME theorem proving. Having validated
tablishing the specificity of the CLB direction. We measure             that vCLB selectively modulates CLB competency in S2B-
                                                                        LM, we apply the same CLB-encoding CAA vector during

                                                                    7
                                               On Compositional Learning Behaviours in Formal Mathematics

                                                                                                                0.6
                         1.0                                                                  =0
solve rate (Wilson 95% CI)
                                                                                             CLB
                                                                                              = 3               0.5
                         0.8                                                                 CLB
                                                                                              =+1
                                                                                             random             0.4




                                                                                                      mean ± s.e.
                                                                                              = 3
                         0.6                                                                 random
                                                                                              =+1               0.3
                         0.4
                                                                                                                0.2

                         0.2                                                                                    0.1

                         0.0                                                                                    0.0   =0   CLB CLB random random
                         _p1 _p2 _p3 _p1 _p7 _p5 _p8 _p8 p15 _p4 _p9 _p3 _p7 _p9 p11                                       = 3 =+1 = 3 =+1
                  _ 1 983_1983_1983_1984_1984_1987_1988_19891990_ _1990_1991_1994_1995_19971999_
                 e e e e e e e e _ e e e e e _
              aim aim aim aim aim aim aim aim aime aim aim aim aim aim aime
      Figure 6. Per-problem (left) and aggregate (right) solve rates (pass@32) under CLB and random CAA steering applied to DSP-V2-7B.
      CLB suppression (α = −3) collapses solve rate from 32.3% to 2.9%; random suppression leaves it at 31.9%.


          1.0                  0.05                                    0.11           residual-stream perturbation. CLB amplification at α = +1
                                      0.10    0.13
                                                                                      yields 23.8%—below baseline. We tentatively attribute this
          0.8
                                                                                      to near-saturation of the model’s CLB representations at
                               0.60                        0.64                       α = 0 (ZSCT 92.6%, close to ceiling), such that further
          0.6                                                          0.59
                                              0.59                                    amplification introduces representational noise rather than
                                      0.86
          0.4                                                                         additional benefit; however, we acknowledge that this expla-
                                                                                      nation is post-hoc and that the amplification direction may
          0.2                  0.32                        0.32                       simply be poorly calibrated for proof generation, leaving
                                              0.24                     0.27
                                                                                      the asymmetry between suppression and amplification as a
          0.0                   =0    CLB     CLB        random      random           limitation for future work. Together, these results establish
                                      = 3     =+1          = 3         =+1            a causal role for the CLB direction in AIME-level theorem
      Figure 7. Mean output coherence fractions per condition under                   proving: selectively suppressing it is sufficient to dismantle
      CAA steering applied to DSP-V2-7B on the AIME subset. Each                      performance, while the random perturbation of the same
      bar shows the fraction of generated proofs falling into one of                  norm leaves performance intact.
      four classes: solved (correct proof), valid Lean, unproven (well-
      formed but incomplete), invalid Lean (parse/elaboration error),
      and system/timeout (Lean compiler timeout or system error). Co-                 5. Discussions
      herence (solved + valid Lean) remains stable across all conditions,
      ruling out garbled-output confounds.                                            5.1. On the Asymmetry of Receptivity vs Constructivity
                                                                                           in CLBs: Receptivity is a Structural Gatekeeper

       miniF2F proof generation, restricting to the 15 AIME prob-                     A potential critique is that a linguistic listener-only bench-
       lems in the Olympiad-level, tail subset to maximise the ex-                    mark like S2B-LM introduces a task-modality mismatch
       pected CLB signal. Figures 6 and 7 show per-problem solve                      when evaluating formal theorem provers, which are inher-
       rates (pass@32) and aggregate performance under baseline                       ently constructive sequence generators. However, this ar-
       (α = 0), CLB suppression (α = −3), CLB amplification                           gument overlooks the structural asymmetry between the
       (α = +1), and random controls (α ∈ {−3, +1}).                                  two aspects of CLBs established in Section 2.1. In for-
                                                                                      mal proof synthesis, constructive aspects are structurally
       CLB suppression at α = −3 collapses aggregate solve rate                       downstream of receptive ones. Even in the whole-proof
       from 32.3% at baseline to 2.9%, without creating incoher-                      generation regime, a prover does not synthesise proof steps
       ent Lean proof candidates. This coherent collapse amounts                      from a fixed prelearned vocabulary alone: Olympiad-level
       to an 91% relative drop, which is spread nearly uniformly                      theorems require the chain-of-thought to decode, bind, and
       across all 15 problems. By contrast, the random control                        recombine novel intermediate propositions, unfamiliar tac-
       at the same magnitude (α = −3) leaves performance vir-                         tic compositions, and out-of-distribution mathematical ob-
       tually unchanged at 31.9%, confirming that the collapse                        jects that cannot be retrieved from pretraining weights by
       is specific to the CLB direction and not an artefact of any

                                                                                  8
                                On Compositional Learning Behaviours in Formal Mathematics

memorisation—the same within-episode grounding require-               A necessary-condition analysis via a quadrant test—
ment that defines the CLB regime (Section 2.1).                       dichotomising each axis at its empirical median (adj-ZSCT
                                                                      = 23.3; miniF2F = 67.95%) and testing depletion of
If an agent lacks the capacity to systematically process novel,
                                                                      the forbidden cell (high miniF2F, low adj-ZSCT) by ex-
out-of-distribution symbolic structures encountered in con-
                                                                      act enumeration of all 10  5 = 252 label placements—finds
text (receptivity), then any subsequent constructive genera-
                                                                      the forbidden cell empty: no model achieves Olympiad-
tion degrades. Confronted with mathematical configurations
                                                                      level performance without measurable CLB competency
beyond its compositional horizon, the agent with low recep-
                                                                      (p = 0.004). This establishes CLB competency as a nec-
tive CLB competency cannot decompose and recombine
                                                                      essary, though not sufficient, condition for crossing the
the relevant symbolic structures systematically, causing its
                                                                      Olympiad-performance threshold: CLB competency gates
constructive search to collapse into stochastic matching over
                                                                      entry to the hard tail without determining ranking within it.
its prelearned tactic distribution.
                                                                      Model scale is ruled out as a confound: DeepSeek-Prover-
Thus, isolating the receptive axis in S2B-LM is a delib-              V2-7B (7B parameters) clears the Olympiad threshold at
erate diagnostic focus. Receptive systematicity serves as             75.6% miniF2F while remaining a small model, demon-
a strict structural gatekeeper. While low-to-medium diffi-            strating that scale is not a necessary condition for the hard
culty theorems (Zheng et al., 2022) (miniF2F ≤ 60.3%)                 tail.
can be traversed purely via shallow syntactic matching and
                                                                      To move beyond correlation, we extract a CLB-encoding
possibly massive search budgets without measurable CLB
                                                                      direction from DSP-V2-7B via Contrastive Activation
competency, breaking into the hard tail (miniF2F > 67.2%)
                                                                      Addition on matched teacher-forced S2B-LM pairs—
requires clearing this foundational bottleneck.
                                                                      contrasting correct verbalizations against surface-coherent
                                                                      but hypothesis-corrupted ones—and apply it as a residual-
5.2. On Self-Evolving Agents requiring CLBs.                          stream intervention during miniF2F proof search. A dosage
The stability of a self-evolving scientific agent’s improve-          sweep on S2B-LM confirms that the direction specifically
ment loop depends critically on CLB capacity. While CB                and monotonically modulates CLB competency (ZSCT
capacity and proof-tree search suffice for the tractable bulk         from 92.6% at α = 0 to 57.2% at α = −4, near the guess-
of formal mathematics, a genuinely self-evolving agent                ing floor) while coherence is preserved, with orthogonal and
must progressively ground proof structures outside its fixed          random control directions producing flat responses. Trans-
prelearned vocabulary. Without robust CLB competency,                 ferring the same vector to AIME-level theorem proving,
an agent cannot isolate abstract principles from success-             CLB suppression (α = −3) collapses the aggregate solve
ful proof trajectories. Indeed, its constructive competency           rate from 32.3% to 2.9% (91% relative drop), while a ran-
would collapse into stochastic matching over prelearned tac-          dom direction of equal magnitude leaves performance at
tics. Systematic receptivity thus stabilises the exploration          31.9%—establishing a specific causal link between the CLB
space, enabling the policy to ground newly-encountered                representational direction and Olympiad-tier proof perfor-
symbolic objects and recombine them with prelearned prim-             mance.
itives as difficulty increases.                                       These findings carry direct implications for self-evolving
                                                                      scientific agents: CB capacity and proof-tree search can nav-
6. Conclusion                                                         igate the tractable portion of formal mathematics, but hit a
                                                                      combinatorial ceiling without the systematic within-episode
We investigated the role of Compositional Learning Be-                generalisation afforded by CLBs. Future work includes: (1)
haviours (CLBs) in formal mathematical theorem proving                repurposing the S2B-LM to generate synthetic training data
by cross-examining ten state-of-the-art provers with the              that explicitly instils CLB competency into formal prov-
S2B-LM benchmark—an extension of the original S2B that                ing models; and (2) evaluating the constructivity aspects
replaces the continuous stimulus domain with a categor-               of CLBs—currently unexplored here—by placing tested
ical one and introduces chain-of-thought scaffolding, in              models in the speaker role of the S2B-LM.
order to control for NUPA confounders and the competence–
performance distinction. Our analysis reveals a fundamental
capability dissociation: CLB competency—the receptive                 Impact Statement
ability to ground never-before-seen symbolic objects from             This paper presents work whose goal is to advance the field
in-context evidence and generalise systematically to their            of Machine Learning. There are many potential societal
novel recombinations, beyond the recombination of pre-                consequences of our work, none which we feel must be
learned atoms (CB capacity)—is neither uniformly corre-               specifically highlighted here.
lated with miniF2F accuracy across the full benchmark, nor
orthogonal to it at the Olympiad level.


                                                                  9
                                 On Compositional Learning Behaviours in Formal Mathematics

Acknowledgements                                                           Song, J., Dong, K., Hu, K., Gao, K., Guan, K., Huang,
                                                                           K., Yu, K., Wang, L., Zhang, L., Xu, L., Xia, L., Zhao,
This work was done as an Independent Researcher, previ-                    L., Wang, L., Zhang, L., Li, M., Wang, M., Zhang, M.,
ously supported by the EPSRC Centre for Doctoral Train-                    Zhang, M., Tang, M., Li, M., Tian, N., Huang, P., Wang,
ing in Intelligent Games & Games Intelligence (IGGI)                       P., Zhang, P., Wang, Q., Zhu, Q., Chen, Q., Du, Q., Chen,
[EP/L015846/1].                                                            R. J., Jin, R. L., Ge, R., Zhang, R., Pan, R., Wang, R.,
We gratefully acknowledge the use of Python (Van Rossum                    Xu, R., Zhang, R., Chen, R., Li, S. S., Lu, S., Zhou, S.,
& Drake, 2009), Weights and Biases (Biewald, 2020),                        Chen, S., Wu, S., Ye, S., Ye, S., Ma, S., Wang, S., Zhou,
SciPy (Virtanen et al., 2020a), Scikit-learn (Pedregosa et al.,            S., Yu, S., Zhou, S., Pan, S., Wang, T., Yun, T., Pei, T.,
2011), NumPy (Harris et al., 2020), PyTorch (Paszke et al.,                Sun, T., Xiao, W. L., Zeng, W., Zhao, W., An, W., Liu,
2019), HuggingFace’s Transformers (Wolf et al., 2020),                     W., Liang, W., Gao, W., Yu, W., Zhang, W., Li, X. Q.,
without which this work would not be possible. We also                     Jin, X., Wang, X., Bi, X., Liu, X., Wang, X., Shen, X.,
acknowledge the use of Claude Code (Anthropic) to assist                   Chen, X., Zhang, X., Chen, X., Nie, X., Sun, X., Wang,
with code development and paper editing throughout this                    X., Cheng, X., Liu, X., Xie, X., Liu, X., Yu, X., Song,
work.                                                                      X., Shan, X., Zhou, X., Yang, X., Li, X., Su, X., Lin, X.,
The code for this work is available at https://github.                     Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhu, Y. X., Zhang,
com/Near32/OnCLBinFM, and the S2B-LM code-                                 Y., Xu, Y., Xu, Y., Huang, Y., Li, Y., Zhao, Y., Sun, Y.,
base is available at https://github.com/Near32/                            Li, Y., Wang, Y., Yu, Y., Zheng, Y., Zhang, Y., Shi, Y.,
SymbolicBehaviourBenchmark/tree/S2B-LM.                                    Xiong, Y., He, Y., Tang, Y., Piao, Y., Wang, Y., Tan, Y.,
                                                                           Ma, Y., Liu, Y., Guo, Y., Wu, Y., Ou, Y., Zhu, Y., Wang,
                                                                           Y., Gong, Y., Zou, Y., He, Y., Zha, Y., Xiong, Y., Ma, Y.,
References                                                                 Yan, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y., Wu, Z. F.,
Biewald, L. Experiment tracking with weights and biases,                   Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Huang, Z.,
  2020. URL https://www.wandb.com/. Software                               Zhang, Z., Xie, Z., Zhang, Z., Hao, Z., Gou, Z., Ma, Z.,
  available from wandb.com.                                                Yan, Z., Shao, Z., Xu, Z., Wu, Z., Zhang, Z., Li, Z., Gu,
                                                                           Z., Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song, Z., Gao, Z.,
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D.,                and Pan, Z. Deepseek-v3 technical report, 2025. URL
  Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,                    https://arxiv.org/abs/2412.19437.
  Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,
  Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J.,   Denamganaı̈, K., Missaoui, S., and Walker, J. A. Meta-
  Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M.,      referential games to learn compositional learning be-
  Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S.,   haviours. arXiv preprint arXiv:2207.08012, 2022.
  Radford, A., Sutskever, I., and Amodei, D. Language         Dong, Q., Li, L., Dai, D., Zheng, C., Ma, J., Li, R., Xia,
  models are few-shot learners.          In Larochelle, H.,     H., Xu, J., Wu, Z., Liu, T., et al. A survey on in-context
  Ranzato, M., Hadsell, R., Balcan, M., and Lin, H. (eds.),     learning, 2024. URL https://arxiv. org/abs/2301.00234,
  Advances in Neural Information Processing Systems,            19, 2022.
  volume 33, pp. 1877–1901. Curran Associates, Inc.,
  2020. URL https://proceedings.neurips. Dul, J. Necessary condition analysis (nca) logic and method-
  cc/paper_files/paper/2020/file/                               ology of “necessary but not sufficient” causality. Organi-
  1457c0d6bfcb4967418bfb8ac142f64a-Paper.                       zational research methods, 19(1):10–52, 2016.
  pdf.
                                                              Firestone, C. Performance vs. competence in human–
Chaabouni, R., Kharitonov, E., Bouchacourt, D., Dupoux,         machine comparisons. Proceedings of the National
  E., and Baroni, M. Compositionality and generalization        Academy   of Sciences, 117(43):26562–26571, 2020.
  in emergent languages. In Proceedings of the 58th annual               Good, P. Permutation, parametric and bootstrap tests of
  meeting of the association for computational linguistics,                hypotheses. Springer, 2005.
  pp. 4427–4442, 2020.
                                                                         Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers,
DeepSeek-AI, Liu, A., Feng, B., Xue, B., Wang, B., Wu, B.,                 R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J.,
  Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai, D.,                Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van
  Guo, D., Yang, D., Chen, D., Ji, D., Li, E., Lin, F., Dai,               Kerkwijk, M. H., Brett, M., Haldane, A., Fernández del
  F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H., Bao,                  Rı́o, J., Wiebe, M., Peterson, P., Gérard-Marchant, P.,
  H., Xu, H., Wang, H., Zhang, H., Ding, H., Xin, H., Gao,                 Sheppard, K., Reddy, T., Weckesser, W., Abbasi, H.,
  H., Li, H., Qu, H., Cai, J. L., Liang, J., Guo, J., Ni, J., Li,          Gohlke, C., and Oliphant, T. E. Array programming with
  J., Wang, J., Chen, J., Chen, J., Yuan, J., Qiu, J., Li, J.,             NumPy, 2020.

                                                                    10
                                On Compositional Learning Behaviours in Formal Mathematics

Kim, N. and Linzen, T. COGS: A compositional general-                 Pitman, E. J. G. Significance tests which may be applied
  ization challenge based on semantic interpretation. In                 to samples from any populations. ii. the correlation co-
  Webber, B., Cohn, T., He, Y., and Liu, Y. (eds.), Pro-                 efficient test. Supplement to the Journal of the Royal
  ceedings of the 2020 Conference on Empirical Methods                  Statistical Society, 4(2):225–232, 1937.
  in Natural Language Processing (EMNLP), pp. 9087–
  9105, Online, November 2020. Association for Computa-               Qwen, :, Yang, A., Yang, B., Zhang, B., Hui, B., Zheng,
  tional Linguistics. doi: 10.18653/v1/2020.emnlp-main.                B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H., Lin, H.,
  731. URL https://aclanthology.org/2020.                              Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J.,
  emnlp-main.731/.                                                     Lin, J., Dang, K., Lu, K., Bao, K., Yang, K., Yu, L.,
                                                                       Li, M., Xue, M., Zhang, P., Zhu, Q., Men, R., Lin, R.,
Lampinen, A. Can language models handle recursively                    Li, T., Tang, T., Xia, T., Ren, X., Ren, X., Fan, Y., Su,
  nested grammatical structures? a case study on com-                  Y., Zhang, Y., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., and
  paring models and humans. Computational Linguis-                     Qiu, Z. Qwen2.5 technical report, 2025. URL https:
  tics, 50(4):1441–1476, December 2024. doi: 10.                       //arxiv.org/abs/2412.15115.
  1162/coli a 00525. URL https://aclanthology.
  org/2024.cl-4.8/.                                                   Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,
                                                                        W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,
Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., LI, J.,          Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,
  Xia, M., Chen, D., Arora, S., and Jin, C. Goedel-prover:              and Ruan, C. Deepseek-prover-v2: Advancing formal
  A frontier model for open-source automated theorem                    mathematical reasoning via reinforcement learning for
  proving. In Second Conference on Language Modeling,                   subgoal decomposition, 2025. URL https://arxiv.
  2025. URL https://openreview.net/forum?                               org/abs/2504.21801.
  id=x2y9i2HDjD.
                                                                      Rimsky, N., Gabrieli, N., Schulz, J., Tong, M., Hubinger,
Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao, H.,
                                                                        E., and Turner, A. Steering llama 2 via contrastive activa-
  Jiang, L., Geng, Y., Ge, J., Sun, J., Wu, J., Gesi, J., Lu, X.,
                                                                        tion addition. In Ku, L.-W., Martins, A., and Srikumar,
  Acuna, D., Yang, K., Lin, H., Choi, Y., Chen, D., Arora,
                                                                        V. (eds.), Proceedings of the 62nd Annual Meeting of
  S., and Jin, C. Goedel-prover-v2: Scaling formal theorem
                                                                        the Association for Computational Linguistics (Volume
  proving with scaffolded data synthesis and self-correction.
                                                                        1: Long Papers), pp. 15504–15522, Bangkok, Thailand,
  In The Fourteenth International Conference on Learning
                                                                        August 2024. Association for Computational Linguis-
  Representations, 2026. URL https://openreview.
                                                                        tics. doi: 10.18653/v1/2024.acl-long.828. URL https:
  net/forum?id=j4C0nALrgK.
                                                                        //aclanthology.org/2024.acl-long.828/.
Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury,
  J., Chanan, G., Killeen, T., Lin, Z., Gimelshein,       Santoro, A., Lampinen, A., Mathewson, K., Lillicrap, T.,
  N., Antiga, L., Desmaison, A., Kopf, A., Yang, E.,        and Raposo, D. Symbolic behaviour in artificial intelli-
  DeVito, Z., Raison, M., Tejani, A., Chilamkurthy,         gence. arXiv preprint arXiv:2102.03406, 2021.
  S., Steiner, B., Fang, L., Bai, J., and Chintala, S.
                                                          Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M.,
  Pytorch: An imperative style, high-performance deep
                                                            Li, Y. K., Wu, Y., and Guo, D. Deepseekmath: Pushing
  learning library. In Advances in Neural Informa-
                                                            the limits of mathematical reasoning in open language
  tion Processing Systems 32, pp. 8024–8035. 2019.
                                                            models. CoRR, abs/2402.03300, 2024. URL https:
  URL        http://papers.neurips.cc/paper/
                                                            //doi.org/10.48550/arXiv.2402.03300.
  9015-pytorch-an-imperative-style-high-performance-deep-learning-library.
  pdf.
                                                          Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M.,
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel,         Jennings, M., Thakur, A., and Chaudhuri, S. Putnam-
  V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer,   bench: Evaluating neural theorem-provers on the putnam
  P., Weiss, R., Dubourg, V., Vanderplas, J., Passos,       mathematical competition. In Globerson, A., Mackey,
  A., Cournapeau, D., Brucher, M., Perrot, M., and          L., Belgrave, D., Fan, A., Paquet, U., Tomczak, J., and
  Édouard Duchesnay. Scikit-learn: Machine learning in     Zhang, C. (eds.), Advances in Neural Information Pro-
  python, 2011. URL http://jmlr.org/papers/                 cessing Systems, volume 37, pp. 11545–11569. Curran
  v12/pedregosa11a.html.                                    Associates,  Inc., 2024. doi: 10.52202/079017-0368.
                                                            URL            https://proceedings.neurips.
Pesarin, F. and Salmaso, L. Permutation tests for complex   cc/paper_files/paper/2024/file/
  data: theory, applications and software. John Wiley &     1582eaf9e0cf349e1e5a6ee453100aa1-Paper-Datasets_
  Sons, 2010.                                               and_Benchmarks_Track.pdf.

                                                                 11
                               On Compositional Learning Behaviours in Formal Mathematics

Turner, A. M., Thiergart, L., Leech, G., Udell, D., Vazquez,         Wei, J., Wang, X., Schuurmans, D., Bosma, M., brian ichter,
  J. J., Mini, U., and MacDiarmid, M. Steering lan-                   Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain of
  guage models with activation engineering. arXiv preprint            thought prompting elicits reasoning in large language
  arXiv:2308.10248, 2023.                                             models. In Oh, A. H., Agarwal, A., Belgrave, D., and Cho,
                                                                      K. (eds.), Advances in Neural Information Processing
Van Rossum, G. and Drake, F. L. Python 3 Reference                    Systems, 2022b. URL https://openreview.net/
  Manual. CreateSpace, Scotts Valley, CA, 2009. ISBN                  forum?id=_VjQlMeSB_J.
  1441412697.
                                                                     Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C.,
Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M.,            Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz, M.,
  Reddy, T., Cournapeau, D., Burovski, E., Peterson, P.,              Davison, J., Shleifer, S., von Platen, P., Ma, C., Jernite,
  Weckesser, W., Bright, J., van der Walt, S. J., Brett, M.,          Y., Plu, J., Xu, C., Scao, T. L., Gugger, S., Drame, M.,
  Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R. J.,          Lhoest, Q., and Rush, A. M. Huggingface’s transformers:
  Jones, E., Kern, R., Larson, E., Carey, C. J., Polat, İ.,          State-of-the-art natural language processing, 2020. URL
  Feng, Y., Moore, E. W., VanderPlas, J., Laxalde, D.,                https://arxiv.org/abs/1910.03771.
  Perktold, J., Cimrman, R., Henriksen, I., Quintero, E. A.,
  Harris, C. R., Archibald, A. M., Ribeiro, A. H., Pedregosa,        Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
  F., van Mulbregt, P., and SciPy 1.0 Contributors. SciPy              C., Li, W., and Liang, X. Deepseek-prover: Advancing
  1.0: Fundamental Algorithms for Scientific Computing                 theorem proving in llms through large-scale synthetic
  in Python, 2020a.                                                    data. arXiv preprint arXiv:2405.14333, 2024.

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M.,           Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H.,
  Reddy, T., Cournapeau, D., Burovski, E., Peterson, P.,               Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhang,
  Weckesser, W., Bright, J., et al. Scipy 1.0: fundamental             H., Zhu, Q., Yang, D., Gou, Z., Wu, Z., Luo, F., and
  algorithms for scientific computing in python. Nature                Ruan, C. Deepseek-prover-v1.5: Harnessing proof as-
  methods, 17(3):261–272, 2020b.                                       sistant feedback for reinforcement learning and monte-
                                                                       carlo tree search. In The Thirteenth International Confer-
Vuong, Q. H. Likelihood ratio tests for model selection and            ence on Learning Representations, 2025. URL https:
  non-nested hypotheses. Econometrica: journal of the                  //openreview.net/forum?id=I4YAIwrsXa.
  Econometric Society, pp. 307–333, 1989.
                                                                     Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng,
Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Dos San-            B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu,
 tos, M., Sung, F., et al. Kimina-Prover: Applying                     D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin,
 test-time RL search on large formal reasoning mod-                    H., Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang,
 els. https://huggingface.co/blog/AI-MO/                               J., Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang,
 kimina-prover, 2025a.                                                 K., Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang,
                                                                       P., Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo,
Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., San-
                                                                       S., Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang,
 tos, M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z.,
                                                                       X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y., Wan,
 Lu, J., de Saxcé, H., Bailey, B., Song, C., Xiao, C.,
                                                                       Y., Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and
 Zhang, D., Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer,
                                                                       Qiu, Z. Qwen3 technical report, 2025a. URL https:
 J., Michel, J., Yu, L., Dreyfus-Schmidt, L., Tunstall,
                                                                       //arxiv.org/abs/2505.09388.
 L., Pagani, L., Machado, M., Bourigault, P., Wang, R.,
 Polu, S., Barroyer, T., Li, W.-D., Niu, Y., Fleureau, Y.,           Yang, H., Hu, Y., Kang, S., Lin, Z., and Zhang, M.
 Hu, Y., Yu, Z., Wang, Z., Yang, Z., Liu, Z., and Li, J.               Number cookbook: Number understanding of language
 Kimina-prover preview: Towards large formal reason-                   models and how to improve it. In The Thirteenth In-
 ing models with reinforcement learning, 2025b. URL                    ternational Conference on Learning Representations,
 https://arxiv.org/abs/2504.11354.                                     2025b. URL https://openreview.net/forum?
                                                                       id=BWS5gVjgeY.
Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B.,
 Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Met-               Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
 zler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang,              P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
 P., Dean, J., and Fedus, W. Emergent abilities of large               Leandojo: Theorem proving with retrieval-augmented
 language models. Transactions on Machine Learning                     language models. In Thirty-seventh Conference on Neu-
 Research, 2022a. ISSN 2835-8856. URL https://                         ral Information Processing Systems Datasets and Bench-
 openreview.net/forum?id=yzkSU5zdwD. Sur-                              marks Track, 2023. URL https://openreview.
 vey Certification.                                                    net/forum?id=g7OX2sOJtn.

                                                                12
                              On Compositional Learning Behaviours in Formal Mathematics

Yang, K., Poesia, G., He, J., Li, W., Lauter, K. E., Chaud-
  huri, S., and Song, D. Position: Formal mathematical
  reasoning—a new frontier in AI. In Forty-second Interna-
  tional Conference on Machine Learning Position Paper
  Track, 2025c. URL https://openreview.net/
  forum?id=HuvAM5x2xG.
Zheng, K., Han, J. M., and Polu, S. minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. In
  International Conference on Learning Representations,
  2022. URL https://openreview.net/forum?
  id=9ZPegFuFTFv.




                                                              13
                                          On Compositional Learning Behaviours in Formal Mathematics

A. Rule-Based Listener Verbalizer Algorithm

Algorithm 1 Hypothesis-tracking rule-based listener verbalizer (one episode)
Require: Posdis-speaker π S , Ndim , supporting-phase games Gsup
 1: V ← {}                                                                         {value map: (pos, tok) → {val : count}}
 2: mlast ← {}
 3: for game g = 1, . . . , Gsup do
 4:   Receive speaker message m = [t0 , . . . , tNdim −1 ] and own stimulus s = [s0 , . . . , sNdim −1 ]
 5:   // Sync round: update V from speaker’s target and message mlast at previous game
 6:   if mlast ̸= {} then
 7:       Receive speaker target at previous game, from listener feedback/sync step flast = [f0last , . . . , fN
                                                                                                               last
                                                                                                                 dim −1
                                                                                                                        ]
 8:       for i = 0, . . . , Ndim − 1 do
 9:          if tlast
                 i ̸= E O S then
10:              V[(i, tlast        last
                         i )][fi ] += 1
11:          end if
12:       end for
13:   end if
14:   // Bookkeeping: records the current game’s speaker message for the next sync round
15:   mlast = [tlast             last
                    0 , . . . , tNdim −1 ] ← m
16:   // Invert V: predict the message the speaker would send for s
17:   for i = 0, . . . , Ndim − 1 do
18:       if (i, si ) has evidence in V (as a value) then
19:          t̂i ← arg maxt V[(i, t)][si ]
20:       else
21:          t̂i ← UNKNOWN
22:       end if
23:   end for
24:   // Decision: count matches between actual and predicted message
25:   nmatch ← |{i : t̂i = ti , t̂i ̸= UNKNOWN}|
26:   d ← 0 (same class) if nmatch ≥ Ndim , else 1 (different class)
27:   E MIT V ERBALIZE(V, s, m, t̂, nmatch , d)
28: end for



B. Conversation Example
  S2B-LM supporting-phase conversation: 6 games, Ndim = 3 (instruments, sports, vegetables), vocab size 16, max sentence
  length 3
  [System]
  You are a listener agent in a referential game played over multiple rounds. Use the conversation history to learn the speaker’s private code across games, then decide
  whether the current stimulus shares the same latent meaning. Think step by step, then end your response with Answer: 0 (same latent meaning) or Answer: 1 (different).
  You and your partner play a sequence of referential games; you are the listener. In the first phase you will get acquainted with the atomic components of the possible
  observations; then you will be tested with new observations combining the same atomic components in novel ways. At each game each of you observes a stimulus
  representing a latent meaning, and your common goal is to figure out whether you are observing different or similar latent meanings. Your partner can send you messages
  via a communication channel of 16 symbols combined into sentences of maximum length 3. Symbol 0 is the end-of-message symbol: any symbol following it is ignored
  and regularised to 0.

  [User — Game #0]
  At game #0, you are observing stimulus: [[’piano’, ’swimming’, ’eggplant’]]. Your partner has sent you the following message: [8, 5, 6].
  Question #1: At game #0, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #0]
  Let’s think step by step and leverage past games. No sync step data yet — cannot predict expected symbols. Answer: 0

  [User — Sync & Game #1]
  At the end of game #0, sync step: the exact stimulus your partner observed was [[’piano’, ’swimming’, ’eggplant’]]. You decided: similar latent meanings.
  This was correct — you have won game #0.



                                                                                   14
                                           On Compositional Learning Behaviours in Formal Mathematics

  At game #1, you are observing stimulus: [[’piano’, ’golf’, ’pepper’]]. Your partner has sent you the following message: [8, 11, 13].
  Question #1: At game #1, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #1 (first full verbalized trace)]
  Let’s think step by step and leverage past games. From the last game syncing, we can learn that: symbol 8 at pos 0 → piano ; symbol 5 at pos 1 → swimming ; symbol 6 at
  pos 2 → eggplant. In the current game, if the speaker were observing a similar stimulus as ours, [piano, golf, pepper], then: at pos 0, piano → symbol 8 (from game
  #0) ; at pos 1, golf has not been observed yet ; at pos 2, pepper has not been observed yet. Since the speaker’s message is [8, 11, 13], yield 1/3 matches, they are
  likely observing a different stimulus. Answer: 1

  [User — Sync & Game #2]
  At the end of game #1, sync step: the exact stimulus your partner observed was [[’piano’, ’golf’, ’pepper’]]. You decided: different latent meanings. This
  was incorrect — you have lost game #1.
  At game #2, you are observing stimulus: [[’oboe’, ’rugby’, ’broccoli’]]. Your partner has sent you the following message: [3, 9, 2].
  Question #1: At game #2, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #2]
  Let’s think step by step and leverage past games. From the last game syncing, we can learn that: symbol 8 at pos 0 → piano ; symbol 11 at pos 1 → golf ; symbol 13 at
  pos 2 → pepper. In the current game, if the speaker were observing a similar stimulus as ours, [oboe, rugby, broccoli], then: at pos 0, oboe has not been observed yet ; at
  pos 1, rugby has not been observed yet ; at pos 2, broccoli has not been observed yet. Since the speaker’s message is [3, 9, 2], yield 0/3 matches, they are likely
  observing a different stimulus. Answer: 1

  [User — Sync & Game #3]
  At the end of game #2, sync step: the exact stimulus your partner observed was [[’oboe’, ’rugby’, ’broccoli’]]. You decided: different latent meanings.
  This was incorrect — you have lost game #2.
  At game #3, you are observing stimulus: [[’oboe’, ’rugby’, ’broccoli’]]. Your partner has sent you the following message: [3, 15, 6].
  Question #1: At game #3, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #3]
  Let’s think step by step and leverage past games. From the last game syncing, we can learn that: symbol 3 at pos 0 → oboe ; symbol 9 at pos 1 → rugby ; symbol 2 at pos 2
  → broccoli. In the current game, if the speaker were observing a similar stimulus as ours, [oboe, rugby, broccoli], then: at pos 0, oboe → symbol 3 (from game #2) ; at
  pos 1, rugby → symbol 9 (from game #2) ; at pos 2, broccoli → symbol 2 (from game #2). Since the speaker’s message is [3, 15, 6], yield 1/3 matches, they are
  likely observing a different stimulus. Answer: 1

  [User — Sync & Game #4]
  At the end of game #3, sync step: the exact stimulus your partner observed was [[’oboe’, ’skiing’, ’eggplant’]]. You decided: different latent meanings.
  This was correct — you have won game #3.
  At game #4, you are observing stimulus: [[’drums’, ’golf’, ’pepper’]]. Your partner has sent you the following message: [12, 11, 13].
  Question #1: At game #4, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #4]
  Let’s think step by step and leverage past games. From the last game syncing, we can learn that: symbol 3 at pos 0 → oboe ; symbol 15 at pos 1 → skiing ; symbol 6 at
  pos 2 → eggplant. In the current game, if the speaker were observing a similar stimulus as ours, [drums, golf, pepper], then: at pos 0, drums has not been observed yet ; at
  pos 1, golf → symbol 11 (from game #1) ; at pos 2, pepper → symbol 13 (from game #1). Since the speaker’s message is [12, 11, 13], yield 2/3 matches, they are
  likely observing a different stimulus. Answer: 1

  [User — Sync & Game #5]
  At the end of game #4, sync step: the exact stimulus your partner observed was [[’drums’, ’golf’, ’pepper’]]. You decided: different latent meanings. This
  was incorrect — you have lost game #4.
  At game #5, you are observing stimulus: [[’guitar’, ’rugby’, ’eggplant’]]. Your partner has sent you the following message: [4, 9, 6].
  Question #1: At game #5, do you think you are observing a stimulus with the same latent meaning as your partner? Answer 0: Yes or 1: No. End your response with your
  decision as a single integer.

  [Listener — Game #5]
  Let’s think step by step and leverage past games. From the last game syncing, we can learn that: symbol 12 at pos 0 → drums ; symbol 11 at pos 1 → golf ; symbol 13 at
  pos 2 → pepper. In the current game, if the speaker were observing a similar stimulus as ours, [guitar, rugby, eggplant], then: at pos 0, guitar has not been observed
  yet ; at pos 1, rugby → symbol 9 (from game #2) ; at pos 2, eggplant → symbol 6 (from game #3). Since the speaker’s message is [4, 9, 6], yield 2/3 matches, they
  are likely observing a different stimulus. Answer: 1




Figure 8. S2B-LM conversation examples over 6 supporting-phase games illustrating the hypothesis-tracking rule-based listener verbalizer.
System sets the task context. User messages present each game’s stimulus and message, followed by the sync-step revelation of the
speaker’s target. Listener responses are produced by V ERBALIZE (Algorithm 1): game #0 defaults to same (no sync data yet); subsequent
games accumulate sync-derived token-to-value evidence in V and apply the sync-summary → inverse-prediction → match-comparison
chain; games #3–#5 illustrate how the evidence base grows across episodes, with partial matches (1/3, 2/3) correctly classified as different
even as the mapping fills in.


                                                                                      15
                               On Compositional Learning Behaviours in Formal Mathematics

C. Further Correlational Evidence
We cross-evaluate the ten provers of Table 2 against two complementary non-parametric tests to determine whether CLB
competency—as measured by adj-ZSCT—constitutes a necessary prerequisite for high miniF2F performance. We begin
with a global ceiling-zone analysis over all 10! = 3,628,800 pairings (Section C.1). Seeing that this global test falls just
short of conventional significance (p = 0.052), we consider the likely confound introduced by the heavily right-skewed
difficulty distribution of miniF2F (Zheng et al., 2022): search-tractable theorems in the lower range can be solved without
any measurable CLB competency, diluting any global boundary signal. We therefore apply a structurally targeted tail
partition test (Section C.2) that isolates the Olympiad-level regime (miniF2F > 75%) and asks whether the models that
penetrate it cluster exclusively at high adj-ZSCT. To rule out model scale as a competing explanation, we embed both
predictors in an identical permutation space and compare their significance footprints (Section C.3). Throughout, we rely
exclusively on exact permutation methods rather than parametric or asymptotic estimators, as the small evaluation pool
(N = 10) renders standard asymptotic tools structurally invalid; the full statistical rationale is given in Appendix D.
C.1. Global Continuous Bottleneck Test
We first apply a global, continuous bottleneck check using non-parametric ceiling zone analysis (Dul, 2016). This framework
operationalises the prerequisite hypothesis geometrically: under a true bottleneck, the upper-left region of the (adj-ZSCT,
miniF2F) scatter—high miniF2F, low adj-ZSCT—should be systematically vacant.
Limitation: slope dependency. The vacancy penalty statistic requires a boundary line Y = s·X that separates the forbidden
upper-left region from the permitted lower-right region. Because adj-ZSCT and miniF2F are expressed on the same [0, 100]
percentage scale but measure incommensurate quantities, the slope s cannot be derived from first principles — it is a free
parameter. We set it in a data-determined, scale-free way as s = max(miniF2F)/ max(adj-ZSCT) = 88.1/100.0 = 0.881,
which normalises each axis by its observed maximum so that the boundary passes through the top-right corner of the
empirical scatter. This is the most principled choice available, but the p-value remains sensitive to it (e.g. p = 0.050 at
s = 0.88, rising to p = 0.054 at the bare diagonal s = 1.0). The slope-free quadrant test in Section 4.1 avoids this limitation
entirely.
Null Hypothesis (H0CLB,global ). The joint distribution of (adj-ZSCT, miniF2F) pairs exhibits no directional vacancy in the
upper-left quadrant; the observed triangular layout is consistent with a random re-pairing of the empirical adj-ZSCT and
miniF2F marginal distributions.
Alternative Hypothesis (H1CLB,global ). The upper-left quadrant of the (adj-ZSCT, miniF2F) space is systematically empty,
indicating that low CLB competency constrains the maximum achievable formal verification accuracy.
We define the test statistic T as the negative upper-left vacancy penalty:
                                             N                                
                                             X          miniF2Fi     adj-ZSCTi
                                     T =−        max 0,          −s·                                                       (2)
                                             i=1
                                                          100            100

T = 0 indicates no violations of the prerequisite ordering; increasingly negative values reflect models that achieve high
miniF2F despite low adj-ZSCT. Under H1CLB,global , the observed pairing should yield a T value significantly closer to zero
than under random re-pairings.
An exact pairings permutation test evaluating all 10! = 3,628,800 possible (adj-ZSCT, miniF2F) pairings, using the scale-
normalised slope s = 0.881, yields an observed statistic of T = −3.237 and an empirical pglobal
                                                                                            CLB = 0.050. This sits exactly
at the conventional significance threshold (α = 0.05) and should be interpreted with caution given its sensitivity to the slope
choice noted above. The primary driver of the residual penalty is Goedel-Prover-V2-32B, which achieves miniF2F = 88.1%
at a comparatively low adj-ZSCT = 30.4, placing a data point in the upper-left region and inflating the observed vacancy
penalty. We attribute this anomaly to the competence–performance distinction (Section 3.2): the model may possess latent
CLB competency that the 10-shot scaffold fails to elicit at this scale and model family, causing adj-ZSCT to underestimate
its true CLB ability.
C.2. Tail Partition Permutation Test
The failure of the global continuous test motivates a more targeted, structurally motivated hypothesis. The difficulty
distribution of miniF2F is heavily right-skewed (Zheng et al., 2022): 164 of the 244 test-split problems (67.2%) are drawn
from MATH levels 1–5 and custom sources, forming a low-to-medium difficulty bulk solvable via syntactic fluency and
extensive proof-tree search without requiring systematic compositional generalisation, while the remaining 80 problems
(32.8%) are drawn from AMC, AIME, and IMO—the competitive and Olympiad tiers that resist brute-force enumeration
and should expose a genuine CLB bottleneck. Any global boundary test will therefore be confounded by the abundance of
search-solvable theorems in the lower miniF2F range.

                                                              16
                               On Compositional Learning Behaviours in Formal Mathematics

We formalise this observation as a tail partition test anchored at the structural undergraduate–Olympiad boundary of
67.2%: 164 of 244 test-split problems (67.2%) are MATH-level bulk; the remaining 80 (32.8%) are AMC/AIME/IMO
Olympiad problems. The empirical median of miniF2F across our ten models (67.95%) corroborates this structural cut.
The five models that surpass this threshold—Goedel-Prover-V2-8B (84.6%), Goedel-Prover-V2-32B (88.1%), DeepSeek-
Prover-V2-7B (75.6%), DeepSeek-Prover-V2-671B (82.4%), and Kimina-Prover (84.0%)—constitute the hard tail partition
T.
Null Hypothesis (H0tail ). The five models with the highest miniF2F scores are drawn uniformly at random from the full pool
with respect to their adj-ZSCT scores; any apparent clustering at high adj-ZSCT is attributable to chance.
Alternative Hypothesis (H1tail ). The five models that penetrate the Olympiad-level tail exhibit systematically higher CLB
competency (adj-ZSCT) than would be expected under a random partition of the pool.
The test statistic is the aggregate adj-ZSCT sum over the hard tail:
                                                           X
                                                    ST =       adj-ZSCTi                                                (3)
                                                          i∈T

We enumerate all 10
                      
                    5 = 252 possible ways to select five models from the pool and compute ST for each partition. The
observed value is ST = 354.80. Strikingly, this value corresponds to the maximum achievable adj-ZSCT sum across all 252
partitions: the five models in T are identically the five models with the highest adj-ZSCT scores in the full pool. Exactly 1
                                                                                                         1
configuration out of 252 meets or exceeds this value, yielding an exact empirical p-value of ptail
                                                                                                 CLB = 252 = 0.00397. This
                                                                   tail
result is highly statistically significant (p < 0.01), supporting H1 . The set of models that conquer the Olympiad-level tail
of formal mathematics is in perfect correspondence with the set of models that exhibit the strongest CLB competency—a
coincidence with probability less than 0.4% under the null. Crucially, this finding is consistent with CLB competency being
a necessary condition for elite formal verification performance: no model outside the top adj-ZSCT tier enters the hard tail,
regardless of architecture scale or search budget.

  Takeaway 1. CLB competency is not required for the tractable bulk (pglobal
                                                                           CLB = 0.052, non-significant) but is a strict
  structural prerequisite for the Olympiad-level tier: the top-5 models by miniF2F are precisely the top-5 by adj-ZSCT
  across all 10
                                    tail
              5 = 252 partitions (pCLB = 0.004).


C.3. Decoupling CLB Competency from Model Scale
A compelling competing explanation for the observed capability dissociation is the scale confound hypothesis (Hscale ): larger
models may dominate both the CLB diagnostic and miniF2F accuracy simultaneously, with raw parameter count—rather
than systematic compositional generalisation—as the true latent predictor. To formally adjudicate between HCLB and Hscale ,
we deploy a competitive hypothesis testing tournament. This is motivated by the non-nested model selection logic of Vuong
(1989) but operating entirely within an exact permutation framework (Pitman, 1937; Pesarin & Salmaso, 2010).
Choice of Test Statistic: Pearson r Under Permutation. We adopt Pearson’s product-moment correlation coefficient
r as the test statistic for the continuous boundary test. A common misconception holds that using r forces bivariate
normality assumptions; this is only true when p-values are derived from asymptotic Student’s t-distributions. When
embedded in an exact permutation framework, r operates as a purely deterministic summary of directional coupling, with
no distributional preconditions (Pitman, 1937). Relative to rank-based alternatives such as Spearman’s ϱ, Pearson r better
captures proportional metric gradients: a model that breaks a structural bottleneck and scales sharply on the miniF2F axis
in proportion to its CLB gain produces a stronger r signal. Critically, by shifting the construction of the null distribution
entirely to exact permutation enumeration, we bypass the standard requirements of homoscedasticity and normality that
would otherwise render our small-sample analysis invalid (Pesarin & Salmaso, 2010).
Continuous Space Permutation Distributions. All analyses use N = 10 consistently. Under H0continuous , miniF2F
performance is structurally independent of the predictor; any pairing of a model’s predictor value with another model’s
miniF2F score is equally likely. We fix the miniF2F vector and compute r across all 10! = 3,628,800 permutations of each
predictor, forming an exact empirical null distribution:
                                                           N!
                                                      1 X
                                                 p=           I(rπi ≥ robs )                                              (4)
                                                      N ! i=1

For HCLB (adj-ZSCT), the observed correlation r = 0.7652 yields an exact p-value of pcontinuous
                                                                                           CLB      = 0.00692—highly
significant. For Hscale (total parameters in billions), the observed correlation r = 0.3597 yields pcontinuous
                                                                                                    scale      = 0.17837,
providing no evidence of a continuous dependency between parameter count and miniF2F accuracy.

                                                             17
                                On Compositional Learning Behaviours in Formal Mathematics

Scale Tail Partition Test (N=10, consistent). The most direct rebuttal to the scale hypothesis is DeepSeek-Prover-V2-7B,
which achieves 75.6% miniF2F on only 7B parameters—placing it in the hard tail while remaining the smallest model in the
suite. This single counterexample directly falsifies scale as a necessary condition for Olympiad-level performance. We
corroborate this with an exact tail partition test using total parameter count as the predictor (N = 10 consistently). The five
hard-tail models yield an aggregate parameter sum of 790B. Enumerating all 10
                                                                                       
                                                                                     5   = 252  partitions, 6 meet or exceed this
value (ptail                                                                                         tail
         scale = 0.02381). By contrast, the CLB tail test yields exactly 1 out of 252 partitions (pCLB = 0.00397).
Non-Parametric Competitive Verdict. Under the exact permutation framework (Pitman, 1937; Pesarin & Salmaso,
2010), CLB competency achieves significance on both the continuous (pcontinuous
                                                                              CLB      = 0.0069) and partition (ptail
                                                                                                                  CLB = 0.0040)
                                                       continuous
axes. Scale establishes no continuous footprint (pscale           = 0.178) and, while marginally significant in the tail partition
(ptail
  scale = 0.024), is directly refuted as a necessary condition by the DP-V2-7B counterexample. Systematic compositional
generalisation is thus the dominant structural predictor of elite formal verification performance.

  Takeaway 2. CLB competency achieves significance on both the continuous (pcontinuous CLB      = 0.0069) and partition
  (ptail
    CLB  = 0.0040) axes. Raw  parameter count achieves no continuous  signal (pcontinuous
                                                                               scale      = 0.178) and is directly refuted
  as a necessary condition by DP-V2-7B (7B params, in the hard tail), ruling out scale as the driving confound.

D. Methodological Limitations
Evaluating frontier foundational models introduces severe sample constraints: our pool (N = 10) is strictly bounded by the
immense compute requirements of training and running state-of-the-art provers. Operating within a small-sample regime
limits the use of traditional parametric or asymptotic statistical tools, rendering standard regression or continuous correlation
metrics structurally invalid.
Inadequacy of Parametric and Asymptotic Estimators. Standard statistical methodologies depend on asymptotic
behaviours, where normality and uniform variance are assumed as sample sizes approach infinity (N → ∞). Applying
these to an N = 10 evaluation space introduces critical vulnerabilities:

   • Parametric Inferences: Testing linear regression models via Student’s t or F -statistics requires normally distributed
     residuals. In a 10-point dataset, testing for normality using standard diagnostics lacks sufficient statistical power,
     making significance claims highly sensitive to subtle outliers.

   • Quantile Regression: While boundary limits are traditionally evaluated via high-quantile curves (e.g., tracking the
     90th percentile), these estimators require dense data along the margins of the distribution. At N = 10, estimating
     high-quantile paths lacks the necessary degrees of freedom, creating unstable, overfit boundaries that track individual
     peripheral data points.

   • Heteroscedastic Distortions: Prerequisite capability boundaries inherently display non-uniform variance (heteroscedas-
     ticity). Low input capabilities restrict output variance tightly near a baseline floor, while high input scores unlock the
     full vertical range of execution. Standard Ordinary Least Squares (OLS) models underperform under these conditions,
     distorting standard errors and inflating the risk of false-positive significance claims.

The Rigor of Exact Permutation Tools. To circumvent these small-sample limitations, our pipeline uses exact permutation
tests processed via verified open-source scientific computing engines (Good, 2005; Virtanen et al., 2020b). Permutation
methods offer an elegant, distribution-free framework that provides exact mathematical precision on small sample pools:

  1. Zero Distributional Dependencies: Permutation techniques operate without making structural assumptions regarding
     the normality or variance profiles of the underlying data points. They bypass population parameter estimation by
     calculating significance directly from the empirical dataset’s internal combinatorial structure.

  2. Deterministic Execution Limits: When total possible dataset configurations remain low, numerical engines             can
     directly process the entire factorial set of allocations (10! = 3,628,800 for the global pairing test, and 10
                                                                                                                   
                                                                                                                 5   = 252 for
     the tail partition). By calculating outcomes across the entire permutation space, the resulting p-value represents an
     exact combinatorial probability under the null hypothesis rather than an asymptotic approximation.

By shifting from continuous parametric approximations to exact partition structures, we ensure that our confirmation of the
tail-dependent bottleneck remains robust, reproducible, and completely free from small-sample estimation bias.
On the scaling of Few-shot CoT prompting. In our experiments, few-shot CoT prompting with N = 10 exemplars is
shown sufficient in eliciting the CLB competences of a wide range of LMs, from 7B to 671B. However, in-context learning

                                                               18
                              On Compositional Learning Behaviours in Formal Mathematics

capabilities, and with it the efficiency of few-shot CoT prompting, are known to scale with LM size (Brown et al., 2020; Wei
et al., 2022a; Dong et al., 2022) and to depend on model family. Thus, it is not impossible that N = 10 exemplars may
simply not be enough for some of our tested models to perform as well as their competency allows. However, we argue that
this is fairly unlikely given the fact that the competency has been successfully elicited in LMs of size 7B, 8B, 32B, 72B,
and 671B, spanning the whole range of tested model sizes and accounting for most of the different base model families
represented in our evaluation (see Table 2).




                                                            19
