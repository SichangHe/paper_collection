                                                       The Hallucination Snowball: Modeling Error Propagation as
                                                            State Transitions in Multi-Agent LLM Pipelines


                                                                                    Prabhjot Singh 1 2 Bhushan Pawar 2


                                                                  Abstract                                    1. Introduction
                                              Sequential multi-agent LLM pipelines chain spe-                 Multi-agent LLM pipelines have become the dominant ar-
                                              cialized agents without verification at handoffs,               chitecture for complex, high-stakes AI tasks. Frameworks
                                              creating a structural flaw with measurable and se-              like LangGraph (LangChain AI, 2024), AutoGen (Wu et al.,
                                              vere consequences. We show that hallucinations                  2023), and CrewAI (CrewAI Inc., 2024) make it trivial to
                                              injected at Stage 1 do not merely persist; they                 chain specialized agents sequentially: Researcher → An-
                                              transform: raw numerical facts become derived                   alyst → Writer → Reviewer. Each agent receives only
                                              computations, then narrative prose, then editori-               its predecessor’s text output with no provenance metadata,
arXiv:2608.14588v1 [cs.AI] 22 Jun 2026




                                              ally approved conclusions. At each transforma-                  no confidence scores, and no access to source documents.
                                              tion, detectability degrades near-irreversibly. We              Every agent trusts its predecessor completely. This archi-
                                              formalize this as the hallucination snowball effect,            tectural choice has a measurable and surprisingly severe
                                              a first-order Markov process over four states (Raw              consequence.
                                              Fact → Derived → Narrative → Invisible) with
                                                                                                              Consider a hallucination introduced at Stage 1: “COGS
                                              empirically measured per-boundary escape proba-
                                                                                                              was $71.2B” (true value: $63.1B). By Stage 2, the Analyst
                                              bilities of 24.6%, 48.3%, and 89.3%. Across 346
                                                                                                              computes “an 8.3% YoY increase,” a derived claim built on
                                              automatically injected hallucinations in a 4-agent
                                                                                                              a fabricated base. By Stage 3, the Writer produces “Boeing
                                              financial analysis pipeline on FinanceBench, gpt-
                                                                                                              faced significant cost headwinds, with COGS rising 8.3%
                                              4o detection drops from 72.0% at Stage 1 to 50.9%
                                                                                                              to $71.2B, reflecting supply chain disruptions.” By Stage 4,
                                              at Stage 4, and 23.7% of hallucinations survive
                                                                                                              the Reviewer approves it as “well-structured analysis with
                                              completely undetected in the final output. Even
                                                                                                              sound reasoning,” having been given no source documents
                                              the strongest model tested (Qwen3.5-397B-A17B,
                                                                                                              and only able to check internal consistency. The hallucina-
                                              87.0% at Stage 1) faces a structural ceiling; pro-
                                                                                                              tion has been laundered completely.
                                              jected Stage 4 detection is only ∼60–65%. Crit-
                                              ically, boundary gates using identical RAG veri-                Prior work frames hallucination mitigation as finding a bet-
                                              fication tools reduce hallucination survival from               ter detector (Min et al., 2023; Dhuliawala et al., 2024; Song
                                              58.4% to 16.2% versus end-of-pipeline checking                  et al., 2024; Wei et al., 2024). We show this framing is fun-
                                              (Cohen’s h = −0.911, p < 0.000001), while                       damentally incomplete for sequential multi-agent systems.
                                              end-checking alone achieves merely 2.3 pp im-                   gpt-4o detection drops from 72.0% at Stage 1 to 50.9% at
                                              provement over no verification. When you verify                 Stage 4, a 21.1 pp decay regardless of detector sophisti-
                                              matters more than whether you verify. Our model                 cation. End-of-pipeline verification achieves only 2.3 pp
                                              predicts survival for n-agent linear pipelines and              improvement over no verification (from 60.7% to 58.4% sur-
                                              prescribes optimal verification resource alloca-                vival) because the information required to verify the original
                                              tion: invest at S1 →S2 first, where 75.4% of hallu-             claim is structurally destroyed by upstream transformations.
                                              cinations are still catchable, not at S3 →S4 where              The correct framing is propagation control, not detection.
                                              89.3% have already escaped.
                                                                                                              We present three experiments and a theoretical model.† Sec-
                                                                                                              tion 3.2 measures detectability decay across stages. Sec-
                                             1
                                               The University of Texas at Austin, Austin, TX,                 tion 3.3 characterizes the structural ceiling of LLM skepti-
                                         USA 2 RediMinds Inc., USA. Correspondence to: Prab-                  cism. Section 3.4 demonstrates that boundary gates reduce
                                         hjot Singh <prabhjot.singh@utexas.edu>, Bhushan Pawar
                                         <bhushan.pawar@rediminds.com>.                                       survival from 58.4% to 16.2%, a 42.2 pp improvement over
                                                                                                              end-checking (Cohen’s h = −0.911, p < 0.000001), at
                                         Accepted at the FAGEN Workshop (Failure Modes in Agentic AI),          †
                                         ICML 2026 (43rd International Conference on Machine Learning),           Code and results available at https://github.com/
                                         Seoul, South Korea, 2026. Copyright 2026 by the author(s).           prabhjotschugh/hallucination-snowball.


                                                                                                          1
                                       The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

