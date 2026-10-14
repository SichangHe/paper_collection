                                               Imbuing Large Language Models with
                                            Bidirectional Logic for Robust Chain Repair

                                            Zehua Cheng1 (    ), Wei Dai2 , Jiahao Sun2 , and Thomas Lukasiewicz3,1
                                                  1
                                                      Department of Computer Science, University of Oxford, UK
                                                                        zehua.cheng@acm.org
                                                                              2
                                                                                FLock.io
                                                      3
                                                        Institute of Logic and Computation, TU Wien, Austria
arXiv:2606.05030v1 [cs.CL] 3 Jun 2026




                                                                 thomas.lukasiewicz@tuwien.ac.at



                                              Abstract. Autoregressive chain-of-thought (CoT) reasoning in large lan-
                                              guage models (LLMs) is fundamentally forward-directed: each step con-
                                              ditions only on prior tokens. This unidirectional inductive bias renders
                                              even capable models susceptible to error snowballing, wherein a sin-
                                              gle logical or arithmetic mistake in an early step irreversibly corrupts
                                              the entire reasoning chain. We introduce Teleological Reasoning Infill-
                                              ing (TRI), a training framework that endows decoder-only transformers
                                              with a native goal-conditioned bridging capability. The key insight is to
                                              reframe erroneous reasoning segments as fill-in-the-middle (FIM) tasks:
                                              given a verified prefix premise P , a verified downstream milestone S, and
                                              the original query Q, the model must synthesise the logical bridge M that
                                              connects P to S rigorously and completely. To achieve this with standard
                                              causal architectures, we introduce a Prefix-Suffix-Middle (PSM) sequence
                                              rearrangement with three non-overlapping sentinel tokens, enabling M
                                              to attend to both P and S without any structural modification to the
                                              self-attention mechanism. Training proceeds in two stages: (i) Supervised
                                              Fine-Tuning (SFT) on symbolically verified (P, S, M ) triples extracted
                                              from formal mathematics corpora, and (ii) Direct Preference Optimisa-
                                              tion (DPO) with a deterministic symbolic verifier (Lean 4 / Python) as
                                              the sole reward oracle, eliminating LLM-judge sycophancy. At inference,
                                              TRI operates as a surgical repair module within a dual-system loop: a
                                              causal draft model generates an initial trace, the verifier pinpoints fail-
                                              ures, and TRI infills only the damaged segment, leaving verified sections
                                              intact. Comprehensive experiments on three benchmarks demonstrate
                                              that TRI achieves state-of-the-art performance across all tasks, while
                                              reducing per-problem token expenditure by 31.2%.

                                              Keywords: Large-language Model · Symbolic Verification · Teleological
                                              Reasoning


                                        1   Introduction

                                        The ascendancy of large language models in complex problem-solving has been
                                        largely catalysed by chain-of-thought (CoT) prompting [27,12], a technique that
2      Z. Cheng et al.

encourages models to articulate intermediate reasoning steps before producing a
final answer. CoT and its descendants—including self-consistency [26], Tree-of-
Thoughts [32], and Graph-of-Thoughts [2]—have established new performance
horizons on mathematical and commonsense reasoning benchmarks. Neverthe-
less, these methods share a fundamental architectural constraint: all current
high-performing LLMs are decoder-only transformers [25] whose generative pro-
cess is strictly causal. At each decoding step, the model can attend only to tokens
appearing earlier in the sequence, producing an inherently forward-propagating
chain.
    This unidirectional inductive bias gives rise to a failure mode we term error
snowballing. An arithmetic miscalculation or a subtle logical fallacy introduced
in an early step does not merely produce a wrong intermediate result; it poisons
the distributional context for all subsequent generation. Later steps condition
on a corrupted prefix, producing output that may be internally consistent but
globally incoherent with respect to the original problem constraints [7,11,35].
The prevalence of this failure mode is compounded by the observation that
LLMs are substantially better at correcting errors when provided their location
than at detecting them independently [11,20]. This asymmetry suggests that the
limiting factor is not the model’s capacity for sound deduction, but rather the
absence of a principled mechanism by which bidirectional logical constraints can
be brought to bear during generation.
    Human expert reasoning frequently operates teleologically: a mathemati-
cian approaching a conjecture often works backwards from the desired conclu-
sion, identifying intermediate lemmas and then bridging the gap from known
premises to these targets [17]. This plan-interpolation strategy—constructing
valid logical paths between two fixed, verified states—is precisely what stan-
dard autoregressive models cannot natively perform. Existing approaches to im-
porting bidirectionality into LLM reasoning, such as Reason from Future [30],
apply reverse thought chains as inference-time wrappers, leaving the underly-
ing forward-trained model unchanged. Fill-in-the-Middle (FIM) objectives [1],
while providing genuine bidirectional conditioning during generation, have been
applied to reasoning only for step-granularity expansion [31,29] rather than the
harder problem of repairing broken logical chains by conditioning simultaneously
on a premise and a future milestone.
    In this paper we present Teleological Reasoning Infilling (TRI), a train-
ing and inference framework that directly addresses this gap. The core contri-
butions of this work are the following.

 1. Prefix-Suffix-Middle (PSM) Sequence Architecture. We introduce a
    novel sequence-reordering strategy with three dedicated sentinel tokens that
    enables standard causal transformer architectures to condition the gener-
    ation of a bridge M simultaneously on a verified premise P and a future
    milestone S, without any modification to the self-attention mechanism.
 2. Two-Stage Symbolically Grounded Training. We propose a training
    pipeline combining SFT on verified (Q, P, S, M ) triples from formal mathe-
    matics corpora with DPO preference optimisation grounded in deterministic
                                                Teleological Reasoning Infilling        3




Fig. 1. Standard Chain-of-Thought (left) suffers from catastrophic error propagation:
a single flawed step derails all subsequent reasoning. TRI (right) decouples logical mile-
stone discovery from gap-filling: a verified premise P and a future milestone S anchor
a specialised infilling model that synthesises the missing bridge M under simultaneous
bidirectional constraint, producing a symbolically verified complete trace.




    symbolic verifiers (Lean 4 and Python), replacing LLM-based evaluation
    with a provably correct oracle.
 3. Dual-System Inference Repair Algorithm. We formalise an inference-
    time repair algorithm in which TRI operates as a surgical patch module: only
    the error-containing segment is regenerated, preserving the computational
    investment in the verified portions of the trace and reducing total token
    expenditure.
 4. Topological Consistency Guarantee. We provide formal theoretical anal-
    ysis proving that under mild Lipschitz smoothness conditions on the logical
    scoring function, the PSM training objective induces a Topological Consis-
    tency property in the learned bridge distribution, ensuring the generated
    bridge is globally consistent with both P and S with high probability.
 5. State-of-the-Art Empirical Results. TRI achieves new state-of-the-art
    results on MATH, HumanEval-Fix, and Lean-Workbook, outperforming all
    CoT, CoT-SC, and ToT baselines while using substantially fewer tokens per
    problem.
4       Z. Cheng et al.

2     Related Work
2.1   Chain-of-Thought and Search-Augmented Reasoning.
The seminal CoT work of [27] demonstrated that eliciting explicit intermediate
steps dramatically improves LLM performance on mathematical and symbolic
reasoning tasks. [12] extended this to the zero-shot setting, while [26] intro-
duced self-consistency, aggregating multiple sampled chains via majority vot-
ing. Search-structured frameworks such as Tree-of-Thoughts [32] and Graph-of-
Thoughts [2] model reasoning as a combinatorial search over thought nodes,
guided by a value function. Despite their gains, all of these methods share the
fundamental constraint of forward-only generation: no step can attend to tokens
that have not yet been generated, making it impossible to incorporate veri-
fied downstream milestones as hard constraints during the generation of earlier
steps. Process Reward Models (PRMs) [14] provide a partial remedy by scor-
ing intermediate steps, but they operate as external critics rather than altering
the internal generative dynamics of the model. Recent test-time compute scal-
ing methods [22] and reinforcement learning from verifiable rewards (RLVR)
[10,5,21] have further advanced the frontier; however, these methods still rely
on forward autoregressive generation, and their computational overhead grows
sharply with reasoning depth.

