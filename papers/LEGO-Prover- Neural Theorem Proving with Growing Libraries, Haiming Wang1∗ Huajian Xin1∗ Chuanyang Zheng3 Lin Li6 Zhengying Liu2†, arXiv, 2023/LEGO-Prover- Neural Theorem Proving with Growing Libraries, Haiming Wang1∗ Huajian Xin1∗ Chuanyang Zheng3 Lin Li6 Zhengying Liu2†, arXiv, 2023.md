                                         LEGO-P ROVER : N EURAL T HEOREM P ROVING WITH
                                         G ROWING L IBRARIES
                                          Haiming Wang1∗ Huajian Xin1∗ Chuanyang Zheng3 Lin Li6 Zhengying Liu2†
                                          Qingxing Cao1 Yinya Huang4 Jing Xiong1 Han Shi2 Enze Xie2 Jian Yin1†
                                          Zhenguo Li2 Heng Liao6 Xiaodan Liang1, 5†
                                          1
                                            Sun Yat-sen University 2 Huawei Noah’s Ark Lab 3 The Chinese University of Hong Kong
                                          4
                                            City University of Hong Kong 5 MBZUAI 6 Huawei HiSilicon
                                          {wanghm39, xinhj, caoqx, xiongj69, issjyin}@mail2.sysu.edu.cn, cyzheng21@cse.cuhk.edu.hk,
                                          {liuzhengying2, xie.enze, shi.han, lilin29, Li.Zhenguo}@huawei.com, liao.heng@hisilicon.com,
                                          yinya.huang@hotmail.com, xdliang328@gmail.com
arXiv:2310.00656v3 [cs.AI] 27 Oct 2023




                                                                                       A BSTRACT
                                                   Despite the success of large language models (LLMs), the task of theorem proving
                                                   still remains one of the hardest reasoning tasks that is far from being fully solved.
                                                   Prior methods using language models have demonstrated promising results, but
                                                   they still struggle to prove even middle school level theorems. One common
                                                   limitation of these methods is that they assume a fixed theorem library during the
                                                   whole theorem proving process. However, as we all know, creating new useful
                                                   theorems or even new theories is not only helpful but crucial and necessary for
                                                   advancing mathematics and proving harder and deeper results. In this work, we
                                                   present LEGO-Prover, which employs a growing skill library containing verified
                                                   lemmas as skills to augment the capability of LLMs used in theorem proving. By
                                                   constructing the proof modularly, LEGO-Prover enables LLMs to utilize existing
                                                   skills retrieved from the library and to create new skills during the proving process.
                                                   These skills are further evolved (by prompting an LLM) to enrich the library on
                                                   another scale. Modular and reusable skills are constantly added to the library
                                                   to enable tackling increasingly intricate mathematical problems. Moreover, the
                                                   learned library further bridges the gap between human proofs and formal proofs
                                                   by making it easier to impute missing steps. LEGO-Prover advances the state-
                                                   of-the-art pass rate on miniF2F-valid (48.0% to 57.0%) and miniF2F-test (45.5%
                                                   to 50.0%). During the proving process, LEGO-Prover also manages to generate
                                                   over 20,000 skills (theorems/lemmas) and adds them to the growing library. Our
                                                   ablation study indicates that these newly added skills are indeed helpful for proving
                                                   theorems, resulting in an improvement from a success rate of 47.1% to 50.4%. We
                                                   also release our code and all the generated skills. 1


                                         1       I NTRODUCTION
                                         The automation of formal reasoning tasks, such as theorem proving and mathematical proof for-
                                         malization, represents a formidable challenge and an active area of research within the domain of
                                         artificial intelligence (Polu & Sutskever, 2020a; Han et al., 2022; Jiang et al., 2022a; First et al., 2023;
                                         Bansal et al., 2019; Lample et al., 2022; Jiang et al., 2022b; 2021; Zhao et al., 2023; Yang et al., 2023;
                                         Wang et al., 2023b; Liu et al., 2023). The process of formalizing mathematical proofs typically relies
                                         on human experts to transcribe intricate mathematical concepts into structured formal languages
                                         verifiable by interactive theorem prover like Lean (de Moura et al., 2015) or Isabelle (Paulson, 1994).
                                         This process, while robust, is often labor-intensive and demands a high level of expertise.
                                         In the past few years, large language models (LLMs) have emerged as a promising avenue, with their
                                         capacity to process and produce human-like text, opening doors to the idea of LLM-based neural
                                             ∗
                                               These authors contributed equally.
                                             †
                                               Corresponding authors.
                                             1
                                               Code and data can be found at https://github.com/wiio12/LEGO-Prover.


                                                                                              1
            Plain Prover                                    LEGO Prover
theorem amc12a_2003_p24:                     (* lemma 1. Retrieved from    ,   proves the
  fixes a b::real                            inequality of arithmetic and geometric means)
  assumes "b≤a" "1<b"                        lemma   :
  shows "ln (a/b) / ln a + ln (b/a) / ln b     fixes x y :: real
≤0" (is "?L ≤ _")                              assumes "x >= 0" "y >= 0"
                                                                                               statement                    proof
proof -                                        shows "x^2 + y^2 >= 2*x*y"
  ...                                          using assms by <ATP>
(* Prove a special form of the AM-GM in-     (* lemma 2. Synthesized by    ,     proves a
equality as an intermediate result that is
equivalent to the lemma on the right *)
                                             special form of the AM-GM inequality required                     prover
                                             in the proof of the target theorem. *)
  also have "... ≤ 0"
  proof -                                    lemma    :
    define a1 a2 where "a1=sqrt(x/y)"          fixes x y :: real
                                                                                               retrieved                     new
"a2=sqrt(y/x)"                                 assumes "x > 0" "y > 0"
    have c2: "a1 \<ge> 0" using c0 c1                                                            skill                      skill
                                               shows "x/y + y/x >= 2"
a1_a2_def by <ATP>                           proof -
    have c3: "a2 \<ge> 0" using c0 c1          ...
a1_a2_def by <ATP>                             have "x/y + y/x >= 2 * sqrt(x/y) * sqrt(y/x)"
    then have "a1^2 + a2^2 ≥ 2 * a1 * a2"        using   [of "sqrt(x/y)" "sqrt(y/x)"] c0 c1
      using c2 c3 by <ATP>                   by <ATP>
    then have "sqrt(x/y)^2 + sqrt(y/x)^2 ≥      ...
2 * sqrt(x/y) *sqrt(y/x)"                    qed
      using a1_a2_def by force                                                                          growing skill library
    then have "x/y + y/x ≥ 2 * sqrt(x/y *    theorem amc12a_2003_p24:
y/x)"                                          fixes a b::real
                                               assumes "b≤a" "1<b"
      by <ATP>
                                               shows "ln (a/b) / ln a + ln (b/a) / ln b ≤0"
    then have "x/y + y/x ≥ 2" using c0 c1
                                             (is "?L ≤ _")
by auto
                                             proof -
    then show ?thesis by auto                  ...
  qed                                          also have "... ≤ 0"
  finally show ?thesis .                         using     ‹0 < x› ‹0 < y› by <ATP>
qed                                                                                                                       evolved
                                               finally show ?thesis .
                                             qed
                                                                                                skill         evolver      skill

                                             (a)                                                                 (b)

Figure 1: (a) Comparison between plain provers and LEGO-Prover. Unlike plain provers that prove the
theorem sequentially, LEGO-Prover constructs the proof in a modular paradigm. Useful lemmas can be directly
retrieved from the skill library and used as part of the proof. A newly constructed lemma can also be added to
the skill library to help the proof of other theorems. (b) Overall framework of our proposed LEGO-Prover.
LEGO-Prover contains the prover that proves the theorem modularly using the retrieved skill and the evolver
that transforms the skill for reusability and generalizability. These two components are bridged by the growing
skill library.

theorem proving. Specifically, two predominant paradigms have been extensively explored in neural
theorem proving. One stream of work involves step-by-step proof generation (Polu & Sutskever,
2020a; Han et al., 2022; Polu et al., 2022; Lample et al., 2022; Wang et al., 2023b; Yang et al.,
2023; Jiang et al., 2022a), where fine-tuned models provide single-step proof actions coupled with
search algorithms to find the complete proofs. Another paradigm leverages the coding capabilities of
LLM to construct entire proofs in a single decoding process (Jiang et al., 2022b; Zhao et al., 2023;
First et al., 2023). As shown in Fig. 1(a) left, these approaches share common proving strategies
that synthesize the proof sequentially, with each step building upon the previous proof step, and
stocking all the proof code into one large proof block. We denoted these approaches as plain provers
since they generate the whole proof directly. Despite their promising results, plain provers still have
several shortcomings. On one hand, plain provers attempt to prove theorems using static LLMs
independently, while different problems can usually provide some insights into others. In other words,
different problems may share the same lemmas while plain provers cannot utilize the proved lemmas
once again even though it has been proved. On the other hand, even though plain provers can generate
short-chain proofs with the help of advanced large language models like ChatGPT or GPT-4 (OpenAI,
2023) , it usually fails when it comes to long-chain proofs due to the reasoning difficulty.
To overcome the shortcomings of plain provers and inspired by the modularity of LEGO building
blocks, we present LEGO-Prover, a novel approach designed to prove theorems in a block-by-block
manner backed by a growing skill library. As shown in Fig. 1(a) right, LEGO-Prover tackles the
problem of proving a theorem by first proving the sub-goal lemmas and then finalizing the problem
using these lemmas. These lemmas can be retrieved from the skill library or newly constructed during
the proving process. Specifically, Fig. 1(b) shows the overall process of LEGO-Prover, containing a
prover and an evolver, which are bridged by the growing skill library. The prover takes the problem’s
formal statement as input and retrieves skills to prompt the LLM in generating the modular proof,
with the generated lemmas accumulated into the skill library. However, lemmas created by the prover
are often problem-specific with low reusability. Thus, LEGO-Prover incorporates an evolver that
transforms the skills in the library for better generality, reusability, and complexity of the skills. The
evolved new skills will also be verified and added back to the skill library.
We conduct extensive experiments on the popular theorem-proving dataset miniF2F (Zheng et al.,
2021) to validate the effectiveness of our proposed approach. LEGO-Prover significantly outperforms
previous approaches, achieving a pass rate of 57.0% and 50.0% on the miniF2F valid and test datasets,
respectively. With a 6.75% absolute improvement on average over the previous state-of-the-art


                                                                   2
methods. In addition, our case study reveals that LLMs prove theorems modularly akin to LEGO
block assembly, utilizing the retrieved skill by directly copying or using as a referee to construct the
proof. Moreover, the learned skill library contains 22532 skills encompassing many useful high-level
lemmas broadly applicable to various problems, as is shown in our case study and ablation study.

