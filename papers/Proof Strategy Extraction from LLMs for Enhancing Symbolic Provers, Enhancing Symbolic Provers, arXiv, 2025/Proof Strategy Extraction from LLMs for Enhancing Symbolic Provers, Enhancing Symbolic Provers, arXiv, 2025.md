                                               Proof Strategy Extraction from LLMs for
                                                     Enhancing Symbolic Provers

                                                          Jian Fang, Yican Sun, and Yingfei Xiong(B)

                                          Key Laboratory of High Confidence Software Technologies (Peking University),
                                        Ministry of Education; School of Computer Science, Peking University, Beijing, China
                                                                    fangjian@stu.pku.edu.cn
arXiv:2510.10131v2 [cs.LO] 4 Mar 2026




                                                                  {sycpku,xiongyf}@pku.edu.cn



                                              Abstract. One important approach to software verification is interac-
                                              tive theorem proving. However, writing formal proofs often requires sub-
                                              stantial human effort, making proof automation highly important. Tradi-
                                              tionally, proof automation has relied on symbolic provers. Recently, large
                                              language models (LLMs) have demonstrated strong capabilities in the-
                                              orem proving, complementing symbolic provers. Nonetheless, prompting
                                              LLMs can be expensive and may pose security risks for confidential code-
                                              bases. As a result, purely symbolic approaches remain important even
                                              in the LLM era, as they are cost-effective, secure, and complement the
                                              strengths of LLMs.
                                              Motivated by these considerations, we pose a new research question: can
                                              the internal proof strategies of LLMs be extracted to enhance the capabil-
                                              ities of symbolic provers? As an initial step, we introduce Strat2Rocq.
                                              In an offline stage, Strat2Rocq extracts proof strategies from LLMs
                                              and formalizes them as lemmas in Rocq. In an online stage, given a
                                              theorem to be proved, Strat2Rocq augments the proof context with
                                              these extracted lemmas, enabling CoqHammer to leverage the LLM-
                                              derived strategies for more effective automated proving. Our evaluation
                                              demonstrates that, on open-source Rocq projects for software verifica-
                                              tion, Strat2Rocq enhances the success rate of CoqHammer by 13.41%.
                                              A side discovery is that the extracted lemmas are also beneficial to LLM
                                              proof agents, improving the success rate of an LLM proof agent by 4.00%.

                                              Keywords: Software Verification · Large Language Models · Proof Strat-
                                              egy Extraction · Symbolic Provers.


                                        1   Introduction

                                        Software verification is a critical area in software engineering, aiming to ensure
                                        that a software system never performs unsafe operations or exhibits undesirable
                                        behavior [21, 23]. One important approach to software verification is interac-
                                        tive theorem proving (ITP), which has been successfully applied to build the
                                        certified C compiler [23], micro operating system kernel [21], and cryptographic
                                        systems [33]. However, writing formal proofs often requires a substantial amount
2       J. Fang et al.

of effort. In seL4 [21], a verified OS kernel, the effort in writing the proof code
is approximately 10 times as large as that of implementing the kernel.
    Recently, large language models (LLMs) have demonstrated significant ca-
pabilities in proof automation, effectively complementing traditional symbolic
approaches [20, 25, 39]. As shown in recent studies, proof agents, which integrate
LLMs with ITPs, can achieve state-of-the-art performance.
    However, these hybrid proof agents cannot fully replace purely symbolic ap-
proaches. LLMs typically require substantial computational resources, making
them unsuitable for scenarios with limited hardware availability [14, 18]. This
drawback is especially relevant for many safety-critical software vendors, which
are often small companies with constrained budgets. Furthermore, their code-
bases are often confidential, preventing the use of external LLM services. In
contrast, symbolic proof automation systems can be executed efficiently on a
personal computer, without requiring significant computational infrastructure
or posing risks of information leakage.
Research Question. Given that symbolic provers remain important even in
the era of LLMs–and indeed complement LLMs–we pose the following research
question:
    Can we extract the proving capabilities of LLMs to enhance symbolic provers?
    As noted in previous literature from cognitive science, human problem solving
is often characterized by the combination of internally acquired strategies [10,29].
In the context of theorem proving, these proof strategies correspond to theorems
and lemmas at which the human prover excels. Given that LLMs are trained on
large corpora of human-created data, we hypothesize that LLMs adopt a similar
paradigm when generating proofs. For example, given the expression a + b + c,
an LLM may be able to immediately infer that this expression is equal to c +
b + a—or any other permutation—rather than applying a step-by-step sequence
of transformations based on the laws of associativity and commutativity. If we
can extract these proof strategies into a form accessible to symbolic provers, we
may be able to improve the performance of symbolic provers.
    The key question, then, is how to extract these proof strategies. Our approach
is to inspect the proof trajectories generated by LLMs. If an LLM infers a conclu-
sion directly from a set of premises without intermediate steps, we identify that
inference as applying a proof strategy. We use lemmas to represent these strate-
gies, since lemmas in modern formal proof languages are both expressive and
accessible to provers. Hence, we design two separate stages for extraction and
utilization of these strategies, namely offline lemma mining and online proving.
    Stage 1: Offline lemma mining. In this stage, we are given a training
set (a corpus of theorems). We scan each theorem in the training set and follow
a prompt-and-formalize workflow as follows: i) First, we prompt the LLMs to
prove each theorem. ii) Then, we extract strategies from the resulting proof
trajectories and formalize these strategies as lemmas in a proof language (e.g.,
Rocq). This stage is executed only once.
    Stage 2: Online theorem proving. After all lemmas have been extracted,
we insert them into the context of new theorems to be proved, thereby making
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers       3

CoqHammer accessible to the internal knowledge distilled from the LLM. Un-
like previous proof agents [20, 39] where LLMs are inevitable in online proving,
our approach only relies on a purely symbolic prover to prove a user-provided
theorem.
    As an initial validation of our idea, this paper introduces Strat2Rocq,
which extracts the proof strategies of LLMs as formalized lemmas in Rocq. We
select CoqHammer [9], the state-of-the-art symbolic prover in Rocq, as the target
system to be improved.
Evaluation. To evaluate Strat2Rocq, we selected open-source Rocq projects
focused on software verification, including:

 – Coq-Art [3]: a textbook on Rocq in building simple certified programming
   languages and data structures.
 – Ext-Lib [26]: a community-driven Rocq library.
 – Vfa [2], the third volume of Software Foundations focusing on verified func-
   tional algorithms.
 – CompCert [23], the certified C compiler written in Rocq.

