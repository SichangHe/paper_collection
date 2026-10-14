                                            VERGE: Formal Refinement and Guidance Engine for Verifiable LLM
                                                                     Reasoning

                                                  Vikash Singh1 * Darion Cassel2 , Nathaniel Weir2 , Nick Feng2 , Sam Bayless2
                                                               1
                                                                   Case Western Reserve University 2 Amazon Web Services



                                                               Abstract                                                     Input Context: "All cats are mammals.
                                                                                                                            Felix is a cat."
                                             Despite the syntactic fluency of Large Lan-                                    Query: "Is Felix a mammal and does he
arXiv:2601.20055v2 [cs.CL] 2 May 2026




                                                                                                                   User     bark?"
                                             guage Models (LLMs), ensuring their logical
                                             correctness in high-stakes domains remains
                                                                                                                            LLM Draft Answer:
                                             a fundamental challenge. We present a neu-
                                                                                                                  Æ         "Yes, Felix is a mammal. Felix also



                                                                                                    ITERATION 1
                                             rosymbolic framework that combines LLMs                              Agent
                                                                                                                            barks."
                                             with SMT solvers to produce verification-
                                             guided answers through iterative refinement.                                   Z3 Verification Failed:
                                             Our approach decomposes LLM outputs into                                       q Claim: (Barks Felix) → Unsat
                                                                                                                  «         Reason: No axioms support ’Barks’.
                                             atomic claims, autoformalizes them into first-                                 Action: Trigger refinement.




                                                                                                                                                                     Feedback Loop
                                                                                                                  Solver
                                             order logic, and verifies their logical consis-
                                             tency using automated theorem proving. We
                                             introduce three key innovations: (1) multi-
                                                                                                                            LLM Refined Answer:
                                             sample consensus via formal semantic equiva-                                   "Felix is a mammal (derived from ’Cats
                                                                                                                  Æ
                                                                                                    ITERATION 2




                                             lence checking to ensure logic-level alignment                                 are Mammals’). However, we cannot
                                                                                                                  Refiner   conclude that Felix barks."
                                             between candidates, eliminating the syntactic
                                             bias of surface-form metrics, (2) semantic rout-
                                                                                                                            Z3 Formalization:
                                             ing that directs different claim types to appro-                               (assert (Mammal Felix))   Entailed
                                             priate verification strategies: symbolic solvers                     «         (assert (not (Barks Felix)))
                                                                                                                  Solver       Consistent
                                             for logical claims and LLM ensembles for com-
                                             monsense reasoning, and (3) precise logical
                                             error localization via Minimal Correction Sub-                                 ¥ Verified Output:
                                                                                                                            "Felix is a mammal. Unknown if he
                                             sets (MCS), which pinpoint the exact subset                                    barks."
                                             of claims to revise, transforming binary failure                               S(A): 1.0

                                             signals into actionable feedback. Our frame-
                                             work classifies claims by their logical status and
                                                                                                   Figure 1: VERGE correcting LLM Hallucinations
                                             aggregates multiple verification signals into a
                                                                                                   via Formal Verification. The solver detects an unsup-
                                             unified score with variance-based penalty. The
                                                                                                   ported claim and guides the LLM to a consistent answer
                                             system iteratively refines answers using struc-
                                                                                                   through MCS-based feedback.
                                             tured feedback until acceptance criteria are met
                                             or convergence is achieved. This hybrid ap-
                                             proach delivers formal guarantees where pos-
                                             sible and consensus verification elsewhere, ad-       (Lewkowycz et al., 2022; Hendrycks et al., 2021)
                                             vancing trustworthy AI. With the GPT-OSS-             to code generation (Chen et al., 2021; Austin et al.,
                                             120B model, VERGE demonstrates an average             2021) and logical inference (Tafjord et al., 2021).
                                             performance uplift of 18.7% at convergence
                                                                                                   Despite these advances, ensuring the correctness
                                             across a set of reasoning benchmarks compared
                                             to single-pass approaches.
                                                                                                   of LLM-generated answers remains a critical bar-
                                                                                                   rier in high-stakes domains such as legal policy
                                        1    Introduction                                          compliances, healthcare and finance etc. While
                                                                                                   recent models achieve impressive benchmark per-
                                        Large Language Models (LLMs) have demon-                   formance (OpenAI, 2025; Anthropic, 2025), they
                                        strated remarkable capabilities across diverse rea-        rely on statistical likelihood maximization (Ouyang
                                        soning tasks, from mathematical problem-solving            et al., 2022) rather than logical deduction. Con-
                                            * Work done during internship at Amazon Web Services   sequently, they operate without mechanisms for
provable correctness, making them prone to hallu-         guarantees for a verifiable subset of claims while
cinations and internal contradictions.                    maintaining the system’s ability to handle broad,
   Current verification strategies such as self-          real-world reasoning tasks.
consistency (Wang et al., 2022), process supervi-             Our work introduces:
sion (Lightman et al., 2023), and self-refinement         1. High-Fidelity Consensus via SMT: We bridge
(Madaan et al., 2023; Shinn et al., 2023) provide            the semantic gap by enforcing semantic equiva-
heuristic rather than formal guarantees. Even multi-         lence (ϕa ⇐⇒ ϕb ) among candidate formaliza-
agent debate frameworks (Du et al., 2023; Liang              tions. Unlike syntactic metrics (e.g., BLEU, Jac-
et al., 2023) merely achieve consensus, which does           card) which fail on variable renaming or struc-
not imply correctness. To achieve verifiable reason-         tural permutation, we utilize the solver to prove
ing, neuro-symbolic methods (Singh et al., 2026;             that different candidate formulas yield identical
Ganguly et al., 2025, 2024; Feng et al., 2025; Pan           truth tables, ensuring robust consensus.
et al., 2023; Callewaert et al., 2025; Olausson et al.,   2. Actionable Feedback via MCS: We adapt
2023; Garcez et al., 2019; Mao et al., 2019) and se-         greedy MCS computation (Marques-Silva et al.,
mantic parsing (Wang et al., 2026; McGinness and             2013b; Morgado et al., 2013; Bacchus and Kat-
Baumgartner, 2024; Zettlemoyer and Collins, 2005;            sirelos, 2016) to provide polynomial-time, spe-
Dong and Lapata, 2016; Zhang et al., 2025) have              cific feedback (e.g., "claim C2 does not hold")
attempted to bridge natural language with formal             rather than generic error signals.
logic. However, these approaches face a fundamen-         3. Flexible Neuro-symbolic Integration: A se-
tal semantic gap: natural language is inherently             mantic routing framework that balances the pre-
ambiguous, and rigid formalization often fails on            cision of SMT solvers with the flexibility of
open-domain claims (Church, 1936; Turing, 1936).             LLMs, avoiding the pitfalls of forcing undecid-
   We present VERGE, a framework that miti-                  able language into decidable theories.
gates this gap by combining LLMs with Satisfiabil-
ity Modulo Theories (SMT) solvers (Barrett et al.,
2009; De Moura and Bjørner, 2008) to produce              2    Related Work
verification-guided answers with formal guaran-
tees for logical/mathematical claims through itera-       Probabilistic vs. Formal Verification. Standard
tive refinement, as illustrated in Figure 1. Unlike       LLM reasoning strategies rely on probabilistic con-
standard feedback loops, VERGE leverages the              fidence. Methods like self-consistency (Wang et al.,
SMT solver’s ability to extract unsatisfied asser-        2022) and process supervision (Ganguly et al.,
tions (Zhang and Malik, 2003; Nadel et al., 2013).        2026; Chen et al., 2025; Lightman et al., 2023;
This allows us to compute Minimal Correction              Uesato et al., 2022; Yang et al., 2026) aggregate
Subsets (MCS) (Marques-Silva et al., 2013a,b),            samples or train verifiers on human labels, but can-
identifying a minimal set of modifications to the         not guarantee logical soundness. Self-refinement
atomic claims sufficient to restore consistency and       approaches (Madaan et al., 2023; Shinn et al., 2023;
move from probabilistic self-correction to provable       Welleck et al., 2022) use the model to critique it-
self-consistency correction.                              self, often failing due to the faithfulness gap where
                                                          reasoning does not match output (Lyu et al., 2023;
The Expressivity Trade-off and Pragmatic Ver-             Huang et al., 2023). Multi-agent debate (Du et al.,
ification. A key insight of our work is that en-          2023; Liang et al., 2023) achieves consensus, not
forcing formal verification on all claims is funda-       truth, recent work shows self-correction can even
mentally misaligned with the ambiguity of natural         degrade performance (Huang et al., 2023; Kamoi
language. Rather than attempting to bridge this           et al., 2024). In contrast, VERGE uses SMT
gap universally, a theoretically intractable goal, we     solvers (Barrett et al., 2009; De Moura and Bjørner,
adopt a pragmatic stance: Apply formal verifi-            2008) to provide mathematically proven feedback.
cation where the semantic gap is narrow (mathe-           Unlike tool-augmented LLMs (Schick et al., 2023;
matical/logical claims), and fall back to consensus-      Gou et al., 2024) that use tools for execution (e.g.,
based verification where it is wide (commonsense/-        calculators), we use tools for consistency checking,
vague claims). VERGE introduces a verification            computing MCS. (Zhang and Malik, 2003; Nadel
cascade with semantic routing to implement this           et al., 2013) to identify exactly which premises
strategy. This hybrid approach provides formal            contradict the generated answer.
Neuro-Symbolic Integration and the Semantic               two constraints for each claim ci : (1) Consis-
Gap. Traditional semantic parsing (Zafar et al.,          tency: SAT(φC ∧ φci ) = true, and (2) Entailment:
2026; Dong and Lapata, 2016; Berant et al., 2013;         SAT(φC ∧ ¬φci ) = false, where φ denotes the log-
Zettlemoyer and Collins, 2005) maps language to           ical formalization function that maps natural lan-
executable logical forms but requires expensive su-       guage statements to SMT constraints. The consis-
pervision. Recent work extends this to theorem            tency constraint verifies that each claim is compati-
proving (Polu and Sutskever, 2020; Polu et al.,           ble with the context, while the entailment constraint
2022; Jiang et al., 2022; Azerbayev et al., 2023)         ensures that each claim is a logical consequence
and augmenting LLMs with symbolic solvers (Pan            of the context. These constraints provide formal
et al., 2023; Olausson et al., 2023; Callewaert et al.,   equivalence guarantees where logic permits, while
2025), but these require fully formalizable domains.      falling back to semantic consistency (soft verifica-
Prior neuro-symbolic integration (Mao et al., 2019;       tion, see §3.4) otherwise. Pipeline. The pipeline
Garcez et al., 2019; Kautz, 2022) and grammar-            (Fig. 2) executes iteratively: (1) entity extraction,
based approaches (Ganguly et al., 2024) struggle          (2) generation, (3) decomposition, (4) formaliza-
with the semantic gap (Church, 1936; Turing, 1936)        tion & verification, and (5) refinement.
the mismatch between ambiguous natural language
and rigid formal systems. VERGE targets open-             3.1   Entity Extraction and Generation
domain natural language where full formalization          We first extract entities E = Extract(C, q) (e.g.,
is often impossible. We introduce semantic rout-          ‘Felix’, ‘Monday’, ‘Process A’) to serve as typed
ing, rather than forcing vague or commonsense             constants in SMT. At iteration t, we generate an-
claims into rigid first-order logic, we route them        swer A(t) via a language model M :
to a consensus-based soft verifier. This treats the
semantic gap as an inherent property of language                   A(t) = M (C, q, A(t−1) , F (t−1) )                    (1)
requiring hybrid verification.                            where F (t−1) is structured feedback (see §3.5).
Automated Reasoning for Repair. Our feed-                 The initial iteration (t = 1) utilizes zero-shot
back mechanism adapts MCS computation                     prompting (e.g., A0 = M (C, q, ∅, ∅)).
(Marques-Silva et al., 2013b; Liffiton and Sakallah,      3.2   Claim Decomposition and Classification
2008) from constraint programming to NLP. MCS
identifies the minimal set of constraints to delete       We decompose A into atomic claims {c1 , . . . , cn }.
to restore satisfiability. Recent work applies MCS        To ensure our system is honest about what it can
to constraint relaxation (Bacchus and Katsirelos,         and cannot formally prove, we classify each claim
2016) and automated debugging (Morgado et al.,            ci into a semantic type τi ∈ T via M :
2013). We innovate by translating MCS output into               τi = arg             max                  PM (τ | ci )   (2)
natural language feedback, guiding the LLM to                              τ ∈{τM ,τL ,τT ,τP ,τC ,τV }
rewrite specific atomic claims. This prioritizes in-
                                                          where types correspond to Mathematical, Logical,
