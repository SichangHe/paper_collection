                                            Towards Trustworthy Legal AI through LLM Agents and Formal Reasoning

                                                             Chen Linze1 , Cai Yufan1 , Hou Zhe2 and Dong Jin Song1
                                                                           1
                                                                             National University of Singapore
                                                                                   2
                                                                                     Griffith University
                                                     e1344652@u.nus.edu, caiyf@nus.edu.sg, z.hou@griffith.edu.au, dcsdjs@nus.edu.sg


                                                                  Abstract                                 rization, pleading drafting [Hendrycks et al., 2021], and bar-
arXiv:2511.21033v2 [cs.AI] 5 Mar 2026




                                                                                                           exam question answering [Katz et al., 2024]. However,
                                             Legal decisions should be logical and based on                purely neural approaches are prone to hallucinating authori-
                                             statutory laws. While large language models                   ties [Hou et al., 2024], conflating distinct doctrinal require-
                                             (LLMs) are good at understanding legal text, they             ments [Savelka, 2023], and producing conclusions whose
                                             cannot provide verifiable justifications. We present          logical validity cannot be independently verified. Domain-
                                             L4L , a solver-centric framework that enforces for-           adapted systems such as C HAT L AW [Cui et al., 2023],
                                             mal alignment between LLM-based legal reason-                 L AW LLM [Shu et al., 2024], and L EXI [Ho et al., 2025] re-
                                             ing and statutory laws. The framework integrates              duce factual errors through retrieval-augmented generation,
                                             role-differentiated LLM agents with SMT-backed                yet they ultimately rely on opaque generation processes and
                                             verification, combining the flexibility of natural            do not provide guarantees.
                                             language with the rigor of symbolic reasoning.
                                                                                                           Legal Formalization. The use of formal representations
                                             Our approach operates in four stages: (1) Statute
                                                                                                           for legal norms has long been a central research direction
                                             Knowledge Building, where LLMs autoformalize
                                                                                                           in Law [Richmond et al., 2024]. Importantly, legal formal-
                                             legal provisions into logical constraints and val-
                                                                                                           ization does not claim to exhaust the full semantic or moral
                                             idate them through case-level testing; (2) Dual
                                                                                                           content of law. Rather, it provides a controlled abstraction
                                             Fact-and-Statute Extraction, in which prosecutor-
                                                                                                           of explicitly articulated statutes and rules that can be sub-
                                             and defense-aligned agents independently map case
                                                                                                           jected to logical scrutiny [Prajescu and Confalonieri, 2025].
                                             narratives to argument tuples; (3) Solver-Centric
                                                                                                           At the same time, legal decision-making inevitably involves
                                             Adjudication, where SMT solvers check the le-
                                                                                                           judicial discretion, particularly in the presence of vague con-
                                             gal admissibility and consistency of the arguments
                                                                                                           cepts, competing principles, or unforeseen factual patterns.
                                             against the formalized statute knowledge; (4) Ju-
                                                                                                           Such discretion does not imply the absence of structure, but
                                             dicial Rendering, in which a judge agent inte-
                                                                                                           reflects the existence of alternative interpretations and subse-
                                             grates solver-validated reasoning with statutory in-
                                                                                                           quent amendments that refine base statutes [Foy III, 2010]. A
                                             terpretation and similar precedents to produce a
                                                                                                           trustworthy legal AI system needs therefore not eliminate dis-
                                             legally grounded verdict. Experiments on public
                                                                                                           cretion, but make interpretive choices explicit and auditable.
                                             legal benchmarks show that L4L consistently out-
                                             performs baselines, while providing auditable jus-            Bridging Substantive and Formal Rationality. In this
                                             tifications that enable trustworthy legal AI.                 work, we present L4L , a solver-centered framework for
                                                                                                           bridging substantive and formal rationality in LLM-based le-
                                                                                                           gal reasoning. L4L embeds role-differentiated LLM agents
                                        1   Introduction                                                   within a formal reasoning loop governed by formalized statu-
                                                                                                           tory constraints. Legal norms are represented using a typed
                                        Legal decision-making requires more than accurate linguis-         schema that captures actors, actions, conditions, and deon-
                                        tic interpretation of statutory text. In rule-of-law systems,      tic status, and are compiled into executable SMT constraints.
                                        judicial outcomes are expected to satisfy formal rational-         LLM agents aligned with prosecutorial and defense roles in-
                                        ity [Linna and Linna, 2025]. Conclusions must be justi-            dependently extract case facts and candidate statutes. An
                                        fied by demonstrating their consistency with explicitly stated,    SMT solver then adjudicates the resulting constraint system,
                                        general, and logically coherent legal rules [Sadowski and          verifying logical consistency and identifying misalignment
                                        Chudziak, 2025b]. Courts are therefore constrained not to          between competing arguments and statutory requirements.
                                        select outcomes based on intuitive or moral preference alone,         Crucially, L4L separates adjudication from rendering. For-
                                        but to articulate decisions that can be traced back to governing   mal reasoning outcomes produced by the solver are not di-
                                        statutes, interpretations, and precedents [Kesari et al., 2024].   rectly exposed to end users. Instead, a judge agent performs
                                        Current Limitations. Recent LLMs have shown impres-                judicial rendering by integrating solver-validated results with
                                        sive performance on legal tasks, including opinion summa-          statutory interpretation principles and retrieved analogous
