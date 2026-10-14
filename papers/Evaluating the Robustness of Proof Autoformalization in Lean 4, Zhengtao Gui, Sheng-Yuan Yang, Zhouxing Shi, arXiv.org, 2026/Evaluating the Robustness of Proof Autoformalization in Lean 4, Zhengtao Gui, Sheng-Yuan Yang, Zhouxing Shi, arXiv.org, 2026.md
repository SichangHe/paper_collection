                                                Evaluating the Robustness of Proof Autoformalization in Lean 4


                                                                 Zhengtao Gui1 Sheng Yang2 Zhouxing Shi2
                                                       1
                                                        University of California, Irvine 2 University of California, Riverside
                                                       zhengtag@uci.edu syang362@ucr.edu zhouxing.shi@ucr.edu




                                                               Abstract                         to detect subtle logical errors reliably. In contrast,
                                                                                                formal theorem provers, such as Coq (Barras et al.,
                                             Proof autoformalization aims to translate
arXiv:2606.14867v1 [cs.CL] 12 Jun 2026




                                                                                                1999), Isabelle (Nipkow et al., 2002), and Lean
                                             a mathematical informal proof written in
                                                                                                4 (Moura and Ullrich, 2021), represent mathemat-
                                             natural language into a formal proof in a
                                             formal language such as Lean 4. Several            ical statements and proofs in a rigorous formal
                                             works have developed LLM-based models              language, enabling formal verification of whether
                                             for proof autoformalization.           However,    a proof is correct for a given statement.
                                             existing evaluations have typically focused           Given the strong capabilities of LLM reason-
                                             on translating well-formed informal proofs         ing developed in the natural-language (NL) space
                                             from curated datasets. We argue that a robust      and the formal reliability provided by the formal-
                                             proof autoformalizer must remain faithful even
                                                                                                language (FL) space, bridging NL and FL reason-
                                             for informal proofs that diverge from these
                                             idealized ones, and we present the first study     ing has emerged as an active research direction.
                                             on the robustness of proof autoformalization       The bridge can run in both directions: NL reason-
                                             models. We formulate two categories of             ing can guide the generation of FL proofs (Jiang
                                             perturbations and evaluate robustness under        et al., 2023b; Ren et al., 2025; Wang et al., 2025),
                                             each: a global perturbation paraphrases the        while FL verification can in turn verify NL reason-
                                             informal proof in a different style, under which   ing once it is faithfully translated into FL (Liu et al.,
                                             the formalization should remain consistent; a      2025a; Yao et al., 2025a; Jana et al., 2025; Cabral
                                             local perturbation alters a value, symbol, or
                                                                                                et al., 2025).
                                             proof step, possibly in a counterfactual way,
                                             and a robust formalization should faithfully          The translation from NL mathematics into FL is
                                             reflect the perturbation rather than reverting     known as autoformalization, which can be catego-
                                             to the original one or inferring a different one   rized into statement autoformalization and proof
                                             on its own. We build a benchmark with both         autoformalization, depending on whether only the
                                             perturbations on miniF2F and MATH-500,             statement or also the proof is translated. Most of
                                             and automatically measure how stable a             the previous work has focused on statement auto-
                                             proof autoformalization’s correctness is
                                                                                                formalization (Gao et al., 2024; Jiang et al., 2024;
                                             under global perturbations and how faithfully
                                             its output reflects local perturbations. We        Poiroux et al., 2025; Wang et al., 2025; Wu et al.,
                                             evaluate seven recent models, all of which         2026). Proof autoformalization, which is substan-
                                             are sensitive to global perturbations and          tially more challenging, has gained attention only
                                             mostly fail to remain faithful under local         recently (Jana et al., 2025; Cabral et al., 2025) and
                                             perturbations.    Code and data are avail-         is the focus of this work. However, these methods
                                             able via https://github.com/ucr-rai/               are typically only trained and tested on well-formed
                                             robust-proof-autoformalization.                    proofs from standard datasets, and it remains un-
                                                                                                clear how robust they are when the input deviates
                                         1   Introduction
                                                                                                from idealized proofs.
                                         Large language models (LLMs) have recently                In this work, we present the first study on the
                                         demonstrated strong capabilities in mathematical       robustness of proof autoformalization. Specifically,
                                         reasoning (Lightman et al., 2024; Guo et al., 2025),   we evaluate robustness under two categories of per-
                                         which is typically conducted in natural language;      turbations applied to the NL input. First, when the
                                         however, such natural-language reasoning is inher-     NL proof is correct but exhibits stylistic variations,
                                         ently challenging to verify reliably, and it is hard   the resulting FL proof should remain correct. This
robustness is crucial for a proof autoformalization      with representative systems including GPT-f (Polu
model to remain effective in practice across NL          and Sutskever, 2020), LISA (Jiang et al., 2021),
proofs of varying styles and quality. We thus de-        and PACT (Han et al., 2021). The second is whole-
sign global perturbations, which paraphrase the          proof generation, which produces a complete FL
entire NL proof in different styles while preserv-       proof in a single pass. Powered by recent advances
ing the mathematical semantics. Second, when a           in LLMs, a number of whole-proof generation mod-
subtle change is introduced into the NL proof —          els have been developed and have achieved strong
even a counterfactual one that represents an error —     performance, including DeepSeek-Prover-V1 (Xin
the autoformalization should faithfully reflect this     et al., 2024), which uses expert iteration; Theo-
change in the FL proof rather than inferring a differ-   remLlama (Wang et al., 2024), which adopts cur-
ent one on its own, for instance by silently correct-    riculum training; DeepSeek-Prover-V2 (Ren et al.,
ing the error. This robustness lays the groundwork       2025), which integrates NL-guided reasoning with
for future work that may combine autoformaliza-          formal proof generation; Kimina-Prover (Wang
tion with Lean-based formal verification to verify       et al., 2025), which uses compilation-based RL
NL proofs and detect errors in them, so that NL          rewards (Jana et al., 2023); and Goedel-Prover-
reasoning can in turn be strengthened by feedback        V2 (Lin et al., 2025), which combines scaffolded
from the FL side. We therefore design local pertur-      data synthesis, verifier-guided self-correction, and
bations, which modify a single value, symbol, or         model averaging. The primary focus of all these
proof step in the NL proof, possibly in a counter-       methods is on generating correct FL proofs, while
factual way.                                             we focus on bridging NL and FL proofs so that the
   We summarize our contributions as follows:            generated FL proof faithfully reflects the given NL
                                                         proof.
    • We present the first study on the robustness
      of proof autoformalization, designing global       Autoformalization. Autoformalization trans-
      and local perturbations with accompanying          lates informal language into formal language
      robustness metrics to assess properties that a     and is broadly divided into statement and proof
      robust autoformalization model should satisfy.     autoformalization. Statement autoformalization is
    • We build a benchmark that instantiates these       relatively more established. Traditional rule-based
      perturbations on miniF2F (Zheng et al., 2021)      autoformalization is hard to implement and
      and MATH-500 (Lightman et al., 2024). We           generalize (Jiang et al., 2023a). Thus, recent
      evaluate the robustness of a variety of proof      work mainly focuses on LLM-based methods,
      autoformalization methods including latest         including in-context learning (Wu et al., 2022),
      ones such as ProofBridge (Jana et al., 2025)       back-translation-based data synthesis (Jiang et al.,
      and ProofFlow (Cabral et al., 2025).               2023a; Azerbayev et al., 2023; Wu et al., 2025),
                                                         retrieval-augmented generation (Liu et al., 2025b),
    • Our experiments reveal that all existing proof     natural language inference (Ying et al., 2024),
      autoformalization methods exhibit limited ro-      expert iteration with LLM judges (Wang et al.,
      bustness, typically suffer from unstable cor-      2025), and dataset construction with translator
      rectness under global perturbations and lim-       fine-tuning, as in Herald-translator (Gao et al.,
      ited faithfulness under local perturbations, in-   2024).
      dicating substantial room for improvement.            Proof autoformalization has received relatively
                                                         limited attention and is a more recent research di-
2    Related Work
                                                         rection. FormL4 (Lu et al., 2024) trains on GPT-4-
Formal Theorem Proving. Formal theorem                   informalized Mathlib proofs with step-wise Lean
proving aims to generate an FL proof for a given         feedback, while ProofBridge (Jana et al., 2025)
FL statement, such that the generated proof can          uses NL-FL representation learning and cross-
be rigorously verified by a proof assistant such as      modal retrieval to guide proof formalization. Addi-
Lean 4, which guarantees that the proof is correct       tionally, some recent methods perform proof auto-
for the given statement. Existing methods gener-         formalization step by step, such as StepProof (Hu
ally fall into two paradigms. The first is next-tactic   et al., 2025) using Isabelle, and ProofFlow (Cabral
prediction, which generates one proof step (tactic)      et al., 2025), which preserves proof structure via de-
at a time conditioned on the current proof state,        pendency DAGs and intermediate lemmas. In this
work, we focus on evaluating the robustness of ex-      proof, denoted as Orig, we consider two paraphras-
isting proof autoformalization methods in Lean 4.       ing modes: free-form paraphrasing (-FF ) uses an
                                                        LLM to restate the NL proof in its own wording and
Metrics for autoformalization. For proof auto-
                                                        style while preserving the mathematical meaning
formalization, recent evaluations introduce proof-
                                                        and overall logic; and step-by-step paraphrasing (-
level metrics. ProofBridge (Jana et al., 2025) eval-
                                                        Step) uses an LLM to reorganize the NL proof into
uates the correctness of generated formalizations
                                                        one with a clearly numbered sequence of steps. NL
using Type Correctness (TC) and Semantic Correct-
                                                        proofs paraphrased with these two modes can rep-
ness (SC). TC is determined by whether the gener-
                                                        resent stylistic variations in NL proofs encountered
ated FL passes Lean’s type checker, whereas SC is
                                                        in real-world scenarios. For example, an original
computed only for type-correct FL and measures
                                                        proof may write:
