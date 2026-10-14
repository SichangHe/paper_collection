                                         Natural Language Translation of Formal Proofs through Informalization of
                                             Proof Steps and Recursive Summarization along Proof Structure

                                                         Seiji Hattrori1 Takuya Matsuzaki1 Makoto Fujiwara1
                                                                      1
                                                                        Tokyo University of Science
                                             1424521@ed.tus.ac.jp matuzaki@rs.tus.ac.jp makotofujiwara@rs.tus.ac.jp



                                                               Abstract                          training. Consequently, its target remains primarily
                                                                                                 on high school level mathematics, such as miniF2F
                                             This paper proposes a natural language trans-
arXiv:2509.09726v1 [cs.CL] 10 Sep 2025




                                                                                                 (Zheng et al., 2022), where the emphasis is on arith-
                                             lation method for machine-verifiable formal
                                             proofs that leverages the informalization (ver-
                                                                                                 metic operations rather than mathematical reason-
                                             balization of formal language proof steps) and      ing.
                                             summarization capabilities of LLMs. For eval-          This paper proposes an auto-informalization
                                             uation, it was applied to formal proof data cre-    method that translates formal proofs into natural
                                             ated in accordance with natural language proofs     language proofs, addressing the challenge of lim-
                                             taken from an undergraduate-level textbook,         ited training data for autoformalization. To achieve
                                             and the quality of the generated natural lan-       this, we need to solve the following challenges:
                                             guage proofs was analyzed in comparison with
                                                                                                 Generation of Natural Reference Expression
                                             the original natural language proofs. Further-
                                             more, we will demonstrate that this method can      Mathematical proofs frequently refer to predefined
                                             output highly readable and accurate natural lan-    concepts, theorems, and assumptions made in the
                                             guage proofs by applying it to existing formal      course of a proof. In formal proofs, these ref-
                                             proof library of the Lean proof assistant.          erences are made using arbitrarily named labels.
                                                                                                 However, simply using these labels during transla-
                                                                                                 tion cannot produce natural reference expressions
                                         1   Introduction
                                                                                                 as those written by humans.
                                         Mathematical proofs written in a formal language        Abstraction to Human-Readable Proofs It is pos-
                                         that computers can verify are known as formal           sible to mechanically translate each piece of a for-
                                         proofs. These are primarily written in languages        mal proof into corresponding natural language ex-
                                         used by theorem proving assistants such as Isabelle     pression, as all operations in formal language have
                                         (Paulson, 1990), Rocq (Bertot and Castéran, 2004),      clear meanings. However, a natural language proof
                                         and Lean (de Moura et al., 2015).                       constructed by mechanically translating and con-
                                            Autoformalization is a technology that automat-      catenating individual pieces often results in an un-
                                         ically converts human-written proofs (natural lan-      natural and incomprehensible output. To achieve
                                         guage proofs) into formal proofs. It reduces the        a natural translation, it is essential to include in-
                                         burden of manually formalizing mathematical the-        formation that is both necessary and sufficient for
                                         orems. Moreover, in the domain of natural lan-          human readers by an appropriate abstraction.
                                         guage theorem proving using large language mod-            To tackle the above problems, we combine the
                                         els (LLMs) (e.g., Jiang et al., 2023, Zhang et al.,     following three components:
                                         2025a, Xin et al., 2025), autoformalization enables     Construction of a Premise Library Our method
                                         us to programmatically verify the logical validity      performs translation using a premise library,
                                         of generated content, thereby contributing to the       which is created by converting definitions and
                                         improvement of automated theorem provers.               propositions within a formal mathematics library
                                            In recent years, with the advancement of LLMs,       (Mathlib) into natural language descriptions in
                                         research into autformalization as a machine trans-      advance. These descriptions are included in the
                                         lation task has become active (e.g., Li et al., 2024;   prompt for step-wise informalization to encourage
                                         Tarrach et al., 2024; Zhang et al., 2025b). However,    the generation of natural reference expressions.
                                         challenges persist due to the lack of natural lan-      Step-wise Informalization Each step of a formal
                                         guage proofs paired with formal proofs for model        proof (consisting of commands called tactics) is
                                         Figure 1: Method Overview


translated into a natural language proof step. It        targets only formal propositions, whereas our re-
is generated by a hybrid method that combines a          search focuses on formal proofs.
rule-based approach using templates prepared for            Although prior work such as Chester (1976) and
each tactic type, and slot-filling by an LLM that        Holland-Minkley et al. (1999) has addressed the
extracts corresponding information based on slot         translation of formal proofs into natural language
types that specify the content to be included.           proofs, there has been relatively little research on
Summarization of Proof Steps We generate a nat-          approaches that utilize LLMs. Gao et al. (2025)
ural language proof by progressively summarizing         proposed a method for constructing high-quality
the description of the proof steps, reflecting the       paired datasets of formal and natural language
structure of the formal proof.                           proofs. Their approach uses static analysis tools to
   The generated natural language proofs must ac-        extract information such as code comments, simi-
curately reflect the logical structure expressed in      lar propositions, and dependent propositions from
the formal proofs, and furthermore, must correctly       Lean’s formal proof library, and then provides this
capture the essential points of the proof to avoid       information to the LLM as auxiliary input to facil-
logical leaps or breakdowns. To evaluate this, we        itate the translation of formal proofs. In addition,
prepared formal proof data by formalizing uni-           they aim for high-quality step-wise informalization
versity undergraduate-level mathematical proofs,         and natural language proof generation by manu-
maintaining their proof structure as much as pos-        ally creating explanatory sentences for each tac-
sible. We then applied the proposed method to            tic’s logical structure and incorporating them into
this data and compared the generated output with         the prompt, thereby helping the LLM capture the
the original natural language proofs to conduct a        relationship between proof steps and goals.
detailed evaluation. Additionally, we will present          While our method is inspired by theirs, it differs
conversion examples for Mathlib proofs, which do         in two ways. First, instead of guiding the LLM with
not have corresponding natural language proofs,          explanatory text, we directly control the form of
to demonstrate that high quality natural language        step-wise informalization by applying rule-based
proofs can be generated.                                 template generation. Second, whereas their method
                                                         generates natural language proofs by concatenating
2   Related Work                                         step-wise results, our approach recursively summa-
This section introduces several recent studies on        rizes these results according to the structure of the
autoformalization and informalization that are par-      formal proof, producing text that is more readable
ticularly relevant to our research.                      and closer in style to human-written proofs.
   Jiang et al. (2024) proposed a method to con-
                                                         3   Theorem Proving Assistant
struct a large-scale dataset of pairs of formal propo-
sition and natural language proposition by informal-     A theorem proving assistant refers to software that
izing formal propositions written in Isabelle and        provides a formal language for writing mathemati-
Lean using GPT-4. While our proposed method              cal proofs and an automated verification system for
also involves prompt-based informalization, it dif-      proofs written using that formal language.
fers from Jiang et al.’s approach in that their method     Lean (de Moura et al., 2015) is one such proof
1   theorem EvenAddEvenEqEven (a : N) (b : N) :                hypotheses remain the same. The subsequent three
2     (Even a ∧ Even b) → Even (a + b) := by                   rw tactics (line 5-8) rewrite on the proof goal using
3     intro ⟨⟨r1, h1⟩ , ⟨r2, h2⟩⟩                              the propositions in the library and hypotheses. The
4     have : a + b = (r1 + r2) + (r1 + r2) :=
        by                                                     first tactic rewrites (r1+r2)+(r1+r2) to r1+r1+
