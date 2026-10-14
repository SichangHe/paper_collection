                                                           SymStep: Symbolic Step Verification for Logical Reasoning

                                               Aida Usmanova1 , Rui Gao2 , Dilshod Azizov2 , Ricardo Usbeck1 and Zangir Iklassov2
                                                                         1
                                                                           Leuphana University of Lüneburg
                                                                2
                                                                  Mohamed bin Zayed University of Artificial Intelligence
                                         {aida.usmanova, ricardo.usbeck}@leuphana.de, {rui.gao, dilshod.azizov, zangir.iklassov}@mbzuai.ac.ae


                                                                  Abstract                                             Method         LGP-14     LGP-10
                                              Chain-of-thought (CoT) prompting can fail                                Direct           14%        20%
                                              severely on constraint-dense logical reasoning                           CoT              0%         0%
                                                                                                                       Self-Refine      36%        30%
                                              tasks, where unverified errors accumulate silently
                                                                                                                       Logic-LM          0%         –
                                              across steps. We introduce SymStep: an LLM                               SymStep          86%        80%
                                              makes one atomic claim at a time (DEDUCE:                                SymStep+G       100%       100%
                                              Alice, pet, Cat), then a lightweight con-
arXiv:2607.23055v1 [cs.AI] 25 Jul 2026




                                              straint propagator checks the claim for consis-            Table 1: Performance comparison on LGP-14 and LGP-10 (10-
                                              tency with prior accepted deductions, rejects con-         puzzle subset of LGP-14). CoT and Logic-LM achieve 0% on
                                              tradictions, and cascades implied facts automati-          logical reasoning. SymStep+G achieves the best accuracy on both
                                              cally. SymStep+G additionally provides an MRV              puzzle sets. All methods are evaluated on Claude Haiku.
                                              guidance after each accepted step, directing the
                                              LLM toward the most constrained unresolved
                                              variable. On a 35-puzzle retained subset of Ze-            Logic-LM, the strongest prior symbolic+LLM method,
                                              braLogicBench—benchmark of 1,000 Einstein-                 also achieve 0% (Table 1). Two failure modes emerge: (1)
                                              style logic puzzles—Direct and CoT both achieve            unverified step accumulation: models produce steps during
                                              0%, while SymStep+G reaches 97%. On AR-                    reasoning, each unverified step can introduce an error, and
                                              LSAT analytical reasoning problems, SymStep                subsequent steps compound that error without detection; (2)
                                              achieves 100% vs. CoT’s 87%. On LGP-14,                    deductive deadlock: failure occurs even when deductions
                                              SymStep+G achieves 100% vs. 0% for CoT and                 are individually correct, but without external direction, the
                                              Logic-LM, the strongest prior symbolic+LLM                 LLM cycles without progress.
                                              baseline we compare against. Ablation studies re-             Logic-LM [Pan et al., 2023] and LINC [Olausson et al.,
                                              veal that MRV guidance is a key mechanism for              2023] translate the entire problem into formal logic in a sin-
                                              reducing directionless cycling, while consistency          gle step before invoking a solver; if that translation is wrong
                                              checking provides a safety net against explicit            anywhere, the whole attempt fails with no opportunity for
                                              contradictions. Across six benchmarks spanning             correction. Although DVCOTR [Ling et al., 2023] decom-
                                              five task domains, SymStep variants match or ex-           poses reasoning into steps and verifies them, it uses the
                                              ceed every baseline on constraint-dense and arith-         LLM itself as the verifier, leaving LLM errors and biases
                                              metic tasks. Experiments on AQUA-RAT alge-                 undetected. SymStep takes a different path. First, every
                                              bra confirm the advantage is constraint-density-           verification decision is deterministic: a constraint propaga-
                                              specific. 1                                                tor, not an LLM, checks each claim for consistency before
                                                                                                         accepting it. Second, the propagator’s arc-consistency cas-
                                                                                                         cade automatically derives implied eliminations that no sin-
                                         1   Introduction                                                gle clue reveals in isolation, performing the bookkeeping
                                         Multi-step logical reasoning remains an open problem for        that the LLM cannot reliably perform on its own. Third,
                                         Large Language Models (LLMs) [Beygi et al., 2022; Pa-           MRV-based guidance tells the LLM which variable to tackle
                                         tel et al., 2024]. Current reasoning approaches perform         next, resolving the deductive deadlock challenge.
                                         poorly on relevant benchmarks: On ZebraLogicBench [Lin          Contributions.
                                         et al., 2025], a benchmark of 1,000 Einstein-style logic puz-
                                         zles, direct prompting and chain-of-thought (CoT) achieve        1. SymStep and SymStep+G. SymStep structures LLM
                                         0%. On our own logical reasoning benchmark, CoT and                 output into one atomic D EDUCE assertion per turn.
                                                                                                             A constraint propagator then verifies it and cascades
                                             1                                                               implied eliminations, or feeds back the exact contra-
                                               Code and LGP-20 benchmark available at:
                                         https://github.com/Zangir/SymStep                                   diction if it is wrong. SymStep+G additionally pro-
                                                                                        revise
                                                           accept, next step

                    Problem                                         DEDUCE: p, a, v
                                                                                           Constraint Propagator Π
               (natural language)
                                                                                            arc-consistency cascade

                                                     LLM M
                                                         MRV hint
                MRV Hint (SymStep+G)                                           Accepted                       Contradiction
                                                                          update Π, cascade                 exact error message



Figure 1: SymStep pipeline (solid: both variants; orange dashed: SymStep+G only). The LLM generates one D EDUCE assertion per turn;
the constraint propagator checks consistency and cascades arc-consistency automatically. Green: the deduction is accepted, Π is updated,
and the LLM continues. Red: the exact contradiction is reported, and the LLM revises. Orange dashed (SymStep+G only): the MRV hint
directs the LLM toward the most constrained undetermined variable (p∗ , a∗ ).


       vides an MRV hint containing the unresolved variable                Formally, a problem has n entities (e.g., people) and k
       with the fewest remaining candidates after each veri-            attributes (e.g., pet, job), each with a finite domain of val-
       fied step, eliminating deductive deadlocks before they           ues. Every attribute is bijective: each value is assigned to
       arise. Our algorithm requires no formal logic training,          exactly one entity. The task is to uniquely determine all
       only regex-parseable output.                                     entity–attribute–value assignments from the given clues.
    2. Ablation insight: guidance is the primary driver. A                 Solution uniqueness. We require each puzzle to have
       controlled ablation (Table 9) reveals that MRV guid-             exactly one valid assignment. This uniqueness is verified
       ance alone achieves 100% with zero variance, while               by running the constraint propagator on the stored solution
       verification alone reaches only 72%. This result shows           and confirming that it reaches a fully determined state with
       that the key bottleneck is not incorrect deductions but          no alternatives, a check that also caught two originally in-
       directionless search: once pointed to the most con-              cluded puzzles (E3-Sport and M2-Nationals) that each ad-
       strained variable, the LLM makes only correct deduc-             mitted two valid solutions; automated uniqueness checks
       tions, and the safety-net verifier is rarely triggered.          are mandatory in deductive benchmarks. (See §4.1.)
    3. Six-domain evaluations. We test on ZebraLog-
       icBench (SymStep+G 97% vs. CoT 0%), AR-                          2.2    Generalization to Other Reasoning Domains
       LSAT analytical reasoning (SymStep 100% vs. CoT
       87%), LGP-14 (100%), and three additional domains                While LGPs are our primary benchmark, SymStep’s archi-
       (scheduling, arithmetic, and financial reasoning). A             tecture is domain-agnostic: it applies to any task that can
       domain-boundary experiment on AQUA-RAT alge-                     be decomposed into a sequence of atomic constraint asser-
       bra (Appendix E) confirms that the advantage is                  tions with checkable consistency. We demonstrate this on
       constraint-density-specific: where constraint propaga-           three additional domains:
       tion is not needed, SymStep+G matches CoT with no                   Scheduling puzzles (SP). Constraint satisfaction prob-
       degradation.                                                     lems in a scheduling context, e.g., assigning presenters to
                                                                        conference time slots given ordering and compatibility con-
                                                                        straints. SP share the bijective structure of LGPs but use
2     Problem Formulation                                               different domain vocabulary (time slots, rooms, roles) from
2.1     Logical Grid Puzzles                                            the LGP distribution, enabling cross-domain transfer tests.
Logical grid puzzles are the clearest way to test step-level               Math word problems (MWP) and financial reason-
deductive reasoning because every fact must follow explicit             ing (FIN). Multi-step numeric reasoning (e.g., deriving em-
constraints; there is no world knowledge to fall back on,               ployee salaries, compound interest, or tax liabilities from
and any undetected error propagates through all subsequent              arithmetic relationships). Each D EDUCE step asserts a vari-
deductions. In a scenario such as “Alice, Bob, and Carol                able’s numeric value. Verifier checks arithmetic consistency
each have a different pet (cat, dog, fish) and live in differ-          and cascades any directly implied values. The MRV hint
ently colored houses (red, blue, green). Alice does not have            identifies the next computable unknown: variable whose
a dog. Bob lives in the blue house. . . . ”, the goal is to de-         constraint becomes evaluable given current knowledge.
termine who has what, using only the given clues. Every                    All extensions reuse the same D EDUCE protocol and
attribute assignment must be derived step by step from the              outer SymStep loop, only the symbolic verifier is adapted
constraints.                                                            per domain.
2.3    Why Step-Level Verification?                                Positive update.     On σ(p, a) = v: if v ∈
                                                                                                             / Π(p, a), return
Consider a small puzzle from E2-Jobs (Adam/Beth/Chris,             CONTRADICTION. Otherwise, set Π(p, a) ← {v} and re-
drinks: Tea/Coffee/Water, jobs: Doctor/Teacher/Engineer):          move v from Π(p′ , a) for all p′ ̸= p; if any such set becomes
                                                                   empty, return CONTRADICTION.
      Adam drinks tea (clue 1). The
      doctor drinks coffee (clue 2),                               Negative update. On σ(p, a) ̸= v: discard v from
      so Adam is not the doctor. Beth is                           Π(p, a); if Π(p, a) = ∅, return CONTRADICTION.
      not the engineer (clue 3).                                   Unit propagation (arc-consistency cascade). After each
      Chris is not the doctor (clue 4).                            update, if |Π(p, a)| = 1 for any undetermined (p, a), that
      So the doctor must be Beth.
      Adam is not the teacher (clue 5), so
                                                                   singleton value is propagated as a positive deduction, poten-
      Adam is the engineer.                                        tially triggering further eliminations. This arc-consistency
      Chris is the teacher. Beth drinks                            step may derive eliminations not derivable from any single
      coffee.                                                      clue in isolation—the propagator “does the bookkeeping”
      Therefore: Adam=Tea+Teacher,                                 that the LLM could miss.
      Beth=Coffee+Doctor,                                             The propagator returns one of: OK(msg), CONTRADIC -
      Chris=Water+Engineer.                                        TION (msg), or SOLVED . Contradiction messages identify
   Although the reasoning chain correctly establishes              the specific inconsistency, e.g., “assigning Cat to Alice
“Adam is the engineer” in step 4, it contradicts that con-         leaves Bob.pet with no valid values.” The propagator runs in
clusion in the final answer (“Adam=Teacher”). The parser           O(n2 k) time per call, which is faster than LLM inference.
receives “Adam=Teacher” as the final answer and marks              Note that the propagator guarantees consistency (no contra-
the puzzle incorrect. This is unverified step accumulation:        diction with prior accepted claims) not entailment: a deduc-
each new sentence updates the narrative without checking           tion consistent with the current state but not implied by the
it against what has already been established. The longer           clues can still be accepted; the LLM bears responsibility for
the chain, the greater the chance that a contradiction will go     clue-grounded claims (formal analysis in Appendix F). The
unnoticed.                                                         propagator guarantees consistency with prior accepted de-
   SymStep prevents this by modeling reasoning as a se-            ductions, not logical entailment from the clues; a fabricated
quence of atomic constraint assertions dt = (σ(p, a) = v)          but locally consistent claim can still be accepted.
or dt = (σ(p, a) ̸= v). A deduction is consistent if it            3.3    SymStep: Verified Step-by-Step Reasoning
does not contradict any previously accepted deduction. The
propagator enforces this property at every step, ensuring          Figure 1 illustrates the full pipeline, and Appendix Algo-
that no inconsistent fact enters the context.                      rithm 1 gives the pseudocode. On each turn, the LLM re-
                                                                   ceives the full interaction history h and produces a single
                                                                   D EDUCE assertion. The propagator checks it, and feedback