whether the generated FL is semantically equiva-
lent to the gold-standard FL. ProofFlow (Cabral              Orig: Since x2 −5x+6 = (x−2)(x−3),
et al., 2025) proposes proofscore, a unified metric          the roots are 2 and 3.
that evaluates proof formalization through syntactic
correctness, semantic faithfulness, and structural      A free-form paraphrase may put the same idea in
fidelity. It checks whether formalized steps com-       different wording:
pile, whether they match the corresponding natural-          FF: Factoring the quadratic shows that it
language steps, and whether their proof-step depen-          vanishes exactly at x = 2 and x = 3.
dencies are preserved by a DAG structure. These
metrics, evaluated on well-formed NL proofs alone,      A step-by-step paraphrase instead makes the deriva-
do not assess the robustness of proof autoformal-       tion explicit:
ization, which we investigate in this work.
                                                             Step:
3     Method                                                   1. Factor x2 −5x+6 = (x−2)(x−3).
We study the robustness of proof autoformalization             2. Set each factor to zero.
models in Lean 4. For a target model f , the task is           3. Thus x = 2 or x = 3.
to translate a natural-language (NL) theorem-proof
pair MNL = ⟨TNL , PNL ⟩ into a formal-language          All three versions prove the same claim, but they ex-
(FL) pair McFL = ⟨TbFL , PbFL ⟩:                        pose the autoformalizer to different wording, levels
                                                        of detail, and proof organization. Using Gemini-
                 M
                 cFL = f (MNL ),                        2.5-Flash and Qwen3.5-397B-A17B, respectively,
                                                        we generate four types of globally perturbed NL
where TNL and PNL denote the NL theorem state-          proofs: G-FF, Q-FF, G-Step, and Q-Step. To-
ment and proof, and TbFL and PbFL denote their FL       gether with Orig, this yields five NL proof styles
counterparts. We investigate the robustness un-         per problem. Details are in Appendix A.2.
der two categories of perturbations applied to the
NL input. A global perturbation paraphrases the         Correctness Metrics. Since these global pertur-
whole NL proof PNL , and we evaluate robustness         bations are expected to preserve the mathemat-
to it by measuring the correctness of the resulting     ical meanings, a robust proof autoformalization
formalization (§3.1); a local perturbation changes      should achieve comparable correctness across all
a single value, symbol, or proof step within the        five styles. We therefore measure robustness by
NL input, and we evaluate faithfulness by measur-       the stability of correctness across styles: large vari-
ing whether the formalization faithfully reflects the   ation across styles indicates sensitivity to surface
change (§3.2).                                          wording rather than the underlying mathematics.
                                                        As shown in Figure 1, each generated FL output
3.1   Global Perturbations                              is evaluated by three complementary correctness
For global perturbations, we use LLMs to para-          metrics: Type Correctness (TC) checks whether
phrase the entire NL proof. Specifically, we use        the generated FL output compiles, which formally
two LLMs: Gemini-2.5-Flash (Google, 2025) (G),          guarantees the correctness of the FL proof for the
representing a closed-source model, and Qwen3.5-        given FL statement. Statement Semantic Correct-
397B-A17B (Qwen Team, 2026) (Q), represent-             ness (StmtSC) and Proof Semantic Correctness
ing an open-source model. Given the original NL         (ProofSC) assess whether the generated formal
statement and formal proof, respectively, semanti-      operator in x2 − 6x + 10 from + to −. A step dele-
cally matches their NL counterparts. FullyCorrect       tion may remove the justification “Since (x−3)2 ≥
is satisfied only when all three metrics are satis-     0, expanding gives x2 − 6x + 9 ≥ 0” while keeping
fied simultaneously: Type Correctness, Statement        the stated outcome “Hence x2 − 6x + 10 ≥ 1.” In
Semantic Correctness, and Proof Semantic Cor-           all three cases, the edited proof may no longer be
rectness. For scoring, TC is checked by the Lean        mathematically valid, but a faithful formalization
compiler, while StmtSC and ProofSC are assigned         should still reflect the edited text rather than silently
by an LLM judge; we detail the judging proce-           repairing it. This is particularly important when
dure in Appendix A.3.3 and audit its reliability in     proof autoformalization is applied to verify an NL
Appendix A.5.                                           proof—possibly incorrect—by checking its auto-
                                                        formalized counterpart in a formal proof assistant
3.2   Local Perturbations                               such as Lean.
A local perturbation changes a single value, sym-          Number and symbol edits are applied in both the
bol, or proof step in the NL input. We deliberately     proof and the statement; step deletion applies only
allow such perturbations to be possibly counter-        to the proof. The statement edits act as a control
factual, in order to reveal the different behaviors     against which the proof-level results can be read.
of two types of autoformalizers. A Faithful Aut-        To build an edit, an LLM (Gemini-2.5-Flash) first
oformalizer produces a Lean formalization that          marks the eligible locations in the input: numeric
faithfully reflects the NL input it is given, even in   literals, relations and operators, and substantive
the presence of counterfactual edits, which is the      proof steps. We keep only locations that pass rule-
desired behavior for robust autoformalization. In       based validity checks, discarding cases that would
contrast, a Biased Autoformalizer produces an aut-      render the problem malformed, such as numbers
oformalization that silently overrides the edit with    inside subscripts or superscripts and relations in-
its own inference. This occurs because a spurious       side chained expressions like 0 < p < 15. From
bias acquired during training may lead the model to     the valid locations, we choose one for each of the
fill in seemingly plausible content based on the FL     statement and the proof. For a number or symbol
statement, the context of the FL proof, and patterns    edit, this is a single-span substitution at a marked
seen in well-formed proofs, rather than faithfully      position; for a step deletion, we instead rank the
following the actual NL input. For example, given       eligible steps by a quality score and delete the justi-
a proof “from 2x + 3 = 17 we get 2x = 14, so            fication of the top-ranked one. Appendix A.2 gives
x = 7”, we may change the intermediate step to          the full marking, filtering, and ranking rules, and
2x = 16, which no longer holds arithmetically. A        Table 1 reports the per-type edit counts.
Faithful Translator should carry this step into the
FL proof and produce 2 * x = 16, whereas a              Faithfulness Metrics. For local perturbations,
Biased Autoformalizer may revert to 14 on its own       we classify each output as faithful, reverted, or
and produce 2 * x = 14.                                 unclear: a faithful output reflects the edited input,
    We design three specific types of edits for the     a reverted output matches the original unedited
local perturbations. A number edit changes a nu-        input, and an unclear output matches neither (for
meric literal to a different value of similar magni-    example, it is empty, fails to compile, or never men-
tude and the same sign; a symbol edit replaces a        tions the edited entity). This label is an objective
relation or operator with its opposite (e.g. + with     property of the output rather than a subjective judg-
−, or ≤ with ≥); and a step deletion removes the        ment: it is determined entirely by which value the
justification of one substantive proof step while       output carries (the edited one, the original, or nei-
keeping its stated outcome, so the proof asserts        ther). We assign these labels with an LLM judge;
the step’s result without proving it. For example,      such labels can be easily inspected by humans, and
consider a proof step that derives a lower bound:       we audit the labeling reliability in Appendix A.5.
                                                        From these labels we compute the Faithful Rate
      Since (x − 3)2 ≥ 0, expanding gives
                                                        (FR) and Reverted Rate (RR) as the fractions of
      x2 −6x+9 ≥ 0. Hence x2 −6x+10 ≥ 1.
                                                        the identifiable (faithful or reverted) outputs, so
A number edit may change the final bound from           that FR + RR = 1; a higher FR marks a Faith-
1 to 2. A symbol edit may change the relation           ful Autoformalizer and a higher RR indicates a
x2 −6x+10 ≥ 1 to x2 −6x+10 ≤ 1, or change the           Biased Autoformalizer. The unclear outputs are
                                Generated Lean Formalization



                    Lean Compiler                       LLM Semantic Judge



                                               Statement Semantic                 Proof Semantic
                   Type Correctness
                                              Correctness (StmtSC)             Correctness (ProofSC)
                        (TC)
                                              Is the formal statement             Is the formal proof
                   Does the generated
                                            semantically consistent with        semantically consistent
                   Lean code compile?
                                               the natural statement?           with the natural proof?



                                                 Fully Correct
                                        All three metrics must be satisfied:
                                           TC, StmtSC, and ProofSC


Figure 1: Correctness metrics pipeline for global perturbations. Type Correctness (TC) is checked by the Lean
compiler, while Statement Semantic Correctness (StmtSC) and Proof Semantic Correctness (ProofSC) are evaluated
by an LLM judge. A generated formalization is counted as FullyCorrect only when all three conditions are satisfied.


excluded from FR/RR, and we report their share                  Table 1: Dataset statistics for local perturbations, re-
as the Other/Unclear Rate (OUR), analyzing its                  porting the number of statement-level / proof-level edit
                                                                instances on miniF2F and MATH-500.
composition with examples in Appendix A.4.
                                                                                          miniF2F         MATH-500
4     Experiments
                                                                        Number-edit       227 / 241       490 / 489
We first describe the common experimental setup                         Symbol-edit       130 / 195       195 / 349
(§4.1), then report two experiments: one measur-                        Step-deletion     – / 129         – / 192
ing robustness to global perturbations through the
stability of correctness (§4.2), and one measuring
faithfulness to local perturbations (§4.3). Finally,               For global perturbations, each of the problems
we validate that the perturbations themselves are               appears in five styles, which gives 3,720 problem-
correctly constructed (§4.4).                                   style instances in total. For local perturbations, we
                                                                generate one edit per problem for each applicable