terpretability and convergence speed (O(m × SAT)
                                                          Temporal, Probabilistic, Commonsense, and Vague
greedy approximation) over theoretical optimality.
                                                          claims. These categories align with standard dis-
To our knowledge, VERGE is the first to apply
                                                          tinctions in semantic parsing to differentiate veri-
MCS-based feedback to guide iterative refinement
                                                          fiable facts from subjective or probabilistic state-
in LLM reasoning, converting abstract unsat cores
                                                          ments. This classification is crucial for minimizing
into actionable guidance (see Appendix B).
                                                          "false formalization", the error of forcing ambigu-
3   Methodology                                           ous natural language into rigid logic. Vague claims
                                                          are identified by the model as containing subjec-
Problem Formulation. Given a context C =                  tive predicates (e.g., "likely", "possibly") that lack
{p1 , . . . , pm } of premise statements and a query      binary truth values, preventing brittle SMT asser-
q, we aim to produce a verified answer A∗ com-            tions.
posed of atomic claims {c1 , . . . , cn } with maximal
verification coverage. Here, A∗ is a refined ver-         3.3   SMT Formalization with Consensus
sion of the candidate answer A obtained through           For claims classified as logical or mathematical,
verification. We formalize this as maximizing             we target the QF_UF (Quantifier-Free Uninter-
the verification score S(A) ∈ [0, 1] subject to           preted Functions) and QF_LIA (Quantifier-Free
        VERGE
                               Generation             Formalization                         Verification                     Decision
                                                                            SOFT / VAGUE                             Calc.
                                   Init t = 1            Route?                              Select Vτi
                                                                                                                     S(A)




                                                                                                  MATH
            Setup




                                                             YES




                                                                                                           VAGUE
                                                                       NO
             Input
                              NO
                                    t = 1?      YES
                                                        Classify τi                          SMT (σ)               S ≥ θacc ?     YES




                                                                                    AMBIG
             (C, q)




                                                             FORMAL
                                                                                                                                  Return A∗




                                                                             YES




                                                                                                                        NO
                           Refine                       Form. φci                             Soft (ν)
                                          Gen. A(1)                                                                ∆S < ϵ?        YES



           Extract E        A(t)




                                                                                                                        NO
                                    Extract                                                   Hybrid
                                                       Consensus?                                                  Gen. F (t)
           Form. φC                  {ci }




                                                             NO
                                                          Self-                              Joint SAT
                                                         Correct




Figure 2: Overview of VERGE: The pipeline is structured into five distinct stages: Setup prepares the context C
and entities E; Generation produces and refines answers A(t) iteratively; Formalization classifies claim types τi and
generates SMT formulas φci ; Verification routes claims to SMT, Soft, or Hybrid verifiers based on semantic type;
and Decision computes the aggregate score S(A) to either accept the answer A∗ or generate feedback F (t) for the
next iteration.


Linear Integer Arithmetic) fragments within the                       semantic equivalence clique is ≥ ⌈K/2⌉). Ad-
SMT-LIB2 standard. Given the context C and query                      ditionally, we employ Round-Trip Translation
q, we first extract entities E as a set of typed con-                 (SMT → Natural Language) as a semantic sanity
stants. For example, from the statement “All hu-                      check to ensure alignment with the source text. If
mans above age 18 are adults”, we extract entities                    consensus fails or the confidence (derived from
age of type Z and adult of type AGE_GROUP,                            clique size and round-trip similarity) is low, we
which are declared as uninterpreted constants of                      trigger a self-correction step φnew = M (φ, . . . ),
the corresponding sorts. We then use generate can-                    constrained such that φnew |= φ. This ensures the
didate formulas ϕ = M (ci , E) for each claim ci                      system strictly strengthens (and never weakens) the
over the vocabulary in E. To mitigate the stochastic                  constraints during refinement. The strengthening
nature of autoformalization, we generate K = 3                        constraint is verified by checking the unsatisfiabil-
candidate formulas {ϕ1 , . . . , ϕK } and check for                   ity of φnew ∧ ¬φ. To ensure decidability, we per-
consensus. Instead of relying on brittle syntactic                    form this check over the finite domain of entities E
overlap, we compute consensus based on seman-                         extracted in the setup phase, effectively reducing
tic equivalence (see Appendix C.2 for the formal                      the check to propositional logic or quantifier-free
definition). Two formulas ϕa and ϕb are deemed                        first-order logic(QF-FOL).
equivalent if and only if their bidirectional entail-
ment is valid, which we verify by querying the                        3.4          Verification Cascade
SMT solver:                                                           We employ a hybrid strategy that routes claims to
                                                                      the most rigorous verifier available for their type,
                                                                      prioritizing formal guarantees where applicable.
Equiv(ϕa , ϕb ) ⇐⇒ UNSAT (ΣE ∧ ¬(ϕa ↔ ϕb ))                           Semantic Routing (Flexibility Mechanism).
                                                (3)                   We define a routing function Vτi :
where ΣE represents the declarations of constants                             
and uninterpreted functions derived from the entity                           SMT-Verify if τi ∈ {τM , τL , τT }
                                                                              
extraction phase. This procedure constructs a se-                       Vτi = Soft-Verify if τi ∈ {τC , τV , τP } (4)
mantic equivalence graph where edges represent                                
                                                                                 Hybrid        else (or SMT error)
                                                                              
proven logical identity.
  A formalization is accepted only if a majority                      While SMT provides provable correctness, it can-
