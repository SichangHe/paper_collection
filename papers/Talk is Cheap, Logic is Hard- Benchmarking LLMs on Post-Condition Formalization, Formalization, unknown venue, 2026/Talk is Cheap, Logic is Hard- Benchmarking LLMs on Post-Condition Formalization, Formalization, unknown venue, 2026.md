                                         Talk is Cheap, Logic is Hard: Benchmarking LLMs on Post-Condition
                                         Formalization
                                         I.S.W.B. Prasetyaa , Fitsum Kifetewb and Davide Prandib
                                         a Utrecht University, Utrecht, the Netherlands
                                         b Fondazione Bruno Kessler, Trento, Italy



                                         ARTICLE INFO                                         ABSTRACT
                                         Keywords:                                            Context: Formal specifications, such as pre- and post-conditions provide a solid basis for performing
                                         LLM for formal specifications                        thorough program verification and validation. However, developers rarely provide such formal
                                         LLM for pre/post-conditions                          specifications, hence if AI could help in constructing them, it would make formal verification possible
                                         LLM for software testing                             or at least make automated testing much more effective. Objective: This paper presents a study on
arXiv:2603.17193v1 [cs.SE] 17 Mar 2026




                                                                                              the ability of Large Language Models (LLMs) in generating formal full pre- and post-conditions of a
                                                                                              program, given its informal natural language description. Method: Twenty-four state-of-the-art LLMs
                                                                                              were evaluated on a freshly prepared dataset of 40 tasks. The paper investigates specifications of
                                                                                              varying difficulty and discusses a set of more refined performance metrics in addition the general
                                                                                              accept@1 performance. It also investigates the impact of using automatically generated tests for
                                                                                              validation of the solutions proposed by LLMs. Results: The results of the experiment reveal that, in
                                                                                              general LLMs can produce valid pre- and post-conditions based on natural language descriptions of
                                                                                              programs. Incorrect solutions from proprietary models are also often near correct. A closer inspection
                                                                                              shows that open-source models tend to result in a higher proportion of erroneous results while
                                                                                              proprietary models tend to have slightly higher false negative rates. Interestingly, the results also show
                                                                                              that augmenting the manually prepared dataset with automatically generated tests leads to the exposure
                                                                                              of wrong solutions, which would have otherwise been accepted as correct. Conclusion: In general,
                                                                                              LLMs perform better in formalizing pre-conditions than on post-conditions and proprietary models
                                                                                              perform better than open ones. However, none of the LLMs were able to correctly formalize all the
                                                                                              tasks in our benchmark. Overall, the effectiveness and reliability of LLMs in formalizing pre- and
                                                                                              post-conditions could be greatly improved by using a good test suite that checks the correctness of the
                                                                                              LLM generated formalizations.



                                         1. Introduction                                                                 developers are not trained in writing them. Arguably though,
                                                                                                                         the more likely reason is that companies consider the effort
                                             Many Large Language Models (LLMs) are able to gener-                        to be too much, so developers are not required or encouraged
                                         ate new content (Feuerriegel et al., 2024) beyond their orig-                   to write them. Hence, if LLMs can produce them, or at least
                                         inal training data (generative AI). They have amazed many
                                                                                                                         aid developers in producing them, it might lower the cost and
                                         of us in their ability to engage in conversations and produce                   make the gain attractive.
                                         coherent answers when asked questions. Many LLMs have                               Let us first argue that a formal specification does not nec-
                                         also been trained in doing code completion tasks. The skill                     essarily have to be expressed in (complex) math formulas. It
                                         has been employed in practice to aid programmers writing                        however needs to be interpretable by a computer, so that it
                                         code, e.g. IDEs like PyCharm and Raider have integrated
                                                                                                                         can be used to validate a program. A ’formal specification’
                                         LLM Copilots. This leads to the hypothesis that perhaps,
                                                                                                                         can thus be just a Python function, for example, with which
                                         with the right prompting, LLMs can also be used to aid other                    we can check if the output of the associated program is
                                         programmimg-related tasks. For example the use of LLMs                          correct. From this perspective, constructing specifications in
                                         to write tests (Yang et al., 2024), inferring test oracles (Mah-                the form of pre- and post-conditions, also known as contract
                                         mud Khandaker et al., 2025), and aid debugging (Xia and                         (Meyer, 1992), can be phrased as a problem of constructing
                                         Zhang, 2023) were recently studied. Another interesting
                                                                                                                         boolean functions 𝑝𝑟𝑒 and 𝑝𝑜𝑠𝑡 given a natural language
                                         application of LLMs is to generate the formal specification
                                                                                                                         description. Many LLMs are trained in such a programming
                                         of a program from its natural language description.                             task in general, i.e., producing a program from a natural
                                             The presence of a formal specification would enable rig-                    language description. So, in theory producing pre- and post-
                                         orous checking of the correctness of a program, e.g. through                    conditions should not be much different. However, there is
                                         symbolic techniques or through extensive automated testing.                     a twist. Consider, for example the following description of a
                                         Note that without specifications such techniques can only
                                                                                                                         program:
                                         be used to check for general errors (such as crashing) or
                                         regression errors. Unfortunately in practice developers rarely                     The program 𝑠𝑜𝑟𝑡𝑥(𝑠) takes a list with no duplicates,
                                         provide formal specifications. A possible explanation is that                      and returns an increasingly sorted copy of 𝑠.
                                                 s.w.b.prasetya@uu.nl (I.S.W.B. Prasetya); kifetew@fbk.eu (F.
                                         Kifetew); prandi@fbk.eu (D. Prandi)                                             While the text describes the program 𝑠𝑜𝑟𝑡𝑥, it does not
                                               ORCID (s): 0000-0002-3421-4635 (I.S.W.B. Prasetya);                       directly describes boolean functions 𝑝𝑟𝑒 and 𝑝𝑜𝑠𝑡. So, it is
                                         0000-0003-1860-8666 (F. Kifetew); 0000-0001-9885-6074 (D. Prandi)


                                         ThisisaPreprint                                                                                                                               Page 1 of 18
                                                  Talk is Cheap, Logic is Hard

not given that the LLM’s programming skill would automat-           is still valuable, e.g. developers can manually fix them
ically transfer to extracting and formalizing pre- and post-        based on information from failing test cases. This paper
conditions.                                                         furthermore looks into the performance of LLMs across
    We will distinguish between full and partial or incom-          pre-/post-conditions of different difficulties. Finally, the
plete pre-/post-conditions. A full post-condition is a post-        paper also discusses several selected cases involving
condition that fully captures the correctness of the intended       language subtleties and the insight learned from them.
functionality of the program it specifies. Alternatively, one
can come up with a post-condition that only partially cap-        • Our study assesses a comprehensive set of state-of-the-
tures the intent. For example, a post-condition that only           art proprietary and open LLMs, offering a broader insight
asserts that the output of 𝑠𝑜𝑟𝑡𝑥(𝑠) should be of the same           into their ability in formalizing contracts.
length as 𝑠 is partial. Analogously, a partial pre-condition
only partially captures the intended constraint on the pro-
                                                                  Paper structure. We start by presenting relevant related
gram’s inputs. Partial pre- and post-conditions are easier to
                                                                  work in Section 2. Section 3 defines pre- and post-conditions,
write, as we do not need to be complete in capturing a pro-
                                                                  gives examples of their formalization, and introduces the
gram’s intent. Unfortunately, a partial post-condition is also
                                                                  concept of specification difficulty. Section 4 describes our
weaker in detecting errors. For instance the aforementioned
                                                                  benchmarking methodology. Section 5 states the research
example of a partial post-condition for 𝑠𝑜𝑟𝑡𝑥 will accept
                                                                  questions that we investigate and describes the design of
an implementation that sorts the returned list decreasingly
                                                                  the experiment carried out to address them. Section 6
(wrong) instead of increasingly. Analogously, using a partial
                                                                  presents the results, and Section 7 discusses several selected
pre-condition would trigger spurious bug reports during
                                                                  cases. Treats to validity are discussed in Section 8. Finally,
testing or verification. That is, the post-condition reports
                                                                  Section 9 concludes the paper and mentions some future
a violation/error, but this occurs because the program was
                                                                  work.
called with an input that does not satisfy its intended pre-
condition. The reported error is therefore not an actual error.
    Full pre- and post-conditions are therefore preferred. On
the other hand they are more challenging to formulate, hence      2. Related Work
if LLMs can help it would considerably reduce the effort               LLMs’ ability to produce specifications, in particular
required in formalizing contracts. In this paper we will focus    post-conditions, has been studied in a number of recent
on the generation of full pre- and post-conditions. More          papers. He et al. (2024) studied the generation of partial post-
specifically, we investigate the following research questions:    conditions of various types (e.g. null-check 𝑟𝑒𝑡𝑣𝑎𝑙≠𝖭𝗈𝗇𝖾 or
                                                                  numerical range such as 0≤𝑟𝑒𝑡𝑣𝑎𝑙<𝑛) given a program’s
• RQ1: how do LLMs perform in generating full formal
                                                                  natural language description, for Python programs in the
  pre- and post-conditions? How good are open source
                                                                  EvalPlus dataset (Liu et al., 2023b) (more specifically, its
  LLMs compared to propriety ones?
                                                                  HumanEval subset). Strong performance was shown, while
• RQ2: how does pre-/post-condition difficulty impact LLMs’       using only small LLMs (Gemma-7b and Mistral-7B, with
  performance?                                                    about 7 billion parameters, as opposed to GPT 3.5’s 175
                                                                  billion) where 99% of the generated post-conditions were
We present the benchmarking experiment we performed               validated to be sound. But, being partial they are of course
using a newly crafted dataset and involving a variety of state-   incomplete (not able to detect all bugs). Extraction of full
of-the-art LLMs to answer these questions.                        post-conditions was attempted by Endres et al. (2024).
                                                                  Larger LLMs were used (GPT3.5, GPT4, and Starchat).
Contribution. This paper offers a study on the ability of         Despite this, for about 39% of the programs from the
state-of-the-art LLMs to generate formal pre- and post-           HumanEval subset, the LLMs could not construct a correct
conditions of a program, given the program’s natural lan-         post-condition. Endres et al. prompted the LLMs to produce
guage specification/description. The study offers the follow-     a post-condition in the form of a single 𝖺𝗌𝗌𝖾𝗋𝗍, potentially
ing advancement with respect to previous studies.                 restricting the LLMs.
                                                                       Since LLMs are also trained to comprehend program
• Previous studies (Endres et al., 2024; He et al., 2024; Ma      code, one may contemplate to ask them to extract pre- and
  et al., 2024) focused on the generation of partial post-        post-conditions directly from the code, or fragments of it.
  conditions, which are weaker in detecting faults. This          This was studied by Wen et al. (2024) with their AutoSpec
  paper offers insight into LLMs’s ability in generating full     tool which uses GPT-3.5 to generate assertions, including
  pre- and post-conditions.                                       post-conditions, for C programs. Symbolic verification is
• Aforementioned previous studies focused on the accept@1         used to remove candidate assertions which are inconsistent
  metric, similar to pass@1 metric (Chen et al., 2021).           with the program. Ma et al. (2024) proposed SpecGen for
  This metric only considers correct solutions. Our paper         generating assertions for Java programs. It also uses GPT-
  offers a set of more refined metrics, e.g. indicating if        3.5 and a symbolic verifier to validate candidates proposed
  a solution is almost correct. Arguably, such a solution         by the LLM. But SpecGen also includes an iterative part. If a

ThisisaPreprint                                                                                                     Page 2 of 18
                                                  Talk is Cheap, Logic is Hard