precedents, producing a transparent and legally grounded ver-         The resulting Horn clauses are
dict. This design preserves the interpretive flexibility required
for substantive rationality, while ensuring that final conclu-         ∀a, α, κ. art i(a, α, κ) ∧ cli,j (κ)
sions remain anchored in formally verified legal constraints.           → prohibited(a, α, κ) ∧ penalty(a, α, κ) = pi,j .      (2)
   We evaluate L4L on public legal benchmarks [Li et al.,
2023] [Xue et al., 2024], demonstrating strong improve-                Formal Knowledge Base (KB). Each article in the crim-
ments over LLM baselines, in statute selection, verdict accu-       inal code is compiled into the above form, with cross-
racy, and sentencing quality. Crucially, our system produces        references (e.g., “Article 347(1)–(3)”) explicitly disam-
solver-checked symbolic justifications that enable auditabil-       biguated and key quantities such as drug amounts and mon-
ity of legal conclusions.                                           etary thresholds parameterized. The construction of the
Contributions.                                                      statute and judicial interpretation KB follows a neurosym-
                                                                    bolic formalization-and-testing paradigm. As illustrated in
   • We propose a systematic approach to formalizing statu-
                                                                    Figure 1, natural-language statutes and judicial interpreta-
      tory law, in which natural-language legal provisions are
                                                                    tions are automatically formalized into SMT models. These
      translated into executable logical constraints with ex-
                                                                    SMT models are subsequently validated through syntactic
      plicit semantic structure.
                                                                    checks and semantic linting to ensure well-formedness and
   • We introduce a SMT solver-centered legal reasoning             logical soundness. We further evaluate the correctness of the
      framework that bridges substantive and formal rational-       formalized models using real-world legal cases with known
      ity by integrating formal reasoning into the adjudication.    outcomes, and iteratively repair the SMT constraints when
   • We design a role-differentiated legal agent architecture,      solver results largely deviate from the corresponding gold la-
      in which prosecutor- and defense-aligned agents inde-         bels. This process grounds the induced statutory constraints
      pendently extract facts and argue statute applicability       in both formal validity and empirical legal practice.
      under shared formal constraints.
   • We conduct extensive experiments on multiple bench-            2.2   Legal AI Agents
      marks, demonstrating that our approach achieves higher        Figure 1 (left half) depicts two role-differentiated LLM
      performance and robustness than other legal AI systems.       agents, prosecutor and defense attorney, that mirror the real
                                                                    courtroom. The pipeline is in the following steps:
2     Approach
Our framework couples the abilities of LLMs with the proof          Suspect-Centric Decomposition. Criminal cases often in-
obligations enforced by an SMT solver (Z3) in order to de-          volve multiple suspects whose roles, intent, and liability may
liver auditable legal conclusions.                                  differ substantially. Given a case narrative, L4L first decom-
                                                                    poses it into a set of suspect-specific views, and all subse-
2.1    Law Formalization                                            quent fact extraction and statute reasoning are performed in-
Meta-schema. We start from a universal first-                       dependently for each suspect. This design ensures that ev-
order template that captures the quadruple Ac-                      idential facts, statute applicability, and sentencing decisions
tor–Action–Condition–Norm, with penalty attached:                   are not conflated across different defendants.

    ∀a:Actor, α:Action, κ:Condition, n:Norm, p:Penalty.             Dual Fact–&–Statute Extractors. For each suspect, the
                                                                    P ROSECUTOR LLM and ATTORNEY LLM receive the same
    scope(a, α, κ, n) → applies(a, α, κ, n, p).         (1)
                                                                    free-text case narrative but are prompted with adversarial
   The sort Norm is an element of prohibited,                       instructions (“maximise conviction” vs. “maximise acquit-
obligated, permitted, while scope will be progres-                  tal”). The dual-extractor design prevents a single model from
sively refined in the subsequent layers. This schema paritally      blending prosecution and defense biases. Each produces:
follows the previous work [Xue et al., 2024]. The schema
is globally consistent across all statutes, and every constraint    • Fact tuples F⟨a, α, κ, w⟩, which instantiate the Actor–
field in downstream verification has a corresponding default          Action–Condition components of the shared legal schema,
extraction output.                                                    where w ∈ [0, 1] encodes evidential confidence;
Article instantiation. For a concrete statute article Arti          • Candidate statute ranks S = [(id1 , π1 ), . . . ] whose prior
we introduce an article guard art i that fixes the over-              probabilities πi stem from retrieval over the formal KB
all applicability domain (jurisdiction, offense category, sub-        using dense embeddings.
ject status, etc.). The formalized article is connected  with
the meta-schema by scope ⟨prohibited, Arti ⟩, a, α, κ        :≡     2.3   Solver-Centered Legal Reasoning
art i(a, α, κ).                                                     L4L is organized around a solver-centered legal reasoning
Clause instantiation. Each article typically contains sev-          pipeline, in which symbolic satisfiability and optimization
eral clauses that refine quantitative thresholds or aggravating     serve as the authoritative mechanisms for validating legal ap-
circumstances. Let Arti .cj denote clause j of article i. For       plicability and deriving legally admissible outcomes. All le-
each article, we define a clause guard cli,j together with a        gal conclusions are produced only if they satisfy the formal
statutory penalty range pi,j .                                      statutory constraints encoded in the SMT solver.
Figure 1: Overview of L4L , a solver-centered framework for auditable legal reasoning. (Top) Law formalization: natural-language text
are automatically translated into SMT constraints, with comprehensive checking and testing, to construct a verified formal knowledge base.
(Left) Legal AI Agents: given a case description, prosecutor and defense LLM agents independently extract suspect-centric facts and propose
applicable statutes. (Bottom) Legal reasoning: Agent outputs are autoformalized into typed fact tuples and checked separately against the
formal KB. An SMT solver verifies article-level applicability and then determines the satisfied statutory clauses, producing legally admissible
conclusions. Verified statutes, with similar cases and interpretation, are finally rendered by a judge LLM into the final verdict and sentence.


