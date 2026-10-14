                                                                                Formalization of QFT
                                                           Michael R. Douglas ∗1 , Sarah Hoback †2 , Anna Mei‡2 , and Ron Nissim §3
                                              1
                                                  Center Of Mathematical Sciences And Applications, Harvard University, Cambridge, MA 02138 USA
                                                           2
                                                             Jefferson Physical Laboratory, Harvard University, Cambridge, MA 02138 USA
                                                                         3
                                                                           Simons Building, MIT, Cambridge, MA 02139 USA


                                                                                            March 2026
arXiv:2603.15770v1 [hep-th] 16 Mar 2026




                                                                                              Abstract
                                                A foundational result in constructive quantum field theory is the construction of the free bosonic quan-
                                             tum field theory in four-dimensional Euclidean spacetime and the proof that it satisfies the Glimm–Jaffe
                                             axioms, a variant of the Osterwalder–Schrader axioms. We present a formalization of this result in the
                                             Lean 4 interactive theorem prover. The project is intended as a proof of concept that extended arguments
                                             in mathematical physics can be translated into machine-checked proofs using existing AI tools. We begin
                                             by introducing interactive theorem proving and constructive quantum field theory, then describe our
                                             formalization and the design decisions that shaped it. We also explain the methods we used, including
                                             coding assistants, and conclude by considering how AI assisted formalization may influence the future of
                                             theoretical physics.
                                                Our original release assumed three results, Minlos’ theorem, the nuclear property of Schwartz space,
                                             and Goursat’s theorem. In subsequent releases from our group and from contributors from the Lean
                                             community, these assumptions have been proven (or avoided), so that the OS/GJ axioms are now proven
                                             using only Lean and its library Mathlib.




                                          ∗ mdouglas@cmsa.fas.harvard.edu
                                          † sarahhoback@g.harvard.edu, now at Physical Superintelligence PBC: sarah@psi.inc
                                          ‡ amei@g.harvard.edu
                                          § rnissim@mit.edu




                                                                                                   1
Contents
1 Introduction                                                                                                  3
  1.1 What is formalization and why? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        3
  1.2 ITP in the age of AI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
  1.3 Comparing Styles of Reasoning in Physics and Mathematics . . . . . . . . . . . . . . . . . . .            6
  1.4 Brief status report on rigorous QFT with respect to the Mass Gap Problem . . . . . . . . . .              7
  1.5 Related work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    8

2 Axiomatic QFT and Constructive Frameworks                                                                     8

3 Introduction to the mathematics                                                                              10

4 Details of the formalization                                                                               12
  4.1 Construction of Gaussian Free Field . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
  4.2 Schwartz Test Functions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
  4.3 Motivation for the definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
  4.4 Other infrastructure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

5 Methods                                                                                                  15
  5.1 Tips and common pitfalls . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

6 Going forward                                                                                             18
  6.1 Advice for now (early 2026) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

A Notations                                                                                                    28

B Proofs of Glimm-Jaffe Axioms                                                                                28
  B.1 Analyticity (OS0) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
  B.2 Regularity (OS1) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
  B.3 Euclidean Invariance (OS2) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
  B.4 Reflection Positivity (OS3) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
  B.5 Ergodicity (OS4) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33




                                                       2
1     Introduction
AI is starting to have a major impact on science. This impact is happening in many ways, and one of
them is its use in interactive theorem proving (ITP), a technology for proving and checking mathematical
theorems expressed in a formal language, via interactive theorem proving and AI coding assistants. There
is rapid and recent development that demonstrates the practical maturity of machine-proven and verified
mathematics at scale, including Lean-verified solutions achieving IMO 2025 gold-medal-level performance,
the release of end-to-end formal (Lean 4) solution corpora for Putnam 2025 by autonomous theorem-proving
systems, and a rapid expansion of autoformalization methods and benchmarks aimed at translating informal
statements/proofs into verifiable Lean code [91, 43]. Many mathematicians are optimistic about the potential
impact ITP will have on research level mathematics, though its influence elsewhere has been far less robust.
    We believe that ITP will also have great value for theoretical physics. To demonstrate that it is now
practical, we have formalized the construction of free massive bosonic d = 4 Euclidean quantum field the-
ory (QFT) in Lean, following the treatment of Glimm and Jaffe [38]. Our code is in the GitHub repo
mrdouglasny/OSforGFF together with its dependencies. In this preprint we explain our methods and many
details.
    As formalization is not a widely known concept in the theoretical physics community, we will begin by
explaining what it is and why physicists should be interested in it. We then explain our goals for this project,
share some important foundational and technical results, and most importantly we discuss the definitions of
QFT within various axiomatic systems and the reconstruction theorems which relate them. We also outline
more ambitious goals which we believe will be possible with strong enough formalization technology. The
authors of this paper have felt the formalization landscape change beneath their feet during the course of this
formalization project. The strength of the formalization technology we used, the publicly available Claude
Code, GPT Codex and Gemini models, significantly improved over the span of 9 months. It is not out of
the question that ambitious projects outlined in the conclusions will come into range in 2026.
    At present, formalization is based on mathematical foundations, so to formalize QFT we must work with
rigorous mathematical definitions. In §3 we give a brief introduction to constructive QFT, both outlining a
few of the major approaches and then diving into the details we will need. One aspect of this is that the
same physical ideas can be expressed in several mathematically different ways, all leading to comparable
final results. These distinctions become even more significant in a formal setting. Concrete choices must be
made, and these choices are strongly influenced by practical considerations, such as which definitions and
theorems are already available in Lean libraries and how difficult the resulting proofs are to implement. As
a result, we occasionally adopt constructions that are not the most conventional from a physics perspective,
but which fit more smoothly into the existing formal framework. In §4, we explain the main choices we
made, the reasons for those choices, and give an overview of the formal proofs.
    In §5 we discuss our methods – how we began, workflow, and tools for managing this medium size
collaborative software project. Some of this is already outdated as LLM and coding assistant technology is
evolving extremely rapidly. In early 2025 coding assistants were not able to write Lean code at the required
level. Perhaps by 2027 we will just give them the informal math statement and they will do all the work. In
§6 we give advice and suggestions from today’s (early 2026) standpoint. In addition to introducing formal
theorists to ITP and encouraging them to consider how it can be used in their research, we intend this to
serve as a historical record of the current progress in AI-assisted formal verification.

1.1    What is formalization and why?
Interactive theorem proving (ITP) is a method for developing and checking mathematical proofs by expressing
them in a formal language, a language with precise logical semantics which can be checked by a computer.
The process of translating a piece of “informal” mathematics into a formal language is called formalization,
and is presently done through interactive collaboration between a user and a proof assistant [44]. There is
a related concept of automated theorem proving (ATP), which does not require human collaboration, while
automated translation to formal mathematics is called autoformalization [89].
    ITP has been developed for many decades, and several proof assistants are well suited to expressing
mathematics, including Coq/Rocq [92], Isabelle [76], and more recently Lean [7]. Lean is the focus of much
current community effort [7, 55, 25] and has a sizable library of standard definitions and results called Mathlib


                                                       3
                           Natural Language                                                       Formal Language                                  Lean 4 Compiler
 [Statement]:                                                                         [Imported Theorem Env]:
 Given two non-negative real numbers, prove that taking the real number               (...)
 minimum of the two by considering them as both non-negative real numbers is
 the same as taking the minimum of the two by only considering them as both           lemma coe_mono : Monotone ((↑) : ℝ≥0 →
 real numbers.                                                                        ℝ) :=
                                                                                            fun _ _ => NNReal.coe_le_coe.2
                                                                                                                                               Compiled Feedback
 [Proof]:
 1. Given two non-negative real numbers, `x` and `y`:                                                                                  'severity': 'error',
                                                                                      [Statement]:
       We can consider them as non-negative real numbers;                                                                              'pos': {'line': 613, 'column': 3},
                                                                                      theorem coe_min :
       We can also consider them as regular real numbers.                                                                              'endPos': {'line': 613, 'column': 26},
                                                                                           ((min (x : ℝ≥0) y : ℝ) : ℝ) = min (x : ℝ)
                                                                                      y :=
                                                                                                                                       'data': 'type mismatch
 2. Since the value order is preserved when viewing a non-negative real number                                                               Monotone.map_min coe_mono has type
 as a real number, the order relationship between `x` and `y` remains the same                                                               ↑(min ?m.78355 ?m.78356) = min ↑?
 whether we view them as non-negative real numbers or real numbers.                                                                    m.78355 ↑?m.78356 : Prop
                                                                                      [Proof]:                                               but is expected to have type
 3. Because this order is preserved, the minimum of `x` and `y` is the same.
                                                                                           NNReal.coe_mono.map_min                           min (↑x) y = min (↑x) y : Prop'




                 Informalization                                                                                                                Compiler-Guided
                                                              Process-Driven Autoformalization
                                                                                                                                               Process Annotation
                                                                                                                                       [Statement & Proof]:
                                                                                                                                       theorem coe_min :
                                                                                                                                            ((min (x : ℝ≥0) y : ℝ) : ℝ) = min (x : ℝ)
                                                                                                                                       b :=
                                                                                                                                            NNReal.coe_mono.map_min
                                                                                                                                                  Successful        Compile error
               Mathlib4 Library                                     Verified Formal Language

 [Statement]:                                               [Statement]:
 theorem coe_min (x y : ℝ≥0) :                              theorem coe_min (x y : ℝ≥0) :
      ((min x y : ℝ≥0) : ℝ) = min (x : ℝ) (y : ℝ) :=             ((min x y : ℝ≥0) : ℝ) = min (x : ℝ) (y : ℝ) :=                             Process-Supervised Verifier


 [Proof]:                                                   [Proof]:
      NNReal.coe_mono.map_min                                    NNReal.coe_mono.map_min




Figure 1: PDA trained on FORML4 ( image from [56]). PDA is aimed at statement autoformalization
rather than proof translation; proof steps are included to let the Lean compiler provide process-level feedback
when jointly compiling the statement and proof steps. In the depicted example, the statement parses but a
proof-step error reveals an incorrect autoformalization, guiding refinement [56].)


[2]. Some recent introductions to Lean are [7, 55]. To give a flavor of Lean, Figure 1.1 shows a short Lean proof
excerpt (adapted from [7]). We will save more detailed discussion for our actual topics, but at first glance
one sees programming code not too different from familiar languages such as Python and Mathematica.
This is correct, with the crucial difference that the operations, both predefined and user defined, are all
constrained to perform sound logical deductions. The elementary steps include applying rules of logical
inference, bringing in axioms, substituting variables and so on. By the use of subroutine definitions and the
sophisticated dependent type system, logical arguments composed of many, many elementary steps can be
expressed concisely. If suitably written, Lean code can be executed in the same way as other programming
languages. But one also has the option to use non-computable logical arguments, such as the principle of
the excluded middle (for any X, one of X or not X must be true). Thus Lean and the other advanced ITP
systems are capable of expressing any mathematical statement and of verifying proofs which use the full
range of mathematical technique.
    Clearly a technology which speeds up proof and is able to verify it in complete rigor would be extremely
valuable throughout the mathematical sciences. Mathematics journals are notorious for their lengthy review
times, and this is largely because checking all of the details of a proof is laborious and time-consuming.
Even then there is no guarantee; there are famous cases of proofs which were published and generally
accepted, only for flaws to be found later. In addition to verification, another major benefit of ITP is that
it facilitates collaboration. Often the main bottleneck in assembling a large collaboration is the need to vet
the contributors and verify their contributions; this difficulty could be largely removed. For these reasons,
mathematicians are excited about the potential of ITP [90].
    How excited should theoretical physicists be about ITP? One significant barrier is that formalization, at
least in its current state, requires all arguments to be stated with precise definitions and complete proofs,
whereas much of the physics literature deliberately operates at a looser level of rigor. We will further discuss
advantages of this flexible style below §1.3, but one must admit that it introduces substantial ambiguity into
scientific communication. An example in the context of QFT is the definition of a path integral, which is


                                                                                              4
very nontrivial and involves many choices which are often left implicit, so that claims based on it must be
carefully re-evaluated in each new application. By contrast, mathematical rigor and even more so formal
rigor force every mathematical object to be explicitly defined and every assumption to be stated. In doing
so, one must articulate clearly the mathematical content of a theory and the precise hypotheses under which
the arguments are valid, often revealing hidden assumptions that were taken for granted. The resulting
framework, while more demanding to construct, provides a shared and unambiguous foundation that can
facilitate collaboration and long-term reuse of results, even in very different contexts.
    Whatever one thinks about the advantages and disadvantages of rigor, as formalization exists now it
must be based on rigorous mathematics. And as any physicist who has tried to read mathematical physics
knows, the structure of the discussions and proofs is rather different from most of theoretical physics, with
a heavy reliance on functional analysis. This added precision can be advantageous, but not always. Is it
really true that we need rigor for formalization? Could formalization be based on some other foundations
more analogous to standard physical reasoning? We will return to these questions in the conclusions. But to
use ITP now, we must formalize a piece of mathematical physics which is rigorously stated and proven. An
important example is the problem of rigorously defining QFT and proving that examples exist, often called
“constructing” the QFT. This has been much studied and there are many results to draw on. We chose a
relatively simple but very foundational project to find out whether formalization is now practical. And we
learned quite a lot doing it, about the mathematical physics, about theorem proving and about AI, which
we report here.
    Formalization could be of great value to both math and physics. Yet the first question is, is it practical
to formalize research level mathematical physics such as QFT at all? Why was this not already done?

1.2    ITP in the age of AI
As we write this in early 2026, ITP has not yet had a major impact on how mathematics research is done.
One reason arises from the observation that much of mathematics builds on a deep structure of definitions
based on other definitions, which takes years of study to gain even a basic familiarity. This is also true
of much of theoretical physics. Now, to formalize a piece of mathematics, its prerequisite definitions and
background theory must already be available in the library to build on; in practice one may initially omit
some proofs by treating results as unchecked “axioms” while continuing development. But even with this
relaxed standard, only a tiny fraction of mathematics has been fully formalized so far [59]. Until substantially
more of the mathematical corpus is formalized, the scope of ITP will remain limited. Moreover, even after
researchers formalize important theorems of value to the broader community, the process of integrating their
work into a foundational library is slow. This is for good reasons: there are important standards upheld by
Mathlib for new code to be integrated into the library, namely it should be humanly readable and follow
community-developed principles of programming and mathematical organization. Still, this seems to be a
serious bottleneck to wider adoption of the technology.
    Furthermore, ITP has a steep learning curve for new users, taking months of study to gain even moderate
proficiency [93, 100]. Formalization is laborious, even for experts. This contrasts with tools like computer
algebra which can be profitably used after a few days of study. Historically, it has taken around a week to
formalize a single page of a textbook [95]. The Lean Mathlib library [55] is growing at about 300K lines/year;
taking into account that a formal proof is about 5 times as long as an informal proof this corresponds to the
entire community of several hundred active contributors formalizing about one textbook every 2 months.
At present Mathlib has fairly good coverage of the undergraduate math curriculum, but at this rate it will
take many years to formalize the prerequisites for research level topics in differential geometry, PDE, Lie
algebras and groups, and so on. Another library PhysLean [94] has been started with a focus on physics
formalization, but these gaps remain. Thus until recently, the answer to the question we raised on the
practicality of formalizing constructive QFT was, not really.
    However, this situation is rapidly improving. Automated theorem proving technologies such as Isabelle’s
