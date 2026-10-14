                                              SOVER: Formal Certification of Optimization Reformulations via
                                                           LLM-Assisted SMT Verification

                                                         Swapnil Bhattacharyya                             Mayank Baranwal
                                                         TCS Research, Mumbai                            TCS Research, Mumbai
                                                          b.swapnil@tcs.com                      Indian Institute of Technology Bombay
                                                                                                        mbaranwal@iitb.ac.in



                                                              Abstract                              LLMs are increasingly used as optimization copi-
                                                                                                 lots, translating natural language specifications into
                                            Large Language Models (LLMs) have shown
                                                                                                 formal models (Huang et al., 2025) and assisting
arXiv:2609.00728v1 [cs.AI] 1 Sep 2026




                                            remarkable promise in translating and refor-
                                            mulating complex mathematical optimization           in solution workflows (Zhang et al., 2025). How-
                                            problems across modeling languages. However,         ever, LLM-generated formulations remain unreli-
                                            validating such transformations through empir-       able (Ma et al., 2026), often containing ambigu-
                                            ical solver executions alone is unreliable, as       ous terminology, missing assumptions, inconsis-
                                            solver outcomes may be affected by local min-        tent variables, or structural errors (AhmadiTeshnizi
                                            ima, structural timeouts, numerical artifacts,       et al., 2024). Rigorous equivalence checking is
                                            and subtle semantic divergence between formu-
                                                                                                 therefore essential (Wang and Li, 2025), especially
                                            lations. We introduce SOVER, an LLM-assisted
                                            SMT framework that separates semantic map-           when AI-generated models (Yao et al., 2025) must
                                            ping from formal certification: Z3 checks            be validated against trusted ground-truth formula-
                                            domain cross-feasibility and global objective-       tions (Zhou and Zhang, 2025) while preserving in-
                                            order preservation for mixed-integer linear for-     tended mathematical semantics (Xiao et al., 2025).
                                            mulations, while dReal provides tolerance-              A central challenge is that reformulation equiva-
                                            aware feasibility/range and ϵ-argmin checks          lence is not captured by equality of solver outputs.
                                            for continuous nonlinear formulations. We            As shown in Figure 1, different formulations may
                                            also introduce NLE QUIV-150, a public bench-
                                            mark of 100 equivalent and 50 deliberately hard
                                                                                                 share the same optimizer and optimal value when
                                            non-equivalent nonlinear reformulation pairs.        constraints are inactive, while equivalent formula-
                                            With LLM-extracted mappings, SOVER classi-           tions can differ when objectives are scaled. Robust
                                            fies 149/150 pairs (99.33%) correctly, includ-       verification must also handle symbolic parameters
                                            ing all 50 hard negatives; the sole error is an      and recognize equivalence across heterogeneous
                                            incomplete mapping extraction.                       representations, such as an LP becoming an NLP
                                                                                                 under a variable transformation. Thus, optimal-
                                        1   Introduction
                                                                                                 value comparison, sampled solutions, and syntactic
                                        Optimization is central to scientific and engineering    similarity produce both false positives/negatives.
                                        decision-making, with applications in energy-cost           Recent work has begun to study LLM-
                                        reduction, supply-chain planning, and profit maxi-       assisted equivalence checking. In particular,
                                        mization (Singh, 2012). Combinatorial optimiza-          EquivaMap (Zhai et al., 2025) uses LLMs to in-
                                        tion (Le, 2024) further underpins core problems          fer transformations between decision variables and
                                        in operations research and computer science, from        then verifies that the mapped formulations preserve
                                        network routing (Christofides et al., 1981) to ma-       feasibility and optimality. While this is an impor-
                                        chine learning system design (Sun et al., 2019). Un-     tant step toward automated reformulation analysis,
                                        derstanding when two optimization problems are           the broader challenges in Figure 1 require verifica-
                                        equivalent, or when one reduces to another (Karp,        tion that is robust to inactive constraints, scaled or
                                        2009), is therefore fundamental: it enables struc-       monotone objectives, symbolic parameters, and het-
                                        turally related NP-complete problems (Aaronson,          erogeneous linear/nonlinear representations. Tra-
                                        2005), such as SAT and the Traveling Salesperson         ditional testing cannot exhaustively cover these se-
                                        problem (Pop et al., 2024), to be organized into         mantic boundaries (Mahmoud et al., 2024), and
                                        equivalence classes (Paulson, 2006) and solved us-       the brittleness of generative modeling further moti-
                                        ing transferable algorithmic ideas (Liu et al., 2022).   vates provable validation mechanisms (Chen et al.,
            (a) Identical optimum scenario                 (b) Diff. optimal values, yet arg min equivalent




               (c) Symbolic formulations                              (d) Nonlinear transformation

Figure 1: Challenges in assessing optimization reformulations. (a) Existing methods may fail to distinguish
genuinely different problems when inactive constraints yield the same optimizer and objective value. (b) Conversely,
they may incorrectly flag equivalent formulations with scaled objectives as different. (c) Robust reformulation anal-
ysis should also be parameter-agnostic, and (d) capable of recognizing equivalence across nonlinear representations.

2026) that separate structural interpretation from            duce SOVER, an LLM-assisted SMT framework
logical verification (Pei et al., 2025).                      that encodes reformulation correctness as logical
   We propose SOVER, a hybrid framework for prov-             verification conditions over symbolic domains.
ably correct optimization reformulation. SOVER              • Equivalence beyond objective-value matching.
uses LLMs to parse optimization statements, align             SOVER verifies domain cross-feasibility & global
variables and parameters, and propose symbolic                objective-order preservation, avoiding failures
correspondences. It then discharges verification              from inactive constraints or scaled objectives.
obligations using SMT solvers under a shared logi-          • Parameter-agnostic and heterogeneous check-
cal representation. Instead of relying on agreement           ing. SOVER supports symbolic parameters and
over finitely many solver executions, SOVER checks            verifies equivalence across different mathemati-
domain cross-feasibility and global objective-order           cal representations, including LP-to-NLP refor-
preservation, thereby establishing arg min equiv-             mulations induced by variable transformations.
alence. Moreover, SOVER solves only the trusted             • Solver-efficient verification. SOVER requires
source optimization problem and verifies reformu-             solving only the trusted source problem and uses
lation correctness through SMT-based feasibility              SMT queries to verify feasibility and ordering
and ordering checks, enabling efficient validation            obligations, rather than validating reformulations
across mixed-integer linear, continuous nonlinear,            through independent optimal-value comparisons.
and non-convex settings.                                      On EquivaFormulation, Z3 verification averages
This paper makes the following contributions:                 0.03 s per pair; end-to-end latency is dominated
• Formal reformulation verification. We intro-                by LLM-assisted mapping.
• Support for mixed-integer and nonlinear set-          semantic alignment with SMT-based formal checks
  tings. The framework integrates Z3 for mixed-         for LPs, MILPs, and nonlinear reformulations.
  integer linear formulations and dReal for contin-
  uous nonlinear formulations via δ-satisfiability.     3     Preliminaries
                                                        3.1    Constrained Mathematical Optimization
• NLE QUIV-150 benchmark.             We release
  100 equivalent and 50 hard non-equivalent             A constrained minimization problem is written as
  application-grounded nonlinear pairs spanning
                                                                              min f (x),
  objective, constraint, equality/direction/coeffi-                           x∈X
  cient, and transformation-range failures.
                                                        where f : Rn → R is the objective and X ⊆ Rn
