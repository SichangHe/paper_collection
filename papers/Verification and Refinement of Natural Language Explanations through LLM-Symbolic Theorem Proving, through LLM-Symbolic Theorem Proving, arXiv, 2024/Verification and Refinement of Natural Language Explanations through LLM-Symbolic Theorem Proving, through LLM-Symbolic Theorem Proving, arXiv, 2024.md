                                                  Verification and Refinement of Natural Language Explanations
                                                             through LLM-Symbolic Theorem Proving
                                                        Xin Quan1 , Marco Valentino2 , Louise A. Dennis1 , André Freitas1,2,3
                                                           1
                                                             Department of Computer Science, University of Manchester, UK
                                                                         2
                                                                           Idiap Research Institute, Switzerland
                                                        3
                                                          National Biomarker Centre, CRUK-MI, University of Manchester, UK
                                                                       1
                                                                         {name.surname}@manchester.ac.uk
                                                                              2
                                                                                {name.surname}@idiap.ch

                                                                 Abstract                                 ity (Camburu et al., 2020; Wiegreffe and Maraso-
                                                                                                          vic, 2021; Valentino et al., 2021; Atanasova et al.,
                                             Natural language explanations represent a                    2023; Quan et al., 2024; Dalal et al., 2024), includ-
                                             proxy for evaluating explanation-based and
                                                                                                          ing the adoption of language generation metrics
                                             multi-step Natural Language Inference (NLI)
arXiv:2405.01379v4 [cs.CL] 11 Oct 2024




                                             models. However, assessing the validity of ex-
                                                                                                          for a direct comparison between models’ generated
                                             planations for NLI is challenging as it typi-                explanations and human-annotated explanations.
                                             cally involves the crowd-sourcing of apposite                   However, this process is subject to different
                                             datasets, a process that is time-consuming and               types of limitations. First, the use of language
                                             prone to logical errors. To address existing lim-            generation metrics requires the crowd-sourcing
                                             itations, this paper investigates the verification
                                                                                                          of explanation corpora to augment existing NLI
                                             and refinement of natural language explana-
                                             tions through the integration of Large Language              datasets (Wiegreffe and Marasovic, 2021), a pro-
                                             Models (LLMs) and Theorem Provers (TPs).                     cess that is time-consuming and susceptible to er-
                                             Specifically, we present a neuro-symbolic                    rors (Valentino et al., 2021; Liu et al., 2022; Zhao
                                             framework, named Explanation-Refiner, that                   et al., 2023). Second, language generation metrics
                                             integrates TPs with LLMs to generate and for-                have been shown to fail capturing fine-grained prop-
                                             malise explanatory sentences and suggest po-                 erties that are fundamental for NLI such as logical
                                             tential inference strategies for NLI. In turn,               reasoning, faithfulness, and robustness (Camburu
                                             the TP is employed to provide formal guaran-
                                                                                                          et al., 2020; Chan et al., 2022; Atanasova et al.,
                                             tees on the logical validity of the explanations
                                             and to generate feedback for subsequent im-                  2023; Quan et al., 2024). Third, human explana-
                                             provements. We demonstrate how Explanation-                  tions in NLI datasets tend to be incomplete and
                                             Refiner can be jointly used to evaluate explana-             contain logical errors that could heavily bias the
                                             tory reasoning, autoformalisation, and error cor-            evaluation (Elazar et al., 2021; Valentino et al.,
                                             rection mechanisms of state-of-the-art LLMs                  2021).
                                             as well as to automatically enhance the qual-
                                             ity of explanations of variable complexity in
                                                                                                             In this paper, we investigate the integration of
                                             different domains.1                                          state-of-the-art LLM-based explanation generation
                                                                                                          models for NLI with external logical solvers to
                                         1    Introduction                                                jointly evaluate explanatory reasoning (Pan et al.,
                                                                                                          2023a; Olausson et al., 2023; Jiang et al., 2024b)
                                         A recent line of research in Natural Language Infer-             and enhance the quality of crowd-sourced explana-
                                         ence (NLI) focuses on developing models capable                  tions. In particular, we present a neuro-symbolic
                                         of generating natural language explanations in sup-              framework, named Explanation-Refiner, that in-
                                         port of their predictions (Thayaparan et al., 2021;              tegrates a Theorem Prover (TP) with Large Lan-
                                         Chen et al., 2021; Valentino et al., 2022a; Bostrom              guage Models (LLMs) to investigate the following
                                         et al., 2022; Weir et al., 2023). Since natural lan-             research questions: RQ1: “Can the integration of
                                         guage explanations can be used as a proxy to evalu-              LLMs and TPs provide a mechanism for automatic
                                         ate the underlying reasoning process of NLI models               verification and refinement of natural language ex-
                                         (Kumar and Talukdar, 2020; Zhao and Vydiswaran,                  planations?”; RQ2: “Can the integration of LLMs
                                         2021; Chen et al., 2021), researchers have proposed              and TPs improve the logical validity of human-
                                         different methods for assessing their intrinsic qual-            annotated explanations?”; RQ3: “To what extent
                                            1
                                              Code and data are available at: https://github.com/neuro-   are state-of-the-art LLMs capable of explanatory
                                         symbolic-ai/explanation_refinement                               reasoning, autoformalisation, and error correction
for NLI in different domains?”. To answer these               to minimise semantic information loss. Ad-
questions, Explanation-Refiner employs LLMs to                ditionally, we introduce a novel method that
generate and formalise explanatory sentences and              leverages a theorem prover and a proof as-
to suggest potential inference strategies for build-          sistant for verifying NLI explanations and a
ing non-redundant, complete, and logically valid              syntactic refiner to minimise syntax errors in
explanations for NLI. In turn, the TP is adopted to           responses generated by LLMs.
verify the validity of the explanations through the
construction of deductive proofs and the generation        3. We conduct a comprehensive series of exper-
of fine-grained feedback for LLMs.                            iments with Explanation-Refiner across five
                                                              LLMs and three datasets, including 1 to 16
   We instantiate Explanation-Refiner with state-of-
                                                              explanatory sentences, covering tasks from
the-art LLMs (i.e., GPT-4 (OpenAI, 2023), GPT-
                                                              textual entailment to complex multiple-choice
3.5 (Brown et al., 2020), LLama (Touvron et al.,
                                                              question answering in various domains.
2023), and Mistral (Jiang et al., 2024a)) and the
Isabelle/HOL proof assistant (Nipkow et al., 2002)         4. We perform extensive analyses to explore the
utilising Neo-Davidsonian event semantics (Par-               explanation refinement process, characteris-
sons, 1990) coupled with First-Order Logic (FOL)              ing the LLMs’ inference capabilities and re-
to effectively and systematically translate natural           vealing the strengths and limitations of differ-
language sentences into logical forms.                        ent models in producing verifiable, explain-
   Our empirical analysis, carried out on three NLI           able logical reasoning for NLI.
datasets of variable complexity (i.e., e-SNLI (Cam-
buru et al., 2018), QASC (Khot et al., 2019), and      2     Explanation Verification and
WorldTree (Jansen et al., 2018)), reveals that ex-           Refinement
ternal feedback from TPs is effective in improv-
                                                       Explanation-based NLI is widely adopted to eval-
ing the quality of natural language explanations,
                                                       uate the reasoning process of multi-step inference
leading to an increase in logical validity using
                                                       models via the construction of natural language
GPT-4 from 36% to 84%, 12% to 55%, and 2%
                                                       explanations. In this work, we refer to the fol-
to 37% (on e-SNLI, QASC, and WorldTree respec-
                                                       lowing formalisation for Explanation-based NLI:
tively). At the same time, the results demonstrate
                                                       given a premise sentence pi , a hypothesis sentence
that integrating external TPs with LLMs can re-
                                                       hi , and an explanation Ei consisting of a set of
duce errors in autoformalisation, with an average
                                                       facts {f1 , f2 , ..., fn }, the explanation Ei is logi-
reduction of syntax errors of 68.67%, 62.31%, and
                                                       cally valid if and only if the entailment pi ∪Ei |= hi
55.17%. Finally, we found notable differences in
                                                       holds. This entailment is considered verifiable if
performance across LLMs and NLI datasets, with
                                                       {pi , Ei , hi } can be translated into a set of logical
closed-sourced LLMs (i.e., GPT-4 and GPT-3.5)
                                                       formulae Φ that compose a theory Θ. The validity
significantly outperforming open-source models
                                                       of the theory Θ is subsequently determined by a
(i.e., Mistral and LLama) on both explanatory rea-
                                                       theorem prover, verifying whether Θ ⊨ ψ, where
soning and autoformalisation, along with a shared
                                                       ψ represents a logical consequence derived from
tendency of LLMs to struggle with increasing ex-
                                                       the logical form of hi .
planation complexity.
                                                          In this paper, we aim to automatically verify the
   To summarise, the main contributions of this
                                                       logical validity of an explanation Ei . To this end, if
paper are:
                                                       Θ ⊨ ψ is rejected by the theorem prover, a further
                                                       refinement stage should be initiated to refine the
  1. We introduce Explanation-Refiner, a novel
                                                       facts {f1 , f2 , ..., fn } based on external feedback,
     neuro-symbolic framework that integrates
                                                       resulting in an updated explanation Ei′ . Thus, an
     LLMs with an external theorem prover. This
                                                       explanation is accepted if all the facts are logically
     framework automatically verifies and refines
                                                       consistent, complementary and non-redundant to
     explanatory sentences in NLI tasks using an
                                                       support the derivation.
     objective external feedback.
                                                       3     Explanation-Refiner
  2. We integrate Neo-Davidsonian event seman-
     tics coupled with FOL to effectively translate    To verify the logical validity and refine any logical
     natural language sentences into logical forms     errors in explanatory sentences for NLI tasks, we
                                                                       (a) Axiomatisation and Theoremisation
    Premise: A man gives a speech
    at an ornate costume party.                                                       axiom_1: "∀x y e1 e2. Someone x ∧ Speech y ∧ Gives
                                                         Autoformalisation                                                                                       Refine
                                                                                      e1 ∧ Agent e1 x ∧ Patient e1 y ⟶ Speaking e2 ∧ Agent
                                                                                                                                                                 Syntax
                                                                                      e2 x"                                                                                      LLM
    Hypothesis: A man is public
                                                                 LLM
    speaking.
                                                                                                                                                            Step (2)
                                                                                      Theorem hypothesis:
                                                      Step (1)                        assumes asm: "Man x ∧ Speech y ∧ Party z ∧ Ornate z ∧                       Theorem
    Initial Explanation:                                                              Costume z ∧ Gives e ∧ Agent e x ∧ Patient e y ∧ At x z"                      Prover           Syntax Error
    If someone gives a speech that                                                    shows "∃x e. Man x ∧ Speaking e ∧ Agent e x"
     means that they are speaking.
                                                                                               Neo-Davidsonian Event Semantics                                             No Syntax Error


                                            New                    (b) Inference, Verification and Refinement
                                          Iteration
                                                                                        Theorem                       Isabelle                        Rough
     Refined Explanation:                                                                                                                            Inference       LLM         Step (3)
                                                                                         Prover                        Theory
     If a man gives a speech, that
     means he is public speaking.                                                                            Construct the theory with
                                                                  Step (5)     Verification
                                                                                                               formalised axioms,
                                                                                                           theorems and proof methods
                                                                                                                                                1. To infer the hypothesis, we need to find the
                                                       proof -                                                                                     information of a man and the action of
                  LLM        Step (6)                 from asm have "Man x ∧ Speech y ∧ Gives                                                      public speaking.
                                                      e ∧ Agent e x ∧ Patient e y" by blast                                                     ....
                                                      then have "Man x ∧ Speaking e ∧ Agent e                                                   5. By combining these steps, we can infer the
                        Drop irrelevant facts and     x" using explanation_1 by blast                                                                hypothesis by satisfying the information of
                                                                                                                        LLM
                      Refine based on the feedback    then show ?thesis using asm by blast                                                           man (from premise) and public speaking
                         from the theorem prover   qed                                                                                             (from premise and explanation 1).
                                                                                                                   Autoformalise
                                                                                        Solvable                                                There are no redundant or not directly related
                                                                                                                   Proof Methods
                                        Unsolvable. Feedback on                                                                                 explanation sentences. The proof steps use
    Failed at then have "Man x ∧              invalid steps                                                                   Step (4)          explanation 1 and the premise sentence.
    Speaking e ∧ Agent e x" using
    explanation_1 by blast                                                    Valid Explanation
                                                                                                                                                                               Proof Strategy




Figure 1: The overall pipeline of Explanation-Refiner: An NLI problem is converted into axioms and theorems for a
theorem prover, along with some proof steps derived from a preliminary inference. In case the proof fails (logically
invalid), the erroneous steps along with the constructed proof strategy are used as feedback to refine the explanation
in a new iteration.


