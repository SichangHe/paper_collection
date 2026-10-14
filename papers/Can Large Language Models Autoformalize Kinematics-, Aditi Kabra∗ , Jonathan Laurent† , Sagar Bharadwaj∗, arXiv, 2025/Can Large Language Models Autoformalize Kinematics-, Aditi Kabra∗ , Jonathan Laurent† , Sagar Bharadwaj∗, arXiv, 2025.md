                                                   Can Large Language Models Autoformalize
                                                                 Kinematics?
                                                                              Aditi Kabra∗ , Jonathan Laurent† , Sagar Bharadwaj∗ ,
                                                                               Ruben Martins∗ , Stefan Mitsch‡ , André Platzer†
                                                                                    ∗ Carnegie Mellon University, Pittsburgh, USA
                                                                              † Karlsruhe Institute of Technology, Karlsruhe, Germany
                                                                                          ‡ DePaul University, Chicago, USA

                                                    {akabra, skalasib, rubenm}@cs.cmu.edu, jonathan.laurent@kit.edu, smitsch@depaul.edu, platzer@kit.edu


                                            Abstract—Autonomous cyber-physical systems like robots and         kinematics problems [9], [14], [15]. We find that, supported
arXiv:2509.21840v1 [cs.LO] 26 Sep 2025




                                         self-driving cars could greatly benefit from using formal methods     by few-shot prompting and parser feedback, OpenAI o3 has
                                         to reason reliably about their control decisions. However, before a   a top-5 accuracy of 70% (success rate on selecting the best
                                         problem can be solved it needs to be stated. This requires writing
                                         a formal physics model of the cyber-physical system, which is a       out of 5 attempts per benchmark). The main cause of failure
                                         complex task that traditionally requires human expertise and          is checker limitations for the most complex problems.
                                         becomes a bottleneck.                                                    Our benchmarks and pipeline are available as an online ar-
                                            This paper experimentally studies whether Large Language           tifact at https://doi.org/10.1184/R1/28934195. Evaluating aut-
                                         Models (LLMs) can automate the formalization process. A 20            oformalization of a physical system is challenging because
                                         problem benchmark suite is designed drawing from undergrad-
                                         uate level physics kinematics problems. In each problem, the
                                                                                                               every problem has many valid formal representations, and
                                         LLM is provided with a natural language description of the            conversely, models can be incorrect for many subtle reasons.
                                         objects’ motion and must produce a model in differential game         To automatically assess the semantic proximity of generated
                                         logic (dGL). The model is (1) syntax checked and iteratively          formal models to the original physics problem, we provide a
                                         refined based on parser feedback, and (2) semantically evaluated      checker that:
                                         by checking whether symbolically executing the dGL formula
                                         recovers the solution to the original physics problem. A success        1) performs symbolic execution over the generated formal
                                         rate of 70% (best over 5 samples) is achieved. We analyze                   model, examining whether the expected symbolic solu-
                                         failing cases, identifying directions for future improvement. This          tion to the original physics problem is recovered.
                                         provides a first quantitative baseline for LLM-based autofor-           2) ensures the model is not in stasis by requiring that a
                                         malization from natural language to a hybrid games logic with
                                                                                                                     minimum number of variables are mutated, indicating
                                         continuous dynamics.
                                            Index Terms—hybrid systems, synthesis, verification, counter-            they are subject to physical effects.
                                         example, large language models                                        Recovering the expected solution to the original natural lan-
                                                                                                               guage problem is a strong indication that the formalization
                                                                I. I NTRODUCTION                               models the problem correctly, though the checker may some-
                                                                                                               times reject answers that are in principle correct but missed
                                            Formal methods seem especially useful in the safety-critical       some implicit assumptions that the original solution made.
                                         but mathematically complex domain of cyber-physical systems              Autoformalization of physical models can have tremen-
                                         (CPSs), i.e., systems like robots and planes where discrete soft-     dous impact on reliable autonomy. Unlike in mathematics,
                                         ware interacts with the continuous dynamics of the real world.        validating a hypothesized CPS formalization is possible with
                                         However, a bottleneck preventing broader industry adoption            comparisons between real measurements and predicted mea-
                                         is the challenge of writing a formalization for these systems         surements during test runs [16]. Easy formalization would
                                         [22]. Unlike program verification, where a mathematically             allow every modular component to be modeled formally,
                                         meaningful object to verify already exists in the form of a           with all assumptions explicit. Verification could lead to safer
                                         program, for CPSs, we must first create a formal model of the         systems and synthesis could make control system design easier
                                         physical system and environment. This process is notoriously          while ensuring no edge cases are missed relative to the formal
                                         difficult, time-consuming, and error-prone.                           model.
                                            Can large language models (LLMs) help autoformalize
                                         physical systems? They have shown autoformalization abilities                                II. OVERVIEW
                                         for mathematics [13], [26] and CPS contracts [2], [19]. This             This section explains by example what the process of
                                         paper presents a first, experiment-focused exploration of the         autoformalizing a physics problem involves. Consider the
                                         ability of LLMs to autoformalize the underlying physics prob-         following physics question [9, problem 1.2], which will serve
                                         lems, faithfully preserving their exact continuous dynamics           as a running example:
                                         and discrete transitions in differential game logic (dGL) [20].            “A point traversed half the distance with a velocity
                                         We propose 20 benchmarks derived from hard undergraduate                   v0 . The remaining part of the distance was covered
      with velocity v1 for half the time, and with velocity        nondeterminism such as unpredictable environmental factors
      v2 for the other half of the time. Find the mean             or controller latency, a second, symmetric, adversarial player
      velocity of the point averaged over the whole time           (canonically called Demon) models the situation by resolving
      of motion.”                                                  nondeterminism with the goal to make Angel lose. Adversarial
      Solution: “vavg = 2v 0 (v1 +v2 )
                         2v0 +v1 +v2 ”                             dynamics are also useful for optimization problems, e.g.,
   The physical motion described here is hybrid, with con-         “choose the launch angle that minimizes drift”, which can be