2   Related Work                                        is the feasible region induced by the problem con-
                                                        straints. When comparing formulations, equality
Large Language Models and Tool Integration.             of optimal objective values is not sufficient: the
Recent advances in natural language processing          relevant object is often the optimal solution set,
have produced Large Language Models (LLMs)
that perform strongly across question answering         arg min f (x) = {x⋆ ∈ X | f (x⋆ ) ≤ f (x), ∀x ∈ X }.
                                                            x∈X
(Brown et al., 2020), summarization, translation
(Grattafiori et al., 2024; Team et al., 2023), and      Two formulations are arg min equivalent if a map-
code generation (Chen et al., 2021). Their capabil-     ping Σ between their feasible domains maps the
ities are further strengthened through integration      minimizers of one formulation onto the minimizers
with external tools for code execution, debugging,      of the other. This allows equivalent formulations
and iterative refinement (Qin et al., 2024).            to have different numerical optimum values, for
LLMs in Mathematical Optimization. Recent               example when one objective is a positive scaling or
work has explored LLMs in operations research and       strictly increasing transformation of the other.
mathematical optimization, either by generating so-
                                                        3.2    Satisfiability Modulo Theories (SMT)
lutions directly through iterative prompting (Yang
et al., 2024) or by assisting modeling workflows.       SMT extends Boolean satisfiability to first-order
(Chen et al., 2024) developed a chatbot for diagnos-    formulas over background theories such as real
ing and repairing infeasible Pyomo models, while        arithmetic, integer arithmetic, arrays, bit-vectors,
OptiMUS (AhmadiTeshnizi et al., 2024) translates        and uninterpreted functions. In verification, SMT
natural language descriptions into MILP formula-        solvers prove a property φ by checking whether its
tions and debugs solver code through automated          negation ¬φ is satisfiable. A SAT result gives a con-
testing. These efforts reflect a larger push toward     crete counterexample, while UNSAT certifies that no
foundation models and self-improving agents for         counterexample exists within the specified theory.
diverse optimization instances (Li et al., 2025a;       This makes SMT well suited to reformulation ver-
Zhou et al., 2025).                                     ification: instead of relying on sampled instances
Formal Equivalence Checking and Verification.           or heuristic solver behavior, the verifier directly
As LLM-based optimization tools evolve from as-         asks whether any feasible assignment violates the
sistants to automated formulation engines (Li et al.,   claimed equivalence.
2025b), verification becomes a central bottleneck.
                                                        4     Proposed Methodology
Generative models may produce syntactically dif-
ferent formulations for the same problem (Herrera-      SOVER verifies whether two optimization formula-
Poyatos et al., 2025), which makes surface-level        tions represent the same underlying optimization
matching insufficient. Building on Karp reductions,     problem under a candidate reformulation map. The
EquivaMap (Zhai et al., 2025) uses LLMs to in-          framework separates the task into two components:
fer mappings between decision-variable spaces and       an LLM-assisted mapping module proposes cor-
applies lightweight verification to assess structural   respondences between variables and parameters,
equivalence. More broadly, the safe deployment          while an SMT-based verifier checks whether these
of generative AI in decision-making pipelines (Shi      correspondences preserve feasible regions and ob-
et al., 2024) requires the coupling of LLM-based        jective order. This design allows the LLM to assist
modeling with rigorous verification. Our work fol-      with structural interpretation, while all equivalence
lows this direction by combining LLM-assisted           claims are discharged by formal logical queries.
4.1     Mapping Generation                                The verifier then checks two properties. First, it
Verifying reformulation equivalence requires align-    checks domain cross-feasibility, namely whether
ing the semantic components of the two models.         both formulations define the same feasible set af-
Given a source formulation PA and a target formu-      ter substitution. Second, it checks objective-order
lation PB , SOVER constructs candidate mappings        preservation, namely whether the two objectives in-
for both decision variables and problem parameters.    duce the same weak ordering over all feasible pairs
These mappings define the substitutions used by        of points. This second condition is weaker than
the SMT verifier to express both formulations in a     algebraic objective identity and therefore accepts
shared symbolic coordinate system.                     valid transformations such as positive rescalings
                                                       and strictly monotone objective transformations.
4.1.1    Decision Variable Mapping                        As shown in Figure 2, the pipeline proceeds from
We build on the LLM-assisted mapping discov-           parsing & symbol declaration to mapping synthesis,
ery strategy of EquivaMap (Zhai et al., 2025),         feasibility verification, and order-profile checking.
which uses semantic information to identify corre-
                                                       4.3    Two-Stage SMT Verification
spondences and transformations between decision-
variable spaces. However, zero-shot mapping ex-        Algorithm 1 summarizes the core verification rou-
traction can produce ambiguous or many-to-one          tine. The key idea is to express both formulations
correspondences. To reduce such errors, SOVER          in a common symbolic environment and search for
applies a single refinement pass using a targeted      counterexamples to equivalence. If no feasibility
prompting template (Figure 3, Appendix). This          counterexample exists and no objective-order coun-
refinement enforces mapping uniqueness and re-         terexample exists, the reformulation is certified as
moves inconsistent assignments in which multiple       arg min-equivalent under the proposed map.
source variables map to the same target variable       4.3.1 Correctness Guarantee
without an explicit aggregation rule.
                                                       The soundness of SOVER follows from the fact that
4.1.2    Parameter Mapping                             the SMT queries search directly for counterexam-
Equivalent reformulations often transform not only     ples to feasibility & arg min equivalence.
variables but also instance parameters, such as ob-    Proposition 1 (Argmin Equivalence via
jective coefficients, right-hand side bounds, capac-   Weak-Order Preservation). Let PA and PB
ities, or scaling constants. We therefore extend       be two minimization problems. After applying
the semantic matching procedure beyond decision        the candidate substitution map Σ, let CA (x) and
variables and extract parameter-level correspon-       CeB (x) denote their feasible-region predicates
dences as well. The extracted parameter relations      in a common coordinate system, and let OA (x)
are passed through an analogous correction prompt      and OeB (x) denote their corresponding objective
(Figure 4, Appendix) before symbolic verification.     functions. Suppose the following two properties
                                                       hold:
4.2     Equivalence Checker
Given the candidate variable and parameter map-         ∀x,    CA (x) ↔ C
                                                                        eB (x),                         (1)
pings, SOVER constructs a formal verification prob-     ∀x, y, CA (x) ∧ CA (y) ⇒
lem using Z3. Each formulation is parsed into a
                                                          h                                  i
                                                            OA (x) ≤ OA (y) ↔ O
                                                                              eB (x) ≤ O
                                                                                       eB (y) . (2)
constraint predicate and an objective expression.
Specifically, for formulation PA , we write CA (x)     Then the two formulations have identical global
for its feasible-region predicate and OA (x) for its   minimizers in the common coordinate system:
objective. The target formulation PB is translated
into the source coordinate system using the pro-               arg min OA (x) = arg min O
                                                                                        eB (x).         (3)
posed substitution map, producing a mapped predi-               x:CA (x)           x:C
                                                                                     eB (x)

cate CeB (x) and mapped objective O  eB (x). When
                                                       If Σ is induced by a bijective coordinate trans-
PB contains auxiliary/slack variables that do not
                                                       formation between the original variables of PA
enter its objective, CeB (x) denotes the existential
                                                       and PB , then the corresponding minimizer sets are
projection of those variables, so Proposition 1 is
                                                       equivalent under that transformation.