a measured quality cost of 4.44 to 3.93 on internal consis-                                  et al., 2024) extends this to structured adversarial debate.
tency. Section 4 formalizes propagation as a Markov process                                  Critically, both use parallel topologies where all agents
with measured transition probabilities and prescribes opti-                                  share the same factual foundation simultaneously. Sequen-
mal gate placement. Figure 1 illustrates the four states and                                 tial propagation, where each agent sees only the previous
their empirically measured escape probabilities. While we                                    agent’s transformed output, is structurally absent from this
demonstrate this in financial analysis, chosen for its unam-                                 line of work. Our failure mode is orthogonal and addresses
biguous numeric ground truth, the transformation mecha-                                      the architecture actually deployed in production via Lang-
nism is domain-agnostic: any pipeline where a checkable                                      Graph (LangChain AI, 2024), AutoGen (Wu et al., 2023),
fact can be converted into confident narrative faces identi-                                 and CrewAI (CrewAI Inc., 2024).
cal dynamics. Medical summarization pipelines that chain
extraction and synthesis, legal review pipelines that chain                                  2.3. Trust and Security in Multi-Agent Systems
precedent retrieval and brief drafting, and research automa-
tion pipelines that chain literature search and report genera-                               TrustAgent (Hua et al., 2024) and work on rogue
tion all share the same structural flaw. The measurement in-                                 agents (Yang et al., 2024) study intentional adversarial ma-
frastructure and gate architecture we provide are structurally                               nipulation by malicious agents in multi-agent settings. Our
applicable across all of them, though domain-specific escape                                 failure mode is categorically different: it requires no adver-
rates will require calibration outside the numeric-finance                                   sary. Completely well-intentioned agents following their
setting.                                                                                     instructions faithfully produce the hallucination snowball
                                                                                             because the architecture provides no error-correction mech-
                                 Increasing Irreversibility                                  anism at handoffs. This makes the snowball more pervasive
                                                                                             than adversarial threats, which require compromised intent.
                      24.6%                48.3%                  89.3%
         S11
         S                       S22
                                 S                      S33
                                                        S                     S44
                                                                              S
    Raw Fact                  Derived                Narrative            Invisible          2.4. RAG and Retrieval-Augmented Verification
  Checkable numeric           Computed                 Causal              Editorially
        claim                 derivative              narrative            approved
                                                                                             Lewis et al. (Lewis et al., 2021) introduced retrieval-
      Stage 1                 Stage 2                 Stage 3              Stage 4
                                                                                             augmented generation to ground LLM outputs in external
                                                                                             documents. Subsequent work (Gao et al., 2024) has ex-
Figure 1. Four-state Markov process of hallucination propagation.                            tended RAG to diverse settings. Our boundary gate is in-
Escape probabilities rise from 24.6% to 89.3% across boundaries;
by S3 →S4 , nearly 90% of hallucinations are structurally unrecov-                           spired by this line of work but deployed at a fundamentally
erable by any downstream gate.                                                               different layer: not to augment generation, but to verify
                                                                                             agent output at handoff points before the next agent pro-
                                                                                             cesses it. Crucially, our gate is a deterministic numeric
2. Background and Related Work                                                               matcher (zero LLM calls) rather than a retrieval system; we
                                                                                             retain the “RAG” label only to signal the grounding intent,
2.1. Single-Agent Hallucination Detection                                                    not the mechanism. The placement principle, verify before
The dominant paradigm treats hallucination as a property                                     handoff, not before generation, is novel.
of isolated model outputs. FActScore (Min et al., 2023)
decomposes generations into atomic claims and verifies                                       2.5. Concurrent and Complementary Work
each against a knowledge source. CoVe (Dhuliawala et al.,                                    AgentHallu (Liu et al., 2026) independently confirms that
2024) uses self-verification chains where a model checks its                                 early-stage errors dominate downstream failures; where it
own outputs. VeriScore (Song et al., 2024) extends this to                                   diagnoses which agent caused a hallucination post-hoc, we
long-form generation. SAFE (Wei et al., 2024) uses search-                                   measure how detectability degrades across transformations
augmented fact evaluation. All of these operate at what we                                   and intervene before transformation occurs. VERIMAP (Xu
call S1 only: a single output evaluated in isolation. None                                   et al., 2026) operationalizes per-subtask verification in DAG-
models what happens when one agent’s hallucinated output                                     structured workflows; our Markov model provides data-
becomes the next agent’s input. Our work shows that a                                        driven guidance for where gates yield the highest return
hallucination detectable at 72.0% at S1 becomes catchable                                    within such frameworks. CaveAgent (Ran et al., 2026) re-
at only 50.9% three transformations later, making single-                                    duces laundering by avoiding lossy text handoffs entirely, an
agent evaluation an insufficient framework for sequential                                    orthogonal mitigation that trades architectural flexibility for
pipelines.                                                                                   verifiability. Comparing boundary gates against structured-
                                                                                             handoff baselines remains an important open question.