consensus is reached (i.e., the size of the largest                   not natively handle vague predicates (e.g., ‘is simi-
lar to’) without excessive and fragile axioms. By          3.5   Score Aggregation
routing these to Soft-Verify, VERGE preserves              We compute an aggregated verification score for
logical rigor where possible while preventing the          the entire answer by combining verification re-
system from falsely treating probabilistic or am-          sults from both soft and hard verification across
biguous reasoning as logical certainty.                    all atomic claims. Let A be an answer to query q
SMT-Based Verification. For logic-amenable                 given context C. Suppose A is decomposed into
claims, we check satisfiability using the Z3 solver.       atomic claims c1 , . . . , cn and verified against q and
We assign statuses based on rigorous logical tests:        C to produce verification results σ1 , . . . , σn , respec-
   • Contradictory (σC ): SAT(φC ∧φci ) = False.           tively. The verification score S(σi ) for each result
     The claim violates the context.                       is defined as:
                                                                       
   • Entailed (σE ): SAT(φC ∧ ¬φci ) = False.                          
                                                                         1.0 if Entailed(σi )
     The claim is proven true (proof by contradic-
                                                                       
                                                                       
                                                                       0.9 if Supported(σ )
                                                                                                    i
     tion).                                                   S(σi ) =
                                                                         0.7 if Possible(σi )
   • Possible (σP ): Consistent (SAT(φC ∧ φci ) =
                                                                       
                                                                       
                                                                       
                                                                       0.0 if Contradictory(σ ) or else
                                                                                                         i
     True) but not entailed. The context allows the
                                                                                                                   (5)
     claim but does not force it.
                                                              These weights reflect verification rigor: formally
    • Unknown (σU ): Solver timeout or execution           entailed claims receive the maximum score (1.0),
      error.                                               while soft-verified supported claims receive 0.9, en-
Minimal Correction Sets (MCS). For contradic-              suring the system favors provable logic over seman-
tions (σC ), we compute the MCS to generate pre-           tic consistency. The final aggregated score S(A)
cise feedback. Let φci be a set of clauses, the subset     integrates a variance-based penalty (Eq. 6) to dis-
S ⊂ of φci is a minimal correction set (MCS) if            courage “gaming” the system, where a model might
    • SAT(φC ∧ φci \ S) = true                             generate claims that are individually confident but
    • ∀S ′ ⊂ S, SAT(φC ∧ φci \ S ′ ) = false               mutually contradictory under joint verification:
   Intuitively, MCS is small subset of clauses to                                                            
remove to restore satisfibility. This provides ac-                                                    σS
                                                               S(A) = S̄ · max 0.5, 1.0 −                          (6)
tionable guidance to address contradictions (e.g.,                                               S̄ + 0.01
"remove constraint X") rather than generic error
messages. See Appendix B for details about MCS             where S̄ is the mean of the verification scores
computation.                                               {S(σ1 ), . . . , S(σn )} and σS is their standard de-
                                                           viation.
Soft Verification. For claims unsuitable
for SMT, we use an ensemble of LLM                         Iterative Refinement. At each iteration t, we
judges. We compute a confidence weighted                   generate feedback F (t) containing: (1) Unsat
majority vote (using self-reported confi-                  Cores & MCS for contradictions, pinpointing ex-
dence of the judge) by defining verdicts v ∈               act logical conflicts; (2) Joint Conflicts for mutu-
{Supported, Plausible, Unsupported, Uncertain}.            ally incompatible claims; and (3) Formalization
   Constraint: To penalize the lack of formal guar-        Alerts for low-confidence mappings. The process
antees, soft-verified claims are capped at a lower         repeats until S(A) ≥ 0.75 and JointSAT=True
maximum score contribution than SMT-verified               (where JointSAT is the boolean result of the joint
claims (see §3.5).                                         satisfiability check), or until convergence (∆S <
                                                           0.01). For Joint Consistency, soft-verified claims
Hybrid Verification. The Hybrid strategy acts as           are treated as atomic boolean variables (bi ) within
a robustness fallback. Claims routed to SMT that           the SMT solver. To capture interactions between
fail due to non-logical errors (e.g., syntax errors, un-   soft and hard claims, the context formalization
declared variables, or timeouts) are automatically         φC includes bridging axioms generated by the
re-routed to Soft Verification. This prevents the          LLM (e.g., assertions linking vague predicates like
pipeline from stalling on "Unknown" (σU ) statuses         “small” to numerical bounds). This allows the
due to correctable formalization issues, allowing          solver to detect if a mathematically proven claim
the system to degrade gracefully from formal proof         (τM ) contradicts a commonsense claim (τC ) (e.g.,
to probabilistic consensus.                                Mathematical Claim “X > 10” vs Commonsense
Claim “X is a small single-digit number” which            By iteratively refining the context based on solver
implies X < 10), ensuring holistic consistency            feedback (Unsat Cores) rather than discarding the
even without full formalization of the common-            entire proof, VERGE successfully salvages logical
sense component. If claims are not jointly con-           entailments that probabilistic baselines miss (see
sistent, we compute the MCS over the claims as            Appendix F).
refinement feedback, signaling a minimal patch to            A notable outlier is the ProofWriter dataset,
restore joint consistency. Algorithm 1 (Appendix)         where Proof of Thought (PoT) retains dominance
details the complete refinement procedure.                (98.4% vs. 89.9%). This performance gap high-
                                                          lights a fundamental methodological distinction
4   Results                                               between monolithic execution and modular veri-
Benchmarking Neuro-Symbolic Reasoning.                    fication. PoT approaches reasoning as program
Table 1 presents a systematic evaluation of               synthesis, converting the full context into a sin-
VERGE against state-of-the-art inference-time             gle executable artifact to derive the answer in one
compute (prompting) strategies.          To ensure        pass. This is ideal for the rigid, deductive structure
comparable computational budgets, we configure            of synthetic datasets like ProofWriter. In contrast,
Self-Consistency (SC) with k = 3 samples and              VERGE treats reasoning as a semantic entailment
Self-Refinement (SR) with n = 3 iterations                task, employing a routing mechanism to decom-
with self-critique. Results for established neuro-        pose and verifying individual atomic claims. On
symbolic baselines (Proof of Thought, LINC,               purely synthetic tasks, this general-purpose ma-
Logic-LM) were computed using their officially            chinery specifically the overhead of claim decom-
released codebase.                                        position and semantic routing, introduces unneces-
   Consistent with these parameters, VERGE op-            sary complexity compared to PoT’s direct solver
erates with a maximum budget of Tmax = 3 itera-           execution. However, it is precisely this modular
tions. This setting balances accuracy with compu-         flexibility that allows VERGE to generalize to se-
tational cost, whereas baselines like CoT represent       mantically complex domains like Law (AR-LSAT),
single-pass performance (for convergence analysis         where a monolithic translation to executable logic
up to Tmax = 10, see Figure 3). Consequently, the         often fails due to linguistic ambiguity.
improvements shown represent the specific value of        4.1   Compute Parity and Search Baselines
iterative verification-guided refinement. To distin-
guish these gains from those achieved by iteration        Table 2 in the appendix reports the per-problem cost
alone, we refer to our ablation study (Table 3). By       on GPT-OSS-120B.VERGE at T =1 uses fewer
comparing the full system against the “w/o MCS”           tokens than SR yet beats it on every benchmark,
and “w/o Routing” variants (both of which also            isolating verification from refinement. SC at k=10
operate iteratively), we isolate the substantial per-     matches VERGE’s T =3 token budget but trails
formance contributions of VERGE’s verification            by 46.6 pts on FOLIO, 1.9 on AR-LSAT, 15.2
and feedback mechanisms.                                  on HLE. ToT-BFS (b=5, k=3, T =2) on GPT-OSS-
                                                          20B reaches 64.7 (FOLIO) and 55.9 (AR-LSAT)
General Performance Trends and Robustness.                versus VERGE’s 88.5 and 90.1, at 4× the tokens
As evidenced in Table 1, VERGE consistently out-          and 2× the calls; search and verification are com-
performs standard prompting and existing neuro-           posable, not competitive.
symbolic baselines on 5 out of the 6 evaluated
benchmarks. The method demonstrates robust scal-          4.2   Ablation study: The Role of MCS,
ing across model sizes, notably on the Humanities               Routing, and Feedback systems
Last Exam (HLE), where it improves GPT-OSS-               Impact of Architectural Components. Table 3
120B performance from 14.2% (CoT) to 30.5%.               isolates the contributions of VERGE’s key com-
This contrasts with traditional neuro-symbolic base-      ponents using GPT-OSS-120B. The full pipeline
lines (DSB, LogicLM), which suffer from a “trans-         consistently outperforms all ablated variants, con-
lation bottleneck”, where invalid SMT specifica-          firming that both Minimal Correction Sets (MCS)
tions cause the solver to fail silently or reject valid   and Semantic Routing are integral to maximizing
reasoning. VERGE overcomes this via its Verifi-           VERGE’s performance. We observe that MCS
cation Cascade, which utilizes Minimal Correction         is particularly critical for strict constraint satisfac-
Sets (MCS) to isolate specific formalization errors.      tion tasks. On AR-LSAT, removing MCS causes
                                  Prompting      Neuro-Symbolic Baselines       VERGE (Ours)
        Dataset       Model     CoT SC     SR DSB LogicLM LINC PoT w/o MCS w/o Rt              Full
                      GPT-20B 40.4 52.2 34.0 53.7       29.9    18.6 48.8     73.9     86.7   89.2±1.1
        FOLIO         GPT-120B 32.0 35.5 42.9 14.0      27.5    47.5 54.2     80.7     81.6   84.7±0.9
                      Sonnet-3.7 70.4 72.4 62.1 44.5    71.6    65.2 58.1     86.7     83.0   87.9±0.7
                    GPT-20B 74.6 71.4 56.8 38.8         35.8    42.8 94.0     82.7     85.8   85.2±1.3
        ProofWriter GPT-120B 52.4 65.6 67.2 31.4        32.0    76.4 98.4     88.7     84.6   89.9±0.8
                    Sonnet-3.7 71.6 86.6 74.0 42.8      64.7    71.1 98.2     90.2     88.0   93.0±0.5
                   GPT-20B 67.6 72.2 46.2 44.8            -       -     -     80.9     83.6   87.3±1.0
        ZebraLogic GPT-120B 84.0 77.8 72.2 28.2           -       -     -     88.9     90.9   91.0±0.6
                   Sonnet-3.7 52.0 51.0 58.8 48.0         -       -     -     58.0     62.8   64.8±1.4
                      GPT-20B 81.7 89.1 63.9 59.6       21.7      -     -     82.6     86.8   89.5±0.8
        AR-LSAT       GPT-120B 87.8 88.7 84.8 32.2      19.9      -     -     83.0     87.4   91.7±0.5
                      Sonnet-3.7 61.7 58.7 73.5 67.8    31.2      -     -     88.2     87.7   88.6±0.9
                      GPT-20B 34.4 38.4 28.0 10.0         -       -     -     42.2     43.7   49.9±1.5
        BBEH          GPT-120B 38.4 41.8 37.4 20.2        -       -     -     54.1     50.2   58.9±1.2
                      Sonnet-3.7 33.0 29.4 37.8 24.0      -       -     -     40.4     43.5   45.9±1.4
                      GPT-20B 9.6 15.0 8.6 1.4            -       -     -     12.2     13.7   19.9±1.1
        HLE           GPT-120B 14.2 14.0 12.8 6.4         -       -     -     21.0     15.2   30.5±1.6
                      Sonnet-3.7 5.8 5.0 6.8 0.6          -       -     -     16.7     14.7   17.2±0.9

Table 1: Comprehensive Performance Analysis. Results are averaged over 5 independent runs, with error bars
(subscript) indicating standard deviation. We compare VERGE against standard prompting (CoT, SC, SR) and
neuro-symbolic baselines (DSB, LogicLM, LINC, PoT) across three different backbone models: GPT-OSS-20B,
GPT-OSS-120B, and Claude 3.7 Sonnet. VERGE consistently outperforms baselines across diverse domains and
model sizes, except on ProofWriter where the specialized PoT method remains dominant. “ − ” indicates that the
baseline does not support the dataset.


       Method         LLM Solver Tokens Wall            mechanism, thereby forcing all claims into formal
                      calls calls (I+O) (s)             logic, substantially impacts HLE and BBEH, with
       CoT (1-pass)      1      0 2.1K 3.2              HLE scores halving from 30.5% to 15.2%. This
       SC (k=3)          3      0 6.3K 8.7
       SC (k=10)        10      0 21.0K 28.3
                                                        lends support to the “Formalization Barrier” hy-
       SR (n=3)          6      0 11.4K 15.3            pothesis (discussed in §4.4): attempting to for-
       PoT               2      1 4.8K 5.4              malize vague or fuzzy predicates leads to brittle
       LINC              3      1 5.1K 6.1
       ToT-BFS          40      0 63.0K 71.2            systems that reject valid reasoning (e.g., a solver
                                                        might reject a valid commonsense claim due to a
       VERGE (T =1) ∼8         ∼5 8.4K 11.8
       VERGE (T =3) ∼17       ∼15 18.2K 32.6            missing axiom). Routing allows VERGE to fall-
                                                        back to soft verification when necessary, a benefit
Table 2: Per-problem cost on GPT-OSS-120B, aver-        most pronounced in domains with high ambiguity
aged across six benchmarks. Solver calls are CPU-only   like HLE.
(<200ms each). VERGE at T =1 is cheaper than SR
yet outperforms it; SC at k=10 matches VERGE’s to-      Feedback Granularity. The right side of Table 3
ken budget but not its accuracy.                        demonstrates the value of high-resolution feedback.
                                                        There is a clear hierarchy of performance correlated
                                                        with feedback specificity. Unsat-Core Only feed-
a sharp drop from 91.7% to 83.0%. This indicates        back, which identifies conflicting constraints but
that while the solver can detect contradictions, the    does not prescribe a fix, lags behind the full model
model struggles to resolve complex scheduling con-      by 10.9% on average. Minimal Solver Feedback
flicts without the precise, minimal deletion guid-      (MSF) performs worst, with a 15.3% average drop.
ance provided by the MCS. Conversely, Semantic          This confirms that simply telling an LLM “you
Routing proves advantageous for open-ended and          are wrong (UNSAT)” (binary feedback) is insuf-
commonsense reasoning. Removing the routing             ficient for complex reasoning; the model requires
                                    Architectural Components          Feedback Granularity
                 Dataset     Full w/o MCS w/o Routing Soft-Only Unsat-Core Only MSF
                 FOLIO       84.7    80.7        81.6        80.8           79.3         76.5
                 ProofWriter 89.9    88.7        84.6        75.8           82.4         80.1
                 ZebraLogic 91.0     88.9        90.9        70.2           85.3         72.5
                 AR-LSAT 91.7        83.0        87.4        84.6           89.4         89.2
                 BBEH        58.9    54.1        50.2        41.7           42.7         40.1
                 HLE         30.5    21.0        15.2        13.2           23.2         19.8
                 Avg. Drop     –     -6.8%      -8.3%       -22.8%        -10.9%       -15.3%

Table 3: Ablation Study on Component Contributions (GPT-OSS-120B). We isolate the impact of Minimal
Correction Subsets (MCS), Semantic Routing (Rt), and the SMT Solver itself. Full represents the complete VERGE
pipeline. w/o Routing forces SMT verification for all claims. Soft-Only removes the SMT solver entirely, relying
solely on LLM consensus. Unsat-Core-Only and MSF vary the granularity of the feedback.


the actionable, structural guidance that VERGE            ing point. Varying the Supported weight wS on
provides.                                                 GPT-OSS-120B (Table 4) yields worst-case −1.3%
    To address the converse hypothesis whether for-       and mean |∆|<0.6%; collapsing wS =1.0 slightly
mal verification is necessary at all we evaluated         hurts, confirming the discount appropriately favors
a Soft-Only variant where all claims are routed           entailment over consensus.
to the LLM consensus mechanism, bypassing the
SMT solver entirely. As shown in Table 3, this            4.3   Efficiency and Convergence
results in the most significant performance degra-        Fig. 3 (in Appendix) reveals a striking diver-
dation across the board (average drop: -22.8%).           gence in refinement dynamics. VERGE achieves
The impact is most severe on strict constraint sat-       monotonic improvement across all six datasets
isfaction tasks like ZebraLogic (91.0% → 70.2%)           (Kendall’s τ = 1.0, p < 0.001), with average
and ProofWriter (89.9% → 75.8%), confirming               convergence at iteration 6.2 (σ = 1.3), beyond
that while soft verification is useful for ambiguity,     T=10 (Table 13) , the gains in performance are neg-
it lacks the precision required to resolve complex        ligible (< 0.3% across all benchmarks), validating
logical dependencies. This effectively validates          our convergence criterion (∆S < ϵ = 0.01). In
the necessity of the hybrid approach: VERGE re-           contrast, probabilistic self-refinement exhibits what
quires SMT for precision and Semantic Routing             we term the correlation cliff phenomenon: perfor-
for flexibility.                                          mance systematically degrades in 85.2% of trials
                                                          (χ2 = 26.7, p < 0.001), characterized by a strong
Semantic Router Reliability. To validate our
                                                          negative correlation between iteration and accuracy
routing mechanism, we evaluated the classifier on
                                                          (τ = −0.84 average, p < 0.001). This could be
a stress-test dataset (also see Appendix C.3) of
                                                          due to self-refinement (without formal verification)
N = 54 claims, including adversarial edge cases
                                                          introducing hallucinations where the model "cor-
such as idioms (e.g., “gave 110%”) and vague quan-
                                                          rects" valid reasoning into invalid states. This con-
tifiers. The router achieved an overall accuracy
                                                          vergence analysis provides the strongest statistical
of 94%, with strong discrimination between cate-
                                                          evidence for VERGE’s value: while final accu-
gories (SMT: F1=0.93; Soft: F1=0.95). Crucially,
                                                          racy gains are modest (average +9.3 points), the
the error patterns reveal a safe failure mode: only
                                                          observed consistent monotonic improvement has
1 out of 32 soft claims was misrouted to SMT; a
                                                          high practical value in production systems where
recoverable error that triggers autoformalization
                                                          reliability matters more than peak performance.
fallback. The high recall for Soft claims (0.97) and
precision for SMT claims (0.95) confirm the sys-          4.4   Model Scalability and The Formalization
tem effectively shields the solver from ambiguity               Barrier
while preserving logical rigor.
                                                          We observe that effectiveness is contingent on the
Scoring sensitivity. The weights (1.0,0.9,0.7,0.0)        model’s ability to produce syntactically valid SMT
encode an ordinal hierarchy, not a tuned operat-          code. We term this threshold the Formalization Bar-
rier. Our tested model under 20B parameters (GPT-       Formalization Barrier and Access Inequality.
OSS-20B) struggles, achieving only ∼30% syntax          Our analysis reveals models under 20B parame-
validity. In this regime, the solver acts merely as     ters achieve only ∼30% formalization validity, re-
a spell-checker. However, models in the 120B+           stricting the solver to syntax checking rather than
and frontier regime (GPT-OSS-120B, Sonnet) cross        semantic verification. This creates a capability
the barrier (>90% validity). Here, solver feedback      threshold where only organizations with access
shifts from generic error messages to semantic logi-    to frontier models (≥70B parameters) can lever-
cal contradictions, enabling VERGE’s MCS mech-          age VERGE’s full potential. Additionally, restrict-
anism to perform actual reasoning repairs. This         ing to decidable logics (QF-UF, LIA) sacrifices ex-
suggests that neuro-symbolic verification is a ca-      pressiveness claims requiring universal quantifica-
pability that emerges with scale, and VERGE is          tion, non-linear arithmetic, or recursive definitions
uniquely positioned to leverage the next generation     cannot be formally verified and must fall back to
of highly capable reasoning models.                     soft verification. This undermines the framework’s
                                                        promise of provability for complex mathematical
5   Conclusions                                         or algorithmic reasoning.
We present VERGE, a neuro-symbolic framework
combining LLMs with SMT solvers for verified
                                                        7   Ethical Considerations
reasoning via iterative refinement. Our approach
introduces three key innovations: (1) high-fidelity
formalization via multi-sample consensus, (2) se-       Logical Correctness is not Ethical Correctness.
mantic routing that balances symbolic solvers with      VERGE verifies internal consistency and logical
soft verification, and (3) actionable feedback via      entailment, not moral soundness or factual truth.
Minimal Correction Subsets (MCS) for precise er-        The system could formally prove harmful reason-
ror localization. Evaluation shows VERGE ex-            ing—discriminatory policies that satisfy legal con-
cels in formal reasoning and achieves convergence       straints, exploit chains in cybersecurity, or conspir-
across all datasets, contrasting with the degrada-      acy theories with internally consistent logic but
tion often observed in probabilistic self-refinement.   false premises. SMT solvers are fundamentally
Our analysis identifies a “Formalization Barrier” at    value-neutral tools. Deploying VERGE in high-
the 70B+ parameter scale where semantic verifica-       stakes domains (legal, medical, military decision-
tion becomes viable. By bridging neural genera-         making) requires additional ethical oversight layers:
tion with symbolic reasoning, VERGE provides a          premise provenance tracking, factuality verification
practical step toward trustworthy AI with provable      orthogonal to logic, and human expert review for
correctness where logic permits.                        consequential decisions.

6   Limitations
                                                        Risk of Overconfidence and Misplaced Trust.
Computational Overhead. VERGE incurs sig-               Labeling outputs as "verified" may induce false
nificantly higher latency than single-pass genera-      confidence in users unfamiliar with the distinction
tion. Each iteration requires claim decomposition,      between formal and soft verification. Our scoring
multiple formalization attempts (K = 3), consen-        system assigns high scores (0.9) to soft-verified
sus computation, SMT solver calls, and feedback         commonsense claims that lack mathematical guar-
generation. For problems with n > 20 atomic             antees. More critically, if autoformalization mis-
claims, the pipeline requires 15-30 seconds per iter-   represents a claim’s semantics producing syntac-
ation compared to > 2 seconds for standard Chain-       tically valid but semantically incorrect SMT code
of-Thought prompting. While our greedy MCS              the solver verifies the wrong statement, creating
approximation reduces complexity from exponen-          "verified hallucinations." Users may over-rely on
tial O(2n ) to linear O(n × SAT), the multiplica-       verification badges without understanding rigor gra-
tive overhead remains substantial. This latency-        dations. Clear interface design distinguishing "for-
accuracy trade-off limits deployment in interactive     mally proven" (σE ) from "consensus-supported"
applications requiring sub-second response times        (νS ) claims is essential but insufficient if users lack
(e.g., conversational AI, real-time decision sup-       technical literacy.
port).
References                                                 Yilun Du, Shuang Li, Antonio Torralba, Joshua B.
                                                             Tenenbaum, and Igor Mordatch. 2023. Improving
Anthropic. 2025. Introducing Claude Opus 4.5. Ac-            factuality and reasoning in language models through
  cessed: 2025-12-19.                                        multiagent debate. arXiv preprint arXiv:2305.14325.
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten         Yu Feng, Nathaniel Weir, Kaj Bostrom, Sam Bayless,
   Bosma, Henryk Michalewski, David Dohan, Ellen             Darion Cassel, Sapana Chaudhary, Benjamin Kiesl-
   Jiang, Carrie Cai, Michael Terry, Quoc Le, and 1          Reiter, and Huzefa Rangwala. 2025. Vericot: Neuro-
   others. 2021. Program synthesis with large language       symbolic chain-of-thought validation via logical con-
   models. arXiv preprint arXiv:2108.07732.                  sistency checks. arXiv preprint arXiv:2511.04662.
Zhangir Azerbayev, Bartosz Piotrowski, Hailey              Debargha Ganguly, Srinivasan Iyengar, Vipin Chaud-
  Schoelkopf, Edward W Ayers, Dragomir Radev, and            hary, and Shivkumar Kalyanaraman. 2024. PROOF
  Jeremy Avigad. 2023. ProofNet: Autoformalizing             OF THOUGHT : Neurosymbolic program synthe-
  and formally proving undergraduate-level mathemat-         sis allows robust and interpretable reasoning. In
  ics. arXiv preprint arXiv:2302.12433.                      The First Workshop on System-2 Reasoning at Scale,
Fahiem Bacchus and George Katsirelos. 2016. Finding          NeurIPS’24.
  a collection of muses incrementally. In Integration of
                                                           Debargha Ganguly, Sreehari Sankar, Biyao Zhang,
  AI and OR Techniques in Constraint Programming,
                                                             Vikash Singh, Kanan Gupta, Harshini Kavuru, Alan
  pages 35–44, Cham. Springer International Publish-
                                                             Luo, Weicong Chen, Warren Morningstar, Raghu
  ing.
                                                             Machiraju, and Vipin Chaudhary. 2026. Trust the
Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia, and     typical. Preprint, arXiv:2602.04581.
  Cesare Tinelli. 2009. Satisfiability modulo theories.
                                                           Debargha Ganguly, Vikash Singh, Sreehari Sankar,
  In Handbook of Satisfiability, volume 185, pages
                                                             Biyao Zhang, Xuecen Zhang, Srinivasan Iyengar, Xi-
  825–885. IOS Press.
                                                             aotian Han, Amit Sharma, Shivkumar Kalyanaraman,
Jonathan Berant, Andrew Chou, Roy Frostig, and Percy         and Vipin Chaudhary. 2025. Grammars of formal
  Liang. 2013. Semantic parsing on Freebase from             uncertainty: When to trust LLMs in automated rea-
  question-answer pairs. In Proceedings of the 2013          soning tasks. In The Thirty-ninth Annual Conference
  Conference on Empirical Methods in Natural Lan-            on Neural Information Processing Systems.
  guage Processing, pages 1533–1544.
                                                           Artur d’Avila Garcez, Marco Gori, Luis C. Lamb, Lu-
Benjamin Callewaert, Simon Vandevelde, and Joost             ciano Serafini, Michael Spranger, and Son N. Tran.
  Vennekens. 2025. Verus-lm: a versatile framework           2019. Neural-symbolic computing: An effective
  for combining llms with symbolic reasoning. arXiv          methodology for principled integration of machine
  preprint arXiv:2501.14540.                                 learning and reasoning. Journal of Applied Logics,
                                                             6(4):611–632.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
 Henrique Ponde de Oliveira Pinto, Jared Kaplan,           Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg            Yujiu Yang, Nan Duan, and Weizhu Chen. 2024.
 Brockman, and 1 others. 2021. Evaluating large              CRITIC: Large language models can self-correct
 language models trained on code. arXiv preprint             with tool-interactive critiquing. In International Con-
 arXiv:2107.03374.                                           ference on Learning Representations (ICLR).

Weicong Chen, Vikash Singh, Zahra Rahmani, De-             Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-
 bargha Ganguly, Mohsen Hariri, and Vipin Chaud-             ing Qi, Martin Riddell, Wenfei Zhou, James Coady,
 hary. 2025. K4: Online log anomaly detection via            David Peng, Yujie Qiao, Luke Benson, and 1 oth-
 unsupervised typicality learning. In 2025 IEEE 32nd         ers. 2024. Folio: Natural language reasoning with
 International Conference on High Performance Com-           first-order logic. In Proceedings of the 2024 Con-
 puting, Data, and Analytics (HiPC), pages 96–107.           ference on Empirical Methods in Natural Language
                                                             Processing, pages 22017–22031.
Alonzo Church. 1936. An unsolvable problem of ele-
  mentary number theory. American Journal of Mathe-        Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  matics, 58(2):345–363.                                     Arora, Steven Basart, Eric Tang, Dawn Song, and
                                                             Jacob Steinhardt. 2021. Measuring mathematical
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An          problem solving with the MATH dataset. Advances
  efficient SMT solver. In International Conference          in Neural Information Processing Systems, 34:6901–
  on Tools and Algorithms for the Construction and           6914.
  Analysis of Systems, pages 337–340. Springer.
                                                           Jie Huang, Xinyun Chen, Swaroop Mishra,
Li Dong and Mirella Lapata. 2016. Language to logical         Huaixiu Steven Zheng, Adams Wei Yu, Xiny-
   form with neural attention. In Proceedings of the          ing Song, and Denny Zhou. 2023. Large language
   54th Annual Meeting of the Association for Compu-          models cannot self-correct reasoning yet. arXiv
   tational Linguistics, volume 1, pages 33–43.               preprint arXiv:2310.01798.
Albert Q Jiang, Sean Welleck, Jin Peng Zhou,               with self-feedback. In Advances in Neural Informa-
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-             tion Processing Systems, volume 36.
  thee Lacroix, Yuhuai Wu, and Guillaume Lample.
  2022. Draft, sketch, and prove: Guiding formal the-    Jiayuan Mao, Chuang Gan, Pushmeet Kohli, Joshua B.
  orem provers with informal proofs. arXiv preprint         Tenenbaum, and Jiajun Wu. 2019. The neuro-
  arXiv:2210.12283.                                         symbolic concept learner: Interpreting scenes, words,
                                                            and sentences from natural supervision. In Interna-
Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han,              tional Conference on Learning Representations.
  and Rui Zhang. 2024. When can llms actually cor-
  rect their own mistakes? a critical survey of self-    Joao Marques-Silva, Federico Heras, Mikolas Janota,
  correction of llms. Transactions of the Association      Alessandro Previti, and Anton Belov. 2013a. On com-
  for Computational Linguistics, 12:1417–1440.             puting minimal correction subsets. In Proceedings
                                                           of the Twenty-Third International Joint Conference
Henry Kautz. 2022. The third AI summer: AAAI               on Artificial Intelligence, IJCAI ’13, page 615–622.
  Robert S. Engelmore memorial lecture. AI Maga-           AAAI Press.
  zine, 43(1):105–125.
                                                         Joao Marques-Silva, Federico Heras, Mikoláš Janota,
Mehran Kazemi, Bahare Fatemi, Hritik Bansal, John          Alessandro Previti, and Anton Belov. 2013b. On
 Palowitch, Chrysovalantis Anastasiou, Sanket Vaib-        computing minimal correction subsets. In Inter-
 hav Mehta, Lalit K Jain, Virginia Aglietti, Disha         national Joint Conference on Artificial Intelligence,
 Jindal, Yuanzhu Peter Chen, and 1 others. 2025. Big-      pages 615–622.
 bench extra hard. In Proceedings of the 63rd An-
                                                         Lachlan McGinness and Peter Baumgartner. 2024.
 nual Meeting of the Association for Computational
                                                           Automated theorem provers help improve large
 Linguistics (Volume 1: Long Papers), pages 26473–
                                                           language model reasoning.     arXiv preprint
 26501.
                                                           arXiv:2408.03492.
Aitor Lewkowycz, Anders Andreassen, David Dohan,         Antonio Morgado, Federico Heras, Mark Liffiton, Jordi
  Ethan Dyer, Henryk Michalewski, Vinay Ramasesh,          Planes, and Joao Marques-Silva. 2013. Iterative and
  Ambrose Slone, Cem Anil, Imanol Schlag, Theo             core-guided MaxSAT solving: A survey and assess-
  Gutman-Solo, and 1 others. 2022. Solving quan-           ment. Constraints, 18(4):478–534.
  titative reasoning problems with language models. In
  Advances in Neural Information Processing Systems,     Alexander Nadel, Vadim Ryvchin, and Ofer Strichman.
  volume 35, pages 3843–3857.                              2013. Efficient mus extraction with resolution. In
                                                           2013 Formal Methods in Computer-Aided Design,
Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang,           pages 197–200.
  Yan Wang, Rui Wang, Yujiu Yang, Zhaopeng Tu, and
  Shuming Shi. 2023. Encouraging divergent thinking      Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  in large language models through multi-agent debate.     Armando Solar-Lezama, Joshua Tenenbaum, and
  arXiv preprint arXiv:2305.19118.                         Roger Levy. 2023. Linc: A neurosymbolic approach
                                                           for logical reasoning by combining language models
Mark H Liffiton and Karem A Sakallah. 2008. Al-            with first-order logic provers. In Proceedings of the
 gorithms for computing minimal unsatisfiable sub-         2023 Conference on Empirical Methods in Natural
 sets of constraints. Journal of Automated Reasoning,      Language Processing, pages 5153–5176.
 40(1):1–33.
                                                         OpenAI. 2025. Introducing OpenAI o3 and o4-mini.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri        Accessed: 2025-12-19.
  Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  John Schulman, Ilya Sutskever, and Karl Cobbe.         Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  2023. Let’s verify step by step. arXiv preprint          Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  arXiv:2305.20050.                                        Sandhini Agarwal, Katarina Slama, Alex Ray, and
                                                           1 others. 2022. Training language models to follow
Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson,           instructions with human feedback. In Advances in
  Ashish Sabharwal, Radha Poovendran, Peter Clark,         Neural Information Processing Systems, volume 35,
  and Yejin Choi. 2025. Zebralogic: On the scaling         pages 27730–27744.
  limits of llms for logical reasoning. arXiv preprint
  arXiv:2502.01100.                                      Liangming Pan, Alon Albalak, Xinyi Wang, and
                                                           William Yang Wang. 2023.          Logic-lm: Em-
Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang,           powering large language models with symbolic
  Delip Rao, Eric Wong, Marianna Apidianaki, and           solvers for faithful logical reasoning. Preprint,
  Chris Callison-Burch. 2023. Faithful chain-of-           arXiv:2305.12295.
  thought reasoning. arXiv preprint arXiv:2301.13379.
                                                         Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li,
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler           Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang,
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,            Mohamed Shaaban, John Ling, Sean Shi, and 1 oth-
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,             ers. 2025. Humanity’s last exam. arXiv preprint
 and 1 others. 2023. Self-refine: Iterative refinement     arXiv:2501.14249.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-      Wang Yang, Debargha Ganguly, Xinpeng Li, Chaoda
   tas Baksys, Igor Babuschkin, and Ilya Sutskever.         Song, Shouren Wang, Vikash Singh, Vipin Chaud-
   2022. Formal mathematics statement curriculum            hary, and Xiaotian Han. 2026. Mid-think: Training-
   learning. In International Conference on Learning        free intermediate-budget reasoning via token-level
   Representations.                                         triggers. Preprint, arXiv:2601.07036.

Stanislas Polu and Ilya Sutskever. 2020. Generative        Osama Zafar, Mina Namazi, Yuqiao Xu, Youngjin Yoo,
   language modeling for automated theorem proving.          and Erman Ayday. 2026. A user-centric, privacy-
   arXiv preprint arXiv:2009.03393.                          preserving, and verifiable ecosystem for personal data
                                                             management and utilization. In Computer Security
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta         – ESORICS 2025, pages 395–414, Cham. Springer
  Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola           Nature Switzerland.
  Cancedda, and Thomas Scialom. 2023. Toolformer:          Luke S. Zettlemoyer and Michael Collins. 2005. Learn-
  Language models can teach themselves to use tools.         ing to map sentences to logical form: Structured clas-
  In Advances in Neural Information Processing Sys-          sification with probabilistic categorial grammars. In
  tems, volume 36.                                           Conference on Uncertainty in Artificial Intelligence,
                                                             pages 658–666.
Noah Shinn, Federico Cassano, Ashwin Gopinath,
  Karthik Narasimhan, and Shunyu Yao. 2023. Re-            Biyao Zhang, Mingkai Zheng, Debargha Ganguly, Xue-
  flexion: Language agents with verbal reinforcement         cen Zhang, Vikash Singh, Vipin Chaudhary, and
  learning. In Advances in Neural Information Pro-           Zhao Zhang. 2025. Efficient fine-grained gpu perfor-
  cessing Systems, volume 36.                                mance modeling for distributed deep learning of llm.
                                                             Preprint, arXiv:2509.22832.
Vikash Singh, Debargha Ganguly, Haotian Yu, Cheng-
  wei Zhou, Prerna Singh, Brandon Lee, Vipin Chaud-        Lintao Zhang and Sharad Malik. 2003. Extracting small
  hary, and Gourav Datta. 2026. Toward guarantees            unsatisfiable cores from unsatisfiable boolean for-
  for clinical reasoning in vision language models via       mula. In International Conference on Theory and
  formal verification. Preprint, arXiv:2602.24111.           Applications of Satisfiability Testing, volume 2003.
                                                           Wanjun Zhong, Siyuan Wang, Duyu Tang, Zenan Xu,
Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.
                                                            Daya Guo, Jiahai Wang, Jian Yin, Ming Zhou, and
  ProofWriter: Generating implications, proofs, and
                                                            Nan Duan. 2021. Ar-lsat: Investigating analytical
  abductive statements over natural language. In Find-
                                                            reasoning of text. arXiv preprint arXiv:2104.06598.
  ings of the Association for Computational Linguistics:
  ACL-IJCNLP 2021, pages 3621–3634.
                                                           A        VERGE: Algorithm / Pseudo code
Alan M. Turing. 1936. On computable numbers, with
  an application to the Entscheidungsproblem. Pro-             wS     FOLIO   PW     ZL     AR-LSAT BBEH HLE
  ceedings of the London Mathematical Society, s2-
  42(1):230–265.                                               0.70    83.9   89.2   90.6    90.8   57.4   29.1
                                                               0.80    84.3   89.5   90.8    91.2   58.1   29.7
                                                               0.90    84.7   89.9   91.0    91.7   58.9   30.5
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-
                                                               0.95    84.4   89.7   90.9    91.4   58.5   30.2
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,          1.00    84.0   89.3   90.5    91.0   57.8   29.4
  Geoffrey Irving, and Irina Higgins. 2022. Solv-
  ing math word problems with process-and outcome-
  based feedback. arXiv preprint arXiv:2211.14275.         Table 4: Sensitivity to wS (others fixed) on GPT-OSS-
                                                           120B.
Nengbo Wang, Tuo Liang, Vikash Singh, Chaoda
  Song, Van Yang, Yu Yin, Jing Ma, Jagdip Singh,
  and Vipin Chaudhary. 2026. Hugrag: Hierarchical          B     Rationale for Greedy MCS
  causal knowledge graph design for rag. Preprint,               Computation
  arXiv:2602.05143.
                                                           To provide actionable feedback when a generated
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,          answer is contradictory, VERGE must identify a
  Ed Chi, Sharan Narang, Aakanksha Chowdhery, and          Minimal Correction Subset (MCS): a minimal sub-
  Denny Zhou. 2022. Self-consistency improves chain
  of thought reasoning in language models. In Interna-     set of atomic claims that, if removed, restores con-
  tional Conference on Learning Representations.           sistency. Formally, finding an MCS is equivalent to
                                                           finding the complement of a Maximal Satisfiable
Sean Welleck, Ximing Lu, Peter West, Faeze Brahman,        Subset (MSS).
  Tianxiao Shen, Daniel Khashabi, and Yejin Choi.
  2022. Generating sequences by learning to self-
                                                              While exact algorithms ensure the theoretically
  correct. In International Conference on Learning         smallest removal set, they require exploring the
  Representations.                                         combinatorial search space of all subsets, leading
Algorithm 1 Iterative Verification and Refinement (VERGE)
 1: Initialize A(0) ← null, S (0) ← 0
 2: Extract entities: E ← EntityExtraction(C, q)
 3: Formalize context: φC ← AutoFormalize(C, E)
 4: if ¬SAT(φC ) then φC ← RefineContext(φC ) {Handle Translation Bottleneck}
 5: best_answer ← null, best_score ← 0
 6: for t = 1 to Tmax do
 7:     Generate answer: A(t) ← LLM(C, q, F (t−1) )
                            (t)
 8:     Extract claims: {ci } ← Decompose(A(t) )
                                                  (t)
 9:     Classify claims: τi ← SemanticRouter(ci )
                                                                 (t)
10:     if IsFormal(τi ) then φci , αi ← FormalizeConsensus(ci )
                                        (t)                    (t)
11:     else φci ← BooleanAbstract(ci ), αi ← SoftConf(ci ) {Boolean var for Soft claims}
                                                           (t)
12:     Verify individual claims: si ← RouteAndVerify(ci , τi , φci )
13:     Identify valid subset: V = {ci | si is not Contradictory} V
14:     Verify joint consistency: JointSAT, Core ← Solver(φC ∧ ck ∈V φck )
15:     Compute score: S (t) ← AggScore({si }, JointSAT, {αi })
16:     if S (t) > best_score then
17:         Update best score: best_score ← S (t) , best_answer ← A(t)
18:     end if
19:     if S (t) ≥ τacc and JointSAT then
20:         return A(t)
21:     end if
22:     if Convergence detected (∆S < ϵ) then
23:         return best_answer
24:     end if
25:     {Feedback Generation}
26:     Findiv ← GetIndividualErrors({ci } \ V )
27:     if ¬JointSAT then
28:         {Sorted Greedy MCS on Valid Claims}
29:         Sort V by confidence α descending
30:         MSS ← ∅, MCS ← ∅
31:         for ck ∈ V do
32:             if Solver(φC ∧ MSS ∧ φck ) is SAT then
33:                 MSS ← MSS ∪ {ck }
34:             else
35:                 MCS ← MCS ∪ {ck } {Conflict found}
36:             end if
37:         end for
38:         Fjoint ← FormatFeedback(MCS, Core)
39:     else
40:         Fjoint ← IdentifyWeakClaims(V )
41:     end if
42:     F (t) ← Findiv ∪ Fjoint
43: end for
44: return best_answer



to exponential time complexity (O(2n )). For an              computational disparity becomes prohibitive even
LLM inference pipeline where latency is critical,            for moderate claim counts (n = 20).
this approach is computationally intractable.

The Greedy Approximation. To address this,                      The trade-off is that the greedy approach is order-
we employ a linear-scan approximation (c.f. Algo-            dependent and may not find the global maximum
rithm 1; (Marques-Silva et al., 2013b)). The algo-           subset (e.g., it might recommend deleting 3 claims
rithm iterates through atomic claims c1 , . . . , cn se-     when deleting 2 would suffice). However, in the
quentially. For each claim, it checks if adding it to        context of Iterative Refinement, actionability pri-
the current set of consistent claims preserves satis-        oritizes optimality. Getting a "valid enough" cor-
fiability (SAT). If SAT(Context ∧ Current_Set ∧ ci )         rection signal in seconds is practically superior to
holds, ci is kept; otherwise, it is marked for re-           waiting hours for a mathematically perfect one.
moval.                                                       The greedy MCS provides a specific, consistent
   This reduces the complexity from exponential              sub-context that guides the LLM effectively, even
to linear (O(n × SAT)). As shown in Table 5, the             if it is sub-optimal.
Stability & Order Dependence: Greedy MCS is                    sorts (e.g., Person, Number) where applica-
order-dependent and to maximize the retention of               ble.
high-quality reasoning, we sort claims by their indi-
vidual verification confidence (descending) before         2. Predicate Mapping: Relations are mapped
the greedy pass. This prioritizes keeping ’Entailed’          to boolean functions. For example, “Felix
or High-Confidence Soft claims and suggests mod-              eats food” maps to (assert (Eats Felix
ifying the weakest links first. In preliminary tests,         Food)).
this sorting reduced feedback variance significantly       3. Quantifier Handling: While SMT solvers
compared to random ordering.                                  support quantifiers (∀, ∃), they often lead to
                                                              undecidability. Where possible, we instanti-
C     Semantic Claim Type Definitions                         ate universals over the finite set of extracted
To ensure the Semantic Router directs claims to               entities E to maintain decidability.
the appropriate verification strategy (as described      C.2    Formal Definition of Semantic
in Section 2.2 and Eq. 2), we formally define the               Equivalence
six semantic categories (τ ) used by VERGE in
Table (6).                                               In Section 3.3, we introduce Semantic Equiva-
                                                         lence Checking to compute consensus among can-
   The routing decision is binary based on these
                                                         didate formalizations. Here, we precisely define the
types: Hard Verification (SMT) is applied to de-
                                                         logical framework and the equivalence condition.
terministically provable claims (τM , τL , τT ), while
Soft Verification (Consensus) is applied to claims       C.2.1 Logical Framework
requiring world knowledge or subjective interpre-        VERGE operates within the framework of Many-
tation (τC , τV , τP ).                                  Sorted First-Order Logic (specifically, the SMT-
                                                         LIB2 standard). However, to ensure decidability
C.1     Technical Implementation Details
                                                         and efficiency, we restrict the formalization to spe-
To ensure reproducibility and formal rigor, we de-       cific fragments:
fine the specific mechanisms used for claim decom-
position, autoformalization, and consensus scoring.         • QF_UF (Quantifier-Free Uninterpreted Func-
                                                              tions): Used for abstract relationships and cat-
C.1.1     Atomic Decomposition Strategy                       egorical claims.
We define an Atomic Claim ci as the minimal
                                                            • QF_LIA (Quantifier-Free Linear Integer
semantic unit that carries a truth value indepen-
                                                              Arithmetic): Used for numerical constraints
dent of other claims. Given a generated answer
                                                              and temporal sequencing.
A, we employ a zero-shot decomposition func-
tion fdecomp : (C, A) → {c1 , . . . , cn }. To pre-         • Finite Domain Quantification: Where uni-
vent context loss, we enforce that every ci must be           versal quantifiers (∀) are unavoidable in nat-
self-contained (i.e., resolving pronouns like "he"            ural language, we instantiate them over the
to specific entities such as "Felix"). This is im-            finite set of extracted entities E (see §3.1),
plemented via a structure-enforcing prompt that               effectively reducing them to conjunctions in
outputs a JSON list of claims, preventing the hallu-          Propositional Logic.
cination of non-existent dependencies.
                                                         C.2.2 Equivalence Definition
C.1.2     Formalization into SMT-LIB2                    Let C be the problem context and E be the set of
For claims classified as τLogic or τM ath , we target    extracted entities. We define a Signature ΣE =
the QF_UF (Quantifier-Free Uninterpreted Func-           (S, F, P) consisting of:
tions) and LIA (Linear Integer Arithmetic) logics
                                                            • S: A set of sorts (types) derived from the
within the SMT-LIB2 standard. The translation
                                                              context (e.g., Student, Day).
process T : ci → φi operates under strict syntactic
constraints:                                                • F: A set of function symbols (e.g., age:
                                                              Person → Int).
    1. Type Declaration: All entities extracted in
       the Setup phase are declared as uninterpreted        • P: A set of predicate symbols (e.g.,
       constants of a generic sort Object or specific         gives_report: Student × Day → Bool).
                     Feature                   MCS             Greedy MCS (Ours)
                     Optimality        Guaranteed Minimal         Approximation
                     Complexity          O(2n × SAT)               O(n × SAT)
                     Space                Exponential                Linear
                     Estimated SAT Calls required:
                     n = 10 atoms           1,024                        10
                     n = 20 atoms         1,048,576                      20
                     n = 30 atoms        ∼1 Billion                      30

Table 5: Computational comparison between exact and greedy MCS strategies. For real-time LLM reasoning tasks
(where n often exceeds 20), the exact approach is infeasible, whereas the greedy approach scales linearly.


  Two candidate formulas ϕa and ϕb generated by          1. Logic & Math (Standard): 22 claims sam-
the LLM are defined as Semantically Equivalent              pled from FOLIO and AR-LSAT contain-
modulo ΣE if and only if they share the same truth          ing explicit logical operators, arithmetic con-
value in every possible interpretation I consistent         straints, and temporal sequences (e.g., “The
with the signature:                                         meeting is at 2 PM,” “x is greater than 70”).
                                                         2. Commonsense & Vague (Standard): 20
  ϕa ≡Σ ϕb ⇐⇒ ∀I |= ΣE ,          Jϕa KI = Jϕb KI           claims involving subjective predicates, proba-
                                                 (7)        bility, or world knowledge not strictly defin-
C.2.3 Verification Implementation                           able in SMT (e.g., “It is likely to rain,” “The
In practice, we verify this condition using the SMT         painting is beautiful”).
solver (Z3) by checking the unsatisfiability of the      3. Adversarial Edge Cases: 12 manually
negated biconditional. We construct a query Q:              crafted claims designed to trick keyword-
                                                            based classifiers. These include:
        Q = Declare(ΣE ) ∧ ¬(ϕa ↔ ϕb )           (8)           • Numeric Idioms: Phrases containing
                                                                  numbers that are not mathematical (e.g.,
If SOLVE(Q) returns UNSAT, it implies there is
                                                                  “He gave 110% effort,” “She was on
no model where ϕa and ϕb differ; thus, they are
                                                                  cloud nine”).
logically equivalent.
   This approach is robust to:                                 • Logical Homonyms: Words like “fol-
                                                                  lows” or “implies” used rhetorically
  1. Syntactic Permutation: (A ∧ B) ≡ (B ∧ A).                    rather than deductively (e.g., “It follows
                                                                  that he was angry”).
  2. Variable Renaming: ∀x.P (x) ≡ ∀y.P (y)
     (handled via canonicalization or finite instan-           • Perturbed Contexts: Claims derived
     tiation).                                                    from logic puzzles where constraints
                                                                  were inverted to test stability (e.g., swap-
  3. Tautological Variance: (P → Q) ≡ (¬P ∨                       ping “banned” for “permitted” to verify
     Q).                                                          routing consistency remains robust under
                                                                  contradiction).
Unlike string matching or embedding similarity,
this provides a mathematically rigorous guarantee        Ground truth labels (SMT-Amenable vs. Soft-
that the consensus candidates represent the exact      Verification) were manually assigned by two au-
same logical constraint.                               thors with high inter-annotator agreement (κ >
                                                       0.9). Table 7 provides examples of these challeng-
C.3   Semantic Router Stress-Test Dataset              ing edge cases.
To rigorously evaluate the Semantic Router (Sec-
                                                        D   Adversarial Robustness and Context
tion 4.2), we constructed a diverse evaluation set
                                                            Faithfulness
of N = 54 atomic claims designed to probe the
decision boundary between formalizable logic and       A known failure mode of reasoning models is
natural language ambiguity. The dataset was com-       the “Faithfulness Gap,” where the model ignores
posed of three distinct subsets:                       provided context in favor of its parametric mem-
            Type     Definition                                    Example                                Router

            Group A: SMT-Amenable Claims (Hard Verification)

            τM       Mathematical: Claims involving arith-         "x is a prime number greater than 5    SMT
                     metic operations, algebraic constraints,      and less than 20."
                     numerical comparisons, or unit conver-
                     sions.
            τL       Logical: Claims involving formal en-          "All entities in set A must also be-   SMT
                     tailment, set theory inclusion, boolean       long to set B."
                     logic, or syllogistic structure.
            τT       Temporal: Claims involving linear se-         "The event occurred 3 days after the   SMT
                     quencing, specific timestamps, duration,      signing."
                     or precedence constraints.

            Group B: LLM-Consensus Claims (Soft Verification)

            τC       Commonsense: Claims relying on gen-           "Glass typically shatters when         Soft
                     eral world knowledge, causality, or phys-     dropped on concrete."
                     ical properties not strictly definable by
                     axioms.
            τV       Vague: Claims involving subjective            "The painting is considered beauti-    Soft
                     predicates, qualitative descriptors, or at-   ful by most critics."
                     tributes lacking a boolean truth value.
            τP       Probabilistic: Claims explicitly stating      "It is likely to rain tomorrow given   Soft
                     uncertainty, likelihood, or future predic-    the clouds."
                     tions without deterministic data.

Table 6: Definitions of Semantic Claim Types (τ ) used in the Routing Module. Claims in Group A are autoformalized
into SMT-LIB2 logic; Claims in Group B are verified via multi-model consensus.

                   Category                 Example Claim                                Correct Route
                   Numeric Idiom            “The team gave 110% effort.”                       Soft
                   Numeric (Real)           “The score was 110 points.”                        SMT
                   Logical Homonym          “It follows that he felt sad.”                     Soft
                   Logical (Real)           “It follows that A ⊂ B.”                           SMT
                   Vague Quantifier         “Many people attended.”                            Soft
                   Exact Quantifier         “More than 50 people attended.”                    SMT

Table 7: Examples from the Semantic Router Stress-Test Dataset, highlighting adversarial pairs used to test the
router’s discrimination capabilities.


ory (e.g., refusing to accept a counterfactual                     align its generated answer with the perturbed con-
premise like “Cats are not mammals”). To eval-                     text. This confirms that our formal verification
uate VERGE’s robustness to such logical pertur-                    constraint effectively enforces context-faithfulness
bations, we conducted an adversarial probe using                   over parametric memory.
paired samples where the logical constraints were
inverted or perturbed (e.g., changing “banned” to                  E     Reproducibility & Implementation
“permitted”, or swapping temporal order).                                Details

   As shown in Table 8, VERGE demonstrated                         To ensure the replicability of VERGE, we provide
100% robustness across the tested categories.                      detailed specifications of our prompt engineering,
Notably, the system maintained high verification                   hyperparameters, and computational infrastructure.
scores (avg. 0.91) on the adversarial samples. This
indicates that VERGE successfully overcame the                     E.1    Hyperparameters and Configuration
“prior bias” of the LLM; rather than hallucinat-                   We utilize all models in Table 1 (via AWS Bedrock)
ing the standard answer or failing verification, the               as the backbone LLM for all generation and refine-
MCS-guided feedback loop forced the model to                       ment steps due to its strong reasoning capabilities.
                         Perturbation Type    Original     Perturbed    Status   Adaptation
                         Logic Inversion                                 Safe    Correct Flip
                         Numeric Threshold                               Safe    Correct Flip
                         Sequence Swap                                   Safe    Correct Flip
                         Mutually Exclusive                              Safe    Correct Flip

Table 8: Adversarial Robustness results. “Safe” indicates the system either rejected the invalid premise or, in these
cases, successfully adapted its reasoning to the counterfactual context (faithfulness), achieving high verification
scores (> 0.9) on the perturbed inputs.


We use Z3 (version 4.12.2) as the SMT solver. Ta-               System Prompt: Decomposition
ble 9 details the specific configuration used across
                                                                You are an expert logician. Analyze the
all experiments.                                                provided Answer and decompose it into
                                                                atomic, verifiable claims.              For each
                                                                claim, assign a Semantic Type based on the
                                                                following definitions:
                                                                   • MATHEMATICAL: Involves arithmetic, algebra, or
        Parameter                       Value                        numerical constraints.
        LLM Generation                                             • LOGICAL: Involves first-order logic, set theory,
                                                                     or strict deduction.
        Temperature (Tgen )             1.0                        • COMMONSENSE: Involves general world knowl-
        Top-P                           0.99                         edge or vague predicates.
                                                                Output format: JSON list of objects {“text":
        Max Output Tokens              10,000                   string,“type": string}.
        Thinking Budget                4,000
        VERGE Pipeline
        Max Iterations (Tmax )           3                   E.2.2     Autoformalization (Natural Language
        Consensus Samples (K)            3                             →SMT-LIB2)
        Consensus Threshold            0.70
        Soft-Verify Judges (N )          5                   This prompt translates text into code. Note the
        Acceptance Score (τacc )       0.75                  instruction (set-logic ALL), which allows the
        Convergence ϵ                  0.01                  solver to handle mixed integer arithmetic and unin-
        Judge Model                  Sonnet-3.7              terpreted functions dynamically.
Table 9: Hyperparameters for the VERGE pipeline.
These values were held constant across all datasets (FO-        System Prompt: Formalization
LIO, ZebraLogic, etc.) to demonstrate robustness.
                                                                Translate the following natural language
                                                                context and claims into SMT-LIB2 format for
                                                                the Z3 solver.
                                                                Constraints:
                                                                  1. Declare all sorts (e.g., Person,
                                                                     Object) explicitly.
                                                                  2. Use (set-logic ALL) to support mixed
E.2     Prompt Templates                                             arithmetic and logic.
                                                                  3. Do not include (check-sat) commands;
                                                                     simply assert the facts.
                                                                  4. If a statement is ambiguous, use
We employ a modular prompting strategy. The sys-                     uninterpreted functions.
tem prompts for the key components of the pipeline              Input Context: [CONTEXT]
                                                                Input Claim: [CLAIM]
are provided below.                                             Output: <smt> ... code ... </smt>




E.2.1    Claim Decomposition & Classification                E.2.3     Feedback Injection (Refinement Step)

                                                             When the SMT solver returns UNSAT, we calculate
This prompt breaks the raw generation into atomic            the Minimal Correction Set (MCS) and feed it back
units and routes them to the appropriate verifier.           to the model using this template.
                                                                 Benchmark    Claims/Ans.    P      R
                                                                 FOLIO            3.2       0.96   0.94
                                                                 PW               4.1       0.97   0.95
                                                                 ZL               5.8       0.93   0.91
                                                                 AR-LSAT          6.4       0.94   0.92
                                                                 BBEH             4.7       0.92   0.90
                                                                 HLE              5.3       0.91   0.89

                                                         Table 10: Decomposition quality (80 audited trajecto-
                                                         ries).


                                                         generate K = 3 candidate formalizations for every
                                                         claim. We compute the Semantic Equivalence
                                                         between candidates by querying the solver for the
                                                         unsatisfiability of their negation (see Eq. 3). We
                                                         construct an equivalence graph where edges rep-
                                                         resent proven logical identity. If a clique of size
                                                         ≥ ⌈K/2⌉ (majority consensus) is found, the rep-
                                                         resentative formalization is accepted. Otherwise,
                                                         the claim is flagged as “Ambiguous” and routed to
                                                         Soft Verification.

                                                         Variance-Based Scoring. The final confidence
                                                         score S(A) is penalized if high-confidence claims
                                                         contradict each other. We define the score as:
                                                                                                         
                                                                                                σclaims
                                                         S(A) = µclaims · max 0.5, 1.0 −
                                                                                              µclaims + ϵ
Figure 3: The Correlation Cliff in Iterative Refine-                                                     (9)
ment. Accuracy progression over 10 iterations (GPT-      where µclaims is the weighted average verification
OSS-120B). VERGE exhibits perfect monotonic im-          status (Entailed=1.0, Soft-Pass=0.9, Possible=0.7,
provement (Kendall’s τ = 1.0, p < 0.001 across all       Fail=0.0) and σclaims is the standard deviation.
datasets). Probabilistic Self-Refinement shows system-
                                                         This penalizes answers that contain a mix of “True”
atic degradation (τ = −0.84 average, p < 0.001),
stagnating below the CoT baseline in 85% of trials       and “False” claims, encouraging internal consis-
(χ2 = 26.7, p < 0.001). Shaded regions show 95%          tency.
confidence bands.
                                                         E.4   Pipeline Reliability and Failure Modes

   System Prompt: Refinement                             We audit the three LLM stages that could silently
                                                         corrupt verification: decomposition, routing, and
   Your previous answer contained logical                formalization.
   contradictions verified by a formal solver.
   Please refine your reasoning. Verification Re-
   port:                                                 Decomposition. On 80 audited trajectories (Ta-
      • Status: UNSATISFIABLE                            ble 10), errors are dominated by omissions, not
      • Conflict Logic: [Z3_UNSAT_CORE]
      • Actionable Feedback: The set of claims           fabrications: omitted claims that matter resurface
         {C1, C3} cannot be true simultaneously.         as joint inconsistencies and are repaired by MCS
         Specifically, [MCS_DESCRIPTION].                feedback.
   Instruction: Rewrite your answer to resolve
   this contradiction.      Do not weaken the
   premises; correct your derivation.                    Formalization funnel. Table 11 traces hard-
                                                         routed claims. Consensus is the central fidelity gate:
                                                         a misformalization must independently appear in
E.3   Consensus and Scoring Metrics
                                                         ≥ 2/3 samples to survive. Round-trip alignment is
Formalization Consensus. To ensure the SMT               a second gate; invalid SMT triggers soft fallback
code faithfully represents the natural language, we      rather than silent failure.
         Stage                   20B     120B              servatively (§3.5); principled validation via com-
         Routed to hard (SMT)   68.1%   72.3%              positional translation remains open. Multi-sample
         Syntactically valid    30.2%   92.3%              consensus uses one formalizer; cross-model con-
         Consensus (≥ 2/3)      41.2%   87.1%
         Round-trip aligned     79.4%   94.6%
                                                           sensus is supported but not yet evaluated. Bridging
         Verified by solver     12.1%   83.8%              axioms enter only the joint check, never individual
         Soft fallback          55.9%   16.2%              verification. Adding constraints can destroy but
         Solver timeout/error    4.6%   3.4%
                                                           never create satisfiability, so a faulty bridge trig-
Table 11: Formalization funnel by scale; VERGE de-         gers conservative over-refinement but cannot cause
grades gracefully below the formalization barrier.         acceptance of an incorrect answer. Empirically,
                                                           joint SAT disagrees with individual verification on
           Benchmark    Hard    Soft   Hybrid              8.3% of GPT-OSS-120B problems; 72% are gen-
           FOLIO        82.4    12.1     5.5
                                                           uine conflicts and 28% bridge artifacts, with net
           PW           91.3    4.2     4.5                accuracy impact below 0.5%.
           ZL           88.7     6.8     4.5
           AR-LSAT      76.3    16.2     7.5
           BBEH         54.1    35.8    10.1               Benchmark Acc@T=10 Acc@T=15 Acc@T=20 ∆(T=10→20)
           HLE          41.2    47.3    11.5               FOLIO         86.1       86.3        86.3        +0.2
                                                           ZebraLogic    92.3       92.4        92.5        +0.2
Table 12: Routing % on GPT-OSS-120B; Hybrid = hard-        AR-LSAT       92.1       92.2        92.2        +0.1
                                                           HLE           31.8       32.0        32.1        +0.3
routed claims that fell back to soft.
                                                           Table 13: Extended iterations T > 10. Beyond T=10
Routing distribution. On GPT-OSS-120B (Ta-                 are negligible (< 0.3% across all benchmarks), validat-
                                                           ing the convergence criterion (∆S < ϵ = 0.01).
ble 12), logic-heavy benchmarks are >76% SMT-
verified, leaving little exposure to consensus-on-
falsehood; HLE/BBEH are soft-dominated by ne-
                                                           E.5   Compute Infrastructure
cessity, and VERGE honestly reflects this rather
than overclaiming.                                         All experiments were conducted on a standard
                                                           workstation (64GB RAM, 16-core CPU). The Z3
Error taxonomy. Three modes account for                    solver component handles both verification (avg.
nearly all formalization failures, each caught by an       < 200ms) and equivalence checking (capped at
existing safeguard: (i) predicate mismatches (Z3           2.0s timeout per pair). The LLM inference was
parse error, soft fallback); (ii) quantifier scope (con-   performed using the AWS Bedrock API.
sensus disagreement); (iii) missing axioms (spuri-
ous UNSAT triggers context refinement, §3.3). The          E.6   Benchmark Descriptions
Soft-Only ablation (−22.8% avg) confirms these
safeguards are load-bearing.                               We used test split of each dataset mentioned below:
                                                              FOLIO (Han et al., 2024): First-order logic
Entity extraction. Accuracy is 93−99% across               reasoning requiring entailment verification. Met-
benchmarks, errors concentrated in type misassign-         ric: Accuracy on predicting "Entailed/Contradicto-
ment. A gold-entity study on AR-LSAT lifts con-            ry/Unknown."
sensus by 2.1% and accuracy by 0.7%, indicating               ProofWriter (Tafjord et al., 2021): Synthetic
robustness to extraction noise.                            deductive reasoning. Metric: Proof step accuracy.
                                                              ZebraLogic (Lin et al., 2025): Constraint satis-
Shared hallucinations. Soft verification can fail
                                                           faction puzzles (Einstein’s riddle variants). Metric:
under correlated judge errors. VERGE mitigates
                                                           Exact answer match.
via the variance penalty (Eq. 6), a 0.9 cap on soft
                                                              AR-LSAT (Zhong et al., 2021): Analytical rea-
claim contributions (entailment cannot be overrid-
                                                           soning from LSAT exams. Metric: Multiple-choice
den by consensus), and the joint check (soft claims
                                                           accuracy.
contradicting hard ones are flagged). None of these
eliminates shared hallucinations; we treat this as            BBEH (Kazemi et al., 2025): Big-Bench Ex-
fundamental to any consensus-based verifier.               tra Hard reasoning subset. Metric: Task-specific
                                                           accuracy (varies by sub-task).
Bridges and cross-model consensus. Bridging                   HLE (Phan et al., 2025): Humanity’s Last
axioms are LLM-generated and validated only con-           Exam—diverse reasoning including ethics, physics,
literature (1,200 questions). Metric: Multiple-
choice accuracy.
   All reported numbers are task accuracy against
gold labels, not internal verification scores. S(A)
is used only to decide whether to accept or refine
during iteration.
F    Detailed Verification Trajectories

Case Study 1: AR-LSAT (Temporal Scheduling)

    Problem Context & Question
    Context: Of eight students—George, Helen, Irving, Kyle, Lenore, Nina, Olivia, and Robert—in a seminar, exactly six
    will give individual oral reports during three consecutive days—Monday, Tuesday, and Wednesday. Exactly two reports
    will be given each day—one in the morning and one in the afternoon—according to the following conditions:
        • Tuesday is the only day on which George can give a report.
        • Neither Olivia nor Robert can give an afternoon report.
        • If Nina gives a report, then on the next day Helen and Irving must both give reports...
    Question: If Kyle and Lenore do not give reports, then the morning reports on Monday, Tuesday, and Wednesday,
    respectively, could be given by:
    Options: A) Helen, George, Nina B) Irving, Robert, Helen C) Nina, Helen, Olivia D) Olivia, Robert, Irving
    E) Robert, George, Helen



    Iteration 1 (Failed)
    Generated Answer
          Answer: E) Robert, George, and Helen

    Extracted Claims & Verification Status
     Idx      Claim Text                                    Type                   Status              Score                     Conf
      0       The selected answer is Option E            LOGICAL           CONTRADICTORY                0.00                      0.95
      1       Robert gives the Monday Morning           TEMPORAL                POSSIBLE                0.70                      0.98
              report
      2       George gives the Tuesday Morning          TEMPORAL                POSSIBLE                0.70                      0.95
              report
      3       Helen gives the Wednesday Morning         TEMPORAL                POSSIBLE                0.70                      0.92
              report
      4       Olivia gives an afternoon report           LOGICAL           CONTRADICTORY                0.00                      1.00
              (Implicit)

    Detailed Failure Analysis
          Claim 0 Failure: Constraint Violation

          Issue: Option E assigns slots (Robert, George, Helen) to mornings. Since Kyle and Lenore are out, the remaining slots (Afternoons) must be
          filled by Nina, Irving, Olivia. This forces Olivia into an afternoon slot.

          ; Context Constraint : Neither Olivia nor Robert can give afternoon reports
          ( assert ( not ( exists (( d Day ) ) ( gives_report Olivia d Afternoon ) ) ) )

          ; Claim 0 implies :
          ( assert ( gives_report Robert Monday Morning ) )
          ( assert ( gives_report George Tuesday Morning ) )
          ( assert ( gives_report Helen Wednesday Morning ) )
          ; This leaves Olivia with only Afternoon slots available - > CONTRADICTION

          Z3 Result: unsat
          Unsat Core: [’context_axiom_olivia’, ’claim_0 part 0’]
          Minimal Correction Subset (MCS): Remove (gives_report Robert Monday Morning) OR Remove Option E.


    Metrics (Iteration 1)
     Overall Score:     0.350               Joint Cons: 0.0%                     Entailment: 0.42                     Verified: False