We collected all theorems from Coq-Art, Ext-Lib and Vfa, and sample 1,000
theorems from CompCert. As a result, we obtain a benchmark of 2,394 for-
malized Rocq theorems. We applied 3-fold cross-validation and measured the
success rate of CoqHammer both before and after granting it access to the new
lemmas extracted by Strat2Rocq. Our results demonstrate that Strat2Rocq
increases the proof success rate by 13.41% in average. Furthermore, though our
primary goal is to improve symbolic provers, the extracted lemmas are also ben-
eficial to an LLM agent, improving the performance of an LLM agent by 4.00%.
Contribution. In summary, the contributions of this paper are as follows:

 – We propose a novel research problem: offline extracting proof strategies
   from large language models (LLMs) to enhance the performance of symbolic
   provers.
 – We propose an approach for extracting reusable lemmas by analyzing natural
   language proofs generated by LLMs, enabling the proof strategies of LLMs
   to be integrated into symbolic provers.
 – We implemented our method as Strat2Rocq and empirically validated its
   effectiveness.


2   Our Framework: Strat2Rocq

This section presents Strat2Rocq, our framework for extracting knowledges
from LLMs. Throughout this section, we will use the following running example
for demonstration.

Example 1 (Running Example). Consider the theorem power_commute_with_x
presented in Figure 1, which is extracted from the widely-used Coq-Art project.
This theorem concerns a fundamental property of Monoids [7, 40]. A Monoid is
4       J. Fang et al.


(* Monoid over the set A *)
Class Monoid (dot: A→ A→ A) (one: A) := {
  dot_assoc : forall x y z: A, dot x (dot y z) = dot (dot x y) z;
  one_left : forall x: A, dot one x = x;
  one_right : forall x: A, dot x one = x
}.
(* Generalized power operator the monoid M *)
Fixpoint power {M : Monoid A dot one} (a: A) (n: nat) :=
  match n with
    | 0 ⇒ one
    | S p ⇒ dot a (power a p)
  end.
 (* The theorem to be proved, where dot and power are monoid operators *)
Theorem power_commute_with_x: forall (x: A) (n: nat), dot x (power x n) = dot (power x n) x.


                              Fig. 1. Our Running Example



an abstract interface that captures the essence of many common data structures,
such as natural numbers and lists, and finds applications in diverse programming
scenarios including data aggregation, log system construction, and parser com-
position [7, 8, 16]. More precisely, as illustrated in Figure 1, a Monoid is defined
over a base set A and is equipped with a multiplication operation dot that is
associative and has a unit element one. Additionally, the power operator for a
Monoid (the function power in Figure 1) is defined as a generalization of the
familiar power operation on natural numbers.
    With these definitions in place, our target theorem states the following: for
every element x ∈ A, multiplying x to either the left or the right of power x n
yields the same result; in both cases, the result is precisely power x (n + 1).
Notably, CoqHammer is unable to prove this theorem.                                ⊓
                                                                                   ⊔




                         Fig. 2. The Workflow of Strat2Rocq
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers          5

Workflow. The overall workflow is illustrated in Figure 2. The proposed frame-
work comprises two stages:
 – Stage 1: Offline Lemma Mining. In this stage, we extract internal proof
   strategies from LLMs over a given training set. For each theorem in the
   training set, we (1) generate a natural-language proof and subsequently (2)
   generalize and formalize each atomic proof step into a new lemma. These
   two steps are detailed in Section 2.1 and Section 2.2, respectively. This stage
   is performed only once.
 – Stage 2: Online Theorem Proving. After obtaining the formalized lem-
   mas, they are inserted into the context of the user-provided new theorem to
   be proved. We describe this stage in Section 2.3.



You are an expert at Rocq theorem proving . Please give a step - by - step natural
  language proof for the given theorem .
Below , we further provide some helper information .
[ Type Definitions ] ...
[ Function Definitions ] ...
[ Script So Far ] ...
Finally , The given theorem is : ...



         Fig. 3. Detailed Prompts for Natural Language Proof Generation




2.1   Step 1 of Stage 1: Natural-Language Proof Generation
For each theorem thm in the training set, we begin by generating a natural-
language (NL) proof. We adopt NL proofs rather than formal proofs because
LLMs typically demonstrate stronger performance in producing NL proof. More-
over, when generating formal proofs, LLMs often first construct an NL proof and
then formalize it. Consequently, the NL proof is likely to reflect the internal rea-
soning process of the LLM.
Example 2. Continuing with Example 1, suppose the training set includes the
following theorem, sqr, located in the file Monoid.v. The theorem states that
for every element x in the monoid, its square is simply dot x x:
Theorem sqr: forall x: A, power x 2 = dot x x.
In subsequent examples (Examples 3 and 4), we will demonstrate that, after
adding the lemmas formalized from the LLM-generated NL proof of the theorem
sqr, CoqHammer becomes capable of proving the theorem in Example 1.       ⊓
                                                                          ⊔
   Our prompt for generating the NL proof follows the template in Figure 3.
The prompt starts with a role description: “You are an expert at Rocq theorem
proving,” followed by an articulation of the task, asking the LLM to generate the
step-by-step NL proof for the given theorem. Our prompt also supplies essential
background information, including:
6          J. Fang et al.

    – Type Definitions: Definitions of all types referenced in thm.
    – Function Definitions: Definitions of all functions used in thm. Supplying
      relevant types and functions helps the LLM better understand the theorem
      and generate higher-quality proofs.
    – Script So Far: The content of the file containing thm, preceding the statement
      of thm. This information enables the LLM to accurately interpret the broader
      context in which the theorem is stated.

In response to our prompt, the LLM produces a step-by-step natural language
proof for the current theorem.

Example 3. Continuing with Example 2, as illustrated in Figure 3, the system
prompt consists of the definitions of Monoid and Power, as well as all Rocq scripts
in Monoid.v preceding the statement of the theorem sqr. The user prompt is
simply the theorem statement of sqr. The response of LLM is presented below.
         1) Introduce the only variable.
         2) Simplify the definition of "power" at n = 2.
         After this simplification, power x 2 = dot x (power x 1).
         3) Simplify "power x 1": Now power x 1 = dot x (power x 0) = dot x one.
         ... Further steps omitted