present a neuro-symbolic framework that iteratively                                                preliminary proof strategy, the LLM is prompted to
checks and refines the explanation Ei based on ex-                                                 construct and formalise the proof steps for proving
ternal feedback. Figure 1 shows an overview of our                                                 the theorem. In step 5, the theorem prover will ver-
proposed framework. Given an NLI task, to evalu-                                                   ify the constructed theory by attempting to prove
ate the logical validity of the entailment, the LLM                                                the theorem. If it is solvable, we consider it a logi-
is prompted to perform an autoformalisation pro-                                                   cally valid explanation. If the prover failed at one
cess that transforms natural language sentences into                                               of the proof steps, we adopt the failed steps along
formal language represented in the form of an Is-                                                  with the applied axioms B ⊆ A as an external feed-
abelle/HOL theory. Each fact f ∈ Ei is converted                                                   back for the LLM. This feedback is used to refine
into an axiom ai , where each ai is an element of                                                  the logical errors and consequently refine the facts
the set A = {a1 , a2 , ..., an }. The premise pi and                                               f ∈ Ei .
corresponding hypothesis hi , is converted into a
theorem for proving pi ∧ B → hi , where B ⊆ A.                                                     3.1        Autoformalisation
A syntax refinement mechanism is subsequently ap-                                                  In order to formally verify the logical validity of the
plied to the previously transferred symbolic forms.                                                explanations, we adopted Neo-Davidsonian event-
The theorem prover is implemented as a checker to                                                  based semantics and FOL.
identify any syntax errors and provide these error
details as feedback to an LLM, enabling the LLM                                                    Neo-Davidsonian Event Semantics Preventing
to iteratively correct the syntax errors over a fixed                                              the loss of semantic information during the repre-
number of iterations, denoted by t.                                                                sentation of natural language sentences in logical
                                                                                                   forms, such as FOL, poses significant challenges
   We can then perform automated reasoning via                                                     when using LLMs, particularly with long and com-
the theorem prover. To this end, in step 3 we use                                                  plex sentences that are crucial for logical reasoning
the LLM to generate a rough inference that states a                                                (Olausson et al., 2023). Neo-Davidsonian event se-
preliminary proof strategy in natural language and                                                 mantics (Parsons, 1990) focused on event variables
elicit the facts f ∈ Ei which are sufficient and nec-                                              to represent the verb predicates and their corre-
essary for entailing the hypothesis hi . Based on this                                             sponding object arguments as semantic roles. This
theorem hypothesis:
  (* Premise: A smiling woman is playing the violin in front of a turquoise background. *)
  assumes asm: "Woman x ∧ Violin y ∧ Background z ∧ Turquoise z ∧ Smiling x ∧ Playing e ∧ Agent e
    x ∧ Patient e y ∧ InFrontOf x z"
  (* Hypothesis: A woman is playing an instrument. *)
  shows "∃ x y e. Woman x ∧ Instrument y ∧ Playing e ∧ Agent e x ∧ Patient e y"
proof -
  from asm have "Woman x ∧ Violin y ∧ Playing e ∧ Agent e x ∧ Patient e y" by blast
  then have "Woman x ∧ Instrument y ∧ Playing e ∧ Agent e x ∧ Patient e y" using explanation_1 by
    blast
  then show ?thesis using asm by blast
qed


Figure 2: An example of representing the premise and hypothesis sentences in Isabelle/HOL theorem includes a
proof constructed by the LLM for verifying the hypothesis.


approach establishes a predicate-argument struc-
                                                         (* Explanation 1: A violin is an instrument. *)
ture that preserves the information content and          axiomatization where
faithfulness of complex sentences, closer to the           explanation_1: "∀x. Violin x −→ Instrument x"
surface form of the sentence (Quan et al., 2024).
For example, the sentence ‘A wolf eating a sheep         In addition, as illustrated in Figure 2, both the
is an example of a predator hunting prey’ can be         premise and the hypothesis constitute parts of the
formalised as follows:                                   theorem to be proven. In particular, the ‘assumes
                                                         asm’ clause includes unquantified, specific propo-
   ∀xye1 (wolf(x) ∧ sheep(y) ∧ eating(e1 )               sitions or conjunctions of propositions which are
       ∧ agent(e1 , x) ∧ patient(e1 , y) →               recognised as known truths (i.e., premises). On the
                                                         other hand, the ‘show’ clause denotes the conclu-
      (∃e2 predator(x) ∧ prey(y)∧                 (1)
                                                         sion (i.e., hypothesis) for which we seek to build
      hunting(e2 ) ∧ agent(e2 , x)∧                      a proof through logical deductions based on the
      patient(e2 , y) ∧ example(e1 , e2 )))              assumed propositions and axioms.

In 1, the verbs are represented as the events ‘eating’   Syntax Error Refiner Recent studies (Olausson
and ‘hunting,’ where the agent and patient argu-         et al., 2023; Gou et al., 2024) have revealed per-
ments correspond to the entities performing and          sistent syntax errors when prompting LLMs for
receiving the actions within these events, respec-       code and symbolic form generation tasks. We cat-
tively. The logical form example(e1 , e2 ) explicitly    egorised the syntax errors into two distinct sub-
captures the semantic meaning of this sentence: the      domains based on feedback from Isabelle: type
event of a wolf eating a sheep as an exemplar of a       unification errors and other syntax errors. Type
predator hunting prey. Similarly, whenever there         unification errors primarily arise from mismatches
are no action verbs involved in a sentence, we use       between declared and actual argument types in log-
FOL to represent the static or descriptive aspects.      ical clauses. Other syntax errors typically involve
For instance:                                            missing brackets, undefined entity names, or in-
                                                         valid logical symbols. Our process involves using
        ∀x(gravity(x) → force(x))                 (2)    Isabelle to identify syntax errors in the transferred
        ∀xy(greater(x, y) → larger(x, y))         (3)    theory, extracting these error messages, and then
                                                         prompting the LLM with these messages along
   The above logical forms correspond to the sen-        with few-shot examples. This guides the model
tences ‘gravity is a kind of force’ and ‘greater         on how to correct each type of syntax error over a
means larger’.                                           series of iterations, allowing for continuous verifi-
                                                         cation and refinement. Details of the autoformali-
Isabelle/HOL Theory Construction A theory                sation prompts are described in Appendix A.4.1.
script for the Isabelle/HOL theorem prover contains
theorems that need to be proven from some axioms.        3.2   Proof Construction
Therefore, we adopt the sentences in an explanation      A proof provides a detailed step-by-step strategy
to construct the set of axioms. For instance:            that elucidates the logical connections and unifica-
tion among axioms to support the reasoning process        syntactic and semantic features expressed in the
aimed at achieving the solver’s goal. Initially, we       datasets. For multiple-choice question answering,
prompt the LLM to create a preliminary proof in           the task includes a question q accompanied by a set
natural language to assess how it infers the hypoth-      of candidate answers C = {c1 , c2 , ..., cn }, with ci
esis and to identify which explanatory sentences          identified as the correct answer. To cast this prob-
are relevant, redundant, or unrelated. Based on           lem into NLI, we simply convert q and the correct
this initial inference, we then guide the LLM to de-      answer ci into a hypothesis hi . On the other hand,
velop a formal proof (Figure 2) that integrates with      the question’s context, if present, is used to build
Isabelle/HOL to verify the explanatory sentences          the premise pi .
(axioms) that are required to derive the hypothe-
sis. The general proof steps generated by an LLM          4.2   Models
are in the format ’show X using Y by Z’, where            To integrate Isabelle/HOL as a real-time verifica-
the theorem prover is asked to prove X given the          tion tool with LLMs, we employ a Python client
assumptions Y , using the automated proof tactic          (Shminke, 2022) which communicates with Is-
Z. The proof tactic often applied is ’blast’, which       abelle/HOL as a server backend. This enables the
is one of broader Isabelle’s FOL theorem proving          communication of the constructed theory files and
tactics(Paulson, 1999). Additional details of the         the extraction of the response messages from Is-
proof construction process and the prompts used to        abelle. We conducted experiments using five LLMs
guide the LLMs are described in Appendix A.4.2.           within the proposed framework. The models in-
                                                          clude two open-sourced models: Llama2-70b (Tou-
3.3    Verification and Refinement                        vron et al., 2023) and Mixtral-8x7b (Jiang et al.,
Finally, the constructed theory, which includes ax-       2024a), as well as Mistral-small (mistral-small-
ioms, theorems, and proof steps, is submitted to          latest) (Mistral AI, 2024), GPT-3.5 (gpt-3.5-turbo)
the theorem prover for verification. If the theory is     (Brown et al., 2020), and GPT-4 (gpt-4-0613) (Ope-
validated, it outputs a logically valid explanation.      nAI, 2023).
If the proof fails or timeouts, we extract the first
                                                          4.3   Results
error from the solver’s error message, identify the
corresponding proof step, and locate the related ex-      Detailed feedback from an external theorem
planatory sentences (axioms) from the theory. We          prover effectively guides LLMs in verifying and
begin by removing redundant and irrelevant facts          refining explanations for NLI. To assess the
that are not present in the preceding Isabelle/HOL        effectiveness of employing an external theorem
proof steps or are declared as such in the text infer-    prover to verify and refine explanations in NLI
ence strategy. Then, we prompt the LLM to refine          tasks, we conducted a comparative analysis across
the explanatory sentences by providing it with the        various LLMs (Figure 3). The initially valid ex-
error message, the failed proof step, the associated      planations represent the percentage of explanations
proof strategy, and the relevant explanatory sen-         that can be verified as logically valid without any
tences for further iteration. This process is iterative   further iteration. Although the initial verification
and progressive; with each iteration, the framework       results varied among different models, all LLMs
addresses one or more logical errors, continually re-     demonstrated a consistent improvement in refining
fining the explanatory sentences to ultimately yield      the logical validity of the explanations. This pro-
a logically valid and verifiable explanation. Addi-       cess highlights the positive impact of the external
tional details on the prompts used for refinement         feedback but also shows significant differences be-
are described in Appendix A.4.3.                          tween models. We found that lower rates of initial
                                                          valid explanations often resulted from syntactic er-
4     Empirical Evaluation                                rors, which impeded the theorem prover’s ability
                                                          to generate proofs. Despite this initial variability,
4.1    Datasets                                           all models demonstrate a consistent improvement
We adopted three different NLI datasets for evalua-       in the refinement process across the datasets. No-
tion: e-SNLI, QASC, and WorldTree, using a total          tably, GPT-4 outperformed other models, improv-
of 300 samples selected via the sampling strategy         ing the validity of explanations by 48%, 43%, and
defined in Valentino et al. (2021), which maximises       35% across the three datasets, respectively, within
representativeness and mutual exclusivity across          a maximum number of ten iterations (Figure 3).
                                                                           e-SNLI                                                                                                                                          QASC                                                                                                                                                           WorldTree
                            100                                                                                      10                                                 100                                                                                                       10                                                 100                                                                                                          10
 Number of Valid Explanations




                                                                                                                                             Number of Valid Explanations




                                                                                                                                                                                                                                                                                                          Number of Valid Explanations
                                                Initially Valid Explanations                                                                                                                 Initially Valid Explanations                                                                                                                                Initially Valid Explanations
                                                Finally Valid Explanations                                84.0                                                                               Finally Valid Explanations                                                                                                                                  Finally Valid Explanations




                                                                                                                     Number of Iterations




                                                                                                                                                                                                                                                                                  Number of Iterations




                                                                                                                                                                                                                                                                                                                                                                                                                                                  Number of Iterations
                                 80             Number of Iterations                                                 8                                                       80              Number of Iterations                                                                 8                                                       80             Number of Iterations                                                                     8

                                                    6.0
                                 60                                                          55.0                    6                                                       60                                                                                        55.0       6                                                       60                                        5.5                                5.38
                                                                                                                                                                                                                                                                                                                                                                                                                                                  6
                                                                                                                                                                                                                                        4.8                                                                                                                                                             4.6
                                                                                                                                                                                                                                                      44.0                                                                                                                                                                                 4.41
                                                                                                                                                                                                                                                          4.11
                                 40                                            36.0                    36.0          4                                                       40                  3.6                3.58                                                   3.55   4                                                       40                 3.33
                                                                                                                                                                                                                                                                                                                                                                                                                                       37.0       4
                                                                32.03.28
                                                                                                2.93                                                                                                                                                                                                                                                                                                                29.0
                                                                                                                                                                                          25.0
                                                                           22.0                               1.96
                                 20                                                      19.0                        2                                                       20                                                                                                   2                                                       20                                                                                                      2
                                                             16.0                 1.58                                                                                                                                           15.0
                                                                                                                                                                                                                 12.0                                               12.0
                                              7.0                                                                                                                                                                                               6.0                                                                                                                           6.0                 5.0
                                                                                                                                                                                    3.0                    3.0                                                                                                                                         3.0              1.0                                                      2.0
                                        0.0                                                                                                                                                                                0.0                                                                                                                   0.0                                        0.0               0.0
                                  0                                                                                  0                                                        0                                                                                                   0                                                        0                                                                                                      0
                                      Llama2-70b Mixtral-8x7bMistral-small GPT-3.5                      GPT-4                                                                     Llama2-70b Mixtral-8x7bMistral-small GPT-3.5                                       GPT-4                                                                     Llama2-70b Mixtral-8x7bMistral-small GPT-3.5                                      GPT-4

                                                                           (a)                                                                                                                                             (b)                                                                                                                                                              (c)

        Figure 3: The initial and final number of logically valid explanations, along with the average iteration times required
        to refine an explanation for each LLM

                                100                                            e-SNLI                                                                                       100                                                QASC                                                                                                      100                                               WorldTree