tinuous dynamics (motion at velocity v0 , v1 , and finally v2 )    modeled as Angel and Demon competing to find this angle.
as well as discrete transitions (changing velocity under speci-       Having formalized the problem as a dGL hybrid game, we
fied conditions). Additionally, there are non-trivial conditions   next describe how symbolic execution enables a check for
describing when the discrete transitions happen. We seek to        whether the model aligns with the natural language question.
symbolically model this motion formally.                           For the fragment of dGL where most of the chosen benchmark
   A canonical way to express control problems is via hybrid       problems lie (loop-free, polynomial solutions), symbolic exe-
games [7], [25]. Hybrid games are commonly formalized in           cution is decidable and existing work [11] describes how to
two ways: via hybrid automata [7] and via logic [20]. In           perform it. Backwards symbolic execution over a game lets us
this paper, we target the logic formalization as it is closer      compute the conditions under which Angel (or dually, Demon)
to code, which LLMs have been more exposed to and trained          can win the game. For example, symbolic execution of the
for. Differential game logic (dGL) is a logic expressing two-      subgame ⟨Line 5⟩dvavg = x at the end of Model 1 evaluates
player hybrid games with a relatively complete axiomatization      to x = dvavg ∧ t = 2th ∧ x = 2dh which is precisely the
[20]. A detailed and gradual introduction can be found in the      weakest precondition starting from which Angel passes the
literature [21]. Model 1 shows an example of a dGL hybrid          tests of Line 5 and ends the game in a state where she wins.
game which formalizes the running example.                         Consider the precondition ϕ of Line 1 computed in this way.
                                                                   Angel should be able to win the game exactly when vavg is