Autoformalizer LLM. A role-neutral LLM serves as a                        the facts. For each clause guard cli,j , check
schema-guided interface between the dual fact extractors and
                                                                                          Φ ∧ art i(a, α, κ) ∧ cli,j (κ).
the formal reasoning backend. For each suspect, it trans-
forms the structured outputs ⟨F, S⟩ into a well-typed SMT                 A clause Arti .cj is selected if the above formula is satisfi-
constraint set Φ by instantiating the shared meta-schema and              able. Each selected clause uniquely determines the corre-
querying the formal knowledge base K. Concretely, the aut-                sponding legal consequence, including offense qualification
oformalizer performs the following steps:                                 and statutory penalty range pi,j . When multiple clauses are
• Value grounding, converting linguistic or fuzzy quantities              simultaneously satisfiable, the solver enumerates all admis-
  (e.g., “large amount”, “multiple transactions”) into sym-               sible clauses, leaving discretionary selection to downstream
  bolic variables and numeric constraints;                                judicial policies.
• Statute resolution, expanding statutory references and                  Iterative feedback loop. If either applicability verification
  clause combinations (e.g., “Art. 347(1)&(3)”) into guarded              or judgment derivation fails (i.e., the solver reports unsat
  Horn clauses defined in the formal KB;                                  or unknown), the pipeline does not produce a verdict. In-
• Provenance tagging, attaching agent identifiers and con-                stead, the minimal unsat core is returned to the autoformal-
  fidence weights to each asserted fact and statute, enabling             izer, which identifies whether the inconsistency arises from
  traceability and conflict diagnosis.                                    fact extraction errors, statute over-approximation, or incom-
                                                                          patible clause combinations. The corresponding constraints
  The resulting constraint system is                                      are revised, and solver-centered reasoning is re-invoked un-
                                                                          til a legally consistent outcome is obtained or all candidate
              Φ = Φfacts ∪ Φstatutes ∪ Φguards ,
                                                                          statutes are exhausted.
which constitutes the sole input to the solver.
                                                                          2.4    Judge LLM and Rendering Mechanism.
Formal Legal Reasoning. Formal legal reasoning is con-
                                                                          Once SMT-solver returns a sat model, its proof object to-
ducted in two successive solver stages, corresponding to
                                                                          gether with the surviving statutes and sentencing ranges are
statutory applicability and clause-level qualification.
                                                                          passed to the J UDGE LLM. The Judge LLM drafts (i) a
Stage I: Article applicability verification. We first verify              declarative verdict (guilty / not guilty) and the statutes, (ii)
whether a candidate statutory article is applicable to the ex-            a quantified sentence derived from the SMT solver’s ranges,
tracted facts. Formally, for each article Arti , we check the             and (iii) a narrative justification that references solver-derived
satisfiability of Φ ∧ ∃a, α, κ. art i(a, α, κ), where art i de-           facts, the relevant Code articles, judicial interpretations, and
notes the article-level guard encoding the scope of Arti . If             each party’s key arguments.
the solver returns unsat, the article is deemed inapplicable              Similar Case Retrieval. In parallel with formal reason-
and discarded from further consideration.                                 ing, L4L retrieves similar cases based on the verified statutes
Stage II: Clause qualification. For each applicable article,              and case descriptions. Similar cases are not used to over-
we further determine which clause(s) Arti .cj are satisfied by            ride solver results, but are injected as auxiliary context to the
Judge LLM. This design reflects real-world judicial practice,         • Transaction facts: {payment channel=WeChat, pay-
where precedent and analogous cases inform the exercise of               ment amount yuan=1000, completed=True}
judicial discretion without altering statutory applicability.         • Participation: {Gong role=organizer}
Judicial Interpretation Matching. Judicial interpretation             • Mens rea: {intentional=True}
is conditioned on the set of verified statutes and serves to re-      • Procedural: {voluntary surrender=True}
fine their legal meaning in specific contexts. It is injected      (B) Defense Attorney (abbreviated):
into the prompt of Judge LLM using the statute matching.              • Quantity band emphasis:             {drug type=MDMA,
This separation allows the core reasoning pipeline to remain             net weight g=6.0, threshold=low}
statute-centric, while enabling flexible adaptation to different      • Role emphasis: {Gong role=intermediary}
legal interpretive regimes and evolving jurisprudence.                • Mitigation: {voluntary surrender=True}
Summary. Our design explicitly combines formal rational-              • Uncertainty flags: {purity=unknown}
ity with substantive judgment. Formal rationality is enforced      Formal Legal Reasoning Each statute/interpretation is
by the SMT solver through applicability verification. Sub-         compiled into solver constraints, which are proven satisfiable
stantive rationality, including judicial discretion and contex-    by an SMT solver and can be exported as verified justifica-
tual reasoning, is modelled at the LLM layer through the in-       tion. Below we show the key constraints.
corporation of similar cases and judicial interpretations.
                                                                      • Art. 347 (Trafficking): satisfiable ⇒ retained.
                                                                      • Interpretation [2016] No. 8 : 6.0 > 20 ⇒ false.
