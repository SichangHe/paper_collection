                                                      Engineering a Formally Verified Automated Bug Finder
                                                                                                                    Arthur Correnson
                                                                                                                    Dominic Steinhöfel
                                                                                                         arthur.correnson@cispa.de
                                                                                                        dominic.steinhoefel@cispa.de
                                                                                                CISPA Helmholtz Center for Information Security
                                                                                                           Saarbrücken, Germany

                                         ABSTRACT                                                                                    Software Engineering Conference and Symposium on the Foundations of Soft-
                                         Symbolic execution is a program analysis technique executing pro-                           ware Engineering (ESEC/FSE ’23), December 3–9, 2023, San Francisco, CA, USA.
arXiv:2305.05570v2 [cs.PL] 12 Oct 2023




                                                                                                                                     ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3611643.3616290
                                         grams with symbolic instead of concrete inputs. This principle
                                         allows for exploring many program paths at once. Despite its wide
                                         adoption—in particular for program testing–little effort was dedi-
                                         cated to studying the semantic foundations of symbolic execution.                           INTRODUCTION
                                         Without these foundations, critical questions regarding the cor-
                                                                                                                                                 It is now two decades since it was pointed out that program
                                         rectness of symbolic executors cannot be satisfyingly answered:
                                                                                                                                                 testing may convincingly demonstrate the presence of bugs,
                                         Can a reported bug be reproduced, or is it a false positive (sound-
                                                                                                                                                 but can never demonstrate their absence. After quoting this
                                         ness)? Can we be sure to find all bugs if we let the testing tool                                       well-publicized remark devoutly, the software engineer returns
                                         run long enough (completeness)? This paper presents a systematic                                        to the order of the day and continues to refine his testing
                                         approach for engineering provably sound and complete symbolic                                           strategies, just like the alchemist of yore, who continued to
                                         execution-based bug finders by relating a programming language’s                                        refine his chrysocosmic purifications.
                                         operational semantics with a symbolic semantics. In contrast to
                                                                                                                                                                                         E.W. Dijkstra, 1988 [13]
                                         prior work on symbolic execution semantics, we address the cor-
                                         rectness of critical implementation details of symbolic bug finders,                           A bridge that works fine for a year but collapses during a windy
                                         including the search strategy and the role of constraint solvers to                         day is considered a failure. A program that works fine for a year
                                         prune the search space. We showcase our approach by implement-                              but crashes for a certain input is considered buggy. This ridiculous
                                         ing WiSE, a prototype of a verified bug finder for an imperative                            analogy reflects the reality of software engineering: While civil
                                         language, in the Coq proof assistant and proving it sound and com-                          engineers carefully identify loads and associated stresses on the
                                         plete. We demonstrate that the design principles of WiSE survive                            structures they build and create their designs accordingly, prevent-
                                         outside the ecosystem of interactive proof assistants by (1) automat-                       ing tragic crashes upfront, “bugs” in software are most frequently
                                         ically extracting an OCaml implementation and (2) transforming                              reported by users only after deployment [29]. However, software
                                         WiSE to PyWiSE, a functionally equivalent Python version.                                   engineers are in a fortunate position: They can stress-test the final
                                                                                                                                     product before it is shipped to users. This becomes an opportu-
                                         CCS CONCEPTS                                                                                nity only if programmers possess adequate verification tools. The
                                         • Theory of computation → Program verification; Operational                                 predominant verification discipline today is testing, which aims
                                         semantics; Higher order logic; Automated reasoning; • Software and                          to find bugs that are actionable in the sense that running the pro-
                                         its engineering → Semantics; Software testing and debugging;                                gram under test with an input provided by the testing tool results
                                         Formal software verification; Software verification; Automated                              in an error state. For example, evolutionary graybox fuzzers (such
                                         static analysis.                                                                            as AFL++ [14]) mutate inputs from an initial population and add
                                                                                                                                     mutants covering new parts in the program. While modern fuzzers
                                                                                                                                     work exceptionally well in many cases, the effectiveness of evolu-
                                         KEYWORDS
                                                                                                                                     tionary fuzzers strongly depends on the quality of the initial seed
                                         Symbolic Execution, Testing, Program Verification, Symbolic Se-                             inputs [26]. Furthermore, they struggle to cover code guarded with
                                         mantics, Proof Assistants                                                                   complex constraints. Consider the Python program
                                         ACM Reference Format:                                                                                         if x == hash((y, z)): fail()
                                         Arthur Correnson and Dominic Steinhöfel. 2023. Engineering a Formally                       Finding a triple of values satisfying the if condition randomly or
                                         Verified Automated Bug Finder. In Proceedings of the 31st ACM Joint European                by mutating previous inputs is extremely difficult. Indeed, Bundt
                                                                                                                                     et al. [9] demonstrated that graybox fuzzers are “mostly useless”
                                         Permission to make digital or hard copies of part or all of this work for personal or       for certain bugs. However, they state that integrating symbolic
                                         classroom use is granted without fee provided that copies are not made or distributed       execution with graybox fuzzers to so-called hybrid fuzzers is highly
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for third-party components of this work must be honored.      effective, a result also confirmed by other studies (e.g., [8]).
                                         For all other uses, contact the owner/author(s).                                               Symbolic Execution (SE) builds on the principle of declaring
                                         ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                    some (or all) inputs to a program to be symbolic. While concrete
                                         © 2023 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-0327-0/23/12.                                                           execution maintains states mapping variables to values, SE uses
                                         https://doi.org/10.1145/3611643.3616290                                                     symbolic states consisting of a path condition and a symbolic store.
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                                    Arthur Correnson and Dominic Steinhöfel


At branching points such as the if statement from above, SE gener-            Contrary, building a T-sound and T-complete symbolic executor
ates multiple successor states distinguished by different constraints     is possible. In this paper, we propose a general approach to build-
added to their path condition. As usual, assignments update the           ing provably sound and complete bug finders based on symbolic
symbolic store, which can map to symbolic values. SE was con-             execution. We implemented a prototypical bug finder based on this
ceived almost simultaneously as a bug finding [23] and program            approach in the Coq proof assistant together with an end-to-end
proving technique [10] and is still actively used in both areas. It is    proof of its correctness. To the best of our knowledge, ours is the
more popular in testing, though, due to its precise nature: Under         first endeavor to explicitly specify the meaning of correctness in the
ideal assumptions, SE yields no false positives and can be used in        context of symbolic bug finders in a proof assistant and to use formal
automated testing campaigns; on the other hand, program proving           verification techniques to prove the correctness of a bug finder.
with SE requires expensive auxiliary specifications [4].
                                                                             Research Questions. Precisely, we answer the following main
   So, what are these “ideal assumptions?” First, SE is a whitebox
                                                                          questions: (1) What constitutes a reliable testing tool?, and (2) How
technique: It requires access to the source code of the tested pro-
                                                                          can we engineer such a tool? These questions cannot be answered
gram, interpreting its structure to drive the search for bugs. While
                                                                          experimentally. Following the terminology of Shaw [30], they be-
this permits better results, implementing a symbolic executor re-
                                                                          long to the categories “Method for Evaluation” (Question (1)) and
quires a precise understanding of the semantics of the targeted
                                                                          “Method/Means of Development” (Question (2)) of software en-
language. For example, a symbolic executor for Python programs
                                                                          gineering research questions. Our answer to Question (1) is the
must respect Python’s integer floor division semantics: The division
                                                                          precise definition of T-soundness and T-completeness. Addressing
expression x // y corresponds to floor(x / y), where “/” is
                                                                          Question (2), we explain the characteristics of a T-sound and T-
division on reals. Other interpretations can result in false positives
                                                                          complete bug finder and expound a methodology to implement
(spurious bugs) or false negative (missed bugs). In the program
                                                                          such a tool. Following this methodology, we implemented SE-based
                     if x // y == -2: fail()
                                                                          testing tools in Coq and Python. For the Coq prototype, we derived
a wrong interpretation of integer division might lead a symbolic
                                                                          a formal, mechanized correctness proof.
bug finder to believe that 𝑥 = −5, 𝑦 = 2 triggers fail(). However,
in Python, the result of -5 // 2 is −3, while in other languages             Related Work. Kapus and Cadar [21] combine compiler testing
such as Java it evaluates to −2.                                          techniques and different oracles to test three symbolic bug finders.
   Second, SE discards unreachable erroneous states by checking           They reported 20 distinct bugs “exposing a variety of important
whether their path conditions are satisfiable. In our examples from       errors”—e.g., related to division. This is the only work on the cor-
above, it must decide if “x == hash((y, z))” or “x // y == -2”            rectness of (symbolic) bug finders (Question (1)) we are aware of.
are consistent with the previously collected constraints. To that         Other work mainly studies how SE can be applied for automated
end, the SE engines use constraint solvers to determine whether           testing. The strongest oracle used by Kapus and Cadar, the “output
a set of constraints is satisfiable (SAT ) or unsatisfiable (UNSAT ).     oracle,” compares the results of a concrete execution and a symbolic
However, instead of returning SAT or UNSAT, solvers frequently            one following the same path. This oracle only works if the initial
time out providing no answers; in that case, blindly reporting a bug      path condition uniquely describes the inputs used for concrete
could result in a false positive.                                         execution, but is, at the same time, “obfuscated” to prevent the ex-
   Consequently, an SE engine is more difficult to implement cor-         ecutor from dropping to “concrete mode.” When testing SE engines
rectly than a fuzzer. While the semantics and correctness of SE have      with less constrained inputs, such that multiple paths are explored,
been studied in different contexts [12, 24, 27, 32], the correctness      Kapus and Cadar use coarser oracles. In contrast, we developed a
of symbolic bug finders remains an open research topic. In particu-       verified symbolic bug finder based on carefully designed semantic
lar, to our knowledge, there exists no rigorous definition of what        foundations in response to Question (2). Likely, Kapus and Cadar
constitutes a trustworthy symbolic bug finder.                            would have found more bugs when investing even more work on
   The main correctness criterion for testing tools is the “soundness     test cases and oracles; our bug finder is guaranteed to be bug-free.
