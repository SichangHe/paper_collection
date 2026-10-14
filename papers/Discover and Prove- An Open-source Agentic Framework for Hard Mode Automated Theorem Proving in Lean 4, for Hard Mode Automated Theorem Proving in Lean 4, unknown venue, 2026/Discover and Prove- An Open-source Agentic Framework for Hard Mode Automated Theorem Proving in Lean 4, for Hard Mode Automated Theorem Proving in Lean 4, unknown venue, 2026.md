                                                      Discover and Prove: An Open-source Agentic Framework
                                                       for Hard Mode Automated Theorem Proving in Lean 4
                                                 Chengwu Liu1∗ , Yichun Yin2 , Ye Yuan1 , Jiaxuan Xie3 , Botao Li4 , Siqi Li4 ,
                                                         Jianhao Shen2 , Yan Xu2 , Lifeng Shang2 , Ming Zhang1 ,
                                         1
                                             State Key Laboratory for Multimedia Information Processing, School of Computer Science,
                                                       PKU-Anker LLM Lab, Peking University 2 Huawei Technologies Co., Ltd.
                                                              3
                                                                School of Software & Microelectronics, Peking University
                                                    4
                                                      School of Electronics Engineering and Computer Science, Peking University
                                                                        Correspondence: Ming Zhang (mzhang_cs@pku.edu.cn)
                                                                    Abstract                       problems generally requires capabilities that
                                                                                                   may generalize and transfer to complex real-
                                                     Most ATP benchmarks embed the final an-
                                                                                                   world tasks. These capabilities include plan-
arXiv:2604.15839v1 [cs.AI] 17 Apr 2026




                                                     swer within the formal statement — a con-
                                                     vention we call “Easy Mode” — a design
                                                                                                   ning, search, deductive reasoning, and induc-
                                                     that simplifies the task relative to what     tion. (Yang et al., 2024) Within the spectrum
                                                     human competitors face and may lead to        of mathematical tasks, competition problems
                                                     optimistic estimates of model capability.     — especially those at the International Math-
                                                     We call the stricter, more realistic set-     ematical Olympiad (IMO) level — have gar-
                                                     ting “Hard Mode”: the system must inde-       nered particular attention. These problems go
                                                     pendently discover the answer before con-     beyond numerical computation or simple for-
                                                     structing a formal proof. To enable Hard
                                                                                                   mula application. They typically demand ab-
                                                     Mode research, we make two contributions.
                                                     First, we release MiniF2F-Hard and FIMO-      straction and modeling, rigorous logical argu-
                                                     Hard, expert-reannotated Hard Mode vari-      mentation, and often require elements of intu-
                                                     ants of two widely-used ATP benchmarks.       ition and creativity. Accordingly, the ability
                                                     Second, we introduce Discover And Prove       to solve IMO-level problems is widely regarded
                                                     (DAP), an agentic framework that uses         as an important milestone for AI (Yang et al.,
                                                     LLM natural-language reasoning with ex-       2024).
                                                     plicit self-reflection to discover answers,
                                                                                                      Existing approaches to solving mathemati-
                                                     then rewrites Hard Mode statements into
                                                     Easy Mode ones for existing ATP provers.
                                                                                                   cal problems fall into two broad categories: in-
                                                     DAP sets the state of the art: on Com-        formal methods and formal methods. Informal
                                                     biBench it raises solved problems from 7      methods solve mathematical problems in nat-
                                                     (previous SOTA, Pass@16) to 10; on Put-       ural language and leverage the strong reason-
                                                     namBench it is the first system to formally   ing abilities of large language models (LLMs),
                                                     prove 36 theorems in Hard Mode — while        whereas formal methods use formal languages
                                                     simultaneously revealing that state-of-the-   such as Lean (Moura and Ullrich, 2021) and
                                                     art LLMs exceed 80% answer accuracy on
                                                                                                   Isabelle (Nipkow et al., 2002) to express the
                                                     the same problems where formal provers
                                                     manage under 10%, exposing a substan-         solution. A key advantage of formal methods
                                                     tial gap that Hard Mode benchmarks are        is that proofs written in formal languages can
                                                     uniquely suited to measure.                   be automatically and rigorously verified by a
                                                                                                   proof assistant program. At the International
                                             1       Introduction                                  Mathematical Olympiad (IMO) 2024, partici-
                                             The use of AI to solve mathematical prob-             pating AI systems employed formal methods
                                             lems has attracted considerable research in-          (AlphaProof and AlphaGeometry, 2024). By
                                             terest, not only because of the potential for         IMO 2025, however, most evaluated systems
                                             concrete applications in domains like educa-          had shifted toward informal approaches (Lu-
                                             tion and mathematical research, but also be-          ong et al., 2025; Huang and Yang, 2025; Wei,
                                             cause tackling highly abstract mathematical           2025; Huawei-xiaoyi, 2025).
                                                                                                      We observe that current practice in many
                                                 *
                                                 Work done during the internship at Huawei         formalization efforts often embeds the final an-
                                             Technologies Co., Ltd.    Code and datasets are
                                             available at https://github.com/liuchengwucn/         swer directly into the statement to be proved,
                                             discover-and-prove.                                   which we refer to as “Easy Mode”. We point
out that Easy Mode may substantially reduce        PutnamBench dataset, DAP solves 36 prob-
the diﬀiculty of formal problem-solving tasks.     lems in total. On solution-style problems with
To address this issue, we draw inspiration         Hard Mode variants, it solves 19 problems —
from prior works (PutnamBench (Tsoukalas           to our knowledge, this constitutes the first pub-
et al., 2024) and CombiBench (Liu et al.,          lic result on PutnamBench under this Hard
2025)): answer-oriented problems are encoded       Mode evaluation setting. On CombiBench
in Lean 4 with two separate goals (two distinct    Hard Mode, it solves 10 problems, improving
sorrys). In this “Hard Mode” configuration,        significantly on the previous state of the art
the model must first supply the final answer       (Kimina-Prover Preview), which solved 8 prob-
by replacing the first sorry with the answer       lems.
and then produce a conventional formal proof          Our contributions are threefold.
for the remaining goal. This setup prevents
                                                     1. We reannotate two commonly used
embedding extra information that human con-
                                                        ATP competition datasets, MiniF2F and
testants must discover by themselves in the for-
                                                        FIMO, to align tasks presented to human
mal statement. By definition, Hard Mode re-
                                                        competitors with those given to AI sys-
quires that any quantity a human competitor
                                                        tems, removing the Easy Mode discrep-
must derive through reasoning is not supplied
                                                        ancy and providing a more principled ba-
as a premise in the formal statement; it must
                                                        sis for evaluating AI mathematical capa-
be independently discovered by the AI system.
                                                        bility.
We adopt the term “Hard Mode” following
the convention in the Lean community;1 Com-          2. We propose DAP, an open-source, agen-
biBench (Liu et al., 2025) refers to the same           tic Hard Mode ATP framework. With a
distinction as “without solution” vs. “with so-         simple and straightforward design, DAP
lution”, while PutnamBench (Tsoukalas et al.,           achieves state-of-the-art performance on
2024) uses “no answer” vs. “with answer”. An            PutnamBench and CombiBench.
example illustrating the difference between
                                                     3. We provide an analysis quantifying the
Easy Mode and Hard Mode is presented in Fig-
                                                        individual contributions of the two mod-
ure 1. We commissioned expert annotators to
                                                        ules of our proposed DAP prover to
reannotate two widely used ATP competition
                                                        overall performance. These results shed
datasets, namely MiniF2F and FIMO, produc-
                                                        light on the relative strengths of informal
ing MiniF2F-Hard and FIMO-Hard. During
                                                        and formal method approaches for solv-
reannotation, we corrected known alignment
                                                        ing competition-level mathematical prob-
issues in existing formal benchmarks (Wang
                                                        lems.
et al., 2025a; Lin et al., 2025b).
   To solve Hard Mode problems, we intro-          2 Related Work
duce the Discover and Prove (DAP) frame-
work, a fully open-source, agent-based ATP         2.1 Mathematical Problem-Solving
framework for Hard Mode ATP tasks. DAP                 with AI systems
consists of two components: a Discovery Mod-       Powered by CoT prompting and RLVR train-
ule and a Proving Module. We prompt an             ing, LLMs have made substantial progress in
open-source LLM to generate and iteratively        mathematical reasoning. Frontier models (e.g.,
refine its reasoning and answers using self-       OpenAI o1 (Jaech et al., 2024), DeepSeek R1
verification procedures. After the Discovery       (Guo et al., 2025), Google Gemini 2.5 Pro
module “discovers” a plausible answer and fills    (Comanici et al., 2025)) now achieve near-
the first sorry, the Proving module attempts       saturation performance on widely-used math
to produce complete formal proofs by invok-        benchmarks, including GSM8K (Cobbe et al.,
ing traditional ATP provers. DAP achieves          2021), MATH-500 (Lightman et al., 2023), and
state-of-the-art results. Evaluating on the full   AIME 2024/2025.
                                                     One downside of the informal methods is
  1
   https://leanprover.                             that the solution traces they produce are no-
zulipchat.com/#narrow/channel/
208328-IMO-grand-challenge/topic/IMO.              toriously diﬀicult to verify automatically. As-
202025.20problem.20statements                      sessing the validity of a generated proof would
                       Easy Mode                                            Hard Mode
                imo_1962_p2 from miniF2F-test                         imo_1962_p2 from miniF2F-Hard



Figure 1: Differences between Easy Mode and Hard Mode configurations in automated theorem proving.
The example shown is a Lean 4 formalization of an IMO problem in two different styles. This example
was intentionally selected to illustrate the kind of semantic misalignment that our re-annotation effort
corrects: the Easy Mode formalization proves only that x must lie within certain ranges, but does not
establish that every value in those ranges is attainable, weakening the original if-and-only-if requirement
to a one-directional implication. By contrast, our Hard Mode formalization represents the answer as a
set, thereby fully capturing the natural-language problem’s requirement in the formal statement.


