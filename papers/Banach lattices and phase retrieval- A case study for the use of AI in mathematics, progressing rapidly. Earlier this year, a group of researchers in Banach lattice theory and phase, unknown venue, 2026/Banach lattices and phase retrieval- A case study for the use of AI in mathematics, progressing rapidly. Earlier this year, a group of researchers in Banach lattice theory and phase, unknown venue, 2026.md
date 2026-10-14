                                           BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE
                                                           USE OF AI IN MATHEMATICS

                                                 JAUME DE DIOS PONT, LUKAS LIEHR, DAVID MUÑOZ-LAHOZ, MITCHELL A. TAYLOR,
                                                                         AND PEDRO TRADACETE


                                                 Abstract. The ability of large language models to assist professional mathematicians has been
                                                 progressing rapidly. Earlier this year, a group of researchers in Banach lattice theory and phase
                                                 retrieval began incorporating this technology into their research workflows. Facing challenges about
                                                 the reliability of these models, they also decided to couple the discovery process with Lean verifica-
                                                 tion. Here, we present a case study of how this has led to a more united community and a deeper
                                                 understanding of our field.
arXiv:2608.07396v1 [math.FA] 7 Aug 2026




                                                                                        1. Introduction
                                             The purpose of this note is to give an account of some of the progress made in the last five months
                                          in Banach lattice theory and phase retrieval, with a focus on how we have begun to incorporate
                                          technology into our research. Our objective will be to explain how Lean, large language models
                                          (LLMs), and a dedicated team of mathematicians working in unison can achieve an improved
                                          understanding of their field, a more united community, and even uncover new opportunities to
                                          connect their research with other areas of STEM.

                                             In the following, we briefly explain the three essential ingredients that were combined to achieve
                                          a broader understanding of our field of mathematics. Interestingly, this enhanced understanding
                                          occurred at many different levels, beginning with the core theory and the overall geometry of our
                                          field (as we needed to build a Lean library of useful facts, which required us to revisit the classical
                                          theory and better explore how known results depended on each other) and culminating at cutting
                                          edge research.
                                          1.1. Lean. Lean [8, 27] is an interactive theorem prover and functional programming language
                                          designed for writing mathematically precise definitions, statements, and formal proofs. At its core,
                                          Lean is based on dependent type theory, where propositions are represented as types and proofs
                                          are terms inhabiting those types. The Lean kernel is responsible for checking that each term has
                                          the claimed type. Under the propositions as types correspondence, this means that the Lean kernel
                                          checks, using only the foundations of dependent type theory, that a given proof is correct.

                                             Thus, if we have a Lean verified proof of a theorem, and we are sure that the statement of
                                          the theorem in Lean code faithfully represents the statement in the way we traditionally write
                                          mathematics, then we can be certain that the statement holds in the given axioms of mathematics.
                                          However, proof checking has traditionally been limited by scale. Lean proofs must contain all of
                                          the details—there is no room for interpretation. Even though Lean does a great job at providing
                                          algorithms (called tactics) that can help you fill in terms automatically, writing complex mathemat-
                                          ics in Lean is challenging and time-consuming. This is where the coding capabilities of generative
                                          AI can be exploited to write Lean at a scale useful for research-level mathematics; this process is
                                          described in more detail in Section 3.
                                          1.2. Large language models. Large language models are AI systems trained on vast collections of
                                          text and code to generate language. Given a prompt, an LLM produces an answer which is a likely
                                                                                                   1
2           J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


continuation in terms of the patterns that it has learned during training. For mathematical research,
LLMs can be very helpful for identifying possible connections between fields and producing sketches
of proofs. However, there is no mathematical certainty in their arguments. Moreover, although
some progress has been made in solving certain problems using LLMs, the vast majority of open
research questions cannot be given to the models we used with any expectation that they will solve
them correctly.

1.3. Our community of mathematicians. We are a group of researchers in Functional Anal-
ysis and Applied Harmonic Analysis who have been incorporating Lean and LLMs into our daily
mathematical lives. This note describes some of our experiences over a 4-5 month span. Dur-
ing this period, we used LLMs and Lean as research tools for both mathematical exploration and
verification. Throughout the process, we continued our usual mathematical duties, such as select-
ing meaningful problems, contributing numerous novel ideas, and connecting our work to relevant
literature. However, we also aimed to recognize useful contributions from LLMs, which required
digesting and evaluating their outputs and deciding whether it could lead to a deeper understanding
of our field. The purpose of this note is to provide a concrete and transparent account of what
worked for us, what failed, and how these tools affected our research and our community. However,
we do not wish to claim that any of our practices are optimal or should be incorporated by the
wider mathematical community.

   Several related articles help to put our work in context. Tao in [25] surveys a broad range of
machine assisted methods and presents LLMs as tools that can complement expert mathematical
judgment. Buzzard, Commelin, and Massot demonstrated in [6] that researchers in mathematics
with no direct background in computer science can become effective in the usage of formal veri-
fication methods in a reasonably short amount of time. Davies et al. [7] describe a methodology
in which machine learning techniques identify patterns that professional mathematicians interpret
and convert into conjectures and proofs. The present note brings these themes together with LLM-
assisted exploration, Lean verification, subject-specific library building and the careful outreach
and training of a mathematical community.

   It is important to emphasize that we are not the only mathematicians incorporating LLMs into
their research. By now, there are hundreds of articles on ArXiv that disclose the usage of AI
tools. There are also many initiatives such as the DARPA expMATH program and numerous
AI4Math startups including Harmonic, Axiom Math and Math, Inc. Various perspectives on AI
in mathematics have also been shared at the Future of Mathematics Symposium at Stanford and
in white papers such as [2, 13]. Within these reactions stands the Leiden Declaration on Artifi-
cial Intelligence and Mathematics, published on June 2, 2026, and endorsed by the International
Mathematical Union. This declaration has called for responsible governance of AI in mathematical
research. It is a community statement, which up to now has been signed by around 3000 people
https://leidendeclaration.ai/. It argues that although AI tools may affect many aspects of
our job, these tools should not alter core values such as correctness, transparency, honesty, attribu-
tion, ethics, open science, independent verification, human understanding, community values, and
research autonomy. In this article, we will describe some of the benefits that we have received by
following these protocols, and how they have led not only to an improved understanding of our
subject, but also to deeper scientific relationships with our colleagues.


1.4. Outline of the article. In Section 2, we give a brief introduction to our mathematical field.
This section is technical and can be skipped on the first reading. In Sections 3.1 and 3.2, we recall
our experiences using Lean and LLMs in the years 2024 and 2025. Then, in Section 3.3, we explain
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS                 3


how we recently combined these technologies. A more detailed summary of the progress made in
the last five months in phase retrieval and related areas is given in Section 3.4.

   In Section 3.5, we briefly explain our new Banach lattice library, referring the reader to [19] for
more information. A discussion on the importance of Mathlib and the shortcomings of our library
is presented in Section 3.6. An explanation of why we have chosen to formalize our results is given
in Section 3.7. Finally, Section 3.8 records some of the recent LLM-assisted progress in Banach
lattice theory (mainly by students). We remark that this latter section contains several technical
terms; the reader is encouraged to ignore all undefined terms and focus on the main message.

   The article concludes with Sections 4 and 5, which discuss some of the community aspects of
