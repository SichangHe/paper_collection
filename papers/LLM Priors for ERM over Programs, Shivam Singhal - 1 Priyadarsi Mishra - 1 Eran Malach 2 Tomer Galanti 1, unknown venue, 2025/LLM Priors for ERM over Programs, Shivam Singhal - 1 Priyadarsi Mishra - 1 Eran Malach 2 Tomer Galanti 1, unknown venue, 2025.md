                                                                           LLM Priors for ERM over Programs


                                                                Shivam Singhal * 1 Priyadarsi Mishra * 1 Eran Malach 2 Tomer Galanti 1


                                                                  Abstract                                      Step      Type                  Candidate function                                       Rationale

                                                                                                                        Candidate A
                                               We study program-learning methods that are ef-                    1
                                                                                                                        Candidate B
                                                                                                                                       Parity rule (Train acc: 50%)
                                                                                                                                       Digit-sum parity (Train acc: 49%)
                                                                                                                                                                                       No signal; try digit-sum thresholds.


                                               ficient in both samples and computation. Clas-                                          Digit-sum sweep        P
                                                                                                                 2      Refinement A   Best over t: ŷ(x) = 1{ i xi ≥ t}               Still weak; move to position-specific tests.
                                               sical learning theory suggests that when the tar-                                       (Train acc: 54%)


                                               get admits a short program description, for ex-
arXiv:2510.14331v3 [cs.LG] 2 Jul 2026




                                                                                                                                       Single-position equality
                                                                                                                 3      Candidate C    Best over (i, v): ŷ(x) = 1{xi = v}             Generalize to per-position thresholds.
                                                                                                                                       (Train acc: 60%).
                                               ample a short piece of “Python code”, it can be
                                                                                                                                       Single-position threshold
                                               learned from few examples by ERM over the pro-                    4      Candidate D    Best over t: ŷ(x) = 1{x0 ≥ t}
                                                                                                                                       (Train acc: 67%).
                                                                                                                                                                                       Try an XOR fit over digit-derived bits.


                                               gram class. However, this approach relies on enu-
                                                                                                                                       F2 fit on digit parities
                                               merating candidate programs, which is typically                   5        Analysis
                                                                                                                                       Solve Aw = y (mod 2); inconsistent.
                                                                                                                                                                                       Try coarser summaries (half-sums).



                                               exponential in the description length; gradient-                                        Half-sum features
                                                                                                                                       Let S1 =
                                                                                                                                                P50
                                                                                                                                                   i=1 xi , S2 =
                                                                                                                                                                 P100
                                                                                                                                                                    i=51 xi .
                                                                                                                 6      Candidate E    ŷ = 1{S1 > S2 } (Train acc: 45%)
                                                                                                                                                                                       Weak signal; pivot to modular structure.

                                               based training avoids this explicit search but, for                                     ŷ = 1{(S1 − S2 ) odd} (Train acc: 49%).


                                               some families of short programs, can require ex-                  7      Candidate F
                                                                                                                                       Mod-3 test
                                                                                                                                       ŷ(x) = 1{x mod 3 ̸= 0} (Train acc: 75%)
                                                                                                                                                                                       Modular signal; look for a sharper modulus-
                                                                                                                                                                                       based rule.

                                               ponentially many samples to succeed. We pro-
                                                                                                                                       Residue classifier
                                               pose LLM-PV, a propose-and-verify recipe that                     8        Analysis     Best m ∈ [2, 300] majority by x mod m
                                                                                                                                       (Train acc: 98%).
                                                                                                                                                                                       Points to a sieve-like decision rule.


                                               enables ERM-style selection over a discrete pro-                                        Divisibility probe
                                                                                                                 9      Refinement B   ŷ(x) = 1{¬(3|x) ∧ ¬(7|x)}                      Test more divisibility rules.
                                               gram class without exhaustive enumeration: a pre-                                       (Train acc: 84%)


                                               trained LLM induces a proposal distribution over                 10
                                                                                                                         Hypothesis
                                                                                                                                       Miller–Rabin primality test (Train acc: 100%)   Hypothesis confirmed.
                                                                                                                        Verification
                                               candidate programs, each proposal is executed
                                               and scored on a held-out validation set, and the                Figure 1. Reasoning trace for learning primality. The search
                                               best program is selected, with no gradient updates              starts from simple digit-level heuristics and progressively shifts
                                               or validation feedback used to adapt the sampling               toward modular structure: after parity and digit-sum baselines fail,
                                               distribution. Across algorithmic tasks including                residue-class predictors achieve high training accuracy, suggesting
                                               parity variants, pattern matching, and primality                a sieve-like mechanism. A direct Miller–Rabin primality test then
                                                                                                               verifies the hypothesis and matches the labels perfectly.
                                               testing, LLM-PV often recovers the exact under-
                                               lying rule from a small labeled set and generalizes
                                               far beyond the training sequence lengths, while
                                                                                                               examples (x, y) from an unknown rule, produce a predic-
                                               SGD-trained transformers, fine-tuning, in-context
                                                                                                               tor that generalizes to unseen inputs. A central lesson of
                                               learning, and classical ML baselines can fit the
                                                                                                               classical learning theory is that simplicity enables sample
                                               training data yet fail to generalize reliably. To-
                                                                                                               efficiency. In particular, for a finite hypothesis class H,
                                               gether, these results suggest that pretrained LLM
                                                                                                               empirical risk minimization (ERM) needs only Õ(log |H|)
                                               priors can serve as effective search biases for
                                                                                                               examples to generalize (Valiant, 1984; Vapnik, 1998). This
                                               ERM, narrowing the gap between statistical and
                                                                                                               immediately suggests a compelling perspective on program
                                               computational efficiency.
                                                                                                               learning: if the target rule can be implemented by a short
                                                                                                               program of length L over a token alphabet Σ, then the ef-
                                        1. Introduction                                                        fective hypothesis class size is at most |Σ|L , and hence
                                                                                                               Õ(L log |Σ|) labeled examples suffice.
                                        At its core, supervised learning asks for an algorithmic
                                        recipe for recovering structure from data: given labeled               The obstacle is computation. A direct implementation of
                                                                                                               ERM is length-first program enumeration: search all pro-
                                           1
                                           Department of Computer Science & Engineering, Texas A&M             grams of length at most L and return the first that fits the
                                        University, TX, USA 2 Kempner Institute, Harvard University, MA,       data. But P the number of candidates grows exponentially,
                                        USA. Correspondence to: Tomer Galanti <galanti@tamu.edu>.              |L≤L | =
                                                                                                                              L      ℓ           L
                                                                                                                              ℓ=1 |Σ| = Θ(|Σ| ), so even when verifica-
                                        Proceedings of the 43 rd International Conference on Machine           tion is fast, the overall runtime scales as Θ(m|Σ|L ). Thus,
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026           the classical route to sample-efficient learning of short pro-
                                        by the author(s).                                                      grams is computationally infeasible for even moderate L

                                                                                                           1
                                             LLM Priors for ERM over Programs

(e.g., L=20 and |Σ|=10 already yields 1020 candidates).                 spired by classic work on programming by example (PBE)
                                                                        and the growing literature on LLM-guided program syn-
Modern deep learning flips this trade-off. Instead of
                                                                        thesis, we introduce LLM-PV. LLM-PV is a propose-
searching explicitly over programs, one typically trains
                                                                        and-verify procedure that cleanly separates roles: (i) a
high-capacity predictors by stochastic gradient descent
                                                                        pretrained LLM induces a data-dependent proposal distri-
(SGD) (Robbins & Monro, 1951; Bottou, 2010). This is
                                                                        bution over candidate programs (or edits), (ii) an external
computationally attractive: the optimization cost is often
                                                                        verifier compiles and executes candidates, and (iii) we
nearly linear in the data, and large models can fit complex
                                                                        select by held-out validation error (Alg. 1). This makes
training sets. Yet computational tractability does not imply
                                                                        the role of pretrained reasoning precise: it serves as a
statistical efficiency on structured rule families. In the sta-
                                                                        search bias that concentrates trials on plausible hypothe-
tistical query (SQ) view (Kearns, 1998), broad classes of
                                                                        ses, while the learning objective and selection rule remain
gradient-based procedures can require exponentially many
                                                                        similar to ERM.
samples on high–SQ-dimension targets such as parity- and
cryptographic-like functions, despite the fact that these tar-        • Sample-efficient rule recovery and length generaliza-
gets admit succinct program descriptions. In other words,               tion across algorithmic tasks. Across algorithmic tasks
the difficulty is not that the rule is long or unstructured,            including parity variants, pattern matching, palindromes,
but that the learning algorithm accesses it through a bottle-           Dyck-2, primality variants and pseudo-random functions,
necked interface (gradients, finite precision, local updates)           LLM-PV often recovers the underlying rule from 200
that is poorly matched to discrete program structure.                   labeled examples (Tabs. 1 and 2), and frequently outputs
                                                                        compact, input-length-invariant programs that generalize
                                                                        far beyond the training length (Fig. 3). In the same set-
    Can we recover the sample efficiency of ERM over                    tings, classic ML methods (e.g., SVM, XGBoost), SGD-
     short programs without paying the full cost of                     trained transformers and standard adaptation baselines
               exhaustive enumeration?                                  (fine-tuning and in-context learning) commonly fit the
                                                                        training set but fail to generalize reliably as input length
Contributions. We focus on a small-data regime where the                or dimension grows (Tab. 2, Fig. 4).
target has a short discrete description, so finite-class ERM          • Auditability of both the learned hypothesis and the
enjoys strong classical generalization guarantees, yet the              search process. The output is executable, human-
two standard computational routes are unsatisfying: length-             readable code, and the full learning trajectory is in-
first enumeration is exponential in program length, while               spectable: we log the sequence of proposed program-
gradient-based training can be sample-inefficient on struc-             s/edits, execution outcomes, and verification diagnostics,
tured, SQ-hard families. Our goal is not to introduce new               yielding an auditable propose–verify trace (Fig. 1 and
PAC/SQ machinery or new constraint solvers. Instead, we                 Fig. 7 in App. A.4). This enables direct debugging of
make ERM over discrete program classes more computation-                failure modes and mechanistic validation of successes,
ally accessible by using pretrained LLMs only as a proposal             beyond reporting final accuracy.
mechanism for search, while keeping selection grounded in
executable verification and held-out error. Concretely, we
                                                                      2. Related Work
ask whether a pretrained LLM can serve as a useful search
prior that reduces the need for exhaustive enumeration with-          PAC learning, Occam’s razor and short programs. We
out changing the learning objective. Our contributions are:           follow the the classical generalization theory, where finite-
                                                                      class ERM has sample complexity O(log |H|) (Valiant,
• A clean compute–sample tension for short programs.
                                                                      1984; Vapnik & Chervonenkis, 1971; Vapnik, 1998). The
  Using classic SQ/PAC tools, we revisit a standard realiz-
                                                                      “short program” view instantiates Occam/MDL: a hypothe-
  able family (planted k-parity) to formalize a regime that is
                                                                      sis encodable in L symbols over alphabet Σ admits bounds
  central to small-data program learning. Finite-class ERM
                                                                      of order O(L log |Σ|), up to confidence terms (Blumer et al.,
  over length-L programs achieves the usual sample bound
                                                                      1987; Barron & Cover, 1991; Barron et al., 1998; Rissanen,
  m = Õ(L log |Σ|) (Eq. 1), but its runtime is exponential
                                                                      1989; McAllester, 1998). The length-first search (Alg. 2)
  in L. In contrast, finite-precision mini-batch coordinate
                                                                      realizes this ERM guarantee but incurs exponential time in
  SGD may be computationally convenient per step, yet
                                                                      description length, reflecting the classic universal-search
  requires many fresh examples to reachq nontrivial  error on
                                                                      trade-off (Levin, 1973; Solomonoff, 1964a;b).
  this family, namely q = T B = Ω( nk /2b ) (Prop. 3.1).
                                           
                                                                      Statistical query (SQ) learning and hardness of learn-
  Together, these results isolate a concrete small-data set-
                                                                      ing. The SQ framework and its refinements (Kearns, 1998;
  ting where both naive enumeration and gradient-based
                                                                      Blum et al., 1994; Feldman, 2017; Reyzin, 2020) yield lower
  training break down, for complementary reasons.
                                                                      bounds for many concept classes. Parity and related families
• ERM-style selection with an LLM proposal prior. In-

                                                                  2
                                             LLM Priors for ERM over Programs

have large SQ dimension under the uniform distribution, so           2012; Alur et al., 2013; Gulwani et al., 2017). This litera-
any SQ learner needs exponentially many (tolerant) queries           ture emphasizes search over discrete program spaces (often
to achieve nontrivial correlation (Blum et al., 1994; Feldman        within a DSL), including enumerative synthesis, version-
et al., 2017; Klivans & Sherstov, 2007; Klivans & Kothari,           space algebras, and CEGIS-style loops (Lau et al., 2003;
2014; Giapitzakis et al., 2025). Intuitively, mini-batch SGD         Solar-Lezama et al., 2006; Polikarpova et al., 2016; Solar-
is itself approximately an SQ algorithm: each update aver-           Lezama, 2013), often complemented by ranking, induc-
ages a bounded statistic over samples (Feldman et al., 2017;         tive bias, or user interaction to resolve ambiguity (Gulwani,
2018; Abbe et al., 2021; Barak et al., 2022). Hence, SQ              2011; Gulwani et al., 2017; Alur et al., 2013).
lower bounds transfer directly to SGD, making its iteration
                                                                     Recent work revisits PBE in the LLM era. One early
complexity grow with the SQ dimension—exponentially for
                                                                     paradigm treats the LLM itself as the “program” via in-
parities and pseudorandom families under the uniform dis-
                                                                     context learning (ICL): demonstrations, often with chain-of-
tribution. Our analysis formalizes this connection, showing
                                                                     thought, induce task procedures without parameter updates
how SQ hardness induces exponential sample requirements
                                                                     (Brown et al., 2020; Min et al., 2022; Wei et al., 2022), and
for gradient-based methods.
                                                                     this phenomenon has been analyzed theoretically (Von Os-
Gradient-based training on algorithmic reasoning. This               wald et al., 2023; Akyürek et al., 2023; Shen et al., 2024;
SQ perspective aligns with extensive empirical evidence:             de Wynter, 2025). Empirically, however, pretrained LLMs
even when a neural family can represent the target com-              can be brittle when asked to synthesize explicit programs
pactly, SGD-trained networks often fail on parity-like and           from examples alone, with performance depending strongly
compositional algorithmic tasks without strong inductive             on distributional match and fine-tuning (Li & Ellis, 2024).
bias or large data (Shalev-Shwartz et al., 2017; Safran              Other work proposes LLM-guided synthesis pipelines that
& Shamir, 2018; Daniely & Malach, 2020; Barak et al.,                retain execution-based verification while improving robust-
2022). More broadly, work on neural trainability separates           ness via decomposition and compositional search (Khan
representational power from optimization and sample ef-              et al., 2025). Complementary benchmarks study interactive
ficiency (Yehudai & Shamir, 2019; Daniely, 2017), and                settings, where an agent can query a hidden target func-
phenomena such as “grokking”—delayed generalization af-              tion and refine solutions using feedback or counterexamples
ter long training—highlight a gap between statistical optima         (Wei et al., 2025). More broadly, LLMs have been combined
and what SGD finds in practice (Power et al., 2022). These           with program analysis and synthesis components to improve
observations motivate alternatives that retain finite-class          the reliability of generated code in practical settings (Jain
guarantees while improving practical search efficiency.              et al., 2022).
LLM-guided search and iterative improvement. Pro-                    Our lens. We adopt the propose–verify view from program
gram synthesis and discrete search over programs has been            synthesis and PBE and repurpose it for learning from i.i.d.
studied for decades, and it has long been viewed as a diffi-         data with an explicit generalization objective. We treat the
cult problem because the hypothesis space is combinatorial           hypothesis space as a discrete class of executable programs
and brittle to small specification changes. The LLM era              and use a pretrained LLM only as an inductive-bias mecha-
introduced a new primitive: strong language-conditioned              nism: a proposal distribution over candidate programs. Each
priors over discrete objects, which can be used as proposals         proposal is verified by execution on the observed samples,
in a search loop. A prominent thread uses iterative propose–         and the final program is chosen by validation-based model
critique–revise driven by natural-language feedback (e.g.,           selection, so the criterion is held-out error rather than mere
Self-Refine, Reflexion), and related approaches treat feed-          consistency with a finite specification. In this sense, we
back as an optimization signal, including so-called textual          inherit the verification discipline of synthesis, but replace in-
gradients (Madaan et al., 2023; Shinn et al., 2023; Yuk-             teractive counterexamples and hand-crafted templates with
sekgonul et al., 2024). In parallel, evolutionary and neuro-         distributional learning and ERM-style selection from S.
symbolic frameworks use LLMs to propose edits or modular
building blocks that are refined via mutation and selection          3. Theoretical Analysis
(Pourcel et al., 2025; Novikov et al., 2025; DeepMind, 2025;
Bhansali et al., 2024).                                              3.1. Problem Setup
Programming by examples and LLM-assisted program                     We study inductive program synthesis (“program learning”):
synthesis. A complementary tradition studies program-                the target is a binary function y : X → {±1} implemented
ming by examples (PBE) and inductive program synthesis,              by a short program in a fixed language, and the learner
where the input is a finite set of input–output examples or                                                                 i.i.d.
                                                                     receives i.i.d. examples S = {(xi , y(xi ))}m
                                                                                                                 i=1 with xi ∼