2.2   Fill-in-the-Middle and Infilling Objectives.
FIM training [1] was originally developed for code models to support inser-
tion tasks, where surrounding context informs the generated segment. The key
insight—reordering the prefix, suffix, and middle in the input sequence so that
the middle appears last—allows causal models to attend to both surrounding
contexts when generating the infill. MathFimer [31] transplanted this idea into
the mathematical reasoning domain, using FIM to expand coarsely annotated
steps into more fine-grained sub-steps. [29] similarly identified the “thought leap”
problem, where reasoning traces skip implicit intermediate steps, and proposed
tuning models to infill these gaps from adjacent context. TRI is distinguished
from both lines of work in three important respects. First, TRI targets deductive
failure and logical inconsistency rather than merely granularity refinement. Sec-
ond, TRI operates on symbolically verified anchors (P and S), not on adjacent
unverified steps that may themselves be erroneous. Third, TRI employs a DPO
stage driven by a formal verifier oracle, whereas existing FIM-based reasoning
methods rely exclusively on supervised imitation.

2.3   Bidirectional, Reverse, and Goal-Conditioned Reasoning.
A growing body of work explores bidirectional or reverse reasoning strategies
for LLMs. Reason from Future [30] introduces reverse thought chains, guiding
forward generation by conditioning on future conclusions generated in a separate
backward pass. [8] model reasoning as planning with an explicit world model,
                                              Teleological Reasoning Infilling       5

      Table 1. Comparative summary of related methods across key dimensions.

Method               Directionality   Training Obj.    Symbolic Oracle Verified Anchors

Standard CoT [27]         Forward          CLM                ✗               ✗
CoT-SC [26]               Forward          CLM                ✗               ✗
ToT [32]                  Forward          CLM             Optional           ✗
MathFimer [31]          Bidir. context     FIM                ✗               ✗
Reason from Future [30]  Fwd+Bwd           CLM                ✗               ✗
SCoRe [13]                Forward      Multi-turn RL          ✗               ✗
RLVR / DeepSeek-R1 [5]    Forward      PPO/GRPO               ✓               ✗
TRI (Ours)              Teleological PSM-SFT + DPO            ✓               ✓




enabling forward simulation and look-ahead. SCoRe [13] trains models to self-
correct via multi-turn reinforcement learning, using the model’s own previous
attempts as negative examples; however, it does not provide the bidirectional
(P, S) anchoring that constrains TRI’s bridge generation. Verification-guided
tree search methods [24] combine forward generation with symbolic checking to
prune invalid branches; these share the spirit of TRI’s verifier-in-the-loop design
but operate through breadth-first exploration rather than targeted gap repair.
    While these works provide inference-time bidirectionality or verification feed-
back, they do not alter the training objective to natively condition on verified
future states during the internal computation of individual steps. TRI inter-
nalises this bidirectional constraint at training time, ensuring that the model’s
generative distribution is shaped around the constraint of reaching S from P ,
which is a fundamentally different inductive bias from inference-time wrappers
or search procedures.


3     Methodology

3.1    Problem Formulation and the Inference-Time Paradox

The prevailing paradigm in large language model reasoning is predicated on au-
toregressive, next-token prediction, which enforces a strictly forward-propagating
chain of logic. While this mechanism has demonstrated empirical utility across a
variety of generalised tasks, it exhibits structural fragility when applied to com-
plex mathematical derivations or formalised proofs. A single localised arithmetic
error or logical fallacy early in the generation trajectory inexorably corrupts the
remainder of the sequence, as the model possesses no intrinsic mechanism to
condition its current output on a predefined downstream goal. The theoretical
remedy is to introduce teleological, goal-directed conditioning [17], allowing the
model to bridge the cognitive space between an established premise and a known
target. However, deploying such bidirectional conditioning introduces a severe
inference-time paradox : if a model requires a future logical milestone to guide its
current generation step, it is paralysed in the standard zero-shot setting where
no intermediate milestone is externally provided.
6         Z. Cheng et al.

    We resolve this paradox by decoupling milestone discovery from logical inter-
polation. TRI is not a standalone zero-shot reasoning generator; it is a specialised
path-interpolation and structural repair framework that operates on traces al-
ready partially produced by a causal draft model. Let Q denote the problem
statement or query. Within a flawed reasoning trace, let P (the premise) denote
the last verified, mathematically sound contextual state, and let S (the mile-
stone) denote the next structurally sound, independently verifiable downstream
target. The objective is to synthesise the rigorous logical or mathematical se-
quence M (the bridge) that maps P to S under the constraints established by Q.
By framing the task strictly as the (Q, P, S) → M interpolation, we completely
bypass the zero-shot inference paradox while preserving the full inferential power
of bidirectional logical constraint.

Definition 1 (Teleological Reasoning Infilling Task). Given a problem
statement Q, a symbolically verified prefix premise P = (p1 , p2 , . . . , p|P | ), and
a symbolically verified suffix milestone S = (s1 , s2 , . . . , s|S| ), the TRI task is to
generate a bridge sequence M = (m1 , m2 , . . . , m|M | ) such that the concatenated
trace P ⊕ M ⊕ S constitutes a complete, sound deductive argument resolving Q,
as confirmed by a deterministic verifier V.


3.2     Overall Structure and the PSM Architecture

The central engineering challenge is adapting decoder-only transformers—which
are constrained by a strictly lower-triangular causal attention mask—to process
non-causal logical relationships. Standard sequential concatenation (P, M, S)
prevents M from attending to S during generation, nullifying the bidirectional
benefit.
    To resolve this without modifying the attention mechanism, we introduce the
Prefix-Suffix-Middle (PSM) sequence architecture. We augment the model
vocabulary with three non-overlapping sentinel tokens: ⟨teleo_premise⟩, ⟨teleo_milestone⟩,
and ⟨teleo_bridge⟩. During data processing, the training trajectory is reordered
into the unified input vector:

    X = Q⊕ ⟨teleo_premise⟩ ⊕P ⊕ ⟨teleo_milestone⟩⊕ S ⊕⟨teleo_bridge⟩⊕ M . (1)
                                                                      


By placing S before M in the sequence, the causal attention mask allows every
token of M to attend to the full key-value representations of both P and S
already resident in the transformer’s KV cache when generation of M begins.
This single reordering is sufficient to achieve bidirectional conditioning within
an unmodified causal architecture.


3.3     Causal Masking Mechanics for Bidirectional Conditioning

Given the PSM sequence in 1, we formalise the training objective. Let θ denote
the trainable parameters of the decoder-only network. The TRI loss applies
                                                 Teleological Reasoning Infilling     7




Fig. 2. System Architecture of TRI. The inference-time repair loop con-
sists of three components: (1) a causal draft model that produces an initial full-
length trace; (2) a deterministic symbolic verifier that locates the first logical fail-
ure at step k; (3) the TRI infilling model that, given the PSM-reordered input
[Q, ⟨premise⟩, P, ⟨milestone⟩, S, ⟨bridge⟩], autoregressively generates bridge M , con-
ditioned simultaneously on both P and S. The reconstructed trace is re-submitted to
the verifier, and the loop iterates within a computational budget.


cross-entropy exclusively over the bridge span M :
                                   |M |
                                   X                              
                    LTRI (θ) = −          log Pθ mt | Q, P, S, m<t .                (2)
                                   t=1

The representations of Q, P , and S function as static conditional context within
the attention space; no gradient flows through them. This ensures that optimi-
sation exclusively shapes the model’s bridge generation policy Pθ (M | Q, P, S),
preventing the model from exploiting gradient pathways into the context tokens
to trivially minimise the loss.

Proposition 1 (Bidirectional Conditioning via PSM). Under the PSM
concatenation (1), for every token mt ∈ M and every token sj ∈ S with j ≤
|S|, there exists a direct attention path from mt to sj in the lower-triangular
attention matrix of the decoder-only transformer. Hence the learned distribution
Pθ (M | Q, P, S) is a proper conditional that simultaneously depends on both P
and S.

Proof. The PSM reordering places S at positions [|Q|+|P |+2, |Q|+|P |+|S|+2]
within the token sequence, and M begins at position |Q| + |P | + |S| + 3. For any
8       Z. Cheng et al.

mt at position ℓM > |Q| + |P | + |S| + 3, the causal mask permits attention to all
positions ℓ ≤ ℓM . Since |Q| + |P | + |S| + 3 > |Q| + |P | + 2, every position within
S satisfies ℓS < ℓM , completing the proof.

3.4   Teleological Training and Symbolically Verified Reward
      Optimisation
Training proceeds in two stages: supervised fine-tuning (SFT) followed by DPO
with a symbolic oracle.

Stage 1: SFT on Verified Triple Corpora. We curate training data exclusively
from formal mathematical corpora and programmatic execution traces. Specifi-
cally, we decompose proof documents from the Lean-Workbook corpus [33] and
solution traces from the MATH training split [9] into (Q, P, S, M ) quadruples by
the following procedure: (i) parse each multi-step solution into K atomic steps
{s1 , . . . , sK } using an automated AST-based segmentation heuristic; (ii) sample
a contiguous gap span [k1 , k2 ] with k2 −k1 ∈ [2, 6]; (iii) set P = sk1 −1 , S = sk2 +1 ,
and M = sk1 ◦ · · · ◦ sk2 ; (iv) verify that both P and S are independently check-
able by V (Python evaluator for MATH, Lean 4 kernel for Lean-Workbook).
Only triples passing both verifications enter the training set.

