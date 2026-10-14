                                                            Plans You Can Check: Verifier-Grounded Learning
                                                         of an Open-Weight Planner for Executable Video-Editing
                                                      Haoyu Wang1,2,† , Cheng Feng3,† , Liuyang Bian2,† , Ruiyang Huang4,5,†
                                                             Lei Wei5 , Yafei Wen2 , Xiaoxin Chen2 , Xiaoying Tang6,7,8,Q
                                                1
                                                  School of Artificial Intelligence, The Chinese University of Hong Kong, Shenzhen
                                                          2
                                                            vivo AI Lab 3 University of the Chinese Academy of Sciences
                                                                     4
                                                                       Southeast University 5 Peking University
                                             6
                                               School of Science and Engineering, The Chinese University of Hong Kong, Shenzhen
                                                       7
                                                         Shenzhen Future Network of Intelligence Institute (FNii-Shenzhen)
                                         8
                                           Guangdong Provincial Key Laboratory of Future Networks of Intelligence, CUHK-Shenzhen
                                                                                          Q
                                                                                              tangxiaoying@cuhk.edu.cn
arXiv:2608.25622v1 [cs.CV] 26 Aug 2026




                                                                  Abstract                                    A. Current Systems: Planning Stays Implicit                                 B. RefineCut: Planning Becomes Explicit




                                             Practical video editing is not only pixel gener-                              Editing intent + Assets                                  Editing intent + Assets + ledger


                                             ation: an editor must turn a brief, a clip pool,               Prompt / human / unified edit model               Edited video /
                                                                                                                                                              Generated clip
                                                                                                                                                                                     RefineCut-Evo Planner
                                                                                                                                                                                                                        Refine Patch    Edited video /
                                                                                                                                                                                                                                        Generated clip
                                                                                                                                                                                         Open-weight 8B Model
                                             music metadata, and hard constraints into an
                                                                                                                                        transition
                                             executable timeline. We study this decision                     Clip choice     timing                  insert
                                                                                                                                                                                                                                       Executable edit
                                                                                                                                                                                                                                            plan
                                                                                                                                                                                                 Verifier     Student      Verifier
                                             layer as executable video-editing planning and                                   Explicit plan ？
                                                                                                                                                                               Teacher
                                                                                                                                                                                traces           replay       Repairs      & Rubric
                                                                                                                                                                                                                   High-Margin

                                             introduce RefineCut, which, unlike workflow                                                                                             Verified
                                                                                                                                                                                   supervision
                                                                                                                                                                                                                      Pairs




                                             systems that wrap a prompted frontier model,                              Hard to
                                                                                                                       replay
                                                                                                                                              Hard to
                                                                                                                                              verify
                                                                                                                                                              Hard to train              Replayable
                                                                                                                                                                                                                Local open-
                                                                                                                                                                                                                weight planner
                                                                                                                                                                                                                                           Reusable
                                                                                                                                                                                                                                           supervision


                                             trains a compact open-weight planner for it.                            RefineCut learns an open-weight planning layer that turns editing intent into executable edit plans
                                             The planner edits a typed timeline through
                                             structured patches covering clip selection, trim-             Figure 1: From implicit to explicit planning. Re-
                                             ming, ordering, transitions, and duration and                 fineCut turns implicit prompted editing into explicit,
                                             music alignment; a deterministic verifier ap-                 verifier-trained executable planning.
                                             plies each patch and checks it against an ex-
                                             plicit constraint ledger. Because editing has
                                             no single ground-truth repair, we do not imi-                 order them, which transitions to use, and how to
                                             tate teachers directly: RefineCut replays every               align cuts to music. These decisions are tightly
                                             multi-teacher branch through the verifier and                 constrained: the final cut must hit a target duration,
                                             keeps verifier-best repairs as supervision. A                 retain or exclude specific clips, respect pacing, and
                                             second stage, RefineCut-Evo, lets the student                 stay synchronized to a soundtrack. The deliverable
                                             score its own repairs with the verifier and a
                                                                                                           is a structured edit plan, executed afterwards by a
                                             task rubric and trains on high-margin prefer-
                                             ence pairs, so the final 8B planner runs in a
                                                                                                           downstream toolchain. Editing, in other words, is
                                             closed verifier loop with no teacher calls at                 first a constrained planning problem and only later
                                             inference. On RefineCut-Bench (3,578 tasks,                   a rendering problem.
                                             7,971 captioned clips, 499 music tracks, ex-                     Recent systems address the layer below this de-
                                             plicit ledgers), verifier-replayed distillation lifts         cision process or sidestep it entirely. Text-to-video
                                             the planner from 0.620 to 0.858 on the protocol-
                                                                                                           and image-to-video models generate or transform
                                             specific Video-Editing Score and RefineCut-
                                             Evo reaches 0.924; the gain transfers to Llama-               pixels directly (Zhuang et al., 2024; Long et al.,
                                             3.1-8B and GLM-4-9B, and in the same closed                   2024), and instruction-editing frameworks modify
                                             loop the 8B planner matches or exceeds its                    content within a single shot (Yoon et al., 2025);
                                             frontier teachers. Code and RefineCut-Bench                   none produces a clip-level plan over a real footage
                                             are publicly released; see the Data Availability              pool. Workflow-oriented mashup and dubbing sys-
                                             statement.                                                    tems (Li et al., 2026a; Zhang et al., 2025; Hu et al.,
                                                                                                           2024; Lin et al., 2026; Liang et al., 2025) do oper-
                                         1   Introduction                                                  ate at the decision layer, but realize it by prompt-
                                                                                                           ing a frozen frontier backbone inside a hand-built
                                         Real-world video editing is rarely about generating               scaffold. The cost is real: the planning policy is
                                         new pixels. Given a pool of existing footage, an                  never updated, so it cannot be optimized against the
                                         editor decides which clips to keep, how to trim and               hard constraints a brief imposes, and is locked to a
                                             †                         Q
                                                 Equal contribution.       Corresponding author.           closed-source model. What the community lacks
is a compact, open-weight planner that learns edit-         Max, and DeepSeek-V4-Pro (DeepSeek-AI, 2026),
ing decisions and can sit in front of any rendering         replays each candidate branch through the verifier,
back-end, as shown in Figure 1.                             and keeps verifier-best branches as SFT targets and
   We argue this gap is also a missed opportunity,          mixed-granularity preference pairs, yielding the
because the editing decision layer has a property           Mixed-Pref 8B planner. Stage 2, RefineCut-Evo,
open-ended generation lacks: its outputs can be             performs verifier-centered, rubric-structured self-
checked. We formalize the layer as executable               improvement: the student scores its own repair can-
video-editing planning. A task instance gives the           didates with the verifier and a task-specific rubric
planner a brief, a real clip pool with captions and         (ER1–ER7), and high-margin pairs train it with
metadata, optional music with beat tracks, the              Direct Preference Optimization (DPO) (Rafailov
current timeline state, and, crucially, an explicit         et al., 2023). Supervision thus shifts from exter-
constraint ledger enumerating what the final cut            nal teachers to verifier-grounded self-improvement,
must satisfy. The planner emits a RefinePatch: an           and at inference the planner runs in a closed verifier
RFC 6902-style JSON Patch (Bryan and Notting-               loop with no teacher calls.
ham, 2013) over a typed timeline state. Because
every requirement is an explicit ledger entry, a            Contributions.
deterministic verifier, rather than a learned LLM
                                                               • We formulate executable video-editing plan-
judge (Zheng et al., 2023), can apply each patch
                                                                 ning and release RefineCut-Bench, a planning-
and recompute the ledger entry by entry, following
                                                                 level benchmark with real clip/music meta-
execution-based supervision in verifiable domains
                                                                 data, constraint ledgers, and multi-teacher tra-
such as mathematical reasoning and code (Cobbe
                                                                 jectories.
et al., 2021; Lightman et al., 2024; Lambert et al.,
2025). This verifiability is what makes the plan-              • We propose verifier-replayed trajectory dis-
ning layer learnable in a way pixel-level generation             tillation: canonical normalization plus deter-
is not.                                                          ministic replay that converts noisy frontier
   Turning this observation into a trained planner               traces into verified SFT targets and mixed-
is still not a single-target imitation problem. The              granularity preference pairs.
natural starting point is to distill trajectories from         • We introduce RefineCut-Evo, an EvoLM-
frontier models, since tool-use trajectories can su-             inspired (Li et al., 2026b) verifier-centered,
pervise planner behavior (Zeng et al., 2024) and                 rubric-structured self-improvement stage
step-level feedback can turn successful and failed               trained with DPO on verifier- and rubric-
attempts into preference signals (Song et al., 2024b;            scored candidates.
Xiong et al., 2024). But editing has no single
ground-truth repair: the same brief admits many                • Across Qwen3-8B, Llama-3.1-8B, and GLM-
valid cuts, so a teacher’s first-choice branch is a              4-9B, verifier replay beats raw imitation, and
guess, not a label, which is why preference-based                the final 8B planner matches its frontier teach-
learning, not imitation of one reference, is standard            ers in the same closed loop (Section 4).
for open-ended generation (Christiano et al., 2017;
Stiennon et al., 2020; Ouyang et al., 2022). A plan-        Positioning. RefineCut is closest to workflow-
ner that imitates noisy teacher traces inherits their       oriented video and multimodal creation systems
noise. We therefore replay every candidate branch           such as DIRECT, LVAS-Agent, GLANCE, StoryA-
through the verifier before using it, and let the stu-      gent, and UniVA (Li et al., 2026a; Zhang et al.,
dent keep improving on its own verified repairs             2025; Lin et al., 2026; Hu et al., 2024; Liang et al.,
after distillation (Madaan et al., 2023; Yuan et al.,       2025), but those systems keep the editing policy
2024).                                                      inside prompted frontier-model workflows. It also
                                                            builds on tool-executable planner learning and on
   RefineCut is a two-stage framework built on this
                                                            self-improvement ideas from EvoLM and Rubric-
logic: editing decisions should be learned and veri-
                                                            Grounded RL (Li et al., 2026b; Bhattarai et al.,
fied, not prompted. Stage 1, the verifier-replayed
                                                            2026), while using a deterministic editing verifier
teacher bootstrap, canonicalizes traces from three
                                                            rather than a general LLM judge as the primary
frontier API teachers, namely GPT-5.41 , Qwen3-
                                                            nical report at the time of writing. Qwen3-Max: https:
   1
       GPT-5.4: accessed via API in 2026, no public tech-   //huggingface.co/Qwen.
training signal. Appendix A gives the full related-        Editing state and edit artifact. The state st
work discussion.                                           holds the selected clip sequence, segment dura-
                                                           tions, transition styles, music-sync parameters, gen-
2     Task and Benchmark                                   erated placeholder slots, and per-entry ledger satis-
                                                           faction. The planner edits it through a RefinePatch,
This section formalizes planning-level video edit-         an RFC 6902-style JSON Patch over the typed time-
ing as a task, derives the evaluation principles used      line state; a typed patch (rather than free-form text)
throughout the paper, and introduces RefineCut-            is what makes each step machine-applicable and
Bench as the dataset, verifier, and multi-teacher          machine-checkable. When the brief calls for con-
trajectory resource that Section 3 turns into super-       tent absent from the pool, a placeholder slot records
vision.                                                    the requested prompt and position, with visual gen-
                                                           eration delegated downstream. Prompts use task-
2.1    Planning-Level Video Editing                        local clip aliases, so measured performance reflects
RefineCut studies the decision layer of video edit-        planning ability rather than memorization of global
ing: the layer that turns an editing intent and a pool     clip identifiers. Schema details are in Appendix C.
of footage into an executable edit plan. The final         Constraint ledger L. Each ledger entry is
video is rendered by a downstream toolchain, not           a tuple (item_id, type, spec, satisfied, evidence),
by the planner, which never observes pixels and            spanning seven field-level constraint families: du-
reads only textual clip captions and visual meta-          ration, transition, music_sync, clip inclusion, clip
data from an upstream vision-language captioner,           exclusion, repeat limit, and pacing; generated-
as in prior work where a language model reasons            placeholder requirements are represented as task-
over captions rather than raw frames (Zeng et al.,         structure constraints checked by the same verifier
2023; Krishna et al., 2017).                               (subtypes in Appendix B.4). The ledger makes edit-
                                                           ing requirements explicit and machine-checkable,
Task definition.     A task instance is a tuple
                                                           as in verifiable instruction-following (Zhou et al.,
                                                           2023; Jiang et al., 2024). An entry is a hard
              x = (b, C, M, s0 , L),                (1)    constraint when its spec admits a deterministic
                                                           pass/fail test (e.g., a target duration within toler-
where b is a natural-language brief; C is a real           ance, a clip that must be kept or excluded), and
clip pool, each clip carrying a caption and visual         H ARD PASS is the event that every hard constraint
metadata (scene, motion intensity, camera dura-            holds simultaneously. Softer entries earn graded
tion); M is optional music metadata (beat times            credit: keeping two of three required clips fails the
and energy); s0 is the initial timeline state; and L is    must_keep_clip entry (and H ARD PASS) but still
an explicit constraint ledger enumerating what the         counts toward the constraint-satisfaction rate and
final cut must satisfy. A planner is a policy πθ that      a required-clip recall of 2/3. The verifier, not the
at step t emits an edit patch pt ∼ πθ (· | x, st , Lt );   planner, recomputes the satisfied field after every
a deterministic verifier applies it, advancing the         patch.
state as st+1 = Apply(st , pt ) and recomputing the
ledger as Lt+1 = Verify(st+1 ). The objective is           2.3   What Makes an Editing Plan Valid?
to reach a ledger-satisfying state within a small re-
                                                           A valid edit plan must be executable, grounded in
pair budget; the closed-loop execution is detailed
                                                           the given clips, satisfy the explicit constraints with-
in Section 3.
                                                           out breaking satisfied ones, and converge within
                                                           a small repair budget. These requirements form a
2.2    Inputs, Outputs, and Editing State
                                                           hierarchy, which our evaluation mirrors with three
Clip pool and metadata. Clip captions and vi-              layers. The first layer, the execution gate, is a hard
sual metadata are produced offline by an upstream          prerequisite covering schema validity, patch appli-
vision-language captioner (Krishna et al., 2017;           cability, and timeline validity; a plan that fails it
Wang et al., 2024); music metadata (beat times,            is not executable at all, mirroring execution-based
energy) is extracted by a standard beat-tracking           evaluation in code generation (Jimenez et al., 2024).
pipeline and supports music-synchronization con-           Conditioned on the gate, the second layer, plan-
straints (Davis and Agrawala, 2018).                       ning quality, asks whether the executable plan actu-
Figure 2: RefineCut-Bench overview. The benchmark ties real clip/music metadata, explicit ledger constraints,
multi-teacher trajectories, and verifier-based evaluation into one planning-level protocol.