4.1    Setup                                                    combination of edit type and location: number and
Datasets. We build our evaluation based on two                  symbol edits in both the statement and the proof,
mathematical reasoning datasets: miniF2F (Zheng                 and step deletion in the proof only. An edit is cre-
et al., 2021) and MATH-500 (Lightman et al.,                    ated only where an eligible location exists, and thus
2024). miniF2F contains 244 olympiad-style prob-                the counts vary by type and dataset. Table 1 shows
lems drawn from AIME, AMC, and IMO; MATH-                       the full breakdown, totaling 2,637 local perturba-
500 contains 500 problems from the MATH bench-                  tions.
mark (Hendrycks et al., 2021). MATH-500 prob-
lems are originally posed as computational prob-                Models. We evaluate seven models in total,
lems that require producing concrete answers; since             which we organize into two groups. (i) Re-
a Lean statement must be a theorem that requires                purposed models. Kimina-Prover-RL-1.7B and
a proof rather than a computational answer, we ap-              Kimina-Prover-Distill-8B (Wang et al., 2025),
pend each gold answer to its statement as a “Show               DeepSeek-Prover-V2-7B (Ren et al., 2025), and
that it is X” clause, turning the problem into a                Goedel-Prover-V2-8B (Lin et al., 2025) are spe-
closed proposition requiring a proof, as similarly              cialized theorem provers in Lean 4, and they are
done in prior work using Lean for answer selec-                 trained to generate a formal proof for a given for-
tion (Yao et al., 2025b; Liu et al., 2025a).                    mal statement. Although these are specialized
                  Edited NL Input                                                 Generated Lean
                     • Number edit            Autoformalization                    Formalization
                      • Symbol edit                                           theorem h : A → B := by
                     • Step deletion                                                      ···
                    (Edited version)                                         (Formal Statement and Proof)



                  Original NL Input                               Compare the output with:
                    (Original version)               (1) the edited version and (2) the original version




                                                                                           ?
                     Matches Edited           Matches Original Input             Neither / Unclear /
                         Input                (Ignores the edit / Reverts)          Unmatched
                     (Reflects the edit)
                                                Reverted Rate (RR)              Other / Unclear Rate
                   Faithful Rate (FR)          The model reverts to the                (OUR)
                    The model faithfully      original, unedited version.       Output is neither clearly
                  follows the edited input.                                      faithful nor reverted.


Figure 2: Overview of the faithfulness metrics for local perturbations. We compare each Lean output against both
the edited and original input and label it faithful (matches the edit), reverted (matches the original), or unclear
(neither). The Faithful (FR) and Reverted (RR) Rates are the shares of identifiable (faithful or reverted) outputs that
are faithful and reverted; the Other/Unclear Rate (OUR) is the unclear share of all outputs.


models for proof generation rather than autofor-                It constructs a directed acyclic graph (DAG) of
malization, given the scarcity of proof autoformal-             proof-step dependencies, formalizes intermediate
ization models, we follow Jana et al. (2025) and                lemmas, and then attempts to complete the proof
repurpose these models for proof autoformaliza-                 through these lemmas. We use each model’s own
tion with new prompts. Additionally, we adopt                   standard decoding settings (Appendix A.1) without
Gemini-3.1-Pro which is a general-purpose LLM                   performing any per-model hyperparameter search
and can thus be prompted to perform proof auto-                 of our own. All models generate a single output
formalization. (ii) Specialized proof autoformal-               per input; we do not consider multiple samples per
ization models. ProofBridge and ProofFlow are                   input (a.k.a. Pass@k), given the computational cost
the two models in our evaluation built specifically             of evaluation across various perturbations.
for proof autoformalization, in contrast to the re-                All semantic and faithfulness metrics (StmtSC,
purposed provers and the general-purpose LLM                    ProofSC, FR/RR/OUR) are assigned by Gemini-
above. ProofBridge (Jana et al., 2025) is trained               2.5-Flash, so that cross-model comparisons are
by Supervised Fine-tuning (SFT) from Kimina-                    not confounded by judge differences. Type check-
Prover-RL-1.7B on proof autoformalization data.                 ing uses Lean 4 (Moura and Ullrich, 2021) with a
Although ProofBridge is enhanced with a retrieval-              900-second per-problem timeout. Details are docu-
augmented approach which guides the autofor-                    mented in Appendix A.1.
malization with similar cases from the database,
this component has not been included in their re-               4.2    Robustness to Global Perturbations
leased code; we thus focus on the SFT model
in this work. Nevertheless, we do not expect                    Table 2 reports FullyCorrect on the original input
the retrieval-augmented approach to improve the                 and four semantic-preserving rewrites. A robust
robustness we study, as it uses extra references                autoformalizer should achieve comparable Fully-
from the database rather than the current NL in-                Correct across columns, but all the models eval-
put. ProofFlow (Cabral et al., 2025) is a formaliza-            uated show sensitivity to NL proof presentation.
tion pipeline designed to preserve proof structure.             On miniF2F, the variation can be large: Proof-
                                                                Bridge drops from 21.3% on Orig to 17.6% under
Table 2: Robustness of proof autoformalization models under global perturbations, measured by FullyCorrect (%)
on miniF2F and MATH-500 across five styles of natural-language proof inputs.

                                              miniF2F                              MATH-500
         Model
                                 Orig G-FF G-Step Q-FF Q-Step Orig G-FF G-Step Q-FF Q-Step
         Kimina-Prover-RL-1.7B 9.4 10.2        11.5      11.5    8.6   6.6 8.2      6.8    8.2    9.6
         Kimina-Prover-Distill-8B 19.3 16.0    16.4      19.7   16.0   19.8 16.4    16.8   16.8   19.0
         DeepSeek-Prover-V2-7B 1.2 8.6          7.4      12.7    8.6   8.2 7.4      5.8    6.4    5.0
         Goedel-Prover-V2-8B       1.2 2.5      4.1       3.7    4.1   4.4 2.0      2.0    3.8    3.0
         Gemini-3.1-Pro           17.2 21.7    18.9      21.7   22.5   26.4 23.6    24.6   23.8   23.8
         ProofBridge              21.3 19.7    18.4      17.6   17.6   13.4 14.4    12.6   14.8   15.2
         ProofFlow                 9.0 6.1      8.2       7.0    9.8   10.8 8.2      8.0    8.4   13.0



both Q-FF and Q-Step, while DeepSeek-Prover-               on these edits is only 6.3%. RR is above 90%
V2-7B rises from 1.2% on Orig to 12.7% on Q-FF.            in almost all corresponding cells. For example,
Gemini-3.1-Pro is the strongest model in aggregate         on miniF2F number-proof edits, Kimina-Prover-
on both datasets, yet its miniF2F score still ranges       Distill-8B has 94.7% RR and Gemini-3.1-Pro has
from 17.2% to 22.5% across styles.                         95.9% RR. ProofBridge and ProofFlow, which are
   Rewriting has mixed effects across models and           specialized proof autoformalization models, are
datasets. On miniF2F, rewrites can substantially           relatively more faithful on proof-level number and
improve some models: DeepSeek-Prover-V2-7B                 symbol edits. ProofBridge has 41.8% average FR
increases from 1.2% on Orig to 12.7% on Q-FF,              on these edits, and ProofFlow has 26.1%, both
Goedel-Prover-V2-8B from 1.2% to 4.1%, and                 higher than the 6.3% average of the other five mod-
Gemini-3.1-Pro from 17.2% to 22.5%. On MATH-               els. However, this advantage is still limited: even
500, however, the same kind of rewriting often             for these proof-level edits, both systems still re-
lowers performance: for example, Kimina-Prover-            vert in more than half of identifiable cases. Such
Distill-8B drops from 19.8% on Orig to 16.4–               reversion is consistent with the bias described in
19.0% on the rewrites, and Gemini-3.1-Pro drops            §3.2. A proof-level edit is only a local change,
from 26.4% to 23.6–24.6%. Thus, rewriting on               with the statement and most of the proof context
its own is neither uniformly helpful nor uniformly         unchanged. The input overall resembles a well-
harmful, and its effect depends on both the dataset        formed proof, and thus a Biased Autoformalizer
and the model.                                             tends to produce a plausible FL proof that is consis-
   Overall, no input style dominates uniformly, and        tent with the statement and the proof context, while
semantic-preserving rewrites can change both ab-           silently overriding the local edit.
solute scores and model rankings. For example, on             Step deletion shows a different pattern. Its FR is
miniF2F, ProofBridge is strongest on Orig, whereas         much higher than for proof-level number and sym-
Gemini-3.1-Pro is strongest on all four rewritten          bol edits, but reversion remains frequent. For ex-
styles. This indicates that current autoformalizers        ample, on miniF2F, step-deletion RR ranges from
are not stable under global perturbations with para-       48.2% to 75.2%, indicating that models still of-
phrased NL inputs, and that evaluations solely on a        ten fill in the removed reasoning step on their
fixed original style can substantially over- or under-     own. The model with the highest FR on step dele-
state a model’s true autoformalization ability.            tion is Kimina-Prover-RL-1.7B, with 51.8% FR on
                                                           miniF2F and 70.7% on MATH-500, though this
4.3   Faithfulness under Local Perturbations               may partly reflect its limited ability to infer miss-
We use the three local perturbations of §3.2, each         ing reasoning owing to its smaller size rather than
testing a specific faithful behavior. Tables 3 and 4       genuinely better faithfulness.
summarize FR (the higher the better) and RR (the              Statement edits are much easier for models to fol-
lower the better) across proof-level and statement-        low than proof edits. For every model, FR is higher
level local perturbations, respectively.                   when the same type of edit is made in the state-
   Models are least faithful on proof-level num-           ment rather than in the proof. For example, Proof-
ber and symbol edits. For the five models other            Bridge goes from 39.4%/44.9% FR on miniF2F
than ProofBridge and ProofFlow, the average FR             proof-level number/symbol edits to 78.6%/80.0%
Table 3: FR/RR results (%) for proof-level local perturbations, computed over identifiable outputs (faithful or
reverted). Unclear outputs that neither faithful nor reverting are excluded; their fraction is reported in the appendix.

                                   Number edit                        Symbol edit                    Step deletion
 Model                        miniF2F       MATH-500           miniF2F        MATH-500        miniF2F        MATH-500
                            FR (↑) RR (↓) FR (↑) RR (↓) FR (↑) RR (↓) FR (↑) RR (↓) FR (↑) RR (↓) FR (↑) RR (↓)
 Kimina-Prover-RL-1.7B      7.3    92.7     5.2     94.8      3.6     96.4    8.1    91.9    51.8    48.2    70.7    29.3
 Kimina-Prover-Distill-8B   5.3    94.7     2.9     97.1      8.3     91.7    3.1    96.9    25.9    74.1    51.3    48.7
 DeepSeek-Prover-V2-7B      8.3    91.7     6.4     93.6      7.9     92.1    8.5    91.5    48.4    51.6    53.6    46.4
 Goedel-Prover-V2-8B        10.1   89.9     6.6     93.4      2.6     97.4    9.2    90.8    43.7    56.3    60.9    39.1
 Gemini-3.1-Pro             4.1    95.9     6.3     93.7      8.3     91.7    4.1    95.9    47.4    52.6    56.9    43.1
 ProofBridge                39.4   60.6    41.4     58.6      44.9    55.1    41.4   58.6    33.7    66.3    53.8    46.2
 ProofFlow                  32.6   67.4    24.4     75.6      27.0    73.0    20.2   79.8    24.8    75.2    33.8    66.2

