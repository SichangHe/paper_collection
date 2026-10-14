                                                                 A Natural Formalized Proof Language

                                                                         Lihan Xie, Zhicheng Hui, and Qinxiang Cao(B)

                                                                         Shanghai Jiao Tong University, Shanghai, China
                                                               {sheringham,laplace demon}@sjtu.edu.cn, caoqinxiang@gmail.com



                                               Abstract. Artificial intelligence assisted mathematical proof has become a highly focused area nowa-
                                               days. One key problem in this field is to generate formal mathematical proofs from natural language
                                               proofs. Due to historical reasons, the formal proof languages adopted by traditional theorem provers
arXiv:2405.07973v1 [cs.PL] 13 May 2024




                                               were not intended to represent natural language proofs. Therefore, they are not well-suited for the
                                               aforementioned tasks and proof-checking work for educational purposes. In this paper, we design a
                                               proof language and its corresponding abstract syntax tree and implement a proof checking tool for it.
                                               This language can be easily converted from natural language, thus providing a rich corpus of formal
                                               proof. Additionally, it supports the handling of issues in informal proofs through static analysis, and
                                               enhances the expressive power of the language by introducing the structure of partial proofs. This
                                               design combines the expressiveness of natural language and the accuracy of formal language, resulting
                                               in an improved mathematical proof language.

                                               Keywords: Formal proof language · Theorem proving · Static analysis


                                         1   Introduction
                                         Formal mathematical proofs are based on rigorous reasoning in formal logic, providing a completely accurate
                                         proof process that can be automatically verified by computers. Formalizing informal proofs can make them
                                         more convincing, as seen in the formal proof of the Four-Color Theorem[1,10]. Additionally, automated
                                         theorem proving relies on formal proof languages to generate rigorous proofs. The rise of large language
                                         models in recent years has spurred research in AI-assisted mathematical proof, particularly in the fields of
                                         automated theorem proving and transforming informal proofs into formal proofs[13,19]. This means that
                                         large language models can directly generate formal proofs or indirectly transform natural language proofs
                                         into formal proofs. These formal proofs can then be verified by theorem provers, ensuring their correctness.
                                             Due to historical reasons, early versions of theorem provers were primarily focused on ensuring the
                                         correctness of proofs, rather than directly modelling natural language proofs. Subsequent developments,
                                         such as the Ltac[8] tactic language in Coq[2] and Isar[18] proof language in Isabelle[15], aimed to help
                                         with proof constructions. Commands in these languages can be seen as transformations that modify the
                                         current proof goal, where each proof goal comprises named premises and the conclusion that needs to be
                                         proved. However, it is still difficult to translate natural language proofs word-for-word into such formal proof
                                         languages. Consequently, for current applications like AI-assisted mathematical proofs or automated proof
                                         grading for educational purposes, these formal languages seem to be insufficient.
                                             In the following example shown in Fig.1 about the proof of the monotone convergence theorem through
                                         the supremum theorem, we can observe several characteristics of natural language proofs and the difficulties
                                         consequent upon the task of formalization using existing formal proof languages like Coq. We will also
                                         demonstrate how our work circumvents these difficulties.




                                         L. Xie and Z. Hui contributed equally to this work.
    Monotone Convergence Theorem: For every sequence of real numbers (an )n∈N , (an )n∈N converges if it is
    monotonically increasing and bounded above.

    Proof. (1) Assume (an )n∈N is monotonically increasing and bounded above.
       (2) By supremum theorem, there exists A such that A = sup{an }.
       (3) We use the definition of limit to show that lim an = A.
                                                      n→+∞
       (4) For every ε > 0, by the definition of least upper bound, there exists an integer N such that aN > A−ε.
       (5) Since {an } increases, for every n, n > N implies an > aN .
       (6) Since A is an upper bound of (an )n∈N , for every n, n > N implies an < A.
       (7) Consequently, for every n, n > N implies A − ε < an < A + ε.
       (8) By the definition of convergence, we have lim an = A,
                                                     n→+∞
       (9) which proves the theorem.


                                 Fig. 1. Proof of monotone convergence theorem.



Partial Transformation of Proof Goal. The concept of proof goal models the task of a mathematical
   proof, i.e. deriving the conclusion from premises and proven results. Following the steps of a proof,
   we implicitly transform the proof goal by introducing new variables, proving intermediate results, or
   posing subgoals. For example, we pose a subgoal in line 3, thereby transforming the proof goal into two
   subsequent proof goals: (1) proving lim an = A, (2) and proving the conclusion with the intermediate
                                          n→+∞
    result   lim an = A proven. However, there are circumstances where the subsequent proof goal cannot
             n→+∞
  be found directly: We pose an assumption ϵ > 0 in line 4 and derive the result ∀n > N, A−ϵ < an < A+ϵ
  in line 7 under the assumption. The overall process proves the result ∀ϵ > 0, ∃N ∈ N, ∀n > N, A − ϵ <
  an < A + ϵ, which is not explicitly stated in line 4. Consequently, the transformation of the proof goal
  in line 4 is partial. Since each tactic in tactic languages should represent a clearly defined, complete
  transformation of the current proof goal, formalizing the proof using tactic languages would involve the
  extra task of determining the subsequent proof goal. For example, by inferring the proposition to be
  filled in a Coq “assert” tactic. In our work, a structure of partial proof is included in the design of proof
  language to model this pattern of proof, it eliminates the need for additional inferences or structural
  modifications on the proof during the task of formalization.
Context-dependent Semantics. Depending on the context, the same natural language statement could
  have multiple interpretations, of which the semantic differences may be subtle. For example, when we
  write “there exists” in the proof, at least three interpretations are possible. (1) In the context of proving
  an existential statement, a satisfying value has been found for one of the existential quantifiers in the
  conclusion to be proved, (2) or a proposition beginning with an existential quantifier is stated, (3) or
  similar to the second case, except that the qualified variable becomes a free variable and can be used later,
  as in line 2 and line 4 of the example, where variables A and N are used in line 3 and line 5, respectively.
  In order to use the tactic language of Coq, all those semantic variances must be explicitly formulated.
  Namely by an “exists” tactic for the case (1), an existentially quantified variable in the proposition for
  the case (2) and a free variable in the proposition for the case (3). Determining the correct semantic
  interpretation would require analysing the context during the process of formalization. Not only is such
  an hidden task of analysis generally harder to perform on an unstructured natural language proof, but
  it is also indirect on a tactic proof, as tactics do not explicitly contain information on proof goals. That
  explains the difficulties faced by the tactic languages as object languages of automatic formalization.
  In our work, the proof language is designed to resemble natural language in order to streamline the
  formalization. Moreover, the resemblance allows the proof language to temporarily preserve the context-
  dependent semantics, thus allowing the resolution to be postponed until we can perform static analysis
  on the formalized version of the proof.