3    Running Example                                                  • Art. 67 (Mitigation): if surrender/confession facts are
In this section, we introduce a running example to illustrate            consistent ⇒ retained.
our pipeline end-to-end.                                              • Art. 65 (Recidivism): retained only if prior-sentence
                                                                         and 5-year window are supported by admissible evi-
Case Synopsis.
                                                                         dence; otherwise the slice becomes unknown.
     Defendant Gong Qiang received a WeChat message
     from Luo, requesting the purchase of 1,000 yuan               Final Judge Rendering. By explicitly matching Fa Shi
     worth of drugs. After receiving the 1,000 yuan                [2016] No. 8, the system classify MDMA as other drugs in
     transfer via WeChat, Gong Qiang, together with ac-            the Article 347 and enforces the quantitative guard. This
     complice Zhang, handed over 10 grams of MDMA                  prevents miss-charging or miss-sentencing caused by other
     to Luo. On Nov 7, 2019, Gong Qiang voluntarily                undefined drugs and the thresholds. After the solver fixes
     surrendered to the police.                                    the applicable charge and quantity band, the system can re-
                                                                   trieve similar precedents with the same drug type (MDMA),
Formal Statute and Judicial Interpretation. As shown in            comparable weight range (e.g., 1–10g), and similar procedu-
Table 1, our formal KB contains both criminal-law articles         ral posture, to produce stable sentencing rationales. Finally,
(e.g., Article 347 on trafficking; Article 65 on recidivism;       the judge agent generates an auditable draft. In the exam-
Article 67 on surrender/confession) and judicial interpreta-       ple, a prompt-only judge tended to overestimate (“2 years”),
tions that refine quantitative thresholds. In particular, the      while L4L moves the recommendation toward the ground-
Supreme People’s Court interpretation Interpretation [2016]        truth range (“around 1 year”).
No. 8 provides: Amphetamine-type drugs such as MDMA,
morphine-equivalent more than 20 grams but less than 100
grams ⇒ “other drugs in relatively large quantity” for pur-
                                                                   4   Experiments
poses of Criminal Law Article 347(2)(1) and Article 348.           Specifically, we investigate the following research questions:
This interpretation becomes a quantity-threshold constraint            • RQ1: How does our method perform compared to state-
used to classify the case into the appropriate sentencing band.          of-the-art baselines?
   Table 2 illustrates the canonical reasoning template to op-
                                                                       • RQ2: What is the contribution of different components
erationalize statute-specific sentencing logic. For each ap-
                                                                         of our method to final sentencing accuracy?
plicable criminal law article, L4L automatically compiles the
corresponding statutory text and judicial interpretations. This        • RQ3: Does our method provide better robustness?
formulation is uniform across statutes and does not rely on        Datasets. We conduct our experiments on three datasets
article-specific heuristics.                                       covering real-world cases and controlled perturbations. De-
Role-Differentiated Legal AI Agents. We instantiate two            tailed dataset preprocessing, and annotation procedures are
aligned agents: (i) Prosecutor agent that tends to maximize        provided in the appendix among supplementary material. Ta-
statutory coverage and aggravating factors, and (ii) Defense       ble 3 shows the dataset statistics, including case counts, aver-
agent that prioritizes exclusion/mitigation and evidentiary un-    age lengths, and the average number of statutes.
certainty. Both agents must express outputs in a shared formal         • LeCaRDv2 Dataset [Li et al., 2023], a large-scale Chi-
schema. Given the narrative, the two agents independently                nese criminal case dataset with statutes and judgments;
extract structured facts and the autoformalizer translated them        • LEEC Dataset [Xue et al., 2024], a legal element ex-
into SMT assertions.                                                     traction corpus derived from publicly available Chinese
(A) Prosecutor (abbreviated):                                            criminal judgments, which we further process to support
    • Drug facts: {drug type=MDMA, net weight g=6.0}                     suspect-level evaluation;
  Article           Formal Schema                                              Description and Legal Implication
  347 (Drug         Norm (prohibited); Actor (person, unit, Age (inte-         Defines factors affecting sentencing for narcotics
  Trafficking)      ger, ≥12 years, default ≥18), ...); Action (smug-          crimes, including actor type, age, type of drug activ-
                    gling, selling, transporting, manufacturing); Condi-       ity, drug quantity thresholds, and aggravating circum-
                    tion ( DrugQuantity (opium/heroin/meth thresholds          stances (e.g., organized or armed operations). These
                    in grams); Circumstance (ringleader, armed protec-         parameters determine the severity level of Article 347
                    tion, international trafficking); ); Penalty(...)          sentencing rules.

                                            Table 1: Examples of Law-Specific Knowledge Base.

 Algorithm                                                              Example Execution: Article 347 (Drug Trafficking)
 Input: Statute-specific fact slice f , compiled rule set Φ             1: Identify Actor = Guo Qiang; Action = trafficking drugs
 Output: Applicable sentencing clause C                                 2: Encode facts (DrugType = MDMA, NetWeight = 6g, Intentional
 1: Initialize constraint solver S; set C = ∅                           = True)
 2: Declare legal entities (actors, actions, ...)                       3: Iterate over Article 347 clauses in descending severity
 3: Encode factual predicates from f into S                             4: Push state for r1 (large quantity)
 4: Sort rules ri ∈ Φ by descending statutory severity                  5: Check r1 ⇒ UNSAT (quantity threshold not met)
 5: for each ri do                                                      6: Push state for r2 (medium quantity)
 6: Push solver state                                                   7: Check r2 ⇒ UNSAT (quantity threshold not met)
 7: Encode statutory and interpretative constraints of ri               8: Push state for r3 (small quantity)
 8: Check satisfiability of ri under S                                  9: Check r3 ⇒ SAT
 9: if SAT and C = ∅ then                                               10: Push state for r4 (small quantity + different circumstance)
 10:      Assign C ← consequence of ri                                  ...
 11:      Pop solver state and break                                    14: Assign C = “Fixed-term imprisonment ≤ 3 years”
 12: Pop solver state                                                   15: Discard other solver states
 13: if C = ∅ then C ← “No applicable clause”                           16: Verify non-empty C, ready for return
 14: return C                                                           17: Return final sentencing clause under Article 347

   Table 2: Canonical Solver-Based Reasoning Template for Statutory Sentencing (Algorithm and Example Execution for Article 347).


  • Synthetic Perturbation Dataset, constructed by inject-              the suspect level, with an additional metric for multi-suspect
    ing legally meaningful factual modifications to assess              identification. For robustness evaluation, we use the Syn-
    robustness under controlled statute-triggering changes.             thetic Perturbation Dataset and measure the change Accu-
                                                                        racy, which quantifies whether the model correctly captures
                                                                        changes induced by designed factual perturbations. Imple-
 Dataset                    #Cases    Avg. Length      Avg. #Statutes
                                                                        mentation details and the code are provided in the supple-
 LeCaRDv2                   55192        889.17               4.53      mentary material.
 LEEC (Suspect-Level)        9470        654.49               5.25
 Perturbed Dataset           3622         77.36               4.88      4.1   RQ1: Accuracy Evaluation
                                                                        We evaluate all models on statute identification and sentenc-
            Table 3: Statistics of Experimental Datasets.               ing prediction. Statute prediction is formulated as a multi-
                                                                        label classification task, and we report Precision, Recall,
                                                                        and F1-score for both general and specific provisions. For