proposed assertion fails, a prompt is generated for the LLM       in the program description. The two approaches are comple-
to fix the proposal, along with some feedback distilled from      mentary, each with strength and weakness. Combining them
the verification report. SpecGen also has a loop to evolve        seems to be an area worth exploring for future work.
candidate specifications through direct mutations (without
using the LLM). Relatively high success rates were reported
(for about 72% of the programs in their dataset, sound post-      3. Pre- and Post-conditions
conditions were extracted). The approach may however pro-             A popular way to formally specify the functionality of
duce partial post-conditions; the study itself does not include   a program is by using pre- and post-conditions. The theory
an assessment on the completeness of the obtained post-           was proposed by Hoare (1969). The idea was later brought
conditions. One should also keep in mind that specifications      into software development by Meyer (1992), who then called
extracted from the code may inherit bugs already in the           them program contract. Consider a program 𝐹 (𝑥) that takes
code. Faria et al. (2026) investigated Claude 4.5 and GPT5.2      a single parameter 𝑥 as input and returns a value as output.
for generating pre-/post-conditions and loop invariants for       𝐹 can be specified using a triple {𝑃 } 𝐹 (𝑥) {𝑄}. The
Dafny (Leino, 2010) programs. Given a Dafny program,              triple is also called Hoare triple (Hoare, 1969). 𝑃 is called
an LLM is asked to add missing specifications, such as            a pre-condition: a predicate over the 𝐹 ’s input, specifying
pre/post conditions and loop invariants. The Dafny verifier       which input values are valid/allowed for invoking 𝐹 . 𝑄
is used for validation. Their approach adopts an iterative        is called a post-condition; a predicate over 𝐹 ’s input and
repair prompting where a repair prompt is sent to the LLM         output, specifying what 𝐹 computes, if it is invoked with an
if a proposed specification failed the validation. The repair     input satisfying 𝑃 . For example, the triple below specifies
is reported to greatly improve the success rate in obtaining      a program that computes the maximum element of a non-
sound specifications. The work presented in this paper as-        empty list of integers.
sesses LLMs’ potential in producing formal specifications
from natural language descriptions, differently from Faria                𝑃 ∶                   { |𝑎| > 0 }
et al. (2026) where the LLM works on a Dafny program.                                      𝖿 𝗂𝗇𝖽𝖬𝖺𝗑(𝑎∶𝑙𝑖𝑠𝑡[𝑖𝑛𝑡])                  (1)
     In AutoSpec and SpecGen, GPT-3.5 is asked to produce                 𝑄∶      { 𝗋𝖾𝗍𝗏𝖺𝗅 ∈ 𝑎 ∧ (∀𝑥 ∈ 𝑎 ∙ 𝗋𝖾𝗍𝗏𝖺𝗅 ≥ 𝑥) }
specifications in respectively ACSL and JML; these are
                                                                  Various specification languages support pre- and post-conditions
dedicated specification languages. Many coding LLMs were
                                                                  e.g. OCL, JML, Z, and the contract language of Eiffel. If
trained with Python and Java, but it is unknown whether
                                                                  present, pre- and post-conditions are very valuable artifacts.
they were also trained with JML or ACSL. Though much
                                                                  Having a post-condition allows a program to be symboli-
of JML’s syntax is similar to Java, it is still a language of
                                                                  cally verified. Alternatively, it allows automated testing to
its own. So if GPT-3.5 was not trained with JML, and yet
                                                                  be applied, serving as a general test-oracle to check the
able to produce JML specifications, that would show that
                                                                  program’s output for any input instance that an automated
LLMs are also capable of cross-lingual generalization. Ni-
                                                                  testing algorithm produces.
had Zitouni et al. (2024) attempted to use GPT-4o to extract
Symboleo specifications from natural language descriptions        3.1. Full and partial conditions
of business contracts. Symboleo is a dedicated specification
                                                                      The concept of full and partial was mentioned before.
language. However, its structure and syntax are different
                                                                  A post-condition 𝑄 of a program 𝐹 (𝑥) is full if it fully
from Java or JML. Unfortunately, in this experiment GPT-4o
                                                                  captures 𝐹 ’s intent. To put it differently, 𝑄 is full if it accepts
struggled in producing correct Symboleo fragments.
                                                                  any output of a correct implementation of 𝐹 , and rejects
     Further in the past, research in formal specifications
                                                                  any wrong output of any incorrect implementation of 𝐹 . A
generation mainly focused on techniques to infer them from
                                                                  partial post-condition 𝑄′ also accepts all correct outputs of
execution traces (dynamic inference). Tools like Daikon
                                                                  𝐹 , but it also accepts some outputs that are actually wrong.
(Ernst et al., 2007) and AutoInfer (Wei et al., 2011) can
                                                                  So, a partial post-condition is strictly weaker than a full one
derive pre- and post-conditions. Only formulas that are
                                                                  (𝑄′ ≢ 𝑄 ∧ 𝑄′ ⇐ 𝑄). A pre-condition is full if it approves
instances of pre-defined formula-patterns can be derived.
                                                                  any input that a correct 𝐹 should be able to accept, and
Other types of formal specifications can be derived as well,
                                                                  rejects inputs that a correct 𝐹 are not expected to accept. A
e.g. temporal specifications (Beschastnikh et al., 2011), al-
                                                                  partial pre-condition approves all correct inputs, but it also
gebraic specifications (Elyasov et al., 2013), or even a Finite
                                                                  approves some inputs that should actually be rejected.
State Machine (FSM) model (Mariani and Pastore, 2008).
                                                                      For example, the pre- and post-conditions in the speci-
Dynamic inference is neither sound nor complete, as we can
                                                                  fication of 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑 in (1) are full. Below is an alternative
only collect finite number of traces. Also, if the program
                                                                  specification, but its post-condition is partial:
has a bug, the bug may manifest in the traces, and thus also
in specifications derived. LLM-based approaches are also                 { |𝑎| > 0 } 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑(𝑎∶𝑙𝑖𝑠𝑡[𝑖𝑛𝑡]) { 𝗋𝖾𝗍𝗏𝖺𝗅 ∈ 𝑎 }         (2)
not guaranteed to be sound and complete, due to LLMs’                      ⏟⏟⏟                               ⏟⏞⏞⏟⏞⏞⏟
probabilistic nature as well as incompleteness and ambiguity                  𝑃                                       𝑄′

                                                                  The post-condition 𝑄′ is simpler than its full counterpart
                                                                  in (1). But if an implementation of 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑 returns the

ThisisaPreprint                                                                                                        Page 3 of 18
                                                    Talk is Cheap, Logic is Hard

smallest element, rather than the greatest element, this bug          this is expressible with a nested list or set comprehension:
will unfortunately be left undetected by this 𝑄′ . That is why        𝖺𝗅𝗅(𝑥>𝑦 𝐟 𝐨𝐫 𝑥 𝐢𝐧 𝑎 𝐟 𝐨𝐫 𝑦 𝐢𝐧 𝑏).
using a partial post-condition, or a partial pre-condition, for
testing is not preferred.                                           • Category 𝖭𝖰: the post condition uses uses one or more
                                                                      explicit loops or recursions. A loop is defined as explicit
3.2. Interpretable specification                                      if it is a 𝗐𝗁𝗂𝗅𝖾-loop or is a 𝖿 𝗈𝗋-loop but is not a compre-
    To be used for verification or testing, a formal speci-           hension. An example of this category is given below.
fication has to be interpretable by a computer. We do not
                                                                        The categories above are disjoint and complete. That is,
necessarily need to use a dedicated specification language
                                                                    a given formula always belongs to one of the categories, and
such as OCL or Z to achieve interpretability. We can also
                                                                    only to one of them.
write pre- and post-conditions as expressions or code in the
                                                                        Not all post-conditions are expressible with traditional ∀
programming language of the specified program itself. Pre-
                                                                    and ∃ Predicate Logic quantifiers, which is why we have the
and post-conditions are predicates, so they can be written
                                                                    𝖭𝖰 class. For example, imagine a program 𝖼𝗇𝗍𝖲𝖻𝗒𝖲(𝑠) that
as boolean functions. For example 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑’s pre- and post-
                                                                    takes a string 𝑠 containing properly nested and possibly side-
conditions in (1) can be written as the following functions in
                                                                    by-side brackets as input, and count how many side-by-side
Python:
                                                                    groups 𝑠 contains. The pre-condition essentially requires 𝑠
      𝐝𝐞𝐟 𝗉𝗋𝖾𝖥𝗂𝗇𝖽𝖬𝖺𝗑(𝑎) ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝗅𝖾𝗇(𝑎) > 0                         to satisfy the Context Free Grammar:
      𝐝𝐞𝐟 𝗉𝗈𝗌𝗍𝖥𝗂𝗇𝖽𝖬𝖺𝗑(𝑟𝑒𝑡𝑣𝑎𝑙, 𝑎) ∶                            (3)
          𝐫𝐞𝐭𝐮𝐫𝐧 𝑟𝑒𝑡𝑣𝑎𝑙 𝗂𝗇 𝑎 𝖺𝗇𝖽 𝖺𝗅𝗅(𝑟𝑒𝑡𝑣𝑎𝑙 ≥ 𝑥 𝐟𝐨𝐫 𝑥 𝐢𝐧 𝑎)               𝑆 → εε | ε(ε 𝑆 ε)ε 𝑆                                  (5)

The paramater 𝑟𝑒𝑡𝑣𝑎𝑙 in the post-condition represents the           While simple, this is not expressible in Predicate Logic due
return value (output) of 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑.                                  to the lack of recursion. To express this pre-condition in
    For verification or testing we can formulate the original       Python we can for example write this:
Hoare triple as a function, e.g. as shown below, which we
then use as the verification or testing entry point.                 𝐝𝐞𝐟 𝗉𝗋𝖾𝖢𝗇𝗍𝖲𝖻𝗒𝖲(𝑠) ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝖲(𝑠) == εε
                                                                     𝐝𝐞𝐟 𝖲(𝑠) ∶ # for recognizing 𝑆
       𝐝𝐞𝐟 𝗏𝖾𝗋𝗂𝖿 𝗒𝖥𝗂𝗇𝖽𝖬𝖺𝗑(𝑎) ∶
                                                                         𝐢𝐟    𝑠 == εε 𝐨𝐫 𝑠 == 𝖭𝗈𝗇𝖾 ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝑠
         𝐢𝐟 𝗉𝗋𝖾𝖿 𝗂𝗇𝖽𝖬𝖺𝗑(𝑎) ∶
                                                              (4)        𝐞𝐥𝐬𝐞                            ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝖲(𝖼𝗅𝗈𝗌𝖾(𝖲(𝗈𝗉𝖾𝗇(𝑠))))
            𝑟𝑒𝑡𝑣𝑎𝑙 = 𝖿𝗂𝗇𝖽𝖬𝖺𝗑(𝑎)
                                                                     𝐝𝐞𝐟 𝗈𝗉𝖾𝗇(𝑠) ∶ # for recognizing "("
            𝐚𝐬𝐬𝐞𝐫𝐭 𝗉𝗈𝗌𝗍𝖿𝗂𝗇𝖽𝖬𝖺𝗑(𝑟𝑒𝑡𝑣𝑎𝑙, 𝑎)
                                                                         𝐢𝐟    𝑠 == εε 𝐨𝐫 𝑠 == 𝖭𝗈𝗇𝖾 ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝖭𝗈𝗇𝖾
                                                                         𝐞𝐥𝐢𝐟 𝑠[0] == ε(ε                ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝑠[1∶]
3.3. Specification difficulty                                            𝐞𝐥𝐬𝐞                            ∶ 𝐫𝐞𝐭𝐮𝐫𝐧 𝖭𝗈𝗇𝖾
     The pre-condition of 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑 is just a simple formula          𝖽𝖾𝖿 𝖼𝗅𝗈𝗌𝖾(𝑠) ∶ # analogous to 𝗈𝗉𝖾𝗇, for recognizing ")"
|𝑎|>0. Such a formula should be easy for a programmer
to figure out. However, formulas that involve quantifiers,
such as the post-condition of 𝖿 𝗂𝗇𝖽𝖬𝖺𝗑, are more challenging            Notice that the recursion in the code of 𝖲 reflects the re-
to write for humans (Prasetya et al., 2020; Bravo, 2023).           cursion in the grammar rule in (5). The above post-condition
Formulas involving nested quantifiers are even more chal-           is of the difficulty class 𝖭𝖰.
lenging (Bravo, 2023). We therefore would want to know                  We can also look at the ’structural’ difficulty of a pre and
whether LLMs can help us in formalizing the more difficult          post-condition from the perspective of the code complexity
specifications. We define the following classes of semantical       of functions that formulate them, expressed as McCabe
difficulty for post-conditions, ordered increasingly in their       (cyclomatic) complexity (CC) (McCabe, 1976). For example
difficulty. Analogously, we have the same classification for        the above pre-condition for 𝖼𝗇𝗍𝖲𝖻𝗒𝖲 has a CC of 11. So, in
pre-conditions.                                                     addition to being semantically difficult (classs 𝖭𝖰), the pre-
                                                                    condition is also quite complex from the code complexity
• Category 𝖲: the post-condition is a simple expression. It         perspective.
  does not contain any quantified formula. Example: 𝑥>0 ∧
  𝑙𝑒𝑛(𝑎)>0.
                                                                    4. Benchmarking Methodology
• Category 𝖰: the post-condition has one or more quantified             Here we describe our approach for benchmarking LLMs
  formulas, but they are not nested. Also, no explicit loop         with respect to the task of generating valid pre- and post-
  nor recursion is used. A list or set comprehension is             conditions. For simplicity we talk about post-conditions, but
  treated as a quantified expression. Example: (∀𝑥 ∶ 𝑥 ∈            the same considerations apply to pre-conditions. Peculiari-
  𝑎 ∶ 𝑥>0). In Python this is expressible with a list or set        ties in validation steps are explained later in Section 4.2.
  comprehension: 𝖺𝗅𝗅(𝑥>0 𝐟 𝐨𝐫 𝑥 𝐢𝐧 𝑎).
• Category 𝖰𝖰: the post-condition has at least one nested           4.1. Prompting
  quantified formula. No explicit loop nor recursion is used.          To obtain a formal post-condition from an LLM, we
  Example: (∀𝑥 ∶ 𝑥 ∈ 𝑎 ∶ (∀𝑦 ∶ 𝑦 ∈ 𝑏 ∶ 𝑥>𝑦)). In Python             prompt the LLM as shown in Figure 1. The wordings are

ThisisaPreprint                                                                                                       Page 4 of 18
                                                           Talk is Cheap, Logic is Hard

formulated by considering how developers could reasonably                     Consider a program P .
be expected to formulate them, and what information could                     Description of what the program does .
reasonably be included in the prompt. To avoid bias, we do
not engineer the prompt towards certain LLMs. The program                     Examples:
code is not included in the prompt as in this study we focus                  𝑃 (inputs) = ouput
on inference from the program’s description.                                  𝑃 (inputs) = ouput
    The prompt contains a natural language description of                     ...
the program and few examples of input and output. This is
followed by instructions:                                                     INSTRUCTION:
                                                                              (1) Extract the post-condition of 𝑃 (in English).
1. The LLM is first asked to extract the post-condition of                    (2) Then, code this post-condition as a Python function
   the program in English. The rationale is that a program’s                  with the header shown below, where the parameter r
                                                                              represents 𝑃 ’s return value.
   description, as exemplified by the description of the pro-
                                                                              Do not explain. If a helper function is needed, define it
   gram 𝑠𝑜𝑟𝑡𝑥 shown in Section 1, describes the program;
                                                                              as an inner function. Import packages, if needed, locally
   but in most cases it is not structured into sections explic-               within the function.
   itly called pre- and post-conditions. So we ask the LLM
   to first explicitly formulate the post-condition.                          def check_post_𝑃 (𝑟∶𝑡𝑦𝑝𝑒, 𝑝𝑎𝑟1 ∶𝑡𝑦𝑝𝑒, 𝑝𝑎𝑟2 ∶𝑡𝑦𝑝𝑒, ...) -> bool :

2. Then, the second instruction asks the LLM to code the
   extracted post-condition as a Python (boolean) function                   Figure 1: The prompt to get a post-condition from an LLM.
   of a specific signature.                                                  𝑃 is to be replaced with the name of the program whose post-
                                                                             condition we want to extract. The red-part is to be filled with
Notice that we instruct the LLM to express the post-condition
                                                                             a textual, natural language, description of 𝑃 ’s functionality.
as a function, different from other work that instructs the                  Several examples of inputs-outputs of 𝑃 are also included in
LLM to write assertions (Endres et al., 2024; He et al., 2024),              the prompt, as part of 𝑃 ’s description.
for example:
       "Write a symbolic postcondition for 𝑃 consist-
       ing of exactly one assert statement" (Endres                          are correct if they are semantically equivalent to the pro-
       et al., 2024).                                                        vided solution 𝑝𝑟𝑒𝐹 and 𝑝𝑜𝑠𝑡𝐹 . This is validated through
                                                                             testing. Validation through formal verification is not a re-
