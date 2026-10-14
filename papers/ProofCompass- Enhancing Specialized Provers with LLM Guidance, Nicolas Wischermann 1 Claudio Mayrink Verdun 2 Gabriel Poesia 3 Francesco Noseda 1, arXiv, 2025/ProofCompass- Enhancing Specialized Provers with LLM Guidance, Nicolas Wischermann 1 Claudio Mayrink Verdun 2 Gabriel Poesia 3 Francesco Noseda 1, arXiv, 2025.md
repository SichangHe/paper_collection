                                                 P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance


                                                        Nicolas Wischermann 1 Claudio Mayrink Verdun 2 Gabriel Poesia 3 Francesco Noseda 1


                                                                   Abstract                                                         56
                                                                                                                                         DeepSeek-Prover-v1.5-RL        55.3
                                                Language models have become increasingly pow-                                       55   ProofCompass                            54.9
                                                erful tools for formal mathematical reasoning.
                                                However, most existing approaches rely exclu-                                       54
arXiv:2507.14335v1 [cs.AI] 18 Jul 2025




                                                                                                                 Success Rate (%)
                                                sively on either large general-purpose models or
                                                                                                                                    53
                                                smaller specialized models, each with distinct lim-                                            52.5
                                                itations, while training specialized large models                                   52                         51.6
                                                still requires significant computational resources.
                                                This paper introduces P ROOF C OMPASS, a novel                                      51
                                                hybrid methodology that achieves remarkable
                                                                                                                                    50   50
                                                computational efficiency by strategically guid-
                                                ing existing specialized prover methods, such                                       49
                                                as DeepSeek-Prover-v1.5-RL (DSP-v1.5) with a
                                                Large Language Model (LLM) without requiring                                        48
                                                                                                                                         Pass@32                   Pass@128    Pass@3200
                                                additional model training. The LLM provides
                                                natural language proof strategies and analyzes
                                                failed attempts to select intermediate lemmas, en-                 Figure 1. Comparison of P ROOF C OMPASS versus DeepSeek-
                                                abling effective problem decomposition. On the                     Prover-v1.5-RL (Xin et al., 2024) on the miniF2F-test dataset.
                                                miniF2F benchmark, P ROOF C OMPASS demon-                          Each group of bars shows the side-by-side success rates for a
                                                strates substantial resource efficiency: it outper-                specific Pass@k budget. The figure highlights the resource effi-
                                                forms DSP-v1.5 (54.9% → 55.3%) while using                         ciency of P ROOF C OMPASS, showing its Pass@128 performance
                                                                                                                   is comparable to the baseline’s more computationally expensive
                                                25x fewer attempts (3200 → 128). Our syner-
                                                                                                                   Pass@3200 result.
                                                gistic approach paves the way for simultaneously
                                                improving computational efficiency and accuracy
                                                in formal theorem proving.
                                                                                                                   landscape, with formal mathematical reasoning emerging
                                                                                                                   as a crucial new frontier (Yang et al., 2024) and prompting
                                         1. Introduction                                                           broader reflection on the future of mathematical practice
                                                                                                                   (Venkatesh, 2024; Fraser et al., 2024). For instance, models
                                         The formalization of mathematics, where one seeks to trans-               like GPT-4 (Achiam et al., 2023) have shown remarkable
                                         late mathematical proofs into machine-verifiable form, rep-               mathematical reasoning capabilities on complex problems.
                                         resents a crucial step toward more reliable mathematical                  At the same time, specialized models have achieved unprece-
                                         knowledge (Avigad, 2024). While proof assistants like Is-                 dented success in formal mathematics, with the recently
                                         abelle (Paulson, 1994), HOL Light (Harrison, 2009), and                   released (April 30) DeepSeek-Prover-V2 (Ren et al., 2025),
                                         Lean (de Moura & Ullrich, 2021) have made formalization                   for instance, automatically solving 88.9% of the problems
                                         possible, the process has historically been labor intensive,              on miniF2F (Zheng et al., 2021), a central benchmark in
                                         requiring deep expertise in both mathematics and formal                   formal mathematics.
                                         verification tools. Recent advances in large language mod-
                                         els (LLMs) show promise in dramatically changing this                     Recent efforts to leverage language models for automated
                                                                                                                   theorem proving have largely followed two distinct paths,
                                            1
                                            Federal University of Rio de Janeiro 2 Harvard John A. Paulson         each with its own set of strengths and limitations. One path
                                         School of Engineering and Applied Sciences 3 Stanford University.         focuses on using large, general-purpose language models,
                                         Correspondence to: Nicolas Wischermann <ndasilva@ufrj.br>.                often by employing them within structured, multi-stage al-
                                         The second AI for MATH Workshop at the 42nd International                 gorithms (Jiang et al., 2023) that break down the task of
                                         Conference on Machine Learning, Vancouver, Canada. Copyright              formal proof generation. While these large models have
                                         2025 by the author(s).                                                    shown strong informal mathematical reasoning capabilities,

                                                                                                             1
                             P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

they frequently struggle with the precise syntax and tac-              intractable for the prover working alone. A diagram of the
tics required by proof assistants. Alternatively, a significant        method is shown in Figure 2.
body of work has focused on developing specialized models,
                                                                       We evaluate P ROOF C OMPASS on the miniF2F benchmark
often at a smaller scale (e.g., 7B parameters or less), tailored
                                                                       (Zheng et al., 2021). The results, displayed in Figure 1,
specifically for formal mathematics (Welleck & Saha, 2023;
                                                                       highlight the powerful efficiency of our synergistic ap-
Xin et al., 2024; Lin et al., 2025; Xin et al., 2025). These
                                                                       proach. P ROOF C OMPASS achieves a Pass@128 success
models excel at generating syntactically correct proofs and
                                                                       rate of 55.3%, exceeding the standalone specialized prover’s
closing smaller subgoals, but their relatively modest size
                                                                       Pass@3200 accuracy of 54.9% while using 25x fewer at-
inherently limits their mathematical reasoning ability.
                                                                       tempts. The efficiency of our framework is further under-
More recently, approaches like Kimina-Prover (72B) (Wang               scored by its performance on a highly constrained budget:
et al., 2025) and DeepSeek-Prover-V2 (671B) (Ren et al.,               with just 32 attempts, our method’s success rate (52.5%)
2025) have achieved state-of-the-art results by training               surpasses that of the standalone prover using 4x as many
large models specifically for theorem proving. However,                attempts (51.6% at 128 attempts). These results establish
this paradigm shift towards ever-larger specialized models             that strategic guidance is a powerfully efficient route to state-
presents significant challenges. The prohibitive computa-              of-the-art performance. We summarize our contributions as
tional resources required for training are largely inaccessible        follows:
to the broader research community, creating a high barrier
to entry and making it difficult to contribute to the advance-            • We introduce P ROOF C OMPASS, a flexible framework
ment of the frontier in AI-assisted theorem proving and                     that synergistically combines a general-purpose LLM
formal mathematics.                                                         with a specialized prover without requiring additional
In this work, we introduce P ROOF C OMPASS: a synergis-                     model training. The core approach is broadly portable
tic methodology that leverages the broad reasoning capa-                    across different LLMs and specialized provers.
bilities of a large language model to guide a specialized                 • We demonstrate that our method achieves superior per-
prover, without requiring model training. This approach                     formance with considerable resource efficiency on the
proves to be highly efficient, matching the average perfor-                 miniF2F benchmark. Our experiments with DeepSeek-
mance of a standalone specialized prover while using a                      Prover-v1.5-RL show that with a 25-fold smaller bud-
25-fold smaller computational budget. Furthermore, the                      get, our method’s Pass@128 accuracy (55.3%) is com-
framework is designed for modularity: the guiding LLM                       parable to the standalone prover’s performance with
can be readily swapped, and its core principles are adapt-                  Pass@3200 (54.9%), while Pass@32 (52.5%) also out-
able for use with other specialized provers. By substantially               performs the prover’s Pass@128 (51.6%).
reducing the resources needed to achieve superior results,
our work directly addresses the high barrier to entry created
by resource-intensive models. This offers a more accessible            2. Related Work
path forward, helping to democratize cutting-edge research
in automated theorem proving.                                          Recent advances in automated theorem proving have demon-
                                                                       strated diverse approaches to combining language models
