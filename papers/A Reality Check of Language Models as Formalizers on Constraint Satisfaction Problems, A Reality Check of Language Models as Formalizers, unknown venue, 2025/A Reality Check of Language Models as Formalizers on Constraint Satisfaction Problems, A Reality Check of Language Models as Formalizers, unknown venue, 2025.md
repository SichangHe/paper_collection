                                         Published at the COLM 2026 Workshop on Efficient Reasoning




                                         A Reality Check of Language Models as Formalizers
                                         on Constraint Satisfaction Problems

                                             Rikhil Amonkar∗       Ceyhun Efe Kayan∗       Qimei Lai
                                             Ronan Le Bras     Li Zhang
                                                 Drexel University   University of Pennsylvania   Allen Institute for AI
                                             {rikhil.amonkar|harry.zhang@drexel.edu}



                                                                                     Abstract
arXiv:2505.13252v6 [cs.CL] 19 Aug 2026




                                                    Recent work shows superior performance when using large language mod-
                                                    els (LLMs) as formalizers instead of as end-to-end solvers for symbolic
                                                    reasoning problems. Given the problem description, the LLM generates a
                                                    formal program that derives a solution via an external solver. We systemati-
                                                    cally investigate the formalization capability of LLMs on real-life constraint
                                                    satisfaction problems on 4 benchmarks, 6 LLMs, and 2 types of formal
                                                    languages. We show that LLM-as-formalizer by no means trivializes the
                                                    problem but underperforms LLM-as-solver in 15 out of 24 model-dataset
                                                    combinations, despite the former’s verifiability and interpretability. Al-
                                                    though the formalization space is magnitudes smaller than the search space,
                                                    our scaling analysis shows that LLM-as-formalizer still drastically degrades
                                                    as problem complexity increases similar to LLM-as-solver. To better under-
                                                    stand this limitation, we observe excessive, solver-like reasoning tokens
                                                    that sometimes lead to hard-coded solutions, highlighting a key challenge
                                                    for improving LLM-based formalization.1


                                         1     Introduction

                                         Considerable efforts have been dedicated to improving the ability of large language models
                                         (LLMs) to solve logical reasoning tasks (Saxton et al., 2019; Clark et al., 2021), primarily in an
                                         end-to-end manner involving intermediate chain-of-thought tokens (Wei et al., 2022; Kojima
                                         et al., 2022). Despite their strong performance, these LLM-as-solver methods have been
                                         shown to lack faithfulness, verifiability, and formal guarantee (Lyu et al., 2023). To bridge
                                         this gap, an emerging line of neuro-symbolic methods use LLMs to translate the natural
                                         language problem description into a formal program, from which a solution can be derived
                                         using an external solver (Gao et al., 2023; Pan et al., 2023; Han et al., 2024). Despite the
                                         desirable features above, the reported triumphant performance of formalization predates
                                         the advance of large reasoning models (LRMs) that scales reasoning tokens during inference
                                         time (Muennighoff et al., 2025; Guo et al., 2025). Most recent work shows the performance
                                         comparison between two methodologies remains unclear and debated (Huang & Zhang,
                                         2025; Kagitha et al., 2025), hindering real-life application.
                                         We systematically compare these two methodologies on constraint satisfaction problems
                                         (CSPs) following existing work that form the backbone of many real-world planning and
                                         scheduling systems, including calendar scheduling, trip planning, and meeting planning,
                                         in addition to a logic grid puzzle. On these 4 domains, we evaluate 6 state-of-the-art
                                         LLMs, including 4 LRMs (DeepSeek-R1, Qwen3-32B, o3-mini-high, GPT-5) and 2 non-
                                         reasoning counterparts (DeepSeek-V3, Qwen2.5-32B), both as solvers and as formalizers.
                                         To ensure maximal generalizability and fairness of comparison, we consider only one-shot
                                         settings with a minimal instruction to generate a solution or a code, but additionally provide
                                         formalizers with revision attempts. We consider two formalization targets: free-form Python
                                         and specific code to interface a Satisfiability Modulo Theories (SMT) solver.
                                              ∗ Equal contribution.
                                              1 Code: github.com/rikhil-amonkar/llm-csp



                                                                                          1
Published at the COLM 2026 Workshop on Efficient Reasoning




Figure 1: An example of the output for LLM-as-solver (top) and LLM-as-formalizer with two
types of formalism (middle and bottom) in a real-life constraint satisfaction task, calendar
scheduling.


While existing work established the superiority of LLM-as-formalizer, we instead show that
it underperforms LLM-as-solver in 12 out of 16 LRM-dataset combinations and 4 out of 8
non-reasoning-LLM-dataset combinations. While many expect LLM-as-formalizer to scale
with problem complexity since the formalization space is magnitudes smaller than the
search space, our analysis shows that its performance still drastically degrades as problem
complexity increases just as LLM-as-solver. We perform a fine-grained error analysis and
attribute the anti-climatic performance of LLM-as-formalizer largely to missing constraints
and erroneous logic. Despite the comparative token efficiency of LLM-as-formalizer for
LRMs, we observe surprising, excessive, solver-like reasoning tokens that sometime lead
to hard-coded solutions, likely an artifact of pre-training. Our work suggests multiple
future directions spanning performance, robustness, and efficiency of neurosymbolic auto-
formalization, which promises verifiability and interpretability.


2     Related Work

2.1   LLM-as-solver

LLM-as-solver, also known as informal reasoning or end-to-end reasoning, is a paradigm
when one or more LLMs generate optional intermediate tokens and eventually the solution
to a logical reasoning problem. As early problem solving ability comes from training, many
major LLMs have been trained or evaluated as a solver (Rajani et al., 2019; Brown et al.,
2020), while limited to low-complexity, common-sense problems. The introduction of chain-
of-thought reasoning made LLM-as-solver feasible in complex tasks such as mathematics
and logic puzzles (Wei et al., 2022; Kojima et al., 2022; Sel et al., 2024; Feng et al., 2023).
Follow-up techniques to further improve LLM-as-solver based on chain-of-thought included
self-verification (Weng et al., 2023), self-refine (Madaan et al., 2023), tree-of-thought (Yao
et al., 2023), self-consistency (Wang et al., 2023), etc.
Despite strong performance, LLM-as-solver has been shown to lack faithfulness, verifiability,
and formal guarantees (Lyu et al., 2023; Turpin et al., 2023; Stechly et al., 2025). To bridge
these gaps, neuro-symbolic methods were introduced to combine LLM-as-solver with formal
tools (Jha et al., 2023; Saparov & He, 2023).

