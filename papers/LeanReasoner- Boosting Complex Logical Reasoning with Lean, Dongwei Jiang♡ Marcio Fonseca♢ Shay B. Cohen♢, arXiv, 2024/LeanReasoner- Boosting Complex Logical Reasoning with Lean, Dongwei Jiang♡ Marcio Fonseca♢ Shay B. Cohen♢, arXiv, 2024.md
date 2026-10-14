                                                    LeanReasoner: Boosting Complex Logical Reasoning with Lean

                                                           Dongwei Jiang♡ Marcio Fonseca♢ Shay B. Cohen♢
                                                             ♡
                                                               Johns Hopkins University ♢ University of Edinburgh
                                                   djiang21@jhu.edu m.fonseca@ed.ac.uk scohen@inf.ed.ac.uk




                                                                    Abstract                                bolic solvers essentially act as a rigorous check-
                                                                                                            point, ensuring that the model outputs align with
                                                 Large language models (LLMs) often struggle
                                                 with complex logical reasoning due to logical              logical rules, thereby mitigating the issue of logic
                                                                                                            inconsistency. In these approaches, solvers may
arXiv:2403.13312v1 [cs.CL] 20 Mar 2024




                                                 inconsistencies and the inherent difficulty of
                                                 such reasoning. We use Lean, a theorem prov-               range from being completely deterministic, like
                                                 ing framework, to address these challenges. By             SymPy (He-Yueya et al., 2023), or relying on a
                                                 formalizing logical reasoning problems into                combination of heuristics and basic machine learn-
                                                 theorems within Lean, we can solve them by                 ing techniques, as is the case with Pyke (Pan et al.,
                                                 proving or disproving the corresponding theo-              2023) and Z3 (Ye et al., 2023; de Moura and
                                                 rems. This method reduces the risk of logical
                                                 inconsistencies with the help of Lean’s sym-
                                                                                                            Bjørner, 2008). While this approach successfully
                                                 bolic solver. It also enhances our ability to treat        addresses hallucinations, it still struggles with more
                                                 complex reasoning tasks by using Lean’s ex-                complex problems.
                                                 tensive library of theorem proofs. Our method                 As a powerful theorem prover and a versatile pro-
                                                 achieves state-of-the-art performance on the               gramming language, Lean (de Moura et al., 2015)
                                                 FOLIO dataset and achieves performance near
                                                                                                            presents a compelling solution to connect symbolic
                                                 this level on ProofWriter. Notably, these results
                                                 were accomplished by fine-tuning on fewer
                                                                                                            solvers with linguistic resources. Much like sym-
                                                 than 100 in-domain samples for each dataset.1              bolic solvers, Lean has a strict checking system
                                                                                                            that ensures each reasoning step is certified. What
                                         1       Introduction                                               distinguishes it, however, is its additional function-
                                         Logical reasoning, a bedrock of intelligence and                   ality as a programming language developed specifi-
                                         a core capability of humans, has been a challeng-                  cally for theorem proving. Every day, a substantial
                                         ing issue for machine learning systems for a long                  amount of code is written in Lean, capturing rea-
                                         time. LLMs, despite their impressive abilities to un-              soning “nuggets” with step-by-step rationals that
                                         derstand and generate natural language, often fall                 are useful for training LLMs. A few recent studies
                                         short when dealing with complex logical reasoning                  have already tapped into Lean for mathematical
                                         tasks. They frequently suffer from logical inconsis-               theorem-proving tasks (Polu et al., 2023; Han et al.,
                                         tencies, where the model hallucinates and makes                    2022a; Lample et al., 2022), showing its potential
                                         statements not grounded in premises, leading to                    in tackling difficult reasoning challenges.
                                         spurious results (Saparov and He, 2023; Dasgupta                      In this paper, we propose LeanReasoner, a Lean-
                                         et al., 2022).                                                     based framework to tackle logical reasoning prob-
                                            Recent advances in AI have adopted a struc-                     lems. We use LLMs to formalize natural language
                                         tured approach to tackle these reasoning problems                  context into Lean and fine-tune a custom model
                                         by splitting them into symbolic formalization and                  on these problems using a modest amount of data
                                         problem-solving (He-Yueya et al., 2023; Pan et al.,                annotated ourselves. As we use LLMs to dynam-
                                         2023; Ye et al., 2023). Specifically, the formal-                  ically generate solutions within the Lean environ-
                                         ization step is often handled by a large language                  ment, our approach stands in stark contrast to the
                                         model, while problem-solving is handled by an off-                 static, pre-defined solution-finding methods of Log-
                                         the-shelf symbolic solver. In this approach, sym-                  icLM (Pan et al., 2023), which only rely on tradi-
                                             1
                                                                                                            tional techniques like forward and backward chain-
                                            Our   code  and  data   is available                       at
                                         https://github.com/Some-random/                                    ing, and SATLM (Ye et al., 2023), which operates
                                         theorem-proving-reasoning.                                         within the Z3 environment using a suite of prede-
termined algorithms and heuristics. The adaptive            • Formalized context refers to the representation
nature of LLMs as a solution-finding tool allows              of context in Lean. For example, the formal-
our system to evolve continuously, harnessing a               ized context for our example would be: axiom
vast array of reasoning data and information.                 A1 is_cat Hudson, axiom A2 ∀x, is_cat x →
   Our contributions in this paper are three-fold.            is_animal x and axiom A3 ∀x, is_cat x → of-
                                                              ten_meow x.
• To our knowledge, this is the first attempt to use
                                                            • Formalized question: Given that Lean operates
  Lean, traditionally associated with mathematical
                                                              as a theorem prover, questions are transformed
  theorem proving, for natural language logical
                                                              into dual theorems: one asserting the positive
  reasoning. This effort highlights a possible inter-
                                                              stance and the other negating it. For the given ex-
  section between mathematical theorem proving
                                                              ample, the formalized questions would be: Theo-
  and logical reasoning.
                                                              rem hudson_often_meows: often_meow Hudson
• Our research revealed that incorporating pre-               and Theorem not_hudson_often_meows: ¬ of-
  training data from mathematical theorem proofs              ten_meow Hudson.
  enhances the development of a more effective
                                                            • Goal: In the context of proving theorems with
  solver for logical reasoning compared to pre-
                                                              Lean, a "goal" is a logical statement that needs
  vious techniques. Additionally, this approach
                                                              to be proven true, given a set of axioms and rules.
  enabled us to achieve SOTA results on FOLIO.
                                                              When we set out to answer a question using the
• We make available the training data accumu-                 Lean prover, this question becomes our root goal.
  lated in this research, comprising 100 Lean-                At that point, we can apply various instructions
  formalized logic reasoning problems from                    in Lean to simplify or break down this primary
  ProofWriter, along with 27 analogous formal-                goal and generate intermediate goals.
  izations from FOLIO. The corresponding proofs
  in Lean are also included.                                    For instance, using our earlier examples,
                                                                if the root goal is proving Theorem hud-
2       Problem Definition and Notation                         son_often_meows: often_meow Hudson, an in-
                                                                termediate goal might be proving that Hudson is
The task we aim to solve is logical reasoning, tak-             a cat. We aim to resolve each intermediate goal
ing the form of multi-choice questions given a nat-             using our provided context, gradually working
ural language context. The answer to the question               our way towards proving the root goal. Once all
can be logically deduced based on the context. The              intermediate goals are resolved, we have effec-
framework we use for solving the problem is Lean.2              tively proven our root goal, and the proof search
Lean is an open-source theorem-proving program-                 concludes successfully.
ming language with vibrant community support.
                                                            • Tactics are the instructions in the Lean theorem
Its current base includes over 100,000 theorems
                                                              proving language that are used to manipulate