⇓ VERGE Feedback: "Constraint Violation: Olivia forced into Afternoon. MCS: Change Option
                               E or Robert’s slot." ⇓
Iteration 2 (Success)
Refined Answer
      Answer: D) Olivia, Robert, and Irving
      Reasoning: The previous attempt failed because it forced Olivia into an afternoon slot. To
      satisfy the condition "Neither Olivia nor Robert can give an afternoon report," both must
      be assigned to morning slots. Option D places Olivia (Mon AM), Robert (Tue AM), and
      Irving (Wed AM). This leaves valid afternoon slots for the others.

Extracted Claims & Verification Status
 Idx      Claim Text                                        Type               Status           Score                 Conf
  0       The selected answer is Option D                 LOGICAL           ENTAILED            1.00                  0.95
  1       Olivia gives the Monday Morning report        TEMPORAL            POSSIBLE            0.95                  0.99
  2       Robert gives the Tuesday Morning report       TEMPORAL            POSSIBLE            0.95                  0.99
  3       Irving gives the Wednesday Morning            TEMPORAL            POSSIBLE            0.95                  0.99
          report
  4       Constraint on Olivia/Robert is satisfied        LOGICAL           ENTAILED            1.00                  1.00

Verification Success
      Joint Consistency Verified


      ( assert ( gives_report Olivia Monday Morning ) )
      ( assert ( gives_report Robert Tuesday Morning ) )
      ( assert ( gives_report Irving Wednesday Morning ) )

      Z3 Result: sat.
      Entailment Check: The conjunction of these assignments is consistent with all global constraints.


