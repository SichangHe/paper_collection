                                         Machine-Generated, Machine-Checked Proofs for a Verified
                                         Compiler (Experience Report)
                                         ZOE PARASKEVOPOULOU, National Technical University of Athens, Greece
                                         We report on using an agentic coding assistant (Claude Code, powered by Claude Opus 4.6) to mechanize
                                         a substantial Rocq correctness proof from scratch, with human guidance but without human proof writing.
                                         The proof establishes semantic preservation for the administrative normal form (ANF) transformation in the
                                         CertiCoq verified compiler for Rocq. The closely related continuation-passing style (CPS) transformation in
arXiv:2602.20082v1 [cs.PL] 23 Feb 2026




                                         CertiCoq was previously proved correct by human experts over several months [Paraskevopoulou and Grover
                                         2021]. We use this proof as a template and instruct the LLM to adapt the proof technique to the ANF setting,
                                         which differs in important technical ways. The resulting ANF proof comprises approximately 7,800 lines of
                                         Rocq (larger than the 5,300-line CPS proof) and was developed in approximately 96 hours. We describe the
                                         proof technique and report on the experience of developing it with an LLM, discussing both the strengths and
                                         limitations of the approach and its implications for verified compiler construction.

                                         1   Introduction
                                         Recent advances in large language models (LLMs) have transformed software development. Agentic
                                         coding assistants such as GitHub Copilot [GitHub 2025] and Claude Code [Anthropic 2025] are now
                                         routinely used to generate and refactor code, and early reports suggest that LLMs can dramatically
                                         accelerate software development [Peng et al. 2023]. At the same time, correctness of LLM-generated
                                         code remains a pressing issue. Software bugs are pervasive even in carefully hand-written code; for
                                         LLM-generated code that the user may not fully understand, the risks are compounded.
                                            This raises a question: can LLMs generate not only code, but also machine-checked proofs of
                                         correctness for that code? If so, software could, in principle, come with formal guarantees certified by
                                         an independent proof checker, guarantees that are unaffected by whether the code was written by
                                         a human or an LLM. This vision, machine-generated code with machine-generated, machine-checked
                                         proofs, represents a compelling direction for the future of software engineering, and one that is
                                         becoming increasingly plausible.
                                            This paper contributes a case study in this direction. We investigate whether a state-of-the-art
                                         LLM, given a suitable template and human guidance, can develop a substantial mechanized proof
                                         in the Rocq proof assistant. Our case study is grounded in a concrete, technically demanding
                                         compiler verification task: proving the correctness of an ANF transformation in the CertiCoq
                                         verified compiler [Anand et al. 2017].
                                            The case study. CertiCoq compiles Gallina (the specification language of the Rocq prover) to
                                         C [Savary Bélanger et al. 2019] and WebAssembly [Meier et al. 2025], via a pipeline of transfor-
                                         mations, a substantial portion of which has been formally verified [Paraskevopoulou and Appel
                                         2019; Paraskevopoulou et al. 2021; Savary Bélanger and Appel 2017]. The pipeline employs Meta-
                                         Coq [Sozeau et al. 2020] as a front end to extract an untyped intermediate representation from
                                         Gallina, which is then translated into a functional intermediate language via either a continuation-
                                         passing style (CPS) transformation or an administrative normal form (ANF) transformation. The
                                         correctness of the CPS transformation was established by Paraskevopoulou and Grover [2021]
                                         using a novel proof technique that combines syntactic simulation arguments with step-indexed
                                         logical relations [Ahmed 2006; Appel and McAllester 2001]. The proof, mechanized in Rocq, is ap-
                                         proximately 4,200 lines and was developed over several months by human experts. The application
                                         of the same proof technique to the ANF transformation was left as future work.
                                         Author’s Contact Information: Zoe Paraskevopoulou, National Technical University of Athens, Greece, zoepar@softlab.
                                         ntua.gr.
1:2                                                                                         Zoe Paraskevopoulou


   In this paper, we report on an experiment in which we used Claude Code (an agentic LLM
tool for software development) to develop the ANF correctness proof, with the authors providing
high-level guidance, help with reasoning using natural language explanations (which was required
in surprisingly few cases), and and reviewing the generated proofs. The authors did not write
Rocq proofs directly and the proof was conducted from scratch. The experiment was largely
successful. The LLM produced approximately 6,000 lines of Rocq proof, covering the central
semantic preservation theorem for terminating programs, several auxiliary lemmas, and various
supporting definitions. The LLM correctly identified that the technique that is used to show that
the CPS transformation preserves diverging behaviors does not generalize to the ANF setting,
proving a counterexample. The proof follows the same high-level structure as the CPS proof, but,
despite the structural similarity, there are important technical differences in the reasoning due to
the different nature of the ANF transformation. As an empirical evidence of complexity relative
to the CPS proof, we report that an author of this paper has previously attempted to develop the
ANF proof manually but set it aside due to complexity and time constraints. The progress of the
LLM-mechanized proof was documented with frequent commits to a public repository that span
the course of approximately 96 hours.

      Contributions. This paper makes the following contributions:
        • We present a mechanized correctness proof of the ANF transformation of the CertiCoq
          compiler (section 4), following the proof technique of the CPS correctness proof of Paraske-
          vopoulou and Grover [2021]. The correctness statement covers semantic preservation for
          terminating source programs.
        • We report on the experience of using an LLM (Claude Code, powered by Claude Opus 4.6) to
          develop this proof (section 5). We describe the experimental setup, the interaction process,
          the challenges encountered, and the lessons learned.
        • We discuss the broader implications of LLM-assisted proof development for programming
          languages research and verified compiler construction (section 6).

   Paper overview. In section 2, we overview the proof technique used for the CPS transformation.
Section 3 provides the technical setup for the proof, including the source and target languages,
their semantics, and the logical relation. In section 4, we describe the ANF transformation and
its correctness proof. Section 5 reports on the experience of developing the proof with an LLM,
and section 6 discusses implications and future directions. We cover related work in section 7
and conclude in section 8. Section A presents detailed proof development statistics and section B
provides a curated selection of user prompts from the conversation transcripts.

2      The CPS Proof Technique
Proving a compiler transformation correct amounts to proving that the observable behaviors of the
compiled program are a subset of the observable behaviors of the source program. For deterministic
languages, this can be expressed as forward simulation [Leroy 2009]: whenever the source program
takes a step 𝑒 → 𝑒 ′ , the compiled program takes one or more steps to reach the translation of 𝑒 ′ ,
that is, [𝑒] →+ [𝑒 ′ ]. There are many transformation that satisfy this simple commuting diagram,
but the CPS transformation is not one of them due to well-studied technical obstacles [Dargaye
and Leroy 2007].
   Let [𝑒] 𝑘 denote the CPS translation of an expression 𝑒 with current continuation 𝑘, and 𝑣¯
the CPS translation of a value. The application case of a CPS transformation can be defined as
[𝑣 1 𝑒 2 ] 𝑘 = (𝜆𝑚. [𝑒 2 ] 𝜆𝑛. 𝑚 𝑘 𝑛 ) 𝑣¯1 . The outer (𝜆𝑚. . . .) 𝑣¯1 is an administrative redex: a 𝛽-redex that
the transformation introduces with no source counterpart.
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                              1:3


   Suppose 𝑣 1 𝑒 2 → 𝑣 1 𝑒 2′ where 𝑒 2 → 𝑒 2′ . A naive simulation tries to show [𝑣 1 𝑒 2 ] 𝑘 →+ [𝑣 1 𝑒 2′ ] 𝑘 .
Contracting the administrative redex and applying the induction hypothesis on 𝑒 2 → 𝑒 2′ brings
the target to [𝑒 2′ ] 𝜆𝑛. 𝑣¯1 𝑘 𝑛 . But the goal [𝑣 1 𝑒 2′ ] 𝑘 = (𝜆𝑚. [𝑒 2′ ] 𝜆𝑛. 𝑚 𝑘 𝑛 ) 𝑣¯1 is not this term: it is a
fresh administrative redex whose contractum is exactly what we reached. We would need to step
backwards to close the diagram, which is impossible. The naive simulation fails.
   An orthogonal obstacle arises from fresh binder names. As Paraskevopoulou and Grover [2021]
