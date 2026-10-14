                                                        Benchmarking Testing in Automated Theorem Proving

                                                               Jongyoon Kim1 * Hojae Han2* Seung-won Hwang1†
                                                  Interdisciplinary Program in Artificial Intelligence, Seoul National University1
                                                              Electronics and Telecommunications Research Institute2
                                                                  {john.jongyoon.kim,seungwonh}@snu.ac.kr
                                                                            {hojae.han}@etri.re.kr



                                                               Abstract                                            Prove commutativity of addition
arXiv:2604.23698v1 [cs.CL] 26 Apr 2026




                                             Recent advances in large language models                theorem commutativity … :      theorem commutativity … :
                                                                                                       a + b = a + b := by            a + b = b + a := by
                                             (LLMs) have shown promise in formal theo-                 simpa using add_comm a b       simpa using add_comm a b
                                             rem proving, yet evaluating semantic correct-
                                             ness remains challenging. Existing evaluations                              (a) Compilation
                                             rely on indirect proxies such as lexical over-                     theorem cancel_eq … :
                                                                                                                  a + b = c + a→b = c := by
                                             lap with human-annotated proof, or expensive                         intro h
                                             manual inspection. Inspired by the shift from                        have h' : a + b = a + c := by
                                                                                                                    simpa [commutativity c a] …
                                             lexical comparison to test-based evaluation in
                                             code generation, we propose T2 , a framework
                                             that evaluates the semantic correctness of for-                           (b) Testing Accuracy
                                             mal theorems: a generated theorem is consid-
                                             ered correct only if all dependent successor          Figure 1: Two candidate theorems for proving commu-
                                             theorems compile successfully, analogous to           tativity of addition: one correct (a ` b “ b ` a) and
                                             integration testing. We construct a benchmark         one tautology (a ` b “ a ` b). (a) Under compilation-
                                             from 5 real-world Lean 4 repositories, compris-       based evaluation, both candidates pass, as each is logi-
                                             ing 2,206 problems paired with 41 successor           cally valid in isolation. (b) Under testing-based evalu-
                                             theorems on average, automatically extracted          ation, the tautology is exposed: the successor theorem
                                             without human effort. Experiments demon-              (cancel_eq) fails when it depends on the incorrect can-
                                             strate that while state-of-the-art models achieve     didate, while it compiles successfully with the correct
                                             high compilation success, they perform signif-        one.
                                             icantly worse under our semantic metric. The
                                             best model, Claude-Sonnet-4.5, achieves only
                                             38.9% Testing Accuracy on the full set, given         can generate valid formal proofs spanning high
                                             both natural language proof and successor the-        school olympiad- to undergraduate-level mathe-
                                             orems as context, revealing a critical gap in         matics (Zheng et al., 2022; Azerbayev et al., 2023;
                                             current theorem generation capabilities.1             Yu et al., 2025), where correctness is verified by
                                                                                                   checking whether the generated theorem compiles,
                                         1   Introduction                                          confirming its syntactic and logical validity.
                                         With the rapid advancement of Large Language                 However, compilation alone does not guarantee
                                         Models (LLMs), there has been growing interest            semantic correctness. As illustrated in Figure 1-(a),
                                         in applying these models to Automated Theorem             an NL specification may ask to prove commutativ-
                                         Proving (ATP), where Natural Language (NL) prob-          ity (a ` b “ b ` a), while the generated theorem
                                         lems are formalized as theorems in proof assis-           is a tautology (a ` b “ a ` b). As this tautology
                                         tants such as Lean, with approaches ranging from          compiles, which only verifies its logical validity,
                                         fine-tuned provers (Wang et al., 2025a; Xin et al.,       the intended meaning may be lost.
                                         2024) to in-context learning agents (Thakur et al.,          Existing benchmarks have recognized this limi-
                                         2024; Kumarappan et al., 2025; Varambally et al.,         tation and proposed various proxy metrics to assess
                                         2026). Recent benchmarks demonstrate that LLMs            semantic correctness, as summarized in Table 1.
                                                                                                   These approaches evaluate the generated theorem
                                         *  Both authors contributed equally to this research.
                                         †                                                         by comparing with a ground-truth proof reference,
                                            Corresponding Author
                                         1
                                           Implementation and dataset are available at: https://   using BLEU (Zheng et al., 2022), or equivalence
                                           github.com/ldilab/T2.                                   checking using linguistic entailment such as natu-
 Benchmark                           Eval. Method Annot.-Free Semantic   and a proof of the target theorem.
 MiniF2F (Zheng et al., 2022)         —               ✗          ✗          Across experiments with 18 open and closed-
 FormalMATH (Yu et al., 2025)         —               ✗          ✗
 PutnamBench (Tsoukalas et al., 2024) —               ✗          ✗       source models, we observe a substantial gap be-
 MiniF2F-v2 (Ospanov et al., 2025)    Human           ✗          ✓       tween compilation and testing accuracy: models
 ProofNet (Azerbayev et al., 2023)    Lexical         ✓          ✗
 Lean-Workbook (Ying et al., 2025)    Lexical         ✓          ✗       that appear successful under traditional measures
 Con-NF (Liu et al., 2025)            Prover          ✓          ✗
 ProofNetVerif (Poiroux et al., 2025) Prover          ✓          ✗       often fail semantically. Our key findings are:
 T2 (Ours)                           Testing          ✓          ✓           • High false positive rate of existing metrics:
                                                                               Up to 93.1% of compilable theorems are se-
Table 1: Comparison of semantic correctness evaluation                         mantically incorrect, and BLEU fails to distin-
across formal theorem benchmarks. All benchmarks
                                                                               guish correct from incorrect outputs.
verify logical validity via compilation. Annot.-Free:
operates without human annotation or evaluation. Se-                         • Overfits to compilation: Specialized prov-
mantic: directly verifies semantic correctness.                                ing models overfit to syntax and score lower
                                                                               on semantic correctness than similarly sized
                                                                               general-purpose models.
ral language inference (Ying et al., 2025), or using
a compiler built-in prover such as BEq (Liu et al.,                          • Dependency structure enables 1k+ test
2025). Alternatively, humans may investigate the                               cases: TA becomes more discriminative as
generated theorem without any reference annota-                                successor coverage grows, with the majority
tion (Ospanov et al., 2025; Tsoukalas et al., 2024;                            of problems verified at depth 7 and an aver-
Yu et al., 2025). Desirably, this evaluation should                            age of 1.6k successor theorems per problem
be automatic, requiring neither human evaluation                               at that depth.
nor reference annotation, while directly verifying                           • Successor context improves generation: Pro-
semantic correctness.                                                          viding successor theorems as context consis-
    Towards this goal, we take inspiration from in-                            tently improves semantic correctness, while
tegrated testing in software engineering, where a                              NL proofs alone do not.
component’s correctness is verified, not in isola-
tion, but by executing the modules that depend                           2    Related Work
on it. Drawing on the Curry-Howard correspon-                            Formal Theorem Proving Benchmarks Recent
dence (Curry, 1934), where proofs correspond to                          benchmarks have driven progress in neural auto-
programs, we observe that a successor theorem that                       mated theorem proving. MiniF2F (Zheng et al.,
uses a generated lemma is analogous to a mod-                            2022), ProofNet (Azerbayev et al., 2023), and Put-
ule that calls a function. That is, if the lemma is                      namBench (Tsoukalas et al., 2024) evaluate mod-
semantically incorrect, the successor theorem can-                       els on high school Olympiad- to undergraduate-
not be correct. Based on this insight, we propose                        level problems, while Lean-Workbook (Ying et al.,
evaluating a generated theorem by whether its suc-                       2025) and FormalMATH (Yu et al., 2025) provide
cessor theorems, those that invoke or build upon                         large-scale training corpora. However, as summa-
it, compile successfully, as illustrated in Figure 1-                    rized in Table 1, these benchmarks primarily verify
(b). This approach is fully automatic, requires no                       logical validity via compilation, leaving semantic
external references, and directly verifies semantic                      correctness either unaddressed or assessed through
correctness through successor compilation.                               unreliable proxies such as BLEU, natural-language-
   Building on this idea, we introduce Testing                           inference-based back-translation, or prover-based