Model 1 Running Example: Finding Mean Velocity
                                                                   set to the correct solution, i.e., vavg = 2v 0 (v1 +v2 )
                                                                                                             2v0 +v1 +v2 ↔ ϕ. Such
    setup 1     x := 0 ; dvavg := 0 ;
                 ′                                                a check is implemented using Z3 and Mathematica.
  phase 0 2       x = v0 , d′vavg = vavg ; dh := x ;
                                                                      Observe that even a minor modeling mistake can result in
                t := 0 ; x′ = v1 , d′vavg = vavg , t′ = 1 ;
                         
  phase 1 3                                                        this check failing. In fact, symbolically executing Model 1
                th := t ; x′ = v2 , d′vavg = vavg , t′ = 1 ;       reveals that it is actually equivalent to ⊤. It suffers from a
                          
  phase 2 4
transitions   5    ?t = 2th ; ?x = 2dh                             subtle exploit where Angel can always run each phase for 0
                                                                   time, in which case xavg = x = 0 regardless of what vavg
 win when     6    dvavg = x                                       is set to. The problem is that the model lets Angel choose
                                                                   the distance that the particle will travel, as her choice at
   In this game, a player (canonically called Angel) runs          Line 2 determines the value of half-distance dh , which in turn
physical dynamics per the problem specification, moving the        determines the distance that phases 1 and 2 must cover. The fix
point’s position x with velocity v0 in phase 0 on Line 2, with     is simple: the assignment dh := x on Line 2 should be turned
velocity v1 in phase 1 on Line 3, and with velocity v2 in phase    to a test ?dh = x. The automated check was able to catch
2 on Line 4). Angel is forced to transition between phases         this difference and is a strong signal of correctness, especially
under the exact conditions specified by the problem because        in combination with manual review. The automated checker
of tests (assertions) on Line 5. These assertions use auxiliary    has a second test to ensure the system is not in stasis, ruling
variables th to keep track of the time elapsed in phase 1, t to    out empty games that exploit the symbolic execution test by
keep track of time elapsed in phase 1 and phase 2 combined,        setting the win condition directly to the desired solution. For
and dh to keep track of half the distance covered. On Line 5,      this example, the second test checks via static analysis that at
test ?x = 2dh ensures that the first phase transition occurred     least two variables are written to, since any reasonable model
when half the distance was covered. The test ?t = 2th ensures      will at least modify the variables representing the particle’s
that the second transition happened at half the total run time     position and time. The checker is provided with the minimum
of phases 1 and 2. If Angel fails either test condition, she       number of variables that must be written to and the expected
immediately loses the game.                                        solution for every benchmark problem.
   Notice that there is a variable vavg representing average          Finally, we see the benefit of formal modeling when the
velocity, and Line 6 says that Angel will win the game             model with Line 2 corrected is still not equivalent to the
only if vavg was correct, as checked using auxiliary variable      expected solution. The problem is that the textbook solution
dvavg , which tracks the displacement covered by a particle        is correct only under some unstated assumptions: distance
traveling at vavg through all phases. The value that vavg must     d is non-zero, velocity v0 is positive, and v1 + v2 is also
hold for Angel to win matches the solution to the original         positive. Finally, Model 2, makes these assumptions. Under
problem, vavg = 2v    0 (v1 +v2 )
                    2v0 +v1 +v2 . In this example, there happens
                                                                   the assumptions of Model 2, Line 1, the modal formula from
to be no adversarial dynamics (Angel is the only player            Model 2, Line 2 to Line 7 is equivalent to 2v   0 (v1 +v2 )
                                                                                                                 2v0 +v1 +v2 . In
making decisions). However, in problems with adversarial           unverified or informal physics, subtle modeling glitches are
widespread. As a human, it is easy to neglect a measure                   “An object A starts from rest and travels a distance
zero case like dh = 0 during an intermediate calculation, but             d. For the first half of the distance, it travels with
formalization forces this case to be explicit.                            velocity v0. For the second half of the distance, it
                                                                          spends half the time traveling with velocity v1 and
