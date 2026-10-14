                                           Verifiable Auto-Formalization of Mathematics
                                            Using a Relaxed Natural Formal Language

                                            Zhicheng Hui1 , Lihan Xie1 , Xingzhi Qi1 , Zhehao Li1 , Yingjun Lan1 , and
                                                                         Qinxiang Cao1

                                                                   Shanghai Jiao Tong University
arXiv:2606.24443v1 [cs.LO] 23 Jun 2026




                                               Abstract. Auto-formalization aims to translate informal mathematical
                                               content into formal languages that can be processed by theorem provers.
                                               However, directly targeting existing theorem provers requires LLMs to
                                               bridge a substantial representational gap between informal mathemat-
                                               ical writing and formal proof languages. This gap also makes semantic
                                               consistency diﬀicult to evaluate. We address these diﬀiculties by intro-
                                               ducing a Relaxed Natural Formal Language (Relaxed NFL) as an inter-
                                               mediate target for auto-formalization. The Relaxed NFL is designed to
                                               remain close to informal mathematical writing: it preserves the usual
                                               structure of informal reasoning and allows partially specified expres-
                                               sions and propositions, without requiring their precise interpretation
                                               to be fixed at the auto-formalization stage. The remaining ambiguity
                                               and implicitness inherited from informal reasoning are resolved during
                                               a later elaboration stage, which transforms Relaxed NFL proofs into
                                               Core Natural Formal Language (Core NFL) proofs with formally de-
                                               fined semantics. The elaboration procedure combines rule-based trans-
                                               formations with LLM-generated heuristics, while maintaining verifiabil-
                                               ity through explicit constraints on each transformation step. The Core
                                               NFL is then used to generate proof gaps, namely verification conditions
                                               that must hold for the formalized proof to be correct. These gaps are
                                               discharged by LLM-generated proof scripts written in a domain-specific
                                               tactic language, which provides commands for invoking theorem libraries
                                               and domain-specific solvers implemented as part of our system.

                                               Keywords: Auto-formalization · Natural formal language · Neural
                                               theorem proving.


                                         1 Introduction

                                         Auto-formalization is the task of automatically translating informal mathemat-
                                         ical content into a formal language that can be processed by a theorem prover,
                                         such as Rocq [2], Lean [20], or Isabelle [22]. Because ordinary mathematical
                                         statements and proofs are written in a mixture of natural language and nota-
                                         tion, their intended semantics may be underspecified and intermediate inferential
                                         steps are often left implicit. Therefore, auto-formalising mathematical content
                                         into a trusted theorem prover can greatly reduce the diﬀiculty of verifying its
2        Authors Suppressed Due to Excessive Length

correctness, while also making mathematical knowledge more reusable and ac-
cessible.
    Recent advances in large language models (LLMs) have led to renewed inter-
est in auto-formalization. Since these models are increasingly capable of process-
ing both natural language and formal proof languages, they can be fine-tuned
or directly prompted to generate formal statements from informal ones. Such
capability can be further improved in several ways. For instance, models can
be post-trained on synthetically generated informal-formal pairs [11,25], aug-
mented with retrieved formal definitions from libraries [18,15], or embedded in
an iterative refinement loop that uses feedback from the theorem prover [8,13].
    Despite the progress, auto-formalization remains intrinsically diﬀicult. A ma-
jor source of such diﬀiculty is the fundamental discrepancy between informal
mathematical writing and the formal languages used by existing theorem provers,
as shown in Figure 1. We can observe that the Mizar [21] and Lean proof lan-
guage often require a single informal proof step to be decomposed into several
explicit declarations, assumptions, and proof obligations. For example, the infor-
mal phrase “Let xn = an+1 (0 < a < 1)” must be expanded into separate formal
steps, including an explicit construction of the existence of such an a. Similarly,
the phrase “when n → +∞” can no longer remain a syntactic modifier attached
to the statement, but must be incorporated into a formal proposition. Besides,
ordinary mathematical notation must be resolved into specific library definitions,
such as the scheme SEQ_1:sch 1 from the Mizar Mathematical Library [1], and
the neighbourhood filter N 0 from Mathlib [5].



                                 Natural Language

                         Let xn = an+1 (0 < a < 1),
                         when n → +∞, we have xn → 0.


                 Mizar
                                                              Lean
    consider a being Real such that
                                              obtain ⟨a, ha ⟩ :
      0 < a & a < 1 by . . .;
                                                ∃ a : ℝ, 0 < a ∧ a < 1 :=
    deffunc X(Nat) =
                                                  by sorry
      a to_power ($1+1);
                                              let x : ℕ → ℝ :=
    consider x being Real_Sequence
                                                fun n => a ^ (n + 1)
      such that for n being Nat
                                              have hx :
        holds x . n = X(n)
                                                Tendsto x atTop (N 0) :=
          from SEQ_1:sch 1();
                                                  by sorry
    then lim x = 0 by . . .;



Fig. 1. The same proof snippet written in natural language, the Mizar proof language,
and the Lean proof language.
                                 Title Suppressed Due to Excessive Length       3

    This discrepancy challenges auto-formalization in two ways. First, it requires
LLMs to bridge a substantial representational gap between informal mathemat-
ical text and formal proof languages. The scarcity of formal data further exacer-
bates this problem, especially for target formal languages with limited available
corpora, such as those used by proof assistants with smaller libraries or user
communities, as well as domain-specific formal languages.
    Second, it makes the evaluation of semantic consistency non-trivial, i.e., de-
termining whether the generated formal statement preserves the intended mean-
ing of the original informal statement. Existing methods either rely on the avail-
ability of a reference formalization [17,15] or use LLMs or human experts as
judges, making the evaluation diﬀicult to carry out. This issue has already had
practical consequences. For example, Ospanov et al. [23] report discrepancies
between the informal and formal statements for more than half of the problems
in the miniF2F benchmark [32], thereby compromising the reliability of some
previous evaluation results.

Overview of the Approach To address these diﬀiculties at a more fundamental
level, we propose using a Relaxed Natural Formal Language (Relaxed NFL) as
the target language for LLM-based auto-formalization. The Relaxed NFL is de-
signed to remain as close as possible to natural mathematical language, so that
auto-formalization into it resembles a structured normalization of informal math-
ematical text, rather than a full elaboration into a theorem prover language. This
reduces the reasoning burden on LLMs and makes auto-formalization largely in-
dependent of the choice of a particular formal system.
     The Relaxed NFL has a formally specified syntax, which enables it to be
parsed and processed by machines. However, since it deliberately preserves part
of the ambiguity, implicitness, and context dependence of informal mathemat-
ical writing, it is not suitable to be used directly as a verification target, but
only as an intermediate representation of proof. We therefore elaborate the Re-
laxed NFL into a Core NFL with formally defined semantics, using a rule-based
procedure supplemented by LLM-generated heuristics. These elaboration steps
isolate the discrepancy between informal mathematical writing and the target
formal system, which constitutes the main diﬀiculty of auto-formalization. At
the same time, since the input and output of each step can be formally speci-
fied, the overall process remains controllable and verifiable even when LLMs are
involved.
     From the Core NFL, we generate proof gaps, i.e., verification conditions