ally satisfies the brief, from constraint satisfaction   Assets, tasks, and splits. The asset library
and clip grounding to duration, pacing, and conver-      draws from 7,971 captioned clips, 23,913 caption-
gence. Both layers are decided entirely by the deter-    anchored frames, and 499 music tracks. Tasks span
ministic verifier, so every score is a checkable con-    three families, (A) multi-clip composition, (B) tar-
sequence of the ledger rather than a learned judg-       geted insertion or replacement, and (C) generative
ment. Finally, the third layer, human-rendered qual-     composition with placeholder slots, totaling 15 sub-
ity, is assessed after rendering and covers instruc-     types and 3,578 canonical tasks. Raw records are
tion fit, content relevance, temporal coherence, shot    deduplicated into canonical tasks and split at the
continuity, pacing, audio-visual rhythm, and over-       record level. Because resampled variants of one
all quality, following established human-evaluation      task can otherwise straddle the train/test bound-
practice for edited video (Huang et al., 2024; Liu       ary, we mark a canonical-clean test subset whose
et al., 2024). The two families are complementary:       canonical identifiers never appear in training, and
verifier metrics test whether a plan executes under      use it to check that headline gains cannot be at-
the ledger, human evaluation whether the rendered        tributed to canonical-id overlap (Section 4.8). Split
edit is perceptually preferred. We report compo-         sizes, per-subtype and per-constraint distributions,
nent metrics with the VES summary; definitions           and the captioning pipeline are in Appendix B and
and weights are in Section 4.2 and Appendix D.           Table 6.

2.4   RefineCut-Bench                                    2.5   Multi-Teacher Trajectories as Noisy
                                                               Supervision
RefineCut-Bench instantiates the task above as a
controlled, executable-planning benchmark. Exist-        RefineCut-Bench also releases a multi-teacher tra-
ing video-editing resources either evaluate rendered     jectory resource, like recent releases of agent trajec-
pixels or wrap a prompted frontier model in an           tories as a training signal rather than only an evalu-
agent scaffold whose decisions are never checked         ation target (Zeng et al., 2024; Song et al., 2024a).
against an explicit specification; to our knowledge,     For every training task we run one refinement roll-
RefineCut-Bench is the first to tie four ingredients     out from each of three independent frontier API
into one planning-level release: real clip and music     teachers (GPT-5.4, Qwen3-Max, and DeepSeek-
metadata, explicit constraint ledgers, multi-teacher     V4-Pro); at each refine step a teacher emits several
trajectories, and a deterministic verifier-based eval-   candidate branches, each a proposed RefinePatch,
uation protocol (Appendix B, Figure 2, Table 6).         with its own first-choice flag (coverage and schema
in Appendix B.6).                                        references against task-local aliases. Schema, path-
   This resource is noisy by construction. Be-           alias table, and validation rules are in Appendix C.
cause editing admits no single ground-truth repair,
teachers disagree on schema, branch structure, and       3.3   Verifier Replay and Branch Arbitration
which branch is best; a first-choice flag is a guess,    For every canonicalized step we keep up to four
not a label, and even one teacher’s branches vary        branches with distinct repair_operators and
in executable quality. Multi-teacher distillation        Jaccard-distinct clip selections, then replay each
that imitates such heterogeneous demonstrations di-      through the deterministic verifier. For branch b
rectly would inherit their inconsistency (Tian et al.,   at state st , the verifier validates and applies the
2025). The constraint ledger offers a way out:           patch, recomputes the ledger L′ , and scores six
every branch can be canonicalized and replayed           signals: constraint-satisfaction change, targeted re-
through the deterministic verifier, which scores it      pair, required-clip recall, patch applicability, no-
against the same explicit ledger regardless of its       regression, and locality. The exact weighted defini-
source. Verifier replay thus converts an inherently      tion is in Appendix D; we write the scalar score as
noisy resource into a consistently graded supervi-       V (b). The verifier-best branch advances the state,
sion signal, the mechanism Section 3 builds on.          and branch score gaps drive preference pairing.
                                                         The full procedure is summarized in Appendix F,
3     Method: Verifier-Replayed Distillation             Algorithm 1.
      and Verifier-Centered
      Self-Improvement                                   3.4   Verifier-Replayed Distillation
                                                         Replay gives two supervision signals. Verified
3.1    Overview and Trajectory Collection
                                                         SFT retains the verifier-best branch as p⋆ when
Our method has two offline learning stages and           it canonicalizes and applies, repairs at least one vi-
one runtime loop, shown in Figure 3. Stage 1,            olated ledger entry, regresses no satisfied constraint,
verifier-replayed teacher bootstrap, canonicalizes       and, for clip-grounding repairs, references a legiti-
raw multi-teacher trajectories and replays every         mate task-local alias. We fine-tune on these canon-
candidate branch through the verifier; verifier-best     icalized patches with standard next-token cross-
branches yield verified SFT targets and mixed-           entropy. Mixed-granularity preference combines
granularity preference pairs that produce an initial     step-level pairs, in which the verifier-best branch
8B planner, Mixed-Pref. Stage 2, RefineCut-Evo,          is paired against a low-scoring branch separated
samples K=4 student repairs on training states,          by margin δ, with trajectory-level pairs ranked by
scores them by verifier and rubric ER1–ER7, and          terminal verifier score. We fine-tune the SFT check-
trains with DPO on high-margin pairs. At runtime,        point with offline DPO (Rafailov et al., 2023):
the planner and verifier run the Apply/Verify closed
loop defined in Section 2.1 for at most T =3 steps.            LDPO = −E(x,p+ ,p− ) log σ(βz) ,
   Each teacher-covered task receives one refine-                  z = ∆θ (p+ , x) − ∆θ (p− , x),           (2)
ment rollout from each available frontier API              ∆θ (p, x) = log πθ (p | x) − log πref (p | x).
teacher (GPT-5.4, Qwen3-Max, and DeepSeek-V4-
Pro). Each refine step contains multiple candidate       Here p+ and p− are the preferred and rejected
RefinePatch branches. The teacher’s first-choice         branches, πref is the frozen SFT checkpoint, and
flag is recorded but not treated as ground truth: the    β controls deviation from it. Preferences come
verifier picks the training target. Per-teacher counts   from executable verifier replay rather than LLM
and the branch schema are in Appendix B.6.               judgments; the resulting checkpoint is Mixed-Pref.

3.2    Canonical Trajectory Normalization                3.5 RefineCut-Evo: Verifier-Centered Student
Raw teacher outputs are heterogeneous: some wrap             Self-Improvement
the task in an envelope, some flatten multi-step         RefineCut-Evo improves the student with its own
trajectories, and others nest branches as lists. We      repairs scored by the verifier and a fixed, task-
rewrite them into canonical patch trajectories keyed     specific editing rubric, following recent rubric-
by (task_id, teacher_id), map JSON Pointer               guided self-improvement work (Li et al., 2026b;
paths to a canonical namespace, and validate clip        Bhattarai et al., 2026).
                         A. Tasks & Noisy Teachers                                                    B. Verifier-Replayed Training                                               C. Closed-Loop
                                                                                                                                                                                          Executable Editing
                                                                                                                                                                                                     Edit Plan Agent

 A.1 Tasks Families
                                                                                             B.1 Canonicalize & Replay                                                     C.1 State + Ledger
                                                                                                                                                      Verifier Replay                                             3/5
                                                                                                                                                         state !!          EditableTimeline State !!              OK      3 1         1
                                                                                                                                                                     ...
                                                                                                                                                                                                                   Duration Bounds
                                                                                                                               Replace
           Composition              Insert / Replace     Generated Insert                                                                                                  Segment Durations (s)                   Transition rules
                                                                                                                                                                                                                   Step budgets ( ≤ 3)
                                                                                                                               Reorder                                     2.4s   3.1s   4.0s   2.8s
                                                                                                                              Duration                                     Transitions
  A.2 Frontier Teachers                                     Shared Task                                                                                    Verifier V                                              Forbidden items
                                                       Òbuild a 4-shot adventure         teacher trajectories
                                                                                                                            Placeholder                                     Cut    Dip   Wipe     Cut              Style consistency
                                                       reel. Replace skyline ->
                                                       sunrise city, mountain ->
                                                       volcano, keep rally shot,             B.2 Two-Stage Planner Training
                                                       generate ending, preserve                                                                                           C.2 Planner
                                                       duration      and   music
                                                       alignment Ó                           base planner                                              initial planner
                                                                                                                                                                                     RefineCut-Evo Planner                 Output:




                                                                                   Stage 1
                                                                                                                             verified SFT                                                                                RefinePatch
                                                                                                                                   +                                                            state ""
                                                                                                                             mixed prefs
                                                                                              Qwen3-8B                                                      &&'&!                         violated items #"
    GPT-5.4                 Replacement                       Reorder
                                                                                                                                                                                           step budget $"
                                                                                                                   sample K=4




                                                                                   Stage 2
DeepSeek-V4-Pro                                                                                                 ## . . . #$ ∼ &% !!                       RefineCut-Evo
                            Replacement                   Generate Insert                                                                                trained planner   C.3 Verify & Update
                                                                                                                Self-
                                                                                                   update                                   verifier                       Apply Patch          Recompute State         Update Ledger
                                                                                                   planner   Improvement                    & rubric
  Qwen3-Max
                                                                                                                                                              &()*
                            Replacement                   Adjust Duration
                                                                                                                High-Margin Pairs
  A.3 Misalignment                                       Teacher-chosen "!
                                                                                                                   3. 4 / ∣ 60        3. 4 4 ∣ 60
                                                                                             ++,- = −./0 12 ./0                 − ./0
                                                                Reorder                                                                                                              Accept                       Reject
                                                                                                                  3123 4 / ∣ 60       3123 4 4 ∣ 60
                                                           Verifier-best "∗!                                    4 / , 4 4 → 356-                                                                repeat ≤ #
                                        Verifier
 Selected state !! from Qwen3-Max   compares actions
                                                               Reorder

                                                                                                    Verifier replay and self-improvement                                                    Executable Edit Plan
                     teacher-chosen ≠ verifier-best
                                                                                                     turns noisy trajectories into !()*                                                     final_plan.json




Figure 3: Framework. Noisy teacher trajectories become verified supervision; verifier- and rubric-scored student
repairs drive self-improvement and closed-loop planning.


Candidates and rubric. For each training state                                                                                 4          Experiments
we sample K=4 RefinePatches from Mixed-Pref,
parse and replay them, and filter schema or ap-                                                                                We address five research questions (RQ1–RQ5),
ply failures. The rubric ER1–ER7 covers Intent,                                                                                a robustness and failure analysis, and a blind
Ledger Satisfaction, Clip Grounding, Timeline Co-                                                                              rendered-preview evaluation.
herence, Duration/Pacing, Music/Beat, and Edit                                                                                 4.1           Experimental Setup
Economy; per-family weights and deterministic
fallback proxies are in Appendix F.                                                                                            Benchmark. All main results are on Common-100,
                                                                                                                               with a single PatchPlanner prompt shared by every
Joint
P7 scoring and training.P       Writing R(c) =                                                                                 model; canonical-clean (N =92) is held out for ro-
   m=1 αm rm (c) with     m αm = 1, each candi-                                                                                bustness checks. dev100 is used once, to pick the
date receives S(c) = λV (c) + (1 − λ)R(c), where                                                                               RefineCut-Evo checkpoint (step 300; Appendix G,
V (c) is the verifier score from Section 3.3 and                                                                               Table 16), before any test-set measurement. At test
λ = 0.65. At each state we choose                                                                                              time the planner interacts only with the verifier; no
                                                                                                                               teacher is called.
           c+ = arg max S(c),
                                    c∈C(s)
                                                                                                             (3)                  Loop and budget. The closed loop runs at most
              −
           c ∈ {c ∈ C(s) : S(c ) − S(c) ≥ τ }.            +                                                                    T =3 repair steps, the same horizon used to collect
                                                                                                                               teacher trajectories (Appendix B.6) and to define
Thus c− is a lower-scoring hard negative rather than                                                                           Converged@3. During Evo training we draw K=4
the lowest sampled candidate. RefineCut-Evo starts                                                                             student candidates per state, matching the teacher
from Mixed-Pref and trains with DPO on these                                                                                   branch budget.
pairs; hyperparameters and the dev100 selection                                                                                   Models. The main progression trains Qwen3-
rule are in Appendix E. Section 4.6 analyzes the                                                                               8B-Instruct with LoRA (Hu et al., 2022): Prompted
verifier and rubric contributions.                                                                                             (no training, same verifier loop), Raw, Verified,
                                                                                                                               Traj-Pref, Mixed-Pref, and RefineCut-Evo, all built
3.6        Closed-loop Deployment                                                                                              on the teacher trajectories of Section 2.5. To check
At test time the planner reads st and the still-                                                                               that verifier-replayed supervision is not tied to one
violated ledger entries and emits one RefinePatch;                                                                             backbone, we rerun the Prompted / Raw / Verified
the verifier validates, applies, and recomputes the                                                                            comparison on Llama-3.1-8B-Instruct and GLM-4-
ledger. No teacher is called at inference. The loop                                                                            9B with identical data, recipe, and protocol (Sec-
repeats for at most T =3 steps, after which the final                                                                          tion 4.7). Hyperparameters and prompts are in
state is dispatched to the editing toolchain.                                                                                  Appendices E–I.
                      Prompted / imitation               Verifier-replay distill.       Self-impr.                          Constraint adherence        Loop quality       Overall
              0.9                                                                   +0.060
                                                                                                     Model                FCSR        Hard     ReqCR    Dur        Cvg      VES
              0.8                                                                                    Prompted backbone and raw imitation
        VES
                                         +0.238                                                      Prompted           0.608     0.150         0.273    0.660     0.210     0.594
              0.7                                                                                    Raw                0.559     0.160         0.723    0.440     0.250     0.620

              0.6                                                                                    Verifier replay distillation
                                                                                                     Verified                 0.880    0.630    0.975    0.820     0.790     0.858
                       ted         Raw          ifie
                                                     d            ef       Pre
                                                                               f           vo        Traj-Pref                0.877    0.670    0.969    0.840     0.790     0.864
                    mp                       Ver              j-Pr      ed-           ut-E
                Pro                                       Tra        Mix         ineC
                                                                             Ref                     Mixed-Pref               0.882    0.670    0.969    0.830     0.800     0.864

                                                                                                     Self-improvement (final)
