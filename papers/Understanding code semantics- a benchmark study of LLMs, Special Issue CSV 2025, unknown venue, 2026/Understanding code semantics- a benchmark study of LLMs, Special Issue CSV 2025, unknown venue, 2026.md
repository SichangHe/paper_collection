International Journal on Software Tools for Technology Transfer (2026) 28:329–343
https://doi.org/10.1007/s10009-026-00842-4

    GENERAL

    Special Issue CSV 2025


Understanding code semantics: a benchmark study of
LLMs
Cosimo Laneve1 · Alvise Spanò2 · Dalila Ressi2 · Sabina Rossi2 · Michele Bugliesi2


Accepted: 20 February 2026 / Published online: 27 March 2026
© The Author(s) 2026


Abstract
We present an empirical study on the ability of Large Language Models (LLMs) to understand code by detecting semantically
equivalent and inequivalent programs, that is, whether they compute the same result given the same input or not. To
probe this, we deliberately perturb the program text by introducing semantics-preserving code transformations, namely
copy propagation and constant folding. Using a benchmark of 11 Python functions with both equivalent and non-equivalent
variants, we evaluate seven state-of-the-art LLMs (including ChatGPT, Claude, Gemini, and Deep-Seek) under zero-shot
prompting, with and without minimal context. Despite strong performance in code generation tasks, the models often fail in
this deeper reasoning challenge, misclassifying 41% of equivalent cases without context and 29% with context. Although
prompting can improve performance, it does not address the underlying limitations of the models. We argue that improving
LLMs themselves, through targeted ﬁne-tuning, contrastive learning on equivalent and nonequivalent implementations, or
training on transformation-invariant code, will be necessary for robust semantic understanding. Meanwhile, practitioners can
achieve better results by selecting stronger models, carefully engineering prom-pts, or writing code with tools that normalize
low-level diﬀerences before inference.

Keywords Large language models · Semantic preserving code transformations · Code understanding

1 Introduction                                                        optimize, and ﬁx programs, as well as for tasks such as vul-
                                                                      nerability detection and malware analysis.
                                                                         However, no thorough assessment appears to have been
Modern Large Language Models (LLMs) exhibit remark-
                                                                      conducted on their robustness in scenarios requiring a nu-
able capabilities in tasks related to programming, including
                                                                      anced semantics understanding of the code. While LLMs
code generation, comprehension, processing, and analysis
                                                                      excel at handling syntactic patterns, high-level semantics—
[4]. Tools like ChatGPT [23], GitHub Copilot [6], and Ama-            such as equivalence of functionally identical programs—is a
zon Q Developer [2] (previously known as CodeWhisperer)               fundamentally harder problem. In fact, while syntactic cor-
are widespread both in academy and industry to generate,              rectness and source-level transformations such as variable
                                                                      renaming or introduction of no-op instructions have been ex-
✉ C. Laneve                                                           plored to evaluate the robustness of LLMs [14, 25, 26], their
      cosimo.laneve@unibo.it
                                                                      ability to grasp program equivalence remains underexamined
      A. Spanò
      alvise.spano@unive.it
                                                                      when it comes to non-trivial semantic-preserving transfor-
                                                                      mations and more general semantic equivalence questions.
      D. Ressi
      dalila.ressi@unive.it                                              Semantic equivalence lies at the heart of a wide range
                                                                      of real-world software engineering tasks, including program
      S. Rossi
      sabina.rossi@unive.it                                           optimization, refactoring, plagiarism detection, and vulner-
      M. Bugliesi                                                     ability analysis [5]. A system that fails to recognize that two
      michele.bugliesi@unive.it                                       semantically identical programs behave the same may of-
                                                                      fer incorrect suggestions, overlook bugs, or fail to generalize
1     DISI, University of Bologna, Bologna, Italy                     learned patterns. Despite its importance, this form of reason-
2     DAIS, Ca’ Foscari University of Venice, Venezia Mestre, Italy   ing challenges LLMs due to the inﬁnite space of equivalent


                                                                                                                             Springer
330                                                                                                               C. Laneve et al.


programs and the undecidability of equivalence in the gen-        Claude proves to be the best performer, with average failure
eral case.                                                        rates of 19%, while Gemini is the worst, failing in 55% of the
   As the theoretical space of semantically equivalent pro-       cases. As a further experiment, we executed the same tests
grams is inﬁnite – and determining equivalence is undecid-        by adding to the prompt semantic-breaking perturbations. In-
able – we narrow our focus to a speciﬁc case of transforma-       terestingly, all LLMs performed better, somehow reinforcing
tions that guarantee identical outputs for identical inputs. In   the common insight that detecting a mistake is easier than
particular, we examine source-to-source transformations in-       proving correctness. In this case, the overall performance
spired by standard compiler-level optimizations that enhance      improves, yielding a 24% error rate with drops to only 18%
code performance: copy propagation and constant folding of        for the contextual prompt.
complex expressions [1].                                             Collectively, the reported results provide clear evidence
   Although these optimizations are well understood and           that LLMs are still far from robust for evaluating non-trivial
routinely applied by compilers, they pose a non-trivial chal-     transformations, even when conﬁned to speciﬁc, well-deﬁned
lenge to LLMs. Unlike humans or formal tools that rely            cases. The poor performance observed is likely due to insuf-
on symbolic reasoning, LLMs must infer equivalence from           ﬁcient training for the task, and additional training focused
learned statistical patterns. This disconnect makes such trans-   on semantically preserving code transformations is there-
formations an ideal testbed for evaluating whether LLMs           fore necessary for improvement. However, traditional train-
“understand” code at more than just the surface level.            ing methods would be slow and costly, as they would require
   Our assessment follows the methodology outlined below.         expert supervision to assess semantic equivalence across a
                                                                  vast code base, even for speciﬁc transformations like con-
1. First, we formalize copy propagation and constant folding
                                                                  stant folding. To lower both the learning curve and associated
   as source-level transformations for a subset of the Python
                                                                  costs, we advocate for integrating LLMs with automatic tools
   language. We target Python as widely adopted for model
                                                                  that implement code transformations, such as those proposed
   training and testing, and restrict to a subset to ease the
                                                                  in this paper. Such integration would serve two complemen-
   formalization of the transformations.
                                                                  tary purposes. First, it would make the tools available for
2. We collect a benchmark of non-trivial use cases, and code
                                                                  self-supervised training starting from the existing code base
   them in the chosen Python subset: the use cases include
                                                                  (simply, the tools would be employed to produce semantic
   classic general-purpose algorithms of which the LLMs
                                                                  equivalent transformations of the existing samples in the code
   are well aware, such as Fibonacci or Eratosthenes’ Sieve;
                                                                  base). Secondly, and more interestingly, they could be em-
   popular operations on arrays and lists typically found in
                                                                  ployed as general-purpose code pre-processors to eliminate
   libraries; and other more domain-speciﬁc algorithms such
                                                                  “noisy” bits, thus enhancing LLMs in their code understand-
   as anti-aliasing and type uniﬁcation.
                                                                  ing task.
3. We apply systematic perturbations to the source samples
   in the benchmark so that the original programs can be re-
                                                                  Paper structure       The rest of the paper is structured as
   covered by applying the source-level transformations of
                                                                  follows. Section 2 reports and discusses related works. Sec-
   interest. By analyzing whether the LLMs can correctly
                                                                  tion 3 presents in detail our methodology, namely the two
   judge the equivalence between the perturbed and original
                                                                  code transformations (copy propagation and constant fold-
   versions, we gain insight into their ability to reason about
                                                                  ing), the deﬁnition of the dataset and the prompts. Section 4
   code and detect deeper relationships than superﬁcial syn-
                                                                  reports our results and Sect. 5 discusses them, analyzing pos-
   tactic reorderings.
                                                                  sible solutions to improve reliability. We conclude in Sect. 6
4. We conduct our assessment on seven mainstream LLMs
                                                                  where we also present future work.
   evaluating their performance based on two classes of
   prompts. A ﬁrst, naive prompt simply asks to test the
   equivalence between the reference samples and their per-
                                                                  2 Related work
   turbed versions; a second, slightly reﬁned prompt informs
   the LLMs that the perturbations may be derived by ei-
                                                                  The integration of formal methods tools with Artiﬁcial In-
   ther copy propagation, constant folding, or combinations
                                                                  telligence techniques and Machine Learning (ML) models
   thereof, without further specifying the speciﬁc implemen-
                                                                  is an emerging practice in various domains [35], includ-
   tation of the transformations.
                                                                  ing data augmentation [24], dataset labeling [30], network
   Our ﬁndings reveal that LLMs are inaccurate in recog-          compression [27, 29], and security [28, 30]: formal meth-
