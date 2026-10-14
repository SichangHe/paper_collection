                                             On Reasoning-Centric LLM-based Automated
                                                         Theorem Proving

                                                 Yican Sun1 , Chengwei Shi1 , Hangzhou Lyu1 , and Yingfei Xiong12(B)
                                             1
                                            Key Laboratory of High Confidence Software Technologies (Peking University),
                                         Ministry of Education; School of Computer Science, Peking University, Beijing, China
                                                                   {sycpku,xiongyf}@pku.edu.cn
arXiv:2604.19558v1 [cs.SE] 21 Apr 2026




                                                             {2200013126,2300012939}@stu.pku.edu.cn
                                                                    2
                                                                       Zhongguancun Laboratory



                                                  Abstract. Automated theorem proving is fundamental to formal meth-
                                                  ods, and the recent trend is to integrate large language models (LLMs)
                                                  and proof assistants to form effective proof agents. While existing proof
                                                  agents show promising performance, they inadequately leverage reason-
                                                  ing capabilities of modern LLMs in high-level planning and self-critique.
                                                  We argue that proof agents should not merely generate tactics but also
                                                  reason strategically about proof plans and critically evaluate their own
                                                  proposals.
                                                  This paper introduces ReCent-Prover, a reasoning-centric LLM-based
                                                  proof agent for Rocq that addresses two critical limitations in current
                                                  systems. First, we present validation with reflection, enabling LLMs to
                                                  scrutinize their generated tactics and synthesize failure summaries when
                                                  reflection identifies potential errors, filtering out potentially misapplied
                                                  tactics earlier. Second, we propose retrieval with planning, which condi-
                                                  tions retrieval on LLM-generated proof plans rather than subgoal simi-
                                                  larity, retrieving lemmas and proofs that align with the anticipated proof
                                                  strategy. Both techniques increase the number of invocations of LLMs.
                                                  However, when evaluated on the CoqStoq benchmark, even under the
                                                  same budget of LLM invocations, ReCent-Prover achieves a 22.58%
                                                  relative improvement in the number of proved theorems over the pre-
                                                  vious state-of-the-art, demonstrating that our reasoning-centric design
                                                  significantly enhances automated theorem proving capabilities.


                                         1       Introduction
                                         Theorem proving within proof assistants is the cornerstone of formal methods,
                                         enabling landmark achievements from verifying compilers [12] to mechanizing
                                         the proofs of mathematical theorems [5, 7, 9]. In the era of generative AI, the
                                         need to formally verify AI-generated artifacts—including both code and mathe-
                                         matical proofs—makes theorem proving even more critical. However, construct-
                                         ing formal proofs is labor-intensive. Traditional automation techniques based on
                                         symbolic proof search [3, 6, 18, 22] have provided valuable assistance, but they
                                         fundamentally struggle to scale to complex tasks due to the explosion of the
                                         search space.
2       Y. Sun et al.

    The recent success of large language models (LLMs) has reshaped automated
theorem proving [4, 8, 10, 11, 13, 14, 23, 26–28, 31], shifting the paradigm from ex-
haustive symbolic search to neural proof generation. Since LLMs rarely generate
correct proofs in a single attempt, state-of-the-art systems [11] adopt an agentic
approach where an LLM iteratively generates formalized proofs in an interactive
environment of a proof assistant. To help the LLM better understand the current
subgoal, these systems retrieve relevant lemmas and definitions to contextualize
the proof task, with some [27] further incorporating existing proofs to guide the
proof strategies.
    Despite substantial progress, existing systems largely emphasize the mechan-
ics of interaction between LLMs and proof assistants (e.g., how to incorporate
the feedback from the proof assistant), rather than fully harnessing the LLMs’
capability in high-level planning and self-critique to guide the proof search itself.
As LLMs continue to advance, especially the advancement of reasoning abilities,
we advocate that LLM-based self-reasoning should be the central component of
future proof agents. Thus, agents should not only generate tactics, but also rea-
son strategically about proof plans and critically evaluate their own proposals.
From this perspective, we identify two key limitations of current approaches and
propose novel modules to address these limitations.
    First, existing proof agents accept every generated tactic validated by the
proof assistant, even when it irreversibly makes the goal more difficult to prove
or directs the search toward unprovable branches. For instance, misapplying
a lemma via apply may generate subgoals that have counter-examples, while
inducting on the wrong variable or failing to properly generalize the hypothesis
in induction can be ineffective, or even lead to unprovable subgoals.
    To address this problem, our solution is to leverage the reasoning capabilities
of LLMs to self-validate its own generated tactics. In detail, we introduce valida-
tion with reflection, a technique that not only validates LLM-generated tactics
using the proof assistant, but also enables the LLM to scrutinize its own tactic
proposals. When reflection identifies a potentially misapplied tactic, the agent
synthesizes and records a failure summary to steer the next iteration; otherwise,
the tactic proceeds as usual. Since reflecting on every tactic would be expensive,
we adopt a selective strategy, applying self-reflection only to tactics that may
(1) generate more than one subgoals, or (2) lead to unprovable states, such as
apply and induction mentioned above.
    The second limitation concerns the retrieval process. Ideally, a retriever would
return lemmas that are actually used in the proof and proofs that instantiate the
same high-level strategy. However, this oracle behavior is unattainable without
knowing the proof in advance. Existing retrieval methods therefore rely on a
proxy assumption—that similar subgoals imply similar proof plans and lemma
usage—which does not necessarily hold.
    To address this, we observe that although we cannot know the final proof in
advance, we can leverage the high-level proof plan, which LLMs excel at gen-
erating, as a proxy for retrieval. We therefore propose retrieval with planning.
We pre-process the lemma library by generating a natural-language description
              On Reasoning-Centric LLM-based Automated Theorem Proving          3

for each lemma using an LLM, then index lemmas by semantic embeddings of
these descriptions rather than by their formal statements. Similarly, for each
proof example, we generate a natural-language proof plan and index the exam-
ple database by embeddings of these plans rather than by subgoals. During proof
search, we first prompt the LLM to generate a proof plan for the current goal,
then use this plan to retrieve candidate lemmas and proofs that align with the
anticipated strategy. By conditioning retrieval on plan-level semantics, our ap-
proach captures strategies that transfer across syntactically different theorems
and surfaces genuinely relevant knowledge beyond subgoal similarity.
    We implement and evaluate ReCent-Prover3 , a Rocq proof agent inte-
grating validation with reflection and retrieval with planning, on CoqStoq [27],
a benchmark of real-world Rocq projects. Despite requiring more LLM invoca-
tions per proof attempt, under the same budget of LLM invocations, ReCent-
Prover achieves a 22.58% relative improvement in proved theorems over the
previous state-of-the-art [11]. Further experiments over different configurations
of ReCent-Prover demonstrate the effectiveness of both techniques.
Contributions. To summarize, this paper makes the following contributions:

 – We propose a novel validation with reflection technique that enables the
   LLM to critique its own generated tactics during proof search, making the
   proof search more robust and effective.
 – We propose a novel retrieval with planning technique that conditions re-
   trieval on LLM-generated proof plans, enabling strategy-aligned lemma and
   example selection beyond subgoal similarity.
 – We implement ReCent-Prover, a Rocq proof agent that integrates two
   techniques mentioned above, and evaluate it on the CoqStoq benchmark. Our
   approach achieves a 22.58% relative improvement in the number of proved
   theorems against the previous state-of-the-art LLM-based proof agent.


2     Preliminaries

This section introduces basic concepts of formal theorem proving in Rocq (for-
merly known as Coq) [1] through the following running example.

Example 1. Suppose one is interested in proving the following lemma from Com-
pCert’s memory-initialization routine, which characterizes alignment checking
for a concatenation of data items laid out consecutively in memory. The theorem
statement and relevant definition are presented in Fig. 1. Here, data_list_size
computes the total size of a data list, and dl_align p il (presented below)
asserts that the list il satisfies the alignment constraints when laid out consec-
utively starting at position p. The lemma dl_align_app reduces alignment of
the concatenation to two independent checks: l1 at pos and l2 at the shifted
position pos + data_list_size l1.
3
    Short for “Reasoning-Centric Prover”
4       Y. Sun et al.


Theorem dl_align_app: forall l2 l1 pos,
  dl_align pos (l1 ++ l2) ↔
  dl_align pos l1 ∧ dl_align (pos + data_list_size l1) l2.

(* the size of an individual datum *)
Definition data_size (i: datum) : Z := ...
(* the sum of data_size of list elements *)
Definition data_list_size (l: list datum) : Z := ...
(* well_aligned i p: datum i is correctly aligned at position p. *)
Definition well_aligned (i: datum) (p: Z) : Prop := ... (* omitted *)
Fixpoint dl_align (p: Z) (il: list datum) : Prop :=
  match il with
  | nil ⇒ True
  | i1 :: il ⇒ well_aligned i1 p ∧ dl_align (p + data_size i1) il
  end.


                                Fig. 1. Running Example