Final Metrics
 Overall Score:     0.965               Joint Cons: 100%                     Entailment: 0.98             Verified:    TRUE
Case Study 2: FOLIO (First-Order Logic)

   Problem Context & Question
   Context:
     1. All guests at the party drink wine or beer. (∀x.Guest(x) => W ine(x) ∨ Beer(x))
     2. If a guest drinks wine, they eat cheese. (∀x.Guest(x) ∧ W ine(x) => Cheese(x))
     3. No one who eats cheese likes fish. (∀x.Cheese(x) => ¬LikesF ish(x))
     4. Alan is a guest. (Guest(Alan))
     5. Alan likes fish. (LikesF ish(Alan))
   Question: Does Alan drink beer?



   Iteration 1 (Hallucination)
   Generated Answer
         No, Alan drinks wine. Since Alan is a guest, he drinks wine or beer. Guests usually drink
         wine with meals, and there is no rule against it.

   Detailed Failure Analysis
         Claim 0: "Alan drinks wine" is Contradictory
         SMT Formalization:
         ( assert ( Drinks Alan Wine ) )


         Constraint Propagation: 1. (Drinks Alan Wine) => (Eats Alan Cheese) [Context
         Axiom 2] 2. (Eats Alan Cheese) => (Not (Likes Alan Fish)) [Context Axiom 3] 3.
         Context Axiom 5 asserts: (Likes Alan Fish) 4. Contradiction: (Likes Alan Fish)
         AND (Not (Likes Alan Fish))
         Z3 Result: unsat.
         Unsat Core: [’Drinks_Alan_Wine’, ’Axiom_2’, ’Axiom_3’, ’Axiom_5’]

   Metrics (Iteration 1)
    Score: 0.000                           Joint Cons: 0.0%                    Verified: False



 ⇓ VERGE Feedback: "Claim ’Alan drinks wine’ causes contradiction with ’Alan likes fish’.
                            MCS: Delete claim." ⇓


   Iteration 2 (Success)
   Refined Answer
         Yes, Alan drinks beer. Reasoning: We know Alan is a guest, so he drinks Wine or Beer. If
         he drank Wine, he would eat Cheese. If he ate Cheese, he would not like Fish. However,
         we know Alan DOES like Fish. Therefore, he cannot drink Wine. Since he must drink
         Wine or Beer, and Wine is impossible, he must drink Beer.

   Extracted Claims & Verification Status
    Idx     Claim Text                         Type        Status      Score                Conf
     0      Alan drinks beer                  LOGICAL    ENTAILED      1.00                 0.98
     1      Alan does not drink wine          LOGICAL    ENTAILED      1.00                 0.98