Model 2 Repaired Model: Finding Mean Velocity                             half the time traveling with velocity v2. Another
  assum2 1 (dh > 0 ∧ v0 > 0 ∧ v1 + v2 > 0) →                              object B tracks A. Its motion has the same duration,
      setup    2    x := 0 ; dvavg := 0 ;                                 starting, and ending points as A, but it travels
                     ′                                                   with uniform velocity vavg. Let vavg remain a free
   phase 0     3      x = v0 , d′vavg = vavg ; ?dh = x ;
                                                                          variable.”
                    t := 0 ; x′ = v1 , d′vavg = vavg , t′ = 1 ;
                             
   phase 1     4
                                                                     The prompt also includes upto four solved examples. The
                    th := t ; x′ = v2 , d′vavg = vavg , t′ = 1 ;
                              
   phase 2     5                                                     returned formal model is passed to the KeYmaera X dGL
transitions    6    ?t = 2th ; ?x = 2dh                              parser for a syntax check.
 win when      7     dvavg = x
                                                                                                                                           Process parser output into
                                                                                          dGL         KeYmaera X Parser      Parser
                                                                                                                                                feedback string.
                                                                                          Formula        Feedback            Error
                                                                                                                                        Store (formalization, feedback)
   This example begins to demonstrate why formalizing a                                               if Parsing              dGL               Natural    History of
hybrid physical problem is not a simple translation task. Intro-                                     Successful               Formula         Language     Attempts and
                                                                                                                                           Specification   Feedback
ducing the right auxiliary variables, absent in the specification,                                                                      LLM: Revise Formalization
                                                                     Natural         LLM: Propose
is often necessary for a clean, tractable formalization. All the     Language        Formalization                 dGL                      Given Feedback
                                                                     Specification                                 Formula
pieces of the model must fit together precisely, e.g., even
                                                                                                                                                        Correct dGL
making a weak inequality strict can transform a correct model                                                                Check Successful          Formalization
                                                                                        Expected
into one admitting no runs [24]. Correctness requires careful                           Solution
                                                                                                       Semantic Checking

attention to the subtleties of the problem specification, e.g.,                                                               Check Failed               Incorrect
                                                                                                                                                       Formalization
benchmark problem 10 (available in the online artifact [10])
has one variable representing a displacement and another,
representing a distance. The former is a signed number while                                Fig. 1. Autoformalization pipeline
the latter must be modeled as non-negative. Models must prune
                                                                        If the syntax check fails, then the parser output is processed
mathematically degenerate cases using background knowledge
                                                                     into short feedback strings. An example of a parser feedback
of the physical world, e.g., by eliminating imaginary roots of
                                                                     string is
polynomials computing real quantities. Additionally, there are
many ways to model the same problem, and the right choice                  “The input formula contains an unsupported Uni-
of coordinate system or frame of motion can be crucial to                  code character (possibly {bad_char}). Use only
writing a model for which symbolic reasoning is tractable.                 ASCII characters.”
   Given the complexity of the task, it is unclear whether           Where bad_char is a parameter extracted from parser
LLMs can succeed at all, making a careful evaluation nec-            output. The incorrect formalization along with the feedback
essary. We create a benchmark suite drawing from textbooks           is then appended to a list of previous failed formalization
and problem sets [9], [14], [15], choosing tricky problems with      attempts.
varying structures to systematically identify the strengths and         The LLM is prompted to repair the formalization given
weaknesses of LLMs on autoformalization.                             past attempts and feedback using the Revise Formalization
                                                                     query. The prompt first provides up to two examples of repair.
                     III. M ETHODOLOGY                               Then it provides the natural language question, and finally
   The autoformalization system, shown by Fig. 1, takes as in-       past incorrect proposals along with the feedback indicating
put the natural language specification of the physical problem       why these proposals were wrong. The LLM replies with a
to model, and produces either a correct dGL formalization of         new, repaired dGL game, which is again passed to the parser
a failure (no formalization found that passed the checker). It       for checking. This syntactic repair loop is allowed to run at
uses two types of LLM queries: one is Propose Formalization,         most three times, after which autoformalization fails. A full
and the second one is Revise Formalization. The artifact [10]        implementation, along with examples, is available in the online
shows all the prompt templates used.                                 artifact [10].
   The autoformalization system first queries the LLM to pro-           If the syntax check succeeds, then the dGL formula is passed