Accuracy (TA), the first testing-based metric                            equivalence checking, all of which require ground-
for semantic evaluation of formal theorems, and                          truth references or external models and provide
Theorem Testing (T2 ), a large-scale Lean bench-                         only indirect estimates of semantic correctness.
mark designed to evaluate the generated theorem                          Manual inspection (Ospanov et al., 2025) offers
by testing it with successor theorems. T2 com-                           a reliable evaluation but lacks scalability. More-
prises 2,206 theorems curated from real-world                            over, since these benchmarks consist of isolated,
Lean repositories, each paired with successor theo-                      self-contained problems, they are far removed from
rems that serve as integration test cases. We further                    real-world mathematical proof development, where
identify a Hard subset of 389 problems that requires                     theorems are deeply interconnected through depen-
the model to generate both an auxiliary proposition                      dency structures.
Test-Based Evaluation in Code Generation In                  -- Predecessors Tpred
                                                             -- Predecessor Theorems : required to state tGT
code generation, test-based evaluation is standard           def InfiniteAdeleRing := ( v : InfinitePlace K ) -y v .
practice. Benchmarks such as APPS (Hendrycks                 ...
                                                                  completion

et al., 2021), HumanEval (Chen et al., 2021), and
                                                             -- Target tGT
MBPP (Austin et al., 2021) evaluate generated                -- Replaced by the generated tfl during evaluation
code by executing it against test cases rather than          @ [ simp ] theorem algebraMap_apply ( x : K ) :
                                                                   algebraMap K (InfiniteAdeleRing K ) x v = x := rfl
comparing it lexically to a reference solution. This
                                                             -- Successors Tsucc
paradigm directly measures functional correctness            -- Successor Theorems test suite : depend on tGT
                                                             theorem mixedEmbedding_eq_algebraMap_comp { x : K } :
and is both automatic and reference-free. Despite                mixedEmbedding K x = ringEquiv_mixedSpace K (
the well-established connection between proofs                     algebraMap K (InfiniteAdeleRing K ) x ) := by
                                                               ext v x ; y simp only [ ringEquiv_mixedSpace_apply ,
and programs via the Curry-Howard correspon-                      algebraMap_apply, ...]
                                                               ...
dence (Curry, 1934), test-based evaluation has not
been applied to formal theorem generation before             theorem ringEquiv_mixedSpace_apply ( x : InfiniteAdeleRing K
                                                                  ) :
our work.                                                        ringEquiv_mixedSpace K x = ... := rfl


                                                                                 (a) Lean source code
3     Testing-Based Semantic Evaluation
Evaluating semantic correctness, whether a gener-                        Tpred     InfiniteAdeleRing            ...

ated theorem captures the intended logical meaning
of an NL theorem, is a central challenge in formal
                                                                                      tGT     algebraMap. . .
theorem generation.
   Given an NL theorem tnl , the task is to gener-
ate a formal theorem tfl “ psfl , pfl q comprising a
statement sfl and a proof pfl , such that tfl is both log-             Tsucc     mixedEmbedding. . .   ringEquiv. . .
ically valid and semantically faithful to tnl . Com-
pilation verifies logical validity (sfl $ pfl ), but
not semantic correctness (sfl $ pfl ^ tfl ” Jtnl K).                                    ...                 ...
Proving strict logical equivalence (tfl ” tGT ) is
generally intractable for complex theories, and it                               (b) Dependency graph
is hard to find the ground-truth of the target theo-         Figure 2: An example problem of T2 . The tar-
rem tGT . Existing proxies that rely on surface-level        get tGT (algebraMap_apply) has predecessors
similarity or approximate entailment fail to capture         Tpred , (e.g. definition of InfiniteAdeleRing),
the intended mathematical semantics, as stated in            and successors Tsucc that invoke it (e.g.
Section 2.                                                   mixedEmbedding_eq_algebraMap_comp).
   To address this, we adopt an observational ap-
proach: rather than proving equivalence directly,
we verify whether tfl behaves equivalently to tGT
in all observed contexts.
                                                             ing to the generated candidate theorem tfl . We
3.1    Integration Testing for Formal Theorems               denote the theorems tGT depends on as prede-
                                                                                    p1q        pmq
In software engineering, a function may be com-              cessors Tpred “ ttpred , . . . , tpred u, and the theo-
piled yet fail to meet its specification. To catch such      rems that transitively depend on tGT as succes-
                                                                                 p1q        pnq
failures, integration testing validates that a compo-        sors Tsucc “ ttsucc , . . . , tsucc u, which serve as
nent, when combined with its dependents, produces            the test cases. Figure 2a shows a concrete Lean
correct behavior (Ammann and Offutt, 2017). If a             source view of these three types of theorem, where
modified component causes dependent modules to               InfiniteAdeleRing serves as a predecessor, alge-
fail, it signals a semantic violation.                       braMap_apply is the target, and mixedEmbed-
   We adopt this principle for formal theorems               ding_eq_algebraMap_comp is one of the succes-
by viewing each theorem as a node in a depen-                sors that invokes the target. Figure 2b gives the
dency graph (Prasad et al., 2024; Cabral et al.,             corresponding dependency view, where predeces-
2026) rather than in isolation. Let tGT be the               sors flow into tGT , and successors flow out of it. We
ground-truth of the target theorem correspond-               consider tfl semantically correct if substituting it
                                                                                    piq                  piq
for tGT 2 leaves every theorem in Tsucc compilable.            where compilesptsucc | tfl q “ 1 if tsucc success-
                                                               fully compiles when tGT is replaced by tfl , and 0
3.2      Cut Elimination as Theorem Testing                    otherwise.
We ground this intuition formally in the Curry-                   To ensure meaningful coverage, we restrict our
Howard correspondence, which identifies proofs as              benchmark to theorems with |Tsucc | ě 2 (see Sec-
programs and logical rules as computational opera-             tion 4). The resulting problems have dependency
tions. Specifically, we identify integration testing           depth up to 7 and an average of 1.6k successor
with the logical principle of Cut Elimination.                 theorems, so each evaluation involves multiple se-
   The Cut Rule in sequent calculus formalizes the             mantic constraints.
composition of proofs. For instance, proving X Ñ
W by chaining intermediate theorems Y and Z,                   4     Benchmark Construction
given a shared set of background assumption Γ,
corresponds to integration testing across multiple             4.1    Extraction Pipeline
modules:
                                                               We employ a fully automated, dependency-aware
     Γ$XÑY             Γ$Y ÑZ Γ$ZÑW                            extraction pipeline targeting public Lean 4 reposi-
                                    (1)
                       Γ$XÑW                                   tories.

where X Ñ Y corresponds to tfl , and the remain-               Dependency Graph Construction We parse the
ing chain represents Tsucc . In proof theory, the              Lean environment to build a global dependency
use of a lemma introduces a cut, and cut elimi-                graph G “ pV, Eq, where V is the set of theorems
nation removes the auxiliary lemma to produce a                and lemmas and E represents usage relationships
direct proof, which computationally corresponds                between them, with Lean-Dojo (Yang et al., 2023).
to a function call. By the cut elimination theorem,
if tfl is semantically correct, this chain of cuts can         Target Selection. From G, we select target theo-
be eliminated, yielding a valid proof of X Ñ W .               rems tGT that satisfy two criteria: (1) non-triviality:
In other words, since X Ñ W holds via the chain                the depth, which is the distance from the target the-
X Ñ Y Ñ Z Ñ W , if tfl breaks the compilation                  orem to the successor theorems, is greater than 1
of Tsucc , then we treat tfl as semantically incorrect.        in G, excluding standalone theorems that existing
Successful compilation across the chain provides               benchmarks predominantly target, and (2) succes-
evidence of semantic correctness, though not a log-            sor coverage: |Tsucc | ě 2, ensuring that each target
ical guarantee. Crucially, this process is not limited         admits multiple semantic constraints for meaning-
to immediate callers, so it can recursively verify tfl         ful evaluation, reducing the possibility of false pos-
across the entire chain of dependent proofs.                   itives.
3.3      Testing Accuracy                                      Context Extraction For each target tGT , we ex-
We apply the above principle to define our metric,             tract the predecessor theorems Tpred , consisting of
TA. Let D be the distribution of problems in the               the definitions and lemmas necessary to state and
benchmark. For a problem P “ ptnl , Tpred , Tsucc q P          prove tGT , and the successor theorems Tsucc , com-
D, let tfl be the generated theorem. Here, Tpred cor-          prising all theorems that transitively depend on tGT .
responds to Γ in Equation (1), namely the prede-
cessor theorems used by both tfl and Tsucc . Each              4.2    Natural Language Annotation
                        piq