5       rw [Nat.add_assoc , Nat.add_comm r2,                   r2+r2 using the commutative and associative laws
6          ← Nat.add_assoc , ← Nat.add_assoc]                  of addition. The next tactic rewrites a+b on the left-
7       rw [h1, h2]
8       rw [← Nat.add_assoc]                                   hand side of the goal using the two hypotheses h1
9     exact ⟨(r1 + r2), this⟩                                  and h2 introduced by the intro tactic, and finally,
                                                               by again using the associative law of addition, the
    Figure 2: Formal proof of "the sum of two even numbers     left and right sides of the goal are made to have
    is an even number"                                         the same form, completing the proof of the sub-
                                                               proposition.
                                                                  Finally, the proof of the initially declared propo-
    assistant, offering a functional programming lan-          sition is completed using the exact tactic (line 9).
    guage based on dependent type theory. Similarly to         Here, r = r1 + r2 is provided as evidence that
    Rocq and Isabelle, Lean provides interactive proof         a + b is even, thus completing the proof. Note that
    assistance through commands called "tactics." Fur-         this given in the exact tactic refers to the propo-
    thermore, formal proofs can be created efficiently         sition declared with the have command, which in
    by leveraging Mathlib, a formal proof library built        this case refers to a + b = (r1 + r2) + (r1 + r2).
    on Lean by its user community.                                In Lean, propositions are thus proven by repeat-
       We use Lean 4 and Mathlib4, released in 2021            edly applying tactics and changing the state of the
    for the implementation of the proposed method and          proof, i.e., the goal proposition and the established
    the creation of few-shot examples.                         hypotheses.
       We explain the gist of Lean’s formal proof using
    the proposition "the sum of two even numbers is            4     Method
    an even number" and its proof. A proof of this       Our proposed method translates formal proofs writ-
    proposition is given as follows:                     ten in Lean 4 syntax into natural language proofs
                                                       
                                                         through five stages: off-line generation of premise
     If a and b are even numbers, then there exist some  library (4.1), information extraction (4.2), step-
     r1 , r2 such that
                   a = r 1 + r 1 , b = r2 + r 2 .        wise informalization (4.3), dependency structure
    This means that                                      analysis (4.4), and summarization (4.5). Figure 1
                a + b = (r1 + r2 ) + (r1 + r2 ).         provides an overview of the method.
    Therefore, a + b is also an even number.
                                                            4.1     Construction of Premise Library
    Figure 2 presents a formalization of this proof. In
                                                               The premise library contains explanatory sentences
    a Lean formal proof, we first declare a proposition
                                                               for all theorems and definitions defined within Lean
    to prove using the theorem command. In Figure 2,
                                                               and Mathlib. This library is generated using the
    it is declared that for any natural numbers a, b, if a
                                                               following procedure:
    and b are even, then a + b is also even (line 1-2).
    Next, we introduce variables and hypotheses using              1. Information Extraction
    the intro tactic (line 3). Since even numbers are                 All theorems and definitions are extracted
    defined as Even x ⇔ ∃r. x = r + r, the following                  from Lean and Mathlib source codes (mod-
    hypotheses are introduced:                                        ules).
        r1 r2 : N,
        h1 : a = r1 + r1, and                                      2. Dependency Analysis
        h2 : b = r2 + r2.                                             Based on the list of modules imported by each
    The proof goal then becomes to prove Even (a                      module, the dependencies between modules
    + b). We then declare a sub-proposition to be                     are expressed in terms of levels. The level
    proven using the have tactic (line 4), namely that                value of each module indicates that it may
    a + b = (r1 + r2) + (r1 + r2). Then, the proof                    depend on modules with smaller level values
    goal temporarily changes from Even (a + b) to                     and does not depend on modules with larger
    a + b = (r1 + r2) + (r1 + r2), while the                          level values.
  3. Explanation Generation
     Starting from modules with smallest level val-
     ues, an LLM is prompted to generate explana-
     tory sentences for the theorems and defini-
     tions defined in that module. If a theorem
     or a definition depends on another definition,
     and its explanation is already available, the
     explanation is provided in the prompt. As
     few-shot examples, three other definitions and
     theorems belonging to the same module or the
     same field (e.g., linear algebra) are randomly
     selected and provided.

   For example, for the theorem representing the
triangle inequality of absolute values (|a + b| ≤
|a| + |b|), the output would be: “This theorem
states that in a linearly ordered additive group, the
absolute value of the sum of the two elements is less
than or equal to the sum of their absolute values,
embodying the triangle inequality.”
   This library is used in the subsequent informal-
ization (4.3) and summarization (4.5) steps.

4.2   Formal Proof Information Extraction                      Figure 3: Informalize task input example
Various pieces of information from the Lean formal
proof data are extracted for use in informalization,
                                                           We first extract a tactic applied in a proof step
dependency structure analysis, and summarization
                                                        from the tactic information, as well as the proof
steps. We extend LeanDojo (Yang et al., 2023)’s
                                                        state before and after its application (all expressed
data extraction tool and use it for this purpose. We
                                                        in the form of hypotheses ⊢ goal).
extract three types of data:
                                                           Next, an appropriate generation template is re-
   • Tactic Information holds the type and the          trieved. One or more template are manually pre-
     arguments of each tactic applied in a formal       pared for each tactic; each template corresponds to
     proof and the changes in the proof state before    different usage of the tactic.
     and after the tactic’s application.                   Let’s take the rw tactic used in lines 5 and 7
                                                        of Figure 2 as an example. In the case of the
   • Premise Information contains information           rw tactic, templates are differentiated by whether
     such as the names and types of theorems and        it rewrites the goal, an existing hypothesis, or
     definitions referenced in the formal proof.        both, and whether the rewriting uses only hy-
                                                        potheses, only theorems, or both hypotheses and
   • Abstract Syntax Tree (AST) represents the
                                                        theorems. The rw tactic on line 5 rewrites the
     dependencies between tactics, variables, and
                                                        proof goal using two theorems, Nat.add_assoc
     other elements contained in a formal proof.
                                                        and Nat.add_comm. The rw tactic on line 7 rewrites
     We obtain it from the internal data structure
                                                        the proof goal using two previously introduced hy-
     of the Lean system.
                                                        potheses, h1 and h2. The template retrieval algo-
4.3   Informalization of each proof step                rithm uses this information to proceed through the
                                                        template branches and select the most appropriate
Using the tactic information and premise informa-
                                                        template. In this example, the following templates
tion extracted in the previous step, we generate
                                                        are selected respectively for the two rw tactics:
