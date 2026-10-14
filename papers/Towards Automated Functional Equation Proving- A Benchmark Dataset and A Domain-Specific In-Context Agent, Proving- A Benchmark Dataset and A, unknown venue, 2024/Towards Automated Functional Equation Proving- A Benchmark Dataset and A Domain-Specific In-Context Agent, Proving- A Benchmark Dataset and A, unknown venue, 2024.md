                                              Towards Automated Functional Equation
                                               Proving: A Benchmark Dataset and A
                                                 Domain-Specific In-Context Agent

                                        Mahdi Buali1[0009−0002−2376−8795] and Robert Hoehndorf1[0000−0001−8149−5890]

                                          Computer Science Program, Computer, Electrical, and Mathematical Sciences &
                                         Engineering Division, King Abdullah University of Science and Technology, Thuwal
arXiv:2407.14521v1 [cs.AI] 5 Jul 2024




                                                                       23955, Saudi Arabia
                                                        {mahdi.buali, robert.hoehndorf}@kaust.edu.sa



                                               Abstract. Automated Theorem Proving (ATP) faces significant chal-
                                               lenges due to the vast action space and the computational demands of
                                               proof generation. Recent advances have utilized Large Language Models
                                               (LLMs) for action selection in ATP, but these methods often require sub-
                                               stantial computational resources. This study introduces the Functional
                                               Equation Automated Solver (FEAS), an agent that builds on the CO-
                                               PRA in-context learning framework within the Lean environment. FEAS
                                               innovates by refining prompt generation and response parsing mech-
                                               anisms, integrating domain-specific heuristics for functional equations,
                                               and introducing the FunEq dataset—a rigorously curated collection of
                                               functional equation problems categorized into three difficulty levels. The
                                               agent’s performance is evaluated against established baselines using this
                                               dataset, demonstrating improvements in theorem proving accuracy, par-
                                               ticularly with the integration of functional equation-specific heuristics.
                                               Our results highlight the effectiveness of FEAS in generating and for-
                                               malizing high-level proof strategies into Lean proofs, emphasizing the
                                               potential of tailored approaches in domain-specific ATP challenges.


                                        1    Introduction

                                        Automated theorem proving (ATP) has long been a challenging endeavor in
                                        computer science [6]. Formalizing mathematics for efficient machine processing
                                        presents a significant hurdle, further complicated by the inherent infinite nature
                                        of the action space for proof construction. Interactive theorem provers (ITPs)
                                        like Lean [13], Coq [7], Isabelle [22], and HOL4 [18] offer a solution by facilitating
                                        formal proofs through user-guided application of tactics until the desired goals
                                        are achieved.
                                            Recent efforts have explored the use of Large Language Models (LLMs) as
                                        action selectors to address the vast action space in ATP [17] [5]. These approaches
                                        involve training LLMs from scratch [11] or fine-tuning pre-trained models [1] to
                                        generate plausible actions within the context of formal proofs. However, such
                                        methods often incur significant computational costs.
2         Buali & Hoehndorf

    In-context learning, exemplified by the COPRA agent [19], presents a promis-
ing avenue to overcome the computational bottleneck. This approach has demon-
strated success in other domains like machine translation and code generation
[14].
    Evaluating the capabilities of these algorithms may relies on challenging prob-
lems encountered in high school math Olympiads. The International Mathemat-
ical Olympiad (IMO) [8] represents the pinnacle of difficulty in this domain.
Notably, AlphaGeometry [20] recently achieved progress in automated theorem
proving for geometric problems using LLMs with a competitive performance
comparing to IMO participant. However, the field of functional equations, an-
other core topic within IMO’s algebraic domain involving finding all unknown
functions satisfying specific conditions, remains largely unexplored in the realm
of automated theorem proving.
    In this project, we build upon the foundation of the COPRA in-context learn-