Concretely, we use a broadly capable LLM to direct the                 with formal reasoning systems. These approaches can be
specialized DeepSeek-Prover-v1.5-RL (DSP-v1.5) model                   broadly categorized into specialized models designed specif-
(Xin et al., 2024), augmenting its theorem-proving ability             ically for formal mathematics, and large, general-purpose
in Lean 4 (de Moura & Ullrich, 2021) through two primary               language models adapted for theorem proving. Below, we
mechanisms. First, we leverage the LLM’s superior nat-                 review key developments in each category.
ural language understanding and mathematical reasoning
abilities to produce a detailed natural language (NL) proof,           Specialized Models. Holophrasm (Whalen, 2016) was one
which, after summarization, is provided to DSP-v1.5 to                 of the earliest works that explored training specialized lan-
guide it during formal proof generation. Second, inspired              guage models — then GRUs — for formal theorem proving,
by approaches that utilize intermediate goals or lemmas to             using LMs as policies and value functions in tree search.
structure proof search (Wang et al., 2024b; He et al., 2024),          This foundational effort was later advanced by models like
we use the LLM to analyze the smaller model’s failed at-               GPT-f (Polu & Sutskever, 2020), which established the
tempts. From these attempts, the LLM extracts relevant                 viability of using Transformers combined with best-first
and correct lemmas, formatted as have statements in Lean.              search. This approach sparked a series of architectural inno-
This serves to decompose the original problem into more                vations, including Thor (Jiang et al., 2022), which integrated
tractable sub-problems for the specialized prover, creating            LLMs and symbolic provers, HTPS (Lample et al., 2022),
a structured pathway to solve problems that were initially             which introduced a novel tree search algorithm for theo-
                                                                       rem proving, and ReProver (Yang et al., 2023), which used

                                                                   2
                                 P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

                     theorem …
                     Generate
                                              LLM                                              SLM
                     informal                                      Generate initial   theorem …
                                      theorem …                      attempts
                       proof                                                            /- [informal proof] -/
                                        /- [informal proof] -/
                                                                                        [formal proof attempt 1]

                                                                                                  ... Verify and retry
                                                                                                          on error
                                             have l₀ : …            Extract and       theorem …
                                             have l₁ : …           select lemmas        /- [informal proof] -/
                                                 ...                                    [formal proof attempt N]


                                                 Generate                             theorem …
                                              informal proofs                           have l₀ : …
                                                                                          /- [informal proof 0] -/
                                                                                          [formal proof 0]
                                      have l₀ : …                                       have l₁ : …
                                        /- [informal proof 0] -/   Generate proofs        /- [informal proof 1] -/
                                      have l₁ : …                  for lemmas and         [formal proof 1]
                                        /- [informal proof 1] -/        theorem                     .
                                                   .                                                .
                                                   .                                                .
                                                   .                                    /- final informal proof -/
                                      /- final informal proof -/                        [final formal proof]




Figure 2. Flowchart of P ROOF C OMPASS. A general-purpose Large Language Model (LLM) first provides natural language guidance for
a specialized model (SLM, specifically DSP-v1.5-RL) to iteratively generate and verify proof attempts. If all of these attempts prove
unsuccessful, the LLM analyzes the failed attempts to select guiding lemmas, generating further informal proofs to direct the SLM in
proving these lemmas and the final theorem.


retrieval-augmented generation. More recently, Lean-STaR                          ProofAug (Liu et al., 2025) and APOLLO (Ospanov et al.,
(Lin et al., 2024) explored training models that interleave                       2025) employ programmatic harnesses with compiler feed-
informal reasoning in natural language and formal proof                           back and built-in solvers to correct failed attempts. In con-
steps. POETRY (Wang et al., 2024a) focused on recursive                           trast, we leverage a second LLM for analyzing failures. Un-
decomposition of proof goals in Isabelle, extracting training                     like works that use an LLM to directly attempt to fix proofs,
data for this decomposition task by restructuring existing                        like Baldur (First et al., 2023), we use an LLM to extract
human-written proofs. Other models like Goedel-Prover                             correct lemmas using the outcomes of failed attempts.
(Lin et al., 2025) and Mathesis-Prover (Xuejun et al., 2025)
                                                                                  Hybrid Approaches. Recognizing the complementary
were trained directly for whole-proof generation, where
                                                                                  strengths of specialized and general-purpose models, a
each pass attempts to generate a complete proof, while
                                                                                  promising research direction involves their synergistic com-
InternLM2.5-StepProver (Wu et al., 2024), HunyuanProver
                                                                                  bination. For instance, BC-Prover (He et al., 2024) employs
(Li et al., 2024), BFS-Prover (Xin et al., 2025), (Lai et al.,
                                                                                  an LLM for backward chaining and sub-goal generation, and
2025), and MPS-Prover (Liang et al., 2025) combined spe-
                                                                                  delegating tactic-level proof steps to specialized provers. In
cialized models with tree search methods. DeepSeek-Prover-
                                                                                  contrast, our method leverages an LLM to analyze the failed
v1.5 (Xin et al., 2024) pushed forward both whole-proof
                                                                                  proof attempts of a specialized prover to select useful in-
generation and tree search.
                                                                                  termediate lemmas, rather than having the LLM directly
General Language Models. Another line of work has                                 generate sub-goals.
focused on leveraging general-purpose language models
                                                                                 Specialized large models. Apart from hybrid systems, an-
in theorem proving, hoping to benefit from their substan-
                                                                                 other powerful yet resource-intensive approach involves
tially better performance in a wide range of reasoning tasks.
                                                                                 directly specializing large models such as Kimina-Prover
For instance, COPRA (Thakur et al., 2024) introduced a
                                                                                 (72B) (Wang et al., 2025) and DeepSeek-Prover-V2 (671B)
model-agnostic language agent framework, initially show-
                                                                                 (Ren et al., 2025) through further training, a strategy that
ing promising results with GPT-4 Turbo (OpenAI, 2023).
                                                                                 yields state-of-the-art results but at an often prohibitive cost
Draft, Sketch and Prove (Jiang et al., 2023) used Minerva
                                                                                 at most compute budgets. Our work, in contrast, focuses
(Lewkowycz et al., 2022) to first write a natural language
                                                                                 on synergistically combining existing models without incur-
proof and then sketch it as an Isabelle proof with subgoals
                                                                                 ring these significant training overheads, aiming for a more
to be proved by hammers. Other recent work leveraging
                                                                                 resource-efficient path to improved performance.
general-purpose LLMs includes Lyra (Zheng et al., 2024),
Subgoal-based prover (Zhao et al., 2023), and LEGO-Prover
(Wang et al., 2024b).
Alternatively, automated proof repair frameworks such as


                                                                            3
                             P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

3. Method                                                                   diate goals. An LLM can analyze failed proofs from
                                                                            DSP-v1.5 and strategically select lemmas that effec-
In this section, we describe our proposed method for auto-                  tively partition the problem. Each such lemma then
mated theorem proving through the synergistic guidance of                   represents a simpler, more constrained subproblem
a specialized prover by a general-purpose LLM.                              for DSP-v1.5. This strategy of using lemmas or sub-
                                                                            goals to augment theorem proving has proven effec-
3.1. Preliminaries                                                          tive in prior systems like BC-Prover (He et al., 2024)
Our methodology builds upon the DeepSeek-Prover-v1.5-                       and LEGO-Prover (Wang et al., 2024b), which utilize
RL (DSP-v1.5) model (Xin et al., 2024), which exhibits a                    them to structure and simplify the proof search process.
distinct proof generation structure. DSP-v1.5 operates in                   Moreover, works such as Lyra (Zheng et al., 2024)
two primary modes: a Chain-of-Thought (CoT) (Wei et al.,                    and ProofAug (Liu et al., 2025) achieve significant
2022) mode and a non-CoT mode. These can be activated                       performance gains by repairing failed proofs using au-
using specific prompts, as detailed in (Xin et al., 2024).                  tomated tools like Sledgehammer (Paulson, 2012) and
                                                                            predefined sets of tactics, thereby demonstrating the
The CoT mode initiates the formal proof by generating an                    potential to extract valuable components from initially
informal, natural-language proof sketch (Figure 3). This                    unsuccessful derivations.
sketch is embedded within Lean’s block comment syntax
(‘/- ... -/’) and is placed immediately after the theorem state-
ment. Following this informal sketch, DSP-v1.5 proceeds to
generate the formal Lean 4 code, often interleaving it with            Our framework’s architecture is designed for broad applica-
short explanatory comments prefixed with ‘–’. In contrast,             bility. The guiding LLM is fully interchangeable, allowing
the non-CoT mode of DSP-v1.5 generates only Lean 4 code,               the system to immediately benefit from future model im-
without any accompanying informal proofs or comments.                  provements, while the core lemma-selection mechanism
In this work, we focus on the CoT mode of DSP-v1.5. A                  is adaptable to any specialized prover that generates struc-
common characteristic of DSP-v1.5’s proof generations is               tured proof attempts. The only component tailored to spe-
the production of intermediate steps articulated as ‘have’             cific prover features is the injection of informal proof texts,
statements within the Lean proof. These ‘have’ statements              which leverages the CoT-style output of DSP-v1.5 in our
effectively function as lemmas or sub-goals, and are a com-            experiments. Consequently, P ROOF C OMPASS is directly
mon mechanism for structuring proofs in Lean.                          compatible with models that share the exact generation struc-
                                                                       ture of DSP-v1.5, such as Goedel-Prover (Lin et al., 2025).