require domain experts to inspect it carefully         structured sketches; DSP+ (Cao et al., 2025)
to detect subtle errors (Lightman et al., 2023),       revives this paradigm with modern reasoning
which is infeasible at scale. For this reason,         models. DAP differs from DSP/DSP+ in
informal systems are typically applied to prob-        three key respects; see Appendix B for a de-
lems that require only a final numerical or            tailed comparison.
symbolic answer, verified by direct comparison
                                                         Several agentic frameworks have also tar-
against ground-truth (Wen et al., 2025).
                                                       geted Lean-based ATP (Thakur et al., 2023;
                                                       Kumarappan et al., 2024; Baba et al., 2025;
2.2   Automated Theorem Proving                        Wang et al., 2025b); see Appendix A.
The key strength of automated theorem prov-               To handle informal mathematical problems
ing (ATP) is that formal proofs can be checked         that require a final answer, prior efforts typi-
rigorously and automatically by proof assis-           cally convert problems requiring solutions into
tants (Yousefzadeh and Cao, 2025; Wang                 proof problems by embedding the desired an-
et al., 2023). Although formal approaches              swer into the formalized statement and prov-
have faced challenges of limited formal-data           ing that statement (Zheng et al., 2021; Liu
availability (Xin et al., 2024), they have ad-         et al., 2023; Xiong et al., 2023). This prac-
vanced rapidly with larger LLMs and scal-              tice raises two concerns. First, embedding
ing searching compute (Xin et al., 2025;               the answer in the statement can reduce the
Chen et al., 2025). Recent systems such as             intrinsic diﬀiculty: for many solution-oriented
Kimina-Prover Preview (Wang et al., 2025a),            problems, the primary challenge is discovering
DeepSeek-Prover-V2 (Ren et al., 2025), and             the answer rather than proving a consequence
Goedel-Prover-V2 (Lin et al., 2025b) have              once known, so supplying it acts as a sub-
made substantial progress on MiniF2F (Zheng            stantial hint. Second, the resulting formalized
et al., 2021) benchmark. Seed-Prover (Chen             statements are sometimes not perfectly seman-
et al., 2025) is a lemma-style whole-proof rea-        tically aligned with the tasks human contes-
soning model that iteratively refines proofs           tants face. As prior analyses (e.g., FMC (Xie
via Lean compiler feedback, proved lemmas,             et al., 2025), OlympiadBench (He et al., 2024))
and self-summarization, achieving over 50%             have noted, some existing formal benchmarks
on PutnamBench and saturating MiniF2F.                 are misaligned: some formal statements may
DSP (Jiang et al., 2023) guides formal theorem         capture only a subset of the goals that human
provers with natural-language draft proofs and         solvers must address.
2.3    Formalization & Data Curation               modules: a Discovery Module and a Prov-
High-quality formal datasets are scarce and        ing Module. The Discovery Module operates
require substantial expert effort (Xin et al.,     in natural language, tasked with identifying
2024). MiniF2F (Zheng et al., 2021) is one         the correct solution to the problem, and sub-
of the most widely used ATP benchmarks, con-       sequently transforms the original Hard Mode
taining formalized statements from mathemat-       Lean 4 statement into an Easy Mode state-
ical olympiads and high-school and undergrad-      ment. This transformation reduces the num-
uate courses; Kimina-Prover Preview (Wang          ber of sorry placeholders from two to one,
et al., 2025a) supplies corrections to a sub-      thereby leaving a single statement that can be
set of its problems.        FIMO (Liu et al.,      resolved by conventional automated theorem
2023) is constructed from IMO shortlist prob-      provers. Then, the Proving Module utilizes
lems but lacked a publicly available Lean 4        the Lean 4 formal language to construct a rig-
version, which impeded its adoption in re-         orous proof for the solution identified by the
cent work. PutnamBench (Tsoukalas et al.,          Discovery Module. The complete workflow of
2024) comprises hand-constructed formaliza-        the DAP framework is depicted in Figure 2.
tions of Putnam Competition problems and,          3.1 Discovery Module
for the first time, provides both “with answer”
                                                   The Discovery Module aims to solve the origi-
and “no answer” evaluation settings. Com-
                                                   nal mathematical problem and substitute the
biBench (Liu et al., 2025) offers 100 combi-
                                                   solution into the first sorry placeholder of the
natorics problems ranging from middle-school
                                                   Lean 4 Hard Mode statement for the Proving
level through IMO and university level, com-
                                                   Module to use. This process mirrors human
plementing the number-theoretic and alge-
                                                   problem-solving by hypothesizing an answer
braic focus of the other benchmarks; IMOSL-
                                                   to guide the proof search. Although the rea-
Lean4 (Sanjaya, 2025) and IMO-Steps (Youse-
                                                   soning capabilities of LLMs have substantially
fzadeh and Cao, 2024) additionally supply
                                                   improved following the introduction of long
complete proofs. To alleviate data scarcity,
                                                   Chain-of-Thoughts such as OpenAI o1 (Jaech
auto-formalization methods (Wu et al., 2022)
                                                   et al., 2024) and DeepSeek R1 (Guo et al.,
automatically translate informal problems into
                                                   2025), the one-shot resolution of highly chal-
formal statements. Representative resources
                                                   lenging, IMO-level problems remains unsolved.
include Lean Workbook (Ying et al., 2024),
                                                   Current research indicates that state-of-the-
NuminaMath-LEAN (Wang et al., 2025a),
                                                   art LLMs often require auxiliary tools (e.g., in-
Goedel-Pset-v1 (Lin et al., 2025a), and For-
                                                   formation retrieval, calculators, external mem-
malMATH (Yu et al., 2025). Because out-
                                                   ory) to support deep reasoning (Nakano et al.,
puts are typically validated only via LLM-as-a-
                                                   2022; Luo et al., 2025; Yuan et al., 2024). In-
judge (Ying et al., 2024), they lack guaranteed
                                                   spired by prior work on LLM reasoning sys-
semantic correctness and are more commonly
                                                   tems (Huang and Yang, 2025), we employ a
used in provers’ RL training phases (Wang
                                                   relatively straightforward configuration where
et al., 2025a; Xin et al., 2024) than as evalua-
                                                   an advanced reasoning model generates solu-
tion benchmarks. To our knowledge, all auto-
                                                   tion steps and performs self-verification to en-
formalization techniques follow the Easy Mode
                                                   hance accuracy. Specifically, the procedure in-
paradigm, embedding the desired answer di-
                                                   volves the following steps:
rectly into each generated statement.
                                                   (1) Solution Generation: Given a math-
3     Methodology                                  ematical problem in natural language, the
                                                   model’s reasoning capabilities are leveraged to
To address the challenge of proving Hard Mode      generate a detailed chain-of-thought describ-
Lean 4 theorems containing two sorry place-        ing the solution process.
holders, we propose the Discover and Prove         (2) Self-Verification: The reasoning LLM is
(DAP) framework, designed to emulate a hu-         instructed to inspect its steps for potential er-
man mathematician’s approach by providing          rors and produce an error report identifying
both the answer and a detailed proof. As its       any erroneous locations (a representative er-
name suggests, DAP consists of two primary         ror report is shown in Appendix C.5). If self-
                                                                                                                    Discovery Module
            Math Problem                                 CoT Reasoning                                           Error Report
         in Natural Language                           Generated by gpt-oss-120b
                                                                                            #2 Self-
                                                                                                              Generated by gpt-oss-120b
                                       Let’s think
         aime_1983_p1 from miniF2F                                                         Verification
                                      step by step


                                         LLM                                                   LLM


                                      #1 Solution                                            #3 Self-
                                      Generation                                            Correction




                                                                       Self-Verified
                                                                       Answer Candidate                                  Proving Module

       “Hard Mode” Statement                         “Easy Mode” Statement                                       Formal Proof
         Annotated by human experts                     Rewrote by gpt-oss-120b                             Generated by Goedel-Prover-V2




                                         LLM                                                   LLM


                                      #4 Rewriting                                         #5 Automated
                                                                                          Theorem Proving




Figure 2: Primary flowchart. A mathematical problem is first processed by the Discovery Module to
generate a solution; this solution is then incorporated into the Easy Mode statement during the rewriting
stage. Orange circles denote the reasoning LLM, and blue circles denote the theorem prover (another
distinct LLM).


verification reveals no errors, the process pro-                          known for its strong mathematical reasoning
ceeds to step 4; otherwise, it moves to step 3.                           performance. In principle, the framework can
(3) Self-Correction: The reasoning LLM is                                 be instantiated with any model that com-
instructed to generate a revised solution that                            bines robust mathematical reasoning with ba-
addresses the errors identified in the error re-                          sic Lean proficiency.
port.
(4) Rewriting: Using the Lean 4 Hard Mode
statement, the natural-language problem, and
the model’s chain-of-thought reasoning, the
LLM is prompted to produce a rewritten Lean                               3.2 Proving Module
4 statement containing only a single place-
holder, suitable for automated theorem prov-
ing.                                                                      Once the Discovery Module transforms a
                                                                          Hard Mode statement into an Easy Mode
   All four steps are implemented through                                 formulation, the task becomes a standard