Number of Refined Explanations




                                                                                                                                            Number of Refined Explanations




                                                                                                                                                                                                                                                                                                         Number of Refined Explanations
                                                          Mixtral-8x7b                                                                                                                                                                                           Mixtral-8x7b                                                                                                                                                 Mixtral-8x7b
                                                          Mistral-small                                                                                                                                                                                          Mistral-small                                                                                                                                                Mistral-small
                                 80                       GPT-3.5                                                                                                            80                                                                                  GPT-3.5                                                                  80                                                                                  GPT-3.5
                                                          GPT-4                                                                                                                                                                                                  GPT-4                                                                                                                                                        GPT-4
                                 60                       Llama2-70b                                                                                                         60                                                                                  Llama2-70b                                                               60                                                                                  Llama2-70b

                                 40                                                                                                                                          40                                                                                                                                                           40

                                 20                                                                                                                                          20                                                                                                                                                           20

                                  00                        2              4             6              8                   10                                                00                       2                   4                    6                    8                   10                                                00                       2                      4                  6                   8                      10
                                                                      Iteration Times                                                                                                                                   Iteration Times                                                                                                                                               Iteration Times
                                                                           (a)                                                                                                                                             (b)                                                                                                                                                              (c)

                                                                                      Figure 4: Number of successfully refined explanations at each iteration step.


      Figure 4 shows the number of explanations refined                                                                                                                                                                                       Iterative and categorical refinement can mono-
      at each iteration across the e-SNLI, QASC, and                                                                                                                                                                                          tonically reduce syntactic errors in autoformal-
      WorldTree datasets. On average, we found that an                                                                                                                                                                                        isation. To evaluate the syntax error refinement
      increasing number of iterations leads to increasing                                                                                                                                                                                     stage, we quantified the presence of syntax errors
      refinement, with models requiring an average of                                                                                                                                                                                         in the Isabelle theories both before and after the
      five iterations across the datasets.                                                                                                                                                                                                    iterative refinement process. After a maximum
                                                                                                                                                                                                                                              of three iterations, all models showed significant
                                                                                                                                                                                                                                              reductions, with maximum reductions of 68.67%,
      Explanation length/complexity impacts formal-                                                                                                                                                                                           62.31%, and 55.17% from 7.82 to 2.45, 20.27 to
      isation and verification. The e-SNLI dataset,                                                                                                                                                                                           7.64, and 22.91 to 10.27 across the three respec-
      which includes only a single explanatory sentence                                                                                                                                                                                       tive datasets (see Figure 5). While models like
      per example, shows the best overall performance.                                                                                                                                                                                        Llama2-70b and Mixtral-8x7b still exhibit some
      In contrast, the multiple-choice question answering                                                                                                                                                                                     syntax errors in the refined theories’ code, this is
      datasets, QASC and WorldTree, exhibit compara-                                                                                                                                                                                          primarily due to their inability to perform complex
      tively lower performance. QASC typically contains                                                                                                                                                                                       autoformalisation, especially for multiple and more
      2 explanatory sentences, while WorldTree ranges                                                                                                                                                                                         complex explanatory sentences such as those in the
      from 1 to 16 sentences. As the number of explana-                                                                                                                                                                                       WorldTree dataset. This result is consistent with
      tory sentences increases, so does the complexity of                                                                                                                                                                                     the percentage of explanations that were success-
      the logical reasoning required. Models show lower                                                                                                                                                                                       fully refined across the models, which suggests that
      refinement performance in WorldTree when com-                                                                                                                                                                                           the autoformalisation process plays a critical role
      pared to e-SNLI and QASC, with only 3%, 5%, and                                                                                                                                                                                         in the models’ logical reasoning capability.
      5% of Llama-70b, Mixtral-8x7b, and Mistral-small
      explanations being refined in WorldTree. Mean-                                                                                                                                                                                          4.4                Ablation Study
      while, 29% and 35% of explanations are refined                                                                                                                                                                                          We conducted an ablation study to further evaluate
      by GPT-3.5 and GPT-4 in WorldTree, respectively.                                                                                                                                                                                        and disentangle the impact of autoformalisation on
      This process involves synthesising multiple ex-                                                                                                                                                                                         performance. To this end, we adopted GPT-4 exclu-
      planatory sentences to fulfill sub-goals, which must                                                                                                                                                                                    sively for the autoformalisation component, while
      then be integrated to meet the overall hypothesis                                                                                                                                                                                       retaining the original models for explanation refine-
      goal.                                                                                                                                                                                                                                   ment and proof strategy generation. As shown in
   Avg. Number of Theories Contain Syntax Errors                                       e-SNLI                                                                                                                           QASC                                                                                                                            WorldTree




                                                                                                                                     Avg. Number of Theories Contain Syntax Errors




                                                                                                                                                                                                                                                                        Avg. Number of Theories Contain Syntax Errors
                                                   100                                                                                                                               100                                                                                                                                100

                                                   80    75.18                                                                                                                       80                                                                                                                                 80
                                                                                                                                                                                                                                                                                                                                           68.45
                                                                64.55                                                                                                                                                                                                                                                                                      63.63        61.73
                                                   60                   58.55                                                                                                        60                   54.45                                                                                                         60    51.27               53.72         54.27
                                                                                        47.0                                                                                               50.18                         50.36
                                                                                                                                                                                                                                       46.1
                                                                                                                                                                                                                41.45                                                                                                              41.27
                                                   40                          31.82                  33.27                                                                          40                                        38.27                                                                                    40                                                    35.64
                                                                                               23.0                                                                                               25.64                                                                                                                                                                                22.91
                                                                                                                                                                                                                                              22.18   20.27
                                                   20                                                       17.64                                                                    20                                                                                                                                 20
                                                                                                                    7.82                                                                                                                                      7.64                                                                                                                         10.27
                                                                                                                           2.45
                                                    0    Llama2-70b Mixtral-8x7b Mistral-small         GPT-3.5       GPT-4                                                            0    Llama2-70b Mixtral-8x7b Mistral-small       GPT-3.5          GPT-4                                                            0    Llama2-70b Mixtral-8x7b Mistral-small      GPT-3.5         GPT-4

                                                                                       (a)                                                                                                                              (b)                                                                                                                               (c)

          Figure 5: The average number of theories containing syntactic errors before and after the syntax refinement process

                                                                                       e-SNLI                                                                                                                            QASC                                                                                                                           WorldTree
Number of Refined Explanations




                                                                                                                                  Number of Refined Explanations




                                                                                                                                                                                                                                                                     Number of Refined Explanations
                                                   100                                                                                                                               100                                                                                                                                100
                                                                 TI+AF(Base model)                                                                                                                                                            TI+AF(Base model)                                                                                                                 TI+AF(Base model)
                                                                 TI+AF(GPT-4)                                       84 84                                                                                                                     TI+AF(GPT-4)                                                                                                                      TI+AF(GPT-4)
                                                    80                                                        74                                                                      80                                                                                                                                 80
                                                                                67              69
                                                                  65
                                                    60                                                 55                                                                             60                                                               55 55                                                             60
                                                                                                                                                                                                                                 45            48
                                                                                                                                                                                                    42            44                    44
                                                    40                    32
                                                                                         36                                                                                           40                                                                                                                                 40                                      31             34      37 37
                                                                                                                                                                                                                                                                                                                                     26            28                    29
                                                                                                                                                                                             25
                                                    20                                                                                                                                20                   12             15                                                                                             20
                                                            7                                                                                                                                                                                                                                                                                 6              5
                                                                                                                                                                                                                                                                                                                                 3
                                                     0 Llama2-70b Mixtral-8x7b Mistral-small GPT-3.5                 GPT-4                                                             0 Llama2-70b Mixtral-8x7b Mistral-small GPT-3.5                  GPT-4                                                             0 Llama2-70b Mixtral-8x7b Mistral-small GPT-3.5                GPT-4

                                                                                       (a)                                                                                                                              (b)                                                                                                                               (c)

       Figure 6: AF represents the autoformalisation components, and TI represents the textual inference components.
       TI+AF (Base Model) indicates the use of the base model for both the autoformalisation and textual inference
       components. TI+AF (GPT-4) indicates the use of GPT-4 for the autoformalisation components, while the base
       model is used for textual inference.


          Figure 6, integrating GPT-4 for autoformalisation                                                                                                                                                                      increases. Models like Mistral-small and GPT-3.5
          led to a significant increase in the number of expla-                                                                                                                                                                  tend to suggest more proof steps to accomplish the
          nations successfully refined across all models. For                                                                                                                                                                    logical goal, which can result in some redundant
          instance, Llama2-70b with GPT-4 as the formali-                                                                                                                                                                        steps, such as the significant pulse shown in Figure
          sation component refined explanations from 7% to                                                                                                                                                                       7c. For unrefined explanations, as shown in Fig-
          65% in the e-SNLI dataset. For the multiple-choice                                                                                                                                                                     ure 7d, 7e and 7f, the progression is steadier but
          question answering dataset, GPT-3.5 showed a rela-                                                                                                                                                                     retains a positive trend, where the models gener-
          tively smaller increase from 44% to 48% and from                                                                                                                                                                       ally suggest more proof steps in response to the
          29% to 34%. Despite these improvements, a perfor-                                                                                                                                                                      additional explanatory sentences introduced to cor-
          mance gap persists between GPT-4 and the other                                                                                                                                                                         rect a logical error identified from the erroneous
          models, which is attributed to GPT-4’s superior                                                                                                                                                                        step. We analysed the correlation between average
          symbolic reasoning capabilities required for expla-                                                                                                                                                                    successful explanatory sentences and total planned
          nation refinement from the identified logical errors.                                                                                                                                                                  sentences in proofs, detailed in Appendix A.3. Ex-
                                                                                                                                                                                                                                 amples of refined and unrefined explanations are in
       Explanations are progressively made more com-                                                                                                                                                                             Appendix A.5.
       plete and consistent through iterative refine-
                                                                                                                                                                                                                                 4.5           Factual Errors and Trivial Explanations
       ment. In order to deliver step-wise logical con-
       sistency, explanations need to be made complete                                                                                                                                                                           In addition to evaluating the logical validity of ex-
       and self-contained, leading to the introduction of                                                                                                                                                                        planations, we also conducted a human evaluation
       additional explanatory sentences, which increases                                                                                                                                                                         of the refined explanations, considering factual cor-
       the total number of suggested proof steps. There-                                                                                                                                                                         rectness and explanation triviality for the two best-
       fore, we further evaluated how the proof steps vary                                                                                                                                                                       performing models (GPT-3.5 and GPT-4). This
       when the total number of suggested proof steps                                                                                                                                                                            evaluation focused on two questions: “Are the
       increases, contrasting both refined and unrefined                                                                                                                                                                         refined explanatory sentences factually correct?”
       cases. Figure 7 illustrates this trend. In general,                                                                                                                                                                       and “Is the explanation trivial, merely repeating
       all models show a positive trend, as the total sug-                                                                                                                                                                       or paraphrasing the content of the premise and
       gested proof steps increase, the average number of                                                                                                                                                                        hypothesis to achieve logical validity?”. As illus-
       proof steps processed by the proof assistant also                                                                                                                                                                         trated in Figure 8, our findings indicate that all
                                              8                          Refined e-SNLI                                                                       8                      Refined QASC                                                        8                                              Refined WorldTree
                     Avg. Processed Proof Steps                                                             Mixtral-8x7b                                                                                    Mixtral-8x7b                                                                                                                Mixtral-8x7b




                                                                                                                                Avg. Processed Proof Steps




                                                                                                                                                                                                                                Avg. Processed Proof Steps
                                              7                                                             Mistral-small                                     7                                             Mistral-small                                7                                                                              Mistral-small
                                                                                                            GPT-3.5                                                                                         GPT-3.5                                                                                                                     GPT-3.5
                                              6                                                             GPT-4                                             6                                             GPT-4                                        6                                                                              GPT-4
                                              5                                                             Llama2-70b                                        5                                             Llama2-70b                                   5                                                                              Llama2-70b

                                              4                                                                                                               4                                                                                          4
                                              3                                                                                                               3                                                                                          3
                                              2                                                                                                               2                                                                                          2
                                              1                                                                                                               1                                                                                          1
                                              00        2          4          6             8         10       12          14                                 00      2       4       6         8     10     12            14                            00                            2           4        6             8       10     12       14
                                                            Total Suggested Proof Steps                                                                                   Total Suggested Proof Steps                                                                                          Total Suggested Proof Steps
                                                                                  (a)                                                                                                     (b)                                                                                                                   (c)
                                        8                              Unrefined e-SNLI                                                                       8                   Unrefined QASC                                                               8                                        Unrefined WorldTree
                                                                                                           Mixtral-8x7b                                                                                     Mixtral-8x7b                                                                                                                 Mixtral-8x7b
              Avg. Processed Proof Steps




                                                                                                                                Avg. Processed Proof Steps




                                                                                                                                                                                                                                      Avg. Processed Proof Steps
                                        7                                                                  Mistral-small                                      7                                             Mistral-small                                      7                                                                         Mistral-small
                                                                                                           GPT-3.5                                                                                          GPT-3.5                                                                                                                      GPT-3.5
                                        6                                                                  GPT-4                                              6                                             GPT-4                                              6                                                                         GPT-4
                                        5                                                                  Llama2-70b                                         5                                             Llama2-70b                                         5                                                                         Llama2-70b

                                        4                                                                                                                     4                                                                                                4
                                        3                                                                                                                     3                                                                                                3
                                        2                                                                                                                     2                                                                                                2
                                        1                                                                                                                     1                                                                                                1
                                        00          2          4          6             8        10           12       14                                     00      2       4       6         8     10     12            14                                  00                          2           4        6             8    10     12       14
                                                            Total Suggested Proof Steps                                                                                   Total Suggested Proof Steps                                                                                          Total Suggested Proof Steps
                                                                              (d)                                                                                                         (e)                                                                                                                       (f)

      Figure 7: Average of proof steps processed by the proof assistant against the total proof steps suggested by the
      LLMs in refined and unrefined explanations.

                                                   100             100
                                                                          e-SNLI                100           100
                                                                                                                                                                                           QASC 98.18              98.18                                                                        100.0
                                                                                                                                                                                                                                                                                                                    WorldTree100.0
                         100                                                                                                                              100         97.73       95.45                                                                                       100                                                                 97.3