explain, when 𝑒 → 𝑒 ′ is a reduction step in the source, [𝑒] 𝑘 may reduce to a term that is 𝛼-equivalent
to [𝑒 ′ ] 𝑘 but not syntactically equal, because two invocations of the CPS transformation may use
different fresh-name counters. The simulation diagram must then be extended with 𝛼-equivalence,
which is possible but tedious and brittle.
   The key insight of Paraskevopoulou and Grover [2021] is to replace the reduction relation at the
target level with logical relatedness. Rather than requiring that [𝑒] 𝑘 reduces to exactly [𝑒 ′ ] 𝑘 after
each source step 𝑒 → 𝑒 ′ , the proof only requires:
                                           𝑒 → 𝑒′       =⇒        [𝑒] 𝑘 ≲ [𝑒 ′ ] 𝑘 .
   where ≲ is a standard logical relation defined over terms which is reflexive and transitive (we
give a formal definition of the logical relation used in this setting in section 3.3).
   Returning to the example: instead of finding a reduction sequence from [𝑣 1 𝑒 2 ] 𝑘 to [𝑣 1 𝑒 2′ ] 𝑘 , we
show they are logically related. The logical relation satisfies Reduce-App: a 𝛽-redex is logically
related to its contractum (in either direction). In addition, 𝛼-equivalent terms are logically related,
so there is no need to reason explicitly about 𝛼-equivalence. Together with transitivity and the
induction hypothesis, the chain closes cleanly:
                     [𝑣 1 𝑒 2 ] 𝑘 = (𝜆𝑚. [𝑒 2 ] 𝜆𝑛. 𝑚 𝑘 𝑛 ) 𝑣¯1
                                ≲𝑖 [𝑒 2 ] 𝜆𝑛. 𝑣¯1 𝑘 𝑛                                  (Reduce-App)
                                ≲ [𝑒 2′ ] 𝜆𝑛. 𝑣¯1 𝑘 𝑛
                                  𝑖
                                                                                       (IH)
                                ≲𝑖 (𝜆𝑚. [𝑒 2′ ] 𝜆𝑛. 𝑚 𝑘 𝑛 ) 𝑣¯1                        (Reduce-App)
                                = [𝑣 1 𝑒 2′ ] 𝑘
Transitivity absorbs the administrative redexes on both sides. There is no need to step backwards:
the relation sees through the administrative structure to the underlying semantics.

3     Technical Setup
In this section, we provide the technical setup of our experiment, including the source and target
languages, their semantics, and the logical relation used in the proof. These are all parts of the
CertiCoq compiler. For the full definitions of the semantics of the two languages, we refer the
reader to Paraskevopoulou and Grover [2021].

3.1    Source Language
The source language, 𝜆DS , is an untyped, call-by-value lambda calculus using de Bruijn indices. The
grammar is shown in fig. 1a. Variables are natural numbers; the environment 𝑣 is a sequence of
values, and the expression 𝑛 evaluates by looking up the 𝑛-th entry. The language is extended with
let-bindings, fixpoints fix(𝑒), constructor application and pattern matching. Mutually recursive
functions are not shown in the paper for simplicity but are supported in the actual definitions.
                                                                                 𝑓
   The semantics of 𝜆DS is given by a big-step evaluation relation written 𝑣; 𝑒 ⇓src Res(𝑣). 𝑣 is the
evaluation environment, 𝑒 is the evaluated expression, 𝑓 is the fuel value which decreases with
each step of evaluation, and Res(𝑣) is the result of the execution, which can be either a value 𝑣 or
an out-of-time result OOT, indicating that the fuel has run out.
1:4                                                                                            Zoe Paraskevopoulou


       𝑒    ::=   𝑛                                               𝑒   ::=    let 𝑥 = C(𝑦) in 𝑒
              |   let 𝑒 1 in 𝑒 2                                        |    let 𝑥 = 𝑦.𝑖 in 𝑒
              |   fix(𝑒)                                                |    fun 𝑓 𝑥 = 𝑒 1 in 𝑒 2
              |   𝑒1 𝑒2                                                 |    let 𝑥 = 𝑓 𝑦 in 𝑒
              |   C(𝑒)                                                  |    case 𝑦 of [C𝑖 → 𝑒𝑖 ] 𝑖 ∈𝐼
              |   match 𝑒 with [C𝑖 → 𝑒𝑖 ] 𝑖 ∈𝐼                          |    𝑓 𝑥
                                                                        |    ret(𝑥)
       𝑣    ::= C(𝑣) | Clos(𝑣, 𝑒)
                                                                  𝑣   ::= C(𝑣) | Clos(𝜎, fun 𝑓 𝑥 = 𝑒)
                  (a) Source language 𝜆DS .                       𝜎    = Var ⇀ Val

                                                                            (b) Target language 𝜆ANF .

                                              Fig. 1. Language grammars.


3.2        Target Language
The target language, 𝜆ANF , is a lambda calculus in administrative normal form, with named variables.
In this representation, every intermediate result is bound to a name. The grammar is shown in
Figure 1b. The seven expression forms are: constructor allocation let 𝑥 = C(𝑦) in 𝑒, field projection
let 𝑥 = 𝑦.𝑖 in 𝑒, function definition fun 𝑓 𝑥 = 𝑒 1 in 𝑒 2 , non-tail call let 𝑥 = 𝑓 𝑦 in 𝑒, case dispatch
case 𝑦 of [C𝑖 → 𝑒𝑖 ] 𝑖 ∈𝐼 , tail call 𝑓 𝑥, and the return form ret(𝑥). Environments 𝜎 are finite maps
from variables to values; values are constructor values C(𝑣) or closures ⟨𝜎, fun 𝑓 𝑥 = 𝑒⟩.
   The semantics of the target language is given by a big-step operational semantics, written
      𝑓
𝜎; 𝑒 ⇓trg 𝑟 , where 𝜎 is the evaluation environment, 𝑒 is the evaluated expression, 𝑓 is the fuel value,
and 𝑟 is the result of the execution, which can be either a value 𝑣 or an out-of-time result OOT.
      1-hole context. We define 1-hole contexts E as 𝜆ANF expression with a hole • in tail-position:
                                              E   ::=   •
                                                    |   let 𝑥 = C(𝑦) in E
                                                    |   let 𝑥 = 𝑦.𝑖 in E
                                                    |   let 𝑥 = 𝑓 𝑦 in E
                                                    |   fun 𝑓 𝑥 = 𝑒 in E
We write E [ 𝑒 ] for the expression obtained by replacing • with 𝑒, and E1 ◦E2 for context composition.
The ANF transformation produces pairs (𝐶, 𝑟 )—a context and a result variable—such that the full
target expression is 𝐶 [ ret(𝑟 ) ].

3.3        Logical Relation
The correctness proof uses step-indexed, untyped logical relations. This logical relation has been
used to prove the correctness of all 𝜆ANF -to-𝜆ANF transformations in CertiCoq [Paraskevopoulou
et al. 2021], and in the correctess proof of the CPS transformation (albeit in a different way). The
relation is defined mutually over values, results, and expressions (fig. 2).
   Two values are related at step 𝑘, written 𝒱 𝑘 (𝑣 1, 𝑣 2 ), as follows. Two constructor values are related