These distinct operational characteristics of DSP-v1.5 in-             For other provers, the informal proof injection must be mod-
form our approach by suggesting two main avenues for                   ified to suit different CoT structures (Wang et al., 2025) or
external guidance, which our method aims to exploit:                   can be omitted entirely for those lacking CoT support (Xin
                                                                       et al., 2025), with the core lemma-based guidance remaining
   • Informal Proof Guidance: The initial informal proof               fully effective in either case.
     section generated by DSP-v1.5 in CoT mode provides
                                                                       We now detail how these guidance mechanisms are imple-
     a natural interface for supplying a high-level, natural
                                                                       mented. Section 3.2 presents our informal proof guidance
     language (NL) proof strategy. We leverage this by em-
                                                                       approach, where the LLM enhances the theorem-proving
     ploying a larger, more capable LLM whose superior
                                                                       capabilities of the specialized prover (SLM, DSP-v1.5 in our
     reasoning abilities can generate more effective informal
                                                                       experiments), while Section 3.3 describes the lemma-based
     proofs than DSP-v1.5 might produce autonomously.
                                                                       guidance mechanism
     This approach is motivated by findings in works such as
     (Xin et al., 2024) and (Lin et al., 2024), which demon-
     strated performance improvements by training models               3.2. Informal Proof Generation and Initial Attempts
     on Lean proofs annotated with natural language rea-               The first stage of P ROOF C OMPASS focuses on providing
     soning steps, thereby showing that NL reasoning can               the SLM with a high-quality, natural language (NL) proof
     enhance specialized models’ performance in formaliza-             to guide its CoT mode.
     tion tasks. Works like (Jiang et al., 2023; Wang et al.,
     2024b; Zheng et al., 2024) also use LLM-generated                 To achieve this, we initially prompt an LLM with the formal
     proofs, which they use to guide the general model in              theorem statement Tf ormal and its informal counterpart
     its proof generation.                                             Tinf ormal 1 to generate a complete natural language proof,
                                                                           1
                                                                             In miniF2F (Zheng et al., 2021), formal statements are already
   • Lemma-based Guidance: The ‘have’ statements of-                   paired with natural language counterparts. When only a formal
     fer a mechanism for decomposing the main theorem                  statement is available, the LLM itself could be used to informalize
     and guiding the proof search via structured interme-              the statement if needed.

                                                                   4
                           P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

                theorem algebra_9onxpypzleqsum2onxpy
                  (x y z : ℝ)
                  (h₀ : 0 < x ∧ 0 < y ∧ 0 < z) :
                  9 / (x + y + z) ≤ 2 / (x + y) + 2 / (y + z) + 2 / (z + x) := by
                  /-
                  To show that for any three positive real numbers \( x \), \( y \), and \( z \), the
                  inequality \( \frac{9}{x + y + z} \leq \frac{2}{x + y} + \frac{2}{y + z} + \frac{2}{z + x}
                  \) holds, we can use the method of simplifying the expression and applying basic algebraic
                  inequalities. Specifically, we will use the fact that the sum of reciprocals of positive
                  numbers is greater than or equal to the reciprocal of the sum of those numbers.
                  -/
                  -- Establish that all sums of pairs of variables are positive.
                  have h₁ : 0 < x + y + z := by linarith
                  have h₂ : 0 < x + y := by linarith
                  have h₃ : 0 < y + z := by linarith
                  have h₄ : 0 < z + x := by linarith
                  -- Clear the denominators by multiplying both sides by the product of all denominators.
                  field_simp [add_pos]
                  -- Use the division inequality to compare the numerators.
                  rw [div_le_div_iff₀ (by positivity) (by positivity)]
                  -- Simplify the expression by expanding and combining like terms.
                  ring_nf
                  -- Use linear arithmetic to prove the inequality.
                  nlinarith [sq_nonneg (x - y), sq_nonneg (y - z), sq_nonneg (z - x)]



                                  Figure 3. Sample proof by DSP-v1.5 of a theorem in Lean 4.


                                                                                                                 1               N
denoted as pN L :                                                   all unique ‘have’ statements extracted from Pinit , . . . , Pinit
                                                                    generated by the SLM. This yields a candidate pool of po-
                                    LLM
             (Tf ormal , Tinf ormal ) −−−→ pN L          (1)        tential lemmas, Lextract :
                                                                               1               N lemma extraction
The full NL proof pN L often exceeds the input context ca-                    Pinit , . . . , Pinit −−−−−−−−−→ Lextract          (4)
pacity of the SLM. Thus, we employ a second LLM query to
summarize it, yielding a concise proof summary psummary :           The candidate pool Lextract is first subjected to an auto-
                                                                    mated syntax check to filter out any malformed statements.
                                    LLM
       (Tf ormal , Tinf ormal , pN L ) −−−→ psummary     (2)        This initial validation step ensures that only syntactically
                                                                    correct lemmas are passed to the LLM for evaluation, result-
psummary is then embedded within the Lean block com-                ing in the set of valid lemmas, Lvalid :
ment syntax (‘/- ... -/’) expected by DSP-v1.5’s CoT mode,
                                                                                               syntax checking
appended to the formal theorem statement.                                           Lextract −−−−−−−−→ Lvalid                    (5)
With this LLM-generated proof summary (psummary ) in-
tegrated into the input, we query DSP-v1.5 (using its CoT           This set of valid lemmas is then processed by the guid-
activation prompt) to sequentially generate and verify indi-        ing LLM. Given the pool Lvalid , the formal theorem state-
vidual proof attempts. This process continues until either a        ment Tf ormal , its informal counterpart Tinf ormal , the com-
correct proof is found or the maximum of N initial attempts         plete LLM-generated natural language proof pN L for the
is reached. Each attempt i ∈ {1, . . . , N } corresponds to a       theorem, and the maximum number of lemmas to select
single generation call:                                             k, the LLM is tasked with selecting at most k lemmas,
                                                                    Lselect = (l0 , l1 , . . . , lm−1 ), m ≤ k:
                                 SLM    i
                (Tf ormal , pN L ) −−→ Pinit             (3)                                                        LLM
                                                                      (Lvalid , Tf ormal , Tinf ormal , pN L , k) −−−→ Lselect   (6)
Each attempt consumes one unit of the total budget B. If a
correct proof is found, the process concludes successfully,         To produce Lselect , the LLM analyzes each candidate
and the subsequent lemma extraction and proving stages are          lemma in Lvalid . This involves evaluating the lemma’s cor-
skipped. If the N -attempt limit is reached without success,        rectness, primarily considering whether the statement is (i)
the method proceeds as detailed in the following sections.          logically sound and provable using only the global hypothe-
                                                                    ses of Tf ormal , and (ii) directly justified by pN L . From the
                                                                    subset of lemmas deemed correct, the LLM then performs a
3.3. LLM-Guided Lemma Selection
                                                                    strategic selection. This selection aims to identify lemmas
Should the initial N proof attempts fail to prove the theo-         covering key inferential steps of pN L , choosing at most k
rem, P ROOF C OMPASS proceeds to extract and select a set           lemmas to constitute the final output set Lselect , which are
of guiding lemmas. This process begins by aggregating               ordered according to the logical flow of pN L . The rationale

                                                                5
                              P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

for this approach of extracting and selecting lemmas from                 lemmas in Lselect hold. The SLM is prompted to generate
SLM attempts, as opposed to direct LLM generation, is                     Pmain using Tf ormal (with all lemmas in Lselect appended
detailed in Appendix C.                                                   as hypotheses) and the LLM-generated informal proof for
                                                                          the main theorem pmain :
In the second stage, the lemmas in Lselect are passed to the
LLM for informal proof generation. The LLM generates a                                                               SLM
concise informal proof pl for each selected formal lemma                            (Tf ormal , Lselect , pmain ) −−→ Pmain          (10)
l ∈ Lselect , derived from pN L , Tf ormal and Tinf ormal . It
                                                                          This Pmain provides the concluding logic to derive Tf ormal
also generates a concise informal proof for the main theo-
                                                                          from the established lemmas.
rem, pmain , which assumes the truth of all selected lemmas
in Lselect :                                                              If Pmain is successfully generated, an iterative procedure
                                                                          begins. Within each iteration of this loop, the method first
                                        LLM
     (l, Tf ormal , Tinf ormal , pN L ) −−−→ pl                 (7)       attempts to prove individual lemmas. It iterates through
                                                LLM                       each lemma li ∈ Lselect (for i from 0 to m − 1). If li is
     (Tf ormal , Tinf ormal , Lselect , pN L ) −−−→ pmain       (8)
                                                                          not already in Lproven , li is formulated as a distinct Lean
