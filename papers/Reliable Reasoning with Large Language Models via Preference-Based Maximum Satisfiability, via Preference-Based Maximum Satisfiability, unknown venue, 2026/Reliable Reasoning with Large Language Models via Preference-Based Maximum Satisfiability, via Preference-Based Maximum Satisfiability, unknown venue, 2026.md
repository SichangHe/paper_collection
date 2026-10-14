                                              Reliable Reasoning with Large Language Models
                                               via Preference-Based Maximum Satisfiability


                                                                                        Pedro Orvalho∗
                                                                      Artificial Intelligence Research Institute (IIIA)
                                                                   Consejo Superior de Investigaciones Científicas (CSIC)
                                                                                 Barcelona, Catalonia, Spain
arXiv:2605.29687v1 [cs.AI] 28 May 2026




                                                                             pedro.orvalho@iiia.csic.es

                                                                                    Marta Kwiatkowska
                                                                               Department of Computer Science
                                                                                    University of Oxford
                                                                                        Oxford, UK
                                                                             marta.kwiatkowska@cs.ox.ac.uk

                                                                                       Guillem Alenyà
                                                               Institut de Robòtica i Informàtica Industrial (IRI-CSIC-UPC)
                                                                                Barcelona, Catalonia, Spain
                                                                                  galenya@iri.upc.edu

                                                                                         Felip Manyà
                                                                      Artificial Intelligence Research Institute (IIIA)
                                                                   Consejo Superior de Investigaciones Científicas (CSIC)
                                                                                 Barcelona, Catalonia, Spain
                                                                                   felip@iiia.csic.es



                                                                                              Abstract
                                                     Large Language Models (LLM S) excel at understanding natural language but
                                                     struggle with optimisation tasks involving multiple constraints and user-defined
                                                     preferences, which commonly arise in domains such as robotics. We propose a
                                                     hybrid reasoning approach in which LLM S externalise reasoning through code
                                                     generation. Given a natural language problem description, an LLM generates
                                                     Python code that encodes user-defined constraints and preferences as a preference-
                                                     based Maximum Satisfiability (MaxSAT) problem, which is then solved by an exact
                                                     MaxSAT solver. To ensure correctness, solutions returned by the model-generated
                                                     code are independently verified for feasibility and optimality against a canonical
                                                     MaxSAT encoding, allowing for different encodings and multiple optimal solutions.
                                                     We evaluate our approach using both open-source and closed-access LLM S on
                                                     three families of preference-based reasoning tasks, and compare it against direct-
                                                     answer, chain-of-thought, and program-of-thought baselines using the same models.
                                                     While these baselines rarely produce feasible solutions, the MaxSAT-based pipeline
                                                     achieves substantially higher acceptance rates, in some cases exceeding 80%. Our
                                                     results demonstrate that LLM-driven code generation combined with preference-
                                                     based MaxSAT enables solver-verifiable optimisation with respect to generated
                                                     encodings, and substantially improves correctness under independently verified
                                                     reference semantics.
                                            ∗ Work conducted while PO was a visiting researcher at the University of Oxford, under the ELSA Mobility Program.



                                         Preprint.
1   Introduction


Over the past few years, Large Language Models (LLM S) have become integral to a wide range of
everyday tasks, including writing assistance, language translation (34), and code generation (18).
Recent work has shown that these models can also translate natural language specifications into
executable code, a paradigm often referred to as vibe coding (25), which can be viewed as a
form of translation between natural and programming languages. Despite these advances, the
reasoning capabilities of LLM S remain unreliable and difficult to verify for many reasoning-intensive
tasks (27), such as planning (8; 29; 16), arithmetic (5), and logical reasoning (31; 3; 19). These
limitations are particularly evident in optimisation problems involving multiple constraints, which
frequently arise in domains such as robotics and logistics, where correctness and reliability are
critical. Several approaches, including explicit reasoning prompts and thinking models, such as
chain-of-thought (CoT) (30) and program-of-thought (PoT) (4) prompting, attempt to mitigate these
issues. While such techniques can yield modest improvements on certain simple reasoning tasks, they
provide no formal correctness guarantees. Moreover, these reasoning traces are often incorrect due to
hallucinations (20) and remain difficult to verify, limiting their applicability to optimisation tasks that
do not require rigorous constraint satisfaction and provable optimality.
To address these shortcomings, recent work has explored hybrid neuro-symbolic approaches that
combine large language models with formal reasoning tools (23; 33; 9; 10; 26). The core idea is
to leverage LLM S for natural language understanding and problem formulation, while delegating
planning or logical inference to sound and complete symbolic solvers. Empirical results show that this
division of labour can substantially improve correctness and reliability in constraint-heavy tasks. This
paradigm has been successfully applied to logical reasoning by encoding tasks directly into logical
formulae (23; 33; 26), as well as to real-world planning scenarios, using Python and Satisfiability
Modulo Theories (SMT) (9; 10). Collectively, these works suggest that formalisation and verification
are promising directions for overcoming the limitations of LLM S in optimisation and planning tasks
where correctness is paramount.
Furthermore, in several application domains, particularly robotics and decision-making systems, it is
essential to account for user-defined preferences in addition to hard constraints. Over the past decade,
prior work has addressed preference-aware reasoning by encoding both constraints and preferences
directly into Maximum Satisfiability (MaxSAT) problems (14; 15; 24). MaxSAT is the optimisation
variant of Boolean Satisfiability (SAT) (17; 1). While these approaches provide strong correctness
and optimality guarantees, they typically require users to express their preferences in specialised
languages (e.g., PDDL) or rigid formats, which require training to use. In this context, LLM S offer a
natural interface for capturing user intent, constraints, and preferences expressed in natural language,
while logical reasoners such as MaxSAT solvers provide reliable, and verifiable solutions to complex
multi-constraint optimisation problems. This complementary relationship motivates combining the
strengths of both methods.
In this paper, we study the use of LLMs as natural language interfaces to weighted partial MaxSAT
solvers for preference-aware optimisation. Our contribution is not a new generic solver-in-the-loop
architecture, but an empirical and methodological study of natural-language-to-MaxSAT encoding,
including canonical verification of feasibility and optimality under weighted soft constraints. Given
a natural language description of an optimisation problem, including constraints and user-defined
preferences, we first prompt an LLM to reason about and plan an encoding of the problem as a
MaxSAT instance. Based on this plan and the original description, the LLM then generates Python
code using the PySAT API (12), which provides access to a range of SAT and MaxSAT solvers.
The generated code is executed to obtain a candidate solution, which we subsequently verify for
feasibility and optimality against a canonical MaxSAT encoding, allowing for alternative encodings
and multiple optimal solutions. When a solution is infeasible or sub-optimal, structured feedback is
provided to the LLM, which is then prompted to revise its implementation.
Our empirical evaluation demonstrates that prompting LLM S to encode optimisation problems as
MaxSAT instances via Python code generation leads to substantial improvements in solution feasibility
and optimality across multiple problem families, compared to relying on these models’ internal
reasoning alone. The results further show that problem structure, preference variety, and intermediate
planning all influence performance, highlighting the importance of externalising optimisation and
verification to MaxSAT solvers for robust, preference-aware reasoning.


                                                    2