this endeavor, as well as a few future plans.

                             2. Banach lattices and phase retrieval
   In this section, we give some basic background and motivation for our field. The reader who is
solely interested in the discussions on Lean and LLMs can skip to Section 3.

   The phase retrieval problem arises in numerous physical scenarios, ranging from crystallography
and speech recognition to quantum mechanics. Mathematically, one begins with an injective linear
operator T : H → X which maps a signal space H to a function space X. The operator T usually
describes some physical phenomena, where, in practice, one is only able to measure the modulus |T x|
of the signal x ∈ H. A classical example is the Pauli problem, where T : L2 (Rd ) → L2 (Rd ) × L2 (Rd )
is the mapping T ψ = (ψ, Fψ). In this example, |T ψ| grants access to |ψ|2 and |Fψ|2 , which are
interpreted as the probability densities of position and momentum of a quantum particle. Pauli’s
problem asks to what extent such data allows one to recover the original wavefunction ψ.

   Note that in the phase retrieval problem, there is always an inevitable ambiguity; namely, for any
unimodular scalar λ, we have |T x| = |T (λx)|. Therefore, the best one can hope to do is recover the
original signal x up to global phase. This ambiguity is often harmless in practice, as global phase
does not usually carry physical meaning. With this in mind, one can frame the uniqueness problem
for phase retrieval as follows: Given an injective linear operator T , is it true that |T x| = |T y| if
and only if x = λy for some unimodular scalar λ?

   Other common examples of operators T which are relevant for phase retrieval include the Fourier
transform F and the short-time Fourier transform Vh with window function h ∈ L2 (Rd ). These
phase retrieval problems occur in imaging applications. Indeed, in classical crystallography, if one
calls the image one wants to see f , then the detector records the power spectrum |F f |2 . Thus,
one is tasked with the problem of recovering the original object f from the distorted image |Ff |2 .
Since the Fourier transform is a unitary operator, this task is clearly impossible, unless one knows
a priori information about the object f . However, one often does,1 meaning one may assume that
f ∈ F ⊆ L2 (Rd ) for a proper subspace F ⊆ L2 (Rd ). In this case, the model operator is T := F |F .

   Since obtaining a priori information on f is often difficult, practitioners have designed experi-
ments that incorporate additional redundancy. For example, in ptychography, a mask or window
h is inserted, so that one measures |F(f h)|2 . One then translates the window h (or sometimes
the object f ), resulting in measurements of the form |F(f Tx h)|2 , where Tx denotes the transla-
tion operator by x. In other words, one now measures |Vh f |2 and wishes to recover f . Since
Vh : L2 (Rd ) → L2 (R2d ), this experimental setup affords a whole variable of redundancy, which one
hopes to use to offset the loss of phase information without needing to impose additional constraints
  1A natural constraint may, for example, be the support properties of f .
4             J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


on f ∈ L2 (Rd ). Mathematically, it immediately connects the phase retrieval problem to the field
of time-frequency analysis.

   The discussion above has been entirely algebraic. However, in practice, there will always be
measurement errors, so one does not only desire uniqueness in the phase retrieval problem but also
stability. In other words, one desires an inequality of the form
(1)                           inf ∥x − λy∥ ≤ C∥|T x| − |T y|∥,      x, y ∈ H.
                             |λ|=1

In practice, the operator T is bounded and, moreover, if such an inequality is to hold, then T −1
must also be bounded. Therefore, we have the proportionality
                                     inf ∥x − λy∥ ∼ inf ∥T x − λT y∥.
                                     |λ|=1            |λ|=1

Up to changing the constant C, we may therefore rewrite (1) as
(2)                        inf ∥f − λg∥ ≤ C∥|f | − |g|∥,      f, g ∈ E := T (H).
                          |λ|=1

The utility of the reformulation (2) is that it removes the operator T from the nonlinear inequality
and instead uses the operator T to select the subspace E := T (H) ⊆ X where the nonlinear
inequality is desired to hold. It also immediately connects stable phase retrieval to the theory of
Banach lattices, which, in essence, can be defined as the spaces where all of the symbols in (2)
make sense.

  Banach lattices are the natural abstraction of function spaces such as Lp (µ), C(K), Orlicz spaces
and Lorentz spaces. They are defined as Banach spaces (X, ≤) equipped with a lattice order (so
that |f | := f ∨ (−f ) := sup{f, −f } exists) satisfying the natural compatibility conditions:
      (1) f, g, h ∈ X, f ≤ g implies f + h ≤ g + h.
      (2) f ∈ X, λ ∈ R+ , f ≥ 0 implies λf ≥ 0.
      (3) |f | ≤ |g| implies ∥f ∥ ≤ ∥g∥.
These objects have been intensively studied for decades, but it was only recently noticed that the
theory has major implications on the mathematics of phase retrieval.

   Banach lattices are not only modeled after spaces of functions, but can be truly represented as
such. For instance, Kakutani’s C(K)-representation theorem guarantees that every Banach lattice
is (in a possibly inequivalent norm) “locally” a space of continuous functions on some compact
Hausdorff space K. Banach lattices also admit global representations as closed sublattices of ℓ∞ -
sums of L1 -spaces. However, in some sense, they are much more than just spaces of functions. For
example, they have a rich categorical structure, as shown by the recent development of free objects
in Banach lattices and related categories (see [20] and the references therein).

  A relevant part of the literature on Banach lattices is concerned with the interaction with Banach
space theory. However, there are also natural overlaps with vector lattice and order theory, which
have a more algebraic flavor. The theory of Banach lattices also has a longstanding interaction
with operator theory and a number of applications in mathematical economics. The Positivity
conference series serves as a consolidated meeting point for the community.

                3. Our experience using Lean and Large Language Models
  Here, we will give a broad overview of our experiences using LLMs and Lean to improve our
mathematical research.
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS                       5


3.1. Our first steps into formalization. The first result in Banach lattice theory to be formal-
ized was Kakutani’s C(K)-representation theorem. This theorem states that any Banach lattice
whose unit ball contains a largest element must, in fact, be a space of continuous functions on a
compact Hausdorff space K. Moreover, in this case, the largest element can be identified with the
constant function 1.

  Given any positive element e in a Banach lattice X, we may define the principal ideal
                                 Ie := {x ∈ X : ∃ λ ∈ R with |x| ≤ λe}.
This ideal has a natural norm, ∥ · ∥e , defined for x ∈ Ie as the smallest real number λ ≥ 0 for which
|x| ≤ λe. It is routine to show that this norm is complete. Hence, by Kakutani’s theorem, (Ie , ∥ · ∥e )
is lattice isometric to a space of continuous functions on a compact Hausdorff space Ke .

   The fact that Banach lattices are “locally” C(K)-spaces (albeit in the ∥ · ∥e norm rather than
the original ∥ · ∥X norm) is fundamental to the theory. In particular, it implies that any inequality
between real numbers that involves only finitely many linear and lattice operations will remain true
in any Banach lattice. Indeed, if x1 , . . . , xn ∈ X, then we may define e := |x1 | + · · · + |xn | and view
x1 , . . . , xn ∈ Ie = C(Ke ). In C(Ke ), the order is pointwise, so if an inequality involving only linear
and lattice operations is true for real numbers, it is also true in C(Ke ), and hence in X.

   Kakutani’s C(K)-representation theorem was formalized by DML on December 19, 2025. The