2.2. Multi-Agent Debate and Collaboration
Du et al. (Du et al., 2024) show that multiple LLMs debating
over the same question improves reasoning. MAD (Liang

                                                                                         2
                        The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

2.6. The Gap We Fill                                                 the pre-injection researcher output at 1% tolerance (tighter
                                                                     than the 2% tolerance used in Experiment 3’s RAG gate,
No prior work provides a mathematical framework for hallu-
                                                                     which accommodates agent-introduced numeric reformat-
cination transformation across sequential agents, measures
                                                                     ting such as rounding $71.2B to $71B). The retrieval checker
where detectability decays most sharply within a pipeline, or
                                                                     represents the theoretical detection ceiling; gpt-4o Judge
demonstrates empirically that verification timing dominates
                                                                     represents the realistic deployment scenario.
verification tooling. The FMAI workshop calls for trace-
level diagnostics and explicit evidence about what improves
                                                                     3.2. Experiment 1: Detectability Decay Across Stages
and what does not. Prior work offers neither for sequential
multi-agent systems. We address all three.                           We evaluate both detection instruments independently at all
                                                                     four pipeline stages across all 346 injected hallucinations
3. Experiments                                                       (Table 1).

3.1. Setup and Injection Protocol                                             Stage                                         gpt-4o Judge          Retrieval            Either

Pipeline. We implement a 4-agent sequential pipeline in                       S1 - Researcher                                    72.0%              91.9%              97.7%
LangGraph (LangChain AI, 2024):                                               S2 - Analyst                                       60.4%              73.1%              84.4%
                                                                              S3 - Writer                                        53.2%              65.0%              76.3%
                                                                              S4 - Reviewer                                      50.9%              67.1%              76.3%
      Researcher → Analyst → Writer → Reviewer
                                                                              Drop (S1 →S4 )                                   −21.1 pp           −24.8 pp            −21.4 pp

All agents use gpt-4o-mini (temperature=0.3) with role-                                   Table 1. Detection rates by stage. Drop measured S1 →S4 .
specific system prompts. The Researcher extracts exact fig-
ures from SEC filings. The Analyst computes YoY changes
and ratios using only Researcher output. The Writer pro-             gpt-4o detection drops 21.1 pp from Stage 1 to Stage 4. Crit-
duces a 300–500 word professional narrative. The Reviewer            ically, 82/346 hallucinations (23.7%) survive completely
performs internal consistency checking only, with no access          undetected by either instrument in the final output. Zero hal-
to source documents.                                                 lucinations follow the all-missed trajectory: every injected
                                                                     hallucination is detectable at Stage 1. The pipeline, not
Dataset. We evaluate on FinanceBench (Islam et al.,                  the hallucination itself, is what produces invisibility. Fig-
2023), 150 expert-annotated financial QA pairs from real             ure 2 visualizes detectability decay across all three detection
SEC filings with exact numeric ground truth. We exclude 10           methods.
questions producing qualitative outputs with no injectable                                100%                                                              gpt-4o Judge
numeric values, yielding 140 usable questions. All questions                                                                                                Retrieval Checker
are converted to complex multi-part analytical directives via                             90%                                                               Either (Union)
gpt-4o-mini to reflect realistic pipeline inputs.
                                                                     Detection Rate (%)




                                                                                          80%

Injection Protocol. We automatically inject 346 hallu-                                    70%
cinations across 140 questions (2–3 per question) using
                                                                                          60%                   -11.6 pp
deterministic regex-based perturbation with fixed seeds
(RANDOM SEED=42). Dollar amounts and large numbers                                                                                     -7.2 pp                              50%
                                                                                          50%
are multiplicatively shifted by 15–40%; percentages receive                                                                                                 -2.3 pp

an additive shift of 3–12 pp. Injection occurs immediately                                40%
                                                                                                      S1                      S2                   S3                      S4
after Stage 1, before any downstream agent, forcing halluci-                                     (Researcher)              (Analyst)             (Writer)              (Reviewer)
nations to propagate through the full transformation chain.
                                                                     Figure 2. Hallucination detectability decays monotonically across
All injections are logged with complete metadata enabling            all three detection methods (n=346). Every hallucination is de-
exact replication.                                                   tectable at S1 ; gpt-4o Judge drops 21.1 pp by S4 , confirming the
                                                                     pipeline, not the hallucination itself, creates invisibility.
Detection Instruments. We use two instruments applied
independently to each of the four stage outputs. gpt-4o              Decay is boundary-concentrated, not uniform. The largest
Judge: a forensic financial auditor with no ground truth             drop occurs at S1 →S2 (gpt-4o: −11.6 pp; Retrieval:
access, instructed to flag suspicious claims via internal rea-       −18.8 pp), where raw numeric facts become derived com-
soning alone. Retrieval Checker: a fully deterministic               putations requiring inverse calculation to verify. A second
numeric matcher (zero LLM calls) comparing agent output              significant drop occurs at S2 →S3 (−7.2 pp; −8.1 pp) as
against FinanceBench ground truth, evidence strings, and             figures become causally embedded narrative. The S3 →S4

                                                                 3
                        The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

boundary is essentially inert (−2.3 pp; +2.1 pp): the Re-            after Agent 4 only, detection but no correction possible),
viewer is editorial, not transformative. Laundering happens          and Ours (identical deterministic gates after every agent
upstream, not at the final gate. Trajectory analysis con-            handoff, with annotated corrections passed downstream);
firms systematic behavior: 10.7% of hallucinations follow            results in Table 3. This design isolates placement as the sole
✓→ × → × →× (detectable at Stage 1, permanently lost                 variable: same tools, different timing.
thereafter) and 9.0% follow ✓→✓→ × →×, together ac-
counting for 23.4% of all cases (see Appendix A).                                    Metric                                            Vanilla      End-Check                   Ours
                                                                                     Survival Rate                                      60.7%              58.4%                16.2%
3.3. Experiment 2: Capability Ceilings of LLM                                        Actionable Detection                                0.0%               0.0%                76.9%
     Skepticism                                                                      Hallucination-Free Reports                         18.6%              20.0%                68.6%
We test whether a sufficiently capable model can overcome                            Correction Rate                                    26.6%              26.3%                54.0%
the structural detection ceiling (Table 2). Four state-of-                           Output Quality (1–5)                                4.16               4.44                 3.93
the-art models are evaluated as skeptic agents at Stage 1,
                                                                     Table 3. Hallucination survival and key metrics (n=346 hallucina-
the best-case position where hallucinations are still raw            tions, n=140 questions).
numerical values, on all 346 hallucinations under identical
prompts and matching protocols.
                                                                     End-of-pipeline checking achieves 2.3 pp improvement over
 Model                   Detection     95% CI       Survival         no verification, statistically negligible and architecturally
                                                                     unactionable since no downstream agent can receive a cor-
 Meta-Llama-3-70B-        51.4%      [46.2–56.6%]    48.6%
 Instruct                                                            rection. Boundary gating achieves −44.5 pp versus Vanilla
 gemini-2.5-flash         72.5%      [67.6–77.2%]    27.5%           and −42.2 pp versus End-Check, confirmed by five inde-
 gpt-4o (Exp. 1 ref.)     72.0%      [67.1–76.6%]    28.0%           pendent statistical tests (McNemar χ2 =122.24, permuta-
 DeepSeek-V3.2            75.7%      [71.1–80.3%]    24.3%           tion p < 0.000001, Cohen’s h=−0.911, χ2 =129.94, Fisher
 Qwen3.5-397B-A17B        87.0%      [83.2–90.5%]    13.0%           OR=0.138; all p < 0.000001). Figure 3 traces hallucina-
                                                                     tion presence at each stage, confirming that boundary gates