In summary, this paper makes the following contributions.

       • We present a neuro-symbolic approach in which LLM S translate natural-language con-
         straints and preferences into MaxSAT formulations via LLM-generated Python code, en-
         abling formal, optimisation-based reasoning.
       • Our method combines the flexibility of LLM S with MaxSAT solvers to compute optimal
         solutions for preference-based reasoning problems.
       • We evaluate LLM-generated solutions through independent feasibility and optimality verifi-
         cation against a canonical encoding, without relying on the model’s internal reasoning.
       • We analyse the impact of different user-defined preference configurations on LLM reasoning
         performance across different constraint optimisation problems.
       • Our MaxSAT-based pipeline achieves substantially higher acceptance rates than baseline
         approaches, in some cases exceeding 80%.

2   Motivation
Consider the following scheduling task. Six computational jobs must be scheduled on a single
machine over discrete time slots {0..7}. Each job must start exactly once, and at most one job may
run at any time. Furthermore, the schedule must respect a set of precedence constraints: J3 must
be executed before J1 , J5 before J0 , J5 before J4 , and J2 before J1 . Each job is associated with a
preferred deadline reflecting its relative importance. Specifically, J0 has a high-priority deadline of at
most time 4; J1 has a high-priority deadline at time 0; and J2 has a high-priority deadline at time 5.
The remaining jobs have medium-priority preferences: J3 has a deadline at time 2; J4 has a deadline
at time 3; and J5 has a deadline at time 3. The optimisation objective is to minimise the total penalty
incurred by violating user-defined deadlines, computed as the sum of their associated weights. If
multiple schedules achieve the same minimum penalty, a deterministic tie-breaking rule selects the
lexicographically earliest schedule. This problem is representative of many real-world scheduling
scenarios: users naturally express constraints and preferences in intuitive terms, for instance, “this job
should finish early”, or “that job is preferably run later”, while the underlying optimisation problem
involves multiple interacting constraints and strict optimality requirements.
When prompted with chain-of-thought (CoT) reasoning, or asked to directly produce a schedule,
modern LLM S such as G EMINI -3.1-P RO, GPT-5.5, L LAMA 3.3, and Q WEN 3-C ODER generate
plausible-looking solutions accompanied by detailed reasoning traces. However, these solutions
are often infeasible or sub-optimal. In this example, GPT-5.5 fails to identify a schedule that
simultaneously satisfies all hard constraints and minimises the total weighted penalty, even when
explicitly encouraged to reason step by step. The model returns the following infeasible solution:
                             {J0 : 4, J1 : 2, J2 : 5, J3 : 1, J4 : 6, J5 : 0},
which violates the given hard constraints, i.e., J2 before J1 . This failure does not stem from a lack
of understanding of the natural language description, but from the nature of optimisation itself, as
the reasoning capabilities of LLM S are not sufficiently robust for reasoning-intensive tasks. The
interaction between precedence constraints, task constraints, and weighted preferences induces a
combinatorial search space that requires exact reasoning. While LLM-based reasoning without
external solvers (i.e., reasoning internally or via CoT chains) can produce explanations that appear
convincing, such models provide no formal guarantees of feasibility or optimality, and optimisation
errors are difficult to detect from the reasoning trace alone.
In contrast, when the same task is encoded as a Maximum Satisfiability (MaxSAT) problem by
GPT-5.5 and solved using a symbolic solver, an optimal solution can be found reliably, and both
feasibility and optimality can be easily verified. By prompting LLM S to generate Python code that
encodes the problem using a MaxSAT solver, the model produces the following optimal schedule:
                             {J0 : 4, J1 : 6, J2 : 5, J3 : 1, J4 : 3, J5 : 2},
which satisfies all hard constraints and minimises the total penalty induced by violated preferences.
This simple optimisation example illustrates a key insight motivating our work: LLM S should not be
trusted to perform optimisation reasoning, but they are highly effective at translating user intent into


                                                    3
Python code. When reasoning is externalised from the LLM and delegated to a sound and complete
MaxSAT solver, the resulting system combines the strengths of both paradigms. The LLM captures
user constraints and preferences from natural language and generates an executable encoding, while
the MaxSAT solver guarantees feasibility, optimality, and verifiability of the solution. Rather than
attempting to improve LLM S ’ internal reasoning capabilities for optimisation tasks, we treat them
as interfaces between users and MaxSAT solvers, enabling reliable, verifiable, and preference-aware
decision-making grounded in formal guarantees.

3     Preliminaries
The Boolean Satisfiability (SAT) problem is the canonical decision problem in propositional logic (2).
A literal is defined as either a propositional variable xi or its negation ¬xi . A formula is in Conjunctive
Normal Form (CNF) if it is expressed as a conjunction of clauses, where each clause is a disjunction
of literals. Given a CNF formula ϕ, the SAT problem consists of determining whether there exists a
truth assignment to the variables that satisfies ϕ, or whether no such assignment exists. The Maximum
Satisfiability (MaxSAT) problem extends SAT by introducing an optimisation objective (17; 1). Given
a CNF formula ϕ, the goal is to find an assignment that maximises the number of satisfied clauses. In
the partial MaxSAT setting, the formula ϕ is partitioned into a set of hard clauses ϕh and a set of soft
clauses ϕs . The objective is to find an assignment that satisfies all hard clauses while minimising
the number of unsatisfied soft clauses. In the weighted partial MaxSAT variant, each soft clause is
associated with a weight, and the objective becomes minimising the total weight of the unsatisfied
soft clauses. In preference-based MaxSAT (14; 15; 24), user-defined preferences are modelled as soft
constraints in a weighted partial MaxSAT formulation, where weights reflect the relative importance
or ordering of user preferences.
Example 1 (Weighted Partial MaxSAT) Consider the partial MaxSAT formula ϕ = (ϕh , ϕs ),
where ϕh = {(x1 ∨ x2 ), (¬x2 ∨ x3 )} and ϕs = {(¬x1 ), (¬x3 )}, with weights w = {w¬x1 =
1, w¬x3 = 3}. The assignment {(x1 , 1), (x2 , 0), (x3 , 0)} is an optimal solution for ϕ, as it satisfies
all hard clauses in ϕh and violates only one soft clause in ϕs , namely (¬x1 ), incurring a total weight
of 1. In contrast, the assignment {(x1 , 0), (x2 , 1), (x3 , 1)}, while satisfying all hard clauses, violates
the soft clause (¬x3 ) and incurs a total weight of 3. Since this weight is higher than the optimal
value of 1, the assignment is not optimal.
Moreover, given an assignment (possible solution) to the variables of a MaxSAT formula, its satisfia-
bility and optimality can be verified by adding the assignment as hard constraints to the solver and
checking both the satisfiability of the resulting instance and the associated optimisation cost.

4     MaxSAT-Based Reasoning for LLM S
We propose a hybrid neuro-symbolic reasoning approach that combines the natural language under-
standing and code generation capabilities of Large Language Models (LLM S) with the formal and
reliable optimisation guarantees of preference-based Maximum Satisfiability (MaxSAT). The key
idea is to externalise reasoning from LLM S into Python code and delegate automated reasoning to a
MaxSAT solver, while independently verifying the correctness of the resulting solutions. All prompts
used to interact with the models are provided in Appendix A.

4.1   Problem Setting

We consider preference-based reasoning problems defined by: (i) a set of hard constraints that must
be satisfied, and (ii) a set of soft constraints and/or preferences that should be optimised. Such
problems arise naturally in domains such as scheduling and robotics, where solutions must be feasible
while optimising user-defined objectives. Each problem instance is provided to the model as a natural
language description specifying constraints and preferences. The goal is to compute a solution that
satisfies all hard constraints and is optimal with respect to the stated preferences.

4.2   LLM-to-MaxSAT Pipeline