applied to the projected feasible set rather than to
the lifted coordinates themselves.                     Proof. See Appendix A.2 for detailed proof.       ■
 Variation ID      Variation Type                                                                   Equivalent
 _c                Rename parameters and variables                                                     Yes
 _d                Binary substitution of decision variables                                           Yes
 _f                Replace objective term by an equivalent constraint                                  Yes
 _g                Add slack variables                                                                 Yes
 _h                Linear substitution of decision variables                                           Yes
 _i                Rescale the objective function                                                      Yes
 _j                Replace the formulation by an unrelated formulation                                 No
 _k                Convert an unrelated formulation into a feasibility problem                         No
 _l                Drop constraints that are inactive at the observed optimum                          No
 _m+               Nonlinear/non-convex coordinate reformulations                                      Yes
 _m−               Near-equivalent nonlinear reformulations with subtle semantic mismatch              No

Table 1: Taxonomy of problem variations and expected reformulation equivalence. Rows _c–_l follow (Zhai et al.,
2025); the _m+ and _m− nonlinear categories are introduced in NLE QUIV-150.




Figure 2: SOVER verification pipeline. The framework parses optimization models, synthesizes variable and
parameter alignments, checks domain cross-feasibility, and verifies preservation of the objective-order profile.

4.4     Extension to Nonlinear Programs via               requiring tolerance-aware interpretation.
        dReal
                                                             A raw δ-SAT result for a strict boundary-negation
The Z3-based verifier is well suited to linear,           query can be produced by the δ-weakening even
mixed-integer, and piecewise-linear arithmetic.           when the exact mismatch set is empty. We there-
However, reformulations involving transcendental          fore search only for margin-separated nonlinear
functions, nonlinear coordinate transformations, or       violations, using a separation margin strictly larger
non-convex continuous constraints may fall out-           than δ. Moreover, the PA → PB feasibility direc-
side the decidable fragments handled by standard          tion is checked as a forward-map range-coverage
SMT procedures. To support such cases, SOVER ex-          property: an A-feasible point is a counterexam-
tends the same verification logic using the dReal         ple only if no B-feasible point maps sufficiently
δ-complete decision procedure.                            close to it. This avoids falsely certifying a non-
4.4.1    δ-Satisfiability                                 surjective transformation and does not require a
                                                          globally single-valued inverse for the rejection of a
For nonlinear real arithmetic with transcendental         bad map.
functions, exact satisfiability is generally undecid-
able. dReal addresses this by deciding formulas              Some nonlinear reformulations introduce auxil-
up to a user-specified numerical tolerance δ > 0.         iary variables, such as slack variables, lifted vari-
Given a formula F, dReal returns either UNSAT,            ables, or projection variables, that do not appear
certifying that F has no solution, or δ-SAT, indi-        explicitly in the source formulation. SOVER handles
cating that a δ-weakened version of the formula           such variables through quantified feasibility checks,
may be satisfiable. In our pipeline, UNSAT is treated     ensuring that auxiliary degrees of freedom do not
as a formal certificate, while δ-SAT is treated as a      create spurious mismatches between the projected
candidate counterexample or an inconclusive result        feasible regions.
Algorithm 1 SOVER: SMT-Based Verification of           the nonlinear verifier checks whether exact mini-
Reformulation Equivalence                              mizers of one formulation map into the ϵ-optimal
Require: Source problem PA , target problem PB ,       region of the other formulation, and vice versa.
    variable mapping MV , parameter mapping              For a minimization problem P with feasible set
    MP                                                 X and objective O, define
Ensure: Status in {Pass,               Feasibility                                                 
    Mismatch,          Ordering           Mismatch,       Ωϵ (P ) = x ∈ X O(x) ≤ inf O(y) + ϵ .
                                                                                       y∈X
    Inconclusive}
 1: E ← ∅         ▷ Initialize symbolic environment    Proposition 2 (ϵ-Argmin Preservation under
 2: D ECLARE S YMBOLS(PA , E)                          δ-Complete Verification). Let PA and PB be non-
 3: D ECLARE S YMBOLS(PB , E)                          linear continuous minimization problems whose
 4: CA , OA ← PARSE M ODEL(PA , E)                     global minima are attained, with feasible sets XA
 5: CB , OB ← PARSE M ODEL(PB , E)                     and XB . Let Σ : XB → XA be a bijective coordi-
 6: Σ ← B UILD S UBSTITUTIONS(MV ∪ MP , E)             nate transformation on the feasible sets. Suppose
    eB ← S UBSTITUTE(CB , Σ)
 7: C                                                  the two feasibility-mismatch queries are UNSAT,
    eB ← S UBSTITUTE(OB , Σ)
 8: O                                                  and dReal also returns UNSAT for both margin-
 9: Γ ← S HADOW C OPY(Vars(PA ))                       separated optimization-mismatch formulas assert-
      (2)     (2)
10: CA , OA                                      ←     ing that an exact minimizer of one problem is
    S UBSTITUTE(CA , Γ), S UBSTITUTE(OA , Γ)           mapped to a point that can be improved by more
    e (2) , O
11: C       e (2)                                ←     than ϵ in the other problem. Then
      B      B
    S UBSTITUTE(CB , Γ), S UBSTITUTE(OB , Γ)
                     e                      e
                                                       Σ(Ω0 (PB )) ⊆ Ωϵ (PA ), Σ−1 (Ω0 (PA )) ⊆ Ωϵ (PB ).
12: // Stage 1: domain cross-feasibility
                                                       Here UNSAT is an exact certificate for the original
13: Assert ¬(CA ↔ C
                  eB )
                                                       mismatch formula; a δ-SAT result is not used as an
14: r ← C HECK S ATISFIABILITY
                                                       equivalence certificate.
15: if r = SAT then
16:     return Feasibility Mismatch                    Proof. See Appendix A.3 for detailed proof.       ■
17: else if r = UNKNOWN then
18:    return Inconclusive                             4.5   Implementation Details
19: end if                                             The implementation operates in four stages.
                                                       1. Parsing and bounded unrolling. The in-
20: // Stage 2: objective-order preservation              put formulations are programmatic gurobipy
21: Reset solver context                                  strings. SOVER removes solver API syntax, such
22: Assert CA ∧ C
                eB
                                                          as addConstr and setObjective, and extracts
              (2)  e (2)
23: Assert CA
               ∧ CB                                     the underlying algebraic constraints and objec-
                         (2)        e (2) )