meticulously designed prompts to the LLM,                                 ATP problem, amenable to conventional the-
which are detailed in Appendix C. The Dis-                                orem provers.      For this purpose, we em-
covery Module is crucial because incorrect so-                            ploy Goedel-Prover-V2 (32B), a state-of-the-
lutions frequently lead to flawed formal state-                           art open-source theorem prover, to process the
ments that are unprovable from the outset,                                transformed problems. By decoupling the rea-
thus emphasizing the model’s capacity for                                 soning model from the ATP model, the pro-
deep reasoning and reliable self-verification.                            posed framework can improve as any of the un-
This framework is released as open-source to                              derlying models advance, and provides a con-
facilitate reproducibility and serve as a base-                           temporary baseline for evaluating LLMs that
line.    For the Discovery Module, we uti-                                generate formal mathematical solutions in a
lize the open-source model GPT-OSS-120B,                                  proof assistant language.
Table 1: The table presents, for commonly used automated theorem proving datasets, the number of
statement samples, the number of Hard Mode problems, the data sources, data curation methods, and
compatibility with different versions of the Lean formal language. Notably, ProofNet and miniF2F were
originally released as Lean 3 datasets, and publicly available community ports to Lean 4 exist. Although
studies have reported performance on a Lean 4 variant of FIMO, no publicly available Lean 4 version of
the FIMO dataset exists.

                       # Samples # Hard Mode Data Source Curation Method Compatibility
        ProofNet            371          N/A          Textbook     Expert Annotation     Lean 3 & 4
                                                     Textbook &
       miniF2F-test         244          N/A                       Expert Annotation     Lean 3 & 4
                                                     Competition
         FIMO               149          N/A         Competition   Expert Annotation       Lean 3
      PutnamBench           660          340         Competition   Expert Annotation       Lean 4
                                                     Textbook &
       CombiBench           100           45                       Expert Annotation       Lean 4
                                                     Competition
      Lean Workbook         57k          N/A        AoPS Website  Auto-formalization       Lean 4
                                                                 Auto-formalization &
    NuminaMath-LEAN        104k          N/A         Competition                           Lean 4
                                                                  Expert Annotation
                                                     Textbook &
 MiniF2F-Hard (Ours)        244           194                      Expert Annotation       Lean 4
                                                     Competition
    FIMO-Hard (Ours)        149           70         Competition   Expert Annotation       Lean 4

4     Data Curation                                  emphasizing idiomatic Lean — “go further in
                                                     the direction of idiomatic Lean rather than
4.1    Annotation Principles                         trying to follow a particular English version
Our re-annotation is guided by three princi-         closely’’ — consistent with the IMOLean (My-
ples.                                                ers, 2025) practice of providing a single canon-
Semantic Accuracy:           Expert-annotated        ical statement.
datasets are small but reliable; auto-
formalized datasets are large but unverifiable       4.2 Data Selection
— current validation methods (LLM-as-a-              To address these deficiencies, we engaged
judge (Ying et al., 2024), BEq (Liu et al.,          Lean experts to reannotate two human-expert–
2024)) cannot guarantee semantic alignment           annotated datasets, namely MiniF2F (Zheng
with the original natural-language problem.          et al., 2021) and FIMO (Liu et al., 2023). Al-
We therefore start from expert-annotated             though ProofNet is also a high-quality, expert-
sources and re-examine each statement                annotated dataset, we observed that all of its
manually.                                            natural-language items are inherently proof-
Interpretability: A formal statement should          based; consequently, we excluded it from con-
reflect exactly what a human contestant is           sideration. The annotators each have more
asked to do: any quantity to be discovered           than one year of Lean-related experience. The
must not be supplied as a premise, and any           MiniF2F and FIMO datasets were originally
claim to be proved must appear as the goal.          produced by experts; we re-examined them in
Current benchmarks violate this in three re-         light of error reports documented in the liter-
curring ways: (1) encoding the final answer          ature (Wang et al., 2025a) and had each prob-
in the statement, (2) weakening the proof            lem independently annotated by two experts
goal to a strict subset of the original, or (3)      to cross-validate labels and thereby safeguard
adding premises that human contestants do            correctness.
not have. Representative instances are shown
in Figure 1; we followed the IMOLean (Myers,         4.3 Dataset Quality Fixes
2025) convention throughout.                         Beyond creating Hard Mode variants, our
Consistency: Formalization style can ma-             annotators performed three non-trivial cate-
terially affect ATP success rates (Lin et al.,       gories of quality-improvement work; full de-
2025a), so permitting annotators to choose ar-       tails are in Appendix D. Porting FIMO
bitrary formalizations would introduce evalu-        to Lean 4: we ported all FIMO problems
ation bias. We provided a unified convention         from Lean 3, verifying compilation and seman-
tic faithfulness. Fixing semantic misalign-       6 Discussion
ments: we identified and repaired ≈15 errors
                                                  6.1 Ablation Study on Agent
in miniF2F and ≈20 in FIMO across four er-
                                                      Effectiveness
ror types (Table 5). Rephrasing for Hard
Mode: unknown values were promoted to free        Advanced reasoning LLMs inherently pos-
parameters with explicit side-conditions; see     sess significant self-reflective capabilities (Wen
Figure 3 (Appendix E).                            et al., 2025). Consequently, explicitly in-
                                                  troducing self-verification and self-correction
                                                  mechanisms might impose an unnecessary rea-
                                                  soning overhead. To investigate when an agen-
5   Experiments
                                                  tic mode is beneficial, we conducted experi-
                                                  ments with the agent mode disabled across the
For the Discovery Module, we use the open-        PutnamBench, CombiBench, MiniF2F-Hard,
source model GPT-OSS-120B, which demon-           and FIMO-Hard datasets. The results are pre-
strates strong performance on natural lan-        sented in Table 2.
guage mathematical reasoning tasks. For the          Disabling the agent’s explicit self-
Proving Module, we use Goedel-Prover-V2,          verification and self-correction mechanisms
which exhibits state-of-the-art performance in    resulted in a significant performance degra-
traditional automated theorem proving. Our        dation on challenging datasets like Put-
formal verification environment uses Lean         namBench.         Conversely, no performance
4.15.0, with Kimina-Server (Dos Santos et al.,    degradation was observed on lower-diﬀiculty
2025) mediating interactions with the Lean 4      datasets, such as CombiBench and MiniF2F.
REPL.                                             We hypothesize that this effect stems from
                                                  these datasets containing a substantial
  For GPT-OSS-120B, we follow the model’s
                                                  proportion of relatively simple problems
recommended configuration with sampling
                                                  (e.g., middle-school textbook problems) that
temperature 1.0. During Self-Verification, the
                                                  reasoning LLMs can solve with minimal
model is allowed up to 30 iterative attempts
                                                  diﬀiculty. In such cases, the explicit inclusion
for self-checking and error correction. If all
                                                  of self-verification might inadvertently cause
attempts fail, the pipeline falls back to the
                                                  the model’s instruction-following behavior
no-agent (ablation) configuration, where the
                                                  to over-dominate, leading to excessive self-
reasoning model’s output is used directly as
                                                  questioning and the introduction of additional
the answer candidate without verification. For
                                                  noise to the solution.
Goedel-Prover-V2, we follow the developer-
                                                     We analyzed the Discovery Module’s accu-
recommended sampling configuration: temper-
                                                  racy on Hard Mode problems with ground-
ature 0.7, max_tokens set to 30,000, 32 sam-
                                                  truth answers, which permit direct assess-
ples, and Pass@32 evaluation metric. We
                                                  ment of natural language responses (Ta-
report performance on PutnamBench, Com-
                                                  ble 3). Even without agentic self-reflection,
biBench, miniF2F-Hard, and FIMO-Hard in
                                                  the model achieves approximately 78% cor-
Table 2.
                                                  rectness on Putnam problems, with perfor-
   Our method achieves state-of-the-art perfor-   mance on MiniF2F approaching saturation.
mance on Hard Mode problems. On Com-              For lower-diﬀiculty problems, explicit self-
biBench, it solves 10 problems, improving on      verification and self-correction can be superflu-
the prior state-of-the-art (8 problems); it is    ous given the already high one-shot accuracy
also the first method to solve problems under     of reasoning LLMs. However, for more chal-
PutnamBench’s “No Answer” configuration.          lenging benchmarks like PutnamBench and
Notably, on PutnamBench and miniF2F-test,         FIMO-Hard, these agentic components remain
our method’s Hard Mode accuracy closely ap-       crucial. A fine-grained failure-mode analysis
proaches Goedel-Prover-V2’s Easy Mode per-        of the Discovery Module on CombiBench and
formance, suggesting that our Discover and        FIMO is provided in Appendix F.
Prove approach effectively reduces Hard Mode         Ablating self-verification iteration counts
problems to Easy Mode problem statements.         shows that 10 iterations approach saturation
Table 2: Performance of various open-source approaches on standard and Hard Mode benchmarks. The
numerals beneath each dataset name indicate the total number of examples and the number of Hard Mode
examples. Best results under each configuration are indicated in boldface. In Hard Mode evaluation,
each dataset contains proof-style problems (evaluated in their original form) and solution-style problems
(evaluated with the answer not provided in the formal statement). Each entry X/Y denotes total problems
solved (X) and solution-style problems solved in Hard Mode (Y ). All results are Pass@32 unless otherwise
specified. † Kimina-Prover Preview originally reported 7 solved problems on CombiBench at Pass@16; the
value of 8 shown here is our re-evaluation at Pass@32.

                                                PutnamBench         CombiBench      miniF2F-test      FIMO
                                                  660 / 340           100 / 45        244 / 197      149 / 70
                    DeepSeek-Prover-V1.5                -                  2              122           1
                  DeepSeek-Prover-V2 (CoT)             22                  -              201           1
 Easy Mode         Kimina-Prover Preview                -                  8              168           1
                     Goedel-Prover-SFT                  6                  3              141           2
                      Goedel-Prover-V2                 43                 10              215           4
                   Kimina-Prover Preview                -               8† / -             -           -
 Hard Mode        DAP w/ Agent (Ours)                36 / 19            9/1            201 / 168      3/0
                  DAP w/o Agent (Ours)               32 / 15           10 / 2         204 / 171       3/0