2   R ELATED WORKS
Machine learning for formal mathematics. Modern formal mathematics environments often center
around Interactive Theorem Provers (ITPs) like Lean (de Moura et al., 2015), Isabelle (Paulson,
1994), Metamath (Megill & Wheeler, 2019) and Coq (Barras et al., 1997). These ITPs often include
specific formal languages, accompanied formal verifiers, and automated provers like Sledgehammer.
ITPs provide machine-human interactive interfaces, which gives verification results during formal
proof construction for specific theorems and human coder can correct errors or continue to fill gaps
in proofs under the guidance of error messages and local proof states, respectively.
Research leveraging machine learning techniques atop these formal mathematics environments
generally falls into two predominant paradigms. The first focuses on proof search strategies and
premise selection, epitomized by GPT-f (Polu & Sutskever, 2020a), where a language model advises
single-step actions based on the current proving state, and the tree search finds a sequence of
correct steps using actions given by the language model. The follow-up works PACT (Han et al.,
2022) and Expert Iteration (Polu et al., 2022) incorporate supplemental pre-training tasks like
theorem naming to enhance the policy model’s reasoning ability. HTPS (Lample et al., 2022)
applies Monte-Carlo tree search coupled with online training to optimize the exploration of the
proof space. DT-Solver (Wang et al., 2023b) enhances search efficiency by dynamically adjusting
search budgets to accommodate varying levels of state complexity. Thor (Jiang et al., 2022a) blends
traditional Automated Theorem Provers (ATPs) with neural policy models to prove theorems in a
neural-symbolic manner. Magnushammer (Mikuła et al., 2023) augments Thor’s performance by
integrating premise selection, thereby boosting the performance of rule-based ATPs.
Autoformalization. Our LEGO-Prover aligns closely with the second paradigm in machine learning
for formal mathematics, which leverages the capabilities of large language models (LLMs) for the
formalization of mathematical proofs. Several notable works have paved the way in this domain. For
instance, Wang et al. (2018) delved into both supervised and unsupervised translation techniques
for auto-formalization tasks. Wu et al. (2022) makes its first attempt at employing a large language
model to translate natural language mathematical problems into formal theorem statements. Building
on this, Draft, sketch, and proof Jiang et al. (2022b) develops a three-step approach that aims to
fully formalize proofs, using natural language as guidance. First et al. (2023) goes a step further
by generating complete proofs in a single pass and introducing a proof repair model to enhance
the theorem-proving capabilities. Zhao et al. (2023) advances Jiang et al. (2022b) by incorporating
cross-verified informal proofs to better inform the generation of formal proof sketches. Despite
their contributions, none of the aforementioned methods have succeeded in establishing a learning
paradigm that incrementally formalizes increasingly complex problems via a growing skill library, a
gap that our work seeks to fill.
Skill-based agents. LEGO-Prover is also related to trending AI agents powered by large language
models like GPT-3.5 and GPT-4 (Shen et al., 2023; Park et al., 2023; Wang et al., 2023c; Zahedi &
Kambhampati, 2021). These AI agents are characterized by their ability to perform complex tasks
through a combination of task planning, logical reasoning, and skill accumulation. For example,
Voyager (Wang et al., 2023a) creates an AI agent capable of autonomously playing Minecraft. It
has a dynamic growing skill library that empowers the in-game character to tackle increasingly
intricate tasks. Similarly, (Cai et al., 2023) showcases the ability to generate reusable Python tools
and documentation, which can then be leveraged by weaker GPT models, increasing the ability of the
model.

3   M ETHOD
In this section, we introduce the detailed implementations of our proposed LEGO-Prover. Following
the setting of Jiang et al. (2022b), we assume that each theorem is equipped with an informal statement,
a human-written informal proof, and a formal statement defining the problem. As illustrated in Fig. 2,


                                                   3
   informal statement                            informal proof                                decomposed                                              formal proof
   If a ≥ b > 1, what                          ...Since a and b                              informal proof                          lemma   :
   is the largest pos-                         are both greater                            1. Introduce vari-                          fixes x y :: real
   sible value of                              than 1, using AM-GM                         ables...                                    assumes "x >= 0" "y >= 0"
   loga(a/b)+logb(b/a)?                        inequality gives                            ...                                         shows "x^2 + y^2 >= 2*x*y"
   Show that it is B.                          that the term in                            2: Given that b > 1                         using assms by <ATP>
                                                                           decomposer                                 formalizer
                                               parentheses must be                         ...                                       lemma       :
                                  informal                                                                                                                                   new skill
                                   solver      at least 2, so the                          6. Use the AM-GM in-
                                               largest possible                                                                        fixes x y :: real
                                                                                           equality to argue
                                               values is 2-2=0...                                                                      assumes "x > 0" "y > 0"
                                                                                           that the term y / x
                                                                                                                                       shows "x/y + y/x >= 2"
                                                                                           + x / y is at least
                                                                                                                                     proof -
                                                                                           2.
                                                                                                                                       ...
                                                                                                                                       have "x/y + y/x >= 2 * sqrt(x/y) * sqrt(y/x)"
                                                                                                                                          using  [of "sqrt(x/y)" "sqrt(y/x)"] c0 c1
                                                                                                                                     by <ATP>
                  skill library
                                                                                                                                         ...
                                                                                                                                     qed
                                                                                   decomposed
                                                                                  formal goals                                       theorem amc12a_2003_p24:       formal statement
                    lemma vector store                                                                                                 fixes a b::real
                                                   lemma   :            request                                  retrieved skill       assumes "b≤a" "1<b"
                                                     fixes x y :: real                             lemma   :
                                                                                                     fixes x y :: real                 shows "ln (a/b) / ln a + ln (b/a) / ln b ≤0"
                                                     assumes "x >= 0" "y >= 0"                                                       (is "?L ≤ _")
                    request vector store                                                             assumes "x >= 0" "y >= 0"
                                                     shows "x^2 + y^2 >= 2*x*y"                                                      proof -
                                                                                                     shows "x^2 + y^2 >= 2*x*y"
                                                                                 request             using assms                       ...
                                                                                            skill                                      also have "... ≤ 0"
                                                   lemma      :                            library     by (simp add:
                    problem vector store
                                                       fixes x y :: real                                   sum_squares_bound)            using     ‹0 < x› ‹0 < y› by <ATP>
                                                       assumes "x > 0" "y > 0"                                                         finally show ?thesis .
                                                       shows "ln (a / b) = ln a - ln b"           not found                          qed
  (a)

                                                              theorem amc12a_2003_p24:                     formal statement                      lemma   :                evolved skill
                                                                fixes a b::real
                                                                                                                                                   fixes x y :: real
  lemma   :           retrieved skill                           assumes "b≤a" "1<b"
                                                                                                                                                   assumes "x >= 0" "y >= 0"
    fixes x y :: real                                           shows "ln (a/b) / ln a + ln (b/a) / ln b ≤0" (is "?L ≤ _")
                                                                                                                                                   shows "2 * sqrt (a * b) <= a + b"
    assumes "x >= 0" "y >= 0"
                                                              lemma   :                                                                            using assms
    shows "x^2 + y^2 >= 2*x*y"                                                     request
                                                                fixes x y :: real                                                                        by (simp add: real_sqrt_mult)
    using assms
          by (simp add:                       skill             assumes "x >= 0" "y >= 0"
                                                                                                                                   directional   lemma    :              solved request
              sum_squares_bound)             library            shows "x^2 + y^2 >= 2*x*y"
                                                                                                                                   transformer     fixes a b :: real
                                                                                                                                                   assumes "a > 0" "b > 0"
                                                                                                                                                   shows "ln (a / b) = ln a - ln b"
                                  request                                                                                                        proof -
  lemma       :                                              lemma   :              similar skill
                                                                                                                                                   have "ln (a / b) = ln a + ln (1 /
      fixes x y :: real                                        fixes a b :: real
                                                                                                                                                 b)" using assms by (simp add: ln_div)
      assumes "x > 0" "y > 0"                                  assumes "a > 0" "b > 0"
                                              skill                                                                                                also have "... = ln a - ln b" using
      shows "ln (a / b) = ln a - ln b"                         shows "log a b = ln b \/ ln a"                                        request
                                             library                                                                                  solver     assms by (simp add: ln_div)
                                                             by (simp add: log_def)
                                                                                                                                                   finally show ?thesis .
  (b)                                                                                                                                            qed




Figure 2: Overview of LEGO-Prover. (a) The prover takes three consecutive steps to prove the problem. The
informal solver produces an informal solution for the problem statement, followed by using the decomposer to
decompose it into step-by-step proof and propose useful sub-goals in the form of lemma statements. We use
these lemma statements to retrieve useful lemma from the skill library. The formalizer constructs the final proof
with the help of decomposed informal proof and retrieved lemma in a block-by-block manner. We extract newly
constructed lemmas from the final proof and add them to the lemma vector store. (b) The evolver contains two
evolution approaches, the directional transformer transforms the existing skill into a more general and reusable
form in four predefined directions. The request solver directly solves the requested subgoal proposed by the
prover. Newly generated and formally verifed lemmas from the evolver will be added to the lemma vector store.

LEGO-Prover consists of two main components: the prover and the evolver. The prover decomposes
the problem into possible subgoal lemmas and proves the problem in a block-by-block style, aided
by the skill library. The evolver refines skills in the skill library for enhanced diversity, generality,
and reusability, and also resolves decomposed sub-goals from the prover to create new skills. These
components are linked via a skill library housing lemmas and requests. In the following sections, we
will detail introduce the skill library, the prover, and the evolver.

3.1       S KILL LIBRARY

The skill library contains various vector stores that are optimized for retrieval. Every vector store
maintains its data in pairs consisting of documents and their corresponding embeddings, encoded with
an embedding language model2 . Upon the receipt of a query, the vector store employs the embedding
model to encode the query and leverages the k-NN algorithm to retrieve relevant documents stored
within. The skill library used in LEGO-Prover is comprised of three distinct vector stores. 1) The
lemma vector store contains the Isabelle verified lemmas, encompassing both the lemma’s statement
and its proof. This is the core of the skill library and it facilitates the perpetual enhancement of LLMs’
capabilities in constructing increasingly intricate theorems. For representation simplicity, the notion
of lemmas in the lemma vector store and skills in the skill library are use interchangeably in this paper.
2) The request vector stores preserve the lemma statements proposed by the decomposer. These
requests are crucial to the success of LEGO-Prover, their works as an in-depth reasoned query for
retrieving the useful skill for the prover, as well as possible complete lemmas when they are solved
by the evolver. 3) The problem vector store houses the formal statements in the miniF2F dataset.
The evolver utilizes these problem statements as heuristics to guide the LLMs in generating more
beneficial new lemmas.

  2
    Practically, ChromaDB serves as our vector store, coupled with the OpenAI’s text-davinci-ada embedding
model.


                                                                                              4
3.2   P ROVER

As illustrated in Fig. 2 (a), the prover employs a three-step process to construct the proof. Initially,
an informal solver is deployed to draft a solution in natural language corresponding to the informal
statement. Akin to (Jiang et al., 2022b), LEGO-Prover experiments the use of ground truth human-
written proofs as alternatives to model-generated proofs. After obtaining the informal proof, LEGO-
Prover constructs the formal proof using the decomposer and the formalizer sequentially, which we
detailed in the following.
Decomposer. The decomposer aims to decompose the formalization tasks, which transform the
informal proof into the decomposed step-by-step informal proof as well as decompose the problem
into formal goals. A concrete example of the decomposer is shown in Fig. 5 in Appendix. A.1.
Specifically, the decomposer prompts the LLM to refine informal proofs, producing step-by-step
informal proof that more closely aligns with the structure of the actual Isabelle proof code. We
posit that this alignment is crucial as it considerably reduces the complexity encountered during the
formalization process. Concurrently, the decomposer tasks the LLM with generating requests: some
potential lemma or theorem statements that could be useful in addressing the given problem. Each
request is composed of a chain-of-thought reasoning on what kind of lemma is required for solving
the problem followed by the formal statement of the lemma. Subsequently, LEGO-Prover put these
requests into the request vector store.
Formalizer. The process of formalization involves translating an informal proof into Isabelle’s proof
sketches, as depicted in Fig. 6 (refer to Appendix. A.1). In addition to the problem statement, the
refined informal proof, and the formal statement, the formalizer is designed to incorporate useful
lemmas retrieved from the lemma vector stores as part of the input. The formalizer employs the
proposed request originating from the decomposer and the formal statement of the problem as query
texts and, in total, retrieves nf skills. Upon collecting all the necessary input, the LLM is tasked to
provide the proof code. Unlike the setting in Jiang et al. (2022b) and Zhao et al. (2023), we prompt
the LLM to construct the complete content of the source file in Isabelle. This may encompass the
requisite imports, definitions, or lemmas before the elucidation of the main problem to be proven.
Consequently, the LLM possesses the capability to generate or apply useful lemmas before embarking
on the resolution of the problem. Empirical evaluations demonstrate that our model exhibits a more
modular problem-solving approach compared to established baseline methods. This modularity
facilitates recycling smaller lemma components, thereby enhancing the LLM’s capability to tackle
progressively intricate problems.
After obtaining the formalized proof code, LEGO-Prover employs the Isabelle theorem prover to
verify the correctness of the provided proof code. In instances where a particular proof tactic (such
as ”by ...”) falls short of proving the given conjecture, we resort to 11 heuristic tactics alongside
the sledgehammer method to facilitate an auto-correction. The heuristic selection we employ is
consistent with those presented in Jiang et al. (2022b). After verifying the code, all validated lemmas
or theorems are added to the skill vector store, while any failed lemmas’ statement is added to the
request vector store. We consider a formalized proof valid if and only if (a) the proof does not contain
”cheating” keywords (sorry or oops) that exit a proof without completing it. (b) Isabelle can verify
the proof code containing the corresponding formal statement.