3     SymStep                                                      (confirmation or contradiction) is appended to h before the
3.1    The D EDUCE Protocol                                        next LLM call. The LLM never sees an unverified fact ac-
SymStep structures LLM–verifier interaction through a              cepted into its context, every piece of confirmed informa-
minimal D EDUCE protocol: the LLM produces exactly one             tion is consistent.
constraint assertion per step:
                                                                   3.4    SymStep+G: MRV-Guided Reasoning
    DEDUCE: Entity, attribute, Value                               After a verified step, SymStep+G appends an MRV hint
    DEDUCE: Entity, attribute, NOT Value                           computed from the updated propagator state:
                                                                            M RV H INT(Π) = p∗ , a∗ , Π(p∗ , a∗ ) ,
                                                                                                                 
This format is parseable by regex, requires no formal logic
training, and is far less demanding than generating a com-                           (p∗ , a∗ ) = arg     min        |Π(p, a)|   (1)
                                                                                                        p∈P, a∈A
plete Prolog program or FOL formula. The LLM signals                                                    |Π(p,a)|>1
task completion with CONCLUDE: done.
                                                                   The hint is delivered in natural language, e.g.:
3.2    Constraint Propagator                                             [Hint] Blake’s drink must be one of: {Coffee, Juice}
The symbolic backbone of SymStep is a constraint prop-             The hint lists remaining candidates, not the answer. It is
agator that maintains a possibility matrix: Π(p, a) ⊆ Va :         derived entirely from propagated arc-consistency: informa-
a set of values still consistent with all accepted deductions      tion the LLM cannot efficiently compute without external
for entity p, attribute a. Initially, Π(p, a) = Va for all p, a.   help. The design mirrors the MRV heuristic in classical
   Intuition. Π is similar to a grid where each cell lists         constraint satisfaction [Hoffmann and Nebel, 2001]: choos-
which values a person might have for a given attribute.            ing the most constrained variable next minimizes branching
When the LLM deduces “Alice has Red,” the propagator               and resolves deadlocks.
(i) crosses Red off the grid for every other person (arc-
consistency), and (ii) checks whether any cell has now             3.5    Why Per-Step Granularity Matters
shrunk to a single option. If so, that forced assignment           Appendix Table 16 positions SymStep against existing
is propagated automatically, potentially triggering further        work. Whole-problem approaches (Logic-LM, LINC) per-
eliminations without requiring an LLM call.                        form a single large translation that is brittle to partial
descriptions and natural-language ambiguity. LLM-as-             Method        Easy (4) Med. (5) Hard (5)      Total      95% CI
verifier approaches (DVCOTR, Self-Refine) cannot guar-           Direct          2/4      0/5      0/5       2/14 (14%)    [4, 40]%
antee soundness. Only SymStep combines deterministic,            CoT             0/4      0/5      0/5         0/14 (0%)   [0, 22]%
per-step verification with proactive guidance.                   Self-Refine     0/4      1/5      4/5        5/14 (36%)  [16, 61]%
                                                                 Logic-LM        0/4      0/5      0/5         0/14 (0%)   [0, 22]%
                                                                 SymStep         4/4      4/5      4/5       12/14 (86%) [60, 96]%
                                                                 SymStep+G       4/4      5/5      5/5      14/14 (100%) [79, 100]%
4     Experiments
In total, SymStep is evaluated on 84 problem instances           Table 2: Main results on LGP-14 (Haiku). 95% Wilson CIs con-
across five task domains (grid puzzles, scheduling, arith-       firm that SymStep+G’s lower bound (79%) exceeds the upper
metic, financial reasoning, and formal constraint): 34 hand-     bounds of CoT and Logic-LM (both 22%), establishing statisti-
crafted puzzles (LGP-14, SP-6, MWP-8, FIN-6) and 50              cal significance despite n=14.
problems from two published external benchmarks (Ze-
braLogicBench n=35, AR-LSAT n=15). A domain-                     to an exact algorithm. Success requires the LLM to trans-
boundary analysis on 35 AQUA-RAT algebra problems                late every natural-language clue into correct Z3 syntax, a
is in Appendix E. All main comparisons are method-vs-            non-trivial task even for capable models.
method on the same model (Claude Haiku), isolating archi-           (4) Step-level verification with a propagator. Sym-
tectural contribution from model scale; the Sonnet cross-        Step: Appendix Algorithm 1 with GUIDE = FALSE. Sym-
model comparison is in §4.4. Single-run results on each          Step+G: Appendix Algorithm 1 with GUIDE = TRUE. Un-
benchmark are cross-validated by the N=3 multi-run ab-           like Logic-LM’s one-shot code generation, SymStep inter-
lation (§5.2), which confirms zero-variance reproducibility      leaves LLM deductions with immediate symbolic feedback
for guided configurations.                                       after every single step, allowing incremental error correc-
                                                                 tion.
4.1    Benchmark: LGP-14                                            A puzzle is counted as correct if every entity–attribute
A meaningful evaluation of step-level verification requires      pair matches the ground truth exactly.
puzzles that are genuinely hard for unverified methods, with        Models. We run all methods on both Haiku (LGP-14, SP-
multiple interacting constraints and a unique, checkable so-     6, MWP-8, FIN-6) and Sonnet (LGP-10 subset), enabling
lution. We construct LGP-14, a benchmark of fourteen log-        cross-model comparison. Full prompts are in Appendix I.
ical grid puzzles across three difficulty levels (Appendix Ta-
ble 12). All puzzles have a unique solution verified by the
                                                                 4.3   Main Results on LGP-14 (Haiku)
constraint propagator; this check caught two originally in-      Table 2 shows results on LGP-14. SymStep+G achieves a
cluded puzzles (E3-Sport and M2-Nationals) that each ad-         perfect 100% across all difficulty levels. Per-step symbolic
mitted two valid solutions. Difficulty scales with the num-      verification with MRV guidance solves every puzzle in the
ber of entities, attributes, and clue density. We additionally   benchmark. CoT and Logic-LM both achieve 0%, confirm-
provide LGP-20, which includes six further verified puz-         ing that unverified step accumulation and brittle one-shot
zles (E5–E6, M6–M7, H6–H7) released with this paper for          program synthesis collapse on constraint-dense reasoning.
future scale-up evaluation.
                                                                 4.4   Cross-Model and Per-Puzzle Detail
4.2    Methods and Baselines                                     Both SymStep and SymStep+G achieve 90% on LGP-10
                                                                 with Sonnet (Appendix B), confirming that the architec-
SymStep constitutes multiple design paradigms: pure LLM          ture is model-agnostic. Sonnet baseline figures require re-
generation, iterative self-improvement, one-shot symbolic        evaluation with a corrected output parser. CoT achieves
program synthesis, and our own step-level verification. To       0% on all 14 LGP-14 puzzles. SymStep’s two failures (one
assess the contribution of each component, we compare six        medium, one hard) are both deductive deadlocks; the hard
methods spanning four design paradigms:                          failure H2-Full stalls after 6 steps without directional guid-
   (1) Zero-shot methods. Direct: a single LLM call that         ance. SymStep+G’s MRV hint resolves both immediately,
outputs the full assignment directly. CoT [Wei et al., 2022]:    achieving 14/14. Per-puzzle outcomes and the per-difficulty
add “think step by step” before answering. Both make ex-         bar chart are in Appendix C.
actly one LLM call per puzzle.
   (2) Self-improvement without symbolic grounding.              4.5   Scheduling Benchmark: SP-6
Self-Refine [Madaan et al., 2023]: generate an initial so-       Strong results on LGP-14 could reflect overfitting to a sin-
lution, then ask the LLM to re-check every clue and revise.      gle domain. SP-6 tests transferability of system to problems
This method uses two LLM calls total; the feedback is gen-       it was not designed for, evaluating SymStep on scheduling
erated and evaluated by the same LLM, providing no exter-        problems where presenters, researchers, or crew members
nal correctness guarantee.                                       are assigned to time slots, labs, and venues. The bijective
   (3) Symbolic-program generation (SOTA). Logic-                constraint structure is preserved, but surface vocabulary, en-
LM [Pan et al., 2023]: ask the LLM to write complete Z3          tity types, and clue phrasing differ entirely from LGP-14.
Python code for the puzzle, execute it, and read the solver’s       The per-puzzle breakdown (Table 14, Appendix D) re-
output. This is the strongest prior symbolic+LLM base-           veals where guidance hurts: SP-M1-Projects and SP-M2-
line: it encodes all constraints at once and delegates solving   Research have a natural presentation order that the LLM
Method        Easy (2) Med. (2) Hard (2)         Total      95% CI    Method           Easy (2) Med. (2) Hard (2)                Total
Direct           0/2         0/2         0/2    0/6 (0%) [0, 39]%
                                                                      Direct              1/2         1/2           2/2     4/6 (67%)
CoT              0/2         0/2         0/2    0/6 (0%) [0, 39]%
Self-Refine      1/2         1/2         0/2   2/6 (33%) [10, 70]%    CoT                 2/2         1/2           2/2     5/6 (83%)
Logic-LM         0/2         0/2         0/2    0/6 (0%) [0, 39]%     SymStep             2/2         2/2           2/2    6/6 (100%)
SymStep          2/2         2/2         1/2   5/6 (83%) [44, 97]%    SymStep+G           2/2         2/2           2/2    6/6 (100%)
SymStep+G        2/2         1/2         1/2   4/6 (67%) [30, 90]%
                                                                      Table 5: Results on FIN-6 financial reasoning. Both SymStep vari-
Table 3: Results on the SP-6 scheduling benchmark. SymStep            ants achieve 100%, while direct prompting fails on an easy interest
(83%) outperforms SymStep+G (67%) here, but their 95% CIs             problem and both Direct and CoT fail on break-even analysis.
overlap substantially ([44,97] vs. [30,90]), so the difference is
not statistically significant at n=6. Both substantially exceed the
baselines.                                                                       Method          Acc.       Total    95% CI
                                                                                 Direct          100%       15/15   [80, 100]%
Method           Easy (3) Med. (3) Hard (2)                Total                 CoT              87%       13/15    [63, 96]%
                                                                                 SymStep         100%       15/15   [80, 100]%
Direct                 3/3         3/3         1/2        7/8 (88%)              SymStep+G       100%       15/15   [80, 100]%
CoT                    3/3         3/3         2/2       8/8 (100%)
SymStep                3/3         3/3         2/2       8/8 (100%)   Table 6: Results on AR-LSAT (15 problems, Haiku). Both Sym-
SymStep+G              3/3         3/3         2/2       8/8 (100%)   Step variants achieve 100%; CoT drops to 87% on the hardest
                                                                      ordering problems, where multi-step inconsistencies accumulate.
Table 4: Results on MWP-8 math word problems. On MWP-8,
CoT also achieves 100%, demonstrating that SymStep’s advan-
tage is specific to constraint-dense deductive tasks where unveri-    linguistic natural language, testing whether SymStep’s sym-
fied accumulation is harmful; for straightforward numeric chains,     bolic pipeline generalizes beyond grid-puzzle vocabulary.
CoT suffices.                                                            CoT fails on 2 of 15 problems (the hardest multi-step
                                                                      ordering items), while Direct, SymStep, and SymStep+G
exploits without guidance. The MRV hint redirects the                 all achieve 100%. AR-LSAT can be generally solved by
LLM to a different variable, disrupting its natural trajectory.       structured reasoning (even one-shot Direct). The symbolic
When guidance helps vs. hurts (dense constraint graphs vs.            verifier provides a formal guarantee against the 13% CoT
problems with a clear natural ordering) remains an open               inconsistency-accumulation failure, confirming that the pat-
question for future work.                                             tern from LGP-14 holds on linguistic natural language.

4.6   Math Word Problems: MWP-8                                       4.9   ZebraLogicBench: External Benchmark
MWP-8 shifts to numeric chain derivation: each problem                      Generalization
describes arithmetic relationships in natural language. D E -
DUCE asserts variable values, and the verifier checks arith-          The four benchmarks above (LGP-14, SP-6, MWP-8, FIN-
metic consistency.                                                    6) establish SymStep’s robustness, but do not prove that
   On MWP-8, SymStep, SymStep+G, and CoT all achieve                  the results are not an artifact of being designed around
100%, while Direct misses one hard problem (88%). CoT                 those specific puzzles. ZebraLogicBench [Lin et al., 2025]
is not universally harmful: it fails specifically on constraint-      is the cleanest available test: a published benchmark of
dense tasks where propagation is needed, but suffices for             1,000 Einstein-style logic grid puzzles spanning 25 diffi-
simple numeric chains where dependencies are linear and               culty levels (2–6 houses × 2–6 attributes) that SymStep
errors do not cascade.                                                has never seen. We evaluate on all puzzles from four size
                                                                      classes (2×3, 2×4, 3×3, 3×4), sampling uniformly to bal-