ing agent [19], working specifically within the Lean environment, yet, expanding
evaluation to various general-purpose LLMs. Our key contributions include:

    – FunEq Dataset: We created the FunEq dataset 1 , a curated collection of
      functional equation problems formalized in Lean. This dataset spans three
      difficulty levels (simple, intermediate, hard), providing a rigorous benchmark
      for evaluating automated theorem provers in this domain. Hard problems are
      drawn from shortlisted IMO problems.
    – FEAS Agent: We introduce the FEAS agent2 , which refines COPRA’s
      prompt generation and response parsing mechanisms. FEAS instructs a LLM
      to produce high-level proof strategies in natural language, followed by their
      formalization and translation into Lean proofs. It adopts a robust block-
      based parsing strategy for error handling and backtracking.
    – Heuristic Integration: To enhance and stabilize FEAS’s performance, we
      explicitly incorporate domain-specific functional equation heuristics [3] di-
      rectly into the agent’s prompts.


2      Related Work

Deep learning has emerged as a promising approach to tackle the combinato-
rial explosion of the search space in automated theorem proving (ATP) [24] [2]
[4] [23]. The advent of Transformer-based language models revolutionized auto-
mated theorem proving by eliminating the need to explicitly hardcode the syntax
of interactive theorem provers (ITPs). GPT-f [17] pioneered this approach, uti-
lizing language models to generate novel proofs accepted into the Metamath [12]
library. PACT [5], a follow-up project, utilized self-supervised data to improve
tactic prediction in the Lean proof assistant. Further enhancements with expert
iteration [16] enabled autonomous curriculum learning, achieving state-of-the-art
1
    https://github.com/bio-ontology-research-group/FunEq.git
2
    https://github.com/bio-ontology-research-group/FEAS.git
                                                                     FEAS        3

performance on the miniF2F benchmark [26], a dataset of formal Olympiad-style
problems.
    Subsequently, Thor [10] integrated language models with Isabelle’s Sledgham-
mers [15] for premise selection, alleviating the need for explicit specification of
every proof step. Other work [9] leveraged this integration, employing in-context
learning for autoformalization and expert iteration to achieve improved results
on the MiniF2F benchmark. Concurrently, HTPS [11] explored the integration
of reinforcement learning with LLMs for guided proof search.
    Recent advances have sought to address the computational cost of LLM pre-
training. LLEMMA [1] continued pretraining Code Llama on mathematical data,
demonstrating capability in formal theorem proving. ReProver [25] focused on
premise selection using a retrieval-augmented approach, achieving success with
relatively modest computational resources.
    However, the computational burden of fine-tuning LLMs remained a concern.
COPRA [19] addressed this by employing general-purpose LLMs within an in-
context learning framework. This approach repeatedly queries a LLM to propose
tactics, leveraging feedback from the proof environment and retrieved lemmas
to refine subsequent queries. While COPRA outperformed several baselines, it,
like most prior works, generates proofs one tactic at a time, focusing on low-level
proof steps in comparison to human-like informal reasoning. Additionally, previ-
ous work primarily developed general solvers without leveraging domain-specific
knowledge, limiting their efficacy in specialized areas like functional equations.


3   The FunEq Dataset
We developed the FunEq dataset, a manually curated collection of functional
equation problems formalized in Lean. Our focus on functional equations is mo-
tivated by the fact that, while a specialized domain, their solutions necessitate
a diverse array of proof techniques. These range from basic algebraic manipula-
tions to sophisticated reasoning about concepts like continuity [21], providing a
rich testing ground for automated theorem provers.
    To accommodate varying levels of difficulty, FunEq is structured into three
categories:
Simple Dataset This dataset introduces 18 problems which require only fun-
   damental functional equation reasoning steps. Proofs primarily involve sim-
   ple substitutions, linear arithmetic, the use of involutions, straightforward
   induction, and basic case analysis.
Intermediate Dataset This dataset contains 15 problems which focuse on
   proving intermediate lemmas often encountered in the solution process of
   more complex functional equations such as establishing injectivity and sur-
   jectivity. Problems are sourced primarily from Evan Chen’s article [3] and
   the book “Functional Equations: A Problem-Solving Approach” by Venkat-
   achala [21].
Hard Dataset This dataset consists of most of the International Mathemat-
   ical Olympiad (IMO) shortlisted functional equation problems since 2002