The LLM adapts explanations from pN L to generate a proof                 4 theorem. This theorem includes all global hypotheses of
for each lemma l. The collection of all these generated                   Tf ormal and all previously ordered lemmas from Lselect
informal proofs is denoted by P = {pl | l ∈ Lselect } ∪                   that precede li as hypotheses, with the goal being the formal
{pmain }.                                                                 statement of li . The SLM then attempts to generate a formal
                                                                          proof Pli for this lemma, guided by li ’s informal proof pli :
Next, Lproven is initialized by extracting lemma proofs
from previous attempts. For each l ∈ Lselect , we search                                                             SLM
                                                                                        (l0 , ..., li , Tf ormal , pli ) −−→ Pli     (11)
  1              N
Pinit , . . . , Pinit for all its occurrences as a ‘have’ state-
ment. For each such occurrence with an associated proof                   If Pli is successfully generated and verified by Lean 4, li is
Pl,extract , we verify if Pl,extract proves l using only the              added to Lproven .
global hypotheses of Tf ormal . If this check passes and l
is not already in Lproven , we add l and that Pl,extract to               Following this lemma-proving pass within an iteration, a
Lproven :                                                                 candidate full proof, Pf inal , is constructed for Tf ormal .
                                                                          This Pf inal starts with Tf ormal and its global hypotheses,
        1
      (Pinit            N
             , . . . , Pinit , Tf ormal , Lselect ) → Lproven   (9)       incorporates ‘have’ statements for each lemma lk ∈ Lproven
                                                                          along with their formal proofs Plk , and finally appends the
                                                                          proof steps from the previously generated Pmain . This com-
The outcome of this stage is thus the curated set of for-
                                                                          plete Pf inal is then submitted to Lean 4 for validation. If
mal lemmas Lselect , the set of their corresponding LLM-
                                                                          Pf inal is a valid proof of Tf ormal , the theorem is considered
generated informal proofs P, and the initialized set of
                                                                          proven, and the process concludes successfully.
proven lemmas Lproven . These are then used to guide sub-
sequent formal proof attempts by DSP-v1.5, as detailed in
the next section.                                                         4. Experiment
                                                                          In this section we describe the experimental evaluation of
3.4. Lemma Proving and Theorem Validation                                 our proposed method.
This stage proceeds to prove the theorem Tf ormal using the
set of selected lemmas Lselect and their corresponding infor-             4.1. Experimental Setup
mal proofs P. In case no lemmas were selected, the method
                                                                          Dataset. We evaluate our approach on the widely used
reverts to the initial proof generation strategy described in
                                                                          miniF2F dataset (Zheng et al., 2021). It contains 488 for-
Section 3.2 for the remainder of the total budget B.
                                                                          mal mathematics problems, consisting of olympiad-level
Throughout this stage, each call to the SLM to generate                   problems (AMC, AIME, IMO) and undergraduate mathe-
Pmain or any individual lemma proof Pli consumes an at-                   matics exercises formalized in various proof assistant sys-
tempt from the overall budget B allocated for the problem.                tems, including Isabelle (Paulson, 1994), HOL Light (Harri-
If the attempts allocated for this lemma-based strategy are               son, 2009), Metamath (Megill & Wheeler, 2019), and Lean
exhausted before a complete and verified proof Pf inal is                 (de Moura & Ullrich, 2021). The Lean problems were orig-
obtained, this approach is considered unsuccessful for the                inally in Lean 3, but were converted to Lean 4 in (Yang,
current theorem.                                                          2023).
Initially, the method seeks to obtain Pmain , a formal proof              Evaluation. We assess the performance of P ROOF C OM -
of the main theorem Tf ormal under the assumption that all                PASS using the Pass@k metric, specifically reporting


                                                                      6
                            P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

                                                                    dalone specialized provers, as our primary goal is to assess
          Table 1. Pass@k performance on miniF2F-test
                                                                    the LLM-guidance technique itself, rather than to conduct a
  M ETHOD                       B UDGET     MINI F2F- TEST          wide-ranging benchmark of all prover types.
  BASELINES                                                         Implementation Details. Our methodology utilizes specific
  BC-P ROVER                      100           30.7%               Large Language Models for its guidance components. The
  BC-P ROVER + R E P ROVER        100           31.6%               initial, comprehensive natural language proof (pN L ) for a
  BC-P ROVER + LLMS TEP            100          32.0%               given theorem is generated using Gemini 2.0 Flash Thinking
  LEGO-P ROVER                     100          50.0%               Experimental (Kane, 2025). All other LLM-driven tasks
  LYRA                             200          51.2%
  DSP- V 1.5                        32       50% ± 0.5%
                                                                    within our method, such as summarizing pN L , performing
                                   128      51.6% ± 0.5%            lemma analysis and selection, and elaborating the proofs
                                  3200      54.9% ± 0.7%            for each lemma, are performed using Gemini 2.0 Flash
  O URS                                                             (Pichai et al., 2024). For all interactions with the DeepSeek-
                                                                    Prover-v1.5-RL model, we employ its Chain-of-Thought
  P ROOF C OMPASS                   32         52.5%
                                   128         55.3%
                                                                    (CoT) mode, using the specific prompt provided in (Xin
                                                                    et al., 2024). All attempts were generated using an Nvidia
  A BLATIONS                                                        GeForce RTX 4090, and verification was conducted using
  O NLY L EMMA G UIDANCE            32          51.6%               Lean version 4.15.
                                   128          53.3%
  O NLY I NFORMAL P ROOF            32          52.0%               Hyperparameters. As we compare our method with the
                                   128          52.9%               Pass@32 and Pass@128 performances of DSP-v1.5, the
                                                                    total generation budget is B = 128. The initial number of
                                                                    attempts was chosen to be N = 16, as this often resolves
                                                                    a significant portion of problems upfront by DSP-v1.5 and
Pass@32 and Pass@128 due to computational budget con-               provides a sufficient corpus of ‘have’ statements from failed
straints. For our methodology, an “attempt” in the Pass@k           attempts for effective LLM guidance, while selecting at most
calculation corresponds to any call made to the DSP-v1.5            k = 5 lemmas focuses on key strategic steps. Appendix B
model. This includes initial proof generation attempts, as          elaborates on these choices and includes supporting analy-
well as individual attempts to prove each selected lemma            sis.
and the theorem itself using the lemmas (see Appendix A
for a detailed breakdown of LLM task and SLM attempt                4.2. Main Results
timings, including overhead considerations). The validity
of generated formal proofs and selected lemmas is verified          The performance of our proposed method on the miniF2F-
by interacting with Lean 4 via the Lean REPL (leanprover-           test dataset is presented in Table 1, with a visual comparison
community, 2023). A proof attempt is deemed success-                to the DeepSeek-Prover-v1.5-RL baseline for Pass@32 and
ful if the Lean REPL returns no error messages and the              Pass@128 rates depicted in Figure 1. Our approach demon-
generated proof does not contain any sorry placeholders.            strates notable improvements in theorem-proving capabili-
Conversely, an attempt is considered a failure if it produces       ties and resource efficiency, particularly when enhancing its
errors, includes sorry placeholders, or if the Lean verifi-         foundational specialized prover, DSP-v1.5.
cation process exceeds a 20-second timeout.                         When compared directly to this baseline, our method yields
Baselines. Our primary point of comparison is the per-              substantial gains. As shown in Table 1, our Pass@32 rate
formance of the DSP-v1.5 model as reported in its original          of 52.5% exceeds the baseline’s Pass@128 rate of 51.6%.
publication (Xin et al., 2024). To contextualize our method’s       More strikingly, with a 25-fold smaller computational bud-
performance, we also compare against BC-Prover (He et al.,          get, our method’s Pass@128 rate of 55.3% matches the
2024), a relevant LLM-driven framework for theorem prov-            average 54.9% performance that DSP-v1.5 achieves with
ing in Lean (considered both as a standalone LLM-based              3200 attempts.
prover and in its hybrid configurations with ReProver (Yang         Further contextualizing these results, our method also shows
et al., 2023) and LLMStep (Welleck & Saha, 2023)), and              strong performance relative to other contemporary systems.
other prominent LLM-based provers such as LEGO-Prover               A key contribution of this work is its novel hybrid archi-
(Wang et al., 2024b) and Lyra (Zheng et al., 2024), all of          tecture. To the best of our knowledge, BC-Prover (He
which utilize the Isabelle proof assistant. This selection of       et al., 2024) is the most comparable contemporary hybrid
baselines reflects our study’s central aim: to introduce and        approach; our method (55.3% Pass@128) significantly out-
evaluate a novel LLM-guidance methodology for a given               performs BC-Prover + LLMStep (32.0% Pass@100), un-
specialized prover, using DSP-v1.5 as our specific test case.       derscoring the efficacy of our specific synergistic design.
We therefore do not include comparisons with other stan-

                                                                7
                            P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