3.3   E VOLVER

The lemmas extracted from the prover are mostly problem-specific, rendering them non-reusable
with limited applicability. And the number of these lemmas is also very limited. The objective of the
evolver is to create or refine these skills, enhancing their reusability and expanding their functional
coverage. As shown in Fig. 2 (b), the evolver contains two functionalities: the directional transformer
transforms the current skill and the request solver directly solves the request proposed by the prover
to create new lemmas. We detail each in the following.
Directional transformer. The objective of the directional transformer is to facilitate the evolution
of a skill along various predefined trajectories, thereby augmenting the reusability and usefulness
of the skill. It is composed of four distinct trajectories: extension of dimensions, identification of
key concepts, parameterization, and enhancement of complexity. Table. A.1 shows the detailed
functionality of each evolving direction. Each instance of the directional transformer adheres to a
unified prompt template depicted in Fig. 8. The adaptation involves substituting the core description


                                                   5
and its in-context examples for the corresponding evolving directions. Specifically, the directional
transformer begins with randomly selecting the least evolved skill (with the least amount of time
being selected to evolve). Subsequently, the transformer employs this skill to retrieve nd relevant
pending problem’s formal statement from the problem vector store and the relevant request’s formal
statement from the request vector store. Upon assembling the inputs for the LLM, the transformer
arbitrarily selects one direction of evolution and prompts the LLM to generate a novel skill.
Request solver. The request solver is designed to facilitate the development of new skills by directly
addressing the sub-goals proposed by the prover. As depicted in Fig. 7, the process initiated by the
request solver involves the random selection of a minimally solved request (with least amount of time
being selected to solve the request). After this selection, this request is employed to query the lemma
vector store to retrieve pertinent skills that can serve as references. Finally, the request solver prompts
the LLM to generate the proof for the request.
After obtaining the new skill (evolved lemma or solved request) generated by the LLM, the evolver
uses Isabelle to verify the generated code. To mitigate the risk of redundancy within the skill library,
a comparative strategy is conducted between the newly acquired skills and existing ones. This is
accomplished by employing the SequenceMatcher method from the difflib Python library,
which quantifies the level of difference between the new and existing skills. Only skills that have
been verified and exhibit a difference bellowing the predetermined threshold of 0.85 are incorporated
into the skill library.

4     E XPERIMENTS

4.1   E XPERIMENTAL SETUP

Implementation details. To expedite the experimental procedure, both the prover and the evolver
are executed in a multi-processing manner, maintaining a process number ratio of 3 : 8 respectively.
Consistent with the (Jiang et al., 2022b; Zhao et al., 2023), each problem undergoes 100 attempts
of proving. To maximally leverage the expanding skill library, problems are formalized through
successive rounds, with each round addressing each valid/test set problem once.
For the execution of the prover and the evolver, ChatGPT is utilized as the LLM.3 The temperature is
consistently set at T = 0.7 across all procedures. Within the prover, 3-shot examples are leveraged
for the decomposer. Regarding the formalizer, the quantity of reference skills nf is set to 6 for
the valid set and 4 for the test set, and paired with 2 formalization in-context examples. For the
directional transformer, the number of reference problem statements nd is set to 4, supplemented by
two directional transformation in-context examples. For the request solver, 3 skills are retrieved for
reference.
Dataset and evaluation. For a more accurate comparison, we follow (Jiang et al., 2022b; Zhao et al.,
2023) and adopt the miniF2F dataset (Zheng et al., 2021). This dataset includes 488 problems sourced
from high-school mathematical competitions. These problems vary in difficulty, ranging from basic
algebra and number theory, originating from the MATH dataset Hendrycks et al. (2021), to more
challenging problems found in the American Invitational Mathematics Examination (AIME) and
International Mathematical Olympiad (IMO). The problems are divided into valid and test sets, with
244 problems each. In this paper, we utilize the updated version of the miniF2F dataset from Jiang
et al. (2022b). Each question in this updated dataset contains a formal statement in Isabelle language,
an informal statement, and a human-written informal proof. For interacting with the Isabelle theorem
prover, we employ the PISA environment (Jiang et al., 2021). PISA is a flexible Python REPL
wrapper for Isabelle, capable of verifying Isabelle’s code and providing information such as proof
states or error messages from Isabelle.
Baseline methods. We have included baselines that represent state-of-the-art neural theorem proving
in Isabelle. Thor(Jiang et al., 2022a) and Thor with expert iteration on auto-formalized data (Wu
et al., 2022) are works focused on proof search paradigms, which use a fine-tuned 700m language
model to prove theorems. Draft, Sketch, and Prove (Jiang et al., 2022b) and Subgoal-Learning Zhao
et al. (2023) are works that use Codex or ChatGPT to prove theorems directly.
    3
      A combination of gpt-3.5-turbo, gpt-3.5-turbo-0301, gpt-3.5-turbo-0613, gpt-3.5-turbo-16k, and gpt-3.5-
turbo-16k-0613 is employed, with a model being selected randomly during calls to the OpenAI API.


                                                     6
Table 1: Proving success rates on the miniF2F dataset with Isabelle. The table displays the success rates of
previous works and the LEGO-Prover, The highest success rates for each set are highlighted in bold. LEGO-
Prover* denotes the cumulative pass rate of the miniF2F dataset, considering the total number of problems
solved using model-generated and human-written proofs.

          Success rate                                          LLM      miniF2F-valid   miniF2F-test
          Baselines
          Thor (Jiang et al., 2022a)                              -         28.3%          29.9%
          Thor + expert iteration (Wu et al., 2022)             Codex       37.3%          35.2%
          Draft, sketch, and Prove (Jiang et al., 2022b)        Codex       42.6%          39.3%
          Subgoal-Learning (Zhao et al., 2023)                 ChatGPT      48.0%          45.5%
          Ours (100 attempts)
          LEGO-Prover (model informal proof)                   ChatGPT      52.4%          45.5%
          LEGO-Prover (human informal proof)                   ChatGPT      55.3%          50.0%
          LEGO-Prover*                                         ChatGPT      57.0%          50.0%
          Ablations (50 attempts)
          LEGO-Prover                                          ChatGPT      50.4%             -
          - Skill Library                                      ChatGPT      47.1%             -


Following the setting from Jiang et al. (2022b), we test the LEGO-Prover with model-generated
and human-written informal proofs. The model-generated informal proofs are pre-generated using
GPT-4, with up to 20 informal proofs per problem. For each proving attempt, we randomly select
one proof as the informal proof to feed into the decomposer procedure. For ablation, we remove the
growing skill library to validate the effectiveness of the LEGO-Prover. Due to limited resources and
the expense of OpenAI API calls4 , we perform ablation only under 50 proving attempts per problem
on the miniF2F validation set.

4.2    M AIN RESULT

In Table. 1, we illustrate the proportion of successful formal proofs found on the miniF2F dataset.
Thor and Thor + expert iteration displays the performance of the fine-tuned search-based proving
method. The results indicate that all LLM-based methods significantly outperform the search-based
methods by around 4.7%. The efficacy of search-based proving methods is limited by the short proof
steps that the policy language model generates, drastically increasing the search space and, therefore,
hindering the prover from finding long proofs.
Our proposed LEGO-Prover significantly outperforms both search-based and LLM-based methods.
With proofs written by humans, the LEGO-Prover improves by 7.3% and 4.5% over the Subgoal-
Learning method on the miniF2F-valid and miniF2F-test datasets, respectively. A total of 257 out of
488 problems were solved by the LEGO-Prover with human-written proof. When replacing human-
written informal proofs with model-generated informal proofs, the LEGO-Prover still achieves 52.4%
and 45.5% pass rates on the valid set and test set, respectively, close to the results with human-written
informal proofs.
Effects of the growing skill library. The growing skill library greatly enhances the proving ability
of static LLMs like chatGPT or GPT-4. As the major contribution of LEGO-Prover, we are interested
in how well it contributes to solving more problems and improving the LLMs’ ability. Specifically,
we remove the growing skill library (including the evolver). As shown in the Table. 1, in 50 attempts,
LEGO-Prover achieves 50.4% on the validation set, whereas the LEGO-Prover without a skill library
achieves 47.1%. For a more intuitive representation, we further plot the trends of the number of
problems solved against the number of proving attempts for both settings, shown in Fig. 3(a).
Compared to the problem solved without a growing skill library, the advantage of adding the skill
library is initially minimal, as the libraries are still underdeveloped and lack useful skills. However, as
the skill library expands, the gap between LEGO-Prover and the ablation method widens consistently.
This outcome supports our hypothesis that the prover becomes increasingly adept at formalizing
theorems as more skills are added to the skill library.
   4
       Estimated to be around 300 dollars for one experiment with 100 proof attempts


                                                           7
                                 miniF2F-valid (human informal proof)                                                                                                                           miniF2F-valid (human informal proof)




                                                                                                                                  cumulative frequency of skill evolution patterns
                                                                                                                                                                                     17.5
                     120                                                                      10
                                                                                                                                                                                     15.0

                                                                                              8




                                                                                                  #skills in library (×103)
                     100                                                                                                                                                             12.5