Notably, there is a sub-step showing that power x 1 = dot x one. After for-
malization, this step becomes crucial for proving our target theorem Example 1.


2.2       Step 2 of Stage 1: Generalization and Formalization of the
          Natural-Language Proof Steps



Based     on   the NL proof above , subsequently do the following tasks :
[ Task    1]   Generalize the proof steps above as general lemmas .
[ Task    2]   Formalize each lemma in Rocq , and provide the formal proof .
[ Task    3]   Return a Rocq script that includes all formalized lemmas and proofs .



                Fig. 4. Detailed Prompts for Generalization and Formalization


    To ensure that the extracted strategy is not restricted to a specific theorem
in the training set, we prompt the LLM to generalize the properties identified
in the natural-language proof. After obtaining these generalized strategies, we
formalize them as lemmas in Rocq.
    The latter task in this step is known also as autoformalization [43], which
aims to automatically translate NL proofs into formal proofs. Autoformaliza-
tion is widely regarded as an open challenge for LLMs [42, 43]. However, in our
setting, we only require the formalization of each individual proof step, which
substantially simplifies the autoformalization problem.
    We reuse the same chat session described in Section 2.1 and append a new
query using the prompt shown in Figure 4. This prompt instructs the LLM, in
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers         7

a step-by-step manner, to generalize, formalize, and summarize the proof. An
alternative design would be to first parse the NL proof into individual steps and
then ask the LLM to generalize, formalize, and prove each step independently.
We do not adopt this design for two reasons: (1) the LLM’s output may not
adhere to a fixed format even when one is specified in the prompt, and parsing
such NL output can lead to frequent failures; and (2) the steps in the NL proof
often depend on one another, so even if parsing were successful, it would still be
difficult to independently formalize each step.
    In practice, LLMs often fail to produce correct lemmas and formal proofs
in a single attempt. To mitigate this, we employ a standard proof agent that
iteratively invokes the LLM to repair both the lemma and its proof. The details
of this proof agent are provided in Section 2.4.

Example 4. Continuing with Example 3, for the highlighted step in the LLM
response, Strat2Rocq generalizes and formalizes the step as lemma power_1.
(* Other lemmas omitted *)
Lemma power_1: forall x: A, power x 1 = x.
Proof. trivial. Qed.

This lemma will be further added to the context of CoqHammer during online
theorem proving.


2.3   Stage 2: Online Theorem Proving

After extracting lemmas from the training set, given a target theorem to be
proved, we insert the extracted lemmas into the context of the target theorem,
thereby making them accessible to CoqHammer during the proof search. Because
these additional lemmas capture the internal proof strategies of the LLM, the
proving capabilities of CoqHammer are improved through the integration of
LLM-extracted knowledge.

Example 5. Continuing with Example 4, after inserting the LLM-generated lem-
mas into the context, we observe that CoqHammer is then able to automatically
prove our target theorem (Example 1). This improvement arises because, after
adding the lemma power_1, CoqHammer can rewrite the theorem statement of
Example 1 as dot (power x 1) (power x n) = dot (power x n) (power x
1). Using other existing theorems, this can be further reduced to power x (1 +
n) = power x (n + 1), which follows directly from the commutativity of ad-
dition.                                                                      ⊔
                                                                             ⊓


2.4   Implementation Details

We implement Strat2Rocq on Rocq 8.20.0. To retrieve relevant type and func-
tion definitions, which are filled into the prompt described in Figure 3, we employ
meta-programming using the OCaml libraries of Coq and develop a dedicated
tactic that pretty-prints these definitions.
8         J. Fang et al.

    A natural concern is whether adding a large number of new lemmas burdens
the hammer. However, CoqHammer uses a built-in KNN-based lemma selection
mechanism for retrieving relevant lemmas from the context. Crucially, regardless
of the total number of lemmas available, CoqHammer always retrieves a fixed
number of candidate lemmas for each proof task. This design ensures that, even
when many new lemmas are added to the context, the efficiency of CoqHammer
remains largely unaffected.
    Finally, we describe the design of our proof agent. The agent takes as input a
lemma, its corresponding proof, and a limit round_limit. It iteratively attempts
to repair errors for at most round_limit rounds, and returns the corrected
versions if successful; otherwise, it reports failure once the round limit is reached.
The repair process follows a module-based approach [25]. We define a set of
predefined error types, each associated with a dedicated LLM-assisted repair
module, where each module is equipped with a specialized prompt tailored to its
error category. When an error message matches one of these predefined types,
the corresponding module is invoked. If the error does not match any predefined
category, the default repair agent, which prompts the LLM using only the raw
error message without additional guidance, is executed.


3      Evaluation

Research Questions. We focus on the following research questions.

    – RQ1: How effectively can Strat2Rocq extract proof strategies from LLMs?
    – RQ2: To what extent do the proof strategies extracted by Strat2Rocq
      improve the success rate of symbolic provers?
    – RQ3: Does Strat2Rocq work with other backend LLMs?
    – RQ4: How does the extraction method in Strat2Rocq contribute to its
      overall performance?
    – RQ5: Do the extracted lemmas benefit LLM agents?

Dataset. The evaluation of our approach requires a training set and a testing
set. We follow the standard machine learning practice, collecting a dataset and
using n-fold cross-validataion to evaluate our approach. We constructed a dataset
of proved theorems collected from open-source Rocq projects focused on software
verification. These projects include:

    – CompCert [23]: a certified C compiler implemented in Rocq,
    – Ext-Lib [26]: a community-driven Rocq library,
    – Coq-Art [3]: a textbook on Rocq for building certified programming lan-
      guages and data structures,
    – Vfa [2]: the third volume of Software Foundations focusing on verified func-
      tional algorithms.

For CompCert, due to its large number of theorems, we follow the procedure
of previous works [20, 39] and randomly sample 1,000 theorems. For the other
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers             9

projects, we collected all theorems available in each project. In total, our dataset
comprises 2,394 theorems from these projects.
Configurations. For generating natural language proofs and summarizing lem-
mas, we use Claude 3.7 Sonnet in non-thinking mode [1]. For proof agent demon-
strated in Section 2.4, we set round_limit to 8.
    All experiments were conducted on a server equipped with an 80-core Intel(R)