nizing the perturbed, yet semantically equivalent, variants       ods provide a structured approach to deﬁning and validating
of programs in 41% of the cases when no context is pro-           semantic-preserving transformations, while Artiﬁcial Intel-
vided and in about 29% of the cases when given a simple           ligence techniques help enhance the scalability of the veriﬁ-
additional context. Among the diﬀerent models, Anthropic          cation processes.


Springer
Understanding code semantics: a benchmark study of LLMs                                                                      331


   LLM models are increasingly being evaluated in their           get programming language for our study. Its simplicity and
performance with code generation tasks. In particular, some       widespread adoption among developers make it a common
studies assess code generation and manipulation of Github         focus in model training, enabling eﬀective analysis and rea-
Copilot against selected fundamental algorithms such as sort-     soning. In the following subsection, we describe our tech-
ing and data structure implementation [7, 36]. Other works        niques for code perturbation, dataset construction, and the
aim to reduce the number of hallucinations (when LLMs             experimental setup.
generate conﬁdent-sounding, ﬂuent, yet factually incorrect,
nonsensical, or fabricated information not supported by their     3.1 Semantic-preserving code optimizations
training data or reality) related to coding tasks [21, 33].
   Our present focus is more directly related to the recent       As discussed in the introduction, we perturb Python code
stream of research work that investigates the performance of      in a way that requires nuanced semantic understanding. To
LLMS in code analysis and bug detection. In particular, the       ensure the correctness of these transformations, we lever-
results by [9, 11] align with our own ﬁndings, conﬁrming          age two well-known compiler techniques commonly used in
that even trivial modiﬁcations, such as variable renaming,        intermediate code optimization: copy propagation of vari-
can lead to performance degradation. On a diﬀerent, but still     ables and constant folding of expressions. To apply these
related account, [3] analyzes ML-based attacks on fully ho-       techniques at the source code level, we
momorphic encryption via side channels, using code trans-         (1) use annotations to record information about variables
formation techniques to show that unoptimized code hinders           (whether they are either constant values or copies);
such attacks.                                                     (2) bind annotations to every control point of the code (every
   However, to our knowledge, no prior work has system-              instruction) by means of a type inference system and a
atically analyzed the impact of ﬁne-grained optimizations            ﬁxpoint analysis;
such as the ones of our present interest. We should also men-     (3) simplify the code according to the information stored in
tion that the analysis itself is challenging as the evaluation       the annotations.
metrics depend on several factors, including both the vary-
ing prompting functionalities oﬀered by the models and the        The most technical aspect of this procedure is point (2),
often nuanced format of the responses [22].                       which operates as follows: (i) we deﬁne a set of rules that
   A key distinction in chatbot evaluation is between user        modify annotations based on their corresponding instruc-
prompts and system prompts [31]. User prompts do not re-          tions; (ii) starting with a program where each instruction has
quire the API and include basic prompting, zero or few-shot       an empty annotation, we iteratively infer annotations; (iii)
prompting, chain-of-thought prompting, and role-based or          the inference process continues until no further modiﬁca-
instruction-tuned prompting. System prompts, in turn, sup-        tions occur (i.e., a ﬁxpoint is reached); (iv) once the ﬁxpoint
port customization of behavior, max token limits, temper-         is reached, we proceed with the transformation step that sim-
ature setting, and further advanced features like function        pliﬁes the original program. For a formal deﬁnition of point
calling and logit bias, and streaming responses [31].             (2), we provide typing rules for a subset of Python statements
   Our assessment is based on user prompts rather than sys-       – suﬃcient to cover the codes in Sect. 4. The correctness of
tem prompts for two main reasons. Chatbot evaluation dis-         the overall process is beyond the scope of this paper; however,
tinguishes between user prompts and system prompts [31].          it can be proven using a similar approach to that presented
User prompts, which do not require API access, include            in [1] for corresponding optimization techniques applied to
various prompting techniques, while system prompts enable         intermediate code.
predeﬁned behaviors and advanced settings. We focus on                The two transformations are deﬁned below. We use the
user prompts for two reasons. Firstly, free-tier chatbots, like   following notations: given a Python program P, let Var(P)
ChatGPT, are widely used and reﬂect real-world interactions       be the set of variables of P (Var(·) also applies to statements
more accurately than open-source models like LLaMA [10],          𝑆, with the same meaning); if 𝑆 is either a statement or
Gemma [34], and Mixtral [17], which are primarily used            an expression, we write 𝑆{ 𝑦 / 𝑥 } the substitution of every
in research. Secondly, system prompts involve hidden pa-          occurrence of 𝑥 in 𝑆 with 𝑦 (we assume that 𝑥 and 𝑦 are not
rameters (e.g., temperature), making results less consistent.     redeﬁned in 𝑆, i.e., they are free).
Additionally, we employ a zero-shot approach [18], assessing
chatbots without providing prior context or examples.             3.1.1 Copy propagation

                                                                  The annotations of the copy propagation analysis are sets ℙ of
3 Methodology                                                     pairs (𝑥, 𝑦), with 𝑥, 𝑦 ∈ Var(P), that are closed by symmetry
                                                                  and transitivity. We always abbreviate {(𝑥, 𝑦), (𝑦, 𝑥)} with
To evaluate the ability of ML models to understand and            𝑥 ∼ 𝑦 whose meaning is “𝑥 and 𝑦 store the same value, i.e.,
manipulate source code, we selected Python as the tar-            they are copies”. Let


                                                                                                                         Springer
332                                                                                                                                          C. Laneve et al.


Table 1 Rewriting rules for                                [Asgn-CP]                [Id-CP]
                                                                                                                                             [Ids-CP]
Copy Propagation: they deﬁne                               𝐸 is not a variable                 𝑥≠𝑦
how to derive judgments of the                                                                                                ℙ⊢𝑥=𝑥▶ℙ
                                                           ℙ ⊢ 𝑥 = 𝐸 ▶ ℙ \ 𝑥 ℙ ⊢ 𝑥 = 𝑦 ▶ (ℙ \ 𝑥 ∪ { ( 𝑥, 𝑦) , ( 𝑦, 𝑥 ) } ) st
form ℙ ⊢ 𝑆 ▶ ℙ′ , which are
                                                           [If-CP]                                        [While-CP]
interpreted as follows: if the
statement 𝑆 is evaluated in a                                   ℙ ⊢ 𝑆 ▶ ℙ′      ℙ ⊢ 𝑆 ′ ▶ ℙ′′      ℙ ∩ ℙ′ ⊢ 𝑆 ▶ ℙ′
                                                                                     ′     ′  ′′
                                                           ℙ ⊢ i 𝑓 (𝐸 ) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ▶ ℙ ∩ ℙ ℙ ⊢ wℎ𝑖𝑙𝑒 (𝐸 ) : 𝑆 ▶ ℙ ∩ ℙ′
memory where the variables in
ℙ are copies, then its evaluation                          [For-CP]                                               [Seq-CP]
terminates in a memory where                                          ℙ ∩ ℙ′ \ 𝑖 ⊢ 𝑆 ▶ ℙ′          ℙ ⊢ 𝑆 ▶ ℙ′      ℙ′ ⊢ 𝑆 ′ ▶ ℙ′′
the variables in ℙ′ are also                                                                  ′
                                                           ℙ ⊢ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒 (𝐸 ) : 𝑆 ▶ ℙ ∩ ℙ \ 𝑖        ℙ ⊢ 𝑆 𝑆 ▶ ℙ′′
                                                                                                                 ′
copies                                                     [Def-CP]
                                                                                                    [Call-CP]
                                                                       ∅ ⊢ 𝑆 ▶ ℙ′
                                                                                                  ℙ ⊢ 𝑓 (𝑒1 , . . . , 𝑒𝑛 ) ▶ ℙ
                                                           ℙ ⊢ d𝑒 𝑓 𝑓 ( 𝑥1 , . . . , 𝑥𝑛 ) : 𝑆 ▶ ℙ



• ℙ \ 𝑥 = {(𝑦, 𝑧) ∈ ℙ | 𝑦 ≠ 𝑥 and 𝑧 ≠ 𝑥};
           def
                                                                       system in Table 1 corresponding to the three approximants
• ℙ ∩ ℙ′ = {(𝑥, 𝑦) | (𝑥, 𝑦) ∈ ℙ and (𝑥, 𝑦) ∈ ℙ′ };
         def
                                                                       in the Figure.
• ( 𝐴) is the closure of a set 𝐴 by symmetry and transitivity.
      st                                                                  We now illustrate in detail the code transformations ob-
                                                                       tained by applying the rules in Table 1. In these transforma-
   The inference system presented in Table 1 deﬁnes how
                                                                       tions, we adopt a slight abuse of notation by using semicolons
to derive judgments of the form ℙ ⊢ 𝑆 ▶ ℙ′ , which are inter-          to separate an assignment from its continuation. Speciﬁcally,
preted as follows: if the statement 𝑆 is evaluated in a memory         Python code of the form 𝑥 = 𝐸 𝑆 is written as 𝑥 = 𝐸 ; 𝑆. The
where the variables in ℙ are copies, then its evaluation termi-        code transformations induced by the copy propagation anal-
nates in a memory where the variables in ℙ′ are also copies.                                   CP
                                                                       ysis, denoted as =⇒, are as follows:
   We now brieﬂy describe the most relevant rules used to