explanatory sentences for the operations of each                                                                       
proof step in a formal proof by using an LLM. The         By using [theorems], [goalsBefore] becomes [goalsAfter].
main part of the prompt used is shown in Figure 3         By using [assumptions], [goalsBefore] becomes [goalsAfter].
and the full prompt is shown in Appendix B.                                                                            
The templates include several slots, such as [the-
orems], [assumptions], [goalsBefore], and [goal-
sAfter]. The LLM is instructed to fill these slots
so that they explain "theorems used during tactic
application," "assumptions used during tactic appli-
cation," "the proof goal before tactic application,"
and "the proof goal after tactic application," respec-
tively. These explanations of the slots are provided
in the informalization prompt along with the tem-
plate itself.                                                   Figure 4: Dependencies among proof steps
   Next, explanatory sentences corresponding to
the theorems and definitions used in the applied
                                                          for the proof steps of that proposition become the
tactic are retrieved from the premise library. For
                                                          children of the proof step that declares the interme-
instance, in line 5 of Figure 2, which uses rw
                                                          diate goal.
[Nat.add_assoc, Nat.add_comm r2, ...],
two theorems are used: Nat.add_assoc and                     Figure 4 shows an example of the tree struc-
Nat.add_comm. Therefore, the premise library is           ture. It represents the structure of the formal proof
searched based on the modules where these theo-           shown in Figure 2. Here, four types of tactics are
rems are defined, and their respective explanatory        used: intro, have, rw, and exact. Of these, the
sentences are retrieved.                                  three rw tactics are used to prove the intermediate
   Next, few-shot examples of the step-wise infor-        goal declared by the have tactic. Therefore, the
malization are obtained from a manually created           dependency structure is represented by a subtree
list. Few-shot examples are created for each type of      where the explanation sentence for the have tactic
tactic operation defined in Lean and Mathlib. Each        is the root, and the explanation sentences for the
example consists of the applied tactic, the proof         three rw tactics are the leaves.
state before and after its application, and the result-
                                                          4.5   Summarization of Informalized Steps
ing operation explanation sentence. The tactic and
proof state of the few-shot examples are extracted        In this step, we leverage the dependency structure
from self-created formal proofs and Mathlib formal        tree constructed in the previous step to summarize
proofs. The corresponding output examples were            the operation explanations of all proof steps into a
all manually created with the intention of being          single proof.
natural as sentences included in a proof and clearly         First, we use an LLM to informalize the proposi-
indicating to the LLM what operation the given            tion to be proven (the proposition declared at the
tactic corresponds to and which part of the proof         beginning of the formal proof), which is the root of
state to focus on for output. The formats of the          a tree structure. For this informalization generation,
example sentences adhere to one of the templates.         we use a different prompt than the one employed
   Finally, the information obtained through the          in 4.3, including three manually created few-shot
preceding steps is provided to the LLM along with         examples, and explanations of definitions used in
a prompt, and natural language explanations corre-        the proposition.
sponding to each proof step are generated.                   Next, to generate a natural language proof that
                                                          aligns with the structure of the formal proof, we
4.4   Dependency Analysis of Proof Steps                  generate a sub-proof for each subtree in the tree
In this step, we analyze the dependencies between         structure. A sub-proof is the natural language proof
tactics using the abstract syntax tree extracted in 4.2   of an intermediate goal declared by the tactic at the
and associate the operation explanation sentences         root of a subtree, and its content is created from
corresponding to each proof step to the nodes of          the operation explanation sentences correspond-
the tree structure that expresses these dependencies.     ing to the nodes of the subtree. Furthermore, the
This tree structure has the proposition being proven      sub-proofs are recursively generated. That is, if a
as its root and the explanation sentences of each         subtree contains further subtrees, the sub-proofs
proof step as its descendants. Furthermore, when          of the contained subtrees are generated first, and
proving an intermediate goal in a proof (declared         they are summarized to the sub-proof of the origi-
by tactics such as have), the explanation sentences       nal subtree. This process is repeated until we get a
                                                              
                                                                     sions and operations appearing in the text cor-
    Require: Informalization result of proof step s                  rectly reflect the content of the proof step.
      if s contains output written in formal language syntax
      then
           return "Untranslated Expression"                        • Sufficiency of Included Information
      else if s contains logical/content errors then                 Evaluates whether the generated explanation
           return "Misinformation"                                   sufficiently contains the necessary informa-
      else if s is unclear/lacks sufficient information then
           return "Insufficient Information"                         tion to describe the proof step.
      else if s contains redundant/inappropriate expressions
              for an explanation then                              • Necessity of Included Information
           return "Unnecessary Mention"                              Evaluates whether the explanation contains
      else
           return "Correct"
                                                                     only necessary information.
                                                              
                                                                   • Appropriateness of Translation
              Figure 5: Evaluation Procedure                         Evaluates whether the output is an appropri-
                                                                     ate natural language explanation that does not
                                                                     include expressions in formal proof syntax.
summary of the whole proof.
                                                               The evaluation was performed manually by the first
5     Experiment                                               authors, who holds a degree in applied mathemat-
5.1     Experiment Settings                                    ics, following the procedure shown in Figure 5. The
                                                               evaluation order in the procedure was set based on
For the step-wise informalization and summariza-               the degree of the negative impact of the defects on
tion, we used OpenAI’s GPT-4.1-mini (gpt-4.1-                  the summarization result.
mini-2025-04-14). In the informalization task, the                The experimental results are shown in Ta-
generation temperature was set to 0.4 to obtain                ble 1. The results show that the proposed method
accurate output that adheres to the format of the              achieves the most accurate informalization when
template and few-shot examples. For the summa-                 both the templates and the premise library are used.
rization task, to generate natural proof texts, the            When templates are present, the proposed method
generation temperature was set to 1.0.                         achieves an accuracy over 80%, but without tem-
   For evaluating the proposed method, we used 17              plates, the accuracy drops to approximately 50%.
proofs from Sections 1.1 and 1.2 of "Calculus I -              Counterintuitively, Misinformation increases when
Calculus of one variable -" by Shizuo Miyajima                 the templates are used; this is because necessary
(2010), which were manually formalized according               content such as references to specific variables and
to the structure of the original proofs.                       hypotheses, and reference to an already-proven the-
                                                               orem is significantly shorter when the templates are
5.2     Evaluation of Step-wise Informalization
                                                               not used, consequently decreasing incorrect infor-
The evaluation of the informalization output was               mation. We further validated these findings using
conducted on 1,242 informalized proof steps cre-               McNemar’s test (α = 0.05). The results show that
ated by applying the proposed method to a total                all pairwise comparisons yielded significant dif-
of 38 formal proofs, which include the evaluation              ferences except for the comparison between w/o
data mentioned in 5.1 plus 21 lemmas used in the               template + w/o premise library and w/o template +
formal proofs. The lemmas include theorems taken               w/ premise library, where no significant improve-
from the same textbook (Miyajima, 2010), as well               ment was observed. Detailed results are provided
as helper lemmas used in the formalization of the              in Appendix C.
proofs (e.g., commutativity of conjunctions). Ad-                 In the following, we scrutinize the effect of
ditionally, to confirm the effects of the templates            premise library and templates.
and premise library, four types of generation were
prepared by toggling the presence/absence of the               Effects of premise library
templates and the premise library.                             Using the premise library in conjunction with the
   The output was evaluated along the following                templates improves accuracy by approximately 6%.