Table 4: FR/RR results (%) for statement-level local perturbations, computed over identifiable outputs (faithful or
reverted). Unclear outputs are excluded; their fraction is reported in the appendix.

                                                       Number edit                   Symbol edit
                   Model                          miniF2F      MATH-500        miniF2F      MATH-500
                                                  FR    RR      FR     RR      FR    RR     FR      RR
                   Kimina-Prover-RL-1.7B       82.9    17.1    62.4    37.6   90.4   9.6    82.8    17.2
                   Kimina-Prover-Distill-8B    75.0    25.0    49.1    50.9   83.1   16.9   67.2    32.8
                   DeepSeek-Prover-V2-7B       66.3    33.7    48.1    51.9   73.8   26.2   69.4    30.6
                   Goedel-Prover-V2-8B         58.9    41.1    44.6    55.4   73.1   26.9   59.3    40.7
                   Gemini-3.1-Pro              22.8    77.2    14.2    85.8   23.3   76.7   26.9    73.1
                   ProofBridge                 78.6    21.4    57.4    42.6   80.0   20.0   70.8    29.2
                   ProofFlow                   52.8    47.2    49.3    50.7   64.8   35.2   57.7    42.3


on statement-level edits. Gemini-3.1-Pro also rises             sample of 100 (original, rewrite) pairs, covering the
from 4.1%/8.3% to 22.8%/23.3%. This is consis-                  four rewrite styles across both datasets, confirms
tent with the bias described above: since a Biased              that each of the edits changes only the wording
Autoformalizer tends to produce an FL proof con-                while preserving all values, claims, reasoning steps,
sistent with the statement, an edit in the statement            and semantic meanings. The detailed procedure is
is naturally more likely to be reflected in the output.         given in Appendix A.5.

4.4   Perturbation Reliability
To ensure the validity of the results under con-                5     Conclusion
structed perturbations, we carefully checked the
quality of the perturbations. A local edit should               This work studies the robustness of proof autofor-
change only the targeted number, symbol, or step,               malization under global paraphrases and local edits.
leaving the rest of the input untouched. We ver-                Our results on seven recent models reveal two types
ify this with an automated script that compares                 of robustness failures: under global perturbations,
every edited input against its original character by            the models are unstable when exposed to semantic-
character: in all 2,637 cases the two differ in ex-             preserving changes in NL proof inputs; under local
actly one contiguous span (the intended edit) and               perturbations, they often fail to faithfully reflect
are otherwise identical (100%). For global per-                 local edits. Our findings suggest that proof autofor-
turbations, an automated script check finds that                malization should be evaluated beyond correctness
96.4% of all 2,976 rewrites preserve every numeric              on well-formed proofs from standard datasets; ro-
and symbolic token of the original, with the re-                bustness to NL proofs of varying styles and qual-
maining 3.6% having formatting differences (digit               ity should be considered in future development to
grouping, numbers spelled out, and similar) but                 build reliable proof autoformalizers that can enable
not content changes. A manual audit of a stratified             broader applications.
Acknowledgement                                           Rafael Cabral, Tuan Manh Do, Xuejun Yu, Wai Ming
                                                            Tai, Zijin Feng, and Xin Shen. 2025. Proofflow: A
This work is supported in part by an NVIDIA Aca-            dependency graph approach to faithful proof autofor-
demic Grant award.                                          malization. arXiv preprint arXiv:2510.15981.
   This work used the Delta system at the National        Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao,
Center for Supercomputing Applications [award               Zihan Qin, Tianyi Xu, and Bin Dong. 2024. Herald:
OAC 2005572] through allocation CIS250704 from              A natural language annotated lean 4 dataset. arXiv
                                                            preprint arXiv:2410.10878.
the Advanced Cyberinfrastructure Coordination
Ecosystem: Services & Support (ACCESS) pro-               Goedel-LM. 2025a.         Goedel-formalizer-v2-
gram, which is supported by National Science                8b.      https://huggingface.co/Goedel-LM/
Foundation grants #2138259, #2138286, #2138307,             Goedel-Formalizer-V2-8B. Hugging Face model
                                                            card.
#2137603, and #2138296.
   This work used resources available through the         Goedel-LM. 2025b.         Goedel-prover-v2-8b.
National Research Platform (NRP) at the Univer-             https://huggingface.co/Goedel-LM/
sity of California, San Diego. NRP has been devel-          Goedel-Prover-V2-8B.   Hugging Face model
                                                            card.
oped, and is supported in part, by funding from Na-
tional Science Foundation, from awards 1730158,           Google. 2025. Gemini 2.5 flash. https://cloud.
1540112, 1541349, 1826967, 2112167, 2100237,                google.com/vertex-ai/generative-ai/docs/
and 2120019, as well as additional funding from             models/gemini/2-5-flash. Google Cloud model
                                                            documentation.
community partners.
                                                          Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
Limitations                                                 Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shi-
                                                            rong Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.
Our study has several limitations that suggest direc-       Deepseek-r1: Incentivizing reasoning capability in
                                                            llms via reinforcement learning. arXiv preprint
tions for future work. First, the evaluated datasets        arXiv:2501.12948.
consist of mathematical competition problems and
undergraduate-level mathematics, which provide            Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W
a controlled setting; we have not yet extended the           Ayers, and Stanislas Polu. 2021. Proof artifact co-
                                                             training for theorem proving with language models.
study to more advanced domains. Second, we tar-              arXiv preprint arXiv:2102.06203.
get only the Lean 4 proof assistant; extending the
benchmark to other systems such as Isabelle and           Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
Coq is also valuable. Third, we study three local           Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
                                                            cob Steinhardt. 2021. Measuring mathematical prob-
perturbation types (number, symbol, and proof-step          lem solving with the MATH dataset. In Proceedings
edits) and two global rewriting styles; a wider range       of the Neural Information Processing Systems Track
of edits and styles could be explored. Lastly, our          on Datasets and Benchmarks (NeurIPS Datasets and
perturbations are generated independently of the            Benchmarks).
models being evaluated, but stronger ones may be          Xiaolin Hu, Qinghua Zhou, Bogdan Grechuk, and
generated adversarially with respect to the models.         Ivan Y Tyukin. 2025. Stepproof: Step-by-step ver-
We leave these extensions to future work.                   ification of natural language mathematical proofs.
                                                            arXiv preprint arXiv:2506.10558.

                                                          Prithwish Jana, Piyush Jha, Haoyang Ju, Gautham
References                                                   Kishore, Aryan Mahajan, and Vijay Ganesh. 2023.
                                                             Cotran: An llm-based code translator using reinforce-
Zhangir Azerbayev, Bartosz Piotrowski, Hailey                ment learning with feedback from compiler and sym-
  Schoelkopf, Edward W Ayers, Dragomir Radev, and            bolic execution. arXiv preprint arXiv:2306.06755.
  Jeremy Avigad. 2023. Proofnet: Autoformalizing
  and formally proving undergraduate-level mathemat-      Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi,
  ics. arXiv preprint arXiv:2302.12433.                      Cruise Song, Sriram Vishwanath, and Vijay Ganesh.
                                                             2025. Proofbridge: Auto-formalization of natural
Bruno Barras, Samuel Boutin, Cristina Cornes, Judi-          language proofs in lean via joint embeddings. arXiv
  caël Courant, Yann Coscoy, David Delahaye, Daniel          preprint arXiv:2510.15681.
  de Rauglaudre, Jean-Christophe Filliâtre, Eduardo
  Giménez, Hugo Herbelin, and 1 others. 1999. The         Albert Q Jiang, Wenda Li, and Mateja Jamnik. 2023a.
  coq proof assistant reference manual. INRIA, version,     Multilingual mathematical autoformalization. arXiv
  6(11):17–21.                                              preprint arXiv:2311.03755.
Albert Q Jiang, Wenda Li, and Mateja Jamnik. 2024.          Stanislas Polu and Ilya Sutskever. 2020. Generative
  Multi-language diversity benefits autoformalization.         language modeling for automated theorem proving.
  Advances in Neural Information Processing Systems,           arXiv preprint arXiv:2009.03393.
  37:83600–83626.
                                                            Qwen Team. 2026. Qwen3.5-397b-a17b. https:
Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han,           //huggingface.co/Qwen/Qwen3.5-397B-A17B.
  and Yuhuai Wu. 2021. Lisa: Language models of              Hugging Face model card.
  isabelle proofs. In 6th Conference on Artificial Intel-
  ligence and Theorem Proving, pages 378–392.               ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
                                                              Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,            Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.
  Timothée Lacroix, Jiacheng Liu, Wenda Li, Mateja            Deepseek-prover-v2: Advancing formal mathemati-
  Jamnik, Guillaume Lample, and Yuhuai Wu. 2023b.             cal reasoning via reinforcement learning for subgoal
  Draft, sketch, and prove: Guiding formal theorem            decomposition. arXiv preprint arXiv:2504.21801.
  provers with informal proofs. In International Con-
  ference on Learning Representations.                      Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
                                                              Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-          Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-
  son Edwards, Bowen Baker, Teddy Lee, Jan Leike,             ers. 2025. Kimina-prover preview: Towards large
  John Schulman, Ilya Sutskever, and Karl Cobbe.              formal reasoning models with reinforcement learn-
  2024. Let’s verify step by step. In International           ing. arXiv preprint arXiv:2504.11354.
  Conference on Learning Representations, volume
  2024, pages 39578–39601.                                  Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe
                                                              Diao, Renjie Pi, and Tong Zhang. 2024. Theoreml-
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-            lama: Transforming general-purpose llms into lean4
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,               experts. In Proceedings of the 2024 Conference on
  Jiawei Ge, Jingruo Sun, and 1 others. 2025. Goedel-         Empirical Methods in Natural Language Processing,
  prover-v2: Scaling formal theorem proving with              pages 11953–11974.
  scaffolded data synthesis and self-correction. arXiv
  preprint arXiv:2508.03613.                                Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
                                                              Rabe, Charles Staats, Mateja Jamnik, and Christian
Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu,             Szegedy. 2022. Autoformalization with large lan-
  Zaoyu Chen, Yasheng Wang, Lifeng Shang, Qun Liu,            guage models. Advances in neural information pro-
  and Ming Zhang. 2025a. Safe: Enhancing mathemat-            cessing systems, 35:32353–32368.
  ical reasoning in large language models via retrospec-
  tive step-aware formal verification. arXiv preprint       Yutong Wu, Di Huang, Wenxuan Shi, Wei Wang, Yewen
  arXiv:2506.04592.                                           Pu, Lingzhe Gao, Shihao Liu, Ziyuan Nan, Kaizhao
                                                              Yuan, Rui Zhang, and 1 others. 2025. Inversec-
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and            oder: Self-improving instruction-tuned code llms
  Junchi Yan. 2025b. Rethinking and improving auto-           with inverse-instruct. In Proceedings of the AAAI
  formalization: Towards a faithful metric and a depen-       Conference on Artificial Intelligence, volume 39,
  dency retrieval-based approach. In The Thirteenth           pages 25525–25533.
  International Conference on Learning Representa-
  tions.                                                    Yutong Wu, Di Huang, Ruosi Wan, Yue Peng, Shijie
                                                              Shang, Chenrui Cao, Lei Qi, Rui Zhang, Xishan
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,         Zhang, Zidong Du, and 1 others. 2026. Stepfun-
   Jing Xiong, Chengwu Liu, Jianhao Shen, Hui Jin,            formalizer: Unlocking the autoformalization poten-
   Jipeng Zhang, Haiming Wang, and 1 others. 2024.            tial of llms through knowledge-reasoning fusion. In
   Process-driven autoformalization in lean 4. arXiv          Proceedings of the AAAI Conference on Artificial
   preprint arXiv:2406.01940.                                 Intelligence, volume 40, pages 33980–33988.