Overloading of Notation. Sometimes a notational convention may be employed though not being mathe-
  matically rigorous. For example, the appearance of {an } in line 2 and line 5 does not represent a singleton


                                                         2
    but rather the set containing all elements of the sequence a. Another typical example is the extensive
    usage of f (x) for representing the function f itself. Similar to context-dependent semantics, all mathe-
    matical formulas should be written rigorously in Coq. By performing static analysis on the entire formal
    proof, the precise meaning of each expression can also be inferred.

    In summary, to address the problems mentioned above, we design a natural-language-like formal proof
language for modeling mathematical proofs. We add partial proof structures to make them more similar
to the natural language proofs. Furthermore, after transforming the natural formal proof into an abstract
syntax tree by a parser, we can perform static analysis on it to resolve context-dependent semantics and
overloading of notation.
    Accordingly, we implement a framework called ProofGrader for checking mathematical proofs auto-
matically. For each step of reasoning, corresponding solvers are chosen heuristically in order to check its
correctness. Apart from the proof checking kernel, the rest of the system is designed to be highly modular
so that our system may fit into different usage scenarios: It is possible to alter the mathematical objects
and the usable theorems involved in the proof, the acceptable forms of proof steps, or the solvers used for
checking. For example, to serve educational purposes, mild solvers fitting the level of human intuition can
be plugged in instead of powerful ones, and advanced theorems can be temporarily disabled until they are
proved or taught later.
    In the rest of this paper, we will first present the design of our proof language in Section 2, with elab-
orations on several important elements. After that, we give the formal semantics of our proof language in
Section 3. We then show the schema of the workflow of our checker in Section 4. A detailed description of
our solvers is developed in Section 5. Section 6 gives an evaluation of the proof checker. And then we will
introduce some related works in Section 7. Finally, Section 8 is devoted to a conclusion.


2   Proof Language Design

We focus on defining a natural-language-like proof language, whose structure faithfully reflects that of natural
language. Thus, our natural formal proof language is provided with the hierarchy of natural language proof.
At the top level are proof steps, what follows are propositions and terms. A certain amount of investigations
of natural language proofs are done to incorporate common proof patterns within our proof language. Such a
proof language follows predefined grammar rules but can be read directly as natural language, an explanation
of its grammar can be found in Appendix A.
    To perform proof checking, the natural formal proof language is further translated into an abstract syntax
tree via a parser. Below shows a subset of its definitions. The definitions related to term and prop can be
found in the Appendix B.

⟨proof ⟩ ::= ‘ProofAction’ ⟨action⟩ ⟨proof ⟩          ⟨bwd ⟩ ::= ‘BNoHint’
  | ‘PoseWithoutProof’ ⟨fwd ⟩ ⟨prop⟩ ⟨proof ⟩           | ‘BContra’
  | ‘PoseAndProve’ ⟨fwd ⟩ ⟨prop⟩ ⟨proof ⟩ ⟨proof ⟩      | ...
  | ‘ClaimSuffice’ ⟨bwd ⟩ ⟨prop⟩ ⟨proof ⟩
  | ‘ProveSuffice’ ⟨bwd ⟩ ⟨prop⟩ ⟨proof ⟩ ⟨proof ⟩    ⟨action⟩ ::= ‘AIntros’ ⟨identifier ⟩
  | ‘ConclWithoutProof’ ⟨fwd ⟩                          | ‘AExists’ ⟨term⟩
  | ‘ConclAndProve’ ⟨fwd ⟩ ⟨proof ⟩                     | ‘ASuppose’ ⟨prop⟩
  | ‘PosePartialProof’      ⟨poseAction⟩     ⟨proof ⟩   | ‘ASet’ ⟨identifier ⟩ ⟨term⟩
     ⟨proof ⟩                                           | ‘ASetProp’ ⟨prop⟩
  | ‘EndPartialProof’                                   | ‘AExistVar’ ⟨identifier ⟩

⟨fwd ⟩ ::= ‘FNoHint’                                       ⟨poseAction⟩ ::= ‘APoseVar’ ⟨identifier ⟩ {prop}∗
  | ‘FDefinition’ ⟨definition⟩                               | ‘APoseProp’ ⟨prop⟩
  | ‘FTheorem’ ⟨theorem⟩
  | ‘FAddEqn’ {identifier }∗
  | ‘FDeriBothTerms’ ⟨identifier ⟩
  | ...
                                                       3
In the following, we will explain the meaning of each proof structure. We will refer to the names of abstract
syntax tree nodes because these names correspond to components of the proof language. Some of our proof
structures have similar functionalities to those of certain tactic language, while others have no counterpart,
which enables us to better express natural language proof.

ProofAction The field action constitutes an operation on the proof goal, and the field proof refers to
subsequent proof steps.
    The design of ProofAction refers to some tactic languages, such as the tactic intro and exists of Coq[3],
which deal with the quantifiers in the proposition to be proved. That corresponds to our proof action
AIntros and AExists. However, the variety of proof actions is richer than that of tactic language. For
example, ASuppose introduces a premise in the conclusion rather than a variable, which is also expressed
by the tactic intro in Coq. Such a difference is due to the fact that the proof language models the natural
language directly, and thus is more in line with human intuition.
    ASet binds a name to a term, to which the proof can refer later, and the existence of the term will be
verified by the checker to ensure mathematical rigor.
    ASetProp is a generalization of ASet. Instead of introducing a new variable through an equation, ASetProp
introduces new variables through a proposition. Fig.2 below contrasts the usage of these two proof actions,
the one-to-one correspondence between natural language and our proof language is marked in background
color.
    Finally, AExistVar indicates the action of instantiating the variable mentioned by an existential quantifier
in the last premise in the proof goal. The usage of AExistVar is further demonstrated in Section 4.3 when
we perform static analysis.




                                        Fig. 2. Example of ProofAction.


In the upper part of Fig2, the variable A is set equal to the limit of a sequence, the checker then verifies
whether the limit exists. In the lower part, a variable k is introduced implicitly due to the introduction of
a subsequence, the checker then verifies whether (an )n∈N admits a convergent subsequence. Both of the two
proof steps will add corresponding assumptions to the proof goal.


                                                       4
PoseWithoutProof & PoseAndProve These two components correspond to forward reasoning. The field fwd
indicates the method involved in forward reasoning. The field prop denotes the proposition that the step
proves. The last field proof still refers to subsequent proof steps.
    Depending on the complexity of the reasoning, one may choose to provide a proof as a justification of
the reasoning or just let the checker figure it out. This makes the difference of PoseWithoutProof and
PoseAndProve. PoseAndProve carries an extra field prop, which is a complete proof showing how to derive
its result. This design is also widespread in tactic languages. An example is the tactic assert in Coq, which
poses a subgoal to be proved. Fig.3 shows its usage scenario, which corresponds to the line 3 of Fig.1.




                                       Fig. 3. Example of PoseAndProve.