four dimensions.                                               This is primarily due to the supression of Misin-
                                                               formation and Insufficient Information, suggesting
    • Accuracy of Included Information                         that providing premises, i.e., natural language ex-
      Evaluates whether the mathematical expres-               planation of definitions and theorems mentioned in
 w/ template     w/ premise      Correct    Misinformation      Insufficient     Unnecessary     Untranslated
                     library                                    Information      Mention         Expression
      ✓               ✓           89.05           5.15               1.50           3.87            0.40
      ✓                           83.09           8.05               4.51           3.46            0.89
                      ✓           53.95           2.50             18.80           24.40            0.40
                                  53.22           3.54             18.44           24.48            0.32

Table 1: Informalization Evaluation Results. The numbers in the table represent percentages relative to the total
number of evaluated proof steps.


a proof, makes it easier to properly refer to them.           Human Evaluation                         Score
On the other hand, when templates are absent,                 w/ recursive            87   11    10    0.857
adding the premise library shows little change in             w/o recursive           85   10    13    0.833
accuracy. This is presumably because the premise
library synergistically improves performance in tan-           Table 2: Summarization Evaluation Results.
dem with template-based generation by allwing the
LLM to fill the slots simply by directly quoting the      of 6.4 evaluation criteria were set. Each evaluation
natural language description of the premises.             criterion included key points that should be men-
Effects of templates                                      tioned in the proof, such as the proposition to be
                                                          proven, theorems used, and newly introduced vari-
Comparing the results with and without templates          ables. These evaluation criteria were all manually
reveals a significant increase in insufficient infor-     set based on the original natural language proofs.
mation and unnecessary mentions when templates               We applied the proposed method to the formal
are absent. This indicates that while the templates       proof to generate a natural language proof, and eval-
function effectively as constraints on the output,        uated whether the result correctly mentioned each
few-shot examples alone are insufficient to con-          evaluation criterion on a three-point scale. The
trol the output. Templates determine the format           evaluation criteria were: "key points correctly cap-
of the output, making it less likely for superfluous      tured ( )", "key points partially captured ( )",
information to be generated while ensuring that           and "key points not captured ( )" (detailed eval-
necessary information is included.                        uation criteria are provided in Appendix D). The
Untranslated formal expressions                           score for the generated result was then calculated
                                                          as follows:
Formal language expressions are occasionally out-
putted directly in the translation and its frequency                     count( ) + 0.5 × count( )
does not change significantly with or without tem-          score =                                  .
                                                                      count( ) + count( ) + count( )
plates or the premise library. This is caused by
formal language definitions (e.g., expressing the         To verify the effectiveness of recursive summariza-
infimum of a set as sInf) and notation specific to        tion, we generated two sets of summaries, with
formal languages (e.g., expressing the n-th element       and without the dependency structure analysis and
of a sequence x as x n) appearing directly in the         recursive summarization.
output. While the former problem is somewhat                 The evaluation results are shown in Table 2. The
ameliorated by the premise library, the latter prob-      numbers in the table represent the total evaluation
lem is due to the shortage of the LLM’s internal          counts for the 17 proofs. The score in the table is
knowledge of mathematical notation and formal             calculated using the previously mentioned formula,
language notation. Thus, no significant improve-          with the denominator being the total number of
ment was observed.                                        evaluation criteria across all the 17 proofs.
                                                             The results show that recursive summarization
5.3   Evaluation of Summarization                         captures slightly more key points than the non-
The evaluation of summarization result was con-           recursive approach. Close inspection revealed that
ducted using the 17 paired data of formal and nat-        the proofs generated using recursive summarization
ural language proofs mentioned in 5.1. First, for         did not exhibit any significant deviations from the
each of the 17 natural language proofs, an average        original formal proofs or logical breakdowns. In
                                                                                                           
   We will show that the greatest lower bound (infi-       We will show that the set P of all positive real
   mum) of the set P of all positive real numbers is       numbers is nonempty, bounded below by zero, and
   zero. First, note that P is nonempty since it con-      that its greatest lower bound (infimum) is exactly
   tains the number 1, which clearly satisfies 1 > 0.      zero. First, we observe that P is nonempty since
   Next, we observe that 0 is a lower bound for P          the number 1 belongs to P by virtue of satisfying
   because every element a ∈ P satisfies a > 0,            the defining property 1 > 0. Next, we demonstrate
   and thus a ≥ 0. Therefore, P is bounded be-             that zero is a lower bound of P by noting that
   low by 0. Since the infimum is the greatest of all      for any element a ∈ P , we have a > 0 and thus
   lower bounds, it follows that the infimum of P is at    a ≥ 0. Since P is nonempty and bounded below,
   least zero. To show that the infimum is not greater     the greatest lower bound inf P exists. We then
   than zero, suppose by contradiction that inf P > 0.     argue by contradiction to show that inf P ≤ 0:
   Then the number inf2 P is positive and thus belongs     assuming inf P > 0, it follows that half of this
   to P , but since inf P is a lower bound, it must        infimum, inf2 P , is an element of P because it is
           inf P
   satisfy 2 ≥ inf P , implying inf P ≤ 0, a con-          strictly greater than zero. However, this contra-
   tradiction. Hence, inf P ≤ 0. Combining these           dicts the property of the infimum being a greatest
   inequalities, we have inf P ≥ 0 and inf P ≤ 0,          lower bound since inf2 P < inf P . Therefore, the
   which together imply inf P = 0. This completes          assumption inf P > 0 fails, and we conclude that
   the proof that zero is the greatest lower bound of      inf P ≤ 0. Coupled with the prior conclusion that
   the set of all positive real numbers.                   inf P ≥ 0, it follows that inf P = 0, completing
                                                        the proof.
Figure 6: The proof of “inf{x ∈ R|x > 0} = 0“ gener-                                                         
ated with using recursive summarization.                 Figure 7: The proof of “inf{x ∈ R|x > 0} = 0” gener-
                                                       ated without using recursive summarization.

contrast, among the 17 outputs generated without
                                                         theorem exists_infinite_primes (n : N) :
recursive summarization, four included reasoning           ∃ p, n ≤ p ∧ Nat.Prime p := by
not in the original proof and/or contained substan-        let p := minFac (n ! + 1)
tial logical inconsistencies. These issues stem from       have f1 : n ! + 1 ̸= 1 :=
                                                             Nat.ne_of_gt <| succ_lt_succ
the LLM’s inability to fully capture the structure                          <| factorial_pos _
of the original formal proof.                              have pp : Nat.Prime p :=
                                                             minFac_prime f1
   The effect of recursive summarization can be            have np : n ≤ p :=
explained as follows. First, the limited input win-          le_of_not_ge fun h =>
dow of the LLM likely contributes to hallucina-                have h1 : p | n ! :=
                                                                 dvd_factorial (minFac_pos _) h