#successful proofs

                                                                                                                                                                                     10.0
                                                                                              6                                                                                                                          direct use of retrieved skills
                     80                                                                                                                                                                                                  proposal of lemmas by imitation
                                                                                                                                                                                      7.5                                scale complexity
                                                                                              4                                                                                                                          extend dimensions
                                                                                                                                                                                      5.0                                identify key concepts
                     60                                                                                                                                                                                                  parameterize
                                                                                                                                                                                                                         do request
                                                                 ablation: no skill library 2                                                                                         2.5
                                                                 LEGO-Prover
                     40                                          number of skills                                                                                                     0.0
                                                                                             0
                           0        10           20           30          40              50                                                                                                0      20           40           60            80           100
                                          #total prover attempts                                                                                                                                         #total prover attempts
                                                      (a)                                                                                                                                                       (b)

             theorem imo_1988_p6_helper_generalized: new skill
                                                                             theorem imo_1988_p6:             formal statement                                                                          theorem division_remainder:              new skill
               fixes a b k x :: nat                                            fixes a b :: nat                                                                                                           fixes a b :: nat
               assumes h0 : "0<a \<and> 0<b"                                   assumes h0 : "0<a \<and> 0<b"                                                                                              assumes h0: "b > 0"
                 and h1 : "a\<le>b"                                               and h1 : "(a*b+1) dvd (a^2 + b^2)"                                                                                      shows "\<exists>q r. a = b * q + r \<and> r < b"
                 and h2 : "a^2 + b^2 = k*(a*b+x)"                              shows "\<exists>(x::nat). ((x^2) =                                                                                       proof -
                 and h3 : "x mod a = 0"                                      (a^2+b^2)/(a*b+1))"                                                                                                          obtain q r where "r = a mod b" and "a = b * q + r"
               shows "(a, b, k) = (a, b, (a^2+b^2) div (a*b+x))"                                                                                                                                            using div_mult_mod_eq[of a b] by auto
             proof -                                                                                                                                                                                      then have "a = b * q + (a mod b)" by simp
               have "(a^2 + b^2) mod (a*b+x) = 0"                                                                                                                                                         moreover have "a mod b < b"
                 using h2 h3 by (metis add.commute mod_mult_-                                                     decompose                                                                                 using mod_less_divisor[OF h0] by simp
             self2_is_0)                                                                                                                                                                                  ultimately show ?thesis by auto
                                                                             theorem imo_1988_p6_helper:
               then have "a^2 + b^2 = (a*b+x) * ((a^2+b^2) div                                                          request                                                                         qed
                                                                               fixes a b k :: nat
             (a*b+x))" by auto                                                 assumes h0 : h0 : "0<a \<and> 0<b"
               then have "a^2 + b^2 = (a*b+x) * k"                                                                                           theorem imo_1988_p6_helper:        old skill with
                                                                                 and h1 : "a\<le>b"                                            fixes a b k :: nat
                 using h2 by auto                                                and h2 : "a^2 + b^2 = k*(a*b+1)"                                                                     new proof
               then have "(a, b, k) = (a, b, (a^2+b^2) div                                                                                     assumes h0 : "0<a \<and> 0<b"
                                                                               shows "(a, b, k) = (a, b, (a^2+b^2) div (a*b+1))"                 and h1 : "a\<le>b"
             (a*b+x))"
                 by (metis add.commute add_eq_0_iff_both_eq_0                                                                                    and h2 : "a^2 + b^2 = k*(a*b+1)"
             bits_div_0 div_mult_self1_is_m h0 less_numeral_ex-                                                                                shows "(a, b, k) = (a, b, (a^2+b^2) div (a*b+1))"
             tra(3) mult.commute nonzero_mult_div_cancel_right)                                                                              proof -
                                                                                                 solve request                                 have "b > 0" using h0 h1 by auto
               then show ?thesis by auto
             qed                                                                                                                               obtain q r where "a^2 + b^2 = (a * b + 1) * q + r"
                                                                             theorem imo_1988_p6_helper:             new skill               and "r < (a * b + 1)"
                                                                               fixes a b k :: nat
                                                                  identify                                                                       using division_remainder[OF \<open>b > 0\<-
                                                                               assumes h0 : "0<a \<and> 0<b"
                                                                key concepts                                                                 close>] by auto
             theorem div_mult_le:                                                and h1 : "a\<le>b"
               fixes a b k x :: nat
                                                      new skill                  and h2 : "a^2 + b^2 = k*(a*b+1)"
                                                                                                                                               then have "a^2 + b^2 = (a * b + 1) * q + r \<and>
                                                                                                                                             r < (a * b + 1)" by auto
               assumes a b c :: nat                                            shows "(a, b, k) = (a, b, (a^2+b^2) div (a*b+1))"
                                                                                                                                               moreover have "(a * b + 1) * q + r = k * (a * b +
               shows "a div b \<le> c"                                       proof -
                                                                                                                                             1)"
             proof -                                                           have "log 2 (x powr y) = log 2 (exp (y * ln x))"
                                                                                                                                                 using h2 by simp
               have "a div b \<le> (b * c) div b"                                using assms by (simp add: powr_def)
                                                                                                                                               ultimately have "a^2 + b^2 = k * (a * b + 1)
                 using assms by (metis div_le_mono)                            also have "... = y * log 2 (exp (ln x))"
                                                                                                                                  identify   \<and> r < (a * b + 1)" by auto
               then show ?thesis by (metis Euclidean_Divi-      parameterize     by (metis assms(1) calculation exp_ln less_nu- key concepts
                                                                                                                                               then have "(a, b, k) = (a, b, (a^2+b^2) div
             sion.div_eq_0_iff Nat.lessE Zero_neq_Suc assms du-              meral_extra(3) log_powr of_nat_numeral)
                                                                                                                                             (a*b+1))"
             al_order.irrefl less_mult_imp_div_less linor-                     also have "... = y * log 2 x"
                                                                                                                                                 using div_mult_mod_eq[of "a^2 + b^2" "a * b +
             der_not_less mult.commute nonzero_mult_div_can-                     by (metis assms(1) exp_ln of_nat_numeral)
                                                                                                                                             1"] by auto
             cel_left order.strict_iff_not order_less_le)                      finally show ?thesis by simp
                                                                                                                                               then show ?thesis by auto
             qed                                                             qed



                                                                                                                 (c)

Figure 3: (a) A comparison of proof success rate between LEGO-Prover with and without the growing skill
library. As the number of skills grows (shown in green dotted line), the prover’s performance gap between
with and without the skill library becomes increasingly evident (b) Distribution of skill origins in successful
proofs, plotted against prover attempts and the percentage contribution of each skill origin to the total successful
proofs. The solid lines show the distribution of the two major methods by which the skill is used (direct use or
proposing a lemma by imitation). The dotted lines show the detailed skill origins used in the successful proofs.
(c) A skill-evolving tree gradually generated through multiple steps for imo 1988 p6 conceals how a relatively
large-scale skill library is produced from a few seed theorems.


4.3                        A NALYSIS

4.3.1                          W HAT DOES THE GROWING SKILL LIBRARY LOOK LIKE ?

Figure. 3(c) illustrates an example of a skill-evolving tree in the skill library. The grown skill library
is a massive forest containing numerous evolved trees like this one. The lemmas, originating from
either the prover or the evolver’s request solver sub-task (as the example shown in the figure), become
the root nodes of these skill-evolving trees. The evolver’s directional transformation generalizes
these lemmas and creates child nodes. In terms of statistics, there are 22532 skills in the skill library
in total, with 10.8% of the skills originating from the prover, 38.2% originating from the evolver’s
solve request sub-task, and 51.1% originating from the evolver’s directional transformation sub-tasks.
Although some lemmas are trivially true or already exist in Isabelle’s theorem library, LEGO-Prover
generates more unique, interesting, and useful lemmas. The gap between natural and formal language
is the greatest challenge in formalizing natural language mathematical proofs. A simple proving step
described in natural language can result in numerous lines of code written in the formal language.
However, this gap can gradually diminish as we accumulate more lemmas and theorems. To conclude,
the grown skill library generated by LEGO-Prover significantly enlarges this library and further
bridges the gap between informal and formal mathematical languages.


                                                                                                                              8
                              retrieved skill                                                                     retrieved skill
 lemma am_gm:                                                                       lemma prod_1n_4n:
   fixes x :: real                                                                    fixes n :: nat
   assumes "x > 0"                                                                    shows "(∏k = 1..n. (4 * k)) = 4^n * fact n"
   shows "x + 1/(2*x) ≥ sqrt 2"                                                     proof(induct n)
 proof -                                                                              case 0
   have "(sqrt x - sqrt (1/(2*x)))^2 ≥ 0" by simp                                     then show ?case by simp
   then have "x + 1/(2*x) - 2 * sqrt x * sqrt (1/(2*x)) ≥ 0"                        next
     by (smt (verit) add_le_imp_le_diff assms divide_nonneg_nonneg less_eq_-          case (Suc n)
 real_def real_sqrt_pow2 sum_squares_bound)                                           then show ?case by (simp add: algebra_simps)
   then have "x + 1/(2*x) - sqrt 2 ≥ 0"                                             qed
     by (metis add_divide_distrib assms div_by_1 divide_divide_eq_right di-
 vide_self less_numeral_extra(3) mult_2 one_add_one real_div_sqrt re-
 al_sqrt_divide real_sqrt_eq_1_iff real_sqrt_gt_0_iff real_sqrt_one times_di-                                   synthesized proof
 vide_eq_right zero_le_numeral)                                                     lemma prod_frac_common_factor:
   then have "x + 1/(2*x) ≥ sqrt 2" by simp
                                                                                      fixes n:: nat and a::real
   then show ?thesis by simp
                                                                                      assumes "a ≠ 0"
 qed
                                                                                      shows "(∏k = 1..n. (a * k + a) / (a * k)) = n + 1"
                                                                                    proof(induct n)
                                                                                      case 0
                          synthesized proof
                                                                                      then show ?case by simp
lemma am_gm:                                                                        next
  fixes x :: real                                                                     case (Suc n)
  assumes "x > 0"                                                                     have "(∏k = 1..Suc n. (a * k + a) / (a * k)) = ((a * Suc n + a) / (a * Suc
  shows "x + 1/(2*x) ≥ sqrt 2"                                                      n)) * (∏k = 1..n. (a * k + a) / (a * k))"
proof -                                                                                  by simp
  have "(sqrt x - sqrt (1/(2*x)))^2 ≥ 0" by simp                                      also have "... = ((a * Suc n + a) / (a * Suc n)) * (n + 1)"
  then have "x + 1/(2*x) - 2 * sqrt x * sqrt (1/(2*x)) ≥ 0"                              using Suc by simp
    by (smt (verit) add_le_imp_le_diff assms divide_nonneg_nonneg less_eq_-           also have "... = Suc n + 1"
real_def real_sqrt_pow2 sum_squares_bound)                                               using assms by (smt (verit) add.commute add_divide_distrib divisors_zero
  then have "x + 1/(2*x) - sqrt 2 ≥ 0"                                              nonzero_mult_div_cancel_left nonzero_mult_divide_mult_cancel_right of_nat_1
    by (metis add_divide_distrib assms div_by_1 divide_divide_eq_right di-          of_nat_add of_nat_neq_0 plus_1_eq_Suc right_inverse_eq times_divide_eq_left)
vide_self less_numeral_extra(3) mult_2 one_add_one real_div_sqrt re-                  finally show ?case by simp
al_sqrt_divide real_sqrt_eq_1_iff real_sqrt_gt_0_iff real_sqrt_one times_di-        qed
vide_eq_right zero_le_numeral)
  then have "x + 1/(2*x) ≥ sqrt 2" by simp                                          theorem amc12a_2008_p4:
  then show ?thesis by simp                                                           "(∏k::nat=1..501. ((4::real) * k + 4) / (4 * k)) = 502"
qed                                                                                 proof -
                                                                                      (* Step 1: Rewrite the given product as $\frac {8}{4}\cdot\frac {12}{8}\c-

  "⋀x. (x>0) ⟹ 2 - sqrt 2 ≥ 2 - x - 1/ (2 * x)"
theorem algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x:                                  dot\frac {16}{12}\cdots\frac {4n + 4}{4n}\cdots\frac {2008}{2004}$. *)
                                                                                      have "(∏k::nat=1..501. ((4::real) * k + 4) / (4 * k)) = (∏k::nat=1..501.
proof -                                                                             (4 * (k + 1)) / (4 * k))"
  fixes x :: real                                                                       by eval
  assumes h0: "x>0"                                                                   (* Step 2: Simplify the product by canceling out common factors. Notice
  (*Step 1: We want to show that $x + \frac{1}{2x} \geq \sqrt{2}$ is true.*)        that each term in the numerator cancels with the corresponding term in the
  (* Step 2: Apply the AM-GM inequality to $x$ and $\frac{1}{2x}$ to get $x         denominator, leaving only the last term $\frac {2008}{4}$. *)
+ \frac{1}{2x} \geq 2\sqrt{\frac{x}{2x}}$. *)                                         also have "... = (∏k::nat=1..501. (k + 1) / k)"
  (* Step 3: Simplify $2\sqrt{\frac{x}{2x}}$ to $\sqrt{2}$. *)                          by eval
  (* Step 4: Conclude that $x + \frac{1}{2x} \geq \sqrt{2}$ is true. *)               (* Use lemma 1 to simplify the product *)
