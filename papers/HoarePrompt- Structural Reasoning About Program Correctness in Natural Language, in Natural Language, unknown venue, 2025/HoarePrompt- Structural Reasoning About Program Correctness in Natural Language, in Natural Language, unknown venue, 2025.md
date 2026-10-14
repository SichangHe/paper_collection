                                        HoarePrompt: Structural Reasoning About Program Correctness
                                                            in Natural Language
                                               Dimitrios Stamatios Bouras                                               Yihan Dai                                    Tairan Wang
                                                2501112125@stu.pku.edu.cn                                 2501112020@stu.pku.edu.cn                           tairan.wang.22@ucl.ac.uk
                                            Key Laboratory of HCST (PKU), MoE,                        Key Laboratory of HCST (PKU), MoE,                      University College London
                                                  SCS, Peking University                                    SCS, Peking University                            London, United Kingdom
                                                      Beijing, China                                            Beijing, China

                                                                                         Yingfei Xiong                                   Sergey Mechtaev∗
                                                                                xiongyf@pku.edu.cn                                    mechtaev@pku.edu.cn
arXiv:2503.19599v3 [cs.SE] 8 Sep 2026




                                                                         Key Laboratory of HCST (PKU), MoE,                     Key Laboratory of HCST (PKU), MoE,
                                                                               SCS, Peking University                                 SCS, Peking University
                                                                                   Beijing, China                                         Beijing, China

                                        Abstract                                                                                 Brazil. ACM, New York, NY, USA, 43 pages. https://doi.org/10.1145/3744916.
                                        While software requirements are often expressed in natural lan-                          3773206
                                        guage, verifying the correctness of a program against such require-
                                        ments is a hard and underexplored problem. Large language mod-                           1    Introduction
                                        els (LLMs) are promising candidates for addressing this challenge,                       Assessing whether a program meets its requirements is a key part of
                                        however, our experience shows that they are ineffective in this                          software quality assurance. In practice, these requirements are often
                                        task, often failing to detect even straightforward bugs. To address                      written in natural language, geared towards human-to-human com-
                                        this gap, we introduce HoarePrompt, a novel approach that adapts                         munication or designed as prompts for LLMs. Verifying program
                                        fundamental ideas from program verification to natural language                          correctness against such requirements is an inherently difficult and
                                        artifacts. Inspired by the strongest postcondition calculus, Hoare-                      unexplored challenge. One approach is address it is to generate
                                        Prompt employs a systematic, step-by-step process in which an                            tests based on requirements using an LLM, and use these tests to
                                        LLM generates natural language descriptions of reachable program                         check program correctness [5]. More generally, natural language
                                        states at various code points. To manage loops, we propose few-                          requirements can be translated in formal ones, and then used in
                                        shot-driven k-induction, an adaptation of the k-induction method                         conjunction with verification tools [16]. Despite the promise of
                                        widely used in model checking. Once program states are described,                        these approaches, our experiments show that LLMs tend to gen-
                                        HoarePrompt leverages the LLM to assess whether the program,                             erate incorrect or incomplete assertions when handling complex
                                        annotated with these state descriptions, conforms to the natural                         requirements, which reduces their accuracy. Another option is to
                                        language requirements. For evaluating the quality of classifiers of                      directly employ LLMs to assess a program’s conformance to re-
                                        program correctness with respect to natural language requirements,                       quirements, relying on LLMs’ ability to reason about both natural
                                        we constructed CoCoClaNeL, a challenging dataset of solutions to                         language and code [34]. Our experiments show that the state-of-
                                        programming competition problems. Our experiments show that                              the-art LLMs struggle with this task, often failing to identify even
                                        HoarePrompt improves the MCC by 61% compared to directly using                           simple bugs. We attribute this limitation to the models’ inability to
                                        Zero-shot-CoT prompts for correctness classification. Furthermore,                       reason about the intricacies of program semantics.
                                        HoarePrompt outperforms a classifier that assesses correctness                              To address this gap, we introduce HoarePrompt, a program analy-
                                        via LLM-based test generation by an MCC increase of 106%. The                            sis approach for reasoning about program correctness w.r.t. natural
                                        inductive reasoning mechanism contributes a 26% boost to MCC,                            language requirements that synergizes LLM reasoning techniques
                                        underscoring its effectiveness in managing loops.                                        with ideas from program verification. In its core is the natural Hoare
                                        ACM Reference Format:                                                                    triple, a variant of the traditional Hoare triple [22] with pre- and
                                        Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey            postconditions expressed in natural language; for example,
                                        Mechtaev. 2026. HoarePrompt: Structural Reasoning About Program Cor-                           {x is a full name} x = x.split() [0] {x is a first name}.
                                        rectness in Natural Language. In 2026 IEEE/ACM 48th International Confer-
                                        ence on Software Engineering (ICSE ’26), April 12–18, 2026, Rio de Janeiro,              Inspired by the strongest postcondition calculus [14], HoarePrompt
                                                                                                                                 employs a step-by-step process to generate natural language de-
                                        ∗ Sergey Mechtaev is the corresponding author.
                                                                                                                                 scriptions of reachable program states at various points in the code.
                                                                                                                                 This is achieved by sampling natural strongest postconditions (NSP)
                                        Please use nonacm option or ACM Engage class to enable CC licenses                       from SP, our LLM-based natural Hoare triple completion model
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.    defining the conditional probability distribution SP (Post | Pre, 𝐶),
                                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                      where Pre, Post are natural pre- and postconditions, 𝐶 is a program
                                        © 2026 Copyright held by the owner/author(s).
                                        ACM ISBN 979-8-4007-2025-3/2026/04                                                       fragment. Inspired by methods to enhance LLM reasoning about
                                        https://doi.org/10.1145/3744916.3773206                                                  program execution [38], HoarePrompt uses these state descriptions
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                       Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


Table 1: Success rates for detecting the bug in Figure 1 via                     • HoarePrompt, the first program analysis approach using nat-
prompts with and without state annotations, using four                             ural language as the medium for reasoning about program
LLMs, across 60 responses for each, with the temperature 0.5.                      semantics.
                                                                                 • Few-shot-driven 𝑘-induction, the first approach that enhances
       Model                          Not Annotated   Annotated                    LLM’s ability to summarize loops.
       Qwen2.5-7B                              0%       11.7%                    • CoCoClaNeL, a challenging benchmark for program correct-
       Qwen2.5-Coder-32B                      15%        85%                       ness classification.
       Qwen2.5-72B                            35%        85%                     • An empirical study of classifying program correctness w.r.t.
       Llama3.1-70B                           50%       100%                       natural language requirements and guiding code generation,
                                                                                   demonstrating the effectiveness of HoarePrompt.
                                                                               All code, scripts, and data, to reproduce this work are available at
to annotate a program, and then prompts an LLM to assess if the                Figshare: https://figshare.com/s/5d39b388bd9ff2c7ffab.
annotated program aligns with the given requirements.
   HoarePrompt’s key novelty in comparison with traditional pro-                2     Motivating Examples
gram analysis and verification is in using natural language as the             To motivate our approach, we first show that annotating a program
medium of reasoning about program semantics, as opposed to,                    with natural language descriptions of reachable program states
e.g., first-order logic [17] or monotonic functions over lattices [10].        enhances LLM’s reasoning about program correctness, and then
This enables a direct application of HoarePrompt to assessing pro-             show how our approach precisely summarizes loops.
gram correctness w.r.t. natural language requirements without hard
and time-consuming formal modeling. In comparison to previous                   2.1     State Descriptions Enhance LLM Reasoning
techniques for reasoning about code with LLMs [28, 34, 38], Hoare-             Consider the following problem: “given an integer list, the task
Prompt reasons about all reachable states simultaneously instead               is to find the maximum product of any sublist.” Figure 1 (left)
of individual concrete states. This enables HoarePrompt to oper-               presents a flawed implementation of Kadane’s algorithm to solve
ate statically, without executing the program and without reliance             this problem. The issue lies in incorrect indentation, which results in
on provided failing tests. In comparison with directly prompting               best_so_far being updated only once, after the loop ends, instead
LLMs to analyze programs, HoarePrompt simplifies this task by                  of being updated during each iteration.
decomposing it into small, independent subtasks, which are solved                 Despite the bug’s simplicity, SOTA LLMs struggle to identify it
step-by-step in the spirit of chain-of-thought reasoning [52].                 consistently, and thus often wrongly classify the program as correct.
   Loops pose a fundamental challenge in program analysis and ver-             Providing evidence that an LLM fails to solve a task is inherently
ification because they give rise to infinite execution paths [46]. Our         challenging due to the model’s non-deterministic behavior [41] and
experiments demonstrate that LLMs also struggle to summarize                   its sensitivity to prompt design [44]. To address these challenges,
the semantics of complex loops, producing incorrect natural post-              we made every effort to present objective evidence by crafting six
conditions. To address this problem, we introduce a novel method,              distinct prompts: a straightforward (Vanilla) prompt, a Zero-shot-
few-shot-driven k-induction, synergizing few-shot learning [4] with            CoT prompt [30], an open-ended prompt [1], and combinations of
the idea of k-induction [15] widely used in model checking. This               these strategies, each containing the problem description and the
method starts with iteratively unwinding a loop 𝑘 times to compute             code snippet. For each prompt, we generated 10 responses from
natural postconditions after each iteration. After that, it performs           four different LLMs, employing various temperature settings. More
an induction inference step by prompting an LLM to compute the                 details about the experimental setup and results for this example
postcondition for the entire loop, using the computed natural Hoare            can be found in the supplementary materials (Section A.1).
triples for individual iterations as few-shot examples.                           The results in Table 1 demonstrate that LLMs, using the above six
   To evaluate HoarePrompt, we created CoCoClaNeL, a dataset                   prompts, labelled collectively as “Not Annotated”, detect the bug
of program and natural language requirement pairs, where some                  with only a small probability. An example of an incorrect response
programs meet the requirements and others do not due to human-                 for the Vanilla prompt is presented in Figure 1 on the left.
introduced bugs. All programs and requirements were published                     HoarePrompt addresses this problem as follows. It first extracts
since January 2024, after the training cut-off date of many SOTA               the program’s natural precondition by prompting an LLM to sum-
LLMs to prevent data leakage. We formulated program correct-                   marize the set of valid input values based on the problem description.
ness assessment as a binary classification problem. Our experi-                In this case, the inferred precondition is {xs is a list of integers}.
ments show that HoarePrompt, at the expense of a higher token                  Then, it iteratively queries its natural strongest postcondition (NSP)
use, improves the Matthews Correlation Coefficient (MCC) by 61%                model to propagate reachable state descriptions along the program’s
compared to directly using Zero-shot-CoT prompts. Furthermore,                 control flow graph (CFG). For example, the Hoare Triplet for the
HoarePrompt outperforms a classifier that assesses correctness via             first if statement:
LLM-generated tests by increasing the MCC by 106%. The few-shot-
driven 𝑘-induction mechanism contributes a 26% boost to MCC. We
also show that HoarePrompt improves code generation when used                                {xs is a list of integers}
as a feedback mechanism, outperforming both direct generation                                if (not xs):
(by 19.4%) and test-based feedback (by 12.7%).                                                 return float(’-inf’)
   In summary, the paper makes the following contributions:                                  {xs is a list of integers, and xs is not empty}
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                                 ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




Figure 1: Annotating code with natural language descriptions of reachable program states, which are automatically inferred by
HoarePrompt, enables an LLM to find a bug that is missed by the straightforward Vanilla prompt.

capturing the fact that if an execution reaches the program point                  with Qwen2.5-72B results in an incorrect natural postcondition
after the if statement, the list is guaranteed to be non-empty.                    mistakenly stating the min_diff is the smallest absolute difference
   HoarePrompt continues to propagate the states until it reaches                  between any two consecutive elements in the list.
the end of the program. Loops, which present a particular challenge,                  HoarePrompt unrolls the loop 𝑘 times, with the semantics of each
are handled via inductive reasoning as illustrated in Section 2.2.                 iteration represented by code snippets in “Iteration 1”, ..., “Iteration
   Finally, HoarePrompt annotates the program with the reachable                   k”. Then, it sequentially computes natural strongest postconditions
states at key program points (return statements, after top-level if                for each iteration, using the postcondition of the previous iteration
statements and loops) as presented in Figure 1 on the right. Adding                as the precondition of the next one (the first iteration uses the
such annotations to the six prompts significantly increases LLM’s                  precondition of the entire loop). The resulting triples
success rate of correctness classification as shown in Table 1. This
improvement stems from HoarePrompt ’s compositional reason-                                   {Precondition} Iteration 1 {Postcondition 1},
ing strategy. Since it reasons about individual blocks in isolation,                                          ...
the loop is interpreted based only on its local semantics. In this                        {Postcondition k-1} Iteration k {Postcondition k}
case, HoarePrompt accurately captures that the loop updates only
consider sublists ending at the final element, with the resulting                  are used as few-shot examples to infer the postcondition of the
postcondition annotation enabling better error detection.                          entire loop in “Inductive NSP Prompt (k=3)”. The intuition of this
                                                                                   step is that LLMs generalize from few relevant examples [4], and
2.2     Inductively Reasoning About Loops                                          the examples above are relevant by construction. As shown in
                                                                                   the corresponding LLM response, the enhanced prompt enabled
Reasoning about loops is challenging, because they induce infinite                 the LLM to correctly infer that min_diff is the smallest absolute
behaviours [46], and our experience shows that LLMs also struggle                  difference between any element in the list and the first element.
to summarize them. To alleviate this problem, we take inspiration                     Interestingly, with k=1, the mistake persisted, as the model failed
for the 𝑘-induction technique [15] widely used in model checking,                  to generalize from a single example. Based on our pilot study (Sec-
which first checks that the property holds for all states in the first 𝑘           tion 5.2), we chose 𝑘 = 3 as the best performing configuration.
steps of the program’s execution, and then proves that if a property
holds for any k consecutive steps, then it holds for the next step.                2.3    Expressive Power of Natural Language
   To illustrate our adaptation of 𝑘-induction, which we refer to                  LLMs exhibit limitations in symbolic reasoning due to their reliance
as few-shot-driven 𝑘-induction, consider the program with a loop                   on natural language [48, 56]. Consequently, HoarePrompt avoids
in Figure 2, labelled as “Program”. Assume that its precondition is                formal logical inference, opting instead for natural language as the
given in “Precondition”. Inferring its natural strongest postcondi-                reasoning medium. While this approach does not provide formal
tion (NSP) using the straightforward “Non-Inductive NSP Prompt”                    correctness guarantees, it generates structured informal proofs,
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                      Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev




Figure 2: Few-shot-driven 𝑘-induction unrolls the loop three times, computes the natural strongest postconditions (NSP) for
each iteration sequentially, and uses the resulting natural Hoare triples as few-shot examples for inductively inferring the
postcondition for the entire loop, which enhances precision compared to non-inductive inference, or only a single unrolling.


                                                                              which the precondition Pre holds, provided that the code termi-
                                                                              nates. Pre- and postconditions are predicates over program states,
                                                                              that are typically expressed in first-order logic [17]. Strongest post-
                                                                              condition calculus [14] automates verification using Hoare logic.
                                                                              The strongest postcondition (SP) of a program 𝐶 w.r.t. a precondi-
                                                                              tion Pre, denoted as sp(Pre, 𝐶), is the most precise logical formula
                                                                              describing all possible states reachable after executing 𝐶 from a
                                                                              state satisfying Pre. Formally,
                                                                                           |= {Pre} 𝐶 {Post}       iff sp(Pre, 𝐶) =⇒ Post.

Figure 3: HoarePrompt succinctly describes program behav-                     The following algorithm for computing SP is defined composition-
ior in human-centric terms, which helps align formal seman-                   ally for While [40], a simple programming language that has only
tics with informal requirements.                                              assignments (𝑥 := 𝑒), sequences (𝑆 1 ; 𝑆 2 ), if statements, one loop
                                                                              instruction (while) and a single type (integer):