tions. In the recursive summarization approach,                have h2 : p | 1 :=
summaries are generated for semantically coherent                (Nat.dvd_add_iff_right h1 ).2
                                                                   (minFac_dvd _)
units, keeping input size small and thereby reduc-
                                                                   pp.not_dvd_one h2
ing the likelihood of hallucinations. In contrast,         exact ⟨p, np, pp⟩
without recursive summarization, all proof steps
are fed into the model at once, resulting in much
                                                       Figure 8: The formal proof of “there are infinitely many
larger inputs and increased the risk of information
                                                       prime numbers.” in Mathlib.
loss and hallucination. These observations suggest
that recursive summarization is effective for gen-
erating accurate summaries. As an example, we       spectively.
present a generated proof for the proposition “the      Comparing these examples, the proof in Figure
infimum of the set of positive real numbers is 0”.  6 captures the flow of the original proof, though
The original proof is as follows:                   it includes some redundant content. On the other
                                                  
                                                    hand, the proof in Figure 7 fails to mention that
 In this proof, let P := {x ∈ R|x > 0}. By defi-    inf P ≥ 0, and furthermore, deviates from the
 nition, 0 is a lower bound of P , so inf P ≥ 0. If logical flow of the original proof in the reasoning
 inf P > 0, then 1/2 inf P ∈ P , so 1/2 inf P ≥
 inf P must hold. This implies inf P ≤ 0, which     expressed in the highlighted sentence.
 contradicts our assumption that inf P > 0.
                                                   5.4     Translation of Mathlib Formal Proofs
  Figure 6 and 7 present the proofs generated with       The data evaluated so far consisted of existing
and without using the formal proof structure, re-      natural language proofs, for which formal proofs
                                                     
                                                          proofs and demonstrated that it can generate read-
  We will show that for any natural number n, there    able proofs that capture 86% of the key points. We
  exists a prime number p such that p ≥ n. Consider
  the number n! + 1. Since the factorial n! is always
                                                       also showed that the proposed method can generate
  positive for natural n, it follows that n! + 1 > 1,  high-quality natural language proofs from Math-
  so n! + 1 ̸= 1. Let p be the smallest prime factor   lib’s formal proofs, i.e., even from those without
  of n! + 1. By definition, p is prime, as the small-  corresponding natural language proofs.
  est prime factor of any integer greater than 1 must
  itself be prime. Next, suppose for the sake of con-  Supplementary Materials Availability State-
  tradiction that p < n. Since p ≤ n, p divides n! by  ment: The appendix will be submitted as a
  the definition of factorial. Furthermore, p divides
  n! + 1 by choice. Therefore, p divides the differ-   PDF file via the submission form. The source
  ence (n! + 1) − n! = 1, which is impossible since    code and output examples is publicly available at
  no prime number divides 1. This contradiction im-    https://github.com/hattori-matsuzakilab/
  plies that p ≥ n. Hence, for any natural number n,   AutoInformalizationWithTemplate.
  there exists a prime p with p ≥ n, completing the
  proof.                                               Acknowledgments: This research was supported
                                                     in part by KIOXIA Corporation.
Figure 9: The generated proof of “there are infinitely
many prime numbers.”


were then developed. In contrast, this section
presents examples of natural language proofs gen-
erated from Mathlib’s formal proofs using our pro-
posed method.
   As an example, we will use the proposition
“there are infinitely many primes”. The original
formal proof of the theorem is presented in Figure
8. This proceeds as follows:
    • Let p be the smallest prime factor of (n! + 1).
    • That n! + 1 | 1 since factorial is always posi-
      tive.
    • If n > p, then from the property of factorials,
      p | n! and p | n! + 1 holds, then it also holds
      that p | 1. However, since prime numbers do
      not divide 1, this is a contradiction. Therefore,
      n ≤ p holds.
The informalize result is shown in Figure 9. This
demonstrates that even when formal proofs are not
created to directly follow human-written proofs, it
is possible to generate proofs that are still quite
readable as human-written ones. Several other ex-
amples are given in Appendix E.

6    Conclusion
We proposed a natural language translation method
for formal proofs by informalizing each proof step
with template and premise library, and summa-
rizing the result recursively, thereby generating
human-readable natural language proofs. We ap-
plied the proposed method to formal proofs for-
malized according to university-level mathematical
References                                                  Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F. Wu, Fuli
                                                            Luo, and Chong Ruan. 2025. Deepseek-prover-v1.5:
Yves Bertot and Pierre Castéran. 2004. Interactive The-     Harnessing proof assistant feedback for reinforce-
  orem Proving and Program Development Coq’Art:             ment learning and monte-carlo tree search. In The
  The Calculus of Inductive Constructions. Springer-        Thirteenth International Conference on Learning
  Verlag Berlin Heidelberg.                                 Representations.
Daniel Chester. 1976. The translation of formal proofs    Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chala-
  into english. Artificial Intelligence, 7(3):261–278.      mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
                                                            Prenger, and Anima Anandkumar. 2023. Leandojo:
Leonardo de Moura, Soonho Kong, Jeremy Avigad,
                                                            Theorem proving with retrieval-augmented language
  Floris van Doorn, and Jakob von Raumer. 2015. The
                                                            models. In Thirty-seventh Conference on Neural
  lean theorem prover (system description). In Auto-
                                                            Information Processing Systems Datasets and Bench-
  mated Deduction - CADE-25, pages 378–388, Cham.
                                                            marks Track.
  Springer International Publishing.
                                                          Jingyuan Zhang, Qi Wang, Xingguang Ji, Yahui Liu,
Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao,            Yang Yue, Fuzheng Zhang, Di Zhang, Guorui Zhou,
  Zihan Qin, Tianyi Xu, and Bin Dong. 2025. Her-             and Kun Gai. 2025a. Leanabell-prover: Post-
  ald: A natural language annotated lean 4 dataset. In       training scaling in formal reasoning. Preprint,
  The Thirteenth International Conference on Learning        arXiv:2504.06122.
  Representations.
                                                          Lan Zhang, Marco Valentino, and Andre Freitas. 2025b.
Amanda M. Holland-Minkley, Regina Barzilay, and             Formalizing complex mathematical statements with
 Robert L. Constable. 1999. Verbalization of high-          llms: A study on mathematical definitions. Preprint,
 level formal proofs. In Proceedings of the Sixteenth       arXiv:2502.12065.
 National Conference on Artificial Intelligence and
 Eleventh Conference on Innovative Applications of        Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
 Artificial Intelligence, July 18-22, 1999, Orlando,        2022. minif2f: a cross-system benchmark for formal
 Florida, USA, pages 277–284. AAAI Press / The              olympiad-level mathematics. In The Tenth Interna-
 MIT Press.                                                 tional Conference on Learning Representations.