2.2   LLM-as-formalizer

LLM-as-formalizer is a subset of the above neuro-symbolic methods where LLMs generate
neither the solution nor the chain-of-thought towards the solution, but rather translate the
natural language problem description to an executable program based on LLM’s ability to
generate code. This methodology has been reported to greatly outperform LLM-as-solver in
classical planning (Liu et al., 2023; Xie et al., 2023; Hao et al., 2025), constraint satisfaction
(Berman et al., 2024; Kesseli et al., 2025), mathematics (Wu et al., 2022; Yang et al., 2023;
Jiang et al., 2023), and general logical reasoning tasks (Ye et al., 2023; Gao et al., 2023; Pan
et al., 2023; Han et al., 2024). Despite the overwhelming report of its success, it has also been
shown to be unstable, dependent on the choice of formal language and solver (Matthew Lam
et al., 2024; Beiser et al., 2025).


                                                2
Published at the COLM 2026 Workshop on Efficient Reasoning




      Calendar Scheduling        Trip Planning                     Meeting Planning                    Zebra Logic
 Xi   start hour s, end hour e   day d, city c                     person p, start s, duration d       person p, attribute a

 Di   {(s, e) | s, e ∈ [9, 17]   {(d, c) | d ∈ [1, len],           {( p, s, d) | p ∈ P, s ∈ [9, 24],   {( p, a) | p ∈ P, a ∈ A}
      e > s}                     c ∈ C}                            d ∈ [1, 12]}

 Cj   Unavailable time range     Total number of days              Start time and place                Various provided clues
      Meeting duration           Allowed direction of travel       Travel time of two places           about people and attributes
                                 Expected duration in a city       Time and place of a person
                                 Expected city on a day            Min. duration with a person


Table 1: Formal definition of variables Xi , domains Di , and constraints Cj from the 4 domains
in NaturalPlan and ZebraLogic.


2.3   LLM-as-formalizer vs. LLM-as-solver

For effective application, research like ours that systematically compares LLM-as-formalizer
and LLM-as-solver is crucial but lacking, especially with the introduction of LRMs, which
reported dramatically improved performance on algorithmic tasks where LLM-as-solver
used to fail (Muennighoff et al., 2025; Guo et al., 2025). The closest work to ours is Chen
et al. (2025), which did not consider any open-source model or inference-time scaling LRMs,
whereas open-source LRMs are our focus. Moreover, their work is an initial investiga-
tion where conclusions are surface-level (formalizing is hard) and inconclusive (neither is
optimal), while ours is a deep dive resulting in an array of fine-grained, relatively defini-
tive, and somewhat counterintuitive conclusions. The other work that considered both
LLM-as-formalizer and LLM-as-solver for LRMs is Kagitha et al. (2025), which only focuses
on classical planning tasks, similarly lacking decisive findings.


3     Task and Data

To systematically compare LLM-as-solver and LLM-as-formalizer, including various for-
malisms, we prioritize depth over breadth by focusing on real-world CSPs. Such a problem
includes the following elements described in natural language:
      1. A set of variables { Xi }, to be assigned values
      2. Domains of variables { Di }, the possible values of the variables
      3. A set of constraints {Cj }, boolean rules that govern one or more variables
The goal of planning is thus to find a value assignment of each variable Xi based on
possibilities Di that does not violate any constraints Cj .
We consider three domains, including calendar scheduling, trip planning, and meeting
planning provided by the NaturalPlan dataset (Zheng et al., 2024), where only LLM-as-solver
methods have been evaluated (Lee et al., 2025; Parmar et al., 2025) but not LLM-as-formalizer.
We additionally consider a logic grid puzzle domain from the ZebraLogic dataset (Lin et al.,
2025), which is less natural but considered in past work (Berman et al., 2024; Kesseli et al.,
2025) evaluating LLM-as-formalizer methods. The formulation and examples of all three
tasks are shown in Table 1. Unlike previous work that evaluated the predicted solution
by matching the ground-truth solution, we manually and formally annotate all constraints
{Cj }. We therefore count a solution as correct if it formally satisfies all the constraints. This
design choice enables us to perform fine-grained analysis on problem complexity and model
errors. Bound by the cost of annotation, we randomly sample 100 out of 1,000 examples for
each domain. The tasks and prompts are exemplified in Appendix A.


4     Experimental Setup

We prompt LLMs in a one-shot manner to generate three different types of output.


                                                               3
Published at the COLM 2026 Workshop on Efficient Reasoning




Solution. This is the LLM-as-solver pipeline where the LLM is given an input and directly
outputs the answer, optionally after generating a reasoning chain. Noting that most of our
LLMs are LRMs, we do not explicitly prompt any model to “think step by step.”
Python code. This is an LLM-as-formalizer pipeline where the LLM is given an input and
generates a Python program that will be executed to output the answer. Conceptually, the
model generates both the declarative component (i.e., the variables and constraints) and the
search component (i.e., the algorithm to search for the correct plan).
SMT code. Alternatively, the LLM may generate a specific program to invoke a CSP solver,
such as an SMT solver. Following previous work, we prompt LLMs to generate code
using the Z3 solver Python wrapper. Here, the model primarily generates the declarative
component as the search component is simply a call to the pre-defined solver function.
Examples of the two formalisms are juxtaposed in Appendix C.
In all cases, the provided one-shot only illustrates the input-output format, contain-
ing neither an example solution nor an example formalized code. To not discount the
LLM-as-formalizer pipelines, we follow Pan et al. (2023); Ye et al. (2023) to optionally include
a revision-by-error module. If the solver, either implemented by the model in the case
of Python or provided by the Z3 library in the case of SMT, returns an error message or
cannot find any plan, this signal is returned to the LLM to re-generate the program up
to 5 times (see prompt examples in Appendix A). We do not consider specific-purpose
formalization pipelines such as (Hao et al., 2025) which defeats our purpose of studying
general applications. We do not consider more involved LLM-as-solver pipelines as our goal
is to use it as a lower bound to benchmark LLM-as-formalizer.


5     Results

We present our findings guided by a series of research questions.

5.1   RQ1: Are LLMs better formalizers than solvers?