Figure 1 illustrates our reasoning pipeline. Given a natural language problem description, we apply
the following steps.


                                                     4
                                                             Intermediate
               User                                            Planning
                Input
                                           Prompt
               (in Natural                                 Encoding Plan into MaxSAT
               Language)
              Optimisation            Neuro-Symbolic           Prompt
                Problem                                                     Code Generation
                                        Controller
                   +
               Constrains
                   +
              Preferences           Feedback                   Syntactic Feedback      Encoding into MaxSAT

               Output
                                       Reasoning       Candidate Solution        Python
             Reliable and              Verification                            Interpreter
            Optimal Solution


Figure 1: Our pipeline for enabling LLM S to externalise reasoning through vibe coding, delegating
formal reasoning and optimisation to a MaxSAT solver via its Python API. LLM S’ solutions are
verified against a canonical MaxSAT encoding.


Intermediate Planning. We introduce an explicit intermediate planning step. Before generating
code, the LLM is asked to produce a structured, symbolic description of the variables, constraints,
and preferences. This step is inspired by prior work (9), which shows that asking the model to first
outline how to encode the problem can lead to improved results. The resulting plan is then provided
back to the model as guidance for code generation. While not required for correctness, this step can
improve modelling accuracy by encouraging more systematic encodings.

Code Generation. Rather than asking the LLM to directly produce a solution, we prompt it to
generate executable Python code that encodes the problem as a MaxSAT instance. If the intermediate
planning step is not performed, the LLM begins by interpreting the user-provided natural language
description, identifying the decision variables, hard constraints, and preferences. We explicitly
instruct the model to use PySAT (12), a Python API for interacting with SAT and MaxSAT solvers.
The generated Python code constructs a weighted CNF formula in which: (i) hard constraints are
encoded as hard clauses, and (ii) preferences are encoded as weighted soft clauses. Moreover, at this
stage we provide a brief explanation and an example illustrating how to use the PySAT API, in order
to familiarise the model with the interface and reduce the likelihood of errors in the generated code.

MaxSAT Solving. The generated code, which encodes the problem as a MaxSAT instance, invokes
a MaxSAT solver. This guarantees that, whenever a solution exists, the returned assignment is feasible
and optimal with respect to the encoded preferences, or at least with respect to the way the model has
encoded the given problem. At this stage, the correctness and optimality of the solution no longer
depend on the LLM, but on the MaxSAT solver.

Verification Against Canonical Encodings. A central challenge in evaluating LLM-generated
encodings is that different encodings may yield different models or objective values, even when
they represent the same underlying problem. To address this, we decouple solution validity from
encoding correctness during evaluation. For each problem instance, we construct a canonical
MaxSAT encoding that serves as a reference specification only for evaluation purposes. This canonical
encoding is not required by the proposed reasoning pipeline and is not assumed to be available
in real-world deployments. Its sole purpose is to provide a model-independent ground truth that
enables fair comparison across different LLM S, prompting strategies, and encodings. During the
code generation step, we explain to the LLM the exact format expected for the solution. After
executing the LLM-generated Python code, we parse the solution returned by the solver and verify
it against the canonical encoding by checking: (i) feasibility, i.e., whether the solution satisfies all
hard constraints; and (ii) optimality, i.e., whether the solution achieves the same objective value as
the canonical optimal solution. This verification procedure allows multiple optimal solutions
and alternative encodings to be accepted, while ensuring that all accepted solutions are correct
with respect to the reference semantics. Importantly, this evaluation protocol does not rely on
trusting the LLM ’s internal reasoning or reported objective values. In practical settings, correctness
and optimality are instead guaranteed by the MaxSAT solver with respect to the constraints and


                                                       5
preferences encoded by the LLM, potentially complemented by interactive user refinement rather
than by a hidden canonical specification.

Feedback. If the generated code fails to execute, violates the required output format, or triggers
a runtime/API error, we return the corresponding error message to the model and request a refined
implementation. In our experiments, canonical feasibility and optimality checks are used only for
final evaluation and are not returned to the model as feedback. Thus, refinement feedback does not
expose the reference encoding or canonical objective value. This feedback loop continues until the
model produces a feasible and optimal solution, a predefined time limit is reached, or the number of
iterations exceeds five, which typically indicates that the model is stuck and repeatedly generating the
same incorrect solution.
Thus, by combining LLM-driven semantic interpretation of user constraints and preferences with
LLM-generated code, exact MaxSAT solving, and independent verification, we transform unreliable
natural language reasoning into a robust and verifiable optimisation process. This separation of
concerns allows LLM S to focus on understanding user intent, while formal reasoning and correctness
are ensured by the MaxSAT solver.

5     Experiments
The goal of our experiments was to evaluate Large Language Models (LLM S) on a range of reasoning
tasks that require optimising an objective, by asking the models to encode these optimisation problems
as MaxSAT instances via the generation of Python code. Accordingly, our experiments were designed
to address the following research questions (RQs):
RQ1. Are LLM S effective at encoding optimisation problems into MaxSAT formulations through
vibe coding?
RQ2. Do LLM S exhibit different performance across different families of optimisation problems?
RQ3. To what extent does an intermediate planning step affect the quality of LLM-generated Python
code for MaxSAT-based optimisation?
RQ4. How do different user preferences influence LLM S ’ reasoning behaviour and solution quality?
RQ5. Do LLM S perform better when leveraging plans generated by other models?

5.1   Experimental Setup

All experiments were run using NVIDIA A100-SXM4 graphics card with 80GB of memory and
256GB of RAM, using a time limit of 5 minutes. For the MaxSAT oracle, RC2 (13) from the PySAT
toolkit (12) was used, since PySAT is a Python API for several SAT/MaxSAT algorithms.

5.2   Evaluation Dataset

To evaluate the proposed approach, we constructed a dataset of preference-based reasoning problems
with natural language descriptions and reference encodings. The dataset is designed to assess a
model’s ability to interpret user constraints and preferences, externalise reasoning through code
generation, and produce solutions that are feasible and optimal with respect to a canonical specifica-
tion. Problem Families: The dataset comprises three families of constraint optimisation problems
typically used in MaxSAT competitions: (1) Maximum Independent Set (MIS), where the objective is
to select the largest subset of mutually non-adjacent vertices; (2) Scheduling, where tasks must be
assigned start times subject to precedence and resource constraints while optimising preference-based
objectives; and (3) Set Cover, where a collection of sets must be selected to cover all required
elements while minimising preference-based costs. These problem families were chosen because
they naturally involve a combination of hard constraints and soft preferences, and thus serve as
a suitable proof of concept for this study. The dataset contains 25 instances of varying size and
difficulty for each problem family, enabling evaluation across different reasoning and modelling
challenges. In total, the dataset includes four preference variants for each problem instance (namely,
none, p1, p2, and p3), each accompanied by a natural language description, a canonical MaxSAT
encoding, and a verified optimal solution. As a result, the dataset comprises 300 reasoning instances
in total. Natural Language Descriptions: Each instance is associated with a natural language
description specifying: (i) the decision variables, (ii) the hard constraints that must be satisfied, and
(iii) the preferences defining the optimisation objective. The descriptions are written to resemble


                                                   6