Albert Q. Jiang, Wenda Li, and Mateja Jamnik. 2024.
  Multi-language diversity benefits autoformalization.
  In The Thirty-eighth Annual Conference on Neural
  Information Processing Systems.

Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
  Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
  Jamnik, Guillaume Lample, and Yuhuai Wu. 2023.
  Draft, sketch, and prove: Guiding formal theorem
  provers with informal proofs. In The Eleventh Inter-
  national Conference on Learning Representations.

Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian
  Zhang, Fan Yang, and Xiaoxing Ma. 2024. Autofor-
  malize mathematical statements by symbolic equiva-
  lence and semantic consistency. In The Thirty-eighth
  Annual Conference on Neural Information Process-
  ing Systems.

Shizuo Miyajima. 2010. Bibun sekibungaku I - 1 hensū
  no bibun sekibun -[Calculus I - Calculus of one vari-
  able -]. KYORITSU SHUPPAN CO., LTD.

Lawrence C Paulson. 1990. Isabelle: The next 700
  theorem provers. In Logic and computer science,
  volume 31, pages 361–386. Academic Press.

Guillem Tarrach, Albert Q. Jiang, Daniel Raggi, Wenda
  Li, and Mateja Jamnik. 2024. More details, please:
  Improving autoformalization with more detailed
  proofs. In AI for Math Workshop @ ICML 2024.

Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao,
  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
  Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang,
A     Limitation                                                and Theorems‘ and ensure you understand their content.
                                                                2. **Examine Hypotheses and Goals**:
A.1    Construction of Templates and Few-shot                  - Compare ‘Hypotheses And Goals Before Tactic Applica-
                                                                tion‘ with ‘Hypotheses And Goals After Tactic Application‘
       Examples                                                 to understand what changes in objectives occurred.
The step-by-step informalization of formal proofs                  - Hypotheses and goals are separated with the symbol ’⊢’.
                                                                3. **Formulate the Explanation**:
proposed in this research only becomes effective               - Describe what action the tactic took, referring only to what
when a unique template is prepared for every pos-              was altered based on the changes observed in the hypotheses
sible operation executable by a tactic, along with              and goals.
                                                               - Avoid directly referencing predicates from the formal lan-
multiple few-shot examples for each tactic. How-                guage.
ever, identifying all possible operations a tactic can             - When referring to variables, be sure to explicitly use
perform and creating appropriate few-shot exam-                 these variable names in the output.
                                                                      - (ex) Set A is Empty.
ples for them is extremely time-consuming.                         - **Do not** include the names of theorems or definitions
   To make the method proposed in this research                 in formal languages, or variables used as aliases to specific
                                                                expressions (like h : x = 2 * y) in the output. Instead, explain
applicable to a wider range of formal proofs, it                the content in natural language.
is desirable to implement tools that assist in the              # Output Format
creation of templates and few-shot examples, or an             - Provide a natural language explanation summarizing the
                                                                operation of the tactic and the immediate effects on the hy-
automatic generation tool utilizing LLMs.                       potheses and goals.
                                                                   - Provide all necessary information for the explanation in
A.2    Regarding the Summarization                              precise and detailed terms.
       Generation Method                                        # Examples
                                                                ### Example X
The summarization method proposed in this re-                  **Input Information**:
search aims to generate natural text by recursively            - Applied Tactic: [example.appliedTactic]
                                                               - Hypotheses And Goals Before Tactic Application: [exam-
summarizing based on dependency structures. This                ple.goalsBefore]
is intended to act like a "sieve," repeatedly select-          - Hypotheses And Goals After Tactic Application: [exam-
ing information necessary for the LLM to construct              ple.goalsAfter]
                                                               **Using Definitions and Theorems**:
natural proof texts, thereby filtering out trivial in-         - [example.premises] **Output**:
formation. Therefore, the more complex the proof               - [example.output]
                                                                # Notes
structure is, the more redundant explanations are              - Always determine what assumptions or definitions are
removed, bringing the generated proof closer to a               brought into effect or altered.
human-written proof. However, a challenge arises               - Make sure explanations are precise to maintain clarity and
                                                                avoid unnecessary details.
when dealing with simple proofs that contain trivial           - Do not include expressions written in Lean’s formal lan-
operations not explicitly stated in human-written               guage in the output.
proofs: the number of times the text is sieved de-                 - In formal proofs, casts such as from natural numbers
                                                                to integers are represented by ↑. Therefore, ensure that the
creases, making it more likely for details that are             output does not contain ↑ representing a cast.
trivial for human to be outputted.                             - If you use explanations or citations to output formulas,
   To solve this problem, we believe it is necessary            please use TeX formatting for citations if the formulas are
                                                                not complex, or use explanations written in natural language
to construct a method that explicitly marks impor-              if the formulas are complex.
tant information and reference expressions to be                Using the example above as a reference, please explain the
retained during summarization, rather than relying              following input in natural language as one operation in a
                                                                mathematical proof.
on a simple recursive algorithm.                               **Input Information**:
                                                               - Applied Tactic: [input.appliedTactic]
B     Informalization Prompt                                   - Hypotheses And Goals Before Tactic Application: [in-
                                                                put.goalsBefore]
You are an expert in Lean4 and formal mathematics.             - Hypotheses And Goals After Tactic Application: [in-
Transform the given Lean4 tactic into a clear and concise       put.goalsAfter]
natural language explanation, accurately conveying the op-     **Using Definitions and Theorems**:
eration performed as a step in a mathematical proof without    - [input.premises] **Output**:
using the format of the formal language.
Ensure that any predicates from the formal language are not    C    Results of McNemar’s test for the
included in the explanation.
# Steps                                                             tabulated results of the inverse
1. **Understand the Applied Tactic**:                               formalization
- Analyze the ‘Applied Tactic‘ to comprehend its function
within the proof.
   - If a tactic involves using one or more theorems or def-   Table 3 shows the results of McNemar’s test on the
initions, read the theorems listed under ‘Using Definitions    informalization results, conducted at α = 0.05.
                 method A        method B       A only count       B only count      χ2        p-value
                w/ template     w/ template         51                 123         28.9713   7.3460e-08
                w/o library     w/ library
                w/o template    w/ template          40                475        365.7398   1.5841e-81
                w library       w/ library
                w/o template    w/ template          56                418        274.9388   9.5181e-62
                w library       w/o library
                w/o template    w/ template          42                477        362.9210   6.5096e-81
                w/o library     w/ library
                w/o template    w/ template          62                423        267.2165   4.5875e-60
                w/o library     w/o library
                w/o template    w/o template        115                118         0.0172    8.9576e-01
                w/o library     w/ library

Table 3: Results of McNemar’s test for the tabulated results of the informalization. In the table, "library" refers to
the Premise Library. "A only count" and "B only count" indicate the number of cases where the result was correct
by method A but incorrect by method B, and incorrect by method A but correct by method B, respectively. χ2
denotes the test statistic.


First, when comparing methods without / with                       • Partially captured: The mention was correct
templates, the number of correct results is clearly                  but incomplete.
higher when templates are applied, and the cor-
                                                                   • Not captured: The item was omitted or the
responding p-value is small, indicating a statisti-
                                                                     reasoning was incorrect.