successor theorem tsucc imposes a semantic con-                Since real-world repositories typically lack natu-
straint on tfl . As the number and depth of these              ral language descriptions, we generate tnl for each
constraints increase, their conjunction increasingly           target using a strong LLM (Claude Sonnet 4.5).
approximates a guarantee of semantic correctness.              This allows us to construct a problem instance
We define TA as the expectation over problems:                                           piq      piq
                                                               Pi “ ptnl , Tpred ptGT , tsucc q, tsucc q for each target
                                                                                                        piq
                                                               tGT and each successor theorem tsucc P Tsucc ptGT q.
                   «                             ff
                     ľk
                                    piq
      TA “ E              compilesptsucc | tfl q    (2)        To validate annotation quality, we manually ver-
                P „D
                        i“1                                    ified 10 randomly sampled NL annotations and
2
    As a theorem with a different name will fail compilation   found no errors. Full details are provided in Ap-
    easily, we condition the theorem name in the context.      pendix C.
4.3    Dataset Statistics                                   5.3    Evaluation Environment
We first examined whether existing benchmarks               Our benchmark comprises two categories of prob-
could support testing-based evaluation. However,            lems with different verification requirements: T2
few problems in these benchmarks satisfy our non-           (including the T2 Hard subset). T2 is drawn from
triviality and successor coverage criteria, yielding        real-world Lean repositories that rely on project-
only 12 problems from evaluation benchmarks and             specific dependencies and varying Lean versions.
110 from training benchmarks (see Table 6).                 For these problems, we execute lake build
   We therefore extract from 5 high-quality Lean 4          within each repository’s native environment to
repositories listed on the Lean community page3 .           strictly adhere to its original configuration and
The resulting benchmark comprises 2,206 prob-               enable full dependency checking. For the supple-
lems with an average of 41 successor theorems per           mentary existing benchmarks (e.g., FormalMath,
target, providing a rigorous testbed for semantic           CombiBench), which consist of single theorem
correctness evaluation. To further challenge model          problems without successor theorems, we use
capabilities, we construct T2 Hard, a subset of 389         kimina-lean-server (Santos et al., 2025) to ver-
problems whose target declarations have a body of           ify compilation within a standardized Lean 4.25.0
type Prop, requiring generation of both the propo-          environment. Details are provided in Appendix B.
sition and its proof.
                                                            6     Results
5     Experiment Setup
                                                            We evaluate state-of-the-art LLMs on the T2 bench-
5.1    Models                                               mark. We first present model performance and key
We evaluate 18 models spanning general-purpose              results in Section 6.1. We then analyze the effect of
and domain-specialized systems, as summarized in            few-shot prompting and iterative refinement with
Table 5. All models are evaluated in a zero-shot set-       compiler feedback in Section 6.2, compare TA
ting with temperature 0.6 and top_p 0.95. Prompts           against existing metrics in Section 6.3, and study
are provided in Appendix K.                                 the impact of successor theorem coverage in Sec-
                                                            tion 6.4.
5.2    Metrics
Our primary metric is TA: the generated theorem             6.1    Overview of Results
tfl replaces the original theorem tGT in the reposi-        Table 2 presents compilation accuracy and TA
tory, and we recompile the entire dependency chain          across T2 and T2 Hard subsets, under the de-
as a test suite. The generated theorem passes the           fault setting (providing both NL proof and succes-
test if and only if all successor theorems compile          sor theorem). The best model (Claude-Sonnet-4.5)
successfully. TA is the only metric that directly           achieves 80.3% compilation accuracy on the Full
evaluates semantic correctness, and all main results        set while achieving only 38.9% TA. Scaling model
are reported using it.                                      size yields modest improvements within model
    To contextualize our findings and demonstrate           families (e.g., Llama-3.1 improves from 24.8% at
the limitations of existing evaluation methods, we          8B to 33.2% at 405B), but overall TA remains be-
additionally report two baseline metrics. Compila-          low 40% (Full) and 6% (Hard), indicating that the
tion accuracy verifies that the generated theorem           semantic gap is far from closed. We additionally
compiles in isolation, corresponding to the stan-           evaluate on existing benchmarks, where the gap be-
dard pass criterion in existing ATP benchmarks.4            tween compilation and TA is substantially smaller
BLEU measures lexical similarity to the ground-             due to the limited number of successor theorems.
truth via n-gram overlap. We analyze the gap be-            Full results are provided in Appendix H.
tween Compilation Accuracy and TA to quantify                  We further investigate the impact of input con-
how much compilation overestimates semantic cor-            text on TA. Table 3 presents the full ablation on the
rectness, and examine whether BLEU can serve as             T2 dataset. We find that both NL proofs and suc-
a reliable proxy for TA, in Section 6.3.                    cessor theorems must be provided together to yield
3
  https://leanprover-community.github.io/papers.            consistent improvements, that is, neither alone of-
  html                                                      fers meaningful benefit. For instance, Claude-4.5-
4
  For repository-sourced problems, we append #exit after
  the generated theorem to prevent the Lean compiler from   Sonnet improves by 4.9% when given both NL
  compiling successor theorems.                             proofs and successor theorems, yet providing suc-
                                     T2            T2 Hard                                          NL ✓             NL ✗
           Model               Compile     TA    Compile   TA               Model               ST ✗     ST ✓    ST ✗          ST ✓
                       Closed-Source LLMs                                               Closed-Source LLMs
  Claude-3.7-Sonnet              75.1     36.8    34.3     2.6     Claude-3.7-Sonnet            29.4     36.8     29.8         32.4
  Claude-4-Sonnet                81.1     36.0    47.5     4.5     Claude-4-Sonnet              27.7     36.0     30.0         32.3
  Claude-Sonnet-4.5              80.3     38.9    46.0     4.5     Claude-Sonnet-4.5            33.0     38.9     34.0         32.9
  GPT-4o-mini                    59.1     36.7    12.2     1.5     GPT-4o-mini                  33.8     36.7     26.2         26.7
  GPT-5                          85.7     37.7    68.3     3.4     GPT-5                        36.9     37.7     29.1         28.7
  GPT-5-mini                     86.0     37.9    66.6     4.1     GPT-5-mini                   35.2     37.9     29.6         30.9
  GPT-5-nano                     88.7     36.6    75.6     1.5     GPT-5-nano                   33.4     36.6     30.8         31.1
                        Open-Source LLMs                                                 Open-Source LLMs
  DeepSeek-R1                    70.5     36.3    25.1     4.1     DeepSeek-R1                  31.0     36.3     28.9         29.1
  GPT-OSS-120B                   68.2     32.3    40.0     4.5     GPT-OSS-120B                 26.7     32.3     28.1         27.4
  Llama-3.1-405B                 63.4     33.2    27.8     2.6     Llama-3.1-405B               30.8     33.2     29.7         30.8
  Llama-3.1-70B                  65.4     37.0    20.1     2.4     Llama-3.1-70B                28.9     37.0     28.5         29.1
  Llama-3.1-8B                   36.9     24.8     6.4     1.3     Llama-3.1-8B                 22.6     24.8     21.6         21.8
                      Math Specialized Models                                          Math Specialized Models
  DeepSeek-Prover-v2-7B          62.2     30.0    35.5     3.2     DeepSeek-Prover-v2-7B        32.0     30.0     28.2         26.1
  Goedel-Formalizer-v2-8B        38.7     23.6    22.1     2.4     Goedel-Formalizer-v2-8B      23.3     23.6     24.3         23.6
  Goedel-Prover-v2-32B           74.6     31.0    54.6     3.2     Goedel-Prover-v2-32B         30.6     31.0     29.4         31.3
  Goedel-Prover-v2-8B            46.1     24.5    37.9     2.6     Goedel-Prover-v2-8B          25.4     24.5     24.7         24.2
  Kimina-Autoformalizer-7B       21.9     20.0     4.3     1.5     Kimina-Autoformalizer-7B     20.2     20.0     20.0         19.9
  Kimina-Prover-Distill-8B       28.0     23.4    5.1      1.7     Kimina-Prover-Distill-8B     21.3     23.4     20.7         22.2