4      Buali & Hoehndorf

    [8]. These problems, originally posed in the context of finding all functions
    satisfying given hypotheses, have been reformulated for Lean 3 by explic-
    itly stating the solutions as the goal state. This modification simplifies the
    problem representation compared to their original form in the competition.

4   The FEAS Agent
   Function FEAS(O, α):
       PUSH(st, O)
       for j ← 1 to t do
           if α = {} then
               p ← PROMPTIFY(st, Bad(O))
               α ← PARSETACTIC(LLM(p))
           end
           a ← POP(α)
           O′ ← T (O, a)
           if O′ = QED then
               terminate successfully
           else if O′ ∈ Err or ∃O′′ s.t. O′ ≡ O′′ then
               add a to Bad(O)
               α ← {}
           else
               FEAS(O′ , α)
           end
       end
       POP(st)
 Algorithm 1: Given an initial proof state (Oin ) and an empty queue of tac-
 tics (α), FEAS aims to find a sequence of tactics that transforms (Oin ) into
 the goal state (QED). Each proof state is either a set of obligations (goal-
 hypothesis pairs) or an error state. The agent utilizes a stack (st) to manage
 proof states, a failure dictionary (Bad(O)) to track unproductive tactics, and
 functions PROMPTIFY and PARSETACTIC to interact with an LLM. The algo-
 rithm proceeds by iteratively querying the LLM for tactics, applying them
 to the current proof state, and adjusting its search based on success, errors,
 or lack of progress as determined by a symbolic checker and the transition
 function (T (O, a)).
   The FEAS (Functional Equation Automated Solver) agent (Algorithm 1)
builds upon the foundation of the COPRA framework [19], specializing in the
domain of functional equations.

Prompt Engineering. FEAS introduces a key refinement in the system prompt
structure. Rather than directly soliciting a Lean proof step, FEAS guides a LLM
through a multi-stage response generation process. It prompts the LLM to first
articulate a high-level proof strategy in natural language, then formalize and
translate this strategy into a Lean-compatible proof.
                                                                      FEAS         5




Fig. 1: Example of FEAS’s Prompting and Response Generation for a Functional
Equation Problem. (a) An example of domain-specific heuristic included in the
system prompt. (b) Natural language proof steps generated by the LLM in re-
sponse to the current proof state. (c) The corresponding Lean proof generated
by the LLM, segmented into blocks for error handling and parsing.


Multi-Block Parsing and Error Handling. FEAS adopts a dynamic block-
based parsing strategy to manage the multi-line Lean proofs generated by a
LLM. This strategy enhances robustness by dividing the generated proof into
logical blocks based on the underlying structure of Lean proofs. By processing
each block independently, FEAS can effectively isolate and recover from errors in
specific parts of the proof, potentially salvaging and utilizing valid proof segments
even if the overall proof generated by the LLM is not entirely correct.


Automatic Tactic Application. After either successful parsing of all blocks or
encountering an error, FEAS attempts the automatic application of the nlinarith
tactic — which can simplify proofs by automatically handling complex algebraic
manipulations that would otherwise need to be done manually. Successful ap-
plication incorporates this step into the proof, otherwise, it is omitted. This
provides automation and taps into the power of Lean’s built-in tactics.


Domain-Specific Heuristics. FEAS integrates functional equation heuris-
tics [3] directly into the system prompt alongside Lean syntax examples. These
heuristics encompass substitution-based simplification, techniques for proving
6        Buali & Hoehndorf


Algorithm        Few Shots         COPRA             FEAS         FEAS+Heuristics

GPT            50.0% (50.0%) 77.78% (77.78%) 80.56% (83.33%) 86.11% (94.44%)
Gemini        33.34% (38.89%) 52.78% (61.11%) 80.56% (88.89%) 88.89% (88.89%)
Claude           0% (0%)      83.33% (83.33%) 91.67% (100%) 86.11% (88.89%)
Llama3           0% (0%)         50.0% (50.0%) 75.0% (77.78%) 63.89% (66.67%)
Table 1: Performance comparison of pass@1 (pass@2) on the simple tier of FunEq
dataset

Algorithm            Few Shots     COPRA             FEAS         FEAS+Heuristics