Since the hint of using the definition of limit is far from sufficient to prove the result, an additional proof is
provided to complete this task. The proven subgoal is then available in the subsequent proof.
   The set of possible methods fwd is rather rich. To name a few, FTheorem denotes applying a theorem,
FAddEqn denotes adding several equations together to get a new one, and FDeriBothTerms denotes taking a
derivative from both sides of an equation. If no method is indicated, FNoHint is filled in. It is quite easy to
incorporate new methods so this set is highly expandable.

ClaimSuffice & ProveSuffice These two components correspond to backward reasoning. The first field bwd
indicates the method involved in backward reasoning, the second field prop denotes the proposition the
step proves and the last field proof refers to subsequent proofs. The distinction between ClaimSuffice and
ProveSuffice follows that between PoseWithoutProof and PoseAndProve.
   Backward reasoning signifies that they start from the conclusion to be proved. The result provided is
supposed to imply goal, which will then become the new goal.

ConclWithoutProof & ConclAndProve These two components correspond to the step of deriving the conclu-
sion and terminating the proof, only a field fwd is presented to indicate the method involved. ConclAndProve
allows the choice of presenting an extra explanatory proof when the derivation of the conclusion is not im-
mediate.
    Basically, ConclWithoutProof corresponds to the last step of the proof, such as the line 9 “which proves
the theorem” in Fig.1, and does not carry much information. But such a concluding remark imitates natural
language proof, and the similarity to natural language characterizes our proof language.

PosePartialProof & EndPartialProof In theorem provers, we always need to explicitly keep a record of the
current proof goal. In most cases, this is the overall proposition to be proved. We can also pose a subgoal
and prove it subsequently, a process represented by the PoseAndProve component in our proof language.
   As discussed in Section 1, natural language proofs may also involve partial transformations of the proof
goal, in the sense that subgoals are not explicitly stated in advance. Instead, We simply pose certain as-
sumptions and proceed to derive the subgoals. Refer to Fig.4 for an illustration of how the different forms


                                                        5
of proof goal are in the example Fig.1. The dark gray part of the proof denotes what we term as a “partial
proof”, aligning with the PosePartialProof and EndPartialProof components in our proof language.
    The notion of partial proof can be considered as one innovation of our proof language. Compared with
tactic languages, it offers us extra convenience in modelling natural language proofs.




                               Fig. 4. Illustration of how the proof goal changes.



A partial proof starts with a list of variables and propositions, which then become the temporary assumptions.
This information is carried by the first field poseAction is the grammar. APoseVar poses a new temporary
variable along with related assumptions, while APoseProp poses a proposition. The former field proof carries
the partial proof, which shall be terminated by EndPartialProof. After the termination of partial proof, all
proven propositions will be altered to its proper form — without free variables. These altered propositions
will become henceforth available in the subsequent proof — the latter field proof.
    In Fig.4, the variable ε and the proposition ε > 0 are posed to start a partial proof. When reaching the
result ∀n > N, A − ε < an < A + ε at the end of the partial proof, it is expanded to ∀ε > 0, ∀n > N, A − ε <
an < A + ε, which is subsequently used to prove convergence. Fig.5 shows the how a partial proof looks like,
which corresponds to line 4 of Fig.1.




                                     Fig. 5. Example of PosePartialProof.




                                                       6
3   The Formal Semantics of Proof Language

In this section, we demonstrate a selected set of the formal semantics of our proof language. Since each proof
step defines a transformation of the proof goal, we use the notation (pr, pg) → (pr′ , pg ′ ) to denote that the
proof goal pg ′ results from the proof goal pg after one or more proof steps in pr, with pr′ continuing the
proof. A proof goal is defined as a pair (A, C), where A is a list of premises and C a conclusion that needs
to be proved. In the case of partial proof, the conclusion C does not exist and we note it as □.
    For convenience, we represent a list of premises as a set of propositions, and we write the triple (pr, A, C)
to represent the pair (pr, (A, C)). We use the notation F V (A) to denote the set of free variables in the set
of propositions A, the same notation F V (t) is also used to denote the set of free variables in the term t. We
also define a constant QED such that the proof is successfully completed when (pr, A, C) = QED.

Proof Action
                                        v∈/ F V (A ∪ {∀x.C})
                                                                                 Intros
                         (ProofAction (AIntros v) pr, A, ∀x.C) → (pr, A, C[v/x])

                                      F V (t) ⊂ F V (A ∪ {∃x.C})
                                                                                 Exists
                         (ProofAction (AExists t) pr, A, ∃x.C) → (pr, A, C[t/x])

                                       PropEquivalent P Q
                                                                                  Suppose
                     (ProofAction (ASuppose P ) pr, A, Q ⇒ C) → (pr, A ∪ {P }, C)

                               TermWellDefined t A v ∈   / F V (A ∪ {C})
                                                                                  Set
                         (ProofAction (ASet v t) pr, A, C) → (pr, A ∪ {v = t}, C)

                                       PropWellDefined P A
                                                                                 SetProp
                        (ProofAction (ASetProp P ) pr, A, C) → (pr, A ∪ {P }, C)

                                  v∈/ F V (A ∪ {∃x.P } ∪ {C})
                                                                                             ExistVar
           (ProofAction (AExistVar v) pr, A ∪ {∃x.P }, C) → (pr, A ∪ {∃x.P } ∪ {P [v/x]}, C)

Proof actions are proof steps that directly manipulates the proof goal, usually when some conditions are
met. In the semantic definitions above, PropEquivalent P Q means the proposition P and Q are equivalent,
TermWellDefined t A means the term t is well-defined under the set of premises A, and PropWellDefined P A
means the proposition P is well-defined and satisfied under the set of premises A. These predicates are
implemented as functions within our proof checking system, however, they are too cumbersome to define
formally.
    The behavior of AIntros v is to remove the universal quantifier in the conclusion ∀x.C and replace the
variable x in C by the variable v, when the variable v does not occur freely in the proof goal. Similarly, the
behavior of AExists t is to remove the existential quantifier in the conclusion ∃x.C and replace the variable
x in C by the term t, when the term t does not contain free variables other than those in the proof goal.
And the behavior of ASuppose P is to remove the implication in the conclusion Q ⇒ C and add P to the
premises when P and Q are equivalent propositions.
    ASet v t adds the equation v = t to the premises, where v does not occur freely and the term t must
be well-defined in the proof goal. The requirement for well-definiteness ensures that a term does not appear
before its existence has been proved in the proof goal. The behavior of ASetProp P is similar, it incorporates
the proposition P possibly containing new variables into the premises. This can be useful when P is not an
equation.
    Finally, when the last premise in the proof goal is an existential proposition, the statement AExistVar v
instantiates the existential quantifier with the variable v, by adding the properties verified by v to the
premises. It is required that the variable v does not occur freely in the proof goal.


                                                       7