tests and the goal is to output a program consistent with them       D. Throughout, we assume the realizable setting, i.e., y ∈
(Gulwani, 2011; Le & Gulwani, 2014; Singh & Gulwani,                 L, where L is the class of total functions computed by


                                                                 3
                                                LLM Priors for ERM over Programs

programs in the language (formalized below).                             strings, making brute-force search infeasible in practice.
Language and semantics. Fix a finite alphabet Σ and a
programming language L ⊆ Σ∗ . Each string u ∈ L has                      3.3. Gradient-Based Optimization
semantics JuK : X ⇀ {±1}, a (possibly partial) function                  A alternative method is to search for a predictor in a large
that may fail to compile or fail to halt. We write JuK(x) =  ⊥          parametric class (e.g., neural networks) using gradient-based
when u does not produce an output on x. Let C := f :                     optimization. To reason about the information such methods
X → {±1} : ∃ u ∈ L s.t. JuK is total and JuK = f .                       obtain from data, we use the statistical-oracles viewpoint:
We denote the length of u by |u| (in symbols over Σ) and                 many iterative optimization procedures can be modeled as
write Lℓ := {u ∈ L : |u| = ℓ}. A program is considered                   algorithms that access the data distribution only through
total if it defines an output for every input—i.e., it never fails       estimates of expectations of bounded functions and closely
to compile and halts on all x ∈ X , returning a ±1 label.                related sample-based variants (Kearns, 1998; Feldman et al.,
                                                                         2018; 2017; Reyzin, 2020).
Objective. For a hypothesis h : X → {±1}, define
population error errD (h) := PPrx∼D [h(x) ̸= y(x)] and                   Finite-precision SGD. There are two standard ways to
                            1   m
empirical error errS (h) := m   i=1 1{h(xi ) ̸= yi }. The                connect SGD to statistical-oracles: either inject indepen-
goal is to output a program u ∈ L whose total semantics                  dent noise so each update becomes a tolerant expectation
JuK attains small errD .                                                 query, or focus on finite-precision coordinate mini-batch
                                                                         SGD where each per-example coordinate contribution simu-
Computational model. When executing a candidate pro-
                                                                         lates a 1-STAT(b) query and q = T B such queries can be
gram u on input x, we allow a time budget T ∈ N per call;
                                                                         simulated via VSTAT by the standard reduction (Feldman
if u fails to compile or does not halt within time T , we treat
                                                                         et al., 2018, Thm. B.4). We therefore model mini-batch
the outcome as ⊥ and reject u as a hypothesis. This makes
                                                                         coordinate SGD as an algorithm that only accesses fresh
search procedures well-defined even when JuK is partial.
                                                                         data through finite-precision (per-example) gradient infor-
Short-program regime. We      will frequently analyze the               mation. At iteration t, the algorithm selects parameters
short-program
            S  subclass H ℓ :=  JuK : u ∈ Lℓ , JuK total ,               θt and a coordinate jt ∈ [d], draws a fresh mini-batch
where H = ℓ≥1 Hℓ and compare (i) explicit search over                    zt,1 , . . . , zt,B ∼ D, and updates using the b-bit quantized
Hℓ (finite-class ERM) to (ii) gradient-based learners hθ                                                                         (b)
                                                                         mini-batch coordinate gradient θt+1 = θt − ηt gbt,jt ejt ,
drawn from a proxy hypothesis family {hθ : θ ∈ Θ}.                         (b)              PB
                                                                         gbt,jt := B1 i=1 Qb (∂jt ℓ(θt , zt,i )), where Qb is a b-bit
                                                                         quantizer and ηt is the step size. The only interaction with
3.2. Program Enumeration
                                                                         fresh samples is via these b-bit per-example gradient values.
One approach to program learning is program enumeration.                 Planted k-parity. A canonical SQ-hard family is parity un-
Given a language L with token alphabet Σ, enumerate can-                 der the uniform distribution, and closely related planted par-
didate programs in a canonical order (e.g., by length and                ity testing problems inherit the same “low-correlation” struc-
then lexicographically), and return the first program that is            ture used in SQ lower bounds (Blum et al., 2003; Kearns,
consistent with the training sample (Alg. 2 in App. B.1).                1998; Reyzin, 2020; Feldman et al., 2017). Fix n ≥ 1 and
Despite its simplicity, enumeration is well known to be                  k ∈ {1, . . . , n}, let X = {0, 1}n , and let Sk be the set
highly sample efficient. By standard PAC bounds for fi-                  of k-sparse vectors in {0, 1}n . For each s ∈ Sk , define
nite hypothesis classes (Valiant, 1984) (see also Cor. 2.3               the target fs (x) = (−1)⟨s,x⟩ and the realizable distribution
of (Shalev-Shwartz & Ben-David, 2014)), if the target func-              Ds on X × {±1}     by x ∼ Unif(X ) and y = fs (x). Let
tion can be implemented by some length-L program in L,                   N := |Sk | = nk be the number of possible targets.
then with probability at least 1 − δ over the selection of S,            The following is a technical application of using the two-
the returned program h satisfies                                         step reduction using (Feldman et al., 2018, Thm. B.4) and
        errD (h) ≤ m−1 [L log |Σ| + log(2L2 /δ)].             (1)        the classic results from SQ learning (Reyzin, 2020). For
                                                                         completeness, we provide a full formal analysis in App. C.
Thus, the required sample size scales with the program
                                                                         Proposition 3.1. Consider any (possibly adaptive, random-
length of the target function. For completeness, we prove
                                                                         ized) procedure that runs T iterations of b-bit mini-batch
this inequality in App. B.1.
                                                                         coordinate SGD with batch size B on the above family,
The main limitation is computational. In the worst case,                 meaning that on fresh examples (x, y) ∼ Ds its only access
length-first enumeration must examine essentially all pro-               to the data is through b-bit quantized per-example coordi-
grams up to length L, which is exponential in L: Ω(|Σ|L ).               nate gradients as in the update displayed above. Let the
For example, with an ASCII-sized alphabet |Σ| = 128 and                  procedure output a hypothesis h : X → {±1}, and write
L = 10, this corresponds to 12810 ≈ 1.2 × 1021 candidate                 q := T B for the total number of fresh examples used.

                                                                     4
                                                                                                          LLM Priors for ERM over Programs
                                                                                        next round

                                                                                                                                                         Algorithm 1 LLM-PV: k-try LLM propose-and-verify with
                                  Sample candidate                 Compile & filter:
   Training set
       Str
                  Build prompt
                     Π(Str )
                                 programs from LLM
                                    (temperature τ )
                                                                   discard invalid or
                                                                  duplicate programs
                                                                                                      Evaluate on Sval :
                                                                                                     compute errSval (h)
                                                                                                                               Update best:
                                                                                                                               keep h⋆ with
                                                                                                                           lowest validation error       validation
                                             after k rounds

                                         Stop:
                                    after k rounds
                                                                                                                                                         Require: train/validation sets Str , Sval ; trials k; prompt
                                                                                                                                                              builder Π; temperature τ
Figure 2. An illustration of LLM-PV. A prompt built from Str
conditions the LLM to sample candidate programs. We compile
                                                                                                                                                         Ensure: Best program u⋆ with h⋆ = Ju⋆ K
and filter candidates, evaluate validation error on Sval , and main-                                                                                      1: Initialize err⋆ ← 1, (u⋆ , h⋆ ) ← (⊥, ⊥), U ← ∅
tain the best-so-far hypothesis h⋆ . The procedure runs for k rounds                                                                                      2: for t = 1, . . . , k do
and returns the program with the lowest validation error among all                                                                                        3:    Sample a candidate program u from LLM(Π(Str ); τ )
candidates evaluated.                                                                                                                                     4:    if u ∈ U then
                                                                                                                                                          5:       continue
                                                                                                                                                          6:    end if
If for every s ∈ Sk the procedure achieves nontrivial popula-                                                                                             7:    U ← U ∪ {u}; compile and set h ← JuK
tion error errDs (h) ≤ 14 withprobability at least β ≥ 5/6,                                                                                             8:    if h undefined on some x ∈ Str ∪ Sval then
                                              √
                                                  N
then necessarily q = Ω                           2b
                                                              .                                                                                           9:       continue
                                                                                                                                                         10:    end if
Program enumeration (Alg. 2) and finite-precision coor-                                                                                                  11:    Compute errSval (h)
dinate SGD fail for planted k-parity for complementary                                                                                                  12:    if errSval (h) < err⋆ then
reasons. Let N = nk be the number of k-parities. Enumer-                                                                                                 13:       (err⋆ , u⋆ , h⋆ ) ← (errSval (h), u, h)
ating programs of length ≤ L costs Θ(m, |Σ|L ). A k-parity                                                                                               14:    end if
has a description of length L = Θ(log N ) (ASCII/Python),                                                                                                15: end for
and Eq. 1 gives m = Õ(L) = Õ(log N ) for nontriv-                                                                                                      16: return (u⋆ , h⋆ )
ial error, so the resulting work is Θ(|Σ|Θ(log N ) log N ) =
N Θ(1) log N , i.e., polynomial in N . By contrast, finite-
precision coordinate SGD runs in Θ(m · Cost∇)√       time on                                                                                             Alg. 1 instantiates this propose–verify–select pipeline.
m fresh examples, but Prop. 3.1 needs m = Ω( N /2b )                                                                                                     Based on Thm. 11.1 in (Shalev-Shwartz & Ben-David,
to reach
    √      population error ≤ 1/4, yielding total work                                                                                                   2014), the guarantee depends on the proposal mass
Ω(( N /2b ) · Cost∇). In short: enumeration is expensive                                                                                                 pϵ (Str ) := Prh∼q(·|Str ) [errD (h) ≤ ϵ], plus the usual finite-
                     Θ(1)
in search (about N√       candidates), while SGD is expen-                                                                                               class validation penalty.
sive in data (about N     fresh examples), and both become
infeasible as N = nk grows (for constant k, N = Θ(nk )
                                                                                                                                                        Proposition 4.1. Fix ϵ ≥ 0 and δ ∈ (0, 1). Draw in-
so costs scale as nΘ(k) vs. nk/2 , up to Cost∇ ).                                                                                                        dependent samples Str ∼ Dmtr and Sval ∼ Dmval with
                                                                                                                                                         labels from the target y : X → {±1}. Run Alg. 1 for
                                                                                                                                                         k trials, and assume each trial outputs an accepted to-
4. New Lens                                                                                                                                              tal hypothesis ht : X → {±1} using only Str . Let
A natural alternative to brute-force program enumeration                                                                                                 h⋆ ∈ arg mint∈[k] errSval (ht ) be the returned hypothesis.
is sampling with verification: draw candidates and return                                                                                                If k ≥ ⌈ log(δ/2)  ⌉, then with probability at least
                                                                                                                                                                    log 1−pϵ (Str )
the one with smallest held-out error. But uniform sampling                                                                                               1 − δ over (Str , Sp
                                                                                                                                                                            val ) (and all algorithmic randomness),
is hopeless: if u ∼ Unif(LL ) and the target is u⋆ , then                                                                                                errD (h⋆ ) ≤ ϵ + 2 log(4k/δ)/(2mval ).
Pr[u = u⋆ ] = |Σ|−L , so the expected trials are |Σ|L , es-
sentially matching enumeration. Thus the bottleneck is not                                                                                               The guarantee separates the two roles in LLM-PV. The
verification, but the proposal distribution.                                                                                                             LLM enters through pϵ (Str ), the probability that a fresh
This motivates a proposer that, given Str , induces a data-                                                                                              accepted proposal has population error at most ϵ. Given
dependent distribution q(· | Str ) placing non-negligible                                                                                                k candidates, validation
                                                                                                                                                                        p          selection pays the standard finite-
mass on programs consistent with the observed pairs. Given                                                                                               class price Õ( log(k/δ)/mval ). Thus the LLM need not
such a proposal, the rest is standard: compile/execute can-                                                                                              be trusted as a predictor; it only needs to put enough mass
didates, discard invalid programs, and select by validation                                                                                              on low-error programs so one appears within k trials, after
error.                                                                                                                                                   which performance is certified by held-out evaluation.
A strong pretrained LLM provides a natural proposal bias:                                                                                                Comparing the number of programs observed. Uni-
prompted with Str , it generates code concentrated on rec-                                                                                               form sampling from LL hits any fixed program with prob-
ognizable templates and concise rules suggested by the ex-                                                                                               ability |Σ|−L , so it takes on the order of |Σ|L trials to ob-
amples, rather than spreading mass nearly uniformly over                                                                                                 serve it. In LLM-PV the relevant quantity is the proposal
the vast program space. In this view, the LLM is used as a                                                                                               mass pϵ (Str ) on ϵ-good hypotheses: by Prop. 4.1 it suf-
                                                                                                                                                                               log(2/δ)
data-dependent proposal prior distribution.                                                                                                              fices that k ≥ ⌈ − log(1−p  ϵ (Str ))
                                                                                                                                                                                               ⌉, and for pϵ (Str ) ≪ 1 this

                                                                                                                                                     5
                                                LLM Priors for ERM over Programs

                                                                         5.1.1. E VALUATION TASKS
                                                                         Synthetic tasks. We use synthetic algorithmic tasks span-
                                                                         ning non-local properties and simple heuristics: (1) parity
                                                                         variants: full parity (FP), first-half parity (FHP), random
Figure 3. LLM-PV generalizes to much larger input lengths.               3-parity (3-P), random 10-parity (10-P); (2) pattern match-
All methods (SGD, FT, and LLM-PV) are trained on 200 examples            ing for fixed motifs 00111111 (Pattern1) and 10101010
at a fixed length (n=10) and evaluated on lengths up to n=100.
SGD learns the training distribution but degrades to near-chance         (Pattern2); (3) palindrome detection (IsPal); (4) Dyck-2
accuracy (≈50%) as n grows. In contrast, LLM-PV maintains                membership (Dyck-2); (5) primality (IsPrime) while restrict-
high accuracy and, on Pattern Matching and Random 3-Parity,              ing negatives to last digits ∈ {1, 3, 7, 9}; (6) the shifted-
synthesizes dimension-invariant programs.                                input primality variant (IsPrime+47), where we add 47 to
                                                                         each integer before labeling; (7) cellular automata parity
                                                                         (CAP); and (8) SHA-256 parity (SHA). All datasets are
                                                                         class-balanced by construction. Formal definitions and data
                                                                         generation appear in App. A.1.
                                                                         Despite being familiar benchmarks, these targets are diffi-
Figure 4. SGD-trained LLMs fail to learn algorithmic tasks               cult to learn from i.i.d. labeled examples without an explicit
even with 100k examples; LLM-PV succeeds with 200. We                    algorithmic bias. First, k-parity suffers from a combinato-
compare the test performance of LLM-PV and SGD training (from-           rial search barrier: the label depends on a tiny unknown
scratch and fine-tuning) on 10-P (left), CAP (middle), and IsPrime
(right) when varying the training set size. SGD training overfits,
                                                                         subset of coordinates, and there are 100 10 candidate 10-bit
with test accuracy near chance across all training sizes. LLM-           subsets over 100 variables, so fitting low-order correlations
PV achieves 100% test accuracy with just 200 examples.                   provides essentially no guidance toward the correct rule.
                                                                         Second, palindromes and Dyck-2 have hard negatives that
                                                                         differ from positives by only a few edits, which preserves
is k ≈ log(2/δ)
          pϵ (Str ) . Thus, LLM-PV replaces the exponen-
                                                                         most local n-gram statistics; thus, any learner that relies
tial search size |Σ|L by an effective search size 1/pϵ (Str ),           primarily on local cues will struggle to separate the classes.
improving over enumeration whenever 1/pϵ (Str ) ≪ |Σ|L                   For Dyck-2, we additionally encode the two bracket types
(equivalently pϵ (Str ) ≫ |Σ|−L ).                                       as a 2-bit alphabet {00, 01, 10, 11} to remove trivial for-
                                                                         matting cues; success must come from tracking the under-
Interpretability. LLM-PV makes both the learned object                   lying stack-like constraint rather than from recognizable
and the learning process transparent: each run returns (i) an            characters. Third, motif detection is a needle-in-a-haystack
executable program and (ii) a reasoning trace that logs the              problem: a short pattern can occur at an unknown position
proposed candidates and their observed errors (often includ-             within a long string, so generalization requires reasoning
ing train accuracy). Fig. 1 shows a GPT-5-Thinking                       that is robust to shifts rather than exploiting fixed coordi-
trace (ChatGPT web UI) on IsPrime with m=100 examples                    nates. Fourth, cellular-automata parity and SHA-based la-
of 100-digit inputs: it starts with simple digit-level rules             bels exhibit an avalanche effect, where small input changes
(parity and digit-sum tests), then shifts to modular struc-              can induce global output changes, ruling out simple heuris-
ture, and ends with a Miller–Rabin primality test. Because               tic rules based on a few digits or local patterns. Finally, for
each step is linked to the errors it aims to fix, failures are           100-digit primality, memorization is implausible given the
auditable and successes are inspectable: the final symbolic              astronomically large number of candidates (on the order of
program can be unit-tested, stress-tested out of distribution,           1097 primes), so systematic success requires implementing
and re-run or edited.                                                    an algorithmic test; moreover, IsPrime+47 makes this ne-
                                                                         cessity explicit by defining the label via the primality of
5. Experiments                                                           int(x) + 47, so any strategy that treats the label as a direct
                                                                         property of the observed digit string x will fail.
5.1. Setup
We evaluate whether LLM-guided propose-and-verify can                    5.2. Methods Compared
recover short executable rules from few labeled examples,                We compare LLM-PV to several families of representative
and compare it to standard learning baselines. Each task                 baselines. To keep the main text focused, we describe each
is binary classification with inputs x ∈ X (bitstrings/digit             baseline at a high level here and defer full hyperparameters,
strings/graph encodings) and labels y(x) ∈ {0, 1}. We                    prompts, and sweeps to App. A.2.
draw m=200 i.i.d. labeled examples and split them into Str
and Sval of size 100 each. We report test accuracy on an                 LLM-PV.    We         instantiate Alg. 1 with sev-
independent held-out set of 10,000 examples.                             eral backbone         models,    including open-source

                                                                     6
                                                                  LLM Priors for ERM over Programs

Model / Task                                                         FP    FHP     Pattern1    Pattern2     3-P     10-P   IsPal   Dyck-2   CAP    IsPrime   IsPrime+47   CycleCount   SHA
XGBoost                                                             49.9    50.0     50.6         52.3      49.9    49.3   83.6     49.7    50.4    61.8        59.3          51.1      50.3
Random Forest                                                       49.8    49.7     50.5         52.5      49.7    49.3   77.8     50.1    49.2    58.7        55.7          50.8      50.6
SVM                                                                 49.9    49.9     49.8         51.6      50.6    48.9   69.7     50.1    50.1    55.7        55.6          47.0      50.2
Genetic Algorithm                                                   49.8    52.5     51.1         49.7      47.0    54.0   87.1     51.9    48.6    51.7        53.5          49.3      49.0
TabPFN (Hollmann et al., 2022)                                      50.1    50.5     49.2         51.2      49.3    50.5   49.4     50.5    48.0    57.1        65.4          51.3      50.6
SGD: Qwen3-1.7B                                                     49.3    50.6     51.5         53.6      49.7    50.3   49.2     51.4    49.4    58.8        53.6          53.5      49.8
SGD: DeepSeek-Coder-1.3B                                            52.2    50.5     51.3         55.1      54.3    51.3   51.6     49.4    50.0    54.5        56.0          53.9      49.8
SGD: Llama-3.2-1B                                                   52.2    48.6     50.0         54.3      51.5    50.6   50.3     51.5    50.2    52.7        51.7          54.7      51.0
FT: Llama-3.2-1B                                                    50.4    51.3     61.5         57.6      51.0    50.5   49.6     52.7    50.7    57.2        58.7          65.7      50.8
FT: Qwen3-1.7B                                                      51.2    50.7     59.6         59.4      50.9    50.7   49.6     52.5    50.8    58.3        52.9          57.4      51.2
FT: DeepSeek-Coder-1.3B                                             50.5    50.2     56.4         57.7      50.7    50.4   49.7     51.7    50.2    58.9        60.3          55.7      49.7
ICL: Qwen3-30B-Instruct (no tools)                                  53.0    54.0     56.0         51.0      50.0    50.0   47.0     48.0    49.0    50.0        58.0          46.0      54.0
ICL: Qwen3-Coder-30B-Instruct (no tools)                            50.0    50.0     50.0         50.0      50.0    44.0   51.0     50.0    49.0    47.0        60.0          47.0      49.0
ICL: DeepSeek-Coder-33B-Instruct (no tools)                         43.0    54.0     54.0         47.0      47.0    48.0   51.0     54.0    44.0    53.0        61.0          41.0      52.0
ICL: Gemini-3.1-Pro (with tools)                                    48.0    54.0     83.0         57.0      50.0    45.0   100      51.0    51.0    52.0        56.0          50.0      45.0
ICL: GPT-5-Thinking (no tools)                                      82.0    66.0     55.0         41.0      47.0    47.0   79.0     57.0    51.0    55.0        47.0          43.0      44.0
ICL: GPT-5-Thinking (with tools)                                    99.0    88.0     51.0         51.0      75.0    79.0   91.0     59.0    46.0    62.0        56.0          51.0      46.0
MLAgentBench (Huang et al., 2024): GPT-5-Thinking (with tools)      53.6    51.0     33.4         60.9      32.8    50.1   31.6     52.1    50.0    32.6        33.1          49.1      49.9
AIDE-ML (Jiang et al., 2025): GPT-5-Thinking (with tools)           49.5    49.9     50.3         50.9      49.5    49.2   50.0     50.5    50.2    55.5        49.7          50.0      50.8
LLM-PV: Qwen3-30B-Instruct (no tools)                               50.4    49.6     51.1         60.9      50.4    51.6   49.9     80.4    50.2    50.6        50.2          49.9      49.7
LLM-PV: DeepSeek-Coder-33B-Instruct (no tools)                      100     50.9     50.9         50.5      51.6    50.8   51.0     57.3    50.2    50.0        50.2          50.0      51.5
LLM-PV: OLMo-3-32B-Instruct (no tools)                              100     50.5     50.9         83.5      50.2    50.2   52.7     50.5    50.8    50.8        50.5          52.7      50.1
LLM-PV: Gemini-3.1-Pro (with tools)                                 100     100      100          100       100     100    100      80.7    52.9    100         68.1          96.1      50.3
LLM-PV: GPT-5-Thinking (no tools)                                   100     51.1     78.4         64.7      50.1    50.4   50.0     79.9    50.2    52.9        64.0          51.0      50.2
LLM-PV: GPT-5-Thinking (with tools)                                 100     100      100          100       100     100    100      100     100     100         80.6          96.9      50.1
Table 1. Test accuracy at length n=100 across baselines and LLM-PV. We compare classic ML algorithms, training from scratch (SGD
on 1B-scale LMs), fine-tuning (top-k layers or full) of 1B-scale pretrained LMs, and in-context learning with 30B+ instruction-tuned
models. Most baselines remain near chance on the algorithmic tasks at n=100, while LLM-PV achieves high test accuracy on all
tasks except SHA.


                            SGD                                             FT                                             ICL                                      LLM-PV
Task       n=20 n=25 n=30 n=50 n=100 n=20 n=25 n=30 n=50 n=100 n=20 n=25 n=30 n=50 n=100 n=20 n=25 n=30 n=50 n=100
FP         56.3    56.2     52.4       52.7     52.2     50.8    51.0      50.4    51.2       51.2       52.0      47.0    54.0    51.0     53.0     100†    100†      100†   100†     100†
FHP        51.0    52.5     50.7       53.7     50.6     52.7    51.7      50.8    50.5       51.3       50.0      50.0    46.0    59.0     54.0     100     100       100    100      100
3-P        50.6    50.5     52.2       51.4     54.3     50.9    50.7      53.3    51.0       51.0       54.0      56.0    51.0    48.0     50.0     100     100       100    100      100
10-P       50.6    50.2     50.3       50.6     50.3     51.1    50.5      50.8    50.3       50.7       51.0      55.0    55.0    51.0     50.0     100     100       100    100      100
Pattern1   91.4    82.8     57.8       58.7     51.5     74.6    72.0      68.4    68.5       61.5       89.0      69.0    77.0    61.0     56.0     100†    98.9      98.5   100†     100†
Pattern2   97.5    96.0     95.2       74.5     55.1     69.4    69.2      67.4    67.3       59.4       79.0      68.0    72.0    79.0     51.0     100†    94.2      93.2   100†     100†
IsPal      62.7    56.5     54.8       51.6     51.6     52.4    51.3      51.1    50.2       49.7       58.0      53.0    63.0    52.0     51.0     100     96.0      100    100      100
Dyck-2∗    65.7    59.1     55.9       51.1     51.8     64.6    57.9      53.9    52.8       52.7       70.0      57.0    61.0    54.0     54.0     77.4    90.5      80.0   90.5     100
IsPrime    59.9    60.2     63.0       57.0     58.8     59.2    59.8      59.2    62.5       58.9       53.0      53.0    53.0    57.0     53.0     100†    100†      100†   100†     100†
CAP⋄       52.5    51.4     52.0       50.5     50.0     50.9    50.6      51.2    51.1       50.8       52.0      47.0    46.0    50.0     49.0     100     100       100†   100†     100†
100† indicates 100% for all n.   ∗
                                     For Dyck-2, lengths are n ∈ {20, 40, 60, 80, 100} respectively.
Table 2. LLM-PV vs. training and prompting baselines. Test accuracy (%) for input lengths n ∈ {20, 25, 30, 50, 100}. SGD:
best test accuracy across Qwen3-1.7B, Deepseek-Coder-1.3B, and Llama3.2-1B, each trained from scratch. FT: best
test accuracy across Llama3.2-1B, Qwen3-1.7B, and Deepseek-Coder-1.3B, sweeping tuned layers ({top-2, top-4, top-
8, full}) and training hyperparameters, separately for each (task,n). ICL: best test accuracy across Qwen3-30B-Instruct,
Qwen3-Coder-30B-Instruct, and Deepseek-Coder-33B-Instruct.



models        such      as       Qwen3-30B-Instruct,                                                 Baselines.      (1) Classic ML: XGBoost, Random For-
Deepseek-Coder-33B-Instruct,                           and                                           est, SVM, and a Genetic Algorithm baseline, each with
Olmo-3-32B-Instruct, as well as closed mod-                                                          validation-based model and hyperparameter selection. (2) A
els such as Gemini-3.1-Pro and GPT-5-Thinking.                                                       pre-trained tabular foundation model: TabPFN (Hollmann
The open-source models are evaluated without tool calls.                                             et al., 2022). (3) From scratch: Qwen3-1.7B trained
For GPT-5-Thinking, we explicitly evaluate both                                                      from scratch as a classifier on the m=200 labeled exam-
no-tool and tool-augmented variants, allowing us to isolate                                          ples. (4) Fine-tuning: Qwen3-1.7B, Llama3.2-1B,
the effect of tool use. Given Str , the model samples up                                             and Deepseek-Coder-1.3B fine-tuned on the same
to k=5 candidate Python programs under a fixed prompt                                                m=200 labeled examples; hyperparameters (e.g., learning
(Fig. 5). We discard invalid or duplicate programs, execute                                          rate, batch size, and the number of tuned layers) are selected
the remaining candidates in a sandboxed interpreter, and                                             via a grid sweep. (5) In-context learning: We evaluate large
select the program with the lowest validation error on Sval                                          language models prompted with all m=200 labeled exam-
(Fig. 2). We do not use validation feedback to adapt the                                             ples and queried for the test labels. The comparison includes
sampling distribution.                                                                               open-weight models, code-specialized models, and closed
                                                                                                     frontier models. Open-weight models are run without tool


                                                                                              7
                                                                     LLM Priors for ERM over Programs

Task       n=20        n=25          n=30          n=50           n=100 PAC bound                  Tabular learners capture surface-level cues. At n=100,
         Train Test Train Test Train Test Train Test Train Test ASCII PyTok                        tabular learners can succeed when local statistics are predic-
10-P    100 53.9 100 49.8 100 50.5 100 49.2 100 50.7 0.995 0.998
CAP     100 99.9 100 50.3 100 50.2 100 49.5 100 50.4 0.985 0.994                                   tive (e.g., IsPal reaches 69.7–87.1% for SVM/GA; IsPrime
IsPrime 100 59.8 100 58.7 100 60.3 100 60.1 100 59.9 0.992 0.997                                   reaches 51.7–61.8% for GA/XGBoost; Tab. 1). Notably,
Table 3. BLOOM-75M (SGD) train/test accuracy (%) and a                                             even TabPFN (Hollmann et al., 2022)—a strong pre-trained
program-length PAC bound for training with m=100k sam-                                             tabular foundation-model—does not close the gap on our
ples. We report train/test accuracy at each length n. The last
two columns report the bound 1 − m−1 [L log |Σ| + log(2L2 /δ)]                                     algorithmic tasks: at n=100 it remains at (near) chance
with δ=10−10 , using L from a compact reference implementa-                                        on FP/FHP/3-P/10-P, Dyck-2, and CAP (roughly 48–51%
tion measured in ASCII bytes (|Σ|=128) or Python lexical tokens                                    across these columns; Tab. 1). Overall, while tabular meth-
(|Σ|=64); the bound is independent of n. Despite perfect train-                                    ods can exploit shallow cues when they exist, they fail on
ing accuracy at each n, test accuracy stays near chance on 10-P                                    parity, Dyck-2, and CAP, highlighting a qualitative distinc-
and CAP, even though both admit short programs for which
the PAC-learning bounds are close to 1.                                                            tion between feature-based prediction and learning an algo-
                                                                                                   rithmic procedure.

                   Adult       Secondary      CDC Diabetes                        Chess
                                                                                                   LLM-PV recovers algorithmic rules. In contrast, LLM-
Model             Income       Mushroom      Health Indicators     HRTU2        (KR vs KP)
                                                                                                   PV achieves perfect accuracy at n=100 on all parity vari-
SVM           52.8 ± 0.000    68.1 ± 0.000    69.1 ± 0.000       91.5 ± 0.000 89.4 ± 0.000
GA            75.2 ± 0.016    64.7 ± 0.020    69.0 ± 0.014       90.6 ± 0.001 92.5 ± 0.013         ants, IsPalindrome, Dyck-2, CAP, and IsPrime (all 100%;
Decision Tree 67.8 ± 0.020    69.0 ± 0.016    62.5 ± 0.004       89.1 ± 0.002 94.1 ± 0.003
Random Forest 74.2 ± 0.008    70.8 ± 0.003    72.7 ± 0.006       91.4 ± 0.005 88.1 ± 0.011
                                                                                                   Tab. 1), indicating broad rule recovery rather than task-
XGBoost
TabPFN
              71.4 ± 0.006
              77.7 ± 0.000
                              66.1 ± 0.012
                              69.9 ± 0.000
                                              68.6 ± 0.004
                                              72.1 ± 0.000
                                                                 91.4 ± 0.001 93.1 ± 0.005
                                                                 93.1 ± 0.000 93.1 ± 0.000
                                                                                                   specific pattern fitting. More strikingly, LLM-PV main-
LLM-PV         75.8 ± 0.007   72.2 ± 0.020     71.1 ± 0.002      92.3 ± 0.007   92.3 ± 0.012       tains high accuracy on the shifted-primality task IsPrime+47,
Table 4. Tabular benchmarks. Test accuracy (%) for compar-                                         reaching 80.6% at n=100 (Tab. 1). Since adding a fixed
ing classic ML baselines with LLM-PV. Our LLM-PV method                                            offset breaks many superficial correlations while preserving
achieves comparable results to other standard tabular learners.                                    a clean arithmetic relationship, this result suggests LLM-
                                                                                                   PV is not merely memorizing primality patterns but is often
                                                                                                   discovering a transferable computational structure. SHA re-
use. For GPT-5-Thinking, we report both no-tool and                                                mains difficult in our setup: all methods are close to chance,
tool-augmented variants; for Gemini-3.1-Pro, we re-                                                with the best performance coming from ICL (up to 54.0%
port the tool-augmented variant. (6) Agentic ML baselines:                                         at n=100; Tab. 1).
We also compare against general-purpose agentic ML sys-                                            Direct prompting is the wrong output space. ICL
tems, including MLAgentBench (Huang et al., 2024) and                                              asks the model to behave like the target function directly:
AIDE-ML (Jiang et al., 2025). These baselines are instan-                                          given a new input, output a label. This is different from
tiated with GPT-5-Thinking and tool use, allowing the                                              recovering an executable rule. Consistent with this dis-
agent to write, execute, and revise code during the search                                         tinction, even tool-augmented ICL remains unreliable:
process. All prompting, tool-use, and evaluation details are                                       GPT-5-Thinking with tools improves over its no-tool
provided in App. A.2.                                                                              variant on several tasks, such as FP (99.0% vs. 82.0%),
                                                                                                   FHP (88.0% vs. 66.0%), and 10-P (79.0% vs. 47.0%), but
5.3. Main results                                                                                  it still remains far from rule recovery on Pattern1, Pattern2,
LLM baselines often fit without recovering the rule.                                               Dyck-2, CAP, CycleCount, and SHA (Tab. 1). Thus, tool-
Across the core algorithmic tasks (parity variants, Dyck-                                          augmented direct prediction does not reliably produce algo-
2, CAP), both training from scratch and fine-tuning re-                                            rithmic generalization.
main close to chance at n=100 (Tab. 1), suggesting length-                                         Tools help when they support program search. The
specific memorization rather than rule recovery. Concretely,                                       GPT-5-Thinking ablation inside LLM-PV shows that
for the parity variants {FP, FHP, 3-P, 10-P}, SGD/FT                                               tool use is highly beneficial when it is embedded in a
scores fall in the range 48.6–54.3% at n=100 (Tab. 1); for                                         propose-and-verify loop. Without tools, LLM-PV recov-
CAP they are even tighter at 49.4–50.8% (Tab. 1). Fine-                                            ers some structure but remains incomplete, e.g., 78.4% on
tuning can exploit local structure when it exists: on Pattern1                                     Pattern1, 64.7% on Pattern2, and 79.9% on Dyck-2. With
at n=100, the best FT model reaches 61.5% versus 51.5%                                             tools, the same backbone reaches 100% accuracy on 10 of
for the best SGD model (Tab. 1). However, this improve-                                            the 13 tasks and remains high on IsPrime+47 (80.6%) and
ment does not transfer to the parity variants or CAP, where                                        CycleCount (96.9%) (Tab. 1). This suggests that much of
FT remains near chance (Tab. 1). In-context learning at                                            the gain comes from programmatic search: the agent can
30B scale yields occasional gains but still does not produce                                       write code, execute it, inspect failures, test hypotheses, and
consistent algorithmic generalization: at n=100, ICL is the                                        refine candidate solutions.
strongest baseline on SHA (up to 54.0%; Tab. 1), while
remaining near chance on parity and CAP (Tab. 1).

                                                                                               8
                                              LLM Priors for ERM over Programs

Tool use alone is not sufficient. The comparison with ICL             across lengths, including perfect generalization on tasks
shows that tools are useful only when paired with the right           such as Pattern Matching and Random 3-Parity.
search objective. Tool-augmented ICL has access to the
                                                                      LLM-PV performs comparably to strong tabular ML
same kind of external computation, but it still returns labels
                                                                      baselines. In addition to the tasks above, we also con-
rather than an executable rule. In contrast, LLM-PV uses
                                                                      sider tabular datasets. For each task, we use only 100 fixed
tools to search over programs and then selects among them
                                                                      training samples and 100 fixed validation samples, and we
using validation error. The gap between tool-augmented
                                                                      report test error on the original test set. To ensure that the
ICL and tool-augmented LLM-PV shows that the benefit
                                                                      samples are not easily recognized by LLM-based methods
is not merely tool access; it is tool use organized around
                                                                      (e.g., LLM-PV), we preprocess each input by applying a
program discovery.
                                                                      fixed random linear transformation x 7→ W x + b, where W
Generic agents are not enough; the output matters. The                is diagonal and b is a vector, with entries drawn i.i.d. from
agentic ML baselines MLAgentBench and AIDE-ML,                        a standard normal distribution. As per Tab. 4, LLM-PV
both instantiated with GPT-5-Thinking and tool use, re-               is competitive against standard tabular learners, suggest-
main close to chance on most tasks. For example, AIDE-ML              ing that propose-and-verify can remain effective beyond
stays between roughly 49% and 55.5% across all tasks,                 synthetic sequence tasks.
while MLAgentBench also fails broadly and even drops
below chance on several tasks (Tab. 1). These systems                 6. Discussion
search over standard ML workflows and return trained pre-
dictors, whereas our tasks often require an explicit algorith-        We studied LLM-PV, a learning algorithm that uses a pre-
mic rule. LLM-PV succeeds because its hypothesis class is             trained LLM as a proposal prior and selects among exe-
executable programs, not generic predictors.                          cutable programs by validation error. Across algorithmic
                                                                      tasks, LLM-PV often recovers exact rules from few exam-
Open-weight models show partial program discovery
                                                                      ples and generalizes far beyond the training length. This
without tools.       The no-tool open-weight LLM-PV
                                                                      suggests a different use of pretrained LLMs in learning: not
variants occasionally recover individual rules, but
                                                                      as predictors that directly imitate the target function, but as
their successes are sparse and unstable across tasks.
                                                                      search priors over discrete, verifiable hypotheses.
For example, DeepSeek-Coder-33B-Instruct
and        OLMo-3-32B-Instruct                solve      FP,          The main lesson is that the output space matters. Standard
OLMo-3-32B-Instruct reaches 83.5% on Pat-                             gradient-based predictors, fine-tuned models, and in-context
tern2, and Qwen3-30B-Instruct reaches 80.4% on                        learning ultimately produce labels or learned predictors. By
Dyck-2 (Tab. 1). However, most other entries remain near              contrast, LLM-PV searches over executable rules and uses
chance, suggesting that the propose-and-verify formulation            held-out error only to select among candidate programs.
can expose partial rule-recovery ability without tools, but           This separation keeps the learning criterion simple and au-
reliable recovery requires active testing and debugging.              ditable: the LLM proposes programs, while execution and
                                                                      validation performance decide.
More data does not reliably fix SGD on these tasks. To
test whether these failures are a small-data artifact, we train       More broadly, our results point toward learning via LLM-
BLOOM-75M from scratch with SGD on m=100k examples                    guided search with verification. Future work should charac-
per task (separately for each n). The model again fits the            terize when the LLM proposal distribution places enough
training data perfectly, yet test accuracy remains near chance        mass on correct or near-correct programs, when validation
on 10-P and on CAP for n ≥ 25, and is only modest on                  can reliably identify the right hypothesis, and where the
IsPrime (Tab. 3). Fig. 4 further shows that scaling m from            approach breaks down.
10 to 100k does not yield reliable generalization for the SGD
                                                                      The main limitation is scope. Our experiments focus on
baseline in our setup, whereas LLM-PV attains perfect test
                                                                      structured low-data regimes, and LLM-PV is not intended
accuracy with m=200 on these tasks.
                                                                      as a general replacement for supervised deep learning. Its
Length generalization.         In Fig. 3 we study out-of-             success depends on a capable agentic proposer and on suffi-
distribution length generalization by training on 200 sam-            cient proposal mass near the correct program. As target pro-
ples at a short input length (n=10) and evaluating on longer          grams become longer, more compositional, or less aligned
sequences. We keep the SGD (and FT) setup identical to                with the pretrained model’s prior, this mass may decrease,
our primary experiments. The SGD and FT baselines are                 requiring more samples, more LLM calls, or richer propose-
oftentime able to generalize at n=10 but fail to generalize           verify-refine procedures. Extending the approach to larger
across lengths: accuracy rapidly collapses toward ≈50%                synthesis problems and real-world structured domains re-
as n increases. In contrast, LLM-PV often synthesizes                 mains future work.
dimension-invariant programs, yielding stable performance

                                                                  9
                                             LLM Priors for ERM over Programs

Impact Statement                                                      Barron, A., Rissanen, J., and Yu, B. The minimum de-
                                                                        scription length principle in coding and modeling. IEEE
This work studies program learning in controlled algorith-              Transactions on Information Theory, 44(6):2743–2760,
mic settings. It raises no direct ethical, safety, or environ-          1998. doi: 10.1109/18.720554.
mental concerns in the scope considered here. We introduce
LLM-PV, a propose-and-verify framework that performs                  Bhansali, S., Jin, A., Lizzo, T., and Heck, L. Lego:
ERM-style selection over a discrete program class using a               Language model building blocks, 2024. URL https:
pretrained model only as a proposal prior, and we provide               //arxiv.org/abs/2410.18287.
empirical evidence that it can recover compact rules from
few labeled examples and generalize to longer inputs. These           Blum, A., Furst, M., Jackson, J., Kearns, M., Mansour, Y.,
results inform how pretrained priors can support auditable,             and Rudich, S. Weakly learning dnf and characterizing
executable hypotheses without gradient-based retraining.                statistical query learning using fourier analysis. In Pro-
While our experiments execute candidate programs, they do               ceedings of the Twenty-Sixth Annual ACM Symposium on
so in a restricted setting; any application beyond this scope           Theory of Computing, STOC ’94, pp. 253–262, New York,
should use sandboxed execution and a constrained language               NY, USA, 1994. Association for Computing Machinery.
to avoid unintended behavior.                                           ISBN 0897916638. doi: 10.1145/195058.195147. URL
                                                                        https://doi.org/10.1145/195058.195147.
References
                                                          Blum, A., Kalai, A., and Wasserman, H. Noise-tolerant
Abbe, E., Kamath, P., Malach, E., Sandon, C., and Srebro,   learning, the parity problem, and the statistical query
  N. On the power of differentiable learning versus         model. J. ACM, 50(4):506–519, July 2003. ISSN 0004-
  pac and sq learning. In Ranzato, M., Beygelzimer,         5411. doi: 10.1145/792538.792543. URL https://
 A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.),     doi.org/10.1145/792538.792543.
 Advances in Neural Information Processing Systems,
 volume 34, pp. 24340–24351. Curran Associates, Inc.,     Blumer, A., Ehrenfeucht, A., Haussler, D., and War-
  2021. URL https://proceedings.neurips.                    muth, M. K. Occam’s razor. Information Process-
  cc/paper_files/paper/2021/file/                           ing Letters, 24(6):377–380, 1987. doi: 10.1016/
  cc225865b743ecc91c4743259813f604-Paper.                   0020-0190(87)90114-1. URL https://doi.org/
  pdf.                                                      10.1016/0020-0190(87)90114-1.