Percentage of Explanations




                                                                                                                                 Percentage of Explanations




                                                                                                                                                                                                                                                     Percentage of Explanations
                                                                                                       Factually Correct                                                                                   Factually Correct                                                                                                               Factually Correct
                                                                                                       Not Trivial                                                                                         Not Trivial                                                                                      86.21                          Not Trivial
                               80                                                                                                                             80                                                                                                                  80

                               60                                                                                                                             60                                                                                                                  60

                               40                                                                                                                             40                                                                                                                  40

                               20                                                                                                                             20                                                                                                                  20

                                     0                  GPT-3.5                                       GPT-4                                                       0        GPT-3.5                         GPT-4                                                                  0                 GPT-3.5                               GPT-4

                                                                         (a)                                                                                                              (b)                                                                                                                        (c)

                                                               Figure 8: Human evaluation of refined explanations in terms of factuality and triviality.


    refined explanations in the e-SNLI and WorldTree                                                                                                                                            5     Related Work
    datasets are consistent with commonsense knowl-
                                                                                                                                                                                                5.1        LLMs Self-Refinement from External
    edge. In the QASC dataset, 2.27% and 1.82% of the
                                                                                                                                                                                                           Feedback
    explanation refined by GPT-3.5 and GPT-4 contain
    sentences misaligned with true world knowledge.                                                                                                                                             Self-refinement of LLMs has demonstrated promis-
    We found that the majority of these errors result                                                                                                                                           ing effectiveness in generating faithful and trust-
    from over-generalisation, such as the sentence All                                                                                                                                          worthy responses (Pan et al., 2023b). The use of
    tetrapods are defined to have four limbs, which                                                                                                                                             external feedback to guide LLMs has been exten-
    inaccurately includes snakes.                                                                                                                                                               sively studied (Yu et al., 2023; Akyurek et al., 2023;
                                                                                                                                                                                                Olausson et al., 2024a). Previous work such as
       Finally, we found a relatively low number of ex-                                                                                                                                         Peng et al. (2023) have employed facts retrieved
    planations that repeat or paraphrase the content of                                                                                                                                         from external knowledge bases as sources of feed-
    premise and hypothesis. This phenomenon is ab-                                                                                                                                              back, while Paul et al. (2024) developed a critic
    sent in e-SNLI and becomes more evident when the                                                                                                                                            model to provide feedback for reasoning refine-
    explanatory sentences increase in complexity (i.e.,                                                                                                                                         ment. Additionally, Nathani et al. (2023) have ex-
    WorldTree), leading models sometimes to gener-                                                                                                                                              plored the use of feedback models for automated
    ate explanations that do not include any additional                                                                                                                                         feedback generation. Various works have also in-
    information for the entailment to hold.                                                                                                                                                     vestigated tasks related to code generation (Chen
et al., 2023; Olausson et al., 2024b) and the creation    ham et al., 2022; Wu et al., 2022; First et al., 2023;
of either synthetic or expert-written logical natural     Jiang et al., 2023), and efforts to transform nat-
language expressions (Olausson et al., 2023). Quan        ural language sentences into logical forms using
et al. (2024) use a differentiable logic reasoner for     LLMs (Pan et al., 2023a; Olausson et al., 2023;
verifying and refining explanations via abductive         Jiang et al., 2024b; Dalal et al., 2024). However,
reasoning, improving logical consistency in ethical       contextual information is frequently lost when sen-
NLI tasks. This paper focuses on the automated            tences are translated in these logical frameworks.
verification and refinement of natural language ex-       To mitigate semantic loss during the transforma-
planations created by human annotators in NLI             tion process, we leverage Neo-Davidsonian event
tasks. Our method leverages feedback from exter-          semantics, which aims to maximise the preserva-
nal solvers to iteratively refine explanations, which     tion sentence-level content. This representation
require specific modelling interventions such as          paradigm can facilitate a more systematic content-
extracting the exact erroneous steps from the theo-       preserving translation to logical forms, which is
rem prover to effectively refine logical errors in the    more independent from particular choices of repre-
explanatory sentences.                                    sentation schema.

5.2   Explanation Generation                              6   Conclusion
Existing work has explored robust and effective ap-       In this work, we present a novel neuro-symbolic
proaches for multi-hop reasoning tasks in explana-        framework, Explanation-Refiner, which integrates
tion generation (Thayaparan et al., 2021; Valentino       LLMs and theorem provers for automatic verifi-
et al., 2022b; Neves Ribeiro et al., 2022). In prior      cation and refinement of natural language expla-
research, metrics such as Mean Average Precision          nations through iterative cycles. Extensive exper-
(MAP) (Valentino et al., 2022a) have been em-             iments on textual entailment and multiple-choice
ployed to assess the ranking of facts in explana-         QA tasks showed improved logical validity of
tion generation tasks against gold-standard explana-      human-annotated explanations. We investigated
tions. Although these metrics effectively measure         the model’s performance from simple to complex
precision relative to these standards, they inade-        explanatory/sentence structures and introduced a
quately capture the logical consistency and com-          method to prevent the loss of semantic information
pleteness of the explanations generated. Such short-      in autoformalisation tasks with error correction.
comings are particularly critical in tasks that re-       In future work, we aspire to enhance the frame-
quire not only factual accuracy but also coherence        work’s robustness towards complex and unstruc-
and inferential soundness, as in natural language         tured explanations with fewer iterations required to
inference and explanation generation. Our pro-            improve the model’s efficiency.
posed metrics address this gap by incorporating
assessments of logical validity. Although some            Limitations
metrics have been proposed to manually evaluate
the logical validity of explanations (Valentino et al.,   While this work have demonstrated significant im-
2021; Yuan et al., 2024), such as non-redundancy          provements in terms of enhancing the logical con-
or logical errors, these require significant effort       sistency of explanations, the connection between
from domain experts in formal languages. In this          logical consistency and AI safety still needs fur-
work, we use human-annotated explanations as a            ther investigation. While the idea of using for-
foundational dataset to detect and correct logical        mal solvers in conjunction with LLMs delivers a
discrepancies, offering a framework adaptable for         promise avenue to improve the consistency of rea-
automatically enhancing both the precision and log-       soning within LLMs, these methodologies need to
ical integrity of outputs across multi-step inference     be further developed and critically assessed as a
tasks.                                                    mechanism which can provide guarantees of cor-
                                                          rectness, consistency and completeness within crit-
5.3   Autoformalisation                                   ical application domains.
Autoformalisation refers to the process of trans-
                                                          Acknowledgments