Moreover, even with a limited budget of 32 attempts, our              our method. Their contributions are complementary: their
method’s Pass@32 rate of 52.5% is competitive with or ex-             combination yields the best performance. P ROOF C OMPASS
ceeds other LLM-based methods using 3−6× larger attempt               thus demonstrates the benefits of a synergistic interaction
budgets, such as LEGO-Prover (50.0% at 100 attempts) and              between the LLM and the specialized prover.
Lyra (51.2% at 200 attempts).
These combined results underscore the significant advantage           5. Conclusion
of our synergistic approach, achieving strong performance
                                                                      In this paper, we introduced P ROOF C OMPASS, a novel
and resource efficiency by effectively leveraging the comple-
                                                                      methodology to enhance automated theorem proving by syn-
mentary strengths of general-purpose LLMs and specialized
                                                                      ergistically leveraging the high-level reasoning of general-
provers.
                                                                      purpose Large Language Models (LLMs) to guide special-
                                                                      ized provers. Our approach employs an LLM to generate
4.3. Ablation Study                                                   strategic natural language proofs and to analyze failed proof
To better understand the contributions of the primary compo-          attempts by a specialized model to extract and select use-
nents of our methodology (LLM-generated informal proof                ful intermediate lemmas, thereby decomposing complex
guidance and LLM-guided lemma selection) we conducted                 problems.
two ablation studies. The results are included in Table 1.            The empirical validation on the miniF2F (Zheng et al., 2021)
The first ablation, “Only Lemma Guidance,” isolates the               benchmark highlights the framework’s remarkable resource
impact of the lemma-based guidance mechanism. In this                 efficiency. P ROOF C OMPASS is on par with the 3200-attempt
configuration, the initial LLM-generated informal proof               average performance of the standalone prover while using
psummary , subsequent informal proofs for lemmas pli and              only 128 attempts—a 25-fold computational saving. This
the main theorem pmain are omitted. Instead, DSP-v1.5                 efficiency extends to smaller scales, where our Pass@32
generates its own informal proofs (as in its standard CoT             performance surpasses the baseline’s Pass@128 accuracy.
mode, illustrated in Figure 3), while still benefiting from           This work thus establishes that intelligently orchestrating the
the LLM’s analysis of failed attempts to extract and select           complementary strengths of LLMs and specialized provers
guiding ‘have’ statements (lemmas). This ablation proved              offers a more promising and resource-efficient path towards
highly effective on its own; in particular, its Pass@32 perfor-       more capable theorem proving systems.
mance of 51.6% already matches the baseline’s Pass@128
result, and its total Pass@128 rate reached 53.3%. This               6. Limitations and Future Work
suggests that strategically decomposing the problem using
LLM-selected lemmas already aids the specialized prover,              The proposed methodology, while demonstrating promising
even without direct informal proof guidance from the LLM              results, presents several limitations that also outline avenues
for each step. However, a high-quality informal proof still           for future research.
provides an extra performance boost.                                  While our core lemma selection loop is designed for broad
The second ablation, “Only Informal Proof,” evaluates the             applicability to any prover generating structured proof at-
effectiveness of providing LLM-generated informal proofs              tempts, the informal proof guidance component in its current
alone without the subsequent lemma processing. Here, the              form is tailored to the specific CoT-style input of provers
LLM generates the initial informal proof psummary , which             like DSP-v1.5. A key avenue for future work is therefore
guides DSP-v1.5 for all N = 128 initial attempts (as de-              to both validate the core lemma-based framework across a
scribed in Section 3.2), but the lemma extraction, selec-             more diverse range of specialized provers and to develop
tion, and proving stages (Sections 3.3 and 3.4) are entirely          more generalized techniques for the informal guidance com-
skipped. This configuration yielded a Pass@32 of 52.0%                ponent.
and a Pass@128 of 52.9%, which also outperforms the base-             Furthermore, the experimental evaluation presented herein
line. Notably, its Pass@32 rate surpasses the baseline’s              was conducted with a maximum of 27 attempts per problem.
Pass@128 rate (51.6%), demonstrating that leveraging the              This represents a considerably more constrained compu-
LLM’s advanced reasoning for high-level proof strategies              tational budget compared to several contemporary works
enables the specialized prover to find correct formalizations         in automated theorem proving, which often report Pass@k
with significantly fewer attempts by effectively narrowing            metrics frequently exceeding 217 attempts (Li et al., 2024;
the search space.                                                     Wu et al., 2024; Xin et al., 2024). Consequently, an im-
Together, these results highlight that both the LLM-                  portant avenue for future research involves assessing the
generated informal proof guidance and the LLM-driven                  performance scaling of our methodology under significantly
lemma processing contribute to the overall performance of             increased computational resources.


                                                                  8
                           P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

Acknowledgements                                                      Conference on Empirical Methods in Natural Language
                                                                      Processing, pp. 3059–3077, 2024.
This study was financed in part by the Coordenação de
Aperfeiçoamento de Pessoal de Nı́vel Superior - Brasil             Jiang, A. Q., Li, W., Tworkowski, S., Czechowski, K.,
(CAPES) – Finance Code 001. The authors also wish to                   Odrzygóźdź, T., Miłoś, P., Wu, Y., and Jamnik, M. Thor:
thank Professor Adriano Côrtes for his valuable assistance            Wielding hammers to integrate language models and auto-
with the computational experiments in this work.                       mated theorem provers. Advances in Neural Information
                                                                       Processing Systems, 35:8360–8373, 2022.
Impact Statement
                                                                    Jiang, A. Q., Welleck, S., Zhou, J. P., Lacroix, T., Liu, J., Li,
This work presents a resource-efficient methodology for au-            W., Jamnik, M., Lample, G., and Wu, Y. Draft, sketch,
tomated theorem proving. By demonstrating a path forward               and prove: Guiding formal theorem provers with informal
that does not require large-scale computational infrastruc-            proofs. In The Eleventh International Conference on
ture, our approach helps to democratize research in this               Learning Representations, 2023.
domain. We believe this focus on computational efficiency
is a positive contribution that can foster broader and more         Kane, P.     Access the latest 2.0 experimen-
inclusive participation within the machine learning commu-            tal models in the gemini app.,     February
nity.                                                                 2025.   URL https://blog.google/feed/
                                                                      gemini-app-experimental-models.
References                                                          Lai, J., Zhang, J., Xu, S., Chen, T., Wang, Z., Yang, Y.,
Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I.,            Zhang, J., Cao, C., and Xu, J. Llm-based automated theo-
  Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S.,           rem proving hinges on scalable synthetic data generation.
  Anadkat, S., et al. Gpt-4 technical report. arXiv preprint          arXiv preprint arXiv:2505.12031, 2025.
  arXiv:2303.08774, 2023.
                                                                    Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
Avigad, J. Mathematics and the formal turn. Bulletin of the           Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hyper-
  American Mathematical Society, 61(2):225–240, 2024.                 tree proof search for neural theorem proving. Advances in
                                                                      neural information processing systems, 35:26337–26349,
de Moura, L. and Ullrich, S. The lean 4 theorem prover and            2022.
  programming language. In Platzer, A. and Sutcliffe, G.
  (eds.), Automated Deduction – CADE 28, pp. 625–635,               leanprover-community. A simple repl for lean 4. https:
  Cham, 2021. Springer International Publishing.                      //github.com/leanprover-community/
                                                                       repl, 2023. Accessed: May 20, 2025.
First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
  Whole-proof generation and repair with large language             Lewkowycz, A., Andreassen, A., Dohan, D., Dyer, E.,
  models. In Proceedings of the 31st ACM Joint European               Michalewski, H., Ramasesh, V., Slone, A., Anil, C.,
  Software Engineering Conference and Symposium on the                Schlag, I., Gutman-Solo, T., et al. Solving quantitative
  Foundations of Software Engineering, pp. 1229–1241,                 reasoning problems with language models. Advances in
  2023.                                                               Neural Information Processing Systems, 35:3843–3857,
                                                                      2022.
Fraser, M., Granville, A., Harris, M. H., McLarty, C., Riehl,
  E., and Venkatesh, A. Will machines change mathemat-              Li, Y., Du, D., Song, L., Li, C., Wang, W., Yang, T., and Mi,
  ics? Bulletin (New Series) of the American Mathematical              H. Hunyuanprover: A scalable data synthesis framework
  Society, 61(2), 2024.                                                and guided tree search for automated theorem proving.
                                                                       arXiv preprint arXiv:2412.20735, 2024.
Harrison, J. HOL Light: An overview. In Berghofer, S.,
  Nipkow, T., Urban, C., and Wenzel, M. (eds.), Proceed-            Liang, Z., Song, L., Li, Y., Yang, T., Zhang, F., Mi, H.,
  ings of the 22nd International Conference on Theorem                and Yu, D. Mps-prover: Advancing stepwise theorem
  Proving in Higher Order Logics, TPHOLs 2009, volume                 proving by multi-perspective search and data curation.
  5674 of Lecture Notes in Computer Science, pp. 60–66,               arXiv preprint arXiv:2505.10962, 2025.
  Munich, Germany, 2009. Springer-Verlag.
                                                                    Lin, H., Sun, Z., Welleck, S., and Yang, Y. Lean-star: Learn-