when their tags agree and their fields are pointwise related. Two closures ⟨𝜎1, fun 𝑓 𝑥 = 𝑒 1 ⟩ and
⟨𝜎2, fun 𝑔 𝑦 = 𝑒 2 ⟩ are related when, for every 𝑖 < 𝑘 and every pair of argument vectors 𝒱 𝑖 (𝑣 1, 𝑣 2 ),
the two bodies yield related expression configurations in their respective extended environments.
The strict decrease from 𝑘 to 𝑖 < 𝑘 at each function application ensures that the definition is
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                                    1:5


    Value relation
                            def
    𝒱 𝑘 (C1 (𝑣 1 ), C2 (𝑣 2 )) = C1 = C2 ∧ 𝒱 𝑘 (𝑣 1, 𝑣 2 )
                                                       def
    𝒱 𝑘 (⟨𝜎1, fun 𝑓 𝑥 = 𝑒 1 ⟩, ⟨𝜎2, fun 𝑔 𝑦 = 𝑒 2 ⟩) =                     Result relation
      ∀ (𝑖 < 𝑘) 𝑣 1 𝑣 2, 𝒱 𝑖 (𝑣 1, 𝑣 2 ) ⇒                                                      def
                                                                           ℛ𝑘 (OOT, OOT) = True
       len(𝑥) = len(𝑣 1 ) ⇒                                                                           def
       len(𝑦) = len(𝑣 2 ) ∧ ℰ 𝑖 (𝜎1′ , 𝑒 1 ) (𝜎2′ , 𝑒 2 )                  ℛ𝑘 (Res(𝑣 1 ), Res(𝑣 2 )) = 𝒱 𝑘 (𝑣 1, 𝑣 2 )
                                                                                        def
       where 𝜎1′ = 𝜎1 [𝑥 ↦→ 𝑣 1, 𝑓 ↦→ ⟨𝜎1, fun 𝑓 𝑥 = 𝑒 1 ⟩]                ℛ𝑘 (𝑟 1, 𝑟 2 ) = False      Otherwise.
       and 𝜎2′ = 𝜎2 [𝑦 ↦→ 𝑣 2, 𝑔 ↦→ ⟨𝜎2, fun 𝑔 𝑦 = 𝑒 2 ⟩].
                 def
    𝒱 𝑘 (𝑣 1, 𝑣 2 ) = False       Otherwise.
              Expression relation
                                     def
              ℰ 𝑘 (𝜎1, 𝑒 1 ) (𝜎2, 𝑒 2 ) = ∀𝑟 1, 𝜎1 ; 𝑒 1 ⇓trg 𝑟 1 ⇒ ∃ 𝑟 2, 𝜎2 ; 𝑒 2 ⇓trg 𝑟 2 ∧ ℛ𝑘 (𝑟 1, 𝑟 2 )

                                       Fig. 2. Logical relation over 𝜆ANF terms.


well-founded despite the absence of types. The result relation ℛ𝑘 (𝑟 1, 𝑟 2 ) lifts value relatedness:
OOT and OOT are always related, Res(𝑣 1 ) and Res(𝑣 2 ) are related when 𝑣 1 and 𝑣 2 are value-related,
and no other pairs are related.
   The expression relation ℰ 𝑘 (𝜎1, 𝑒 1 ) (𝜎2, 𝑒 2 ) is the heart of the definition: it asserts that for every
evaluation of (𝜎1, 𝑒 1 ) to a result 𝑟 1 , there exists an evaluation of (𝜎2, 𝑒 2 ) to a related result 𝑟 2 . In the
full definition, the relation is additionally parameterized by resource invariants on evaluation costs,
used to establish divergence preservation and asymptotic cost bounds; we refer to [Paraskevopoulou
and Grover 2021; Paraskevopoulou et al. 2021] for details.

4    The ANF Transformation and Its Correctness Proof
The ANF transformation proof is done in two layers: first, we define the ANF transformation as
a relation 𝑆; 𝑥; 𝑒 ▷ 𝐶; 𝑟 ; 𝑆 ′ and prove semantic preservation for this relation. Then, we show that
the executable ANF transformation, defined using a state monad over a supply of fresh names,
satisfies the relational specification. This allows us to separate the monadic reasoning from the
core simulation argument, leading to a cleaner and more modular proof structure. The proof of all
𝜆ANF transformations follows this pattern.
   Unlike CPS, the ANF transformation does not introduce continuations. Functions remain in
direct style, and intermediate results are named with let-bindings rather than being passed to
continuations. The ANF transformation is written 𝑆; 𝑥; 𝑒 ▷ 𝐶; 𝑟 ; 𝑆 ′ , where 𝑆 is a set from which
fresh variables are drawn, 𝑥 is a de Bruijn environment mapping de Bruijn indices to variable
names and 𝑒 is a source expression. 𝐶 is a target 1-hole context and 𝑟 : the context 𝐶 computes the
result of 𝑒 and binds it to 𝑟 . The full ANF expression corresponding to 𝑒 is 𝐶 [ ret(𝑟 ) ]. We explain
some illustrative cases of the transformation below; the definition is shown in Figure 3.
Variable. A DeBruijn index 𝑛 is translated to the corresponding variable in the environment 𝑥 [𝑛]
and the empty context.
Lambda. A lambda fix(𝑒) introduces a fresh function name 𝑓 and parameter 𝑥 1 , translates the
body 𝑒 in environment 𝑥 1 :: 𝑥 to to obtain the context–variable pair (𝐶 1, 𝑟 1 ), and produces context
fun 𝑓 𝑥 1 = 𝐶 1 [ ret(𝑟 1 ) ] in • with result 𝑓 .
Application. An application 𝑒 1 𝑒 2 translates each subexpression, yielding contexts 𝐶 1, 𝐶 2 and result
variables 𝑥 1, 𝑥 2 , and produces context 𝐶 1 ◦ 𝐶 2 ◦ let 𝑟 = 𝑥 1 𝑥 2 in • with 𝑟 holding the result.
1:6                                                                                                                   Zoe Paraskevopoulou


         𝑥 [𝑛] = 𝑦                        𝑥1 ∈ 𝑆              𝑓 ∈ 𝑆 \ {𝑥 1 }           𝑆 \ {𝑥 1, 𝑓 }; 𝑥 1 :: 𝑥; 𝑒 ▷ 𝐶 1 ; 𝑟 1 ; 𝑆 ′
                          Var                                                                                                         Lam
      𝑆; 𝑥; 𝑛 ▷ •; 𝑦; 𝑆                            𝑆; 𝑥; fix(𝑒) ▷ fun 𝑓 𝑥 1 = 𝐶 1 [ ret(𝑟 1 ) ] in •; 𝑓 ; 𝑆 ′

                          𝑆 1 ; 𝑥; 𝑒 1 ▷ 𝐶 1 ; 𝑥 1 ; 𝑆 2        𝑆 2 ; 𝑥; 𝑒 2 ▷ 𝐶 2 ; 𝑥 2 ; 𝑆 3       𝑟 ∈ 𝑆3
                                                                                                               App
                            𝑆 1 ; 𝑥; 𝑒 1 𝑒 2 ▷ 𝐶 1 ◦ 𝐶 2 ◦ let 𝑟 = 𝑥 1 𝑥 2 in •; 𝑟 ; 𝑆 3 \ {𝑟 }

                                      𝑧 ∈ 𝑆1               𝑆 1 \ {𝑧}; 𝑥; 𝑒 ▷e 𝐶; 𝑦; 𝑆 2
                                                                                                  Constr
                                  𝑆 1 ; 𝑥; C(𝑒) ▷ 𝐶 ◦ let 𝑧 = C(𝑦) in •; 𝑧; 𝑆 2

                               𝑆 1 ; 𝑥; 𝑒 1 ▷ 𝐶 1 ; 𝑥 1 ; 𝑆 2        𝑆 2 ; 𝑥 1 :: 𝑥; 𝑒 2 ▷ 𝐶 2 ; 𝑥 2 ; 𝑆 3
                                                                                                             Let
                                           𝑆 1 ; 𝑥; let 𝑒 1 in 𝑒 2 ▷ 𝐶 1 ◦ 𝐶 2 ; 𝑥 2 ; 𝑆 3

                              Fig. 3. ANF transformation (relational definition, excerpt).