lating natural language descriptions into symbolic
representations. Research in this area has included       This work was partially funded by the Swiss Na-
the formalisation of mathematical proofs (Cunning-        tional Science Foundation (SNSF) project Neu-
Math (200021_204617), by the EPSRC grant                     Proceedings of the 58th Annual Meeting of the Asso-
EP/T026995/1, “EnnCore: End-to-End Concep-                   ciation for Computational Linguistics, pages 4157–
                                                             4165, Online. Association for Computational Lin-
tual Guarding of Neural Architectures” under Secu-
                                                             guistics.
rity for all in an AI enabled society, by the CRUK
National Biomarker Centre, and supported by the            Chun Sik Chan, Huanqi Kong, and Liang Guanqing.
Manchester Experimental Cancer Medicine Centre               2022. A comparative study of faithfulness metrics
                                                             for model interpretability methods. In Proceedings
and the NIHR Manchester Biomedical Research                  of the 60th Annual Meeting of the Association for
Centre.                                                      Computational Linguistics (Volume 1: Long Papers),
                                                             pages 5029–5038, Dublin, Ireland. Association for
                                                             Computational Linguistics.
References                                                 Qianglong Chen, Feng Ji, Xiangji Zeng, Feng-Lin
Afra Feyza Akyurek, Ekin Akyurek, Ashwin Kalyan,             Li, Ji Zhang, Haiqing Chen, and Yin Zhang. 2021.
  Peter Clark, Derry Tanti Wijaya, and Niket Tandon.         KACE: Generating knowledge aware contrastive ex-
  2023. RL4F: Generating natural language feedback           planations for natural language inference. In Pro-
  with reinforcement learning for repairing model out-       ceedings of the 59th Annual Meeting of the Associa-
  puts. In Proceedings of the 61st Annual Meeting of         tion for Computational Linguistics and the 11th Inter-
  the Association for Computational Linguistics (Vol-        national Joint Conference on Natural Language Pro-
  ume 1: Long Papers), pages 7716–7733, Toronto,             cessing (Volume 1: Long Papers), pages 2516–2527,
  Canada. Association for Computational Linguistics.         Online. Association for Computational Linguistics.

Pepa Atanasova, Oana-Maria Camburu, Christina Li-          Xinyun Chen, Maxwell Lin, Nathanael Schärli, and
  oma, Thomas Lukasiewicz, Jakob Grue Simonsen,              Denny Zhou. 2023. Teaching large language models
  and Isabelle Augenstein. 2023. Faithfulness tests          to self-debug.
  for natural language explanations. In Proceedings
  of the 61st Annual Meeting of the Association for        Garett Cunningham, Razvan Bunescu, and David
  Computational Linguistics (Volume 2: Short Papers),        Juedes. 2022. Towards autoformalization of math-
  pages 283–294, Toronto, Canada. Association for            ematics and code correctness: Experiments with el-
  Computational Linguistics.                                 ementary proofs. In Proceedings of the 1st Work-
                                                             shop on Mathematical Natural Language Processing
Kaj Bostrom, Zayne Sprague, Swarat Chaudhuri, and            (MathNLP), pages 25–32, Abu Dhabi, United Arab
  Greg Durrett. 2022. Natural language deduction             Emirates (Hybrid). Association for Computational
  through search over statement compositions. In Find-       Linguistics.
  ings of the Association for Computational Linguistics:
                                                           Dhairya Dalal, Marco Valentino, André Freitas, and
  EMNLP 2022, pages 4871–4883, Abu Dhabi, United
                                                             Paul Buitelaar. 2024. Inference to the best explana-
  Arab Emirates. Association for Computational Lin-
                                                             tion in large language models.
  guistics.
                                                           Yanai Elazar, Hongming Zhang, Yoav Goldberg, and
Tom Brown, Benjamin Mann, Nick Ryder, Melanie                Dan Roth. 2021. Back to square one: Artifact detec-
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind         tion, training and commonsense disentanglement in
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda           the Winograd schema. In Proceedings of the 2021
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,              Conference on Empirical Methods in Natural Lan-
  Gretchen Krueger, Tom Henighan, Rewon Child,               guage Processing, pages 10486–10500, Online and
  Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens         Punta Cana, Dominican Republic. Association for
  Winter, Chris Hesse, Mark Chen, Eric Sigler, Ma-           Computational Linguistics.
  teusz Litwin, Scott Gray, Benjamin Chess, Jack
  Clark, Christopher Berner, Sam McCandlish, Alec          Emily First, Markus N. Rabe, Talia Ringer, and Yuriy
  Radford, Ilya Sutskever, and Dario Amodei. 2020.           Brun. 2023. Baldur: Whole-proof generation and
  Language models are few-shot learners. In Ad-              repair with large language models.
  vances in Neural Information Processing Systems,
  volume 33, pages 1877–1901. Curran Associates,           Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,
  Inc.                                                       Yujiu Yang, Nan Duan, and Weizhu Chen. 2024.
                                                             Critic: Large language models can self-correct with
Oana-Maria Camburu, Tim Rocktäschel, Thomas                  tool-interactive critiquing.
  Lukasiewicz, and Phil Blunsom. 2018. e-snli: Natu-
  ral language inference with natural language explana-    Peter Jansen, Elizabeth Wainwright, Steven Mar-
  tions. In Advances in Neural Information Processing        morstein, and Clayton Morrison. 2018. WorldTree:
  Systems, volume 31. Curran Associates, Inc.                A corpus of explanation graphs for elementary sci-
                                                             ence questions supporting multi-hop inference. In
Oana-Maria Camburu, Brendan Shillingford, Pasquale           Proceedings of the Eleventh International Confer-
  Minervini, Thomas Lukasiewicz, and Phil Blunsom.           ence on Language Resources and Evaluation (LREC
  2020. Make up your mind! adversarial generation            2018), Miyazaki, Japan. European Language Re-
  of inconsistent natural language explanations. In          sources Association (ELRA).
Albert Q. Jiang, Alexandre Sablayrolles, Antoine           Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-
  Roux, Arthur Mensch, Blanche Savary, Chris                 son. 2002. Isabelle/HOL: a proof assistant for
  Bamford, Devendra Singh Chaplot, Diego de las              higher-order logic. Springer.
  Casas, Emma Bou Hanna, Florian Bressand, Gi-
  anna Lengyel, Guillaume Bour, Guillaume Lam-             Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  ple, Lélio Renard Lavaud, Lucile Saulnier, Marie-          Armando Solar-Lezama, Joshua Tenenbaum, and
  Anne Lachaux, Pierre Stock, Sandeep Subramanian,           Roger Levy. 2023. LINC: A neurosymbolic approach
  Sophia Yang, Szymon Antoniak, Teven Le Scao,               for logical reasoning by combining language models
  Théophile Gervet, Thibaut Lavril, Thomas Wang,             with first-order logic provers. In Proceedings of the
  Timothée Lacroix, and William El Sayed. 2024a.             2023 Conference on Empirical Methods in Natural
  Mixtral of experts.                                        Language Processing, pages 5153–5176, Singapore.
                                                             Association for Computational Linguistics.
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timoth’ee         Theo X. Olausson, Jeevana Priya Inala, Chenglong
  Lacroix, Yuhuai Wu, and Guillaume Lample. 2023.            Wang, Jianfeng Gao, and Armando Solar-Lezama.
  Draft, Sketch, and Prove: Guiding formal theorem           2024a. Is self-repair a silver bullet for code gen-
  provers with informal proofs. In International Con-        eration? In International Conference on Learning
  ference on Learning Representations.                       Representations (ICLR).
Dongwei Jiang, Marcio Fonseca, and Shay B. Cohen.
                                                           Theo X. Olausson, Jeevana Priya Inala, Chenglong
  2024b. Leanreasoner: Boosting complex logical
                                                             Wang, Jianfeng Gao, and Armando Solar-Lezama.
  reasoning with lean. In Proceedings of the 2024
                                                             2024b. Is self-repair a silver bullet for code genera-
  Conference of the North American Chapter of the
                                                             tion?
  Association for Computational Linguistics: Human
  Language Technologies.
                                                           OpenAI. 2023. GPT-4 technical report.            CoRR,
Tushar Khot, Peter Clark, Michal Guerquin, Pe-               abs/2303.08774.
  ter Alexander Jansen, and Ashish Sabharwal. 2019.
  QASC: A dataset for question answering via sentence      Liangming Pan, Alon Albalak, Xinyi Wang, and
  composition. In AAAI.                                      William Wang. 2023a. Logic-LM: Empowering large
                                                             language models with symbolic solvers for faithful
Sawan Kumar and Partha Talukdar. 2020. NILE : Natu-          logical reasoning. In Findings of the Association
  ral language inference with faithful natural language      for Computational Linguistics: EMNLP 2023, pages
  explanations. In Proceedings of the 58th Annual            3806–3824, Singapore. Association for Computa-
  Meeting of the Association for Computational Lin-          tional Linguistics.
  guistics, pages 8730–8742, Online. Association for
  Computational Linguistics.                               Liangming Pan, Michael Saxon, Wenda Xu, Deepak
                                                             Nathani, Xinyi Wang, and William Yang Wang.
Haochen Liu, Joseph Thekinen, Sinem Mollaoglu,               2023b. Automatically correcting large language
  Da Tang, Ji Yang, Youlong Cheng, Hui Liu, and              models: Surveying the landscape of diverse self-
  Jiliang Tang. 2022. Toward annotator group bias in         correction strategies.
  crowdsourcing. In Proceedings of the 60th Annual
  Meeting of the Association for Computational Lin-        Terence Parsons. 1990. Events in the semantics of en-
  guistics (Volume 1: Long Papers), pages 1797–1806,         glish: A study in subatomic semantics.
  Dublin, Ireland. Association for Computational Lin-
  guistics.                                                Debjit Paul, Mete Ismayilzada, Maxime Peyrard, Beat-
                                                             riz Borges, Antoine Bosselut, Robert West, and Boi
Mistral AI. 2024. https://docs.mistral.ai/.
                                                             Faltings. 2024. REFINER: Reasoning feedback on
Deepak Nathani, David Wang, Liangming Pan, and               intermediate representations. In Proceedings of the
  William Wang. 2023. MAF: Multi-aspect feedback             18th Conference of the European Chapter of the As-
  for improving reasoning in large language models.          sociation for Computational Linguistics (Volume 1:
  In Proceedings of the 2023 Conference on Empiri-           Long Papers), pages 1100–1126, St. Julian’s, Malta.
  cal Methods in Natural Language Processing, pages          Association for Computational Linguistics.
  6591–6616, Singapore. Association for Computa-
  tional Linguistics.                                      Lawrence Charles Paulson. 1999. A generic tableau
                                                             prover and its integration with isabelle. J. Univers.
Danilo Neves Ribeiro, Shen Wang, Xiaofei Ma, Rui             Comput. Sci., 5:73–87.
  Dong, Xiaokai Wei, Henghui Zhu, Xinchi Chen,
  Peng Xu, Zhiheng Huang, Andrew Arnold, and Dan           Baolin Peng, Michel Galley, Pengcheng He, Hao Cheng,
  Roth. 2022. Entailment tree explanations via itera-        Yujia Xie, Yu Hu, Qiuyuan Huang, Lars Liden, Zhou
  tive retrieval-generation reasoner. In Findings of the     Yu, Weizhu Chen, and Jianfeng Gao. 2023. Check
  Association for Computational Linguistics: NAACL           your facts and try again: Improving large language
  2022, pages 465–475, Seattle, United States. Associ-       models with external knowledge and automated feed-
  ation for Computational Linguistics.                       back.
Xin Quan, Marco Valentino, Louise Dennis, and An-         Nathaniel Weir, Peter Clark, and Benjamin Van Durme.
  dre Freitas. 2024. Enhancing ethical explanations         2023. Nellie: A neuro-symbolic inference engine for
  of large language models through iterative symbolic       grounded, compositional, and explainable reasoning.
  refinement. In Proceedings of the 18th Conference of
  the European Chapter of the Association for Compu-      Sarah Wiegreffe and Ana Marasovic. 2021. Teach me to
  tational Linguistics (Volume 1: Long Papers), pages       explain: A review of datasets for explainable natural
  1–22, St. Julian’s, Malta. Association for Computa-       language processing. In Thirty-fifth Conference on
  tional Linguistics.                                       Neural Information Processing Systems Datasets and
                                                            Benchmarks Track (Round 1).
Boris Shminke. 2022. Python client for isabelle server.
                                                          Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus
Mokanarangan Thayaparan, Marco Valentino, and               Rabe, Charles Staats, Mateja Jamnik, and Christian
 André Freitas. 2021. Explainable inference over            Szegedy. 2022. Autoformalization with large lan-
 grounding-abstract chains for science questions. In        guage models. In Advances in Neural Information
 Findings of the Association for Computational Lin-         Processing Systems, volume 35, pages 32353–32368.
 guistics: ACL-IJCNLP 2021, pages 1–12, Online.             Curran Associates, Inc.
 Association for Computational Linguistics.
                                                          Wenhao Yu, Zhihan Zhang, Zhenwen Liang, Meng
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
                                                           Jiang, and Ashish Sabharwal. 2023. Improving lan-
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay
                                                           guage models via plug-and-play retrieval feedback.
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
  Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton
  Ferrer, Moya Chen, Guillem Cucurull, David Esiobu,      Li Yuan, Yi Cai, Haopeng Ren, and Jiexin Wang. 2024.
  Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller,        A logical pattern memory pre-trained model for en-
  Cynthia Gao, Vedanuj Goswami, Naman Goyal, An-             tailment tree generation. In Proceedings of the
  thony Hartshorn, Saghar Hosseini, Rui Hou, Hakan           2024 Joint International Conference on Computa-
  Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa,         tional Linguistics, Language Resources and Evalua-
  Isabel Kloumann, Artem Korenev, Punit Singh Koura,         tion (LREC-COLING 2024), pages 759–772, Torino,
  Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Di-         Italia. ELRA and ICCL.
  ana Liskovich, Yinghai Lu, Yuning Mao, Xavier Mar-
  tinet, Todor Mihaylov, Pushkar Mishra, Igor Moly-       Wenting Zhao, Justin Chiu, Claire Cardie, and Alexan-
  bog, Yixin Nie, Andrew Poulton, Jeremy Reizen-            der Rush. 2023. Abductive commonsense reason-
  stein, Rashi Rungta, Kalyan Saladi, Alan Schelten,        ing exploiting mutually exclusive explanations. In
  Ruan Silva, Eric Michael Smith, Ranjan Subrama-          Proceedings of the 61st Annual Meeting of the As-
  nian, Xiaoqing Ellen Tan, Binh Tang, Ross Tay-            sociation for Computational Linguistics (Volume 1:
  lor, Adina Williams, Jian Xiang Kuan, Puxin Xu,          Long Papers), pages 14883–14896, Toronto, Canada.
  Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan,       Association for Computational Linguistics.
  Melanie Kambadur, Sharan Narang, Aurelien Ro-
  driguez, Robert Stojnic, Sergey Edunov, and Thomas      Xinyan Zhao and V.G.Vinod Vydiswaran. 2021. Lirex:
  Scialom. 2023. Llama 2: Open foundation and fine-         Augmenting language inference with relevant expla-
  tuned chat models.                                        nations. Proceedings of the AAAI Conference on
                                                            Artificial Intelligence, 35(16):14532–14539.
Marco Valentino, Ian Pratt-Hartmann, and André Fre-
 itas. 2021. Do natural language explanations repre-
 sent valid logical arguments? verifying entailment in    A     Appendix
 explainable NLI gold standards. In Proceedings of
 the 14th International Conference on Computational       A.1    Algorithm
 Semantics (IWCS), pages 76–86, Groningen, The
 Netherlands (online). Association for Computational      Algorithm 1 shows the overall framework of
 Linguistics.                                             Explanation-Refiner.
Marco Valentino, Mokanarangan Thayaparan, Deborah
 Ferreira, and André Freitas. 2022a. Hybrid autore-       A.2    Scalability
 gressive inference for scalable multi-hop explanation
                                                          Figure 9 shows the average Isabelle/HOL solving
 regeneration. Proceedings of the AAAI Conference
 on Artificial Intelligence, 36(10):11403–11411.          time against the number of planned explanatory
                                                          sentences in a proof and the length of suggested
Marco Valentino, Mokanarangan Thayaparan, and An-         proof steps, including theories that have syntax
 dré Freitas. 2022b. Case-based abductive natural         errors, respectively. In some cases, the theorem
 language inference. In Proceedings of the 29th Inter-
 national Conference on Computational Linguistics,
                                                          prover may get stuck on a proof step, and we have
 pages 1556–1568, Gyeongju, Republic of Korea. In-        set a termination time if the solving time exceeds
 ternational Committee on Computational Linguistics.      65 seconds.
                                                     100                Total Dataset
                                                                                                Mixtral-8x7b




                          Avg. Isabelle Solving Time/s
                                                                                                Mistral-small
                                                         80                                     GPT-3.5
                                                                                                GPT-4
                                                                                                Llama2-70b
                                                         60

                                                         40

                                                         20

                                                         00    2    4    6           8     10     12     14
                                                              Number of Explanatory Sentences
                                                                             (a)

                                                     100                Total Dataset
                                                                                                Mixtral-8x7b
                          Avg. Isabelle Solving Time/s




                                                                                                Mistral-small
                                                         80                                     GPT-3.5
                                                                                                GPT-4
                                                                                                Llama2-70b
                                                         60

                                                         40

                                                         20

                                                         00    2    4    6           8     10     12     14
                                                              Length of Suggested Proof Steps
                                                                          (b)

Figure 9: (a) Average Isabelle/HOL solving time against number of explanatory sentences planned in a proof. (b)
Average Isabelle/HOL solving time against number of suggested proof steps in a proof.


A.3   Average Processed vs. Planned                                                A.4.1   Autoformalisation
      Explanatory Sentences per Proof

Figure 10 and Figure 11 shows experiments on
average number of successfully processed explana-                                  Figure 13 displays the prompts used to identify ac-
tory sentences in one proof against total planned                                  tion verbs (events) within the premise, explanation,
explanatory sentences in a suggest proof. Figure                                   and hypothesis sentences, representing events in
12 also shows the comparison of average processed                                  Davidsonian-event semantics. Figure 14 displays
proof steps against total suggested proof steps in                                 the prompts used to transfer natural language to
all dataset.                                                                       logical forms based on the identified events verbs.
                                                                                   Figure 15 shows how to convert logical forms into
                                                                                   Isabelle/HOL code (axioms and type declaration).
A.4   Prompts                                                                      Figure 16 shows how to convert the premise and hy-
                                                                                   pothesis sentences into the Isabelle/HOL theorem
Temperature settings were adjusted to 0 for GPT-                                   code, based on the previously constructed axioms
3.5 and GPT-4, and to 0.01 for Llama2-70b,                                         code. Figure 17 shows how to refine the syntax
Mixtral-8x7b, and Mistral-small, aiming to achieve                                 errors based on the types of errors, the provided
both determinism in the output and effective code                                  code, the error messages, and the locations of the
generation for theorem prover.                                                     errors within the code.
A.4.2 Proof Construction
Figure 18 shows the prompts for making a pre-
liminary inference strategy, which also identifies
redundant and related explanatory sentences that
will be used for proof generation. Figure 19 shows
the prompts for building the proof steps used for
Isabelle/HOL Proof assistant based on the provided
inference strategy.
A.4.3 Explanation Refinement
Figure 20 shows how to refine the explanatory sen-
tences based on the provided information.

A.5   Examples of Explanation Refinement
Table 1 shows an example from the e-SNLI dataset
of how the explanation changes after each iteration.
Figures 21, 22, and 23 illustrate the Isabelle/HOL
theory code changes during the refinement process.
Table 2 with Figures 24, 25, and 26 also show
another example of how the explanation is refined
after each iteration.
   Green code indicates the proof steps that have
successfully progressed, while red code shows
where the proof failed at that step. More examples
can be found at https://github.com/neuro-symbolic-
ai/explanation_refinement.

A.6   Datasets and Theorem Prover
The datasets used in our experiments, including
samples from e-SNLI (Camburu et al., 2018),
QASC (Khot et al., 2019), and WorldTree (Jansen
et al., 2018), are all sourced from open academic
works. We employed Isabelle as the theorem
prover, which is distributed under the revised BSD
license. Additionally, the TCP client used for the
Isabelle server (Shminke, 2022) is licensed under
Apache-2.0.
                                5                     Refined e-SNLI                                                                 5                 Refined QASC                                                         5                          Refined WorldTree
                                                                                       Mixtral-8x7b                                                                              Mixtral-8x7b                                                                                             Mixtral-8x7b
      Avg. Processed Explanations




                                                                                                           Avg. Processed Explanations




                                                                                                                                                                                                  Avg. Processed Explanations
                                                                                       Mistral-small                                                                             Mistral-small                                                                                            Mistral-small
                                4                                                      GPT-3.5                                       4                                           GPT-3.5                                    4                                                             GPT-3.5
                                                                                       GPT-4                                                                                     GPT-4                                                                                                    GPT-4
                                                                                       Llama2-70b                                                                                Llama2-70b                                                                                               Llama2-70b
                                3                                                                                                    3                                                                                      3

                                2                                                                                                    2                                                                                      2

                                1                                                                                                    1                                                                                      1

                                00            2            4                 6              8          10                            00       2          4              6          8             10                         00             2               4                 6              8             10
                                     Number of Planned Explanations                                                                       Number of Planned Explanations                                                               Number of Planned Explanations
                                                               (a)                                                                                            (b)                                                                                              (c)
                          5                        Unrefined e-SNLI                                                                  5                 Unrefined QASC                                                             5                Unrefined WorldTree
                                                                                      Mixtral-8x7b                                                                               Mixtral-8x7b                                                                                              Mixtral-8x7b
Avg. Processed Explanations




                                                                                                           Avg. Processed Explanations




                                                                                                                                                                                                        Avg. Processed Explanations
                                                                                      Mistral-small                                                                              Mistral-small                                                                                             Mistral-small
                          4                                                           GPT-3.5                                        4                                           GPT-3.5                                          4                                                        GPT-3.5
                                                                                      GPT-4                                                                                      GPT-4                                                                                                     GPT-4
                                                                                      Llama2-70b                                                                                 Llama2-70b                                                                                                Llama2-70b
                          3                                                                                                          3                                                                                            3

                          2                                                                                                          2                                                                                            2

                          1                                                                                                          1                                                                                            1

                          00              2            4                 6              8             10                             00       2          4              6          8             10                               00           2               4                 6              8          10
                                     Number of Planned Explanations                                                                       Number of Planned Explanations                                                               Number of Planned Explanations
                                                           (d)                                                                                                (e)                                                                                                  (f)

Figure 10: Average Progressed Explanations against Number of Planned Explanations in Refined and Unrefined
e-SNLI, QASC and WorldTree Dataset


                                5                 Refined Total Dataset                                                              5            Unrefined Total Dataset                                                   5                            Total Dataset
                                                                                       Mixtral-8x7b                                                                              Mixtral-8x7b                                                                                             Mixtral-8x7b
      Avg. Processed Explanations




                                                                                                           Avg. Processed Explanations




                                                                                                                                                                                                  Avg. Processed Explanations



                                                                                       Mistral-small                                                                             Mistral-small                                                                                            Mistral-small
                                4                                                      GPT-3.5                                       4                                           GPT-3.5                                    4                                                             GPT-3.5
                                                                                       GPT-4                                                                                     GPT-4                                                                                                    GPT-4
                                                                                       Llama2-70b                                                                                Llama2-70b                                                                                               Llama2-70b
                                3                                                                                                    3                                                                                      3

                                2                                                                                                    2                                                                                      2

                                1                                                                                                    1                                                                                      1

                                00            2            4                 6              8          10                            00       2          4              6          8             10                         00             2               4                 6              8             10
                                     Number of Planned Explanations                                                                       Number of Planned Explanations                                                               Number of Planned Explanations
                                                               (a)                                                                                            (b)                                                                                              (c)

Figure 11: Average Progressed Explanations against Number of Planned Explanations for Refined, Unrefined, and
Combined Across All Datasets


                                8                 Refined Total Dataset                                                              8            Unrefined Total Dataset                                                   8                            Total Dataset
                                                                                        Mixtral-8x7b                                                                              Mixtral-8x7b                                                                                             Mixtral-8x7b
      Avg. Processed Proof Steps




                                                                                                           Avg. Processed Proof Steps




                                                                                                                                                                                                  Avg. Processed Proof Steps




                                7                                                       Mistral-small                                7                                            Mistral-small                             7                                                              Mistral-small
                                                                                        GPT-3.5                                                                                   GPT-3.5                                                                                                  GPT-3.5
                                6                                                       GPT-4                                        6                                            GPT-4                                     6                                                              GPT-4
                                5                                                       Llama2-70b                                   5                                            Llama2-70b                                5                                                              Llama2-70b

                                4                                                                                                    4                                                                                      4
                                3                                                                                                    3                                                                                      3
                                2                                                                                                    2                                                                                      2
                                1                                                                                                    1                                                                                      1
                                00    2           4        6         8           10         12    14                                 00   2        4      6         8       10     12      14                               00         2           4       6             8           10     12      14
                                          Total Suggested Proof Steps                                                                         Total Suggested Proof Steps                                                                  Total Suggested Proof Steps
                                                               (a)                                                                                            (b)                                                                                              (c)

Figure 12: Average Processed Proof Steps against Total Suggested Proof Steps for Refined, Unrefined, and Combined
Across All Datasets
  Algorithm 1: Explanation-Refiner
   Input :Premise p, Explanation E, Hypothesis h, Isabelle//HOL server isabelle,
              Autoformalisation model ma , Isabelle syntax refinement model msr , Rough inference
              model mri , Proof step build model mpr , Facts filter model mf , Explanation refinement
              model me
   Output :Updated Explanation E
 1 valid ← f alse
 2 isabelle_theory ← [ ]
 3 iterations ← 0
 4 max_iterations ← 11
 5 has_syntax_error ← f alse
 6 while not valid and iterations < max_iterations do
 7     session_id ← session_build(HOL, isabelle)
 8     isabelle.start(session_id)
 9     isabelle_theory ← transfer_to_symbolic(p, E, h, ma )
10     messages, error_content, error_code ← isabelle.check(isabelle_theory)
11     if syntax_errors in messages then
12          has_syntax_error ← true
13          it ← 0
14          while has_syntax_error and it < 3 do
15              isabelle_theory = refine_syntax(messages, error_content, error_code, isabelle_theory,
                  msr )
16              messages, error_content, error_code ← isabelle.check(isabelle_theory)
17              if syntax_errors in messages then
18                   has_syntax_error ← true
19                   it ← it + 1
20              else
21                   break
22              end if
23          end while
24     end if
25     rough_inference ← make_rough_inference(p, E, h, mri )
26     proof_steps ← build_proof(rough_inference, mpr )
27     isabelle_theory ← isabelle_theory + proof_steps
28     messages, error_content, error_code ← isabelle.check(isabelle_theory)
29     if messages is not empty then
30          message ← messages[0]
31          E ← filter(E, rough_inference, proof_steps, mf )
32          E ← refine_explanation(message, error_content, error_code, rough_inference, proof_steps,
             p, E, H, me )
33     else
34          valid ← true
35          break
36     end if
37     iterations ← iterations + 1
38     isabelle.shutdown()
39 end while
40 return E
SYSTEM: You are an expert in linguistics. You will be provided
with some sentences, find any action verbs of these sentences.
You need to ignore auxiliary verbs and modal verbs.
Some instructions:
1. You must give me the answer for all provided sentences.
2. Do not add any notes.
3. If no premise sentence provided, include it in the answer
as none.
4. Retain the answer words in their original form within the
provided sentence.
USER:
Here are some examples:
###
Hypothesis Sentence:
1. A woman is playing an instrument.
Has action: Yes
Actions: 1. playing

Explanation Sentence:
1. A violin is an instrument.
Has action: No
Actions: none

Premise Sentence:
1. A smiling woman is playing the violin in front of a
turquoise background.
Has action: Yes
                                                                 SYSTEM: You are an expert in semantics, formal language and
Actions: 1. playing
                                                                 neo-davidsonian event semantics. You will be provided with
###
                                                                 some sentences and the action verbs involved in those
...
                                                                 sentences. You need to transfer the sentences into symbolic
###
                                                                 language. If the sentence has no action, transfer it into
<<<<<<<<<<<<<<<<<<<<<<<
                                                                 formal language using first-order language. If the sentence
Strictly follow the instructions that I have claimed.
                                                                 has one action, transfer it using first-order language and
                                                                 davidsonian event semantics within one event. If the sentence
Provided sentences:
                                                                 has two more actions, transfer it using first-order language
{{input_sentence}}
                                                                 and davidsonian event semantics within at most two events.
                                                                 Some instructions:
Answer:
                                                                 1. Capture All Information: Ensure the logical form reflects
                                                                     every detail from the sentence.
                                                                 2. Use '⟶' for Certain Verbs: Represent actions like 'cause',
                                                                 'lead', 'help' that represent an implication, causal relation
Figure 13: Prompts for detecting event-related words in          with '⟶' for clarity.
                                                                 3. Event Variable 'e': Use 'e' for events, actions, with
the given sentences                                              action predicates having 'e' as their sole argument.
                                                                 ...
                                                                 USER: Here are some examples:
                                                                 ###
                                                                 Sentence: Grass is a kind of plant.
                                                                 Has action: No
                                                                 Actions:
                                                                 Logical form: ∀x. Grass(x) ⟶ Plant(x)
                                                                 ###
                                                                 Sentence: Squirrels typically eat nuts for energy.
                                                                 Has action: Yes
                                                                 Actions: 1. eat
                                                                 Logical form: ∀x y z. Squirrels(x) ∧ Nuts(y) ⟶ (∃e. Eat(e) ∧
                                                                 Agent(e, x) ∧ Patient(e, y) ∧ ForEnergy(y, x))
                                                                 ###
                                                                 ...
                                                                 <<<<<<<<<<<<<<<<<<<<<<<
                                                                 Strictly followed the instructions that I have claimed.

                                                                 Provided sentences:
                                                                 {{input_sentence}}

                                                                 Answer:



                                                                 Figure 14: Prompts for converting natural language
                                                                 sentences into logical form representations
                                                                 SYSTEM: You are an expert in Isabelle theorem prover, first-
                                                                 order logic and Davidsonian event semantics. You will be
                                                                 provided with a Hypothesis sentence and a Premise sentence
                                                                 with their corresponding logical forms (first-order logic and
                                                                 davidsonian event semantics).
                                                                 ...
                                                                 Some instructions:
                                                                 1. Isabelle code use ∧, ∨, ∀, ∃, ¬, ⟷, ⟶ as logic symbols.
SYSTEM: You are an expert in Isabelle theorem prover, first-     Please write the code with these logic symbols.
order logic and Davidsonian event semantics. You will be         ...
provided with some sentences and corresponding logical forms     The code structure for theorem hypothesis is:
(first-order logic and davidsonian event semantics) of those     ```
sentences. You need to transfer such logical forms into          theorem hypothesis:
Isabelle axioms code and define the consts and of the symbolic     (* Premise: [provided premise sentence in natural language]
forms.                                                           *)
Some instructions:                                               ...
1. Isabelle axioms code use ∧, ∨, ∀, ∃, ¬, ⟷, ⟶ as logic         end
symbols. Please write the axiom code with these logic symbols.   ```
2. Isabelle consts code use ⇒ as logic symbols. Please define    USER: Here are some examples:
...                                                              ###
The code structure for axioms is:                                Provided sentences:
```                                                              ...
begin                                                            Provided code:
                                                                 ...
typedecl entity                                                  Answer:
typedecl event                                                   ```
consts                                                           imports Main
  [define the consts here]
                                                                 begin
(* Explanation 1: [provided sentence 1 in natural language] *)
axiomatization where                                             typedecl entity
  explanation_1: [Transfer the logical form into isabelle code   typedecl event
here, non-bracketed of the predicate-argument form]
...                                                              consts
```                                                                AdultSponges :: "entity ⇒ bool"
USER: Here are some examples:                                      Eggs :: "entity ⇒ bool"
###                                                                Sperm :: "entity ⇒ bool"
Provided sentences:                                                Gametes :: "entity ⇒ bool"
                                                                   Produce :: "event ⇒ bool"
Explanation Sentence:                                              Agent :: "event ⇒ entity ⇒ bool"
1. If the infant is crying, it can be assumed that they are        Patient :: "event ⇒ entity ⇒ bool"
unhappy.
Logical form: ∀x e. Infant(x) ∧ Crying(e) ∧ Agent(e, x) ⟶        (* Explanation 1: Adult sponges produce eggs and sperm. *)
Unhappy(x)                                                       axiomatization where
                                                                   explanation_1: "∀x. AdultSponges x ⟶ (∃e y z. Eggs y ∧
Answer:                                                          Sperm z ∧ Produce e ∧ Agent e x ∧ Patient e y ∧ Patient e z)"
```
begin                                                            (* Explanation 2: Sperm and eggs are cells known as gametes.
typedecl entity                                                  *)
typedecl event                                                   axiomatization where
                                                                   explanation_2: "∀x y. Sperm x ∧ Eggs y ⟶ Gametes x ∧
consts                                                           Gametes y"
  Unhappy :: "entity ⇒ bool"
  Infant :: "entity ⇒ bool"
                                                                 theorem hypothesis:
  Crying :: "event ⇒ bool"                                         (* Premise: Students are studying adult sponges. *)
  Agent :: "event ⇒ entity ⇒ bool"                                 assumes asm: "Students x ∧ AdultSponges y ∧ Studying e ∧
                                                                 Agent e x ∧ Patient e y"
(* Explanation 1: If the infant is crying, it can be assumed       (* Hypothesis: Adult sponges produce gametes. *)
that they are unhappy. *)                                          shows "∃x y e. AdultSponges x ∧ Gametes y ∧ Produce e ∧
axiomatization where                                             Agent e x ∧ Patient e y"
  explanation_1: "∀x e. Infant x ∧ Crying e ∧ Agent e x ⟶        proof -
Unhappy x"

```                                                              qed
###
...                                                              end
###
<<<<<<<<<<<<<<<<<<<<<<<                                          ```
Strictly follow the instructions that I have claimed.            ###
                                                                 ...
Provided sentences:                                              ###
{{explanatory_sentences}}                                        <<<<<<<<<<<<<<<<<<<<<<<
                                                                 Strictly follow the instructions that I have claimed.
Answer:                                                          Provided sentences:
                                                                 {{input_sentence}}
```
answer goes here                                                 Provided code:
```                                                              {{axiom_code}}

Figure 15: Prompts for converting logical form into              Answer:
Isabelle/HOL code format for building the axioms and
                                                                 ```
type declaration                                                 answer code goes here (complete isabelle code )
                                                                 ```




                                                                 Figure 16: Prompts for building the theorem code part
                                                                 of the Isabelle/HOL theory
SYSTEM: You are an expert in the Isabelle theorem prover and
familiar with HOL session syntax and Davidsonian event
semantics. You will be provided with Isabelle code containing
some syntax errors, along with details of the errors and their
locations in the code. You need to fix the code (logical form)
of the related error.
Some instructions:
1. Do not change code structure, you just need to fix the        SYSTEM: You are an expert in natural language inference,
syntax error.                                                    textual entailment and linguistic semantics. You will be
2. Type unification failed errors indicates the defined consts   provided with a premise sentence, some explanatory sentences
and the acutal preidcates are not consistent. There are only     and a hypothesis sentence. The premise sentence and
two types: event and entity. The type defined in the consts      explanatory sentences should entail the hypothesis sentence.
should be same as the type represented in the logical form       You need to write a step-by-step natural language inference to
codes.                                                           state how the explanatory sentences will entail the hypothesis
...                                                              sentence from the premise sentences.
USER: Here are some examples:                                    Instructions:
###                                                              1. You must elicit the explanatory sentences which are
Provided code:                                                   redundant and not directly related (if there are no redundant
...                                                              or all related state it as no).
Error Identified:                                                2. You must state on which step of the proof each explanatory
                                                                 sentence is used.
1. Error on line 15: Type unification failed: Clash of types     3. You must elicit the used explanatory sentences in the
"entity" and "event"                                             natural language inference steps.
                                                                 USER: Here are some examples:
Type error in application: incompatible operand type             ###
                                                                 Provided Premise Sentence:
...                                                              A group of students are studying non-contact force.
Code Cause This Error:
                                                                 Provided Explanation Sentences:
explanation_1: "∀x c. Cute x ∧ Couple x ∧ Club c ∧ At x c ⟶      1. Non-contact forces can affect objects that are not
(∃y. Couple y ∧ Club c ∧ At y c)"                                touching.
...                                                              2. A magnet attracts magnetic and ferromagnetic metals through
                                                                 magnetism.
Answer:                                                          3. Magnetism does not require contact between objects to act.
From the error found, the error type is type unification         4. A paper clip is a kind of object.
failed, which means the operand type defined in consts is not    5. A magnet is a kind of object.
consistent with the operand in the code.                         6. Magnetism is a kind of force.
As the error indicates the Operator 'At' in code is defined as   7. A kind of something is an example of that something.
At :: "event ⇒ entity ⇒ bool" but in the code it is stated as
At x c where x is defined as entity. That's the reason cause     Provided Hypothesis Sentence:
type unification failed.                                         A paper clip attracted to a magnet is an example of a non-
It should have the same type which can be refined as:            contact force acting on an object.
```
...                                                              Natural Language Inference Steps:
Couple :: "entity ⇒ bool"                                        1. As we need to infer the hypothesis, we need to find the
  Club :: "entity ⇒ bool"                                        information of paper clip, magnet, non-contact force and
  At :: "entity ⇒ entity ⇒ bool"                                 object. The action event of attracted and acting. The
  Cute :: "entity ⇒ bool"                                        relationship of is an example of.
                                                                 2. From the premise, we can get the information of non-contact
(* Explanation 1: A cute couple at a club means a couple is at   force.
a club. *)                                                       3. From explanation 4 and 5, we deduce that both a paper clip
axiomatization where                                             and a magnet are objects.
  explanation_1: "∀x c. Cute x ∧ Couple x ∧ Club c ∧ At x c ⟶    4. Explanation 2 establishes that a magnet can attract certain
(∃y. Couple y ∧ Club c ∧ At y c)"                                metals through magnetism, which is a force (due to explanation
                                                                 6).
theorem hypothesis:                                              ...
  (* Premise: A cute couple at a club *)
  assumes asm: "Cute x ∧ Couple x ∧ Club c ∧ At x c"             Explanation 1 is redundant. There is no not directly related
  (* Hypothesis: The couple is at a club. *)                     explanation sentence.
  shows "∃x. Couple x ∧ Club c ∧ At x c"                         The proof steps use explanation 2, explanation 3, explanation
proof -                                                          4, explanation 5, explanation 6, explanation 7.

qed                                                              ###
                                                                 ...
end                                                              ###
```
The At :: "event ⇒ entity ⇒ bool" has been refined as At ::      <<<<<<<<<<<<<<<<<<<<<<<
"eneity ⇒ entity ⇒ bool", then the types are consistent for      Strictly follow the instructions that I have claimed.
both consts and following logical code.
###                                                              Provided Premise Sentence:
                                                                 {{premise}}
<<<<<<<<<<<<<<<<<<<<<<<
Strictly follow the instructions that I have claimed.            Provided Explanation Sentences:
Provided code:                                                   {{explanation}}
{{code}}
                                                                 Provided Hypothesis Sentence:
Error Identified:                                                {{hypothesis}}
{{error_detail}}
                                                                 Natural Language Inference Steps:
Code Cause This Error:
{{code_cause_error}}

Answer:
                                                                 Figure 18: Prompts for how to make a step-by-step
```
answer code goes here (complete refined isabelle code)           preliminary inference strategy
```



Figure 17: Prompts for how to refine the identified
syntax errors in the constructed code
                                                                 SYSTEM: You are an expert in Isabelle theorem prover, first-
SYSTEM: You are an expert in Isabelle theorem prover, first-
                                                                 order, Davidsonian event semantics and natural language
order logic and Davidsonian event semantics. You will be
                                                                 inference. You will be provided with three types of sentences:
provided with an Isabelle code which consistent of some
                                                                 Premise Sentence, Explanation Sentence and Hypothesis
axioms, a theorem hypothesis that needs to be proven. The        sentence.
logical form of axioms indicates some explanatory sentences,
                                                                 ...
the logical form after "assume asm:" indicates a premise
                                                                 Some instructions:
sentence and the logical form after "shows" indicates a          1. Only refine the related axioms/explanatory sentence in
hypothesis sentence.
                                                                 natural language sentences.
...                                                              ...
Some instructions:
                                                                 USER: Here are some examples:
1. 'sorry' and ‘fix’ command is not allowed.
                                                                 ###
...
                                                                 Provided Premise Sentence:
USER: Here are some examples:
                                                                 ...
###                                                              Natural Language Inference steps:
Provided Isabelle Code:
                                                                 1. To infer the hypothesis, we need to identify the
```
                                                                 information related to a tennis ball, water, and the action of
...
                                                                 floating. The relationship of "will" indicates a future or
begin
                                                                 potential action.
typedecl entity
                                                                 ...
typedecl event
consts
                                                                 Isabelle code:
  PlantReproduction :: "entity ⇒ bool"
                                                                 ...
...
(* Explanation 1: Plant reproduction often requires pollen. *)
                                                                 (* Explanation 5: water is a kind of liquid. *)
axiomatization where                                             axiomatization where
  explanation_1: "∀x y e. PlantReproduction x ∧ Pollen y ∧
                                                                   explanation_5: "∀x. Water x ⟶ Liquid x"
Require e ∧ Agent e x ∧ Patient e y"
                                                                 ...
theorem hypothesis:
                                                                 proof -
  (* Premise: Students are studying plant reproduction             from asm have "TableTennisBall x " by simp
process. *)
                                                                   then have "Object x" using explanation_1 by blast
  assumes asm: "Students x ∧ PlantReproduction y ∧ Studying e
                                                                   then obtain e1 where e1: "Contains e1 ∧ Agent e1 x ∧ Patient
∧ Agent e x ∧ Patient e y"
                                                                 e1 y" using explanation_2 by blast
  (* Hypothesis: Plant reproduction often requires bees. *)      ...
  shows "∃x y e. PlantReproduction x ∧ Bee y ∧ Require e ∧       qed
Agent e x ∧ Patient e y"
                                                                 ...
proof -
                                                                 Proof failed at:
qed
                                                                 then have "Object x" using explanation_1 by blast
end
                                                                 Refine strategy:
```
                                                                 From the provided error location, it failed at the step of
Provided Natural Language Inference Strategy:
                                                                 "then have "Object x" using explanation_1 by blast" using
                                                                 explanation 1.
1. As we need to infer the hypothesis, we need to find the
                                                                 ...
information of plant, reproduction process, requires action      Updated explanatory sentences:
and bees.                                                        1. a table tennis ball is a kind of object.
2. From explanation 1, we get the information of plant
                                                                 2. a tennis ball contains air.
reproduction, which requires pollen.
                                                                 3. something that contains air is usually buoyant.
...
                                                                 4. buoyant means able to float in a liquid or gas.
Explanation 3 and 4 is not related and Explanation 5 is          5. water is a kind of liquid.
redundant.
                                                                 ###
The proof steps use explanation 1 and explanation 2.
                                                                 ...
                                                                 <<<<<<<<<<<<<<<<<<<<<<<
Answer:
                                                                 Strictly follow the instructions that I have claimed.
```
proof -
                                                                 Provided Premise Sentence:
  from asm have "PlantReproduction x" by simp
                                                                 {{premise}}
  then obtain e1 where e1: "Require e1 ∧ Agent e1 x ∧ Patient
e1 y" using explanation_1 by blast                               Provided Explanation Sentences:
  then have "Bee y" using explanation_2 by blast                 {{explanation}}
  have conclusion: "Require e1 ∧ Agent e1 x ∧ Patient e1 y"
using e1 by simp
                                                                 Provided Hypothesis Sentence:
  show ?thesis using asm conclusion `Bee y` by blast
                                                                 {{hypothesis}}
qed
```
                                                                 Natural Language Inferece steps:
###                                                              {{rough_inference}}
...
<<<<<<<<<<<<<<<<<<<<<<<
                                                                 Isabelle code:
Strictly follow the instructions that I have claimed.
                                                                 {{isabelle_code}}
Provided Isabelle Code:                                          Proof failed at:
{{isabelle_code}}
                                                                 {{error_code}}
Provided Natural Language Inference Strategy:
                                                                 Refine strategy:
{{rough_inference}}

Answer:
                                                                 Updated explanatory sentences:


Figure 19: Prompts for how to build a proof for Is-              Figure 20: Prompts for how to refine the explanatory
abelle/HOL proof assistant                                       sentences
           Dataset     Sentences                        Explanation                        Iteration Validity
           e-SNLI      Premise: A woman in black        The lady is looking through a         0      Invalid
                       framed glasses peruses a photo   photo album which is a type of
                       album while sitting in a red     book.
                       wicker chair.
                       Hypothesis: There is a lady
                       with a book.
           e-SNLI      Premise: A woman in black        A woman can be referred to as a       1      Invalid
                       framed glasses peruses a photo   lady. A photo album is a type of
                       album while sitting in a red     book.
                       wicker chair.
                       Hypothesis: There is a lady
                       with a book.
           e-SNLI      Premise: A woman in black        A woman can be referred to as a       2      Valid
                       framed glasses peruses a photo   lady. A photo album is a type of
                       album while sitting in a red     book. If a woman is perusing a
                       wicker chair.                    photo album, then the woman is
                       Hypothesis: There is a lady      with a book.
                       with a book.

  Table 1: An example of how the explanation sentences in e-SNLI can be refined with Explanation-Refiner




theory question_28_0

imports Main

begin
typedecl entity
typedecl event

consts
  Lady :: "entity ⇒ bool"
  PhotoAlbum :: "entity ⇒ bool"
  Book :: "entity ⇒ bool"
  Looking :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  Patient :: "event ⇒ entity ⇒ bool"
  Woman :: "entity ⇒ bool"
  Glasses :: "entity ⇒ bool"
  BlackFramed :: "entity ⇒ bool"
  Chair :: "entity ⇒ bool"
  Red :: "entity ⇒ bool"
  Wicker :: "entity ⇒ bool"
  Peruses :: "event ⇒ bool"
  Sitting :: "entity ⇒ entity ⇒ bool"
  With :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: The lady is looking through a photo album which is a type of book. *)