He, Y., Zhang, J., Bao, J., Lin, F., Yang, C., Qin, B., Xu,           ing to interleave thinking and proving. In The 4th Work-
  R., and Yin, W. Bc-prover: Backward chaining prover                 shop on Mathematical Reasoning and AI at NeurIPS’24,
  for formal theorem proving. In Proceedings of the 2024              2024.

                                                                9
                            P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J.,        Wang, H., Xin, H., Liu, Z., Li, W., Huang, Y., Lu, J.,
  Xia, M., Chen, D., Arora, S., et al. Goedel-prover: A fron-          Zhicheng, Y., Tang, J., Yin, J., Li, Z., et al. Proving theo-
  tier model for open-source automated theorem proving.                rems recursively. In The Thirty-eighth Annual Conference
  arXiv preprint arXiv:2502.07640, 2025.                               on Neural Information Processing Systems, 2024a.
Liu, H., Sun, J., Li, Z., and Yao, A. C. Efficient neural             Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang, Y.,
  theorem proving via fine-grained proof structure analysis.           Xiong, J., Shi, H., Xie, E., Yin, J., et al. Lego-prover:
  arXiv preprint arXiv:2501.18310, 2025.                               Neural theorem proving with growing libraries. In The
                                                                       Twelfth International Conference on Learning Represen-
Megill, N. D. and Wheeler, D. A.         Metamath: A
                                                                       tations, 2024b.
 Computer Language for Mathematical Proofs. Lulu
 Press, Morrisville, North Carolina, 2019. http://us.                 Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
 metamath.org/downloads/metamath.pdf.                                  M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
OpenAI.   GPT-4 Turbo, 2023. URL https:                                Kimina-prover preview: Towards large formal reason-
 //platform.openai.com/docs/models/                                    ing models with reinforcement learning. arXiv preprint
  gpt-4-turbo.                                                         arXiv:2504.11354, 2025.

Ospanov, A., Farnia, F., and Yousefzadeh, R. Apollo: Au-              Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi,
  tomated llm and lean collaboration for advanced formal               E., Le, Q. V., Zhou, D., et al. Chain-of-thought prompting
  reasoning. arXiv preprint arXiv:2505.05758, 2025.                    elicits reasoning in large language models. Advances in
                                                                       neural information processing systems, 35:24824–24837,
Paulson, L. Three years of experience with sledgehammer, a             2022.
  practical link between automatic and interactive theorem
  provers. In Schmidt, R. A., Schulz, S., and Konev, B.               Welleck, S. and Saha, R. llmstep: Llm proofstep suggestions
  (eds.), PAAR-2010: Proceedings of the 2nd Workshop on                in lean. In The 3rd Workshop on Mathematical Reasoning
  Practical Aspects of Automated Reasoning, volume 9 of                and AI at NeurIPS’23, 2023.
  EPiC Series in Computing, pp. 1–10. EasyChair, 2012.
                                                                      Whalen, D. Holophrasm: a neural automated theo-
  doi: 10.29007/tnfd. URL /publications/paper/
                                                                       rem prover for higher-order logic. arXiv preprint
  Mzp.
                                                                       arXiv:1608.02644, 2016.
Paulson, L. C. Isabelle: A Generic Theorem Prover.
                                                                      Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and
  Springer Verlag, 1994.
                                                                       Chen, K. Internlm2. 5-stepprover: Advancing automated
Pichai, S., Hassabis, D., and Kavukcuoglu, K. In-                      theorem proving via expert iteration on large-scale lean
  troducing gemini 2.0: our new ai model for the                       problems. arXiv preprint arXiv:2410.15700, 2024.
  agentic era, December 2024. URL https://blog.
  google/technology/google-deepmind/                                  Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu,
  google-gemini-ai-update-december-2024.                                B., Zhang, L., Lu, X., Du, Q., et al. Deepseek-prover-v1.5:
                                                                        Harnessing proof assistant feedback for reinforcement
Polu, S. and Sutskever, I. Generative language model-                   learning and monte-carlo tree search. arXiv preprint
  ing for automated theorem proving. arXiv preprint                     arXiv:2408.08152, 2024.
  arXiv:2009.03393, 2020.
                                                                      Xin, R., Xi, C., Yang, J., Chen, F., Wu, H., Xiao, X., Sun,
Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,               Y., Zheng, S., and Shen, K. Bfs-prover: Scalable best-
  Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. Deepseek-                first tree search for llm-based automatic theorem proving.
  prover-v2: Advancing formal mathematical reasoning via                arXiv preprint arXiv:2502.03438, 2025.
  reinforcement learning for subgoal decomposition. arXiv
  preprint arXiv:2504.21801, 2025.                                    Xuejun, Y., Zhong, J., Feng, Z., Zhai, P., Yousefzadeh, R.,
                                                                        Ng, W. C., Liu, H., Shou, Z., Xiong, J., Zhou, Y., et al.
Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaud-                 Mathesis: Towards formal theorem proving from natural
  huri, S. An in-context learning agent for formal theorem-             languages. arXiv preprint arXiv:2506.07047, 2025.
  proving. In First Conference on Language Modeling,
  2024. URL https://openreview.net/forum?                             Yang, K. minif2f-lean4. https://github.com/
  id=V7HRrxXUhN.                                                        yangky11/miniF2F-lean4, 2023.

Venkatesh, A. Some thoughts on automation and mathemat-               Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
  ical research. Bull. Amer. Math. Soc.(NS), 61(2):203–210,             Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  2024.                                                                 Leandojo: Theorem proving with retrieval-augmented

                                                                 10
                            P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

  language models. Advances in Neural Information Pro-
  cessing Systems, 36:21573–21612, 2023.
Yang, K., Poesia, G., He, J., Li, W., Lauter, K., Chaudhuri,
  S., and Song, D. Formal mathematical reasoning: A new
  frontier in ai. arXiv preprint arXiv:2412.16075, 2024.
Zhao, X., Li, W., and Kong, L. Decomposing the enigma:
  Subgoal-based demonstration learning for formal theo-
  rem proving. arXiv preprint arXiv:2305.16366, 2023.
Zheng, C., Wang, H., Xie, E., Liu, Z., Sun, J., Xin, H., Shen,
  J., Li, Z., and Li, Y. Lyra: Orchestrating dual correction
  in automated theorem proving. Transactions on Machine
  Learning Research, 2024.
Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021. Available at: https:
  //github.com/openai/miniF2F.




                                                                 11
                                                                            P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

                                                                                                                                    Supplementary material for
       P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance
This supplementary document is organized as follows:

   • Section A presents a computational time analysis for each component of the proposed workflow.

   • Section B provides justification for key hyperparameter choices.

   • Section C compares the chosen strategy of extracting lemmas from the specialized prover’s failed attempts with direct
     LLM generation.

   • Section D provides the complete prompts used for all LLM tasks to ensure reproducibility.

A. Generation Times


                                                                                    
                                                                                                                                                                                                                                                                                               & D W H J R U \
                                                                                                                                                                                                                                                                                             / / 0  7 D V N V
                                                                                                                                                                                                                                                                                               6 / 0  $ W W H P S W V
                                                                                                                                                                                                                                                                                               & R Q G L W L R Q D O  7 D V N
                       $ Y H U D J H  7 L P H   V H F R Q G V 




                                                                       

                                                                                                                                         


                                                                       
                                                                                                                                                                            
                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                            

                                                                        
                                                                               p NL                 ma
                                                                                                      ry                                 V L V                          ain                                   ary                           ain                             ma
                                                                                                                                                                                                                                                                              ry                            ain
                                                                                                                                  D O \                          p m                                     m
                                                                                                                                                                                                                                     , pm                                                            , pm
                                                                                            p sum                        D  $
                                                                                                                                Q
                                                                                                                                                      D Q
                                                                                                                                                            G                                          um
                                                                                                                                                                                                    p s                          p l                              p sum                       R 
                                                                                                                                                                                                                                                                                                    pl
                                                                                                                  P P                              pl                                          Z                           Z                         Z     R                       Z
                                                                                                                                                                                                                                                                                         
                                                                                                            / H                                                                         P init                    P m
                                                                                                                                                                                                                         ain
                                                                                                                                                                                                                                              P init                                 ain
                                                                                                                                                                                                                                                                              P m
                                                                                                                                                                                                           P l  	                                                    P l  	


Figure 4. A detailed breakdown of the average time, in seconds, for each component of the P ROOF C OMPASS workflow compared to the
baseline. The chart categorizes operations into three types: one-time LLM guidance tasks (solid blue), conditional LLM tasks for lemma
processing (striped blue), and per-attempt costs for the Specialized Language Model (SLM) (red).