“Sledgehammer” [13], and newer protocols for agentic interaction with Lean via the Model Context Protocol
(MCP) [68, 31, 62] have made steady progress. Of potentially greater import, one can apply modern AI to
interactive theorem proving; this direction, often referred to as AI for theorem proving (AITP), has been
actively pursued since at least 2015 [1, 3]. Many experts believe this direction is starting to take off; for
example, DARPA’s expMath initiative aims to radically (“exponentially”) accelerate the rate of progress in


                                                       5
pure mathematics by developing AI systems for decomposition and autoformalization [24]. At this rate, even
the present Lean community could formalize 600 textbooks/year and rapidly bring much of math and physics
into the scope of ITP. And if the techniques become easy to learn, one can foresee widespread adoption.
    There are several AITP paradigms. One is to view proof search as a game-like sequential decision
process (often likened to solitaire), and to apply game-playing methods such as reinforcement learning (RL)
and Monte Carlo search [46, 11]. The power of RL was famously demonstrated by AlphaGo and AlphaZero
[84, 85], and AlphaProof is a recent example in formal mathematics, combining RL with formal verification
inside Lean [47].
    Another paradigm is to view formalization as a form of language translation and to automate it, autofor-
malization, using AI methods for language translation [56, 77]. This naturally connects with the remarkable
recent development of large language models (LLMs) [32, 69], which have revolutionized computational
linguistics, and are now revolutionizing computer programming and many of the other tasks which lie at
the heart of computing. LLMs have remarkable problem solving and reasoning abilities and are advancing
rapidly. There are even projections that “artificial general intelligence” (an ill-defined term) will be achieved
soon. Some AI researchers believe that AITP will be a central part of this. One argument is that the most
successful AI technologies are statistical and destined to make errors (at least occasionally), so to make long
correct chains of argument they must be coupled to a verification engine such as an ITP system.
    The imminent prospect of AI’s doing math and science is raising questions which a few years ago would
have been dismissed as science fiction. Already AI is far faster and more prolific in generating results than
any human. Soon the bottleneck will not be writing the papers, it will be reading the papers! How will we
understand all of this new science? A first step towards understanding is simply to be convinced that the
claims and arguments are correct, how can we convince ourselves that a long paper full of intricate arguments
is correct? Math is already bottlenecked by review time.
    Formalization provides a partial answer. It is a way that the computer can reliably certify that assump-
tions A, B, C imply consequences X, Y, Z. It does not completely solve the problem, after all we still need to
convince ourselves that A, B, C were the right assumptions and X, Y, Z answer our questions. But it would
be a great help.
    We leave further discussion and speculation for other venues, but the point we draw from this is that ITP
technology is advancing quickly and we expect the problems of practical difficulty and insufficient libraries
to be largely solved over the next few years (the first author has consistently predicted this by 2030 in many
talks as far back as 2019 [27]). We will report below on our experience using the existing tools for theorem
proving, and we do see rapid progress: our ability to do ITP with mid-2025 tools was far greater than it was
at the beginning of that year, and the early 2026 tools are noticeably better still. It seems entirely possible
that, over the coming years, AI will so much enhance our abilities (or even achieve superhuman abilities) that
the advantages of rigor and formalization will far outweigh the remaining disadvantages. Thus we believe
that yes, theoretical physicists should be excited about ITP.

1.3    Comparing Styles of Reasoning in Physics and Mathematics
A strength that physicists claim over mathematicians is that looser levels of rigor allow them to see far
beyond what they can prove [33]. One joke has it that “Mathematicians are proving what physicists have
known for years.” A less physics-centric observation is that in exploratory work, before ideas take their final
form, often it is better to maintain flexibility. As Niels Bohr famously said, “Never express yourself more
clearly than you are able to think” [74].
    However, mathematical concepts often arise independently of physics, yet later map onto nature with
striking success [96]. Mathematics has obvious implications for physics research, starting with the need for
physical theories to be mathematically consistent. Mathematicians can unblock technical barriers of physics
by providing new mathematical machinery and frameworks. Novel theorems can make complex physical
arguments manifestly true. However, physics is having more and more impact on mathematics. There is
a real advantage to making squishier conjectures and using less precise definitions of the objects one is
reasoning about. Reasoning under uncertainty about the features and transformations which apply to an
object is something physicists thrive on [6].
    As our understanding of the natural world evolves, our frameworks, definitions, and understanding of
relevant key features of a system evolve. Kuhn’s account of scientific development distinguishes periods


                                                       6
of “normal science,” in which a community works within a shared paradigm to solve well-posed puzzles,
from rare episodes of “scientific revolution,” in which persistent anomalies provoke a crisis and are resolved
only by a reorganization of the field’s core conceptual framework. On this view, mature formalisms and
tightened standards of admissible argument are not neutral, they are part of what defines a paradigm and
stabilizes normal science. This stabilization is productive, but it can also make conceptual innovation harder:
anomalies that resist expression in the reigning formalism are more likely to be treated as technical puzzles,
deferred, or re-described, rather than as pressure toward a new framework. If so, a comparative advantage
of physicists’ informal, heuristic style is that it can generate candidate re-conceptualizations and partial
“exemplars” more quickly than fully rigorous approaches can, supplying the kinds of alternatives Kuhn
argues are necessary for genuine paradigm change [54].
    On a more practical level, one of the greatest difficulties we encountered is that the long algebraic
calculations which are common in theoretical physics can be quite difficult to formalize in Lean. This is
somewhat ironic as when used in the proper contexts, algebraic arguments are rigorous. We will return to
this issue in the conclusions.

1.4    Brief status report on rigorous QFT with respect to the Mass Gap Problem
This section is written to put this project in the context of Yang-Mills, and to discuss recent developments
in progress towards the mass-gap problem. The mass gap problem is the question of whether quantum
Yang–Mills theory, the mathematical framework underlying the strong interaction, can be defined rigorously
in four dimensions and proved to have a positive gap between the vacuum state and the lightest possible
excitation. Informally, even though the classical gauge fields are “massless,” the quantum theory appears
to produce only particles with nonzero minimum mass. The Clay Mathematics Institute formulates this as
proving that for any compact simple gauge group, a nontrivial quantum Yang–Mills theory exists on (R4 )
and has a mass gap (∆ > 0). The mass gap problem is of interest to physicists because this gap is tied
to the observed short-range, confining behavior of the strong force and to why free gluons are not seen
experimentally, so solving the problem would put one of the Standard Model’s most successful pieces on
a fully rigorous mathematical foundation rather than the current mix of physical evidence, approximation
methods, and lattice simulations [23].
    In the 1970s there was a great effort among mathematical physicists to make the construction of interact-
ing quantum field theories mathematically rigorous. A successful approach has been to construct a Euclidean
version of the theory and then rigorously apply a Wick rotation procedure to construct the original quantum
field theory. This approach is all based on a reconstruction theorem carrying out the Wick rotation proce-
dure, provided the Euclidean theory satisfies a set of axioms known as the Osterwalder-Schrader (OS) axioms
[70]. Around the same time there was a huge effort to construct Euclidean scalar quantum field theories.
This program succeeded in the construction of the Euclidean P (Φ)2 and Φ43 theory were constructed along
with the verification that they satisfy the OS axioms (See i.e. [38, 87] for an overview of these results). On
the other hand, in four dimensions, heuristic calculations indicated that there are no nontrivial scalar field
theories, and it was rigorously verified that the Φ4d theory is trivial for d ≥ 5 [4]. Much more recently, this
was also verified for d = 4 [5]. But despite this, it is widely believed that the four dimensional Yang–Mills
theory can be rigorously constructed, and there are strong physical and computational arguments that it is
nontrivial and has the mass gap property.
    There has been a recent revival of interest in Yang–Mills theory and constructive quantum field theory
in the math community. This is partially due to the introduction of regularity structures and paracontrolled
calculus techniques in the theory of singular stochastic partial differential equations [42, 39]. Due to these
technical breakthroughs, the stochastic quantization program for constructing Euclidean field theories has
been carried out for the Φ43 theory, and part of the program has been carried out for pure Yang-Mills and
Yang-Mills-Higgs in 2d and 3d [20].
    One approach to the problem is by taking continuum limits of lattice Yang–Mills model. In four space-
time dimensions, continuum limit convergence for the Abelian lattice theory was proven by Driver [28], and
significant progress towards convergence for the non-Abelian theory was made by Balaban (i.e. [10, 9]).
The two dimensional non-Abelian pure Yang–Mills theory is relativey easy to construct via gauge symmetry,
however constructing even the 2d Yang–Mills–Higgs theory or 3d pure Yang–Mills theory in the continuum
is still open


                                                      7
    Moreover, since Wilson’s proposal to define non-Abelian gauge theory nonperturbatively via Euclidean
lattice regularization [98], lattice gauge theory has become a very important tool for strongly-coupled Yang-
Mills. For instance, a simple cluster expansion argument shows that at very strong coupling, lattice Yang–
Mills theories exhibit a mass gap and area law [72], and more recently gauge–string duality and stochastic
quantization based approaches weakened the requirement on the coupling [83, 19, 18, 67]. In parallel,
the large-N limit has has become a complementary organizing principle for nonperturbative Yang-Mills,
where lattice computations produce quantitative evidence that many infrared observables admin a smooth
extrapolation as N = ∞. The pure Yang–Mills N = ∞ limit has also recently been proven to exist and has
been described rather explicitly in terms of rigorously defined surface sums or string trajectories [21, 14].
These conceptual and computational advances underpin increasingly precise nonperturbative determinations
of Yang–Mills observables (e.g. glueball spectroscopy and related continuum extrapolations) [64].
    From a constructive perspective, lattice gauge theory is compelling because it supplies an ultraviolet-
regularized, gauge-invariant definition of the theory at finite lattice spacing; the central mathematical chal-
lenge is to understand (and ultimately prove) the continuum limit and its universality class. In four dimen-
sions this is intimately tied to the Clay Millennium Yang–Mills existence and mass gap problem [49]. What
is missing is a fully rigorous control of the renormalization/continuum-limit map for non-Abelian gauge the-
ories that would (i) construct a continuum Wightman/OS-compatible theory from the lattice, (ii) identify
the emergent long-distance physics (confinement, mass gap, string tension), and (iii) prove that physically
relevant observables are independent of microscopic discretization choices (universality). Even at a more
structural level, lattice gauge theory exposes deep issues mathematicians can engage with: reflection posi-
tivity and reconstruction (for connecting Euclidean and Minkowski formulations), the analytic structure of
RG flows, and the subtle interplay between topology and locality (e.g. topological charge sectors becoming
sharply separated in the continuum as illuminated by Wilson flow) [58]. Finally, the fermionic sector poses
“mathematics-first” problems: implementing chiral symmetry and anomalies without doublers [36, 57, 66]
is now conceptually clean but still raises hard questions about locality, index theorems at finite cutoff, and
extensions toward genuinely chiral gauge theories. A classic reference framing many of these issues explic-
itly as problems in constructive QFT/statistical mechanics is Seiler’s monograph [82], and the foundational
lattice formulation and its statistical-mechanical structure are laid out in Wilson/Kogut [97, 52].

1.5    Related work
While we know of no previous formalizations of constructive QFT, a significant related project is the Brow-
nian motion project of Remy Degenne et al [26], RemyDegenne/brownian-motion . This contains the Kol-
mogorov Extension theorem, in RemyDegenne/kolmogorov extension4, which is imported by our proof of
Minlos.
    The two axioms we initially introduced in our formalization, Minlos theorem and one to prove nuclearity
of Schwartz space, were proven in our subsequent formalization. Moreover, the dependence on Goursat’s
theorem was also removed in our subsequent formalization. At this writing there are three axiom-free
constructions. Matteo Cipollina has independently formalized the proof of nuclearity and a construction
of the Gaussian measure to obtain an axiom-free proof of OS in or4nge19/OSforGFF. The first author
(MRD) has independently formalized the proofs of these theorems and adapted our formalization to use
them, in the repos mrdouglasny/gaussian-field and GFF4D. In addition the repo mrdouglasny/bochner
has proofs of the Bochner and Minlos theorems, which are imported by our final released construction in
mrdouglasny/OSforGFF. The original construction with 3 axioms is preserved in the “original” branch of
that repo.


2     Axiomatic QFT and Constructive Frameworks
To rigorously prove that a QFT exists, one must define the properties that a mathematical object must
possess to be considered a QFT, and then construct such a mathematical object. In this section, we will
give an overview of some of the most influential approaches to developing an axiomatic definition on a QFT.
    In physics, a QFT can be defined in several ways: a quantum mechanical system with Lorentz covariance
and causality; a path integral over fields on Minkowski space-time; the related path on Euclidean space-time
obtained by Wick rotation; and other possibilities. Each way can be codified by an axiomatic approach, in


                                                      8
which one specifies the data (or set of observables) that determine the QFT, and a short list of axioms the
data must satisfy. The axioms include restatements of the physical principles and consistency conditions,
and additional “technical” assumptions which facilitate the mathematical arguments. One can then prove
reconstruction theorems which, given the QFT data of one axiomatic approach, show that the data in another
approach is uniquely determined and satisfies the axioms of that approach.
    In the rest of the section we will survey some of the most influential approaches to axiomatizing QFT and
explain their relations. The three main approaches are the Wightman axioms [35], the Osterwalder-Schrader
(OS) axioms [70], and the Haag-Kastler axioms [41]. Both the Wightman and Haag-Kastler axioms formulate
a QFT in Minkowski spacetime, the first in terms of correlation functions and the second in terms of C ∗
operator algebras. The OS axioms axiomatize QFT in Euclidean space-time. Other important approaches
are the CFT approaches using operator product expansions or sewing axioms, and factorization algebras.
    The most direct approach is to formulate the QFT in the usual language of quantum mechanics, with a
Hilbert space, a Hamiltonian and field operators. These must satisfy the Wightman axioms, which express
Lorentz invariance, microscopic causality, and the existence of a vacuum state. Physically, this is the original
definition of QFT; the other approaches are justified by their relation to it. Assuming the Wightman Axioms,
one can rigorously prove the CPT theorem and the spin-statistics theorem [88, 50].
    Given field operators and a vacuum state, one can define the vacuum expectation value of a product of n
operators, the Wightman distributions on M n . The Wightman reconstruction theorem shows that this data
uniquely determines the original QM formulation [35]. Wightman distributions can be analytically continued
to complex time and thus to Euclidean spacetime. The analytically continues objects are called Schwinger
functions, which are non-singular on n-tuples of points in M d which are pairwise distinct [70]. Schwinger
functions are the defining observables of Euclidean QFT, and can be summarized in a generating function
(3.3).
    In the Euclidean approach to constructive QFT one typically requires the Schwinger functions, or equiv-
alently a generating functional that determines the Schwinger functions to satisfy the Osterwalder-Schrader
axioms [70]. The corrected Osterwalder-Schrader reconstruction theorem [73] shows that the Schwinger
functions obeying the Euclidean axioms together with an additional growth condition are sufficient to en-
sure temperedness and admit an analytic continuation to Minkowski-space Wightman distributions which
satisfy the Wightman axioms. Hence, to be precise the 1975 reconstuction theorem revises the original 1973
Osterwalder-Schrader formulation by adding an extra regularity/growth input. In this framework, reflection
positivity is the crucial Euclidean remnant of Hilbert space positivity after Wick rotation. A stronger but
sufficient framework is the Glimm and Jaffe [38] measure theoretic formulation, which assumes a Euclidean
probability measure on a space of distributions and imposes stronger regularity conditions adapted to con-
structive proofs. While this is more restrictive than the abstract Schwinger function setup, it is often more
technically convenient in application, and certainly more friendly to formalization efforts.
    In Haag-Kastler (or algebraic QFT) one replaces point-like fields by a net of local observable algebras