Baselines. The baselines cover both pure LLM inference,                 sentencing prediction, we report Average Sentencing Error
specialized legal agents and retrieval-augmented settings to            (ASE) in Months and Root Mean Squared Error (RMSE) in
ensure a comprehensive comparison, including GPT-4o, GPT                Months. We measure a Valid Ratio to assess legal consistency
o4-mini, GPT-5.2, DeepSeek V3, Claude 4 Sonnet, DISC-                   of the predicted outcomes and the formal laws. For L4L , it
Law [Yue et al., 2023] and LexiLaw [Li et al., 2024].                   measures whether the Judge LLM follows the provided for-
Settings. We adopt GPT-5.2 throughout the entire pipeline               mal reasoning results. On the LEEC dataset, we report Sus-
of L4L . Our experiments evaluate two aspects of perfor-                pect Extraction F1 to evaluate the accuracy of suspect-level
mance: (i) accuracy on real-world legal cases, and (ii) ro-             decomposition in multi-defendant cases. The detailed met-
bustness under controlled factual perturbations. Across all             rics are in the appendix. Table 4 summarizes provision pre-
datasets, we construct disjoint subsets for (i) formal knowl-           diction performance. On LeCaRDv2, general-purpose LLMs
edge base validation, (ii) retrieval and case matching, and             tend to favor recall at the expense of precision, leading to
(iii) final evaluation. Unless otherwise specified, each subset         systematic over-prediction of applicable statutes and more re-
is obtained by random sampling under fixed seeds to ensure              cent LLMs further improve recall. In contrast, L4L applies
fair and reproducible comparison. Evaluation on LeCaRDv2                SMT-based verification to filter legally inconsistent argu-
is performed at the case level, while LEEC is evaluated at              ments, which may reject some marginally applicable provi-
                                              LeCaRDv2                                                  LEEC
                                   General                   Specific                   General                    Specific
        Model                P       R        F1      P         R        F1       P        R       F1          P      R        F1
        LexiLaw             8.96    26.27    13.36   47.76    49.91     48.81    1.03     0.21     0.34     1.89     3.09      2.23
        DISC-LawLLM        66.67     2.13     4.12   64.22    75.27     69.31    0.00     0.00     0.00     1.56     1.25      1.04
        GPT o4-mini        21.54    35.00    26.67   69.00    21.00     32.00   34.80    23.24    25.52    65.93    63.37     62.82
        GPT-4o             12.00    36.00    18.00   67.00    73.00     70.00   34.00    23.27    24.85    67.15    66.58     65.22
        Claude 4 Sonnet    32.79    26.67    29.41   64.00    75.00     69.00   36.85    24.05    26.05    65.96    63.63     63.73
        DeepSeek v3        10.25    44.84    16.88   60.19    82.77     69.70   32.16    22.95    23.29    64.72    63.49     62.50
        GPT-5.2            23.47    46.25    31.14   70.71    81.05     75.53   52.01    37.38    39.08    79.73    76.06     76.46
        L4L (Ours)         34.00    45.95    39.08   81.03    77.05     78.99   64.05    40.77    45.51    82.35    76.71     78.13

      Table 4: Provision Prediction Performance on dataset LeCaRDv2 and LEEC (%), comparing (P)recision, (R)ecal, and F1 scores.