and 1,000,000 lines of code.3 We use Lean as a
                                                              goals to obtain a proof for a given goal. For
generic theorem prover, outside of mathematics.
                                                              example, apply A3 Hudson is a tactic that uses
   The task and our solution to it, consist of the
                                                              modus ponens on the Goal often_meow Hudson
following components:
                                                              and transforms it to a new Goal is_cat Hudson
• Context, which is composed of natural language
  utterances, composing a set of rules and facts.             A diagram of these components and the relations
  For example: Hudson is a cat, all cats are ani-           between them is depicted in Figure 1. This proce-
  mals, and cats often meow.                                dure is framed within the language of the Lean
                                                            theorem prover as a goal-satisfying process.
• Question, which denotes the posed question. For
  example, Does Hudson often meow?
                                                            3    LeanReasoner
• Options is a set of available answers (discrete
  categories) from which an answer can be chosen.           Our framework, LeanReasoner, is composed of
  For example, True, False or Unknown.                      four main components: a formalizer, a tactic gen-
    2                                                       erator, a proof search mechanism, and a result
   https://leanprover.github.io/.
    3
   https://en.wikipedia.org/wiki/Lean_                      interpreter. The formalizer converts the context
(proof_assistant).                                          and question to formalized context and formalized

                                                        2
                                                                         Context, Question and Options

   Context: The cow is big. The cow likes the dog. The cow visits the dog. The dog needs the cow The cow needs the cow. If something visits the dog and the dog needs the
             cow then it needs the cow. If the dog visits the cow then the cow visits the dog. If something needs the cow and the cow likes the dog then it likes the cow.

                                  Question: Does the Cow like the Cow                                                       Options: True, False or Unknown

 Formalizer                        Formalizer
                                           Formalizer                                  Tactic Generator + Proof Search                                    Result Interpreter
 constant Cow: obj                           axiom T1: Big Cow                                            Likes Cow Cow                                       Check every proof path
 constant Dog: obj                           axiom T2: Likes Cow Dog
                                                                                apply R4       apply R3 Cow                      sorry
 constant Cat: obj                           axiom T3: Visits Cow Dog
                                                                                                                                                                      Exists path
                                                                            Needs Cat Cow ∧           Needs Cow Cow ∧
 constant Big: obj -> Prop                   axiom T4: Needs Dog Cow                                                                 No Goals   Unknown              that found a
                                                                             Likes Cow Cat             Likes Cow Dog
 constant Likes: obj->obj->Prop              axiom T5: Needs Cow Cow                                                                                                     proof
                                                                                                  split               exact T5
 constant Needs: obj->obj->Prop
 axiom R1: ∀ x : obj, Visits x Dog ∧ Needs Dog Cow → Needs x Cow                           Needs Cow Cow,
                                                                                                                     Likes Cow Dog
                                                                                   …                                                                                  Theorem is
 axiom R2: Visits Dog Cow → Visits Cow Dog                                                  Likes Cow Dog                                         False              the positive
 axiom R3: ∀ x : obj, Needs x Cow ∧ Likes Cow Dog → Likes x Cow                    apply R1 Cow                                exact T2                                version
 axiom R4: ∀ x : obj, Needs Cat Cow ∧ Likes Cow Cat → Likes Cow Cow
                                                                                                  …                       No Goals
 theorem does_cow_like_cow: Likes Cow Cow                                                                                                                                True




Figure 1: An overview of our approach. The natural language context is first processed by the “formalizer”. It
then advances to the proof search stage, where all the tactics (in red) generated by the “tactic generator” are used to
manipulate goals. Finally, the outcome is interpreted by the “result interpreter”.

question. The tactic generator then generates tac-                                             two parts: a retriever that employs retrieval mecha-
tics based on premises extracted from the formal-                                              nisms to explicitly select premises when provided
ized context. The proof search mechanism oversees                                              with the current goal, and a generator that generates
tactic execution and goal expansion. The result in-                                            tactics using the goal and the retrieved premises.
terpreter analyses the output of the proof search                                                 The division of the problem-solving task into
and identifies the correct answer in the options. In                                           premise selection and tactic generation simplifies
this section, we detail each of those components.                                              the process and facilitates easier troubleshooting.
3.1      Formalizer                                                                            It isolates the source of potential issues, be it in
                                                                                               the premise selection or the tactic generation, thus
As formalizers, we used OpenAI models text-                                                    reducing the complexity of the problem. Also, this
davinci-003 (GPT-3) and GPT-4 (OpenAI, 2023).                                                  division of responsibilities eases the burden on the
For text-davinci-003, we followed the same prompt-                                             tactic generator. Choosing the right premise with
ing approach as Logic-LM (Pan et al., 2023) to                                                 numerous distractions is challenging, especially in
separate task specifications and problems, thereby                                             logical reasoning problems when several options
enabling the model to continue with the task of                                                might seem promising for the current step but will
formalization through next-token-prediction. For                                               not ultimately lead to the desired goal.
GPT-4, we used similar prompts but included the
task specification in the system prompt.                                                          The premise retrieval component of our process
    There is no automatic way to assert all the en-                                            draws from the Dense Passage Retriever (DPR)
tities, relationships, and constraints of the context                                          (Karpukhin et al., 2020). Provided with a goal g
have been captured by the formalized result. How-                                              as the query and a set of candidate premises P , it
ever, the syntax of the formalized result can be                                               generates a ranked list of m premises from P . In
checked by Lean. Because correct syntax is a pre-                                              DPR, both g and P are treated as raw texts that are
requisite for downstream theorem proving, if an                                                embedded in a vector space. We then retrieve the
error is encountered during compilation, we pro-                                               top m premises that maximize the cosine similarity
vide the error message generated by Lean along                                                 between the goal and the premise. For tactic gen-
with the faulty formalization and ask the formal-                                              eration, we use a standard sequence-to-sequence
izer to regenerate the result. We further manually                                             model. The goal and the premises are concatenated
inspect the formalizer in §5. We note that we take                                             together as a string to generate new tactics.
a strict approach, and if the formalizer fails more                                               As a baseline, we also prompt GPT-4 to generate
than once, then the problem is counted as not being                                            proofs. For cases when the chosen theorem to prove
correctly solved.                                                                              aligns with the answer (say the chosen theorem is
                                                                                               the positive stance of the question and the answer is
3.2      Tactic Generator                                                                      Y ES), we present GPT-4 with the correct proof as
The model we used for tactic generation is Re-                                                 part of the prompt. Conversely, if the answer does
Prover (Yang et al., 2023). This model contains                                                not align with the chosen theorem or the answer is

                                                                                           3
U NKNOWN, the formalized theorem is unprovable.              for each search, which is usually sufficient. We
In those cases, we still encourage the model to              provided more analysis of the errors made by tactic
engage in step-by-step reasoning, even though it             generator in the experiment section.
will eventually hit a roadblock. An example of the
prompt to GPT-4 can be found in Appendix A.1.                3.4    Result Intepreter
                                                             If the correct answer is Unknown, we only regard
3.3   Proof Search                                           the result as correct if neither True nor False can
                                                             be proven. All datasets investigated in this study
The proof search module controls the overall search
                                                             only contain questions with only one correct an-
process that selects tactics and maintains states dur-
                                                             swer. Consequently, if the proof system verifies
ing proof construction. Essentially, the goal of the
                                                             more than one option, the response is immediately
search method is to build a proof tree that incre-
                                                             marked as incorrect.
mentally evolves the goal through tactic invoca-
tions. This approach was first introduced in GPT-
                                                             4     Experimental Setup
F (Polu and Sutskever, 2020). LeanDoJo (Yang
et al., 2023), a recently released framework that            We now describe our experimental setup: the
enables interaction with Lean programmatically,              datasets we used for evaluation and model training
subsequently provided an implementation of this              and the details of model training.
method, which we use for our study.
   As a reference, the middle part of Figure 1 pro-          4.1    Evaluation Data