whose validity is suﬀicient to verify the correctness of the proof. We discharge
these proof gaps by prompting LLMs to synthesize proof scripts written in a
domain-specific language. Beyond standard tactic operations such as case analy-
sis, term rewriting, quantifier instantiation, and lemma application, the language
provides commands for invoking theorem libraries and domain-specific solvers
implemented as part of our system.
     Figure 2 gives an overview of the entire auto-formalization pipeline.

Contributions The contributions of this paper are summarized as follows:
4         Authors Suppressed Due to Excessive Length


                    Natural Language

                                               Auto-Formalizer

                      Relaxed NFL

                                               Proof Elaborator

                        Core NFL

                                             Proof Gap Generator

                       Proof Gaps           Proof Script Generator,
                                              Theorem Libraries,
                                            Domain-Specific Solvers,
                    Verification Result


                  Fig. 2. Overview of the auto-formalization pipeline.


    – We propose a novel approach to LLM-based auto-formalization based on an
      intermediate representation that resembles informal mathematical writing.
    – We study how to turn this intermediate representation into a semantically
      well-defined formal proof, and develop a verifiable elaboration procedure.
    – We study how proof gaps generated along this pipeline can be effectively dis-
      charged by combining LLM-guided proof search with theorem library sup-
      port and domain-specific solvers.
    – We give concrete designs of our Relaxed NFL, Core NFL, and the domain-
      specific tactic language.

Organization of the Paper The rest of this paper is organized as follows. Sec-
tion 2 presents the Relaxed and the Core NFL, as well as the LLM-based auto-
formalization process into Relaxed NFL. Section 3 demonstrates the elaboration
of the Relaxed NFL into the Core NFL via three representative steps: notation
resolution, problem-solving translation, and implicit variable scope resolution.
Section 4 explains how proof gaps are generated from the Core NFL and sub-
sequently discharged. Section 5 evaluates whether LLMs can reliably generate
Relaxed NFL proofs under different settings. Finally, Sections 6 and 7 are de-
voted to related work and conclusions, respectively.


2 Natural Formal Language
In principle, natural formal language is intended to be extensible and can be
instantiated in different mathematical domains. The particular natural formal
languages presented in this paper are designed with reference to the proof struc-
tures, notation, and mathematical knowledge appearing in the textbook Prob-
lems in Mathematical Analysis by B. P. Demidovich [7].
                                  Title Suppressed Due to Excessive Length        5

   The remainder of this section is organized as follows. We first briefly introduce
the Relaxed NFL, then describe how informal mathematical proofs can be auto-
formalized into the Relaxed NFL by using LLMs. Finally, we present the Core
NFL, whose formal semantics is defined by a proof-gap generation function.

2.1 The Relaxed Natural Formal Language
The Relaxed NFL remains close to informal mathematical writing in two re-
spects. First, it preserves the common reasoning patterns of informal proofs, so
that the overall proof structure is largely maintained after auto-formalization.
Second, it allows partially specified terms and propositions by retaining infor-
mal mathematical writing without requiring every expression to be resolved to
a precise definition in a specific library.
    As an example, Appendix A presents the Relaxed NFL formalization of an
IMO functional-equation problem. As shown in this example, the Relaxed NFL is
a declarative-style proof language. Among other things, user can introduce new
symbols, derive intermediate conclusions, reason locally under assumptions, and
solve equations.
    The Relaxed NFL serves only as a surface syntax for LLM-based auto-
formalization. Terms in the Relaxed NFL do not yet have fully precise math-
ematical meanings at this stage. Some notations may remain ambiguous, and
information on variable scopes may be left implicit, as shown by the occurrence
of free variables in expressions. These partially specified expressions are later
resolved into precise mathematical objects through elaboration, as described in
Section 3.
    The detailed grammar of the Relaxed NFL is given in Appendix B. The
non-terminal <program> can be either a proof problem or a solving problem.
They share the same reasoning steps, but are translated into the Core NFL
differently. The non-terminal <term> represents mathematical propositions and
expressions. We omit its grammar here and introduce the relevant fragments in
Section 3 when needed.

2.2 Auto-Formalization into the Relaxed NFL
We instruct LLMs to translate informal mathematical content into the Relaxed
NFL in two ways: in-context learning and fine-tuning.
   For in-context learning, the prompt first provides the complete grammar of
the Relaxed NFL, followed by 16 examples that serve as few-shot demonstrations.
The model is then asked to translate the input into the target language. We then
use the obtained informal-formal pairs as supervised training data, and perform
LoRA fine-tuning [9] so that the model learns the grammar of the Relaxed NFL
more directly.

2.3 The Core Natural Formal Language
The Core NFL is an internal proof language obtained by elaborating the surface-
level constructs of the Relaxed NFL into a small number of primitive proof
6         Authors Suppressed Due to Excessive Length

steps over formally specified terms. Unlike the Relaxed NFL, the Core NFL
has a precisely defined semantics, and captures the information necessary for
generating proof gaps.
   We define the abstract syntax of the Core NFL as follows. We assume two
syntactic categories: Term, whose elements represent mathematical expressions
and propositions in the Core NFL, and Method, whose elements represent proof
methods, with a distinguished element ∅M denoting the empty method. We write
Term∗ for the set of finite, possibly empty sequences of terms.
   Based on this, we define the set of proof states PState by

                              PState = Term∗ × Term.

We write a proof state consisting of a sequence of assumptions Γ ∈ Term∗ and
a proof goal G ∈ Term in sequent form as Γ ⊢ G.
   Let Proof be the least set satisfying

         Proof = {Forward(M, P, π) | M ∈ Method, P ∈ Term, π ∈ Proof}
               ∪ {Backward(M, P, π) | M ∈ Method, P ∈ Term, π ∈ Proof}
               ∪ {Subgoal(P, π1 , π2 ) | P ∈ Term, π1 , π2 ∈ Proof}
               ∪ {QED}.

The set of Core NFL program Program is then defined by

                             Program = PState × Proof.

      The constructors of Proof are interpreted as follows:
    – Forward(M, P, π) derives the proposition P from the current proof state using
      the method M , adds it to the available assumptions, and then continues with
      the proof π.
    – Backward(M, P, π) reduces the current proof goal to the proposition P using
      the method M , and then continues with the proof π.
    – Subgoal(P, π1 , π2 ) introduces the proposition P as an intermediate subgoal,
      proves it by π1 , adds it to the available assumptions, and then continues
      with the proof π2 .
    – QED terminates the proof, indicating that the current proof goal is derivable
      from the available assumptions.
   A Core NFL program is therefore a pair P = (σ, π), where σ ∈ PState