which, as demonstrated in Section 5, improve the LLMs’ ability to                                sp(Pre, 𝑥 := 𝑒) = Pre[𝑥 ↦→ 𝑒]
effectively align program semantics with informal requirements.                                   sp(Pre, 𝑆 1 ; 𝑆 2 ) = sp(sp(Pre, 𝑆 1 ), 𝑆 2 )
   The method’s effectiveness stems from natural language’s ex-               sp(Pre, if 𝑏 then 𝑆 1 else 𝑆 2 ) = sp(Pre ∧ b, 𝑆 1 ) ∨ sp(Pre ∧ ¬b, 𝑆 2 )
pressivity. In Figure 3, Qwen2.5-72B derives an NSP that succinctly
                                                                                        sp(Pre, while 𝑏 do 𝑆) = (Pre ∧ ¬𝑏) ∨
describes sat in human terms, beyond formal semantics—an ex-                                                           sp(sp(Pre ∧ b, 𝑆), while 𝑏 do 𝑆)
pressivity symbolic logic lacks. Further examples are in Section A.2.
                                                                              The last rule, which handles loops, is recursively defined, making
3     Background                                                              it hard to compute.
Hoare logic [22] is a formalism for reasoning about program cor-                 The 𝑘-induction method [15] applies mathematical-induction
rectness, at the core of which are specifications called Hoare triples        principles to practical loop analysis. Let 𝑃 (𝑠𝑖 ) denote the target
{Pre} 𝐶 {Post}, meaning that the postcondition Post holds in any              property at loop state 𝑠𝑖 after 𝑖 iterations. The method has two
state reachable by executing the code 𝐶 from an initial state in              components: the base case (1), which checks that the property holds
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                                ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




Figure 4: HoarePrompt’s correctness classification workflow.


for the first 𝑘 iterations, and the inductive step (2), which proves
that any window of 𝑘 satisfying iterations implies the next one also
satisfies it:
          −1
         𝑘Û                               −1
                                         𝑘Û
                                                      !
    (1)       𝑃 (𝑠𝑖 )        (2) ∀𝑛 ≥ 0.     𝑃 (𝑠𝑛+𝑖 ) → 𝑃 (𝑠𝑛+𝑘 )
         𝑖=0                                 𝑖=0

4    HoarePrompt
We introduce the natural Hoare triple, a Hoare triple where pre-
                                                                                         Figure 5: Computing NSP for an if-else statement.
and postconditions are expressed in natural language (NL). To dif-
ferentiate natural Hoare triples from traditional Hoare triples, we
highlight sentences from NL with blue:
                                                                                   4.1     Precondition Extraction
                                                                                   HoarePrompt prompts an LLM to extract a precondition from the
                              {Pre} 𝐶 {Post}.                                      given requirements in order to identify the set of valid program
   In analogy with the strongest postcondition calculus, we intro-                 inputs. For example, for the problem description
duce the natural strongest postcondition (NSP). The traditional algo-              “given 𝑁 , write a function that finds the 𝑁 th Fibonacci number”
rithm sp(Pre, 𝐶) cannot be applied in the context of NL. Instead, we
                                                                                   and the function signature def func(num), the LLM produces the
create SP, an LLM-based natural Hoare triple completion model
                                                                                   precondition: {num is a non-negative integer}.
defining a conditional probability distribution
                                                                                   We implement precondition extraction using few-shot learning (see
                         SP (Post | Pre, Stmt).
                                                                                   supplementary materials, Sections B.6 and B.7).
Let J·K : NL → 2𝑆 capture the human interpretation of NL state
descriptions as a mapping from sentences to sets of program states                 4.2     NSP Computation
𝑆. Then, the goal to achieve by SP to ensure plausible reasoning                   In principle, SP can be realized by fine-tuning an LLM to optimize
can be measured using the following objective function:                            the NSP objective function (Theorem 4.1). Due to budget constraints,
                                                                                   we opted instead to adapt an LLM through prompt engineering and
   Definition 4.1 (NSP Objective Function). The objective function
                                                                                   in-context learning. Specifically, we curated a pilot dataset, distinct
for SP is the cross-entropy loss between predicted postconditions
                                                                                   from our evaluation set, and carefully designed prompts and few-
and the traditional strongest postconditions computed over the
                                                                                   shot examples for Python programs by eyeballing the LLM’s output
interpretations of natural language preconditions:
            ∑︁                                                                     on this dataset.
   L =−           I(JPostK ≡ sp(JPreK, 𝐶)) log SP (Post | Pre, 𝐶),                    Simple Statements. Atomic operations such as assignments are
           Post∈NL
                                                                                   processed by directly prompting an LLM to compute the postcondi-
where I(·) is the indicator function.                                              tion. We use a dedicated prompt with few-shot examples, presented
                                                                                   in supplementary materials Section B.8, that tasks the model to infer
   HoarePrompt applies SP to classify program correctness w.r.t.
                                                                                   the updated state based on variable modifications while preserving
natural language requirements using the workflow depicted in
                                                                                   relevant information from the precondition. Apart from that, we
Figure 4. First, it prompts an LLM to extract a precondition (a de-
                                                                                   use dedicated prompts (in supplementary materials Sections B.10
scription of valid program inputs) from the requirements. Second, it
                                                                                   and B.11) to capture effects of return and print commands, since
traverses the program’s control-flow graph (CFG), while sampling
                                                                                   program correctness often depends on them.
natural strongest postconditions from SP, starting from the pre-
condition, for each code segment. Finally, it annotates key program                   Compound Statements. Similar to the traditional sp, SP is de-
points with the inferred reachable state descriptions, and prompts                 fined compositionally, which enables it to precisely reason about
an LLM to check whether the code meets the requirements.                           complex programs by breaking them down into simpler fragments.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                        Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


For example, given a sequence of statements 𝑆 1 ; 𝑆 2 , SP is computed
by first completing natural Hoare triple {Pre}𝑆 1 {Post}, and then its
postcondition Post serves as the precondition for 𝑆 2 . To reduce the
number of LLM queries, we group a configurable number of atomic
statements together using a dedicated prompt (in supplementary
materials Section B.9).
  If Statements. Figure 5 shows how if-else statements are pro-
cessed by HoarePrompt. Given a precondition {Pre} and a statement
if 𝑏 : 𝑆 1 else : 𝑆 2 , it first samples preconditions for the branches:
Preif ∼ SP ( · | Pre, assert 𝑏), Preelse ∼ SP ( · | Pre, assert ¬𝑏)
Then, it samples NSPs for each branch:
      Postif ∼ SP ( · | Preif , 𝑆 1 ), Postelse ∼ SP ( · | Preelse, S2 )
Finally, it uses a dedicated prompt to merge Postif and Postelse into
a single postcondition Post, which will hold after the loop. Prompts             Figure 6: Computing NSP for the call of input() for stdin.
used for these operations are given in supplementary materials
Sections B.14 to B.16.                                                          where 𝑖 ∈ [1, 2, ..., 𝑘], Post0 = Pre, stmtiter is

   Loop Statements. HoarePrompt reasons about loops using our                                            try:
few-shot-driven 𝑘-induction method. For a while statement while 𝑏 :                                        item = next(I_iter)
𝑆 and a precondition Pre, it first samples a precondition for the loop                                     index += 1
body, and a postcondition for the first iterations:                                                      except StopIteration:
                                                                                                           break
  Prewhile ∼ SP ( · | Pre, assert 𝑏), Post1 ∼ SP ( · | Prewhile, 𝑆).
                                                                                where I_iter is an iterator obtained from I and index is initialized
Then, it continues to unwind the loop 𝑘 − 1 times, sequentially                 to 0. For commonly used loops over lists or ranges of elements
computing the following natural pre- and postconditions for each                such as range(0,n), we directly refer to the index of list without
iteration:                                                                      modeling the semantics of next() for simplicity.
    Pre𝑖 ∼ SP ( · | Post𝑖 −1, assert 𝑏), Post𝑖 ∼ SP ( · | Pre𝑖 , 𝑆),               The supplementary materials include our prompts for computing
                                                                                preconditions of the loop body (Sections B.17 and B.19), for handling
where 𝑖 ∈ [2, 3, ..., 𝑘].                                                       while and for loops transitions (Sections B.18 and B.20), and for
  Finally, the NSP for the whole while statement is computed using              inductive inference (Sections B.21 and B.23).
our inductive prompt that includes the natural Hoare triples
                       n                    o                                       Exceptions Handling. Given Pre, and a try-except statement
                         {Pre𝑖 } 𝑆 {Post𝑖 }
                                                  𝑖 ∈ [1,2,...,𝑘 ]                      try : 𝛼 except 𝐸 1 : 𝛽 1 except 𝐸 2 : 𝛽 2, . . . except 𝐸𝑚 : 𝛽𝑚 ,
as few-shot examples. This process is illustrated in Figure 2 for a             we first sample the NSP for the try-block:
for statement, which is handled accordingly.
   Many programming languages allow iterations over a collection,                                        Posttry ∼ SP ( · | Pre, 𝛼),