of bugs” [17]: If the tool answers Is there a bug in my program? with        In formal program verification, it is much more common to ad-
yes, there must exist a bug witness (an actionable input). We call        dress the soundness of verification tools and their underlying theo-
this property soundness for testing (T-soundness). Fuzz testers (short    retical underpinnings. The goal of formal verification is not to show
fuzzers) generate inputs that they feed to the program under test         the presence but prove the absence of bugs. Consequently, the main
and report a bug if the program crashes. Such tools are T-sound by        correctness criterion is the soundness of proofs (P-soundness): If a
construction. However, T-soundness alone is an insufficient quality       verifier answers Is my program safe to execute? with yes, then there
measure for bug finders. Indeed, a tester never reporting any bug is      exists a proof of the program’s correctness. As with T-completeness,
trivially T-sound. Thus, the converse of soundness is an additionally     P-completeness is the converse of P-soundness. Since checking a
desirable property: If a bug witness exists, a tester should eventually   complex program proof is arguably more complex then checking
answer the question Is there a bug in my program? with yes. This          whether an input causes a bug, the formal verification community
property, which we name completeness for testing (T-completeness),        put significant effort into justifying their tools and foundations.
is generally out of reach for fuzzers. The best option is to estimate     For example, Abstract Interpretation (AI) [11] is a mathematical
the residual risk that an ongoing fuzzing campaign would discover         framework for designing and implementing correct static analy-
an error if it only ran for a bit longer [7].                             sis. Following the AI framework, Jourdan et al. [20] proved the
                                                                          soundness of an abstract interpreter for C programs in the Coq
                                                                          proof assistant. This project is strongly related to the development
Engineering a Formally Verified Automated Bug Finder                                             ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA


of CompCert [25], a C compiler also proven correct in Coq. Coq               Statements        stmt      F      skip
itself is based on an established meta logic; its kernel was proven                                      |      fail
correct [31].                                                                                            |      VAR = aexpr
   Closing the circle to symbolic execution, there have been various                                     |      stmt ; stmt
efforts to show P-soundness of SE-based verifiers [1, 22, 33]. Further-                                  |      while bexpr do stmt od
more, the semantics of SE was addressed in the past [12, 24, 27, 32]                                     |      if bexpr then stmt else stmt fi
in a more general context. The symbolic semantics used in this
paper is inspired by the semantics proposed by de Boer and Bon-              Expressions       bexpr     F      true | false
sangue [12]. Building on these foundations, we define soundness                                          |      bexpr ( and | or ) bexpr
and completeness in the context of symbolic bug finding and pro-                                         |      not bexpr
vide a formally verified implementation.                                                                 |      aexpr ( == | <= | < | >= | > ) aexpr

                                                                                               aexpr     F      INT | VAR
    Contributions. Following the CompCert approach [5, 28] to build                                      |      aexpr ( + | - ) aexpr
verified program analyzers in a proof assistant, we develop a proto-
type of a formally verified symbolic bug finder in Coq. We formalize
the concrete operational semantics of a small imperative program-                                 Figure 1: Syntax of IMP
ming language and derive a symbolic operational semantics inspired
by de Boer and Bonsangue [12] (Sect. 1). Then, we extensively ex-          1.1     A Small Imperative Programming Language
plore the relations between concrete and symbolic semantics by
                                                                           IMP is an imperative programming language with assignments,
proving that SE is a sound and complete method for reachability
                                                                           while loops, and conditionals. Figure 1 contains a grammar of IMP’s
analysis and various bug-finding tasks (Sect. 2). Building on these
                                                                           concrete syntax; VAR denotes a variable identifier and INT an inte-
theoretical results, we derive a T-sound and T-complete symbolic
                                                                           ger. We integrate a fail statement signaling an error. Using fail,
bug finder (Sect. 3). In the course of this, we formally address several
                                                                           one can instrument source code to, e.g., mark supposedly unreach-
practical questions such as path selection and search space prun-
                                                                           able sections or model run-time assertions. IMP does not natively
ing using constraint solvers and their influence on exhaustiveness
                                                                           support multiplication and division; these operators can be imple-
(i.e., T-completeness) and precision (i.e., T-soundness) of SE. All
                                                                           mented in terms of addition and subtraction.
implementations, definitions, theorems, and proofs in this paper
are realized in Coq. Thus, if our specifications convince you, you
can blindly trust the proofs. We call our prototypical symbolic bug                          ⟨𝑉 , 𝑥 = 𝑒⟩ → ⟨𝑉 [𝑥 := ⟦𝑒⟧𝑉 ], skip⟩
finder WiSE (“What is Symbolic Execution”). To demonstrate the
practicability of our SE engine’s design principles, we (1) extract                                        ⟦𝑏⟧𝑉 = true
an executable OCaml implementation fully automatically from the                            ⟨𝑉 , if 𝑏 then 𝑠 1 else 𝑠 2 fi⟩ → ⟨𝑉 , 𝑠 1 ⟩
Coq code and (2) manually transform WiSE to PyWiSE, a WiSE
implementation written in Python (Sect. 4). Both extracted bug                                            ⟦𝑏⟧𝑉 = false
finders can be invoked on the command line. To provide hands-on
                                                                                           ⟨𝑉 , if 𝑏 then 𝑠 1 else 𝑠 2 fi⟩ → ⟨𝑉 , 𝑠 2 ⟩
evidence that WiSE works—additionally to our formal proofs—we
apply it to find bugs inserted into numeric algorithms.
                                                                                                        ⟨𝑉1, 𝑠 1 ⟩ → ⟨𝑉2, 𝑠 2 ⟩
                                                                                                  ⟨𝑉1, 𝑠 1 ; 𝑠 3 ⟩ → ⟨𝑉2, 𝑠 2 ; 𝑠 3 ⟩
1    CONCRETE AND SYMBOLIC SEMANTICS
We study symbolic execution along the example of IMP, a small                                         ⟨𝑉 , skip ; 𝑠⟩ → ⟨𝑉 , 𝑠⟩
imperative programming language with loops and integer arith-
metic. In this section, we introduce the IMP language (Sect. 1.1)                                          ⟦𝑏⟧𝑉 = true
and describe its operational semantics (Sect. 1.2). Afterward, we                    ⟨𝑉 , while 𝑏 do 𝑠 od⟩ → ⟨𝑉 , 𝑠 ; while 𝑏 do 𝑠 od⟩
equip IMP with a symbolic operational semantics following de Boer
and Bonsangue [12] (Sect. 1.3). The symbolic semantics will be the                                        ⟦𝑏⟧𝑉 = false
formal basis to justify the correctness of our SE engine.                                     ⟨𝑉 , while 𝑏 do 𝑠 od⟩ → ⟨𝑉 , skip⟩

   Notation. We use the following notational conventions to clarify                                 ⟦𝑥⟧𝑉 := 𝑉 (𝑥), 𝑥 ∈ Vars
the domains of identifiers in our formalizations.
                                                                                         ⟦true⟧𝑉 := true             ⟦false⟧𝑉 := false
     • 𝑝, 𝑞, . . . for programs                                            ⟦𝑒 1 + 𝑒 2 ⟧𝑉 := ⟦𝑒 1 ⟧𝑉 + ⟦𝑒 2 ⟧𝑉       ⟦𝑏 1 and 𝑏 2 ⟧𝑉 := ⟦𝑏 1 ⟧𝑉 ∧ ⟦𝑏 2 ⟧𝑉
     • 𝑉 for concrete environments, 𝑆 for symbolic stores
                                                                                                                 ...
     • 𝜑 for path conditions or LTL formulas
     • 𝜎 for concrete states ⟨𝑉 , 𝑝⟩, 𝜎ˆ for symbolic states ⟨𝜑, 𝑆, 𝑝⟩
     • 𝛼 for streams (e.g., of symbolic states)                                         Figure 2: Operational Semantics of IMP
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                                    Arthur Correnson and Dominic Steinhöfel



              ⟨𝜑, 𝑆, 𝑥 = 𝑒⟩ →sym ⟨𝜑, 𝑆 [𝑥 := ⟦𝑒⟧𝑆 ], skip⟩               about the program inputs. We write ⟨true, 𝑖𝑑, 𝑝⟩ →∗sym ⟨𝜑, 𝑆, 𝑝 ′ ⟩ to
                                                                         denote that the symbolic state ⟨𝜑, 𝑆, 𝑝 ′ ⟩ can be reached by symbolic
      ⟨𝜑, 𝑆, if 𝑏 then 𝑠 1 else 𝑠 2 fi⟩ →sym ⟨𝜑 and ⟦𝑏⟧𝑆 , 𝑆, 𝑠 1 ⟩      execution of 𝑝. Figure 4 shows a symbolic execution tree for the
                                                                         execution of a conditional statement in the default initial state.
  ⟨𝜑, 𝑆, if 𝑏 then 𝑠 1 else 𝑠 2 fi⟩ →sym ⟨𝜑 and (not ⟦𝑏⟧𝑆 ), 𝑆, 𝑠 2 ⟩
                                                                               ⟨true, 𝑥 ↦→ 𝑥, if x < 0 then fail else x = x - 1 fi⟩
                         ⟨𝜑 1, 𝑆 1, 𝑠 1 ⟩ → ⟨𝜑 2, 𝑆 2, 𝑠 2 ⟩                                  sym                    sym

                 ⟨𝜑 1, 𝑆 1, 𝑠 1 ; 𝑠 3 ⟩ →sym ⟨𝜑 2, 𝑆 2, 𝑠 2 ; 𝑠 3 ⟩             ⟨x < 0, 𝑥 ↦→ 𝑥, fail⟩          ⟨x >= 0, 𝑥 ↦→ 𝑥, x = x - 1⟩
                                                                                                                              sym
                     ⟨𝜑, 𝑆, skip ; 𝑠⟩ →sym ⟨𝜑, 𝑆, 𝑠⟩
                                                                                                               ⟨x >= 0, 𝑥 ↦→ 𝑥 − 1, skip⟩