Figure 4: Training-stage progression. Common-                                                        RefineCut-Evo⋆        0.953 0.820 0.981 0.980  0.950  0.924
100 VES across checkpoints; annotations mark the                                                     ∆ vs. Mixed-Pref +0.071 +0.150 +0.012 +0.150 +0.150 +0.060
Raw→Verified and Mixed-Pref→Evo aggregate gains.
                                                                                                     Table 1: Closed-loop planning results on Common-
                                                                                                     100. The ∆ row gives aggregate changes relative to
4.2   Evaluation Metrics                                                                             Mixed-Pref; ⋆ marks the final RefineCut checkpoint.
Automatic metrics evaluate executable planning:
                                                                                                                            Replay scale             Verifier components
schema validity, patch applicability, timeline va-
                                                                                                     Teacher                N     Branches FCSR Hard PASR ReqCR VES
lidity, constraint satisfaction, hard-constraint pass,
                                                                                                     GPT-5.4         2,000            6,000    0.379 0.015 0.872     0.698 0.521
clip grounding, duration/pacing, no-regression, and                                                  Qwen3-Max       1,946            3,892    0.446 0.016 0.989     0.712 0.557
convergence. The Video-Editing Score (VES) ag-                                                       DeepSeek-V4-Pro 1,959            3,920    0.473 0.028 0.946     0.703 0.559

gregates them as                                                                                     Table 2: Verifier-best replay diagnostics by teacher.
 VES = 0.30 FinalCSR + 0.15 HardPass
                                                                                                     Per-branch values are computed from replay logs; this
       + 0.15 PASR + 0.15 ReqClipRecall                                                              diagnoses the teacher resource, not student closed-loop
       + 0.10 DurationPass + 0.10 TimelineValidity                                                   performance.
       + 0.05 NoRegression.
                                                                                                     fine step, the three teachers disagree on schema and
The same frozen ledger and verifier that score VES
                                                                                                     branch structure, and even their best branches are
also drive replay and closed-loop feedback, so VES
                                                                                                     partial repairs rather than solved plans. Before any
is an in-protocol measure, not an independent judg-
                                                                                                     branch becomes supervision, we therefore canon-
ment; we always report the component metrics
                                                                                                     icalize it, apply it to the real editing state, and let
with it and check rendered-preview preference sep-
                                                                                                     the verifier score the result. Table 2 shows what
arately (Section 4.9). Definitions and weight sen-
                                                                                                     this replay finds.
sitivity are in Appendices D–G; tables abbreviate
                                                                                                        Even the verifier-best branches, which almost
Converged@3 as C VG.
                                                                                                     always apply cleanly (PASR 0.87–0.99), almost
4.3   RQ1: Can an Open-Weight Planner                                                                never satisfy the whole ledger in one step (H ARD
      Learn Executable Editing Planning?                                                             ≤ 0.03): a teacher’s first choice is a weak label,
An open-weight planner can learn executable edit-                                                    and which branch actually helps depends on the
ing planning, and the two training stages contribute                                                 state it lands on. Table 1 shows the consequence.
in different ways (Table 1, Figure 4). Verifier-                                                     Imitating teacher-selected branches yields VES
replayed SFT does most of the work, lifting VES                                                      0.620, barely above the prompted backbone, while
from 0.620 to 0.858; preference training over the                                                    training on verifier-best branches yields 0.858 from
same traces adds little on aggregate (0.864) un-                                                     a training set three times smaller (3,317 vs. 9,690
til RefineCut-Evo reaches 0.924. Where the Evo                                                       examples). The gain comes from replay filtering
gain lands explains what it adds: H ARD PASS rises                                                   out branches that fail on execution, not from more
0.670→0.820, D UR @2 S 0.830→0.980, and C ON -                                                       data.
VERGED @3 0.800→0.950 – precisely the all-or-
                                                                                                     4.5       RQ3: Can RefineCut-Evo Self-Improve
nothing checks a finished plan must pass, not prop-
                                                                                                               Beyond Mixed-Pref?
erties of any single patch. Distillation teaches the
planner to make edits that execute; Evo teaches it                                                   It does, and the improvement behaves like targeted
to finish plans that satisfy the whole brief.                                                        repair rather than a broad shift. Of the 100 test
                                                                                                     tasks, Evo improves 22 and degrades only 5, leav-
4.4   RQ2: Why is Verifier Replay Needed?                                                            ing the other 73 untouched, which moves the ag-
Teacher traces cannot be imitated as they are. Each                                                  gregate from 0.864 to 0.924. The paired gain of
teacher proposes several candidate branches per re-                                                  +0.059 VES (95% CI [0.028, 0.092]) is not noise,
                             Component metrics            Overall                                       VES by training stage           Gain
Variant             FCSR       Hard     Dur      Cvg        VES          Backbone             Prompted           Raw        Verified    ∆V−R
Rubric-margin DPO   0.9530     0.820   0.980     0.950        0.9237     Qwen3-8B                     0.594      0.620          0.858   +0.238
Verifier-only DPO   0.9395     0.780   0.940     0.900   0.9085↓ 0.015   Llama-3.1-8B                 0.566      0.496          0.649   +0.153
No-margin DPO       0.9178     0.760   0.910     0.870   0.8965↓ 0.027   GLM-4-9B                     0.643      0.607          0.686   +0.079
UCPO-lite DPO       0.9012     0.740   0.890     0.840   0.8800↓ 0.044
                                                                         Table 4: Cross-backbone transfer. Same data, recipe,
Table 3: RefineCut-Evo ablation under matched back-                      and frozen protocol; 95% CIs: +0.153 [0.109, 0.197],
bone, candidate pool, DPO recipe, and wall-clock bud-                    +0.079 [0.036, 0.120]. Full components in Appendix G,
get. Verifier-scored self-improvement is the primary                     Table 13.
signal; rubric-structured margins add 0.015.
                                                                         Policy (identical loop)                VES             Hard      Cvg
and the same picture holds on canonical-clean and                        Frontier teachers (online)
                                                                         GPT-5.4                                0.893            0.76     0.86
against the other distilled variants (Appendix G,                        Qwen3-Max                              0.773            0.63     0.72
Table 17).                                                               DeepSeek-V4-Pro                        0.936            0.89     0.95

                                                                         Untrained Qwen3-8B: prompting and search
4.6       RQ4: What Drives RefineCut-Evo?                                Direct prompting (T =1)            0.502                0.07     0.08
                                                                         + verifier feedback (T ≤3)         0.592                0.15     0.21
                                                                         R=4 verifier reranking             0.700                0.32     0.42
Evo differs from Mixed-Pref in two ingredients:                          Visited-pool oracle                0.712                0.32     0.40
preference pairs are scored by the verifier, option-                     RefineCut-Evo (8B, local)              0.924            0.82     0.95
ally refined by the rubric, and only high-margin
pairs are kept. Table 3 removes one ingredient at                        Table 5: Same-loop external comparison. All policies
a time, holding backbone, candidate pool, DPO                            use the identical state, ledger, RefinePatch interface,
                                                                         Apply/Verify loop, stopping rule, and T =3 budget. Full
recipe, and wall-clock budget fixed. Scoring pairs
                                                                         tables with latency, W/T/L, CIs, and R=1 sampling are
with the verifier alone already reaches 0.909, so                        in Appendix G.
certified repairs carry most of the gain; rubric-
structured margins add a further 0.015, concen-                          (−0.012, [−0.034, 0.010]), and matches the best
trated in duration (0.940→0.980) and convergence                         Converged@3 at 11.7 s/task locally; four newer
(0.900→0.950). Keeping every pair instead of only                        frontier policies land at 0.933–0.943 under the
high-margin ones costs 0.027, and replacing the se-                      same contract (Appendix G).
lection scheme altogether with UCPO-lite (Lochab                            The lower block rules out the cheaper explana-
et al., 2026) costs 0.044. Which pairs enter training                    tions. Verifier feedback lifts direct prompting from
matters more than how finely each pair is scored.                        0.502 to 0.592; R=4 verifier reranking reaches
4.7       RQ5: Does Verifier Replay Transfer                             0.700; and even an oracle that picks the best state
          Across Backbones, and Does RefineCut                           any of these runs ever visited stops at 0.712, still
          Compete with Frontier Policies?                                0.212 below Evo ([0.170, 0.252]). Searching over
                                                                         the verifier’s signal is not a substitute for learning
Verifier replay is not a Qwen-specific effect. Re-                       from it.
running the Prompted / Raw / Verified comparison
on Llama-3.1-8B and GLM-4-9B with the same                               4.8     Robustness and Failure Analysis
data and recipe repeats the pattern (Table 4): raw                       Aggregate numbers can hide the wrong kind of win:
imitation is flat on Qwen (+0.026) and harmful                           a gain that leans on task overlap, is bought with
on Llama and GLM (−0.070, −0.035), while veri-                           heavier editing, exists only under our own metric,
fied SFT recovers every family (+0.238, +0.153,                          or never engages with what the clips show. The
+0.079) and lifts required-clip recall to 0.98, 0.92,                    checks below rule these out in turn.
and 0.99. Absolute scores stay highest on Qwen3-
8B, the only backbone that also gets the preference                      Canonical-clean and human-written briefs.
stages.                                                                  The gain survives both the split and the instruction
   The second half of the question is whether the                        style. On canonical-clean (N =92), where no test
distilled planner can stand beside the frontier poli-                    task shares a canonical id with training, Evo scores
cies it learned from, so we run each teacher as an                       0.917 against 0.859 for Mixed-Pref with the variant
online policy in exactly the same loop (Table 5).                        ordering unchanged (Table 19); on Common-100
RefineCut-Evo ends above GPT-5.4 (+0.030 VES,                            each of the three task families improves individu-
95% CI [0.001, 0.062]) and Qwen3-Max (+0.150,                            ally, the local-repair family most of all (Table 20).
[0.091, 0.213]), statistically ties DeepSeek-V4-Pro                      On Human50, 50 free-form briefs written by seven
                                                                                               randomized A/B previews for each model pair (pro-
      RefineCut-Evo                                                                  9 fail    tocol in Appendix H). Evo beats Mixed-Pref in
                                                                                               100 of the 150 pairs, ties 34, and loses 16 (prefer-
         Mixed-Pref                                                                  26 fail
                                                                                               ence 0.780, κ=0.620); the sanity pair Mixed-Pref
                      0          25           50                  75              100          vs. Prompted, whose gap is large, reaches 0.887.
                           Closed-loop outcomes on Common-100 tasks
                          OK plan             Low CSR                  Patch-apply fail        Preference here scores the planner and renderer
                          Duration mismatch   Missing clip ref.
                                                                                               together, and it agrees with the VES ordering.
Figure 5: Failure composition. RefineCut-Evo in-
creases OK plans from 74 to 91 and reduces duration                                            4.10   Summary of Findings
mismatches from 16 to 1 on Common-100; the small                                               Verifier-replayed supervision provides the largest
residual tail shows all remaining closed-loop failure                                          single improvement over raw imitation and trans-
types.
                                                                                               fers across Qwen3-8B, Llama-3.1-8B, and GLM-
                                                                                               4-9B. In the identical closed loop, RefineCut-Evo
contributors unaffiliated with the authors (ledgers
                                                                                               outperforms two of its three teachers, ties the third,
drafted by an LLM, revised by two research as-
                                                                                               and stays well above prompting and inference-time
sistants, and checked by two video editors), the
                                                                                               search on the same backbone. Human briefs, ren-
ranking holds and Evo stays 0.054 ahead (0.902 vs.
                                                                                               dered previews, plan statistics, and sensitivity and
0.848; Appendix H).
                                                                                               fallback analyses corroborate these results beyond
Failure composition. Per task, Evo mostly con-                                                 one backbone, variant, or scoring configuration.
verts near-misses: OK plans rise from 74 to 91, and
duration mismatches, the dominant failure under                                                5   Conclusion
Mixed-Pref, fall from 16 to 1 (Figure 5; per-type                                              We treated video editing as a planning problem
counts in Table 18).                                                                           whose outputs can be checked, and built RefineCut
Plan statistics. The improvement is not bought                                                 around that property. An explicit constraint ledger
with more editing. Evo uses fewer patches per task                                             turns each brief into machine-checkable require-
(1.76 vs. 2.72 for the prompted baseline), fewer op-                                           ments, a typed timeline with RefinePatch opera-
erations (3.77 vs. 5.95), and similar output length                                            tions makes edits executable, and a deterministic
(67.5 vs. 69.1), and it never emits an invalid clip                                            verifier closes the loop. The same verifier then
reference or an over-rewrite (Table 21).                                                       does the training work: replaying every candidate
                                                                                               branch turns noisy multi-teacher traces into verified
LLM-judge agreement. Does an evaluator out-                                                    supervision, and RefineCut-Evo continues improv-
side our loop see the same ordering? A blind API                                               ing the planner on its own verified repairs with
judge points the same way as the verifier on 68–                                               high-margin DPO. On RefineCut-Bench this recipe
70% of tasks with a nonzero VES margin, and on                                                 lifts an 8B planner from 0.620 to 0.924 VES, the
every task the verifier marks as a degradation. Its                                            verified-over-raw gain carries over to Llama-3.1-
many ties sit almost entirely on the 73/100 tasks                                              8B and GLM-4-9B, and the final planner stands
whose terminal plans also tie under the verifier (Ap-                                          beside the frontier teachers it distilled from, inside
pendix G).                                                                                     the same closed loop. The broader lesson: when a
                                                                                               creative task admits an executable specification, a
Semantic dependence. If the planner ignored
                                                                                               deterministic verifier can stand in for human labels
the captions, editing them should not matter. It
                                                                                               or a learned judge as the primary training signal,
does not ignore them: removing all clip seman-
                                                                                               and a compact open model can then be trained to
tics costs 0.074 VES, and shuffling captions across
                                                                                               hold its own against much larger prompted systems.