4.1     Proof Statements
The main correctness theorem relates the source evaluation of 𝑒 to the ANF-compiled target
context 𝐶 via the logical relation. The statement is adjusted to work with the big-step semantics of
CertiCoq. It states that the source program 𝑒 evaluates to a value 𝑣 in environment 𝑣, and the ANF
transformation produces context 𝐶 with result variable 𝑟 ; then, for any continuation 𝑒𝑘 , running 𝐶
followed by 𝑒𝑘 in the target is logically related to running 𝑒𝑘 directly with 𝑟 bound to the translated
value 𝑣 ′ . We relate 𝑣 and 𝑣 ′ via the ANF value translation relation, written anf_val_rel. We lift
this relation to environments with anf_env_rel.

  Theorem 4.1 (ANF Correctness). Let 𝑣 be a well-formed environment, 𝑒 a well-formed source
expression, and 𝑣; 𝑒 ⇓src 𝑣. Suppose 𝑆; 𝑥; 𝑒 ▷ 𝐶; 𝑥; 𝑆 ′ . Then for any target environment 𝜎 such that
anf_env_rel(𝑥, 𝑣, 𝜎), and target value such that anf_val_rel(𝑣, 𝑣 ′ ) we have

                                            ∀ 𝑖, ℰ 𝑖 (𝑒𝑘 , 𝜎 [𝑥 ↦→ 𝑣 ′ ]) (𝐶 [ 𝑒𝑘 ], 𝜎)

where 𝑒𝑘 is any continuation expression such that fv(𝑒𝑘 ) ∩ ((𝑆 \ 𝑆 ′ ) \ {𝑥 }) = ∅.

  The universally quantified continuation 𝑒𝑘 is what makes the statement compositional: it allows
the theorem to be applied inductively in larger contexts, as illustrated by the Let case below.

    Example: the Let case. To illustrate the proof structure, consider the Let case. Suppose 𝑣; let 𝑒 1 in 𝑒 2 ⇓src
𝑟 , which decomposes as 𝑣; 𝑒 1 ⇓src 𝑣 1 and 𝑣 1 :: 𝑣; 𝑒 2 ⇓src 𝑟 . The ANF transformation yields contexts
𝐶 1 , 𝐶 2 and result variables 𝑥 1 , 𝑥 2 such that 𝑆; 𝑥; 𝑒 1 ▷ 𝐶 1 ; 𝑥 1 ; 𝑆 2 and 𝑆 2 ; 𝑥 1 :: 𝑥; 𝑒 2 ▷ 𝐶 2 ; 𝑥 2 ; 𝑆 ′ , with
output context 𝐶 1 ◦ 𝐶 2 and result 𝑥 2 . We must show:

                                         ℰ 𝑖 (𝑒𝑘 , 𝜎 [𝑥 2 ↦→ 𝑣 2′ ]) ((𝐶 1 ◦ 𝐶 2 ) [ 𝑒𝑘 ], 𝜎)

The induction hypotheses for the two sub-evaluations give:

      ℰ 𝑖 (𝑒𝑘 , 𝜎 [𝑥 1 ↦→ 𝑣 1′ ] [𝑥 2 ↦→ 𝑣 2′ ]) (𝐶 2 [ 𝑒𝑘 ], 𝜎 [𝑥 1 ↦→ 𝑣 1′ ])                     (IH for 𝑒 2 , continuation 𝑒𝑘 )
                   ℰ (𝐶 2 [ 𝑒𝑘 ], 𝜎 [𝑥 1 ↦→ 𝑣 1′ ]) (𝐶 1 [ 𝐶 2 [ 𝑒𝑘 ] ], 𝜎)
                     𝑖
                                                                                            (IH for 𝑒 1 , continuation 𝐶 2 [ 𝑒𝑘 ])

Transitivity closes the chain.
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                  1:7


  Top-level correctness. Following Paraskevopoulou and Grover [2021], from theorem 4.1 we can
derive a whole-program correctness corollary. We first define an observation relation ≈ between
source and target values:

                            C(𝑣) ≈ C(𝑣 ′ ) = ∀ 𝑖, 𝑣𝑖 ≈ 𝑣𝑖′
                                             def

                                                                          def
                            Clos(𝑣, fix(𝑒)) ≈ Clos(𝜎, fun 𝑓 𝑥 = 𝑒 ′ ) = True
Constructor values are related when they share the same outermost constructor and have pairwise
related arguments; closures are trivially related. We then define whole-program refinement 𝑒 src ⊑
𝑒 trg :
                                                                                          
                𝑒 src ⊑ 𝑒 trg = ∀ 𝑣, []; 𝑒 src ⇓src 𝑣 ⇒ ∃ 𝑣 ′, ∅; 𝑒 trg ⇓trg 𝑣 ′ ∧ 𝑣 ≈ 𝑣 ′
                              def


   Corollary 4.2 (Whole-Program ANF Correctness). If 𝑒 is well-formed, then there exist 𝐶 and
𝑥 such that 𝑆; []; 𝑒 ▷ 𝐶; 𝑥; 𝑆 ′ , and
                                       𝑒 ⊑ 𝐶 [ ret(𝑥) ]
where 𝐶 [ ret(𝑥) ] is evaluated from the empty target environment.
    A similar corollary is derived for separate compilation, which we elide for brevity.

4.2    Divergence Preservation
The above theorem only establishes semantic preservation for terminating programs. The CPS
correctness proof, also establishes divergence preservation. This is done by additionally proving than
                                                      𝑓src                                            𝑓trg
wen the source program runs out of fuel, 𝑣; 𝑒 src ⇓src     OOT, then so does the target, 𝜎; 𝐶 [ 𝑒𝑘 ] ⇓trg
OOT, for some 𝑓trg ≥ 𝑓src . This is a standard technique for proving divergence preservation with
fuel-based big-step semantics, used, among other by the CakeML compiler [Owens et al. 2017].
    However, this technique fails when the transformation can decrease the number of steps taken
by a program, as is the case for ANF. Consider the source program that applies a variable to another
𝑥 1 𝑥 2 and its ANF translation let 𝑟 = 𝑥 1 𝑥 2 in ret(𝑟 ). With the existing cost models of the source
and target languages, the source program evaluates in three steps (one for the rule of application
and two for the rules of variable lookups), while the target program evaluates in only two steps (one
for the application and one for the variable lookup). We believe that is possible to adjust the cost
models to make the proof go through, but we leave it as future work. The LLM correctly identified
this issue generating a counterexample, but was not able to fix it. The CakeML compiler addresses
this by inserting “tick” instructions that consume fuel without doing work. Paraskevopoulou et al.
[2021] propose an alternative technique based on resource invariants.

4.3    Proof Structure
The ANF correctness proof is organized into four parts, summarized along with their proof sizes in
Table 1. The ANF proof is roughly 47% larger than the CPS proof, with the bulk of the increase in
the semantic preservation component.

5     Experience Report: Proof Development with an LLM
The proof was developed using Claude Code [Anthropic 2025], Anthropic’s agentic coding assistant
for software development, running as a VSCode extension with the Claude Opus 4.6 model. Claude
Code is capable of reading and editing files, searching the codebase, running build commands, and
carrying out multi-step tasks with access to the full development environment. In our setting, it
had access to the entire CertiCoq repository, including the completed CPS proof files, and was able
to invoke Rocqc to type-check generated proofs. We started the proof development by tackling the
1:8                                                                               Zoe Paraskevopoulou


      Part                    Description                                           CPS     ANF
      Semantic preservation Main simulation theorem                                2,243   4,755
      Alpha-equivalence     ANF results from different name supplies are logi-     1,860   1,914
                            cally related
      Monadic/relational    Monadic implementation satisfies relational spec         763     864
      Top-level theorems    Whole-program & separate compilation                     428     250
      Total                                                                       5,294    7,783
                           Table 1. Proof structure and sizes in lines of Rocq.




main semantic preservation theorem, then moved to the other parts of the proof, building up to
the top-level theorems. The human role was to provide high-level guidance: structuring the proof
development into phases, explaining the high-level correspondence between the CPS and ANF
proofs, and providing natural-language feedback on certain proof attempts. Full transcripts of the
interaction have been preserved alongside the proof development.