Xeon(R) Gold 6230 CPU, 512 GB RAM, and running Ubuntu 20.04.6.

3.1   RQ1: How effectively can Strat2Rocq extract proof strategies
      from LLMs?

Procedure. This experiment evaluates the offline lemma mining stage (Stage
1, Sections 2.1 and 2.2) of Strat2Rocq. We apply Strat2Rocq to mine proof
strategy lemmas with corresponding proofs across all collected 2,394 theorems.
The results are summarized in Table 1, where for each project, we further report:
i) the total number of natural-language proof steps generated by the backend
LLM, and ii) the number of lemmas successfully proved by our proof agent.
We also report the average number of added lemmas, relative to the number of
existing theorems, which reflects the average number of internal proof strategies
that can be extracted by Strat2Rocq from each theorem.


            Table 1. Detailed Statistics for Proof Strategies Extraction

                                   Claude 3.7 Sonnet              o3-mini
                   #Theorems #NL Steps    #Lemmas        #NL Steps    #Lemmas
        CompCert      1000      3650     1611 (× 1.61)     4583       721 (× 0.72)
         Ext-Lib       187       468     300 (× 1.60)       439       243 (× 1.30)
        Coq-Art        947      3573     2409 (× 2.54)     3602      1906 (× 2.01)
          Vfa         260       1023     263 (× 1.01)      1004       215 (× 0.83)
           Total      2394      8714     4583 (× 1.91)     9947      3085 (× 1.29)




Results. Table 1 shows that, on average, Strat2Rocq is able to extract 1.91
new lemmas for each original theorem. These results demonstrate that Strat2Rocq
has been effective in extracting internal proof strategies from LLM.
Case Studies. We observe that about half of the NL steps are not success-
fully generalized and formalized as lemmas. We analyzed the main reasons, and
summarize three main reasons qualitatively below.
    Incorrect NL Proof due to Hallucinations in LLMs. Consider the following
theorem from our dataset.
Hypothesis bad_inference := forall P Q : Prop, (P → Q) → ∼P → ∼Q.
Theorem incons: False.
It assumes an incorrect logical rule: it swaps the premise and conclusion in the
contrapositive rule, whereas the correct form should be (P → Q) → (∼ Q →∼ P).
10      J. Fang et al.

Our goal is to show that, by applying this incorrect rule, one can derive False
without any assumptions, thereby establishing the logical inconsistency of the
incorrect inference rule.
   However, when generating the natural-language proof for the theorem above,
the LLM produces the following response:
     ...
     This is actually a valid principle in i ntuiti onisti c logic ! It ’ s a
     cont raposi tive form that says : if P implies Q , and P is false , then
      Q must be false . Since the hypothesis is valid , we cannot prove
     False from it directly .


In this case, the LLM falls into the hallucination [15], it misidentifies the incorrect
hypothesis as the correct contrapositive rule and, as a result, refuses to provide
any natural-language proof.
   Failure in Converting an NL step into a Lemma. Consider the following
theorem from our dataset, which concerns another fundamental property of the
generalized power function on Monoid (see Figure 1 for the definition).
Lemma power_of_power_monoid: forall {M: monoid dot one} (x: A) (n p: nat),
    power (power x n) p = power x (p * n).

The LLM-generated natural language proof includes the following step (high-
lighted in red), which involves manipulating natural numbers:
     ...
     we have power x (n + (q * n)), which equals power x ((1 + q) * n).
     ...


Ideally, we would expect the LLM to derive the following lemma, which is not
present in the standard library of natural numbers.
Lemma nat_succ_mul_custom: forall (n q: nat), n + (q * n) = (1 + q) * n.

However, the LLM fails to identify this lemma in the complex context involving
the power function and natural number manipulation, and does not generate it
when prompted to summarize its own natural-language proof.
    Failures in Proving a Lemma. We note that the effectiveness of Strat2Rocq
is also significantly influenced by the proving capabilities of the underlying proof
agent. A stronger proof agent can verify a larger fraction of LLM-summarized
lemmas, resulting in a more comprehensive set of extracted proof strategies. The
development of advanced proof agents is orthogonal to this paper. In the future,
equipping Strat2Rocq with a more powerful agent could yield an even richer
library of internal proof strategies derived from LLMs.

  Answer to RQ1: Strat2Rocq is overall effective in extracting internal
  proof strategies from the LLM via a training set.
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers       11

Table 2. Performance of CoqHammer with and without Lemmas Generated By
Strat2Rocq

                         Claude 3.7 Sonnet             o3-mini
                                 CoqHammer             CoqHammer
                      CoqHammer             CoqHammer
                                +Strat2Rocq           +Strat2Rocq
           CompCert      293    345 (↑ 17.75%)   293     332 (↑ 13.31%)
            Ext-Lib       78     82 (↑ 5.13%)    78       82 (↑ 5.13%)
           Coq-Art       446    501 (↑ 12.33%)   446     504 (↑ 13.00%)
             Vfa         63      70 (↑ 11.11%)   63       69 (↑ 9.52%)
             Total       880    998 (↑ 13.41%)   880     987 (↑ 12.16%)




3.2    RQ2: Does the proof strategies extracted by Strat2Rocq
      enhance the capabilities of symbolic provers?

Procedure. This experiment evaluates the online theorem proving stage (Stage
2, Section 2.3) of Strat2Rocq. We compare the performance of CoqHammer
with and without access to the lemmas mined in the previous research ques-
tion (Section 3.1). We apply the standard 3-fold cross-validation for this evalu-
ation. Specifically, we partition the collected theorems into three disjoint parts
with equal size, and conduct three separate experiments. In the i-th experiment
(1 ≤ i ≤ 3), the i-th part serves as the set of theorems to be proved, while the
remaining two parts serve as the training set.
    For each experiment, we use the default configuration of CoqHammer. Specif-
ically, the timeout is set to 20 seconds, and the number of lemmas retrieved from
the context is fixed at 1024.
Results. The comparison results are presented in Table 2. In terms of the num-
ber of proved theorems, Strat2Rocq achieves an improvement ranging from
5.13% to 17.75% over CoqHammer across different projects. Overall, it proves
13.41% more theorems than CoqHammer.
    Notably, Strat2Rocq achieves its greatest improvement on CompCert, a
