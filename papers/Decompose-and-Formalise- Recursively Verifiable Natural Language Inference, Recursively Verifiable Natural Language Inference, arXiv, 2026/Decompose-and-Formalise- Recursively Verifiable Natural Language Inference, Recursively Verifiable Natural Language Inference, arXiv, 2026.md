                                                                       Decompose-and-Formalise:
                                                            Recursively Verifiable Natural Language Inference
                                                       Xin Quan1 , Marco Valentino2 , Louise A. Dennis1 , André Freitas1,3,4
                                                           1
                                                             Department of Computer Science, University of Manchester, UK
                                                               2
                                                                 School of Computer Science, University of Sheffield, UK
                                                                          3
                                                                            Idiap Research Institute, Switzerland
                                                       4
                                                         National Biomarker Centre, CRUK-MI, University of Manchester, UK
                                                          xin.quan@manchester.ac.uk m.valentino@sheffield.ac.uk
                                                          louise.dennis@manchester.ac.uk andre.freitas@idiap.ch

                                                                Abstract                                Suchanek, 2025). Recent works in neuro-symbolic
                                                                                                        pipelines offer a principled route to this goal by
                                             Recent work has shown that integrating large
arXiv:2601.19605v1 [cs.CL] 27 Jan 2026




                                                                                                        integrating Large Language Models (LLMs) with
                                             language models (LLMs) with theorem provers
                                             (TPs) in neuro-symbolic pipelines helps with               external theorem provers (TPs): LLMs autofor-
                                             entailment verification and proof-guided refine-           malise natural language statements into formal rep-
                                             ment of explanations for natural language infer-           resentations, and TPs then verify whether premises
                                             ence (NLI). However, scaling such refinement               and explanations entail a hypothesis in the target
                                             to naturalistic NLI remains difficult: long, syn-          logic (Pan et al., 2023; Olausson et al., 2023; Quan
                                             tactically rich inputs and deep multi-step argu-           et al., 2025a; Wu et al., 2022; Xu et al., 2024,
                                             ments amplify autoformalisation errors, where
                                                                                                        2025c; Zhang et al., 2025; Jiang et al., 2024). TP
                                             a single local mismatch can invalidate the proof.
                                             Moreover, current methods often handle fail-
                                                                                                        feedback can further support iterative refinement
                                             ures via costly global regeneration due to the             of both formalisation and explanations (Quan et al.,
                                             difficulty of localising the responsible span or           2024, 2025b; Xu et al., 2025b).
                                             step from prover diagnostics. Aiming to ad-                   Despite the pace of progress, scaling formal re-
                                             dress these problems, we propose a decompose-              finement to naturalistic and complex NLI remains
                                             and-formalise framework that (i) decomposes                an open problem. Real explanations often involve
                                             premise-hypothesis pairs into an entailment                long, syntactically rich sentences and deep multi-
                                             tree of atomic steps, (ii) verifies the tree bottom-
                                                                                                        step arguments that compress many coupled se-
                                             up to isolate failures to specific nodes, and (iii)
                                             performs local diagnostic-guided refinement                mantic commitments into a small surface form.
                                             instead of regenerating the whole explanation.             A single local mismatch (such as a role swap, a
                                             Moreover, to improve faithfulness of autofor-              negation-scope error, or a quantifier mistake) can
                                             malisation, we introduce θ-substitution in an              derail an entire reasoning chain. Moreover, be-
                                             event-based logical form to enforce consistent             cause these errors propagate across steps, end-
                                             argument–role bindings. Across a range of rea-             to-end regeneration and re-proving becomes in-
                                             soning tasks using five LLM backbones, our
                                                                                                        creasingly unstable and costly as chains become
                                             method achieves the highest explanation verifi-
                                             cation rates, improving over the state-of-the-art
                                                                                                        longer and more branched (Pan et al., 2023; Quan
                                             by 26.2%, 21.7%, 21.6% and 48.9%, while re-                et al., 2025b). At the same time, autoformalisa-
                                             ducing refinement iterations and runtime and               tion must be both prover-compatible and semanti-
                                             preserving strong NLI accuracy.                            cally faithful (preserving scope, roles, quantifica-
                                                                                                        tion, and lexical commitments) because even mi-
                                                                                                        nor semantic drift can yield proofs that are syn-
                                         1   Introduction
                                                                                                        tactically valid but misaligned with the original
                                         Natural language explanations are the workhorse                text (Jiang et al., 2024; Xu et al., 2025b; Quan et al.,
                                         of human communication and rationality, yet they               2025b). These bottlenecks foreground three ques-
                                         are frequently incomplete, imprecise, and logi-                tions: RQ1: How can we obtain autoformalisation
                                         cally fragile (Valentino and Freitas, 2024; Valentino          that is both prover-compatible and semantically
                                         et al., 2021). This motivates verifiable Natural Lan-          faithful? RQ2: What kind of verification strategy
                                         guage Inference (NLI) systems that can make the                provides transparent, stepwise verification that pre-
                                         implicit commitments of everyday explanations                  serves multi-step structure and reduces refinement
                                         explicit, and refine them into solver-checkable step-          drift? RQ3: To what extent can local diagnostic-
                                         wise certificates (Quan et al., 2024; Sadeddine and            guided refinement improve efficiency and robust-

                                                                                                    1
                       Premises                                                                       H: Rosa is the daughter of                            (ii) Atomic
 P1: Rosa was born in Santiago.                                                                     someone who is responsible for                        Decomposition
 P2: Santiago is the capital and largest city of Chile.                                                the oversight of traffic.
 P3: Rosa is the daughter of a Catalan building
contractor, Jose.                                                                                      IC: Rosa is the daughter of
                                                                    (i) Tree                                                                  Atom 1: Rosa is the daughter of a person.
 P4: Jose has a Chilean wife, Carmen.                                                               someone who is responsible for
 P5: A building contractor is responsible for the day-            Construction                                                                Atom 2: The person is responsible for the
                                                                                                     the oversight of a construction          oversight of a construction site.
to-day oversight of a construction site.                                                                           site.
                     Hypothesis                                                                                                              Atom 1: A building contractor is responsible
H: Rosa is the daughter of someone who is                                                                                                    for the day-to-day oversight.
responsible for the oversight of traffic.                                                                     Intermediate                   Atom 2: The oversight is of a construction
                                                                                                               Conclusion
                                                                                                                                             site.
                                                                                                     P3            (IC)        P5
                                                                                                                                             Atom 3: The oversight occurs on a day-to-day
                    H                                                       Valid Entailment                                                 basis.
                                                                            Invalid Entailment

             IC         New Premise 2
                                                                                                                (iv) Recursive
                                                                                                                                                      (iii) Theta-Substitution
                                                                                                               Verification and
    P3         P5       New Premise 1                                                                                                                    Autoformalisation
                                                                                                                  Refinement




                                                             IC                    IC                                                  Atom 1: ∃x y.Rosa(x)∧DaughterOf(x,y) ∧ Person(y)
                    H                   H                                                                                        IC    ...


                                                                                                                                       Atom 1: ∃x e.(Contractor(x)∧ResponsibleFor(e
              IC                        IC            P3     P5              P3          P5                                      P5    )∧Agent(e,x)∧Oversight(e)∧OccursOnDailyBasis(e))
                                                                                                                                       ...
New Premise 2: Anyone who is responsible for the
oversight of a construction site is also responsible for                                                                               Atom 1: ∃x y.Rosa(x)∧DaughterOf(x,y) ∧ Jose(y)
                                                           New Premise 1: Jose is a person.                                      P3    ...
the oversight of traffic.

Figure 1: An illustration of the proposed framework for recursively verifiable natural language inference (NLI)
via entailment trees, atomic decomposition, and θ-substitution autoformalisation. The entailment tree is initially
constructed from the given premises and hypothesis, including intermediate conclusions. Each sentence is then
decomposed into atomic propositions and autoformalised into logical forms. By utilising an external theorem prover,
we progressively verify and refine each subtree until the final hypothesis node is reached. The reasoning chain is
considered logically sound and coherent once the entire entailment tree has been fully verified and refined.


ness without sacrificing end-task accuracy?                                                           We evaluate LLM-TP Tree on FOLIO,
   To address these challenges, we propose LLM-                                                    ProofWriter, PrOntoQA, and EntailmentBank
TP Tree, a scalable decompose-and-formalise                                                        using five LLM backbones (GPT-4o, GPT-5 nano,
framework built around an entailment-tree view                                                     Grok-4-fast, Deepseek-V3.1 and Qwen3-Max).
of explanations. The core idea is to replace holis-                                                We compare against state-of-the-art baselines
tic refinement with structured decomposition and                                                   including Explanation-Refiner (Quan et al.,
local repair. Concretely, LLM-TP Tree (i) decom-                                                   2024), Faithful-Refiner (Quan et al., 2025b),
poses each premise–hypothesis instance into an                                                     LINC (Olausson et al., 2023), and Logic-LM (Pan
entailment tree of atomic steps, (ii) verifies the                                                 et al., 2023). Across datasets, our approach
tree bottom-up to isolate proof failures to specific                                               achieves the strongest refinement performance,
nodes, and (iii) performs local diagnostic-guided                                                  improving the average verification rate by 26.2%,
refinement on the failing nodes rather than regen-                                                 21.7%, 21.6%, and 48.9% points on FOLIO,
erating the entire explanation. This design makes                                                  ProofWriter, PrOntoQA, and EntailmentBank,
semantic preservation controllable at the smallest                                                 respectively, while reducing refinement iterations
meaningful granularity, stabilises refinement under                                                and runtime and maintaining strong NLI accuracy.
longer-horizon reasoning, and improves efficiency                                                  In summary, our contributions are:
by focusing computation where proofs actually
                                                                                                     1. We introduce LLM-TP Tree, a recursive
fail. To improve faithfulness in autoformalisation,
                                                                                                        entailment-tree framework that verifies and
we introduce a θ-substitution procedure within an
                                                                                                        refines multi-step inference chains for verifi-
event-based logical form that enforces consistent
                                                                                                        able NLI via bottom-up checking and local
argument-role bindings during autoformalisation,
                                                                                                        repair.
making role commitments explicit and systemati-
cally repairable. Together, atomic decomposition,                                                    2. We propose atomic decomposition, which
recursive bottom-up verification, and θ-substitution                                                    decomposes complex sentences into atomic
yield prover-compatible theories that better track                                                      propositions and reduces inference-time by
the intended semantics of the original text while                                                       16.5%, 13.7%, 21.1%, and 10.1% across
enabling targeted refinement.                                                                           datasets compared to baseline neuro-symbolic

                                                                                               2
      frameworks.                                               directed edges encoding entailment dependencies.
                                                                For each internal node v ∈ Ti with proposition
    3. We propose a θ-substitution autoformalisation            φv and descendant nodes D(v), the corresponding
       procedure that enforces consistent argument-             local entailment obligation requires that the con-
       role bindings and improves autoformalisation             junction  of descendants entails the parent, namely
       faithfulness by 0.09, 0.106, 0.128, and 0.21             V
                                                                   u∈D(v) φu |= φv . The prompt of the entailment
       on average over baseline models.                         tree construction is in Appendix J.
    4. We conduct comprehensive automatic and hu-               3.2   Atomic Decomposition
       man evaluations with ablations, showing that
                                                                Sentence complexity is a major contributor to both
       LLM-TP Tree substantially improves the ro-
                                                                the latency and the brittleness of autoformalisation
       bustness and efficiency of LLM-TP explana-
                                                                (Quan et al., 2025b). Long and structurally com-
       tion refinement while preserving strong logi-
                                                                plex sentences tend to increase the search space of
       cal reasoning performance.
                                                                the translation process, which not only slows down
2     Recursively Verifiable NLI                                inference but also amplifies semantic inconsisten-
                                                                cies in the resulting logical forms. To mitigate these
In this work, we define an NLI instance i with a                issues, we then decompose each natural language
premise set Pi = {p1 , p2 , . . . , pn } and a hypoth-          proposition into a set of atomic propositions, so
esis hi to be formally verifiable if the entailment             that the subsequent autoformalisation operates on
condition can be verified by a theorem prover. Let              shorter, semantically focused units.
Φ : NL → L translate natural language sentences                    After constructing the entailment reasoning tree,
into a target logic L, and let S be a solver for                we apply atomic decomposition to the propositions
L. The NLI instance i is labelled as entailment                 (first subtree) that participate in proof obligations.
if S(Φ(Pi ) ⊢ Φ(hi )) is provable, and as contradic-            For the hypothesis hi , we generate a set of atoms
tion if S(Φ(Pi ) ⊢ ¬Φ(hi )) is provable.
   Formal verifiability certifies only the endpoint                                                                k
                                                                                                                   ^
relation between Pi and hi . We call an instance                  D(hi ) = {ah1 , ah2 , . . . , ahk },      hi ≡         ahℓ .
recursively verifiable if there exists an explicit in-                                                             ℓ=1
                                                                                                                     (1)
ference chain Π = ⟨δ1 , δ2 , . . . , δk ⟩ whose interme-
                                                                  Similarly, for the premise set Pi = {p1 , . . . , pn },
diate steps are individually solver-checkable and
                                                                each premise pj is decomposed into
compose to hi . Let Π<j = ⟨δ1 , . . . , δj−1 ⟩ denote
the prefix before step j. Then Π is a recursively ver-
                                                                                                                   tj
                 for all j ∈ {1, . . . , k}, S Φ(Pi ∪
ifiable witness if,                                                         p     p             p
                                                                                                                   ^        p
   <j
Π ) ⊢ Φ(δj ) is provable, and S Φ(Pi ∪ Π) ⊢                     D(pj ) = {a1j , a2j , . . . , atjj },      pj ≡          aℓ j .
Φ(hi ) is provable.                                                                                                ℓ=1
                                                                                                            (2)
3     Methodology                                                 We define the global atom set induced by the
                                                                premises as
To enable faithful formal checking of multi-step
reasoning chains and to refine them when proof                                  n
obligations are not discharged, we propose LLM-
                                                                                [                             ^
                                                                  D(Pi ) :=           D(pj ),        Pi ≡              a. (3)
TP Tree, a neuro symbolic framework for recur-                                  j=1                         a∈D(Pi )
sively verifiable NLI based on an entailment rea-
soning tree Ti . Figure 1 provides an overview.                 Entailment-preserving requirement. We re-
                                                                quire the decomposition operator D(·) to be
3.1    Entailment Tree Construction                             entailment-preserving: for any sentence φ and any
Given a premise set Pi and a hypothesis hi , we                 atom a ∈ D(φ), it must hold that φ ⊨ a. In-
first prompt an LLM to construct an entailment                  tuitively, each atom is a logically entailed con-
tree and a set of intermediate conclusions C =                  sequence of the original sentence, so decompo-
{δ1 , δ2 , . . . , δm }, optionally selecting a subset of       sition does not introduce new information that is
premises Pi′ ⊆ Pi , such that Pi′ ∪ C |= hi holds.              not supported by the source. We obtain candidate
The tree Ti consists of nodes labelled by proposi-              atoms by prompting an LLM (see Appendix I).
tions (premises or intermediate conclusions) and                To enforce the entailment-preserving requirement

                                                            3
in practice, we apply a pretrained NLI classifier                Example 2 illustrates the resulting stepwise
(roberta-large-mnli (Liu et al., 2019)) to verify              derivation in detail.
that each atom is entailed by its source sentence
within a predefined threshold (0.9). This filtering            3.4   Entailment tree verification and
step reduces invalid decompositions and improves                     refinement for recursively verifiable NLI
the stability of downstream autoformalisation.                 Finally, given an entailment tree T , we verify
                                                               it recursively by turning each subtree into a set
3.3   θ-substitution Autoformalisation                         of local proof obligations that are checkable by
Existing autoformalisation pipelines (Pan et al.,              a TP. Each node n ∈ T stores a natural lan-
2023; Olausson et al., 2023) often rely on complex,            guage statement sn , its atomic decomposition
monolithic generation procedures to map natural                D(n) = {an1 , an2 , . . . , an|D(n)| }, and a role indi-
language sentences into fully specified logical for-           cator ρ(n) ∈ {EXPLANATION, HYPOTHESIS} that
mulas. This design is computationally inefficient              is defined with respect to the current subtree un-
and, more importantly, prone to systematic errors              der verification. For a subtree Tsub ⊆ T with root
that frequently prevent theorem provers from cer-              h = root(Tsub ) and leaf set E = leaves(Tsub ), we
tifying entailment. These observations motivate                set
a more structured autoformalisation strategy that                           (
decomposes the translation into smaller, verifiable                           EXPLANATION if n ∈ E,
                                                                    ρ(n) =                                         (12)
steps and reduces sensitivity to surface linguistic                           HYPOTHESIS           if n = h.
variation.
   We then adopt the Neo-Davidsonian event se-                 From atoms to axioms and lemmas. Let Φ
mantics formulation used in Quan et al. (2024),                denote autoformalisation from natural language
where events and semantic roles (e.g., agent, pa-              atoms to the target logic. For every explanation
tient) are represented explicitly in first-order logic         node e ∈ E, each atom a ∈ D(e) is translated
to autoformalise the decomposed atomic proposi-                into an Isabelle/HOL (Nipkow et al., 2002) axiom
tions in previous step to logical forms. Building              (example in Appendix D):
on this representation, we propose a multi-step θ-
substitution procedure that constructs the final logi-                         axiom(e, a) : Φ(a).                (13)
cal form by progressively instantiating an abstract
                                                               Collecting all explanation atoms yields the axiom
template (see Example 2).
                                                               set
   A substitution θ is a mapping from placeholders
to terms:
                                                                                [
                                                                    A(E) :=         {Φ(a) | a ∈ D(e)}.       (14)
                                                                                 e∈E
  θ = {x1 7→ t1 , x2 7→ t2 , . . . , xn 7→ tn }.    (9)
                                                               For the hypothesis node h, each atom a ∈ D(h)
   Applying θ to a formula φ, denoted φ[θ], re-                induces a local proof obligation:
places each placeholder xi with its corresponding
term ti .                                                                lemma(h, a) : A(E) ⊢ Φ(a).               (15)
   For a natural language sentence, we start from
an abstract logical template and apply a sequence              We accept h as verified for the current subtree if
of substitutions:                                              TP certifies lemma(h, a) for all atoms a ∈ D(h).
                θ        θ       θ
                1
            φ0 −→     2
                  φ1 −→     3
                        φ2 −→ φfinal .             (10)        Recursive verification with localized refinement.
                                                               The verification proceeds bottom-up. Intuitively,
   Each substitution handles a specific aspect: 1)
                                                               once a subtree root is verified, it can be treated as a
Entity substitution (θ1 ): maps generic predicates
                                                               support statement for its parent level. Algorithm 1
to specific entities 2) Event substitution (θ2 ): intro-
                                                               summarises the procedure.
duces event predicates and event structure. 3) Role
                                                                 When T P cannot discharge a lemma
substitution (θ3 ): adds Neo-Davidsonian semantic
                                                               lemma(h, a) for some atom a ∈ D(h), we
roles and their arguments.
                                                               extract diagnostics from the prover (e.g., the failed
   The final formula is obtained by composing the
                                                               goal and relevant constraints) and use them to
substitutions:
                                                               localise the failure to a small set of implicated
              φfinal = φ0 [θ1 ◦ θ2 ◦ θ3 ].         (11)        explanation nodes E. b We then prompt an LLM

                                                           4
 Example 3.1: θ-substitution Autoformalisation
 Sentence: A forest fire would cause deer to die or leave a woodland.
 Logic Template Generation:
                                                    φ0 = ∀x y z. P (x) ∧ Q(y) ∧ R(z) → S                                     (4)

 Step 1: Entity Substitution (Apply θ1 = {P/ForestFire, Q/Deer, R/Woodland}):

                                    φ1 = φ0 [θ1 ] = ∀x y z. ForestFire(x) ∧ Deer(y) ∧ Woodland(z) → S                        (5)

 Step 2: Event Substitution (Apply θ2 = {S/(Die(e1 ) ∨ Leave(e2 ))}):

                         φ2 = φ1 [θ2 ] = ∀x y z. ForestFire(x) ∧ Deer(y) ∧ Woodland(z) → (Die(e1 ) ∨ Leave(e2 ))             (6)

 Step 3: Semantic Role Substitution (Apply θ3 ):
                                            (
                                             Die(e1 ) 7→ (Die(e1 ) ∧ Agent(e1 , y))
                                     θ3 =                                                                                    (7)
                                             Leave(e2 ) 7→ (Leave(e2 ) ∧ Agent(e2 , y) ∧ Patient(e2 , z))

 Final Result:

                               φfinal = φ2 [θ3 ] = ∀x y z e1 e2 . ForestFire(x) ∧ Deer(y) ∧ Woodland(z) →
                                                                                                                             (8)
                                      (Die(e1 ) ∧ Agent(e1 , y)) ∨ (Leave(e2 ) ∧ Agent(e2 , y) ∧ Patient(e2 , z))


                                       Figure 2: θ-substitution autoformalisation example.


to refine only these implicated nodes, update                               including a direct standard prompting and chain-of-
the subtree accordingly, and re-check the same                              thought (CoT) prompting. In addition, we com-
local obligations. This loop continues until all                            pare against two representative neuro-symbolic
atoms in D(h) are certified for the subtree root h,                         frameworks, Logic-LM (Pan et al., 2023) and
after which the verified root is promoted and the                           LINC (Olausson et al., 2023). We evaluate five dis-
algorithm proceeds to higher levels. Repeating this                         tinct LLM backbones, spanning a general-purpose
process bottom-up yields a recursively verifiable                           chat model (GPT-4o (OpenAI, 2024)), models eval-
proof certificate for the entire entailment tree.                           uated in non-thinking mode (GPT-5 Nano (OpenAI,
                                                                            2025), Grok-4 Fast (xAI, 2025)), and models evalu-
4    Experimental Setup                                                     ated in thinking mode (DeepSeek-V3.1 (Deepseek-
                                                                            AI, 2025), Qwen3-Max (Qwen Team, 2025)) and
We evaluate our neuro-symbolic framework from
                                                                            additionally include GPT-3.5 in logical reasoning
two complementary perspectives: (i) explanation
                                                                            tasks to match the model coverage reported in prior
refinement apply theorem-prover checking and re-
                                                                            work. LLM implementation details is described in
fine the explanation; and (ii) logical reasoning,
                                                                            Appendix D.
which measures standard end-task accuracy to en-
sure that enhanced verification and refinement do
                                                                            5    Empirical Results and Evaluation
not come at the cost of predictive performance.
Datasets We use four datasets ranging from                                  LLM-TP Tree effectively verifies and refines ex-
synthetically generated deductive reasoning                                 planations for NLI. Table 1 reports the main
benchmarks to expert-written real-world corpora:                            results on the explanation refinement task. Across
ProofWriter (Tafjord et al., 2021), PrOn-                                   all datasets and all LLM backbones, LLM-TP
toQA (Saparov and He, 2023), FOLIO (Han et al.,                             Tree achieves the best final refinement perfor-
2024), and EntailmentBank (Dalvi et al., 2021).                             mance (Fin.), indicating that it is consistently more
Additional dataset details (i.e. number of samples)                         effective at producing a checkable witness for
are provided in Appendix A.                                                 explanation-based NLI. Averaged over backbone
                                                                            LLMs, LLM-TP Tree improves the final verified
Baselines and Models For explanation refine-                                rate by 26.23%, 21.73%, 21.60%, and 48.93%
ment, we compare against two state-of-the-                                  on each dataset compared to Explanation-Refiner.
art explanation refinement models, Explanation-                             The effect is most pronounced on EntailmentBank:
Refiner (Quan et al., 2024) and Faithful-                                   while holistic refiners remain below 52% final va-
Refiner (Quan et al., 2025b). For logical reason-                           lidity, LLM-TP Tree reaches 68.67–78.67% across
ing, we consider two prompting-based baselines,                             backbones. Beyond final refinement quality, the

                                                                        5
                                                 GPT-4o    GPT-5 nano Grok-4 fast Deepseek-V3.1 Qwen3-max
       Dataset             Approach
                                                Init. Fin. Init.   Fin.   Init. Fin. Init.    Fin.     Init.   Fin.
                           Explanation-Refiner 53.28 63.93 46.72 59.84 45.08 52.46 50.82      62.30    55.74 68.85
                           Faithful-Refiner    68.03 78.69 53.28 68.03 54.92 65.57 71.31      81.15    69.67 84.43
        FOLIO                                        90.16        81.15        79.51          92.62          95.08
                           LLM-TP Tree         81.15 ↑26.23 66.39 ↑21.31 62.30 ↑27.05 83.61   ↑30.32   85.25 ↑26.23
                           Explanation-Refiner 62.67 76.67 59.33 73.33 53.33 69.33 52.67      66.67    64.00 78.00
                           Faithful-Refiner    80.00 86.67 72.00 84.67 60.00 78.67 83.33      90.67    84.00 91.33
        ProofWriter                                  95.33        91.33        90.00          98.00          98.00
                           LLM-TP Tree         91.33 ↑18.66 85.33 ↑18.00 72.67 ↑20.67 91.33   ↑31.33   92.00 ↑20.00
                           Explanation-Refiner 64.00 78.67 60.00 74.67 61.33 73.33 62.00 74.00 64.67 78.00
                           Faithful-Refiner    82.67 90.00 73.33 80.00 72.00 84.00 85.33 91.33 82.00 91.33
        PrOntoQA                                     97.33        98.00        91.33        100.00      100.00
                           LLM-TP Tree         92.00 ↑18.66 93.33 ↑23.33 86.00 ↑18.00 97.33 ↑26.00 98.00 ↑22.00
                       Explanation-Refiner 15.33 26.67 12.00 23.33 8.67 13.33 15.33           26.67    16.67 28.00
                       Faithful-Refiner    23.33 44.00 17.33 47.33 14.00 46.00 25.33          48.00    22.00 52.00
        EntailmentBank                           70.00        74.00        68.67              71.33          78.67
                       LLM-TP Tree         21.33 ↑43.33 18.00 ↑50.67 16.67 ↑55.34 22.00       ↑44.66   22.67 ↑50.67

Table 1: Comparison results on the explanation refinement tasks. Init. shows the number of explanation that is
initially logically valid. Fin. shows the number of explanation that is finally logically valid after refinement. Bold
values indicate the best performance. Arrows indicate absolute performance gain of LLM-TP Tree over the baseline.


    Dataset           ER      FR      LT   LT w/o AD            shown in Table 2. Across all four datasets (FOLIO,
    FOLIO             4.27   3.75   3.04       3.57             ProofWriter, PrOntoQA, and EntailmentBank), LT
    ProofWriter       3.47   3.08   2.42       2.88             converges in fewer iterations than baseline refin-
    PrOntoQA          3.36   2.73   2.04       2.44             ers, reducing the required iterations by an aver-
    EntailmentBank    4.97   4.46   4.04       4.35
                                                                age of 1.14 relative to ER and by an average of
    Avg.              4.02   3.51   2.88       3.31             0.63 relative to Faithful-Refiner (FR). To isolate
                                                                the advantages of atomic decomposition, we run
Table 2: Average refinement iterations required aver-
                                                                an ablation that disables atomic sentence splitting.
aged over five LLM backbones. Comparison between
ER (Explanation-Refiner), FR (Faithful-Refiner), LT             Relative to the full LT system, removing atomic
(LLM-TP Tree) and LT w/o AD (LT without atomic                  decomposition increases the number of required
decomposition)                                                  refinement iterations by between 0.31 and 0.53
                                                                . This ablation indicates that atomic decomposi-
                                                                tion contributes materially to LT’s efficiency gains:
Init. column probes whether a backbone can pro-                 by splitting premises and intermediate conclusions
duce an initially provable explanatory chain be-                into atomic subclaims, verification failures can be
fore any refinement cycle. On synthetic bench-                  localised to a small set of fine-grained hypotheses,
marks such as ProofWriter and PrOntoQA, LLM-                    enabling targeted repairs of the minimal logical
TP Tree yields substantially higher initial validity            mismatch and thereby reducing both the number
than holistic refiners; for instance, on ProofWriter            of refinement iterations and the cost of each veri-
with Qwen3-max, LLM-TP Tree attains 92.00%                      fication/refinement pass. We also report the mean
Init. versus 64.00% for Explanation-Refiner. No-                running time per refinement iteration (including
tably, EntailmentBank exhibits low initial valid-               theorem-proving time) under different LLM back-
ity across methods, suggesting that constructing                bones, and provide the full per-backbone iteration
globally coherent verifiable chains is difficult un-            results in Appendix F.
der more realistic multi-hop explanations. In this
regime, our proposed mechanism yields the largest
gains after refinement.                                         Multi-step θ-substitution autoformalisation im-
                                                                proves semantic faithfulness. A faithful auto-
Atomic decomposition improves the efficiency                    formalisation should preserve the semantic content
of verification-driven explanation refinement.                  of the original sentence as much as possible. Fol-
We report the average number of refinement itera-               lowing the rule-based informalisation procedure by
tions, averaged across different LLM backbones,                 Quan et al. (2025b), we quantify faithfulness by
required to refine an explanation for each dataset, as          converting each predicted logical form back into

                                                            6
                                        Syntax          Implication         Quantifier            Variable                                                           Syntax          Implication        Quantifier          Variable                                                                      Syntax        Implication          Quantifier        Variable                                                                 Syntax          Implication               Quantifier                Variable
                 40                                                                                                                          40                                                                                                                           40                                                                                                                           40
                                                                                                                                                                                                                                                                                                                                                                                                                                       37.0

                 35                                                                                                                          35                                                                                                                           35                                                                                                                           35                       33.0                                 33.5


                 30                                                                                                                          30                                                                                                                           30                                                                                                                           30                                                                                                                       28.5
Percentage (%)




                                                                                                                            Percentage (%)




                                                                                                                                                                                                                                                         Percentage (%)




                                                                                                                                                                                                                                                                                                                                                                                      Percentage (%)
                                                                                                                                                                                                                                                                                                                                                                                                                         26.0
                 25                                                                                                                          25                                                                                                                           25                                                                                                                           25         24.2
                                                                                                                                                                                                                                                                                                                                                                                                                                                              23.0                                                       22.5

                 20                18.0 17.5
                                                                                                                                             20                                                                                                                           20                                                                                                                           20

                 15                                                14.0                                                                      15                                                                                                                           15                                                                                                                           15
                                                                                                                   11.0                                                                                                                                                                                                                                                                                                                                11.5
                      10.2                                                                                                                                    10.0                                                                                                                                  9.5
                 10          8.5                             8.0
                                                                                                                                             10                                                                                                                           10                                                                                                                           10                                        8.1                                                               8.5

                                                       5.5                                                   6.0                                                                                                                                                                              5.5                                                                                                                                                                                                            5.4
                                                                                                                                                                     4.5                  5.0                                            4.5                                                                                 5.0                                                                                                                                                      5.0
                  5                              4.1
                                                                                      3.0          3.4 4.0                                    5   4.2
                                                                                                                                                        3.5                                                                                                                5            3.8               3.5                                                             4.0                           5                                                                       3.6         3.0
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  4.0
                                                                                                                                                                              2.4               2.5             2.0          2.3               2.5                                                                                 2.5                                          2.0
                                                                          1.2                                                                                                       1.5                                            1.5                                                                             1.3 1.5                                      1.1 1.5
                                                                                0.0         0.0                                                                                                       0.0 0.0         0.0                                                                                                                0.0 0.0 0.0 0.0
                  0                                                                                                                           0                                                                                                                            0                                                                                                                            0
                              ER                        FR                        LT               LT w/o sub.                                           ER                          FR                     LT               LT w/o sub.                                                       ER                       FR                      LT              LT w/o sub.                                                ER                            FR                             LT                   LT w/o sub.




                                               (a) FOLIO                                                                                                         (b) ProofWriter                                                                                                                          (c) PrOntoQA                                                                                                   (d) EntailmentBank
Figure 3: Distribution of the autoformlisation errors (syntax, implication, quantifier, variable in Isabelle/HOL
Theories.


                                                                                                                                                                                                                                                                                    5                 Ideal (y=x)                                                                                             5                   Ideal (y=x)
                  Dataset                                                                         ER                       FR                                   LT                              LT w/o sub.                                                                                           ER band
                                                                                                                                                                                                                                                                                                      ER mean
                                                                                                                                                                                                                                                                                                                                                                                                                                  ER band
                                                                                                                                                                                                                                                                                                                                                                                                                                  ER mean




                                                                                                                                                                                                                                                                     Used Proof Depth




                                                                                                                                                                                                                                                                                                                                                                                               Used Proof Depth
                                                                                                                                                                                                                                                                                    4                 FR band                                                                                                 4                   FR band
                                                                                                                                                                                                                                                                                                      FR mean                                                                                                                     FR mean
                  FOLIO                                                                     0.766                         0.822                          0.856                                        0.828                                                                         3
                                                                                                                                                                                                                                                                                                      LT band
                                                                                                                                                                                                                                                                                                      LT mean                                                                                                 3
                                                                                                                                                                                                                                                                                                                                                                                                                                  LT band
                                                                                                                                                                                                                                                                                                                                                                                                                                  LT mean
                  ProofWriter                                                               0.834                         0.892                          0.940                                        0.914                                                                         2                                                                                                                         2
                  PrOntoQA                                                                  0.824                         0.918                          0.952                                        0.924                                                                         1                                                                                                                         1
                  EntailmentBank                                                            0.614                         0.726                          0.824                                        0.770
                                                                                                                                                                                                                                                                                    0 1                             2                    3                 4                      5                           0 1                                2                          3                           4                         5
                                                                                                                                                                                                                                                                                                                              Gold Depth                                                                                                                       Gold Depth
                  Avg.                                                                      0.760                         0.840                          0.893                                        0.859
                                                                                                                                                                                                                                                                                   (a) ProofWriter - Refined                                                                                      (b) EntailmentBank - Refined
Table 3: Average autoformalisation faithfulness (cosine                                                                                                                                                                                                                             5                 Ideal (y=x)
                                                                                                                                                                                                                                                                                                      ER band
                                                                                                                                                                                                                                                                                                                                                                                                              5                   Ideal (y=x)
                                                                                                                                                                                                                                                                                                                                                                                                                                  ER band
                                                                                                                                                                                                                                                                                                      ER mean                                                                                                                     ER mean
                                                                                                                                                                                                                                                                     Used Proof Depth




                                                                                                                                                                                                                                                                                                                                                                                               Used Proof Depth
similarity) averaged over five LLM backbones. Compar-                                                                                                                                                                                                                               4                 FR band                                                                                                 4                   FR band
                                                                                                                                                                                                                                                                                                      FR mean                                                                                                                     FR mean
                                                                                                                                                                                                                                                                                                      LT band                                                                                                                     LT band
ison between ER (Explanation-Refiner), FR (Faithful-                                                                                                                                                                                                                                3                 LT mean                                                                                                 3                   LT mean

Refiner), LT (LLM-TP Tree) and LT w/o sub. (LT with-                                                                                                                                                                                                                                2                                                                                                                         2
                                                                                                                                                                                                                                                                                    1                                                                                                                         1
out θ-substitution autoformalisation).
                                                                                                                                                                                                                                                                                    0 1                             2                    3                 4                      5                           0 1                                2                          3                           4                         5
                                                                                                                                                                                                                                                                                                                              Gold Depth                                                                                                                       Gold Depth

natural language and computing the cosine simi-                                                                                                                                                                                                                             (c) ProofWriter - Unrefined                                                                                           (d) EntailmentBank - Unre-
                                                                                                                                                                                                                                                                                                                                                                                                  fined
larity between the informalised sentence and the
                                                                                                                                                                                                                                                                          Figure 4: Proof depth alignment between gold and ac-
original sentence. Table 3 summarises the results.                                                                                                                                                                                                                        tual constructed proof depths across frameworks. The
Our approach achieves the highest average faithful-                                                                                                                                                                                                                       solid curve shows the mean used depth averaged over
ness across all datasets, outperforming Explanation-                                                                                                                                                                                                                      five LLMs, while the shaded band shows the range
Refiner by an average of 0.13 and Faithful-Refiner                                                                                                                                                                                                                        across backbones. Top: Trends in refined cases. Bottom:
by an average of 0.053. As expected, faithful-                                                                                                                                                                                                                            Trends in unrefined cases.
ness is generally higher on synthetic benchmarks,
whose language more closely follows rule-based
templates, whereas EntailmentBank is more chal-                                                                                                                                                                                                                           depth compression: the used depth grows slowly,
lenging due to its more naturalistic multi-hop ex-                                                                                                                                                                                                                        saturates, or even decreases, increasingly under-
planations. Notably, our method yields the largest                                                                                                                                                                                                                        shooting the gold depth. This indicates that holistic
margin on EntailmentBank, indicating stronger ro-                                                                                                                                                                                                                         refiners tend to collapse longer multi-step expla-
bustness of θ-substitution autoformalisation under                                                                                                                                                                                                                        nations into shorter proofs. In contrast, LLM-TP
distributional and linguistic variability. We further                                                                                                                                                                                                                     Tree tracks the gold depth much more closely sug-
perform an ablation by removing θ-substitution (LT                                                                                                                                                                                                                        gesting that its refinement process better preserves
w/o sub.). This variant shows a consistent drop in                                                                                                                                                                                                                        proof-step granularity in longer-horizon inference.
similarity of an average of 0.034 across the same                                                                                                                                                                                                                         Detailed distributions are provided in Appendix H.
datasets compared to the full model. We also shows                                                                                                                                                                                                                        We further analyse autoformalisation failures by
the full ablation study results in Appendix E                                                                                                                                                                                                                             categorising errors in the generated Isabelle/HOL
                                                                                                                                                                                                                                                                          theories into four types (details in Appendix B)
5.1                                 Failure and Error Analysis                                                                                                                                                                                                            across 200 sampled theories. Figure 3 shows that
We analyse refinement drift using proof-depth                                                                                                                                                                                                                             LLM-TP Tree consistently yields the lowest error
alignment. Figure 4 measure proof-depth align-                                                                                                                                                                                                                            rates across datasets, with the largest margin on the
ment by comparing the TP-extracted used proof                                                                                                                                                                                                                             more naturalistic EntailmentBank. Removing θ-
depth of each explanation with the dataset-provided                                                                                                                                                                                                                       substitution (LT w/o sub.) leads to a clear increase
gold depth (ideal y=x). In refined cases, all frame-                                                                                                                                                                                                                      in semantic and structural errors, particularly quan-
works show a positive trend that is close to the ideal                                                                                                                                                                                                                    tifier and variable errors on EntailmentBank, high-
y=x line. By contrast, in unrefined cases, ER and                                                                                                                                                                                                                         lighting the importance of staged substitution auto-
FR exhibit a clear refinement drift in the form of                                                                                                                                                                                                                        formalisation for maintaining a prover-compatible

                                                                                                                                                                                                                                                     7
                                                        Standard                            CoT                             Logic-LM                           LINC                       LLM-TP                                                                                            Standard                         CoT                             Logic-LM                         LINC                     LLM-TP                                                                                            Standard                            CoT                             Logic-LM                             LINC                      LLM-TP

               100                                                                                                                                                                                                                                 100                                                                                                                                                                                                                          100
                                                                                                                                                                                                                                                                                            100.0100.0                                                                                                                 99.6                                                                                              100.0100.0                        100.0100.0                                                              100.0100.0                             99.5
                                                                                                                                                                                                                                                                                     98.7                            98.7                                                                      98.7 98.7                                                                                     99.0                                                                                                     98.5                                             98.5 98.5
                                                                                                                                                                                                                                                                                                                                                                                       97.8                                                                                                                                                                                                                                97.5
                                                                                                                                                                                                                                                                                                                            95.6                                                                                                                                                                                  96.0                                                                                       95.5                               96.0
                                                                                                                                                                                                                                                                              95.1                                                                                                                                                                                                                                                                                                    95.0
                                                                                                                                                                                          94.0                                                                                                                                                        93.8                                                                                                                                                                                                                                                                                                                              93.5
                                                                                                                                                                                                                                                                                                                                   92.9                                                                                                                                                                                                             92.5                                                            92.5
                                                                                                                                                                              91.8 91.8                                                                                                                                                                                                                                                            92.0                                                    92.0                                                                                                                                                                  92.0
                                                                                                                                                                                                                                                                       91.1                                                                                                                                                                                                           91.0                                                                                     91.0
                                                                                                                                                                                                                                                                                                                                                                      90.2 90.2 90.7                       90.0 90.2                                                                                                                         90.0
                                                                                                                                                                                                                                                                                                                                          88.9 89.3            89.3                                                                                       89.3                                      88.5                                                                                       89.0
                                                 87.4                                                                                                   87.9           87.9                                                                                                                              88.0 88.4
                                          86.3                                                                                                   86.3           86.8                                                                                                                                                                                                                                                                                                                                                                                                    87.0
                                                                                                                                          85.2                                                                                                                                                                                                                                                                                                                                                                                        85.5
                                   84.1                                                    84.1 84.6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               84.0



                80                                                                                                                                                                                                                                  80
                                                                                                                                                                                                                                                                                                                                                                                                                                     80.9

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 80
                                                                                    79.7                                                                                                                              80.2
                                                        79.1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   78.5
                                                                                                                                                                                                                                                                                                                                                                                                                                            77.7
                                                               75.8                                                  75.8
                                                                      74.7                                                                                                                              74.7
                                                                                                              73.1                                                                                             73.1
Accuracy (%)




                                                                                                                                                                                                                                    Accuracy (%)




                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Accuracy (%)
                                                                                                       72.0
                                                                             70.9
                                                                                                                                                                                                 69.8                        69.2
                            67.6                                                                                              67.0 67.0

                     63.2


                60                                                                                                                                                                                                                                  60          55.1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 60
                                                                                                                                                                                                                                                         52.4




                                                                                                                                                                                                                                                                                                                                                                                                                              44.0



                40                                                                                                                                                                                                                                  40                                                                                                                                                                                                                           40


                20                                                                                                                                                                                                                                  20                                                                                                                                                                                                                           20


                 0                                                                                                                                                                                                                                   0                                                                                                                                                                                                                            0
                            GPT-4o                      GPT-5 nano                         Grok-4 fast                       Deepseek-V3.1                      Qwen3-max                               GPT-3.5                                                 GPT-4o                       GPT-5 nano                     Grok-4 fast                       Deepseek-V3.1                    Qwen3-max                             GPT-3.5                                                 GPT-4o                       GPT-5 nano                        Grok-4 fast                       Deepseek-V3.1                        Qwen3-max                              GPT-3.5




                                                                             (a) FOLIO                                                                                                                                                                                                        (b) ProofWriter                                                                                                                                                                                                                  (c) PrOntoQA
                                                                                                                                                                       Figure 5: Comparison on the logical reasoning accuracy tasks.


logical structure.                                                                                                                                                                                                                                                                                                                                            a symbolic reasoner (Prolog) with a rule-learning
                                                                                                                                                                                                                                                                                                                                                              component to solve multi-hop reasoning problems.
5.2                         Logical Reasoning                                                                                                                                                                                                                                                                                                                 More recently, researchers have increasingly com-
Figure 5 reports accuracy on three logical reason-                                                                                                                                                                                                                                                                                                            bined LLMs with symbolic solvers across a range
ing benchmarks. Across all datasets and LLM                                                                                                                                                                                                                                                                                                                   of logical reasoning tasks. For example, Pan et al.
backbones, LLM-TP Tree is the strongest neuro-                                                                                                                                                                                                                                                                                                                (2023) and Olausson et al. (2023) autoformalise
symbolic method: compared with Logic-LM and                                                                                                                                                                                                                                                                                                                   natural-language contexts into symbolic represen-
LINC, it achieves higher overall accuracy, with                                                                                                                                                                                                                                                                                                               tations and then apply external solvers to perform
the largest gains on the more challenging settings                                                                                                                                                                                                                                                                                                            deductive reasoning over the resulting formal struc-
where multi-step composition is essential. These                                                                                                                                                                                                                                                                                                              tures. Along a related direction, Xu et al. (2025a)
results suggest that explicit theorem proving, cou-                                                                                                                                                                                                                                                                                                           proposes a decompose-search-resolve framework
pled with a tree-structured verification procedure,                                                                                                                                                                                                                                                                                                           that breaks a problem into smaller logical substruc-
provides a reliable supervision signal for reduc-                                                                                                                                                                                                                                                                                                             tures and performs structured search to resolve each
ing spurious inferences in existing neuro-symbolic                                                                                                                                                                                                                                                                                                            reasoning step. Prover feedback has also been used
pipelines, especially when the backbone model can                                                                                                                                                                                                                                                                                                             to improve reliability: Quan et al. (2025a) extracts
produce sufficiently accurate autoformalisation.                                                                                                                                                                                                                                                                                                              erroneous proof steps from solver feedback and
   At the same time, prompting-only baselines such                                                                                                                                                                                                                                                                                                            iteratively refines reasoning in a loop. In contrast
as CoT can still be competitive and may outperform                                                                                                                                                                                                                                                                                                            to endpoint-focused verification, our work targets
neuro-symbolic approaches on certain datasets.                                                                                                                                                                                                                                                                                                                recursively verifiable NLI by enforcing chain-level
In particular, on PrOntoQA, Standard and CoT                                                                                                                                                                                                                                                                                                                  checking and localised refinement over structured
prompting remain consistently strong, leaving lim-                                                                                                                                                                                                                                                                                                            entailment trees.
ited headroom for additional symbolic verification
to improve raw accuracy. This pattern is consis-                                                                                                                                                                                                                                                                                                               7                              Conclusion
tent with two factors: some benchmarks are close
to saturation under strong prompting, and neuro-
                                                                                                                                                                                                                                                                                                                                                              We presented LLM-TP Tree, a neuro-symbolic
symbolic methods introduce an additional failure
                                                                                                                                                                                                                                                                                                                                                              framework for recursively verifiable NLI that
mode through autoformalisation, where an incom-
                                                                                                                                                                                                                                                                                                                                                              follows a decompose-and-formalise paradigm.
plete or incorrect theory prevents the prover from
                                                                                                                                                                                                                                                                                                                                                              By combining entailment-tree verification with
establishing a label. Importantly, even in regimes
                                                                                                                                                                                                                                                                                                                                                              entailment-preserving atomic decomposition and θ-
where CoT is stronger in accuracy, LLM-TP Tree
                                                                                                                                                                                                                                                                                                                                                              substitution autoformalisation, our method enables
provides an advantage that prompting-only meth-
                                                                                                                                                                                                                                                                                                                                                              localised, refinement that targets the implicated part
ods do not: when successful, it produces solver-
                                                                                                                                                                                                                                                                                                                                                              of an explanation rather than regenerating it holisti-
checkable proof certificates and intermediate struc-
                                                                                                                                                                                                                                                                                                                                                              cally. Experiments on four datasets with multiple
ture that support auditability and diagnosis, which
                                                                                                                                                                                                                                                                                                                                                              LLM backbones show improved TP-verified expla-
are central to verifiable NLI.
                                                                                                                                                                                                                                                                                                                                                              nation rates, more faithful autoformalisation, and
6                    Related Work                                                                                                                                                                                                                                                                                                                             reduced refinement drift while maintaining strong
                                                                                                                                                                                                                                                                                                                                                              end-task reasoning accuracy. In future work, we
Neuro-symbolic pipelines have shown strong effec-                                                                                                                                                                                                                                                                                                             will extend this framework to broader naturalistic
tiveness on multi-hop reasoning, as they combine                                                                                                                                                                                                                                                                                                              settings, improve the robustness of entailment-tree
learned language understanding with symbolic rea-                                                                                                                                                                                                                                                                                                             construction and diagnostic localisation, and fur-
soning to support complex, multi-step inference.                                                                                                                                                                                                                                                                                                              ther reduce verification cost through better reuse of
Early work such as Weber et al. (2019) integrates                                                                                                                                                                                                                                                                                                             verified subtrees.

                                                                                                                                                                                                                                                                                                                                           8
Limitations                                                    pages 22017–22031, Miami, Florida, USA. Associa-
                                                               tion for Computational Linguistics.
Our framework produces solver-checkable certifi-
cates, but the guarantee is necessarily conditional          Dongwei Jiang, Marcio Fonseca, and Shay Cohen. 2024.
                                                               LeanReasoner: Boosting complex logical reasoning
on the chosen autoformalisation function Φ, the                with lean. In Proceedings of the 2024 Conference of
target formalism, and the capabilities of the under-           the North American Chapter of the Association for
lying theorem prover. In particular, a verification            Computational Linguistics: Human Language Tech-
can be valid in the induced formal theory while still          nologies (Volume 1: Long Papers), pages 7497–7510,
                                                               Mexico City, Mexico. Association for Computational
being partially misaligned with the original natural
                                                               Linguistics.
language intent if Φ introduces subtle scope, po-
larity, or role mismatches that are not exposed by           Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
our current faithfulness checks. This dependence is            dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
                                                               Luke Zettlemoyer, and Veselin Stoyanov. 2019.
amplified in naturalistic NLI, where missing back-             Roberta: A robustly optimized bert pretraining ap-
ground knowledge, implicit commonsense assump-                 proach. arXiv preprint arXiv:1907.11692.
tions, or discourse phenomena (e.g., coreference,
                                                             Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-
modality, temporality) may not be representable                son. 2002. Isabelle/HOL: a proof assistant for
in the event-based logical form, making some in-               higher-order logic. Springer.
stances difficult to certify without additional ax-
ioms or richer semantics. The effectiveness of lo-           Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
                                                               Armando Solar-Lezama, Joshua Tenenbaum, and
calised refinement also depends on the quality of              Roger Levy. 2023. LINC: A neurosymbolic approach
the intermediate structures proposed by the LLM                for logical reasoning by combining language models
and on the ability to map prover diagnostics back to           with first-order logic provers. In Proceedings of the
the responsible region. When the initial entailment            2023 Conference on Empirical Methods in Natural
                                                               Language Processing, pages 5153–5176, Singapore.
tree omits critical intermediate conclusions or intro-         Association for Computational Linguistics.
duces a misleading proof plan, bottom-up checking
can localise which obligations are not discharged            OpenAI. 2024. Gpt-4 technical report.         Preprint,
                                                               arXiv:2303.08774.
but may not reliably recover the globally correct
chain without substantial restructuring. Finally,            OpenAI. 2025. Introducing gpt-5. https://openai.
although our approach reduces expensive global                 com/index/introducing-gpt-5/.
regeneration, it still incurs non-trivial compute due        Liangming Pan, Alon Albalak, Xinyi Wang, and
to repeated LLM calls, repeated autoformalisation,             William Wang. 2023. Logic-LM: Empowering large
and repeated prover invocations. Prover timeouts or            language models with symbolic solvers for faithful
inconclusive outcomes can remain a practical bot-              logical reasoning. In Findings of the Association
                                                               for Computational Linguistics: EMNLP 2023, pages
tleneck on harder instances, and our current system            3806–3824, Singapore. Association for Computa-
does not provide a formal convergence guarantee                tional Linguistics.
to the minimal or unique refined explanation.
                                                             Xin Quan, Marco Valentino, Danilo Carvalho, Dhairya
                                                               Dalal, and Andre Freitas. 2025a. PEIRCE: Unify-
                                                               ing material and formal reasoning via LLM-driven
References                                                     neuro-symbolic refinement. In Proceedings of the
Bhavana Dalvi, Peter Jansen, Oyvind Tafjord, Zhengnan          63rd Annual Meeting of the Association for Compu-
  Xie, Hannah Smith, Leighanna Pipatanangkura, and             tational Linguistics (Volume 3: System Demonstra-
  Peter Clark. 2021. Explaining answers with entail-           tions), pages 11–21, Vienna, Austria. Association for
  ment trees. EMNLP.                                           Computational Linguistics.

Deepseek-AI. 2025. Deepseek-v3 technical report.             Xin Quan, Marco Valentino, Louise A. Dennis, and An-
  Preprint, arXiv:2412.19437.                                  dre Freitas. 2024. Verification and refinement of nat-
                                                               ural language explanations through LLM-symbolic
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-              theorem proving. In Proceedings of the 2024 Con-
  ing Qi, Martin Riddell, Wenfei Zhou, James Coady,            ference on Empirical Methods in Natural Language
  David Peng, Yujie Qiao, Luke Benson, Lucy Sun,               Processing, pages 2933–2958, Miami, Florida, USA.
  Alexander Wardle-Solano, Hannah Szabó, Ekaterina             Association for Computational Linguistics.
  Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu,
  Brian Wong, Malcolm Sailor, and 16 others. 2024.           Xin Quan, Marco Valentino, Louise A. Dennis, and An-
  FOLIO: Natural language reasoning with first-order           dre Freitas. 2025b. Faithful and robust LLM-driven
  logic. In Proceedings of the 2024 Conference on              theorem proving for NLI explanations. In Proceed-
  Empirical Methods in Natural Language Processing,            ings of the 63rd Annual Meeting of the Association


                                                         9
  for Computational Linguistics (Volume 1: Long Pa-            Jundong Xu, Hao Fei, Meng Luo, Qian Liu, Liangming
  pers), pages 17734–17755, Vienna, Austria. Associa-            Pan, William Yang Wang, Preslav Nakov, Mong-Li
  tion for Computational Linguistics.                            Lee, and Wynne Hsu. 2025a. Aristotle: Mastering
                                                                 logical reasoning with a logic-complete decompose-
Qwen Team. 2025. Qwen3 technical report. Preprint,               search-resolve framework. In Proceedings of the
 arXiv:2505.09388.                                               63rd Annual Meeting of the Association for Compu-
                                                                 tational Linguistics (Volume 1: Long Papers), pages
Zacchary Sadeddine and Fabian M. Suchanek. 2025.                 3052–3075, Vienna, Austria. Association for Compu-
  Verifying the steps of deductive reasoning chains. In          tational Linguistics.
  Findings of the Association for Computational Lin-
  guistics: ACL 2025, pages 456–475, Vienna, Austria.          Jundong Xu, Hao Fei, Liangming Pan, Qian Liu, Mong-
  Association for Computational Linguistics.                     Li Lee, and Wynne Hsu. 2024. Faithful logical rea-
                                                                 soning via symbolic chain-of-thought. In Proceed-
Abulhair Saparov and He He. 2023. Language models                ings of the 62nd Annual Meeting of the Association
  are greedy reasoners: A systematic formal analysis             for Computational Linguistics (Volume 1: Long Pa-
  of chain-of-thought. In The Eleventh International             pers), pages 13326–13365, Bangkok, Thailand. As-
  Conference on Learning Representations.                        sociation for Computational Linguistics.

                                                               Jundong Xu, Hao Fei, Huichi Zhou, Xin Quan, Qi-
Boris Shminke. 2022. Python client for isabelle server.          jun Huang, Shengqiong Wu, William Yang Wang,
  Preprint, arXiv:2212.11173.                                    Mong-Li Lee, and Wynne Hsu. 2025b. Training llms
                                                                 with logicreward for faithful and rigorous reasoning.
Neha Srikanth and Rachel Rudinger. 2025. NLI under               Preprint, arXiv:2512.18196.
  the microscope: What atomic hypothesis decomposi-
  tion reveals. In Proceedings of the 2025 Conference          Lei Xu, Pierre Beckmann, Marco Valentino, and André
  of the Nations of the Americas Chapter of the Asso-            Freitas. 2025c. Adaptive llm-symbolic reasoning
  ciation for Computational Linguistics: Human Lan-              via dynamic logical solver composition. Preprint,
  guage Technologies (Volume 1: Long Papers), pages              arXiv:2510.06774.
  2574–2589, Albuquerque, New Mexico. Association
  for Computational Linguistics.                               Lan Zhang, Marco Valentino, and Andre Freitas. 2025.
                                                                 Autoformalization in the wild: Assessing LLMs on
Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.            real-world mathematical definitions. In Proceed-
  ProofWriter: Generating implications, proofs, and              ings of the 2025 Conference on Empirical Methods
  abductive statements over natural language. In Find-           in Natural Language Processing, pages 1720–1738,
  ings of the Association for Computational Linguis-             Suzhou, China. Association for Computational Lin-
  tics: ACL-IJCNLP 2021, pages 3621–3634, Online.                guistics.
  Association for Computational Linguistics.
                                                               A     Dataset Details
Marco Valentino and André Freitas. 2024. On the na-
 ture of explanation: An epistemological-linguistic            A.1    Explanation Refinement
 perspective for explanation-based natural language            ProofWriter. ProofWriter (Tafjord et al., 2021)
 inference. Philosophy & Technology, 37(3):88.
                                                               is a synthetically generated deductive reasoning
Marco Valentino, Ian Pratt-Hartman, and André Freitas.         benchmark where each instance contains a natural
 2021. Do natural language explanations represent              language theory (facts and rules), a query, and a
 valid logical arguments? verifying entailment in ex-          gold truth label, with controllable multi-hop proof
 plainable nli gold standards. IWCS 2021, page 76.
                                                               depth. For explanation refinement, we sample 150
Leon Weber, Pasquale Minervini, Jannes Münchmeyer,             instances and stratify the sampling to cover a range
  Ulf Leser, and Tim Rocktäschel. 2019. NLProlog:              of gold proof depths d ∈ {1, 2, 3, 4, 5} on the
  Reasoning with weak unification for question answer-         ProofWriter D5 split under the open-world assump-
  ing in natural language. In Proceedings of the 57th          tion. To avoid ambiguity in verification-oriented re-
  Annual Meeting of the Association for Computational
  Linguistics, pages 6151–6161, Florence, Italy. Asso-         finement, we restrict to boolean-labelled instances
  ciation for Computational Linguistics.                       and exclude indeterminate cases (e.g., Unknown un-
                                                               der open-world settings). Each instance is cast into
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus              an NLI-style pair (P, h), where P is the provided
  Rabe, Charles Staats, Mateja Jamnik, and Christian
                                                               set of facts/rules and h is the hypothesis statement.
  Szegedy. 2022. Autoformalization with large lan-
  guage models. In Advances in Neural Information              PrOntoQA. PrOntoQA (Saparov and He, 2023)
  Processing Systems, volume 35, pages 32353–32368.
  Curran Associates, Inc.                                      is a synthetic dataset designed to evaluate deduc-
                                                               tive reasoning in controlled settings. Following the
xAI. 2025. Grok 4. https://x.ai/news/grok-4.                   Logic-LM (Pan et al., 2023) setup, we use the most

                                                          10
challenging five-hop subset (fictional-entity reason-         five-hop PrOntoQA subset. We randomly sam-
ing). For explanation refinement, we randomly                 ple 200 instances from this subset (binary labels),
sample 150 instances from this subset. Since this             which represents the most challenging multi-hop
subset is binary in nature, we keep boolean-labelled          configuration in the benchmark.
instances and cast each instance into the NLI-style
format (P, h).                                                B   Autoformalisation Errors

FOLIO. FOLIO (Han et al., 2024) is a human-                   Following the error taxonomy in Quan et al.
curated first-order logic reasoning benchmark, pair-          (2025b), we categorise autoformalisation errors
ing natural-language statements with formal logical           into four broad types: syntax, implication, quanti-
structure to support theorem-prover-based verifi-             fier, and variable errors. We define an autoformali-
cation. For explanation refinement, we use the                sation error as any mismatch between the intended
evaluation split commonly adopted by prior neuro-             logical meaning of the input sentence(s) (as cap-
symbolic work after preprocessing, and remove                 tured by a reference logic template or gold formali-
indeterminate labels to keep a boolean setting. Con-          sation) and the produced formal statement. Notably,
cretely, we start from 182 evaluation instances after         these categories differ in how easily they can be
filtering out 22 erroneous examples identified by             detected: syntax errors are often surfaced immedi-
Olausson et al. (2023) and exclude those with un-             ately by the theorem prover, whereas the remaining
certain labels, yielding 122 instances. We then               three categories typically produce well-typed, well-
treat the remaining instances as NLI pairs (P, h)             formed formulas that may still be semantically un-
for verification and refinement.                              faithful and therefore require semantic-level check-
                                                              ing.
EntailmentBank. EntailmentBank (Dalvi et al.,
                                                              Syntax errors. Syntax errors are those that pre-
2021) is a multi-hop entailment benchmark that pro-
                                                              vent the proof assistant from parsing or type-
vides naturalistic premises and hypotheses together
                                                              checking the generated statement, and are there-
with structured explanation annotations (interme-
                                                              fore usually the easiest to detect. Typical causes
diate conclusions and entailment structure). For
                                                              include missing brackets, malformed binder syntax,
explanation refinement, we sample 150 instances
                                                              incorrect use of infix operators, and type unifica-
and select examples spanning different gold proof
                                                              tion conflicts (e.g., using an event-typed variable
depths to ensure coverage of both shallow and
                                                              where an entity is expected). Such errors are often
longer-horizon multi-step chains. Each instance
                                                              directly indicated by the theorem prover’s feedback
is cast into (P, h), where P is the set of supporting
                                                              (parse errors, unknown constants, failed unification,
statements (facts) and h is the hypothesis.
                                                              or unsatisfied type-class constraints), making them
A.2   Logical Reasoning                                       amenable to automatic filtering.

ProofWriter. For logical reasoning, we evalu-                 Implication errors. Implication errors occur
ate on the ProofWriter D5 split under the open-               when the generated formula has a valid syntax and
world assumption to retain the three-way label                type, but its logical structure encodes the wrong
space (True/False/Unknown). We sample 225                     entailment relation compared to the intended tem-
instances stratified by gold reasoning depth d ∈              plate. This includes incorrect direction of implica-
{1, 2, 3, 4, 5}, with 45 instances per depth. Within          tion, incorrect connective choice (e.g., ∧ vs. →), or
each depth bucket, we balance labels by sampling              wrong nesting/precedence that changes the mean-
15 instances per class.                                       ing. These errors are difficult for theorem provers
                                                              to flag because the statement may still be perfectly
FOLIO. For logical reasoning, the original vali-              consistent and provable under some background
dation split contains 204 instances, while we select          axioms, while representing a different claim.
the 182 evaluation instances after filtering out 22
erroneous examples identified by Olausson et al.              Quantifier errors. Quantifier errors arise when
(2023) for evaluation. We evaluate on this 182-               the autoformalisation introduces incorrect quanti-
instance set under the dataset’s original label space.        fiers (∀ vs. ∃), incorrect quantifier scope, or incor-
                                                              rect ordering of quantifiers. These errors are es-
PrOntoQA. For logical reasoning, we follow                    pecially harmful because they often produce state-
prior work (Pan et al., 2023) and evaluate on the             ments that are strictly stronger or weaker than in-

                                                         11
Algorithm 1 VerifySubtree(Tsub , TP )                                     Dataset
                                                                                                 LT       w/o Atom         w/o θ
                                                                                         Init.    Fin.   Init.   Fin.    Init.   Fin.
 1: h ← root(Tsub ) {current hypothesis node}
 2: E ← leaves(Tsub ) {current  explanation nodes}                        Backbone: GPT-4o
                          S                                                                              71.31 86.07 75.41 88.52
 3: Construct A(E) = e∈E {Φ(a) | a ∈ D(e)} {axioms}                       FOLIO          81.15 90.16     ↓9.84   ↓4.09   ↓5.74 ↓1.64
 4: for each atom a ∈ D(h) do                                                                            87.33 92.00 89.33 94.67
                                                                          ProofWriter    91.33 95.33     ↓4.00   ↓3.33   ↓2.00 ↓0.66
 5:    Define the goal τ ← Φ(a)                                                                         86.67 92.67 90.00 94.00
 6:    if TP .prove A(E) ⊢ τ = FAIL then                                  PrOntoQA       92.00 97.33     ↓5.33   ↓4.66   ↓2.00 ↓3.33
                                                                                                         17.33 53.33 19.33 61.33
 7:       diag ← TP .diagnostics()                                        EntailmentBank 21.33 70.00     ↓4.00 ↓16.67 ↓2.00 ↓8.67
 8:       Identify implicated explanation nodes Eb ⊆ E from               Backbone: Qwen3-max
          diag                                                                                        72.13 86.89 79.51 90.98
                                                                          FOLIO          85.25 95.08 ↓13.12 ↓8.19 ↓5.74 ↓4.10
 9:       Refine Eb using an LLM conditioned on (E,  b diag)                                          88.00 93.33 88.00 96.00
10:        Update Tsub ; recompute D(·) and re-autoformalise              ProofWriter    92.00 98.00 ↓4.00 ↓4.67 ↓4.00 ↓2.00
                                                                                                      86.67 94.00 92.00 96.00
          Φ(·)                                                            PrOntoQA       98.00 100.00 ↓11.33 ↓6.00 ↓6.00 ↓4.00
11:        return VerifySubtree(Tsub , TP ) {retry locally}                                           18.00 61.33 20.00 71.33
                                                                          EntailmentBank 22.67 78.67 ↓4.67 ↓17.34 ↓2.67 ↓7.34
12:    end if
13: end for                                                         Table 4: Ablations of LLM-TP Tree on GPT-4o and Qwen3-
14: Mark h as verified                                              max (Init/Fin verified rate, %). Red arrows indicate the abso-
15: return h {promote as support for parent level}                  lute decrease compared to LT under the same backbone.

                                                                    the constructed Isabelle/HOL theory is shown in
tended while remaining syntactically valid. More-                   Figure 6. We then apply atomic decomposition to
over, theorem provers typically do not report quan-                 each axiom and to the hypothesis. The decomposed
tifier mismatches as errors; the formula is well-                   hypothesis sentence and the decomposed axioms
formed, yet its truth conditions can differ dramati-                are then forming a new theory, which we use to
cally.                                                              prove theorems from each decomposed hypothesis
Variable errors. Variable errors occur when log-                    atoms.
ical variables are incorrectly assigned to predicate
                                                                    E    Ablation Study on Explanation
arguments, resulting in role confusion or broken
                                                                         Refinement Task
discourse links. This category covers a wide range
of semantic binding mistakes, including swapping                    Table 4 reports ablations of LLM-TP Tree (LT) on
semantic roles (e.g., agent vs. patient), incorrectly               GPT-4o and Qwen3-max, using Init./Fin. logically
linking pronouns/coreference, using the wrong                       valid explanation rates. Removing either of the two
event/entity variable in a clause, or mistakenly                    proposed components, atomic decomposition or
reusing a variable that should be distinct. Vari-                   multi-step θ-substitution autoformalisation, consis-
able errors may be subtle because they can remain                   tently degrades across all datasets. Across datasets,
type-correct (e.g., swapping two entity variables                   Init. decreases by 4.00 to 13.12 points and Fin.
still type-checks) yet invert the intended meaning.                 decreases by 3.33 to 17.34 points, with the most
                                                                    pronounced degradation on EntailmentBank. Re-
C    Algorithm                                                      moving θ-substitution also leads to a consistent
                                                                    drop, although smaller than w/o Atom indicating
D    Isabelle/HOL and LLMs                                          that multi-step substitution contributes materially
     Implementation Detail                                          to producing prover-compatible formalisations.
We use the isabelle-client Python pack-                             F    Full results: Model efficiency Across
age (Shminke, 2022) to run Isabelle/HOL as a real-                       LLM Backbones
time server and to retrieve prover responses. We
access all LLM backbones via API calls with the                     Figure 7a, 7b and 7c shows average number of
following model versions: GPT-4o (gpt-4o), GPT-                     iterations required to refine an explanation across
5 nano (gpt-5-nano), Grok-4 fast (grok-4-fast),                     all LLMs. Figure 7e, 7f, 7g and 8 shows average
Deepseek-V3.1 (DeepSeek-v3.1-terminus), and                         inference time per iteration in both thinking and
Qwen3-Max (qwen3-max-preview). For all non-                         non-thinking models.
thinking models, we set the temperature to 0. We
                                                                    G    Full Results: Autoformalisation
also do not limit any thinking effort for Deepseek-
                                                                         Faithfulness Across LLM Backbones
V3.1 and Qwen3-Max.
   We build the Isabelle/HOL theory following the                   Figure 9 compares the average faithfulness of
approach in (Quan et al., 2025b). An example of                     the autoformalisation process across different ap-

                                                               12
                                                                                                
theory data_0
imports Main

begin

typedecl entity
typedecl event

consts
  Melting :: "event ⇒ bool"
  Change :: "event ⇒ bool"
  Source :: "event ⇒ entity ⇒ bool"
  Destination :: "event ⇒ entity ⇒ bool"
  Solid :: "entity ⇒ bool"
  Liquid :: "entity ⇒ bool"
  IncreaseHeatEnergy :: "entity ⇒ bool"
  By :: "event ⇒ entity ⇒ bool"
  Chocolate :: "entity ⇒ bool"
  Melts :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  In :: "event ⇒ entity ⇒ bool"
  Sunlight :: "entity ⇒ bool"

(* Explanation 1: melting means changing from a solid to a liquid by increasing heat energy *)
axiomatization where
  explanation_1: "∀ e x y z. Melting e ↔ (Change e ∧ Source e x ∧ Destination e y ∧ Solid x ∧
    Liquid y ∧ IncreaseHeatEnergy z ∧ By e z)"

(* Explanation 2: chocolate melts in the sunlight *)
axiomatization where
  explanation_2: "∃ x e. Chocolate x ∧ Melts e ∧ Agent e x ∧ In e Sunlight"

theorem hypothesis:
  assumes asm: "Chocolate x ∧ Solid y ∧ Liquid z"
  (* Hypothesis: chocolate changes from a solid to a liquid in the sunlight *)
  shows False
  sledgehammer
  oops

end
                                                                                                
                      Figure 6: An example of the constructed Isabelle/HOL Theory.




                                                  13
Average Iteration Numbers




                                                                                                                                                                                      Average Iteration Numbers




                                                                                                                                                                                                                                                                                                                                                                             Average Iteration Numbers




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Average Iteration Numbers
                             6                                                      ER                         FR                    LT                    LT w/o AD                                               6                                                      ER                         FR                    LT                    LT w/o AD                                                6                                                      ER                         FR                    LT                    LT w/o AD                                               6                                                      ER 5.71                    FR                     LT                    LT w/o AD
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           5.21
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      5.06
                             5                                                                                                                                                                                     5                                                                                                                                                                                      5                                                                                                                                                                                     5        4.94
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             4.86                                                4.88

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           4.52                          4.56
                                                                                                 4.44
                                                                                                                             4.36                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 4.36                                4.31
                                      4.23                                                                                                                4.19                                                                                                                                                                                                                                                                                                                                                                                                                                                                4.25                                                                                            4.24
                                                                   4.13                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         4.13                                                                                    4.09                                       4.11
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    4.02                                                                             4.02
                             4                                                                                                                                                                                     4                                                                                                                                                                                      4                                                                                                                                                                                     4
                                                                                                                                    3.92                                                                                                                                                                                                                                                                                                                                                                                                                                                                               3.95                                                                                    3.99
                                             3.85                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           3.88
                                                                          3.78          3.73                                                                                                                                                                                                                       3.76
                                                                                                        3.69                                                                   3.64
                                                                                                                      3.55                                                                                                                               3.57                                               3.55                                                                                                                                3.59
                                                           3.45                                                                                   3.46           3.50                                                                                                                                                                                                                                                                                                                                     3.44
                                                                                                                                                                                                                                                                                       3.42                                                     3.38                                                                                                                          3.39
                                                                                                               3.27                                                                                                         3.24                                                              3.21                                                                                                                                                                                                                                     3.25
                                                                                 3.11                                                                                                                                                                           3.11          3.18                                                                                                                                 3.14
                                                    3.09                                                                                                                3.08                                                                                                                         3.04                                              3.09
                                                                                                                                                                                                                                   3.00                                                                                   3.00
                             3                                                                                                             2.64
                                                                                                                                                                                                                   3                                                                                                                                                 2.66
                                                                                                                                                                                                                                                                                                                                                                                                          3               2.90
                                                                                                                                                                                                                                                                                                                                                                                                                                        2.73                                         2.67          2.71          2.78                         2.71
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                3
                                                                                                                                                                                                                                                 2.55                                                                                                                                                                                                  2.60
                                                                                                                                                                                                                                                                       2.44                                                             2.46                                                                                                                         2.48
                                                                                                                                                                                                                                          2.33                                                                                                                                                                                                                                              2.38
                                                                                                                                                                                                                                                                                                                                 2.30                                                                                            2.25                                                                                          2.25
                                                                                                                                                                                                                                                                                                                                                                                                                                                              2.14
                                                                                                                                                                                                                                                                                                                                                              2.00                                                                                                                                                                                          2.01
                             2                                                                                                                                                                                     2                                                                                                                                                                                      2                                                                                                             1.75
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1.67
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                2

                             1                                                                                                                                                                                     1                                                                                                                                                                                      1                                                                                                                                                                                     1

                             0                                                                                                                                                                                     0                                                                                                                                                                                      0                                                                                                                                                                                     0
                                         GPT-4o                    GPT-5 nano                    Grok-4 fast Deepseek-V3.1Qwen3-max                                                                                            GPT-4o                    GPT-5 nano                    Grok-4 fast Deepseek-V3.1Qwen3-max                                                                                             GPT-4o                    GPT-5 nano                    Grok-4 fast Deepseek-V3.1Qwen3-max                                                                                            GPT-4o                    GPT-5 nano                    Grok-4 fast Deepseek-V3.1Qwen3-max




                                                                     (a) FOLIO                                                                                                                                                               (b) ProofWriter                                                                                                                                                                             (c) PrOntoQA                                                                                                                                                       (d) EntailmentBank
                                                                      ER                        FR                      LT                   LT w/o AD                                                                                                      ER                        FR                      LT                   LT w/o AD                                                                                                       ER                        FR                      LT                   LT w/o AD                                                                                                      ER                        FR                      LT                    LT w/o AD
Average Inference Time (s)




                                                                                                                                                                                      Average Inference Time (s)




                                                                                                                                                                                                                                                                                                                                                                             Average Inference Time (s)




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Average Inference Time (s)
                             300                                                                                                                                                                                   300                                                                                                                                                                                    300                                                                                                                                                                                   300

                             250                                                                                                                                                                                   250                                                                                                                                                                                    250                                                                                                                                                                                   250             244.50

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  223.20                                       219.30


                             200                                                                                                                                                                                   200                                                                                                                                                                                    200                                                                                                                                                                                   200
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          179.30                                           179.30
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         165.80
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               158.50

                             150             147.20
                                                                                               141.30                                      144.10
                                                                                                                                                                                                                   150                                                                                                                                                                                    150                                                                                                                                                                                   150                                   134.80                                        134.80
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                142.80
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  132.60
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              141.70
                                                                                                                                                                                                                                   129.50
                                                                                                                                                                                                                                                                                                                                                                                                                          121.40
                                                                                                                                                                                                                                                                                     117.10                                                                                                                                                                                                                             113.80
                                                                                                                                                                                                                                                                                                                                 108.50                                                                                                                                     108.30

                             100                       97.40                                            94.30                                        91.20                                                         100                       87.30
                                                                                                                                                                                                                                                                                              82.30                                        80.10
                                                                                                                                                                                                                                                                                                                                                                                                          100                                                                                                                                                                                   100
                                                                            79.10                                            75.10                                                                                                                                                                                                                                                                                                  75.30
                                                                                                                                                                          72.30                                                                                                                                                                                                                                                                                                      70.50                                        72.70
                                                                   67.50                                          65.40                                                                                                                                           68.00                                            64.80                                        66.90                                                                                    64.30                                            64.00
                                                                                                                                                                 61.60                                                                                   62.10                                                                                                                                                                                                                                                                                         62.80
                                                                                                                                                                                                                                                                                                        58.40                                          55.20                                                                                    58.40
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               51.20
                                 50                                                                                                                                                                                    50                                                                                                                                                                                     50                                                                                                                              48.20
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    50

                                  0                                                                                                                                                                                     0                                                                                                                                                                                      0                                                                                                                                                                                     0
                                                           GPT-4o                                  GPT-5 nano                                      Grok-4 fast                                                                                   GPT-4o                                  GPT-5 nano                                      Grok-4 fast                                                                                    GPT-4o                                  GPT-5 nano                                      Grok-4 fast                                                                                   GPT-4o                                  GPT-5 nano                                       Grok-4 fast




                                                                     (e) FOLIO                                                                                                                                                                   (f) ProofWriter                                                                                                                                                                         (g) PrOntoQA                                                                                                                                                       (h) EntailmentBank
Figure 7: Top: Average number of iterations required to refine an explanation. Bottom: Average inference time per
iteration. Comparison between ER (Explanation-Refiner), FR (Faithful-Refiner), LT (LLM-TP Tree) and LT w/o
AD (LT without atomic decomposition).

                                                                      ER                        FR                      LT                   LT w/o AD                                                                                                      ER                        FR                      LT                   LT w/o AD                                                                                                       ER                        FR                      LT                   LT w/o AD                                                                                                      ER                        FR                      LT                    LT w/o AD
Average Inference Time (s)




                                                                                                                                                                                      Average Inference Time (s)




                                                                                                                                                                                                                                                                                                                                                                             Average Inference Time (s)




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Average Inference Time (s)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  832.90                                                                    820.60

                             800                                                                                                                                                                                   800                                                                                                                                                                                    800                                                                                                                                                                                   800
                                               684.80

                                                                                                                         623.30                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      623.70                                                               634.00

                             600                                  580.10                                                              573.50                            584.80
                                                                                                                                                                                                                   600               584.40
                                                                                                                                                                                                                                                                                                               553.10
                                                                                                                                                                                                                                                                                                                                                                                                          600                                                                                                                                                                                   600                                                                 594.50
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             548.80
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            577.10

                                                                                                 523.30                                                                                                                                                                                                                                                                                                                     533.20                                                                                                                                                                                                                  534.90
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      512.50
                                                                                 490.30                                                                                                                                                                 484.20                                                                                                                                                                                 494.20
                                                                                                                                                                                                                                                                                                                            460.40
                                                                                                                                                         441.00                                                                                                                                                                                                                                                                                                                                                    434.10                            429.40
                                                                                                                                                                                                                                                                                       412.70                                                                 423.50
                                                                                                                                                                                                                                                                                                                                                                                                                                                                              404.20
                             400                                                                                                                                                                                   400                                                 382.30
                                                                                                                                                                                                                                                                                                                                               355.70
                                                                                                                                                                                                                                                                                                                                                                                                          400                                                 347.80
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                400
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      321.90




                             200                                                                                                                                                                                   200                                                                                                                                                                                    200                                                                                                                                                                                   200


                                  0                                                                                                                                                                                     0                                                                                                                                                                                      0                                                                                                                                                                                     0
                                                             Deepseek-V3.1                                                            Qwen3-max                                                                                                    Deepseek-V3.1                                                            Qwen3-max                                                                                                     Deepseek-V3.1                                                            Qwen3-max                                                                                                    Deepseek-V3.1                                                             Qwen3-max




                                                                     (a) FOLIO                                                                                                                                                               (b) ProofWriter                                                                                                                                                                             (c) PrOntoQA                                                                                                                                                       (d) EntailmentBank
Figure 8: Average inference time per iteration in thinking mode LLMs. Comparison between ER (Explanation-
Refiner), FR (Faithful-Refiner), LT (LLM-TP Tree) and LT w/o AD (LT without atomic decomposition).


proaches, averaged over all LLM backbones.                                                                                                                                                                                                                                                                                                                                                                     USER: Here are some examples:
                                                                                                                                                                                                                                                                                                                                                                                                               Example:
H                                              Solver Proof Depths                                                                                                                                                                                                                                                                                                                                             Provided Sentence:
                                                                                                                                                                                                                                                                                                                                                                                                               Professional actors are in a summer performance.
Table 5 and Table 6 shows Per-LLM depth align-                                                                                                                                                                                                                                                                                                                                                                 Answer:
                                                                                                                                                                                                                                                                                                                                                                                                               Atom 1: The people are professional.
ment details for ProofWriter and EntailmentBank                                                                                                                                                                                                                                                                                                                                                                Atom 2: The people are actors.
in refined and unrefined cases. Each cell reports                                                                                                                                                                                                                                                                                                                                                              Atom 3: The performance is during summer.
the mean used proof depth averaged over instances                                                                                                                                                                                                                                                                                                                                                              Task:
                                                                                                                                                                                                                                                                                                                                                                                                               Provided Sentence: {sentence}
within the corresponding gold depth bucket, for a
fixed framework and LLM backbone.                                                                                                                                                                                                                                                                                                                                                                              Answer:

I                                      Atomic Decomposition Prompt                                                                                                                                                                                                                                                                                                                                    J                          Entailment Tree Construction Prompt
We build the atomic decomposition prompt based                                                                                                                                                                                                                                                                                                                                                                 SYSTEM: You are an expert in natural language inference
on Srikanth and Rudinger (2025) as:                                                                                                                                                                                                                                                                                                                                                                            and textual entailment. Given the following premise sen-
                                                                                                                                                                                                                                                                                                                                                                                                               tences and a final conclusion, generate some step-by-step
                             SYSTEM: You are an expert in symbolic/logical reasoning,                                                                                                                                                                                                                                                                                                                          intermediate conclusion sentences to finally infer the final
                             linguistic and natural language inference. You are given                                                                                                                                                                                                                                                                                                                          conclusion.
                             a sentence and its logical information. Generate a list of                                                                                                                                                                                                                                                                                                                        Instructions:
                             atomic facts that are strictly logically entailed from the given
                             sentence.                                                                                                                                                                                                                                                                                                                                                                                       1. The intermediate conclusion sentences must be strictly
                             Instructions:                                                                                                                                                                                                                                                                                                                                                                                      logical entailed from the premise sentences.

                                        1. Keep each fact independent and self-contained.                                                                                                                                                                                                                                                                                                                                    2. Since the reasoning is step-by-step, the intermediate
                                                                                                                                                                                                                                                                                                                                                                                                                                conclusion sentences can be the new premise sen-
                                        2. Each fact should make sense when read on its own.                                                                                                                                                                                                                                                                                                                                    tences for next step.

                                        3. Only write facts that are directly described or sup-                                                                                                                                                                                                                                                                                                                              3. One intermediate conclusion sentence can be gener-
                                           ported by the sentence.                                                                                                                                                                                                                                                                                                                                                              ated from multiple premise sentences.

                                        4. The atomic facts must be logically entailed from the                                                                                                                                                                                                                                                                                                                              4. If the final conclusion can be directly inferred from the
                                           given sentence.                                                                                                                                                                                                                                                                                                                                                                      premise sentences, you need to state the intermediate



                                                                                                                                                                                                                                                                                                                                                                            14
                                                          ER                     FR                  LT                  LT w/o sub.                                                                                               ER                     FR                  LT                  LT w/o sub.                                                                                                ER                     FR                  LT                  LT w/o sub.                                                                                            ER                     FR                  LT                  LT w/o sub.
                       1.0                                                                                                                                                                      1.0                 0.95                                                                                0.94                        0.95
                                                                                                                                                                                                                                                                                                                                                                          1.0                 0.96                        0.95                        0.95                        0.96
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0.940.93
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                1.0
                                                                                                                                                                                                                           0.92                 0.93                        0.93                               0.92                        0.93                                        0.92          0.92          0.93          0.92                        0.92          0.92          0.93
                                                                                                                                                           0.91                                              0.91                                      0.90                        0.90          0.90                                                                                                                                          0.91                                                    0.91
                                                                                                                                                    0.88          0.88                                                                   0.89                        0.88                                                    0.88
Average Faithfulness




                                                                                                                                                                         Average Faithfulness




                                                                                                                                                                                                                                                                                                                                                   Average Faithfulness




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Average Faithfulness
                                                                       0.85                                                    0.86                                                                   0.85                                                                                                                                                                      0.85
                                           0.84                               0.83                                                                                                                                                0.83                        0.83                        0.84                                                                                                                                                                      0.83                                                                                            0.84                                                                                0.83                        0.84
                                    0.82          0.81          0.81                               0.82                 0.81          0.82                                                                                                                                                                            0.82                                                                                  0.81                        0.82                                                    0.81                                                                                            0.82
                                                                                                          0.80                               0.80
                       0.8   0.78
                                                         0.74
                                                                                            0.79                 0.78                                                                           0.8                                                                                                                                                                       0.8                                                                                                                                                                   0.8          0.76
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0.78                        0.77
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            0.79                               0.79
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0.74
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0.79

                                                                                     0.73                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          0.72          0.73
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0.71
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.69

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0.62                                                                                0.63                        0.62
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0.61
                       0.6                                                                                                                                                                      0.6                                                                                                                                                                       0.6                                                                                                                                                                   0.6                               0.59




                       0.4                                                                                                                                                                      0.4                                                                                                                                                                       0.4                                                                                                                                                                   0.4


                       0.2                                                                                                                                                                      0.2                                                                                                                                                                       0.2                                                                                                                                                                   0.2


                       0.0      GPT-4o                    GPT-5 nano                  Grok-4 fast                Deepseek-V3.1                Qwen3-max
                                                                                                                                                                                                0.0       GPT-4o                   GPT-5 nano                  Grok-4 fast                Deepseek-V3.1                Qwen3-max
                                                                                                                                                                                                                                                                                                                                                                          0.0      GPT-4o                    GPT-5 nano                  Grok-4 fast                Deepseek-V3.1                Qwen3-max
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                0.0       GPT-4o                   GPT-5 nano                  Grok-4 fast                Deepseek-V3.1                Qwen3-max




                                                         (a) FOLIO                                                                                                                                              (b) ProofWriter                                                                                                                                                                 (c) PrOntoQA                                                                                                                                          (d) EntailmentBank
                       Figure 9: Comparison of the average faithfulness of the autoformalisation process across different approaches.

                                              (a) ProofWriter: mean used proof depth by gold depth                                                                                                                                                                                                                                                                                       (b) EntailmentBank: mean used proof depth by gold depth

                                                                                                                                                                                                                                  Gold depth d                                                                                                                                                                                                                                                                                                                                    Gold Depths d
Framework                                                                                                        LLM                                                                                                                                                                                                                                 Framework                                                                                                       LLM
                                                                                                                                                                                                      1                           2                                  3                              4                                  5                                                                                                                                                                                                              1                            2                                  3                                  4                                 5

                    GPT-4o                                                                                                                                                                       1.00                       2.32                              2.51                          2.92                               3.23                                      GPT-4o                                                                                                                                                                   1.23                        2.14                            2.65                               3.15                           3.21
                    GPT-5 nano                                                                                                                                                                   1.14                       2.00                              2.67                          2.61                               2.94                                      GPT-5 nano                                                                                                                                                               1.21                        2.23                            2.43                               2.91                           2.94
Explanation-Refiner Grok-4 fast                                                                                                                                                                  1.08                       2.04                              2.53                          2.62                               2.92                  Explanation-Refiner Grok-4 fast                                                                                                                                                              1.13                        2.21                            2.52                               2.93                           2.92
                    Deepseek-V3.1                                                                                                                                                                1.28                       2.41                              2.23                          2.87                               3.04                                      Deepseek-V3.1                                                                                                                                                            1.16                        2.28                            2.67                               3.04                           3.16
                    Qwen3-max                                                                                                                                                                    1.10                       2.43                              2.24                          2.90                               3.11                                      Qwen3-max                                                                                                                                                                1.28                        2.32                            2.63                               3.18                           3.20

                                                                                                                 GPT-4o                                                                          1.00                       2.26                              2.76                          3.43                               3.94                                                                                                                                  GPT-4o                                                                       1.12                        2.10                            2.87                               3.33                           3.67
                                                                                                                 GPT-5 nano                                                                      1.02                       2.04                              3.13                          3.34                               3.63                                                                                                                                  GPT-5 nano                                                                   1.11                        2.12                            2.64                               3.22                           3.40
Faithful-Refiner                                                                                                 Grok-4 fast                                                                     1.14                       2.09                              2.67                          3.18                               3.87                  Faithful-Refiner                                                                                                Grok-4 fast                                                                  1.17                        2.13                            2.72                               3.58                           3.42
                                                                                                                 Deepseek-V3.1                                                                   1.00                       2.17                              2.78                          3.41                               3.73                                                                                                                                  Deepseek-V3.1                                                                1.03                        2.25                            2.78                               3.40                           3.69
                                                                                                                 Qwen3-max                                                                       1.00                       2.22                              2.77                          3.58                               3.79                                                                                                                                  Qwen3-max                                                                    1.17                        2.20                            2.93                               3.47                           3.73

                                                                                                                 GPT-4o                                                                          1.00                       1.99                              2.94                          3.76                               4.72                                                                                                                                  GPT-4o                                                                       1.00                        2.10                            2.85                               3.90                           4.81
                                                                                                                 GPT-5 nano                                                                      1.08                       2.12                              2.98                          3.68                               4.53                                                                                                                                  GPT-5 nano                                                                   1.00                        1.84                            2.84                               3.86                           4.71
LLM-TP Tree                                                                                                      Grok-4 fast                                                                     1.17                       1.89                              3.18                          3.49                               5.03                  LLM-TP Tree                                                                                                     Grok-4 fast                                                                  1.00                        2.04                            2.92                               3.88                           4.73
                                                                                                                 Deepseek-V3.1                                                                   1.00                       2.03                              3.08                          3.84                               4.94                                                                                                                                  Deepseek-V3.1                                                                1.00                        1.97                            3.03                               4.03                           4.85
                                                                                                                 Qwen3-max                                                                       1.00                       2.00                              3.00                          3.89                               4.88                                                                                                                                  Qwen3-max                                                                    1.00                        1.96                            2.94                               3.98                           4.92


                                                         Table 5: Per-LLM depth alignment details for ProofWriter and EntailmentBank in refined cases.


                                             conclusion sentences are empty.                                                                                                                                                                                                                                                                                                Conclusion: Humans can get monkeypox.

                             5. There might be redundant premise sentences.
                                                                                                                                                                                                                                                                                                                                                                            Humans are mammals.
                       USER: Here are some examples:                                                                                                                                                                                                                                                                                                                        Mammals are animals.
                       Example:                                                                                                                                                                                                                                                                                                                                             Conclusion:Humans are animals.
                       Initial Premises:
                       1.           Monkeypox is an infectious disease caused by the                                                                                                                                                                                                                                                                                        ...
                       monkeypox virus.                                                                                                                                                                                                                                                                                                                                     Humans are animals.
                       2. Monkeypox virus can occur in certain animals, including                                                                                                                                                                                                                                                                                           Therefore, there is an animal (humans) that can get
                       humans.                                                                                                                                                                                                                                                                                                                                              monkeypox and feel tired. Conclusion:Therefore, there is an
                       3. Humans are mammals.                                                                                                                                                                                                                                                                                                                               animal.
                       4. Mammals are animals.
                       5.            Symptoms of Monkeypox include fever, headache,                                                                                                                                                                                                                                                                                         Initial Premises:
                       muscle pains, feeling tired, and so on.
                       6. People feel tired when they get a flu.
                                                                                                                                                                                                                                                                                                                                                                            Final Conclusion:
                       Final Conclusion:
                       There is an animal.
                                                                                                                                                                                                                                                                                                                                                                            Answer:
                       Answer:
                       Monkeypox is an infectious disease caused by the
                       monkeypox virus.
                       Monkeypox virus can occur in certain animals, including
                       humans.



                                                                                                                                                                                                                                                                                                                                                  15
           (a) ProofWriter: mean used proof depth by gold depth                     (b) EntailmentBank: mean used proof depth by gold depth

                                                 Gold depth d                                                              Gold Depths d
Framework              LLM                                                   Framework            LLM
                                           1     2      3         4    5                                             1      2      3      4      5

                    GPT-4o               1.00   2.34   2.49   2.57    2.33                       GPT-4o             1.53   2.84   2.48   2.44   2.21
                    GPT-5 nano           1.12   1.99   2.57   2.46    2.24                       GPT-5 nano         1.39   2.99   2.33   2.31   1.95
Explanation-Refiner Grok-4 fast          1.10   1.87   2.48   2.38    2.32   Explanation-Refiner Grok-4 fast        1.43   2.83   2.24   2.21   1.92
                    Deepseek-V3.1        1.18   2.37   1.98   2.84    2.54                       Deepseek-V3.1      1.48   2.58   2.33   2.14   1.96
                    Qwen3-max            1.00   2.33   2.11   2.47    2.62                       Qwen3-max          1.88   3.12   2.32   2.19   2.12

                       GPT-4o            1.02   2.16   2.73   3.44    3.12                        GPT-4o            1.34   2.42   2.48   3.23   3.55
                       GPT-5 nano        1.02   1.95   3.23   3.24    3.02                        GPT-5 nano        1.33   2.32   2.41   3.32   3.30
Faithful-Refiner       Grok-4 fast       1.16   2.46   2.62   3.09    3.06   Faithful-Refiner     Grok-4 fast       1.49   2.28   2.43   3.54   3.42
                       Deepseek-V3.1     1.00   1.98   2.78   2.98    3.27                        Deepseek-V3.1     1.10   2.85   2.34   3.38   3.45
                       Qwen3-max         1.00   2.22   2.67   3.15    3.43                        Qwen3-max         1.67   2.74   2.53   3.43   3.42

                       GPT-4o            1.02   2.13   3.01   3.72    4.72                        GPT-4o            1.03   2.13   2.83   3.93   4.62
                       GPT-5 nano        1.09   2.14   2.95   3.54    4.65                        GPT-5 nano        1.13   1.86   2.80   3.78   4.51
LLM-TP Tree            Grok-4 fast       1.15   1.79   3.16   3.50    5.13   LLM-TP Tree          Grok-4 fast       1.12   2.04   2.95   3.91   4.43
                       Deepseek-V3.1     1.02   2.13   3.04   3.86    4.87                        Deepseek-V3.1     1.03   1.89   3.12   4.12   4.67
                       Qwen3-max         1.00   1.98   3.00   3.88    4.91                        Qwen3-max         1.00   2.01   2.99   4.08   4.74


           Table 6: Per-LLM depth alignment details for ProofWriter and EntailmentBank in unrefined cases.


K        θ-substitution Autoformalisation
         Prompt                                                                 Answer:


  SYSTEM: You are an expert in symbolic/logical reasoning
  and autoformalisation. You are given a sentence.Extract
  the logical relation from a given natural language sentence
  and construct a logical template representing its structure,
  following the format demonstrated in the examples.

  Instructions:

        1. Read and understand the provided sentence.

        2. Identify key entities, relationships, and logical struc-
           ture (e.g., quantifiers, conjunctions, disjunctions, im-
           plications).

        3. Abstract the sentence into a logical template using
           placeholders (e.g., ∀ x y z. P(x) ∧ Q(y) ∧ R(z) → S)
           that capture the logical form, not the specific content.

  Follow these steps:
  1. Parse the sentence and reason step-by-step about its
  logical components: What are its predicates, quantifiers,
  variables, and connectives?
  2. Formulate the logical template, using generic predicate
  letters (P, Q, R, S, etc.) and variable placeholders (x, y, z,
  etc.), mirroring the schema shown in the examples.
  ...
  Example 1:
  Sentence: If someone wins the lottery, they will buy a new
  house or a car.


  Example 1 Answer:
  Logical Template: ∀x y z. P(x) ∧ Q(y) → (R(z) ∨S(z))
  ...
  Provided Sentence: {sentence}



                                                                           16
