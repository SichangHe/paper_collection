                                          Gödel Test: Can Large Language Models Solve Easy Conjectures?
                                                                    Moran Feldman                           Amin Karbasi
                                                                   University of Haifa                   Cisco Foundation AI
                                                                moranfe@cs.haifa.ac.il                   karbasi@cisco.com


                                                                                            Abstract
arXiv:2509.18383v1 [cs.AI] 22 Sep 2025




                                                     Recent announcements from frontier AI model labs have highlighted strong results on high-
                                                 school and undergraduate math competitions. Yet it remains unclear whether large language
                                                 models can solve new, simple conjectures in more advanced areas of mathematics. We propose
                                                 the Gödel Test: evaluating whether a model can produce correct proofs for very simple,
                                                 previously unsolved conjectures. To this end, we study the performance of GPT-5 on five
                                                 conjectures in combinatorial optimization. For each problem, we provided one or two source
                                                 papers from which the conjecture arose, withheld our own conjecture, and then assessed the
                                                 model’s reasoning in detail. On the three easier problems, GPT-5 produced nearly correct
                                                 solutions; for Problem 2 it even derived a different approximation guarantee that, upon checking,
                                                 refuted our conjecture while providing a valid solution. The model failed on Problem 4, which
                                                 required combining results from two papers. On Problem 5, a harder case without a validated
                                                 conjecture, GPT-5 proposed the same algorithm we had in mind but failed in the analysis,
                                                 suggesting the proof is more challenging than expected. Although our sample is small, the
                                                 results point to meaningful progress on routine reasoning, occasional flashes of originality, and
                                                 clear limitations when cross-paper synthesis is required. GPT-5 may represent an early step
                                                 toward frontier models eventually passing the Gödel Test.


                                         Introduction
                                         Based on his experience working with OpenAI’s o1 models, Terence Tao offered the following
                                         impression:1

                                                 “The new model could work its way to a correct (and well-written) solution if provided a
                                                 lot of hints and prodding, but did not generate the key conceptual ideas on its own, and
                                                 did make some non-trivial mistakes. The experience seemed roughly on par with trying
                                                 to advise a mediocre, but not completely incompetent, graduate student. However, this
                                                 was an improvement over previous models, whose capability was closer to an actually
                                                 incompetent graduate student. It may only take one or two further iterations of improved
                                                 capability (and integration with other tools, such as computer algebra packages and proof
                                                 assistants) until the level of ‘competent graduate student’ is reached.”
                                                 — Terence Tao

                                             In this report, we examine to what extent GPT-5 is capable of proving simple conjectures. Both
                                         OpenAI and Google have claimed that their frontier models, without external tools, can achieve
                                         gold-medal performance on the International Mathematical Olympiad (IMO). While IMO problems
                                         are undoubtedly challenging, they are designed for exceptionally bright high school students.
                                           1
                                               See Tao’s Mastodon posts from Sept. 2024, https://mathstodon.xyz/@tao/113132504933420227



                                                                                                1
    Here, our focus is different: we ask whether large language models can also handle new con-
jectures in more advanced mathematical domains, where success requires not only problem-solving
ability, but also mathematical maturity and background knowledge. We frame this challenge as
the Gödel Test: evaluating whether an AI system can prove very easy conjectures that are simple
for humans with appropriate training, yet novel enough not to be directly available from existing
sources.2
    To explore this challenge, we designed a set of conjectures from our own line of work, namely
submodular maximization, a subfield of combinatorial mathematics with many applications in AI.
This choice provides a natural testing ground: the problems are concrete, well-motivated, and
deliberately chosen to lie within reach of a system aiming to display mathematical reasoning.
Unlike the above-mentioned experiments conducted by Terence Tao, we did not provide extensive
hints or guidance about what we believed the solutions might be. Instead, we gave only a minimal
description of each problem, together with one or two source papers that inspire the conjecture. We
then allowed the large language model to interpret the problem and attempt to produce a solution
on its own.
    In terms of difficulty, our plan was to formulate conjectures simple enough that a strong un-
dergraduate or graduate student in theoretical computer science or a related area of applied math-
ematics could reasonably be expected to solve them all (within a day). We also ensured that, for
most problems, there were clear conjectures and known approaches for resolving them if needed.3
This is true for the first four problems. We initially believed the 5th problem, though somewhat
harder, would also be easily solvable. However, after experimenting with GPT-5, we came to realize
that it is more challenging than we had anticipated. Our high-level idea, which was also suggested
by GPT-5 but incorrectly proven, may not suffice, and at present we do not have a clear conjecture
for Problem 5. As a result, it remains open-ended and still awaits a human (or an AI generated)
solution.

Related Efforts. Very recently, right after GPT-5 was released, Sebastian Bubeck reported via
an X post4 that GPT-5 solved an open problem in convex optimization by improving a known
bound from 1/L to 1.5/L. Motivated by this example, Diez, da Maia, and Nourdin [6] studied
GPT-5’s ability to provide explicit convergence rates within the Malliavin–Stein framework for
central limit theorems, focusing on Gaussian and Poisson settings. Both of these efforts point to
similar conclusions: GPT-5 was able to make progress on well-posed mathematical problems, but
its reasoning often remains limited and requires careful human verification [6]. In contrast to [6],
we did not guide the model interactively toward the correct solution (which is a very reasonable
approach). Instead, we only posed the question and provided one or two related papers, leaving
the model to interpret the problem and attempt a solution on its own.

Limitations. Our study has several limitations. First, we examined only five conjectures. Eval-
uating correctness requires carefully checking each proof attempt, which makes the process highly
time-consuming. Drawing more definitive conclusions would require a much larger sample size.
Second, we tested only GPT-5. For the same reason, i.e., verifying solutions is labor-intensive,
we did not extend our experiments to other frontier models. While we might expect comparable
performance from peers, we cannot make claims without direct evaluation. Third, although we
  2
     We acknowledge that this definition is somewhat vague and depends on subjective judgments, both about what
qualifies as “simple” for humans and what counts as “directly available” in existing literature.
   3
     However, we intentionally refrained from offering the model any hints or possible lines of attack.
   4
     See https://x.com/SebastienBubeck/status/1958198661139009862. An increasing amount of AI research
seems to be first discussed on X.


                                                      2
made a strong effort to design original conjectures within our domain of expertise, ensuring that
they were both simple enough to be approachable and somewhat novel to be nontrivial, this is not
an easy task. We cannot guarantee that none of the conjectures have appeared in the literature;
we only tried our best to avoid overlap.5

Take-home messages.           From our experiments, several insights stand out:

       • GPT-5 performed well when a single, straightforward path of reasoning was sufficient, pro-
         ducing nearly correct proofs in three out of five cases.

       • For Problem 2, it even derived a different approximation guarantee that, upon checking,
         refuted our original conjecture while providing a valid solution.

       • Its adaptation of known proofs was often adequate, but somewhat superficial: the model
         tended to skip over unchanged steps and closely mirrored the original structure rather than
         pursuing more natural alternatives. This pattern resembles how humans might minimize
         effort by avoiding redundant steps.

       • The model was unsuccessful on Problems 4 and 5, both of which required combining insights
         across proof techniques. Developing such integrative reasoning seems to be a major limitation.

       • On Problem 5, GPT-5 identified the same algorithm we had in mind, but was unable to
         analyze it correctly. Our own review suggested that proving a meaningful guarantee may be
         possible, but it appears more difficult than we initially anticipated.

       • Relative to earlier model generations, GPT-5 shows clear gains in baseline mathematical com-
         petence, at least within the specialized domain of combinatorial optimization, and occasional
         sparks of originality. These trends give reason for cautious optimism that future models may
         acquire the ability to connect proof techniques in a more systematic way.

       • Prompting can have a substantial effect on performance. For instance, when asked to provide a
         full proof, GPT-5 tends to include more intermediate steps instead of skipping them, leading
         to solutions that are more complete and self-contained. We expect that improved prompt
         design could have a major impact on both the quality and correctness of the results.

       • The incorrect proofs on Problems 4 and 5 initially appeared plausible and even convincing.
         Only after a detailed examination did it become clear that they contained deep flaws. This
         highlights a central limitation, and maybe potential danger, of frontier models in mathemat-
         ical reasoning: outputs can look correct on the surface while being fundamentally wrong.

Disclaimer. This report is based on a limited set of interactions with GPT-5. The claims pre-
sented here are context-dependent and should not be interpreted as definitive or generalizable
beyond the specific experiments we conducted. Our goal is to provide an initial perspective on the
mathematical reasoning abilities of frontier models, and in particular GPT-5. We make no guaran-
tees about the completeness of the claims, and caution that they should not be taken out of context.
We can only hope that these observations may serve as a starting point for the broader scientific
   5
    One of the authors recalls attending an information theory conference around 2010 where a presenter offered a
solution to a cute conjecture, only to be interrupted by a senior member who remarked that the problem had already
been solved by Russian mathematicians in the 60s. The presenter calmly replied, “I would have been surprised if it
wasn’t,” and continued the talk.



                                                        3
community to propose new conjectures, examine them in greater depth, and collectively advance
progress toward the longer-term aspiration of developing models capable of passing the Gödel Test.
Finally, the views expressed are solely our own, and do not represent the official positions of our
institutions or employers.


Overview on Submodular Maximization
In the following few paragraphs, we give a short informal overview on the field of submodular
maximization. The goal of this overview is to help the reader understand (on a high level) the
descriptions given in the next sections for the conjectures that we have have designed.
    Given a ground set N of elements, a set function f is a function that assigns a numerical value
to every subset S of N . One can intuitively think of f (S) as the value of the elements in the set S,
or the amount one is willing to pay for these elements in an auction. Sometimes each element in N
has a value that does not depend
                               P on the other elements it comes with. Formally, this means that
the function f obeys f (S) = u∈S f ({u}) for every set S of elements. Such functions f are called
modular functions. In general, however, the function f might have a much more involved structure
exhibiting both complementarity and substitution. Elements exhibit complementarity if they are
worth together more than separately. For example, a left shoe alone and a right shoe alone both
have little value, but they have a much higher value together. Elements exhibit substitution if their
worth together is smaller than the sum of their individual values. For example, a computer and a
tablet exhibit substitution as they have many overlapping uses.
    It turns out that set functions that exhibit no complementarity are quite common in diverse
fields such as combinatorial optimization, machine learning and game theory. Such functions are
called submodular functions. Formally, a set function f is submodular if it obeys f (A) + f (B) ≥
f (A ∪ B) + f (A ∩ B) for every two sets A and B. There are also classes of continuous functions
that are analogous to the class of submodular set functions. Among these, we sometimes refer in
our conjectures to the class of DR-submodular functions.
    In a submodular maximization problem, the goal is to maximize a set function f subject to a