represents the current proof state, and π ∈ Proof represents the proof to be
executed from that state.


3 Elaborating the Relaxed NFL into the Core NFL
In this section, we present how the Relaxed NFL is elaborated into the Core NFL
in a verifiable way. Such elaboration generally cannot be achieved by purely syn-
tactic transformation of the proof. Instead, we often have to perform semantic
                                  Title Suppressed Due to Excessive Length       7

analysis in order to recover information that is left implicit. Some of the simple
cases can be formulated as deterministic rules, while others require a closer anal-
ysis of the proof and may even involve inferring the author’s intended meaning.
In such cases, we use LLMs to give heuristics, while keeping the elaboration step
verifiable by placing models inside a suitable harness. For example, the model
may be restricted to choosing among a finite set of candidates generated by
deterministic rules, or its output may be required to pass a dedicated checker
before being accepted.
    Since different mathematical domains use different notations and proof writ-
ing conventions, and tolerate different degrees of implicitness, the concrete elab-
oration process is dependent on the domain. In this section, we focus on math-
ematical analysis and present three representative elaboration steps extracted
from our implementation. They exemplify three different levels at which ambi-
guity and implicitness arise in informal mathematical writing: the term level,
the proof-step level, and the proof-state level.
    Because the Core NFL can be regarded as a restricted fragment of the Re-
laxed NFL, we present the elaboration steps in this section as transformations
on the Relaxed NFL itself. Each step resolves certain ambiguity or implicitness,
thereby moving the proof closer to the Core NFL fragment.

3.1 Notation Resolution
A common source of ambiguity in informal mathematical writing is notation
overloading, where the same notation may denote different mathematical ob-
jects. A simple example is the notation |x|. Depending on the meaning of x,
|x| may denote the absolute value of a real number, or the cardinality of a set.
Consequently, the surface syntax |x| in the Relaxed NFL does not automatically
resolve to a Core NFL term by itself.
    In order to perform notation resolution, we first need to augment the defini-
tion of terms in the Relaxed NFL with the following constructs:

                           ⟨term⟩ ::= ...
                             | | ⟨term⟩ |
                             | IsReal( ⟨term⟩ )
                             | IsSet( ⟨term⟩ )
                             | Abs( ⟨term⟩ )
                             | Card( ⟨term⟩ )

    Here, | · | is the overloaded surface notation, while Abs(·) and Card(·) are
disambiguated forms that can be deterministically translated into the corre-
sponding Core NFL terms, namely the absolute value of a real number and the
cardinality of a set. The predicates IsReal and IsSet record information about
whether a term has been treated as a real number or as a set. They are not
part of a static type system for Relaxed NFL, but annotations used to guide the
interpretation of overloaded notation. In this respect, they are similar in spirit
to Mizar’s soft type system [28].
8       Authors Suppressed Due to Excessive Length

    We perform a static analysis over the Relaxed NFL and maintain an envi-
ronment that stores such annotations. These annotations may come from two
sources.
    First, they may be introduced by the LLM during the initial auto-formalization
process. The prompts are designed to encourage the LLM to preserve explicit
information from the informal proof about what kind of mathematical object
a term denotes. For example, the informal phrase “for every real number t” is
supposed to be translated into the Relaxed NFL by introducing t together with
the annotation IsReal(t).
    Second, our system may infer them by constraint propagation over such an-
notations. It derives constraints from operator signatures and records the corre-
sponding annotations in the environment. For example, if an operator expects a
set argument and is applied to t, the constraint IsSet(t) is generated.
    After constraint propagation, the elaborator checks each unresolved over-
loaded notation. When the environment determines a unique interpretation, the
notation is replaced by the corresponding disambiguated form. For instance, |t|
is resolved as Abs(t) if IsReal(t) is available, and as Card(t) if IsSet(t) is available.
Otherwise, the system queries the LLM with instructions, the surrounding proof
context, and the finite set of remaining candidate interpretations, asking it to
select the intended one.

3.2 Problem-Solving Translation
In addition to theorem proving, the Relaxed NFL also supports problem-solving.
Problem-solving does not merely require proving a given proposition. Rather,
it requires constructing an answer together with a proof that the answer is
correct [16,3]. For example, consider a Relaxed NFL program of the form:
                      Find all x such that P(x) { ... }

   When it terminates, we should be able to identify a candidate solution set S
and prove that S is exactly the set of all solutions. Once S has been determined,
the ending of the problem-solving step is reduced to the following step:
                    We have forall (x), x in S <==> P(x)

    However, the candidate solution set S cannot be recovered at the syntactic
level alone. This is because the reasoning steps of problem-solving may not all
preserve logical equivalence with the original constraint P (x). Some may only
derive a suﬀicient or necessary condition, and such steps are not distinguishable
from their surface syntax alone. Therefore, identifying the exact solution set is a
semantic task, as it depends on whether the derived candidates genuinely satisfy
the original constraint.
    This task is well suited to LLMs, because the model only needs to propose
a candidate answer, whose validity can be verified symbolically. Thus, we use
in-context learning to infer the exact candidate solution set for each problem-
solving task by providing the model with instructions and the surrounding proof
context. Other kinds of problem-solving steps are handled analogously.
                                 Title Suppressed Due to Excessive Length       9

   In some cases, we explicitly check whether the candidates obtained satisfy
the constraints. For example, consider a Relaxed NFL program of the form:

        Solve the system of equations P(x), Q(x) {
          ... After checking, x = x0 satisfies the constraints
        }

This can be translated into a step asserting that the checked candidate satisfies
the original equations:

               Solve the system of equations P(x), Q(x) {
                 ... We have P(x0) and Q(x0)
               }


3.3 Implicit Variable Scope Resolution
Informal mathematical writing often omits parts of the information on the scope
of variables. In particular, adjacent steps may share locally introduced variables
and conditions without explicitly specifying their scope. For example, consider
the following simplified Relaxed NFL proof adapted from Appendix A:


   Solve: Find all f such that
     ...,
     forall (x, y in Real),
       f(x - f(y)) = f(f(y)) + x * f(y) + f(x) - 1

   Solution:
      Set f(0) = c
      ...
   1. We have f(x) = frac(c + 1, 2) - frac(x ^ 2, 2)
   2. [@method By x ^ 2 = (-x) ^ 2 @]
      We have f(x) = f(-x)
   3. We have f(c) = f(-c)
   4. We have f(c) = f(c) + c - 1
   5. We have c = 1
   6. We have f(x) = 1 - frac(x ^ 2, 2)


    Here, the same name x occurs free in Steps 1, 2, and 6, suggesting that
these occurrences may refer to the same variable and requiring the current proof
context to be interpreted within the scope of x, which has two semantic impli-
cations.
    First, variable scopes determine the interpretation of a term written in the