Proof Library. A proof library is a collection of (i) previously established lem-
mas imported at the point where the proof of dl_align_app begins, and (ii) the
proofs of these imported lemmas. These lemmas can be reused to significantly
simplify the proof. Moreover, existing proofs in the library may provide useful
proof patterns or insights that can be adapted when constructing the formal
proof of dl_align_app.
Subgoals. Once the proof is initiated, the proof assistant returns to our prover
a list of subgoals to be established. Each subgoal consists of a set of premises and
a consequent, requiring the prover to prove the consequent from the premises.
Example 2. Continuing with Example 1, at the start of the proof of dl_align_app,
there is exactly one subgoal presented below.
      [No Premise]

      forall (l1 l2 : list datum) (pos : Z),
      dl_align pos (l1 ++ l2) ↔
      dl_align pos l1 ∧ dl_align (pos + data_list_size l1) l2

This state has no premise, and its goal is precisely the statement of dl_align_app,
meaning that we aim to prove the theorem without any additional assumptions.

Tactics. Subgoals are proved or transformed by applying tactics, each of which
consumes a subgoal and produces zero, one, or more new subgoals (with zero
indicating that the subgoal is proved). Tactics are applied sequentially, one at
a time. Each tactic application is checked by the proof assistant. Applying a
syntactically valid tactic produces an updated list of subgoals, whereas applying
an invalid tactic results in an error and leaves the current subgoals unchanged.
By default, tactics are applied to the first subgoal in the remaining subgoal
list, and all subgoals produced are prepended as the first element to the list of
unproved subgoals.
Example 3. Continuing with Example 2, suppose we apply the tactic intros l1
l2 pos. This introduces l1, l2, and pos into the context, yielding the following
subgoal:
             On Reasoning-Centric LLM-based Automated Theorem Proving           5

     l1, l2: list datum
     pos: Z

                      + l2) ↔
     dl_align pos (l1 +
     dl_align pos l1 ∧ dl_align (pos + data_list_size l1) l2


   Having introduced the relevant concepts, the objective of formal theorem
proving is to find a sequence of tactics that (1) can be successfully checked by
the proof assistant, and (2) leaves no remaining subgoals after all tactics have
been applied.


3   The Workflow of ReCent-Prover




                          Fig. 2. Workflow of ReCent-Prover.



    In this section, we present the workflow of ReCent-Prover (illustrated in
Fig. 2) by continuing the running example introduced in (Example 1).
    ReCent-Prover proceeds iteratively. The prover first checks whether there
are any remaining subgoals. If no subgoals remain, the prover reports success
and returns a complete formal proof. Otherwise, if the iteration limit T has
been reached, the prover reports failure. If neither condition holds, the prover
continues proving. When continuing, ReCent-Prover attempts to prove the
first element S among the remaining subgoals, which is the default target for
subsequent tactic applications. For instance, the first iteration for proving the
theorem in Example 1 will try to solve the subgoal in Example 2. Invoking
Hammer. To prove S, our prover first tries to invoke CoqHammer [6], a state-
of-the-art symbolic prover for Rocq. CoqHammer performs symbolic proof search
over S, automatically selecting and reusing previously established lemmas from
the proof library via its built-in lemma selection module. If CoqHammer suc-
ceeds, it generates a formal proof that proves S. In this case, our prover records
6         Y. Sun et al.

the generated proof and advances to the next iteration. If CoqHammer fails, the
prover falls back to invoking an LLM to generate tactics.
Retrieval with Planning. To guide the LLM in generating tactics, we need
to provide the LLM not only with the current subgoal S but also with essential
information in the proof library to make the LLM aware of existing lemmas
and proofs. However, including the entire proof library is impractical due to the
input-length limitations of LLMs. Thus, it is necessary to retrieve a subset of the
library that is most useful for proving the current subgoal. ReCent-Prover
therefore performs lemma and proof-example retrieval, taking the current sub-
goal S as input and producing two outputs: (1) a set of lemmas that are expected
to be reused in the proof, and (2) a set of existing proofs [27] that are likely to
share similar proof ideas and can thus assist the LLM in generating a formal
proof.
    Unlike conventional retrieval methods based on textual similarity between the
current subgoal S and the formal lemma statements or subgoal of the proofs in
the library, ReCent-Prover employs a novel retrieval-with-planning technique,
which leverages the power of LLMs to identify higher-quality lemmas and proofs
from the library. Further details about our novel retrieval technique are provided
in Sect. 5.
LLM-based Proof Generation. After retrieving lemmas and examples from
the library, we are ready to construct a prompt (details in Sect. A). Our prompt
consists of two parts: (i) a fixed system prompt that specifies the Rocq theorem-
proving task, and (ii) a user prompt that provides task-specific information for
the current subgoal. The user prompt is instantiated from a template and in-
cludes the following four components.

    – First, we provide the current subgoal S to be proved, together with all formal
      definitions of the terms that appear in S. We can get these definitions by
      calling standard APIs of the Rocq prover. This information helps the LLM
      accurately understand and reason about the current proof task. For example,
      when instructing the LLM to prove the subgoal shown in Example 2, we
      include not only the subgoal itself but also the definitions of data_list_size
      and dl_align.
    – In addition to the current subgoal, we also provide the retrieved lemmas and
      proofs.
    – Moreover, we also provide the LLM with the history of previous failed at-
      tempts on the same subgoal, which helps it avoid repeating the same errors.
      The failure history is maintained per subgoal and updated by the validation-
      with-reflection module after each failed attempt.
    – Finally, the prompt instructs the LLM to wrap all generated Rocq tactics
      with predefined decorators, which facilitates parsing the response from the
      LLM.

After receiving the response from the LLM, our prover can easily parse the
LLM-generated formal proof by the design of our prompt.
             On Reasoning-Centric LLM-based Automated Theorem Proving               7

Example 4. Continuing with Example 2, after performing retrieval and instruct-
ing the LLM using the prompt template described above, ReCent-Prover
receives the following response:
                   intros l1 l2 pos. induction l1; simpl.
                   ... (* proof below omitted due to irrelevance *)




Validation with Reflection. However, LLMs frequently make mistakes when
generating tactics, making it necessary to validate their outputs. Traditionally,
existing agents only use the proof assistant to validate LLM-generated tactics,
and blindly accepts all proofs that are validated to be syntactically correct by
the proof assistant. However, an LLM may occasionally misapply a tactic in a
way that does not immediately trigger an error. Existing proof agents may still
retain such misapplied tactics, causing the search to become trapped in an even
harder or invalid branch. Below, we present a concrete example that illustrates
this issue.

Example 5. Continuing with Example 4, all LLM-generated tactics are verified
to be syntactically correct by the proof assistant. Intuitively, the proof first in-
troduces the variables l1, l2, and pos, yielding the subgoal shown in Example 3.
It then performs induction on l1 and simplifies all subgoals generated by the
induction. As a result, two subgoals remain, corresponding to the base case and
the inductive case; for brevity, we present only the inductive case.
    In this case, l1 is destructed as a :: l1’. The resulting subgoal (shown
below) requires proving that the consequent of Example 3 holds for l1, under
the inductive hypothesis that the same consequent holds for l1’.
    (* Subgoal for Inductive Case, omit irrelevant details *)
    l1’ : list datum
    l2 : list datum
    a    : datum
    pos : Z
    IHl1 : ... ∧ dl_align (pos + data_list_size l1’) l2

    ... ∧ dl_align (pos + data_size a + data_list_size l1’) l2

    Although these tactics are validated by the proof assistant, the induction
is not effective. Specifically, in the consequent, the first argument of dl_align
differs from the corresponding argument in the inductive hypothesis. This mis-
match prevents the inductive hypothesis from being applied, making the subgoal
more complicated and even harder to prove.
    Instead, the correct approach is to perform induction directly on l1 before
introducing the remaining variables. This ensures that the inductive hypothesis
is sufficiently general and can be applied in the inductive case.

    To address this issue, ReCent-Prover introduces a novel validation-with-
reflection technique (details in Sect. 4) to filter out potentially misapplied tactics
early. Our technique leverages the reasoning capabilities of LLMs during proof
validation. This module sequentially examines the generated tactics, checking
8         Y. Sun et al.

whether each tactic can be validated by the proof assistant and, more impor-
tantly, instructing the LLM to review whether its own generated tactic is po-
tentially misapplied–either ineffective or leading to unprovable subgoals. The
output of this module consists of two components:

    – The tactics to be retained for the current iteration, which are both validated
      by the proof assistant and not flagged as potentially misapplied by the LLM.
    – A new failure record that updates the failure history. Each record is a triple
      consisting of (1) the subgoal that failed to be proved, (2) the sequence of
      tactics attempted in this failure case–either rejected by the proof assistant or
      flagged as misapplied by the LLM, and (3) the reason for the failure. If the
      tactics are rejected by the proof assistant, the reason is the corresponding
      error message; if they are flagged as misapplied, the reason is a concise
      explanation generated by the LLM.

The retained tactics update the set of subgoals, and the proof agent advances
to the next iteration with a new set of subgoals.

Example 6. Continuing with Example 5, our validation-with-reflection module
flags these two tactics as misapplied and returns:

    – that no proof should be retained; and
    – a failure record consisting of (1) the subgoal in Example 2, (2) the tactics
      shown in Example 4, and (3) an LLM-generated explanation stating: “The
      induction is performed without appropriate generalization, making
      the hypothesis too weak to be applied...”

Since no tactic is retained, the next iteration continues to attempt the same
subgoal in Example 2, while the failure history records this unsuccessful induc-
tion attempt. In the subsequent iteration, conditioned on this failure record, the
LLM avoids repeating the same mistake and successfully generates a complete
formal proof of dl_align_app.


4      Validation with Reflection

This section presents our novel validation with reflection module. The key feature
of this module is to use an LLM to self-validate its tactic proposals. This raises
two challenges.
Challenges. First, examining every tactic generated by the LLM is prohibitively
costly. Therefore, we adopt a selective strategy that focuses only on tactics that
may (1) generate multiple subgoals, or (2) lead to unprovable states (e.g., assert,
apply, induction). In contrast, tactics such as intros, simpl, and rewrite
are excluded from reflection. We identify the categories of tactics that require
reflection by manually inspecting the Rocq tactic index [1]. We use ReflCat
to denote the set of all tactic categories selected for reflection. Due to space
limitations, we present ReflCat in Sect. B.
             On Reasoning-Centric LLM-based Automated Theorem Proving               9

    Second, recall that this module produces failure records that update the
failure history. Each record consists of (1) the subgoal that failed to be proved,
(2) the sequence of tactics leading to the failure, and (3) the failure reason. Prior
proof agents [26] record only the subgoal immediately preceding the error and
the single tactic that directly triggers it, with the failure reason limited to the
error message reported by the proof assistant.
    However, failures caused by misapplied tactics often arise from a sequence
of tactics rather than a single step. For example, applying intros followed by
induction may result in insufficient generalization and an unusable inductive
hypothesis. In such cases, recording only the subgoal before induction and
the induction tactic itself is insufficient; instead, the entire sequence of tactics
leading to the failure must be captured. Moreover, because misapplied tactics
may not trigger any error from the proof assistant, the failure reason must be
explicitly summarized by our system rather than obtained from an error message.

Our Idea. To address this issue, our module attempts to capture the problematic
sequence of tactics–that is, the contiguous sequence of tactic applications that
leads to a misapplied or ineffective subgoal–using a simple heuristic. ReCent-
Prover maintains the index of the most recent tactic, denoted pid, at which
one of the following events occurs: (1) the proof begins, (2) a subgoal is fully
proved, or (3) a tactic in ReflCat is applied.
    When a tactic is flagged as misapplied, the module rolls back to pid and
records a single failure instance consisting of: (1) the subgoal after the first pid
tactics, (2) the sequence of tactics from pid to the current tactic, and (3) a failure
reason summarized by the LLM. Our insight is that proving a subgoal naturally
“closes” a local proof branch, while tactics in ReflCat (e.g., assert, apply,
induction) are precisely those that can branch the proof or irreversibly alter
the proof structure. Consequently, the sequence of tactics from pid to the current
tactic captures a compact yet sufficient context leading to the misapplication.

Details. As shown in the pseudo-code in Algorithm 1, the module scans the tac-
tics sequentially (Line 2) and maintains two key pieces of state: (1) pid, the most
recent rollback point to be used when a misapplied tactic is detected; and (2)
gpre , the first unproved subgoal after applying the first pid tactics. The subgoal
gpre is used when constructing failure records, as it captures the subgoal before
the potentially misapplied tactic sequence begins, providing precise context for
diagnosing the failure.
    For each tactic Ti , the module first invokes the function Execute (Line 3)
with side effect, which executes Ti in the proof assistant and returns a triple
(gapp , err, gsnew ). Here, gapp is the subgoal to which the tactic is applied–by
default, the first unproved subgoal prior to execution. The component err is the
error message returned by the proof assistant, with err = ∅ indicating successful
execution. The component gsnew is the list of new subgoals produced by applying
Ti to gapp .
    If the proof assistant reports an error (err ̸= ∅, Lines 4–5), the module imme-
diately terminates validation: it saves all previously validated tactics T1 . . . Ti−1
10       Y. Sun et al.


 Algorithm 1: Pseudo-code for Validation with Reflection
   Input: A list of LLM-generated tactics T1 . . . Tn
   Output: The tactics to be saved, and the failure
 1 pid ← −1; gpre ← ∅
 2 for i ← 1 to n do
 3     gapp , err, gsnew ← Execute(Ti )
 4     if err ̸= ∅ then
 5         return (T1 . . . Ti−1 , (gapp , Ti , err))
 6     if gsnew = ∅ then
 7         pid ← i; gpre ← SubGoals(0)
 8         continue
 9     if Category(Ti ) ∈ ReflCat then
10         (res, summary) ← Reflection(gapp , gsnew , Ti )
11         if res = Misapplied then
12              Resume(Ti , Ti−1 , Ti−2 , . . . , Tpid+1 )
13              return (T1 . . . Tpid , (gpre , Tpid+1 . . . Ti , summary))
14         pid ← i; gpre ← SubGoals(0)
15 return (T1 . . . Tn , ∅)




and returns a failure record consisting of the current subgoal gapp , the invalid
tactic Ti , and the error message err.
    If no new subgoals are generated (gsnew = ∅), the current subgoal is fully
proved. In this case, the module updates pid ← i and sets gpre to the current
first unproved subgoal via SubGoals(0) (Lines 6–8).
    If Ti belongs to ReflCat, the module invokes the Reflection subroutine
(Lines 9–10), whose details are demonstrated at the end of this section. This
subroutine takes as input the applied subgoal gapp , the newly generated subgoals
gsnew , and the tactic Ti , and prompts the LLM to assess whether the tactic
is potentially misapplied, i.e., ineffective or leading to unprovable states. The
subroutine returns either Accepted or Misapplied, along with a short LLM-
generated explanatory summary.
    If Misapplied is returned, the module rolls back the subgoal to the last
rollback point pid and records a failure instance consisting of: (1) the subgoal
gpre ; (2) the sequence of tactics Tpid+1 . . . Ti responsible for the failure; and (3)
the LLM-generated summary explaining why the tactic sequence is misapplied.
Otherwise if Accepted is returned, the module updates pid ← i and refreshes
gpre (Lines 11–14).
    If all tactics are successfully validated, the module returns the full tactic
sequence along with an empty failure record (Line 15).
Details of Reflection. Finally, we present the details of the Reflection sub-
routine. This subroutine performs two checks: (1) whether all newly generated
subgoals in gsnew are provable, i.e., whether any of them is likely to admit coun-
terexamples; and (2) in the case of the induction tactic, whether the induction
is performed on an appropriate variable and whether the inductive hypothesis
             On Reasoning-Centric LLM-based Automated Theorem Proving           11

is sufficiently well generalized. We treat destruct as a weak form of induction
(i.e., induction without an inductive hypothesis) and apply the same checks.
Both checks are carried out by prompting the LLM.
    To perform the first check, the system prompt explicitly explains the task,
including what it means for a goal to admit a counterexample. It also provides
several in-context learning examples illustrating common cases of unprovable
subgoals, such as subgoals with no premises and a contradictory consequent (e.g.,
a < a). We verify that these examples do not overlap with any benchmarks used
in our experiments. The user prompt then specifies the concrete task, consisting
of all subgoals in gsnew together with all definitions appearing in these subgoals.
We additionally require the LLM to produce a structured, machine-parsable
response to facilitate downstream processing.
    To perform the second check, we use a similar prompt with two key differ-
ences. First, the prompt explains common failure modes in induction, such as
performing induction on an inappropriate variable or failing to generalize hy-
potheses properly. Second, we include the original subgoal gapp in the prompt,
allowing the LLM to compare the goal before and after the application of in-
duction and assess whether the induction has been applied appropriately. Due
to space limitations, the prompt for both checks are presented in Sect. A.



5   Retrieval with Planning

This section presents our retrieval with planning technique. Given the current
unproved subgoal, it retrieves relevant lemmas and proofs from the proof library.
We begin with a motivating example that highlights a key limitation of subgoal-
similarity retrieval, and then describe our method in detail.



 Theorem approx_scale s m : range1 m (exp2R s * (m / exp2R s)).
 Proof.
   (* Show exp2R s * (m / exp2R s) == m *)
   assert (Em: exp2R s * (m / exp2R s) == m). {
     (* To prove this equality, the key is to use *)
     (* the lemma mulRCA: x * (y * z) == y * (x * z) *)
     rewrite mulRCA.
     (* Now we need to prove m * (exp2R s / exp2R s) == m, we omit
     the trivial proof here. *)
     ...
   }
   rewrite Em.
   (* Now it suffices to show range1 m m, which we omit here. *)
   ...
 Qed.


               Fig. 3. Motivating Example for Retrieval with Planning.
12      Y. Sun et al.

5.1   Motivating Example

Consider the theorem approx_scale (Fig. 3) from the Four-Color project in
CoqStoq [9], where:

 – range1 m x is a predicate asserting that a real number x ∈ R lies within the
   range [m, m + 1), where m ∈ Z is an integer.
 – exp2R s is a function that takes as input a real number s and outputs 2s .

Overall, the lemma states m dividing and then multiplying by exp2R s, whose
result is exactly the same as m, still falls into the range [m, m + 1).
    To prove approx_scale, the crucial step is to establish that the second argu-
ment of range1 is exactly m, i.e., the assertion Em in Fig. 3. Once Em is proved, the
goal reduces to range1 m m—namely, m ∈ [m, m+1)—which is immediate. Proving
Em requires a small but strategically important algebraic rearrangement: we need
to rewrite exp2R s * (m / exp2R s) into a form where m is isolated and the
reciprocal terms are grouped. This step relies on a multiplication-rearrangement
lemma, mulRCA, in the proof context.
    Ideally, the retrieval component should return mulRCA, since it is essential
for proving Em. However, standard retrievers (including the one in Fig. 4) rank
candidate lemmas by syntactic similarity to the current subgoal. For instance,
BM25 [27], a widely used baseline, models both the current subgoal and each
lemma as bags of terms and scores candidates using term-frequency statistics.
While this heuristic often works, it fails in this example because the subgoal is
dominated by domain-specific symbols such as exp2R (which appears twice). As a
result, BM25 is biased toward lemmas about exponentiation—most of which are
irrelevant to the needed algebraic rearrangement. In contrast, mulRCA has little
overlap with the subgoal and is therefore ranked low. Consequently, a proof agent
relying on BM25 may fail to retrieve mulRCA and cannot complete the proof.
    To address this limitation, we introduce retrieval with planning, which con-
ditions retrieval on the anticipated proof strategy rather than the raw subgoal.
In this example, a plan that explicitly mentions “rearrange the multiplication
to isolate m” naturally points to mulRCA, even though mulRCA is syntactically
dissimilar to the subgoal. Fig. 4 presents the overall workflow.
Our Insight. Our key insight is that LLMs are effective at generating a high-
level natural-language proof plan that serves as a good proxy for the structure of
the eventual formal proof. However, this plan is expressed in natural language,
whereas the available library lemmas are stated in a formal proof language,
making direct matching difficult. As illustrated in Fig. 4, we bridge this gap by
generating a natural-language description for each lemma and retrieving lemmas
based on semantic similarity between each proof-plan step and these descriptions.
The semantic similarity is computed in a standard way: we embed each proof-
plan step and each lemma description into vectors using an embedding model
and rank lemmas by vector similarity (e.g., cosine similarity [16]). Intuitively,
semantically related steps and lemmas tend to yield nearby embeddings, and are
therefore retrieved together.
             On Reasoning-Centric LLM-based Automated Theorem Proving            13

Retrieving Proofs. Besides retrieving lemmas, prior work [27] also retrieves
proofs as references to help the LLM construct the current proof. Following the
same insight, we generate a natural-language plan for each existing proof and
retrieve proofs by embedding-based similarity between the current plan and the
stored plans.




                    Fig. 4. Diagram of Retrieval with Planning.




5.2   Details of Retrieval Procedure

Below, we first present the retrieval procedure for lemmas, and then briefly de-
scribe the retrieval procedure for proofs, which follows the same overall structure.
Pre-processing Lemma Databases. ReCent-Prover requires a repository
of lemmas and proofs. To avoid data leakage, at query time we restrict candidates
to the lemmas that are available in the current proof context (i.e., imported and
usable at the current location), and retrieve only within this restricted set.
    For each lemma, we instruct the LLM to generate a short description that
abstracts away syntactic details while preserving the lemma’s semantic intent
and typical usage (full details in Sect. A). We then embed this description using
a text embedding model that maps text sequences to fixed-dimensional vectors,
such as text-embedding-3-large [20], and store the lemma together with its de-
scription and embedding vector in the database.
Example 7. Let us continue with Sect. 5.1. The description of the lemma mulRCA
in the proof context generated by the LLM is:
This lemma states that the order of multiplication can be
rearranged without changing the result . It can be used to
rewrite expressions involving nested multiplications .
14     Y. Sun et al.

Retrieving Lemmas. Given an unproved subgoal S, we first prompt the LLM
to produce a high-level proof plan for S. Specifically, the prompt asks for a
step-by-step natural-language outline of how to prove the subgoal. To help the
LLM generate a better proof plan, in addition to the current subgoal S, we also
provide the definitions appearing in S. To facilitate downstream parsing, we
include detailed formatting instructions requiring the plan to be returned as a
structured, machine-parsable list (see Sect. A for the full prompt). In response,
the LLM outputs a step-by-step proof plan in natural language.
Example 8. Continuing with Example 7, When we are at the beginning of the
proof of theorem approx_scale in Fig. 3, the LLM generates the following proof
plan:
< step > Show that the second argument is exactly m </ step >
< step > Use a multiplication - rearrangement lemma to rewrite
the expression . </ step >
( Further steps are omitted for brevity .)
...


    For each generated proof step, ReCent-Prover embeds the step using the
same embedding model and retrieves candidate lemmas by the similarity between
the step embedding and the embeddings of lemma descriptions. All retrieved
lemmas, along with their descriptions and typical usage, are merged and included
in the prompt provided to the LLM.

Example 9. Continuing with Example 8, note that the second step of the proof
plan is semantically similar to the lemma mulRCA in the proof context. Therefore,
ReCent-Prover will retrieve mulRCA as the candidate lemma for the second
step.

Retrieval Procedure for Proofs. The retrieval procedure for proofs is sim-
ilar to that for lemmas, but differs in two key aspects. First, for each existing
proof, we generate a natural-language proof plan using a prompt similar to that
described in Sect. A, while omitting any failure history (since none exists) and
providing the completed proof. We then embed the resulting proof plan and
store each proof together with its plan embedding vector in the database. Sec-
ond, at query time, we embed the entire proof plan for the current unproved state
and retrieve those proofs whose plan embeddings are most similar. All retrieved
proofs, along with their proof ideas, are included in the prompt provided to the
LLM. The prompts for building the proof database are presented in Sect. A.


6    Evaluation
This section evaluates the performance of ReCent-Prover. Specifically, it ad-
dresses the following research questions:
 – RQ1: What is the overall performance of ReCent-Prover?
            On Reasoning-Centric LLM-based Automated Theorem Proving           15

 – RQ2: How does ReCent-Prover compare with state-of-the-art proof au-
   tomation systems?
 – RQ3: What is the effectiveness of each proposed technique, namely valida-
   tion with reflection (Sect. 4) and retrieval with planning (Sect. 5)?

Benchmark. We evaluate ReCent-Prover using CoqStoq [27], a comprehen-
sive benchmark suite for automated proof search in Rocq. CoqStoq is built on
Rocq version 8.18 and contains a diverse collection of theorems spanning multiple
domains, including compiler verification [12] and formalized mathematics [5,7,9].
Implementation Details. ReCent-Prover is implemented on Rocq version
8.18 to ensure compatibility with CoqStoq. For CoqHammer, we configure a
timeout of 25 seconds and allow up to 64 threads per invocation. All experiments
are conducted on a machine equipped with Intel Xeon Gold 6230 CPUs and
503 GB of memory. We set the iteration limit T = 25, allowing at most 25
proof-search iterations per theorem.
    Across all experiments, within each experimental setup, we use the same
backend language model for retrieval, proof generation, and reflection. For em-
beddings, we consistently adopt text-embedding-3-large [20] as the embedding
model. The maximum token limit and temperature for the LLMs are set to their
default values.
    Recall that ReCent-Prover requires a repository of lemmas and proofs for
retrieval. In our experiments, the retrieval database is the set of theorems in
CoqStoq. The database is constructed once offline. At query time, we restrict
retrieval to the intersection between this database and the current proof library,
ensuring that all retrieved lemmas are available for use in the proof and avoiding
potential data leakage. At each retrieval step, we retrieve eight lemmas and eight
proofs, and left-clip the final prompt to satisfy the maximum token constraint.

6.1   RQ1: What is the overall performance of ReCent-Prover

Setup. To assess the overall performance of ReCent-Prover, we evaluate it
on the CoqStoq benchmark. Due to budget constraints, we randomly sample 200
theorems from CoqStoq, following prior work [11]. We use the state-of-the-art
o4-mini model [21] as the backend language model.
Results. On the 200 sampled theorems from CoqStoq, ReCent-Prover suc-
cessfully proves 138 out of 200 (69%), demonstrating strong overall performance.

6.2   RQ2: How does ReCent-Prover compare to state-of-the-art
      proof automation systems?

Setup. We compare ReCent-Prover against CobbleStone, the existing
state-of-the-art (SOTA) proof agent. To reduce the cost of LLM invocations, we
directly use the detailed evaluation results reported in the open-source reposi-
tory of CobbleStone, without re-running the system. For a fair comparison,
we adopt the following configurations for ReCent-Prover:
16     Y. Sun et al.

 – CobbleStone is configured with GPT-4 [19]. Accordingly, we also use GPT-
   4 as the backend language model for ReCent-Prover.
 – CobbleStone limits the number of LLM invocations to 20 per theorem. To
   match this setting, we also restrict ReCent-Prover to at most 20 LLM
   invocations per online theorem proving, including those used for retrieval, re-
   flection, and proof generation. Note that each iteration of ReCent-Prover
   may invoke multiple LLM invocations–two for retrieval with planning, one for
   proof generation, and several for validation with reflection. As a result, the
   prover may terminate before reaching the iteration limit T = 25. Note that
   since the database of lemmas and proofs is constructed once, this one-time
   pre-processing cost is not counted toward the per-theorem LLM-invocation
   budgets.
 – CobbleStone uses a CoqHammer timeout of 25 seconds and runs on Intel
   Xeon Gold 6230 hardware. Accordingly, we also configure ReCent-Prover
   with a 25-second CoqHammer timeout and conduct all experiments on the
   same CPU architecture.

Furthermore, since CobbleStone is built on an earlier version of Rocq (8.12),
whereas ReCent-Prover targets Rocq 8.18, we evaluate both systems on the
intersection of the benchmarks used in the CobbleStone paper [11] and Co-
qStoq. This results in a total of 222 benchmarks.

Results. On these 222 benchmarks, CobbleStone successfully proves 93 theo-
rems, whereas ReCent-Prover proves 114, yielding a 22.58% relative improve-
ment. This performance gap indicates that our approach substantially outper-
forms the existing state-of-the-art proof agent, with Example 5 and Example 9
providing concrete illustrations of the effectiveness of our techniques. We make
best efforts to align the experimental setup across systems, using the same back-
end model, the same number of LLM invocations, and the intersection of bench-
marks for evaluation. While we cannot guarantee identical configurations in all
aspects, we believe the observed performance gap (22.58% relative improvement)
is sufficiently large to outweigh these differences.
   Beyond the direct comparison with CobbleStone, because we evaluate on
the same benchmark set, our results also yield indirect comparisons with the
other proof systems [2, 4, 24, 27] reported in the CobbleStone paper. Table 1
summarizes these results. ReCent-Prover substantially outperforms all prior
systems on this benchmark.

Token Efficiency. In addition to proof success rate, ReCent-Prover is also
substantially more token-efficient than CobbleStone. On the 222-benchmark
set with the GPT-4 backend, ReCent-Prover uses an average of 15.6K to-
kens per theorem, compared with CobbleStone’s 48.2K tokens, making
ReCent-Prover approximately 3.1× more token-efficient while simulta-
neously solving 22.58% more theorems.
            On Reasoning-Centric LLM-based Automated Theorem Proving           17

      Table 1. Comparison of ReCent-Prover against baseline proof systems

 Baseline          ReCent-Prover (Ours)         Baseline    Rel. Improvement
 CobbleStone                51.35%               41.89%          +22.58%
 PALM                       51.35%               38.74%          +32.56%
 ProverBot9001              51.35%               17.12%          +200.00%
 Rango                      52.50%               36.50%          +43.84%
 Tactician                  52.50%               22.50%          +133.33%

 Table 2. Results of Different Configurations in Random 200 Samples in CoqStoq

                                     Modules
Configuration                                              #Proved       Avg. Tokens
                       Hammer LLM Refl. Retrieval
(C1) Hammer               ✓       ×      ×        ×     55 (↑ 150.91%)      24.1K
(C2) BM25                 ✓       ✓      ×      BM25 118 (↑ 16.95%)         30.0K
(C3) Planning             ✓       ✓      ×     Planning 128 (↑ 7.81%)       58.5K
(C4) Refl. & BM25         ✓       ✓      ✓      BM25    130 (↑ 6.15%)       45.5K
(C5) ReCent-Prover        ✓       ✓      ✓     Planning       138           66.7K



6.3   RQ3: Effectiveness of Techniques


Setup. To assess the effectiveness of each technique in ReCent-Prover, namely
validation with reflection and retrieval with planning, we evaluate ReCent-
Prover with various configurations. We selectively enable or disable the validation-
with-reflection module and vary the retrieval strategy between retrieval-with-
planning and BM25, the latter being the retrieval method used in prior work [4,
27]. We use the same experimental setup as in Sect. 6.1.

Results. Table 2 presents the result. Each row corresponds to a configuration
with different modules enabled or disabled. The “Modules” columns indicate
whether the configuration uses Hammer, LLM-based proof generation, reflec-
tion during validation, and the retrieval strategy employed (none, BM25, or
planning). The final column reports #Proved, the number of problems success-
fully proved in our random subsamples, and the average token cost per theorem,
while the ↑ percentage indicates the relative improvement of the full system over
each configuration.
    The full system, ReCent-Prover (C5), achieves the best performance,
proving 138 theorems and outperforming all other configurations. In contrast,
the Hammer-only baseline (C1) proves only 55 theorems, highlighting the neces-
sity of LLM-based proof generation in modern proof agents.
    Under the same BM25 retrieval strategy, enabling reflection (C4) yields a
10.17% improvement over the no-reflection setting (C2), demonstrating that
reflection-based validation substantially improves proof success. Similarly, under
retrieval with planning, reflection (C5) provides a further 7.81% improvement
18      Y. Sun et al.

Table 3. Statistical significance (p-values) of ReCent-Prover (C5) vs. each baseline
configuration.

                            Comparison        p-Value
                            vs. CobbleStone    0.0196
                            vs. (C1) Hammer    0.0000
                            vs. (C2) BM25      0.0002
                            vs. C3 Planning    0.0075
                            vs. C4 Refl.       0.0481



over its no-reflection counterpart (C3), indicating that reflection consistently
contributes additional gains even with stronger retrieval.
    Comparing retrieval strategies without validation with reflection, the re-
trieval with planning (C3) outperforms the BM25 retrieval (C2) by 8.47%,
suggesting that our novel retrieval module is more effective than purely text-
similarity based retrieval. When reflection is enabled, the retrieval with planning
(C5) still yields an additional 6.15% improvement over the BM25 retrieval (C4),
reinforcing that retrieval with planning remains beneficial even in the presence
of validation with reflection.
    Regarding token cost, the full system (C5) uses more tokens per theorem
than simpler configurations because of the overhead of plan-based retrieval and
reflection. However, this additional cost is worthwhile: the full system (C5) solves
150.91% more theorems than the no-RAG, no-reflection baseline (C1).
Generalization Across Backend Models. To assess how well our techniques
generalize across language models, we conduct a preliminary experiment us-
ing MiniMax-M2.5 [17], a popular open-source model with 10B active parame-
ters. We randomly sample 100 theorems from CoqStoq and compare ReCent-
Prover (full system) against the BM25-retrieval, no-reflection ablation (match-
ing the C2 vs. C5 comparison in Table 2). ReCent-Prover solves 61/100 the-
orems while the ablation solves 52/100, yielding a 17.31% improvement. This
is consistent with the 16.95% improvement observed under o4-mini (C2 vs. C5
in Table 2), suggesting that our two proposed techniques generalize across both
closed-source and open-source backend models.
Statistical Significance. To further confirm the superiority of ReCent-Prover
over the baselines, we conduct a p-test comparing C5 against each configuration.
As shown in Table 3, all p-values are below 0.05, confirming that the improve-
ments are statistically significant.


7    Related Work

LLM-based proof agents. Our work is closely related to LLM-based proof
agents. A substantial body of prior work has developed agentic systems that
             On Reasoning-Centric LLM-based Automated Theorem Proving            19

combine symbolic provers with LLM-based proof generation [4, 11, 26]. How-
ever, as discussed in Sect. 1, these systems primarily focus on how to interact
with the proof assistant, rather than fully leveraging the reasoning and plan-
ning capabilities of LLMs. In contrast, ReCent-Prover introduces two novel
techniques—validation with reflection and retrieval with planning—that enable
LLMs to contribute more effectively to the overall proof-search workflow. Ex-
perimental results demonstrate the effectiveness of our approach, achieving a
22.58% relative improvement in the number of theorems proved over existing
state-of-the-art systems.
Language Models for Theorem Proving. Another related line of research
focuses on developing fine-tuned neural theorem provers [8,10,13,14,23,27,28,31].
While these approaches leverage learned models for proof generation, to our
knowledge, none of them incorporates the two techniques proposed in ReCent-
Prover, namely validation with reflection and retrieval with planning.
Agents with Planning and Self-reflection. In the broader AI community,
LLM-based agents increasingly combine planning and self-reflection to improve
decision making [15, 25, 29, 30]. Adapting these ideas to formal theorem proving,
however, is nontrivial. First, the feedback is both sparse and brittle. Many tactic
sequences fail abruptly with low-level error messages, while other sequences may
be accepted locally yet steer the proof into a potentially unprovable or unneces-
sarily difficult branch. Second, the available context (e.g., large proof libraries)
often exceeds the input budget of LLMs, so planning and reflection must oper-
ate under partial information rather than the full set of reusable lemmas and
proof patterns. ReCent-Prover addresses these challenges by introducing two
domain-specific mechanisms: retrieval with planning, which enables plan-level
retrieval of relevant lemmas and proofs under limited context, and validation
with reflection, which detects and filters potentially misapplied yet syntactically
valid tactics before they derail the proof search.
Symbolic provers. Traditional proof automation in proof assistants relies on
symbolic proof search [3, 6, 18, 22]. Some approaches translate proof goals into
SMT formulas and then reconstruct proofs as tactics in the proof assistant [3,
6, 22], while others employ dedicated proof search over dependent type theory.
However, purely symbolic provers suffer from significant scalability limitations.
As our experiments indicate, a purely symbolic prover proves only 55/200 theo-
rems in a random sample from CoqStoq, whereas our proof agent proves 138/200
theorems–a 150.91% relative improvement in the number of theorems proved (de-
tails in Table 2).


8   Conclusion
This paper advocates for a reasoning-centric approach to automated theorem
proving, where LLMs not only generate proof tactics but also strategically plan
and critically evaluate their proposals. We address two fundamental limitations
in existing LLM-based proof agents: the blind acceptance of syntactically valid
20      Y. Sun et al.

but potentially misapplied tactics, and the reliance on syntactic similarity for
retrieval rather than strategic alignment.
    Our solution introduces two techniques. First, validation with reflection en-
ables the LLM to scrutinize its generated tactics through self-reflection, synthe-
sizing failure analyses and regenerating alternatives when potential errors are
detected. By selectively targeting tactics whose misuse leads to unprovable sub-
goals, we maintain efficiency while improving robustness. Second, retrieval with
planning conditions retrieval on LLM-generated proof plans rather than subgoal
similarity. By indexing lemmas through natural-language descriptions and proof
examples through strategic plans, we surface knowledge that genuinely aligns
with anticipated proof strategies across syntactically diverse theorems.
    We implement these innovations in ReCent-Prover, a proof agent for Rocq
evaluated on CoqStoq. Our approach achieves a 22.58% relative improvement
in the number of theorems proved over the previous state-of-the-art, with fur-
ther studies confirming that both components contribute substantially to overall
performance. As reasoning capabilities of language models continue to evolve,
positioning reasoning at the heart of automated theorem proving promises in-
creasingly capable systems that effectively complement human expertise in mech-
anizing complex formal arguments.


References

 1. Bertot, Y., Casteran, P.: Interactive Theorem Proving and Program Development.
    SpringerVerlag (2004)
 2. Blaauwbroek, L., Urban, J., Geuvers, H.: The tactician: A seamless, interactive tac-
    tic learner and prover for coq. In: Intelligent Computer Mathematics: 13th Interna-
    tional Conference, CICM 2020, Bertinoro, Italy, July 26–31, 2020, Proceedings. p.
    271–277. Springer-Verlag, Berlin, Heidelberg (2020). https://doi.org/10.1007/978-
    3-030-53518-6_17, https://doi.org/10.1007/978-3-030-53518-6_17
 3. Blanchette, J.C., Böhme, S., Paulson, L.C.: Extending sledgehammer with smt
    solvers. In: Bjørner, N., Sofronie-Stokkermans, V. (eds.) Automated Deduction –
    CADE-23. pp. 116–130. Springer Berlin Heidelberg, Berlin, Heidelberg (2011)
 4. Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A.,
    Barham, P., Chung, H.W., Sutton, C., Gehrmann, S., Schuh, P., Shi, K.,
    Tsvyashchenko, S., Maynez, J., Rao, A., Barnes, P., Tay, Y., Shazeer, N., Prab-
    hakaran, V., Reif, E., Du, N., Hutchinson, B., Pope, R., Bradbury, J., Gur-Ari, G.,
    Yin, P., Duke, T., Levskaya, A., Ghemawat, S., Dev, S., Michalewski, H., Garcia,
    X., Misra, V., Robinson, K., Fedus, L., Zhou, D., Ippolito, D., Luan, D., Lim, H.,
    Zoph, B., Spiridonov, A., Sepassi, R., Dohan, D., Agrawal, S., Omernick, M., Dai,
    A.M., Pillai, T.S., Pellat, M., Lewkowycz, A., Moreira, E., Child, R., Polozov, O.,
    Lee, K., Zhou, Z., Wang, X., Saeta, B., Diaz, M., Firat, O., Catasta, M., Wei, J.,
    Meier-Hellstern, K., Eck, D., Dean, J., Petrov, S., Fiedel, N.: Palm: Scaling lan-
    guage modeling with pathways. Journal of Machine Learning Research 24(240),
    1–113 (2023), https://jmlr.org/papers/v24/22-1144.html
 5. Cohen, C., Mörtberg, A.: A coq formalization of finitely presented modules. In:
    Klein, G., Gamboa, R. (eds.) Interactive Theorem Proving. pp. 193–208. Springer
    International Publishing, Cham (2014)
             On Reasoning-Centric LLM-based Automated Theorem Proving                21

 6. Czajka, z., Kaliszyk, C.: Hammer for coq: Automation for dependent type theory.
    J. Autom. Reason. 61(1–4), 423–453 (Jun 2018). https://doi.org/10.1007/s10817-
    018-9458-4, https://doi.org/10.1007/s10817-018-9458-4
 7. Doczkal, C., Smolka, G.: Regular language representations in the con-
    structive type theory of coq. J. Autom. Reason. 61(1–4), 521–553 (Jun
    2018). https://doi.org/10.1007/s10817-018-9460-x, https://doi.org/10.1007/
    s10817-018-9460-x
 8. First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: Whole-proof generation and
    repair with large language models. In: Proceedings of the 31st ACM Joint Eu-
    ropean Software Engineering Conference and Symposium on the Foundations of
    Software Engineering (ESEC/FSE 2023). pp. 1229–1241. ACM, San Francisco,
    CA, USA (2023). https://doi.org/10.1145/3611643.3616243, https://people.cs.
    umass.edu/~brun/pubs/pubs/First23fse.pdf
 9. Gonthier, G.: Formal proof—the four-color theorem. Notices of the Ameri-
    can Mathematical Society 55(11), 1382–1393 (2008), https://www.ams.org/
    journals/notices/200811/tx081101382p.pdf
10. Jiang, A.Q., Welleck, S., Zhou, J.P., Li, W., Liu, J., Jamnik, M., Lacroix, T., Wu,
    Y., Lample, G.: Draft, sketch, and prove: Guiding formal theorem provers with
    informal proofs. In: International Conference on Learning Representations (2023),
    https://arxiv.org/abs/2210.12283
11. Kasibatla, S.R., Agarwal, A., Brun, Y., Lerner, S., Ringer, T., First, E.:
    Cobblestone: A divide-and-conquer approach for automating formal verifi-
    cation (2025). https://doi.org/10.48550/arXiv.2410.19940, https://arxiv.org/
    abs/2410.19940, arXiv v3 (Aug 2025)
12. Leroy, X.: Formal verification of a realistic compiler. Communications of the
    ACM 52(7), 107–115 (2009). https://doi.org/10.1145/1538788.1538814, https:
    //xavierleroy.org/publi/compcert-CACM.pdf
13. Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.H., Zhao, H., Jiang, L., Geng, Y.,
    Ge, J., Sun, J., Wu, J., Gesi, J., Lu, X., Acuna, D., Yang, K., Lin, H., Choi,
    Y., Chen, D., Arora, S., Jin, C.: Goedel-prover v2: Scaling formal theorem proving
    with scaffolded data synthesis and self-correction. arXiv preprint arXiv:2508.03613
    (2025), https://arxiv.org/abs/2508.03613, version V2, improved pipeline and
    SOTA results
14. Liu, H., Sun, J., Li, Z., Yao, A.C.: Proofaug: Efficient neural theorem proving via
    fine-grained proof structure analysis. In: Singh, A., Fazel, M., Hsu, D., Lacoste-
    Julien, S., Berkenkamp, F., Maharaj, T., Wagstaff, K., Zhu, J. (eds.) Proceedings of
    the 42nd International Conference on Machine Learning. Proceedings of Machine
    Learning Research, vol. 267, pp. 39568–39586. PMLR (13–19 Jul 2025), https:
    //proceedings.mlr.press/v267/liu25bp.html
15. Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon,
    U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B.P., Hermann,
    K., Welleck, S., Yazdanbakhsh, A., Clark, P.: Self-refine: iterative refinement with
    self-feedback. In: Proceedings of the 37th International Conference on Neural In-
    formation Processing Systems. NIPS ’23, Curran Associates Inc., Red Hook, NY,
    USA (2023)
16. Manning, C.D., Raghavan, P., Schütze, H.: Introduction to Information Retrieval.
    Cambridge University Press, Cambridge, UK (2008)
17. MiniMax: MiniMax-M2.5: Built for real-world productivity. https://www.
    minimax.io/news/minimax-m25 (2026), accessed: 2026
22      Y. Sun et al.

18. Norman, C., Avigad, J.: Canonical for automated theorem proving in
    lean. In: 16th International Conference on Interactive Theorem Prov-
    ing (ITP 2025). Leibniz International Proceedings in Informatics (LIPIcs),
    vol. 352, pp. 14:1–14:20. Schloss Dagstuhl–Leibniz-Zentrum für Informatik
    (2025). https://doi.org/10.4230/LIPIcs.ITP.2025.14, https://drops.dagstuhl.
    de/entities/document/10.4230/LIPIcs.ITP.2025.14
19. OpenAI: Gpt-4 technical report, https://arxiv.org/abs/2303.08774
20. OpenAI: text-embedding-3-large, https://platform.openai.com/docs/models/
    text-embedding-3-large, openAI API embedding model documentation; model
    released 2024-01-25.
21. OpenAI: o4-mini: latest reasoning model in the openai o-series (2025), https:
    //platform.openai.com/docs/models/o4-mini
22. Qian, Y., Clune, J., Barrett, C., Avigad, J.: Lean-auto: An interface between lean
    4 and automated theorem provers. In: Piskac, R., Rakamarić, Z. (eds.) Computer
    Aided Verification. pp. 175–196. Springer Nature Switzerland, Cham (2025)
23. Ren, Z.Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z., Zhu,
    Q., Yang, D., Wu, Z.F., Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,
    Ruan, C.: Deepseek-prover-v2: Advancing formal mathematical reasoning via re-
    inforcement learning for subgoal decomposition (2025), https://arxiv.org/abs/
    2504.21801
24. Sanchez-Stern, A., Alhessi, Y., Saul, L., Lerner, S.: Generating correctness
    proofs with neural networks. In: Proceedings of the 4th ACM SIGPLAN
    International Workshop on Machine Learning and Programming Languages.
    p. 1–10. MAPL 2020, Association for Computing Machinery, New York,
    NY, USA (2020). https://doi.org/10.1145/3394450.3397466, https://doi.org/
    10.1145/3394450.3397466
25. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S.: Reflexion: lan-
    guage agents with verbal reinforcement learning. In: Proceedings of the 37th Inter-
    national Conference on Neural Information Processing Systems. NIPS ’23, Curran
    Associates Inc., Red Hook, NY, USA (2023)
26. Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., Chaudhuri, S.: An in-context learn-
    ing agent for formal theorem-proving. In: Proceedings of the 1st Conference on
    Language Modeling (COLM 2024). Philadelphia, PA, USA (Oct 2024), https:
    //openreview.net/forum?id=V7HRrxXUhN, cOLM 2024, Oct 7–9, 2024
27. Thompson, K., Saavedra, N., Carrott, P., Fisher, K., Sanchez-Stern, A.,
    Brun, Y., Ferreira, J.F., Lerner, S., First, E.: Rango: Adaptive retrieval-
    augmented proving for automated software verification. In: Proceedings of
    the 47th International Conference on Software Engineering (ICSE). Ottawa,
    Canada (Apr 2025). https://doi.org/10.48550/arXiv.2412.14063, https://arxiv.
    org/abs/2412.14063, to appear; ICSE 2025
28. Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil,
    S., Prenger, R.J., Anandkumar, A.: Leandojo: Theorem proving with
    retrieval-augmented language models. In: Advances in Neural Information
    Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track
    (2023),      https://proceedings.neurips.cc/paper_files/paper/2023/file/
    4441469427094f8873d0fecb0c4e1cee-Paper-Datasets_and_Benchmarks.pdf,
    includes Lean datasets/benchmarks (Lean 3/4) for training and evaluation
29. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T.L., Cao, Y., Narasimhan, K.: Tree
    of thoughts: deliberate problem solving with large language models. In: Proceedings
    of the 37th International Conference on Neural Information Processing Systems.
    NIPS ’23, Curran Associates Inc., Red Hook, NY, USA (2023)
             On Reasoning-Centric LLM-based Automated Theorem Proving              23

30. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K.R., Cao, Y.: Re-
    act: Synergizing reasoning and acting in language models. In: The Eleventh Inter-
    national Conference on Learning Representations (ICLR 2023), Kigali, Rwanda,
    May 1–5, 2023. OpenReview.net (2023), https://openreview.net/forum?id=WE_
    vluYUL-X
31. Zhang, J., Wang, Q., Ji, X., Liu, Y., Yue, Y., Zhang, F., Zhang, D., Zhou, G.,
    Gai, K.: Leanabell-prover: Posttraining scaling in formal reasoning (2025), https:
    //arxiv.org/abs/2504.06122


A     Omitted Prompts
A.1    Prompts for LLM-based Proof Generation

    [System Prompt]
    You are an expert in Rocq theorem proving . Your task is
    to generate a sequence of tactics to prove the given
    subgoal . You will be provided with : ( i ) the current
    subgoal , and ( ii ) contextual information including
    relevant definitions , illustrative examples , applicable
    lemmas , and the history of previous proof attempts . Based
     on this information , generate a valid proof script that
    will be accepted by the Rocq proof assistant .
    [User Prompt]
    ### subgoal to be Solved ...
    ### Definitions ...
    ### Examples ...
    ### Lemmas ...
    ### Failure History ...
    You need to wrap generated tactics with <coq > and </ coq >.



A.2    Prompts for Evaluating the Provability of Subgoals

[ System Prompts ]
# Rocq Provability Evaluation Module

You are an expert Rocq proof assistant specializing in
evaluating the provability of proof goals . Your role is to
analyze whether the current proof goals are likely to be
provable or if they contain logical contradictions , false
assumptions , or other issues that would make them
impossible to prove .

## Your Task

Given :
- ** Current Goals **: The obtained proof subgoal ( s ) after
applying the tactic
24    Y. Sun et al.

- ** Relevant Definitions **: All definitions from the
codebase that are relevant to understanding the goal
structure

You must evaluate whether the current goals are provable ,
identifying any issues that would prevent successful
completion of the proof .

## Common Issues to Detect

### 1. Contradictory Hypotheses
When the hypotheses contain logical contradictions that
make the goal vacuously true but practically unprovable .

** Example of Unprovable Goal :**
- Hypotheses : ‘n : nat ‘ , ‘ H1 : n = 0 ‘ , ‘ H2 : n = 1 ‘
- Goal : ‘n + 1 = 2 ‘
- Problem : The hypotheses contradict each other ( n cannot
be both 0 and 1) , making this state impossible to reach in
a valid proof

** What to check :**
- Look for hypotheses that assert contradictory facts
- Check for equality assumptions that conflict with each
other
- Identify impossible combinations of conditions

### 2. Missing or Insufficient Hypotheses
When the goal requires information that is not available in
 the hypotheses or context .

** Example of Unprovable Goal :**
- Hypotheses : ‘n : nat ‘
- Goal : ‘n > 10 ‘
- Problem : There ’ s no information about n that would allow
proving it ’ s greater than 10

** What to check :**
- Does the goal make claims that can be derived from the
hypotheses ?
- Are all necessary facts about variables present in the
context ?
- Would the goal require additional axioms or lemmas not
available ?

### 3. Overly Strong or Unprovable Statements
When the goal makes a claim that is mathematically false or
 requires axioms not available .

** Example of Unprovable Goal :**
          On Reasoning-Centric LLM-based Automated Theorem Proving   25

- Goal : ‘ forall n : nat , exists m : nat , m > n /\ m < n ‘
- Problem : This is logically impossible ( no number can be
both greater than and less than another number )

** What to check :**
- Is the goal mathematically / logically valid ?
- Does it require non - constructive reasoning in a
constructive logic ?
- Are there claims that would require additional axioms ( e .
g . , excluded middle ) ?

## Output Format

You MUST respond with the following structured format :

‘‘‘ markdown
### Analysis
[ Your detailed analysis of the current proof goals ,
explaining what you observe and any potential issues ]

### Decision
[ PROVABLE , UNPROVABLE , or UNCERTAIN ]

- ** PROVABLE **: The goals appear to be logically valid and
provable with available tactics and lemmas
- ** UNPROVABLE **: The goals contain clear contradictions or
 impossible requirements
- ** UNCERTAIN **: Unable to determine with confidence ; may
require specialized knowledge or techniques

### Reason
[ Brief explanation of your decision , highlighting the key
factors ]

### Suggestion
[ If UNPROVABLE , provide suggestions on how to fix the issue
, such as :
- What hypotheses need to be corrected
- What additional lemmas might be needed
You may include Rocq code blocks with ‘‘‘ rocq for concrete
suggestions .
If PROVABLE or UNCERTAIN , output " N / A "]
‘‘‘

## Important Guidelines

1. Focus on logical validity and provability , not on
finding the optimal proof strategy
2. Be conservative : if you ’ re not sure whether something is
 provable , mark it as UNCERTAIN rather than UNPROVABLE
26    Y. Sun et al.

3. Consider that the proof may require advanced techniques
you ’ re not aware of - don ’ t mark something UNPROVABLE
unless you ’ re confident
4. Check for contradictions carefully - subtle
contradictions can make goals unprovable
5. Consider the constructive nature of Rocq ’ s logic - some
classically true statements may not be constructively
provable
6. Always follow the exact output format for parseability
7. Provide actionable suggestions when marking goals as
UNPROVABLE
8. Remember that " difficult " does not mean " unprovable "

[ User Prompts ]
### Current Goals ...
### Relevant Definitions ...



A.3   Prompts for Induction Schema Evaluation

[ System Prompt ]
# Rocq Induction Evaluation Module

You are an expert Rocq proof assistant specializing in
evaluating induction strategies . Your role is to analyze
whether an induction tactic was applied reasonably and
effectively . Please treat destruct as a weaker form of
induction with no inductive hypothesis .

## Your Task

Given :
1. ** Goal Before Induction **: The original proof goal
2. ** Goal After Induction **: The resulting subgoals after
applying induction
3. ** Induction Strategies **: The specific tactic ( s ) used
for induction strategy ( e . g . , intro + induction pattern )
4. ** Relevant Definitions **: Key definitions from the
codebase that are relevant to understanding the goal
structure and determining the appropriate induction
strategy

You must evaluate whether the induction was performed
reasonably , particularly checking if variables were over -
bound before induction . Use the relevant definitions to
understand the recursive structure of functions and
datatypes involved in the goal .

## Common Issues to Detect
          On Reasoning-Centric LLM-based Automated Theorem Proving   27



### 1. Over - binding Variables
When proving statements like ‘ forall n m , P n m ‘ , if you
introduce both ‘n ‘ and ‘m ‘ into the context before applying
 induction on ‘n ‘ , the induction hypothesis will only apply
 to the specific ‘m ‘ already in the context . This makes the
 induction hypothesis too weak , as it doesn ’ t generalize
over all possible values of ‘m ‘.

** Example of Unreasonable Induction :**
- Goal : ‘ forall n m , n + m = m + n ‘
- UNREASONABLE Tactic : ‘ intros n m . induction n . ‘ ( over -
bound m before induction )
- Problem : The induction hypothesis becomes ‘n + m = m + n
-> S n + m = m + S n ‘ for the specific ‘m ‘ in context ,
rather than ‘ forall m , n + m = m + n -> forall m , S n + m =
 m + S n ‘. This makes the proof impossible or much harder .

** Reasonable Version :**
- Avoid introducing m before induction : ‘ intros n .
induction n . intros m . ‘
- Or use : ‘ induction n ; intros m . ‘
- If already introduced : ‘ intros n m . revert m . induction n
. intros m . ‘

### 2. Wrong Variable for Induction
Choosing to induct on a variable that doesn ’ t appear in the
 toplevel match .

** Example of Unreasonable Induction :**
- Relevant Definitions :
   ‘‘‘ coq
   Fixpoint plus ( n m : nat ) : nat :=
     match n with
     | O => m
     | S p = > S ( plus p m )
     end .
   ‘‘‘
- Goal : ‘ forall n m , n + m = m + n ‘
- UNREASONABLE Tactic : ‘ induction m . ‘ ( note that the
recursive definition of + matches on ‘n ‘ instead of ‘m ‘ in
the toplevel )
- Problem : Inducting on ‘m ‘ does not simplify the ‘ match ‘
expression in the definition of ‘+ ‘ , which matches on ‘n ‘.
This makes the proof much harder .
** Reasonable Version :**
- Should induct on n : ‘ induction n . ‘

#### Hint : ** Induction Should Choose the Variable with
Toplevel Match **
28    Y. Sun et al.



** Key Principle :** When a goal involves a function ,
induction should be performed on the variable that appears
in the ** toplevel match ** of that function ’ s definition .
This aligns the induction with the recursive structure of
the function .

** How to identify the correct variable :**
1. Look at the relevant function definitions in the goal
2. Find the ** toplevel match ** statement ( ignore nested
matches )
3. The variable being matched at the toplevel is the one
you should induct on

** Example 1 - Simple Case :**
‘‘‘ coq
Fixpoint plus ( n m : nat ) : nat :=
   match n with (* toplevel match on n *)
   | O => m
   | S p = > S ( plus p m )
   end .
‘‘‘
- Toplevel match is on ‘n ‘
- ** Correct induction :** ‘ induction n ‘
- ** Incorrect induction :** ‘ induction m ‘ ( m does not appear
 in toplevel match )

** Example 2 - List Append :**
‘‘‘ coq
Fixpoint app ( A : Type ) ( xs ys : list A ) : list A :=
   match xs with (* toplevel match on xs *)
   | nil = > ys
   | cons x xs ’ = > cons x ( app A xs ’ ys )
   end .
‘‘‘
- Toplevel match is on ‘xs ‘
- ** Correct induction :** ‘ induction xs ‘
- ** Incorrect induction :** ‘ induction ys ‘ ( ys does not
appear in toplevel match )

** Example 3 - Nested Matches :**
‘‘‘ coq
Fixpoint some_function ( n m : nat ) : nat :=
   match n with (* toplevel match on n - this determines
   induction variable ! *)
   | O = > match m with (* nested match - ignore for
   induction choice *)
           | O => 0
           | S m’ => m
           end
          On Reasoning-Centric LLM-based Automated Theorem Proving   29

  | S n ’ = > S ( some_function n ’ m )
  end .
‘‘‘
- Toplevel match is on ‘n ‘ ( the nested match on ‘m ‘ is
irrelevant )
- ** Correct induction :** ‘ induction n ‘
- ** Incorrect induction :** ‘ induction m ‘ ( m only appears in
 nested match )



### 3. Over - binding Multiple Variables
When multiple variables appear after the induction variable
, over - binding all of them before induction makes the
induction hypothesis too weak .

** Example of Unreasonable Induction :**
- Goal : ‘ forall n m k , n + ( m + k ) = ( n + m ) + k ‘
- UNREASONABLE Tactic : ‘ intros n m k . induction n . ‘ ( over -
bound m and k )
- Problem : The induction hypothesis is too weak - it only
proves the property for the specific m and k in context ,
not for all m and k

** Reasonable Version :**
- Should avoid over - binding m and k : ‘ intros n . induction n
. intros m k . ‘
- Or use : ‘ induction n ; intros m k . ‘

** Another Example :**
- Goal : ‘ forall xs ys zs , app xs ( app ys zs ) = app ( app xs
ys ) zs ‘
- UNREASONABLE Tactic : ‘ intros xs ys zs . induction xs . ‘ (
over - bound ys and zs )
- Problem : The induction hypothesis won ’ t be strong enough
to handle arbitrary lists ys and zs

** Reasonable Version :**
- Should use : ‘ induction xs ; intros ys zs . ‘ or ‘ intros xs .
induction xs . intros ys zs . ‘


## Output Format

You MUST respond with the following structured format :

‘‘‘ markdown
### Analysis
30      Y. Sun et al.

[ Your detailed analysis of the induction strategy ,
explaining what was done and why it may or may not be
reasonable ]

### Decision
[ REASONABLE or UNREASONABLE ]

### Reason
[ Brief explanation of your decision ]

### Suggestion
[ If UNREASONABLE , output in the following form :
‘‘‘ coq
[ the reasonable version of the tactic sequence ]
‘‘‘
If REASONABLE , output " N / A "]
‘‘‘

## Important Guidelines

1. Focus on whether the induction hypothesis will be strong
 enough to complete the proof
2. Check if universally quantified variables that appear
after the induction variable were over - bound ( introduced
before induction when they shouldn ’ t be )
3. Consider the structure of the goal and what the
induction hypothesis needs to prove
4. Be specific in your suggestions - provide actual Rocq
tactic syntax
5. Always follow the exact output format for parseability
6. Look at ‘ Relevant Definitions ‘ why checking ‘ Wrong
Variable for Induction ‘
7. Think carefully for a good answer .
8. Wrap the code in a ‘‘‘ rocq code block in the suggestion
part .
9. Provide ONLY ONE better version of tactic sequence .

[ User prompts ]
### Goal Before Induction ...
### Goal After Induction ...
### Induction Strategies ...
### Relevant Definitions ...



A.4     Prompts for Building Retrieval Database for Lemmas

     [System Prompt]
     You are an expert in Rocq theorem proving . Your task is
     to generate a concise natural - language description for
          On Reasoning-Centric LLM-based Automated Theorem Proving   31

  the given lemma . You will be provided with the lemma
  statement and the definitions of all terms in the lemma
  statement . Your description should explain : (1) what the
  lemma states , and (2) the scenarios in which this lemma
  is typically used .
  [User Prompt]
  ### Lemma Statement ...
  ### Definitions ...




A.5   Prompts for Retrieving Lemmas and Proofs


  [System Prompt]
  You are an expert in Rocq theorem proving . Your task is
  to generate a concise natural - language step - by - step proof
    plan for the given subgoal . You will be provided with
  the subgoal , as well as the definitions of all terms in
  the subgoal . Your plan should be in natural language .
  Please generate in the following format :
  < step > The step 1 description </ step >
  < step > The step 2 description </ step >
  ...
  [User Prompt]
  ### Subgoal ...
  ### Definitions ...




A.6   Prompts for Building Retrieval Database for Proofs


[System Prompt]
You are an expert in Rocq theorem proving . Your task is to
generate a concise natural - language step - by - step proof plan
  for the given subgoal . You will be provided with the
subgoal , the formal proof to this subgoal , and the
definitions of all terms in the subgoal and the proof . Your
  plan should be in natural language . Please generate in the
  following format :
< step > The step 1 description </ step >
< step > The step 2 description </ step >
...
[User Prompt]
### Subgoal ...
### Formal Proof ...
### Definitions ...
32     Y. Sun et al.

B    Details in Reflection

Below, we present the complete list of ReflCat. The set ReflCat consists of the
following categories of tactics:
 – Introducing auxiliary subgoals: assert, have, pose.
 – Applying lemmas: apply, eapply.
 – Choosing a proof branch: left, right.
 – Induction-related tactics: induction, destruct, case, elim.
