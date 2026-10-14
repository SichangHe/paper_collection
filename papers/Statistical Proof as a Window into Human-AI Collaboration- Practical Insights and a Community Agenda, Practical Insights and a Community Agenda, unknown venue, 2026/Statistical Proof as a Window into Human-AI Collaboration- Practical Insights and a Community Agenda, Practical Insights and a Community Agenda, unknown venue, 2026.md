                                               Statistical Proof as a Window into Human-AI Collaboration:
                                                        Practical Insights and a Community Agenda
                                               Xiaojing Sun∗        Huayu Tang∗          Buxin Su†         Mateo Matijasevick∗          Chong Wu‡
                                                                              Fei Xue∗§              Bingxin Zhao†§

                                                                                          June 23, 2026
arXiv:2606.23666v1 [stat.OT] 22 Jun 2026




                                                                                             Abstract
                                                       Large language models (LLMs) are increasingly woven into expert cognitive work in
                                                   daily research, yet we know little about how human expertise should adapt when an AI
                                                   system can execute substantial technical reasoning on its own. Here we use statistical proof
                                                   development, a demanding and structured form of expert reasoning, as a window into this
                                                   broader question. Drawing on day-to-day proof problems, we find that current general-
                                                   purpose LLMs occupy a useful but limited role: they can execute technical components
                                                   given a precisely formulated problem and targeted guidance, but become unreliable when
                                                   the problem is open-ended or requires a long reasoning chain with multiple interdependent
                                                   steps. This execution-strategy gap is rooted in what makes research-level statistical proof
                                                   distinctive: unlike pure mathematics, where problems arrive pre-formulated and solutions
                                                   often demand entirely novel techniques, statistical proof requires first modeling a scientific
                                                   question into a statistical framework with appropriate assumptions, and then identifying and
                                                   adapting the right strategy from a repertoire of reusable domain-specific tools. Each step
                                                   involves judgments that require deep expertise in both the statistical literature and the real-
                                                   world context being modeled. For human-AI collaboration in such cognitive work, current AI
                                                   assistance does not reduce the need for human expertise; it relocates that expertise to where
                                                   human decision-making matters most, such as problem formulation and verification of AI-
                                                   generated results, and may raise the bar for both, since human users must now make rapid
                                                   decisions alongside AI tools. These findings yield practical suggestions for how statisticians
                                                   can structure AI-assisted proof workflows in their daily research, and point to a broader
                                                   community agenda for shared resources, better AI tools, and training the next generation
                                                   of researchers. Using statistical proof as a window, our study carries implications for how
                                                   experts structure human-AI collaboration in technical cognitive domains more broadly.


                                           1       Introduction
                                           Proof is the backbone of statistical research, where theory and real-world scientific problems
                                           are deeply intertwined. Through rigorous mathematical argument, statisticians justify new
                                           estimators and procedures used in data analysis, clarify the assumptions under which they are
                                           valid, and explain how performance depends on model structure, dataset features, and noise
                                           [Zhao, 2025]. These arguments are often directly motivated by interdisciplinary applications
                                           such as in genomics, economics, and medicine, where the choice of assumptions needed to form a
                                           statistical framework and the interpretation of results must remain grounded in the underlying
                                           science. Together, these features make statistical proof development a demanding form of expert
                                               ∗
                                                 Purdue University
                                               †
                                                 University of Pennsylvania
                                               ‡
                                                 University of Texas MD Anderson Cancer Center
                                               §
                                                 These authors jointly supervised this work. Correspondence: feixue@purdue.edu;bxzhao@wharton.upenn.edu



                                                                                                 1
cognition: it requires scientific judgment about how to formulate a real-world question as a
tractable statistical problem, domain expertise to navigate a broad landscape of proof strategies,
and the experience to know which strategy fits a new problem and context, capabilities that
can take years to acquire even for experienced researchers. For graduate students, acquiring
this expertise is also challenging: they must learn to formulate real-world questions as precise
statistical problems, identify appropriate proof strategies, and execute rigorous arguments, skills
that are currently transmitted slowly and unevenly through textbooks, previous literature, and
one-on-one guidance from their advisors. These bottlenecks slow both the development of
new statistical methodology and the transmission of proof expertise to the next generation of
statisticians.
    Large language models (LLMs) are now reshaping how scientists conduct research across
many disciplines. Notably, LLM-based AI systems are increasingly capable of mathemati-
cal reasoning and proof assistance [Wang et al., 2026, Ju and Dong, 2026, Ren et al., 2025,
Romera-Paredes et al., 2024], and recent progress in Olympiad-style problem solving, formal
verification, and research-level reasoning suggests that these systems may become useful tools
for mathematical research more broadly [Trinh et al., 2024, Hubert et al., 2026, Woodruff et al.,
2026, Feng et al., 2026]. The statistics community is no exception: researchers are increasingly
asking whether AI can assist with proof development, the central intellectual task of statisti-
cal research [Abouzaid et al., 2026]. From a practical standpoint, a key question is whether
current general-purpose LLMs, which are now widely accessible to everyday researchers, can
provide meaningful assistance with proof tasks in day-to-day statistical research. Progress on
this question would have direct implications not only for how statisticians work, but also for
how graduate students are trained, how proof expertise is acquired and shared, and how the
community allocates its intellectual effort. Yet despite the growing presence of LLMs in statis-
tical research workflows, their boundaries as proof assistants remain poorly understood: which
tasks they can meaningfully assist with, and which remain out of reach?
    These open questions in statistical proof provide a useful lens for a broader question, now
facing many areas of expert work, about human-AI collaboration: as AI systems take on sub-
stantial technical reasoning in daily research, how should human expertise adapt? This question
reaches well beyond statistics, into other fields where experts are beginning to delegate technical
execution to AI while remaining responsible for the direction and outcome. Statistical proof is
a demanding and highly structured form of expert cognition, which makes it a clear setting in
which to study this question: it allows us to ask not just whether AI can help, but specifically
where in the process AI assistance is reliable and where human judgment remains essential. The
practical insights that emerge are not a narrow statistical finding; they speak to many expert
domain in which technical work is increasingly being reshaped by human-AI collaboration.
    Although mathematics is a related domain where AI proof assistance has been increasingly
tested, the insights and progress in AI for mathematical reasoning do not transfer automatically
to statistical proof. Statistical proof tasks differ from most mathematical proof tasks in at least
two important respects that determine when and how AI assistance can be effective. First,
statistical problems are inherently closer to real-world applications than most mathematical
problems [Zhao, 2025]. Assumptions in statistical proofs are rarely mathematically simple or
clean; they must be chosen to be both tractable and interpretable, and consistent with the
scientific problems being modeled, a judgment that has no direct analogue in pure mathemat-
ics, where problems typically arrive pre-formulated. Second, statistical proofs less commonly
demand entirely novel proof approaches; instead, they predominantly build on a repertoire of
reusable domain-specific strategies that need to be identified and adapted to each new problem
and context. Effective AI assistance for statistical proof thus requires a different set of capabil-
ities, priorities, and resources from those needed for mathematical reasoning [Chen et al., 2025,
Baba et al., 2025].
    In this paper, we investigate when and how current general-purpose LLMs succeed and


                                                 2
                       Eight research-level statistical proof problems High-dimensional inference Extreme value theory
                                    Four paired case studies from day-to-day statistical research                            Transfer learning        Differential privacy




                         Works today            Current limits           Central gap & human role           Actionable now              Future directions




                  When and why AI works                                                                       When and why AI fails

                Precise problem formulation and clear
                                                                                                         Open-ended problems
                assumptions


                                                                                                         Long reasoning chains or multiple technical
                Targeted strategy hints or references
                                                                                                         components


                Manageable problem scale and reasoning
                                                                                                         Cannot select strategies autonomously
                chain


                                                                                 therefore

                                                                                               Human expertise does not shrink as AI takes on execution. It
         The execution–strategy gap: LLMs can execute a supplied
                                                                                              relocates to where human decision-making matters most, such as
          strategy, but cannot reliably select one on their own.
                                                                                                                formulation and verification.

                                                                                 motivates


                                     Practical insights for AI-assisted daily statistical research
                  Precise problem                                                                                                                    Iterative workflow,
                                                            Targeted guidance                        Proof decomposition
                    specification                                                                                                                      no magic prompt



         Community                                                                    Agentic AI and verification tools
                                    Shared proof strategy repositories                                                                    Training future statisticians
          agenda                                                                               (such as Lean)




Figure 1: Study overview. Four paired case studies covering eight research-level proof prob-
lems from day-to-day statistical research reveal a consistent pattern: current general-purpose
LLMs can execute a proof strategy when one is supplied but cannot reliably select one on their
own. This execution-strategy gap (yellow) emerges from examining when and why AI assistance
works (green, Section 3) and when and why it fails (red, Section 4). The gap carries a parallel
implication for the human role (yellow): AI assistance does not reduce the expertise that sta-
tistical proof demands but relocates it to problem formulation and verification of AI-generated
results, where the bar on human judgment may rise. Together, these findings provide practical
insights for individual statisticians working with these tools today (blue) and motivate a broader
community agenda for future AI developments (amber, dashed).


fail as proof assistants in day-to-day statistical research. Through paired case studies drawn
from active research problems across several areas of modern statistical research, we identify
a consistent pattern: current general-purpose LLMs can assist with substantial components of
statistical proof when the problem is precisely stated and supplemented with targeted guidance,
but become unreliable when the problem is open-ended, requires a long reasoning chain, or
demands simultaneous control of multiple technical components, settings in which the model
must identify and adapt an appropriate strategy on its own. This execution-strategy gap is
currently a primary determinant of whether AI assistance succeeds or fails on research-level
statistical proof tasks. These observations indicate that the demands on human expertise do
not shrink as AI takes on more of the execution; rather, they relocate to the points of greatest
judgment, such as problem formulation and verification of AI-generated results, and may grow
more exacting as experts must make rapid decisions alongside AI tools. These demands may
also grow more exacting, as experts must now make rapid judgments alongside AI tools. Based
on these observations, we discuss practical lessons for individual statisticians, covering problem
formulation, proof decomposition, rapid verification, and the use of targeted guidance, and
outline a broader community agenda: building shared repositories of reusable proof strategies,


                                                                                    3
developing agentic AI and proof assistants, and training future statisticians to interact effectively
with AI tools. As AI systems take on more of the technical execution across many expert
domains, our practical insights from statistical proof provide an early and clear picture of what
this shift demands of human expertise.


2    Study design and key findings
We evaluate AI assistance for statistical proof development through four paired case studies that
together cover eight research-level proof problems. Within each pair, one problem illustrates a
setting in which current general-purpose LLMs provide useful proof assistance, while the other
illustrates a setting in which they become unreliable. Both problems are drawn from the same
broader research context, enabling direct comparison and practical insights into when and how
these tools can be used most effectively in statistical research. Specifically, the four pairs cover
high-dimensional inference, extreme value theory, transfer learning, and differential privacy,
together reflecting the breadth of modern statistical research [Xue and Zhao, 2025, Wainwright,
2019, Ledford and Tawn, 1996, de Haan and Ferreira, 2006, Nelsen, 2006]. Most proof problems
arise from ongoing research projects without publicly available proofs. The only exception is
the high-dimensional inference pair, where a related paper Xue and Zhao [2025] is publicly
available, yet the AI models arrived at correct results through proof strategies distinct from
those in that paper, suggesting the model followed a genuinely different proof route rather than
reproducing it. An overview of the study design is shown in Figure 1.
    For each problem, we evaluated three widely used general-purpose LLMs: GPT-5.4 Think-
ing, Gemini 3.1 Pro, and Claude Opus 4.6. The qualitative conclusions were remarkably consis-
tent across all three models, suggesting that the patterns we identify reflect systematic proper-
ties of current general-purpose LLMs. Unless stated otherwise, we focus our illustrations on the
results of GPT-5.4 Thinking, with model-specific outputs for all three models reported in the
supplementary material. Our goal is not to rank or compare these models, but to extract practi-
cal insights for statisticians working with these tools today, and to outline a broader community
agenda for advancing AI-assisted statistical proof development.
    Our case studies yield the following practical insights into the capabilities and limitations