As discussed in Section 2.2, much existing work has shown superior performance of
LLM-as-formalizer on various logical reasoning tasks. However, we observe that LLM-
as-formalizer underperforms LLM-as-solver in 12 out of 16 LRM-dataset combinations
and 4 out of 8 non-reasoning-LLM-dataset combinations (Figure 2). In datasets with more
saturated performance such as Calendar Scheduling, Meeting Planning, and Zebra Logic,
models’ formalization performance is decent but does not exceed the straightforward rea-
soning towards a solution in most cases. On the more challenging Trip Planning dataset,
LLM-as-formalizer consistently underperforms LLM-as-solver. The performance of the two
methods roughly correlates, as an LLM that is a better solver is often also a better formalizer,
even when comparing an LRM like DeepSeek-R1 and a non-reasoning LLM like DeepSeek-V3.
In contrast, the weakest model Qwen2.5 as formalizer outperforms that as a solver. Notably,
revision during formalization induces consistent performance gain in many cases, at the cost
of more calls to the LLM. Comparing formalization targets, general Python outperforms
code to an SMT solver in 15 out of 24 model-dataset combinations, even though SMT is a
tool arguably more suitable for the CSP tasks providing much more syntactic convenience,
while general Python is a higher-resource language during pre-training.

5.2   RQ2: Are formalizers more robust to complexity than solvers?

Even though LLM-as-formalizer underperforms LLM-as-solver, the former is expected to
be more robust to increasing problem complexity than LLM-as-solver because the two
paradigms scale differently in their output structure. End-to-end solving requires the
LLM to navigate the search space which exponentially explodes with the increased variables
and constraints. Even though LRM was introdeuced to address this issue, existing work
(Valmeekam et al., 2024; Shojaee et al., 2025) still pointed out their failure to scale as a
solver when the search space of a problem becomes large. In contrast, formalization in
theory decouples problem description from solution via declarative programming, leav-


                                               4
Published at the COLM 2026 Workshop on Efficient Reasoning




                                                    Calendar Scheduling
   100
    80
    60
    40
    20
     0
                   .5*                3*             n3                  -R
                                                                           1              ini           t-5
               2                   -V              e                                               gp
            en
                              Se
                                ek              Qw                  S eek            o3
                                                                                       -m
         Qw                 ep                                 e  p
                         De                                 De

                                                           Trip Planning
   100
               Solution          Python       Python+rev       SMT         SMT+rev
    80
    60
    40
    20
     0
                .5*                      3*       en
                                                       3                 -R
                                                                           1                 ini        t-5
               2                    -V                                                             gp
            en                  eek             Qw                  S eek            o3
                                                                                        -m
         Qw                 ep
                              S                                e  p
                         De                                 De

                                                       Meeting Planning
   100
    80
    60
    40
    20
     0
                .5*                      3*       en
                                                       3                 -R
                                                                           1              ini           t-5
               2                    -V                                                             gp
            en                  eek             Qw                  S eek            o3
                                                                                        -m
         Qw                 ep
                              S                                e  p
                         De                                 De

                                                           Zebra Logic
   100
    80
    60
    40
    20
     0
                .5*                   3*            en
                                                       3                -R
                                                                          1               ini           t-5
            en
               2                    -V                                ek                -m         gp
                                eek             Qw                 S e               o3
         Qw                 ep
                              S                                ep
                         De                                 De

Figure 2: The percentage of correct plans (defined by formally passing all annotated con-
straints) by LLM-as-solver and LLM-as-formalizer generating both Python and SMT code
of various LLMs on all 4 CSP domains. In the settings with revision, only solver errors,
including the inability to find a plan, induce revisions. LLMs that are not LRMs are marked
by an asterisk (*).


                                                              5
Published at the COLM 2026 Workshop on Efficient Reasoning




                    Calendar Scheduling       Trip Planning               Meeting Planning           Zebra Logic

                                                                                                              Plan
 Qwen2.5*      75                                                                                          Python+rev
                                                                                                            SMT+rev
               50

               25

               0
DeepSeek-V3*




               75

               50

               25

               0

               75
 Qwen3




               50

               25

               0
DeepSeek-R1




               75

               50

               25

               0
                    1   2   3    4    5   1    2   3    4         5   1     2    3    4      5   1    2      3      4

Figure 3: The change in the percentage of correct plans by LLM-as-solver and
LLM-as-formalizer over buckets of examples stratified by complexity measured by the num-
ber of constraints. Data in the NaturalPlan domains is roughly equally partitioned into 5
percentiles, while that in ZebraLogic is partitioned based on the 4 strata provided by the
dataset.


ing the heavy-lifting of search to the solver or the algorithmic component of the output
code. Its workload is therefore linear to the input length, leading the community to expect
substantially better robustness to complexity compared to LLM-as-solver.
We validate the lack of robustness of LRMs as solvers (Figure 3) which quickly fail as
the problems become complex in all domains other than the easiest Calendar Schedul-
ing which we exclude from the discussion below. However, we note that neither does
LLM-as-formalizer scale well with complexity. For the better performing Python formal-
ization, even with revision, the performance on the problems with top 20% most constraints
is less than half of the top 20% least constraints in 10 out of 12 model-dataset combinations
we study. Clearly, even with state-of-the-art LLMs and revision attempts, LLM-as-formalizer
does not show the promised robustness, pointing towards open space for improvement.

5.3             RQ3: Why does LLM-as-formalizer underperform and fail to scale?

To understand why LLMs are struggling to generate syntactically and semantically formal
programs, we consider 4 outcomes:
                • Error: the program is unable to be executed due to an error such as TypeError,
                  RuntimeError, or an error specific to the Z3 library.
                • No plan: the solver outputs a custom message that no plan can be found.
                • Wrong plan: the solver outputs a plan, but the plan does not pass all the constraint
                  checks for NaturalPlan or does not exactly match the ground truth for ZebraLogic.


                                                              6
Published at the COLM 2026 Workshop on Efficient Reasoning




              Qwen3, Py, Trip Qwen3, SMT, Trip    R1, Py, Trip       R1, SMT, Trip   R1, Py, Meeting R1, SMT, Meeting

No revision
Revision




                                          Error        No plan        Wrong plan      Correct

Figure 4: Error analysis of two LRMs Qwen3 and DeepSeek-R1 as both Python and SMT
formalizers. Revision is only allowed in case of errors (red ring) and not being able to find a
plan (brown ring), and thus has no bearing on existing wrong plans (blue ring).




                • Correct plan: the plan is correct.