Relaxed NFL. The declaration forall (x, y in Real) at the beginning of the
problem provides evidence that its proof steps may enter the scope of a univer-
sally quantified real variable x. Thus, Step 1 should be interpreted as deriving
10      Authors Suppressed Due to Excessive Length

                                                   2
the closed proposition ∀x ∈ R, f (x) = c+1 2 − 2 . Similarly, Step 2 should be
                                                x

interpreted as deriving ∀x ∈ R, f (x) = f (−x). In this sense, the interpretation
of a surface syntax term is determined by the current variable scope.
    One may be tempted to think that this interpretation can always be obtained
simply by closing the free variables syntactically occurring in the term. We show
in the following paragraphs that this is not the case.
    Second, variable scopes may also suggest how a proposition is derived, which
in turn affects the interpretation of a term written in the Relaxed NFL. For
                                                                       x2
example, for an arbitrarily fixed x ∈ R, Step 1 gives f (x) = c+1 2 − 2 . Together
                                                                        2
with Step 5, namely c = 1, it yields Step 6, namely f (x) = 1 − x2 . Since the
interpretation of Step 6 is still deriving the universal proposition ∀x ∈ R, f (x) =
      2
1 − x2 , rather than properties about one particular x in the current scope. What
                                                                       x2
happens here is that, when c = 1, we prove ∀x ∈ R, f (x) = c+1    2 − 2 ⇒ f (x) =
      2                                               2
                                                                                 x2
1 − x2 in order to justify (∀x ∈ R, f (x) = c+12 − 2 ) ⇒ (∀x ∈ R, f (x) = 1 − 2 ),
                                                    x

which constitutes a form of local derivation carried out within the scope of x.
    However, being in the same scope for x does not mean that the derivation
is always local in the above sense. For example, in deriving Step 2 from Step 1,
                                                          x2
what is proved is the implication (∀x ∈ R, f (x) = c+12 − 2 ) ⇒ (∀x ∈ R, f (x) =
                                                    2
f (−x)) itself, rather than ∀x ∈ R, f (x) = c+1
                                             2 − 2 ⇒ f (x) = f (−x), which in
                                                  x

fact does not hold.
    Similarly, when multiple variables are present in the scope, some of them
may not occur freely in the derived surface syntax term, but a non-local deriva-
tion as shown in the previous paragraph will still make the interpretation to
be quantified by these variables. It demonstrates that determining the precise
interpretation of surface syntax terms which contains free variables involves a se-
mantic analysis as to the actual reasoning pattern of the proof (local/non-local),
instead of a syntactic analysis of free variables. Consequently, we delegate the
resolution of implicit variable scopes to LLMs.
   In order to perform implicit variable scope resolution, we first need to aug-
ment definition of proofs and terms in the Relaxed NFL with the following
constructs:

      ⟨local_action_step⟩ ::= ...
        | [@scope ([∀ ⟨term⟩ ]|[∃ ⟨term⟩ ]|[ ⟨term⟩ ])* @]

      ⟨term⟩ ::= ...
        | [@free ⟨term⟩ (, ⟨term⟩)* @]

    The construct [@scope ... @] allows the LLM to explicitly annotate the
implicit variable scope via <local_action_step> in the Relaxed NFL. The con-
struct [@free ... @] marks the free variables occurring in a term, it is precom-
puted and annotated to the Relaxed NFL proof given to the LLM, helping it to
infer the implicit scope covering the step.
                                        Title Suppressed Due to Excessive Length          11


  [@scope [ ∀ x] [x in Real] @] {
                                           LLM
      We have P(x)                        ===⇒        We have forall (x), x in Real => P(x)
  }




        Fig. 3. Elimination of the variable scope annotation in LLM’s output.


    The output of this elaboration step is then verified by a deterministic checker.
The checker ensures that all the annotated free variables occur within a matching
scope, and that no other part of the proof has been modified.
    Finally, we eliminate the explicit variable scope annotation in the Relaxed
NFL as in Figure 3. This is done by adding the content of variable scope anno-
tation to every terms in the scope as quantifiers and premises.


4 Generating and Discharging Proof Gaps

In this section, we define the semantics of Core NFL programs. Rather than
interpreting an element of Program as a complete formal proof, we interpret it
as a procedure that generates a collection of proof gaps. These proof gaps must
subsequently be discharged by a trusted backend in order for the whole proof to
be certified.


4.1 The Proof Gap Generator

A proof gap consists of a proof method together with a proof state. Formally,
we define the set of proof gaps Gap by:

                                    Gap = PState × Method.

We write a proof gap consisting of a proof state (Γ, G) ∈ PState and method
M ∈ Method in sequent form as Γ ⊢M G. It represents the obligation of deriving
the goal G from the available assumptions Γ using the method M .
   We denote by Γ P the sequence obtained by appending P to the end of Γ.
The proof gap generator for the Core NFL is a function

                          PGG : PState × Proof −→ Pfin (Gap),

defined by structural recursion on the proof as follows:

    PGG(Γ ⊢ G, Forward(M, P, π))            = {Γ ⊢M P } ∪ PGG(Γ P ⊢ G, π),

    PGG(Γ ⊢ G, Backward(M, P, π)) = {Γ P ⊢M G} ∪ PGG(Γ ⊢ P, π),

    PGG(Γ ⊢ G, Subgoal(P, π1 , π2 )) = PGG(Γ ⊢ P, π1 ) ∪ PGG(Γ P ⊢ G, π2 ),

    PGG(Γ ⊢ G, QED)                         = {Γ ⊢∅M G}.
12     Authors Suppressed Due to Excessive Length

4.2 Discharging Generated Proof Gaps

A Core NFL program is certified by checking all generated proof gaps. We define
two functions

      CheckGap : Gap → {⊥, ⊤},         CheckProgram : Program → {⊥, ⊤},

such that
                                                      ∧
       ∀ (σ, π) ∈ Program, CheckProgram(σ, π) =                 CheckGap(G).
                                                   G∈PGG(σ,π)


Thus, for a Core NFL program P, CheckProgram(P) = ⊤ means that all the
generated proof gaps are successfully discharged.


Tactic Language for Proof Gaps Since the Core NFL inherits the reasoning
structure of the informal proof, the generated proof gaps may still contain non-
trivial intermediate reasoning. As a result, relying only on automatic theorem
proving techniques is often insuﬀicient.
    To address this issue, we use LLMs to facilitate the proof search. Concretely,
we design a domain-specific tactic language that operates on individual proof
gaps. Given a proof gap, the LLM is asked to synthesize a proof script in this
language, which specifies a sequence of commands that either close the gap or
reduce it to simpler subgaps. The method annotations in the Relaxed NFL,
corresponding to the non-terminal <method> in Appendix B, are used to provide
proof search hints.
    The main commands of the tactic language are summarized in Table 1.