vides a practical illustration of this process. Start-       In our evaluation, we use two common logical rea-
ing from the root goal, for each given proof goal,           soning datasets as testbeds:
we explore 64 possible tactics. All goals are main-             ProofWriter: This deductive logical reasoning
tained in a priority queue and expanded based on             dataset presents problems in an intuitive language
cumulative log probabilities of the goal. The cumu-          form. We incorporated the Open-World Assump-
lative log probability is defined as the summation           tion (OWA) subset as per (Pan et al., 2023), where
of the log probabilities of the tactics that brought         each instance is characterized by a {problem, goal}
us to the goal from the root. This implies that we           pairing. The label for each pair contains T RUE,
tend to expand those goals where our generative              FALSE, or U NKNOWN. It encompasses five seg-
model has the highest global confidence.                     ments based on the required reasoning depth. Our
   To enhance search efficiency and circumvent po-           focus is the depth-5 subset, which is the most chal-
tential loops, we have incorporated a mechanism              lenging one. To get a fair comparison against Logic-
that stops the expansion of a node N if we have              LM, we used the same 600 sample tests, ensuring
already explored another node M with a state se-             an even label distribution.
quence that prefixes N . Essentially, if the current            FOLIO: Unlike ProofWriter, FOLIO is con-
goal being explored contains all the elements of a           structed using first-order logic. This increases the
previously explored goal, then it shouldn’t be fur-          complexity of the proving part. The dataset also
ther expanded. This is based on the observation              presents problems in a more natural wording, with
that if we have already assessed the potential paths         relationships that are considerably more complex.
and outcomes for a specific goal, then exploring             Such a combination of advanced logic and rich lin-
a more generalized version of the same goal is re-           guistic structure makes the formalization task in
dundant. Such a mechanism avoids unnecessary                 FOLIO substantially tougher than in ProofWriter.
repetitions, which streamlines the search process            For our analysis, we turned to the entire FOLIO
and improves the overall efficiency. Moreover, we            test set, encompassing 204 examples.
define a valid proof as one that is devoid of “cheat-
ing” tactics (such as sorry) that tell Lean to assume        4.2    Training Data for Domain Adaptation
that the current goal is completed, even though it           Regarding the data for model training, we collected
has not been proven. This means that every path              100 theorem proofs for ProofWriter and 27 theorem
containing “cheating” tactics is disregarded.                proofs for FOLIO, where each problem’s proof
   Errors in the search process typically manifest in        was either manually annotated or collected from
two ways: a timeout or an exhaustion of nodes to             successful proofs generated by GPT-4. The data
search. We have allocated a three-minute window              collection took about eight days.

                                                         4
   During data annotation, we adopted two diver-             and rule are counted as accurate. We manually
gent approaches for constructing proofs. One ap-             examined 100 questions from ProofWriter’s vali-
proach emulated a straightforward strategy, encom-           dation set and 40 questions from FOLIO’s training
passing a detailed procedure with all of the interme-        set. The findings have been summarized in Table 1.
diate steps and lemmas, similar to how we humans
might derive proof when given theorem-proving                Comparison of formalization accuracy. The
tasks. Conversely, the second approach resembles             formalization accuracy of ProofWriter is much
the proof formats found in mathlib.4 We gener-               higher than FOLIO. This can be attributed to its
ate more succinct proofs of the same problem by              simpler language structure. In the case of FOLIO,
reducing the number of intermediate lemmas and               although using LLM for formalization helped in
combining multiple tactics into a single compound            filtering out unnecessary details from the natural
tactic. The objective of having two annotations for          language context, there still exists some common
the same problem was to examine the influence of             error patterns. We have illustrated typical GPT-4
annotation style on downstream logical reasoning.            error patterns in Appendix B using a composite
In the following experiments, we use Intuitive to            sample derived from various error instances. Inter-
refer to the first annotation style and Concise to           estingly, Lean’s formalization accuracy is on par
denote the second annotation style. An illustrative          with both Prolog and FOL in Logic-LM. This con-
example is available in Appendix C.                          sistency underscores Lean’s versatility, allowing
   It is important to mention that despite the limited       it to uniformly represent different problem types
data collected, the reasoning patterns for logical           within a single framework.
reasoning likely mirror those found in mathemati-
                                                             Adding textual comments increases formaliza-
cal reasoning, which were potentially learned dur-
                                                             tion accuracy. We observed improved results
ing pretraining. The main purpose of this data
                                                             when formalized code was paired with descrip-
collection is domain adaptation to transfer from
                                                             tive textual comments (example in Appendix A.1)
math to natural language logical reasoning.
                                                             sourced from the context. This approach further
4.3    Model Training                                        splits the formalization task into two subtasks: 1)
                                                             linking textual context with formalized code and 2)
We used the same model structure for pretraining as          generating formalized code based on the prior tex-
in the ReProver paper, namely, Google’s Byte-T5              tual context. These textual cues acted as a bridge
(Xue et al., 2022). We also experimented with the            between raw text and formalized code, enhancing
pretrained ReProver from LeanDoJo (Yang et al.,              the performance of formalization.
2023), which was pretrained on mathlib. The fine-
tuning of our collected data took about six hours on         GPT-3’s performance on formalization is worse
one A100 40G. The hyperparameters are the same               than GPT-4 . The distinction in performance be-
as in the original LeanDoJo paper.                           tween GPT-3 and GPT-4 is evident. While the
                                                             formalization for simpler problems is the same,
5     Results                                                GPT-3 struggles with intricate logic and complex
We present our experimental results, including an            problems. As such, we opted not to use GPT-3
examination of prompting-based baseline, experi-             in further tests. Additionally, we experimented
mental results for LeanReasoner, and a comparison            with the CodeLLAMA (Baptiste Rozière and et.al,
between our work and other baselines.                        2023) model family for similar tasks, but found that
                                                             their accuracy in formalization was significantly
5.1    Prompting-Based Baselines                             lower than that of GPT-3, achieving less than 30%
                                                             on ProofWriter.
Since there is no automated method to verify the
accuracy of formalization, we conducted manual               The proof accuracy of prompting-based base-
examinations of the formalized results to determine          line is very low. The proof accuracy section of
whether errors occur during formalization or proof           the table is determined by whether the generated
generation stages. In this examination, only formal-         proof can be validated successfully in Lean. If
izations that correctly capture every fact, axiom,           the formalization of the question as a theorem is
  4
    https://github.com/                                      correct and the proof can be validated without any
leanprover-community/mathlib                                 error or warning, then we can treat the proof as

                                                         5
                                          ProofWriter                                 FOLIO
                Model
                                   Formalize Prove Answer                 Formalize    Prove      Answer
       GPT-4 Base                    94%       15%    80%                   60%         10%        35%
       GPT-4 Base Comments           99%       15%    80%                   75%         15%        35%
       GPT-4 Base Separate           95%        5%    75%                   60%         10%        40%
       GPT-3 Base Comments           77%       12%    63%                   45%         10%        35%
       Logic-LM                      98%      75.5%   74%                   65%        69.2%       55%
Table 1: Formalization, Proof, and Answer choice accuracy of 100 ProofWriter samples and 40 FOLIO samples
via OpenAI Language Model API, with manual annotation. ‘GPT-4 Base’ serves as our baseline, where few-shot
examples include both formalization and proof generation in a single prompt. In ‘GPT-4 Base Comments’, we
augment these examples with line-by-line comments in Lean code. For ‘GPT-4 Base Separate’, we divide the task
into two parts, using separate prompts for formalization and proof generation. For simplicity, we did not use the
self-refinement technique when evaluating Logic-LM.