4.7   Financial Reasoning: FIN-6                                      ance difficulty. Because ZebraLogicBench does not include
FIN-6 tests six high-stakes financial problems (compound              ground-truth solutions, we derive them with a custom back-
interest, margin analysis, break-even analysis, portfolio re-         tracking CSP solver applied to the structured clue format.
turns, and income tax) where multi-step arithmetic errors             Puzzles yielding non-unique solutions or unparseable clue
accumulate silently.                                                  formats are excluded. The rest 35 puzzles are distributed as
   Direct (67%) and CoT (83%) both fail on compound                   9+9+11+6 across the four size classes. Methods and evalu-
arithmetic chains, while SymStep achieves 100%. On FIN-               ation are identical to those used for LGP-14.
M2-BreakEven, the propagator cascades the two-step de-                   Table 7 shows the same qualitative pattern as LGP-14.
pendency automatically once the LLM asserts seed values.              Direct and CoT fail on constraint-dense deductive puzzles
                                                                      regardless of puzzle source, meanwhile SymStep+G main-
4.8   AR-LSAT: Formal Constraint Reasoning                            tains high accuracy. The result is notable because Ze-
AR-LSAT is an external benchmark of 230 formal con-                   braLogicBench puzzles use different vocabulary, attribute
straint problems (ordering, selection, and assignment tasks           types (car models, house styles, etc.), and clue-phrasing
drawn directly from real LSAT analytical reasoning sec-               conventions than LGP-14. SymStep’s symbolic propagator
tions). Unlike grid puzzles, clues are expressed in legal and         operates on the assignment structure, not on surface form.
 Method           2×3    2×4      3×3     3×4         Total          Config.                Description          Acc.    Calls Contra.
                                                                     None (= CoT)       No verification, no 0%           1.0         –
 Direct           0/9     0/9     0/11     0/6     0/35 (0%)                            hint
 CoT              0/9     0/9     0/11     0/6     0/35 (0%)         Guidance only      MRV hint, no contra. 100%        6.3         0
 SymStep          9/9     9/9     7/11     3/6    28/35 (80%)                           report
 SymStep+G        9/9     8/9    11/11     6/6    34/35 (97%)        Verification only  Contra. report, no hint 72%      7.2         0
                                                                     Both (= SymStep+G) Contra. + MRV hint      100%     6.5         0
Table 7: Results on ZebraLogicBench (Haiku). Puzzles are drawn
from a published 1,000-puzzle external benchmark and were never      Table 9: Component ablation on LGP-6 (N =3 mean, per-puzzle
seen during SymStep’s design. Direct and CoT achieve 0% across       accuracy). Guidance alone achieves 100% with zero con-
all sizes, while SymStep+G reaches 97%, replicating the LGP-14       tradictions; verification alone reaches only 72%. All 6 puz-
pattern on an independently sourced benchmark.                       zles are solved in every run by both guided configurations
                                                                     (18/18 total evaluations), confirming zero-variance reproducibil-
                                                                     ity. Verification-only failures are deadlocks (the LLM cycles with-
                   Constraint / Logical           Arithmetic         out progress), not contradictions: the LLM rarely asserts inconsis-
                                                                     tent facts but stalls without directional guidance. The MRV signal,
Method         LGP-14 ZLB SP-6 LSAT MWP-8 FIN-6                      not error correction, is the primary driver.
Direct      14%            0% 0% 100%             88%      67%
CoT          0%            0% 0% 87%             100%      83%             Method                         Mean Acc (%)     Std (%)
Self-Refine 36%             – 33%   –              –        –
Logic-LM     0%             – 0%    –              –        –              CoT                                0.0              0.0
SymStep     86%           80% 83% 100%           100%     100%             Verification only (SymStep)       72.2              9.6
SymStep+G 100%            97% 67% 100%           100%     100%             Guidance only                     100.0             0.0
                                                                           SymStep+G                         100.0             0.0
Table 8: Cross-benchmark summary across six datasets. Left:
constraint-dense logical reasoning (LGP-14, ZLB, SP-6, LSAT).        Table 10: Multi-run statistics on LGP-6 (N =3, Haiku). Both
Right: arithmetic (MWP-8, FIN-6). SymStep variants dominate          guided configurations solve all 6 puzzles in every run (18/18).
constraint-dense tasks and match or exceed all baselines on arith-   Verification-only variance (σ=9.6%) reflects which hard puzzle
metic. “–” = not evaluated. See Appendix E for domain-boundary       fails in a given run, not systemic instability.
results on AQUA-RAT algebra.
                                                                     verification alone reaches only 72%. The primary bottle-
4.10    Cross-Benchmark Summary                                      neck is not incorrect deductions but directionless ones: the
                                                                     LLM stalls because it does not know which variable will ex-
Table 8 presents a cross-benchmark comparison. On                    pose the most information. Once pointed toward the most
constraint-dense logical reasoning tasks (LGP-14, ZLB,               constrained cell (2–3 candidates), it makes only correct de-
SP-6, LSAT), Direct and CoT often collapse, while Sym-               ductions and no contradictions across all guided runs. In
Step variants reach high accuracy. On arithmetic and finan-          the guidance-only configuration, the propagator still runs
cial tasks (MWP-8, FIN-6), SymStep matches or exceeds                silently, contradictions are detected internally to maintain
every baseline. The gap is largest on FIN-6, where multi-            the possibility matrix for MRV, but are not reported to the
step chains of dependent quantities punish any single unde-          LLM, which receives only directional hints.
tected error.                                                           Verification-only reaches 72% (σ=9.6%): it catches er-
   MRV guidance matters most when constraint graphs are              rors but cannot prevent deadlocks. On LGP-14, comple-
dense: SymStep+G leads on LGP-14 (100% vs. 86%),                     mentarity is visible: SymStep solves 12/14, while Sym-
while both variants achieve 100% on arithmetic tasks.                Step+G solves 14/14, with the MRV hint resolving the two
Logic-LM’s 0% on LGP-14 and SP-6 confirm that complete               deadlock-prone hard puzzles. As puzzles scale larger, the
program synthesis is prone to natural-language ambiguity,            probability of an incorrect assertion on a constrained cell
whereas one checkable claim at a time avoids the problem.            increases, and the safety net becomes the key component,
                                                                     making verification essential beyond the controlled LGP-6
5     Ablation Studies                                               setting.
SymStep+G has two key parts: a verifier that rejects incon-          5.2     Multi-Run Reproducibility
sistent claims and an MRV hint that directs what to try next.
Ablation studies isolate contribution of each part.                  Table 10 reports mean ± standard deviation computed from
                                                                     per-puzzle outcomes across three independent runs, con-
5.1    Component Ablation                                            firming that the zero-variance result is not due to single run.
We ran four configurations on LGP-6 (the six core
easy/medium/hard puzzles) over three independent runs: no            6     Analysis and Discussion
augmentation (CoT), guidance only, verification only, and            CoT vs. constraint tasks The results show a specific,
both together.                                                       predictable failure mode. CoT produces a long, uncon-
  MRV guidance alone achieves 100% (σ=0, 18/18 eval-                 strained narrative: each sentence updates the story with-
uations correct) without any contradiction detection, while          out checking whether it contradicts what has already been
established. On constraint-dense problems like LGP-14,           and LGP-20 (20 verified puzzles) is released for this pur-
undetected contradictions accumulate faster than a direct        pose. Initial Sonnet results (90% on LGP-10, §B) are en-
guess, introducing more errors, which is why CoT ends up         couraging; a clean cross-model study on GPT-4 [OpenAI
worse than answering directly. This failure is constraint-       et al., 2024], open-weight models [Touvron et al., 2023],
density-specific: CoT achieves 100% on MWP-8, where              and large reasoning models (o1, DeepSeek-R1 [Guo et al.,
arithmetic chain dependencies are simpler and a single           2025]) will clarify whether the gains are model-agnostic.
wrong number does not produce a tangled web of inconsis-            Extending the symbolic backbone. The propagator
tencies. Hence, as constraint density rises, unverified rea-     handles bijective constraints—a broad class covering grid
soning becomes actively harmful.                                 puzzles, scheduling, and selection problems—with elegant
                                                                 arc-consistency propagation. Temporal ordering, count-
Guidance as primary driver, verification as safety net.
                                                                 ing, and conditionals are well-studied in constraint pro-
There are two main reasons to include verification, even
                                                                 gramming; adding SAT/ASP [Gelfond and Lifschitz, 1988]
with guidance. First, the 72% verification-only result shows
                                                                 backends would extend SymStep to these domains, and
that verification recover errors that guidance cannot prevent.
                                                                 the outer loop and D EDUCE protocol are already backend-
As puzzles grow harder and assertion errors become more
                                                                 agnostic. The SymStep+G regression on SP-6 (n=6, not
frequent, this safety net becomes essential. Second, Sym-
                                                                 statistically significant) raises an interesting open ques-
Step’s consistency guarantee is formal: the propagator en-
                                                                 tion: learned or adaptive guidance [Lightman et al., 2024]
sures that no inconsistent fact ever enters the LLM’s con-
                                                                 that adjusts hint aggressiveness based on constraint density
text, regardless of model behavior. MRV prevents dead-
                                                                 could close this gap and clarify when MRV direction is ben-
locks, symbolic verification provides correctness. Neither
                                                                 eficial versus disruptive.
suffices alone as problems scale.
SymStep as propagation-guided search. In SymStep,                References
the LLM acts as a natural-language branching oracle while
the propagator handles consistency and cascades implied          [Achiam et al., 2023] Josh Achiam, Steven Adler, Sand-
deductions. Neither suffices alone: CoT without propa-              hini Agarwal, Lama Ahmad, Ilge Akkaya, , et al. GPT-4
gation gives 0% on LGP-14, and a propagator alone can-              technical report. arXiv preprint arXiv:2303.08774, 2023.
not extract facts from natural language. The feedback loop       [Besta et al., 2024] Maciej Besta, Nils Blach, Ales Ku-
(generate, verify, cascade, hint) is more powerful than either      bicek, Robert Gerstenberger, Michal Podstawski, Lukas
component alone.                                                    Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert
Cost and efficiency. SymStep+G uses ≈ 7 LLM calls per               Niewiadomski, Piotr Nyczyk, and Torsten Hoefler.
problem versus 1 for Direct/CoT, but ≈ 60% of assignments           Graph of thoughts: Solving elaborate problems with
are derived by cascade automatically. At ≈ $0.0013/puzzle           large language models. In Proceedings of the AAAI
(Haiku), the full LGP-14 benchmark costs under two                  Conference on Artificial Intelligence, volume 38, pages
cents. The meaningful comparison is cost per correct so-            17682–17690, 2024.
lution: Logic-LM’s single call costs ≈ $0.0006/attempt but       [Cobbe et al., 2021] Karl Cobbe, Vineet Kosaraju, Mo-
achieves 0%, making its effective cost per correct answer           hammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
unbounded.                                                          Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton,
                                                                    Reiichiro Nakano, Christopher Hesse, and John Schul-
7   Conclusion                                                      man. Training verifiers to solve math word problems.
                                                                    arXiv preprint arXiv:2110.14168, 2021.
LLMs mainly fail on constraint-dense reasoning because
unverified errors accumulate unchecked. SymStep fixes this       [d’Avila Garcez and Lamb, 2023] Artur S. d’Avila Garcez
by verifying every deduction before the next begins, achiev-        and Luı́s C. Lamb. Neurosymbolic AI: The 3rd wave.
ing 83–100% across six benchmarks (LGP-14, SP-6, MWP-               Artificial Intelligence Review, 56:12387–12406, 2023.
8, FIN-6, ZebraLogicBench, AR-LSAT) and outperform-              [Guo et al., 2025] Daya Guo, Dejian Yang, Haowei Zhang,
ing Logic-LM, the strongest prior symbolic+LLM base-                et al. DeepSeek-R1: Incentivizing reasoning capabil-
line; on ZebraLogicBench, a published 1,000-puzzle bench-           ity in LLMs via reinforcement learning. arXiv preprint
mark never seen during design, SymStep+G achieves 97%.              arXiv:2501.12948, 2025.
   Wilson CIs confirm significance: SymStep+G’s lower            [Han et al., 2024] Simeng Han, Hailey Schoelkopf, Yilun
bound strictly exceeds all baselines’ upper bounds on both          Zhao, Zhenting Qi, Martin Riddell, Wenfei Zhou, Ar-
LGP-14 (79% vs. 22%, n=14) and ZebraLogicBench (85%                 man Cohan, Dragomir Radev, et al. FOLIO: Natural lan-
vs. 10%, n=35).                                                     guage reasoning with first-order logic. In Proceedings
                                                                    of the 2024 Conference on Empirical Methods in Natu-