Table 2. Stage 1 detection rates with 95% bootstrap CIs (5,000       intercept the cascade at its origin.
resamples).
                                                                                                  110
                                                                                                                                                            Vanilla (no verification)
                                                                                                  100   96.8 96.8 96.8                                      End-Check (end-of-pipeline)
                                                                                                                         92.2 91.6                          Ours (boundary gates)
Bootstrap CIs reveal three statistically distinct clusters:                                        90
                                                                                                                                                                          Final
                                                                                                   80                                                                    Output
                                                                     Hallucinations Present (%)




Meta-Llama-3-70B-Instruct alone at the bottom (p <
                                                                                                                                     70.2
0.000001 vs. all others via McNemar tests); gemini-2.5-                                            70                                       65.9 64.7
                                                                                                                                                                    60.7 58.4
                                                                                                   60
flash, DeepSeek-V3.2, and gpt-4o mutually indistinguish-
                                                                                                   50
able; Qwen3.5-397B-A17B significantly above all others
                                                                                                   40
(p < 0.001 for all pairwise comparisons), yet its upper CI                                         30                                                     24.6
bound is 90.5%. No model approaches 100% (full pairwise                                            20                                                                           16.2
tests in Appendix A).                                                                              10
                                                                                                    0
The ceiling is structural, not a model quality problem. Per-                                                 S1               S2                  S3                      S4
                                                                                                         Researcher         Analyst              Writer                Reviewer
centage hallucinations are detected at 71–98% because
a 30%+ additive shift is often obviously implausible;                Figure 3. Boundary gates intercept the cascade at its origin while
dollar amounts are detected at only 49–86% because a                 baselines decay passively. All methods begin identically at S1
12.8% perturbation on Boeing’s COGS is entirely within               (96.8%); Gate 1 alone drives a 26.6 pp drop at S2 , reducing final
                                                                     survival to 16.2% versus 60.7% for Vanilla, a 3.75× reduction.
industry-plausible range. Plausibility reasoning cannot
catch magnitude-plausible-but-wrong values without ground
                                                                     Gate breakdown exposes the mechanism (Table 4): Gate 1
truth access. Even projecting the strongest model (Qwen3.5-
                                                                     alone captures 75.4%, nearly as much as all three gates com-
397B-A17B, 87.0%) through measured decay rates, Stage 4
                                                                     bined (76.9%). Gate 3 adds only 1.5 pp of marginal cover-
detection falls to 60–65%, leaving 35–40% undetected in
                                                                     age. Stage-by-stage presence curves confirm early intercep-