Table 1: Portion of feasible and optimal solution achieved by each LLM, across all preferences
(acceptance rate %).
            Family          Model                        direct-answer      cot-answer       pot-answer        maxsat-no-plan       maxsat-with-plan
                            G EMINI -3.1-P RO                 0.0                4.0             11.0               36.0                   56.0
            mis             GPT-5.5                           0.0                2.0             13.0               32.0                   51.0
                            L LAMA 3.3                        0.0                1.0              5.0               18.0                   24.0
                            Q WEN 3-C ODER                    0.0                0.0              6.0               15.0                   20.0
                            G EMINI -3.1-P RO                 0.0                1.0             14.0               44.0                   59.0
            scheduling      GPT-5.5                           0.0                0.0             9.0                41.0                   56.0
                            L LAMA 3.3                        0.0                0.0             3.0                 9.0                    8.0
                            Q WEN 3-C ODER                    0.0                0.0             0.0                22.0                    4.0
                            G EMINI -3.1-P RO                34.0                36.0            46.0               79.0                   87.0
            setcover        GPT-5.5                          29.0                33.0            45.0               76.0                   82.0
                            L LAMA 3.3                       14.0                37.0            41.0               62.0                   45.0
                            Q WEN 3-C ODER                   17.0                27.0            25.0               49.0                   29.0



                          Table 2: Acceptance rate (%) by preference (none / p1 / p2 / p3).
Family     Model                    direct-answer                   cot-answer                pot-answer               maxsat-no-plan           maxsat-with-plan
           G EMINI -3.1-P RO     0.0 / 0.0 / 0.0 / 0.0       16.0 / 0.0 / 0.0 / 0.0       40.0 / 4.0 / 0.0 / 0.0   100.0 / 4.0 / 20.0 / 20.0 100.0 / 44.0 / 40.0 / 40.0
mis        GPT-5.5               0.0 / 0.0 / 0.0 / 0.0        8.0 / 0.0 / 0.0 / 0.0       52.0 / 0.0 / 0.0 / 0.0   100.0 / 4.0 / 12.0 / 12.0 96.0 / 72.0 / 28.0 / 8.0
           L LAMA 3.3            0.0 / 0.0 / 0.0 / 0.0       4.0 / 0.0 / 0.0 / 0.0        20.0 / 0.0 / 0.0 / 0.0    64.0 / 8.0 / 8.0 / 0.0   60.0 / 12.0 / 12.0 / 12.0
           Q WEN 3-C ODER        0.0 / 0.0 / 0.0 / 0.0       0.0 / 0.0 / 0.0 / 0.0        12.0 / 4.0 / 4.0 / 4.0   20.0 / 16.0 / 12.0 / 12.0 12.0 / 68.0 / 0.0 / 0.0
           G EMINI -3.1-P RO     0.0 / 0.0 / 0.0 / 0.0        4.0 / 0.0 / 0.0 / 0.0       56.0 / 0.0 / 0.0 / 0.0   60.0 / 40.0 / 40.0 / 36.0 96.0 / 56.0 / 48.0 / 36.0
scheduling GPT-5.5               0.0 / 0.0 / 0.0 / 0.0        0.0 / 0.0 / 0.0 / 0.0       36.0 / 0.0 / 0.0 / 0.0   56.0 / 80.0 / 16.0 / 12.0 92.0 / 92.0 / 20.0 / 20.0
           L LAMA 3.3            0.0 / 0.0 / 0.0 / 0.0        0.0 / 0.0 / 0.0 / 0.0       12.0 / 0.0 / 0.0 / 0.0   12.0 / 12.0 / 12.0 / 0.0   12.0 / 12.0 / 8.0 / 0.0
           Q WEN 3-C ODER        0.0 / 0.0 / 0.0 / 0.0        0.0 / 0.0 / 0.0 / 0.0        0.0 / 0.0 / 0.0 / 0.0    76.0 / 8.0 / 4.0 / 0.0     16.0 / 0.0 / 0.0 / 0.0
           G EMINI -3.1-P RO 88.0 / 12.0 / 16.0 / 20.0 92.0 / 16.0 / 16.0 / 20.0 100.0 / 28.0 / 28.0 / 28.0 100.0 / 84.0 / 60.0 / 72.0 100.0 / 88.0 / 80.0 / 80.0
setcover   GPT-5.5            92.0 / 12.0 / 12.0 / 0.0 96.0 / 12.0 / 12.0 / 12.0 100.0 / 20.0 / 32.0 / 28.0 96.0 / 84.0 / 60.0 / 64.0 100.0 / 88.0 / 72.0 / 68.0
           L LAMA 3.3          44.0 / 4.0 / 4.0 / 4.0 100.0 / 16.0 / 16.0 / 16.0 100.0 / 16.0 / 24.0 / 24.0 92.0 / 72.0 / 44.0 / 40.0 68.0 / 60.0 / 32.0 / 20.0
           Q WEN 3-C ODER      68.0 / 0.0 / 0.0 / 0.0   96.0 / 4.0 / 4.0 / 4.0     96.0 / 4.0 / 0.0 / 0.0   80.0 / 56.0 / 40.0 / 20.0 64.0 / 24.0 / 20.0 / 8.0




user-provided specifications rather than formal problem definitions, requiring models to infer intent
from natural language. Canonical MaxSAT Encodings: For each instance, we provide a canonical
preference-based MaxSAT formula that serves as the reference specification for our evaluation. This
encoding captures the intended semantics of the problem, with hard clauses representing mandatory
constraints and weighted soft clauses representing preferences. The canonical encoding is solved
using an exact MaxSAT solver to compute an optimal objective value. Importantly, the canonical
encoding is used only for verification and evaluation; models are not given access to this encoding or
its solution during inference. During evaluation, canonical verification is used only to score the final
output and is not used to provide feedback to the model. Note that this evaluation protocol allows
different encodings and multiple optimal solutions to be accepted, while ensuring that all reported
successes correspond to correct solutions under the reference semantics.

5.3      Large Language Models (LLM S)

In our evaluation, we consider four LLM S: two open-source models and two closed-access models.
For the open-source models, we select LLM S available on Hugging Face (11): Alibaba’s Q WEN -
3-C ODER (32) (30B) and Meta’s L LAMA 3.3 (21) (70B). These specific model sizes were chosen
as they correspond to the most recent and largest available versions of each model that can be run
on the GPU infrastructure used in our experiments. For the closed-access models, we evaluate
OpenAI’s GPT-5.5 (22) and Google’s G EMINI -3.1-P RO (7), as these are among the most widely
adopted state-of-the-art proprietary models. Moreover, to ensure consistency across experiments, the
temperature of all models was set to zero.

5.4      Evaluation

Baselines. We compare our approach against three commonly used prompting strategies: (1) Direct
Answer, where the LLM S generate a solution directly from a natural language description; (2) Chain-
of-Thought (CoT), where the model is prompted to reason step by step in natural language before
producing a solution; and (3) Program-of-Thought (PoT), where the model generates Python code
to derive a solution. Across these baselines, the model is responsible either for performing reasoning
and optimization internally (Direct Answer and CoT) or for delegating them to generated Python


                                                                                      7