Leonardo de Moura and Sebastian Ullrich. 2021. The          Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  lean 4 theorem prover and programming language. In          Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  International Conference on Automated Deduction,            Xiaodan Liang. 2024. Deepseek-prover: Advancing
  pages 625–635. Springer.                                    theorem proving in llms through large-scale synthetic
                                                              data. arXiv preprint arXiv:2405.14333.
Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-
  son. 2002. Isabelle/HOL: a proof assistant for            Jiarui Yao, Ruida Wang, and Tong Zhang. 2025a. Fans:
  higher-order logic. Springer.                                Formal answer selection for llm natural language
                                                               math reasoning using lean4. In Proceedings of the
Auguste Poiroux, Gail Weiss, Viktor Kunčak, and An-           2025 Conference on Empirical Methods in Natural
  toine Bosselut. 2025. Reliable evaluation and bench-         Language Processing, pages 3181–3200.
  marks for statement autoformalization. In Proceed-
  ings of the 2025 Conference on Empirical Methods in       Jiarui Yao, Ruida Wang, and Tong Zhang. 2025b.
  Natural Language Processing, pages 17958–17980.              FANS: Formal answer selection for LLM natural
  language math reasoning using Lean4. In Proceed-
  ings of the 2025 Conference on Empirical Methods
  in Natural Language Processing, pages 3181–3200.
  Association for Computational Linguistics.
Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
  Dahua Lin, and Kai Chen. 2024. Lean workbook:
  A large-scale lean problem set formalized from nat-
  ural language math problems. Advances in Neural
  Information Processing Systems, 37:105848–105863.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  2021. Minif2f: a cross-system benchmark for for-
  mal olympiad-level mathematics. arXiv preprint
  arXiv:2109.00110.
A     Appendix                                         LLM judge. We use Gemini-2.5-Flash (Google,
                                                       2025) (model identifier gemini-2.5-flash) to as-
A.1    Implementation Details                          sign StmtSC, ProofSC, and FR/RR/OUR. Using
Inference. All models run zero-shot from one           the same judge for every metric keeps cross-model
fixed autoformalization prompt, with no hyperpa-       rankings from being affected by differences be-
rameter search. We serve the open-weight single-       tween judges.
stage models (Kimina-Prover-RL-1.7B, Kimina-
                                                       Lean toolchain. We check type correctness with
Prover-Distill-8B, ProofBridge, DeepSeek-Prover-
                                                       Lean 4.15.0 and Mathlib v4.15.0, through a persis-
V2-7B, and Goedel-Prover-V2-8B) with vLLM,
                                                       tent Lean REPL that keeps Mathlib loaded across
generating one sample per input under our Pass@1
                                                       calls. Each type-check has a per-problem timeout
evaluation setting. Gemini-3.1-Pro is queried
                                                       of 900 seconds.
through its API.
   For ProofFlow, we use the released dependency-      Reproducibility. The (anonymized) project
DAG pipeline but adapt its component models            repository contains all perturbation datasets
and output interface to our evaluation. The            (number, symbol, and step-deletion edits across
graph builder is Gemini-2.5-Flash, and the             miniF2F and MATH-500), the scored output files
lemma formalizer and tactic completer are              for every model and condition, the human-audit
Goedel-LM/Goedel-Formalizer-V2-8B               (Lin   task files, and the inference and judge prompts
et al., 2025; Goedel-LM, 2025a) and                    (also in Appendix A.3.4).
Goedel-LM/Goedel-Prover-V2-8B (Lin et al.,
2025; Goedel-LM, 2025b).          We keep DAG          Licenses and terms. We use each artifact
following, previous formal context, and supplying      under its public license, and each proprietary
the original informal proof enabled. We use            API under its service terms.       The Lean 4
three retries for graph construction, lemma            toolchain, Mathlib, and the Lean version of
formalization, and proving, and set the internal       miniF2F are released under Apache-2.0. The
ProofFlow pass budget to three; this is smaller        MATH dataset, from which MATH-500 is
than the retry budget used in some released            derived, is released under the MIT license.
ProofFlow benchmark scripts, which use more            The ProofBridge and ProofFlow codebases are
attempts for formalization and proving. To avoid       released under the MIT license. The open-weight
giving ProofFlow credit for partial intermediate       checkpoints     AI-MO/Kimina-Prover-RL-1.7B,
progress, our adapter exports only verified final      AI-MO/Kimina-Prover-Distill-8B, Goedel-
Lean theorems to the downstream TC/SC pipeline.        LM/Goedel-Prover-V2-8B, Goedel-LM/Goed
If ProofFlow formalizes intermediate lemmas but        el-Formalizer-V2-8B, and Qwen/Qwen3.5-3
does not verify a final theorem, we treat the output   97B-A17B are released under Apache-2.0. For
as an error. We do not report ProofFlow’s original     deepseek-ai/DeepSeek-Prover-V2-7B, the
ProofScore; instead, all models are evaluated with     repository code is MIT-licensed, while the model
the same TC, StmtSC, ProofSC, FullyCorrect, FR,        weights are governed by the DeepSeek Model
RR, and OUR metrics.                                   License. Gemini-3.1-Pro and Gemini-2.5-Flash
                                                       are proprietary models that we access through
Compute budget. All the main experiments runs          Google’s Gemini API and use subject to the Gem-
on a cluster with NVIDIA A100 (40/80 GB), H200,        ini API terms. We use all artifacts and services
and A40 GPUs. We estimate the project’s total cost     for non-commercial research evaluation, and
at about 1,900 GPU-hours. Roughly half is LLM          we release our perturbation datasets, evaluation
inference: the five open-weight models served with     prompts, and evaluation code under the MIT
vLLM, plus the multi-stage ProofFlow pipeline          license.
(a graph model, a formalizer, and a solver with
intermediate Lean checking), which is by far the       A.2   Perturbation Construction Details
most expensive per problem. The rest is Lean type-     This section explains how we build the two kinds
checking on GPU nodes, together with develop-          of perturbations from §3.1 and §3.2.
ment runs. Gemini-3.1-Pro and the Gemini-2.5-
Flash judge run through a hosted API and are not       Global perturbations. For each problem we
in this GPU total.                                     produce four semantic-preserving rewrites of the
natural-language statement and proof: two free-             each deletable step into a quality tier (gold, silver,
form rephrasings (G-FF, Q-FF) and two numbered              or bronze) by how readable its outcome is (capi-
step-by-step rewrites (G-Step, Q-Step), generated           talization, English words, and a proper sentence
by Gemini-2.5-Flash and Qwen3.5-397B-A17B.                  ending). It selects the top step by a fixed, determin-
Both prompts (Appendix A.3.1) start with a shared           istic ranking: tier first, then a reasoning-substance
set of rules: do not change any number, symbol,             score (whether the reasoning contains mathematics
hypothesis, or logical step, and keep the rewrite           and a substantive verb), then outcome readability,
within ±30% of the original length. Together with           then reasoning length. Finally, the script removes
the original input, this gives five styles per problem.     the chosen step’s reasoning while keeping its stated
                                                            outcome, and requires the deletion to remove be-
Local perturbations. All three local edit types
                                                            tween 0.5% and 80% of the proof. Step deletions
share the same three-stage pipeline. First, an LLM
                                                            apply to the proof only.
(Gemini-2.5-Flash) labels candidate edit locations.
Second, we filter the candidates and pick one per
region, where a region is the statement or the proof
(so a problem can receive both a statement edit and
a proof edit). Third, a deterministic rule writes
the edited text as a single-span substitution at the
recorded character offset.
                                                            A.3     Prompt Templates