Most of them correspond to standard proof-state transformations in tactic-based
proof languages. The last three commands are more special: auto_solve and
auto_replace provides a higher level of automation by invoking our domain-
specific solvers to close proof gaps directly or replace a term with a semantically
equivalent one. get_prop retrieves and instantiates propositions from our the-
orem libraries, allowing the model to use established theorems without recon-
structing them from scratch.


Theorem Libraries and Domain-Specific Solvers The theorem libraries
contain formalized propositions extracted from Problems in Mathematical Anal-
ysis, together with commonly used facts about sets, inequalities, elementary
functions, limits, etc.
    The domain-specific solvers are designed to discharge recurring proof gap
patterns for which effective decision procedures are available. Rather than being
used in isolation, these solvers are composed automatically. Each solver may close
a proof gap directly or generate new subgaps, which can in turn be handled by
other solvers. This is implemented as a breadth-first search. The main solvers
are summarized in Table 2.
                                   Title Suppressed Due to Excessive Length          13

  Table 1. Main commands of the tactic language used for discharging proof gaps.

Command          Use
assert           Proves a proposition and adds it to the assumptions.
apply            Reduces the proof goal using a matching implicational assumption.
case_analysis    Splits a proof gap according to a disjunctive assumption.
rewrite          Rewrites assumptions or the proof goal by equalities or
                 equivalences.
get_forall       Instantiates universal quantifiers in the proof goal with fresh
                 variables.
get_condition    Introduces premises of an implicational proof goal as assumptions.
get_exists       Eliminates existential quantifiers in an assumption using fresh
                 variables.
exists           Instantiates existential quantifiers in the proof goal with witnesses.
use_condition    Specializes an implicational assumption using matching premises.
auto_replace     Performs semantic term transformation.
auto_solve       Invokes automatic solvers on selected assumptions.
get_prop         Instantiates hypotheses or imports theorem-library facts.
auto_solve       Invokes solvers to automatically close the proof gap.
auto_replace     Invokes solvers to perform semantically-equivalent term
                 replacement.
get_prop         Retrieves and instantiates a proposition from the theorem library.



5 Evaluation

We evaluate the learnability of the Relaxed NFL as a target language for LLM-
based auto-formalization. We report pass@1 and pass@3. An auto-formalization
attempt is counted as a pass if it can semantically yield semantically well-defined
proof gaps, while the discharge of these proof gaps is not included in this evalua-
tion. For each problem, we sample three independent candidates from the model.
The pass@1 rate is the proportion of problems for which the first generated can-
didate is counted as a pass, while the pass@3 rate is the proportion of problems
for which at least one of the three generated candidates is counted as a pass.
    Our dataset contains 3600 problems extracted by OCR from Problems in
Mathematical Analysis, covering major topics in elementary mathematical anal-
ysis, including limits, continuity, differentiation, integration, series, and multi-
variable calculus.
    We first use Qwen3-235B-A22B-Instruct [30], a large MoE model with 235B
total parameters and 22B activated parameters, for the few-shot auto-formalization
described in Section 2.2. Without chain-of-thought prompting (CoT), the model
achieves 44.4% pass@1 and 72.3% pass@3. With CoT, the rates increase to 70.3%
pass@1 and 90.4% pass@3.
    We then select 2,000 correctly generated informal-formal pairs from this stage
as supervised training data, and use the remaining examples as the test set.
Finally, we fine-tune Qwen2.5-7B-Instruct [31], a smaller dense model from an
earlier generation of the Qwen series, with LoRA, using rank r = 128, scaling
14       Authors Suppressed Due to Excessive Length

         Table 2. Main domain-specific solvers used for discharging proof gaps.

Solver                 Use
EqbSolver              Reflexivity and exact matching against assumptions.
PolyRatSolver          Normalization of polynomial and rational expressions.
RootFracSolver         Normalization of radical and fractional expressions.
SgnSolver              Inequality reasoning using basic facts about sign.
IntervalSolver         Propagation of interval constraints.
SmtLraSolver           Linear real arithmetic theory reasoning.
DerivSolver            Calculation of symbolic derivatives.
IntegralSolver         Calculation of symbolic integrations.
ConDiffFuncSolver      Continuity and differentiability of functions.
ConstTypeSolver        Membership of constant expressions in standard number sets.
NotUnfoldSolver        Normalization of negated propositions.

                   Table 3. Evaluation of Relaxed NFL generation.

Model                           Setting                             pass@1   pass@3
Qwen3-235B-A22B-Instruct        Few-shot prompting without CoT      44.4%    72.3%
Qwen3-235B-A22B-Instruct        Few-shot prompting with CoT         70.3%    90.4%
Qwen2.5-7B-Instruct             LoRA fine-tuning on 2,000           83.6%    89.9%
                                informal-formal pairs



factor α = 256, and learning rate η = 10−4 . The fine-tuned model achieves 83.6%
pass@1 and 89.9% pass@3. The results are summarized in Table 3.
    These results show that Relaxed NFL proofs can be reliably generated by
LLMs. In the few-shot prompting experiments, we observe that many failed sam-
ples are caused by the model drifting toward other formal languages, such as
LaTeX-like notation. This suggests that these failures mainly reflect the model’s
prior bias toward familiar mathematical syntaxes, rather than an intrinsic dif-
ficulty of learning the Relaxed NFL grammar. When the model is allowed to
reason explicitly about the target grammar, it is less likely to drift away from
Relaxed NFL, as suggested by the improvement brought by CoT.
    More importantly, the fine-tuning result shows that the Relaxed NFL can
be learned by smaller models with a lightweight training method and limited
training data. Using only 2,000 informal-formal pairs and LoRA fine-tuning,
Qwen2.5-7B-Instruct achieves a higher pass@1 rate than the much larger Qwen3-
235B-A22B-Instruct with CoT, and a comparable pass@3 rate. This suggests
that a suitable target language can substantially reduce the diﬀiculty of LLM-
based auto-formalization.


6 Related Work

Theorem-Proving Large Language Models One important role of auto-formalization
is to synthesize large amounts of formal proof data. Since the available formal
proof corpora are relatively scarce, auto-formalization has become an essential
                                  Title Suppressed Due to Excessive Length        15

component in the training pipelines of theorem proving LLMs, i.e., LLMs whose
primary goal is to prove theorems in proof assistants. For example, the post-
training data of DeepSeek-Prover [29], Goedel-Prover [14], and AlphaProof [10]
all contain a large number of auto-formalized Lean 4 proofs.
    However, existing work on theorem-proving language models mainly focuses