axiomatization where
    explanation_1: "∃x y e. Lady x ∧ PhotoAlbum y ∧ Book y ∧ Looking e ∧ Agent e x ∧ Patient e y"

theorem hypothesis:
(* Premise: A woman in black framed glasses peruses a photo album while sitting in a red wicker chair. *)
assumes asm: "Woman x ∧ Glasses x ∧ BlackFramed x ∧ PhotoAlbum y ∧ Chair z ∧ Red z ∧ Wicker z ∧ Peruses e ∧ Agent e
x ∧ Patient e y ∧ Sitting x z"
(* Hypothesis: There is a lady with a book. *)
shows "∃x y. Lady x ∧ Book y ∧ With x y"
proof -
  from asm have "Woman x ∧ PhotoAlbum y" by blast
  from this have "Lady x ∧ Book y" using explanation_1 by blast
  then show ?thesis using `Lady x` `Book y` by blast
qed

end


                             Figure 21: The Isabelle theory code for table 1 iteration 0
theory question_28_1

imports Main

begin
typedecl entity
typedecl event

consts
  Woman :: "entity ⇒ bool"
  Lady :: "entity ⇒ bool"
  PhotoAlbum :: "entity ⇒ bool"
  Book :: "entity ⇒ bool"
  Glasses :: "entity ⇒ bool"
  BlackFramed :: "entity ⇒ bool"
  Peruses :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  Patient :: "event ⇒ entity ⇒ bool"
  Chair :: "entity ⇒ bool"
  Red :: "entity ⇒ bool"
  Wicker :: "entity ⇒ bool"
  SittingIn :: "entity ⇒ entity ⇒ bool"
  With :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: A woman can be referred to as a lady. *)