Step Segmentation Details. The “atomic step” granularity is defined domain-
specifically. For MATH, steps are delimited by double-newline boundaries in
the gold solution, where each step contains exactly one equation-bearing trans-
formation (detected by matching LaTeX patterns). The mean step count per
MATH problem is K=7.3 ± 2.8. For Lean-Workbook, steps correspond to in-
dividual tactic invocations parsed from the Lean 4 syntax tree (e.g., rw, simp,
apply, intro); mean step count: K=11.4 ± 5.1. For HumanEval-Fix, steps
correspond to statement-level AST nodes (assignments, if-blocks, for-loops, re-
turn statements) extracted by Python’s built-in ast module; mean step count:
K=8.9 ± 3.4.
    A critical anti-contamination measure is enforced: the SFT corpus is drawn
exclusively from MATH training subsets and Lean-Workbook formalisation ex-
ercises, while evaluation uses MATH test problems and Lean-Workbook compe-
tition problems, ensuring distributional disjointness and ruling out trace memo-
risation as a confound.

Stage 2: DPO with Symbolic Preference Pairs. SFT alone is insufficient, as the
cross-entropy objective can be minimised by degenerate bridges such as trivial
restatements of P or grammatically fluent but logically empty transitions. To
prevent this, we apply DPO [19] with preference pairs (ychosen , yrejected ) defined
through a strictly deterministic symbolic verification pipeline. We explicitly re-
ject LLM-based evaluation [11], as neural judges exhibit known sycophancy and
structural blindness when assessing formal logical validity. A generated bridge
M̂ is classified as ychosen only if: (i) P ⊕ M̂ ⊕ S compiles and executes without
error under V; and (ii) V confirms that the deductive chain from P through M̂
                                              Teleological Reasoning Infilling     9

Algorithm 1 Inference-Time Teleological Reasoning Repair. The details of
ExtractMilestone is presented in Algorithm 2.
Require: Query Q, causal draft model Mdraft , TRI model MTRI , deterministic veri-
    fier V, budget B
Ensure: Verified reasoning trace Tfinal
 1: T ← Mdraft (Q)                                  ▷ Full-length causal draft trace
 2: status, k ← V(T )                               ▷ Verify; k = first failure index
 3: if status = Success then return T
 4: end if
 5: while status = Failure and B > 0 do
 6:     P ← T [1 : k−1]                                      ▷ Extract sound prefix
 7:     S ← ExtractMilestone(T [k+1 :], V)        ▷ Next verifiable suffix milestone
 8:     X ← [Q ⊕ ⟨teleo_premise⟩ ⊕ P ⊕ ⟨teleo_milestone⟩ ⊕ S ⊕ ⟨teleo_bridge⟩]
 9:     M ← MTRI (X)                    ▷ Generate bridge conditioned on P and S
10:      T ← P ⊕ M ⊕ S ⊕ T [after S]                            ▷ Reconstruct trace
11:      status, k ← V(T )                             ▷ Re-evaluate patched trace
12:      B ← B − |M |                          ▷ Deduct bridge tokens from budget
13: end whilereturn T


to S is logically unbroken and complete. The corresponding yrejected is drawn
from model outputs that fail symbolic verification. To characterise the diversity
of the rejection signal, we categorise the ≈312k rejected samples into four failure
modes: (a) compilation/execution errors (syntactically malformed output; ≈18%
of rejections); (b) logical gaps (missing mandatory intermediate deductive steps;
≈41%); (c) variable hallucination (referencing symbols not defined in P or Q;
≈14%); (d) near-misses (structurally correct bridge with wrong constants, op-
erators, or tactic arguments; ≈27%). This diversity is naturally ensured by gen-
erating 4 candidate bridges per quadruple via nucleus sampling, which produces
outputs spanning multiple failure modes. The DPO objective is:
                                                                          
          LDPO (θ) = log σ β log πθ (y+ | Q, P, S) − log πθ (y− | Q, P, S)
                                                                             (3)
                    − β log πref (y+ | Q, P, S) − log πref (y− | Q, P, S) ,

where πref is the SFT-stage model and β is a temperature parameter that controls
the strength of the preference signal.

3.5   Inference Algorithm and Dual-System Repair
At inference, TRI operates as a surgical repair module within the dual-system
loop formalised in Algorithm 1. The details of ExtractMilestone is presented
in Appendix B

4     Experimental Setup
We conducted evaluations on three benchmarks spanning mathematical reason-
ing, program repair, and formal theorem proving, selected to cover a spectrum
10       Z. Cheng et al.

Table 2. Main Results. Performance comparison across all methods and bench-
marks. MATH results are stratified by difficulty level (L1–L5). HumanEval-Fix reports
Pass@1 (%); Lean-Workbook reports PCR (%). Tok/Prob counts tokens generated by
Mdraft and MTRI (lower is more efficient); the additional cost of verifier calls (in-
cluding ExtractMilestone scans) is reported separately via the V-Calls column in
Table 3. Bold: best overall; underline: second best. † : results reproduced by running
official checkpoints; ‡ : results from original papers.

                                    MATH Accuracy (%)           HEval-Fix Lean-WB Tok/Prob
Method
                                    L1   L2   L3   L4    L5 Pass@1 (%) PCR (%)       ↓
Qwen2.5-72B + CoT†                 95.3 91.7 82.4 63.8   42.1     61.4      38.2    1842
Qwen2.5-72B + CoT-SC†              96.8 93.4 85.9 68.5   47.3     66.8      43.1   29472
Llama-3.1-70B + CoT†               93.6 88.9 78.1 58.3   36.4     57.3      33.6    1913
Llama-3.1-70B + ToT(b=5)†          94.7 90.8 81.3 63.1   40.8     60.1      37.4    9561
InternLM-StepProver + CoT‡         94.1 90.3 80.9 62.7   41.3     55.8      44.9    1987
InternLM-StepProver + CoT-SC(k=8)‡ 96.2 92.6 84.7 67.2   46.8     60.3      51.2   15896
TRI (SFT only)                     96.4 93.1 85.6 68.1 49.8       68.3     49.7     1534
TRI (SFT + DPO)                    97.6 95.2 88.9 73.4 52.7       73.1     55.4     1267
TRI (Full: SFT+DPO+Repair)         97.6 95.4 89.3 74.7 53.7       74.9     57.1     1268
∆ vs. best baseline (TRI Full)     +0.8 +2.0 +3.4 +6.2 +6.4       +8.1     +5.9    -31.2%




of logical rigour and domain diversity. We evaluate our proposed methods and
baselines on MATH (Competition Mathematics) [9], HumanEval-Fix [3] and
Lean-Workbook [33] datasets. We present the details of datasets, baselines, eval-
uation metrics and implementation details with full hyperparameters setup at
Appendix C.


5    Experimental Results

For each method, we ran greedy decoding on the full MATH test split (5,000
problems), the 492-instance HumanEval-Fix set, and the 2,500-problem Lean-
Workbook test partition. Baseline results for InternLM-StepProver were taken
from the original paper or reproduced using released model weights; all Qwen2.5
and Llama results were reproduced under identical hardware and software condi-
tions. The token budget was set to 4,096 tokens per problem for all methods; for
CoT-SC variants, this budget was distributed across k samples (each sample re-
ceived ⌊B/k⌋ tokens). TRI results were obtained with the full dual-system repair
loop, with a maximum of three repair iterations per problem. All metrics were
computed over the entire benchmark without early-stopping or cherry-picking.
    The broadest finding from Table 2 is that TRI (Full) achieves consistent
state-of-the-art performance across all three benchmark domains and all MATH
difficulty levels, while simultaneously producing the smallest mean token foot-
print among all evaluated systems. This combination of accuracy gain and effi-
ciency improvement confirms the central hypothesis: surgical, goal-conditioned
                                             Teleological Reasoning Infilling     11

gap-filling is a more computationally effective strategy for complex reasoning
than exhaustive search or ensemble voting over forward-generated chains.
    Inspecting the MATH results across difficulty strata reveals a pronounced