This might be constraining the LLM. For human program-                       alistic option as many of the conditions are complex and
mers, it is not always convenient, or even possible, to code a               fall beyond the range of automated theorem provers, as in
full post-condition in a single 𝖺𝗌𝗌𝖾𝗋𝗍. Since LLMs are trained               the case of the example program 𝖼𝗇𝗍𝖲𝖻𝗒𝖲 shown in Section
from human data, this may influence the resulting LLMs’                      3.3. Also, note that we do not check for mere syntactical
behavior. In contrast, we phrase the problem as a task of                    similarities, as there are infinitely many ways the same
writing a function, with the rationale that this would relate                condition can formulated.
better to LLMs’ general programming training/skill.                               Test suites 𝑇𝑝𝑟𝑒 , 𝑇𝑝𝑜𝑠𝑡 are provided by the dataset (Sec-
     To obtain multiple answers from the LLM, we send the                    tion 5.2). Each test case 𝑥 ∈ 𝑇𝑝𝑟𝑒 represents an input for 𝐹 .
prompt multiple times, and collect the answer of each. The                   Each test case in 𝑇𝑝𝑜𝑠𝑡 is a pair (𝑜, 𝑥) where 𝑥 represents an
same prompt is used across all subject LLMs (Section 5.3)1                   input for 𝐹 and 𝑜 a value that could be 𝐹 ’s output.
. Despite the instruction that says: "Do not explain", an LLM
can still insist to be helpful by giving explaining text along               • The LLM proposed pre-condition 𝑝𝑟𝑒′ is accepted as a
with the code. While such an answer is not what the prompt                     correct pre-condition for 𝐹 if for all 𝑥 ∈ 𝑇𝑝𝑟𝑒 , 𝑝𝑟𝑒′ (𝑥) =
asks, a pre-processing step is still applied to try to locate                  𝑝𝑟𝑒𝐹 (𝑥).
the code in the text and extract it. It may also happen that                 • The LLM proposed post-condition 𝑝𝑜𝑠𝑡′ is accepted as
the generated Python code is not properly indented (e.g.                       a correct post-condition for 𝐹 if for all (𝑜, 𝑥) ∈ 𝑇𝑝𝑜𝑠𝑡 ,
without any indentation at all), making the code syntactically                 𝑝𝑜𝑠𝑡′ (𝑜, 𝑥) = 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥).
incorrect. The pre-processor also makes an attempt to fix
the indentation. This pre-processing is uniformly applied to                     Note that 𝑥 can represent an invalid input for 𝐹 , for
every answer from any LLM.                                                   which 𝑝𝑟𝑒𝐹 (𝑥) will give a 𝑓𝑎𝑙𝑠𝑒 to reject it. Similarly, for
                                                                             a valid input 𝑥, 𝑜 could represent a wrong output by 𝐹 for
4.2. Solution validation                                                     which 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) will give a 𝑓𝑎𝑙𝑠𝑒 to reject this 𝑜. Such
   Suppose for a program 𝐹 (𝑥) an LLM proposes a pre-                        tests are negative tests. It is important that the test suites in
condition 𝑝𝑟𝑒′ and a post-condition 𝑝𝑜𝑠𝑡′ . These proposals                  the study include negative tests (they do) to avoid accepting
     1 Tuning the prompt per model would introduce confounding variables     proposals that are too weak. The test suites in the dataset
related to optimization resulting in a wide configuration space which goes   were manually written and achieve full branch coverage over
well beyond the scope of in this paper.                                      their corresponding programs. Still, to increase the variety
                                                                             of the tests and to maximize the likelihood of detecting

ThisisaPreprint                                                                                                                      Page 5 of 18
                                                      Talk is Cheap, Logic is Hard




Figure 2: The basic workflow for generating more positive and negative tests using Pynguin. 𝐹 (𝑥) is the program under
consideration; 𝑝𝑟𝑒𝐹 and 𝑝𝑜𝑠𝑡𝐹 are solution pre- and post-conditions. Using 𝐹 we cannot actually generate negative post-condition
tests. To do the latter, 𝐹 is replaced by a mutant (𝐹 containing a mutated code) and re-run the same workflow.



corner cases that challenge LLMs, we developed an auto-                5. Experiment Design
mated test generation pipeline that uses Pynguin (Lukasczyk
et al., 2020), the Python General Unit test generator, and                 This section presents the design of the empirical study
Poodle (Busch, accessed Sept. 2025), a tool for mutation               we performed to answer the research questions, which we
testing of Python code.                                                describe first, followed by the dataset designed for the study,
    The basic workflow without Poodle in shown in Figure               as well as the different models considered. Finally, we will
2 —we will go back to Poodle later. Given a program 𝐹 (𝑥),             describe the experiment protocol and evaluation metrics.
we first run Pynguin on 𝐹 (𝑥), to obtain test cases 𝑡1𝐹 … 𝑡𝑛𝐹 ,
                                                                       5.1. Research questions
each is an instance of 𝑥. Then:
                                                                           The principal research questions that drive the empirical
1. For each test case 𝑡𝑖𝐹 , we evaluate the solution pre-              investigation concern the performance of LLMs in produc-
   condition on the test case: 𝑝𝑟𝑒𝐹 (𝑡𝑖𝐹 ).                            ing correct full pre- and post-conditions from descriptions
                                                                       in natural language (RQ1), and the impact of the difficulty
2. If 𝑝𝑟𝑒𝐹 (𝑡𝑖𝐹 ) evaluates to 𝑓𝑎𝑙𝑠𝑒, we add 𝑡𝑖𝐹 to the set of         of the task on the performance of the LLMs (RQ2). Specifi-
   negative pre-condition tests for 𝐹 (𝑥).                             cally:
3. Otherwise, if 𝑝𝑟𝑒𝐹 (𝑡𝑖𝐹 ) evaluates to 𝑡𝑟𝑢𝑒, we classify 𝑡𝑖𝐹        1. RQ1: how do LLMs perform in generating formal full
   as a positive pre-condition test. Then, we also execute the            pre- and post-conditions? How good are open source
   program 𝐹 (𝑥) using the input 𝑡𝑖𝐹 to obtain the output 𝑜𝑖𝐹 .           LLMs compared to proprietary ones?
4. We then evaluate the solution post-condition: 𝑝𝑜𝑠𝑡𝐹 (𝑜𝑖𝐹 , 𝑡𝑖𝐹 )    2. RQ2: how do LLMs perform on pre-/post-conditions of
   and add the pair (𝑜𝑖𝐹 , 𝑡𝑖𝐹 ) to the post-condition test suite         varying levels of difficulty?
   of 𝐹 (𝑥).
                                                                          We refine RQ2 into following sub-questions based on the
      Because in step-3 above we use 𝐹 (𝑥) itself to obtain               two notions of difficulty discussed in Section 3:
𝑜𝑖𝐹 , when in step-4 we evaluate (𝑜𝑖𝐹 , 𝑡𝑖𝐹 ) using 𝑝𝑜𝑠𝑡𝐹 , it will       RQ2.1 cyclomatic complexity: how much does the cyclo-
always result in 𝑡𝑟𝑢𝑒. So, tests added in step-4 are always               matic complexity of the pre-/post-condition impact the
positive post-condition tests, and therefore with the above               performance of LLMs? RQ2.2 quantifiability: how much
scheme Pynguin cannot add negative post-condition tests.                  does the semantic difficulty level (𝖲, 𝖰, 𝖰𝖰, 𝖭𝖰) impact
To be able to do the latter, we generate mutated versions                 LLMs’ capability in formalizing contracts?
𝐹1 (𝑥), … , 𝐹𝑘 (𝑥) of the program 𝐹 (𝑥) using Poodle. For
each mutant 𝐹𝑗 (𝑥), we execute Pynguin again and repeat the            5.2. Dataset
workflow in Figure 2 to categorize the generated test cases                Previous studies (Endres et al., 2024; He et al., 2024)
into the appropriate test suites: positive and negative for both       use the HumanEval dataset (Chen et al., 2021). This dataset
pre- and post-conditions. In particular, if in step-4 evaluating       is publicly available, so it might have been included in the
𝑝𝑜𝑠𝑡𝐹 (𝑜𝑖 , 𝑡𝑖𝐹 ) gives 𝑓 𝑎𝑙𝑠𝑒 (where 𝑜𝑖 is produced by a mutant       training of the studied LLMs, which would then bias the re-
of 𝐹 ), the test (𝑜𝑖 , 𝑡𝑖𝐹 ) is thus a negative post-condition test.   sults. To mitigate this, our dataset, called HEx, consists of 40

ThisisaPreprint                                                                                                          Page 6 of 18
                                                  Talk is Cheap, Logic is Hard

tasks freshly adapted from the HumanEval dataset (Chen              Table 1
et al., 2021). The repository of HEx is unexposed and un-           Distribution of the difficulty and complexity of 𝖧𝖤𝗑 pre- and
likely to have been used for the training of an LLM. The 40         post-conditions.
tasks were selected with consideration to provide a balanced                             difficulty         cyclomatic complexity
distribution of difficulty levels for pre- and post-conditions.               𝑁     𝐒    𝐐     𝐐𝐐     𝐍𝐐   low    high   avg. CC
Table 1 shows the distribution, reflecting a well-spread range       pre-c    19    10   7      0      2    17      2      2.8
                                                                     post-c   40    5    7     11     17    25     15      5.4