24: Assert ¬ (OA ≤ OA ) ↔ (O   eB ≤ O
                                      B                   tive expressions. For benchmark evaluation,
25: r ← C HECK S ATISFIABILITY                            indexed variables and matrix expressions are
26: if r = SAT then                                       unrolled to a fixed proxy dimension. This certi-
27:      return Ordering Mismatch                         fies the resulting instantiated model; dimension-
28: else if r = UNKNOWN then                              parametric verification would require an addi-
29:      return Inconclusive                              tional induction or quantified-array argument.
30: else                                               2. Symbol declaration and substitution. Ex-
31:      return Pass                                      tracted variables and parameters are declared in
32: end if                                                the SMT environment using their native sorts, in-
                                                          cluding Boolean, integer, and real symbols. The
                                                          verified variable and parameter mappings are
4.4.2   ϵ-Argmin Equivalence                              then converted into a substitution dictionary that
For nonlinear objectives, exact order preservation        expresses the target formulation in the source
may be too brittle near boundary points or flat re-       coordinate system.
gions. We therefore use an ϵ-argmin relaxation. In-    3. Feasibility verification. The verifier searches
stead of requiring exact equality of minimizer sets,      for an assignment satisfying ¬(CA ↔ C     eB ). A
    satisfying assignment is a concrete feasibility      unless explicit indexing is present (examples in Ap-
    counterexample. If the formula is unsatisfiable,     pendix, Figure 6). We evaluate nine transformed
    the two formulations define the same feasible        versions of each original formulation and exclude
    region after substitution.                           variation _e (added valid inequalities), since our
4. Objective-order verification. The verifier in-        focus is structural equivalence rather than instance-
   troduces a shadow copy of all source variables        specific or solver-dependent behavior.
   to represent a second feasible point. It then
                                                         5.2 Experimental Setup & Problem Variations
   searches for two feasible points whose objective
   order differs across the two formulations. Un-        Each benchmark instance pairs an original opti-
   satisfiability of this query certifies global weak-   mization formulation with one transformed formu-
   order preservation, and therefore arg min equiv-      lation. Table 2 reports the number of correctly clas-
   alence by Proposition 1.                              sified instances for each subtype. The expanded
                                                         evaluation contains 2328 pairs in Table 2: 2178
   For each benchmark pair, SOVER records the ver-       EquivaFormulation pairs and 150 NLE QUIV-150
ification status, generated SMT formulas, solver         pairs.
outputs, counterexamples when available, and di-
agnostic metadata in a structured csv file.              5.3   Baselines
                                                         We compare against five baselines:
5     Experiments and Evaluation                         • EquivaMap (Zhai et al., 2025): LLM-derived
We evaluate SOVER on reformulation pairs derived           variable mappings followed by feasibility/opti-
from the EquivaFormulation dataset1 introduced             mality checks.
                                                         • Naive LLM Prompting: Zero-shot binary equiv-
by (Zhai et al., 2025). EquivaFormulation modifies
                                                           alence classification (Zhai et al., 2025) without
problems from the NLP4LP corpus2 (AhmadiTesh-
                                                           explicit mappings or solvers.
nizi et al., 2024) using semantic and algebraic
                                                         • Gemini-CoT: Chain-of-Thought classification
transformations, summarized in Table 1. We addi-
                                                           (Team et al., 2023; Wei et al., 2022) with interme-
tionally introduce NLE QUIV-150, 150 application-
                                                           diate structural reasoning (prompt in Appendix,
grounded continuous nonlinear pairs: 100 equiva-
                                                           Figure 5).
lent pairs related by diverse nonlinear coordinate       • Weisfeiler-Lehman Graph Test (WLT) (Dou-
transformations and 50 hard negatives with subtle          glas, 2011): Bipartite formulation graphs com-
semantic mismatches. The positives span expo-              pared by iterative color refinement.
nential/log, softplus, reciprocal, square/root, logis-   • Canonical Accuracy: Exact character-level dec-
tic/odds, hyperbolic, shifted-exponential, and cubic       laration matching.
transformations; the negatives span 11 objective,
constraint, equality/direction/coefficient, and range-   5.4   Results and Analysis
mismatch mechanisms. Formulations, mappings,             On EquivaFormulation, SOVER correctly classi-
labels, metadata, and code are publicly available        fies 2173/2178 MILP pairs (99.77%): 1446/1449
at https://github.com/baranwa2/SOVER. For                equivalent and 727/729 non-equivalent. It ob-
nonlinear verification, the forward map is primary:      tains 242/243 on objective rescaling (_i), where
SOVER checks mapped feasibility and reverse range        canonical matching obtains 0/243, and perfect ac-
coverage using dReal with δ = 10−5 , separation          curacy on objective-to-constraint (_f) and linear-
margin 10−3 , and ϵ = 10−3 .                             substitution (_h) variants. For the challenging
                                                         non-equivalent _l subtype, where inactive con-
5.1    Data Cleaning
                                                         straints are removed without necessarily changing
Before evaluation, we clean metadata that would          an observed optimum, explicit feasibility checking
otherwise corrupt SMT declarations: qualitative          yields 241/243. These results show the benefit of
dimension descriptors (e.g., “positive,” “continu-       feasible-region and objective-order reasoning over
ous,” “non-negative”) are removed by regex, and          surface or single-optimum agreement.
empty/non-indexed shapes are treated as scalars             Our reproduction of EquivaMap with its re-
                                                         leased code and multiple frontier LLM backends
   1
     huggingface.co/datasets/humainlab/
EquivaFormulation                                        obtains 1935/2178 (88.84%), including 186/243
   2
     huggingface.co/datasets/udell-lab/NLP4LP            on _h and 166/243 on _i. The observed errors are
         Subtype     Total    SOVER     EquivaMap        WLT       Naive      Gemini     Canonical
                              (Ours)                              Prompt      Aided      Accuracy
         _c           243      243           234          243       152        226         224
         _d           234      234           207           63        56         79          58
         _f           243      243           233            0        84        110           0
         _g           243      241           234           51        57         60          42
         _h           243      243           186           51         1          6          0
         _i           243      242           166          243        82        157          0
         _j           243      243           241          232       239        238         243
         _k           243      243           237          243       243        242         243
         _l           243      241           197          243       243        240         243
         _m+          100       99            –             –        –          –           –
         _m−          50        50            -             –        –          –           –

Table 2: Comparative performance across problem-transformation subtypes. Entries report the number of correctly
classified instances. NLE QUIV-150 comprises _m+ (100 equivalent) and _m− (50 hard non-equivalent) pairs.
Counts are end-to-end with LLM-extracted mappings; the sole _m+ miss is an incomplete map. Baselines target
the original EquivaFormulation setting and are omitted for these new pairs.


concentrated in cases requiring precise mappings:        verses; forward-map range checking still rejects all
inaccurate, incomplete, or non-unique single-shot        three. Overall accuracy is 149/150 = 99.33% on
mappings propagate to the final decision, whereas        NLE QUIV-150 and 2322/2328 = 99.74% includ-
SOVER formally checks the proposed alignment             ing EquivaFormulation.
through SMT feasibility and ordering obligations.           Runtime decomposition. We do not claim
In order to prove robustness of our framework,           end-to-end speed superiority: SOVER averages
we have also evaluated SOVER directly on Formu-          7.07 s per EquivaFormulation pair versus 2.60 s
lationBench (Robbins et al., 2026), beyond the           for EquivaMap. Yet Z3 verification itself averages
EquivaFormulation data used in the original sub-         only 0.03 s (about 0.4%); almost all remaining time
mission. We conducted 116 formulation-level              is LLM-assisted mapping/refinement. Thus, robust-
equivalence tests spanning all 20 base problems:         ness is obtained through stricter upstream semantic
5 from EquivaFormulation (Zhai et al., 2025), 7          alignment, while certification is inexpensive: once
from EvoCut(Yazdani et al., 2026), and 8 from            a candidate map is available, SOVER verifies feasi-
(Ferchtandiker et al., 2025). SOVER correctly classi-    bility/order obligations directly rather than indepen-
fies 111/116 cases (95.69%). The latest version of       dently solving both formulations and comparing
FormulationBench contains 109 formulations, but          optima. The advantage is therefore robust, low-cost
our experimentation is based on the version as of        verification—not lower present end-to-end latency.
12 July 2026. The detailed results are highlighted
in Table 4.                                              6   Conclusion and Future Work
   Nonlinear benchmark analysis. On NLE QUIV-            We presented SOVER, an LLM-assisted SMT frame-
150, the LLM recovers 99/100 intended positive           work for verifying optimization reformulations.
forward maps and SOVER certifies those same 99;          Rather than comparing solver outputs empirically,
the only miss is an incomplete extracted map.            SOVER encodes correctness as logical obligations
SOVER rejects all 50 hard negatives. These include       over symbolic domains. For Z3 cases, cross-
five cases each of eight mismatch types (constraint      feasibility and objective-order preservation certify
tightening/addition/omission, functional mismatch,       exact arg min equivalence; for nonlinear dReal
objective linear perturbation, equality mismatch,        cases, margin-separated UNSAT queries certify the
objective risk-target shift, coefficient mismatch),      stated ϵ-argmin guarantee. Experimentation using
four direction mismatches, and three each of             EquivaFormulation shows that SOVER substantially
objective-target and nonlinear-range mismatches.         outperforms prompting, syntactic, graph-based,
Of three imperfect negative mapping records, one         and mapping-based baselines, particularly in cases
has an incorrect forward map and two have correct        where equivalence cannot be inferred from optimal
non-injective tanh2 (·) maps with single-branch in-      values alone.
       Metric                           SOVER        EquivaMap   WLT     Naive   Gemini   Canonical
                                      (End-to-End)                      Prompt   Aided    Accuracy
       End-to-end time (s)                 7.07        2.60      1.01    1.17     2.18      7.04
       Formal verifier only (s)         0.03 (Z3)        –         –       –       –         –

Table 3: Average approximate evaluation time per instance. For SOVER, 7.07 s is the complete mapping-plus-
verification pipeline, whereas the Z3 verification stage alone averages 0.03 s.


  Variation     Total    Mismatches          Correct
  _a              20              0             20
  _b              20              1             19
  _c              12              1             11
  _d              12              1             11
  _e              10              1              9
  _f              9               1              8
  _g              9               0              9
  _h              9               0              9
  _i              9               0              9
  _j              6               0              6
  Total          116              5            111

Table 4: Performance of SOVER across different formu-
lation variations in FormulationBench.


   Several directions remain open. Improving
LLM-based mapping synthesis could reduce in-
conclusive cases, while extending the verifier be-
yond bounded instances to dimension-parametric
formulations would provide stronger guarantees
for problem families. Although the dReal exten-
sion supports nonlinear continuous reformulations
via δ-satisfiability, tighter tolerance-aware certifi-
cates for non-convex models remain important. Fi-
nally, integrating SOVER into automated modeling
pipelines could provide end-to-end safeguards for
LLM-generated formulations before deployment in
high-stakes settings.
Limitations                                                with (mi) LP Solvers and Large Language Models.
                                                           arXiv preprint arXiv:2402.10172.
Although our SMT-driven framework demonstrates
                                                         Tom Brown, Benjamin Mann, Nick Ryder, Melanie
high reliability in verifying structural equivalence,      Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
it is subject to several operational limitations. Pri-     Neelakantan, Pranav Shyam, Girish Sastry, Amanda
marily, the system is bottlenecked by its depen-           Askell, and 1 others. 2020. Language Models are
dence on the upstream LLM mapping phase; be-               Few-shot Learners. Advances in neural information
                                                           processing systems, 33:1877–1901.
cause the deterministic solver relies on these gener-
ated alignments, any failure by the language model       Hao Chen, Gonzalo E Constante-Flores, and Can Li.
to extract a precise, unique mapping—particularly          2024. Diagnosing Infeasible Optimization Problems
                                                           using Large Language Models. INFOR: Information
in highly convoluted or obfuscated reformula-              Systems and Operational Research, 62(4):573–587.
tions—directly results in a verification failure. Sec-
ondly, relying on an SMT solver like Z3 introduces       Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
                                                          Henrique Ponde De Oliveira Pinto, Jared Kaplan,
inherent scalability challenges. While highly ef-
                                                          Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
fective for standard formulations, symbolic verifi-       Brockman, and 1 others. 2021. Evaluating Large
cation can experience exponential computational           Language Models Trained on Code. arXiv preprint
overhead when applied to massive, industrial-scale        arXiv:2107.03374.
models with thousands of integer variables and con-      Yitian Chen, Jingfan Xia, Siyu Shao, Dongdong Ge, and
straints. Finally, as observed in specific edge cases      Yinyu Ye. 2026. Solver-informed RL: Grounding
involving slack variables, our current feasibility          Large Language Models for Authentic Optimization
parser relies on a fixed unrolling proxy depth. This        Modeling. Advances in Neural Information Process-
                                                            ing Systems, 38:106027–106069.
architectural choice occasionally restricts the en-
gine’s ability to resolve deeply nested inequalities     Nicos Christofides, Aristide Mingozzi, and Paolo Toth.
or complex nonlinear bounds, presenting a poten-           1981. Exact Algorithms for the Vehicle Routing
                                                           Problem, based on Spanning Tree and Shortest Path
tial area for refinement in future iterations of the       Relaxations. Math. Program., 20(1):255–282.
pipeline.
                                                         Brendan L Douglas. 2011. The Weisfeiler-Lehman
                                                           Method and Graph Isomorphism Testing. arXiv
Ethical Considerations                                     preprint arXiv:1101.5211.
The deployment of automated verification frame-          Nathan Ferchtandiker, Dick den Hertog, Madeleine
works for optimization models carries several ethi-        Udell, and Segev Wasserkrug. 2025. Finding effi-
cal implications. A primary concern is automation          cient milo formulations with llms. Working paper.
bias in high-stakes domains (e.g., healthcare lo-        Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
gistics or resource allocation); practitioners might       Abhinav Pandey, Abhishek Kadian, Ahmad Al-
over-rely on automated approvals, potentially lead-        Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten,
                                                           Alex Vaughan, and 1 others. 2024. The Llama 3 Herd
ing to real-world mismanagement if a flawed model          of Models. arXiv preprint arXiv:2407.21783.
bypasses detection due to upstream extraction er-
rors. Additionally, while the SMT solver pro-            David Herrera-Poyatos, Carlos Peláez-González,
                                                           Cristina Zuheros, Andrés Herrera-Poyatos, Virilo
vides deterministic proofs, the LLM-based map-             Tejedor, Francisco Herrera, and Rosana Montes.
ping phase remains an opaque "black box," com-             2025. An Overview of Model Uncertainty and Vari-
plicating the full auditability of the verification        ability in LLM-based Sentiment Analysis: Chal-
pipeline. Finally, the environmental and compu-            lenges, Mitigation Strategies, and the Role of Ex-
                                                           plainability. Frontiers in Artificial Intelligence,
tational costs of querying large language models in        8:1609097.
tandem with resource-intensive symbolic solvers
must be carefully weighed in future deployments.         Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao,
                                                           and Benyou Wang. 2025. LLMs for Mathematical
                                                           Modeling: Towards Bridging the Gap Between Natu-
                                                           ral and Mathematical Languages. In Findings of the
References                                                 Association for Computational Linguistics: NAACL
                                                           2025, pages 2678–2710.
Scott Aaronson. 2005. NP-Complete Problems and
  Physical Reality. ACM Sigact News, 36(1):30–52.        Richard M Karp. 2009. Reducibility Among Combina-
                                                           torial Problems. In 50 Years of Integer Programming
Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell.       1958-2008: from the Early Years to the State-of-the-
  2024. Optimus: Scalable Optimization Modeling            Art, pages 219–241. Springer.
Phuong Le. 2024. A Survey on Combinatorial Opti-          Shiliang Sun, Zehui Cao, Han Zhu, and Jing Zhao. 2019.
  mization. arXiv preprint arXiv:2409.00075.                A Survey of Optimization Methods from a Machine
                                                            Learning Perspective. IEEE Transactions on Cyber-
Sirui Li, Janardhan Kulkarni, Ishai Menache, Cathy Wu,      netics, 50(8):3668–3681.
   and Beibin Li. 2025a. Towards Foundation Models
   for Mixed Integer Linear Programming. In Inter-        Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-
   national Conference on Learning Representations,         Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan
   volume 2025, pages 88590–88638.                          Schalkwyk, Andrew M Dai, Anja Hauth, Katie Mil-
                                                            lican, and 1 others. 2023. Gemini: A Family of
Wenhao Li, Bo Jin, Mingyi Hong, Changhong Lu,               Highly Capable Multimodal Models. arXiv preprint
 and Xiangfeng Wang. 2025b. Optimization Prob-              arXiv:2312.11805.
 lem Solving Can Transition to Evolutionary Agentic
 Workflows. arXiv preprint arXiv:2505.04354.              Yang Wang and Kai Li. 2025. Large Language Models
                                                            in Operations Research: Methods, Applications, and
Xinran Liu, Yuzhe Lu, Ali Abbasi, Meiyi Li, Javad           Challenges. arXiv preprint arXiv:2509.18180.
  Mohammadi, and Soheil Kolouri. 2022. Teaching
  Networks to Solve Optimization Problems. Preprint,      Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  arXiv:2202.04104.                                          Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
                                                             and 1 others. 2022. Chain-Of-Thought Prompting
Jingyuan Ma, Damai Dai, Zihang Yuan, Rui Li, Weilin          Elicits Reasoning in Large Language Models. Ad-
   Luo, Bin Wang, Qun Liu, Lei Sha, and Zhifang Sui.         vances in neural information processing systems,
   2026. Large Language Models Struggle with Un-             35:24824–24837.
   reasonability in Math Problems. In Proceedings of
   the AAAI Conference on Artificial Intelligence, vol-   Ziyang Xiao, Jingrong Xie, Lilin Xu, Shisi Guan,
   ume 40, pages 32428–32436.                               Jingyan Zhu, Xiongwei Han, Xiaojin Fu, WingYin
                                                            Yu, Han Wu, Wei Shi, and 1 others. 2025. A
Amira T Mahmoud, Ahmad A Mohammed, Mahitap
                                                            Survey of Optimization Modeling meets LLMs:
 Ayman, Walaa Medhat, Sahar Selim, Hala Zayed,
                                                            Progress and Future Directions. arXiv preprint
 Ahmed H Yousef, and Nahla Elaraby. 2024. Formal
                                                            arXiv:2508.10047.
 Verification of Code Conversion: A Comprehensive
 Survey. Technologies, 12(12):244.                        Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao
                                                            Liu, Quoc V Le, Denny Zhou, and Xinyun Chen.
Lawrence C Paulson. 2006. Defining Functions on
                                                            2024. Large Language Models as Optimizers. In In-
  Equivalence Classes. ACM Transactions on Com-
                                                            ternational Conference on Learning Representations,
  putational Logic (TOCL), 7(4):658–675.
                                                            volume 2024, pages 12028–12068.
Yu Pei, Yongping Du, and Xingnan Jin. 2025. "FoVer:
  First-Order Logic Verification for Natural Language     Jiayi Yao, Haibo Sun, and Nianwen Xue. 2025.
  Reasoning". Transactions of the Association for            Fact-checking AI-generated News Reports: Can
  Computational Linguistics, 13:1340–1359.                   LLMs Catch Their Own Lies?      arXiv preprint
                                                             arXiv:2503.18293.
Petrică C Pop, Ovidiu Cosma, Cosmin Sabo, and Co-
  rina Pop Sitar. 2024. A comprehensive survey on the     Milad Yazdani, Mahdi Mostajabdaveh, Samin Aref,
  generalized traveling salesman problem. European          and Zirui Zhou. 2026. Evocut: Strengthening inte-
  Journal of Operational Research, 314(3):819–835.          ger programs via evolution-guided language models.
                                                            Preprint, arXiv:2508.11850.
Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan
  Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang,       Haotian Zhai, Connor Lawless, Ellen Vitercik, and Liu
  Bill Qian, and 1 others. 2024. Toolllm: Facilitat-        Leqi. 2025. EquivaMap: Leveraging LLMs for Auto-
  ing Large Language Models to Master 16000+ Real-          matic Equivalence Checking of Optimization Formu-
  World Apis. In International Conference on Learn-         lations. arXiv preprint arXiv:2502.14760.
  ing Representations, volume 2024, pages 9695–9717.
                                                          Yisong Zhang, Ran Cheng, Guoxing Yi, and Kay Chen
Henry Robbins, Connor Lawless, Madeleine Udell, and         Tan. 2025. A Systematic Survey on Large Language
  Ellen Vitercik. 2026. Flare: Verifying milp reformu-      Models for Evolutionary Optimization: From Model-
  lations with llm-based theorem proving. Working           ing to Solving. arXiv preprint arXiv:2509.08269.
  paper.
                                                          Chenyu Zhou, Tianyi Xu, Jianghao Lin, and Dong-
Dan Shi, Tianhao Shen, Yufei Huang, Zhigen Li, Yongqi       dong Ge. 2025. Steporlm: A Self-evolving Frame-
  Leng, Renren Jin, Chuang Liu, Xinwei Wu, Zishan           work with Generative Process Supervision for Oper-
  Guo, Linhao Yu, and 1 others. 2024. Large Language        ations Research Language Models. arXiv preprint
  Model Safety: A Holistic Survey. arXiv preprint           arXiv:2509.22558.
  arXiv:2412.17686.
                                                          Kuo Zhou and Lu Zhang. 2025. Step-wise Formal Veri-
Ajay Singh. 2012. An Overview of the Optimiza-              fication for LLM-based Mathematical Problem Solv-
  tion Modelling Applications. Journal of Hydrology,        ing. arXiv preprint arXiv:2505.20869.
  466:167–182.
A     Appendix                                                • Structural Heuristics: To avoid proof cor-
                                                                ruption from superficial encoding differences,
GenAI Usage Disclosure
                                                                slack and auxiliary variables are automatically
We used OpenAI’s ChatGPT only to assist with                    isolated using regular expressions. These are
limited language refinement of the manuscript. We               parameterized as existentially quantified enti-
did not use GenAI tools for problem formulation,                ties (∃ slack), preventing them from disrupting
algorithm design, theoretical analysis, proof de-               the primary structural identity check.
velopment, code generation, data collection, data
preprocessing, experimental design, result genera-            • Computational Bounding: To manage unde-
tion, result analysis, or scientific interpretation. All        cidability boundaries and combinatorial explo-
technical content, experimental results, scientific             sion during SMT checking, each Z3 instance
claims, and conclusions are entirely the authors’               is constrained by a strict execution timeout of
own and were verified by the authors.                           10, 000 ms. This guarantees clean classifica-
                                                                tion into empirical results (Pass, Feasibility
A.1    Inference Hyperparameters and                            Mismatch, Objective Mismatch, or Runtime
       Evaluation Libraries                                     Error) without unbounded hanging.
LLM Generation Pipeline:
                                                           A.2   Proof of Proposition 1
    • Orchestration Framework: All generation              Proof. By Eq. (1), both formulations define the
      queries are orchestrated via the liteLLM ab-         same feasible set after substitution. Let this com-
      straction framework to interface uniformly           mon feasible set be X .
      with the GPT-5.4-mini deployment endpoint.             We first show that every minimizer of PA is also
    • Hyperparameter Configuration: To ensure              a minimizer of the mapped target problem. Let
      deterministic, reproducible structural align-        x⋆ ∈ arg minx∈X OA (x). Then, for every x ∈ X ,
      ments, the decoding temperature is strictly
                                                                           OA (x⋆ ) ≤ OA (x).
      set to τ = 0.0. The top_p parameter is
      fixed at 1.0, while both presence_penalty            Applying Eq. (2) with x⋆ and x gives
      and frequency_penalty are maintained at
      0.0 to eliminate stochastic variance in struc-                       eB (x⋆ ) ≤ O
                                                                           O          eB (x),
      tured JSON production.
                                                           for every x ∈ X . Hence x⋆ is also a global mini-
    • Prompt-Level Context Rules: Generative               mizer of the mapped target problem.
      behavior is bounded by a strict structural bi-          The reverse inclusion follows identically. If x⋆
      jection constraint, preventing the mapping of        minimizes O eB over X , then Eq. (2) implies that
      multiple distinct Problem 1 source variables to      OA (x ) ≤ OA (x) for every feasible x. Thus x⋆
                                                                 ⋆
      a singular Problem 2 target variable. Further-       also minimizes OA . Therefore, the two argmin sets
      more, a “scalar-by-default” logic is mandated,       are identical.                                   ■
      requiring explicit array indexing evidence be-
      fore declaring any variable a vector.                A.3   Proof of Proposition 2
Formal Verification Engine:                                Proof. We prove the first containment; the second
                                                           follows by applying the same argument to the bijec-
    • Model Parsing: The gurobipy API is uti-
                                                           tion Σ−1 . Suppose, for contradiction, that there ex-
      lized to extract and sanitize the underlying
                                                           ists x⋆ ∈ Ω0 (PB ) such that x′ = Σ(x⋆ ) ∈
                                                                                                    / Ωϵ (PA ).
      mixed-integer and linear programming mod-
                                                           Feasibility preservation ensures x′ ∈ XA . By the
      els, translating constraint and objective func-
                                                           definition of Ωϵ (PA ),
      tions into programmatic Python representa-
      tions.                                                          OA (x′ ) > inf OA (y) + ϵ.
                                                                                   y∈XA
    • Symbolic Evaluation: Core formal equiva-
      lence proofs are evaluated using the Z3 Theo-        Because the global minimum of PA is attained,
      rem Prover via the Z3-solver Python library,         choose y⋆ ∈ Ω0 (PA ). Then
      serving as the deterministic Satisfiability Mod-
      ulo Theories (SMT) backend.                                OA (y⋆ ) = inf OA (y) < OA (x′ ) − ϵ.
                                                                            y∈XA
Consequently, x⋆ is an exact minimizer of PB
whose mapped point in PA admits a feasible com-
petitor improving the objective by more than ϵ.
Hence the corresponding optimization-mismatch
formula is satisfiable. A sound dReal call therefore
cannot return UNSAT for that formula, contradicting
the hypothesis. Thus Σ(Ω0 (PB )) ⊆ Ωϵ (PA ). The
reverse containment follows symmetrically using
Σ−1 .
   The argument relies only on the soundness of
the UNSAT answer for the original mismatch for-
mula. A δ-SAT answer, which may arise from the
δ-weakening near a shared boundary, is intention-
ally not used to certify equivalence.             ■

A.4   Prompts
The secondary prompts for variable and param-
eter mapping generation, prompt for non-linear
mapping generation, the Gemini-aided Chain-of-
Thought (CoT) prompt for generation, and exam-
ples of dataset instances with dimensional issues
are provided in the subsequent parts of this ap-
pendix. The complete NLE QUIV-150 release—
including source/reformulated nonlinear formula-
tions, ground-truth and LLM-extracted mappings,
labels, mismatch metadata, and verification code—
is available at https://github.com/baranwa2/
SOVER.
You are an expert AI assistant mapping decision variables between two
optimization problems. Your goal is to find the equivalent variables in
Problem 2 for EVERY variable in Problem 1.
**Problem 1 (Reference):** -Variables: {json.dumps(vars1, indent=2)}
-Constraints:{json.dumps([c.get('formulation') for c in constraints1],indent=2)}
-Objective: {json.dumps(objective1.get('formulation',''),indent=2)}
**Problem 2 (Target):** -Variables:{json.dumps(vars2,indent=2)}
-Constraints:{json.dumps([c.get('formulation') for c in constraints2],indent=2)}
- Objective: {json.dumps(objective2.get('formulation', ''), indent=2)}
**Previous Incorrect Mapping (TO BE CORRECTED):** {json.dumps(old_mappings,
indent=2)}
**STRICT RULES FOR VARIABLE MAPPING:** 1. **MANDATORY CORRECTION (CRITICAL):**
   - The "Previous Incorrect Mapping" provided above is MATHEMATICALLY INVALID
   and FAILED equivalence tests.
   - You are strictly forbidden from returning the exact same mapping. You MUST
   identify the specific error internally (e.g., mismatched variable, inverted
   coefficient like using 10 instead of 0.1) and change it in your final output.
   - If you return the `old_mappings` unchanged, you have failed your core
   directive.
2. **CORE MAPPING LOGIC:**
   - Every Problem 1 variable MUST be mapped. Do NOT map to "none".
   - UNIQUE MAPPING: Do not map multiple different Problem 1 variables to the
   exact same Problem 2 variable (e.g., if x maps to x1 and x2, y must map to
   different variables, not x1 and x2).
   - ONE-TO-MANY: A single Problem 1 variable can be mapped to multiple Problem
   2 variables (e.g., digit-wise $x = x_0 + 10x_1$ or split variables $x = x_1
   + x_2$). Parts of a variable that cannot be detached must remain mapped to
   that specific variable.
   - SEMANTIC PRIORITY: Variable descriptions are crucial. Analyze the physical
   meaning alongside the mathematical formulation.
3. **COEFFICIENT & MATHEMATICAL PRECISION:**
   - DECIMAL CONVERSION: All fractions (e.g., `1/10`, `frac{{1}}{{100}}`,
   `1/100*j`) MUST be converted to decimal coefficients (e.g., `0.1`, `0.01`).
   - LINGUISTIC INVERSES: If the description states a Problem 2 variable is
   "100 times before" or "100 times larger" than Problem 1, use the inverse
   coefficient as **constant** (e.g., `0.01`) so that $P1\_var = 0.01 \times
   P2\_var$.
   - ALGEBRAIC CONSISTENCY: If you substitute your new mapping into Problem 1's
   equations, they must become identical to Problem 2's equations.
4. **FORMAT:**
   - Output ONLY a valid raw JSON object. No markdown formatting, no triple
   backticks, no explanations, no text outside the JSON.
   - Each mapping must be a list of objects: `{{"constant": float,
   "variable": "string"}}`.
Example Format:
{{ "P1_VarA": [{{"constant": 1.0, "variable": "P2_VarX"}}],
  "P1_VarB": [{{"constant": 0.1, "variable": "P2_VarY"}}, {{"constant": 0.01,
  "variable": "P2_VarZ"}}]}}



                    Figure 3: Prompt for Variable Mapping Correction
You are an expert AI assistant tasked with mapping parameters (constants)
between two optimization problems.Your goal is to find the exact
equivalent parameter in Problem 2 for EVERY parameter in Problem 1.To
help you, the CORRECT mapping of variables between these problems is provided.
You must also correct the PREVIOUSLY FAILED parameter mapping.
**Problem 1 (Reference):**
- Parameters: {json.dumps(params1, indent=2)} - Constraints:
{json.dumps([c.get('formulation') for c in constraints1], indent=2)}
- Objective: {json.dumps(objective1.get('formulation', ''), indent=2)}
**Problem 2 (Target):** - Parameters: {json.dumps(params2, indent=2)}
-Constraints:{json.dumps([c.get('formulation')for c in constraints2],indent=2)}
- Objective: {json.dumps(objective2.get('formulation', ''), indent=2)}
**Correct Variable Mappings (Use this context to align the equations):**
{json.dumps(var_mappings, indent=2)}
**Previous Incorrect Parameter Mapping (TO BE CORRECTED):**
{json.dumps(old_param_mappings, indent=2)}
--- **STRICT RULES FOR PARAMETER MAPPING:** 1. **CORE MAPPING LOGIC:**
   - Every Problem 1 parameter MUST be mapped. Do NOT map to "none".
   - 1-TO-1 MAPPING: Unlike variables, parameters map exactly 1-to-1. Do not map
multiple different Problem 1 parameters to the exact same Problem 2 parameter.
   - SEMANTIC MATCHING: Look at the parameter descriptions first. Costs map to
   costs, capacities map to capacities, limits map to limits. If words are not
   same look into the meanings they convey.
2. **USE THE VARIABLE MAPPING (ALGEBRAIC CONTEXT):**
   - You MUST use the provided `Correct Variable Mappings` to substitute
   Problem 2's variables into Problem 1's equations.
   - Use this substitution to see which parameters perfectly align in the newly
   balanced equations. 3. **COEFFICIENT RULE: 1.0 DEFAULT **
   - **DEFAULT TO 1.0:** In all cases, the constant for a parameter mapping is
   exactly `1.0`. Do not invent scaling differences or guess coefficients.
   (default 1.0 constant). If previously generated was not 1.0 change it to 1.0.
   - In rare cases it will be other value but if other value is submitted as old
   parameter mapping, then there is high chance that constant is actually 1.0
   (1.0 strictly and only no other value)
4. **MANDATORY CORRECTION (NO REPETITION ALLOWED):**
   - The "Previous Incorrect Parameter Mapping" is entirely WRONG. It failed our
   equivalence tests.
   - YOUR OUTPUT MUST CHANGE: You are strictly forbidden from outputting the
   exact same mapping you were given as the incorrect baseline.
   - DIAGNOSE THE FAILURE: The old mapping likely failed because it paired the
   wrong parameters, or it used a bizarre constant when it should have just been
   `1.0` (or vice versa, failing to apply a rare mathematical exception).
   Fix the error and output the corrected version. 5. **FORMAT:**
   - Output ONLY a valid raw JSON object. No markdown, no conversational text.
   - Each mapped value must be a list of objects representing the linear
   relationship: `{{"constant": float, "parameter": "string"}}`.
Example Output Format (Showing standard 1.0 and a rare exception):
{{"P1_ParamA": [{{"constant": 1.0, "parameter": "P2_ParamX"}}],
  "P1_ParamB": [{{"constant": 0.1, "parameter": "P2_ParamY"}}]}}


                   Figure 4: Prompt for parameter mapping correction
You are an expert mathematical optimization solver and formal verification
engine.
Your task is to rigorously determine if two Mixed-Integer Programming (MIP)
formulations (Problem A and Problem B) are strictly equivalent.
Two formulations are equivalent if and only if they share identical feasible
regions and objective contours. This means they can be perfectly mapped to one
another through:
1. 1-to-1 renaming of variables and parameters.
2. Algebraic rearrangement or scalar multiplication of constraints (e.g.,
$x + y \le 5$ is equivalent to $10 \ge 2y + 2x$).
3. Reordering of constraints or objective terms.
**Strict Parsing Rule:**
If a parameter or variable shape has only one value 'Integer', you must
strictly treat it as a scalar entity, not a vector.
**First problem formulation (Problem A):**
{prob1_str}
**Second problem formulation (Problem B):**
{prob2_str}
**Instructions:**
Think step-by-step. Provide a brief analysis mapping the variables,
parameters, objective functions, and constraints.
After your analysis, you MUST output your final decision on the VERY LAST
LINE of your response as exactly one of these two phrases:
Equivalent ; Not Equivalent


                   Figure 5: COT-based Prompt for Equivalence Check
--- Instance from problem_info.json in problem 169 (169_c) ---
"variables": {
        "v": {
            "description": "The total amount of journeys made by cargo planes",
            "type": "continuous",
            "shape": [
                "integer"
            ]
        },
        "n": {
            "description": "The quantity of oversized truck journeys",
            "type": "continuous",
            "shape": [
                "integer"
            ]
        }
--- Instance from problem_info.json in problem 220 (220_c) ---
 "variables": {
        "c": {
            "description": "A binary variable that signifies if any Calcium
            supplements are consumed.",
            "type": "continuous", "shape": ["Binary"]},
        "q": {
            "description": "Variable that is set to either 1 or 0 to show if any
            Vitamin D supplements have been consumed.",
            "type": "continuous", "shape": ["Binary"]},
        "f": {
            "description": "The overall duration required for the medications to
            take effect.",
            "type": "continuous", "shape": ["Continuous"]},
        "e": {
            "description": "The quantity of Calcium tablets consumed within a
            month.",
            "type": "continuous","shape": ["Integer"]},
        "h": {
            "description": "The quantity of Vitamin D capsules consumed within
            one month",
            "type": "continuous", "shape": [ "Integer"]}
            --------------------------------------------------


                     Figure 6: Examples with irrelevant dimensions
You are an expert mathematical optimizer and symbolic algebra engine.
Your job is to find the exact non-linear algebraic mapping between an original
optimization problem(Formulation A) and its reformulated version(Formulation B).
### Context
We have two versions of the same optimization problem:
- **Formulation A**: Uses bounded or restricted variables.
- **Formulation B**: Uses unconstrained latent variables to simplify
optimization.
### Data Inputs for Instance ID: {pair_id}
---
[FORMULATION A JSON]
{json_A_str}
---
[FORMULATION B JSON]
{json_B_str}
---
### Instructions
1. **Analyze Domains**: Look at the variable descriptions and constraints in
Formulation A (e.g., variable > 0, or 0 < variable < 1). Match them with
the unconstrained variables in
Formulation B.
2. **Match Expressions**: Compare the Objective Functions and the Constraints.
Identify how terms in Formulation A (like `log(CatalystDose)` or
`MixingRatio / (1 - MixingRatio)`) map directly to terms in Formulation
B (like `LatentDose` or `exp(LatentRatio)`).
3. **Derive the Forward Mapping**: Express each variable from Formulation A
explicitly as a function of the variables in Formulation B.
4. **Derive the Inverse Mapping**: Invert your forward equations to express each
variable from Formulation B explicitly as a function of the variables in
Formulation A.
### Output Format
Provide your final answer strictly in valid JSON format matching the schema
below. Do not include any conversational prose, explanations outside the JSON,
or markdown code blocks (like ```json).
{{ "pair_id": "{pair_id}",
  "formulation_A_to_B": {{
    "VariableA_1": "expression_in_terms_of_B",
    "VariableA_2": "expression_in_terms_of_B"
  }},
  "inverse_mapping": {{
    "VariableB_1": "expression_in_terms_of_A",
    "VariableB_2": "expression_in_terms_of_A"
  }}
}}"""


                   Figure 7: Prompt for non-linear mapping extraction