have c1: "f (500 * (6/5)) = f 500 / (6/5)"                                            also have "... = 501 + 1"
  have "x + 1/(2*x) ≥ sqrt 2" using am_gm[OF h0] by simp                                using prod_frac_common_factor[of "1::real" "501"] by eval
  (* Step 5: Since $2 - \sqrt{2} \geq 2 - x - \frac{1}{2x}$ is equivalent to          (* Step 3: Calculate the value of $\frac {2008}{4}$ to find that it is
$x + \frac{1}{2x} \geq \sqrt{2}$, we can conclude that $2 - \sqrt{2} \geq 2         equal to $502$. *)
- x - \frac{1}{2x}$ is true. *)                                                       also have "... = 502"
  then show "2 - sqrt 2 ≥ 2 - x - 1/ (2 * x)" by simp                                   by simp
qed                                                                                   (* Step 4: Conclude that the given product is equal to $502$. *)
                                                                                      finally show ?thesis by simp
                                                                                    qed

                               (a) Directly Use                                                           (b) Propose Lemma by Imitation


Figure 4: Two primary forms of utilizing the skills. (a) Directly use. we retrieved the am gm skill from
the skill library and provided it as a reference skill for the formalizer. The formalizer synthesizes proof by
directly copying the lemma as part of the proof code and using the lemma in the main proof. (b) Propose lemma
by imitation. The retrieved lemma prod 1n 4n serves as a useful reference for the prover to synthesize the
lemma prod frac common factor.

4.3.2       H OW DOES THE SKILL BOOST THE ABILITY OF LLM S ?

To investigate closely how these learned skills can better help and boost the performance of LLM, we
manually inspect the successfully proven problems in the miniF2F valid set. The conclusions are as
follows:
Skill as directly reusable blocks. This is the most straightforward way of utilizing the generated
skills. Since every skill in the skill library is verified by the Isabelle prover, LLM can directly copy
the lemma code from the input prompt without fear of causing an error. As shown in Fig. 4 left,
the final proof of the problem algebra amgm faxinrrp2msqrt2geq2mxm1div2x directly
copies the retrieved skill am gm’s code as part of the proof and uses this lemma to help prove the
problem.
Skill as reference for solving the problem. Many skills cannot be directly reused but are
very helpful as reference examples for formalizing the main problem. As shown in Fig. 4
right, the retrieved skill examples prod 1n 4n provide great clues for solving the conjecture
prod frac common factor. Since the provided skills are lemmas with verified steps, these
steps drastically increase the accuracy of the LLM to generate the correct proof steps.
Fig. 3(b) first compares two scenarios: directly applying retrieved skills to the proofs and constructing
new lemmas by imitating retrieved skills to assist in theorem proving (represented by the light blue
and light green lines). It then examines the skill evolution pattern of the lemmas used in the proofs
(corresponding to Fig. 2 (b) and Table. 2). Out of 135 problems of the miniF2F-valid dataset passing
the validation of the Isabelle verifier, 24% is completed with the aid of retrieved skills. Within this
subset, 51% of the problems directly incorporate the retrieved skills into their proofs, while the
remaining 49% formulate new lemmas that are specifically tailored to address the distinct problems
at hand. Regarding the skills directly applied in the proofs, 71% are procured by the ”do requests”


                                                                                9
procedure. The skills derived through the evolution techniques of ”identifying key concepts” and
”scaling complexity” each contributes to 12%, while those acquired through ”parameterization”
constitute 6%. Although skill as directly reusable blocks is the most ideal usage of skills in the library,
the problems solved by directly reusing the skill are not substantial. That is because many trivial
problems in the dataset miniF2F can be solved trivially without requiring any skill as a reference.

5    C ONCLUSIONS
In this work, we introduced a new theorem-proving method, LEGO-Prover, which uses a growing
skill library to continuously boost the capability of LLM for formalization. The prover utilizes refined
structural informal proof and retrieved lemma to correctly formalize the proof. The evolver solves the
request proposed by the prover or evolves existing skills into new skills. LEGO-Prover introduces a
fundamentally different theorem proving paradigms for the community. With the previous approaches
all struggling to complete the proof at once, LEGO-Prover tries to prove the theorem in a block-by-
block manner, akin to divide and concur approaches. Extensive tests show that our method can indeed
improve pass rates on the miniF2F dataset. Our ablation studies and detailed analysis showcase the
effectiveness of each component we proposed in LEGO-Prover.

R EFERENCES
Jesse Alama, Michael Kohlhase, Lionel Mamane, Adam Naumowicz, Piotr Rudnicki, and Josef Urban.
  Licensing the mizar mathematical library. In James H. Davenport, William M. Farmer, Josef Urban,
  and Florian Rabe (eds.), Intelligent Computer Mathematics - 18th Symposium, Calculemus 2011,
  and 10th International Conference, MKM 2011, Bertinoro, Italy, July 18-23, 2011. Proceedings,
  volume 6824 of Lecture Notes in Computer Science, pp. 149–163. Springer, 2011. doi: 10.1007/
  978-3-642-22673-1\ 11. URL https://doi.org/10.1007/978-3-642-22673-1_
  11.
Alexander A. Alemi, François Chollet, Niklas Een, Geoffrey Irving, Christian Szegedy, and Josef
  Urban. DeepMath - deep sequence models for premise selection. In Proceedings of the 30th
  International Conference on Neural Information Processing Systems, NIPS’16, pp. 2243–2251,
  Red Hook, NY, USA, December 2016. Curran Associates Inc. ISBN 978-1-5108-3881-9.
Jeremy Avigad. Mathematics and the formal turn. 2023. URL https://www.andrew.cmu.
  edu/user/avigad/Papers/formal_turn.pdf.
Kshitij Bansal, Sarah M. Loos, Markus N. Rabe, Christian Szegedy, and Stewart Wilcox. Holist: An
  environment for machine learning of higher order logic theorem proving. In Kamalika Chaudhuri
  and Ruslan Salakhutdinov (eds.), Proceedings of the 36th International Conference on Machine
  Learning, ICML 2019, 9-15 June 2019, Long Beach, California, USA, volume 97 of Proceedings of
  Machine Learning Research, pp. 454–463. PMLR, 2019. URL http://proceedings.mlr.
  press/v97/bansal19a.html. 1
Kshitij Bansal, Christian Szegedy, Markus Norman Rabe, Sarah M. Loos, and Viktor Toman. Learning
  to Reason in Large Theories without Imitation. September 2020. URL https://openreview.
  net/forum?id=qbRv1k2AcH.
Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Jean-Christophe Filliâtre, Ed-
  uardo Giménez, Hugo Herbelin, Gérard Huet, César Muñoz, Chetan Murthy, Catherine Parent,
  Christine Paulin-Mohring, Amokrane Saı̈bi, and Benjamin Werner. The Coq Proof Assistant
  Reference Manual : Version 6.1. report, INRIA, May 1997. URL https://hal.inria.fr/
  inria-00069968. Pages: 214. 3
Clark Barrett, Christopher L Conway, Morgan Deters, Liana Hadarean, Dejan Jovanović, Tim King,
  Andrew Reynolds, and Cesare Tinelli. Cvc4. In Computer Aided Verification: 23rd International
  Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings 23, pp. 171–177.
  Springer, 2011.
Alexander Bentkamp, Jasmin Blanchette, Sophie Tourret, and Petar Vukmirović. Superposition for
  Full Higher-order Logic. In André Platzer and Geoff Sutcliffe (eds.), Automated Deduction –


                                                    10
  CADE 28, Lecture Notes in Computer Science, pp. 396–412, Cham, 2021. Springer International
  Publishing. ISBN 978-3-030-79876-5. doi: 10.1007/978-3-030-79876-5 23.
Garrett Birkhoff. Rings of sets. Duke Mathematical Journal, (3):443–454, 1937.
Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx,
  Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson,
  Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri Chatterji, Annie Chen, Kathleen Creel,
  Jared Quincy Davis, Dora Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano
  Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren
  Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter
  Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil
  Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar
  Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal
  Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu
  Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric Mitchell, Zanele Munyikwa,
  Suraj Nair, Avanika Narayan, Deepak Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles,
  Hamed Nilforoshan, Julian Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung
  Park, Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu
  Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa Sadigh,
  Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan Taori,
  Armin W. Thomas, Florian Tramèr, Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai
  Wu, Sang Michael Xie, Michihiro Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi
  Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. On the
  Opportunities and Risks of Foundation Models. Technical Report arXiv:2108.07258, arXiv,
  August 2021. URL http://arxiv.org/abs/2108.07258. arXiv:2108.07258 [cs] type:
  article.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,
  Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel
  Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler,
  Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Ben-
  jamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and
  Dario Amodei. Language Models are Few-Shot Learners. In H. Larochelle, M. Ranzato, R. Hadsell,
  M. F. Balcan, and H. Lin (eds.), Advances in Neural Information Processing Systems, volume 33,
  pp. 1877–1901. Curran Associates, Inc., 2020. URL https://proceedings.neurips.
  cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf.
Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar,
   Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi, Marco Tulio
   Ribeiro, and Yi Zhang. Sparks of artificial general intelligence: Early experiments with gpt-4,
   2023.
Aydar Bulatov, Yuri Kuratov, and Mikhail S. Burtsev. Recurrent memory transformer, 2022.
Aydar Bulatov, Yuri Kuratov, and Mikhail S. Burtsev. Scaling transformer to 1m tokens and beyond
  with rmt, 2023.
Kevin Buzzard, Johan Commelin, and Patrick Massot. Formalising perfectoid spaces. CoRR,
  abs/1910.12320, 2019. URL http://arxiv.org/abs/1910.12320.
Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou. Large language models as
  tool makers. arXiv preprint arXiv:2305.17126, 2023. 3
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared
 Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri,
 Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan,
 Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian,
 Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios
 Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino,
 Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders,
 Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa,


                                               11
  Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob
  McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating
  large language models trained on code. CoRR, abs/2107.03374, 2021. URL https://arxiv.
  org/abs/2107.03374.
Noam Chomsky. Three models for the description of language. IRE Transactions on information
  theory, 2(3):113–124, 1956.
Thierry Coquand and Gérard Huet. The calculus of constructions. PhD thesis, INRIA, 1986.
Thierry Coquand and Gérard Huet. The calculus of constructions. Information and Computation, 76
  (2):95–120, February 1988. ISSN 0890-5401. doi: 10.1016/0890-5401(88)90005-3. URL https:
  //www.sciencedirect.com/science/article/pii/0890540188900053.
Thierry Coquand and Christine Paulin. Inductively defined types. In Per Martin-Löf and Grigori
  Mints (eds.), COLOG-88, Lecture Notes in Computer Science, pp. 50–66, Berlin, Heidelberg,
  1990. Springer. ISBN 978-3-540-46963-6. doi: 10.1007/3-540-52335-9 47.
Sander R. Dahmen, Johannes Hölzl, and Robert Y. Lewis. Formalizing the solution to the cap
  set problem. In John Harrison, John O’Leary, and Andrew Tolmach (eds.), 10th International
  Conference on Interactive Theorem Proving, ITP 2019, September 9-12, 2019, Portland, OR,
  USA, volume 141 of LIPIcs, pp. 15:1–15:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik,
  2019. doi: 10.4230/LIPIcs.ITP.2019.15. URL https://doi.org/10.4230/LIPIcs.ITP.
  2019.15.
Giannis Daras and Alexandros G. Dimakis. Discovering the Hidden Vocabulary of DALLE-2.
  Technical Report arXiv:2206.00169, arXiv, May 2022. URL http://arxiv.org/abs/
  2206.00169. arXiv:2206.00169 [cs] type: article.
Martin Davis, George Logemann, and Donald Loveland. A machine program for theorem-proving.
 Communications of the ACM, 5(7):394–397, 1962. ISSN 0001-0782. doi: 10.1145/368273.368557.
 URL https://doi.org/10.1145/368273.368557.
Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In Proceedings of the
  Theory and Practice of Software, 14th International Conference on Tools and Algorithms for the
  Construction and Analysis of Systems, TACAS’08/ETAPS’08, pp. 337–340, Berlin, Heidelberg,
  2008. Springer-Verlag. ISBN 3540787992.