derive the set of copies of a Python program P, as outlined            1. if ℙ ⊢ 𝑥 = 𝑦 ▶ ℙ′ with 𝑥 ∼ 𝑦 ⊆ ℙ then
in Table 1.
                                                                                                                        CP
   Rule [Asgn-CP] deﬁnes the annotation of an assignment                                                 𝑥=𝑦            =⇒        𝜀
to a variable 𝑥. In this case (𝐸 is not a variable), any copy
of 𝑥 is broken and must be removed from the set ℙ, hence                  (in this case ℙ = ℙ′ : we are erasing 𝑥 = 𝑦);
the conclusion ℙ \ 𝑥. Rule [Id-CP] destroys previous copies            2. if ℙ ⊢ 𝑥 = 𝑦 ▶ ℙ′ and ℙ′ ⊢ 𝑆 ▶ ℙ′′ , such that either (i) every
of 𝑥 and creates a copy with 𝑦 and with all the variables                 annotation in the proof of ℙ′ ⊢ 𝑆 ▶ ℙ′′ contains 𝑥 ∼ 𝑦 or (ii)
that are copies of 𝑦 in ℙ. Rule [While-CP] is the critical                𝑥 ∉ Var(𝑆), then
one. To determine the set ℙ′′ such that ℙ ⊢ wℎ𝑖𝑙𝑒 (𝐸) : 𝑆 ▶
                                                                                                                 CP
ℙ′′ we need an invariant: a set ℙ′ such that ℙ′ ⊢ 𝑆 ▶ ℙ′ .                                    𝑥=𝑦;𝑆             =⇒           𝑆{ 𝑦 / 𝑥 } ; 𝑥 = 𝑦
However, a generic set ℙ′ is not correct because we cannot
have more copies than those when the control reaches the ﬁrst          3. if ℙ ⊢ 𝑦 = 𝑒 ; 𝑆 ; 𝑥 = 𝑦 ▶ ℙ′ and 𝑥 ∼ 𝑦 ⊆ ℙ and 𝑥 ∉ Var(𝑆)
time the iteration. Hence the invariant becomes ℙ ∩ ℙ′ ⊢ 𝑆 ▶              then
ℙ′ and the conclusion of [While-CP] takes into account this                                              CP
invariant and the fact that the iteration may be not executed             𝑦=𝑒;𝑆;𝑥=𝑦                    =⇒
at all. Rule [For-CP] is similar to [While-CP]. Rules [Def-CP]                                                          𝑥 = 𝑒 ; 𝑆{ 𝑥 / 𝑦 } ; 𝑦 = 𝑥       (1)
and [Call-CP] deal with function deﬁnitions and invocations;
they assume that no access to global variables is possible.               (in this case 𝑥 ∼ 𝑦 ⊆ ℙ′ )
With this constraint, the judgments are pretty easy.                   4. if ℙ ⊢ wℎ𝑖𝑙𝑒 (𝑒) : (𝑆 ; 𝑥 = 𝑦) ▶ ℙ′ and (𝑥, 𝑦) ∈ ℙ and 𝑥 ∉
   The main diﬃculty of the system in Table 1 is determining              Var(S) then
the invariants in correspondence of iterations. There is a stan-
                                                                                                                   CP
dard way to solve this issue: starting with empty annotations,            wℎ𝑖𝑙𝑒 (𝑒) : (𝑆 ; 𝑥 = 𝑦)                =⇒
running the type systems several times until the annotations
                                                                                                                (wℎ𝑖𝑙𝑒 (𝑒{ 𝑦 / 𝑥 }) : 𝑆 ) ; 𝑥 = 𝑦        (2)
do not change anymore. This algorithm always terminates
(given a program, the corresponding sets ℙ are a ﬁnite lattice         5. if ℙ ⊢ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(𝑒) : (𝑆 ; 𝑥 = 𝑦) ▶ ℙ′ and 𝑥 ∼ 𝑦 ⊆ ℙ
and the iterations always return greater annotations). As an              and 𝑥 ∉ Var(𝑆) \ 𝑖 then
example, we apply the algorithm to a simple code printing
the factorial of a value taken in input, shown in Fig. 1. Here-                                                                    CP
                                                                          f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(𝑒) : (𝑆 ; 𝑥 = 𝑦)                         =⇒
after, we abbreviate ℙ ⊢ 𝑆 ▶ ℙ′ with 𝑆 ℙ, ℙ′ ). In this case,
the algorithm terminates after three applications of the type                                  (f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(𝑒{ 𝑦 / 𝑥 }) : 𝑆 ) ; 𝑥 = 𝑦                 (3)


Springer
Understanding code semantics: a benchmark study of LLMs                                                                       333


Fig. 1 Application of copy
propagation rules




Fig. 2 Annotations and transformations of copy propagation



For example, in Fig. 2, we show the code transformation of          or ⊤, where ⊤ represents a non-constant value, or ? that
our simple iterative program computing the factorial. At            represents an error. We use the following operations:
each step, we indicate the transformation rule that has been
                                                                    • ℂ \ 𝑥 = {(𝑦, 𝜇) ∈ ℂ | 𝑦 ≠ 𝑥};
                                                                           def
applied. In particular, in the ﬁrst step, we apply rule 3 when 𝑆
                                                                                  ⎧     if 𝜇 = 𝜇′
is empty. It is worth to notice that since every transformation                   ⎨𝜇
                                                                                  ⎪
                                                                                  ⎪
                                                                            ′
                                                                    • 𝜇⊔𝜇 = ⊤           if 𝜇 ≠ 𝜇′ and 𝜇, 𝜇′ ≠ ?
                                                                              def
step modiﬁes the program, the corresponding annotations                           ⎪
                                                                                  ⎪?    if 𝜇 = ? or 𝜇′ = ?
must also be updated. However, rerunning the inference sys-                       ⎩
tem at every step is not necessary; instead, annotation up-
                                                                                  ⎧
                                                                                  ⎪ {(𝑥, 𝜇 ⊔ 𝜇′ )} ∪ (ℂ \ 𝑥 ⊔ ℂ′ \ 𝑥)
dates can be incorporated directly within the transformation                      ⎪
                                                                                  ⎪
                                                                                  ⎪
                                                                                  ⎪            if (𝑥, 𝜇) ∈ ℂ and (𝑥, 𝜇′ ) ∈ ℂ′
steps. Finally, we notice that it is possible to use the standard                 ⎪
                                                                                  ⎪
                                                                                  ⎪
                                                                                  ⎪
garbage collection rule:                                                          ⎨ {(𝑥, 𝜇)} ∪ (ℂ \ 𝑥 ⊔ ℂ′ )
                                                                                  ⎪
                                                                    • ℂ ⊔ ℂ′ =
                                                                              def

   If P = 𝑆 ; 𝑥 = 𝑒 ; 𝑆 ′ and 𝑥 ∉ Var(𝑆 ′ ) then remove 𝑥 = 𝑒.                    ⎪            if (𝑥, 𝜇) ∈ ℂ and ℂ′ \ 𝑥 = ℂ′
                                                                                  ⎪
                                                                                  ⎪
For example, in the last code of Fig. 2, we can delete the                        ⎪
                                                                                  ⎪
                                                                                  ⎪
                                                                                  ⎪ {(𝑥, 𝜇′ )} ∪ (ℂ ⊔ ℂ′ \ 𝑥)
statement tmp = n.                                                                ⎪
                                                                                  ⎪
                                                                                  ⎪            if (𝑥, 𝜇′ ) ∈ ℂ′ and ℂ \ 𝑥 = ℂ
                                                                                  ⎩
3.1.2 Constant folding                                              • ⟦𝐸⟧ℂ that evaluates 𝐸 in the abstract memory ℂ; if some
                                                                      variable in 𝐸 has value ? in ℂ or has no value then the
The annotations for the constant folding are abstract memo-           result is ? (error); otherwise if some variable is ⊤ (and no
ries ℂ, which are sets of pairs (𝑥, 𝜇) where 𝑥 ∈ Var(P) (for          variable is ? or has no value in ℂ) then the overall result
some Python program P) and 𝜇 is either a constant value               is ⊤; otherwise the result is the value of 𝐸 when all the


                                                                                                                          Springer
334                                                                                                                                                          C. Laneve et al.