code (PoT), without access to formal solvers or external verification. Appendix A provides the prompt
templates used for all baselines.
Configurations. We consider two configurations of our neuro-symbolic approach: (1) MaxSAT (no
plan), in which the LLM directly generates Python code encoding the optimisation problem as a
MaxSAT problem; and (2) MaxSAT (with plan), in which the LLM first produces an intermediate
plan of variables, constraints, and preferences before generating the corresponding MaxSAT encoding.
Evaluation Metric. All LLM-generated solutions are evaluated using feasibility and optimality
verification against a canonical MaxSAT encoding, independent of the model’s internal reasoning or
reported objective values. A solution is counted as accepted if and only if it satisfies all hard con-
straints and achieves an optimal objective value under the canonical encoding. We report acceptance
rate (%) as the proportion of instances for which a feasible and optimal solution is achieved.
RQ1. Table 1 reports global acceptance rates across all preference variants. Direct-answer and
CoT baselines perform poorly, especially on MIS and scheduling: direct-answer achieves 0% for all
models, while CoT reaches at most 4% on MIS and 1% on scheduling. PoT improves slightly but
remains far below MaxSAT-based methods. In contrast, MaxSAT with planning achieves 56% and
51% on MIS for G EMINI -3.1-P RO and GPT-5.5, and 59% and 56% on scheduling, respectively. On
set cover, MaxSAT-based methods also obtain the best results, reaching 87% for G EMINI -3.1-P RO
and 82% for GPT-5.5. These results show that LLM S can effectively encode optimisation problems
into MaxSAT through vibe coding, provided that optimisation is externalised to a symbolic solver.
RQ2. Performance differs substantially across problem families. Set cover is consistently the easiest:
even prompting baselines obtain non-zero acceptance rates, and MaxSAT-based approaches achieve
the highest overall results. By contrast, MIS and scheduling are more challenging, with prompting-
only methods almost entirely failing and MaxSAT performance becoming more model-dependent.
This suggests that LLM-generated MaxSAT encodings are sensitive to problem structure: coverage-
style constraints are easier to encode than problems requiring precise modelling of exclusivity,
precedence, feasibility, and combinatorial interactions.
RQ3. Table 1 also compares MaxSAT encodings with and without intermediate planning. Planning
consistently improves performance for the stronger models. For G EMINI -3.1-P RO, acceptance
increases from 36% to 56% on MIS, 44% to 59% on scheduling, and 79% to 87% on set cover;
GPT-5.5 shows a similar trend, improving from 32% to 51%, 41% to 56%, and 76% to 82%,
respectively. However, planning is not uniformly beneficial: for L LAMA 3.3 and Q WEN 3-C ODER, it
sometimes degrades performance, particularly on scheduling and set cover. Thus, planning helps
when the model can translate the plan into correct executable MaxSAT code, but may otherwise
introduce error propagation.
RQ4. Table 2 shows that preferences substantially affect solution quality. The none setting is
generally easiest, while preference variants often reduce acceptance rates. However, the degradation
is not strictly monotonic: some preferences appear qualitatively harder than others. For example,
Q WEN 3-C ODER with MaxSAT and planning reaches 68% on MIS under p1, but 0% under both p2
and p3. Despite these drops, MaxSAT-based methods remain more robust than direct-answer, CoT,
and PoT baselines, especially for set cover, where G EMINI -3.1-P RO and GPT-5.5 maintain strong
performance even under p2 and p3. Overall, user preferences significantly influence LLM reasoning
and encoding quality, but MaxSAT mitigates much of this difficulty.
RQ5. Table 3 evaluates whether models benefit from plans generated by other models, focusing on
MIS; extended results for all families are reported in Table 4 in Appendix C. Cross-model plans can
improve individual cases: for example, G EMINI -3.1-P RO improves on p1 and p2 using L LAMA 3.3-
and GPT-5.5-generated plans, while GPT-5.5 achieves its best p1 and p2 results with L LAMA 3.3-
and G EMINI -3.1-P RO-generated plans. However, these gains are inconsistent, especially for weaker
models, where transferred plans often lead to unstable or near-zero performance. The appendix
results show the same pattern across scheduling and set cover: transfer is most useful for simpler,
more modular encodings such as set cover, but remains brittle for more constrained families. Overall,
cross-model CoTs or plans are useful only when the transferred plan is clear and the target model can
faithfully implement it as executable MaxSAT code.


Discussion. Our evaluation yields four main findings. First, consistent with prior work (23; 33; 10),
LLM S are largely ineffective at solving constrained optimisation problems through internal reasoning


                                                  8
Table 3: Acceptance rates when LLM S generate MaxSAT encodings using an intermediate planning
step produced either by the same model or by a different model.
                  Family Model                Plan-from           none   p1     p2    p3
                                              G EMINI -3.1-P RO 100.0 44.0 40.0 40.0
                          G EMINI -3.1-P RO   GPT-5.5           100.0 72.0 48.0 0.0
                                              L LAMA 3.3        88.0 84.0 8.0 4.0
                                              Q WEN 3-C ODER    96.0 72.0 0.0 8.0
                  mis
                                              G EMINI -3.1-P RO 96.0     72.0 32.0    8.0
                          GPT-5.5             GPT-5.5           96.0     72.0 28.0    8.0
                                              L LAMA 3.3        88.0     84.0 8.0     4.0
                                              Q WEN 3-C ODER 100.0       72.0 4.0     0.0
                                              G EMINI -3.1-P RO   68.0   12.0 12.0 12.0
                          L LAMA 3.3          GPT-5.5              0.0   24.0 4.0 0.0
                                              L LAMA 3.3          60.0   12.0 12.0 12.0
                                              Q WEN 3-C ODER       0.0   68.0 0.0 0.0
                                              G EMINI -3.1-P RO   12.0   68.0   0.0   8.0
                          Q WEN 3-C ODER      GPT-5.5              0.0   16.0   0.0   0.0
                                              L LAMA 3.3          4.0    52.0   0.0   0.0
                                              Q WEN 3-C ODER      12.0   68.0   0.0   0.0



alone: direct-answer and CoT prompting almost entirely fail on MIS and scheduling, while PoT
provides only limited gains. Second, encoding optimisation problems into MaxSAT via Python code
generation substantially improves acceptance rates, especially for stronger models such as G EMINI -
3.1-P RO and GPT-5.5. This supports our central claim that externalising optimisation reasoning to a
symbolic MaxSAT solver enables more reliable and verifiable preference-aware reasoning than relying
on the LLM alone. Third, intermediate planning helps only when the model can translate the plan into
correct executable code. While planning consistently improves MaxSAT performance for G EMINI -
3.1-P RO and GPT-5.5, it can degrade results for L LAMA 3.3 and Q WEN 3-C ODER, indicating that
the planning step may also introduce error propagation. Finally, cross-model plans show limited and
task-dependent transferability. They can improve selected cases, particularly for simpler problems
such as set cover, but may hurt performance when the transferred plan is misaligned with the target
model’s encoding strategy. Overall, the most reliable configuration is not the one that produces more
reasoning text, but the one that produces executable, solver-verifiable MaxSAT encodings.

6   Related Work
Neuro-symbolic reasoning methods. Recent work has explored neuro-symbolic approaches for
improving LLM reasoning across planning (8; 29; 16; 9; 10), arithmetic (5), and logical reasoning (31;
3; 19; 33; 23; 26; 28). Representative systems such as SATLM (33) and LOGIC-LM (23) combine LLM S
with symbolic solvers by translating natural language problems into formal logical specifications,
which are then solved by SMT solvers or other deterministic inference engines. By separating
parsing from reasoning and execution, these methods reduce errors commonly observed in chain-of-
thought (CoT) prompting; however, directly generating logical formulae can still produce syntactically
invalid or ill-formed encodings. More recently, ConstraintLLM (26) introduced a neuro-symbolic
framework for constraint programming that combines a fine-tuned LLM with retrieval, tree-of-
thought exploration, and solver-guided self-correction to generate and validate constraint models at
industrial scale. Similarly, work on realistic travel-planning benchmarks shows that LLM S struggle to
generate valid plans directly for complex multi-constraint problems, but become more reliable when
guided to formalise queries and invoke SMT-based verification tools (9). LLMFP (10) generalises this
paradigm to diverse planning domains by framing problems as constrained optimisation tasks solved
with SMT solvers. Like these approaches, our work externalises reasoning by using LLM S to vibe
code constraints into executable Python. However, prior work primarily focuses on feasibility or
planning with SMT-based APIs, whereas we target preference-aware optimisation using PySAT (12)
and SAT/MaxSAT solvers.
Preference-based MaxSAT. In preference-based MaxSAT (14; 15; 24), user preferences are repre-
sented as soft constraints in a weighted partial MaxSAT formulation, where weights encode their
relative importance or priority. Existing approaches typically require users to specify constraints
and preferences in the Planning Domain Definition Language (PDDL) (6). While this provides


                                                    9