GPT                   0% (0%)      0% (0%)      6.67% (13.33%)    10.0% (13.33%)
Gemini                0% (0%) 6.67% (6.67%) 10.0% (13.33%)         3.33% (6.67%)
Claude                0% (0%) 6.67% (6.67%) 13.33% (13.33%) 13.33% (13.33%)
Llama3                0% (0%)      0% (0%)         0% (0%)        6.67% (6.67%)
Table 2: Performance comparison of pass@1 (pass@2) on the intermediate tier
of FunEq dataset



bijectivity, exploitation of symmetry and involution, and the utilization of in-
duction over natural and rational numbers. This integration aims to guide the
LLM towards generating more relevant and successful proof strategies within
this specific problem domain.


5   Evaluation

We conduct a series of experiments to evaluate the performance of the FEAS
agent and the impact of incorporating domain-specific heuristics. Our evaluation
includes comparisons across four different LLMs: GPT-4 Turbo, Gemini-1.5-
Pro, Claude-3.5-Sonnet, and Llama3 70b. We evaluate FEAS agents against two
baselines: Few-Shots and COPRA, the original in-context learning agent, which
serves as points of comparison. We assess FEAS in two distinct configurations:
one with the integrated domain-specific functional equation heuristics and one
without.
    The experiments are performed on the simple and intermediate tiers of the
FunEq dataset. To gauge performance on more complex problems, we further
evaluate all agents on the A1 subset of the hard dataset, which consists of the eas-
iest shortlisted algebra problems from each corresponding IMO year. To control
for potential variability in LLM responses, we execute each experiment twice on
the simple and intermediate datasets. Due to computational resource constraints,
we limit our evaluation to a single run on the A1 subset.
                                                                      FEAS         7

    In all experiments, we impose a maximum limit of 60 LLM queries and a
timeout of 720 seconds. The LLMs are used with a temperature setting of 0,
prioritizing deterministic responses. Performance is assessed using Pass@1 and
Pass@2 metrics, representing success on the first and second attempts, respec-
tively. For the simple and intermediate datasets, Pass@1 is calculated as an
average of the results of the two runs.

5.1   Results
Tables 1 and 2 show our evaluation across the Simple and Intermediate tiers of
FunEq. All combinations of agents and LLMs fail to generate proofs on the Hard
tier of FunEq. On the Simple dataset, FEAS agents consistently achieves the
highest success rates across all evaluated LLMs. FEAS with integrated heuris-
tics on GPT and Gemini achieves the highest performance, demonstrating the
efficacy of domain-specific knowledge. However, Claude and Llama3, without
heuristics, shows superior performance on this dataset, suggesting that in cer-
tain LLM configurations, heuristics may misguide proof search.
     On the more challenging Intermediate dataset, the challenge increases sub-
stantially, with all approaches showing lower success rates. However, FEAS
agents again consistently ranks highest in performance, highlighting its ability to
navigate more complex functional equation proofs. Again, in some cases, Gem-
ini, FEAS performs better without heuristics. Furthermore, all methods fail to
generate proofs on the Hard tier of FunEq, indicating that significant challenges
remain in automated theorem proving for functional equations.

6     Conclusion
Our experiments establish the FEAS agent as an advancement in automated
theorem proving for functional equations. FEAS refines prompting, parsing, and
integration of domain-specific heuristics demonstrate improvement over base-
lines. While results on the Simple dataset are encouraging, performance on the
Intermediate and Hard datasets highlights the ongoing challenges in this complex
domain.
    Specifically, the challenges revealed by our evaluation can be decomposed
into two distinct sub-problems: (1) proposing mathematically useful proof steps,
and (2) accurately translating these high-level steps into the formal language
of the theorem prover. Each of these sub-problems poses its own complexities,
requiring distinct approaches for further improvement.
    Several avenues present themselves for future research. The development
of agents tailored to specific sub-tasks within the framework. Incorporating a
broader repertoire of high-level proof tactics within the LLM’s prompting could
improve the performance of generating Lean proof steps. Investigating search al-
gorithms beyond the currently employed depth-first search has the potential to
improve efficiency and solution discovery. Finally, designing efficient self-learning
mechanisms for FEAS would enable it to continuously refine its strategies based
on both successful and unsuccessful proof attempts.
8       Buali & Hoehndorf