Table 2 Rewriting rules for                                           [Asgn-CF]                                  [If-CF]
Constant Folding: they deﬁne                                                         ⟦𝐸⟧ℂ = 𝜇                    ⟦𝐸⟧ℂ = ⊤            ℂ ⊢ 𝑆 ▶ ℂ′       ℂ ⊢ 𝑆 ′ ▶ ℂ′′
how to derive judgments of the
form ℂ ⊢ 𝑆 ▶ ℂ′ whose meaning                                         ℂ ⊢ 𝑥 = 𝐸 ▶ ℂ \ 𝑥 ∪ { ( 𝑥, 𝜇) }             ℂ ⊢ i 𝑓 (𝐸 ) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ ▶ ℂ′ ⊔ ℂ′′
is: if 𝑆 is evaluated in an abstract                                     [If-CF-t]                                    [If-CF-f]

memory where variables have                                                    ⟦𝐸⟧ℂ = true ℂ ⊢ 𝑆 ▶ ℂ′                      ⟦𝐸⟧ℂ = false         ℂ ⊢ 𝑆 ′ ▶ ℂ′′
the values stored in ℂ then its                                           ℂ ⊢ i 𝑓 (𝐸 ) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ ▶ ℂ′             ℂ ⊢ i 𝑓 (𝐸 ) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ ▶ ℂ′′
evaluation terminates with a                                      [While-CF]                                                 [While-CF-f]
memory whose variables have                                          ⟦𝐸⟧ℂ = 𝜇         𝜇 ≠ false   ℂ ⊔ ℂ′ ⊢ 𝑆 ▶ ℂ′             ⟦𝐸⟧ℂ = false ℂ ⊔ ℂ′ ⊢ 𝑆 ▶ ℂ′
the values stored in ℂ′
                                                                            ℂ ⊢ wℎ𝑖𝑙𝑒 (𝐸 ) : 𝑆 ▶ ℂ ⊔ ℂ′                             ℂ ⊢ wℎ𝑖𝑙𝑒 (𝐸 ) : 𝑆 ▶ ℂ
                                                           [For-CF]

                                                                           ⟦𝐸⟧ℂ = 𝜇        ( 𝜇 > 0 or 𝜇 = ⊤)                      [For-CF-f]

                                                                                                                                               ⟦𝐸⟧ℂ = k k ≤ 0
                                                                             ℂ ⊔ ℂ′ ⊔ { (𝑖, ⊤) } ⊢ 𝑆 ▶ ℂ′
                                                                                                                                  ℂ ⊢ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒 (𝐸 ) : 𝑆 ▶ ℂ
                                                           ℂ ⊢ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒 (𝐸 ) : 𝑆 ▶ ℂ ⊔ ℂ′ ⊔ { (𝑖, ⊤) }
                                                          [Seq-CF]                                [Def-CF]
                                                                                                                                                 [Call-CF]
                                                           ℂ ⊢ 𝑆 ▶ ℂ′ ℂ′ ⊢ 𝑆 ′ ▶ ℂ′′                         ⊤ ⊢ 𝑆 ▶ ℂ′
                                                                                                                                                 ℂ ⊢ 𝑓 (𝑒1 , . . . , 𝑒𝑛 ) ▶ ℂ
                                                                 ℂ ⊢ 𝑆 𝑆 ′ ▶ ℂ′′                  ℂ ⊢ d𝑒 𝑓 𝑓 ( 𝑥1 , . . . , 𝑥𝑛 ) : 𝑆 ▶ ℂ




Fig. 3 Application of constant folding rules (ℂ1 = { (n, ⊤) , (tmp, 1) , (m, 1) }, ℂ2 = { (n, ⊤) , (tmp, 2) , (m, 1) }, ℂ3 = { (n, ⊤), (tmp, 2) , (m, ⊤) },
ℂ4 = { (n, ⊤) , (tmp, 1) , (m, ⊤) })



  variables have been replaced by the corresponding values                             in this case, the algorithm terminates after three applications
  in ℂ (errors may occur at this stage as well, e.g. the division                      of the type system in Table 2.
  by 0 returns ?).                                                                         The inference system reported in Table 2) allows us to
   The judgments for the constant folding are ℂ ⊢ 𝑆 ▶ ℂ′ ,                             derive judgments of the form ℂ ⊢ 𝑆 ▶ ℂ′ whose meaning is:
meaning that, if 𝑆 is typed with an initial abstract memory                            if 𝑆 is evaluated in an abstract memory where variables have
ℂ, then its evaluation terminates with a memory whose vari-                            the values stored in ℂ then its evaluation terminates with a
ables have the values stored in ℂ′ . The rules for deriving                            memory whose variables have the values stored in ℂ′ . The
copies of a Python program P are written in Table 2. We                                topmost code in Fig. 4 reports the annotations we derive,
comment on rules [Asgn-CF] and [If-CF], as the explanations                            where we write 𝑆 ℂ, ℂ′ instead of ℂ ⊢ 𝑆 ▶ ℂ′ .
for the remaining rules closely follow those given for copy                                The pair (𝑥, k), where k is a constant, means that the
propagation.                                                                           variable 𝑥 has value k (in the memory); (𝑥, ⊤) means that
   Rule [Asgn-CF] updates the abstract memory ℂ by bind-                               the variable 𝑥 is undetermined (in the memory) – we are not
ing 𝑥 with the value ⟦𝐸⟧ℂ . Rule [If-CF] types conditionals                            able to determine its value at static time – or ? that represents
when the value of the guard is not determined. In this case                            an error.
the abstract memory after the conditional must include the                                 The transformation steps for the constant folding, denoted
results ℂ′ and ℂ′′ of the two branches (at static time we are                               CF
not aware of the branches that will be executed). Hence the                            as =⇒, use an auxiliary function ⟦𝐸⟧ℂ that, given an ex-
abstract memory ℂ′ ⊔ ℂ′′ is the conclusion.                                            pression 𝐸, evaluates 𝐸 in the abstract memory ℂ; if some
   Like the copy propagation analysis, the constant folding                            variable in 𝐸 has either no value or it is ? in ℂ then the
requires an iterative algorithm to determine the annotations.                          result is ? (error), otherwise (some variable is ⊤ in ℂ and
The algorithm starts with empty abstract memories. As an                               no variable is ?) the result is ⊤. We use expression contexts,
example, we apply the algorithm to a simple code printing                              written ℰ [ ], which are expressions with one hole [ ] in cor-
the factorial of a value taken in input, shown in Fig. 3. Also                         respondence of a sub-expression. For example 𝑥 + [ ] is an


Springer
Understanding code semantics: a benchmark study of LLMs                                                                                      335


                                                                       Table 3 Our dataset of Python programs. Green denotes general-
expression context. The steps are deﬁned by the following
                                                                       purpose classic algorithms; yellow marks notorious functions that are
four rules:                                                            typically found in libraries; red refers to algorithms that belong to spe-
                                                                       ciﬁc domains, such as computer graphics or compiler construction
1. if 𝑆 is either 𝑥 = ℰ [𝐸] or i 𝑓 (ℰ [𝐸]) : 𝑆 ′ e𝑙𝑠𝑒 : 𝑆 ′′
   or wℎ𝑖𝑙𝑒 (ℰ [𝐸]) : 𝑆 ′ or f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(ℰ [𝐸]) : 𝑆 ′
   or 𝑓 (· · · , ℰ [𝐸], . . .) and ℂ ⊢ 𝑆 ▶ ℂ′ with ⟦𝐸⟧ℂ = k and
   k ≠ ⊤ then 𝑆 may be rewritten as follows:
                                        CF
                         𝑥 = ℰ [𝐸] =⇒ 𝑥 = ℰ [k]
                                        CF
      i 𝑓 (ℰ [𝐸]) : 𝑆 ′ e𝑙𝑠𝑒 : 𝑆 ′′ =⇒ i 𝑓 (ℰ [k]) : 𝑆 ′ e𝑙𝑠𝑒 : 𝑆 ′′
                                        CF
              wℎ𝑖𝑙𝑒 (ℰ [𝐸]) : 𝑆 ′ =⇒ wℎ𝑖𝑙𝑒 (ℰ [k]) : 𝑆 ′
                                        CF
    f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(ℰ [𝐸]) : 𝑆 ′ =⇒ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(ℰ [k]) : 𝑆 ′         standalone functions implementing various algorithms, dif-
                                        CF
               𝑓 (· · · , ℰ [𝐸], . . .) =⇒ 𝑓 (· · · , ℰ [k], . . .)    fering in length, complexity, and notoriety. Some are general-
                                                                       purpose algorithms, such as Bubble Sort and the Sieve of Er-
2. if ℂ ⊢ 𝑥 = 𝐸 ▶ ℂ′ and ⟦𝐸⟧ℂ = k (k ≠ ⊤) and (𝑥, k) ∈ ℂ               atosthenes, while others, like type uniﬁcation and 3D point
   then                                                                rotation, are more domain-speciﬁc. The dataset includes both
                                             CF                        algorithms that manipulate data structures, such as lists and
                              𝑥 = 𝐸 =⇒ 𝜀                               arrays, and those performing mathematical computations,
                                                                       ensuring a diverse set of challenges. Table 3 provides an
   (remove the assignment);                                            overview of all included algorithms.