Akyürek, E., Schuurmans, D., Andreas, J., Ma, T., and                Bottou, L. Large-scale machine learning with stochastic
  Zhou, D. What learning algorithm is in-context learn-                 gradient descent. In Proceedings of COMPSTAT’2010,
  ing? investigations with linear models. In The Eleventh               pp. 177–186. Physica Verlag, 2010.
 International Conference on Learning Representations,
  2023. URL https://openreview.net/forum?                             Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D.,
  id=0g0X4H8yN4I.                                                       Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
                                                                        Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,
Alur, R., Bodik, R., Juniwal, G., Martin, M. M. K.,                     Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J.,
  Raghothaman, M., Seshia, S. A., Singh, R., Solar-                     Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M.,
  Lezama, A., Torlak, E., and Udupa, A. Syntax-guided                   Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S.,
  synthesis. In 2013 Formal Methods in Computer-Aided                   Radford, A., Sutskever, I., and Amodei, D. Language
  Design, pp. 1–8, 2013. doi: 10.1109/FMCAD.2013.                       models are few-shot learners.          In Larochelle, H.,
  6679385.                                                              Ranzato, M., Hadsell, R., Balcan, M., and Lin, H. (eds.),
                                                                        Advances in Neural Information Processing Systems,
Barak, B., Edelman, B. L., Goel, S., Kakade, S. M., eran                volume 33, pp. 1877–1901. Curran Associates, Inc.,
  malach, and Zhang, C. Hidden progress in deep learn-                  2020. URL https://proceedings.neurips.
  ing: SGD learns parities near the computational limit.                cc/paper_files/paper/2020/file/
  In Oh, A. H., Agarwal, A., Belgrave, D., and Cho,                     1457c0d6bfcb4967418bfb8ac142f64a-Paper.
  K. (eds.), Advances in Neural Information Processing                  pdf.
  Systems, 2022. URL https://openreview.net/
  forum?id=8XWP2ewX-im.                                               Daniely, A. Sgd learns the conjugate kernel class of
                                                                        the network. In Proceedings of the 31st International
