                                          Formally Solving Answer-Construction Problems in Lean
                                               Jialiang Sun1 , Yuzhi Tang1 , Ao Li1 , Chris Maddison1 , and Kuldeep Meel1,2
                                                                            1
                                                                           University of Toronto, Toronto, Canada
                                                                jialiang.sun@mail.utoronto.ca, meel@cs.toronto.edu
                                                                      2 Georgia Institute of Technology, Atlanta, USA


                                                                                             Abstract
arXiv:2505.18492v6 [cs.AI] 30 Jun 2026




                                                   Large language models (LLMs) have achieved remarkable progress in formal mathematical rea-
                                               soning. Mathematical competition problems fall into two broad types: theorem-proving problems
                                               ask for a proof of a fully specified statement, whereas answer-construction problems ask the solver to
                                               construct an answer object and prove that it satisfies the stated specification. Existing mathematical
                                               reasoning engines mainly target theorem-proving problems, yet answer-construction problems remain
                                               less studied. This setting is challenging because model capabilities are misaligned, with general
                                               LLMs better suited to answer construction and prover LLMs better suited to proof generation, and
                                               because Lean proof checking alone does not rule out inadmissible circular witnesses. To close this
                                               gap, we introduce Enumerate-Conjecture-Prove (ECP), a neuro-symbolic framework for solving
                                               answer-construction problems in Lean. ECP uses general LLMs to perform bounded enumeration
                                               and construct candidate answers, and invokes prover LLMs to produce machine-checked proofs. ECP
                                               introduces admissibility checking to ensure that each answer is canonical and does not involve a circu-
                                               lar argument. On answer-construction problems from PutnamBench and autoformalized MathArena,
                                               ECP formally solves 17/346 PutnamBench instances and 18/75 MathArena instances with admissible
                                               answers and proofs, outperforming LLM baselines at aligned inference budgets. Our code is available
                                               at https://github.com/sunjia72/ecp-lpar.


                                         1    Introduction
                                         Large language models (LLMs) have achieved remarkable progress in mathematical reasoning, with broad
                                         applications in math education, verified code generation [13, 39], and research-level math discovery [22,
                                         29, 30, 32]. On one hand, general LLMs, such as models in the GPT-5 family, provide powerful human-
                                         like informal math capabilities. On the other hand, there is a growing community effort around large-scale
                                         formalized mathematics frameworks such as Lean Mathlib [19, 21], which provide the ecosystem and
                                         training corpus for prover LLMs that generate proofs in a machine-verifiable format. State-of-the-art
                                         prover LLMs can match and even outperform top human experts in formally solving high-school and
                                         undergraduate math competition problems [1, 5, 11].
                                             We focus on math competition problems in Lean, which broadly fall into two types. Theorem-proving
                                         problems have the form ∀X. P(X) → Q(X): the task is to prove a fully specified target statement. Answer-
                                         construction problems have the form ∃Ψ. ∀X. P(X) → Q(X, Ψ(X)): the answer object Ψ is not supplied
                                         and must be synthesized together with a proof of correctness. Once Ψ is known, an answer-construction
                                         problem reduces to the theorem-proving task of proving the substituted statement. Figure 1 illustrates
                                         this distinction using AIME II (2026) Problem 8: the original problem asks for an answer and a proof,
                                         while the reduced version substitutes the ground-truth answer and asks only for a proof.
                                             Existing methods and benchmarks in Lean mainly focus on theorem-proving problems. Popular
                                         benchmarks like ProofNet [2], MiniF2F [44], and FormalMath [43] are formalized from informal source
                                         problems, and answer-construction problems in the original informal sources are reduced to theorem-
                                         proving problems by substituting the ground-truth answers. Benchmarks like PutnamBench [33] include
                                         answer-construction problems, but these problems are reduced to theorem-proving versions in practice.
Formally Solving Answer-Construction Problems in Lean                                                         J. Sun et al.



                                                   AIME II P8 (2026)

                                                                              Informal Conclusion
                Informal Hypothesis                                (a) Original:
    Assume that an isosceles triangle △ ABC has AB =               Find the minimum possible value of AB with proof.
    BC. Let I be the incenter of △ ABC. The perimeters
    of △ ABC and △ AIC are in the ratio 125: 6, and all            (b) Reduced:
    the sides of both triangles have integer lengths.              Prove that the minimum possible value of AB is
                                                                   245.


                 Formal Hypothesis                                             Formal Conclusion
    def Property : Set ℕ := {x | ∃ y                               theorem aimeii_p8_original :
                                                                   ∃ (answer : ℕ), (IsLeast Property)
    z, 0 < x ∧ 0 < y ∧ 0 < z ∧ y < 2 *
                                                                   answer
    x ∧ z ^ 2 * (2 * x + y) = x * y ^
    2 ∧ 6 * (2 * x + y) = 125 * (y + 2                             theorem aimeii_p8_reduced : (IsLeast
    * z)}                                                          Property) 245


Figure 1: Example American Invitational Mathematics Examination (AIME) II Problem 8 (2026). Top:
Informal problem statement in natural language, where the original task requires constructing an answer
and proving it satisfies the statement, while the reduced task asks for a proof after the ground-truth answer
has been substituted. Bottom: Formalized statement in Lean 4.

In fact, according to the PutnamBench leaderboard for the Lean proof assistant1 , there are 33 “with-
answer” (theorem-proving) evaluations, where the ground-truth answer is already substituted into the
theorem statement, but only 2 “no-answer” (answer-construction) evaluations, where the answer needs
to be constructed. Our method was ranked first in “no-answer” evaluation at the time of submission in
June 2026. Current prover LLMs [15, 26, 34, 36, 37] focus on theorem-proving problems rather than
answer-construction problems, and pure symbolic search is expensive for various domains [8, 10], with
real quantifier elimination doubly exponential in the worst case [9].
     The difficulty of formally solving answer-construction problems is twofold: (i) admissibility checking
for constructed answers and (ii) misaligned capabilities between general and prover LLMs. For (i), the
issue is as follows: in an answer-construction problem, we require the constructed answer to have the
target format, such as “a natural-number numeral” (e.g. 1) or “a real number with arithmetic expressions”
(e.g. 52 ). We call such answers admissible answers. However, Lean does not support checking whether a
constructed answer is in the target format or simply “cheats” by circularly constructing a non-canonical
answer that trivializes the proof. We show two proofs with different constructed answers in Figure 2: the
AIME problem expects the answer to be a natural-number numeral, and both displayed proofs are accepted
by the Lean compiler. The first proof’s answer is 245 and is clearly admissible. However, the second
proof’s answer sInf Property essentially says “the minimum possible value of AB is the minimum
possible value of AB”. Although the second proof passes the Lean check, it is clearly inadmissible and
trivializes the proof via a circular argument. In fact, as shown in our evaluation in Section 5, simply using
a general or prover LLM to solve answer-construction problems can produce many spurious “successful”
trivial proofs that contain inadmissible answers. For (ii), the issue is as follows: general LLMs are
effective at constructing answers due to their strong informal reasoning capabilities and agentic tool
calls, but are expensive; prover LLMs are fine-tuned on vast formal proof data and have higher formal
proof-generation accuracy than general LLMs under aligned parameter sizes and cost budgets, but are
mostly designed for pure theorem-proving tasks and are less reliable at answer construction.
    1 Source: https://trishullab.github.io/PutnamBench/leaderboard.html.



2
Formally Solving Answer-Construction Problems in Lean                                                               J. Sun et al.




                                 Formal Statement (Answer-Construction)
    def Property : Set ℕ := {x | ∃ y z, 0 < x ∧ 0 < y ∧ 0 < z ∧ y < 2 * x ∧ z ^
    2 * (2 * x + y) = x * y ^ 2 ∧ 6 * (2 * x + y) = 125 * (y + 2 * z)}
    theorem aimeii_p8_original : ∃ (answer : ℕ), (IsLeast Property) answer :=
    by



                                                                        Proof with Inadmissible Answer
          Proof with Admissible Answer                             refine ⟨sInf Property, ?_⟩ -- inadmissible!
    use 245 –- admissible!                                         have h : Property.Nonempty := …
      <Omit 75 lines of nontrivial proof>                          exact ⟨Nat.sInf_mem h, fun y hy =>
                                                                   Nat.sInf_le hy⟩ -- trivial!

                                                        Used Constants
                      [OfNat.ofNat]                                 [HMul.hMul, setOf, Exists, And, LT.lt,
                                                                    HPow.hPow, HAdd.hAdd, OfNat.ofNat, Eq,
                                                                    InfSet.sInf]

Figure 2: Two compiling Lean proofs for AIME II P8 (2026) with different constructed answers. Left:
Proof with an admissible natural-number numeral. Right: Proof with an inadmissible circular answer.
Complete proofs are in Appendices D.2 and D.3.

    To address the limitations of existing work, we propose Enumerate-Conjecture-Prove (ECP), an
end-to-end framework for formally solving answer-construction problems. ECP first leverages general
LLMs for enumeration and answer construction, then generates formal proofs via prover LLMs with
answer refinement upon disproof. ECP verifies the solution through admissibility checking for the
constructed answer and Lean compilation of the proof. Overall, ECP takes advantage of general and
prover LLMs to correctly solve more answer-construction problems at lower cost, while ensuring the
admissibility of constructed answers to avoid trivializing proofs. The ECP workflow is largely inspired
by Pólya’s problem-solving methodology [24], which emphasizes exploration of simpler cases, pattern
generalization, and proof. The answer refinement loop is also connected to work on counterexample-
guided abstraction refinement [6, 7].
    We organize the rest of the paper as follows. We first introduce preliminary notation and formulations
of answer-construction problems in Section 2, followed by a discussion of related work in Section 3. We
present our method, including problem preprocessing, answer construction, and proving, in Section 4.
We then describe the benchmarks and present the evaluation results in Section 5. Finally, we summarize
ECP with an analysis of limitations and future work in Section 6.


2     Preliminaries
In this section, we introduce mathematical notation and basic Lean background, then describe helper
functions and formulations of answer-construction problems that illustrate the ECP workflow.

2.1     Basic Notation
By convention, we denote by D the universe of discourse (domain) and by V the set of variables, each de-
noted by a lowercase letter with optional subscripts. Given sequences of variables X = ⟨x1 , . . . , xn ⟩
and Y = ⟨y1 , . . . , ym ⟩, and a predicate P over X and Y , we write ∀X.∃Y.P(X,Y ) as shorthand for
∀x1 . · · · ∀xn .∃y1 . · · · ∃ym .P(x1 , . . . , xn , y1 , . . . , ym ). When the variables are clear from the context, we write
P as shorthand for P(X,Y ), and Vars(P) for the set of variables occurring free in P. An assignment to
a formula P is a mapping σ : Vars(P) → D that assigns each variable a concrete value in the domain;

                                                                                                                               3
Formally Solving Answer-Construction Problems in Lean                                                 J. Sun et al.


σ satisfies P(X,Y ) if P evaluates to True under σ . For a variable yi ∈ Y and a value b ∈ D, we write
P(X,Y )|yi =b for the formula obtained by substituting all free occurrences of yi in P with b. For a tuple
Y ′ = ⟨y′1 , . . . , y′m ⟩, we write P(X,Y ′ ) for the simultaneous substitution of each yi with y′i in P. We say
that a set is extensionally defined if it is an explicit finite enumeration of elements (e.g., {1, 2, 3}), or
intensionally defined if it is specified by a predicate that characterizes the elements belonging to the set
(e.g., {x ∈ R | x > 0}).