This section details the computational timings of individual LLM guidance tasks and Specialized Language Model (SLM)
proof attempts, followed by an analysis of their impact on overall time-to-solution performance.
Figure 4 presents the average durations for key operations. Initial LLM tasks, such as pN L generation and subsequent
summarization, constitute an upfront time investment, with specific durations detailed in the figure. Lemma analysis also
introduces an overhead if a problem is not solved within N = 16 initial attempts. A crucial benefit of this LLM pre-processing
is evident in the SLM attempt times: proof attempts guided by an LLM-generated psummary are notably faster (average
3.21s) than the baseline DSP-v1.5 CoT attempts (average 4.05s). This speed-up occurs because the baseline model, in its
CoT mode, must first generate its own informal proof sketch, as illustrated in Figure 3, whereas our method provides this
sketch as input. Similarly, the generation of informal proofs for lemmas (pl ) and the main theorem (pmain ), while adding to
LLM task time, leads to more efficient SLM generation for the corresponding lemma and final theorem proofs.
A quantitative analysis reveals when the upfront time cost of our method is offset by its greater per-attempt efficiency. For
problems requiring more than N = 16 attempts, P ROOF C OMPASS incurs a significant fixed time overhead of approximately
100.83 seconds. This accounts for initial LLM guidance tasks (29.87s), the first 16 failed SLM attempts (51.36s), and the
conditional lemma processing (19.60s). Following this, each subsequent attempt to prove a lemma or the main theorem is
highly efficient, costing only 2.84 seconds. In contrast, the baseline method costs 4.05 seconds per attempt, regardless of

                                                                                                                                                                                   12
                                                                                      P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

the stage. Consequently, the baseline’s cumulative time surpasses P ROOF C OMPASS’s full workflow after approximately
46 total attempts. This indicates that while the baseline may be faster for problems solved in fewer than 46 attempts,
P ROOF C OMPASS’s approach becomes more time-efficient for more complex problems requiring a larger computational
budget.

B. Hyperparameters Analysis

                                                                               


                                                                                                                                                                                                                                            




                                                                                                                                                                                                                                                & X P X O D W L Y H  8 Q L T X H  C K D Y H C  6 W D W H P H Q W V  * H Q H U D W H G
                                                                               
                      & X P X O D W L Y H  3 U R E O H P V  6 R O Y H G




                                                                                                                                                                                                                                         


                                                                                                                                                                                        3 U R E O H P V  6 R O Y H G
                                                                                                                                                                                     8 Q L T X H  / H P P D V  * H Q H U D W H G
                                                                                                                                                                                                                                            


                                                                               


                                                                                                                                                                                                                                            
                                                                               



                                                                                                                                                                                                                   
                                                                                                             1 X P E H U  R I  , Q L W L D O  ' 6 3  Y     $ W W H P S W V



Figure 5. Impact of the number of initial DSP-v1.5 attempts (N ) on the cumulative number of problems solved (blue line, left y-axis) and
the cumulative number of unique ‘have’ statements (potential lemmas) generated (red line, right y-axis). This data was collected from the
initial proof generation stage (Section 3.2), where DSP-v1.5 was guided by the LLM-generated proof summary, prior to any subsequent
lemma extraction (Section 3.3) or proving (Section 3.4) cycles.

This section provides the justification for the key hyperparameters used in the experiments (Section 4). The number of initial
proof attempts by DSP-v1.5 was set to N = 16. This choice is informed by the trends observed in Figure 5. While the rate
of solving new problems (blue curve) significantly diminishes after approximately N = 10 − 15 attempts, the pool of unique
‘have’ statements (potential lemmas, red curve) continues to expand, reaching around 2000 unique statements close to
N = 20. Setting N = 16 thus aims to capture a majority of the problems solvable by DSP-v1.5 in its initial attempts while
still generating a diverse corpus of material from failed attempts for effective LLM-guided lemma extraction (Section 3.3).
Regarding the maximum number of selected lemmas, this was set to k = 5. This value was established through preliminary
qualitative evaluations, which indicated that up to five strategically chosen lemmas were generally adequate to cover the
essential inferential steps of most proofs. Our methodology also allows the LLM to select fewer than k lemmas if a smaller
set is deemed optimal. Requesting a larger k in these evaluations risked the inclusion of trivial or redundant lemmas,
which could dilute the specialized prover’s focus and inefficiently expend its attempt budget on less critical sub-problems.
Therefore, k = 5 encourages the LLM to identify a concise yet impactful set of guiding lemmas for DSP-v1.5.

C. Alternative Lemma Generation Strategies
An alternative to our adopted method of extracting and selecting lemmas from the Specialized Language Model’s (SLM,
DSP-v1.5) attempts is to directly prompt a Large Language Model (LLM) to generate intermediate lemmas. This section
elaborates on why the former approach was chosen. The primary reason, identified in early experimentation, is that lemmas
directly generated by an LLM, while often semantically correct, tended to be syntactically different from those typically
produced by DSP-v1.5 and proved more challenging for the SLM to utilize.
For instance, in the problem numbertheory x5neqy2p4, directly LLM-generated lemmas often express constraints
using set theory (e.g., stating a variable is an element of a set of possible values), as can be seen in Figure 7. In contrast,
lemmas extracted from SLM attempts (Figure 6) frequently articulate equivalent constraints as disjunctions of direct equality

                                                                                                                                            13
                              P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

  theorem numbertheory_x5neqy2p4                                     theorem numbertheory_x5neqy2p4
   (x y : ℤ) :                                                         (x y : ℤ) :
   x^5 ≠ y^2 + 4 := by                                                 x^5 ≠ y^2 + 4 := by
   have l₀ : x^5 % 11 = 0 ∨ x^5 % 11 = 1 ∨ x^5 % 11 = 10 :=            have l₀ : ∀ (x : ℤ), x^5 % 11 ∈ ({0, 1, 11} : Set ℤ) := by
  by                                                                       sorry
        sorry                                                          have l₁ : ∀ (y : ℤ), (y^2 + 4) % 11 ∈ ({2, 4, 5, 7, 8, 9}
   have l₁ : (y^2 + 4) % 11 = 2 ∨ (y^2 + 4) % 11 = 4 ∨ (y^2 +        : Set ℤ) := by
  4) % 11 = 5 ∨ (y^2 + 4) % 11 = 7 ∨ (y^2 + 4) % 11 = 8 ∨                  sorry
  (y^2 + 4) % 11 = 9 := by                                             have l₂ : Disjoint ({0, 1, 11} : Set ℤ) ({2, 4, 5, 7, 8, 9}
        sorry                                                        : Set ℤ) := by
   have l₂ : x^5 % 11 ≠ (y^2 + 4) % 11 := by                               sorry
        sorry                                                          sorry
   sorry




       Figure 6. Lemmas extracted from failed SLM attempts.                        Figure 7. Lemmas generated by the LLM




assertions for the variable. While semantically equivalent, these syntactic variations significantly impacted the SLM’s
proving efficiency. In a comparative experiment where the SLM was tasked with proving theorems using these two styles of
guiding lemmas (requiring proofs for each lemma Pli and the main theorem Pmain ), the approach using LLM-extracted,
SLM-style lemmas required an average of 12 attempts. Conversely, using directly LLM-generated lemmas required an
average of 17.25 attempts (both averaged over 4 independent runs), a difference of over 40%.
This empirical difference suggests that the SLM is more adept at processing lemmas that conform to syntactic patterns
closer to its own typical outputs or training data. Therefore, our methodology prioritizes extracting and selecting lemmas
from the SLM’s own attempts. This aim is to provide strategically sound intermediate steps in a form that is more tractable
for the SLM, thereby optimizing the overall resource efficiency of the theorem-proving process.

D. LLM Prompts
This appendix provides all prompts used in our experiments for reproducibility.

D.1. User Prompt for Natural Language Proof Generation

       Provide a proof in natural language for the theorem below:
       Theorem statement in Lean 4:
       <formal statement>
       Informal Statement:
       <informal statement>
       Please provide a rigorous, detailed proof using natural language.




D.2. System Prompt for Proof Summarization

       You are a mathematical proof summarizer. You will be given a formal statement of a theorem in Lean 4, its informal
       counterpart, and a natural language proof of the theorem. Your response should contain only a summarized version
       of the natural language proof that’s both concise and complete. You should start you response with “We want to
       show that”, “We have”, “We need to show that” or “To show that”. You should write only the proof in your response,
       nothing more.




                                                                14
                           P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

D.3. User Prompt for Proof Summarization

   THEOREM STATEMENT IN LEAN 4:
   <formal statement>
   INFORMAL STATEMENT:
   <informal statement>
   COMPLETE PROOF:
   <nl proof>
   Write your summarized proof below