on exploring more effective post-training methods and proof-search strategies.
For instance, DeepSeek-Prover-V2 [24] uses reinforcement learning to help the
model decompose a problem into subgoals. Other systems improve the quality of
the feedback available to the model. For instance, Seed-Prover [4] combines Lean
compiler feedback, proved lemmas, and self-summarization to refine generated
proofs, while LEGO-Prover [26] maintains a growing library of verified lemmas
and uses them as skills during inference. In contrast, relatively less attention
has been paid to whether the reasoning ability of LLMs can be improved by
carefully designing the target formal representation itself, or to what kind of
language is suitable for mathematical reasoning by LLMs while still remaining
machine-checkable. In this respect, our work is complementary to these systems.

Natural-Language-Like Formal Languages Proof languages that aim to resemble
natural language, or that take readability as a design goal, are usually described
as declarative-style proof languages. Unlike term-style or procedural-style proof
languages, they allow users to write proofs by explicitly stating assumptions,
intermediate claims, and local arguments, which are common structures in in-
formal mathematical writing. Many theorem provers support such declarative
style. For example, Isabelle’s Isar [27] language represents proofs as structured
mathematical texts. It supports nested proof contexts and the introduction of
local variables, but its proof contexts are still tied to the current proof obliga-
tion, and local variables and assumptions cannot be introduced with the same
flexibility as in informal mathematical writing.
    Lean’s verbose-lean4 language [19] combines declarative and procedural styles.
It provides declarative constructs such as have, while also allowing users to ma-
nipulate the proof state through a more natural-language-like surface syntax
that is subsequently elaborated into tactics. However, it has limited support for
structured proofs. For example, nested subproofs are mainly expressed through
by-blocks, whose contents must be written as tactics rather than in the same
declarative style. The Mizar proof language [21] and Naproche’s ForTheL [6]
also follow a declarative style close to conventional mathematical prose. Previ-
ous work has shown that such natural-language-like proof languages can improve
LLM-based auto-formalization. For instance, Draft, Sketch, and Prove [12] uses
natural-language drafts to generate Isar proof skeletons.
    The Relaxed NFL presented in this paper not only supports structured proofs
organized by introducing local variables and assumptions, but also has richer
structures such as problem-solving. In this respect, the Relaxed NFL is closer
to informal mathematical writing. More importantly, terms and propositions in
existing proof languages usually have to refer to precise library definitions, and do
not allow partially specified expressions or the occurrence of free variables, while
the Relaxed NFL preserve the surface form of informal mathematical notation,
16      Authors Suppressed Due to Excessive Length

allowing a degree of ambiguity and context dependence. Subsequent elaboration
steps can repair term-level ambiguities and explicitly reconstruct implicit local
proof contexts to eliminate free variables, thereby offloading part of the reasoning
burden from LLMs during auto-formalization.


7 Conclusion

In this paper, we present an auto-formalization pipeline based on a relaxed natu-
ral formal language. The main idea is to use an intermediate representation that
remains close to informal mathematical writing, instead of directly instructing
LLMs to generate the formal proof language of a specific theorem prover. This
design reduces the representational gap that LLMs need to bridge and makes
auto-formalization less dependent on the details of a particular formal system.
    We introduce the Relaxed NFL as a surface language for LLM-based auto-
formalization, and the Core NFL as a semantically well-defined proof language.
We then describe a verifiable elaboration pipeline from the Relaxed NFL to the
Core NFL, taking notation resolution, problem-solving translation, and implicit
variable scope resolution as examples.
    To verify the correctness of proofs, we generate proof gaps from the Core
NFL and design a dedicated domain-specific tactic language in which LLMs can
generate proof scripts to discharge these gaps. We incorporate theorem libraries
and domain-specific solvers as part of our system to enhance the tactic language
and facilitate LLM-based proof gap discharging.
    Our work demonstrates the feasibility and benefits of using a proof language
closer to natural mathematical writing for auto-formalization. With a carefully
designed elaboration process, the logical rigor that is intentionally left implicit
in the relaxed proof language can be recovered in a controlled and verifiable way,
thereby supporting proof verification. Such design not only makes the language
easier for LLMs to acquire and use, but also improves the readability of formal
proofs.


References

 1. Bancerek, G., Byliński, C., Grabowski, A., Korniłowicz, A., Matuszewski, R., Nau-
    mowicz, A., Pąk, K.: The role of the mizar mathematical library for interactive
    proof development in mizar. J. Autom. Reason. 61(1–4), 9–32 (Jun 2018). https://
    doi.org/10.1007/s10817-017-9440-6, https://doi.org/10.1007/s10817-017-9440-6
 2. Bertot, Y., Castran, P.: Interactive Theorem Proving and Program Development:
    Coq’Art The Calculus of Inductive Constructions. Springer Publishing Company,
    Incorporated, 1st edn. (2010)
 3. Cao, Q., Xie, L., Yan, J.: The llm era demands natural-language-aligned theorem
    provers for mathematics. In: Proceedings of the 1st ACM SIGPLAN International
    Workshop on Language Models and Programming Languages. p. 46–50. LMPL
    ’25, Association for Computing Machinery, New York, NY, USA (2025). https:
    //doi.org/10.1145/3759425.3763384, https://doi.org/10.1145/3759425.3763384
                                    Title Suppressed Due to Excessive Length          17

 4. Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie, A., Jin, X., Jin, X., Li, C.,
    Ma, K., Ren, C., Shen, J., Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang, Z.,
    Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H., Yang, F., Ying, H., Yuan, H.,
    Yuan, Z., Zhan, T., Zhang, C., Zhang, Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y.,
    Zhu, T.H.: Seed-prover: Deep and broad reasoning for automated theorem proving
    (2025), https://arxiv.org/abs/2507.23726
 5. mathlib Community, T.: The lean mathematical library. In: Proceedings of the 9th
    ACM SIGPLAN International Conference on Certified Programs and Proofs. p.
    367–381. POPL ’20, ACM (Jan 2020). https://doi.org/10.1145/3372885.3373824,
    http://dx.doi.org/10.1145/3372885.3373824
 6. De Lon, A., Koepke, P., Lorenzen, A., Marti, A., Schütz, M., Wenzel, M.: The
    isabelle/naproche natural language proof assistant. In: Automated Deduction –
    CADE 28: 28th International Conference on Automated Deduction, Virtual Event,
    July 12–15, 2021, Proceedings. p. 614–624. Springer-Verlag, Berlin, Heidelberg
    (2021). https://doi.org/10.1007/978-3-030-79876-5_36, https://doi.org/10.1007/
    978-3-030-79876-5_36
 7. Demidovich, B.P.: Problems in Mathematical Analysis. Mir Publishers (1970)
 8. Guo, Q., Wang, J., Zhang, J., Kong, D., Huang, X., Xi, X., Wang, W., Wang,
    J., Cai, X., Zhang, S., Ye, W.: Autoformalizer with tool feedback (2025), https:
    //arxiv.org/abs/2510.06857
 9. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen,
    W.: Lora: Low-rank adaptation of large language models (2021), https://arxiv.
    org/abs/2106.09685