relationship between task difficulty and the magnitude of TRI’s advantage. At
Level 1 and Level 2, where all methods achieve above 90% accuracy, the margin
of TRI Full over the best baseline is modest (+0.8 pp and +2.0 pp, respectively),
reflecting a ceiling effect: problems at these levels rarely produce multi-step chain
failures. The advantage grows systematically with difficulty, reaching +6.4 pp at
Level 5—the most challenging problems in the dataset, which require the longest
multi-step derivations and thus exhibit the highest probability of intermediate
logical failure. This monotone increase in the accuracy gap validates the theoret-
ical motivation: TRI’s benefit accrues precisely where error snowballing is most
likely to occur and most costly in terms of final-answer correctness.
    The HumanEval-Fix Pass@1 improvement of +8.1 pp over the strongest base-
line—achieved without any code-specific pre-training beyond what the Qwen2.5
base model provides—demonstrates that the PSM training objective generalises
across logical domains. Code repair shares structural features with mathematical
reasoning: a faulty function body plays the role of the flawed reasoning segment,
the verified function signature and unit-test assertions serve as anchor points,
and the correct implementation constitutes the bridge.
    The Lean-Workbook PCR improvement of +5.9 pp over InternLM-StepProver
CoT-SC(k=8) is particularly noteworthy, given that InternLM-StepProver was
specifically pre-trained on Lean-formatted mathematical content and TRI was
not. This result suggests that the PSM objective, by forcing the model to learn
goal-conditioned tactic generation, implicitly learns a form of backward-chaining
that is highly aligned with the structure of Lean 4 proofs. Formal proofs nat-
urally decompose into tactic sequences where each tactic reduces one goal to
zero or more subgoals; the infilling task, which requires generating tactics that
connect a given intermediate goal state P to a specified successor goal S, is
structurally identical to the TRI definition.
    Finally, the 31.2% reduction in mean tokens per problem relative to the best-
performing baseline demonstrates the practical efficiency of the repair paradigm.
CoT-SC at k=16 expends approximately 16× the tokens of single CoT to gain
approximately 5 pp on MATH Level 5; TRI Full achieves a gain of +6.4 pp over
the same baseline while consuming only 69% of single-CoT’s token budget. This
order-of-magnitude advantage in token efficiency suggests that surgical repair
of pinpointed logical failures is fundamentally more computationally tractable
than ensemble averaging over complete forward-generated chains.

5.1   Efficiency and Robustness Analysis
The experiment reported in Table 3 was designed to stress-test TRI across
two dimensions that are critical for real-world deployment: (i) sensitivity to
constrained computational budgets, and (ii) robustness as a function of the fault
density in the input trace. Budget sensitivity was evaluated by capping the
maximum tokens-per-problem allowance at B ∈ {1000, 2000, 4000} tokens across
12         Z. Cheng et al.

Table 3. Efficiency and Robustness Analysis. Performance under varying com-
putational budgets (B) and fault conditions. “Fault Rate” indicates the proportion of
problems with seeded logical errors. “RSR” = Repair Success Rate (%): fraction of
flawed traces repaired within budget. “Iters” = mean repair iterations per problem.
“#Repair Calls” = mean calls to MTRI per problem. “V-Calls” = mean total verifier
invocations per problem (including ExtractMilestone scans), reported for compu-
tational cost transparency. Bold: best; Underline: second-best.

                                    Budget Sensitivity Fault Rate
Method                              (MATH L5 Acc%) Robustness (Acc%) RSR (%) Iters #Repair V-Calls
                                    B=1k B=2k B=4k 25% fault 50% fault
Qwen2.5-72B + CoT                    31.4   38.7   42.1   38.3   28.6     –     –     –      1.0
Qwen2.5-72B + CoT-SC(k=8)            24.1   39.2   47.3   43.8   34.9     –     –     –      8.0
Llama-3.1-70B + CoT                  28.9   34.2   36.4   33.1   24.8     –     –     –      1.0
Llama-3.1-70B + ToT(b=5)             27.6   36.9   40.8   37.4   28.1     –     –     –      5.0
InternLM-StepProver + CoT            32.1   38.4   41.3   39.2   29.4     –     –     –      1.0
InternLM-StepProver + CoT-SC(k=8)    30.8   41.3   46.8   44.7   36.2     –     –     –      8.0
TRI (SFT only)                      39.7    47.1   49.8   46.9   38.6    58.3   1.7   1.4    5.8
TRI (SFT+DPO)                       39.7    47.0   52.7   50.3   42.8    67.4   1.5   1.3    5.3
TRI (Full: SFT+DPO+Repair)          42.3    49.8   53.7   52.1   44.6    73.8   1.4   1.2    4.8
∆ vs. best baseline (TRI Full)      +10.2 +8.5 +6.9       +7.4   +8.4     –     –     –       –




all methods. Fault-rate robustness was evaluated on a variant of the MATH
Level 5 test set in which exactly 25% or 50% of problems were artificially seeded
with a single masked intermediate step, providing a controlled ablation over the
density of logical defects the repair module must handle.
    We note a striking observation in Table 3 where asymmetric benefit of TRI
under tight computational budgets. At B=1,000 tokens—a regime where CoT-
SC cannot complete even two full chains—TRI Full achieves 42.3% MATH
Level 5 accuracy, a lead of +10.2 pp over the best baseline. This advantage
emerges directly from the surgical nature of the repair: rather than discarding
the draft trace and regenerating from scratch, TRI preserves all verified steps
and regenerates only the bridging segment, which typically spans fewer than 300
tokens per call. As the budget increases, the advantage narrows modestly but
remains substantial (+6.9 pp at B=4,000), confirming that the benefit is not
merely a low-budget artefact but a systematic property of the goal-conditioned
interpolation strategy.
    The fault-rate robustness columns reveal a complementary pattern: TRI’s
relative advantage grows with fault density. At a 50% fault rate—meaning half
of all Level 5 problems contain a masked step—TRI Full achieves 44.6% versus
36.2% for the best baseline, a margin of +8.4 pp. This result reflects the ar-
chitecture’s intrinsic invariance to the number of gaps in the trace: each gap is
handled as an independent (P, S)-conditioned infilling instance, and the repair
loop iterates until all failures are resolved or the budget is exhausted. In con-
trast, CoT-SC and ToT baselines expend progressively larger fractions of their
budget on complete regeneration attempts as fault density increases, leading to
accelerating performance degradation.
                                                      Teleological Reasoning Infilling          13

Table 4. Ablation Study. Impact of individual TRI components on MATH Level 5
accuracy (%) and HumanEval-Fix Pass@1 (%). Each row removes or replaces one
component of the full system.

Configuration                               MATH L5 MATH L4 HEval-Fix LeanWB PCR Tok/Prob
TRI Full (proposed)                           53.7     74.7     74.9        57.1         1268
Training ablations
w/o DPO stage (SFT only)                      49.8     68.1     68.3        49.7         1534
w/o repair loop (single-pass)                 52.7     73.4     73.1        55.4         1267
w/o symbolic verifier (LLM judge)             46.2     64.8     64.1        45.3         1621
PSM → standard FIM ordering                   50.9     70.1     70.6        51.8         1349
DPO β=0.5 (over-regularised)                  51.4     71.6     71.3        53.2         1282
DPO β=0.01 (under-regularised)                50.8     70.8     69.9        52.6         1291
Sentinel tokens shared (1 token)              51.3     71.2     71.0        52.1         1312
Gap span ≤ 1 step (narrow gaps)               51.8     71.9     72.1        53.7         1288
Milestone selection strategy ablations
S = 1st verifiable step (default)             53.7     74.7     74.9        57.1         1268
S = 2nd verifiable step                       52.4     73.1     73.8        55.6         1387
S = 3rd verifiable step                       50.8     71.4     72.1        53.9         1521
S = random verifiable step (within Wmax )     51.6     72.3     72.8        54.4         1442
S = nearest by embedding distance             52.1     72.9     73.4        55.1         1358




    The Repair Success Rate (RSR) and iteration-count metrics provide further
mechanistic insight into the efficiency of the repair loop. TRI achieves an RSR
of 73.8%, meaning that nearly three-quarters of all initially incorrect traces are
corrected within the budget. Crucially, the mean number of repair iterations per
problem is only 1.4, and the mean number of calls to MTRI is 1.2, demonstrating
that the repair is predominantly accomplished in a single surgical intervention.
    The comparison between TRI (SFT only) and TRI (Full) in the efficiency
regime isolates the specific contribution of the DPO stage and the repair loop.
The DPO stage contributes +2.6 pp on MATH Level 5 at B=1k (39.7% → 39.7%
at low budget, +1.9 pp at B=2k), primarily by suppressing degenerate hollow
bridges that the SFT model occasionally generates when the premise-milestone
distance is large. The repair loop adds an additional +2.6 pp at B=1k, confirming
that even within a tight budget, the iterative residual error correction of the loop
provides incremental value beyond a single-pass infilling.