Figure 4 presents the error analysis of LLM-as-formalizer conducted of on Trip Planning and
Meeting Planning. We focus on these two open-source LRMs with distinct architectures
(Mixture-of-Experts and dense) and on these two tasks, since they exhibit the strongest
contrast in outcomes, with LLM-as-solver consistently outperforming LLM-as-formalizer on
Trip Planning and vice versa in Meeting Planning.
Syntax errors are rare but still existent, while the majority of them are eliminated given
revision. Common syntax errors are diverse and include import errors, value error, and
run-time errors, but are primarily dominated by erroneous use of APIs in the Z3 library for
SMT generation. Similarly, the inability to find a plan, which is a kind of semantic errors,
can be largely addressed with revision. With its effect on both kinds of errors, revision does
increase overall correctness of the solution. The persistent and challenging error is a wrong
plan, which is associated with capabilities of translating constraints and conducting correct
algorithmic reasoning. In real-life applications, validating the correctness of plans assumes
much more resources and risks than validating the existence of a plan.
To further study the root cause of semantic errors, including both cases of “no plan” and
“wrong plan”, we manually annotate 5 examples per domain, per Python or SMT, per Qwen3
or gpt-5 as a formalizer, 80 examples in total. We break down the semantic errors into 3
finer-grained categories:
                • Missing constraint: the program misses the definition of a constraint otherwise
                  present in the problem description.
                • Wrong constraint: the program wrongly defines a constraint as presented in the
                  problem description.
                • Wrong solver: the program wrongly defines or calls the solver.
We count that across domains and formalisms, the majority of the semantic errors are due
to wrongly defining constraints (95% of Qwen3). Examples include treating 2 : 16 as an end
time while it should be the start time for Calendar Scheduling, defining meeting time to be
9 : 16 while it should be 9 : 18 for Meeting plan, and so on. Such trivial errors of information
extraction still plague the state-of-the-art LRMs and cannot be caught by the error message
provided by the solver, posing a great safety concern in real-life applications. This calls for
the need for a specific translation module beyond solely relying on LLMs to perform the
translation from the problem description to the formal program. The other two categories,
missing constraint and wrong solver, are much less common, though still existent.


                                                                 7
Published at the COLM 2026 Workshop on Efficient Reasoning




      Calendar Scheduling            Trip Planning          Meeting Planning             Zebra Logic

                       Plan

10                    Python
                       SMT

 5

 0
       en3           R1           en3           R1           n3            k-R
                                                                              1     en3            R1
  Qw          Se ek-           Qw       S e ek-          Qw
                                                            e
                                                                      ee          Qw         e ek-
           ep                         ep                          epS                   ep S
        De                         De                           De                   De

Figure 5: Number of reasoning tokens (in thousands) generated by LRMs as a solver (Plan)
and as a formalizer (Python and SMT).



           26                           24                            20                            3
                                                                                            36      1
                  4                          6                    7
            10                          10                             13


  (a) Qwen3, Python              (b) Qwen3, SMT      (c) DeepSeek-R1, Python (d) DeepSeek-R1, SMT

Figure 6: The distribution of different types of reasoning chains (code-related, solver-like,
and spurious) in all domains for both LRMs and both formalisms.


5.4    RQ4: Are LRMs more efficient as a formalizer than as a planner?

It is known that LRMs’ impressive performance as a planner comes at a cost of excessive
and often inefficient reasoning chains (Sui et al., 2025). On the other hand, LLM-as-formalizer
may be expected to generate fewer reasoning tokens because the task of formalizing is
O(n + d) with n variables and a domain size of d, as opposed to the worst case O(dn ) for an
NP-complete problem like CSP. We show that indeed LRMs often generate significantly
less reasoning tokens as a formalizer than as a solver. From Figure 5, it can be seen that the
number of tokens is consistently higher for LLM-as-solver compared to LLM-as-formalizer
except the Zebra-Logic domain with Qwen3. We also observe that the number of tokens in
the case of Python formalization is less than SMT formalization.
In addition to the efficiency of the reasoning chains during formalization, we also inspect
their nature by breaking them down into the following granular categories:
       • Code-related reasoning focuses on coding such as errors, edge cases, and fixes.
       • Solver-like reasoning unnecessarily tries to solve the problem like LLM-as-solver,
         but still generates code that declares the constraints and calls a solver.
       • Spurious reasoning hard-codes the answer without the constraints and the solver
         within the code.
We manually annotate the reasoning chains of DeepSeek-R1 and Qwen3 for 10 examples
per domain per formalism, resulting in 160 labels in total. Figure 6 reveals a concerning
phenomenon where only less than 75% of the reasoning chains of Qwen3 and less than 50%
of those of DeepSeek-R1 are primarily code-related. LLM-as-formalizer frequently “reason
like a solver” to perform search, enumeration, and backtracking to attempt to solve the
problem rather than formalizing it. We count that the average number of tokens generated
for such solver-like reasoning more than 1.5 times the token consumption than code-related
reasoning. A likely explanation of this behavioral mismatch is that LRMs are trained to
reason towards a solution, not formalize, and such behavior manifests when the the model
is prompted to formalize, giving rise to suboptimal performance.


                                                     8
Published at the COLM 2026 Workshop on Efficient Reasoning




# Reasoning chain: ... Let me think about a possible sequence.
# Maybe the user should visit Rome on the first day? Wait, but
# that will violate the constraint of being in Dubrovnik for a
# conference. Let me think again...
import json
def main():
    itinerary = [
        {"day_range": "Day 1-2", "place": "Dubrovnik"},
        {"day_range": "Day 3", "place": "Rome (travel from Dubrovnik)"},
        {"day_range": "Day 4", "place": "Riga (travel from Rome)"},
        # More days omitted
    ]
    print(json.dumps({"itinerary": itinerary}))
if __name__ == "__main__":
    main()


Figure 7: An example of solver-like and spurious reasoning resulting in a hard-coded
program (abridged) of DeepSeek-R1 as a Python formalizer on Trip Planning.


Despite those shortcomings, one of the built-in advantages of LLM-as-formalizer is its im-
proved interpretability, verifiability, and faithfulness, as previously discussed. However,
spurious reasoning, the most insidious category of reasoning chains, nullifies this advantage.
Figure 7 shows an example of spurious reasoning, where the model not only generates a
solver-like, unnecessary reasoning chain, but also hard-codes the entire proposed solution
in the output program without performing any declaration of constraints or implementa-
tion of search. These undesired behavioral deviations from the formalization instruction
indicates a tendency that steers LLMs towards solving the problem directly instead of for-
malization. Regardless of the correctness, a practitioner would have no way of interpreting
and verifying such a hard-coded program. Unnecessary reasoning chains constitutes as
much as 90% of programs generated by Deepseek-R1 in all domains, revealing a considerable
concern in safety.