Leonardo de Moura and Nikolaj Bjørner. Z3: An Efficient SMT Solver. In C. R. Ramakrishnan
  and Jakob Rehof (eds.), Tools and Algorithms for the Construction and Analysis of Systems,
  Lecture Notes in Computer Science, pp. 337–340, Berlin, Heidelberg, 2008. Springer. ISBN
  978-3-540-78800-3. doi: 10.1007/978-3-540-78800-3 24.
Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von Raumer.
  The Lean Theorem Prover (System Description). In Amy P. Felty and Aart Middeldorp (eds.),
  Automated Deduction - CADE-25, Lecture Notes in Computer Science, pp. 378–388, Cham, 2015.
  Springer International Publishing. ISBN 978-3-319-21401-6. doi: 10.1007/978-3-319-21401-6 26.
  1, 3
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: pre-training of
  deep bidirectional transformers for language understanding. In Jill Burstein, Christy Doran, and
  Thamar Solorio (eds.), Proceedings of the 2019 Conference of the North American Chapter of
  the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT
  2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers), pp. 4171–
  4186. Association for Computational Linguistics, 2019. doi: 10.18653/v1/n19-1423. URL
  https://doi.org/10.18653/v1/n19-1423.
Gabriel Ebner, Sebastian Ullrich, Jared Roesch, Jeremy Avigad, and Leonardo de Moura. A metapro-
  gramming framework for formal verification. Proc. ACM Program. Lang., 1(ICFP), aug 2017. doi:
 10.1145/3110278. URL https://doi.org/10.1145/3110278.
Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation and
 repair with large language models. CoRR, abs/2303.04910, 2023. doi: 10.48550/arXiv.2303.04910.
 URL https://doi.org/10.48550/arXiv.2303.04910. 1, 2, 3


                                               12
Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang,
  Horace He, Anish Thite, Noa Nabeshima, Shawn Presser, and Connor Leahy. The Pile: An 800gb
  dataset of diverse text for language modeling. arXiv preprint arXiv:2101.00027, 2020.
Vijay K. Garg. Introduction to Lattice Theory with Computer Science Applications. Wiley Publishing,
  1st edition, 2015. ISBN 1118914376.
Thibault Gauthier, Cezary Kaliszyk, and Josef Urban. Tactictoe: Learning to reason with HOL4
  tactics. In Thomas Eiter and David Sands (eds.), LPAR-21, 21st International Conference on
  Logic for Programming, Artificial Intelligence and Reasoning, Maun, Botswana, May 7-12, 2017,
  volume 46 of EPiC Series in Computing, pp. 125–143. EasyChair, 2017. doi: 10.29007/ntlb. URL
  https://doi.org/10.29007/ntlb.
Emmanuel Gunther, Miguel Pagano, Pedro Sánchez Terraf, and Matı́as Steinberg. The independence
  of the continuum hypothesis in isabelle/zf. Arch. Formal Proofs, 2022, 2022. URL https:
 //www.isa-afp.org/entries/Independence_CH.html.
Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W. Ayers, and Stanislas Polu. Proof Artifact
  Co-training for Theorem Proving with Language Models. ICLR 2022, February 2021. URL
  http://arxiv.org/abs/2102.06203. arXiv: 2102.06203.
Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W. Ayers, and Stanislas Polu. Proof artifact
  co-training for theorem proving with language models. In The Tenth International Conference on
  Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022. OpenReview.net, 2022.
  URL https://openreview.net/forum?id=rpxJc9j04U. 1, 2, 3
John Harrison. HOL light: An overview. In Stefan Berghofer, Tobias Nipkow, Christian Urban, and
  Makarius Wenzel (eds.), Theorem Proving in Higher Order Logics, 22nd International Conference,
  TPHOLs 2009, Munich, Germany, August 17-20, 2009. Proceedings, volume 5674 of Lecture
  Notes in Computer Science, pp. 60–66. Springer, 2009. doi: 10.1007/978-3-642-03359-9\ 4. URL
  https://doi.org/10.1007/978-3-642-03359-9_4.
John Harrison, Josef Urban, and Freek Wiedijk. History of interactive theorem proving. In Jörg H.
  Siekmann (ed.), Computational Logic, volume 9 of Handbook of the History of Logic, pp. 135–214.
  Elsevier, 2014a. doi: 10.1016/B978-0-444-51624-4.50004-6. URL https://doi.org/10.
  1016/B978-0-444-51624-4.50004-6.
John Harrison, Josef Urban, and Freek Wiedijk. History of interactive theorem proving. In Computa-
  tional Logic, volume 9, pp. 135–214, 2014b.
John Harrison, Josef Urban, and Freek Wiedijk. History of Interactive Theorem Proving. In
  Handbook of the History of Logic, volume 9, pp. 135–214. Elsevier, 2014c. ISBN 978-0-444-51624-
  4. doi: 10.1016/B978-0-444-51624-4.50004-6. URL https://linkinghub.elsevier.
  com/retrieve/pii/B9780444516244500046.
Chadi Helwe, Chloe Clavel, and Fabian Suchanek. Reasoning with Transformer-based Models: Deep
  Learning, but Shallow Reasoning. Deep Learning, pp. 28.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset, 2021. 6
William Alvin Howard. The Formulae-as-Types Notion of Construction. In Haskell Curry, Hindley
 B, Seldin J. Roger, and P. Jonathan (eds.), To H. B. Curry: Essays on Combinatory Logic, Lambda
 Calculus, and Formalism. Academic Press, 1980.
Geoffrey Jefferson. The mind of mechanical man. British Medical Journal, 1(4616):1105, 1949.
Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Yejin Bang, Andrea
  Madotto, and Pascale Fung. Survey of hallucination in natural language generation. CoRR,
  abs/2202.03629, 2022. URL https://arxiv.org/abs/2202.03629.
Albert Q Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr
  Miłoś, Yuhuai Wu, and Mateja Jamnik. Thor: Wielding hammers to integrate language models
  and automated theorem provers. arXiv preprint arXiv:2205.10893, 2022a. 1, 2, 3, 6, 7


                                                13
Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
  Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem
  provers with informal proofs. CoRR, abs/2210.12283, 2022b. doi: 10.48550/arXiv.2210.12283.
  URL https://doi.org/10.48550/arXiv.2210.12283. 1, 2, 3, 5, 6, 7

Albert Qiaochu Jiang, Wenda Li, Jesse Michael Han, and Yuhuai Wu. Lisa: Language models of
  isabelle proofs. 2021. 1, 6

Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large
  Language Models are Zero-Shot Reasoners. Technical Report arXiv:2205.11916, arXiv, May 2022.
  URL http://arxiv.org/abs/2205.11916. arXiv:2205.11916 [cs] type: article.

Laura Kovács and Andrei Voronkov. First-Order Theorem Proving and Vampire. In Natasha
  Sharygina and Helmut Veith (eds.), Computer Aided Verification, Lecture Notes in Computer
  Science, pp. 1–35, Berlin, Heidelberg, 2013. Springer. ISBN 978-3-642-39799-8. doi: 10.1007/
  978-3-642-39799-8 1.

Guillaume Lample and François Charton.    Deep Learning for Symbolic Mathematics.
  arXiv:1912.01412 [cs], December 2019. URL http://arxiv.org/abs/1912.01412.
  arXiv: 1912.01412.

Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril, Xavier Martinet, Amaury Hayat, Gabriel
  Ebner, Aurélien Rodriguez, and Timothée Lacroix. HyperTree Proof Search for Neural Theorem
  Proving. Technical Report arXiv:2205.11491, arXiv, May 2022. URL http://arxiv.org/
  abs/2205.11491. arXiv:2205.11491 [cs] type: article. 1, 2, 3

Yann LeCun, Yoshua Bengio, and Geoffrey Hinton. Deep learning. Nature, 521(7553):436–444,
  May 2015. ISSN 1476-4687. doi: 10.1038/nature14539. URL https://www.nature.com/
  articles/nature14539. Number: 7553 Publisher: Nature Publishing Group.

Mike Lewis, Yinhan Liu, Naman Goyal, Marjan Ghazvininejad, Abdelrahman Mohamed, Omer
 Levy, Ves Stoyanov, and Luke Zettlemoyer. Bart: Denoising sequence-to-sequence pre-training for
 natural language generation, translation, and comprehension, 2019.

Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay V.
  Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam
  Neyshabur, Guy Gur-Ari, and Vedant Misra. Solving quantitative reasoning problems with language
  models. In NeurIPS, 2022. URL http://papers.nips.cc/paper_files/paper/
  2022/hash/18abbeef8cfe9203fdf9053c9c4fe191-Abstract-Conference.
  html.

Wenda Li, Lei Yu, Yuhuai Wu, and Lawrence C. Paulson. IsarStep: a Benchmark for High-level
 Mathematical Reasoning. In ICLR 2021, September 2020. URL https://openreview.net/
 forum?id=Pzj6fzU6wkj.

Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom
  Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien
  de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven
  Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson,
  Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-Level
  Code Generation with AlphaCode. arXiv:2203.07814 [cs], February 2022. URL http://
  arxiv.org/abs/2203.07814. arXiv: 2203.07814.

Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
  Chuanyang Zheng, Yichun Yin, Lin Li, et al. Fimo: A challenge formal dataset for automated
  theorem proving. arXiv preprint arXiv:2309.04295, 2023. 1

Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike
  Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized BERT pretraining
  approach. CoRR, abs/1907.11692, 2019. URL http://arxiv.org/abs/1907.11692.


                                               14
Sarah M. Loos, Geoffrey Irving, Christian Szegedy, and Cezary Kaliszyk. Deep network guided
  proof search. In Thomas Eiter and David Sands (eds.), LPAR-21, 21st International Conference on
  Logic for Programming, Artificial Intelligence and Reasoning, Maun, Botswana, May 7-12, 2017,
  volume 46 of EPiC Series in Computing, pp. 85–105. EasyChair, 2017. doi: 10.29007/8mwc. URL
  https://doi.org/10.29007/8mwc.
Haipeng Luo, Qingfeng Sun, Can Xu, Pu Zhao, Jianguang Lou, Chongyang Tao, Xiubo Geng,
  Qingwei Lin, Shifeng Chen, and Dongmei Zhang. WizardMath: Empowering Mathematical
  Reasoning for Large Language Models via Reinforced Evol-Instruct, August 2023. URL http:
 //arxiv.org/abs/2308.09583. arXiv:2308.09583 [cs].
Carlin MacKenzie, Jacques D. Fleuriot, and James Vaughan. An evaluation of the archive of formal
  proofs. CoRR, abs/2104.01052, 2021. URL https://arxiv.org/abs/2104.01052.
The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, CPP 2020, pp. 367–381, New York,
  NY, USA, 2020. Association for Computing Machinery. ISBN 978-1-4503-7097-4. doi: 10.1145/
  3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
John McCarthy, Marvin L Minsky, Nathaniel Rochester, and Claude E Shannon. A proposal for the
  dartmouth summer research project on artificial intelligence, august 31, 1955. AI magazine, 27(4):
  12–12, 2006.
Norman Megill and David A Wheeler. Metamath: a computer language for mathematical proofs.
  Lulu Press, 2019. ISBN 978-0-359-70223-7. OCLC: 1105224041. 3
Maciej Mikuła, Szymon Antoniak, Szymon Tworkowski, Albert Qiaochu Jiang, Jin Peng Zhou,
 Christian Szegedy, Łukasz Kuciński, Piotr Miłoś, and Yuhuai Wu. Magnushammer: A transformer-
 based approach to premise selection. arXiv preprint arXiv:2303.04488, 2023. 3
OpenAI. GPT-4 technical report. CoRR, abs/2303.08774, 2023. doi: 10.48550/arXiv.2303.08774.
  URL https://doi.org/10.48550/arXiv.2303.08774. 2
Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and
  Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior, 2023. 3