pose the formalization using the Propose Formalization query,        onto the semantic evaluation system. This system takes as
providing up to four solved examples as part of the prompt. It       input the expected symbolic solution to the problem along
provides an LLM with the natural language description of the         with the proposed dGL formula. For our running example, the
problem and asks it to produce a dGL formula, including in           expected solution consists of the formula vavg = 2v   0 (v1 +v2 )
                                                                                                                        2v0 +v1 +v2 , to
the prompt common dGL syntax mistakes and their remedies.            test against for equivalence, and minimum expected number
An example of a problem description the prompt would use             of variables that are written to, 2. If the checker finds that
based on the running example is                                      the dGL formula is equivalent to the expected solution under
the initial assumptions of the formula and has enough variable
writes, then it declares that the formalization is acceptable. The                        20                                                         Outcome
pipeline is implemented using Delphyne [12] and KeYmaera X                                                                                                      Tool Failure
[6], which in turn uses Z3 [4] and Mathematica.




                                                                     Number of Problems
                                                                                                                                                                Timeout
                                                                                          15
                                                                                                                                                                Failed
                     IV. R ELATED W ORK                                                                                                                         Success

   Given a natural language description, formal physics models                            10
are generally written manually. Prior work has studied the
use of structured natural language to perform formalization
                                                                                          5
by rule-based transformations [1], [18], but this limits flexi-
bility in input specification. Recent progress in NLP (LLMs)
raises the prospect of automating formalization directly from                             0
                                                                                               4o         4o         4          4          O3      O3
unstructured natural language.                                                                      Ze         Mu .1 Ze .1 M
                                                                                                        ro-       lti-       r o        ult Zero Mult
                                                                                                                                           i-s          i
   The use of LLMs for autoformalizing mathematics has                                                      sh
                                                                                                               ot
                                                                                                                       sh
                                                                                                                          ot
                                                                                                                                 -sh
                                                                                                                                     ot        ho -sho -sho
                                                                                                                                                 t    t     t
received significant research attention [13], [26], including for
purely continuous systems with partial differential equation
[5], [8]. Recent work also uses LLMs to synthesize contracts         Fig. 2. Outcomes of autoformalization by GPT 4o, GPT-4.1 and o3, with
                                                                     zero-shot and multi-shot prompting.
for cyber-physical systems [2], [17], [19]. However, we focus
on LLM based autoformalization for physics models of hybrid            4o Zero-shot
systems, with discrete transitions and continuous dynamics            4o Multi-shot
faithfully represented, which to the best of our knowledge           4.1 Zero-shot
                                                                     4.1 Multi-shot
has not yet been studied. Compared to general mathematics
                                                                     O3 Zero-shot
and LTL specifications, we expect this domain to be more             O3 Multi-shot
data-scarce, with few examples of differential dynamic logic                                   1    2    3    4   5   6   7   8   9    10 11 12 13 14 15 16 17 18 19 20

system formalizations and even fewer examples of differential                                                                         Problem
game logic games available on the Internet. Additionally, we
expect CPS model formalization to have a more operational                                                    Fig. 3. Problem outcome by model.
flavor, modeling physical realities required to make a system
work rather than abstract concepts that can be simplified              3) Timeout: The solver timed out after 3 minutes of symbolic
for theoretical convenience (mathematics) or focused on only              execution. Symbolic execution uses real quantifier elim-
output behavior (LTL contracts). This difference makes it                 ination, which is doubly exponential [3], and can result
worth investigating the hybrid systems modeling domain.                   in timeouts.
                                                                       4) Tool Failure: The solver encountered an expression that it
                       V. E VALUATION                                     could not automatically symbolically execute (e.g., ODE
                                                                          with a square roots on the right hand side).
   We propose 20 benchmarks derived from challenging prob-