Table 2: Compilation accuracy and TA (%) on T2 and               Table 3: Impact of input context on TA (%) on T2 full
T2 Hard.                                                         dataset. We compare two axes: whether an NL proof is
                                                                 provided (✓) and whether a successor theorem (ST) is
                                                                 provided (✓) or withheld (✗).
cessor theorems alone without NL proofs actually
decreases TA. This suggests that the successor the-                Model                  Zero-shot TA (%)       2-shot TA (%)
orem helps the model understand the required se-                   Claude-4-Sonnet                4.5                    4.3
mantic constraints, while NL proofs provide the                    Claude-3.7-Sonnet              2.6                    2.8
necessary reasoning context to satisfy them. The                   GPT-5                          3.4                    2.6
ablation results on T2 Hard subset are provided in                 GPT-5-mini                     4.1                    2.8
Appendix F.
                                                                       Table 4: Zero-shot vs. 2-shot TA on T2 Hard.
6.2   Extended Experiments: Few-shot and
      Iterative Refinement
                                                                 for. The harder part is producing a formalization
To test whether other prompting strategies can im-               that matches the natural-language annotation in
prove semantic correctness, we evaluate 2-shot                   meaning, which a few examples cannot teach.
prompting and iterative refinement on the T2 Hard
subset.                                                          Iterative refinement We also evaluate
                                                                 Hilbert (Varambally et al., 2026), a method
Few-shot prompting We test whether the low                       that takes feedback from the Lean compiler
performance on T2 Hard comes from the models                     and uses it to refine the generated theorems
struggling to understand the task format, or from                over multiple rounds. Even with this feedback
a gap in their ability to solve it. We evaluate the              loop, Hilbert reaches 5.0% TA on T2 Hard,
four top-performing models with 2-shot prompting.                compared to 3.2% from the zero-shot baseline
We sample two examples from the Herald (Gao                      (DeepSeek-Prover-v2-7B). The gain is small and
et al., 2025) training set that Claude Sonnet 4.5                does not reduce the semantic gap.
solves, and prepend them as in-context examples.
Table 4 compares TA between the zero-shot and 2-                 6.3    Comparison with Existing Metrics
shot settings. We see no consistent gain across the              Compilation rate As shown in Table 2, there
four models, and in some cases, the performance                  is a significant divergence between compilation
drops. This shows that the difficulty of T2 does                 success and semantic correctness across all mod-
not come from understanding what the task asks                   els. The precision of compilation as a predictor of
                                                                                Open Source                                                                                           0.7
                                                                                Closed Source                                                                                         0.6
                                 50                                             Prover/Formalizer                       102




                                                                                                                                                                   Testing Accuracy
                                                                                Reference (y=x)                                                                                       0.5
              Relative TA (%)




                                                                                                          Count (Log)
                                                                                                                                                                                      0.4
                                  0                                                                                                                                                   0.3
                                                                                                                        101                                                           0.2
                                50                                                                                                                                                    0.1
                                                                                                                                                                                      0.0
                                                                                                                              3        4       5       6       7                            2      4         6        8
                                100                                                                                               Number of Successor Theorems                                  Number of Successor
                                                                                                                                           per Depth                                                Theorems
                                          100           50         0                 50
                                                       Relative Compile (%)                                              (a) Depth distribution                                (b) TA by number of STs

                                                                                                          Figure 5: (a) Distribution of successor theorem (ST)
Figure 3: Relative performance drop from existing                                                         depth in T2 Hard. Most problems (380) reach depth 7,
benchmarks to T2 Hard, in compilation accuracy (x-                                                        with 1,600 STs on average at that depth. (b) TA drops
axis) vs. TA (y-axis). Prover/Formalizer models (red                                                      sharply as STs grow, indicating that broader coverage
stars) in the lower-right quadrant, where compilation                                                     yields stricter evaluation.
gains do not translate to TA improvements.

                                                        Incorrect          Correct
             100%
                                                              12.8% 8.8% 10.0% 6.1%                       6.4                 Analysis of Successor Theorem Coverage
                                31.9%           28.7% 29.9%                                       26.1%
             80%                                                                          35.4%
                                        45.2%

             60%                                                                                          We further examine how successor theorem cov-
Proportion




                                                              87.2% 91.2% 90.0% 93.9%                     erage affects evaluation strictness. As shown in
             40%                                71.3% 70.1%                                       73.9%
                                68.1%                                                     64.6%           Figure 5a, the majority of problems in our bench-
                                        54.8%
             20%                                                                                          mark have a dependency depth of 7, ensuring deep
                                                                               Correlation: 0.123
              0%                                                                                          semantic verification by default. Figure 5b shows
                                 0-10 10-20 20-30 30-40 40-50 50-60 60-70 70-80 80-90 90-100
                                                       BLEU Score Bin                                     that TA decreases sharply as the number of succes-
                                                                                                          sor theorems increases: with only 2 successor the-
Figure 4: Proportion of testing-verified (green) and                                                      orems, Claude-4-Sonnet achieves approximately
testing-failed (red) samples across BLEU score bins,                                                      70% TA, dropping to near 0% when 5 or more must
aggregated over all models. High BLEU scores do not
                                                                                                          be satisfied. This confirms that each additional suc-
guarantee semantic correctness.
                                                                                                          cessor theorem imposes a meaningful semantic con-
                                                                                                          straint, and that our benchmark’s rich dependency
semantic correctness is only 6.89%. For instance,                                                         structures provide a rigorous evaluation setting.
GPT-5 achieves 68.3% compilation accuracy but
only 3.4% TA. This disparity persists regardless of
model scale or specialization, confirming that com-                                                       7               Conclusion
pilation metrics fail to capture semantic correctness.
Notably, as shown in Figure 3, specialized prov-
                                                                                                          We introduced TA, the first testing-based metric
ing models report compilation gains over general-
                                                                                                          for evaluating semantic correctness in automated
purpose models, but these gains do not translate to
                                                                                                          theorem proving, and T2 , a large-scale Lean bench-
TA improvements, suggesting that domain-specific
                                                                                                          mark of 2,206 theorems with rich dependency struc-
fine-tuning improves syntactic fluency without im-
                                                                                                          tures. Our experiments across 18 models reveal
proving semantic correctness.
                                                                                                          that compilation-based evaluation fundamentally
Lexical metric We find that lexical similarity is                                                         overestimates model capability, with up to 2ˆ gap
an unreliable proxy for semantic correctness. As                                                          between compilation and TA on the full set and
shown in Figure 4, even in the highest BLEU score                                                         up to 50ˆ on the hard set. We further showed that
bins (90-100), over 70% of samples are semanti-                                                           lexical metrics such as BLEU cannot reliably dis-
cally incorrect. Conversely, the lowest bins (0-10)                                                       tinguish semantically correct theorems from incor-
still contain approximately 30% verified correct                                                          rect ones, and that providing successor theorems
samples. This demonstrates that high BLEU scores                                                          as generation context consistently improves seman-
do not guarantee semantic correctness, nor do low                                                         tic correctness. These findings demonstrate that
scores, confirming that lexical metrics cannot be                                                         testing-based evaluation is essential for trustworthy
utilized for semantic correctness.                                                                        assessment of formal theorem generation.
8   Limitations                                         Jacob Austin, Augustus Odena, Maxwell I. Nye,
                                                           Maarten Bosma, Henryk Michalewski, David Dohan,
The reliability of TA increases with the number            Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V. Le,
and diversity of successor theorems, as each im-           and Charles Sutton. 2021. Program synthesis with
poses an additional semantic constraint. However,          large language models. CoRR, abs/2108.07732.
for problems with few successor theorems, cover-        Zhangir Azerbayev, Bartosz Piotrowski, Hailey
age may be insufficient to catch all semantic errors,     Schoelkopf, Edward W. Ayers, Dragomir Radev,
and even with many dependents, full completeness          and Jeremy Avigad. 2023. Proofnet: Autoformal-
cannot be guaranteed, analogous to the inherent           izing and formally proving undergraduate-level
                                                          mathematics. Preprint, arXiv:2302.12433.