clips costs 0.200, with required-clip recall collaps-
ing from 0.98 to 0.46. Deleting only the short cap-                                            Limitations
tion, whose content overlaps the structured fields,
changes nothing measurable (full deltas and CIs in                                             Planning-layer scope. RefineCut is deliberately
Appendix G).                                                                                   scoped to executable edit planning over a typed
                                                                                               timeline. The verifier checks structural require-
4.9   Blind Rendered-Preview Preference                                                        ments, from schema validity to ledger satisfaction
Do the planning gains survive rendering? Three                                                 and duration control; it cannot judge whether a cut
annotators per pair compared 150 blind, left–right                                             is tasteful or a story lands, which only the rendered-
preview study touches. Because the verifier also         provenance tracking, misuse detection, and over-
supplies training-time replay and closed-loop feed-      sight.
back, VES is an in-protocol measure rather than an
independent absolute quality score.                      Data Availability

Upstream perception. The planner reads up-               The code is available at https://github.
stream captions, motion metadata, and music meta-        com/Lancelot-wy/RefineCut and RefineCut-
data rather than raw pixels, so caption or beat-         Bench at https://huggingface.co/datasets/
tracking errors can bound edit-plan quality. Story-      Randallhy/RefineCut-Bench. The benchmark
board previews also mix planner effects with the         release contains the 3,578 canonical tasks with
rendering pipeline. Controlled removal and shuf-         briefs, constraint ledgers, clip-pool metadata and
fling of planner-visible semantic fields show that       captions, music metadata with beat tracks, all splits
the planner uses textual clip semantics, but do not      including Common-100, dev100, and the canonical-
establish robustness to errors from a real captioner,    clean subset, the canonicalized multi-teacher tra-
robustness across captioners, or raw-pixel percep-       jectories with per-branch verifier replay scores, and
tion; these remain future work.                          the JSON schemas for the constraint ledger, edit
                                                         plan, RefinePatch, timeline IR, and verifier output.
Generalization and future work. The current              The code release contains the deterministic verifier,
evidence covers three model families in the com-         RefinePatch canonicalization and the Apply/Verify
pact 8B–9B regime, three editing-task families, and      loop, the metric implementation, the PatchPlan-
one primary asset pool; the preference stages are        ner evaluation prompt, and the closed-loop evalu-
trained only on Qwen3-8B, and absolute transfer          ation harness used for all reported numbers. Raw
scores remain below it. RefineCut-Evo is an offline      video clips and music are referenced by their pub-
DPO stage rather than a full EvoLM reproduction          lic research-licensed source identifiers rather than
or online RL. Task briefs and constraint ledgers in      redistributed.
RefineCut-Bench are LLM-generated under con-
trolled templates, which keeps verifier-based eval-      Declaration of Generative AI Usage
uation reproducible; Human50 tests transfer to           During preparation, the authors used AI assistants
free-form human-written briefs, while larger-scale       for language polishing, LaTeX formatting, consis-
real-user specifications, additional asset domains,      tency checking, and coding assistance. AI tools did
model scales, longer-form editing, and final-video       not generate experimental results or automatically
evaluation remain future work.                           validate references. All claims, analyses, citations,
                                                         and final decisions were manually verified and ap-
Ethical Considerations                                   proved by the authors, who bear full responsibility
RefineCut studies planning-level editing rather than     for the manuscript.
unrestricted video generation, but executable edit
                                                         Acknowledgments
plans can connect to rendering or generation tools
and could be misused to create misleading edits,         This work is supported in part by the Guang-
omit context, or insert synthetic content without dis-   dong Basic and Applied Basic Research Founda-
closure. Our benchmark uses controlled tasks, ex-        tion under Grant No. 2025A1515012968, in part
plicit ledgers, and clip-level metadata; deployment      by the Shenzhen Science and Technology Pro-
on real media should respect copyright, consent,         gram under Grant No. JCYJ20240813113502004,
provenance, and disclosure requirements. Clips           in part by the National Natural Science Foun-
come from public research-licensed sources and           dation of China under Grant No. 62001412,
are not annotated with person identities; captions       in part by Shenzhen Stability Science Program
are short scene/action descriptions and do not con-      2023, in part by the Guangdong Provincial Key
tain personal names. The planner reads only cap-         Laboratory of Future Networks of Intelligence
tions and metadata, not raw pixels. The verifier         (Grant No. 2022B1212010001), and in part by
checks structural correctness, not factual accuracy,     the Shenzhen Key Lab of Crowd Intelligence
fairness, or social appropriateness, so we view Re-      Empowered Low-Carbon Energy Network (Grant
fineCut as a research framework for verifier-guided      No. ZDSYS20220606100601002).
planner training and encourage future work on
References                                                    Panwen Hu, Jin Jiang, Jianqi Chen, Mingfei Han,
                                                                Shengcai Liao, Xiaojun Chang, and Xiaodan Liang.
Manish Bhattarai, Ismael Boureima, Nishath Ra-                  2024. StoryAgent: Customized storytelling video
 jiv Ranasinghe, Scott Pakin, and Dan O’Malley.                 generation via multi-agent collaboration. Preprint,
 2026.    Rubric-grounded RL: Structured judge                  arXiv:2411.04925.
 rewards for generalizable reasoning. Preprint,
 arXiv:2605.08061.                                            Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang,
                                                                Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianx-
Paul C. Bryan and Mark Nottingham. 2013. JavaScript             ing Wu, Qingyang Jin, Nattapol Chanpaisit, Yao-
  Object Notation (JSON) patch. RFC 6902.                       hui Wang, Xinyuan Chen, Limin Wang, Dahua Lin,
Jiaxin Cheng, Tianjun Xiao, and Tong He. 2024. Con-             Yu Qiao, and Ziwei Liu. 2024. VBench: Compre-
   sistent video-to-video transfer using synthetic dataset.     hensive benchmark suite for video generative mod-
   In The Twelfth International Conference on Learning          els. In Proceedings of the IEEE/CVF Conference
   Representations.                                             on Computer Vision and Pattern Recognition, pages
                                                                21807–21818.
Paul F. Christiano, Jan Leike, Tom Brown, Miljan Mar-
  tic, Shane Legg, and Dario Amodei. 2017. Deep               Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun
  reinforcement learning from human preferences. In             Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin
  Advances in Neural Information Processing Systems,            Jiang, Qun Liu, and Wei Wang. 2024. Follow-
  volume 30.                                                    Bench: A multi-level fine-grained constraints fol-
                                                                lowing benchmark for large language models. In
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,                 Proceedings of the 62nd Annual Meeting of the As-
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias                sociation for Computational Linguistics (Volume 1:
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro               Long Papers), pages 4667–4688, Bangkok, Thailand.
  Nakano, and Christopher Hesse. 2021. Training                 Association for Computational Linguistics.
  verifiers to solve math word problems. Preprint,
  arXiv:2110.14168.                                           Carlos E. Jimenez, John Yang, Alexander Wettig,
                                                                Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
Abe Davis and Maneesh Agrawala. 2018. Visual                    Narasimhan. 2024. SWE-bench: Can language mod-
  rhythm and beat. ACM Transactions on Graphics,                els resolve real-world GitHub issues? In The Twelfth
  37(4).                                                        International Conference on Learning Representa-
                                                                tions.
DeepSeek-AI. 2026. DeepSeek-V4: Towards highly
  efficient million-token context intelligence. Techni-       Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo
  cal report and Hugging Face model card. Accessed              Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu,
  2026-05-26.                                                   Jianwei Zhang, and 1 others. 2024. HunyuanVideo:
                                                               A systematic framework for large video generative
Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff,                models. Preprint, arXiv:2412.03603.
  Dan Jurafsky, and Douwe Kiela. 2024. Model align-
  ment as prospect theoretic optimization. In Proceed-        Ranjay Krishna, Kenji Hata, Frederic Ren, Li Fei-Fei,
  ings of the 41st International Conference on Machine          and Juan Carlos Niebles. 2017. Dense-captioning
  Learning, volume 235 of Proceedings of Machine                events in videos. In Proceedings of the IEEE In-
  Learning Research, pages 12634–12651. PMLR.                   ternational Conference on Computer Vision, pages
                                                                706–715.
Mohammad Gheshlaghi Azar, Zhaohan Daniel Guo, Bi-
 lal Piot, Remi Munos, Mark Rowland, Michal Valko,            Max Ku, Cong Wei, Weiming Ren, Huan Yang, and
 and Daniele Calandriello. 2024. A general theoretical         Wenhu Chen. 2024. AnyV2V: A tuning-free frame-
 paradigm to understand learning from human pref-              work for any video-to-video editing tasks. Transac-
 erences. In Proceedings of The 27th International             tions on Machine Learning Research.
 Conference on Artificial Intelligence and Statistics,
 volume 238 of Proceedings of Machine Learning                Nathan Lambert, Jacob Morrison, Valentina Pyatkin,
 Research, pages 4447–4455. PMLR.                               Shengyi Huang, Hamish Ivison, Faeze Brahman,
                                                                Lester James V. Miranda, Alisa Liu, Nouha Dziri,
Jiwoo Hong, Noah Lee, and James Thorne. 2024.                   Shane Lyu, Yuling Gu, Saumya Malik, Victoria Graf,
   ORPO: Monolithic preference optimization without             Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras,
   reference model. In Proceedings of the 2024 Confer-          Oyvind Tafjord, Chris Wilhelm, Luca Soldaini, and
   ence on Empirical Methods in Natural Language Pro-           4 others. 2025. Tulu 3: Pushing frontiers in open
   cessing, pages 11170–11189, Miami, Florida, USA.             language model post-training. In The Second Confer-
   Association for Computational Linguistics.                   ence on Language Modeling.

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan             Ke Li, Maoliang Li, Jialiang Chen, Jiayu Chen, Zihao
  Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and               Zheng, Shaoqi Wang, and Xiang Chen. 2026a. DI-
  Weizhu Chen. 2022. LoRA: Low-rank adaptation of               RECT: Video mashup creation via hierarchical multi-
  large language models. In The Tenth International             agent planning and intent-guided editing. Preprint,
  Conference on Learning Representations.                       arXiv:2604.04875.
Shuyue Stella Li, Rui Xin, Teng Xiao, Yike Wang,             Training language models to follow instructions with
  Rulin Shao, Zoey Hao, Melanie Sclar, Sewoong Oh,           human feedback. In Advances in Neural Information
  Faeze Brahman, Pang Wei Koh, and Yulia Tsvetkov.           Processing Systems, volume 35, pages 27730–27744.
  2026b. EvoLM: Self-evolving language models
  through co-evolved discriminative rubrics. Preprint,     Adam Polyak, Amit Zohar, Andrew Brown, Andros
  arXiv:2605.03871.                                          Tjandra, Animesh Sinha, Ann Lee, Apoorv Vyas,
                                                             Bowen Shi, Chih-Yao Ma, Ching-Yao Chuang, and 1
Zhengyang Liang, Daoan Zhang, Huichi Zhou, Rui               others. 2024. Movie Gen: A cast of media foundation
  Huang, Bobo Li, Yuechen Zhang, Shengqiong Wu,              models. Preprint, arXiv:2410.13720.
  Xiaohan Wang, Jiebo Luo, Lizi Liao, and Hao Fei.
  2025. UniVA: Universal video agent towards open-         Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
  source next-generation video generalist. Preprint,         pher D. Manning, Stefano Ermon, and Chelsea Finn.
  arXiv:2511.08521.                                          2023. Direct preference optimization: Your language
                                                             model is secretly a reward model. In Advances in
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-         Neural Information Processing Systems, volume 36,
  son Edwards, Bowen Baker, Teddy Lee, Jan Leike,            pages 53728–53741.
  John Schulman, Ilya Sutskever, and Karl Cobbe.
  2024. Let’s verify step by step. In The Twelfth Inter-   Noah Shinn, Federico Cassano, Ashwin Gopinath,
  national Conference on Learning Representations.           Karthik R. Narasimhan, and Shunyu Yao. 2023. Re-
                                                             flexion: Language agents with verbal reinforcement
Zihao Lin, Haibo Wang, Zhiyang Xu, Siyao Dai, Huan-          learning. In Advances in Neural Information Pro-
  jie Dong, Xiaohan Wang, Yolo Y. Tang, Yixin Wang,          cessing Systems, volume 36.
  Qifan Wang, and Lifu Huang. 2026. GLANCE: A
  global-local coordination multi-agent framework for      Yifan Song, Weimin Xiong, Xiutian Zhao, Dawei Zhu,
  music-grounded non-linear video editing. Preprint,         Wenhao Wu, Ke Wang, Cheng Li, Wei Peng, and
  arXiv:2604.05076.                                          Sujian Li. 2024a. AgentBank: Towards generalized
                                                             LLM agents via fine-tuning on 50000+ interaction tra-
Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang,           jectories. In Findings of the Association for Computa-
  Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng,           tional Linguistics: EMNLP 2024, pages 2124–2141,
  Raymond Chan, and Ying Shan. 2024. EvalCrafter:            Miami, Florida, USA. Association for Computational
  Benchmarking and evaluating large video generation         Linguistics.
  models. In Proceedings of the IEEE/CVF Conference
  on Computer Vision and Pattern Recognition, pages        Yifan Song, Da Yin, Xiang Yue, Jie Huang, Sujian
  22139–22149.                                               Li, and Bill Yuchen Lin. 2024b. Trial and error:
                                                             Exploration-based trajectory optimization of LLM
Anamika Lochab, Bolian Li, and Ruqi Zhang.                   agents. In Proceedings of the 62nd Annual Meeting
  2026. Uniform-correct policy optimization: Break-          of the Association for Computational Linguistics (Vol-
  ing RLVR’s indifference to diversity. Preprint,            ume 1: Long Papers), pages 7584–7600, Bangkok,
  arXiv:2605.00365.                                          Thailand. Association for Computational Linguistics.
Fuchen Long, Zhaofan Qiu, Ting Yao, and Tao Mei.           Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel M.
  2024. VideoStudio: Generating consistent-content           Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
  and multi-scene videos. In Computer Vision – ECCV          Dario Amodei, and Paul F. Christiano. 2020. Learn-
  2024, pages 468–485. Springer.                             ing to summarize with human feedback. In Ad-
                                                             vances in Neural Information Processing Systems,
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler             volume 33, pages 3008–3021.
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,             Yijun Tian, Yikun Han, Xiusi Chen, Wei Wang, and
 Shashank Gupta, Bodhisattwa Prasad Majumder,                Nitesh V. Chawla. 2025. Beyond answers: Transfer-
 Katherine Hermann, Sean Welleck, Amir Yazdan-               ring reasoning capabilities to smaller LLMs using
 bakhsh, and Peter Clark. 2023. Self-refine: Itera-          multi-teacher knowledge distillation. In Proceedings
 tive refinement with self-feedback. In Advances in          of the Eighteenth ACM International Conference on
 Neural Information Processing Systems, volume 36,           Web Search and Data Mining, WSDM ’25, pages
 pages 46534–46594.                                          251–260. Association for Computing Machinery.