of difficulty levels. Importantly, no consideration was made
towards the strength or weakness of any particular LLM, so
as not to bias the selection towards a particular LLM.
                                                                         All 𝖧𝖤𝗑 tasks have post-conditions; 19 have pre-conditions
     Each task 𝖧𝖤𝗑𝑘 is based on the task 𝖧𝖤𝑘 in HumanEval.
                                                                    (the rest have no constraint on their inputs). We take the
The new task either paraphrases the original natural lan-
                                                                    difficulty of their solutions, 𝑝𝑟𝑒𝐹 and 𝑝𝑜𝑠𝑡𝐹 , as an indicator
guage description and adds some new nuances/tweaks, or
                                                                    of their actual difficulty. Table 1 shows the distribution of
it formulates a related task, rather than an extension of the
                                                                    the difficulty class (see Section 3) and complexity (of the
original 𝖧𝖤𝑘 . Note that for LLMs, paraphrasing matters,
                                                                    solutions). The difficulty class is manually classified by a
as they are trained on natural language input (Guan et al.,
                                                                    human expert. The cyclomatic complexity is calculated with
2025). The idea is that even if an LLM has been trained
                                                                    the metric tool Radon (accessed 2025). The pre-conditions
with HumanEval, it needs to be able to generalize to solve
                                                                    are generally simple, though there are two 𝖭𝖰s. For example,
𝖧𝖤𝗑 tasks. For example, below is the original description of
                                                                    the task 𝖧𝖤𝗑1 describes a program that takes a string input
𝖧𝖤104 and its modified 𝖧𝖤𝗑104 . Notice that the phrasing is
                                                                    satisfying the grammar in (5). As previously discussed, such
different. The added twist is marked in bold.
                                                                    a pre-condition is 𝖭𝖰. Almost 75% of the post-conditions
              Given a list of positive integers 𝑥, return a         are challenging (𝖰𝖰 or 𝖭𝖰). For example, the solution post-
              sorted list of all elements that hasn’t any           condition of the aforementioned 𝖧𝖤𝗑104 is of the difficulty
   𝖧𝖤104                                                            class 𝖰𝖰.
              even digit. Note: Returned list should be
              sorted in increasing order.
              Given a non-empty array 𝑠 of integers and             5.3. Models
              an integer 𝑘 between 1 and 9 (inclusive),                 The EvalPlus Leaderboard (Liu et al., 2023a) provides a
              the program returns a sorted array 𝑡 con-             comparison of various LLMs designed for code generation,
   𝖧𝖤𝗑104
              sisting of all integers in s which have a             ranking them based on the pass@1 metric (Chen et al., 2021).
              digit that is divisible by 𝑘. Digit 0 is              For our selection process, we focused on models with a
              considered as always divisible.                       pass@1 score greater than 70. We downloaded open models
                                                                    from Hugging Face (Wolf et al., 2020) and eliminated those
                                                                    that could not be processed using llama.cpp (Gerganov,
Each HEx task is a tuple:                                           2023) or that exceeded our computational resources. The
                                                                    final list of open models, shown in light blue in Table 2, also
      (𝐷, 𝐹 , 𝑝𝑟𝑒𝐹 , 𝑝𝑜𝑠𝑡𝐹 , 𝑇𝑝𝑟𝑒 , 𝑇𝑝𝑜𝑠𝑡 )                   (6)   includes some recent releases such as Athene and Qwen3,
                                                                    resulting in 17 models. The closed models primarily come
• 𝐷 is a natural language specification of some program,
                                                                    from OpenAI© , Google© , and Anthropic© , totaling 7 mod-
• 𝐹 is a Python implementation of 𝐷,                                els (represented in dark blue in Table 2). This selection
                                                                    features at least two generations from each model family.
• 𝑝𝑜𝑠𝑡𝐹 is a Boolean function (also in Python) formalizing          Overall, Table 2 presents a complete list of 24 models used in
  𝐹 ’s full post-condition,                                         our study, detailing their full names, abbreviated names used
                                                                    in plots, and, for the open models, the number of parameters
• 𝑝𝑟𝑒𝐹 is a Boolean function formalizing 𝐹 ’s full pre-
                                                                    and size.
  condition,
• 𝑇𝑝𝑟𝑒 and 𝑇𝑝𝑜𝑠𝑡 are test suites. The first is used to validate     5.4. Experiment protocol
  proposed (by LLMs) pre-conditions, the second to vali-                The experimental protocol follows the methodology de-
  date proposed post-conditions.                                    scribed in Section 4 and comprises two parts: prompting and
                                                                    solution validation.
    Given 𝐷, the task for an LLM is to come up with 𝑝𝑟𝑒′                During the prompting phase, we send the prompt 10
and 𝑝𝑜𝑠𝑡′ which are equivalent to the provided solution             times for each model and each task, resulting in 4,560
𝑝𝑟𝑒𝐹 and 𝑝𝑜𝑠𝑡𝐹 . Since full verification of equivalence is          proposed solutions for pre-conditions and 9,600 proposed
undecidable, the test suites 𝑇𝑝𝑟𝑒 and 𝑇𝑝𝑜𝑠𝑡 are used instead        solutions for post-conditions. Proprietary models are ac-
to validate this (see Section 4.2). The original HumanEval          cessed through their APIs, while open models are run locally
was meant to assess LLMs’ ability to construct programs             on a machine equipped with 8 Tesla© A40 GPUs, each
given their natural language description (𝐷); so, 𝑝𝑟𝑒𝐹 and          with 48GB of VRAM. The size of open models is limited
𝑝𝑜𝑠𝑡𝐹 solutions were not provided. In our dataset 𝖧𝖤𝗑, these        to 380GB, which is the total amount of VRAM available
components are provided.                                            when using all 8 GPUs simultaneously. All models operate

ThisisaPreprint                                                                                                      Page 7 of 18
                                                   Talk is Cheap, Logic is Hard

Table 2
LLMs used in the study. Proprietary models are shaded in blue, open models in light blue.
                        Full name                          Short name        Parameters (B)     Size (GB)
                         claude-3-7-sonnet                 Claude3.7                      -             -
                         claude3-haiku                     Claude3                        -             -
                         gemini-1.5-flash                  Gemini1.5                      -             -
                         gemini-2.0-flash-exp              Gemini2.0                      -             -
                         gpt-3.5-turbo                     GTP3.5                         -             -
                         gpt-4-turbo                       GPT4                           -             -
                         gpt-4o                            GPT4o                          -             -
                         athene-v2-chat                    Athene                     72.70           271
                         CodeFuse-DeepSeek-33B             CodeFuse                   33.30           125
                         codegemma-7b-it                   CodeGemma                   8.54            32
                         CodeQwen1.5-7B-Chat               CodeQwen1.5                 7.25            28
                         Codestral-22B-v0.1                Codestral                  22.20            83
                         deepseek-coder-33b-instruct       DeepSeekCoder              33.30           125
                         gemma-3-27b                       Gemma3                     27.40           101
                         Hermes-2-Theta-Llama-3-70B        Hermes2                    70.60           263
                         Meta-Llama-3-70B-Instruct         Llama3                     70.60           263
                         Nxcode-CQ-7B-orpo                 Nxcode                      7.25            28
                         OpenCodeInterpreter-DS-6.7B       OpenCodeInt                 6.74            26
                         OpenCoder-8B-Instruct             OpenCoder                   7.77            29
                         Qwen2.5-Coder-32B-Instruct        Qwen2.5                    32.80           123
                         speechless-codellama-34b-v2.0     Codellama                  34.00           126
                         starchat2-15b-v0.1                Starchat2                  16.00            60
                         WizardCoder-33B-V1.1              WizardCoder                33.30           125
                         Qwen3-32B                         Qwen3                      32.80           123


with a temperature setting, controlling the randomness of          emphasis was put on the so-called accept@1 metric, similar
the model’s output, of 0.7. This is the typical default of         to the popular pass@1 (Chen et al., 2021). We propose more
many LLMs, giving a medium level of randomness. The                refined metrics that also give further insight on how close are
maximum number of tokens, which limits the length of               LLMs’ solutions to being good, allowing for a more nuanced
the generated text, is set to 1,024. Recall that the prompt        understanding of the strengths and weaknesses of LLMs in
specifically asks the LLM to just answer with the code of          formalizing pre- and post-conditions.
pre-/post-conditions; the limit should be generous for this.
    The solution validation phase comprises of 162 manually        accept@1
written tests for pre-conditions and 603 for post-conditions.      For a given task and an LLM, the metric accept@k is
For each program 𝐹 in the dataset, the manually written            conceptually defined as the expected probability of extract-
tests achieves 100% branch coverage. To provide additional         ing a correct solution when sampling 𝑘 solutions (Endres
strength, these test suites are extended further using the tools   et al., 2024). In particular, accept@1 is then the probability
Pynguin and Poodle, as detailed in Section 4.2. Pynguin is         of getting the right answer from just one attempt. In our
configured with a maximum test generation time of 180 sec-         experiment setup, see previous Section 5.4, for every task
onds and uses the DYNAMOSA algorithm. As all programs              the prompt is repeated ten times. So, we get ten ’replicas’.
in the dataset use Python type annotations, we emphasize           The expected probability accept@1 is approximated by the
explicit typing by setting original_type_weight to 100, while      proportion of correct solutions observed among these ten
minimizing the weights of inference parameters type4py             replicas.
and type_tracing to 0.01. The tool targets branch coverage
and limits collection size to 10 elements. Finally, a low          Mean Passing Tests
object_reuse_probability of 0.01 promotes the creation of              When an LLM fails to give a correct solution, near-
new objects, increasing test diversity. In total, we generated     correct solutions could still be valuable. For instance a
additional 1383 tests for pre-conditions and 1662 for post-        developer could accept a near-correct solution and make an
conditions.                                                        effort to fix it. Hence, we also want to know how close the
                                                                   solutions proposed by the LLM are to being correct. The
5.5. Metrics                                                       accept@1 metric is however too coarse for this, as it only
    To evaluate LLM performance (RQ1), we measure                  looks at correct solutions. Suppose that for a program 𝐹 (𝑥)
different aspects of the quality of the solution proposed by       models 𝑀1 and 𝑀2 return solutions 𝑠1 and 𝑠2 . If 𝑠1 passes
the LLM. In total, seven metrics are used. In previous work        99% of the tests and 𝑠2 5%, we could say that 𝑀1 generates
(Wen et al., 2024; Endres et al., 2024; He et al., 2024) much      a better approximation of the correct solution than 𝑀2 .

ThisisaPreprint                                                                                                     Page 8 of 18
                                                    Talk is Cheap, Logic is Hard

Consequently we introduce the Mean Passing Tests metric             as post_M1 incorrectly states that −2 is not the correct
which captures this notion. For a given LLM and a task 𝑇 ,          output for the input [−5, −2, −10] and thus marking a correct
Mean Passing Tests is computed as the average proportion            implementation of the findMax program as incorrect.
of correct (passing) tests across 10 replicas for the task 𝑇 .          Consider now a negative test for post: (20, [5, 2, 10]).
                                                                    This test is negative because an implementation of find-
Error Rate                                                          Max that returns 20 for the input list [5, 2, 10] is incorrect.
    With the Error Rate metric we quantify all scenarios            Therefore, the correct post-condition post evaluates to false.
where an LLM proposed pre- or post-condition 𝑝 fails to             Consider a different model, 𝑀2 , which does not recognise
produce a well-formed output. Examples of this include              that the output should be an element of the input list and
cases where 𝑝 is not present at all, or 𝑝 is present but it         produced the following post-condition:
does not return a boolean value when applied to a test 𝑡
or where 𝑝 is not even syntactically correct, and will thus                 𝐝𝐞𝐟    𝗉𝗈𝗌𝗍_𝖬𝟤(𝑟𝑒𝑡𝑣𝑎𝑙∶𝑖𝑛𝑡, 𝑎∶𝑙𝑖𝑠𝑡[𝑖𝑛𝑡]) → 𝑏𝑜𝑜𝑙 ∶
crash when applied to 𝑡. Unlike failed tests, which require an                     𝐫𝐞𝐭𝐮𝐫𝐧 𝖺𝗅𝗅(𝑟𝑒𝑡𝑣𝑎𝑙 ≥ 𝑥 𝐟𝐨𝐫 𝑥 𝐢𝐧 𝑎)
oracle for detection, an error could potentially be identified
by examining the output of the LLM proposed solution. For a         For the negative test (20, [5, 2, 10]), the post-condition post_-
given LLM, the Error Rate metric is computed as the number          M2 evaluates to true, therefore accepting an incorrect im-
of runs (out of 10) that resulted in error. For an LLM, a high      plementation of the findMax program. We call this a false
Error Rate is an indication that it struggles in the more basic     positive, because post_M2 incorrectly states that 20 is the
skill of producing syntactically and type correct pre-/post-        correct output for the input [5, 2, 10]. In this case, a buggy
conditions.                                                         implementation of findMax is accepted by the post-condition
                                                                    post_M2.