Table 3: On the subset of Hard Mode problems                Table 4: Pass@32 comparison of three rewriting
with definitive (ground-truth) answers, the Discov-         strategies. No Rewriting and Straight Rewriting
ery Module’s performance in solving mathematical            results were manually verified to exclude spurious
problems presented in natural language was evalu-           proofs.
ated.
                                                              Benchmark             No    Straight    Ours
 Benchmark      Size   DAP w/ Agent   DAP w/o Agent
 PutnamBench    340       293 (86%)      265 (78%)            PutnamBench (660)      23         19      36
 CombiBench     45        32 (71%)       29 (64%)             CombiBench (100)       9          9       9
 miniF2F-Hard   197      197 (100%)     197 (100%)
 FIMO-Hard       70       43 (61%)       38 (54%)             miniF2F-Hard (244)     57         38     201
                                                              FIMO-Hard (149)        3          3       3
and 30 (our default) add only marginal gains;
see Appendix G.                                             draw three key observations.
6.2   Ablation on Rewriting Strategies                      No Rewriting is largely ineffective on
A central design choice in DAP is the two-                  Hard Mode problems. We attribute this
stage rewriting pipeline: the Discovery Mod-                to models’ lack of training on Hard Mode ATP
ule first derives the answer in natural lan-                tasks, producing large out-of-distribution per-
guage, and only then is the Hard Mode state-                formance drops when asked to both discover
ment transformed into an Easy Mode state-                   answers and prove them directly in the formal
ment for the ATP prover. To justify this de-                system.
sign, we compare three alternative strategies.
                                                         Straight Rewriting performs no better
No Rewriting: The Hard Mode problem
                                                         — and sometimes worse. Requiring the
statement (containing two sorry placehold-
                                                         model to handle answer discovery and formal-
ers) is fed directly to the ATP prover without
                                                         ization simultaneously in a single step causes it
any rewriting. Straight Rewriting: The Dis-
                                                         to frequently fail at both. The joint burden of
covery Module is discarded; instead, an LLM
                                                         informal mathematical reasoning and syntac-
is asked to simultaneously discover the answer
                                                         tically precise Lean code generation leads to
and produce the rewritten Easy Mode state-
                                                         degraded performance on most benchmarks.
ment in a single step. Proposed Rewriting
(Ours): The Discovery Module first finds the                Spurious proofs explain the remaining
answer; the Rewriting stage then transforms                 gap. We frequently observed spurious proofs
the statement using that answer.                            (cheating behavior) in both No Rewriting and
   Table 4 shows the results, from which we                 Straight Rewriting settings.    Because the
model can see the full Lean statement — in-       LLMs with self-reflection exceed 80% accuracy
cluding the abbrev solution definition —          on PutnamBench, while formal-language sys-
during solving, it sometimes avoids genuine       tems achieve less than 10
mathematical reasoning by copying problem            Despite the robust empirical performance
conditions directly into the proof. A concrete    of natural-language reasoning, formal mathe-
example from fimo_2009_algebra_p3 is              matical language will remain essential for fu-
shown in Figure 4 (Appendix H). DAP’s de-         ture AI systems in mathematical reasoning.
coupled design prevents this shortcut: the        Natural-language proofs are prone to subtle
prover only ever receives the rewritten Easy      errors that are challenging to identify with-
Mode statement, which does not expose the         out formal verification, significantly limiting
answer placeholder, eliminating the opportu-      their practical utility for critical applications
nity for such cheating behavior.                  such as education and advanced mathematics
   DAP’s modular design allows the Discov-        research. As evidenced by results on datasets
ery Module and the Proving Module to be re-       like Putnam and FIMO, formal mathematical
placed independently; experiments with both       reasoning still requires considerable develop-
lightweight small open-source models and          ment. We therefore propose that a promis-
the stronger Aristotle API confirm that the       ing avenue for future research involves inte-
pipeline remains functional across resource       grating the strengths of both natural-language
constraints and that stronger informal rea-       and formal-language approaches to bridge the
soning models yield further gains (see Ap-        existing performance disparity.
pendix I).

6.3   Natural Language Reasoning or
                                                  7 Conclusion
      Formal Language Reasoning?
The choice between natural-language and           This study identifies semantic accuracy, inter-
formal-language reasoning presents a criti-       pretability, and transparency problems in cur-
cal dilemma for AI’s advancement in com-          rent Easy Mode automated theorem-proving
plex problem-solving.      Recent innovations     settings. We argue that formal statements in
in natural-language reasoning—such as Long        Hard Mode, manually annotated by human
Chain-of-Thought and Reinforcement Learn-         experts with a unified convention, more ac-
ing from Human Feedback (RLHF), exempli-          curately reflect the problem-solving require-
fied by OpenAI’s o1 and DeepSeek’s R1—have        ments faced by participants in mathematical
significantly enhanced LLMs’ capabilities. Re-    competitions.
search has shown that natural-language rep-
resentations can exhibit very high empirical        To address the scarcity of Hard Mode ATP
ceilings; performance on challenging datasets     benchmarks, we engaged Lean 4 experts to re-
like AIME has saturated rapidly (Jaech et al.,    annotate high-quality datasets into the Hard
2024; Wen et al., 2025). At IMO 2025, the ma-     Mode format, producing MiniF2F-Hard and
jority of AI systems transitioned from formal     FIMO-Hard. In parallel, we rectified existing
to natural-language representations and suc-      semantic misalignments and enforced a unified
cessfully solved creative reasoning problems,     convention.
with several solutions attaining gold-medal          To address Hard Mode problems, we intro-
recognition. In contrast, formal-language sys-    duce the DAP framework, designed to offer a
tems like Seed Prover (Chen et al., 2025)         rigorous evaluation of AI systems’ capacity to
and Aristotle (Achim et al., 2025) achieved       solve complex formal mathematical problems.
medal-worthy results through extensive com-       The framework achieves state-of-the-art per-
putational search, with some solutions com-       formance on PutnamBench and CombiBench,
pleted only after oﬀicial submission deadlines.   representing the first reported progress on Put-
   This study investigates Hard Mode ATP as       namBench’s Hard Mode configuration. These
a neutral benchmark for comparing natural-        results demonstrate the eﬀicacy of combining
language and formal-language reasoning. We        natural-language reasoning to derive answers
observe a similar divergence: state-of-the-art    with formal methods to prove them.
Limitations                                         Kaito Baba, Chaoran Liu, Shuhei Kurita, and
                                                      Akiyoshi Sannai. 2025.     Prover agent: An
The primary limitation of this work concerns          agent-based framework for formal mathematical
potential dataset contamination, which may            proofs. arXiv preprint arXiv:2506.19923.
have led to inflated estimates of reported
                                                    Chenrui Cao, Liangcheng Song, Zenan Li, Xinyi Le,
AI performance. The miniF2F and FIMO
                                                      Xian Zhang, HUI XUE, and Fan Yang. 2025. Re-
datasets annotated in this study, together            viving dsp for advanced theorem proving in the
with their source problems in natural language        era of reasoning models. In The Thirty-ninth
(like IMO shortlisted problems) and other re-         Annual Conference on Neural Information Pro-
lated datasets, are publicly accessible on the        cessing Systems.
Internet. The two main LLMs employed                Luoxin Chen, Jinming Gu, Liankai Huang, Wen-
in this work—GPT-OSS-120B and Goedel-                 hao Huang, Zhicheng Jiang, Allan Jie, Xiaoran
Prover-V2—have released model weights but             Jin, Xing Jin, Chenggang Li, Kaijing Ma, and 1
not their training corpora; consequently, we          others. 2025. Seed-prover: Deep and broad rea-
                                                      soning for automated theorem proving. arXiv
cannot definitively determine whether these           preprint arXiv:2507.23726.
datasets were included in training data.
   By demonstrating a performance gap be-           Karl Cobbe, Vineet Kosaraju, Mohammad Bavar-
tween the Discovery Module and the Prov-              ian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
                                                      Matthias Plappert, Jerry Tworek, Jacob Hilton,
ing Module, this study identifies the bottle-         Reiichiro Nakano, and 1 others. 2021. Training
neck for Hard Mode ATP as formal reasoning            verifiers to solve math word problems. arXiv
rather than natural-language reasoning. This          preprint arXiv:2110.14168.
suggests that approaches leveraging natural-
                                                    Gheorghe Comanici, Eric Bieber, Mike Schaeker-
language reasoning to assist formal-language
                                                      mann, Ice Pasupat, Noveen Sachdeva, Inder-
reasoning, such as DSP (Jiang et al., 2023),          jit Dhillon, Marcel Blistein, Ori Ram, Dan
show promise. In our work, however, the               Zhang, Evan Rosen, and 1 others. 2025. Gem-
natural-language output passed to the Prov-           ini 2.5: Pushing the frontier with advanced rea-
ing Module is limited to answer candidates.           soning, multimodality, long context, and next
                                                      generation agentic capabilities. arXiv preprint
The integration between formal-language and          arXiv:2507.06261.
natural-language reasoning therefore remains
limited. Ideally, the two modules would inter-      Marco Dos Santos, Hugues de Saxcé, Haiming
act more tightly, with one modality providing        Wang, Mantas Baksys, Mert Unsal, Junqi Liu,
                                                     Zhengying Liu, and Jia LI. 2025. Kimina lean
assistance when the other encounters diﬀiculty.      server: A high-performance lean server for large-
Developing such tighter, cooperative integra-        scale verification. In The 5th Workshop on Math-
tion is left to future work.                         ematical Reasoning and AI at NeurIPS 2025.

Acknowledgments                                     Daya Guo, Dejian Yang, Haowei Zhang, Junxiao
                                                      Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