8   Limitations and Future Work                                     ral Language Processing, pages 22017–22031, Miami,
Scaling and model coverage. SymStep has been validated              Florida, USA, November 2024. Association for Compu-
on 119 instances spanning six independent domains and two           tational Linguistics.
model families; extending to FOLIO [Han et al., 2024] and        [Hao et al., 2023] Shibo Hao, Yi Gu, Haodi Ma, Joshua Ji-
ProofWriter [Tafjord et al., 2021] is a natural next step,          ahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting
   Hu. Reasoning with language model is planning with            timally is more effective than scaling model parameters
   world model. In Proceedings of the 2023 Conference            for reasoning. arXiv preprint arXiv:2408.03314, 2024.
   on Empirical Methods in Natural Language Processing,       [Valmeekam et al., 2024] Karthik Valmeekam,          Kaya
   pages 8154–8173, Singapore, December 2023. Associa-           Stechly, and Subbarao Kambhampati. LLMs still can’t
   tion for Computational Linguistics.                           plan; can LRMs? a preliminary evaluation of OpenAI’s
[Hoffmann and Nebel, 2001] Jörg Hoffmann and Bernhard           o1 on PlanBench. arXiv preprint arXiv:2409.13373,
   Nebel. The FF planning system: Fast plan generation           2024.
   through heuristic search. Journal of Artificial Intelli-   [Wang et al., 2024] Wenguan Wang, Yi Yang, and Fei Wu.
   gence Research, 14:253–302, 2001.                             Towards data- and knowledge-driven artificial intelli-
[Kambhampati et al., 2024] Subbarao          Kambhampati,        gence: A survey on neuro-symbolic computing. IEEE
   Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya                Transactions on Pattern Analysis and Machine Intelli-
   Stechly, Siddhant Bhambri, Lucas Saldyt, and Anil             gence, 2024. arXiv:2210.15889.
   Murthy. Position: LLMs can’t plan, but can help            [Wei et al., 2022] Jason Wei, Xuezhi Wang, Dale Schuur-
   planning in LLM-Modulo frameworks. arXiv preprint             mans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi,
   arXiv:2402.01817, 2024. ICML 2024.                            Quoc V. Le, and Denny Zhou. Chain-of-thought prompt-
[Kojima et al., 2022] Takeshi Kojima, Shixiang Shane Gu,         ing elicits reasoning in large language models. In Ad-
   Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.               vances in Neural Information Processing Systems 35
   Large language models are zero-shot reasoners. In Ad-         (NeurIPS 2022), 2022.
   vances in Neural Information Processing Systems, vol-      [Yao et al., 2023] Shunyu Yao, Dian Yu, Jeffrey Zhao,
   ume 35, pages 22199–22213. 2022.                              Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and
[Lightman et al., 2024] Hunter        Lightman,      Vineet      Karthik Narasimhan. Tree of thoughts: Deliberate prob-
   Kosaraju, Yuri Burda, Harri Edwards, Bowen Baker,             lem solving with large language models. In Advances
   Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever,          in Neural Information Processing Systems 36 (NeurIPS
   and Karl Cobbe. Let’s verify step by step. In In-             2023), 2023.
   ternational Conference on Learning Representations,        [Zhou et al., 2023] Denny Zhou, Nathanael Schärli,
   2024.                                                         Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale
[Ling et al., 2023] Zhan Ling, Yunhao Fang, Xuanlin Li,          Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le,
   Zhiao Huang, Mingu Lee, Roland Memisevic, and Hao             and Ed Chi. Least-to-most prompting enables complex
   Su. Deductive verification of chain-of-thought reason-        reasoning in large language models. In The Eleventh
   ing. In Advances in Neural Information Processing Sys-        International Conference on Learning Representations,
   tems 36 (NeurIPS 2023), 2023. arXiv:2306.03872.               ICLR 2023, Kigali, Rwanda, May 1-5, 2023.
[Mackworth, 1977] Alan K. Mackworth. Consistency in
   networks of relations. Artificial Intelligence, 8(1):99–
   118, 1977.
[Madaan et al., 2023] Aman Madaan, Niket Tandon,
   Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
   Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prab-
   humoye, Yiming Yang, et al. Self-refine: Iterative
   refinement with self-feedback. In Advances in Neural
   Information Processing Systems, volume 36, pages
   46534–46594. 2023.
[Pan et al., 2023] Liangming Pan, Alon Albalak, Xinyi
   Wang, and William Yang Wang. Logic-LM: Empow-
   ering large language models with symbolic solvers for
   faithful logical reasoning. In Findings of the Associa-
   tion for Computational Linguistics: EMNLP 2023, pages
   3806–3824, 2023.
[Shinn et al., 2023] Noah Shinn, Federico Cassano, Ed-
   ward Berman, Ashwin Gopinath, Karthik Narasimhan,
   and Shunyu Yao. Reflexion: Language agents with
   verbal reinforcement learning. In Advances in Neu-
   ral Information Processing Systems, volume 36, pages
   8634–8652. 2023.
[Snell et al., 2024] Charlie Snell, Jaehoon Lee, Kelvin Xu,
   and Aviral Kumar. Scaling LLM test-time compute op-