axiomatization where
    explanation_1: "∀x. Woman x ⟶ Lady x"

(* Explanation 2: A photo album is a type of book. *)
axiomatization where
    explanation_2: "∀x. PhotoAlbum x ⟶ Book x"

theorem hypothesis:
(* Premise: A woman in black framed glasses peruses a photo album while sitting in a red wicker chair. *)
assumes asm: "Woman x ∧ Glasses x ∧ BlackFramed x ∧ PhotoAlbum y ∧ Peruses e ∧ Agent e x ∧ Patient e y ∧ Chair z ∧
Red z ∧ Wicker z ∧ SittingIn x z"
(* Hypothesis: There is a lady with a book. *)
shows "∃x y. Lady x ∧ Book y ∧ With x y”
proof -
  from asm have "Woman x" by blast
  then have "Lady x" using explanation_1 by blast
  from asm have "PhotoAlbum y" by blast
  then have "Book y" using explanation_2 by blast
  show ?thesis using `Lady x` `Book y` by blast
qed

end




                           Figure 22: The Isabelle theory code for table 1 iteration 1
theory question_28_2

imports Main

begin
typedecl entity
typedecl event

consts
  Woman :: "entity ⇒ bool"
  Lady :: "entity ⇒ bool"
  PhotoAlbum :: "entity ⇒ bool"
  Book :: "entity ⇒ bool"
  Perusing :: "event ⇒ bool"