constraint C. The function f is usually assumed to be submodular, and it can also be assumed
to have additional properties such as monotonicity (i.e., if a set A contains a set B, than f (A) ≥
f (B)). Sometimes the assumption of submodularity is replaced with a weaker one. One popular
such weakened assumption is known as γ-weak submodularity. Here, γ ∈ [0, 1] is a parameter
controlling the extent to which the assumption of submodularity is weakened: γ = 1 corresponds
to the standard (unweakened) submodularity assumption, while γ = 0 allows for any set function.
Similarly, the assumptions on the constraint C also vary from problem to problem. Often the
constraint C is just a cardinality constraint (i.e., any set whose size is smaller than some given
value is allowed), but in other cases more involved types of constraints are assumed.


1       Maximizing Monotone Plus Non-monotone Submodular Func-
        tions over a Convex Set Constraint
Our first conjecture studies the maximization of a function expressed as the sum of a monotone
DR-submodular function and a non-monotone DR-submodular function over a constraint given
by a down-closed convex set P ⊆ [0, 1]n .6 Guarantees for this problem are specified using two
    6
    The down-closedness of P means that if x ∈ P and y is a vector in [0, 1]n that is coordinate-wise dominated by
x, then y also belongs to P .



                                                        4
parameters α and β measuring the quality of the approximation guarantee with respect to each
component of the objective function. We have attached to the prompt of this conjecture the paper
[8], which studies similar optimization problems in which the objective function is expressed as the
sum of a concave function with either a monotone or a non-monotone DR-submodular function.

  Prompt to GPT-5

  Consider the problem of maximizing a function F from [0, 1]n to the reals that is the sum
  of a non-negative monotonically increasing DR-submodular function G and a non-negative
  DR-submodular function H over a solvable down-closed polytope P . I would like to bound
  the performance on this problem from the NeurIPS 2021 paper ”Submodular + Concave”
  which is attached. Specifically, if x is the output vector of this algorithm and o is the vector
  in P maximizing F , then I would like to lower bound F (x) with an expression of the form
  α ∗ G(o) + β ∗ H(o) − err, where α and β are constants. err should be a function that depends
  only on the error parameter ϵ of the algorithm, the diameter D of the polytope P , and the
  smoothness parameters LG and LH of G and H, respectively, and goes to zero as ϵ goes to zero.
  Please give the best such bound that you prove (a bound is considered better if the values of
  the constants α and β are larger). Provide a mathematically rigorous and well explained proof
  for the bound you come up with.


Note. The problem is described in terms of DR-submodular functions instead of submodular set
functions to avoid the need to refer to continuous relaxations of discrete submodular optimization
problems and rounding procedures for such relaxations.

Conjecture. We believe that a variant of the Frank-Wolfe-like algorithm of [1] can guarantee
α = 1 − 1/e and β = 1/e. This value of α is provably the best that can be obtained. It is possible
to get better values of β [2], but this requires more involved algorithms, and it is unclear if it can
be done without deteriorating the value of α.
    We asked GPT-5 to write its proof in .tex format. The following is the response.7

  Response of GPT-5 (thought for 2m 49s)

  Here is a clean way to get exactly the kind of “split guarantee” you asked for when

                                F (x) = G(x) + H(x),       x ∈ P ⊆ [0, 1]n ,

  with P a solvable down-closed polytope, G non-negative, monotone and DR-submodular, and H
  non-negative and DR-submodular (not necessarily monotone). I’ll run essentially the Measured
  Greedy Frank-Wolfe (MGFW) algorithm from the paper and adapt its proof so that the DR-
  submodular second part H replaces the concave part in the original analysis. I state the bound
  first, then give a rigorous proof.
  Let G, H be LG - and LH -smooth, respectively, and let D := maxx∈P ∥x∥2 . Run Measured
  Greedy Frank–Wolfe (MGFW) on F = G + H with stepsize parameter ε ∈ (0, 1). Denote by x

  7
    When we asked GPT-5 to put the exact proof into a .tex file, it does not reproduce the proof exactly as it
appeared in the chat. The mathematical content remains the same, but a few words and sentences are slightly
rephrased. Nothing changes dramatically, yet the text is not a verbatim copy.




                                                      5
its output and by o ∈ P an optimizer of F . Then

                       F (x) ≥ α G(o) + β H(o) − ε (LG + LH ) D2 ,
                                                 |      {z     }
                                                          =: err(ε,D,LG ,LH )