valid. However, the accuracy of rendered proofs is           where GT_Prem means ground truth premises and
very low. The issue could stem from assigning too            Pred_Prem means top predicted premises. The sub-
many tasks to the large language model, making it            optimal results of LeanReasoner pretrained solely
challenging to address both within a single prompt.          with math data may be attributed to the domain
Despite our efforts to separate formalization and            mismatch between mathematical theorem proving
proof, the results were still disappointing, which           and logical reasoning. The model frequently makes
highlights GPT-3 and GPT-4’s struggle with gener-            mistakes by attempting to use other, unrelated tac-
ating correct Lean proof. Interestingly, the proof           tics that are useful in mathematical theorem prov-
accuracy of Logic-LM wasn’t as high as we ex-                ing (like ring, linarith) but not applicable in logi-
pected. Upon replicating their code, we found their          cal reasoning. Furthermore, the accuracy for FO-
chosen solver Pyke to be suboptimal, struggling to           LIO was noticeably poorer than that of ProofWriter.
identify an answer when multiple search paths are            This disparity is likely due to FOLIO’s intricate
available and some could result in loops.                    logic and its need for a broader array of first-order
                                                             logic tactics such as cases, have, and contradic-
The answer accuracy of prompting-based base-
                                                             tion. In contrast, ProofWriter primarily employs
line is surprisingly high. Despite the low accu-
                                                             tactics like apply, exact, and split.
racy in most of GPT-4’s proofs, it achieved high ac-
curacy for final choices on ProofWriter (as shown            Pretraining on theorem proving data increases
in column Answer). We believe this may be due                overall accuracy. Regarding the overall proof
to GPT-4’s training exposure to the dataset, poten-          results, LeanReasoner pretrained on math theorem
tially leading to a degree of memorization.                  proving data consistently outperformed other ap-
                                                             proaches for both ProofWriter and FOLIO datasets.
5.2   LeanReasoner
                                                             This success indicates that our model effectively
In this section, we focus on training our own mod-           uses the logical “nuggets” found in mathemati-
els to do tactic generation using our annotated train-       cal theorem proofs. While the premise selector
ing data. To isolate the impact of erroneous formal-         benefits from distinct cues and a limited range of
ization, we only used the accurate formalizations            choices, the realm of tactic generation is much
from the previous subsection for testing. This gave          broader. This vastness of options renders the Re-
us 99 test examples for ProofWriter and 28 for               Prover baseline’s proof accuracy nearly negligible.
FOLIO. All findings are detailed in Table 2.                 But other than that, there is a strong correlation
Fine-tuning on annotated data increases                      between premise selection accuracy and overall
premise selection accuracy. We first compare                 proof accuracy. While the benefits of a pretrained
the results on premise selection using the metrics           LeanReasoner may not be as noticeable for sim-
recall@1 and recall@4. The recall@k metric is                pler datasets like ProofWriter, its value becomes
defined as follows:                                          evident for more complex datasets, such as FOLIO.

                |GT_Prem ∩ Pred_Prem[0 : k]|                 Concise annotation gives better result on
  recall@k =                                 ,               premise selection. Fine-tuning with different an-
                        |GT_Prem|

                                                         6
                     Pretrained Fine-tuned      ProofWriter                                FOLIO
       Method         on Math     on our   Premise Selection Proof                 Premise Selection      Proof
                        Data    Annotation Rec@1 Rec@4        Acc                  Rec@1 Rec@4             Acc
  GPT-4                 N/A        N/A           N/A         15%                         N/A               10%
  LeanReasoner          Yes         No     56.2%    81.3%     0%                   23.5%    38.2%          0%
  LeanReasoner           No      Intuitive 62.5%    100%     99%                   54.8%    95.2%         71.4%
  LeanReasoner          Yes      Intuitive  75%     100%     99%                   71.4%    96.8%         85.7%
  LeanReasoner          Yes      Concise    75%     100%     99%                   83.8%    97.4%         85.7%
Table 2: Comparative Analysis of Recall@k in premise selection and overall proof accuracy for 99 ProofWriter
test samples and 28 FOLIO test samples. Note the proof accuracy here is different from Table 1 because it is
directly linked to the final accuracy. The effects of pretraining and fine-tuning on LeanReasoner are evaluated using
theorem-proving data and both Intuitive and Concise annotation sets, respectively. Premise Selection accuracy was
not calculated for the GPT-4 baseline due to the complexities in prompting GPT-4 with Lean goals.

notations has a slight effect on premise selection             Method                                Acc
and tactic generation in this small test set. When             Full training set method
fine-tuned with Concise annotations, LeanRea-                  Abs Biases (Gontier et al., 2022)    80.6%
soner would also try to generate concise proofs,
                                                               MetaInduce (Yang et al., 2022)       98.6%
which usually use compound tactics that offer more
                                                               RECKONING (Chen et al., 2023b)       99.8%
information for premise selection. However, the
                                                               Zero-shot method
final proof accuracy has not changed on this small
test set. Figure 2 displays an example of proofs for           GPT-4 CoT (Pan et al., 2023)         68.1%
the same question, produced by the three primary               Logic-LM (Pan et al., 2023)          79.3%
methods we compared. In the absence of pretrain-               Our method (finetuned on 100 samples)
ing, the model struggles to identify an appropri-              LeanReasoner without Pretraining     95.8%
ate approach for solving the problem. It merely                LeanReasoner fine-tuned on Intuitive 98.3%
attempts to apply the next applicable theorem, lack-           LeanReasoner fine-tuned on Concise 98.3%
ing a clear objective. While Intuitive data offers
                                                             Table 3: The fine-tuned LeanReasoner has been pre-
numerous lemmas that assist in the thought process           trained on mathlib. Full training set method means
during proof-writing, these excessive lemmas do              the model has been trained on the full training set of
not aid LLMs in generating tactics effectively.              ProofWriter. Fine-tuning on Concise achieves near-
                                                             perfect accuracy with significantly less data.
5.3   Other Baselines                                          Method                                Acc
Having demonstrated that pretraining on theorem-               Full training set method
proving data yields superior performance, we pro-              Roberta (Han et al., 2022b)          62.1%
ceed to benchmark our results against established              FOLNet (Chen, 2023)                  70.6%
baselines for both ProofWriter and FOLIO. The                  Zero-shot method
evaluation uses the same set of 600 problems from              GPT-4 CoT (Pan et al., 2023)         70.6%
LogicLM and the entire FOLIO test set.                         Logic-LM (Pan et al., 2023)          74.5%
                                                               Lean Z3 (SATLM)                      77.5%
Our approach yields near-perfect accuracy on                   Our method (finetuned on 27 samples)
ProofWriter with significantly less data. As                   LeanReasoner without Pretraining     66.2%
illustrated in Table 3, our approach yields near-              LeanReasoner fine-tuned on Intuitive 78.4%
perfect accuracy on the ProofWriter dataset. While             LeanReasoner fine-tuned on Concise 82.6%
other methods except Logic-LM and GPT-4 COT
                                                             Table 4: Result from “Lean Z3” is derived from lean-
use the entire training set of ProofWriter, our ap-
                                                             smt applied to formalized Lean Code. The fine-tuned