real-world certified compiler, demonstrating the effectiveness of Strat2Rocq
in practical Rocq proof engineering.
Case Studies. Below, we present some case studies to have a more fine-grained
understanding of how Strat2Rocq enhances CoqHammer.
    Avoiding Induction. Automated induction remains a long-standing challenge
for symbolic provers [17, 36]. Notably, CoqHammer does not support induction
at all [9]. However, incorporating additional lemmas can help symbolic provers
circumvent the need for induction. Below, we present a concrete example.
    Continuing with our running example (Example 4; see also Figure 1 for de-
tails), the target theorem power_commute_with_x requires induction over n and,
as a result, cannot be proved by CoqHammer. However, by adding the lemma
power_1, the proof can be reduced to the commutativity of natural numbers–an
established result in the Rocq standard library. This avoids the need for induc-
tion and enables CoqHammer to successfully prove the target theorem.
12     J. Fang et al.

    Moreover, upon further inspection of the experimental results, we find that
42.52% of the improvement achieved by Strat2Rocq involves theorems that
were originally proved by the developer using induction.
    More Robust Lemma Selection. The problem of identifying the set of useful
lemmas is another fundamental challenge for symbolic provers [19,27,32]. Under
this context, we also find that Strat2Rocq enhances the robustness of lemma
selection procedure of CoqHammer. Below we present an example.
Theorem target: forall x (i: interval), In x i → ∼empty i.
Here, i is an interval of integers and x is an integer. The theorem asserts that if
there exists a number in the interval, then the interval is non-empty. Although
the context consists of the contrapositive of the target theorem, see the lemma
contra below, CoqHammer does not select this lemma and fails to prove the
target theorem.
Lemma contra: forall x (i: interval), ∼empty i → In x i.
Fortunately, after training Strat2Rocq on contra, it generates an equivalent
form of the lemma contra, as shown in contra_2 below. This lemma is success-
fully selected by CoqHammer, enabling it to prove the target theorem.
Lemma contra_2: forall x (i: interval), empty i → In x i → False.


 Answer to RQ2:
 Strat2Rocq significantly enhances the performance of CoqHammer in
 terms of the number of theorems proved.


3.3   RQ3: Does Strat2Rocq work with other backend LLMs?

Procedure. This experiment aims to understand whether Strat2Rocq is spe-
cific to a particular backend LLM, or can generically extract strategies from
different LLMs. We replace Claude 3.7 Sonnet–the backend LLM originally used
in RQ1 and RQ2–with OpenAI o3-mini [31], and rerun the experiments described
in RQ1 and RQ2.
Results. The results are summarized in Table 1 and Table 2. We observe that
Strat2Rocq remains effective in producing formalized lemmas in Rocq that re-
flect the internal proof strategies of o3-mini. Furthermore, replacing the backend
LLM with o3-mini continues to enhance the proving capability of CoqHammer,
increasing the number of proved theorems by 12.16% and the number of tactics
automated by 26.27%.
     Since the two sets of experiments extract internal strategies from different
LLMs, we are also interested in whether the lemmas extracted from two LLMs
together could further improve the performance. We make a union of the two sets
of lemmas, and evaluate how this set improves CoqHammer. The result shows
that CoqHammer proves 1019 theorems, which is higher than 998 theorems
(from Claude 3.7 Sonnet) and 987 theorems (from o3-mini). This suggests that
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers          13

the internal strategies from different LLMs are not fully overlapped and may
complement each other.

 Answer to RQ3: Strat2Rocq is not specific to a particular backend LLM
 and can extract internal strategies from different backend LLMs.


3.4   RQ4: How does the NL proof generation in Section 2.1
      Contribute to the Effectiveness of Strat2Rocq?

Procedure. This experiment evaluates the impact of the NL proof generation
step (Section 2.1). Instead of using the NL proof generation step, we directly ask
the LLM to generate formalized lemmas.
Results. As shown in Table 3, the result indicate a 63.56% decrease in the
number of extracted lemmas and a 6.21% decrease in performance.


                 Table 3. An ablation study of the extraction method

                           Original                        -NL
                  #Lemmas #Proved Theorems     #Lemmas         #Proved Theorems
       CompCert     1611          345        212 (↓ 86.84%)     308 (↓ 10.72%)
        Ext-Lib      300          82         137 (↓ 54.33%)       78 (↓ 4.88%)
       Coq-Art      2409          501        1263 (↓ 47.57%)     484 (↓ 3.39%)
         Vfa         263          70          58 (↓ 77.95%)       66 (↓ 5.71%)
         Total      4583          998        1670 (↓ 63.56%)     936 (↓ 6.21%)




 Answer to RQ4: The NL proof generation step in Strat2Rocq is essential
 for effectively extracting strategies from LLMs and, in turn, enhancing the
 proving capabilities of CoqHammer.


3.5   RQ5: Can Strat2Rocq enhance the capability of LLM agents?

Currently, many approaches [25, 39, 41] employ LLM agents for automated the-
orem proving, where an agent interacts with LLMs, symbolic provers, and proof
assistants to construct proofs. While our primary objective is to enhance purely
symbolic provers, it is natural to ask whether the lemmas extracted by Strat2Rocq
can also improve the performance of LLM agents.
Procedure. To investigate this, we implement an LLM agent on top of the
agent described in Section 2.4 by incorporating a retrieval-augmented generation
(RAG) module [24]. The RAG module retrieves relevant lemmas from all lemmas
accessible in the current context to assist the LLM in generating proofs. When
the extracted lemmas are inserted into the context, they become available for
retrieval by the RAG module. Furthermore, our agent can also be configured to
14     J. Fang et al.

enable or disable CoqHammer in proof, and will always try CoqHammer first
when it is enabled. We evaluate two settings of the agent:
 – Setting I: The agent has access to the LLM, CoqHammer, and the proof
   assistant. We compare its performance with and without the lemmas mined
   by Strat2Rocq inserted into the context.
 – Setting II: The agent has access to the LLM and the proof assistant only
   (CoqHammer disabled). Again, we compare its performance with and with-
   out the lemmas mined by Strat2Rocq.
   Setting I directly addresses the research question posed in this section, while