limitation of software testing. TA is inherently in-
applicable to standalone theorems without depen-        Rafael Medeiros Cabral, Tuan Manh Do, Yu Xuejun,
dents, such as the most recently added theorems           Wai Ming Tai, Zijin Feng, and SHEN XIN. 2026.
at the frontier of a repository that no other proof       Proofflow: A dependency graph approach to faithful
                                                          proof autoformalization. In The Fourteenth Interna-
yet builds upon. Both our metric and benchmark
                                                          tional Conference on Learning Representations.
are implemented exclusively for Lean 4. Moreover,
T2 is constructed from 5 Lean 4 repositories cover-     Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
ing primarily research-level mathematics. The NL         Henrique Ponde de Oliveira Pinto, Jared Kaplan,
specifications tnl are generated by a strong LLM         Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
                                                         Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
rather than written by the original authors. While       Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
this enables scalable annotation, it may introduce       Mishkin, Brooke Chan, Scott Gray, and 39 others.
noise that affects the autoformalization setting.        2021. Evaluating large language models trained on
                                                         code. Preprint, arXiv:2107.03374.
Acknowledgments
                                                        H. B. Curry. 1934. Functionality in combinatory logic.
This work was supported by Electronics and                Proceedings of the National Academy of Sciences of
Telecommunications Research Institute (ETRI)              the United States of America, 20(11):584–590.
grant funded by ICT R&D program of MSIT/IITP            Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao,
(2022-0-00995, Automated reliable source code             Zihan Qin, Tianyi Xu, and Bin Dong. 2025. Her-
generation from natural language descriptions),           ald: A natural language annotated lean 4 dataset. In
the National Research Foundation of Korea(NRF)            The Thirteenth International Conference on Learning
                                                          Representations.
grant funded by the Korea government(MSIT) (No.
RS-2024-00414981), and Institute of Information         Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
& communications Technology Planning & Eval-              Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle,
uation (IITP) grant funded by the Korea govern-           Aiesha Letman, Akhil Mathur, Alan Schelten, Alex
                                                          Vaughan, and 1 others. 2024. The llama 3 herd of
ment(MSIT) [NO.RS-2021-II211343, Artificial In-           models. arXiv preprint arXiv:2407.21783.
telligence Graduate School Program (Seoul Na-
tional University)].                                    Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,
                                                          Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong
                                                          Ma, Peiyi Wang, Xiao Bi, and 1 others. 2025.
References                                                Deepseek-r1: Incentivizing reasoning capability in
                                                          llms via reinforcement learning. arXiv preprint
Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Alt-          arXiv:2501.12948.
  man, Andy Applebaum, Edwin Arbus, Rahul K
  Arora, Yu Bai, Bowen Baker, Haiming Bao, and 1        Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-
  others. 2025. gpt-oss-120b & gpt-oss-20b model          tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
  card. arXiv preprint arXiv:2508.10925.                  Samir Puranik, Horace He, Dawn Song, and Jacob
                                                          Steinhardt. 2021. Measuring coding challenge com-
Paul Ammann and Jeff Offutt. 2017. Introduction to        petence with APPS. In Proceedings of the Neural
  software testing. Cambridge University Press.           Information Processing Systems Track on Datasets
AI Anthropic. 2024. The claude 3 model family: Opus,      and Benchmarks 1, NeurIPS Datasets and Bench-
  sonnet, haiku. Claude-3 Model Card, 1(1):4.             marks 2021, December 2021, virtual.

AI Anthropic. 2025a. Claude 3.7 sonnet system card.     Adarsh Kumarappan, Mo Tiwari, Peiyang Song,
  Claude 3.7 Sonnet Model Card.                           Robert Joseph George, Chaowei Xiao, and Anima
                                                          Anandkumar. 2025. Leanagent: Lifelong learning for
AI Anthropic. 2025b. System card: Claude sonnet 4.5.      formal theorem proving. In The Thirteenth Interna-
  Claude Sonnet 4.5 Model Card.                           tional Conference on Learning Representations.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-       Sumanth Varambally, Thomas Voice, Yanchao Sun,
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,            Zhifeng Chen, Rose Yu, and Ke Ye. 2026. Hilbert:
  Jiawei Ge, Jingruo Sun, and 1 others. 2025. Goedel-      Recursively building formal proofs with informal rea-
  prover-v2: Scaling formal theorem proving with scaf-     soning. In The Fourteenth International Conference
  folded data synthesis and self-correction. arXiv         on Learning Representations.
  preprint arXiv:2508.03613.
                                                         Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao, and         Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Junchi Yan. 2025. Rethinking and improving aut-          Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-
  oformalization: Towards a faithful metric and a de-      qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-
  pendency retrieval-based approach. In International      dong Song, Chenjun Xiao, Dehao Zhang, Ebony
  Conference on Learning Representations.                  Zhang, Frederick Pu, Han Zhu, and 21 others. 2025a.
                                                           Kimina-prover preview: Towards large formal rea-
OpenAI. 2024. GPT-4o mini: Advancing Cost-Efficient        soning models with reinforcement learning. Preprint,
  Intelligence.                                            arXiv:2504.11354.

                                                         Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
Azim Ospanov, Farzan Farnia, and Roozbeh Youse-            Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  fzadeh. 2025. minif2f-lean revisited: Reviewing lim-     Marina Vinyes, Zhenzhe Ying, Zekai Zhu, and 1 oth-
  itations and charting a path forward. In Advances in     ers. 2025b. Kimina-prover preview: Towards large
  Neural Information Processing Systems (NeurIPS),         formal reasoning models with reinforcement learning.
  volume 39.                                               arXiv preprint arXiv:2504.11354.
Auguste Poiroux, Gail Weiss, Viktor Kunčak, and An-     Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,
  toine Bosselut. 2025. Reliable evaluation and bench-     Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and
  marks for statement autoformalization. In Proceed-       Xiaodan Liang. 2024. Deepseek-prover: Advancing
  ings of the 2025 Conference on Empirical Methods in      theorem proving in llms through large-scale synthetic
  Natural Language Processing. Association for Com-        data. Preprint, arXiv:2405.14333.
  putational Linguistics.
                                                         Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
Vishesh Prasad, Brian Kim, and Nickvash Kani. 2024.        mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  Mathematical derivation graphs: A relation extrac-       Prenger, and Anima Anandkumar. 2023. LeanDojo:
  tion task in stem manuscripts. arXiv preprint            Theorem proving with retrieval-augmented language
  arXiv:2410.21324.                                        models. In Neural Information Processing Systems
                                                           (NeurIPS).
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
                                                         Huaiyuan Ying, Zijian Wu, Yihan Geng, Zheng Yuan,
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
                                                           Dahua Lin, and Kai Chen. 2025. Lean work-
  Fu, Qihao Zhu, Dejian Yang, and 1 others. 2025.
                                                           book: A large-scale lean problem set formalized
  Deepseek-prover-v2: Advancing formal mathemati-
                                                           from natural language math problems. Preprint,
  cal reasoning via reinforcement learning for subgoal
                                                           arXiv:2406.03847.
  decomposition. arXiv preprint arXiv:2504.21801.
                                                         Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li,
Marco Dos Santos, Haiming Wang, Hugues de Saxcé,           Zhongyuan Peng, Minghao Liu, Yifan Zhang, Zheng
 Ran Wang, Mantas Baksys, Mert Unsal, Junqi Liu,           Yuan, Huajian Xin, Wenhao Huang, Yandong Wen,
 Zhengying Liu, and Jia Li. 2025. Kimina lean server:      Ge Zhang, and Weiyang Liu. 2025. Formalmath:
 Technical report. Preprint, arXiv:2504.21230.             Benchmarking formal mathematical reasoning of
                                                           large language models.
Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart,
  Adi Ganesh, Ahmed El-Kishky, Aidan McLaughlin,         Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  Aiden Low, AJ Ostrow, Akhila Ananthram, and 1 oth-       2022. Minif2f: a cross-system benchmark for for-
  ers. 2025. Openai gpt-5 system card. arXiv preprint      mal olympiad-level mathematics. In International
  arXiv:2601.03267.                                        Conference on Learning Representations.