10. Hubert, T., Mehta, R., Sartran, L., Horváth, M.Z., Žužić, G., Wieser, E., Huang,
    A., Schrittwieser, J., Schroecker, Y., Masoom, H., Bertolli, O., Zahavy, T., Mand-
    hane, A., Yung, J., Beloshapka, I., Ibarz, B., Veeriah, V., Yu, L., Nash, O.,
    Lezeau, P., Mercuri, S., Sönne, C., Mehta, B., Davies, A., Zheng, D., Pedregosa,
    F., Li, Y., von Glehn, I., Rowland, M., Albanie, S., Velingker, A., Schmitt, S.,
    Lockhart, E., Hughes, E., Michalewski, H., Sonnerat, N., Hassabis, D., Kohli,
    P., Silver, D.: Olympiad-level formal mathematical reasoning with reinforce-
    ment learning. Nature (Nov 2025). https://doi.org/10.1038/s41586-025-09833-y,
    https://doi.org/10.1038/s41586-025-09833-y
11. Jiang, A.Q., Li, W., Jamnik, M.: Multi-language diversity benefits autoformaliza-
    tion. In: Proceedings of the 38th International Conference on Neural Information
    Processing Systems. NIPS ’24, Curran Associates Inc., Red Hook, NY, USA (2024)
12. Jiang, A.Q., Welleck, S., Zhou, J.P., Li, W., Liu, J., Jamnik, M., Lacroix, T., Wu,
    Y., Lample, G.: Draft, sketch, and prove: Guiding formal theorem provers with
    informal proofs (2023), https://arxiv.org/abs/2210.12283
13. Leang, J.O.J., Hong, G., Li, W., Cohen, S.B.: Theorem prover as a judge for
    synthetic data generation. In: Proceedings of the 63rd Annual Meeting of the As-
    sociation for Computational Linguistics (Volume 1: Long Papers). p. 29941–29977.
    Association for Computational Linguistics (2025). https://doi.org/10.18653/v1/
    2025.acl-long.1448, http://dx.doi.org/10.18653/v1/2025.acl-long.1448
14. Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J., Xia, M., Chen, D.,
    Arora, S., Jin, C.: Goedel-prover: A frontier model for open-source automated
    theorem proving (2025), https://arxiv.org/abs/2502.07640
15. Liu, Q., Zheng, X., Lu, X., Cao, Q., Yan, J.: Rethinking and improving autofor-
    malization: Towards a faithful metric and a dependency retrieval-based approach.
    In: The Thirteenth International Conference on Learning Representations (2025),
    https://openreview.net/forum?id=hUb2At2DsQ
18      Authors Suppressed Due to Excessive Length

16. Liu, Q., Zheng, X., Xia, R., Qi, X., Cao, Q., Yan, J.: Beyond theorem proving:
    Formulation, framework and benchmark for formal problem-solving (2025), https:
    //arxiv.org/abs/2505.04528
17. Liu, Y., Zhu, T., Liu, X., Chen, Y., Liu, Z., Guo, Q., Zhang, J., Bao, K., Luo, T.:
    Generalized tree edit distance (gted): A faithful evaluation metric for statement
    autoformalization (2025), https://arxiv.org/abs/2507.07399
18. Lu, W., Du, L., Li, S., Weng, K., Sun, H., Liu, H., Yu, M., Zhang, T., Yu, G.:
    Automated formalization via conceptual retrieval-augmented llms (2026), https:
    //arxiv.org/abs/2508.06931
19. Massot, P.: Teaching Mathematics Using Lean and Controlled Natural Language.
    In: Bertot, Y., Kutsia, T., Norrish, M. (eds.) 15th International Conference on In-
    teractive Theorem Proving (ITP 2024). Leibniz International Proceedings in Infor-
    matics (LIPIcs), vol. 309, pp. 27:1–27:19. Schloss Dagstuhl – Leibniz-Zentrum für
    Informatik, Dagstuhl, Germany (2024). https://doi.org/10.4230/LIPIcs.ITP.2024.
    27, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.27
20. Moura, L.d., Ullrich, S.: The lean 4 theorem prover and programming language. In:
    Automated Deduction – CADE 28: 28th International Conference on Automated
    Deduction, Virtual Event, July 12–15, 2021, Proceedings. p. 625–635. Springer-
    Verlag, Berlin, Heidelberg (2021). https://doi.org/10.1007/978-3-030-79876-5_37,
    https://doi.org/10.1007/978-3-030-79876-5_37
21. Naumowicz, A., Korniłowicz, A.: A brief overview of mizar. In: Proceedings of the
    22nd International Conference on Theorem Proving in Higher Order Logics. p.
    67–72. TPHOLs ’09, Springer-Verlag, Berlin, Heidelberg (2009). https://doi.org/
    10.1007/978-3-642-03359-9_5, https://doi.org/10.1007/978-3-642-03359-9_5
22. Nipkow, T., Wenzel, M., Paulson, L.C.: Isabelle/HOL: a proof assistant for higher-
    order logic. Springer-Verlag, Berlin, Heidelberg (2002)
23. Ospanov, A., Farnia, F., Yousefzadeh, R.: minif2f-lean revisited: Reviewing lim-
    itations and charting a path forward. In: The Thirty-ninth Annual Conference
    on Neural Information Processing Systems (2026), https://openreview.net/forum?
    id=KtaHv0YUyh
24. Ren, Z.Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z.,
    Zhu, Q., Yang, D., Wu, Z.F., Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo,
    D., Ruan, C.: Deepseek-prover-v2: Advancing formal mathematical reasoning via
    reinforcement learning for subgoal decomposition (2025), https://arxiv.org/abs/
    2504.21801
25. Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos, M.D., Sung, F., Vinyes,
    M., Ying, Z., Zhu, Z., Lu, J., de Saxcé, H., Bailey, B., Song, C., Xiao, C., Zhang, D.,
    Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer, J., Michel, J., Yu, L., Dreyfus-Schmidt,
    L., Tunstall, L., Pagani, L., Machado, M., Bourigault, P., Wang, R., Polu, S.,
    Barroyer, T., Li, W.D., Niu, Y., Fleureau, Y., Hu, Y., Yu, Z., Wang, Z., Yang,
    Z., Liu, Z., Li, J.: Kimina-prover preview: Towards large formal reasoning models
    with reinforcement learning (2025), https://arxiv.org/abs/2504.11354
26. Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q., Huang, Y., Xiong, J., Shi, H.,
    Xie, E., Yin, J., Li, Z., Liao, H., Liang, X.: Lego-prover: Neural theorem proving
    with growing libraries (2023), https://arxiv.org/abs/2310.00656
27. Wenzel, M.: Isabelle/isar: A versatile environment for human-readable formal proof
    documents. In: Theorem Proving in Higher Order Logics: TPHOLs 1999. Lecture
    Notes in Computer Science, vol. 1690. Springer (1999)