Yu Meng, Mengzhou Xia, and Danqi Chen. 2024.               Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie
  SimPO: Simple preference optimization with a               Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming
  reference-free reward. In Advances in Neural In-           Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang,
  formation Processing Systems, volume 37.                   Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan
                                                             Chen, Kai Zhu, Kang Zhao, Keyu Yan, and 43 others.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,            2025. Wan: Open and advanced large-scale video
  Carroll Wainwright, Pamela Mishkin, Chong Zhang,           generative models. Preprint, arXiv:2503.20314.
  Sandhini Agarwal, Katarina Slama, Alex Ray, John
  Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,      Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhi-
  Maddie Simens, Amanda Askell, Peter Welinder,              hao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin
  Paul Christiano, Jan Leike, and Ryan Lowe. 2022.           Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei
  Du, Xuancheng Ren, Rui Men, Dayiheng Liu,               Andy Zeng, Maria Attarian, Brian Ichter,
  Chang Zhou, Jingren Zhou, and Junyang Lin. 2024.          Krzysztof Marcin Choromanski, Adrian Wong,
  Qwen2-VL: Enhancing vision-language model’s per-          Stefan Welker, Federico Tombari, Aveek Purohit,
  ception of the world at any resolution. Preprint,         Michael S. Ryoo, Vikas Sindhwani, Johnny Lee, Vin-
  arXiv:2409.12191.                                         cent Vanhoucke, and Pete Florence. 2023. Socratic
                                                            models: Composing zero-shot multimodal reasoning
Renxi Wang, Xudong Han, Yixuan Zhang, Timothy               with language. In The Eleventh International
  Baldwin, and Haonan Li. 2025. NAT: Enhancing              Conference on Learning Representations.
  agent tuning with negative samples. In Proceedings
  of the 2025 Conference of the Nations of the Americas   Aohan Zeng, Mingdao Liu, Rui Lu, Bowen Wang, Xiao
  Chapter of the Association for Computational Lin-         Liu, Yuxiao Dong, and Jie Tang. 2024. AgentTun-
  guistics: Human Language Technologies (Volume 1:          ing: Enabling generalized agent abilities for LLMs.
  Long Papers), pages 7385–7398, Albuquerque, New           In Findings of the Association for Computational
  Mexico. Association for Computational Linguistics.        Linguistics: ACL 2024, pages 3053–3077, Bangkok,
                                                            Thailand. Association for Computational Linguistics.
Zhiheng Xi, Yiwen Ding, Wenxiang Chen, Boyang
  Hong, Honglin Guo, Junzhe Wang, Xin Guo, Ding-          Yehang Zhang, Xinli Xu, Xiaojie Xu, Doudou Zhang,
  wen Yang, Chenyang Liao, Wei He, Songyang                 Li Liu, and Ying-Cong Chen. 2025. Orchestrating
  Gao, Lu Chen, Rui Zheng, Yicheng Zou, Tao Gui,            audio: Multi-agent framework for long-video audio
  Qi Zhang, Xipeng Qiu, Xuanjing Huang, Zuxuan              synthesis. In Proceedings of the 2025 Conference on
  Wu, and Yu-Gang Jiang. 2025. AgentGym: Evaluat-           Empirical Methods in Natural Language Processing,
  ing and training large language model-based agents        pages 22267–22282, Suzhou, China. Association for
  across diverse environments. In Proceedings of the        Computational Linguistics.
  63rd Annual Meeting of the Association for Compu-
  tational Linguistics (Volume 1: Long Papers), pages     Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  27914–27961, Vienna, Austria. Association for Com-        Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  putational Linguistics.                                   Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
                                                            Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
Weimin Xiong, Yifan Song, Xiutian Zhao, Wenhao Wu,          LLM-as-a-judge with MT-Bench and chatbot arena.
 Xun Wang, Ke Wang, Cheng Li, Wei Peng, and                 In Advances in Neural Information Processing Sys-
  Sujian Li. 2024. Watch every step! LLM agent              tems, volume 36, pages 46595–46623.
  learning via iterative step-level process refinement.
  In Proceedings of the 2024 Conference on Empiri-        Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha
  cal Methods in Natural Language Processing, pages          Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and
 1556–1572, Miami, Florida, USA. Association for             Le Hou. 2023. Instruction-following evaluation for
  Computational Linguistics.                                 large language models. Preprint, arXiv:2311.07911.
Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding,         Sidan Zhu, Yutong Wang, Hongteng Xu, and Dixin
  Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi            Luo. 2025. Weakly-supervised movie trailer genera-
  Hong, Xiaohan Zhang, Guanyu Feng, Da Yin, Yux-            tion driven by multi-modal semantic consistency. In
  uan Zhang, Weihan Wang, Yean Cheng, Bin Xu,               Proceedings of the Thirty-Fourth International Joint
  Xiaotao Gu, Yuxiao Dong, and Jie Tang. 2025.              Conference on Artificial Intelligence, pages 10234–
  CogVideoX: Text-to-video diffusion models with an         10242.
  expert transformer. In The Thirteenth International
  Conference on Learning Representations.                 Shaobin Zhuang, Kunchang Li, Xinyuan Chen, Yaohui
                                                            Wang, Ziwei Liu, Yu Qiao, and Yali Wang. 2024.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak            Vlogger: Make your dream a vlog. In Proceedings of
  Shafran, Karthik Narasimhan, and Yuan Cao. 2023.          the IEEE/CVF Conference on Computer Vision and
  ReAct: Synergizing reasoning and acting in language       Pattern Recognition, pages 8806–8817.
  models. In The Eleventh International Conference
  on Learning Representations.
Jaehong Yoon, Shoubin Yu, and Mohit Bansal. 2025.
   RACCooN: Versatile instructional video editing with
   auto-generated narratives. In Proceedings of the
  2025 Conference on Empirical Methods in Natural
  Language Processing, pages 27972–28008, Suzhou,
   China. Association for Computational Linguistics.
Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho,
 Xian Li, Sainbayar Sukhbaatar, Jing Xu, and Jason E.
 Weston. 2024. Self-rewarding language models. In
 Proceedings of the 41st International Conference on
 Machine Learning, volume 235 of Proceedings of
 Machine Learning Research, pages 57905–57923.
  PMLR.
A     Related Work                                      feedback use without necessarily updating model
                                                        weights. Training-oriented systems instead use in-
A.1    AI-Assisted Video Editing and
                                                        teraction or tool-use trajectories to improve agent
       Generation
                                                        behavior: AgentTuning (Zeng et al., 2024) fine-
A first line of work focuses on creating or modi-       tunes on tool-use traces, AgentBank (Song et al.,
fying visual content. Text-to-video and image-to-       2024a) scales trajectory fine-tuning across diverse
video models generate clips de novo (Zhuang et al.,     agent skills, and AgentGym (Xi et al., 2025)
2024; Long et al., 2024; Yang et al., 2025; Kong        evolves agents across environments from collected
et al., 2024; Wan et al., 2025; Polyak et al., 2024),   trajectories. Trajectory feedback can also be turned
and instruction-based editing models change ap-         into a preference signal: ETO (Song et al., 2024b)
pearance or style within a fixed shot or short se-      pairs successful and failed trajectories for Direct
quence (Cheng et al., 2024; Ku et al., 2024; Yoon       Preference Optimization (DPO) (Rafailov et al.,
et al., 2025). Trailer, montage, and mashup sys-        2023), IPR (Xiong et al., 2024) estimates step-level
tems (Li et al., 2026a; Lin et al., 2026; Zhu et al.,   rewards by Monte-Carlo sampling along expert
2025) assemble cuts from a footage library accord-      trajectories, and negative-aware training (Wang
ing to a script or theme, and UniVA (Liang et al.,      et al., 2025) incorporates failed trajectories dur-
2025) packages generation, editing, and segmenta-       ing fine-tuning. RefineCut belongs to this broader
tion under one tool-calling loop. These systems can     executable-agent line, but differs by using determin-
produce or rearrange content. However, they do          istic replay of typed video-editing patches (Bryan
not train a reusable open-weight planner: a planner     and Nottingham, 2013) to construct both super-
that learns editing decisions over a real clip pool     vised fine-tuning (SFT) targets and preference
from a constraint ledger and an editable timeline.      pairs.

A.2 Workflow Decomposition for Multimodal               A.4   Rubric-Guided and Verifier-Guided
    Creation                                                  Self-Improvement
Hierarchical multi-agent systems break complex          Recent work explores rubric-structured self-
creation into staged professional roles. DIRECT         improvement of language models. EvoLM (Li
(Li et al., 2026a) decomposes mashup creation into      et al., 2026b) uses a co-trained rubric model to
Screenwriter, Director, and Editor agents under a hi-   score self-generated candidates and drive student
erarchical multimodal coherency objective. LVAS-        improvement. Rubric-Grounded RL (Bhattarai
Agent (Zhang et al., 2025) mirrors a long-video         et al., 2026) applies multi-criterion weighted re-
dubbing studio with Storyboarder, Scriptwriter, De-     wards, and UCPO-style diversity penalties (Lochab
signer, and Generator. StoryAgent (Hu et al., 2024)     et al., 2026) target collapse in multiple-correct set-
takes a similar role-based view of storytelling video   tings. RefineCut adapts this idea to executable
production. These systems share two properties:         video-editing planning. The student samples can-
the planning logic is built from prompted frontier      didate repairs at training states, each candidate is
backbones, and the editing decision flow is encoded     scored by the deterministic verifier together with a
in the prompt scaffolding rather than learned. Re-      task-specific editing rubric, and high-margin pairs
fineCut keeps the workflow-decomposition view           train the planner with DPO: EvoLM’s co-trained
but inverts the operating mode. We collect trajec-      rubric model is replaced by a deterministic verifier
tories from such workflows, replay them through         plus a fixed task rubric, and UCPO-lite appears
a deterministic verifier, and train an open-weight      only as a negative diagnostic in the ablation.
planner that internalizes the editing decision flow.
                                                        Preference-optimization objectives. RefineCut
A.3    Tool-Executable Planners from                    uses DPO because verifier replay and Evo can-
       Trajectories                                     didate scoring naturally yield paired chosen/re-
A complementary line of work studies agents             jected repairs.       Recent alternatives such as
that reason, act, or revise through tool-like tra-      IPO (Gheshlaghi Azar et al., 2024), KTO (Etha-
jectories. Prompt-time and self-correction meth-        yarajh et al., 2024), ORPO (Hong et al., 2024), and
ods such as ReAct (Yao et al., 2023), Self-             SimPO (Meng et al., 2024) modify the preference
Refine (Madaan et al., 2023), and Reflexion (Shinn      objective, reduce reference-model dependence, or
et al., 2023) demonstrate iterative reasoning or        use unary/desirable–undesirable signals. These ob-
Item                                                   Value     B.2       Frame Sampling and Captioning
Raw video clips                                         7,971
Extracted caption frames                               23,913
Music tracks                                              499
                                                                 We use an adaptive frame sampler (“v2”) that es-
Raw task records                                       3,960
                                                                 timates motion intensity from optical-flow magni-
Canonical unique tasks                                 3,578     tude on a coarse temporal grid and then samples
Train / Dev / Test (records)                2,773 / 596 / 591
Test canonical-clean                                518 / 591    3, 5, or 7 frames per clip for low / medium / high
Removed by canonical overlap                   73 (12.35%)       motion. The motion bucket is also stored in the
Common-100 ∩ canon.-clean                                  92
Task-level record overlap                            0/0/0       motion_intensity field of the caption row, so
Raw teacher rollouts                     2,000 / 1,962 / 1,962   that downstream task generation can use it as a
Replayed teacher rollouts                2,000 / 1,946 / 1,959
Raw canonical triple intersection                          381
                                                                 metadata signal.
Replayed canonical triple intersection                     375
Canonical teacher union                                  3,578
                                                                   The captioning module is an upstream compo-
                                                                 nent: the planner does not read pixels and only
Table 6: Dataset, splits, and teacher coverage. Teacher          sees the caption fields. The captioner varies across
counts are GPT-5.4 / Qwen3-Max / DeepSeek-V4-Pro.                rows; each row’s exact configuration is recorded in
                                                                 model_used and released with the dataset.
jectives are orthogonal to our central contribution:
deterministic verifier replay creates the supervision
source. We therefore use DPO as a standard paired-               B.3       Task Generation
preference optimizer and leave objective swaps to
future work.                                                     Tasks are generated by an LLM conditioned on a
                                                                 sampled clip pool, the family and subtype slot in
B       RefineCut-Bench Construction Details                     Table 8, and a family-conditioned ledger template.
                                                                 The generated record separates task identity, the
This appendix lists the construction steps required              natural-language brief, planner inputs, and subtype-
to reproduce RefineCut-Bench: asset collection,                  specific structure.
captioning, task generation, ledger design, clip-
pool sampling, teacher trajectory collection, and
                                                                 Record group Fields
the canonical-id split. The main benchmark
                                                                 Identity         task_id, task_type, task_subtype
overview appears in Figure 2.                                    Brief            brief, target_duration
                                                                 Planner inputs   clip_pool, constraint_ledger
                                                                 Structure        structure, subtype_constraints
B.1      Asset Pool and Caption Sources
                                                                 Task-record schema. The appendix names implementation fields here; the
The asset pool contains 7,971 captioned clips                    surrounding text uses plain-language descriptions.
drawn from five public sources (Table 7). Each row
in the clip caption table carries the fields clip_id,
source, duration, subject, action, scene,                        Family                         Subtypes

camera, scene_category, motion_intensity,                        A (multi-clip                  themed_montage, pacing_progression,
                                                                 composition)                   motion_dynamics_montage, scene_traversal,
caption_short, model_used, and ts.               The                                            character_focus, abstract_rhythm
model_used field records which caption model                     B (local                       b_roll_insert, clip_swap, cut_extend,
                                                                 edit/repair)                   transition_repair
emitted each row, so captioner provenance is
tracked per clip rather than assumed globally;                   C (generative                  generated_opener, generated_bridge,
                                                                 composition)                   generated_text_overlay,