2.2    Lean 4 and Dependent Type Theory
Lean 4 [21] is a proof assistant and functional programming language whose kernel implements a
dependent type theory in the family of the Calculus of Inductive Constructions (CIC). Mathlib [19] is the
largest Lean standard library of definitions, theorems, and proofs in cutting-edge formalized mathematics.
In Lean, propositions are types and proofs are terms according to the Curry-Howard correspondence.
A type judgment has the form Γ ⊢ t : T , meaning that the term t has type T under a typing context Γ (a
list of variable bindings). The language is based on a small core of term formers: variables, constants
(definitions) from the Lean environment Σ, function application, λ -abstraction, dependent function
types (also written as ∀-types), and let-bindings. Example constants include Real.pi (denoting π)
and functions such as Real.sin (denoting sin(·)) and HAdd.hAdd (denoting +). The Lean elaborator
translates Lean code into this kernel representation by inserting implicit arguments, such as universe
parameters and type arguments, and instance arguments, such as typeclass dictionaries. To align our
presentation with standard dependent type theory, we describe Lean expressions using a compact core
calculus according to LeanAuto’s [25] λC type system with a countable number of non-cumulative
universe levels. Let Uℓ (ℓ ∈ N) denote the sorts, let V denote the set of variables, and let Σ denote the set
of constants. The syntax of expressions is inductively defined as follows:

                   T ::= V | Σ | Uℓ | T T | λ (V : T ). T | ∀(V : T ). T | let (V : T ) := T ; T.

Here, T T denotes function application, λ (V : T ). T denotes λ -abstraction, ∀(V : T ). T denotes a de-
pendent product type, and let (V : T ) denotes a let-binding. For example, Real.sin x corresponds to
T T with head constant Real.sin and variable x, and HAdd.hAdd a b corresponds to ((HAdd.hAdd a) b),
i.e., nested applications using T T . Similarly, fun x : Real => Real.sin x + 1 corresponds to λ (x :
R). ((+) (sin x)) 1 after elaboration, where + is a constant such as HAdd.hAdd with implicit and instance
arguments inserted.

2.3    Helper Functions
We use the following helper functions for notational convenience in algorithm descriptions. Let ⊥ denote
the empty string. LLM(prompt) queries a language model with an input prompt string prompt and
outputs a response string. Python(code) executes a Python program string code and returns its standard
output and standard error. Lean(code) compiles a Lean program string code and returns error_message.
When code is composed of a theorem statement and proof, error_message = ⊥ indicates that the proof is
correctly verified. We refer to general LLMs as models trained for broad tasks, such as GPT-5.4 [27]
and Qwen3 [38], and to prover LLMs as models fine-tuned for formal theorem proving in Lean, such as
Goedel-Prover-V2 [15].

2.4    Answer-Construction Formulations
We model the answer-construction problem as a functional-synthesis problem: synthesize a mathematical
object (an answer function) satisfying given specifications, together with a machine-checkable proof

4
Formally Solving Answer-Construction Problems in Lean                                              J. Sun et al.


of correctness. Let D be the universe of discourse, and let V = X ∪ Y be the variables, including
context variables X = ⟨x1 , . . . , xn ⟩ and answer variables Y = ⟨y1 , . . . , ym ⟩. The hypothesis predicate
P(X) denotes the constraint for context variables, and the conclusion predicate Q(X,Y ) denotes the
constraint for both context and answer variables. Given any X satisfying P(X), the answer function
Ψ(X) = ⟨ψ1 (X), . . . , ψm (X)⟩ must map each such X to either a witness Y satisfying Q(X,Y ) (find-any
problem) or the set of all witnesses Y satisfying Q(X,Y ) (find-all problem). In particular, a find-any
problem is written as ∃Ψ.∀X.P(X) → Q(X, Ψ(X)), and a find-all problem is written as ∃Ψ.∀X.P(X) →
∀Y (Y ∈ Ψ(X) ↔ Q(X,Y )). The admissible vocabulary A is the set of allowed constants that can appear
in the expression of constructed answers, and the answer Ψ is said to be admissible if all constants it
uses are in A. Overall, each answer-construction problem is specified by the 5-tuple T = (D,V, P, Q, A).
When the context is clear, we use T to denote the formalized Lean statement for the answer-construction
task, and TΨ to denote the statement after the ∃ is eliminated by substituting the explicit Ψ. We say that a
proof successfully solves the answer-construction problem T if it compiles without error in Lean and the
constructed answer in the proof is admissible.

Example 1. The AIME II P8 example in Figure 1 is a find-any problem. In fact, it does not have any
free context variables, so X := ∅ and P := True. The only answer variable is Y = ⟨y1 ⟩ in domain D = N,
which is essentially the minimum possible value of the edge length AB in the problem. Notice that this
problem can equivalently be stated as “find the least positive integer x such that there exist positive
integers y, z with y < 2x, z2 (2x + y) = xy2 , and 6(2x
                                                      + y) = 125(y + 2z)” by translating the geometric
information into algebraic form. Thus, Q(y1 ) := y1 = min{y ∈ N : ∃z1 , z2 ∈ N, (y, z1 , z2 > 0) ∧ 2y >
                                                          
z1 ∧ z22 (2y + z1 ) = yz21 ∧ 6(2y + z1 ) = 125(z1 + 2z2 )} . The formalized statement is obtained from this
information. Since the AIME competition requires the synthesized Ψ to be a canonical natural number
without arithmetic operations, the admissible vocabulary is A =[OfNat.ofNat].


3     Related Work
Prover LLMs in Lean. Interactive theorem provers (ITPs) such as Isabelle [23] and Lean [21] support
human-friendly environments for proof development. Lean supports built-in proof automation tactics
such as LeanSMT [20] and aesop [14]. Recent prover LLMs combine these formal environments with
large-scale proof search and training on a vast formal corpus. Open-weight prover LLMs such as Goedel-
Prover [15], DeepSeek-Prover [26, 36, 37], InternLM-Prover [42], and Kimina-Prover [34] substantially
improve Lean proof success on standard Lean theorem-proving benchmarks such as miniF2F and
PutnamBench. Inference-time techniques like Seed-Prover [5] and Aristotle [1] maintain lemma pools
of proved conjectures to optimize the efficacy of prover LLMs and achieve silver- to gold-medal-level
results in IMO. These systems are primarily evaluated on theorem-proving (non-answer-construction)
problems with specified conclusions, whereas our answer-construction setting focuses on tasks with
existentially quantified answer variables.

Answer-Construction Systems. Several systems address answer-construction problems. PyEuclid [12]
combines an AlphaGeometry-style deduction engine [31] with algebraic computation to solve Euclidean
geometry calculation problems with proofs in a geometry DSL. FPS [18] studies general answer-
construction problems in Lean 4 through a search-based algorithm, and reports solving 1 PutnamBench
problem in the answer-construction format. High-performance formal reasoning engines have also shown
strong results on Olympiad-level problems. AlphaProof [11] solved three out of six IMO 2024 problems
in Lean 4 and one more problem in the AlphaGeometry DSL, contributing to silver-medal performance. It
also leverages general LLMs for answer-construction problems to sample hundreds of candidate answers

                                                                                                              5
Formally Solving Answer-Construction Problems in Lean                                          J. Sun et al.


and attempt proofs on the substituted Lean statements. However, AlphaProof’s model weights and
implementation are closed-source. Moreover, its training and inference pipelines are substantially more
expensive: in fact, AlphaProof reports around 180,000 TPU-days of Google v6e for data processing and
reinforcement learning, several orders of magnitude more compute than our experiments use.


Formal Benchmarks. General formal benchmarks such as MiniF2F [44], FIMO [16], LeanWork-
Book [41], ProofNet [2], and FormalMath [43], as well as domain-specific benchmarks like LeanGeo [28]
(geometry), MO-INT [35] (inequality), and FormalML [40] (machine learning theory), are constructed
by formalizing raw informal mathematics from math textbooks and past competition problems. These
benchmarks focus on formal theorem-proving problems, and the ground-truth answers are substituted
into the statements during formalization if the raw informal statements are answer-construction problems.
PutnamBench [33] (Putnam competition) and CombiBench [17] (combinatorics) include some answer-
construction problems. However, most methods still evaluate on the reduced theorem-proving versions of
problems, and there is no formal mechanism to detect the admissibility of candidate constructed answers.


4     Methods
In this section, we describe the main workflow of ECP. Prior to problem solving, we first preprocess the
raw answer-construction problems into Lean formalizations with admissible vocabularies according to
the template in Section 2.4. Then ECP solves the answer-construction problem as follows. (i) During the
Enumerate and Conjecture stages, the general LLM constructs an answer by first performing bounded
Python enumeration and then generalizing to the broader case to conjecture an admissible answer in Lean.
(ii) During the Prove stage, the constructed answer is substituted into the theorem statement and the
prover LLM generates the proof with automation tactics. ECP returns to the Enumerate and Conjecture
stage if the substituted statement can be disproved. An overview of ECP is shown in Figure 3. We explain
each stage in detail in the subsequent subsections.

                       Problem      Preprocess          Enumerate     Python
                                                                                     LLM
                                                                                     I/O
                                                                     Admissibility
                         Proof         Prove            Conjecture    Checking



                                                          Lean

                                 Figure 3: An overview of the ECP workflow.



4.1    Preprocess Stage
Autoformalization. During the Preprocess stage, the raw informal problem statement in natural
language is converted into a formal problem with an admissible vocabulary according to the problem
formulation template in Section 2.4. Specifically, we prompt a general LLM with the raw informal
problem and instructions for producing the problem formulation according to the template in Appendix H,
and ask it for a compilable formalization. Each formalization is validated using Lean compilation for
syntax correctness and manual inspection for equivalence to its informal statement. Failed formalizations
are sent to the LLM for repair. Using this approach, we autoformalized the 75 problems in the 2026
MathArena Final Answer Competitions [3], consisting of 30 AIME problems, 33 HMMT (Harvard-MIT
Mathematics Tournament) problems, and 12 Apex problems. In addition, out of 672 existing formalized

6
Formally Solving Answer-Construction Problems in Lean                                                 J. Sun et al.


problems in PutnamBench [33], we found that 346 are answer-construction problems and processed them
into our problem formulation.


Admissible Vocabularies. We label the admissible vocabularies for each problem using rule-based
heuristics according to each problem’s source and answer type. In particular, we design three levels of
vocabulary breadth for different problem sources: (i) basic numbers without arithmetic operations (for
AIME problems in MathArena); (ii) expressions with elementary arithmetic operations such as +, −, ×,
and ÷ (for HMMT and Apex problems in MathArena); (iii) expressions with university-level constants
(for PutnamBench problems). We also infer vocabularies from answer types: if the expected answer
has tuple-, set-, or function-related constructor constants, detected by occurrences of ×, Set, or → in the
answer type, we include additional vocabulary accordingly.
    After labeling, we run a validation test to examine whether each problem’s labeled admissible
vocabulary covers the constants actually used in the ground-truth answer. We found that all 75/75
MathArena problems and 301/346 (87.0%) PutnamBench problems passed validation. We discovered
that the remaining 45/346 (13.0%) PutnamBench problems have complicated answer formats and
manually fixed them as described in Appendix G.1.


4.2    Admissibility Checking
In addition to semantic correctness, answer-construction problems in Lean require that the synthesized
answer be admissible, meaning that it is composed of constants in the admissible vocabulary. For
example, in the AIME II P8 example in Figure 1, answers like 1 or 245 are admissible, but answers like
sInf Property are inadmissible. To check admissibility, it is sufficient to extract the constants used by
the answer Ψ following Lean’s expression syntax from Section 2.2. Let Σ be the set of global constants,
let A ⊆ Σ be the admissible vocabulary, and let Aadmin ⊆ Σ denote the set of administrative constants that
arise from the Lean compiler runtime, including type formers, typeclass instances, instance-producing
constants, and compiler-generated private constants. We ignore constants in Aadmin during admissibility
checking.
    For an application expression t, we use spine decomposition: t = h a1 a2 · · · an , where h is the head