formalization took around one month, did not involve any use of AI and can be accessed via the
following link:
                          https://github.com/davidmunozlahoz/veclat.
The motivation for DML to learn Lean and formalize this theorem was mainly curiosity. Intrinsic
interest was also the main catalyst for JD to learn Lean, who then taught a seminar and a full
course on formalization at ETH Zürich in 2025. These lectures were attended by S. Bertolini and
MT. As will be discussed below, formalization is not easy, and having experienced people who knew
how to formalize mathematics by hand was essential to our project.
3.2. Our first experience with LLMs. The first experience where an LLM had a positive impact
on our research occurred in late 2024, with the paper [21]. Here, our goal was to precisely quantify
the failure of the hot spots conjecture by computing the hot spots ratio Sd .
                                                                              √
   Interesting results from [16, 24] show that Sd ≤ 60 and lim supd→∞ Sd ≤ e. Motivated by an
informal suggestion in [11], we used GPT to help perform a relatively routine computation using a
family of spherical Neumann sieves  √to give a lower bound on the hot spots ratio. To our surprise,
this showed that lim inf d→∞ Sd ≥ e.

   In view of the above, it was natural to conjecture that the spherical sieve construction would give
the exact value of Sd in every dimension d. After several weeks of thinking about this problem, we
asked GPT for some ideas. In a multi-turn conversation, GPT suggested combining three standard
ingredients that we thought were too naive to be sharp. Although the execution of the LLM was
completely incorrect, we did eventually produce a corresponding upper bound on Sd using exactly
these tools.

  We emphasize that the above experience was not at all reproducible and we were unable to
extract another novel mathematical insight from an LLM until March 2026.
3.3. Combining LLMs and Lean. The first paper that we autoformalized was [1]. The main
bulk of the formalization was completed in early-mid March, 2026. The motivation for formalizing
this result was mainly to see if it was possible. However, we learned through trial and error that
6           J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


not only was autoformalization possible, but it can also be highly instructive. Indeed, our original
proof in [1] relied on a concentration compactness scheme, which we found to be extremely difficult
to formalize. We therefore spent a significant amount of time working with LLMs to make the proof
simpler and more quantitative. By the end of the project, we had not only a Lean verification of
our theorem, but an alternative, more elementary (though perhaps less illuminating) proof. Both
of these proofs were presented in [1], as they contained interesting and complementary ideas.

    The biggest shift in our perspectives on the usage of LLMs in mathematics came during a visit
of JD to ETH Zürich during the week of March 19-25, 2026. During this week, we were working
on the L2 -stability problem for STFT phase retrieval. This is a problem that we had thought
about for a long time in collaboration with several other mathematicians. We had made significant
progress on it, but had not yet reached a final solution and had no indication that we would be
able to. We therefore tried to see if we could get some new inspiration by discussing the problem
with GPT 5.4 Plus. During a multi-turn conversation, GPT offered a largely incorrect execution of
a possible strategy to prove the main lemma to which we had reduced the local stability problem
at the constant function 1. However, as mathematicians familiar with the problem, we quickly
realized that the overall strategy was sensible and would allow us to complete our proof. Moreover,
using our previous notes, our autoformalization experience from [1] and guiding GPT to correctly
fill in the missing details, we were able to obtain a Lean verification of the solution in less than 72
hours. Interestingly, a large percentage of the formalization was completed while we were visiting
PSI, which contains a leading ptychography lab in Switzerland. As we will discuss in Section 5, we
hope that LLMs will help bridge the gap between physics and mathematics, leading to numerous
new and exciting collaborations.

   As mathematicians, our job is not only to solve problems, but to find beautiful proofs and to
ask natural followup questions [28]. In the first experience mentioned above [1], we were able to
find a new and instructive proof of our result. In the second experience [4], it was clear to us
that the proof would generalize significantly. Indeed, although our original goal was to prove local
stability in the Fock space (identified with the image of the STFT with Gaussian window) at the
constant function in one dimension, it was clear that the proof architecture would generalize to
prove local stability for all Hermite windows at all elements in the finite span of the canonical basis
and in all dimensions. However, it was also clear that the proof would be largely technical and
not instructive. We therefore experimented, breaking the generalization into multiple steps, giving
the LLMs the Lean-verified proof from the previous step, working with them to get a proof of the
next step, Lean verifying that step, and then repeating the strategy at the next level of generality.
This process took roughly six weeks, which we estimate to be about the same amount of time that
it would have taken us to write the proof carefully by hand. However, as mathematicians with
significant experience writing technical proofs, this alternative strategy was both more instructive
and more enjoyable for us.
3.4. Next steps: Formalizing papers and building libraries. After the above two experi-
ences, we contacted several members of the phase retrieval and Banach lattice communities to see
if they would be interested in an experiment to systematically incorporate LLMs into our math-
ematical lives. In certain cases, this was met with extreme enthusiasm and in other cases with
skepticism or concern for the future of mathematics. The large variance in reactions is, of course,
completely natural, and we therefore tried to work with people on as personal a level as possible.
This ranged from some members using LLMs on a daily basis, others wishing to have a weekly
meeting to discuss team progress, and others who preferred to wait until we had strong evidence
that this would be a viable new way of doing mathematics and a systematic way to teach them
how to properly use it. In all of the above cases, respect for people’s opinions was our top priority.
With that being said, we will comment below on some of the outcomes of the last few months.
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS                   7


   As mentioned above, our first experience with autoformalization was [1]. Here, we already had
an informal proof of our main result, and we wanted to formalize it in Lean. The key lesson was
that formalization often forces one to rethink and simplify the proof and in this case it lead to
new insights on the problem. We remark that these insights cannot be observed from the theorem
statement itself, which did not change. However, mathematics is not just about solving problems.
It is also a quest to find deeper understanding, which makes having multiple proofs with different
insights fundamentally important.

   Our second experience with autoformalization was [4]. This involved a major collaboration with
LLMs both at the formalization stage and at the proof discovery stage. This problem was introduced
to MT by J. Ramos, who was able to prove the result for squares. The proof of this is instructive
and will likely be submitted for publication soon. However, we could not adapt the method to
prove the result in general. Instead, we developed other strategies, important reductions, and
began discussing with other people as well. As mentioned above, the key breakthrough occurred
when GPT 5.4 offered a new perspective on the problem, incorrectly executed, but observed to be
important by us. We then properly incorporated this new insight into the scheme of proof that we
had been developing before. Another interesting application of the LLMs was to help generalize the
result – based on the same ideas – to a more natural statement. This roughly doubled the length
of the proof, but, more importantly, allowed the authors to focus the exposition on the ideas rather
than on the routine, but technical, details.

   Another interesting experience occurred in the article [15]. In this paper, we investigated a