D.4. System Prompt for Lemma Selection

   You are a theorem-proving assistant trained to evaluate individual statements for their provability as standalone
   lemmas in Lean 4. Your task is to analyze a single list of candidate lemma statements, and then select at most 5 to
   cover all key steps of the natural language proof.
   Core Principle for Lemma Evaluation
   A candidate lemma statement L is “correct” if and only if a Lean 4 statement have [name] : [statement]
   := by [proof] would be successfully provable using ONLY the global assumptions/hypotheses provided in the
   formal theorem statement.
   A lemma is “incorrect” if it couldn’t be proven in Lean 4 using only the assumptions and hypothesis provided in the,
   or if it’s not fully justified by the natural language proof based on the global assumptions.
   Specific Criteria Guiding “Correct” vs. “Incorrect” Evaluation

     1. Global Provability: The exact mathematical statement of the lemma must be provably true using only the
        given hypotheses in the formal theorem statement.
     2. Justification by NL Proof: The lemma must be a direct and logical step or assertion found in the natural
        language proof, understandable from the global context.
     3. No Dependence on Undischarged Assumptions:
           • If the proof proceeds by cases (e.g., “Case 1: Assume P ... then R”, “Case 2: Assume Q... then T ”), a
             lemma stating P by itself, Q by itself, R by itself (if R depends on P ), or T by itself (if T depends on Q)
             is incorrect. These statements are only true under temporary, local assumptions.
           • However, a lemma stating P ∨ Q (if this disjunction is provable globally) would be correct.
           • Similarly, P → R or Q → T might be correct if these implications are what the proof establishes.

     4. Contradictions & Unjustified Steps:
           • If a lemma contradicts a statement in the proof or a hypothesis, it’s incorrect.
           • If a lemma makes an assertion not present or derivable from the NL proof and global hypotheses, it’s
             incorrect.
           • In a proof by contradiction, if ‘A’ is true and the proof temporarily assumes ‘not A’ to reach a contradiction,
             a lemma stating ‘not A’ as a factual step from the global context is incorrect.
     5. Consequences of Incorrect Lemmas: If a lemma B follows logically from another lemma A, and lemma A is
        determined to be “incorrect”, then lemma B is also “incorrect”.

   Input Format You’ll receive the formal statement of the theorem in Lean 4, its informal counterpart, a complete
   natural language proof, and a list of candidate lemma statements.
   THEOREM STATEMENT IN LEAN 4:
   <Formal statement in Lean 4>
   INFORMAL STATEMENT:
   <Informal translation of theorem statement>


                                                             15
                       P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance


COMPLETE PROOF:
<Complete natural language proof of theorem>
LEMMAS:
0: <lemma in Lean 4>
1: <lemma in Lean 4>
...
N-1: <lemma in Lean 4>
Output Format (Strictly Adhere to This Structure) LEMMA ANALYSIS
0:
Analysis: [Provide a short, step-by-step analysis of lemma 0. Explain precisely why it IS or IS NOT provable as a
standalone ‘have’ statement given ONLY the theorem’s global hypotheses and the NL proof. Reference the Core
Principle and Specific Criteria above.]
Evaluation: [correct or incorrect]
1:
Analysis: [Analysis for lemma 1 as above.]
Evaluation: [correct or incorrect]
...
N-1:
Analysis: [Analysis for lemma N-1 as above.]
Evaluation: [correct or incorrect]
SELECTION RATIONALE FOR CHOSEN LEMMAS
AVAILABLE LEMMAS: [List all lemmas that you evaluated as ’correct’.]
REASONING: [Based on your ’Evaluation’ of all original lemmas above, select up to 5 correct lemmas that
represent the key intermediate steps from the provided natural language proof. Do not select lemmas that are
restatements of the theorem’s hypotheses or its final conclusion. Always try to select 5 lemmas, choosing fewer only
if there are not enough correct intermediate lemmas available. The final chosen lemmas must be ordered to reflect
the logical flow of the natural language proof.]
CHOSEN LEMMAS

[Write all chosen lemmas here. Each chosen lemma must be presented in the following format. Number them
sequentially starting from l0 , regardless of their original index.]

have l0 : <statement> := by
have l1 : <statement> := by
...
This is how your output should look like
LEMMA ANALYSIS
0:
Analysis: [Analysis of lemma 0 based on the criteria explained above]
Evaluation: [Evaluation of lemma 1 (correct or incorrect)]
1:
Analysis: [Analysis of lemma 0 based on the criteria explained above]
Evaluation: [Evaluation of lemma 1 (correct or incorrect)] ...
N-1:
Analysis: [Analysis of lemma 0 based on the criteria explained above]
Evaluation: [Evaluation of lemma 1 (correct or incorrect)]
SELECTION RATIONALE FOR CHOSEN LEMMAS
AVAILABLE LEMMAS:
[first correct lemma statement]
...
[last correct lemma statement]
REASONING: [Reasoning about which (AT MOST 5) lemmas to choose, with the goal of selecting the key



                                                        16
                          P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance


   intermediate steps of the NL proof, excluding hypotheses and the conclusion, and ordering them according to the
   proof’s logical flow.]
   CHOSEN LEMMAS:
   [List of chosen lemmas. Note that the subscripts should be in the order 0, 1, 2, ..., irrespective of the number of its
   corresponding lemma in the input.]

   have l0 : <statement> := by
   have l1 : <statement> := by



D.5. User Prompt for Lemma Selection

   THEOREM STATEMENT IN LEAN 4:
   <formal statement>
   INFORMAL STATEMENT:
   <informal statement>
   COMPLETE PROOF:
   <nl proof>
   LEMMAS:
   0: <lemma 0>
   1: <lemma 1>
   ...
   N-1: <lemma N-1>
   Proceed with your response below, strictly following all guidelines and output structures specified in the system
   prompt.


D.6. System Prompt for Lemma and Final Proof Generation

   You are a mathematical proof analyst. Your task is to analyze a given mathematical proof (provided alongside
   formal and informal statements) and break it down into a sequence of logical steps, formatted clearly for potential
   formalization in Lean 4.
   You will receive:

     1. A formal theorem statement in Lean 4, potentially including hypothesis labels like h0 , h1 .
     2. An informal statement of the theorem.
     3. A complete natural language proof of the theorem.

     4. Formal lemma statements (e.g., have l0 : < ... > ) that will appear in the Lean proof.
   Analyze the provided natural language proof and follow these guidelines meticulously to structure your output:

     1. REASONING Section:
           • Start with REASONING:.
           • Analyze the provided natural language proof to identify its overall strategy and key insights.
           • Explicitly note how the formal lemma statements (have l0 , have l1 , etc.) map to the key steps in the
             natural language proof. These will directly correspond 1-to-1 with the l0 :, l1 : steps you generate. You
             must NEVER include new lemma statements that are not present in the input.
           • Briefly list the main steps you identified in the provided proof, ensuring each step aligns with one of the
             provided formal lemma statements. Remember to never include new lemma statements in the steps.


                                                             17
                          P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance


          • In the case the formal lemma statements don’t match the steps in the proof well, you should try to modify
            the natural language proof to make it match the formal lemma statements. You should NEVER modify the
            formal lemma statements themselves, or add new lemma statements.
 2. STEPS Section:
          • Follow with STEPS:.
          • Label the key milestones as l0 :, l1 :, etc. These must exactly match the order and content of the formal
            have statements provided.
          • Each step (li :) must state a precise mathematical fact in natural mathematical language.

 3. Step Proofs (Proof: sections):
          • Follow each li : statement with Proof:.
          • Provide a concise summary of the justification found in the provided natural language proof.
          • To show dependency on a previous step lj , state the mathematical result of lj as a fact within the narrative
            summary of the proof for li , instead of mentioning the name lj directly. You should NEVER mention the
            name lj inside the proof.
          • Correct: “Since <mathematical statement from lj holds / was established>, the proof proceeds by...”
          • Incorrect: “By lj ...” or “Using the result from lj ...”. This is incorrect because ’lj ’ is present in the proof,
            which is not allowed.
 4. Final Proof Section:
          • End with Final Proof:.
          • Summarize how the proof combines the results stated in the li steps to reach the final conclusion.
          • State intermediate results directly as established facts, without referencing step labels.
 5. Formatting:
    Your response must follow this exact structure:
    REASONING:
    <Analysis noting correspondence between formal lemmas and steps>
    STEPS:
    l0 :
    <First mathematical statement matching first have>
    Proof:
    <Detailed explanation with all necessary calculations>
    l1 :
    <Next mathematical statement matching next have>
    Proof:
    <Detailed explanation with all necessary calculations>
    ...
    Final Proof:
    <Conclusion using established results>

Here’s an example showing the expected output format:
<example from miniF2F-valid>




                                                              18
                       P ROOF C OMPASS: Enhancing Specialized Provers with LLM Guidance

D.7. User Prompt for Lemma and Final Proof Generation

   THEOREM STATEMENT IN LEAN 4:
   <formal statement>
   INFORMAL STATEMENT:
   <informal statement>
   COMPLETE PROOF:
   <nl proof>
   FORMAL LEMMAS::
   <lemmas>




                                                     19