lems in undergraduate physics textbooks and problem sets                Fig. 2 shows the outcome. The autoformalization system is
[9], [14], [15]. The online artifact [10] lists them. Phrasing is    sampled five times independently with temperature 1, and the
changed to focus on modeling the physical situation described        best outcome is reported (where tool failure and solver timeout
in the problem (rather than on solving for a variable) and           are considered better than failure). For each sample, the LLM
the numbers are changed to induce rational answers to avoid          is given three chances to repair syntax if the KeYmaera X
failures of the automated check over numerical imprecision.          parser reported an error. We evaluate two different prompts,
Each benchmark is accompanied by an expected symbolic                one using few-shot prompting considering four examples
solution that the model should be equivalent to and the              (multi-shot) and another one without examples (zero-shot).
minimum expected number of variables that must be written               GPT 4o without few-shot prompting fails on every bench-
to. Four additional problems, separate from the benchmarks,          mark. Few-shot prompting significantly improves performance
serve as examples for few-shot prompting.                            for all models. With few-shot prompting o3 has a success
                                                                     rate of 70%, which is higher than GPT 4.1’s 45% and GPT
   We run the LLM autoformalization system using OpenAI
                                                                     4o’s 20%. Our results support that the improvements and the
GPT 4o, GPT 4.1 (best available OpenAI non-reasoning
                                                                     introduction of reasoning LLM models significantly increase
model) and OpenAI o3 (best available OpenAI reasoning
                                                                     their success rate on mathematical tasks, enabling strong
model) on the benchmark set, getting successively improving
                                                                     performance in the autoformalization of hybrid games.
results. Outcomes are classified into 4 buckets:
 1) Success: Correct, checker-certified formalization.                                                                VI. D ISCUSSION
 2) Failed: autoformalization failed either the syntax or se-          Fig. 3 shows the outcome of each problem by model. We
    mantic check.                                                    can observe that models found the same problems hard.
There are six problems that no model solves. For these, the         formally justified control decisions to respond to them. For
best performing model produces a formalization that could           such applications, where the physical environment must be
potentially be correct but is too complex for the checker to        formalized at runtime, the input to autoformalization would
verify. The problems can be classified into three groups that       be vision and sensor data rather than a natural language
explain where their complexity arises from.                         description. LLM autoformalization from such multimodal
  1) Optimization Problems: Problem 5 and 20.                       input data provides an interesting future research direction.
  2) Non-polynomial continuous dynamics: Problem 8 and 9.
  3) Complicated dynamics: Problem 13 and 15.                                                ACKNOWLEDGMENT