problem that we believed to be within reach, but with a solution that lied outside of the expertise
of anyone who had worked on the problem previously. Indeed, this was a problem in time-frequency
analysis where the solution was naturally obtained by a topological argument involving Chern
classes. Our interest in this problem came from our desire to better understand time-frequency
analysis and its connection to phase retrieval. Notably, we are not experts in topology, but we
felt that this problem had a topological flavor. We therefore worked with GPT 5.4 to obtain our
desired counterexample. However, not being complete experts in all of the material, we also wanted
to know with absolute certainty that the proof was correct. We therefore autoformalized the result
in Lean, which gave us complete confidence that our argument was sound. Moreover, as in [4], we
naturally extended the counterexample to its rightful level of generality. This experience highlighted
that solutions to certain problems that a priori seem out of reach may sometimes be obtained by
using techniques from other areas of mathematics. This leads both to an incredible opportunity to
connect fields and learn new mathematics, and to a concern that the proposed execution is indeed
correct. In our case, Lean helped ensure that our argument was indeed airtight.

   A second issue in [15] was that formalizing the statement of our theorem in Lean in a manner
digestible to a non-expert was quite difficult. In fact, in our original theorem, the statement would
have likely been impossible for anyone except a Lean expert to understand. Therefore, we spent a
lot of time and effort reformulating and refining our theorem. In the end, we found a much simpler
way to state the result. Interestingly, the task of properly formalizing and refining the theorem in
Lean also led us to discover several new examples, equivalences and structural phenomena related
to the underlying theory that we would not have found if we had not put in this effort. These
additional findings will be reported on in a separate article, which will likely involve more difficult
Lean statements and definitions. In particular, in this case, we expect that it will be more efficient to
carefully formalize the concepts that we are repeatedly using and incorporate them into a reusable
library.
8           J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


   The next paper that we highlight in detail is [14]. This paper was correctly Lean verified – with
almost no guidance – by LL. This is quite remarkable, as he had no experience with Lean three
months ago. Of course, those more experienced with Lean carefully checked that the verification is
correct, which was an extremely important part of the process. This success was made possible by
a broader effort to help our community to get started with Lean. Indeed, we have been designing
tutorials to conveniently set up and teach Lean to our community [18]. We also emphasize that
translating statements from natural language into Lean is not at all trivial and that the models we
used struggled significantly with formalizing definitions. Therefore, a careful, hands-on approach
to teaching Lean was an imperative part of our community project.

   As mentioned above, autoformalization can lead to improved understanding. However, we wish
to acknowledge that the opposite can also be true. Indeed, we had one rather surprising situation
where GPT 5.4 in Codex quickly constructed an ambiguity function with a bounded spectral gap,
which we knew had some implications in STFT phase retrieval. The construction was technical
and, being skeptical that it was correct, we decided to run it through Lean. Surprisingly, within 48
hours we had a certificate of the correctness of the theorem. However, in the spirit of Thurston’s
insightful article [28], we did not feel that we had a proof of this theorem. To avoid a Faustian
deal, it was therefore very important for us to revisit the argument, understand it, make it more
general, make it more enlightening, and to track the entirely omitted references to where the ideas
came from. As Klowden and Tao emphasize, formal correctness of an argument captures only the
logical validity but it does not communicate to a reader why the proof works, what ideas it is based
on, or how the argument might generalize [13, Section 4.4]. In this vein, we would also like to stress
the importance of traditional methods of mathematical communication, such as discussing with
colleagues and preparing slides for talks. Indeed, the intent to communicate mathematics often
leads to a deeper understanding of the mathematics itself, and in our case JD even discovered a
new mechanism behind one of our recent proofs while preparing a talk on it.

   We have had several other experiences in addition to the above. Personal and group dynamics
will be discussed further in Section 4 and experiences (mainly by students) with the use of LLMs as
research assistants can be found in Section 3.8. For now, we emphasize that there have been many
more failures than successes. Indeed, although we have focused on the successes above, the majority
of the time the LLMs did not know how to make any progress on the problem and just outputted
nonsense. Moreover, being limited by context length, the models we used rarely produced anything
reliable that was more than 5-10 pages. This made human intuition and guidance imperative, as
answering a difficult problem often took months of human-AI discussions. However, as we remarked
above, there were a few cases in which the LLMs were able to solve a problem remarkably quickly.
Although these proofs never required truly new ideas, it was sometimes striking how well the LLMs
were able to answer certain problems. As mentioned above, in this case, our job was to understand
the proof, put it in its proper generality, do a literature search to find out where the method of
proof came from, and then ask and investigate the next natural followup question.


3.5. The Banach lattice library. When formalizing papers, our main objective was to get a
Lean verification. However, when using LLMs directly, the quality, reusability, and organization of
the code can be very poor. The only parts of the code that were intensively reviewed by us were
the statement of the theorem and the definitions it relied on. These were decoupled from the Lean
proof, and carefully explained in both the paper and the GitHub repository. We were also careful
to pick problems where the statement, together with all definitions, could be formalized in an easily
digestible manner. We remark that neither of these approaches scale: One instead wants to build
detailed, reusable libraries, so that one can easily verify complicated theorems which rely on many
definitions in an efficient manner.
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS                  9


   Thus, with this approach in mind, the library [19] will serve two main purposes. On the one
hand, it will be a trusted base of knowledge, in which the community reaches a consensus that the
formalized definitions correspond to the actual definitions used in the field. As noted above, when
working on an autoformalization project, it is not uncommon for LLMs to make slight changes
to the definitions that greatly simplify the proofs of the theorems. Thus, careful checking of the
definitions becomes paramount. This means not only checking the definitions that appear in the
theorem, but also the definitions that these definitions depend upon, and so on. The only way one
can perform this recursive task efficiently is if, as close to the main theorem as possible, definitions
only depend on a trusted library, and therefore one can be certain that they faithfully represent
the concepts that they claim to represent. In particular, we stress that formalization merely shifts
the burden of trust from the proofs to the statements and definitions. With the inherent scale and
complexity of mathematics, it is therefore necessary for numerous people to carefully review and
certify the material in the library so that it can be trusted.

   On the other hand, libraries serve as code infrastructure to make most formalizations not only
feasible, but also efficient. If, eventually, we want formalization of research to become a mathemat-
ical standard (at least in our community), sustainability and affordability of the autoformalization
process are critical. No one knows what the cost of LLM tokens will be in the future, but it is in
our best interest to keep the ratio of mathematical output to token usage as high as possible. One
clear way to accomplish this is by having shared and reusable code in the form of a library.

   This is the reason we started the Banach lattice library [19]. This library was coded making
an intensive use of LLMs, but with careful human supervision; we could say that it was “semiaut-
oformalized.” Although the resulting code cannot be compared to that of purely human-written
libraries, the supervision process made sure that the definitions are correct, the approaches to for-
malizing the different concepts are reasonable, and that the organization of the library is clean,
understandable and practical for researchers.

   At the same time, the sacrifice in code quality had a benefit in the form of scale, to the point
where we could use it to naturally formalize three research-level results and constructions. We
expect that, as other researchers join the project, they will greatly expand the library in their
directions of interest and be able to formalize their own research. Indeed, we have reasons to
believe that this level of scale is possible. The library project was launched at the beginning of
April, 2026, and so far DML has been its sole contributor. After two months of part-time work, and
starting from the definition of a Banach lattice, we got the library to a point where the formalization
of the three research-level results mentioned above, including the solution to an open question that
was solved very recently, was possible. Needless to say, our library builds on top of Mathlib; this
would not have been possible without the enormous human effort that has been put into writing,
reviewing and curating Mathlib, as discussed in the next section.

  As a desired by-product of building the library, we gained new mathematical insights into the
