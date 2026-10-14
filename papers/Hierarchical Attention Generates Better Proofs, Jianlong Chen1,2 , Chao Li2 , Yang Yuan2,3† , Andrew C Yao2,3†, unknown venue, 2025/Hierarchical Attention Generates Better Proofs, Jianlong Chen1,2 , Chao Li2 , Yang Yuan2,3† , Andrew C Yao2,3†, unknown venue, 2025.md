                                                                  Hierarchical Attention Generates Better Proofs

                                                                Jianlong Chen1,2 , Chao Li2 , Yang Yuan2,3† , Andrew C Yao2,3†
                                                                             1
                                                                              The Chinese University of Hong Kong, Shenzhen
                                                                         2
                                                                             Shanghai Qi Zhi Institute 3 IIIS, Tsinghua University
                                                                   {jianlongchen}@link.cuhk.edu.cn, {yuanyang,andrewcyao}@tsinghua.edu.cn




                                                                   Abstract                               et al., 2023; Wang et al., 2023a; First et al., 2023).
                                                                                                          These models excel at generating proofs and tack-
                                                 Large language models (LLMs) have shown                  ling a broad array of problems, significantly re-
                                                 promise in formal theorem proving, but their
arXiv:2504.19188v1 [cs.LG] 27 Apr 2025




                                                                                                          ducing the need for manually crafted heuristics.
                                                 token-level processing often fails to capture the
                                                                                                          However, they still struggle with key challenges
                                                 inherent hierarchical nature of mathematical
                                                 proofs. We introduce Hierarchical Attention,             in formal theorem proving, often failing to gener-
                                                 a regularization method that aligns LLMs’ at-            ate difficult proofs or producing unnecessarily long
                                                 tention mechanisms with mathematical reason-             ones.
                                                 ing structures. Our approach establishes a five-            These limitations arise because mathematics is
                                                 level hierarchy from foundational elements to            inherently formal and rigorous, whereas LLMs
                                                 high-level concepts, ensuring structured infor-          are primarily designed to process plain token se-
                                                 mation flow in proof generation. Experiments
                                                                                                          quences, without explicit formal semantics. There-
                                                 demonstrate that our method improves proof
                                                 success rates by 2.05% on miniF2F and 1.69%              fore, the structured nature of formal concepts —
                                                 on ProofNet while reducing proof complexity              where dependencies and relationships between con-
                                                 by 23.81% and 16.50% respectively. The code              cepts play a critical role — is difficult for LLMs to
                                                 is available at https://github.com/Car-pe/               fully capture. This raises a natural question:
                                                 HAGBP.
                                                                                                               How to understand structure better?
                                         1       Introduction                                                Mathematical theorem proving exhibits inherent
                                                                                                          hierarchical structures in the flow of information
                                         The intersection of AI and mathematics has
                                                                                                          between different components. While large lan-
                                         emerged as an important research direction in re-
                                                                                                          guage models have shown promising results in this
                                         cent years, particularly in the domain of formal
                                                                                                          domain, their attention mechanisms often fail to
                                         theorem proving. Proof assistants, such as Lean
                                                                                                          capture these natural hierarchies. We propose a
                                         (De Moura et al., 2015; Moura and Ullrich, 2021),
                                                                                                          novel framework that guides the model’s attention
                                         Coq (The Coq Development Team, 2024), and
                                                                                                          patterns to better align with the hierarchical na-
                                         Isabelle (Paulson, 1994), have become key plat-
                                                                                                          ture of mathematical reasoning, while maintaining
                                         forms to explore this direction. Traditionally, theo-
                                                                                                          flexibility for complex proof steps.
                                         rem provers primarily rely on search-based meth-
                                                                                                             Our key insight is that mathematical reasoning
                                         ods to systematically explore proof spaces, often
                                                                                                          follows a natural hierarchical structure, with in-
                                         guided by complex rule-based techniques or sym-
                                                                                                          formation flowing from foundational elements to
                                         bolic heuristics (Han et al., 2021; Jiang et al., 2021;
                                                                                                          higher-level concepts. As shown in Figure 1, we
                                         Polu and Sutskever, 2020; Polu et al., 2022; Lam-
                                                                                                          formalize this intuition through a five-level hierar-
                                         ple et al., 2022; Jiang et al., 2022b; Yang et al.,
                                                                                                          chy and implement it by structured attention pat-
                                         2024).
                                                                                                          terns. This hierarchical framework not only re-
                                            The advent of large language models (LLMs)
                                                                                                          spects the natural dependencies in mathematical
                                         has brought a transformative shift, leveraging their
                                                                                                          proofs but also provides flexibility in attention dis-
                                         capacity for deep contextual understanding to rea-
                                                                                                          tribution, allowing the model to capture both local
                                         son about mathematical proofs (Xin et al., 2024;
                                                                                                          and cross-level relationships necessary for complex
                                         Welleck and Saha, 2023; Zhao et al., 2023; Jiang
                                                                                                          reasoning.
                                             †
                                                 Corresponding author.                                       Based on this framework, we propose Hierar-

                                                                                                      1
Figure 1: Overview of our hierarchical attention framework. Left: The five-level hierarchy from inner (context) to
outer (goal) layer, illustrating the natural information flow in mathematical reasoning. Right: A concrete example
showing how different components in a theorem proving state are assigned to hierarchical levels, with guided and
unrestricted flow (solid arrows) representing allowed attention paths and limited flow (dashed arrows) representing
restricted attention paths.


chical Attention, a novel regularization method                 • We demonstrated substantial improvements
aimed at improving structural learning in LLMs.                   on multiple standard benchmarks in proof ac-
Our approach constructs a hierarchical tree from                  curacy and proof conciseness.
the input token sequence, assigning levels to tokens
                                                            2    Related Work
and guiding information flow based on these levels.
Specifically, we enforce the following constraints:         Formal Theorem Proving. Formal theorem prov-
                                                            ing systems are typically classified into two cate-
   • Tokens at higher levels can access information         gories: Automated Theorem Proving (ATP) and In-
     from the same level or lower levels.                   teractive Theorem Proving (ITP). ATP systems aim
   • Tokens at lower levels are restricted from ac-         to discover proofs without human intervention auto-
     cessing higher-level information.                      matically. Saturation-based provers like E (Schulz,
                                                            2002) and Vampire (Kovács and Voronkov, 2013)
   Through extensive experiments on multi-                  use resolution calculus, while specialized solvers
ple theorem-proving benchmarks—including                    like SAT and SMT solvers (e.g., MiniSat (Eén
miniF2F (Zheng et al., 2021) and ProofNet (Azer-            and Sörensson, 2003), Z3 (De Moura and Bjørner,
bayev et al., 2023)—our method demonstrates                 2008)) focus on boolean satisfiability and other
significant improvements in both proof success              mathematical theories. Domain-specific systems
rates and proof conciseness. Specifically, our              like GEX (Chou et al., 2000) handle geometric
approach achieves a 2.05% improvement in proof              problems through specialized deduction rules.
success rates while reducing the proof length                  In contrast, ITP systems like Lean (De Moura
by 23.81% in successful cases. These results                et al., 2015; Moura and Ullrich, 2021), Coq (The
highlight the advantages of preserving semantic             Coq Development Team, 2024), and Isabelle (Paul-
and hierarchical structures in theorem proving.             son, 1994) emphasize human-machine collabora-
This is further confirmed by our ablation studies           tion. These systems provide expressive proof lan-
and attention pattern analysis.                             guages and sound kernels, enabling mathemati-
   The main contributions of this work are as fol-          cians to formalize theorems and construct proofs
lows:                                                       in a manner that mirrors informal mathematical
   • We analyzed the hierarchical structure in math-        reasoning while ensuring logical correctness.
     ematical reasoning, from foundational defini-             Neural Theorem Proving. Neural Theorem
     tions to final goals.                                  Proving has risen to prominence alongside the rapid
                                                            development of LLMs and more specialized neural
   • We proposed a new algorithm for better struc-          architectures for formal reasoning. A central fo-
     ture learning for LLMs.                                cus has been autoformalization (Wang et al., 2018,

                                                        2
2020; Wu et al., 2022b; Murphy et al., 2024; Jiang          though studies have explored their use in tasks such
et al., 2022a, 2023; Lu et al., 2024; Ying et al.,          as generating math problems or document classifi-
2024a; Azerbayev et al., 2023; Liu et al., 2023; ?),        cation (Yang et al., 2016; Wu et al., 2022a), there
which converts informal mathematical statements             is a gap in leveraging attention-based methods ex-
and proofs into machine-verifiable languages de-            plicitly for mathematical reasoning.
spite the ongoing challenges in semantic alignment.
Another key area is premise selection (Irving et al.,       3     Preliminaries
2016; Kucik and Korovin, 2018; Piotrowski and               3.1    Hierarchical Structure in Lean
Urban, 2020; Ferreira and Freitas, 2020a,b; Wu,
2022; Mikuła et al., 2023; Holden and Korovin,              Lean is a strongly typed language, which allows all
2025), where models retrieve the most relevant              tokens to be naturally unfolded across multiple se-
lemmas from vast libraries to aid in proving a tar-         mantic levels. These levels align with various com-
get statement. Researchers also tackle proof-step           ponents of reasoning, with each successive level
generation (Huang et al., 2018; Yang et al., 2024;          built upon the foundations of the preceding ones.
Welleck and Saha, 2023; Sanchez-Stern et al., 2020,         The categorization of these layers can be delineated
2023; Yang and Deng, 2019; Polu and Sutskever,              as follows:
2020; Han et al., 2021; Wang et al., 2023b, 2024;
                                                            Lowest or contextual layer: Contains     back-
Lin et al., 2024; Wu et al., 2024; Rute et al., 2024;
                                                               ground information, auxiliary concepts, or
Dong and Ma, 2025; Lin et al., 2025; Wang et al.,
                                                               general knowledge relevant to the proof (T0 :
2025b,a; Zhang et al., 2025), aiming to accurately
                                                               context).
predict the next formal step or tactic, often through
auto-regressive models that learn from existing             Intermediate layers: Include pattern matching
proofs. A further challenge is proof search (Loos                and case analysis (T1 : case), type declarations
et al., 2017; Suda, 2021; Aygün et al., 2020, 2022;              and definitions (T2 : type), instance declara-
Chvalovskỳ et al., 2023; Rawson and Reger, 2019,                tions and concrete examples (T3 : instance)
2021; McKeown and Sutcliffe, 2023; Fokoue et al.,                that support the proof.
2023; Abdelaziz et al., 2022; Crouse et al., 2021;
Xin et al., 2025), where deep learning-guided algo-         Highest or goal layer: Represents the core theo-
rithms, sometimes using Monte Carlo Tree Search                 rem or proposition to be proved (T4 : goal),
or reinforcement learning, explore and prune mas-               which relies on the information introduced in
sive proof spaces, balancing correctness with com-              the lower layers.
putational efficiency.
   Hierarchical Attention Mechanisms for Math-                 These layers follow a natural partial order:
ematical Reasoning. Mathematical documents                  context ≺ case ≺ type ≺ instance ≺ goal.
typically have an implicit multilevel structure, from       Structuring mathematical reasoning within this hi-
foundational definitions to the main theorems. Pre-         erarchy yields two key benefits:
vious studies have attempted to exploit this hier-              • Proper Scoping: Contextual elements and def-
archical nature by parsing formulas or proofs into                initions are confined to their appropriate lev-
trees or graphs to better represent logical struc-                els. Intuitively, each concept is most mean-
tures (Wang et al., 2017; Peng and Ma, 2017; Pali-                ingfully analyzed in conjunction with others
wal et al., 2020; Rawson and Reger, 2020), or by                  at the same level, ensuring logical coherence
building dependency graphs over entire libraries                  and clarity.
to capture relationships between statements and
lemmas (Ferreira and Freitas, 2020b; Bauer et al.,              • Clear Semantic Flow: The reasoning pro-
2024). These approaches, while promising, often                   gresses seamlessly from foundational defini-
depend on carefully crafted rules or programmati-                 tions to the final goal, reflecting the natural
cally generated data, lacking mechanisms to ensure                and intuitive structure of mathematical argu-
that neural models respect the partial orders and                 ments.
compositional dependencies inherent in mathemat-
ical logic.                                                 3.2    Information Flow
   The attention mechanism is central to modern             We want to exploit the hierarchical structure by
Transformer-based models (Vaswani, 2017). Al-               incorporating flow control into the model. Let T be

                                                        3
the set of all tokens of the input theorem. We use                 Algorithm 1: Hierarchical Attention Imple-
ti , tj to denote individual tokens, L for the number              mentation
of transformer layers, and 1 ≤ l ≤ L for layer                      Input: Theorem text T , Model layers L
indices. For tokens ti , tj in layer l, we define:                  Output: Flow loss Lf low
    • attl (ti , tj ): attention score from ti to tj , rep-         /* Initialize hierarchical levels
      resenting how much ti will affect embedding                       */
      of tj at layer l,                                             Parse input into level sets {T0 , ..., T4 } ;
                                                                      // Using Algorithm 2
    • Mij : binary attention mask, controlling the                  ;
      information flow from ti to tj ,                              Initialize attention mask M , Lf low ← 0;
    • αl = 1 − l/L: layer-wise adaptation factor,                   for each layer l in 1 to L do
      which attenuates flow control for deeper lay-                     αl ← (1 − l/L) ;                  // Layer
      ers.                                                               adaptation factor
                                                                        for tokens ti , tj in input do
   We use level(ti ) to denote the hierarchical level                       /* Construct attention mask
of token ti , taking value from {0, 1, 2, 3, 4}, cor-                            */
responding to the five levels in our hierarchy. By                          if level(ti ) ≤ level(tj ) then
controlling attention flow based on these levels, we                             Mij ← 1 ;                // Allow
encourage the model to follow natural mathemati-                                  upward/horizontal flow
cal reasoning patterns, where higher-level concepts                          else
build upon lower-level foundations.                                              Mij ← 0 ;               // Limit
4     Approach                                                                    downward flow
                                                                            /* Compute loss contribution
To enhance the model’s comprehension of the hier-                               */
archical structure and its ability to reason in align-                      invalidf low ←
ment with it, we propose a two-step approach. First,                         attl (ti , tj ) · (1 − Mij );
we extract the flow pattern from the input by identi-                       Lf low ←
fying different hierarchical levels in mathematical                          Lf low + αl · ReLU(invalidf low );
statements. Second, we guide the model’s attention
through a specialized loss function that encourages                 Lf low ← Lf low /|T |;
the model to respect these hierarchical relationships               return Lf low ;
during training.

4.1    Extract Flow Pattern                                       reduced attention proportion, while guided flow
In mathematical reasoning, different components                   demonstrates increased dominance. This structure
of a statement naturally form a hierarchy. We iden-               ensures that semantic dependencies respect the hi-
tify five distinct levels (labeled 0 to 4): basic tokens,         erarchical nature of mathematical reasoning, with
case-specific elements, type definitions, problem                 tokens primarily attending to those at the same or
instances, and goal statements. The flow from to-                 lower levels, while limiting attention in the reverse
ken ti to token tj may follow one of three types,                 direction to maintain logical consistency.
based on their hierarchical levels:
                                                                 4.2   Algorithm Implementation
     Unrestricted if level(ti ) = level(tj )
                                                                 Based on these flow patterns, we implement a hi-
        Guided          if level(ti ) < level(tj )    (1)         erarchical attention mechanism as shown in Al-
     
     
        Limited         if level(ti ) > level(tj )                gorithm 1. The algorithm first parses the input
                                                                  into different hierarchical levels using string pattern
While sharing similar algorithmic treatment, un-                  matching to identify key mathematical components.
restricted and guided flows are distinctly catego-                It then constructs attention masks and computes a
rized due to their different functional roles. Our                flow loss that penalizes attention patterns violating
experiments 5.3 show these flows develop distinct                 hierarchical constraints.
patterns during training: unrestricted flow shows                    The flow loss Lf low penalizes attention patterns

                                                              4
that violate hierarchical constraints:                      demonstrate the robustness of our method (detailed
                                                            algorithms in Appendix A.2).
                 L
            1 X X                                              For both strategies, we define the computation
Lf low =            αl ·     ReLU(attl (ti , tj )·(1−Mij ))
           |T |                                             budget   as K × T , where T indicates the number
                l=1      i,j
                                                     (2) of expansion iterations, which is set to 100 across
where αl = (1 − L ) provides stronger regulariza- all our experiments, and K = N × S. For the best-
                     l

tion in earlier layers while allowing more flexibility      first search, N represents the number of parallel
in later layers.                                            search attempts and S denotes the number of tactics
   The final training objective combines this flow          generated per expansion. For single-pass sampling,
loss with the standard cross-entropy loss LLM :             N represents the total number of sampling attempts
                                                            per problem, while S is fixed to 1 as only one tactic
                 L = LLM + λLf low                   (3) is attempted at each expanded node. The search
                                                            process employs parallel sampling with fixed time
where λ controls the strength of hierarchical con- constraints per theorem. In the following sections,
straints. A larger λ enforces stricter adherence to         we use K to denote the product of N and S for
the hierarchy, while a smaller value allows more            simplicity.
flexible attention patterns.                                   Our method is a general-purpose fine-tuning
   In summary, our approach:                                technique that can be applied to any formal
                                                            theorem-proving system. For empirical validation,
    • Identifies natural hierarchical levels in mathe- we chose LLMSTEP (Welleck and Saha, 2023) as
      matical statements.                                   our primary baseline, which provides full access
                                                            to its model, dataset, and hyperparameters, ensur-
    • Guides attention patterns to respect hierarchi-
                                                            ing complete reproducibility of our comparative
      cal relationships.
                                                            analysis.
    • Enables flexible reasoning through layer-wise         5.2 Main Results
      adaptation.
                                                            We present a comparative analysis of our method
5 Experiments                                               against the baseline, highlighting its performance
                                                            and advancements.
In this section, we evaluate our method through
comprehensive experiments on multiple theorem- Metrics We evaluate our method using two key
proving benchmarks.                                         metrics: pass@K accuracy and proof complexity.
                                                            The pass@K metric measures the model’s ability
5.1 Experimental Setup                                      to generate a valid proof within K sampling at-
Training Data and Configuration We use Le- tempts, where K = N × S represents the total
anDojo Benchmark 4* as our training dataset. number of tactic samples considered during this
The training process involves fine-tuning a Pythia- iteration of proof search.
2.8B† (Biderman et al., 2023) model for 3 epochs.              For proof conciseness analysis, we measure the
Detailed hyperparameters and training configura-            number    of proof steps required to solve the goals.
tions are provided in Appendix A.1.                         Let Tcom be the set of theorems successfully proved
                                                            by both methods with different proof lengths. For
Evaluation Protocol We conduct comprehen- each theorem t ∈ Tcom , we define its proof com-
sive evaluations across four benchmark datasets: plexity as:
miniF2F (test/valid)‡ and ProofNet (test/valid)§ .
Our evaluation employs two complementary strate-                              C(t, m) = |pt,m |               (4)
gies: best-first search and single-pass sampling, to           where p      is the proof generated for theorem
                                                                         t,m
   *Yang, K. (2023). LeanDojo Benchmark (v1) [Data set].       t using method m, and |pt,m | denotes the number
Zenodo. https://doi.org/10.5281/zenodo.8016386                 of proof steps. We then compute the average com-
   †
     https://huggingface.co/EleutherAI/pythia-2.
8b                                                             plexity ratio:
   ‡
     https://huggingface.co/datasets/cat-searcher/
minif2f-lean4                                                                    1        X        C(t, ours)
   §
     https://huggingface.co/datasets/UDACA/                          Ravg =                                        (5)
proofnet-lean4                                                                 |Tcom |            C(t, baseline)
                                                                                         t∈Tcom


                                                           5
Figure 2: Performance comparison between our method and baseline at K = 64. Left: Pass rate comparison across
miniF2F (test/valid) and ProofNet (test/valid) datasets. Best-first search (BFS) consistently outperforms single-pass
sampling (SPS), with our method further enhancing BFS performance. Solid bars represent our method while
transparent bars represent the baseline. Right: Proof complexity ratio (Ravg ), where values below 1.0 (dashed line)
indicate more concise proofs. Our method with BFS achieves consistent complexity reductions across all datasets.


Table 1: Results on miniF2F test set with best-first               Table 3: Results on miniF2F test set with single-pass
search strategy.                                                   sampling strategy.

          PASS(%)         COMPLEXITY                                         PASS(%)         COMPLEXITY
  K                                         Ravg   Diff. (%)         K                                         Ravg   Diff. (%)
       Baseline   Ours    Baseline   Ours                                 Baseline   Ours    Baseline   Ours
  1     14.75     14.34      -         -      -       -              1      9.84     18.44      -         -      -       -
  2     18.44     17.62      -         -      -       -              2     12.30     20.90      -         -      -       -
  4     22.54     23.36      -         -      -       -              4     16.80     24.18      -         -      -       -
  8     26.23     26.23    2.00      1.86   0.93    11.67            8     19.63     25.00    1.95      1.86   0.95    51.16
  16    29.10     28.28    2.11      1.50   0.71    13.24            16    20.49     26.23    1.85      1.92   1.04    26.00
  32    29.51     31.15    1.89      1.67   0.88    12.50            32    23.36     26.64    1.83      1.78   0.97    15.38
  64    29.51     31.56    2.10      1.60   0.76    8.11             64    23.36     27.87    2.00      1.85   0.93    23.21


                                                                   Table 4: Results on miniF2F validation set with single-
Table 2: Results on miniF2F validation set with best-
                                                                   pass sampling strategy.
first search strategy.
                                                                             PASS(%)         COMPLEXITY
          PASS(%)         COMPLEXITY                                 K                                         Ravg   Diff. (%)
  K                                         Ravg   Diff. (%)              Baseline   Ours    Baseline   Ours
       Baseline   Ours    Baseline   Ours
                                                                     1      9.43     14.75      -         -      -       -
  1     12.70     13.52       -        -      -       -              2     12.30     15.16      -         -      -       -
  2     15.16     14.75       -        -      -       -              4     16.80     20.08      -         -      -       -
  4     20.49     23.77       -        -      -       -              8     18.03     21.13    2.33      1.73   0.74    37.50
  8     27.05     29.51     2.83     2.67   0.94    9.68             16    18.44     24.59    1.95      1.89   0.97    43.18
  16    31.15     33.20     2.89     1.89   0.65    13.89            32    20.08     25.41    1.92      1.92   1.00    27.66
  32    31.56     34.02     3.11     2.00   0.64    12.00            64    21.72     26.64    2.12      2.38   1.12    16.33
  64    31.56     34.02     3.11     2.00   0.64    12.68



                                                                   Overview Figure 2 presents a comprehensive
  This metric provides a direct measure of our                     evaluation of our method across miniF2F (test/-
method’s proof conciseness, where Ravg < 1 indi-                   valid) and ProofNet (test/valid) datasets at K = 64.
cates that our method generally produces shorter                   The results demonstrate that best-first search (BFS)
proofs. Note that we only consider theorems where                  is the superior search strategy across all datasets,
both methods succeed but generate proofs of                        consistently outperforming single-pass sampling
different lengths, as this provides a meaningful                   (SPS). When combined with our hierarchical at-
comparison of the proof conciseness. We also re-                   tention mechanism, BFS achieves even stronger
port Diff. (%), which indicates the percentage of                  results. For example, on the miniF2F test set, our
such theorems among all theorems that both meth-                   method improves the pass rate by 2.05% while
ods successfully prove, reflecting how often the                   reducing proof complexity by 23.81%. Similar im-
methods differ in their proof strategies.                          provements are observed on the ProofNet test set,

                                                               6
with a 1.69% increase in pass rate and a 16.50% re-        Table 5: Results on ProofNet test set with best-first
duction in proof complexity. Notably, our method           search strategy.
also significantly improves SPS performance, par-
                                                                      PASS(%)         COMPLEXITY
ticularly on the miniF2F dataset where we observe            K                                          Ravg   Diff. (%)
                                                                   Baseline   Ours    Baseline   Ours
pass rate improvements of 4.51% and 4.92% on
                                                             16     11.86     11.86      -         -      -       -
test and valid sets respectively.                            32     13.56     14.69    1.83      1.83   1.00    28.57
                                                             64     13.56     15.25    2.00      1.67   0.84    26.09
Results on miniF2F Tables 1-4 present compre-
hensive results on the miniF2F benchmark. With
best-first search, our method achieves consistent          Table 6: Results on ProofNet validation set with best-
improvements in pass rates at higher computation           first search strategy.
budgets, reaching 31.56% on test set (vs. baseline’s
                                                                      PASS(%)         COMPLEXITY
29.51%) and 34.02% on validation set (vs. base-              K                                          Ravg   Diff. (%)
                                                                   Baseline   Ours    Baseline   Ours
line’s 31.56%). The performance gain becomes
                                                             16      9.04     10.73      -         -      -       -
more pronounced as the computation budget in-                32      9.04     10.73    2.00      1.00   0.50    12.50
creases, particularly when K exceeds 16.                     64     10.17     11.86    2.00      1.00   0.50    18.75
   Single-pass sampling results also demonstrate
the effectiveness of our method, achieving 27.87%
and 26.64% pass rates on test and validation sets          our method shows consistent improvements across
respectively at K = 64, compared to baseline’s             computation budgets, achieving 14.12% at K = 64
23.36% and 21.72%. This represents substantial             compared to baseline’s 13.56%, with improve-
improvements of 4.51% and 4.92% respectively.              ments ranging from 1.70% to 2.63%. On the valida-
   For proof conciseness evaluation, we focus on           tion set, while performance is initially comparable
higher computation budget scenarios (K ≥ 8)                at K = 16 (both 7.34%), our method shows im-
where sufficient successful proofs are available           provement at higher computation budgets, reaching
for reliable complexity comparison. At K = 64,             9.04% at K = 64 compared to baseline’s 8.47%.
our method demonstrates significant advantages                For proof conciseness evaluation at K = 64,
in proof conciseness with the search strategy, re-         our method demonstrates significant advantages
ducing the average proof length from 3.11 to 2.00          across all settings. With the search strategy, the
steps (Ravg = 0.64) on the validation set and from         average proof length decreases from 2.00 to 1.67
2.10 to 1.60 steps (Ravg = 0.76) on the test set.          steps (Ravg = 0.84) on the test set and from 2.00
The reliability of these complexity metrics is sup-        to 1.00 steps (Ravg = 0.50) on the validation set,
ported by a substantial proportion of comparable           based on 26.09% and 18.75% of differing proofs
cases (Diff.), where both methods succeed but with         respectively. The single-pass sampling shows simi-
different proof lengths. For instance, at K = 64           lar improvements with Ravg = 0.75 on the test set
with best-first search, these comparable cases con-        across 21.74% of differing cases.
stitute 8.11% and 12.68% of all successful proofs
for test and validation sets respectively, providing       5.3     Visualization and Analysis of Attention
a meaningful sample size for complexity compari-                   Patterns
son. Similar reliability is observed in single-pass
                                                           The attention distribution analysis shown in Fig-
sampling, where Diff. reaches 23.21% and 16.33%,
                                                           ure 3 demonstrates that our mechanism success-
ensuring the robustness of the reported complexity
                                                           fully implements and maintains the designed infor-
improvements.
                                                           mation flow structure (Equation 1) throughout the
Results on ProofNet Tables 5-8 present the re-             model. Our analysis reveals several key findings
sults on ProofNet benchmark. With best-first               across both constrained and unconstrained layers:
search strategy, our method achieves consistent
improvements in PASS rates at higher computation           5.3.1    Implementation of Limited Flow
budgets, reaching 15.25% on test set (vs. base-                     Constraint
line’s 13.56%) and 11.86% on validation set (vs.           Our approach enforces the limited flow constraint
baseline’s 10.17%) at K = 64.                              by minimizing attention flows from higher to lower
   Single-pass sampling results also demonstrate           levels across all layers. In constrained layers (Fig-
the effectiveness of our method. On the test set,          ure 3, left), this is evidenced by the near-zero per-

                                                       7
Figure 3: Attention distribution analysis in different layers. Left: Hierarchy-constrained layers (where αl ̸= 0).
Right: Unconstrained layers (where αl = 0). This visualization is derived from averaging attention patterns across
all evaluation samples on the LeanDojo Benchmark 4 test set. The x-axis represents different hierarchical levels,
while the y-axis shows the percentage of attention scores, combining both cases where the level’s tokens serve as
source (ti ) and target (tj ). Blue and green bars represent the baseline and our method respectively, with different
transparency levels indicating different attention flow types based on the relationship between source level(ti ) and
target level(tj ).


Table 7: Results on ProofNet test set with single-pass              upward attention while restricting reverse flows to
sampling strategy.                                                  just 0.2%. Type and instance levels receive sub-
                                                                    stantial guided information flow from lower lev-
           PASS(%)         COMPLEXITY
  K                                          Ravg   Diff. (%)       els (77.7% and 71.0% respectively), demonstrating
        Baseline   Ours    Baseline   Ours
                                                                    strong hierarchical information propagation. This
  16     9.60      11.30       -        -      -        -
  32     10.17     12.80     2.00     2.00   1.00     31.25         pattern strengthens in unconstrained layers, where
  64     13.56     14.12     2.40     1.80   0.75     21.74         the goal level receives even stronger attention from
                                                                    lower levels (84.5%), and type and instance levels
Table 8: Results on ProofNet validation set with single-
                                                                    maintain robust upward attention flows (89.0% and
pass sampling strategy.                                             81.5% respectively).

           PASS(%)         COMPLEXITY                               5.3.3   Global Impact on Model Behavior
  K                                          Ravg   Diff. (%)
        Baseline   Ours    Baseline   Ours                          The consistency of hierarchical patterns between
  16      7.34     7.34       -         -      -       -            constrained and unconstrained layers is particularly
  32      8.47     7.34     1.50      1.50   1.00    18.18          significant, indicating that our method induces a
  64      8.47     9.04     1.50      1.50   1.00    30.77
                                                                    global, coherent hierarchical information process-
                                                                    ing framework. Rather than merely responding to
                                                                    external constraints, the model appears to have in-
centages of level(ti ) > level(tj ) attention across                ternalized the hierarchical structure, as evidenced
all hierarchical levels, compared to the baseline’s                 by the preservation of desired attention patterns
substantial invalid flows ranging from 5.5% to                      in unconstrained layers. This seamless continu-
27.8%. Remarkably, this pattern persists in un-                     ation of attention patterns throughout the model
constrained layers (Figure 3, right), where invalid                 architecture suggests that our hierarchical attention
flows remain minimal (ranging from 0.5% to 3.2%                     mechanism effectively shapes the model’s overall
across different levels), demonstrating the robust-                 information processing strategy, establishing a sta-
ness of our hierarchical structure.                                 ble and consistent hierarchical flow structure.
5.3.2    Effectiveness of Guided Flow Design
                                                                    6   Conclusion
Our method successfully implements and main-
tains the guided flow design throughout the model.                  We introduced Hierarchical Attention, a regular-
In constrained layers, the goal level effectively in-               ization method that aligns transformer attention
tegrates information from lower levels with 68.7%                   with mathematical reasoning structures through a

                                                                8
five-level hierarchy. Our approach balances struc-             Eser Aygün, Zafarali Ahmed, Ankit Anand, Vlad Firoiu,
tured information flow with the flexibility needed               Xavier Glorot, Laurent Orseau, Doina Precup, and
                                                                 Shibl Mourad. 2020. Learning to prove from syn-
for complex proofs through layer-wise adaptation.
                                                                 thetic theorems. arXiv preprint arXiv:2006.11259.
Experimental results show improved proof suc-
cess rates and conciseness across multiple bench-              Eser Aygün, Ankit Anand, Laurent Orseau, Xavier Glo-
                                                                 rot, Stephen M Mcaleer, Vlad Firoiu, Lei M Zhang,
marks, while attention pattern analysis confirms
                                                                 Doina Precup, and Shibl Mourad. 2022. Proving
the method’s effectiveness in helping models in-                 theorems using incremental learning and hindsight
ternalize mathematical hierarchies. The consistent               experience replay. In International Conference on
improvements demonstrate a promising direction                   Machine Learning, pages 1198–1210. PMLR.
for bridging neural language models and mathemat-              Zhangir Azerbayev, Bartosz Piotrowski, Hailey
ical reasoning.                                                  Schoelkopf, Edward W Ayers, Dragomir Radev, and
                                                                 Jeremy Avigad. 2023. Proofnet: Autoformalizing
Limitations                                                      and formally proving undergraduate-level mathemat-
                                                                 ics. arXiv preprint arXiv:2302.12433.
Our approach has three main limitations: (1) the               Andrej Bauer, Matej Petković, and Ljupco Todorovski.
hierarchy definition is specific to Lean’s seman-                2024. Mlfmf: data sets for machine learning for
tics and may require adaptation for other proof                  mathematical formalization. Advances in Neural In-
                                                                 formation Processing Systems, 36.
languages, (2) the fixed hierarchy structure may
limit dynamic reasoning patterns, and (3) data con-            Stella Biderman, Hailey Schoelkopf, Quentin Gregory
straints prevented evaluation on advanced mod-                   Anthony, Herbie Bradley, Kyle O’Brien, Eric Hal-
                                                                  lahan, Mohammad Aflah Khan, Shivanshu Purohit,
els like DeepSeek-Prover (Xin et al., 2024) and                   USVSN Sai Prashanth, Edward Raff, et al. 2023.
InternLM-Math (Ying et al., 2024b). Future work                   Pythia: A suite for analyzing large language mod-
could explore adaptive hierarchies and the cross-                 els across training and scaling. In International
domain generalization.                                           Conference on Machine Learning, pages 2397–2430.
                                                                  PMLR.
Ethical Considerations                                         Shang-Ching Chou, Xiao-Shan Gao, and Jing-Zhong
                                                                 Zhang. 2000. A deductive database approach to au-
Our work focuses on improving theorem proving                    tomated geometry theorem proving and discovering.
through Hierarchical Attention while addressing                  Journal of Automated Reasoning, 25(3):219–246.
several ethical considerations. We use publicly                Karel Chvalovskỳ, Konstantin Korovin, Jelle Piepen-
available datasets, including LeanDojo Benchmark                 brock, and Josef Urban. 2023. Guiding an instanti-
4 under the MIT license¶ , and strictly follow data              ation prover with graph neural networks. In LPAR,
                                                                 pages 112–123.
usage policies. While mathematical content is gen-
erally objective, we acknowledge potential biases              Maxwell Crouse, Ibrahim Abdelaziz, Bassem Makni,
in theorem selection and proof styles. Our method,              Spencer Whitehead, Cristina Cornelio, Pavan Kapa-
                                                                nipathi, Kavitha Srinivas, Veronika Thost, Michael
though designed for positive applications, should               Witbrock, and Achille Fokoue. 2021. A deep re-
be used with human oversight as it could poten-                 inforcement learning approach to first-order logic
tially generate misleading proofs. To promote trans-            theorem proving. In Proceedings of the AAAI Con-
parency and reproducibility, we will release our                ference on Artificial Intelligence, volume 35, pages
                                                                6279–6287.
code and models with appropriate licenses and us-
age guidelines.                                                Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:
                                                                 An efficient smt solver. In International conference
                                                                 on Tools and Algorithms for the Construction and
                                                                 Analysis of Systems, pages 337–340. Springer.
References
                                                               Leonardo De Moura, Soonho Kong, Jeremy Avigad,
Ibrahim Abdelaziz, Maxwell Crouse, Bassem Makni,                 Floris Van Doorn, and Jakob von Raumer. 2015. The
   Vernon Austel, Cristina Cornelio, Shajith Ikbal, Pa-          lean theorem prover (system description). In Auto-
   van Kapanipathi, Ndivhuwo Makondo, Kavitha Srini-             mated Deduction-CADE-25: 25th International Con-
   vas, Michael Witbrock, et al. 2022. Learning to guide         ference on Automated Deduction, Berlin, Germany,
   a saturation-based theorem prover. IEEE Transac-              August 1-7, 2015, Proceedings 25, pages 378–388.
   tions on Pattern Analysis and Machine Intelligence,           Springer.
   45(1):738–751.
                                                               Kefan Dong and Tengyu Ma. 2025. Stp: Self-play
   ¶                                                             llm theorem provers with iterative conjecturing and
    https://github.com/lean-dojo/LeanDojo/blob/
main/LICENSE                                                     proving. Preprint, arXiv:2502.00212.


                                                           9
Niklas Eén and Niklas Sörensson. 2003. An extensible             Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski,
  sat-solver. In International conference on theory and            Konrad Czechowski, Tomasz Odrzygóźdź, Piotr
  applications of satisfiability testing, pages 502–518.           Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022b. Thor:
  Springer.                                                        Wielding hammers to integrate language models and
                                                                   automated theorem provers. Advances in Neural In-
Deborah Ferreira and André Freitas. 2020a. Natu-                   formation Processing Systems, 35:8360–8373.
  ral language premise selection: Finding supporting
  statements for mathematical text. arXiv preprint               Laura Kovács and Andrei Voronkov. 2013. First-order
  arXiv:2004.14959.                                                theorem proving and vampire. In International Con-
                                                                   ference on Computer Aided Verification, pages 1–35.
Deborah Ferreira and André Freitas. 2020b. Premise                 Springer.
  selection in natural language mathematical texts. In
  Proceedings of the 58th Annual Meeting of the Asso-            Andrzej Stanisław Kucik and Konstantin Korovin. 2018.
  ciation for Computational Linguistics, pages 7365–               Premise selection with neural networks and dis-
  7374.                                                            tributed representation of features. arXiv preprint
                                                                   arXiv:1807.10268.
Emily First, Markus N Rabe, Talia Ringer, and Yuriy
  Brun. 2023. Baldur: Whole-proof generation and
  repair with large language models. In Proceedings of           Guillaume Lample, Timothee Lacroix, Marie-Anne
  the 31st ACM Joint European Software Engineering                 Lachaux, Aurelien Rodriguez, Amaury Hayat,
  Conference and Symposium on the Foundations of                   Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
  Software Engineering, pages 1229–1241.                           2022. Hypertree proof search for neural theorem
                                                                   proving. Advances in neural information processing
Achille Fokoue, Ibrahim Abdelaziz, Maxwell Crouse,                 systems, 35:26337–26349.
  Shajith Ikbal, Akihiro Kishimoto, Guilherme Lima,
  Ndivhuwo Makondo, and Radu Marinescu. 2023. An                 Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean
  ensemble approach for automated theorem proving                  Welleck. 2024.      Lean-star: Learning to in-
  based on efficient name invariant graph neural repre-            terleave thinking and proving. arXiv preprint
  sentations. arXiv preprint arXiv:2305.08676.                     arXiv:2407.10040.

Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W               Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
   Ayers, and Stanislas Polu. 2021. Proof artifact co-             Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
   training for theorem proving with language models.              Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
   arXiv preprint arXiv:2102.06203.                                2025. Goedel-prover: A frontier model for open-
                                                                   source automated theorem proving.     Preprint,
Edvard K Holden and Konstantin Korovin. 2025. Graph                arXiv:2502.07640.
  sequence learning for premise selection. Journal of
  Symbolic Computation, 128:102376.                              Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying
                                                                   Liu, Ye Yuan, Haiming Wang, Wei Ju, Chuanyang
Daniel Huang, Prafulla Dhariwal, Dawn Song, and                    Zheng, Yichun Yin, Lin Li, et al. 2023. Fimo: A chal-
  Ilya Sutskever. 2018. Gamepad: A learning en-                    lenge formal dataset for automated theorem proving.
  vironment for theorem proving. arXiv preprint                    arXiv preprint arXiv:2309.04295.
  arXiv:1806.00608.
                                                                 Sarah Loos, Geoffrey Irving, Christian Szegedy, and
Geoffrey Irving, Christian Szegedy, Alexander A Alemi,             Cezary Kaliszyk. 2017. Deep network guided proof
  Niklas Eén, François Chollet, and Josef Urban. 2016.             search. arXiv preprint arXiv:1701.06972.
  Deepmath-deep sequence models for premise selec-
  tion. Advances in neural information processing
                                                                 Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,
  systems, 29.
                                                                    Jing Xiong, Chengwu Liu, Jianhao Shen, Hui Jin,
Albert Q Jiang, Wenda Li, and Mateja Jamnik. 2023.                  Jipeng Zhang, Haiming Wang, et al. 2024. Process-
  Multilingual mathematical autoformalization. arXiv                driven autoformalization in lean 4. arXiv preprint
  preprint arXiv:2311.03755.                                        arXiv:2406.01940.

Albert Q Jiang, Sean Welleck, Jin Peng Zhou,                     Jack McKeown and Geoff Sutcliffe. 2023. Reinforce-
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-                      ment learning for guiding the e theorem prover. In
  thée Lacroix, Yuhuai Wu, and Guillaume Lample.                   The International FLAIRS Conference Proceedings,
  2022a. Draft, sketch, and prove: Guiding formal                  volume 36.
  theorem provers with informal proofs. arXiv preprint
  arXiv:2210.12283.                                              Maciej Mikuła, Szymon Tworkowski, Szymon An-
                                                                  toniak, Bartosz Piotrowski, Albert Qiaochu Jiang,
Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han,                Jin Peng Zhou, Christian Szegedy, Łukasz Kuciński,
  and Yuhuai Wu. 2021. Lisa: Language models of                   Piotr Miłoś, and Yuhuai Wu. 2023. Magnushammer:
  isabelle proofs. In 6th Conference on Artificial Intel-         A transformer-based approach to premise selection.
  ligence and Theorem Proving, pages 378–392.                     arXiv preprint arXiv:2303.04488.


                                                            10
Leonardo de Moura and Sebastian Ullrich. 2021. The                4th ACM SIGPLAN International Workshop on Ma-
  lean 4 theorem prover and programming language. In              chine Learning and Programming Languages, pages
  Automated Deduction–CADE 28: 28th International                 1–10.
  Conference on Automated Deduction, Virtual Event,
  July 12–15, 2021, Proceedings 28, pages 625–635.              Alex Sanchez-Stern, Emily First, Timothy Zhou,
  Springer.                                                       Zhanna Kaufman, Yuriy Brun, and Talia Ringer. 2023.
                                                                  Passport: Improving automated formal verification
Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu                    using identifiers. ACM Transactions on Program-
  Li, Anima Anandkumar, and Xujie Si. 2024. Aut-                  ming Languages and Systems, 45(2):1–30.
  oformalizing euclidean geometry. arXiv preprint
  arXiv:2405.17216.                                             Stephan Schulz. 2002. E–a brainiac theorem prover. Ai
                                                                   Communications, 15(2-3):111–126.
Aditya Paliwal, Sarah Loos, Markus Rabe, Kshitij
  Bansal, and Christian Szegedy. 2020. Graph repre-             Martin Suda. 2021. Improving enigma-style clause
  sentations for higher-order logic and theorem proving.         selection while learning from history. In Automated
  In Proceedings of the AAAI Conference on Artificial            Deduction–CADE 28: 28th International Conference
  Intelligence, volume 34, pages 2967–2974.                      on Automated Deduction, Virtual Event, July 12–15,
                                                                 2021, Proceedings 28, pages 543–561. Springer.
Lawrence C Paulson. 1994. Isabelle: A generic theorem
  prover. Springer.                                             The Coq Development Team. 2024. Coq. URL https:
                                                                  //coq.inria.fr.
Kebin Peng and Dianfu Ma. 2017. Tree-structure cnn
  for automated theorem proving. In Neural Infor-               A Vaswani. 2017. Attention is all you need. Advances
  mation Processing: 24th International Conference,               in Neural Information Processing Systems.
  ICONIP 2017, Guangzhou, China, November 14-18,
  2017, Proceedings, Part II 24, pages 3–12. Springer.          Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
                                                                  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
Bartosz Piotrowski and Josef Urban. 2020. State-                  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-
  ful premise selection by recurrent neural networks.             qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-
  arXiv preprint arXiv:2004.08212.                                dong Song, Chenjun Xiao, Dehao Zhang, Ebony
                                                                  Zhang, Frederick Pu, Han Zhu, Jiawei Liu, Jonas
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-             Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-
   tas Baksys, Igor Babuschkin, and Ilya Sutskever.               Schmidt, Lewis Tunstall, Luigi Pagani, Moreira
   2022. Formal mathematics statement curriculum                  Machado, Pauline Bourigault, Ran Wang, Stanislas
   learning. arXiv preprint arXiv:2202.01344.                     Polu, Thibaut Barroyer, Wen-Ding Li, Yazhe Niu,
Stanislas Polu and Ilya Sutskever. 2020. Generative               Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan
   language modeling for automated theorem proving.               Wang, Zhilin Yang, Zhengying Liu, and Jia Li. 2025a.
   arXiv preprint arXiv:2009.03393.                               Kimina-prover preview: Towards large formal rea-
                                                                  soning models with reinforcement learning. Preprint,
Michael Rawson and Giles Reger. 2019. A neurally-                 arXiv:2504.11354.
  guided, parallel theorem prover. In Frontiers of Com-
  bining Systems: 12th International Symposium, Fro-            Haiming Wang, Huajian Xin, Zhengying Liu, Wenda Li,
  CoS 2019, London, UK, September 4-6, 2019, Pro-                 Yinya Huang, Jianqiao Lu, Zhicheng Yang, Jing Tang,
  ceedings 12, pages 40–56. Springer.                             Jian Yin, Zhenguo Li, et al. 2024. Proving theorems
                                                                  recursively. arXiv preprint arXiv:2405.14414.
Michael Rawson and Giles Reger. 2020. Directed graph
  networks for logical reasoning. In PAAR+ SC2 @                Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin
  IJCAR, pages 109–119.                                           Li, Zhengying Liu, Qingxing Cao, Yinya Huang,
                                                                  Jing Xiong, Han Shi, Enze Xie, et al. 2023a. Lego-
Michael Rawson and Giles Reger. 2021. lazycop: Lazy               prover: Neural theorem proving with growing li-
  paramodulation meets neurally guided search. In                 braries. arXiv preprint arXiv:2310.00656.
  Automated Reasoning with Analytic Tableaux and
  Related Methods: 30th International Conference,               Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,
  TABLEAUX 2021, Birmingham, UK, September 6–9,                   Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun
  2021, Proceedings 30, pages 187–199. Springer.                  Li, Lin Li, et al. 2023b. Dt-solver: Automated theo-
                                                                  rem proving with dynamic-tree sampling guided by
Jason Rute, Miroslav Olšák, Lasse Blaauwbroek, Fi-                proof-level value function. In Proceedings of the
   del Ivan Schaposnik Massolo, Jelle Piepenbrock, and            61st Annual Meeting of the Association for Compu-
   Vasily Pestun. 2024. Graph2tac: learning hierar-               tational Linguistics (Volume 1: Long Papers), pages
   chical representations of math concepts in theorem             12632–12646.
   proving. arXiv preprint arXiv:2401.02949.
                                                                Mingzhe Wang, Yihe Tang, Jian Wang, and Jia Deng.
Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul,                2017. Premise selection for theorem proving by deep
  and Sorin Lerner. 2020. Generating correctness                  graph embedding. Advances in neural information
  proofs with neural networks. In Proceedings of the              processing systems, 30.


                                                           11
Qingxiang Wang, Chad Brown, Cezary Kaliszyk, and                  language models. Advances in Neural Information
  Josef Urban. 2020. Exploration of neural machine                Processing Systems, 36.
  translation in autoformalization of mathematics in
  mizar. In Proceedings of the 9th ACM SIGPLAN                  Zichao Yang, Diyi Yang, Chris Dyer, Xiaodong He,
  International Conference on Certified Programs and              Alex Smola, and Eduard Hovy. 2016. Hierarchical at-
  Proofs, pages 85–98.                                            tention networks for document classification. In Pro-
                                                                  ceedings of the 2016 conference of the North Ameri-
Qingxiang Wang, Cezary Kaliszyk, and Josef Urban.                 can chapter of the association for computational lin-
  2018. First experiments with neural translation of              guistics: human language technologies, pages 1480–
  informal to formal mathematics. In Intelligent Com-             1489.
  puter Mathematics: 11th International Conference,
  CICM 2018, Hagenberg, Austria, August 13-17, 2018,            Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang,
  Proceedings 11, pages 255–270. Springer.                        Dahua Lin, and Kai Chen. 2024a. Lean work-
                                                                  book: A large-scale lean problem set formalized
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang, Yizhen               from natural language math problems. arXiv preprint
  Jia, Shizhe Diao, Renjie Pi, Junjie Hu, and Tong                arXiv:2406.03847.
  Zhang. 2025b. Ma-lot: Multi-agent lean-based long
  chain-of-thought reasoning enhances formal theorem            Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou,
  proving. Preprint, arXiv:2503.03205.                            Yunfan Shao, Zhaoye Fei, Yichuan Ma, Jiawei Hong,
                                                                  Kuikun Liu, Ziyi Wang, Yudong Wang, Zijian Wu,
Sean Welleck and Rahul Saha. 2023. Llmstep: Llm                   Shuaibin Li, Fengzhe Zhou, Hongwei Liu, Songyang
  proofstep suggestions in lean. arXiv preprint                   Zhang, Wenwei Zhang, Hang Yan, Xipeng Qiu, Jiayu
  arXiv:2310.18457.                                               Wang, Kai Chen, and Dahua Lin. 2024b. Internlm-
                                                                  math: Open math large language models toward veri-
Qinzhuo Wu, Qi Zhang, and Xuanjing Huang. 2022a.                  fiable reasoning. Preprint, arXiv:2402.06332.
  Automatic math word problem generation with topic-
  expression co-attention mechanism and reinforce-              Jingyuan Zhang, Qi Wang, Xingguang Ji, Yahui Liu,
  ment learning. IEEE/ACM Transactions on Audio,                   Yang Yue, Fuzheng Zhang, Di Zhang, Guorui
  Speech, and Language Processing, 30:1061–1072.                   Zhou, and Kun Gai. 2025. Leanabell-prover: Post-
                                                                   training scaling in formal reasoning. Preprint,
Yuhuai Wu. 2022. Formal premise selection with lan-                arXiv:2504.06122.
  guage models. In Conference on Artificial Intelli-
  gence and Theorem Proving (AITP), volume 4.                   Xueliang Zhao, Wenda Li, and Lingpeng Kong. 2023.
                                                                  Decomposing the enigma: Subgoal-based demon-
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus                 stration learning for formal theorem proving. arXiv
  Rabe, Charles Staats, Mateja Jamnik, and Christian              preprint arXiv:2305.16366.
  Szegedy. 2022b. Autoformalization with large lan-
  guage models. Advances in Neural Information Pro-             Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  cessing Systems, 35:32353–32368.                                2021. Minif2f: a cross-system benchmark for for-
                                                                  mal olympiad-level mathematics. arXiv preprint
Zijian Wu, Jiayu Wang, Dahua Lin, and Kai Chen.                   arXiv:2109.00110.
   2024. Lean-github: Compiling github lean repos-
   itories for a versatile lean prover. arXiv preprint
   arXiv:2407.17227.

Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  Xiaodan Liang. 2024. Deepseek-prover: Advancing
  theorem proving in llms through large-scale synthetic
  data. arXiv preprint arXiv:2405.14333.

Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Kai Shen.
  2025. Bfs-prover: Scalable best-first tree search
  for llm-based automatic theorem proving. Preprint,
  arXiv:2502.03438.

Kaiyu Yang and Jia Deng. 2019. Learning to prove
  theorems via interacting with proof assistants. In In-
  ternational Conference on Machine Learning, pages
  6984–6994. PMLR.

Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Prenger, and Animashree Anandkumar. 2024. Le-
  andojo: Theorem proving with retrieval-augmented


                                                           12
A         Appendix                                              tactics, and creates new states by applying valid
                                                                tactics. The search succeeds when reaching a state
A.1         Training Details
                                                                with no remaining goals within N expansions.
We use Pythia-2.8B|| as our base model. The train-
ing data is sourced from LeanDojo Benchmark 4                   Single-Pass Sampling runs K parallel proof at-
** , which consists of 169,530 samples for training             tempts. Each attempt samples tactics sequentially
and 3,606 samples for validation.                               until finding a valid one or reaching the attempt
    We train the model for 3 epochs on 8 NVIDIA                 limit. A proof succeeds if it completes within N
A800 GPUs using DeepSpeed†† with ZeRO-3 opti-                   valid tactics. This approach simplifies the search
mization, taking approximately 40 hours. The train-             process by setting S = 1 and focusing on trajectory
ing uses a per-device batch size of 2 with gradient             sampling rather than state ranking.
accumulation steps of 2, resulting in an effective
batch size of 32. We adopt a learning rate of 1e-5              A.3     Ablation Studies
with a cosine decay schedule and 3% warmup ratio.
The training process employs FP16 precision with-               A.3.1    Layer-wise Adaptation Mechanism
out weight decay, and ZeRO-3 is configured with                 To validate the effectiveness of our layer-wise adap-
parameter and optimizer state partitioning across               tation mechanism (αl = 1 − l/L), we conduct abla-
GPUs. For reproducibility, we set the random seed               tion studies on miniF2F and ProofNet benchmarks
to 42 across all experiments.                                   using best-first search with K = 64. The results
    During training, we evaluate the model every                are shown in Table 10.
500 steps and save checkpoints at the same fre-
quency, maintaining the 3 most recent checkpoints.              Table 10: Ablation study results on miniF2F and
The best model is selected based on validation per-             ProofNet benchmarks with best-first search (K = 64).
formance at the end of training. The training objec-                                             miniF2F         ProofNet
tive combines the standard cross-entropy loss with                 Method
                                                                                               Test    Valid   Test    Valid
our hierarchical flow loss. Table 9 shows the spe-
                                                                   PASS (baseline)             29.51   31.56   13.56   10.17
cific hyperparameters (λ and L) used for different                 PASS (w/o adaptation)       30.74   32.34   14.69   11.30
evaluation sets.                                                   PASS (w/ adaptation)        31.56   34.02   15.25   11.86
                                                                   Ravg (w/o adaptation)       0.53    0.82    0.69     0.50
Table 9: Hyperparameters for different evaluation sets.            Ravg (w/ adaptation)        0.76    0.64    0.84     0.50
                                                                   Diff.(w/o adaptation) (%)   9.86    11.27   22.73   18.75
                    Dataset            λ     L                     Diff.(w/ adaptation) (%)    8.11    12.68   26.09   18.75
                    miniF2F (test)     0.1   4
                    miniF2F (valid)    0.1   16
                    ProofNet (test)    0.2   16
                                                                   The results demonstrate an interesting trade-off
                    ProofNet (valid)   0.2   4
                                                                in our layer-wise adaptation mechanism. Without
                                                                adaptation, where hierarchical constraints are ap-
                                                                plied uniformly across layers, the model achieves
A.2         Evaluation algorithm                                better proof complexity ratios across three bench-
We implement two evaluation algorithms for theo-                marks but lower pass rates. This suggests that grad-
rem proving: best-first search and single-pass sam-             ually reducing the constraint strength in deeper lay-
pling. Both algorithms share the same computation               ers through layer-wise adaptation (αl = 1 − l/L)
budget K × T , where T = 100 is the maximum                     helps achieve better proof success rates at the cost
expansion steps.                                                of slightly longer proofs. The superior pass rates
                                                                across all benchmarks validate that our adaptive
Best-First Search maintains a priority
                                                                approach effectively enhances the model’s theorem
queue
Pi−1 of states ranked by trajectory score                       proving capabilities while maintaining reasonable
   j=0 log p(aj |sj ). For each expansion, it selects           proof complexity. Notably, even without layer-wise
the highest-scoring state si , generates S candidate
                                                                adaptation, our hierarchical attention mechanism
     ||
          https://huggingface.co/EleutherAI/pythia-2.           still outperforms the baseline substantially in both
8b                                                              pass rates and proof complexity, demonstrating the
  **Yang, K. (2023). LeanDojo Benchmark (v1) [Data set].

Zenodo. https://doi.org/10.5281/zenodo.8016386                  effectiveness of our basic hierarchical structure de-
  ††
     https://github.com/microsoft/DeepSpeed                     sign.

                                                           13
A.3.2 Hierarchical Structure Variants                                       <instance>...</instance>...
To explore the impact of different hierarchical struc-                      <goal>...</goal>...",
tures, we conducted ablation experiments compar-                     }
ing the fine-grained structure (with all five levels                   Table 12 shows the results with best-first search
T0 −T4 ) against a coarse-grained variant where lev-                 (K = 64). The explicit tags approach significantly
els T1 − T3 are merged into a single level. Table 11
shows the results with best-first search (K = 64).                   Table 12: Comparison between baseline, explicit tags
On the miniF2F benchmark, the coarse-grained                         approach, and our method with best-first search (K =
                                                                     64).