where to each suitable spacetime region one assigns a C ∗ algebra (for a fixed representation of a von Neumann
algebra) of observables localized in spacetime [41]. In a vacuum representation one further assumes a vacuum
vector that is cyclic for the quasilocal algebra together with the positive conditions for the translation group.
    In conformal field theory (CFT), it is often natural to take as fundamental the spectrum of local op-
erators (e.g. primaries) and their operator product expansion (OPE). Schematically, for local operators Oi
one posits an expansion valid inside correlation functions, where conformal symmetry fixes the spacetime
dependence of Cij k up to numerical OPE coefficients and representation-theoretic data [12, 78]. In unitary
CFTs one can make this precise: the OPE and conformal-block decomposition converge inside correlators in
an appropriate domain, with a finite radius governed by the operator-insertion geometry [75]. Consistency
of performing OPEs in different channels for a four-point function yields crossing symmetry constraints
(bootstrap equations), which can be treated analytically in special cases and numerically in general [79, 78].
    In two dimensions one can also formulate CFT globally via sewing/gluing axioms. Segal’s functorial
axioms encode the assignment of state spaces to boundary circles and amplitudes (linear maps) to Riemann
surfaces with parametrised boundaries, subject to compatibility with gluing of surfaces [81]. Related sewing
constraints provide field-theoretic control of how correlators behave under cutting and gluing, and play a
key role in rational CFT and the Moore–Seiberg consistency conditions [63].
    The primary reason we formalized Glimm-Jaffe [37] rather than other approaches is that their axiomatic
framework turns the problem of defining a QFT into that of defining a functional measure (a path integral),


                                                       9
which in many interesting cases (scalar fields with a real action, pure Yang-Mills theory) is a probability
measure (real and non-negative). Measure theory and probability are relatively well covered by Lean Mathlib.
By contrast, Mathlib currently lacks a sufficiently developed theory of operators on Hilbert spaces, as well
as sufficient complex analysis and Riemann surface theory for the 2d CFT approaches.
    In this paper, we constructed the free scalar field using the GJ construction and proved that it satisfies
the given axioms. This is an important proof of concept that given the existing Lean libraries (Mathlib) and
AI tools, such construction is already possible, and will only be more efficient in the future. Next milestones
would be to prove the OS reconstruction theorem [38], to construct free fermions, and interacting theories
in two dimensions.


3     Introduction to the mathematics
We generally follow the notation of Glimm and Jaffe [37], and our precise notations are in appendix A. We
treat a free massive scalar field in D = 4 Euclidean dimensions; while the strategy and arguments work in
any dimension, some results on the covariance would require adaptation for other dimensions.
    In physics terms, we want to define a functional measure which naively looks like
                                                Y
                                        dµ[ϕ] ∼    dϕ(x) exp(−S[ϕ])                                  (3.1)
                                                   x

with the action                                   Z
                                              1
                                       S[ϕ] =          dD x (∂ϕ)2 + m2 ϕ2                                 (3.2)
                                              2    M
with m2 > 0. ThisQ is naive as Eq. (3.1) cannot be interpreted as a product of an infinite dimensional
Lebesgue measure x dϕ(x) with the weight exp(−S[ϕ]) as the first of these does not exist. Rather, the
measure must be constructed by other means.
   The Glimm-Jaffe axioms are stated in terms of the generating functional of correlation functions,
                                           Z R
                                                    D
                                   S(J) := ei M d x J(x)ϕ(x) dµ[ϕ].                                  (3.3)

In a physics treatment we could immediately write it down for the free field,
                                        Z
                                                     D  D
                                             R
                                 S(J) := eic M ×M d x d y J(x)K(x−y)J(y)                                  (3.4)

where K(x − y) is the propagator (Green function for ∆ + m2 ) or covariance (in the language of probability
theory).
    However, from a rigorous and even more so from a formal perspective, we have things to define and
prove. What is K? Under what conditions on J does Eq. (3.4) make sense? But the first order of business
is to show that there exists a measure dµ[ϕ] for which Eq. (3.3) equals Eq. (3.4). Conceptually this is
not difficult; essentially, we want to diagonalize K(x − y) and define dµ as the product of one-dimensional
Gaussians over its eigenspaces. However there are some technical obstacles to doing this which we discuss
below and which led us (in version 1) to appeal to a general existence theorem due to Minlos for this step.
    Suppose we have this measure, next we need to show that this statistical field theory can be related to
a true quantum field theory with a Hilbert space, Hamiltonian, and Lorentz symmetry. This follows from
the Osterwalder-Schrader reconstruction theorem [71] (and subsequent work [73]). In these works it was
shown that this will be the case if Eq. (3.4) satisfies a short list of “OS” axioms. There are variations on
the original axioms, we follow the set in Glimm-Jaffe.
    • OS0: Analyticity- The functional S(f ) is analytic. More precisely for every finite set of test functions
      fj ∈ D(RD ) with j = 1, 2, . . . , N, and taking ⃗z = (z1 , . . . , zn ) ∈ Cn , the function
                                                                            
                                                                    Xn
                                            (z1 , . . . , zn ) → S    zj fj                             (3.5)
                                                                  j=1

      is entire on CN .


                                                        10
• OS1: Regularity- There exists a real number p with 1 ≤ p ≤ 2 and a constant c > 0 such that, for
  every test function f ∈ D(Rn ),
                                               h                 i
                                   S{f } ≤ exp c ∥f ∥L1 + ∥f ∥pLp .                          (3.6)

  If p = 2, we further assume that the two-point Schwinger function

                                                      ∂2     
                                  S2 (x, y) :=              S z1 δx + z2 δy                       ,
                                                    ∂z1 ∂z2                           z1 =z2 =0

  is locally integrable in (x, y) and is defined in our generating functional, S(f ) = eiϕ(f ) dµ. Let dµ be
                                                                                      R

  a probability measure on D′ (RD ) which satisfies OS0. Then the measure dµ has moments of all order.
  The nth-moment has a density Sn (x1 , . . . , xn ) ∈ D′ (RD ) which means
                              Z                             Z                         n
                                                                                      Y
                                  ϕ(f1 ) . . . ϕ(fn )dµ =       Sn (x1 , . . . xn )         fi (xi )dx    (3.7)
                                                                                      i=1

  is locally integrable in (x, y) ∈ RD × RD .Note that for p = 2 then ||f ||L2 gives us a Hilbert space norm
  which is useful for Fourier analysis and two-point functions.
• OS2: Euclidean Invariance- S(f ) is invariant under Euclidean symmetries (translations, rotations and
  reflections). More explicitly, for any such Euclidean isometry of RD , E, we have,

                                                       S(f ) = S(Ef ).                                    (3.8)

  Equivalently, dµ is Euclidean invariant in the sense that µ = E∗ µ where E∗ µ denotes the pushforward
  of µ under E.
Before moving on to OS3 and OS4, we isolate a class of functions on D′ (RD ),
                                        N
                                        X
                        A = {A(ϕ) =              cj exp(ϕ(fj )) : cj ∈ C, fj ∈ D′ (RD ))}.                (3.9)
                                           j=1


• OS3: Reflection Positivity- The Euclidean symmetries act on D′ (RD ), so that Eϕ(f ) = ϕ(Ef ) , which
  defines a unitary condition action on the L2 (µ). Finally, let A+ ⊂ A be the set of functionals where
  fj ∈ C0 (RD              D
             + ) and C0 (R+ ) is the space of continuous functions that vanish at infinity in the positive
                D
  half space. R+ := {(t, ⃗x) : t > 0} so now if we let θ : (t, ⃗x) → (−t, ⃗x) be the time reflection. Then the
  content of this axiom states that the inner-product inequality is satisfied:
                                       Z
                                         (θA)− A dµ = ⟨θA, A⟩L2 (µ) ≥ 0.                                (3.10)


• OS4: Ergodicity- The time translation subgroup T (t) acts ergodically, meaning it upholds the unique-
  ness of the vacuum, on the measure dµ. The time translation subgroup in Euclidean space is the one
  parameter group of pure time shifts

                                     T (t) : x = (t, ⃗x) → (t + t′ , ⃗x)              t′ ∈ R             (3.11)

  so that T (t + s) = T (t)T (s).
  This is equivalent to saying that for all L1 (µ) functions A(ϕ),
                                           Z t                               Z
                                       1                         −1
                                   lim           T (s)A(ϕ)T (s)       ds =       A(ϕ)dµ(ϕ),              (3.12)
                                  t→∞ t     0

  where the limit above should be taken in the L1 sense.


                                                          11
Remark 3.1 (Schwartz functions vs compactly supported test functions). In OSforGFF, instead of working
with the spaces D(RD ) and D′ (RD ), our axioms and proofs were stated in terms of Schwartz functions S(RD )
and tempered distributions S ′ (RD ). Since D(RD ) ⊂ S(RD ) and S ′ (RD ) ⊂ D′ (RD ), our axioms imply the
ones stated in Glimm and Jaffe.
Remark 3.2 (OS4 Ergodicity Statement). When Glimm and Jaffe write T (s)A(ϕ)T (s)−1 , they interpret
A(ϕ) and T (s)A(ϕ)T (s)−1 as linear operator on the space of functions D′ (RD ) → C where A(ϕ) is a
multiplication operator. Unpacking the definitions one can check that (3.12) is equivalent to
                                           Z t                   Z
                                       1
                                   lim           A(T (s)ϕ)ds =       A(ϕ)dµ(ϕ),                         (3.13)
                                   t→∞ t    0

where we now treat A simply as a function on D′ (RD ).
   In OSforGFF, the OS4Ergodicity axiom is stated only for functions in A instead of for all L1 (µ) functions,
and we use L2 convergence instead of L1 convergence. Our axiom implies Glimm and Jaffe’s axiom, since
a general functional analytic argument shows that A is dense in S ′ (RD ) with respect to L1 norm, and L2
convergence implies L1 convergence on probability spaces.
Remark 3.3 (OS4 Clustering). In OSforGFF, we also include two alternate stronger versions of the OS4
called OS4Clustering and OS4PolynomialClustering which are stated below. As before S[f ] denotes the
generating functional of the measure µ

    1. (OS4Clustering) For any f, g ∈ S(RD ),

                                            S[f + T (s)g] − S[f ]S[g] → 0                               (3.14)

      as s → ∞.

    2. (OS4PolynomialClustering) For any f, g ∈ S(RD ), and any n > 0, there exists a constant Cf,g,d,n

                                  |S[f + T (s)g] − S[f ]S[g]| ≤ Cf,g,d,n (1 + |s|)−n .                  (3.15)

Of course OS4PolynomialClustering implies OS4Clustering. We will sketch in Section B.5 why these clus-
tering variations imply the original ergodicity axiom.


4     Details of the formalization
Here we comment on some choices we made and points where we encountered technical difficulties. The full
proof is given in appendix B. We strongly encourage the reader interested in more detailed explanations to
clone our repo, fire up a coding agent and ask it your questions.

4.1     Construction of Gaussian Free Field
We construct the Gaussian free field (GFF) as a generalized random field by applying Minlos’ theorem to
a canonical Gaussian characteristic functional on a nuclear space of test functions. An equivalent “mode
expansion” construction as an infinite sum of independent Gaussian random variables, which is more familiar
to physicists, is explained in 4.3.
    Let E be a real nuclear locally convex topological vector space and let E ′ denote its continuous dual. We
write ϕ(f ) for the canonical pairing ϕ ∈ E ′ , f ∈ E. A function χ : E → C is called positive definite if for
every n ∈ N, every f1 , . . . , fn ∈ E, and every c1 , . . . , cn ∈ C,
                                           n
                                           X
                                                   ci cj χ(fi − fj ) ≥ 0.
                                           i,j=1




                                                          12
Theorem 4.1 (Minlos). Let E be nuclear. If χ : E → C is continuous, positive definite, and normalized by
χ(0) = 1, then there exists a unique Borel probability measure µ on E ′ such that for all f ∈ E,
                                                  Z
                                        χ(f ) =        e iϕ(f ) dµ(ω).
                                                     E′

Equivalently, every continuous positive-definite functional on a nuclear space is the Fourier transform (char-
acteristic functional) of a unique probability measure on the continuous dual.
   Fix a domain or manifold M and choose a space of test functions E (in our case E = S(Rd )). Let

                                               C :E×E →R

be a continuous, symmetric, positive semidefinite bilinear form, interpreted as the covariance form. The
GFF is defined by                    Z
                                             m
                          C(f, f ) ≡                K1 (m|x − y|)f (x)f (y) dx dy                    (4.1)
                                       4π 2 |x − y|
and                                                            
                                                       1
                                          χ(f ) = exp − C(f, f ) .                                         (4.2)
                                                       2

4.2    Schwartz Test Functions
Lean Mathlib already has the definition of Schwartz functions and many of their properties. Examples of
properties we had to prove include double mollifier convergence and various Fubini lemmas. The former
allows the definition of Schwinger two-point functions, which is an integral involving a singularity at x = y
in K(x, y). The Fubini lemmas are necessary to exchange orders of integration, e.g. spacetime integral and
momentum integral, and they require the absolute convergence of integrands. The convergence of regular
Schwartz function integrals are easy as we can impose arbitrary polynomial bound; yet, there are subtleties
when the free covariance (Green’s function) is involved, which is discussed in appendix B. Some of these are
general results which could be “upstreamed” into Lean Mathlib (work in progress).

4.3    Motivation for the definitions
For a physics reader there is already a lot to unpack and motivate, in particular, the function spaces and
other unfamiliar terminology. Where does this come from? We will not try to give a complete answer here,
but let us explain the motivation for the use of Schwartz spaces, the concept of Gel’fand triple, and the
Minlos theorem.
    First, what is dµ(ϕ)? Mathematical probability theory is basedR on measure theory (Kolmogorov); the
probability that a random variable x will take values in a set S is S dµ(x). For us the random variable is
the field configuration ϕ(x), which (naively) is a function from spacetime M to R. We will define the set of
all of its possible values as the configuration space C (the type FieldConfiguration in our formalization).
    The way that physicists usually construct an infinite-dimensional field space is to use a series of finite
dimensional spaces CN , which approximate C arbitrarily well as N → ∞. A standard choice is to discretize
by only keeping the function values at lattice points ZD ·a for some lattice spacing a, and take (say) a = 2−N .
We would also have to take the total volume finite and explicitly take the infinite volume limit. We could then
define the measure by taking the product Lebesgue (uniform) measure over all the lattice points, approximate
the action in a standard way say by taking ∂ϕ → (ϕ(x + a) − ϕ(x))/a, and then write an explicit Gaussian
weight. This is perfectly rigorous and a viable approach, why should we consider alternatives?
    One answer is that proving the existence of the limiting measure is nontrivial, and this does not save as
much work as one might think. Another is that, while approximations are not intrinsically problematic, it
is preferable that they preserve the very properties one ultimately wishes to prove. In particular, a lattice
approximation breaks the full Euclidean invariance appearing in OS2 from the outset. Since there are no
nontrivial finite-dimensional representations of the Euclidean group, preserving OS2 naturally leads one to
work with measures on infinite-dimensional function spaces.


                                                      13
   A conceptually simple construction, sufficient at least in the Gaussian case, is to diagonalize the covariance