an explicit and rigorous representation of user intent, it also requires familiarity with a specialised
domain-specific language.
Our work differs from prior hybrid LLM–solver approaches in three main ways. First, we address
preference-based optimisation rather than only feasibility checking or single-objective planning.
Second, we use weighted soft constraints and independently verify optimality, rather than relying
on the LLM’s internal reasoning or encoding. Third, the optimisation problems considered here are
predominantly Boolean, making SAT/MaxSAT a natural formalism; SMT-based methods typically
reduce such Boolean structure to SAT internally. To the best of our knowledge, this is the first work
to combine LLM S for extracting user intent from natural language with MaxSAT solvers for rigorous
preference-aware optimisation under user-defined constraints.

7   Conclusion
We studied the use of Large Language Models (LLM S) for preference-aware optimisation by ex-
ternalising reasoning to Maximum Satisfiability (MaxSAT) solvers. Our results show that, while
LLM S are unreliable at solving optimisation problems through internal reasoning alone, they can
effectively translate natural language constraints and preferences into executable MaxSAT encod-
ings via Python code generation. By delegating optimisation and verification to symbolic solvers,
our approach enables more reliable and verifiable preference-aware reasoning. Across multiple
optimisation families, our evaluation shows that solution quality depends on problem structure,
preference complexity, and intermediate planning. Overall, these findings highlight the value of
separating semantic interpretation from formal optimisation, and suggest that combining LLM S with
MaxSAT solvers is a promising direction for robust user-facing decision-making systems. Future
work will explore interactive optimisation settings in which LLM S and logical reasoners support
user-in-the-loop decision making, enabling users to iteratively refine preferences and request revised
solutions as requirements evolve.

Acknowledgements
This work was supported by grant PID2022-139835NB-C21 funded by MCIN/AEI/10.13039/-
501100011033. This project has received funding from the European Union’s HORIZON-
MSCA-2025-PF research and innovation programme under the Marie Skłodowska-Curie (Sher-
lock4Py, GA No 101269051). This project was additionally supported by the ALLIES Co-
fund, and has received funding from the European Union’s Horizon-MSCA-2022-COFUND-01
research and innovation programme under the Marie Skłodowska-Curie (GA No 101126626).
This project also received funding from ELSA: European Lighthouse on Secure and Safe AI
project (GA No. 101070617 under UK guarantee). PO acknowledges travel support from ELSA
Mobility Program (GA No 101070617).

References
 [1] Fahiem Bacchus, Matti Järvisalo, and Ruben Martins. Maximum satisfiability. In Armin Biere,
     Marijn Heule, Hans van Maaren, and Toby Walsh, editors, Handbook of Satisfiability - Second
     Edition, volume 336 of Frontiers in Artificial Intelligence and Applications, pages 929–991.
     IOS Press, 2021. doi: 10.3233/FAIA201008.

 [2] Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh, editors. Handbook of Sat-
     isfiability, volume 185 of Frontiers in Artificial Intelligence and Applications. IOS Press,
     2009.

 [3] Diego Calanzone, Stefano Teso, and Antonio Vergari. Logically consistent language models
     via neuro-symbolic integration. In The Thirteenth International Conference on Learning
     Representations (ICLR), 2025.

 [4] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. Program of thoughts
     prompting: Disentangling computation from reasoning for numerical reasoning tasks. Trans.
     Mach. Learn. Res., 2023, 2023.


                                                  10
 [5] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan,
     and Graham Neubig. Pal: Program-aided language models. In International Conference on
     Machine Learning, pages 10764–10799. PMLR, 2023.
 [6] Malik Ghallab, Adele Howe, Craig Knoblock, ISI Drew McDermott, Ashwin Ram, Manuela
     Veloso, Daniel Weld, David Wilkins Sri, Anthony Barrett, Dave Christianson, et al. Pddl—the
     planning domain definition language. Technical Report, Tech. Rep., 1998.
 [7] Google.          Gemini-3.1-Pro  https://blog.google/innovation-and-ai/
     models-and-research/gemini-models/gemini-3-1-pro/, 2026. Released: 2026-02-
     19.
 [8] Lin Guan, Karthik Valmeekam, Sarath Sreedharan, and Subbarao Kambhampati. Leveraging
     pre-trained large language models to construct and utilize world models for model-based task
     planning. Advances in Neural Information Processing Systems, 36:79081–79094, 2023.
 [9] Yilun Hao, Yongchao Chen, Yang Zhang, and Chuchu Fan. Large language models can solve
     real-world planning rigorously with formal verification tools. In Proceedings of the 2025 Con-
     ference of the Nations of the Americas Chapter of the Association for Computational Linguistics:
     Human Language Technologies, NAACL, pages 3434–3483. Association for Computational
     Linguistics, 2025.
[10] Yilun Hao, Yang Zhang, and Chuchu Fan. Planning anything with rigor: General-purpose
     zero-shot planning with llm-based formalized programming. In The Thirteenth International
     Conference on Learning Representations (ICLR), 2025.
[11] HuggingFace. . https://huggingface.co, 2026. [Online; accessed 21-January-2026].
[12] Alexey Ignatiev, António Morgado, and João Marques-Silva. PySAT: A python toolkit for
     prototyping with SAT oracles. In Olaf Beyersdorff and Christoph M. Wintersteiger, editors,
     Theory and Applications of Satisfiability Testing - SAT 2018, volume 10929 of Lecture Notes in
     Computer Science, pages 428–437. Springer, 2018. doi: 10.1007/978-3-319-94144-8_26.
[13] Alexey Ignatiev, António Morgado, and João Marques-Silva. RC2: an efficient MaxSAT solver.
     J. Satisf. Boolean Model. Comput., 11(1):53–64, 2019.
[14] Farah Juma, Eric I Hsu, and Sheila A McIlraith. Exploiting maxsat for preference-based
     planning. In Proceedings of the ICAPS-11 Workshop on Constraint Satisfaction Techniques for
     Planning and Scheduling Problems (COPLAS), 2011.
[15] Farah Juma, Eric I. Hsu, and Sheila A. McIlraith. Preference-based planning via maxsat.
     In Advances in Artificial Intelligence - 25th Canadian Conference on Artificial Intelligence,
     Canadian AI 2012, Toronto, ON, Canada, May 28-30, 2012. Proceedings, volume 7310 of
     Lecture Notes in Computer Science, pages 109–120. Springer, 2012.
[16] Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant
     Bhambri, Lucas Paul Saldyt, and Anil B Murthy. Position: Llms can’t plan, but can help
     planning in llm-modulo frameworks. In Forty-first International Conference on Machine
     Learning, 2024.
[17] Chu Min Li and Felip Manya. Maxsat, hard and soft constraints. In Handbook of satisfiability,
     pages 613–631. IOS Press, 2009.
[18] Jenny T. Liang, Chenyang Yang, and Brad A. Myers. A large-scale survey on the usability of
     AI programming assistants: Successes and challenges. In ICSE 2024, pages 52:1–52:13. ACM,
     2024. doi: 10.1145/3597503.3608128.
[19] Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter
     Clark, and Yejin Choi. Zebralogic: On the scaling limits of llms for logical reasoning. In
     Forty-second International Conference on Machine Learning, 2025.