and a1 , . . . , an are the arguments. We define ExplicitArgs(t) using Lean’s elaborated function-argument
metadata for explicit binders. In the projection case, πi denotes the corresponding field projection
constant. The constants used by the expression t, UsedConstants(t), are inductively defined as follows:
                              
                              
                              {c}                                          t = c, c ∈ Σ \ Aadmin
                                          UsedConstants(t ′ )
                                   [
                              
                              
                              
                                                                           t = λ (x : A). b
                              
                                ′
                               t ∈{A,b}
                              
                                          UsedConstants(t ′ )
                                   [
                                                                            t = ∀(x : A). B
                              
                              
                              
                              
                              t ′ ∈{A,B}
                              
                              
                                            UsedConstants(t ′ )
                                    [
           UsedConstants(t) =                                               t = let (x : A) := u; v            (1)
                               t ′ ∈{A,u,v}
                              
                              
                              
                              
                               UsedConstants(t ′ ) ∪ {πi }                  t = πi (t ′ )
                              
                              
                              
                              
                                                      UsedConstants(t ′ )
                                         [
                                                                            t = h a1 · · · an
                              
                              
                              
                              
                                 ′
                              
                              
                              
                              t ∈{h}∪ExplicitArgs(t)
                              
                               0/                                           otherwise

   We define admissibility of the constructed answer Ψ with respect to A, Admissible(A, Ψ), as
UsedConstants(Ψ) ⊆ A. Existential and universal quantifiers require slightly different handling. First, ∃

                                                                                                                 7
Formally Solving Answer-Construction Problems in Lean                                                                                        J. Sun et al.


can be treated as the constant Exists because the expression ∃(x : A).B is elaborated as Exists (fun
x: A => B) in Lean. This expression is handled by the application case t = h a1 · · · an , with Exists as
the head h, together with the lambda-abstraction case t = λ (x : A).b for (fun x: A => B). Second, if ∀
is not allowed, then the expression t is inadmissible whenever the case t = ∀(x : A).B is executed during
UsedConstants(t).

4.3       Enumerate and Conjecture Stage
During the Enumerate and Conjecture stage, ECP is given the Lean answer-construction problem
statement T and the expected answer type. It first writes Python programs for bounded enumeration
(Enumerate stage), then constructs an answer that generalizes from enumeration with mathematical
reasoning (Conjecture stage), as described in Algorithm 1.

LLMs with Tool Calling. General LLMs, such as the commercial model GPT-5.4 and the open-source
local model Qwen3, support reasoning with tool calls for code generation and execution. In particular,
the LLM encloses tool calls (code content) inside delimiters <tool_call>...</tool_call> under the
OpenAI function-calling JSON schema. The compiler backend executes the tool call and adds stdout and
stderr to the rollout response using delimiters <tool_response>...</tool_response> immediately
after </tool_call>. For fast and parallel code execution, we deploy the SandboxFusion [4] server as
the code interpreter backend, and we restrict the tool interface to Python calls. Let ParseToolCall denote
the helper function that extracts the tool call from a response.

Enumerate Stage. Initially, the prompt is built from the system instruction template in Appendix H and
the input examples. ECP first queries a general LLM to write one or more Python programs to directly
solve for the answer or search for tuples (X,Y ) satisfying P(X) ∧ Q(X,Y ) over bounded and tractable
values, as shown in Lines 2–7 in Algorithm 1. Each Python program is executed by SandboxFusion,
and each program and its output are added back to the context. There may be multiple rounds of
tool calls, depending on whether the enumeration results have provided sufficient evidence for answer
construction. When the LLM no longer generates tool calls or hits max_enumerate_rounds, it proceeds
to the Conjecture stage.

                              Enumerate Traces                                               Conjecture Traces
                Round 1                               Round 2

    import sympy as s                  for x in range(1, 1000):
                                                                              Let 6(2x + y) = 125(y + 2z).
    r=s.symbols('r')                     for y in range(1, 2 * x):
                                                                              Write 2x + y = 125k, y + 2z = 6k.
    poly=2*r**3-125*r**2-1500*r+4500       for z in range(1, 1000):
                                                                              Parity condition implies y = 2a, k = 2n.
    print(s.factor(poly))                    if (z*z*(2*x + y) == x*y*y and
                                                                              Write r = a/n.
    print(s.nroots(poly))                    6*(2*x + y) == 125*(y + 2*z)):
                                                                              The equation becomes 2r ! − 125𝑟 " − 1500r + 4500 = 0. The   Admissible
                                                print(x, y, z)
                                                                              only rational root is r = 5/2.
                                                break
                                                                              Write n = 2m. Then a = 5m, n = 2m gives x= 245m. The least   Compilable
    Output:                                                                   positive integer is x = 245.
    (2*r - 5)*(r**2 - 60*r - 900)      Output:                                <<< 245 >>>
    [-12.426…, 2.5, 72.426…]           245 10 7



Figure 4: LLM traces for solving AIME II P8 (2026) during the Enumerate (Left) and Conjecture (Right)
stages. The Conjecture trace is manually compacted due to the page limit.


Conjecture Stage. During the Conjecture stage, the LLM sees the Python programs and execution
results produced by the Enumerate stage, performs mathematical reasoning toward the answer construc-
tion by generalizing beyond bounded enumerations, and proposes the explicit final answer Ψ inside
the delimiter <<<. . . >>> for extraction (denoted by ExtractAnswer(response)). ECP then runs Lean
compilation and an admissibility check for the constructed answer, and returns the answer for repair if it
fails either test.

8
Formally Solving Answer-Construction Problems in Lean                                            J. Sun et al.


Algorithm 1 ConstructAnswer(T, FailedAnswers = ⊥)
 1: context ← BuildPrompt(T, FailedAnswers)
 2: for i ← 1 to max_enumerate_rounds do
 3:   response ← LLM(context)
 4:   code ← ParseToolCall(response)
 5:   if code = ⊥ then
 6:       break
 7:   context ← context + code + Python(code)
 8: for i ← 1 to max_conjecture_rounds do
 9:   response ← LLM(context)
10:   Ψ ← ExtractAnswer(response)
11:   error_message ← Lean(Ψ)
12:   is_admissible ← Admissible(A, Ψ)
13:   if error_message = ⊥ and is_admissible then
14:       return Ψ
15:   if error_message ̸= ⊥ then
16:       context ← context + Ψ + error_message
17:   if not is_admissible then
18:      context ← context + Ψ + “inadmissible”
19: return ⊥

    An explicit example of LLM traces during answer construction for AIME II P8 (2026) is shown in
Figure 4. During the Enumerate stage, the LLM first uses SymPy to solve for a key equation with rational
root r = 52 and writes a brute-force enumeration to print the smallest valid answer. In the Conjecture
stage, it leverages the key enumerated results, performs mathematical reasoning, and concludes that the
answer is 245, which compiles in Lean and is admissible.


4.4    Prove Stage
After the Conjecture stage, the constructed answer is substituted into the theorem statement to form TΨ
using the Lean tactic use Ψ. The goal of the Prove stage is to find a proof of TΨ . It first applies Lean’s
automation engines, denoted by Auto, by sequentially applying the automation tactics native_decide,
simp, aesop [14], ring, and norm_num. If automation fails, it invokes a prover LLM with a repair
loop that incorporates error messages from unsuccessful attempts, as shown in Algorithm 2. In practice,
this procedure runs for multiple parallel independent attempts and succeeds if any attempt outputs a
successful proof.
    In ECP, Prove is invoked for both TΨ and its negation ¬TΨ . A successful Prove(TΨ ) concludes
the ECP loop; if Prove(¬TΨ ) succeeds, ECP adds Ψ to the failed answer collection and returns to the
Enumerate and Conjecture stage for answer reconstruction. We leave the full proof of the AIME II P8
example in Figure 1 to Appendix D.2.


4.5    Equivalence Testing for Answers
In addition to end-to-end proof generation, this approach naturally applies to equivalence checking
between the ground-truth answer Ψground_truth and a constructed answer Ψ by proving the Lean goal
Ψ = Ψground_truth , when the problem has a find-all type or a find-any type with a unique answer. This test
uses the fixed tactic portfolio and prover LLMs described in Section 4.4, making the check type-aware
and certified whenever it succeeds. It can also prove equivalences that may be missed by script-based
symbolic checkers, such as MathArena’s evaluation protocol [3], or by traditional LLM judges.

                                                                                                            9
Formally Solving Answer-Construction Problems in Lean                                     J. Sun et al.


Algorithm 2 Prove(TΨ )
 1: for j ← 1 to parallel_proof_samples do
 2:   feedback ← ⊥
 3:   error_message ← Lean(TΨ + automation)
 4:   if error_message = ⊥ then
 5:      return automation
 6:   for i ← 1 to max_prove_rounds do
 7:      proof ← LLM(TΨ + feedback)
 8:      error_message ← Lean(proof)
 9:      if error_message = ⊥ then
10:         return proof
11:      feedback ← proof + error_message
12: return ⊥

Algorithm 3 ECP(T )
 1: FailedAnswers ← ⊥
 2: for r ← 1 to max_ecp_rounds do
 3:   Ψ ← ConstructAnswer(T, FailedAnswers)
 4:   if Ψ = ⊥ then
 5:      return ⊥
 6:   proof ← Prove(TΨ )
 7:   disproof ← Prove(¬TΨ )
 8:   if proof ̸= ⊥ then
 9:      return use Ψ; + proof
10:   if disproof ̸= ⊥ then
11:      FailedAnswers ← FailedAnswers + Ψ
12:      continue
13:   break
14: return ⊥

5     Evaluation
In this section, we evaluate ECP against baseline methods for solving answer-construction problems
across multiple math competition benchmarks in Lean. The evaluated benchmarks span difficulty levels
from high school to university and include contamination-free problems beyond the evaluated models’
knowledge cutoffs. Our evaluation aims to answer the following research questions (RQs):

RQ 1. Problem-Solving Accuracy. Can ECP successfully solve more answer-construction problems in
      Lean than baseline methods?

RQ 2. Answer-Only Accuracy. Can ECP predict more correct answers without proof for answer-
      construction problems than baseline methods?

RQ 3. Cost Efficiency. Can ECP solve formal answer-construction problems at a lower cost than
      baseline methods?

RQ 4. Ablation Studies. What are the contributions of each component in ECP?

Dataset Setup. We evaluate on two benchmarks: PutnamBench [33] and MathArena [3]. PutnamBench
originally includes 672 Putnam Mathematical Competition problems from 1962–2025 that are manually

10
Formally Solving Answer-Construction Problems in Lean                                                                 J. Sun et al.


formalized in Lean 4 by human experts. We extract the subset of 346 instances that are answer-
construction problems. The MathArena Final Answer Competitions benchmark2 [3] contains 75 problems
from the AIME I, AIME II, HMMT (February), and Apex competitions in 2026, all of which are
contamination-free for the evaluated models according to Table 1. Since the raw MathArena problems
are originally written in natural language, we preprocess them into the target formulation of answer-
construction problems following Section 4.1. Figure 5 summarizes the MathArena sources and domains.




                            APEX 2026
                          (12 Problems)                                                               Combinatorics
                                                                                      Algebra         (28 Problems)
           AIME I 2026                                                             (9 Problems)
          (15 Problems)

                                          HMMT Feb 2026                        Number Theory
                                           (33 Problems)                       (14 Problems)
              AIME II 2026
             (15 Problems)                                                                          Geometry
                                                                                                  (24 Problems)




                     (a) Sources                                                          (b) Domains
                                 Figure 5: Problem sources and domains for MathArena 2026.


Hyperparameter Setup. We evaluate the general LLMs
GPT-5.4 and Qwen3-32B, and the prover LLM Goedel- Dataset / Model                 Knowledge Cutoff
Prover-V2-32B. For the ECP setup, we set the Enumerate,
                                                            PutnamBench [33]          1962–2025
Conjecture, and ECP round limits to 10, 5, and 2, respec- MathArena [3]             After Feb 2026
tively. For the Prove stage, we use 4 and 32 parallel proof
samples and a maximum of 3 prove rounds. Lean compi- GPT-5.4 [27]                 Before Aug 31, 2025
lation is conducted on 64 AMD EPYC 9655 CPU cores           Qwen3-32B  [38]       Before Mar 31, 2025
                                                            Goedel-Prover-V2 [15] Before Aug 5, 2025
in parallel with a 120-second timeout. The Qwen3 and
Goedel-Prover-V2-32B models are deployed on 4 H100 Table 1: Knowledge cutoffs of evaluated
SXM (80GB) GPUs in parallel. The GPT-5.4 model is datasets and models.
queried via the OpenAI API platform. The default model
setup of ECP uses GPT-5.4 for the Enumerate and Conjecture stages, and Goedel-Prover-V2-32B for the
Prove stage.

Metric Setup. For RQ 1, we evaluate ECP’s and the baseline models’ accuracy for answer-construction
problem solving. A proof is said to successfully solve problem T if it compiles in Lean without
error and the constructed answer in the proof is admissible, as described in Section 2. Recall that
parallel_proof_samples in ECP’s Prove is aligned to the Pass@k accuracy metric, which generates k
independent parallel outputs and succeeds if any proof is successful. We also compare baseline LLMs
GPT-5.4 and Goedel-Prover-V2-32B without ECP under the same Pass@k and proof-correction attempt
settings, meaning that they have the same parallel_proof_samples, max_prove_rounds, and access to the
proof automation portfolio. For RQ 2, we focus on answer prediction without proof. That is, we only
    2 Source: https://matharena.ai/?comp=overall–final_answer_comps&view=problem



                                                                                                                               11
Formally Solving Answer-Construction Problems in Lean                                                              J. Sun et al.


evaluate the number of constructed answers that are provably equivalent to the ground-truth answers of
each dataset. For RQ 3, we report the API costs and GPU hours of the methods. The OpenAI API rates
of GPT-5.4 are 2.5 USD per 1M input tokens and 15.0 USD per 1M output tokens. Our GPUs are on
computing clusters, but we assume the H100 GPU hourly rate is 2.0 USD3 to normalize costs. For RQ
4, we analyze the effects of the Enumerate stage, answer reconstruction, proof repair, and admissibility
checking.

5.1      RQ 1: Problem-Solving Accuracy
ECP successfully solves more instances than baseline LLMs on both the MathArena and PutnamBench
benchmarks, as shown in Table 2. In particular, on MathArena, the strongest LLM-only baseline GPT-5.4
solves 13/75 problems at Pass@32, while ECP with GPT-5.4 answer construction and Goedel-Prover-
V2-32B solves 18/75. On PutnamBench, due to the high cost (projected at approximately 1400 USD)
of GPT-5.4 baselines with Pass@32, we omit this setup and compare ECP with the GPT-5.4 baseline
under Pass@4: ECP and GPT-5.4 solve 9/346 and 8/346 problems, respectively. With the Pass@32
budget, ECP solves 17/346 problems. The complete lists of solved instances are given in Appendix B
and Appendix C. Overall, ECP gives the strongest end-to-end accuracy on both benchmarks under the
evaluated budgets.
                                                            High School (MathArena 2026)                     Undergraduate
Method                           Pass@k
                                           AIME I (15)   AIME II (15)   HMMT (33)   Apex (12)   Total (75)   PutnamBench (346)
LLM Baselines
                                    4       3 (20.0%)      1 (6.7%)     2 (6.1%)    0 (0.0%)     6 (8.0%)        6 (1.7%)
  Goedel-Prover-V2-32B
                                    32      4 (26.7%)      1 (6.7%)      2 (6.1%)   0 (0.0%)     7 (9.3%)        7 (2.0%)
                                    4       2 (13.3%)     2 (13.3%)     3 (9.1%)    0 (0.0%)     7 (9.3%)        8 (2.3%)
  GPT-5.4
                                    32      6 (40.0%)     2 (13.3%)     5 (15.2%)   0 (0.0%)    13 (17.3%)           -
ECP (Ours)
                                    4       6 (40.0%)     4 (26.7%)     6 (18.2%)   0 (0.0%)    16 (21.3%)        2 (0.6%)
  GPT-5.4+Goedel-Prover-V2-8B
                                    32      6 (40.0%)     4 (26.7%)     7 (21.2%)   0 (0.0%)    17 (22.7%)        7 (2.0%)
                                    4       6 (40.0%)     4 (26.7%)     7 (21.2%)   0 (0.0%)    17 (22.7%)        9 (2.6%)
  GPT-5.4+Goedel-Prover-V2-32B
                                    32      6 (40.0%)     5 (33.3%)     7 (21.2%)   0 (0.0%)    18 (24.0%)       17 (4.9%)

     Table 2: Solved instances by Pass@k setup across MathArena subcategories and PutnamBench.


5.2      RQ 2: Answer-Only Accuracy
ECP can predict more correct answers than baseline methods, resulting in fewer proof failures due
to incorrectly constructed answers. Table 3 focuses only on answer construction without considering
proofs. For GPT-5.4, ECP improves MathArena correct answer construction from 58/75 to 68/75 and
PutnamBench answer construction from 290/346 to 303/346. Similar gains appear for the smaller
open-source model Qwen3-32B, which improves from 35/75 to 39/75 on MathArena and from 201/346
to 217/346 on PutnamBench. We also record statistics for Enumerate-stage tool calls for ECP equipped
with GPT-5.4. In particular, more than 50% of the instances use at least two tool calls. The number of
tool calls increases with problem difficulty. For AIME problems, the easiest exam in MathArena, ECP
uses about 2.5 tool calls on average, while for Apex problems, this rises to 8.2 tool calls. Overall, ECP
enables solving more answer-construction problems by correctly predicting more answers, largely due to
bounded enumeration.



     3 Source: Vast AI’s H100 pricing: https://vast.ai/pricing/gpu/H100-SXM



12
Formally Solving Answer-Construction Problems in Lean                                                                                                               J. Sun et al.


                                                                         High School (MathArena 2026)                                                    Undergraduate
Method         Setting
                                                   AIME I (15)      AIME II (15)           HMMT (33)              Apex (12)            Total (75)        PutnamBench (346)
                ECP                                    14                    15                    32                    7                  68                     303
GPT-5.4
               Baseline                                13                    15                    26                    4                  58                     290
                ECP                                    12                    12                    14                    1                  39                     217
Qwen3-32B
               Baseline                                12                     9                    13                    1                  35                     201

                                                    Table 3: Answer-only accuracy by model and setting.

                                                                     42.5%                                                                   matharena
                                           40.0%                                                                                             putnam
                                                                 37.3%
                                           35.0%
                                                                                                                                           30.7%
                                           30.0%
                  Percentage of Problems




                                                                                  26.6%
                                           25.0%

                                           20.0%

                                           15.0%                              14.7%
                                                                                            12.0%                                                11.0%
                                           10.0%                                                    9.2%
                                                                                                                  6.1%
                                            5.0%                                                                                    4.6%
                                                                                                           2.7%              2.7%
                                            0.0%     0.0% 0.0%
                                                         0           1            2             3              4                5             6+
                                                                                        Number of Tool Calls

Figure 6: Distribution of Python tool-call counts for GPT-5.4 answer construction in the ECP workflow
with tools enabled on MathArena and PutnamBench. The 6+ column aggregates all runs with at least 6
tool calls.


5.3    RQ 3: Cost Efficiency

             Method                                    Dataset           Pass@k       GPT-5.4 (USD)        Goedel-Prover (USD / GPU hours)                Total
             GPT-5.4                                   MathArena           32             341.2                              0.0                          341.2
             ECP                                       MathArena           32              8.6                     102.0 (51.0 GPU hours)                 110.6
             GPT-5.4                                   PutnamBench          4              178.8                            0.0                            178.8
             GPT-5.4 (Projected)                       PutnamBench         32             1430.4                            0.0                           1430.4
             ECP                                       PutnamBench         32               24.5                  450.0 (225.0 GPU hours)                 474.5

Table 4: Total cost of GPT-5.4 and Goedel-Prover-V2-32B models for ECP and GPT-5.4 baselines. For
the GPT-5.4 baseline on PutnamBench (Pass@32), the cost is projected from its Pass@4 experiment
result.

    ECP operates at a lower cost than LLM-only baselines while achieving better results. GPT-5.4 is
much more expensive than locally deployable models like Goedel-Prover-V2-32B. ECP assigns answer
construction to GPT-5.4 and heavier proof generation with multiple samples to Goedel-Prover-V2-32B,
taking advantage of the cost efficiency and proving performance of Goedel-Prover-V2-32B and the
accurate answer construction of GPT-5.4. Under aligned Pass@k (parallel_proof_samples) for proof
generation, ECP outperforms the GPT-5.4 baseline while operating at only one-third of the GPT-5.4
baseline cost. On PutnamBench (Pass@32), the GPT-5.4 baseline has a projected cost of approximately
1400 USD (estimated by multiplying its Pass@4 cost by 8), while ECP costs approximately 475 USD
(which only includes 24.5 USD of OpenAI API cost) because it uses the cheaper locally deployable
Goedel-Prover-V2-32B for proof generation.

                                                                                                                                                                             13
Formally Solving Answer-Construction Problems in Lean                                         J. Sun et al.


5.4    RQ 4: Ablation Studies

Problem Solving. We perform ablation studies to evaluate the main design choices of ECP for answer-
construction problem solving. Table 5 reports end-to-end ablations for the default ECP configuration
when using a smaller prover model, disabling proof correction, and disabling proof automation. Each
ablated case results in accuracy degradation in at least one benchmark. On the high-school MathArena
benchmark, the main degradation comes from removing the proof automation portfolio, which causes 7
fewer solved instances, while on the more difficult undergraduate PutnamBench benchmark, switching to
a weaker prover LLM causes 10 fewer solved instances. Overall, problem-solving performance depends
on both the prover model selection and proof-generation techniques.

                   Variant                              MathArena (75)   PutnamBench (346)
                   ECP (original)                             18                 17
                   - Smaller prover LLM (v1)                17 (-1)            7 (-10)
                   - Disable proof correction (v2)          16 (-2)            16 (-1)
                   - Disable proof automation (v3)          11 (-7)              17

Table 5: Ablation results for answer-construction problem solving. The red parentheses show decreases
relative to ECP. Original ECP uses GPT-5.4 for the Enumerate and Conjecture stages, and Goedel-
Prover-V2-32B for the Prove stage, including proof correction and automation. ECP v1 (smaller prover
LLM) uses Goedel-Prover-V2-8B for the Prove stage; ECP v2 disables proof correction by setting
max_prove_rounds = 1; ECP v3 disables the portfolio of proof automation tactics.




Answer Prediction. We focus on answer-only accuracy and ablate the effects of the Enumerate stage
and answer reconstruction. Table 6 reports the answer-only results for the default ECP setup and the
ablated cases of disabling the Enumerate stage and answer reconstruction upon disproof. The negative
effect of disabling the Enumerate stage is significant: on each benchmark, there are at least 10 fewer
solved instances. Answer reconstruction helps recover the answer for 1 instance in MathArena. Therefore,
the gains in answer-only accuracy mostly come from the Enumerate stage and its bounded enumeration
results, while disproof-guided answer reconstruction has a smaller effect.

                   Variant                              MathArena (75)   PutnamBench (346)
                   ECP (original)                             68               303
                   - Disable Enumerate stage (v1)          58 (-10)          290 (-13)
                   - Disable reconstruction (v2)            67 (-1)            303

Table 6: Ablation results for answer prediction. The red parentheses show decreases relative to ECP.
Original ECP uses GPT-5.4 for the Enumerate and Conjecture stages. ECP v1 disables the Enumerate
stage; ECP v2 disables answer reconstruction upon a disproved substituted statement.




Admissibility Checking. We study the effects of admissibility checking in problem solving by com-
paring two evaluation metrics: (i) our standard metric that requires both Lean compilation of the proof
and admissibility checking for the constructed answer; (ii) the naive metric that requires only Lean
compilation.

14
Formally Solving Answer-Construction Problems in Lean                                           J. Sun et al.


                    Method                              MathArena       PutnamBench
                    ECP                                   18+0               17+0
                    GPT-5.4 baseline                      13+19             8+134
                    Goedel-Prover-V2-32B baseline         7+18              7+99
Table 7: Solved instances under two metrics: (i) the standard metric, enforcing both Lean compilation
and admissibility checking; (ii) the naive metric, enforcing only Lean compilation. Each entry is a + b,
where a denotes solved instances under the standard metric, while b denotes the number of spurious
“solved” instances under the naive metric without enforcing admissibility checking.

    Table 7 shows that direct LLM baselines for answer-construction problem solving are highly vulnera-
ble to proofs with inadmissible answers: under the naive metric, GPT-5.4 and Goedel-Prover-V2-32B
produce 19 and 18 additional spurious solves on MathArena, and 134 and 99 on PutnamBench, re-
spectively. These proofs compile in Lean, but Lean compilation alone cannot detect witnesses that
circularly restate the target property or otherwise fall outside the admissible vocabulary, as illustrated
in Appendices D.3 and E. ECP avoids this failure mode by separating answer construction from proof
generation, assigning them to specialized models, and checking Admissible(A, Ψ) before proving the
substituted statement TΨ . We manually inspected the instances counted under the standard metric and
found that the constructed answers and their Lean proofs are nontrivial and do not rely on circular or
trivial existential witnesses.
    Overall, ECP improves both problem-solving accuracy and answer-only accuracy over direct LLM
baselines while operating at lower cost. The ablations further show that bounded enumeration, prover
LLM selection with proof correction and automation, and admissibility checking address distinct failure
modes in solving answer-construction problems.



6     Conclusion
We introduced Enumerate-Conjecture-Prove (ECP), a neuro-symbolic framework for formally solving
answer-construction problems in Lean. Enumerate searches bounded instances with Python tool calls,
Conjecture generalizes the resulting traces into an explicit Lean answer, and Prove verifies the answer-
substituted statement with automation and prover LLMs. Admissibility checking extracts the constants
used by the constructed answer and rejects answers outside the problem-specific admissible vocabulary,
preventing circular witnesses from being counted as solutions. Empirically, ECP improves both answer-
only accuracy and end-to-end proof generation. It solves 17/346 PutnamBench answer-construction
problems and 18/75 MathArena 2026 problems (including 6 AIME I problems, 5 AIME II problems, and
7 HMMT problems) end-to-end in Lean, outperforming the strongest evaluated direct proof-generation
baselines at the reported budgets.


Limitations and Future Work. Currently, the admissible vocabulary is automatically labeled by
heuristics that partially rely on implicit information about answer formats and the mathematical knowl-
edge level required by the problem. Future work may extend this framework to broader mathematical
domains beyond competitions and incorporate admissible-vocabulary labeling into the autoformalization
procedure. Methodologically, ECP partially depends on bounded enumeration during the Enumerate
stage, which can suffer from combinatorial explosion in difficult combinatorics problems. Designing
specialized methods for Olympiad-level and research-level mathematical conjecture generation may be a
promising direction for research.

                                                                                                         15
Formally Solving Answer-Construction Problems in Lean                                         J. Sun et al.


References
 [1] Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathïs Fédérico, Sergei Gukov, Daniel Halpern-
     Leistner, Kirsten Henningsgard, Yury Kudryashov, Alexander Meiburg, et al. Aristotle: IMO-Level
     Automated Theorem Proving. arXiv preprint arXiv:2510.01346, 2025.

 [2] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev,
     and Jeremy Avigad. ProofNet: Autoformalizing and Formally Proving Undergraduate-Level
     Mathematics. arXiv preprint arXiv:2302.12433, 2023.

 [3] Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. MathArena:
     Evaluating LLMs on Uncontaminated Math Competitions, February 2025.

 [4] ByteDance. SandboxFusion.                https://github.com/bytedance/SandboxFusion, 2024.
     GitHub repository.

 [5] Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
     Xing Jin, Chenggang Li, Kaijing Ma, et al. Seed-Prover: Deep and Broad Reasoning for Automated
     Theorem Proving. arXiv preprint arXiv:2507.23726, 2025.

 [6] Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. Counterexample-guided
     abstraction refinement. In International Conference on Computer Aided Verification, pages 154–169.
     Springer, 2000.

 [7] Edmund M Clarke, Anubhav Gupta, and Ofer Strichman. Sat-based counterexample-guided
     abstraction refinement. IEEE Transactions on Computer-Aided Design of Integrated Circuits and
     Systems, 23(7):1113–1123, 2004.

 [8] George E Collins. Quantifier elimination for real closed fields by cylindrical algebraic decomposi-
     tion: a synopsis. ACM SIGSAM Bulletin, 10(1):10–12, 1976.

 [9] James H Davenport and Joos Heintz. Real quantifier elimination is doubly exponential. Journal of
     Symbolic Computation, 5(1-2):29–35, 1988.

[10] Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, and Tushar Khot. Complexity-based prompting
     for multi-step reasoning, 2023.

[11] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja
     Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal
     mathematical reasoning with reinforcement learning. Nature, pages 1–3, 2025.

[12] Zhaoyu Li, Hangrui Bi, Jialiang Sun, Zenan Li, Kaiyu Yang, and Xujie Si. Pyeuclid: A versatile for-
     mal plane geometry system in python. In International Conference on Computer Aided Verification,
     pages 405–420. Springer, 2025.

[13] Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su, Zenan Li, Xian Zhang, Kaiyu Yang, and Xujie
     Si. A survey on deep learning for theorem proving, 2024.

[14] Jannis Limperg and Asta Halkjær From. Aesop: White-Box Best-First Proof Search for Lean.
     In Proceedings of the 12th ACM SIGPLAN International Conference on Certified Programs and
     Proofs, pages 253–266, 2023.

16
Formally Solving Answer-Construction Problems in Lean                                       J. Sun et al.


[15] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
     Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
     Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover-V2: Scaling
     Formal Theorem Proving with Scaffolded Data Synthesis and Self-Correction. In The Fourteenth
     International Conference on Learning Representations, 2026.

[16] Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
     Chuanyang Zheng, Yichun Yin, Lin Li, et al. FIMO: A Challenge Formal Dataset for Automated
     Theorem Proving. arXiv preprint arXiv:2309.04295, 2023.

[17] Junqi Liu, Xiaohan Lin, Jonas Bayer, Yael Dillies, Weijie Jiang, Xiaodan Liang, Roman Soletskyi,
     Haiming Wang, Yunzhou Xie, Beibei Xiong, Zhengfeng Yang, Jujian Zhang, Lihong Zhi, Jia Li,
     and Zhengying Liu. CombiBench: Benchmarking LLM Capability for Combinatorial Mathematics,
     2025.

[18] Qi Liu, Xinhao Zheng, Renqiu Xia, Xingzhi Qi, Qinxiang Cao, and Junchi Yan. Beyond theorem
     proving: Formulation, framework and benchmark for formal problem-solving. arXiv preprint
     arXiv:2505.04528, 2025.

[19] The mathlib Community. The Lean Mathematical Library. In Proceedings of the ACM SIGPLAN
     International Conference on Certified Programs and Proofs, 2020.

[20] Abdalrhman Mohamed. Lean-SMT: Tactics for Discharging Lean Goals into SMT Solvers, 2025.

[21] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language.
     In Proceedings of the International Conference on Automated Deduction, 2021.

[22] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
     Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco JR Ruiz, Abbas Mehrabian,
     et al. Alphaevolve: A coding agent for scientific and algorithmic discovery. arXiv preprint
     arXiv:2506.13131, 2025.

[23] Lawrence C Paulson. Isabelle: A Generic Theorem Prover. Springer, 1994.

[24] George Polya. How to solve it: A new aspect of mathematical method. In How to solve it. Princeton
     university press, 2014.

[25] Yicheng Qian, Joshua Clune, Clark Barrett, and Jeremy Avigad. Lean-auto: An Interface Be-
     tween Lean 4 and Automated Theorem Provers. In International Conference on Computer Aided
     Verification, pages 175–196. Springer, 2025.

[26] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
     Zhe Fu, Qihao Zhu, Dejian Yang, et al. DeepSeek-Prover-V2: Advancing Formal Mathematical Rea-
     soning via Reinforcement Learning for Subgoal Decomposition. arXiv preprint arXiv:2504.21801,
     2025.

[27] Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart, Adi Ganesh, Ahmed El-Kishky, Aidan
     McLaughlin, Aiden Low, AJ Ostrow, Akhila Ananthram, et al. OpenAI GPT-5 System Card. arXiv
     preprint arXiv:2601.03267, 2025.

[28] Chendong Song, Zihan Wang, Frederick Pu, Haiming Wang, Xiaohan Lin, Junqi Liu, Jia Li, and
     Zhengying Liu. LeanGeo: Formalizing Competitional Geometry Problems in Lean. arXiv preprint
     arXiv:2508.14644, 2025.

                                                                                                     17
Formally Solving Answer-Construction Problems in Lean                                     J. Sun et al.


[29] Nat Sothanaphan. Resolution of Erdős Problem #728: A Writeup of Aristotle’s Lean Proof. arXiv
     preprint arXiv:2601.07421, 2026.

[30] Anja Surina, Arun Suggala, George Tsoukalas, Anton Kovsharov, Sergey Shirobokov, Francisco JR
     Ruiz, Pushmeet Kohli, and Swarat Chaudhuri. An improved last-iterate convergence rate for
     anchored gradient descent ascent. arXiv preprint arXiv:2604.03782, 2026.

[31] Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving Olympiad Geometry
     without Human Demonstrations. Nature, 2024.

[32] George Tsoukalas, Anton Kovsharov, Sergey Shirobokov, Anja Surina, Moritz Firsching, Gergely
     Bérczi, Francisco JR Ruiz, Arun Suggala, Adam Zsolt Wagner, Eric Wieser, et al. Advancing
     mathematics research with ai-driven formal proof search. arXiv preprint arXiv:2605.22763, 2026.

[33] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating Neural Theorem-Provers on
     the Putnam Mathematical Competition. arXiv preprint arXiv:2407.11214, 2024.

[34] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
     Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, et al. Kimina-prover preview: Towards large
     formal reasoning models with reinforcement learning. arXiv preprint arXiv:2504.11354, 2025.

[35] Chenrui Wei, Mengzhou Sun, and Wei Wang. Proving olympiad algebraic inequalities without
     human demonstrations. Advances in Neural Information Processing Systems, 37:82811–82822,
     2024.

[36] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
     and Xiaodan Liang. DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale
     Synthetic Data. arXiv preprint arXiv:2405.14333, 2024.

[37] Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue
     Zhang, Xuan Lu, Qiushi Du, et al. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback
     for Reinforcement Learning and Monte-Carlo Tree Search. arXiv preprint arXiv:2408.08152, 2024.

[38] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
     Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 Technical Report. arXiv preprint arXiv:2505.09388,
     2025.

[39] Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri, and Dawn
     Song. Formal mathematical reasoning: A new frontier in ai. arXiv preprint arXiv:2412.16075,
     2024.

[40] Xiao-Wen Yang, Zihao Zhang, Jianuo Cao, Zhi Zhou, Zenan Li, Lan-Zhe Guo, Yuan Yao, Taolue
     Chen, Yu-Feng Li, and Xiaoxing Ma. Formalml: A benchmark for evaluating formal subgoal
     completion in machine learning theory, 2025.

[41] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and Kai Chen. Lean Workbook: A
     Large-Scale Lean Problem Set Formalized from Natural Language Math Problems. arXiv preprint
     arXiv:2406.03847, 2024.

[42] Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao, Zhaoye Fei, Yichuan Ma,
     Jiawei Hong, Kuikun Liu, Ziyi Wang, et al. InternLM-Math: Open Math Large Language Models
     Toward Verifiable Reasoning. arXiv preprint arXiv:2402.06332, 2024.

18
Formally Solving Answer-Construction Problems in Lean                                    J. Sun et al.


[43] Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
     Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. Formalmath:
     Benchmarking formal mathematical reasoning of large language models, 2025.
[44] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: A Cross-System Benchmark for
     Formal Olympiad-Level Mathematics. In Proceedings of the International Conference on Learning
     Representations, 2022.




                                                                                                  19
Formally Solving Answer-Construction Problems in Lean                                         J. Sun et al.


A      Artifact Evaluation
We release the repository at https://github.com/sunjia72/ecp-lpar with README and LICENSE files.
The data are in data/dataset/, the implementation is in src/, and the experiment logs are in
output_artifact_eval.


B     List of 17 PutnamBench Problems Solved by ECP
                      1970s                      1980s            1990s–2000s
                      putnam_1975_a1             putnam_1984_b2   putnam_1990_a1
                      putnam_1975_b1             putnam_1985_a3   putnam_1990_a5
                      putnam_1977_a2             putnam_1985_a4   putnam_1991_a2
                      putnam_1977_a3             putnam_1986_a1   putnam_1999_a1
                                                 putnam_1986_b1   putnam_1995_b4
                                                 putnam_1988_b2   putnam_1998_b1
                                                                  putnam_2005_b1

The proof files for this list are stored at output_artifact_eval/putnam_gpt-5_mcp_Goedel-
Prover-V2-32B/successful_proofs.jsonl in the released artifact.


C      List of 18 MathArena 2026 Problems Solved by ECP
                      AIME I                    AIME II           HMMT February
                      P2026AIMEI_1              P2026AIMEII_1     P2026HMMT_1
                      P2026AIMEI_3              P2026AIMEII_4     P2026HMMT_4
                      P2026AIMEI_5              P2026AIMEII_6     P2026HMMT_10
                      P2026AIMEI_7              P2026AIMEII_8     P2026HMMT_12
                      P2026AIMEI_12             P2026AIMEII_15    P2026HMMT_14
                      P2026AIMEI_13                               P2026HMMT_21
                                                                  P2026HMMT_23

The proof files for this list are stored at output_artifact_eval/matharena_gpt-5_mcp_Goedel-
Prover-V2-32B/successful_proofs.jsonl in the released artifact.


D      Proof of AIME II Problem 8 (2026)
D.1     Default Header
Throughout the evaluation, we use the following header during proof compilation by default:
 Lean
 import Mathlib
 import Aesop
 open BigOperators Classical ENNReal Equiv EuclideanGeometry Filter Finset Fintype
 Function Lex List MeasureTheory Nat ProbabilityTheory Real SimpleGraph Real Nat
 Topology Rat


20
Formally Solving Answer-Construction Problems in Lean                         J. Sun et al.


 set_option maxHeartbeats 0


D.2     Successful Proof
 Lean


 theorem P2026AIMEII_8 : ∃ (P2026AIMEII_8_answer : Nat), (IsLeast {x : N | ∃ (y : N)
 (z : N), (0 : N) < x ∧ (0 : N) < y ∧ (0 : N) < z ∧ y < (2 : N) * x ∧ z ^ (2 : N)
 * ((2 : N) * x + y) = x * y ^ (2 : N) ∧ (6 : N) * ((2 : N) * x + y) = (125 : N) *
 (y + (2 : N) * z)} P2026AIMEII_8_answer) := by
   use (245 : Nat)
   have h245 : 245 ∈ {x : N | ∃ (y : N) (z : N), (0 : N) < x ∧ (0 : N) < y ∧ (0 :
 N) < z ∧ y < (2 : N) * x ∧ z ^ (2 : N) * ((2 : N) * x + y) = x * y ^ (2 : N) ∧ (6
 : N) * ((2 : N) * x + y) = (125 : N) * (y + (2 : N) * z)} := by

      refine' ⟨10, 7, by decide, by decide, by decide, by norm_num, _⟩
      <;> norm_num
      <;> ring_nf at *
      <;> norm_num
      <;> rfl

   have hmin : ∀ (x' : N), x' ∈ {x : N | ∃ (y : N) (z : N), (0 : N) < x ∧ (0 : N)
 < y ∧ (0 : N) < z ∧ y < (2 : N) * x ∧ z ^ (2 : N) * ((2 : N) * x + y) = x * y ^
 (2 : N) ∧ (6 : N) * ((2 : N) * x + y) = (125 : N) * (y + (2 : N) * z)} → 245 ≤
 x' := by
     intro x' hx'
     rcases hx' with ⟨y, z, hx'_pos, hy_pos, hz_pos, h_y_lt_2x', h_z_sq_eq, h_6_eq⟩
     have h1 : 245 ≤ x' := by
       by_contra! h
       have h2 : x' ≤ 244 := by linarith
       have h3 : 0 < x' := hx'_pos
       have h4 : 0 < y := hy_pos
       have h5 : 0 < z := hz_pos
       have h6 : y < 2 * x' := h_y_lt_2x'
       have h7 : z ^ 2 * (2 * x' + y) = x' * y ^ 2 := h_z_sq_eq
       have h8 : 6 * (2 * x' + y) = 125 * (y + 2 * z) := h_6_eq
       have h9 : x' ≤ 244 := by linarith

         have h10 : 12 * x' = 119 * y + 250 * z := by
           have h101 : 6 * (2 * x' + y) = 125 * (y + 2 * z) := h_6_eq
           ring_nf at h101 ⊢
           omega

         have h11 : y ≤ 24 := by
           by_contra! h11
           have h12 : y ≥ 25 := by linarith
           have h13 : 12 * x' = 119 * y + 250 * z := h10
           have h14 : 119 * y + 250 * z ≥ 119 * 25 + 250 * 1 := by
             nlinarith
           have h15 : 12 * x' ≥ 119 * 25 + 250 * 1 := by linarith
           have h16 : x' ≥ (119 * 25 + 250 * 1) / 12 := by


                                                                                       21
Formally Solving Answer-Construction Problems in Lean                           J. Sun et al.


             omega
           norm_num at h16 ⊢
           <;> omega
         have h12 : z ≤ 11 := by
           by_contra! h12
           have h13 : z ≥ 12 := by linarith
           have h14 : 12 * x' = 119 * y + 250 * z := h10
           have h15 : 119 * y + 250 * z ≥ 119 * 1 + 250 * 12 := by
             nlinarith
           have h16 : 12 * x' ≥ 119 * 1 + 250 * 12 := by linarith
           have h17 : x' ≥ (119 * 1 + 250 * 12) / 12 := by
             omega
           norm_num at h17 ⊢
           <;> omega

        interval_cases y <;> interval_cases z <;> norm_num at h10 h7 h8 ⊢ <;>
          (try omega) <;>
          (try {
             ring_nf at h7 h8 ⊢
             norm_num at h7 h8 ⊢
             <;>
             (try omega) <;>
             (try {
               have h13 : x' ≤ 244 := by linarith
               interval_cases x' <;> norm_num at h7 h8 ⊢ <;> omega
             })
          }) <;>
          (try {
             have h13 : x' ≤ 244 := by linarith
             interval_cases x' <;> norm_num at h7 h8 ⊢ <;> omega
          })
      exact h1

   have hmain : IsLeast {x : N | ∃ (y : N) (z : N), (0 : N) < x ∧ (0 : N) < y ∧ (0
 : N) < z ∧ y < (2 : N) * x ∧ z ^ (2 : N) * ((2 : N) * x + y) = x * y ^ (2 : N) ∧
 (6 : N) * ((2 : N) * x + y) = (125 : N) * (y + (2 : N) * z)} 245 := by
     refine' ⟨h245, _⟩
     intro x' hx'
     have h1 : 245 ≤ x' := hmin x' hx'
     exact h1

     exact hmain


D.3     Compilable Proof with an Inadmissible Answer
 Lean
 theorem P2026AIMEII_8 : ∃ (P2026AIMEII_8_answer : Nat), (IsLeast {x : N | ∃ (y : N)
 (z : N), (0 : N) < x ∧ (0 : N) < y ∧ (0 : N) < z ∧ y < (2 : N) * x ∧ z ^ (2 : N)
 * ((2 : N) * x + y) = x * y ^ (2 : N) ∧ (6 : N) * ((2 : N) * x + y) = (125 : N) *
 (y + (2 : N) * z)} (P2026AIMEII_8_answer)) := by
   let S : Set N := {x : N | ∃ (y : N) (z : N),


22
Formally Solving Answer-Construction Problems in Lean                                            J. Sun et al.


     (0 : N) < x ∧ (0 : N) < y ∧ (0 : N) < z ∧
     y < (2 : N) * x ∧
     z ^ (2 : N) * ((2 : N) * x + y) = x * y ^ (2 : N) ∧
     (6 : N) * ((2 : N) * x + y) = (125 : N) * (y + (2 : N) * z)} -- circular
 answer construction
   refine ⟨sInf S, ?_⟩
   have h : S.Nonempty := ⟨490, 20, 14, by norm_num [S]⟩
   exact ⟨Nat.sInf_mem h, fun y hy => Nat.sInf_le hy⟩

   The proof fails admissibility checking because it uses an answer containing the following constants,
some of which are not included in the admissible vocabulary [OfNat.ofNat].
 Lean
 HMul.hMul, setOf, Exists, And, HPow.hPow, HAdd.hAdd, LT.lt, OfNat.ofNat, Eq,
 InfSet.sInf


E     Additional Inadmissible Baseline Proof
The following direct GPT-5.4 baseline proof for putnam_2023_b2 is Lean-compilable but inadmissible.
The PutnamBench answer is the numeral 3; however, the proof below eliminates the existential quantifier
by returning the same minimization expression that appears in the theorem statement. Lean accepts the
proof because the goal then reduces to reflexivity, but the witness is a circular restatement of the problem
rather than a constructed answer. The proof is rejected by the admissibility checker.
 Lean
 import Mathlib
 open Nat

 theorem putnam_2023_b2 :
     ∃ (putnam_2023_b2_solution : N),
       (sInf {x : N | ∃ n > (0 : N),
         (digits (2 : N) ((2023 : N) * n)).sum = x}
         = putnam_2023_b2_solution) := by
   refine ⟨sInf {x : N | ∃ n > (0 : N),
     (digits (2 : N) ((2023 : N) * n)).sum = x}, rfl⟩

    For this problem, the admissible vocabulary is shown below.
 Admissible Vocabulary


 admissible_vocabulary :=
   [Fin.val, HAdd.hAdd, HDiv.hDiv, HMod.hMod, HMul.hMul,
    HPow.hPow, HSMul.hSMul, HSub.hSub, Int.cast, Int.ceil,
    Int.ediv, Int.emod, Int.floor, Int.sqrt, Int.toNat,
    Nat.cast, Nat.ceil, Nat.choose, Nat.digits, Nat.factorial,
    Nat.fib, Nat.floor, Nat.gcd, Nat.lcm, Nat.mod, Nat.sqrt,
    Neg.neg, OfNat.ofNat, Rat.cast, Rat.sqrt, Real.arccos,
    Real.arcsin, Real.arctan, Real.cos, Real.cosh, Real.exp,
    Real.log, Real.pi, Real.sin, Real.sinh, Real.sqrt,
    Real.tan, Real.tanh, Subtype.val, abs, multiplicity]


                                                                                                          23
Formally Solving Answer-Construction Problems in Lean                                         J. Sun et al.


    Running the admissibility checker on the witness extracted from the proof reports the following
semantic constants. The constants List.sum, setOf, Exists, GT.gt, And, Eq, and InfSet.sInf are
not in the original admissible vocabulary, so the witness is rejected.
 Checker Output

 #isCanonical
   (sInf {x : N | ∃ n > (0 : N),
     (digits (2 : N) ((2023 : N) * n)).sum = x} : N)
   with admissible_vocabulary := <putnam_2023_b2 admissible_vocabulary>
        allow_quantifier := false

 Results:
 not canonical
 used_constants :=
   [HMul.hMul, List.sum, setOf, Exists, GT.gt, And,
    Nat.digits, OfNat.ofNat, Eq, InfSet.sInf]

 missing_from_admissible_vocabulary :=
   [List.sum, setOf, Exists, GT.gt, And, Eq, InfSet.sInf]


F     Putnam 1990 A1 Example
In this section, we show an example of a problem with a complicated answer type that requires general-
ization beyond enumerated traces. The natural-language description of Putnam 1990 A1 is as follows:
Let T0 = 2, T1 = 3, and T2 = 6, and for n ≥ 3,

                                  Tn = (n + 4)Tn−1 − 4nTn−2 + (4n − 8)Tn−3 .

Find, with proof, a formula for Tn of the form Tn = An + Bn , where {An } and {Bn } are well-known
sequences.
   The problem is formalized as follows:
 Lean
 import Mathlib
 open Filter Topology Nat

 theorem putnam_1990_a1 : ∃ (putnam_1990_a1_solution : (N → Z) × (N → Z)), ∀ (T :
 N → Z), ((T (0 : N) = (2 : Z) ∧ T (1 : N) = (3 : Z) ∧ T (2 : N) = (6 : Z)) ∧ (∀
 (n : N), T (n + (3 : N)) = ((↑n : Z) + (7 : Z)) * T (n + (2 : N)) - (4 : Z) * ((↑n
 : Z) + (3 : Z)) * T (n + (1 : N)) + ((4 : Z) * (↑n : Z) + (4 : Z)) * T n)) → (T =
 putnam_1990_a1_solution.1 + putnam_1990_a1_solution.2) := by sorry

     The answer type is:
 Lean
 (N → Z) × (N → Z)

   From this answer type, the preprocessing mechanism infers that the answer is tuple-valued. Since the
source is a Putnam problem, the policy requires advanced arithmetic operators. Therefore, the admissible
vocabulary is the advanced numeric vocabulary together with tuple constructors:


24
Formally Solving Answer-Construction Problems in Lean                                         J. Sun et al.


 Admissible Vocabulary

 [And, Dvd.dvd, Eq, Even, False, Fin.val, GE.ge, GT.gt,
  HAdd.hAdd, HDiv.hDiv, HMod.hMod, HMul.hMul, HPow.hPow,
  HSMul.hSMul, HSub.hSub, Iff, Int.ModEq, Int.cast,
  Int.ceil, Int.ediv, Int.emod, Int.floor, Int.sqrt,
  Int.toNat, LE.le, LT.lt, List.cons, List.nil,
  Membership.mem, Nat.ModEq, Nat.Prime, Nat.cast,
  Nat.ceil, Nat.choose, Nat.digits, Nat.factorial,
  Nat.fib, Nat.floor, Nat.gcd, Nat.lcm, Nat.mod,
  Nat.sqrt, Ne, Neg.neg, Not, Odd, OfNat.ofNat, Or,
  Prime, Prod.fst, Prod.mk, Prod.snd, Rat.cast, Rat.sqrt,
  Real.arccos, Real.arcsin, Real.arctan, Real.cos,
  Real.cosh, Real.exp, Real.log, Real.pi, Real.sin,
  Real.sinh, Real.sqrt, Real.tan, Real.tanh, Subtype.mk,
  Subtype.val, True, abs, ite, multiplicity]

    During the Enumerate stage, ECP runs a Python program to compute the initial terms of the recur-
rence:
 Python

 def seq(N):
     T=[0]*(N+1)
     T[0]=2; T[1]=3; T[2]=6
     for n in range(N-2):
         T[n+3]=(n+7)*T[n+2]-4*(n+3)*T[n+1]+(4*n+4)*T[n]
     return T
 T=seq(15)
 print(T)

    The program returns:
 Python Output

 [2, 3, 6, 14, 40, 152, 784, 5168, 40576, 363392, 3629824, 39918848, 479005696,
 6227028992, 87178307584, 1307674400768]

    In the Conjecture stage, the model observes that the enumerated sequence matches n! + 2n . It then
verifies this candidate symbolically: the initial values agree, and both An = n! and Bn = 2n satisfy the
recurrence. The conjecture trace is shown below:
 Conjecture Trace
 Using Python, the sequence begins
 \[
 2,3,6,14,40,152,784,5168,\dots
 \]
 and matches
 \[
 n!+2^n.
 \]

 Indeed, let
 \[


                                                                                                       25
Formally Solving Answer-Construction Problems in Lean                                        J. Sun et al.


 A_n=n!, \qquad B_n=2^n.
 \]
 Then:

 - Initial values:
   \[
   A_0+B_0=1+1=2,\quad A_1+B_1=1+2=3,\quad A_2+B_2=2+4=6.
   \]

 - For \(A_n=n!\),
   \[
   (n+7)A_{n+2}-4(n+3)A_{n+1}+(4n+4)A_n
   \]
   \[
   =(n+7)(n+2)!-4(n+3)(n+1)!+(4n+4)n!
   =(n+3)! = A_{n+3}.
   \]

 - For \(B_n=2^n\),
   \[
   (n+7)B_{n+2}-4(n+3)B_{n+1}+(4n+4)B_n
   \]
   \[
   =(n+7)2^{n+2}-4(n+3)2^{n+1}+(4n+4)2^n
   =2^{n+3}=B_{n+3}.
   \]

 So \(A_n+B_n\) satisfies the recurrence and the initial conditions. Since the
 recurrence determines each next term from the previous three, the solution is
 unique. Hence every such \(T\) is exactly
 \[
 T_n=n!+2^n.
 \]

     The proposed Lean answer extracted from this trace is:
 Lean
 <<<(fun n : N => (Nat.factorial n : Z), fun n : N => (2 : Z) ^ n)>>>

     After answer substitution, the Prove stage successfully verifies the following proof:
 Lean
 import Mathlib
 open Filter Topology Nat
 theorem putnam_1990_a1 : ∃ (putnam_1990_a1_solution : (N → Z) × (N → Z)), ∀ (T :
 N → Z), ((T (0 : N) = (2 : Z) ∧ T (1 : N) = (3 : Z) ∧ T (2 : N) = (6 : Z)) ∧ (∀
 (n : N), T (n + (3 : N)) = ((↑n : Z) + (7 : Z)) * T (n + (2 : N)) - (4 : Z) * ((↑n
 : Z) + (3 : Z)) * T (n + (1 : N)) + ((4 : Z) * (↑n : Z) + (4 : Z)) * T n)) → (T =
 putnam_1990_a1_solution.1 + putnam_1990_a1_solution.2) := by
   use ((fun n : N => (Nat.factorial n : Z), fun n : N => (2 : Z) ^ n) : (N → Z) ×
  (N → Z))
   intro T h



26
Formally Solving Answer-Construction Problems in Lean                         J. Sun et al.


   have h_main : ∀ (n : N), T n = (Nat.factorial n : Z) + (2 : Z) ^ n := by
     have h1 : T 0 = 2 := h.1.1
     have h2 : T 1 = 3 := h.1.2.1
     have h3 : T 2 = 6 := h.1.2.2
     have h4 : ∀ (n : N), T (n + 3) = ((n : Z) + 7) * T (n + 2) - 4 * ((n : Z) + 3) *
  T (n + 1) + (4 * (n : Z) + 4) * T n := by
       intro n
       exact h.2 n
     have h5 : ∀ (n : N), T n = (Nat.factorial n : Z) + (2 : Z) ^ n := by
       intro n
       induction n using Nat.strong_induction_on with
       | h n ih =>
         match n with
         | 0 =>
           norm_num [Nat.factorial] at h1 ⊢
           <;> simp_all [h1 ]
           <;> norm_num
         | 1 =>
           norm_num [Nat.factorial] at h2 ⊢
           <;> simp_all [h2 ]
           <;> norm_num
         | 2 =>
           norm_num [Nat.factorial] at h3 ⊢
           <;> simp_all [h3 ]
           <;> norm_num
         | n + 3 =>
           have h6 := h4 n
           have h7 := ih n (by omega)
           have h8 := ih (n + 1) (by omega)
           have h9 := ih (n + 2) (by omega)
           simp [Nat.factorial, pow_succ, mul_add, add_mul, mul_assoc, mul_comm,
 mul_left_comm] at h6 h7 h8 h9 ⊢
           ring_nf at h6 h7 h8 h9 ⊢
           norm_cast at h6 h7 h8 h9 ⊢
           <;>
           (try omega) <;>
           (try
             {
               simp_all [Nat.factorial, pow_succ, mul_add, add_mul, mul_assoc,
 mul_comm, mul_left_comm]
               <;> ring_nf at *
               <;> norm_cast at *
               <;> nlinarith
             }) <;>
           (try
             {
               simp_all [Nat.factorial, pow_succ, mul_add, add_mul, mul_assoc,
 mul_comm, mul_left_comm]
               <;> ring_nf at *
               <;> norm_cast at *
               <;> omega
             }) <;>



                                                                                       27
Formally Solving Answer-Construction Problems in Lean                         J. Sun et al.


           (try
              {
                simp_all [Nat.factorial, pow_succ, mul_add, mul_assoc, mul_comm,
 mul_left_comm]
                <;> ring_nf at *
                <;> norm_cast at *
                <;> nlinarith
              })
           <;>
           (try
              {
                simp_all [Nat.factorial, pow_succ, mul_add, mul_assoc, mul_comm,
 mul_left_comm]
                <;> ring_nf at *
                <;> norm_cast at *
                <;> omega
              })
           <;>
           (try
              {
                simp_all [Nat.factorial, pow_succ, mul_add, mul_assoc, mul_comm,
 mul_left_comm]
                <;> ring_nf at *
                <;> norm_cast at *
                <;> nlinarith
              })
     exact h5
   have h_final : T = ((fun n : N => (Nat.factorial n : Z), fun n : N => (2 : Z) ^
 n) : (N → Z) × (N → Z)).1 + ((fun n : N => (Nat.factorial n : Z), fun n : N =>
 (2 : Z) ^ n) : (N → Z) × (N → Z)).2 := by
     funext n
     have h1 : T n = (Nat.factorial n : Z) + (2 : Z) ^ n := h_main n
     simp [Prod.fst, Prod.snd, Pi.add_apply] at h1 ⊢
     <;>
     (try simp_all) <;>
     (try ring_nf at *) <;>
     (try norm_cast at *) <;>
     (try linarith)
     <;>
     (try simp_all [Nat.factorial, pow_succ, mul_add, add_mul, mul_assoc, mul_comm,
 mul_left_comm])
     <;>
     (try ring_nf at *)
     <;>
     (try norm_cast at *)
     <;>
     (try linarith)
   exact h_final




28
Formally Solving Answer-Construction Problems in Lean                                       J. Sun et al.


G      Admissible Vocabularies
G.1     Representative Admissible Vocabularies
The preprocessing script assigns admissible vocabularies from problem-source and answer-type metadata.
The template vocabulary is shown below, with details in src/preprocess/process_datasets.py.
 Vocabulary Policy

 BASIC_ADMISSIBLE_VOCABULARY :=
   [OfNat.ofNat]

 ARITHMETIC_ADMISSIBLE_VOCABULARY :=
   [OfNat.ofNat, Nat.cast, Int.cast, Rat.cast,
    HAdd.hAdd, HSub.hSub, HMul.hMul, HDiv.hDiv,
    HPow.hPow, Neg.neg, Real.sqrt, Real.pi, Real.exp]

 ADVANCED_NUMERIC_ADMISSIBLE_VOCABULARY :=
   ARITHMETIC_ADMISSIBLE_VOCABULARY ++
   [HMod.hMod, abs, Nat.factorial, Nat.choose, Nat.digits,
    Nat.fib, Nat.gcd, Nat.lcm, Nat.mod, Nat.floor,
    Nat.ceil, Nat.sqrt, Int.floor, Int.ceil, Int.ediv,
    Int.emod, Int.toNat, Int.sqrt, Rat.sqrt, Real.log,
    Real.sin, Real.cos, Real.tan, Real.sinh, Real.cosh,
    Real.tanh, Real.arctan, Real.arccos, Real.arcsin,
    Fin.val, Subtype.val, HSMul.hSMul, multiplicity]

 PREDICATE_ADMISSIBLE_VOCABULARY :=
   [Eq, Ne, And, Or, Iff, Not, True, False, Exists,
    ite, LT.lt, LE.le, GT.gt, GE.ge, Dvd.dvd,
    Nat.ModEq, Int.ModEq, Even, Odd, Prime, Nat.Prime,
    Membership.mem]

 EXTENSIONAL_SET_ADMISSIBLE_VOCABULARY :=
   [EmptyCollection.emptyCollection, Singleton.singleton, Set.singleton,
    Insert.insert, Set.insert, Union.union, Inter.inter, Set.univ,
    Set.Ici, Set.Ioi, Set.Iic, Set.Iio, Set.Icc, Set.Ioo,
    Set.Ioc, Set.Ico, Finset.card, Finset.product, Finset.range,
    Finset.Ici, Finset.Ioi, Finset.Iic, Finset.Iio, Finset.Icc,
    Finset.Ioo, Finset.Ioc, Finset.Ico, Multiset.replicate]

 INTENSIONAL_SET_ADMISSIBLE_VOCABULARY :=
   EXTENSIONAL_SET_ADMISSIBLE_VOCABULARY ++
   [setOf, Set.Mem, Set.EqOn, Set.image, Membership.mem, Exists]

 TUPLE_ADMISSIBLE_VOCABULARY :=
   [Prod.mk, Prod.fst, Prod.snd, Subtype.mk, Subtype.val,
    Fin.val, List.cons, List.nil]

 COMPLEX_ADMISSIBLE_VOCABULARY :=
   [Complex.I, Complex.mk, Complex.ofReal]

 POLYNOMIAL_ADMISSIBLE_VOCABULARY :=


                                                                                                     29
Formally Solving Answer-Construction Problems in Lean                                            J. Sun et al.


     [Polynomial.X, Polynomial.C, Polynomial.eval, Polynomial.map,
      Polynomial.degree, Polynomial.natDegree, Polynomial.coeff,
      MvPolynomial.X, MvPolynomial.C, RatFunc.X]

 OTHERS_ADMISSIBLE_VOCABULARY :=
   [ContinuousOn, Dist.dist, Matrix.vecCons, Matrix.vecEmpty,
    MeasureTheory.Measure.restrict,
    MeasureTheory.MeasureSpace.volume, MeasureTheory.average,
    midpoint]

 SUM_PRODUCT_ADMISSIBLE_VOCABULARY :=
   [Finset.Icc, Finset.prod, Finset.range, Finset.sum,
    Finset.univ]

 PROP_ONLY_ADMISSIBLE_VOCABULARY :=
   [True, False]

   After automated admissible-vocabulary labeling, 75/75 MathArena and 301/346 PutnamBench
problems passed validation (i.e., the admissible vocabulary covers the constants used in the ground-truth
answer). There remain 45 problems that require manual inspection, which we categorize below:


 Override family          Count    Problems
 Quantifiers                25     putnam_1962_a2, putnam_1963_b3, putnam_1969_a1, putnam_1972_a3,
                                   putnam_1974_b1, putnam_1979_a3, putnam_1991_a3, putnam_1991_b1,
                                   putnam_1996_a6, putnam_2001_a3, putnam_2005_b2, putnam_2005_b3,
                                   putnam_2007_a4, putnam_2008_b5, putnam_2009_b3, putnam_2010_a2,
                                   putnam_2014_b1, putnam_2015_b3, putnam_2016_b5, putnam_2018_b1,
                                   putnam_2021_a3, putnam_2022_b6, putnam_2024_a2, putnam_2024_b1,
                                   putnam_2025_a5
 Sum/product                3      putnam_1975_a4, putnam_1986_a6, putnam_1989_b3
 notation
 Special constants          5      putnam_1962_a2, putnam_1974_b1, putnam_1996_a2, putnam_1996_a6,
                                   putnam_2018_b1
 Intensional set            20     putnam_1980_b1, putnam_1980_b3, putnam_1987_a6, putnam_1988_a3,
 vocabulary                        putnam_1994_b2, putnam_1995_a2, putnam_1996_a6, putnam_1997_b3,
                                   putnam_1998_a4, putnam_1998_b4, putnam_2011_a4, putnam_2012_a5,
                                   putnam_2014_b1, putnam_2021_a3, putnam_2021_a5, putnam_2022_a1,
                                   putnam_2022_b4, putnam_2023_a6, putnam_2023_b5, putnam_2024_b1


     These problems are mostly find-all tasks with extremely complicated answers. We found four major
overlapping issues: (i) 25 problems appear to require quantified descriptions in candidate answers, (ii) 3
require nontrivial sums or products, (iii) 5 require rare constants such as those related to matrix algebra
and measure theory, and (iv) 20 problems require intensional set vocabulary.
     They are handled as follows: For (i), we enable quantifiers in candidate answers; for (ii), we enable
∑ ∏ notation (corresponding to Finset.sum, Finset.prod, etc.); for (iii), we add constants for matrix
  ,
algebra and measure theory (e.g. MeasureTheory.average); and for (iv), we assign the intensional set
vocabulary rather than the extensional set vocabulary. After these fixes, all of these problems passed the
final validation. The detailed implementation is in src/preprocess/process_datasets.py in the
artifact.

30
Formally Solving Answer-Construction Problems in Lean                                                   J. Sun et al.


G.2     Answer Extraction for Baseline Proof Evaluation
For LLM-only baselines, we inspect the compiled proof term and check the answer used for the outermost
existential quantifier.
 Lean
 private def existsIntroWitness? (e : Expr) : Option Expr :=
   match e.getAppFn with
   | Expr.const name _ =>
       if name == Exists.intro then
         let args := e.getAppArgs
         if h : 3 < args.size then
           some args[2]
         else
           none
       else
         none
   | _ => none

 partial def firstWitnessAtProofRoot? (e : Expr) : MetaM (Option Expr) := do
   let e ← withTransparency .all <| whnf (← instantiateMVars e)
   if let some witness := existsIntroWitness? e then
     return some witness
   match e with
   | Expr.mdata _ body =>
       firstWitnessAtProofRoot? body
   | Expr.letE name type value body _ =>
       withLetDecl name type value fun x =>
         firstWitnessAtProofRoot? (body.instantiate1 x)
   | Expr.lam name type body binderInfo =>
       withLocalDecl name binderInfo type fun x =>
         firstWitnessAtProofRoot? (body.instantiate1 x)
   | _ =>
       return none


G.3     Example Admissible Vocabulary for Putnam Problem
                                                                                         (n0)+(n2)x+(n4)x2 +···
The natural-language description of Putnam 1965 B4 is as follows: Let f (x, n) =                                for
                                                                                         (n1)+(n3)x+(n5)x2 +···
all real numbers x and positive integers n. Express f (x, n + 1) as a rational function involving f (x, n) and
x, and find limn→∞ f (x, n) for all x for which this limit converges.
     The problem is formalized as follows:
 Lean
 theorem putnam_1965_b4 : ∃ (putnam_1965_b4_solution : ((((R → R) → (R → R)) ×
 ((R → R) → (R → R))) × ((Set R) × (R → R)))), ∀ (f u v : N → R → R), ∀ (n
 : N), ((∀ n > (0 : N), ∀ (x : R), u n x = Σ i ∈ Finset.Icc (0 : N) (n / (2 : N)),
 (↑(n.choose ((2 : N) * i)) : R) * x ^ i) ∧ (∀ n > (0 : N), ∀ (x : R), v n x = Σ i
 ∈ Finset.Icc (0 : N) ((n - (1 : N)) / (2 : N)), (↑(n.choose ((2 : N) * i + (1 : N
 ))) : R) * x ^ i) ∧ (∀ n > (0 : N), ∀ (x : R), f n x = u n x / v n x) ∧ ((0 : N)
 < n)) → (match putnam_1965_b4_solution with | ((p, q), s, g) => (∀ (x : R), v n x ̸=


                                                                                                                 31
Formally Solving Answer-Construction Problems in Lean                                           J. Sun et al.


  (0 : R) → v (n + (1 : N)) x ̸= (0 : R) → q (f n) x ̸= (0 : R) → f (n + (1 : N))
 x = p (f n) x / q (f n) x) ∧ s = {x : R | ∃ (l : R), Tendsto (fun (n : N) => f n
 x) atTop N ( l)} ∧ ∀ x ∈ s, Tendsto (fun (n : N) => f n x) atTop N ( (g x))) := by
 sorry

     The answer type is:
 Lean
 ((((R → R) → (R → R)) × ((R → R) → (R → R))) × ((Set R) × (R → R)))

    From this answer type, the dataset preprocessing mechanism infers a tuple answer type that contains
a set. Since the source is a Putnam problem, the policy requires advanced arithmetic operators. Therefore,
the mechanism adds the allowed constants for advanced arithmetic, set-building, and tuple-building,
resulting in the following admissible vocabulary:
 Lean
 [And, Dvd.dvd, EmptyCollection.emptyCollection, Eq, Even, Exists, False, Fin.val,
 Finset.Icc, Finset.Ici, Finset.Ico, Finset.Iic, Finset.Iio, Finset.Ioc, Finset.Ioi,
 Finset.Ioo, Finset.card, Finset.product, Finset.range, GE.ge, GT.gt, HAdd.hAdd,
 HDiv.hDiv, HMod.hMod, HMul.hMul, HPow.hPow, HSMul.hSMul, HSub.hSub, Iff,
 Insert.insert, Int.ModEq, Int.cast, Inter.inter, LE.le, LT.lt, List.cons, List.nil,
 Membership.mem, Multiset.replicate, Nat.ModEq, Nat.Prime, Nat.cast, Nat.digits,
 Nat.factorial, Ne, Neg.neg, Not, Odd, OfNat.ofNat, Or, Prime, Prod.fst, Prod.mk,
 Prod.snd, Rat.cast, Real.exp, Real.log, Real.sqrt, Set.EqOn, Set.Icc, Set.Ici,
 Set.Ico, Set.Iic, Set.Iio, Set.Ioc, Set.Ioi, Set.Ioo, Set.Mem, Set.image,
 Set.insert, Set.singleton, Set.univ, Singleton.singleton, Subtype.mk, Subtype.val,
 True, Union.union, abs, ite, setOf]

   During the validation phase, the checker confirms that the above admissible vocabulary covers the
constants used by the ground-truth answer, as shown below:
 Lean
 [GE.ge, HAdd.hAdd, OfNat.ofNat, Prod.mk, Real.sqrt, setOf]


H       Prompt
H.1     Prompt for Autoformalization
 Prompt

 You are given a math problem that requires answer-construction.
 Your task is to formalize the problem in Lean 4 (v4.24.0).
 1. Start with imports and namespaces such as `import Mathlib` and `open Real`.
 2. Define the ground-truth answer as an abbrev for parsing:
    `abbrev <problem_name>_answer : β := <expression>`
    or
    `abbrev <problem_name>_answer : α → β := fun x => <expression>`
    (Don't put `(n : N)` before `: α → β `; encode inputs inside `fun x => . . .`.)
 3. Formalize the theorem skeleton (leave proof as sorry).
    `theorem <problem_name> (x : α) (hx : P x) (y : β ) :
       Q(x, y) ↔ y = <problem_name>_answer x := by sorry`


32
Formally Solving Answer-Construction Problems in Lean                          J. Sun et al.


 Other suggestions:
 - Use `IsLeast` / `IsGreatest` for optimal answers.
 - Use `Set β ` and membership if there are multiple answers.
 Your task: {Raw Problem}


H.2     Prompt for Enumerate and Conjecture Stage
 Prompt

 I have a difficult high-school competition-level math problem in Lean, which asks
 for an answer with informal mathematical reasoning.

 Your task is to attempt the problem and state the final answer as a Lean expression,
 with the help of Python function calls.

 You are encouraged to use the tool code_exec to write code to enumerate the answer
 and obtain output, reason about the problem, and, if your reasoning and the code
 output disagree, keep doing the code/reasoning refinements until you
 are confident with your reasoning steps and come up with a proposed answer that
 agrees with the enumerations. Be sure to use a print command to obtain the answer in
 Python.

 Nevertheless, do not solely rely on the program enumeration. You should also provide
 mathematical reasoning for the answer.

 Finally, you should provide a Lean answer and enclose your answer within the
 delimiter <<< >>> so I can parse it. You should include only the proposed answer in
 the delimiter (such as <<<1>>>), and you should never include complete declarations
 in the delimiter (such as `abbrev <answer_name> : <type> := 1`). You should not put
 proofs or justifications inside <<< >>>. It should include only the final answer.
 Example: {Example}
 Your task: {Raw Problem}
 Previously failed answers: {Failed Answers}


H.3     Prompt for Proof Stage
 Prompt

 Complete the following Lean 4 code:
 {theorem statement}




                                                                                        33