Table 11: Comparison of hierarchical structure variants
on miniF2F and ProofNet benchmarks.                                                                     miniF2F         ProofNet
                                                                           Method
                                                                                                      Test    Valid   Test    Valid
                                  miniF2F         ProofNet
    Method                                                                 PASS (baseline)            29.51   31.56   13.56   10.17
                                Test    Valid   Test    Valid              PASS (explicit tags)       21.88   16.80    9.04    7.34
    PASS (baseline)             29.51   31.56   13.56   10.17              PASS (ours)                31.56   34.02   15.25   11.86
    PASS (coarse-grained)       30.33   32.38   14.12   11.30              Ravg (explicit tags)        2.01    1.78    1.30    2.00
    PASS (fine-grained)         31.56   34.02   15.25   11.86              Ravg (ours)                0.76    0.64    0.84     0.50
    Ravg (coarse-grained)       0.67    0.82    0.73     1.26              Diff.(explicit tags) (%)   24.44   17.50   40.00   18.18
    Ravg (fine-grained)         0.76    0.64    0.84     0.50              Diff.(ours) (%)            8.11    12.68   26.09   18.75
    Diff.(coarse-grained) (%)   8.33    11.43   26.32   21.43
    Diff.(fine-grained) (%)     8.11    12.68   26.09   18.75
                                                                     underperformed both the baseline and our method
                                                                     across all datasets. These results indicate that sim-