the supplementary artifact records the exact                                                    generated_replacement,
                                                                                                generated_full_assembly
model_used distribution.
                                                                     Table 8: The 15 task subtypes grouped by family.
Source                                   Captioned clips
panda70m_sample                                       3,990
pexels                                                3,219
pixabay                                                 255      B.4       Constraint Ledger Design
openvid                                                 100
long_video_segment                                      407
                                                                 The constraint ledger is the explicit specification
Total                                                 7,971
                                                                 of what a successful cut has to satisfy. To keep the
Table 7: Captioned clip counts per source. The total             appendix readable, we group the 14 fine-grained
matches the asset count reported in Section 2.4.                 ledger types by the editing requirement they ex-
                                                                 press.
Requirement Ledger types                                                   repair_operator                Intent
Duration       target_duration, duration_tolerance
Transition     transition_style
                                                                           modify_prompt                  rewrite the generative prompt
Music sync     music_sync_bpm, music_sync_beat                             change_tool                    switch the downstream tool slot
Clip inclusion must_keep_clip, must_open_with                              adjust_parameter               tweak a numeric or enum field
               tag_inclusion                                               reselect_clip                  replace a clip in the sequence
Clip exclusion must_exclude_clip, must_close_with
               tag_exclusion                                               retry_with_fallback            redo with a safer default
Repeat limit   no_repeat_within_seconds                                    abort_and_skip                 drop the step
               max_repeats_per_clip
Pacing         pacing                                                             Table 9: The six repair_operator values.
Ledger type groups. Fine-grained types are shown as implementation field
names; the main text uses the broader requirement names.
                                                                           B.7     Splits and Canonical IDs
   Every ledger ships with at least four items, and
                                                                           Raw task records are deduplicated to canonical
every ledger includes a target_duration item.
                                                                           task ids by collapsing minor surface variants (re-
The seven field-level constraint families mentioned
                                                                           sampled clip_pools of the same underlying task)
in Section 2.2 (duration, transition, music syn-
                                                                           into a single canonical id. We then split at the
chronization, clip inclusion, clip exclusion, repeat
                                                                           record level into train / dev / test of 2,773/596/591.
limit, and pacing) group these field-level checks;
                                                                           Of the 591 test records, 518 carry a canonical id
generated-placeholder requirements are checked
                                                                           that does not appear in the train set (canonical-
separately as task-structure constraints. Per-type
                                                                           clean); the remaining 73 records overlap by canon-
counts on the 3,578 canonical task universe are
                                                                           ical id with train. The intersection of canonical-
shown in Figure 2 (C); the full numeric table is
                                                                           clean with the Common-100 evaluation subset is
released with the dataset.
                                                                           N = 92 records and is used for the robustness
                                                                           check in Section 4.8.
B.5      Clip-Pool Sampling
                                                                           B.8     Licensing and Intended Use
The clip_pool of a task is sampled from the cap-
tioned asset pool under the following rules.                               All clip sources in Table 7 are publicly available
   (i) The planner may only choose clips from the                          and permit research use; the music tracks and a
given clip_pool; references to a clip_id outside                           subset of in-house clips are private assets used
the pool are flagged as invalid by the verifier.                           for research only. We use every source within
   (ii) When the candidate pool (given_pool) con-                          its stated terms and solely for non-commercial re-
tains at least 30 clips, the sampled clip_pool size                        search. RefineCut-Bench (task records, ledgers,
is between 30 and 60; otherwise the entire candi-                          captioned-clip and music metadata, multi-teacher
date pool is used.                                                         trajectories) and the training/inference code will
                                                                           be released under CC BY-NC 4.0 upon acceptance.
   (iii) The ledger is generated jointly with the
                                                                           Derived artifacts inherit the research-only restric-
clip_pool so that every must_keep_clip and
                                                                           tion of their underlying sources and should not be
must_exclude_clip item refers to a clip that ex-
                                                                           used outside research contexts.
ists in the pool.
                                                                           C      Schemas and Interfaces
B.6      Teacher Trajectory Generation
                                                                           This appendix gives compact schemas for the five
For the teacher-covered subset of canonical tasks                          interfaces that appear throughout the paper. Full
we collect a teacher trajectory from each available                        JSON Schemas and longer worked examples are in
frontier API teacher (GPT-5.4, Qwen3-Max, and                              the supplementary release.
DeepSeek-V4-Pro); coverage is partial, and the
per-teacher replayed counts and canonical triple                            RefinePatch – a planner step
intersection are reported in Table 6. At every re-                          {
                                                                                "operations": [
fine step a teacher must emit exactly four candi-                                  {"op": "replace",
                                                                                    "path": "/args/selected_sequence",
date branches; each branch is a RefinePatch that                                    "value": ["C003","C001","C007","C012"]},
carries: a list of operations (RFC 6902 add / re-                                  {"op": "replace",
                                                                                    "path": "/args/segment_durations",
move / replace), a rationale_against_ledger                                         "value": [2.0, 3.5, 4.0, 3.5]}
                                                                                ],
naming the ledger items it tries to repair, a                                   "rationale_against_ledger":
repair_operator label from the fixed vocabulary,                                   ["target_duration#0", "must_keep_clip#2"],
                                                                                "repair_operator": "reselect_clip",
a free-text thought, and a numeric confidence.
     "affected_clips": ["C001","C007","C012"],             quence (denominator rules in Appendix J). VALID -
     "thought": "Swap C005 -> C007 to keep duration.",
     "confidence": 0.71                                    C LIP P RECISION: fraction of clip references in the
 }                                                         terminal sequence that lie inside the pool. D URA -
                                                           TION PASS @2 S (Dur): ⊮[|D UR final − D UR target | ≤
 EditPlan / Timeline IR – closed-loop terminal             2]. N O R EGRESSIONA LL S TEPS: no previously sat-
 artifact
                                                           isfied ledger item becomes unsatisfied at any step.
 {
     "selected_sequence": ["C003","C001","C007","C012"],   C ONVERGED @3 (Cvg): ⊮[F INAL CSR ≥ 0.8]
     "segment_durations": [2.0, 3.5, 4.0, 3.5],            within T =3 closed-loop steps (operational rule in
     "transitions": ["cut","cross_dissolve","cut"],
     "music_sync": {"bpm": 96, "beat_offset_ms": 120},     Appendix J).
     "placeholders": [],
     "renderer_hints": {"target_fps": 30}
 }                                                         VES summary.        VES is a fixed weighted sum:
                                                                VES = 0.30 FinalCSR
 ConstraintLedger entry – one row
                                                                      + 0.15 HardPass + 0.15 PASR
 {
     "item_id": "target_duration#0",
                                                                      + 0.15 FinalReqClipRecall
     "type": "target_duration",                                       + 0.10 DurationPass
     "spec": {"value_sec": 13.0, "tolerance_sec": 2.0},
     "satisfied": false,                                              + 0.10 TimelineValidity
     "evidence": {"current_sec": 15.4}
 }                                                                    + 0.05 NoRegression.
                                                           Branch-score signals. The replay score of a sin-
 VerifierOutput – one verifier call
                                                           gle candidate branch combines six signals. ∆CSR
 {                                                         is the increase in the per-entry ledger pass rate
     "schema_ok": true, "patch_apply_ok": true,
     "timeline_valid": true,                               between the pre-patch state st and the post-patch
     "delta_csr": 0.20,
     "targeted_repair": true,                              state st+1 . TARGETED R EPAIR, R EQ C LIP R ECALL,
     "no_regression": true,                                PASR, and N O R EGRESSION are the per-branch
     "req_clip_recall": 1.0,
     "locality": 1.0,                                      counterparts of the planning-quality metrics above,
     "score": 0.72
 }                                                         evaluated for one applied branch rather than the
                                                           terminal state. L OCALITY is the fraction of patch
 RubricScore – Evo rubric weighted aggregate               operations that edit only fields tied to the ledger
 ER1–ER7 (illustrative per-task instance)                  items named in rationale_against_ledger; it
 {                                                         penalizes patches that modify state unrelated to the
     "ER1": 0.50, "ER2": 1.00, "ER3": 0.75,
     "ER4": 0.50, "ER5": 1.00, "ER6": 0.50, "ER7": 1.00,   items being repaired.
     "weights":
       {"ER1":0.10,"ER2":0.25,"ER3":0.20,                  Branch score weights. The replay branch score
        "ER4":0.10,"ER5":0.15,"ER6":0.05,"ER7":0.15},
     "total": 0.825,                                       uses the six signals named in the method section:
     "fallback_used": ["ER1", "ER3_judge"]
 }                                                               V (b; st , Lt ) = w1 ∆CSR
                                                                                  + w2 TargetedRepair
D      Metric Definitions
                                                                                  + w3 ReqClipRecall
                                                                                                             (4)
Execution Gate. SCR (schema-conformance                                           + w4 PASR
rate): output parses against the RefinePatch JSON
                                                                                  + w5 NoRegression
schema. PASR (patch-apply success rate): canoni-
calized patch applies cleanly to st . T IMELINE VA -                              + w6 Locality.
LIDITY: the resulting state serializes to a Timeline       It uses fixed weights (w1 , w2 , w3 , w4 , w5 , w6 ) =
IR that the renderer parser accepts.                       (0.35, 0.20, 0.20, 0.10, 0.10, 0.05) applied in order
                                                           to ∆CSR, TARGETED R EPAIR, R EQ C LIP R ECALL,
Planning Quality. F INAL CSR (FCSR; termi-
                                                           PASR, N O R EGRESSION, and L OCALITY.
nal constraint-satisfaction rate): terminal mean
per-entry pass rate over the ledger. H ARD PASS            Sensitivity analyses. Table 10 summarizes sen-
(Hard): ⊮[F INAL CSR=1]. TARGETED R EPAIR:                 sitivity to the loop budget T , the candidate count
fraction of ledger items named in the patch’s              K, the mix weight λ, and the VES weights. The
rationale_against_ledger that are satisfied af-            T and K analyses are post-hoc over the archived
ter Apply. F INAL R EQ C LIP R ECALL (ReqCR): re-          trajectories and candidate pools, not new inference
call over the required clip ids on the terminal se-        or training.
Dimension       Setting               Result                        differ only in the pair-scoring function and the mar-
Loop budget T   1/2/3 (truncation)
                                      Evo VES 0.677/0.908/0.924;    gin filter (Table 3). Hyperparameters and elapsed
                                      first at every prefix
                                      Kendall τ -b ≥ 0.973;
                                                                    wall-clock times are matched across variants.
Mix weight λ    0.5/0.8/1.0
                                      0/779 pair flips

Candidates K    2/3 from K=4 pool
                                      top-1 retention 0.500/0.750   Compute budget and cost. All training ran on
                                      (sampling coverage)
                14 weights ±50%;      Evo first, above Mixed-Pref   a single NVIDIA A100 GPU. The core pipeline
VES weights
                20,000 reweightings   in 100% of settings
                                                                    consumed approximately 14.5 GPU-hours: Veri-
Table 10: Sensitivity of the main ranking. The T and                fied SFT (1,200 steps, ∼7.5 h), Mixed-Pref pref-
K rows are post-hoc analyses over archived trajectories             erence fine-tuning (800 steps, ∼2.1 h), and the
and candidate pools.                                                RefineCut-Evo Rubric-margin DPO run (600 steps,
                                                                    ∼4.9 h; the step-300 checkpoint is selected by dev
E     Training Details                                              VES). Including the Raw SFT ablation, the total
                                                                    is 23.5 GPU-hours; the three step-300 DPO abla-
Backbone and LoRA. All planners in the                              tions (Verifier-only, No-margin, UCPO-lite) each
primary progression initialize from Qwen3-8B-                       add ∼2.5 matched wall-clock hours, and generat-
Instruct with LoRA (Hu et al., 2022): rank r=32,                    ing the 6,000 Evo candidates took 3.98 h locally
α=64, applied to the q/k/v/o and gate/up/down                       with no API calls. Multi-teacher trajectory col-
projections. The cross-backbone transfer runs (Sec-                 lection used 13,804 frontier API calls to GPT-5.4,
tion 4.7) reuse the identical adapter configuration                 Qwen3-Max, and DeepSeek-V4-Pro (Section 2.5),
on Llama-3.1-8B-Instruct and GLM-4-9B. Adapter                      archiving 39.2M output characters (≈10–11M out-
checksums are released with the training artifacts.                 put tokens); input volume, estimated from per-call
                                                                    payloads (mean 11.1k characters), is ≈46–92M to-
Raw SFT. Examples 9,690 (teacher first-choice
                                                                    kens, and the total spend was approximately CNY
branches without verifier filtering). Max steps 800;
                                                                    2,000–3,000 (≈$280–420). Call counts and output
other hyperparameters follow Verified SFT.
                                                                    volume are exact archival values; input tokens and
Verified SFT. Examples 3,317 (one verifier-best                     monetary cost are estimates from payload sizes and
target per replayed step that passes the verified-SFT               author accounting records. At inference, RefineCut-
filter; Section 3.4). Max steps 1,200. Learning rate                Evo runs locally at 11.7 s/task, while teacher and
5e−5. Per-device batch 2 with gradient accumula-                    frontier APIs range 6.7–36.9 s/task; per-task to-
tion 8. Loss is standard next-token cross-entropy                   ken usage and latency are released with the arti-
on the canonicalized patch.                                         facts. No model training was performed through
                                                                    the APIs.
Traj-Pref DPO. Examples 357 trajectory-level
pairs. Max steps 400; other hyperparameters follow                  Decoding. All closed-loop evaluations use R=1
Mixed-Pref. Initialized from Verified.                              greedy decoding at generation time (a single sam-
                                                                    ple per step). R is the inference-time sampling/r-
Mixed-Pref DPO. Examples 2,380 chosen / re-                         eranking pool size and is distinct from the training-
jected pairs, mixing step-level and trajectory-level                time student-candidate count K=4 (Section 3.5).
signals. Max steps 800. Learning rate 2e−6.                         R=4 verifier reranking over the untrained back-
β = 0.1. Initialized from Verified.                                 bone is evaluated as a search control under the
                                                                    frozen protocol (Table 5; Appendix G, Table 15).