(equivalently, the quadratic kinetic form) and write
                                                      X
                                             ϕ(x) =      ck ϕk (x),                                          (4.3)
                                                       k∈N

where the ck are independent centered Gaussian random variables of variance 1, and the mode functions ϕk
are chosen so that                                X
                                       K(x, y) =    ϕk (x)ϕk (y)
                                                       k∈N

reproduces the desired covariance kernel.
    However, this already raises a nontrivial issue: the covariance is represented by an infinite sum or integral
which need not converge pointwise. In the continuum theory this is not an accident but a manifestation of
ultraviolet singularity. Indeed, for the free massive field one has in momentum space
                                                             1
                                               K(p) =              ,
                                                         p2 + m2
and in D = 4 this is not trace class, since formally

                                                        d4 p
                                               Z
                                                      2      2
                                                               = ∞.
                                                  R4 p + m

Correspondingly, the position-space covariance K(x, y) is singular on the diagonal, so in particular K(x, x)
diverges. Thus the Gaussian field cannot be realized as an ordinary random function, but only as a random
distribution.
    One might think that this prevents constructing such a measure, and this would be the case if we required
it to have support on continuous functions, or even in the Hilbert space of functions on spacetime L2 (R4 ).
This corresponds to the (probably familiar) fact that a typical value of ϕ(x) in dimension D ≥ 2 is not a
continuous function.
    The solution to this problem is to broaden the support of the measure to distributions, i.e. linear
functionals on some restricted space of test functions. What space? We need test functions whose values
can be freely chosen on any finite set of points; we need them to have finite integrals against K(x − y), and
we need their integral over all of spacetime to be finite (since K is translation invariant).
    The space S(RD ) of Schwartz test functions is a common choice to satisfy these requirements, and is well
implemented in Mathlib. These are functions with rapid (faster than polynomial) decay in both position and
momentum space, and the spaces of Schwartz test functions and of distributions are preserved under Fourier
transform. One can describe them concretely using a basis of Hermite functions (normalized harmonic
oscillator number states) in an expansion analogous to Eq. (4.3),
                                                     X
                                             ϕ(x) =       ck ϕk (x),                                     (4.4)
                                                       k∈N

The test functions then have cn → 0 faster than any polynomial in n. The dual Schwartz distributions can
have cn growing at most polynomially–to be precise, there exists k such that
                                         X
                                             |cn |2 (1 + n)−k < ∞.
                                            n≥0


     While the space of Schwartz distributions S ′ (RD ) is large enough to contain our field configurations, we
still need to show that the sum in Eq. 4.3 converges with probability one. This places conditions both on
the space (the sum must be over a countable basis) and on the covariance.
     A key additional structural fact is that S(RD ) is a nuclear Fréchet space. Informally, nuclearity means
that the topology can be described by a nested family of Hilbert norms whose inclusion maps are extremely
compact (indeed trace-class in a suitable sense). This is precisely the infinite-dimensional regularity needed
to extend finite-dimensional Gaussian intuition to the continuum. In particular, by the Bochner–Minlos


                                                        14
theorem, every continuous positive-definite functional on a nuclear space is the Fourier transform of a unique
probability measure on its topological dual. Hence a Gaussian characteristic functional of the form
                                                        
                                                1
                                χ(f ) = exp − C(f, f ) ,         f ∈ S(RD ),
                                                2

defines a probability measure on S ′ (RD ). In this sense, nuclearity plays the role that tightness or compactness
plays in finite dimensions: it prevents probability mass from “escaping to infinity” when one passes from
finite-dimensional approximations to the full infinite-dimensional limit, and thereby underlies the existence
of the Euclidean field measure [38].
    The condition on the covariance can be stated in several ways: one is that it must be continuous in
the nuclear topology. More concretely, it must be definable by means of a linear operator T which densely
embeds the test function space into a Hilbert space,

                                              C(f, g) = ⟨T f, T g⟩,                                          (4.5)

and such that T is a Hilbert-Schmidt operator, tr T † T ≤ ∞. This would be false for T = (k 2 + m2 )−1/2
considered as a bounded operator on L2 (RD ), but if we instead consider it as an embedding of Schwartz
test functions into L2 it is true. This structure of a test function space with high regularity embedded in a
Hilbert space which itself is embedded into the space of distributions is called a Gel’fand triple (or rigged
Hilbert space) and is foundational for constructive QFT.
    For the future (renormalization of interacting theories) we want to use smaller spaces of distributions
with more regularity. Despite the seeming abstractness one could be more concrete about these spaces, for
example work on rigorous stochastic quantization uses Sobolev and weighted Sobolev spaces. One can still
construct the measure on S ′ and later argue that the measure has support on a smaller space. However
these function spaces are not yet in Mathlib.
    In the original formalization described here, we dealt with these matters by postulating the Minlos
theorem and the nuclear property of Schwartz space as axioms, and carefully checked them by hand. As
discussed in §1.5, we now also have axiom-free proofs which are available in the latest version of our repository.

4.4    Other infrastructure
    • We defined the Euclidean group action in the file Spacetime/Euclidean without much help from
      Mathlib. We defined the group structure, elements, and their actions on the measure or test functions.
      Yet these definitions are specified to 4D spacetime and scalar test functions, therefore future work
      would include rewriting it to standards befitting a foundational element, and generalization to non-
      scalar fields.
    • The standard definition of the free covariance is the Fourier transform of the free propagator 1/(k 2 +m2 ),
      but this is a conditionally convergent integral whose integrability is hard to prove. Instead, we used
      the Bessel function definition as stated in B.5.
    • We used two slightly different definitions for Fourier transform: the physics convention in Parseval.lean
      and the Mathlib convention in General/FourierTransform, differ by a factor of 2π in the phase.
      Although one could stick to one convention, we found it easier and more intuitive to use different
      conventions when proving different theorems. Unlike symbolic math, the prover will catch the mistake
      if the wrong one is used, so the mixing of conventions does not cause trouble.
    • We prove both the positivity required by Minlos and reflection positivity using the Schur-Hadamard
      theorem, which reduces positivity of the generating functional to positivity of the free covariance. The
      positivity here is defined in the sense of probability theory, details can be found in appendix B.


5     Methods
Two of us (MRD and SH) started the project in July 2025 by writing an informal outline of the math and
physics concepts, the OS axioms, and proof strategies. This was in no sense a “blueprint” as it was more


                                                       15
sketchy than the published proofs! Nevertheless we gave it to two models (GPT-5 and Gemini 2.5) and
asked them to translate it to Lean. The results were not of high quality but they were helpful in suggesting
definitions and theorems which we would eventually need to make. Still, the results were better than we had
expected given the paucity of Lean code in the training corpus.
     We then hand-coded the basic definitions, such as FieldConfiguration (Schwartz distributions on space-
time), the Euclidean group, and the generating function; everything which was needed to formulate the OS
axioms. Which we then proceeded to do, again by hand-coding.
     From that point on we primarily used coding assistants, at first mostly GPT and Gemini in GitHub
Copilot, with Lean-LSP MCP, which we found to be a significant help. We also tried Claude Sonnet and
Opus, and while over the course of the fall all of the models improved, in our estimation the introduction
of Claude Code (which launched in VS Code at the end of September) was the single biggest jump. By the
end of the project, Claude Code Opus 4.6 (often in the CLI version) was our go-to coding agent, and it was
substantially stronger than the agents we had started the project with.
     We also developed better prompts; one of note deals with the observation that all of the coding agents seem
too willing to abandon a difficult proof and delete their partial work. We speculate that while abandoning an
unpromising path is often appropriate, their stopping criteria (perhaps length of time spent?) were tuned to
optimize more common coding tasks rather than theorem proving. Anyways, if one could catch the agent in
time, it was useful to say “Don’t give up and delete a sizable block of code unless you can identify a blocking
difficulty, and if you do, explain the difficulty and lessons learned in the chat.” This behavior became less
of a problem over time, perhaps due to better agents or better system prompts.
     Some parts of the project (such as the Euclidean group action) were forward coded, and others were
elaborated by defining intermediate lemmas by hand and asking the models for proofs. In attempting to
fill in the proof from there, we developed the backward-chaining strategy by which much of the project was
done: we asked the agents to prove a lemma or OS axiom, but when they ran into difficulty, rather than
leave sorrys we suggested that the agent propose a simpler “helper lemma” which if assumed as an axiom
would enable a proof. Often we gave hints about what this might be (we were not trying to get an automatic
system), but just as often the agent would make a sensible proposal on its own and formulate it in Lean,
and we would accept it. Except for easy cases, we added these helper lemmas as Lean axioms rather than
sorrys, so that the model would stay focused on the original problem, and also added them to a list of
axioms to prove later. As the project filled in this strategy became more and more effective.
     Of course, the danger of this procedure is that the conjectured helper lemmas might be false or too
difficult to prove. Thus it was very important to validate them before proceeding. In some cases this could
be done by spot checking numerical examples, and we both asked the models to do this and observed them
do it spontaneously. But our main tool for doing this was cross-validation by the other models. A conjecture
by Claude would be given to Gemini and GPT (we developed MCP tools to make this easy) and their
comments relayed back to Claude. Difficult proofs would also employ this collaborative approach, with the
model writing a proof plan which would then be reviewed by the other models. Although the relative abilities
of the models varied with the versions, we generally found that Claude was the most effective at coding,
with Gemini giving crucial advice as it had a better and broader understanding of the underlying math and
physics.
     A variation of the method which we found particularly effective in the later stages was to tell the agent
to look for a helper lemma that is as general as possible, which might appear in a textbook and which
is formulated without using any project-specific definitions. For example, the statement should not refer
to SpaceTime but instead to EuclideanSpace R d (where R denotes R) and work for any d. This both
significantly decreased the number of false conjectures and also led to conjectures which were easier to prove.
     Several times during our work we discovered that definitions (including our original renditions of the
OS axioms themselves) were incorrect. A noteworthy example was that we originally defined the covariance
as a Fourier transform of a simple momentum space expression—this is the universal practice in physics
and we did not give it a second thought. But when a mathematician (RN) joined the project, he soon
noticed that this was a conditionally convergent integral and very problematic (it could even be interpreted
as zero in certain contexts!). This was soon fixed by introducing an absolutely convergent definition (in
terms of a Bessel function), but the experience led us to introduce further systematic checks, for example
that integrals are absolutely convergent. The coding agents made such checks straightforward and were good
at implementing special-purpose code (usually in Python) to speed them up.


                                                      16
    The choice of the final axioms to leave as assumptions was made based on prior math knowledge and a
sense of what topics are lacking in Mathlib, as well as repeated proof attempts. We envisioned assuming
Minlos’ theorem from the very start for the reasons discussed earlier. The other two “axioms” (Goursat’s
theorem and the nuclear property of Schwartz space) were attempted, and the length of the proof plans and
estimated Lean code dissuaded us. As mentioned above, these axioms were subsequently eliminated, the
first by explicit proof and the second by redoing the proof of OS0.
    It seems to us that for many projects, assuming major theorems as axioms is a better course than
restricting to only allow statements which can be entirely proven from the foundations. Of course this has
pitfalls which we will discuss below in 5.1.

5.1    Tips and common pitfalls
We emphasize that all of the observations in this subsection reflect the state of AI tooling as of early 2026.
Given the pace of improvement, some of these limitations may well be short-lived. Indeed, perhaps the most
striking aspect of this project is how noticeably the models improved over its course. When we started,
it was a struggle to get anything nontrivial done. By around December, proving things was no longer the
main difficulty, but the problems described below, false analogies, context limits, stale documentation, were
serious obstacles. By the time of writing, we are getting some fairly nontrivial proofs done with minimal
guidance, though other proofs remain hard.

Correctness of definitions. Large language models have a reasonable intuition for what is “correct”
or “conventional” in mathematics, and in our experience, if one asks two models independently whether
a conjectured axiom is true, at least one will usually flag an outright false statement—which is why the
cross-model validation protocol described earlier is so valuable. The more insidious failure mode is subtler:
the models can be led astray by analogies that are nearly but not quite right. For instance, a model
may confidently apply results about complex matrices to matrices over a Grassmann algebra, or treat a
conditionally convergent integral as though it were absolutely convergent, because these are the “standard”
settings it has seen most often in training. Even when given explicit instructions about how a proof should be
structured, the model’s prior intuitions can override the guidance, and it will repeatedly attempt strategies
that do not apply in the non-standard setting. During the Lean code-writing phase, the most important role
for a human in the loop was therefore to ensure that key definitions were correct and that the mathematical
context was not being silently shifted to a more familiar one. Subtle slips of this kind are hard to detect
by inspection, especially when the types still line up and everything compiles. A reliable countermeasure
was to constantly build small unit tests for newly introduced definitions and lemmas. One can of course
feed Lean code back into an LLM and ask it to translate the formal statement into natural language, but
we found that this step alone did not reliably catch transcription or interpretation errors. A more robust
debugging strategy was to take a lemma just proved, or a definition just stated, and use it to prove an
additional statement as a unit test, not necessarily something dictated by the original scaffold. In practice,
one such auxiliary check was usually enough to surface hidden mistakes and force a correction in the relevant
definitions.

Decomposition of long proofs. A shortcoming of our formalization is due to the models’ limitations at
long-form proofs. This is largely a consequence of context limits: the model cannot simultaneously “see”
all definitions, previous lemmas, and local proof state for a large development, nor can it reliably output a
long proof script without losing earlier constraints. Our formalization’s design, logical flow, and readability
still requires much improvement to meet the foundational standards of Mathlib or PhysLean. As the project
went on, the refactor for quite large sections of the code became much more manageable. One example is
the proof of Bochner’s theorem, which was done by Claude Code in February 2026 over the space of two
days nearly autonomously. However it still is the case that when pushing the models to plan and execute
very long horizon proofs the resulting Lean code often falls into the “merely true” rather than highly legible,
logical, and production ready unless a significant effort is imposed by a human to require such standards.
Still we know of no clear obstacle to further automating this, using better models and giving them better
explanations of the standards.



                                                      17
    Making new definitions and using them in long proofs remains a challenge. Human input is valuable
for formulating definitions, planning the high-level decomposition and supplying a proof outline in ordinary
mathematical language; the AI is most effective when asked to fill in individual steps rather than invent an
entire long proof from scratch. As a result, at least with current tooling, formalization tends to follow known
human proofs, and it is difficult to use these systems to reliably produce genuinely new arguments that were
not already understood at the informal level.

Stale docstrings and unreliable summaries. A related issue is that the LLMs understand the codebase
largely through docstrings and comments rather than by genuinely reading the Lean code. These docstrings
are not always up to date: they may reference definitions or lemmas that have since been deleted, or record
earlier proof strategies in phrases like “not . . . but . . . ” that no longer reflect the current approach. As a
consequence, when we asked an agent to summarize the contents of a file, the resulting markdown documents
were often polluted with stale or irrelevant information inherited from outdated comments. Worse, the models
showed little ability to distinguish the essential components of a proof from routine bookkeeping: summaries
would dwell on trivial details (type coercions, import boilerplate) while glossing over or entirely omitting
the key mathematical ideas. This made it difficult to rely on AI-generated documentation for planning or
for onboarding new collaborators, and we found that human-written or at least human-edited summaries
remain necessary for any high-level overview of the proof architecture. Again, there is no evident reason
that these reflect fundamental shortcomings of the models, but they will need to be dealt with to further
automate the procedure.