Amitayush Thakur, George Tsoukalas, Yeming Wen,
 Jimmy Xin, and Swarat Chaudhuri. 2024. An in-
 context learning agent for formal theorem-proving.
 In First Conference on Language Modeling.

George Tsoukalas, Jasper Lee, John Jennings, Jimmy
  Xin, Michelle Ding, Michael Jennings, Amitayush
  Thakur, and Swarat Chaudhuri. 2024. Putnambench:
  Evaluating neural theorem-provers on the putnam
  mathematical competition. In Advances in Neural In-
  formation Processing Systems (NeurIPS), volume 38.
A      Model Details                                                    theorems are checked against the correct dependen-
                                                                        cies and definitions.
    Family                                   Models
                                                                        C    NL Annotation Validation
                                             Claude-3.7-Sonnet
    Claude (Anthropic, 2025a, 2024, 2025b)   Claude-4-Sonnet
                                             Claude-Sonnet-4.5          To validate the quality of LLM-generated NL anno-
                                             GPT-4o-mini
                                                                        tations, we randomly sampled 10 annotations from
    GPT (OpenAI, 2024; Singh et al., 2025)
                                             GPT-5                      T2 and manually verified them against the corre-
                                             GPT-5-Mini
                                             GPT-5-Nano                 sponding formal theorems. Each annotation was
    GPT-OSS (Agarwal et al., 2025)           GPT-OSS-120B
                                                                        checked for (1) mathematical accuracy of the de-
                                             Llama-3.1-8B
                                                                        scribed statement, (2) completeness of hypotheses
    Llama (Grattafiori et al., 2024)         Llama-3.1-70B              and conclusions, and (3) absence of hallucinated or
                                             Llama-3.1-405B
                                                                        missing conditions. All 10 annotations were judged
    DeepSeek (Guo et al., 2025)              DeepSeek-R1
                                                                        correct, as summarized in Table 8.
    DeepSeek-Prover (Ren et al., 2025)       DeepSeek-Prover-v2-7B      For a qualitative example, consider the following
                                             Goedel-Prover-v2-8B        annotation:
    Goedel-Prover (Lin et al., 2025)         Goedel-Prover-v2-32B
                                             Goedel-formalizer-v2-8B
                                                                            Formal Theorem
                                             Kimina-Autoformalizer-7B
    Kimina (Wang et al., 2025b)
                                             Kimina-Prover-Distill-8B
                                                                            theorem EmptyShapeIn . rfl {S : Set
      Table 5: Models evaluated in our experiments.                             Point } :
                                                                                EmptyShapeIn S S := by
                                                                              intro _ h
                                                                              simp at h
   We evaluate 18 models across 8 model families,
as listed in Table 5. Closed-source models are ac-
cessed via Snowflake AI Cortex API. Parameter                               Generated NL Annotation
counts for these models are not publicly disclosed,
except for GPT-OSS-120B. Open-source models                                 For any set of points S, the set S carves out
are served locally using vLLM. The Llama-3.1 fam-                           an empty shape in itself. That is, the convex
ily (8B, 70B, 405B) and DeepSeek-R1 are general-                            hull of S contains no points from S other
purpose models, while DeepSeek-Prover-v2-7B,                                than those already in S.
Goedel-Prover-v2 (8B, 32B), Goedel-formalizer-
v2-8B, Kimina-Autoformalizer-7B, and Kimina-                            This NL description contains some redundancy (no
Prover-Distill-8B are fine-tuned on formal mathe-                       points from S other than those already in S), but
matical corpora for theorem proving or autoformal-                      it correctly captures the semantics of the formal
ization tasks. All models are evaluated in a zero-                      statement. Such minor stylistic issues do not affect
shot setting with temperature 0.6 and top_p 0.95.                       the autoformalization task, as the logical content is
For each problem, we generate a single completion                       faithfully conveyed.
and evaluate it against the successor theorems as
a test suite. Closed-source model evaluations were                      D    Evaluation Environment Details
conducted between January and February 2026.
                                                                        All experiments are conducted on a server equipped
B      Dataset Details                                                  with 2 NVIDIA A6000 or 1 NVIDIA 6000Pro
                                                                        GPUs, having 49 GB and 98 GB VRAM, re-
We constructed our T2 benchmark by mining high-                         spectively. Open-source models are served using
quality, real-world Lean 4 repositories. Table 7 lists                  vLLM with bfloat16 precision. For models exceed-
the source projects included in our dataset, covering                   ing single-GPU memory (e.g., Llama-3.1-405B,
a diverse range of mathematical domains such as al-                     DeepSeek-R1), we use tensor parallelism across 2
gebra, topology, and number theory. This diversity                      GPUs for NVIDIA A6000.
is crucial for evaluating the generalization capabili-                    For T2 problems, we execute lake build within
ties of autoformalization models beyond standard                        each repository’s native environment. We set a time-
educational problems. For evaluation, we employ                         out of 600 seconds per problem for both theorem
a rigorous environment setup using lake build                           generation and compilation verification. For Stan-
within each repository to ensure that all generated                     dalone benchmarks like supplementary existing
                                                  Overall Statistics
                                                  Test (Avg.)    Prompt (Avg.)   Solution (Avg.)
                    Benchmark            # Task
                                                       #                Char.           Char.
                    Existing Benchmarks
                    Kimina (train)       5            2.00             1208.00        48.00
                    Numina (train)      105           6.53             1185.65       114.01
                    combibench (eval)    6            2.67             1229.83        70.33
                    formalmath (eval)    6           13.00             217.00         66.17
                    Total / Avg.          122         6.48             1141.10       106.80
                    T2
                    Directed-Topology     438        19.68             5489.52       172.28
                    Untangle              133        16.71             2413.51       727.90
                    WhitneyGraustein        4         2.00              177.75        22.00
                    adele-ring             67        4.52              3548.19       270.45
                    math2001              1564       50.12             1056.79        54.53
                    Total / Avg.          2206       40.59             2092.78       125.00
                    T2 (Hard)
                    Directed-Topology      6          3.00             5360.17        42.00
                    adele-ring            17          2.53             3239.24       337.76
                    math2001              366         6.97             1476.30        45.97
                    Total / Avg.          389         6.71             1613.25       58.66

Table 6: Dataset statistics for T2 benchmark, including the number of tasks, average successor theorems (Test), and
average prompt/solution lengths in characters. Untangle and WhitneyGraustein are absent in Hard set as they have
no problem matches Hard set criteria.

     Repository          Github Link                                              Lean Version       Difficulty
     adele-ring          smmercuri/adele-ring_locally-compact/tree/journal         v4.10.0-rc2       Research
     Directed-Topology   Dominique-Lawson/Directed-Topology-Lean-4                  v4.6.0-rc1       Research
     Untangle            dignissimus/Untangle                                         v4.6.1         Research
     math2001            hrmacbeth/math2001                                           v4.3.0       Undergraduate
     WhitneyGraustein    MetalCreator666/WhitneyGraustein                            v4.10.0         Research

                               Table 7: Details of the Source Repositories used in T2


benchmarks, we use kimina-lean-server within                 successor theorem is provided as context.
a standardized Lean 4.25.0 environment with a                   On T2 Hard (Table 10), providing successor the-
timeout of 120 seconds.                                      orems yields consistent improvements for most
                                                             models. GPT-OSS-120B achieves the highest TA
E    Computation Cost                                        of 5.1% in the NL ✗, ST ✓setting. Notably, NL
Table 9 summarizes the approximate computation               proofs show mixed or negligible effects: for sev-
cost of our experiments.                                     eral models (e.g., Claude-4-Sonnet, GPT-5-mini),
                                                             adding NL proofs without a successor theorem does
   The dominant cost is closed-source API calls, as
                                                             not improve or even decreases TA compared to the
each of the 389 Hard problems (and 2,206 full prob-
                                                             baseline (NL ✗, successor theorem ✗), while adding
lems) requires a separate generation call per model
                                                             a successor theorem consistently helps regardless
across 4 context settings. Compilation verification
                                                             of whether NL is provided.
is comparatively inexpensive, as lake build runs
on a CPU.
                                                             G    Compilation vs. Testing Accuracy
F   Ablation Study: Input Context
                                                             Figure 6 visualizes the divergence between com-