False positive and false negative rates                                 The notions of false negative and false positive tests
     If a test does not result in an error, the pass/fail clas-     allow the pass/fail classification of non erroneous tests to
sification can be further refined by considering whether it         be refined. Consider the post-condition candidate 𝑝𝑜𝑠𝑡𝑀
is a positive or a negative test, as defined in Section 4.2.        generated by an LLM 𝑀 for a program 𝐹 . The objective
Consider a program 𝐹 that takes an input 𝑥 and produces an          is to assess how accurately 𝑝𝑜𝑠𝑡𝑀 captures the correctness
output 𝐹 (𝑥). A post-condition is a boolean function, denoted       criteria defined by the oracle post-condition 𝑝𝑜𝑠𝑡𝐹 . Evaluat-
as 𝑝𝑜𝑠𝑡𝐹 (𝐹 (𝑥), 𝑥), that formally specifies the properties the     ing 𝑝𝑜𝑠𝑡𝑀 against 𝑝𝑜𝑠𝑡𝐹 for a specific test (𝑜, 𝑥) yields four
output 𝐹 (𝑥) must satisfy for a given input 𝑥 for the program       possible outcomes:
𝐹 to be considered correct. A test case for the post-condition
                                                                    • True Positive (TP): both 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) and 𝑝𝑜𝑠𝑡( 𝑜, 𝑥) are
𝑝𝑜𝑠𝑡𝐹 is a pair (𝑜, 𝑥), where 𝑥 is a valid input for the program
                                                                      true. This signifies that the LLM’s post-condition cor-
𝐹 and 𝑜 is a possible output of 𝐹 . The test (𝑜, 𝑥) is a positive
                                                                      rectly validates a correct program output.
test if 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) evaluates to true, else (𝑜, 𝑥) is a negative
test.                                                               • True Negative (TN): both 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) and 𝑝𝑜𝑠𝑡( 𝑜, 𝑥) are
     As an example, let us consider the program findMax               false. In this case, the LLM’s post-condition identifies an
intended to find the maximum value in a non-empty list a              incorrect program output, thereby correctly flagging the
of integers. A robust post-condition post for findMax would           program 𝐹 as faulty.
assert the following two properties: the returned value must
be present in the input list, and the returned value must           • False Negative (FN): 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) is true, but 𝑝𝑜𝑠𝑡𝑀 (𝑜, 𝑥)
be greater than or equal to every other element in the list           is false. This is a scenario where the LLM’s post-condition
(see Eq. 1). A Python function that encodes a correct post-           is too strong, leading to the incorrect rejection of a valid
condition is shown below:                                             program output. This could cause a correct program to be
                                                                      flagged as incorrect.
        𝐝𝐞𝐟   𝗉𝗈𝗌𝗍(𝑟𝑒𝑡𝑣𝑎𝑙∶𝑖𝑛𝑡, 𝑎∶𝑙𝑖𝑠𝑡[𝑖𝑛𝑡]) → 𝑏𝑜𝑜𝑙 ∶                • False Positive (FP): 𝑝𝑜𝑠𝑡𝐹 (𝑜, 𝑥) is false, but 𝑝𝑜𝑠𝑡𝑀 (𝑜, 𝑥)
              𝐫𝐞𝐭𝐮𝐫𝐧 𝑟𝑒𝑡𝑣𝑎𝑙 𝗂𝗇 𝑎 𝖺𝗇𝖽 𝖺𝗅𝗅(𝑟𝑒𝑡𝑣𝑎𝑙 ≥ 𝑥 𝐟𝐨𝐫 𝑥 𝐢𝐧 𝑎)       is true. This is a critical failure where the LLM’s post-
The pair (−2, [−5, −2, −10]) is a positive test for post,             condition is too weak. Model 𝑀 incorrectly validates a
because a correctly implemented findMax should return −2              wrong program output, thus failing to detect a bug and
for the input list [−5, −2, −10]. Now suppose that the model          potentially leading to the acceptance of a faulty program.
𝑀1 incorrectly assumes that the output must be non-negative           This is often considered a more dangerous error in verifi-
and returns the following buggy post-condition:                       cation than a false negative.

                                                                        The False Negative Rate (FNR) over the test cases rep-
     𝐝𝐞𝐟   𝗉𝗈𝗌𝗍_𝖬𝟣(𝑟𝑒𝑡𝑣𝑎𝑙∶𝑖𝑛𝑡, 𝑎∶𝑙𝑖𝑠𝑡[𝑖𝑛𝑡]) → 𝑏𝑜𝑜𝑙 ∶                resents the proportion of positive cases that are incorrectly
           𝐫𝐞𝐭𝐮𝐫𝐧 𝑟𝑒𝑡𝑣𝑎𝑙 𝗂𝗇 𝑎                                       identified as negative. In other words, it reflects the like-
                  𝖺𝗇𝖽 𝖺𝗅𝗅(𝑟𝑒𝑡𝑣𝑎𝑙 ≥ 𝑥 𝐟𝐨𝐫 𝑥 𝐢𝐧 𝑎) 𝖺𝗇𝖽 𝑟𝑒𝑡𝑣𝑎𝑙 ≥ 0     lihood of a correct program being flagged as incorrect.
The post-condition post_M1 evaluates to false on the posi-          Conversely, the False Positive Rate (FPR) is the proportion
tive test (−2, [−5, −2, −10]). We call this a false negative,       of actual negatives that are incorrectly classified as positives.

ThisisaPreprint                                                                                                        Page 9 of 18
                                                    Talk is Cheap, Logic is Hard

Put simply, it measures how often a post-condition leads to a       shows the results for pre-condition generation and the plot at
positive result when the program is incorrect. More formally,       the bottom shows the results for post-condition generation,
                                                                    while the names of the models are shown on the x-axis,
                    𝐹𝑁                        𝐹𝑃
         𝐹𝑁𝑅 =                     𝐹𝑃𝑅 =                            sorted in decreasing order of Mean Passing Tests for post-
                  𝐹𝑁 + 𝑇𝑃                   𝐹𝑃 + 𝑇𝑁                 conditions. Each boxplot in Figure 3 corresponding to an
    The same considerations regarding test classification           LLM represents the results obtained when applying that
also apply to pre-conditions.                                       LLM on all tasks (pre- or post-condition) each repeated 10
    FNR and FPR are further refinement of the aforemen-             times. The boxplots corresponding to proprietary models are
tioned test passing rate metric. Recall that the latter gives an    shown in blue colour, while those corresponding to open
indication on how close an LLM solution is to being correct.        models are shown in light blue. Overall we can observe that
If a developer, hypothetically, adopts a post-condition from        the models, proprietary models in particular, tend to perform
an LLM as is, and it turns out to be only near-correct, FNR         better on pre-condition generation than post-condition. We
gives an indication on how noisy the post-condition is by           can also observe that proprietary models perform generally
producing spurious bug alarms, and FPR is an indication of          better than the open models, across all tasks, in terms of both
how lossy it is by failing to catch bugs.                           the accept@1 and mean passing tests metrics. We can further
                                                                    notice that the proprietary models have high mean passing
Difficulty related metrics                                          tests numbers, considerably higher than their accept@1. This
    To evaluate the impact of task difficulty on LLMs’              suggests that their solutions, even if not correct, are still often
performance (RQ2), we calculate the number of failing               near correct. Section 7 will show some examples of these.
models per task, for each category of difficulty. A model                The plots shown in Figure 3 are based on pre-/post-
is considered to have failed a specific task if there is at least   conditions returned by the LLMs and were parsed correctly
one failing test in each replica. This could give us insight        as executable Python code, i.e., execution of the generated
on, for example, whether across the board LLMs can handle           code gives pass/fail result. However, in our experiments we
pre- and post-conditions that involve quantifiers. Another          have noticed the presence of quite a significant proportion
important metric is the number of tasks of each category            of pre-/post-condition code returned by LLMs that results
of difficulty with accept@1 > 0 for an LLM. If a model’s            in error where the returned code either does not represent a
accept@1 is not 0, this indicates that there is at least one        valid Python code or is somehow malformed and/or returns
replica in which the model proposes a correct solution for          values outside of the expected range, thus resulting in an
the task.                                                           error. Figure 4 shows, for each task in the experiment, the
                                                                    number of runs (out of 10) that resulted in error for each of
Impact of automated testing                                         the LLMs, i.e., the Error Rate. Each dot in the plot represents
     Finally, we calculate the number of misclassified solu-        the number of times an LLM gave an erroneous response for
tions to assess the impact of automated generated tests on the      a task (pre-/post-condition generation) out of 10 replicas. We
benchmark. A solution 𝑠 proposed by a model 𝑀 for a task            consider a solution proposed by an LLM to be erroneous if
𝑇 is misclassified if 𝑠 was deemed correct based on manual          the execution of at least one test case results in an erroneous
tests, but was found to be incorrect when executed against          output. Python being an interpreted language, some of the
automatically generated tests. The automatically generated          errors are revealed only in certain execution scenarios, which
tests thus manage to identify an incorrect solution, for which      in our experiments are represented by different test cases,
the manual test suite failed to do so. The number of misclas-       both written manually and generated automatically (see Sec-
sified solutions gives thus indication on the contribution of       tion 5 for details). For example, on the 𝖧𝖤𝗑57 task, the best
automatically generated tests in augmenting the manual tests        performing model (Claude3.7), out of the 10 replicas, it gave
in the dataset.                                                     9 correct results and one erroneous result. The erroneous
                                                                    result causes a runtime Python error when executed on a test
6. Results                                                          case.
                                                                         As can be seen from Figure 4, the open LLMs tend to
    Here we present the results of the experiment and pro-          produce a high number of code that ends up in error. A closer
vide answers to the research questions.                             inspection reveals that the error cases are mainly due to: 1)
                                                                    the LLM failing to produce correct Python code, 2) the pre-
6.1. RQ1 (LLM performance)                                          /post-condition function returns an unexpected value, e.g.,
    RQ1 investigates the performance of LLMs in generat-            an integer instead of boolean, 3) the LLM does not follow the
ing formal pre-/post-conditions from their natural language         prompted instruction well e.g., by not producing any code at
descriptions. Figure 3 shows the results for all the LLMs           all, or by returning a lengthy explanation text from which it is
considered in our experiment, based on the Mean Passing             difficult to reliably extract the code part. Note that the prompt
Tests and accept@1 metrics (see Section 5.5). The boxplots          in Figure 1 explicitly instructs the LLM not to provide an
show the values of the Mean Passing Tests metric for each           explanation.
model, i.e., the proportion of the test cases that pass when             The performance results shown in Figure 3 should be
executed on the code proposed by the LLM. The asterisks             interpreted in light of the Error Rate presented in Figure 4
correspond to the accept@1 metric. The plot at the top

ThisisaPreprint                                                                                                        Page 10 of 18
                                                   Talk is Cheap, Logic is Hard

                                                     Open model            Yes     No
                                                                   Pre
                                       100%


                                       75%


                                       50%


                                       25%
                  Mean Passing Tests




                                           0%

                                                                   Post
                                       100%


                                       75%


                                       50%


                                       25%


                                           0%
                                                       em .7

                                                        G .0
                                                                4o

                                                       em 4

                                                        G .5
                                                       C 3.5

                                                        At 3
                                                      G ene

                                                        Ll 3
                                                      Q a3

                                                      H 2.5

                                                      eG s2

                                                        Q a

                                                W ode 3
                                                        dC l

                                                         e r

                                                O nC a

                                                 pS od r
                                                        kC t
                                                      od er

                                                                 e

                                                        w e
                                                        ar 5
                                                                  2
                                                      ar stra




                                                     ee eIn
                                                      od e


                                             D en ode
                                                    G PT




                                                                e



                                                                a




                                                               m

                                                     C en




                                                     pe m




                                                              us

                                                    eQ d

                                                     St n1.

                                                               at
                                                    G e3

                                                              i2




                                                              i1




                                                    C od




                                                    C od
                                                  od rme
                                                           PT




                                                            ud



                                                             m
                                                           am




                                                             o
                                                          TP




                                                           en


                                                          em




                                                  O lla




                                                           ch
                                                           in




                                                           in




                                                          eF
                                                           w
                                                            h




                                                od Nxc
                                                          G
                                                         ud




                                                        em




                                                          e
                                                         la




                                                        w




                                              ee C
                                                        e
                                             la
                                            C




                                                   iz




                                                  p
                                                C




                                               C