variant achieves better proof complexity ratios
                                                                     ply annotating data with explicit level tags is in-
(Ravg ) on the test set (0.67 vs 0.76), while the fine-
                                                                     effective and potentially detrimental for theorem
grained structure achieves better complexity on the
                                                                     proving.
validation set (0.64 vs 0.82). More importantly,
the fine-grained approach delivers superior pass                     A.5      Input Parsing Algorithm
rates across both test and validation sets. Similar
patterns are observed in the ProofNet benchmark.                     To implement our hierarchical structure, we de-
These results demonstrate that distinguishing be-                    veloped a rule-based parsing algorithm that iden-
tween different reasoning elements (case analysis,                   tifies different structural components in theorem
type declarations, and instances) is beneficial for                  text, as shown in Algorithm 2. This lightweight
overall theorem-proving performance, with mixed                      pattern-matching approach identifies key mathe-
effects on proof complexity. The fine-grained struc-                 matical components through syntactic indicators:
ture provides the model with more detailed infor-                    goal statements (containing turnstile ⊢), case anal-
mation about the relationships between different                     ysis statements (starting with "case"), type declara-
elements in the proof state, enabling more accurate                  tions (containing "Type" and colon), and instance
reasoning and higher success rates.                                  definitions (containing colon but neither "Type"
                                                                     nor turnstile). The parser maintains context across