[20] Stephanie Lin, Jacob Hilton, and Owain Evans. Truthfulqa: Measuring how models mimic hu-
     man falsehoods. In Proceedings of the 60th annual meeting of the association for computational
     linguistics (volume 1: long papers), pages 3214–3252, 2022.


                                                11
[21] Meta. Llama-3.3 https://www.llama.com/docs/model-cards-and-prompt-formats/
     llama3_3/, 2024. Released: 2024-12.
[22] OpenAI. GPT5.5 https://openai.com/index/introducing-gpt-5-5/, 2026. Released:
     2026-04-23.
[23] Liangming Pan, Alon Albalak, Xinyi Wang, and William Wang. Logic-lm: Empowering
     large language models with symbolic solvers for faithful logical reasoning. In Findings of the
     Association for Computational Linguistics: EMNLP 2023, pages 3806–3824, 2023.
[24] Richard Anthony Russell. Planning with preferences using maximum satisfiability. PhD
     thesis, University of Cambridge, UK, 2012. URL https://ethos.bl.uk/OrderDetails.
     do?uin=uk.bl.ethos.610496.
[25] Ranjan Sapkota, Konstantinos I Roumeliotis, and Manoj Karkee. Vibe coding vs. agentic coding:
     Fundamentals and practical implications of agentic ai. arXiv preprint arXiv:2505.19443, 2025.
[26] Weichun Shi, Minghao Liu, Wanting Zhang, Langchen Shi, Fuqi Jia, Feifei Ma, and Jian Zhang.
     Constraintllm: A neuro-symbolic framework for industrial-level constraint programming. In
     Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing,
     pages 16010–16030, 2025.
[27] Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Bengio, and
     Mehrdad Farajtabar. The illusion of thinking: Understanding the strengths and limitations of
     reasoning models via the lens of problem complexity. In NeurIPS 2025, 2025.
[28] Stefan Szeider. Mcp-solver: Integrating language models with constraint programming systems.
     arXiv preprint arXiv:2501.00539, 2024.
[29] Karthik Valmeekam, Matthew Marquez, Sarath Sreedharan, and Subbarao Kambhampati. On
     the planning abilities of large language models-a critical investigation. Advances in Neural
     Information Processing Systems, 36:75993–76005, 2023.
[30] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le,
     Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models.
     Advances in neural information processing systems, 35:24824–24837, 2022.
[31] Jundong Xu, Hao Fei, Meng Luo, Qian Liu, Liangming Pan, William Yang Wang, Preslav
     Nakov, Mong-Li Lee, and Wynne Hsu. Aristotle: Mastering logical reasoning with a logic-
     complete decompose-search-resolve framework. In Proceedings of the 63rd Annual Meeting
     of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3052–3075,
     2025.
[32] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,
     Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint
     arXiv:2505.09388, 2025.
[33] Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett. Satlm: Satisfiability-aided language
     models using declarative prompting. Advances in Neural Information Processing Systems, 36:
     45548–45580, 2023.
[34] Wenhao Zhu, Hongyi Liu, Qingxiu Dong, Jingjing Xu, Shujian Huang, Lingpeng Kong, Jiajun
     Chen, and Lei Li. Multilingual machine translation with large language models: Empirical
     results and analysis. In Findings of the association for computational linguistics: NAACL 2024,
     pages 2765–2781, 2024.




                                                12
A     Prompt Templates

This appendix summarises the prompt templates used to interact with the LLM S across all ex-
perimental configurations. All prompts are executed with a temperature of 0 and are designed to
explicitly separate semantic interpretation, planning, and formal optimisation. The prompts enforce
solver-backed reasoning and avoid reliance on the LLM ’s internal reasoning traces.

A.1   Intermediate Planning Prompt

When the intermediate planning step is enabled, the LLM is first asked to produce a symbolic
encoding plan before generating any code:

You are an expert MaxSAT/SAT encoding designer.

Given ONLY a natural-language problem description, draft a precise encoding plan
with the following sections:

1) Variables
2) Hard constraints
3) Soft constraints / preferences
4) Objective (weighted MaxSAT)
5) Output schema (repeat the JSON schema to emit)

Do NOT write code.
Do NOT use external data.

The generated plan is provided verbatim to the subsequent code-generation step.

A.2   RC2 Solver Usage Prompt

The following prompt is provided verbatim to the LLM S to explain how to use the RC2 MaxSAT
solver through the PySAT API:

# RC2 / WCNF usage
# IMPORTANT: The call rc2.compute() returns the model (a list of integer literals).
#            If rc2.compute() returns None, then the WCNF formula is UNSAT.
#            The objective (weighted cost) is available as rc2.cost after compute().
#
# Use this exact pattern in your solve() implementation:
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

def rc2_solve_example():
    w = WCNF()
    # Example hard clause: w.append([1, -2])
    # Example soft clause with weight 3: w.append([-3], weight=3)

      rc2 = RC2(w)
      # rc2.compute() returns the model (list of ints) or None if the MaxSAT
      # formula is UNSAT
      model_lits = rc2.compute()   # <- model_lits is a list of signed ints
      # if model_lits is None then the formula is UNSAT
      # Read the cost (sum of falsified soft clause weights) after compute():
      cost = int(rc2.cost)
      assignment = {abs(l): (l > 0) for l in model_lits}
      return cost, assignment

# End of RC2_HELP


                                                13
This prompt is prepended to the code-generation instructions to ensure consistent and correct interac-
tion with the MaxSAT solver across all models and experimental configurations, and to reduce API
misuse and syntactic errors in the generated code.

A.3   Code Generation Prompt (with Plan)

If a plan is available, the following user prompt is used to generate the MaxSAT encoding:

Natural-language problem description:
---
<problem description>
---

Encoding PLAN:
---
<generated plan>
---

You are a code model that writes standalone Python using PySAT to solve a
planning/optimization task from a natural-language description.
Your job: Write PySAT code that exactly models the hard rules and preferences
and computes the optimal solution.
You MUST use python-sat (PySAT) to build and solve a SAT/MaxSAT model
matching the problem.
Use the RC2 example provided in RC2_HELP exactly as a template if helpful.
Write PySAT code implementing the PLAN. Return JSON ONLY as specified.

A.4   Code Generation Prompt (without Plan)

If the intermediate planning step is disabled, the LLM is prompted directly from the natural-language
description:

Problem description:
---
<problem description>
---

You are a code model that writes standalone Python using PySAT
to solve a planning/optimization task from a natural-language description.
Your job: Write PySAT code that exactly models the hard rules
and preferences and computes the optimal solution.
You MUST use python-sat (PySAT) to build and solve a
SAT/MaxSAT model matching the problem.
Use the RC2 example provided in RC2_HELP exactly as a template if helpful.
Return JSON ONLY as specified.

A.5   Direct-Answer Baseline Prompt

For the direct-answer baseline, the LLM is asked to produce a solution without generating code or
invoking solvers:

Problem description:
---
<problem description>
---

You are an expert solver.

Your Job: Provide the optimal solution to the optimization task


                                                 14
from a natural-language description, in using the required JSON schema.

Return ONLY the JSON. No code. JSON only.

A.6   Chain-of-Thought Baseline Prompt

For the chain-of-thought (CoT) baseline, the LLM is encouraged to reason step by step before
producing the final answer:

Problem description:
---
<problem description>
---

You are an expert solver.

Your Job: Provide the optimal solution to the optimization task
from a natural-language description, using the required JSON schema.

Think step-by-step to derive the optimal solution.

Write numbered steps. Then output the final JSON on the last line.

