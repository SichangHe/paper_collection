                                         Beyond Theorem Proving: Formulation, Framework
                                            and Benchmark for Formal Problem-Solving


                                                    Qi Liu, Xinhao Zheng, Renqiu Xia, Xingzhi Qi, Qinxiang Cao∗ , Junchi Yan∗†
                                                Sch. of Computer Science & Sch. of Artificial Intelligence, Shanghai Jiao Tong University
                                                    {purewhite,void_zxh,xiarenqiu,dennyqi123,caoqinxiang,yanjunchi}@sjtu.edu.cn
arXiv:2505.04528v1 [cs.AI] 7 May 2025




                                                          § https://github.com/Purewhite2019/formal_problem_solving_main


                                                                                            Abstract

                                                      As a seemingly self-explanatory task, problem-solving has been a significant com-
                                                      ponent of science and engineering. However, a general yet concrete formulation
                                                      of problem-solving itself is missing. With the recent development of AI-based
                                                      problem-solving agents, the demand for process-level verifiability is rapidly in-
                                                      creasing yet underexplored. To fill these gaps, we present a principled formulation
                                                      of problem-solving as a deterministic Markov decision process; a novel frame-
                                                      work, FPS (Formal Problem-Solving), which utilizes existing FTP (formal theorem
                                                      proving) environments to perform process-verified problem-solving; and D-FPS
                                                      (Deductive FPS), decoupling solving and answer verification for better human-
                                                      alignment. The expressiveness, soundness and completeness of the frameworks
                                                      are proven. We construct three benchmarks on problem-solving: FormalMath500,
                                                      a formalization of a subset of the MATH500 benchmark; MiniF2F-Solving and
                                                      PutnamBench-Solving, adaptations of FTP benchmarks MiniF2F and Putnam-
                                                      Bench. For faithful, interpretable, and human-aligned evaluation, we propose
                                                      RPE (Restricted Propositional Equivalence), a symbolic approach to determine
                                                      the correctness of answers by formal verification. We evaluate four prevalent FTP
                                                      models and two prompting methods as baselines, solving at most 23.77% of For-
                                                      malMath500, 27.47% of MiniF2F-Solving, and 0.31% of PutnamBench-Solving.

                                                                                             “In five minutes you will say that it is all so absurdly simple.”
                                                                                             — Sherlock Holmes
                                                                                                 Sir Arthur Conan Doyle, The Adventure of Dancing Men
                                        1       Introduction
                                        Problem-solving, encompassing facets such as computation, equation solving, and counter-example
                                        construction, is the key to superintelligence [1, 2, 3]. While large language models (LLMs) demon-
                                        strate remarkable capabilities in complex problem-solving [4, 5, 6, 7], their effectiveness is fun-
                                        damentally constrained by the lack of process-level verification mechanisms. Current approaches
                                        struggle to ensure the correctness of intermediate reasoning steps [8], as evidenced by the prevalence
                                        of flawed derivations and hallucination in model outputs [9]. More critically, training with these data
                                        will significantly reduce model capacity [10] and lead to incorrect learning [11].
                                        Formal theorem proving (FTP) [12] shows promise in process-level verifiability by generating
                                        machine-verifiable proofs. However, beyond proving propositions, more problems require solving
                                        unknowns. Pioneers [13, 14] enhance informal problem-solving with FTP to improve outcome-level
                                        correctness, but their solutions’1 process-level correctness are not guaranteed [15].

                                                ∗
                                                 Correspondence. † Also affiliated with Shanghai Artificial Intelligence Laboratory.
                                            1
                                                We use solution to refer to the reasoning steps and answer to the final answer.


                                        Preprint. Under review.
                      (a) Informal Problem-Solving                                   (b) Formal Problem-Solving (FPS)                             (c) Deductive FPS (D-FPS)

                                 Informal Problem                                                Formal Problem                                           Formal Problem
                  Let P(n) and S(n) denote the product and the sum,                  ∀ (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9) (h₁ : 0 ≤ b          ∀ (answer : ℕ) (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤
                  respectively, of the digits of the integer n. For example,         ∧ b ≤ 9) (h₂ : n = 10 * a + b) (h₃ : n = a * b          9) (h₁ : 0 ≤ b ∧ b ≤ 9) (h₂ : n = 10 * a + b)
                  P(23) = 6 and S(23) = 5. Suppose N is a two-digit number such      + a + b),                                               (h₃ : n = a * b + a + b),
                  that N = P(N)+S(N). What is the units digit of N?                  ∃ (answer : ℕ), answer = b                              ∃ (A : Prop), (answer = b)   A
Problem-Solving


                                     LLM             Prompt      Tool    Algorithm
                                                                                                      LLM       Formal Env.                                    LLM      Formal Env.
                                 Informal Solution                                               Formal Solution                                          Formal Solution
                   Step 1: Write down the equation given in the problem              simp only [h₀, h₁, h₂, h₃,                              Forward Solution
                   statement.
                                                                                     le_antisymm_iff, eq_self_iff_true,                      have h_eq : 10*a+b = a*b + a+b := by ...
                   N=P(N)+S(N)
                   Step 2: Use the values provided in the problem                    and_self_iff, true_and_iff]                             have h_simp : 9*a = a*b := by omega
                   statement to find the digits of P(N) and S(N).                    norm_num [h₀.1, h₀.2, h₁.1, h₁.2, h₂,                   have h_b_eq_9 : b = 9 := by nlinarith
                   For example, if N = 23, then P(N) = 6 and S(N) = 5.               h₃]                                                     have h_answer : answer = 9 := by ...
                   Step 3: Substitute the values found in Step 2 into the            norm_num at h₀ h₁ h₂ h₃ ⊢                               exact h_answer
                   equation from Step 1.
                                           Invalid Substitution                      refine ⟨?_,?_⟩
                   N=6+5
                                                                                     case h.refine_2 := by exact h₁                          Backward Proof
                   Step 4: Simplify the right-hand side of the equation.
                   N=11                                                              nlinarith                                               subst h_answer
                   Therefore, the units digit of N is 1.                                                                                     nlinarith
                     Direct Answer                                                    Direct Answer                                            Direct Answer
                                                1                                                           9                                                   answer = 9




                     (d) Informal Answer Checking                                                                (e) Formal Answer Checking by RPE
Answer Checking




                                    Direct Answer                                                     Direct Answer                                      Direct Answer
                              {x ∈ ℝ | 0 ≤ x ≤ 1}                                            {x : ℝ | 0 ≤ x ∧ x ≤ 1}                                     0 ≤ x ∧ x ≤ 1



                                   Sympy
                                               ×    String Matching
                                                                        ×                                                    Restricted Propositional
                                                                                                                                Equivalence (RPE)

                                     Ground-truth                                                     Ground-truth                                       Ground-truth
                                           [0, 1]                                           Set.Icc (0 : ℝ) (1 : ℝ)                           x ∈ Set.Icc (0 : ℝ) (1 : ℝ)




Figure 1: Advantages of Formal Problem-Solving (FPS) and Deductive-FPS (D-FPS). (a) Even with
sophisticated enhancements, LLMs may make reasoning flaws; (b) (c) FPS and D-FPS perform
process-level verified problem-solving inside formal theorem proving environments; (c) D-FPS
decouples answer deduction and validation to improve readability; (d) Informal answer checking
suffer from false negatives on complex objects; (e) Restricted Propositional Equivalence (RPE)
evaluates answers with symbolic heuristic in formal verification for stronger expressiveness.

A more fundamental question is, even under decades of debate [16], a rigorous definition of problem
and answer does not reach a consensus, not to mention the whole problem-solving process.
To fill the above gaps, we first define basic concepts and formulate problem-solving as a deter-
ministic Markov decision process from a formal verification perspective.
Based on the formulation, we propose FPS (Formal Problem-Solving), a framework for process-
verified problem-solving. The problem-solving process is implemented in existing FTP environments
by coupling metavariables and enforcing constructive proofs. For find-all problems, i.e., finding all
valid answers satisfying a certain proposition, we further propose D-FPS(Deductive FPS) to better
align with informal reasoning. D-FPS further restricts the answer into the proposition universe and
decouples the problem-solving process into a forward and backward stage: The forward stage derives
the answer step-by-step, prioritizing deductive reasoning; The backward stage verifies the correctness
of answers. The frameworks’ expressive, soundness, and completeness are proven.
A consequent challenge is evaluation. Some valid answers may misalign with human intuition. For
example, “limn→∞ n2 ” itself is a valid answer to “calculate limn→∞ n2 ”, but a human judge prefers
“0”. Existing informal answer checking methods, including exact match [17, 18, 19], Sympy [20, 6,
21], and relaxed match [22], fall short on complex math objects such a set {x ∈ R | 0 ≤ x ≤ 1}
and an interval [0, 1], not to mention formal objects such as Sec.Icc (0:R) (1:R). Model-based
methods [23] are also unsuitable for formal mathematics.
Therefore, we propose RPE(Restricted Propositional Equivalence), which determines the equiv-
alence between two answer terms by propositional equivalence with restricted proof automation.
Experiments validate RPE’s high human-alignment with 0.9732 Cohen’s kappa [24].
A long-standing gap between informal and formal math benchmarks is the task focus. Informal
ones focus on problem-solving with outcome-level correctness, while formal ones focus on theorem
proving with process-level correctness. To comprehensively evaluate FPS and D-FPS, and provide an
informal-formal parallel arena, we construct three benchmarks with formal problems and answers:


                                                                                                        2
FormalMath500, a formalized subset of the MATH500 [6] benchmark; MiniF2F-Solving and
PutnamBench-Solving: refactored subsets of FTP benchmarks MiniF2F [25] and PutnamBench [14].
Baseline experiments are conducted to analyze existing challenges and future directions. For FPS,
given its analogy to FTP, we evaluate 4 SOTA models under two main FTP paradigms: proof search
(InternLM2.5-StepProver [26], LeanSTaR [27]) and whole-proof generation (DeepSeek-Prover-
V1.5 [28], TheoremLlama [29]). For D-FPS, we evaluate direct in-context learning and Hybrid CoT
as baselines. We also provide intuitive parallel results between FPS and FTP. Highest solving rates
are 23.77% on FormalMath500, 27.47% on MiniF2F-Solving, and 0.31% on PutnamBench-Solving.
However, given ground-truth answers, the highest proving rates are 47.55%, 53.60%, and 1.54%,
respectively. This huge gap shows the difficulty of FPS and calls for more exploration.

2     Related Works
We omit related works about philosophy and answer checking to Appendix B for brevity.
AI Methods for Informal Reasoning. Recent works [30, 31] exhibit sparks to artificial general
intelligence (AGI), but complex reasoning and problem-solving tasks [32, 33, 34] remain challenging.
Various methods are exploited to address this gap, including prompt engineering [35, 36, 37], tool
augmentation [22, 38, 39], and pre-/post-training [40, 41, 42]. A recent trend is scaling not only at
training but also inference [5, 43], aided by verification engineering [44] and process supervision [6,
45, 46, 9], However, [47] highlights that existing verifiers remain domain-limited or yield false
positives. Therefore, we propose a neural-symbolic framework generalizable to well-defined problem-
solving tasks, ensuring process-verifiable reasoning.
AI Methods for Formal Reasoning. Built on foundations like dependent type theory [48], formal
theorem proving (FTP) environments such as Lean [49], Coq [50] and Isabelle [51] enable rigorous
proof verification. Current FTP methods can be roughly divided into two paradigms. Proof search [52,
53, 26, 54] constructs proofs step-by-step by transforming proof states. Whole-proof generation
methods generate full proofs in one shot, either directly from formal statements [55, 56] or translated
from informal proofs [57, 58, 59]. FTP environments work as oracle verifiers [47] but are limited
to proving known targets. Towards solving unknowns trustworthily, DTV [13] enhances informal
reasoning via autoformalization and formal proof verification. PutnamBench[14] pioneers in using
sorry placeholders to factor answers out of propositions, which enables agents to informally solve
first and formally prove later. Our work aims to implement the end-to-end problem-solving process -
including answer derivation, soundness/completeness proof, and correctness check — within FTP
environments, ensuring the entire reasoning chain is verified and the final answer is correct.
Benchmarks for Formal Reasoning. Benchmarks for FTP cover a broad spectrum of difficulty.
MiniF2F [25] comprises 488 propositions up to the high-school competition level. ProofNet [60]
comprises 374 propositions of undergraduate-level mathematics. FIMO [61] contains 149 IMO
shortlisted propositions. PutnamBench [14] consists of 644 propositions from undergraduate-level
competitions. Many propositions in MiniF2F and PutnamBench are constructed by concatenating
problems and answers, which can be refactored into MiniF2F-Solving and Putnam-Solving.

3     Formulations and Frameworks
Please refer to Appendix A for the background about FTP. In this section, we first present rigorous
definitions of problem and answer, and formulate the problem-solving processes as a deterministic
Markov decision process with a déjà vu to formal verification. Then, we propose FPS (Formal
Problem-Solving), a framework to encompass problem-solving processes inside existing TP environ-
ments. In FPS, the resulting solutions are process-verified, and the soundness of answers is ensured.
For find-all problems, deductive solving is usually more human-readable. We further propose D-FPS
(Deductive FPS), decoupling solving and verification to enhance deductive reasoning.

3.1   Definitions and Formulations of Problem-Solving

Consider the following problems (more examples and formalizations are in Appendix E.1):
1. Yes-no question: Does there exist a positive real number α s.t. [αn ] − n is even for all n ∈ N+ ?
2. Equation: Solve x ∈ R s.t. x2 − 1 = 0.


                                                  3
3. Calculation: Calculate limn→∞ n2 .
                            √     √      √
4. Simplification: Simplify 28x · 15x · 21x.
                                                             n
5. Counter-example construction: Find a Fermat number Fn = 22 + 1 which is not prime.
All of them consist of variables (including a queried variable), hypotheses, and conclusions that
the answer must satisfy. More generally, all elementary questions (whether-questions and which-
questions) [62] can be expressed in this form [3]. Their answers are terms (e.g., numbers and
functions) that depend on variables defined before the queried variable. Formally,
                                              Vp          Vq
Definition 3.1. A problem P (â) = (∀ni=1 vi , i=1 ϕi → i=1 ψi )[a 7→ â] is a predicate2 that maps
a direct answer â to a proposition. P is composed of (V, a, Φ, Ψ), where
• Independent variables V = {vi }ni=1 is the set of variables independent to a;
                                                                     Vp       Vq
• Queriable3 a is the queried variable that occurs free in ∀ni=1 vi , i=1 ϕi → i=1 ψi ;
• Hypotheses Φ = {ϕi }pi=1 is the set of propositions that depend on V (whose all free variables are
  included in V ), consisting of conditions that can be used to deduce the answer.
• Conclusions Ψ = {ψi }qi=1 is the set of propositions which depend on V ∪ {a}, consisting of
  conclusions that should be satisfied.
Definition 3.2. A direct answer is a term â which depends on V .
To avoid vacuous discussions of insolvable problems and following [62], we presuppose the problems
under discussion to be satisfiable.
Assumption 3.3. A problem is presupposed to be satisfiable, i.e., the following propositions hold.
                                               p
                                               ^          q
                                                          ^
                                    ∀ni=1 vi ,   ϕi → ∃a,    ψi                                 (1)
                                                       i=1             i=1

“Solving a problem” is essentially delineating two requirements: 1) Finding a direct answer â; 2)
Proving P (â). A step-by-step solution simultaneously finds a valid â and constructs a proof of P (â).
The queriable a is treated as a “hole”, which serves as a free variable and is finally filled with a
direct answer â. In a non-aftereffect manner, solution steps manipulate solution states, which consist
of all known conditions, target conclusions, and existing holes. When all holes are filled, and all
target conclusions are satisfied, the problem is successfully solved. Detailed discussions of reasoning
patterns in solution steps can be found in Appendix C. In this view, the problem-solving process can
be modeled as a deterministic MDP (S, A, P, R).
Definition 3.4. A solution state S = (H, G) ∈ S maintains unfilled holes and unproven goals.
• H is the set of unfilled holes, H = {(?hi , Vi , Φi )}si=1 , where ?hi is the placeholder of the i-th
  hole, Vi = {vi,j }nj=1
                      i
                         is a set of variables, Φi = {ϕi,j }pj=1
                                                              i
                                                                 is a set of hypotheses which depend on
  V and other holes. Notice that circular dependency of holes is not allowed.