Setting II serves as an ablation study that provides a more fine-grained un-
derstanding of the contribution of the extracted lemmas. In both settings, we
evaluate the number of theorems successfully proved and the total number of
tokens consumed. The LLM choice retains the same as Section 3.1.

                        Table 4. Performance of the LLM Agents

                                     LLM Agent
                 LLM Agent                                 LLM Agent
                                    + CoqHammer LLM Agent
                + CoqHammer                               + Strat2Rocq
                                    + Strat2Rocq
     CompCert           502       545 (↑ 8.57%)       363      406 (↑ 11.85%)
      Ext-Lib           104       106 (↑ 1.92%)        76       77 (↑ 1.32%)
     Coq-Art            667       688 (↑ 3.15%)       584       581 (↓ 0.51%)
       Vfa              128       118 (↓ 7.81%)       105      94 (↓ 10.47%)
        Total       1401          1457 (↑ 4.00%)     1128      1158 (↑ 2.65%)
       Tokens    1.379×107     1.298×107 (↓ 5.87%) 1.798×107 1.727×107 (↓ 3.94%)




Results. The results are presented in Table 4. Comparing the column 2 and
column 3, we observe an improvement of 4.00% in Setting I. To understand
why this improvement happens, we can compare the latter two columns, which
show an improvement of 2.65% with LLM proof generation alone in Setting II.
Although these lemmas represent knowledge internal to the LLM, the RAG com-
ponent remains important for surfacing and prioritizing this knowledge during
proof generation of LLM. Notably, the improvement in Setting I exceeds that
of Setting II, indicating that deeper integration between CoqHammer and the
LLM strategies proves lemmas that the agent cannot. This is because, as we
conjecture, LLM only invokes CoqHammer as a blackbox in a standard agent,
but our approach allows to integrate the strategies into the internal proof search
process in CoqHammer.
    We also observe reduced token usage in both settings. This reduction arises
because the enhanced CoqHammer can solve more theorems independently,
thereby decreasing the number of LLM calls required during proof generation.

 Answer to RQ5: Strat2Rocq improves the performance of LLM agents,
 yielding both stronger proving capability and reduced token usage.
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers          15

4   Related Work

Machine Learning for Theorem Proving. There is a long line of research
focused on applying machine learning techniques to theorem proving [4, 5, 11–
13, 19, 20, 25, 27, 32, 35, 37, 39, 41, 44]. These approaches can be divided into two
categories: i) Training a model for theorem proving. ii) Employing an agentic
approach that iteratively generates proofs through interaction with LLMs.
    All of these methods require online interaction with trained models during
the process of proving new theorems, which can be both expensive and insecure,
as discussed in Section 1. In contrast, Strat2Rocq only invokes the symbolic
prover when proving new theorems, making the process secure, cost-effective,
and suitable for execution on a personal computer.
Knowledge Extraction from LLMs. This line of research focuses on extract-
ing the internal knowledge of LLMs into alternative representations. Previous
work in this area has primarily concentrated on extracting LLM knowledge into
knowledge graphs [22, 45].
    However, these approaches are not directly applicable to our setting, as
knowledge graphs capture a set of concepts and their relations, does not rep-
resent the internal proof strategies of LLMs, and is not accessible to symbolic
provers. In contrast, Strat2Rocq extracts the internal proof strategies of LLMs
as verified lemmas in Rocq, making them accessible to CoqHammer.
Symbolic Provers. There have been numerous efforts to develop symbolic
provers for various proof assistants, such as CoqHammer [9] for Rocq [38],
Lean-auto [34] for Lean4 [28], and Sledgehammer [6] for Isabelle [30]. Cur-
rently, Strat2Rocq implements strategy extraction on top of Rocq and has
demonstrated significant improvements over CoqHammer. Our approach can be
adapted to other symbolic provers by translating the formalized theorems from
Rocq to other proof assistants, which we leave as future work.


5   Conclusion and Future Work

In this paper, we explore a new research direction: leveraging the internal knowl-
edge of LLMs to augment symbolic provers. We introduce Strat2Rocq, a
framework that extracts proof strategies from LLMs and formalizes them as lem-
mas in Rocq. Empirical results demonstrate that, on open-source Rocq projects
for software verification, Strat2Rocq increases the success rate of CoqHammer
by 13.41%.
    We would also like to point out that our work is also valuable in under-
standing how LLMs work, a fundamental research question regarding LLMs. A
standard approach towards this question is to build various interpretable sym-
bolic models to approximate the behavior of the LLMs. Our approach provides
a means to approximate an LLM in a symbolic prover. If, with potential future
work, the enhanced symbolic prover could achieve a similar performance with
LLMs, this provides a potential explanation of how LLMs conduct formal proofs.
16      J. Fang et al.

References
 1. Anthropic: Claude 3.7 sonnet and claude code (2025), https://www.anthropic.
    com/news/claude-3-7-sonnet
 2. Appel, A.W.: Verified Functional Algorithms, Software Foundations, vol. 3. Elec-
    tronic textbook (2024)
 3. Bertot, Y., Castéran, P.: Interactive theorem proving and program development:
    Coq’Art: the calculus of inductive constructions. Springer Science & Business Me-
    dia (2013)
 4. Blaauwbroek, L., Olsák, M., Rute, J., Massolo, F.I.S., Piepenbrock, J., Pestun,
    V.: Graph2tac: Online representation learning of formal math concepts. In: Forty-
    first International Conference on Machine Learning, ICML 2024, Vienna, Austria,
    July 21-27, 2024. OpenReview.net (2024), https://openreview.net/forum?id=
    A7CtiozznN
 5. Blaauwbroek, L., Urban, J., Geuvers, H.: The tactician - A seamless, interac-
    tive tactic learner and prover for coq. In: Benzmüller, C., Miller, B.R. (eds.)
    Intelligent Computer Mathematics - 13th International Conference, CICM 2020,
    Bertinoro, Italy, July 26-31, 2020, Proceedings. Lecture Notes in Computer
    Science, vol. 12236, pp. 271–277. Springer (2020). https://doi.org/10.1007/
    978-3-030-53518-6_17, https://doi.org/10.1007/978-3-030-53518-6_17
 6. Böhme, S., Nipkow, T.: Sledgehammer: Judgement day. In: Giesl, J., Hähnle,
    R. (eds.) Automated Reasoning, 5th International Joint Conference, IJCAR
    2010, Edinburgh, UK, July 16-19, 2010. Proceedings. Lecture Notes in Com-
    puter Science, vol. 6173, pp. 107–121. Springer (2010). https://doi.org/10.1007/
    978-3-642-14203-1_9, https://doi.org/10.1007/978-3-642-14203-1_9
 7. Chiusano, P., Bjarnason, R.: Functional Programming in Scala. Manning Publica-
    tions (2014)
 8. Cole, M.: Parallel programming with list homomorphisms. Parallel Processing Let-
    ters 5(2), 191–203 (1995). https://doi.org/10.1142/S0129626495000175
 9. Czajka, L., Kaliszyk, C.: Hammer for coq: Automation for dependent type the-
    ory. J. Autom. Reason. 61(1-4), 423–453 (2018). https://doi.org/10.1007/
    S10817-018-9458-4, https://doi.org/10.1007/s10817-018-9458-4