A.4     Explicit Level Tags Baseline                                 multi-line statements by inheriting the level of pre-
To further evaluate the effectiveness of different                   vious lines when appropriate, ensuring accurate
structural representation methods, we implemented                    hierarchical structure capture with minimal compu-
a baseline that uses explicit level tags. This experi-               tational overhead.
ment was designed to compare two fundamentally
different approaches to representing structure: di-                  A.6      Case Studies
rectly adding explicit tags in the input data versus                 To demonstrate the effectiveness of our hierarchical
implicitly guiding hierarchical information flow                     attention mechanism in generating concise proofs,
through attention mechanisms. In this baseline, we                   we present three representative examples from
modified the input format to include explicit tags                   different mathematical domains in the miniF2F
indicating the hierarchical level of each component:                 dataset.
{                                                                       These examples showcase how our hierarchical
      Input: "<context>...</context>...                              attention mechanism improves proof generation
      <type>...</type>...                                            across different mathematical domains. In Table 13,

                                                                14
                                                             Lean4 Statement
 Algorithm 2: Hierarchical Structure Pars-
 ing                                                         theorem mathd_algebra_148 (c : Real) (f : Real -> Real)
                                                               (h0 : ∀ x, f x = c * x^3 - 9 * x + 3)
  Input: Theorem text
                                                               (h1 : f 2 = 9) : c = 3
  Output: Hierarchical level information
  Initialize empty segments list;                            Baseline Proof

  /* Initialize context level             */                 rw [h0] at h1    -- Substitute f(2) with its definition
                                                             linarith      -- Solve the resulting equation c * 8 - 18 + 3 = 9
  Add context tokens to segments with level
   context;                                                  Our Proof
  Extract Lean4 code block between context;
                                                             linarith only [h0 2, h1] -- Directly solve using h0 applied to 2 and h1
  current ← context;
  /* Process text line by line                */
  for each line in Lean4 code do                               Table 13: Case Study 1: Basic Algebra Problem
      /* Determine hierarchical level
                                                             Lean4 Statement
           */
      if line contains ⊢ then                                theorem mathd_numbertheory_185 (n : Nat)
           current ← goal;                                     (h0 : n % 5 = 3) : 2 * n % 5 = 1

      else if line starts with case then                     Baseline Proof
           current ← case;
      else if line contains Type and : then                  rw [two_mul]           -- Convert 2 * n to n + n
                                                             rw [Nat.add_mod, h0] -- Apply modular addition: (3 + 3) % 5 = 1
           current ← type;
      else if line contains : but not Type or ⊢              Our Proof
        then
                                                             rw [Nat.mul_mod, h0] -- Apply modular multiplication: 2 * 3 % 5 = 1
           current ← instance;
      else
           Maintain current for continued                     Table 14: Case Study 2: Number Theory Problem
            lines;
      Record segment with position and level;                Lean4 Statement
  return Hierarchical level information;
                                                             theorem amc12a_2016_p3 (f : Real -> Real -> Real)
                                                               (h0 : ∀ x, ∀ (y) (_ : y != 0),
                                                                     f x y = x - y * Int.floor (x / y)) :
                                                               f (3/8) (-(2/5)) = -(1/40)

                                                             Baseline Proof

                                                             simp [h0]                   -- Expand function definition
                                                             field_simp [two_ne_zero]    -- Simplify rational expressions
                                                             norm_cast                   -- Convert between types

                                                             Our Proof

                                                             field_simp [h0]   -- Combine function expansion and field simplification
                                                             norm_cast           -- Convert between types
our model directly combines the function defini-
tion with the given value, eliminating the need for
intermediate expansion. Table 14 demonstrates                Table 15: Case Study 3: Advanced Algebra Problem
improved pattern recognition, where our model
directly applies the appropriate modular multipli-
cation rule instead of decomposing the operation
into addition. Table 15 shows enhanced tactic un-
derstanding, combining function expansion with
field simplification in a single step. The consistent
reduction in proof steps across these diverse exam-
ples demonstrates how our hierarchical attention
mechanism enables better mathematical reasoning.

                                                        15