RefineCut-Evo DPO. Candidate generation:
K = 4 candidates per training state, on 1,500                       F   RefineCut-Evo Details
training states. Pair construction: 779 rubric-
margin pairs oversampled to 1,651 training rows                     Verifier replay procedure. Algorithm 1 formal-
(Appendix F). Max steps 600 with an intermedi-                      izes the verifier replay and branch-arbitration proce-
ate checkpoint at step 300. Learning rate 1e−6.                     dure used by the Stage 1 distillation (Section 3.3).
β = 0.05. Initialized from Mixed-Pref. Step 300
is selected on dev100 VES (Table 16).                               Rubric construction. For each canonical task we
                                                                    construct a task-specific editing rubric with seven
Ablation variants. Verifier-only, No-margin,                        criteria ER1–ER7 (Section 3.5). The criteria and
and UCPO-lite share the same backbone, candi-                       their average weights across the train set are listed
date pool, and DPO recipe as Rubric-margin; they                    in Table 11. Weights are computed per task-family
Algorithm 1 Verifier replay and branch arbitration.            6,000/6,000 candidates. Because the K=4 candi-
Require: task x, initial state s0 , teacher trajectory τ =     dates of a state receive the same constant, it cancels
    (step1 , . . . , stepT )                                   in every within-state score difference, so the fall-
Ensure: replayed trajectory with per-branch scores
 1: s ← s0 ; L ← I NIT L EDGER(x, s0 )                         back shifts absolute rubric values without affecting
 2: for t = 1, . . . , T do                                    candidate selection, margins, or preference-pair
 3:     Rt ← ∅                                                 construction; a counterfactual rescoring with both
 4:     for each candidate branch bkt in stept do
 5:           pkt ← C ANONICALIZE(bkt )                        channels zeroed reproduces every ranking and ev-
 6:           if not VALID(pkt , s) then                       ery training pair.
 7:                 rtk ← I NVALID; continue
 8:           end if                                           Pair construction. 779 chosen / rejected pairs
 9:           s′ ← A PPLY(s, pkt )                             are kept after applying a fixed margin threshold.
10:           L′ ← R ECOMPUTE(x, s′ )
11:           rtk ← S CORE(s, s′ , L, L′ )           ▷ Eq. 4   Mean margin 0.18; median margin 0.19; hard-
12:           Rt ← Rt ∪ {(pkt , rtk )}                         negative rate 0.987. The training set is oversam-
13:     end for                                                pled to 1,651 rows. The number of training states
14:     b∗t ← arg maxk rtk
15:     s ← A PPLY(s, p∗t )                                    skipped because the highest-scoring valid repair
16:     L ← R ECOMPUTE(x, s)                                   and the lower-scoring hard negative fell inside the
17: end for                                                    margin band is 635.
18: return replayed trajectory with {Rt , b∗t }Tt=1
                                                               Ablation caveats. Under the matched ablation
from a template that puts mass on the criteria most            (Table 3), verifier-only DPO reaches 0.909 VES
relevant to the family.                                        against 0.924 for the full method: the main signal
                                                               is verifier-scored student self-improvement, while
ID       Criterion                             Avg. weight
                                                               rubric-structured deterministic scoring adds 0.015
ER1      Intent and Story Alignment                0.09
                                                               and improves margin construction and interpretabil-
ER2      Ledger Satisfaction                       0.25
ER3      Clip Grounding and Relevance              0.22        ity. Temporal contrast was not trained: the data
ER4      Timeline and Segment Coherence            0.11        summary records 0 temporal-contrast pairs.
ER5      Duration and Pacing Alignment             0.15
ER6      Music / Beat Alignment                    0.05
ER7      Edit Economy / Minimality                 0.11
                                                               G         Additional Results

Table 11: Average rubric weights across the train set          Teacher replay diagnostics (RQ2).
(rounded; per-task weights sum to 1). Family A puts            Teacher           N Branches FCSR Hard PASR ReqCR NoReg          Dur VES
more mass on ER4; families B and C put more mass on            GPT-5.4         2,000   6,000 0.379 0.015 0.872   0.698   1.000 0.202 0.521
ER3.                                                           Qwen3-Max       1,946   3,892 0.446 0.016 0.989   0.712   1.000 0.157 0.557
                                                               DeepSeek-V4-Pro 1,959   3,920 0.473 0.028 0.946   0.703   1.000 0.156 0.559


                                                               Table 12: Extended teacher replay diagnostics. Ex-
Candidate generation. States with sampled can-                 pands Table 2 with NoRegression and Dur@2s. This
didates: 1,500. Total candidates: 6,000 (K=4 per               diagnoses the teacher trajectory resource used for dis-
state). JSON parse success 0.9968; patch-apply                 tillation (Section 4.4), not student closed-loop perfor-
success 0.9960.                                                mance; same-loop teacher policies are in Table 14.

Rubric scoring. Mean rubric score 0.67 (std                    Cross-backbone transfer (RQ5a). The transfer
0.13). The candidate pool shows a high verifier                runs repeat the Prompted / Raw / Verified compari-
/ rubric correlation ρ = 0.94, which indicates that            son on Llama-3.1-8B-Instruct and GLM-4-9B with
the rubric mostly tracks the verifier signal on these          the same training data, hyperparameters, and frozen
states. The joint score used for pair construction             closed-loop protocol. We fixed the success criterion
is S(c) = 0.65V (c) + 0.35R(c), making the self-               (Verified−Raw ≥ +0.10 VES with same-direction
improvement stage verifier-centered while retain-              HardPass) before running, and first checked that
ing rubric-structured margins. Criterion ER1 (in-              each backbone emits parseable, applicable step-1
tent) and the judge-side component of ER3 (clip                patches (≥ 7/10; Llama 8/10, GLM 10/10). Ta-
relevance, judge-side) fall back to deterministic              ble 13 reports the outcome: the Verified−Raw gain
proxies when external judge features are unavail-              is significantly positive on all three families and ex-
able; the fallback_used flag is recorded for ev-               ceeds +0.10 on two; the GLM gain is smaller but
ery one of the 6,000 candidates. In this run, both             significant. Unfiltered imitation is flat or harmful
channels used the constant neutral value 0.5 on                (Raw−Prompted +0.026, −0.070, −0.035); on
GLM the raw data also lowers patch-apply suc-                                          Qwen3-8B condition                            VES              Hard                Cvg

cess from 0.95 to 0.75. Required-clip recall rises                                     Direct prompting (T =1)                      0.502               0.07              0.08
                                                                                       + verifier feedback (T ≤3)                   0.592               0.15              0.21
from 0.72/0.39/0.77 to 0.98/0.92/0.99.                                                 Sampling R=1                                 0.646               0.23              0.30
                                                                                       R=4 verifier reranking                       0.700               0.32              0.42
Backbone         Prompt.       Raw     Verif.     ∆V−R [95% CI]                   p    Visited-pool oracle                          0.712               0.32              0.40
Qwen3-8B            0.594     0.620    0.858      +0.238                         –     RefineCut-Evo                                0.924               0.82              0.95
Llama-3.1-8B        0.566     0.496    0.649      +0.153 [0.109, 0.197]     3.6e−8
GLM-4-9B            0.643     0.607    0.686      +0.079 [0.036, 0.120]     9.0e−4     Table 15: Prompting and search ladder over the un-
Table 13: Cross-backbone transfer of verifier-                                         trained backbone, including the R=1 sampling row
replayed SFT. Same data, recipe, and frozen protocol;                                  omitted from Table 5.
paired statistics on Common-100. The Qwen3-8B row
                                                                                       dev100 checkpoint selection.
is the primary progression of Table 1.
                                                                                                Model               FCSR       Hard         Dur      Cvg        VES
Same-loop teacher and frontier policies (RQ5b).                                                 Verified            0.473      0.240        0.360    0.260      0.496
Each teacher runs as an online policy in the identi-                                            Mixed-Pref          0.534      0.260        0.400    0.310      0.543
                                                                                                Evo step300         0.608      0.450        0.570    0.470      0.604
cal closed loop: the same task records, typed state,                                            Evo step600         0.590      0.440        0.570    0.470      0.587
ledger, RefinePatch schema, parser, Apply/Verify,
                                                                                       Table 16: dev100 checkpoint selection for RefineCut-
feedback, T =3 budget, and CSR≥0.8 stopping
                                                                                       Evo. Step-300 is selected by dev VES; step-600 shows
rule, with no weight updates. Table 14 reports                                         mild over-optimization.
final scores, latency, and paired differences against
RefineCut-Evo. Newer-generation frontier poli-                                         Paired significance.
cies under the same contract score 0.940 (gpt-5.4-                                     Subset                 vs.           ∆VES            95% CI           W/T/L        p

mini), 0.943 (Qwen3.5-397B), 0.936 (its workflow-                                      Common-100        Mixed-Pref         +0.059     [0.028, 0.092]      22/73/5      0.0015
                                                                                       Common-100         Verified          +0.066     [0.036, 0.096]      24/71/5      0.0005
reflection variant), and 0.933 (deepseek-v4-flash).                                    Common-100         Traj-Pref         +0.060     [0.029, 0.091]      22/73/5      0.0015

Existing workflow video-editing agents assume                                          Canonical-clean   Mixed-Pref         +0.058     [0.027, 0.090]      21/66/5      0.0025
                                                                                       Canonical-clean    Verified          +0.068     [0.036, 0.100]      23/64/5      0.0009
tool interfaces different from our typed timeline,                                     Canonical-clean    Traj-Pref         +0.059     [0.028, 0.091]      21/66/5      0.0025

ledger, and RefinePatch loop and cannot be run in
                                                                                       Table 17: Paired significance for RefineCut-Evo.
it directly, so the workflow-reflection variant stands                                 ∆VES is the mean paired per-task difference, not the
in for that family here. Per-task call records are                                     aggregate table-level difference; the sign-test p-value
released with the artifacts.                                                           treats ties as halves.
Policy                      VES Hard Cvg s/task Evo−policy [95% CI]           W/T/L

GPT-5.4                   0.893   0.76 0.86      6.7 +0.030 [0.001, 0.062]  16/74/10
                                                                                       Closed-loop failure taxonomy.
Qwen3-Max                 0.773   0.63 0.72     32.8 +0.150 [0.091, 0.213]   30/61/9
DeepSeek-V4-Pro           0.936   0.89 0.95     23.2 −0.012 [−0.034, 0.010] 6/82/12    Outcome                              Mixed-Pref         RefineCut-Evo         Change
RefineCut-Evo (8B, local) 0.924   0.82 0.95     11.7 –                             –
                                                                                       OK plan                                 74                    91                 +17
Table 14: Same-loop teacher policies. Identical closed-                                DurationMismatch                        16                     1                 -15
                                                                                       LowCSRNoSingleFailure                    7                     4                  -3
loop contract; differences are mean paired per-task val-                               MissingClipReference                     3                     3                  0
ues, and W/T/L counts are per-task Evo wins, ties, and                                 PatchApplyFail                           0                     1                 +1
losses. The DeepSeek difference is not significant.
                                                                                       Table 18: Closed-loop failure taxonomy on Common-
Prompting, feedback, and search over the un-                                           100. The compact view highlights the main shift:
trained backbone (RQ5c). All conditions in Ta-                                         RefineCut-Evo turns more tasks into fully OK plans,
                                                                                       primarily by removing duration mismatches. Counts are
ble 15 run the untrained Qwen3-8B backbone under
                                                                                       task counts out of 100.
the frozen protocol with the stopping rule matched
to the RefineCut-Evo loop. Verifier feedback adds                                      Evo-degraded tasks. Of the five tasks where
+0.090 over direct prompting, and R=4 reranking                                        RefineCut-Evo scores below Mixed-Pref (Ta-
adds +0.054 over R=1 sampling. The visited-                                            ble 17), four preserve execution, duration, and con-
pool oracle selects, per task, the best state vis-                                     vergence and each misses exactly one constraint
ited by any of these runs; even this upper bound                                       entry: a required closing clip, a semantic tag, a tran-
stays 0.212 VES below RefineCut-Evo (95% CI                                            sition style, and a required kept clip (three family-A
[0.170, 0.252]). The feedback condition corre-                                         composition tasks and one family-B local repair).
sponds to the Prompted row of Table 1; under                                           One family-C generative-assembly task fails more
the fully matched stopping rule, tasks continue to                                     broadly, with patch applicability dropping to 0.33
the shared horizon instead of stopping at a patch-                                     and a duration overshoot. The degradations are
extraction failure, giving 0.592 against 0.594, with                                   local single-constraint misses rather than a system-
all state-level components identical.                                                  atic capability loss.
Canonical-clean closed-loop.                                                        Raw, 0.880 for Mixed-Pref vs. Verified, 0.764 for
Model                 N       FCSR           Hard    Dur         Cvg        VES
                                                                                    Mixed-Pref vs. Prompted, 0.805 for Traj-Pref vs.
Prompted              92       0.607         0.152   0.652      0.217       0.591
                                                                                    Verified, and 0.655 for Traj-Pref vs. Prompted.
Raw                   92       0.552         0.152   0.424      0.228       0.612
Verified              92       0.872         0.609   0.804      0.772       0.849
Traj-Pref             92       0.872         0.652   0.837      0.783       0.858
Mixed-Pref            92       0.879         0.652   0.826      0.793       0.859   Judge          Comparison           W    T    L   n    WRex
RefineCut-Evo         92       0.949         0.804   0.978      0.946       0.917   Judge A       Verified vs. Raw      17   2    1   20   0.944
                                                                                    Judge B†      Verified vs. Raw      18   1    0   19   1.000
Table 19: Closed-loop results on the canonical-clean                                Judge C       Verified vs. Raw      16   3    1   20   0.941
subset of Common-100 (N = 92).                                                      Judge A      Mixed vs. Verified     8    10   2   20   0.800
                                                                                    Judge B†     Mixed vs. Verified     6    13   0   19   1.000
Per-family breakdown.                                                               Judge C      Mixed vs. Verified     8    11   1   20   0.889

                                                                                    Judge A     Mixed vs. Prompted      15   1    4   20   0.789
Family                        Mixed-Pref VES                 RefineCut-Evo VES      Judge B     Mixed vs. Prompted      14   2    4   20   0.778
                                                                                    Judge C     Mixed vs. Prompted      13   2    5   20   0.722
A (composition)                      0.865                         0.892
B (insert / repair)                  0.871                         0.975            Judge A    Traj-Pref vs. Verified   11   7    2   20   0.846
C (generative)                       0.853                         0.890            Judge B    Traj-Pref vs. Verified   10   6    4   20   0.714
                                                                                    Judge C    Traj-Pref vs. Verified   12   6    2   20   0.857