28. Wiedijk, F.: Mizar’s soft type system. In: Proceedings of the 20th International
    Conference on Theorem Proving in Higher Order Logics. p. 383–399. TPHOLs’07,
    Springer-Verlag, Berlin, Heidelberg (2007)
                                     Title Suppressed Due to Excessive Length           19

29. Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan, C., Li, W., Liang, X.:
    Deepseek-prover: Advancing theorem proving in llms through large-scale synthetic
    data (2024), https://arxiv.org/abs/2405.14333
30. Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang,
    C., Lv, C., Zheng, C., Liu, D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin,
    H., Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J., Zhou, J., Lin,
    J., Dang, K., Bao, K., Yang, K., Yu, L., Deng, L., Li, M., Xue, M., Li, M., Zhang,
    P., Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo, S., Li, T., Tang, T., Yin,
    W., Ren, X., Wang, X., Zhang, X., Ren, X., Fan, Y., Su, Y., Zhang, Y., Zhang, Y.,
    Wan, Y., Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., Qiu, Z.: Qwen3 technical
    report (2025), https://arxiv.org/abs/2505.09388
31. Yang, A., Yang, B., Hui, B., Zheng, B., Yu, B., Zhou, C., Li, C., Li, C., Liu, D.,
    Huang, F., Dong, G., Wei, H., Lin, H., Tang, J., Wang, J., Yang, J., Tu, J., Zhang,
    J., Ma, J., Yang, J., Xu, J., Zhou, J., Bai, J., He, J., Lin, J., Dang, K., Lu, K.,
    Chen, K., Yang, K., Li, M., Xue, M., Ni, N., Zhang, P., Wang, P., Peng, R., Men,
    R., Gao, R., Lin, R., Wang, S., Bai, S., Tan, S., Zhu, T., Li, T., Liu, T., Ge, W.,
    Deng, X., Zhou, X., Ren, X., Zhang, X., Wei, X., Ren, X., Liu, X., Fan, Y., Yao,
    Y., Zhang, Y., Wan, Y., Chu, Y., Liu, Y., Cui, Z., Zhang, Z., Guo, Z., Fan, Z.:
    Qwen2 technical report (2024), https://arxiv.org/abs/2407.10671
32. Zheng, K., Han, J.M., Polu, S.: Minif2f: a cross-system benchmark for formal
    olympiad-level mathematics (2022), https://arxiv.org/abs/2109.00110
20      Authors Suppressed Due to Excessive Length

A      An example proof written in the Relaxed NFL

This appendix presents the Relaxed NFL formalization of a functional-equation
problem from the 1999 International Mathematical Olympiad. The solution is
adapted from the one available on the Art of Problem Solving website: https:
//artofproblemsolving.com/wiki/index.php/1999_IMO_Problems/Problem_6.


     Solve: Find all f such that
       IsFunc(f),
       f : Real -> Real,
       forall (x, y in Real),
         f(x - f(y)) = f(f(y)) + x * f(y) + f(x) - 1

     Solution:
       Set f(0) = c

       [@method Substitute x = y = 0 into forall (x, y in Real),
         f(x - f(y)) = f(f(y)) + x * f(y) + f(x) - 1 @]
       We have f(-c) = f(c) + c - 1

       Assume c = 0 holds {
         We have f(0) = f(0) - 1
         Contradiction
       }

       We have c != 0

       [@method Substitute x = f(y) into forall (x, y in Real),
         f(x - f(y)) = f(f(y)) + x * f(y) + f(x) - 1 @]
       We have c = f(x) + x ^ 2 + f(x) - 1

       Solve the system of equations c = f(x) + x ^ 2 + f(x) - 1 {
         We have f(x) = frac(c + 1, 2) - frac(x ^ 2, 2)
       }

       [@method By x ^ 2 = (-x) ^ 2 @]
       We have f(x) = f(-x)
       We have f(c) = f(-c)
       We have f(c) = f(c) + c - 1
       We have c = 1
       We have f(x) = 1 - frac(x ^ 2, 2)
                                Title Suppressed Due to Excessive Length   21

B     Grammar of the Relaxed Natural Formal Language
⟨program⟩ ::= ⟨assumptions⟩ Prove: ⟨term⟩ Proof: ⟨proof ⟩
  | ⟨assumptions⟩ Solve: ⟨solving_step⟩ Solution: ⟨derivation⟩
⟨assumptions⟩ ::= Assume: ⟨term⟩ (, ⟨term⟩)*
⟨proof ⟩ ::= ⟨derivation⟩ QED
⟨derivation⟩ ::= ⟨annotated_step⟩*
⟨annotated_step⟩ ::= ([@method ⟨method⟩ @])? ⟨step⟩
⟨step⟩ ::= ⟨forward_step⟩
  | ⟨backward_step⟩
  | ⟨subgoal_step⟩ { ⟨proof ⟩ }
  | ⟨action_step⟩
  | ⟨local_action_step⟩ { ⟨arguments⟩ }
  | ⟨solving_step⟩ { ⟨arguments⟩ }
⟨forward_step⟩ ::= We have ⟨term⟩
  | Contradiction
⟨backward_step⟩ ::= It suffices to prove ⟨term⟩
⟨subgoal_step⟩ ::= We prove that ⟨term⟩
⟨action_step⟩ ::= Set ⟨term⟩ = ⟨term⟩
  | Take ⟨term⟩ as a witness
  | After checking, ⟨term⟩ (, ⟨term⟩) satisfies the constraints
  | After checking, ⟨term⟩ (, ⟨term⟩) does not satisfy the constraints
⟨local_action_step⟩ ::= Assume ⟨term⟩ (, ⟨term⟩) holds
  | For arbitrary ⟨term⟩ (, ⟨term⟩) satisfying ⟨term⟩ (, ⟨term⟩)
  | In order for ⟨term⟩ to hold
⟨solving_step⟩ ::= Find ⟨term⟩ (, ⟨term⟩) such that ⟨term⟩ (, ⟨term⟩)
  | Find all ⟨term⟩ (, ⟨term⟩) such that ⟨term⟩ (, ⟨term⟩)
  | Find the range of ⟨term⟩ (, ⟨term⟩) such that ⟨term⟩ (, ⟨term⟩)
  | Solve the system of equations ⟨term⟩ (, ⟨term⟩)
  | Solve the system of inequalities ⟨term⟩ (, ⟨term⟩)
  | Compute ⟨term⟩ (, ⟨term⟩)
⟨method⟩ ::= By ⟨term⟩
 | By ⟨string⟩
 | Similarly
 | Substitute ⟨term⟩ (, ⟨term⟩) into ⟨term⟩
 | Multiply both sides of ⟨term⟩ by ⟨term⟩
 | Square both sides of ⟨term⟩
 | Take limits on both sides ⟨term⟩ as ⟨term⟩
 | ...