⟨𝜑, 𝑆, while 𝑏 do 𝑠 od⟩ →sym ⟨𝜑 and ⟦𝑏⟧𝑆 , 𝑆, 𝑠 ; while 𝑏 do 𝑠 od⟩
                                                                                  Figure 4: Example Symbolic Execution Tree
      ⟨𝜑, 𝑆, while 𝑏 do 𝑠 od⟩ →sym ⟨𝜑 and (not ⟦𝑏⟧𝑆 ), 𝑆, skip⟩

               Figure 3: Symbolic Semantics of IMP
                                                                         2     FINDING BUGS SYMBOLICALLY
                                                                         A symbolic executor simulates many concrete executions of a pro-
                                                                         gram simultaneously. From this, we can obtain a bug finder by
1.2     Concrete Operational Semantics                                   reporting an error whenever one simulated execution reaches an er-
IMP programs are executed in an environment 𝑉 : Vars → Z repre-          ror state. Every reported bug must come with an witness. In fuzzing,
senting the values assigned to each program variable. Execution          this is a bug-triggering input; in the case of SE, it is frequently a
states are pairs ⟨𝑉 , 𝑝⟩ of an environment and a program that re-        more abstract witness in the form of a boolean formula describing
mains to be executed. The small-step operational semantics for IMP       all inputs triggering the bug. Additionally, we would like to ensure
(Fig. 2) is a relation between execution states. We use the notation     that any bug in the program will eventually be detected during SE.
⟨𝑉 , 𝑝⟩ → ⟨𝑉 ′, 𝑝 ′ ⟩ to state that executing program 𝑝 in environ-      In this section, formally connect bug finding and symbolic execu-
ment 𝑉 for one step produces a new environment 𝑉 ′ together with         tion. In particular, we lift the symbolic semantics from Sect. 1.3 to
a program 𝑝 ′ that remains to be executed. The relation “→∗ ” is         a sound and complete method to find bugs.
the reflexive, transitive closure of “→.” We use the notation ⟦𝑒⟧𝑉
to denote the value of the expression 𝑒 in environment 𝑉 . The           2.1    Sound & Complete Reachability
operational semantics is presented in Fig. 2.                            Our first step toward a symbolic bug finder is to connect symbolic
                                                                         and concrete executions. The glue we use to establish this connec-
1.3     Symbolic Operational Semantics                                   tion is reachability. A correct symbolic executor should only reach
Informally, a program is symbolically executed by using symbolic         symbolic states representing reachable concrete states. Conversely,
placeholders instead of concrete values as inputs. When a statement      we would like it to reach any reachable concrete state in the form
with different possible outcomes is reached (in IMP, this can be         of a symbolic state representing it.
an if statement or a loop), both possibilities are independently            We write Reach(𝑝, 𝜎) and Reachsym (𝑝, 𝜎) to express that con-
explored in different execution branches. Symbolic execution thus        crete state 𝜎 can be reached by concrete and symbolic execution
produces in a tree representing all possible execution paths. Each       of the program 𝑝. Then, we express soundness and completeness
tree node is labeled with a formula (called the path condition), which   concerning reachability as a simple equivalence:
characterizes the condition on the program inputs that needs to be       Theorem 2.1 (Soundness and Completeness for Reachability).
met for the program to reach the associated state.                         Reachsym (𝑝, 𝜎) ⇔ Reach(𝑝, 𝜎)
   More formally, we regard SE as a type of program execution
respecting a symbolic operational semantics “→sym ” (Fig. 3). In SE,       Reach(𝑝, 𝜎) can be expressed using the concrete operational se-
symbolic stores 𝑆 : Vars → expr take the role of environments.           mantics. A state 𝜎 is reachable for a program 𝑝 if executing 𝑝 in
Contrary to the latter, symbolic stores map variables to symbolic        some initial store 𝑉0 eventually leads to 𝜎.
expressions and not numeric values. The dual to concrete execution       Definition 2.1 (Concrete Reachability).
states are symbolic states, triples ⟨𝜑, 𝑆, 𝑝⟩ of a formula 𝜑 (the path     Reach(𝑝, 𝜎) ≜ ∃𝑉0, ⟨𝑉0, 𝑝⟩ →∗ 𝜎
condition), a symbolic store 𝑆, and a program to be executed 𝑝 (the
                                                                            Symbolic states reached during SE represent many concrete
program counter). We extend the concrete evaluation of an expres-
                                                                         states. To make Reachsym (𝑝, 𝜎) precise, we relate them to their
sion 𝑒 in a store 𝑉 to a symbolic evaluation ⟦𝑒⟧𝑆 . The result of ⟦𝑒⟧𝑆
                                                                         “concretizations.” The concretization operation ◦ turns a symbolic
is again a symbolic expression obtained by replacing variables in 𝑒
                                                                         store 𝑆 into a concrete store 𝑉 ′ = 𝑉 ◦𝑆 by replacing all free variables
with their associated expressions in 𝑆, if any.
                                                                         in 𝑆 by their associated values in 𝑉 . For example, if 𝑆 = {𝑥 ↦→ 𝑦, 𝑦 ↦→
   The symbolic execution of a program 𝑝 usually starts in the initial
                                                                         𝑦} and 𝑉 = {𝑥 ↦→ 1, 𝑦 ↦→ 2}, we obtain 𝑉 ′ = {𝑥 ↦→ 2, 𝑦 ↦→ 2}.
state ⟨true, 𝑖𝑑, 𝑝⟩, where 𝑖𝑑 := 𝑥 ↦→ 𝑥 is an “empty” symbolic store
assigning to each program variable a symbol of the same name. The        Definition 2.2.
initial path condition true indicates that we make no assumptions          (𝑉 ◦ 𝑆)(𝑥) := ⟦𝑆 (𝑥)⟧𝑉
Engineering a Formally Verified Automated Bug Finder                                               ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA


   We lift the store concretization “◦” to the concretization of sym-         Proof. By immediate application of Lemma 2.4 and the fact that
bolic states. To express that a symbolic state 𝜎ˆ represents a concrete       ⟨𝑉0, 𝑝⟩ ≃𝑉0 ⟨true, 𝑖𝑑, 𝑝⟩.                                  □
state 𝜎 via an initial store 𝑉0 , we write 𝜎 ≃𝑉0 𝜎. ˆ Any concretiza-
tion 𝜎 of 𝜎ˆ must have the same program counter as 𝜎. Furthermore,
the initial store 𝑉0 must satisfy the path condition of 𝜎.
                                                         ˆ Finally, 𝜎’s                            PROOF OF COMPLETENESS
environment must be a concretization of 𝜎’s  ˆ store via 𝑉0 .
                                                                              We address the converse direction: All concretely reachable states
Definition 2.3.                                                               are symbolically reachable. The idea is to show that for any exe-
  ⟨𝑉 , 𝑝⟩ ≃𝑉0 ⟨𝜑, 𝑆, 𝑝 ′ ⟩ ≜ 𝑝 = 𝑝 ′ ∧ 𝑉 = 𝑉0 ◦ 𝑆 ∧ ⟦𝜑⟧𝑉0 = true              cution step that can be taken according to the concrete semantics,
                                                                              there exists a symbolic step to simulate it.
   Now, all concretizations of reachable symbolic states are symboli-
cally reachable. Formally:                                                    Lemma 2.5.
                                                                                (𝜎 ≃𝑉0 𝜎ˆ ∧ 𝜎 → 𝜎 ′ ) ⇒ ∃𝜎ˆ ′, 𝜎ˆ →sym 𝜎ˆ ′ ∧ 𝜎 ′ ≃𝑉0 𝜎ˆ ′
Definition 2.4.
                          ˆ ⟨true, 𝑖𝑑, 𝑝⟩ →∗sym 𝜎ˆ ∧ 𝜎 ≃𝑉0 𝜎ˆ
  Reachsym (𝑝, 𝜎) ≜ ∃𝑉0, ∃𝜎,                                                  Proof. By induction on the derivation 𝜎 → 𝜎 ′ and selecting the
   In the remainder of this section, we describe the proofs of both           appropriate symbolic rule for each case.                      □
directions of Theorem 2.1 for the interested reader. Following the               We extend Lemma 2.5 to the reflexive transitive closure.
proofs, Sect. 2.2 addresses the detection of bugs, which involves
making precise what constitutes an “error state.”                             Lemma 2.6.
                                                                                (𝜎 ≃𝑉0 𝜎ˆ ∧ 𝜎 →∗ 𝜎 ′ ) ⇒ ∃𝜎ˆ ′, 𝜎ˆ →∗sym 𝜎ˆ ′ ∧ 𝜎 ′ ≃𝑉0 𝜎ˆ ′
                         PROOF OF SOUNDNESS
                                                                              Proof. By iterating Lemma 2.5.                                             □
Subsequently, we derive the proof of “sound reachability,” i.e., that
all states reachable by SE are also reachable by concretely exe-                 The completeness of Reachsym follows directly from Lemma 2.6.
cuting a program. This proof requires some intermediate lemmas.
Lemma 2.1 is a compositionality result on the interplay of con-               Theorem 2.3 (Complete Reachability).
cretization and symbolic store updates.                                         Reach(𝑝, 𝜎) ⇒ Reachsym (𝑝, 𝜎)

Lemma 2.1.                                                                    Proof. It is easy to see that ⟨𝑉0, 𝑝⟩ ≃𝑉0 ⟨true, 𝑖𝑑, 𝑝⟩. The result
  𝑉 ◦ (𝑆 [𝑥 := ⟦𝑒⟧𝑆 ]) = (𝑉 ◦ 𝑆) [𝑥 := ⟦𝑒⟧𝑉 ◦𝑆 ]                              immediately follows from this observation and Lemma 2.6.         □

Proof. By structural induction on 𝑒.                                     □    2.2    Sound & Complete Bug Finding
  During SE, path conditions get only ever more specific by accu-             In the previous section, we proved that the states reachable by SE