5.1    Development Process
We initially instructed the LLM to complete an existing partial proof (approximately 1,200 lines)
that had been abandoned months earlier due to complexity. The LLM made some progress but
eventually stalled, cycling through similar unsuccessful attempts. We then started from scratch on
a new branch, instructing the LLM to follow the proof technique and structure of the CPS proof,
adapting the reasoning to the ANF setting.
   Phase 1: Theorem statements and proof skeleton. The LLM began by generating theorem statements
for the four mutually inductive proof obligations and then laid out the proof structure, closely fol-
lowing the organization of the CPS proof files. The initial correctness statement it generated lacked
the universally quantified continuation 𝑒𝑘 (theorem 4.1), which is essential for compositionality.
The LLM corrected this after we pointed it out. It then rapidly dispatched the trivial cases—the
main correctness theorem has thirteen cases—before moving on to the substantive ones.
  Phase 2: Case-by-case development. The LLM worked through the remaining cases one at a time,
partially filling each case, generating admits (often with explanatory comments describing what
remained to be proved), and stating helper lemmas as needed. We guided it on which case to tackle
next, and it would produce short work plans before starting. Once all cases were sketched out with
admits, we prompted it to first resolve the inner admits (within individual cases) before turning to
the outer helper lemmas. This ordering worked well: after the inner admits were filled, the outer
lemmas were discharged with remarkable success.
   Phase 3: Auxiliary proof files. After the main correctness proof was complete, we directed the LLM
to the three remaining proof files. The alpha-equivalence utilities, showing that the transformation
yields logically related results when invoked with different fresh-name supplies, went smoothly,
closely following the CPS template. The monadic/relational correspondence was more disappointing:
despite being conceptually the simplest of the four files (a purely syntactic argument) and the most
similar to the CPS counterpart, the LLM struggled. Rather than adapting the proof, it copied the
CPS proof wholesale and attempted to fix type errors one by one from error messages, leading to
many slow iterations. Ultimately, the author manually fixed two tactic invocations in the last ten
lines of the proof script to explicitly unify a variable that was blocking the remaining goals. The
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)              1:9


top-level theorems were straightforward. During this phase, the LLM discovered that the standard
technique for divergence preservation does not apply to the ANF transformation (section 4.2),
generating a high-level readable comment next to the blocked admit, explaining why.
  Autonomous operation. During the process, the LLM was frequently left to work unattended,
sometimes for hours, and continued to make progress independently, often completing entire
proof cases end-to-end without guidance. Interface issues hindered this: at times, the tool would
repeatedly request permission for routine operations (compiling, grepping) despite permission
having already been granted, blocking progress until a human intervened.

5.2   What the LLM Did Well
    Proof structure and adaptation. The LLM was remarkably effective at adapting the CPS proof
structure to the ANF setting. It understood the high-level proof strategy and was able to instantiate
it in a setting with different technical details.
  Proof reasoning. For each case, the LLM would first reason about why the case should hold, often
producing a natural-language train of thoughts, and then write the corresponding proof script.
When the resulting script contained no remaining admits, it was typically logically correct and
required only syntactic adjustments (tactic names, hypothesis names, goal ordering) to compile.
  Routine proof work. The LLM was proficient at the tedious but necessary parts of mechanized
proving: setting up inductions, performing case analyses, applying known lemmas from the code-
base, and managing proof subgoals. It also independently generated helper lemmas and stated them
with appropriate generality.
   Code quality. The generated proof code was well-structured, with clear naming conventions,
informative comments, and a logical file organization consistent with the existing codebase.

5.3   Challenges and Limitations
   Silently weakening proof statements. The most concerning behavior we observed was the LLM
silently modifying proof statements to make them easier to prove. When it encountered the
divergence preservation obstacle (section 4.2), rather than reporting the difficulty, it removed the
fuel bound from the statement and filled the fuel obligation with a trivial zero value. This was
caught when proving the top-level theorem, but it highlights a risk: the machine-checked guarantee
holds only for the statement that was actually proved, and if that statement has been weakened,
the guarantee may be vacuous. Careful human review of both proof statements and proof bodies
remains essential.
  Incorrect assumptions about variable freshness. The two last admits in the body of the semantics
preservation proof turned out to encode a false assumption: the LLM assumed that certain result
variables in the let-application case could not coincide, so that no shadowing occurs. In fact, the
variables can coincide, requiring a case split and additional reasoning that if they are the same, the
contexts evaluate consistently. The LLM understood the issue and it was able to fix the proof.
   Iterative repair. The interactive repair process once the proof scripts were generated was quite
inefficient. The LLM frequently encountered issues with hypothesis names (which change as the
proof context evolves), and occasionally with goal numbering, leading to unnecessary repair cycles.
This iterative repair process was slow and often circular (fixing one error introduced another). The
LLM interacted with Rocq exclusively through file editing and the Rocqc compiler, with no access
to the interactive proof state. Each fix required a full re-compilation, which was time-consuming.
1:10                                                                                 Zoe Paraskevopoulou


   Context window limitations. The LLM’s context window filled frequently during long proof
sessions, triggering automatic context compaction. After compaction, it would sometimes lose
track of the current proof state and need to re-orient itself by re-reading files and re-grepping the
codebase, work it had already done in the compacted portion of the conversation. This repeated
exploration was time-consuming and suggests that better mechanisms for persistent proof state
across context boundaries would be valuable.
  Attention and focus. The LLM’s focus could be narrow and unpredictable: it would sometimes
jump between distant parts of a proof or preferentially work on easier cases while avoiding difficult
admits. Re-implementing lemmas that already existed in the codebase (but were not imported in
the current file) was another recurring issue.

5.4     Comparison with the CPS Proof
The CPS correctness proof was developed manually by human experts over several months, re-
quiring both conceptual innovation (the proof technique combining syntactic simulations with
step-indexed logical relations) and substantial mechanical effort (formalizing hundreds of lemmas in
Rocq). The ANF proof, by contrast, was developed in approximately 96 hours of LLM-assisted work,
with no manual proof writing and mechanized a known proof strategy. The human contribution
consisted of high-level guidance and review, and occasional natural-language feedback on reasoning
steps. Human effort was not systematically measured; we supervised the process intermittently
while engaged in other work and did not keep a detailed log of hours spent.
    As shown in table 1, the ANF proof is larger than its CPS counterpart (7,783 vs. 5,294 total lines),
with the main correctness file roughly twice the size (4,755 vs. 2,243 lines). The ANF proof is in
some respects more complex than the CPS proof because of the context handling. In other respects
it is simpler: there are no administrative reductions to reason through. This also suggests that the
LLM-generated proof is more verbose than the human-written one.

6      Discussion
   A template-based paradigm for compiler verification. Our experience points toward a new work-
flow for verified compiler development: a human expert designs the proof strategy and builds the
verification infrastructure for one transformation, and an LLM mechanizes subsequent applications
of the same technique to related transformations. CertiCoq’s pipeline is a natural candidate for this
approach: it uses the same logical relation framework to verify a series of 𝜆ANF -to-𝜆ANF transfor-
mations [Paraskevopoulou et al. 2021], each following a similar proof pattern. We anticipate that
LLMs will prove effective at adapting proofs across this family of transformations, substantially
reducing the effort required to extend or modify verified compiler pipelines.
   Toward verified code generation. If LLMs can generate both code and proofs together, verified
software could become more of a norm than an exception. Rather than a single verified compiler
pipeline built with enormous human effort, it might become feasible to generate new verified trans-
formations on demand. Our case study suggests that this vision is within reach for transformations
that follow known proof templates.
  Tool support for LLM-assisted proving. We identified several concrete gaps in tool support:
Proof state access. The LLM interacted with Rocq only through file editing and Rocqc invocations.
Access to the current proof state (goal, hypotheses, available lemmas) could dramatically reduce
the time spent on syntactic repair.
Structured error feedback. Rocqc error messages are designed for human experts. Structured,
machine-readable error output may help LLMs diagnose and fix proof failures more efficiently.
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)              1:11