theory of Banach lattices, which are reported in detail in [19, Section 3]. This emphasizes the idea
that the process of building the library is not only about producing formally-verified facts, but also
about improving our understanding of mathematics.

3.6. The importance of Mathlib. As mentioned above, none of our formalization projects would
have been possible without Mathlib. Mathlib is the core reason for our trust in our formalizations,
and this trust stems from the fact that Mathlib is thoughtfully designed, from definitions, to theo-
rems, to proofs. Moreover, the extreme care of the Mathlib community in formalizing mathematical
objects has ensured that their meaning faithfully represents what the mathematical community ex-
pects. This, in turn, has ensured that the material in Mathlib may be intuitively and reliably
10              J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


extended to formalize more advanced concepts. Indeed, if such care were not taken, formalizations
of advanced topics would become exceedingly messy, and hence more prone to misinterpretation.

   Our library is not yet at the level of Mathlib. Its purpose is to facilitate mathematical research,
and for this reason we have had to sacrifice code quality. However, it is an evolving project that
we hope will both expand and improve over time. In this regard, we would like to emphasize the
formalization scales suggested in [26]. The formalization of our papers (so far) is at the lowest
level of formalization, as the goal is solely to verify correctness. However, we would argue that
our library lies somewhere between levels 2 (Publication-level formalization) and 3 (Prototype-level
formalization). The increase in quality of the library compared to that of the papers is to ensure
reusability and trust. However, our library leaves much to be desired. In particular, we wish not
only for it to expand over time, but also for the core material to be revisited. Indeed, this has
already happened, as after proving a new result we realized that we needed to frame certain concepts
in the library in the language of locally solid topologies. Importantly, given the infrastructure that
we had already built, this was not difficult, as many of the proofs were identical. It was also
an instructive experience, as the authors learned about the utility of locally solid topologies from
redoing parts of the library at this level of generality.

   Complementing the scales of formalization in [26], we also remark that there are scales of under-
standing. Three of the authors are very familiar with executing technical details in Banach lattice
theory, but, through the process of semiautoformalization, we learned a significant amount about
the large scale structure of our field. We believe that the scales of formalization and understanding
can be symbiotic. Indeed, the process of carefully formalizing a proof leads to an extreme under-
standing of the fine details of a small subfield, as it causes one to deeply reflect on the mathematical
structures at play. However, semiautoformalizing a library also leads to fundamentally new insights
about the overall architecture of one’s field.

   We remark that we have also limited our scale compared, e.g., to [22]. Our goal was to build
a reusable, trusted and affordable research-level library in our specific research field, so we did
not pursue utmost scale or speed. Instead, we picked a pace where human understanding and
trust in the library could be easily obtained. In the near future, we hope to encourage researchers
in our field to extend the library at the same quality level to cover their topics of interest, and
concurrently revisit the core of the library to improve code quality, put results in proper generality,
and encourage students and researchers to learn more about the fine details of the field. We also
emphasize that we are continually learning, and refer the reader to [10] for additional perspectives
on formalization.

3.7. Why we are formalizing our papers. The main reason that we have decided to formalize
our papers is to ensure correctness against LLM hallucinations. Indeed, there have been several
instances (see Section 3.8) where we were able to generate a proof that looked entirely correct,
but with a subtle error – even in just a single line – invalidating the whole argument. In many
cases, finding the mistake was not trivial: It required a lot of patience, mathematical intuition and
skepticism, and, without this, the mistake could have easily been missed.2 Moreover, we have found
that models are getting better at hiding their lies. Indeed, we have had a recent experience where
five independent agents certified essentially the same argument, which turned out to be completely
wrong.

   We also note another experience, where an LLM offered a proof of a major conjecture in Banach
lattice theory. In this case, the reasoning of the LLM was entirely correct. However, it relied on an

     2Especially since we wanted to believe that the result was true.
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS 11


external reference, which we later read and found to have a gap. Again, this is an example where
skepticism and mathematical intuition allowed us to find the error in the reasoning. However, it
also brought us new awareness on potential difficulties in carefully validating LLM-assisted proofs.

   Formalizing mathematics in Lean is a partial solution to this issue. However, Lean is not a black
box that outputs the correctness of your theorem. Indeed, formalizing definitions and translations
of natural language statements into Lean code requires tremendous skill and precision (in [12] this
is called the specification gap: Lean can formally verify the correctness of a statement but it cannot
guarantee that the statement faithfully expresses the intended mathematical theorem). Learning
how to do this takes time, and has not been easy for our group. To partially remedy this, we
have designed tutorials to help people in our community learn Lean, and we have experts available
to answer any questions and to certify that Lean translations are correct. Notably, this strategy
does not immediately scale, as we can only reliably teach these high standards to a small group of
devoted mathematicians.

   We have also found that formalizing theorems in Lean gets harder as one gets to more advanced
material. Indeed, introductory textbooks usually contain all of the details, and a natural path to
formalize the material would be to follow the textbook. However, research papers are far from
self-contained and usually rely on dozens of external inputs, so this blueprint completely breaks
down. Moreover, a nice way to double check that a theorem is correctly formalized is to make
sure that it is useful, i.e., when you invoke it as an ingredient in a later proof, it actually serves
its purpose. However, research papers often contain results that are not repeatedly used, so this
method of double checking breaks down. For this and many other reasons (e.g., incorrect references
as mentioned above) partial formalizations can also be misleading.

   The above paragraph once again highlights why we have decided to build trusted libraries, as
discussed in Section 3.5. We believe that reasonable code quality and excellent organization will
be necessary for our community to efficiently verify deep theories and, more importantly, to be
able to quickly check that the verification is correct. Building such libraries will require large scale
communication, and we believe that this is an aspect where our community approach will shine.

  Finally, we mention that the desire to formally verify an important and technically delicate
theorem need not be specific to LLM-influenced mathematics. When proposing the Liquid Tensor
Experiment [23], Scholze explained his motivation as wanting to be sure that one of his most
important theorems to date was undoubtedly correct.
3.8. Our experiences using LLMs as a research assistant. In the following, we highlight
experiences collected from feedback from students3 of PT on several ongoing research projects in
Banach lattice theory, vector lattices, free constructions, and the homological properties of Banach
lattices. They show a consistent pattern: LLMs were often useful as mathematical assistants in the
early and intermediate stages of research to propose examples, suggest proofs, identify plausible
characterizations, and in some cases produce complete arguments. However, their output required
systematic verification. Some of the most useful contributions came with incomplete or incorrect
proofs, and several failures were caused by the model relying on false general principles that sounded
plausible in the surrounding mathematical context.

   We begin with a work in progress on free dual Banach lattices. For Banach spaces, the bidual
behaves naturally as a free object in the category of dual Banach spaces with adjoint (equiva-
lently weak∗ -to-weak∗ continuous) operators. In the setting of Banach lattices, the corresponding
question is subtler, since lattice homomorphisms are not stable under taking adjoints. Indeed,
  3This information was collected before the release of the most recent models, which have improved in many aspects.