During evaluation, only the final JSON output is considered; the reasoning trace itself is ignored.

A.7   Program-of-Thought Baseline Prompt

For the Program-of-Thought (PoT) baseline, the LLM is prompted to generate standalone Python
code that computes the optimal solution without using any symbolic solver:

Problem description:
---
<problem description>
---

You are an expert Python programmer.

Your task is to solve the optimisation problem described above and
return the optimal solution using the required JSON schema.

Write a standalone Python script that exactly models the hard rules
and preferences and computes the optimal solution for the planning or
optimisation task.

You CANNOT use any symbolic solver or constraint satisfaction method.

Return JSON ONLY as specified.

A.8   Feedback Prompt for Iterative Refinement

When the generated code fails to execute or produces a non-optimal solution, the following feedback
prompt is used to guide refinement:

You previously provided a response for the problem below, but it did not produce
a correct optimal solution or failed to run.

Problem description:
---
<problem description>


                                                 15
---

Previous output or code:
---
<previous model output>
---

Execution result and errors:
---
<stderr and solver feedback>
---

Please provide a corrected solution.
Follow the exact same output specification as before.
If producing code, return a single Python code block that prints:
{ "objective_cost": <int>, "solution_json": <JSON> }
and nothing else.

This feedback loop is repeated for up to five attempts per instance.
All prompts are designed to: (i) externalise optimisation reasoning from the LLM; (ii) enforce
solver-backed reasoning via MaxSAT; (iii) avoid reliance on the model’s internal reasoning traces;
and (iv) enable independent verification of feasibility and optimality during evaluation.

B     Limitations
In this section we present the possible limitations of our work. First, our evaluation focuses on
three families of Boolean optimisation problems: maximum independent set, scheduling, and set
cover. Although these families cover different constraint structures and preference types, they do
not capture the full range of optimisation problems that may arise in real-world decision-making
systems. In particular, problems involving continuous variables, rich numeric constraints, uncertainty,
or multi-agent interaction may require formalisms beyond SAT/MaxSAT. Second, our evaluation
relies on canonical MaxSAT encodings to verify feasibility and optimality. These encodings are used
only for offline evaluation and are not assumed to be available in deployment. In practical settings, the
MaxSAT solver guarantees optimality only with respect to the constraints and preferences encoded
by the LLM. Therefore, while our approach makes optimisation solver-verifiable, it does not by
itself guarantee that the generated encoding fully captures the user’s intended semantics. Third,
performance remains model-dependent. Stronger models such as G EMINI -3.1-P RO and GPT-5.5
benefit substantially from MaxSAT-based code generation, while weaker models are less reliable,
especially on more constrained problem families and harder preference variants. This indicates that
solver-backed reasoning reduces, but does not eliminate, the need for accurate semantic parsing
and modelling by the LLM. Finally, our benchmark consists of controlled problem instances with
structured natural language descriptions. Real user inputs may be more ambiguous, underspecified, or
inconsistent. Handling such cases may require interactive clarification, richer validation mechanisms,
or human oversight. We view these directions as important future work for deploying LLM–MaxSAT
systems in practical preference-aware decision-making settings.




                                                   16
Table 4: Acceptance rates when LLM S generate MaxSAT encodings using an intermediate planning
step produced either by the same model or by a different model.
                Family       Model               Plan-from           none    p1     p2     p3
                                                 G EMINI -3.1-P RO 100.0 44.0 40.0 40.0
                             G EMINI -3.1-P RO   GPT-5.5           100.0 72.0 48.0 0.0
                                                 L LAMA 3.3        88.0 84.0 8.0 4.0
                                                 Q WEN 3-C ODER    96.0 72.0 0.0 8.0
                mis
                                                 G EMINI -3.1-P RO 96.0      72.0 32.0     8.0
                             GPT-5.5             GPT-5.5           96.0      72.0 28.0     8.0
                                                 L LAMA 3.3        88.0      84.0 8.0      4.0
                                                 Q WEN 3-C ODER 100.0        72.0 4.0      0.0
                                                 G EMINI -3.1-P RO   68.0    12.0 12.0 12.0
                             L LAMA 3.3          GPT-5.5              0.0    24.0 4.0 0.0
                                                 L LAMA 3.3          60.0    12.0 12.0 12.0
                                                 Q WEN 3-C ODER       0.0    68.0 0.0 0.0
                                                 G EMINI -3.1-P RO   12.0    68.0   0.0    8.0
                             Q WEN 3-C ODER      GPT-5.5              0.0    16.0   0.0    0.0
                                                 L LAMA 3.3          4.0     52.0   0.0    0.0
                                                 Q WEN 3-C ODER      12.0    68.0   0.0    0.0
                                                 G EMINI -3.1-P RO   96.0    56.0 48.0 36.0
                             G EMINI -3.1-P RO   GPT-5.5             96.0    80.0 52.0 12.0
                                                 L LAMA 3.3          56.0    64.0 4.0 12.0
                                                 Q WEN 3-C ODER      48.0    92.0 12.0 16.0
                scheduling
                                                 G EMINI -3.1-P RO   96.0    80.0 8.0 20.0
                             GPT-5.5             GPT-5.5             92.0    92.0 20.0 20.0
                                                 L LAMA 3.3          56.0    64.0 4.0 12.0
                                                 Q WEN 3-C ODER      48.0    92.0 24.0 16.0
                                                 G EMINI -3.1-P RO   20.0    12.0   4.0    4.0
                             L LAMA 3.3          GPT-5.5              8.0     8.0   4.0    4.0
                                                 L LAMA 3.3          12.0    12.0   8.0    0.0
                                                 Q WEN 3-C ODER      20.0     0.0   0.0    0.0
                                                 G EMINI -3.1-P RO   60.0    20.0   0.0    0.0
                             Q WEN 3-C ODER      GPT-5.5             16.0     8.0   0.0    0.0
                                                 L LAMA 3.3          60.0    20.0   0.0    0.0
                                                 Q WEN 3-C ODER      16.0     0.0   0.0    0.0
                                                 G EMINI -3.1-P RO   100.0   88.0   80.0   80.0
                             G EMINI -3.1-P RO   GPT-5.5             100.0   88.0   68.0   64.0
                                                 L LAMA 3.3          100.0   96.0   72.0   60.0
                                                 Q WEN 3-C ODER      100.0   92.0   68.0   60.0
                setcover
                                                 G EMINI -3.1-P RO   100.0   88.0   72.0   64.0
                             GPT-5.5             GPT-5.5             100.0   88.0   72.0   68.0
                                                 L LAMA 3.3          100.0   96.0   72.0   60.0
                                                 Q WEN 3-C ODER      100.0   92.0   72.0   60.0
                                                 G EMINI -3.1-P RO   80.0    72.0   52.0   36.0
                             L LAMA 3.3          GPT-5.5             68.0    20.0   12.0   24.0
                                                 L LAMA 3.3          68.0    60.0   32.0   20.0
                                                 Q WEN 3-C ODER      76.0    72.0   52.0   36.0
                                                 G EMINI -3.1-P RO   72.0    60.0   44.0 36.0
                             Q WEN 3-C ODER      GPT-5.5             76.0    16.0   32.0 36.0
                                                 L LAMA 3.3          72.0    60.0   44.0 36.0
                                                 Q WEN 3-C ODER      64.0    24.0   20.0 8.0



C    Leveraging Chains of Thought (CoTs) generated by other models
Table 4 presents the complete acceptance rates for MaxSAT encodings generated using an intermediate
planning step produced either by the same model or by a different model.




                                                     17