• G is the set of unproven goals, G = {(Vi , Φi , Ψi )}ri=1 , where Vi = {vi,j }nj=1  i
                                                                                         is a set of vari-
  ables, Φi = {ϕi,j }j=1 is a set of hypotheses dependent on V and H, and Ψi = {ψi,j }qj=1
                        pi                                                                            i


  is a set ofVconclusionsVdependent on V and H. Each goal represents one proposition Pi =
               pi             qi
  ∀nj=1
     i
        vi,j , j=1 ϕi,j → j=1      ψi,j should be proven.
Definition 3.5. A solution step s ∈ A is a function s : (H, G) 7→ (H ′ , G′ ) that maps a solution state
(H, G) to (H ′ , G′ ) by manipulating holes and goals.
Given a problem with (V, a, Φ, Ψ), the initial solution state is ({?a, V, Φ}, {V, Φ, Ψ[a 7→?a]}). By
sequentially executing solution steps si in solution s = [si ]m    i=1 , the initial solution state is finally
transformed to the terminal state ({}, {}), where all holes are filled and all goals are proven, i.e.
({}, {}) = (sm ◦sm−1 ◦· · ·◦s1 )(({?a, V, Φ}, {V, Φ, Ψ})). A problem-solving agent can be rewarded
if the solution is successfully constructed, i.e., Rs (S, S ′ ) = IS ′ =({},{}) .

3.2        Formal Problem-Solving Framework

Readers familiar with formal theorem proving may feel an intense déjà vu: both theorem proving and
problem-solving can be modeled as a deterministic MDP, both proof states and solution states consist
      2
          ϕ[x 7→ t] represents substituting a term t for a variable x in a formula ϕ at the places where x occurs free.
      3
          We follow the terminology in [62], although our formulations differs.


                                                             4
                Formal Problem-Solving (FPS)                                                                 Deductive FPS (D-FPS)

                               Formal Problem                                                                      Formal Problem
             ∀ (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9) (h₁ : 0 ≤ b                                        ∀ (answer : ℕ) (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤
             ∧ b ≤ 9) (h₂ : n = 10 * a + b) (h₃ : n = a * b                                        9) (h₁ : 0 ≤ b ∧ b ≤ 9) (h₂ : n = 10 * a + b)
             + a + b),                                                                             (h₃ : n = a * b + a + b),
             ∃ (answer : ℕ), answer = b                                                            ∃ (A : Prop), (answer = b)   A
                    Initialize                                 Problem-Solving                      Initialize                               Problem-Solving
                                      State 0                                                     Forward State 0
                      goal h                         goal w
             a b n : ℕ                     a b n : ℕ                                           answer a b n : ℕ
             h₀ : 1 ≤ a ∧ a ≤ 9            h₀ : 1 ≤ a ∧ a ≤ 9                                  h₀ : 1 ≤ a ∧ a ≤ 9
             h₁ : 0 ≤ b ∧ b ≤ 9            h₁ : 0 ≤ b ∧ b ≤ 9                                  h₁ : 0 ≤ b ∧ b ≤ 9
             h₂ : n = 10 * a + b           h₂ : n = 10 * a + b                                 h₂ : n = 10 * a + b
                                                                                               h₃ : n = a * b + a + b
             h₃ : n = a * b + a + b        h₃ : n = a * b + a + b
                                                                                               h_answer : answer = b             Backward State 0
             ⊢ ?w = b                      ⊢ ℕ
                                                                                               ⊢ ?w                            answer a b n : ℕ
                                                simp [Nat.add_comm,                                                            h₀ : 1 ≤ a ∧ a ≤ 9
                                  Step 1        Nat.add_left_comm,                                                             h₁ : 0 ≤ b ∧ b ≤ 9
                                                                                             have h_equation : 10 * a
                                                Nat.add_assoc] at h₃ ⊢               Forward                                   h₂ : n = 10 * a + b
                                                                                             + b = a * b + a + b :=
                                                                                      Step 1
                                      State 1                                                by linarith                       h₃ : n = a * b + a + b
                                                                                                                               h_answer : answer = 9
                      goal h                        goal w                                                                     ⊢ answer = b
             ...                           ...                                                    Forward State 1
             h₁ : 0 ≤ b ∧ b ≤ 9            h₃ : n = a * b + a + b                              ...                                                      Backward
                                           ⊢ ℕ                                                                                    subst h_answer
             h₃ : n = a * b + a + b                                                            h_equation : 10 * a + b                                   Step 1
             h₃ : n = a + (b + a * b)                                                          = a * b + a + b
             ⊢ ?w = b                                                                          ⊢ ?w                              Backward State 1
                                                                                                                               a b n : ℕ
                           Step 2 ~ m-2                  ...                         Forward                                   h₀ : 1 ≤ a ∧ a ≤ 9
                                                                                       Step            ...                     h₁ : 0 ≤ b ∧ b ≤ 9
                                    State m-2                                        2 ~ m-1                                   h₂ : n = 10 * a + b
         goal h.refine_1          goal h.refine_2               goal w                          Forward State m-1              h₃ : n = a * b + a + b
      ...                      ...                     ...                                     ...                             ⊢ 9 = b
      h₁ : 0 ≤ b ∧ b ≤ 9       h₁ : 0 ≤ b ∧ b ≤ 9      h₃ : n = a * b + a + b                  h_answer : answer = b
      h₁ : b ≤ 9               h₁ : b ≤ 9              ⊢ ℕ                                     h_simplified : 9 * a = a                                 Backward
                                                                                                                                    nlinarith
      ⊢ ?w ≤ b                 ⊢ b ≤ ?w                                                        * b                                                       Step 2
                                                                                               h_b_eq_9 : b = 9                  Backward State 2
                                                                                               h_answer : answer = 9
                                                case h.refine_2 := by
                                Step m-1                                                       ⊢ ?w                                    No goals
                                                       exact h₁
                                    State m-1                                        Forward
                                                                                                  exact h_answer
                   goal h.refine_1                 assignment                        Step m
              ...                           ?w : ℕ = 9                                            Forward State m
              ⊢ 9 ≤ b                                                                                 assignment
                                                                                               ?w : Prop = (answer = 9)

                                  Step m              nlinarith

                                      State m                                                                      Extract
                                      assignment
                               ?w : ℕ = 9
                                                                                                                                                   Results
                                                                                                     Direct Answer
                     Extract
                                                                    Results                          answer = 9                   Soundness Proof
                                                                                                                                 answer = 9 implies
                  Direct Answer                Soundness Proof                                     Completeness Proof            ground-truth answer
                                             9 is one of the ground-                               Ground-truth answer
                           9                      truth answers                                    satisfy answer = 9




Figure 2: Demonstrations of FPS and D-FPS. FPS: After initialization, an agent iteratively executes
solution steps to transform solution states until all goals are solved. A direct answer and its soundness
proof can be extracted. D-FPS: The whole process is further decoupled into a forward-solving part
and an optional backward-proving part. Forward-solving enforces deductive reasoning for better
human readability. The direct answer and the completeness proof can be extracted upon finishing
forward-solving, while the soundness proof should be extracted after finishing backward-proving.
of goals to prove and holes to fill, and both tactic applications and solution steps transform the states
towards the terminal state. Based on these parallels, we implement the problem-solving processes
in the FTP environment Lean 4 for its maturity and popularity. Similar implementations are also
available in other environments, e.g., Coq, where more convenient eexists and evar can be used.
Problems. The theory foundation of Lean 4 is dependent type theory [63]. Therefore, for problem
(V, a, Φ, Ψ), P should be rewritten in Lean 4 as
                      P (â) = (∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (∧qi=1 ψi ))[a 7→ â]
Prop. 1 should be rewritten as
                            ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∃(a : Ta ), ∧qi=1 ψi               (2)
where Ti is the type of the independent variable vi , Ta is the type of the queriable a, and dependent
type notations are omitted for brevity.
Problem-Solving. Sec. 3.1 concludes the essence of problem-solving as finding a direct answer â
and a proof for P (â). These two targets can be further summarized as finding a constructive proof
(w.r.t a) of Prop. 2. We name this framework as FPS (Formal Problem-Solving) in line with formal
theorem proving (FTP). A demo is in Fig. 2 (left), where
• Initialization. The Lean 4 environment is initialized with Prop. 2. Then, variables in V and
  hypotheses in Φ are introduced. The queriable a is split as a metavariable ?w by apply Ex-
  ists.intro. ?w is coupled [64, 65] with the main goal h to prevent non-constructive proofs4 and
   4
     The logical foundation of Lean, calculus of construction, follows intuitionistic logic and rejects non-
constructive axioms, e.g., the axiom of choice and the law of excluded middle. However, Lean assumes the
axiom of choice (and subsequently admits the law of excluded middle) to facilitate proving.


                                                                                 5
   facilitate answer extraction while maintaining semantics. Lean code and generic initial proof states
   are in Appendix D.1. The resulting initial solution state is State 0.
 • Solving. The solution states and solution steps are implemented as proof states and tactic appli-
   cations in Lean 4. To solve a problem, starting from State 0, an agent iteratively interacts with
   Lean 4, manipulating the solution states. The terminal state State m consists of no unsolved goals.
   Once the agent finds a sequence of tactics s = [si ]m
                                                       i=1 which transforms State 0 to State m, the
   problem is successfully solved with the formal solution s.
 • Extraction. Once the problem-solving succeeds, we extract the direct answer â from the metavari-
   able assignments in Lean kernel.
Theorem 3.6. (Proof in Appendix F.1) FPS is sound: for any problem P and direct answer â resulted
from FPS, P (â) holds.
Discussion. There are two main types of problems. Find-one problems are problems requiring
one valid answer, e.g., counter-example construction. Find-all problems require finding all valid
answers (unique one or multiple candidates), e.g., equation solving and computation. For find-all
problems, FPS does not need a “completeness theorem” but ensures that all answers are found
by proper formalization. For example, a multiple-answer problem
                                                              Vq      with ground-truth answer set
ā can be formalized
              Vq     as  (V, (a : Set Tx ), Φ, {a = {x : Tx |  i=1 ψ i }}) or (V ∪ {(x : Tx )}, (a :
Set Tx ), Φ, { i=1 ψi ↔ x ∈ a}) (neither a nor x occurs free in Φ).
The intense affinity between FPS and FTP is a double-edged sword. It allows direct application of
existing FTP methods without fine-tuning. However, it inherits the flexibility from FTP, which allows
mixed forward-backward reasoning and the “guess-then-check” paradigm. For find-one problems,
this framework works well. For find-all problems, humans usually prefer deductive and declarative
reasoning processes [66, 67, 68].
3.3       Deductive Formal Problem-Solving Framework
To force deductive solving for find-all problems, we focus on a “subset” of FPS, namely D-FPS
(Deductive FPS), whose problems should satisfy:
• The queriable A lives in the universe of propositions, i.e., A : Prop;
• Ψ = {ψ ↔ A} and ψ only depends on V , i.e., A doesn’t occur free in ψ.
Theorem 3.7. (Proof in Appendix F.2) Regarding find-all problems, the expressiveness of D-FPS is
at least as strong as that of FPS.
A demo of D-FPS is in Fig. 2 (right), where
• Initialization. The proof state is initialized as in FPS. Then, the main goal h is explicitly split
   into a forward goal h.mp and a backward goal h.mpr with corresponding hypotheses introduced.
   We use forward state to refer to the goal h.mp and the hole ?w (usually omitted for brevity), and
   backward state to refer to the goal h.mpr. Code implementation and generic initial proof states are
   in Appendix D.2. The initial forward state is Forward State 0, and the initial backward state is
   Backward State 0.
• Solving. The problem-solving process is explicitly split into a forward-solving part and a backward-
   proving part. A problem-solving agent uses deductive reasoning to derive new conclusions in
   forward reasoning iteratively. If the agent simultaneously5 fills ?w and proves h.mp by a simple
   exact tactic, the forward-solving is finished. Then, it can early-exit or continue to finish the
   backward-proving part, i.e., proving h.mpr.
• Extraction. Once forward-solving succeeds, we extract the direct answer Â from the metavariable
   assignments in Lean kernel.
Theorem 3.8. (Proof in Appendix F.3) D-FPS is complete: for any find-all problem with ground-truth
Ā, for any direct answer Â resulted from D-FPS, the following assertion holds:
                                 ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Ā → Â
Theorem 3.9. (Proof in Appendix F.4) D-FPS is sound: for any find-all problem with ground-truth
Ā, for any direct answer Â resulted from D-FPS, if the backward-proving is finished, it holds:
                                   ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Â → Ā
      5
    Otherwise, after ?w is filled by Â, the target of the forward state is concretized as Â. Hence, tactics of
backward reasoning can be applied to this goal.


                                                       6
4     Evaluation
In this section, we first define the correctness of formal answers. Then, we propose RPE (Restricted
Propositional Equivalence), which determines the correctness of direct answers by propositional
equality with restricted proof automation. Finally, for a comprehensive evaluation, we construct three
benchmarks, FormalMath500, MiniF2F-Solving, and PutnamBench-Solving, whose difficulty
ranges from grade school math to undergraduate competitions.

4.1   Metric
Correctness. Even though the soundness (and completeness, for find-all problems) of answers
resulting from FPS and D-FPS are formally verified, shortcuts still exist. For example, one can cheat
FPS by directly constructing answer terms based on the problem predicate or by separately proving
Prop.
Vq 2 and applying the axiom of choice to it. For D-FPS, one may assign the answer hole with
  i=1 ψi itself to form a tautology. Therefore, the correctness of an answer should not only be sound
(and complete) but also aligned with human preference.
Definition 4.1. A direct answer â for problem (V, a, Φ, Ψ) is correct if: 1) P (â) holds; 2) Answering
(V, a, Φ, Ψ) with â aligns with human intuition.

Restricted Propositional Equivalence. We design RPE (Restricted Propositional Equivalence)
to automatically, flexibly, and faithfully model correctness in human preference: Given a formal
problem (V, a,VΦ, Ψ), its ground-truth answer ā, and a direct answer â, RPE holds if and only if
                  p
∀ni=1 (vi : Ti ), i=1 ϕi , â = ā can be proven by restricted proof automation T .
The idea behind RPE is intuitive. Human preferences, e.g., simplicity and elegance, are too compli-
cated to model without prior. Fortunately, they can be captured in the human-annotated ground-truths.
Therefore, it is easier to determine whether a direct answer â is “human-aligned” by its “closeness”
to the ground-truth answer ā. For this purpose, Propositional equality [49], i.e., whether âV= ā can
                                                                                               q
be proven, is too broad. (e.g., They cannot discriminate aforementioned tautology answer i=1 ψi ).
Restricting this broadness by only allowing limited proof automation, the closeness can be faithfully
and flexibly modeled, as done in [69].
The restricted proof automation T includes the following. The code template is in Appendix D.3.
• rfl proves equalities up to definitional equality [49];
• norm_num prove equalities by normalizing numerical expressions;
• ring_nf proves equalities in commutative rings;
• rw_search proves equalities by repeatedly rewriting using lemmas in Mathlib 4 [70];
• aesop [64] is a symbolic heuristic that prioritizes normalizing and provability-preserving.
Validation of RPE. To fairly and comprehensively evaluate RPE, we uniformly sampled 300 ex-
amples from the test set of xVerify [23], each consisting of an informal problem, an informal
solution generated by a diverse group of SOTA LLMs, the ground-truth informal answer, and a
manually-annotated correctness label. We use xFinder [71] to extract informal answers from the
informal solutions and use DeepSeek-V3 [41] with 4-shot demonstrations to transform
                                                                             Vp       the informal
answers and corresponding ground-truths into RPE statements ∀ni=1 (vi : Ti ), i=1 ϕi , â = ā. (See
Appendix J.5 for detailed prompt)
RPE demonstrates strong alignment with human annotators, reaching 100% precision, 97.18% recall,
and 0.9732 Cohen’s kappa [24]. Case analysis of failures in this experiment and rejected answers in
the following experiments can be found in Appendix G.