Unproductive search and the need for human redirection. There were theorems for which the model
worked for hours, repeatedly adding auxiliary lemmas and expanding the codebase without making progress.
The model would propose alternative approaches, but they often failed to resolve the core obstruction. Again,
this is a result of the model’s inability to identify the core component or central argument of the proof. When
a human stepped in with a clearer proof route, the LLM could usually implement the new direction quickly,
and the development then proceeded smoothly.

Workflow and complexity management As the project grew, several difficulties particular to the later
stages emerged: completing successful chains of arguments and not getting lost in the thicket of helper
lemmas, keeping track of which lemmas and axioms are contributing to the main line of the proof, and
occasionally keeping track of two or three proof strategies being simultaneously developed since none had
closed. This was aided by the tool DependencyExtractor [22]. But the main organizational technique we
followed was to frequently ask the agents to write and update auxiliary documents describing the plans
being followed to close each active chain of arguments and the current situation. For example, we had a
file axioms.md which listed the sorrys and assumed axioms. Such organizational methods will no doubt be
further automated in the future. Planning more broadly was essential and deserved even more investment
than we gave it.


6    Going forward
Let us outline several directions that we expect to develop in the near future: the formalization of results in
mathematical physics, the prospects for formalizing physics which presently does not exist in mathematically
rigorous form, and the further development of formal mathematical libraries. We also comment on the role
of formalization in a hypothetical future in which AI’s have human or superhuman reasoning ability.

Existing results in mathematical physics We start by listing a few existing results for which for-
malization could be in range. One is the Osterwalder-Schrader reconstruction theorem, which relates the
Euclidean QFT approach we followed to the original Wightman definition of QFT as quantum mechanics.
Ideally this would use a version of the OS axioms which are both provable and state necessary and sufficient
conditions for reconstruction, but this is not completely clear for the current axioms (a recent discussion is
[53]). Formalizing the reconstruction theorem could help resolve these questions, and is being studied by Xi
Yin and the first author.


                                                       18
    One of the simplest interacting QFTs is P (ϕ)2 , the 2d boson with a polynomial potential. This was
constructed in [38, 40, 86, 65] and these proofs look formalizable. In fact, the first author has made progress on
it. More recently the construction was redone using stochastic quantization [29]. This should be formalizable
given the prerequisite stochastic PDE theory.
    Rigorous construction of fermionic field theories is generally easier as they do not have the large field
problem, and there are many works on this. A rigorous treatment of the 2d supersymmetric Wess-Zumino
model is in [48]. The 2d abelian Higgs model was treated in [15, 16, 17]. If these results could be combined
to construct the supersymmetric gauged linear sigma model, one could aspire to a direct QFT argument for
mirror symmetry.
    Another field that is increasingly being formalized is quantum information theory [61]. Recent work has
begun to translate central theorems in quantum information into Lean proofs. For example [61] formally
verified the Generalized Quantum Stein’s Lemma, a fundamental result in quantum hypothesis testing that
gives an operational interpretation of quantum relative entropy in the asymptotic discrimination of quantum
states. Their formalization included components from operator algebras, functional analysis and topology.
In the process, the formalization clarified several implicit assumptions in the original analytic arguments
and led to a more precise formulation of quantum resource theories, while simultaneously contributing to
the development of a growing QuantumInfo library [60] in Lean intended to support a broader program of
formalizing quantum theory itself.
    From the perspective of formal theorists, it would be very appealing to use these ideas to formulate
conjectures about quantum gravity as well. One ambitious possible direction would be to clarify the mathe-
matical structure of the gravitational path integral.
                                                    R The gravitational partition function is written as a sum
over spacetime geometries, schematically, Z = DgeiS[g] , where the integral ranges over metrics modulo
diffeomorphisms. However, in gravity the functional measure Dg is not rigorously defined. Moreover, the
configuration space itself, remains poorly understood mathematically [30].
    In particular, the gravitational path integral involves integration over an ∞−dimensional space of metrics
(and possibly topologies), and the corresponding measure cannot be treated as a straightforward analogue
of Lebesgue measure. Determining the correct measure is highly non-trivial in constrained gauge systems
such as in gravity [30]. Consequently, despite a central role in semiclassical and holographic calculations
commonly studied in quantum gravity settings, the gravitational path integral is not a mathematically
controlled object[34]. Developing a rigorous definition of this measure (or even clarifying what the appropriate
configuration space should be) would represent a significant conceptual advance in quantum gravity research.

Non-rigorous theoretical physics The low-hanging fruit in the formalization of physics is to improve
the verification of calculations and computations. Many algebraic calculations in physics are essentially
rigorous; they need only be placed in the right physical and mathematical context. Formalizing this context,
even without proving it all from mathematical foundations, would be valuable if it enables us to find errors
due to incompatible conventions or other misapplications of results. A famous example which might have
been caught this way was a long-standing disagreement between theory and experiment of the muon g − 2,
which turned out to be due to a wrong sign convention [51, 45].
    Going the other way, there is little to be gained by formalizing symbolic algebra calculations in Lean
(or the other ITP languages) as a good symbolic algebra system should be 100% reliable. Rather, one
could extend the scope of formalization by implementing communication between ITP verifiers and symbolic
algebra systems, and the importation of certificates validating such calculations. Recent work on this includes
[80].
    While valuable, these methods do not help much with formalizing theories whose formulations are far
beyond present-day mathematical physics, such as 4d Yang-Mills theory and its supersymmetric extensions.
Given their central role in theoretical particle physics, excluding them is hardly an acceptable limitation.
Rather, ITP will make it far easier to postulate axioms which capture our physicists’ current understanding
and intuitions, try them out and see what consequences they imply.

Formalization of more existing mathematics The most immediate enabling factor for these goals is
the formalization of more existing mathematics. Mathlib, while impressive, is still small relative to the body
of known mathematics. In part this is because it (rightly) maintains a very high standard of code quality. As
of this writing there are roughly 2,300 pull requests waiting to be reviewed, each requiring substantial human


                                                       19
effort. We hope that AI tools will soon help alleviate this in at least two ways. First by assisting the review
process itself, checking style conventions, verifying clean integration with existing modules, and flagging
potential issues before a human reviewer looks at the PR. Second, by helping authors bring their individual
projects into compliance with library standards before submission, lowering the barrier to contributing and
reducing the burden on maintainers.
    A closely related issue is the fragmentation of independent formalization projects. As more groups
undertake projects like ours, each might start by defining its own versions of the basic objects it needs,
Euclidean transformations, quantum field theory axioms, function spaces, and so on. This could lead to
many independent, mutually incompatible formalizations of the same mathematical structures, making it
difficult for one project to build on another’s work. While solving these problems motivates the Mathlib
project, it is evidently hard for any single project to do this across the full breadth of the mathematical
sciences. It is not clear to us that a single monolithic library (or even one for math and one for physics)
is the best or even a scalable solution. We can compare the present situation with a hypothetical world in
which (say) the Annals of Mathematics were the only refereed mathematics journal. The reader can judge
the desirability and practicality of this for him or herself. Perhaps several libraries building on Mathlib in
various more specialized directions would be better. An alternate approach would be to design lightweight
but rigorous standards, shared definitions, interface conventions, and compatibility requirements, along
with search tools to find relevant prior work and adopt its conventions from the start. This would enable
independently developed projects to interoperate without requiring every one to go through a full human
review process. Designing such standards and building tools that help authors conform to them, strikes us
as a very important infrastructure problem for the formalization community going forward.

Benchmarking formalization progress It would be valuable to develop benchmarks that measure for-
malization progress itself. Existing benchmarks such as miniF2F [101] and ProofNet [8] evaluate how well
AI systems can prove formalized statements, but they measure the capability of the AI, not the state of
human mathematical knowledge that has been made rigorous. What is missing is a way to track how much
of mathematics has actually been formalized, where the remaining gaps are, and how they are shrinking over
time. Some recent work addressing this problem is [99].
    Here we note an interesting distinction between physics and math. In mathematics, formalization pro-
ceeds bottom-up: one starts from definitions, builds lemmas, and works toward theorems, always on solid
ground. Progress can be measured, at least roughly, by how much of the known corpus has been formalized
from the foundations. In physics the natural direction is often the reverse. One starts from a conjecture
or a physical intuition—say, that a certain quantum field theory exists and has specific properties—and
works backward to identify the precise mathematical criteria under which the conjecture holds. This is
essentially the backward-chaining strategy we employed in this project, elevated to the level of an entire
research program. A meaningful benchmark for physical formalization would therefore need to capture not
just how many theorems have been proved, but also how far the top-down analysis has reached: how many
of the assumptions have been made explicit, how many have been validated or closed, and how large the
remaining gaps are. Developing such metrics would help the community track progress, compare approaches,
and identify where effort is most needed.

Further development of AI With the rapid improvement of coding agents, it is becoming possible to
formalize entire chapters of textbook mathematics at a pace that would have been impractical a year ago.
Progress on the shortcomings of AI-generated code quality and organization mentioned earlier would be
quite valuable from this point of view. But despite these shortcomings, if coding agents continue to improve
at the current rate, then autoformalization, the complete automation of formalization, could well become
practical in the near future. We can hope that this will see rapid application and solve the library problem
fairly quickly.
    Still, one can imagine that if AI can so easily translate between informal and formal reasoning, perhaps
it will also do 100% reliable informal reasoning. Recent progress can be read both ways: in the 2025 IMO
(considered as a challenge for AIs), both types of reasoning (informal and formal) led to strong performance.
If informal reasoning becomes reliable, will there be any need for formalization?
    One can of course compare this question with the parallel one about mathematical rigor. And with few
exceptions (theoretical physics being one), the historical evolution in the exact sciences leads towards more


                                                      20
rigor: this is quite clear in applied math, statistics and computer science. All other things being equal,
except in the initial exploratory phase of research, the advantages of rigor seem to win out. This suggests
that if formalization becomes easy, it too would win out.
    Another analogy, drawn from computer science, is to the differences between interpreted and compiled
languages. Here the fundamental difference is whether the computer translates the higher level code to
machine code in advance (using a compiler) or as it is being executed (in an interpreter). This difference
is also reflected in the language – to be compilable a language must be more rigid, making coding more
difficult, but in return one gains faster and more secure execution as many problems can be detected in
advance. In practice one usually uses interpreted languages for smaller short-lived projects, and compiled
languages for larger long-lived software. The analogy between compilation and formalization is that both
methods do more required work (of translation; of verification) up front, saving the need to do it again later.
Thus the advantages of formalization will be more significant in working with large theories and frameworks
which undergo sustained mathematical development. This clearly includes quantum field theory, suggesting
that even if reliable AI informal reasoning about it becomes possible, formalization will still bring significant
advantages.