Number edits. The labeler marks every editable
number in the statement and proof, skipping struc-
tural numbers (subscripts, superscripts, indices)
and numbers inside LaTeX formatting arguments.
We pick one per region. A SHA256-seeded deter-              This appendix collects all prompts used in our
ministic rule then sets the new value: it shifts the        pipeline: the perturbation rewriting prompts,
number by an amount that scales with its size (for          the autoformalization prompt, and the semantic-
example, an integer up to 10 changes by 1 to 3, and         correctness and faithfulness judge prompts.
one up to 100 by 1 to 5) and keeps the sign, so the
edited problem stays well-formed.
Symbol edits. The labeler marks relation and
operator symbols (other than = and ̸=) and tags
each as a relation or an operator. We swap each
one by a fixed table: relations flip direction (<↔>,
≤↔≥) and operators go to their inverse (+ ↔ −,              A.3.1    Perturbation Rewriting Prompts
× ↔ ÷). We skip symbols inside relation chains
(e.g., 0 < p < 15) and inside subscripts or super-
scripts, and we oversample relations to keep the
relation/operator mix balanced.                             We first give the shared rules that every semantic-
Step deletions. The labeler (the LLM) does the              preserving rewrite must follow, then the two
language-level work: it splits each proof into steps,       prompts that generate the global perturbations.
splits each step into a reasoning part and an out-
come, and flags whether the step is deletable. A
step is flagged deletable only if the reasoning is
substantive (not a filler connective such as “thus”
or “we have”) and the outcome stands on its own:
it must be a contiguous substring of the step, must
not start with a dangling or anaphoric fragment             Shared rewriting rules. These rules are
(e.g. “which. . . ”, “this gives. . . ”), and must not be   prepended to both rewriting prompts below. They
a bare number or symbol. Everything after this is           require the rewrite to keep the original meaning,
a deterministic script with no further LLM calls.           length, and logical steps, and to avoid fixing or
The script re-checks these hard rules, then sorts           extending the original.
  Shared Rewriting Rules                                Step-by-Step Rewriting Prompt
  This is a MEANING-PRESERVING transformation.          You are a mathematics professor. Faithfully translate
  Your rewrite must be a faithful translation of        the following problem statement and its proof into a
                                                        numbered step-by-step format. This is a pure formatting
  the original — a reader must be able to recover       change: break the existing content into numbered steps
  the original’s exact mathematical content from        with short bold step titles. Do NOT add explanations,
  your version. Specifically:                           details, motivation, or any content that is not already in
                                                        the original — only reorganize what is there.
 - Do NOT change any numerical constant,
                                                        The proof should follow this structure:
 variable name, function name, set, inequality          1.   **Step Title:** <content taken directly from the
  direction, or quantifier.                             original>
 - Do NOT change, weaken, strengthen, or                2.   **Step Title:** <content taken directly from the
  generalize the hypotheses or the conclusion.          original>
 - Do NOT add new mathematical facts, lemmas,           The statement may use the same numbered-step format if
  intermediate results, or justifications that          it naturally decomposes, or remain as a single paragraph
 were not in the original.                              if it does not — but its mathematical content must stay
                                                        identical.
 - Do NOT remove, merge, or reorder logical
  steps of the original argument.                      {faithfulness_rules}
 - Do NOT fix or “clean up” the original. If            Original problem statement:
  the original is awkward, incomplete, or even          %STATEMENT%
 wrong, preserve it faithfully — your job is
                                                        Original proof:
  translation, not editing.                             %PROOF%
 - The rewritten version should be roughly the
  same length as the original, within ±30%.
                                                      A.3.2 Autoformalization Prompts
  Use LaTeX math notation exactly as in the
  original, e.g., x2 , \frac{a}{b}, \neq, \notin,     We use the following system and user prompts to
  \tan. Write every backslash literally as a          autoformalize each natural-language statement and
  single backslash — do NOT escape them, do NOT       proof into a Lean 4 theorem together with its proof.
  wrap anything in JSON, do NOT add code fences.
 Output format — return EXACTLY these two               Autoformalization System Prompt
 tagged blocks and NOTHING else before
 or after.       Your entire response must              You are an expert in mathematics. Your task is
 start with <informal_statement> and end with           to convert informal, natural-language proofs
 </informal_proof>.                                     into correct Lean 4 formalizations.

 <informal_statement>                                   Autoformalization User Prompt
 ... rewritten problem statement ...
 </informal_statement>                                  Your task is to take as input an informal
 <informal_proof>                                       proof in natural language and autoformalize it
 ... rewritten proof ...                                in Lean 4 with a header. Think step-by-step
 </informal_proof>                                      and ensure that the output formal theorem is
                                                        compilable with Lean 4 (version 4.15.0).

   We use the following prompt to generate global      {example_block}
perturbations by paraphrasing, while preserving the     Here is the **actual** informal proof in
                                                        natural language:
original mathematical meaning.
                                                       <informal_statement>
  paraphrasing Prompt                                  {informal_statement}
                                                       </informal_statement>
  You are a mathematics professor. Paraphrase
  the following problem statement and its proof        <informal_proof>
  into different wording while preserving the          {informal_proof}
  exact same mathematical meaning. Change only         </informal_proof>
  the phrasing, sentence structure, and word            Now first think step-by-step for the actual
  choice; keep every mathematical object, value,        output and autoformalize it in Lean 4 with a
  and logical step identical.                           header. Importantly, enclose the final formal
 {faithfulness_rules}                                   proof in Lean 4 inside the following tags:

  Original problem statement:                           <formal_proof>
  %STATEMENT%                                           ```lean4
                                                        (Provide your entire Lean 4 proof with header
  Original proof:                                       here)
  %PROOF%                                               ```
                                                        </formal_proof>
   We use the following prompt to convert the orig-
inal natural-language statement and proof into a      A.3.3 Semantic Correctness Judge Prompts
numbered step-by-step format while preserving the     We use two judges to score semantic correctness,
original mathematical content.                        one for the proof and one for the statement. The
first checks whether the generated Lean proof is    theorem statement expresses the same claim as the
semantically consistent with the natural-language   natural-language statement.
proof.

  Proof Semantic Correctness Judge Prompt
 You are an expert in formal mathematics and
 Lean 4. Judge ONE thing:
 Do the following two pieces of reasoning carry
 out the SAME LOGICAL STEPS?                          Statement Semantic Correctness Judge
                                                      Prompt
  === CRITICAL — Independence from validity ===
                                                     You are an expert in formal mathematics and
 You are shown a natural-language proof and a
                                                     Lean 4.
 sequence of Lean 4 proof tactics. You are
                                                     Does the following Lean 4 theorem signature
 NOT shown the Lean theorem statement that
                                                     express the same mathematical proposition as
 these tactics target. This is intentional and
                                                     the natural-language statement?
 important.
 Your job is to compare the two REASONING             === Equivalence criteria ===
 SEQUENCES on their own merit:
                                                     Two statements are equivalent if they capture
 - Whether the Lean tactics actually prove the       the same mathematical content, even if they
  hidden Lean theorem is checked separately by       differ in surface form:      variable names,
  Lean’s type checker. You MUST IGNORE that          quantifier order when commutative,   notation
  question entirely. The tactics may or may not
                                                                                   P
                                                     such as \le vs ≤, \sum vs       , or how the
  prove the theorem they are attached to — that      conclusion is phrased.
  is not your concern.                               Use your mathematical understanding to judge
                                                     whether the two statements describe the same
 - Even if the Lean tactics seem to refer to
                                                     problem.
  a different goal than the NL proof suggests,
  evaluate the reasoning sequence on its own          === Note on inputs ===
  terms.
                                                     You are shown the Lean theorem signature,
  === Equivalence criteria ===                       including binders and goal type, only; the
                                                     Lean proof body is hidden because it is judged
 Two proofs are equivalent if they follow the
                                                     separately.
  SAME OVERALL STRATEGY and the substantive
  intermediate claims agree, modulo:                  === Output ===
 - wording and step ordering,
 - level of abstraction.         Lean tactics         Provide a clear justification, then output:
  may IMPLEMENT abstract NL principles such          <stmt_justification>your            reasoning
  as AM-GM, Cauchy-Schwarz, or trigonometric         here</stmt_justification>
  identities via automation tactics like             <stmt_score>1 or -1</stmt_score>
  nlinarith, polyrith, or positivity.      This
  counts as the SAME step, not a different one.       === Inputs ===
 They are NOT equivalent if:                         Natural-language statement:
 - they use a fundamentally different strategy       {nl_statement}
  or prove a different goal,
                                                     Lean 4 theorem signature:
 - the Lean proof body is empty, sorry, admit,
                                                     {lean_theorem_signature}
  or a degenerate placeholder,
 -    the   substantive   intermediate  claims
  disagree.
  === Output ===
  First, briefly map each substantive NL step
  to a corresponding Lean tactic, or note where
  they disagree. Then output:
 <proof_justification>your        step-by-step
 correspondence here</proof_justification>
 <proof_score>1 or -1</proof_score>
  === Inputs ===                                    A.3.4   Faithfulness Judge Prompts
 Natural-language proof:
 {nl_proof}
 Lean 4 proof tactics, with theorem signature
 deliberately hidden:
 {lean_proof_body}
                                                    Number edits. This judge decides whether the
  The second checks whether the generated Lean      Lean output reflects the edited number.
 Number-Edit Faithfulness Judge Prompt              Symbol-Edit Faithfulness Judge Prompt
 You   are    an   expert  in  mathematical         You   are    an   expert  in   mathematical
 formalization.      Given a math problem           formalization.      Given a math problem
 (whose natural language has been edited            (whose natural language has been edited by
 by changing one number) and a fragment of          changing one math symbol) and a fragment of
 the model-generated Lean 4 formalization,          the model-generated Lean 4 formalization,
 determine whether the model faithfully             determine whether the model faithfully
 reflects the number edit.                          reflects the symbol edit.
 The Lean fragment shown below is the ONLY part     The Lean fragment shown below is the ONLY part
 of the formalization you should consider. It       of the formalization you should consider. It
 is the region targeted by the edit ({source}).     is the region targeted by the edit ({source}).
 Do not infer or imagine any other Lean code.       Do not infer or imagine any other Lean code.
 Base your judgment strictly on the fragment.       Base your judgment strictly on the fragment.
 === Edit Info ===                                  === Edit Info ===
 Edit type: {edit_type}; Original number:          Edit type: {edit_type}; Original symbol:
 {old_value}; Edited number:   {new_value};        {old_symbol}; Edited symbol: {new_symbol};
 Edit location:    {source}; Edit context:         Symbol family:     {family}; Edit location:
 “{context}”.                                      {source}; Edit context: “{context}”.
 === Inputs ===                                     === Inputs ===
 Edited           informal          statement:     Edited           informal          statement:
 {informal_statement}                              {informal_statement}
 Edited informal proof: {informal_proof}           Edited informal proof: {informal_proof}
 Model-generated Lean 4 fragment ({source}         Model-generated Lean 4 fragment ({source}
 region only): {generated_fl}                      region only): {generated_fl}
 === Tasks ===                                      === Tasks ===
 1. In the Lean fragment, find the number that      1. In the Lean fragment, find the math symbol
 semantically corresponds to “{new_value}” or       corresponding to the edited symbol in the edit
 “{old_value}” in the edit context. Numbers in      context. Symbol mapping from LaTeX to Lean:
 Lean may differ from natural language; e.g.,       \geq or >= → >=; \leq or <= → <=; > → >; <
 6.5 may appear as 13/2, and 65 may appear as       → <; \neq or != → != or Ne; + → +; - → -;
 (65 : R).                                          \times or \cdot → *; \div → /. Note: a > b
                                                    in Lean may equivalently be written as b < a.
 2. Determine the number at that position:
 if it is {new_value} (or an equivalent form)      2. Determine the symbol at that position:
 → “faithful”; if it is {old_value} (or            if it is the Lean equivalent of {new_symbol}
 an equivalent form) → “reverted”; if the          → “faithful”; if it is the Lean equivalent
 corresponding position cannot be found, or it     of {old_symbol} → “reverted”; otherwise →
 is some other value → “other”.                    “other”.
 IMPORTANT — ground your judgment in evidence;     IMPORTANT — ground your judgment in evidence;
 do not hallucinate.         Before returning      do not hallucinate.          Before returning
 “faithful” or “reverted”, you MUST be able to     “faithful” or “reverted”, you MUST be able to
 point to the literal substring of the fragment    point to the literal substring of the fragment
 where the value appears. If you cannot find       where the symbol appears.       If you cannot
 such a substring, return value_in_fl="" and       find such a substring, return value_in_fl=""
 judgment="other".    The context_in_fl field      and judgment="other". The context_in_fl field
 below is the proof — it must be copied            below is the proof — it must be copied verbatim
 verbatim from the fragment and must contain       from the fragment.
 value_in_fl.
                                                    === Output (strict JSON only) ===
 === Output (strict JSON only) ===
                                                   {“found_in_fl”: true/false,
 {“found_in_fl”: true/false,                         “value_in_fl”: “copy the symbol from the
   “value_in_fl”: “copy the number from the        fragment as-is (or empty string if not
 fragment as-is (or empty string if not            found)”,
 found)”,                                            “context_in_fl”:    “∼40-character window
   “context_in_fl”:     “if value_in_fl is         surrounding the symbol, or empty string”,
 non-empty, copy the ∼40-character window            “judgment”: “faithful”/“reverted”/“other”,
 surrounding the value;      otherwise empty         “reason”: “one-sentence explanation”}
 string”,
   “judgment”: “faithful”/“reverted”/“other”,
   “reason”: “one-sentence explanation”}

                                                  Step deletion. This judge decides whether the