Table 10 presents the full ablation results on the T2        pilation accuracy and TA on the T2 Hard subset.
Hard subsets, varying whether a NL proof and/or              While compilation rates vary widely across models
                     Theorem Name                                      Repository    Verification
                     isUniformizer_ne_zero                             adele-ring      Correct
                     extensionEmbedding_of_comp_coe                    adele-ring      Correct
                     isometry_extensionEmbedding_of_comp               adele-ring      Correct
                     algebraMap_injective                              adele-ring      Correct
                     eq_pow_uniformizer_mul_unit                       adele-ring      Correct
                     not_isUnit_iff_valuation_lt_one                   adele-ring      Correct
                     bijective_extensionEmbedding_of_isReal            adele-ring      Correct
                     outputEnd                                         Untangle        Correct
                     Int.ModEq                                         math2001        Correct
                     parseExpression                                   Untangle        Correct

Table 8: Manual verification of 10 randomly sampled NL annotations. All annotations were judged to be mathemati-
cally accurate.

                            Category                                Time      Cost (USD)
                            Closed-source API calls           total 12 hrs   approx. 2500
                            Open-source inference      up to 48 GPU-hrs                 –
                            Compilation verification                96 hrs              –
                            NL annotation                             1 hr    approx. 100
                            Total                        approx. 157 hrs            2600

                            Table 9: Approximate computation cost of experiments.


(4.3% to 75.6%) and generally improve with scale,           GPT-5-nano achieves the highest compilation accu-
TA remains consistently below 5% for nearly all             racy (75.6%) but only 1.5% TA, a 50ˆ gap, while
models, visually confirming the persistent semantic         Claude-Sonnet-4.5 compiles at 46.0% but achieves
gap discussed in Section 6.3.                               the highest TA (4.5%). This rank reversal further
                                                            demonstrates that compilation accuracy is a poor
H    Detailed Experimental Results                          predictor of semantic correctness and that the Hard
                                                            subset effectively isolates the challenge of genuine
Table 11 presents the full compilation and testing
                                                            mathematical reasoning.
accuracy across three evaluation settings: existing
benchmarks, T2 (full), and T2 Hard.                         I    Discussion
   On existing benchmarks, the gap between com-
pilation and testing accuracy is relatively small           We now examine the scope and reliability of TA in
for most models. For instance, Claude-Sonnet-4.5            light of the limitations above.
achieves 90.6% compilation and 88.1% testing                   While coverage imposes an upper bound on what
accuracy. This is expected, as these benchmarks             TA can detect, the risk of false negatives, where
consist of isolated problems with a small number            a logically correct but differently formulated theo-
of successor theorems, limiting the discriminative          rem fails to compile against successor theorems, is
power of TA.                                                minimal in our setup. The type declarations such as
   On the full T2 benchmark, a clear gap emerges.           theorem, lemma, and def, and the exact name of
Models that compile at 60-80% drop to 24-39%                the target are provided as context (Section 3.1, foot-
testing accuracy, reflecting the stricter verification      note 1), and successor theorems reference the target
imposed by successor theorems in repository-level           by this name. If a generated theorem is logically
problems. Notably, testing accuracy across models           correct, it should type-check successfully against
converges to a narrow range (24-39%) despite wide           all successor theorems, leaving little room for false
variation in compilation rates, suggesting that most        negatives.
models can produce syntactically valid code for                The inapplicability of TA to standalone theo-
repository-level problems but struggle equally with         rems is likewise bounded in practice: across our
semantic correctness.                                       collected repositories, approximately 1.4% of theo-
   On T2 Hard, the gap becomes most pronounced.             rems have no successor theorems. Existing meth-
Compilation rates vary widely (4.3% to 75.6%),              ods, such as BLEU or manual inspection, can be
yet testing accuracy is uniformly low (1.3%-4.5%).          applied to these few cases, while our contribution
                                         NL ✓               NL ✗         K    Prompts
              Model               ST ✗      ST ✓      ST ✗     ST ✓
                          Closed-Source LLMs
                                                                         Following standard conventions in code genera-
     Claude-3.7-Sonnet             2.6          2.6   2.4          2.6
                                                                         tion evaluation, we design structured prompts that
     Claude-4-Sonnet               3.2          4.5   3.2          3.9   provide clear task specifications and output format
     Claude-Sonnet-4.5             3.9          4.5   3.0          3.6   constraints. Similar to how SWE-Bench restricts
     GPT-4o-mini                   1.3          1.5   1.3          1.5
     GPT-5                         3.4          3.4   1.9          2.8   models to bash-only interactions with explicit for-
     GPT-5-mini                    3.6          4.1   2.1          2.6   matting requirements, our prompts enforce a strict
     GPT-5-nano                    2.1          1.5   2.1          1.5
                                                                         output protocol: models must produce exactly one
                           Open-Source LLMs
                                                                         Lean 4 code block preceded by a reasoning section.
     DeepSeek-R1                   3.0          4.1   2.8          3.0
     GPT-OSS-120B                  3.9          4.5   4.7          5.1   The full prompt templates for informalization and
     Llama-3.1-405B                2.6          2.6   2.4          2.8   autoformalization are provided in Figure 7 and Fig-
     Llama-3.1-70B                 2.4          2.4   1.9          1.7
     Llama-3.1-8B                  1.5          1.3   1.5          1.5
                                                                         ure 8, respectively. We do not perform prompt sen-
                         Math Specialized Models
                                                                         sitivity analysis (e.g., varying instruction phrasing
     DeepSeek-Prover-v2-7B         2.4          3.2   2.8          3.2
                                                                         or format constraints), as our goal is to benchmark
     Goedel-Formalizer-v2-8B       1.5          2.4   1.9          2.1   model capabilities under a standardized evaluation
     Goedel-Prover-v2-32B          2.1          3.2   1.3          0.9
     Goedel-Prover-v2-8B           1.7          2.6   2.4          3.0
                                                                         protocol rather than optimize for prompt engineer-
     Kimina-Autoformalizer-7B      1.3          1.5   1.3          1.5   ing. This is consistent with prior work in both code
     Kimina-Prover-Distill-8B      2.6          1.7   1.7          2.6   generation (HumanEval, APPS) and theorem prov-
                                                                         ing (MiniF2F), where a fixed prompt template is
Table 10: Impact of input context on TA (%) on T2 Hard.
We compare two axes: whether an NL proof is provided,
                                                                         used across all models to ensure fair comparison.
and whether a successor theorem is provided (✓) or
withheld (✗).


enables automatic semantic evaluation for the re-
maining 98.6%.

J      Future Work
Our results suggest several promising directions
for extending TA and T2 . A natural next step is to
refine the binary scoring of TA into a graded met-
ric that accounts for partial success in successor
theorems compilation, providing a more nuanced
signal for model development. Beyond Lean 4, TA
is language-agnostic by design and can be extended
to any proof assistant that provides a dependency
parser and research-level repositories, such as Coq
and Isabelle.5 We chose Lean 4 for its actively
growing ecosystem with diverse repositories, and
leave extension to other proof assistants for future
work. Within Lean 4 itself, expanding T2 to addi-
tional repositories as the ecosystem grows would
further improve domain coverage. We also plan
to pursue a larger-scale verification of the natu-
ral language annotations in consultation with Lean
mathematics experts, complementing our initial
sample-based assessment.
5
    Coq provides coq-dpdgraph and the built-in coqdep for de-
    pendency parsing, with more than 45 research-level packages
    on GitHub. Isabelle provides a built-in session dependency
    system, and the Archive of Formal Proofs contains more than
    935 entries.
                                                   Existing              T2           T2 (Hard)
                    Model                       Compile       TA   Compile     TA    Compile   TA
                                                Closed-Source LLMs
                    Claude-3.7-Sonnet               79.5   76.7       75.1    36.8      34.3   2.6
                    Claude-4-Sonnet                 86.6   83.3       81.1    36.0      47.5   4.5
                    Claude-Sonnet-4.5               90.6   88.1       80.3    38.9      46.0   4.5
                    GPT-4o-mini                     64.3   60.5       59.1    36.7      12.2   1.5
                    GPT-5                           92.4   80.5       85.7    37.7      68.3   3.4
                    GPT-5-mini                      86.3   80.8       86.0    37.9      66.6   4.1
                    GPT-5-nano                      89.6   69.6       88.7    36.6      75.6   1.5
                                                 Open-Source LLMs
                    DeepSeek-R1                     82.3   79.0       70.5    36.3      25.1   4.1
                    GPT-OSS-120B                    53.7   48.4       68.2    32.3      40.0   4.5
                    Llama-3.1-405B                  75.4   72.9       63.4    33.2      27.8   2.6
                    Llama-3.1-70B                   72.2   68.1       65.4    37.0      20.1   2.4
                    Llama-3.1-8B                    54.4   45.8       36.9    24.8       6.4   1.3
                                               Math Specialized Models
                    DeepSeek-Prover-v2-7B           63.8   53.9       62.2    30.0      35.5   3.2
                    Goedel-Formalizer-v2-8B         22.0   19.2       38.7    23.6      22.1   2.4
                    Goedel-Prover-v2-32B            61.3   54.2       74.6    31.0      54.6   3.2
                    Goedel-Prover-v2-8B             22.3   18.7       46.1    24.5      37.9   2.6
                    Kimina-Autoformalizer-7B        14.2    1.0       21.9    20.0       4.3   1.5
                    Kimina-Prover-Distill-8B         3.0    2.0       28.0    23.4       5.1   1.7