Barron, A. and Cover, T. Minimum complexity density                     Conference on Neural Information Processing Systems,
  estimation. IEEE Transactions on Information Theory,                  NIPS’17, pp. 2419–2427, Red Hook, NY, USA, 2017.
  37(4):1034–1054, 1991. doi: 10.1109/18.86996.                         Curran Associates Inc. ISBN 9781510860964.

                                                                 10
                                          LLM Priors for ERM over Programs

Daniely, A. and Malach, E. Learning parities with neural          Hollmann, N., Müller, S., Eggensperger, K., and Hutter, F.
  networks. In Proceedings of the 34th International Con-          TabPFN: A transformer that solves small tabular classi-
  ference on Neural Information Processing Systems, NIPS            fication problems in a second. In NeurIPS 2022 First
 ’20, Red Hook, NY, USA, 2020. Curran Associates Inc.              Table Representation Workshop, 2022. URL https:
  ISBN 9781713829546.                                              //openreview.net/forum?id=eu9fVjVasr4.

de Wynter, A. Is in-context learning learning?, 2025. URL         Huang, Q., Vora, J., Liang, P., and Leskovec, J. Mlagent-
  https://arxiv.org/abs/2509.10414.                                 bench: evaluating language agents on machine learning
                                                                    experimentation. In Proceedings of the 41st International
DeepMind. Alphaevolve: A gemini-powered coding agent
                                                                   Conference on Machine Learning, ICML’24. JMLR.org,
  for designing advanced algorithms, 2025. URL https:
                                                                    2024.
  //deepmind.google/discover/blog/
  alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms.
                                                            Jain, N., Vaidyanath, S., Iyer, A., Natarajan, N.,
Feldman, V. A general characterization of the statis-          Parthasarathy, S., Rajamani, S., and Sharma, R. Jig-
  tical query complexity. In Kale, S. and Shamir, O.           saw: large language models meet program synthesis.
  (eds.), Proceedings of the 2017 Conference on Learning       In Proceedings of the 44th International Conference
  Theory, volume 65 of Proceedings of Machine Learn-           on Software Engineering, ICSE ’22, pp. 1219–1231,
  ing Research, pp. 785–830. PMLR, 07–10 Jul 2017.             New York, NY, USA, 2022. Association for Comput-
  URL https://proceedings.mlr.press/v65/                       ing Machinery. ISBN 9781450392211. doi: 10.1145/
  feldman17c.html.                                             3510003.3510203. URL https://doi.org/10.
                                                               1145/3510003.3510203.
Feldman, V., Grigorescu, E., Reyzin, L., Vempala, S. S.,
  and Xiao, Y. Statistical algorithms and a lower bound     Jiang, Z., Schmidt, D., Srikanth, D., Xu, D., Kaplan, I.,
  for detecting planted cliques. J. ACM, 64(2), April 2017.    Jacenko, D., and Wu, Y. Aide: Ai-driven exploration in
  ISSN 0004-5411. doi: 10.1145/3046674. URL https:             the space of code, 2025. URL https://arxiv.org/
  //doi.org/10.1145/3046674.                                   abs/2502.13138.

Feldman, V., Perkins, W., and Vempala, S. On the com-             Kearns, M. Efficient noise-tolerant learning from statistical
  plexity of random satisfiability problems with planted            queries. J. ACM, 45(6):983–1006, November 1998. ISSN
  solutions. SIAM Journal on Computing, 47(4):1294–                 0004-5411. doi: 10.1145/293347.293351. URL https:
  1338, 2018. doi: 10.1137/16M1078471. URL https:                   //doi.org/10.1145/293347.293351.
  //doi.org/10.1137/16M1078471.
                                                                  Khan, R., Gulwani, S., Le, V., Radhakrishna, A., Tiwari, A.,
Giapitzakis, G., Fountoulakis, K., Nichani, E., and Lee,            and Verbruggen, G. Llm-guided compositional program
  J. D. On the statistical query complexity of learning             synthesis, 2025. URL https://arxiv.org/abs/
  semiautomata: a random walk approach, 2025. URL                   2503.15540.
  https://arxiv.org/abs/2510.04115.
                                                                  Klivans, A. and Kothari, P. Embedding Hard Learning
Gulwani, S. Automating string processing in spreadsheets
                                                                    Problems Into Gaussian Space. In Jansen, K., Rolim, J.,
  using input-output examples. SIGPLAN Not., 46(1):
                                                                    Devanur, N. R., and Moore, C. (eds.), Approximation,
  317–330, January 2011. ISSN 0362-1340. doi: 10.
                                                                    Randomization, and Combinatorial Optimization.
 1145/1925844.1926423. URL https://doi.org/
                                                                    Algorithms and Techniques (APPROX/RANDOM 2014),
 10.1145/1925844.1926423.
                                                                    volume 28 of Leibniz International Proceedings in
Gulwani, S., Polozov, O., and Singh, R. Program synthesis.          Informatics (LIPIcs), pp. 793–809, Dagstuhl, Ger-
 Foundations and Trends in Programming Languages, 4                 many, 2014. Schloss Dagstuhl – Leibniz-Zentrum
  (1–2):1–119, 2017. doi: 10.1561/2500000010. URL                   für Informatik.   ISBN 978-3-939897-74-3.        doi:
  https://doi.org/10.1561/2500000010.                               10.4230/LIPIcs.APPROX-RANDOM.2014.793. URL
                                                                    https://drops.dagstuhl.de/entities/
Guo, D., Zhu, Q., Yang, D., Xie, Z., Dong, K., Zhang,               document/10.4230/LIPIcs.APPROX-RANDOM.
 W., Chen, G., Bi, X., Wu, Y., Li, Y. K., Luo, F., Xiong,           2014.793.
 Y., and Liang, W. Deepseek-coder: When the large
  language model meets programming - the rise of code             Klivans, A. R. and Sherstov, A. A. Unconditional lower
  intelligence. CoRR, abs/2401.14196, 2024. URL                     bounds for learning intersections of halfspaces. Ma-
  http://dblp.uni-trier.de/db/journals/                             chine Learning, 69(2-3):97–114, 2007. doi: 10.1007/
  corr/corr2401.html#abs-2401-14196.                                s10994-007-5010-1.

                                                             11
                                          LLM Priors for ERM over Programs

Lau, T., Wolfman, S. A., Domingos, P., and Weld,                 Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis,
  D. S.    Programming by demonstration using ver-                M., Hajishirzi, H., and Zettlemoyer, L. Rethinking
  sion space algebra. Mach. Learn., 53(1–2):111–156,              the role of demonstrations: What makes in-context
  October 2003. ISSN 0885-6125. doi: 10.1023/                     learning work? In Goldberg, Y., Kozareva, Z., and
  A:1025671410623. URL https://doi.org/10.                        Zhang, Y. (eds.), Proceedings of the 2022 Confer-
  1023/A:1025671410623.                                           ence on Empirical Methods in Natural Language Pro-
                                                                  cessing, pp. 11048–11064, Abu Dhabi, United Arab
Le, V. and Gulwani, S. Flashextract: a framework for              Emirates, December 2022. Association for Computa-
  data extraction by examples. SIGPLAN Not., 49(6):               tional Linguistics. doi: 10.18653/v1/2022.emnlp-main.
  542–553, June 2014. ISSN 0362-1340. doi: 10.                    759. URL https://aclanthology.org/2022.
  1145/2666356.2594333. URL https://doi.org/                      emnlp-main.759/.
  10.1145/2666356.2594333.
                                                                 Novikov, A., Vũ, N., Eisenberger, M., Dupont, E., Huang,
Levin, L. A. Universal sequential search problems. Prob-           P.-S., Wagner, A. Z., Shirobokov, S., Kozlovskii, B., Ruiz,
  lems of Information Transmission, 9(3):265–266, 1973.            F. J. R., Mehrabian, A., Kumar, M. P., See, A., Chaudhuri,
  URL https://www.mathnet.ru/eng/ppi914.                           S., Holland, G., Davies, A., Nowozin, S., Kohli, P., and
  English translation of Probl. Peredachi Inf., 9(3):115–          Balog, M. Alphaevolve: A coding agent for scientific and
  116.                                                             algorithmic discovery, 2025. URL https://arxiv.
                                                                   org/abs/2506.13131.
Li, W.-D. and Ellis, K. Is programming by example solved
  by llms? In Globerson, A., Mackey, L., Belgrave,           Polikarpova, N., Kuraj, I., and Solar-Lezama, A. Program
  D., Fan, A., Paquet, U., Tomczak, J., and Zhang, C.          synthesis from polymorphic refinement types. In Pro-
  (eds.), Advances in Neural Information Processing            ceedings of the 37th ACM SIGPLAN Conference on Pro-
  Systems, volume 37, pp. 44761–44790. Curran As-              gramming Language Design and Implementation, PLDI
  sociates, Inc., 2024. doi: 10.52202/079017-1422.             ’16, pp. 522–538. Association for Computing Machinery,
  URL             https://proceedings.neurips.                 2016. doi: 10.1145/2908080.2908093. URL https:
  cc/paper_files/paper/2024/file/                              //doi.org/10.1145/2908080.2908093.
  4eff61b79274124bc71efe2ee9772f95-Paper-Conference.
  pdf.                                                       Pourcel, J., Colas, C., and Oudeyer, P.-Y. Self-improving
                                                               language models for evolutionary program synthesis: A
Loshchilov, I. and Hutter, F. Decoupled weight decay reg-      case study on ARC-AGI. In Forty-second International
  ularization. In International Conference on Learning         Conference   on Machine Learning, 2025. URL https:
  Representations, 2019. URL https://openreview.               //openreview.net/forum?id=z4IG090qt2.
  net/forum?id=Bkg6RiCqY7.
                                                             Power, A., Burda, Y., Edwards, H., Babuschkin, I., and
Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L.,      Misra, V. Grokking: Generalization beyond overfit-
  Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang,    ting on small algorithmic datasets. arXiv preprint
  Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck,        arXiv:2201.02177, 2022. URL https://arxiv.
  S., Yazdanbakhsh, A., and Clark, P. Self-refine: iterative   org/abs/2201.02177.
  refinement with self-feedback. In Proceedings of the
                                                             Reyzin, L. Statistical queries and statistical algorithms:
  37th International Conference on Neural Information
                                                               Foundations and applications, 2020. URL https://
  Processing Systems, NIPS ’23, Red Hook, NY, USA,
                                                               arxiv.org/abs/2004.00557.
  2023. Curran Associates Inc.
                                                             Rissanen, J. Stochastic Complexity in Statistical Inquiry
McAllester, D. A. Some pac-bayesian theorems. In Pro-
                                                               Theory. World Scientific Publishing Co., Inc., USA, 1989.
  ceedings of the Eleventh Annual Conference on Com-
                                                               ISBN 981020311X.
  putational Learning Theory, COLT’ 98, pp. 230–234,
  New York, NY, USA, 1998. Association for Com-              Robbins, H. and Monro, S. A stochastic approxima-
  puting Machinery. ISBN 1581130570. doi: 10.                  tion method. The Annals of Mathematical Statis-
  1145/279943.279989. URL https://doi.org/10.                  tics, 22(3):400–407, 1951.         doi: 10.1214/aoms/
  1145/279943.279989.                                          1177729586. URL https://doi.org/10.1214/
                                                               aoms/1177729586.
Meta AI. Llama 3.2: Revolutionizing edge ai and vision
  with open, multimodal models. Meta AI Blog, Septem-        Safran, I. and Shamir, O. Spurious local minima are
  ber 2024. URL https://ai.meta.com/blog/                      common in two-layer ReLU neural networks. In
  llama-3-2-connect-2024-vision-edge-mobile-devices/.          Dy, J. and Krause, A. (eds.), Proceedings of the

                                                            12
                                               LLM Priors for ERM over Programs

  35th International Conference on Machine Learn-                          Novikova, J., Forde, J. Z., Clive, J., Kasai, J., Kawamura,
  ing, volume 80 of Proceedings of Machine Learn-                          K., Hazan, L., Carpuat, M., Clinciu, M., Kim, N., Cheng,
  ing Research, pp. 4433–4441. PMLR, 10–15 Jul 2018.                       N., Serikov, O., Antverg, O., van der Wal, O., Zhang,
  URL https://proceedings.mlr.press/v80/                                   R., Zhang, R., Gehrmann, S., Mirkin, S., Pais, S., Shav-
  safran18a.html.                                                          rina, T., Scialom, T., Yun, T., Limisiewicz, T., Rieser, V.,
                                                                           Protasov, V., Mikhailov, V., Pruksachatkun, Y., Belinkov,