Figure 3: Boxplot showing the distribution of Mean Passing Tests. Each dot represents the average across 10 replicas of successful
tests for a task. The pink asterisk indicates the average accept@1 across all tasks.


                                                    Open model            Yes     No

                                       10

                                       8
                  Error Rate




                                       6

                                       4

                                       2

                                       0
                                                     em 3.7

                                                      G .0
                                                              4o

                                                     em 4

                                                      G .5
                                                     C 3.5

                                                      At 3

                                                      em e

                                                      Ll 3
                                                    Q a3

                                                    H 2.5

                                                    eG es2

                                                      Q a
                                                   C en3

                                                      dC l
                                                    od er

                                                               a




                                                                2
                                                                r

                                                      kC t




                                                      w e
                                                        eF r
                                                      N se


                                                   St n1.5
                                                    ar tra




                                                   ee eIn
                                           D en ode



                                                  C ode
                                                  G PT




                                                              e

                                                              n

                                                              a




                                                             m




                                                   pe m




                                                  eQ od



                                                             at
                                                            i2




                                                            i1




                                                  C od




                                                            u
                                                         PT




                                                          ud

                                                          he

                                                           m
                                                         am




                                                           s
                                                          e




                                                        TP




                                                         en



                                                        em




                                                O lla




                                                         ch
                                                         in




                                                         in




                                              C erm



                                                         w




                                               pS od




                                               od xc
                                                        G




                                              W de
                                                       ud




                                                        e
                                                p C
                                                       la




                                                       e




                                                      ar
                                                      w




                                                      n
                                            ee C



                                                    od
                                                     o
                                       la




                                                    G
                                             G
                                       C




                                                od




                                                 iz




                                              O




                                             C




Figure 4: Number of replicas where the LLM proposed solution on a task is not valid because at least one test returns an error
when executed on it. Each dot represents a task. For instance, the dot with value ten for Claude3.7 model means that there is a
task for which all ten replicas contain an execution of a test that results in an error.



where we can observe the general pattern that the best             that these cases do not include the erroneous cases discussed
performing models tend to be those with lower Error Rate           in the previous paragraph. To get insight into the nature of
values. It is also interesting to note, however, that even the     the wrong proposals produced by the models, we inspect the
best performing models produce erroneous proposals, as             data related to cases of False Positive and False Negative
demonstrated by the presence of outliers in the plot shown         (see Section 5.5). Figure 5 shows the distribution of False
in Figure 4.                                                       Negative Rate (FNR, top plot) and False Positive Rate (FPR,
    Delving further into the results, we inspected the cases       bottom plot) for each model on the post-condition generation
where the models gave the wrong answer, i.e., the proposals        tasks. Recall that FNR is an indicator of how noisy a
generated by the models fail on one or more tests. Please note     proposed pre-/post-condition is, whereas FPR indicates how


ThisisaPreprint                                                                                                    Page 11 of 18
                                                  Talk is Cheap, Logic is Hard

                                                 Open model       Yes        No

                                        100%




                  False Negative Rate
                                        75%


                                        50%


                                        25%


                                         0%

                                        100%
                  False Positive Rate




                                        75%



                                        50%



                                        25%



                                         0%
                                                     em .7

                                                      G .0
                                                              4o

                                                     em 4

                                                      G .5
                                                     C 3.5

                                                      At 3
                                                    G ene

                                                      Ll 3
                                                    Q a3

                                                    H 2.5

                                                    eG s2

                                                      Q a

                                              W ode 3
                                                      dC l

                                                       e r

                                              O nC a

                                               pS od r
                                                      kC t




                                                      w e
                                                    od er

                                                               e



                                                      ar 5
                                                                2
                                                    ar stra




                                                   ee eIn
                                                    od e


                                           D en ode
                                                  G PT




                                                              e



                                                              a




                                                             m

                                                   C en




                                                   pe m




                                                            us

                                                  eQ d

                                                   St n1.

                                                             at
                                                  G e3

                                                            i2




                                                            i1




                                                  C od




                                                  C od
                                                od rme
                                                         PT




                                                          ud



                                                           m
                                                         am




                                                           o
                                                        TP




                                                         en


                                                        em




                                                O lla




                                                         ch
                                                         in




                                                         in




                                                        eF
                                                         w
                                                          h




                                              od Nxc
                                                        G
                                                       ud




                                                      em




                                                        e
                                                       la




                                                      w




                                            ee C
                                                      e
                                          la
                                         C




                                                 iz




                                                p
                                              C




                                             C
Figure 5: Boxplot showing the False Negative (above) and Positive (below) Rates per task. Each dot shows the average FNR/FPR
across ten replicas of a model on a task. Red cross mark indicates the Error Rate.



lossy it is. As can be seen from the plot in Figure 5, the
                                                                        Overall, the LLMs were able to generate valid pre-
LLMs generally have a low FNR, i.e., the post-condition
                                                                        and post-conditions for the majority of the tasks,
proposed by the LLM has a low probability of incorrectly
                                                                        with the proprietary models being significantly
marking a correct program as wrong. Some open source
                                                                        more effective than open models. Looking at the
models, such as Starchat2 and Athene, appear to have a lower
                                                                        wrong solutions, those from proprietary models
FNR compared to closed models. However, when comparing
                                                                        are often near-correct, with high tests passing rate.
different LLMs, the Error Rate should be considered (red
                                                                        FPR and FNR are generally low on pre-condition
cross mark in Figure 5). While it is true that Starchat2 has
                                                                        tasks than on post-condition tasks. Proprietary
a very low FNR, it was only able to produce a non-error
                                                                        models have slightly higher FPR and FNR on post-
solution on four tasks. The same applies to FPR. Some
                                                                        condition tasks than on pre-conditions. Results
closed models have quite low FNR and FPR as well as Error
                                                                        also show that open models generate an over-
Rate. Even a higher FNR may not be bad, as a spurious
                                                                        whelmingly large number of erroneous solutions.
error alarm would trigger the developer to investigate and
fix the pre- or post-condition he/she adopted. Once fixed, the
error will not appear again. On the other hand, low FPR still     6.2. RQ2 (Impact of task difficulty on LLM
means that there is risk. It is then prudent to complement an          performance)
LLM-generated pre- or post-condition, if adopted, with e.g.            With RQ2 we investigate the performance of the LLMs
manual tests. When we consider closed models, we can also         as a function of the difficulty of the task. We consider two
see the improvements in terms of lower FNR and FPR across         notions of difficulty, i.e., cyclomatic and semantic complex-
different versions of the same model. For instance, when          ity. The details of these metrics and how they are computed is
considering FPR, Claude3 has a median FPR of 5%, which            discussed in Section 3.3, while a summary of the complexity
is reduced to zero in the new Claude3.7 version. However,         metrics for our dataset is presented in Table 1.
even the top-performing models show some outliers, with
peaks exceeding 25% for both FNR and FPR. The results             6.3. RQ2.1 Cyclomatic complexity
for pre-condition tasks are generally similar to those of post-       As shown in Table 1, the tasks in our dataset are grouped
condition tasks but the FPR and FNR values tend to be lower.      into low (CC ≤ 5) and high (CC > 5) complexity based
The detailed results are included in our replication package.     on the cyclomatic complexity of the (manually written)
                                                                  functions that implement the contracts (Section 3). Figure 6

ThisisaPreprint                                                                                                    Page 12 of 18
                                                  Talk is Cheap, Logic is Hard




Figure 6: Number of models failing to produce a valid post-condition for each task across different difficulties. Colours indicate
the difficulty category of a task, and strips the cyclomatic complexity.



shows, for each post-condition generation task, the number         solutions belong to the NQ class. Aside from a few outliers
of LLMs that fail to produce a valid post-condition. Notice        where few models were challenged by NQ tasks (𝖧𝖤𝗑65 and
that in the plot in Figure 6 the cyclomatic complexity of          𝖧𝖤𝗑84 ), overall the difficulty class, similar to the cyclomatic
each task is represented by the patterns of the stripes. As        complexity, highlights the challenge faced by LLMs when
can be seen from the figure, the tasks with high cyclomatic        dealing with difficult specifications.
complexity indeed challenge the LLMs where in the extreme               To get further insight, we also analysed, for each LLM,
case (𝖧𝖤𝗑158 ) none of the LLMs were able to generate a            how many of the tasks of each difficulty class it was able
valid solution for it. For the tasks with low complexity the       to find a valid solution for. In Figure 7 we plot the number
number of LLMs that fail to generate a valid solution drops        of post-conditions each model was able to find at least one
considerably. There are however cases where the complexity         correct solution out of the 10 replicas, distinguished by the
class does not appear to match the observed results, i.e.,         difficulty class. We observe that proprietary models and
low complexity tasks leading to a large number of LLMs             some of the open models (e.g. Qwen) are able to handle
failing to generate a valid solution (e.g., 𝖧𝖤𝗑73 , 𝖧𝖤𝗑141 ,       S, Q, and QQ tasks well. The newer proprietary models
𝖧𝖤𝗑57 ). On the contrary, some of the high complexity tasks        perform well on the difficult tasks (NQ) while the older
do not appear to be as challenging (e.g., 𝖧𝖤𝗑111 , 𝖧𝖤𝗑161 , and    ones (Gemini1.5, GPT3.5) do not perform as well as their
𝖧𝖤𝗑114 ). Some of these outlier cases are discussed in greater     latest variants. It is also worth noting that the number of
detail in Section 7. Overall, we can observe that tasks with       low-difficulty tasks (S and Q) tends to be stable over a large
high cyclomatic complexity do pose challenges to the LLMs’         number of the LLMs. Though we do not show the plot
capability of generating valid post-conditions.                    here due to space limitations, a similar trend is observed for
                                                                   cyclomatic complexity as well.
6.4. RQ2.2 Semantic complexity
    While cyclomatic complexity is an indirect measure of
                                                                         Our dataset is composed of tasks with varying
a task’s difficulty, as it is based on the complexity of the
                                                                         difficulty, and our experiment reveals that the per-
function written to implement it, in RQ2.2 we look at a
                                                                         formance of LLMs is significantly affected by the
measure of complexity of the task considering its natural
                                                                         difficulty level of the task at hand, performing well
language specification. Our analysis (see Section 3) led to
                                                                         on non-NQ tasks, but not on NQ ones. In the
four complexity classes to which the tasks in our dataset
                                                                         extreme case, none of the 24 LLMs in our study
belong (see Table 1 for a summary). Similarly to RQ2.1,
                                                                         were able to generate a valid solution for one of
we consider post-condition tasks only. We can see from
                                                                         the tasks. On the other hand, the best performing
Figure 6 (colored shades) that generally more than half
                                                                         models are able to solve a higher number of diffi-
of the tested LLMs are able to produce a correct solution
                                                                         cult tasks.
for tasks with difficulty S, Q, or even QQ, indicating that
these are the kind of tasks that are reasonably within the
current LLMs capability. However, tasks classified as NQ
(non quantifiable) do indeed challenge the LLMs leading to         6.5. Impact of automatically generated tests
a majority of the LLMs not producing valid post-conditions.            The results discussed so far are based on the entire set
With the exception of a few cases (e.g., 𝖧𝖤𝗑57 ) the tasks         of test cases in our dataset, i.e., both tests written manually
on which a large number of LLMs fail to produce valid              and those generated automatically (Section 4). Here we take