This paper is partially supported by grants           Shirong Ma, Peiyi Wang, Xiao Bi, and 1 oth-
from the National Key Research and Devel-             ers. 2025. Deepseek-r1: Incentivizing reason-
opment Program of China with Grant No.                ing capability in llms via reinforcement learning.
                                                      arXiv preprint arXiv:2501.12948.
2023YFC3341203.
                                                    Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding
                                                      Hu, Zhen Thai, Junhao Shen, Jinyi Hu, Xu Han,
References                                            Yujie Huang, Yuxiang Zhang, Jie Liu, Lei
Tudor Achim, Alex Best, Kevin Der, Mathïs             Qi, Zhiyuan Liu, and Maosong Sun. 2024.
  Fédérico, Sergei Gukov, Daniel Halpern-Leister,     OlympiadBench: A challenging benchmark for
  Kirsten Henningsgard, Yury Kudryashov,              promoting AGI with olympiad-level bilingual
  Alexander Meiburg, Martin Michelsen, and            multimodal scientific problems. In Proceedings
  1 others. 2025.    Aristotle: Imo-level auto-       of the 62nd Annual Meeting of the Association
  mated theorem proving.         arXiv preprint       for Computational Linguistics (Volume 1: Long
  arXiv:2510.01346.                                   Papers), pages 3828–3850, Bangkok, Thailand.
                                                      Association for Computational Linguistics.
Team AlphaProof and Team AlphaGeometry.
  2024. Ai achieves silver-medal standard solving   Yichen Huang and Lin F Yang. 2025. Gemini 2.5
  international 178 mathematical olympiad prob-       pro capable of winning gold at imo 2025. arXiv
  lems. DeepMind blog, 179:45.                        preprint arXiv:2507.15855.
Huawei-xiaoyi. 2025.     Huawei-xiaoyi/IMO2025-        In The Thirteenth International Conference on
  solutions.                                           Learning Representations.
Aaron Jaech, Adam Kalai, Adam Lerer, Adam            Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao,
  Richardson, Ahmed El-Kishky, Aiden Low, Alec         Junwei Yang, Yiyang Gu, Bohan Wu, Binqi
  Helyar, Aleksander Madry, Alex Beutel, Alex          Chen, Ziyue Qiao, Qingqing Long, Rongcheng
  Carney, and 1 others. 2024. Openai o1 system         Tu, Xiao Luo, Wei Ju, Zhiping Xiao, Yifan
  card. arXiv preprint arXiv:2412.16720.               Wang, Meng Xiao, Chenwu Liu, Jingyang Yuan,
                                                       Shichang Zhang, and 7 others. 2025. Large
Albert Qiaochu Jiang, Sean Welleck, Jin Peng
                                                       language model agent: A survey on method-
  Zhou, Timothee Lacroix, Jiacheng Liu, Wenda
                                                       ology, applications and challenges. Preprint,
  Li, Mateja Jamnik, Guillaume Lample, and
                                                       arXiv:2503.21460.
  Yuhuai Wu. 2023. Draft, sketch, and prove:
  Guiding formal theorem provers with informal       Thang Luong, Edward Lockhart, and 1 others.
  proofs. In The Eleventh International Confer-        2025. Advanced version of gemini with deep
  ence on Learning Representations.                    think oﬀicially achieves gold-medal standard at
Adarsh Kumarappan, Mo Tiwari, Peiyang Song,            the international mathematical olympiad. Deep-
  Robert Joseph George, Chaowei Xiao, and An-          Mind Blog.
  ima Anandkumar. 2024. Leanagent: Lifelong          Leonardo de Moura and Sebastian Ullrich. 2021.
  learning for formal theorem proving. In The          The lean 4 theorem prover and programming
 Thirteenth International Conference on Learn-         language. In International Conference on Au-
  ing Representations.                                 tomated Deduction, pages 625–635. Springer.
Hunter Lightman, Vineet Kosaraju, Yuri Burda,
                                                     Joseph Myers. 2025. Jsm28/IMOLean: Suggested
  Harrison Edwards, Bowen Baker, Teddy Lee,
                                                       conventions and examples for Lean formaliza-
  Jan Leike, John Schulman, Ilya Sutskever, and
                                                       tion of IMO problem statements.
  Karl Cobbe. 2023. Let’s verify step by step. In
 The Twelfth International Conference on Learn-      Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff
  ing Representations.                                 Wu, Long Ouyang, Christina Kim, Christopher
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,           Hesse, Shantanu Jain, Vineet Kosaraju, William
  Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou           Saunders, Xu Jiang, Karl Cobbe, Tyna Eloun-
  Xia, Danqi Chen, Sanjeev Arora, and Chi              dou, Gretchen Krueger, Kevin Button, Matthew
  Jin. 2025a. Goedel-Prover: A Frontier Model          Knight, Benjamin Chess, and John Schulman.
  for Open-Source Automated Theorem Proving.           2022.    Webgpt: Browser-assisted question-
  Preprint, arXiv:2502.07640.                          answering with human feedback.        Preprint,
                                                       arXiv:2112.09332.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang,
  Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan        Tobias Nipkow, Markus Wenzel, Lawrence C. Paul-
  Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri        son, Gerhard Goos, Juris Hartmanis, and Jan
  Gesi, Ximing Lu, David Acuna, Kaiyu Yang,            Van Leeuwen, editors. 2002. Isabelle/HOL, vol-
  Hongzhou Lin, Yejin Choi, Danqi Chen, San-           ume 2283 of Lecture Notes in Computer Science.
  jeev Arora, and Chi Jin. 2025b. Goedel-Prover-       Springer, Berlin, Heidelberg.
  V2: Scaling Formal Theorem Proving with
  Scaffolded Data Synthesis and Self-Correction.     Z. Z. Ren, Zhihong Shao, Junxiao Song, Hua-
  Preprint, arXiv:2508.03613.                          jian Xin, Haocheng Wang, Wanjia Zhao, Liyue
                                                       Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z. F.
Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengy-        Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang,
  ing Liu, Ye Yuan, Haiming Wang, Wei Ju,              Yuxuan Liu, Wenjun Gao, Daya Guo, and
  Chuanyang Zheng, Yichun Yin, Lin Li, Ming            Chong Ruan. 2025. DeepSeek-Prover-V2: Ad-
  Zhang, and Qun Liu. 2023. FIMO: A Challenge          vancing Formal Mathematical Reasoning via Re-
  Formal Dataset for Automated Theorem Prov-           inforcement Learning for Subgoal Decomposi-
  ing. Preprint, arXiv:2309.04295.                     tion. Preprint, arXiv:2504.21801.
Junqi Liu, Xiaohan Lin, Jonas Bayer, Yael Dillies,   Gian Sanjaya. 2025. Mortarsanjaya/IMOSLLean4.
  Weijie Jiang, Xiaodan Liang, Roman Soletskyi,
  Haiming Wang, Yunzhou Xie, Beibei Xiong,           Amitayush Thakur, George Tsoukalas, Yeming
  Zhengfeng Yang, Jujian Zhang, Lihong Zhi, Jia       Wen, Jimmy Xin, and Swarat Chaudhuri. 2023.
  Li, and Zhengying Liu. 2025. CombiBench:            An in-context learning agent for formal theorem-
  Benchmarking LLM Capability for Combinato-          proving. In First Conference on Language Mod-
  rial Mathematics. Preprint, arXiv:2505.03171.       eling.
Qi Liu, Xinhao Zheng, Xudong Lu, Qinxiang Cao,       George Tsoukalas, Jasper Lee, John Jennings,
  and Junchi Yan. 2024. Rethinking and Improv-         Jimmy Xin, Michelle Ding, Michael Jennings,
  ing Autoformalization: Towards a Faithful Met-       Amitayush Thakur, and Swarat Chaudhuri.
  ric and a Dependency Retrieval-based Approach.       2024.   PutnamBench:     Evaluating Neural
  Theorem-Provers on the Putnam Mathematical         Ran Xin, Chenguang Xi, Jie Yang, Feng Chen,
  Competition. Preprint, arXiv:2407.11214.             Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng,
                                                       and Kai Shen. 2025. BFS-Prover: Scalable Best-
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas          First Tree Search for LLM-based Automatic
  Baksys, Junqi Liu, Marco Dos Santos, Flood           Theorem Proving. Preprint, arXiv:2502.03438.
  Sung, Marina Vinyes, Zhenzhe Ying, Zekai
  Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton          Jing Xiong, Jianhao Shen, Ye Yuan, Haiming
  Bailey, Chendong Song, Chenjun Xiao, De-             Wang, Yichun Yin, Zhengying Liu, Lin Li,
  hao Zhang, Ebony Zhang, Frederick Pu, Han             Zhijiang Guo, Qingxing Cao, Yinya Huang,
  Zhu, and 21 others. 2025a. Kimina-Prover Pre-         Chuanyang Zheng, Xiaodan Liang, Ming Zhang,
  view: Towards Large Formal Reasoning Mod-             and Qun Liu. 2023. TRIGO: Benchmarking for-
  els with Reinforcement Learning. Preprint,            mal mathematical proof reduction for generative
  arXiv:2504.11354.                                     language models. In Proceedings of the 2023
                                                       Conference on Empirical Methods in Natural
Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao          Language Processing, pages 11594–11632, Singa-
  Shen, Yichun Yin, Jing Xiong, Enze Xie, Han           pore. Association for Computational Linguistics.
  Shi, Yujun Li, Lin Li, Jian Yin, Zhenguo Li, and
  Xiaodan Liang. 2023. DT-solver: Automated          Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda
  theorem proving with dynamic-tree sampling           Li, Kristin Lauter, Swarat Chaudhuri, and
  guided by proof-level value function. In Pro-        Dawn Song. 2024. Formal Mathematical Rea-
  ceedings of the 61st Annual Meeting of the Asso-     soning: A New Frontier in AI.        Preprint,
  ciation for Computational Linguistics (Volume        arXiv:2412.16075.
 1: Long Papers), pages 12632–12646, Toronto,
  Canada. Association for Computational Linguis-     Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu
  tics.                                                Wang, Dahua Lin, and Kai Chen. 2024. Lean
                                                       workbook: A large-scale lean problem set for-