Scao, T. L., Fan, A., Akiki, C., Pavlick, E., Ilić, S., Hesslow,          Y., Bamberger, Z., Kasner, Z., Rueda, A., Pestana, A.,
  D., Castagné, R., Luccioni, A. S., Yvon, F., Gallé, M.,                Feizpour, A., Khan, A., Faranak, A., Santos, A., Hevia,
  Tow, J., Rush, A. M., Biderman, S., Webson, A., Am-                      A., Unldreaj, A., Aghagol, A., Abdollahi, A., Tammour,
  manamanchi, P. S., Wang, T., Sagot, B., Muennighoff, N.,                 A., HajiHosseini, A., Behroozi, B., Ajibade, B., Saxena,
  del Moral, A. V., Ruwase, O., Bawden, R., Bekman, S.,                    B., Ferrandis, C. M., McDuff, D., Contractor, D., Lansky,
  McMillan-Major, A., Beltagy, I., Nguyen, H., Saulnier,                   D., David, D., Kiela, D., Nguyen, D. A., Tan, E., Bay-
  L., Tan, S., Suarez, P. O., Sanh, V., Laurençon, H., Jer-               lor, E., Ozoani, E., Mirza, F., Ononiwu, F., Rezanejad,
  nite, Y., Launay, J., Mitchell, M., Raffel, C., Gokaslan, A.,            H., Jones, H., Bhattacharya, I., Solaiman, I., Sedenko, I.,
  Simhi, A., Soroa, A., Aji, A. F., Alfassy, A., Rogers, A.,               Nejadgholi, I., Passmore, J., Seltzer, J., Sanz, J. B., Dutra,
  Nitzav, A. K., Xu, C., Mou, C., Emezue, C., Klamm, C.,                   L., Samagaio, M., Elbadri, M., Mieskes, M., Gerchick,
  Leong, C., van Strien, D., Adelani, D. I., Radev, D., Pon-               M., Akinlolu, M., McKenna, M., Qiu, M., Ghauri, M.,
  ferrada, E. G., Levkovizh, E., Kim, E., Natan, E. B., Toni,              Burynok, M., Abrar, N., Rajani, N., Elkott, N., Fahmy,
  F. D., Dupont, G., Kruszewski, G., Pistilli, G., Elsahar, H.,            N., Samuel, O., An, R., Kromann, R., Hao, R., Alizadeh,
  Benyamina, H., Tran, H., Yu, I., Abdulmumin, I., John-                   S., Shubber, S., Wang, S., Roy, S., Viguier, S., Le, T.,
  son, I., Gonzalez-Dios, I., de la Rosa, J., Chim, J., Dodge,             Oyebade, T., Le, T., Yang, Y., Nguyen, Z., Kashyap,
  J., Zhu, J., Chang, J., Frohberg, J., Tobing, J., Bhattachar-            A. R., Palasciano, A., Callahan, A., Shukla, A., Miranda-
  jee, J., Almubarak, K., Chen, K., Lo, K., Werra, L. V., We-              Escalada, A., Singh, A., Beilharz, B., Wang, B., Brito, C.,
  ber, L., Phan, L., allal, L. B., Tanguy, L., Dey, M., Muñoz,            Zhou, C., Jain, C., Xu, C., Fourrier, C., Periñán, D. L.,
  M. R., Masoud, M., Grandury, M., Šaško, M., Huang,                     Molano, D., Yu, D., Manjavacas, E., Barth, F., Fuhrimann,
  M., Coavoux, M., Singh, M., Jiang, M. T.-J., Vu, M. C.,                  F., Altay, G., Bayrak, G., Burns, G., Vrabec, H. U., Bello,
  Jauhar, M. A., Ghaleb, M., Subramani, N., Kassner, N.,                   I., Dash, I., Kang, J., Giorgi, J., Golde, J., Posada, J. D.,
  Khamis, N., Nguyen, O., Espejel, O., de Gibert, O., Ville-               Sivaraman, K. R., Bulchandani, L., Liu, L., Shinzato, L.,
  gas, P., Henderson, P., Colombo, P., Amuok, P., Lhoest,                  de Bykhovetz, M. H., Takeuchi, M., Pàmies, M., Castillo,
  Q., Harliman, R., Bommasani, R., López, R. L., Ribeiro,                 M. A., Nezhurina, M., Sänger, M., Samwald, M., Cullan,
  R., Osei, S., Pyysalo, S., Nagel, S., Bose, S., Muhammad,                M., Weinberg, M., Wolf, M. D., Mihaljcic, M., Liu, M.,
  S. H., Sharma, S., Longpre, S., Nikpoor, S., Silberberg,                 Freidank, M., Kang, M., Seelam, N., Dahlberg, N., Broad,
  S., Pai, S., Zink, S., Torrent, T. T., Schick, T., Thrush,               N. M., Muellner, N., Fung, P., Haller, P., Chandrasekhar,
  T., Danchev, V., Nikoulina, V., Laippala, V., Lepercq,                   R., Eisenberg, R., Martin, R., Canalli, R., Su, R., Su, R.,
  V., Prabhu, V., Alyafeai, Z., Talat, Z., Raja, A., Heinzer-              Cahyawijaya, S., Garda, S., Deshmukh, S. S., Mishra,
  ling, B., Si, C., Taşar, D. E., Salesky, E., Mielke, S. J.,             S., Kiblawi, S., Ott, S., Sang-aroonsiri, S., Kumar, S.,
  Lee, W. Y., Sharma, A., Santilli, A., Chaffin, A., Stiegler,             Schweter, S., Bharati, S., Laud, T., Gigant, T., Kainuma,
  A., Datta, D., Szczechla, E., Chhablani, G., Wang, H.,                   T., Kusa, W., Labrak, Y., Bajaj, Y. S., Venkatraman, Y.,
  Pandey, H., Strobelt, H., Fries, J. A., Rozen, J., Gao, L.,              Xu, Y., Xu, Y., Xu, Y., Tan, Z., Xie, Z., Ye, Z., Bras,
  Sutawika, L., Bari, M. S., Al-shaibani, M. S., Manica, M.,               M., Belkada, Y., and Wolf, T. Bloom: A 176b-parameter
  Nayak, N., Teehan, R., Albanie, S., Shen, S., Ben-David,                 open-access multilingual language model, 2023. URL
  S., Bach, S. H., Kim, T., Bers, T., Fevry, T., Neeraj, T.,               https://arxiv.org/abs/2211.05100.
  Thakker, U., Raunak, V., Tang, X., Yong, Z.-X., Sun,
  Z., Brody, S., Uri, Y., Tojarieh, H., Roberts, A., Chung,              Shalev-Shwartz, S. and Ben-David, S. Understanding Ma-
  H. W., Tae, J., Phang, J., Press, O., Li, C., Narayanan,                 chine Learning: From Theory to Algorithms. Cambridge
  D., Bourfoune, H., Casper, J., Rasley, J., Ryabinin, M.,                 University Press, USA, 2014. ISBN 1107057132.
  Mishra, M., Zhang, M., Shoeybi, M., Peyrounette, M.,
  Patry, N., Tazi, N., Sanseviero, O., von Platen, P., Cor-              Shalev-Shwartz, S., Shamir, O., and Shammah, S. Failures
  nette, P., Lavallée, P. F., Lacroix, R., Rajbhandari, S.,               of gradient-based deep learning. In Proceedings of the
  Gandhi, S., Smith, S., Requena, S., Patil, S., Dettmers,                 34th International Conference on Machine Learning -
  T., Baruwa, A., Singh, A., Cheveleva, A., Ligozat, A.-L.,                Volume 70, ICML’17, pp. 3067–3075. JMLR.org, 2017.
  Subramonian, A., Névéol, A., Lovering, C., Garrette, D.,
  Tunuguntla, D., Reiter, E., Taktasheva, E., Voloshina, E.,             Shen, L., Mishra, A., and Khashabi, D. Do pre-trained
  Bogdanov, E., Winata, G. I., Schoelkopf, H., Kalo, J.-C.,                transformers really learn in-context by gradient descent?,

                                                                    13
                                            LLM Priors for ERM over Programs

  2024. URL https://openreview.net/forum?                            descent. In Krause, A., Brunskill, E., Cho, K., En-
  id=992eLydH8G.                                                     gelhardt, B., Sabato, S., and Scarlett, J. (eds.), Pro-
                                                                     ceedings of the 40th International Conference on Ma-
Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. R.,             chine Learning, volume 202 of Proceedings of Machine
  and Yao, S. Reflexion: language agents with verbal rein-           Learning Research, pp. 35151–35174. PMLR, 23–29 Jul
  forcement learning. In Thirty-seventh Conference on Neu-           2023. URL https://proceedings.mlr.press/
  ral Information Processing Systems, 2023. URL https:               v202/von-oswald23a.html.
  //openreview.net/forum?id=vAElhFcKW6.
                                                                   Wei, A., Suresh, T., Cao, J., Kannan, N., Wu, Y., Yan,
Singh, R. and Gulwani, S. Synthesizing number transfor-             K., Teixeira, T. S. F. X., Wang, K., and Aiken, A.
  mations from input-output examples. In Proceedings of             CodeARC: Benchmarking reasoning capabilities of LLM
  the 24th International Conference on Computer Aided               agents for inductive program synthesis. In Second Con-
  Verification, CAV’12, pp. 634–651, Berlin, Heidelberg,            ference on Language Modeling, 2025. URL https:
  2012. Springer-Verlag. ISBN 9783642314230. doi:                   //openreview.net/forum?id=Q5pVZCrrKr.
  10.1007/978-3-642-31424-7 44. URL https://doi.
  org/10.1007/978-3-642-31424-7_44.                                Wei, J., Wang, X., Schuurmans, D., Bosma, M., brian ichter,
                                                                    Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain of
Solar-Lezama, A.      Program sketching.    Interna-
                                                                    thought prompting elicits reasoning in large language
  tional Journal on Software Tools for Technology
                                                                    models. In Oh, A. H., Agarwal, A., Belgrave, D., and Cho,
  Transfer, 15(5–6):475–495, 2013.    doi: 10.1007/
                                                                    K. (eds.), Advances in Neural Information Processing
  s10009-012-0249-7. URL https://doi.org/10.
                                                                    Systems, 2022. URL https://openreview.net/
  1007/s10009-012-0249-7.
                                                                    forum?id=_VjQlMeSB_J.
Solar-Lezama, A., Tancau, L., Bodik, R., Seshia, S.,
                                                                   Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng,
  and Saraswat, V. Combinatorial sketching for finite
                                                                     B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu,
  programs. SIGARCH Comput. Archit. News, 34(5):
                                                                     D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin,
  404–415, October 2006. ISSN 0163-5964. doi: 10.
                                                                     H., Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang,
  1145/1168919.1168907. URL https://doi.org/
                                                                     J., Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang,
  10.1145/1168919.1168907.
                                                                     K., Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang,
Solomonoff, R. J. A formal theory of inductive inference.            P., Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo,
  part i. Information and Control, 7(1):1–22, 1964a. doi: 10.        S., Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang,
  1016/S0019-9958(64)90223-2. URL https://doi.                       X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y., Wan,
  org/10.1016/S0019-9958(64)90223-2.                                 Y., Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and
                                                                     Qiu, Z. Qwen3 technical report, 2025. URL https:
Solomonoff, R. J. A formal theory of inductive in-                   //arxiv.org/abs/2505.09388.
  ference. part ii. Information and Control, 7(2):
  224–254, 1964b.     doi: 10.1016/S0019-9958(64)                  Yehudai, G. and Shamir, O. On the power and limi-
  90131-7.     URL https://doi.org/10.1016/                          tations of random features for understanding neural
  S0019-9958(64)90131-7.                                             networks. In Wallach, H., Larochelle, H., Beygelz-
                                                                     imer, A., d'Alché-Buc, F., Fox, E., and Garnett, R.
Valiant, L. G. A theory of the learnable. Commun. ACM,               (eds.), Advances in Neural Information Process-
  27(11):1134–1142, November 1984. ISSN 0001-0782.                   ing Systems, volume 32. Curran Associates, Inc.,
  doi: 10.1145/1968.1972. URL https://doi.org/                       2019. URL https://proceedings.neurips.
  10.1145/1968.1972.                                                 cc/paper_files/paper/2019/file/
                                                                     5481b2f34a74e427a2818014b8e103b0-Paper.
Vapnik, V. N. Statistical Learning Theory.           Wiley-
                                                                     pdf.
  Interscience, 1998.
Vapnik, V. N. and Chervonenkis, A. Y. On the uniform               Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Huang, Z.,
  convergence of relative frequencies of events to their             Guestrin, C., and Zou, J. Textgrad: Automatic ”differen-
  probabilities. Theory of Probability and Its Applica-              tiation” via text, 2024. URL https://arxiv.org/
  tions, 16(2):264–280, 1971. doi: 10.1137/1116025. URL              abs/2406.07496.
  https://doi.org/10.1137/1116025.
Von Oswald, J., Niklasson, E., Randazzo, E., Sacramento,
  J., Mordvintsev, A., Zhmoginov, A., and Vladymy-
  rov, M. Transformers learn in-context by gradient

                                                              14
                                             LLM Priors for ERM over Programs

A. Additional Experimental Details And Results
A.1. Evaluation Tasks
We evaluate across a suite of synthetic algorithmic tasks that isolate distinct forms of structure: sparse global rules
(parity), position-invariant search (pattern matching), symmetry (palindromes), context-free constraints (Dyck-2), arithmetic
(primality), and compositions of local nonlinear maps with global summaries (CAP, SHA). Unless noted otherwise, for each
task and input length n we construct class-balanced datasets with equal numbers of positive and negative examples.

• Parity (FP/FHP/k-P). Inputs are x ∈ {0, 1}n and labels are ±1. For a fixed selector s ∈ {0, 1}n , define y(x) =
  (−1)⟨s,x⟩ . We consider: (i) full parity (FP) with s = 1n ; (ii) first-half parity (FHP) with s = (1n/2 ∥0n/2 ) (for even n);
  and (iii) random k-parity (k-P), where s is sampled uniformly from {0, 1}n subject to ∥s∥0 = k (fixed per run). Datasets
  are generated by sampling x ∼ Unif({0, 1}n ) and labeling by y(x).

• Pattern Matching
                       (Pattern1/Pattern2). Fix a binary pattern p ∈ {0, 1}k with k < n and input x ∈ {0, 1}n . The label is
  y(x) = I ∃ i ∈ {1, . . . , n − k + 1} s.t. (xi , . . . , xi+k−1 ) = p . We use p = 00111111 (Pattern1) and p = 10101010
  (Pattern2). This task requires a position-invariant “search” rule rather than reliance on fixed coordinates.
                                                                                               
• Palindrome (IsPal). For x ∈ {0, 1}n , y(x) = I ∀ i ∈ {1, . . . , ⌊n/2⌋} : xi = xn−i+1 . Positives are constructed by
  sampling a random first half and mirroring it. Negatives are generated by first constructing a palindrome and then flipping
  one bit in the first half; this produces “near-miss” negatives that share most local statistics with positives.

• Dyck-2. Let M : {0, 1}2 → {(, ), [, ]} map bit-pairs to bracket symbols, and let S(x) be the resulting bracket string
  for x ∈ {0, 1}n (so |S(x)| = n/2 when n is even). The label is y(x) = I[S(x) ∈ D2 ], where D2 is the Dyck-2 language
  of balanced parentheses with two bracket types. This probes recognition of a context-free constraint that naturally admits
  stack-like reasoning.
                                                                                                                      n
• Primality with restricted last digit (IsPrime). Inputs  are digit strings  x = (x1 , . . . , xn ) ∈ {0, . . . , 9} interpreted
  as an n-digit base-10 integer. The label is y(x) = I IsPrime(int(x)) . We construct balanced datasets by sampling
  uniformly from the set of n-digit primes (positives) and the set of n-digit composite numbers (negatives), while excluding
  leading zeros.1 We constrain the data distribution to integers whose last digit lies in {1, 3, 7, 9}, i.e., xn ∈ {1, 3, 7, 9},
  removing the most common last-digit shortcut and forcing dependence on the full input.

• Cellular Automaton Parity (CAP). Inputs are x ∈ {0, 1}n . Define a one-step local update x 7→ x′ with boundary
                               ′
          Pxn0 =′ xn+1 = 0: xi = xi−1 ⊕ (xi ∨ xi+1 ) (i = 1, . . . , n). The label is the parity of the updated string,
  conditions
  y(x) = ( i=1 xi ) mod 2. This composes a local nonlinear transformation with a global summary statistic.

• Graph Cycle Density (CountCycles, fn aa). Inputs are graphs encoded as strings of edges like u12v23u45v67 . . . ,
  where each edge is u + two-digit source + v + two-digit destination. All instances satisfy V = E = n/2, so the cycle
  rank E − V + C(G) equals the number of connected components C(G). We label by y(G) = I[C(G) > E/6]. Positives
  have many small components (e.g., triangles and disjoint edges), while negatives have one or a few large components
  (spanning tree plus extra edges). Node IDs are permuted and edges are shuffled to avoid positional shortcuts. Whenever
  necessary (running TabPFN), we tokenize the characters as follows: digits 0–9 7→ 0–9, u7→ 10, v7→ 11.

• SHA-256 Parity (SHA). For x ∈ {0, 1}n , compute the 256-bit digest (h1 , . . . , h256 ) = SHA-256(x) and output its
                  P256
  parity: y(x) = ( i=1 hi ) mod 2. Because cryptographic hashes behave pseudorandomly, this is intended as a stringent
  stress test.

A.2. Baselines
We compare LLM-PV to four families of baselines: (i) classic tabular classifiers, (ii) LMs trained from scratch with SGD,
(iii) fine-tuning pre-trained LMs, and (iv) in-context prediction with large instruction-tuned LMs. Unless stated otherwise,
experiments use m=200 labeled examples, split into |Str |=100 and |Sval |=100, and are evaluated on an independent test
set of 10,000 examples.
   0
     For Dyck-2 at n=20, the number of valid strings is too small to sample the standard-sized balanced test set without excessive
duplication; in this case we reduce the test set to 1,000 examples.
   1
     We exclude leading zeros when sampling n-digit integers.

                                                               15
                                              LLM Priors for ERM over Programs

      LLM Prompt
     Problem Statement: Given a sequence of input vectors (binary, length {sequence dimension}) and their corresponding scalar
     binary outputs (‘0’ or ‘1’), find a concise Python function f(x) that accurately approximates the underlying relationship.
     The function should not be a trainable model, but a direct logical or mathematical representation of the target function.
     Data Examples:
      000111101011110010100101001100 -> 1
      ... 011011010111000010010101001000 -> 1
     You must output ONLY a single JSON object:
      {"code": "<python function>"}

Figure 5. Prompt used in our LLM-PV procedure. We run GPT-5 with this prompt for up to k independent iterations, each returning only
Python code for a candidate target function.