ThisisaPreprint                                                                                                     Page 13 of 18
                                                                                                     Talk is Cheap, Logic is Hard




            Number of post tasks with accept@1 > 0
                                                                                        Difficulty             S             Q           QQ              NQ



                                                     30



                                                     20



                                                     10



                                                     0
                                                                   em 3.7

                                                                    G .0
                                                                            4o

                                                                   em 4

                                                                    G .5



                                                                    At 3
                                                                   C 3.5



                                                                    em e

                                                                    Ll 3
                                                                  Q a3

                                                                  H 2.5

                                                                  eG es2



                                                                 C en3
                                                                    Q a



                                                                    dC l
                                                                  od er

                                                            O nC a
                                                                              r

                                                                    kC t




                                                                    w e
                                                                      eF r
                                                                    N se


                                                                 St n1.5

                                                                              2
                                                                  ar tra




                                                                 ee eIn
                                                         D en ode



                                                                C ode
                                                                G PT




                                                                            e

                                                                            n

                                                                            a




                                                                           m




                                                                 pe m




                                                                eQ d



                                                                           at
                                                                          i2




                                                                          i1




                                                                C od




                                                                          u
                                                                       PT




                                                                        ud

                                                                        he

                                                                         m
                                                                       am




                                                                         o
                                                                         s
                                                                        e




                                                                      TP




                                                                       en



                                                                      em




                                                              O lla




                                                                       ch
                                                                       in




                                                                       in




                                                            C erm



                                                                       w




                                                             pS od




                                                            od xc
                                                                      G




                                                            W de
                                                                     ud




                                                                      e
                                                                     la




                                                                     e




                                                                    ar
                                                                    w




                                                          ee C



                                                                  od
                                                                   o
                                                     la




                                                                  G
                                                          G
                                                     C




                                                              od




                                                               iz




                                                              p




                                                           C
                                             Figure 7: Number of correct post-conditions, across different difficulties, generated by each model.


                                                                                                     Open model                   Yes             No
                                                                                                              82
                                                     30%
            Misclassified Solutions




                                                                                                                        68                                           8

                                                                                        146                                                             10       5
                                                     20%
                                                                                                                                                   17
                                                                                                                             12
                                                                        269 240               143
                                                                                                                   97              84
                                                              332 258             219                                                        39
                                                     10%                                                                                63
                                                                                                    161 150


                                                                                                                                                             7           2   2   1
                                                     0%
                                                                        em 3.7

                                                                          G .0
                                                                                  4o

                                                                        em T4

                                                                         G .5



                                                                          At 3
                                                                        C 3.5


                                                                       G ene

                                                                          Ll 3
                                                                       Q a3

                                                                       H 2.5

                                                                       eG es2




                                                                 W ode 3
                                                                          Q a



                                                                          dC al

                                                                           e r
                                                                                     a

                                                                                     r

                                                                          kC t
                                                                       od er

                                                                                     e

                                                                          w e

                                                                         ar 5
                                                                                     2
                                                                      ee eIn
                                                                       od e


                                                              D en ode
                                                                                  e



                                                                                  a




                                                                                  n
                                                                                 m




                                                                      pe m




                                                                                us

                                                                     eQ od

                                                                      St n1.

                                                                                 at
                                                                                   r
                                                                                i2




                                                                                i1




                                                                     C od




                                                                     C od
                                                                                 t
                                                                             PT




                                                                              ud



                                                                               m
                                                                             am




                                                                                e
                                                                               P




                                                                               s
                                                             e




                                                                            TP




                                                                             en



                                                                            em




                                                                   O lla




                                                                             ch
                                                                             in




                                                                             in




                                                                 C erm




                                                                            eF
                                                                             w
                                                                              h




                                                                  pS od




                                                                  od xc
                                                                            G
                                                          ud




                                                                         em




                                                                            e
                                                                   p C
                                                                           la




                                                                          w




                                                                         N
                                                                          n
                                                               ee C
                                                       la




                                                                       ar
                                                                      C
                                                            G




                                                                     G
                                                      C




                                                                   od




                                                                    iz




                                                                 O




                                                                C


Figure 8: Percentage of invalid responses for post-conditions when considering only manual tests. The numbers above the bars
show the total number of valid solutions when using manual tests only.



a closer look at the results in order to get insight into the                                                            As can be seen from the figure, the automatically generated
role of the tests that were automatically generated. For this                                                            tests exposed several misclassified cases. It is worth men-
purpose we analyzed the results by distinguishing the cases                                                              tioning that the open LLMs (the right half of the figure)
where the LLMs produced correct results when considering                                                                 generate very few valid (non erroneous) solutions, as shown
only manually written tests but the outcome changed (i.e., the                                                           in Figure 4, hence the plot of misclassified solutions is based
solution proposed by the LLM turned out to be incorrect)                                                                 on a small number of cases.
when considering automatically generated tests as well. In
other words, we computed for each LLM how many pro-                                                                      7. Discussion
posed solutions would have been considered correct if we
had used only the manually written tests for checking the                                                                Erroneous solutions from open LLMs
correctness. For example, when considering only manual                                                                       As discussed in Section 6, open LLMs tend to produce
tests, 9.6% (32) of the valid solutions proposed by Claude                                                               more erroneous solutions. To get a more comprehensive
3.7 are actually invalid when automatically generated tests                                                              view of the successes and failures of the various LLMs, we
are also used. Keep in mind that the manually written tests                                                              have plotted the outcomes from all executions and all tasks in
achieve full branch coverage of the code. In Figure 8 we                                                                 Figure 9. As we can see from the figure, erroneous solutions
plot the number of cases where the use of automated tests                                                                account for a large proportion of the failures observed for the
exposed a wrong solution, i.e., solutions that were deemed                                                               open models, where the proportion of wrong solutions (false
correct with respect to manual tests, but turned out to be                                                               positives/negatives) are much less than the proportion of
wrong when executed against automatically generated tests.                                                               erroneous solutions. One of the reasons is that some LLMs
                                                                                                                         verbosely respond to prompts by generating explanations.

ThisisaPreprint                                                                                                                                                                      Page 14 of 18
                                                               Talk is Cheap, Logic is Hard


                                                      Metric      TP        TN          FP         FN         Err
                                                                                 Pre
                                        100%


                                        75%


                                        50%


                                        25%
              Percentage of all tests




                                         0%

                                                                                 Post
                                        100%


                                        75%


                                        50%


                                        25%


                                         0%
                                                                   .7

                                                          G 0
                                                                  4o

                                                         em 4

                                                          G .5

                                                           la 5

                                                          At 3
                                                        G ene

                                                          Ll 3

                                                          w 3
                                                        H 2.5

                                                        eG s2

                                                          Q a
                                                         o n3

                                                          dC l
                                                        od der

                                                                     a

                                                                     r

                                                          kC t




                                                          w e
                                                            eF r
                                                          N e


                                                       St 1.5

                                                                     2
                                                        ar tra




                                                       ee eIn
                                               D en de



                                                      C ode
                                                                   .


                                                      G PT



                                                                 3.

                                                                 e



                                                                  a

                                                                  a




                                                                 m




                                                    O llam




                                                                us

                                                      eQ d



                                                                 at
                                                               e3

                                                                i2




                                                                i1




                                                    od rme
                                                             PT




                                                                e
                                                              ud



                                                               m
                                                             am




                                                               o
                                                               s
                                                            TP




                                                             en



                                                            em




                                                            en

                                                             ch
                                                              o



                                                              o
                                                             in




                                                             in




                                                             w
                                                              h




                                                   pS od




                                                   od xc
                                                            G




                                                  W de
                                            ud




                                                          em




                                                  O nC
                                                 em




                                                           e




                                                          ar
                                                ee C



                                                        od
                                                          e
                                                         C
                                          la




                                                        Q




                                                       pe
                                                       C
                                               G
                                         C




                                                      C
                                                     iz




                                                    p
                                                  C




                                                 C
Figure 9: The barplot depicts the execution output of all executed tests for each model for pre- and post-conditions. The test
results are categorised as true positive (TP), true negative (TN), false positive (FP), false negative (FN) and error (Err), in
accordance with the metrics defined in Section 5.5.



This is the case with the five LLMs with the highest number                      This is certainly good news for open LLMs. If we however
of erroneous proposals. These are also the lowest performing                     look at the ten most challenging post-conditions in Figure 6
LLMs (Figure 3). Note that the prompt in Figure 1 explicitly                     (left most ten columns), they are all of the difficulty 𝖭𝖰,
asks the LLMs not to explain, as we are only interested                          which is perhaps not surprising. The good thing is that all
in the code. These LLMs fail to understand the instruction                       of them, except 𝖧𝖤𝗑158 , are at least collectively solvable by
well. For instance, Nxcode responds with an explanation                          the LLMs (that is, for each of these post-conditions, at least
but does not give the code. Deepseek-coder typically gives                       one LLM manages to produce one good solution within the
lengthy explanations and the code is embedded somewhere                          allotted ten tries). Unfortunately though, with the exception
in the explanation. It then becomes problematic to reliably                      of 𝖧𝖤𝗑21 and 𝖧𝖤𝗑141 , none of the solving LLMs are open
extract the code from the surrounding text. In contrast, the                     LLMs. This emphasizes the previously made observation on
top performing LLMs clearly understand the instruction and                       the significant gap between the open and proprietary LLMs.
return only the code; and if explanation is provided, it is                          The open LLM Llama3 (70B) is the only one that can
properly included as code comments. What this tells us is                        produce a correct solution for the post-condition of 𝖧𝖤𝗑21 .
that just training an LLM with programming skill is not                          However, GPT4o also came up with a solution that passed
sufficient. To be useful for end users, it also needs to be                      all the tests, but one. 𝖧𝖤𝗑21 involves calculations such as
trained to follow instructions (so-called instruct-training).                    ⌊𝑎 ∗ 𝑏∕𝑐⌋ that can be sensitive to the imprecision of 𝖿 𝗅𝗈𝖺𝗍
Propriety LLMs perform well on this, whereas the open                            arithmetic. The failing test exposes the imprecision. If this is
source community still has some gap to close on this aspect.                     tolerated, then arguably GPT4o’s solution can be considered
                                                                                 as correct as well. Neither solution employs robust floating
Difficult and subtle cases                                                       point arithmetic (e.g. using Python’s 𝖣𝖾𝖼𝗂𝗆𝖺𝗅 datatype), but
    The post-condition 𝖧𝖤𝗑104 mentioned in Section 5.2,                          to be fair, the natural language description of 𝖧𝖤𝗑21 did not
which is of difficulty 𝖰𝖰, is non trivial. Figure 6 shows that                   explicitly require that either.
most LLMs can actually solve it. Furthermore, it turns out                           𝖧𝖤𝗑158 is an interesting case as no LLM can solve it. The
that seven open LLMs can solve it (not shown in the figure).                     post-condition is of type 𝖭𝖰. Its description:


ThisisaPreprint                                                                                                                   Page 15 of 18
                                                        Talk is Cheap, Logic is Hard

      Given a list 𝑠 of strings, the program returns a string           Should we show the program’s code?
      with the longest stutter. A stutter of a string is a                  Our prompt (Figure 1) does not send the program’s code,
      segment of length at least two, consisting of the same            it only shows the program’s natural language description.
      letter. If no string in 𝑠 has a stutter, the program              This is a deliberate choice as we want to focus on contract
      returns 𝖭𝗈𝗇𝖾.                                                     generation purely from natural language descriptions. Also,
      Example: 𝖯𝗋_𝖧𝖤𝟣𝟧𝟪(["hiii!","woorld"]) = "hiii!"
                                                                        as remarked in Section 2, including the program code may
                                                                        pass on bugs in the code to the produced contract. It is
    Claude-3.7 and Gemini-2.0 produce solutions that pass               also unclear whether including code in the prompt would
93% of the tests (so, near correct), failing on three tests             actually help the LLM. In the study by Endres et al. (2024)
that check that only repeated letters count as a stutter, in            this does not lead to a significant improvement; in some
accordance with the description. Hence, "ii" counts as a                cases even worsens the performance. On the other hand,
stutter, but "11" does not. This subtle point is missed by both         tools like AutoSpec and SpecGen only use the program code
Claude-3.7 and Gemini-2.0. To be fair, a human programmer               (without program description) and showed that LLMs can
may miss the subtlety as well.                                          generate useful assertions, despite being partial. Faria et al.
    Another subtle case is the post-condition of 𝖧𝖤𝗑𝟧𝟢 :                (2026) use both code and descriptions inside the code in
      Given a string 𝑠, the program returns an encoded ver-
                                                                        an iterative approach with promising results. This could be
      sion of s. This is obtained by shifting every character           further investigated as future work, exploring different ways
      𝑐 in 𝑠. A letter is cyclicly shifted by 𝑘 symbols in the          of combining description-based and code-based approaches.
      alphabet. We keep the case (e.g. if it was lower case, it
      remains lower case). Digits in a number are shifted 𝑘             What does this mean in practice?
      symbols in 0..9. Non alpha-numneric characters, ex-                    As mentioned in the conclusion to RQ1, as it is now,
      cept spaces, are left unchanged. Segments consisting              the LLMs, in particular the high end proprietary models, are
      of only spaces are replaced by a single dash.                     able to produce correct or near correct full pre- and post-
      Example: 𝖯𝗋_𝖧𝖤𝟧𝟢("h3i!",1) = "i4j!"                               conditions in our dataset, indicating that adopting them in