sions but substantially improves precision. L4L maintains a             where Strue denotes statutes whose applicability changes un-
better precision–recall balance and achieves the best F1 score          der perturbation, and Spred the statutes predicted after per-
on both general and specific provisions. The advantage of               turbation. Only perturbed statutes are considered. Table 7
L4L is more pronounced on LEEC dataset. L4L delivers the                reports the robustness performance of all models. The de-
best precision, recall, and F1 scores in multi-defendant set-           tailed perturbation settings are provided in the appendix.
tings, where complex suspect-level cases increases difficul-            L4L achieves the highest Change Accuracy (62.56%), outper-
ties. Table 5 summarizes sentencing accuracy, legal validity,           forming all general-purpose and domain-specific baselines.
and suspect extraction performance. L4L achieves the best               Domain-specific systems show limited adaptability. These
overall performance, with the lowest sentencing error, highest          results indicate that combining agent-based cross-checking
Valid Ratio under statute grounding, and the highest Suspect            with formal logic validation enables more reliable identifica-
Extraction F1, demonstrating robust suspect-centric reason-             tion of legally relevant changes, yielding more stable statute
ing in multi-defendant cases. These results underscore the              updates. Remaining errors mainly stem from upstream fact
importance of solver-anchored verification for accurate and             extraction, suggesting a direction for future improvement.
legally admissible sentencing.
                                                                        5     Discussion and Limitations
4.2   RQ2: Ablation Study
                                                                        Error Analysis. We observe that the performance for gen-
To quantify the contribution of each component in our Le-               eral provisions is consistently lower than that for specific pro-
gal LLM Agent framework (Figure 1), we conduct an abla-                 visions. General articles regulate contextual and offender-
tion study on LeCaRDv2 by selectively disabling key mod-                related factors, such as intent, participation mode, mitigat-
ules and comparing them against the full pipeline. Table 6              ing or aggravating circumstances, rather than explicit crim-
reports three evaluation metrics: G-F1 for general-provision            inal acts. These elements are often implicitly expressed in
prediction, S-F1 for specific-provision prediction, and SE              case narratives, making them harder to extract and align reli-
(M) for sentencing error measured in months. Disabling the              ably than act-centered specific statutes. Due to the inclusion
attorney module reduces general-provision accuracy and in-              of statute reverse verification, our framework adopts a con-
creases sentencing error, indicating that dual-agent adversar-          servative prediction strategy, favoring legally well-supported
ial extraction provides complementary perspectives beyond               statutes while filtering uncertain ones. This trade-off is inten-
a prosecution-only view. Disabling the formal reasoning                 tional and appropriate for high-stakes legal settings, where
module causes the most severe degradation, with sharp drops             avoiding incorrect statute application is more critical than ex-
in G-F1 and S-F1 and sentencing error, highlighting the ne-             haustively enumerating all potentially relevant provisions.
cessity of formal logical verification. Disabling the judge
rendering module increases sentencing error, suggesting its             Limitations. Despite its promising results, our framework
primary role in refining sentencing severity.                           still faces three main challenges. First, its formalization qual-
                                                                        ity is constrained by the accuracy of LLM outputs, so errors in
4.3   RQ3: Robustness Evaluation                                        identifying actors or conditions can propagate throughout the
To evaluate robustness under factual variations, we apply               reasoning pipeline. Second, our current evaluation is limited
controlled perturbations to case descriptions and examine               to statutory rules, leaving the extension to case law, open-
whether resulting changes in applicable statutes are correctly          textured norms, and evolving jurisprudence as future work.
captured. This evaluation focuses on general provisions,                Third, the system assumes deterministic rule parsing, which
which are more sensitive to some detailed factual changes               prevents it from fully capturing legal provisions that delib-
(e.g., age or mitigating circumstances). Robustness is quanti-          erately incorporate normative ambiguity. In addition, the
fied using Change Accuracy:                                             framework introduces moderate computational overhead due
                                                                        to its multi-stage LLM-based reasoning process. As sum-
 Change Accuracy = { s | s ∈ Spred ∧ s ∈ Strue } / Strue                marized in Table 8, on average, a single case requires mul-
                                         LeCaRDv2                                                          LEEC
    Model
                        w/o Golden Statute           w/ Golden Statute                w/o Golden Statute            w/ Golden Statute
                      RMSE↓       Valid (%)↑    RMSE↓        Valid (%)↑    RMSE↓        Valid (%)↑   SusF1 (%)↑    RMSE↓    Valid (%)↑
    LexiLaw            39.09        92.13        28.51            90.00       25.89       97.00             9.62   31.75       96.00
    DISC-LawLLM        52.45        83.00        37.14            90.00         –           –              13.87     –           –
    GPT o4-mini        33.20        92.00        28.03            94.00       34.94       91.00            78.68   38.46       96.00
    GPT-4o             32.84        94.00        22.68            95.00       41.66       95.60            80.25   50.41       95.50
    Claude 4 Sonnet    26.25        93.00        26.20            94.00       36.92       94.00            89.97   28.40       98.00
    DeepSeek v3        26.73        64.30        15.42            93.00       27.67       97.00            66.48   22.61       97.00
    GPT 5.2            14.54        94.20        13.87            94.00       28.48       95.20            97.80   23.90       95.00
    L4L (Ours)         12.72        94.60         9.98            96.20       23.04       97.20            98.80   20.95       96.77

                Table 5: Sentencing Error, Legal Validity, and Suspect-Level Performance with or without Golden Statutes


     Model Variant            G-F1 (%)      S-F1 (%)      SE (M)          [Gao et al., 2024] further show that careful construction of
                                                                          high-quality synthetic query–candidate pairs can markedly
     – Attorney                37.89         69.56        13.00
     – Formal Reasoning        25.29         61.01        20.87
                                                                          improve legal-case retrieval. Our work goes further by
     – Judge Rendering         39.08         78.99        11.88           compiling the extracted norms into executable formal
     Raw GPT-5.2               31.14         75.53         8.78           reasoning.
     L4L (Ours)                39.08         78.99        8.30            Multi-agent Judicial Simulation. Treating legal reasoning
                                                                          as collaboration among specialized agents has gained trac-