Persistent state across context windows. Mechanisms for summarizing and preserving proof
progress across context compaction boundaries would reduce the repeated exploration we observed.
   Proof scripts vs. proof terms. A natural question is whether LLMs would be better suited to
generating proof terms (fully explicit proof objects) rather than proof scripts (sequences of tactics).
Proof terms avoid the fragility of tactic scripts, where hypothesis names and goal numbering can
silently change. On the other hand, proof terms are harder to diagnose and repair interactively. We
leave an empirical comparison as future work, but note that many of the iterative repair difficulties
we encountered are artifacts of the tactic-based workflow.
   The changing role of proof automation. If LLMs can reliably generate and repair proof scripts, the
role of custom tactic automation in proof developments may shift. Traditionally, proof engineers
invest significant effort in writing custom tactics and decision procedures to reduce proof burden.
In an LLM-assisted workflow, the emphasis may shift from writing automation to writing clear,
well-structured proof templates that the LLM can follow and adapt.
   Generalizability. The success of our experiment depends on several preconditions: the existence
of a closely related, complete proof serving as a template; a domain expert able to identify corre-
spondences and provide targeted guidance; and a sufficiently capable LLM. How well this approach
generalizes to settings where one or more of these preconditions are absent, e.g., proofs without a
close template, or domains where the human lacks deep expertise, is an important open question.
   Reproducibility and attribution. LLMs are inherently stochastic and the proof generation in our
experiment cannot be reproduced exactly. We mitigate this by making the complete proof and its
commit history publicly available, providing evidence that the proof was developed in a timeframe
consistent with LLM-assisted development. Authorship is also hard to attribute, as there is no
reliable way to determine if the code was LLM generated.
   Education and the future of proof expertise. If mechanized proofs can be generated by LLMs,
researchers will focus more on designing proof strategies and less on the mechanics of tactic-based
proving. At the same time, the ability to evaluate, guide, and debug LLM-generated proofs requires
a level of expertise that is difficult to acquire without hands-on proof experience, suggesting that
proof education remains important, even as its focus shifts.
  Reliance on LLM providers. Our experiment relied on a commercial LLM. This creates a depen-
dency on the continued availability, affordability, and capability of commercial services. Open-source
models, while currently less capable for this task, are an important direction for the community to
develop, both for accessibility and for scientific reproducibility.

7   Related Work
  Agentic proof development. There are early reports on the successful use of agentic proof devel-
opment. Swamy [2026] describes the process of using F* and LLMs to produce 10,000 lines of code
and proof, spanning a range of examples. de Moura [2026] similarly argues that proof assistants
and AI are entering a new symbiotic era, and identifies machine-checked proof generation as a key
near-term opportunity. Our work is an instance of this paradigm applied to compiler verification.
   LLM-assisted proof generation. Several recent papers have explored the use of LLMs for automated
proof generation. Qin et al. [2025] study LLM proof generation for FSCQ, a verified file system in
Rocq, achieving 38% proof coverage on preexisting theorems sampled from the FSCQ codebase.
Our experience suggests that higher coverage is achievable when a closely related proof template
is available, even in end-to-end proof development and not only in standalone lemma proving.
1:12                                                                                               Zoe Paraskevopoulou


   PALM [Lu et al. 2024] analyzes common error patterns in LLM-generated proofs to design a
generate-then-repair approach that corrects low-level errors in LLM generated proofs. Using GPT-
3.5 it achieves 40% coverage on a dataset of 10K+ Rocq theorems, outperforming previous methods
by over 76.6%. CoqPilot [Kozyrev et al. 2024] is a VSCode extension that uses LLMs to fill proof holes
in Rocq files. The tool was evaluated on a dataset of 300 Rocq theorems with proofs of at most 20
tactics with different LLMs, achieving a maximum coverage of 50% when using GPT-4. On a similar
track, Lean Copilot [Song et al. 2025] is a native LLM interface for Lean proof assistant [de Moura
and Ullrich 2021], that assists with automating parts of proof development. Rango [Thompson
et al. 2025] is a synthesis tool for Rocq that, at each proof step, retrieves relevant premises and
similar proofs to guide a fine-tuned LLM. On CoqStoq, a new benchmark of 196,929 theorems
from 2,226 open-source projects, it proves 32.0% of theorems (29% more than the state-of-the-art
Tactician [Blaauwbroek et al. 2020]). Our work differs in scale: these tools focus on automatically
proving many smaller independent lemmas, while we generate a single large, coherent proof, under
user guidance. Most prior work evaluates proof generation on existing proof corpora; we target
previously unproven statements. Our experience supports that integrating such tools in the agentic
proving environment could further speed up the process of mechanized proof development.
   Misu et al. [2024] explore LLM-assisted synthesis of verified Dafny methods by prompting
models to generate verified Danfy programs, achieving as much as 58% coverage on the MBPP
dataset of Python programs [Austin et al. 2021]. Baldur [First et al. 2023] demonstrates whole-proof
generation using Minerva LLM [Lewkowycz et al. 2022] fine-tuned on Isabelle/HOL proofs, using a
repair step to fix low-level errors.
   AI for mechanized mathematics. The use of AI to generate machine-checked proofs for mathemat-
ical theorems is gaining increasing attention. Remarkably, DeepMind’s AlphaProof [Hubert et al.
2025], a formal proof capable of formalizing mathematics in Lean using reinforcement learning,
solved 4 out of the 6 problems in 2024 International Mathematical Olympiad.

8 Conclusion
We have presented a case study in LLM-assisted mechanized proof development. Using an agentic
LLM coding assistant and high-level human guidance, we have developed approximately 6,000
lines of Rocq proof for the correctness of the ANF transformation in CertiCoq in a matter of
days, compared to the months required for the closely related CPS proof developed manually by
human experts. Our experience suggests that LLMs can be highly effective at adapting known proof
techniques to new but related settings, with human guidance at key junctures. We believe that
LLM-assisted proof development may suggest a new paradigm of mechanized proof construction,
and we offer this case study as a concrete data point for further investigation.