3. if ℂ ⊢ 𝑥 = 𝐸 ; 𝑆 ▶ ℂ′ and 𝑥 ∉ Var(𝑆) then                              Each algorithm in the dataset follows a structured design,
                                       CF                              with implementations grouped into two classes:
                      𝑥 = 𝐸 ; 𝑆 =⇒ 𝑆 ; 𝑥 = 𝐸
                                                                       • Correct Implementations (Semantically Equivalent):
   if ℂ ⊢ 𝑥 = 𝐸 ; 𝑥 = 𝐸 ′ ▶ ℂ′ and 𝑥 ∉ Var(𝐸 ′ ) then                    – One standard implementation serving as a reference.
                                                                         – Three perturbed versions that preserve the original se-
                                              CF                           mantics while applying simple transformations - copy
                    𝑥 = 𝐸 ; 𝑥 = 𝐸 ′ =⇒ 𝑥 = 𝐸 ′
                                                                           propagation, constant folding, and a combination of
4. if either ℂ ⊢ i 𝑓 (𝐸) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ ▶ ℂ′ or ℂ ⊢ wℎ𝑖𝑙𝑒 (𝐸) :            both. These transformations are reversible using stan-
   𝑆 ▶ ℂ′ or ℂ ⊢ f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(𝐸) : 𝑆 ▶ ℂ′ then                           dard optimization rules (see Sect. 3.1).
                                                                       • Incorrect Implementations (Semantically Non-
                                      CF                                 equivalent):
       i 𝑓 (𝐸) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ =⇒ 𝑆 (when ⟦𝐸⟧ℂ = true)
                                      CF
                                                                         – One version introducing a semantic-breaking bug in the
       i 𝑓 (𝐸) : 𝑆 e𝑙𝑠𝑒 : 𝑆 ′ =⇒ 𝑆 ′ (when ⟦𝐸⟧ℂ = false)                   reference implementation.
                                      CF
               wℎ𝑖𝑙𝑒 (𝐸) : 𝑆 =⇒ 𝜀 (when ⟦𝐸⟧ℂ = false)                    – Three additional versions derived from each of the per-
                                      CF                                   turbed correct implementations by introducing a bug.
    f𝑜𝑟 𝑖 i𝑛 r𝑎𝑛𝑔𝑒(𝐸) : 𝑆 =⇒ 𝜀 (when ⟦𝐸⟧ℂ = k
                                                                           These errors involve small but meaningful changes, such
                                and k ≤ 0)
                                                                           as index modiﬁcations or incorrect assignments, making
    In Fig. 4, we apply the constant folding transformations               them semantically incorrect.
to our simple iterative program computing the factorial.                  To further challenge model recognition, especially for
    In particular, in the ﬁrst step, we apply rule 1, thus comput-     domain-speciﬁc algorithms, we introduced a degree of ob-
ing all the constant subexpressions. As for copy propagation,          fuscation. Function names were anonymized, and variable
it is possible to collect garbage variables not used in the con-       identiﬁers were replaced with short, uninformative labels to
tinuations. Therefore, the assignment tmp = 1 in the last              prevent reliance on superﬁcial patterns.
code may be removed.                                                      The dataset is publicly available on GitHub [32]. Each
                                                                       source ﬁle contains one algorithm in the 8 variants, plus
3.2 Dataset construction                                               some extra code that puts the actual semantic equivalence
                                                                       to the test by performing unit tests for a reasonable range of
The dataset comprises multiple semantically equivalent and             inputs and comparing the outputs.
non-equivalent variants of small Python programs, designed
                                                                       3.3 Experimental setup
to assess the model’s ability to distinguish correct from in-
correct implementations. We crafted 11 distinct programs in            Our experiments involved collecting and analyzing responses
total, each available in 8 variants. These programs consist of         from several mainstream chatbots. We formulated our case


                                                                                                                                       Springer
336                                                                                                                  C. Laneve et al.




Fig. 4 Annotations and transformations of constant folding



study as a multi-instance binary classiﬁcation problem,
where both the reference implementation and its perturbed
variants were presented within the same prompt. For each
algorithm in the dataset, we designed four zero-shot prompts
as follows:




Prompt 1 (single-class, contextless): a contextless brief
 question, followed by the four correct versions of the al-
 gorithm (one reference and three perturbed);
Prompt 2 (single-class, contextual): a contextualized
 preamble, followed by the same four correct versions;
                                                                 Fig. 5 Diﬀerence between the preamble of the contextless and contex-
Prompt 3 (multi-class, contextless): Prompt 1 plus the four      tual prompts
 incorrect implementations, resulting in a total of eight code
 snippets that mix correct and incorrect versions;
Prompt 4 (multi-class, contextual): similar to Prompt 3, but     the chatbot distinguish between correct and incorrect imple-
 including the contextual preamble from Prompt 2.                mentations with no contextual support?” Unlike Prompt 1, it
   Prompt 1 is intended to ask: “Can the chatbot recognize       includes both valid and ﬂawed versions, requiring the model
correct implementations based solely on structure, without       to rely solely on its understanding of correctness. Prompt 4
contextual guidance?” It presents a brief, contextless ques-     combines this challenge with additional context, assessing
tion alongside four correct implementations—the reference        whether more information aids or complicates classiﬁcation.
and three perturbed versions—testing whether the chatbot            Each response to the prompts was carefully reviewed by
can assess correctness purely from code patterns. Prompt 2       two of the authors and framed as a binary multi-instance
adds background information to evaluate whether context im-      classiﬁcation problem. Speciﬁcally, each algorithm within a
proves classiﬁcation accuracy. Prompt 3 shifts focus to: “Can    prompt was compared to the ﬁrst function provided, which


Springer
Understanding code semantics: a benchmark study of LLMs                                                                           337


                                                                   Table 4 Chatbot models and versions involved in our experimentation
served as the reference to assess semantic equivalence. To
                                                                   as of January-February 2025. Experiments have been conducted at
evaluate the explanations produced by the chatbots, the two        various times of the day and over multiple weeks
reviewers manually inspected every single answer. Most
models followed a consistent structure: an initial binary judg-    Company                      Product             Model
ment (“yes” or “no”), a descriptive rationale, and a con-
                                                                   Github                       Copilot Pro         Claude 3.5 Sonnet
cluding summary table indicating which implementations
                                                                   Github                       Copilot Pro         GPT-4o
were considered equivalent to the reference. However, mod-
                                                                   Google                       Gemini              Gemini 2.0 Flash
els sometimes displayed internal inconsistencies, for exam-
                                                                   OpenAI                       ChatGPT             GPT-4o
ple, starting with an aﬃrmative answer, contradicting this
                                                                   DeepSeek                     DeepSeek            DeepSeek-R1 V3
position in the explanatory text, and then concluding with a
                                                                   Amazon Web Services          Q Developer         Various
negative assessment (or vice versa). In such cases, when the
                                                                   Anthropic                    Claude              Claude 3.5 Sonnet
narrative explanation was coherent with the ﬁnal summary
table, we disregarded the initial contradictory response and
considered the ﬁnal answer.                                           Table 4 lists the chatbots evaluated in our study together
   Particular attention was paid to contradictions, halluci-       with the model versions available at the time of testing. Pre-
nated justiﬁcations, or rapid shifts in stance that signaled       mium subscriptions are not included, with the sole exception
unstable reasoning. When a chat session exhibited persistent       of Copilot, which requires one. No APIs were used: all exper-
inconsistencies undermining the interpretability of the ex-        iments were carried out manually through the web interface
planation, the entire session was discarded and the prompt         when available, or via the free Visual Studio Code plugin
was resubmitted in a fresh chat. Importantly, no automated         when that was the only access point (as in the case of Copilot
post-processing or secondary LLM veriﬁcation was used: to          and Amazon Q). This choice is essential for our preliminary
avoid compounding model errors and to reﬂect the condi-            analysis, as we aim to assess chatbot performance under the
tions experienced by real users, the evaluation relied solely      same conditions experienced by the vast majority of casual
on human judgment.                                                 users. Admittedly, our choice partially undermines the re-
   The preamble or contextual priming at the beginning of          producibility and scalability of the results, mainly due to
the prompts follows two distinct formats, illustrated in Fig. 5.   how temperature is set by default in free-to-use versions of
Both preambles are zero-shot, as no labeled examples are           the models. Our goal, though, is to examine how the mod-
provided. The contextual preamble combines multiple strate-        els behave for casual users who typically do not possess
gies:                                                              premium licences and rely on freely accessible versions. In
                                                                   other words, while the authors are fully aware that most LLM
• Role prompting: “You are a chatbot for comparing the
                                                                   providers oﬀer more capable models through premium plans
  semantics of small Python programs.”
                                                                   and/or API usage, we intentionally focus on the baseline im-