Lawrence C. Paulson. Isabelle a Generic Theorem Prover. Springer Verlag, 1994. 1, 3
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  CoRR, abs/2009.03393, 2020a. URL https://arxiv.org/abs/2009.03393. 1, 2, 3
Stanislas Polu and Ilya Sutskever. Generative Language Modeling for Automated Theorem Prov-
  ing. arXiv:2009.03393 [cs, stat], September 2020b. URL http://arxiv.org/abs/2009.
  03393. arXiv: 2009.03393.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal Mathematics Statement Curriculum Learning. (arXiv:2202.01344), February
  2022. doi: 10.48550/arXiv.2202.01344. URL http://arxiv.org/abs/2202.01344.
  arXiv:2202.01344 [cs] type: article. 2, 3
Jianing Qiu, Lin Li, Jiankai Sun, Jiachuan Peng, Peilun Shi, Ruiyang Zhang, Yinzhao Dong, Kyle
   Lam, Frank P-W Lo, Bo Xiao, et al. Large ai models in health informatics: Applications, challenges,
   and the future. arXiv preprint arXiv:2303.11568, 2023.
Markus Norman Rabe, Dennis Lee, Kshitij Bansal, and Christian Szegedy. Mathematical Reasoning
 via Self-supervised Skip-tree Training. September 2020. URL https://openreview.net/
 forum?id=YmqAnY0CMEy.
Markus Norman Rabe, Dennis Lee, Kshitij Bansal, and Christian Szegedy. Mathematical reasoning
 via self-supervised skip-tree training. In 9th International Conference on Learning Representations,
 ICLR 2021, Virtual Event, Austria, May 3-7, 2021. OpenReview.net, 2021. URL https://
 openreview.net/forum?id=YmqAnY0CMEy.


                                                 15
Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language
  Models are Unsupervised Multitask Learners. pp. 24.
Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Lan-
  guage models are unsupervised multitask learners. 2018a. URL https://d4mucfpksywv.
  cloudfront.net/better-language-models/language-models.pdf.
Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Lan-
  guage models are unsupervised multitask learners. 2018b. URL https://d4mucfpksywv.
  cloudfront.net/better-language-models/language-models.pdf.
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi
  Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text
  transformer, 2020.
Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel
  Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake
  Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals,
  Mahyar Bordbar, and Nando de Freitas. A Generalist Agent. Technical Report arXiv:2205.06175,
  arXiv, May 2022. URL http://arxiv.org/abs/2205.06175. arXiv:2205.06175 [cs]
  type: article.
Alexandre Riazanov and Andrei Voronkov. The design and implementation of vampire. AI communi-
  cations, 15(2-3):91–110, 2002.
J. A. Robinson. A Machine-Oriented Logic Based on the Resolution Principle. Journal of the ACM,
   12(1):23–41, 1965. ISSN 0004-5411. doi: 10.1145/321250.321253. URL https://doi.org/
   10.1145/321250.321253.
Stephan Schulz. E - a brainiac theorem prover. AI Communications, 15(2,3):111–126, August 2002.
  ISSN 0921-7126.
Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang. Hugginggpt:
  Solving ai tasks with chatgpt and its friends in hugging face, 2023. 3
David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den Driessche,
  Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, Sander Dieleman,
  Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy Lillicrap, Madeleine
  Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis. Mastering the game of Go with
  deep neural networks and tree search. Nature, 529(7587):484–489, January 2016. ISSN 1476-4687.
  doi: 10.1038/nature16961. URL https://www.nature.com/articles/nature16961.
  Number: 7587 Publisher: Nature Publishing Group.
David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur
  Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy Lillicrap,
  Karen Simonyan, and Demis Hassabis. Mastering Chess and Shogi by Self-Play with a
  General Reinforcement Learning Algorithm. arXiv:1712.01815 [cs], December 2017. URL
  http://arxiv.org/abs/1712.01815. arXiv: 1712.01815.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée
  Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand
 Joulin, Edouard Grave, and Guillaume Lample. LLaMA: Open and Efficient Foundation Language
  Models, February 2023a. URL http://arxiv.org/abs/2302.13971. arXiv:2302.13971
  [cs].
Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cris-
  tian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu,
  Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn,
  Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel
  Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee,
  Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra,


                                                  16
  Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi,
  Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh
  Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen
  Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic,
  Sergey Edunov, and Thomas Scialom. Llama 2: Open Foundation and Fine-Tuned Chat Models,
  July 2023b. URL http://arxiv.org/abs/2307.09288. arXiv:2307.09288 [cs].

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
  Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Isabelle Guyon, Ulrike von
  Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman
  Garnett (eds.), Advances in Neural Information Processing Systems 30: Annual Conference on
  Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA, pp.
  5998–6008, 2017. URL https://proceedings.neurips.cc/paper/2017/hash/
  3f5ee243547dee91fbd053c1c4a845aa-Abstract.html.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
 Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. arXiv
  preprint arXiv: Arxiv-2305.16291, 2023a. 3

Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen, Yichun Yin, Jing Xiong, Enze Xie, Han Shi,
  Yujun Li, Lin Li, et al. Dt-solver: Automated theorem proving with dynamic-tree sampling guided
  by proof-level value function. In Proceedings of the 61st Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers), pp. 12632–12646, 2023b. 1, 2, 3

Mingzhe Wang and Jia Deng. Learning to Prove Theorems by Learning to Generate Theorems. In
 Advances in Neural Information Processing Systems, volume 33, pp. 18146–18157. Curran As-
 sociates, Inc., 2020. URL https://proceedings.neurips.cc/paper/2020/hash/
 d2a27e83d429f0dcae6b937cf440aeb1-Abstract.html.

Qingxiang Wang, Cezary Kaliszyk, and Josef Urban. First experiments with neural translation
  of informal to formal mathematics. In Intelligent Computer Mathematics: 11th International
  Conference, CICM 2018, Hagenberg, Austria, August 13-17, 2018, Proceedings 11, pp. 255–270.
  Springer, 2018. 3

Zhenhailong Wang, Shaoguang Mao, Wenshan Wu, Tao Ge, Furu Wei, and Heng Ji. Unleashing
  cognitive synergy in large language models: A task-solving agent through multi-persona self-
  collaboration, 2023c. 3

Christoph Weidenbach, Dilyana Dimova, Arnaud Fietzke, Rohit Kumar, Martin Suda, and Patrick
  Wischnewski. Spass version 3.5. In Renate A. Schmidt (ed.), Automated Deduction – CADE-22,
  pp. 140–145, Berlin, Heidelberg, 2009. Springer Berlin Heidelberg. ISBN 978-3-642-02959-2.

Daniel Whalen. Holophrasm: a neural automated theorem prover for higher-order logic. CoRR,
  abs/1608.02644, 2016a. URL http://arxiv.org/abs/1608.02644.

Daniel Whalen. Holophrasm: a neural Automated Theorem Prover for higher-order logic. Technical
  Report arXiv:1608.02644, arXiv, August 2016b. URL http://arxiv.org/abs/1608.
  02644. arXiv:1608.02644 [cs] type: article.

Wikipedia contributors. Recursion (computer science) — Wikipedia, the free encyclope-
 dia, 2023. URL https://en.wikipedia.org/w/index.php?title=Recursion_
 (computer_science)&oldid=1143431394. [Online; accessed 14-May-2023].

Yuhuai Wu, Albert Qiaochu Jiang, Jimmy Ba, and Roger Grosse. INT: An Inequality Benchmark for
  Evaluating Generalization in Theorem Proving. ICLR 2021, April 2021. URL http://arxiv.
  org/abs/2007.02924. arXiv: 2007.02924.

Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and
  Christian Szegedy. Autoformalization with large language models. Advances in Neural Information
  Processing Systems, 35:32353–32368, 2022. 3, 6, 7


                                               17
Jing Xiong, Chengming Li, Min Yang, Xiping Hu, and Bin Hu. Expression syntax information
   bottleneck for math word problems. In Enrique Amigó, Pablo Castells, Julio Gonzalo, Ben
   Carterette, J. Shane Culpepper, and Gabriella Kazai (eds.), SIGIR ’22: The 45th International
   ACM SIGIR Conference on Research and Development in Information Retrieval, Madrid, Spain,
   July 11 - 15, 2022, pp. 2166–2171. ACM, 2022. doi: 10.1145/3477495.3531824. URL https:
   //doi.org/10.1145/3477495.3531824.
Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting with proof assistants. In
  Kamalika Chaudhuri and Ruslan Salakhutdinov (eds.), Proceedings of the 36th International
  Conference on Machine Learning, ICML 2019, 9-15 June 2019, Long Beach, California, USA,
  volume 97 of Proceedings of Machine Learning Research, pp. 6984–6994. PMLR, 2019. URL
  http://proceedings.mlr.press/v97/yang19a.html.
Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-augmented
  language models. arXiv preprint arXiv:2306.15626, 2023. 1, 2
Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu, Zhengying Liu, Yu Zhang, James T. Kwok,
  Zhenguo Li, Adrian Weller, and Weiyang Liu. Metamath: Bootstrap your own mathematical
  questions for large language models, 2023.
Zahra Zahedi and Subbarao Kambhampati. Human-ai symbiosis: A survey of current approaches,
  2021. 3
Xueliang Zhao, Wenda Li, and Lingpeng Kong. Decomposing the enigma: Subgoal-based demon-
  stration learning for formal theorem proving. arXiv preprint arXiv:2305.16366, 2023. 1, 2, 3, 5, 6,
 7
Chuanyang Zheng, Zhengying Liu, Enze Xie, Zhenguo Li, and Yu Li. Progressive-hint prompting
  improves reasoning in large language models. arXiv preprint arXiv:2304.09797, 2023.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. miniF2F: a cross-system benchmark for
  formal Olympiad-level mathematics. September 2021. URL https://openreview.net/
  forum?id=9ZPegFuFTFv. 2, 6




                                                 18
A     A PPENDIX
A.1   P ROMPT EXAMPLES

In this section, we illustrate the prompts used in the LEGO-Prover. For prover, the prompt used is the
decomposer (Fig. 5), and the formalizer (Fig. 6). For the evolver, the prompt used is the directional
evolver (Fig. 8) and request solver (Fig. 7). The blue line separates the LLMs’ input and outputs.
For directional evolve, we list all the core statement to be replaced in the Table. 2

Table 2: The core description of individual directional evolve. The description will be replaced into
the directional evolve prompt template.

                Evolve type        Description
                                   Determine the essential ideas, methods, or
           Identify key concepts
                                   theorems that are crucial to solving the initial problem.
                                   If the problem involves specific numbers, generalize
               Parameterize
                                   it by replacing these with variables.
                                   Try both simpler and more complicated versions of the
             Scale complexity
                                   problem to see how the approach adapts.
                                   If the problem is defined in a specific number of dimensions,
            Extend dimensions
                                   consider if it holds in more or fewer dimensions.




                                                    19
Input:
System message: As a mathematician and expert in Isabelle theorem prover, your task is to analyze the given theorem (including the prob-
lem’s informal statement, human written informal proof, and formal statement). Provide a better structured step-by-step proof that is closer to Isabelle.
and request relevant lemmas, and theorems that might help in proving this problem. Statement: If a ≥ b > 1, what is the largest possible value of
loga (a/b) + logb (b/a)? Show that it is 0.
Informal proof: Using logarithmic rules, we see that loga a − loga b + logb b − logb a = 2 − (loga b + logb a) = 2 − (loga b + log1 b )
                                                                                                                                                    a
Since a and b are both greater than 1, using [[AM-GM]] gives that the term in parentheses must be at least 2, so the largest possible values is 2 − 2 = 0
Note that the maximum occurs when a = b.
Formal statement:
theorem
  fixes a b::real
  assumes "b\<le>a"
      and "1<b"
  shows "ln (a/b) / ln a + ln (b/a) / ln b \<le>0" (is "?L \<le> _")