cally significant difference. Regarding the Premise
Library, a significant difference is observed only               For composite categories, an item was rated as
when templates are applied, while no significant               correctly captured only if all component criteria
difference is found when templates are not used.               were satisfied.
This indicates that the Premise Library is effective
only in combination with templates.                            E     Generation Example
                                                               E.1     Example 1
D     Criteria for summarization evaluation
                                                               Theorem : The interior of a closed ball centered at
For the proof summarization evaluation, "key                   a point x with radius r in a metric space is precisely
points" were identified by exhaustively extracting             the open ball centered at x with the same radius r.
items from the original natural language proof that
                                                               theorem interior_closedBall (x : E) {r : R}
fall into the following categories:                               (hr : r ̸= 0) :
                                                                 interior (closedBall x r) = ball x r :=
    1. Definitions of variables and constants used in              by
       the proof.                                                cases ’ hr.lt_or_lt with hr hr
                                                                 . rw [closedBall_eq_empty.2 hr,
                                                                   ball_eq_empty.2 hr.le, interior_empty]
    2. Statements of propositions corresponding to               refine Subset.antisymm ?_
       sub-lemmas.                                                 ball_subset_interior_closedBall
                                                                 intro y hy
                                                                 rcases (mem_closedBall.1 <|
    3. Proofs of the sub-lemmas.                                   interior_subset hy).lt_or_eq with (hr|
                                                                   rfl)
    4. Mentions of proof methods (e.g., proof by                 . exact hr
       contradiction).                                           set f : R → E := fun c : R => c · (y - x
                                                                   ) + x
                                                                               ′
                                                                 suffices f −1 closedBall x (dist y x) ⊆
    5. References to theorems or lemmas used.                      Icc (-1) 1 by
                                                                   have hfc : Continuous f :=
Categories 2 and 3 may be combined with 4 and 5,                      (continuous_id.smul continuous_const)
for instance in cases such as “mentioning the use                       .add continuous_const
                                                                                              ′
                                                                   have hf1 : (1 : R) ∈ f −1 interior (
of proof by contradiction to prove A.”                                closedBall x <| dist y x) := by simpa
   Each item was then evaluated according to the                       [f]
following criteria:                                                have h1 : (1 : R) ∈ interior (Icc (-1 :
                                                                       R) 1) := interior_mono
                                                                      this (
     • Correctly captured: The item was mentioned                       preimage_interior_subset_interior_preimage
       correctly.                                                        hfc hf1)
    simp at h1                                                    have numerator_nonneg : 0 ≤ numerator :=
  intro c hc                                                        by
  rw [mem_Icc , ← abs_le , ← Real.                                  have frac_nonneg : 0 ≤ numerator /
    norm_eq_abs , ← mul_le_mul_right hr]                               denominator :=
  simpa [f, dist_eq_norm , norm_smul] using                            (sub_nonneg.mpr (cos_sq_le_one γ)).
    hc                                                                   trans_eq split_to_frac
                                                                    cases ’ div_nonneg_iff.mp frac_nonneg
                                                                       with h h
      We will show that the interior of a closed ball centered
                                                                    . exact h.left
at a point x with radius r in a metric space is precisely the
                                                                    . simpa [numerator , denominator , a, b,
open ball centered at x with the same radius r.
                                                                       c, h1, h2] using le_antisymm h.right
First, consider the case when r < 0. By the definition of
                                                                       (sq_nonneg _)
a closed ball, no points satisfy the distance condition for a
                                                                  have ab2_nonneg : 0 ≤ 2 * a * b := by
negative radius, so both the closed ball and the open ball are
                                                                    positivity
empty sets. Since the interior of the empty set is empty, the
                                                                  calc
proposition holds trivially in this case.
                                                                    1 / 2 * a * b * sin γ = 1 / 2 * a * b *
Next, for r ≥ 0, we prove the equality by showing mutual                 √               √
                                                                        ( numerator /       denominator) := by
inclusion. Specifically, it suffices to prove that the interior
of the closed ball is contained within the open ball. Assume           rw [sin_eq_sqrt_one_sub_cos_sq ,
y is an element of the interior of the closed ball centered              split_to_frac , sqrt_div
at x with radius r. To establish that y lies in the open                 numerator_nonneg] <;>
ball, we conduct a case analysis on the distance d(y, x). If             simp [γ, angle_nonneg , angle_le_pi]
                                                                                  √
d(y, x) < r, then y is clearly in the open ball by definition,      _ = 1 / 4 *      ((2 * a * b) ^ 2 - (a * a
so the claim holds.                                                     + b * b - c * c) ^ 2) := by
To treat the remaining case, we define a function f : R → E            field_simp [numerator , denominator ,
by f (c) = c·(y−x)+x. This function is continuous, as it is              ab2_nonneg]; ring
                                                                                    √
composed of scalar multiplication and vector addition, both         _ = ↑1 / ↑4 *      (s * (s - a) * (s - b)
of which preserve continuity. Since y lies in the interior of          * (s - c) * ↑4 ^ 2) := by simp only [
the closed ball with radius d(y, x), it follows that the scalar        s]; ring_nf
                                                                         √
1 (corresponding to y = f (1)) is an interior point of the          _ =     (s * (s - a) * (s - b) * (s - c))
preimage under f of this interior. Given that the preimage of           := by
the closed ball under f is contained in the interval [−1, 1],          rw [sqrt_mul ’, sqrt_sq ,
this implies that 1 is an interior point in [−1, 1]. Using the           div_mul_eq_mul_div , one_mul ,
continuity of f and properties of norms and distances, we                mul_div_cancel_right_0] <;>
show that any c such that f (c) lies in the closed ball must             norm_num
satisfy c ∈ [−1, 1]. By exploiting the positivity of d(y, x)
and the equivalence of norms and absolute values, we verify
                                                      We will prove Heron’s formula by showing that half
the inequalities establishing this containment. Together,
                                                the product of two sides of a triangle and the sine of their
these arguments imply that y must lie within the open ball
                                                included angle equals the square root of the semiperimeter
centered at x with radius r, completing the proof that the
                                                times its differences with each side. Let a, b, and c be the
interior of the closed ball equals the open ball with the same
                                                lengths of the sides opposite points p1 , p3 , and p2 , respec-
parameters.                                     tively, and let s = a+b+c   denote the semiperimeter. Define
                                                                       2
                                                γ as the angle formed at vertex p2 between sides a and b.
E.2 Example 2                                   Noting that a and b are positive since the points are dis-
                                                tinct, we proceed to express cos γ via the Law of Cosines
Theorem : Heron’s formula                                       2  2
                                                                     −c2
                                                as cos γ = a +b   2ab
                                                                         . Squaring this expression and sub-