proach relies on just 100 examples, underscoring             LeanReasoner has been pretrained on mathlib. Full
the efficiency of our method. Fine-tuning on Con-            training set method means the model has been trained on
cise annotation does not bring any advantage to the          the full training set of FOLIO. Our approach achieves
final performance on this dataset.                           state-of-the-arts performance on FOLIO.


                                                         7
 Problem Statement: All rabbits are cute. Some                                   Formalization:
 turtles exist. An animal is either a rabbit or a                                axiom A1 : ∀ (a : Animal), is_rabbit a → is_cute a
 squirrel. If something is skittish, then it is not                              axiom A2 : ∀ (a : Animal), is_rabbit a ∨ is_squirrel a
 still. All squirrels are skittish. Rock is still.                               axiom A3 : ∀ (a : Animal), is_skittish a → ¬ is_still a
                                                                                 axiom A4 : ∀ (a : Animal), is_squirrel a → is_skittish a
                                                                                 axiom A5 : is_still Rock
 Question: Rock is a turtle or cute.
                                                                                 theorem rock_condition : is_turtle Rock ∨ is_cute Rock:=




LeanReasoner without Pretraining:             LeanReasoner Intuitive:                                   LeanReasoner Concise:
right,                                        have h1 : ¬ is_skittish Rock, {                           cases A2 Rock, {
apply A1 Rock,                                       intro h, have h2 : is_still Rock, from A5,                right,
cases A2 Rock, {                                     have h3 : ¬ is_still Rock, from A3 Rock h,                exact A3 Rock (A4 Rock h) A5,
         exact h,                                    contradiction,                                     }, {
}, {                                          }, cases A2 Rock, {                                              exfalso,
     ...                                             have h2 : is_cute Rock, from A1 Rock h,                exact A1 Rock h
},                                                right, exact h2,                                      }
                                                                                                                               ✔
                              ✘               }, {                                  ✘                           compresses multiple tactics
                    model fails to find the          have h3 : ...,     model is confused by                    into one reduces the workload
                    correct solution                                    excessive lemmas                        of LLM
                                                     have h4 : ..., }




Figure 2: Sample proofs created by LeanReasoner without pretraining (left), finetuned on Intuitive data (middle),
and finetuned on Concise data (right).

Our approach achieves state-of-the-arts perfor-                             correct. A case in point is when the answer to a
mance on FOLIO. Table 4 presents our per-                                   problem is U nknown, and errors arise in these
formance on FOLIO. For a fair comparison with                               stages. In such instances, the model would strug-
SATLM that uses the Z3 solver, we used the lean-                            gle to prove either the positive or negative theo-
smt tool5 on our formalized Lean code. This tool                            rem. However, with our result interpreter, these
produces outcomes in the form of “sat/unsat”. In                            instances would still be classified as correct despite
Z3, “sat” stands for “satisfiable.” When Z3 re-                             the underlying issues in problem handling.
turns “sat” as the result, it means that there exists
a set of variable values that makes the theorem                             6    Related Work
true. On the other hand, “unsat” stands for “unsat-
isfiable”. When Z3 returns “unsat”, it means that                           Combining LLM with symbolic solver. Several
the formula is inherently contradictory and cannot                          past studies (Chen, 2023; Creswell and Shanahan,
be satisfied under any circumstance. We interpret                           2022; Chen et al., 2023b) used symbolic solvers
these results similarly to “found a proof/didn’t find                       to augment neural networks with logical reason-
a proof” using our result interpreter. Due to the ex-                       ing. Many of these approaches have limitations,
tensive length of proofs for FOLIO problems, we                             like the necessity for custom or specialized mod-
observed that when LeanReasoner is fine-tuned on                            ule designs that lack broad applicability. Recent
the Intuitive dataset, it often allocates an excessive                      work (Pan et al., 2023; Ye et al., 2023; Poesia et al.,
amount of time for exploration and occasionally                             2023; Olausson et al., 2023) presents a more gen-
enters loops. In contrast, generating shorter proofs                        eral framework that combines contemporary LLMs
tends to ease the discovery of the proof. While the                         with symbolic logic, bypassing the need to train or
tactics generated when fine-tuned on the Concise                            craft intricate modules tailored for specific prob-
dataset are more challenging to produce, the bot-                           lems. While our research aligns with these, we do
tleneck for LeanReasoner on FOLIO resides in the                            not exclusively rely on off-the-shelf solvers.
search process.
                                                                            Boosting the reasoning skill of LLM by train-
Challenges in Benchmarking. It is important                                 ing on reasoning data. A common way to boost
to acknowledge that there can be scenarios where                            the reasoning skills of LLMs is by training them
errors in problem formalization or proof genera-                            on data that requires some form of reasoning. As
tion may occur, yet the final answer is still deemed                        noted by Lewkowycz et al. (2022), LLMs trained
                                                                            with science and math data do better on tasks
     5
         https://github.com/ufmg-smite/lean-smt                             that require reasoning, especially when using CoT

                                                                        8
prompting. Other results by Fu and Khot (2022)                between language understanding and theorem prov-
and Fu et al. (2023) suggest that powerful LLMs               ing.
obtain advanced reasoning capabilities from being                Even in the context of symbolic problems, there
trained on code. This work is an extension of this            are challenges. For instance, consider the Logi-
idea to theorem proving.                                      calDeduction task from the BigBench dataset (Sri-
                                                              vastava et al., 2022). Although this problem ap-
7   Conclusion                                                pears straightforward, employing Lean to solve it
                                                              is neither the most practical nor the most efficient
We introduced LeanReasoner, a framework based                 approach. Lean, as a theorem prover, is excellent in
on Lean that augments the logical reasoning abili-            abstract reasoning and proof construction, but when
ties of LLMs. We follow an extensive examination              faced with tasks involving constraints and variable
of errors from the formalization and proof genera-            possibilities, it falls short. To solve the problems
tion stages that are present in our framework. We             in LogicDeduction, using Lean would require us
also examine the performance enhancements from                to formalize the concepts of ordering and relative
pretraining on theorem-proving data and annotation            positioning. Even after doing so, generating proof
styles (concise v.s. intuitive). We offered a com-            would necessitate significant labor and wouldn’t
prehensive comparison with other techniques that              necessarily yield a readily interpretable answer. In
highlight the strengths of our model. Our results             contrast, a Constraint Satisfaction Problem (CSP)
underscore the potential of integrating theorem-              solver can effectively manage constraints and gen-
proving frameworks with LLMs in advancing logi-               erate potential solutions efficiently.
cal reasoning.
                                                              Ethical Considerations
Limitations                                                   Incorporating Lean’s theorem-proving capabilities
                                                              into LLMs offers a layer of mathematical rigor
Despite our promising results, our method encoun-
                                                              that improves the reliability of conclusions derived.
ters limitations when dealing with problems that
                                                              However, LLMs are known to be susceptible to data
involve commonsense and factual reasoning. In
                                                              biases, which may manifest in critical applications.
these cases, it is challenging to retrieve all the nec-
                                                              This issue can inadvertently lead to skewed logic
essary information and accurately represent it in
                                                              or unintended bias in sensitive domains such as
Lean. Consider MMLU (Hendrycks et al., 2020)
                                                              medical diagnoses or legal interpretations. While
and SummEdits (Laban et al., 2023): MMLU re-
                                                              our method’s foundation in Lean’s theorem proving
quires the model to possess extensive world knowl-
                                                              data acts as a rigorous check, complete reliance
edge, while SummEdits involves determining con-
                                                              on it is not foolproof. A proactive approach in
sistency in summaries of different edits. In both
                                                              reviewing both training data and model outcomes
instances, the ability to represent the complexity
                                                              is essential to uphold unbiased reasoning.
and nuance of real-world knowledge in Lean is
severely limited.                                             Acknowledgements
   Further complications arise when dealing with
math word problems (Cobbe et al., 2021) and simi-             We thank the reviewers and members of the Cohort
lar tasks (Hendrycks et al., 2021), where the goal            for the valuable feedback and comments on the
is to derive a numeric solution rather than a proof.          paper. We appreciate the provision of computing
The theorem-proving approach, while effective for             resources through the Baskerville cluster at the
certifying the validity of logical reasoning, does            University of Birmingham.
not directly yield a numerical answer. Lastly, our
method grapples with problems found in more com-
plicated reasoning datasets like TheoremQA (Chen
et al., 2023a). These problems require an advanced
understanding of complex concepts and the ability
to formalize these concepts into Lean. Our current
framework struggles with this level of complex-
ity, underscoring the need for more sophisticated
formalization techniques and a deeper integration

                                                          9