Verification Success
   Entailment Proof


   ; To prove " Alan drinks Beer " is entailed , we assert its negation and check for UNSAT
   ( push )
   ( assert ( not ( Drinks Alan Beer ) ) )
   ( check-sat ) ; Returns UNSAT - > Proves Entailment
   ( pop )




Final Metrics
 Score:   1.000           Joint Cons: 100%           Entailment: 1.00          Verified:   TRUE
Case Study 3: ZebraLogic (Spatial Relations)

   Problem Context & Question
   Context: Three houses (Red, Blue, Green) are in a row, numbered 1 (left) to 3 (right).
      • The Blue house is immediately to the right of the Red house.
      • The Green house is somewhere to the left of the Blue house.
   Question: What is the order of the houses from left to right?



   Iteration 1 (Inconsistent)
   Generated Answer
         The order is Red, Blue, Green. Reasoning: Red is at 1. Blue is right of Red, so Blue is 2.
         Green is left of Blue, so Green is 3... wait.

   Extracted Claims & Verification Status
    Idx       Claim Text                                   Type                  Status               Score                   Conf
     0        Red is at position 1                      LOGICAL                POSSIBLE                  0.70                  0.90
     1        Blue is at position 2                     LOGICAL                POSSIBLE                  0.70                  0.90
     2        Green is at position 3                    LOGICAL           CONTRADICTORY                  0.00                  0.90

   Detailed Failure Analysis
         Joint Inconsistency

         Issue: Claim 2 (Green=3) contradicts Claim 1 (Blue=2) given the constraint "Green is left of Blue".

         ( declare-fun pos ( House ) Int )
         ( assert (= ( pos Blue ) (+ ( pos Red ) 1) ) )                ; Blue right of Red
         ( assert ( < ( pos Green ) ( pos Blue ) ) )                   ; Green left of Blue

         ; Claims :
         ( assert (= ( pos Blue ) 2) )
         ( assert (= ( pos Green ) 3) )

         ; Check : 3 < 2 ? - > FALSE .

         Z3 Result: unsat.
         Unsat Core: [’Green_Left_Blue_Constraint’, ’Claim_1’, ’Claim_2’]


   Metrics (Iteration 1)
    Score:     0.466                                   Joint Cons: 0.0%                                    Verified: False