References
 1. Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M.D., McAleer, S., Jiang, A.Q.,
    Deng, J., Biderman, S., Welleck, S.: Llemma: An open language model for mathe-
    matics. arXiv preprint arXiv:2310.10631 (2023)
 2. Blaauwbroek, L., Urban, J., Geuvers, H.: The tactician: A seamless, interactive
    tactic learner and prover for coq. In: International Conference on Intelligent Com-
    puter Mathematics. pp. 271–277. Springer (2020)
 3. Chen, E.: Introduction to functional equations (2016), https://web.evanchen.cc/
    handouts/FuncEq-Intro/FuncEq-Intro.pdf, accessed on: 08 May 2024
 4. Gauthier, T., Kaliszyk, C., Urban, J., Kumar, R., Norrish, M.: Tactictoe: learning
    to prove with tactics. Journal of Automated Reasoning 65(2), 257–286 (2021)
 5. Han, J.M., Rute, J., Wu, Y., Ayers, E.W., Polu, S.: Proof artifact co-training for
    theorem proving with language models (2022)
 6. Harrison, J., Urban, J., Wiedijk, F.: History of Interactive Theorem Proving, vol. 9,
    pp. 135–214. North Holland (12 2014). https://doi.org/10.1016/B978-0-444-51624-
    4.50004-6
 7. Huet, G., Kahn, G., Paulin-Mohring, C.: The Coq Proof Assistant : A Tutorial :
    Version 7.2. Research Report RT-0256, INRIA (Feb 2002), https://inria.hal.
    science/inria-00069918, projet COQ
 8. IMO: International mathematical olympiad official website, https://www.
    imo-official.org/, accessed: 08 May 2024
 9. Jiang, A., Staats, C.E., Szegedy, C., Rabe, M., Jamnik, M., Li, W., Wu, Y.T.:
    Autoformalization with large language models. NeurIPS (2022)
10. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Miloś, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers. Advances in Neural Information Processing Systems
    35, 8360–8373 (2022)
11. Lample, G., Lacroix, T., Lachaux, M.A., Rodriguez, A., Hayat, A., Lavril, T.,
    Ebner, G., Martinet, X.: Hypertree proof search for neural theorem proving. Ad-
    vances in neural information processing systems 35, 26337–26349 (2022)
12. Megill, N., Wheeler, D.: Metamath: A Computer Language for Mathe-
    matical Proofs. Lulu.com (2019), https://books.google.com.sa/books?id=
    dxqeDwAAQBAJ
13. de Moura, L., Kong, S., Avigad, J., van Doorn, F., von Raumer, J.: The lean theo-
    rem prover (system description). In: Felty, A.P., Middeldorp, A. (eds.) Automated
    Deduction - CADE-25. pp. 378–388. Springer International Publishing (2015)
14. OpenAI: Gpt-4 and gpt-4 turbo, https://platform.openai.com/docs/models/
    gpt-4-and-gpt-4-turbo
15. Paulsson, L.C., Blanchette, J.C.: Three years of experience with sledgehammer, a
    practical link between automatic and interactive theorem provers. In: Proceedings
    of the 8th International Workshop on the Implementation of Logics (IWIL-2010),
    Yogyakarta, Indonesia. EPiC. vol. 2 (2012)
16. Polu, S., Han, J.M., Zheng, K., Baksys, M., Babuschkin, I., Sutskever, I.: Formal
    mathematics statement curriculum learning (2022)
17. Polu, S., Sutskever, I.: Generative language modeling for automated theorem prov-
    ing (2020)
18. Slind, K., Norrish, M.: A brief overview of hol4. In: Mohamed, O.A., Muñoz, C.,
    Tahar, S. (eds.) Theorem Proving in Higher Order Logics. pp. 28–32. Springer
    Berlin Heidelberg, Berlin, Heidelberg (2008)
                                                                       FEAS         9

19. Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., Chaudhuri, S.: An in-context learning
    agent for formal theorem-proving (2024)