References                                                       Tao Yu, Rui Zhang, Shafiq R. Joty, Alexander R. Fab-
                                                                 bri, Wojciech Kryscinski, Xi Victoria Lin, Caiming
Fabian Gloeckle Baptiste Rozière, Jonas Gehring and              Xiong, and Dragomir Radev. 2022b. FOLIO: natural
  et.al. 2023. Code llama: Open foundation models for            language reasoning with first-order logic. CoRR.
  code. CoRR, abs/2308.12950.
                                                               Joy He-Yueya, Gabriel Poesia, Rose E. Wang, and
Jianshu Chen. 2023. Learning language representa-                Noah D. Goodman. 2023. Solving math word prob-
   tions with logical inductive bias. In ICLR. OpenRe-           lems by combining language models with symbolic
   view.net.                                                     solvers.
Wenhu Chen, Ming Yin, Max Ku, Pan Lu, Yixin Wan,               Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
 Xueguang Ma, Jianyu Xu, Xinyi Wang, and Tony                    Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
 Xia. 2023a. Theoremqa: A theorem-driven question                2020. Measuring massive multitask language under-
 answering dataset.                                              standing.
Zeming Chen, Gail Weiss, Eric Mitchell, Asli Celiky-           Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul
  ilmaz, and Antoine Bosselut. 2023b. RECKON-                    Arora, Steven Basart, Eric Tang, Dawn Song, and Ja-
  ING: reasoning through dynamic knowledge encod-                cob Steinhardt. 2021. Measuring Mathematical Prob-
  ing. CoRR, abs/2305.06349.                                     lem Solving With the MATH Dataset. In NeurIPS,
                                                                 Menlo Park, Calif. AAAI Press.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias               Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro                S. H. Lewis, Ledell Wu, Sergey Edunov, Danqi Chen,
  Nakano, Christopher Hesse, and John Schulman.                  and Wen-tau Yih. 2020. Dense passage retrieval for
  2021. Training verifiers to solve math word prob-              open-domain question answering. In EMNLP.
  lems.
                                                               Philippe Laban, Wojciech Kryscinski, Divyansh Agar-
Antonia Creswell and Murray Shanahan. 2022. Faith-               wal, Alexander R. Fabbri, Caiming Xiong, Shafiq
  ful reasoning using large language models. CoRR,               Joty, and Chien-Sheng Wu. 2023. Llms as factual
  abs/2208.14271.                                                reasoners: Insights from existing benchmarks and
                                                                 beyond.
Ishita Dasgupta, Andrew K. Lampinen, Stephanie
   C. Y. Chan, Antonia Creswell, Dharshan Kumaran,             Guillaume Lample, Timothée Lacroix, Marie-Anne
   James L. McClelland, and Felix Hill. 2022. Lan-               Lachaux, Aurélien Rodriguez, Amaury Hayat,
   guage models show human-like content effects on               Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
   reasoning. CoRR.                                              2022. Hypertree proof search for neural theorem
                                                                 proving. In NeurIPS.
Leonardo Mendonça de Moura and Nikolaj S. Bjørner.
  2008. Z3: an efficient SMT solver. In TACAS.                 Aitor Lewkowycz, Anders Andreassen, David Dohan,
                                                                 Ethan Dyer, Henryk Michalewski, Vinay V. Ra-
Leonardo Mendonça de Moura, Soonho Kong, Jeremy                  masesh, Ambrose Slone, Cem Anil, Imanol Schlag,
  Avigad, Floris van Doorn, and Jakob von Raumer.                Theo Gutman-Solo, Yuhuai Wu, Behnam Neyshabur,
  2015. The lean theorem prover (system description).            Guy Gur-Ari, and Vedant Misra. 2022. Solving quan-
  In CADE-2.                                                     titative reasoning problems with language models. In
                                                                 NeurIPS.
Hao Fu, Yao; Peng and Tushar Khot. 2022. How does
  gpt obtain its ability? tracing emergent abilities of        Theo Olausson, Alex Gu, Benjamin Lipkin, Cedegao E.
  language models to their sources. Yao Fu’s Notion.             Zhang, Armando Solar-Lezama, Joshua B. Tenen-
                                                                 baum, and Roger Levy. 2023. LINC: A neurosym-
Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, and             bolic approach for logical reasoning by combining
  Tushar Khot. 2023. Complexity-based prompting for              language models with first-order logic provers. In
  multi-step reasoning. In ICLR. OpenReview.net.                 EMNLP.
Nicolas Gontier, Siva Reddy, and Christopher Pal. 2022.        OpenAI. 2023. GPT-4 technical report. CoRR.
  Does entity abstraction help generative transformers
  reason? Trans. Mach. Learn. Res., 2022.                      Liangming Pan, Alon Albalak, Xinyi Wang, and et.al.
                                                                 2023. Logic-lm: Empowering large language models
Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W.              with symbolic solvers for faithful logical reasoning.
   Ayers, and Stanislas Polu. 2022a. Proof artifact co-
   training for theorem proving with language models.          Gabriel Poesia, Kanishk Gandhi, Eric Zelikman, and
   In ICLR.                                                      Noah D. Goodman. 2023. Certified reasoning with
                                                                 language models. CoRR.
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting
  Qi, Martin Riddell, Luke Benson, Lucy Sun, Eka-              Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Man-
  terina Zubova, Yujie Qiao, Matthew Burtell, David               tas Baksys, Igor Babuschkin, and Ilya Sutskever.
  Peng, Jonathan Fan, Yixin Liu, Brian Wong, Mal-                 2023. Formal mathematics statement curriculum
  colm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai,               learning. In ICLR.


                                                          10
Stanislas Polu and Ilya Sutskever. 2020. Generative           A     Prompts for Formalization
   language modeling for automated theorem proving.
  CoRR, abs/2009.03393.                                       A.1    Prompts for ProofWriter
Abulhair Saparov and He He. 2023. Language models             In subsection 5.1, we discussed various formaliza-
  are greedy reasoners: A systematic formal analysis          tion approaches. In this section, we present the
  of chain-of-thought. In ICLR. OpenReview.net.               results using the GPT-4 Base Comments method
Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao,             on ProofWriter when the answer is False. As evi-
  Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch,               dent from the last line, the predicted outcome from
  and et al. 2022. Beyond the imitation game: Quanti-         GPT-4 can be derived easily.
  fying and extrapolating the capabilities of language
                                                              System Message:
  models.
                                                              You are a logician with a background in
                                                              mathematics that translates natural language
Linting Xue, Aditya Barua, Noah Constant, Rami Al-            reasoning text to Lean code so that these natural
  Rfou, Sharan Narang, Mihir Kale, Adam Roberts,              language reasoning problems can be solved. During
  and Colin Raffel. 2022. Byt5: Towards a token-free          the translation, please pay close attention to the
  future with pre-trained byte-to-byte models. Trans.         predicates and entities. There is an additional
  Assoc. Comput. Linguistics, 10.                             requirement: I also want you to try to prove the
                                                              theorem you translated to Lean. If you can prove the