of current general-purpose LLMs for statistical proof development.

    • Clarity and precision enable success. Current general-purpose LLMs can assist with sub-
      stantial components of research-level statistical proof when the problem is stated clearly,
      the goal is explicit, the reasoning scope is kept at an appropriate scale, and the prompt
      is written in a precise and professional way.

    • Zero-shot prompting is often insufficient. Models frequently struggle when the problem
      depends on newly introduced context [Dou et al., 2026], requires careful control of mod-
      eling assumptions, or demands selection of an appropriate proof strategy. In these cases,
      models often produce plausible-looking but ultimately incorrect or incomplete derivations.

    • Modest guidance can make a substantial difference. Concise proof-strategy hints or
      literature-based methodological references often enable the model to produce a correct
      and rigorous argument where zero-shot prompting had failed. The right guidance does
      not need to be extensive, a few targeted sentences are often enough to redirect the model
      toward a valid proof strategy.

    • Execution is more reliable than strategy selection. Current general-purpose LLMs perform
      considerably better at executing a suitable proof strategy than at identifying one on their
      own. This asymmetry, between what LLMs can execute and what they can identify, is
      the primary manifestation of the execution–strategy gap in practice.


                                                 4
   • Long reasoning chains and weak guidance lead to failure. AI reliability decreases substan-
     tially when the argument requires a long reasoning chain, simultaneous control of multiple
     technical components, or decision making under weak guidance. In these settings, models
     tend to introduce convenient but unjustified intermediate assumptions, shift the target of
     the proof, or produce notation-heavy derivations that obscure rather than illuminate the
     main argument.
    Together, these observations suggest that current general-purpose LLMs can be meaning-
fully integrated into statistical proof development within a structured workflow that specifies
the problem clearly and professionally, states assumptions explicitly, decomposes the proof
into manageable problems, and introduces targeted guidance when necessary. They also point
to a broader need in the statistics community for explicit and accessible resources that or-
ganize reusable proof strategies by research area, since shared repositories of proof strategies
and literature-based templates could improve both human and AI-assisted proof development.
For education, these findings suggest that training future statisticians should include not only
mathematical theory but also effective interaction with AI tools: learning to formulate statistical
problems precisely, specify context and assumptions, evaluate whether an AI-generated proof
uses an appropriate strategy, provide corrective guidance when it does not, and distinguish a
plausible-looking but inaccurate derivation from a rigorous one.
    Beyond these specific lessons, our case studies point to more general insights about the role
of human expertise in human-AI collaboration for statistical proof.
   • Defining a good proof task is a growing bottleneck. As AI lowers the technical barrier
     to executing a proof, the difficulty shifts to what AI currently cannot do: knowing what
     should be proved in a scientific context, why that problem is important, what assumptions
     are appropriate, and what result would be scientifically meaningful. This requires a chain
     of human decisions, from selecting a worthwhile research question, to formulating it as a
     precise statistical problem, to conveying that precision to the AI model in efficient human-
     AI conversations. Human researchers who can make these decisions fluently extract more
     value from AI assistance and direct it toward more meaningful research outputs.
   • Live human verification makes the workflow productive. In proof development, the realis-
     tic workflow is iterative, closer to an engaged human-AI conversation than to a one-shot
     prompt query. At every step, the human user must rapidly diagnose whether the AI-
     generated proof is valid. This diagnosis is often not a matter of mathematical correctness
     alone; it is about whether the proof answers the intended question, whether unjustified
     assumptions have been quietly introduced, and whether the result is sharp and scientifi-
     cally useful. A good human expert can often tell quickly whether a generated proof is on
     the right track, has changed the target, or has produced a result that is mathematically
     valid but scientifically weak. This kind of rapid proof triage is what makes the iterative
     workflow actually work: an AI model can only be corrected by guidance if a human al-
     ready knows what went wrong. Consistent with the first point, AI does not reduce the
     expertise statistical proof demands; it relocates and intensifies it.
    The contributions of this paper are therefore fourfold. First, we provide a set of paired
research-level case studies that characterize both productive and unreliable scenarios for general-
purpose LLMs as proof assistants in statistical research. Second, we identify an execution-
strategy gap that helps explain when AI assistance succeeds and fails, and show that this
gap reflects a broader pattern: AI does not reduce the human expertise that statistical proof
demands, but relocates it to where human decision-making matters most. Third, we extract
practical insights for integrating AI tools into daily statistical research workflows. Fourth, we
outline a broader community agenda and highlight the opportunities and challenges this shift in
human-AI collaboration creates. We view this as an evolving effort and will continue to update
our findings as additional proof problems, AI models, and tools become available.

                                                5
3      When and how AI assistance succeeds
Despite coming from different areas of statistical research, the four successful cases reveal a con-
sistent pattern: AI assistance works best when the proof task is precisely scoped, the modeling
assumptions are made explicit, and the reasoning chain is kept at a manageable scale. In three
of the four cases, zero-shot prompting, asking the model to solve the problem directly from the
problem statement alone, without any additional domain-specific guidance, was insufficient. In
those cases, however, relatively modest and targeted guidance, such as a short strategy hint, a
key literature reference, or an important clarifying instruction, was enough to redirect the model
toward a correct and rigorous argument. These cases illustrate that the barrier to effective AI
assistance in statistical proof is often not mathematical difficulty alone, but the availability of
the right proof strategy at the right moment.

3.1      Variance calculation in high-dimensional inference
Our first example comes from linkage disequilibrium score regression (LDSC), a widely used
method for estimating trait heritability from genome-wide association study (GWAS) summary
statistics [Bulik-Sullivan et al., 2015]. The specific task is a technical problem in the high-
dimensional asymptotic analysis of LDSC: computing the exact finite-sample variance of the
oracle LDSC estimator, where “oracle” means that the linkage disequilibrium (LD) scores are
treated as known. This problem is mathematically nontrivial but sufficiently self-contained,
making it a natural task of whether AI can carry out a rigorous derivation when the statistical
setting is stated clearly. The prompt and problem setup are summarized in the following boxes,
with full derivations provided in the supplementary material.
     Zero-shot prompt 1
     You are an expert in mathematical statistics and genetics. The following is a research-
     level problem. Please make the best effort to provide a rigorous and complete formal
     proof for the problem.
     Problem: The problem stated in Problem 1
     Emphasize: (i) The genetic effects are fixed. Do NOT assume that they are random
     effects. (ii) Please define notations carefully and use only natural notations. (iii) Write
     the output in LaTeX language using the standards of rigor and scholarship that prevail
     in the mathematical literature.

    Problem 1
    This is a sub-problem of the high-dimensional inference for the linkage disequilibrium score
    regression (LDSC) in the genome-wide association studies (GWAS).
    Suppose that we have a GWAS cohort with X ∈ Rn×p consisting samples of p genetic
    variants and y ∈ Rn consisting samples of the outcome.          P Let Σ be the covariance matrix
    of the p genetic variants. Define the LD score ℓj = pi=1 Σ2ji and the estimated marginal
    covariance baj = n−1 · XjT y, where Σji is the (j, i) element of Σ and Xj is the j-th column
    of X for i = 1, . . . , n and j = 1, . . . , p. Let w
                                                        b = (b             a2p )⊤ , ℓ = (ℓ1 , . . . , ℓp )⊤ , and
                                                             a21 , . . . , b

                                                 1 ⊤                   1 ⊤
                                        µℓ =      1 ℓ,         µ̂w =    1 ŵ.
                                                 p p                   p p

    Define the (centered) “oracle” LDSC estimator

                                                 (ℓ − µℓ 1p )⊤ (ŵ − µ̂w 1p )
                                        σ̃α2 =                                .
                                                  (ℓ − µℓ 1p )⊤ (ℓ − µℓ 1p )


                                                           6
  We assume that
                                               y = Xα + ϵ,
  where α = (α1 , . . . , αp )T are unknown fixed genetic effects and ϵ = (ϵ1 , . . . , ϵn )T consists
  of mean-zero normal random error terms with variance σϵ2 . We also assume that all the
  genetic variants follow a multivariate normal distribution with a block-diagonal structured
  covariance matrix.
  Calculate the variance of σ̃α2 . Write down the final results in terms of n, Σ, ℓ, α, and σϵ2 .

    The model produced a complete derivation whose final variance formula agrees with the