Table 11: Full results across three evaluation settings: existing benchmarks, T2 (full), and T2 Hard. Results are
grouped by model type.
                          Closed Source
            Claude-3.7-Sonnet
                                                             ?B
                        Claude-4-Sonnet
                  Claude-Sonnet-4.5
              GPT-4o-mini
                                               GPT-5
                                          GPT-5-mini
                                                GPT-5-nano

                           Open Source
                      DeepSeek-R1
                                                       > 400B
         Llama-3.1-405B
                     GPT-OSS-120B
                                                        ~120B
                     Llama-3.1-70B
                        Goedel-Prover-v2-32B
                                                         ~32B
         Llama-3.1-8B
                                                        < 10B
        Kimina-Prover-Distill-8B
           Goedel-Prover-v2-8B
                     Goedel-formalizer-v2-8b
        DeepSeek-Prover-v2-7B                    Metric
                                                 Compilation
        Kimina-Autoformalizer-7B                 Testing
  0.0          0.2            0.4              0.6           0.8
                             Accuracy

Figure 6: Compilation accuracy and testing accuracy on
T2 Hard. Models are grouped by source availability and
parameter scale. Dashed bars indicate LLMs fine-tuned
on formal mathematical reasoning tasks.
System Prompt

You are a helpful assistant that can interact multiple times with a computer shell to solve programming
tasks. However, for this specific interaction, you are acting as an expert Lean 4 mathematician tasked
with translating formal Lean 4 code into a natural language description or proof.
Your response must contain exactly ONE plaintext code block.
Include a THOUGHT section before your code where you explain your reasoning process. Format
your response as shown in <format_example>.
<format_example>
 Natural Language


 THOUGHT : Your reasoning and analysis here


 Natural Language


 your_natural_language_description_here


</format_example>
Failure to follow these rules will cause your response to be rejected.


User Prompt

<task_description>
Your task is to provide a natural language description (that is informal proof or problem statement)
for the specific Lean 4 declaration.
Target Code Name: {{ target_code_name }}
The declaration is part of a larger code sequence.
The Code Context is provided below.

   • Header: Imports and open namespaces.

   • Code Before: Code appearing before the target.

   • Target Code: The specific code you need to describe/informalize.

Header:
 Lean 4


 {{ header }}


Code Before:
 Lean 4


 {{ before_target_code }}


Target Code:
 Lean 4


 {{ target_code }}


Code After:
 Lean 4


 {{ after_target_code }}


<instructions>
# Task Instructions
## Overview
You are an expert Lean 4 mathematician. You must provide a clear, concise, and mathematically
accurate natural language description of the Target Code.
   • If Target Code is a theorem/proof, provide an informal proof.

   • If Target Code is a definition, provide a mathematical definition in latex.

   • Use standard mathematical terminology (TeX/LaTeX style for formulas is preferred).

   • You must not use the exact function name used in lean code. You need to describe in natural
     language.

   • Do not start with which function name you are translating. Just start with the informal proof or
     problem statement.
## Output Coding Rules
1. A THOUGHT section where you explain your reasoning:
   • Analyze the Target Code to understand what it proves or defines.

   • Consider the context from Code Before and Code After if relevant.

   • Plan the natural language description.
2. A single plaintext code block with your description.
Format your responses like this:
<format_example>

 Natural Language


 THOUGHT : The target code defines a function \ texttt { foo } that adds two numbers
     .
     I will describe it as " The function determines the sum of two integers ."


 Natural Language


 The function determines the sum of two integers .


</format_example>
CRITICAL REQUIREMENTS:
   • Your response SHOULD include a THOUGHT section.

   • Your response MUST include EXACTLY ONE plaintext block.

   • This block MUST contain the COMPLETELY NEW natural language description.

   • Do NOT repeat the input code.
</instructions>
AI Response

 Natural Language


 {{ thoughts }}


 Natural Language


 {{ target_natural_language }}




                        Figure 7: Prompt template for informalizing Lean 4 code.

System Prompt

You are a helpful assistant that can interact multiple times with a computer shell to solve programming
tasks. However, for this specific interaction, you are acting as an expert Lean 4 mathematician tasked
with implementing a formal Lean 4 declaration (theorem or definition) based on the provided context.
Your response must contain exactly ONE lean code block.
Include a THOUGHT section before your code where you explain your reasoning process. Format
your response as shown in <format_example>.
<format_example>
 Natural Language


 THOUGHT : Your reasoning and analysis here , explaining how you deduce the
     implementation from the context .


 Lean 4


 your_formal_lean_code_here


</format_example>
Failure to follow these rules will cause your response to be rejected.


User Prompt

<task_description>
Your task is to provide the full formal Lean 4 code for the specific declaration named {{
target_code_name }}. The declaration is part of a larger code sequence, and you must imple-
ment it to fit seamlessly into the provided context.
The Code Context is provided below.

   • Header: Imports and open namespaces.

   • Code Before: Code appearing before the target.

   • Target Code Name: The name of the definition or theorem you need to implement.

   • Natural Language Description: A description of the target code in natural language.

   • Code After: Code appearing after the target.

Header:
 Lean 4


 {{ header }}


Code Before:
 Lean 4


 {{ before_target_code }}


Target Code Name:
 Natural Language


 {{ target_code_name }}


Natural Language Description:
 Natural Language


 {{ target_natural_language }}


Code After:
 Lean 4


 {{ after_target_code }}


<instructions>
# Task Instructions
## Overview
You are an expert Lean 4 mathematician. You must provide the complete and correct Lean 4 imple-
mentation for {{ target_code_name }}.

   • If it is a theorem, provide the statement and the full proof (do not use sorry).

   • If it is a definition, provide the full definition.

   • Pay close attention to Code Before and Code After to infer the correct type signatures, variable
     names, and logical dependencies.

   • Ensure your code compiles and integrates correctly with the surrounding context.

## Output Coding Rules
1. A THOUGHT section where you explain your reasoning:

   • Analyze the Code Before and Code After to deduce the purpose and signature of {{
     target_code_name }}.

   • Plan the implementation.

2. A single lean code block with your implementation.
Format your responses like this:
<format_example>
 Natural Language


 THOUGHT : The context shows a function \ texttt { foo } is used to add two numbers .
 I will implement \ texttt { foo } as a definition taking two Nats and returning
     their sum .


 Lean 4


 def foo (n m : Nat ) : Nat := n + m


</format_example>
CRITICAL REQUIREMENTS:

  • Your response SHOULD include a THOUGHT section.

  • Your response MUST include EXACTLY ONE lean block.

  • This block MUST contain the COMPLETELY NEW implementation for {{ target_code_name
    }}.

  • Do NOT repeat the Header or Code Before or Code After. Only output the code for {{
    target_code_name }}.

</instructions>

AI Response

 Natural Language


 {{ thoughts }}


 Lean 4


 {{ formal_proof }}




                    Figure 8: Prompt template for autoformalizing to Lean 4 code.