• Instruction prompting: “I will provide you with multiple
                                                                   plementation, widely accessible to developers worldwide and
  implementations of the same Python function. The ﬁrst
                                                                   which does not oﬀer any control on the temperature setting,
  function is the reference version.”
                                                                   to probe the intrinsic quality of the models’ understanding.
• Contextual information: “The other functions are per-               It is worth mentioning that Copilot is not a model on its
  turbed with copy propagation, constant folding, or a com-        own, but it serves as a frontend for multiple models; our
  bination of the two.”                                            tests focus on two: ChatGPT and Claude Sonnet. Despite
   Each of the four prompts was repeatedly submitted to            using the same underlying technology as their standalone
seven chatbots over 10 rounds, with a new chat session             versions, results on Copilot diﬀer, warranting their inclusion
initialized for each iteration. This resulted in a total of        in our experiments. Similarly, Amazon Q reportedly employs
11 · 4 · 7 · 10 = 3, 080 outputs (11 Python programs, 4 prompts,   Claude 3.5 Sonnet,1 alongside custom models selected based
7 chatbots and 10 rounds of experiments). Chatbot responses        on the prompt type. However, both Amazon Q and Copilot
tend to be highly verbose. To encourage the models’ reason-        Claude yield results distinct from their oﬃcial counterparts.
ing process, we did not request a simple yes/no answer, as            Additionally, chat-based interaction prevents users from
we observed a performance drop in such cases. Each re-             adjusting the temperature parameter [8], which controls re-
sponse was carefully analyzed, taking into account potential       sponse variability. Typically ranging from 0 to 1, a tempera-
contradictions in the text and other logical inconsistencies.      ture of 0 ensures deterministic outputs, while higher values
Rather than post-processing the answers using an additional         1 As of February 2025, the Amazon Q Developer oﬃcial blog states
AI, this preliminary series of experiments relied on human         that Claude Sonnet is the primary model for code review and gen-
evaluation to mitigate the risk of misinterpreting verbose and     eration: https://aws.amazon.com/it/blogs/devops/amazon-q-developer-
complex outputs.                                                   inline-chat.


                                                                                                                              Springer
338                                                                                                                C. Laneve et al.


introduce randomness. Most chatbots default to 0.7, adjust-       as there is a degradation of about 3.5% on average in perfor-
ing dynamically, though the exact settings are not always dis-    mance between Prompt 2 and Prompt 4, with only ChatGPT
closed. Consequently, responses may vary across sessions,         seeming unaﬀected.
times, and even accounts. To account for this variability, our       Finally, we report the overall results of the multi-class
experiments were conducted across diﬀerent time frames and        prompts for both classes and the partial results. Interestingly,
conditions to ensure a fair sampling of model behavior.           Table 6 exhibits good results in detecting incorrect imple-
                                                                  mentations. In particular, if we compare the two tables, there
                                                                  is no real improvement between the contextless Prompt 3
4 Experimental results                                            and the contextual Prompt 4 concerning the class of incor-
                                                                  rect programs. However, this increase comes at the expense
Our evaluation is based on a total of 3,080 outputs generated     of the class of semantically equivalent programs. The exper-
by the seven chatbots under study. For the single-class setting   iments thus show that there is a classiﬁcation bias, where the
(Prompts 1 and 2), we manually analyzed 1,540 responses,          chatbots tend to misclassify correct perturbations when they
each addressing the semantic equivalence of the three pro-        are also provided with incorrect implementations.
gram variants. This yielded 4,620 ﬁne-grained yes/no judg-           Table 7 provides a detailed breakdown of the results for
ments. For the multi-class setting (Prompts 3 and 4), the re-     each type of code perturbation. For each of the 11 algo-
maining 1,540 responses each compared a reference program         rithms, the accuracy of all chatbots is reported across the
against seven variants, resulting in 10,780 yes/no judgments.     three perturbations: copy propagation (CP), constant folding
In total, we manually reviewed all 3,080 chatbot outputs and      (CF), and their combination (CP + CF). Claude Sonnet and
extracted 15,400 ﬁne-grained equivalence decisions. The ag-       DeepSeek once again stand out, achieving the highest perfor-
gregated results are presented in Tables 5 and 6.                 mances even on individual perturbation types. Conversely,
    Table 5 shows the accuracy of the class of semantically       Gemini performs worse than the other models overall. On
equivalent programs across all prompts for each chatbot.          average, constant folding is the least confusing perturbation
The rightmost column shows the average accuracy for each          for chatbots, yielding an accuracy of 76.40%. Copy propaga-
prompt across all chatbots. The bottom row represents the         tion appears more challenging, with an accuracy of 69.20%,
average for each chatbot across all prompts. Prompts 3 and        while the combination of both perturbations results in the
4 report the accuracy of the class of semantically equiva-        lowest accuracy, at 49.39%.
lent programs, despite including both correct and incorrect
code. At ﬁrst glance, Claude Sonnet and DeepSeek emerge
                                                                  5 Discussion
as the top performers, with Claude holding a slight edge
on average across all prompts (79.09% vs. 76.88%). Con-           Our investigation into the semantic equivalence of Python
versely, Gemini exhibits the lowest scores in most compart-       programs using Large Language Models (LLMs) has re-
ments (43.72% overall), followed somewhat unexpectedly by         vealed a number of intriguing behavioral patterns and in-
Copilot Claude (60.19%). Interestingly, despite both purport-     consistencies. Our observations highlighted the presence of
edly using Claude Sonnet, the model behind Copilot appears        contradictions, hallucinations, and limited understanding of
to behave diﬀerently from Anthropic’s implementation. The         certain coding patterns. Notably, the models occasionally
rest of the models fall in the middle range, with ChatGPT         contradict themselves during the evaluation process, stating
surprisingly not exceeding the average. It is clear that con-     something at the beginning of the output and landing on the
textual prompts, i.e., Prompts 2 and 4, enhance the accuracy      opposite conclusion by the end. For example, an initial aﬃr-
of all chatbots, with the notable exception of Gemini, whose      mative response regarding the equivalence of two functions
performance unexpectedly declines. The most signiﬁcant im-        is sometimes later followed by a retraction or a confusing
provement is observed in Copilot ChatGPT and Amazon Q,            double negative, a behavior that suggests a superﬁcial rather
which appear to beneﬁt greatly from contextual information.       than robust internal reasoning process. Furthermore, we ob-
Conversely, top-performing models such as DeepSeek and            served that in many cases, when models initially judged two
Claude Sonnet show only a minor accuracy gain.                    versions of a program to be non-equivalent (e.g., the “cp” and
    We also investigate the behavior of the chatbots when we      “cp+cf” perturbed versions), they later stated that the two
insert in the prompt both correct and incorrect perturbations     were equivalent. This ﬂip-ﬂopping not only highlights the
of the reference function (yellow and green rows). In this        internal instability of the models’ reasoning but also raises
case, we observe a signiﬁcant drop in performance compared        concerns about their ability to maintain logical consistency
to the single-class prompt (red and purple rows). Speciﬁcally,    across the whole output.
there is about an 8% drop in average performance between             Another intriguing observation concerns response ver-
Prompt 1 and Prompt 3, with DeepSeek being the only excep-        bosity. When we instructed models to be concise, their an-
tion. The same phenomenon happens when we add context,            swers were often more erroneous. Though not included in


Springer
Understanding code semantics: a benchmark study of LLMs                                                                                     339


Table 5 Performance of all chatbots on the class of semantically cor-    4 we report only the performance on the class of correct programs, i.e.
rect programs across all prompts. Prompts 1 and 2 contain only correct   those that are truly semantically equivalent. The best and worst perfor-
implementations. To ensure a fair comparison, for Prompt 3 and Prompt    mances are highlighted in bold




Table 6 Complete results on the classiﬁcation of both semantically correct and incorrect programs. A comparison is made between prompts with
and without contexts




our statistics, this suggests that extended outputs, reﬂecting               The Sieve of Eratosthenes serves as a particularly reveal-
the model’s chain of thought, play a crucial role in accurate            ing example. This algorithm combines arithmetic operations
reasoning. Limiting verbosity may truncate this process, in-             with list manipulation, yielding the lowest accuracy scores
creasing errors—a ﬁnding that merits further investigation               across all models. We argue that this poor performance stems
into the link between output length and reasoning quality in             from the modulus operation in the if-guard, which appears
program understanding.                                                   to confuse most LLMs in determining when the list removal
    Overall, copy propagation appears to be particularly chal-           operation takes place in the then-branch. The issue is fur-
lenging for most models, with the combination of copy prop-              ther exacerbated in perturbed versions of the code, where
agation and constant folding being the most problematic case.            the presence of copies ampliﬁes the confusion, as models
                                                                         struggle to distinguish between actual list copies and mere
A closer look at the data suggests this confusion becomes
                                                                         references.