A    Related Work                                               Berant et al., 2013]. LLM-Modulo [Kambhampati et al.,
Chain-of-thought and multi-step reasoning. The most             2024] makes the conceptual case for pairing LLMs with
popular approach for multi-step reasoning with LLMs is          external critics; SymStep instantiates this principle at the
chain-of-thought (CoT) prompting [Wei et al., 2022], with       finest possible granularity—one claim, one check—with a
extensions ranging from zero-shot variants [Kojima et al.,      deterministic symbolic propagator.
2022] and Least-to-Most decomposition [Zhou et al., 2023]       Large reasoning models and test-time compute. Recent
to tree- and graph-structured search [Yao et al., 2023a;        LRMs (o1 [Valmeekam et al., 2024], DeepSeek-R1 [Guo
Besta et al., 2024]. These methods share one common limi-       et al., 2025]) and test-time compute scaling [Snell et al.,
tation: they generate reasoning traces but provide no mech-     2024] extend CoT by allocating more inference-time com-
anism to check whether any given step is factually valid.       putation, yet their scratchpads remain unverified. SymStep
PAL [Gao et al., 2023] and Program-of-Thought [Chen et          is complementary: it provides a sound symbolic oracle that
al., 2023] address arithmetic by offloading computation to      deterministically checks every intermediate claim, indepen-
Python, but logical deduction at the step level remains un-     dent of model scale. SymStep is evaluated on Claude Haiku
verified. Other iterative strategies such as ReAct [Yao et      and Sonnet; the broader landscape includes GPT-4 [OpenAI
al., 2023b], Self-Ask [Press et al., 2023], RAP [Hao et al.,    et al., 2024], Gemini [Anil et al., 2023], and LLaMA [Tou-
2023], Thought Cloning [Hu and Clune, 2023], and MCTS-          vron et al., 2023].
guided search [Zhao et al., 2023] add reasoning loops, yet      Classical planning and constraint satisfaction. Sequen-
none introduce step-level symbolic verification. The rich       tial search under constraints underpins classical AI plan-
evaluation literature on math reasoning [Cobbe et al., 2021;    ning: STRIPS [Fikes and Nilsson, 1971], PDDL [Mc-
Hendrycks et al., 2021], commonsense tasks [Talmor et           Dermott et al., 1998], Graphplan [Blum and Furst, 1995],
al., 2019; Bhakthavatsalam et al., 2021; Geva et al., 2021;     and LAMA [Richter and Westphal, 2010]. Compilabil-
Sakaguchi et al., 2021; Zellers et al., 2019; Yang et al.,      ity results [Nebel, 2000] and the situation calculus [Mc-
2018], and multi-task suites [Suzgun et al., 2022; Srivastava   Carthy and Hayes, 1987] formalize constraint semantics.
et al., 2022] has revealed that constraint-dense problems are   Applied to LLMs, planning benchmarks [Valmeekam et
a common bottleneck for these approaches.                       al., 2023b; Valmeekam et al., 2023a; Valmeekam et al.,
Step-level verification. Several recent works confirm that      2024] show consistent failure without symbolic support;
verifying reasoning as it unfolds is more powerful than         LLM+PDDL [Liu et al., 2023] and generalized plan-
checking a completed trace, yet none achieves the determin-     ning [Silver et al., 2024] partially address this. LLMs
istic soundness SymStep introduces. DVCOTR [Ling et al.,        also power embodied agents [Huang et al., 2024; Ichter
2023] decomposes CoT into “Natural Program” steps that          et al., 2023; Wang et al., 2023a; Wang et al., 2023b;
the LLM itself verifies, but the verifier is the same model     Song et al., 2023] on benchmarks such as ALFRED [Shrid-
that made the claim, so errors can go undetected and still      har et al., 2020], ALFWorld [Shridhar et al., 2021], and
accumulate. Faithful CoT [Lyu et al., 2023] translates a        VirtualHome [Puig et al., 2018].
completed CoT trace to a symbolic solver post hoc, but          LLM agents, tools, and code. Tool-augmented
by the time checking occurs, errors have already propa-         LLMs [Schick et al., 2023; Shen et al., 2023; Cai et
gated through subsequent steps. Self-Refine [Madaan et al.,     al., 2024] and agent architectures [Sumers et al., 2024;
2023] and Reflexion [Shinn et al., 2023] iterate on LLM         Liu et al., 2024; Yang et al., 2023] extend LLMs with
self-critique, which produces useful surface-level correc-      external execution. Code-as-policy [Liang et al., 2023;
tions but remains logically ungrounded.                         Singh et al., 2023] and code generation [Le et al., 2022;
Neuro-symbolic integration. The neuro-symbolic tradi-           Li et al., 2022] show that structured outputs with execution
tion, spanning tensor product representations [Smolensky,       feedback improve reliability. Inner Monologue [Huang
1990], neural-symbolic cognitive architectures [d’Avila         et al., 2023] provides environment feedback to the LLM
Garcez et al., 2009], and recent surveys [Wang et al., 2024;    analogously to our propagator; SymStep specializes this
Garcez and Lamb, 2023; Yan et al., 2025; Sakhovskiy et          feedback loop for logical consistency with a sound verifier.
al., 2024], aims to combine the flexibility of learned mod-
els with the reliability of formal reasoning. Our prop-         B    Cross-Model Results on LGP-10 (Sonnet)
agator draws directly on classical formal methods: arc-         Table 11 compares Haiku and Sonnet on LGP-10 (the ten
consistency [Mackworth, 1977], description logics [Baader       core puzzles shared between both runs). Both SymStep and
et al., 2003], and first-order resolution [Robinson, 1965].     SymStep+G achieve 90% on Sonnet, confirming that the
The two most closely related systems, Logic-LM [Pan et          architecture is not specific to one model family. Sonnet re-
al., 2023] and LINC [Olausson et al., 2023], represent the      quires no guidance to match Haiku+guidance, suggesting
whole-problem end of this spectrum: both ask the LLM to         that stronger models are better at variable selection without
produce a complete formal program (Z3 or FOL) from a            external hints.
natural-language description in one shot, then hand it off to
a solver. This brittle translation achieves 0% on LGP-14
and SP-6. Language-to-logic translation has also been ex-       C    Per-Puzzle Breakdown (LGP-14)
plored for temporal logic [Fuggitti and Chakraborti, 2023]      Table 13 shows binary outcomes for every method on every
and structured knowledge bases [Bollacker et al., 2008;         LGP-14 puzzle. CoT achieves 0% universally across all 14
        Method            Haiku Sonnet Haiku avg calls
                                                                                                100
        Direct      20%              0%†                1.0




                                                                                 Accuracy (%)
        CoT          0%              0%†                1.0
        Self-Refine 30%              0%†                2.0
        SymStep     80%              90%                6.2                                      50
        SymStep+G 100%               90%                6.7

Table 11: Cross-model comparison on LGP-10. † Sonnet base-
line figures reflect a now-corrected parser limitation (calibrated                                0
for Haiku’s concise output; misses Sonnet’s verbose formatting).                                      Easy                   Medium                     Hard
SymStep solutions always derive from the propagator state and are
unaffected.                                                                                                                  Difficulty
                                                                                                                Direct           CoT           Self-Refine
                                                                                                               SymStep        SymStep+G
Level    Puzzles                                        Entities Attrs Clues
Easy   E1-Pets, E2-Jobs, E3-Sport, E4-Music                3      2    4–5
Medium M1-Houses, M2-Nationals, M3-Hobby,                  4      2    6–8     Figure 2: Accuracy (%) per difficulty on LGP-14 (Haiku). Sym-
       M4-PetFruit, M5-Cities                                                  Step+G (green) achieves 100% at every level; CoT (blue) stays at
Hard   H1-Full, H2-Full, H3-5People, H4-Full, H5-Full    4–5     2–3   8–10
                                                                               0%. Easy (4 puzzles), Medium (5), Hard (5).
Table 12: LGP-14 benchmark structure. All 14 solutions are ver-
ified for uniqueness. M2-Nationals uses 8 clues (disambiguated).                                  Puzzle                 Dir CoT SR SS SS+G
LGP-20 adds 6 more puzzles: E5, E6 (easy, 3-entity), M6, M7
(medium, 4-entity), H6, H7 (hard, 4–5 entities).                                                  SP-E1-Workshop         ✗      ✗      ✓   ✓      ✓
                                                                                                  SP-E2-Lab              ✗      ✗      ✗   ✓      ✓
                                                                                                  SP-M1-Projects         ✗      ✗      ✓   ✓      ✗
puzzles. Self-Refine excels only on harder puzzles (H1, H2,                                       SP-M2-Research         ✗      ✗      ✗   ✓      ✗
H4, H5), where the self-critique pass covers more clues; it                                       SP-H1-Dept             ✗      ✗      ✗   ✗      ✓
fails on easy/medium puzzles, where the LLM rationalizes                                          SP-H2-EventCrew        ✗      ✗      ✗   ✓      ✓
wrong answers rather than catching errors. SymStep stalls                                         Total (6)              0      0      2   5       4
on M1 and H2 (deductive deadlock); SymStep+G resolves
both.                                                                          Table 14: Per-puzzle outcomes on SP-6 (Haiku). SymStep+G fails
                                                                               on SP-M1 and SP-M2 (medium puzzles with a natural sequential
            Puzzle            Dir CoT SR SS SS+G                               ordering that MRV hints disturb), while SymStep succeeds.
            E1-Pets            ✗      ✗      ✗    ✓        ✓
            E2-Jobs            ✓      ✗      ✗    ✓        ✓
            E3-Sport           ✓      ✗      ✗    ✓        ✓                   advantage. Unlike grid puzzles and scheduling problems,
            E4-Music           ✗      ✗      ✗    ✓        ✓                   AQUA-RAT questions require arithmetic reasoning over
            M1-Houses          ✗      ✗      ✗    ✗        ✓
                                                                               free-form algebraic relationships without the bijective con-
            M2-Nationals       ✗      ✗      ✗    ✓        ✓
            M3-Hobby           ✗      ✗      ✗    ✓        ✓                   straint structure that the propagator exploits.
            M4-PetFruit        ✗      ✗      ✓    ✓        ✓
            M5-Cities          ✗      ✗      ✗    ✓        ✓
            H1-Full            ✗      ✗      ✓    ✓        ✓                                                  Method          Acc.     Total
            H2-Full            ✗      ✗      ✓    ✗        ✓                                                  Direct          86%      30/35
            H3-5People         ✗      ✗      ✗    ✓        ✓                                                  CoT             89%      31/35
            H4-Full            ✗      ✗      ✓    ✓        ✓                                                  SymStep         66%      23/35
            H5-Full            ✗      ✗      ✓    ✓        ✓                                                  SymStep+G       89%      31/35
            Total (14)          2      0     5    12      14
                                                                               Table 15: Results on AQUA-RAT algebra MCQ (35 problems,
Table 13: Per-puzzle binary outcomes on LGP-14 (Haiku).                        Haiku). SymStep+G matches CoT (both 89%), confirming that
Dir=Direct, SR=Self-Refine, SS=SymStep, SS+G=SymStep+G.                        SymStep’s advantage is constraint-density-specific: where bijec-
✓=correct, ✗=incorrect.                                                        tive constraint propagation is not the bottleneck, the symbolic ver-
                                                                               ifier adds no benefit over standard reasoning.

  Figure 2 visualizes the per-difficulty breakdown.
                                                                                  SymStep+G matches CoT at 89%, while the unguided
D SP-6 Per-Puzzle Breakdown                                                    variant underperforms (66%), since the structured D EDUCE
                                                                               protocol imposes overhead not compensated by propaga-
E AQUA-RAT: Domain Boundary Analysis                                           tion benefits on open-ended algebra MCQ. This confirms
AQUA-RAT [Ling et al., 2017] is a dataset of algebra word                      the domain boundary: SymStep’s advantage is specific to
problems in multiple-choice format. We evaluate on a 35-                       tasks where constraints are dense and arc-consistency cas-
problem sample to characterize the boundary of SymStep’s                       cades contribute meaningfully to the solution.
Method                        Verifier type   Granularity    Guidance Multi-domain   thus, the cascade terminates. The O(n2 k) bound follows
Logic-LM [Pan et al., 2023]       Symbolic solver Whole problem –     –
LINC [Olausson et al., 2023]      FOL prover      Whole problem –     –              from standard arc-consistency analysis [Mackworth, 1977;
          [
DVCOTR Ling et al., 2023    ]     LLM self-check Per step       –
Self-Refine [Madaan et al., 2023] LLM self-check Whole output Vague
                                                                      –
                                                                      –
                                                                                     Hoffmann and Nebel, 2001].
SymStep                       Propagator      Per step       –        ✓              Soundness caveat. The propagator guarantees consistency,
SymStep+G                     Propagator      Per step       MRV      ✓
                                                                                     not soundness. A consistent-but-incorrect deduction (valid
Table 16: Method comparison. SymStep+G uniquely combines                             against the prior state but not entailed by the clues) can still
a deterministic per-step verifier, proactive MRV guidance, and a                     be accepted. The residual failure rate on hard puzzles re-
domain-agnostic design.                                                              flects exactly this gap.

Algorithm 1 SymStep and SymStep+G                                                    G        LGP-20 Benchmark Description
Input: Puzzle P, LLM M, budget T , flag GUIDE ∈                                      LGP-20 adds six verified puzzles to LGP-14. Solutions are
{true,false}                                                                         available in the released code. Difficulty mirrors LGP-14:
Output: Assignment σ̂ or FAIL                                                        E5-Colors (3 entities, 2 attrs, 4 clues), E6-School (3 enti-
 1: Initialize propagator Π with Π(p, a) ← Va                                        ties, 2 attrs, 5 clues), M6-Travel (4 entities, 2 attrs, 8 clues),
 2: h ← ⟨puzzle text, D EDUCE format instructions⟩                                   M7-Food (4 entities, 2 attrs, 7 clues), H6-Full (4 entities, 3
 3: for t = 1 to T do                                                                attrs, 10 clues), and H7-5People (5 entities, 2 attrs, 9 clues).
 4:    dt ← M(h)                         {one deduction}
 5:    if CONCLUDE ∈ dt or Π.S OLVED() then                                          H        Full Puzzle Descriptions
 6:       return σ̂(Π)                                                               All fourteen LGP-14 puzzles are listed below with their
 7:    end if                                                                        complete clue sets; solutions are in Table 17.
 8:    (status, msg) ← Π.A PPLY(dt )
 9:    if status = OK then                                                           Easy puzzles. E1-Pets: Alice, Bob, Carol; {Red, Blue,
10:       f b ← “✓ Verified. msg”                                                    Green} × {Cat, Dog, Fish}; 5 clues including “Bob lives
11:       if GUIDE then                                                              in the blue house” and “The person in the red house
12:          f b ← f b+ M RV H INT(Π)      {SymStep+G}                               has a cat.” E2-Jobs: Adam, Beth, Chris; {Tea, Coffee,
13:       end if                                                                     Water} × {Doctor, Teacher, Engineer}; 5 clues including
14:    else                                                                          “The doctor drinks coffee.” E3-Sport: Lena, Milo, Nora;
15:       f b ← “× Contradiction: msg. Please revise.”                               {Tennis, Swim, Run} × {Paris, London, Tokyo}; 4 clues
16:    end if                                                                        including “The person in London swims” and “Lena is not
17:    Append f b to h                                                               in Tokyo.” E4-Music: Jake, Kim, Leo; {Piano, Guitar,
18: end for                                                                          Drums} × {Mon, Tue, Wed}; 4 clues including “The piano
19: return FAIL                                                                      player practices on Wednesday.”
                                                                                     Medium puzzles. M1-Houses: Alice, Bob, Carol, Dave;
                                                                                     4 × {color, drink}; 6 clues. M2-Nationals: Ana, Ben, Carl,
F     Formal Properties of the Constraint                                            Donna; 4×{nationality, pet}; 8 clues (disambiguated). M3-
      Propagator                                                                     Hobby: Ivan, Jana, Karl, Lea; 4 × {color, hobby}; 6 clues.
                                                                                     M4-PetFruit: Omar, Petra, Quinn, Rosa; 4 × {pet, fruit};
Theorem 1 (Consistency). Every assignment σ(p, a) = v                                7 clues. M5-Cities: Alice, Bob, Carol, Dave; 4 × {city,
accepted by the propagator is consistent with all previously                         sport}; 7 clues.
accepted deductions. The possibility matrix Π satisfies:
v ∈ Π(p, a) iff v has not been ruled out by any accepted                             Hard puzzles. H1-Full: Alex, Blake, Casey, Drew; 4 ×
deduction at any prior step.                                                         {color, drink, pet}; 9 clues. H2-Full: Pam, Quinn, Rosa,
                                                                                     Sam; 4 × {color, job, pet}; 9 clues. H3-5People: Alex,
Proof. By induction on the deduction sequence. Base: Ini-                            Beth, Carl, Dana, Eric; 5 × {color, drink}; 8 clues. H4-
tially, Π(p, a) = Va ; the invariant holds trivially. Step: A P -                    Full: Kim, Lee, Mia, Ned; 4 × {color, job, pet}; 10 clues.
PLY returns OK only if v ∈ Π(p, a), ensuring consistency.                            H5-Full: Ash, Bay, Cole, Drew; 4 × {color, drink, pet}; 10
Arc-consistency propagation discards v from Π(p′ , a) for                            clues.
all p′ ̸= p, maintaining bijectivity. Any empty domain trig-
                                                                                     Puzzle Entities                     Solution (Attr1 / Attr2 / Attr3)
gers CONTRADICTION, so no inconsistent state is ever ac-                             E1     Alice / Bob / Carol              Red+Cat / Blue+Dog / Green+Fish
cepted.                                                                              E2
                                                                                     E3
                                                                                            Adam / Beth / Chris
                                                                                            Lena / Milo / Nora
                                                                                                                             Tea+Eng. / Coffee+Doctor / Water+Teacher
                                                                                                                             Tennis+Paris / Swim+London / Run+Tokyo
                                                                                     E4     Jake / Kim / Leo                 Guitar+Mon / Drums+Tue / Piano+Wed
                                                                                     M1     Alice / Bob / Carol / Dave       Green+Tea / Red+Juice / Blue+Coffee / Yellow+Water
Theorem 2 (Propagation completeness). If |Π(p, a)| = 1                               M2
                                                                                     M3
                                                                                            Ana / Ben / Carl / Donna
                                                                                            Ivan / Jana / Karl / Lea
                                                                                                                             English+Cat / German+Fish / Spanish+Bird / French+Dog
                                                                                                                             Blue+Dance / Green+Read / White+Paint / Red+Cook
for some (p, a) after accepting a deduction, the propagator                          M4
                                                                                     M5
                                                                                            Omar / Petra / Quinn / Rosa
                                                                                            Alice / Bob / Carol / Dave
                                                                                                                             Cat+Cherry / Parrot+Date / Snake+Banana / Fish+Apple
                                                                                                                             London+Run / Berlin+Tennis / Paris+Swim / Rome+Soccer
derives this assignment automatically without an additional                          H1
                                                                                     H2
                                                                                            Alex / Blake / Casey / Drew
                                                                                            Pam / Quinn / Rosa / Sam
                                                                                                                             Green+Tea+Bird / Red+Juice+Dog / Blue+Coffee+Fish / Yellow+Water+Cat
                                                                                                                             Red+Teacher+Fish / Blue+Chef+Bird / Yellow+Doctor+Cat / Green+Eng.+Dog
LLM call. The cascade reaches an arc-consistency fixed                               H3
                                                                                     H4
                                                                                            Alex / Beth / Carl / Dana / Eric White+Tea / Blue+Milk / Red+Coffee / Green+Juice / Yellow+Water
                                                                                            Kim / Lee / Mia / Ned            Red+Doctor+Cat / Green+Lawyer+Bird / Yellow+Teacher+Fish / Blue+Chef+Dog
point in O(n2 k) steps.                                                              H5     Ash / Bay / Cole / Drew          Red+Tea+Cat / Blue+Coffee+Bird / Green+Juice+Dog / Yellow+Water+Fish



Proof. Each                                                                                Table 17: Ground-truth solutions for all LGP-14 puzzles.
         P cascade step strictly reduces the total do-
main size p,a |Π(p, a)|, which is bounded below by nk;
I    System Prompts                                                  LLM: CONCLUDE: done
All methods receive the same problem header:                       After Step 2, the arc-consistency cascade automatically
     LOGIC PUZZLE                                               narrows Alice’s color to {Red}; the LLM never explicitly
     People: {people}                                           deduced this, yet the hint reveals it. This cascade efficiency
     Attributes: {attr (vals)}                                  is the key benefit of unit propagation: ≈60% of assignments
     Clues: {numbered clue list}                                are derived automatically, without requiring separate LLM
   Direct appends: “Provide your final answer as: [person]:     calls.
attr=value, ...”
   CoT appends: “Think step by step through the clues to        Full Bibliography
determine each person’s attributes. Show your reasoning,        [Anil et al., 2023] Rohan Anil, Sebastian Borgeaud, Jean-
then give the final answer.”                                       Baptiste Alayrac, Jiahui Yu, Radu Soricut, et al. Gemini:
   Self-Refine: the first call is Direct; the second call ap-      A family of highly capable multimodal models. arXiv
pends the first answer and asks: “Carefully verify each clue       preprint arXiv:2312.11805, 2023.
against your answer. List any violated clues, correct them,     [Baader et al., 2003] Franz Baader, Diego Calvanese, Deb-
and provide the revised final answer.”                             orah L. McGuinness, Daniele Nardi, and Peter F. Patel-
   SymStep / SymStep+G append after the problem                    Schneider. The Description Logic Handbook: Theory,
header:                                                            Implementation, and Applications. Cambridge Univer-
     You are solving a logic problem by making one                 sity Press, 2003.
     deduction at a time.
     Each deduction must follow EXACTLY one of these
                                                                [Berant et al., 2013] Jonathan Berant, Andrew Chou, Roy
     formats:                                                      Frostig, and Percy Liang. Semantic parsing on freebase
     DEDUCE: <Person>, <attribute>,                                from question-answer pairs. In Proceedings of the 2013
     <Value>                                                       Conference on Empirical Methods in Natural Language
     DEDUCE: <Person>, <attribute>, NOT                            Processing (EMNLP), pages 1533–1544, 2013.
     <Value>                                                    [Besta et al., 2024] Maciej Besta, Nils Blach, Ales Ku-
     After each deduction, you will receive verification
     feedback.                                                     bicek, Robert Gerstenberger, Michal Podstawski, Lukas
     When the problem is fully solved, output:                     Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert
     CONCLUDE: done                                                Niewiadomski, Piotr Nyczyk, and Torsten Hoefler.
     Do not output multiple deductions at once.                    Graph of thoughts: Solving elaborate problems with
                                                                   large language models. In Proceedings of the AAAI
    Verifier feedback:
                                                                   Conference on Artificial Intelligence, volume 38, pages
    • Accepted:        [Verifier]: ✓ Correct                       17682–17690, 2024.
      deduction accepted. (followed by an MRV
                                                                [Beygi et al., 2022] Sajjad Beygi, Maryam Fazel-Zarandi,
      hint if SymStep+G is used: [Hint] X’s attr
      must be one of: {...})                                       Alessandra Cervone, Prakash Krishnan, and Siddhartha
                                                                   Jonnalagadda. Logical reasoning for task oriented dia-
    • Contradiction:              [Verifier]: ×                    logue systems. In Proceedings of the Fifth Workshop on
      CONTRADICTION --- {exact message}.                           e-Commerce and NLP (ECNLP 5), pages 68–79. Asso-
      Please reconsider.                                           ciation for Computational Linguistics, May 2022.
                                                                [Bhakthavatsalam et al., 2021] Sumithra         Bhakthavat-
J    Example SymStep+G Transcript                                  salam, Daniel Khashabi, Tushar Khot, Bhavana Dalvi
The following is an abridged transcript of SymStep+G on            Mishra, Kyle Richardson, Ashish Sabharwal, Carissa
puzzle E1-Pets (solution: Alice=Red+Cat, Bob=Blue+Dog,             Schoenick, Oyvind Tafjord, and Peter Clark. Think
Carol=Green+Fish).                                                 you have solved direct-answer question answering?
     LLM: DEDUCE: Bob, color, Blue                                 try arc-da, the direct-answer AI2 reasoning challenge.
     Verifier: ✓ Verified. [Hint] Alice’s color must be one        CoRR, abs/2102.03315, 2021.
     of: {Red, Green}                                           [Blum and Furst, 1995] Avrim Blum and Merrick L. Furst.
     LLM: DEDUCE: Carol, color, Green                              Fast planning through planning graph analysis. In
     Verifier: ✓ Verified. [Hint] Alice’s color must be one        Proceedings of the 14th International Joint Conference
     of: {Red}                                                     on Artificial Intelligence - Volume 2, IJCAI’95, page
     LLM: DEDUCE: Alice, color, Red                                1636–1642, San Francisco, CA, USA, 1995. Morgan
     Verifier: ✓ Verified. [Hint] Alice’s pet must be one of:      Kaufmann Publishers Inc.
     {Cat}
     LLM: DEDUCE: Alice, pet, Cat                               [Bollacker et al., 2008] Kurt Bollacker, Colin Evans,
     Verifier: ✓ Verified. [Hint] Bob’s pet must be one of:        Praveen Paritosh, Tim Sturge, and Jamie Taylor.
     {Dog, Fish}                                                   Freebase: a collaboratively created graph database
     LLM: DEDUCE: Carol, pet, Fish                                 for structuring human knowledge. In Proceedings of
     Verifier: ✓ Verified. [Problem solved!] Output CON-           the 2008 ACM SIGMOD International Conference on
     CLUDE: done                                                   Management of Data, SIGMOD ’08, page 1247–1250,
  New York, NY, USA, 2008. Association for Computing          [Guo et al., 2025] Daya Guo, Dejian Yang, Haowei Zhang,
  Machinery.                                                    Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu,
[Cai et al., 2024] Tianle Cai, Xuezhi Wang, Tengyu Ma,          Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang,
                                                                Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong
  Xinyun Chen, and Denny Zhou. Large language models
                                                                Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue,
  as tool makers. In International Conference on Learn-
                                                                Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu,
  ing Representations, volume 2024, pages 54067–54089,
                                                                Chenggang Zhao, Chengqi Deng, Chong Ruan, Damai
  2024.
                                                                Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin,
[Chen et al., 2023] Wenhu Chen, Xueguang Ma, Xinyi              Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen,
  Wang, and William W. Cohen. Program of thoughts               Guowei Li, H. Zhang, Hanwei Xu, Honghui Ding,
  prompting: Disentangling computation from reasoning           Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi
  for numerical reasoning tasks. Transactions on Machine        Li, Jingchang Chen, Jingyang Yuan, Jinhao Tu, Jun-
  Learning Research, 2023.                                      jie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang,
                                                                Jin Chen, Kai Dong, Kai Hu, Kaichao You, Kaige
[Cobbe et al., 2021] Karl Cobbe,      Vineet Kosaraju,          Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang,
  Mo Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,            Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Rei-           Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang,
  ichiro Nakano, Christopher Hesse, and John Schulman.          Minghui Tang, Mingxu Zhou, Meng Li, Miaojun Wang,
  Training verifiers to solve math word problems. ArXiv,        Mingming Li, Ning Tian, Panpan Huang, Peng Zhang,
  abs/2110.14168, 2021.                                         Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge,
[d’Avila Garcez et al., 2009] Artur S. d’Avila Garcez,          Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen,
   Luı́s C. Lamb, and Dov M. Gabbay. Neural-Symbolic            R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou,
   Cognitive Reasoning. Cognitive Technologies. Springer,       Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuip-
   2009.                                                        ing Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang
                                                                Zhou, Shaoqing Wu, Tao Yun, Tian Pei, Tianyu Sun,
[Fikes and Nilsson, 1971] Richard E. Fikes and Nils J.
                                                                T. Wang, Wangding Zeng, Wen Liu, Wenfeng Liang,
   Nilsson. Strips: a new approach to the application of        Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao,
   theorem proving to problem solving. In Proceedings of        Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen,
   the 2nd International Joint Conference on Artificial In-     Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao
   telligence, IJCAI’71, page 608–620, San Francisco, CA,       Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng
   USA, 1971. Morgan Kaufmann Publishers Inc.                   Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha
[Fuggitti and Chakraborti, 2023] Francesco Fuggitti and         Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song,
   Tathagata Chakraborti. NL2LTL – a python package for         Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q.
   converting natural language (NL) instructions to linear      Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao
   temporal logic (LTL) formulas. In Proceedings of the         Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang,
   AAAI Conference on Artificial Intelligence, volume 37,       Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong
   pages 16428–16430, 2023.                                     Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang
                                                                Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou,
[Gao et al., 2023] Luyu Gao, Aman Madaan, Shuyan                Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You,
  Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie               Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanping Huang,
  Callan, and Graham Neubig. Pal: program-aided lan-            Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying
  guage models. In Proceedings of the 40th International        Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren,
  Conference on Machine Learning, ICML’23. JMLR.org,            Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan
  2023.                                                         Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu
[Garcez and Lamb, 2023] Artur d’Avila Garcez and                Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie,
  Luı́s C. Lamb. Neurosymbolic ai: the 3rd wave. Artif.         Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu,
  Intell. Rev., 56(11):12387–12406, March 2023.                 Zhongyu Zhang, and Zhen Zhang. Deepseek-r1 incen-
                                                                tivizes reasoning in llms through reinforcement learning.
[Gelfond and Lifschitz, 1988] Michael   Gelfond      and        Nature, 645(8081):633–638, 2025.
  Vladimir Lifschitz. The stable model semantics for
  logic programming. In Proceedings of the International      [Han et al., 2024] Simeng Han, Hailey Schoelkopf, Yilun
  Logic Programming Conference and Symposium, pages
                                                                Zhao, Zhenting Qi, Martin Riddell, Wenfei Zhou, James
  1070–1080. MIT Press, 1988.
                                                                Coady, David Peng, Yujie Qiao, Luke Benson, Lucy
[Geva et al., 2021] Mor Geva, Daniel Khashabi, Elad Se-         Sun, Alexander Wardle-Solano, Hannah Szabó, Ekate-
  gal, Tushar Khot, Dan Roth, and Jonathan Berant. Did          rina Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,
  aristotle use a laptop? a question answering benchmark        Brian Wong, Malcolm Sailor, Ansong Ni, Linyong Nan,
  with implicit reasoning strategies. Transactions of the       Jungo Kasai, Tao Yu, Rui Zhang, Alexander Fabbri, Wo-
  Association for Computational Linguistics, 9:346–361,         jciech Maciej Kryscinski, Semih Yavuz, Ye Liu, Xi Vic-
  2021.                                                         toria Lin, Shafiq Joty, Yingbo Zhou, Caiming Xiong,
   Rex Ying, Arman Cohan, and Dragomir Radev. FOLIO:               The 6th Conference on Robot Learning, volume 205 of
   Natural language reasoning with first-order logic. In Pro-      Proceedings of Machine Learning Research, pages 287–
   ceedings of the 2024 Conference on Empirical Methods            318. PMLR, 14–18 Dec 2023.
   in Natural Language Processing, pages 22017–22031,           [Kambhampati et al., 2024] Subbarao          Kambhampati,
   Miami, Florida, USA, November 2024. Association for             Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya
   Computational Linguistics.                                      Stechly, Siddhant Bhambri, Lucas Saldyt, and Anil
[Hao et al., 2023] Shibo Hao, Yi Gu, Haodi Ma, Joshua              Murthy. Position: Llms can’t plan, but can help plan-
   Hong, Zhen Wang, Daisy Wang, and Zhiting Hu. Rea-               ning in llm-modulo frameworks. In Proceedings of the
   soning with language model is planning with world               41st International Conference on Machine Learning,
   model. In Proceedings of the 2023 Conference on Em-             ICML’24. JMLR.org, 2024.
   pirical Methods in Natural Language Processing, pages        [Kojima et al., 2022] Takeshi Kojima, Shixiang (Shane)
   8154–8173, Singapore, December 2023. Association for            Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.
   Computational Linguistics.                                      Large language models are zero-shot reasoners. In Ad-
[Hendrycks et al., 2021] Dan Hendrycks, Collin Burns,              vances in Neural Information Processing Systems, vol-
   Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang,          ume 35, pages 22199–22213, 2022.
   Dawn Song, and Jacob Steinhardt. Measuring math-             [Le et al., 2022] Hung Le, Yue Wang, Akhilesh Deepak
   ematical problem solving with the MATH dataset. In              Gotmare, Silvio Savarese, and Steven C.H. Hoi.
   Advances in Neural Information Processing Systems 34            CodeRL: Mastering code generation through pretrained
   (NeurIPS 2021), 2021.                                           models and deep reinforcement learning. In Advances
[Hoffmann and Nebel, 2001] Jörg Hoffmann and Bernhard             in Neural Information Processing Systems 35 (NeurIPS
   Nebel. The ff planning system: fast plan generation             2022), 2022.
   through heuristic search. 14(1):253–302, May 2001.           [Li et al., 2022] Yujia Li, David Choi, Junyoung Chung,
[Hu and Clune, 2023] Shengran Hu and Jeff Clune.                   Nate Kushman, Julian Schrittwieser, Rémi Leblond,
   Thought cloning: Learning to think while acting by              Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal
   imitating human thinking. In Advances in Neural                 Lago, Thomas Hubert, Peter Choy, Cyprien de Mas-
   Information Processing Systems, volume 36, pages                son d’Autume, Igor Babuschkin, Xinyun Chen, Po-
   44451–44469, 2023.                                              Sen Huang, Johannes Welbl, Sven Gowal, Alexey
[Huang et al., 2023] Wenlong Huang, Fei Xia, Ted Xiao,             Cherepanov, James Molloy, Daniel J. Mankowitz,
                                                                   Esme Sutherland Robson, Pushmeet Kohli, Nando
   Harris Chan, Jacky Liang, Pete Florence, Andy Zeng,
                                                                   de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
   Jonathan Tompson, Igor Mordatch, Yevgen Chebotar,
                                                                   Competition-level code generation with alphacode. Sci-
   Pierre Sermanet, Tomas Jackson, Noah Brown, Linda
                                                                   ence, 378(6624):1092–1097, 2022.
   Luu, Sergey Levine, Karol Hausman, and brian ichter.
   Inner monologue: Embodied reasoning through plan-            [Liang et al., 2023] Jacky Liang, Wenlong Huang, Fei Xia,
   ning with language models. In Proceedings of The 6th            Peng Xu, Karol Hausman, Brian Ichter, Pete Florence,
   Conference on Robot Learning, volume 205 of Proceed-            and Andy Zeng. Code as policies: Language model pro-
   ings of Machine Learning Research, pages 1769–1782.             grams for embodied control. In 2023 IEEE International
   PMLR, 14–18 Dec 2023.                                           Conference on Robotics and Automation (ICRA), 2023.
[Huang et al., 2024] Xu Huang, Weiwen Liu, Xiaolong             [Lightman et al., 2024] Hunter      Lightman,        Vineet
   Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng                Kosaraju, Yuri Burda, Harrison Edwards, Bowen
   Wang, Ruiming Tang, and Enhong Chen. Understanding              Baker, Teddy Lee, Jan Leike, John Schulman, Ilya
   the planning of LLM agents: A survey. arXiv preprint            Sutskever, and Karl Cobbe. Let’s Verify Step by Step. In
   arXiv:2402.02716, 2024.                                         International Conference on Learning Representations,
                                                                   2024.
[Ichter et al., 2023] Brian Ichter, Anthony Brohan, Yev-
   gen Chebotar, Chelsea Finn, Karol Hausman, Alexan-           [Lin et al., 2025] Bill Yuchen Lin, Ronan Le Bras, Kyle
   der Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric           Richardson, Ashish Sabharwal, Radha Poovendran, Pe-
   Jang, Ryan Julian, Dmitry Kalashnikov, Sergey Levine,           ter Clark, and Yejin Choi. Zebralogic: On the scaling
   Yao Lu, Carolina Parada, Kanishka Rao, Pierre Ser-              limits of llms for logical reasoning. In Forty-second
   manet, Alexander T Toshev, Vincent Vanhoucke, Fei               International Conference on Machine Learning, ICML
   Xia, Ted Xiao, Peng Xu, Mengyuan Yan, Noah Brown,               2025, Vancouver, BC, Canada, July 13-19, 2025, vol-
   Michael Ahn, Omar Cortes, Nicolas Sievers, Clayton              ume 267 of Proceedings of Machine Learning Research,
   Tan, Sichun Xu, Diego Reyes, Jarek Rettinghouse, Jor-           2025.
   nell Quiambao, Peter Pastor, Linda Luu, Kuang-Huei           [Ling et al., 2017] Wang Ling, Dani Yogatama, Chris
   Lee, Yuheng Kuang, Sally Jesmonth, Nikhil J. Joshi,             Dyer, and Phil Blunsom. Program induction by rationale
   Kyle Jeffrey, Rosario Jauregui Ruano, Jasmine Hsu,              generation: Learning to solve and explain algebraic word
   Keerthana Gopalakrishnan, Byron David, Andy Zeng,               problems. In Proceedings of the 55th Annual Meeting
   and Chuyuan Kelly Fu. Do as i can, not as i say: Ground-        of the Association for Computational Linguistics (ACL
   ing language in robotic affordances. In Proceedings of          2017), pages 158–167, 2017.
[Ling et al., 2023] Zhan Ling, Yunhao Fang, Xuanlin Li,         approach for logical reasoning by combining language
   Zhiao Huang, Mingu Lee, Roland Memisevic, and Hao            models with first-order logic provers. In Proceedings of
   Su. Deductive verification of chain-of-thought reason-       the 2023 Conference on Empirical Methods in Natural
   ing. In Advances in Neural Information Processing Sys-       Language Processing, pages 5153–5176, Singapore, De-
   tems 36 (NeurIPS 2023), 2023. arXiv:2306.03872.              cember 2023. Association for Computational Linguis-
[Liu et al., 2023] Bo Liu, Yuqian Jiang, Xiaohan Zhang,         tics.
   Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Pe-
   ter Stone. Llm+p: Empowering large language mod-           [OpenAI et al., 2024] OpenAI, Josh Achiam, Steven
   els with optimal planning proficiency. arXiv preprint        Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya,
   arXiv:2304.11477, 2023.                                      Florencia Leoni Aleman, Diogo Almeida, Janko Al-
[Liu et al., 2024] Xiao Liu, Hao Yu, Hanchen Zhang, Yi-         tenschmidt, Sam Altman, Shyamal Anadkat, Red Avila,
                                                                Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul
   fan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang
                                                                Baltescu, Haiming Bao, Mohammad Bavarian, Jeff
   Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xi-
                                                                Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-
   ang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang,
                                                                Shapiro, Christopher Berner, Lenny Bogdonoff, Oleg
   Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie
                                                                Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg
   Huang, Yuxiao Dong, and Jie Tang. Agentbench: Eval-
                                                                Brockman, Tim Brooks, Miles Brundage, Kevin Button,
   uating llms as agents. In International Conference on
                                                                Trevor Cai, Rosie Campbell, Andrew Cann, Brittany
   Learning Representations, volume 2024, pages 52989–
                                                                Carey, Chelsea Carlson, Rory Carmichael, Brooke
   53046, 2024.
                                                                Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully
[Lyu et al., 2023] Qing Lyu, Shreya Havaldar, Adam Stein,       Chen, Ruby Chen, Jason Chen, Mark Chen, Ben
   Li Zhang, Delip Rao, Eric Wong, Marianna Apidianaki,         Chess, Chester Cho, Casey Chu, Hyung Won Chung,
   and Chris Callison-Burch. Faithful chain-of-thought rea-     Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory
   soning. In Proceedings of the 13th International Joint       Decareaux, Thomas Degry, Noah Deutsch, Damien Dev-
   Conference on Natural Language Processing and the 3rd        ille, Arka Dhar, David Dohan, Steve Dowling, Sheila
   Conference of the Asia-Pacific Chapter of the Associa-       Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou,
   tion for Computational Linguistics (Volume 1: Long Pa-       David Farhi, Liam Fedus, Niko Felix, Simón Posada
   pers), pages 305–329, Nusa Dua, Bali, November 2023.         Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie
   Association for Computational Linguistics.                   Georges, Christian Gibson, Vik Goel, Tarun Gogineni,
[Mackworth, 1977] Alan K. Mackworth. Consistency in             Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon,
   networks of relations. Artificial Intelligence, 8(1):99–     Morgan Grafstein, Scott Gray, Ryan Greene, Joshua
   118, 1977.                                                   Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy,
                                                                Jesse Han, Jeff Harris, Yuchen He, Mike Heaton,
[Madaan et al., 2023] Aman Madaan, Niket Tandon,
                                                                Johannes Heidecke, Chris Hesse, Alan Hickey, Wade
   Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah              Hickey, Peter Hoeschele, Brandon Houghton, Kenny
   Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye,        Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu
   Yiming Yang, Shashank Gupta, Bodhisattwa Prasad              Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger
   Majumder, Katherine Hermann, Sean Welleck, Amir              Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie
   Yazdanbakhsh, and Peter Clark. Self-refine: Iterative        Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser, Ali
   refinement with self-feedback. In Advances in Neural         Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar,
   Information Processing Systems, volume 36, pages             Tabarak Khan, Logan Kilpatrick, Jong Wook Kim,
   46534–46594, 2023.                                           Christina Kim, Yongjik Kim, Jan Hendrik Kirchner,
[McCarthy and Hayes, 1987] J. McCarthy and P. J. Hayes.         Jamie Kiros, Matt Knight, Daniel Kokotajlo, Łukasz
   Some philosophical problems from the standpoint of arti-     Kondraciuk, Andrew Kondrich, Aris Konstantinidis,
   ficial intelligence, page 26–45. Morgan Kaufmann Pub-        Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael
   lishers Inc., San Francisco, CA, USA, 1987.                  Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung,
[McDermott et al., 1998] Drew McDermott, Malik Ghal-            Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin,
   lab, Adele Howe, Craig Knoblock, Ashwin Ram,                 Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan
   Manuela Veloso, Daniel Weld, and David Wilkins.              Lowe, Patricia Lue, Anna Makanju, Kim Malfacini,
   PDDL – the planning domain definition language. Tech-        Sam Manning, Todor Markov, Yaniv Markovski, Bianca
   nical Report CVC TR-98-003 / DCS TR-1165, Yale Cen-          Martin, Katie Mayer, Andrew Mayne, Bob McGrew,
   ter for Computational Vision and Control, 1998.              Scott Mayer McKinney, Christine McLeavey, Paul
                                                                McMillan, Jake McNeil, David Medina, Aalok Mehta,
[Nebel, 2000] Bernhard Nebel. On the compilability and          Jacob Menick, Luke Metz, Andrey Mishchenko, Pamela
   expressive power of propositional planning formalisms.       Mishkin, Vinnie Monaco, Evan Morikawa, Daniel
   12(1):271–315, May 2000.                                     Mossing, Tong Mu, Mira Murati, Oleg Murk, David
[Olausson et al., 2023] Theo Olausson, Alex Gu, Ben Lip-        Mély, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak,
   kin, Cedegao Zhang, Armando Solar-Lezama, Joshua             Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh,
   Tenenbaum, and Roger Levy. LINC: A neurosymbolic             Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex
   Paino, Joe Palermo, Ashley Pantuliano, Giambattista        [Richter and Westphal, 2010] Silvia Richter and Matthias
   Parascandolo, Joel Parish, Emy Parparita, Alex Passos,        Westphal. The lama planner: guiding cost-based any-
   Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe            time planning with landmarks. 39(1):127–177, Septem-
   de Avila Belbute Peres, Michael Petrov, Henrique Ponde        ber 2010.
   de Oliveira Pinto, Michael, Pokorny, Michelle Pokrass,     [Robinson, 1965] J. A. Robinson. A machine-oriented
   Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris           logic based on the resolution principle.        J. ACM,
   Power, Elizabeth Proehl, Raul Puri, Alec Radford,             12(1):23–41, January 1965.
   Jack Rae, Aditya Ramesh, Cameron Raymond, Francis
   Real, Kendra Rimbach, Carl Ross, Bob Rotsted, Henri        [Sakaguchi et al., 2021] Keisuke Sakaguchi, Ronan Le
   Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders,           Bras, Chandra Bhagavatula, and Yejin Choi. Wino-
   Shibani Santurkar, Girish Sastry, Heather Schmidt,            Grande: An adversarial winograd schema challenge at
   David Schnurr, John Schulman, Daniel Selsam, Kyla             scale. Communications of the ACM, 64(9):99–106, 2021.
   Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker,     [Sakhovskiy et al., 2024] Andrey Sakhovskiy, Mikhail
   Pranav Shyam, Szymon Sidor, Eric Sigler, Maddie               Salnikov, Irina Nikishina, Aida Usmanova, Angelie
   Simens, Jordan Sitkin, Katarina Slama, Ian Sohl,              Kraft, Cedric Möller, Debayan Banerjee, Junbo Huang,
   Benjamin Sokolowsky, Yang Song, Natalie Staudacher,           Longquan Jiang, Rana Abdullah, Xi Yan, Dmitry
   Felipe Petroski Such, Natalie Summers, Ilya Sutskever,        Ustalov, Elena Tutubalina, Ricardo Usbeck, and
   Jie Tang, Nikolas Tezak, Madeleine B. Thompson, Phil          Alexander Panchenko. Textgraphs 2024 shared task on
   Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston           text-graph representations for knowledge graph question
   Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cerón         answering. In Proceedings of TextGraphs-17: Graph-
   Uribe, Andrea Vallone, Arun Vijayvergiya, Chelsea             based Methods for Natural Language Processing, pages
   Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang,        116–125, Bangkok, Thailand, August 2024. Association
   Ben Wang, Jonathan Ward, Jason Wei, CJ Weinmann,              for Computational Linguistics.
   Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian        [Schick et al., 2023] Timo Schick, Jane Dwivedi-Yu,
   Weng, Matt Wiethoff, Dave Willner, Clemens Winter,            Roberto Dessı́, Roberta Raileanu, Maria Lomeli, Eric
   Samuel Wolrich, Hannah Wong, Lauren Workman,                  Hambro, Luke Zettlemoyer, Nicola Cancedda, and
   Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu,            Thomas Scialom. Toolformer: language models can
   Sarah Yoo, Kevin Yu, Qiming Yuan, Wojciech Zaremba,           teach themselves to use tools. In Proceedings of the
   Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia            37th International Conference on Neural Information
   Zhao, Tianhao Zheng, Juntang Zhuang, William Zhuk,            Processing Systems, NIPS ’23, Red Hook, NY, USA,
   and Barret Zoph. Gpt-4 technical report, 2024.                2023.
[Pan et al., 2023] Liangming Pan, Alon Albalak, Xinyi
                                                              [Shen et al., 2023] Yongliang Shen, Kaitao Song, Xu Tan,
   Wang, and William Yang Wang. Logic-LM: Empow-
                                                                 Dongsheng Li, Weiming Lu, and Yueting Zhuang. Hug-
   ering large language models with symbolic solvers for
                                                                 ginggpt: Solving ai tasks with chatgpt and its friends in
   faithful logical reasoning. In Findings of the Associa-
                                                                 hugging face. In Advances in Neural Information Pro-
   tion for Computational Linguistics: EMNLP 2023, pages
                                                                 cessing Systems, volume 36, pages 38154–38180, 2023.
   3806–3824, 2023.
                                                              [Shinn et al., 2023] Noah Shinn, Federico Cassano, Ash-
[Patel et al., 2024] Nisarg Patel, Mohith Kulkarni, Mihir
                                                                 win Gopinath, Karthik Narasimhan, and Shunyu Yao.
   Parmar, Aashna Budhiraja, Mutsumi Nakamura, Neeraj
                                                                 Reflexion: language agents with verbal reinforcement
   Varshney, and Chitta Baral. Multi-logieval: Towards
                                                                 learning. In Advances in Neural Information Processing
   evaluating multi-step logical reasoning ability of large
                                                                 Systems, volume 36, pages 8634–8652, 2023.
   language models. In Proceedings of the 2024 Confer-
   ence on Empirical Methods in Natural Language Pro-         [Shridhar et al., 2020] Mohit Shridhar, Jesse Thomason,
   cessing, pages 20856–20879. Association for Computa-          Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh
   tional Linguistics, November 2024.                            Mottaghi, Luke Zettlemoyer, and Dieter Fox. ALFRED:
[Press et al., 2023] Ofir Press, Muru Zhang, Sewon Min,          A benchmark for interpreting grounded instructions for
   Ludwig Schmidt, Noah Smith, and Mike Lewis. Mea-              everyday tasks. In 2020 IEEE/CVF Conference on Com-
   suring and narrowing the compositionality gap in lan-         puter Vision and Pattern Recognition (CVPR), 2020.
   guage models. In Findings of the Association for Com-      [Shridhar et al., 2021] Mohit Shridhar, Xingdi Yuan,
   putational Linguistics: EMNLP 2023, pages 5687–5711,          Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler,
   Singapore, December 2023. Association for Computa-            and Matthew Hausknecht. ALFWorld: Aligning text
   tional Linguistics.                                           and embodied environments for interactive learning. In
[Puig et al., 2018] Xavier Puig, Kevin Ra, Marko Boben,          International Conference on Learning Representations
   Jiaman Li, Tingwu Wang, Sanja Fidler, and Antonio Tor-        (ICLR 2021), 2021.
   ralba. VirtualHome: Simulating household activities via    [Silver et al., 2024] Tom Silver, Soham Dan, Kavitha
   programs. In Proceedings of the IEEE Conference on            Srinivas, Joshua B. Tenenbaum, Leslie Pack Kaelbling,
   Computer Vision and Pattern Recognition (CVPR 2018),          and Michael Katz. Generalized planning in PDDL do-
   pages 8494–8502, 2018.                                        mains with pretrained large language models. In Pro-
   ceedings of the AAAI Conference on Artificial Intelli-       Eric Hambro, Faisal Azhar, Armand Joulin, Edouard
   gence, volume 38, pages 20256–20264, 2024.                   Grave, and Guillaume Lample. LLaMA: Open and
[Singh et al., 2023] Ishika Singh, Valts Blukis, Arsalan        efficient foundation language models. arXiv preprint
   Mousavian, Ankit Goyal, Danfei Xu, Jonathan Trem-            arXiv:2302.13971, 2023.
   blay, Dieter Fox, Jesse Thomason, and Animesh Garg.        [Valmeekam et al., 2023a] Karthik Valmeekam, Matthew
   ProgPrompt: Generating situated robot task plans us-          Marquez, Alberto Olmo, Sarath Sreedharan, and Sub-
   ing large language models. In 2023 IEEE International         barao Kambhampati. Planbench: An extensible bench-
   Conference on Robotics and Automation (ICRA), pages           mark for evaluating large language models on planning
   11523–11530, 2023.                                            and reasoning about change. Advances in Neural Infor-
[Smolensky, 1990] P. Smolensky. Tensor product variable          mation Processing Systems, 36:38975–38987, 2023.
   binding and the representation of symbolic structures in   [Valmeekam et al., 2023b] Karthik Valmeekam, Matthew
   connectionist systems. Artif. Intell., 46(1–2):159–216,       Marquez, Sarath Sreedharan, and Subbarao Kambham-
   November 1990.                                                pati. On the planning abilities of large language models-
[Snell et al., 2024] Charlie Victor Snell, Jaehoon Lee,          a critical investigation. Advances in Neural Information
   Kelvin Xu, and Aviral Kumar. Scaling llm test-time com-       Processing Systems, 36:75993–76005, 2023.
   pute optimally can be more effective than scaling model    [Valmeekam et al., 2024] Karthik Valmeekam,       Kaya
   parameters. ArXiv, abs/2408.03314, 2024.                      Stechly, and Subbarao Kambhampati. LLMs still can’t
[Song et al., 2023] Chan Hee Song, Jiaman Wu, Clayton            plan; can LRMs? a preliminary evaluation of OpenAI’s
   Washington, Brian M. Sadler, Wei-Lun Chao, and Yu Su.         o1 on PlanBench. arXiv preprint arXiv:2409.13373,
   Llm-planner: Few-shot grounded planning for embod-            2024.
   ied agents with large language models. In Proceedings      [Wang et al., 2023a] Guanzhi Wang, Yuanzhuo Xie, Yun-
   of the IEEE/CVF International Conference on Computer         fan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu,
   Vision (ICCV), pages 2998–3009, October 2023.                Linxi Fan, and Anima Anandkumar. Voyager: An open-
[Srivastava et al., 2022] Aarohan Srivastava, Abigail Ras-      ended embodied agent with large language models. In
   togi, Abhishek Rao, et al. Beyond the imitation game:        Proceedings of the 37th International Conference on
   Quantifying and extrapolating the capabilities of lan-       Neural Information Processing Systems, NIPS ’23, 2023.
   guage models. arXiv preprint arXiv:2206.04615, 2022.       [Wang et al., 2023b] Zihao Wang, Shaofei Cai, Guanzhou
[Sumers et al., 2024] Theodore Sumers, Shunyu Yao,              Chen, Anji Liu, Xiaojian (Shawn) Ma, and Yitao Liang.
   Karthik R Narasimhan, and Thomas L. Griffiths. Cog-          Describe, explain, plan and select: Interactive planning
   nitive Architectures for Language Agents. Transactions       with llms enables open-world multi-task agents. In Ad-
   on Machine Learning Research, 2024.                          vances in Neural Information Processing Systems, vol-
                                                                ume 36, pages 34153–34189, 2023.
[Suzgun et al., 2022] Mirac Suzgun, Nathan Scales,
   Nathanael Schärli, Sebastian Gehrmann, Yi Tay,            [Wang et al., 2024] Wenguan Wang, Yi Yang, and Fei Wu.
   Hyung Won Chung, Aakanksha Chowdhery, Quoc V.                Towards data- and knowledge-driven artificial intelli-
   Le, Denny Zhou, William Fedus, et al. Challenging            gence: A survey on neuro-symbolic computing. IEEE
   BIG-Bench tasks and whether chain-of-thought can             Transactions on Pattern Analysis and Machine Intelli-
   solve them. arXiv preprint arXiv:2210.09261, 2022.           gence, 2024. arXiv:2210.15889.
[Tafjord et al., 2021] Oyvind Tafjord, Bhavana Dalvi, and     [Wei et al., 2022] Jason Wei, Xuezhi Wang, Dale Schuur-
   Peter Clark. ProofWriter: Generating implications,           mans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi,
   proofs, and abductive statements over natural language.      Quoc V. Le, and Denny Zhou. Chain-of-thought prompt-
   In Findings of the Association for Computational Lin-        ing elicits reasoning in large language models. In Ad-
   guistics: ACL-IJCNLP 2021, pages 3621–3634, Online,          vances in Neural Information Processing Systems 35
   August 2021. Association for Computational Linguis-          (NeurIPS 2022), 2022.
   tics.                                                      [Yan et al., 2025] Xi Yan, Aida Usmanova, Cedric Möller,
[Talmor et al., 2019] Alon Talmor, Jonathan Herzig,             Patrick Westphal, and Ricardo Usbeck. Neuro-symbolic
   Nicholas Lourie, and Jonathan Berant.         Common-        relation extraction. In Handbook on Neurosymbolic AI
   senseQA: A question answering challenge targeting            and Knowledge Graphs, volume 400 of Frontiers in Arti-
   commonsense knowledge. In Proceedings of the 2019            ficial Intelligence and Applications, pages 550–576. IOS
   Conference of the North American Chapter of the              Press, 2025.
   Association for Computational Linguistics: Human           [Yang et al., 2018] Zhilin Yang, Peng Qi, Saizheng Zhang,
   Language Technologies (NAACL-HLT 2019), pages                Yoshua Bengio, William Cohen, Ruslan Salakhutdinov,
   4149–4158, 2019.                                             and Christopher D. Manning. HotpotQA: A dataset for
[Touvron et al., 2023] Hugo Touvron, Thibaut Lavril, Gau-       diverse, explainable multi-hop question answering. In
   tier Izacard, Xavier Martinet, Marie-Anne Lachaux,           Proceedings of the 2018 Conference on Empirical Meth-
   Timothée Lacroix, Baptiste Rozière, Naman Goyal,           ods in Natural Language Processing (EMNLP), 2018.
[Yang et al., 2023] John Yang, Akshara Prabhakar, Karthik
  Narasimhan, and Shunyu Yao. InterCode: Standardiz-
  ing and benchmarking interactive coding with execution
  feedback. In Advances in Neural Information Processing
  Systems 36 (NeurIPS 2023), 2023.
[Yao et al., 2023a] Shunyu Yao, Dian Yu, Jeffrey Zhao,
  Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and
  Karthik Narasimhan. Tree of thoughts: Deliberate prob-
  lem solving with large language models. In Advances
  in Neural Information Processing Systems 36 (NeurIPS
  2023), 2023.
[Yao et al., 2023b] Shunyu Yao, Jeffrey Zhao, Dian Yu,
  Nan Du, Izhak Shafran, Karthik R Narasimhan, and
  Yuan Cao. ReAct: Synergizing Reasoning and Acting
  in Language Models. In International Conference on
  Learning Representations, 2023.
[Zellers et al., 2019] Rowan Zellers, Ari Holtzman,
  Yonatan Bisk, Ali Farhadi, and Yejin Choi. HellaSwag:
  Can a machine really finish your sentence?        arXiv
  preprint arXiv:1905.07830, 2019.
[Zhao et al., 2023] Zirui Zhao, Wee Sun Lee, and David
  Hsu. Large language models as commonsense knowl-
  edge for large-scale task planning. In Advances in Neu-
  ral Information Processing Systems, volume 36, pages
  31967–31987, 2023.
[Zhou et al., 2023] Denny Zhou, Nathanael Schärli,
  Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale
  Schuurmans, Claire Cui, Olivier Bousquet, Quoc V.
  Le, and Ed H. Chi. Least-to-most prompting enables
  complex reasoning in large language models. In The
  Eleventh International Conference on Learning Repre-
  sentations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023,
  2023.