Table 20: Per-family closed-loop VES on Common-100.                                 Judge A    Traj-Pref vs. Prompted   10   2    8   20   0.556
Per-subtype counts are released in the supplementary                                Judge B    Traj-Pref vs. Prompted   14   0    6   20   0.700
artifacts.                                                                          Judge C    Traj-Pref vs. Prompted   14   0    6   20   0.700

                                                                                    Table 22: Per-(judge, comparison) raw counts for the
Plan statistics and reward-hacking diagnostics.
                                                                                    distillation-stage blind API-judge analysis. WRex =
Model
                           Patches            Ops        Op.               Output   W/(W + L). † Judge B parse coverage is n=19 on
                            /task            /task     entropy             length
                                                                                    these two rows.
Prompted                    2.72             5.95        0.83               69.1
Verified                    2.61             6.23        0.89              131.5
Mixed-Pref                  2.58             6.11        0.89              135.0
RefineCut-Evo               1.76             3.77        0.99               67.5
                                                                                    Final-stage Evo API-judge alignment. A blind
Table 21: Per-variant plan statistics on Common-                                    API judge was run on final-stage compar-
100. Invalid clip references and over-rewrites are 0                                isons. After parse filtering, the aggregate non-
for all listed variants, no-regression stays 1.0, and                               tie win rates are 0.574 for Evo vs. Mixed-Pref
RefineCut-Evo’s mean duration deviation drops from                                  (108W/108T/80L), 0.545 for Evo vs. Verified
1.55 s (Mixed-Pref) to 0.34 s. RefineCut-Evo improves                               (103W/110T/86L), and 0.548 for Evo vs. Traj-Pref
with fewer, more selective edits, not longer outputs.
                                                                                    (102W/108T/84L). Aligning per-task judgments
Semantic-input intervention (full deltas). An                                       with the verifier margin explains this structure:
unmodified control run reproduces the headline                                      judge ties concentrate on tasks with ∆VES = 0
VES (0.9237). Removing only the short caption,                                      (mean |∆VES| ≈ 0.00 on judge-tie tasks vs.
while retaining the structured subject/action/scene/-                               ≈0.13 on non-tie tasks; Mann–Whitney p ≤
motion fields, yields 0.9190 (paired clean-minus-                                   1.3e−5, consistent across the three comparisons);
condition +0.0048, 95% CI [−0.0145, 0.0255],                                        when both sides give a non-tie verdict, directions
n.s.).    Removing all clip semantics yields                                        agree on 68–70% of tasks, and on every task the
0.8502 (+0.0736, [0.0422, 0.1093], p = 4.9e−5),                                     verifier scores as an Evo degradation the judge
and shuffling semantic descriptions across clips                                    points the same way. On ∆VES = 0 tasks the
yields 0.7241 (+0.1996, [0.1579, 0.2431], p =                                       judge’s non-tie verdicts are near-symmetric (e.g.,
1.6e−15), with required-clip recall falling from                                    16W/20L). The high tie rate thus reflects gen-
0.98 to 0.46.                                                                       uinely equivalent terminal plans (73/100 tasks at
                                                                                    ∆VES = 0) rather than disagreement between
Distillation-stage API-judge analysis. Three in-                                    the evaluation layers; rendered previews amplify
dependent blind API judges are run on distillation-                                 perceptual differences and separate the same com-
stage variants using a stripped pairwise prompt                                     parisons more strongly (Appendix H).
that contains no model identifiers, file paths, or
judge-identifying text (full prompt in Appendix I).
Per-judge raw counts on the 20-pair Common-100                                      Step-Pref. A step-level-only preference variant
panel are in Table 22; final-stage alignment with the                               (Step-Pref) is inconclusive: gains over Verified on
verifier is analyzed below. Pooled non-tie win rates,                               the closed-loop summary are within the variance
aggregated across judges, are 0.962 for Verified vs.                                of the multi-seed runs we performed.
H       Human Evaluation and                                                   I     Full Prompts
        Human-Written Brief Validation
This appendix reports the blind rendered-preview
evaluation (Section 4.9) and the Human50 human-                                This appendix collects compact versions of the six
written brief validation. Human evaluators com-                                prompts used throughout the pipeline. The full text
pare blind randomized A/B rendered storyboard                                  of each prompt is included in the supplementary
previews. Each comparison has 150 judged pairs                                 artifacts; each entry below records the prompt role,
and three annotators per pair. Preference score is                             expected inputs, output schema, and a compact
(W + 0.5T )/N for the first model in each compar-                              excerpt for readability.
ison. Annotators were recruited from university
campuses and partner companies, all with one to
five years of video-editing experience, and were
compensated at a rate consistent with local stan-                              Task-generation prompt. Purpose: generate
dards for their region. They received a written                                benchmark tasks and ledgers from clip pools. In-
instruction sheet covering the rating axes, blinded                            put fields: clip pool, task family, subtype, ledger
protocol, compensation, opt-out policy, and a brief                            template. Output schema: task record JSON. Ver-
content-risk disclaimer; the full instruction text is                          sion/source path: supplementary prompt artifact;
released with the supplementary artifacts.                                     compact excerpt below.
                                  Pref.   Non-tie     Maj.
Comparison             W/T/L
                                  Score    WR        Agree.
                                                                 κ      α          Task-generation prompt (compact)

Evo vs Mixed          100/34/16   0.780    0.862     0.873     0.620   0.580
Evo vs Traj            95/37/18   0.757    0.841     0.860     0.590   0.553       system: You are a video-editing task author.
                                                                                   task: Given a clip pool and a family/subtype slot,
Evo vs Verified        97/35/18   0.763    0.843     0.867     0.601   0.562
                                                                                   emit one task record with fields
Mixed vs Prompted      124/18/8   0.887    0.939     0.927     0.781   0.742
                                                                                     task_id, task_type, task_subtype,
                                                                                     brief, target_duration,
Table 23: Final pairwise human evaluation (N = 150                                   constraint_ledger (>= 4 items, includes target_duration)
                                                                                         ,
per comparison, three annotators per pair). Higher pref-                             clip_pool, structure, subtype_constraints.
erence scores and non-tie win rates prefer the first model.                        constraints:
                                                                                     - clip_ids in clip_pool MUST come from given_pool.
The sanity comparison confirms that the protocol sepa-                               - clip_pool size in [30, 60] when given_pool>=30.
rates a known large quality gap.                                                     - ledger items use the 14 allowed constraint types.
                                                                                   output: STRICT JSON; no commentary.

Human50 construction. Human50 contains 50
free-form briefs written independently by seven                                Caption prompt. Purpose: convert sampled clip
contributors unaffiliated with the authors (three                              frames into metadata read by the planner. Input
vloggers, four editing students) under a shared in-                            fields: clip frames, motion bucket, clip id, source.
struction sheet. For each brief, an LLM proposed                               Output schema: one caption metadata row. Ver-
candidate ledger entries; two research assistants                              sion/source path: supplementary prompt artifact;
revised them into decidable constraint entries fol-                            compact excerpt below.
lowing the public construction guide, and two inde-
                                                                                   Caption prompt (compact)
pendent professional video editors validated every
entry. The briefs are free-form, while the ledgers                                 system: You are a video-clip captioner.
retain the executable constraint vocabulary of the                                 input: a clip (sampled frames; sampling rate
                                                                                     determined by motion bucket: low=3, med=5, high=7).
frozen verifier, so the instruction source is human                                task: emit one JSON row with fields
                                                                                     clip_id, source, duration, subject, action,
and evaluation stays decidable. Table 24 reports                                     scene, camera, scene_category,
closed-loop results on this set.                                                     motion_intensity, caption_short,
                                                                                     model_used (record which captioner produced this row),
                                                                                     ts (ISO timestamp).
Model           FCSR        Hard      Dur          Cvg   ReqCR         VES         output: STRICT JSON; no commentary.
Prompted            0.582   0.140     0.620    0.180         0.270     0.578
Raw                 0.534   0.160     0.420    0.220         0.710     0.608
Verified            0.856   0.580     0.780    0.740         0.960     0.839   Trajectory-teacher prompt. Purpose: collect
Traj-Pref           0.852   0.620     0.800    0.740         0.960     0.842
Mixed-Pref          0.864   0.620     0.800    0.760         0.960     0.848   frontier-teacher candidate repair branches. Input
RefineCut-Evo       0.928   0.760     0.940    0.900         0.980     0.902   fields: brief, clip pool, music metadata, timeline
Table 24: Human-written brief validation (N = 50).                             state, constraint ledger. Output schema: four Re-
The ranking from Common-100 is preserved; the Evo-                             finePatch candidates. Version/source path: sup-
stage gap remains +0.054 VES over Mixed-Pref.                                  plementary prompt artifact; compact excerpt below.
 Trajectory-teacher prompt (compact)                              Stripped blind judge prompt (compact)

 system: You are a frontier video-editing planner.                system: You are a blind video-editing-plan judge.
 input: brief, clip_pool with captions and metadata,              You will see two plans for the SAME task.
   music metadata, current timeline state,                        The model identity and any file path are removed.
   constraint_ledger (with per-item satisfied flags).             input: brief, ledger, plan_A, plan_B.
 task: at this refine step, emit EXACTLY 4 candidate              task: pick the plan that better satisfies the brief and
   RefinePatch branches. Each branch must contain                   the ledger; output one of {A, B, tie} with a brief
   operations[], rationale_against_ledger[],                        reason. Do not reveal the model identity in your
   repair_operator, thought, confidence.                            reasoning. Do not mention "as an LLM".
 output: a list of 4 RefinePatch objects in STRICT JSON.          output: STRICT JSON {"winner": "A"|"B"|"tie",
                                                                                       "reason": "..."}.


Unified PatchPlanner prompt. Purpose: run
the trained planner in closed-loop evaluation. In-            J     Verifier Implementation
put fields: brief, clip pool, captions, music meta-           The verifier is deterministic: it validates a patch,
data, current state, ledger, violated subset. Output          applies it to the current state, recomputes the ledger,
schema: one RefinePatch. Version/source path:                 and emits both gate signals and branch-score com-
supplementary prompt artifact; compact excerpt                ponents.
below.
                                                              Algorithm 2 Verifier replay for one candidate
 Unified PatchPlanner prompt (compact, used at test)
                                                              patch.
 system: You are an executable video-editing planner.         Require: state st , patch pt , task record τ
 input: brief, clip_pool, captions, music_metadata,            1: if pt fails schema validation then
   current_state, constraint_ledger (with satisfied flags      2:      return reject(schema)
   and a violated_subset listing currently unmet items).       3: end if
 task: emit one RefinePatch that targets ledger items
   in violated_subset and does not regress satisfied items.    4: st+1 ← Apply(st , pt )
 constraints:                                                  5: if st+1 is invalid then
   - operations limited to RFC 6902 add/remove/replace         6:      return reject(apply)
     on canonical paths of current_state.                      7: end if
   - reference only clip_ids that appear in clip_pool.
   - keep rationale_against_ledger aligned with operations.    8: if timeline is not renderable then
 output: STRICT JSON; no commentary.                           9:      return reject(timeline)
                                                              10: end if
                                                              11: Lt ← RecomputeLedger(st , τ )
Rubric construction template. Purpose: build                  12: Lt+1 ← RecomputeLedger(st+1 , τ )
                                                              13: compute ∆CSR, TargetedRepair, ReqClipRecall, PASR,
task-specific ER1–ER7 scoring weights for                         NoRegression, and Locality
RefineCut-Evo. Input fields: task family and sub-             14: score       ←          w1 ∆CSR         +w2 TargetedRepair
type. Output schema: rubric JSON with criteria,                   +w3 ReqClipRecall +w4 PASR +w5 NoRegression
                                                                  +w6 Locality
weights, and fallbacks. Version/source path: sup-             15: return accepted patch, new state, new ledger, score terms
plementary prompt artifact; compact excerpt below.
 Rubric construction template (compact)                       Metric                       Rule
                                                              ReqClipRecall denominator Number of required keep-clip items; tasks with
 template: For task_subtype X under family F:                                           none are excluded from this component average.
   - assign ER1..ER7 a non-negative weight; sum to 1.         NoRegression              Items satisfied at Lt must remain satisfied after
   - default weights start from the family template                                     the patch; the all-steps variant conjoins this across
     (A puts mass on ER4; B and C put mass on ER3).                                     the loop.
   - for each criterion list:                                 Converged@3               Fires when terminal constraint satisfaction
       criterion_name, weight,                                                          reaches at least 0.8 within three repair steps, in-
       verifier_signals_used,                                                           cluding early termination.
       fallback_proxy_if_judge_absent.                        TargetedRepair            Counts only listed ledger items that were unsat-
 output: a rubric JSON used by the Evo scorer.                                          isfied before the patch and become satisfied after
                                                                                        replay.
                                                              VES                       Uses the fixed weights in Appendix D; undefined
                                                                                        ReqClipRecall tasks use the normalized remain-
Stripped blind judge prompt. Purpose: audit                                             ing components.
distillation-stage plans without model identity leak-
                                                              Table 25: Verifier denominator and aggregation rules.
age. Input fields: brief, ledger, plan A, plan B.
                                                              These rules keep branch scoring deterministic and avoid
Output schema: strict JSON winner plus reason.                treating undefined clip-recall denominators as successes
Version/source path: supplementary prompt arti-               or failures.
fact; compact excerpt below.
                                                              K        Worked Example
                                                              This compact example illustrates one verifier-
                                                              replay step for a b_roll_insert task. It is
                                                              schematic and is not a released-record identifier.
Item         Illustrative value

Brief         Insert a short b-roll cutaway between a speaker close-up and a
              wide street shot.
Pool          C001 speaker close-up; C002 wide street at dusk; C007 traffic-light
              cutaway; C012 empty alley.
Initial state sequence [C001, C002], durations [5.4, 10.0], total 15.4s. The
              13s duration target is violated; required clips C001 and C002 are
              already present.
Branch 1      Replace the sequence with [C001, C007, C002] and set durations
              to [5.0, 3.0, 5.0]; operator reselect_clip.
Branch 2      Keep [C001, C002] but set durations to [4.0, 9.0]; operator
              adjust_parameter.


Replay outcome. Branch 1 is selected: it fixes
duration, preserves required clips, inserts C007,
and touches only ledger-relevant fields. Branch 2
fixes duration but misses the b-roll intent, so it is
the hard negative. After Branch 1, all four ledger
items pass and the loop ends at step 1.