where
   • α = 1 − 1e ,
         (
           1 − 1e , if H is monotone;
   • β= 1
           e,       if H may be non-monotone.
In particular, when both G and H are monotone DR-submodular, you get

                   F (x) ≥ (1 − 1e ) G(o) + (1 − 1e ) H(o) − ε(LG + LH )D2 .


Proof
We give a self-contained proof using the MGFW update and DR-submodularity on both com-
ponents.

Preliminaries and notation. Let P ⊆ [0, 1]n be a nonempty down-closed polytope ad-
mitting a linear optimization oracle. A differentiable f : [0, 1]n → R is DR-submodular if
for all x ≤ y (coordinatewise) we have ∇f (y) ≤ ∇f (x) (coordinatewise). Assume G, H ≥ 0
are DR-submodular, G is monotone, and let LG , LH ≥ 0 denote their smoothness constants:
∥∇G(x) − ∇G(y)∥2 ≤ LG ∥x − y∥2 and similarly for H. Set F := G + H and LF := LG + LH ,
and let D := maxx∈P ∥x∥2 .

Measured Greedy Frank–Wolfe (MGFW).                    Fix ε ∈ (0, 1), initialize y0 := 0, and for
i = 0, 1, . . . , T − 1 with T := ε−1 do

                              si ∈ arg max ⟨(1 − yi ) ⊙ ∇F (yi ), x⟩,
                                        x∈P
                            yi+1 := yi + ε (1 − yi ) ⊙ si .

Down-closedness implies yi ∈ P for all i, and 0 ≤ yi ≤ 1 − (1 − ε)i 1 by the standard mask
bound.

Step 1: One-step progress.       By LF -smoothness and the choice of si ,

              F (yi+1 ) − F (yi ) ≥ ε ⟨(1 − yi ) ⊙ ∇F (yi ), o⟩ − ε2 (LG + LH )D2 .            (1)

Let zi := o ⊙ (1 − yi ) + yi . For any DR-submodular f and any v ≥ 0, the antitonicity of ∇f
gives ⟨v, ∇f (y)⟩ ≥ f (y + v) − f (y). Apply this to G and to H with v = (1 − yi ) ⊙ o ≥ 0,
obtaining
                  ⟨(1 − yi ) ⊙ ∇F (yi ), o⟩ ≥ [G(zi ) − G(yi )] + [H(zi ) − H(yi )].
Plugging in (1),
                                                                    
        F (yi+1 ) − F (yi ) ≥ ε [G(zi ) − G(yi )] + [H(zi ) − H(yi )] − ε2 (LG + LH )D2 .      (2)


                                                 6
  Step 2: Relating G(zi ), H(zi ) to G(o), H(o). Define the monotonicity multipliers for any
  non-negative f by
              (
               1,        f monotone,
  M (f, i) :=         i
                                                    S(f, 0) := 0, S(f, i) := (1−ε)S(f, i−1)+ε M (f, i−1).
               (1 − ε) , f possibly non-monotone,

  A short induction yields
                                 (
                                  1 − (1 − ε)i , f monotone,
                       S(f, i) =
                                  iε(1 − ε)i−1 , f possibly non-monotone.

  Using DR-submodularity and nonnegativity one shows G(zi ) ≥ M (G, i) G(o), H(zi ) ≥
  M (H, i) H(o). Combining with (2) gives the recurrence
                                                                   
       F (yi+1 ) ≥ (1 − ε) F (yi ) + ε M (G, i) G(o) + M (H, i) H(o) − ε2 (LG + LH )D2 . (3)

  Step 3: Solving the recurrence.        We prove by induction that

                   F (yi ) ≥ S(G, i) G(o) + S(H, i) H(o) − i ε2 (LG + LH )D2 .

  The base i = 0 is trivial. The step follows from (3) and the identity (1−ε)S(f, i−1)+εM (f, i−
  1) = S(f, i). Setting i = T = ε−1 yields

                F (yT ) ≥ S(G, ε−1 ) G(o) + S(H, ε−1 ) H(o) − ε(LG + LH )D2 .
                          | {z }            | {z }
                              =: αε              =: βε


  With the closed forms above, αε = 1 − (1 − ε)1/ε and βε = 1 − (1 − ε)1/ε if H is monotone,
  while βε = (1 − ε)1/ε−1 in general. Since (1 − ε)1/ε ≤ e−1 , we obtain the universal constants
  α ≥ 1 − 1/e and β ≥ 1 − 1/e in the monotone case, or β ≥ 1/e in general.                    2


  Remarks
     • Tightness w.r.t. technique. Allowing H to be non-monotone naturally limits β to 1/e
       in MGFW/continuous-greedy style analyses under down-closed constraints, while G’s
       monotonicity permits α = 1 − 1/e.

     • Error term. Each step incurs at most ε2 (LG + LH )D2 , and there are 1/ε steps, hence
       the total error ε(LG + LH )D2 , which vanishes as ε → 0.


Our Evaluation of GPT-5’s Response
Despite claiming otherwise, GPT-5 did not provide a standalone algorithm and proof. Instead, it
only tried to explain how to adapt an existing proof of [8]. Overall, the adaptation is correct, but
is lazy in two senses. First, GPT-5 skips many parts of the proof that are unchanged compared
to [8]. Second, GPT-5 really tries to stay as close as possible to the proof of [8], even when this
is not the most natural thing to do. This laziness is similar to what a human would have done
to avoid writing too much text. In the following, we give some additional information about the


                                                 7
laziness of GPT-5 in the second sense as well as some minor inaccuracies in the proof.

        • GPT-5 refers to the “standard mask bound” just before Step 1. We are not aware of any
          bound known by this name, but the result that follows from this bound according to GPT-5
          is correct (and quite standard).

        • The inequality ⟨v, ∇f (y)⟩ ≥ f (y + v) − f (y) stated in Step 1 holds only when v ≤ 1 − y, but
          this is not mentioned by GPT-5, and furthermore, this condition is not checked when this
          inequality is used for v = (1 − yi ) ⊙ o.

        • GPT-5 attributes the lower bounds on G(zi ) and H(zi ) to the DR-submodularity and non-
          negativity of these functions. This is not accurate since the bound for G uses also the
          monotonicity of this function (it does not hold otherwise).

        • The Inequality (3) represents an unnecessary generalization. It would have been appropriate
          if both G and H could be either monotone or non-monotone, but since the prompt fixes G to
          be the monotone function and H to be the non-monotone function, the terms M (G, i) and
          M (H, i) could be easily replaced with their appropriate concrete expressions. Keeping the
          terms M (G, i) and M (H, i) unchanged can be viewed as a laziness on behalf of GPT-5, which
          tries to stick as much as possible to the proof of [8] to reduce the length of its answer, even
          at the cost of making the proof more general than what is necessary.

        • In the last sentence before the “Remarks” section, GPT-5 uses the inequality (1 − ε)1/ε ≤ e−1
          to justify the lower bounds on α and β. However, getting a lower bound on β in fact requires
          the slightly different inequality (1 − ε)(1/ε−1) ≥ e−1 .


2        Bicriteria Maximization of a Monotone Submodular Function
         subject to a p-System Constraint
Our second conjecture is about bicriteria algorithms for submodular maximization. Recently, the
paper [7] (mentioned in the prompt) has systematically studied such algorithms for many sub-
modular maximization problems. In particular, Feldman and Kuhnle [7] studied such problems
having a matroid constraint.8 In this conjecture, we asked for a bicriteria algorithm for maximizing
a monotone submodular function subject to another class of combinatorial constraint known as
p-systems. A p-system is equivalent to a matroid when the parameter p is set to 1, and it is strictly
more general for larger values of this parameter. We attached to the prompt of this conjecture both
the paper [7], and the paper [4] whose appendix studies non-bicriteria submodular optimization
subject to a p-system constraint.

    Prompt to GPT-5

    In our recent paper “Bicriteria Submodular Maximization” which is attached, we defined a
    notion of bicriteria optimization for submodular maximization problems. In the current prob-
    lem, given a non-negative monotone submodular function f : 2N → R≥0 and a p-system (N , I)
    over the same ground set, we want a bicriteria algorithm for finding a set S ∈ I that (ap-

    8
    Matroid constraints are a well-studied class of combinatorial constraints capturing, for example, a constraint that
allows only the selection of a linearly independent set of vectors out of a ground set consisting of vectors from some
linear space, or a constraint that allows only the selection of a non-cyclic set of edges out of a ground set consisting
of the edges of some graph.


                                                           8
 proximately) maximizes f among all such sets. The bicriteria approximation guarantee of the
 algorithm should be of the form (1 − ε, g(ε)), where g(ε) is as small as possible expression of ε.
 I also attached a good reference for a p-system.


Conjecture. The paper [7] showed that a simple greedy algorithm can guarantee (1−ε, ⌈log2 ε−1 ⌉)-
bicriteria approximation for any ε > 0 for the special case of the above problem in which the
p-system is a matroid (i.e., p = 1). The same algorithm should guarantee (1 − ε, ⌈logp+1 ε−1 ⌉)-
bicriteria approximation for general p-systems.

 Response of GPT-5 (thought for 2m 57s)

 Awesome—using your bicriteria framework and a standard p-system reference, here’s a clean
 algorithm with a tight-in-spirit guarantee.


 Result (monotone f over a p-system)
 Let f : 2N → R≥0 be monotone submodular and (N , I) a p-system (down-closed independence
                                                                                      1
 family with the “bases within any Y ” ratio at most p). Greedy on a p-system is a p+1  -
 approximation for single-pass maximization.

 Theorem (bicriteria for p-systems).
 There is a polynomial-time algorithm that, for any ε ∈ (0, 1), returns a set S ⊆ N with

                                      f (S) ≥ (1 − ε) · max f (T ),
                                                            T ∈I
                                         1S ≤ gp (ε) · y

 for some y ∈ P = conv{1I : I ∈ I}. Equivalently (since P is down-closed), 1S /gp (ε) ∈ P . In
 particular
                                        l ln(1/ε) m    l              m
                                                                    1
                               gp (ε) =             ≤    (p + 1) ln ε   .
                                          ln p+1
                                                 
                                              p
                        
 This is a 1 − ε, gp (ε) -bicriteria guarantee in your (α, β) sense (with y1 = 0, y2 = y).

 Algorithm (multi-pass greedy for p-systems)
 Set S0 ← ∅. For i = 1, 2, . . . , ℓ with ℓ = gp (ε):

    1. Run standard greedy for maximizing the marginal f (· | Si−1 ) over I: start from
       Ti ← ∅ and repeatedly add the feasible element of maximum marginal f (u | Si−1 ∪ Ti )
       while maintaining independence in I, until maximality.

    2. Set Si ← Si−1 ∪ Ti . Return S ← Sℓ .

 Feasibility (bicriteria) bound. Each Ti ∈ I is independent; S = ℓi=1 Ti is covered by ℓ
                                                                          S

 independent sets. Let y = 1ℓ ℓi=1 1Ti ∈ P . Then 1S ≤ ℓ · y, i.e., 1S /gp (ε) ∈ P . This matches
                               P
 your bicriteria definition with β = gp (ε).



                                                        9
Value bound.      For each round, greedy on a p-system gives (applied to the marginal function)

                        f (Si ) = f (Si−1 ) + f (Ti | Si−1 )
                                                 1
                                ≥ f (Si−1 ) +         max f (U | Si−1 )
                                              p + 1 U ∈I
                                                 1                       
                                ≥ f (Si−1 ) +         f (OPT) − f (Si−1 ) ,
                                              p+1

using monotonicity/submodularity and OPT ∈ I. Rearranging, the residual gap shrinks by a
        p
factor p+1 :
                                            
                                          p                         
                     f (OPT) − f (Si ) ≤ p+1   · f (OPT) − f (Si−1 ) .

After ℓ rounds,
                                           ℓ
           f (OPT) − f (Sℓ ) ≤         p
                                      p+1     f (OPT) ≤ e−ℓ/(p+1) f (OPT) ≤ ε · f (OPT),

by the choice ℓ = gp (ε). Hence f (Sℓ ) ≥ (1 − ε)f (OPT).

Complexity. Each greedy pass uses only the value oracle for f and an independence/mem-
                                                                                             1
bership oracle for I; total time is polynomial in |N | and ℓ. (Greedy for p-systems and the p+1
factor are standard.)


Notes & context
   • Your bicriteria formalism: We used exactly the (α, β) notion with 1S ≤ β y2 (and y1 =
     0), which is the natural specialization for down-closed systems since it’s equivalent to
     1S /β ∈ P .

   • For p = 1 (matroids) our bound gives g1 (ε) ≤ ⌈2 ln(1/ε)⌉. Your paper sharpens this to
     (1 − ε, ⌈ln(1/ε)⌉) via Measured Continuous Greedy + pipage rounding, and also gives a
     simple fully-combinatorial (1 − ε, ⌈log2 (1/ε)⌉) algorithm.

   • Reference for p-systems (definition, special cases, and greedy analysis) is Calinescu–
     Chekuri–Pál–Vondrák.


TL;DR
A multi-pass greedy that unions
                                             l ln(1/ε) m
                                 gp (ε) =             ≲ (p + 1) ln 1ε
                                              ln p+1
                                                   p

independent sets achieves a (1−ε, gp (ε)) bicriteria approximation for maximizing a monotone
submodular f over any p-system—value 1−ε of OPT with only a logarithmic-in-1/ε blow-up
scaled by p. This matches your framework and uses only value + independence oracles.




                                                    10
Our Evaluation of GPT-5’s Response
The β parameter, known as the inapproximability ratio, is set by GPT-5 to roughly ln(1/ε)
                                                                                     p+1 =
                                                                                                  ln   p
log1+1/p (1/ε) instead of log1+p (1/ε), as in our conjecture. We note that the choice of GPT-5 for
β makes more sense than the one from the conjecture since the infeasibility ratio should get worse
(larger) with p. Furthermore, the proof of GPT-5 for its choice of β is basically correct, up to the
following points.

     • In the inequality
                                                  ℓ
                 f (OPT) − f (Sℓ ) ≤          p
                                             p+1     f (OPT) ≤ e−ℓ/(p+1) f (OPT) ≤ ε · f (OPT),

                                                                          ℓ
                                                                         p
       the third inequality is incorrect. However, the second side p+1       f (OPT) is indeed upper
       bounded by the rightmost side ε · f (OPT), so the error is only due to the unnecessarily second
       inequality, which is somewhat lossy.

     • The note for the case of p = 1 refers to the results of [7] for this case. The second result
       of [7] mentioned (a guarantee of (1 − ε, ⌈log2 (1/ε)⌉)) uses the same algorithm as suggested by
       GPT-5, and is in fact an exact restriction of the result proved by GPT-5 to this special case
       because g1 (ε) = ⌈log2 (1/ε)⌉. However, GPT-5 fails to notice that because in the context of
       this notes it only considers the upper bound g1 (ε) ≤ ⌈2 ln(1/ε)⌉ as its result, and “forgets”
       the exact value of g1 (ε).


3     Maximizing a Weakly-DR-Submodular Function over a Convex
      Set Constraint
Recall that weak-submodularity (due to [5]) is a well-studied relaxation of submodularity for set
functions. Our third conjecture is about an analogous relaxation for DR-submodularity of contin-
uous functions. It asks to maximize a continuous monotone function with this relaxed property
subject to a convex set constraint. For the prompt of this conjecture, we have attached the paper
[1], which defines DR-submodularity and studies optimization of DR-submodular functions.

    Prompt to GPT-5

    A non-negative monotone differentiable function F : [0, 1]N → R≥0 is γ-weakly DR-submodular
    if for every two vectors x, y ∈ [0, 1]N such that x ≤ y, it holds that
                             X                     ∂F (x)
                                   (yu − xu ) ·           ≥ γ · [F (y) − F (x)] .
                                                    ∂xu
                             u∈S

    Given such a function which is also L-smooth and a convex set C ⊆ [0, 1]N . The goal in
    the current problem is describe an algorithm that finds a vector z ∈ C that (approximately)
    maximizes F . A good reference for DR-submodular is the paper attached.


Conjecture. We believe that is not difficult to show that the Frank-Wolfe-like algorithm of [1]
can guarantee 1 − e−γ approximation for this problem (up to an appropriate error term).



                                                         11
Response of GPT-5 (thought for 1m 47s)

Here’s a clean, projection-free method that works under your assumptions and gives the usual
continuous-greedy/Frank–Wolfe style guarantee, adapted to the γ-weak DR setting.


Algorithm (projection-free continuous greedy / Frank–Wolfe
variant)
Input:

    • monotone, non-negative, differentiable, L-smooth, γ-weakly DR-submodular F               :
      [0, 1]N → R+ ;

    • a down-closed convex feasible region C ⊆ [0, 1]N (if C is down-closed with lower bound
      u ̸= 0, shift to C ′ = {x | x = y − u, y ∈ C} and optimize F ′ (x) = F (x + u));

    • number of iterations K; optional linear-oracle accuracy parameters α ∈ (0, 1] (multiplica-
      tive) and δ ≥ 0 (additive).

Oracle: ability to (approximately) solve

                                   vk ∈ arg max⟨v, ∇F (xk )⟩.
                                              v∈C

Initialize: x0 ← 0.
For k = 0, 1, . . . , K − 1:

   1. Compute gradient gk = ∇F (xk ).

   2. (Linear oracle) Find vk ∈ C such that

                                 ⟨vk , gk ⟩ ≥ α · max⟨v, gk ⟩ − 21 δL.
                                                    v∈C


   3. Use the constant step size γk = K1 and update

                                        xk+1 ← xk + γk vk .

Return z = xK ∈ C.
Why this update (using vk , not vk − xk )? For DR-submodular objectives, F (x + ξv) is concave
in ξ for any non-negative direction v, so moving toward vk preserves a 1-D concavity that
powers the analysis.
If your feasible set is down-closed with a nonzero lower bound, shift it to the positive orthant
as noted above and run the same procedure; this is standard in the continuous-greedy analysis.


Approximation guarantee (with γ-weak DR)
Let x⋆ ∈ arg maxx∈C F (x). Under L-smoothness (the usual 1-D descent lemma along any
direction), one obtains the standard additive error term from discretization: for step size γk
the loss is bounded by 2 k γk2 . Using constant γk = K1 gives an additive 2K
                        LP                                                 L
                                                                             .



                                                12
 For the value factor, the usual DR analysis yields

                               max⟨v, ∇F (xk )⟩ ≥ F (x⋆ ) − F (xk ).
                                v∈C

 In your γ-weak DR setting (your inequality ⟨y − x, ∇F (x)⟩ ≥ γ [F (y) − F (x)] on monotone
 directions), this tightens to

                              max⟨v, ∇F (xk )⟩ ≥ γ [F (x⋆ ) − F (xk )],
                              v∈C

 and with an α-approximate linear oracle we get

                          ⟨vk , ∇F (xk )⟩ ≥ αγ [F (x⋆ ) − F (xk )] − 12 δL.

 Plugging this into the standard continuous-greedy recursion gives

                     F (xK ) ≥ (1 − e−αγ ) F (x⋆ ) − 2K
                                                      L
                                                        − Lδ
                                                          2 + e
                                                               −αγ
                                                                   F (0).

 When F (0) = 0 and you use an exact oracle (α = 1, δ = 0), this is

                                 F (z) ≥ (1 − e−γ ) F (x⋆ ) − 2K
                                                               L
                                                                 .

 For γ = 1 this recovers the classic (1 − 1/e) for continuous greedy; the original proof and
 statement (for full DR, i.e., γ = 1) appear as Algorithm 1 + Theorem 1 with the L-smooth
 additive term shown explicitly.


 Practical notes
     • Oracle cost. Each iteration calls a linear optimization oracle over
                                                                         C (e.g., a positive
       LP if C is a down-closed polytope). With constant steps, K = Θ Lε iterations suffice to
       make the additive term ≤ ε.

     • Why no projections? This method stays feasible by construction and avoids projec-
       tions, which is important for complicated C.

     • Relationship to DR/weak-DR. The paper formalizes weak-DR as equivalent to sub-
       modularity and then specializes to DR (which adds coordinate-wise concavity); the algo-
       rithm and analysis are given for monotone DR functions. Your γ-weak DR simply scales
       the marginal-gain lower bound, hence the exponential factor becomes e−αγ .

 If you’d like, I can tailor this to your exact C (e.g., matroid/knapsack polytopes) and pick the
 fastest linear oracle for it.


Our Evaluation of GPT-5’s Response
The response of GPT-5 seems to be correct in general. However, we note the following.

   • GPT-5 restricts its response to down-closed sets C. This restriction is unnecessary (it is never
     used in the analysis), but some published works on the subject include it for no good reason,
     and GPT-5 follows them instead of observing that the restriction is unnecessary.


                                                 13
   • The phrasing used by GPT-5 is a bit weird in times. For example, it uses of the unknown term
     value factor instead of approximation ratio, and it references the unspecified Algorithm 1
     + Theorem 1.
A more general issue with the response of GPT-5 is that it omits many intermediate steps, making
it a difficult read even for experts. Thus, we have decided to ask GPT-5 to produce a self-contained
version of the proof.

  Prompt to GPT-5

  Provide the full proof.

  Response of GPT-5 (thought for 4m 32s)

  Here’s a self-contained proof of the Frank–Wolfe–style method for maximizing a non-negative,
  monotone, differentiable, L-smooth, γ-weakly DR-submodular function F : [0, 1]N → R≥0
  over a convex, down-closed set C ⊆ [0, 1]N with lower bound 0. (If your feasible set does
  not have lower bound 0, shift as in the reference by translating the lower bound to 0.) The
  proof directly adapts the analysis of Bian–Mirzasoleiman–Buhmann–Krause and only changes
  one line to account for the γ-weakness. We keep an (optional) multiplicative linear-oracle
  accuracy parameter α ∈ (0, 1] (set α = 1 for an exact oracle). The algorithmic template and
  the smoothness inequality we use are in the cited reference.


  Algorithm
  Initialize x0 ← 0, t ← 0. For k = 0, 1, 2, . . . while t < 1:

     1. Choose vk ∈ C that (approximately) maximizes the linearization:

                                    ⟨vk , ∇F (xk )⟩ ≥ α · max⟨v, ∇F (xk )⟩.
                                                           v∈C


     2. Pick a stepsize γk ∈ (0, 1], then clip to stay within total mass 1: γk ← min{γk , 1 − t}.

     3. Update xk+1 ← xk + γk vk and t ← t + γk .
                                         PK−1
  Return z = xK after K iterations (so      k=0 γk = 1). This is exactly Algorithm 1 in the
  reference (we only omit
                       P  an additive oracle
                                       P error to keep the presentation clean). Feasibility
  follows because xK = k γk vk + (1 − k γk ) · 0 is a convex combination of points in C (and
  0 ∈ C).


  Assumptions recalled from the reference
     • Down-closed feasibility in the positive orthant with lower bound 0 (so 0 ∈ C).

     • Directional smoothness: for any x and any v ∈ RN     + , letting gx,v (ξ) = F (x + ξv) for
       ξ ∈ [0, 1],
                                                                   L
                              F (x + ξv) ≥ F (x) + ξ⟨v, ∇F (x)⟩ − ξ 2 .                       (1)
                                                                    2
       This is the one-dimensional smoothness bound used in the reference.


                                                    14
   • Monotone DR-submodularity implies concavity along any non-negative direction; we
     do not need concavity for the inequality (1) but it motivates taking vk (a non-negative
     direction) rather than vk − xk .
   • Weak DR is the first-order characterization of continuous submodularity in the reference;
     below we insert our factor γ (your assumption).


Key inequality from γ-weak DR
Your assumption says: for all x ≤ y,
                          X
                              (yu − xu ) ∂u F (x) ≥ γ [F (y) − F (x)].
                              u

Apply this with y = x⋆ ∨x                                                                     ⋆
                            k and x = xk (coordinate-wise max), and note F is monotone so F (x ∨
xk ) ≥ F (x⋆ ). Also ∇F (xk ) ≥ 0 coordinate-wise because F is monotone and differentiable.
Hence
                          (x⋆ − xk )+ , ∇F (xk ) ≥ γ [F (x⋆ ) − F (xk )].              (2)
Moreover, since ∇F (xk ) ≥ 0 and x⋆ ≥ (x⋆ − xk )+ component-wise,
                              ⟨x⋆ , ∇F (xk )⟩ ≥     (x⋆ − xk )+ , ∇F (xk ) .                 (3)
Combining (2)–(3), and using the linear oracle,
        ⟨vk , ∇F (xk )⟩ ≥ α max⟨v, ∇F (xk )⟩ ≥ α⟨x⋆ , ∇F (xk )⟩ ≥ αγ [F (x⋆ ) − F (xk )].    (4)
                              v∈C

For γ = 1, this reproduces Lemma 1 in the reference (up to the optional additive error they
include); here we simply scale by γ.


Per-iteration progress via smoothness
Apply (1) with ξ = γk and v = vk :
                                                                            L 2
                          F (xk+1 ) ≥ F (xk ) + γk ⟨vk , ∇F (xk )⟩ −         γ .
                                                                            2 k
Using (4),
                                                                               L 2
                       F (xk+1 ) ≥ F (xk ) + αγ γk [F (x⋆ ) − F (xk )] −        γ .          (5)
                                                                               2 k

Solving the recurrence
Let ∆k := F (x⋆ ) − F (xk ). Rearranging (5),
                                                                  L 2
                                    ∆k+1 ≤ (1 − αγ γk ) ∆k +       γ .                       (6)
                                                                  2 k
                                                    P
Iterating (6) over k = 0, . . . , K − 1 and using        k γk = 1, we get
                                                               K−1
                                                             L X 2
                                     ∆K ≤ e−αγ ∆0 +             γk .
                                                             2
                                                               k=0




                                                    15
  Therefore
                                                           K−1
                                                         L X 2
                      F (xK ) ≥ (1 − e−αγ ) F (x⋆ ) −       γk + e−αγ F (x0 ).                      (7)
                                                         2
                                                           k=0

  This is precisely the reference’s Theorem 1 with α replaced by αγ. (They prove the γ = 1 case;
  compare their display (6).)
  If we take constant steps γk ≡ 1/K, then k γk2 = 1/K and F (0) = 0 (by non-negativity at
                                               P
  the origin), yielding the clean bound

                                                                    L
                                 F (xK ) ≥ (1 − e−αγ ) F (x⋆ ) −      .                             (8)
                                                                   2K

  This is the exact analogue of Corollary 1 in the reference, again with α replaced by αγ.


  Remarks
     • When the linear subproblem is solved exactly (α = 1), (8) gives a (1−e−γ )-approximation
       in the limit K → ∞; for the usual DR case (γ = 1) this is the classic 1 − 1/e factor.

     • The analysis only used: (i) your γ-weak DR inequality to get (4), (ii) the P
                                                                                  simple smooth-
       ness lower bound (1) along the non-negative direction vk , and (iii) that     γk = 1. The
       rest is algebra identical to the reference’s proof of Theorem 1.

  This completes the proof.


Our Evaluation of GPT-5’s Response
This time the response of GPT-5 is much more detailed. However, despite writing almost every-
thing from scratch, as requested, the response follows Bian et al. [1] very closely, and also constantly
compares itself to this work. This close following of [1] creates an unnecessary complication. Specif-
ically, the algorithm and most of the analysis are based on variable step sizes, and only towards
the end of the analysis these are replaced with a fixed step size (which is what was originally used
in the previous response). It is also interesting to note that the response is not very consistent
regarding its assumption about the sum of the step sizes. In most places, there seems to be an
assumption that these step sizes add up to 1, but other places, such as the proof that xK ∈ C do
not seem to include this assumption.
    Below we list a few additional minor issues in the analysis.

   • Bian et al. [1] defines both DR-submodularity and weak DR-submodularity. Our new defi-
     nition in the prompt of γ-weakly DR-submodular employs the word “weak”, but is in fact a
     relaxation of the DR-submodularity of [1], rather than of the weak DR-submodularity of [1].9
     GPT-5 seems to be confused because of this similarity in the names when it discusses the
     assumption of Weak DR from the reference.

   • GPT-5 tries to explain that the operator ∨ represents coordinate-wise maximization. How-
     ever, it does that after the wrong equality (specifically, one equality after the one in which
  9
    The motivation for the name we use is a the weak submodularity for set functions introduced by Das and
Kempe [5].


                                                   16
       this operator is used), which makes it difficult to understand what operator the definition
       refers to.
     • GPT-5 claims that F (0) = 0 due to the non-negativity of F . However, this non-negativity
       only implies that F (0) ≥ 0. Fortunately, however, that inequality suffices for letting the proof
       go through.


4     Maximizing a Partially Monotone Weakly-Submodular Func-
      tion over a Cardinality Constraint
Recall that weak-submodularity is a relaxation of the submodularity property introduced by [5].
A more recent paper by Santiago and Yoshida [10] studies optimization of non-monotone weakly-
submodular functions. A different paper by Mualem and Feldman [9] introduced the notion of m-
monotonicity that relaxes the property of monotonicity. Our fourth conjecture is about combining
the two relaxations, i.e., getting results for maximization of weak-submodular m-monotone set
functions. The results of [10] immediately apply to this easier case, and thus, the interesting
question is whether one can get better guarantee as a function of the parameter m, which measures
the distance of the function from monotonicity (monotone functions have m = 1, and m decreases
to 0 as the function becomes more and more non-monotone in some sense). For the prompt of this
conjecture, we have attached the papers [9] and [10].

    Prompt to GPT-5

    The monotonicity ratio was defined in our paper “Using Partial Monotonicity in Submodular
    Maximization”, and weak submodularity was extended to non-monotone functions by the paper
    “Weakly Submodular Function Maximization Using Local Submodularity Ratio”. Both papers
    are attached. In the current problem, we are given a non-negative m-monotone γ-weakly
    submodular function f : 2N → R≥0 and a positive integer 1 ≤ k ≤ |N |. The goal is to find a
    set S ⊆ N of size at most k that (approximately) maximizes f among all such sets.


Conjecture. We believe that one can use the m-monotonicity of f to get new bounds on the
values ᾱi and β̄i used in the proof of [10]. These new bounds should improve (for m > 0) over the
bounds given by [10], and plugging them into Theorem 2.4 of the same paper should then yield an
improved result (again, for m > 0).

    Response of GPT-5 (thought for 2m 52s)

    Here’s a clean, provably-good way to tackle your hybrid setting (non-negative, m-monotone,
    γ-weakly submodular; cardinality ≤ k).


    Algorithm
    Use the Randomized Greedy with dummies (Buchbinder et al. style), analyzed for weak sub-
    modularity:

       • Add 2k dummy elements D with zero marginal gain.

       • For each round i = 1, . . . , k:


                                                   17
          Let Mi be a size-k subset of remaining elements (original ground set ∪D) maximizing
        – P
            e∈Mi fSi−1 (e) (break ties in favor of real elements).
        – Pick a uniform random element ei ∈ Mi and set Si = Si−1 ∪ {ei }.

Return Sk . This uses O(nk) oracle calls.


Guarantees you can cite
General non-monotone γ-weakly submodular (your case, no extra assumptions):
Running the algorithm above yields, in expectation,
                                                    γ
                                    E[f (Sk )] ≥      f (OPT).
                                                    e
This follows from the “localPsubmodularity ratio” analysis, which for constant γi = γ gives a
                           1   k−1
non-monotone guarantee ek      i=0 γi = γ/e.
A complementary bound from the same algorithm is

                                    1 k−1
                                     
               E[f (Sk )] ≥ γ 1 −          f (OPT) (as k → ∞ this is γe−1/γ ),
                                   γk
but γ/e is never worse and is strictly better unless γ = 1.

If f turns out to be monotone (m = 1) in your instance:             The same analysis with local
ratios gives the Das–Kempe-style bound

                                E[f (Sk )] ≥ (1 − e−γ )f (OPT).

(Here the monotone branch of the theorem applies.)

If in addition f is actually submodular (γ = 1) and you want to leverage partial
monotonicity m: Two simple baselines (different algorithms) are available:
   • Greedy (add the best non-negative marginal each step) achieves

                                   f (Sk ) ≥ m (1 − 1/e) f (OPT).

   • Random Greedy (no dummies; sample one from the top-k marginal set each round)
     achieves                                           
                     E[f (Sk )] ≥ m(1 − 1/e) + (1 − m)1/e f (OPT).


Practical takeaway
   • Default choice (fits your stated assumptions): run Randomized Greedy with dummies;
     you get at least γ/e of OPT in expectation, with only O(nk) oracle calls.

   • If later you verify monotonicity (m = 1), your bound tightens to 1 − e−γ .

   • If you also verify submodularity (γ = 1), you can switch to the simple Greedy/Random-
     Greedy variants and plug in the m-dependent bounds above.


                                               18
Our Evaluation of GPT-5’s Response
GPT-5 did not really give any result for this problem. It just states some known results. First it
says that if you ignore the m-monotonicity, then one can get the result that is known when the
m-monotonicity is not given. Then, it says that in the special case of m = 1 (i.e., the function
is monotone), one can use known results for maximizing monotone weakly submodular functions,
and in the special case of γ = 1 (i.e., the function is submodular), one can use known results for
maximizing m-monotone submodular functions.
    To get a more meaningful answer, we then asked GPT-5 for an algorithm whose guarantees
improves smoothly with m and γ. Such a request does not exactly exclude the above answers
(in the mathematical sense), but we hoped it might give GPT an “intuitive” idea of what we are
looking for.

  Prompt to GPT-5

  The monotonicity ratio was defined in our paper “Using Partial Monotonicity in Submodular
  Maximization”, and weak submodularity was extended to non-monotone functions by the paper
  “Weakly Submodular Function Maximization Using Local Submodularity Ratio”. Both papers
  are attached. In the current problem, we are given a non-negative m-monotone γ-weakly
  submodular function f : 2N → R≥0 and a positive integer 1 ≤ k ≤ |N |. The goal is to find a
  set S ⊆ N of size at most k that (approximately) maximizes f among all such sets. Find an
  algorithm whose guarantees improve smoothly with m and γ. Provide the full proof.

  Response of GPT-5 (thought for 11m 44s)

  Below is a complete, self-contained proof that the standard Randomized Greedy with dum-
  mies algorithm attains a guarantee that improves smoothly with both the monotonicity
  ratio m and the (local) weak-submodularity ratios γi for the problem

                                    max{f (S) : S ⊆ N , |S| ≤ k},
  when f : 2N → R≥0 is non-negative, m-monotone, and γ-weakly submodular.


  Theorem (smooth in m and γ)
  Run RandomizedGreedy (with 2k dummies) for k iterations (algorithm recalled below). Let
  γ0 , . . . , γk−1 ∈ [0, 1] be any numbers such that at iteration i (with current solution Si−1 ) the
  local weak-submodularity condition
                        X                     
                               fSi−1 (e) ≥ min γi · fSi−1 (OPT), fSi−1 (OPT)                    (LSR)
                       e∈OPT

  holds (this is satisfied, e.g., by taking the local ratios of Santiago–Yoshida, or by γi ≡ γ when
  f is globally γ-weakly submodular). Then, if Sk is the output,
                              k−1                                k−1
                             Y                          1−mX                i
                                   1 − γki                           γi 1 − k1 f (OPT).
                  
          E f (Sk ) ≥ 1 −                     m f (OPT) +                                          (*)
                                                              k
                              i=0                                i=0

  In particular, using 1 − i (1 − γi /k) ≥ 1 − exp − k1 i γi and mini (1 − k1 )i = (1 − k1 )k−1 ≥ e−1 ,
                           Q                           P 




                                                   19
                                                                                     k−1
                                          1 Pk−1
                                                                              1−mX
              E[f (Sk )] ≥          1 − e− k  i=0 γi        m f (OPT) +             γi f (OPT) .
                                                                                ek
                                                                                     i=0

If γi ≡ γ, this simplifies to

                                                   m(1 − e−γ ) + (1 − m) γe f (OPT).
                                                                          
                         E[f (Sk )] ≥

Ingredients from the attached papers
1. Monotonicity ratio m. For a non-negative submodular f , the monotonicity ratio is

                                                                  f (T )
                                         m :=          min               ∈ [0, 1],
                                                     S⊆T ⊆N       f (S)
so f is m-monotone iff f (T ) ≥ m f (S) for all S ⊆ T . This interpolates between general (m = 0)
and monotone (m = 1) functions.
2. Randomized Greedy with 2k dummies. In each of k rounds, pick a size-k set Mi
maximizing the sum of marginals and add a uniformly random element of Mi . With dummies
we have |MPi | = k and every chosen
                               P       marginal is nonnegative, hence f (Si ) is nondecreasing
in i. Also e∈Mi fSi−1 (e) ≥      e∈OPT fSi−1 (e).
3. Local submodularity ratios & one-step progress. Santiago–Yoshida analyze Random-
izedGreedy using local ratios γA,B , yielding the per-round lower bound
                                           1      n                           o
              E f (Si ) − f (Si−1 ) | Si−1 ≥   · min γi fSi−1 (OPT), fSi−1 (OPT) .         (P)
                                             k
(Here γi may be chosen from the local γA,B family; taking γi ≡ γ also satisfies (LSR).) This is
the “dynamic local ratio” replacement for the classic submodular step.
4. Partial monotonicity via Lovász extension. For non-negative m-monotone submodular
f , for any deterministic O and random D,
                                                                               
                      E[f (O ∪ D)] ≥                1 − (1 − m) · max Pr[u ∈ D] f (O).                 (PM)
                                                                        u

5. A simple occupancy bound under Randomized Greedy. For every u and every round
i,
                                                       1 i
                                 Pr[u ∈ Si ] ≤ 1 − 1 −       .                (Occ)
                                                        k
(Each element is selected in round i with prob. ≤ 1/k.)
6. Randomized Greedy analysis template. For submodular f , partial monotonicity plus
(Occ) gives
                                 h                 1 i−1 i
           E f (Si−1 ∪ OPT) ≥ m + (1 − m) 1 −                  · f (OPT).                          (UnionLB)
                                                      k
(Exactly Corollary 4.6 in the partial-monotonicity paper.)




                                                             20
A calculus inequality we shall use
For any γ ∈ [0, 1], any real x, and any y ≥ 0,

                          min{γ(x + y), x + y} ≥ min{γx, x} + γy.                         (MIX)
Proof. If x ≥ 0 then min{γ(x + y), x + y} = γ(x + y) = γx + γy = min{γx, x} + γy. If x < 0 and
x + y ≤ 0 then min{γ(x + y), x + y} = x + y ≥ x + γy = min{γx, x} + γy since γ ≤ 1. If x < 0
and x + y > 0 then min{γ(x + y), x + y} = γ(x + y) = γx + γy ≥ x + γy = min{γx, x} + γy
because γx ≥ x.

Proof of the theorem
Let OPT be any optimal size-k solution, and let S0 = ∅. Fix i ∈ {1, . . . , k}. By the choice of
Mi and (LSR), we have the one-step bound (P):
                                          1      n                           o
             E f (Si ) − f (Si−1 ) | Si−1 ≥   · min γi fSi−1 (OPT), fSi−1 (OPT) .
                                            k
Taking total expectation and writing

                          fSi−1 (OPT) = f (Si−1 ∪ OPT) − f (Si−1 ),
we get

                       1 h               i
 E f (Si ) − f (Si−1 ) ≥   E min γi ∆i , ∆i ,         where ∆i := f (Si−1 ∪ OPT) − f (Si−1 ). (1)
                         k
Lower bounding the “union” term via partial monotonicity. Apply (PM) with O =
OPT and D = Si−1 . Using (Occ), maxu Pr[u ∈ Si−1 ] ≤ 1 − (1 − k1 )i−1 , hence

                        h        i−1 i           h            i−1 i
E f (Si−1 ∪OPT) ≥ 1−(1−m) 1− 1− k1         f (OPT) = m+(1−m) 1− k1
              
                                                                          f (OPT),

which is precisely (UnionLB).
Thus
                             h                  i−1 i
                  E[∆i ] ≥    m + (1 − m) 1 − k1        f (OPT) − E[f (Si−1 )].               (2)

Plug into the one-step inequality. Using (MIX) with x = m f (OPT) − E[f (Si−1 )] and
y = (1 − m)(1 − k1 )i−1 f (OPT) ≥ 0, and then combining with (1)–(2), we obtain

                        1                       
   E f (Si ) − f (Si−1 ) ≥     min{γi x, x} + γi y
                           k
                                                                                              (3)
                           γi                           γi               i−1
                         ≥      mf (OPT) − E[f (Si−1 )] +    (1 − m) 1 − k1      f (OPT).
                           k                              k
(The second line uses that, in any case, the chosen marginal is nonnegative under the dummy
trick, so replacing min{γi x, x} by γi x only weakens the lower bound when x < 0.)
Rearranging (3),


                                                 21
                                          γi h                   i−1 i
                     1 − γki E[f (Si−1 )] +
          E[f (Si )] ≥                           m + (1 − m) 1 − k1        f (OPT).                (4)
                                            k
Unrolling the recurrence. Starting from E[f (S0 )] = f (∅) ≥ 0 and iterating (4),
                           k             k 
                           X γi          Y             γt  h                   i−1 i
           E[f (Sk )] ≥                          1−         · m + (1 − m) 1 − k1        f (OPT).
                                 k                     k
                           i=1          t=i+1

Discarding the product (which is ≤ 1) in the m-part and using the product fully in the (1 − m)-
part yields exactly the claimed explicit bound (*):
                                k−1                                       k−1
                               Y               1−mX 
                                                                    i
        E[f (Sk )] ≥       1−          1 − γki               γi 1 − k1 f (OPT).
                                                      m f (OPT) +
                                                  k
                               i=0                      i=0

From (*) to the compact closed form. Finally, 1 − i (1 − γi /k) ≥ 1 − exp − k1 i γi , and
                                                 Q                            P 
mini (1 − k1 )i = (1 − k1 )k−1 ≥ e−1 . Hence
                                           1 P
                                                        1−mX
              E[f (Sk )] ≥           1 − e− k  i γi       m f (OPT) +
                                                                  γi f (OPT),
                                                          ek
                                                               i

as stated. When γi ≡ γ, this becomes E[f (Sk )] ≥ m(1 − e ) + (1 − m) γe f (OPT).
                                                         −γ
                                                                        

This completes the proof.

Notes & connections to the attached results
   • When m = 1P(monotone),   the theorem reduces to the local-ratio monotone guarantee
     1 − exp − k1 i γi proved by Santiago–Yoshida (first bullet of their Theorem 1.10).
                      

   • When m = 0 (general non-monotone), the theorem reduces to ek     1 P
                                                                          i γi , i.e., the non-
     monotone local-ratio bound (second bullet of their Theorem 1.10).

   • For submodular (γi ≡ 1) objectives, the bound becomes exactly the smooth m-
     (1/e) interpolation proved for Random Greedy in the “partial monotonicity” paper:
     E[f (Sk )] ≥ m(1 − 1/e) + (1 − m) · (1/e). Our proof retraces their Section 4.2 steps but
     replaces the single submodular step by the local-ratio inequality (P).

   • The occupancy bound (Occ) and the Lovász-extension corollary (PM) are exactly Lemma
     4.5 and Corollary 2.2 in the partial-monotonicity analysis, which are the only places
     where m enters; all the γ-dependence flows through the (LSR) step taken from Santiago–
     Yoshida.

Algorithm (for completeness)
RandomizedGreedy(f, k). Add 2k dummy elements D with zero marginal; P         initialize S0 = ∅.
For i = 1, . . . , k: pick Mi ⊆ (N ∪ D) \ Si−1 of size k maximizing e∈Mi fSi−1 (e) (tie-break
toward real elements); sample ei uniformly from Mi ; set Si = Si−1 + ei ; return Sk . (Dummies
ensure nonnegative chosen marginals and |Mi | = k.)




                                                            22
  What to remember
     • Guarantee scales smoothly in both parameters: as m ↑ 1 you recover the monotone-
       γ guarantee; as m ↓ 0 you recover the non-monotone γ bound.

     • With global γ, the clean corollary is E[f (Sk )] ≥ m(1 − e−γ ) + (1 − m)γ/e OPT.
                                                                                 


  These theorems use only standard Randomized Greedy; no tuning or extra parameters are
  needed.


Our Evaluation of GPT-5’s Response
As we have observed also for previous problems, GPT-5 sticks to the reference papers even at the
cost of introducing extra unnecessary complications in its response. Specifically, in the current
problem, the response of GPT-5 refers to local weak submodularity ratios despite the fact that the
prompt only referred to global weak submodularity.
    Unlike the situation in the previous problems, here the response of GPT-5 is clearly wrong.
Below we list multiple mistakes of various significance levels, ranging from funny typos to errors
that essentially make the answer useless.

   • The inequalities (LSR) and (P) are missing a factor of 1/γi in the second term of their
     corresponding minimum expressions.

   • GPT-5 uses the equality mini (1 − k1 )i = (1 − k1 )k−1 ≥ e−1 to lower bound the terms (1 − k1 )i .
     It has to use such a weak bound because, as discussed above, it chose to prove a more general
     result with varying local ratios rather than a result with one global ratio as it was asked to
     prove. If GPT-5 had used one global ratio, then it could instead simple bound the sum of
     the elements (1 − k1 )i , and get a better result. Notice that this sum is easy to compute as it
     is the sum of a geometric series.

   • GPT titles (MIX) as “calculus inequality”, which is inappropriate since the proof of this
     inequality has nothing to do with calculus.

   • GPT-5 claims that (PM) can be proved using the Lovász extension, but does not give too
     many details. Unfortunately, the Lovász extension can be used for this purpose only for
     submodular functions, and fails for weakly submodular ones.

   • The second inequality in (3) does not seem to be justified. Interestingly, GPT-5 “noticed”
     that this inequality is questionable, and thus, tries to give a justification for this inequality,
     but this justification does not work. First, because this justification does not really try to
     justify the given inequality. Instead, it tries to justify a different version of this inequality in
     which a maximum with 0 is added to the second side. Second, and more importantly, the
     justification seems to ignore the fact that once the contribution of γi y is removed from the
     marginal f (Si ) − f (Si−1 ), one can no longer argue that what remains is non-negative using
     the dummy elements argument. One can only argue that what remains is at least −γi y.

   • Between the two unnumbered display math inequalities appearing immediately after (4), a
     product is discarded. This discard is unjustified because this product can be (and almost
     always is) less than 1 (as GPT-5 itself correctly identifies). Furthermore, in the second of
     these unnumbered inequalities, γi should have been γi+1 in both places where it appears


                                                  23
       because of a change that takes place between the two inequalities regarding the limits of the
       sums.


5      Maximizing a Monotone Weakly-Submodular Function over a
       Matroid Intersection Constraint
Our last conjecture is about maximizing a monotone weakly-submodular function subject to two
matroid constraints. For the prompt of this conjecture, we have attached the paper [3], which
studies the special case of this problem in which there is only one matroid constraint.

    Prompt to GPT-5

    In the paper ”Weakly Submodular Maximization Beyond Cardinality Constraints: Does Ran-
    domization Help Greedy?” gives an approximation ratio of (1 + 1/γ)−2 for a general matroid
    constraint. The paper is attached. Given a non-negative monotone γ-weakly-submodular func-
    tion f : 2N → R≥0 and 2 matroids M1 = (N , I1 ) and M2 = (N , I2 ) over the same ground
    set, we would like to find a set S that is independent in both matroids (i.e., S ∈ I1 ∩ I2 ) and
    (approximately) maximizes f among all such sets. Provide an algorithm and the full proof of
    its approximation guarantee.


Conjecture. The paper [3] gives an approximation ratio of (1 + 1/γ)−2 for this problem. We
originally conjectured that its algorithm and analysis technique should easily extend to two matroids
(but yield a worse guarantee for this case). Algorithm 1 is the algorithm that would have been
obtained in this way. As one can see below, GPT-5 indeed suggested this algorithm (up to minor
changes), but failed to analyze it correctly. Furthermore, after studying the response of GPT-5, we
came to the conclusion that while it might indeed be possible to prove an interesting approximation
guarantee for Algorithm 1, this seems to be more challenging than we have originally realized.

    Algorithm 1: Random Greedy for Matroid Intersection
 1 Let S0 ← ∅ and i ← 0.
 2 while there exists an element u ∈ N \ Si such that Si + u ∈ I1 ∩ I2 do
 3       Increase i by 1.
 4       For every element u ∈ N \ Si−1 , define wi (u) ≜ f (u | Si−1 ).
 5       Let Mi be a set of maximum weight according to the weight function wi among all the
          sets that are independent in both contracted matroids M1 /Si−1 and M2 /Si−1 .
          // There are known algorithms for finding such a set in polynomial time.
 6       Let ui be a uniformly random element of Mi .
 7       Let Si ← Si−1 + ui .
 8 return Si .




    Response of GPT-5 (thought for 10m 43s)

    Below is a self-contained algorithm (no black boxes) for maximizing a non-negative, monotone,
    γ-weakly-submodular set function under the intersection of two matroids, together with a
    complete analysis of its approximation guarantee.


                                                  24
I’ll first restate the weak-submodularity notion we rely on, then give the algorithm and prove
its guarantee step-by-step.


Problem & weak submodularity (set version)
Let f : 2N → R≥0 be monotone and γ-weakly submodular, meaning that for all A, B ⊆ N ,
            X
                  f (u | A) ≥ γ · f (B | A)    where f (B | A) = f (A ∪ B) − f (A).
            u∈B

(We follow the paper’s Definition 1.1; all notational conventions also match the paper.)
Let M1 = (N , I1 ) and M2 = (N , I2 ) be two matroids on the common ground set N . We seek

                                   max{f (S) : S ∈ I1 ∩ I2 }.
Write I := I1 ∩ I2 . Let r denote the maximum size of any common independent set (i.e.,
cardinality of a maximum feasible solution). Let OP T ∈ I be an optimal solution; k below will
denote |OP T | = r.


The algorithm:             Residual Random Greedy for two matroids
(RRG-2MI)
We extend the Residual Random Greedy (RRG) paradigm (Algorithm 1 in the paper) from a
single matroid to the intersection of two matroids. The change is: in every round we compute
a maximum-weight common completion (under both matroids simultaneously), then add a
uniformly random element from it.
RRG-2MI(f, M1 , M2 )
1. S0 ← ∅; let r be the maximum common rank (size of a max set in I).
2. For i = 1, 2, . . . , r

   • For every u ∈ N \ Si−1 , set weight wu := f (u | Si−1 ).

   • Let Mi be a maximum-weight set of size r − i + 1 such that Si−1 ∪ Mi ∈ I. (This is
     a standard weighted matroid-intersection call on the contracted matroids M1 /Si−1 and
     M2 /Si−1 .)

   • Pick ui uniformly at random from Mi and set Si ← Si−1 ∪ {ui }.

3. Return Sr .
Feasibility & complexity. By construction, Si ∈ I for all i. Each round solves one weighted
matroid-intersection instance on N \ Si−1 (polynomial time with independence oracles), and
makes O(|N |) value-oracle calls for the weights. The procedure ends after exactly r rounds, so
total time is polynomial in |N | (dominated by r calls to weighted matroid intersection). (The
single-matroid RRG template and its oracle accounting are as in the attached paper. )




                                               25
Analysis roadmap
The original one-matroid analysis (paper’s Sec. 2) hinges on two ingredients:
1. a progress inequality that lower-bounds the expected gain at round i in terms of the
marginal value of a carefully coupled “residual optimum,” and
2. a decay inequality that lower-bounds the expected value of that residual optimum as
rounds progress.
We prove two analogous statements for the intersection of two matroids. The only new combi-
natorial work is to handle simultaneous exchange in two matroids; for this we use Brualdi’s
base exchange lemma independently in each matroid (as done in the paper for a single matroid)
and combine the exchanges carefully.
Below, k = r.

A. Two-matroid exchange coupling
Fix round i. Consider the two common bases
                           (S)                                 (O)
                          Bi     := Si−1 ∪ Mi ,              Bi      := Si−1 ∪ OP Ti ,
where OP Ti ⊆ N \ Si−1 is a size-(k − i + 1) set chosen so that Si−1 ∪ OP Ti ∈ I and (deter-
ministically) maximizes f (OP Ti ) among all such completions. (Set OP T0 := OP T .) Both are
common independent sets of size k.
Apply Brualdi’s bijection lemma (the paper cites this tool; see Lemma 2.2 and its use)
separately inside M1 and M2 : there are bijections

                                 g1 : Mi → OP Ti ,           g2 : Mi → OP Ti
such that for each u ∈ Mi ,
                                                                                  
           Si−1 ∪ OP Ti − g1 (u) ∪ {u} ∈ I1 ,                 Si−1 ∪ OP Ti − g2 (u) ∪ {u} ∈ I2 .
(Each statement is a direct base-exchange in the corresponding matroid, with Si−1 contracted
away; compare to the one-matroid use in the paper. )
Define the blocking set for u as

                                   Ψi (u) := {g1 (u), g2 (u)} ∩ OP Ti .
Then for every u ∈ Mi ,
                                                      
                                 Si−1 ∪ OP Ti − Ψi (u) ∪ {u} ∈ I1 ∩ I2 .                           (1)
(Indeed, removing g1 (u) certifies independence in M1 , removing g2 (u) certifies independence
in M2 ; removing both preserves independence in both.)
We will use two basic consequences of the max-weight choice of Mi , with weights wx = f (x |
Si−1 ):
(Weight-domination) For each u ∈ Mi ,
                                                              X
                                                     1
                               f (u | Si−1 ) ≥    |Ψi (u)|              f (v | Si−1 ).             (2)
                                                             v∈Ψi (u)




                                                     26
Otherwise replacing u by Ψi (u) would strictly increase the completion’s total weight (feasible
by (1)), contradicting the maximality of Mi .
(Two-to-one compression) Summing (2) over u ∈ Mi and using |Ψi (u)| ≤ 2,
            X                             X      X                               X
                                     1                                      1
                  f (u | Si−1 ) ≥    2                    f (v | Si−1 ) ≥   2             f (v | Si−1 ),   (3)
           u∈Mi                           u∈Mi v∈Ψi (u)                         v∈OP Ti

where the last step uses that every v ∈ OP Ti appears in at least one Ψi (u) (if g1 (u) = v or
g2 (u) = v).

B. Progress inequality (expected gain per round)
Condition on all randomness up to round i − 1. With Mi fixed and ui uniform in Mi ,
                                         1 X
            E f (Si ) − f (Si−1 ) =             f (u | Si−1 )
                                          |Mi |
                                               u∈Mi
                                    (3)     1    X
                                    ≥              f (v | Si−1 )
                                          2|Mi |                                            (4)
                                          v∈OP Ti
                                    γ
                               ≥         f (OP Ti | Si−1 )     (weak submodularity)
                                  2|Mi |
                                        γ                                     
                               =                  f (OP Ti ∪ Si−1 ) − f (Si−1 ) .
                                  2(k − i + 1)
This is the two-matroid analogue of Observation 2.4 in the paper; the only change is the factor
1/2 coming from having to clear feasibility in two matroids simultaneously (via (3) above).
Taking expectation also over the algorithm’s history up to round i − 1 yields

                                                 γ                                           
          E[f (Si )] ≥ E[f (Si−1 )] +                      E[f (OP Ti ∪ Si−1 )] − E[f (Si−1 )] .           (5)
                                            2(k − i + 1)

C. Decay inequality (residual optimum keeps large value)
We now lower-bound E[f (OP Ti )] across rounds. In round i the algorithm selects ui ∈ Mi
uniformly, and we update the residual completion by deleting the blocking set:

                                     OP Ti := OP Ti−1 \ Ψi (ui ).
By (1), Si ∪ OP Ti ∈ I, so the invariant “Si−1 ∪ OP Ti−1 feasible base” persists.
Crucially, since |OP Ti−1 | = |Mi | = k − i + 1 and each v ∈ OP Ti−1 belongs to at least one
blocking set Ψi (u) while u is sampled uniformly from Mi , each v ∈ OP Ti−1 is deleted with
probability at most 1/(k − i + 1). A standard convexity/averaging argument identical to the
paper’s Lemma 2.3 (which conditions on a uniformly chosen element of the residual optimum)
then gives the following two-matroid analogue (the proof is the same induction as in Lemma
2.3 with |Mi | = k − i + 1; we omit verbatim repetition and only note the sampling difference
discussed above).
Lemma 1 (residual value). For every 0 ≤ i ≤ k,
                                                  γ 
                                                i+1
                                       
                            E f (OP Ti ) ≥ 1 − k+1       f (OP T ).                                        (6)



                                                      27
(As in the paper, one proves the slightly stronger exponential form and then integrates to get
the closed form with (i+1)/(k+1); the only property used is that each step removes a uniformly
random one unit of “mass” in expectation from the residual completion, which remains
true here because |OP Ti−1 | = |Mi | and ui is uniform.)
By monotonicity of f , f (OP Ti ∪Si−1 ) ≥ f (OP Ti ); plugging this into (5) we get the two-matroid
progress recurrence
                                         γ             
                                                           i
                                                             γ                          
        E[f (Si )] ≥ E[f (Si−1 )] +                 1 − k+1       f (OP T ) − E[f (Si−1 )] .    (7)
                                    2(k − i + 1)

D. Solving the recurrence
Define Ai := E[f (Si )]. Rearranging (7) gives
                              γ                    γ       
                                                                            i
                                                                               γ   
            Ai ≥ 1 −                     Ai−1 +                1−          k+1          f (OP T ).   (8)
                          2(k − i + 1)          2(k − i + 1)
Iterating (as in the paper’s proof of Theorem 2.6, but with the extra factor 1/2 throughout)
and using the same integral estimate kj=i+1 1j ≥ ln k+1
                                      P
                                                    i+1 , one obtains
                                                   2
                                               γ
                                   Ak ≥                  f (OP T ).                                  (9)
                                              γ+2
(The algebra is exactly the same as in the single-matroid case in the paper—where (γ/(γ + 1))2
appears—except every “+1” that came from one matroid now becomes “+2” because of the
factor 1/2 we carried from (3)→(4)→(5). )
Thus we have proved:

Theorem (approximation under two matroids)
For every non-negative, monotone, γ-weakly-submodular f and two matroids M1 , M2 on the
same ground set, **RRG-2MI** returns a feasible set S ∈ I1 ∩ I2 with
                                                        2
                                                 γ
                               E f (S) ≥                      f (OP T ).
                                                  γ+2
The algorithm runs in polynomial time with value- and independence-oracle access.
Sanity checks.
• When γ = 1 (true submodularity), we get 1/9. (This is not tight—continuous-greedy-
type methods are known to do better for submodular functions under two matroids—but the
guarantee is provable with this simple randomized greedy.)
                                                               2
                                                              γ
• When there is only one matroid, our proof specializes to γ+1     , matching the paper’s
guarantee.


Remarks, variants, and how to tighten further
                                                                               γ
1. Why the square? As in the single-matroid analysis in the paper, one factor γ+(·) comes
from the per-round gain vs. current gap, and the second factor comes from accumulating
those gains across k rounds via the harmonic/integral estimate.


                                                  28
  2. Can we do better? Yes—using the measured continuous greedy in the common-
  independence polytope followed by a contention-resolution scheme for the intersection of two
                                                                 −γ
  matroids yields a (strictly better) ratio that scales like 1−eC for a small constant C (e.g., C = 3
  with a simple scheme). That analysis is different in flavor (fractional relaxation + rounding).
  I kept the proof above fully combinatorial and deliberately parallel to the attached paper’s
  technique.
  3. Implementation note. The only heavy subroutine is weighted matroid intersec-
  tion—polynomial-time and very mature in practice.

  Appendix: the “residual value” induction (sketch)
  For completeness, here is the standard induction underlying Lemma 1 (the same as Lemma
  2.3’s proof in the paper). Condition on round i−1. Let T := OP Ti−1 with |T | = m = k − i + 1,
  and let U be a uniformly random member of Mi . We update T to T ′ = T \ Ψi (U ). Since every
  v ∈ T lies in Ψi (u) for exactly one or two u’s and U is uniform over m choices, one checks
  that
                                              1
                          Pr[v ∈ T ′ ] = 1 −     (in expectation over U ).
                                              m
  Define h(j) := min|R|=j E[f (R)] over all random subsets R ⊆ OP T of size j. Then h is concave
  in j (by the weak-submodular averaging used in the paper), and the above “one unit mass in
  expectation” decrement implies
                                                               
                                                           i+1 γ
                       E[f (OP Ti )] ≥ h(k − i) ≥ 1 − k+1          f (OP T ),

  precisely as in Lemma 2.3.
  If you’d like, I can also write out the continuous-greedy + contention-resolution variant for
  two matroids, which gives a larger constant (roughly (1 − e−γ )/3) with a clean proof in the
  multilinear/continuous framework. “‘


Our Evaluation of GPT-5’s Response
The response of GPT-5 contains multiple errors. The most significant errors stem from GPT-
5’s seemingly inability to “understand” that removing two elements has different consequences
compared to removing a single element. Thus, GPT-5 believes that OP Ti is a set of size k−i despite
the fact that two elements are removed from it in every iteration, which should have resulted in a
set of size k − 2i. Another demonstration of this inability is the proof given for Lemma 1 in the
appendix of the response that would have been correct if Ψi (u) had contained only one element (a
similar error appears also in the argument given for this lemma in Section C of the response).
    In the following, we list additional problems with the proof given by GPT-5.

   • GPT-5 uses both k and r to denote the size of the optimal set OP T , which is unnecessary
     and confusing. Interestingly, both k and r are introduced by the same line (just before the
     section of the algorithm in the response), but the equality between them is explained again
     just before Section A of the analysis.

   • The given algorithm makes r iterations even though the presence of two matroids means that
     there might not be any elements that can be selected after r/2 iterations (which would make


                                                  29
     the algorithm crash). Fixing that requires either replacing the upper bound of the for loop
     with r/2, or replacing the for loop with an appropriate while loop.

   • Since there are two matroids, a set Mi of size r − i + 1 with the properties required by the
     algorithm may not exist.

   • The definition
                                    Ψi (u) := {g1 (u), g2 (u)} ∩ OP Ti .
     is somewhat amusing since the ranges of both g1 and g2 are OP Ti , which makes the intersec-
     tion with this set completely unnecessary.

   • The inequality (2) is wrong. It would have made sense if the elements of Ψi (u) could replace
     u in Mi , but the definition of Ψi (u) actually says the opposite, namely, u can replace the
     elements of Ψi (u) in OP T . Furthermore, the division by |Ψi (u)| in this inequality seems to
     have no justification at all.

   • GPT justifies Inequality (3) using the argument: “the last step uses that every v ∈ OP Ti
     appears in at least one Ψi (u) (if g1 (u) = v or g2 (u) = v).” We believe this argument is correct,
     but it is not something that is easy to see. Moreover, both this inequality and Inequality (2)
     seem to be putting effort in the wrong direction since the stronger result that the left hand
     side of (3) upper bounds the right hand side of (3), even without the coefficient of 1/2, follows
     immediately from the maximality of the set Mi .

   • In Inequality (9), GPT-5 has “forgot” an error term of −1/k.
                                                                                    2
                                                                                   γ
   • GPT claims that “When there is only one matroid, our proof specializes to γ+1      , matching
     the paper’s guarantee.” We are not sure that this sentence is correct. However, as this is
     somewhat of an intuitive statement, its correctness is open for interpretation.

   • GPT-5 claims that one can get a better result using contention resolution schemes. However,
     for the best of our knowledge, no such scheme is known for weakly submodular functions.


Conclusion
We evaluated GPT-5 on five conjectures of varying difficulty. The sample is small, so our findings
are indicative rather than definitive. Based on our observations, several patterns emerge.

   • When a single path of argument sufficed, GPT-5 performed well: in three of five cases it
     produced a nearly correct proof.

   • GPT-5 often adapts existing proofs in a way that is broadly correct, but somewhat lazy:
     it tends to omit steps that carry over unchanged from the source, and it clings closely to
     the original structure even when alternative approaches might be more natural. This kind
     of shortcut resembles how a human might minimize effort by avoiding repeating unchanged
     arguments.

   • The model failed on Problems 4 and 5, both of which required combining insights from at
     least two papers; forming such cross-paper connections remains a main obstacle.




                                                  30
  • Interestingly, for Problem 5, GPT-5 proposed the same algorithm we had in mind, but failed
    to analyze it correctly. Upon reviewing its response, we realized that while an interesting
    approximation guarantee may indeed be provable, establishing such a result appears to be
    more challenging than we have initially thought.

  • Relative to prior model generations, we observe clear improvement in baseline mathematical
    competence and occasional originality. We are cautiously optimistic that, within a few years,
    models may make more systematic and meaningful connections across proof techniques.

  • Better and interactive prompting may further improve results. Our setup used only a short
    prompt and one or two source papers. Even under these minimal conditions, the model
    consistently understood the questions and nearly solved a majority of the problems.


References
[1] Andrew An Bian, Baharan Mirzasoleiman, Joachim M. Buhmann, and Andreas Krause. Guar-
    anteed non-convex optimization: Submodular maximization over continuous domains. In Aarti
    Singh and Xiaojin (Jerry) Zhu, editors, Proceedings of the 20th International Conference on
    Artificial Intelligence and Statistics, AISTATS 2017, 20-22 April 2017, Fort Lauderdale, FL,
    USA, volume 54 of Proceedings of Machine Learning Research, pages 111–120. PMLR, 2017.

[2] Niv Buchbinder and Moran Feldman. Constrained submodular maximization via new bounds
    for dr-submodular functions. In Bojan Mohar, Igor Shinkar, and Ryan O’Donnell, editors,
    Proceedings of the 56th Annual ACM Symposium on Theory of Computing, STOC 2024, Van-
    couver, BC, Canada, June 24-28, 2024, pages 1820–1831. ACM, 2024.

[3] Lin Chen, Moran Feldman, and Amin Karbasi. Weakly submodular maximization beyond
    cardinality constraints: Does randomization help greedy? In Jennifer G. Dy and Andreas
    Krause, editors, Proceedings of the 35th International Conference on Machine Learning, ICML
    2018, Stockholmsmässan, Stockholm, Sweden, July 10-15, 2018, volume 80 of Proceedings of
    Machine Learning Research, pages 803–812. PMLR, 2018.

[4] Gruia Cualinescu, Chandra Chekuri, Martin Pál, and Jan Vondrák. Maximizing a monotone
    submodular function subject to a matroid constraint. SIAM J. Comput., 40(6):1740–1766,
    2011.

[5] Abhimanyu Das and David Kempe. Submodular meets spectral: Greedy algorithms for subset
    selection, sparse approximation and dictionary selection. In Lise Getoor and Tobias Scheffer,
    editors, Proceedings of the 28th International Conference on Machine Learning, ICML 2011,
    Bellevue, Washington, USA, June 28 - July 2, 2011, pages 1057–1064. Omnipress, 2011.

[6] Charles-Philippe Diez, Luı́s da Maia, and Ivan Nourdin. Mathematical research with gpt-
    5: A malliavin-stein experiment. arXiv preprint arXiv:2509.03065, 2025. Studying explicit
    convergence rates in Gaussian and Poisson settings using GPT-5.

[7] Moran Feldman and Alan Kuhnle.            Bicriteria submodular maximization.         CoRR,
    abs/2507.10248, 2025.

[8] Siddharth Mitra, Moran Feldman, and Amin Karbasi. Submodular + concave. In Marc’Aurelio
    Ranzato, Alina Beygelzimer, Yann N. Dauphin, Percy Liang, and Jennifer Wortman Vaughan,
    editors, Advances in Neural Information Processing Systems 34: Annual Conference on Neural

                                              31
    Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual, pages
    11577–11591, 2021.

 [9] Loay Mualem and Moran Feldman. Using partial monotonicity in submodular maximization.
     In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors,
     Advances in Neural Information Processing Systems 35: Annual Conference on Neural In-
     formation Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 -
     December 9, 2022, 2022.

[10] Richard Santiago and Yuichi Yoshida. Weakly submodular function maximization using local
     submodularity ratio. In Yixin Cao, Siu-Wing Cheng, and Minming Li, editors, 31st Interna-
     tional Symposium on Algorithms and Computation, ISAAC 2020, December 14-18, 2020, Hong
     Kong, China (Virtual Conference), volume 181 of LIPIcs, pages 64:1–64:17. Schloss Dagstuhl
     - Leibniz-Zentrum für Informatik, 2020.




                                              32