10. Ericsson, K.A., Kintsch, W.: Long-term working memory. Psychological Review
    102(2), 211–245 (1995)
11. First, E., Brun, Y.: Diversity-driven automated formal verification. In: 44th
    IEEE/ACM 44th International Conference on Software Engineering, ICSE 2022,
    Pittsburgh, PA, USA, May 25-27, 2022. pp. 1–13. ACM (2022). https://doi.org/
    10.1145/3510003.3510138, https://doi.org/10.1145/3510003.3510138
12. First, E., Brun, Y., Guha, A.: Tactok: semantics-aware proof synthesis. Proc. ACM
    Program. Lang. 4(OOPSLA), 231:1–231:31 (2020). https://doi.org/10.1145/
    3428299, https://doi.org/10.1145/3428299
13. First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: Whole-proof generation
    and repair with large language models. In: Chandra, S., Blincoe, K., Tonella,
    P. (eds.) Proceedings of the 31st ACM Joint European Software Engineering
    Conference and Symposium on the Foundations of Software Engineering, ES-
    EC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023. pp. 1229–1241.
    ACM (2023). https://doi.org/10.1145/3611643.3616243, https://doi.org/
    10.1145/3611643.3616243
14. Han, T., Wang, Z., Fang, C., Zhao, S., Ma, S., Chen, Z.: Token-budget-aware llm
    reasoning (2025), https://arxiv.org/abs/2412.18547
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers           17

15. Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng,
    W., Feng, X., Qin, B., Liu, T.: A survey on hallucination in large language mod-
    els: Principles, taxonomy, challenges, and open questions. ACM Trans. Inf. Syst.
    43(2), 42:1–42:55 (2025). https://doi.org/10.1145/3703155, https://doi.org/
    10.1145/3703155
16. Hutton, G.: Higher-order functions for parsing. Journal of functional programming
    2(3), 323–343 (1992)
17. Ireland, A., Bundy, A.: Productive use of failure in inductive proof. Journal of
    automated reasoning 16(1), 79–111 (1996)
18. J, M.R., VM, K., Warrier, H., Gupta, Y.: Fine tuning llm for enterprise: Practical
    guidelines and recommendations (2024), https://arxiv.org/abs/2404.10779
19. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Miłoś, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers. CoRR abs/2205.10893 (2022). https://doi.org/
    10.48550/arXiv.2205.10893, https://arxiv.org/abs/2205.10893
20. Kasibatla, S.R., Agarwal, A., Brun, Y., Lerner, S., Ringer, T., First, E.: Cob-
    blestone: Iterative automation for formal verification. CoRR abs/2410.19940
    (2024). https://doi.org/10.48550/ARXIV.2410.19940, https://doi.org/10.
    48550/arXiv.2410.19940
21. Klein, G., Elphinstone, K., Heiser, G., Andronick, J., Cock, D.A., Derrin, P.,
    Elkaduwe, D., Engelhardt, K., Kolanski, R., Norrish, M., Sewell, T., Tuch, H.,
    Winwood, S.: seL4: formal verification of an os kernel. In: Matthews, J.N., An-
    derson, T.E. (eds.) Proceedings of the 22nd ACM Symposium on Operating
    Systems Principles 2009, SOSP 2009, Big Sky, Montana, USA, October 11-14,
    2009. pp. 207–220. ACM (2009). https://doi.org/10.1145/1629575.1629596,
    https://doi.org/10.1145/1629575.1629596
22. Kommineni, V.K., König-Ries, B., Samuel, S.: From human experts to machines:
    An LLM supported approach to ontology and knowledge graph construction.
    CoRR abs/2403.08345 (2024). https://doi.org/10.48550/ARXIV.2403.08345,
    https://doi.org/10.48550/arXiv.2403.08345
23. Krebbers, R., Leroy, X., Wiedijk, F.: Formal C semantics: Compcert and the C
    standard. In: Klein, G., Gamboa, R. (eds.) Interactive Theorem Proving - 5th In-
    ternational Conference, ITP 2014, Held as Part of the Vienna Summer of Logic,
    VSL 2014, Vienna, Austria, July 14-17, 2014. Proceedings. Lecture Notes in Com-
    puter Science, vol. 8558, pp. 543–548. Springer (2014). https://doi.org/10.1007/
    978-3-319-08970-6_36, https://doi.org/10.1007/978-3-319-08970-6_36
24. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal,
    N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., Kiela,
    D.: Retrieval-augmented generation for knowledge-intensive NLP tasks. In:
    Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M., Lin, H. (eds.) Ad-
    vances in Neural Information Processing Systems 33: Annual Conference on
    Neural Information Processing Systems 2020, NeurIPS 2020, December 6-
    12, 2020, virtual (2020), https://proceedings.neurips.cc/paper/2020/hash/
    6b493230205f780e1bc26945df7481e5-Abstract.html
25. Lu, M., Delaware, B., Zhang, T.: Proof automation with large language
    models. In: Filkov, V., Ray, B., Zhou, M. (eds.) Proceedings of the 39th
    IEEE/ACM International Conference on Automated Software Engineering, ASE
    2024, Sacramento, CA, USA, October 27 - November 1, 2024. pp. 1509–1520.
    ACM (2024). https://doi.org/10.1145/3691620.3695521, https://doi.org/
    10.1145/3691620.3695521
18      J. Fang et al.

26. Malecha, G., Malecha, G., Li, Y.: coq-ext-lib (2024), https://github.com/
    rocq-community/coq-ext-lib