Direct Forward Proof

                                       PropDeducible P A
                                                                                NoHint
                      (PoseWithoutProof FNoHint P pr, A, C) → (pr, A ∪ {P }, C)

                                  TheoremApplicable thm P A
                                                                                   ApplyTheorem
                  (PoseWithoutProof (FTheorem thm) P pr, A, C) → (pr, A ∪ {P }, C)

                                                                                       Concl
                          (ConclWithoutProof FNoHint, A ∪ {C}, C) → QED
                                    TheoremApplicable thm C A
                                                                        ConclWithTheorem
                         (ConclWithoutProof (FTheorem thm), A, C) → QED

The predicate PropDeducible P A indicates that the proposition P can be deduced from the set of premises
A. Similarly, TheoremApplicable thm P A signifies that the theorem thm can be applied to the set of
premises A to yield the result P . It is important to note that the notion of deducibility here is algorithmic
rather than theoretical: a proposition is considered deducible if it can be derived using our predefined set of
solvers within a specified number of steps. The applicability of theorem is also defined by the theorem checker
in our implementation. Again, we do not provide formal definitions but give descriptions in the following.
    The behavior of PoseWithoutProof FNoHint depends largely on the solvers. In the process of proof
checking, the checker will send the proposition P and the current proof goal (A, C) to the solver manager,
which checks whether the proposition P can be derived. Then, the checker adds P to the premises of the
proof goal, and checks the rest of the proof pr.
    Similarly, the behavior of PoseWithoutProof (FTheorem thm) depends on the theorem checker in
our implementation. The theorem checker checks two aspects: (1) whether the prerequisites for applying the
theorem thm are satisfied, (2) and whether P can be derived as a conclusion from the theorem under those
prerequisites.
    The working process of the theorem checker begins with a pattern match between P and the conclusion
of the theorem thm. This pattern match instantiates the variables and identifies the prerequisites of the
theorem. Then, the theorem checker searches in the proof goal to see if all the prerequisites are satisfied.
If the theorem checker is unable to match the conclusion or find all the prerequisites, then this step of
transformation cannot be realized.
    ConclWithoutProof FNoHint transforms the proof goal into QED when the conclusion appears in
the premises. ConclWithoutProof (FTheorem thm) does the same transformation when the conclusion
follows from the theorem thm by the theorem checker.
    The Table 1 shows how the proof goal gets transformed when reaching line 2 of Fig.1, where we apply
the supremum theorem.


                                Premises                               Conclusion

                 {an } has an upper bound
                 {an } is monotonically increasing          there exists A such that A = lim an
                                                                                       n→+∞

                 + there exists A such that A = sup{an }

Table 1. Transformation of proof goal when reaching line 2 of the proof in Fig.1. The proposition marked with + is
added by the transformation of line 2.




                                                        8
Subgoal Forward Proof
                                       (pr, A, P ) → QED
                                                                                   Subgoal
                      (PoseAndProve FNoHint P pr pr′ , A, C) → (pr′ , A ∪ {P }, C)
The subgoal proof statement PoseAndProve FNoHint adds the proposition P to the premises on the
condition that the proof of the subgoal is successfully completed. In the process of proof checking, the
checker first checks the subgoal proof, and then returns to the main proof with the proven result.
   The Table 2 shows how the proof goal gets transformed when reaching line 3 of Fig.1, where the lines 3-8
constitutes a typical subgoal proof. It generates a new proof goal and provides a proof for it. The subgoal
gets added to the premises as the newly added proof succeeds.


                                 Premises                             Conclusion

                   {an } has an upper bound              there exists A such that A = lim an
                   {an } is monotonically increasing                                 n→+∞

                   there exists A such that A = sup{an }
                   A = sup{an }                                       A = lim an
                                                                          n→+∞


Table 2. Transformation of proof goal when reaching line 3 of the proof in Fig.1. The premises remain unchanged,
but a new conclusion is generated.




Partial Proof
                 (pr, A ∪ sP, □) → (EndPartialProof, A′ , □) F V (sP ) ⊂ F V (A ∪ {C}) ∪ {s}
                                                                                                             PoseVar
       (PosePartialProof (APoseVar s sP ) pr pr′ , A, C) → (pr′ , A ∪ (AddVarDep (A′ \ (A ∪ lP )) s sP ), C)
                 (pr, A ∪ {P }, □) → (EndPartialProof, A′ , □) F V ({P }) ⊂ F V (A ∪ {C})
                                                                                                          PoseProp
       (PosePartialProof (APoseProp P ) pr pr′ , A, C) → (pr′ , A ∪ (AddPropDep (A′ \ (A ∪ {P })) P ), C)
 A partial proof first makes one or more assumptions and then deduces a series of results. After the partial
proof terminates, these results are added with dependencies on the assumptions, by prefixing them with
universal quantifiers and prerequisite conditions. The assumptions can be either (1) posing a new variable
satisfying certain conditions, (2) or posing a hypothesis on the existing variables of the proof goal. These
two cases correspond to the constructs APoseVar s sP and APoseProp P defined above, where s refers
to the name of the posed variable, sP a set of assumptions on the posed variable and P an assumption on
existing variables. The two operators AddVarDep and AddPropDep add dependencies on the assumptions
to the results derived during the partial proof. Similar to the subgoal proof, a PosePartialProof statement
causes the checker to first check the partial proof. After reaching EndPartialProof, which marks the end of
the partial proof, the checker integrates the proof goal back to the main proof by modifying all the derived
premises.
    The Table 3 shows how the proof goal gets transformed between lines 4-7 in Fig.1, which represents a
partial proof structure. It first makes an assumption ϵ > 0 and then deduces several results. After that, these
results are added with a prefix ∀ϵ > 0 to indicate their dependency on the assumption ϵ > 0.

4     The Workflow of ProofGrader
4.1   Overall Architecture
In this subsection, we will primarily introduce the overall working framework of ProofGrader. Fig.6 illustrates
how the natural formal proof is processed step by step in our proof checking system to obtain the final result.
A larger figure can be found in Appendix C for greater clarity.


                                                         9
                                               Premises                                    Conclusion

              {an } has an upper bound
              {an } is monotonically increasing                                            A = lim an
              there exists A such that A = sup{an }                                             n→+∞

              A = sup{an }

              + ϵ > 0 (partial proof start)
              + there exists N such that aN > A − ϵ
              + for all n, if n > N then an > aN                                                 □
              + for all n, if n > N then an < A
              + for all n, if n > N then A − ϵ < an < A + ϵ (partial proof end)
              - Remove all the premises added above
              + for all ϵ > 0, there exists N such that aN > A − ϵ
              + for all ϵ > 0, there exists N such that for all n, if n > N then an > aN A = n→+∞
                                                                                              lim an
              + for all n, there exists N such that if n > N then an < A
              + for all n, there exists N such that if n > N then A − ϵ < an < A + ϵ