⇓ VERGE Feedback: "Constraint violation: Green must be < Blue. Current: 3 < 2 (False)." ⇓
   Iteration 2 (Success)
   Refined Answer
         The order is Green, Red, Blue. Reasoning: 1. Blue is right of Red -> B = R + 1. 2. Green
         is left of Blue -> G < B. Possible values: If R=1, B=2. Then G < 2 implies G=1. But
         houses are distinct, so G cannot be 1. Therefore, Red cannot be 1. Try R=2, B=3. Then G
         < 3 implies G=1 or G=2. Since R=2, G must be 1. Solution: Green(1), Red(2), Blue(3).

   Extracted Claims & Verification Status
    Idx       Claim Text                                        Type             Status          Score                       Conf
     0        Green is at position 1                         LOGICAL          ENTAILED            1.00                       0.95
     1        Red is at position 2                           LOGICAL          ENTAILED            1.00                       0.95
     2        Blue is at position 3                          LOGICAL          ENTAILED            1.00                       0.95
Verification Success
   Entailment Verified


   ( assert (= ( pos Green ) 1) )
   ( assert (= ( pos Red ) 2) )
   ( assert (= ( pos Blue ) 3) )

   Z3 Result: sat. The solution uniquely satisfies all spatial constraints.


Final Metrics
 Score:   1.000                       Joint Cons: 100%                        Entailment: 1.00   Verified:   TRUE