The first category, for example, includes problem 5, which is         This work was partially supported by the National Sci-
about identifying the launch angle of a boat that minimizes         ence Foundation (NSF) under Award Number CCF2427581,
drift, modeled by adversarial Angel trying to pick a better         DARPA under Agreement FA8750-24-9-1000, and by an
angle than Demon, who must set the optimal angle to win. The        Alexander von Humboldt Professorship.
interplay of the two players leads to combinatorial branching
over possible sequence of events, while continuous dynamics                                    AUTHORS ’ N OTE
occur under constraints preventing control blocking. These
constraints make symbolic reasoning about the differential             This is a pre-print. The definitive version of record appears
equations particularly computationally expensive.                   in the proceedings of FMCAD 2025 (https://fmcad.org), as:
   An example of the second category is problem 8, which is         Aditi Kabra, Jonathan Laurent, Sagar Bharadwaj, Ruben Mar-
about drones arranged in an equilateral triangle that cyclically    tins, Stefan Mitsch, André Platzer. “Can Large Language
pursue each other with constant radial velocity, collapsing         Models Autoformalize Kinematics?”, FMCAD 2025.
inwards in increasingly rapid revolutions, till they crash. Their
dynamics, often modeled with a non-polynomial square root                                        R EFERENCES
expression on the right side of an ODE, cannot be handled            [1] Gustavo Carvalho, Ana Cavalcanti, and Augusto Sampaio. Modelling
automatically by the tool. Problem 13 is an example from                 timed reactive systems from natural-language requirements. Formal
the third category. It has three phases of dynamics, including           Aspects of Computing, 28(4):725–765, 2016.
                                                                     [2] Yongchao Chen, Rujul Gandhi, Yang Zhang, and Chuchu Fan. NL2TL:
one where acceleration has a continuous dependence on time.              Transforming natural languages to temporal logics using large language
Such a differential equation is more expensive to symbolically           models. In Proceedings of the 2023 Conference on Empirical Meth-
evaluate, making a timeout the likely outcome.                           ods in Natural Language Processing, pages 15880–15903, Singapore,
                                                                         December 2023. Association for Computational Linguistics.
   Sometimes a problem fundamentally requires capabilities           [3] James H. Davenport and Joos Heintz. Real quantifier elimination is
that a solver lacks, and the solver must be extended. Other              doubly exponential. J. Symb. Comput., 5(1/2):29–35, 1988.
times a difficult but crucial part of formalizing problems is        [4] Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver.
                                                                         In C. R. Ramakrishnan and Jakob Rehof, editors, Tools and Algorithms
choosing the right abstractions and representations that let             for the Construction and Analysis of Systems, pages 337–340, Berlin,
proofs succeed. For the six failing problems, the solution likely        Heidelberg, 2008. Springer Berlin Heidelberg.
lies in a combination of these methods. The solver must be           [5] Mengge Du, Yuntian Chen, Zhongzheng Wang, Longfeng Nie, and
                                                                         Dongxiao Zhang. Large language models for automatic equation
extended to better automatically handle, for instance, non-              discovery of nonlinear dynamics. Physics of Fluids, 36(9), 2024.
polynomial dynamics by using continuous invariant generation         [6] Nathan Fulton, Stefan Mitsch, Jan-David Quesel, Marcus Völp, and
[23]. Complementing this, the LLM should be guided to use                André Platzer. KeYmaera X: An axiomatic tactical theorem prover for
                                                                         hybrid systems. In CADE, pages 527–538, 2015.
tricks like polar coordinates and auxiliary variables to rewrite     [7] Thomas A. Henzinger, Benjamin Horowitz, and Rupak Majumdar.
dynamics in friendlier forms, and to also provide checking               Rectangular hybrid games. In Proceedings of the 10th International
hints such as continuous invariants.                                     Conference on Concurrency Theory, CONCUR ’99, page 320–335,
                                                                         Berlin, Heidelberg, 1999. Springer-Verlag.
   Unsolved benchmarks provide a roadmap for improvement             [8] Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao, and Benyou
in both these directions. Additionally, the rapid improvement            Wang. LLMs for mathematical modeling: Towards bridging the gap
in success rate displayed by better LLM models suggests that             between natural and mathematical languages. In Luis Chiruzzo, Alan
                                                                         Ritter, and Lu Wang, editors, Findings of the Association for Computa-
autoformalization of hybrid games will continue to improve               tional Linguistics: NAACL 2025, pages 2678–2710, Albuquerque, New
with advancements in LLMs.                                               Mexico, April 2025. Association for Computational Linguistics.
                                                                     [9] I. E. Irodov. Problems in General Physics. Mir Publishers, 1988.
          VII. C ONCLUSION AND F UTURE W ORK                        [10] Aditi Kabra, Jonathan Laurent, Sagar Bharadwaj, Ruben
   This work experimentally studies the ability of LLMs to               Martins, Stefan Mitsch, and Andre Platzer.             Artifact for Can
                                                                         Large Language Models Autoformalize Kinematics?                    2025.
formally model physical behavior given a natural language                https://kilthub.cmu.edu/articles/software/Artifact for Can Large
specification. The results (70% success rate) are encouraging,           Language Models Autoformalize Kinematics /28934195.                DOI:
and suggest that CPS model autoformalization using LLMs                  10.1184/R1/28934195.
                                                                    [11] Aditi Kabra, Jonathan Laurent, Stefan Mitsch, and André Platzer.
could be an impactful direction for future research.                     CESAR: Control envelope synthesis via angelic refinements. In Bernd
   Beyond the broader adoption of formal methods in offline              Finkbeiner and Laura Kovács, editors, Tools and Algorithms for the
controller design, physics autoformalization enables a new               Construction and Analysis of Systems, volume 14570 of LNCS, pages
                                                                         144–164. Springer, 2024.
class of applications, where autonomous systems autoformal-         [12] Jonathan Laurent and André Platzer. Oracular programming: A modular
ize unfamiliar situations they face in the open world and derive         foundation for building llm-enabled software, 2025.
[13] Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Fan Yang, Xian Zhang,
     and Xiaoxing Ma. Autoformalize mathematical statements by symbolic
     equivalence and semantic consistency. In A. Globerson, L. Mackey,
     D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors,
     Advances in Neural Information Processing Systems, volume 37, pages
     53598–53625. Curran Associates, Inc., 2024.
[14] Samuel J. Ling, Jeff Sanny, and William Moebs. University Physics:
     Volume 1. OpenStax, Houston, TX, September 19 2016.
[15] MIT OpenCourseWare. 8.01SC Classical Mechanics Problem Set
     1.     https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/
     resources/mit8 01f16 pset1 new/, 2016. Fall 2016, undergraduate level.
[16] Stefan Mitsch and André Platzer. ModelPlex: verified runtime validation
     of verified cyber-physical system models. Formal Methods Syst. Des.,
     49(1-2):33–74, 2016.
[17] Daniel Neider and Rajarshi Roy. What Is Formal Verification Without
     Specifications? A Survey on Mining LTL Specifications, pages 109–125.
     Springer Nature Switzerland, Cham, 2025.
[18] Bruno Oliveira, Gustavo Carvalho, Mohammad Reza Mousavi, and
     Augusto Sampaio. Simulation of hybrid systems from natural-language
     requirements. In 2017 13th IEEE Conference on Automation Science
     and Engineering (CASE), pages 1320–1325, 2017.
[19] Jiayi Pan, Glen Chou, and Dmitry Berenson. Data-efficient learning
     of natural language to linear temporal logic translators for robot task
     specification. In 2023 IEEE International Conference on Robotics and
     Automation (ICRA), pages 11554–11561, 2023.
[20] André Platzer. Differential game logic. ACM Trans. Comput. Log.,
     17(1):1:1–1:51, 2015.
[21] André Platzer. Logical Foundations of Cyber-Physical Systems. Springer,
     Cham, 2018.
[22] Kristin Yvonne Rozier. Specification: The biggest bottleneck in formal
     methods and autonomy. In Sandrine Blazy and Marsha Chechik, editors,
     Verified Software. Theories, Tools, and Experiments, pages 8–26, Cham,
     2016. Springer International Publishing.
[23] Andrew Sogokon, Stefan Mitsch, Yong Kiam Tan, Katherine Cordwell,
     and André Platzer. Pegasus: Sound continuous invariant generation.
     Form. Methods Syst. Des., 58(1):5–41, 2022. Special issue for selected
     papers from FM’19.
[24] Yong Kiam Tan and André Platzer. Switched systems as hybrid
     programs**this research was sponsored by the afosr under grant number
     fa9550-16-1-0288. the first author was also supported by a *star, singa-
     pore. IFAC-PapersOnLine, 54(5):247–252, 2021. 7th IFAC Conference
     on Analysis and Design of Hybrid Systems ADHS 2021.
[25] Claire J. Tomlin, John Lygeros, and Shankar Sastry. A game theo-
     retic approach to controller design for hybrid systems. Proc. IEEE,
     88(7):949–970, 2000.
[26] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats,
     Mateja Jamnik, and Christian Szegedy. Autoformalization with large
     language models. In Proceedings of the 36th International Conference
     on Neural Information Processing Systems, NIPS ’22, Red Hook, NY,
     USA, 2022. Curran Associates Inc.