27. Mikuła, M., Tworkowski, S., Antoniak, S., Piotrowski, B., Jiang, A.Q., Zhou, J.P.,
    Szegedy, C., Kuciński, Ł., Miłoś, P., Wu, Y.: Magnushammer: A transformer-based
    approach to premise selection. In: Proceedings of the International Conference
    on Learning Representations (ICLR) (2024), https://openreview.net/forum?id=
    WgaVCqZeIU
28. de Moura, L.M., Kong, S., Avigad, J., van Doorn, F., von Raumer, J.: The lean
    theorem prover (system description). In: Felty, A.P., Middeldorp, A. (eds.) Auto-
    mated Deduction - CADE-25 - 25th International Conference on Automated De-
    duction, Berlin, Germany, August 1-7, 2015, Proceedings. Lecture Notes in Com-
    puter Science, vol. 9195, pp. 378–388. Springer (2015). https://doi.org/10.1007/
    978-3-319-21401-6_26, https://doi.org/10.1007/978-3-319-21401-6_26
29. Newell, A., Simon, H.A.: Human Problem Solving. Prentice-Hall (1972)
30. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL - A Proof Assistant for
    Higher-Order Logic, Lecture Notes in Computer Science, vol. 2283. Springer
    (2002). https://doi.org/10.1007/3-540-45949-9, https://doi.org/10.1007/
    3-540-45949-9
31. OpenAI: Openai o3-mini system card (2025), https://openai.com/index/
    o3-mini-system-card/
32. Proroković, K., Wand, M., Schmidhuber, J.: Improving stateful premise selection
    with transformers. In: Kamareddine, F., Coen, C.S. (eds.) Intelligent Computer
    Mathematics – 14th International Conference (CICM 2021), Lecture Notes in Com-
    puter Science, vol. 12833. pp. 84–89. Springer (2021). https://doi.org/10.1007/
    978-3-030-81097-9_6
33. Protzenko, J., Parno, B., Fromherz, A., Hawblitzel, C., Polubelova, M., Bharga-
    van, K., Beurdouche, B., Choi, J., Delignat-Lavaud, A., Fournet, C., Kulatova,
    N., Ramananandro, T., Rastogi, A., Swamy, N., Wintersteiger, C.M., Zanella-
    Béguelin, S.: Evercrypt: A fast, verified, cross-platform cryptographic provider.
    In: IEEE Symposium on Security and Privacy. IEEE (May 2020), https:
    //www.microsoft.com/en-us/research/publication/evercrypt-a-fast-veri%
    ef%ac%81ed-cross-platform-cryptographic-provider/
34. Qian, Y., Clune, J., Barrett, C., Avigad, J.: Lean-auto: An interface between lean
    4 and automated theorem provers (2025), https://arxiv.org/abs/2505.14929
35. Sanchez-Stern, A., Alhessi, Y., Saul, L.K., Lerner, S.: Generating correctness
    proofs with neural networks. In: Sen, K., Naik, M. (eds.) Proceedings of the
    4th ACM SIGPLAN International Workshop on Machine Learning and Pro-
    gramming Languages, MAPL@PLDI 2020, London, UK, June 15, 2020. pp.
    1–10. ACM (2020). https://doi.org/10.1145/3394450.3397466, https://doi.
    org/10.1145/3394450.3397466
36. Sun, Y., Ji, R., Fang, J., Jiang, X., Chen, M., Xiong, Y.: Proving functional pro-
    gram equivalence via directed lemma synthesis. In: International Symposium on
    Formal Methods. pp. 538–557. Springer (2024)
37. Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., Chaudhuri, S.: An in-context learning
    agent for formal theorem-proving. In: First Conference on Language Modeling
38. The Coq Development Team: The Coq reference manual – release 8.20.0 (2024),
    https://rocq-prover.org/doc/V8.20.0/refman/index.html
39. Thompson, K., Saavedra, N., Carrott, P., Fisher, K., Sanchez-Stern, A., Brun,
    Y., Ferreira, J.F., Lerner, S., First, E.: Rango: Adaptive retrieval-augmented
      Proof Strategy Extraction from LLMs for Enhancing Symbolic Provers            19

    proving for automated software verification. In: 2025 IEEE/ACM 47th Interna-
    tional Conference on Software Engineering (ICSE). pp. 347–359 (2025). https:
    //doi.org/10.1109/ICSE55347.2025.00161
40. Vazou, N., Lampropoulos, L., Polakow, J.: A tale of two provers: verifying monoidal
    string matching in liquid haskell and coq. In: Proceedings of the 10th ACM SIG-
    PLAN International Symposium on Haskell. p. 63–74. Haskell 2017, Association for
    Computing Machinery, New York, NY, USA (2017). https://doi.org/10.1145/
    3122955.3122963, https://doi.org/10.1145/3122955.3122963
41. Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang, Y., Xiong, J., Shi, H., Xie,
    E., Yin, J., Li, Z., Liang, X.: Lego-prover: Neural theorem proving with growing
    libraries. In: The Twelfth International Conference on Learning Representations,
    ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net (2024), https:
    //openreview.net/forum?id=3f5PALef5B
42. Weng, K., Du, L., Li, S., Lu, W., Sun, H., Liu, H., Zhang, T.: Autoformalization
    in the era of large language models: A survey (2025), https://arxiv.org/abs/
    2505.23486
43. Wu, Y., Jiang, A.Q., Li, W., Rabe, M.N., Staats, C., Jamnik, M., Szegedy, C.:
    Autoformalization with large language models. In: Proceedings of the 36th Inter-
    national Conference on Neural Information Processing Systems. NIPS ’22, Curran
    Associates Inc., Red Hook, NY, USA (2022)
44. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assis-
    tants. In: Chaudhuri, K., Salakhutdinov, R. (eds.) Proceedings of the 36th In-
    ternational Conference on Machine Learning, ICML 2019, 9-15 June 2019, Long
    Beach, California, USA. Proceedings of Machine Learning Research, vol. 97, pp.
    6984–6994. PMLR (2019), http://proceedings.mlr.press/v97/yang19a.html
45. Zhang, B., Soh, H.: Extract, define, canonicalize: An llm-based framework for
    knowledge graph construction. In: Al-Onaizan, Y., Bansal, M., Chen, Y. (eds.)
    Proceedings of the 2024 Conference on Empirical Methods in Natural Language
    Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024. pp. 9820–
    9836. Association for Computational Linguistics (2024), https://aclanthology.
    org/2024.emnlp-main.548