the final report (Appendix A).
                                                                     tion: all three methods begin identically at S1 (96.8% pres-
                                                                     ence;3 ); divergence begins at S2 (Ours: 70.2% vs. Vanilla:
3.4. Experiment 3: Timing Dominates Method
                                                                         3
                                                                           The 3.2% gap from 100% reflects injections whose logged
We isolate the effect of verification placement using a full         numeric scale differs from their text representation (e.g., 71200
gemini-2.5-flash pipeline with three conditions: Vanilla             vs. $71.2B); the 2% evaluation tolerance cannot bridge this unit
(no verification), End-Check (deterministic numeric gate             mismatch.

                                                                 4
                           The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

92.2%) and accelerates through S3 (Ours: 24.6% vs. Vanilla:              Transition   Escape sk   95% CI          Interpretation

65.9%).                                                                  S1 →S2       24.6%       [19.9–28.9%]    Raw facts directly matchable;
                                                                                                                  highest-value gate
                                                                         S2 →S3       48.3%       [42.8–53.8%]    Derived computations partially
 Gate              Position         Detection        95% CI                                                       reversible
                                                                         S3 →S4       89.3%       [86.1–92.5%]    Narrative embedding is
 Gate 1            S1 →S2             75.4%       [71.1–80.1%]                                                    near-irreversible

 Gate 2            S2 →S3             51.7%       [46.2–57.2%]          Table 5. Measured per-boundary escape probabilities (derived
 Gate 3            S3 →S4             10.7%        [7.5–13.9%]          from Experiment 3 gate detection rates).
 Any Gate          —                  76.9%       [72.3–81.2%]

          Table 4. Per-gate detection rates (Ours only).                mathematical explanation for why end-checking fails: by
                                                                        the time an end gate runs, nearly 90% of narrative-embedded
                                                                        hallucinations are structurally unrecoverable.
The −0.51 quality drop (Ours vs. End-Check, 3.93 vs. 4.44)
 is real but its source is precise: post-hoc analysis of all 266
 gate interventions finds a false positive rate of 0.4% (1/266)         Predictive Formula. For a linear n-agent pipeline with
- the gate almost never refutes a reference-correct value. The          per-boundary escape probabilities s1 , . . . , sn−1 :
 quality penalty instead originates from suppression-without-
 restoration: in 32.7% of caught cases (87/266), the gate                                                        n−1
                                                                                                                 Y
 correctly suppressed the injected value but the downstream                                   P (survival) =           sk
 agent failed to propagate the annotated correction, leaving                                                     k=1
 a numerical gap. This is an instruction-following limita-
 tion, not a gate accuracy problem, and points directly to              For our 4-agent setup: 0.246 × 0.483 × 0.893 ≈ 10.6%,
 source-grounded correction (injecting the correct value ex-            versus measured 16.2%. The 5.6 pp gap reflects gate false
 plicitly into agent context) as the fix. The gate precision is         negatives from value reformatting (e.g., “$71.2 billion” →
 high; the correction propagation is not. Despite this, 96/140          “71.2B”), rounding, and unit conversion. The Markov model
 hallucination-free reports versus 28/140 represents a cate-            describes transformation dynamics; measured detection
 gorical improvement in factual accuracy. A coherent report             probabilities provide a lower bound on survival.
 built on a fabricated figure is not a high-quality report.
                                                                        Design Prescriptions. Three actionable prescriptions fol-
                                                                        low directly from the model, addressing FMAI’s call
4. State-Transition Model
                                                                        for verified fixes with explicit resource tradeoffs. (1)
We formalize hallucination propagation as a first-order                 Gate placement: invest at S1 →S2 first (75.4% detection),
Markov process over four states defined by the form a hallu-            then S2 →S3 (51.7%). The S3 →S4 gate contributes only
cination takes at each pipeline stage:                                  10.7% marginal detection and is economically unjustified
                                                                        in resource-constrained deployments. (2) The first gate
                      1s    2   s 3     s                               dominates: every hallucination surviving Gate 1 faces a
                  S1 −→ S2 −→ S3 −→ S4
                                                                        48.3% chance of surviving Gate 2 and an 89.3% chance of
                                                                        surviving Gate 3. Gate 1 is worth more than Gates 2 and 3
where sk is the per-boundary escape probability. States
                                                                        combined. (3) Pipeline length risk: in a 6-agent pipeline
are defined by irreversible transformation: once a raw fact
                                                                        without gates, vanilla survival would exceed our measured
(S1 ) is embedded in a derived computation (S2 ), the origi-
                                                                        60.7% as additional transformation stages increase launder-
nal checkable claim is structurally destroyed. Downstream
                                                                        ing opportunities. With gates, the model predicts survival
agents cannot recover it because they receive only trans-
                                                                        of approximately 8–12% depending on per-boundary es-
formed text. This irreversibility property explains why end-
                                                                        cape rates, suggesting diminishing but positive returns from
of-pipeline verification fails: the information required to
                                                                        extending the gated architecture.
verify the original claim no longer exists in verifiable form.

Measured Transition Probabilities. We derive escape                     5. Discussion
probabilities directly from Experiment 3 gate detection rates
                                                                        Limitations. Three limitations bound our current claims.
(sk = 1 − gate detectionk ), shown in Table 5.
                                                                        First, our experiments operate in the financial domain, cho-
The progression 24.6% → 48.3% → 89.3% quantifies                        sen precisely for its unambiguous numeric ground truth.
progressive irreversibility: each stage roughly doubles the             Detection rates and decay slopes may differ in domains
fraction of hallucinations that will survive to the final output.       where facts are less crisply verifiable, such as medical sum-
The near-unity S3 →S4 escape probability (89.3%) is the                 marization or legal review. The transformation mechanism

                                                                    5
                        The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

(S1 →S4 ) is domain-agnostic; the specific rates are not. Sec-         fully deterministic (zero LLM calls); in our setup, boundary
ond, we evaluate a strictly linear 4-agent topology. Branch-           gating adds approximately 0.9 seconds of total overhead
ing, parallel, and cyclic architectures have different propaga-        across three gates due to rate limiting, negligible relative to
tion dynamics that the current Markov formulation does not             the 3–5 second per-agent Gemini latency. This produces a
capture. Extended transition matrices for non-linear topolo-           22.9 pp gap between actionable detection (76.9%) and full
gies remain future work. Third, our perturbation range                 correction (54.0%): the hallucination is suppressed but the
of 15–40% models realistic LLM hallucinations that are                 correct value is not always propagated. A stronger interven-
plausible-but-wrong. Subtle hallucinations below 5% pertur-            tion would retrieve and inject the correct value directly into
bation, which may be more common in practice for certain               agent context rather than relying on instruction-following to
domains, are not tested and would likely produce lower gate            propagate an annotation. We expect source grounded cor-
detection rates given the 2% matching tolerance. Fourth, we            rection to close this gap substantially and reduce the quality
do not evaluate structured-handoff baselines (typed JSON               penalty simultaneously, since agents would have the correct
fields, citation passing, or provenance-preserving program-            value explicitly available rather than inferring it from an
matic state (Ran et al., 2026)), which may independently               annotation.
reduce laundering by avoiding lossy free-text transforma-
tions entirely. Where boundary gates intercept hallucina-              Generalization to Other Pipeline Topologies. The
tions after transformation has begun, structured handoffs              Markov formulation extends naturally to n-agent          linear
                                                                                                                            Qn−1
would prevent the transformation step itself. Whether this             pipelines via the product formula P (survival) = k=1 sk .
architectural alternative achieves comparable or superior              For non-linear topologies, the key insight generalizes even
survival reduction, and at what cost to pipeline flexibility, is       if the formula does not: verification value is highest immedi-
a direct avenue for future work.                                       ately before a transformation that destroys verifiability, and
                                                                       lowest after narrative embedding has occurred. In branching
The Quality Metric is Structurally Blind to the Interven-              pipelines, this prescribes gates at every merge point where
tion’s Primary Benefit. The −0.51 quality drop (3.93 vs.               outputs from parallel agents are synthesized. In memory-
4.44) requires careful interpretation. Our evaluator scores            augmented pipelines, it prescribes verification before any
internal consistency without access to ground truth, which             memory write, since a hallucination written to persistent
means it is structurally incapable of rewarding the primary            memory propagates to every future agent that reads it.
benefit of boundary gating: factual accuracy. A pipeline that
produces a fluent, internally consistent report built on a fab-        Why This Matters Beyond Finance. The hallucination
ricated $71.2B figure scores higher than one that correctly            snowball is not a financial analysis problem. It is a systems
suppresses that figure but leaves a numerical gap. This is             architecture problem that manifests wherever sequential
precisely the wrong incentive structure for high-stakes de-            agents transform each other’s outputs without structured
ployment, and it means our quality scores systematically               verification. Medical summarization pipelines that chain
underestimate the true benefit of our intervention. The cor-           extraction, synthesis, and report generation face identical dy-
rect evaluation instrument is a metric that jointly scores             namics. Legal review pipelines that chain document parsing,
factual accuracy and narrative coherence - for example, a              precedent retrieval, and brief drafting face identical dynam-
retrieval-grounded rubric that checks each numerical claim             ics. Any domain where a wrong fact can be transformed
in the final report against the source filing before scoring           into a confident narrative and then institutionally approved
analytical quality. We expect such an instrument would not             faces this failure mode. The measurement infrastructure and
only close the observed quality gap but reverse it: a report           gate architecture we provide are domain-agnostic in mecha-
with 96/140 hallucination-free outputs is categorically more           nism; practitioners in other domains should expect different
valuable than one with 28/140, regardless of how fluent the            per-boundary escape rates requiring domain-specific cali-
hallucinated reports appear. Designing and validating this             bration.
joint metric is a direct avenue for future work and a pre-
requisite for fair evaluation of any boundary-gating system.
This tradeoff directly addresses FMAI’s call for explicit evi-
                                                                       6. Conclusion
dence about what improves and what does not: our method                We present the hallucination snowball effect: a formally
improves factual accuracy substantially and measurably;                characterized, empirically measured, and theoretically mod-
the quality cost is real but measured by an instrument that            eled failure mode in sequential multi-agent LLM pipelines.
cannot see the benefit it trades against.                              Hallucinations do not merely persist across agent handoffs.
                                                                       They transform through predictable stages that progressively
Annotation-Based Correction vs. Source Grounding.                      destroy verifiability, from a checkable raw fact at S1 to an
Our boundary gates annotate refuted values and instruct                editorially approved conclusion at S4 that no downstream
downstream agents to use corrected figures. Each gate is               agent can recover. gpt-4o detection degrades 21.1 pp across

                                                                   6
                        The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

four stages. 23.7% of hallucinations escape entirely. Even           References
the strongest model tested faces a structural ceiling of 87.0%
                                                                     CrewAI Inc. CrewAI: Framework for orchestrating role-
at best-case conditions, projected to 35–40% survival at
                                                                       playing, autonomous AI agents. https://github.
Stage 4.
                                                                       com/crewAIInc/crewAI, 2024.
The solution is not a better detector. It is earlier interven-
tion. Boundary gates using identical tools to end-of-pipeline        Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R.,
checking achieve a 42.2 pp reduction in hallucination sur-             Li, X., Celikyilmaz, A., and Weston, J. Chain-of-
vival (Cohen’s h = −0.911), confirmed by five indepen-                verification reduces hallucination in large language
dent statistical tests. The Markov model explains precisely            models. In Ku, L.-W., Martins, A., and Srikumar,
why: the S3 →S4 escape probability is 89.3%, meaning                  V. (eds.), Findings of the Association for Computa-
that by the time an end gate runs, nearly 90% of narrative-            tional Linguistics: ACL 2024, pp. 3563–3578, Bangkok,
embedded hallucinations are already unrecoverable. Gate 1             Thailand, August 2024. Association for Computa-
alone, placed at S1 →S2 , captures 75.4% of all hallucina-             tional Linguistics. doi: 10.18653/v1/2024.findings-acl.
tions while they are still raw numerical facts and directly            212. URL https://aclanthology.org/2024.
matchable against reference values.                                    findings-acl.212/.

This intervention comes with a measured cost: output qual-           Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., and Mordatch,
ity drops from 4.44 to 3.93 on internal consistency scoring,           I. Improving factuality and reasoning in language models
reflecting a genuine accuracy-coherence tradeoff. Post-hoc             through multiagent debate. In Proceedings of the 41st In-
analysis attributes this primarily to suppression-without-             ternational Conference on Machine Learning, ICML’24.
restoration (32.7% of caught cases) rather than false posi-            JMLR.org, 2024.
tives (0.4%), pointing to source-grounded correction as the          Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y.,
direct fix. We report this honestly because FMAI’s call                Sun, J., Wang, M., and Wang, H. Retrieval-augmented
for explicit evidence about what improves and what does                generation for large language models: A survey, 2024.
not demands it. The tradeoff is real, but it is preferable to          URL https://arxiv.org/abs/2312.10997.
the alternative: a fluent, coherent report built entirely on
fabricated figures.                                                  Hua, W., Yang, X., Jin, M., Li, Z., Cheng, W.,
                                                                      Tang, R., and Zhang, Y.        TrustAgent: Towards
The reframe this paper offers is simple and actionable: from
                                                                       safe and trustworthy LLM-based agents.         In Al-
“can we detect hallucinations?” to “can we control their prop-
                                                                       Onaizan, Y., Bansal, M., and Chen, Y.-N. (eds.), Find-
agation?” For practitioners deploying multi-agent pipelines
                                                                       ings of the Association for Computational Linguis-
in high-stakes domains today, this is not a theoretical con-
                                                                       tics: EMNLP 2024, pp. 10000–10016, Miami, Florida,
cern. It is a measurable, reproducible, and now-addressable
                                                                       USA, November 2024. Association for Computational
systems engineering problem. Act before transformation,
                                                                       Linguistics. doi: 10.18653/v1/2024.findings-emnlp.
not after.
                                                                       585. URL https://aclanthology.org/2024.
                                                                       findings-emnlp.585/.
                                                                     Islam, P., Kannappan, A., Kiela, D., Qian, R., Scherrer,
                                                                        N., and Vidgen, B. Financebench: A new benchmark
                                                                        for financial question answering, 2023. URL https:
                                                                        //arxiv.org/abs/2311.11944.
                                                                     LangChain AI. LangGraph: Build stateful, multi-actor
                                                                       applications with LLMs. https://github.com/
                                                                       langchain-ai/langgraph, 2024.
                                                                     Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin,
                                                                       V., Goyal, N., Küttler, H., Lewis, M., tau Yih, W.,
                                                                       Rocktäschel, T., Riedel, S., and Kiela, D. Retrieval-
                                                                       augmented generation for knowledge-intensive nlp tasks,
                                                                       2021.     URL https://arxiv.org/abs/2005.
                                                                       11401.
                                                                     Liang, T., He, Z., Jiao, W., Wang, X., Wang, Y., Wang, R.,
                                                                       Yang, Y., Shi, S., and Tu, Z. Encouraging divergent think-
                                                                       ing in large language models through multi-agent debate.

                                                                 7
                        The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

  In Al-Onaizan, Y., Bansal, M., and Chen, Y.-N. (eds.),               Long Papers), pp. 7528–7546, Rabat, Morocco, March
  Proceedings of the 2024 Conference on Empirical Meth-                2026. Association for Computational Linguistics. ISBN
  ods in Natural Language Processing, pp. 17889–17904,                 979-8-89176-380-7. doi: 10.18653/v1/2026.eacl-long.
  Miami, Florida, USA, November 2024. Association                      353. URL https://aclanthology.org/2026.
  for Computational Linguistics. doi: 10.18653/v1/2024.                eacl-long.353/.
  emnlp-main.992. URL https://aclanthology.
  org/2024.emnlp-main.992/.                                          Yang, W., Bi, X., Lin, Y., Chen, S., Zhou, J., and Sun,
                                                                       X. Watch out for your agents! investigating back-