12          J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


the adjoint of a lattice homomorphism is generally an interval preserving operator rather than a
lattice homomorphism. This led to the problem of determining the Banach lattices which admit
a free object in the category of dual Banach lattices with adjoint lattice homomorphisms, and in
particular of characterizing when the bidual of the free Banach lattice has this universal property.
In this case, the LLM produced a complete and understandable solution after only a small number
of iterations. The result is now part of an ongoing project of A. Avilés, E. Garcı́a-Sánchez, and
G. Martı́nez-Cervantes, building on earlier work on free dual spaces and free Banach lattices [9].

   A related success arose while studying weak∗ closed sublattices generated by sets. If A is a subset
of the dual of a Banach lattice, one may consider the operation
                                                          w∗
                                          A 7−→ lat(A)          .
Since lattice operations need not be weak∗ continuous, the weak∗ closure of a sublattice need not
itself be a sublattice. Previously, examples had been constructed for scattered compact spaces K
and subsets A ⊆ C(K)∗ such that
                                                          w∗
                                           Z1 = lat(A)
is not a sublattice, while
                                                           w∗
                                           Z2 = lat(Z1 )
is already a weak∗ closed sublattice. The open question was how many iterations of this combined
operation might be necessary before stabilization. The LLM first produced an example, based
on the same underlying ideas, requiring three iterations rather than two. It then suggested a
mechanism that appears capable of producing examples requiring an arbitrary ordinal number of
steps before stabilization. The details of this construction are still being developed by the authors,
but the model’s contribution was valuable because it pointed to a broader transfinite phenomenon
rather than merely solving a single finite case.

   Another substantial group of contributions concerned free products and push-outs of vector
lattices, Archimedean vector lattices, and Banach lattices. In an ongoing project by G. Martı́nez-
Fernández and PT, the LLM helped formulate and prove several results about preservation of
injectivity in categorical constructions. For example, in a push-out square of vector lattices
                                                   S1
                                            XO 1        / PO
                                                           O
                                           T1              S2

                                            X0          / X2
                                                   T2

the model suggested a proof that if T2 is injective, then S1 is injective. The proof strategy replaces
the Hahn–Banach type argument from [3] with extension and contraction of prime ideals, followed
by a reduction to totally ordered vector spaces.

   The LLM also helped with a key injectivity statement for Banach lattice free products. If
T1 : C(K1 ) → X1 and T2 : C(K2 ) → X2 are injective lattice homomorphisms, then the induced
lattice homomorphism
                            T1 ∗T2 : C(K1 ) ∗ C(K2 ) −→ X1 ∗ X2
is injective. The suggested argument used the representation C(K1 )∗C(K2 ) ≃ C(K1 ∗K2 ) developed
in [17] but supplied the missing ingredient together with further structural consequences, including
the injectivity of the canonical map from the Archimedean vector lattice free product of a family of
Banach lattices into their Banach lattice free product, and the order density of X1 ∗AVL X2 inside
X1 ∗ X2 .
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS 13


   In the same circle of questions, the LLM was useful for generating examples and counterexamples.
It helped identify that the vector lattice free product of two Archimedean vector lattices need not
be Archimedean, even though free vector lattices themselves are Archimedean. The obstruction
was translated into a question about open polyhedral cone covers of closed cones in Rn ; the cases
where such covers fail yield non-Archimedean free products. These examples illustrate one of the
strongest uses of LLMs in this work: They are good at proposing concrete test cases, pushing
definitions through specific situations, and suggesting counterexamples when a statement is too
optimistic. This was particularly helpful in all of the cases mentioned above, as the questions being
pursued were rather “new” and the authors were still in the process of gaining intuition for them.
In particular, we emphasize that the models that we employed in this case study were much less
useful in shedding light on longstanding problems or on problems that we had been stuck on for a
long time.

   A further line of work involved homological properties of Banach lattices, especially extension
and splitting phenomena. In Banach space theory, triviality of exact sequences is closely related
to extension properties. In the category of Banach lattices, however, one must distinguish between
an extension property and a splitting property. For λ > 1, a Banach lattice E has the λ-extension
property if for every lattice isometric interval preserving embedding i : Y → X and every lattice
homomorphism T : Y → E, there is a lattice homomorphism S : X → E such that Si = T and
∥S∥ ≤ λ∥T ∥. On the other hand, E has the splitting property if every lattice isometric interval
preserving embedding i : E → X has image which is a projection band in X. The interval preserving
assumption ensures that the image is an ideal, allowing quotients to remain within the relevant
category.

   The LLM helped clarify that the extension property implies the splitting property, but not
conversely. It produced a correct proof that C[0, 1] does not have the extension property, while the
researchers already knew that C[0, 1] has the splitting property. More precisely, it generated an
example of a lattice homomorphism into C[0, 1] that cannot be extended. This argument was later
generalized by the authors to spaces C(K) where K contains non-trivial convergent sequences.

   The model also suggested useful characterizations. For the splitting property, it proposed the
criterion that a Banach lattice has the splitting property if and only if every truncation is internal.
The statement turned out to be correct, although the proof supplied by the LLM had substantial
gaps. The final proof was written independently and was simpler than the model’s version. For the
extension property, the researchers asked whether monotone completeness implied the extension
property and suspected that the converse might fail. The model instead answered that no coun-
terexample should exist, because the two properties are equivalent. This statement was correct,
although again the proof supplied by the model was not. The researchers eventually proved the
equivalence using some of the ideas suggested by the model. These results form part of an advanced
work in progress [5].

   In the above case study, one recurring issue was that the LLM would tend to use false facts that
are close to true statements in the surrounding theory. For instance, in the work involving weak∗
convergence, it repeatedly asserted that every weak∗ convergent net in the dual of a Banach space
is norm bounded, invoking the uniform boundedness principle. This is clearly false, as there are
weak∗ convergent nets in dual spaces that are unbounded in norm. The mistake is particularly
dangerous because the analogous statement for sequences, or for pointwise bounded families under
the hypotheses of uniform boundedness, can make the argument superficially plausible.

 Another repeated failure concerned AM-spaces (spaces which satisfy ∥|f |∨|g|∥ = ∥f ∥∨∥g∥). The
model repeatedly used the false assertion that every AM-space is isomorphic, as a Banach space or
14          J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


as a lattice, to a space C(K). This occurred in the study of the splitting property for AM-spaces.
Other recurrent mistakes followed the same pattern. In the study of vector lattices, the model
often tried to use lattice homomorphisms into R in situations where such homomorphisms need not
exist. A further issue we find important to mention was incomplete citation: On many occasions,
the arguments proposed by the model can be identified with known facts, but the proper source
and authorship were entirely omitted. In addition, the model sometimes invoked results from the
literature while omitting essential hypotheses. These errors are beyond merely bibliographic, as
omitting a hypothesis can invalidate an entire proof.

   Overall, these experiences suggest that LLMs in this context are most reliable when used as