4.2   Benchmarks
We construct three datasets with broad topics and diverse difficulty, each containing four fields:
informal problem, informal ground-truth answer, formal problem, and formal ground-truth answer.
See Appendix H for the processing details and Appendix E.2 for examples.
FormalMath500 is a formalized subset of the prevalent MATH500 benchmark [6], including 387
data points: 123 about Algebra, 92 about Intermediate Algebra, 62 about Number Theory, 65
about Prealgebra, and 45 about Precalculus. They cover a wide range of difficulties annotated
by [18]: 38 of Level 1, 67 of Level 2, 87 of Level 3, 96 of Level 4, and 99 of Level 5.


                                                   7
MiniF2F-Solving is a refactored subset of MiniF2F [25], which is composed of 488 propositions
up to high-school competition-level. We rewrite these propositions to fit in the FPS and D-FPS
framework, resulting in 375 data points with: 30 from AIME, 140 from MATH-Algebra, 82 from AMC,
3 from IMO, and 120 from MATH-Number Theory.
PutnamBench-Solving is a refactored subset of PutnamBench [14], which consist of 644 propositions
from undergraduate-level competitions. PutnamBench is a pioneer at using a sorry placeholder to
factor out the direct answers from problem propositions. After refactoring, the subset contains 324
data points with: 9 about Abstract Algebra, 138 about Algebra, 122 about Analysis, 14 about
Combinatorics, 28 about Geometry, 25 about Linear Algebra, 49 about Number Theory, 8
about Probability, and 4 about Set Theory. (One problem may cover multiple subjects.)

5         Experiments
In this section, we evaluate baseline methods for FPS and D-FPS on the three benchmarks. Given
FPS’s direct affinity to TP, we take two main TP paradigms, proof search and whole-proof generation,
as baselines. Moreover, to provide a side-by-side comparison with traditional TP, we evaluate these
methods’ proving capability by proving P (ā) (statement asserting the soundness of the ground-
truth answer). For D-FPS, due to its novel designs relative to traditional TP, we evaluate two
chain-of-thought prompting methods: direct in-context learning and hybrid CoT. Comprehensive
experiments are conducted to analyze existing obstacles and future directions thoroughly. Please refer
to Appendix K.1 for detailed hyperparameters and Appendix K.2 for Lean 4 environment settings.

5.1        Baseline Methods
Proof Search methods sequentially construct a formal proof t by best-first search: proof states Si
are nodes, tactics ti are edges, the terminal state “No goals” is the target node. Given an LLM
                                                    P    log pθ (tj | Sj )
pθ (ti | Si ), the normalized log-probabilities vi = j≤i       |tj |       is used as the value function.
In this paradigm, InternLM2.5-Step-Prover [26] and LeanSTaR [27] are evaluated.
Whole-Proof Generation methods perform conditional generation: Given a formal statement sf ,
an LLM p(t|sf ) directly models the distribution of the whole proof t. In this paradigm, DeepSeek-
Prover-V1.5 [29] and TheoremLlama [28] are evaluated.
In-Context Learning (ICL) constructs a forward formal solution by directly prompting DeepSeek-
V3 [41] with 10-shot demonstrations, each consisting of the original informal problem, the initial
forward state, and a ground-truth forward solution. The demonstrations are randomly sampled from
the MATH [18] train set, with 2 for each subject.
Hybrid Chain-of-Thought (Hybrid CoT) constructs a forward formal solution by alternatively
generating informal thoughts and formal solution steps to combine the flexibility of informal reasoning
and the rigor of formal verification. We conduct in-context learning on DeepSeek-V3 [41] with 10-
shot demonstrations identical to In-Context Learning. Those demonstrations are manually annotated
with aligned informal reasoning steps.

5.2        Results and Discussions
Experiment results are summarized in Table 1, where three indicators are reported:
• Solved. The portion of problems whose direct answers and proofs are successfully constructed and
  the direct answers are correct under RPE.
• Proven. The portion of problems for which the correctness of ground-truth answers P (ā) is proven.
  Proven and Solved compare proving a proposition and solving an unknown in parallel.
• NE-Submitted. The portion of problems whose direct answers and proofs are successfully
  constructed, but the direct answers are not equivalent to ground-truths under RPE.
Comparison between Solving and Proving. The best indicators between proof search and whole-
proof generation do not vary much. However, comparisons between Solved and Proven exhibit
consistently6 high discrepancies. SOTA methods can prove 47.55% of FormalMath500 and 53.60%
of MiniF2F-Solving. However, the highest solving rates are 23.77% and 27.47%, nearly half of
proving. We speculate that the vast difference stems from two extra requirements of problem-
      6
          The only exception is TheoremLlama, for which we have double-checked the experiments.


                                                        8
Table 1: Experiment results of baseline methods. Bold numbers highlight the best values for each
metric; Solved indicates the portion that is successfully solved; Proven indicates the portion whose
statements (asserting the correctness of ground-truth answer) are proven; NE-Submitted indicates the
portion of problems whose submitted answers are incorrect under RPE.
         Framework   Dataset        Method              Model             Solved↑   Proven↑   NE-Submitted↓
                                     Proof       InternLM2.5-StepProver   23.77%    47.55%       19.38%
                       Formal-       Search             LeanSTaR          23.51%    43.41%       20.93%
                       Math500
                                   Whole-Proof    DeepSeekProver-V1.5     22.22%    46.51%       14.47%
                                   Generation        TheoremLlama         16.02%    4.39%        15.50%
                                     Proof       InternLM2.5-StepProver   27.47%    50.67%       13.60%
         FPS           MiniF2F       Search             LeanSTaR          24.27%    49.33%       14.40%
                       Solving
                                   Whole-Proof    DeepSeekProver-V1.5     22.40%    53.60%       10.93%
                                   Generation        TheoremLlama         13.07%     7.73%       8.80%
                                     Proof       InternLM2.5-StepProver   0.00%     1.54%        28.09%
                     PutnamBench     Search             LeanSTaR          0.00%     0.93%        41.05%
                        Solving
                                   Whole-Proof    DeepSeekProver-V1.5     0.31%     1.54%        22.22%
                                   Generation        TheoremLlama         0.00%     0.31%        16.67%
                       Formal-        ICL            DeepSeek-V3          13.70%       -         0.00%
                       Math500     Hybrid CoT        DeepSeek-V3          15.50%       -         1.03%
         D-FPS         MiniF2F        ICL            DeepSeek-V3          21.87%       -         0.00%
                       Solving     Hybrid CoT        DeepSeek-V3          21.60%       -         0.00%
                     PutnamBench      ICL            DeepSeek-V3          0.00%        -         0.00%
                        Solving    Hybrid CoT        DeepSeek-V3          0.00%        -         0.31%

solving: continuously handling coupled metavariables [65] and deriving unknowns based on existing
conditions. This calls for future work in supervised fine-tuning (SFT) on problem-solving data.
Comparison between FPS and D-FPS. Methods under the D-FPS framework result in lower solving
capability than those under FPS. This meets our expectations since D-FPS has more constraints than
FPS and a larger gap to TP. Notably, D-FPS demonstrates significantly lower NE-Submitted than
FPS. This might be because existing models are pretrained or SFTed on TP data, which contains
severe inductive bias to construct an arbitrary term corresponding to the target type as the proof term.
However, FPS requires finding a correct term, which should not only be sound and complete but
also align with human intuition. A Venn graph of solved problems can be found in Appendix I.1,
where D-FPS shows a strong complementarity to FPS. Preference model experiments can be found
in Appendix I.2, where D-FPS demonstrates a clear advantage over FPS on human-alignment (avg.
> 0.75 on two preference models). Case studies of model-generated solutions are in Appendix I.4.
Nearly zero NE-Submitted rate of D-FPS depicts a promising picture of unsupervised problem-
solving: even without a ground-truth answer, perfect inference-scaling [47] with D-FPS can derive a
sound, complete, and human-aligned answer.
Comparison between Hybrid CoT and ICL. For D-FPS, Hybrid CoT demonstrates slightly better
solving capability than ICL, and other indicators hold statistically negligible differences. Error
analysis of Hybrid CoT and ICL can be found in Appendix I.3, which reveals that current LLMs’
underfitting on D-FPS might be the primary cause of their relatively low solving rate.
More discussions about limitations and potential future works are in Appendix L.

6   Conclusion
This paper aims to systematically answer two crucial and underexplored questions: what is problem-
solving, and how to conduct process-verified problem-solving. First, from a formal verification
perspective, we present rigorous definitions of problem, answer, an MDP formulation of the problem-
solving process, and the correctness of answers. In response to the second, we concretize the
definitions and encompass the “end-to-end” problem-solving process inside existing theorem proving
environments. We propose FPS (Formal Problem-Solving) framework for general problem-solving
and D-FPS (Deductive FPS) framework for more human-aligned solving find-all problems. Theorems
about their soundness, completeness, and expressiveness are proven. We also propose RPE (Restricted
Propositional Equivalence), a formal method for faithful, interpretable, and human-aligned evaluation
on answer correctness. We constructed three benchmarks, FormalMath500, MiniF2F-Solving, and
PutnamBench-Solving, covering wide subjects and difficulty range for comprehensive evaluation.
In 6 evaluated baselines, including SOTA FTP methods and general LLMs, at most 23.77% of
FormalMath500, 27.47% of MiniF2F-Solving, and 0.31% of PutnamBench-Solving are solved.


                                                        9
References
 [1] NeurIPS, “Announcing the neurips 2024 test of time paper awards,” 2024,
     accessed:    2025-01-13. [Online]. Available:          https://blog.neurips.cc/2024/11/27/
     announcing-the-neurips-2024-test-of-time-paper-awards/
 [2] D. Batens, “A formal approach to problem solving,” Computer modeling of scientific reasoning,
     pp. 15–26, 2003.
 [3] T. Nickles, “What is a problem that we may solve it?” Synthese, pp. 85–118, 1981.
 [4] DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang,
     X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue,
     B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai, D. Chen,
     D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Bao, H. Xu,
     H. Wang, H. Ding, H. Xin, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Wang, J. Chen, J. Yuan,
     J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang,
     K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang,
     M. Tang, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du,
     R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen,
     S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, S. Ye, T. Yun, T. Pei, T. Sun,
     T. Wang, W. Zeng, W. Zhao, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An,
     X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su,
     X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang,
     X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang,
     Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo,
     Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X.
     Zhu, Y. Xu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren,
     Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu,
     Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang,
     “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,” 2025.
     [Online]. Available: https://arxiv.org/abs/2501.12948
 [5] A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry,
     A. Beutel, A. Carney et al., “Openai o1 system card,” arXiv preprint arXiv:2412.16720, 2024.
 [6] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman,
     I. Sutskever, and K. Cobbe, “Let’s verify step by step,” arXiv preprint arXiv:2305.20050, 2023.
 [7] C. Snell, J. Lee, K. Xu, and A. Kumar, “Scaling llm test-time compute optimally
     can be more effective than scaling model parameters,” 2024. [Online]. Available:
     https://arxiv.org/abs/2408.03314
 [8] Z. Li, J. Sun, L. Murphy, Q. Su, Z. Li, X. Zhang, K. Yang, and X. Si, “A survey on deep
     learning for theorem proving,” 2024. [Online]. Available: https://arxiv.org/abs/2404.09939
 [9] C. Zheng, Z. Zhang, B. Zhang, R. Lin, K. Lu, B. Yu, D. Liu, J. Zhou, and J. Lin,
     “Processbench: Identifying process errors in mathematical reasoning,” 2024. [Online]. Available:
     https://arxiv.org/abs/2412.06559
[10] Z. Allen-Zhu and Y. Li, “Physics of language models: Part 3.3, knowledge capacity scaling
     laws,” 2024. [Online]. Available: https://arxiv.org/abs/2404.05405
[11] T. Ye, Z. Xu, Y. Li, and Z. Allen-Zhu, “Physics of language models: Part 2.2,
     how to learn from mistakes on grade-school math problems,” 2024. [Online]. Available:
     https://arxiv.org/abs/2408.16293
[12] K. Yang, G. Poesia, J. He, W. Li, K. Lauter, S. Chaudhuri, and D. Song, “Formal mathematical
     reasoning: A new frontier in ai,” arXiv preprint arXiv:2412.16075, 2024.
[13] J. P. Zhou, C. Staats, W. Li, C. Szegedy, K. Q. Weinberger, and Y. Wu, “Don’t trust: Verify–
     grounding llm quantitative reasoning with autoformalization,” arXiv preprint arXiv:2403.18120,
     2024.
[14] G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings, A. Thakur, and S. Chaudhuri,
     “Putnambench: Evaluating neural theorem-provers on the putnam mathematical competition,”
     arXiv preprint arXiv:2407.11214, 2024.


                                                10
[15] T. Lanham, A. Chen, A. Radhakrishnan, B. Steiner, C. Denison, D. Hernandez, D. Li,
     E. Durmus, E. Hubinger, J. Kernion, K. Lukošiūtė, K. Nguyen, N. Cheng, N. Joseph,
     N. Schiefer, O. Rausch, R. Larson, S. McCandlish, S. Kundu, S. Kadavath, S. Yang,
     T. Henighan, T. Maxwell, T. Telleen-Lawton, T. Hume, Z. Hatfield-Dodds, J. Kaplan, J. Brauner,
     S. R. Bowman, and E. Perez, “Measuring faithfulness in chain-of-thought reasoning,” 2023.
     [Online]. Available: https://arxiv.org/abs/2307.13702
[16] C. Cross and F. Roelofsen, “Questions,” in The Stanford Encyclopedia of Philosophy, Summer
     2024 ed., E. N. Zalta and U. Nodelman, Eds. Metaphysics Research Lab, Stanford University,
     2024.
[17] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek,
     J. Hilton, R. Nakano, C. Hesse, and J. Schulman, “Training verifiers to solve math word
     problems,” 2021. [Online]. Available: https://arxiv.org/abs/2110.14168
[18] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Stein-
     hardt, “Measuring mathematical problem solving with the math dataset,” arXiv preprint
     arXiv:2103.03874, 2021.
[19] Q. Li, L. Cui, X. Zhao, L. Kong, and W. Bi, “Gsm-plus: A comprehensive benchmark for
     evaluating the robustness of llms as mathematical problem solvers,” 2024. [Online]. Available:
     https://arxiv.org/abs/2402.19255
[20] A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone,
     C. Anil, I. Schlag, T. Gutman-Solo, Y. Wu, B. Neyshabur, G. Gur-Ari, and V. Misra,
     “Solving quantitative reasoning problems with language models,” 2022. [Online]. Available:
     https://arxiv.org/abs/2206.14858
[21] E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning, C. F. Olsson, J.-S. Denain,
     A. Ho, E. d. O. Santos et al., “Frontiermath: A benchmark for evaluating advanced mathematical
     reasoning in ai,” arXiv preprint arXiv:2411.04872, 2024.
[22] Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, M. Huang, N. Duan, and W. Chen, “Tora: A tool-
     integrated reasoning agent for mathematical problem solving,” arXiv preprint arXiv:2309.17452,
     2023.
[23] D. Chen, Q. Yu, P. Wang, W. Zhang, B. Tang, F. Xiong, X. Li, M. Yang, and Z. Li,
     “xverify: Efficient answer verifier for reasoning model evaluations,” 2025. [Online]. Available:
     https://arxiv.org/abs/2504.10481