Structure proof: Step 1: Introduce variables x and y to represent the natural logarithms of a and b respectively.
Step 2: Given that b > 1, conclude that the natural logarithm of b, y, is greater than 0.
Step 3: Using the given assumptions, establish that x ≥ y. This implies x > 0.
Step 4: Express the LHS of the main inequality in terms of x and y.
Step 5: Simplify the expression derived in Step 4.
Step 6: Demonstrate that the above expression is less than or equal to 0. The Arithmetic Mean-Geometric Mean Inequality (AM-GM) is used here to argue
that the term (y/x + x/y) is at least 2, hence the expression is at most 0.
Required skills:
Thoughts 1: A base lemma proving am gm inequality that is useful for step 6
Code 1:
lemma am_gm:
  fixes x y :: real
  assumes "x >= 0" "y >= 0"
  shows "xˆ2 + yˆ2 >= 2*x*y"
Thoughts 2: According to the step 6, we derived a special form of am gm inequality. which proofs the conjecture x/y + y/x >= 2 required in step 6.
Code 2:
lemma am_gm_divide_form:
  fixes x y :: real
  assumes "x > 0" "y > 0"
  shows "x/y + y/x >= 2"
[two more examples like above...] Statement: What is the least possible value of (xy − 1)2 + (x + y)2 for real numbers x and y? Show that it is 1.
Informal proof:
Expanding, we get that the expression is x2 + 2xy + y 2 + x2 y 2 − 2xy + 1 or x2 + y 2 + x2 y 2 + 1. By the Trivial Inequality (all squares are
nonnegative) the minimum value for this is 1, which can be achieved at x = y = 0.
Formal statement:
theorem amc12a_2021_p7:
  fixes x y ::real
  shows "1 \<le> ((x * y) - 1)ˆ2 + (x + y)ˆ2"
  apply (auto simp:algebra_simps power2_eq_square)


Output:
Structure proof:
Step 1: Expand the expression (xy − 1)2 + (x + y)2 to obtain x2 + 2xy + y 2 + x2 y 2 − 2xy + 1.
Step 2: Simplify the expression derived in Step 1 to obtain x2 + y 2 + x2 y 2 + 1.
Step 3: Apply the Trivial Inequality, which states that all squares are nonnegative, to argue that the minimum value of the expression is 1.
Step 4: Show that the minimum value of 1 can be achieved when x = y = 0.
Required skills:
Thoughts 1: The Trivial Inequality is a key concept in this proof. Understanding and applying this inequality is crucial to show that the minimum value of
the expression is 1.
Code 1:
lemma trivial_inequality:
  fixes a :: real
  shows "0 \<le> aˆ2"
Thoughts 2: The ability to expand and simplify algebraic expressions is important in this proof.
Code 2:
lemma expand_expression:
  fixes x y :: real
  shows "(x * y - 1)ˆ2 + (x + y)ˆ2 = xˆ2 + 2 * x * y + yˆ2 + xˆ2 * yˆ2 - 2 * x * y + 1"
Thoughts 3: The ability to substitute values into an expression and evaluate it is necessary to show that the minimum value of 1 can be achieved when
x = y = 0.
Code 3:
lemma substitute_values:
  fixes x y :: real
  assumes "x = 0" "y = 0"
  shows "(x * y - 1)ˆ2 + (x + y)ˆ2 = 1"




                                        Figure 5: Prompt example for decomposer.




                                                                           20
Input:
System message: As a mathematician familiar with Isabelle, your task is to provide formal proof in response to a given problem statement.
Your proof should be structured and clearly written, meeting the following criteria:
- It can be verified by Isabelle.
- Each step of the proof should be explained in detail using comments enclosed in ”(*” and ”*)”.
- The explanation for each step should be clear and concise, avoiding any unnecessary or apologetic language.
- You are strongly encouraged to create useful and reusable lemmas to solve the problem.
- The lemmas should be as general as possible (generalizable), and be able to cover a large step in proofs (non-trivial). Please ensure that your proof is
well-organized and easy to follow, with each step building upon the previous one.
Here are some useful skills for reference:
Useful skills 1:
lemma square_diff_identity:
    fixes x y z :: real
    shows "(x - y)ˆ2 + (y - z)ˆ2 + (z - x)ˆ2 = 2 * (xˆ2 + yˆ2 + zˆ2 - x * y - y * z - z * x)"
proof -
    have "(x - y)ˆ2 + (y - z)ˆ2 + (z - x)ˆ2 = (xˆ2 - 2 * x * y + yˆ2) + (yˆ2 - 2 * y * z + zˆ2) + (zˆ2 - 2 * z * x + xˆ2)"
      by (simp add: power2_diff)
    also have "... = 2 * (xˆ2 + yˆ2 + zˆ2 - x * y - y * z - z * x)"
      by (simp add: algebra_simps)
    finally show ?thesis by auto
qed

[5 more useful skills...]

Statement: Show that for positive integer n, 2 divides 4n .
Informal Proof:
Step 1: Since n is positive, we can find a natural number m where m + 1 = n. Then we can show that 2 divides 4m+1
Formal statement:
theorem numbertheory_2dvd4expn:
  fixes n :: nat
  assumes h0 : "n \<noteq> 0"
  shows "(2::nat) dvd 4ˆn"
Formal proof:
theory Scratch
  imports Complex_Main
begin
theorem numbertheory_2dvd4expn:
  fixes n :: nat
  assumes h0 : "n \<noteq> 0"
  shows "(2::nat) dvd 4ˆn"
proof -
  obtain m::nat where c0: "m+1=n"
     sledgehammer
  have "(2::nat) dvd 4ˆ(m+1)" sledgehammer
  then show ?thesis unfolding c0 sledgehammer
qed
end
[1 more formalization example...]

Statement: What is the least possible value of (xy − 1)2 + (x + y)2 for real numbers x and y? Show that it is 1.
Informal proof:
Step 1: Expand the expression (xy − 1)2 + (x + y)2 to obtain x2 + 2xy + y 2 + x2 y 2 − 2xy + 1.
Step 2: Simplify the expression derived in Step 1 to obtain x2 + y 2 + x2 y 2 + 1.
Step 3: Apply the Trivial Inequality, which states that all squares are nonnegative, to argue that the minimum value of the expression is 1.
Step 4: Show that the minimum value of 1 can be achieved when x = y = 0.
Formal statement:
theorem amc12a_2021_p7:
  fixes x y ::real
  shows "1 \<le> ((x * y) - 1)ˆ2 + (x + y)ˆ2"


Output:
Formal proof:
theory Scratch
  imports Complex_Main
begin
lemma am_gm:
  fixes x y :: real
  shows "xˆ2 + yˆ2 \<ge> 2 * x * y"
proof -
  have "(x - y)ˆ2 \<ge> 0"
    by simp
  then have "xˆ2 - 2 * x * y + yˆ2 \<ge> 0"
    by (simp add: algebra_simps power2_diff)
  then have "xˆ2 + yˆ2 \<ge> 2 * x * y"
    by simp
  then show ?thesis
    by simp
qed
theorem amc12a_2021_p7:
  fixes x y ::real
  shows "1 \<le> ((x * y) - 1)ˆ2 + (x + y)ˆ2"
  apply (auto simp:algebra_simps power2_eq_square)
  by (metis am_gm add.commute add.left_commute add_mono_thms_linordered_semiring(1) add_pos_nonneg less_add_same_cancel1
         power2_sum power_mono zero_le_power2)
end




                                        Figure 6: Prompt example for formalization.
                                                            21
Input:
System message: As a mathematician familiar with Isabelle, your task is to provide a formal proof in response to a given formal statement.
Your proof should be structured and clearly written, meeting the following criteria:
- It can be verified by Isabelle.
- Please ensure that your proof is well-organized and easy to follow, with each step building upon the previous one.
Formal statement:
lemma power_eq_imp_eq:
    fixes a::real
    assumes "a>0" "a\<noteq>1" "aˆm = aˆn"
    shows "m = n"
Formal proof:
theory Scratch
    imports Complex_Main
begin
lemma power_eq_imp_eq:
    fixes a::real
    assumes "a>0" "a\<noteq>1" "aˆm = aˆn"
    shows "m = n"
proof -
    have "aˆ(m-n) = 1"
      using assms(3) assms(2) by (metis assms(1) diff_is_0_eq diff_self_eq_0 le_numeral_extra(3) less_imp_diff_less
               linorder_le_less_linear nat_int_comparison(2) nle_le one_le_power order_le_less order_less_irrefl order_refl
               power_0 power_0_left power_decreasing_iff power_eq_0_iff power_inject_exp real_root_ge_1_iff
               real_root_pos_unique real_root_power zero_le_power)
    hence "m-n=0"
      by (smt (verit) assms(1) assms(2) assms(3) cancel_comm_monoid_add_class.diff_cancel diff_is_0_eq’ power_decreasing_iff
                power_inject_exp verit_comp_simplify1(3))
    thus "m = n"
      by (smt (verit) assms(1) assms(2) assms(3) less_numeral_extra(3) nat_neq_iff power_inject_exp
               power_strict_decreasing_iff zero_less_diff)
qed
end
[3 more request solving examples...]

Formal statement:
lemma exponent_properties:
  fixes a b :: real
  assumes "0 < a \<and> 0 < b"
  shows "aˆn * aˆm = aˆ(n + m) \<and> (aˆn)ˆm = aˆ(n * m)"


Output:
Formal proof:
theory Scratch
  imports Complex_Main
begin
lemma exponent_properties:
  fixes a b :: real
  assumes "0 < a \<and> 0 < b"
  shows "aˆn * aˆm = aˆ(n + m) \<and> (aˆn)ˆm = aˆ(n * m)"
proof
  show "aˆn * aˆm = aˆ(n + m)"
    by (simp add: assms(1) power_add)
next
  show "(aˆn)ˆm = aˆ(n * m)"
    by (simp add: assms(1) power_mult)
qed
end




                                  Figure 7: Prompt example for solving request.




                                                                   22
Input:
System Message: As an expert mathematician who is proficient in Isabelle theorem proving, your task is to modify the given lemma, theo-
rem, function, or definition given in the code to aid in solving one or more of the problems provided. You should accomplish this by [evolve description].
Here are some reference problems:
Problem 1:
theorem mathd_algebra_131:
  fixes a b :: real
    and f :: "real \<Rightarrow> real"
  assumes h0 : "\<And>x. f x = 2 * xˆ2 - 7 * x + 2"
    and h1 : "f a = 0"
    and h2 : "f b = 0"
    and h3 : "a \<noteq> b"
  shows "1 / (a-1) + 1 / (b-1) = -1"
[3 more reference problems...]

Skill to evolve:
theory Scratch
  imports Complex_Main
begin
lemma mathd_numbertheory_001:
  fixes n :: nat
  shows "n mod 3 = 0 \<or> n mod 3 = 1 \<or> n mod 3 = 2"
by auto
end

Evolved skill:
theory Scratch
  imports Complex_Main
begin
lemma remainder_modulo:
  fixes n d :: nat
  assumes "d > 0"
  shows "n mod d \<in> {0..d-1}"
proof -
  have "n mod d < d" by (rule mod_less_divisor[OF assms(1)])
  moreover have "n mod d \<ge> 0" by simp
  ultimately show ?thesis by auto
qed
end

[2 more directional evolve examples]

Skill to evolve:
theory Scratch
  imports Complex_Main
begin
lemma divide_cross_mul:
  fixes a b c d :: real
  assumes "b \<noteq> 0"
     and "d \<noteq> 0"
     and "a / b = c / d"
  shows "a * d = b * c"
  using assms by (auto simp: field_simps)
end



Output:
Evolved skill:
theory Scratch
  imports Complex_Main
begin
lemma divide_cross_mul_generalized:
  fixes a b c d x y :: real
  assumes "b \<noteq> 0"
    and "d \<noteq> 0"
    and "a / b = c / d"
    and "a = x * b"
    and "c = y * d"
  shows "x * d = y * b"
  using assms by (auto simp: field_simps)
end




                                   Figure 8: Prompt examples for directional evolve




                                                                          23