Table 6: Ablation study results with different components removed.        tion. AGENTS ON THE B ENCH simulates a collegial bench to
                                                                          improve judgment quality through deliberative voting [Jiang
            Model               Change Accuracy (%)                       and Yang, 2024], whereas AGENT C OURT evolves adversar-
                                                                          ial lawyer agents via long-horizon self-play, yielding measur-
            LexiLaw                                0.00                   able skill gains [Chen et al., 2024]. These systems, however,
            DISC-LawLLM                           23.17                   lack guarantees on logical soundness. We retain the agent
            GPT o4-mini                           46.33
                                                                          metaphor and further introduce a neural–symbolic pipeline
            GPT-4o                                50.67
            Claude 4 Sonnet                       51.50                   with legal rendering mechanism that integrates statutory in-
            DeepSeek v3                           55.93                   terpretation and retrieved precedents..
            GPT-5.2                               59.63                   Neural–Symbolic Methods. Early work such as Logic
            L4L (Ours)                            62.56                   Tensor Networks [Badreddine et al., 2022] embeds many-
                                                                          valued fuzzy logic into differentiable architectures, while
    Table 7: Robustness Evaluation on the Perturbation Dataset.           DeepProbLog [Manhaeve et al., 2018] integrates probabilis-
                                                                          tic logic programming with neural predicates. More recent
                                                                          studies add large-scale LLM components: NS-LCR learns ex-
tiple LLM calls and over one minute of end-to-end runtime.
                                                                          plicit law- and case-level rules for explainable case retrieval
Nevertheless, this cost is acceptable given the level of inter-           [Sun et al., 2024]; Logic-LM introduces structured prompting
pretability and formally verified reasoning achieved.
                                                                          plus theorem-prover feedback to enforce logical soundness
                                                                          [Sadowski and Chudziak, 2025a]; and Kant et al. combine
6    Related Work                                                         neuro-symbolic reasoning with contract analysis to improve
Domain-specific Legal                                                     coverage decisions [Kant et al., 2025]. These results show
LLMs. General-               Metric                  Average              that logic grounding enhances transparency and robustness,
purpose LLMs often           LLM calls per case         10.33             which we pursue by marrying an agent-driven statute predic-
mishandle legal ter-         Runtime (sec)             107.36             tor with a symbolic criminal-law reasoner to bridge substan-
minology and citation        Input tokens              13,049             tive and formal rationality.
style. C HAT L AW cou-       Output tokens              4,217
ples a knowledge-graph-      Cost per case (USD)       0.0819             7     Conclusion
enhanced     mixture-of-                                                  We presented L4L , a solver-centered framework for trust-
experts backbone with a     Table 8: Average cost/case of L4L .
                                                                          worthy legal AI that bridges substantive and formal ratio-
multi-agent pipeline that                                                 nality in LLM-based legal reasoning. L4L enables legally
mirrors law-firm SOPs, outperforming GPT-4 on LawBench                    grounded verdicts that are both interpretable and verifiable.
and national bar exams [Cui et al., 2023]. L AWYER GPT                    Experimental results demonstrate that integrating symbolic
shows that lightweight domain pre-training plus retrieval                 verification with LLM-based reasoning improves accuracy,
boosts statute-matching and consultation accuracy while                   robustness, and explainability over LLM systems.
remaining compute-efficient [Yao et al., 2024]. Gao et al.
References                                                       [Li et al., 2024] Haitao Li, Qingyao Ai, Qian Dong, and
[Badreddine et al., 2022] Samy Badreddine, Artur d’Avila            Yiqun Liu. Lexilaw: A scalable legal language model for
   Garcez, Luciano Serafini, and Michael Spranger. Logic            comprehensive legal understanding. https://github.com/
   tensor networks. Artificial Intelligence, 303:103649, 2022.      CSHaitao/LexiLaw, 2024.
[Chen et al., 2024] Guhong Chen, Liyang Fan, Zihan Gong,         [Linna and Linna, 2025] Eljas Linna and Tuula Linna. Ju-
   Nan Xie, Zixuan Li, Ziqiang Liu, Chengming Li, Qiang             dicial requirements for generative ai in legal reasoning.
   Qu, Shiwen Ni, and Min Yang. Agentcourt: Simulat-                arXiv preprint arXiv:2508.18880, 2025.
   ing court with adversarial evolvable lawyer agents. arXiv     [Manhaeve et al., 2018] Robin Manhaeve, Sebastijan Du-
   preprint arXiv:2408.08089, 2024.                                 mančić, Angelika Kimmig, Thomas Demeester, and Luc
[Cui et al., 2023] Jiaxi Cui, Zongjian Li, Yang Yan, Bohua          De Raedt. Deepproblog: Neural probabilistic logic pro-
   Chen, and Li Yuan. ChatLaw: Open-source legal large              gramming. In Advances in Neural Information Processing
   language model with integrated external knowledge bases.         Systems, volume 31, 2018.
   CoRR, abs/2306.16092, 2023.                                   [Prajescu and Confalonieri, 2025] Andrada Iulia Prajescu
[Foy III, 2010] H Miles Foy III. On judicial discretion in          and Roberto Confalonieri. Argumentation-based explain-
   statutory interpretation. Admin. L. Rev., 62:291, 2010.          ability for legal ai: Comparative and regulatory perspec-