more pronounced when non-numerical data types, such as
                                                                             Despite the obfuscation of function names, all models
lists and arrays, are involved. This is likely due to the models’
                                                                         rapidly recognized even lesser-known algorithms. Interest-
limited understanding of the subtle semantics of Python’s as-
                                                                         ingly, the antialiasing algorithm was frequently identiﬁed
signment operator, which behaves diﬀerently depending on                 as an “upscaling” technique, even though it also performs
the data type: numeric types are copied, whereas arrays and              downscaling to induce a blur eﬀect. In other words, none of
lists are merely aliased by reference. In other words, a state-          the tested models fully grasped the antialiasing algorithm’s
ment like B = A, where A is an array, results in a new binding           dual role – upscaling followed by downscaling – which con-
rather than an actual copy of A. This distinction appears to be          stitutes a hallmark of its functionality.
a common source of confusion among the tested models. No-                    Surprisingly, when tested on the 3D point rotation and
tably, only Claude Sonnet and Deepseek demonstrated some                 FFT algorithms, all models achieved a 100% success rate,
ability to diﬀerentiate between references and true copies in            suggesting that even less canonical snippets are well rep-
cases of variable rebinding.                                             resented in their extensive knowledge base. Conversely, the


                                                                                                                                       Springer
340                                                                                                                       C. Laneve et al.


 Table 7 Averaged results for each algorithm in the dataset and the corresponding semantically-preserving perturbations




uniﬁcation algorithm was consistently the least understood.              5.1 Improving LLMs in code understanding
This is likely due to the nature of the data structures involved:
                                                                         LLMs’ ability to understand code depends on the complex-
the algorithm computes a substitution – speciﬁcally, the Most
                                                                         ity of the chatbot’s model ecosystem, where models may
General Uniﬁer (MGU) – by performing pattern matching                    be dynamically selected based on the query type. For in-
over pairs of types. Substitutions are essentially dictionaries,         stance, ChatGPT appears to use diﬀerent models/extensions
while types are syntactic entities deﬁned through case-based             depending on whether the task involves text, images, or code
structures in an object-oriented manner. Such a use of classes           execution.
                                                                            To assess execution capabilities, we asked chatbots if they
appears to confuse chatbots, which seem better suited to un-             had direct access to a Python interpreter. All but two – Chat-
derstanding numerical algorithms, or those involving con-                GPT and Gemini – denied this ability. ChatGPT consistently
ventional data structures such as arrays and lists.                      conﬁrmed that it could execute Python code, although Ope-


Springer
Understanding code semantics: a benchmark study of LLMs                                                                    341


nAI provides no oﬃcial conﬁrmation. Gemini, on the other             Finally, the complexity of current chatbot ecosystems
hand, gave inconsistent answers, sometimes aﬃrming and            could readily accommodate the integration of static code
others denying interpreter access, suggesting variable be-        analysis or transformation pipelines behind the scenes. If
havior or conditional access.                                     chatbots incorporated a pre-processing phase that normalizes
   In general, techniques for improving performance on code       function implementations – using optimizations or rewrites
understanding tasks can be grouped into two categories:           like those described in Sect. 3.1 – they could help the model
those that modify the model itself, and those that improve        focus on the semantic content of the code rather than super-
how the model is used, without altering its parameters.           ﬁcial syntactic variation. This type of tool-assisted prepro-
   Model-level improvements involve adapting LLMs to rea-         cessing is especially attractive when retraining the model is
son more robustly about semantic equivalence.                     not feasible.
   Fine-tuning is a standard approach where a subset of              While these usage-level strategies do not improve the
model weights is updated using supervised datasets. This          model itself, they often yield substantial gains in practice
technique can also be applied to LLMs to change a small por-      and oﬀer a practical path forward for applications requiring
tion of the model [12, 19], for example, by using Parameter-      code understanding.
Eﬃcient Fine-Tuning (PEFT) methods such as Low-Rank
Adaptation (LoRA) or adapters. In our case, we could in-
vert the transformation rules outlined in Sect. 3.1 to generate   6 Conclusions
a dataset of semantically equivalent but syntactically varied
function implementations. Training on such pairs – both with      We analyzed LLMs’ code understanding by integrating in-
and without nonequivalent perturbations – could help mod-         sights from compiler design and advances in generative AI.
els learn invariance to superﬁcial code changes. Additionally,    To generate semantically equivalent code requiring nuanced
contrastive learning [15, 16] could be employed to shape the      comprehension, we employed standard compiler optimiza-
model’s internal representations, bringing equivalent code        tion techniques: copy propagation and constant folding. In
closer together and pushing non-equivalent code apart.            this preliminary study, we deﬁned optimization rules only for
   However, these model-level improvements require access         Python data types that exhibit call-by-value behaviour. Con-
to the model’s internal parameters and training procedures,       sequently, mutable structures such as lists and arrays, whose
which is typically limited for commercial LLMs (e.g., the full    operational semantics are eﬀectively call-by-reference, are
architecture for models of the GPT family is not disclosed).      excluded. Also, since these optimizations are typically de-
This limitation poses a signiﬁcant challenge for academic re-     ﬁned on control ﬂow graphs of intermediate representations,
search and practical adaptation, underscoring the importance      we adapted them to work directly at the source code level.
of collaboration between model developers and the research            Our experiments highlight both the strengths and limita-
community to enable specialized ﬁne-tuning for tasks like         tions of current LLMs in code understanding. While con-
code understanding.                                               textual prompting can improve performance in some cases,
   Usage-level improvements, on the other hand, focus on          it also reveals inconsistencies in logical reasoning. Results
leveraging existing models more eﬀectively. Prompting is          indicate that zero-shot contextless queries yield a 59% ac-
a commonly used and ﬂexible strategy [31]. Basic prompt-          curacy, while adding contextual information improves to a
ing involves direct instructions, while more advanced forms       71%. Despite a 12% increase, a 29% error rate is still too
such as few-shot prompting provide examples to guide the          high to broadly trust these models for code reasoning. We
model’s behavior. Chain-of-thought prompting, which en-           suggest that a code pre-processing tool integrated into the
courages the model to reason step-by-step through a problem,      LLM pipeline would improve program understanding by a
can notably improve performance on tasks requiring deeper         fair amount.
semantic understanding and logical reasoning [20]. Other              Future work should disentangle these eﬀects, reﬁning both
techniques – such as role-based prompting, where the model        LLM reasoning and evaluation methods for complex seman-
is asked to assume a speciﬁc persona (e.g., a compiler or         tic tasks. Further directions include expanding the dataset,
code reviewer), or instruction-tuned prompting using clearly      testing additional models, and exploring more advanced op-
structured commands – can also be used eﬀectively in stan-        timizations.
dard chatbot interfaces, without API access. These methods            While usage-level improvements such as prompting and
improve task-speciﬁc performance without modifying the            preprocessing can provide practical performance gains, our
underlying model.                                                 study underscores the necessity of adapting the LLMs them-
   Another widely used strategy is retrieval-augmented gen-       selves to robustly handle semantic code equivalence. Such
eration (RAG) [13], which enhances LLM outputs by inject-         model-level modiﬁcations, including ﬁne-tuning or con-
ing relevant context retrieved from an external source, such      trastive learning on semantically equivalent code, require
as similar code snippets or documentation.                        direct access to and control over the models’ parameters.


                                                                                                                       Springer
342                                                                                                                                   C. Laneve et al.


Given the proprietary nature of the commercial LLMs eval-                    10. Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Let-
uated here, only their owners can realistically implement                        man, A., Mathur, A., Schelten, A., Yang, A., Fan, A., et al.: The
                                                                                 llama 3 herd of models (2024). arXiv:2407.21783. arXiv preprint