20. Trinh, T., Wu, Y., Le, Q., et al.: Solving olympiad geometry without human demon-
    strations. Nature 625, 476–482 (2024). https://doi.org/10.1038/s41586-023-06747-
    5, https://doi.org/10.1038/s41586-023-06747-5
21. Venkatachala, B.: Functional Equations A Problem Solving Approach. Prism
    (2002)
22. Wenzel, M., Paulson, L.C., Nipkow, T.: The isabelle framework. In: Mohamed,
    O.A., Muñoz, C., Tahar, S. (eds.) Theorem Proving in Higher Order Logics. pp.
    33–38. Springer Berlin Heidelberg, Berlin, Heidelberg (2008)
23. Wu, M., Norrish, M., Walder, C., Dezfouli, A.: Tacticzero: Learning to prove theo-
    rems from scratch with deep reinforcement learning. Advances in Neural Informa-
    tion Processing Systems 34, 9330–9342 (2021)
24. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assis-
    tants. In: International Conference on Machine Learning. pp. 6984–6994. PMLR
    (2019)
25. Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger,
    R.J., Anandkumar, A.: Leandojo: Theorem proving with retrieval-augmented lan-
    guage models. Advances in Neural Information Processing Systems 36 (2024)
26. Zheng, K., Han, J.M., Polu, S.: Minif2f: a cross-system benchmark for formal
    olympiad-level mathematics. arXiv preprint arXiv:2109.00110 (2021)
10     Buali & Hoehndorf

7     Appendix

7.1   Qualitative Analysis

theorem intermediate_funeq_2
(f : R → R)
(h_0 : ∀ x, f(x + 1) = f(x) + 1)
(h_1 : ∀ x, x ̸= 0 → f(1/x) = f(x)/x^2) :
∀ x, x ̸= 0 → f(1 + 1/x) = 1 + f(x)/x^2 :=
begin
    intro x,
    intro hx,
    have h_2 : f (1 / x + 1) = f (1 / x) + 1 := h_0 (1 / x),
    have h_3 : f (1 / x) = f x / x ^ 2 := h_1 x hx,
    rw h_3 at h_2,
    rw add_comm at h_2,
    nlinarith,
end
                            Listing 1.1: FEAS Proof

theorem intermediate_funeq_2
(f : R → R)
(h_0 : ∀ x, f(x + 1) = f(x) + 1)
(h_1 : ∀ x, x ̸= 0 → f(1/x) = f(x)/x^2) :
∀ x, x ̸= 0 → f(1 + 1/x) = 1 + f(x)/x^2 :=
begin
    intro x, intro hx,
    rw [h_0 (1 / x), h_1 x hx] at *,
    field_simp [hx],
    rw mul_comm at *,
    rw [←h_0 (1 / x), h_1 x hx] at *,
    rw [←h_0 (1 / x), h_1 x hx] at *,
    ring_nf,
end
                    Listing 1.2: COPRA Incomplete Proof

   To illustrate the distinct strengths of FEAS, we examine a specific functional
equation problem (intermediate funeq 2) where it succeeds while COPRA does
not. FEAS’ solution demonstrates its ability to generate high-level intermediate
proof steps using the have tactic, mirroring a human’s approach. This contrasts
with COPRA, which focuses solely on lower-level Lean tactics. FEAS’ strategy,
guided by the system prompt instruction to first generate a natural language
proof sketch, leads to a more human-readable and strategically structured proof.
   Furthermore, FEAS’ block-by-block parsing successfully handles errors within
individual proof blocks. While all three lines generated by the LLM contained
                                                                      FEAS       11

incorrect tactic applications, FEAS was able to isolate and utilize the correct
proof concepts within each block. This error recovery mechanism showcases the
robustness of FEAS’ parsing strategy.
   Interestingly, despite the LLM failing to suggest the final correct tactic (erro-
neously proposing exact h 2), FEAS’ automated application of the nlinarith
tactic successfully concludes the proof. This demonstrates the complementary
nature of FEAS’ high-level reasoning and the underlying theorem prover’s au-
tomated capabilities.