mulating addition constraints. This is asserted in Lemma 2.2. We              are the same as those reachable by concrete execution. Building on
note 𝜑 ⊨ 𝜑 ′ ≜ ∀𝑉 , ⟦𝜑⟧𝑉 = true ⇒ ⟦𝜑 ′ ⟧𝑉 = true.                             that, we establish that SE can also be used as a sound and complete
                                                                              bug-finding method. First, however, we must address the question
Lemma 2.2.                                                                    What does it mean to find bugs? We present different views on this
  ⟨𝜑, 𝑆, 𝑝⟩ →∗sym ⟨𝜑 ′, 𝑆 ′, 𝑝 ′ ⟩ ⇒ 𝜑 ′ ⊨ 𝜑                                  question and prove that SE answers each case.
Proof. By induction on the length of the →∗sym derivation and by                 Detecting Buggy Programs. A natural view on bug finding is to
induction on the last →sym step.                               □              ask—and answer—the question Does my program contain a bug?
                                                                              We introduce a relation HasBug(𝑝) characterizing buggy programs.
  Whenever the path condition after a symbolic step is satisfiable,
                                                                              This predicate is central to our definition of T-soundness and T-
we can make a corresponding concrete step.
                                                                              completeness (Sect. 3.5). A state 𝜎 = ⟨𝑉 , 𝑝⟩ “has a bug” if 𝑝 is
Lemma 2.3.                                                                    stuck, i.e., has no semantic successor state. However (in the case
  ⟨𝜑, 𝑆, 𝑝⟩ →sym ⟨𝜑 ′, 𝑆 ′, 𝑝 ′ ⟩ ∧ 𝑉 ⊨ 𝜑 ′ ⇒ ⟨𝑉 ◦ 𝑆, 𝑝⟩ → ⟨𝑉 ◦ 𝑆 ′, 𝑝 ′ ⟩    of IMP), this would also hold if 𝑝 was skip, although we were
                                                                              more thinking of fail. We explicitly exclude the skip case in the
Proof. By induction over the symbolic derivation and by compo-                following definitions of “not stuck” (i.e., “can progress”) and “stuck.”
sition (2.1) in the case of variable assignments 𝑥 = 𝑒.     □
                                                                              Definition 2.5 (Progress).
   We extend Lemma 2.3 to the transitive reflexive closure by ap-               Progress(⟨𝑉 , 𝑝⟩) ≜ 𝑝 = skip ∨ ∃𝜎, ⟨𝑉 , 𝑝⟩ → 𝜎
plying monotonicity (Lemma 2.2).
                                                                              Definition 2.6 (Stuck States).
Lemma 2.4.                                                                      Stuck(𝜎) ≜ ¬Progress(𝜎)
  ⟨𝜑, 𝑆, 𝑝⟩ →∗sym ⟨𝜑 ′, 𝑆 ′, 𝑝 ′ ⟩ ∧𝑉 ⊨ 𝜑 ′ ⇒ ⟨𝑉 ◦ 𝑆, 𝑝⟩ →∗ ⟨𝑉 ◦ 𝑆 ′, 𝑝 ′ ⟩
                                                                                 A buggy program has a reachable, stuck state.
Proof. By iterating Lemma 2.3 and by Lemma 2.2.                          □
                                                                              Definition 2.7 (Having a Bug).
   Sound reachability follows from the (more general) Lemma 2.4.                HasBug(𝑝) ≜ ∃𝜎, Reach(𝑝, 𝜎) ∧ Stuck(𝜎)
Theorem 2.2 (Sound Reachability).                                                As the question Does my program contain a bug? can be reduced
  Reachsym (𝑝, 𝜎) ⇒ Reach(𝑝, 𝜎)                                               to reachability, we can answer it symbolically.
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                                        Arthur Correnson and Dominic Steinhöfel


Definition 2.8.                                                            (Sect. 3.2). Third, we introduce “relative” notions of soundness and
  HasBugsym (𝑝) ≜ ∃𝜎, Reachsym (𝑝, 𝜎) ∧ Stuck(𝜎)                           completeness and relate them to the symbolic executor (Sect. 3.3)
                                                                           and bug finder (Sect. 3.4). Finally, we bridge the (already tiny) gap
   The equivalence of HasBugsym and HasBug follows immediately
                                                                           toward a T-sound and T-complete bug finder (Sect. 3.5).
from the equivalence of Reachsym and Reach.
Theorem 2.4 (Sound and Complete Bug Detection (1)).                        3.1     From the Symbolic Semantics to an
  HasBugsym (𝑝) ⇔ HasBug(𝑝)                                                        Executable Symbolic Executor
                                                                           Our symbolic operational semantics is a solid basis for symbolic bug
Proof. By soundness of Reachsym in the “⇒” direction and by
                                                                           finding. Yet, its design leaves some crucial questions open that need
completeness of Reachsym in the “⇐” direction.            □
                                                                           to be addressed when developing an executable SE-based testing
   Finding Erroneous Execution States. HasBug(𝑝) asserts that some         tool. These are: (1) The symbolic semantics is nondeterministic.
bug exists. Alternatively, we can specifically ask whether a given         Whenever an if or while statement is reached, SE can choose which
state is erroneous and whether SE can find it. The predicate IsBug(𝑝, 𝜎)   branch to execute next. (2) We need an effective way to detect error
asserts that 𝜎 is an error state of 𝑝. In Sect. 3.4, we derive a refined   states. The previously regarded predicates HasBugsym , IsBugsym ,
“relative” version of T-soundness and T-completeness for nontermi-         and BadInputsym are adequate formalizations for bug detection but
nating symbolic executors using IsBug(𝑝, 𝜎).                               are not executable because they live on the semantic level. Finally,
                                                                           (3) the symbolic semantics does not terminate for programs with
Definition 2.9.
                                                                           loops, which we cannot solve in general, but must face nonetheless.
  IsBug(𝑝, 𝜎) ≜ Reach(𝑝, 𝜎) ∧ Stuck(𝜎)
    Similarly to above, we derive a symbolic predicate IsBugsym (𝑝, 𝜎).                               HasBugsym (𝑝)
Theorem 2.5 (Sound and Complete Bug Detection (2)).                                                          ⇔
  IsBugsym (𝑝, 𝜎) ⇔ IsBug(𝑝, 𝜎)                                                               ∃𝜎, Reachsym (𝑝, 𝜎) ∧ Stuck(𝜎)
   Finding Erroneous Inputs. Our final view is to ask for “bad,” i.e.,                                       ⇔