6   Conclusion

We provide a comprehensive evaluation of LLMs’ ability to formalize real-life constraint
satisfaction problems and outsourcing the heavy-lifting of search to external tools. In
contrastive to existing work that advocates for the efficacy of LLM-as-formalizer, we show
that it consistently underperforms LLM-as-solver on real-life constraint satisfaction problems,
offering no more scalability with problem complexity. Our in-depth error analysis points to
missing constraints and erroneous logic, internally caused by excessive, solver-like reasoning
tokens that sometime lead to hard-coded solution. Our work indicates urgency in addressing
these issues for LLM-as-formalizer that otherwise promises verifiability, interpretability, and
application in high-stakes domains.

References
Alexander Beiser, David Penz, and Nysret Musliu. Intermediate languages matter: Formal
  choice drives neurosymbolic llm reasoning, 2025. URL https://arxiv.org/abs/2502.
  17216.
Shmuel Berman, Kathleen McKeown, and Baishakhi Ray. Solving zebra puzzles using
  constraint-guided multi-agent systems, 2024. URL https://arxiv.org/abs/2407.03956.
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini
  Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya
  Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen,
  Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner,


                                              9
Published at the COLM 2026 Workshop on Efficient Reasoning




  Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are
  few-shot learners. In Proceedings of the 34th International Conference on Neural Information
  Processing Systems, NIPS ’20, Red Hook, NY, USA, 2020. Curran Associates Inc. ISBN
  9781713829546.
Yongchao Chen, Harsh Jhamtani, Srinagesh Sharma, Chuchu Fan, and Chi Wang. Steering
  large language models between code execution and textual reasoning. In The Thirteenth
  International Conference on Learning Representations, 2025. URL https://openreview.net/
  forum?id=5X5Z7Ffrjb.
Peter Clark, Oyvind Tafjord, and Kyle Richardson. Transformers as soft reasoners over
  language. In Proceedings of the Twenty-Ninth International Joint Conference on Artificial
  Intelligence, IJCAI’20, 2021. ISBN 9780999241165.
Guhao Feng, Bohang Zhang, Yuntian Gu, Haotian Ye, Di He, and Liwei Wang. Towards
 revealing the mystery behind chain of thought: A theoretical perspective. In Thirty-seventh
 Conference on Neural Information Processing Systems, 2023. URL https://openreview.net/
 forum?id=qHrADgAdYu.
Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan,
  and Graham Neubig. Pal: program-aided language models. In Proceedings of the 40th
  International Conference on Machine Learning, ICML’23. JMLR.org, 2023.
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu,
 Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin
 Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao
 Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chong Ruan, Damai Dai,
 Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao,
 Guanting Chen, Guowei Li, H. Zhang, Hanwei Xu, Honghui Ding, Huazuo Gao, Hui
 Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jingchang Chen, Jingyang Yuan, Jinhao Tu, Junjie
 Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaichao
 You, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang
 Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang,
 Minghui Tang, Mingxu Zhou, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan
 Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang,
 Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou,
 Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan,
 S. S. Li, Shuang Zhou, Shaoqing Wu, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding
 Zeng, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao,
 Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin
 Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q.
 Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan
 Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang,
 Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan
 Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan
 Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan
 Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanping Huang,
 Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z.
 Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen
 Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li,
 Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and
 Zhen Zhang. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning.
 Nature, 645(8081):633–638, Sep 2025. ISSN 1476-4687. doi: 10.1038/s41586-025-09422-z.
 URL https://doi.org/10.1038/s41586-025-09422-z.
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Wenfei Zhou,
  James Coady, David Peng, Yujie Qiao, Luke Benson, Lucy Sun, Alexander Wardle-Solano,
  Hannah Szabó, Ekaterina Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu, Brian Wong,
  Malcolm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai, Tao Yu, Rui Zhang, Alexander
  Fabbri, Wojciech Maciej Kryscinski, Semih Yavuz, Ye Liu, Xi Victoria Lin, Shafiq Joty,
  Yingbo Zhou, Caiming Xiong, Rex Ying, Arman Cohan, and Dragomir Radev. FOLIO:


                                             10
Published at the COLM 2026 Workshop on Efficient Reasoning




  Natural language reasoning with first-order logic. In Yaser Al-Onaizan, Mohit Bansal,
  and Yun-Nung Chen (eds.), Proceedings of the 2024 Conference on Empirical Methods in
  Natural Language Processing, pp. 22017–22031, Miami, Florida, USA, November 2024.
  Association for Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.1229.
  URL https://aclanthology.org/2024.emnlp-main.1229/.

Yilun Hao, Yang Zhang, and Chuchu Fan. Planning anything with rigor: General-purpose
  zero-shot planning with LLM-based formalized programming. In The Thirteenth Interna-
  tional Conference on Learning Representations, 2025. URL https://openreview.net/forum?
  id=0K1OaL6XuK.

Cassie Huang and Li Zhang. On the limit of language models as planning formalizers. In
 Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (eds.),
  Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume
 1: Long Papers), pp. 4880–4904, Vienna, Austria, July 2025. Association for Computational
  Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/2025.acl-long.242. URL https:
 //aclanthology.org/2025.acl-long.242/.

Susmit Jha, Sumit Kumar Jha, Patrick Lincoln, Nathaniel D. Bastian, Alvaro Velasquez, and
  Sandeep Neema. Dehallucinating large language models using formal methods guided
  iterative prompting. In 2023 IEEE International Conference on Assured Autonomy (ICAA),
  pp. 149–152, 2023. doi: 10.1109/ICAA58325.2023.00029.

Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng Liu, Wenda
  Li, Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. Draft, sketch, and prove: Guiding
  formal theorem provers with informal proofs. In The Eleventh International Conference on
  Learning Representations, 2023. URL https://openreview.net/forum?id=SMa9EAovKMC.

Prabhu Prakash Kagitha, Andrew Zhu, and Li Zhang. Addressing the challenges of planning
  language generation, 2025. URL https://arxiv.org/abs/2505.14763.

Pascal Kesseli, Peter O’Hearn, and Ricardo Silveira Cabral. Logic.py: Bridging the gap
  between llms and constraint solvers, 2025. URL https://arxiv.org/abs/2502.15776.

Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.
  Large language models are zero-shot reasoners. In Proceedings of the 36th International
  Conference on Neural Information Processing Systems, NIPS ’22, Red Hook, NY, USA, 2022.
  Curran Associates Inc. ISBN 9781713871088.