Ruida Wang, Rui Pan, Yuxin Li, Jipeng Zhang,           malized from natural language math problems.
  Yizhen Jia, Shizhe Diao, Renjie Pi, Junjie Hu,      Advances in Neural Information Processing Sys-
  and Tong Zhang. 2025b. Ma-lot: Multi-agent          tems, 37:105848–105863.
  lean-based long chain-of-thought reasoning en-
  hances formal theorem proving. arXiv e-prints,     Roozbeh Yousefzadeh and Xuenan Cao. 2024. A
  pages arXiv–2503.                                    lean dataset for international math olympiad:
                                                       Small steps towards writing math proofs for
Alexander Wei. 2025.      Aw31/openai-imo-2025-        hard problems. Transactions on Machine Learn-
  proofs.                                              ing Research.

Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu           Roozbeh Yousefzadeh and Xuenan Cao. 2025.
  Ye, Zhirong Wu, Yang Wang, Zhijian Xu, Xiao          Advocate for Complete Benchmarks for For-
  Liang, Junjie Li, Ziming Miao, Jiang Bian,           mal Reasoning with Formal/Informal State-
  and Mao Yang. 2025. Reinforcement Learning           ments and Formal/Informal Proofs. Preprint,
  with Verifiable Rewards Implicitly Incentivizes      arXiv:2507.04719.
  Correct Reasoning in Base LLMs. Preprint,
                                                     Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li,
  arXiv:2506.14245.
                                                       Zhongyuan Peng, Minghao Liu, Yifan Zhang,
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li,             Zheng Yuan, Huajian Xin, Wenhao Huang, and
  Markus Rabe, Charles Staats, Mateja Jamnik,          1 others. 2025. Formalmath: Benchmarking for-
  and Christian Szegedy. 2022. Autoformalization       mal mathematical reasoning of large language
  with large language models. Advances in neu-         models. arXiv preprint arXiv:2505.02735.
  ral information processing systems, 35:32353–      Ye Yuan, Chengwu Liu, Jingyang Yuan, Gongbo
  32368.                                               Sun, Siqi Li, and Ming Zhang. 2024. A hybrid
Jiaxuan Xie, Chengwu Liu, Ye Yuan, Siqi Li, Zhip-      rag system with comprehensive enhancement on
   ing Xiao, and Ming Zhang. 2025. Fmc: Formal-        complex reasoning. Preprint, arXiv:2408.05141.
   ization of natural language mathematical compe-   Kunhao Zheng, Jesse Michael Han, and Stanislas
   tition problems. In 2nd AI for Math Workshop@       Polu. 2021. minif2f: a cross-system benchmark
  ICML 2025.                                           for formal olympiad-level mathematics. In In-
                                                      ternational Conference on Learning Representa-
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong
                                                      tions.
  Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
  Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao,
  Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F. Wu,
  Fuli Luo, and Chong Ruan. 2024. DeepSeek-
  Prover-V1.5: Harnessing Proof Assistant Feed-
  back for Reinforcement Learning and Monte-
  Carlo Tree Search. Preprint, arXiv:2408.08152.
A   Agentic Frameworks for Formal                  C Prompts used in Discovery
    Theorem Proving                                  Module

Beyond pure proof-search approaches, sev-          C.1 Prompt for Solution Generation
eral agentic frameworks have been explored         ### Core Instructions ###

for Lean-based ATP. COPRA (Thakur et al.,           *
                                                   ,→
                                                         **Rigor is Paramount:** Your primary goal is to
                                                         produce a complete and rigorously justified solution.
2023) converts a general-purpose LLM into a        ,→    Every step in your solution must be logically sound
                                                   ,→    and clearly explained. A correct final answer derived
Lean proof specialist via a language-agent loop.   ,→    from flawed or incomplete reasoning is considered a
                                                   ,→    failure.
LeanAgent (Kumarappan et al., 2024) stud-           *    **Honesty About Completeness:** If you cannot find a
                                                   ,→    complete solution, you must **not** guess or create a
ies lifelong learning to continuously improve      ,→    solution that appears correct but contains hidden
                                                   ,→    flaws or justification gaps. Instead, you should
LLM performance on advanced mathematics.           ,→    present only significant partial results that you can
                                                   ,→    rigorously prove. A partial result is considered
ProverAgent (Baba et al., 2025) leverages non-     ,→    significant if it represents a substantial advancement
                                                   ,→    toward a full solution. Examples include:
formal models to propose auxiliary lemmas                *   Proving a key lemma.
                                                         *   Fully resolving one or more cases within a
that guide formal proofs. MA-LoT (Wang                  ,→ logically sound case-based proof.
                                                         *   Establishing a critical property of the
et al., 2025b) applies a multi-agent, Lean-             ,→ mathematical objects in the problem.
                                                         *   For an optimization problem, proving an upper or
based long chain-of-thought approach with it-           ,→ lower bound without proving that this bound is
                                                        ,→ achievable.
erative proof repair via Lean compiler feed-        *    **Use TeX for All Mathematics:** All mathematical
                                                   ,→    variables, expressions, and relations must be enclosed
back. None of these systems are directly com-      ,→    in TeX delimiters (e.g., `Let $n$ be an integer.`).

pared to DAP experimentally, as they target        ### Output Format ###

standard (Easy Mode) ATP tasks and their            Your response MUST be structured into the following
                                                   ,→ sections, in this exact order.
setups are not directly comparable.
                                                   **1. Summary**

                                                    Provide a concise overview of your findings. This section
                                                   ,→ must contain two parts:
B   Comparison between DAP and
                                                    *    **a. Verdict:** State clearly whether you have found a
    DSP/DSP+                                       ,→    complete solution or a partial solution.
                                                         *   **For a complete solution:** State the final
                                                        ,→ answer, e.g., "I have successfully solved the
                                                        ,→ problem. The final answer is..."
DAP differs from DSP/DSP+ in three key                   *   **For a partial solution:** State the main
                                                        ,→ rigorous conclusion(s) you were able to prove,
respects. First, target task: DSP/DSP+                  ,→ e.g., "I have not found a complete solution, but I
                                                        ,→ have rigorously proven that..."
address standard ATP where the full formal          *
                                                   ,→
                                                         **b. Method Sketch:** Present a high-level, conceptual
                                                         outline of your solution. This sketch should allow an
statement is already given; DAP targets Hard       ,→    expert to understand the logical flow of your argument
                                                   ,→    without reading the full detail. It should include:
Mode ATP, where the system must first dis-               *   A narrative of your overall strategy.
                                                         *   The full and precise mathematical statements of any
cover the answer before proving. Second,                ,→ key lemmas or major intermediate results.
                                                         *   If applicable, describe any key constructions or
inter-module communication: DSP passes                  ,→ case splits that form the backbone of your
                                                        ,→ argument.
intermediate reasoning steps (draft and proof
                                                   **2. Detailed Solution**
sketch) to the formal prover; DAP passes only
                                                    Present the full, step-by-step mathematical proof. Each
the final answer to the rewriting stage. Pass-     ,→ step must be logically justified and clearly explained.
                                                   ,→ The level of detail should be sufficient for an expert
ing only the answer avoids reliance on par-        ,→ to verify the correctness of your reasoning without
                                                   ,→ needing to fill in any gaps. This section must contain
ticular formal-language idioms and sidesteps       ,→ ONLY the complete, rigorous proof, free of any
                                                   ,→ internal commentary, alternative approaches, or failed
the problem that natural-language solution         ,→ attempts.

steps are often awkward or counterproductive       ### Self-Correction Instruction ###

when injected directly into tactic-based Lean       Before finalizing your output, carefully review your
                                                   ,→ "Method Sketch" and "Detailed Solution" to ensure they
proofs (Liu et al., 2023). Additionally, DSP’s     ,→ are clean, rigorous, and strictly adhere to all
                                                   ,→ instructions provided above. Verify that every
design is tightly coupled to Isabelle’s subgoal    ,→ statement contributes directly to the final, coherent
                                                   ,→ mathematical argument.
syntax, making it diﬀicult to port to Lean,
while DSP+’s sketch steps require single equa-
tions expressible as Lean have statements,         C.2 Prompt for Self-Verification
which limits applicability. Third, verifica-
                                                    Below is the bug report. If you agree with certain item in
tion design: DAP front-loads self-verification     ,→ it, can you improve your solution so that it is
                                                   ,→ complete and rigorous? Note that the evaluator who
inside the Discovery Module before passing to      ,→ generates the bug report can misunderstand your
                                                   ,→ solution and thus make mistakes. If you do not agree
the prover; DSP includes no self-verification,     ,→ with certain item in the bug report, please add some
                                                   ,→ detailed explanations to avoid such misunderstanding.
and DSP+ performs repair only when the for-        ,→ Your new solution should strictly follow the
                                                   ,→ instructions in the system prompt.