Liu, X., Yang, X., Li, Z., Li, P., and He, R. Agenthallu:              door threats to llm-based agents, 2024. URL https:
  Benchmarking automated hallucination attribution of llm-             //arxiv.org/abs/2402.11208.
  based agents, 2026. URL https://arxiv.org/
  abs/2601.06818.
Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P.,
 Iyyer, M., Zettlemoyer, L., and Hajishirzi, H. FActScore:
 Fine-grained atomic evaluation of factual precision in
 long form text generation. In Bouamor, H., Pino, J., and
 Bali, K. (eds.), Proceedings of the 2023 Conference on
 Empirical Methods in Natural Language Processing, pp.
 12076–12100, Singapore, December 2023. Association
 for Computational Linguistics. doi: 10.18653/v1/2023.
 emnlp-main.741. URL https://aclanthology.
 org/2023.emnlp-main.741/.
Ran, M., Wan, Z., Lin, C., Zhang, Y., Xin, H., Fan, H., Xu,
  Y., Luo, B., Zhou, Y., Zhao, W., Yang, L., Feng, L., Yang,
  F., Wu, J., Huang, Y., Ma, C., Jiang, D., Deng, J., Han,
  S., You, Y., An, B., Guo, Y., and Song, J. Caveagent:
  Transforming llms into stateful runtime operators, 2026.
  URL https://arxiv.org/abs/2601.01569.