Symbol edits. This judge decides whether the      Lean output reflects the deleted step or instead re-
Lean output reflects the edited symbol.           constructs it.
  Step-Deletion Faithfulness Judge Prompt             faithful or reverted. Inspecting a large sample of
  You    are   an    expert    in    mathematical     these outputs, we find a few recurring patterns. A
  formalization.     A math proof was edited          small portion are degenerate, where the targeted
  by removing the reasoning from one proof step       region contains no theorem at all, or the output is
  while keeping only the step’s outcome/claim.
  The model then generated a Lean 4 formalization     empty or an error. The rest are genuine formaliza-
  from the edited proof.                              tions in which the edited value never appears at the
  Determine whether the model         faithfully      target position, neither the new value nor the origi-
  reflects the missing reasoning.                     nal one. This is most common in proof edits, where
  === Edit Info ===                                   the proof is closed by an automation tactic such as
  Deleted   reasoning:      “{reasoning_text}”;       norm_num, ring, or linarith that never writes the
  Preserved outcome: “{outcome_text}”; Step was       value out, or reaches the goal by a different route.
  last step: {is_last}.                               For instance, in the proof edit that changes 49 to
  === Inputs ===                                      48 in amc12a_2020_p7, one model’s entire proof
 Edited informal proof (reasoning removed):           is := by norm_num, so neither value shows up and
 {informal_proof}                                     we label the output Other. Step deletion behaves
 Model-generated Lean 4 code: {generated_fl}
                                                      the same way: the deleted step’s result usually ap-
  === Tasks ===                                       pears nowhere in the Lean. In short, Other/Unclear
  1.       Find where the outcome claim               means the edit left no trace in the output, not that
  (“{outcome_text}”) is formalized in the Lean
  code.    Look for a have, show, theorem             we faced a hard faithful-versus-reverted call.
  conclusion, or equivalent statement.                   Table 5 reports the identifiable fraction (1 minus
 2. Determine how the model handles the proof         OUR) for each model and condition. It is highest
 of that claim: if the model uses sorry,              for statement edits, in the middle for step deletion,
 admit, leaves it incomplete, or provides a
 significantly simplified/placeholder proof →
                                                      and lowest for proof-level number and symbol edits,
 “faithful” (reflected the missing reasoning);        where an automation tactic usually closes the proof
 if the model provides a full substantive             without writing the edited value.
 tactic proof reconstructing the deleted
 reasoning → “reverted” (fabricated the
 missing justification); if the outcome claim         A.5   Reliability Validation
 is not present, or the output is empty/error
 → “other”.                                           We check three things: that the perturbations
                                                      (§4.4) are constructed correctly, that the semantic-
 IMPORTANT — ground your judgment in evidence;
 do not hallucinate.        Before returning          correctness judge agrees with human judgment,
 “faithful” or “reverted”, you MUST be                and that the faithfulness judge reports trustworthy
 able to point to literal Lean code that              verdicts.
 supports the call:     for “faithful”, the
 placeholder/sorry/simplified token(s); for
 “reverted”, the substantive tactic block(s)          Perturbation reliability. We verify that every
 reconstructing the deleted reasoning. If you         edit is exactly the intended one. For number
 cannot find such literal evidence, return
 judgment="other". The evidence_in_fl field
                                                      and symbol edits we compare the original and
 below must be copied verbatim from the Lean          edited natural language character by character: the
 code.                                                recorded span must hold the old value in the origi-
  === Output (strict JSON only) ===                   nal and the new value in the edited string, and the
 {“outcome_present”: true/false,                      text on both sides of the span must match exactly,
   “proof_method”:        one    of   “sorry”,        so the change is localized with no collateral edits.
 “placeholder”,      “simplified”,     “full”,        For example, in aime_1983_p1 the span covers the
 “absent”,
   “evidence_in_fl”:     “copy the relevant           token 40 in the fragment logy w = 40; we confirm
 ∼80-character snippet of Lean supporting the         the original holds 40 at that span and the edited
 verdict, or empty string”,
   “judgment”: “faithful”/“reverted”/“other”,
                                                      string holds 43, while the 112 characters before the
   “reason”: “one-sentence explanation”}              span and every character after it match exactly, so
                                                      40 → 43 is the only difference. Symbol edits are
                                                      checked the same way, for instance a lone + → −
A.4   Composition of the Other/Unclear
                                                      that turns x2 + 18x + 30 into x2 − 18x + 30. For
      Category
                                                      step deletions, whose recorded offsets can be noisy,
This section explains what ends up in the Other/Un-   we instead locate the changed region as the gap
clear category (§3.2): the outputs we cannot label    between the longest common prefix and the longest
Table 5: Identifiable fraction (%): the share of outputs classified as faithful or reverted, over which FR/RR are
computed (the complement of OUR). Lower values mean FR/RR rest on a smaller subset.

                                       Statement edits                           Proof edits              Step deletion
 Model
                            NummF2F   NumM500 SymmF2F    SymM500    NummF2F   NumM500 SymmF2F   SymM500   mF2F M500
 Kimina-Prover-RL-1.7B       30.8      28.8      40.0     29.7         17.0    11.9     14.4     10.6     43.4    42.7
 Kimina-Prover-Distill-8B    72.2      67.3      63.8     59.5         31.1    28.2     24.6     27.5     62.8    58.9
 DeepSeek-Prover-V2-7B       82.4      84.5      82.3     82.1         49.8    48.3     39.0     40.4     73.6    58.3
 Goedel-Prover-V2-8B         64.3      70.0      71.5     63.1         53.5    49.5     39.5     37.2     55.0    45.3
 Gemini-3.1-Pro              75.3      84.7      69.2     74.4         30.3    26.0     18.5     20.9     60.5    64.1
 ProofBridge                 86.3      90.0      88.5     86.2         58.9    48.5     45.6     41.5     64.3    62.0
 ProofFlow                   63.4      72.0      67.7     66.7         80.1    84.7     75.9     70.8     81.4    81.8



common suffix of the two proofs, and require the                 supporting its verdict and confirm that this snippet
edited proof to be strictly shorter and to differ in a           occurs in the scored fragment; this check fails on
single contiguous span; in aime_1983_p3, this iso-               only 0.2% of cases, upper-bounding the judge’s
lates one removed sentence of 151 characters lying               hallucination rate. Third, an author independently
between a 300-character shared prefix and a 359-                 audits 100 number and symbol verdicts and 50 step-
character shared suffix. All 2,637 local edits pass              deletion verdicts against the model output and the
these checks. For the global rewrites, an automated              judge’s evidence field, flagging only two of the 150
check finds that 96.4% of the 2,976 rewrites pre-                as potentially incorrect.
serve the exact set of numeric and symbolic tokens
of the original; the rest are formatting differences             A.6    Full Results
such as digit grouping or numbers spelled out, not               We give the full results behind the main tables.
content changes, so this figure is a lower bound. A              For global perturbations we report TC, StmtSC,
manual reading of 100 rewrites spanning all four                 and ProofSC for every model on the original in-
styles and both datasets confirms that every one                 put and four variants, across both datasets; Ful-
keeps the original meaning.                                      lyCorrect, their conjunction, is in Table 2. For
                                                                 local perturbations we report all six metrics (TC,
Semantic-correctness judge. We check the                         StmtSC, ProofSC, FullyCorrect, FR, and RR) for
StmtSC and ProofSC judge against independent                     every model and condition. The identifiable frac-
human annotation. For each dimension, an author                  tion (the complement of OUR) is reported in Ta-
labels 100 judge verdicts as correct or not, read-               ble 5.
ing each against the natural-language statement or
proof. We deliberately balance each sample, 50                   A.7    Potential Risks and Use of AI Assistants
verdicts the judge accepted and 50 it rejected, so               Potential risks. Our work uses only public math-
we test it on both the cases it passes and the cases             ematics benchmarks and poses no foreseeable risk.
it rejects rather than only the common one. The
judge matches the human label on 94 of the 100                   Use of AI assistants. AI assistants were used to
StmtSC cases and 90 of the 100 ProofSC cases,                    assist with coding and polish writing.
with Cohen’s κ of 0.88 and 0.80, confirming that
its verdicts are reliable on this boundary-stressed
sample.