mal sketch has a syntactic error.
C.3      Prompt for Self-Correction                             ```


 You are an expert AI assistant specializing in Formal
,→ Mathematics with the Lean 4 proof assistant. Your task
,→ is to perform a specific and targeted code                   C.4 Prompt for Rewriting
,→ modification.
                                                                 You are an expert mathematician and a meticulous grader for
 You will be given three inputs:                                ,→ an International Mathematical Olympiad (IMO) level
 1. A natural language math problem                             ,→ exam. Your primary task is to rigorously verify the
,→ (`<NATURAL_LANGUAGE_PROBLEM>`).                              ,→ provided mathematical solution. A solution is to be
 2. A detailed natural language solution to that problem        ,→ judged correct **only if every step is rigorously
,→ (`<NATURAL_LANGUAGE_SOLUTION>`).                             ,→ justified.** A solution that arrives at a correct
 3. A Lean 4 code statement that formalizes the problem         ,→ final answer through flawed reasoning, educated
,→ (`<LEAN4_STATEMENT>`).                                       ,→ guesses, or with gaps in its arguments must be flagged
                                                                ,→ as incorrect or incomplete.
 The Lean 4 statement contains a "fill-in-the-blank"
,→ definition for the solution, typically an `abbrev` or        ### Instructions ###
,→ `def` with `sorry` as its value.
                                                                 **1. Core Instructions**
**Your task is to:**                                             *   Your sole task is to find and report all issues in the
                                                                ,→ provided solution. You must act as a **verifier**, NOT
 1.   **Read the `<NATURAL_LANGUAGE_SOLUTION>` to find the      ,→ a solver. **Do NOT attempt to correct the errors or
,→    final answer** to the problem. The answer is usually      ,→ fill the gaps you find.**
,→    explicitly stated at the end (e.g., "The value is π/2",    *   You must perform a **step-by-step** check of the
,→    "The result is 42").                                      ,→ entire solution. This analysis will be presented in a
 2.   **Locate the `abbrev` or `def` line** in the              ,→ **Detailed Verification Log**, where you justify your
,→    `<LEAN4_STATEMENT>` that defines the solution variable    ,→ assessment of each step: for correct steps, a brief
,→    (e.g., `abbrev my_solution : ℝ := sorry`).                ,→ justification suffices; for steps with errors or gaps,
 3.   **Replace the `sorry`** in that definition with the       ,→ you must provide a detailed explanation.
,→    final answer you extracted. Ensure the syntax is
,→    correct for Lean 4 (e.g., `π` becomes `Real.pi`).          **2. How to Handle Issues in the Solution**
 4.   **Output the entire Lean 4 code block with this single     When you identify an issue in a step, you MUST first
,→    modification.** Do not change any other part of the       ,→ classify it into one of the following two categories
,→    code. Specifically, the `theorem`'s proof, which is       ,→ and then follow the specified procedure.
,→    also `sorry`, must remain unchanged.
                                                                *      **a. Critical Error:**
**Example:**                                                           This is any error that breaks the logical chain of the
                                                                      ,→ proof. This includes both **logical fallacies**
**<NATURAL_LANGUAGE_PROBLEM>:**                                       ,→ (e.g., claiming that `A>B, C>D` implies `A-C>B-D`)
Evaluate the integral \[\int_0^1 \frac{1}{1+x^2} \,dx.\]              ,→ and **factual errors** (e.g., a calculation error
                                                                      ,→ like `2+3=6`).
 **<NATURAL_LANGUAGE_SOLUTION>:**                                      *    **Procedure:**
 The problem is to evaluate the definite integral of \(f(x)                 *   Explain the specific error and state that it
,→ = \frac{1}{1+x^2}\) from \(0\) to \(1\).                                ,→ **invalidates the current line of reasoning**.
                                                                            *   Do NOT check any further steps that rely on
 The antiderivative of \(\frac{1}{1+x^2}\) is                              ,→ this error.
,→ \(\arctan(x)\).                                                          *   You MUST, however, scan the rest of the
 Using the Fundamental Theorem of Calculus, we have:                       ,→ solution to identify and verify any fully
 \[                                                                        ,→ independent parts. For example, if a proof is
 \int_0^1 \frac{1}{1+x^2} \,dx = [\arctan(x)]_0^1                          ,→ split into multiple cases, an error in one
 \]                                                                        ,→ case does not prevent you from checking the
 \[                                                                        ,→ other cases.
 = \arctan(1) - \arctan(0)
 \]                                                             *      **b. Justification Gap:**
 Since \(\arctan(1) = \pi/4\) and \(\arctan(0) = 0\), the              This is for steps where the conclusion may be correct,
,→ value of the integral is:                                          ,→ but the provided argument is incomplete, hand-wavy,
 \[                                                                   ,→ or lacks sufficient rigor.
 \frac{\pi}{4} - 0 = \frac{\pi}{4}.                                    *    **Procedure:**
 \]                                                                         *   Explain the gap in the justification.
 The final answer is \(\pi/4\).                                             *   State that you will **assume the step's
                                                                           ,→ conclusion is true** for the sake of argument.
 **<LEAN4_STATEMENT>:**                                                     *   Then, proceed to verify all subsequent steps
 ```lean                                                                   ,→ to check if the remainder of the argument is
 import                                                                    ,→ sound.
,→ Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
                                                                 **3. Output Format**
open Set                                                         Your response MUST be structured into two main sections: a
                                                                ,→ **Summary** followed by the **Detailed Verification
abbrev integral_value : ℝ := sorry                              ,→ Log**.
theorem integral_example                                        *      **a. Summary**
  : ∫ x in Icc 0 1, 1 / (1 + x^2) = integral_value :=                  This section MUST be at the very beginning of your
sorry                                                                 ,→ response. It must contain two components:
```                                                                    *    **Final Verdict**: A single, clear sentence
                                                                      ,→ declaring the overall validity of the solution. For
 **Expected Output:**
                                                                      ,→ example: "The solution is correct," "The solution
 ```lean
                                                                      ,→ contains a Critical Error and is therefore
 import
                                                                      ,→ invalid," or "The solution's approach is viable
,→ Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
                                                                      ,→ but contains several Justification Gaps."
                                                                       *    **List of Findings**: A bulleted list that
open Set
                                                                      ,→ summarizes **every** issue you discovered. For
abbrev integral_value : ℝ := Real.pi / 4                              ,→ each finding, you must provide:
                                                                            *   **Location:** A direct quote of the key phrase
theorem integral_example                                                   ,→ or equation where the issue occurs.
  : ∫ x in Icc 0 1, 1 / (1 + x^2) = integral_value :=                       *   **Issue:** A brief description of the problem
