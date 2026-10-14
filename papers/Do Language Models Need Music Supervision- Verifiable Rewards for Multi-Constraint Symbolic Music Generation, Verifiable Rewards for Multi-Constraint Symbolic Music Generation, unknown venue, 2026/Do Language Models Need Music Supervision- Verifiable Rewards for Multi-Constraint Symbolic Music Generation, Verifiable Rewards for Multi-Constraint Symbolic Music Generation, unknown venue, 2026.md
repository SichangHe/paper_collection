                                                       Do Language Models Need Music Supervision?
                                            Verifiable Rewards for Multi-Constraint Symbolic Music Generation

                                                                                  Haoyue Liu1,2         Xiaoying Tang1,2,†
                                                   1
                                                       School of Science and Engineering, The Chinese University of Hong Kong, Shenzhen 518172, China
                                                                     2
                                                                         Shenzhen Future Network of Intelligence Institute (FNii-Shenzhen)




                                                                 Abstract                                                       Qwen3-4B       Qwen3-32B       Llama-70B    MiniMax-M3
                                                                                                                                           SFT                     MusicRLVR (SFT init.)
                                                                                                                                           Direct GRPO (R = A)     MusicRLVR (Direct)
                                            Language models now generate symbolic music                                         1.0




                                                                                                           All-satisfied rate
arXiv:2609.23665v2 [cs.SD] 7 Oct 2026




                                            from text, and research has focused on musi-                                        0.8
                                            cality. However, many applications require
                                            a score that meets explicit constraints, which                                      0.6
                                            models struggle to satisfy jointly: on Music-                                       0.4                                                   0.419
                                            ConstraintBench, our benchmark of 2,180
                                            items over eight families of programmatically                                       0.2
                                            verifiable constraints, Llama-3.1-70B satisfies                                     0.0
                                            0.630 of single-constraint items but only 0.044                                           1              2              3             4
                                            of four-constraint ones. As a remedy, we in-                                                       Number of constraints k
                                            troduce MusicRLVR, which trains a language                     Figure 1: All-satisfied rate against k over all 2,180 Mus-
                                            model with group relative policy optimisation                  icConstraintBench items, for the matched runs and the
                                            (GRPO) on verifier rewards alone, needing                      baselines of Table 2. Each slice pools every suite with that
                                            no human annotation, reward model or music-                    k (354, 614, 512 and 700 items), so slices differ in suite and
                                                                                                           family mixture (Table 51). The right-hand label gives the
                                            domain supervised fine-tuning. MusicRLVR                       Direct MusicRLVR rate at k = 4.
                                            incorporates (1) a hard validation gate that re-
                                            jects malformed scores, (2) graded per-family
                                            credit that, unlike a binary reward, separates                 programmatically from the parsed score, placing
                                            partially correct outputs, and (3) an all-satisfied            constraint-following music generation in a class of
                                            bonus for meeting every constraint at once. Ex-                property-verifiable generation problems.
                                            tensive experiments show that, in under four
                                            hours of training, MusicRLVR raises Qwen3-                        Despite this progress, current models have a
                                            4B-Instruct-2507 from 0.160 to 0.797 on mixed                  critical drawback: they struggle to satisfy such
                                            constraints, outperforming Llama-3.1-70B, and                  constraints jointly. A request may simultaneously
                                            generalises to unseen property combinations,                   require a tune to be in D minor, in 6/8, sixteen
                                            out-of-range parameters and more constraints                   bars long, ending on the tonic, with limited melodic
                                            than any training prompt. The recipe transfers                 leaps and an AABA form; because these require-
                                            to Qwen3-8B, and neither trained model loses
                                                                                                           ments must hold jointly, violating any one of them
                                            significant accuracy on general benchmarks.
                                                                                                           makes the output non-compliant. No dedicated
                                        1   Introduction                                                   benchmark isolates this capability, so we construct
                                                                                                           MusicConstraintBench, a benchmark of 2,180
                                        Language models can now generate machine-                          ABC-generation items spanning eight constraint
                                        readable symbolic scores from free-text descrip-                   families. As illustrated in Figure 1, the all-satisfied
                                        tions (Yuan et al., 2024; Qu et al., 2025; Wang et al.,            rate drops sharply as the number of simultane-
                                        2025a). For users who want a piece that satisfies                  ous constraints increases: Llama-3.1-70B satisfies
                                        explicit requirements rather than an arbitrary piece,              0.630 of single-constraint items but only 0.044 of
                                        however, a more natural interface is a score speci-                four-constraint ones. Notably, the natural solu-
                                        fication that names properties such as key, meter,                 tion of using the deterministic verifiers directly as
                                        length, pitch range, final note, rhythmic vocabu-                  reinforcement-learning rewards inherits the same
                                        lary, melodic motion, and form. Unlike perceptual                  conjunction problem when the reward is binary:
                                        quality (Cideron et al., 2024; Jonason et al., 2025;               once any constraint fails, outputs with very dif-
                                        Ziv et al., 2026), these properties can be evaluated               ferent degrees of partial compliance receive the
same reward. In group relative policy optimisation           to 0.657 on Mixed, and neither policy loses sig-
(GRPO), a group whose rollouts all receive the               nificant accuracy on IFBench, MMLU-Redux or
same reward provides no learning signal, and under           GSM8K.
this binary reward 0.550 of rollout groups in our
matched run have zero reward variance over the           2    Related Work
first 50 updates.
                                                         Symbolic music models (Sturm et al., 2016; Huang
   To tackle the above problems, we address the
                                                         et al., 2018; Yuan et al., 2024; Qu et al., 2025; Wang
following core question:
                                                         et al., 2025a; von Rütte et al., 2023; Thickstun et al.,
 Can deterministic verifiers alone teach a model         2023; Agostinelli et al., 2023; Copet et al., 2023) are
 to jointly follow multiple musical constraints?         trained by likelihood or against a learned music–text
Hence, we introduce MusicRLVR, a verifier-driven         encoder (Wu et al., 2025), with hard rules applied,
reinforcement learning method that addresses the         if at all, at decoding time (Lu et al., 2021; Huang
aforementioned question through three components:        et al., 2024; Kaliakatsos-Papakostas et al., 2025).
(1) a hard validation gate that rejects malformed        Reinforcement learning for music optimises human
or unparseable scores before any credit is assigned,     or learned quality signals (Cideron et al., 2024;
since partial credit alone would reward a fragment       Jonason et al., 2025; Ziv et al., 2026; He et al.,
that satisfies local properties without forming a        2026) or music-theory heuristics (Jaques et al.,
tune; (2) graded per-family credit that, unlike the      2017). However, none of them checks whether the
binary reward, separates partially correct outputs;      properties a prompt requests hold; in this paper, we
and (3) an all-satisfied bonus for meeting every         instead reward with deterministic verifiers whose
requested constraint at once. We summarise the           families and parameters change from item to item.
contributions of this paper as follows:                     Reinforcement learning with verifiable rewards
 • The first benchmark for joint score-constraint        (RLVR) builds on PPO-based RLHF (Schulman
   compliance. We introduce MusicConstraint-             et al., 2017; Ouyang et al., 2022) and group-relative
   Bench, the first benchmark of its kind: 2,180         baselines (Ahmadian et al., 2024; Shao et al., 2024),
   items spanning eight verifier-defined constraint      underpins reasoning models (Guo et al., 2025; Lam-
   families, plus 400 paraphrases, testing constraint    bert et al., 2024) and extends beyond mathematics
   density, unseen family combinations, parameter        (Ma et al., 2026; Gunjal et al., 2026); DAPO (Yu
   extrapolation, and wording robustness.                et al., 2026) and Dr. GRPO (Liu et al., 2025) patch
 • Turning property verifiers into fine-grained          dead groups and length bias, whereas we grade the
   training rewards. We introduce MusicRLVR,             reward itself. FollowBench (Jiang et al., 2024),
   which combines a hard validation gate, graded         IFEval (Zhou et al., 2023) and IFBench (Pyatkin
   per-family credit, and an all-satisfied bonus with-   et al., 2026), which also trains with RLVR, test
   out human annotation or a learned reward model,       text constraint following, and Wang et al. (2025b)
   giving credit across requested families and, for      build verifiable sheet-music reasoning questions.
   form, within one family. Removing or reweight-        However, our constraints act on a parsed score that
   ing any of these components lowers the all-           a fragment can partly satisfy without forming a
   satisfied rate over all 2,180 items from 0.580 to     tune, and no prompt has a target composition.
   0.502–0.553 (§5.5).
                                                         3    Method
 • Training constraint following without music-
   domain supervised fine-tuning (SFT). Exper-           In this section, we introduce MusicRLVR, a rein-
   iments show that, in under four hours of train-       forcement learning method that trains a general-
   ing on three accelerators, Direct MusicRLVR           purpose model to follow requested constraints, with
   raises the Mixed all-satisfied rate of Qwen3-4B-      deterministic verifiers as its only task-specific su-
   Instruct-2507 from 0.160 to 0.797, outperform-        pervision. As shown in Figure 2, this is achieved in
   ing every zero-shot baseline of Table 2, includ-      four steps: (A) the policy samples G ABC rollouts;
   ing Llama-3.1-70B, and generalises to property        (B) a hard validation gate rejects invalid ABC and
   combinations never observed together during           verifiers check the requested properties (§3.2); (C) a
   training, to parameter values outside the training    graded reward with an all-satisfied bonus scores the
   range and to free-form requests. The recipe           verdicts (§3.3); and (D) GRPO updates the policy
   transfers to Qwen3-8B, which rises from 0.123         with group-relative advantages (§3.4; Algorithm 1).
        Make                                    MusicRLVR: Verifiable Rewards for Constraint-Following Music Generation                                                                                                                 Verifiable
                                                                                                                                                                                                                                          Music
        Music
        with
                                                  hard validation gate · graded per-family credit · verifier-driven GRPO · no learned reward model                                                                                      Generation
        Rules!




            1      Why Constraint-Following Is Hard                                   2     MusicRLVR: verifier-driven policy training
           A One prompt can request many musical properties
                                                                                        A Sample ABC rollouts from the policy                     B     Hard validation gate + deterministic verifiers
                                                                                             Diverse melodies under the same constraints                Reject invalid ABC; check only requested properties
            Example prompt
                                                                                                 G major · 6/8 meter · AABA form                         ABC parse /                                  music21 verifiers
            "Write a monophonic tune in ABC."
                                                                                                                                                         format gate                                  (requested families only)
                   G major                  6/8 meter             AABA form                                                     ABC + melody                valid ABC                                    key: G major
                                                                                                                                                                                   if valid
                                                                                                                          M:6/8 · K:G                       required
                                                                                          LLM policy                      GAB d2B | ...                                                                  meter: 6/8
                           Eight supported constraint families
                                                                                                                                                                if invalid
                                                                                                                                                                                              form:     A      A     B      A
                  Key                Meter              Length         Range                                              M:6/8 · K:G
                                                                                                                                                      reject; no further checks

                                                                                                                          Bde d2B | ...                       Deterministic · no human reward labels · no learned reward model

                 G major                                16 bars        G3–A5
                                                                                              direct RL from              M:6/8 · K:G
             Final note             Rhythm         Melodic leap      Structure            Qwen3-4B-Instruct-2507
                                                                                                                          GGAB d2 | ...
                                                                     A A B A               optional verifier-labelled                             C     Graded reward with an all-satisfied bonus
                                                                                                    SFT init                                            Credit partial compliance and reward joint success
                 = tonic             no rests                        AABA form

                           Each item activates its own requested subset.
                                                                                                              update composer
                                                                                                                                                        Average per-family credit                           All-satisfied bonus
           B Binary rewards cannot distinguish near misses
                                                                                        D Update the policy with GRPO
                                                                                             Compare rewards within each prompt group                     over the requested families                    1 only if every check passes
               Sample 1           Sample 2         Sample 3          Equal rewards
                                                                                                                                                                  Structure gets partial credit; other families are binary.
           M:6/8 K:G             M:6/8 K:G        M:6/8 K:G
                                                                                                                                                   Example: partial AABA, valid key and meter
           GAB d2B | ...         Bde dB | ...     GGAB d | ...
                                                                                                   Normalise within each prompt group
           passes                passes           passes

                                                                                           reinforce                       discourage


                     Almost-correct tunes receive the same reward.



                                                             Key idea: deterministic property checks turn partial progress into a dense, verifiable learning signal.


Figure 2: Overview of MusicRLVR. Left: Binary all-satisfied rewards cannot distinguish near misses. Right: MusicRLVR
samples G ABC rollouts, uses a hard validation gate, and verifies requested properties deterministically. Average per-family
credit (binary except for graded structure) and an all-satisfied bonus form the reward, normalised per prompt group for GRPO.

3.1   Problem Formulation                                                                                                         Verifying properties at multiple musical scales.
                                                                                                                                  Table 1 lists the eight constraint families. Seven
In this section, we formalise the task and its success
                                                                                                                                  constrain one attribute each, such as key, meter
criterion. Let F be a set of constraint families;
                                                                                                                                  or pitch range; the eighth, structure, is a cross-
we use the eight families in Table 1. A constraint
                                                                                                                                  section form constraint: a sixteen-bar tune in a
c = (f, θ) pairs a family f ∈ F with parameters
                                                                                                                                  stated form over four-bar units (AABA, AABB,
θ (e.g. f = key, θ = (G, major)). Each family
                                                                                                                                  ABAB), units sharing a letter identical note-for-
has a deterministic verifier vf : S × Θf → {0, 1},
                                                                                                                                  note and units with different letters differing. A
where S is the set of parseable scores and Θf the
                                                                                                                                  unit ua (a ∈ {1, . . . , 4}) is its sequence of M = 4
parameter space of family f . A problem is a set of
                                                                                                                                  bar signatures (pitch and duration per event); a tune
constraints C = {c1 , . . . , ck } with distinct families,
                                                                                                                                  without exactly 4M bars scores 0 on every structure
rendered into a prompt xC by a fixed template. The
                                                                                                                                  term. Writing E for the index pairs required equal,
policy πϕ , with trainable parameters ϕ, emits a
                                                                                                                                  D for those required different (minimal sets per
string y in ABC text notation (Appendices C.5–
                                                                                                                                  form in Appendix C.1) and I[·] for an indicator,
C.7); ρ extracts the ABC and applies the validation
gate of Appendix C.1, returning ρ(y) ∈ S or ⊥                                                                                                             hV                  i
on rejection. The training reward uses the binary                                                                                        vstructure = I (a,b)∈E ua = ub
                                                                                                                                                            hV                  i    (2)