Classic ML baselines. We train XGBoost, Random Forest, SVM, and a Genetic Algorithm (GA) baseline on Str and select
hyperparameters by validation performance on Sval ; reported numbers use the selected configuration and are evaluated on
the test set. Hyperparameter grids are: (i) SVM: C ∈ {0.1, 1, 10, 100}, γ ∈ {scale, auto, 0.001, 0.01, 0.1}, kernel ∈
{rbf, poly, sigmoid}; (ii) Random Forest: n estimators ∈ {64, 128, 256}, max depth ∈ {5, 10, 15, None},
min samples split ∈ {2, 5, 10}; (iii) XGBoost: n estimators ∈ {100, 128, 256}, max depth ∈ {5, 6, 7},
learning rate ∈ {0.1, 0.3}, subsample ∈ {0.8, 1.0}; (iv) Genetic Algorithm (GA): genetic programming over
Boolean expression trees with leaves given by input variables or Boolean constants and internal nodes drawn from
{NOT, XOR, AND, OR}; prediction is obtained by evaluating the tree on the input bits. Fitness is training accuracy (optionally
on a random subsample for speed) minus a small size penalty to discourage large expressions. We evolve the population
using tournament selection, subtree crossover, subtree mutation, and elitism, and return the best individual (selected by
training fitness; reported with validation/test accuracy). GA hyperparameters are: population size pop size ∈ {300, 500},
number of generations generations=80, initial program depth max depth init ∈ {6, 10}, mutation depth cap
max depth mut ∈ {4, 6}, crossover probability cx prob=0.7, and mutation probability mut prob=0.25.
Training from scratch (SGD). We train decoder-only language-model backbones from scratch as binary classifiers on
sequence-encoded pairs (x, y), minimizing binary cross-entropy with AdamW (Loshchilov & Hutter, 2019). Our SGD
baselines are Qwen3-1.7B (Yang et al., 2025), Llama3.2-1B (Meta AI, 2024), and Deepseek-Coder-1.3B (Guo
et al., 2024). We adapt each LM to classification by (i) restricting the tokenizer vocabulary to three tokens (vocab_size=3)
and (ii) replacing the LM head with a single-logit linear classifier (hidden→1). Unless stated otherwise, we train for 200
epochs with batch size 20 using cosine-annealed learning rates with ηmax =10−5 and ηmin =10−6 . To probe data scaling
with a lighter model, we additionally train BLOOM-75M, a scaled-down BLOOM-style architecture (Scao et al., 2023)
(hidden size 512, 8 heads, 24 layers), on m=100k examples per (task, n) for 1,000 epochs with batch size 256 and constant
learning rate η=10−5 .
Fine-tuning pre-trained LMs (FT). We fine-tune Qwen3-1.7B (Yang et al., 2025), Llama3.2-1B (Meta AI, 2024),
and Deepseek-Coder-1.3B (Guo et al., 2024). For each model and input length n ∈ {20, 25, 30, 50, 100}, we train
with AdamW for 1,000 epochs using a cosine-annealing learning-rate schedule, and report accuracy on 10k held-out
test examples. We evaluate both full fine-tuning and partial fine-tuning of only the top {2, 4, 8} transformer blocks.
Hyperparameters are selected via grid search over the number of tuned layers, batch size {20, 50, 100}, and learning rate
{5 × 10−3 , 10−3 , 5 × 10−4 , 10−4 , 5 × 10−5 , 10−5 }, choosing the configuration with the best test performance. The selected
batch size is 20 for all models, with peak learning rates of 10−3 for Llama3.2-1B and 5 × 10−3 for Qwen3-1.7B
and Deepseek-Coder-1.3B; the scheduler anneals to a minimum learning rate of 10−3 . All runs use bfloat16,
space-separated integer tokenization with EOS padding, and a single-logit classifier head applied to the final position.
In-context learning (ICL). We evaluate whether a large instruction-tuned LLM can recover the latent rule from
labeled examples in its context window and apply it to a new input. Concretely, given a training set Str of
200 labeled pairs, we ask whether the induced predictor h(xtest | Str ) matches the ground-truth label y(xtest ).
We use Qwen3-30B-A3B-Instruct-2507 and Qwen3-Coder-30B-A3B-Instruct (Yang et al., 2025), and
Deepseek-Coder-33B-Instruct (Guo et al., 2024). For each of 100 test inputs, we construct a prompt (Fig. 6)
containing the task description, the full set of 200 training examples, and the held-out test input, and then query the model
for the corresponding label. We decode with temperature 0.2, top-p 0.95, and a maximum of 1024 generated tokens.

                                                                16
                                                                LLM Priors for ERM over Programs

       LLM Prompt
       Problem Statement: Given a sequence of input vectors (binary, length {sequence dimension}) and their corresponding
       scalar binary outputs (’0’ or ’1’), you have to learn a hypothesis that approximates the underlying relationship. Given the data
       below, determine what is the label for the given string and output ONLY the label. Data Examples:
       000111101011110010100101001100 -> 1
       ... 011011010111000010010101001000 -> 1
       Test Input:
       010100110111001001010101001000
       You must output ONLY a single JSON object: {”lable”: ”¡your predicted label¿”}

Figure 6. Prompt used in in-context learning procedure. We run three models Qwen3-30B-A3B-Instruct-2507,
Qwen3-Coder-30B-A3B-Instruct, and Deepseek-Coder-33B-Instruct with this prompt. For each prompt, the model
outputs only the predicted label for the test input.



                                                                                          Accuracy vs. training set size
                               m=10                      m=100                      m=200                          m=1,000                     m=10,000                   m=100,000
Task       Model     Train   Test   Bound (A/T) Train   Test   Bound (A/T) Train   Test   Bound (A/T) Train       Test     Bound (A/T) Train   Test   Bound (A/T) Train   Test   Bound (A/T)
           BLOOM-75M 100% 49.9%       0.0/0.0%   100% 49.1%     0.0/0.0%   100% 49.7%        0.0/0.0%    100% 49.9%        46.7/76.5%   99.9% 50.1%   94.7/97.6%   99.8% 50.7%   99.5/99.8%
10-P
           LLM-PV    100% 49.3%       0.0/0.0%   100% 100%      0.0/0.0%   100% 100%         0.0/0.0%      –    –          46.7/76.5%     –     –     94.7/97.6%     –     –     99.5/99.8%
           BLOOM-75M 100% 50.9%       0.0/0.0%   100% 50.2%     0.0/0.0%   100% 51.3%        0.0/0.0%    100% 56.4%        22.9/71.9%   100% 59.7%    92.3/97.2%   100% 59.9%    99.2/99.7%
IsPrime2
           LLM-PV    100% 50.5%       0.0/0.0%   100% 100%      0.0/0.0%   100% 100%         0.0/0.0%      –    –          22.9/71.9%     –    –      92.3/97.2%     –    –      99.2/99.7%
           BLOOM-75M 100% 50.1%       0.0/0.0%   100% 50.4%     0.0/0.0%   100% 50.4%        0.0/0.0%    100% 50.0%         0.0/42.2%   99.6% 50.0%   85.5/94.2%   99.9% 50.4%   98.5/99.4%
CAP
           LLM-PV    100% 50.3%       0.0/0.0%   100% 50.1%     0.0/0.0%   100% 100%         0.0/0.0%      –    –           0.0/42.2%     –     –     85.5/94.2%     –     –     98.5/99.4%

Table 5. Scaling labeled data does not reliably fix SGD generalization, even on tasks with short programs. We report train/test
accuracy (%) at n=100 as a function of the number of labeled training examples m (test set size is 10k in all cases). BLOOM-75M trained
with SGD attains (near-)perfect training accuracy throughout, yet test accuracy remains near chance on 10-P and CAP, and improves only
modestly on IsPrime2. LLM-PV is far more sample-efficient in this setup, solving 10-P and IsPrime2 with m ≤ 100 and all three
tasks with m=200. The Bound (A/T) columns give the length-based lower bound 1 − m−1 [L log |Σ| + log(2L2 /δ)] (with δ=10−10 ),
evaluated using compact reference implementations with length L measured in ASCII bytes (A, |Σ|=128) or Python lexical tokens
(T, |Σ|=64 token types); values are clipped to [0, 1] and reported as A/T. This bound depends only on (m, L, |Σ|, δ) and is included to
emphasize that these targets admit short descriptions, even though SGD does not exploit this bias here.




LLM-PV. LLM-PV (Alg. 1, Fig. 2) uses a pretrained code LLM (GPT-5-Thinking) as a proposal distribution over
candidate programs. We split S into Str and Sval of equal size, build a prompt from Str (Fig. 5), sample up to k=5 candidate
programs, compile and filter invalid/duplicate outputs, and select the candidate with minimum validation error on Sval . We
run the API with reasoning effort=High, text verbosity=Low, max tokens=20k, and a per-call timeout
of 20 minutes; sampling parameters such as temperature/top-p are platform-managed.

A.3. Additional Results
A.3.1. DATA S CALING
To investigate the impact of training set size on generalization, we trained the BLOOM-75M baseline using SGD across
multiple data scales, using mtrain ∈{10, 100, 200, 1000, 10k, 100k} for n=100. This evaluation was conducted on Random
10-Parity, Cellular Automata Parity, and IsPrime (with restricted negatives). The BLOOM-75M model was trained for 1000
epochs and a constant learning rate of η=10−5 . The batch size was set to 256 for training sets with 1000 or more samples,
and to 10 for smaller datasets. The model trained on this largest dataset was also evaluated across multiple input lengths
n ∈ {20, 25, 30, 50, 100}.
The results highlight a failure of the SGD baseline to generalize, even with extensive data. As detailed in Fig. 4 and Tab. 5,
increasing the training set size did not yield better test performance; the model consistently overfits, achieving perfect
training accuracy while its test accuracy on Random 10-Parity and Cellular Automata Parity remained at the ≈50% chance
level. Furthermore, Tab. 3 show that even with 100k training samples, the model still overfits when the input dimension is
too high, with performance again collapsing to chance. In contrast, LLM-PV seems to be sample-efficient, synthesizing
correct programs for all three tasks with a training set size of just 100–200.

                                                                                          17
                                             LLM Priors for ERM over Programs

  Prompt Templates for Prompt Ablation

  P1. Given a sequence of input vectors ({data mode}, length {seq len}) mapped to scalar binary outputs, extract
  the underlying relationship as a concise Python function f(x). The solution must be a direct logical or mathematical
  expression, not a machine learning model.
  P2. Analyze the provided input vectors ({data mode}, length {seq len}) and their corresponding binary outputs
  to determine the governing logic. Express this logic as a short, deterministic Python function f(x) using mathematical
  or logical operations, avoiding trainable parameters.
  P3. Identify the mapping between the input vectors ({data mode}, length {seq len}) and binary scalar outputs.
  Represent this mapping through a concise, stateless Python function f(x) that relies only on explicit mathematical or
  logical rules rather than learned weights.
  P4. Discover the strict mathematical or logical rule that maps the input vectors ({data mode}, length {seq len})
  to their binary outputs. Output a concise Python function f(x) that formally encodes this rule without relying on any
  trainable architecture.
  P5. Infer the rule that best explains the observed input-output pairs, where each input is a vector in {data mode}
  of length {seq len} and each output is binary. Return the rule as a compact Python function f(x) using explicit
  logical or mathematical operations.

Table 6. Prompt templates used in the prompt ablation experiments. Here, {data mode} denotes the input representation and
{seq len} denotes the sequence length, with n = 100.




A.3.2. H YPERPARAMETER A BLATION
To assess whether SGD’s failures are driven by particular optimization settings, we ran learning-rate and batch-size sweeps
in the 200-sample regime, holding all other choices fixed. We trained Qwen3-1.7B for 200 epochs on 200 training samples
and evaluated on 10k random test samples, across three representative tasks (10-P, Pattern2, IsPal) and lengths up to n=100.
For the learning-rate sweep, we used batch size B=20 and varied η ∈ {8 × 100 , 8 × 10−1 , . . . , 8 × 10−7 }. For the batch-size
sweep, we fixed η and varied B ∈ {10, 20, 50, 100, 200}. Tab. 9 reports, for each (task, n), the best test accuracy achieved
over the corresponding sweep.
Across both sweeps, the qualitative picture is unchanged. Random 10-Parity (10-P) stays at chance for all n, even after
selecting the best η or the best B (max ≤ 51.1%), indicating that no setting in these ranges yields meaningful generalization.
Pattern Matching (Pattern2) can reach near-perfect accuracy at short lengths (e.g., 100% at n=20 when sweeping η), but
performance drops sharply with increasing n and falls to 56.9% at n=100 even after optimizing over η (and to 65.5% after
optimizing over B). Similarly, IsPalindrome (IsPal) improves at short lengths under the best settings (up to 72.4% at n=20),
yet collapses to chance by n=100 (max 50.0% over η and 49.6% over B).
Overall, tuning learning rate or batch size mainly affects short-length performance and does not prevent the systematic
degradation with length. This supports the interpretation that the dominant failure mode is out-of-distribution length
generalization, rather than a fixable optimization detail.

A.3.3. P ROMPT A BLATION
We evaluate the sensitivity of LLM-PV to the exact wording of the prompt given to GPT-5-Thinking. To construct the
ablation, we use five prompt templates that express the same high-level instruction: infer the relationship from the training
samples and return a concise Python function f(x) that implements the rule. The prompts differ only in phrasing, not in
the information provided to the model.
Tab. 7 reports the performance of LLM-PV under each prompt. The results are stable across prompt variations. In particular,
all prompts achieve perfect performance on PATTERN 2, 10-P, IS P RIME, and CAP. On the hardest task, IS P RIME +47,
performance varies mildly across prompts, with an average accuracy of 82.5 ± 3.1. These results suggest that the gains of
LLM-PV are not driven by a carefully engineered prompt.

                                                              18
                                              LLM Priors for ERM over Programs

                     Prompt        Pattern2          10-P           isPrime       CAP          isPrime+47
                     P1               100            100             100           100             81.8
                     P2               100            100             100           100             77.9
                     P3               100            100             100           100             86.7
                     P4               100            100             100           100             83.0
                     P5               100            100             100           100             83.0
                     Average        100 ± 0        100 ± 0        100 ± 0       100 ± 0        82.5 ± 3.1
Table 7. Prompt variation results for LLM-PV. We report test accuracy across five prompt templates. Performance is stable across
prompt rephrasings, indicating that the method is not sensitive to a single carefully engineered prompt.




                                                             Train time                    Test time
                     Method                             (seconds per sample)         (seconds per sample)
                     SGD: Qwen3-1.7B                            0.671                         0.016
                     FT: Qwen3-1.7B                             0.345                         0.017
                     LLM-PV: GPT-5                              2.091                         0.224
                     ICL: GPT-5-Thinking                        0.001                        53.961
                     ICL: Qwen3-30B-Instruct                    0.001                         0.139
Table 8. Wall-clock runtime. Train and test times are reported in seconds per sample. LLM-PV has higher training cost due to
LLM-based proposal generation, but its selected program can be evaluated efficiently at test time.




A.3.4. WALL -C LOCK T IMES
We report the wall-clock runtime of the main baselines and LLM-PV in Tab. 8. The comparison includes SGD training
from scratch and fine-tuning on Qwen3-1.7B, LLM-PV with GPT-5, and in-context learning with GPT-5-Thinking
and Qwen3-30B-Instruct. All times are normalized per sample, computed as the total runtime divided by the number
of samples. For SGD training from scratch and fine-tuning, we report the runtime using the minimum number of epochs
required to reach 100% training accuracy.
The results highlight the main computational tradeoff. LLM-PV incurs the largest training-time cost, primarily because
program proposals are generated by an LLM. However, once a program has been selected, inference is fast: its test-time
cost is substantially lower than GPT-5-Thinking in-context learning and competitive with the other non-API baselines.
Gradient descent and fine-tuning are fast at test time, but their predictive performance is poor. In-context learning avoids
training altogether, but its test-time cost can be large because every test example requires a fresh model call. Thus, LLM-PV
shifts computation from test time to training time and obtains the best performance while retaining efficient deployment.