6.1    Advice for now (early 2026)
This reflects our impressions and practice as of March 2026 and may go out of date quickly.
   • To optimize the coding agents’ abilities, the most important resource is context – reading many large
     files will rapidly exhaust this. Keep the project well organized with many supplementary documentation
     files: summaries, plans, lists of sorrys or custom axioms remaining to prove, and so on. We find that
     markdown (md) format is better than latex or pdf for these files.
   • The frontier models’ abilities differ and their ranking changes frequently, so one should use several
     models and follow their performance. A pattern which seems more stable is that the coding agents
     with harness (Claude Code and Codex), while better at coding, will also try hard to prove incomplete or
     even false statements. The chat/query agents (especially Gemini) are more able to evaluate definitions
     and theorem statements for correctness and propose refinements and corrections.
   • Specific wording of prompts is less important than it used to be. If the models have the information
     they need, they can work with high level instructions. Skills such as lean4-skills (at
     https://github.com/cameronfreer/lean4-skills) and tools such as Lean-LSP MCP are valuable.

   • The most difficult phase of a project is the beginning, developing project-specific definitions and a
     proof sketch. One approach, and arguably the best approach, if a lot of human time and expertise are
     available, is to do all this by hand. On the other hand this doesn’t scale and we are having reasonable
     success with letting the agents do this, with a good deal of human review and guidance.
   • It is very advantageous if the precise final theorems to prove can be formulated from the start, with
     a minimal use of project-specific and non-tested definitions. If too many new definitions are required,
     the project may be out of range.
   • One should give the models the actual math/physics papers with the informal proofs (latex is better
     but pdf works) and ask to study them and make summaries.
   • Although one can let the models improvise a proof sketch, once it is reasonably filled in (having a clear
     proof path but with many sorrys or axioms) one should have the models make clear summaries and
     vet these thoroughly before proceeding.
   • We found a backward chaining approach to work well: the first draft of a proof could use sorrys; ask
     the agents to fill them directly; if any are too hard for this then ask the agent to formulate a “textbook
     axiom” which would fill them, then carefully vet these proposals with other models and by human
     review before signing off and leaving them to prove later.
   • Keeping the supplementary docs and lean docstrings up to date pays off.


                                                       21
   • One needs to use the best (“pro”) models and a professional subscription to do research level formal-
     ization.


Acknowledgments
We thank Jeremy Avigad, Sourav Chatterjee, Martin Hairer, Jesse Han, Arthur Jaffe, Kim Morrison,
Dwarkesh Patel, Tripp Roberts, Scott Sheffield, Julian Sonner, Christian Szegedy, Yoh Tanimoto, Joseph
Tooby-Smith, Zixiao Wang and Xi Yin for valuable discussions. Some early stages of the project were done
during the July 2025 visit of MRD and SH to Morph Labs/Math Inc, whom we thank for inspiration and
hospitality. We thank the many contributors to and maintainers of Mathlib, we thank Rémy Degenne and
Peter Pfaffelhuber for formalizing the Kolmogorov extension theorem, and we thank Matteo Cipollina for
his independent formalization of the axioms in our first release. Finally, we thank Alok Singh for suggesting
an MCP setup and more generally for cluing the authors into the techniques being used by Lean engineers,
and David Renshaw (who is supported by ICARM) for code golfing.


References
  [1] Artificial intelligence and theorem proving (aitp) announcement, https://www.dfki.de/pipermail/
      vki-list/2015-November/001561.html, November 2015, Announcement describing AITP as a forum
      for AI + theorem proving research. Accessed 2026-02-12.
  [2] The lean mathematical library, CoRR abs/1910.09336 (2019).
  [3] AITP, Conference on artificial intelligence and theorem proving (aitp), https://aitp-conference.
      org/, 2025, Conference site describing AITP as a yearly meeting on AI and theorem proving. Accessed
      2026-02-12.
  [4] Michael Aizenman, Proof of the triviality of ϕd 4 field theory and some mean-field features of ising
      models for d&gt; 4, Phys. Rev. Lett. 47 (1981), 1–4.
  [5] Michael Aizenman and Hugo Duminil-Copin, Marginal triviality of the scaling limits of critical 4D
      Ising and ϕ44 models, Annals Math. 194 (2021), no. 1, 163.
  [6] Michael Atiyah, The interaction between geometry and physics, The Unity of Mathematics, Progress
      in Mathematics, vol. 244, Birkhäuser, 2006, pp. 1–15.
  [7] Jeremy Avigad, Leonardo de Moura, Soonho Kong, Sebastian Ullrich, and contributors from the
      Lean Community, Theorem proving in lean 4, https://leanprover.github.io/theorem_proving_
      in_lean4/, 2021, Online textbook and tutorial for Lean 4. Accessed 2026-02-12.
  [8] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and
      Jeremy Avigad, Proofnet: Autoformalizing and formally proving undergraduate-level mathematics,
      2023.
  [9] Tadeusz Balaban, Renormalization group approach to lattice gauge field theories: I. generation of effec-
      tive actions in a small field approximation and a coupling constant renormalization in four dimensions,
      Communications in Mathematical Physics 109 (1987), 249–301.
 [10] Tadeusz Balaban, Large field renormalization. I. The basic step of the r operation, Communications in
      Mathematical Physics 122 (1989), no. 2, 175–202 (en).
 [11] Kshitij Bansal, Sarah M. Loos, Markus N. Rabe, Christian Szegedy, and Stewart Wilcox, Holist: An
      environment for machine learning of higher-order theorem proving, 2019, Presents HOList, a bench-
      mark and environment (derived from HOL Light) designed for ML/RL-style theorem proving.
 [12] A. A. Belavin, A. M. Polyakov, and A. B. Zamolodchikov, Infinite conformal symmetry in two-
      dimensional quantum field theory, Nuclear Physics B 241 (1984), no. 2, 333–380.


                                                     22
[13] Jasmin Christian Blanchette, Sascha Böhme, and Lawrence C. Paulson, Extending sledgehammer
     with smt solvers, Automated Deduction – CADE-23, Lecture Notes in Computer Science, vol. 6803,
     Springer, 2011, pp. 116–130.
[14] Jacopo Borga, Sky Cao, and Jasper Shogren-Knaak, Surface sums for lattice Yang-Mills in the large-N
     limit, arXiv e-prints (2024), arXiv:2411.11676.

[15] David Brydges, Jürg Fröhlich, and Erhard Seiler, On the construction of quantized gauge fields. I.
     General results, Annals of Physics 121 (1979), 227–284.
[16]          , Construction of quantised gauge fields. II. Convergence of the lattice approximation, Commu-
       nications in Mathematical Physics 71 (1980), 159–205.

[17]           , Construction of quantised gauge fields. III. The two-dimensional abelian Higgs model without
       cutoffs, Communications in Mathematical Physics 79 (1981), 353–399.
[18] Sky Cao, Ron Nissim, and Scott Sheffield, Dynamical approach to area law for lattice Yang-Mills,
     arXiv e-prints (2025), arXiv:2509.04688.

[19] Sky Cao, Ron Nissim, and Scott Sheffield, Expanded regimes of area law for lattice Yang-Mills theories,
     May 2025, arXiv:2505.16585 [math].
[20] Ajay Chandra, Ilya Chevyrev, Martin Hairer, and Hao Shen, Langevin dynamic for the 2D Yang–Mills
     measure, Publications Mathématiques de l’IHÉS 136 (2022), 1–147, Constructs a state space and
     Markov process for the stochastic Yang–Mills heat flow in 2D using regularity structures.

[21] Sourav Chatterjee, Rigorous solution of strongly coupled SO(N ) lattice gauge theory in the large N
     limit, Communications in Mathematical Physics 366 (2019), no. 1, 203–268 (English).
[22] Patrik Cihal, lean-graph: Theorem relational dependencies automatic extraction and visualization for
     Lean 4, 2023, Accessed: 2026-02-19.

[23] Clay Mathematics Institute, Yang-mills & the mass gap, https://www.claymath.org/millennium/
     yang-mills-the-maths-gap/?utm_source=chatgpt.com, Accessed 2026-03-08.
[24] DARPA, expmath: Exponentiating mathematics, https://www.darpa.mil/research/programs/
     expmath-exponential-mathematics, 2025, DARPA program aiming to radically accelerate progress
     in pure mathematics via AI, including auto(in)formalization. Accessed 2026-02-12.

[25] Leonardo de Moura and Sebastian Ullrich, The lean 4 theorem prover and programming language,
     Proceedings of the 28th International Conference on Automated Deduction (CADE 28), Springer,
     2021.
[26] Rémy Degenne, David Ledvinka, Etienne Marion, and Peter Pfaffelhuber, Formalization of Brownian
     motion in Lean, November 2025, arXiv:2511.20118 [math].

[27] Michael R. Douglas, How will we do mathematics in 2030?, January 2017.
[28] Bruce K. Driver, Convergence of the U(1)4 lattice gauge theory to its continuum limit, Comm. Math.
     Phys. 110 (1987), no. 3, 479–501. MR 891949
[29] Pawel Duch, Wojciech Dybalski, and Azam Jahandideh, Stochastic quantization of two-dimensional
     p(ϕ) quantum field theory, Communications in Mathematical Physics 406 (2024).
[30] Jonathan Engle, Muxin Han, and Thomas Thiemann, Canonical path integral measures for holst and
     plebanski gravity, (2009).
[31] Benjamin Breen et al., Ax-prover: A deep reasoning agentic framework for theorem proving in math-
     ematics and quantum physics, arXiv, 2025, Describes connecting general-purpose LLMs to Lean tools
     via MCP (using lean-lsp-mcp).


                                                     23
[32] Tom Brown et al., Language models are few-shot learners, 2020, Introduces GPT-3 and demonstrates
     strong scaling-driven gains and few-shot capabilities.
[33] Richard P Feynman, The character of physical law, Messenger Lectures, Cornell University / BBC,
     London, 1965.

[34] Maarten et al. Fraaije, On the reconstruction problem in quantum gravity, Physics Letters B (2022).
[35] Lars Gårding and Arthur S. Wightman, Fields as operator-valued distributions in relativistic quantum
     theory, Arkiv för Fysik 28 (1964), 129–189, Classic presentation of the (Gårding–)Wightman axioms
     for relativistic quantum fields.
[36] Paul H. Ginsparg and Kenneth G. Wilson, A remnant of chiral symmetry on the lattice, Physical
     Review D 25 (1982), no. 10, 2649–2657.
[37] James Glimm and Arthur Jaffe, Regularity and axioms, Quantum Physics: A Functional Integral Point
     of View, Springer–Verlag, New York, 2 ed., 1987, pp. 255–269.
[38] James Glimm and Arthur Jaffe, Quantum physics: A functional integral point of view, Springer, 2012.

[39] Massimiliano Gubinelli, Peter Imkeller, and Nicolas Perkowski, Paracontrolled distributions and sin-
     gular PDEs, August 2017, arXiv:1210.2684 [math].
[40] Francesco Guerra, Lon Rosen, and Barry Simon, The p(ϕ)2 euclidean quantum field theory as classical
     statistical mechanics, Annals of Mathematics 101 (1975), 111–259.

[41] Rudolf Haag and Daniel Kastler, An algebraic approach to quantum field theory, Journal of Mathe-
     matical Physics 5 (1964), no. 7, 848–861, Original formulation of the Haag–Kastler (algebraic QFT)
     axioms in terms of nets of local observable algebras.
[42] Martin Hairer, A theory of regularity structures, February 2014, arXiv:1303.5113 [math-ph].
[43] harmonic-ai, Harmonic’s IMO 2025 results (lean 4 statements and proofs), GitHub repository, 2025,
     Repository containing Lean artifacts for Aristotle’s IMO 2025 solutions (problems 1–5).
[44] John Harrison, Josef Urban, and Freek Wiedijk, History of interactive theorem proving, Handbook of
     Automated Reasoning, Elsevier, 2014, Defines interactive theorem proving as human–machine inter-
     active production of formal proofs.

[45] M. Hayakawa and T. Kinoshita, Pseudoscalar pole terms in the hadronic light by light scattering con-
     tribution to muon g - 2, Phys. Rev. D 57 (1998), 465–477, [Erratum: Phys.Rev.D 66, 019902 (2002)].
[46] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever, Gamepad: A learning environment
     for theorem proving, 2018, Introduces a game-like ML environment for interactive theorem proving in
     Coq, including tactic prediction and position evaluation.

[47] Thomas et. al Hubert, Olympiad-level formal mathematical reasoning with reinforcement learning,
     Nature (2025), Describes AlphaProof, an RL-based system that searches for formal Lean proofs and is
     evaluated on olympiad-level formal mathematics benchmarks.
[48] Arthur Jaffe, Andrzej Lesniewski, and Jonathan Weitsman, The two-dimensional,N=2 Wess-Zumino
     model on a cylinder, Communications in Mathematical Physics 114 (1988), no. 1, 147–165 (en).

[49] Arthur Jaffe and Edward Witten, Quantum Yang–Mills theory, (2000), Clay Mathematics Institute
     Millennium Problem description.
[50] Res Jost, The general theory of quantized fields, American Mathematical Society, 1965, Axiomatic QFT
     in the Wightman framework; includes Jost’s treatment of the CPT theorem (often referred to as Jost’s
     theorem).



                                                   24
[51] M. Knecht, A. Nyffeler, M. Perrottet, and E. de Rafael, Hadronic light-by-light scattering contribution
     to the muon: An effective field theory approach, Physical Review Letters 88 (2002), no. 7.
[52] John B. Kogut, An introduction to lattice gauge theory and spin systems, Reviews of Modern Physics
     51 (1979), no. 4, 659–713.
[53] Petr Kravchuk, Jiaxin Qiao, and Slava Rychkov, Distributions in CFT II. Minkowski Space, Journal
     of High Energy Physics 2021 (2021), no. 8, 94, arXiv:2104.02090 [hep-th, physics:math-ph].
[54] Thomas S. Kuhn, The structure of scientific revolutions, University of Chicago Press, 1962.
[55] leanprover-community,    Mathematics in lean,   https://leanprover-community.github.io/
     mathematics_in_lean/, 2020, Textbook for learning mathematical formalization in Lean 4 and
     mathlib. Accessed 2026-02-12.
[56] Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu Liu, Jianhao Shen,
     Hui Jin, Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing Tang, and Zhijiang Guo, Process-driven
     autoformalization in lean 4, 2024, Introduces a Lean 4 autoformalization benchmark (FormL4) and a
     process-supervised verifier approach.
[57] Martin Lüscher, Exact chiral symmetry on the lattice and the Ginsparg–Wilson relation, Physics Letters
     B 428 (1998), no. 3–4, 342–345.
[58] Martin Luscher, Properties and uses of the Wilson flow in lattice QCD, Journal of High Energy Physics
     2010 (2010), no. 08, 071.
[59] Patrick Massot, Why formalize mathematics?, https://www.imo.universite-paris-saclay.fr/
     ~patrick.massot/files/exposition/why_formalize.pdf, 2024, Discusses the need for more for-
     malized basic mathematics to build upon, the option of using unchecked building blocks, and notes
     that fully formalized mathematics remains a tiny fraction of mathematics. Accessed 2026-02-12.
[60] Aaron Meiburg and collaborators, Lean-quantuminfo: A lean library for quantum information theory,
     https://github.com/leanprover-community/Lean-QuantumInfo, 2025, Lean formalization library
     for quantum information theory.
[61] Alexander Meiburg, Leonardo A. Lessa, and Rafael R. Soldati, A formalization of the generalized
     quantum stein’s lemma in lean, arXiv preprint arXiv:2510.08672 (2025).
[62] Model Context Protocol, Model context protocol specification, https://modelcontextprotocol.io/
     specification/2025-03-26, 2025, Defines MCP as a protocol for integrating LLM applications with
     external tools and context. Accessed 2026-02-12.
[63] Gregory Moore and Nathan Seiberg, Classical and quantum conformal field theory, Communications
     in Mathematical Physics 123 (1989), no. 2, 177–254.
[64] Colin J. Morningstar and Mike Peardon, Glueball spectrum from an anisotropic lattice study, Physical
     Review D 60 (1999), no. 3, 034509.
[65] Edward Nelson, Probability theory and euclidean field theory, Lecture Notes in Physics 25 (1973),
     94–124.
[66] Herbert Neuberger, Exactly massless quarks on the lattice, Physics Letters B 417 (1998), no. 1–2,
     141–144.
[67] Ron Nissim, U(n) lattice Yang-Mills in the ’t Hooft regime, arXiv e-prints (2025).
[68] oOo0oOo, lean-lsp-mcp: Lean theorem prover mcp, GitHub repository, 2025, MCP server enabling
     agentic interaction with Lean via the Language Server Protocol. Accessed 2026-02-12.
[69] OpenAI, Gpt-4 technical report, 2023, Reports development and evaluation of GPT-4, a large-scale
     multimodal large language model.


                                                    25
[70] K Osterwalder and R Schrader, Axioms for euclidean green’s functions, Communications in Mathe-
     matical Physics (1972).
[71] K. Osterwalder and R. Schrader, Axioms for euclidean green’s functions, Communications in Mathe-
     matical Physics 31 (1973), no. 2, 83–112.

[72] K Osterwalder and E Seiler, Gauge field theories on a lattice, Annals of Physics 110 (1978), no. 2,
     440–471.
[73] Konrad Osterwalder and Robert Schrader, Axioms for Euclidean Green’s functions. II, Comm. Math.
     Phys. 42 (1975), 281–305, With an appendix by Stephen Summers. MR 376002
[74] Abraham Pais, The genius of science: A portrait gallery of twentieth-century physicists, Oxford Uni-
     versity Press, 2000, Contains the quotation attributed to Niels Bohr: “Never express yourself more
     clearly than you are able to think.”.
[75] Duccio Pappadopulo, Slava Rychkov, Johnny Espin, and Riccardo Rattazzi, Operator product expan-
     sion convergence in conformal field theory, Physical Review D 86 (2012), no. 10, 105043.

[76] Lawrence C. Paulson, Isabelle: A generic theorem prover, Lecture Notes in Computer Science, vol.
     828, Springer, 1994, Canonical reference for Isabelle.
[77] Auguste Poiroux, Gail Weiss, Viktor Kuncak, and Antoine Bosselut, Reliable evaluation and bench-
     marks for statement autoformalization, Proceedings of the 2025 Conference on Empirical Methods in
     Natural Language Processing (EMNLP), Association for Computational Linguistics, November 2025,
     Introduces benchmarks including RLM25 and ProofNet#; proposes BEq+ metric for autoformalization
     evaluation., pp. 17947–17969.
[78] David Poland, Slava Rychkov, and Alessandro Vichi, The conformal bootstrap: Theory, numerical
     techniques, and applications, Reviews of Modern Physics 91 (2019), no. 1, 015002.
[79] Riccardo Rattazzi, Vyacheslav S. Rychkov, Erik Tonni, and Alessandro Vichi, Bounding scalar operator
     dimensions in 4d cft, Journal of High Energy Physics 0812 (2008), 031.
[80] Tate Rowney, Riyaz Ahuja, Jeremy Avigad, and Sean Welleck, Dslean: A framework for type-correct
     interoperability between lean 4 and external dsls, 2026.
[81] G. B. Segal, The definition of conformal field theory, Topology, Geometry and Quantum Field The-
     ory (U. L. Tillmann, ed.), London Mathematical Society Lecture Note Series, vol. 308, Cambridge
     University Press, Cambridge, 2004, pp. 421–577.
[82] Erhard Seiler, Gauge theories as a problem of constructive quantum field theory and statistical mechan-
     ics, Lecture Notes in Physics, vol. 159, Springer, Berlin, Heidelberg, 1982.
[83] Hao Shen, Rongchan Zhu, and Xiangchan Zhu, A stochastic analysis approach to lattice Yang-Mills at
     strong coupling, Comm. Math. Phys. 400 (2023), no. 2, 805–851. MR 4589716
[84] David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den Driessche,
     Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, Sander Dieleman,
     Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy Lillicrap, Madeleine Leach,
     Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis, Mastering the game of go with deep neural
     networks and tree search, Nature 529 (2016), no. 7587, 484–489.
[85] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez,
     Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy Lillicrap, Karen Simonyan,
     and Demis Hassabis, A general reinforcement learning algorithm that masters chess, shogi, and go
     through self-play, Science 362 (2018), no. 6419, 1140–1144.

[86] Barry Simon, The p(ϕ)2 euclidean (quantum) field theory, Princeton University Press, 1974.


                                                    26
 [87]          , P (0) 2 euclidean (quantum) field theory, P (0) 2 Euclidean (Quantum) Field Theory, Princeton
        University Press, 2015.
 [88] Raymond F. Streater and Arthur S. Wightman, Pct, spin and statistics, and all that, W. A. Benjamin,
      New York, 1964, Classic axiomatic QFT reference proving the CPT and spin–statistics theorems in
      the Wightman framework.

 [89] Christian Szegedy, A promising path towards autoformalization and general artificial intelligence, In-
      ternational Conference on Intelligent Computer Mathematics, 2020.
 [90] Terence Tao, Formalizing the proof of pfr in lean4 using blueprint: a short tour, https://terrytao.
      wordpress.com/2023/11/18/formalizing-the-proof-of-pfr-in-lean4-using-blueprint-a-short-tour/,
      November 2023, Blog post. Accessed 2026-02-12.
 [91] The Harmonic Team, Aristotle: IMO-level automated theorem proving, 2025, Introduces Aristotle;
      reports gold-medal-equivalent performance on IMO 2025 with formal verification in Lean 4.
 [92] The Rocq Development Team, The rocq prover, Project website, Official description of Rocq (formerly
      Coq) as an interactive theorem prover / proof assistant for developing mathematical proofs and formal
      specifications.
 [93] René Thiemann et al., Structuring definitions in mathematical libraries, https://arxiv.org/abs/
      2509.10828, 2025.
 [94] Joseph Tooby-Smith and PhysLean contributors, Physlean: Digitalizing physics in lean 4, 2026, Ac-
      cessed: 2026-03-08.
 [95] Freek Wiedijk, Formalization of mathematics, https://www.cs.ru.nl/~freek/talks/nmc.pdf, 2007,
      Talk at Nederlands Mathematisch Congres, Leiden University, April 12, 2007.
 [96] Eugene P. Wigner, The unreasonable effectiveness of mathematics in the natural sciences, Communi-
      cations on Pure and Applied Mathematics 13 (1960), 1–14, Richard Courant Lecture (NYU), May 11,
      1959.
 [97] Kenneth G. Wilson, Confinement of quarks, Physical Review D 10 (1974), no. 8, 2445–2459.
 [98] Kenneth G Wilson and John Kogut, The renormalization group and the epsilon expansion, Physics
      reports 12 (1974), no. 2, 75–199.

 [99] Bowen Yang, Yi Yuan, Chenyi Li, Ziyu Wang, Liangqi Li, Bo Zhang, Zhe Li, and Zaiwen Wen,
      Construction-verification: A benchmark for applied mathematics in lean 4, 2026.
[100] Liao Zhang, David M. Cerna, and Cezary Kaliszyk, Learning rules explaining interactive theorem prov-
      ing tactic prediction, https://arxiv.org/abs/2411.01188, 2024, Notes that while proof verification
      is more accessible than ever, the learning curve remains steep for many state-of-the-art interactive
      theorem provers.
[101] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu, Minif2f: a cross-system benchmark for formal
      olympiad-level mathematics, 2022.




                                                      27
A      Notations
Here we provide the notations we used in this paper.
    1. Function Spaces
       (a) For F ∈ {R, C}, C k (RD ; F) will denote the space of F-valued functions on RD for which all
           derivatives of orderS ≤ k exist and are continuous, and we define the set of smooth functions
           as C ∞ (RD ; F) = k≥0 C k (Rn ; F). For F = C we will simply denote the spaces C k (RD ; F)
           (C ∞ (RD ; F)) by C ∞ (RD ) (C k (RD )).
       (b) Cc∞ (RD ) will denote the set of smooth functions with compact support. We frequently use the
           notation D(RD ) = Cc∞ (RD ) for the set of test functions. The topology on D(RD ) is specified by
           saying a sequence of functions fn → f in D(Rn ) if ∂ α fn → ∂f uniformly on K, for any multi-index
           α and compact set K ⊂ RD .
        (c) The space of Schwartz functions S(RD ; F) denotes the set of f ∈ C ∞ (RD ; F) for which all deriva-
            tives ∂ α f decay faster than any polynomial, i.e. supx∈Rn |(1 + |x|)−k ∂ α f (x)| < ∞ for all k ∈ N
            and α ∈ Nn . The seminorms ∥f ∥k,α := supx∈Rn |(1 + |x|)−k ∂ α f (x)| turn S(RD ; F) into a Fréchet
            space.
       (d) For p ∈ [1, ∞), and a measure space (X, F , µ) and F ∈ {R, C}, R
           Lp (X; F) = Lp (µ; F) = {measurable f on Rn taking values in F : X |f |p dx < ∞}, and
           L∞ (X; F) = L∞ (µ; F) = {measurable f on Rn taking values in F : ess sup|f | < ∞} Once again
           when   F = C we omit F from the notation. Lp (X; F) is a Banach space with norm ∥f ∥Lp :=
           ( X |f |p dx)1/p for p < ∞ and ∥f ∥L∞ := ess sup|f |.
            R

    2. Distributions
       (a) The space of distributions D′ (RD ) is the dual space of D(RD ).
       (b) The space of tempered distributions S ′ (RD ) is the dual space of S(RD ).

    3. Complex Analysis
       (a) A function f : Cn → C is holomorphic at a point (z1 , . . . , zn ) ≡ ⃗z if all of its first order complex
           derivatives exist as complex linear maps at ⃗z. Complex linearity requires uDu⃗z f = D⃗z f for
           complex u, which implies ∂¯⃗z f = 0.
       (b) A function f : Cn → C is analytic at a point (z1 , . . . , zn ) if it can be represented by a convergent
           power series in a neighborhood of the point. One can prove that holomorphic functions are
           analytic (Goursat’s theorem).
        (c) A function f : Cn → C is entire if it is analytic at every point in Cn .


B      Proofs of Glimm-Jaffe Axioms
We mostly followed the proof structure laid out in Glimm and Jaffe with slight variations.

B.1     Analyticity (OS0)
The strict definition of analyticity of the GFF generating functional requires that
                                    "          # Z                    !
                                     X                   X
                                  S       zi fi = exp i      zi ϕ(fi ) dµ(ϕ)                                  (B.1)
                                       i                      i

admits a converging power series expansion
                                     P       with respect to all zi for each fixed ω. In practice, it would be
hard to construct an expansion of S [ i zi fi ] and prove its convergence; instead, we used Hartog’s theorem
to simplify the proof.



                                                        28
   Hartog’s theorem states that in finite dimension, holomorphy of a complex function (C-differentiable)
implies its analyticity. Therefore OS0 simplifies to proving
                        Z                    !         Z                          !
                    ∂            X                                     X
                          exp i     zi ϕ(fi ) dµ(ϕ) = i ϕ(fj ) · exp i   zi ϕ(fi ) dµ(ϕ)           (B.2)
                   ∂zj            i                                    i

is well-defined. This requires
                        P        that                                   P
1. the integrand exp (i i zi ϕ(fi )) is measurable, integrable (for S [ i zi fi ] to be well-defined), and analytic
(derivative exists);
2. the z derivative is bounded by an integrable function B(ϕ), so that the derivative and integral can be
exchanged;
3. the z derivative is measurable, and hence integrable when combined with (2).
    The hardest part in the proof was to establish a bound on the derivative. As we can see on the RHS of
B.2, its norm is bounded by
                                                      !
                                           X               X
                         |i ϕ(fj ) · exp i   zi ϕ(fi ) | ≤    | ϕ(fj )| exp (− [ϕ(fi )]im ) .                (B.3)
                                            i                  j

To prove integrability of the bound, we use Fernique’s Theorem, which states that for any f , there exists
α > 0 such that                       Z
                                         exp α [ϕ(f )]2 dµ(ϕ) < ∞,
                                                       
                                                                                                    (B.4)

and hence we can show | ϕ(fj )|, exp (−[ϕ(f )]im ) ∈ L2 . Lastly, we can apply Hölder’s inequality, which says
that product of L2 functions is in L1 , to show that the RHS of B.2 is integrable. In the actual proof, the
exact bound is slightly different because we require the bound to be uniform in a neighborhood of z0 (when
taking the ∂zj derivatives), so we need to expand the bound function around z0 ; still, the general logic
follows the same way.

B.2     Regularity (OS1)
                                               1
For GFF, we will prove 3.6 with p = 2 and c = 2m 2 . The local integrability follows from the close-form

expression of two-point functions:
                                                                m
                                 K(x, y) = S2 (x, y) =                 K1 (m|x − y|).                        (B.5)
                                                          4π 2 |x − y|
Let y = 0 and take x → 0, we have
                                              m                   1
                                              2
                                                   K1 (m|x|) ∼                                               (B.6)
                                            4π |x|             4π |x|2
                                                                 2

which is locally integrable in 4-dimension.
   First, by Minlos construction of the GFF, we have
                                                 Z
                               S(f ) = ⟨f, Kf ⟩ ≡ d4 x d4 y f ∗ (x) K(x, y) f (y).                           (B.7)

To obtain an exponential bound, first notice that
                                                                    
                                           1               1
                        |S(f )| = exp − ⟨f, Kf ⟩C   = exp − Re⟨f, Kf ⟩C ,                                    (B.8)
                                           2               2
then decompose f into its real and imaginary components

                      ⟨f, Kf ⟩C = ⟨fre , Kfre ⟩ + i⟨fre , Kfim ⟩ + i⟨fim , Kfre ⟩ − ⟨fim , Kfim ⟩.           (B.9)

Taking the real part of both sides we have

                                     Re⟨f, Kf ⟩C = ⟨fre , Kfre ⟩ − ⟨fim , Kfim ⟩                            (B.10)


                                                          29
   Since K is positive semi-definite, ⟨fre , Kfre ⟩ ≥ 0, so

                                          −Re⟨f, Kf ⟩C ≤ ⟨fim , Kfim ⟩.                                (B.11)

To bound ⟨f, Kf ⟩, we can expand it in momentum space

                                                      |fˆ(k)|2
                                                  Z
                                       ⟨f, Kf ⟩ =              dk                                      (B.12)
                                                    |k|2 + m2

where fˆ(k) is the fourier transform of f . Notice that the denominator is bounded by
                                                     1      1
                                                          ≤ 2                                          (B.13)
                                                |k|2 + m2  m

and by Plancherel’s theorem ( |f (x)|2 dx = |fˆ(k)|2 dk), we get the bound
                             R             R

                                                           1
                                              ⟨f, Kf ⟩ ≤      ∥f ∥2L2 ,                                (B.14)
                                                           m2
and therefore
                                                      1               1
                                    ⟨fim , Kfim ⟩ ≤     2
                                                          ∥fim ∥2L2 ≤ 2 ∥f ∥2L2                        (B.15)
                                                      m              m
and
                                                                                             
               1                   1                        1      2           1                2
|S(f )| = exp − Re⟨f, Kf ⟩ ≤ exp     ⟨fim , Kfim ⟩ ≤ exp       ∥f ∥L2 ≤ exp       (∥f ∥L1 + ∥f ∥L2 ) .
               2                   2                       2m2                2m2
                                                                                                (B.16)

B.3    Euclidean Invariance (OS2)
We would like to show that under any Euclidean transformation E (translation and rotation), S(f ) remains
unchanged. First we perform a change of variable by x → E −1 x and y → E −1 y:
             Z                                Z
   S(Ef ) = d x d y f (Ex)K(x, y)f (Ey) = d4 (E −1 x) d4 (E −1 y) f ∗ (x)K(E −1 x, E −1 y)f (y).
                 4  4   ∗
                                                                                                    (B.17)

From B.5, we can see that K(x, y) only depends |x − y|, and therefore K(E −1 x, E −1 y) = K(x, y) is invariant
under Euclidean group action. Furthermore, the Lebesgue measure is also invariant under translation and
rotation (| det R| = 1), so d4 (E −1 x) = d4 x. Combining these facts, we can conclude that
                                          Z
                                S(Ef ) = d4 (x) d4 (y) f ∗ (x)K(x, y)f (y) = S(f ).                     (B.18)


B.4    Reflection Positivity (OS3)
The statement of OS3 as in 3.10 refers to the reflection positivity of the generating functional. First, we
would want to use the Schur product theorem to reduce this statement to the reflection positivity of the free
covariance. An equivalent statement with 3.10 is that for every finite sequence of functions fj , S{fi − θfj }
is positive semi-definite. We want to show that
                                                                                   
                                                         1
                    ⟨θf, Kf ⟩ ≥ 0 ⇒ S{fi − θfj } = exp − ⟨fi − Θfj , K(fi − Θfj )⟩ ⪰ 0                 (B.19)
                                                         2
for any f defined on positive time. Rewriting the exponent on the RHS gives

                       ⟨fi − Θfj , K(fi − Θfj )⟩ = ⟨fi , Kfi ⟩ + ⟨fj , Kfj ⟩ − 2⟨Θfi , Kfj ⟩           (B.20)

where we used the time-reflection symmetry of the inner product. Then we can expand the exponential
                                                                          
           1                                    1                    1
    exp − ⟨fi − Θfj , K(fi − Θfj )⟩ = exp − ⟨fi , Kfi ⟩ × exp − ⟨fj , Kfj ⟩ × exp (Rij )        (B.21)
           2                                    2                    2

                                                         30
where Rij ≡ ⟨θfi , Kfj ⟩. For any coefficient c, the quadratic form is
                                            *              !               +
                              X                    X              X
                                 ci cj Rij = Θ        ci fi , K      cj fj  ≥ 0                        (B.22)
                              i,j                      i           j
                                                                                       P
where the last inequality is given by free covariance reflection positivity, treating     ci fi as one function.
Since Rij is positive semi-definite, by Schur product theorem (product of PSD is also PSD), we conclude
that exp (Rij ) is PSD. Finally, looking at the quadratic form of B.21, we have
      X                         X        
                                             1
                                                                
                                                                     1
                                                                                  
           ci cj S(fi − θfj ) =     ci exp − ⟨fi , Kfi ⟩     cj exp − ⟨fj , Kfj ⟩    exp (Rij ) ≥ 0      (B.23)
       i,j                      i,j
                                             2                       2

which is exactly the condition for OS3.
   Now the proof os OS3 simplifies to proving the reflection positivity of the free covariance ⟨θf, Kf ⟩.
Expanding the inner product gives
                            Z
                ⟨θf, Kf ⟩ ≡ d4 x d4 y f ∗ (−x0 , ⃗x)f (y0 , ⃗y )K(x, y)
                            Z                                 Z                                        (B.24)
                                4   4   ∗                        3        1      −ik0 (x0 +y0 )+i⃗
                                                                                                 k·⃗
                                                                                                   x
                          = d x d y f (x0 , ⃗x)f (y0 , ⃗y ) d k dk0 2          e                     ,
                                                                        k + m2
where θ is the time reflection operator and K(x, y) is the free covariance, or the Green’s function. Naively,
we want to first perform the k0 integral to get
                                 Z
                                           1                           π −ωk |x0 +y0 |
                                     k0 2        e−ik0 (x0 +y0 ) =        e            ,              (B.25)
                                        k + m2                         ωk
             p
where ωk = ⃗k 2 + m2 . Then we commute the ⃗k integral outside the x and y integrals, and perform the ⃗x
and ⃗y integrals to get
                            Z           Z
                                                                      π                  ⃗
                              d4 x d4 y d3 k f ∗ (x0 , ⃗x)f (y0 , ⃗y ) e−ωk |x0 +y0 | eik·⃗x
                                                                      ωk
                              Z       Z
                                                                          π                 ⃗
                            = d k d4 x d4 y f ∗ (x0 , ⃗x)f (y0 , ⃗y ) e−ωp |x0 +y0 | eik·⃗x
                                   3
                                                                         ωk
                              Z       Z
                                                  π ˜∗                                                (B.26)
                            = d3 k dx0 dy0            f (x0 , ⃗k)f˜(y0 , ⃗k)e−ωk |x0 +y0 |
                                                  ωp
                              Z           Z                      2
                                       π
                            = d3 k           dt f (t, ⃗k)e−ωp t ≥ 0
                                       ωk
given that ωk ≥ 0 and f is supported in positive time only. However, this did not work so simply in
lean, as we require the integrand to be absolutely convergent to use Fubini theorem for exchanging order
of integration. The integrand in the first line of B.26 is NOT absolutely integrable - the integrand
                                                                                                   √ is finite
for x ̸= y, but it relies on the oscillating property. If we take the absolute value, the factor 1/ k 2 + m2 is
divergent under the 3D k-integral. To resolve this, we need to make use of the Schwinger parametrization:
                                        Z
                           ⟨θf, Kf ⟩ ≡ d4 x d4 y f ∗ (x)f (y)K(θx, y)
                                        Z Z                Z ∞                           
                                                                        2
                                     =       f ∗ (x) f (y)        e−sm H(s, |Θx − y|) ds                 (B.27)
                                         x y                 0
                                        Z ∞          Z Z                               
                                                   2
                                     =      e−sm            f ∗ (x) f (y) H(s, |Θx − y|) ds
                                       0               x   y

where                                                              2
                                                         1           r
                                           H(s, r) ≡          exp  −                                     (B.28)
                                                       (4πs)2        4s

                                                           31
is the heat kernel, and bounded by s−2 . The integrand is absolute integrable in this case: the Schwartz
functions f ∗ (x) and f (y) are bounded and integrable in x and y by definition; H(s, r) is bounded, in addition
                                 2
to the exponential decay e−sm on s.1 Therefore, we are allowed to perform the change of integration order
in B.27.
    We then use the fourier representation of the heat kernel
                                                       Z
                                                    −4
                                   H(s, |z|) = (2π)      exp(−ik · z) exp(−s|k|2 )                        (B.29)
                                                                     k

to rewrite the full integral as
                       Z    Z Z Z Z
                                                       2
                                                 e−sm f ∗ (x) f (y) exp(−ik · (θx − y)) exp(−s|k|2 ).      (B.30)
                         s≥0   x   y   ⃗
                                       k   k0

The k0 integral yields                 Z                                      r
                                               ik0 (x0 +y0 ) −sk02                π −(x0 +y0 )2 /4s
                                           e               e         dk0 =          e               .      (B.31)
                                                                                  s
In order to apply Fubini theorem, we will show that the absolute value of the integrand
                                r
                                  π −(x0 +y0 )2 /4s −s(m2 +⃗k2 ) ∗            ⃗
                                    e              e            f (x) f (y) eik·⃗x                         (B.32)
                                  s

is bounded by an integrable function. When taking the norm, exp(i⃗k · ⃗x) has norm 1 and drops out. We can
bound the Schwartz functions by
                                                                                x0 y0
                                       |f (x)||f (y)| ≤ C ·                                                (B.33)
                                                                     (1 + |⃗x|2 )N (1 + |⃗y |2 )N

for some constant C and any N ∈ Z+ , given that x0 , y0 > 0 as f is only defined on positive time. Then we
can use the Gaussian moment formula on the x0 and y0 integrals, and use N = 4 for the spatial integrals to
get
                       Z Z r
                               π −(x0 +y0 )2 /4s −s(m2 +⃗k2 ) ∗                  ⃗
                                 e                e               f (x) f (y) eik·⃗x
                        x y    s
                           Z Z r
                                   π             x0 y0                         2         2 ⃗2
                       ≤C                       2 )4 (1 + |⃗   2 )4
                                                                    e−(x0 +y0 ) /4s e−s(m +k )      (B.34)
                            x y    s (1 +  |⃗
                                            x |            y |
                         4C ′ π −s(m2 +⃗k2 ) √ 2
                             r
                       =         e                πs
                          3    s
where C ′ is C multiplied by the finite result from the spatial integrals. This shows that B.32 is integrable
under the (x, y) double integration. Then we can prove that this is still integrable under the ⃗k ans s integrals:

                                                                                 π 3/2
                          Z    Z                     Z
                                        2 ⃗2                  2
                                   e−s(m +k ) s3/2 =      e−sm s3/2 (π/s)3/2 =                             (B.35)
                            s≥0 ⃗k                    s≥0                         m2

is finite.
     After rearranging the order of integration in B.30, we have
                           Z Z Z Z       r
                                            π −(x0 +y0 )2 /4s −s(m2 +⃗k2 ) ∗            ⃗
                                              e              e            f (x) f (y) eik·⃗x
                            ⃗
                            k x y s≥0       s
                              Z Z Z                                                             (B.36)
                                        π −ω|x0 +y0 | ∗           i⃗
                                                                   k·⃗
                                                                     x
                           =             e           f (x) f (y) e
                               k x y ω
                               ⃗

                 R∞                             p              √
where we used 0 s−1/2 exp(−a/s − bs) ds = π/b exp(−2 ab). This is essentially the exchange of integra-
tion order we wanted in B.26, and the positivity simply follows as proposed.
  1 The exact proof can be found in OS3 foundations, theorem named Schwinger bilinear integrable.




                                                                         32
B.5      Ergodicity (OS4)
Once we know the polynomial clustering statement
                                              P (3.15), OS4 follows quite readily. First instead of proving
ergodicity for functions of the form A(ϕ) = j cj e(ϕ,fj ) , we can reduce the claim to working with single
exponential functions e(ϕ,f ) by Minkowski’s (L2 triangle) inequality and linearity of the integral.

                1 t                                          1 t (Ts ϕ,fj )
                 Z                                 X           Z
                     A(Ts ϕ)ds − Eµ [A(ϕ)]       ≤     |cj |      e         ds − Eµ [e(ϕ,fj ) ]        . (B.37)
                t 0                         2
                                           L (µ)     j
                                                             t  0                               L2 (µ)


As a note for implementation in lean, even this seemingly trivial step was not so easy to implement when
presented to Claude code. In particular the difficulty was in verifying measurability for basic operations such
as linearity of the integral. It was useful to tell Claude code to make general measurability lemmas which
would apply to later arguments.
    The next step is to use linearity and Fubini as follows,
                         Z t                   2            Z t                                         2
                     1                                  1
   Eµ [e(ϕ,f ) ] −             e(Ts ϕ,f ) ds        =             (Eµ [e(ϕ,f ) ] − e(Ts ϕ,f ) )ds
                     t    0                    L2       t    0                                          L2
                                                            Z tZ t                                                                                      (B.38)
                                                      1                             (ϕ,f )         (Ts ϕ,f )                                       ′
                                                    = 2                Eµ [(Eµ [e            ]−e               )(Eµ [e(ϕ,f ) ] − e(Ts′ ϕ,f ) )]dsds .
                                                      t      0     0

The justification for Fubini follows from the Fernique bound which was once again the most difficult part of
the above equation display to implement in lean.
   After a little algebra, using the easy to prove property that C(Ts g, Ts g) = C(g, g) for any Schwartz
function g (this is proven as a lemma in our lean repository), and plugging in the polynomial clustering
bound,

                                               |Eµ [(e(ϕ,f ) − e(Ts ϕ,f ) )(e(ϕ,f ) − e(Ts′ ϕ,f ) )]|
                                               = |Eµ [e(ϕ,f ) ]Eµ [e(ϕ,f ) ] − Eµ [e(Ts ϕ,f )+(Ts′ ϕ,f ) ]|                                             (B.39)
                                               ≤ c(1 + |s − s′ |)−2 .

Plugging this bound back into (B.38) we have,

                                     1 t (Ts ϕ,f )           1 t t
                                      Z                          Z Z
                     Eµ [e(ϕ,f ) ] −     e         ds     ≤c 2            (1 + |s − s′ |)−2 dsds′
                                     t 0              L 2    t    0     0
                                                                       1 t
                                                                          Z
                                                          ≤ c sup            (1 + |s − s′ |)−2 ds                                                       (B.40)
                                                             s′ ∈[0,t] t 0

                                                             1 ∞
                                                                Z
                                                          ≤c           (1 + |s|)−2 ds → 0
                                                             t −∞

as t → ∞. The equation display above was fairly simple to implement in lean.

    The remaining task for OS4 is now to prove the polynomial clustering version (3.15). This property
follows from the following two key results

   1. (Pointwise decay of correlation functions) The covariance function K(x, y) satisfies a bound of the
      form,
                                         |K(x, y)| ≤ c|x − y|−2 e−m|x−y|                           (B.41)
      for some constant c > 0.
   2. (Decay of averaged correlation functions) Let E be a finite-dimensional real normed vector space with
      d = dim E. Let f, g ∈ S(E; C) be Schwartz functions. Let K : E → R be measurable and locally
      integrable. Assume there exist m > 0, CK > 0, R0 > 0 such that for all z ∈ E with ∥z∥ ≥ R0 ,

                                                                       |K(z)| ≤ CK e−m∥z∥ .


                                                                              33
       Then for every α > 0 there exists c ≥ 0 such that for all a ∈ E,
                             Z    Z
                                        f (x) K(x − y) g(y − a) dy dx ≤ c (1 + ∥a∥)−α .                                (B.42)
                                     x∈E       y∈E


   The bound on the covariance above follows from standard large and small scale asymptotics of the Bessel
function K1 (z) which we were able to implement in lean.
   We give more details for the proof of (B.42) since the fact we proved it for Schwartz functions required
some additional argument which one would not find in the textbook of Glimm and Jaffe. The first step is
the following lemma.

Lemma B.1 (Convolution polynomial decay). Assume N > d. Let F, G : E → C be integrable and satisfy

                                                         CF                                  CG
                                      |F (y)| ≤                 ,            |G(y)| ≤               .
                                                     (1 + ∥y∥)N                          (1 + ∥y∥)N
                 R
Define h(x) :=   E
                     F (y) G(x − y) dy. Then for all x ∈ E,

                                                                         C
                                                         |h(x)| ≤
                                                                    (1 + ∥x∥)N
                                
for C := 2N CF ∥G∥L1 + CG ∥F ∥L1 .

   Proof (domain split at ∥y∥ = ∥x∥/2). Fix x ∈ E and split E = A ∪ B with

                                   A := {y : ∥y∥ ≥ ∥x∥/2},               B := {y : ∥y∥ < ∥x∥/2}.

Then                                       Z                                     Z
                                |h(x)| ≤        |F (y)| |G(x − y)| dy +               |F (y)| |G(x − y)| dy.
                                           A                                      B

On A we have 1 + ∥y∥ ≥ (1 + ∥x∥)/2, hence (1 + ∥y∥)−N ≤ 2N (1 + ∥x∥)−N and

                                                               CF           2N CF
                                               |F (y)| ≤             N
                                                                       ≤            .
                                                           (1 + ∥y∥)     (1 + ∥x∥)N

Therefore
                                                          2N CF                                      2N CF
                 Z                                                   Z
                         |F (y)| |G(x − y)| dy ≤                             |G(x − y)| dy =                 ∥G∥L1 ,
                     A                                 (1 + ∥x∥)N        E                        (1 + ∥x∥)N
using translation invariance in the last equality.
   On B, the triangle inequality gives ∥x − y∥ ≥ ∥x∥ − ∥y∥ > ∥x∥/2, hence similarly

                                                                        2N CG
                                                      |G(x − y)| ≤              .
                                                                     (1 + ∥x∥)N

Thus
                                                            2N CG                                  2N CG
                     Z                                                   Z
                             |F (y)| |G(x − y)| dy ≤                             |F (y)| dy =              ∥F ∥L1 .
                         B                               (1 + ∥x∥)N          E                  (1 + ∥x∥)N
Adding the two bounds gives the claimed estimate.
    The rest of the proof of (B.42) involves similar arguments decomposing the domain of integration into
‘singular’ and ‘tail’ regions so we assume it for the rest of the argument.
Proof sketch of OS4 (polynomial clustering) for the massive GFF. Fix α > 0 and test functions f, g ∈ S(R4 ; C).
By definition of Ts ω as the dual action on distributions, and bilinearity of the inner product,

                          Eµ e⟨ω,f ⟩+⟨Ts ω,g⟩ = Eµ e⟨ω,f ⟩+⟨ω,T−s g⟩ = Eµ e⟨ω,f +T−s g⟩ .
                                                                                  




                                                                    34
   Next, for a centered Gaussian field with covariance bilinear form S2 (·, ·) (the Schwinger 2-point function),
one has the standard identity

                        Eµ e⟨ω,f +T−s g⟩ = Eµ e⟨ω,f ⟩ Eµ e⟨ω,T−s g⟩ exp S2 (f, T−s g) .
                                                                                 


   Moreover, by time-translation invariance of the GFF, Eµ e⟨ω,T−s g⟩ = Eµ e⟨ω,g⟩ . So defining the con-
                                                                              

stants, Ef := Eµ e⟨ω,f ⟩ ,  Eg := Eµ e⟨ω,g⟩ , we have,
                                         


                            Eµ e⟨ω,f ⟩+⟨Ts ω,g⟩ − Ef Eg = Ef Eg exp(S2 (f, T−s g)) − 1 ,
                                                                                    
                                                                                                         (B.43)

and using the elementary inequality (valid for all z ∈ C), | exp(z) − 1| ≤ |z| e|z| ,

                    Eµ e⟨ω,f ⟩+⟨Ts ω,g⟩ − Ef Eg ≤ |Ef | |Eg | |S2 (f, T−s g)| exp(|S2 (f, T−s g)|).
                                      
                                                                                                         (B.44)

So it suffices to prove a polynomial bound

                                       |S2 (f, T−s g)| ≤ cdecay (1 + s)−α        (s ≥ 0),                (B.45)

with some constant cdecay ≥ 0 depending on (f, g, α).
   Finally recalling that
                                                    Z Z
                                  S2 (f, T−s g) =           f (x) K(x − y) g(y − τs ) dy dx.,            (B.46)
                                                    x   y

we are now in a position to apply the main Schwartz double integral decay bound (B.42). As a result, there
exists a constant cdecay ≥ 0 such that for all a ∈ R4 ,
                           Z Z
                                f (x) K(x − y) g(y − a) dy dx ≤ cdecay (1 + ∥a∥)−α .
                              x    y

Taking a = τs and using 1 + ∥τs ∥ = 1 + s gives exactly (B.45).
   Finally combining (B.44) and (B.45) we have

                 Eµ e⟨ω,f ⟩+⟨Ts ω,g⟩ − Ef Eg ≤ |Ef | |Eg | cdecay (1 + s)−α exp cdecay (1 + s)−α ,
                                                                                              


and since (1 + s)−α ≤ 1, (3.15) holds with constant

                                               |Ef ∥ ∥Eg ∥ cdecay ecdecay ≥ 0,

which is the desired OS4 polynomial clustering bound.
   Finally, for completeness the file OS/NonTrivial verifies that the correlation functions are nontrivial, as
taking ϕ(x) = 0 would satisfy the axioms.




                                                                35