Table 3. Transformation of proof goal between lines 4-7 in Fig.1. The upper part of the table shows the proof goal
before reaching line 4 of the proof. The middle part of the table shows the deduction of intermediate results during
the partial proof. The lower part of the table shows the proof goal after terminating the partial proof in line 7 of the
proof.




    The modules described in the squares of the diagram are the main components of ProofGrader, which
include the parser, static analyser, and proof checker. These three parts will be discussed in detail in the
following. The other process boxes represent different forms of mathematical proof during the whole workflow.
We utilize a parser to convert the natural formalized proof into an abstract syntax tree, and then perform
static analysis on the abstract syntax tree to eliminate ambiguities and add omitted steps. The checker takes
in the proof goal generated by the static analyser along with the complete abstract syntax tree, and checks
the proof step by step by predefined rules. Finally, it confirms whether the proof goal has been proven and
generates the final result.


4.2   Proof Parsing

Proof parsing is the first step of the entire workflow of ProofGrader. Since the design of our proof language
also takes a large part into account readability factors, it may not be the most convenient for the subsequent
checking process. Therefore, we will first convert the natural formal proof into an abstract syntax tree
described in Section 2. In our implementation, the lexer and parser are realized by flex and bison [9,14].
    The parser simply performs a plain translation based on the grammar rules, without making any further
modification on the proof structure or the formulation of proposition. These are the subjects of the next
section where we will discuss the static analysis on the proof.


4.3   Static Analysis

As discussed in Section 1, natural language proofs exhibit complexities such as context-dependent semantics
and overloading of notation. Given the close resemblance of our proof language to natural language and the
direct translation performed by the parser, these properties will be carried into the natural formal proof, and
then the abstract syntax tree. Performing static analysis on the abstract syntax tree allows us to eliminate
these problems by reorganizing the proof into a more rigorous form, ready to be checked by the proof checker.


                                                          10
                                    Fig. 6. Overall workflow of ProofGrader.


    The static analyser tackles each kind of problem separately with ad hoc method. For one problematic
proof step, proposition or expression, the task is to choose the right semantic between all the possible
interpretations. The static analyser works by first inferring how the current proof step transforms the proof
goal, based on the previous and subsequent proof goals. It then selects the semantic corresponding to this
transformation, by elaborating the proof step, proposition or expression into a proper form. Judging from
the problems we are currently solving by static analysis, most of them are accompanied by the appearance
of free variables. So it is often the case to perform a lexical scope analysis.

Handling Context-dependent Semantics. The context-dependent semantics we currently address are stated
in the descriptions of Fig.1. In this example, the static analyser infers the correct semantic from the context,
as shown in the inference steps below. As a reminder, the three possible interpretations of “there exists A
such that A = sup{an }” are respectively: (1) a value sup{an } has been found for an existential quantifier in
the conclusion to be proved, (2) an intermediate result ∃A = sup{an } is stated, where A is qualified by a
quantifier, (3) a variable A is given the value sup{an } after proving the existence of this supremum.
                                                                                analyser
                     interpretation (1)         proof goal beginning with ∃                False


                                                                               analyser
                     interpretation (2)           A unbounded thereafter                   False


                                                                               analyser
                     interpretation (3)             A bounded thereafter                   True

The three potential semantic interpretations appear syntactically identical in the proof. Therefore, the static
analyser takes the responsibility for reflecting the result of the above analysis on the abstract syntax tree
through modification. This is where the proof action AExistVar comes into play. Placed immediately after
a proposition starting with an existential quantifier, it indicates the instantiation of the variable mentioned
by the quantifier, thus bringing about the semantics corresponding to case (3), namely binding variable A
of the value.


                                                      11
  Algorithm 1 illustrates the procedure of handling context-dependent semantics in the cases of Pose-
WithoutProof and PoseAndProve, the processing of other cases follows a similar approach.