Faithfulness judge. We check the FR/RR/OUR
judge in three ways. First, the judge reports the
value it reads from the Lean output, which lets us
test each verdict for internal consistency without
a second model: a faithful verdict should carry
the edited value, a reverted verdict the original
value, and an other verdict neither, with equivalent
forms such as 6.5 and 13/2 treated as equal. The
verdict and the reported value agree on 95.4% of
the 13,896 number and symbol cases. Second, we
require the judge to copy the verbatim Lean snippet
                               Table 6: Global perturbation full results (%).

                                                  miniF2F                               MATH-500
Metric   Model
                                    Orig G-FF G-Step Q-FF Q-Step Orig G-FF G-Step Q-FF Q-Step
         Kimina-Prover-RL-1.7B      38.5   32.4   39.3      40.2   45.9   39.8   38.8    38.0   39.2   37.4
         Kimina-Prover-Distill-8B   44.7   39.3   40.6      43.4   46.7   49.2   48.2    44.6   46.8   50.0
         DeepSeek-Prover-V2-7B       5.7   17.2   19.3      28.7   27.5   25.8   25.4    22.0   26.0   20.8
TC       Goedel-Prover-V2-8B         9.8   11.9   12.3      14.8   15.2   16.8   16.4    14.6   17.8   18.4
         Gemini-3.1-Pro             46.3   50.4   49.2      47.1   53.7   58.0   56.8    57.8   55.6   54.4
         ProofBridge                37.3   36.5   37.3      39.3   38.9   33.2   35.0    35.2   31.6   33.6
         ProofFlow                  26.6   19.7   26.6      25.4   26.2   27.4   21.0    23.2   22.6   32.4
         Kimina-Prover-RL-1.7B      38.1   39.3   42.6      43.9   41.4   29.2   32.4    28.8   31.6   28.0
         Kimina-Prover-Distill-8B   74.2   63.1   65.2      66.8   69.7   58.4   56.8    59.2   60.0   58.8
         DeepSeek-Prover-V2-7B      57.4   63.1   66.0      64.3   58.2   50.8   53.0    49.6   50.6   49.6
StmtSC   Goedel-Prover-V2-8B        50.8   46.7   51.2      52.9   51.2   42.2   38.6    39.8   40.8   40.4
         Gemini-3.1-Pro             82.0   79.5   79.9      78.3   81.1   81.4   81.8    82.0   82.8   81.2
         ProofBridge                71.3   69.7   69.7      71.3   71.3   50.8   51.6    48.8   50.4   49.0
         ProofFlow                  42.2   56.6   39.3      42.2   40.6   47.6   58.4    60.6   58.2   45.8
        Kimina-Prover-RL-1.7B       20.9   23.0   20.1      23.0   17.6   16.8   15.8    18.0   19.2   19.2
        Kimina-Prover-Distill-8B    41.4   36.9   38.5      38.5   40.2   43.6   39.4    38.2   40.2   39.0
        DeepSeek-Prover-V2-7B       40.2   41.4   38.5      40.2   43.0   43.2   41.4    43.6   43.6   43.4
ProofSC Goedel-Prover-V2-8B         27.0   27.9   34.0      34.0   33.6   29.4   27.4    29.0   28.4   25.8
        Gemini-3.1-Pro              36.5   38.1   37.7      39.8   36.1   41.6   40.4    41.8   41.2   39.8
        ProofBridge                 38.1   43.9   41.0      37.3   43.0   37.0   41.8    43.2   39.6   45.2
        ProofFlow                   31.1   36.5   33.6      30.7   36.1   34.2   34.8    38.0   39.8   33.8
                   Table 7: Local perturbation full results on miniF2F (%).

Model                    Condition           TC     StmtSC ProofSC FullyCorrect   FR     RR
                         Number, statement   23.8    14.1     7.5         2.2     82.9   17.1
                         Number, proof       42.7    40.7    14.5         4.6      7.3   92.7
Kimina-Prover-RL-1.7B    Symbol, statement   16.2    23.1     4.6         0.8     90.4    9.6
                         Symbol, proof       47.7    43.6    12.8         6.2      3.6   96.4
                         Step deletion       31.8    34.9    14.7         4.7     51.8   48.2
                         Number, statement   39.6    45.8    30.8          7.9    75.0   25.0
                         Number, proof       41.9    65.1    29.0         12.0     5.3   94.7
Kimina-Prover-Distill-8B Symbol, statement   32.3    40.0    16.2          3.1    83.1   16.9
                         Symbol, proof       46.7    69.7    29.7         12.8     8.3   91.7
                         Step deletion       41.9    66.7    31.8         10.9    25.9   74.1
                         Number, statement   16.7    35.7    25.6         0.9     66.3   33.7
                         Number, proof       18.3    63.5    32.0         5.0      8.3   91.7
DeepSeek-Prover-V2-7B    Symbol, statement   17.7    39.2    23.8         1.5     73.8   26.2
                         Symbol, proof       21.0    67.2    26.2         4.6      7.9   92.1
                         Step deletion       9.3     55.0    26.4         0.8     48.4   51.6
                         Number, statement 1.8       26.0    12.8         0.0     58.9   41.1
                         Number, proof     13.3      49.0    21.6         1.2     10.1   89.9
Goedel-Prover-V2-8B      Symbol, statement 11.5      30.8     8.5         0.0     73.1   26.9
                         Symbol, proof     4.6       49.7    23.1         0.5      2.6   97.4
                         Step deletion     8.5       49.6    26.4         1.6     43.7   56.3
                         Number, statement   46.3    28.2    32.6          3.1    22.8   77.2
                         Number, proof       48.5    81.3    29.5         17.0     4.1   95.9
Gemini-3.1-Pro           Symbol, statement   41.5    23.1    30.8          3.1    23.3   76.7
                         Symbol, proof       45.6    76.4    26.2         15.4     8.3   91.7
                         Step deletion       40.3    80.6    31.8         10.1    47.4   52.6
                         Number, statement   29.1    57.7    30.4          6.2    78.6   21.4
                         Number, proof       36.1    71.8    29.5         12.9    39.4   60.6
ProofBridge              Symbol, statement   33.8    55.4    31.5          8.5    80.0   20.0
                         Symbol, proof       37.9    65.6    25.6         10.8    44.9   55.1
                         Step deletion       34.1    66.7    26.4          9.3    33.7   66.3
                         Number, statement   18.9    33.5    24.2         0.9     52.8   47.2
                         Number, proof       17.4    54.8    27.4         5.4     32.6   67.4
ProofFlow                Symbol, statement   11.5    30.0    18.5         0.8     64.8   35.2
                         Symbol, proof       19.5    60.0    26.2         7.2     27.0   73.0
                         Step deletion       19.4    58.9    34.1         5.4     24.8   75.2
                 Table 8: Local perturbation full results on MATH-500 (%).

Model                    Condition           TC     StmtSC ProofSC FullyCorrect   FR     RR
                         Number, statement   24.9     8.8     7.3       0.6       62.4   37.6
                         Number, proof       35.6    25.2    12.3       3.9        5.2   94.8
Kimina-Prover-RL-1.7B    Symbol, statement   27.2     9.7     4.6       0.5       82.8   17.2
                         Symbol, proof       39.3    23.5    11.2       4.6        8.1   91.9
                         Step deletion       34.9    28.6    19.3       8.3       70.7   29.3
                         Number, statement   34.5    23.3    29.0        1.8      49.1   50.9
                         Number, proof       45.0    54.4    33.5       11.0       2.9   97.1
Kimina-Prover-Distill-8B Symbol, statement   30.3    28.2    21.0        3.1      67.2   32.8
                         Symbol, proof       45.0    52.4    34.1       13.5       3.1   96.9
                         Step deletion       40.6    53.6    37.5       14.6      51.3   48.7
                         Number, statement   22.2    21.0    32.7       1.8       48.1   51.9
                         Number, proof       25.8    49.7    35.0       4.3        6.4   93.6
DeepSeek-Prover-V2-7B    Symbol, statement   14.9    30.3    24.6       1.5       69.4   30.6
                         Symbol, proof       35.8    49.6    35.2       7.4        8.5   91.5
                         Step deletion       25.0    43.2    39.1       5.7       53.6   46.4
                         Number, statement 18.8      13.9    17.6       0.2       44.6   55.4
                         Number, proof     3.9       38.4    20.4       0.2        6.6   93.4
Goedel-Prover-V2-8B      Symbol, statement 9.7       22.1    12.8       0.5       59.3   40.7
                         Symbol, proof     16.9      33.0    18.6       2.0        9.2   90.8
                         Step deletion     14.1      33.3    19.3       3.1       60.9   39.1
                         Number, statement   63.7    19.8    39.2        3.5      14.2   85.8
                         Number, proof       57.9    81.6    32.9       19.0       6.3   93.7
Gemini-3.1-Pro           Symbol, statement   47.2    22.1    31.3        2.6      26.9   73.1
                         Symbol, proof       49.3    79.9    33.8       18.9       4.1   95.9
                         Step deletion       56.2    81.2    40.1       22.4      56.9   43.1
                         Number, statement   33.3    29.6    39.6        4.1      57.4   42.6
                         Number, proof       33.9    44.4    38.4       12.1      41.4   58.6
ProofBridge              Symbol, statement   26.7    32.3    32.3        4.1      70.8   29.2
                         Symbol, proof       27.5    44.4    35.0        9.7      41.4   58.6
                         Step deletion       37.5    40.6    37.0        9.9      53.8   46.2
                         Number, statement   16.9    17.3    28.4       0.6       49.3   50.7
                         Number, proof       19.6    53.4    29.4       5.7       24.4   75.6
ProofFlow                Symbol, statement   11.3    28.7    21.5       0.5       57.7   42.3
                         Symbol, proof       19.5    56.4    25.5       6.3       20.2   79.8
                         Step deletion       22.4    58.9    37.0       6.8       33.8   66.2