[Gao et al., 2024] Cheng Gao, Chaojun Xiao, Zhenghao Liu,           tives. arXiv preprint arXiv:2510.11079, 2025.
   Huimin Chen, Zhiyuan Liu, and Maosong Sun. Enhanc-            [Richmond et al., 2024] Karen         McGregor     Richmond,
   ing legal case retrieval via scaling high-quality synthetic      Satya M Muddamsetty, Thomas Gammeltoft-Hansen,
   query–candidate pairs. In Proceedings of the 2024 Con-           Henrik Palmer Olsen, and Thomas B Moeslund. Explain-
   ference on Empirical Methods in Natural Language Pro-            able ai and law: An evidential survey. Digital Society,
   cessing, pages 7086–7100. Association for Computational          3(1):1, 2024.
   Linguistics, 2024.                                            [Sadowski and Chudziak, 2025a] Albert Sadowski and
[Hendrycks et al., 2021] Dan Hendrycks, Collin Burns,               Jarosław A. Chudziak. Explainable rule application via
   Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song,              structured prompting: A neural–symbolic approach. arXiv
   and Jacob Steinhardt. Measuring massive multitask lan-           preprint arXiv:2506.16335, 2025.
   guage understanding. In Proc. ICLR 2021, 2021.                [Sadowski and Chudziak, 2025b] Albert Sadowski and
[Ho et al., 2025] Justin Ho, Alexandra Colby, and William           Jaroslaw A Chudziak. On verifiable legal reasoning: A
   Fisher.       Incorporating legal structure in retrieval-        multi-agent framework with formalized knowledge repre-
   augmented generation: A case study on copyright fair use,        sentations. In Proceedings of the 34th ACM International
   2025.                                                            Conference on Information and Knowledge Management,
[Hou et al., 2024] Abe Bohan Hou, William Jurayj, Nils              pages 2535–2545, 2025.
   Holzenberger, Andrew Blair-Stanek, and Benjamin Van           [Savelka, 2023] Jaromir Savelka. Unlocking practical appli-
   Durme. Gaps or hallucinations? gazing into machine-              cations in the legal domain: Evaluation of GPT for zero-
   generated legal analysis for fine-grained text evaluations,      shot semantic annotation of legal texts. In Proc. ICAIL
   2024.                                                            2023, pages 447–451, 2023.
[Jiang and Yang, 2024] Cong Jiang and Xiaolei Yang.              [Shu et al., 2024] Dong Shu, Haoran Zhao, Xukun Liu,
   Agents on the bench: Large language model based multi            David Demeter, Mengnan Du, and Yongfeng Zhang.
   agent framework for trustworthy digital justice. arXiv           Lawllm: Law large language model for the us legal sys-
   preprint arXiv:2412.18697, 2024.                                 tem. In Proceedings of the 33rd ACM International
[Kant et al., 2025] Manuj Kant, Sareh Nabi, Manav Kant,             Conference on Information and Knowledge Management,
   Roland Scharrer, Megan Ma, and Marzieh Nabi. Towards             CIKM ’24, page 4882–4889. ACM, October 2024.
   robust legal reasoning: Harnessing logical llms in law.       [Sun et al., 2024] Zhongxiang Sun, Kepu Zhang, Weijie Yu,
   arXiv preprint arXiv:2502.17638, 2025.                           Haoyu Wang, and Jun Xu. Logic rules as explanations
[Katz et al., 2024] Daniel M. Katz, Michael J. Bommarito II,        for legal case retrieval (ns-lcr). In Proceedings of LREC-
   Shang Gao, and Pablo Arredondo. GPT-4 passes the bar             COLING 2024, 2024.
   exam. Philosophical Transactions of the Royal Society A,      [Xue et al., 2024] Zongyue Xue, Huanghai Liu, Yiran Hu,
   2024. First posted as SSRN 4389233, 2023.                        Yuliang Qian, Yajing Wang, Kangle Kong, Chenlu Wang,
[Kesari et al., 2024] Aniket Kesari, Daniela Sele, Elliott          Yun Liu, and Weixing Shen. Leec for judicial fairness:
   Ash, and Stefan Bechtold. A legal framework for explain-         A legal element extraction dataset with extensive extra-
   able artificial intelligence. Center for Law & Economics         legal labels. In Proceedings of the Thirty-Third Interna-
   Working Paper Series, 9, 2024.                                   tional Joint Conference on Artificial Intelligence, IJCAI-
[Li et al., 2023] Haitao Li, Yunqiu Shao, Yueyue Wu,                24, pages 7527–7535, 2024.
   Qingyao Ai, Yixiao Ma, and Yiqun Liu. Lecardv2: A             [Yao et al., 2024] Shunyu Yao, Qingqing Ke, Qiwei Wang,
   large-scale chinese legal case retrieval dataset. arXiv          Kangtong Li, and Jie Hu. Lawyer gpt: A legal large
   preprint arXiv:2310.17609, 2023.                                 language model with enhanced domain knowledge and
  reasoning capabilities. In Proceedings of the 3rd Inter-
  national Symposium on Robotics, Artificial Intelligence
  and Information Engineering (RAIIE ’24), pages 108–112.
  ACM, 2024.
[Yue et al., 2023] Shengbin Yue, Wei Chen, Siyuan Wang,
  Bingxuan Li, Chenchen Shen, Shujun Liu, Yuxuan Zhou,
  Yao Xiao, Song Yun, Xuanjing Huang, and Zhongyu Wei.
  Disc-lawllm: Fine-tuning large language models for in-
  telligent legal services. arXiv preprint arXiv:2309.11325,
  2023.