engines for mathematical exploration rather than as final authorities. They can quickly generate
proof strategies, test examples, identify alternative formulations, and suggest plausible character-
izations. They can also sustain long searches that would be tedious to perform manually. At the
same time, every AI-generated argument needs to be checked line by line, or better yet in Lean.
The failures show that the large language models used above may repeatedly import false general
facts, blur distinctions between nearby categories, and cite theorems without their full hypothe-
ses. Used critically, however, they functioned as productive research assistants that accelerated the
generation of ideas and uncovered results that have now become part of ongoing research papers.



                                        4. Our community
   As mentioned above, it was important to us that this was a community project. Indeed, the
past few months have seen a tremendous increase in the number of quality interactions between
members of our group. It was also important for us to give many talks and to build tutorials
that could potentially benefit other interested members of the Positivity, Functional Analysis and
Applied Harmonic Analysis communities. The interactions over the past few months were facilitated
by numerous group chats, weekly online meetings and in-person interactions. In particular, MT
is grateful to J. Serra who funded his travel during this period and allowed for vital in-person
interactions with various members of the group.

   A primary goal of this project was to benefit students. At the beginning of the project, we insisted
that students complete any projects that did not involve AI, so that they could receive full credit
for their excellent contributions. Moreover, in the papers where they did use AI, we asked them to
carefully disclose the process, identify what is their contribution, verbally explain the arguments
to us, and maintain an extremely high standard of quality. Otherwise, we let them explore on their
own. Although the sample size is small, we found that students adapted more quickly to the new
technology than senior members and had some of the best attitudes of all members of the group.
This can be clearly seen by the progress shown in Section 3.8, which hints that properly mentored
students can learn faster, strive for higher standards, and achieve deeper understanding than ever
before.

   Large scale communication and organization was also a very important aspect of our group’s
success. In particular, it was vital to respect people’s ideas, give people space to attack their
problems, and to keep morale high. It was also important for students to investigate problems that
they cared about (rather than just collecting random problems an LLM happened to know how to
solve) and to publish results that they are proud of. Although organizing such a large group during
a time of change was not easy, in general it brought the community closer.

  Finally, we remark on the adoption of Lean into our mathematical workflows. For the most part,
the community has shown a lot of enthusiasm for formalizing their results, although some members
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS 15


have not yet been convinced that this is important. The main roadblock is the high entry point4.
For this reason, we have spent a lot of time teaching, and also tried to present the Lean statements
in our papers in a way that was easier for mathematicians to digest rather than optimized for
coding.5 In our small sample size, we have noticed that those using Lean experienced an increase
in morale and creativity. Indeed, reading pages of LLM text can be exhausting, and it is much
nicer to share a result with colleagues that you know is correct. Similarly, exploring out-of-the-box
ideas becomes easier when you have multiple ways to later verify correctness.

  We also note that we have a wonderful group of Bachelor’s students at ETH Zürich who took
JD’s class on Lean and have been developing new insights on AI-assisted formalization under the
guidance of S. Bertolini and J. Serra. Their enthusiasm has been palpable, and we have been
extremely lucky to benefit from their numerous insights.


                                           5. Future endeavors
  Since it is impossible to predict the future, here we will focus on the concrete plans that we
have already committed to. Our first objective is to increase communication. We have already
been asked to give numerous talks, workshops, and minicourses on AI for math. In addition, we
will organize our own conference on AI for analysis at IMPA in early 2027, and DML will give
a Lean minicourse at our conference on phase retrieval in September 2026 https://www.mathc.
rwth-aachen.de/phaseretrieval/. JD will also give a course on formalization at NYU in Fall
2026 which will bring together graduate students from Mathematics, Computer Science and Data
Science, and MT has proposed dissertations on formalization in analysis for up to four students at
Oxford University.

   In addition to the above, we are also in the process of improving organization. This includes
not only organization at the personal level but also in designing new infrastructure to organize
relevant results and partial progress. As we have seen, one strength that LLMs have is that they
can invoke facts from all over mathematics. In general, the literature is poorly organized, as we have
traditionally rewarded advancing the forefront of knowledge much more than we have collecting,
digesting, and properly presenting known mathematics. However, with AI tools, better organization
is possible and canonizing mathematical knowledge into usable databases and Lean libraries seems
both doable at scale and fundamentally important.

   Otherwise, we wish to further develop our field and expand our scientific knowledge. As men-
tioned above, it is not uncommon for LLMs to solve a problem by invoking a fact that you did
not know. This then forces you to expand your mathematical horizons and learn new fields. In
the course of using LLMs, we have also needed to take on many jobs which are atypical for math-
ematicians. Indeed, many of the difficulties we have overcome can be better classified as software
engineering problems. Moreover, in our research, we have for the first time used tools such as
interval arithmetic to certify a proof, and we expect that using large scale numerics will become
common for testing hypotheses. Thus, we expect our mathematical lives to blend somewhat with
computer science and engineering and have a more direct impact on the other sciences. More con-
cretely, we have never had more confidence that we may be able to help answer real world problems
in phase retrieval and related areas, such as the dynamic range problem. In particular, we hope
that the discussions with physicists and engineers at our conference in September will stimulate
new multi-disciplinary collaborations.

  4Though this has been decreasing with time.
  5We did not do this in the library, of course.
16            J. DE DIOS PONT, L. LIEHR, D. MUÑOZ-LAHOZ, M. A. TAYLOR, AND P. TRADACETE


   Finally, we think it is important to emphasize that LLMs are only becoming good at mathematics
because they have been trained on mathematics. This, once again, proves that the enormous body
of research produced by mathematicians is not only a beautiful example of human ingenuity, but
is fundamentally useful. In particular, mathematics is – and always will be – the language of the
universe. With the recent developments in AI, we now have a better way to harness this knowledge,
and our objective for the future is best summarized as the desire to use these tools to advance our
understanding of mathematics and its implications on the rest of the world.

                                            6. Acknowledgments
  We thank Alessio Figalli and Joaquim Serra for encouraging us to write this note. We also thank
Javier Gomez-Serrano for mentorship and advice as well as several participants at the National
Academy of Sciences event Organizing Mathematical Knowledge in the Age of AI and Formalization,
July 20-21 2026 and the International Congress of Mathematicians, July 23-30 2026 for sharing their
comments. Finally, we wish to thank various members of the Banach lattice and phase retrieval
communities, including Rima Alaifari, Antonio Avilés, Susanna Bertolini, Eugene Bilokopytov,
Avik Das, Ingrid Daubechies, Dan Freeman, Enrique Garcı́a-Sánchez, Josef Greilhuber, David de
Hevia, Jorge S. Ibáñez-Marcos, Jesús Illescas, Philippe Jaming, Denny Leung, Gonzalo Martı́nez-
Fernández, Timur Oikhberg, Ben Pineau, João Ramos, Christian Rosendal, Alberto Salguero-
Alarcón, Alexander Schell, Nazaret Trejo-Arroyo, Vladimir Troitsky and Matthias Wellershoff for
the numerous discussions that have influenced the perspectives that we have shared here.

  In thanking all of these people, we do not wish to imply that incorporating technology into our
mathematical lives has been emphatically desired by all. Change is almost always coupled with
uncertainty, and how one adapts to change is a very personal choice. This note only serves to
explain what has worked for our community. With this in mind, we are exceptionally grateful to
the people mentioned above for the many years of friendship and collaboration, which, in turn,
made their suggestions and input over the last few months even more valuable.

   The authors declare that they did not use any AI tools when writing this article. The AI models