Acknowledgments
References
Amal Ahmed. 2006. Step-Indexed Syntactic Logical Relations for Recursive and Quantified Types. In Programming Languages
   and Systems, Peter Sestoft (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 69–83.
Abhishek Anand, Andrew W. Appel, John Gregory Morrisett, Zoe Paraskevopoulou, Randy Pollack, Olivier Savary Bélanger,
   Matthieu Sozeau, and Matthew Weaver. 2017. CertiCoq: A verified compiler for Coq. In CoqPL’17: The Third International
   Workshop on Coq for Programming Languages. 2 pages.
Anthropic. 2025. Claude Code. https://www.anthropic.com/claude-code. Accessed: 2026-02-18.
Andrew W. Appel and David McAllester. 2001. An Indexed Model of Recursive Types for Foundational Proof-Carrying
   Code. ACM Trans. Program. Lang. Syst. 23, 5 (Sept. 2001), 657–683. doi:10.1145/504709.504712
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai,
   Michael Terry, Quoc Le, and Charles Sutton. 2021. Program Synthesis with Large Language Models. arXiv preprint
   arXiv:2108.07732 (2021). https://arxiv.org/abs/2108.07732
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                                   1:13


Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. The Tactician: A Seamless, Interactive Tactic Learner and
   Prover for Coq. In Intelligent Computer Mathematics (CICM) (LNCS, Vol. 12236). Springer, 271–277. doi:10.1007/978-3-030-
   53518-6_17
Zaynah Dargaye and Xavier Leroy. 2007. Mechanized Verification of CPS Transformations. In Proceedings of the 14th
   International Conference on Logic for Programming, Artificial Intelligence and Reasoning (Yerevan, Armenia) (LPAR’07).
   Springer-Verlag, Berlin, Heidelberg, 211–225.
Leonardo de Moura. 2026. Proof Assistants in the Age of AI. Blog post. https://leodemoura.github.io/blog/2026/02/18/proof-
   assistants-in-the-age-of-ai.html Accessed: 2026-02-19.
Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and Programming Language. In Automated
   Deduction – CADE 28 (LNCS, Vol. 12699). Springer, 625–635. doi:10.1007/978-3-030-79876-5_37
Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-Proof Generation and Repair with Large
   Language Models. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the
   Foundations of Software Engineering (San Francisco, CA, USA) (ESEC/FSE 2023). Association for Computing Machinery,
   New York, NY, USA, 1229–1241. doi:10.1145/3611643.3616243
GitHub. 2025. GitHub Copilot. https://github.com/features/copilot. Accessed: 2026-02-18.
Thomas Hubert, Rishi Mehta, Laurent Sartran, et al. 2025. Olympiad-level formal mathematical reasoning with reinforcement
   learning. Nature (2025). doi:10.1038/s41586-025-09833-y
Andrei Kozyrev, Gleb Solovev, Nikita Khramov, and Anton Podkopaev. 2024. CoqPilot, a plugin for LLM-based generation
   of proofs. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (Sacramento,
   CA, USA) (ASE ’24). Association for Computing Machinery, New York, NY, USA, 2382–2385. doi:10.1145/3691620.3695357
Xavier Leroy. 2009. A Formally Verified Compiler Back-end. Journal of Automated Reasoning 43, 4 (2009), 363–446.
Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone,
   Cem Anil, Imanol Schlag, Theo Gutman-Solo, et al. 2022. Solving Quantitative Reasoning Problems with Language
   Models. Advances in Neural Information Processing Systems 35 (2022), 3843–3857. https://arxiv.org/abs/2206.14858
Minghai Lu, Benjamin Delaware, and Tianyi Zhang. 2024. Proof Automation with Large Language Models. In Proceedings
   of the 39th IEEE/ACM International Conference on Automated Software Engineering (Sacramento, CA, USA) (ASE ’24).
   Association for Computing Machinery, New York, NY, USA, 1509–1520. doi:10.1145/3691620.3695521
Wolfgang Meier, Martin Jensen, Jean Pichon-Pharabod, and Bas Spitters. 2025. CertiCoq-Wasm: A Verified WebAssembly
   Backend for CertiCoq. In Proceedings of the 14th ACM SIGPLAN International Conference on Certified Programs and Proofs
   (CPP 2025). Association for Computing Machinery, New York, NY, USA, 127–139. doi:10.1145/3703595.3705879
Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, and James Noble. 2024. Towards AI-assisted Synthesis of Verified
   Dafny Methods. In Proceedings of the ACM International Conference on the Foundations of Software Engineering (FSE ’24).
   Association for Computing Machinery, New York, NY, USA. doi:10.1145/3643763
Scott Owens, Michael Norrish, Ramana Kumar, Magnus O. Myreen, and Yong Kiam Tan. 2017. Verifying Efficient Function
   Calls in CakeML. Proc. ACM Program. Lang. 1, ICFP, Article 18 (Aug. 2017), 27 pages. doi:10.1145/3110262
Zoe Paraskevopoulou and Andrew W. Appel. 2019. Closure Conversion is Safe for Space. Proc. ACM Program. Lang. 3, ICFP,
   Article 83 (July 2019), 29 pages. doi:10.1145/3341687
Zoe Paraskevopoulou and Anvay Grover. 2021. Compiling with Continuations, Correctly. Proc. ACM Program. Lang. 5,
   OOPSLA, Article 114 (Oct. 2021), 29 pages. doi:10.1145/3485491
Zoe Paraskevopoulou, John M. Li, and Andrew W. Appel. 2021. Compositional Optimizations for CertiCoq. Proc. ACM
   Program. Lang. 3, ICFP, Article 86 (July 2021), 30 pages. doi:10.1145/3341687
Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. 2023. The Impact of AI on Developer Productivity: Evidence
   from GitHub Copilot. arXiv preprint arXiv:2302.06590 (2023). https://arxiv.org/abs/2302.06590
Jianxing Qin, Alexander Du, Danfeng Zhang, Matthew Lentz, and Danyang Zhuo. 2025. Can Large Language Models Verify
   System Software? A Case Study Using FSCQ as a Benchmark. In Proceedings of the 2025 Workshop on Hot Topics in
   Operating Systems (Banff, AB, Canada) (HotOS ’25). Association for Computing Machinery, New York, NY, USA, 34–41.
   doi:10.1145/3713082.3730382
Olivier Savary Bélanger and Andrew W. Appel. 2017. Shrink Fast Correctly!. In Proceedings of the 19th International Symposium
   on Principles and Practice of Declarative Programming (Namur, Belgium) (PPDP ’17). Association for Computing Machinery,
   New York, NY, USA, 49–60. doi:10.1145/3131851.3131859
Olivier Savary Bélanger, Matthew Z. Weaver, and Andrew W. Appel. 2019. Certified Code Generation from CPS to C. (Oct.
   2019). Unpublished manuscript. https://www.cs.princeton.edu/~appel/papers/CPStoC.pdf.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. 2025. Lean Copilot: Large Language Models as Copilots for Theorem
   Proving in Lean. In Proceedings of the International Conference on Neuro-symbolic Systems (Proceedings of Machine Learning
   Research, Vol. 288). PMLR, 144–169. https://proceedings.mlr.press/v288/song25a.html
Matthieu Sozeau, Abhishek Anand, Simon Boulier, Cyril Cohen, Yannick Forster, Fabian Kunze, Gregory Malecha, Nicolas
   Tabareau, and Théo Winterhalter. 2020. The MetaCoq Project. Journal of Automated Reasoning (Feb. 2020). doi:10.1007/
1:14                                                                                               Zoe Paraskevopoulou


   s10817-019-09540-0
Nikhil Swamy. 2026. Agentic Proof-Oriented Programming. RiSE MSR Blog. https://risemsr.github.io/blog/2026-02-04-nik-
   agentic-pop/ Accessed: 2026-02-18.
Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-Stern, Yuriy Brun, João F. Ferreira, Sorin Lerner,
   and Emily First. 2025. Rango: Adaptive Retrieval-Augmented Proving for Automated Software Verification. In Proceedings
   of the IEEE/ACM 47th International Conference on Software Engineering (ICSE ’25). ACM. doi:10.1109/ICSE55347.2025.00161

A      Proof Development Statistics
We report statistics on the proof development process, extracted from the preserved conversation
transcripts (JSONL logs) of all Claude Code sessions. This was the author’s first experience using
an LLM for mechanized proof development and the first time using Claude Code. As a result, no
systematic plan for structuring the interaction or measuring progress was established in advance.
The development was tracked through 80 manual git commits. The proof was developed across two
Claude Code sessions: the author started in one session on Day 0, then accidentally switched to a
new session the next day and continued there for the remainder of the development. The statistics
reported below are aggregated across both sessions. The author subscribed to the Claude Max 20x
plan; the weekly usage limit was sufficient for the entire proof development.
  Overall statistics. Table 2 summarizes the aggregate tool usage across all sessions. The develop-
ment spanned five consecutive days with 90.2 wall-clock hours (elapsed time from first to last event
each day) and 62.6 active hours (an approximation of actual running time, obtained by excluding
gaps of more than 30 minutes with no recorded event). The human provided 114 prompts in total,
while the LLM performed 6,538 tool invocations. Context compaction occurred 101 times across
the five days, reflecting the long-running nature of the sessions.

                                        Metric                           Count
                                        User prompts (human)                114
                                        Context compactions                 101
                                        Rocqc/make invocations              872
                                        Grep/search calls                 1,684
                                        Edit/Write calls                  1,209
                                        Read calls                        2,383
                                        Bash calls                        1,035
                                        Total tool uses                   6,538
                                        Wall-clock hours                    90.2
                                        Active hours                        62.6
                              Table 2. Aggregate LLM tool usage across all sessions.



   Per-day and per-file activity. Table 3 breaks down the development activity by day. Day 0 was
essentially a fully autonomous run. The single initial prompt (section B) was followed by roughly
4.3 active hours in which the LLM explored the codebase, familiarized itself with the proof structure,
and began working on the semantic preservation proof. The bulk of the semantic preservation
proof was developed on Days 1-2, with the LLM making steady progress on the main proof and the
generated helper lemmas. Days 3-4 were devoted to the 𝛼-equivalence proof, the monadic/relational
correspondence, and the top-level theorems. Day 4 has the highest number of human prompts (50).
The majority of these prompts came after the completion of the top-level corollaries, when the
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                                   1:15


user and LLM encountered a block on the divergence preservation proof. The user prompted the
LLM explain the problem with the proof and provide a counterexample. Then, the user prompted
the LLM to walk through specific proof cases step by step, in an attempt to understand and fix the
source of the issue.

      Day      Prompts      Compact    Rocqc      Grep    Edit/Wr      Read           Bash    Wall (h)     Active (h)
      Day 0           1           9       72       150         111         212          80          4.3          4.3
      Day 1          18          21      211       324         302         589         226         16.2         12.6
      Day 2          22          22      204       456         323         610         255         24.0         14.9
      Day 3          23          34      208       466         270         661         291         24.0         18.3
      Day 4          50          15      177       288         203         311         183         21.7         12.5
      Total        114          101      872      1,684     1,209      2,383      1,035            90.2         62.6
                                    Table 3. Per-day development activity.




   Per-file activity. Table 4 shows the tool usage broken down by proof file and day. The semantic
preservation file received the most attention by far, dominating Days 0-2 and requiring 515 com-
pilation attempts over the five days. The alpha-equivalence utilities and the monadic/relational
correspondence were developed primarily on Days 3 and 4, with the latter requiring 132 compila-
tions despite being a conceptually simpler and smaller proof (section 5.3). The top-level theorems
were the lightest component, completed entirely on Day 4. The per-file totals do not sum to the
overall totals in table 3, as the LLM also read and searched other files in the codebase for reference
lemmas and definitions.

               Proof file                 Day       Prompts    Rocqc        Grep       Edit/Wr       Read
               Semantic preservation      0                0          66      49             107      100
                                          1               18         209     142             302      493
                                          2               18         199     196             320      536
                                          3                1          41      33              48       74
                                          4               22           0      32               2       50
                                          Total           59     515         452             779    1,253
               Alpha-equivalence          3               13         141         79          208      385
                                          4                0           0         12            0       12
                                          Total           13     141             91          208      397
               Monadic/relational         3                1           1          0            1        4
                                          4               14         131         17          164      145
                                          Total           15     132             17          165      149
               Top-level theorems         4                6         28           0           36          19
                                          Total            6         28           0           36          19
                                  Table 4. Tool usage per proof file and day.
1:16                                                                                              Zoe Paraskevopoulou


B      Sample User Prompts
To illustrate the nature of the human–LLM interaction, we present a curated selection of user
prompts drawn from the conversation transcripts. The prompts are lightly edited for readabil-
ity (fixing typos) but are otherwise verbatim. They are grouped by the role they played in the
development process.
    Initial task framing. The very first prompt set up the overall goal:
         “The file LambdaBoxLocal_to_LambdaANF.v contains definitions for CPS and ANF transfor-
         mations. The correctness of the CPS transformation has been proved in the files LambdaBoxLocal_
         to_LambdaANF_correct.v and LambdaBoxLocal_to_LambdaANF_corresp.v; the correctness
         of ANF has not yet been proved. Can you apply a similar proof technique to prove ANF correct?
         The code and proofs that you generate should compile.”

   Directing which task to work on. A large fraction of prompts simply steered the LLM to the next
task:
         “Proceed with the rest of the admits. Note that: for now, ignore preord_exp_Ecase_red; anf_
         cvt_val_alpha_equiv and anf_val_rel_exists will be the last ones to prove.”
         “Amazing job. Now I want you to work to remove all admits in the main proof. Be careful when
         introducing helper lemmas, you should be 100% sure that they are provable. After all inner admits
         are gone we will work on proving all the helper lemmas.”
         “Next I want you to tackle the lemmas in the family anf_cvt_disjoint_*.”
         “Now the final big proof, before we go to top-level lemmas. The correspondence of the relational
         and monadic transformations. This should be done as per CPS; the proof for CPS is in file
         LambdaBoxLocal_to_LambdaANF_corresp. Create a similar file for ANF and do the proof.”
  Looking at the last prompt, the fact that the LLM copied the CPS correspondence proof could be
due to the prompt not explicitly asking to adapt the proof, but rather to create a similar file.
   Mathematical guidance. In few critical cases (for example, the constructor case of the semantic
preservation proof), the human provided detailed the human provided proof ideas in natural
language. The most significant ones are provided below.
         “I have the following idea that I want you to investigate and tell me if it’s feasible.
         • First, abandon all the replace_with_rho stuff you are doing.
         • We know that xs may have duplicates. Let xs[𝑖] = xs[ 𝑗] for 𝑖 ≠ 𝑗. I claim that it should
             be the case that vs0[𝑖] = vs0[ 𝑗]. This will be proven structurally using the ANF conversion
             definition and the definition of the semantics. It may even follow from the definition of the
             conversion that syntactically es[𝑖] = es[ 𝑗], which will make proving vs0[𝑖] = vs0[ 𝑗] easier
             by the determinism of the semantics.
         • Then, using the alpha-equivalence result, preord_val vs’0[𝑖] = vs’0[ 𝑗], which should
             suffice to make the proof go through.
         Examine if this approach works, and if it does, implement it. If not, tell me what the problem is.”
         “I want us to prove the following, then we will use this to show the remaining admit.
         • anf_cvt_rel 𝑆 𝑒 vnames cnstrs 𝑆 ′ 𝐶 𝑥 → 𝑥 = vnames[𝑖] → eval_fuel env 𝑒 𝑣 𝑓 𝑡
            → 𝑣 = vnames[𝑖]
         • anf_cvt_rel_exps 𝑆 es vnames cnstrs 𝑆 ′ 𝐶 xs → xs[ 𝑗] = vnames[𝑖] → eval_fuel_
            exps env es vs 𝑓 𝑡 → vs[ 𝑗] = vnames[𝑖]
         First make sure it is true, then start proving it. You will need mutual induction. If you find that it
         is not true, tell me instantly.”
         “I am thinking how to use the lemmas to remove the first admit. Say that we have a more general
         version of consistent that relates the second list with any relation, not just equality. Then:
Machine-Generated, Machine-Checked Proofs for a Verified Compiler (Experience Report)                    1:17


        • Lemma 1: eval_fuel_many vs′ es vs0 fs ts → anf_cvt_correct_exps vs′ es vs0 fs ts
          → Forall2 (𝜆 𝑣 𝑣 ′ . anf_val_rel 𝑣 𝑣 ′ ) vs0 vs′ 0 → consistent preord_val vs0 vs′ 0.
          You will probably need the anf-equiv lemma for this.
        • Lemma 2: consistent preord_val xs vs → ∃ xs, getlist xs (setlist xs vs 𝜌) = vs′
          ∧ Forall2 preord_val vs vs′ .
        Then these two together should suffice to remove the admit.”
   Corrections and error diagnosis. The human caught errors ranging from silent proof erasure to
tactic misapplication. In a few cases the user fed the proof state directly into the LLM to assist in
fixing low-level tactic errors.
        “It compiled because you erased the proof. The goal is to fix the proof, please add it back.”
        “It is just further down the file. You are trying to use a lemma that is proved later on.”
        “You are inverting HL which is a var. This makes no sense; it is probably due to inconsistent
        naming. You should invert H1 and then zify; lia will work.”
  Nudging and continuing. A substantial portion of prompts were simple continuations, often
needed after the LLM paused waiting for direction or after context compaction:
        “Why did you stop?”      “Carry on please.”    “Continue from where you left off.”
   Discussion of proof limitations. When the LLM identified the divergence preservation obstacle
(section 4.2), the interaction shifted to a collaborative discussion:
        “Can you explain the issue with the bound and the OOT case and what it would take to resolve?”
        “Can you give me a counterexample of the property to put in the paper?”