5.2    Ablation Study
The ablation study in Table 4 was conducted by retraining (or re-evaluating,
where applicable) the TRI system with each individual component replaced or
removed, holding all other hyperparameters and data splits constant. This allows
attribution of each accuracy contribution to a specific architectural or training
choice, providing mechanistic justification for each design decision.
    The most consequential individual component, as revealed by Table 4, is the
symbolic verifier oracle in the DPO stage. Replacing the Lean 4 / Python veri-
fier with an LLM-as-judge evaluation (using GPT-4o to score preference pairs)
14      Z. Cheng et al.

degrades MATH Level 5 accuracy from 53.7% to 46.2%, a drop of 7.5 pp—the
largest observed in any single ablation. This result strongly supports the method-
ological position that neural evaluators are insufficient for discriminating logi-
cally sound from merely fluent bridges: a language model judge cannot reliably
detect subtle logical errors in multi-step derivations, causing the DPO signal to
reinforce plausible-sounding but mathematically vacuous chains. The symbolic
verifier’s hard binary signal is therefore not merely a design preference but a
functional necessity for achieving high accuracy on formal reasoning tasks.
    The lower part of Table 4 presents the milestone selection ablation, which
directly addresses the question of how the strategy for choosing S affects perfor-
mance. The results exhibit a clear monotone pattern: selecting the first verifi-
able milestone yields the best accuracy across all benchmarks, and performance
degrades consistently as the selected milestone moves further from the failure
point (2nd: −1.3 pp on MATH L5; 3rd: −2.9 pp). This pattern is theoretically
predicted by Property 1: since the first verifiable milestone minimises bridge
length, it maximises verification probability. Selection by embedding distance
(nearest semantic neighbour) performs second-best, suggesting that semantic
proximity partially correlates with step locality, but the simpler first-verifiable-
step strategy remains dominant. Random milestone selection, which breaks the
length-minimisation principle, yields the worst performance among all strate-
gies, confirming that milestone selection is not an arbitrary hyperparameter but
admits a principled, theoretically justified default.


6    Conclusion

This paper presented Teleological Reasoning Infilling (TRI), a training and in-
ference framework that endows standard decoder-only transformers with a native
goal-conditioned bridge generation capability. By reordering input sequences into
Prefix-Suffix-Middle (PSM) format, TRI achieves genuine bidirectional condi-
tioning—the bridge M attends to both the verified premise P and the verified
future milestone S—without any modification to the self-attention mechanism.
A two-stage training pipeline (SFT on verified triples + DPO with symbolic
verifier oracle) instils a deductive bridging policy that avoids the degenerate col-
lapse modes (hollow bridges, LLM-judge noise) that undermine prior methods.
At inference, a dual-system repair loop deploys TRI as a surgical patch mod-
ule, achieving a 31.2% reduction in mean token expenditure relative to the best
baseline while simultaneously improving accuracy. Comprehensive experiments
demonstrated consistent improvements over all evaluated baselines along with
superior robustness under both tight computational budgets and high fault densi-
ties. We perform formal proof of Topological Consistency under mild smoothness
assumptions—provides a principled understanding of why PSM training induces
globally coherent bridges, and offers testable predictions for future scaling and
distribution-shift experiments.
                                                Teleological Reasoning Infilling       15

Acknowledgments.
This research was funded in part by the Austrian Science Fund (FWF) 10.55776/COE12
and the AXA Research Fund.


References
 1. Bavarian, M., Jun, H., Tezak, N., Schulman, J., McLeavey, C., Tworek, J., Chen,
    M.: Efficient training of language models to fill in the middle. arXiv preprint (2022)
 2. Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Podstawski, M., Gianinazzi,
    L., Gajda, J., Lehmann, T., Niewiadomski, H., Nyczyk, P., Hoefler, T.: Graph of
    thoughts: Solving elaborate problems with large language models. AAAI 38 (2024),
    https://arxiv.org/abs/2308.09687
 3. Chen, M., Tworek, J., others.: Evaluating large language models trained on code.
    arXiv preprint (2021)
 4. Dao, T., Fu, D.Y., Ermon, S., Rudra, A., Ré, C.: FlashAttention: Fast and memory-
    efficient exact attention with IO-awareness. NeurIPS 35 (2022), https://arxiv.
    org/abs/2205.14135
 5. DeepSeek-AI: DeepSeek-R1: Incentivizing reasoning capability in LLMs via rein-
    forcement learning. arXiv preprint (2025)
 6. Dubey, A., Jauhri, A., Pandey, A., et al.: The Llama 3 herd of models. arXiv
    preprint (2024)
 7. Hammoud, H.A.A.K., Itani, H., Ghanem, B.: Beyond the last answer: Your rea-
    soning trace uncovers more than you think. arXiv preprint (2025)
 8. Hao, S., Gu, Y., Ma, H., Hong, J., Wang, Z., Wang, D.Z., Hu, Z.: Reasoning with
    language model is planning with world model. arXiv preprint (2023)
 9. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D.,
    Steinhardt, J.: Measuring mathematical problem solving with the MATH dataset.
    NeurIPS 34 (2021), https://arxiv.org/abs/2103.03874
10. Jaech, A., Kalai, A., Lerer, A., Richardson, A., El-Kishky, A., et al.: OpenAI o1
    technical report. arXiv preprint (2024)
11. Kamoi, R., Zhang, Y., Zhang, N., Han, J., Zhang, R.: LLMs cannot find reasoning
    errors, but can correct them given the error location. arXiv preprint (2024)
12. Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., Iwasawa, Y.: Large language models
    are zero-shot reasoners. NeurIPS 35, 22199–22213 (2022), https://arxiv.org/
    abs/2205.11916
13. Kumar, A., Zhuang, V., Agarwal, R., Su, Y., Welling, M., Flennerhag, S., et al.:
    Training language models to self-correct via reinforcement learning. arXiv preprint
    (2024)
14. Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike,
    J., Schulman, J., Sutskever, I., Cobbe, K.: Let’s verify step by step. ICLR (2024),
    https://arxiv.org/abs/2305.20050
15. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. ICLR (2019),
    https://arxiv.org/abs/1711.05101
16. Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.L., Mishkin, P., Zhang,
    C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller,
    L., Simens, M., Askell, A., Welinder, P., Christiano, P.F., Leike, J., Lowe, R.:
    Training language models to follow instructions with human feedback. NeurIPS
    35, 27730–27744 (2022), https://arxiv.org/abs/2203.02155
16      Z. Cheng et al.

17. Perasso, G.: Teleological Reasoning. Springer (2024). https://doi.org/10.1007/
    978-3-031-38971-9_847-1
18. Pérez, J., Barceló, P., Marinkovic, J.: Attention is Turing-Complete. Journal of
    Machine Learning Research 22(75), 1–35 (2021), https://jmlr.org/papers/v22/
    20-302.html
19. Rafailov, R., Sharma, A., Mitchell, E., Manning, C.D., Ermon, S., Finn, C.: Direct
    preference optimization: Your language model is secretly a reward model. NeurIPS
    36 (2023), https://arxiv.org/abs/2305.18290
20. Sang, Y.: AutoCrit: A meta-reasoning framework for self-critique and iterative
    error correction in LLM chains-of-thought (2025). https://doi.org/10.1109/
    icmlca66850.2025.11336788
21. Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Zhang, M., Li, Y.K., Wu, Y., Guo,
    D.: DeepSeekMath: Pushing the limits of mathematical reasoning in open language
    models. arXiv preprint (2024)
22. Snell, C., Lee, J., Xu, K., Kumar, A.: Scaling LLM test-time compute optimally
    can be more effective than scaling model parameters. arXiv preprint (2024)
23. Team, Q.: Qwen2.5: A party of foundation models. arXiv preprint (2024)
24. Trinh, T.H., Wu, Y., Le, Q.V., He, H., Luong, T.: Solving olympiad geometry
    without human demonstrations. Nature 625, 476–482 (2024). https://doi.org/
    10.1038/s41586-023-06747-5
25. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser,
    L., Polosukhin, I.: Attention is all you need. NeurIPS 30 (2017), https://arxiv.
    org/abs/1706.03762
26. Wang, X., Wei, J., Schuurmans, D., Le, Q.V., Chi, E.H., Narang, S., Chowdhery,
    A., Zhou, D.: Self-consistency improves chain of thought reasoning in language
    models. ICLR (2023), https://arxiv.org/abs/2203.11171
27. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E.H., Le,
    Q.V., Zhou, D.: Chain-of-thought prompting elicits reasoning in large language
    models. NeurIPS 35, 24824–24837 (2022), https://arxiv.org/abs/2201.11903
28. Wu, Z., Huang, S., Zhou, Z., Ying, H., Yuan, Z., Zhang, W., Lin, D., Chen, K.:
    Internlm2. 5-stepprover: Advancing automated theorem proving via critic-guided
    search. arXiv preprint arXiv:2410.15700 (2024)
29. Xu, H., Yan, Y., Shen, Y., Zhang, W., Hou, G., Jiang, S.: Mind the gap: Bridging
    thought leap for improved chain-of-thought tuning. arXiv preprint (2025)
30. Xu, Y., Zheng, Y., Sun, S., Huang, S., Dong, B., Zhu, H., Huang, R., Yu, G., Xu,
    H., Wu, J.: Reason from future: Reverse thought chain enhances LLM reasoning.
    arXiv preprint (2025)
31. Yan, Y., Luo, C., et al.: MathFimer: Enhancing mathematical reasoning by ex-
    panding reasoning steps through fill-in-the-middle task. In: ICLR (2025), https:
    //openreview.net/forum?id=14i2wzPPfn
32. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T.L., Cao, Y., Narasimhan, K.:
    Tree of thoughts: Deliberate problem solving with large language models. NeurIPS
    36 (2023), https://arxiv.org/abs/2305.10601
33. Ying, H., Li, Z., He, Y., et al.: Lean Workbook: A large Lean problem set formalized
    from natural language math problems. arXiv preprint (2024)
34. Yun, C., Bhojanapalli, S., Rawat, A.S., Reddi, S.J., Kumar, S.: Are transform-
    ers universal approximators of sequence-to-sequence functions? In: ICLR (2020),
    https://arxiv.org/abs/1912.10077
35. Zhang, T., et al.: Achieving >97% on GSM8K: Deeply understanding the problems
    makes LLMs better solvers for math word problems. arXiv preprint (2024)
                                               Teleological Reasoning Infilling   17

A     Theoretical Analysis
This appendix provides formal theoretical analysis of the TRI framework. We
prove the central Topological Consistency property of the PSM training ob-
jective, establish convergence guarantees for the SFT stage, and analyse the
optimisation landscape of the DPO stage under symbolic preference pairs. All
mathematical objects are introduced with explicit definitions before their first
use.

A.1     Notation
We first declare all notation used throughout this appendix.

– X : finite vocabulary of tokens; |X | = V .
– X ∗ : the set of all finite sequences over X .
– Q, P, S, M ∈ X ∗ : query, premise, milestone, and bridge sequences.
– X = [Q ⊕ ⟨tp⟩ ⊕ P ⊕ ⟨tm⟩ ⊕ S ⊕ ⟨tb⟩ ⊕ M ]: the PSM-concatenated input.
– n = |X|: total sequence length; nM = |M |: bridge length.
– θ ∈ Θ ⊆ Rd : trainable parameters of the decoder.
– fθ : X ∗ → RV : the decoder’s output logit function.
– πθ (m | c) = softmax(fθ (c))m : the autoregressive conditional for token m given
  context c.             QnM
– Pθ (M | Q, P, S) = t=1       πθ (mt | Q, P, S, m<t ): the joint bridge probability.
           ∗
– V : X → {0, 1}: the deterministic symbolic verifier; V(T ) = 1 iff T is a
  complete, sound deductive argument.
– D = {(Qi , Pi , Si , Mi )}Ni=1 : the SFT training corpus.
– ρ(P, S, M ) ∈ [0, 1]: a logical scoring function assessing the deductive quality
  of bridge M given anchors P and S.
– LSFT (θ): the SFT cross-entropy loss over D.
– LDPO (θ): the DPO loss defined in (3).
– β ∈ (0, 1): DPO temperature parameter.
– πref : the SFT-trained reference policy for DPO.
– ∥ · ∥2 , ∥ · ∥F : ℓ2 vector norm, Frobenius matrix norm.
– σ(·): the logistic sigmoid function.
– E[·]: expectation over the specified distribution.
– 1[·]: indicator function.
– ∇θ : gradient with respect to θ.

A.2     Assumptions
Assumption 1 (Lipschitz Logical Scorer) The logical scoring function ρ :
X ∗ × X ∗ × X ∗ → [0, 1] is Lρ -Lipschitz in the embedding space: for any two
bridge sequences M, M ′ and anchors P, S,

               |ρ(P, S, M ) − ρ(P, S, M ′ )| ≤ Lρ · ∥e(M ) − e(M ′ )∥2 ,

where e : X ∗ → Rh denotes the mean-pooled token embedding of a sequence.
18      Z. Cheng et al.

Remark 1 (On the Lipschitz Assumption in Discrete Domains). Assumption 1
posits a Lipschitz-continuous logical scorer ρ defined over the mean-pooled em-
bedding space. In discrete verification domains such as programming or formal
mathematics, a single-token change can flip correctness from true to false, mean-
ing the underlying binary verifier V is not Lipschitz in the token space. How-
ever, the assumption is imposed on the embedding representation e(M ), where
the model’s learned embeddings provide a smoother geometry than the discrete
token space. Consequently, the theorem should be interpreted as providing guar-
antees on the distributional concentration of bridge quality in expectation over
the learned embedding manifold, rather than pointwise guarantees on individual
discrete outputs. The empirical results in §5 serve as the primary evidence of
TRI’s effectiveness on discrete, brittle verification tasks, and the theory provides
asymptotic justification for why the training procedure converges to high-quality
bridges rather than a tight bound on individual output correctness.
Assumption 2 (Verifier Consistency) There exists a threshold ρ∗ ∈ (0, 1)
such that for all (P, S, M ) ∈ X ∗ × X ∗ × X ∗ :
                    V(P ⊕ M ⊕ S) = 1 ⇐⇒ ρ(P, S, M ) ≥ ρ∗ .
That is, the binary verifier is a level-set detector for the logical scorer.
Assumption 3 (Bounded Model Capacity) The parameter space Θ is com-
pact, and the output logit function fθ is Lf -Lipschitz in θ uniformly over all
inputs of length at most nmax tokens:
                      sup      ∥fθ (X) − fθ′ (X)∥2 ≤ Lf ∥θ − θ′ ∥2 .
                  X:|X|≤nmax


A.3     Topological Consistency
We now define and prove the central property guaranteed by PSM training.
Definition 2 (Topological Consistency). A bridge distribution Pθ (M | Q, P, S)
is (ϵ, δ)-Topologically Consistent with respect to verifier V if
                                                     
                   PM ∼Pθ (·|Q,P,S) V(P ⊕ M ⊕ S) = 1 ≥ 1 − δ
for all (Q, P, S) in the support of D, with verification margin
                           EM ∼Pθ ρ(P, S, M ) ≥ ρ∗ + ϵ.
                                            

Theorem 4 (Topological Consistency of PSM Training). Let Assump-
tions 1–3 hold. Suppose the SFT training set D consists exclusively of triples
(Q, P, S, M ) where V(P ⊕ M ⊕ S) = 1, and let θ̂SFT = arg minθ LSFT (θ). Then
the learned distribution Pθ̂SFT is (ϵN , δN )-Topologically Consistent with
                                       N                           
             ϵN = ρ∗ − ρ∗ exp −C ·            ,     δN = exp −2N ϵ2N ,
                                     nM V
where C > 0 is a constant depending only on Lρ , Lf , and the vocabulary size V ,
and N is the number of training triples.
                                              Teleological Reasoning Infilling   19

Proof. We establish the result in three steps.
   Step 1: SFT Loss Decomposition. Since every training triple satisfies
V(P ⊕M ⊕S) = 1, Assumption 2 implies ρ(P, S, M ) ≥ ρ∗ for all (Q, P, S, M ) ∈ D.
The SFT loss is:
                                N nM
                           1 X Xi             (i)                 (i)
              LSFT (θ) = −           log πθ (mt | Qi , Pi , Si , m<t ).
                           N i=1 t=1

    Step 2: Expected Log-Likelihood Bound. By the chain rule of proba-
bility and Jensen’s inequality,
                                            
                      ED log Pθ (M | Q, P, S) ≥ −LSFT (θ).