e.g., the for loop in Python. The challenge of handling such itera-              and then the NSPs for different exception handling blocks:
tion constructs is that they are implemented using implicit iterators,
which store internal states updated at each iteration. Since iterators                Posti ∼ SP ( · | “variables may take arbitrary values", 𝛽𝑖 ).
are not explicit variables, LLM tends to not include them when                     Finally, we merge Posttry, Post1, Post2, . . . , Postm using a prompt
producing NSPs. Therefore, when dealing with iterators, we also                  provided in the supplementary materials (Section B.12). Note that,
explicitly model the state of the iterator.                                      due to the complexity of handling nonlinear control flow, the NSP
   Our modeling of Python’s iterators involves maintaining the                   computation for exception handling blocks does not inherit any
index of the next element of the iterator, which increments by 1 with            preconditions here, assuming that the state may be arbitrary.
each call to next(). Our natural language descriptions of program
                                                                                    Input Stream. Figure 6 shows how data from the standard in-
states refer to elements from the iterator as “the {index}th elements
                                                                                 put (stdin) is processed by HoarePrompt. When programs read
of the iterator”, where “{index}” represents our modeled index, and
                                                                                 from stdin, the precondition extraction explicitly describes the
the description of the iterator itself is always accompanied with
                                                                                 expected structure and content of the stdin based on the given
the description of the current index representing its state. If an
                                                                                 problem description. So, the precondition would clearly indicate
iterator is used across loops, its index also needs to be summarized
                                                                                 that stdin contains these inputs in that specific order. Every time
via k-induction together with other parts of the state.
                                                                                 a postcondition for a statement reading stdin is sampled as
   For a loop for item in I, to accurately reflect the additional
changes of both the iterator and the index for at the start of each                                Post ∼ SP ( · | Pre, x = input()),
iteration, the precondition for the i-th iteration is sampled as:                the description of the stream state in Post will be updated accord-
                        Pre𝑖 ∼ SP ( · | Post𝑖 , stmtiter ),                      ingly. After all data is read, the state of the stream is described
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                                ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


as “stdin is empty”. Note that this modeling applies only to non-                  Table 2: Effect of unroll bound 𝑘 on MCC and token usage
interactive programs, where stdin is predetermined and does not                    (normalized over 𝑘=0).
depend on the execution of the program.
                                                                                             Unroll Bound 𝑘       MCC         Token Increase
4.3     Correctness Classification                                                           0 (no unroll)        0.211              1.00×
Let 𝑅 be the natural language requirement, 𝑃 be the program to                               1                    0.228              3.02×
be evaluated, 𝐷 = {(𝑅1, 𝑃1, 𝑦1 ), (𝑅2, 𝑃2, 𝑦2 ), . . . , (𝑅𝑛 , 𝑃𝑛 , 𝑦𝑛 )} be a               3                    0.262              11.29×
labeled dataset, where 𝑦𝑖 ∈ {Correct, Incorrect} represents whether                          5                    0.231              24.53×
program 𝑃𝑖 satisfies requirement 𝑅𝑖 . The problem of classifying
correctness w.r.t. natural language requirements can be formalized
as the task of learning a function 𝑓 : (𝑅, 𝑃) → {Correct, Incorrect}.
   In this work, we investigate several classification functions based             adopted the Matthews Correlation Coefficient (MCC) as it considers
on NSP, as well as alternative ideas.                                              all four components of the confusion matrix, and produces more
   HoarePrompt: Given 𝑅 and 𝑃, HoarePrompt first annotates key                     reliable statistical results than F1 score [9]. Further information on
program points with descriptions of reachable states computed                      MCC is available in supplementary materials (Appendix A.8.) We
using SP. Specifically, it adds annotations as comments after top-                 also report other standard metrics such as Balanced Accuracy, True
level if and loop statements. Apart from that, it adds descriptions                Positive Rate (TPR), False Negative Rate (FNR), and False Positive
of returned and printed values after return and print statements, as               Rate (FPR). To ensure robustness against LLM non-determinism,
these values are often used to assess correctness. An example of an                we repeated each experiment multiple times. Following best prac-
annotation program is given in Figure 1. The annotated program                     tices [41, 54], we calibrated the rerun count based on model confi-
is passed alongside 𝑅 to an LLM via our classification prompt. The                 dence and consistency. This yielded 3 reruns per experiment. Details
supplementary materials contain the classification prompts for                     of this derivation are included in supplementary materials (Appen-
single- and multi-function programs (Sections B.4 and B.5).                        dix A.4). All experiments were conducted in a virtual machine with
   HoarePrompt (No Unroll): We also implemented a variant                          a AMD EPYC 7543 64-bit CPU, two cores and 16GB of RAM.
of HoarePrompt that employs a non-compositional approach to
computing the NSP for loops by prompting an LLM to infer the post-                 5.1    CoCoClaNeL Dataset
condition of the entire loop directly within a single LLM query. The               Although there exist numerous datasets of natural language re-
prompts applied in this approach are given in the supplementary                    quirements [2, 21], some including incorrect implementations [49],
materials (Sections B.22 and B.24).                                                we could not use most of them due to potential data leakage, since
   Vanilla: Given 𝑅 and 𝑃, it directly asks an LLM to classify                     memorization of correct solutions will significantly impact LLM
program correctness using the prompt given in Section B.2.                         reasoning [13, 53]. Apart from that, we required non-trivial re-
   Zero-shot-CoT: Our Zero-shot-CoT [30] prompt extends the                        quirements and subtle bugs to thoroughly evaluate the ability of
Vanilla by triggering chain-of-thought reasoning [52] by adding                    LLMs to reason about program correctness. We constructed a bench-
the “think step-by-step” instruction (Section B.1).                                mark CoCoClaNeL (Code Correctness Classification w.r.t. Natural
   Tester: As an alternative to static reasoning, we also employed                 Language requirements). It consists of 645 problem-solution pairs
testing for classifying program correctness. Specifically, this method             from Codeforces programming contests that took place in the first
first generates tests based on 𝑅 with an LLM using the testing                     half of 2024, with solutions labelled as correct or incorrect by the
prompt adapted from AgentCoder [24], executes 𝑃 on the generated                   Codeforces’ internal testing system. Totally, 322 of the solutions
tests, and classifies it as correct iff it passes the tests.                       (49.9%) are incorrect. All problems and solutions are released since
                                                                                   January 2024, after the cut-off data of many SOTA LLMs, and the
5     Evaluation                                                                   problems are challenging, have unambiguous descriptions, and
Our experiments address these research questions:                                  solutions to these problems are rigorously tested to find subtle
RQ1: How does the classification performance of HoarePrompt                        bugs [25]. To capture subtle and challenging coding errors, we
  compare to other techniques?                                                     specifically included incorrect submissions that immediately pre-
RQ2: How does few-shot-driven 𝑘-induction impact HoarePrompt’s                     ceded correct ones, hypothesizing that these would likely contain
  effectiveness?                                                                   nuanced mistakes. Further details about the dataset are provided in
RQ3: How does the LLM token use of HoarePrompt compare to                          supplementary materials (Section A.3).
  other techniques?
RQ4: How effective is HoarePrompt as a feedback mechanism in a                     5.2    Hyperparameters
  downstream code generation task?                                                 We tuned the unrolling bound 𝑘 ∈ {0, 1, 3, 5} using Llama3.1-70B
   We selected four representative open-weight LLMs. Three come                    on a 140-entry pilot set randomly sampled from the same source
from the Qwen [19] family: Qwen2.5-7B-Instruct, a popular smaller                  as CoCoClaNeL, but disjoint from the 645 CoCoClaNeL programs.
model, Qwen2.5-Coder-32B-Instruct, a model specialized for cod-                    As shown in Table 2, 𝑘=3 achieves the best MCC (0.262), balanc-
ing tasks, and Qwen2.5-72B-Instruct, demonstrating performance                     ing generalization and token cost. Higher 𝑘 increase token usage
comparable to GPT-4o-mini [47]. Another one is from the Llama                      while degrading the quality. Notably, no matter the choice of 𝑘
family: Llama3.1-70b-Instruct. To measure classification quality, we               HoarePrompt outperforms the baseline classifiers by at least 23.7%.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                        Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


Table 3: Performance of classifiers of program correctness w.r.t. natural language requirements and their token use across four
LLMs evaluated on CoCoClaNeL. HoarePrompt significantly improves the MCC in comparison with baselines at the expense of
a higher token use. HoarePrompt without loop unrolling represents a trade-off between classification quality and token cost.

                                                            Correctness Classification Quality Metrics                          Tokens (Millions)
      Model             Classifier
                                                      MCC       ΔMCC      BA        TPR     FNR      FPR                     IT       OT         TT
                        Vanilla                       0.055               0.521     0.193   0.807    0.151                   1.8       0.8        2.6
                        Zero-shot-CoT                 0.085    +54.5%     0.543     0.563   0.437    0.478                   2.1       1.3        3.4
  Qwen2.5-7B            Tester                        0.109    +98.18%    0.519     0.051   0.949    0.012                   1.7       3.8        5.5
                        HoarePrompt                   0.159    +189.1%    0.577     0.700   0.300    0.546               205.1 (93.9) 31.9 237.1 (125.9)
                        HoarePrompt no unroll         0.119    +116.36% 0.558       0.666   0.334    0.550               19.9 (12.3)   3.4    23.4 (15.7)
                        Vanilla                       0.137               0.553     0.233   0.767    0.128                   1.9       0.9        2.8
                        Zero-shot-CoT                 0.123    -10.22%    0.560     0.438   0.562    0.318                   2.4       1.5        3.9
    Qwen2.5-
                        Tester                        0.096    -29.93%    0.518     0.055   0.945    0.019                   1.9       3.3        5.2
    Coder-32B
                        HoarePrompt                   0.231    +68.61%    0.616     0.593   0.407    0.362               186.5 (88.2) 42.6 229.1 (130.8)
                        HoarePrompt no unroll         0.158    +15.04%    0.579     0.571   0.429    0.412               19.2 (11.6)   4.4    23.6 (15.9)
                        Vanilla                       0.169               0.578     0.382   0.618    0.226                   1.7       0.9        2.6
                        Zero-shot-CoT                 0.193    +14.20%    0.593     0.714   0.286    0.527                   2.0       1.3        3.2
  Qwen2.5-72B           Tester                        0.131    -22.49%    0.522     0.052   0.948    0.007                   1.9       3.8        5.6
                        HoarePrompt                   0.259    +53.25%    0.629     0.667   0.333    0.409               163.5 (78.7) 32.5 196.0 (111.2)
                        HoarePrompt no unroll         0.231    +36.69%    0.615     0.618   0.382    0.387               19.3 (11.8)   3.8    23.1 (15.6)
                        Vanilla                       0.161               0.579     0.671   0.329    0.513                   1.7      0.01        1.7
                        Zero-shot-CoT                 0.157    -2.48%     0.575     0.728   0.329    0.514                   1.8       0.7        2.5
  Llama3.1-70b          Tester                        0.099    -38.51%    0.527     0.109   0.891    0.055                   1.7       2.4        4.1
                        HoarePrompt                   0.250    +55.28%    0.601     0.895   0.105    0.692              144.3 (106.8) 27.3 171.6 (134.1)
                        HoarePrompt no unroll         0.209    +29.81%    0.588     0.858   0.142    0.681                12.0 (9.5)   1.7    13.7 (11.2)
Abbreviations: MCC = Matthews Correlation Coefficient, ΔMCC: Relative MCC Improvement over Vanilla , BA = Balanced Accuracy, TPR = True
Positive Rate, FNR = False Negative Rate, FPR = False Positive Rate, IT = Input Tokens, OT = Output Tokens, TT = Total Tokens. Parentheses in
IT and TT for HoarePrompt classifiers indicate token counts excluding few-shot learning examples, which can be eliminated via fine-tuning.


   Another key design choice is how many and which annota-                         Similar improvement is observed across other classification met-
tions to include in the final prompt. We mark only major pro-                   rics. HoarePrompt’s TPR is 15.5% higher than Zero-shot-COT and
gram points—after loops, branches, returns, prints, and try-catch               107.1% higher than Vanilla. HoarePrompt also reduces the FNR
blocks—to reduce prompt size while maintaining clarity. In pilots,              compared to Zero-shot-COT and Vanilla, The FPR for HoarePrompt
full-state annotation improved MCC over Zero-shot-CoT by 19.7%,                 (0.502), is also just slightly higher than Zero-shot-COT (0.459) but
whereas our sparse strategy achieved 62%. We hypothesize that                   significantly higher than Vanilla (0.254).
excessive detail dilutes focus, while key transitions aid reasoning.               HoarePrompt also significantly outperforms the Tester classi-
                                                                                fier, increasing MCC by 106% on average. Notably, Tester achieves
5.3      RQ1: Classification Performance                                        a very low average TPR of only 6.7%, indicating frequent misclassi-
In the first research question, we examine whether structural rea-              fications of correct programs. This issue stems from test generation
soning with descriptions of reachable states helps HoarePrompt                  inaccuracies: LLMs often fail to produce correct output oracles,
improve LLMs’ ability to evaluate program correctness compared                  leading to false negatives. Table 4 shows the breakdown of Tester
to other techniques. By systematically tracking program states                  behavior. On average, each program was evaluated with 13–28 test
through HoarePrompt, we hypothesize that structured reasoning                   cases, but 15–25% of examples had no passing test cases, and only
will enhance correctness classification.                                        3–8% had no failing test. Thus, the program was marked incorrect in
   Table 3 shows the results for each model. In comparison with                 over 90% of cases, including the vast majority of correct programs,
LLM-based baselines, Vanilla and Zero-shot-CoT, HoarePrompt                     due to at least one failing test case. This affected all model sizes,
consistently demonstrated higher classification quality. On average,            showcasing a limitation of test-based correctness classification. A
HoarePrompt improves the MCC by 61% over Zero-shot-COT and                      qualitative analysis of the misclassifications of HoarePrompt and
72% over Vanilla. The impact of HoarePrompt is most pronounced                  Tester are presented in Section 5.7.
in smaller models. The most significant improvement of MCC is in
Qwen2.5-7B, being 87% over Zero-shot-COT and 189% over Vanilla.
For Qwen2.5-72B, MCC improves by 34% and 53% over the Zero-                       RQ1: HoarePrompt consistently outperforms the baselines in
shot-CoT and Vanilla respectively. The results of the Llama model                 terms of classification quality across all LLMs, achieving an
follow similar trends to those exhibited by the Qwen2.5 models,                   average improvement of 61% in MCC over Zero-shot-COT, 72%
being especially close to Qwen2.5-72b, which is of a similar size.                over Vanilla and 106% over Tester.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                                 ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 4: Tester statistics across four LLMs. “Avg. Total” and                      Table 5: Code generation results on 100 problems from CoCo-
“Avg. Passed” — the average number of generated/passed tests                       ClaNeL. Correct%: percentage of programs passing all hidden
per program. “0 Pass %” and “0 Fail %” — the percentage of                         tests; ATP: average fraction of test cases passed.
programs for which all tests failed or all tests passed.
                                                                                                             Llama3.1                       GPT-4.1
                                                                                      Method
Model               Avg. Total       Avg. Passed       0 Pass %      0 Fail %                           Correct%         ATP         Correct%          ATP
Qwen2.5-7B              27.81             9.99           23.17%        3.32%          HoarePrompt          33%         57.98%            47%          69.55%
Qwen2.5-32B             17.30             7.86           15.14%        3.63%          Testing              29%         54.89%            42%          69.53%
Qwen2.5-72B             17.47             6.50           16.90%        3.13%          Baseline             30%         56.34%            37%          62.03%
LLaMA3.1-70B            12.72             5.02           25.34%        8.19%

5.4     RQ2: Impact of Inductive Reasoning                                            A key reason for the increased token usage is our inductive
Loops introduce complexity for reasoning about programs. Hoare-                    reasoning algorithm (few-shot-driven 𝑘-induction) that performs
Prompt mitigates this complexity by inductively reasoning about                    loop unrolling. On average, it requires 10.9 times extra tokens (8.6
loops using our novel few-shot-driven k-induction technique. This                  times extra when excluding non-essential tokens) than the non-
technique involves unrolling loops k times, with 𝑘 = 3 in our ex-                  inductive variant. Thus, the few-shot k-induction is more suitable
periments, before generalizing the final state.                                    for situations when classification accuracy is prioritized over cost.
   This question investigates whether loop unrolling enhances cor-                 The non-inductive version, HoarePrompt no unroll, represents a
rectness classification quality. To measure the impact of our few-                 practical trade-off by retaining a substantial performance boost
shot-driven k-induction algorithm, we compare HoarePrompt’s                        (27.8% better than the top performing approach, Zero-shot-COT)
classification performance with that of HoarePrompt (no unroll)                    while consuming 90% fewer tokens than full unrolling. Overall,
that summarizes loops within a single step.                                        it consumes only 6.4 times more tokens (4.5 times more, when
   As shown in Table 3, the few-shot-driven 𝑘-induction technique                  excluding non-essential tokens) than Zero-shot-COT.
provides significant additional performance gains, improving the
MCC by an average of 25.7% over the non-inductive version (Hoare-                   RQ3: HoarePrompt’s significant performance boost comes at
Prompt no unroll). Specifically, it improves MCC by 33.6% in Qwen2.5-               the expense of an average token usage increase of 64 times (39
7B, 45.3% in Qwen2.5-Coder-32B, 12.1% in Qwen2.5-32B and 19.6%                      times when excluding non-essential tokens that can be elimi-
for LLama3.1-70b. Even without unrolling, HoarePrompt demon-                        nated via fine-tuning) compared to the most accurate baseline,
strates the second-best result among the studied classifiers.                       Zero-shot-COT. The version of HoarePrompt without unrolling
                                                                                    represents a practical trade-off between classification quality
 RQ2: Few-shot-driven k-induction enhances classification per-                      and cost, demonstrating the second-best performance, while
 formance across all models, improving the MCC by an average                        consuming 90% fewer tokens than the main variant.
 of 25.7% over the non-inductive version of HoarePrompt.
                                                                                   5.6    RQ4: Code generation
5.5     RQ3: Token Usage                                                           To assess HoarePrompt as a feedback mechanism in the context
Since HoarePrompt involves multiple LLM queries, it consumes                       of code generation, we adapted the AgentCoder [24] pipeline and
more tokens than direct LLM prompts [35]. We quantified this                       implemented two variants: one using test-based feedback (as in the
increase and investigated the trade-off between token use and clas-                original), and one replacing test failures with correctness judgments
sification quality. Table 3 provides the total token usage across                  from HoarePrompt. The third baseline generates a final solution
classifiers and models for the 645 problem-solution pairs of the                   in a single step without refinement. We evaluated all three meth-
CoCoClaNeL. For each classifier, we measured the input tokens                      ods on 100 problems randomly sampled from CoCoClaNeL. We
(IT), the output tokens (OT), and total tokens (TT). As explained                  excluded problems with multiple valid outputs — cases where dif-
in Section 4.2, we chose to implement our natural strongest post-                  ferent programs produce acceptable but non-identical outputs —
condition computation using prompt engineering with few-shot                       since correctness becomes ambiguous and not reliably testable [42].
learning examples due to budget constraints. Tokens representing                      For our main experiments, we used Llama3.1-70b-instruct.
these hard-coded examples are repeatedly sent to an LLM during                     Due to the complexity of CoCoClaNeL and to evaluate generaliza-
the algorithm iterations; in principle, they can be eliminated via                 tion on more capable models, we additionally employed the stronger
fine-tuning. Because of that, for the HoarePrompt variants, we also                GPT-4.1 model. Results for both models are shown in Table 5.
report the number of “essential” input and total token, in parenthe-                  With Llama3.1-70B, the testing-based variant occasionally re-
ses, that excludes hard-coded few-shot example tokens.                             gressed due to incorrect oracles, reducing both fully correct pro-
   On average, HoarePrompt consumes 85.9 times more tokens than                    grams and test pass rates compared to the baseline. In contrast,
Vanilla (51 times when excluding non-essential tokens), 64.1 times                 HoarePrompt consistently improved both metrics, highlighting its
more tokens than Zero-shot-CoT (38.6 times more when excluding                     robustness. The supplementary materials include a regression ex-
non-essential tokens), and 40.8 times more tokens than Tester (24.6                ample (Section A.6) and HoarePrompt’s improvement (Section A.7).
times more, when excluding non-essential tokens).                                  With the stronger GPT-4.1, the test-based variant improves over
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                      Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


the baseline — suggesting that test-driven refinement benefits from           ambiguities, which are typically not present in programming com-
stronger models. However, HoarePrompt still outperforms both,                 petition problems. Techniques like ClarifyGPT [36] that detects
achieving the highest correct rate (47%) and best ATP (69.55%).               ambiguities in informal requirements may address this concern.
                                                                                 We evaluated HoarePrompt across models of diverse sizes (7B to
    RQ4: HoarePrompt is effective as a feedback mechanism for iter-           72B) from 2 families (Qwen, Llama), including Qwen-32B-Coder, a
    ative code generation, increasing the number of solved problems           model specialized for coding tasks. This broad spectrum enhances
    by 12–14% compared to using generated tests as feedback.                  generalizability; however, different LLM architectures may yield
                                                                              varying results. Nevertheless, observed trends suggest broad appli-
                                                                              cability, especially relevant given industry shifts toward proprietary
5.7      Qualitative Error Analysis                                           small and mid-sized models [7]. Evaluating HoarePrompt on larger
We manually audited misclassifications to understand failure modes            and more powerful models may help assess its scalability and effec-
of HoarePrompt and Tester. First for HoarePrompt:                             tiveness in leveraging more advanced reasoning capabilities.
• Missing Edge Case: The NSP chain omits critical boundary
   conditions, leading to overly optimistic judgments.                         7    Related Work
• Oversimplified Annotations: Annotations blur fine-grained
   state differences, producing misleading correctness cues.                  HoarePrompt introduces a new paradigm for reasoning about pro-
• Incorrect Loop Generalization: Loop effects are overgeneral-                grams in NL. Its contributions are relevant to works on reasoning
   ized, resulting in faulty postconditions.                                  about code with LLMs, LLM-assisted testing and verification.
• Semantic Trust Bias: When code structure resembles the de-                     Reasoning About Code with LLMs. Many generic approaches have
   scription, the LLM sometimes ignores contradictory annotations             been introduced to realize effective chain-of-though (CoT) reason-
   and falsely assumes correctness.                                           ing [52]. We employed Zero-shot-CoT [30], a popular automation
• Interprocedural Failures: Reasoning errors occur across func-               of CoT, as a baseline in our experiments. CJ-Eval [60] uses LLMs
   tion boundaries, corrupting inference consistency.                         as judges of program correctness applying an approach equivalent
• Variable Scope or Shadowing Errors: In loop-heavy code,                     to our baseline Vanilla prompt (Section 4.3). Since CJ-Eval is based
   reused indices or scope bleed distort postconditions.                      on a widely-used Apps dataset [21], which is subject to data leak-
• Description–Code Misalignment (rare): For correct programs                  age, we constructed a new dataset CoCoClaNeL. A large body of
   using alternative logic patterns (e.g., DP vs. greedy), annotations        work focused on reasoning about concrete execution states. Zhang
   fail to reflect intent.                                                    et al. [59] fine-tuned LLMs with concrete execution states to im-
and for Tester, false negatives fell in four categories:                      prove their ability to track execution faithfully. Similarly, NExT [38]
• Misread semantics (19%): misunderstood IO relation.                         enhances debugging using programs annotated with concrete exe-
• Output computation failure (58%): logic is described correctly              cution traces. CodeMind [34] includes a “specification reasoning”
   but numerical results are wrong.                                           task that measures how including test data in the specification
• Multiple valid answers (21%): tests assert one of several correct           helps the model generate correct code. REval [6] evaluates run-
   outputs (Section A.5).                                                     time behaviour reasoning capabilities, specifically, consistency in
• Insufficient coverage (2%): corner cases not tested.                        intermediate state prediction by analyzing variable states at spe-
   In Figure 7, the program (a greedy method with a suffix array)             cific execution points. The key difference of HoarePrompt is that it
is correct. Vanilla misreads the role of min(a[i],b[i]); Tester               reasons about not individual executions but, potentially, infinitely
predicts an incorrect output—consistent with findings that LLMs               many executions, without relying of specific inputs.
struggle to directly compute nontrivial results [18]. HoarePrompt ’s             LLM-Assisted Formal Verification. Recent works on LLM-assisted
annotations make the purpose of c explicit (per-position minimum              verification focused on translating natural language specifications
cost), enabling the correct verdict.                                          into formal ones, and rely on external theorem provers or SMT
                                                                              solvers [16]. Marmaragan [11] synthesizes formal Ada/SPARK con-
                                                                              tracts from natural language. Similarly, SynVer [37] biases LLM-
6     Threats of Validity                                                     generated C code towards verifiability by producing assertions
LLMs are inherently nondeterministic [41], leading to varied re-              and invariants, subsequently verified by Coq or Verified Software
sponses. To address this, we employed multiple reruns per sample              Toolchain (VST). LLMLIFT [3] integrates LLMs into verified compi-
with confidence-based sampling to ensure robust performance es-               lation, generating proof sketches alongside code translation, with
timates. Although further reruns could slightly refine our results,           formal verification performed via SMT solvers. Stanford et al. [29]
the current methodology provides high-confidence evaluations.                 introduce Proof-Carrying Code Completions (PC3), prompting
   Main threats to external validity are that the selected dataset may        LLMs to produce Dafny [31] programs accompanied by machine-
not generalize to other programs, or that performance enhance-                checkable correctness proofs, automating verification through Dafny.
ments will not generalize to other LLMs. To avoid data leakage,               While these approaches embed formal verification into LLM-driven
we constructed a new dataset from recent Codeforces competi-                  code generation pipelines, they fundamentally rely on external
tion problems, ensuring challenging, human-authored, and varied               verification systems such as Dafny, Coq [51], or Z3 [12]. Despite
submissions. Despite efforts to minimize biases, future studies on            the promise of these methods, they have shown limited scalability,
alternative datasets could further validate generalizability and per-         with Marmaragan achieving only 50.7% correctness in its generated
formance trends. Apart from that, real-world requirements contain             Ada/SPARK contracts [11] and Endres et al. [16] reporting that
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                               ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




Figure 7: A CoCoClaNeL problem with a correct solution. Vanilla misclassifies by misreading the algorithm; Tester fails by
predicting wrong outputs; HoarePrompt ’s state annotations enable a correct judgment.

even with optimized prompting, only 77% of LLM-generated post-                     such as LiveCodeBench [26], CodeElo [42], ProBench [57], and
conditions were verifiable. HoarePrompt employs an alternative                     USACO-based evaluations [45], mitigate leakage by incorporating
approach of constructing structured informal proofs in natural lan-                recent programming competition problems. However, they primar-
guage, leveraging its expressive power and flexibility, for classifying            ily assess code generation capabilities and do not provide solu-
program correctness. Following previous work [27] such informal                    tion submissions with correctness labels. In contrast, CoCoClaNeL
proofs might be translated into formal ones to automate formal                     specifically targets correctness classification by offering labeled
verification. Closest to our loop reasoning technique, Liu et al. [33]             problem-solution pairs sourced from Codeforces 2024 contests, en-
propose LLM-SE, which combines symbolic execution with LLMs                        abling evaluation of LLMs on their execution-state reasoning capa-
to generate loop invariants for memory-manipulating programs.                      bilities rather than memorization or test-based validation alone.
While HoarePrompt does not target formal invariant synthesis,                      8   Conclusion
instead focusing in textual inductive reasoning. Although Hoare-                   This work introduces HoarePrompt, the first LLM-based program
Prompt does not provide formal guarantees, prior work shows that                   analysis approach to assess program correctness against natural lan-
formal proofs mirror informal reasoning [27], suggesting Hoare-                    guage requirements. Unlike traditional verification and testing that
Prompt could serve as a foundation for automated verification.                     depend on external tools or concrete test executions, HoarePrompt
Integrating HoarePrompt with techniques like symbolic CoT [56]                     systematically applies natural language-based structural reasoning
may further enhance reasoning and provide guarantees. A promis-                    inspired by the strongest postcondition calculus and k-induction.
ing future direction is to develop a hybrid (formal and natural)                   Our evaluation shows significant performance improvements in
language to promote more grounding of the LLM’s output.                            classification quality, with HoarePrompt increasing the MCC by
   LLM-Based Automated Test Generation Recent works [8, 32, 43, 58]                61% over Zero-shot-CoT, 72% over Vanilla, and 106% over an LLM
have employed LLMs for automated test generation. Apart from                       testing-based classifier. Our novel k-induction further enhances per-
that, the analysis of LLM-generated test outcomes has been used to                 formance, yielding an average MCC improvement of 26% compared
facilitate program synthesis tasks [55], exemplified by CODET [5],                 to a non-inductive approach. Although HoarePrompt consumes
AgentCoder [24], CodeCoT [23], and CoCoST [20]. Section 5 shows                    more tokens, the no-unroll variant provides a practical trade-off,
that using LLM-generated tests for correctness classification, em-                 achieving a 28% MCC improvement over Zero-shot-CoT while using
bodied in our Tester baseline adopting AgentCoder’s approach [24],                 90% fewer tokens than the standard HoarePrompt version.
suffers from high false negative rate, as LLMs fail to infer precise
assertions for complex requirements. Ideas of HoarePrompt could                    Acknowledgments
be synergized with testing to improve accuracy and cost.
  Competition-Level Benchmarks Recent studies reveal significant                   This work was sponsored by the National Key Research and Devel-
data leakage in widely used LLM benchmarks, inflating model per-                   opment Program of China under Grant No. 2022YFB4501902 and
formance due to test-training overlaps [13, 39]. New benchmarks,                   the National Natural Science Foundation of China (NSFC) under
                                                                                   Grant No. W2411051.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                          Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


References                                                                                         [22] Charles Antony Richard Hoare. 1969. An axiomatic basis for computer program-
 [1] Simran Arora, Avanika Narayan, Mayee F Chen, Laurel Orr, Neel Guha, Kush                           ming. Commun. ACM 12, 10 (1969), 576–580.
     Bhatia, Ines Chami, Frederic Sala, and Christopher Ré. 2022. Ask me anything: A               [23] Dong Huang, Qingwen Bu, Yuhao Qing, and Heming Cui. 2023. Codecot: Tack-
     simple strategy for prompting language models. arXiv preprint arXiv:2210.02441                     ling code syntax errors in cot reasoning for code generation. arXiv preprint
     (2022).                                                                                            arXiv:2308.08784 (2023).
 [2] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk                              [24] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming
     Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le,                         Cui. 2023. Agentcoder: Multi-agent-based code generation with iterative testing
     and Charles Sutton. 2021. Program Synthesis with Large Language Models. arXiv                      and optimisation. arXiv preprint arXiv:2312.13010 (2023).
     preprint arXiv:2108.07732 (2021).                                                             [25] Yiming Huang, Zhenghao Lin, Xiao Liu, Yeyun Gong, Shuai Lu, Fangyu Lei, Yaobo
 [3] Sahil Bhatia, Jie Qiu, Niranjan Hasabnis, Sanjit A. Seshia, and Alvin Cheung.                      Liang, Yelong Shen, Chen Lin, Nan Duan, and Weizhu Chen. 2024. Competition-
     2024. Verified Code Transpilation with LLMs. arXiv:2406.03003 [cs.PL] https:                       Level Problems are Effective LLM Evaluators. In Findings of the Association for
     //arxiv.org/abs/2406.03003                                                                         Computational Linguistics: ACL 2024. Association for Computational Linguistics,
 [4] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan,                             Bangkok, Thailand, 13526–13544. https://doi.org/10.18653/v1/2024.findings-
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda                         acl.803
     Askell, et al. 2020. Language models are few-shot learners. Advances in neural                [26] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang,
     information processing systems 33 (2020), 1877–1901.                                               Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. 2024. Live-
 [5] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou,                        CodeBench: Holistic and Contamination Free Evaluation of Large Language
     and Weizhu Chen. 2022. Codet: Code generation with generated tests. arXiv                          Models for Code. arXiv:2403.07974 [cs.SE] https://arxiv.org/abs/2403.07974
     preprint arXiv:2207.10397 (2022).                                                             [27] Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja
 [6] Junkai Chen, Zhiyuan Pan, Xing Hu, Zhenhao Li, Ge Li, and Xin Xia. 2024.                           Jamnik, Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. 2022. Draft, sketch,
     Reasoning Runtime Behavior of a Program with LLM: How Far Are We?                                  and prove: Guiding formal theorem provers with informal proofs. arXiv preprint
     arXiv:2403.16437 [cs.SE] https://arxiv.org/abs/2403.16437                                          arXiv:2210.12283 (2022).
 [7] Lihu Chen and Gaël Varoquaux. 2024. What is the role of small models in the                   [28] Nan Jiang, Xiaopeng Li, Shiqi Wang, Qiang Zhou, Soneya Hossain, Baishakhi Ray,
     llm era: A survey. arXiv preprint arXiv:2409.06857 (2024).                                         Varun Kumar, Xiaofei Ma, and Anoop Deoras. 2024. LeDex: Training LLMs to
 [8] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, and Jianwei                         Better Self-Debug and Explain Code. Advances in Neural Information Processing
     Yin. 2024. Chatunitest: A framework for llm-based test generation. In Compan-                      Systems 37 (2024), 35517–35543.
     ion Proceedings of the 32nd ACM International Conference on the Foundations of                [29] Parnian Kamran, Premkumar Devanbu, and Caleb Stanford. 2024. Vision Paper:
     Software Engineering. 572–576.                                                                     Proof-Carrying Code Completions. In Proceedings of the 39th IEEE/ACM Inter-
 [9] Davide Chicco and Giuseppe Jurman. 2023. The Matthews correlation coefficient                      national Conference on Automated Software Engineering Workshops (Sacramento,
     (MCC) should replace the ROC AUC as the standard metric for assessing binary                       CA, USA) (ASEW ’24). Association for Computing Machinery, New York, NY,
     classification. BioData Mining 16, 1 (2023), 4. https://doi.org/10.1186/s13040-                    USA, 35–42. https://doi.org/10.1145/3691621.3694932
     023-00322-4                                                                                   [30] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke
[10] Patrick Cousot and Radhia Cousot. 1977. Abstract interpretation: a unified                         Iwasawa. 2022. Large language models are zero-shot reasoners. Advances in
     lattice model for static analysis of programs by construction or approximation                     neural information processing systems 35 (2022), 22199–22213.
     of fixpoints. In Proceedings of the 4th ACM SIGACT-SIGPLAN symposium on                       [31] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional
     Principles of programming languages. 238–252.                                                      Correctness. In Logic for Programming, Artificial Intelligence, and Reasoning,
[11] Marcos Cramer and Lucian McIntyre. 2025. Verifying LLM-Generated Code in                           Edmund M. Clarke and Andrei Voronkov (Eds.). Springer Berlin Heidelberg,
     the Context of Software Verification with Ada/SPARK. arXiv:2502.07728 [cs.SE]                      Berlin, Heidelberg, 348–370.
     https://arxiv.org/abs/2502.07728                                                              [32] Kefan Li and Yuan Yuan. 2024. Large language models as test case generators:
[12] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver.                          Performance evaluation and enhancement. arXiv preprint arXiv:2404.13340 (2024).
     In Proceedings of the 14th International Conference on Tools and Algorithms for               [33] Chang Liu, Xiwei Wu, Yuan Feng, Qinxiang Cao, and Junchi Yan. 2024. Towards
     the Construction and Analysis of Systems (TACAS). Springer, 337–340. https:                        General Loop Invariant Generation: A Benchmark of Programs with Memory
     //doi.org/10.1007/978-3-540-78800-3_24                                                             Manipulation. arXiv:2311.10483 [cs.PL] https://arxiv.org/abs/2311.10483
[13] Chunyuan Deng, Yilun Zhao, Yuzhao Heng, Yitong Li, Jiannan Cao, Xian-                         [34] Changshu Liu, Shizhuo Dylan Zhang, Ali Reza Ibrahimzada, and Reyhaneh
     gru Tang, and Arman Cohan. 2024. Unveiling the Spectrum of Data Con-                               Jabbarvand. 2024. Codemind: A framework to challenge large language models
     tamination in Language Model: A Survey from Detection to Remediation. In                           for code reasoning. arXiv preprint arXiv:2402.09664 (2024).
     Findings of the Association for Computational Linguistics: ACL 2024. Associa-                 [35] Tongxuan Liu, Xingyu Wang, Weizhe Huang, Wenjiang Xu, Yuting Zeng, Lei
     tion for Computational Linguistics, Bangkok, Thailand, 16078–16092. https:                         Jiang, Hailong Yang, and Jing Li. 2024. Groupdebate: Enhancing the efficiency
     //doi.org/10.18653/v1/2024.findings-acl.951                                                        of multi-agent debate using group discussion. arXiv preprint arXiv:2409.14051
[14] Edsger Wybe Dijkstra, Edsger Wybe Dijkstra, Edsger Wybe Dijkstra, Etats-Unis                       (2024).
     Informaticien, and Edsger Wybe Dijkstra. 1976. A discipline of programming.                   [36] Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, Chenxue Wang,
     Vol. 613924118. prentice-hall Englewood Cliffs.                                                    Shichao Liu, and Qing Wang. 2023. Clarifygpt: Empowering llm-based code
[15] Alastair F Donaldson, Leopold Haller, Daniel Kroening, and Philipp Rümmer.                         generation with intention clarification. arXiv preprint arXiv:2310.10996 (2023).
     2011. Software verification using k-induction. In Static Analysis: 18th International         [37] Prasita Mukherjee and Benjamin Delaware. 2024. Towards Automated Ver-
     Symposium, SAS 2011. Springer, 351–368.                                                            ification of LLM-Synthesized C Programs. arXiv:2410.14835 [cs.PL] https:
[16] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K Lahiri.                        //arxiv.org/abs/2410.14835
     2024. Can large language models transform natural language intent into formal                 [38] Ansong Ni, Miltiadis Allamanis, Arman Cohan, Yinlin Deng, Kensen Shi, Charles
     method postconditions? Proceedings of the ACM on Software Engineering 1, FSE                       Sutton, and Pengcheng Yin. 2024. Next: Teaching large language models to reason
     (2024), 1889–1912.                                                                                 about code execution. arXiv preprint arXiv:2404.14662 (2024).
[17] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3—where programs                     [39] Shiwen Ni, Xiangtao Kong, Chengming Li, Xiping Hu, Ruifeng Xu, Jia Zhu,
     meet provers. In Programming Languages and Systems: 22nd European Symposium                        and Min Yang. 2025. Training on the Benchmark Is Not All You Need.
     on Programming, ESOP 2013, Held as Part of the European Joint Conferences on                       arXiv:2409.01790 [cs.CL] https://arxiv.org/abs/2409.01790
     Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013.                  [40] Flemming Nielson, Hanne R Nielson, and Chris Hankin. 2015. Principles of
     Proceedings 22. Springer, 125–128.                                                                 program analysis. springer.
[18] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang,                       [41] Shuyin Ouyang, Jie M Zhang, Mark Harman, and Meng Wang. 2025. An empirical
     Jamie Callan, and Graham Neubig. 2023. Pal: Program-aided language models. In                      study of the non-determinism of chatgpt in code generation. ACM Transactions
     International Conference on Machine Learning. PMLR, 10764–10799.                                   on Software Engineering and Methodology 34, 2 (2025), 1–28.
[19] Alibaba Group. 2024. Qwen2.5: Advancing Open-Source Large Language Models.                    [42] Shanghaoran Quan, Jiaxi Yang, Bowen Yu, Bo Zheng, Dayiheng Liu, An Yang, Xu-
     https://qwenlm.github.io/blog/qwen2.5-llm/?utm_source=chatgpt.com                                  ancheng Ren, Bofei Gao, Yibo Miao, Yunlong Feng, Zekun Wang, Jian Yang,
[20] Xinyi He, Jiaru Zou, Yun Lin, Mengyu Zhou, Shi Han, Zejian Yuan, and Dong-                         Zeyu Cui, Yang Fan, Yichang Zhang, Binyuan Hui, and Junyang Lin. 2025.
     mei Zhang. 2024. CoCoST: Automatic Complex Code Generation with Online                             CodeElo: Benchmarking Competition-level Code Generation of LLMs with
     Searching and Correctness Testing. arXiv preprint arXiv:2403.13583 (2024).                         Human-comparable Elo Ratings. arXiv:2501.01257 [cs.CL] https://arxiv.org/abs/
[21] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora,                         2501.01257
     Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Stein-                [43] Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip. 2023. An empirical
     hardt. 2021. Measuring Coding Challenge Competence with APPS. In Advances in                       evaluation of using large language models for automated unit test generation.
     Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track.                     IEEE Transactions on Software Engineering 50, 1 (2023), 85–105.
                                                                                                   [44] Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr. 2023. Quantify-
                                                                                                        ing Language Models’ Sensitivity to Spurious Features in Prompt Design or:
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


     How I learned to start worrying about prompt formatting. arXiv preprint
     arXiv:2310.11324 (2023).
[45] Quan Shi, Michael Tang, Karthik Narasimhan, and Shunyu Yao. 2024. Can
     Language Models Solve Olympiad Programming? arXiv:2404.10952 [cs.CL]
[46] Xujie Si, Hanjun Dai, Mukund Raghothaman, Mayur Naik, and Le Song. 2018.
     Learning loop invariants for program verification. Advances in Neural Information
     Processing Systems 31 (2018).
[47] LLM Stats. 2024. GPT-4o-mini 2024-07-18 vs Qwen2 72B Instruct. https://llm-
     stats.com/models/compare/gpt-4o-mini-2024-07-18-vs-qwen2-72b-instruct Ac-
     cessed: 2025-03-14.
[48] Rob Sullivan and Nelly Elsayed. 2024. Can Large Language Models Act as
     Symbolic Reasoners? arXiv:2410.21490 [cs.CL] https://arxiv.org/abs/2410.21490
[49] Shin Hwei Tan, Jooyong Yi, Sergey Mechtaev, Abhik Roychoudhury, et al. 2017.
     Codeflaws: a programming competition benchmark for evaluating automated
     program repair tools. In 2017 IEEE/ACM 39th International Conference on Software
     Engineering Companion (ICSE-C). IEEE, 180–182.
[50] Codeforces Team. 2019. Codeforces: Problem Difficulties. https://codeforces.com/
     blog/entry/62865
[51] The Coq Development Team. 2024. The Coq Reference Manual – Release 8.19.0.
     https://coq.inria.fr/doc/V8.19.0/refman.
[52] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,
     Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning
     in large language models. Advances in Neural Information Processing Systems 35
     (2022), 24824–24837.
[53] Chulin Xie, Yangsibo Huang, Chiyuan Zhang, Da Yu, Xinyun Chen, Bill Yuchen
     Lin, Bo Li, Badih Ghazi, and Ravi Kumar. 2024. On memorization of large language
     models in logical reasoning. arXiv preprint arXiv:2410.23123 (2024).
[54] Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan
     Hooi. 2024. Can LLMs Express Their Uncertainty? An Empirical Evaluation of
     Confidence Elicitation in LLMs. arXiv:2306.13063 [cs.CL] https://arxiv.org/abs/
     2306.13063
[55] Weimin Xiong, Yiwen Guo, and Hao Chen. 2023. The program testing ability of
     large language models for code. arXiv preprint arXiv:2310.05727 (2023).
[56] Jundong Xu, Hao Fei, Liangming Pan, Qian Liu, Mong-Li Lee, and Wynne Hsu.
     2024. Faithful logical reasoning via symbolic chain-of-thought. arXiv preprint
     arXiv:2405.18357 (2024).
[57] Lei Yang, Renren Jin, Ling Shi, Jianxiang Peng, Yue Chen, and Deyi Xiong. 2025.
     ProBench: Benchmarking Large Language Models in Competitive Programming.
     arXiv:2502.20868 [cs.CL] https://arxiv.org/abs/2502.20868
[58] Zhiqiang Yuan, Yiling Lou, Mingwei Liu, Shiji Ding, Kaixin Wang, Yixuan Chen,
     and Xin Peng. 2023. No more manual tests? evaluating and improving chatgpt
     for unit test generation. arXiv preprint arXiv:2305.04207 (2023).
[59] David W. Zhang, Michaël Defferrard, Corrado Rainone, and Roland Memise-
     vic. 2025. Grounding code understanding in step-by-step execution. https:
     //openreview.net/forum?id=MUr7Fl93QS
[60] Yuwei Zhao, Ziyang Luo, Yuchen Tian, Hongzhan Lin, Weixiang Yan, Annan Li,
     and Jing Ma. 2024. CodeJudge-Eval: Can Large Language Models be Good Judges
     in Code Understanding? arXiv preprint arXiv:2408.10718 (2024).
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                        Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


A     Supplementary Materials
All code, documentation, results and complimentary material for
this work is available in our repository: https://github.com/msv-
lab/HoarePrompt.

A.1      Details of Motivating Example
For evaluating the motivating example presented in Section 2.1, we
ran a series of experiments using three different qwen2.5-instruct
models (7b, coder-32b, 72b) and one Llama model                                           Figure 8: Example 2 - Unique Email Domains
(Llama3.1-70b-instruct) at three temperatures (0.5, 1.0, 1.5).
For each temperature, we tested:
  • Not Annotated: 6 different prompts with no reachable state
    annotations.
  • Annotated: 6 different prompts that included reachable state
    descriptions.
Each model/prompt combination was run 10 times, for a total of
1080 calls across all setups. Table 6 shows the success rates (the                         Figure 9: Example 3 - First name extraction
percentage of calls that correctly identified the code as buggy).

Table 6: Success rates (%) for detecting the indentation bug
under different prompts (“Not Annotated” vs. “Annotated”),
temperatures, and models. Each cell shows successful runs /
total runs (percentage).

                              Temperature = 0.5
    Model                                Not Annotated     Annotated
    7b-instruct                              0/60 (0%)     7/60 (11.7%)
    coder-32b-instruct                      9/60 (15%)      51/60 (85%)
    72b-instruct                            21/60 (35%)     51/60 (85%)
    llama3.1-70b-instruct                   30/60 (50%)    60/60 (100%)
                              Temperature = 1.0
    Model                                Not Annotated     Annotated             Figure 10: The Frequency Histogram of Rating for CoCo-
                                                                                 ClaNeL with x-axis representing the rating intervals of the
    7b-instruct                              0/60 (0%)      2/60 (3.3%)
                                                                                 problems and y-axis representing the number of problem-
    coder-32b-instruct                      9/60 (15%)     50/60 (83.3%)
                                                                                 code pairs within each rating interval in the dataset.
    72b-instruct                           29/60 (48.3%)   49/60 (81.7%)
    llama3.1-70b-instruct                   30/60 (50%)    60/60 (100%)
                                                                                precision by utilizing variable names and structure to improve rea-
                              Temperature = 1.5                                 soning. While it does not provide formal correctness guarantees, it
    Model                                Not Annotated     Annotated            acts as a practical fuzzy correctness classifier, making it useful for
                                                                                tasks like bug detection and code generation.
    7b-instruct                             4/60 (6.7%)     5/60 (8.3%)            In Figures 8,9 we present two more examples to complement
    coder-32b-instruct                      7/60 (11.7%)    51/60 (85%)         that in Section 2.3. These examples illustrate how an LLM can con-
    72b-instruct                           31/60 (51.7%)    42/60 (70%)         cisely infer express program states by leveraging natural language.
    llama3.1-70b-instruct                   40/60 (67%)    60/60 (100%)         We believe this ability of LLM to succinctly capture program be-
                                                                                havior using user-centric terms helps HoarePrompt to accurately
                                                                                classify program correctness by bridging the gap between program
A.2      Natural Language and LLMs for State                                    semantics and informal requirements.
         Tracking
We explore the effectiveness of Qwen2.5-72B-Instruct in inferring                A.3      Dataset Details
the final state (postcondition) of a program segment by leveraging              To better illustrate the difficulty of problems in CoCoClaNeL, we
semantic context and real-world knowledge. Unlike formal verifi-                use the rating tags for problems provided by Codeforces as an
cation methods that rely on explicit rules and symbolic execution,              indicator. Initially, rating was solely an indicator of user rankings on
Qwen2.5-72B-Instruct can generate intuitive and human-readable                  programming competition platforms. Subsequently, to better assist
explanations of code behavior. This approach enhances analysis                  users in selecting appropriate problems for practice, Codeforces
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                                ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


began assigning each problem a rating to represent its difficulty,                 A.4     Rerun Strategy and Variance Control
which is determined by the solving statistics of participants for                  To ensure statistical reliability given LLM response variability,
this problem [50]. Formally, a problem’s rating 𝑥 quantifies that                  we computed the number of reruns required to achieve a high-
participants with a rating of 𝑥 have a 50% probability of solving it               confidence estimate with low error. Our approach follows the frame-
on their first encounter.                                                          work of Ouyang et al. [41] and the confidence-weighted aggregation
   Rating for problems ranges from 800 to 3500 and serves as a dif-                method of Xiong et al. [54].
ficulty coefficient indicator, where a higher rating indicates greater
problem difficulty. During the problem collection process, we also                   Confidence Estimation. Given a binary prediction (Correct or
gathered the ratings of each problem and present the rating distri-                Incorrect), the LLM assigns a log-probability log 𝑃 (𝑌 ), which is con-
bution of our dataset. As shown in Figure 10, our dataset has an                   verted to confidence via exp(log 𝑃 (𝑌 )). We aggregate confidences
average rating of 1206. According to the statistics and evaluations                across 𝑀 reruns using the Avg-Conf method:
from CodeElo[42], a problem with a rating of 1206 indicates that                                                  Í𝑀
                                                                                                                       I(𝑌𝑖 = 𝑌 ) · 𝐶𝑖
approximately 60% of all participants on Codeforces find it chal-                                     𝐶 avg-conf = 𝑖=1 Í𝑀
lenging (with less than a 50% probability of solving it on their first                                                   𝑖=1 𝐶𝑖
encounter), and only 2 of the 33 tested LLMs achieved a higher
                                                                                   where 𝑌𝑖 is the 𝑖-th response, 𝐶𝑖 its confidence score, and I(𝑌𝑖 = 𝑌 )
rating than 1206, which is difficult for LLMs to simply retrieve.
                                                                                   is an indicator for agreement with the majority response.
   Additionally, as can be seen from the figure, the data presents a
skewed distribution of "higher on the left and lower on the right".                   Rerun Count Calculation. Let 𝑃 be the estimated consistency of
The frequency in low rating intervals (such as 800–1000) is signifi-               the LLM across reruns, 𝑋 the number of evaluation instances, and
cantly higher, and as the rating increases, the frequency generally                𝑅 the number of reruns. We aim to bound the margin of error 𝜖 for
shows a downward trend. The main reason is that as the difficulty                  a desired confidence level 𝐶, modeled with a binomial distribution:
of the problem increases (the rise in rating), the number of people                              √︂
who solve this problem (or even the number of people who attempt                                    𝑃 (1 − 𝑃)                     𝑍 2 𝑃 (1 − 𝑃)
                                                                                           𝜖 =𝑍               , 𝑁 = 𝑅 · 𝑋, 𝑅 =
to solve it) decreases. Therefore, there are fewer submission records                                   𝑁                             𝑋 · 𝜖2
available for sampling, and even fewer submission records that                     where 𝑍 is the critical value for the desired confidence level (e.g.,
meet our sampling strategy.                                                        𝑍 = 2.33 for 98%).
   The scraped problems were originally in raw HTML format. We
parsed out all the useful content w.r.t. the problem and converted it                Final Parameters. Using:
into Markdown format (to be consistent with our prompt), which                      • Dataset size: 𝑋 = 645,
may include the problem description, input format, output format,                   • Observed average confidence: 𝐶 = 0.963,
examples, notes, and so on, to ensure the sufficiency of the problem                • Desired confidence level: 98% (𝑍 = 2.33),
information and details.                                                            • Error margin: 𝜖 = 0.01,
   For a problem, we filtered out all its Python submissions. The
specific strategy for selecting submissions is as follows:                         we compute 𝑅 ≈ 3, meaning all experiments are repeated three
                                                                                   times to achieve statistically reliable results.
  • Include three consecutive incorrect/correct code pairs (each
    pair comes from the same user). If there are less than three,
    include all that are available. If the problem has not been solved             A.5     Example: Tester Misclassification due to
    by anyone, skip it.                                                                    multiple correct solutions
  • If available, include one code with a test passed rate of 50% (or              This example from our dataset CoCoClaNeL, as seen on Figure
    close to 50% due to an odd number of test cases), and one code                 11, highlights a common limitation of the LLM-generated tester.
    with only a single failing test case.                                          Specifically, it shows how problems with multiple valid outputs can
   Furthermore, we provide a detailed comparison in Table 7 of our                 lead the tester to incorrectly reject a correct implementation.
CoCoClaNeL dataset to two prominent datasets: LiveCodeBench [26]
and APPS [21], based on key metrics such as solution complexity,                   A.6    Example : Impact of Incorrect Test Cases on
code length, loop depth, and description verbosity.                                       LLM-Driven Code Refinement based on
                                                                                          Agent Coder
  Dataset         LOC LD        DL   CC HD         HV
                                                                                   In our experiments with Llama3.1, we observed a striking exam-
  CoCoClaNeL       25.1 1.29 2156.83 7.77 28.8 1063.2
                                                                                   ple of how incorrect test cases can mislead LLM-based program
  LiveCodeBench 9.95 1.01 42.35 4.18 21.81 416.2
                                                                                   synthesis or correction systems, resulting in previously correct
  APPS            24.03 1.29 1416.06 7.63 34.12 1103.6
                                                                                   implementations being erroneously altered.
Table 7: Comparison of dataset complexity based on Lines
of Code (LOC), Loop Depth (LD), Description Length (DL),                             Context. The underlying programming problem involves a little
Cyclomatic Complexity (CC), Halstead Difficulty (HD), and                          boy, Nikita, who builds a tower using cubes. The process follows
Halstead Volume (HV). Higher CC, HD, and HV values indi-                           two simple rules:
cate more complex programs.                                                         • In each of 𝑛 moves, Nikita must either add exactly one cube on
                                                                                      top of the tower or remove exactly one cube from the top.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                     Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


                                                                                  • Input: 5 0, Expected Output: Yes
Figure 11: Example of problem with multiple correct solu-                    which contradict the problem’s constraints: for example, with 1
tions                                                                        0, it is impossible to end with 0 cubes after a single move since
                                                                             removing a cube is invalid on an empty tower.
                              Problem Description
                                                                                 Misguided Corrections. The faulty test cases were executed on the
                    Given integer 𝑥 , find any 𝑦 (1 ≤ 𝑦 < 𝑥 ) such
                    that                                                      original correct implementation, resulting in output mismatches. In-
                                   gcd(𝑥, 𝑦) + 𝑦                              terpreting these mismatches as genuine errors, the LLM attempted
                    is maximized.                                             to fix the code to satisfy the flawed expectations—introducing ad-
                    Multiple 𝑦 may be equally valid.
                                                                              hoc conditions that deviated from the correct logic:
                         Tester Generated Test Case                           if (n - m) % 2 == 0 or ((n - m) % 2 == 1 and m != 0):
                    Input:
                                                                                  return "Yes"
                    1                                                        which breaks the parity logic and admits invalid solutions, thereby
                    10                                                       turning correct code into incorrect code.
                    Output:
                    5
                                                                              A.7      Example: HoarePrompt-Guided Correction
                             gcd(10, 5) = 5 5 + 5 = 10                                 for Code Generation based on Agent Coder
                    Tester selected 𝑦 = 5 as the solution.
                                                                                 Context. Count all pairs ⟨𝑖, 𝑗⟩ in an array 𝑎 so that
                              Tester Classification                                  𝑎𝑖 + 𝑎 𝑗 ≡ 0     (mod 𝑥)      and 𝑎𝑖 − 𝑎 𝑗 ≡ 0        (mod 𝑦).
                    Incorrect                                                    Faulty Implementation.
                    Our implementation produced:
                    9                                                         for num in a:
                                                                                  rx = num % x
                             gcd(10, 9) = 1, 1 + 9 = 10                           ry = num % y
                                                                                  remainder = (rx + ry) % y
                    Also optimal, but tester flagged as incorrect
                    due to strict expected match.
                                                                                  complement = ((x - rx) % x + ry) % y
                                                                                  beautiful_pairs += cnt[complement]
                                                                                  cnt[remainder] += 1
  • The tower starts with 0 cubes, and it is never allowed to have
    a negative height—removing a cube from an empty tower is                    HoarePrompt Annotation. HoarePromptwith Llama3.1,highlights
    invalid.                                                                  the line
   Given this setup, the task is to determine whether it is possible,               remainder = (rx + ry) % y
after exactly 𝑛 moves, to end up with a tower that has exactly 𝑚             with the note the remainder is the remainder of the sum of num
cubes.                                                                       divided by x plus the remainder of num divided by y, divided by y
   Two simple conditions fully characterize the problem:
  • 𝑚 ≤ 𝑛, since each move changes the height by at most 1.                     Feedback. “The program contains a bug. This bug stems from
  • (𝑛 − 𝑚) is even, ensuring moves can be paired into balanced               merging num mod 𝑥 and num mod 𝑦 into one mod 𝑦 expression, drop-
    “add and remove” operations to reach exactly 𝑚.                           ping the independent mod𝑥 check.”
Thus, the tower ends with 𝑚 cubes after 𝑛 moves if and only if:                  Corrected Implementation.
             possible ⇐⇒ (𝑚 ≤ 𝑛 ∧ (𝑛 − 𝑚) mod 2 = 0)                          cnt = defaultdict(int)
                                                                              for num in a:
The LLM produced an implementation which faithfully reflects this
                                                                                  r_x = num % x
reasoning:
                                                                                  r_y = num % y
def solve(n, m):                                                                  need_x = (-r_x) % x
     if m > n:                                                                    beautiful_pairs += cnt[(need_x, r_y)]
         return "No"                                                              cnt[(r_x, r_y)] += 1
     if (n - m) % 2 == 0:
                                                                             Here each element is bucketed by the pair (𝑟 𝑥 , 𝑟 𝑦 ), so “sum ≡ 0 mod
         return "Yes"
                                                                             x” and “difference ≡ 0 mod y” are enforced independently.
     else:
         return "No"
                                                                              A.8      MCC Calculation and Justification
   Faulty Test Cases. LLaMA3.1-70B generated test cases that the             To evaluate the quality of binary correctness classification, we adopt
expected output was incorrectly calculated by the model and they             the Matthews Correlation Coefficient (MCC) as our primary
were subsequently used as feedback to refine the code.Two such               metric. Given the confusion matrix entries—true positives (TP), true
test cases are:                                                              negatives (TN), false positives (FP), and false negatives (FN)—the
     • Input: 1 0, Expected Output: Yes                                      MCC is computed as:
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language   ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




                              (TP × TN) − (FP × FN)
        MCC = √︁
                    (TP + FP)(TP + FN)(TN + FP)(TN + FN)
   The MCC yields a score in [−1, 1], where:
  • 1 indicates perfect prediction,
  • 0 indicates random prediction,
  • −1 indicates total disagreement.
   We chose MCC over commonly used alternatives such as ROC
AUC or accuracy because MCC takes into account all four con-
fusion matrix categories, and it remains informative even under
class imbalance. This makes it particularly suitable for correctness
classification, where false negatives (missing bugs) and false posi-
tives (flagging correct code as incorrect) are both costly. As shown
by Chicco and Jurman [9], ROC AUC can yield misleadingly high
scores even for classifiers with low precision or poor practical per-
formance. Moreover, ROC AUC considers performance over all
thresholds, not the concrete operating point used for binary deci-
sions. In contrast, MCC directly reflects classifier behavior at the
applied threshold and ensures high values only when sensitivity,
specificity, precision, and NPV are all high. Therefore, we follow
their recommendation that MCC should replace ROC AUC as the
standard metric in binary classification settings [9], especially in
sensitive domains like program verification, where balanced cor-
rectness evaluation is critical.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                     Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B     LLM Prompts
In this section of the Appendix, we include all prompts provided to the LLMs during the evaluation and experiments in our study. Where FSL
was employed, the FSL examples are also included.




B.1      Zero-Shot Chain-of-Thought (CoT) Prompt

      Your task is to determine if a given Python program is correct based on the provided problem description. Assume valid inputs as
            described in the problem description.

      First, explain your reasoning step by step, then reply with:
      - Correctness: `True` if the given program is correct.
      - Correctness: `False` if the given program is incorrect.


      Problem:
      {decription}

      Program:
      {code}

      # Your response:
      Reasoning:
      Correctness: **True** or **False**




B.2      Vanilla Prompt (No Chain-of-Thought)

      Your task is to determine if a given Python program is correct based on the provided problem description. Assume valid inputs as
            described in the problem description.

      Reply with:
      - Correctness: `True` if the given program is correct.
      - Correctness: `False` if the given program is incorrect.


      Problem:
      {description}

      Program:
      {code}

      # Your response:
      Correctness: **True** or **False**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.3      Prompt for Input-Output Test Case Generation

      **Role**: As a tester, your task is to create comprehensive test cases for the following coding problem. These test cases should
            encompass Basic and Edge scenarios to ensure the code's robustness, reliability, and scalability.

      **Problem Description**:
      {description}

      **1. Basic Test Cases**:
      - **Objective**: To verify the fundamental functionality of the `has_close_elements` function under normal conditions.

      **2. Edge Test Cases**:
      - **Objective**: To evaluate the function's behavior under extreme or unusual conditions.

      **Instructions**:
      - Implement a comprehensive set of test cases following the guidelines above.
      - Ensure each test case is complete (no omission) and well-documented with comments explaining the scenario it covers.
      - Pay special attention to edge cases as they often reveal hidden bugs.
      - Do not repeat, do not summarize.

      All test cases you give need to strictly follow the problem description and format like this:

      # Test 1
      **Input**:
      ```

      ```
      **Output**:
      ```

      ```




B.4      HoarePrompt Correctness Classification Prompt

      Your task is to determine if a given Python program is correct based on the problem description and the execution states of the program
             provided as comments. Assume valid inputs as described in the problem description.

      First, explain your reasoning, then reply with:
      - Correctness: `True` if the given program is correct.
      - Correctness: `False` if the given program is incorrect.


      **# Problem:**
      {description}

      **# Annotated Program:**
      {annotated_program}

      **# Your response:**
      Reasoning:
      Correctness: **True** or **False**
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                     Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.5      HoarePrompt Correctness Classification for Multi-Function Programs

      Your task is to determine if a given Python program is correct based on the problem description and the execution states of the program
             provided as comments. Assume valid inputs as described in the problem. The program is made of multiple functions and the program
             is **correct** only if all its functions together meet the problem description.

      First, explain your reasoning, then reply with:
      - Correctness: `True` if the given program is correct.
      - Correctness: `False` if the given program is incorrect.


      **# Problem:**
      {description}

      **# Annotated Functions:**
      {functions}

      **# Your response:**
      Reasoning:
      Correctness: **True** or **False**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.6      Precondition Extraction Prompt

      You are given a programming problem description and a function definition for a function that solves this problem. From the problem
            description, extract a description of the values of the program's input variables and the relationships between these variables.
            We refer to this description as the **precondition**. Print the precondition following the word **"Precondition"**, and surround
            it with double asterisks (**). Follow these examples:

      ### Example 1
      **Problem description:** Write a function to find the minimum cost path to reach (m, n) from (0, 0) for the given cost matrix cost[][]
            and a position (m, n) in cost[][].
      **Function definition:**
      ```python
      def min_cost(cost, m, n):
      ```
      **Precondition:** **cost is a 2D list of non-negative integers, m and n are non-negative integers such that 0 <= m < len(cost) and 0 <=
             n < len(cost[0]).**

      ### Example 2
      **Problem description:** Write a function to find the similar elements from the given two tuple lists.
      **Function definition:**
      ```python
      def similar_elements(test_tup1, test_tup2):
      ```
      **Precondition:** **test_tup1 and test_tup2 are tuples.**

      ### Example 3
      **Problem description:** Write a Python function to identify non-prime numbers.
      **Function definition:**
      ```python
      def is_not_prime(n):
      ```
      **Precondition:** **n is an integer greater than 1.**

      ### Example 4
      **Problem description:** Write a function to find the largest integers from a given list of numbers using the heap queue algorithm.
      **Function definition:**
      ```python
      def heap_queue_largest(nums, n):
      ```
      **Precondition:** **nums is a list of integers, and n is a non-negative integer such that 0 <= n <= len(nums).**

      ### Example 5
      **Problem description:** Write a function to find the number of ways to fill it with 2 x 1 dominoes for the given 3 x n board.
      **Function definition:**
      ```python
      def count_ways(n):
      ```
      **Precondition:** **n is a non-negative integer.**

      ### Example 6
      **Problem description:** Find the average of the positive integers in a list.
      **Function definition:**
      ```python
      def func_1(numbers):
      ```
      **Precondition:** **numbers is a list of integers.**

      ### **Your Task**

      **Problem description:**
      {description}

      **Function definition:**
      ```python
      {program}
      ```
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                     Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.7         Precondition Extraction Prompt for Multi-Function Programs

      You are given a programming problem description and a function that contributes to the solution of this problem. The total solution
            comprises multiple functions, and this is just one of them.
      From the problem description, and based on the variables used in the signature of this specific function, extract a description of the
            values of the variables in the function signature and the relationship between them. We refer to this description as the **
            precondition**. Print the precondition following the word **Precondition**, and surround it with double asterisks (**). Follow
            these examples:
      Remember, the function given may not solve the problem directly but may perform a side functionality that contributes to the total
            solution. Include information only about the variables in the function signature.

      ---

      ### Example 1
      **Problem description:** Write a function to find the minimum cost path to reach (m, n) from (0, 0) for the given cost matrix cost[][]
            and a position (m, n) in cost[][].
      **Program:**
      ```python
      def min_cost(cost, m, n):
          tc = [[0 for x in range(C)] for x in range(R)]
          tc[0][0] = cost[0][0]
          for i in range(1, m+1):
              tc[i][0] = tc[i-1][0] + cost[i][0]
          for j in range(1, n+1):
              tc[0][j] = tc[0][j-1] + cost[0][j]
          for i in range(1, m+1):
              for j in range(1, n+1):
                  tc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + cost[i][j]
          return tc[m][n]
      ```
      **Precondition:** **cost is a 2D list of non-negative integers, m and n are non-negative integers such that 0 <= m < len(cost) and 0 <=
             n < len(cost[0]).**

      ---

      ### Example 2
      **Problem description:** Write a function to find the similar elements from the given two tuple lists.
      **Program:**
      ```python
      def are_similar(elem, elem1):
          if elem == elem1:
              return True
          else:
              return False
      ```
      **Precondition:** **elem1 and elem are values of any type and value.**

      ---

      ### Example 3
      **Problem description:** Write a Python function to identify if 2 consecutive integers in a list are not prime.
      **Program:**
      ```python
      import math
      def is_not_prime(n):
          result = False
          for i in range(2, int(math.sqrt(n)) + 1):
              if n % i == 0:
                  result = True
          return result
      ```
      **Precondition:** **n is an integer greater than 1.**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




     ### Example 4
     **Problem description:** Write a function to find the largest integers from a given list of numbers using the heap queue algorithm.
     **Program:**
     ```python
     import heapq as hq
     def heap_queue_largest(nums, n):
         largest_nums = hq.nlargest(n, nums)
         return largest_nums
     ```
     **Precondition:** **nums is a list of integers, and n is a non-negative integer such that 0 <= n <= len(nums).**

     ---

     ### **Your Task**

     **Problem description:**
     {description}

     **Program:**
     ```python
     {program}
     ```
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                      Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.8         Simple Statement Execution Prompt

      You have been assigned the role of a program executor, responsible for simulating the execution of Python code. You will be provided
            with an initial state and a Python code snippet. You need to provide the output state after running the Python code based on the
            initial state. Please avoid describing how the program runs. When a variable has a specific value, use that specific value
            directly for calculations. If a return takes place, make sure to always mention that a value or variable has been returned in the
             output state. You must adhere to the text format: **Output State: `output state`**.

      Include all the information of the precondition that is still valid after the code has been executed. Just update the values of the
            variables that have been changed by the code.

      I am giving you some examples to understand the task better. Then I am giving you your task.

      ---

      ### Example 1
      **Initial State:** `str` is a string
      ```python
      n = int(input())
      ```
      **Output State:** **`str` is a string, `n` is an input integer**

      ---

      ### Example 2
      **Initial State:** Variables can hold any values
      ```python
      i += 1
      ```
      **Output State:** **variable `i` is increased by 1**

      ---

      ### Example 3
      **Initial State:** `n` is either 3 or 5
      ```python
      m = n + 1
      ```
      **Output State:** **`n` is either 3 or 5; `m` is either 4 or 6**

      ---

      ### Example 4
      **Initial State:** `x` is a positive integer; if `x` is greater than 10, then `z = 0`, else `z = 1`.
      ```python
      y = -z
      ```
      **Output State:** **`x` is a positive integer, if `x` is greater than 10 then `z=0` and `y=0`, else `z=1` and `y=-1`**

      ---

      ### Example 5
      **Initial State:** `total` is 0, `i` is 1
      ```python
      break
      ```
      **Output State:** **`total` is 0, `i` is 1 and we break out of the most internal loop or if statement.**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




     ### Example 6
     **Initial State:** `total` is positive, `num` is negative, `x` is 0
     ```python
     x = total - num
     ```
     **Output State:** **`total` is positive, `num` is negative, `x` is a positive value equal to `total - num`.**

     ### **Your Task**

     **Initial State:**
     {pre}

     ```python
     {program}
     ```
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                     Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.9         Compound Simple Statements Execution Prompt

      You have been assigned the role of a program executor, responsible for simulating the execution of Python code. You will be provided
            with an initial state and a Python code snippet consisting of multiple lines. Your task is to execute all the lines in sequence
            and provide the output state after the entire code block has been run. Avoid describing how the program runs step-by-step for
            individual lines but instead focus on the combined effect of all lines. When a variable has a specific value, use that specific
            value directly for calculations.

      Include all the information from the precondition that remains valid after the code execution and update the values of any variables
            that are modified by the code. Provide the final state, including the state of all the variables after the execution of the code
            snippet. Use the text format: **Output State: `output state`**.

      Here are some examples to help you understand the task:

      ---

      ### Example 1
      **Initial State:** `a` is 5, `b` is 3
      ```python
      c = a + b
      d = c * 2
      ```
      **Output State:** **a is 5, b is 3, c is 8, d is 16**

      ---

      ### Example 2
      **Initial State:** `x` is a positive integer
      ```python
      n = int(input())
      x += n
      ```
      **Output State:** **x is a positive integer equal to its original value plus `n`, `n` is an integer**

      ---

      ### Example 3
      **Initial State:** `n` is 3, `total` is 1
      ```python
      total += n
      pass
      n = max(total, n)
      ```
      **Output State:** **n is 4, total is 4**

      ---

      ### **Your Task**

      **Initial State:**
      {pre}

      ```python
      {program}
      ```

      Now, please analyze the entire block of code and provide the final output state. List the impact of all lines on the program, check the
             previous values of affected variables, and calculate the states of the variables after the code executes. Be as specific as
            possible, combining changes from all lines into a single coherent final state. Include all valid information from the
            precondition and update only what is modified by the code.

      In your response, strictly use the format: **Output State: `the output state you calculate`.**, and describe this output state in
            natural language easily understandable by humans.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.10       Print Commands Execution Prompt

     You will be given an **initial state** (precondition) and a **Python code snippet** containing a `print` statement. Your task is to **
           determine exactly what will be printed** when the statement executes.

     - If a variable or object has a known **explicit value**, use that value in the output.
     - If a variable or object is defined by a **formula or condition**, describe its value using the given information.
     - Always provide the most **precise** description possible based on the precondition.
     - Format the final output as: **Output: `what is printed`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ---

     ### Example 1
     **Initial State:** `arr` is a list containing 1, 2, 3, 4, 5, and `sum` is the sum of all elements in the list `arr`.
     ```python
     print(arr[2], sum)
     ```
     **Output:** **3, sum (where sum is the sum of all elements in list `arr`)**

     ---

     ### Example 2
     **Initial State:** The `points` list is a list of points. The `shoelace_sum` is the sum of all terms calculated as \(x_1 * y_2 - y_1 *
           x_2\) for each consecutive pair of points in the `points` list. The `area` is the absolute value of `shoelace_sum` divided by 2.0.
            `i` is equal to `len(points) - 2`, and `x1` is the first element of `points[i]`, `y1` is the second element of `points[i]`,
           while `x2` is the first element of `points[i + 1]`, and `y2` is the second element of `points[i + 1]`.
     ```python
     print(area)
     ```
     **Output:** **area (where area is the area of the polygon formed by the points in the `points` list)**

     ---

     ### Example 3
     **Initial State:** `balances` is a list of integers, `A` is the first element of the `balances` list, `B` is the second element of the
           `balances` list, and `amount` is an integer less than or equal to `A`.
     ```python
     print(f"The amount {amount} is less than or equal to {A}")
     ```
     **Output:** **The amount [amount] is less than or equal to [A] (where `amount` is the value of `amount` and `A` is the first element of
            the `balances` list)**

     ---

     ### **Your Task**

     **Initial State:**
     {pre}

     ```python
     {program}
     ```

     Now, please think step by step. Based on the precondition that describes the state of the program, variables, objects, etc., before the
            code is executed, calculate what will be printed when the `print` statement is executed. Explain the values of the variables,
           objects, etc., that are printed.

     Use natural language to describe the output, ensuring it is easily understandable by a human. Strictly adhere to the format **Output: `
           what is printed`**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.11       Return Command Execution Prompt

     You have been assigned the role of a program executor, responsible for simulating the execution of Python code. You will be provided
           with an **initial state** and a **Python code snippet**. Your task is to determine what the program **returns** based on the
           given initial state.
     - Avoid describing how the program runs step by step.
     - If a variable has a **specific value**, use that value directly.
     - If a return statement is executed, **always mention the returned value explicitly** in the output state.
     - Adhere to the text format: **Output State: `output state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.
     ### Example 1
     **Initial State:** `str` is a string, 'str' has 3 or more characters
     ```python
     return str
     ```
     **Output State:** **The program returns string `str` that has 3 or more characters**

     ### Example 2
     **Initial State:** `numbers` is an empty list, `total` is the sum of all positive integers that were in the original `numbers` list, `
           count` is the number of positive integers that were in the original `numbers` list, `average` is equal to `total / count`
     ```python
     return average
     ```
     **Output State:** **The program returns `average`, which is equal to `total/count`, where `total` is the sum of all positive integers
           in the original `numbers` list, and `count` is the number of positive integers in the original `numbers` list.**

     ### Example 3
     **Initial State:** `n` is either 3 or 5
     ```python
     return n + 1
     ```
     **Output State:** **The program returns 4 or 6**

     ### Example 4
     **Initial State:** `x` is 1, `y` is greater than 3, `z` is 0
     ```python
     return y + x
     ```
     **Output State:** **The program returns `y + 1`, where `y` is greater than 3**

     ### Example 5
     **Initial State:** `count` contains the number of numbers greater than 1 in the list `numbers`, `numbers` is a list of integers, `total
           ` is 0
     ```python
     return count
     ```
     **Output State:** **The program returns the number of integers greater than 1 in list `numbers`**

     ### **Your Task**

     **Initial State:**
     {pre}

     ```python
     {program}
     ```

     Now, please think step by step: List the impact of the code on the program, check the previous values of the affected variables, and
           then calculate what the program returns. Any variable or value that is included in the return should be fully described with all
           available information.

     Strictly adhere to the format: **Output State: `the output state you calculate`**, and describe this output state in **natural language
            easily understandable by humans**.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.12       Try-Except Statement Execution Prompt

     You have been assigned the role of a program verifier, responsible for summarizing the state of the function after executing a Python `
           try` statement. You will be provided with the **final state of the program** after executing the `try` block, along with the **
           changes in the program after executing one or more `except` blocks** in any situation. Your task is to **combine this information
            to summarize the program's state after the complete execution of the `try` statement**.

     - If a `return` statement is executed, **always include it in the output state**.
     - Adhere to the text format: **Output State: `output state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ---

     ### Example 1
     **Initial State:** `a` is an integer, `b` is an integer.
     ```python
     try:
         result = a / b
         return result
     except ZeroDivisionError:
         return None
     ```
     **Output state after executing the `try` block:** `a` is an integer, `b` is an integer, `result` is `a` divided by `b`, and the
           function returns `result`.

     **Output state after executing the `except` block:** If a `ZeroDivisionError` occurs (i.e., `b` is 0), the function returns `None`.

     **Final Output State:**
     A `ZeroDivisionError` might be triggered at `result = a / b`. If `b` is 0, the function returns `None`. Otherwise, the function returns
            the value of `a` divided by `b`.
     **Output State:** **`a` and `b` are integers. If `b` is zero, the function returns `None`, otherwise the function returns the value of
           `a` divided by `b`.**

     ---

     ### Example 2
     **Initial State:** `file_path` is a string that's supposed to be a path to a file.
     ```python
     def read_file(file_path):
         try:
             with open(file_path, 'r') as file:
                 data = file.read()
                 print("File content successfully read.")
                 return data
         except FileNotFoundError:
             print("Error: The file was not found. Please check the file path.")
             return None
         except PermissionError:
             print("Error: You do not have permission to read this file.")
             return None
     ```
     **Output state after executing the `try` block:** `file_path` is a string representing a file path, `data` contains the file content,
           and the function returns `data`.

     **Output state after executing the `except` block(s):**
     - If a `FileNotFoundError` occurs, the function prints an error message and returns `None`.
     - If a `PermissionError` occurs, the function prints a different error message and returns `None`.

     **Final Output State:**
     The program could raise a `FileNotFoundError` if the file is not found at the specified path or a `PermissionError` if the user does
           not have permission to read the file. If the file is found and the user has permission, the function reads the file content and
           returns it.
     **Output State:** **`file_path` is a string representing a file path. If the file exists and the user has permission, the function
           returns the file content; otherwise, it prints an error message and returns `None`.**
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev




     ### **Your Task**

     **Initial State:**
     {pre}

     **Code for the try-except block:**
     ```python
     {code}
     ```

     **Output state after executing the `try` block:**
     {try_post}

     **Output state after executing the `except` block(s):**
     {except_post}

     Now, please think step by step: At which point in the program could such an exception occur? Summarize what the `try-except` statement
           accomplishes and what the program output state is after execution.

     Strictly adhere to the format: **Output State: `the output state you calculate`**, and describe this output state in **natural language
            easily understandable by humans**.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.13      Function Functionality and Return Summary Prompt

     You have been assigned the task of a program verifier, responsible for describing the functionality of a Python function. You will be
           provided with the **constraints and relationships** between the input parameters, as well as the **resulting output** of the
           function based on these inputs. Your task is to **organize this information and describe the functionality of the function**.

     - Avoid describing how the function operates (e.g., local variable initialization or step-by-step execution).
     - Focus only on **what parameters the function accepts** and **what it returns**.
     - If there are multiple return points in the function, we will split them into **cases** labeled sequentially (Case 1, Case 2, etc.).
     - If one case is fulfilled, **none of the others are executed**.
     - Adhere strictly to the format: **Functionality: `functionality description`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.


     ### Example 1
     **Parameter constraints and relationships:** `number` is an integer.
     ```python
     def func(number):
     ```
     **Output:**
     - Case 1: If `number` is even, the function returns `True`.
     - Case 2: If `number` is not even, the function returns `False`.

     **Final Answer:**
     The function `func` accepts a parameter `number` and returns `True` if `number` is even. If `number` is not even, it returns `False`.
     **Functionality:** **The function accepts a parameter `number`, returns `True` if `number` is even. If `number` is not even, it returns
            `False`.**

     ### Example 2
     **Parameter constraints and relationships:** `age` is an integer.
     ```python
     def func(age):
     ```
     **Output:**
     - Case 1: If `age` is less than 0, the function returns an error message stating that ages can't be negative.
     - Case 2: If `age` is between 0 and 18, the function returns "minor".
     - Case 3: Otherwise, the function returns "adult".

     **Final Answer:**
     The function `func` accepts a parameter `age`. If `age` is below 0, the function returns an error message. If `age` is between 0 and
           18, it returns "minor". Otherwise, it returns "adult".
     **Functionality:** **The function accepts an integer `age`, returns an error if `age` is negative, "minor" if `age` is between 0 and
           18, and "adult" otherwise.**

     ### **Your Task**

     **Parameter constraints:**
     {pre}

     ```python
     {head}
     ```

     **Output:**
     {body_post}

     Now, please think step by step: What are the parameters the function accepts, and what does it return?

     Strictly adhere to the format: **Functionality: `the functionality you calculate`**, and describe this functionality in **natural
           language easily understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.14       If Condition Precondition Extraction Prompt

     You are assigned the role of a program verifier, responsible for finding the **postcondition** of an `if` statement based on its
           condition. You will be given:
     - A **precondition**, describing the initial state of the program variables before entering the `if` statement.
     - An **if condition**, which determines whether the program enters the `if` block.

     Your task is to determine the **postcondition**, which describes the state of the program variables after entering the `if` block. The
           postcondition must extend the precondition by ensuring that the `if` condition is true. This description should include both the
           values of the variables and the relationships between them.

     - **Do not explain how the program runs**; only focus on variable values and relationships.
     - Ensure that the postcondition retains all valid information from the precondition while incorporating the truth of the `if` condition.

     - Follow the format: **Postcondition: `calculated postcondition`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ---

     ### Example 1
     **Precondition:** `str` is a string
     **If condition:**
     ```python
     if len(str) < 3:
     ```
     **Postcondition:** **`str` is a string, and the length of `str` is less than 3**

     ---

     ### Example 2
     **Precondition:** `n` can have any value
     **If condition:**
     ```python
     if isinstance(n, int):
     ```
     **Postcondition:** **`n` is an integer of any value**

     ---

     ### Example 3
     **Precondition:** `x` is a positive integer
     **If condition:**
     ```python
     if x < 2:
     ```
     **Postcondition:** **`x` is a positive integer less than 2**

     ---

     ### Example 4
     **Precondition:** `m` is an integer. If `m` is higher than 10, then `n` equals `-m`. `a` is a list of integers.
     **If condition:**
     ```python
     if n < 0:
     ```
     **Postcondition:** **`m` is an integer, if `m` is higher than 10, `n` equals `-m`. `a` is a list of integers. The current value of `n`
            is less than 0**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




     ### Example 5
     **Precondition:** `x` is an integer, `a` is a list of integers.
     **If condition:**
     ```python
     if a[0] != 0:
     ```
     **Postcondition:** **`x` is an integer, `a` is a list of integers. The first element of `a` is not 0**

     ### **Your Task**

     **Precondition:**
     {precondition}

     **If condition:**
     ```python
     {program_fragment}
     ```

     Your task is to complete the **postcondition**. Ensure that:
     - All valid information from the **precondition** is retained.
     - The **if condition** is now assumed to be **true**.
     - If variables have values related to previous conditions, put that early in the postcondition and state the **current** value of the
           variable clearly.
     - The final state of the program **after entering the if block** is fully described.

     Strictly adhere to the format: **Postcondition: `the postcondition you calculate`**, and describe this postcondition in **natural
           language easily understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.15       Else Condition Precondition Extraction Prompt

     You are assigned the role of a program verifier, responsible for finding the **postcondition** of an `else` statement based on the
           condition of the corresponding `if` statement. You will be given:
     - A **precondition**, describing the initial state of the program variables before evaluating the `if` condition.
     - An **if condition**, which determines whether the program enters the `if` block. **In this case, we do not enter the `if` block but
           instead follow the `else` block**.

     Your task is to determine the **postcondition**, which describes the state of the program variables after entering the `else` block.
           The postcondition must extend the precondition by ensuring that the `if` condition is **false**. This description should include
           both the values of the variables and their relationships.

     - **Do not explain how the program runs**; only focus on variable values and relationships.
     - Ensure that the postcondition retains all valid information from the precondition while incorporating the negation of the `if`
           condition.
     - Follow the format: **Postcondition: `calculated postcondition`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ---

     ### Example 1
     **Precondition:** `str` is a string
     **If condition:**
     ```python
     if len(str) < 3:
     ```
     **Postcondition:** **`str` is a string, and the length of `str` is greater than or equal to 3**

     ---

     ### Example 2
     **Precondition:** `n` can have any value
     **If condition:**
     ```python
     if isinstance(n, int):
     ```
     **Postcondition:** **`n` can have any value except an integer**

     ---

     ### Example 3
     **Precondition:** `x` is a positive integer
     **If condition:**
     ```python
     if x < 2:
     ```
     **Postcondition:** **`x` is a positive integer greater than or equal to 2**

     ---

     ### Example 4
     **Precondition:** `m` is an integer, `n` is an integer, `a` is a list of integers.
     **If condition:**
     ```python
     if n <= 0:
     ```
     **Postcondition:** **`m` and `n` are integers, `n` is greater than 0, `a` is a list of integers**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




     ### Example 5
     **Precondition:** `x` is an integer, `a` is a list of integers.
     **If condition:**
     ```python
     if a[0] != 0:
     ```
     **Postcondition:** **`x` is an integer, `a` is a list of integers. The first element of `a` is 0**

     ### **Your Task**

     **Precondition:**
     {precondition}

     **If condition:**
     ```python
     {program_fragment}
     ```

     Your task is to complete the **postcondition**. Ensure that:
     - All valid information from the **precondition** is retained.
     - The **if condition** is now assumed to be **false**.
     - If variables have values related to previous conditions, put that early in the postcondition and state the **current** value of the
           variable clearly.
     - The final state of the program **after entering the else block** is fully described.

     Strictly adhere to the format: **Postcondition: `the postcondition you calculate`**, and describe this postcondition in **natural
           language easily understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.16       If-Else Statement Postcondition Extraction Prompt

     You are assigned the role of a program verifier, responsible for completing the **overall postcondition** of Hoare triples for `if`
           statements based on the postconditions of both the `if` and `else` parts. You will be given:
     - A **precondition**, describing the initial state of the program variables before the execution of the program fragment.
     - A **program fragment**, which contains an `if` condition and possibly an `else` block.
     - The **postcondition of the `if` part**, describing the state after entering the `if` block.
     - The **postcondition of the `else` part**, describing the state after entering the `else` block (if an `else` exists).

     Your task is to **combine the postconditions of both the `if` and `else` parts** (if an `else` exists), taking into account the `if`
           condition, to derive the **overall postcondition of the entire `if-else` block**.

     - **Do not explain how the program runs**; only focus on variable values and relationships.
     - Ensure that the postcondition retains all valid information from the precondition while incorporating both branches of the `if-else`
           logic.
     - Summarize the `if` statement in a **coherent paragraph**, rather than discussing it in separate sections.
     - Follow the format: **Postcondition: `calculated postcondition`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ---

     ### Example 1
     **Precondition:** `str` is a string
     **Program Fragment:**
     ```python
     if len(str) < 3:
     ```
     **If part:** `str` is a string with length less than 3, the function returns `None`
     **Else part:** There is no `else` part in the code

     **Postcondition:** **`str` is a string. If the length of `str` is less than 3, the function returns `None`.**

     ---

     ### Example 2
     **Precondition:** `n` can have any value
     **Program Fragment:**
     ```python
     if isinstance(n, int):

     else:
     ```
     **If part:** `n` is an integer of any value, and the function returns `n`
     **Else part:** `n` can have any value except an integer, and the function returns `int(n)`

     **Postcondition:** **If `n` is an integer, the function returns `n` itself. Otherwise, the function returns `int(n)`.**

     ---

     ### Example 3
     **Precondition:** `x` is a positive integer
     **Program Fragment:**
     ```python
     if x < 2:

     else:
     ```
     **If part:** `x` is a positive integer less than 2, and the function returns `False`
     **Else part:** `x` is a positive integer greater than or equal to 2, and the function returns `True`

     **Postcondition:** **`x` is a positive integer. If `x` is less than 2, the function returns `False`. Otherwise, the function returns `
           True`.**
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil




     ### Example 4
     **Precondition:** `m` is an integer, `n` is an integer
     **Program Fragment:**
     ```python
     if n < 0:

     else:
     ```
     **If part:** The integer `n` was originally negative, `n` is updated to its negation, and `m` is increased by 1
     **Else part:** If `n` is 0, the function returns `m`. Otherwise, `n` is decreased by 13, and `m` is increased by 1

     **Postcondition:** **`m` and `n` are integers. If `n < 0`, `m` is increased by 1 and `n` is negated. If `n == 0`, the function returns
            `m`. Otherwise, `n` is decreased by 13 and `m` is increased by 1.**

     ---

     ### Example 5
     **Precondition:** `x` is an integer, `y` is zero
     **Program Fragment:**
     ```python
     if x > 0:
     ```
     **If part:** `x` is a positive integer. If `x > 10`, `y` is set to twice the value of `x`. Otherwise, `y` is set to `x + 5`.
     **Else part:** There is no `else` part in the code

     **Postcondition:** **`x` is an integer. If `x > 10`, `y` is set to twice the value of `x`. If `x` is greater than 0 but less than 10, `
           y` is set to `x + 5`.**

     ---

     ### **Your Task**

     **Precondition:**
     {precondition}

     **Program Fragment:**
     ```python
     {program_fragment}
     ```

     **If part:**
     {postconditions_if}

     **Else part:**
     {postconditions_else}

     Your task is to **complete the overall postcondition of the entire if-else block**. Summarize all cases and describe the final state of
            the program **after executing the if-else statement**.

     Strictly adhere to the format: **Postcondition: `the postcondition you calculate`**, and describe this postcondition in **natural
           language easily understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.17       While Loop First Execution Necessary Condition Prompt

     You have been assigned the task of a program verifier, responsible for modifying the **program state** so that the first iteration of
           the `while` loop can proceed. You will be provided with the **program state right before the loop**, which you need to modify,
           and the `while` loop statement.

     - If the loop is a `while True` loop or if the loop **can certainly execute at least once**, simply repeat the program state right
           before the loop.
     - **Do not make any assumptions** beyond the provided information.
     - Only modify the states of **objects in the loop condition** that affect whether the loop executes.
     - **Follow the text format:** **State: `state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ### Example 1
     **State right before the while loop:** `total` is 10, `i` is 0, `n` is an integer.
     **While loop:**
     ```python
     while i < n:
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute the first time? **Only the states of objects
           in the loop head can be adjusted.**

     **Example Answer:**
     The variables in the loop condition are `i` and `n`, so we can only adjust them. The loop executes while `i < n`. Right before the loop
           , `i` is 0 and `n` is an integer. Since `n` being an integer does not ensure the loop executes, it needs to be modified to `n` is
            greater than 0.

     **State:** **`total` is 10, `i` is 0, `n` must be greater than 0**

     ### Example 2
     **State right before the while loop:** `total` is 0, `students` is 2 less than its initial value.
     **While loop:**
     ```python
     while students >= 1:
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute the first time? **Only the states of objects
           in the loop head can be adjusted.**

     **Example Answer:**
     The only variable in the loop condition is `students`. The loop executes while `students >= 1`. Right before the loop, `students` is
           **2 less than its initial value**, so for the loop to execute at least once, the initial value of `students` must have been at
           least 3, and its current value must be greater than or equal to 1.

     **State:** **`total` is 0, `students` is 2 less than its initial value, and `students` must currently be greater than or equal to 1**

     ### **Your Task**

     **State right before the while loop:**
     {post}

     ```python
     {loop_head}
         # the loop body is omitted
     ```

     Now, please think step by step: Which states need to be adjusted for the loop to execute the first time? **Only modify the states of
           objects in the loop head.*
     Strictly adhere to the format: **State: `the state you calculate`**, and describe this state in **natural language easily
           understandable by humans**.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.18      While Loop Prerequisite for Next Execution Prompt

     You have been assigned the task of a program verifier, responsible for modifying the **program state** so that the next iteration of
           the `while` loop can proceed. You will be provided with the **program state after the previous iteration**, which you need to
           modify, and the `while` loop statement.

     - If the loop is a `while True` loop or if the loop **can certainly execute one more time**, simply repeat the program state at the end
            of the previous iteration.
     - **Do not make any assumptions** beyond the provided information.
     - Only modify the states of **objects in the loop condition** that affect whether the loop executes.
     - **Follow the text format:** **State: `state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ### Example 1
     **State at the end of the previous iteration:** `total` is 10, `i` is 4, `n` is greater than 3.
     **While loop:**
     ```python
     while i < n:
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute one more time? **Only the states of objects in
            the loop head can be adjusted.**

     **Example Answer:**
     The variables in the loop condition are `i` and `n`, so we can only adjust them. The loop executes while `i < n`. At the end of the
           last iteration, `i` is 4, `n` is greater than 3. `n` being greater than 3 does not ensure another execution, so it needs to be
           modified to `n` is greater than 4.

     **State:** **`total` is 10, `i` is 4, `n` must be greater than 4**


     ### Example 2
     **State at the end of the previous iteration:** `total` is 0, `students` is 3 less than its initial value.
     **While loop:**
     ```python
     while students >= 1:
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute one more time? **Only the states of objects in
            the loop head can be adjusted.**

     **Example Answer:**
     The only variable in the loop condition is `students`. The loop executes while `students >= 1`. At the end of the last iteration, `
           students` is **3 less than its initial value**, so for the loop to execute again, the initial value of `students` must have been
           at least 4, and its current value must be greater than or equal to 1.

     **State:** **`total` is 0, `students` is 3 less than its initial value, and `students` must currently be greater than or equal to 1**

     ### **Your Task**

     **State at the end of the previous iteration:**
     {post}

     ```python
     {loop_head}
         # the loop body is omitted
     ```

     Now, please think step by step: Which states need to be adjusted for the loop to execute one more time? **Only modify the states of
           objects in the loop head.**
     Strictly adhere to the format: **State: `the state you calculate`**, and describe this state in **natural language easily
           understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.19       For Loop First Execution Necessary Condition Prompt

     You have been assigned the task of a program verifier, responsible for understanding the **program state at the start of the `for` loop
           **. You will be provided with the **program state before the first execution of the `for` loop**, which you need to modify, and
           the `for` loop statement.

     - **Do not make any assumptions** beyond the provided information.
     - Only modify the states of **objects in the loop condition** that affect whether the loop executes.
     - **Follow the text format:** **State: `state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ### Example 1
     **State before the `for` loop:** `total` is 10.
     **For loop:**
     ```python
     for i in range(n):
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute? **Only the states of objects in the loop head
            can be adjusted.**

     **Example Answer:**
     The only variables in the loop head are `i` and `n`, so we can only adjust those. The loop executes while `n` is at least 1. Since `
           total` being 10 does not ensure that the loop will execute, `n` needs to be adjusted to be greater than 0, and `i` is initialized
            to 0.

     **State:** **`total` is 10, `i` is 0, `n` must be greater than 0**


     ### Example 2
     **State before the loop starts:** `total` is 0, `students_list` is a list of students.
     **For loop:**
     ```python
     for index, student in enumerate(students_list):
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute? **Only the states of objects in the loop head
            can be adjusted.**

     **Example Answer:**
     The only objects in the loop head are `index`, `student`, and `students_list`, so we can only adjust those. The loop executes if `
           students_list` has at least 1 student. Since the `total` value does not impact execution, we focus on ensuring that `
           students_list` contains at least 1 student. The `index` starts at 0, and `student` is set to the first student in the list.

     **State:** **`total` is 0, `students_list` is a list of students that must have at least 1 student, `student` is the first student in
           the list, `index` is 0**

     ### **Your Task**

     **State before the loop starts:**
     {post}

     ```python
     {loop_head}
         # the loop body is omitted
     ```

     Now, please think step by step: Which states need to be adjusted for the loop to execute? **Only modify the states of objects in the
           loop head.**

     Strictly adhere to the format: **State: `the state you calculate`**, and describe this state in **natural language easily
           understandable by humans**.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.20      For Loop Prerequisite for Next Execution Prompt

     You have been assigned the task of a program verifier, responsible for understanding the **program state at the start of the next
           iteration of a `for` loop**. You will be provided with the **program state after the previous iteration**, which you need to
           modify, and the `for` loop statement.
     - **Do not make any assumptions** beyond the provided information.
     - Only modify the states of **objects in the loop condition** that affect whether the loop executes again.
     - **Follow the text format:** **State: `state`**.

     I am giving you some examples to understand the task better. Then I am giving you your task.

     ### Example 1
     **State at the end of the previous iteration:** `total` is 10, `i` is 3, `n` must be greater than 3.
     **For loop:**
     ```python
     for i in range(n):
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted at the start of the next iteration of the loop? **Only the states of
           objects in the loop head can be adjusted.**

     **Example Answer:**
     The only variables in the loop head are `i` and `n`, so we can only adjust those. The loop executes while `i` is less than `n`. At the
           end of the last iteration, `i` is 3, `n` is greater than 3. Since `i` is incremented by 1 in each iteration, for the loop to
           execute again, `i` must be 4 and `n` must be greater than 4.

     **State:** **`total` is 10, `i` is 4, `n` must be greater than 4**

     ### Example 2
     **State at the end of the previous iteration:** `total` is 0, `students_list` is a list of students that must have at least 2 students,
            `student` is the second student in the list, `index` is 1.
     **For loop:**
     ```python
     for index, student in enumerate(students_list):
         # the loop body is omitted
     ```
     Now, please think step by step: Which states need to be adjusted for the loop to execute one more time? **Only the states of objects in
            the loop head can be adjusted.**

     **Example Answer:**
     The only objects in the loop head are `index`, `student`, and `students_list`, so we can only adjust those. The loop executes if `
           students_list` has at least 3 students. At the end of the last iteration, `students_list` has at least 2 students, `student` is
           the second student in the list, and `index` is 1. So, for the loop to execute one more time, `students_list` must have at least 3
            students, `index` must be 2, and `student` must be the third student in the list.

     **State:** **`total` is 0, `students_list` is a list of students that must have at least 3 students, `student` is the third student in
           the list, `index` is 2**

     ### **Your Task**

     **State at the end of the previous iteration:**
     {post}

     ```python
     {loop_head}
         # the loop body is omitted
     ```

     Now, please think step by step: Which states need to be adjusted for the loop to execute one more time? **Only modify the states of
           objects in the loop head.**
     Strictly adhere to the format: **State: `the state you calculate`**, and describe this state in **natural language easily
           understandable by humans**.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                    Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev


B.21       Total While Loop Execution with Unrolling Prompt

     Given a Python loop, an initial execution state, and the output states after the first {times} iterations of the loop, determine the
           output state after all the executions of the loop have finished.

     You must adhere to the text format: Output State: **output state.**

     Initial State: {pre}
     Code of the loop:
     {loop_code}

     The output state after the loop executes the first {times} times includes what needed to be true for the loop to execute at least that
           number of times:
     {loop_unrolled}

     What is the ouput state after the loop executes all the iterations? Change the values of only the variables in the loop head and body.
           The state of the other variables in the precondition that are not affected by the loop head and body must remain unchanged.
     In your response strictly use the format: Output State: **the output state you calculate.**, and describe this output state in Natural
           language easily understandable by humans.




B.22       Total While Loop Execution Without Unrolling Prompt

     Given a Python loop and an initial execution state, determine the output state after all the executions of the loop have finished.

     You must adhere to the text format: Output State: **output state.**

     Initial State: {pre}
     Code of the loop:
     {loop_code}

     What is the output state after the loop executes all the iterations? Change the values of only the variables in the loop head and body.
            The state of the other variables in the precondition that are not affected by the loop head and body must remain unchanged.
     In your response strictly use the format: Output State: **the output state you calculate.**, and describe this output state in Natural
           language easily understandable by humans.




B.23       Total For Loop Execution with Unrolling Prompt

     Given a Python loop, an initial execution state, and the output states after the first {times} iterations of the loop, determine the
           output state after all the executions of the loop have finished.

     You must adhere to the text format: Output State: **output state.**

     Initial State: {pre}
     Code of the loop:
     {loop_code}

     The output state after the loop executes the first {times} of times includes what needed to be true for the loop to execute at least
           that number of times:
     {loop_unrolled}

     What is the ouput state after the loop executes all the iterations? Change the values of only the variables in the loop head and body.
           The state of the other variables in the precondition that are not affected by the loop head and body must remain unchanged.
     In your response strictly use the format: Output State: **the output state you calculate.**, and describe this output state in Natural
           language easily understandable by humans.
HoarePrompt : Structural Reasoning About Program Correctness in Natural Language                         ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


B.24      Total For Loop Execution Without Unrolling Prompt

     Given a Python loop, and an initial execution state, determine the output state after all the executions of the loop have finished.

     You must adhere to the text format: Output State: **output state.**

     Initial State: {pre}
     Code of the loop:
     {loop_code}

     What is the ouput state after the loop executes all the iterations? Change the values of only the variables in the loop head and body.
           The state of the other variables in the precondition that are not affected by the loop head and body must remain unchanged.
     The output state must be in a similar format as the initial execution state. Describe this output state in Natural language easily
           understandable by humans. In your response strictly use the format: Output State: **the output state you calculate.**.