Kuang-Huei Lee, Ian Fischer, Yueh-Hua Wu, Dave Marwood, Shumeet Baluja, Dale
 Schuurmans, and Xinyun Chen. Evolving deeper llm thinking, 2025. URL https:
 //arxiv.org/abs/2501.09891.

Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Pooven-
  dran, Peter Clark, and Yejin Choi. Zebralogic: On the scaling limits of LLMs for logi-
  cal reasoning. In Forty-second International Conference on Machine Learning, 2025. URL
  https://openreview.net/forum?id=sTAJ9QyA6l.

Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Peter
  Stone. Llm+ p: Empowering large language models with optimal planning proficiency.
  arXiv preprint arXiv:2304.11477, 2023.

Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang, Delip Rao, Eric Wong, Marianna
  Apidianaki, and Chris Callison-Burch. Faithful chain-of-thought reasoning. In Jong C.
  Park, Yuki Arase, Baotian Hu, Wei Lu, Derry Wijaya, Ayu Purwarianti, and Adila Alfa
  Krisnadhi (eds.), Proceedings of the 13th International Joint Conference on Natural Language
  Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computa-
  tional Linguistics (Volume 1: Long Papers), pp. 305–329, Nusa Dua, Bali, November 2023.
  Association for Computational Linguistics. doi: 10.18653/v1/2023.ijcnlp-main.20. URL
  https://aclanthology.org/2023.ijcnlp-main.20/.


                                              11
Published at the COLM 2026 Workshop on Efficient Reasoning




Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegr-
 effe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bod-
 hisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh,
 and Peter Clark. Self-refine: Iterative refinement with self-feedback. In Thirty-seventh
 Conference on Neural Information Processing Systems, 2023. URL https://openreview.net/
 forum?id=S37hOerQLB.
Long Hei Matthew Lam, Ramya Keerthy Thatikonda, and Ehsan Shareghi. A closer look
  at tool-based logical reasoning with LLMs: The choice of tool matters. In Tim Baldwin,
  Sergio José Rodríguez Méndez, and Nicholas Kuo (eds.), Proceedings of the 22nd Annual
  Workshop of the Australasian Language Technology Association, pp. 41–63, Canberra, Australia,
  December 2024. Association for Computational Linguistics. URL https://aclanthology.
  org/2024.alta-1.4/.
Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi,
  Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple
  test-time scaling, 2025. URL https://arxiv.org/abs/2501.19393.
Liangming Pan, Alon Albalak, Xinyi Wang, and William Wang. Logic-LM: Empowering
  large language models with symbolic solvers for faithful logical reasoning. In Houda
  Bouamor, Juan Pino, and Kalika Bali (eds.), Findings of the Association for Computational
  Linguistics: EMNLP 2023, pp. 3806–3824, Singapore, December 2023. Association for
  Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.248. URL https:
  //aclanthology.org/2023.findings-emnlp.248/.
Mihir Parmar, Xin Liu, Palash Goyal, Yanfei Chen, Long Le, Swaroop Mishra, Hossein
 Mobahi, Jindong Gu, Zifeng Wang, Hootan Nakhost, Chitta Baral, Chen-Yu Lee, Tomas
 Pfister, and Hamid Palangi. Plangen: A multi-agent framework for generating planning
 and reasoning trajectories for complex problem solving, 2025. URL https://arxiv.org/
 abs/2502.16111.
Nazneen Fatema Rajani, Bryan McCann, Caiming Xiong, and Richard Socher. Explain
 yourself! leveraging language models for commonsense reasoning. In Anna Ko-
 rhonen, David Traum, and Lluís Màrquez (eds.), Proceedings of the 57th Annual Meet-
 ing of the Association for Computational Linguistics, pp. 4932–4942, Florence, Italy, July
 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1487. URL
 https://aclanthology.org/P19-1487/.
Abulhair Saparov and He He. Language models are greedy reasoners: A systematic
 formal analysis of chain-of-thought. In The Eleventh International Conference on Learning
 Representations, 2023. URL https://openreview.net/forum?id=qFVVBzXxR2V.
David Saxton, Edward Grefenstette, Felix Hill, and Pushmeet Kohli. Analysing math-
 ematical reasoning abilities of neural models. In International Conference on Learning
 Representations, 2019. URL https://openreview.net/forum?id=H1gR5iR5FX.
Bilgehan Sel, Ahmad Al-Tawaha, Vanshaj Khattar, Ruoxi Jia, and Ming Jin. Algorithm of
  thoughts: enhancing exploration of ideas in large language models. In Proceedings of the
  41st International Conference on Machine Learning, ICML’24. JMLR.org, 2024.
Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Bengio, and
  Mehrdad Farajtabar. The illusion of thinking: Understanding the strengths and limitations
  of reasoning models via the lens of problem complexity, 2025. URL https://arxiv.org/
  abs/2506.06941.
Kaya Stechly, Karthik Valmeekam, and Subbarao Kambhampati. On the self-verification
  limitations of large language models on reasoning and planning tasks. In The Thirteenth
  International Conference on Learning Representations, 2025. URL https://openreview.net/
  forum?id=4O0v4s3IzY.
Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi
  Liu, Andrew Wen, Shaochen Zhong, Na Zou, Hanjie Chen, and Xia Hu. Stop overthinking:


                                             12
Published at the COLM 2026 Workshop on Efficient Reasoning




  A survey on efficient reasoning for large language models. Transactions on Machine Learning
  Research, 2025. ISSN 2835-8856. URL https://openreview.net/forum?id=HvoG8SxggZ.

Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman. Language models don’t
 always say what they think: unfaithful explanations in chain-of-thought prompting. In
 Proceedings of the 37th International Conference on Neural Information Processing Systems,
 NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc.

Karthik Valmeekam, Kaya Stechly, and Subbarao Kambhampati. Llms still can’t plan;
  can lrms? a preliminary evaluation of openai’s o1 on planbench, 2024. URL https:
 //arxiv.org/abs/2409.13373.

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang,
 Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought
  reasoning in language models. In The Eleventh International Conference on Learning Repre-
  sentations, 2023. URL https://openreview.net/forum?id=1PL1NIMMrw.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H.
  Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large
  language models. In Proceedings of the 36th International Conference on Neural Information
  Processing Systems, NIPS ’22, Red Hook, NY, USA, 2022. Curran Associates Inc. ISBN
  9781713871088.