bug-triggering, inputs. The predicate BadInput(𝑝, 𝑉0 ) characterizes                        ˆ ⟨true, 𝑖𝑑, 𝑝⟩ →∗sym 𝜎ˆ ∧ 𝜎 ≃𝑉0 𝜎)
                                                                                 ∃𝜎, (∃𝑉0, ∃𝜎,                               ˆ ∧ Stuck(𝜎)
those (where the environment 𝑉0 represents an input):
                                                                                                             ⇔
Definition 2.10.                                                                                      ∃𝑉0, ∃⟨𝜑, 𝑆, 𝑞⟩,
  BadInput(𝑝, 𝑉0 ) ≜ ∃𝜎, ⟨𝑉0, 𝑝⟩ →∗ 𝜎 ∧ Stuck(𝜎)
                                                                            ⟨true, 𝑖𝑑, 𝑝⟩ →∗sym ⟨𝜑, 𝑆, 𝑞⟩ ∧ ⟦𝜑⟧𝑉0 = true ∧ Stuck(⟨𝑉0 ◦ 𝑆, 𝑞⟩)
   The symbolic equivalent is more subtle since →∗sym ranges over
                                                                                                             ⇔
symbolic states. We must concretize the reached symbolic state
before checking whether it denotes a bug.                                              ∃⟨𝜑, 𝑆, 𝑞⟩, ⟨true, 𝑖𝑑, 𝑝⟩ →∗sym ⟨𝜑, 𝑆, 𝑞⟩          ∧
                                                                                                                                    (1)
Definition 2.11.
  BadInputsym (𝑝, 𝑉0 ) ≜ ∃𝜎∃𝜎,ˆ                                                       ∃𝑉0, ⟦𝜑⟧𝑉0 = true         ∧ Stuck(⟨𝑉0 ◦ 𝑆, 𝑞⟩)
                                                                                                          (2)                             (3)
     ⟨true, 𝑆, 𝑝⟩ →∗sym 𝜎ˆ ∧ 𝜎 ≃𝑉0 𝜎ˆ ∧ Stuck(𝜎)
  The equivalence of BadInputsym and BadInput follows from the             Figure 5: Decomposition of symbolic bug finding into checks
definition of Reachsym and the proof of Theorem 2.2 and Theo-              for (1) reachability, (2) satisfiability, and (3) “stuckness.”
rem 2.3.
Theorem 2.6 (Sound and Complete Bug Detection (3)).                           Resolving Nondeterminism. While in theory, we could spawn
  BadInputssym (𝑝, 𝑉0 ) ⇔ BadInputs(𝑝, 𝑉0 )                                independent processes whenever SE performs a case distinction
                                                                           when facing an if or while statement, this cannot continue forever.
   This view bridges the gap between SE and fuzzing: What is               The number of branches in a symbolic execution tree is exponential
needed to report a bug-triggering input is (1) a bug oracle (a symbolic    in the number of such branching points; eventually, we will have
equivalent of Stuck(𝜎)) and (2) a constraint solver extracting a           to decide which branches to follow first. This process is known
solution 𝑉0 from a path constraint. Subsequently, we describe how          as path selection in SE [3]. Usually, path selection is regarded as a
to build a testing tool based on our insights on SE, including a brief     “heuristics,” merely an artifact of efficiency considerations. However,
discussion of “crash oracles.” Constraint solving is not in our scope.     the exploration order has solid consequences on the T-completeness
                                                                           of the resulting bug finder. Early dynamic symbolic executors such
3    A TRUSTWORTHY SYMBOLIC BUG FINDER                                     as DART [18] explored programs using a Depth-First Search (DFS).
Section 2 demonstrated the feasibility of finding bugs with SE based       This approach is incomplete in general: Such executors likely get
on the symbolic operational semantics. Now, we turn these insights         lost in ever deeper iterations of loops at the beginning of a program,
into an executable correct symbolic bug finder. First, we discuss          neglecting any states that follow. Instead, we choose a Breadth-
how to detect errors, resolve the nondeterminism of the symbolic           First Search (BFS) approach. In Sect. 3.3, we prove the completeness
semantics, and deal with diverging executions (Sect. 3.1). Second,         of BFS-based path selection, which requires estimating where a
we provide relevant implementation details of our WiSE prototype           successor state is added in the stream of states to explore.
Engineering a Formally Verified Automated Bug Finder                                        ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA


   Detecting Errors. Any bug finder depends on a bug oracle to
                                                                         let run 𝑙 =
determine when a program state constitutes a bug. Predicates such
                                                                           match 𝑙 with
as HasBugsym are non-executable semantic notions. Moreover, they
                                                                           | [] ->
are defined using symbolic reachability, which requires checking
                                                                             yield None
if a path condition is satisfiable (see Fig. 5). Fuzzers commonly
                                                                             run []
classify program runs as erroneous if they end with a crash of the
                                                                           | ⟨𝜑, 𝑆, 𝑝⟩::𝑙 ->
program. We use a similar approach: We classify a program as
                                                                             yield ⟨𝜑, 𝑆, 𝑝⟩
buggy or crashing if it is stuck. In our case, it can be shown that
                                                                             run (𝑙 + expand ⟨𝜑, 𝑆, 𝑝⟩)
a state is stuck if and only the next statement to be executed is
fail. This simple solution is already quite powerful. For example,
to extend IMP with failing expressions, one can use fail to model           Figure 6: Main Entry Point of the Symbolic Executor
the exceptional cases. Consider integer division: For any expression
x / y, we add a preceding statement if y == 0 then fail else
d = div(x,y), replacing x / y with the fresh variable d. The             let expand ⟨𝜑, 𝑆, 𝑝⟩ =
function div would implement division using repeated subtraction,          match 𝑝 with
assuming that y is nonzero.                                                | skip | fail -> [ ]
                                                                           | skip ; c ->
    Addressing Termination. As a method simulating concrete execu-
                                                                             [ ⟨𝜑, 𝑆, 𝑐⟩ ]
tions, SE does not terminate for most looping or recursive programs.
                                                                           | x = e ->
Derivations in our symbolic semantics (Fig. 3) are infinite for any
                                                                             [ ⟨𝜑, 𝑆 [x := ⟦𝑒⟧𝑆 ], skip⟩ ]
program with a loop. In Sect. 3.5, we integrate pruning of unsat-
                                                                           | 𝑐 1 ; 𝑐 2 ->
isfiable states, which solves that issue for loops with concrete or
                                                                             [ ⟨𝜑 ′, 𝑆 ′, 𝑐 1 ; 𝑐 2 ⟩ for ⟨𝜑 ′, 𝑆 ′, 𝑐 1 ⟩ in expand 𝑐 1 ]
unsatisfiable guards. Even so, loops with underconstrained symbolic
                                                                           | while cond do c od ->
guards induce an infinite amount of reachable successor states.
                                                                             [ ⟨𝜑 and cond, 𝑆, 𝑐 ; 𝑝⟩, ⟨𝜑 and (and cond), 𝑆, skip⟩ ]
    There are two main options for dealing with nontermination in
                                                                           | if 𝑐𝑜𝑛𝑑 then 𝑐 1 else 𝑐 2 fi ->
SE. The first option is to impose an upper bound on the number of
                                                                             [ ⟨𝜑 and 𝑐𝑜𝑛𝑑, 𝑆, 𝑐 1 ⟩, ⟨𝜑 and (not 𝑐𝑜𝑛𝑑), 𝑆, 𝑐 2 ⟩ ]
times a loop is unwound. This approach has the advantage that it is
easy to implement. However, it prevents us from reasoning about
the T-completeness of a symbolic executor, since the chosen bound            Figure 7: Computing Successors of Symbolic States
might be too small to detect sufficiently deep bugs. The approach we
chose instead is to implement the symbolic executor as a generator
of an infinite stream of states. A user of a stream-based executor      this syntax to, e.g., Python. Everything discussed in this section is
can only ever inspect finitely many states from the stream, which       implemented in Coq, proven correct, and automatically extracted
corresponds to bounded execution; yet, we can obtain a completeness     to an executable OCaml executable version.
result. Our OCaml and Python implementations (Sect. 4) retrieve
elements from the stream up to a user-specified bound.                     Symbolic Evaluator and Symbolic Stores. Implementing a sym-
    Thus, we view automated bug finders as producers of lazily          bolic executor requires an efficient implementation of symbolic
evaluated infinite sequences of status messages reporting on the        stores and a function to evaluate symbolic expressions. One way
progress of the bug finding process. There are various ways of          to implement symbolic stores is using hash tables with variable
implementing infinite streams depending on the capabilities of the      names as keys and expressions as values. Updating a store 𝑆 with
programming language a symbolic executor is implemented in. In          an assignment 𝑥 B 𝑒, written 𝑆 [𝑥 B 𝑒], returns an updated copy
proof systems based on purely functional languages such as Coq,         of the hash table. The symbolic evaluation ⟦𝑒⟧𝑆 of an expression
infinite sequences can be modeled by co-induction [15, 16]. In lan-     𝑒 in a store 𝑆 can be performed by a simple recursive function.
guages with lazy evaluation such as Haskell, such infinite sequences    We abstract from these implementation details and use the math-
can be implemented using standard lists. In the case of eagerly eval-   ematical notations 𝑆 [𝑥 := 𝑒] and ⟦𝑒⟧𝑆 in code snippets to denote
uated functional languages such as OCaml, the implementation            assignments and symbolic evaluations.
can resort to explicit suspensions. Otherwise, we can model streams        A Lazy Symbolic Executor. The main component of the symbolic
with generators à la Python.                                            executor is a function expand (Fig. 7) computing the successors of a
    In Sect. 3.3, we show that the stream-based approach permits        symbolic state, implementing the symbolic semantics in Fig. 3. The
elegant specifications of correctness based on temporal logic.          executor’s entry point is a function run (Fig. 6) taking a FIFO queue
                                                                        of symbolic states and returning a stream of (optional) reachable
3.2     Functional Implementation                                       symbolic states. At every iteration, it yields the first state from the
After many dry discussions, we provide some implementation              queue. Then, the direct successors of the current state are computed
details of our proven-correct symbolic executor. As discussed in        using expand and enqueued in the task queue (with the lowest
Sect. 3.1, the executor uses a breadth-first goal selection and pro-    priority, realizing a breadth-first search). Finally, run calls itself
duces a “lazy” infinite stream of status messages. We use an OCaml-     recursively on the updated queue. If the queue is empty, a None
flavored syntax in all code snippets; we found it easy to translate     token is yielded indicating that no states are left for expansion.
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                                     Arthur Correnson and Dominic Steinhöfel


                                                                        time provided to the bug finder. Moreover, relative completeness
 let display state =
                                                                        is parametric in a concrete bug-triggering input. Though formally
   if state is None then
                                                                        weaker than T-completeness due to the additional precondition,
     Finished
                                                                        it provides the strong guarantee a specific bug will be found, not
   else if is_stuck state then
                                                                        just any bug. In the context of SE, relative soundness additionally
     BugFound(state)
                                                                        permits conveying false positives with unsatisfiable path constraints;
   else
                                                                        excluding these requires a complete constraint solver that correctly
     Pending
                                                                        classifies all unsatisfiable path conditions. Provided such a solver, it
                                                                        is an easy exercise to construct a T-sound and T-complete bug finder
 let bug_finder 𝑝 =
                                                                        from a relatively sound/complete one, as described in Sect. 3.5.
     map display (run [ ⟨true, 𝑖𝑑, 𝑝⟩ ])
                                                                            In this section, we investigate SE-specific notions of relative
                                                                        soundness and completeness, asserting that a symbolic executor
Figure 8: Status Message Conversion, Bug Finder Entry Point             explores only reachable symbolic states (soundness) and all reach-
                                                                        able states (completeness). The subsequent Sect. 3.4 formalizes the
                                                                        more general notions of relative soundness and completeness and
 let is_stuck ⟨𝜑, 𝑆, 𝑝⟩ =                                               applies the results from this section to prove that the bug finder
   match 𝑝 with                                                         from Sect. 3.2 satisfies these properties.
   | fail -> True                                                           To conveniently express predicates over streams of symbolic
   | 𝑝 ; _ -> is_stuck 𝑝                                                states or status messages, we use Linear Temporal Logic (LTL) [2,
   | _ -> False                                                         Chapter 5] notation. LTL formulas describe infinite streams of
                                                                        elements of some carrier set 𝐴. Atomic LTL formulas are predicates
                                                                        over 𝐴-elements, or, equivalently, subsets of 𝐴. For example, the
                 Figure 9: Classifying Error States                     LTL formula 𝑃 = {𝑛 | ∃𝑚, 2 · 𝑚 = 𝑛} is satisfied by the stream
                                                                        4, 5, 6, . . . since its first element is even. The formula □𝑃 (“globally”)
                                                                        describes streams in which all elements are even; ♢𝑃 (“eventually”)
   Reporting Bugs. The function run implements a symbolic execu-        matches streams with some even number. The property □♢𝑃 holds
tor. We obtain a bug finder by turning symbolic states from the         for streams with infinitely many even numbers (“every position in
stream into adequate status messages:                                   the stream must eventually be succeeded by an even number”). In
   (1) BugFound(⟨𝜑, 𝑉 , 𝑝⟩) informs the user that a bug has been        addition to “□” and “♢,” we use logical implication “→.” For example,
       detected and returns the associated symbolic state.              {42}→(♢{0, 1}) means that any stream whose first element is 42
   (2) Pending informs the user that the SE is in progress.             must contain either 0 or 1 at a later position.
   (3) Finished informs the user that the SE terminated. No fur-            We write 𝛼 ⊨ 𝜑 if the stream 𝛼 = 𝛼 0, 𝛼 1, . . . satisfies the LTL
       ther symbolic state will be discovered.                          formula 𝜑; 𝛼 ⊭ 𝜑 means that 𝛼 does not satisfy 𝜑. Formally, the
   The conversion from symbolic states to status messages is ac-        semantics of LTL formulas is inductively defined as follows:
complished by the function display (Fig. 8). The final bug finder                        𝛼 ⊨𝑃          ⇔ 𝑃 (𝛼 0 )
(bug_finder in Fig. 8) starts SE with a singleton task queue consist-
                                                                                         𝛼 ⊨ □𝜑        ⇔ ∀𝑖 ≥ 0, 𝛼𝑖 𝛼𝑖+1 ... ⊨ 𝜑
ing of an initial symbolic state and applies display on the results.
                                                                                         𝛼 ⊨ ♢𝜑        ⇔ ∃𝑖 ≥ 0, 𝛼𝑖 𝛼𝑖+1 ... ⊨ 𝜑
    Detecting Bugs. The function display uses is_stuck (Fig. 9) to
                                                                                         𝛼 ⊨ 𝜑 1 →𝜑 2 ⇔ 𝛼 ⊭ 𝜑 1 or 𝛼 ⊨ 𝜑 2
filter error states. As discussed in Sect. 2.2, is_stuck considers a
symbolic state ⟨𝜑, 𝑆, 𝑝⟩ an error state if 𝑝 starts with fail.              Our symbolic executor produces a stream of optional (possibly
                                                                        None) symbolic states from a list 𝑙 of input states. To be sound, every
3.3     Relative Soundness and Completeness of                          symbolic state in the stream must be reachable from some state in
        the Symbolic Executor                                           𝑙. The LTL formula ReachableFrom(𝑙) asserts that the first element
                                                                        in a stream is None or a symbolic state reachable from a state in 𝑙.
T-soundness and T-completeness are expressed assuming a “yes/no”
oracle. For example, a T-sound bug finder only responds with yes        Definition 3.1 (Reachable From).
to Is there a bug in my program? if there is a bug that manifests         ReachableFrom(𝑙) := {𝜎ˆ ′ | ∃𝜎ˆ ∈ 𝑙, 𝜎ˆ →∗sym 𝜎ˆ ′ } ∨ {None}
for a concrete input. However, fuzzers and symbolic bug finders
                                                                          Our bug finder’s soundness depends on the single-step execution
generally do not terminate unless interrupted, as in the case of
                                                                        function expand correctly implementing the relation →sym :
our symbolic bug finder from the previous section. Thus, we adapt
these notions to testers producing a stream of results. We call the     Theorem 3.1 (Correct expansion).
resulting concepts relative soundness/completeness. They address          𝜎ˆ →sym 𝜎ˆ ′ ⇔ 𝜎ˆ ′ ∈ expand(𝜎)
                                                                                                       ˆ
the question of whether an input in a stream exposes a bug.
                                                                        Proof. By induction on (1) the →sym -derivation (direction “⇒”)
   More precisely, a bug finder is relatively sound if any bug report
                                                                                                 ˆ program counter (“⇐”).
                                                                        and (2) the structure of 𝜎’s                                 □
in the generated stream corresponds to bug-exposing input(s). It is
relatively complete if it will eventually report a bug for any given       Now we can state the relative soundness theorem, whose proof
bug-triggering input. In other words, both terms are relative to the    follows directly from Theorem 3.1:
Engineering a Formally Verified Automated Bug Finder                                              ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA


Theorem 3.2 (Relative Soundness of Symbolic Execution).                           According to this definition, a bug report is always valid for
  run(𝑙) ⊨ □ReachableFrom(𝑙)                                                  symbolic states with unsatisfiable path conditions since these have
                                                                              an empty Concrete(𝜎). ˆ How to get from there to real T-soundness
   By outputting a None value in the stream, run signals that all
                                                                              is the focus of Sect. 3.5. The definition of relative soundness is easy:
reachable states have been exhaustively explored. Consequently,
                                                                              A relatively sound bug finder only outputs valid status messages.
the stream should only consist of None after the first issued one,
guaranteeing that we can safely terminate SE after the first None.            Theorem 3.5 (Relatively Sound Bug Discovery).
                                                                                find_bugs(𝑝) ⊨ □ValidStatus(𝑝)
Theorem 3.3 (Sound Termination of Symbolic Execution).
  run(𝑙) ⊨ □(None → □None)                                                    Proof. Direct application of Lemma 3.1, and the fact that display
   We consider the symbolic executor relatively complete if, for any          filters only stuck states.                                      □
                        ˆ it generates at least all →∗sym -successors
initial symbolic state 𝜎,                                                        Completeness. Relative completeness means that any given bug
of 𝜎ˆ when started on the list [𝜎].ˆ We first state a more general            will eventually be reported in the stream of status messages. As
theorem (Lemma 3.1) from which we then conclude the relative                  mentioned before, this property is both weaker—due to the precon-
soundness. Lemma 3.1 asserts that for any state 𝜎ˆ discovered during          dition of providing a concrete bug-triggering input—and stronger—
SE, its (direct or indirect) successors will eventually be found. Its         since it guarantees that a pre-chosen bug will be found—than T-
proof requires us to predict when exactly the direct successors of            completeness. The subsequent completeness theorem uses a func-
any state 𝜎ˆ will be discovered by our breadth-first search strategy.         tion Symbolic(𝜎) mapping from a concrete state to the set of sym-
Lemma 3.1 (Reachability of Successors).                                       bolic states representing it (the inverse of Concrete). More formally,
  𝜎ˆ →∗sym 𝜎ˆ ′ ⇒ ∀𝑙, run(𝑙) ⊨ □(𝜎ˆ → ♢𝜎ˆ ′ )                                 Symbolic(𝜎) = {𝜎ˆ | ∃𝑉0, 𝜎 ≃𝑉0 𝜎ˆ }.

Proof. By induction on the length of the derivation 𝜎ˆ →∗sym 𝜎ˆ ′ . If        Theorem 3.6 (Relatively Complete Bug Discovery).
𝜎ˆ ′ = 𝜎,
        ˆ then the theorem is obvious. Otherwise, we have 𝑠 →sym                IsBug(𝑝, 𝜎) ⇒ find_bugs(𝑝) ⊨ ♢Symbolic(𝜎)
𝜎ˆ ′′ and 𝜎ˆ ′′ →∗sym 𝜎ˆ ′ for some intermediate state 𝜎ˆ ′′ . Now suppose    Proof. Suppose IsBug(𝑝, 𝜎). By completeness of bug finding, we
that 𝜎ˆ occurs at a given position 𝑖𝜎ˆ in the stream run(l), the direct       have IsBugsym (𝑝, 𝜎). The result follows by the completeness of run
successor of 𝜎ˆ ′′ necessarily occurs at index 𝑖𝜎ˆ ′′ = 𝑖𝜎ˆ + |𝑙 | + 1 or
                                                                              and the fact that display keeps all stuck states in the stream. □
𝑖𝜎ˆ ′′ = 𝑖𝜎ˆ + |𝑙 | + 2 because run extends the task list by adding all the
successors (see Theorem 3.1) of the current state at the end of the              Termination. Implementing a complete and yet always terminat-
task list and there are at most two successors for any state. Since           ing bug finder is impossible as it would solve the Halting problem.
𝜎ˆ ′′ occurs at position 𝑖𝜎ˆ ′′ , we know by induction hypothesis that        Yet, there are programs for which SE can be exhaustive (e.g., pro-
𝜎ˆ ′ occurs at some index 𝑖𝜎ˆ ′′ + 𝑛 for 𝑛 ≥ 0.                           □   grams without loops nor recursion). We define “sound termination”
                                                                              as the property that whenever a bug finder emits a Finished mes-
   From Lemma 3.1, we conclude the completeness result.
                                                                              sage, it will not report anything else from that point on. If a soundly
Theorem 3.4 (Relative Completeness of Symbolic Execution).                    terminating, relatively complete bug finder does not report a bug
  𝜎ˆ →∗sym 𝜎ˆ ′ ⇒ run([𝜎])
                       ˆ ⊨ ♢𝜎ˆ ′                                              and says Finished, we can be sure that the tested program is safe.
Proof. It suffices to see that the first element of the stream run([𝜎])
                                                                    ˆ         Theorem 3.7 (Sound Termination of the Bug Finder).
is 𝜎ˆ and then to apply Lemma 3.1 at position 0.                      □         find_bugs(𝑝) ⊨ □(Finished → □Finished)

3.4     Relative Soundness and Completeness of                                Proof. Direct consequence of Theorem 3.3.                                 □
        the Symbolic Bug Finder                                               3.5    A T-Sound and T-Complete Bug Finder
In the previous section, we established the relative soundness and
                                                                              A T-sound and T-complete bug finder is a binary oracle answering
completeness of the symbolic executor regarding the symbolic se-
                                                                              yes if, and only if, the tested program is faulty. So far, we considered
mantics. Now, we define relatively sound bug discovery, a property
                                                                              bug finders producing infinite streams of status messages, to which
relevant to bug finders in general, including fuzzers. We assume
                                                                              T-soundness and T-completeness do not directly apply. Yet, relative
the interface of the function find_bugs from Sect. 3.2. That is,
                                                                              soundness and completeness (Theorem 3.6, Theorem 3.5) are suffi-
a bug finder outputs a stream of status messages that are either
                                                                              ciently strong to derive such an oracle. Relative soundness ensures
Pending, Finished, or BugFound. For a status message to be valid,
                                                                              for every BugFound(𝜎)    ˆ message that all 𝜎 ∈ Concrete(𝜎)  ˆ are error
a BugFound message must report a symbolic state corresponding
                                                                              states. The only obstacle in the way toward T-soundness is that
to a concrete set of bug-triggering states. The following defini-
                                                                              Concrete(𝜎)ˆ could be empty, i.e., 𝜎’sˆ path condition unsatisfiable.
tion of ValidStatus uses a function Concrete(𝜎)  ˆ mapping from a
                                                                              Otherwise, a BugFound message from the stream corresponds to a
symbolic state to the set of concrete states it represents. Formally,
                                                                              sound bug. SE engines typically use off-the-shelf constraint solvers
          ˆ = {𝜎 | ∃𝑉0, 𝜎 ≃𝑉0 𝜎ˆ }.
Concrete(𝜎)
                                                                              such as Z3 or CVC5 to determine if a path condition is unsatisfiable.
Definition 3.2 (Valid Status).                                                   Relative completeness, on the other hand, ensures that for any
  ValidStatus(𝑝) :=                                                           error state 𝜎, the stream contains a message BugFound(𝜎)         ˆ with
    {BugFound(𝜎) ˆ | ∀𝜎, 𝜎 ∈ Concrete(𝜎)
                                      ˆ ⇒ IsBug(𝑝, 𝜎)}                        𝜎ˆ ∈ Symbolic(𝜎). The latter condition implies that 𝜎’s     ˆ path con-
    ∨ Pending ∨ Finished                                                      dition is satisfiable. Inconveniently, a terminating bug finder can
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                                  Arthur Correnson and Dominic Steinhöfel


                                                                       two numbers. We annotated each program with assertions of their
 exception Bug
                                                                       correctness; e.g., for an integer square root 𝑟 of a number 𝑛, 𝑛 must
 exception Termination
                                                                       be in the closed interval [𝑟 2 ; (𝑟 + 1) 2 ]. Next, we derived a “buggy”
                                                                       mutation of each program, e.g., turning while _s > x do into
 let report msg =
                                                                       while _s < x do in the square root example. Finally, we asserted
   match msg with
                                                                       that our symbolic executors find the inserted bug but report no
   | BugFound (path, _, _) ->
                                                                       bug for the original programs. In addition, we verified that SE ter-
     if is_sat path then raise Bug
                                                                       minates with a Finished message for the correct programs when
   | Finished -> raise Termination
                                                                       we restrict the domain of the input number(s) to a finite range. To
   | _ -> ()
                                                                       demonstrate that a breadth-first path selection is superior to depth-
                                                                       first (as in the original DART symbolic executor [18]) in finding any
 type answer = YES | NO
                                                                       bug in a program, we added a --depth-first option to PyWiSE to
                                                                       transition to depth-first search. As a result, the bug in the factorial
 let has_bug p =
                                                                       implementation is not uncovered since SE gets “trapped” in infinite
   try iter report (find_bugs p)
                                                                       iterations of an early loop.
   with
     | Bug -> YES                                                         Engineering Tasks. The main novelty of this paper is the presenta-
     | Termination -> NO                                               tion of a mechanized specification of the correctness of testing tools
                                                                       and the implementation of a mechanically verified symbolic testing
                                                                       tool in a proof assistant. We abstracted the addressed problem in
       Figure 10: A T-sound and T-complete Bug Finder                  two noteworthy ways to facilitate this project.
                                                                          (1) Our target programming language IMP is a simple WHILE
never be complete in general; the bug could always be hidden in the            language. Extending our framework to a richer language
next state. Our solution to this problem is to implement a nontermi-           requires the specification of a richer semantics. For example,
nating but complete symbolic tester. Our implementation, shown in              the semantics of ES5 JavaScript in the JSCert project [6] is
Figure 10, builds on find_bugs and uses a constraint solver is_sat             implemented in about 3,000 lines of Coq code. The correct-
and a function iter for iterating over all elements of a stream. It            ness proof of JSRef, an executable reference interpreter for
only outputs “sound” bugs, terminates for finite symbolic execu-              JSCert, spans 3,500 lines of code.
tions, and continues SE as long as no bug is found or the process is      (2) We disregard the question of efficiency, which is orthogonal
interrupted. Since only terminating functions can be implemented               to our Questions (1) and (2). Yet, efficiency is crucial for the
in Coq, we have to resort to a “pen-and-paper” proof of has_bug’s              competitiveness of SE-based testing tools compared to ran-
T-soundness and T-completeness.                                                dom testing [8]. An efficient symbolic executor might replace
                                                                               the breadth-first path selection with, e.g., a coverage-guided
Theorem 3.8 (T-soundness and T-completeness).                                  generational search [19]. A considerable body of literature
  has_bug(𝑝) = 𝑌 𝐸𝑆 ⇔ HasBug(𝑝)                                                on efficient symbolic execution exists (cf. the survey by Bal-
Proof. The answer is YES iff there is a BugFound(⟨𝜑, 𝑆, 𝑝 ′ ⟩) mes-            doni et al. [3] for an overview). The role of our contribution
sage in the stream find_bugs(𝑝) such that 𝜑 is satisfiable. The                is to show how the correctness of an SE system can be re-
result follows from relative soundness/completeness.             □             tained in the face of efficiency optimizations. Exchanging
                                                                               path selection, for example, requires proving that all reach-
4    IMPLEMENTATIONS AND CASE STUDIES                                          able symbolic states are eventually considered by the new
In this section, we connect to Question (2) from the introduction:             selection mechanism (Lemma 3.1).
How can we engineer a reliable symbolic testing tool? We aim to           Extending our foundational work to efficient systems for richer
propose a design for symbolic executors independently of the im-       languages is possible. Of course, that step requires significant (proof)
plementation language; for the solution to be of general interest,     engineering work. This paper shows the way.
it should be able to “live” outside an interactive theorem prover.
Thus, we derived two executable implementations from the Coq           5    CONCLUSION AND FUTURE WORK
implementation of WiSE. First, we automatically extracted OCaml        Considering that testing is the predominant program verification
code, wrapped in a command line interface with a parser for IMP’s      technique, it may seem surprising that the correctness of bug
concrete syntax. Second, we developed a functionally equivalent        finders has not received more attention. Probably, this is because
Python implementation, PyWiSE, again with a usable command-            fuzzers, the most popular automated testing tools, are naturally
line frontend. We used Python generators to implement streams          “bug-sound”—they only report inputs that have already made the
where the Coq version uses co-induction and re-implemented the         program under test crash. However, fuzzers only find shallow bugs
Coq code with only small, purely syntactical changes.                  for programs with complex demands on their inputs or with code
    Since the transformations from Coq to executable programs          guarded by complex constraints. SE is a whitebox technique sim-
are not formally proven correct, we evaluated them with three          ulating multiple program executions at once. As such, this tech-
numeric algorithms. We chose the computation of a number’s fac-        nique can handle complex input constraints fully automatically.
torial and integer square root and the greatest common divisor of      Compared to a fuzzer, correctly implementing a symbolic executor
Engineering a Formally Verified Automated Bug Finder                                                              ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA


constitutes a much more significant challenge. We defined when a                          [5] Sandrine Blazy, Vincent Laporte, André Maroneze, and David Pichardie. 2013.
tester is “bug-sound” and “bug-complete” (i.e., a program is buggy                            Formal Verification of a C Value Analysis Based on Abstract Interpretation. In
                                                                                              Static Analysis, Francesco Logozzo and Manuel Fähndrich (Eds.). Springer, 324–
if, and only if, a bug is reported), resulting in the notions of T-                           344.
soundness and T-completeness. We chose a semantics for SE and                             [6] Martin Bodin, Arthur Charguéraud, Daniele Filaretti, Philippa Gardner, Sergio
                                                                                              Maffeis, Daiva Naudziuniene, Alan Schmitt, and Gareth Smith. 2014. A Trusted
demonstrated that it can be used as a foundation for symbolic bug                             Mechanised JavaScript Specification. In The 41st Annual ACM SIGPLAN-SIGACT
finding. Finally, we implemented a symbolic bug finder (WiSE) in                              Symposium on Principles of Programming Languages, POPL ’14, Suresh Jagan-
Coq, proved it T-sound and T-complete, and extracted executable                               nathan and Peter Sewell (Eds.). ACM, 87–100. https://doi.org/10.1145/2535838.
                                                                                              2535876
implementations in OCaml and Python.                                                      [7] Marcel Böhme, Danushka Liyanage, and Valentin Wüstholz. 2021. Estimating
    The resulting symbolic executors interpret programs in the sim-                           Residual Risk in Greybox Fuzzing. In ESEC/FSE ’21: 29th ACM Joint European
ple programming language IMP. Connecting to our foundational                                  Software Engineering Conference and Symposium on the Foundations of Software
                                                                                              Engineering, Diomidis Spinellis, Georgios Gousios, Marsha Chechik, and Massi-
work, we plan to support additional IMP features, such as functions                           miliano Di Penta (Eds.). ACM, 230–241. https://doi.org/10.1145/3468264.3468570
and pointers, in our symbolic executor. Thus, we could discover                           [8] Marcel Böhme and Soumya Paul. 2016. A Probabilistic Analysis of the Efficiency
                                                                                              of Automated Software Testing. IEEE Trans. Software Eng. 42, 4 (2016), 345–360.
common pitfalls in implementing their symbolic evaluation. More                               https://doi.org/10.1109/TSE.2015.2487274
generally, WiSE constitutes a solid basis for studying more advanced                      [9] Joshua Bundt, Andrew Fasano, Brendan Dolan-Gavitt, William Robertson, and
SE features, such as different path selection algorithms, constraint                          Tim Leek. 2021. Evaluating Synthetic Bugs. In ASIA CCS ’21: ACM Asia Conference
                                                                                              on Computer and Communications Security, Jiannong Cao, Man Ho Au, Zhiqiang
representations, or constraint-solving approaches.                                            Lin, and Moti Yung (Eds.). ACM. https://doi.org/10.1145/3433210.3453096
    Is it realistic to expect a fully verified symbolic executor for                     [10] Rod M. Burstall. 1974. Program Proving as Hand Simulation With a Little Induc-
an industrial programming language? We think it is—considering                                tion. In Information Processing, Proceedings of the 6th IFIP Congress 1974, Jack L.
                                                                                              Rosenfeld (Ed.). North-Holland, 308–312.
the existence of fully verified C compilers. In any case, blackbox                       [11] P. Cousot and R. Cousot. 1977. Abstract Interpretation: A Unified Lattice Model
testing will never find all the errors in existing symbolic executors;                        for Static Analysis of Programs by Construction or Approximation of Fixpoints.
                                                                                              In Conference Record of the Fourth Annual ACM SIGPLAN-SIGACT Symposium on
but insights from implementing different programming language                                 Principles of Programming Languages. ACM Press, 238–252.
features in a framework will positively influence their design.                          [12] Frank S. de Boer and Marcello M. Bonsangue. 2019. On the Nature of Symbolic
                                                                                              Execution. In Formal Methods - The Next 30 Years - Third World Congress, FM
                                                                                              2019, Proceedings (Lecture Notes in Computer Science, Vol. 11800), Maurice H. ter
DATA AVAILABILITY                                                                             Beek, Annabelle McIver, and José N. Oliveira (Eds.). Springer, 64–80. https:
Our WiSE and PyWiSE prototypes and the documentation of the                                   //doi.org/10.1007/978-3-030-30942-8_6
                                                                                         [13] Edsger W. Dijkstra. 1988. On the cruelty of really teaching computing science.
Coq sources can be accessed at                                                                Center for American History, University of Texas at Austin. http://www.cs.
                  https://github.com/acorrenson/WiSE/                                         utexas.edu/users/EWD/ewd10xx/EWD1036.PDF EWD-1036.
                                                                                         [14] Andrea Fioraldi, Dominik Christian Maier, Heiko Eißfeldt, and Marc Heuse. 2020.
                   https://acorrenson.github.io/WiSE/                                         AFL++: Combining Incremental Steps of Fuzzing Research. In 14th USENIX Work-
                                                                                              shop on Offensive Technologies, Yuval Yarom and Sarah Zennou (Eds.). USENIX
PyWiSE is also available on PyPI and can be installed via                                     Association. https://www.usenix.org/conference/woot20/presentation/fioraldi
                     pip install wise-se                                                 [15] Eduardo Giménez. 1996. An application of co-inductive types in Coq: Verification
                                                                                              of the alternating bit protocol. In Types for Proofs and Programs, Stefano Berardi
ACKNOWLEDGMENTS                                                                               and Mario Coppo (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 135–152.
                                                                                         [16] Eduardo Giménez and Pierre Castéran. 2007. A Tutorial on (Co-)Inductive Types
This work was supported by the European Research Council (ERC)                                in Coq. Available at https://www.labri.fr/perso/casteran/RecTutorial.pdf.
                                                                                         [17] Patrice Godefroid. 2005. The Soundness of Bugs is What Matters (Position
Grant HYPER (No. 101055412) and by DFG grant 389792660 as part                                Statement). In PLDI’05 Workshop on the Evaluation of Software Defect Detection
of TRR 248. Views and opinions expressed are however those of                                 Tools (BUGS’05), Proceedings. https://patricegodefroid.github.io/public_psfiles/
the authors only and do not necessarily reflect those of the Euro-                            bugs2005.pdf
                                                                                         [18] Patrice Godefroid, Nils Klarlund, and Koushik Sen. 2005. DART: Directed Auto-
pean Union or the European Research Council Executive Agency.                                 mated Random Testing. In Proceedings of the ACM SIGPLAN 2005 Conference on
Neither the European Union nor the granting authority can be                                  Programming Language Design and Implementation (PLDI’05), Vivek Sarkar and
                                                                                              Mary W. Hall (Eds.). ACM, 213–223. https://doi.org/10.1145/1065010.1065036
held responsible for them. A. Correnson carried out this work as a                       [19] Patrice Godefroid, Michael Y. Levin, and David A. Molnar. 2008. Automated
member of the Saarbrücken Graduate School of Computer Science.                                Whitebox Fuzz Testing. In Proceedings of the Network and Distributed Sys-
                                                                                              tem Security Symposium (NDSS’08). The Internet Society. https://www.ndss-
                                                                                              symposium.org/ndss2008/automated-whitebox-fuzz-testing/
REFERENCES                                                                               [20] Jacques-Henri Jourdan, Vincent Laporte, Sandrine Blazy, Xavier Leroy, and David
 [1] Wolfgang Ahrendt, Andreas Roth, and Ralf Sasse. 2005. Automatic Validation               Pichardie. 2015. A Formally-Verified C Static Analyzer. In Proceedings of the
     of Transformation Rules for Java Verification Against a Rewriting Semantics. In          42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Logic for Programming, Artificial Intelligence, and Reasoning, 12th International        Languages (POPL’15), Sriram K. Rajamani and David Walker (Eds.). ACM, 247–259.
     Conference (LPAR’05), Proceedings (Lecture Notes in Computer Science, Vol. 3835),        https://doi.org/10.1145/2676726.2676966
     Geoff Sutcliffe and Andrei Voronkov (Eds.). Springer, 412–426. https://doi.org/     [21] Timotej Kapus and Cristian Cadar. 2017. Automatic Testing of Symbolic Execution
     10.1007/11591191_29                                                                      Engines via Program Generation and Differential Testing. In Proceedings of the
 [2] Christel Baier and Joost-Pieter Katoen. 2008. Principles of Model Checking. The          32nd IEEE/ACM International Conference on Automated Software Engineering
     MIT Press. http://www.amazon.com/Principles-Model-Checking-Christel-                     (ASE’17), Grigore Rosu, Massimiliano Di Penta, and Tien N. Nguyen (Eds.). IEEE
     Baier/dp/026202649X%3FSubscriptionId%3D13CT5CVB80YFWJEPWS02%                             Computer Society. https://doi.org/10.1109/ASE.2017.8115669
     26tag%3Dws%26linkCode%3Dxm2%26camp%3D2025%26creative%3D165953%                      [22] Steven Keuchel, Sander Huyghebaert, Georgy Lukyanov, and Dominique De-
     26creativeASIN%3D026202649X                                                              vriese. 2022. Verified Symbolic Execution with Kripke Specification Monads
 [3] Roberto Baldoni, Emilio Coppa, Daniele Cono D’Elia, Camil Demetrescu, and                (and no Meta-Programming). Proc. ACM Program. Lang. 6, ICFP (2022), 194–224.
     Irene Finocchi. 2018. A Survey of Symbolic Execution Techniques. ACM Comput.             https://doi.org/10.1145/3547628
     Surv. 51, 3 (2018), 50:1–50:39. https://doi.org/10.1145/3182657                     [23] James C. King. 1976. Symbolic Execution and Program Testing. Commun. ACM
 [4] Christoph Baumann, Bernhard Beckert, Holger Blasum, and Thorsten Bormer.                 19, 7 (1976). https://doi.org/10.1145/360248.360252
     2012. Lessons Learned From Microkernel Verification – Specification is the New      [24] Ralf Kneuper. 1991. Symbolic Execution: A Semantic Approach. Sci. Comput.
     Bottleneck. In Proceedings Seventh Conference on Systems Software Verification,          Program. 16, 3 (1991), 207–249. https://doi.org/10.1016/0167-6423(91)90008-L
     (SSV’12) (EPTCS, Vol. 102), Franck Cassez, Ralf Huuck, Gerwin Klein, and Bastian    [25] Xavier Leroy. 2009. A Formally Verified Compiler Back-end. J. Autom. Reason.
     Schlich (Eds.). 18–32. https://doi.org/10.4204/EPTCS.102.4                               43, 4 (2009). https://doi.org/10.1007/s10817-009-9155-4
ESEC/FSE ’23, December 3–9, 2023, San Francisco, CA, USA                                 Arthur Correnson and Dominic Steinhöfel


[26] Danushka Liyanage, Marcel Böhme, Chakkrit Tantithamthavorn, and Stephan
     Lipp. 2023. Reachable Coverage: Estimating Saturation in Fuzzing. In 45th
     IEEE/ACM International Conference on Software Engineering (ICSE’23), Proceedings.
     ACM. https://mboehme.github.io/paper/ICSE23.Effectiveness.pdf to appear..
[27] Dorel Lucanu, Vlad Rusu, and Andrei Arusoaie. 2017. A Generic Framework
     for Symbolic Execution: A Coinductive Approach. J. Symb. Comput. 80 (2017),
     125–163. https://doi.org/10.1016/j.jsc.2016.07.012
[28] Valentin Robert and Xavier Leroy. 2012. A formally-verified alias analysis. In
     Certified Programs and Proofs (CPP 2012) (Lecture Notes in Computer Science,
     Vol. 7679). Springer, 11–27.
[29] Rollbar. 2021. The State of Software Code Report. https://content.rollbar.com/
     hubfs/State-of-Software-Code-Report.pdf. Accessed: 2023-01-24.
[30] Mary Shaw. 2003. Writing Good Software Engineering Research Papers. In
     Proceedings of the 25th International Conference on Software Engineering, May
     3-10, 2003, Portland, Oregon, USA, Lori A. Clarke, Laurie Dillon, and Walter F.
     Tichy (Eds.). IEEE Computer Society, 726–737. https://doi.org/10.1109/ICSE.2003.
     1201262
[31] Matthieu Sozeau, Simon Boulier, Yannick Forster, Nicolas Tabareau, and Théo
     Winterhalter. 2020. Coq Coq correct! Verification of Type Checking and Erasure
     for Coq, in Coq. Proc. ACM Program. Lang. 4, POPL (2020), 8:1–8:28. https:
     //doi.org/10.1145/3371076
[32] Dominic Steinhöfel. 2020. Abstract Execution: Automatically Proving Infinitely
     Many Programs. Ph. D. Dissertation. Darmstadt University of Technology, Ger-
     many. http://tuprints.ulb.tu-darmstadt.de/8540/
[33] Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2015. Featherweight VeriFast.
     Log. Methods Comput. Sci. 11, 3 (2015). https://doi.org/10.2168/LMCS-11(3:19)2015

Received 2023-02-02; accepted 2023-07-27