indicator                                                                                                                                                · I (a,b)∈D ua ̸= ub .
                            (Q
                                          (f,θ)∈C vf (ρ(y), θ)                        ρ(y) ̸= ⊥,                                  We write vrep and vcontrast for the two factors, the
 A(y, C) =
                                 0         ρ(y) = ⊥.                                                                              repetition and contrast halves. Their conjunction is
                                                     (1)                                                                          zero whenever either fails, however close the output
At evaluation, all-satisfied rate is the fraction of all                                                                          is. Writing ua [m] for the m-th bar signature of unit
test items whose outputs pass the validation gate                                                                                 ua , the graded repetition credit
and satisfy every requested musical constraint, i.e.
                                                                                                                                                                M
the mean of A.                                                                                                                                    1           X X                 
                                                                                                                                           ē =                   I ua [m] = ub [m]                                                                  (3)
                                                                                                                                                |E|M
3.2   Constraint Families and Verifiers                                                                                                                  (a,b)∈E m=1

In this section, we present the verifiers that supply                                                                             counts how much of the required repetition is al-
every reward signal, how they are validated and                                                                                   ready in place rather than whether all of it is. The
how the key criterion is calibrated.                                                                                              verifiers are validated without annotators: all 32
Table 1: The eight constraint families, each decided by a deterministic music21 routine on the parsed score, spanning global, bar,
note, transition and cross-section properties. The third column is the default sampler’s domain; the verifier domain Θf is wider,
which the Edge split exploits. Table 20 adds each prompt sentence.

 Family           Checked over        Default sampler values
 key              global              13 keys: 8 major, 5 minor
 meter            every bar           4/4, 3/4, 6/8, 2/4; each bar must sum to the signature
 length           global              8, 12 or 16 bars, no pickup
 range            every note          4 inclusive pitch spans, e.g. G3–A5
 final            last note           a pitch class, any octave (a scale degree 1/3/5 when a key is present)
 rhythm           every note          4 admissible duration sets; no dotted values, no rests
 leap             adjacent notes      largest melodic interval: 7, 9 or 12 semitones
 structure        4-bar units         aaba, aabb or abab over 16 bars; equal letters identical, different letters distinct


constructed scores with known property values, cov-                Addressing the limitations by graded per-family
ering the eight families, receive the correct verdict;             credit. To address the aforementioned limitations,
six single-property mutations of a fully compliant                 we grade the reward per requested family and keep
tune each flip exactly the targeted family; and the                an all-satisfied bonus. In detail, for a completion y
meter check agrees with the declared meter of all                  on problem C with k = |C|,
400 IrishMAN tunes tested (Appendix C.1).                                       
                                                                                
                                                                                  0,                         ρ(y) = ⊥,
Calibrating the key criterion. The key verifier
                                                                                
                                                                                 1 X
                                                                                
is the one hybrid among the eight, because a literal               R(y, C) = λ                  sf (ρ(y), θ)
                                                                                      k
check fails in both directions: the K: header is                                        (f,θ)∈C
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                      + (1 − λ) A(y, C), else,
                                                                                
gameable, and key-profile analysis (Krumhansl,
2001; Temperley, 1999) (Aarden–Essen profiles)                                                                          (5)
agrees with the corpus header on only 0.750 of                     with λ = 0.7, which leaves the binary term 0.3 of
400 corpus tunes. We accept a tune iff the header                  the reward even at k = 1 (§5.5 and Appendix D.18
matches and the analysed key is the requested one                  vary it). Here sf : S × Θf → [0, 1] equals vf for
or its relative (Appendix C.3).                                    the seven non-structure families; for structure it
                                                                   is graded, sstructure = 0.7 ē + 0.3 vcontrast (a fixed
3.3    Gated Graded Reward                                         split, separate from λ). The λ-weighted average
In this section, we present the reward that turns                  separates rollouts satisfying different numbers of
verifier verdicts into a learning signal.                          families; holding the contrast verdict fixed, the
                                                                   graded sstructure also separates rollouts that fail
Binary all-satisfied reward and its limitations.                   the form check but match different fractions of bar
For a prompt xC , GRPO samples a group of G                        positions, which is credit within a family. We grade
rollouts {y1 , . . . , yG } and centres their rewards              repetition and keep contrast binary because exact
within that group,                                                 bar matches measure partial repetition directly (a
                                                                   symmetric variant is in Appendix E.2).
                                             G
       R(yi , C) − µC                1 X                           Guarding against fragments by a hard valida-
 Âi =                ,         µC =     R(yj , C),
          σC + ϵ                     G                             tion gate. However, paying partial credit to every
                                            j=1
                 G                                                 output would let a fragment satisfying key and
 2         1     X                   2
                                                                   range, but forming no tune, collect λ · 2/k (cf.
σC =                   R(yj , C) − µC ,
          G−1                                                      Skalse et al., 2022). As a remedy, the gate scores
                 j=1
                                                  (4)              every rejected output 0 before any credit is assigned.
with ϵ = 10−4 a small constant. Despite matching                   Training and main evaluation share the gate; under
the evaluation criterion exactly, taking R = A                     the stricter format checks of Appendix C.2, the
(Equation 1) has two limitations: (1) it separates                 matched checkpoints of Table 2 keep every success.
no partial ordering, as a rollout that misses one
constraint scores the same as one that misses all;                 3.4    Training
and (2) such ties remove the learning signal, since a              In this section, we elaborate on the training pro-
group whose rollouts all score alike contributes only              cedure, which consists of two parts, namely (1)
the Kullback–Leibler (KL) term (Appendix D.24).                    GRPO on the reward of Equation 5; and (2) an
optional music-domain SFT warm start. Direct                   Prompt: 3/4 | 8 bars | last note E | eighths and quarters only
                                                             Llama-3.1-70B: every bar half full
applies (1) to Qwen3-4B-Instruct-2507, whereas
                                                         G
SFT init. applies (2) before (1); both use the same          ✗ 3/4             ✗ 8 bars           ✓ ends on E    ✓ 8th + qtr
reward, prompt pool and GRPO settings, with the              MusicRLVR (Direct, 4B): all four hold
initial policy as the KL reference.                      G
                                                             ✓ 3/4             ✓ 8 bars           ✓ ends on E    ✓ 8th + qtr
Optimising with the verifier as the only source of       Figure 3: One High-k item, the first that Direct MusicRLVR
task supervision. In detail, both routes use GRPO        solves and Qwen3-32B, Llama-3.1-70B and MiniMax-M3 all
(Shao et al., 2024): every rollout of a group is first   fail. Llama-3.1-70B fills half of every 3/4 bar.
scored by Equation 5, its group-relative advantage
(Equation 4) is then assigned to every token, and the    the 2,180 items; both were added after the reward
policy finally maximises the PPO clipped surrogate       design was final. The held-out pairs are (key,
(Schulman et al., 2017) with a per-token KL penalty      rhythm), (meter, leap), (final, structure),
β towards the route’s initial checkpoint (Equation 6     and (length, range); none occurs together in ei-
in Appendix A). No value network is trained; the         ther training stage (Lake and Baroni, 2018; Kim
group mean µC is the baseline. We run G = 8,             and Linzen, 2020). They form a perfect matching
β = 0.04, clipping range εclip = 0.2, learning rate      over the eight families, so each family is held out
1×10−6 , 300 optimiser steps on 6,000 synthetic          once and any held-out-pair-free set has at most
prompts, with Qwen3-4B-Instruct-2507 (Yang et al.,       k = 4 (Appendix C.4). Finally, re-rendering all
2025) trained full-parameter (§B.1). The prompt          Single and Seen items with alternative wording
pool upsamples structure-containing problems from        yields a 400-item paraphrase suite with unchanged
21% to 33% (§5.5 compares both), and Table 7 gives       constraint values (Appendix C). Figure 3 shows one
all settings.                                            High-k item that Llama-3.1-70B fails and Direct
                                                         MusicRLVR solves.
Warm-starting on targets that the verifiers la-
bel themselves. The optional SFT uses 12,890             5      Experiments
instruction–tune pairs self-labelled from the Irish-     In this section, we carry out experiments to address
MAN corpus (Wu et al., 2023): for each corpus            the following questions:
tune the verifiers read candidate constraint param-
                                                          • Q1: Do existing models comply? See §5.2.
eters off the parsed score, sample k ∼ U{1, 2, 3}
                                                          • Q2: Is music-domain SFT needed? See §5.3.
families, and admit the pair only if A(y, C(y)) = 1.
                                                          • Q3: Does the gain generalise? See §5.4.
Held-out family pairs (§4) are excluded from both
                                                          • Q4: Which reward parts matter? See §5.5.
training pools. Full construction details are in
                                                          • Q5: Where are the gains largest? See §5.6.
Appendices B.4–B.6.
                                                         Additional results can be found in Appendix D.
4   MusicConstraintBench                                 5.1         Experiment Setup
In this section, we introduce MusicConstraint-           To answer the above five questions, we score greedy
Bench, which comprises five complementary tests:         completions with the all-satisfied criterion of §3
constraint density (Single, Mixed, High-k), compo-       (temperature 1.0 for the sampling-budget study).
sitional generalisation (Seen, Unseen, Dense), pa-       Baselines. Qwen3-4B-Instruct-2507, Qwen3-8B
rameter extrapolation (Edge), multi-section control      and Qwen3-32B (Yang et al., 2025), Llama-3.1-
(Structure), and linguistic variation (paraphrases).     70B (Grattafiori et al., 2024), MiniMax-M3, and
Single (n = 200) contains one constraint, High-          ChatMusician-7B (Yuan et al., 2024) all receive the
k (n = 160) four, and Mixed (n = 300) spans              same user prompt under their own chat templates
k ∈ {1, 2, 3, 4} and serves as the per-family di-        without requested reasoning; the music-domain
agnostic. Seen (n = 200) contains two or three           SFT checkpoint serves as a supervised baseline (Ap-
families that co-occur in training, whereas Unseen       pendix B.5). Training runs. The three matched
(n = 200) requires one of four held-out pairs; Struc-    runs, Direct GRPO (R = A, i.e. λ = 0), Di-
ture (n = 120) always includes the cross-section         rect MusicRLVR, and SFT-initialised MusicRLVR,
form constraint. Dense (n = 500; four constraints        share seed 43, 300 updates, and 48 completions per
with a held-out pair) and Edge (n = 500; parame-         update, and are evaluated once per suite (decoding
ters outside the RL prompt domain, §5.4) complete        variation: Appendix B.10; paired McNemar tests
Table 2: All-satisfied rate under greedy decoding on the eight MusicConstraintBench suites and over all 2,180 items.
Qwen3-4B is Qwen3-4B-Instruct-2507; the 4B RL rows are matched runs at equal budget, and RFT (rejection-sampling
fine-tuning) fine-tunes Qwen3-4B on its own verifier-accepted samples at that budget (Appendix D.7). Each column marks its
best and runner-up ; the shaded row is our main configuration. Counts and paired tests: Appendix D.13.
                                                Six original splits                               Later splits      Overall
Model                      Mixed     Single      Seen      Unseen        High-k    Structure    Dense      Edge      All
Zero-shot
Qwen3-4B                   0.160      0.225      0.100      0.040        0.037       0.100      0.008     0.010      0.068
Qwen3-8B                   0.123      0.210      0.115      0.050        0.006       0.000      0.020     0.032      0.064
Qwen3-32B                  0.363      0.535      0.250      0.190        0.094       0.267      0.074     0.112      0.204
Llama-3.1-70B              0.380      0.695      0.300      0.195        0.056       0.167      0.040     0.058      0.197
MiniMax-M3                 0.367      0.580      0.315      0.190        0.100       0.008      0.088     0.160      0.215
ChatMusician-7B            0.160      0.290      0.130      0.090        0.006       0.000      0.020     0.046      0.084
Trained (Qwen3-4B-Instruct-2507)
SFT                      0.477        0.745      0.415      0.440        0.231       0.600      0.290     0.076      0.346
RFT                      0.543        0.960      0.445      0.355        0.163       0.758      0.098     0.128      0.342
Direct GRPO (R = A)      0.797        0.960      0.745      0.565        0.469       0.908      0.322     0.300      0.545
MusicRLVR (SFT init.) 0.577           0.880      0.585      0.530        0.350       0.383      0.366     0.134      0.424
MusicRLVR (Direct)       0.807        0.985      0.815      0.595        0.575       0.967      0.362     0.310      0.580
Trained (Qwen3-8B)
MusicRLVR (Direct)         0.657      0.915      0.705      0.645        0.431       0.900      0.404     0.252      0.530


(McNemar, 1947): Appendix D.13). Reward ab-                    Table 3: One greedy decode against the best of eight samples
                                                               reranked by the verifier (temperature 1.0; Appendix D.8).
lations (§5.5) start from the Direct configuration;            Each row marks its best and runner-up .
sensitivity analyses use a separate SFT-initialised
                                                                              Qwen3-4B (zero-shot) MusicRLVR (Direct)
reference, the diagnostic study.
                                                                 Suite        Greedy      Best of 8     Greedy    Best of 8
5.2   A1: Existing Models Struggle with                          Mixed           0.160       0.393      0.807      0.897
      Multi-Constraint Music Instructions                        Single          0.225       0.685      0.985      1.000
                                                                 Seen            0.100       0.330      0.815      0.875
In this section, we evaluate the zero-shot models                Unseen          0.040       0.180      0.595      0.750
on MusicConstraintBench. As shown in Ta-                         High-k          0.037       0.050      0.575      0.756
                                                                 Structure       0.100       0.367      0.967      0.975
ble 2 and Figure 1, we observe that (1) parsing is               Dense           0.008       0.052      0.362      0.624
largely solved while joint compliance remains low:               Edge            0.010       0.090      0.310      0.448
Llama-3.1-70B writes a parseable score for 0.970 of
Mixed items yet satisfies every requested constraint           with every completion clearing the validation gate
on only 0.380, with Qwen3-32B and MiniMax-M3                   on the six original suites. Item by item, it satisfies
alongside it at 0.363 and 0.367; (2) neither size              609 of the 2,180 items that Qwen3-32B, Llama-3.1-
nor music specialisation sets the ranking: Qwen3-              70B and MiniMax-M3 all fail, against 5 the other
8B reaches 0.123 on Mixed, below the 0.160 of                  way round (Appendix F). (2) Music-domain SFT is
the smaller Qwen3-4B, and the music-specialised                not a prerequisite: under the same reward, prompt
ChatMusician-7B reaches only 0.160; (3) compli-                pool and budget, the SFT-initialised route reaches
ance is lost as constraints accumulate: Llama-3.1-             0.577 on Mixed against 0.797 for Direct and trails
70B falls 14.2× from one to four constraints, from             on seven of eight suites; pooled over the 2,180
0.630 to 0.044, whereas Direct MusicRLVR falls                 items they disagree on 765, 549 in Direct’s favour
2.4×, from 0.992 to 0.419 (Appendix D.20).                     (p < 10−4 ), and Direct stays significantly ahead
                                                               on six of the eight suites after Holm correction
5.3   A2: MusicRLVR Teaches Constraint                         (Appendix D.13). (3) The supervised initialisation
      Following Without Music-Domain SFT                       also collapses on form, clearing the repetition half
In this section, we train Qwen3-4B-Instruct-2507               of the form verifier on 119/120 Structure items
with MusicRLVR directly, without music-domain                  but the contrast half on only 50, and emitting an
SFT. As shown in Table 2, we observe that (1)                  all-identical tune on 69 (Figure 4(f)).
Direct MusicRLVR raises the Mixed all-satisfied                   Neither self-distillation nor inference-time selec-
rate from 0.160 to 0.797 and surpasses every zero-             tion substitutes for training. We further observe
shot baseline of Table 2 on all eight suites, reaching         that (1) fine-tuning Qwen3-4B on its own verifier-
0.985 on Single, 0.967 on Structure and 0.575 on               accepted samples, drawn at the sampling budget of
High-k against a best zero-shot of merely 0.100,               GRPO, reaches 0.543 on Mixed and trails Direct on
                                                                                                               binary                        SFT init.                                  graded (MusicRLVR)

                               (a) Training compliance                                                   (b) Zero-variance groups                                                   (c) Policy movement                                                    (d) Completion length
                         1.0                                                                      1.00
all-satisfied rollouts




                                                                         fraction of groups
                                                                                                                                                                                                                                                     0.3




                                                                                                                                                                                                                                 length (k tokens)
                                                                                                                                                         KL to reference
                         0.8                                                                      0.75
                                                                                                  0.50                                                                        0.2                                                                    0.2
                         0.6

                         0.4                                                                      0.25
                                                                                                                                                                                                                                                     0.1
                                                                                                  0.00                                                                        0.0
                                 0       100          200      300                                       0         100          200          300                                    0        100       200          300                                    0       100    200         300
                                         GRPO step                                                                 GRPO step                                                                 GRPO step                                                             GRPO step

                               (e) Per-family                                                            (f) Form halves                                                            (g) Sensitivity (diag.)                                                (h) Learning by family (diag.)
  rhythm                                                                                                                                                                                   Mixed         Structure                                   1.0
                                                                              fraction of items




                                                                                                                                                         all-satisfied rate
                                                                                                          0.99
    range




                                                                                                         0.97




                                                                                                                            0.97
                                                                                                         0.96




                                                                                                                    0.94
                                                                                                                                                                              1.0




                                                                                                                                                                                                                                      satisfaction
      leap                                                                                         1.0
    meter




                                                                                                                                      0.57
     final                                                                                                                                                                                                                                           0.5




                                                                                                                         0.42
                                                                                                   0.5                                                                        0.5
       key
structure                                                                                                                                                                           lr (×10−6)     β




                                                                                                                                   0.03
                                                                                                                                                                                                                G




                                                                                                                                           0.00
   length                                                                                          0.0                                                                        0.0                                                                    0.0
         0.50                                  0.75              1.00                                     repeat    contrast identical                                              0.5 1 2 5 0 .01.04 .1 4 8 16                                           50       150         250
                                 satisfied when requested                                                                                                                                                                                                          GRPO step
                                                             families in (h):                            key         meter                length                 range                   final         rhythm             leap                        structure

Figure 4: Training dynamics. (a–f) Matched runs of Table 2: “binary” and “graded” are the two Direct arms (λ = 0 and 0.7),
“SFT init.” starts from the SFT checkpoint. (a) All-satisfied rollouts. (b) Zero-variance groups. (c) KL. (d) Completion length.
(e) Per-family satisfaction. (f) Form-verifier components. (g–h) Diagnostic study: (g) sensitivity to learning rate, β and G
(dotted: reference); (h) per-family learning curves.

                         Zero-shot (best-of-k)              MusicRLVR (best-of-k)                                  MusicRLVR (greedy)                                    Table 5: All-satisfied rate beyond the training range of k (at
                                          Qwen3-4B                                                       Qwen3-8B                                                        most 3). k = 4 is Dense; k = 5–7 hold 300 items each, every
                           1.0                                                                                                                                           one with a held-out pair. Colours as in Table 2.
                           0.8         0.807
                                                                                                                                                                              Model                                                                  k=4 k=5 k=6 k=7
      All-satisfied rate




                                                                                                                                   0.713
                                                                  0.637                            0.657
                                                                                                                                                                              Qwen3-4B (zero-shot)                                                   0.008        0.003   0.000        0.000
                           0.6                                                                                                                                                SFT                                                                    0.290        0.140   0.117        0.073
                                                                                                                                                                              RFT                                                                    0.098        0.053   0.007        0.003
                           0.4                                                                                                                                                Direct GRPO (R = A)                                                    0.322        0.170   0.060        0.063
                                                                                                                                                                              MusicRLVR (SFT init.)                                                  0.366        0.187   0.200        0.117
                           0.2                                                                                                                                                MusicRLVR (Direct)                                                     0.362        0.230   0.160        0.087
                                                                                                                                                                              MusicRLVR (Direct, Qwen3-8B)                                           0.404        0.273   0.250        0.153
                           0.0
                                     1 2 4 8 16 32 64                                     1 2 4 8 16 32 64
                                 Samples per problem k                                 Samples per problem k                                                              Mixed and posts the highest Unseen and Dense rates
Figure 5: Best-of-k verifier reranking on Mixed (64 samples                                                                                                               in Table 2. As shown in Table 4, neither policy
at temperature 1.0). The dotted line is one greedy decode of                                                                                                              trades away general capability (Appendix D.4).
the trained policy.
                                                                                                                                                                          5.4           A3: MusicRLVR Generalises Beyond the
Table 4: Accuracy (%) before and after training on IFBench
(Pyatkin et al., 2026), MMLU-Redux (Gema et al., 2025) and                                                                                                                              Training Distribution
GSM8K (Cobbe et al., 2021). No difference is significant
(paired exact McNemar, p ≥ 0.096). Shading as in Table 2.
                                                                                                                                                                         In this section, we test the trained policy beyond
                                                                                                                                                                         its training distribution. As shown in Tables 2
                                                                         IFBench
                                                                                                                                                                         and 5, we observe that (1) the gain transfers to
  Model                                                                 strict loose MMLU-Redux GSM8K
                                                                                                                                                                         held-out pairs. Every Unseen item requires one of
  Qwen3-4B (zero-shot)                                                  32.0 33.3                                  83.9                   93.9
  MusicRLVR (Direct)                                                    29.3 31.7                                  84.4                   94.1                           the four family pairs excluded from both training
  Qwen3-8B (zero-shot)         25.7 30.3                                                                           81.5                   93.0                           pools; Direct reaches 0.595 there, three times the
  MusicRLVR (Direct, Qwen3-8B) 25.3 30.0                                                                           82.6                   93.3
                                                                                                                                                                         best zero-shot rate of 0.195 (Appendix B.8).
                                                                                                                                                                            (2) It extends to new parameter values. Edge
all eight suites (Table 2; Appendix D.7); (2) rerank-                                                                                                                    moves meters to 5/4, 2/2, 9/8, 12/8 and lengths to
ing 64 samples of the untrained Qwen3-4B with the                                                                                                                        4, 24, 32 bars and extends leap, range and rhythm
verifier reaches 0.637, below Direct’s single greedy                                                                                                                     (Table 14). Direct scores 0.300 against the strongest
decode, and the untrained Qwen3-8B needs 32 to 64                                                                                                                        zero-shot 0.160. On items whose meter or length
reranked samples to match its trained policy (Fig-                                                                                                                       no RL prompt requests, Direct reaches 0.287 and
ure 5); (3) reranking eight samples of the trained                                                                                                                       0.181, against at most 0.138 and 0.142 for any
policy raises every suite further (Table 3), to 0.897                                                                                                                    zero-shot model (Table 33).
on Mixed against 0.393 for the untrained model, so                                                                                                                          (3) It extends to more constraints than trained.
training and selection are complementary.                                                                                                                                Training prompts request at most three constraints
   The recipe also carries over to Qwen3-8B (Ap-                                                                                                                         (Appendix B.7), so every High-k and Dense item
pendix B.3), which rises from 0.123 to 0.657 on                                                                                                                          already asks for one more; Direct reaches 0.575
Table 6: Reward ablations in the Direct configuration. Each row below the default changes one part of Equation 5, keeping the
seed, budget, prompts (except the last row) and evaluation of Table 2; λ = 0 is Direct GRPO (R = A). Details: Appendix D.10.
Colours as in Table 2.
Variant                   Mixed      Single      Seen      Unseen     High-k     Structure   Dense       Edge        All
MusicRLVR (Direct)        0.807       0.985      0.815      0.595      0.575      0.967      0.362       0.310      0.580
Gate on A only            0.763       0.975      0.770      0.575      0.469      0.867      0.346       0.238      0.534
λ = 0 (R = A)             0.797       0.960      0.745      0.565      0.469      0.908      0.322       0.300      0.545
λ = 0.5                   0.703       0.985      0.665      0.545      0.406      0.883      0.246       0.302      0.502
λ = 1 (no bonus)          0.753       0.950      0.735      0.635      0.494      0.908      0.358       0.298      0.553
Binary form credit        0.777       0.980      0.785      0.590      0.481      0.900      0.360       0.242      0.546
Symmetric form credit     0.757       0.950      0.760      0.500      0.394      0.942      0.282       0.272      0.515
Equal form weights        0.753       0.940      0.740      0.570      0.475      0.942      0.352       0.290      0.544
Form share 21%            0.753       0.980      0.740      0.550      0.381      0.967      0.270       0.276      0.518


and 0.362 there. Suites at k = 5, 6 and 7 go further            in absolute value by at most 0.019 (Figure 4(e); Ap-
(Appendix D.9): the untrained Qwen3-4B satisfies                pendix D.1); (3) from the SFT checkpoint, graded
1 of their 900 items, whereas Direct MusicRLVR                  form credit lifts Structure from 0.525 to 0.808
keeps 0.230, 0.160 and 0.087, and the Qwen3-8B                  (Appendix D.15), and every learning rate, KL coef-
policy 0.273, 0.250 and 0.153, the highest at every             ficient and group size tested keeps Mixed at 0.540–
rung (Table 5).                                                 0.837, above the SFT start of 0.477 (Figure 4(g)).
   (4) It extends to free-form wording. On 60 hand-
written requests that phrase the constraints as a user          5.6    A5: The Largest Gains Are on Counting
might (Appendix D.3), Direct reaches 0.583, the                        and Structure
highest of the 4B models (Qwen3-4B: 0.067), and
                                                                In this section, we break the all-satisfied rate down
the Qwen3-8B policy reaches 0.717.
                                                                by constraint family over all 2,180 items (Ap-
                                                                pendix D.1) and observe that (1) larger zero-shot
5.5   A4: Every Reward Component Helps
                                                                models already handle the tonal families: on key
In this section, we ablate Equation 5 in the Direct             and final, Qwen3-32B and Llama-3.1-70B reach
configuration, one part at a time. As shown in                  0.719–0.868 against 0.242 and 0.278 for Qwen3-
Table 6, every change lowers the rate over all 2,180            4B, and Direct MusicRLVR stays close with 0.735
items from 0.580 to 0.502–0.553 (paired exact                   and 0.796; (2) scale falls short on counting and
McNemar, Holm-adjusted p ≤ 0.002). The default                  structure: no zero-shot model exceeds 0.378 on
is higher on 61 of the 64 variant–suite pairs, and              meter, 0.281 on length or 0.150 on structure,
every variant loses most on High-k, 0.381–0.494                 whereas Direct reaches 0.820, 0.657 and 0.658; (3)
against 0.575, where at least four families must                Direct also far exceeds every zero-shot model on
hold at once. We further observe that (1) crediting             rhythm, range and leap, 0.853–0.928 against at
outputs that the gate rejects but music21 parses                most 0.671.
lowers all eight suites, Structure by 0.100 and High-
k by 0.106; (2) dropping per-family credit (λ = 0)              6     Conclusion and Future Work
or the all-satisfied bonus (λ = 1) lowers High-k
to 0.469 and 0.494; (3) graded form credit lifts                In this paper, we frame constraint-following music
Structure to 0.967 from 0.900–0.942 under binary,               generation as a property-verifiable generation prob-
symmetric and equal-weight form rewards, and                    lem and introduce MusicConstraintBench and
training with 21% form prompts gives the lowest                 MusicRLVR, a method using only verifier rewards.
High-k rate, 0.381, even though that pool holds                 Our results show that MusicRLVR raises Qwen3-
more three-constraint prompts.                                  4B from 0.160 to 0.797 on Mixed in under four
   We also observe that (1) graded credit cuts groups           hours of training, above every zero-shot baseline
without a reward gradient from 0.550 to 0.307 over              including Llama-3.1-70B, with gains beyond the
the first 50 updates and from 0.717 to 0.660 over all           training distribution and no significant change on
300 (Figure 4(b)); (2) in the matched runs, with each           general benchmarks. This demonstrates that music
family scored only on the items requesting it, gains            models need no music-domain SFT to follow musi-
are clearly largest for length (0.558 → 0.663) and              cal constraints. For future work, we will extend the
leap (0.833 → 0.839), while the other six move                  verifiers to polyphony and richer forms.
Limitations                                               Jade Copet, Felix Kreuk, Itai Gat, Tal Remez, David
                                                            Kant, Gabriel Synnaeve, Yossi Adi, and Alexandre
The verifiers cover eight constraint families               Défossez. 2023. Simple and controllable music gen-
over monophonic ABC in Western tonal idioms;                eration. Advances in neural information processing
                                                            systems, 36:47704–47720.
polyphony and richer forms are outside this scope.
Within it, held-out family pairs, out-of-range pa-        Michael Scott Cuthbert and Christopher Ariza. 2010.
rameters, more constraints than any training prompt         music21: A toolkit for computer-aided musicology
                                                            and symbolic music data.
and hand-written free-form requests test generali-
sation (§5.4). We evaluate compliance with stated         Aryo Pradipta Gema, Joshua Ong Jun Leang, Giwon
constraints rather than musical quality, which a            Hong, Alessio Devoto, Alberto Carlo Maria Mancino,
listening study would measure.                              Rohit Saxena, Xuanli He, Yu Zhao, Xiaotang Du,
                                                            Mohammad Reza Ghasemi Madani, et al. 2025. Are
                                                            we done with mmlu? In Proceedings of the 2025
Ethics Statement                                            Conference of the Nations of the Americas Chapter
                                                            of the Association for Computational Linguistics:
The study involves no human subjects, no personal           Human Language Technologies (Volume 1: Long
data and no user-facing deployment. Supervised              Papers), pages 5069–5096.
targets derive from the publicly available IrishMAN       Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
corpus of traditional Irish music (Wu et al., 2023);        Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
the reinforcement prompts are produced by deter-            Aiesha Letman, Akhil Mathur, Alan Schelten, Alex
ministic samplers rather than drawn from a corpus.          Vaughan, et al. 2024. The llama 3 herd of models.
                                                            arXiv preprint arXiv:2407.21783.
The intended uses are settings that need a score to
meet a stated specification, such as music education,     Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar
game audio and accessibility tools. The misuse              Nath, Yunzhong He, Bing Liu, and Sean Hendryx.
we consider most likely is reading a compliance             2026. Rubrics as rewards: Reinforcement learning
                                                            beyond verifiable domains. In International Con-
score as a quality score; the verifiers certify the         ference on Learning Representations, volume 2026,
requested properties. Appendix G gives the longer           pages 127924–127945.
discussion.
                                                          Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
                                                            Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,
                                                            Shirong Ma, Xiao Bi, et al. 2025. Deepseek-r1: Incen-
References                                                  tivizing reasoning capability in llms via reinforcement
                                                            learning. arXiv preprint arXiv:2501.12948.
Andrea Agostinelli, Timo I Denk, Zalán Borsos, Jesse
  Engel, Mauro Verzetti, Antoine Caillon, Qingqing        Xuzheng He, Nan Nan, Zhilin Wang, Ziyue Kang,
  Huang, Aren Jansen, Adam Roberts, Marco Tagliasac-        Zhuoru Mo, Ao Li, Yu Pan, Xiaobing Li, Feng Yu, and
  chi, et al. 2023. Musiclm: Generating music from          Xiaohong Guan. 2026. Symphonygen: 3d hierarchi-
  text. arXiv preprint arXiv:2301.11325.                    cal orchestral generation with controllable harmony
                                                            skeleton. arXiv preprint arXiv:2604.25498.
Arash Ahmadian, Chris Cremer, Matthias Gallé,
  Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin,       Cheng-Zhi Anna Huang, Ashish Vaswani, Jakob Uszko-
  Ahmet Üstün, and Sara Hooker. 2024. Back to basics:       reit, Noam Shazeer, Ian Simon, Curtis Hawthorne,
  Revisiting reinforce-style optimization for learning      Andrew M Dai, Matthew D Hoffman, Monica Din-
  from human feedback in llms. In Proceedings of the        culescu, and Douglas Eck. 2018. Music transformer.
  62nd Annual Meeting of the Association for Compu-         arXiv preprint arXiv:1809.04281.
  tational Linguistics (Volume 1: Long Papers), pages
  12248–12267.                                            Yujia Huang, Adishree Ghatare, Yuanzhe Liu, Ziniu Hu,
                                                            Qinsheng Zhang, Chandramouli S Sastry, Siddharth
                                                            Gururani, Sageev Oore, and Yisong Yue. 2024. Sym-
Geoffrey Cideron, Sertan Girgin, Mauro Verzetti,
                                                            bolic music generation with non-differentiable rule
  Damien Vincent, Matej Kastelic, Zalán Borsos, Brian
                                                            guided diffusion. arXiv preprint arXiv:2402.14285.
  McWilliams, Victor Ungureanu, Olivier Bachem,
  Olivier Pietquin, et al. 2024. Musicrl: Aligning mu-    Natasha Jaques, Shixiang Gu, Dzmitry Bahdanau,
  sic generation to human preferences. arXiv preprint       José Miguel Hernández-Lobato, Richard E Turner,
  arXiv:2402.04229.                                         and Douglas Eck. 2017. Sequence tutor: Conserva-
                                                            tive fine-tuning of sequence generation models with
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,             kl-control. In International Conference on Machine
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias            Learning, pages 1645–1654. PMLR.
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
  Nakano, et al. 2021. Training verifiers to solve math   Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun
  word problems. arXiv preprint arXiv:2110.14168.           Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin Jiang,
  Qun Liu, and Wei Wang. 2024. Followbench: A multi-      Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  level fine-grained constraints following benchmark        Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  for large language models. In Proceedings of the 62nd     Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
  Annual Meeting of the Association for Computational       2022. Training language models to follow instruc-
  Linguistics (Volume 1: Long Papers), pages 4667–          tions with human feedback. Advances in neural
  4688.                                                     information processing systems, 35:27730–27744.

Nicolas Jonason, Luca Casini, and Bob LT Sturm. 2025.     Valentina Pyatkin, Saumya Malik, Victoria Graf, Hamish
  Smart: Tuning a symbolic music generation system          Ivison, Shengyi Huang, Pradeep Dasigi, Nathan Lam-
  with an audio domain aesthetic reward. arXiv preprint     bert, and Hanna Hajishirzi. 2026. Generalizing ver-
  arXiv:2504.16839.                                         ifiable instruction following. Advances in Neural
                                                            Information Processing Systems, 38.
Maximos Kaliakatsos-Papakostas,      Konstantinos         Xingwei Qu, Yinghao Ma, Ziya Zhou, Ka Man Lo,
 Soiledis, Theodoros Tsamis, Dimos Makris, Vassilis         Jiaheng Liu, Ruibin Yuan, Lejun Min, Xueling Liu,
 Katsouros, and Emilios Cambouropoulos. 2025.               Tianyu Zhang, Xeron Du, et al. 2025. Mupt: A
 Incorporating structure and chord constraints in           generative symbolic music pretrained transformer. In
 symbolic transformer-based melodic harmonization.          International Conference on Learning Representa-
 arXiv preprint arXiv:2512.07627.                           tions, volume 2025, pages 46753–46779.

Najoung Kim and Tal Linzen. 2020. Cogs: A compo-          John Schulman, Filip Wolski, Prafulla Dhariwal,
  sitional generalization challenge based on semantic       Alec Radford, and Oleg Klimov. 2017. Proxi-
  interpretation. In Proceedings of the 2020 conference     mal policy optimization algorithms. arXiv preprint
  on empirical methods in natural language processing       arXiv:1707.06347.
  (emnlp), pages 9087–9105.
                                                          Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
                                                            Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
Carol L Krumhansl. 2001. Cognitive foundations of
                                                            Zhang, YK Li, Yang Wu, et al. 2024. Deepseekmath:
  musical pitch. Oxford University Press.
                                                            Pushing the limits of mathematical reasoning in open
                                                            language models. arXiv preprint arXiv:2402.03300.
Brenden Lake and Marco Baroni. 2018. Generalization
  without systematicity: On the compositional skills      Joar Skalse, Nikolaus Howe, Dmitrii Krasheninnikov,
  of sequence-to-sequence recurrent networks. In In-        and David Krueger. 2022. Defining and characteriz-
  ternational conference on machine learning, pages         ing reward gaming. Advances in neural information
  2873–2882. PMLR.                                          processing systems, 35:9460–9471.

Nathan Lambert, Jacob Morrison, Valentina Pyatkin,        Bob L Sturm, Joao Felipe Santos, Oded Ben-Tal, and
  Shengyi Huang, Hamish Ivison, Faeze Brahman,              Iryna Korshunova. 2016. Music transcription mod-
  Lester James V Miranda, Alisa Liu, Nouha Dziri,           elling and composition using deep learning. arXiv
  Shane Lyu, et al. 2024. Tulu 3: Pushing frontiers in      preprint arXiv:1604.08723.
  open language model post-training. arXiv preprint
                                                          David Temperley. 1999. What’s key for key? the
  arXiv:2411.15124.
                                                            krumhansl-schmuckler key-finding algorithm recon-
                                                            sidered. Music Perception, 17(1):65–100.
Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi,
  Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin.         John Thickstun, David Hall, Chris Donahue, and Percy
  2025. Understanding r1-zero-like training: A critical     Liang. 2023. Anticipatory music transformer. arXiv
  perspective. arXiv preprint arXiv:2503.20783.             preprint arXiv:2306.08620.

Ximing Lu, Peter West, Rowan Zellers, Ronan Le Bras,      Dimitri von Rütte, Luca Biggio, Yannic Kilcher, and
  Chandra Bhagavatula, and Yejin Choi. 2021. Neuro-         Thomas Hofmann. 2023. Figaro: Controllable music
  logic decoding:(un) supervised neural text generation     generation using learned and expert features. In
  with predicate logic constraints. In Proceedings of       The Eleventh International Conference on Learning
  the 2021 Conference of the North American Chap-           Representations.
  ter of the Association for Computational Linguistics:
                                                          Yashan Wang, Shangda Wu, Jianhuai Hu, Xingjian Du,
  Human language technologies, pages 4288–4299.
                                                            Yueqi Peng, Yongxin Huang, Shuai Fan, Xiaobing
                                                            Li, Feng Yu, and Maosong Sun. 2025a. Notagen:
Xueguang Ma, Qian Liu, Dongfu Jiang, Ge Zhang, Ze-          Advancing musicality in symbolic music generation
  jun Ma, and Wenhu Chen. 2026. General-reasoner:           with large language model training paradigms. arXiv
  Advancing llm reasoning across all domains. Ad-           preprint arXiv:2502.18008.
  vances in Neural Information Processing Systems,
  38:56596–56618.                                         Zhilin Wang, Zhe Yang, Yun Luo, Yafu Li, Xiaoye Qu,
                                                            Ziqian Qiao, Haoran Zhang, Runzhe Zhan, Derek F
Quinn McNemar. 1947. Note on the sampling error             Wong, Jizhe Zhou, et al. 2025b. Towards an ai
  of the difference between correlated proportions or       musician: Synthesizing sheet music problems for
  percentages. Psychometrika, 12(2):153–157.                musical reasoning. arXiv preprint arXiv:2509.04059.
Shangda Wu, Xiaobing Li, Feng Yu, and Maosong
  Sun. 2023. Tunesformer: Forming irish tunes
  with control codes by bar patching. arXiv preprint
  arXiv:2301.02884.
Shangda Wu, Yashan Wang, Ruibin Yuan, Guo
  Zhancheng, Xu Tan, Ge Zhang, Monan Zhou, Jing
  Chen, Xuefeng Mu, Yuejie Gao, et al. 2025. Clamp
  2: Multimodal music information retrieval across
  101 languages using large language models. In Find-
  ings of the Association for Computational Linguistics:
  NAACL 2025, pages 435–451.
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
  Chengen Huang, Chenxu Lv, et al. 2025. Qwen3
  technical report. arXiv preprint arXiv:2505.09388.
Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan,
  Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan,
  Gaohong Liu, Lingjun Liu, et al. 2026. Dapo: An
  open-source llm reinforcement learning system at
  scale. Advances in Neural Information Processing
  Systems, 38:113222–113244.

Ruibin Yuan, Hanfeng Lin, Yi Wang, Zeyue Tian,
  Shangda Wu, Tianhao Shen, Ge Zhang, Yuhang Wu,
  Cong Liu, Ziya Zhou, et al. 2024. Chatmusician: Un-
  derstanding and generating music intrinsically with
  llm. In Findings of the Association for Computational
  Linguistics: ACL 2024, pages 6252–6271.

Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Sid-
   dhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou,
   and Le Hou. 2023. Instruction-following evalu-
   ation for large language models. arXiv preprint
   arXiv:2311.07911.
Alon Ziv, Sanyuan Chen, Andros Tjandra, Yossi Adi,
  Wei-Ning Hsu, and Bowen Shi. 2026. Mr-flowdpo:
  Multi-reward direct preference optimization for flow-
  matching text-to-music generation. In ICASSP 2026-
  2026 IEEE International Conference on Acoustics,
  Speech and Signal Processing (ICASSP), pages 1821–
  1825. IEEE.
               Contents of Appendix                                A     Algorithm
A Algorithm                                                   12   In this section, we present the detailed algorithm
B Experimental Settings                                       12
  B.1 Infrastructure . . . . . . . . . . . . . . . . . .      12   of MusicRLVR. Algorithm 1 runs verifier-driven
  B.2 Training Hyperparameters . . . . . . . . . . . .        13   GRPO directly or with an optional supervised
  B.3 Second Base Model . . . . . . . . . . . . . . .         13   warm start built from verified corpus-derived labels
  B.4 SFT Data Construction . . . . . . . . . . . . .         14
  B.5 SFT Training Examples . . . . . . . . . . . . .         15   (θf (y) := pf (ρ(y)), §3.4). Unless marked Direct,
  B.6 Prompt Template . . . . . . . . . . . . . . . .         15   the diagnostics below describe the SFT-initialised
  B.7 Dataset Statistics . . . . . . . . . . . . . . . . .    15   route, retaining a common initialisation for the
  B.8 Prompt Coverage, Training Overlap, and Split
           Composition . . . . . . . . . . . . . . . . .      15   reward-design comparisons.
  B.9 Reproducibility . . . . . . . . . . . . . . . . .       17
  B.10 Evaluation Nondeterminism . . . . . . . . . . .        17   Objective. For a prompt xC from the reinforce-
  B.11 Data and Code Release . . . . . . . . . . . . .        18   ment pool DRL , the behaviour policy πϕold samples
C Benchmark and Verifier Details                              19   a group {y1 , . . . , yG } and the advantage Âi of Equa-
  C.1 Verifier Implementation Details . . . . . . . . .       19
  C.2 Stricter Fixed-Instruction Gate Audit . . . . . .       20   tion 4 is assigned to every token of yi . Writing yi,t
  C.3 Key Verifier Calibration . . . . . . . . . . . . .      21   for the t-th token of yi and ri,t (ϕ) for the token-level
  C.4 Held-out Pair Rationale . . . . . . . . . . . . .       22
  C.5 ABC Notation Primer . . . . . . . . . . . . . .         22
                                                                   likelihood ratio πϕ (yi,t | xC , yi,<t )/πϕold (yi,t |
  C.6 ABC Notation: A Worked Example . . . . . . .            22   xC , yi,<t ), GRPO maximises
  C.7 Constraint Rendering Examples . . . . . . . . .         23
                                                                                  h P                     n
  C.8 Paraphrase Examples . . . . . . . . . . . . . .         23                                1 P|yi |
D Additional Experiments                                      24
                                                                     J (ϕ) = E G1 G       i=1 |yi |   t=1 min ri,t Âi ,
  D.1 Per-Family Satisfaction Across Models . . . . .         24                                                      
  D.2 Instruction Wording . . . . . . . . . . . . . . .       25                   clip(ri,t , 1−εclip , 1+εclip )Âi    (6)
  D.3 Free-Form Requests . . . . . . . . . . . . . . .        25
                                                                                                oi
  D.4 General Capability . . . . . . . . . . . . . . . .      26                    −βK    b i,t ,
  D.5 Paraphrase and Training Dynamics . . . . . . .          26
  D.6 Rejection Sampling and a Music-Specialised Base-             where the expectation is over problems C and their
           line . . . . . . . . . . . . . . . . . . . . . .   26
  D.7 Rejection-Sampling Fine-Tuning . . . . . . . .          27   sampled groups, |yi | counts completion tokens,
  D.8 Training versus Inference-Time Selection . . . .        27                                      b i,t = ed − d − 1
                                                                   εclip = 0.2 is the clipping range, K
  D.9 Constraint-Count Ladder . . . . . . . . . . . .         27   with d = log πref (yi,t | ·) − log πϕ (yi,t | ·) is the
  D.10 Direct Reward Ablations . . . . . . . . . . . . .      28
  D.11 Edge Subsets and a Stricter Key Criterion . . . .      28   per-token KL estimator of Shao et al. (2024), πϕold
  D.12 Significance Tests . . . . . . . . . . . . . . . .     29   is a detached copy of πϕ (one update per rollout
  D.13 Matched Comparison . . . . . . . . . . . . . .         29
  D.14 Diagnostic Reference Results . . . . . . . . . .       30
                                                                   batch), and πref is the route’s initial checkpoint
  D.15 Diagnostic Reward-Design Ablations . . . . . .         30   (hyperparameters in Appendix B.2).
  D.16 Fixed-Checkpoint Evaluation . . . . . . . . . .        30
  D.17 Hyper-parameter Sweeps . . . . . . . . . . . .         30   B     Experimental Settings
  D.18 Reward Mixing Weight . . . . . . . . . . . . .         31
  D.19 Per-Family Satisfaction on the Original Suites .       32   In this section, we present the detailed experimen-
  D.20 Performance by Number of Constraints (k) . . .         32
  D.21 Variety and Degeneration of the Matched Check-              tal settings, including the infrastructure, hyper-
           points . . . . . . . . . . . . . . . . . . . .     32   parameters, SFT data, prompt template and dataset
  D.22 Length-Controlled Output Statistics . . . . . . .      35   statistics.
  D.23 Output Length Statistics . . . . . . . . . . . . .     35
  D.24 Zero-Variance Groups During Training . . . . .         35
  D.25 Additional Training Curves . . . . . . . . . . .       36   B.1    Infrastructure
  D.26 Additional Diagnostics . . . . . . . . . . . . .       36   In this section, we describe the training stack, which
E Error and Structure Analysis                                36
  E.1 Which Constraint Binds, by Split . . . . . . . .        36   uses ms-swift’s GRPO implementation with a cus-
  E.2 Structure Reward Variants . . . . . . . . . . . .       36   tom reward plugin that shells out to the evaluation
  E.3 Structure Results by Form Type . . . . . . . . .        38   verifiers, so training and benchmarking share one
F Qualitative Examples                                        39
                                                                   music21 build. On these accelerators, co-locating
G Broader Impact                                              48
                                                                   the vLLM rollout engine with the training state
                                                                   is infeasible for full-parameter 4B training: the
                                                                   sleeping engine’s memory pool still counts against
                                                                   the training process and the backward pass fails
                                                                   at a fixed allocation point regardless of batch size.
                                                                   Serving rollouts from a dedicated device solves
                                                                   it. Two further settings are required on this stack:
 Algorithm 1:MusicRLVR: verifier-only                         Algorithm 1:    MusicRLVR (continued):
 GRPO with optional self-labelled SFT                         verifier-driven GRPO
  Input: initial policy πϕ0 ; optional SFT flag u and          πϕ ← πref
           corpus tunes Y; families F with verifiers           // Verifier-driven GRPO (§3.4)
           {vf } and parser ρ; held-out pairs H; held-out      for step s = 1, . . . , T do
           retries N ; reinforcement pool DRL (no                   ϕold ← ϕ (detached)
           prompt contains a pair in H; structure share             sample a batch of prompts xC , C ∼ DRL
           33%); reward weight λ; group size G; β, εclip ,          foreach xC in the batch do
           ϵ; steps T ; learning-rate schedule ηs                        sample a group
  Output: trained policy πϕ                                                {y1 , . . . , yG } ∼ πϕold (· | xC )
  πref ← πϕ0                                                             score every yi by R(yi , C) (Equation 5)
                                                                                                      
  if u is enabled then                                                   Âi ← R(yi , C) − µC /(σC + ϵ) for
       // Optional self-labelled supervised                                every i (Equation 4)            // Âi = 0 for
            fine-tuning (§3.4)                                             every i if σC = 0
       D←∅                                                          end
       foreach y ∈ Y do                                             accumulate ∇ϕ (−J (ϕ)) over the batch, clip its
             C(y) ← null; draw k ∼ U{1, 2, 3}                         norm to 1.0, AdamW step at ηs
             for attempt = 1, . . . , N do                            // Equation 6
                  sample F ⊆ Fy (families measurable
                    on y), |F | = min(k, |Fy |)                end
                  C ← {(f, θf (y)) : f ∈ F } with
                    θf (y) = pf (ρ(y)) read off ρ(y)
                  if C contains no pair in H then            range never binds. In the default diagnostic GRPO
                    C(y) ← C; break                          run no completion reaches the 768-token cap: the
             end                                             longest sampled completion over training is 492
             if C(y) = null then
                  C(y) ← one constraint drawn from y’s       tokens, and the trainer’s truncation counter stays at
                    properties             // singleton:     zero.
                    trivially held-out-free
             end                                             B.3   Second Base Model
             if A(y, C(y)) = 1 then
                  D ← D ∪ {(xC(y) , y)}           // else    In this section, we describe the Qwen3-8B run,
                    this draw of y is discarded              which applies the Direct recipe unchanged: λ =
             end
             // with prob. 0.2: a
                                                             0.7, seed 43, 300 updates of 48 completions with
                 structure-only pair from y’s                G = 8, learning rate 10−6 , β = 0.04 and a 768-
                 first two 4-bar units,                      token completion cap. Qwen3-8B is a hybrid rea-
                 re-verified the same way
       end
                                                             soning model; training and evaluation use its chat
       πref ← fine-tune πϕ0 on D                             template with thinking disabled, as does the zero-
  end                                                        shot Qwen3-8B row of Table 2. The larger model
                                                             trains on two policy devices with ZeRO-3 and CPU
disabling the NZ tensor layout (it corrupts weight           offload of parameters and optimiser state (micro-
synchronisation during RL) and capping the rollout           batch 1, accumulation 24), which changes memory
engine’s context length, which otherwise reserves            layout but not the update; a further device serves
key-value cache for the model’s full 262,144-token           rollouts. The run takes 15.7 hours.
window.                                                      Where the two base models differ. The 4B base
B.2   Training Hyperparameters                               is the instruction-tuned Qwen3-4B-Instruct-2507
                                                             release, whereas Qwen3-8B is the original hybrid
In Table 7, we list the settings of the optional SFT,        release used with thinking disabled; zero-shot, the
the matched GRPO runs of Table 2 and the seed-42             smaller model is the stronger of the two (0.160
diagnostic GRPO run; both GRPO configurations                against 0.123 on Mixed). After training, the 4B
keep 48 completions per update. The saved trainer            and 8B policies reach 0.807 and 0.657 on Mixed.
configurations carry the remaining optimiser de-             On the Structure suite the 8B policy reaches 0.900
faults.                                                      (108/120), despite its base parsing only 19 of the
Figure 6 shows the supervised stage, run for a               120 prompts, showing that the same Direct recipe
fixed two-epoch budget. Two diagnostics from the             can recover strong form control from a weak zero-
GRPO logs are worth recording alongside it. The              shot starting point. The 4B policy remains stronger
clipped fraction of Equation 6 is identically zero           on Structure at 0.967, while the 8B policy posts
at all 300 steps, as expected when one optimiser             the highest Unseen and Dense rates in Table 2,
update follows each rollout batch, so the clipping           supporting transfer of the same recipe across model
 Table 7: Hyperparameters of the optional SFT, the matched GRPO runs (seed 43) and the seed-42 diagnostic GRPO run. TP:
 tensor-parallel degree; mem. frac.: the rollout engine’s memory fraction.

                                                    Optional SFT                                    GRPO (matched)          GRPO (diagnostic)
            Base model                                                               Qwen3-4B-Instruct-2507
            Parameters trained                           Full                                  Full                               Full
            Training data                            12,890 pairs                        6,000 prompts                      6,000 prompts
            Optimiser                                  AdamW                                AdamW                              AdamW
            Learning rate                             1 × 10−5                             1 × 10−6                           1 × 10−6
            LR schedule                                Cosine                                Cosine                             Cosine
            Warmup (fraction of steps)                    3%                                   2%                                 2%
            Batch size (per device × devices)        4 × 3 pairs                      2 × 2 completions                   2 × 3 completions
            Gradient accumulation                          4                                    12                                 8
            Effective batch per optimiser step         48 pairs                         48 completions                      48 completions
            Epochs / steps                       2 epochs (538 steps)                       300 steps                          300 steps
            Max sequence / completion length           1536 / –                            1536 / 768                         1536 / 768
            Group size (G)                                 –                                    8                                  8
            KL coefficient (β)                             –                                  0.04                               0.04
            Clipping range (εclip )                        –                                   0.2                                0.2
            Rollout temperature                            –                                   1.0                                1.0
            λ (Equation 5)                                 –                                   0.7                                0.7
            Structure share in data                     16.5%                    33.1% (upsampled from 21%)                     33.1%
            Precision                                    bf16                                 bf16                               bf16
            Devices                                        3                           2 train + 1 rollout                3 train + 1 rollout
            Rollout engine (vLLM)                          –                        TP = 1, mem. frac. 0.92             TP = 1, mem. frac. 0.9
            Framework                               ms-swift 4.2.3                       ms-swift 4.2.3                     ms-swift 4.2.3
            Wall time                                 ∼45 min                              ∼3.7 hours                          ∼3 hours

                                    (a) Loss                                                                   (b) Token accuracy
                3                                       training                              0.8
                                                                        next-token accuracy




                                                                                                                                        0.748
                                                        validation
cross-entropy




                                                                                              0.7
                2


                                                                                              0.6
                                                          0.913
                1


                    0.0     0.5       1.0         1.5          2.0                                  0.0       0.5     1.0         1.5       2.0
                                     epoch                                                                           epoch
 Figure 6: The supervised stage. Cross-entropy (a) and next-token accuracy (b) over the two SFT epochs, for the 12,890 training
 pairs and the 125-pair validation split. Validation loss decreases to 0.913 and validation accuracy plateaus at 0.748.

 scales.                                                                                     for evaluation extract the true properties of
                                                                                             each tune: its key (hybrid policy), meter, bar
 B.4                SFT Data Construction                                                    count, pitch range, final note, the set of distinct
 In this section, we describe how the supervised                                             note durations, and the largest melodic interval.
 training data is built from the IrishMAN corpus (Wu                                      3. Instruction rendering. A random subset of
 et al., 2023), a collection of ∼45,000 traditional                                          the extracted properties is selected (with k
 Irish tunes in ABC notation. The construction                                               sampled uniformly from {1, 2, 3}, capped by
 pipeline has four steps:                                                                    the number of measurable properties) and ren-
      1. Filter and parse. Tunes whose body contains                                         dered into a constraint instruction using the
         the builder’s list of unsupported tokens, or that                                   same template as evaluation. The tune itself is
         have fewer than 4 or more than 32 written bars,                                     the target output.
         are discarded; the survivors are parsed with                                     4. Verification gate. Every (instruction, tune)
         music21 and kept only if the parsed bar count                                       pair is re-verified: the tune is checked against
         agrees with the written one.                                                        the rendered constraints using the evaluation
      2. Property extraction. The same verifiers used                                        verifiers. Any pair that fails verification is
      discarded. This ensures that no training exam-       must differ”. The paraphrase suite (§4) replaces
      ple teaches the model to produce output that         these renderers with alternative phrasings while
      violates its own constraints.                        preserving the constraint values.
   Form examples (structure family) are con-
                                                           B.7   Dataset Statistics
structed separately: for a tune with at least eight bars
whose first two four-bar units differ, the two units       In this section, we report the composition of the
are arranged into a sampled AABA/AABB/ABAB                 benchmark splits and the training data.
shape (attempted with probability 0.2 per tune;            Benchmark splits. Table 8 summarises the com-
the resulting pair carries the structure constraint        position of the six original benchmark splits. The
only). The resulting 12,890 pairs form the training        mixed suite spans k ∈ {1, 2, 3, 4} and covers all
set, with a further 125 pairs held out for valida-         eight families; the structure split is the only one
tion. Importantly, the four held-out family pairs          where every item includes the cross-section form
(§4) are enforced during construction: any pair            structure family. Family frequencies depend on
whose constraints contain a held-out combination           the sampler and exclusion rules (Table 12); the
is regenerated with a different family subset.             structure split contains its namesake family in every
B.5    SFT Training Examples                               item and one of five companion families in 66 of
                                                           120.
In this section, we present three representative
(instruction, output) pairs from the SFT training          Training data. The supervised stage uses 12,890
set to illustrate the data quality and the range of        instruction–tune pairs self-labelled from the Irish-
constraint combinations.                                   MAN corpus. The reinforcement stage uses
                                                           6,000 synthetic prompts with k ∈ {1, 2, 3}
B.6    Prompt Template                                     (2,046/3,060/894 respectively). After the reward-
In this section, we present the fixed template that        design iteration of Appendix D.15, the share of
renders every benchmark item into a prompt. The            prompts containing the structure family was
shared instruction prefix (the first paragraph) is         raised to 33.1% (1,983/6,000) to increase expo-
part of the user message of every item; the con-           sure to form constraints; every other family appears
straint block is populated from the item’s constraint      in 1,068–1,347 prompts.
list. No chain-of-thought, few-shot examples, or
                                                           B.8   Prompt Coverage, Training Overlap, and
reasoning instructions are given.
                                                                 Split Composition
      Write a single monophonic tune in ABC
      notation.
                                                           In this section, we analyse prompt coverage, overlap
      Rules: write every bar out                           with the training prompts and split composition.
      explicitly (no repeat signs like |:                  The weighting and fixed-k comparisons below use
      or :|), one voice only, no chords, no
      lyrics, no grace notes. Start with                   the diagnostic SFT-initialised reference; the suite
      an X: header, include T:, M:, L:, K:                 definitions and prompt counts apply to both studies.
      headers, then the music. Output ONLY                    The 2,180 suite items are sampled and con-
      the ABC notation and nothing else.
                                                           tain 1,623 distinct prompt strings across all eight
      The tune must satisfy ALL of the
      following constraints:                               splits. Table 9 compares each prompt with the
      – ⟨constraint 1 in natural language⟩                 user messages in both training datasets. “Set over-
      – ⟨constraint 2 in natural language⟩                 lap” ignores constraint order and compares family–
        .
        .
        .                                                  parameter sets instead. Unseen, High-k and Dense
                                                           share no complete prompt or constraint set with
   The constraint text for each family is generated        either training stage, and neither stage requests any
by a deterministic renderer that maps parameters           of the four held-out pairs. Single and Structure
to a fixed English sentence. For example, the              prompts all occur in training.
key family with θ = (D, major) renders as “the
tune must be in D major”; the structure family             Equal weighting of distinct prompts. Table 10
with θ = (AABA, 4) renders as “the tune must be            first averages repeated rows for each prompt within
exactly 16 bars with an AABA form in 4-bar units:          one evaluation, then averages over distinct prompts.
labeled units with the same letter must be note-           The RL column uses the same fixed checkpoint and
for-note identical, and units with different letters       evaluation files as Table 44. The advantage over
SFT example 1: single constraint (meter).
Instruction: Write a single monophonic tune in ABC notation . . . The tune must satisfy ALL of the following constraints: – the
meter must be 6/8, and every bar must contain exactly the right total duration.
Target (from IrishMAN):

X:89124
T:Tune
L:1/8
M:6/8
K:G
GBd gdB | GBd cBA | GBd gdB | cBA edc | GBd gdB | GBd cBA | cBA dcB | cAF G3 |
DFA cBA | GAB d2 d | DFA cBA | BAG AGE | DFA cBA | GAB d2 d | cBc dcB | cAF G3 |

Every one of the 16 bars contains exactly six eighth-note units, and the tune carries no repeat sign, so it passes the gate and the
meter verifier.
SFT example 2: two constraints (length + key).
Instruction: . . . – the tune must be exactly 32 bars long (no pickup bar). – the tune must be in D major.
Target:

X:106003
T:Tune
L:1/8
Q:1/8=180
M:6/8
K:D
DFA cdc | AFA BGE | DFA dcd | AFA gfe | DFA cdc | AFA BGE | afd bge | AFD E2 D |
DFA cdc | AFA BGE | DFA dcd | AFA gfe | DFA cdc | AFA BGE | afd bge | AFD E2 D |
fef gfg | afd AFD | fef gfg | DFA B2 A | fdf gfg | afd bge | fga Bcd | AFD E2 D |
fef gfg | afd AFD | fef gfg | DFA B2 A | fdf gfg | afd bge | fga Bcd | AFD E2 D |

The header reads K:D and content analysis returns D major; exactly 32 bars. The constraint parameters were read off this tune’s
own properties, and the pair was re-verified before admission.
SFT example 3: structure constraint (structure, AABA).
Instruction: . . . – the tune must be exactly 16 bars with an AABA form in 4-bar units: labeled units with the same letter must be
note-for-note identical, and units with different letters must differ.
Target (assembled from the source tune’s first two 4-bar units):

X:141183
T:Tune
L:1/4
M:3/4
K:Bmin
B2 c | d3 | d2 a | f e d | B2 c | d3 | d2 a | f e d |
c3 | e3 | f2 B | B3 | B2 c | d3 | d2 a | f e d |

Units 1, 2, and 4 are identical (A sections, bars 1–4, 5–8, 13–16); unit 3 (bars 9–12) differs, satisfying the AABA form. The two
units are the source tune’s first eight bars; every assembled pair is verified before entering the dataset.
Table 8: Composition of MusicConstraintBench splits: number of items, distribution over k (number of simultaneous
constraints), and family coverage, as ranges where shown.

                        Split                n    k distribution              Families (count)
                        Mixed              300    1:100, 2:100, 3:60, 4:40    All eight
                        Single             200    1:200                       All eight (16–29 each)
                        Seen comb.         200    2:116, 3:84                 All eight (51–72 each)
                        Unseen comb.       200    2:88, 3:112                 All eight (54–70 each)
                        High-k             160    4:160                       All eight (56–104 each)
                        Structure          120    1:54, 2:66                  structure: 120; 5 others


SFT persists on all eight splits under this weighting.             applies the same weighting to the three matched
On Structure, whose 120 items repeat 50 prompts,                   checkpoints of Table 2, read from the same saved
the rates are 0.637 and 0.522, respectively. Item-                 per-item files.
paired tests in the main analysis retain the original
                                                                   Fixed k does not fix family composition. Ta-
sampler weights, so they measure the sampled suites
                                                                   ble 12 gives family frequencies in High-k, Dense
rather than 2,180 distinct instructions. Table 11
                                                                   and Edge. The first two share k = 4 but are
Table 9: Coverage and overlap with either training stage.             by make_fig_degrade_pooled.py. This script
Overlap columns count sampled test rows, while “unique
prompts” counts distinct strings.                                     checks saved per-item IDs, success counts and
 Split       Items   Unique prompts     Exact overlap   Set overlap
                                                                      provenance hashes for all 24 evaluations, then ren-
 Mixed       300          222               201            203
                                                                      ders the two paired comparisons with eight-suite
 Single      200           39               200            200        Holm correction. Figure scripts read the same
 Seen        200          177               147            151
 Unseen      200          159                 0              0        saved reports or training logs; each later analysis
 High-k      160          156                 0              0        (reranking, k ladder, Edge factors, output vari-
 Structure   120           50               120            120
 Dense       500          490                 0              0        ety) names its script where it is reported. The
 Edge        500          437                32             39
                                                                      family-definition and rendering tables are main-
Table 10: Original item weighting and equal weighting of              tained descriptions of the sampler. The six origi-
unique prompts, using the main-table criterion and the diag-          nal suites were used during reward development;
nostic reference checkpoint.                                          Dense and Edge were added afterwards, without
 Split       SFT, items   SFT, unique     RL, items     RL, unique    that exposure. All training and local evaluation
 Mixed         0.477         0.402          0.663         0.615       ran on Ascend 910B2 accelerators (64 GB HBM
 Single        0.745         0.705          0.835         0.820
 Seen          0.415         0.407          0.635         0.618       each, CANN 8.2.RC1) with vLLM 0.11.0 through
 Unseen        0.440         0.396          0.595         0.547       vllm-ascend; the seed-42 diagnostic GRPO runs
 High-k        0.231         0.237          0.356         0.359
 Structure     0.600         0.522          0.808         0.637       used three policy accelerators and one rollout accel-
 Dense         0.290         0.290          0.370         0.371       erator. The matched study used two policy accelera-
 Edge          0.076         0.078          0.162         0.164
                                                                      tors and one rollout accelerator. Local models were
                                                                      served at context 4,096 and generated at most 1,200
independently sampled and have different family
                                                                      tokens per item, greedy. The hosted baselines were
mixtures. Edge additionally mixes pair-free and
                                                                      queried at temperature 0 through the NVIDIA NIM
held-out items (171/500 contain a held-out pair).
                                                                      API (integrate.api.nvidia.com), MiniMax-
Appendix D.11 scores the pair-free and held-out-
                                                                      M3 as minimaxai/minimax-m3 in August 2026,
pair halves of Edge separately. Table 13 bootstraps
                                                                      with per-model completion budgets of 800 tokens
the Dense-minus-High-k difference for each model,
                                                                      for Llama-3.1-70B, 4,000 for MiniMax-M3 and
separating item-sampling variation from this com-
                                                                      2,048 of context for ChatMusician-7B; budgets
position difference.
                                                                      and timeouts per model are in the release scripts.
   All three intervals include zero: at k = 4, re-
                                                                      The release includes per-item completions, orig-
quiring a held-out pair does not measurably lower
                                                                      inal and strict gate decisions, aggregate reports,
compliance for any of the three models. Table 12
                                                                      audit scripts, and training logs. Historical reports
gives the family composition the two splits differ
                                                                      remain unchanged; src/verifiers_legacy.py
in.
                                                                      reproduces the training and main evaluation metric,
B.9      Reproducibility                                              while src/verifiers.py implements the stricter
                                                                      gate. The reward plugin pins the historical gate
In this section, we list the scripts that
                                                                      unless strict-gate training is explicitly selected.
regenerate the paper’s tables, macros and
                                                                      src/run_verify.py defaults to this same A cri-
figures.     make_assets.py regenerates the
                                                                      terion (legacy mode).
original quantitative tables and numerical
macros; make_audit_assets.py adds the                                 B.10   Evaluation Nondeterminism
overlap, sensitivity and gate-audit tables;
                                                                      In this section, we quantify evaluation nondeter-
src/rescore_subsets.py produces the Edge-
                                                                      minism. Compliance evaluation uses temperature
subset and stricter-key tables. The historical report-
                                                                      0, yet vLLM’s batched decoding is not bitwise
ing pass, make_checkpoint_assets.py –sync,
                                                                      reproducible: evaluating the diagnostic checkpoint
computes reference-table, by-k, Edge-subset and
                                                                      (outputs/grpo_4b_v2/checkpoint-300)
fixed-k comparisons from saved verdicts, checks
                                                                      twice, on 08-22 and 08-24, with identical
ablation equivalence under the format audit, and
                                                                      serving flags (Table 15), none of the 160 high-k
supplies the fixed-checkpoint decompositions; it
                                                                      completions was byte-identical across the two
also supplies the corresponding historical figure
                                                                      runs. A plausible mechanism is that the ordering
panels. The matched tables and macros are gen-
                                                                      of floating-point reductions depends on batch
erated by make_matched_s43_assets.py after
                                                                      composition, and that the first generated token (the
all three runs finish, and the pooled by-k figure
                                                                      arbitrary X: reference number) sits on a near-tie
Table 11: The same weighting applied to the three matched checkpoints of Table 2: “items” repeats the sampler weights of
Table 2, “unique” averages within each distinct prompt first. The splits whose prompts repeat most, Single (39 distinct prompts)
and Structure (50), move most; the ordering between the three checkpoints is unchanged on every split but Edge, where the two
Direct arms swap by 0.008.

                                  Direct GRPO (R = A) MusicRLVR (SFT init.) MusicRLVR (Direct)
                     Split         items           unique       items      unique      items     unique
                     Mixed        0.797            0.741        0.577       0.527      0.807     0.760
                     Single       0.960            0.949        0.880       0.875      0.985     0.981
                     Seen         0.745            0.729        0.585       0.567      0.815     0.814
                     Unseen       0.565            0.509        0.530       0.479      0.595     0.547
                     High-k       0.469            0.458        0.350       0.353      0.575     0.571
                     Structure    0.908            0.860        0.383       0.457      0.967     0.940
                     Dense        0.322            0.322        0.366       0.363      0.362     0.358
                     Edge         0.300            0.291        0.134       0.135      0.310     0.283

Table 12: Number and percentage of items requesting each                   training pairs and 6,000 RL prompts.
family. Percentages sum to more than 100% because items
contain multiple families.                                               • Model outputs: per-item completions and per-
 Family      High-k (n = 160)    Dense (n = 500)     Edge (n = 500)        item verifier decisions (with all sub-signals) for
 key            76 (47.5%)         288 (57.6%)        168 (33.6%)          every checkpoint and baseline evaluated in this
 meter          82 (51.2%)         282 (56.4%)        160 (32.0%)          paper.
 length         60 (37.5%)         209 (41.8%)        127 (25.4%)
 range         100 (62.5%)         236 (47.2%)        164 (32.8%)        • Evaluation reports: aggregate reports, signif-
 final         104 (65.0%)         234 (46.8%)        180 (36.0%)
 rhythm         84 (52.5%)         279 (55.8%)        152 (30.4%)          icance tests, quality statistics, prompt-overlap
 leap           78 (48.8%)         270 (54.0%)        157 (31.4%)
 structure      56 (35.0%)         202 (40.4%)        148 (29.6%)          and unique-prompt analyses, strict-gate audits,
                                                                           and the training logs from which the reward
between many candidates, so a small numerical                              curves are drawn.
difference there can send the whole continuation                         • Asset generation scripts: make_assets.py
down a different path.                                                     for the initial tables, make_audit_assets.py
   The two evaluations differ by 0.040 on Mixed                            for supplementary analyses, the final reporting
and 0.050 on Structure.                                                    pass make_checkpoint_assets.py –sync,
   The first evaluation supplies the historical refer-                     and one make_fig_*.py per figure, all reading
ence and diagnostic values except Dense and Edge,                          saved reports, so every number in the paper is
which come from the re-evaluation, and Figure 7(d),                        traceable to a specific evaluation output.
which uses a separate full-retention run. The fixed-                       The IrishMAN corpus (Wu et al., 2023) used for
k comparison uses the re-evaluated High-k score                         SFT training is publicly available; source-specific
(0.394 → 0.370).                                                        rights and attribution should be preserved for
                                                                        corpus-derived targets. Model distribution follows
B.11      Data and Code Release
                                                                        the licence of the exact Qwen3-4B-Instruct-2507
We will release the code and synthetic benchmark                        checkpoint (Yang et al., 2025). No human subjects
suites under an MIT licence, with corpus-derived                        were involved in this research; all evaluation is
data and model artefacts subject to their upstream                      automated.
terms:
 • MusicConstraintBench benchmark suites:
   eight frozen JSONL files containing all 2,180
   benchmark items plus the 400-item paraphrase
   suite. Each item includes the prompt and the
   constraint specifications; the generation seed is
   a parameter of the suite sampler rather than a
   per-row field.
 • Verifier code: the eight constraint verifiers, the
   ABC parser, the reward function, the historical
   verifier, the corrected strict gate, and both sets
   of scoring reports.
 • SFT and RL data: the 12,890 supervised
Table 13: Dense minus High-k: absolute all-satisfied rate differences with percentile intervals from 20,000 within-split item
bootstrap replicates (seed 20260909).

                           Model                         High-k      Dense      ∆        95% interval
                           SFT                           0.231       0.290    +0.059   [−0.019, +0.132]
                           MusicRLVR (re-evaluated)      0.394       0.370    −0.024   [−0.111, +0.062]
                           Llama-3.1-70B                 0.056       0.040    −0.016   [−0.057, +0.021]

Table 14: Parameter values of the Edge split against the standard suites. Families are sampled by the same generator; only the
value sets differ. key, final and structure take the same values in both, so they are omitted.

                            Family    Standard suites                  Edge
                            meter     2/4, 3/4, 4/4, 6/8               5/4, 2/2, 9/8, 12/8
                            length    8, 12, 16 bars                   4, 24, 32 bars
                            leap      ≤ 7, 9, 12 semitones             ≤ 2, 3, 4 semitones
                            rhythm    three- and two-duration sets     {16th, 8th}, {quarter, half},
                                                                       {quarter}, {half}
                            range     mixed spans                      one-octave spans (C4–C5, D4–D5,
                                                                       E4–E5, G3–G4, A3–A4)

Table 15: The same checkpoint evaluated twice under greedy           key. As discussed in §3.2, the verifier uses
decoding. “Flipped” counts items whose binary all-satisfied
outcome differed between the two. Both have parse rate 1.000.        a hybrid policy: the K: header must match
 Split        n    First     Second    Flipped     0→1   1→0
                                                                     the request, and key-profile analysis of the
 Mixed       300   0.663      0.703   52 (17.3%)    32    20
                                                                     note content (score.analyze("key"), which in
 High-k      160   0.356      0.394   32 (20.0%)    19    13         music21 10.5.0 selects the Aarden–Essen profiles)
 Structure   120   0.808      0.758   26 (21.7%)    10    16
                                                                     must return the requested key or its relative ma-
                                                                     jor/minor. On a calibration set of 400 IrishMAN
C        Benchmark and Verifier Details                              tunes, this hybrid policy achieves 0.890 agreement
In this section, we present the verifier implementa-                 with the corpus key annotation, compared to 0.750
tion and its audit, the key calibration, the held-out                for content analysis alone and 1.000 (trivially) for
pairs, ABC notation and examples of the prompt                       header-only checking.
renderings.                                                          meter. The verifier checks two conditions: (1)
C.1       Verifier Implementation Details                            the time signature in the M: header matches the
                                                                     request, and (2) every non-empty bar’s total duration
In this section, we describe the validation gate and                 (notes and rests, in quarter-note equivalents) equals
the family verifiers. The historical gate ρ, which                   that signature’s bar length within 10−4 . Incomplete
is the validation gate of §3 and is also called the                  initial or final bars receive no tolerance.
parse gate below, is used in training and in all tables
labelled A, and runs first. It extracts the ABC block                length. The number of non-empty bars is
from the completion and rejects the output if extrac-                counted after parsing and compared with the re-
tion fails, if the text contains |: or :|, if music21                quest. The prompt’s “no pickup bar” is enforced
raises or exceeds a 20-second parse timeout, or if                   here as well: the first and last written bar must
the selected first part has fewer than eight notes,                  each carry a full measure of the tune’s own time
fewer than four non-empty measures, or any chord                     signature, so an output that opens with an anacrusis
object. Outputs that clear the gate are then scored                  and closes with its complement fails even when no
by the family verifiers. Appendix C.2 adds stricter                  meter constraint is requested.
format checks on the same saved completions, un-
                                                                     range. Every sounding pitch is compared against
der which the matched checkpoints of Table 2 keep
                                                                     the specified minimum and maximum (as MIDI
every success.
                                                                     numbers). Rests are ignored.
   Each of the eight constraint families is imple-
mented as a deterministic function that takes a                      final. The pitch class of the last sounding note
music21 Score object and the constraint param-                       is compared against the request; octave is always
eters, returning a binary verdict. We describe the                   ignored.
non-trivial implementation choices below.
                                                                     rhythm. Every note’s duration in quarter-note
                                                                     units, rounded to four decimals, must belong to
the admissible set, and any rest fails the check.        whereas key analysis inspects the whole score. It
A dotted or tied value therefore passes only if its      also does not reject every wrapper, missing header,
parsed duration is itself admissible.                    lyric or grace note. We retain that verifier as
                                                         verifiers_legacy.py to reproduce the saved
leap. Every pair of consecutive sounding pitches
                                                         training runs, and implement a stricter gate in
is examined; the verifier returns 0 if any interval
                                                         verifiers.py. It requires a single tune with
exceeds the stated maximum (in semitones).
                                                         the specified headers, no unconsumed wrapper text,
structure. A tune with other than sixteen non-           no repeat notation, lyrics or grace notes, and no
empty bars fails outright; otherwise it is split into    multiple parts, multiple voices, chord objects or
four units of four bars each. Each bar is reduced to     overlapping notes. Whitespace is normalised when
its signature (event type, MIDI pitch and duration       detecting wrappers. The eight family checks re-
rounded to four decimals, rests included). The min-      main unchanged. This hardens the fixed-instruction
imal pair sets are AABA: E = {(1, 2), (1, 4)},           checks.
D = {(1, 3)}; AABB: E = {(1, 2), (3, 4)},                   The stricter metric is
D = {(1, 3)}; ABAB: E = {(1, 3), (2, 4)},
D = {(1, 2)}. For each pair in E (Equation 2)                   Astrict (y, C) = A(y, C) I[gstrict (y)].
the verifier compares the bar signatures position by
                                                         audit_strict_gate.py evaluates the additional
position; for each pair in D it checks that at least
                                                         gate on saved completions; no regeneration or re-
one position differs. The graded training signal ē is
                                                         training is involved. For the configurations within
the fraction of bar positions that match across all
                                                         this manuscript’s scope, the audit covers 175 eval-
pairs in E; the binary evaluation signal requires all
                                                         uation files and 43920 rows: the three matched
to match.
                                                         checkpoints of Table 2 on all eight suites, plus the
Validation without annotators. Except for the            baseline, training-configuration, ablation, sweep,
hybrid key check, every family is a deterministic        paraphrase and retained dynamics checkpoints. All
function of the parsed score, so the question is         file-level outcomes, rejection reasons and source
whether the implementation computes the prop-            hashes are saved separately. Tables 16–17 show the
erty it claims. src/validate_verifiers.py                original six suites; Table 18 adds Dense and Edge.
builds 32 ABC scores whose property values are           Across the audit subset, 201 previously successful
fixed by construction (key 2, meter 4, length 3,         rows fail the stricter gate, and none of them belongs
range 5, final 3, rhythm 5, leap 5, structure            to the three matched RL rows of Table 2: those
5, including the inclusive bounds) and all 32 ver-       three checkpoints incur no additional gate rejection
dicts are correct. It then starts from one tune          and lose no success on any of the 6,540 items they
that satisfies six families at once and mutates          were scored on, so every rate in those three RL rows
one property at a time (length, meter, range,            is unchanged under Astrict . The main comparison
final, rhythm, leap); each mutation flips ex-            and reward curves use A; this audit measures the
actly the targeted verdict and leaves the other          additional fixed-format requirements, which are not
five unchanged. Three conventions are reported           included in the main score.
rather than asserted: a pickup bar counts against           The SFT and fixed SFT-to-GRPO checkpoints
length, an enharmonic spelling of the final pitch        incur no additional gate rejections on any of the
class is accepted, and a tune whose notes outline        eight suites. ChatMusician’s strict success rates
the relative key of its header is accepted by key.       are zero because its otherwise accepted outputs
src/validate_meter_corpus.py runs the me-                omit required headers or include wrappers. This
ter check on 400 IrishMAN tunes: the parsed time         audit therefore changes some baseline scores; a
signature equals the declared M: field on all 400.       strict-format failure is a formatting verdict.
                                                            The corrected gate has regression checks for valid
C.2   Stricter Fixed-Instruction Gate Audit              monophonic output and for multiple voices, chords,
In this section, we audit the diagnostic checkpoints     grace notes, lyrics, missing title, prose wrappers
of Table 44 and the three matched RL checkpoints         and repeat signs. Historical training uses the frozen
of Table 2 under stricter format checks.                 gate.
   The historical gate can accept a second voice
because most checks inspect only the first part,
Table 16: All-satisfied rate under the stricter fixed-instruction gate Astrict on the original-suite completions. The last three rows
are the matched checkpoints of Table 2; every one of their rates equals the corresponding A rate.
                           Model                              Mixed         Single     Seen    Unseen    High-k   Structure
                           Qwen3-4B                           0.160     0.225          0.100     0.040   0.037      0.100
                           Qwen3-8B                           0.120     0.210          0.115     0.050   0.006      0.000
                           Qwen3-32B                          0.357     0.535          0.240     0.190   0.094      0.267
                           Llama-3.1-70B                      0.377     0.695          0.300     0.190   0.050      0.167
                           MiniMax-M3                         0.367     0.580          0.315     0.190   0.100      0.008
                           ChatMusician-7B                    0.000     0.000          0.000     0.000   0.000      0.000
                           SFT                                0.477     0.745          0.415     0.440   0.231      0.600
                           MusicRLVR (diagnostic reference)   0.663     0.835          0.635     0.595   0.356      0.808
                           Direct GRPO (R = A)                0.797         0.960      0.745     0.565   0.469      0.908
                           MusicRLVR (Direct)                 0.807         0.985      0.815     0.595   0.575      0.967
                           MusicRLVR (SFT init.)              0.577         0.880      0.585     0.530   0.350      0.383


Table 17: Additional gate rejections across the six original suites (1,180 rows per model). Lost successes previously had A = 1
and now have Astrict = 0; an extra rejection need not change success if a family already failed. Reasons list only the first detected
violation per output.
        Model                              New rejects    Lost successes       Leading reasons
        Qwen3-4B                                     7                  0      non abc wrapper or unconsumed text: 7
        Qwen3-8B                                     6                  1      non abc wrapper or unconsumed text: 5, grace notes forbidden: 1
        Qwen3-32B                                   22                  4      non abc wrapper or unconsumed text: 19, repeat signs forbidden: 2
        Llama-3.1-70B                               26                  3      non abc wrapper or unconsumed text: 26
        MiniMax-M3                                   1                  0      non abc wrapper or unconsumed text: 1
        ChatMusician-7B                            749                151      missing required header: 734, non abc wrapper or unconsumed text:
                                                                               15
        SFT                                          0                 0       –
        MusicRLVR (diagnostic reference)             0                 0       –
        Direct GRPO (R = A)                          0                 0       –
        MusicRLVR (Direct)                           0                 0       –
        MusicRLVR (SFT init.)                        0                 0       –


        Table 18: Historical and strict all-satisfied rates on the two additional suites, using the same saved completions.

                 Model                                            Dense A              Dense Astrict     Edge A       Edge Astrict
                 Qwen3-4B                                             0.008                0.008          0.010             0.010
                 Qwen3-8B                                             0.020                0.020          0.032             0.032
                 Qwen3-32B                                            0.074                0.074          0.112             0.102
                 Llama-3.1-70B                                        0.040                0.038          0.058             0.056
                 MiniMax-M3                                           0.088                0.088          0.160             0.160
                 ChatMusician-7B                                      0.020                0.000          0.046             0.000
                 SFT                                                  0.290                0.290          0.076             0.076
                 MusicRLVR (diagnostic, re-evaluated)                 0.370                0.370          0.162             0.162
                 Direct GRPO (R = A)                                  0.322                0.322          0.300             0.300
                 MusicRLVR (Direct)                                   0.362                0.362          0.310             0.310
                 MusicRLVR (SFT init.)                                0.366                0.366          0.134             0.134


C.3    Key Verifier Calibration                                                Table 19: Key verifier calibration on 400 IrishMAN tunes.
                                                                               Agreement is the fraction of tunes where the verifier’s answer
In this section, we provide the full calibration data                          matches the corpus key annotation.
of the hybrid key verifier (§3.2), the most complex                                 Strategy                                              Agreement
verifier in our suite, which involves both header                                   Header only (trivially gameable)                         1.000
matching and content-based key analysis.                                            Content analysis only (Aarden–Essen profiles)            0.750
                                                                                    Content analysis with relative-key tolerance             0.890
Calibration dataset. We sampled 400 tunes from                                      Hybrid: header AND content ∈ {key, relative}             0.890
the IrishMAN corpus at random (seeded), each with
a key annotation in the K: header. We then ran                                 major passes the header-only check but fails the
four key-verification strategies and measured their                            hybrid one. The remaining 0.110 is disagreement
agreement with that annotation (Table 19):                                     between the analysis routine and that annotation,
The reference here is the corpus K: annotation,                                which modal tunes, extensive chromaticism and
which the header-only policy reproduces by con-                                very short tunes can each move. The same policy
struction. The hybrid policy matches the content-                              applies to every model we score.
with-tolerance policy on this set; its advantage
                                                                               Effect on reported numbers. The key family’s
appears when the model might game the header,
                                                                               per-constraint satisfaction rate (Table 50) is 0.862
since a policy that prints K:G above music in C
on the single split and 0.671 on the high-k split. If   Key conventions: note names C D E F G A B
we used a header-only verifier, these would be higher   denote the octave starting at middle C; lowercase c
(the model rarely writes the wrong K: header), but      d e f g a b denote one octave higher; trailing
header-only acceptance does not inspect the notes.      apostrophes (e.g. c’) raise further. A digit after
Content analysis with relative-key tolerance carries    a note name multiplies its duration by that factor
the 0.110 disagreement above; exact content-only        relative to the default length L:. Thus G2 in a
matching disagrees on 0.250 of the calibration tunes.   tune with L:1/8 is a quarter note on G. The pipe
We adopt the hybrid policy and log all sub-signals,     character | separates bars.
so future work can re-score under any policy.              Because ABC is plain text, a language model
                                                        generates it token by token in exactly the way it
C.4    Held-out Pair Rationale                          generates code or prose. The music21 library
In this section, we explain how the held-out pairs      (Cuthbert and Ariza, 2010) parses ABC into a
are chosen. The four held-out pairs (key, rhythm),      rich internal representation (pitch, duration, key
(meter, leap), (final, structure) and (length,          analysis, interval computation) that our verifiers
range) were chosen to form a perfect matching on        operate on. If parsing fails, for instance because the
the eight families, ensuring that (1) every family      model outputs prose instead of notation or uses an
participates in exactly one held-out pair, (2) no       invalid header like L:8 instead of L:1/8, the gate
family appears in multiple exclusions, and (3) the      returns ρ(y) = ⊥, so A(y, C) = 0 (Equation 1).
matching constrains the maximum testable k to 4
without touching any held-out pair, which naturally     C.6   ABC Notation: A Worked Example
defines the high-k split.                               In this section, we provide a token-by-token walk-
   The specific pairing was selected to maximise        through of a model-generated output that passes all
the diversity of inter-family interaction types:        four constraints of a high-k problem, for readers
  • key–rhythm: one harmonic, one temporal,             unfamiliar with ABC notation.
    with no obvious interaction (a tune can be in       Problem. Meter 3/4; exactly 8 bars; last note E;
    any key with any rhythm vocabulary).                eighth and quarter notes only.
  • meter–leap: one temporal, one melodic; the
                                                        Model output:
    meter determines bar duration but should not
                                                        X:17011
    affect interval size.                               T:Tune
  • final–structure: one local (last note), one         L:1/8
                                                        M:3/4
    global (16-bar form); the most interesting test     K:Edor
    of whether a model can coordinate endpoint and      B2 B2 AG | E2 E2 DE | F2 F2 ED | B2 B2 AG |
    large-scale structure without having seen them      E2 E2 DE | F2 F2 ED | B2 B2 AG | E2 E2 DE |
    together.                                           Token-by-token analysis:
  • length–range: both are “bounding” con-               • X:17011: Reference number (arbitrary, used
    straints (number of bars, pitch boundaries)            by databases).
    that interact primarily through the amount of        • T:Tune: Title (arbitrary, not constrained).
    melodic material available.
                                                         • L:1/8: Default note length is an eighth note.
   The supervised dataset contains zero instances          This means B alone is an eighth note, B2 is two
of any held-out pair, verified by an exhaustive check      eighth notes = one quarter note.
over all 12,890 pairs before training.                   • M:3/4: Time signature: three quarter notes per
C.5    ABC Notation Primer                                 bar. Since L:1/8, each bar must contain six
                                                           eighth-note equivalents. ✓ meter.
In this section, we introduce ABC notation, a plain-
                                                         • K:Edor: Key of E Dorian (E minor with raised
text format for monophonic music widely used in
                                                           sixth). The key constraint is not active in this
folk-music archives. A minimal valid tune contains
                                                           problem, so any key is acceptable.
a header block and a body:
                                                         • B2 B2 AG: Bar 1. B2 = quarter note B (two
X:1               % reference number
T:My Tune          % title
                                                           eighths); B2 = quarter note B; A = eighth note
M:4/4              % meter (time signature)                A; G = eighth note G. Total: 2 + 2 + 1 + 1 = 6
L:1/8              % default note length
K:G                % key signature                         eighth-note equivalents. ✓ meter. Durations
G2 BG dGBG | G2 Bd cAFA | G2 BG dGBG | cABG AGFG |
                                                           used: quarter, eighth. ✓ rhythm.
  • |: Bar line separator.
  • E2 E2 DE: Bar 2. Same structure. Total 6. ✓
  • . . . (bars 3–7 follow the same pattern) . . .
  • E2 E2 DE |: Bar 8 (last bar). The final token
    is E, an eighth note on pitch E. ✓ final.
Verification summary: meter ✓ (all 8 bars have 6
eighth-note equivalents); length ✓ (exactly 8 bars);
final ✓ (last note is E); rhythm ✓ (only eighth and
quarter notes appear). All four constraints satisfied;
A = 1.

C.7   Constraint Rendering Examples
In Table 21, we show the complete set of constraint-
text renderers: for each family, the table lists the
parameter types and one representative rendering.
These renderers are deterministic functions, so
every benchmark item with the same family and
parameters produces the same constraint text.
The constraint texts are designed to be unambiguous
to a musically literate reader. The meter renderer
explicitly states “every bar must contain exactly the
right total duration” because simply saying “the
meter is 3/4” could be interpreted as a header-only
requirement. Similarly, the structure renderer
spells out the matching/differing requirement rather
than assuming the model knows what AABA form
means.

C.8   Paraphrase Examples
In Table 22, we show three examples of the para-
phrase suite, which re-renders the same constraint
values with alternative wordings; they illustrate
the range of surface variation, and the constraint
parameters are unchanged.
Table 20: Table 1 with the prompt column restored. Under each family name is the span it is checked over; the second column
lists the default sampler’s values (the verifier domain Θf is wider), the third the sentence the prompt template emits for one such
value, verbatim from the renderer. structure is set apart as the only cross-section form family.

 Family                 Default sampler values                  Prompt line (one sampled value)
 key                    13 keys: 8 major, 5 minor               the tune must be in D minor
 global
 meter                  4/4, 3/4, 6/8, 2/4; each bar must       the meter must be 6/8, and every bar must contain exactly the right
 every bar              sum to the signature                    total duration
 length                 8, 12 or 16 bars, no pickup             the tune must be exactly 16 bars long (no pickup bar)
 global
 range                  4 inclusive pitch spans, e.g. G3–A5     every note must lie between G3 and A5 inclusive
 every note
 final                  a pitch class, any octave (a scale      the last note of the tune must be E (any octave)
 last note              degree 1/3/5 when a key is present)
 rhythm                 4 admissible duration sets; no dotted   use only eighth and quarter notes (no dotted notes, no other
 every note             values, no rests                        durations, no rests)
 leap                   largest melodic interval: 7, 9 or 12    melodic motion must be smooth: no melodic leap larger than a major
 adjacent notes         semitones                               sixth
 structure              aaba, aabb or abab over 16 bars;        the tune must be exactly 16 bars with an ABAB form in 4-bar units:
 4-bar units            equal letters identical, different      labeled units with the same letter must be note-for-note identical, and
                        letters distinct                        units with different letters must differ

Table 21: Constraint rendering for all eight families. The “Parameters” column shows the parameter space; the “Rendered text”
column shows the template output for one example value. Paraphrase variants (Appendix C.8) replace these templates with
alternative wordings.

                   Family           Parameters                      Rendered text (example)
                   key              key name × mode                 “The tune must be in G major.”
                   meter            time signature                  “The meter must be 3/4, and every bar must contain
                                                                    exactly the right total duration.”
                   length           bar count                       “The tune must be exactly 16 bars long (no pickup
                                                                    bar).”
                   range            low pitch, high pitch           “Every note must lie between C4 and C6 inclusive.”
                   final            pitch class; any octave         “The last note of the tune must be D (any octave).”
                   rhythm           admissible duration set         “Use only eighth and quarter notes (no dotted notes,
                                                                    no other durations, no rests).”
                   leap             max interval name               “Melodic motion must be smooth: no melodic leap
                                                                    larger than a perfect fifth.”
                   structure        form label, unit size           “The tune must be exactly 16 bars with an AABA
                                                                    form in 4-bar units: labeled units with the same
                                                                    letter must be note-for-note identical, and units with
                                                                    different letters must differ.”

Table 22: Paraphrase examples. Each row shows the original constraint text and one paraphrased variant; the constraint parameters
are identical.

             Original                                                   Paraphrased
             The tune must be in A minor.                               Compose the melody in the key of A minor.
             The meter must be 4/4, and every bar must contain          Write it in 4/4 time, and make every measure add up
             exactly the right total duration.                          to exactly the right duration.
             Melodic motion must be smooth: no melodic leap             Keep the melodic motion conjunct: no interval between
             larger than an octave.                                     consecutive notes may exceed 12 semitones.


D      Additional Experiments                                           per-family statistics report the individual verifier
                                                                        verdicts. Appendix C.2 separately reports the addi-
In this section, we present additional experiments.
                                                                        tional format-gate audit.
Appendix D.13 contains the matched comparison;
all other RL analyses in this section preserve the                       D.1    Per-Family Satisfaction Across Models
diagnostic study, with SFT initialisation unless a                       In Table 23, we break the all-satisfied rate of every
Direct row or another configuration is explicitly                        model of Table 2 down by constraint family over
named, and Table 44 collects those historical refer-                     all 2,180 items. Each cell is the fraction of items
ence scores.                                                             requesting the family whose output satisfies it; an
   Unless explicitly labelled otherwise, all-satisfied                   output rejected by the validation gate fails every
rates use A (Equation 1), as in the main comparison;
Table 23: Per-family satisfaction over all 2,180 items for every model of Table 2. Each column marks its best and runner-up ;
the shaded row is our main configuration.

        Model                      key     meter length range final rhythm leap structure                      All
        Requests                   786      773    609   744   756    761   756    733                        2180
        Zero-shot
        Qwen3-4B                   0.242   0.109    0.016    0.293    0.278    0.332    0.336      0.057      0.068
        Qwen3-8B                   0.125   0.079    0.043    0.179    0.168    0.152    0.246      0.010      0.064
        Qwen3-32B                  0.767   0.219    0.148    0.628    0.868    0.585    0.574      0.150      0.204
        Llama-3.1-70B              0.719   0.234    0.097    0.671    0.837    0.608    0.640      0.117      0.197
        MiniMax-M3                 0.468   0.248    0.281    0.456    0.460    0.250    0.452      0.030      0.215
        ChatMusician-7B            0.159   0.378    0.049    0.384    0.194    0.322    0.565      0.000      0.084
        Trained (Qwen3-4B-Instruct-2507)
        SFT                     0.660 0.724         0.819    0.777    0.333    0.603    0.683      0.610      0.346
        RFT                     0.617 0.464         0.256    0.761    0.660    0.812    0.737      0.538      0.342
        Direct GRPO (R = A) 0.719 0.820             0.565    0.907    0.788    0.937    0.819      0.644      0.545
        MusicRLVR (SFT init.) 0.670 0.872           0.844    0.867    0.487    0.629    0.798      0.506      0.424
        MusicRLVR (Direct)      0.735 0.820         0.657    0.867    0.796    0.928    0.853      0.658      0.580
        Trained (Qwen3-8B)
        MusicRLVR (Direct)         0.805   0.841    0.731    0.817    0.905    0.913    0.792      0.307      0.530


family it requests. The first row counts the items              0.587 and the matched Direct arm’s 0.553, with
requesting each family.                                         every completion clearing the parse gate. What
                                                                transfers across languages is wording variety rather
D.2    Instruction Wording                                      than the language itself, and the bottleneck is word-
In this section, we test robustness to instruction              ing generalisation within a language.
wording. Rendering the same constraint values in
different words costs the matched Direct arm 0.122              D.3     Free-Form Requests
joint satisfaction, against 0.050 for the untrained             In this section, we test requests worded as a
base model. Drawing each training prompt from                   user would write them, whereas every Music-
three renderings removes the effect (−0.018, p =                ConstraintBench prompt lists its constraints in
0.311) and costs 0.057 on Mixed, so the wording                 template sentences. We hand-write 60 requests (12,
sensitivity comes from the training distribution.               16, 16 and 16 at k = 1 to 4) that state each constraint
    Every row pairs item for item with its own orig-            in free-form English, with varied order, synonyms
inal, so the exact McNemar test applies; the con-               (measures, time signature, lowest and highest note)
straint values are identical in both members of a               and indirect phrasing (“bring it home on C”, “no
pair and only the surface form changes. Paraphrase              anacrusis”), for example “I’d like something in
re-renders the 400 single and seen-combination                  waltz time, so 3/4, and please make sure every
problems in a third English wording, never used in              measure adds up exactly.” Parameter values stay
training. Chinese re-renders the 300 Mixed items,               inside the default sampler domain and no request
and no arm is trained on the wording used there.                contains a held-out pair, so the set changes only the
    Three observations. First, the paraphrase effect            wording. Each request keeps the format rules of
scales with how much a run was trained on one                   the template, which the validation gate enforces for
wording: the matched Direct arm, the highest on the             every model, and has a twin that renders the same
original wording, loses 0.122 under paraphrase, and             constraints with the template. Both sets are scored
the untrained model loses 0.050. Second, wording                by the unchanged verifiers under the protocol of
variation in training buys invariance at a price (Ta-           Table 2 (scripts/make_bench_freeform.py;
ble 25). The English-augmented arm loses 0.05 to                paper/make_robustness_tables.py).
0.11 on Single, Seen, High-k and Structure, whose                  Table 26 reports every model we ran. Direct
items contain no held-out pair, and stays within                MusicRLVR has the highest free-form rate among
0.005 of the matched Direct arm on Unseen and                   the 4B models, 0.583, and item by item solves
Dense, where every item contains one; the mul-                  more free-form requests than each of them: 11 to
tilingual arm loses on every suite. Third, adding               3 against Direct GRPO (R = A), 21 to 9 against
a Chinese rendering to training does not improve                the SFT-initialised run, 18 to 8 against RFT, 21 to 5
Chinese compliance: the multilingual arm reaches                against SFT and 32 to 1 against Qwen3-4B. Every
0.543 against the English-only augmented arm’s                  trained model clears the validation gate on at least
Table 24: Instruction-wording robustness on the matched runs. “Lost” and “gained” count items that flip in each direction. The
wording-augmented arm draws each training prompt from three English renderings; the multilingual arm adds a fourth, Chinese
one. Qwen3-8B’s Chinese figure is set by the parse gate: 0.74 of its completions there omit the X: reference number, which no
other arm does.

               Model                                Variant           Original   Variant   Lost   Gained       p
               Qwen3-4B zero-shot                  Paraphrase          0.163     0.113      49       29       0.031
               SFT (4B)                            Paraphrase          0.580     0.540      40       24       0.060
               Direct GRPO (R=A)                   Paraphrase          0.853     0.805      29       10      0.0034
               MusicRLVR (Direct)                  Paraphrase          0.900     0.777      54        5    1.9×10−11
               MusicRLVR (Qwen3-8B)                Paraphrase          0.810     0.787      27       18       0.233
               MusicRLVR wording-aug.              Paraphrase          0.815     0.797      21       14       0.311
               MusicRLVR multiling.-aug.           Paraphrase          0.797     0.838      13       29       0.020
               Qwen3-4B zero-shot                   Chinese            0.160     0.013      46        2    8.4×10−12
               SFT (4B)                             Chinese            0.477     0.377      52       22     0.00064
               Direct GRPO (R=A)                    Chinese            0.797     0.447     111        6    4.0×10−26
               MusicRLVR (Direct)                   Chinese            0.807     0.553      78        2    5.4×10−21
               MusicRLVR (Qwen3-8B)                 Chinese            0.657     0.187     143        2    4.8×10−40
               MusicRLVR wording-aug.               Chinese            0.740     0.587      50        4    3.8×10−11
               MusicRLVR multiling.-aug.            Chinese            0.737     0.543      74       16    4.4×10−10

Table 25: What wording augmentation costs, against the                     D.5    Paraphrase and Training Dynamics
matched Direct run under the same recipe, seed, budget and
group size. Both augmented arms spend the same 300 updates                 In Table 28, we re-render the single and seen-
over more renderings.
                                                                           combination problems with alternative wordings
 Suite         MusicRLVR (Direct)   wording-aug.    multiling.-aug.        of identical constraint values, and in Table 29, we
 Mixed                 0.807           0.740            0.737
 Single                0.985           0.915            0.915
                                                                           give the numeric values behind Figure 7(d).
 Seen                  0.815           0.715            0.680
 Unseen                0.595           0.600            0.500              D.6    Rejection Sampling and a
 High-k                0.575           0.463            0.506
 Structure             0.967           0.917            0.667                     Music-Specialised Baseline
 Dense (k=4)           0.362           0.360            0.294
 Edge                  0.310           0.292            0.270              In Table 55(b), we spend the verifier at inference
 Paraphrase            0.777           0.797            0.838              time instead: for each item we draw eight comple-
 Chinese               0.553           0.587            0.543
                                                                           tions, matching the GRPO group size G = 8 and the
                                                                           rollout temperature (1.0), from both trained models,
58 of the 60 free-form requests, against 24 and 26
                                                                           so selection sees the same per-prompt candidate
for the untrained Qwen3-4B and Qwen3-8B. The
                                                                           count as one GRPO group, and report pass@k      un-
Qwen3-8B policy reaches 0.717, the highest rate
                                                                           der the unbiased estimator (1 − n−c     k   / n
                                                                                                                          k for c
overall.
                                                                           of n samples satisfying all constraints, averaged
D.4      General Capability                                                over items). The results show that selection helps
In this section, we evaluate both Direct policies                          both models and MusicRLVR stays ahead at ev-
and their base models on three general benchmarks:                         ery matched candidate budget, on both suites, so
IFBench (Pyatkin et al., 2026), all 300 test prompts                       verifier-guided selection stacks with training rather
scored by the official strict and loose checkers                           than substituting for it; note that, unlike the trained
at the prompt level; MMLU-Redux (Gema et al.,                              policy alone, best-of-N requires the verifier and N
2025), a fixed subject-proportional sample of 1,000                        generations and N verifications at deployment.
questions answered zero-shot; and GSM8K (Cobbe                                ChatMusician-7B (Yuan et al., 2024) is eval-
et al., 2021), the full 1,319-question test split with                     uated zero-shot under the same protocol as ev-
zero-shot chain of thought. Decoding is greedy                             ery other untrained model, through its released
under each model’s own chat template with at                               Human:/Assistant: template and greedy decod-
most 4,096 new tokens, and Qwen3-8B runs with                              ing (context 2,048 tokens). Under A, it reaches
thinking disabled, as in Table 2. Table 27 gives the                       0.160 on the mixed suite and 0.000 on the struc-
item-level comparison behind Table 4; no difference                        ture split, where its parse rate is 0.158. Under the
is significant at either scale (exact McNemar, p ≥                         additional format gate its score is zero on all eight
0.096).                                                                    suites (Tables 16 and 18), mainly because required
                                                                           headers are missing. Trained on corpus ABC, it
                                                                           writes repeat signs on most form prompts, which
Table 26: Free-form requests (60 items) against their template-worded twins, which request the same constraints. “Free-form
gate” counts completions that pass the validation gate; “lost” and “gained” count items that flip from the template twin to the
free-form request; p is the exact McNemar test on these flips.

          Model                                Template           Free-form       Free-form gate   Lost   Gained        p
          Qwen3-4B (zero-shot)                      0.117            0.067             24/60         6         3       0.51
          SFT                                       0.483            0.317             60/60        12         2      0.013
          RFT                                       0.500            0.417             58/60         7         2       0.18
          Direct GRPO (R = A)                       0.700            0.450             60/60        16         1     < 0.001
          MusicRLVR (SFT init.)                     0.617            0.383             60/60        15         1     < 0.001
          MusicRLVR (Direct)                        0.717            0.583             60/60        10         2      0.039
          Qwen3-8B (zero-shot)                      0.150            0.133             26/60         4         3      1.00
          MusicRLVR (Direct, Qwen3-8B)              0.767            0.717             60/60         8         5      0.58

Table 27: General benchmarks before and after training (accuracy, %). MusicRLVR is the Direct policy at each scale; “only ours
/ base” counts items that only one of the two models answers correctly, and p is the exact McNemar test on them.

                                                     Qwen3-4B                                             Qwen3-8B
 Benchmark                      Base MusicRLVR Only ours / base                    p      Base MusicRLVR Only ours / base       p
 IFBench, strict (n = 300)      32.0       29.3                   5 / 13          0.096   25.7     25.3             4/5        1.00
 IFBench, loose (n = 300)       33.3       31.7                   9 / 14           0.40   30.3     30.0             5/6        1.00
 MMLU-Redux (n = 1,000)         83.9       84.4                    14 / 9         0.40    81.5     82.6            25 / 14     0.11
 GSM8K (n = 1,319)              93.9       94.1                   15 / 13         0.85    93.0     93.3            16 / 12     0.57

Table 28: Diagnostic study: instruction paraphrase, scored by               the verifier as the selector, pass@k is the accuracy
A (the format audit leaves these verdicts unchanged). The orig-
inal column averages the single and seen-combination splits;                of best-of-k reranking. The results in Table 30 show
the paraphrased column re-renders the same 400 problems                     that, at every budget, the trained policy outscores
with alternative wordings of identical constraint values. Rows
are the diagnostic lineage; Table 24 reports the matched runs.
                                                                            its base model reranked from the same number
                                                                            of samples. To match the trained policy’s single
 Model                Original wording   Paraphrased          ∆
                                                                            greedy decode, Qwen3-4B needs more than 64
 SFT                        0.580           0.535           -0.045
 MusicRLVR (diag.)          0.735           0.688           -0.047          reranked samples and Qwen3-8B between 32 and
                                                                            64.
the instruction forbids and the parse gate rejects.                            Table 3 extends the comparison to all eight
Its training objective is stylistic generation rather                       suites at a budget of eight samples per item.
than stated requirements.                                                   Mixed reuses the 64 samples above under
                                                                            the same estimator; the other seven suites
D.7      Rejection-Sampling Fine-Tuning                                     draw eight completions per item at temper-
In this section, we use rejection-sampling fine-                            ature 1.0 (scripts/run_rerank8_card0.sh
tuning (RFT) to ask whether the verifier’s signal                           and run_rerank8_card4.sh, summarised by
is better spent filtering supervised targets than as                        src/analyse_rerank8.py). Reranking raises
a reward. For each of the first 1,800 prompts of                            the trained policy on every suite, by 0.008 to 0.262,
the reinforcement pool we draw 8 completions                                and on every suite the untrained model’s best of
from Qwen3-4B-Instruct-2507 at temperature 1.0,                             eight stays below the trained policy’s single greedy
14,400 in all, the number GRPO samples over 300                             decode.
updates of 48. For each prompt we keep the first                            D.9   Constraint-Count Ladder
completion that passes the gate and satisfies every
requested constraint, which leaves 773 pairs, and                           In this section, we extend the number of constraints
fine-tune the full model on them for three epochs                           beyond the training range, as training prompts
(learning rate 10−5 , effective batch 16, 147 steps,                        use k ∈ {1, 2, 3}. src/gen_k_ladder.py draws
seed 43). Evaluation follows the protocol of Table 2.                       suites of 300 items at k = 2, 3, 5, 6 and 7 with the
                                                                            sampler and satisfiability filter of Dense, which is
D.8      Training versus Inference-Time Selection                           the k = 4 rung. The four held-out pairs form a
In this section, we compare training with inference-                        perfect matching over the eight families, so any set
time selection. For each Mixed item we draw 64                              of five or more families contains one; the ladder
completions at temperature 1.0 and report pass@k                            therefore keeps a held-out pair in every item at every
under the unbiased estimator of Appendix D.6; with                          rung, as Dense does, and varies only k. Because
Table 29: Diagnostic study: numeric values behind Figure 7(d). Curve rows come from a full-retention re-run of the SFT-initialised
reference configuration; “original run” gives the three checkpoints the original run retained. Its step-300 value 0.660 is a
separate evaluation of the weights Table 45 scores at 0.663, within the re-evaluation shift of Appendix B.10; the two are reported
separately. The last row uses the symmetric structure reward of Appendix E.2; it and the symmetric row of Table 45 (0.590 on
Mixed) are that reward’s two separate runs.

                  Step                                                               50       100      150    200     250      300
                  All satisfied                                                     0.570    0.593    0.633   0.687   0.693   0.703
                    meter                                                           0.716    0.852    0.901   0.926   0.914   0.926
                    final                                                           0.505    0.505    0.558   0.642   0.632   0.632
                    key                                                             0.838    0.838    0.787   0.838   0.800   0.812
                    structure                                                       0.767    0.836    0.808   0.740   0.822   0.781
                  All satisfied (original run, retained ckpts)                        –        –        –     0.630   0.640   0.660
                  All satisfied (symmetric structure reward)                        0.477    0.463    0.463   0.530   0.537   0.553

Table 30: Mixed suite: greedy all-satisfied rate and pass@k                                  Table 2.
from 64 samples at temperature 1.0.
                                                                                           • Binary form credit. sstructure = vstructure .
 Model                        Greedy       pass@1      pass@8         pass@64
                                                                                           • Symmetric form credit and equal form
 Qwen3-4B zero-shot           0.160         0.132          0.393       0.637
 SFT (4B)                     0.477         0.417          0.847       0.973                 weights. 0.5ē + 0.5d, ¯ with credit 1 for a pass-
 RFT (4B)                     0.543         0.499          0.740       0.867
 Direct GRPO (R = A)          0.797         0.765          0.878       0.920                 ing form and 0 for four identical units, and
 MusicRLVR (SFT init.)        0.577         0.653          0.946       1.000                 0.5ē + 0.5vcontrast (Appendix E.2).
 MusicRLVR (Direct)           0.807         0.778          0.897       0.937
 Qwen3-8B zero-shot           0.123         0.135          0.398       0.713
                                                                                           • Form share 21%. The prompt pool before
 MusicRLVR (Direct, 8B)       0.657         0.667          0.767       0.823                 upsampling: 1,282 of 6,000 prompts con-
                                                                                             tain structure, and k = 1/2/3 is split
length and structure cannot both be requested,                                               1,863/3,076/1,061 against 2,046/3,060/894.
k = 7 is the largest admissible value. Table 31 lists                                     Table 32 gives the counts behind the All column of
every arm evaluated on the ladder.                                                        Table 6, with exact McNemar tests against the de-
Table 31: All-satisfied rate on the constraint-count ladder                               fault, Holm-corrected over the eight arms. Without
(k = 4 is Dense). Every item contains a held-out pair; training                           the all-satisfied bonus (λ = 1) the policy fails to
prompts hold at most three constraints.                                                   parse 25 outputs: 19 repeat notes without bar lines
Model                              k=2 k=3 k=4 k=5 k=6 k=7                                until the token limit and 6 end before four bars.
Qwen3-4B (zero-shot)               0.073   0.037   0.008    0.003   0.000   0.000
SFT                                0.467   0.357   0.290    0.140   0.117   0.073
RFT                                0.530   0.207   0.098    0.053   0.007   0.003         D.11      Edge Subsets and a Stricter Key
Direct GRPO (R = A)                0.710   0.487   0.322    0.170   0.060   0.063
MusicRLVR (SFT init.)              0.630   0.403   0.366    0.187   0.200   0.117                   Criterion
MusicRLVR (Direct)                 0.647   0.530   0.362    0.230   0.160   0.087
MusicRLVR (Direct, Qwen3-8B)       0.707   0.493   0.404    0.273   0.250   0.153         In this section, we rescore Edge subsets and apply
MusicRLVR (Direct, wording-aug.)   0.680   0.477   0.360    0.167   0.117   0.087
                                                                                          a stricter key criterion; both analyses use saved
                                                                                          per-item verdicts, without regeneration or retrain-
D.10      Direct Reward Ablations                                                         ing. src/rescore_subsets.py computes the
In Table 6, we vary one part of Equation 5 at a time                                      key-sensitivity audit under the historical gate; the fi-
from the Direct configuration of Table 2. Every arm                                       nal make_checkpoint_assets.py pass uses the
uses seed 43, 300 updates of 48 completions, the                                          same A verdicts for Edge subsets.
same rollout server and the evaluation of Table 2;                                           Edge mixes two factors. Table 34 splits it by
at the first update every arm except the 21% pool                                         whether an item requests one of the four held-
samples exactly the default’s rollouts. The arms                                          out pairs. On the 329 items without a held-out
are:                                                                                      family pair, the diagnostic reference reaches 0.210
 • Gate on A only. An output that the gate rejects                                        against 0.100 for the warm start (exact McNemar
    for repeat signs or for a degenerate or polyphonic                                    p = 2.03 × 10−6 ) and 0.195 for MiniMax-M3
    score,  but that music21 still parses, receives                                       (p = 0.685), a wider margin over the warm start
      1 P                                                                                 than on Edge as a whole.
    λ k (f,θ)∈C sf instead of 0. A keeps the gate,
    so the joint term and the evaluation criterion are                                       Table 33 instead splits Edge by the factor it
    unchanged; outputs with no ABC block or no                                            extrapolates: items that request a meter outside
    parse still score 0.                                                                  {4/4, 3/4, 6/8, 2/4} and items that request a length
                                                                                          outside {8, 12, 16} bars, for every model of Table 2.
 • λ = 0, 0.5 and 1. The outer mixture of Equa-
                                                                                             The deployed key check requires the header to
    tion 5; λ = 0 is Direct GRPO (R = A) of
Table 32: Direct reward ablations over all 2,180 items: parsed outputs, solved items, and the items solved only by the variant or
only by the default, with exact McNemar p and its Holm adjustment over the eight arms.

        Variant                                Parsed       Solved         Rate          Only variant   Only default       p         Holm p
        Default                                2176          1265          0.580              –              –             –            –
                                                                                                                               −8
        Gate on A only                         2179          1164          0.534             125            226        7.7×10       3.9×10−7
        λ = 0 (R = A)                          2180          1188          0.545             152            229          0.0001       0.0002
        λ = 0.5                                2168          1095          0.502             150            320        3.2×10−15    2.6×10−14
        λ = 1 (no bonus)                       2155          1206          0.553             146            205          0.0019       0.0019
        Binary form credit                     2180          1190          0.546             129            204        4.7×10−5       0.0002
        Symmetric form credit                  2180          1122          0.515             134            277        1.5×10−12    1.0×10−11
        Equal form weights                     2178          1186          0.544             142            221        4.0×10−5     1.6×10−4
        Form share 21%                         2179          1130          0.518             188            323        2.5×10−9     1.5×10−8

Table 33: Edge all-satisfied rate on the items whose requested                              per update. Two policy accelerators use micro-
meter or length lies outside the RL prompt domain.
                                                                                            batch 2 and accumulation 12; a third serves rollouts
Model                          Unseen meter (n = 160) Unseen length (n = 127) All Edge
Qwen3-4B                               0.000                   0.000           0.010        with memory fraction 0.92. The remaining GRPO
Qwen3-8B                               0.019                   0.024           0.032
Qwen3-32B                              0.037                   0.063           0.112        settings match Table 7. Direct binary uses λ = 0
Llama-3.1-70B                          0.019                   0.055           0.058
MiniMax-M3                             0.138                   0.142           0.160        (R = A), and both MusicRLVR routes use λ = 0.7.
ChatMusician-7B                        0.044                   0.008           0.046
SFT
RFT
                                       0.144
                                       0.131
                                                               0.055
                                                               0.102
                                                                               0.076
                                                                               0.128
                                                                                            The reward weight is the only changed training
Direct GRPO (R = A)                    0.269                   0.189           0.300
MusicRLVR (SFT init.)                  0.188                   0.094           0.134
                                                                                            setting between the two Direct arms. The SFT-
MusicRLVR (Direct)                     0.287                   0.181           0.310
MusicRLVR (Direct, Qwen3-8B)           0.300                   0.260           0.252        initialised arm changes both the initial policy and
                                                                                            its fixed KL reference. All evaluations use the same
match and the analyzed key to be the requested                                              item IDs and the all-satisfied criterion A.
key or its relative (§C.3). Tables 35 and 36 hold
                                                                                            Pooled comparison. The eight suites are dis-
the historical format gate fixed and report every
                                                                                            joint item sets whose union is the 2,180 items of
rate with that tolerance and without it, that is with
                                                                                            MusicConstraintBench, so the same paired test
key satisfied only when header and analysis both
                                                                                            applies to the union. Against binary reward, Di-
give the requested key. Rates stay unchanged or
                                                                                            rect MusicRLVR satisfies 1257 items against 1196
decrease. The largest baseline decrease is 0.060
                                                                                            (0.577 against 0.549), winning 221 and losing 160
(Qwen3-32B on Unseen); the largest decrease for
                                                                                            of the 381 items on which the two disagree (exact
the fixed MusicRLVR checkpoint is 0.030 on Seen.
                                                                                            two-sided p = 0.0021). Against the SFT-initialised
The diagnostic MusicRLVR checkpoint remains
                                                                                            route it satisfies 1257 against 924, winning 549 and
the highest-scoring model on seven of the eight
                                                                                            losing 216 (p < 10−4 ); the binary-reward arm also
splits.
                                                                                            leads that route, 1196 against 924 (p < 10−4 ).
D.12       Significance Tests                                                               Per-suite breakdown. Graded credit has the
In this section, we report significance tests for                                           higher rate on all eight of the suites, and the pooled
the diagnostic reward-design comparisons; the                                               comparison above is significant (p = 0.0021).
matched Direct-versus-SFT-initialised tests are in                                          Against the SFT-initialised route, Direct is ahead
Appendix D.13.                                                                              on seven suites, six of them significant after the
   Table 37 reports exact McNemar tests for the                                             eight-suite Holm correction of Table 42. All
single-run diagnostic reward-design experiment                                              three models pass the parse gate on every original-
under the main-table success criterion, pairing the                                         suite item; on Edge the Direct MusicRLVR model
same item IDs; Appendix D.16 lists the success                                              passes 496/500, while the binary-reward and SFT-
counts underlying the historical reference rates.                                           initialised models pass 500/500 (Tables 40 and 41).
Table 38 reports the Edge comparison.
                                                                                            What the residual failures look like. Table 43
D.13       Matched Comparison                                                               decomposes the 58 Mixed items the Direct Music-
In this section, we detail the matched comparison,                                          RLVR checkpoint does not satisfy, from the same
which supplies the three 4B RL rows in Table 2.                                             saved per-item verdicts as Table 39. The failures
All runs use seed 43, checkpoint 300, the same                                              are shallow rather than pervasive: 48 of the 58 miss
6,000-prompt training pool and 48 completions                                               a single family and only 2 miss three, and none
Table 34: Diagnostic study: Edge split by held-out-pair membership, using the main-table success criterion. Pair-free items
contain none of the four held-out family pairs.

             Model                                 All (n = 500)          Pair-free (n = 329)            With held-out pair (n = 171)
             Qwen3-4B                                   0.010                     0.012                                 0.006
             Qwen3-8B                                   0.032                     0.049                                 0.000
             Qwen3-32B                                  0.112                     0.125                                 0.088
             Llama-3.1-70B                              0.058                     0.067                                 0.041
             MiniMax-M3                                 0.160                     0.195                                 0.094
             ChatMusician-7B                            0.046                     0.055                                 0.029
             SFT                                        0.076                     0.100                                 0.029
             MusicRLVR (re-evaluated)                   0.162                     0.210                                 0.070

Table 35: Diagnostic study: All-satisfied rate with the relative-key tolerance and without it (hybrid/exact key), six original suites,
holding the historical format gate fixed. Baselines show the paired rates; the two MusicRLVR rows report the fixed-checkpoint
rate under each key rule.
                      Model / key rule             Mixed         Single         Seen         Unseen         High-k       Structure
                      Qwen3-4B                   0.160/0.157   0.225/0.210   0.100/0.090   0.040/0.030    0.037/0.031   0.100/0.100
                      Qwen3-8B                   0.123/0.117   0.210/0.200   0.115/0.110   0.050/0.050    0.006/0.006   0.000/0.000
                      Qwen3-32B                  0.363/0.340   0.535/0.485   0.250/0.240   0.190/0.130    0.094/0.062   0.267/0.267
                      Llama-3.1-70B              0.380/0.370   0.695/0.675   0.300/0.295   0.195/0.185    0.056/0.056   0.167/0.167
                      MiniMax-M3                 0.367/0.363   0.580/0.550   0.315/0.310   0.190/0.185    0.100/0.100   0.008/0.008
                      ChatMusician-7B            0.160/0.147   0.290/0.280   0.130/0.120   0.090/0.085    0.006/0.000   0.000/0.000
                      SFT                        0.477/0.453   0.745/0.715   0.415/0.385   0.440/0.415    0.231/0.225   0.600/0.592
                      MusicRLVR (hybrid)            0.663         0.835         0.635         0.595          0.356         0.808
                      MusicRLVR (strict key)        0.637         0.815         0.605         0.580          0.344         0.783


Table 36: Diagnostic study: Hybrid/exact key on Dense and                      the other five suites move by at most 0.025; grad-
Edge, holding the historical format gate fixed; MusicRLVR
uses the single re-evaluation.                                                 ing contrast as well (symmetric) drops it to 0.200.
                                                                               Figure 7 traces these runs: under graded credit
 Model                                   Dense             Edge
                                                                               Structure outputs pass repetition on 0.99 and con-
 Qwen3-4B                           0.008/0.006        0.010/0.008
 Qwen3-8B                           0.020/0.018        0.032/0.032
                                                                               trast on 0.87 of items (c), and every learning rate,
 Qwen3-32B                          0.074/0.056        0.112/0.102             KL coefficient and group size tested keeps Mixed
 Llama-3.1-70B                      0.040/0.032        0.058/0.048             above the SFT start, 0.540–0.837 against 0.477 (b).
 MiniMax-M3                         0.088/0.084        0.160/0.152
 ChatMusician-7B                    0.020/0.014        0.046/0.042             In the Direct configuration (Table 6) Structure stays
 SFT                                0.290/0.266        0.076/0.070             between 0.867 and 0.967 under every variant, and
 MusicRLVR (re-evaluated)           0.370/0.342        0.162/0.150             every variant loses most on High-k.

fails the parse gate. structure has the largest                                D.16        Fixed-Checkpoint Evaluation
per-family deficit (22 of the 73 items requesting it)                          In this section, we report success counts
and the top sole miss (18 items); length is next in                            for the diagnostic reference checkpoint,
missed count (14) and key and final each miss                                  outputs/grpo_4b_v2/checkpoint-300.
11. The split-level patterns of Appendix E.1 come                              Table 46 gives its counts on the six original suites;
from the diagnostic checkpoint.                                                on Dense and Edge it reaches 185/500 and 81/500.
                                                                               Its first evaluation supplies the original-suite
D.14     Diagnostic Reference Results
                                                                               rates; the separate re-evaluation is documented
In Table 44, we give the diagnostic evaluations.                               in Appendix B.10. Success counts for the three
Unless a diagnostic explicitly states another setting,                         matched checkpoints are in Table 39.
its RL results refer to the SFT-initialised checkpoint
in this table. The Direct route is reported only                               D.17        Hyper-parameter Sweeps
from the matched runs of Table 2, so no Direct row                             In Table 47, we list the values plotted in Figure 7(b).
appears here.                                                                  Each cell is one training run per setting with a single
                                                                               parameter moved from the SFT-initialised reference
D.15     Diagnostic Reward-Design Ablations
                                                                               configuration, scored on Mixed and Structure. The
In Table 45, we run the reward-design comparison                               reward mixing weight is swept the same way in
from the SFT checkpoint of the diagnostic study.                               Appendix D.18.
The results show that raising form exposure from
21% to 33% takes Structure from 0.250 to 0.525,                                Stability across settings. Every setting exceeds
and graded form credit then takes it to 0.808 while                            the SFT Mixed baseline of 0.477. Learning rate
   Table 37: Diagnostic study: Single-run reward-design comparisons (nominal exact McNemar p) over per-item outcomes.

                           Comparison                                                                                             Mixed         Single             Seen                           Unseen         High-k        Struct.
                           Reference run vs. SFT                      < 10−4                                                                     0.002            < 10−4                      < 10−4                 0.007    < 10−4
                           Reference run vs. binary credit, 21% share 0.076                                                                      0.597             1.000                       0.312                 1.000    < 10−4
                           Reference run vs. binary credit, 33% share 0.822                                                                      0.583             0.625                       0.771                 0.678    < 10−4

                                                                                                                    binary form credit                    graded (final)

                                              (a) Zero-variance                                                           (b) Hyper-parameter sensitivity                                         (c) Structure split, decomposed
              fraction of groups




                                                                                              all-satisfied rate




                                                                                                                                                                      fraction of 120
                                   0.50                                                                                           Mixed         Structure                                              0.99
                                                                                                                    1.0                                                                     1.0                0.87    0.81
                                   0.25                                                                                                                                                     0.5
                                                                                                                    0.5
                                                                                                                          lr (×10−6)      β                                                                                   0.12
                                                                                                                                                      G
                                   0.00                                                                             0.0                                                                     0.0
                                              0        100        200           300                                       0.5 1 2 5 0 .01 .04 .1 4 8 16                                            repeat contrast all identical
                                                                                                                                                                                                                 requested
                                                       GRPO step

                                              (d) Learning curve by family                                                (e) Drift from the reference                                            (f) Completion length




                                                                                                                                                                        completion tokens
                                                                                              KL to reference
                                        1.0                                                                                                                                                 150
                         satisfaction




                                                                                                                   0.02
                                        0.5                                                                                                                                                 130
                                                                                                                   0.01
                                                                                                                                                                                            110
                                        0.0                                                                        0.00
                                              50          150          250                                                0       100         200           300                                    0          100       200      300
                                                       GRPO step                                                                   GRPO step                                                                  GRPO step
                                                   families in (d):             key               meter                       length          range           final                     rhythm                leap       structure

Figure 7: Reward-design ablations (diagnostic study). (a) Zero-variance groups. (b) Sensitivity to learning rate, β and G
(dotted: reference). (c) Form verifier decomposed. (d) Per-family satisfaction. (e–f) KL and length.

Table 38: Diagnostic study: Paired comparison on Edge.                                                                                        where 0.7 is likewise highest over all 2,180 items.
“Only RL” and “Only baseline” count discordant items in the
designated single evaluation of each model.
                                                                                                                                              Contrast distinguishes the tested weights. The
 Comparison                                        Only RL      Only baseline     Exact p                             Direction
                                                                                                                                              last two columns separate the halves of the form
 Edge: RL vs. MiniMax-M3                             62               61              1.000              No detected difference
                                                                                                                                              constraint. Repetition is satisfied on 119–120 of the
                                                                                                                                              120 items at every weight, while contrast passes 55
moves Mixed most (0.270), against 0.063 for the
                                                                                                                                              items at λ = 0.5 and 45 at λ = 1.0 against 104 at
KL coefficient and 0.123 for group size.
                                                                                                                                              the default: the decrease on Structure accompanies
   The G sweep fixes 48 completions per optimiser
                                                                                                                                              a drop in contrast, not in repetition. The all-satisfied
step. Accordingly G = 4, 8, 16 uses 12, 6, 3 prompt
                                                                                                                                              counts behind those rates are 51, 97 and 39; each
groups per step, for 3,600, 1,800, 900 prompt draws
                                                                                                                                              deficit relative to the contrast count consists of items
in 300 steps. The corresponding logged epochs are
                                                                                                                                              passing the form check and missing a co-requested
0.60, 0.30, 0.15. The sweep therefore compares al-
                                                                                                                                              family. Outputs whose four units are all identical
locations of a fixed completion budget, with prompt
                                                                                                                                              – which satisfy every required-equal pair and no
exposure falling as G grows.
                                                                                                                                              required-distinct one – rise from 15 items at the
D.18          Reward Mixing Weight                                                                                                            default to 65 and 74 at the two ends. The same
In Table 48, we move λ of Equation 5, which                                                                                                   pattern holds across the rows of Table 45: repetition
weights the per-family average against the binary                                                                                             passes 119–120 items, and the binary form pass
all-satisfied term, while every other setting stays                                                                                           count equals the contrast pass count.
at the SFT-initialised reference configuration. It is                                                                                         Where the weight can act. Write mi for the
reported separately from Table 47 because that table                                                                                          per-family average in Equation 5, setting it to
lists the values plotted in Figure 7(b), and because                                                                                          zero for a gate-rejected rollout. For λ > 0, a
the form decomposition below is what makes this                                                                                               group in which every rollout has A(yi , C) = 0
sweep interpretable.                                                                                                                          has R(yi , C) = λmi . Equation 4 then gives
   The default scores highest on both suites among                                                                                            Âi = (mi − m̄)/(σm + ϵ/λ), where σm is the
the three weights tested. Against λ = 0.7, the                                                                                                group sample standard deviation of m: the scaling
low arm’s Mixed comparison gives exact McNemar                                                                                                cancels except through the stabiliser. The mixture
p = 0.368, while its Structure score is lower (p =                                                                                            also controls the reward gap between full and par-
3.54 × 10−9 ); the high arm scores lower on both                                                                                              tial success. Consider two gate-passing rollouts
(p = 0.002 and p = 4.74 × 10−15 ). Table 6 varies                                                                                             for the same prompt: one satisfies all k families;
λ over 0, 0.5, 0.7 and 1 in the Direct configuration,                                                                                         the other fails exactly one family, retaining graded
                                       Table 39: Success counts and rates for the matched final checkpoints.

                                 Split                Direct, binary        Direct, MusicRLVR       SFT init., MusicRLVR
                                 Mixed            239/300 (0.797)              242/300 (0.807)         173/300 (0.577)
                                 Single           192/200 (0.960)              197/200 (0.985)         176/200 (0.880)
                                 Seen             149/200 (0.745)              163/200 (0.815)         117/200 (0.585)
                                 Unseen           113/200 (0.565)              119/200 (0.595)         106/200 (0.530)
                                 High-k            75/160 (0.469)               92/160 (0.575)          56/160 (0.350)
                                 Structure        109/120 (0.908)              116/120 (0.967)         46/120 (0.383)
                                 Dense            161/500 (0.322)              181/500 (0.362)         183/500 (0.366)
                                 Edge             150/500 (0.300)              155/500 (0.310)         67/500 (0.134)

Table 40: Parse-gate pass rates on the six original suites, for every model of Table 2. SFT and every GRPO-trained checkpoint
clear the gate on every item.
Model                                                     Mixed              Single        Seen         Unseen           High-k    Structure
Qwen3-4B                                                  0.513              0.450        0.510          0.545           0.362       0.925
Qwen3-8B                                                  0.367              0.465        0.345          0.305           0.219       0.158
Qwen3-32B                                                 0.973              1.000        0.960          0.945           0.938       0.983
Llama-3.1-70B                                             0.970              1.000        0.980          0.980           0.944       1.000
MiniMax-M3                                                0.577              0.670        0.565          0.465           0.531       0.083
ChatMusician-7B                                           0.693              0.800        0.680          0.670           0.575       0.158
SFT (4B)                                                  1.000              1.000        1.000          1.000           1.000       1.000
Direct GRPO (R = A)                                       1.000              1.000        1.000          1.000           1.000       1.000
MusicRLVR (SFT init.)                                     1.000              1.000        1.000          1.000           1.000       1.000
MusicRLVR (Direct)                                        1.000              1.000        1.000          1.000           1.000       1.000
RFT (4B)                                                  1.000              0.980        0.995          1.000           0.988       1.000
MusicRLVR (Direct, Qwen3-8B)                              1.000              1.000        1.000          1.000           1.000       1.000

Table 41: Parse-gate pass rates for the matched evaluations.                          0.522 (Appendix B.8). The splits differ in their
Model                   Mixed Single   Seen Unseen High-k Structure Dense    Edge
                                                                                      requested constraints and prompt weights.
Direct GRPO (R = A)     1.000   1.000 1.000   1.000    1.000   1.000   1.000 1.000
MusicRLVR (SFT init.)   1.000   1.000 1.000   1.000    1.000   1.000   1.000 1.000    length and range maintain high satisfaction
MusicRLVR (Direct)      1.000   1.000 1.000   1.000    1.000   1.000   1.000 0.992
                                                                                      across the splits.
credit s ∈ [0, 1) for that family. Their reward gap is                                D.20       Performance by Number of Constraints
                                                                                                 (k)
                                                λ(1 − s)
                 ∆R = (1 − λ) +                          ,                            In Table 52, we break the mixed suite (n = 300;
                                                   k
                                                                                      100/100/60/40 items at k = 1/2/3/4) down by
which is (1 − s)/k at λ = 1 and 0.3 + 0.7(1 − s)/k                                    the number of constraints, using the same saved
at the default. The binary term thus adds an explicit                                 diagnostic reference evaluations as Table 44. Fig-
bonus for joint satisfaction; its effect on normalised                                ure 1 instead pools all 2,180 items for the matched
advantages also depends on the other rewards in                                       runs; Table 51 lists its values.
the group. The default mixture gives the highest                                      The endpoint ratios vary across models. Llama-
compliance and the fewest all-identical outputs.                                      3.1-70B falls from 0.720 at k = 1 to 0.050 at
                                                                                      k = 4, a 14.4× drop; MiniMax-M3 falls 11.2×
D.19       Per-Family Satisfaction on the Original
                                                                                      and the untrained 4B base 13.6×. The diagnostic
           Suites
                                                                                      reference rates are 0.850 and 0.475, giving the
In this section, we break the all-satisfied rate down                                 smallest endpoint ratio in the table (1.8×), against
by family. Table 44 reports the all-satisfied rate,                                   2.4× for SFT. The matched by-k curves, pooled
which is zero whenever any single constraint fails;                                   over all suites, are in Figure 1.
Table 50 reports each family’s satisfaction rate on
each split for the same checkpoint, and Figure 8                                      D.21       Variety and Degeneration of the
gives the same per-family view on Mixed across                                                   Matched Checkpoints
models.                                                                               In Tables 53 and 54, we repeat the within-tune
   The mixed suite includes 73 structure-family                                       statistics of Table 56 for every model of Table 2 over
items. Their satisfaction rate is 0.644 for Music-                                    all 2,180 items (src/audit_quality_main.py).
RLVR against 0.726 for SFT. On the dedicated                                          Pitch-class entropy uses the whole tune; the distinct-
structure split, the all-satisfied rate is 0.808 against                              bar and distinct pitch 4-gram ratios use the first eight
0.600; equal prompt weighting gives 0.637 against                                     bars, so tunes of different lengths are compared on
Table 42: Exact two-sided McNemar tests for the matched Direct MusicRLVR checkpoint against each control; discordant counts
are successes by only one checkpoint, and Holm correction is applied over the eight suites within each comparison.

                       Comparison         Split       Only Direct         Only control        Exact p    Holm p
                       Binary reward      Mixed                    19              16         0.7359      1.0000
                                          Single                    5               0         0.0625      0.3125
                                          Seen                     25              11         0.0288      0.1729
                                          Unseen                   21              15         0.4050      1.0000
                                          High-k                   32              15         0.0186      0.1304
                                          Structure                 7               0         0.0156      0.1250
                                          Dense                    78              58         0.1029      0.4117
                                          Edge                     42              37         0.6530      1.0000
                       SFT init.          Mixed                   90               21      < 10−4        < 10−4
                                          Single                  22                1      < 10−4        < 10−4
                                          Seen                    65               19      < 10−4        < 10−4
                                          Unseen                  36               23      0.1175        0.2350
                                          High-k                  58               22      < 10−4        0.0002
                                          Structure               71                1      < 10−4        < 10−4
                                          Dense                   90               92      0.9409        0.9409
                                          Edge                   122               34      < 10−4        < 10−4

Table 43: Matched study: the 58 unsatisfied Mixed items of the Direct MusicRLVR checkpoint. “Missed” counts items
requesting a family whose verifier fails; “sole miss” restricts to the 48 items that miss exactly one family. rhythm is omitted,
with no miss among the items requesting it.

                          Family         Requested        Missed                   Sole miss
                          final              95            11                             7
                          structure          73            22                            18
                          key                80            11                             9
                          length             65            14                            10
                          leap               89             7                             4
                          meter              81             3                             0
                          range              80             2                             0
                          Items by number of families missed: 1: 48, 2: 8, 3: 2; parse-gate failures: 0.

Table 44: Diagnostic reference results (SFT-initialised route): all-satisfied rates above, parse-gate pass rates below. A different
RL checkpoint from the matched comparison of Table 2. Colours rank rows within this table; missing entries were not evaluated.
                                                           Six original splits                                            Later splits
Model                       Mixed        Single        Seen          Unseen        High-k           Structure           Dense       Edge
Zero-shot
Qwen3-4B                    0.160         0.225       0.100             0.040       0.037               0.100           0.008      0.010
Qwen3-8B                    0.123         0.210       0.115             0.050       0.006               0.000           0.020      0.032
Qwen3-32B                   0.363         0.535       0.250             0.190       0.094               0.267           0.074      0.112
Llama-3.1-70B               0.380         0.695       0.300             0.195       0.056               0.167           0.040      0.058
MiniMax-M3                  0.367         0.580       0.315             0.190       0.100               0.008           0.088      0.160
ChatMusician-7B             0.160         0.290       0.130             0.090       0.006               0.000           0.020      0.046
Trained (4B)
SFT (4B)                    0.477         0.745       0.415             0.440       0.231               0.600           0.290      0.076
MusicRLVR (diag.)           0.663         0.835       0.635             0.595       0.356               0.808           0.370      0.162

Parse-gate pass rate (six original splits)
Model                          Mixed              Single                Seen         Unseen                 High-k              Structure
Qwen3-4B                        0.513             0.450             0.510                0.545                  0.362            0.925
Qwen3-8B                        0.367             0.465             0.345                0.305                  0.219            0.158
Qwen3-32B                       0.973             1.000             0.960                0.945                  0.938            0.983
Llama-3.1-70B                   0.970             1.000             0.980                0.980                  0.944            1.000
MiniMax-M3                      0.577             0.670             0.565                0.465                  0.531            0.083
ChatMusician-7B                 0.693             0.800             0.680                0.670                  0.575            0.158
SFT (4B)                        1.000             1.000             1.000                1.000                  1.000            1.000
MusicRLVR (diag.)               1.000             1.000             1.000                1.000                  1.000            1.000


equal spans. Three flags mark degenerate tunes: at                         Against its base model, Direct MusicRLVR
most three distinct pitches, every bar identical, and                   raises pitch-class entropy from 2.06 to 2.15, low-
more than half of consecutive notes repeating the                       ers the share of tunes with at most three pitches
previous pitch.                                                         from 28.9% to 22.9% and of tunes dominated by
                                   Qwen3-4B      0.24         0.22     0.01         0.38       0.37         0.42       0.39          0.04

                               Qwen3-32B         0.84         0.18     0.09         0.70       0.96         0.69       0.69          0.20

                                Llama-70B        0.81         0.42     0.14         0.71       0.87         0.60       0.81          0.10

                              MiniMax-M3         0.57         0.30     0.28         0.61       0.58         0.38       0.56          0.04

                                        SFT      0.62         0.63     0.97         0.88       0.42         0.73       0.76          0.73

                              MusicRLVR          0.85         0.93     1.00         0.97       0.61         0.75       0.85          0.64


                                                ke
                                                  y          ter      len        ge            al        thm
                                                                                                                        p          uc
                                                                                                                                      t
                                                        me                    ran          fin                       lea       str
                                                                                                      rhy
Figure 8: Diagnostic study: Per-family satisfaction on the mixed suite; MusicRLVR cells use the fixed checkpoint (Table 49);
structure stays red for every untrained model.

Table 45: Reward-design ablations (diagnostic study): one                           Table 48: Diagnostic study: Reward mixing weight, one
300-step run per RL row from the same SFT checkpoint. Rows                          training run per setting, scored by the binary criterion of
give the credit for the form constraint and the share of training                   Equation 1. Repetition and contrast count the structure-split
problems containing it (symmetric credit: Appendix E.2).                            items passing all required-equal and all required-distinct unit-
Colours as in Table 2; the shaded row is the default reward.                        pair checks, respectively; ⋆ marks the default.
Form credit           Mixed Single Seen Unseen High-k Struct.                              λ           Mixed          Structure             Repetition      Contrast
SFT, no GRPO          0.477   0.745   0.415    0.440     0.231       0.600                 0.5          0.633              0.425             120/120        55/120
Binary, 21%           0.610   0.810   0.630    0.635     0.350       0.250
                                                                                           0.7⋆         0.663              0.808             119/120        104/120
Binary, 33%           0.653   0.810   0.610    0.610     0.331       0.525
Graded, 33%           0.663   0.835   0.635    0.595     0.356       0.808                 1.0          0.570              0.325             119/120        45/120
Symmetric, 33%        0.590   0.745   0.590    0.630     0.388       0.200
                                                                                    Table 49: Diagnostic study: Per-family satisfaction on Mixed:
Table 46: Diagnostic study: success counts and all-satisfied                        the fraction of items requesting a family whose verifier passes.
rates for the SFT-initialised reference checkpoint on the six                       ∆ is the fixed-checkpoint rate minus the SFT rate.
original suites, matching Table 44.
                                                                                       Family                  Base           SFT           MusicRLVR            ∆
              Split           SFT init. count         Rate                             key            0.237 0.625          0.850        +0.225
                                                                                       meter          0.222 0.630          0.926        +0.296
              Mixed                199/300            0.663                            length         0.015 0.969          1.000        +0.031
              Single               167/200            0.835                            range          0.375 0.875          0.975        +0.100
              Seen                 127/200            0.635                            final          0.368 0.421          0.611        +0.189
              Unseen               119/200            0.595                            rhythm         0.416 0.727          0.753        +0.026
              High-k                57/160            0.356                            leap           0.393 0.764          0.854        +0.090
              Structure             97/120            0.808                            structure 0.041 0.726               0.644         -0.082
                                                                                    Table 50: Diagnostic study: per-family satisfaction rate for
Table 47: Diagnostic study: All-satisfied rate on the mixed and                     MusicRLVR across the splits. Each cell is the fraction of
structure suites for each hyper-parameter setting, one training                     problems mentioning that family whose own verifier passes
run each. ⋆ marks the SFT-initialised reference configuration.                      at the fixed checkpoint (other constraints may fail); families
                                                                                    mentioned by fewer than five problems in a split are marked
    Hyper-parameter           Value           Mixed      Structure                  “–”.
    Learning rate             5×10−7          0.567           0.808                   Family                Single          Seen          Unseen   High-k     Structure
                              1×10−6⋆         0.663           0.808
                                                                                      final                 0.783          0.636          0.407    0.635          –
                              2×10−6          0.710           0.542                   key                   0.862          0.887          0.565    0.671        0.643
                              5×10−6          0.837           0.833                   leap                  0.292          0.935          0.985    0.872        1.000
                                                                                      length                1.000          1.000          1.000    1.000          –
    KL coefficient β          0               0.607           0.750                   meter                 0.812          0.903          0.897    0.890        1.000
                              0.01            0.660           0.567                   range                 1.000          0.982          0.955    0.980        1.000
                              0.04⋆           0.663           0.808                   rhythm                0.833          0.790          0.843    0.655        0.692
                              0.1             0.600           0.458                   structure             1.000          0.510          0.667    0.554        0.867
    Group size G              4               0.540           0.533
                              8⋆              0.663           0.808
                              16              0.577           0.475


repeated notes from 8.5% to 1.2%. Table 54 keeps
only the 332 items without a form constraint, which
requests repetition by design, on which both models
render at least eight bars. The same pattern holds
there: entropy 2.02 to 2.17 and repeated-note tunes
12.3% to 2.1%.
Table 51: All-satisfied rate by number of constraints k over                   Table 57: Diagnostic study: full-score duplication for the first
all eight suites (2,180 items), the values plotted in Figure 1.                eligible occurrence of each of 220 distinct prompts in that
Each slice pools the suites containing that k; the trained rows                common set, identified by parsed event signatures and ignoring
are the matched runs of Table 2.                                               metadata, which measures duplication across prompts.
Model                     k = 1 k = 2 k = 3 k = 4 k=1/k=4                       Model                    Unique full scores   Most frequent score
Items                      354   614   512   700                                SFT                          167/220                7/220
Qwen3-4B                  0.243    0.068    0.018    0.016       15.5×          MusicRLVR (diagnostic)       182/220                5/220
Qwen3-32B                 0.559    0.225    0.098    0.083        6.8×
Llama-3.1-70B             0.630    0.212    0.090    0.044       14.2×
MiniMax-M3                0.486    0.267    0.137    0.089        5.5×            On the full completions, MusicRLVR raises
SFT                       0.723    0.349    0.178    0.277        2.6×
Direct GRPO (R = A)       0.977    0.661    0.357    0.361        2.7×         distinct-bar fraction from 0.276 to 0.313 while
MusicRLVR (SFT init.)     0.757    0.430    0.283    0.353        2.1×         mean length falls 39.2 → 28.7 bars. Under the
MusicRLVR (Direct)        0.992    0.673    0.406    0.419        2.4×
                                                                               length control of Table 55 the distinct-bar com-
                                                                               parison is 0.417 → 0.426 on matched eight-bar
D.22      Length-Controlled Output Statistics                                  prefixes. The matched checkpoints of Table 2 are
                                                                               analysed in Appendix D.21.
Table 55: Diagnostic output analysis. (a) Surface statistics
(first 8 bars, 297 matched items). (b) Best-of-N (T =1.0,
n=8, binary).                                                                  D.23     Output Length Statistics
                                  (a)                                          In Table 58, we report the average number of bars
Model                  Notes      PC ent.      Dist. bars        Dist. 4-gr.   and notes per parsed completion on the mixed suite,
SFT                    42.7        1.930         0.417             0.419       supplementing the quality metrics in Table 56.
MusicRLVR (diag.)      40.5        1.826         0.426             0.403
                                                                               The supervised model over-generates (39.2 bars
                                  (b)
                                                                               against 19.9 for the corpus), and the reinforcement
Suite      Model                   p@1       p@2         p@4          p@8
                                                                               stage pulls this back to 28.7 bars, consistent with
Mixed      SFT                    0.415      0.584       0.728       0.827
           MusicRLVR (diag.)      0.676      0.817       0.900       0.950
                                                                               a reward that favours concision without an uncon-
Struct.    SFT                    0.692      0.861       0.938       0.967
                                                                               ditional length term, since a longer tune has more
           MusicRLVR (diag.)      0.844      0.953       0.978       0.983     places to violate a constraint. The three larger zero-
                                                                               shot models sit near the corpus length (17.9–21.2
In Table 55, we compare the first eight parsed                                 bars; the 4B base averages 29.3), and MiniMax-M3
bars of a common item set of the diagnostic study,                             parses on only 173 of 300 problems.
because the full-tune ratios of Table 56 have length-
dependent denominators. In this section, we give                               D.24     Zero-Variance Groups During Training
the uncontrolled statistics those ratios come from,                            In this section, we track groups without a re-
and the cross-prompt duplication counts of Table 57.                           ward gradient during training. Equation 4 im-
Both read historical-gate outputs, but they measure                            plies that a group whose G rollouts all receive the
different things: the first are within-tune proxies,                           same reward contributes no reward gradient. The
the second counts how often two different prompts                              trainer logs the fraction of such groups per step
produce the same score.                                                        (frac_reward_zero_std); Table 59 summarises
                                                                               it for the two reward variants of the main ablation.
Table 56: Diagnostic study: distributional statistics of the
single-run mixed-suite completions and 299 corpus tunes.                           The two diagnostic rows differ in both the reward
No constraint names entropy or either distinctness measure;                    and the share of structure prompts; the matched
bar count is constrained on the 138/300 items requesting                       runs below change the reward alone.
length or structure. Mean length differs between rows, so
distinctness denominators are unmatched; Table 55 controls                         The matched runs measure the same quantity on
for that.                                                                      two arms that differ only in λ, holding the prompt
   Model                Bars PC ent. Dist. bars Dist. 4-gr.                    mix fixed. Averaged over the first 50 updates, binary
   Corpus               19.9      2.63       0.758           0.676             reward leaves 0.550 of groups with zero reward
   Base                 29.3      2.06       0.366           0.391             variance against 0.307 for the graded reward; over
   SFT                  39.2      2.00       0.276           0.294
   RL, binary credit    32.2      1.85       0.284           0.289             the last 50 the two reach 0.823 and 0.823, once most
   MusicRLVR            28.7      1.89       0.313           0.292             groups succeed outright, and over all 300 updates
                                                                               they average 0.717 and 0.660 (Figure 4(b)). The
                                                                               SFT-initialised arm runs lower throughout (0.120,
                                                                               0.343, 0.245), so the fraction is compared between
                                                                               arms that share an initialisation.
Table 52: Diagnostic study: all-satisfied rate on the mixed suite by number of constraints k. The last column is the k=1 rate over
the k=4 rate; a dagger marks curves not monotone in k (the k=3 and k=4 cells hold only 60 and 40 items, so one item moves
them by 0.017 and 0.025).

                                             Model                               k=1             k=2     k=3       k=4      k=1/k=4
                                             MusicRLVR (diag.)                   0.850           0.640   0.517     0.475      1.8×
                                             SFT (4B)                            0.720           0.430   0.267     0.300      2.4×†
                                             Qwen3-32B                           0.650           0.300   0.133     0.150      4.3×†
                                             Llama-3.1-70B                       0.720           0.340   0.100     0.050      14.4×
                                             MiniMax-M3                          0.560           0.360   0.267     0.050      11.2×
                                             Qwen3-4B                            0.340           0.110   0.033     0.025      13.6×
                                             Qwen3-8B                            0.240           0.120   0.017     0.000        –

Table 53: Variety and degeneration over all 2,180 items (n:                                          D.26     Additional Diagnostics
completions that music21 parses into at least four notes,
a looser test than the validation gate), with the IrishMAN                                           In Figure 10, we show two further per-item diagnos-
reference sample of Table 56. Distinctness uses the first eight
bars.
                                                                                                     tics: which families fail together, and when each
Source                           n PC ent. Dist. bars Dist. 4-gr. ≤3 pitches Same bars Rep. notes
                                                                                                     item is first solved during training.
IrishMAN corpus                 299   2.63     0.828    0.769       0.0%       0.0%       0.7%
Qwen3-4B                       1053   2.06     0.449    0.503      28.9%       5.4%       8.5%
Qwen3-8B                        891   1.97     0.457    0.393      24.2%      18.0%      40.6%       E      Error and Structure Analysis
Qwen3-32B                      2076   2.64     0.775    0.752       0.8%       0.1%       5.0%
Llama-3.1-70B                  2093   2.42     0.610    0.607       3.0%       0.2%       1.1%
MiniMax-M3
ChatMusician-7B
                               2143
                               1710
                                      2.29
                                      1.83
                                               0.725
                                               0.599
                                                        0.794
                                                        0.551
                                                                    9.2%
                                                                   31.2%
                                                                               4.4%
                                                                              12.1%
                                                                                         12.7%
                                                                                         32.8%
                                                                                                     In this section, we analyse which constraints bind
SFT                            2180   1.87     0.389    0.390      23.0%       7.7%      32.0%
RFT                            2172   2.07     0.472    0.521      31.7%       6.6%      11.2%       on each split and how form credit behaves across
Direct GRPO (R = A)            2180   2.14     0.389    0.444      22.9%       7.8%      1.4%
MusicRLVR (SFT init.)
MusicRLVR (Direct)
                               2180
                               2178
                                      1.62
                                      2.15
                                               0.359
                                               0.381
                                                        0.342
                                                        0.434
                                                                   35.1%
                                                                   22.9%
                                                                              11.4%
                                                                               6.5%
                                                                                         40.7%
                                                                                          1.2%
                                                                                                     reward variants and form types.
MusicRLVR (Direct, Qwen3-8B)   2180   2.02     0.508    0.494      28.1%       7.0%      52.0%

                                                                                                     E.1     Which Constraint Binds, by Split
Table 54: The same statistics on the 332 items without a form
constraint that both Qwen3-4B and Direct MusicRLVR render                                            In Figure 11, we give the outcome composition of
to at least eight bars; every model is scored on those items.                                        each split, and in Table 60, we add the most frequent
Model                           n PC ent. Dist. bars Dist. 4-gr. ≤3 pitches Same bars Rep. notes
                                                                                                     failing families, using the diagnostic reference eval-
Qwen3-4B                       332    2.02    0.530     0.562     30.1%       4.2%       12.3%
SFT
Direct GRPO (R = A)
                               332
                               332
                                      1.82
                                      2.10
                                              0.372
                                              0.406
                                                        0.366
                                                        0.430
                                                                  24.4%
                                                                  31.6%
                                                                              9.3%
                                                                              16.9%
                                                                                         30.1%
                                                                                         0.6%
                                                                                                     uation. Figure 12 breaks the same evaluation down
MusicRLVR (Direct)             332    2.17    0.410     0.442     25.0%       7.5%       2.1%
MusicRLVR (Direct, Qwen3-8B)   332    2.23    0.627     0.634     16.3%       3.9%       61.1%       by requested form and by how many models solve
Llama-3.1-70B                  322    2.40    0.665     0.631      4.7%       0.3%        2.2%
                                                                                                     each item.
Table 58: Diagnostic study: Output length in the single-run                                          Most unsatisfied items miss one family. The frac-
mixed-suite diagnostic (n = 300 problems). Only comple-                                              tion missing multiple families is 0.040 on Seen and
tions that pass the historical parse gate are included, so the
parsed count differs by model; the IrishMAN reference (299                                           0.105 on Unseen, rising to 0.206 on High-k. The
tunes, 19.9 bars) is in Table 56.                                                                    most frequent failing family is final on Unseen
 Source                                      Parsed n      Mean bars           Mean notes            and High-k. structure is among the three most
 Qwen3-4B (zero-shot)                          154              29.3                78.4             frequent failures on Seen and Unseen; leap appears
 Qwen3-32B (zero-shot)                         292              18.4                58.1
 Llama-3.1-70B (zero-shot)                     291              21.2                66.1
                                                                                                     among the top three only on Single.
 MiniMax-M3 (zero-shot)                        173              17.9                37.0
 SFT                                           300              39.2               167.5             E.2     Structure Reward Variants
 MusicRLVR                                     300              28.7               130.3
                                                                                                     In Table 61, we compare the fixed default checkpoint
D.25         Additional Training Curves                                                              with the equal-weight control and the symmetric-
                                                                                                     credit study. The default and equal-weight rows
In Figure 9, we give the trainer-log quantities be-                                                  each use one run; symmetric credit reports the mean
hind the diagnostics of Figure 7; the numbers                                                        and sample SD of its two runs. The default form
behind it are as follows. Final KL to the refer-                                                     term weights repetition 0.7 and contrast 0.3; the
ence falls 0.047 → 0.024 → 0.010 as β rises                                                          following controls examine that choice.
0.01 → 0.04 → 0.1 (the β = 0 run logs no KL
term), and yet the observed mixed rates lie in the                                                   Symmetric form credit.            The contrast counter-
narrow range 0.600–0.663 (Table 47): the KL term                                                     part of Equation 3 is
therefore tracks β as designed, while Mixed com-
                                                                                                                             M
pliance is flat across the range. Along learning rate,                                                              1      X X
                                                                                                           d¯ =
                                                                                                                                                
                                                                                                                               I ua [m] ̸= ub [m] ,
final KL 0.006, 0.024, 0.049, 0.157 and mean group                                                                |D|M
                                                                                                                         (a,b)∈D m=1
reward 0.713, 0.832, 0.893, 0.936 over 5×10−7 to
5×10−6 run in the same order as the mixed suite.
Table 59: Diagnostic study: Fraction of GRPO groups with zero reward variance (duplicate step records from restarts removed),
averaged over the first and last quarter of training and over all 300 steps, with the mean within-group reward standard deviation
alongside.

                                                                                                         Zero-variance groups                                                             Reward std
                      Run                                                                          first 25%                                    last 25%              all           first 25%         last 25%
                      Binary form credit, original form share (21%)                                    0.116                                      0.307          0.221                  0.301          0.214
                      Graded form credit, 33% form share (final)                                       0.133                                      0.322          0.254                  0.296          0.210

                                                                                   binary form credit                                          graded (final)
                           (a) Mean group reward                                        (b) Within-group reward std                                                                       (c) Gradient norm
                                                                                                                                                                              2.0
     reward




                0.8                                                               0.3




                                                                                                                                                                   norm
                                                                       std
                                                                                  0.2                                                                                         1.5
                0.6
                                                                                  0.1
                      0               100     200         300                            0         100                         200                     300                          0           100      200       300
                             (d) Learning rate                                               (e) KL coefficient β                                                                          (f) Group size G
  mean reward




                                                                    mean reward




                                                                                                                                                                mean reward
            0.75                                                              0.75                                                                                        0.75
            0.50           5e-7        1e-6   2e-6    5e-6                    0.50             0        0.01                          0.04            0.1                 0.50                           4     8   16

                      0               100     200         300                            0         100                         200                     300                          0           100      200       300
                                      GRPO step                                                    GRPO step                                                                                    GRPO step
Figure 9: Diagnostic study: trainer-log quantities behind Figure 7. (a–c) Mean group reward, within-group reward SD and
gradient norm, binary form credit against the final graded run. (d–f) Mean group reward for every hyper-parameter setting of
Figure 7(b) on one shared scale; the thick blue curve is the default run (lr = 1e−6, β = 0.04, G = 8). Curves are smoothed
over 9 steps; each axis spans the 2nd–98th percentile of its raw trace, so a few steps clip.

                                  (a) Co-failure matrix                                                                                                               (b) Learning timeline
                                                                                                                                               1.0
        key           12                             1          2                       1
                                                                                                   35                                                                                           80.0% 80.7% 81.0%
                                                                                                               Fraction of items ever solved




  meter                           6                  2                                                                                                                              77.0%
                                                                                                                                               0.8
                                                                                                   30                                                              68.7%
          len
                                                                                                   25                                                 57.0%
                                                                                                                                               0.6
  range                                       2
                                                                                                   20
    final              1          2                  37         1            4          2
                                                                                                   15                                          0.4
rhythm                 2                             1       19                         1          10

      leap                                           4                     13                      5                                           0.2
                                                                                                                                                                                                         MusicRLVR
  struct               1                             2          1                       26         0                                                                                                     SFT baseline
                                                                                                                                               0.0
                                                                                                                                                                        100                      200               300
                 y




                                             e
                           er

                                             n



                                      rh l
                                           hm

                                                                ap

                                                                                   t
                                            a




                                                                                  uc




                                                                                                                                                                                    GRPO step
                                         ng
                ke



                                  le


                                        fin
                       et




                                                             le
                                                                         str
                                        yt
                                        ra
                      m




                           MusicRLVR failures (n=300)
Figure 10: Diagnostic study: per-item diagnostics on the mixed suite (n = 300). (a) Co-failure matrix of MusicRLVR: diagonal
entries are per-family failure counts, off-diagonal entries co-failures, which are rare: key shares at most two with any family. (b)
CDF of the step at which each item is first solved: 57% by step 50, 81% at least once by step 300.

and the symmetric term is                                                                                 the all-identical fraction is 0.762 ± 0.018. The
                                                                                                         control jointly changes the weights, the contrast
         1,
                          vstructure = 1,                                                                factor and the credit for all-identical outputs. Un-
  sym
 s    = 0,                 u1 = u2 = u3 = u4 ,                                                            der the default term, an all-identical output earns
                        ¯ else.                                                                           sstructure = 0.7 but has A = 0, because it fails
         
           0.5 ē + 0.5 d,
         
                                                                                                          contrast. Appendix D.18 separately varies the outer
The outer reward mixture is unchanged. Across                                                             mixing weight.
two runs, contrast satisfaction is 0.233 ± 0.024 and
                                   all satisfied      miss 1      miss ≥ 2            parse fail
            Single                                                                                                                                        0.835
      Seen combo                                                                                                           0.635
    Unseen combo                                                                                                   0.595
           High-k                                                             0.356
        Structure                                                                                                                                     0.808
           Mixed                                                                                                               0.663

                           0.00                                 0.25                                     0.50                                     0.75                                 1.00
                                                                                                   fraction of items
 Figure 11: Diagnostic study: What an unsatisfied item is missing. Outcome composition for the fixed checkpoint; printed
 all-satisfied rates match Table 44. Parse failures are zero on all six original splits.

                                  (a) Structure split, by form                                                                            (b) Item difficulty
                                             SFT        MusicRLVR                                                                                                 all items
all-satisfied rate




                                                                                                             75                         70                        solved by MusicRLVR
                     1.0           0.86
                            0.74                   0.77 0.77                  0.79
                                                                                                                              48                 48




                                                                                                     items
                                                                                                             50    46
                                                                                                                                                         33         35
                     0.5
                                                                       0.33                                                                                               19
                                                                                                             25
                                                                                                                                                                                   1
                     0.0                                                                                      0
                             AABA                   AABB                ABAB                                       0          1           2       3       4         5      6       7
                                                                                                                                       models solving it (of 7)
 Figure 12: Diagnostic study: Structure and item-level diagnostics. (a) Satisfaction by requested form for the fixed checkpoint.
 (b) Item counts by the number of seven evaluated models solving them under the historical A.

 Table 60: Diagnostic study: which constraints fail, by split. “Not all satisfied” is one minus the all-satisfied rate; the next column
 counts items failing two or more families at once; the last lists the three most frequent failing families as fractions of the split’s
 items (an item failing two is counted under both). No completion fails the parse gate on any split.

             Split                Not all satisfied            Failing ≥ 2 families                                     Most frequent failing families
             Single                       0.165                          0.000                             leap (0.085), final (0.025), key (0.020)
             Seen                         0.365                          0.040                        structure (0.125), final (0.120), rhythm (0.065)
             Unseen                       0.405                          0.105                          final (0.160), key (0.150), structure (0.090)
             High-k                       0.644                          0.206                           final (0.237), rhythm (0.181), key (0.156)
             Structure                    0.192                          0.017                         structure (0.133), key (0.042), rhythm (0.033)

 Reweighting repetition and contrast. The                                                              the highest rate over all items, 0.580 against 0.515
 single-variable version moves only the weights,                                                       (symmetric) and 0.544 (equal weights).
 to 0.5/0.5: an all-identical output still banks the
 repetition half, the binary contrast factor is kept,                                                  E.3        Structure Results by Form Type
 and the rest of the reward and the training setup are                                                 In Table 62, we decompose performance on the
 unchanged. Two things follow.                                                                         three form types of the structure split, which come
  (1) In the single-run diagnostic comparison, the                                                     in unequal numbers: AABA (n = 42), AABB
      structure split moves 0.808 → 0.675 and all-                                                     (n = 35) and ABAB (n = 43).
      identical outputs 15 → 32 of 120, the same                                                       Table 62: Diagnostic study: Structure results by form for
      direction as the joint control (Table 61).                                                       the fixed MusicRLVR and SFT checkpoints. Contrast and
                                                                                                       all-identical are fractions of items of that form.
  (2) The equal-weight control scores 0.637 on
      Mixed, compared with 0.663 for the default.                                                        Model                     Form       All-sat.    Contrast       All-identical
 Appendix D.18 extends this comparison to the outer                                                      SFT                       aaba       0.738           0.810            0.190
                                                                                                         SFT                       aabb       0.771           0.857            0.143
 reward mixture. In the single-run diagnostic study,                                                     SFT                       abab       0.326           0.395            0.605
 the two tested λ endpoints yield larger increases                                                       MusicRLVR                 aaba       0.857           0.905            0.071
 in all-identical outputs than the equal-weight form                                                     MusicRLVR                 aabb       0.771           0.829            0.171
                                                                                                         MusicRLVR                 abab       0.791           0.860            0.140
 control. The default achieves the highest Structure
 score and fewest all-identical outputs among these
                                                                                                       ABAB is the form supervision handles worst, and
 tested weight settings. In the Direct configuration
                                                                                                       by a wide margin: SFT reaches 0.771 on AABB
 (Table 6), the default again gives the highest Struc-
                                                                                                       but 0.326 on ABAB, with 26/43 of its ABAB
 ture, 0.967 against 0.942 for both variants, and
                                                                                                       outputs written as four identical units. All three
Table 61: Diagnostic study: structure decomposition. “Runs” is the number of training runs: default and equal-weight use one
each, symmetric credit reports mean ± sample SD over two. All-identical is a fraction; “all requested” additionally requires the
companion constraint, present in 66 of 120 items.

                   Reward                  Runs         Repetition       Contrast      All requested   All-identical
                   MusicRLVR                  1          0.992             0.867           0.808           0.125
                   Equal weights              1          1.000             0.733           0.675           0.267
                   Symmetric credit           2      0.996 ± 0.006     0.233 ± 0.024   0.208 ± 0.012   0.762 ± 0.018

      Prompt: 3/4 | 8 bars | last note E | eighths and quarters only      items are common. Over the 2,180 benchmark
    SFT: one two-bar cell repeated
                                                                          items, Direct MusicRLVR satisfies 609 that all
G
    ✓ 3/4             ✓ 8 bars         ✓ ends on E      ✓ 8th + qtr
                                                                          three of these models fail, whereas all three satisfy
    MusicRLVR: a three-bar cycle
                                                                          only 5 items that Direct MusicRLVR fails. The
G                    ♯ ♯                       ♯ ♯
                                                                          six examples cover four constraints on Mixed, two
    ✓ 3/4             ✓ 8 bars         ✓ ends on E      ✓ 8th + qtr       held-out pairs on Dense (with the Qwen3-8B policy
Figure 13: One High-k item, diagnostic study (Ap-                         alongside), a held-out pair with a form on Unseen,
pendix D.14): both outputs satisfy all four constraints.                  the interleaved abab form, and two Edge items: one
                                                                          with out-of-range meter (5/4), and one combining
forms require distinct A and B units, so the gap                          a rhythm restriction with abab structure.
tracks the arrangement rather than the distinctness
requirement: ABAB is the only one that interleaves
the two units instead of repeating each in place.
   At the fixed checkpoint, ABAB has the largest
improvement over SFT among the three forms: its
all-satisfied rate rises from 0.326 to 0.791, while
the all-identical fraction changes from 0.605 to
0.140. Table 62 reports the rate for every form.

F      Qualitative Examples
In this section, we present qualitative examples.
Figure 13 shows two outputs that satisfy the same
four constraints with different repeating patterns.
Every example below is a benchmark item chosen
by a fixed rule (the first item in file order with
the stated constraint families and pass/fail pattern),
its completions are read verbatim from the frozen
evaluation files, and the notation is drawn from
music21’s parse of the output: pitch, duration and
bar lines. The key and meter checks additionally
read the header-derived objects, and the key check
analyses the whole score. Marks under each staff
are the verifiers’ decisions on that output. Outputs
rejected at the gate are shown as a short excerpt
together with the gate’s reason. Examples 1–6
compare the zero-shot base model with Music-
RLVR (diagnostic run), and Example 2 shows SFT
as well; Examples 7–8 compare MusicRLVR with
the larger zero-shot models on the same items.
   Examples 9–14 use the matched Direct Music-
RLVR of Table 2 and one rule: the first item in file
order, among those with the stated families, that
Direct MusicRLVR satisfies while Qwen3-32B,
Llama-3.1-70B and MiniMax-M3 all fail. Such
Example 1: unseen-combination split (k = 2, held-out pair key–rhythm).
Item uc-0022. Constraints: (1) the tune must be in G major; (2) use only sixteenth, eighth, and quarter notes (no dotted notes,
no other durations, no rests)
                 Qwen3-4B (zero-shot) (8 bars)




             G
                  ✗ key G major             ✓ rhythm set


                 MusicRLVR (18 bars; first 16 shown)

             G



             G
                  ✓ key G major             ✓ rhythm set

Qwen3-4B (zero-shot) fails key; MusicRLVR satisfies every constraint.



Example 2: high-k split (k = 4).
Item hk-0004. Constraints: (1) the meter must be 3/4, and every bar must contain exactly the right total duration; (2) the tune
must be exactly 8 bars long (no pickup bar); (3) the last note of the tune must be E (any octave); (4) use only eighth and quarter
notes (no dotted notes, no other durations, no rests)
                 Qwen3-4B (zero-shot)
                 not rendered: parse-error: ABCTokenException
                 X:1 ⏎ T:Monophonic Tune ⏎ M:3/4 ⏎ L:8 ⏎ K:C ⏎ C D E | C D E | E D C | E D C | ⏎ E D C | E D C | C D E | E D E …


                  ✗ meter 3/4              ✗ 8 bars                 ✗ final E       ✗ rhythm set


                 SFT (8 bars)

             G
                  ✓ meter 3/4              ✓ 8 bars                 ✓ final E       ✓ rhythm set


                 MusicRLVR (8 bars)

             G
                                  #         #              #    #          #    #     #            #       #   #

                  ✓ meter 3/4              ✓ 8 bars                 ✓ final E       ✓ rhythm set

Qwen3-4B (zero-shot) fails at the parse gate (parse-error: ABCTokenException); SFT satisfies every constraint; MusicRLVR
satisfies every constraint.



Example 3: single-constraint split (k = 1).
Item sg-0000. Constraints: (1) melodic motion must be smooth: no melodic leap larger than an octave
                 Qwen3-4B (zero-shot)
                 not rendered: degenerate-or-polyphonic
                 X:1 ⏎ T:Simple Melody ⏎ M:4/4 ⏎ L:1/4 ⏎ K:C


                  ✗ leap ≤ 12


                 MusicRLVR (16 bars)

             G
                                            #                              #                       #                    #




                                                #                   #      #                           #           #    #

             G
                  ✓ leap ≤ 12

Qwen3-4B (zero-shot) fails at the parse gate (degenerate-or-polyphonic); MusicRLVR satisfies every constraint.
Example 4: seen-combination split (k = 3).
Item sc-0005. Constraints: (1) the last note of the tune must be D (any octave); (2) use only sixteenth, eighth, and quarter notes
(no dotted notes, no other durations, no rests); (3) melodic motion must be smooth: no melodic leap larger than a perfect fifth
                 Qwen3-4B (zero-shot)
                 not rendered: degenerate-or-polyphonic
                 X:1 ⏎ T:Simple Tune ⏎ M:4/4 ⏎ L:1/16 ⏎ K:C


                  ✗ final D                 ✗ rhythm set      ✗ leap ≤ 7


                 MusicRLVR (23 bars; first 16 shown)
                                                                               #       # #       #   #       # #   #

             G




             G
                  ✓ final D                 ✓ rhythm set      ✓ leap ≤ 7

Qwen3-4B (zero-shot) fails at the parse gate (degenerate-or-polyphonic); MusicRLVR satisfies every constraint.




Example 5: seen-combination split (k = 2).
Item sc-0001. Constraints: (1) use only sixteenth, eighth, and quarter notes (no dotted notes, no other durations, no rests); (2)
the tune must be exactly 16 bars with an AABB form in 4-bar units: labeled units with the same letter must be note-for-note
identical, and units with different letters must differ
                 Qwen3-4B (zero-shot) (8 bars)

             G
                  ✓ rhythm set              ✗ form AABB


                 MusicRLVR (16 bars)

             G



             G
                  ✓ rhythm set              ✓ form AABB

Qwen3-4B (zero-shot) fails structure; MusicRLVR satisfies every constraint.




Example 6: unseen-combination split (k = 2, held-out pair length–range).
Item uc-0001. Constraints: (1) the tune must be exactly 16 bars long (no pickup bar); (2) every note must lie between G3 and
A5 inclusive
                 Qwen3-4B (zero-shot)
                 not rendered: degenerate-or-polyphonic
                 X:1 ⏎ T:Monophonic Tune ⏎ M:4/4 ⏎ L:1/4 ⏎ K:C


                  ✗ 16 bars                 ✗ range G3–A5


                 MusicRLVR (16 bars)

             G
                                            #                 #                              #                         #



                     #               #               #                     #       #                     #

             G
                                                              #                                                        #

                  ✓ 16 bars                 ✓ range G3–A5

Qwen3-4B (zero-shot) fails at the parse gate (degenerate-or-polyphonic); MusicRLVR satisfies every constraint.
Example 7: structure split (k = 1, zero-shot models against MusicRLVR).
Item st-0023. Constraints: (1) the tune must be exactly 16 bars with an AABA form in 4-bar units: labeled units with the
same letter must be note-for-note identical, and units with different letters must differ
                                Qwen3-32B (zero-shot) (15 bars)

                            G



                            G
                                 ✗ form AABA

                                Llama-3.1-70B (zero-shot) (32 bars; first 16 shown)

                            G



                            G
                                 ✗ form AABA

                                MiniMax-M3 (zero-shot)
                                not rendered: repeat-signs-forbidden
                                X: 1 ⏎ T: AABA Tune ⏎ M: 4/4 ⏎ L: 1/4 ⏎ K: G ⏎ |: G2 B2 | d4 B2 A2 | G4 D2 | E4 G2 A2 | ⏎ B2 d2 | g4 d2 B2 | A…

                                 ✗ form AABA

                                MusicRLVR (16 bars)

                            G
                                                            #               #          #                       #             #         #




                            G
                                                            #               #          #                       #             #         #

                                 ✓ form AABA


Qwen3-32B (zero-shot) fails structure; Llama-3.1-70B (zero-shot) fails structure; MiniMax-M3 (zero-shot) fails at the
parse gate (repeat-signs-forbidden); MusicRLVR satisfies every constraint.




Example 8: high-k split (k = 4, zero-shot models against MusicRLVR).
Item hk-0278. Constraints: (1) the tune must be in C major; (2) every note must lie between D4 and D6 inclusive; (3) the last
note of the tune must be G (any octave); (4) melodic motion must be smooth: no melodic leap larger than a perfect fifth
                                Qwen3-32B (zero-shot) (235 bars; first 16 shown)

                            G



                            G
                                 ✓ key C major              ✗ range D4–D6        ✗ final G        ✓ leap ≤ 7

                                Llama-3.1-70B (zero-shot) (18 bars; first 16 shown)

                            G



                            G
                                 ✓ key C major              ✗ range D4–D6        ✓ final G        ✓ leap ≤ 7

                                MusicRLVR (169 bars; first 16 shown)

                            G


                            G
                                 ✓ key C major              ✓ range D4–D6        ✓ final G        ✓ leap ≤ 7


Qwen3-32B (zero-shot) fails range, final; Llama-3.1-70B (zero-shot) fails range; MusicRLVR satisfies every constraint.
Example 9: Mixed split (k = 4).
Item k4-0002. Constraints: (1) the tune must be in A minor; (2) the meter must be 3/4, and every bar must contain exactly the
right total duration; (3) the last note of the tune must be C (any octave); (4) melodic motion must be smooth: no melodic leap
larger than a perfect fifth
                    Qwen3-32B (zero-shot) (8 bars)

                G

                     ✓ key A minor             ✗ meter 3/4          ✓ final C        ✗ leap ≤ 7

                    Llama-3.1-70B (zero-shot) (20 bars; first 8 shown)

                G

                     ✓ key A minor             ✗ meter 3/4          ✓ final C        ✗ leap ≤ 7
                    MiniMax-M3 (zero-shot) (32 bars; ABC excerpt)
                    ABC excerpt; fails meter and leap
                    X: 1 ⏎ T: Smooth A Minor Waltz ⏎ M: 3/4 ⏎ L: 1/4 ⏎ K: Am ⏎ A2 c2 | e2 d2 | c2 A2 | B2 c2 | ⏎ d2 e2 | c2…

                     ✓ key A minor             ✗ meter 3/4          ✓ final C        ✗ leap ≤ 7


                    MusicRLVR (Direct, Qwen3-4B) (12 bars; first 8 shown)

                G
                     ✓ key A minor             ✓ meter 3/4          ✓ final C        ✓ leap ≤ 7

Qwen3-32B (zero-shot) fails meter, leap; Llama-3.1-70B (zero-shot) fails meter, leap; MiniMax-M3 (zero-shot) fails meter,
leap; MusicRLVR (Direct, 4B) satisfies every constraint.
Example 10: Dense split (k = 4, two held-out pairs, MusicRLVR on both base models).
Item dn-0003. Constraints: (1) the tune must be in D minor; (2) the tune must be exactly 16 bars long (no pickup bar); (3)
every note must lie between G3 and A5 inclusive; (4) use only eighth, quarter, and half notes (no dotted notes, no other durations,
no rests)
                    Qwen3-32B (zero-shot) (16 bars)

                G            b                                  b               b          b                     b




                G        b                b                                            b            b


                     ✗ key D minor              ✗ 16 bars       ✓ range G3–A5        ✗ rhythm set

                    Llama-3.1-70B (zero-shot) (16 bars)

                G                                           b                                           b




                G
                     ✓ key D minor              ✗ 16 bars       ✓ range G3–A5        ✓ rhythm set

                    MiniMax-M3 (zero-shot)
                    not rendered: repeat-signs-forbidden
                    X: 1 ⏎ T: Minor Tune ⏎ M: 4/4 ⏎ L: 1/8 ⏎ K: Dmin ⏎ |:d2 a2 a2 g2|f2 e2 d2 e2|f2 g2 a2 f2|e2 d2 d4:| ⏎ |:d2 f2 …

                     ✗ key D minor              ✗ 16 bars       ✗ range G3–A5        ✗ rhythm set

                    MusicRLVR (Direct, Qwen3-4B) (16 bars)

                G


                G
                     ✓ key D minor              ✓ 16 bars       ✓ range G3–A5        ✓ rhythm set

                    MusicRLVR (Direct, Qwen3-8B) (16 bars)

                G



                G
                     ✓ key D minor              ✓ 16 bars       ✓ range G3–A5        ✓ rhythm set

Qwen3-32B (zero-shot) fails key, length, rhythm; Llama-3.1-70B (zero-shot) fails length; MiniMax-M3 (zero-shot) fails at
the parse gate (repeat-signs-forbidden); MusicRLVR (Direct, 4B) satisfies every constraint; MusicRLVR (Direct, 8B) satisfies
every constraint.
Example 11: unseen-combination split (k = 3, held-out pair meter–leap plus a form).
Item uc-0006. Constraints: (1) the meter must be 6/8, and every bar must contain exactly the right total duration; (2) melodic
motion must be smooth: no melodic leap larger than an octave; (3) the tune must be exactly 16 bars with an ABAB form in 4-bar
units: labeled units with the same letter must be note-for-note identical, and units with different letters must differ
                    Qwen3-32B (zero-shot) (16 bars)

                G



                G
                     ✗ meter 6/8                ✓ leap ≤ 12         ✗ form ABAB

                    Llama-3.1-70B (zero-shot) (22 bars; first 16 shown)

                G



                G
                     ✗ meter 6/8                ✓ leap ≤ 12         ✗ form ABAB

                    MiniMax-M3 (zero-shot)
                    not rendered: repeat-signs-forbidden
                    X: 1 ⏎ T: Smooth Six-Eight ⏎ M: 6/8 ⏎ L: 1/8 ⏎ K: G ⏎ |: (no repeat signs allowed, so bars are written out exp…

                     ✗ meter 6/8                ✗ leap ≤ 12         ✗ form ABAB

                    MusicRLVR (Direct, Qwen3-4B) (16 bars)

                G



                G
                     ✓ meter 6/8                ✓ leap ≤ 12         ✓ form ABAB

Qwen3-32B (zero-shot) fails meter, structure; Llama-3.1-70B (zero-shot) fails meter, structure; MiniMax-M3
(zero-shot) fails at the parse gate (repeat-signs-forbidden); MusicRLVR (Direct, 4B) satisfies every constraint.
Example 12: structure split (k = 2, the interleaved form abab).
Item st-0033. Constraints: (1) the meter must be 6/8, and every bar must contain exactly the right total duration; (2) the tune
must be exactly 16 bars with an ABAB form in 4-bar units: labeled units with the same letter must be note-for-note identical, and
units with different letters must differ
                    Qwen3-32B (zero-shot) (32 bars; first 16 shown)

                G



                G
                     ✗ meter 6/8                ✗ form ABAB

                    Llama-3.1-70B (zero-shot) (20 bars; first 16 shown)

                G



                G
                     ✗ meter 6/8                ✗ form ABAB

                    MiniMax-M3 (zero-shot)
                    not rendered: repeat-signs-forbidden
                    X:1 ⏎ T:Monophonic Tune ⏎ M:6/8 ⏎ L:1/8 ⏎ K:G ⏎ |: D | G2 B d2 B | A2 F D2 F | G2 A B2 c | d2 c B2 A | ⏎ G2 B …

                     ✗ meter 6/8                ✗ form ABAB

                    MusicRLVR (Direct, Qwen3-4B) (16 bars)

                G



                G
                     ✓ meter 6/8                ✓ form ABAB

Qwen3-32B (zero-shot) fails meter, structure; Llama-3.1-70B (zero-shot) fails meter, structure; MiniMax-M3
(zero-shot) fails at the parse gate (repeat-signs-forbidden); MusicRLVR (Direct, 4B) satisfies every constraint.


Example 13: Edge split (k = 2, a 5/4 meter, outside the RL prompt range).
Item eg-0033. Constraints: (1) the meter must be 5/4, and every bar must contain exactly the right total duration; (2) every
note must lie between C4 and C5 inclusive
                    Qwen3-32B (zero-shot) (163 bars; first 16 shown)

                G



                G
                     ✗ meter 5/4                ✓ range C4–C5

                    Llama-3.1-70B (zero-shot) (12 bars)

                G



                G
                     ✗ meter 5/4                ✓ range C4–C5

                    MiniMax-M3 (zero-shot)
                    not rendered: degenerate-or-polyphonic
                    X: 1 ⏎ T: Five-Four Tune ⏎ M: 5/4 ⏎ L: 1/4 ⏎ K: C

                     ✗ meter 5/4                ✗ range C4–C5

                    MusicRLVR (Direct, Qwen3-4B) (5 bars)

                G
                     ✓ meter 5/4                ✓ range C4–C5

Qwen3-32B (zero-shot) fails meter; Llama-3.1-70B (zero-shot) fails meter; MiniMax-M3 (zero-shot) fails at the parse gate
(degenerate-or-polyphonic); MusicRLVR (Direct, 4B) satisfies every constraint.
Example 14: Edge split (k = 2, rhythm restriction + abab structure).
Item eg-0005. Constraints: (1) use only quarter and half notes (no dotted notes, no other durations, no rests); (2) the tune must
be exactly 16 bars with an ABAB form in 4-bar units: labeled units with the same letter must be note-for-note identical, and units
with different letters must differ
                     Qwen3-32B (zero-shot) (16 bars; 4 bars per row)

                 G


                 G


                 G


                 G
                      ✓ rhythm set               ✗ form ABAB
                     Llama-3.1-70B (zero-shot) (16 bars; 4 bars per row)

                 G


                 G


                 G


                 G
                      ✓ rhythm set               ✗ form ABAB
                     MiniMax-M3 (zero-shot)
                     not rendered: repeat-signs-forbidden
                     X: 1 ⏎ T: ABAB Tune ⏎ M: 4/4 ⏎ L: 1/4 ⏎ K: G ⏎ |: G2 B2 | d2 B2 | A2 G2 | E2 D2 | ⏎ G2 B2 | d2 B2 | A2 …

                      ✗ rhythm set               ✗ form ABAB

                     MusicRLVR (Direct, Qwen3-4B) (16 bars; 4 bars per row)

                 G


                 G


                 G


                 G
                      ✓ rhythm set               ✓ form ABAB

Qwen3-32B (zero-shot) fails structure; Llama-3.1-70B (zero-shot) fails structure; MiniMax-M3 (zero-shot) fails at the
parse gate (repeat-signs-forbidden); MusicRLVR (Direct, 4B) satisfies every constraint.
G    Broader Impact
In this section, we expand the ethics statement. The
method makes music-generation models follow ex-
plicit specifications, which helps wherever a score
must meet a specification: music education, game
audio, accessibility tools. We do not foresee sig-
nificant negative societal impacts specific to this
work, which concerns short monophonic melodies
in ABC notation under explicit constraints. The
likeliest misreading is to take a high all-satisfied
rate as a quality score; it certifies that the requested
properties hold. All supervised targets derive from
the publicly available IrishMAN corpus of tradi-
tional Irish music; the reinforcement prompts are
generated synthetically. The benchmark and veri-
fiers will be released to support reproducibility and
further research.