Kaiyu Yang, Jia Deng, and Danqi Chen. 2022. Gen-              theorem, give me True at the end of the answer. If
  erating natural language proofs with verifier-guided        you can prove the negation of the theorem, write
                                                              False at the end of the answer. If you can neither
  search. In EMNLP.                                           prove the original theorem nor the negation
                                                              of the theorem, please give me Unknown at the end of
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-             the answer.
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  Prenger, and Anima Anandkumar. 2023. Leandojo:
  Theorem proving with retrieval-augmented language           Input:
                                                              Textual context: The cat is blue. The cat is nice.
  models.
                                                              The cat likes the cow. The cat needs the cow. The
                                                              cat needs the rabbit. The cow does not need the
Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett.           rabbit. The cow needs the tiger. The rabbit is
  2023. Satisfiability-aided language models using            round. The tiger is nice. The tiger does not
  declarative prompting.                                      like the cow. If someone likes the cat and they
                                                              chase the cat then they are blue. If someone
                                                              likes the cow and they are red then the cow is
                                                              round. If someone needs the tiger and they need
                                                              the cat then they do not chase the cow. If someone
                                                              needs the cat and the cat is blue then the cat is
                                                              red. If someone is round then they need the cat.
                                                              If someone likes the cat and the cat needs the
                                                              rabbit then the cat chases the tiger. If the rabbit
                                                              needs the tiger then the rabbit is not round.

                                                              Question: Based on the above information, is the
                                                              following statement true, false, or unknown? The
                                                              cow chases the cow.




                                                         11
Output:                                                    -- The negation of the theorem can be proven in
universe u                                                      Lean. So
                                                           -- The answer is False
constant obj : Type u

constant Cat : obj
constant Cow : obj                                         A.2   Prompts Used for FOLIO
constant Rabbit : obj
constant Tiger : obj                                       For FOLIO, the prompts differ slightly from those
constant Blue : obj → Prop                                 used for ProofWriter. Since FOLIO’s textual con-
constant Nice : obj → Prop
constant Likes : obj → obj → Prop                          text remains consistent across multiple questions,
constant Needs : obj → obj → Prop
constant Round : obj → Prop
                                                           we concatenate questions sharing the same context
constant Red : obj → Prop                                  and prompt the large language model in a single in-
constant Chases : obj → obj → Prop
                                                           stance. An illustrative example is provided below.
axiom T1 : Blue Cat
axiom T2 : Nice Cat                                        System Message:
axiom T3 : Likes Cat Cow                                   You are a logician with a background in
axiom T4 : Needs Cat Cow                                   mathematics that translates natural language
axiom T5 : Needs Cat Rabbit
axiom T6 : ¬ Needs Cow Rabbit                              reasoning text to Lean code so that these natural
axiom T7 : Needs Cow Tiger                                 language reasoning problems can be solved. During
axiom T8 : Round Rabbit                                    the translation, please pay close attention to the
axiom T9 : Nice Tiger                                      predicates and entities. There is an additional
axiom T10 : ¬ Likes Tiger Cow                              requirement: I also want you to try to prove the
-- If someone likes the cat and they chase the cat         theorem you translated to Lean. If you can prove the
     then they are blue                                    theorem, give me True at the end of the answer. If
axiom R1 : ∀ x : obj, Likes x Cat ∧ Chases x Cat →         you can prove the negation of the theorem, write
      Blue x                                               False at the end of the answer. If you can neither
-- If someone likes the cow and they are red then          prove the original theorem nor the negation
     the cow is round
axiom R2 : ∀ x : obj, Likes x Cow ∧ Red x → Round          of the theorem, please give me Unknown at the end of
     Cow                                                   the answer.
-- If someone needs the tiger and they need the cat
     then they do not chase the cow
axiom R3 : ∀ x : obj, Needs x Tiger ∧ Needs x Cat          Input:
     → ¬ Chases x Cow                                      Textual context: There are six types of wild
-- If someone needs the cat and the cat is blue
                                                           turkeys: Eastern wild turkey, Osceola wild
     then the cat is red
axiom R4 : ∀ x : obj, Needs x Cat ∧ Blue Cat →             turkey, Gould’s wild turkey, Merriam’s wild
     Red Cat                                               turkey, Rio Grande wild turkey, and Ocellated
-- If someone is round then they need the cat              wild turkey. Tom is not an Eastern wild turkey.
axiom R5 : ∀ x : obj, Round x → Needs x Cat                Tom is not an Osceola wild turkey. Tom is
-- If someone likes the cat and the cat needs the
                                                           also not a Gould’s wild turkey, or a
     rabbit then the cat chases the tiger
axiom R6 : ∀ x : obj, Likes x Cat ∧ Needs Cat              Merriam’s wild turkey, or a Rio Grande wild
     Rabbit → Chases Cat Tiger                             turkey. Tom is a wild turkey.
-- If the rabbit needs the tiger then the rabbit is
     not round                                             Question 1: Based on the above information, is the
axiom R7 : ∀ x : obj, Needs Rabbit Tiger → ¬
                                                           following statement true, false, or uncertain?
     Round Rabbit
                                                           Tom is an Ocellated wild turkey.
                                                           Question 2: Based on the above information, is the
theorem cow_chases_cow : Chases Cow Cow :=                 following statement true, false, or uncertain?
begin                                                      Tom is an Eastern wild turkey.
  have H1 : Needs Cow Tiger := T7,
                                                           Question 3: Based on the above information, is the
  have H2 : Needs Cat Cow := T4,
  have H3 : ¬ Chases Cow Cow := R3 Cow (and.intro          following statement true, false, or uncertain?
     H1 H2),                                               Joey is a wild turkey.
  contradiction,
  sorry,
end

-- Looks like the theorem cannot be proven in Lean.
-- So let’s try to prove the negation of the
     theorem, which is Cow does not chase Cow

theorem not_cow_chases_cow : ¬ Chases Cow Cow :=
begin
  apply R3 Cow,
  split,
  exact T7,
  apply R5,
  apply R2 Cat,
  split,
  exact T3,
  apply R4 Rabbit,
  split,
  apply R5,
  exact T8,
  exact T1,
end




                                                      12
                                                           theorem not_tom_is_ocellated_wild_turkey : ¬
Output:                                                         is_ocellated_wild_turkey Tom :=
-- Introducing basic types for entities in our             begin
     universe.                                                 exact A2,
constant Turkey : Type                                     end
constant Tom : Turkey
constant Joey : Turkey                                     -- The answer is Unknown
-- Defining properties for the turkeys in our              -- Question 2
     universe.                                             -- Tom is an Eastern wild turkey.
constant is_wild_turkey : Turkey → Prop                    -- Let’s first prove the positive case.
constant is_eastern_wild_turkey : Turkey → Prop            theorem tom_is_eastern_wild_turkey :
constant is_osceola_wild_turkey : Turkey → Prop                 is_eastern_wild_turkey Tom :=
constant is_goulds_wild_turkey : Turkey → Prop             begin
constant is_merriams_wild_turkey : Turkey → Prop               sorry, -- Placeholder for proof
constant is_rio_grande_wild_turkey : Turkey → Prop         end
constant is_ocellated_wild_turkey : Turkey → Prop
                                                           -- Let’s try the negative case.
-- Context from the information
                                                           theorem not_tom_is_eastern_wild_turkey : ¬
-- Tom is not an Eastern wild turkey.                           is_eastern_wild_turkey Tom :=
axiom A1 : ¬ is_eastern_wild_turkey Tom                    begin
-- Tom is not an Osceola wild turkey.                          exact A1,
axiom A2 : ¬ is_osceola_wild_turkey Tom                    end
-- Tom is also not a Gould’s wild turkey.
axiom A3 : ¬ is_goulds_wild_turkey Tom                     -- The answer is False
-- Tom is not a Merriam’s wild turkey.
axiom A4 : ¬ is_merriams_wild_turkey Tom                   -- Question 3
-- Tom is not a Rio Grande wild turkey.                    -- Joey is a wild turkey.
axiom A5 : ¬ is_rio_grande_wild_turkey Tom                 -- Let’s first prove the positive case.
-- Tom is a wild turkey.                                   theorem joey_is_wild_turkey : is_wild_turkey Joey :=
axiom A6 : is_wild_turkey Tom                              begin
-- There are six types of wild turkeys: Eastern                sorry, -- Placeholder for proof
     wild turkey, Osceola wild turkey, ’Goulds wild        end
     turkey, ’Merriams wild turkey, Rio Grande wild
     turkey, and Ocellated wild turkey.                    -- Let’s try the negative case.