Yixuan Weng, Minjun Zhu, Fei Xia, Bin Li, Shizhu He, Shengping Liu, Bin Sun, Kang Liu,
  and Jun Zhao. Large language models are better reasoners with self-verification. In Houda
  Bouamor, Juan Pino, and Kalika Bali (eds.), Findings of the Association for Computational
  Linguistics: EMNLP 2023, pp. 2550–2575, Singapore, December 2023. Association for
  Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.167. URL https:
  //aclanthology.org/2023.findings-emnlp.167/.

Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik, and
  Christian Szegedy. Autoformalization with large language models. In Proceedings of the
  36th International Conference on Neural Information Processing Systems, NIPS ’22, Red Hook,
  NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088.

Yaqi Xie, Chen Yu, Tongyao Zhu, Jinbin Bai, Ze Gong, and Harold Soh. Translating natural
  language to planning goals with large-language models. arXiv preprint arXiv:2302.05128,
  2023.

Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
  Godil, Ryan Prenger, and Anima Anandkumar. Leandojo: theorem proving with retrieval-
  augmented language models. In Proceedings of the 37th International Conference on Neural
  Information Processing Systems, NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc.

Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and
  Karthik Narasimhan. Tree of thoughts: deliberate problem solving with large language
  models. In Proceedings of the 37th International Conference on Neural Information Processing
  Systems, NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc.

Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett. Satlm: satisfiability-aided language
  models using declarative prompting. In Proceedings of the 37th International Conference
  on Neural Information Processing Systems, NIPS ’23, Red Hook, NY, USA, 2023. Curran
  Associates Inc.

Huaixiu Steven Zheng, Swaroop Mishra, Hugh Zhang, Xinyun Chen, Minmin Chen, Azade
 Nova, Le Hou, Heng-Tze Cheng, Quoc V. Le, Ed H. Chi, and Denny Zhou. Natural plan:
 Benchmarking llms on natural language planning. 2024. URL https://arxiv.org/abs/
 2406.04520.


                                             13
Published at the COLM 2026 Workshop on Efficient Reasoning