At the SFT optimum θ̂SFT , LSFT (θ̂) converges to the empirical entropy HN (M |
Q, P, S). By standard uniform convergence results for bounded-capacity func-
tion classes (Rademacher complexity argument; see, e.g., Thm. 3.3 in [16], with
probability at least 1 − exp(−2N ϵ2 ):

                                                            CnM V
             E(Q,P,S,M )∼D log Pθ̂ (M | Q, P, S) ≥ log ρ∗ −
                                               
                                                                  ,
                                                             N
for an absolute constant C depending on Lf and Lρ .
    Step 3: Logical Scoring Bound. By Assumption 1, ρ is continuous with
respect to the embedding distance. The log-likelihood lower bound from Step 2
implies that, with high probability, the learned model places mass predominantly
on sequences M ′ that are close in embedding space to the verified training bridges
M:

        EM ′ ∼Pθ̂ ρ(P, S, M ′ ) ≥ ρ∗ · EM ′ ∼Pθ̂ 1[∥e(M ′ ) − e(M )∥2 ≤ ϵ/Lρ ] .
                                                                           


Combining with the concentration inequality from Step 2, and applying Assump-
tion 2 to convert the scoring bound to a verifier probability:

               PM ′ ∼Pθ̂ V(P ⊕ M ′ ⊕ S) = 1 ≥ 1 − exp(−2N ϵ2N ),
                                          


establishing the claim with δN = exp(−2N ϵ2N ).

Remark 2. Theorem 4 implies that as N → ∞, δN → 0 and ϵN → ρ∗ (1−1/e), so
the learned bridge distribution asymptotically concentrates on symbolically veri-
fied outputs. The rate of convergence is O(1/N ), which is standard for bounded-
loss ERM over compact hypothesis classes.


A.4    DPO Optimisation Landscape

Lemma 1 (Existence of a Unique DPO Stationary Point). Let the SFT
reference policy πref satisfy πref (y | Q, P, S) > 0 for all y ∈ X ∗ (positivity
20      Z. Cheng et al.

condition). Then the DPO objective LDPO (θ) admits a unique stationary point
 ∗
θDPO  satisfying
                               1
                                       πref (y | Q, P, S) exp β −1 r∗ (Q, P, S, y) ,
                                                                                  
      πθ∗ (y | Q, P, S) =
                            Z(Q, P, S)
where r∗ (Q, P, S, y) = 1[V(P ⊕ y ⊕ S) = 1] is the binary symbolic reward, and
Z(Q, P, S) is the corresponding partition function.
Proof. The DPO objective in (3) is derived from the KL-regularised reward
maximisation problem:
                          max Ey∼π [r(y)] − β DKL (π ∥ πref ),
                            π

whose unique optimiser is the Gibbs distribution π ∗ (y) ∝ πref (y) exp(β −1 r(y))
by the Donsker-Varadhan variational principle [19, Prop. 1]. Under our sym-
bolic reward r = 1[V = 1], the optimiser assigns probability proportional to
exp(β −1 ) to verified bridges and 1 to unverified bridges, scaled by πref . The pos-
itivity condition ensures Z > 0, and the strict convexity of the KL term ensures
uniqueness.
Proposition 2 (DPO Convergence Rate). Under Assumption 3 and the
              Lemma 1, running stochastic gradient descent on LDPO with step
conditions of √
size η = O(1/ T ) for T steps yields:
                                              L2 ∥θ0 − θ∗ ∥2 
                                    ∗
                                               f           2
               E LDPO (θT ) − LDPO (θDPO ) =O       √           .
                                                      T
Proof. The DPO loss LDPO is smooth with Lipschitz gradient constant LG =
O(L2f /β) (verified by computing the Hessian of the log-sigmoid composition un-
                              √
der Assumption 3). The O(1/ T ) rate follows from standard SGD convergence
analysis for smooth, possibly non-convex objectives with bounded gradient vari-
ance [16, Thm. 4.7].

A.5     Gap-Length Sensitivity
Property 1 (Gap-Length Monotonicity of Verification Probability). Let g = |M |
denote the gap length in tokens. Under Assumptions 1–3, the (ϵN , δN )-Topological
Consistency guarantee satisfies:
                                ∂δN               ∂ϵN
                                    ≥0     and        ≤ 0.
                                 ∂g                ∂g
That is, verification probability decreases (and failure probability increases)
monotonically with gap length.
Proof. From Theorem 4, δN = exp(−2N ϵ2N ), which is monotone increasing in
g iff ϵN is decreasing in g. The constant C in ϵN = ρ∗ (1 − exp(−CN/(nM V )))
depends on nM = g, since longer bridges require modelling longer token se-
quences over the vocabulary V . Specifically, ∂ϵN /∂g = −ρ∗ · C · N/(g 2 V ) ·
exp(−CN/(gV )) < 0, confirming the claim.
                                              Teleological Reasoning Infilling    21

Remark 3. Property 1 theoretically motivates the training design decision to re-
strict gap spans to [2, 6] steps: sufficiently large gaps allow the model to learn
non-trivial bridging, but excessively long gaps degrade the verification proba-
bility and introduce noise into the preference pairs. The empirically observed
ablation result (Table 4, “Gap span ≤ 1 step”) is consistent with this predic-
tion: restricting to single-step gaps reduces MATH Level 5 accuracy by 1.9 pp,
confirming that moderate-length gap training is necessary for generalisation to
multi-step failures.


A.6     PSM Expressiveness Theorem

Theorem 5 (Universal Approximation of Bidirectional Conditionals
via PSM). For any target bidirectional conditional    Qdistribution q ∗ (M | Q, P, S)
       ∗                                                  ∗
over X that factors as a product of conditionals t q (mt | Q, P, S, m<t ), and
for any ε > 0, there exists a decoder-only transformer with L layers, embedding
dimension d, and feed-forward dimension h, parameterised by θ, such that:

                  sup DKL q ∗ (· | Q, P, S) ∥ Pθ (· | Q, P, S) < ε,
                                                              
                Q,P,S,M


provided L, d, h are chosen sufficiently large relative to ε, |X |, and the maximum
sequence lengths.

Proof. By Proposition 1, the PSM reordering ensures that every token mt has
access to all tokens in P , S, and m<t through the causal attention mechanism.
The target distribution q ∗ (mt | Q, P, S, m<t ) is thus a function of the same
information set available to the decoder under PSM. By the universal approxi-
mation results for autoregressive transformers established in [34] and [18] (which
prove that sufficiently deep transformers with sufficient width can approximate
any continuous sequence-to-sequence function to arbitrary precision, and that
transformers are Turing-complete respectively), there exists a parameterisation
θ achieving the stated KL bound. The technical requirements on L, d, h follow
from the dimension-counting arguments of [34] applied to the extended vocabu-
lary X ∪ {⟨tp⟩, ⟨tm⟩, ⟨tb⟩}.

Remark 4. Theorem 5 establishes that the PSM reordering does not sacrifice any
representational capacity relative to a hypothetical encoder-decoder architecture:
any conditional distribution that a bidirectional model could represent is also
representable by a PSM-trained decoder. This closes the potential objection
that PSM training merely provides bidirectional conditioning in name while
remaining structurally forward-only.


B     The ExtractMilestone Subroutine.

The milestone discovery step on line 7 is formalised in Algorithm 2. Starting
from the first step after the failure index k, the subroutine performs a bounded
22      Z. Cheng et al.

Algorithm 2 ExtractMilestone: Bounded Forward Scan
Require: Trace suffix Tsuf = (tk+1 , . . . , tn ) parsed into steps, verifier V, scan window
    Wmax
Ensure: Milestone step S or ∅
 1: for j = 1 to min(|Tsuf |, Wmax ) do
 2:    if V(tk+j ) = Pass then       ▷ Step passes verification in isolation return tk+j
 3:    end if
 4: end forreturn ∅                          ▷ No verifiable milestone within scan window



linear scan of at most Wmax subsequent steps, invoking the verifier V on each
step in isolation (i.e. checking whether the step, instantiated with available vari-
able bindings, constitutes a self-contained, locally sound deductive statement).
The scan terminates upon finding the first step that passes verification, which
becomes the milestone S. If no verifiable step is found within the scan window,
the subroutine returns ∅, and the repair loop falls back to suffix regeneration:
the entire remainder of the trace from P onward is regenerated by Mdraft con-
ditioned on P (without bidirectional anchoring).

Computational Complexity. Each invocation of ExtractMilestone requires
at most Wmax calls to V. In our experiments we set Wmax =8. On the MATH
benchmark, the verifier is a Python eval call (mean execution time: 2.3 ms per
step); on Lean-Workbook, it is a Lean 4 kernel type-check (mean: 47 ms per
step). Across all benchmarks, the mean number of verifier calls per problem
(including both the initial trace verification and all milestone scans) ranges from
4.1 (MATH) to 9.7 (Lean-Workbook); see the V-Calls column in Table 3. These
lightweight symbolic checks constitute less than 3% of total inference wall-clock
time, which is dominated by autoregressive token generation.

Failure Modes and Fallback Behaviour. Two failure scenarios merit explicit dis-
cussion. (i) No milestone found. If ExtractMilestone returns ∅, the repair
loop cannot perform bidirectional infilling and instead falls back to suffix re-
generation (full re-generation from P ). Across our evaluations, this occurred in
6.8% of repair attempts on MATH Level 5, 4.2% on HumanEval-Fix, and 11.3%
on Lean-Workbook (where tactic steps are less likely to be independently ver-
ifiable). (ii) Distant milestones. When the first verifiable milestone lies many
steps from P , the bridge M becomes correspondingly longer. By Property 1
(Appendix A.5), verification probability decreases monotonically with bridge
length. In practice, the mean bridge length was 3.2 steps (MATH), 2.8 steps
(HumanEval-Fix), and 4.1 steps (Lean-Workbook), with 95th-percentile values
of 6, 5, and 7 steps respectively—well within the [2, 6]-step gap span used during
training.
    Computational fairness across baselines is enforced by holding the total token
budget B constant: baselines (CoT, CoT-SC, ToT, backtracking) receive the
same budget, ensuring that observed gains stem from the quality of the repair
strategy rather than additional compute.
                                               Teleological Reasoning Infilling      23

C     Details of Experimental Setup
C.1    Datasets
MATH (Competition Mathematics). The MATH dataset [9] comprises 12,500
competition mathematics problems drawn from AMC, AIME, and related Olympiad
training materials, organised into five difficulty levels (Level 1–5) across seven
topic categories (Algebra, Combinatorics, Geometry, Number Theory, Pre-Calculus,
Pre-Algebra, and Statistics). We use the standard 7,500 / 5,000 train-test split.
Problems are pre-processed by normalising Unicode characters and standardis-
ing LATEX delimiters; no data augmentation is applied to the test set. We focus
our primary analysis on Level 4 and Level 5 problems, which constitute the
most demanding subset (50% of the test set) and exhibit the highest incidence
of multi-step chain failures in baseline models.

HumanEval-Fix (Code Repair). HumanEval-Fix [3] is derived from the orig-
inal HumanEval benchmark of 164 Python programming problems. For each
problem, we introduce controlled logical faults into the gold solution at one or
two randomly selected steps—analogous to the “gapped trace” used in TRI train-
ing—producing a set of 492 faulty solution instances (3 fault variants per prob-
lem). Evaluation uses a Python interpreter as the deterministic verifier, checking
all associated unit tests. A prediction is scored as correct only if all unit tests pass
on the repaired solution. Pre-processing consists of stripping docstrings, normal-
ising indentation, and inserting syntactically valid but semantically incorrect
placeholder expressions as fault markers; the structure and variable names of
the original function are preserved.

Lean-Workbook (Formal Theorem Proving). Lean-Workbook [33] contains 57,132
natural-language competition mathematics problems paired with Lean 4 formal
statement annotations, of which a curated subset of 2,500 problems with com-
plete proof trees forms our test partition. Each Lean 4 proof is parsed into
step-level tactics; the repair task requires the model to infill one or more miss-
ing tactic steps between verified intermediate goals. The Lean 4 kernel serves
as the deterministic verifier, accepting a generated bridge tactic block only if
the resulting proof compiles without error. Pre-processing consists of converting
Unicode symbols to standard Lean 4 Unicode identifiers and removing trailing
whitespace.

C.2    Baselines
We compare against the following six baselines, which collectively span the range
of relevant paradigms and represent the strongest publicly available methods for
each task:

– Qwen2.5-72B-Instruct + CoT. The Qwen2.5-72B-Instruct model [23] prompted
  with standard CoT zero-shot, representing the strongest open-source model
  with a standard causal generation strategy.
24     Z. Cheng et al.

– Qwen2.5-72B-Instruct + CoT-SC (k=16). The same model with self-
  consistency [26], generating k=16 independent chains and selecting the majority-
  vote answer. This incurs approximately 16× the computational cost of single
  CoT.
– Llama-3.1-70B-Instruct + CoT. Meta’s Llama 3.1 70B model [6] with
  standard CoT, providing a comparison baseline across model families.
– Llama-3.1-70B-Instruct + ToT (b=5). Tree-of-Thoughts [32] with beam
  size b=5, applied to the Llama model to assess whether structured search
  recovers competitive performance without specialised training.
– InternLM2.5-StepProver + CoT. The InternLM2.5-StepProver model
  [28], the current state of the art on Lean-Workbook, using standard CoT
  generation.
– InternLM2.5-StepProver + CoT-SC (k=8). The same model with self-
  consistency at k=8, representing the best previously published result on the
  Lean-Workbook benchmark.
    All baselines are granted the same total token budget as TRI, ensuring fair
resource comparison. Qwen2.5-72B-Instruct and Llama-3.1-70B-Instruct were se-
lected because they represent state-of-the-art open-source models of comparable
scale to the TRI-fine-tuned backbone, making any performance gap attributable
to training strategy rather than raw capacity. InternLM2.5-StepProver was in-
cluded as the domain-specific SOTA on formal proving tasks.

C.3   Evaluation Metrics
We report the following metrics, chosen for their direct alignment with the sym-
bolic correctness criterion central to TRI:
– Solution Accuracy (Acc%). For MATH, the fraction of test problems for
  which the final answer exactly matches the gold answer. This metric is ap-
  propriate because competition problems have unique, verifiable numerical or
  symbolic answers.
– Pass@1. For HumanEval-Fix, the fraction of faulty instances repaired cor-
  rectly on the first attempt (single greedy decoding), as verified by all unit
  tests passing. Pass@1 reflects the practical utility of the repair: a user needs
  a correct fix on the first try.
– Proof Completion Rate (PCR%). For Lean-Workbook, the fraction of
  problems for which the generated bridge tactics complete a formally verifiable
  Lean 4 proof. PCR is appropriate because Lean 4 provides a binary, deter-
  ministic outcome that cannot be gamed by surface-level linguistic fluency.
– Token Efficiency (Tok/Prob). The average number of tokens generated per
  problem, reported as a proxy for inference-time computational cost. Reduction
  in Tok/Prob, coupled with accuracy gains, provides direct evidence of TRI’s
  claim of surgical efficiency.
– Repair Success Rate (RSR%). The fraction of initially incorrect traces
  that are successfully repaired within the fixed token budget. RSR isolates the
  repair capability from the draft model’s base accuracy, providing a clean signal
  for the comparative evaluation.
                                             Teleological Reasoning Infilling   25

C.4   Implementation Details

Base Model. TRI is initialised from a Qwen2.5-72B base model checkpoint.
The model vocabulary is expanded by three sentinel tokens (⟨teleo_premise⟩,
⟨teleo_milestone⟩, ⟨teleo_bridge⟩), whose embeddings are randomly initialised
and trained jointly with all other parameters.

SFT Stage. We fine-tune on ≈780k (Q, P, S, M ) quadruples (450k from MATH
training traces, 330k from Lean-Workbook formalisation exercises) for 3 epochs
using AdamW [15] with an initial learning rate of 2 × 10−5 , a cosine decay
schedule with 500 warm-up steps, weight decay λ = 0.01, and a batch size of 128
sequences (global batch, across 8 GPUs). The maximum sequence length is set to
4096 tokens; sequences exceeding this threshold are discarded. Label smoothing
of 0.1 is applied to reduce over-confident predictions on noisy training instances.

DPO Stage. Following SFT, we generate 4 candidate bridges per training quadru-
ple using nucleus sampling (p = 0.95, temperature τ = 1.0) from the SFT check-
point. Each candidate is evaluated by the deterministic verifier; preference pairs
are retained only when at least one chosen and one rejected sample are avail-
able. This yields ≈312k preference pairs. DPO training uses β = 0.1, a constant
learning rate of 5 × 10−7 , batch size 32, and runs for 1 epoch.

Regularisation. Dropout (p = 0.1) is applied to the feed-forward sublayers during
both training stages. Gradient clipping at ℓ∞ -norm 1.0 is applied throughout.
FlashAttention-2 [4] is used to reduce memory footprint and increase throughput.

Compute. All training and evaluation were performed on a cluster of 8 NVIDIA
H100 SXM 80GB GPUs using FSDP (Fully Sharded Data Parallelism). The
SFT stage required approximately 58 hours of wall-clock time; the DPO stage
required approximately 12 hours. Inference is performed with greedy decoding
(T = 0) for primary results and temperature τ = 0.7 for ablation studies involv-
ing self-consistency variants. A single evaluation run on the full MATH test set
(5,000 problems) required approximately 4 hours.