theorem heron {p1 p2 p3 : P} (h1 : p1 ̸= p2)    tracting from 1, we write 1 − cos2 γ as a ratio of polyno-
                                                                                           numerator
   (h2 : p3 ̸= p2) :                            mial expressions in a, b, c, specifically denominator , where the
    let a := dist p1 p2                         numerator is defined as the difference between (2ab)2 and
    let b := dist p3 p2                         (a2 +b2 −c2 )2 , and the denominator is (2ab)2 . We establish
    let c := dist p1 p3                         that this numerator is nonnegative by analyzing the quotient
    let s := (a + b + c) / 2
                                        √       and considering the range of cos2 γ, then employing a case
    1 / 2 * a * b * sin (∠ p1 p2 p3) =    (     analysis of the signs of numerator and denominator along
      s * (s - a) * (s - b) * (s - c)) :=       with the nonnegativity of squares and inequalities among the
      by                                        side lengths. Furthermore, we show that 2ab is nonnegative
  intro a b c s                                 since it appears multiplied by sin γ, which corresponds to
  let γ := ∠ p1 p2 p3                           geometric quantities bounded between zero and π. Confirm-
  obtain := (dist_pos.mpr h1).ne’, (            ingpthat the angle γ satisfies 0 ≤ γ ≤ π, we express sin γ
    dist_pos.mpr h2).ne’                        as 1 − cos2 γ and simplify the corresponding expressions
  have cos_rule : cos γ = (a * a + b * b -      by substituting the polynomial ratios and simplifying via
    c * c) / (2 * a * b) := by                  algebraic equivalences. Through     these steps, we verify the
    field_simp [mul_comm ,                                                   p
                                                key equality 12 ab sin γ = s(s − a)(s − b)(s − c), com-
    dist_sq_eq_dist_sq_add_dist_sq_sub_two_mul_dist_mul_dist_mul_cos_angle
                                                pleting the proof of Heron’s formula as desired.
       p1 p2 p3]
  let numerator := (2 * a * b) ^ 2 - (a * a
     + b * b - c * c) ^ 2
                                               E.3 Example 3
  let denominator := (2 * a * b) ^ 2           Theorem: f and g are real-valued functions defined
  have split_to_frac : ↑1 - cos γ ^ 2 =
    numerator / denominator := by              on the real line. For all x and y, f (x + y) + f (x −
    field_simp [cos_rule]                      y) = 2f (x)g(y). f is not identically zero and
|f (x)| ≤ 1 for all x. Prove that |g(x)| ≤ 1 for all             Since |f (x)| ≤ 1 for all x, the set S is bounded above by 1,
x. (IMO 1972 Q5)                                                 ensuring k ≤ 1. For any real number x, we have |f (x)| ≤ k
                                                                 by definition of the supremum.
                                                                      Next, we observe that for all x, y ∈ R, the functional
theorem imo1972_q5 (f g : R → R) (hf1 : ∀ x
                                                                 equation implies
  , ∀ y, f (x + y) + f (x - y) = 2 * f x *
  g y)
  (hf2 : ∀ y, ∥f y∥ ≤ 1) (hf3 : ∃ x, f x ̸=                       2|f (x)||g(y)| = |2f (x)g(y)| = |f (x + y) + f (x − y)|
     0) (y : R) : ∥g y∥ ≤ 1 := by                                                ≤ |f (x + y)| + |f (x − y)| ≤ 2k.
-- Suppose the conclusion does not hold.
by_contra! hneg                                                  Dividing both sides by 2|g(y)|, we define
set S := Set.range fun x => ∥f x∥
-- Introduce ‘k‘, the supremum of ‘f‘.                                                             k
let k : R := sSup S                                                                     k′ :=           .
                                                                                                 |g(y)|
-- Show that ‘∥f x∥ ≤ k‘.
have hk 1 : ∀ x, ∥f x∥ ≤ k := by                                 Now, since k ≥ |f (x)| > 0 for some x where f (x) ̸= 0,
  have h : BddAbove S := ⟨1, Set.                                we have k > 0. Because we assumed |g(y)| > 1, it follows
     forall_mem_range.mpr hf2⟩                                   that
  intro x                                                                                  k
  exact le_csSup h (Set.mem_range_self x)                                           k′ =        < k,
                                                                                         |g(y)|
-- Show that ‘2 * (∥f x∥ * ∥g y∥) ≤ 2 * k‘.
have hk 2 : ∀ x, 2 * (∥f x∥ * ∥g y∥) ≤ 2 * k                     as dividing by a number greater than one reduces the value.
   := fun x 7→                                                         On the other hand, considering the inequality for arbi-
  calc                                                           trary x,
     2 * (∥f x∥ * ∥g y∥) = ∥2 * f x * g y∥ :=                                           |f (x)| ≤ k,
        by simp [abs_mul , mul_assoc]
                                                                 and from the previous inequality,
     _ = ∥f (x + y) + f (x - y)∥ := by rw [
       hf1]
     _ ≤ ∥f (x + y)∥ + ∥f (x - y)∥ :=                                                2|f (x)||g(y)| ≤ 2k,
       norm_add_le _ _
     _ ≤ k + k := add_le_add (hk 1 _) (hk 1 _)                   which implies
     _ = 2 * k := (two_mul _).symm
set k’ := k / ∥g y∥                                                                               k
                                                                                   |f (x)| ≤           = k′ .
-- Demonstrate that ‘k’ < k‘ using ‘hneg ‘.                                                     |g(y)|
have H1 : k’ < k := by
  have h1 : 0 < k := by                                          Since this is true for all x, it follows that every element of
     obtain ⟨x, hx⟩ := hf3                                       S is bounded above by k′ ; hence k ≤ k′ by definition of
     calc                                                        supremum.
       0 < ∥f x∥ := norm_pos_iff.mpr hx                               Combining these two inequalities yields the contradic-
       _ ≤ k := hk 1 x                                           tion
  rw [div_lt_iff]                                                                         k′ < k ≤ k′ ,
  . apply lt_mul_of_one_lt_right h1 hneg
  . exact zero_lt_one.trans hneg                                 which cannot hold. This contradiction arises from the as-
-- Demonstrate that ‘k ≤ k’‘ using ‘hk 2 ‘.                      sumption that |g(y)| > 1.
have H2 : k ≤ k’ := by                                                 Therefore, we conclude that |g(y)| ≤ 1 for all y, com-
  have h1 : ∃ x : R, x ∈ S := by use ∥f 0∥;                      pleting the proof.
      exact Set.mem_range_self 0
  have h2 : ∀ x, ∥f x∥ ≤ k’ := by
     intro x
     rw [le_div_iff]
     . apply (mul_le_mul_left zero_lt_two).
       mp (hk 2 x)
     . exact zero_lt_one.trans hneg
  apply csSup_le h1
  rintro y’ ⟨yy, rfl⟩
  exact h2 yy
-- Conclude by obtaining a contradiction , ‘
  k’ < k’‘.
apply lt_irrefl k’
calc
  k’ < k := H1
  _ ≤ k’ := H2


      We will show that if a function f satisfies the func-
tional equation f (x + y) + f (x − y) = 2f (x)g(y) for all
real numbers x, y, and if |f (x)| ≤ 1 for all x with some
|g(y)| > 1, then this leads to a contradiction, thereby imply-
ing that |g(y)| ≤ 1.
      To proceed, let S = {|f (x)| : x ∈ R} denote the set
of norms of values of f , and let k = sup S be its supremum.