Algorithm 1 HCDS: Handling Context-dependent Semantics
Input: the original proof P r before static analysis
Output: the modified proof with ontext-dependent Semantics eliminated
  When P r = PoseWithoutProof f wd P 0 P r0
         P 0 = PQuant exists “x” P 1
         “x” occur freely in P r0
  Then HCDS(P r) = PoseWithoutProof f wd P 0 (ProofAction (AExistVar “x”) HCDS(P r0))

  When P r = PoseAndProve f wd P 0 P r0 P r1
        P 0 = PQuant exists “x” P 1
        “x” occur freely in P r1
  Then HCDS(P r) = PoseAndProve f wd P 0 (HCDS(P r0) (ProofAction (AExistVar “x”) HCDS(P r1))
  ...

Handling Overloading of Notation. If there is only one possible interpretation for notation overloading, there
is no need for analysis and the static analyser simply restores its rigorous form. So far, the cases we have
encountered with multiple possible interpretations for notation overloading all involve the use of formal
variables. In such cases, the static analyser examines the appearance of free variables. As an example, the
{an } in line 2 of Fig.1 admits two possible interpretations: (1) the singleton {an }, (2) or a set containing
all elements of the sequence a. The correct interpretation depends on whether the variable n is bound to a
value in the current proof goal. Similarly, if x is identified as a free variable in the proof goal, f (x) will be
transformed into either f or λx.f (x), rather than the value of x applied to the function f .
    Algorithm 2 illustrates the procedure for handling the notation overloading of f (x) in the cases of Pose-
WithoutProof and ProofAction (ASet x t), the processing of other cases follows a similar approach.

Algorithm 2 HON: Handling Overloading of Notation
Input: the original proof pr before static analysis
      the list of binded variables binded varlist from the beginning to the current point of the proof
Output: the modified proof with overloading of notation eliminated
  When P r = PoseWithoutProof f wd P 0 P r0
          P 0 = Eq (TApply (“f ”) (“x”)) t1
          if “x” is not in binded varlist
  Then HON(P r, binded varlist) = PoseWithoutProof f wd (Eq (f ) (TBinder Lambda “x” t1)) HON(P r0,
  binded varlist)

  When pr = ProofAction (ASet “x” t) P r0
  Then HON(P r, binded varlist) = ProofAction (ASet “x” t) HON(P r0, x :: binded varlist)
  ...


4.4   Proof Checking

Proof checking is the final step of the entire workflow of ProofGrader. The checker takes the proof and the
proof goal elaborated by the static analyser as input. For each proof step, the checker takes the current
proof goal and checks the step according to the formal semantics presented in Section 3, it computes the
subsequent proof goal along with a boolean value indicating whether the step is accepted. By iteratively
repeating this process, the proof checker finally generates a list of boolean values indicating the correctness
of each proof step. In order to help with proposition checking, we also develop several solvers and a solver
manager system. We will introduce them in Section 5. The entire proof checking process is detailed in Fig.7.


                                                       12
13
     Fig. 7. Process of proof checking.
5     Solver Manager

The solver manager is an important component of the proof checker, and therefore, we will introduce it
separately here. It is primarily used to verify the correctness of mathematical propositions under certain
conditions. When it comes to proving and simplifying mathematical expressions, we combine different solvers
to check if the current proposition can be derived from known results using specific rules.
    Each solver corresponds to a deduction rule based on specific mathematical concepts, and implements
the corresponding algorithm internally in the proof checker. Different solvers are responsible for handling
different types of mathematical expressions. For example, when dealing with expressions involving algebraic
operators, ProofGrader utilizes algebra-related solvers for simplification. Similarly, solvers for trigonometric
functions, exponential and logarithm, sequential limit, and other mathematical concepts are employed to
handle corresponding cases.
    When users write proofs, they must adhere to the steps supported by the solvers. In Section 1, it was
noted that AI-generated formal proofs sometimes use solvers like Z3[7] to check propositions. However, Z3
possesses strong reasoning capabilities and can sometimes prove the correctness of conclusions even if the
original deduction process contains error. On the other hand, our solver does not engage in excessively
powerful reasoning. It only supports relatively obvious deduction methods in proofs and does not allow
excessive omission of steps. This approach aims to reflect the correctness of the original proof more accurately.
Additionally, since we can provide explicit deduction rules supported by each solver, users can clearly know
which steps can be omitted and which steps cannot be omitted in their proof process.


5.1   Structural Design of the Solver

Before presenting the design of the solver manager, it is necessary to first define the structure of the solver,
as these two are closely related. Each solver consists of the following four components:

 – solve(s,p) : the function used to verify the correctness of a proposition takes two parameters: the current
   proof goal and the proposition itself. It can either return false when the proposition does not pass the
   solver, or a list of propositions, indicating that after being processed by the current solver, the correctness
   of the original proposition can be determined by individually checking the propositions in the list. This
   design allows us to combine multiple solvers to simplify a proposition. The list can contain only one
   proposition, which means the solver simplifies the original proposition and passes it to the next solver.
   An empty list indicates that the current proposition is accepted by the solver.
 – fee : the cost of this solver. While we want to combine multiple solvers, we cannot endlessly repeat using
   various solvers, as it may result in non-termination. Therefore, we need to set an upper limit on the total
   cost within the solver manager and define the cost of each solver.
 – default-priority : the default priority of solvers. When dealing with mathematical propositions that do
   not exhibit any prominent characteristics, solvers can be selected based on their default priority levels.
 – priority(p) : the function used to compute the dynamic priority. Given the current proposition as input,
   this function returns the dynamic priority of the solver. For example, when handling a mathematical
   proposition without limits, solvers related to sequential limit may have a low priority or even be unavail-
   able. However, when dealing with limit-related propositions, these solvers would have a high priority.
   Therefore, it is necessary to dynamically adjust the priority of solvers based on the specific proposition.
   This prepares us for the subsequent development of the solver manager.


5.2   The Design of Solver Manager

The solver manager achieves dynamic scheduling of various solvers by combining dynamic priorities. First, we
categorize the existing solvers into two main types. The first type is the general solvers, which are applicable
to various forms of propositions. For example, they can determine if both sides of an equation are identical
or simplify expressions using polynomial rules. The second type is conditional solvers, which are designed to


                                                       14
handle propositions that meet specific forms, or involve a specific mathematical object, field of knowledge,
etc.
    When examining the current proposition, the solver manager needs to provide a list of available solvers
related to that proposition. The algorithm proceeds as follows: for each conditional solver, the dynamic
priority of the solver is computed for the current proposition. Then, all conditional solvers with a non-zero
dynamic priority are included in the available solver list. Finally, all general solvers are appended to the list,
forming the final list of available solvers. This is the functionality implemented by the usablelist function in
Algorithm 3.


Algorithm 3 Implementation of the solver manager
Input: f ee: limit on the total cost;        ls : list of solvers;
          pg : the proof goal;              p : proposition to be verified;
Output: the correctness of proposition p;
 1: Procedure SolverManager (f ee, ls, pg, p)
 2: if f ee > 0 then
 3:     uselist = usablelist(ls, p);
 4:     for every solver s in uselist do
 5:        listP rop = s.solve(pg, p);
 6:        if listP rop is empty then return true;
 7:        else if listP rop is false then return false;
 8:        else f lag = false;
 9:           for every proposition p′ in listP rop
10:              if p′ == p then break;
11:              else if SolverManager(f ee − s.f ee, ls, pg, p′ ) is false;
12:                 f lag = true;
13:                 break;
14:           if f lag is true then return true;
15:     return false;
16: else return false;



As shown in Algorithm 3 above, the final solver manager takes in four parameters and returns the correctness
of the proposition. The manager first checks the remaining cost. If it is greater than 0, it selects a subset
of solvers from ls to form an available solver list L by calculating the dynamic priority of each solver based
on the form of proposition p. Let L be (s1, s2, s3, ..., sn). Then, it selects s1 and uses s1’s solver function
to check proposition p. If the result is an empty list or false, it returns the proposition as true or false. If it
returns a list of propositions listP rop, it means the original proposition has been simplified and decomposed
to be passed to other solvers for resolution. Before passing it to other solvers, we need to check if listP rop
contains an identical proposition to the original proposition p. If it exists, it means that s1 did not make
any effective contribution to the validation of proposition p, so this branch will be pruned, and the solver
manager will continue to call s2 to handle proposition p. Otherwise, the solver manager recursively validate
each proposition in listP rop. If all validation results are true, the original proposition p is true. If any sub-
proposition is false, this branch will also be pruned, and the solver manager will continue to call s3 to recheck
proposition p, and so on until the final validation is completed.
     Configurability adapted to educational scenarios. Since the initial list of solvers that the solver
manager can use is configurable, we can conveniently control the deduction steps supported by the checker.
When applied in an educational setting, we can set the solver list based on the progress of the curriculum,
so that students can only use the methods learned in the current chapter to complete the proofs, and other
methods will not pass the checker. For instance, if students are expected to evaluate limits by the definition,
it is necessary to disable solvers like those for L’Hôpital’s rule. This management design can also be used to
regulate which theorems can be used in the proof checker.


                                                             15
6     Evaluation

In this section, we give an evaluation of our proof checking system as well as our proof language. We first run
our system on a set of sample mathematical proofs, covering the topic of arithmetic, trigonometric functions,
exponential and logarithm, inequality, derivative, sequential limit and function continuity. The source code
of our system and the dataset are available at: https://github.com/Laplace-Demon/ProofGrader. We then
compare the features of our proof language with other proof languages and proof checking tools.


6.1   Performance

We test our system on a dataset of 52 mathematical proofs, Table 4 shows the average time and memory
overhead of the proof parser and the checker on each of the topics, along with the average file size of the
proof. We can observe that our proof parser and checker perform their task in a reasonable amount of time.


                             Examples                              Parser                Checker
                  Topic            Number File size (bytes) Time (ms) Memory (kb) Time (ms) Memory (kb)
               arithmetic            6           271           34         3584       477       3456
         trigonometric functions     8           599           53         3712      1409       3456
       exponential and logarithm     3           371           40         3840       506       3456
                inequality           10          395           58         3712       528       3456
                derivative           3           385           75         3328       760       3328
       sequential limit evaluation   10          550           58         3840       701       3328
          sequential limit proof     10         1027           78         3968       670       3328
        function continuity proof    2           923           68         3712      7758       3456

                Table 4. Runtime and memory usage of the parser and checker on different topics.




6.2   Comparison of Features

In the table5 below, we compare the features of our proof language with some other proof languages and
proof checking tools. The term “transformation chain” refers to the ability to handle and perform automated
reasoning on a series of consecutive transformation derivations, such as:
                          √3
                                                                        √
                             x+1−1                      x                 x+1+1        2
                      lim √           = lim √        2
                                                          √           ·             =
                      x→0                     3           3
                             x + 1 − 1 x→0 ( x + 1) + x + 1 + 1              x         3

Our proof checker aims to provide automated deduction capabilities that align with human judgment, while
excessive step omissions are not allowed.
    In terms of readability, our natural formal proof can be read with the same effort of reading a natural
language mathematical proof. Even the abstract syntax tree generated by the parser remains readable since
the components bear a mnemonic name.
    In terms of static analysis, most theorem provers like Coq and Isabelle primarily support propositional-
level static analysis. They utilize type inference to fill in missing information in user-written proofs. However,
they do not perform static analysis on the entire proof. Regarding partial proofs, while it is sometimes possible
to reorganize a proof to avoid partial proofs, we aim to preserve the characteristics of natural language proofs.
Users should be able to write mathematical proofs without additional effort.
    The work of Waterproof[17] aims to help students understand mathematical proofs. Therefore, its lan-
guage readability falls between natural language and theorem provers. The proof checking functionality of
Waterproof relies on Coq implementation, so it inherits some limitations of Coq as well. Diproche[5] utilizes


                                                       16
natural language fragments as its input language. Due to its lack of support for static analysis and partial
proofs, it imposes stricter requirements on the types and structure of proofs being written. Lurch[6] is lim-
ited to checking proofs in propositional logic and naive set theory. It does not have automatic reasoning
capabilities and relies on users to provide detailed proofs for checking.


                      Feature         ProofGrader WaterProof Diproche Lurch Isabelle[15] Coq[2]
            Natural language fragment      ✓          ×         ✓      ✓         ×          ×
                 Static analysis       proof-level    ×         ×      ×     prop-level prop-level
                  Partial proof            ✓          ×         ×      ×         ×          ×
             Transformation chains         ✓          ×         ✓      ×         ✓          ×

                 Table 5. Comparison of features of different mathematical proof checking tools.




7   Related Work
Proof assistants and other proof checkers. Recent decades have seen the emergence of various proof languages.
A well-known work is Ltac[8] for the theorem prover Coq, which provides convenience for constructing proofs
and facilitates better proof automation. Another famous one is that of Isar[18] for the system Isabelle. One
objective of Isar is to provide a more human-readable proof language than before. Despite their efforts to
improve readability, the learning curve for using these tools remains high. Wemmenhove et al. developed
an educational software called Waterproof[17] based on this to assist students in practicing proofs. Since
they still choose to rely on the tactic library extended with the Ltac2 tactic language, Waterproof has not
actually gained stronger expressive power than these tactic-based proof language. Additionally, the proof
assistant Agda[4] also employs some proof notations that resemble natural language, such as using equation
chain instead of the “rewrite” tactic used in Coq. However, despite these advancements, they still struggle to
effectively support the structure of partial proofs. While they can perform static analysis at the propositional
level, such as type inference, they are unable to perform static analysis on the entire proof. In addition, tools
mentioned in Section6.2, such as Diproche and Lurch, although they support controlled natural language
input, have stricter requirements on the notation and structure of proofs being written.

Machine learning for formalization. Machine learning techniques have been used in the formalization of
informal proofs. The work of Yuhuai Wu et al.[19] based on large language models can correctly transform
25.3% of the solution for mathematical competition problems in MATH dataset[11] into formal specifications
in Isabelle/HOL. In the work of Jiang et al.[12], they introduce Draft, Sketch, and Prove (DSP), a method
that maps informal proofs to formal proof sketches, The accuracy was improved to 39.3% on the same
dataset[11]. And the automatic theorem prover implemented by GPT-f[16] achieved a completion rate of
56.22% on their test set. The purpose of formalizing proofs with AI-based methods is to ensure that the
proven proposition is correct, especially when proving previously unproven propositions in mathematical
research. Since the target language of the transformation is often tactic-based proof languages that differ
greatly from natural language, these works mainly use the original proof to guide theorem provers to complete
the proof, rather than truly transforming the original proof into a formalized proof. In this case, because the
language we designed combines formal rigor with similarity to natural language, if AI automatic translation
is set to use our language as the target, it will complement our work well and lead to better results.


8   Conclusion
In this paper, we present our design of a natural-formalized proof language and the implementation of a
mathematical proof checker. Compared to existing tactic-based proof language, our proof language has more


                                                       17
expressive power thanks to the incorporation of partial proof. To cope with the characteristics of natural
language proof, such as context-dependent semantics and overloading of notation, tactic language provides
a fine-grained but cumbersome formal specification in the hope that someone can correctly reproduce the
proof, while our proof language can automatically fix these problems through static analysis. All these factors
result in better readability and an easier formalization process.
    Regarding the process of proof checking, we implement a solver manager responsible for managing various
automated proof checking strategies. It selects the most suitable strategies based on the form and contextual
environment of the proposition to assess its correctness. Building upon this, the proof checker takes the proof
and the proof goal provided by the static analyser, applies the appropriate checking methods, updates the
proof goal iteratively, and ultimately completes the checking process.




                                                      18
References
 1. Appel, K.I., Haken, W.: Every planar map is four colorable, vol. 98. American Mathematical Soc. (1989)
 2. Barras, B., Boutin, S., Cornes, C., et al.: The coq proof assistant reference manual. INRIA, version 6(11) (1999)
 3. Bertot, Y., Castran, P.: Interactive Theorem Proving and Program Development: Coq’Art The Calculus of
    Inductive Constructions. Springer Publishing Company, Incorporated, 1st edn. (2010)
 4. Bove, A., Dybjer, P., Norell, U.: A brief overview of agda–a functional language with dependent types. In: Theorem
    Proving in Higher Order Logics: 22nd International Conference, TPHOLs 2009, Munich, Germany, August 17-20,
    2009. Proceedings 22. pp. 73–78. Springer (2009)
 5. Carl, M., Krapf, R.: Diproche–ein automatisierter tutor für den einstieg ins beweisen. Digitale Kompetenzen und
    Curriculare Konsequenzen p. 43 (2020)
 6. Carter, N.C., Monks, K.G.: Using the proof-checking word processor lurch to teach proof-writing (2014)
 7. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: International conference on Tools and Algorithms for
    the Construction and Analysis of Systems. pp. 337–340. Springer (2008)
 8. Delahaye, D.: A tactic language for the system coq. In: Parigot, M., Voronkov, A. (eds.) Logic for Programming
    and Automated Reasoning. pp. 85–95. Springer Berlin Heidelberg, Berlin, Heidelberg (2000)
 9. Donnelly, C.: Bison the yacc-compatible parser generator. Technical report, Free Software Foundation (1988)
10. Gonthier, G., et al.: Formal proof–the four-color theorem. Notices of the AMS 55(11), 1382–1393 (2008)
11. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D., Steinhardt, J.: Measuring
    mathematical problem solving with the math dataset (2021)
12. Jiang, A.Q., Welleck, S., Zhou, J.P., Li, W., Liu, J., Jamnik, M., Lacroix, T., Wu, Y., Lample, G.: Draft, sketch,
    and prove: Guiding formal theorem provers with informal proofs. arXiv preprint arXiv:2210.12283 (2022)
13. Lample, G., Lacroix, T., Lachaux, M.A., Rodriguez, A., Hayat, A., Lavril, T., Ebner, G., Martinet, X.: Hypertree
    proof search for neural theorem proving. Advances in Neural Information Processing Systems 35, 26337–26349
    (2022)
14. Levine, J.: Flex & Bison: Text Processing Tools. ” O’Reilly Media, Inc.” (2009)
15. Paulson, L.C.: Isabelle: A generic theorem prover. Springer (1994)
16. Polu, S., Sutskever, I.: Generative language modeling for automated theorem proving. arXiv preprint
    arXiv:2009.03393 (2020)
17. Wemmenhove, J., Beurskens, T., McCarren, S., Moraal, J., Tuin, D., Portegies, J.: Waterproof: educational
    software for learning how to write mathematical proofs. arXiv preprint arXiv:2211.13513 (2022)
18. Wenzel, M.: Isar - a generic interpretative approach to readable formal proof documents. In: International Con-
    ference on Theorem Proving in Higher Order Logics (1999)
19. Wu, Y., Jiang, A.Q., Li, W., Rabe, M., Staats, C., Jamnik, M., Szegedy, C.: Autoformalization with large language
    models. Advances in Neural Information Processing Systems 35, 32353–32368 (2022)




                                                         19
A     Key grammar of natural formalized proof language
⟨proof ⟩ ::= ⟨proof statement⟩
  | ⟨proof statement⟩ ‘,’ ⟨proof ⟩
  | ‘The following proves’ ⟨math proposition⟩ ‘{’ ⟨proof ⟩ ‘}’ ⟨proof ⟩
  | ‘It suffices to prove’ ⟨math proposition⟩ ⟨proof ⟩
  | ⟨proof action statement⟩ ‘{’ ⟨proof ⟩ ‘}’ ⟨proof ⟩
⟨proof statement⟩ ::= ‘which proves the proposition.’
  | ‘Use’ ⟨definition⟩ ‘to prove’
  | ‘Use’ ⟨theorem⟩ ‘to prove’
  | ⟨since clause⟩ ‘then’ ⟨math proposition⟩
  | ⟨proof action statement⟩
  | ...
⟨since clause⟩ ::= ‘Obviously’
  | ‘Similarly’
  | ‘Since’ ⟨knowledge⟩
  | ‘Because’ ⟨math proposition⟩
  | ‘By’ ⟨prop action statement⟩
  | ...
⟨prop action statement⟩ ::= adding ⟨list proposition name⟩
  | ⟨prop transformation⟩ ‘on the both sides of the equality’
  | ...
⟨prop transformation⟩ ::= ‘adding’ ⟨math expression⟩
  | ‘squaring’
  | ‘taking the logarithm’
  | ‘taking the derivative of’ ⟨variable name⟩
  | ...
⟨proof action statement⟩ ::= ‘Let’ ⟨variable name⟩
  | ‘Let’ ⟨variable name⟩ ⟨math proposition⟩
  | ‘There exists’ ⟨math expression⟩
  | ‘There exists’ ⟨variable name⟩ ‘such that’ ⟨math proposition⟩
  | ‘Suppose’ ⟨math proposition⟩
  | ‘Suppose’ ⟨variable name⟩ ‘such that’ ⟨math proposition⟩
  | ‘Set’ ⟨variable name⟩ ‘=’ ⟨math expression⟩
  | ...
⟨knowledge⟩ ::= ⟨theorem⟩
  | ⟨definition⟩
  | ⟨property⟩

Since natural language offers various ways to express the same meaning, we have chosen a subset of these
expressions as keywords for the grammar of natural formalized proof. In the above grammar, we have chosen
only one of the possible options as example. Furthermore, due to the complexity of mathematical expressions
and propositions involving various mathematical concepts, we do not elaborate on them in detail here.




                                                    20
B    Grammar of term and prop
⟨term⟩ ::= ‘TNum’ ⟨number ⟩
  | ‘TInfty’ ⟨infinity⟩
  | ‘TConst’ ⟨const⟩
  | ‘TUnOp’ ⟨unaryTermOperator ⟩ ⟨term⟩
  | ‘TBinOp’ ⟨binaryTermOperator ⟩ ⟨term⟩ ⟨term⟩
  | ‘TApply’ ⟨term⟩ ⟨term⟩
  | ‘TBinder’ ⟨binder ⟩ ⟨identifier ⟩ ⟨term⟩
  | ‘TVar’ ⟨identifier ⟩
  | ‘TInterval’ ⟨intervalType⟩ ⟨term⟩ ⟨term⟩
  | ‘TSet’ {string}∗ ⟨term⟩ ⟨prop⟩
⟨prop⟩ ::= ‘PUnPred’ ⟨unaryPredicate⟩ ⟨term⟩
  | ‘PBinPred’ ⟨binaryPredicate⟩ ⟨term⟩ ⟨term⟩
  | ‘PCBinPred’ ⟨binaryPredicate⟩ ⟨term⟩ ⟨term⟩ ⟨propContext⟩
  | ‘PLongOrder’ ⟨order ⟩ ⟨term⟩ ⟨prop⟩
  | ‘PUnOp’ ⟨unaryPropOperator ⟩ ⟨prop⟩
  | ‘PBinOp’ ⟨binaryPropOperator ⟩ ⟨prop⟩ ⟨prop⟩
  | ‘PQuant’ ⟨quantifier ⟩ ⟨identifier ⟩ ⟨prop⟩
⟨binder ⟩ ::= ‘SeqLimitB’
  | ‘LambdaB’




                                                   21
C   The overall workflow of ProofGrader




                                                                               22
                                    Fig. 8. Overall workflow of ProofGrader.