sorry                                                                      ,→ and its classification (**Critical Error** or
```                                                                        ,→ **Justification Gap**).

---                                                             *      **b. Detailed Verification Log**
                                                                       Following the summary, provide the full, step-by-step
Now, perform the task for the following inputs.                       ,→ verification log as defined in the Core
                                                                      ,→ Instructions. When you refer to a specific part of
**<NATURAL_LANGUAGE_PROBLEM>:**                                       ,→ the solution, **quote the relevant text** to make
{{NATURAL_LANGUAGE_PROBLEM}}                                          ,→ your reference clear before providing your
                                                                      ,→ detailed analysis of that part.
**<NATURAL_LANGUAGE_SOLUTION>:**
{{NATURAL_LANGUAGE_SOLUTION}}                                    **Example of the Required Summary Format**
                                                                 *This is a generic example to illustrate the required
**<LEAN4_STATEMENT>:**                                          ,→ format. Your findings must be based on the actual
```lean                                                         ,→ solution provided below.*
{{LEAN4_STATEMENT}}
 **Final Verdict:** The solution is **invalid** because it     We found approximately 15 misalignments in
,→ contains a Critical Error.
                                                               miniF2F and 20 in FIMO. Table 5 summarises
 **List of Findings:**
 *    **Location:** "By interchanging the limit and the        the four most common error types.
,→ integral, we get..."
      *   **Issue:** Justification Gap - The solution          Rephrasing for Hard Mode Compatibil-
     ,→ interchanges a limit and an integral without
     ,→ providing justification, such as proving uniform       ity: Our annotation principle requires that
     ,→ convergence.
 *    **Location:** "From $A > B$ and $C > D$, it follows      any quantity a human competitor must de-
,→ that $A-C > B-D$"
      *   **Issue:** Critical Error - This step is a logical   rive must not be hard-coded in the formal
     ,→ fallacy. Subtracting inequalities in this manner
     ,→ is not a valid mathematical operation.                 statement. In some cases this meant non-
                                                               trivially rephrasing a problem so that the un-
C.5    Example of Self-Verification Error                      known value becomes a free parameter and
       Report                                                  proper side-conditions (simplicity, squarefree-
                                                               ness, positivity, etc.) are added explicitly. A
The Self-Verification step prompts the LLM
                                                               representative before/after example is shown
to carefully review the generated solution step
                                                               in Figure 3 (Appendix E).
by step and produce a structured error report.
Each finding identifies a specific location in the             E Hard Mode Annotation Example
solution, describes the issue, and classifies its
severity. The following is a representative ex-                Figure 3 shows a representative before/after
ample of such an error report, produced by the                 example of rephrasing a problem for Hard
Discovery Module on a functional-equation                      Mode compatibility. The original formaliza-
problem.                                                       tion hard-codes c = 2, leaking part of the an-
                                                               swer; the rephrased version promotes c to
 Final Verdict: The solution contains several Justification
,→ Gaps and therefore is not fully rigorous.
                                                               a free parameter and adds explicit simplicity
 List of Findings:
                                                               and squarefreeness conditions, requiring the
 * Location: Lemma 1 proof -- "h(x0) is an upper bound of
,→ the set {y | y < x0} ..."
                                                               solver to determine the canonical form inde-
    Issue: Justification Gap -- the claim that h(x0) bounds
   ,→ all predecessors of x0 is not proved; the argument
                                                               pendently.
   ,→ that this contradicts the supremum property is
   ,→ invalid.
 * Location: Lemma 2 proof -- "Both lines are proved by a      F Failure-Mode Analysis of the
,→ simple induction on the natural variable."
    Issue: Justification Gap -- the induction for the second     Discovery Module
   ,→ coordinate is only sketched; it is not shown that
   ,→ the composed beta-functions satisfy the required
   ,→ monotonicity and domination properties.                  To understand the limitations of the Discov-
 * Location: Lemma 2 proof -- base case "For n=0 ..." while
,→ N was earlier taken to start at 1.
                                                               ery Module, we analyzed all Discovery out-
    Issue: Minor Justification Gap -- the indexing mismatch
   ,→ is not addressed, though it does not affect the
                                                               puts on the 45 solution-style problems from
   ,→ overall argument.
                                                               CombiBench and the 70 solution-style prob-
                                                               lems from FIMO. These two sets are moder-
D     Dataset Quality Fixes                                    ate in diﬀiculty (avoiding the saturation seen
                                                               on miniF2F-Hard) and cover a broad range
Porting FIMO to Lean 4: The publicly
                                                               of competition mathematics areas (combina-
available FIMO dataset is written in Lean 3.
                                                               torics, number theory, and algebra), mak-
Although a largely automated migration tool
                                                               ing them well-suited for diagnosing real weak-
exists, the syntactic and library-level changes
                                                               nesses. We manually categorized every Dis-
between Lean 3 and Lean 4 mean that many
                                                               covery failure and summarize the main error
statements do not port cleanly: tactic names
                                                               types in Table 6.
changed, Mathlib APIs were reorganised, and
some constructs require manual rewriting to                    FIMO: high diﬀiculty in number the-
compile while remaining semantically faithful.                 ory and algebra. Many FIMO problems
Our annotators ported every FIMO problem                       remain beyond the model’s capabilities; self-
to Lean 4, verifying that each statement com-                  verification cannot fully recover correct an-
piles and is semantically faithful to the origi-               swers for the hardest instances. Function-
nal.                                                           equation problems are particularly challenging
Fixing Semantic Misalignments: Follow-                         and often fail even with verification, as the
ing the annotation principles described in §4.1,               underlying reasoning requires multi-step alge-
annotators identified and repaired formaliza-                  braic manipulation that is diﬀicult to check
tion errors present in the source datasets.                    automatically.
Table 5: Semantic misalignment types found and corrected in miniF2F and FIMO during our re-
annotation.

 Misalignment Type                # in miniF2F # in FIMO Example
 Ignoring whether an extremum                               mathd_numbertheory_495,
                                       8           8
 is attainable                                              fimo_2010_number_theory_p1_1
 Adding extra conditions in the                             mathd_algebra_320,
                                       2           1
 formalization                                              fimo_2017_number_theory_p8
                                                            amc12b_2021_p3,
 Incomplete proof goals                2           2
                                                            fimo_2008_algebra_p1
 Missing/incomplete NL prob-                                mathd_algebra_188,
                                       2           2
 lem statements                                             fimo_2008_algebra_p3_1

Table 6: Failure-mode analysis of the Discovery Module on FIMO and CombiBench, with and without
self-verification (SV). Counts indicate the number of problems exhibiting each failure type.

                               FIMO FIMO Combi Combi
 Error Type                                              Example
                               w/o SV w/ SV w/o SV w/ SV
 Failed to correctly under-                                   imo_2010_p5: invented a non-existent
                                  0        0   3        3
 stand the problem                                            operation
 Ignored or misused con-                                      fimo_2010_number_theory_p1_2:
                                  3        2   2        2
 straints                                                     omitted case analysis
 Incorrect mathematical rea-                                  fimo_2016_algebra_p3:     induction
                                  2        2   5        3
 soning foundations                                           without base case
 Minor arithmetic / computa-                                  fimo_2012_algebra_p1: arithmetic
                                  9        4   0        0
 tional error                                                 mistake
 Insuﬀicient depth / beyond                                   fimo_2013_algebra_p6: missing pre-
                                  4        2   2        2
 model capability                                             processing



CombiBench: comprehension failures.                G Self-Verification Iteration
On CombiBench, we frequently observed that           Ablation
the model did not correctly understand prob-
lem statements or even hallucinated conditions     Table 7 quantifies the effect of the maximum
that do not appear in the original problem.        number of self-verification iterations on Dis-
These comprehension failures are not substan-      covery Module accuracy.
tially reduced by self-verification. We hypoth-
                                                   Table 7: Discovery Module accuracy (number of
esize that certain combinatorial phrasings—
                                                   correctly solved problems) under varying maxi-
though natural to humans—are less accessible       mum self-verification iteration budgets. Column
to current LLMs and lead to misparsing or mis-     headers indicate the iteration limit; 0 means no
interpretation.                                    self-verification. † Our default setting. All results
                                                   are Pass@32.

Self-verification helps but is not a cure-                                   Max SV Iterations
all. For number-theory and algebra prob-               Dataset                0     5    10    30†
lems, self-verification notably reduces minor
                                                       PutnamBench (340) 265 291 292 293
computational errors (9 → 4) and some                  CombiBench (45)     29  31  32 32
shallow-reasoning failures (4 → 2), rescuing           miniF2F-Hard (194) 194 194 194 194
answers lost due to arithmetic mistakes. For           FIMO-Hard (70)      38  40  43 43
combinatorics, self-verification helps reduce
instances of incorrect reasoning foundations          Two observations emerge.         First, on
(5 → 3) but does not eliminate comprehen-          miniF2F-Hard the Discovery Module achieves
sion or hallucination errors. Overall, self-       perfect accuracy even without self-verification,
verification is most effective when the error is   consistent with the saturation effect (though
a localized mistake (e.g., an arithmetic slip)     possible dataset contamination should be
rather than a fundamental misunderstanding         noted).    Second, for harder benchmarks
of the problem.                                    like PutnamBench and FIMO-Hard, self-
Natural-language problem:√Let x be a positive number such that 2x2 = 4x + 9. If x can be written
                      a+ b
in simplified form as         where a, b, and c are positive integers, what is a + b + c?
                         c
Original formalization (problematic) — c = 2 is hard-coded:

theorem mathd_algebra_320
    (x : ℝ) (a b c : ℕ)
    (h0 : 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 ≤ x)
    (h1 : 2 * x ^ 2 = 4 * x + 9)
    (h2 : x = (a + Real.sqrt b) / c)
    (h3 : c = 2) : a + b + c = 26 := by


Rephrased formalization (aligned) — c is a free parameter:

abbrev mathd_algebra_320_solution : ℕ := sorry
-- 26

theorem mathd_algebra_320
    (x : ℝ) (a b c : ℕ)
    (h_x_pos : 0 < x)
    (h_eqn : 2 * x ^ 2 = 4 * x + 9)
    (h_form : x = (a + Real.sqrt b) / c)
    (h_abc_pos : a > 0 ∧ b > 0 ∧ c > 0)
    (h_simplified_gcd : Nat.gcd a c = 1)
    (h_simplified_sq_free : Squarefree b)
    : a + b + c = mathd_algebra_320_solution := by
      sorry

Figure 3: Rephrasing mathd_algebra_320 for Hard Mode compatibility. The original formalization
hard-codes c = 2, leaking part of the answer; the rephrased version promotes c to a free parameter and
adds explicit simplicity and squarefreeness conditions, requiring the solver to determine the canonical
form independently.


verification provides substantial gains; 10 iter-    model. Because the Aristotle API (Achim
ations approach saturation and balance com-          et al., 2025) does not support concurrent re-
putational cost with accuracy, while 30 iter-        quests and each problem can take hours, we
ations adds marginal gains and serves as our         sampled five problems per dataset for that con-
default.                                             dition; results are reported as solved/total.

H    Spurious Proof Example                          Table 8: Pass@32 results for different Discovery–
                                                     Proving model pairings. † Aristotle API results are
Figure 4 shows a concrete example of a spu-          sampled (5 problems per dataset).
rious proof observed under the No Rewriting
setting. The proof closes by rfl because the          Configuration
                                                                             Putnam   Combi   mF2F    FIMO
                                                                              (660)   (100)   (244)   (149)
abbrev solution was defined to be liter-              GPT-OSS 120B +
ally the same set as the one appearing in the         Goedel-V2 32B (Ours)     36       9      201      3
                                                      Qwen3 8B +
theorem statement — the prover never needed           DS-Prover-V1.5 7B        5        2      107      2
                                                      GPT-5 (Thinking) +
to reason about the underlying mathematics.
                                                      Aristotle API†          3/5      3/5     5/5     2/5

I   Cross-Model Pairing
                                                       Two conclusions follow. First, the pipeline
A practical advantage of DAP’s modular de-           is functional even with small, resource-
sign is that the Discovery Module and the            eﬀicient models, supporting use in compute-
Proving Module can be replaced indepen-              constrained settings. Second, replacing the
dently. To demonstrate this flexibility, Table 8     Discovery Module with a significantly stronger
reports results for three model combinations:        model yields meaningful further gains, illus-
our default pairing, a lightweight pairing us-       trating the headroom available as informal rea-
ing smaller open-source models, and a high-          soning models continue to improve.
resource pairing using a stronger closed-source
abbrev fimo_2009_algebra_p3_solution : Set (ℕ+ → ℕ+) :=
  { f : ℕ+ → ℕ+ | (∀ x y,
      x + f y > f (y + f x - 1) ∧
      x + f (y + f x - 1) > f y ∧
      f y + f (y + f x - 1) > x) }

theorem fimo_2009_algebra_p3 :
  { f : ℕ+ → ℕ+ | (∀ x y,
      x + f y > f (y + f x - 1) ∧
      x + f (y + f x - 1) > f y ∧
      f y + f (y + f x - 1) > x) } =
    fimo_2009_algebra_p3_solution := by
  have h_main : { f : ℕ+ → ℕ+ | (∀ x y,
      x + f y > f (y + f x - 1) ∧
      x + f (y + f x - 1) > f y ∧
      f y + f (y + f x - 1) > x) } =
    fimo_2009_algebra_p3_solution := by rfl
  exact h_main


Figure 4: A spurious proof of fimo_2009_algebra_p3 observed under the No Rewriting setting. The
abbrev solution is defined as the same set that appears in the theorem statement, so the prover
closes the goal with rfl without performing any mathematical reasoning.