...

(* Explanation 1: A woman can be referred to as a lady. *)
axiomatization where
    explanation_1: "∀x. Woman x ⟶ Lady x"

(* Explanation 2: A photo album is a type of book. *)
axiomatization where
    explanation_2: "∀x. PhotoAlbum x ⟶ Book x"

(* Explanation 3: If a woman is perusing a photo album, then the woman is with a book. *)
axiomatization where
    explanation_3: "∀x y e. Woman x ∧ PhotoAlbum y ∧ Perusing e ∧ Agent e x ∧ Patient e y ⟶ With x y"

theorem hypothesis:
(* Premise: A woman in black framed glasses peruses a photo album while sitting in a red wicker chair. *)
assumes asm: "Woman x ∧ Glasses x ∧ BlackFramed x ∧ PhotoAlbum y ∧ Chair z ∧ RedWicker z ∧ Perusing e ∧ Agent e x ∧
Patient e y ∧ SittingIn x z"
(* Hypothesis: There is a lady with a book. *)
shows "∃x y. Lady x ∧ Book y ∧ With x y"
proof -
  from asm have "Woman x ∧ PhotoAlbum y ∧ Perusing e ∧ Agent e x ∧ Patient e y" by blast
  then have "With x y" using explanation_3 by blast
  from asm have "Woman x" by blast
  then have "Lady x" using explanation_1 by blast
  from asm have "PhotoAlbum y" by blast
  then have "Book y" using explanation_2 by blast
  show ?thesis using `Lady x` `Book y` `With x y` by blast
qed

end




                           Figure 23: The Isabelle theory code for table 1 iteration 2
           Dataset     Sentences                           Explanation                          Iteration Validity
           e-SNLI      Premise: A male bartender           A bartender, who is a person, is        0      Invalid
                       dressed in all black with his       wearing black.
                       sleeves rolled up to elbow height
                       making a drink in a martini
                       glass.
                       Hypothesis: A person in black
           e-SNLI      Premise: A male bartender           A bartender is a person. If a per-      1      Invalid
                       dressed in all black with his       son is wearing black, then the
                       sleeves rolled up to elbow height   person is in black.
                       making a drink in a martini
                       glass.
                       Hypothesis: A person in black
           e-SNLI      Premise: A male bartender           A bartender is a person. If a per-      2      Valid
                       dressed in all black with his       son is dressed in black, then the
                       sleeves rolled up to elbow height   person is in black.
                       making a drink in a martini
                       glass.
                       Hypothesis: A person in black

  Table 2: An example of how the explanation sentences in e-SNLI can be refined with Explanation-Refiner




theory question_66_0

imports Main

begin
typedecl entity
typedecl event

consts
  Bartender :: "entity ⇒ bool"
  Person :: "entity ⇒ bool"
  Black :: "entity ⇒ bool"
  Wearing :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  Patient :: "event ⇒ entity ⇒ bool"
  Male :: "entity ⇒ bool"
  Drink :: "entity ⇒ bool"
  MartiniGlass :: "entity ⇒ bool"
  Making :: "event ⇒ bool"
  In :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: A bartender, who is a person, is wearing black. *)
axiomatization where
    explanation_1: "∃x e. Bartender x ∧ Person x ∧ Black x ∧ Wearing e ∧ Agent e x ∧ Patient e x"

theorem hypothesis:
(* Premise: A male bartender dressed in all black with his sleeves rolled up to elbow height making a drink in a
martini glass. *)
assumes asm: "Bartender x ∧ Male x ∧ Black x ∧ Drink y ∧ MartiniGlass z ∧ Making e ∧ Agent e x ∧ Patient e y ∧ In z
y"
(* Hypothesis: A person in black *)
shows "∃x. Person x ∧ Black x"
proof -
   from asm have "Bartender x ∧ Black x" by blast
   from this have "Person x ∧ Black x" using explanation_1 by blast
   then show ?thesis by blast
qed

end


                              Figure 24: The Isabelle theory code for table 2 iteration 0
theory question_66_1

imports Main

begin
typedecl entity
typedecl event

consts
  Bartender :: "entity ⇒ bool"
  Person :: "entity ⇒ bool"
  Wearing :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  Black :: "event ⇒ bool"
  InBlack :: "entity ⇒ bool"
  Male :: "entity ⇒ bool"
  Dress :: "event ⇒ bool"
  Sleeves :: "entity ⇒ bool"
  RolledUp :: "event ⇒ bool"
  ElbowHeight :: "event ⇒ bool"
  Drink :: "entity ⇒ bool"
  MartiniGlass :: "entity ⇒ bool"
  Making :: "event ⇒ bool"
  Patient :: "event ⇒ entity ⇒ bool"
  In :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: A bartender is a person. *)
axiomatization where
    explanation_1: "∀x. Bartender x ⟶ Person x"

(* Explanation 2: If a person is wearing black, then the person is in black. *)
axiomatization where
    explanation_2: "∀x e. Person x ∧ Wearing e ∧ Agent e x ∧ Black e ⟶ InBlack x"

theorem hypothesis:
(* Premise: A male bartender dressed in all black with his sleeves rolled up to elbow height making a drink in a
martini glass. *)
assumes asm: "Bartender x ∧ Male x ∧ Black e1 ∧ Dress e1 ∧ Agent e1 x ∧ Sleeves x ∧ RolledUp e2 ∧ Agent e2 x ∧
ElbowHeight e2 ∧ Drink y ∧ MartiniGlass z ∧ Making e3 ∧ Agent e3 x ∧ Patient e3 y ∧ In z y"
(* Hypothesis: A person in black *)
shows "∃x. Person x ∧ InBlack x"
proof -
  from asm have "Bartender x" by blast
  then have "Person x" using explanation_1 by blast
  from asm have "Black e1 ∧ Dress e1 ∧ Agent e1 x" by blast
  then have "InBlack x" using `Person x` explanation_2 by blast
  show ?thesis using `Person x` `InBlack x` by blast
qed

end




                           Figure 25: The Isabelle theory code for table 2 iteration 1
theory question_66_2

imports Main

begin
typedecl entity
typedecl event

consts
  Bartender :: "entity ⇒ bool"
  Person :: "entity ⇒ bool"
  DressedInBlack :: "entity ⇒ bool"
  InBlack :: "entity ⇒ bool"
  Male :: "entity ⇒ bool"
  SleevesRolledUpToElbowHeight :: "entity ⇒ bool"
  Drink :: "entity ⇒ bool"
  MartiniGlass :: "entity ⇒ bool"
  Making :: "event ⇒ bool"
  Agent :: "event ⇒ entity ⇒ bool"
  Patient :: "event ⇒ entity ⇒ bool"
  In :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: A bartender is a person. *)
axiomatization where
    explanation_1: "∀x. Bartender x ⟶ Person x"

(* Explanation 2: If a person is dressed in black, then the person is in black. *)
axiomatization where
    explanation_2: "∀x. Person x ∧ DressedInBlack x ⟶ InBlack x"

theorem hypothesis:
(* Premise: A male bartender dressed in all black with his sleeves rolled up to elbow height making a drink in a
martini glass. *)
assumes asm: "Male x ∧ Bartender x ∧ DressedInBlack x ∧ SleevesRolledUpToElbowHeight x ∧ Drink y ∧ MartiniGlass z ∧
Making e ∧ Agent e x ∧ Patient e y ∧ In z y"
(* Hypothesis: A person in black *)
shows "∃x. Person x ∧ InBlack x"
proof -
  from asm have "Bartender x ∧ DressedInBlack x" by blast
  then have "Person x ∧ DressedInBlack x" using explanation_1 by blast
  then have "Person x ∧ InBlack x" using explanation_2 by blast
  then show ?thesis by blast
qed

end



                           Figure 26: The Isabelle theory code for table 2 iteration 2