used over the last several months to gather the above experiences were Claude Opus 4.6, 4.7 and
4.8, a small amount of Fable 5, and GPT 5.4 and 5.5. We emphasize that the views and practices
described in this paper are not static and will certainly change over time as the models improve.

                                                  References
 [1] Pedro Abdalla, Jaume de Dios Pont, João P. G. Ramos, and Mitchell A. Taylor. Stable Phase Retrieval for Spans
     of Independent Random Variables. arXiv preprint arXiv:2607.06693, 2026.
 [2] Jeremy Avigad. Mathematicians in the Age of AI. arXiv preprint arXiv:2603.03684, 2026.
 [3] Antonio Avilés and Pedro Tradacete. Amalgamation and injectivity in Banach lattices. Int. Math. Res. Not.,
     2023(2):956–997, 2023.
 [4] Susanna Bertolini, Jaume de Dios Pont, Ben Pineau, Mitchell A. Taylor, and João P. G. Ramos. L2 -Stability
     for STFT phase retrieval. arXiv preprint arXiv:2605.20527, 2026.
 [5] E. Bilokopytov, A. Salguero-Alarcón, P. Tradacete, and N. Trejo-Arroyo. Splitting and extension properties in
     Banach lattices. Work in progress.
 [6] Kevin Buzzard, Johan Commelin, and Patrick Massot. Formalising perfectoid spaces. In Proceedings of the 9th
     ACM SIGPLAN International Conference on Certified Programs and Proofs, pages 299–312, 2020.
 [7] Alex Davies, Petar Veličković, Lars Buesing, Sam Blackwell, Daniel Zheng, Nenad Tomašev, Richard Tanburn,
     Peter Battaglia, Charles Blundell, András Juhász, et al. Advancing mathematics by guiding human intuition
     with ai. Nature, 600(7887):70–74, 2021.
 [8] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language. In Au-
     tomated Deduction – CADE 28: 28th International Conference on Automated Deduction, Virtual Event, July
     12–15, 2021, Proceedings, page 625–635, Berlin, Heidelberg, 2021. Springer-Verlag.
 [9] E. Garcı́a-Sánchez and P. Tradacete. Free dual spaces and free Banach lattices. J. Math. Anal. Appl., 532(2):22,
     2024. Id/No 127931.
   BANACH LATTICES AND PHASE RETRIEVAL: A CASE STUDY FOR THE USE OF AI IN MATHEMATICS 17


[10] Vasily Ilin and Brian Nugent. Sorries Are Not the Hard Part: An Expert-Review Case Study of a Semi-
     Autonomous Formalization. arXiv preprint arXiv:2606.13925, 2026.
[11] David Jerison and Nikolai Nadirashvili. The “hot spots” conjecture for domains with two axes of symmetry.
     Journal of the American Mathematical Society, 13(4):741–772, 2000.
[12] Eric Jiang, Xiao Liang, Yikai Zhang, Yingjia Wan, Mengting Li, Haikang Deng, Alexander K. Taylor, Justin
     Baker, Rushil Raghavan, Junyi Zhang, Ying Nian Wu, Andrea L. Bertozzi, Kai-Wei Chang, Raghu Meka,
     Matthew Sottile, Nanyun Peng, Amit Sahai, Terence Tao, and Wei Wang. From solvers to research: Large
     language model-driven formal mathematics at the research frontier. arXiv preprint arXiv:2607.07779, 2026.
[13] Tanya Klowden and Terence Tao. Mathematical methods and human thought in the age of AI. arXiv preprint
     arXiv:2603.26524, 2026.
[14] Lukas Liehr, Jaume de Dios Pont, and Mitchell A. Taylor. Cantor measures with odd base do not admit Fourier
     frames. arXiv preprint arXiv:2607.08656, 2026.
[15] Lukas Liehr, Jaume de Dios Pont, and Mitchell A. Taylor. On the existence problem of regular Gabor frames.
     arXiv preprint arXiv:2606.26052, 2026.
[16] Phanuel Mariano, Hugo Panzo, and Jing Wang. Improved upper bounds for the Hot Spots constant of Lipschitz
     domains. Potential Analysis, 59(2):771–787, 2023.
[17] Gonzalo Martı́nez-Fernández and Pedro Tradacete. Free Products of Banach Lattices. arXiv preprint
     arXiv:2605.28988, 2026.
[18] David Muñoz-Lahoz. Autoformalize your math. https://lean.functionalanalysismadrid.com/.
[19] David Muñoz-Lahoz. The Banach lattice Lean library. 2026.
[20] Timur Oikhberg, Mitchell A. Taylor, Pedro Tradacete, and Vladimir G. Troitsky. Free Banach lattices. J. Eur.
     Math. Soc. (JEMS), 28(10):4387–4514, 2026.
[21] Jaume de Dios Pont, Alexander W Hsu, and Mitchell A Taylor. Sharp bounds on the failure of the hot spots
     conjecture. arXiv preprint arXiv:2508.16321, 2025.
[22] Ahmad Rammal, Niket Patel, Fabian Gloeckle, Amaury Hayat, Julia Kempe, Remi Munos, Charles Arnal, and
     Vivien Cabannes. Formalizing mathematics at scale. arXiv preprint arXiv:2605.29955, 2026.
[23] Peter Scholze. Liquid tensor experiment. Experimental Mathematics, 31(2):349–354, 2022.
[24] Stefan Steinerberger. An upper bound on the hot spots constant. Revista Mathematica Iberoamericana, 39(4),
     2023.
[25] Terence Tao. Machine-assisted proof. Notices of the American Mathematical Society, 72(1):6–13, 2025.
[26] Terence Tao. The integrated explicit analytic number theory network : a progress report. Conference talk at
     Techniques and Tools for the Formalization of Analysis, Institute for Computational and Experimental Research
     in Mathematics (ICERM), 2026.
[27] The mathlib Community. The Lean Mathematical Library. In Proceedings of the 9th ACM SIGPLAN Interna-
     tional Conference on Certified Programs and Proofs, CPP 2020, New Orleans, LA, USA, January 2020. ACM.
[28] William P Thurston. On proof and progress in mathematics. In 18 Unconventional essays on the nature of
     mathematics, pages 37–55. Springer, 2006.

  Center for Data Science, New York University, New York, New York 10011, USA
  Email address: jdedios@nyu.edu

  Department of Mathematics, Bar-Ilan University, Ramat-Gan 5290002, Israel
  Email address: lukas.liehr@biu.ac.il

  Instituto de Ciencias Matemáticas. Universidad Autónoma de Madrid, Campus de Cantoblanco
UAM 28049 Madrid, Spain
  Email address: david.munnozl@uam.es

  Department of Mathematics, ETH Zürich, Ramistrasse 101, 8092 Zürich, Switzerland
  Email address: mitchell.taylor@math.ethz.ch

  Instituto de Ciencias Matemáticas (CSIC-UAM-UC3M-UCM), Consejo Superior de Investigaciones
Cientı́ficas, C/ Nicolás Cabrera, 13–15, Campus de Cantoblanco UAM, 28049 Madrid, Spain.
  Email address: pedro.tradacete@icmat.es