result we derived independently in Xue and Zhao [2025]. Notably, despite the public availability
of our paper, the AI-generated proof arrived at the correct answer through a different proof
strategy, suggesting the result was not a simple retrieval of the published work.
   AI-generated proof 1
   Final variance formula. Let
                                                                     p
                                                                     X
                        c = ℓ − µℓ 1p ,      C = diag(c),      ∆=          (ℓj − µℓ )2 ,
                                                                     j=1

   and
                                             τ 2 = α⊤ Σα + σε2 .
   Then
                               
                            1 8(n + 2)(n + 3) 2 4(n + 2)(n + 4) 2   8(n + 2) 2
                  σα2 ) =
              Var(e                           B +              τ R+         τ BS
                            ∆2         n3             n3               n3
                                                   
                              2(n + 2) 4    2
                            +         τ U + 3 τ 4S2 ,
                                 n3        n

   where
                                              B = α⊤ ΣCΣα,
                                                         α⊤ ΣCΣα
                                          S = tr(CΣ) −           ,
                                                            τ2
                                                            (α⊤ ΣCΣα)2
                                  R = α⊤ ΣCΣCΣα −                      ,
                                                                 τ2
                                          2 α⊤ ΣCΣCΣα (α⊤ ΣCΣα)2
                            U = tr (CΣ)2 −                     +              .
                                                     τ2               τ4
   This is the exact finite-sample variance of the centered oracle LDSC estimator under the Gaussian
   design model with fixed effects α.

    This example illustrates that zero-shot prompting can be sufficient for research-level statis-
tical proof when the task is precisely scoped and the prompt is written with care. Although
zero-shot prompting ultimately succeeded here, the experience of getting there yields several
practical lessons, and shows that human expertise plays a strong role during problem formula-
tion. First, the problem must be stated precisely and the relevant assumptions made explicit.
When the setup is underspecified, the model tends to introduce additional assumptions that
are mathematically convenient but inconsistent with the intended statistical framework and
scientific context. Second, when the intended modeling framework differs from what dominates
the relevant literature, the prompt must do more than state the correct assumption. It must
also explicitly rule out the incorrect default. Specifically, the critical assumption here was that
the genetic effects are fixed rather than random. Because the LDSC literature is predominantly
developed under a random-effects framework [Bulik-Sullivan et al., 2015, Jiang et al., 2023],


                                                     7
the model defaulted to that framework even when a fixed-effects setup was provided in the
prompt, producing a derivation that appeared superficially reasonable but was answering the
wrong question. The fixed-effects assumption is essential here because our goal is an exact
finite-sample variance, which requires treating the genetic effects as deterministic rather than
stochastic. Explicitly instructing the model to treat the genetic effects as fixed, and to avoid
the random-effects framework, was necessary to obtain a correct derivation. This is a subtle
but serious pitfall: for researchers less familiar with the distinction between fixed and random
effects in this context, an AI-generated proof under the wrong framework may appear valid on
the surface while being fundamentally misaligned with the intended problem.

3.2   Scaling invariance of angular tail dependence in copulas
Our second example comes from an ongoing project on copulas [Sklar, 1959] and angular tail de-
pendence, which is representative of a broad class of questions in extreme value theory [de Haan
and Ferreira, 2006]. The task is to prove that a limit-based measure of lower-tail behavior [Joe,
2014, Hua and Joe, 2011, Su and Hua, 2017], designed to quantify dependence along different
angular paths toward the tail, remains invariant with respect to a scaling parameter under suit-
able regularity conditions. The main difficulty here is strategic rather than computational. The
proof requires choosing an appropriate way to compare limits and identifying the regularity con-
ditions needed to justify each step. This is the kind of judgment that current general-purpose
LLMs struggle to exercise without guidance. Yet as we show below, a short and targeted
proof-strategy hint is often enough to resolve it.
    The problem setup is given in the following box. The quantity κL (δ, γ; C) is designed to
capture lower-tail behavior along an angular path indexed by δ, while allowing a scale pertur-
bation indexed by γ. Establishing invariance with respect to γ is a necessary theoretical step
before κL can be interpreted as a coherent and well-defined measure of angular tail dependence.

  Problem 2
  For a copula C on [0, 1]2 and parameters γ > 0, δ ∈ (0, 2), define

                                                log C γuδ , γ −1 u2−δ
                                                                      
                             κL (δ, γ; C) = lim                         ,
                                            u↓0        log u

  whenever the limit exists. The claim to be proved is that under suitable regularity condi-
  tions, κL (δ, γ; C) does not depend on the choice of scaling parameter γ for all δ ∈ (0, 2).

    To help the model engage with this problem correctly, we provided not only the specific
mathematical question but also the surrounding scientific context, clarifying the motivation of
the problem, its role in the broader research project, and why the claimed invariance property
is important. They are summarized in the box below.

  Context 1
  We propose a new class of copulas that can account for angular full-range tail dependence,
  capturing not only asymmetry but also non-exchangeability. Our proposed copula, denoted
  by CPM , is defined explicitly in the supplement. To theoretically analyze this new model
  class, we first need a principled measure of tail behavior that can vary with the direction
  (angle) of approach to the tail. That is the motivation of how we define κL (δ, γ; C). This
  quantity is a generalized lower-tail dependence coefficient [Hua and Joe, 2011]. Our intu-
  ition is that, when the limit exists, the resulting angular tail behavior should primarily be
  governed by the direction parameter δ, and should not depend on the scaling parameter γ.
  We therefore seek (i) regularity conditions under which such scaling invariance holds and



                                                   8
  (ii) a rigorous proof under those conditions.

   We first provided the model with the problem context, the formal statement to be proved,
and a brief prompt instruction.
   Zero-shot prompt 2
   “You are an expert in statistical methodology and mathematical reasoning. Your task is
   to produce a full formal proof for a problem in an ongoing research project.
   Problem: Prove the claim stated in Problem 2. In addition, verify that the proposed
   copula CPM described in Context 1 also satisfies this claim.
   Context: The background provided in Context 1.
   Given the problem and context above, give a full formal proof for the problem. State any
   assumptions that are needed. Justify each step and give the complete proof in LATEX.”

    Without any proof-strategy guidance, the model produced a lengthy and seemingly well-
structured derivation. However, it adopted a proof technique rarely used for problems of this
type and did not fully engage with the newly introduced research context, leading to several
non-rigorous steps, most notably, failing to state the regularity conditions necessary to justify
key arguments. This zero-shot attempt therefore did not constitute a valid proof. Notably, this
failure was not algebraic: the model made no obvious calculation errors, but did not recognize
which proof approach was appropriate for this statistical problem. The main limitation was
thus strategic rather than computational.
    The standard approach for establishing this type of invariance result is to bound the differ-
ence between the two quantities of interest by decomposing it using the triangle inequality and
then invoking suitable regularity conditions to control each term [Resnick, 2007], an approach
that statisticians working in extreme value theory would recognize as natural and well-suited
to this problem. The model did not adopt this strategy, instead pursuing a less natural and ul-
timately non-rigorous route. This observation motivated us to supplement the original prompt
with two concise proof-strategy hints pointing toward the standard approach, as shown in the
box below.
   Guidance prompt 1

   Guidance: To prove that κL (δ, γ; C) does not depend on γ, it is enough to show that,
   for any γ, γ̃ > 0, κL (δ, γ; C) = κL (δ, γ̃; C). That is, we need to prove the equality of the
   two limits corresponding to γ and γ̃.
   (i) To prove equality of these two limits, consider to show that there exists u0 ∈ (0, 1)
   such that for all 0 < u < u0 , the absolute value of the difference of the corresponding
   pre-limit quantities is less than or equal to ε for every ε > 0;
   (ii) To use the triangle inequality by adding and subtracting terms inside the absolute
   value, bounding each term, and stating essential assumptions of the limits (such as type
   of the convergence) based on our research context and problem.
   User: “Give a full formal proof. Justify each step and state any assumptions you use”

    With these two strategy hints, the model produced a correct and rigorous proof, decomposing
the difference into three terms and bounding each by ε/3, with appropriate regularity conditions
stated explicitly. The same model that had produced a non-rigorous derivation under zero-
shot prompting delivered a correct and complete proof once the right strategy was indicated,
demonstrating that the bottleneck was not mathematical ability but strategy identification.
    This example illustrates a clear instance of the execution–strategy gap: the bottleneck was
not mathematical execution but strategy identification. A key reason the zero-shot attempt


                                                  9
failed is that the model did not genuinely understand the research context. It processed the
problem statement and background but could not situate the proof task within the broader
landscape of extreme value theory, and therefore had no principled basis for selecting an appro-
priate proof strategy. This is where human expertise becomes essential. A statistician familiar
with the domain can recognize immediately which proof approach is natural for a problem of
this type, and supplying that insight in a few targeted sentences can change the entire outcome.
Conversely, without such guidance, the model may pursue a plausible-looking but ultimately
invalid route, producing a derivation that appears well-structured on the surface but fails to
meet the standards of statistical rigor. This points to a practical workflow for statisticians:
rather than asking the model to develop a proof from scratch, it may be more effective to first
identify the appropriate proof strategy, drawing on domain expertise and familiarity with the
statistical literature, and then provide that strategy as targeted guidance before asking the
model to execute.

3.3   Bounding the prediction risk in transfer learning
Our third example comes from an ongoing project on transfer learning under a high-dimensional
linear regression framework [Gu et al., 2025, Li et al., 2022]. The goal is to derive an asymptotic
upper bound for the prediction risk of a transfer learning estimator that leverages information
from a source site to improve prediction at a target site, while accounting for cross-site hetero-
geneity and feature mismatch. Deriving a sharp and informative bound, rather than a valid but
loose one, is the central challenge, as an overly conservative bound provides little insight into
how the estimator’s performance depends on the key problem parameters. The specific context
and setup of this problem are described in the boxes below.

  Context 2
  We consider a transfer learning setting consisting of a target site t and a source site s. For
  each site m ∈ {t, s}, the response y (m) ∈ R and the covariate vector x ∈ Rp satisfy the
  linear model
                                      y (m) = x⊤ β (m) + ε,
  where β (m) ∈ Rp is a random coefficient vector, x ∼ N (0, Σ), and ε ∼ N (0, σ 2 ) is indepen-
  dent of x. The dimension p increases to infinity as the sample size n increases.

  Problem 3
  Suppose that we only observe the subvector xR(t) , indexed by R(t) ⊆ [p] in the target site.
        (t)
  Let XR(t) ∈ Rnt ×pt and Y (t) ∈ Rnt denote the observed design matrix and response vector,
  respectively, where pt = |R(t)| and nt is the target-site sample size.

  Given an estimator β̂ (s) of the source-site coefficient vector β (s) , we define a transfer learning
              (t)
  estimator ω̂TL for the coefficient vector corresponding to the observed target features xR(t)
  by                                                                               
                      (t)              1     (t)     (t)    2                 (t) 2
                    ω̂TL := arg min       ∥Y − XR(t) ω∥2 + λTL ∥ω − ω̂s ∥2 ,
                                   ω   nt
              (t)
  where ω̂s = Φ(t)β̂ (s) , and λTL ≥ 0 is a tuning paramete. Here Φ(t) ∈ Rpt ×p is a
  matrix such that Φ(t) i,j∈R(t) = Ipt with Ipt ∈ Rpt ×pt denoting an identity matrix, and
   (t)                         −1
   Φ i∈R(t), j∈[R(t)]c = ΣR(t)       ΣR(t),[R(t)]c , where [R(t)]c = [p] \ R(t) denotes the set of
  features unobserved at the target site.




                                                   10
  For a new independent test observation (x̃R(t) , ỹ (t) ) from the target site, we define the
                      (t)
  predictive risk of ω̂TL as
                                          h                              i
                                    (t)                     (t) 2  (t)
                            rpred ω̂TL = E ỹ (t) − x̃⊤
                                                      R(t) ω̂TL     XR(t) .

  Our goal is to derive an asymptotic upper bound for this predictive risk, as sharp as
  possible in the regime nt , p → ∞, together with the corresponding optimal choice of λω ,
  under the following assumptions.

  High-Dimensional Assumption: The full-feature dimension p and the observed-feature
  dimension pt go to infinity as nt goes to infinity, with p/nt → γ ∈ (0, ∞) and
  pt /nt → η ∈ (0, ∞).

  Random Regression Coefficients Assumption: For each m ∈ {s, t}, the regression coefficient
  vector β (m) is random with E[β (m) ] = 0 and Cov[β (m) ] = (αm
                                                                2 /p)I , where α
                                                                      p         m ̸= 0. In
                   (t) (s)
  addition, Cov(β , β ) = (ραt αs /p)Ip , where ρ ∈ (0, 1].

  Source
        Estimation Error Assumption:                  The source estimator β̂ (s) satisfies
  λmax E (β̂ (s) − β (s) )(β̂ (s) − β (s) )⊤    ≤ C U /p uniformly as (nt , p) → ∞, for some
                                             

  constant C U > 0. Here λmax (·) denotes the largest eigenvalue.

    We began with a zero-shot prompt providing the background context and problem setup,
as shown in the box below.
   Zero-shot prompt 3
   You are an expert in statistical methodology and mathematical reasoning. Your task is
   to produce a full formal proof for a problem in an ongoing research project.
   Background: The background introduced in Context 2
   Problem: The problem stated in Problem 3.
   Give a full formal proof for the problem. You need to state assumptions and regularity
   conditions that you use. Justify each step and give the complete proof in LATEX.

    Under this zero-shot prompt, the model decomposed the predictive risk and attempted to
bound each term individually, a broadly reasonable high-level approach. However, the resulting
bound was loose and uninformative. Two specific failures drove this outcome. First, for trace
terms that admit an exact closed-form expression, the model instead applied a crude spectral
bound, such as ΣR(t),R(t) ⪯ CΣ Ipt , where CΣ is the largest eigenvalue of ΣR(t),R(t) . Second, for
terms whose high-dimensional limits can be calculated exactly using tools from random matrix
theory [Bai et al., 2010], the model did not attempt the calculation and instead simply assumed
the limits as given. Overall, the result was a bound expressed in terms of unspecified quantities,
making it difficult to understand how prediction risk depends on the key problem parameters,
such as sample size, dimension, cross-site correlation, and feature mismatch.
    We then explored whether the model could learn directly from existing literature that ad-
dresses similar problems using established domain principles. To this end, we supplemented
the original prompt with targeted guidance drawn from two closely related papers. The first
provided tools for exact trace calculations and deterministic equivalent approximations in high-
dimensional settings [Dobriban and Wager, 2018]. The second provided a risk decomposition
and bounding strategy specifically developed for transfer learning estimators of this type [Gu
et al., 2025]. Notably, we did not reproduce the arguments from these papers; we simply named


                                                  11
them and indicated how they were relevant to the problem at hand.
   Guidance prompt 2

   Guidance: Use the techniques listed below. (i) The limiting trace / deterministic equiv-
   alent calculations in Dobriban and Wager (2018), High-Dimensional Asymptotics of Pre-
   diction: Ridge Regression and Classification. (ii) The predictive-risk decomposition and
   bounding strategy for the L2 transfer learning estimator in Gu, Han, and Duan (2025),
   Robust Angle-Based Transfer Learning in High Dimensions.
   Given the background, problem, and guidance above, give a full formal proof for the
   problem. You need to state assumptions and regularity conditions that you use. Justify
   each step and give the complete proof in LATEX.

     With this literature-based guidance, the model’s performance improved substantially. Rather
than applying loose spectral bounds throughout, it retained exact expressions for the terms that
admit closed-form limits and applied bounding only where genuinely necessary, specifically, for
the term involving source estimation error, where an exact expression is not available. The
resulting asymptotic upper bound was sharper, more interpretable, and richer in statistical
insight than the zero-shot results.
     This example highlights an important and practical lesson: in statistical proof develop-
ment, the usefulness of an AI-generated result depends not only on its correctness but also on
whether it leads to sharp and statistically meaningful conclusions. A loose but valid bound is
not equivalent to a sharp and informative one: the former may be mathematically defensible
but scientifically uninformative, failing to reveal how the quantity of interest depends on the
key problem parameters. The model could bound terms but could not judge which admitted a
closed-form limit and which could only be bounded, a distinction that requires domain exper-
tise. In our example, providing two targeted literature references was enough to supply that
judgment, transforming a valid but uninformative derivation into one that is both rigorous and
scientifically useful. Recognizing that a bound was loose rather than sharp, despite being math-
ematically valid, currently requires a human judgment of this kind: an expert who can quickly
tell that a formally correct result is nonetheless scientifically unsatisfying, and who knows which
literature would resolve the gap.

3.4   Equivalence of privacy formalisms in differential privacy
Our fourth example comes from an ongoing project on the exact relationships among different
privacy formalisms in differential privacy (DP). Several standard languages exist for quantify-
ing privacy guarantees, including Rényi-DP [Bun and Steinke, 2016], (ε, δ)-DP [Dwork et al.,
2006a,b], and f -DP [Dong et al., 2022, Su et al., 2025]. Each formalism arises from a different
theoretical perspective and characterizes the privacy level through an exact curve, but these
curves are indexed by different parameters and encode privacy from different viewpoints. Briefly,
the Rényi-DP curve records the Rényi divergence as a function of the order α, and thus defines
privacy through a family of divergence comparisons between neighboring output distributions.
The (ε, δ)-DP curve records, for each threshold ε, the smallest admissible failure probability δ,
so it defines the privacy through the tail behavior of the privacy loss. The f -DP curve is indexed
by the type-I error level and gives the optimal type-II error for testing between two neighboring
output distributions, defining privacy from a statistical distinguishability perspective.
    The proof task is to investigate whether the full exact Rényi-DP curve determines the full
exact (ε, δ)-DP curve and the full exact f -DP curve, and whether the converse implication
holds. This question is natural and important because the same mechanism is often analyzed
with different DP languages in the literature. For example, one may derive Rényi-DP to an-
alyze composition, convert to (ε, δ)-DP for reporting guarantees, and use f -DP to interpret


                                                12
distinguishability [Abowd et al., 2022]. A precise understanding of whether the corresponding
full exact curves contain the same information is therefore necessary for translating privacy
guarantees across formalisms without loss of information. Specifically, we consider privacy
additive-noise mechanisms with centered symmetric noise, of the form

                                       M (x) = A(x) + Z,

where A is a deterministic algorithm and Z follows a centered symmetric noise distribution,
such as a Gaussian or Laplace distribution [Dwork et al., 2006a,b, McSherry, 2010]. Here Z
is the noise added to protect privacy. The centered symmetry of Z is not merely a technical
convenience; it encodes a structural property of the mechanism that, as we show below, plays a
decisive role in determining what privacy information can be recovered across formalisms. The
problem statement, context, and prompt provided to the model are shown in the boxes below.

  Problem 4
  Does the full exact Rényi-DP curve imply the full exact (ε, δ)-DP curve and f -DP curve?
  Does the converse implication hold?

  Context 3
  Consider an additive-noise mechanism M (x) = A(x)+Z, where A is deterministic and Z ∼ ν
  is a centered symmetric noise distribution. Let L(X) denote the probability law of a random
  variable X. For neighboring datasets, define P = L(M (x)) and Q = L(M (x′ )). We want to
  compare the information contained in the full exact Rényi-DP curve {Dα (P ∥Q) : α > 1}, the
  full exact (ε, δ)-DP curve {δ(ε) : ε > 0}, and the full exact f -DP curve {f (α) : 1 ≥ α ≥ 0}.

   Zero-shot prompt 4
   “You are an expert in differential privacy and theoretical computer science. Your task is
   to produce a full formal proof for a problem in an ongoing research project.
   Problem: The problem stated in Problem 4.
   Context: The background provided in Context 3.
   Given the problem and context above, provide a rigorous mathematical answer. You
   need to state the assumptions and regularity conditions that you use, justify each step
   carefully, and give a complete proof in LATEX.”

     Under the zero-shot prompt, the model produced a partially correct answer. The forward
direction was handled well: the model correctly argued that the full exact Rényi-DP curve
contains enough information to recover the corresponding exact (ε, δ)-DP curve and the exact
f -DP curve, successfully proving one side of the desired equivalence. The failure occurred in the
converse direction. Rather than exploiting the specific structure of the additive-noise mechanism
with centered symmetric noise, the model treated the reverse implication as a generic question
about arbitrary pairs of neighboring output distributions. Under that generic formulation, it
concluded that the one-sided (ε, δ)-DP profile is strictly weaker and does not determine the
other two curves, a conclusion that is reasonable in a general setting but misses the sharper
result available here. Because the noise distribution is centered and symmetric, the one-sided
(ε, δ)-DP profile in fact contains enough information to recover the full privacy description,
making it equivalent to the full exact Rényi-DP and f -DP curves in this setting.
     To address this, we provided a short follow-up prompt explicitly directing the model back to
the overlooked centered-symmetry assumption and asking it to reconsider the conclusion about
one-sided versus two-sided privacy profiles, as shown in the box below.



                                               13
    Guidance prompt 3
    “Be careful that Z ∼ ν is a centered symmetric noise distribution, so that reconsider your
    conclusion on the one-sided and two-sided (ε, δ)-DP curve {δ(ε)}.”

   With this targeted guidance, the model produced a correct and complete proof, concluding
that

    1. For arbitrary (P, Q), the usual one-sided profile {δ(ε) : ε ≥ 0} is strictly weaker than the
       full exact Rényi-DP and f -DP curves; and

    2. In the additive-noise setting with centered symmetric noise, the full exact Rényi-DP curve,
       the full exact f -DP curve, the full exact two-sided (ε, δ)-DP curve, and the usual one-sided
       exact profile {δ(ε) : ε ≥ 0} are all equivalent.

     Unlike the other case studies, the limitation here was not a missing proof strategy or unfa-
miliar technique, but an incomplete use of the problem’s key assumptions, leading the model
to answer a more general question than the one being asked. In privacy protection, symmetry
assumptions often encode nontrivial information about the relationship between neighboring
output distributions, and this information can significantly affect what can be recovered from a
given exact privacy curve [Vinterbo, 2022, Balle et al., 2018]. Overlooking such an assumption
therefore does not merely weaken the proof; it changes the question being answered and the con-
clusion that can be drawn. This kind of incompleteness can be serious in research: an argument
may be fully correct in a general setting and yet inadequate for the actual research question,
because it misses a structural property that yields a stronger and more specific conclusion.
Recognizing when a proof is answering the wrong question, and identifying which assumption
restores the correct result, requires the kind of statistical judgment that current general-purpose
LLMs do not reliably exercise on their own. Yet this is also where human expertise can intervene
efficiently: recognizing that the model had quietly answered a more general question than the
one posed, a downstream diagnostic judgment rather than a strategic correction, took only a
moment for a human expert. As this example demonstrates, a single short prompt highlighting
the overlooked assumption was enough to redirect the model toward the correct and complete
proof, turning an inadequate derivation into a rigorous one with minimal effort.


4     When and how AI assistance fails
The four failure cases share a complementary pattern to the successful cases: current general-
purpose LLMs break down most severely when the proof task is open-ended, the reasoning
chain is long, or the problem requires simultaneous control of multiple technical components.
In these settings, the execution–strategy gap widens: the model not only struggles to identify
an appropriate proof strategy but also fails to sustain a coherent reasoning path long enough to
reach a valid conclusion. Together, these cases reveal the current boundaries of general-purpose
LLMs as proof assistants in statistical research, and point to the kinds of advances that would
be needed to push those boundaries further. They also sharpen the role of human expertise:
as the model’s own derivations grow less reliable, the burden of recognizing where and why an
argument has gone wrong falls more heavily on the human collaborator.

4.1    Asymptotic normality in high-dimensional inference
Our first failure case follows directly from the successful case in Section 3.1. Having shown that
AI models can handle a precisely scoped problem, computing the exact finite-sample variance
of the oracle LDSC estimator, we now ask a more demanding question: can the model directly
establish the asymptotic normality of the full LDSC estimator with given LD scores? This

                                                 14
problem is substantially harder for at least two reasons. First, it requires a much longer reason-
ing chain, spanning multiple steps including variance calculation, denominator concentration,
linearization of the ratio estimator, and a final normal approximation step. Second, it requires
simultaneous control of multiple technical components that must be coordinated carefully across
the full argument. The specific problem setup is described in the box below.

  Problem 5
  Suppose that we have a GWAS cohort with X ∈ Rn×p consisting samples of p genetic
  variants and y ∈ Rn consisting samples of the outcome. In addition, we have a reference
  panel with Z ∈ Rnr ×p consisting nr samples of the p genetic variants. The GWAS cohort
  samples and reference panel samples are independent. Let Σ be the true covariance matrix
  of the p genetic variants, P  and Σ    b be the corresponding sample covariance matrix. Define the
                                    p
  estimated LD score ℓ̂j = i=1 Σ             ji                                      aj = n−1 · XjT y,
                                           b 2 and the estimated marginal covariance b
  where Σ b ji is the (j, i) element of Σ       b and Xj is the j-th column of X for i = 1, . . . , n and
  j = 1, . . . , p. Let w
                        b = (b2           ap ) , ℓ̂ = (ℓ̂1 , . . . , ℓ̂p )⊤ , and
                             a1 , . . . , b2  ⊤


                                             1 ⊤                    1 ⊤
                                    µℓ̂ =     1 ℓ̂,         µ̂w =    1 ŵ.
                                             p p                    p p

  Define the (centered) LDSC estimator

                                             (ℓ̂ − µℓ̂ 1p )⊤ (ŵ − µ̂w 1p )
                                    σ̂α2 =                                    .
                                             (ℓ̂ − µℓ̂ 1p )⊤ (ℓ̂ − µℓ̂ 1p )

  We assume that
                                                y = Xα + ϵ
  where α = (α1 , . . . , αp )T are unknown fixed genetic effects and ϵ = (ϵ1 , . . . , ϵn )T represent
  mean-zero normal random error vectors. We also assume that all the genetic variants follow
  a multivariate normal distribution with a block-diagonal structured covariance matrix.
  Please show the asymptotic normality of σ̂α2 as n, p → ∞.

    We first applied a zero-shot prompt, then supplemented it with targeted guidance referencing
two key papers, one for variance calculation and one for the asymptotic normality step, as shown
in the boxes below.
   Zero-shot prompt 5
   You are an expert in mathematical statistics and genetics. The following is a research-
   level problem. Please make the best effort to provide a rigorous and complete formal
   proof for the problem.
   Problem: The problem stated in Problem 5
   Emphasize: (i) The genetic effects are fixed. Do NOT assume that they are random
   effects. (ii) Please define notations carefully and use only natural notations. (iii) Write
   the output in LaTeX language using the standards of rigor and scholarship that prevail
   in the mathematical literature.




                                                       15
   Guidance prompt 4

   Guidance: (i) For variance calculation, consider using Proposition S1 in the supplement of
   the paper “Dicker, L. H. (2014). Variance estimation in high-dimensional linear models.
   Biometrika, 101(2), 269-284.”, which is attached. (ii) For asymptotic normality, consider
   using Theorem 2.2 in the paper “Chatterjee, S. (2009). Fluctuations of eigenvalues and
   second order Poincaré inequalities. Probability Theory and Related Fields, 143(1), 1-40.
   (https://arxiv.org/abs/0705.1224)”.

     We tested all three models under the combined prompt. Despite the targeted guidance, all
three produced polished-looking derivations that fell short of what would be required for use in
statistical research. The Gemini 3.1 Pro output was the weakest. It provided only a high-level
proof sketch, introduced additional scaling assumptions on the fixed effects that were not part
of the original problem, and invoked Chatterjee’s theorem [Chatterjee, 2009] using heuristic
derivative bounds rather than verified calculations. Several key claims, including the order of
the variance, the concentration of the denominator of the LDSC estimator, and the derivative
bounds needed to apply Chatterjee’s theorem, were asserted with minimal justification. The
argument had the right overall shape but remained far from a complete proof.
     The GPT-5.4 Thinking and Claude Opus 4.6 outputs were substantially more polished, but
still not ready for use in a research paper. Both models identified a plausible high-level pathway:
linearize the ratio estimator, reduce the problem to a Gaussian fluctuation statement, and apply
Chatterjee’s theorem to conclude asymptotic normality. However, the main problem is that the
most difficult parts of the argument were handled by introducing additional assumptions rather
than being derived from the original setup. For example, in the GPT-5.4 Thinking output, the
proof assumed the variance of the LD score estimators rather than deriving it from the model, a
quantity that should follow from the setup, not be taken as given. The order of several derived
bounds and estimates was also claimed without justification, leaving the final application of
Chatterjee’s theorem insufficiently supported. The Claude Opus 4.6 output went further but
changed the target of the problem: rather than working directly with the original estimator, it
introduced a pseudo-true centering quantity σα,0 2 defined through the estimated LD scores and

proved asymptotic normality around that modified target, shifting part of the original difficulty
into new definitions and assumptions. Some crucial steps in the martingale-CLT argument were
also only justified informally.
     Across all three models, a consistent pattern emerged: once the reasoning path becomes
long enough, the model tends to preserve the overall structure of a plausible proof by introduc-
ing convenient intermediate assumptions, auxiliary targets, or black-box asymptotic conditions
at the points where the real derivation becomes most difficult. The proof appears complete
on the surface, but the hardest steps have been quietly replaced by unjustified assumptions.
Combined with Section 3.1, this example suggests that current general-purpose LLMs are con-
siderably more reliable on well-specified isolated problems than on full end-to-end asymptotic
arguments. The execution–strategy gap widens as the reasoning chain lengthens: the model
not only struggles to identify the right overall strategy but also loses the ability to sustain a
rigorous argument across all the steps needed to reach a valid conclusion.

4.2   Strategy selection from weak cues in copula tail dependence
Section 3.2 showed that two short proof-strategy hints transformed a failed zero-shot attempt
into a correct and rigorous proof. This raises a natural question: how much of that work are
the hints actually doing? Could the model identify an appropriate strategy on its own if given
weaker but still domain-relevant cues, without being told explicitly what to do?
    To explore this, we returned to the same copula problem from Section 3.2, but this time
replaced the explicit strategy hints with a short list of domain-relevant keywords: “copula, tail


                                                16
dependence, extreme value theory, and tail dependence coefficient”. We asked the model to use
these keywords, together with the problem statement and research context, to first propose its
own proof strategy and then carry it out. The prompt is shown in the box below.
   Keyword-guided prompt 1
   “You are an expert in statistical methodology and mathematical reasoning. Use the
   problem statement, the background context, and the given domain keywords to identify
   a proof strategy and then provide a full formal proof.
   You must output two labeled sections:
   Strategy: A short paragraph describing the proof strategy.
   Proof: A complete formal proof. State all assumptions and regularity conditions explicitly,
   justify each step, and prove the exact claim stated in the problem.”
   Problem: The problem stated in Problem 2.
   Context: The background provided in Context 1.
   Keywords: copula, tail dependence, extreme value theory, tail dependence coefficient.
   Use the exact headers Strategy: and Proof:.”

    The model did propose a strategy below, but not the right one. Briefly, it suggested using
the copula’s coordinatewise monotonicity to sandwich the copula along the target path between
two fixed multiplicative reparametrizations of u, then applying a squeeze argument to conclude
the desired invariance. This approach does not invoke the triangle inequality or the uniform
convergence arguments that the correct proof requires, and the resulting formal derivation
introduced unverified assumptions and non-rigorous steps. In summary, the keywords pointed
the model toward the right research area but provided no principled basis for selecting among
the proof strategies available within that area.
   AI-generated strategy 1

   Use the copula’s coordinatewise monotonicity to sandwich C(γuδ , γ −1 u2−δ ) between C evaluated
   along the reference path (γ̃(ru)δ , γ̃ −1 (ru)2−δ ) at two fixed multiplicative reparametrizations r = r1
   and r = r2 of u. Then prove that replacing u by ru does not change the asymptotic ratio
   [log C]/ log u when the limit for γ̃ exists. Apply a squeeze argument to conclude κL (δ, γ; C) =
   κL (δ, γ̃; C) for all γ > 0.

    This experiment reveals a sharp distinction between two kinds of guidance. Domain key-
words orient the model toward a relevant body of literature but leave the strategy selection
problem unsolved: the model must still choose among many plausible approaches without the
judgment to know which one fits. Explicit proof-strategy hints, by contrast, resolve that choice
directly. This distinction reflects the execution-strategy gap in action: the model can follow a
strategy once it is provided, but cannot select one reliably on its own, even when broad domain
context is available.

4.3   Multi-source transfer learning
Section 3.3 showed that literature-based guidance could substantially improve the sharpness of
an asymptotic bound in a single-source transfer learning problem. We now extend that problem
to a more complex multi-source setting, asking whether the same guidance approach remains
effective when the estimation procedure involves multiple stages and the reasoning chain grows
correspondingly longer. The updated context and problem setup are described in the boxes
below.




                                                      17
Context 4
We consider a transfer learning problem with a target site t and M source sites indexed
by 1, . . . , M , where our primary interest is prediction at the target site. For each site
m ∈ {t, 1, . . . , M }, the outcome y (m) ∈ R and the covariate vector x ∈ Rp follow the linear
model
                                        y (m) = x⊤ β (m) + ε,
where β (m) ∈ Rp is a random coefficient vector, x ∼ N (0, Σ), and ε ∼ N (0, σ 2 ) is indepen-
dent of x. The dimension p increases to infinity as the sample size n increases.

Problem 6
Suppose that we only observe the subvector xR(m) , indexed by R(m) ⊆ [p] in each site
                             (m)
m ∈ {t, 1, . . . , M }. Let XR(m) ∈ Rnm ×pm and Y (m) ∈ Rnm denote the observed design
matrix and response vector, respectively, where pm = |R(m)| and nm is the sample size at
the site m.

We propose an estimation procedure including 3 steps. In the first step, we compute a local
ridge estimator based on the observed data in each site m ∈ {1, . . . , M }:
                                                                         
                    (m)              1           (m)
                  ω
                  bLoc := arg min      ∥Y (m) − XR(m) ω∥22 + λ(m)
                                                              ω   ∥ω∥   2
                                                                        2 ,
                               ω    nm
        (m)
where λω      ≥ 0 is a tuning parameter.

In the second step, we define an aggregator that reconstructs a full-feature coefficient vector:
                                                           (m) 2
                                            X
                          β̂ (s) := arg min     Φ(m) β − ω
                                                         bLoc Wm ,
                                        β
                                            m∈[M ]

where Wm ⪰ 0 is positive semi-definite and ∥x∥Wm = ⟨x, Wm x⟩ for any vector x. Here
Φ(m) ∈ Rpm ×p is a matrix such that [Φ(m) ]i,j∈R(m) = Ipm with Ipm ∈ Rpm ×pm denoting
an identity matrix, and [Φ(m) ]i∈R(m),j∈[R(m)]c = (ΣR(m),R(m) )−1 ΣR(m),[R(m)]c , where
[R(m)]c = [p] \ R(m) denotes the set of features unobserved at the site m.
                            (t)                                                        (t)
In the third step, we let ω̂s = Φ(t) β̂ (s) and perform transfer learning to obtain ω̂TL [...].

For a new independent test sample (x̃R(t) , ỹ (t) ) from the target site, we define a predictive
risk for the transfer learning estimation above as
                                        h                               i
                                  (t)                      (t) 2  (t)
                          rpred ω̂TL = E ỹ (t) − x̃⊤R(t) ω̂TL     XR(t) .

Our goal is to derive an asymptotic upper bound for the above predictive risk, as tight
                                                     (m)
as possible as nt , p → ∞, with optimal choice of λω , λTL and Wm under the high-
dimensional and random-coefficient assumptions as below. Hereh the optimal Wm refers toi
the aggregation weights that minimize the aggregation error E (β̂ (s) − β (t) )(β̂ (s) − β (t) )⊤
in the Loewner sense.

High-Dimensional Assumption: For m ∈ {t, 1, . . . , M }, the full-feature dimension p and the
observed-feature dimension pm go to infinity as nm goes to infinity, with p/nm → γ ∈ (0, ∞)
and pm /nm → ηm ∈ (0, ∞).



                                                18
  Random Regression Coefficients Assumption: For m ∈ {t, 1, . . . , M }, the regression co-
  efficient vector β (m) is random with E[β (m) ] = 0 and Cov[β (m) ] = (αm        2 /p)I , where
                                                                                         p
                                                                                            ′
  αm ̸= 0. In addition, for any m, m′ ∈ {t, 1, . . . , M }, the coefficients β (m) and β (m ) sat-
                       ′
  isfy Cov(β (m) , β (m ) ) = (ρm,m′ αm αm′ /p)Ip , where ρm,m′ ∈ [0, 1].

    The [...] in the prompt above represents the transfer learning procedure defined in Problem 3.
The extended problem introduces a third step: an aggregation stage that combines local ridge
estimators from multiple source sites into a single full-feature coefficient vector before transfer
learning is performed. The key challenge in this problem is to quantify how estimation error
accumulates and propagates across each stage of the procedure [Li et al., 2022, Chang et al.,
2024, Tian and Feng, 2023]. Therefore, a complete proof would proceed in three steps: (i)
deriving the estimation error of the local ridge estimators at each source site; (ii) quantifying how
this error propagates through the aggregator; and (iii) incorporating the resulting aggregation
error into the final analysis of the transfer learning estimator at the target site. Each step builds
on the previous one, and the final asymptotic upper bound for the predictive risk should be
traceable back through all three stages to the original problem parameters.
    To reflect this added complexity, we supplemented the guidance from Section 3.3 with a third
literature reference specifically covering the error analysis of the aggregator and the optimal
choice of weighting matrix. The guided prompt is shown in the box below. Here the Guidance
references (ii) and (iii) were carried over from Section 3.3 to maintain continuity with the domain
principles established there, while Guidance (i) is new to this example.
   Guided prompt 5
   You are an expert in statistical methodology and mathematical reasoning. Your task is
   to produce a full formal proof for a problem in an ongoing research project.
   Background: The background introduced in Context 4
   Problem: The problem stated in Problem 6.
   Guidance: Use the techniques listed below. (i) The error analysis of the aggregator and
   the solution of optimal weighting metrics in Cheng, C., Cheng, G., & Duchi, J. C. (2023).
   Collaboratively learning linear models with structured missing data. Advances in Neural
   Information Processing Systems, 36, 7529-7540. (ii) The limiting trace / deterministic
   equivalent calculations in Dobriban and Wager (2018), High-Dimensional Asymptotics of
   Prediction: Ridge Regression and Classification. (iii) The predictive-risk decomposition
   and bounding strategy for the L2 transfer learning estimator in Gu, Han, and Duan
   (2025), Robust Angle-Based Transfer Learning in High Dimensions.
   Give a full formal proof for the problem. You need to state assumptions and regularity
   conditions that you use. Justify each step and give the complete proof in LATEX.

    The guided proof failed in a revealing way. Rather than deriving the estimation errors of the
local ridge estimators and the aggregator from the model, the model assumed their convergence
and defined the limits. Specifically, it assumed the convergence of the source estimation error
       (m)
Cov(b ωLoc − ω (m) ) → Vm with a deterministic matrix Vm ⪰ 0. Similarly, it further assumed the
error of aggregator, Cov(ω̂ (s) − ω (s) ) → CA with a deterministic matrix CA ⪰ 0. Here Vm and
CA serve as unspecified covariance matrices and were never derived or bounded: they simply
appeared as placeholders. As a result, the final asymptotic upper bound for the predictive risk
was expressed in terms of these unspecified matrices, making it impossible to understand how
the bound depends on the key problem parameters.
    This example provides insights into the boundaries of literature-based guidance. In Section
3.3, the same guidance approach succeeded because the proof involved a manageable number of
coordinated components. Here, the reasoning chain was longer and more interdependent, and


                                                 19
the model could not track all the dependencies simultaneously. Even with targeted references
pointing to the right tools, it resorted to replacing the hardest derivations with unverified
assumptions. This suggests that the effectiveness of literature-based guidance may diminish as
problem complexity grows, and that proof decomposition could be a more robust strategy for
problems of this kind.

4.4   Zero-concentrated differential privacy
Section 3.4 showed that the three standard privacy formalisms, Rényi-DP, (ε, δ)-DP, and f -DP,
are equivalent under the centered-symmetry assumption when one retains the full exact privacy
curve. We now ask a related but harder question: what happens when the full exact curve is
replaced by a scalar summary? Specifically, we consider zero-concentrated differential privacy
(zCDP) [Bun and Steinke, 2016], and a mechanism is said to satisfy ρ-zCDP if, for every order
α > 1, its Rényi divergence is bounded by

                                           Dα (P ∥Q) ≤ ρα

for every pair of neighboring output distributions P and Q. Thus, zCDP can be viewed as
a scalar summary of the full Rényi-DP curve: instead of looking at the entire function α 7→
Dα (P ∥Q), it keeps a single parameter ρ that upper bounds the curve by a line. This scalar
summary is convenient, as the composition rule is simple and additive, but potentially lossy,
since it replaces the full Rényi-DP curve with a single linear upper bound ρα. The question
is: how lossy is it, and under what conditions? In particular, we ask when zCDP is nearly
tight, as it is known to be for Gaussian mechanisms, and when it loses substantial information
relative to the full exact Rényi-DP curve, especially under non-Gaussian noise distributions and
heterogeneous composition.
    Unlike the problem in Section 3.4, this question is inherently more open-ended and has
no pre-determined solution path. There is no standard proof strategy to retrieve, no directly
applicable theorem to invoke, and no existing literature that resolves the question. The problem
asks the model not to execute a known argument but to navigate an open solution space and
identify a promising direction, a fundamentally different and more challenging task.
    The problem statement, research context, and formal proof instruction are shown in the
boxes below. We asked the model to derive lower bounds for a gap metric that explicitly
quantifies the optimality of zCDP. Specifically, the bound should reveal how this optimality
varies with the number of compositions, the allocation of privacy parameters, and the underlying
noise distribution.

  Problem 7
  Consider a heterogeneous composition of mechanisms

                                        M = (M1 , . . . , Mn ),

  where each Mi uses the same noise family ν (possibly non-Gaussian), and you may assume
  the noise is centered and symmetric whenever needed. Suppose P       each Mi satisfies ρi -zCDP, so
  the usual composition rule gives total privacy parameter ρ = ni=1 ρi . The main question
  is: How can we rigorously quantify its optimality or sub-optimality as a function of the
  number of compositions n, the allocation (ρ1 , . . . , ρn ), and the underlying noise distribution
  ν?
  More specifically, consider the following metric

                                    Γn,ν (α) := ρ · α − Dα (P |Q),




                                                  20
  or, depending on normalization, possibly
                                                        n
                                                        X
                                  Γn,ν (α) := ρ · α −         Dα (Pi |Qi )
                                                        i=1

  that measures the gap between the zCDP accounting and the exact privacy level of M . Your
  answer should derive lower bounds under suitable assumptions, explain how it depends
  on the number of compositions n, the allocation (ρ1 , . . . , ρn ), and the underlying noise
  distribution ν?

  Context 5
  A guiding principle is that zCDP is easy
                                        P to compose but may lose information: in general,
  from ρi -zCDP one only gets total ρ = i ρi , while for Gaussian mechanisms this accounting
  is known to be tight. In additive symmetric mechanisms, the exact privacy descriptions
  through the full Rényi DP curve, the full exact (ε, δ)-DP curve, and the f -DP curve are
  expected to be mathematically equivalent under suitable regularity assumptions. Thus the
  loss in zCDP accounting should be understood as the loss incurred by replacing the full
  exact privacy curve by a single scalar.

   Zero-shot prompt 6
   “You are an expert in differential privacy and theoretical computer science. Your task is
   to produce a full formal proof for a problem in an ongoing research project.
   Problem: The problem stated in Problem 7.
   Context: The background provided in Context 5.
   Given the problem and context above, provide a rigorous mathematical answer. You
   need to state the assumptions and regularity conditions that you use, justify each step
   carefully, and give a complete proof in LATEX.”

      The model’s response did not address this open-ended problem. A meaningful answer is
expected to reveal how the optimality of zCDP depends on the noise distribution ν through
interpretable quantities, such as the distance from Gaussianity, tail behavior, cumulants of
the privacy loss, or curvature of the Rényi-DP curve, so that the bound becomes informative
about when zCDP is nearly tight and when it loses substantial information. The model instead
introduced a “local non-Gaussian envelope defect” assumption with unspecified           constants cν (α),
Cν (α), and r0 , and derived a lower bound of the form Γn,ν (α) ≥ cν (α) i ρ2i /2. This displaced
                                                                               P
the core difficulty into undefined constants: since cν (α) and Cν (α) were never computed from
any interpretable privacy quantity, the bound has a formal shape but no scientific content. It
does not reveal why zCDP is tight for Gaussian mechanisms and loose for non-Gaussian ones,
the insight the problem was designed to extract.
      The response also spent considerable effort on proving statements that are either textbook
facts or not useful for this research question. For example, it provided a full     P proof that Rényi
divergence tensorizes under independent composition, namely Dα (P ∥Q) = i Dα (Pi ∥Qi ), and
later used basicP tools such as Cauchy–Schwarz and Jensen’s inequality to rewrite the bound
in terms of i ρ2i or an effective number of compositions. They are well-known facts that do
not advance the question of when zCDP is informative. The notation and writing style were
also unnecessarily heavy. For example, the output introduced many auxiliary objects, such as
ρ̄i , gν (α; r), Pν,r , Qν,r , H(w), neff , Kt (λ), and several envelope constants, without using them
to illuminate the underlying mechanism. Such notation-heavy presentation makes the proof
difficult to read and is not consistent with good scientific writing, where new notation should
simplify the argument rather than obscure the main idea.

                                                   21
    This example illustrates a failure case for open-ended research questions: the model produced
something that resembles a proof, with assumptions, formal derivations, and derived bounds,
but that does not engage with the actual research question. Faced with a large and open solution
space, the model defaulted to local plausibility: making each individual step look reasonable
without ensuring that the overall argument addresses what was asked. It suggests that open-
ended research questions, where the solution path is not pre-determined and deep conceptual
insight is required, currently may lie beyond the reliable reach of general-purpose LLMs.


5     Toward AI-assisted statistical proof
The case studies presented in this paper point to an actionable picture of where current general-
purpose LLMs stand as proof assistants in statistical research. They are genuinely useful,
capable of carrying out substantial and technically demanding derivations when the problem is
precisely specified and the proof strategy is clear. But they are also systematically limited by the
execution-strategy gap: the inability to identify, select, and adapt appropriate proof strategies
on their own when facing a new problem and context. This gap is not merely a performance
shortcoming; it reflects something deeper about what statistical proof requires that current
general-purpose LLMs, trained broadly across many domains, are not yet equipped to provide.
The gap, however, is only half the story. As Section 2 highlighted, the demands on human
expertise persist on either side of it in the human-AI collaborative workflow: in formulating a
good proof task, and in verifying whether what an AI model returns is valid, on-target, and
sharp. At the level of individual research practice, they suggest concrete ways to structure
AI-assisted proof workflows so that the model’s strengths are leveraged and human judgment
is applied where it matters most. At the level of the broader statistical community, they point
to a coordinated agenda: building shared resources that make proof strategies more accessible,
developing more capable AI systems that can reason across longer and more complex arguments
and support faster verification, and training a new generation of statisticians to work effectively
in human-AI collaboration. In this section, we discuss each of these directions.

5.1   Practical lessons for individual statisticians
Our case studies show that the difference between a useful and an unhelpful proof generated by
a general-purpose LLM often comes down to how the human-AI interaction is structured. Four
practical lessons emerge consistently across the examples.
    The first is precision in problem specification. A well-structured prompt makes the target
quantity, notation, modeling assumptions, asymptotic regime, and any nonstandard conventions
explicit from the outset. When the setup is underspecified, the model tends to fill in the
gaps with mathematically convenient but scientifically inappropriate defaults, as illustrated in
Section 3.1, where an underspecified prompt led the model to adopt a random-effects framework
inconsistent with the intended fixed-effects setup. Moreover, when the intended formulation
departs from the default convention in the relevant literature, stating the correct assumption
is often not enough, the prompt should also explicitly rule out the incorrect default. Negative
instructions of this kind are an effective way to prevent the model from defaulting to a confident
but wrong formulation.
    The second lesson is the value of targeted guidance. When zero-shot prompting fails because
the model cannot identify or retrieve the right proof strategy, providing concise strategy hints
or key literature references can make a substantial difference, often transforming a non-rigorous
or uninformative derivation into a correct and sharp one, as illustrated in Sections 3.2 and 3.3.
The guidance does not need to be extensive: a few targeted sentences pointing to the right
approach, or two or three literature references indicating the relevant tools, are often sufficient.
What matters is that the guidance resolves the strategy selection problem that the model cannot


                                                22
solve on its own.
    The third lesson is proof decomposition. When the proof task is long, open-ended, or requires
simultaneous control of multiple technical components, asking the model to produce a complete
end-to-end proof in a single pass is unlikely to succeed, as illustrated in Sections 4.1 and 4.3. A
more effective approach is to decompose the proof into smaller and more tractable problems and
work on each within a structured human-AI workflow. This decomposition strategy shifts the
model’s role from end-to-end proof generator to targeted proof assistant, a role it is considerably
better equipped to play in human-AI collaboration.
    The fourth lesson is that there is no magic prompt and that iterative engagement is needed.
Even for the small and tractable problems illustrated in our successful case studies, a single
prompt attempt was rarely sufficient on its own; the prompt blocks used to present our case
studies, including zero-shot attempts and targeted guidance, are a simplification chosen for
clarity of exposition, not a description of how the underlying work actually proceeded. Arriving
at each guided result typically took more exploration than the final presentation shows. For
more complex and open-ended problems, the need for iteration is even greater. The realistic
workflow is therefore closer to an engaged research conversation than to a single prompt query:
specify the question, ask the model to propose a proof route, inspect that route, verify the
AI-generated output at each step, and repair what fails. Treating prompt design as a one-time
act risks the failure mode our case studies observed: a plausible-looking derivation accepted
without the iterative scrutiny that catches when it has gone wrong.
    In summary, these four lessons suggest a practical workflow for AI-assisted statistical proof:
specify the problem precisely, provide targeted guidance when the strategy is not obvious, de-
compose complex arguments into manageable problems, and treat the whole process as iterative
rather than a single exchange. This workflow does not replace human statistical expertise. It
redefines the human role, redirecting expertise away from routine execution and toward the
judgments and decision-making that current AI cannot reliably make on its own.

5.2   Building shared resources for proof strategies
The practical lessons in Section 5.1 all depend, to varying degrees, on the availability of the
right proof strategy at the right moment. In the copula example of Section 3.2, two short
strategy hints transformed a failed derivation into a correct proof. In the transfer learning
example of Section 3.3, two literature references were enough to shift the model from a loose
and uninformative bound to a sharp and meaningful one. In these cases, the critical resource
was not computational power or mathematical ability, it was access to the right domain-specific
proof strategy, supplied by a human expert who knew where to look.
    This points to a broader opportunity for the statistics community. Statistical proof de-
velopment has two distinctive components that set it apart from most mathematical proof:
translating a real-world scientific question into a precise statistical framework with appropriate
assumptions, and then identifying and adapting the right strategy from a repertoire of reusable
domain-specific tools. Both components currently rely on knowledge that is rarely documented
in a retrievable form. The modeling component covers decisions about which assumptions are
scientifically appropriate, which quantities are meaningful, and which mathematical idealiza-
tions are justifiable. This knowledge is largely transmitted through domain-specific training
and research experience, with little explicit guidance available for researchers working at the
boundaries of their expertise. The strategy component covers knowing which proof technique
applies to a given problem and how to adapt it to a new context. This knowledge is similarly
scattered across textbooks, papers, and the tacit knowledge of experienced researchers, rarely
organized in a way that makes it easy to find and reuse. Building shared, organized repositories
that address both components could make this knowledge substantially more accessible across
the community. Such repositories would document not only reusable proof strategies but also
the modeling principles and assumption choices that characterize different research areas, in-

                                                23
dexed by proof goal, scientific context, and typical assumptions, with representative references
for each entry.
    Such repositories would serve multiple purposes simultaneously. For individual researchers,
they would reduce the time spent searching for applicable proof techniques, particularly for
researchers working at the boundaries of their expertise. For graduate students, they would
provide a structured entry point into the proof strategies of a new field, complementing what is
currently transmitted slowly and unevenly through textbooks and one-on-one advising. For AI
systems, they could serve as a retrieval resource that addresses the strategy-selection bottleneck
directly, providing the targeted guidance that our case studies show is often sufficient to unlock
reliable AI performance. Recent community efforts such as Lu et al. [2025] and StatProver1
provide encouraging early examples of what such resources might look like, and point toward a
more systematic and community-wide effort.
    Building and maintaining such repositories will require collective effort from the statistics
community, contributions from researchers across subfields, curation to ensure quality and con-
sistency, and regular updates as new proof techniques emerge. We view this as an important
and tractable community agenda item, one that would benefit both human and AI-assisted
statistical proof development simultaneously.

5.3      Agentic AI systems and formal verification
The workflow insights and shared repositories described in Sections 5.1 and 5.2 can substantially
improve the reliability of current general-purpose LLMs for well-scoped statistical proof tasks.
But our failure cases, such as Sections 4.1 and 4.4, suggest that some limitations run deeper
than what better prompting or richer resources can address. When the reasoning chain is long
or when the problem is genuinely open-ended, current general-purpose LLMs struggle in ways
that targeted guidance alone cannot resolve. These cases point to the need for more capable
end-to-end AI architectures, such as agentic AI systems that can plan, maintain memory across
steps, verify intermediate results, revise their own arguments, and draw on external tools and
literature in a coordinated way.
    Recent progress in agentic AI for mathematics provides an encouraging reference point.
Systems such as Aletheia [Feng et al., 2026] and the AI co-mathematician [Zheng et al., 2026]
organize mathematical reasoning through iterative generation-verification-revision workflows, in
which a generator proposes a candidate argument, a verifier checks for errors and logical gaps,
and a reviser improves the argument based on the feedback. These systems also use web search
and literature navigation to reduce fabricated citations and ground arguments in existing re-
sults. Applied to research-level mathematical problems, they have shown substantially stronger
performance than single-pass LLM prompting on complex reasoning tasks [Xia et al., 2026].
In addition, the use of formal proof assistants such as Lean2 can provide machine-checkable
verification of mathematical arguments. Recent work has shown that LLMs can be trained to
generate Lean-verifiable proofs for Olympiad-level problems, suggesting that formal verification
could eventually serve as a rigorous and automated checking mechanism within agentic statis-
tical proof workflows. This is one of the supports our case studies suggest are most needed: not
a replacement for the rapid diagnostic judgment described in Section 2, but a complementary
check that can flag what even a careful human reviewer might miss in a long or notation-heavy
derivation. However, many of these advanced agentic AI systems and LLM-Lean integrations
are not publicly available; they are developed and maintained by large research organizations
with access to substantial computational resources, and are not yet accessible to everyday sta-
tistical researchers in the way that general-purpose LLMs are. Closing this accessibility gap is
itself an important community challenge, and points to the value of open and community-driven
  1
      https://huggingface.co/datasets/StatAILab/StatProver.
  2
      https://lean-lang.org/



                                                 24
development of agentic AI proof tools tailored to the needs of statistical research.
    Notably, adapting these architectures to statistical proof development would require going
beyond what current mathematical agentic AI systems provide. Statistical proofs are shaped by
modeling assumptions tied to scientific application domains and often require careful domain-
specific judgment about what constitutes a sharp and meaningful result. A statistical proof
AI system would therefore need to integrate several capabilities that current systems lack: a
mechanism for navigating and applying domain-specific modeling conventions, access to orga-
nized repositories of statistical proof strategies of the kind described in Section 5.2, tools for
verifying not just mathematical correctness but also the scientific meaningfulness and sharpness
of conclusions, and an exposition-revision stage that simplifies notation, removes inessential def-
initions, and ensures that the final argument is readable and verifiable by a human statistician.
Formal proof assistants such as Lean could play a valuable role in this architecture, providing
a verification layer that catches logical gaps and unjustified steps of the kind observed in our
failure cases. For higher-level assessment, such as whether a proof is asking and answering the
right scientific question, human diagnostic judgment is unlikely to be easily replaced.

5.4     Training future statisticians for AI-assisted research
The findings of this study have direct implications for how the next generation of statisticians
should be trained. Our case studies show that effective use of general-purpose LLMs in statistical
proof development is not simply a matter of knowing how to operate the AI tools: it requires a
set of intellectual skills that are distinct from, but deeply complementary to, the mathematical
skills that current graduate training already emphasizes. The main educational goal is to train
students to direct, constrain, and critically evaluate AI assistance, treating current general-
purpose LLMs as proof assistants that are often useful for precisely formulated problems but
unreliable for unsupervised end-to-end derivations. We suggest emphasizing five complementary
skills that current curricula do not systematically address.
    The first is precise problem formulation with AI interaction. Students should learn to
identify important questions from a scientific context, formulate statistical problems with ap-
propriate assumptions, and translate a research-level proof task into a prompt that conveys
the problem precisely and unambiguously to the AI model. This skill is closely related to the
broader statistical skill of problem formulation, but applied in a new context where the con-
sequences of underspecification are immediate and sometimes difficult to detect. For example,
the LDSC example in Section 3.1 illustrates both the importance of this skill and the subtle
pitfalls that arise when it is not exercised carefully. As Section 2 noted, this is also a skill
whose importance will likely increase: as AI handles more of the execution, what distinguishes
researchers is increasingly their ability to formulate the right question in the first place. From a
technical perspective, learning structured prompting techniques can also help students formu-
late research problems more precisely with AI. From a technical perspective, actively keeping
up with fast-evolving structured prompting techniques3 can also sharpen students’ ability to
formulate research problems with AI. For example, rather than relying solely on the student to
write a complete and precise prompt, a “grill me” routine asks the AI model itself to interro-
gate the student about the theorem statement, the assumptions, the target quantity, and the
intended proof strategy, until the problem is well specified before any derivation begins.
    The second is proof decomposition. Students should learn to identify which components of
a proof are well-scoped enough for reliable AI assistance and which require human judgment,
and to decompose complex arguments into tractable tasks accordingly. This skill is not only
useful for AI-assisted proof development, but it is also a valuable approach in its own right,
encouraging students to think carefully about the logical structure of a proof before attempting
to execute it.
  3
      https://github.com/mattpocock/skills



                                                25
    The third is critical evaluation of AI-generated proofs. Students should learn to read AI-
generated derivations with the same critical eye they would apply to a proof from a textbook
or a paper, checking for hidden assumptions, unjustified appeals to standard results, changes in
the estimand, and notation that obscures rather than clarifies the argument. Our failure cases
show that general-purpose LLMs can produce derivations that appear complete and rigorous
on the surface but contain errors that are easy to miss and hard to detect without domain
expertise. Actively learning structured prompting techniques can support this skill in practice.
For example, a “zoom out” routine can ask the model to explain the proof’s overall architecture,
the role of each assumption, and where the main difficulty lies, before technical details are
generated, which helps a student check the shape of an argument before getting lost in its
details. An “assumption audit” routine can ask the model to list every assumption used in
the proof and classify each one as stated in the original problem, derived during the argument,
newly introduced, or unnecessary, which makes hidden or unjustified assumptions more visible
and checkable. Detecting these errors requires both mathematical maturity and familiarity with
the specific failure modes that current general-purpose LLMs tend to exhibit.
    The fourth is strategic use of guidance. Students should learn to recognize when a zero-shot
prompt is unlikely to succeed. This is often the case when the problem requires strategy se-
lection, careful control of modeling assumptions, or a long reasoning chain. In such situations,
students should learn to provide targeted guidance that resolves the current bottleneck effi-
ciently. This includes knowing how to identify relevant literature references, how to formulate
concise proof-strategy hints, and how to calibrate the level of guidance needed for a given task.
The copula and transfer learning examples in Sections 3.2 and 3.3 illustrate how modest but
well-targeted guidance can transform an unreliable AI output into a useful and rigorous one.
    The fifth is rapid diagnostic judgment. As Section 5.1 discussed, what separates a productive
AI-assisted session from an unproductive one is often not whether an error eventually gets
caught, but how quickly it is caught and corrected within the interactive workflow. A student
who can tell within moments that a derivation has changed its target, smuggled in an unjustified
assumption, or produced a result that is technically valid but scientifically weak can redirect
the model immediately and keep a multi-round conversation moving toward a correct proof. A
student who lacks this fluency may accept a flawed intermediate step, build further reasoning on
top of it, and only discover the error much later, at far greater cost. This is, at its core, a form
of human decision making rather than purely a technical skill: the student must decide whether
to trust an output, redirect it, or dig deeper before proceeding, decisions that AI cannot make
on the student’s behalf.
    Put together, these five skills outline what a well-structured AI-assisted proof session might
look like for future statisticians. It begins with formulating the statistical question, sharpened
where useful by a grill-me interrogation that forces precision before any derivation starts. The
student then selects or proposes a proof strategy, supplying targeted guidance where zero-shot
prompting is unlikely to succeed, and decomposing the argument into lemma-level problems
where the reasoning chain is long or the components are numerous. As the model generates
each piece of the proof, a zoom-out check confirms that the overall architecture is sound before
the details are scrutinized, and an assumption audit surfaces anything stated, derived, added,
or left unjustified along the way. Throughout, rapid diagnostic judgment operates continuously,
catching a wrong target or a quietly weakened result early enough to redirect the conversation.
The exposition is then refined once the argument itself is sound, simplifying notation and
removing inessential definitions so that the final proof is as readable to a human reader as it is
correct. None of these stages is mechanical on its own; each depends on the kind of judgment
that AI assistance relocates to the human rather than removes.
    These skills can be integrated into graduate training through dedicated courses on AI-
assisted statistical proof. Such courses would be structured around hands-on exercises in which
students practice the five skills described above: formulating precise proof tasks, decomposing


                                                26
complex arguments, evaluating AI-generated outputs critically, providing targeted guidance,
and developing rapid diagnostic judgment. The goal is not to replace traditional proof training
but to complement it, preparing future statisticians to work effectively at the interface of sta-
tistical expertise and AI assistance that will increasingly characterize statistical research in the
years ahead. Since courses of this kind are new to most statistics departments, developing them
will itself benefit from community-wide collaboration: sharing course materials, exercises, and
assessment frameworks across departments, and revisiting them regularly as the capabilities of
AI tools continue to evolve rapidly.


6    Limitations and future work
The practical insights of this paper should be interpreted in light of several limitations. The first
limitation is scope. Our findings are based on eight proof problems drawn from four areas of
statistical research. While these problems were chosen to reflect the range of tasks that arise in
day-to-day statistical research, and while the qualitative conclusions were consistent across three
different models, eight problems cannot capture the full diversity of proof tasks in statistics. The
execution-strategy gap we identify may manifest differently, or may be less pronounced, in other
fields, proof types, or levels of technical difficulty. Future work can extend this investigation
to a broader range of problems, including problems from areas such as Bayesian statistics,
causal inference, and survival analysis, where proof strategies and modeling conventions differ
substantially from those examined here.
    A second limitation is the rapid pace of AI development. The findings reported here reflect
the capabilities of GPT-5.4 Thinking, Gemini 3.1 Pro, and Claude Opus 4.6 at the time of
writing. Model capabilities are changing rapidly, and some of the limitations we observe may
be partially addressed by future models. We view this study as a snapshot of the current state
rather than a permanent characterization, and we plan to update our findings as new models
and tools become available. This applies with particular force to our claim that the importance
of problem formulation and rapid diagnostic judgment will grow as execution improves: this
is a prediction about a dynamic, not a direct empirical finding from our case studies, and it
deserves the same scrutiny and updating as any other forecast about a fast-moving technology.
The paired case study design introduced here, with matched success and failure cases drawn
from the same research context, provides a reusable framework for ongoing evaluation as the
landscape evolves.
    Another limitation is that we focus exclusively on general-purpose LLMs accessible to every-
day researchers. Domain-specific fine-tuned models and agentic AI architectures may perform
substantially better on statistical proof tasks. As discussed in Section 5.3, some early evidence
from mathematical agentic AI suggests meaningful improvements on complex reasoning tasks.
Evaluating these more capable but currently less accessible systems on statistical proof tasks is
an important direction for future work, particularly after these systems become more publicly
available.
    Despite these limitations, we believe the findings reported here provide a useful and ac-
tionable starting point for the statistics community. The execution-strategy gap is a real and
systematic phenomenon that shapes the reliability of current general-purpose LLMs on statisti-
cal proof tasks, and the practical lessons and community agenda outlined in this paper provide
concrete directions for addressing it, both through better use of existing AI tools and through
the development of more capable ones. More broadly, statistical proof serves as a window into
what human-AI collaboration in expert cognitive work actually demands: structured, verifiable,
and tied to real-world scientific questions, it makes visible patterns that are likely to recur across
domains where experts delegate technical execution to AI while remaining responsible for its
direction and outcome.



                                                 27
Acknowledgments
The research has been partially supported by NSF Grant DMS 2210860 and start-up funds from
Purdue Statistics Department and Department of Statistics and Data Science at the University
of Pennsylvania. This research was supported in part by Analytics at Wharton, Wharton AI
& Analytics Initiative, Wharton Dean’s Research Fund, Perelman School of Medicine CCEB
Innovation Center Grant, and the University Research Foundation Grant. This research was
also supported by the National Institute of Mental Health under Award Number R01MH136055,
and National Institute on Aging under Award Numbers RF1AG082938, R01AG085581, and
R03AG102039. The content is solely the responsibility of the authors and does not necessarily
represent the official views of the National Institutes of Health.


Author contributions
B.Z. and F.X. designed the study. F.X., X.S., H.T, and B.S., performed the case study analysis
and generated most of the results. M.M and C.W. provided input on the research question,
prompt design, and interpretation of the findings. X.S., H.T, B.S., F.X., and B.Z. wrote the
manuscript with feedback from all authors.


Supplementary materials
Supplementary materials are available at https://github.com/xiaojing777/Human-AI-Sta
tistical-Proof-Supplement.


Competing interests
The authors declare no competing interests.


References
Mohammed Abouzaid, Andrew J. Blumberg, Martin Hairer, Joe Kileel, Tamara G. Kolda,
 Paul D. Nelson, Daniel Spielman, Nikhil Srivastava, Rachel Ward, Shmuel Weinberger, and
 Lauren Williams. First proof. arXiv preprint arXiv:2602.05192, 2026.
John M Abowd, Robert Ashmead, Ryan Cumings-Menon, Simson Garfinkel, Micah Heineck,
  Christine Heiss, Robert Johns, Daniel Kifer, Philip Leclerc, Ashwin Machanavajjhala, et al.
  The 2020 census disclosure avoidance system topdown algorithm. Harvard Data Science
  Review, 2:1–72, 2022.
Kaito Baba, Chaoran Liu, Shuhei Kurita, and Akiyoshi Sannai. Prover agent: An agent-based
 framework for formal mathematical proofs. arXiv preprint arXiv:2506.19923, 2025.
Zhidong Bai, Jack W Silverstein, et al. Spectral analysis of large dimensional random matrices,
  volume 20. Springer, 2010.
Borja Balle, Gilles Barthe, and Marco Gaboardi. Privacy amplification by subsampling: Tight
  analyses via couplings and divergences. Advances in neural information processing systems,
  31, 2018.
Brendan K Bulik-Sullivan, Po-Ru Loh, Hilary K Finucane, Stephan Ripke, Jian Yang, Nick
  Patterson, Mark J Daly, Alkes L Price, Benjamin M Neale, Schizophrenia Working Group
  of the Psychiatric Genomics Consortium, et al. LD score regression distinguishes confounding
  from polygenicity in genome-wide association studies. Nature Genetics, 47(3):291–295, 2015.

                                              28
Mark Bun and Thomas Steinke. Concentrated differential privacy: Simplifications, extensions,
 and lower bounds. In Theory of Cryptography Conference, pages 635–658. Springer, 2016.

Jae Ho Chang, Massimiliano Russo, and Subhadeep Paul. Heterogeneous transfer learning for
  high-dimensional regression with feature mismatch. arXiv preprint arXiv:2412.18081, 2024.

Sourav Chatterjee. Fluctuations of eigenvalues and second order poincaré inequalities. Proba-
  bility Theory and Related Fields, 143(1):1–40, 2009.

Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran
  Jin, Xing Jin, Chenggang Li, Kaijing Ma, et al. Seed-prover: Deep and broad reasoning for
  automated theorem proving. arXiv preprint arXiv:2507.23726, 2025.

Laurens de Haan and Ana Ferreira. Extreme Value Theory: An Introduction. Springer Science
  & Business Media, 2006.

Edgar Dobriban and Stefan Wager. High-dimensional asymptotics of prediction: Ridge regres-
  sion and classification. The Annals of Statistics, 46(1):247–279, 2018.

Jinshuo Dong, Aaron Roth, and Weijie J Su. Gaussian differential privacy. Journal of the Royal
  Statistical Society Series B: Statistical Methodology, 84(1):3–37, 2022.

Shihan Dou, Ming Zhang, Zhangyue Yin, Chenhao Huang, Yujiong Shen, Junzhe Wang, Jiayi
  Chen, Yuchen Ni, Junjie Ye, Cheng Zhang, et al. Cl-bench: A benchmark for context learning.
  arXiv preprint arXiv:2602.03587, 2026.

Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya Mironov, and Moni Naor. Our
  data, ourselves: Privacy via distributed noise generation. In Annual international conference
  on the theory and applications of cryptographic techniques, pages 486–503. Springer, 2006a.

Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. Calibrating noise to sensi-
  tivity in private data analysis. Theory Of Cryptography, Proceedings, 3876:265–284, 2006b.

Tony Feng, Trieu Trinh, Garrett Bingham, Jiwon Kang, Shengtong Zhang, Sang-hyun Kim,
  Kevin Barreto, Carl Schildkraut, Junehyuk Jung, Jaehyeon Seo, et al. Semi-autonomous
  mathematics discovery with gemini: A case study on the erd\h {o} s problems. arXiv preprint
  arXiv:2601.22401, 2026.

Tian Gu, Yi Han, and Rui Duan. Robust angle-based transfer learning in high dimensions.
  Journal of the Royal Statistical Society Series B: Statistical Methodology, 87(3):723–745, 2025.

Lei Hua and Harry Joe. Tail order and intermediate tail dependence of multivariate copulas.
  Journal of Multivariate Analysis, 102(10):1454–1471, 2011.

Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić, Eric Wieser,
 Aja Huang, et al. Olympiad-level formal mathematical reasoning with reinforcement learning.
 Nature, 651:607–613, 2026.

Jiming Jiang, Wei Jiang, Debashis Paul, Yiliang Zhang, and Hongyu Zhao. High-dimensional
  asymptotic behavior of inference based on gwas summary statistic. Statistica Sinica, 33:
  1555–1576, 2023.

Harry Joe. Dependence modeling with copulas. CRC press, 2014.

Haocheng Ju and Bin Dong. Ai for mathematics: Progress, challenges, and prospects. arXiv
 preprint arXiv:2601.13209, 2026.



                                               29
Anthony W Ledford and Jonathan A Tawn. Statistics for near independence in multivariate
 extreme values. Biometrika, 83(1):169–187, 1996.

Sai Li, T Tony Cai, and Hongzhe Li. Transfer learning for high-dimensional linear regression:
  Prediction, estimation and minimax optimality. Journal of the Royal Statistical Society Series
  B: Statistical Methodology, 84(1):149–173, 2022.

Yuchen Lu, Run Yang, Yichen Zhang, Shuguang Yu, Runpeng Dai, Ziwei Wang, Jiayi Xiang,
  Siran Gao, Xinyao Ruan, Yirui Huang, et al. Stateval: A comprehensive benchmark for large
  language models in statistics. arXiv preprint arXiv:2510.09517, 2025.

Frank McSherry. Privacy integrated queries: an extensible platform for privacy-preserving data
  analysis. Commun. ACM, 53(9):89–97, 2010.

Roger B. Nelsen. An Introduction to Copulas. Springer Science & Business Media, 2 edition,
  2006.

ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
  Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal
  mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
  arXiv:2504.21801, 2025.

Sidney I Resnick. Heavy-tail phenomena: probabilistic and statistical modeling. Springer, 2007.

Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
  M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang,
  Omar Fawzi, et al. Mathematical discoveries from program search with large language models.
  Nature, 625(7995):468–475, 2024.

Abe Sklar. Fonctions de répartition à n dimensions et leurs marges. Publications de l’Institut
 de Statistique de l’Université de Paris, 8:229–231, 1959.

Buxin Su, Weijie J. Su, and Chendi Wang. The 2020 US Decennial Census is more private than
  you (might) think. Proceedings of the National Academy of Sciences, 122(45):e2500337122,
  2025.

Jianxi Su and Lei Hua. A general approach to full-range tail dependence copulas. Insurance:
  Mathematics and Economics, 77:49–64, 2017.

Ye Tian and Yang Feng. Transfer learning under high-dimensional generalized linear models.
  Journal of the American Statistical Association, 118(544):2684–2697, 2023.

Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong. Solving olympiad geometry
  without human demonstrations. Nature, 625:476–482, 2024.

Staal A Vinterbo. Differential privacy for symmetric log-concave mechanisms. In International
  Conference on Artificial Intelligence and Statistics, pages 6270–6291. PMLR, 2022.

Martin J Wainwright. High-dimensional statistics: A non-asymptotic viewpoint, volume 48.
 Cambridge University Press, 2019.

Peng-Yuan Wang, Tian-Shuo Liu, Chenyang Wang, Ziniu Li, Yidi Wang, Shu Yan, Chengxing
  Jia, Xu-Hui Liu, Xinwei Chen, Jiacheng Xu, et al. A survey on large language models for
  mathematical reasoning. ACM Computing Surveys, 58(8):1–35, 2026.

David P. Woodruff et al. Accelerating scientific research with gemini: Case studies and common
  techniques. arXiv preprint arXiv:2602.03837, 2026.

                                              30
Hai Xia, Carla P. Gomes, Bart Selman, and Stefan Szeider. Agentic neurosymbolic collab-
 oration for mathematical discovery: A case study in combinatorial design. arXiv preprint
 arXiv:2603.08322, 2026.

Fei Xue and Bingxin Zhao. High-dimensional statistical inference for linkage disequilibrium
  score regression and its cross-ancestry extensions. The Annals of Statistics, 53(5):1913–1937,
  2025.

Kino Zhao. What are statistical assumptions about? an answer from perspectivism. Harvard
  Data Science Review, 7(1), 2025.

Daniel Zheng, Ingrid von Glehn, Yori Zwols, Iuliya Beloshapka, Lars Buesing, Daniel M
 Roy, Martin Wattenberg, Bogdan Georgiev, Tatiana Schmidt, Andrew Cowie, et al.
 Ai co-mathematician: Accelerating mathematicians with agentic ai.      arXiv preprint
 arXiv:2605.06651, 2026.




                                              31