The post-condition, which is of 𝖭𝖰 difficulty, is solved by             actual practice is a very plausible idea, at least for unit-
six LLMs (the LLMs give at least one correct proposal).                 level programs. Also, one can expect LLMs to become better
Interestingly, some wrong solutions from Claude-3.7 failed              in the future, e.g. due to increase in size and intensified
only on one test. A simplified version of this test gives               training. We cannot however expect LLMs to be flawless,
𝑠 = ε∖𝑥0𝑏ε and 𝑘=1 as the input, and poses the question                 both due to hallucination that is inherent in them and due to
whether the same 𝑠 would be a correct output 𝑡 of the                   ambiguity and incompleteness inherent in natural language
program 𝖯𝗋_𝖧𝖤𝟧𝟢. In Python, ∖𝑥0𝑏 is a code for the vertical             descriptions, leading to subtle cases as discussed earlier
tab character. A correct post-condition should approve this             in Section 7. This means that employing an LLM-based
𝑡. A vertical tab is not a letter, and technically it is not a          generation in practice requires a good test suite as a guard
space either. So, it should not be shifted. The wrong post-             rail, enabling developers to detect and fix subtle errors.
conditions rejected the 𝑡, insisting that the correct 𝑡 should be       Writing tests has of course its own cost, so we would want to
a "-", as per the red part of 𝖧𝖤𝗑𝟧𝟢 ’s description shown above.         know how to reduce this cost while still getting good quality
These post-conditions consider all white space characters,              pre- and post-conditions. This is as far as we know still an
including a vertical tab, as spaces. Indeed, arguably, the              open question and would make an interesting future work.
given natural language description was ambiguous.
    So, just like humans, LLMs are prone to natural lan-                8. Threats to Validity
guage pitfalls e.g. implicit information (𝖧𝖤𝗑21 ), ambiguity                There are potential threats to the internal and external
(𝖧𝖤𝗑50 ), and nuances (𝖧𝖤𝗑158 ). Using an LLM still of course           validity of our results. Internal threats could arise from
saves us from spending human effort. One may speculate                  our dataset where pre- and post-condition could be incor-
whether a solution with high test passing rate can be con-              rect, as they are prepared manually by us. Pre-conditions
sidered as ’almost good’, and is therefore valuable. For the            are typically simple and easy to check. Post-conditions are
above three cases, the ’almost good’ LLM solutions are                  checked via testing. Still, potential error cannot be altogether
actually quite well readable. Given the failing test cases,             excluded. Another threat is the fact that the test cases in
an experienced programmer can easily fix them. One might                our dataset may not be adequate for checking the correct-
then wonder: how hard would it be, more generally, to fix ’al-          ness of the generated contracts. To mitigate this threat we
most good’ LLM solutions? This would make an interesting                have augmented the manual tests through automated test
future work.                                                            generation, which indeed proved to be fundamental. We
    It is also worth noting that the discriminating tests men-          have used a newly constructed dataset with the objective
tioned in 𝖧𝖤𝗑21 and 𝖧𝖤𝗑50 were generated by Pynguin. This               of avoiding potential leakage from LLMs having already
suggests that augmentation with automated testing has a                 seen the dataset. Yet another threat is the non determinis-
key role to guard against LLMs susceptibility to language               tic responses from LLMs. We have repeated every LLM
subtleties. Human testers are prone to that as well, while a            prompting 10 times to account for this aspect, however a
tool like Pyguin is not.                                                larger number of repetitions may be necessary for a more

ThisisaPreprint                                                                                                          Page 16 of 18
                                                  Talk is Cheap, Logic is Hard

reliable results. Regarding external validity, we have used           For future research, we would like to look into spec-
24 proprietary and open models which are currently in use         ification generation for larger program units, e.g. classes.
both in research and practice, however a larger number could      Also, it is important to look into mechanisms to improve
increase confidence in the results. Finally, in our experiment,   incorrect proposals. We also believe that the sensitivity
the contracts generated are in Python, and results may be         towards language subtleties needs more in depth studies.
different for other programming languages.


9. Conclusion and Future Work
    We have evaluated 24 LLMs, seven of which are pro-            Data: a package with our data is available via Zenodo https:
prietary, on the task of formalizing contracts (full pre- and     //zenodo.org/records/17499683.
post-conditions) of programs, given their natural language
descriptions. A new dataset, called 𝖧𝖤𝗑, was used. On av-
erage, the proprietary LLMs performed significantly better        References
than the open LLMs, with the top five models being all            Beschastnikh, I., Brun, Y., Schneider, S., Sloan, M., Ernst, M.D., 2011.
                                                                     Leveraging existing instrumentation to automatically infer invariant-
proprietary. At the other end, the five lowest performing
                                                                     constrained models, in: 19th ACM SIGSOFT symposium and the 13th
LLMs are all open models. These LLMs produce a‘ high                 European conference on Foundations of software engineering.
number of erroneous/ill-formed proposals. This is not nec-        Bravo, E., 2023. Students’ Struggle with Mathematical Quantifiers and
essarily due to lower programming skill. We observed that            Assessment of Various Teaching Methodologies. Master’s thesis. Cal-
these LLMs struggle in interpreting the instructions in the          ifornia State University Channel Islands. URL: https://scholarworks.
                                                                     calstate.edu/concern/theses/dz010x690.
prompt. A better instruct-training may significantly improve
                                                                  Busch, P., accessed Sept. 2025. Poodle documentation. https://poodle.
their performances.                                                  readthedocs.io.
    Claude3.7 gave the best performance of 0.78 average           Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H.P., Kaplan,
accept@1 over combined pre- and post-conditions of all               J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R.,
problems in the dataset. The best performing open mod-               Krueger, G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B.,
                                                                     Gray, S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian, M.,
els are Gemma3 and Athene, with 0.47 average accept@1,
                                                                     Winter, C., Tillet, P., Such, F.P., Cummings, D., Plappert, M., Chantzis,
beating Claude3 and GPT3.5 proprietary models. Interest-             F., Barnes, E., Herbert-Voss, A., Guss, W.H., Nichol, A., Paino, A.,
ingly, Gemma3 ’only’ has 27B parameters, compared to e.g.            Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saunders, W.,
Athene or Llama3 with 70B parameters.                                Hesse, C., Carr, A.N., Leike, J., Achiam, J., Misra, V., Morikawa,
    Generally, the LLMs perform better on pre-condition              E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K.,
                                                                     Welinder, P., McGrew, B., Amodei, D., McCandlish, S., Sutskever, I.,
tasks. This is expected, as pre-conditions are typically less
                                                                     Zaremba, W., 2021. Evaluating large language models trained on code.
complex. None of the 24 LLMs can solve all pre- and post-            arXiv:2107.03374.
condition tasks (within the tried ten attempts). In particular,   Elyasov, A., Prasetya, I.W.B., Hage, J., 2013. Guided algebraic specification
generating correct contracts of difficulty 𝖭𝖰 is challenging         mining for failure simplification, in: IFIP Int. Conf. Testing Software and
for the LLMs. The good news is that the best performing              Systems ICTSS, Springer.
                                                                  Endres, M., Fakhoury, S., Chakraborty, S., Lahiri, S.K., 2024. Can large
LLMs are able to solve a higher number of 𝖭𝖰 tasks. The
                                                                     language models transform natural language intent into formal method
relatively low proportions of false positives and negatives          postconditions? Proceedings of the ACM on Software Engineering 1.
suggest that proposed solutions, while incorrect, might be        Ernst, M.D., Perkins, J.H., Guo, P.J., McCamant, S., Pacheco, C., Tschantz,
not too far from being correct. In some cases, they indeed           M.S., Xiao, C., 2007. The daikon system for dynamic detection of likely
can be easily fixed by a human programmer. Whether this              invariants. Science of computer programming 69.
                                                                  Faria, J.P., Trigo, E., Honorato, V., Abreu, R., 2026. Automatic generation
would hold more generally is beyond the scope of the current
                                                                     of formal specification and verification annotations using llms and test
study. This would be an interesting future work.                     oracles. arXiv preprint arXiv:2601.12845 .
    A good test suite is needed to validate LLM-generated         Feuerriegel, S., Hartmann, J., Janiesch, C., Zschech, P., 2024. Generative
contracts. Tests written by the developers themselves, even if       ai. Business & Information Systems Engineering 66.
they have full code coverage, while certainly useful, are also    Gerganov, G., 2023. llama.cpp: Inference of Llama Language Model. URL:
                                                                     https://github.com/ggerganov/llama.cpp.
often biased. Augmenting human tests with automatically
                                                                  Guan, B., Roosta, T., Passban, P., Rezagholizadeh, M., 2025. The order
generated tests were observed to be critical in rejecting            effect: Investigating prompt sensitivity in closed-source llms. arXiv
wrong contracts that would have otherwise been accepted.             preprint arXiv:2502.04134 .
    Closer inspections of selected cases reveal that LLMs         He, F., Zhai, J., Pan, M., 2024. Beyond code generation: Assessing code
are susceptible to language subtleties such as implicitness,         llm maturity with postconditions. arXiv preprint arXiv:2407.14118 .
                                                                  Hoare, C.A.R., 1969. An axiomatic basis for computer programming.
ambiguity, and nuances in the human-written program de-
                                                                     Communications of the ACM 12, 576–580.
scription, which is the source of their inference. They can       Leino, K.R.M., 2010. Dafny: An automatic program verifier for functional
propose contracts that look deceptively correct, but are ac-         correctness, in: International conference on logic for programming arti-
tually wrong. Again here, automated testing, which carry             ficial intelligence and reasoning, Springer. pp. 348–370.
no human bias, proved to be useful in differentiating such        Liu, J., Xia, C.S., Wang, Y., Zhang, L., 2023a. Evalplus leaderboard.
                                                                     https://evalplus.github.io/leaderboard.html.
proposals.
                                                                  Liu, J., Xia, C.S., Wang, Y., Zhang, L., 2023b. Is your code generated by
                                                                     chatGPT really correct? rigorous evaluation of large language models


ThisisaPreprint                                                                                                               Page 17 of 18
                                                               Talk is Cheap, Logic is Hard

   for code generation, in: Thirty-seventh Conference on Neural Infor-
   mation Processing Systems. URL: https://openreview.net/forum?id=
   1qvx610Cu7.
Lukasczyk, S., Kroiß, F., Fraser, G., 2020.             Automated unit test
   generation for python, in: Proceedings of the 12th Symposium on
   Search-based Software Engineering (SSBSE), Springer. doi:10.1007/
   978-3-030-59762-7\_2.
Ma, L., Liu, S., Li, Y., Xie, X., Bu, L., 2024. Specgen: Automated
   generation of formal program specifications via large language models.
   arXiv preprint arXiv:2401.08807 .
Mahmud Khandaker, S., Kifetew, F., Prandi, D., Susi, A., 2025. Aug-
   mentest: Enhancing tests with LLM-driven oracles. 18th IEEE Int. Conf.
   on Software Testing, Verification and Validation (ICST) .
Mariani, L., Pastore, F., 2008. Automated identification of failure causes in
   system logs, in: 19th International Symposium on Software Reliability
   Engineering (ISSRE), IEEE.
McCabe, T.J., 1976. A complexity measure. IEEE Transactions on software
   Engineering , 308–320.
Meyer, B., 1992. Applying design by contract. Computer 25, 40–51.
Nihad Zitouni, M., Anda, A.A., Rajpal, S., Amyot, D., Mylopoulos, J., 2024.
   Towards the llm-based generation of formal specifications from natural-
   language contracts: Early experiments with symboleo. arXiv .
Prasetya, I., Leek, C.Q., Oosenbrug, R., Kostic, P., De Vries, M., 2020. Can
   learning formal specification be fun?—experience and perspective, in:
   2020 IEEE International Conference on Software Testing, Verification
   and Validation Workshops (ICSTW), IEEE.
Radon, accessed 2025. Radon documentation. https://radon.readthedocs.
   io/.
Wei, Y., Furia, C.A., Kazmin, N., Meyer, B., 2011. Inferring better con-
   tracts, in: Proceedings of the 33rd International Conference on Software
   Engineering, pp. 191–200.
Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S.C., Tian,
   C., 2024. Enchanting program specification synthesis by large language
   models using static analysis and program verification, in: Int. Conf. on
   Computer Aided Verification, Springer.
Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac,
   P., Rault, T., Louf, R., Funtowicz, M., et al., 2020. Transformers:
   State-of-the-art natural language processing, in: Proceedings of the 2020
   conference on empirical methods in natural language processing: system
   demonstrations, pp. 38–45. https://huggingface.co/.
Xia, C.S., Zhang, L., 2023. Keep the Conversation Going: Fixing 162
   out of 337 bugs for $0.42 each using ChatGPT. arXiv preprint
   arXiv:2304.00385 .
Yang, L., Yang, C., Gao, S., Wang, W., Wang, B., Zhu, Q., Chu, X., Zhou,
   J., Liang, G., Wang, Q., et al., 2024. On the evaluation of large language
   models in unit test generation, in: Proceedings of the 39th IEEE/ACM
   International Conference on Automated Software Engineering.




ThisisaPreprint                                                                               Page 18 of 18