axiom turkey_type_exclusivity : ∀ (t : Turkey),
    is_wild_turkey t → is_eastern_wild_turkey t ∨          theorem not_joey_is_wild_turkey : ¬ is_wild_turkey
     is_osceola_wild_turkey t ∨                                 Joey :=
     is_goulds_wild_turkey t ∨                             begin
     is_merriams_wild_turkey t ∨                               sorry, -- Placeholder for proof
     is_rio_grande_wild_turkey t ∨                         end
     is_ocellated_wild_turkey t
                                                           -- The answer is Unknown
-- Formalizing the Questions

-- Question 1
-- Tom is an Ocellated wild turkey.
-- Let’s first prove the positive case.
                                                           B   Example Errors During Formalization
theorem tom_is_ocellated_wild_turkey :
     is_ocellated_wild_turkey Tom :=                       This is an artificial example highlighting typical
begin
    cases turkey_type_exclusivity Tom A6, {                errors encountered in the formalization stage.
         have h1 : ¬ is_eastern_wild_turkey Tom,
     from A1,                                              Input:
         contradiction,                                    There are three types of wild turkeys: Eastern
    }, {                                                   turkey, Osceola turkey, Gould’s turkey. Tom is
         cases h, {                                        neither an Eastern turkey nor an Osceola turkey.
             have h1 : ¬ is_osceola_wild_turkey
     Tom, from A2,                                         Tom is a wild turkey. Bob is a Eastern turkey.
             contradiction,                                Bob weights 86 pounds and Tom weights 73 pounds.
         }, {                                              Turkey either bites or stings.Bob bites. Eastern
             cases h, {                                    turkey ’s bite would cause death.
                 have h1 : ¬ is_goulds_wild_turkey
     Tom, from A3,
                 contradiction,                            Question 1:   Tom is a Gould’s turkey.
             }, {                                          Question 2:   Bob is heavier than Tom.
                 cases h, {                                Question 3:   If Bob bites you, you will die.
                     have h1 : ¬
     is_merriams_wild_turkey Tom, from A4,
                     contradiction,                        Output:
                 }, {                                      constant Turkey : Type
                     cases h, {                            constant Eastern Osceola Goulds : Turkey → Prop
                         have h1 : ¬                       constant weight_86 weight_73 : Turkey → Prop
     is_rio_grande_wild_turkey Tom, from A5,               constant bites stings : Turkey → Prop
                         contradiction,                    constant eastern_bite_causes_death : Turkey → Prop
                     }, {                                  constant Tom Bob : Turkey
                         assumption,
                     }                                     axiom A1 : ¬ Eastern Tom ∧ ¬ Osceola Tom
                 }                                         axiom A2 : Eastern Bob
             }                                             axiom A3 : weight_86 Bob
         }                                                 axiom A4 : weight_73 Tom
    }                                                      axiom A5 : ∀ (t : Turkey), bites t ∨ stings t
end                                                        axiom A6 : bites Bob
                                                           axiom A7 : ∀ (t : Turkey),
-- Let’s try the negative case.                                 eastern_bite_causes_death t




                                                      13
  There are a few errors in the above code, includ-           axiom A5 : ∀ (t : Thing), is_animal t → breathes t
                                                              -- If a sea eel is either an eel or a plant, then a
ing:                                                               sea eel is an eel or an animal.
                                                              axiom A6 : (is_eel sea_eel ∨ is_plant sea_eel) →
                                                                   (is_eel sea_eel ∨ is_animal sea_eel)
    • There is a missing axiom that corresponds to
      "There are three types of wild turkeys":
                                                              Intuitive Proof:
                                                              theorem not_sea_eel_is_paper : ¬ is_paper sea_eel
      Goulds Tom ∨ Eastern Tom ∨ Osceola Tom                       :=
                                                              begin
                                                                  cases A3 sea_eel, {
    • The formalization of numbers is incorrect, it                    have h1 : ¬ is_fish sea_eel, {
                                                                           intro h,
      should be:                                                           have temp := A2 sea_eel h,
                                                                           contradiction,
      constant weight : Turkey → N                                     },
                                                                       have h2 : ¬ is_eel sea_eel, {
                                                                           intro h,
      axiom A3 : weight Bob = 86                                           have temp := A1 sea_eel h,
                                                                           contradiction,
                                                                       },
      axiom A4 : weight Tom = 73                                       have h3 : is_eel sea_eel ∨ is_plant
                                                                   sea_eel, {
                                                                           right,
    • The formalization of logic is incorrect, it                          assumption,
                                                                       },
      should be:                                                       have h4 : is_eel sea_eel ∨ is_animal
                                                                   sea_eel := A6 h3,
      ¬ bite_causes_death t ∧ bite_causes_itching t) ∨                 cases h4, {
                                                                           contradiction,
      (bite_causes_death ∧ ¬ bite_causes_itching t                     }, {
                                                                           have h5 : breathes sea_eel := A5
                                                                   sea_eel h4,
    • There is an incorrect division of concepts that                      have h6 : ¬ is_paper sea_eel := A4
                                                                   sea_eel h5,
      would make the proving impossible, the cor-                          contradiction,
      rect version should be:                                          }
                                                                  }, {
                                                                       have h1 : breathes sea_eel := A5 sea_eel h,
      ∀ (t : Turkey), Eastern t → bite_causes_death t                  have h2 : ¬ is_paper sea_eel := A4 sea_eel
                                                                   h1,
                                                                       contradiction,
C    Example Proof Annotation with                                }
                                                              end
     Different Annotation Styles
Here we’re showing two example proofs created on              Concise Proof:
                                                              theorem not_sea_eel_is_paper : ¬ is_paper sea_eel
the same problem with ‘Intuitive’ annotation style                 :=
                                                              begin
and ‘Concise’ annotation style.                                   cases A3 sea_eel, {
                                                                      cases A6 (or.inr h), {
Input:                                                                    have h1 := A2 sea_eel (A1 sea_eel h_1),
"Textual Context": All eels are fish. No fish are                         contradiction,
plants. A thing is either a plant or animal.                          }, {
Nothing that breathes is paper. All animals breathe.                      exact A4 sea_eel (A5 sea_eel h_1),
                                                                      }
If a sea eel is either an eel or a plant, then a sea
                                                                  }, {
eel is an eel or an animal.                                           exact A4 sea_eel (A5 sea_eel h),
"Question": "Based on the above information, is                   }
the following statement true, false, or uncertain?            end
Sea eel is a paper.


Formalized Context:
constant Thing : Type

constant is_eel : Thing → Prop
constant is_fish : Thing → Prop
constant is_plant : Thing → Prop
constant is_animal : Thing → Prop
constant is_paper : Thing → Prop
constant breathes : Thing → Prop

constant sea_eel : Thing

-- All eels are fish.
axiom A1 : ∀ (t : Thing), is_eel t → is_fish t
-- No fish are plants.
axiom A2 : ∀ (t : Thing), is_fish t → ¬ is_plant t
-- A thing is either a plant or animal.
axiom A3 : ∀ (t : Thing), is_plant t ∨ is_animal t
-- Nothing that breathes is paper.
axiom A4 : ∀ (t : Thing), breathes t → ¬ is_paper
     t
-- All animals breathe.



                                                         14