these changes. This highlights a critical role for developers                11. Fang, C., Miao, N., Srivastav, S., Liu, J., Zhang, R., Fang, R.,
of large language models to facilitate or enable specialized                     Tsang, R., Nazari, N., Wang, H., Homayoun, H., et al.: Large
ﬁne-tuning and adaptation to advance code understanding                          language models for code analysis: do {LLMs} really do their
capabilities.                                                                    job? In: 33rd USENIX Security Symposium (USENIX Security,
                                                                                 vol. 24, pp. 829–846 (2024)
Acknowledgements This study was carried out within the
                                                                             12. Han, Z., Gao, C., Liu, J., Zhang, J., Zhang, S.Q.: Parameter-
                                                                                 eﬃcient ﬁne-tuning for large models: a comprehensive survey
PE0000014 - Security and Rights in the CyberSpace (SERICS) and
                                                                                 (2024). arXiv:2403.14608. arXiv preprint
received funding from the European Union Next-GenerationEU - Na-
                                                                             13. He, P., Wang, S., Chowdhury, S., Chen, T.H.: Evaluating the ef-
tional Recovery and Resilience Plan (NRRP) – MISSION 4 COM-
                                                                                 fectiveness and eﬃciency of demonstration retrievers in rag for
PONENT 2, INVESTIMENT 1.3 – CUP N. H73C22000890001. This
                                                                                 coding tasks. In: 2025 IEEE International Conference on Software
work has been also partially supported by the Research Project INDAM
                                                                                 Analysis, Evolution and Reengineering (SANER), pp. 500–510.
GNCS 2024 - CUP E53C23001670001 “Modelli composizionali per
                                                                                 IEEE, New York (2025)
l’analisi di sistemi reversibili distribuiti (MARVEL)” and by the Project
                                                                             14. Henkel, J., Ramakrishnan, G., Wang, Z., Albarghouthi, A., Jha,
PRIN 2020 - CUP N. 20202FCJMH “NiRvAna - Noninterference and
                                                                                 S., Reps, T.: Semantic robustness of models of source code. In:
Reversibility Analysis in Private Blockchains”. This manuscript reﬂects
                                                                                 2022 IEEE International Conference on Software Analysis, Evolu-
only the authors’ views and opinions, neither the European Union nor
                                                                                 tion and Reengineering (SANER), pp. 526–537. IEEE, New York
the European Commission can be considered responsible for them.
                                                                                 (2022)
                                                                             15. Hu, H., Wang, X., Zhang, Y., Chen, Q., Guan, Q.: A comprehen-
Funding information Open access funding provided by Alma Mater                   sive survey on contrastive learning. Neurocomputing 610, 128645
Studiorum - Università di Bologna within the CRUI-CARE Agreement.                (2024)
                                                                             16. Jaiswal, A., Babu, A.R., Zadeh, M.Z., Banerjee, D., Makedon,
Open Access This article is licensed under a Creative Commons At-                F.: A survey on contrastive self-supervised learning. Technologies
tribution 4.0 International License, which permits use, sharing, adap-           9(1), 2 (2020)
tation, distribution and reproduction in any medium or format, as long       17. Jiang, A.Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B.,
as you give appropriate credit to the original author(s) and the source,         Bamford, C., Chaplot, D.S., Casas, D.D.L., Hanna, E.B., Bres-
provide a link to the Creative Commons licence, and indicate if changes          sand, F., et al.: Mixtral of experts (2024). arXiv:2401.04088. arXiv
were made. The images or other third party material in this article are          preprint
included in the article’s Creative Commons licence, unless indicated         18. Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., Iwasawa, Y.: Large
otherwise in a credit line to the material. If material is not included in       language models are zero-shot reasoners. Adv. Neural Inf. Process.
the article’s Creative Commons licence and your intended use is not              Syst. 35, 22199–22213 (2022)
permitted by statutory regulation or exceeds the permitted use, you will     19. Latif, E., Zhai, X.: Fine-tuning chatgpt for automatic scoring. Com-
need to obtain permission directly from the copyright holder. To view a          put. Educ. Artif. Intell. 6, 100210 (2024)
copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.     20. Li, J., Li, G., Li, Y., Jin, Z.: Structured chain-of-thought prompting
                                                                                 for code generation. ACM Trans. Softw. Eng. Methodol. 34(2),
                                                                                 1–23 (2025)
                                                                             21. Liu, F., Liu, Y., Shi, L., Huang, H., Wang, R., Yang, Z., Zhang,
References                                                                       L., Li, Z., Ma, Y.: Exploring and evaluating hallucinations in
                                                                                 llm-powered code generation (2024). arXiv:2404.00971. arXiv
 1. Aho, A.V., Lam, M.S., Sethi, R., Ullman, J.D.: Compilers: Prin-              preprint
    ciples, Techniques, and Tools, 2nd edn. Addison Wesley, Boston,          22. Maroengsit, W., Piyakulpinyo, T., Phonyiam, K., Pongnumkul, S.,
    MA, USA (2006)                                                               Chaovalit, P., Theeramunkong, T.: A survey on evaluation methods
 2. Amazon website Services: Amazon q developer website, https://                for chatbots. In: Proceedings of the 2019 7th International Con-
    aws.amazon.com/it/q/developer/, accessed: 2025-02-21                         ference on Information and Education Technology, pp. 111–119
 3. Aydin, F., Aysu, A.: Leaking secrets in homomorphic encryption               (2019)
    with side-channel attacks. J. Cryptogr. Eng., 1–11 (2024)                23. OpenAI: Openai chatgpt website, https://openai.com/blog/chatgpt,
 4. Cao, Y., Li, S., Liu, Y., Yan, Z., Dai, Y., Yu, P.S., Sun, L.: A             accessed: 2025-02-21
    comprehensive survey of ai-generated content (aigc): a history of        24. Pellicer, L.F.A.O., Ferreira, T.M., Costa, A.H.R.: Data augmenta-
    generative ai from gan to chatgpt (2023). arXiv:2303.04226. arXiv            tion techniques in natural language processing. Appl. Soft Comput.
    preprint                                                                     132, 109803 (2023)
 5. Chandrasekaran, D., Mago, V.: Evolution of semantic similarity—          25. Pour, M.V., Li, Z., Ma, L., Hemmati, H.: A search-based testing
    a survey. ACM Comput. Surv. 54(2), 1–37 (2021)                               framework for deep neural networks of source code embedding.
 6. Chatgpt website. https://github.com/features/copilot, accessed:              In: 2021 14th IEEE Conference on Software Testing, Veriﬁcation
    2025-02-21                                                                   and Validation (ICST), pp. 36–46. IEEE, New York (2021)
 7. Dakhel, A.M., Majdinasab, V., Nikanjam, A., Khomh, F., Des-              26. Rabin, M.R.I., Alipour, M.A.: Evaluation of generalizability of
    marais, M.C., Jiang, Z.M.J.: Github copilot ai pair programmer:              neural program analyzers under semantic-preserving transforma-
    asset or liability? J. Syst. Softw. 203, 111734 (2023)                       tions (2020). arXiv:2004.07313. arXiv preprint
 8. Davis, J., Van Bulck, L., Durieux, B.N., Lindvall, C., et al.: The       27. Ressi, D., Romanello, R., Piazza, C., Rossi, S.: Neural networks
    temperature feature of chatgpt: modifying creativity for clinical            reduction via lumping. In: International Conference of the Italian
    research. JMIR Human Factors 11(1), e53559 (2024)                            Association for Artiﬁcial Intelligence, pp. 75–90. Springer, Berlin
 9. Dolcetti, G., Arceri, V., Iotti, E., Maﬀeis, S., Cortesi, A., Zaf-           (2022)
    fanella, E.: Helping llms improve code generation using feedback         28. Ressi, D., Romanello, R., Piazza, C., Rossi, S.: Ai-enhanced
    from testing and static analysis (2024). arXiv:2412.14841. arXiv             blockchain technology: a review of advancements and opportu-
    preprint                                                                     nities. J. Netw. Comput. Appl., 103858 (2024)


Springer
Understanding code semantics: a benchmark study of LLMs                                                                                           343


29. Ressi, D., Romanello, R., Rossi, S., Piazza, C.: Compressing neural         34th USENIX Security Symposium (USENIX Security, vol. 25,
    networks via formal methods. Neural Netw., 106411 (2024)                    pp. 3687–3706 (2025)
30. Ressi, D., Spanò, A., Benetollo, L., Piazza, C., Bugliesi, M., Rossi,   34. Team, G., Mesnard, T., Hardin, C., Dadashi, R., Bhupatiraju, S.,
    S.: Vulnerability detection in Ethereum smart contracts via ma-             Pathak, S., Sifre, L., Rivière, M., Kale, M.S., Love, J., et al.:
    chine learning: a qualitative analysis (2024). arXiv:2407.18639.            Gemma: Open models based on Gemini research and technology
    arXiv preprint                                                              (2024). arXiv preprint. arXiv:2403.08295
31. Sahoo, P., Singh, A.K., Saha, S., Jain, V., Mondal, S., Chadha,         35. Urban, C., Miné, A.: A review of formal methods applied to ma-
    A.: A systematic survey of prompt engineering in large language             chine learning (2021). arXiv:2104.02466. arXiv preprint
    models: Techniques and applications (2024). arXiv preprint. arXiv:      36. Wermelinger, M.: Using github copilot to solve simple program-
    2402.07927                                                                  ming problems. In: Proceedings of the 54th ACM Technical Sym-
32. Spanò, A.: Github repository. https://github.com/alvisespano/               posium on Computer Science Education V, vol. 1, pp. 172–178
    perturb                                                                     (2023)
33. Spracklen, J., Wijewickrama, R., Sakib, A.N., Maiti, A.,
    Viswanath, B.: We have a package for you! A comprehensive anal-         Publisher’s note Springer Nature remains neutral with regard to ju-
    ysis of package hallucinations by code generating {LLMs}. In:           risdictional claims in published maps and institutional aﬃliations.




                                                                                                                                          Springer