Song, Y., Kim, Y., and Iyyer, M. VeriScore: Evaluating
  the factuality of verifiable claims in long-form text gen-
  eration. In Al-Onaizan, Y., Bansal, M., and Chen, Y.-N.
  (eds.), Findings of the Association for Computational Lin-
  guistics: EMNLP 2024, pp. 9447–9474, Miami, Florida,
  USA, November 2024. Association for Computational
  Linguistics. doi: 10.18653/v1/2024.findings-emnlp.
  552. URL https://aclanthology.org/2024.
  findings-emnlp.552/.
Wei, J., Yang, C., Song, X., Lu, Y., Hu, N., Huang, J., Tran,
 D., Peng, D., Liu, R., Huang, D., Du, C., and Le, Q. V.
 Long-form factuality in large language models, 2024.
 URL https://arxiv.org/abs/2403.18802.
Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang,
 L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White,
 R. W., Burger, D., and Wang, C. Autogen: Enabling next-
 gen llm applications via multi-agent conversation, 2023.
 URL https://arxiv.org/abs/2308.08155.
Xu, T., Zhang, D., Mitra, K., and Hruschka, E. Verification-
  aware planning for multi-agent systems. In Demberg,
  V., Inui, K., and Marquez, L. (eds.), Proceedings of
  the 19th Conference of the European Chapter of the
 Association for Computational Linguistics (Volume 1:

                                                                 8
                           The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

A. Full Statistical Results                                                      gemini-2.5-flash vs. DeepSeek-V3.2:     212/39/50/45.
                                                                                 gemini-2.5-flash vs. Qwen3.5-397B-A17B: 236/15/65/30.
A.1. Hallucination Trajectory Distribution (Experiment                           DeepSeek-V3.2 vs. Qwen3.5-397B-A17B: 242/20/59/25.
     1, n=346)
                                                                                 A.3. Experiment 3: Five Independent Statistical Tests
 Trajectory                  Count            %     Interpretation
 ✓→✓→✓→✓                        244      70.5%      Always detected              Ours vs. Vanilla (16.2% vs. 60.7%, ∆ = −44.5 pp): Mc-
 ✓→ × → × →×                     37      10.7%      Full decay at S1 →S2 ;       Nemar χ2 = 136.10 (p < 0.000001); permutation test
                                                    permanently lost
 ✓→✓→ × →×                       31      9.0%       Decay at S2 →S3
                                                                                 p < 0.000001 (10,000 permutations); Cohen’s h = −0.958
 ✓→ × →✓→×                       11      3.2%       Intermittent                 (large effect); unpaired χ2 = 142.95 (p < 0.000001);
 ✓→✓→ × →✓                        8      2.3%       Late recovery                Fisher’s exact OR = 7.996 (p < 0.000001). McNemar
 ×→✓→✓→✓                          4      1.2%       Late detection               contingency: both survived = 47, only Vanilla survived
 ✓→ × → × →✓                      4      1.2%       Partial recovery             = 9, only Ours survived = 163, both caught = 127.
 ×→ × →✓→✓                        2      0.6%       Very late detection
 ✓→✓→✓→×                          2      0.6%       Final-stage laundering       Ours vs. End-Check (16.2% vs. 58.4%, ∆ = −42.2 pp):
 ×→ × → × →✓                      1      0.3%       Single-stage late            McNemar χ2 = 122.24 (p < 0.000001); permutation test
                                                    detection
 ×→ × → × →×                     0       0.0%       Never occurs
                                                                                 p < 0.000001 (10,000 permutations); Cohen’s h = −0.911
                                                                                 (large effect); unpaired χ2 = 129.94 (p < 0.000001);
Table 6. Hallucination trajectory distribution (Experiment 1,                    Fisher’s exact OR = 0.138 (p < 0.000001). McNemar con-
n=346). The ×→ × → × →× count is exactly zero: every hallu-                      tingency: both survived = 43, only End-Check survived
cination is detectable at S1 .
                                                                                 = 13, only Ours survived = 159, both caught = 131. All
                                                                                 five tests are mutually consistent; p-values are orders of
The all-missed trajectory count is exactly zero: every in-                       magnitude below any Bonferroni-corrected threshold.
jected hallucination is detectable at Stage 1 by at least one
instrument. The pipeline creates invisibility; the hallucina-                    A.4. Experiment 2: Detection by Injection Type
tion does not arrive invisible.
                                                                                  Model                Dollar Amount     Large Number     Percentage

A.2. Experiment 2: All Six Pairwise McNemar Tests                                 Meta-Llama-3-70B-    49.3% (133/270)   37.0% (10/27)   71.4% (35/49)
                                                                                  Instruct
     (n=346)                                                                      gemini-2.5-flash     69.6% (188/270)   55.6% (15/27)   98.0% (48/49)
                                                                                  DeepSeek-V3.2        71.1% (192/270)   85.2% (23/27)   95.9% (47/49)
 Pair                   ∆ (pp)         χ2          p-value      Cohen’s h         Qwen3.5-397B-A17B    85.6% (231/270)   81.5% (22/27)   98.0% (48/49)

 Meta-Llama-3-70B-       −21.1        44.31       <0.000001       −0.439         Table 8. Detection rates by injection type at Stage 1, Experiment 2.
 Instruct vs.                                                                    Percentage hallucinations are easiest to catch; dollar amounts are
 gemini-2.5-flash                                                                hardest, explaining the structural ceiling.
 Meta-Llama-3-70B-       −24.3        63.79       <0.000001       −0.511
 Instruct vs.
 DeepSeek-V3.2
 Meta-Llama-3-70B-       −35.5        108.64      <0.000001       −0.804         This asymmetry directly explains the structural ceiling: per-
 Instruct vs.                                                                    centage hallucinations are caught at 71–98% because a
 Qwen3.5-397B-                                                                   large additive shift is often obviously implausible; dollar
 A17B                                                                            amount hallucinations are caught at only 49–86% because
 gemini-2.5-flash vs.    −3.2          1.12         0.289         −0.073
 DeepSeek-V3.2
                                                                                 a 12.8% perturbation on a large company’s financials is en-
 gemini-2.5-flash vs.    −14.5        30.01       <0.000001       −0.365         tirely within industry-plausible range without ground truth
 Qwen3.5-397B-                                                                   access.
 A17B
 DeepSeek-V3.2 vs.       −11.3        18.28       0.000019        −0.293
 Qwen3.5-397B-                                                                   B. Injection Protocol
 A17B
                                                                                 B.1. Regex Patterns
              Table 7. All six pairwise McNemar tests.
                                                                                 Three numeric expression classes are detected and perturbed,
                                                                                 applied case-insensitively in priority order.
McNemar contingency tables (both caught / only A caught /
only B caught / both missed): Meta-Llama-3-70B-Instruct                          • Dollar amounts: patterns beginning with $ followed by
vs. gemini-2.5-flash: 156/22/95/73. Meta-Llama-3-70B-                              comma-separated digits, optional decimal, and optional
Instruct vs. DeepSeek-V3.2: 166/12/96/72. Meta-Llama-                              scale suffixes (million, billion, mn, bn, k, MM, trillion,
3-70B-Instruct vs. Qwen3.5-397B-A17B: 171/7/130/38.                                etc.)

                                                                             9
                       The Hallucination Snowball: Error Propagation in Multi-Agent LLM Pipelines

• Percentages: signed or unsigned numeric values followed
  by %, percent, percentage points, or bps
• Large numbers: non-dollar, non-percentage sequences
  of five or more digits with optional decimals

Year exclusion: values in range 1900–2099 are excluded
when surrounding context (20 chars before, 10 chars after)
contains any of: FY, FISCAL, YEAR, Q1–Q4, 10-K, 10-Q,
ANNUAL, QUARTER. Any 4-digit value in 1950–2030 is
treated as a year unconditionally.

B.2. Perturbation Rules and Seed Structure
Dollar amounts and large numbers are multiplicatively
shifted by 15–40% of their original value; percentages re-
ceive an additive shift of 3–12 percentage points. Direction
(increase or decrease) is chosen randomly per injection.
Each question receives 2–3 injections. Seeds are fully deter-
ministic: RANDOM SEED=42; primary seed per question
=     RANDOM SEED + abs(hash(question id))
% 10000; per-injection sub-seed = primary seed +
abs(hash(question id)) % 100000 + i ×
7919. Retry on no-change: re-attempts with sub-seed +
999983.

C. Infrastructure
Frameworks: Python, LangGraph (StateGraph). APIs: Ope-
nAI (gpt-4o, gpt-4o-mini), Google GenAI SDK (gemini-2.5-
flash), HuggingFace Router / Novita (Meta-Llama-3-70B-
Instruct, DeepSeek-V3.2, Qwen3.5-397B-A17B). Rate lim-
iting: 0.3-second delay between API calls (Experiment 3).
Retry logic: 3 attempts with 2-second base delay across all
experiments.




                                                                10