A.4. LLM Reasoning Traces
We extend (Fig. 7) the reasoning-trace analysis from Fig. 1 to Cellular Automata Parity and Full Parity to highlight how the
model adapts its search strategy across tasks.
For Cellular Automata Parity, the model starts with simple dataset checks and parity-style baselines, then attempts a linear
rule over F2 . When this fails, it escalates to a structured search over non-linear, hand-designed features (for example edge
bits, transition counts such as #01/#10, and their parities), and identifies an XOR rule that fits perfectly. It then rewrites the
rule using parity identities and verifies equivalent forms.
For Full Parity, the trace is much shorter: after a quick sanity check, the model proposes global parity and immediately
verifies a perfect match. This contrast shows that the model expands its hypothesis class only when simpler families fail, but
locks onto the correct rule quickly when it is obvious.

                                                               19
                                                                               LLM Priors for ERM over Programs

                                                            Task          Summary                           n=20 n=25 n=30 n=50 n=100
                                                                          max over η                             50.4          50.3   50.4           50.2            51.1
                                                            10-P
                                                                          max over B                             50.8          50.4   50.4           50.9            50.4
                                                                          max over η                         100.0             94.8   93.9           87.9            56.9
                                                            Pattern2
                                                                          max overB                           97.7             96.4   96.0           89.5            65.5
                                                                          max over η                             72.4          60.5   54.5           50.3            50.0
                                                            IsPal
                                                                          max over B                             68.6          57.5   53.9           50.8            49.6
Table 9. Hyperparameter ablations (test accuracy, %). For each task and sequence length n, we report the maximum test accuracy
obtained by sweeping learning rates η ∈ {8 × 100 , . . . , 8 × 10−7 } and batch sweep over B ∈ {10, 20, 50, 100, 200}. 10-P remains near
chance across all n, while Pattern2 and IsPal achieve high accuracy at short lengths but degrade substantially as n increases.


 Step       Type                    Candidate function                                  Rationale                              Step     Type                    Candidate function                                      Rationale
                           Dataset check                                                                                                               Ones-count scan
  1        Analysis
                           Class balance and basic counts
                                                                       Start with simple baselines                              1      Analysis
                                                                                                                                                       Check #1(x) statistics; sweep thresholds
                                                                                                                                                                                                      Start with simple dataset-level features


         Candidate A
                           Population parity (Train acc: 58%)                                                                                          ParityP
                                                                                                                                                             of ones 
  2                        Mod-3 baseline (Train acc: 36%)
                                                                       Quick arithmetic heuristics                              2     Candidate A      ŷ =    49
                                                                                                                                                               i=0 xi mod 2 (Train acc: 51%)
                                                                                                                                                                                                      Classic baseline on binary strings
         Candidate B

                                                                                                                                      Candidate B      Edge bits
                           Linear fit over F2
  3        Analysis
                           Solve Xw = y (mod 2); inconsistent.
                                                                       Try structured features beyond a single parity.          3                      ŷ = x0 (Train acc: 50%)                       Test whether boundary bits drive the label
                                                                                                                                      Candidate C      ŷ = x49 (Train acc: 48%)

                           Threshold on #1
                                                                                                                                                       Linear solve over F2
  4      Candidate C       Best over t: ŷ = 1{#1 ≥ t}                 Count-based separators are weak; try transitions         4      Analysis                                                       Recover a sparse XOR by Gaussian elimination
                                                                                                                                                       Solve Xw = y (mod 2) for X ∈ F100×50
                                                                                                                                                                                     2      .
                           (Train acc: 55%)
                                                                                                                                                       Support set
                           Threshold on transitions
                                                                                                                                                       Identify S      =
  5      Candidate D       Best over t: ŷ = 1{#01 + #10 ≥ t}          Move to parity/XOR combinations of features              5     Hypothesis                                                      Back-substitution reveals active indices
                                                                                                                                                       {0, 8, 17, 18, 20, 25, 30, 34, 36, 42}
                           (Train acc: 61%)
                                                                                                                                                       (0-based).
           Analysis        Feature-mask XOR search
                           Best over XOR masks: f (x) = xlast ⊕        Search XORs over a small hand-designed fea-                                     Final XOR
                                                                                                                                                               L rule
  6                        (#01 mod 2)                                 ture set                                                 6     Verification     f (x) =   i∈S xi (Train acc: 100%)
                                                                                                                                                                                                      Exact match on all training examples
         Hypothesis 1      (Train acc: 100%)

                           Edge-bit only
  7                                                                    Check if a simpler rule suffices
         Refinement A      Best edge-bit classifier (Train acc: 44%)                                                                                      (b) Random 10-Parity
                           Transition parity only
  8      Refinement B      Best ŷ = (#01 mod 2)                       Isolate which feature drives the XOR rule
                           (Train acc: 58%)                                                                                    Step     Type                    Candidate function                                      Rationale
                           Parity identity                                                                                                             Ones-count check
  9        Analysis
                           #01 − #10 = xlast − xfirst .
                                                                       Use identities to rewrite the hypothesis
                                                                                                                                1      Analysis
                                                                                                                                                       Summarize #1(x); threshold baselines
                                                                                                                                                                                                      Start with simple statistics at length 50.


                           Equivalent form                                                                                                             Full parityP
 10      Verification 1    f (x) = xfirst ⊕ (#10 mod 2)                Verify an algebraically equivalent rule                                                      49
                                                                                                                                                                                                     If labels encode global XOR, parity should
                           (Train acc: 100%)
                                                                                                                                2     Candidate A      f (x) =      i=0 xi mod 2                      match
                                                                                                                                                       (Train acc: 100%)

                           Final form                                                                                                 Hypothesis
                           f (x) = xlast ⊕ (#01 mod 2)                                                                                                 Verify on all samples
 11      Verification 2                                                Same rule; most concise statement                        3                      Parity matches every label (Train acc: 100%)
                                                                                                                                                                                                      Hypothesis confirmed; exact rule found
                           (Train acc: 100%)                                                                                          Verification



                          (a) Cellular Automata Parity                                                                                                             (c) Full Parity
Figure 7. Reasoning traces for discrete synthetic tasks. Left: Cellular Automata Parity, where the search escalates from simple
heuristics to an XOR rule over hand-designed features and then simplifies it via parity identities. Right (top): Random 10-Parity, solved
by a linear system over F2 that recovers the active XOR support. Right (bottom): Full Parity, identified directly by the global parity
hypothesis and verified on all samples.


B. Proofs
B.1. Proof of Eq. 1
Theorem B.1 (Valiant (1984); see also Cor. 2.3 of Shalev-Shwartz & Ben-David (2014)). Let y : X → {±1} be an unknown
target function and let H ⊂ {±1}X be a finite hypothesis class. Suppose we are in the realizable setting (i.e., y ∈ H). Let
S = {(xi , y(xi ))}m
                   i=1 be m training examples drawn i.i.d. from a distribution D over X × {±1}. Then, with probability at
least 1 − δ over the draw of S, every hypothesis h ∈ H that is consistent with S satisfies

                                                                                                                   log(|H|) + log(1/δ)
                                                                                errD (h) ≤                                             .
                                                                                                                            m

Corollary B.2. Let y : X → {±1} be an unknown target function and let H = ℓ≥1 Hℓ ⊂ {±1}X be a union of finite
                                                                                        S
sets. Suppose we are in the realizable setting (i.e., y ∈ H). Let S = {(xi , y(xi ))}m  i=1 be m training examples drawn i.i.d.
from a distribution D over X × {±1}. Then, with probability at least 1 − δ over the draw of S, for any ℓ ∈ N and any
hypothesis h ∈ Hℓ that is consistent with S, it holds that
                                                                                       
                                                       log(|Hℓ |) + log (π 2 /6) ℓ2 /δ
                                       errD (h) ≤                                        .
                                                                      m
                                                                                                                          20
                                            LLM Priors for ERM over Programs

Algorithm 2 Length-First Program Search (LFPS)
                                                        ∗
Require: Sample S = {(xi , yi )}m   i=1 , language L ⊆ Σ , per-run timeout T ∈ N, optional max length Lmax ∈ N ∪ {∞}
Ensure: A program u ∈ L whose total semantics Ju K : X → {±1} satisfies Ju⋆ K(xi ) = yi for all (xi , yi ) ∈ S; or ⊥ if
                           ⋆                            ⋆

    none is found up to Lmax
 1: for ℓ = 1, 2, . . . , Lmax do
 2:   for all strings u ∈ L with |u| = ℓ in lexicographic order do
 3:      if u fails to compile then continue
 4:      consistent ← true
 5:      for each (xi , yi ) ∈ S do
 6:         Run u on input xi for at most T steps; let oi ∈ {±1, ⊥} be the output (⊥ if no halt)
 7:         if oi = ⊥ or oi ̸= yi then
 8:            consistent ← false; break
 9:         end if
10:      end for
11:      if consistent then
12:         return u⋆ ← u                                                            {minimal-length consistent program}
13:      end if
14:   end for
15: end for
16: return ⊥                                                               {no consistent total program found up to Lmax }


Proof. Assume that y ∈ H = ℓ≥1 Hℓ ; hence, there exists some ℓ∗ for which Hℓ∗ is realizable. For each fixed ℓ with at
                               S
least one hypothesis consistent with S, Thm. B.1 implies that for any δℓ > 0, with probability at least 1 − δℓ , every h ∈ Hℓ
consistent with S satisfies
                                                        log(|Hℓ |) + log(1/δℓ )
                                           errD (h) ≤                           .
                                                                   m
Choose δℓ = π62 ℓδ2 , so that ℓ≥1 δℓ = δ. Then, for each such ℓ, with probability at least 1 − δℓ ,
                             P

                                                                                  
                                                  log(|Hℓ |) + log (π 2 /6) ℓ2 /δ
                                       errD (h) ≤                                   .
                                                                 m
Applying a union bound over all ℓ ≥ 1 yields the claim (for each ℓ with no consistent hypothesis, the inequality is
vacuous).

Proposition B.3. Suppose we wish to learn a target function y : X → {±1} that can be implemented as a program of
length L in a programming language L. Let Lℓ denote the set of programs of length ℓ in L, and let S = {(xi , y(xi ))}m
                                                                                                                     i=1 be
m training examples drawn i.i.d. from a distribution D over X × {±1}. Then, with probability at least 1 − δ over the draw
of S, Alg. 2 outputs a program h ∈ L that is consistent with S and satisfies

                                                        L log |Σ| + log(2L2 /δ)
                                           errD (h) ≤                           .
                                                                   m

Proof. Since y ∈ L, there exists a minimal length L such that y ∈ LL . Therefore, there is at least one program of length
L consistent with S. Alg. 2 enumerates programs in order of increasing length, so it eventually returns a program h of
some length ℓ ≤ L that is consistent with S. Every program in Lℓ is described over the alphabet Σ, hence |Lℓ | ≤ |Σ|ℓ and
log |Lℓ | ≤ ℓ log |Σ| ≤ L log |Σ|. Applying Cor. B.2 with H = L and Hℓ = Lℓ and then upper-bounding by L gives

                                          log |Lℓ | + log(2ℓ2 /δ)   L log |Σ| + log(2L2 /δ)
                             errD (h) ≤                           ≤                         .
                                                     m                         m


Proposition 4.1. Fix ϵ ≥ 0 and δ ∈ (0, 1). Draw independent samples Str ∼ Dmtr and Sval ∼ Dmval with labels from the
target y : X → {±1}. Run Alg. 1 for k trials, and assume each trial outputs an accepted total hypothesis ht : X → {±1}

                                                             21
                                               LLM Priors for ERM over Programs

using only Str . Let h⋆ ∈ arg mint∈[k] errSval (ht ) be the returned hypothesis. If k ≥ ⌈ log(δ/2)  ⌉, then with probability
                                                                                         log 1−pϵ (Str )
                                                                            ⋆
                                                                                        p
at least 1 − δ over (Str , Sval ) (and all algorithmic randomness), errD (h ) ≤ ϵ + 2 log(4k/δ)/(2mval ).

Proof. Fix ϵ ≥ 0 and δ ∈ (0, 1). Throughout the proof we condition on the (random) training set Str and use that, by
assumption, all k trials produce accepted hypotheses using only Str . Hence, conditioned on Str , the hypotheses (ht )kt=1
are i.i.d. draws from the (accepted) proposal distribution q(· | Str ) and are independent of Sval . (Here |Str | = mtr and
|Sval | = mval .)

Step 1: a near-ϵ candidate appears with high probability.              Define the set of ϵ-good hypotheses
                                            Gϵ := {h : X → {±1} : errD (h) ≤ ϵ}.
By definition,
                                                  pϵ (Str ) =       Pr    [ h ∈ Gϵ ].
                                                                h∼q(·|Str )
Let Ehit be the event that at least one of the k candidates is ϵ-good:
                                                        n                   o
                                              Ehit := ∃ t ∈ [k] s.t. ht ∈ Gϵ .

Conditioned on Str , since the ht are i.i.d. from q(· | Str ),
                                                                               
                                       c
                                                                       / Gϵ Str = (1 − pϵ (Str ))k .
                                               
                                 Pr Ehit  | Str = Pr ∀t ∈ [k], ht ∈
            l                    m
                log(δ/2)
Assume k ≥ log(1−p    ϵ (S tr ))  . Since log(1 − pϵ (Str )) ≤ 0, this implies (1 − pϵ (Str ))k ≤ δ/2, and therefore
                                                                   
                                                   Pr Ehit | Str ≥ 1 − δ/2.                                               (2)

Step 2: uniform validation-to-population deviation over k hypotheses. For each fixed hypothesis h, by Hoeffding’s
inequality applied to the Bernoulli losses 1{h(x′j ) ̸= y(x′j )} on Sval with |Sval | = mval ,
                                                                                       2
                                     Pr errSval (h) − errD (h) > α ≤ 2e−2mval α .
Conditioned on Str , the hypotheses h1 , . . . , hk are independent of Sval , so we can apply the above bound to each ht and
union bound over t ∈ [k]:
                                                                k
                                                                  X           2              2
                      Pr max errSval (ht ) − errD (ht ) > α Str ≤   2e−2mval α = 2k e−2mval α .
                          t∈[k]
                                                                                t=1
Choose                                                          s
                                                                    log(4k/δ)
                                                       α :=                   .
                                                                      2mval
                  2
Then 2ke−2mval α = 2ke− log(4k/δ) = δ/2, hence
                                                                        
                          Pr ∀t ∈ [k], errSval (ht ) − errD (ht ) ≤ α Str ≥ 1 − δ/2.                                      (3)
Let Eunif denote the event inside (3).

Step 3: conclude the bound on errD (h⋆ ). On the intersection Ehit ∩ Eunif , pick an index tgood ∈ [k] such that
htgood ∈ Gϵ , so errD (htgood ) ≤ ϵ. Also, on Eunif we have for all t,
                           errSval (ht ) ≤ errD (ht ) + α        and          errD (ht ) ≤ errSval (ht ) + α.
         ⋆
Since h ∈ arg mint∈[k] errSval (ht ),
                                  errSval (h⋆ ) ≤ errSval (htgood ) ≤ errD (htgood ) + α ≤ ϵ + α.
Applying the other side of the uniform deviation bound to h⋆ yields
                                                                                          s
                                                                                              log(4k/δ)
                                  errD (h⋆ ) ≤ errSval (h⋆ ) + α ≤ ϵ + 2α = ϵ + 2                       .
                                                                                                2mval

                                                                  22
                                             LLM Priors for ERM over Programs

Step 4: probability of the good event.    By (2) and (3) and a union bound (still conditioned on Str ),
                                                         
                                    Pr Ehit ∩ Eunif | Str ≥ 1 − δ/2 − δ/2 = 1 − δ.

Removing the conditioning (i.e., averaging over Str ) preserves the same lower bound, so with probability at least 1 − δ over
(Str , Sval ) and all algorithmic randomness,
                                                                  s
                                                     ⋆               log(4k/δ)
                                              errD (h ) ≤ ϵ + 2                .
                                                                       2mval

This is exactly the claimed guarantee.

C. Finite-Precision Mini-Batch SGD as a 1-STAT(b) Statistical Algorithm
Consider optimizing a parameter vector θ ∈ Θ ⊆ Rd from i.i.d. data z ∼ D via a loss ℓ(θ, z). To model b-bit access to
gradients in the statistical-query framework, we assume each per-example coordinate gradient is uniformly bounded: there
exists G > 0 such that for all θ ∈ Θ, j ∈ [d], and z ∈ Z, |∂j ℓ(θ, z)| ≤ G.
Coordinate mini-batch SGD. We consider a simple coordinate version of mini-batch SGD. Fix a batch size B and step
sizes (ηt )t≥1 . Starting from θ1 , at each iteration t the algorithm selects a coordinate jt ∈ [d] to update (the choice may
                                                                                                          i.i.d.
depend on the past randomness and observations). It then draws a fresh mini-batch zt,1 , . . . , zt,B ∼ D and uses these
samples to estimate the jt -th partial derivative by the empirical average
                                                                  B
                                                              1 X
                                                  gbt,jt :=        ∂j ℓ(θt , zt,i ).
                                                              B i=1 t

Finally, it takes a step along that coordinate:

                                                    θt+1 = θt − ηt gbt,jt ejt .

Finite-precision model. To obtain sample/iteration lower bounds, we analyze a finite-precision abstraction of coordinate
mini-batch SGD. The point is that, in many implementations, each per-example coordinate gradient is effectively represented
with only a small number of bits. This finite-precision view is also convenient for connecting SGD to the statistical-algorithm
framework (Reyzin, 2020).
Fix an integer b ≥ 1 and set M := 2b . Partition the interval [−G, G] into M equal bins of width ∆ := 2G
                                                                                                      M . For any
u ∈ [−G, G], define the (clipped) bin index
                                            n                   o
                            idx(u) := min M − 1, (u + G)/∆ ∈ {0, 1, . . . , M − 1},

and map u to the midpoint of its bin:
                                                            
                                   Qb (u) := −G + idx(u) + 12 ∆,                   u ∈ [−G, G].

This is a deterministic b-bit quantizer with worst-case error at most half a bin: for all u ∈ [−G, G],

                                                  |Qb (u) − u| ≤ ∆/2 = G/2b .                                                 (4)

Definition C.1 (b-bit coordinate mini-batch SGD). The b-bit variant of coordinate mini-batch SGD replaces each per-
                                   (b)                                          (b)
example coordinate gradient ∂jt ℓ(θt , zt,i ) by its quantized value Qb (∂jt ℓ(θt , zt,i )). At iteration t it forms the quantized
mini-batch estimate
                                                          B
                                               (b)     1 X              (b)      
                                             gbt,jt :=       Qb ∂jt ℓ(θt , zt,i ) ,
                                                       B i=1
and updates only coordinate jt :
                                                     (b)        (b)       (b)
                                                   θt+1 = θt − ηt gbt,jt ejt .

                                                                  23
                                                LLM Priors for ERM over Programs

Before turning to lower bounds, we introduce a simple stability estimate for finite-precision updates. Intuitively, the b-bit
run differs from the full-precision run in two ways: each per-example coordinate gradient is quantized, and the two runs
may evaluate gradients at slightly different iterates. Under a Lipschitz assumption on per-example coordinate gradients, the
accumulated deviation between the two coupled trajectories scales with the rate of precision O(2−b ).
Lemma C.2 (Quantization error telescoping under Lipschitz gradients). Fix b ∈ N and a quantizer Qb : [−G, G] → [−G, G]
satisfying |Qb (x) − x| ≤ 2Gb for all x ∈ [−G, G]. Assume per-example coordinate gradients are bounded and Lipschitz in
parameters: there exists L > 0 such that for all θ, θ′ ∈ Θ, all z ∈ Z, and all j ∈ [d],

                                 |∂j ℓ(θ, z)| ≤ G,            |∂j ℓ(θ, z) − ∂j ℓ(θ′ , z)| ≤ L∥θ − θ′ ∥2 .                 (5)

At iteration t, define the (unquantized) mini-batch coordinate gradient
                                                                 B
                                                          1 X
                                              gbt,jt :=        ∂j ℓ(θt , zt,i ) ∈ [−G, G],
                                                          B i=1 t

and the b-bit mini-batch coordinate gradient
                                                          B
                                         (b)         1 X             (b)       
                                        gbt,jt :=          Qb ∂jt ℓ(θt , zt,i ) ∈ [−G, G].
                                                     B i=1

                                                                         (b)
Consider two coupled runs that use the same initialization θ1 = θ1 , the same coordinates (jt )t≥1 , and the same mini-
batches (zt,i ), updated by
                                                              (b)      (b)     (b)
                              θt+1 = θt − ηt gbt,jt ejt ,    θt+1 = θt − ηt gbt,jt ejt .
Then, for all T ≥ 1,
                                                    T     T                           T
                         (b)                    GX        Y               G        X           
                       ∥θT +1 − θT +1 ∥2 ≤            η t    1 + Lη r   ≤      exp L     ηt   − 1   ,                     (6)
                                                2b t=1 r=t+1              2b L       t=1

with the convention that the empty product equals 1 (so the t = T term is ηT ).

Proof. Fix t. Write
                                                           (b)
                                       at,i := ∂jt ℓ(θt , zt,i ),              bt,i := ∂jt ℓ(θt , zt,i ).
By the triangle inequality,
                                                       B                  B
                                (b)                 1 X                1 X
                               gbt,jt − gbt,jt =          Qb (at,i ) −       bt,i
                                                    B i=1              B i=1
                                                       B                         B
                                                    1 X                      1 X
                                               ≤          Qb (at,i ) − at,i +       (at,i − bt,i )
                                                    B i=1                     B i=1
                                                    B                            B
                                                 1 X                          1 X
                                               ≤       |Qb (at,i ) − at,i | +       |at,i − bt,i |.
                                                 B i=1                        B i=1

By the quantization property, |Qb (at,i ) − at,i | ≤ G/2b . By the coordinate Lipschitz condition (5),
                                                   (b)                                       (b)
                        |at,i − bt,i | = ∂jt ℓ(θt , zt,i ) − ∂jt ℓ(θt , zt,i ) ≤ L∥θt − θt ∥2               for each i.

Therefore,
                                                   (b)                 G       (b)
                                                gbt,jt − gbt,jt ≤         + L∥θt − θt ∥2 .                                (7)
                                                                       2b
Now subtract the updates:
                                        (b)                      (b)                  (b)
                                       θt+1 − θt+1 = (θt − θt ) − ηt (b
                                                                      gt,jt − gbt,jt )ejt .

                                                                       24
                                              LLM Priors for ERM over Programs

Taking ℓ2 norms and using ∥ejt ∥2 = 1 gives
                                        (b)                 (b)                (b)
                                      ∥θt+1 − θt+1 ∥2 ≤ ∥θt − θt ∥2 + ηt gbt,jt − gbt,jt .

Plugging (7) yields the recursion
                                                        G                              (b)
                                ∆t+1 ≤ (1 + Lηt )∆t + ηt b ,           where ∆t := ∥θt − θt ∥2 .
                                                        2
             (b)
Assuming θ1 = θ1 so that ∆1 = 0, unrolling gives
                                                            T    T
                                                        GX       Y
                                              ∆T +1 ≤         ηt    (1 + Lηr ),
                                                        2b t=1 r=t+1

which is the first bound in (6).
For the second bound, use 1 + u ≤ eu to obtain
                                               T
                                               Y                    XT   
                                                   (1 + Lηr ) ≤ exp L   ηr .
                                              r=t+1                       r=t+1
               PT                     LSt
Define St :=        r=t ηr and At := e    , so At = eLηt At+1 and AT +1 = 1. Then
                                                                                             1
                        At − At+1 = (eLηt − 1)At+1 ≥ Lηt At+1           =⇒     ηt At+1 ≤       (At − At+1 ).
                                                                                             L
Summing this inequality over t = 1, . . . , T yields
         T              T         T               T
         X          X         X              1X                  1                1  L PTt=1 ηt   
             ηt exp L       ηr =     ηt At+1 ≤       (At − At+1 ) = (A1 − AT +1 ) =    e           −1 .
         t=1          r=t+1      t=1
                                               L t=1               L                L

Therefore,
                                                                    T
                                                         G        X            
                                              ∆T +1 ≤        exp L     η t   − 1   ,
                                                        2b L       t=1

establishing (6).

C.1. b-Bit Coordinate Mini-Batch SGD as a 1-STAT(b) Algorithm
A 1-STAT(b) query is a vector of b Boolean functions g = (g1 , . . . , gb ) with gk : Z → {0, 1}. The oracle draws a fresh
z ∼ D and returns (g1 (z), . . . , gb (z)) ∈ {0, 1}b .

Encoding the quantized gradient as a 1-STAT(b) answer. Fix (θ, j). Recall that the quantizer Qb defined above maps
[−G, G] to exactly M := 2b midpoints, indexed by {0, . . . , M − 1}. For a sample z ∈ Z, define
                                                               
                                idxθ,j (z) := idx ∂j ℓ(θ, z) ∈ {0, 1, . . . , M − 1}.

For each r ∈ {1, . . . , b}, define the Boolean function grθ,j : Z → {0, 1} as the r-th bit (under a fixed convention) of the
binary representation of idxθ,j (z):
                                                 grθ,j (z) := bitr (idxθ,j (z)) .
Then one call to 1-STAT(b) on (g1θ,j , . . . , gbθ,j ) returns the b bits encoding idxθ,j (z) for a fresh sample z ∼ D, from which
the algorithm reconstructs                                                              
                                         Qb ∂j ℓ(θ, z) = −G + idxθ,j (z) + 12 ∆.
                                                           

Lemma C.3 (b-bit mini-batch SGD is a 1-STAT(b) statistical algorithm). A T -iteration run of b-bit coordinate mini-batch
SGD (Definition C.1) with batch size B can be implemented using exactly q = T B calls to 1-STAT(b), plus internal
computation.

                                                                  25
                                              LLM Priors for ERM over Programs

                                                                                                           (b)
Proof. At iteration t, for each i = 1, . . . , B the algorithm needs the quantized value Qb (∂jt ℓ(θt , zt,i )) for a fresh zt,i ∼ D.
           (b)
Fix θ = θt and j = jt . Using the encoding above, one call to 1-STAT(b) on (g1θ,j , . . . , gbθ,j ) returns the b bits encoding
idxθ,j (zt,i ), hence allows reconstruction of Qb (∂j ℓ(θ, zt,i )). Repeating this for i = 1, . . . , B yields the B quantized
                                                                 (b)                             (b)
per-example gradients, which can be averaged to obtain gbt,jt and then used to update θt+1 . Over T iterations this uses
exactly T B oracle calls.
Lemma C.4 (SDA for planted k-parity testing). Let n ≥ 1, k ∈ {1, . . . , n}, and let
                                                                                                                 
                           n                                                n                                    n
              X = {0, 1} ,         Y = {±1},          Sk := {s ∈ {0, 1} : ∥s∥0 = k},               N := |Sk | =     .
                                                                                                                 k

For each s ∈ Sk , let Ds be the realizable distribution on X × Y given by
                                                                                             n
                                                                                             X
                                                              ⟨s,x⟩
                   x ∼ Unif(X ),        y = fs (x) := (−1)            ,    where ⟨s, x⟩ :=         si xi     (mod 2).
                                                                                             i=1

Let D0 be the null distribution where x ∼ Unif(X ) and y ∼ Unif(Y) independently. Let χD0 (·, ·) and ρ(·, D0 ) be as in
Definitions 27–28 of Reyzin (2020) (equivalently, Feldman et al. (2018)).
Then for every nonempty D′ ⊆ {Ds : s ∈ Sk } with |D′ | = m, we have
                                                                          1
                                                        ρ(D′ , D0 ) =       .
                                                                          m
(Here ρ includes diagonal terms, i.e., D1 , D2 are drawn independently and uniformly from D′ , so Pr[D1 = D2 ] = 1/|D′ |.)
Consequently, for the promise testing problem Z (distinguish D0 from some Ds ), define SDAZ (Z, γ̄) to be the integer-valued
statistical dimension with average correlation, namely the largest integer d ≥ 1 such that for every D′ ⊆ {Ds : s ∈ Sk }
with |D′ | ≥ N/d, we have ρ(D′ , D0 ) ≤ γ̄; if no such integer exists, define SDAZ (Z, γ̄) := 0. Then for every γ̄ ∈ (0, 1),
                                                          (
                                                            Θ(γ̄N ), if γ̄ ≥ 1/N,
                                         SDAZ (Z, γ̄) =
                                                            0,          if γ̄ < 1/N.

In particular, when γ̄ < 1/N , Theorem 30 is vacuous in this regime (and in particular, it does not imply any ω(1) query
lower bound).
Remark C.5 (Real-valued SDA and the γ̄ < 1/N regime). Definition 29 in Reyzin (2020) defines SDA(Z, γ̄) as the largest
real d > 0 such that for every D′ ⊆ {Ds : s ∈ Sk } with |D′ | ≥ N/d we have ρ(D′ , D0 ) ≤ γ̄. When a maximum need not
be attained, we use the standard extension
                                           n                                                       o
                   SDAsup (Z, γ̄) := sup d > 0 : ∀ D′ ⊆ {Ds } with |D′ | ≥ N/d, ρ(D′ , D0 ) ≤ γ̄ .

In our setting, if γ̄ < 1/N then the feasible set equals (0, 1) (all d ∈ (0, 1) make the condition vacuous, while no d ≥ 1 is
feasible), and hence SDAsup (Z, γ̄) = 1. Therefore Theorem 30 yields at most an O(1) (in particular, not ω(1)) query lower
bound in this regime.

Proof. Fix s, s′ ∈ Sk . For (x, y) ∈ X × Y, under the null distribution D0 we have x ∼ Unif(X ) and y ∼ Unif(Y)
independent, hence
                                               D0 (x, y) = 2−(n+1) .
Under Ds , we have x ∼ Unif(X ) and y = fs (x) deterministically, so

                                                Ds (x, y) = 2−n · 1{y = fs (x)}.

Therefore
                                                                                   (
              Ds (x, y)                                                   Ds        1,       y = fs (x),
                        = 2 · 1{y = fs (x)},         and hence               −1=                          = y fs (x).
              D0 (x, y)                                                   D0        −1,      y = −fs (x),

                                                                 26
                                            LLM Priors for ERM over Programs

By Definition 27 (pairwise correlation),
                                                                       
                                                           Ds       Ds′
                       χD0 (Ds , Ds′ ) = E(x,y)∼D0            −1        −1
                                                           D0       D0
                                                                                              
                                       = E(x,y)∼D0 yfs (x) · yfs′ (x) = Ex∼Unif(X ) fs (x)fs′ (x) .

Moreover,
                                                                         ′                   ′
                                     fs (x)fs′ (x) = (−1)⟨s,x⟩+⟨s ,x⟩ = (−1)⟨s⊕s ,x⟩ ,
where ⊕ is bitwise XOR. Since x is uniform on {0, 1}n ,
                                                                        (
                                                           ⟨t,x⟩            1,   t = 0,
                                               Ex [(−1)            ]=
                                                                            0,   t ̸= 0,

so χD0 (Ds , Ds′ ) = 1 if s = s′ and 0 otherwise.
Now let D′ ⊆ {Ds : s ∈ Sk } be any nonempty subset of size m. Using Definition 28 (average correlation) and the above
orthogonality, only the m diagonal terms contribute:

                                               1       X                                   1     1
                               ρ(D′ , D0 ) =                       χD0 (D1 , D2 ) =           ·m= .
                                               m2                                          m2    m
                                                    D1 ,D2 ∈D ′


We now compute SDAZ (Z, γ̄). Fix an integer d ≥ 1 and write
                                                           
                                                            N
                                                   m0 :=      .
                                                            d

Since ρ(D′ , D0 ) = 1/|D′ | is decreasing in |D′ |, the worst case among |D′ | ≥ N/d occurs at the smallest allowed size,
namely |D′ | = m0 . Thus the defining condition for SDAZ (Z, γ̄) is equivalent to

                                                             1
                                                                ≤ γ̄.
                                                             m0

Regime 1: γ̄ < 1/N . For every integer d ≥ 1 we have m0 = ⌈N/d⌉ ≤ N , hence 1/m0 ≥ 1/N > γ̄. So no integer d ≥ 1
is feasible and SDAZ (Z, γ̄) = 0.
Regime 2: γ̄ ≥ 1/N . We show SDAZ (Z, γ̄) = Θ(γ̄N ).
Lower bound. Let d := max{1, ⌊γ̄N/2⌋}. If d = 1, then m0 = ⌈N ⌉ = N and 1/m0 = 1/N ≤ γ̄, so d is feasible.
Otherwise d = ⌊γ̄N/2⌋ ≥ 1, so d ≤ γ̄N/2 and hence N/d ≥ 2/γ̄. Therefore
                                                     
                                                   N       2      1
                                           m0 =        ≥       ≥ ,
                                                   d      γ̄     γ̄

which implies 1/m0 ≤ γ̄. Thus d is feasible and SDAZ (Z, γ̄) ≥ Ω(γ̄N ).
Upper bound. If γ̄ ≥ 1/2, then γ̄N = Θ(N ) and trivially SDAZ (Z, γ̄) ≤ N , so SDAZ (Z, γ̄) = Θ(γ̄N ).
Assume γ̄ < 1/2 and let d > 4γ̄N . Then N/d < 1/(4γ̄) and hence
                                                    
                                                   N         1   1
                                            m0 =        ≤       < ,
                                                    d       4γ̄  γ̄

where the last inequality uses γ̄ < 1/2. Therefore 1/m0 > γ̄, so the condition fails and no such d is feasible. Thus
SDAZ (Z, γ̄) ≤ O(γ̄N ) for γ̄ < 1/2.
Combining the lower and upper bounds yields SDAZ (Z, γ̄) = Θ(γ̄N ) for γ̄ ≥ 1/N .

                                                                   27
                                             LLM Priors for ERM over Programs

Theorem C.6 (Iteration/sample lower bound for b-bit mini-batch coordinate SGD on k-parity learning). Let n ≥ 1 and
k ∈ {1, . . . , n}, and let N = nk . For each k-sparse s ∈ Sk ⊆ {0, 1}n , let Ds be the realizable distribution over X × {±1}
given by
                                       x ∼ Unif({0, 1}n ),     y = fs (x) = (−1)⟨s,x⟩ .
Consider a procedure that runs T iterations of b-bit coordinate mini-batch SGD with batch size B (Definition C.1),
and whose interaction with fresh examples (x, y) ∼ Ds is only through the quantized per-example coordinate gradients
(equivalently, through 1-STAT(b) access as in Lemma C.3). Let the procedure output a hypothesis h : {0, 1}n → {±1}.
Assume that for every s ∈ Sk the procedure achieves nontrivial population error with probability at least β ≥ 5/6, namely
                                        
                                       1
                       Pr errDs (h) ≤      ≥ β,       where      errDs (h) := Pr [h(x) ̸= y].
                                       4                                      (x,y)∼Ds

Let q := T B be the total number of fresh examples used (equivalently, the number of 1-STAT(b) queries). Then necessarily
                                                             √ 
                                                    q 2b = Ω     N ,

and hence                              √     !                                                 √      !
                                         N                                                       N
                              q=Ω                ,     and consequently                 T =Ω                .
                                        2b                                                     B 2b

Proof. Step 1: b-bit SGD is a 1-STAT(b) algorithm. By Lemma C.3, a T -iteration run with batch size B uses exactly

                                                               q := T B

calls to 1-STAT(b).
Step 2: Simulate 1-STAT(b) by VSTAT. Apply Theorem B.4 in (Feldman, 2017) with a fixed constant δ := 1/100. This
yields an algorithm A′ that succeeds with probability at least β − δ > 2/3 and uses at most

                                                           Q = O(q 2b )

queries to VSTAT(t) with
                                                               q 2b
                                                                     
                                                     t=Θ                  = Θ(q 2b ),
                                                                δ2
where the hidden constants may depend on δ but δ is fixed. In particular, by choosing δ sufficiently small as an absolute
constant, we may assume that whenever q2b ≥ 1 the corresponding parameter t satisfies t ≥ 64.
Step 3: Learning implies testing using one additional VSTAT(t) query. Define the promise testing problem Z: given
oracle access to an unknown distribution D that is either D0 (where x ∼ Unif({0, 1}n ) and y ∼ Unif({±1}) independent)
or Ds for some unknown s ∈ Sk , output PLANTED if D = Ds and NULL if D = D0 .
Fix any s ∈ Sk . Condition on the event that the learner outputs h with errDs (h) ≤ 1/4, and consider the bounded query

                                                                1 + h(x)y
                                              ϕh (x, y) :=                ∈ [0, 1].
                                                                    2
Under Ds ,
                                                                                                      3
                               E(x,y)∼Ds [ϕh (x, y)] = Pr[h(x) = y] = 1 − errDs (h) ≥                   .
                                                                                                      4
Under D0 , since y is independent uniform and h(x) ∈ {±1},
                                                                                                       1
                              E(x,y)∼D0 [h(x)y] = 0             ⇒           E(x,y)∼D0 [ϕh (x, y)] =      .
                                                                                                       2

Now make one additional VSTAT(t) query with ϕh and let v be the oracle’s response. Output PLANTED iff v ≥ 5/8,
else output NULL.

                                                                  28
                                                  LLM Priors for ERM over Programs

For the standard VSTAT(t) oracle (Feldman et al., 2018), for any [0, 1]-valued query with mean p the returned value
satisfies                                                         r
                                                           n1       p(1 − p) o
                                             |v − p| ≤ max      ,             .
                                                              t         t
Since t ≥ 64, this error is at most 1/16 both at p = 1/2 and at p = 3/4, so the threshold 5/8 separates the two cases:
                                        1   1   9   5                                         3   1   11  5
                      D = D0 : v ≤        +   =    < ,                         D = Ds : v ≥     −   =    > .
                                        2 16    16  8                                         4 16    16  8
Thus, whenever errDs (h) ≤ 1/4, this extra query yields a correct test.
Since A′ outputs such an h with probability at least 2/3 on Ds , the composed tester succeeds with probability at least 2/3
as well. It uses at most Q + 1 = O(q2b ) queries to the same oracle VSTAT(t).
Step 4: Apply the VSTAT lower bound. Apply Theorem 30 of Reyzin (2020) to the promise testing problem Z. That
theorem is parameterized by an accuracy γ̄ > 0 and assumes oracle access to VSTAT(⌈c1 /γ̄⌉) for a universal constant
c1 > 0.
Fix another universal constant c2 > 0 and set
                                                                              c2
                                                                    γ̄ :=        .
                                                                               t
Then                                                                  
                                                          c1         c1
                                                                   =    t = Θ(t).
                                                          γ̄         c2
Since the VSTAT(t) accuracy guarantee is monotone in t (larger t means smaller allowed error), any response admissible
for VSTAT(t) is also admissible for VSTAT(t′ ) for every t′ ≤ t. Therefore, by choosing the constant c2 > 0 (in the
definition γ̄ = c2 /t) sufficiently small so that          
                                                   c1     c1
                                                      =      t ≤ t,
                                                   γ̄     c2
we ensure that oracle access to VSTAT(t) suffices to instantiate Theorem 30 at accuracy γ̄ (up to constant factors in the
parameterization).
Let d := SDA(Z, γ̄). By Lemma C.4,
                                 (
                                            Θ(γ̄N ) = Θ(N/t), if γ̄N ≥ 1 (i.e. t ≤ c2 N ),
                                   d=
                                            Θ(1),             if γ̄N < 1 (i.e. t > c2 N ).

Theorem 30 implies that any algorithm that solves Z with probability at least 2/3 using only VSTAT(t) access must make
at least Ω(d) oracle queries.
We have such a tester using O(q2b ) queries. Therefore:

  • If t ≤ c2 N , then d = Θ(N/t) and hence
                                                                   q2b = Ω(N/t).
     With t = Θ(q2b ) from Step 2 this gives
                                                                                                   √     !
                               b            N                         b 2                              N
                            q2 = Ω                    =⇒           (q2 ) = Ω(N )         =⇒    q=Ω             .
                                            q2b                                                       2b

                                                                                            √
  • If t√> c2 N , then t = Θ(q2b ) implies q2b = Ω(N ), which in particular implies q2b = Ω( N ) and hence q =
    Ω( N /2b ) as well.
                                                                         √ 
                                                                                N
Finally, since q = T B, the lower bound on q implies T = Ω                    B 2b
                                                                                     .



                                                                         29