A   Data and Prompt Examples
We use the prompt wordings from NaturalPlan as is, but provide some examples here for
the paper to be self-contained. Here is an example from the calendar scheduling task:
You are an expert at scheduling meetings . You are given a few
constraints on the existing schedule of each participant , the meeting
duration , and possibly some preferences on the meeting time . Note there
exists a solution that works with existing schedule of every
participant . Here are a few example tasks and solutions : TASK : You need
to schedule a meeting for James and John for one hour between the work
hours of 9:00 to 17:00 on Monday .           Here are the existing schedules for
everyone during the day : James has blocked their calendar on Monday
during 11:30 to 12:00 , 14:30 to 15:00; John is busy on Monday during
9:30 to 11:00 , 11:30 to 12:00 , 12:30 to 13:30 , 14:30 to 16:30;         Find a
time that works for everyone 's schedule and constraints . Please provide
your solution in a JSON format as as
{" start ":{" day ":" Monday " ," time "13:30"} ,
" end ":{" day ":" Monday " ," time "14:30"}}.

To facilitate parsing, we add the last sentence to encourage an output in JSON. Here is an
example from the trip planning task:
You plan to visit 3 European cities for 7 days in total . You only take
direct flights to commute between cities . You want to spend 4 days in
Madrid . You would like to visit Dublin for 3 days . You want to spend 2
days in Tallinn . You have to attend a workshop in Tallinn between day 6
and day 7. Here are the cities that have direct flights : Madrid and
Dublin , Dublin and Tallinn . Find a trip plan of visiting the cities for
7 days by taking direct flights to commute between them . Please provide
your solution in a JSON format as as {" itinerary ": [{" day_range ": " Day
1 -2" , " place ": " Reykjavik "} , {" day_range ": " Day 2 -4" , " place ":
" Stockholm "}......]}.

Here is an example from the meeting planning task:
You are visiting San Francisco for the day and want to meet as many
friends as possible . Solve the problem by considering various different
schedules and picking the best one to optimize your goals . Travel
distances ( in minutes ): Sunset District to Chinatown : 30. Sunset
District to Russian Hill : 24. Sunset District to North Beach : 29.
Chinatown to Sunset District : 29. Chinatown to Russian Hill : 7.
Chinatown to North Beach : 3. Russian Hill to Sunset District : 23.
Russian Hill to Chinatown : 9. Russian Hill to North Beach : 5. North
Beach to Sunset District : 27. North Beach to Chinatown : 6. North Beach
to Russian Hill : 4. CONSTRAINTS : You arrive at Sunset District at
9:00 AM . Anthony will be at Chinatown from 1:15 PM to 2:30 PM . You 'd like
to meet Anthony for a minimum of 60 minutes . Rebecca will be at Russian
Hill from 7:30 PM to 9:15 PM . You 'd like to meet Rebecca for a minimum of
105 minutes . Melissa will be at North Beach from 8:15 AM to 1:30 PM . You 'd
like to meet Melissa for a minimum of 105 minutes . Please provide your
solution in a JSON format as as {" itinerary ": [{" action ": " meet ",
" location ": " Golden Gate Park ", " person ": " David " ," start_time ": "13:00" ,
" end_time ": "14:00"} , ...]}.

For all methods, we provide one-shot only to illustrate the format of each problem. For
LLM-as-formalizer, we prompt the LLM to write code which produces the output in the for-
mat specified above, though this cannot be guaranteed. We perform simple post-processing
with the aid of a small LLM, gpt-4.1-mini. To encourage models’ formalization behavior,
we additionally append the following wording.
Solve the following problem by
1. First conducting a reasoning to form a generalizible solution method
2. Then applying the formed solution technique in a python script
enclosed in ``` python and ```.


                                           14
Published at the COLM 2026 Workshop on Efficient Reasoning




    100
                                                   Calendar scheduling
    80
    60
    40
    20
     0

    100
                                                           Trip planning
    80
    60                                                     1-shot       5-shot
    40
    20
     0

    100
                                                     Meeting planning
    80
    60
    40
    20
     0




                                                                                                    i
                                                     8B




                                                                     B



                                                                                        B




                                                                                                               i
              an



                         8B



                                       0B




                                                                                                   in



                                                                                                             in
                                                                    70



                                                                                   71
                                                       -




                                                                                                  m
          um




                        1-



                                      -7




                                                                                                         -m
                                                    R1




                                                                    -



                                                                                   -6
                                                                 R1




                                                                                               o-
                        3.



                                       1




                                                                              R1




                                                                                                        o3
                                    3.



                                                 k-
          H



                    a-




                                                                                              t-4
                                                              k-
                                a-



                                               ee




                                                                               -
                   am




                                                                            ek
                                                             ee




                                                                                            gp
                               am



                                             pS



                                                           pS



                                                                         Se
               Ll



                             Ll



                                           ee




                                                                        p
                                                      ee
                                           D




                                                                     ee
                                                     D



                                                                    D




Figure 8: The performance of preliminary studies of 1-shot and 5-shot prompting on all 3
domains of NaturalPlan for LLM-as-solver.


or
2. Implement a python script enclosed in ``` python and ``` that solves
the problem using the z3 solver .



B   Few-Shot versus One-Shot

In our preliminary experiment, we compared both 5-shot prompting and 1-shot prompting
(default of this paper). For the former, we use the 5-shot prompts provided by NaturalPlan.
We evaluate only generating plan on all 3 tasks, because in-context exemplars for code
generation requires expertise in annotation and is thus unrealistic. From Figure 8, 5-shot
prompting does not increase performance in most cases, while occasionally hurting per-
formance. We inspected its performance gain for some models in meeting planning, and
conclude that many errors in 1-shot settings are due to not conforming to a specific output
format. These errors are mitigated via 5-shot prompting, while adding little value to insights
into reasoning. In later experiments, we relaxed the stringency on output format and rely
more on post-processing for a fairer evaluation.


C    Python and Z3 Code

To showcase the difference between the general Python syntax and the Z3-Python syntax,
consider the following example input:
Find the earliest 1- hour meeting time between 9AM -5 PM .
9 AM -10 AM is not available .


                                                             15
Published at the COLM 2026 Workshop on Efficient Reasoning




          Listing (1) Python solution                      Listing (2) Z3 solution
                                                  from z3 import Int , Optimize

meeting_duration = 1                              meeting_duration = 1
working_start = 9                                 working_start = 9
working_end = 17                                  working_end = 17
# declare disallowed time
unavailable = [(9 , 10) ]                         # declare the start time variable
                                                  start = Int ( ' start ')
# declare the start time variable
# declare alowed time                             opt = Optimize ()
for start in range ( working_start ,              # declare disallowed time
working_end - meeting_duration +                  opt . add ( start != 9)
1) :
     conflict = False                             # declare alowed time
     # check disallowed time                      opt . add ( start >= working_start )
     for u_start , u_end in                       opt . add ( start + meeting_duration
unavailable :                                     <= working_end )
          if not ( start +
meeting_duration <= u_start or                    # find the earliest time
start >= u_end ):                                 opt . minimize ( start )
               conflict = True
               break                              if opt . check () == 0:
     if conflict :                                     m = opt . model ()
          continue                                     s = m[ start ]. as_long ()
     # find the earliest time                          print (f" Earliest meeting :
     print (f" Earliest meeting :                 {s }:00 to {s +
{ start }:00 to { start +                         meeting_duration }:00 ")
meeting_duration }:00 ")                          else :
     break                                             print (" No solution found .")

         Figure 9: Side-by-side comparison of pure Python and Z3-Python code.


The correct solution (generated by o3-mini) is shown in Figure 9. Both include two distinctive
components of declarative code and algorithmic code.

D    More Error Analysis

Another example of a hard-coded solution due to spurious reasoning is shown in Figure 10.

E   License

The NaturalPlan dataset we use is licensed under Apache License 2.0.




                                             16
Published at the COLM 2026 Workshop on Efficient Reasoning




import json
def compute_itinerary () :
    # Input parameters
    total_days = 16
    days_in_lyon = 7
    days_in_bucharest = 7
    days_in_porto = 4
    # Available direct flights :
    # Bucharest <-> Lyon , Lyon <-> Porto
    # Additional constraint :
    # - There is a wedding in Bucharest between day 1 and day 7, so one
must be in Bucharest
    #    during that period .
    # - Note : if one flies from a city A to city B on a day , that day
counts as a day in both A and B.
    # We have three cities to visit :
    #    Bucharest , Lyon , and Porto .
    # With 2 flights ( transitions ) , the overlapping days count for both
cities .
    # Let the flight from Bucharest to Lyon be on day f1 and the flight
from Lyon to Porto be on day f2 .
    # The days spent in each city are :
    #    Bucharest : days 1 to f1 ( inclusive )          -> count = f1
    #    Lyon : day f1 ( arrival day ) + full days from ( f1 +1) to (f2 -1) +
day f2 ( departure day )
    #            -> count = 1 + ( f2 - f1 - 1) + 1 = f2 - f1 + 1
    #    Porto : day f2 ( arrival day ) + days ( f2 +1) to total_days
    #            -> count = 1 + ( total_days - f2 )
    # We want :
    #    f1 = days_in_bucharest = 7 ( so that days 1 -7 cover Bucharest ,
    #         ensuring the wedding is attended in the first 7 days )
    #    For Lyon : f2 - f1 + 1 = days_in_lyon = 7
    #               => f2 - 7 + 1 = 7 -> f2 = 7 + 6 = 13
    #    Then Porto : 1 + ( total_days - f2 ) = 1 + (16 - 13) = 4 =
days_in_porto
    # This gives :
    flight_day_bucharest_to_lyon = 7 # f1
    flight_day_lyon_to_porto = 13                # f2
    # Building the itinerary :
    # The trip plan segments :
    # 1. Bucharest from day 1 to day 7 ( day 7 is used for the flight and
counts as Bucharest )
    # 2. Lyon from day 7 to day 13 ( day 7 from arrival flight , day 13
for departure flight )
    # 3. Porto from day 13 to day 16 ( day 13 counts as the arrival day )
    itinerary = [
         {" day_range ": " 1 -7 " , " place ": " Bucharest "},
         {" day_range ": " 7 -13 " , " place ": " Lyon "},
         {" day_range ": " 13 -16 " , " place ": " Porto "}
    ]
    # Output result as a JSON - formatted dictionary
    result = {" itinerary ": itinerary }
    return result
def main () :
    itinerary_plan = compute_itinerary ()
    print ( json . dumps ( itinerary_plan ))
if __name__ == ' __main__ ':
    main ()

Figure 10: Another Python program generated by o3-mini on trip planning which hard-
codes the solution.



                                        17