[24] D. Philosophical Society of Washington (Washington, P. S. of Washington., and S. Institution,
     Bulletin of the Philosophical Society of Washington. Washington, D.C, Published by
     the co-operation of the Smithsonian Institution, [1874-, 1887, vol. v.10 (1887); Index
     v.1-10, p. 83, https://www.biodiversitylibrary.org/bibliography/46528. [Online]. Available:
     https://www.biodiversitylibrary.org/page/55377146
[25] K. Zheng, J. M. Han, and S. Polu, “Minif2f: a cross-system benchmark for formal
     olympiad-level mathematics,” 2022. [Online]. Available: https://arxiv.org/abs/2109.00110
[26] Z. Wu, S. Huang, Z. Zhou, H. Ying, J. Wang, D. Lin, and K. Chen, “Internlm2. 5-stepprover:
     Advancing automated theorem proving via expert iteration on large-scale lean problems,” arXiv
     preprint arXiv:2410.15700, 2024.
[27] H. Lin, Z. Sun, S. Welleck, and Y. Yang, “Lean-star: Learning to interleave thinking and
     proving,” 2025. [Online]. Available: https://arxiv.org/abs/2407.10040
[28] R. Wang, J. Zhang, Y. Jia, R. Pan, S. Diao, R. Pi, and T. Zhang, “Theoremllama:
     Transforming general-purpose llms into lean4 experts,” 2024. [Online]. Available:
     https://arxiv.org/abs/2407.03203
[29] H. Xin, Z. Z. Ren, J. Song, Z. Shao, W. Zhao, H. Wang, B. Liu, L. Zhang, X. Lu, Q. Du,
     W. Gao, Q. Zhu, D. Yang, Z. Gou, Z. F. Wu, F. Luo, and C. Ruan, “Deepseek-prover-v1.5:
     Harnessing proof assistant feedback for reinforcement learning and monte-carlo tree search,”
     2024. [Online]. Available: https://arxiv.org/abs/2408.08152
[30] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal,
     K. Slama, A. Ray et al., “Training language models to follow instructions with human feedback,”
     Advances in neural information processing systems, vol. 35, pp. 27 730–27 744, 2022.


                                                 11
[31] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee,
     Y. Li, S. Lundberg et al., “Sparks of artificial general intelligence: Early experiments with gpt-4,”
     arXiv preprint arXiv:2303.12712, 2023.
[32] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou, “Large language
     models cannot self-correct reasoning yet,” arXiv preprint arXiv:2310.01798, 2023.
[33] J. Xie, K. Zhang, J. Chen, S. Yuan, K. Zhang, Y. Zhang, L. Li, and Y. Xiao, “Revealing the
     barriers of language agents in planning,” arXiv preprint arXiv:2410.12409, 2024.
[34] I. Mirzadeh, K. Alizadeh, H. Shahrokhi, O. Tuzel, S. Bengio, and M. Farajtabar,
     “Gsm-symbolic: Understanding the limitations of mathematical reasoning in large language
     models,” 2024. [Online]. Available: https://arxiv.org/abs/2410.05229
[35] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou et al., “Chain-of-
     thought prompting elicits reasoning in large language models,” Advances in neural information
     processing systems, vol. 35, pp. 24 824–24 837, 2022.
[36] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou,
     “Self-consistency improves chain of thought reasoning in language models,” arXiv preprint
     arXiv:2203.11171, 2022.
[37] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflexion: Language agents
     with verbal reinforcement learning,” Advances in Neural Information Processing Systems,
     vol. 36, 2024.
[38] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig, “Pal: Program-
     aided language models,” in International Conference on Machine Learning. PMLR, 2023, pp.
     10 764–10 799.
[39] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer,
     N. Cancedda, and T. Scialom, “Toolformer: Language models can teach themselves to use
     tools,” Advances in Neural Information Processing Systems, vol. 36, pp. 68 539–68 551, 2023.
[40] Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer, A. Q. Jiang, J. Deng,
     S. Biderman, and S. Welleck, “Llemma: An open language model for mathematics,” arXiv
     preprint arXiv:2310.10631, 2023.
[41] DeepSeek-AI, A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang,
     C. Ruan, D. Dai, D. Guo, D. Yang, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao,
     G. Chen, G. Li, H. Zhang, H. Bao, H. Xu, H. Wang, H. Zhang, H. Ding, H. Xin, H. Gao, H. Li,
     H. Qu, J. L. Cai, J. Liang, J. Guo, J. Ni, J. Li, J. Wang, J. Chen, J. Chen, J. Yuan, J. Qiu, J. Li,
     J. Song, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Xu, L. Xia,
     L. Zhao, L. Wang, L. Zhang, M. Li, M. Wang, M. Zhang, M. Zhang, M. Tang, M. Li, N. Tian,
     P. Huang, P. Wang, P. Zhang, Q. Wang, Q. Zhu, Q. Chen, Q. Du, R. J. Chen, R. L. Jin, R. Ge,
     R. Zhang, R. Pan, R. Wang, R. Xu, R. Zhang, R. Chen, S. S. Li, S. Lu, S. Zhou, S. Chen, S. Wu,
     S. Ye, S. Ye, S. Ma, S. Wang, S. Zhou, S. Yu, S. Zhou, S. Pan, T. Wang, T. Yun, T. Pei, T. Sun,
     W. L. Xiao, W. Zeng, W. Zhao, W. An, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, X. Q. Li,
     X. Jin, X. Wang, X. Bi, X. Liu, X. Wang, X. Shen, X. Chen, X. Zhang, X. Chen, X. Nie, X. Sun,
     X. Wang, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yu, X. Song, X. Shan, X. Zhou, X. Yang, X. Li,
     X. Su, X. Lin, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. X. Zhu, Y. Zhang, Y. Xu, Y. Xu, Y. Huang,
     Y. Li, Y. Zhao, Y. Sun, Y. Li, Y. Wang, Y. Yu, Y. Zheng, Y. Zhang, Y. Shi, Y. Xiong, Y. He,
     Y. Tang, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Wu, Y. Ou, Y. Zhu, Y. Wang,
     Y. Gong, Y. Zou, Y. He, Y. Zha, Y. Xiong, Y. Ma, Y. Yan, Y. Luo, Y. You, Y. Liu, Y. Zhou, Z. F.
     Wu, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Huang, Z. Zhang, Z. Xie, Z. Zhang, Z. Hao,
     Z. Gou, Z. Ma, Z. Yan, Z. Shao, Z. Xu, Z. Wu, Z. Zhang, Z. Li, Z. Gu, Z. Zhu, Z. Liu, Z. Li,
     Z. Xie, Z. Song, Z. Gao, and Z. Pan, “Deepseek-v3 technical report,” 2024. [Online]. Available:
     https://arxiv.org/abs/2412.19437
[42] H. Luo, Q. Sun, C. Xu, P. Zhao, J. Lou, C. Tao, X. Geng, Q. Lin, S. Chen, and D. Zhang,
     “Wizardmath: Empowering mathematical reasoning for large language models via reinforced
     evol-instruct,” arXiv preprint arXiv:2308.09583, 2023.
[43] N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda,
     A. Liu, N. Dziri, S. Lyu, Y. Gu, S. Malik, V. Graf, J. D. Hwang, J. Yang, R. L. Bras,
     O. Tafjord, C. Wilhelm, L. Soldaini, N. A. Smith, Y. Wang, P. Dasigi, and H. Hajishirzi,
     “Tulu 3: Pushing frontiers in open language model post-training,” 2024. [Online]. Available:
     https://arxiv.org/abs/2411.15124


                                                   12
[44] X. Guan, Y. Liu, X. Lu, B. Cao, B. He, X. Han, L. Sun, J. Lou, B. Yu, Y. Lu et al., “Search,
     verify and feedback: Towards next generation post-training paradigm of foundation models via
     verifier engineering,” arXiv preprint arXiv:2411.11504, 2024.
[45] P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui, “Math-shepherd:
     Verify and reinforce LLMs step-by-step without human annotations,” in Proceedings
     of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume
     1: Long Papers), L.-W. Ku, A. Martins, and V. Srikumar, Eds. Bangkok, Thailand:
     Association for Computational Linguistics, Aug. 2024, pp. 9426–9439. [Online]. Available:
     https://aclanthology.org/2024.acl-long.510/
[46] X. Lai, Z. Tian, Y. Chen, S. Yang, X. Peng, and J. Jia, “Step-dpo: Step-wise preference
     optimization for long-chain reasoning of llms,” arXiv preprint arXiv:2406.18629, 2024.
[47] B. Stroebl, S. Kapoor, and A. Narayanan, “Inference scaling flaws: The limits of llm resampling
     with imperfect verifiers,” arXiv preprint arXiv:2411.17501, 2024.
[48] A. Bove and P. Dybjer, “Dependent types at work,” in International LerNet ALFA Summer
     School on Language Engineering and Rigorous Software Development. Springer, 2008, pp.
     57–99.
[49] L. d. Moura and S. Ullrich, “The lean 4 theorem prover and programming language,” in
     Automated Deduction–CADE 28: 28th International Conference on Automated Deduction,
     Virtual Event, July 12–15, 2021, Proceedings 28. Springer, 2021, pp. 625–635.
[50] B. Barras, S. Boutin, C. Cornes, J. Courant, Y. Coscoy, D. Delahaye, D. de Rauglaudre, J.-C.
     Filliâtre, E. Giménez, H. Herbelin et al., “The coq proof assistant reference manual,” INRIA,
     version, vol. 6, no. 11, 1999.
[51] T. Nipkow, M. Wenzel, and L. C. Paulson, Isabelle/HOL: a proof assistant for higher-order
     logic. Springer, 2002.
[52] S. Polu and I. Sutskever, “Generative language modeling for automated theorem proving,” arXiv
     preprint arXiv:2009.03393, 2020.
[53] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and
     A. Anandkumar, “Leandojo: Theorem proving with retrieval-augmented language models,”
     Advances in Neural Information Processing Systems, vol. 36, 2024.
[54] G. Lample, T. Lacroix, M.-A. Lachaux, A. Rodriguez, A. Hayat, T. Lavril, G. Ebner, and X. Mar-
     tinet, “Hypertree proof search for neural theorem proving,” Advances in neural information
     processing systems, vol. 35, pp. 26 337–26 349, 2022.
[55] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof generation and repair with
     large language models,” in Proceedings of the 31st ACM Joint European Software Engineering
     Conference and Symposium on the Foundations of Software Engineering, 2023, pp. 1229–1241.
[56] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan, W. Li, and X. Liang, “Deepseek-
     prover: Advancing theorem proving in llms through large-scale synthetic data,” arXiv preprint
     arXiv:2405.14333, 2024.
[57] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample,
     “Draft, sketch, and prove: Guiding formal theorem provers with informal proofs,” arXiv preprint
     arXiv:2210.12283, 2022.
[58] H. Wang, H. Xin, C. Zheng, L. Li, Z. Liu, Q. Cao, Y. Huang, J. Xiong, H. Shi, E. Xie et al.,
     “Lego-prover: Neural theorem proving with growing libraries,” arXiv preprint arXiv:2310.00656,
     2023.
[59] C. Zheng, H. Wang, E. Xie, Z. Liu, J. Sun, H. Xin, J. Shen, Z. Li, and Y. Li, “Lyra: Orchestrating
     dual correction in automated theorem proving,” arXiv preprint arXiv:2309.15806, 2023.
[60] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad, “Proofnet:
     Autoformalizing and formally proving undergraduate-level mathematics,” 2023. [Online].
     Available: https://arxiv.org/abs/2302.12433
[61] C. Liu, J. Shen, H. Xin, Z. Liu, Y. Yuan, H. Wang, W. Ju, C. Zheng, Y. Yin, L. Li, M. Zhang,
     and Q. Liu, “Fimo: A challenge formal dataset for automated theorem proving,” 2023. [Online].
     Available: https://arxiv.org/abs/2309.04295


                                                  13
[62] N. Belnap, T. Steel, U. Egli, and H. Schleichert, The Logic of Questions and Answers.
     Yale University Press, 1976. [Online]. Available: https://books.google.co.jp/books?id=
     SCxuQgAACAAJ
[63] J. Avigad, L. de Moura, S. Kong, and S. Ullrich, “Theorem proving in lean 4,” https://github.
     com/leanprover/theorem_proving_in_lean4, 2024.
[64] J. Limperg and A. H. From, “Aesop: White-box best-first proof search for lean,” in Proceedings
     of the 12th ACM SIGPLAN International Conference on Certified Programs and Proofs, 2023,
     pp. 253–266.
[65] L. Aniva, C. Sun, B. Miranda, C. Barrett, and S. Koyejo, “Pantograph: A machine-to-machine
     interaction interface for advanced theorem proving, high level reasoning, and data extraction in
     lean 4,” arXiv preprint arXiv:2410.16429, 2024.
[66] F. Portoraro, “Automated Reasoning,” in The Stanford Encyclopedia of Philosophy, Spring
     2025 ed., E. N. Zalta and U. Nodelman, Eds. Metaphysics Research Lab, Stanford University,
     2025.
[67] R. Ahuja, J. Avigad, P. Tetali, and S. Welleck, “Improver: Agent-based automated proof
     optimization,” in The Thirteenth International Conference on Learning Representations, 2025.
     [Online]. Available: https://openreview.net/forum?id=dWsdJAXjQD
[68] S. Autexier and D. Dietrich, “A tactic language for declarative proofs,” in Interactive Theorem
     Proving, M. Kaufmann and L. C. Paulson, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
     2010, pp. 99–114.
[69] Q. Liu, X. Zheng, X. Lu, Q. Cao, and J. Yan, “Rethinking and improving
     autoformalization: towards a faithful metric and a dependency retrieval-based approach,” in The
     Thirteenth International Conference on Learning Representations, 2025. [Online]. Available:
     https://openreview.net/forum?id=hUb2At2DsQ
[70] T. mathlib Community, “The lean mathematical library,” in Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, ser. CPP 2020. New
     York, NY, USA: Association for Computing Machinery, 2020, p. 367–381. [Online]. Available:
     https://doi.org/10.1145/3372885.3373824
[71] Q. Yu, Z. Zheng, S. Song, Z. li, F. Xiong, B. Tang, and D. Chen, “xfinder:
     Large language models as automated evaluators for reliable evaluation,” in The
     Thirteenth International Conference on Learning Representations, 2025. [Online]. Available:
     https://openreview.net/forum?id=7UqQJUKaLM
[72] W. A. Howard et al., “The formulae-as-types notion of construction,” To HB Curry: essays on
     combinatory logic, lambda calculus and formalism, vol. 44, pp. 479–490, 1980.
[73] L. P. Community, “A lean 4 metaprogramming book,” https://github.com/leanprover-community/
     lean4-metaprogramming-book, 2025, accessed: 2025-01-20.
[74] K. Buzzard, “Formalising mathematics,” https://www.ma.imperial.ac.uk/~buzzard/xena/
     formalising-mathematics-2024/, 2024, accessed: 2025-01-20.
[75] C. Bailey, P. Monticone, M. Dvořák, K. C, and Kitamado, “Type checking in lean 4,” https:
     //github.com/ammkrn/type_checking_in_lean4, 2024.
[76] R. Collingwood, An Autobiography. Read Books Limited, 2015. [Online]. Available:
     https://books.google.co.jp/books?id=NHh-CgAAQBAJ
[77] C. L. Hamblin, “Questions in montague english,” Foundations of Language, vol. 10, no. 1, pp.
     41–53, 1973. [Online]. Available: http://www.jstor.org/stable/25000703
[78] L. Karttunen, “Syntax and semantics of questions,” Linguistics and Philosophy, vol. 1, pp. 3–44,
     01 1977.
[79] C. Menzel, “Possible Worlds,” in The Stanford Encyclopedia of Philosophy, Summer 2024 ed.,
     E. N. Zalta and U. Nodelman, Eds. Metaphysics Research Lab, Stanford University, 2024.
[80] J. Groenendijk and M. Stokhof, “Semantic analysis of" wh"-complements,” Linguistics and
     philosophy, pp. 175–233, 1982.
[81] M. Aloni, A. Butler, and P. J. E. Dekker, “Questions in dynamic semantics,” 2007. [Online].
     Available: https://api.semanticscholar.org/CorpusID:122764653


                                                 14
[82] J. Groenendijk, “Inquisitive semantics: Two possibilities for disjunction,” in International
     Tbilisi Symposium on Logic, Language, and Computation. Springer, 2007, pp. 80–94.
[83] I. Ciardelli, J. Groenendijk, and F. Roelofsen, “Inquisitive semantics: a new notion of meaning,”
     Language and Linguistics Compass, vol. 7, no. 9, pp. 459–476, 2013.
[84] I. Ciardelli, F. Roelofsen, and N. Theiler, “Composing alternatives,” Linguistics and Philosophy,
     vol. 40, pp. 1–36, 2017.
[85] A. Meurer, C. P. Smith, M. Paprocki, O. Čertík, S. B. Kirpichev, M. Rocklin, A. Kumar,
     S. Ivanov, J. K. Moore, S. Singh et al., “Sympy: symbolic computing in python,” PeerJ
     Computer Science, vol. 3, p. e103, 2017.
[86] L. Xie, Z. Hui, and Q. Cao, “A natural formalized proof language,” 2024. [Online]. Available:
     https://arxiv.org/abs/2405.07973
[87] Y. Zhang, G. Zhang, Y. Wu, K. Xu, and Q. Gu, “Beyond bradley-terry models: A
     general preference model for language model alignment,” 2025. [Online]. Available:
     https://arxiv.org/abs/2410.02197
[88] H. Dong, W. Xiong, B. Pang, H. Wang, H. Zhao, Y. Zhou, N. Jiang, D. Sahoo, C. Xiong, and
     T. Zhang, “RLHF workflow: From reward modeling to online RLHF,” Transactions on Machine
     Learning Research, 2024. [Online]. Available: https://openreview.net/forum?id=a13aYUU9eU
[89] H. Face, “Math-verify,” February 2025. [Online]. Available: https://github.com/huggingface/
     Math-Verify
[90] E. Beeching, L. Tunstall, and S. Rush, “Scaling test-time compute with open models.” [Online].
     Available: https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute




                                                 15
A        Background
A.1       Formal Theorem Proving

Based on the Curry-Howard isomorphism [72] (aka. propositions-as-types correspondence), inter-
active proof assistants such Lean [49], Coq [50] can verify proofs of mathematical theorems and
assertions about complex systems by performing type check on the given terms.
To construct such a “proof term”, one can directly construct a term of the corresponding proposition’s
type. This direct proof is called “term-style" proof [63]. Another incremental way is “tactic-style"
proof [63] (aka. proof script), a series of tactic applications, continually reducing goals into subgoals,
until all goals are resolved.
In tactic mode, proof assistants maintain a proof state, a set of proof goals. Each goal Γ ⊢ U contains
a local context Γ, which is a telescope (ordered list) of declarations, and a conclusion U , which is
a type to construct. Each declaration might be a local assumption (x : T ) (variable declaration or
hypothesis), or a local definition (x := t : T ). A tactic is a partial function that manipulates the
current proof state by closing a goal Γ ⊢ ϕ and creating a finite set of subgoals {Γ′i ⊢ Ui′ }ni=1 (n can
be 0). Tactic applications are provability-reflecting: if all subgoals {Γ′i ⊢ Ui′ }ni=1 are solved, then the
original goal Γ ⊢ ϕ is solved [65].

                                                     Γ′1 ⊢ U1′
                                                     Γ′2 ⊢ U2′
                                                      ......
                                                     Γ′n ⊢ Un′
                                                                 PR
                                                      Γ⊢C

Some “safe7 tactics” are further provability-preserving, i.e. if the original goal Γ ⊢ ϕ is provable,
then all subgoals {Γ′i ⊢ Ui′ }ni=1 are also provable.

                                                      Γ⊢C
                                                                 PP
                                                     Γ′1 ⊢ U1′
                                                     Γ′2 ⊢ U2′
                                                      ......
                                                     Γ′n ⊢ Un′

When sufficient information is unavailable for tactic applications, metavariables are introduced to
represent "holes" in expressions. Unresolved proof goals are similarly represented by metavariables
internally [73]. A metavariable is a typed placeholder that represents the same expression in all
occurrences. It carries a local context (same as that of goals) and a target type (corresponding to the
conclusions of goals). A metavariable must be assigned an expression of its target type, using only
free variables from its local context and information from the global context.

A.2       Equality

In Lean 4, there are three levels of equivalence between terms [74]:
         1. Syntactic equality is the strongest kind of equivalence. Two terms are syntactically equal if
            they have the same syntactic structures. For example, x␣+␣0 is syntactically equal to x+␣␣0
            because redundant whitespaces8 are syntactically neglected in this case, while x + 0 and x
            are not syntactically equal since “+ 0” do introduce syntactical difference.
         2. Definitional equality is a relatively weaker kind of equivalence. Two terms are definitionally
            equal if they are convertible under a series of conversion rules, including α-conversion,
            η-expansion, proof irrelevance, β-reduction, etc. [75]. Although weaker than syntactic
            equality, definitional equality remains too strong, even for determining equivalence between
            propositions [69]. For instance, 2 + 1 is not definitionally equal to 1 + 2, where 1 and 2 are
            real numbers.
    7
        Named by [64].
    8
        Here “ ” is used to emphasize whitespaces.


                                                         16
      3. Propositional equality is the weakest kind of equivalence. Two terms t and t′ are propo-
         sitionally equal if the proposition t = t′ is provable, i.e., a proof term of type t = t′ can
         be constructed. However, this form of equality is too weak when determining equivalence
         between an answer term and the ground truth. For example, in the find-all problem "Find all
         x of type Tx such that P x," with the ground truth S̄ of type Set Tx , a direct adaptation of
         the problem {x : Tx | P x} is propositionally equal to S̄.

B    More Related Works
Philosophical Discussions. Since the proposal of erotetic logic [76], also known as the logic of
questions and answers [62], a significant body of discussions has emerged concerning questions,
answers, and their relations from the perspectives of philosophy, linguistics, and logic. Within their
consensus, questions are categorized into elementary questions (including whether-questions and
which-questions), why-questions, and embedded questions (aka. indirect questions).
The semantics of elementary questions can be broadly summarized into four theories [16]. Among
these, Hamblin Semantics, Partition Semantics, and Inquisitive Semantics are proposition-set theories,
as they conceptualize the meaning of questions as sets of propositions. In Hamblin Semantics [77,
78, 62], a question is defined as a function that maps a possible world into a set of propositions, each
corresponding to a possible answer, where a possible world refers to a complete and consistent way
how things could have been [79]. [3] further defines a problem as the constraints on the solution and
the requirement that a solution exists. However, Hamblin Semantics lack a clear definition for “what
a possible answer should be.” To solve this limitation, Partition Semantics [80, 81] restricts that the
set of propositions, which a question maps to, must be mutually exclusive and exhaustively cover
the entire logical space. The resulting definition of possible answers is a “true exhaustive answer.”
However, in some cases, the “true exhaustive answer” is challenging to specify. Another attempt
to clarify the definition of possible answers is Inquisitive Semantics [82, 83, 84], which extends
classical logic by incorporating questions and interrogatives, treating both questions and propositions
as fundamental concepts. This line of theories defines the meaning of questions as downward-closed
proposition sets.
Our work differs by formalizing both whether- and which-questions and their solving processes
from the perspective of formal verification. This enables seamless integration with existing theorem
proving environments.
Evaluation of Answer Correctness. Existing methods are all designed for informal problem-solving.
They evaluate by string matching [17, 18, 19], symbolic equivalence [20, 6, 21] via SymPy [85], or
domain-specific LLMs [23]. However, these methods may lack numerical robustness (e.g., false-
positive between 0.999999997 and 1), fall short in complex answers (e.g., false negative between
{x ∈ R | 0 ≤ x ≤ 1} and [0, 1]), or rely on LLMs.
In contrast, we propose a symbolic approach based on formal verification, providing expressive,
interpretable, human-aligned, and light-weighted correctness checking.

C    Exemplar Reasoning Patterns
There are dazzlingly many reasoning patterns in problem-solving that can unify in this formulation,
to name a few:

       • Deriving a new condition
                               Vpi,jby deductive  reasoning on conditions Φi . This step adds one new
         condition ϕ′i to Φi if j=1  ϕi,j → ϕ′i ;
       • Deducing necessary conditions of the answer by partial deductiveVqreasoning  [86] on the
                                                                            i,j
         conditions Φ and conclusions Ψ; This step adds one new condition j=1   ψi,j → ϕ′i to Φi if
          Vpi,j       Vqi,j
         ( j=1  ϕi,j ∧ j=1  ψi,j ) → ϕ′i ;
       • Drawing sufficient conditions of conclusions Ψ by backward reasoning. This step replaces
                                 ′       ′
         one conclusion ψi,j to ψi,j if ψi,j → ψi,j ;
       • Case-by-case discussion. This step replaces one goal with multiple goals and adds one
         concrete condition to each goal;


                                                  17
        • Extracting a new hole from one ∃-quantified conclusion. This step replaces the quantified
          variable with a newly introduced hole;
        • Filling the hole a with a term and proposing possibly other holes. This step replaces every
          occurrence of the hole into a term and removes the hole.

D     Code template
D.1    Formal Problem Solving

example :
∀(v1 : T1 ) · · · (vn : Tn )(h1 : ϕ1 ) · · · (hp : ϕp ),
∃(a : Ta ), ψ1 ∧ · · · ∧ ψq := by
      intros v1 · · · vn h1 · · · hp
      apply Exists.intro
-- Initial Proof State
case h -- Goal of the problem
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ (ψ1 ∧ · · · ∧ ψq )[a 7→?w]
case w -- Hole of the answer
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ Ta


D.2    Deductive Formal Problem-Solving

example :
∀(v1 : T1 ) · · · (vn : Tn )(h1 : ϕ1 ) · · · (hp : ϕp ),
∃(A : Prop), ψ ↔ A := by
      intros v1 · · · vn h1 · · · hp
      apply Exists.intro
      constructor
      intros h′ -- on goal "h.mp"
      intros ha              -- on goal "h.mpr"
-- Initial Proof State
case h.mp -- Forward Solving
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
(h′ : ψ)
⊢ ?w
case h.mpr -- Backward Provinng
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
(ha : ?w)
⊢ψ
case w -- Hole of the answer
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ Prop


D.3    Restricted Propositional Equivalence

example (v1 : T1 ) · · · (vn : Tn )(h1 : ϕ1 ) · · · (hp : ϕp )
: (â : Ta ) = (ā : Ta ) := by
try rfl
try norm_num
try ring_nf
try rw_search
try aesop



                                                           18
E     Exemplar Formalizations of Problems
E.1   Exemplar Problem in Different Types

      1. Yes-no question: Does there exist a positive real number α such that [αn ] − n is even for all
         integers n > 0?
         The formalization is straight-forward as:
         V = ∅, Φ = ∅, â := True, and
                                  Ψ = {a ∈ {True, False},
                                   (a ↔ ∃α, ∀n ∈ Z, n > 0 → ([αn ] − n)
                                    := 0 mod 2)}
         The code implementation of the FPS framework is:
         example :
         ∃ (a : Prop), (a ↔ ∃ α : R, ∀ n : N, n > 0 → (α^n - n) %
         apply Exists.intro
         -- Initial Proof State
         case h -- Goal of the problem
         ⊢ (?a ↔ ∃ α : R, ∀ n : N, n > 0 → (α^n - n) %
         case a -- Hole of the answer
         ⊢ Prop

         The code implementation of the D-FPS framework is:
         example :
         ∀ (a : Prop), ∃ (A : Prop), (a ↔ ∃ α : N → Z, ∀ n : N, n > 0 → (α n -
              n) %
         intros a
         apply Exists.intro
         constructor
         intros h_a
         -- Initial Proof State
         case h.mp -- Forward Reasoning
         (a : Prop)
         (h_p_1 : a ↔ ∃ α : N → Z, ∀ n : N, n > 0 → (α n - n) %
         ⊢ ?A
         case h.mpr
         (a : Prop)
         (h_a : ?A)
         ⊢ (a ↔ ∃ α : N → Z, ∀ n : N, n > 0 → (α n - n) %
         case A
         (a : Prop)
         ⊢ Prop

      2. Equation solving: Solve the equation x2 − 1 = 0.
         The formalization depends on the concrete meaning of the problem: find one answer or find
         all possible answers. The find-one problem can be formulated as
                                      V = ∅, Φ = ∅, â := −1 ∨ â := 1
                                      Ψ = {a ∈ R, a2 − 1 = 0}
         The code implementation of the FPS framework is:
         example :
         ∃ (a : R), (a^2 - 1 = 0) := by
         apply Exists.intro
         -- Initial Proof State
         case h -- Goal of the problem
         ⊢ (?a^2 - 1 = 0)
         case a -- Hole of the answer
         ⊢ R


                                                  19
         Notably, the D-FPS framework is unsuitable for the find-one problem so we omit the code
         implementation of the D-FPS framework here.
         The find-all problem can be
                                     V = {x}, Φ = {x ∈ R}, â := {−1, 1}
                                     Ψ = {a ∈ 2R , x ∈ a ↔ x2 − 1 = 0}
         The code implementation of the FPS framework is:
         example :
         ∀ (x : R)
         ∃ (a : Set R), (x ∈ a ↔ x^2 - 1 = 0) := by
         intros x
         apply Exists.intro
         -- Initial Proof State
         case h -- Goal of the problem
         (x : R)
         ⊢ (x ∈ ?a ↔ x^2 - 1 = 0)
         case a -- Hole of the answer
         (x : R)
         ⊢ Set R

         The code implementation of the D-FPS framework is:
         example :
         ∀ (x : R)
         ∀ (a : R), ∃ (A : Prop), (x ∈ a ↔ x^2 - 1 = 0) ↔ A := by
         intros x a
         apply Exists.intro
         constructor
         intros h_p_1
         intros h_a
         -- Initial Proof State
         case h.mp -- Forward Reasoning
         (x : R)
         (a : R)
         (h_p_1 : x ∈ a ↔ x^2 - 1 = 0)
         ⊢ ?A
         case h.mpr -- Backward Reasoning
         (x : R)
         (a : R)
         (h_a : ?A)
         ⊢ (x ∈ a ↔ x^2 - 1 = 0)
         case A -- Hole of the answer
         (x : R)
         (a : R)
         ⊢ Prop

                                  √     √       √
     3. Simplification: Simplify 28x · 15x · 21x.
        This problem is somewhat ill-defined since the metric of “simplify” is not clear9 . But it can
        still be formulated as follows:
                                                                     √
                                  V = {x}, Φ = {x ∈ R+ }, â := 42x 5x
                                                   √      √        √
                                  Ψ = {a ∈ R, a = 28x · 15x · 21x}
         The code implementation of the FPS framework is:
         example :
         ∀ (x : R) (h_1 : x > 0)
         ∃ (a : R), (a = sqrt(28 * x) * sqrt(15 * x) * sqrt(21 * x)) := by
         intros x h_1
         apply Exists.intro
9
    RPE in Sec. 4.1 can provide a human-aligned evaluation for direct answers.


                                                    20
   -- Initial Proof State
   case h -- Goal of the problem
   (x : R)
   ⊢ (?a = sqrt(28 * x) * sqrt(15 * x) * sqrt(21 * x))
   case a -- Hole of the answer
   ⊢ R

   The code implementation of the D-FPS framework is:
   example :
   ∀ (x : R) (h_1 : x > 0)
   ∀ (a : R), ∃ (A : Prop), (a = sqrt(28 * x) * sqrt(15 * x) * sqrt(21 * x)) ↔
        A := by
   intros x h_1 a
   apply Exists.intro
   constructor
   intros h_p_1
   intros h_a
   -- Initial Proof State
   case h.mp -- Forward Reasoning
   (x : R)
   (h_1 : x > 0)
   (a : R)
   (h_p_1 : a = sqrt(28 * x) * sqrt(15 * x) * sqrt(21 * x))
   ⊢ ?A
   case h.mpr -- Backward Reasoning
   (x : R)
   (h_1 : x > 0)
   (a : R)
   (h_a : ?A)
   ⊢ (a = sqrt(28 * x) * sqrt(15 * x) * sqrt(21 * x))
   case A -- Hole of the answer
   (x : R)
   (h_1 : x > 0)
   (a : R)
   ⊢ Prop

                                                                     n
4. Counter-example construction: Find a Fermat number Fn = 22 + 1 which is not prime.
   One possible answer is 5. (F5 = 4, 294, 967, 297 = 641 × 6, 700, 417)
   Let Prime be a predicate that a given natural number is a prime number, the formalization is
                                     V = ∅, Φ = ∅, â := 5 ∧ . . .
                                                         a
                                Ψ = {a ∈ N, ¬Prime(22 + 1)}
   The code implementation of the FPS framework is:
   example :
   ∃ (a : N), (¬ Nat.Prime (2^(2^a) + 1)) := by
   apply Exists.intro
   -- Initial Proof State
   case h -- Goal of the problem
   ⊢ (¬ Nat.Prime (2^(2^?a) + 1))
   case a -- Hole of the answer
   ⊢ N

   Notably, the D-FPS framework is unsuitable for the find-one problem so we omit the code
   implementation of the D-FPS framework here.
5. Physics Modeling: A spherical droplet falls through the stationary mist, absorbing all
   encountered water molecules. Assuming the droplet remains spherical, mist density is
   uniform, air viscosity is negligible, and gravitational acceleration g is constant. After
   sufficient time, the droplet’s acceleration approaches a steady value. Determine this value.
   The answer is 17 g. Interestingly. it doesn’t depend on various variables such as the mist
   density and the density of water.


                                           21
We denote the mass of the droplet by m, the velocity by v, the radius by R, the density
of water by ρ, and the mass density of the mist by k. Then V = {g, ρ, k, t, m, v, R} The
physical process can be modeled as
                                                                
                          
                           g ∈ R+ , ρ ∈ R+ , k ∈ R+ , m ∈ R∗ R ,
                                                                 
                                                                
                                  ∗R          ∗R
                                                                
                            v ∈      , R  ∈      , m(−∞) = 0,
                                                                
                          
                          
                               R           R                    
                                                                 
                                                                 
                      Φ=                            dv    dm
                            v(−∞) = 0, mg = m          +v     , 
                                                    dt    dt
                          
                                                                
                          
                                                                
                                                                 
                          
                                 4     3   dm         2
                                                                 
                                                                 
                            m = πR ρ,            = kπR v
                          
                                                                
                                                                 
                                  3         dt
And Ψ = {a = ( dv              1
               dt )(∞)}, â = 7 g
The code implementation of the FPS framework is:
example :
∀ (g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
(h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
(h_4 : Tendsto (m t) atBot (N 0))
(h_5 : Tendsto (v t) atBot (N 0))
(h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
(h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
(h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))
∃ (a : R), (Tendsto (v t) atTop (N a)) := by
intros g ρ k t m v R h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8
apply Exists.intro
-- Initial Proof State
case h -- Goal of the problem
(g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
(h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
(h_4 : Tendsto (m t) atBot (N 0))
(h_5 : Tendsto (v t) atBot (N 0))
(h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
(h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
(h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))
⊢ (Tendsto (v t) atTop (N ?a))
case a -- Hole of the answer
⊢ R

The code implementation of the D-FPS framework is:
example :
∀ (g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
(h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
(h_4 : Tendsto (m t) atBot (N 0))
(h_5 : Tendsto (v t) atBot (N 0))
(h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
(h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
(h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))
∀ (a : R), ∃ (A : Prop) (Tendsto (v t) atTop (N a)) ↔ A := by
intros g ρ k t m v R h_1 h_2 h_3 h_4 h_5 h_6 h_7 h_8
apply Exists.intro
constructor
intros h_p_1
intros h_a
-- Initial Proof State
case h.mp -- Forward Reasoning
(g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
(h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
(h_4 : Tendsto (m t) atBot (N 0))
(h_5 : Tendsto (v t) atBot (N 0))
(h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
(h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
(h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))


                                      22
         (a : R)
         (h_p_1 : Tendsto (v t) atTop (N a))
         ⊢ ?A
         case h.mpr -- Backward Reasoning
         (g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
         (h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
         (h_4 : Tendsto (m t) atBot (N 0))
         (h_5 : Tendsto (v t) atBot (N 0))
         (h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
         (h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
         (h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))
         (a : R)
         (h_a : ?A)
         ⊢ (Tendsto (v t) atTop (N a))
         case A -- Hole of the answer
         (g : R) (ρ : R) (k : R) (t : R) (m : R → R) (v : R → R) (R : R → R)
         (h_1 : g > 0) (h_2 : ρ > 0) (h_3 : k > 0)
         (h_4 : Tendsto (m t) atBot (N 0))
         (h_5 : Tendsto (v t) atBot (N 0))
         (h_6 : (m t) * g = (m t) * (deriv v t) + (v t) * (deriv m t))
         (h_7 : m t = 4/3 * Real.pi * (R t)^3 * (ρ t))
         (h_8 : deriv m t = k * Real.pi * (R t)^2 * (v t))
         (a : R)
         ⊢ Prop


E.2   Exemplar Problem in the Benchmarks

FormalMath500

      1. How many integers are in the solution set of |x − 2| ≤ 5.6?
         The problem can be formulated as follows:
                     V = {S}, Φ = {S ∈ 2Z , S = {x : Z | |x − 2| ≤ 28/5}}, â := 11
                                                             Ψ = {a ∈ N, |S| = a}
         The code implementation of the FPS framework is:
         example :
         ∀ (S : Set Z) (hS : S = {x : Z | abs (x - 2) ≤          28 / 5 })
         ∃ (a : N), (S.encard = a) := by
         intros S hS
         apply Exists.intro
         -- Initial Proof State
         case h -- Goal of the problem
         (S : Set Z)
         (hS : S = {x : Z | abs (x - 2) ≤ 28 / 5 })
         ⊢ (S.encard = ?a)
         case a -- Hole of the answer
         ⊢ N

         The code implementation of the D-FPS framework is:
         example :
         ∀ (S : Set Z) (hS : S = {x : Z | abs (x - 2) ≤ 28 / 5 })
         ∀ (a : N), ∃ (A : Prop), (S.encard = a) ↔ A := by
         intros x hS a
         apply Exists.intro
         constructor
         intros h_p_1
         intros h_a
         -- Initial Proof State
         case h.mp -- Forward Reasoning
         (S : Set Z)
         (hS : S = {x : Z | abs (x - 2) ≤ 28 / 5 })


                                                23
   (a : N)
   (h_p_1 : S.encard = a)
   ⊢ ?A
   case h.mpr -- Backward Reasoning
   (S : Set Z)
   (hS : S = {x : Z | abs (x - 2) ≤          28 / 5 })
   (a : N)
   (h_a : ?A)
   ⊢ (S.encard = a)
   case A -- Hole of the answer
   (S : Set Z)
   (hS : S = {x : Z | abs (x - 2) ≤          28 / 5 })
   (a : N)
   ⊢ Prop

2. The proper divisors of 12 are 1, 2, 3, 4, and 6. A proper divisor of an integer N is a positive
   divisor of N that is less than N . What is the sum of the proper divisors of the sum of the
   proper divisors of 284?
   The problem can be formulated as follows:
                                       V = ∅, Φ = ∅, â := 220
                                                X
                                  Ψ = {a ∈ R,           i = a}
                                                 i|284,i<284

   The code implementation of the FPS framework is:
   example :
   ∃ (a : R), (Σ n ∈ (Finset.filter (fun d => d < 284) (Nat.divisors 284)), n
       = answer) := by
   apply Exists.intro
   -- Initial Proof State
   case h -- Goal of the problem
   ⊢ (Σ n ∈ (Finset.filter (fun d => d < 284) (Nat.divisors 284)), n = ?a)
   case a -- Hole of the answer
   ⊢ R

   The code implementation of the D-FPS framework is:
   example :
   ∀ (a : R), ∃ (A : Prop), (Σ n ∈ (Finset.filter (fun d => d < 284)
        (Nat.divisors 284)), n = a) ↔ A := by
   intros a
   apply Exists.intro
   constructor
   intros h_p_1
   intros h_a
   -- Initial Proof State
   case h.mp -- Forward Reasoning
   (a : R)
   (h_p_1 : Σ n ∈ (Finset.filter (fun d => d < 284) (Nat.divisors 284)), n =
        a)
   ⊢ ?A
   case h.mpr -- Backward Reasoning
   (a : R)
   (h_a : ?A)
   ⊢ (Σ n ∈ (Finset.filter (fun d => d < 284) (Nat.divisors 284)), n = a)
   case A -- Hole of the answer
   (a : R)
   ⊢ Prop




                                            24
MiniF2F-Solving
    1. Define a function on the positive integers recursively by f (1) = 2, f (n) = f (n − 1) + 1 if
       n is even, and f (n) = f (n − 2) + 2 if n is odd and greater than 1. What is f (2017)?
       The problem can be formulated as follows:
       V = {f }, Φ = {f ∈ RN , f (1) = 2, (∀ n ∈ N, (1 < n ∧ Even n) → f (n) = f (n − 1)),
       (∀ n ∈ N, (1 < n ∧ Odd n) → f (n) = f (n − 2) + 2)}, â := 2018, Ψ = {a ∈ R, f (2017) = a}
       The code implementation of the FPS framework is:
       example :
       ∀ (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       ∃ (w : R), (w = f 2017) := by
       intros f h0 h1 h2
       apply Exists.intro
       -- Initial Proof State
       case h -- Goal of the problem
       (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       ⊢ ?w = f 2017
       case w -- Hole of the answer
       ⊢ R

       The code implementation of the D-FPS framework is:
       example :
       ∀ (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       ∀ (w : R), ∃ (A : Prop), (w = f 2017) ↔ A := by
       intros f h0 h1 h2 w
       apply Exists.intro
       constructor
       intros h_p_1
       intros h_a
       -- Initial Proof State
       case h.mp -- Forward Reasoning
       (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       (w : R)
       (h_p_1 : w = f 2017)
       ⊢ ?A
       case h.mpr -- Backward Reasoning
       (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       (w : R)
       (h_a : ?A)
       ⊢ (w = f 2017)
       case A -- Hole of the answer
       (f : N → R)
       (h0 : f 1 = 2)
       (h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1)
       (h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2)
       (w : R)
       ⊢ Prop


                                               25
     2. Find the units digit of 1617 × 1718 × 1819 .
        The problem can be formulated as follows:
                                                        V = ∅, Φ = ∅, â := 8,
                                                       17
                              Ψ = {a ∈ N, a = (16           × 1718 × 1819 )%10}

        The code implementation of the FPS framework is:
        example :
        ∃ (a : N), (a = (16^{17} \times 17^{18} \times 18^{19}) \% 10) := by
        apply Exists.intro
        -- Initial Proof State
        case h -- Goal of the problem
        ⊢ ?a = (16^{17} \times 17^{18} \times 18^{19}) \% 10
        case a -- Hole of the answer
        ⊢ N

        The code implementation of the D-FPS framework is:
        example :
        ∀ (a : N), ∃ (A : Prop), (a = (16^{17} \times 17^{18} \times 18^{19}) \%
             10) ↔ A := by
        intros a
        apply Exists.intro
        constructor
        intros h_p_1
        intros h_a
        -- Initial Proof State
        case h.mp -- Forward Reasoning
        (a : N)
        (h_p_1 : a = (16^{17} \times 17^{18} \times 18^{19}) \% 10)
        ⊢ ?A
        case h.mpr -- Backward Reasoning
        (a : N)
        (h_a : ?A)
        ⊢ (a = (16^{17} \times 17^{18} \times 18^{19}) \% 10)
        case A -- Hole of the answer
        (a : N)
        ⊢ Prop


PutnamBench-Solving
                R1
     1. Evaluate 0 ln(x+1)
                     x2 +1 dx.
        The problem can be formulated as follows:
                                        V = ∅, Φ = ∅, â := π log 2/8,
                                                   Z 1
                                                       ln(x + 1)
                                   Ψ = {a ∈ R, a =                dx}
                                                    0     x2 + 1
        The code implementation of the FPS framework is:
        example :    R
        ∃ (a : R), ( x in (0:R)..1, (Real.log (x+1))/(x^2 + 1) =
         a) := by
        apply Exists.intro
        -- Initial Proof State
        case
          R h -- Goal of the problem
        ⊢    x in (0:R)..1, (Real.log (x+1))/(x^2 + 1) = ?a
        case a -- Hole of the answer
        ⊢ R

        The code implementation of the D-FPS framework is:


                                                26
  example :                   R
  ∀ (a : R), ∃ (A : Prop), ( x in (0:R)..1, (Real.log (x+1))/(x^2 + 1) =
       a) ↔ A := by
  intros a
  apply Exists.intro
  constructor
  intros h_p_1
  intros h_a
  -- Initial Proof State
  case h.mp -- Forward Reasoning
  (a : R) R
  (h_p_1 :    x in (0:R)..1, (Real.log (x+1))/(x^2 + 1) = a)
  ⊢ ?A
  case h.mpr -- Backward Reasoning
  (a : R)
  (h_aR : ?A)
  ⊢ ( x in (0:R)..1, (Real.log (x+1))/(x^2 + 1) = a)
  case A -- Hole of the answer
  (a : R)
  ⊢ Prop

2. Find
                                   ∞
                                 ∞ X
                                 X               1
                                          2 j + 2ij + ij 2
                                                           .
                                 i=1 j=1
                                         i

  The problem can be formulated as follows:
                                         V = ∅, Φ = ∅, â := 7/4,
                                         ∞ X ∞
                                        X               1
                        Ψ = {a ∈ R, a =          2 j + 2ij + ij 2
                                                                  }
                                        i=1 j=1
                                                i

  The code implementation of the FPS framework is:
  example :
  ∃ (a : R), (a = (Σ’ i : N+, Σ’ j : N+, (1 : Q) / (i ^ 2 * j + 2 * i * j +
       i * j ^ 2)) := by
  apply Exists.intro
  -- Initial Proof State
  case h -- Goal of the problem
  ⊢ ?a = (Σ’ i : N+, Σ’ j : N+, (1 : Q) / (i ^ 2 * j + 2 * i * j + i * j ^
      2))}
  case a -- Hole of the answer
  ⊢ R

  The code implementation of the D-FPS framework is:
  example :
  ∀ (a : R), ∃ (A : Prop), (a = (Σ’ i : N+, Σ’ j : N+, (1 : Q) / (i ^ 2 *
       j + 2 * i * j + i * j ^ 2))) ↔ A := by
  intros a
  apply Exists.intro
  constructor
  intros h_p_1
  intros h_a
  -- Initial Proof State
  case h.mp -- Forward Reasoning
  (a : R)
  (h_p_1 : a = (Σ’ i : N+, Σ’ j : N+, (1 : Q) / (i ^ 2 * j + 2 * i * j + i *
        j ^ 2)))
  ⊢ ?A
  case h.mpr -- Backward Reasoning
  (a : R)
  (h_a : ?A)


                                        27
          ⊢ (a = (Σ’ i : N+, Σ’ j : N+, (1 : Q) / (i ^ 2 * j + 2 * i * j + i * j ^
              2)))
          case A -- Hole of the answer
          (a : R)
          ⊢ Prop



F      Proofs of Properties
F.1    Soundness of FPS

Theorem. FPS is sound: for any problem P and direct answer â resulted from FPS, P (â) holds.

Proof. The Lean 4 proof state of FPS initializes as:
case h
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ (ψ1 ∧ · · · ∧ ψq )[a 7→?a]
case a
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ Ta

Therefore, upon finishing the proof, we can extract from the Lean 4 kernel:

        • A term â : Ta filling the metavariable ?a from the initial goal case a
        • A proof term h from the initial goal case h.

Since ?a is filled by â, h is actually a proof of (∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (∧qi=1 ψi ))[a 7→ â], i.e.
P (â).
Therefore, P (â) holds by the proof term h.

F.2    Expressivenss of D-FPS for Find-All Problems

Theorem. Regarding find-all problems, the expressiveness of D-FPS is at least as strong as that of
FPS.

Proof. We construct an injection from an arbitrary find-all FPS problem to D-FPS while preserving
semantics.
Suppose the FPS problem consists of (V, (a : Ta ), Φ, Ψ) and the ground-truth answer is ā. We have
                               ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (∧qi=1 ψi )[a 7→ ā]

Therefore, the following assertion holds.
                      ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(a : Ta ), (a = ā) → (∧qi=1 ψi )                   (3)

Since it is a find-all problem, ā is the only answer (for find-unique-one problems) or the complete
collection of all valid answers (for multiple-answer problems). The following assertion holds.
                      ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(a : Ta ), (∧qi=1 ψi ) → (a = ā)                   (4)

Therefore, composing Prop. 3 and Prop. 4, the following proposition holds:
                      ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(a : Ta ), (∧qi=1 ψi ) ↔ (a = ā)
i.e.
              ∀ni=1 (vi : Ti ), ∀(a : Ta ), ∀pi=1 (hi : ϕi ), ((∧qi=1 ψi ) ↔ A)[A 7→ a = ā]
                                                                                     Vq
which corresponds to the D-FPS problem (V ∪ {(a : Ta )}, (A : Prop), Φ, { i=1 ψi ↔ A}) with
ground-truth answer Ā = (a = ā).


                                                         28
                            Vq problem with ground-truth answer ā formulated
Specifically, a multiple-answer                                                Vqin FPS as (V, (a :
Set Tx ), Φ, {a = {x : Tx | i=1 ψi }}) or (V ∪ {(x : Tx )}, (a : V
                                                                 Set Tx ), Φ, { i=1 ψi ↔ x ∈ a})
                                                                   q
can be mapped into D-FPS as (V ∪ {(x : Tx )}, (A : Prop), Φ, { i=1 ψi ↔ A}) with ground-truth
answer Ā := x ∈ ā (neither a nor x occurs free in Φ).

F.3     Completeness of D-FPS for Find-All Problems

Theorem. D-FPS is complete: for any find-all problem with ground-truth Ā, for any direct answer Â
resulted from D-FPS, the following proposition holds:

                                  ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Ā → Â

Proof. Suppose the D-FPS problem consists of (V, (A : Prop), Φ, {ψ ↔ A}) and the Lean 4 proof
state is initializes as:
case h→ -- Forward Solving
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
(h′ : ψ)
⊢?A
case h← -- Backward Provinng
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
(ha : ?A)
⊢ψ
case A -- Hole of the answer
(v1 : T1 ) . . . (vn : Tn )
(h1 : ϕ1 ) · · · (hp : ϕp )
⊢ Prop


Therefore, upon finishing forward-solving, we can extract from the Lean 4 kernel:

         • A term Â : Prop filling the metavariable ?A from the initial goal case A
         • A proof term h→ from the initial goal case h→ .

Since ?A is filled by Â, h→ is actually a proof of

                                ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(h′ : ψ), Â

The ground-truth Ā satisfies
                                 ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (ψ ↔ Ā)

Therefore, we have
                                ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(h′ : Ā), Â
i.e.,
                                  ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Ā → Â



F.4     Soundness of D-FPS for Find-All Problems

Theorem. D-FPS is sound: for any find-all problem with ground-truth Ā, for any direct answer Â
resulted from D-FPS, if the backward-proving is finished, the following proposition holds:

                                  ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Â → Ā


                                                       29
Proof. Upon finishing backward-proving, apart from Â, we can extract a proof term h← from the
initial goal case h← .
Since ?A is filled by Â, h← is actually a proof of

                         ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (∀(ha :?A), ψ)[?A 7→ Â]
i.e.,
                                ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(ha : Â), ψ

The ground-truth Ā satisfies
                                  ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), (ψ ↔ Ā)

Therefore, we have
                                ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), ∀(ha : Â), Ā
i.e.,
                                   ∀ni=1 (vi : Ti ), ∀pi=1 (hi : ϕi ), Â → Ā



Notably, for find-unique-one problems (only one valid answer exists) with queriable a, if it is
expressed in D-FPS as in Appendix F.2 and concludes a direct answer of the form Â = (a = â), a
backward proof is not required anymore (completeness implies soundness). Because of the uniqueness
of ā and Assumption 3.3, the valid answer term â must be the unique one.

G       More Analysis of RPE
G.1     Error Analysis on xVerify Benchmark

On the xVerify benchmark consisting of 300 examples, RPE results in 0 false positives and 4 false
negatives. Their error types are categorized as follows:
         • Failure of xFinder (2 false-negatives). xFinder incorrectly extracts an intermediate result as
           the answer.
         • Intolerance of numerical error (1 false-negative). RPE is based on formal verification; thus,
           imperfect floating-point approximation should not be passed. In this false-negative, the
                                               7
           answer 0.4667 and ground-truth 15      are not equivalent under RPE.
         • Insufficiency of proof automation (1 false-negative). RPE incorrectly determines proposi-
                                                2     2
           tions x2 /3 + y 2 /4 − 1 = 0 and x3 + y4 = 1 as inequivalent. This type of error does not
           significantly affect the following proposed benchmarks since most of the answers are simple
           terms instead of complicated propositions.

G.2     Rejected Case Study in Experiments

Here, we analyze answers rejected by RPE from In-Context Learning and Hybrid CoT:
             √                     √
      • a = 180/2 ↔ a = 3 ∗ 5. This is correctly rejected due to insufficient simplification;
      • a = {x | x2 − 5x + 6 > 0} ↔ a = {x | x < 2 ∨ x > 3}. This is correctly rejected since
        the answer is directly constructed from the original problem and is insufficiently solved;
                          2(j+k−2)             2(j+k−3)
                                                             ) ↔ a = 17
             P
      • a = i,j,k ( 3(i+k−2)  ×5(i+j−2)
                                        + 3(i+k−3) ×5(i+j−3)         21 . This is correctly rejected
        since the answer is directly constructed from the original problem and is insufficiently
        solved;
      • 2004%12 = 0 ↔ a = 0. This is correctly rejected since the submitted answer is irrelevant
        to the queriable a;
      • a = {f (R2 ) | f ∈ R[x, y]} ↔ a = {{x} | x ∈ R} ∪ {[x, ∞) | x ∈ R} ∪ {(−∞, x] | x ∈
        R} ∪ {(−∞, x) | x ∈ R} ∪ {(x, ∞) | x ∈ R} ∪ {R}. This is correctly rejected since the
        answer is directly constructed from the original problem and is insufficiently solved.


                                                       30
                                                             Whole-Proof
                      Proof Search                           Generation

                                         34          65
                                                                22

                                                    73

                                              23           11

                                                   34

                                           Hybrid CoT

Figure 3: Venn diagram of all problems solved by Proof Search, Whole-Proof Generation, and Hybrid
CoT.


H     Benchmark Construction Details

FormalMath500. We exclude all Geometry and Counting & Probability problems, as their
difficulty mainly lies in formalization. Once formalized, most of them collapse to simple arithmetic.
MiniF2F-Solving and PutnamBench-Solving. Many datapoints in MiniF2F and PutnamBench
are originally math word problems. By filling a problem predicate P with its ground-truth answer
ā, a proposition P (ā) is constructed for theorem proving. Based on this observation, we conduct a
rule-based selection of datapoints. For MiniF2F, we collect all datapoints with informal statements
ending with “Show that it is [answer]”; For PutnamBench, we collect all datapoints with factored
solutions. Then, we split formal problems and answers from original formal statements and recover
missing conditions/constraints due to destructive formalizations. For example, an informal problem
“Find the minimum of x2 − 2x + 1” with ground-truth 0 can be formalized into “Prove that ∀x ∈
R, x2 − 2x + 1 ≥ 0” in theorem proving. However, its correct formalization in problem-solving
is not “Find a s.t. ∀x ∈ R, x2 − 2x + 1 ≥ a” but “Find a s.t. ∀x ∈ R, x2 − 2x + 1 ≥ a and
∃x ∈ R, x2 − 2x + 1 = a”.


I     More Analysis of Experiment Results

I.1   Distribution of Solved Problems

The Venn diagram of all problems solved in the three benchmarks by Proof Search (InternLM2.5-
StepProver), Whole-Proof Generation (DeepSeekProver-V1.5), and Hybrid CoT is visualized in
Fig. 3. Interestingly, substantial overlap exists in the efficacy spectra of Proof Search and Whole-Proof
Generation: 60.53% of their solved problems are common. However, their overlap with Formal
CoT is significantly lower: 40% and 36.84%, respectively. This echoes our hypothesis that TP
models are trained on existing TP data, therefore sharing inductive biases on reasoning patterns. This
complementarity between FPS and D-FPS shows a promising future direction.

I.2   Preference Experiment

In this experiment, to validate D-FPS’s better alignment with human preference, we quantitatively
evaluate preference scores on the solutions from FPS and D-FPS using preference models.
We extract formal solutions of commonly solved problems by Proof Search (InternLM2.5-StepProver),
Whole-Proof Generation (DeepSeekProver-V1.5), and Hybrid CoT. All informal comments are
removed to ensure a fair comparison since InternLM2.5-StepProver seldom generates informal
thoughts, while Hybrid CoT always incorporates informal steps for flexible reasoning. Two preference


                                                   31
                      Table 2: Preference scores of FPS and D-FPS methods.

      Comparison                                  Preference Model       Mean      Min     Max
      Hybrid CoT - Proof Search                         GPM               0.77     0.28    1.00
                                                       RLHFlow            0.80     0.27    0.98
      Hybrid CoT - Whole-Proof Generation               GPM               0.76     0.05    1.00
                                                       RLHFlow            0.81     0.13    0.97
      Whole-Proof Generation - Proof Search             GPM               0.01    -0.36    0.57
                                                       RLHFlow            0.47    0.07     0.97

                         Table 3: Error distribution of D-FPS experiments.

  Benchmark          Method      Length    Rejection    Format    Submission     Answer     Solution
  Formal-             ICL         0.21%      0.00%       0.22%       1.07%       26.37%     72.14%
  Math500          Hybrid CoT     3.31%      0.02%       0.60%       1.82%       26.22%     68.03%
  MiniF2F             ICL         0.32%      0.00%       0.28%       0.85%       20.26%     78.28%
  Solving          Hybrid CoT     4.57%      0.00%       0.64%       1.79%       21.77%     71.24%
  PutnamBench         ICL         0.50%      0.00%       1.60%       8.47%       64.70%     24.73%
     Solving       Hybrid CoT     5.71%      0.00%       0.95%       22.76%      54.91%     15.67%


models, general-preference/GPM-Gemma-2-2B [87] and RLHFlow/pair-preference-model-LLaMA3-
8B [88], are evaluated with prompt templates in Appendix J.6.
Results are shown in Table 2, where Hybrid CoT consistently outperforms Proof Search and Whole-
Proof Generation by a clear margin.

I.3   Error Analysis of D-FPS Experiments

To provide more insights on improving D-FPS methods, we break down the failure modes of ICL and
Hybrid CoT across benchmarks, as summarized in Table 3. The main error types are as follows:
       • Length: Incomplete responses truncated due to token limits.
       • Rejection: Request rejected by API providers.
       • Format: Response unparsable due to invalid format.
       • Submission: The submitted answer is irrelevant to the queriable.
       • Answer: The submitted answer is wrong (determined via HuggingFace Math-Verify [89]).
       • Solution: The formal solution fails in Lean 4 check.
ICL and Hybrid CoT share similar error distributions. For simpler benchmarks (FormalMath500
and MiniF2F-Solving), flawed solutions (∼ 70%) are the significant errors. This reveals that
although the model can derive the correct answer in most cases, its rigor in mathematical steps and
capability to express the solution in formal languages is insufficient. For more difficult PutnamBench-
Solving, incorrect answers and irrelevant submissions are prevalent. This aligns with intuition since
PutnamBench is an undergraduate-competition-level benchmark that is challenging for even human
experts.

I.4   Case Studies

To provide an intuitive comparison, representative formal solutions of the best method in each
paradigm are shown as follows.
Proof Search (InternLM2.5-StepProver).
Let n = 317 + 310 . It is known that 11 divides into n + 1. If n can be written in base 10 as
ABCACCBAB, where A, B, C are distinct digits such that A and C are odd and B is not divisible
by 3, find 100A + 10B + C.


                                                 32
-- Initial Solution State (FPS)
case h
n A B C : N
h0 : n = 3 ^ 17 + 3 ^ 10
h1 : 11 | n + 1
h2 : List.Pairwise (fun (x1 x2 : N) => x1 ̸= x2) [A, B, C]
h3 : {A, B, C} ⊆ Finset.Icc 0 9
h4 : Odd A ∧ Odd C
h5 : ¬3 | B
h6 : Nat.digits 10 n = [B, A, B, C, C, A, C, B, A]
⊢ ?w = 100 * A + 10 * B + C
case w
⊢ N
-- Formal Solution
norm_num at h0 h1 h2 h3 h4 h5 h6 -- at 0-th goal
simp only [h0 , h2 .1.2, h2 .1.1, h2 .2, h4 .1, h4 .2, h5 ] at h6 ⊢ -- at 0-th goal
norm_num at h1 h3 h4 h5 h6 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2
    h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 h0 h2 -- at 0-th goal
exact 100 * 1 + 10 * 2 + 9 -- at 1-th goal
omega -- at 0-th goal
-- Submission: 100 * 1 + 10 * 2 + 9

Define a function on the positive integers recursively by f (1) = 2, f (n) = f (n − 1) + 1 if n is even,
and f (n) = f (n − 2) + 2 if n is odd and greater than 1. What is f (2017)?
-- Initial Solution State (FPS)
case h
f : N → R
h0 : f 1 = 2
h1 : ∀ (n : N), 1 < n ∧ Even n → f n = f (n - 1) + 1
h2 : ∀ (n : N), 1 < n ∧ Odd n → f n = f (n - 2) + 2
⊢ ?w = f 2017
case w
⊢ R
-- Formal Solution
norm_num [h0 , h1 , h2 , Nat.add_sub_cancel] -- at 0-th goal
simp [h0 , h1 , h2 , Nat.even_iff, Nat.odd_iff] -- at 1-th goal
norm_num [h0 , h1 , h2 ] -- at 0-th goal
norm_num [h0 , h1 , h2 ] -- at 0-th goal
norm_cast at * -- at 0-th goal
-- Submission: 2018

What integer n satisfies 0 ≤ n < 18 and n ≡ −11213141 (mod 18)?
-- Initial Solution State (FPS)
case h
n : N
hn : 0 ≤ n ∧ n < 18 ∧ n ≡ 18 - 11213141 %
⊢ ?w = n
case w
⊢ N
-- Formal Solution
norm_num [hn.1, hn.2.1, hn.2.2] -- at 0-th goal
norm_num at hn ⊢ -- at 0-th goal
exact 13 -- at 1-th goal
simp only [Nat.modEq_iff_dvd, Nat.mod_eq_of_lt hn.1] at hn -- at 0-th goal
omega -- at 0-th goal
-- Submission: 13

Whole-Proof Generation (DeepSeekProver-V1.5).
The product of two consecutive positive even integers is 288. What is the greater of the two integers?
-- Initial Solution State (FPS)


                                                  33
case h
⊢ ∃ n > 0, n %
case w
⊢ N
-- Formal Solution
use 16 -- at 0-th goal
apply And.intro -- at 0-th goal
apply Nat.succ_pos -- at 0-th goal
apply And.intro -- at 0-th goal
apply Eq.refl -- at 0-th goal
apply And.intro -- at 0-th goal
apply Eq.refl -- at 0-th goal
apply Eq.refl -- at 0-th goal
-- Submission: 16 + 2

Recently, Frank took a one-hundred question aptitude test where each correct answer scored 5 points,
each incorrect answer scored −2 points, and each question not answered scored zero points. Frank
answered 80 questions and scored 232 points. How many questions did he answer correctly?
-- Initial Solution State (FPS)
case h
total_questions correct incorrect unanswered : N
h0 : total_questions = 100
h1 : correct + incorrect + unanswered = total_questions
h2 : correct + incorrect = 80
h3 : 5 * correct - 2 * incorrect = 232
⊢ correct = ?w
case w
⊢ N
-- Formal Solution
have h4 : correct = 80 - incorrect := by omega; -- at 0-th goal
have h5 : 5 * (80 - incorrect) - 2 * incorrect = 232 := by omega; -- at 0-th goal
have h6 : 400 - 7 * incorrect = 232 := by omega; -- at 0-th goal
have h7 : 7 * incorrect = 168 := by omega; -- at 0-th goal
have h8 : incorrect = 24 := by omega; -- at 0-th goal
have h9 : correct = 80 - 24 := by omega; -- at 0-th goal
have h10 : correct = 56 := by omega; -- at 0-th goal
exact h10 -- at 0-th goal
-- Submission: 56

Hillary has eleven coins, all dimes and nickels. In total, the coins are worth 75 cents. How many
nickels does she have?
-- Initial Solution State (FPS)
case h
dimes nickels : N
h0 : dimes + nickels = 11
h1 : 10 * dimes + 5 * nickels = 75
⊢ nickels = ?w
case w
⊢ N
-- Formal Solution
have h2 : 10 * dimes + 5 * nickels = 75 := h1 -- at 0-th goal
have h3 : dimes + nickels = 11 := h0 -- at 0-th goal
have h4 : nickels = 11 - dimes := by omega; -- at 0-th goal
have h5 : 10 * dimes + 5 * (11 - dimes) = 75 := by omega; -- at 0-th goal
have h6 : dimes = 4 := by omega; -- at 0-th goal
have h7 : nickels = 7 := by omega; -- at 0-th goal
exact h7 -- at 0-th goal
-- Submission: 7

Hybrid CoT.
Suppose that g(x) = f −1 (x). If g(−15) = 0, g(0) = 3, g(3) = 9 and g(9) = 20, what is f (f (9))?


                                                34
-- Initial Solution State (D-FPS)
case h.mp
answer : R
f g : R → R
h_inv : Function.RightInverse g f
h0 : g (-15) = 0
h1 : g 0 = 3
h2 : g 3 = 9
h3 : g 9 = 20
h_answer : answer = f (f 9)
⊢ ?w
case h.mpr
answer : R
f g : R → R
h_inv : Function.RightInverse g f
h0 : g (-15) = 0
h1 : g 0 = 3
h2 : g 3 = 9
h3 : g 9 = 20
h_submission : ?w
⊢ answer = f (f 9)
case w
answer : R
⊢ Prop
-- Formal Forward Solution
have h_right_inverse : ∀ x, f (g x) = x := h_inv
have h_f_at_0 : f 0 = -15 := by {
    specialize h_right_inverse (-15)
    rw [h0 ] at h_right_inverse
    exact h_right_inverse
}
have h_f_at_3 : f 3 = 0 := by {
    specialize h_right_inverse 0
    rw [h1 ] at h_right_inverse
    exact h_right_inverse
}
have h_f_at_9 : f 9 = 3 := by {
    specialize h_right_inverse 3
    rw [h2 ] at h_right_inverse
    exact h_right_inverse
}
have h_f_at_20 : f 20 = 9 := by {
    specialize h_right_inverse 9
    rw [h3 ] at h_right_inverse
    exact h_right_inverse
}
have h_f_9 : f 9 = 3 := h_f_at_9
have h_f_3 : f 3 = 0 := h_f_at_3
have h_f_f_9 : f (f 9) = 0 := by {
    rw [h_f_9, h_f_3]
}
have h_answer : answer = 0 := by {
    rw [h_answer, h_f_f_9]
}
exact h_answer
-- Submission: answer = 0

The sequence S1 , S2 , S3 , · · · , S10 has the property that every term beginning with the third is the sum
of the previous two. That is, Sn = Sn−2 + Sn−1 for n ≥ 3. Suppose that S9 = 110 and S7 = 42.
What is S4 ?
-- Initial Solution State (D-FPS)
case h.mp
answer : R


                                                    35
s : N → R
h0 : ∀ (n : N), s (n + 2) = s (n + 1) + s n
h1 : s 9 = 110
h2 : s 7 = 42
h_answer : answer = s 4
⊢ ?w
case h.mpr
answer : R
s : N → R
h0 : ∀ (n : N), s (n + 2) = s (n + 1) + s n
h1 : s 9 = 110
h2 : s 7 = 42
h_submission : ?w
⊢ answer = s 4
case w
answer : R
⊢ Prop
-- Formal Forward Solution
have h_recurrence : ∀ (n : N), s (n + 2) = s (n + 1) + s n := h0
have h_S9 : s 9 = 110 := h1
have h_S7 : s 7 = 42 := h2
have h_S9_expressed : s 9 = s 8 + s 7 := h_recurrence 7
have h_S8 : s 8 = s 9 - s 7 := by
  linarith [h_S9_expressed, h_S9, h_S7]
have h_S8_expressed : s 8 = s 7 + s 6 := h_recurrence 6
have h_S6 : s 6 = s 8 - s 7 := by
  linarith [h_S8_expressed, h_S7, h_S8]
have h_S7_expressed : s 7 = s 6 + s 5 := h_recurrence 5
have h_S5 : s 5 = s 7 - s 6 := by
  linarith [h_S7_expressed, h_S7, h_S6]
have h_S6_expressed : s 6 = s 5 + s 4 := h_recurrence 4
have h_S4 : s 4 = s 6 - s 5 := by
  linarith [h_S6_expressed, h_S5, h_S6]
have h_answer : answer = 10 := by
  linarith [h_S4, h_S5, h_S6, h_S7, h_S8, h_S9]
exact h_answer
-- Submission: answer = 10

                           2
           4 −1       3x3         1 −3
                                   
Simplify   x           x         2x    .
-- Initial Solution State (D-FPS)
case h.mp
x answer : R
h0 : x ̸= 0
h_answer : answer = (4 / x)−1 * (3 * x ^ 3 / x) ^ 2 * (1 / (2 * x))−1 ^ 3
⊢ ?w
case h.mpr
x answer : R
h0 : x ̸= 0
h_submission : ?w
⊢ answer = (4 / x)−1 * (3 * x ^ 3 / x) ^ 2 * (1 / (2 * x))−1 ^ 3
case w
x answer : R
⊢ Prop
-- Formal Forward Solution
have h1 : (4 / x)−1 = x / 4 := by {
    field_simp [h0 ]
}
have h2 : (3 * x^3 / x)^2 = (3 * x^2)^2 := by {
    field_simp [h0 ]
    ring
}
have h3 : (3 * x^2)^2 = 9 * x^4 := by {
    ring


                                           36
}
have h4 : (1 / (2 * x))−1 = 2 * x := by {
    field_simp [h0 ]
}
have h5 : (1 / (2 * x))−1 ^3 = (2 * x)^3 := by {
    rw [h4 ]
}
have h6 : (2 * x)^3 = 8 * x^3 := by {
    ring
}
have h_combined : (4 / x)−1 * (3 * x^3 / x)^2 * (1 / (2 * x))−1 ^3 = (x / 4) * (9 *
    x^4) * (8 * x^3) := by {
    rw [h1 , h2 , h3 , h5 , h6 ]
}
have h_simplified : (x / 4) * (9 * x^4) * (8 * x^3) = 18 * x^8 := by {
    field_simp [h0 ]
    ring
}
have h_answer : answer = 18 * x^8 := by {
    linarith [h_combined, h_simplified]
}
exact h_answer
-- Submission: answer = 18 * x ^ 8



J     Prompt Tempaltes
J.1   Proof Search

---
NAME: {THEOREM_FULL_NAME}
---
PROOF_BEFORE: {PROOF_BEFORE}
---
STATE_BEFORE: {STATE}
---
TACTIC:


J.2   Whole-Proof Generation

Complete the following Lean 4 code with explanatory comments preceding each line of
    code:

‘‘‘lean4
import Mathlib
import Aesop
set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option tactic.hygienic false
set_option pp.fullNames true
set_option pp.funBinderTypes true
set_option pp.piBinderTypes true

/-- {INFORMAL_PROBLEM}-/

example {PROBLEM_STATE} := by
intros v1 · · · vn h1 · · · hp
apply Exists.intro


J.3   In-Context Learning


                                         37
Given an informal math problem and a corresponding Lean 4 goal state, please
    construct a formal proof deducing the answer.
Please assume the following header code has already been executed, and do not add
    any imports or openings.
‘‘‘lean4
import Mathlib
import Aesop
‘‘‘

Here are some examples:

# Informal Problem
"""
{INFORMAL_PROBLEM_i}_i
"""
# Goal State
‘‘‘lean4
{INFORMAL_PROBLEM}_i
‘‘‘
# Formal Proof
‘‘‘lean4
{FORWARD_SOLUTION}_i
‘‘‘

---

 (10-shot demonstrations). . .

---

Now, please generate a formal proof for the following problem.

# Informal Problem
"""
{INFORMAL_PROBLEM}
"""
# Goal State
‘‘‘lean4
{FORWARD_STATE}
‘‘‘


J.4   Hybrid CoT

Given an informal math problem and a corresponding Lean 4 goal state, please think
    step by step and construct a formal proof deducing the answer.
Please assume the following header code has already been executed, and do not add
    any imports or openings.
‘‘‘lean4
import Mathlib
import Aesop
‘‘‘

Here are some examples:

# Informal Problem
"""
{INFORMAL_PROBLEM_i}_i
"""
# Goal State
‘‘‘lean4
{INFORMAL_PROBLEM}_i
‘‘‘
# Formal Proof


                                         38
‘‘‘lean4
{FORWARD_SOLUTION_WITH_INFORMAL_THOUGHTS}_i
‘‘‘

---

 (10-shot demonstrations). . .

---

Now, please generate a formal proof for the following problem.

# Informal Problem
"""
{INFORMAL_PROBLEM}
"""
# Goal State
‘‘‘lean4
{FORWARD_STATE}
‘‘‘



J.5   RPE Benchmark Formalization

Given two answers to some problem, please construct a Lean 4 statement to assert
    their equivalence. Don’t try to prove them; only formalize the statement. The
    following are some examples:

# Answer A
\( x < -\frac{4}{3} \) or \( x > 0 \)
# Answer B
$(-\infty ,-\frac{4}{3})\cup (0,+\infty )$
# Formal Statement
‘‘‘lean4
example : {x : R | x < (-4/3 : R) ∨ x > (0 : R)} = (Set.Iio (-4/3 : R)) ∪
    (Set.Ioi (0 : R)) := by sorry
‘‘‘

# Answer A
\frac{1 + \sqrt{1 + 8n}}{2}
# Answer B
(1 + (1 + 8n)^(1/2)) / 2
# Formal Statement
‘‘‘lean4
example (n : R) : (1 + Real.sqrt (1 + 8 * n)) / 2 = (1 + (1 + 8 * n)^(1/2 : R)) /
    2 := by sorry
‘‘‘

# Answer A
(m-1)(n-1)
# Answer B
$\binom{m+n-2}{m-1}$
# Formal Statement
‘‘‘lean4
example (m n : N) : (m-1) * (n-1) = Nat.choose (m+n-2) (m-1) := by sorry
‘‘‘

# Answer A
364000
# Answer B
$3.64 \times 10^5
# Formal Statement
‘‘‘lean4
example : (364000 : Q) = (3.64 : Q) * (10^5) := by sorry


                                         39
‘‘‘

Now, please process the two answers:
# Answer A
{answer_a}
# Answer B
{answer_b}



J.6   Preference Model

User Message
The following is a problem, and it’s Lean 4 formalization.

# Informal Problem
"""
{informal_problem}
"""

# Formal Problem
‘‘‘lean4
{formal_problem}
‘‘‘

Please use Lean 4 code to solve the following problem step by step.


Assistant Message
‘‘‘lean4
{FORMAL_SOLUTION_WO_INFORMAL_STEPS}
‘‘‘



K     Detailed Experiment Settings

K.1   Hyperparameters

Proof Search. Following [26], we set the number of children nodes in each expansion S = 32, the
search budget K = 600, the sampling temperature T = 0.7, and the maximum token limit for each
tactic as 256. The detailed prompt template can be found in Appendix J.1. The adopted Lean 4
interface, Pantograph [65], requires tactic applications to be specific to goals. Therefore, in each
expansion step, we averagely allocate S tactic applications to each goal.
Whole-Proof Generation. Following the setting of DeepSeek-Prover-V1.5 [29], we set the search
budget K = 128, sampling temperature T = 1.0, top-p value 0.95, and the maximum token limit of
2048. The detailed prompt template is in Appendix J.2.
In-Context Learning & Hybrid CoT. The search budget is set to K = 16, sampling temperature
T = 1.0. In alignment with Whole-Proof Generation, we set the top-p value 0.95 and the maximum
token limit of 2048. The detailed prompt templates are in Appendix J.3 and Appendix J.4. We only
run forward reasoning to disentangle forward solving from backward proving and directly evaluate
the resulting answers with RPE.

K.2   Lean Environment Settings

All relevant open-source projects are summarized in Table 5 for reproducibility. Special thanks to the
authors of these excellent projects :)
The options of Lean 4 environments are summarized in Table 4. In each Pantograph [65] REPL, we
import Mathlib and Aesop, while the opened namespaces vary according to problems.


                                                 40
                                  Table 4: Environment options.

                                 Option                    Value
                                 maxHeartbeats               0
                                 maxRecDepth              100000
                                 tactic.hygienic           false
                                 pp.fullNames              true
                                 pp.funBinderTypes         true
                                 pp.piBinderTypes          true


                         Table 5: Open-source projects used in this paper.
 Name                                          Github Link                              Version
 Lean 4 [49]                 https://github.com/leanprover/lean4                        v4.15.0
 Mathlib 4 [70]       https://github.com/leanprover-community/mathlib4                  v4.15.0
 Aesop [64]            https://github.com/leanprover-community/aesop                    v4.15.0
 Pantograph [65]           https://github.com/lenianiva/Pantograph                      v0.2.25


K.3   Compute Resource Requirement

Proof Search. Each proof search experiment requires 1 Ascend-910B GPU and 32 Kunpeng-920
CPUs for 8350 minutes.
Whole-Proof Generation. Each whole-proof generation experiment requires 1 Ascend-910B GPU
and 8 Kunpeng-920 CPUs for 2890 minutes.
In-Context Learning requires 16 Kunpeng-920 CPUs for 5187 minutes, consuming 33M prompt
tokens and 15M completion tokens.
Hybrid CoT requires 16 Kunpeng-920 CPUs for 5050 minutes, consuming 95M prompt tokens and
13M completion tokens.

L     Limitations
Benchmark. During the construction of the FormalMath500 benchmark, all Geometry and Count-
ing & Probability problems are excluded. Because these problems are about elementary geom-
etry or classical probability, the difficulty mainly lies in “formally describing the conditions and
conclusions” instead of “deriving an answer based on the conditions and conclusions”. Therefore,
most of them collapse to simple arithmetic once formalized. A more elegant formalization is needed,
which keeps the difficulty of thinking.
Find-one Problems. The three constructed benchmarks and the evaluation method RPE focus on
find-all problems (including find-unique-one problems). In contrast, find-one problems (finding
one possible answer among multiple candidates) remain underexplored. This calls for benchmarks
for non-trivial find-one problems (e.g., counterexample crafting) and a human-aligned evaluation
method.
Method. Modern LLMs can reach > 50% [90] accuracy on the MATH-500 benchmark with informal
reasoning. However, the best baseline method performs significantly lower, with an accuracy of
23.77% on the FormalMath500 benchmark. This discrepancy demonstrates an urgent demand for a
domain-specific model fine-tuned on FPS data or integrating FPS capabilities into generalist LLMs.

M     Ethics Statement
Our research focuses on performing and evaluating process-verified problem-solving. While our
methods offer potential benefits for the trustworthiness and verifiability of AI reasoning, we ac-
knowledge the importance of considering the ethical implications of deploying such models. These
include ensuring the responsible use of LLMs, mitigating biases in model outputs, and addressing


                                                41
accessibility concerns. We commit to making our code available for transparency and encourage the
community to use our findings responsibly, considering the societal impacts of deploying LLMs.
The three benchmarks are annotated by ourselves based on existing datasets:

       • FormalMath500. The informal problems and answers are sampled from the MATH [18]
         dataset, which adopts the permissive MIT License;
       • MiniF2F-Solving. The original formal propositions are from the MiniF2F [25] benchmark,
         whose Lean subset is released under the permissive Apache 2.0 License;
       • PutnamBench-Solving. The original formal propositions are from the PutnamBench [14]
         benchmark, whose Lean subset is released under the permissive Apache 2.0 License;

We believe our use of the aforementioned datasets aligns with their intended purpose. We fully respect
and acknowledge their authors’ valuable work and outstanding contributions to the community. In
the released version, we will include their original copyright notices, license statements, disclaimers,
and notices of any modifications made.
The proposed benchmarks focus on formal mathematical problem-solving and do not contain sensitive
or personal information.
In this work, AI assistants are used mainly as a search engine on the Internet as well as a grammar
checker for writing. We assure that human researchers have entirely led the research and writing of
this work.




                                                  42
