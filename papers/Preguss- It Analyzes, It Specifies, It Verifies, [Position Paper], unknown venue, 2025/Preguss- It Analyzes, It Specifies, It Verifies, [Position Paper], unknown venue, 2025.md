                                                         Preguss: It Analyzes, It Specifies, It Verifies
                                                                                                              [Position Paper]
                                                          Zhongyi Wang∗                                             Tengjie Lin∗                              Mingshuai Chen†
                                                       Zhejiang University                                      Zhejiang University                            Zhejiang University
                                                        Hangzhou, China                                          Hangzhou, China                                Hangzhou, China
                                                    zhongyi.wang@zju.edu.cn                                    tengjie.lin@zju.edu.cn                          m.chen@zju.edu.cn

                                                            Mingqi Yang                                              Haokun Li                                        Xiao Yi
                                                       Zhejiang University                                        Peking University                 The Chinese University of Hong Kong
                                                         Hangzhou, China                                           Beijing, China                           Hong Kong, China
arXiv:2508.14532v1 [cs.SE] 20 Aug 2025




                                                      mingqiyang@zju.edu.cn                                         ker@pm.me                          yixiao5428@link.cuhk.edu.hk

                                                                                      Shengchao Qin                                       Jianwei Yin
                                                                                    Xidian University                                  Zhejiang University
                                                                                      Xi’an, China                                      Hangzhou, China
                                                                                shengchao.qin@gmail.com                                zjuyjw@zju.edu.cn

                                         Abstract                                                                             Software and its engineering → Formal software veri-
                                         Fully automated verification of large-scale software and hard-                       fication; Automated static analysis.
                                         ware systems is arguably the holy grail of formal methods.
                                                                                                                              Keywords: Abstract interpretation, Large language models,
                                         Large language models (LLMs) have recently demonstrated
                                                                                                                              Minimal contract, Undefined behaviors
                                         their potential for enhancing the degree of automation in for-
                                         mal verification by, e.g., generating formal specifications as                       ACM Reference Format:
                                         essential to deductive verification, yet exhibit poor scalability                    Zhongyi Wang, Tengjie Lin, Mingshuai Chen, Mingqi Yang, Haokun
                                         due to context-length limitations and, more importantly, the                         Li, Xiao Yi, Shengchao Qin, and Jianwei Yin. 2025. Preguss: It
                                         difficulty of inferring complex, interprocedural specifications.                     Analyzes, It Specifies, It Verifies. In Proceedings of 1st International
                                         This paper outlines Preguss – a modular, fine-grained frame-                         Workshop on Language Models and Programming Languages (LMPL
                                         work for automating the generation and refinement of formal                          ’25). ACM, New York, NY, USA, 6 pages. https://doi.org/xx.xxxx/
                                         specifications. Preguss synergizes between static analysis
                                         and deductive verification by orchestrating two components:                          1    Introduction
                                         (i) potential runtime error (RTE)-guided construction and
                                         prioritization of verification units, and (ii) LLM-aided syn-                        Runtime errors (RTEs), e.g., division by zero, buffer/numeric
                                         thesis of interprocedural specifications at the unit level. We                       overflows, and null pointer dereference, are a common cause
                                         envisage that Preguss paves a compelling path towards the                            of undefined behaviors (UBs) exhibited during the execution
                                         automated verification of large-scale programs.                                      of C/C++ programs [16, Sect. 3.5.3]. These UBs can trigger
                                                                                                                              catastrophic failures, rendering them critical considerations
                                         CCS Concepts: • Theory of computation → Program                                      for safety-critical applications [1, 4, 22, 27]. Consequently,
                                         verification; Program specifications; Program analysis; •                            in conventional program verification methodologies, estab-
                                         ∗ Both authors contributed equally to this research.                                 lishing RTE-freeness (i.e., conformance to the C standard
                                         † Corresponding author.                                                              specification) constitutes a necessary precondition for veri-
                                                                                                                              fying functional correctness (i.e., adherence to intended be-
                                         Permission to make digital or hard copies of all or part of this work for            haviors) [24]. State-of-the-art abstract interpretation-based
                                         personal or classroom use is granted without fee provided that copies                static analyzers, such as Astrée [18], Frama-C/Eva [8], and
                                         are not made or distributed for profit or commercial advantage and that
                                         copies bear this notice and the full citation on the first page. Copyrights          Mopsa [17], aim to reliably detect all potential UBs in C pro-
                                         for components of this work owned by others than the author(s) must                  grams, thereby formally certifying the absence of RTEs. How-
                                         be honored. Abstracting with credit is permitted. To copy otherwise, or              ever, due to the inherent abstraction mechanism that soundly
                                         republish, to post on servers or to redistribute to lists, requires prior specific   approximates concrete program semantics [10], these tools
                                         permission and/or a fee. Request permissions from permissions@acm.org.               often emit numerous false positives. Manually identifying
                                         LMPL ’25, Singapore
                                                                                                                              such false alarms or tuning analyzer configurations for better
                                         © 2025 Copyright held by the owner/author(s). Publication rights licensed
                                         to ACM.                                                                              accuracy remains notoriously difficult [26].
                                         ACM ISBN 979-8-4007-1248-7/2025/06                                                      Program verification tools employing deductive verifica-
                                         https://doi.org/xx.xxxx/                                                             tion [2] provide a rigorous methodology for ensuring critical
LMPL ’25, October 15, 2025, Singapore                                                                                         Wang et al.


program properties, including both RTE absence and func-             #include <limits.h>              #include <limits.h>
tional correctness. The verification process typically involves      int abs(int x) {                 /*@ requires INT_MIN < x; */
two stages: (i) constructing specifications to formalize in-           if (x < 0)                     int abs(int x) {
                                                                         /*@ assert overflow:           if (x < 0)
tended program behaviors, and (ii) proving that the program
                                                                         ↩→ -2147483647 <= x; */          return -x;
adheres to the specifications. While modern verifiers such as            return -x;                     else
Frama-C/Wp [7] and Dafny [19] automate the latter stage,               else                               return x;
the former stage still relies heavily on human expertise.                return x;                    }
   Recent studies [20, 21, 28–30] have explored large lan-           }                                void main() {
guage models (LLMs) for automated specification synthesis,           void main() {                      int a = abs(42);
                                                                       int a = abs(42);                 /*@ preconditions of abs */
demonstrating substantial improvements over conventional               int b = abs(INT_MIN);            int b = abs(INT_MIN);
techniques. Nevertheless, these methods exhibit significant          }                                }
scalability limitations when applied to large-scale programs.
Current evaluations [21, 28–30] remain confined to small-              (a) analysis result of abs.c   (b) verification of specified abs.c
scale benchmarks (e.g., SV-COMP test suites [6], Code2Inv
benchmark set [23], SyGuS competition [3]), each compris-            Figure 1. Identifying potential RTEs in a C program via the
ing individual or just a few functions. Although SpecGen [20,        abstract interpretation-based analyzer Frama-C/Eva [8] and
Sect. VI-A] explores specification synthesis for substantial         the deductive verifier Frama-C/Wp [7].
real-world Java programs, its focus remains restricted to
specification verifiability (i.e., syntactic and semantic correct-
ness) rather than holistic program verification – emcompass-         potential RTEs. These tools exhibit significant advantages in
ing properties like RTE-freeness and functional correctness.         automatically scaling to large codebases. During the analy-
This limitation is primarily due to two constraints: First, the      sis, they embed RTE (guard) assertions at program locations
context-length limitation of LLMs [13] prohibits them from           susceptible to undefined behaviors – as exemplified by the
processing large-scale programs as a whole; Second, verify-          assertion -2147483647 <= x in Fig. 1a. The analyzers main-
ing complex programs necessitates the synthesis of a diverse         tain abstract program states – e.g., overapproximating pos-
set of interprocedural specifications, e.g., preconditions, post-    sible values {−3, 0, 3} via an interval abstraction [−3, 3] –
conditions, invariants, etc. The latter is beyond the capability     and validate satisfiability of the RTE assertions against these
of existing approaches: (i) some focus exclusively on specific       abstract states. Unsatisfied assertions are subsequently re-
categories (e.g., invariants [21, 29, 30]), and (ii) others gener-   ported as RTE alarms. Fig. 1a illustrates the analysis result
ate function contracts holistically without modeling intrinsic       for the commonly used code snippet abs.c generated by
differences between preconditions and postconditions (as             Frama-C/Eva [8], which signifies a potential RTE of signed
part of the contracts) [20, 28], which are critical for validating   integer overflow expressed in the ANSI/ISO C Specification
potential RTEs (as demonstrated in Section 2).                       Language (ACSL) [5].
   In response to the aforementioned challenges, we propose             Tracing the RTE in Fig. 1a is a classic source-to-sink prob-
Preguss – an LLM-aided framework for synthesizing fine-              lem [25] in static (taint) analysis, namely, to identify that x =
grained formal specifications. Preguss first employs a static        INT_MIN (source) exclusively triggers the overflow RTE (sink)
analyzer to emit RTE assertions (signifying all possible RTEs),      in the abs function. Although taint analysis tools can track
then constructs a queue of verification units (contexts of pro-      data-flow paths from untrusted sources to sinks, validating
gram slices and relevant assertions) according to the RTE            these paths requires analysts to monitor how the data flows
assertions, and finally prompts an LLM to generate and re-           through the program and interacts with different compo-
fine interprocedural specifications for every verification unit.     nents. This is a prohibitively challenging task in large-scale
We envisage that Preguss facilitates (i) the synergy between         programs due to intricate call hierarchies and data dependen-
static analysis and deductive verification: The RTE assertions       cies. Deductive verification addresses this challenge through
reported by static analysis are used to either construct nec-        an advanced mechanism that propagates guard assertions
essary specifications certifying RTE-freeness or locate root         from sinks upward along caller-callee chains, enabling vio-
causes triggering RTEs; and (ii) modular synthesis of inter-         lation checks at potential source locations. This approach
procedural specifications and thereby a viable approach to           facilitates either precise RTE source tracing or formal estab-
the automated verification of large-scale programs.                  lishment of RTE absence [12, 14].
                                                                        Specifically, by augmenting functions with necessary spec-
                                                                     ifications, e.g., the ACSL precondition requires INT_MIN <
2     Background and Motivation
                                                                     x in Fig. 1b, verifiers like Frama-C/Wp [7] (based on weakest-
2.1   Potential RTE-Guided Verification                              precondition reasoning [11]) formally certify RTE-free exe-
Abstract interpretation-based static analyzers [8, 17, 18] con-      cution under the specified preconditions. These preconditions
duct sound value analysis of target programs to warn about           subsequently serve as guard assertions at call sites of caller
Preguss: It Analyzes, It Specifies, It Verifies                                                           LMPL ’25, October 15, 2025, Singapore


 int id(int x) {return x;}             /*@ requires x != 0; */                 Nevertheless, existing approaches [20, 28] mostly assume
                                       /*@ ensures \result == x; */         RTE-freeness of a target program for verifying functional cor-
 void one() {                          int id(int x) {return x;}            rectness, employing simplistic interprocedural-specification
   int x = id(1);
                                                                            synthesis strategies that ask LLMs to generate holistic func-
   /*@ assert division_by_0:           void one() {
   ↩→ x != 0; */                         int x = id(1); 1/x;
                                                                            tion contracts across the entire program context in a uni-
   1/x;                                }                                    form, monolithic manner. This methodology risks inducing
 }                                     void zero() {                        false positives during RTE-freeness validation, as illustrated
 void zero() {                           /*@ preconditions of id */         by Fig. 2. An LLM may be misled by the context “x != 0
   id(0);                                id(0);                             and 1/x” in one and thus forge an over-constrained precon-
 }                                     }
 void main() {                         void main() {
                                                                            dition requires x != 0 for id, which triggers spurious
   one(); zero();                        one(); zero();                     alarms at call sites like id(0) in function zero. Although
 }                                     }                                    discarding over-constrained preconditions while retaining
                                                                            postconditions may resolve immediate false alarms (as is
   (a) analysis result of id.c         (b) verification of specified id.c   the case for Fig. 2b), determining whether a precondition
                                                                            is over-constrained is per se a nontrivial task (cf. Fig. 1b vs.
Figure 2. Demonstrating the dual role of interprocedural                    Fig. 2b). For Fig. 1b, simply discarding the precondition com-
specifications: postconditions can eliminate false RTEs while               promises soundness (as true RTEs are missed) and thus un-
over-constrained preconditions can induce false alarms.                     dermines verification integrity. Therefore, interprocedural-
                                                                            specification synthesis mechanisms should make efforts to
                                                                            prevent the generation of over-constrained preconditions.
functions. Fig. 1b demonstrates this mechanism: The argu-
ment INT_MIN violates abs’s (weakest) precondition, thus
                                                                            3     Methodology
leading the verifier to report a definitive RTE at call site
abs(INT_MIN); In other words, RTE-freeness can be guaran-                   This section presents the design principles behind Preguss –
teed in case no caller of abs violates its precondition.                    our framework for Potential Runtime Error-GUided Specifi-
    This gives rise to our conceptual idea of potential RTE-                cation Synthesis. As depicted in Fig. 3, Preguss is comprised
guided verification, which aims to synergize between static                 of two synergistic components: (i) Potential RTE-guided con-
analysis and deductive verification. The core paradigm is to                struction and prioritization of verification units: a divide-and-
exploit analyzer-reported RTE assertions to either (i) con-                 conquer strategy [31] for decomposing the monolithic RTE-
struct necessary specifications certifying RTE-freeness, or                 freeness verification into prioritized units; (ii) Fine-grained
(ii) locate root causes triggering RTEs. We will show in Sec-               interprocedural specification synthesis: a tactic for inferring
tion 3 how this paradigm can be refined to a pipeline that                  necessary specifications via LLMs along caller-callee chains
facilitates automated verification of large-scale programs.                 to validate target assertions per verification unit. Below, we
                                                                            show how these two components cooperate to facilitate Pre-
2.2    Interprocedural Specifications                                       guss’s scalability to large-scale programs.
The example in Fig. 1 illustrates the simple case where an
RTE assertion (-2147483647 <= x) can be validated through                   3.1   Decomposing the Monolithic Verification
specifications (requires INT_MIN < x) localized to its host                 To address the context-length limitation of LLMs [13], we
function (abs). There are, however, common cases where in-                  decompose the monolithic RTE-freeness verification prob-
terprocedural specifications are necessary: As demonstrated                 lem into a sequence of subproblems for validating individual
by Fig. 2, function one contains a potential division-by-zero               potential RTEs associated with necessary program contexts. As
UB flagged by assertion x != 0 (Fig. 2a), which is in fact a                shown in Fig. 3, we first employ static analysis to generate
false alarm that can be eliminated solely through the postcon-              RTE assertions for all possible UBs in the target program (❶).
dition ensures \result == x of function id (Fig. 2b). Con-                  We then construct the program’s call graph while recording
cretely, the value of x is determined by argument 1 and the                 all the call sites (❷), yielding a complete set of RTE guard
postcondition of id at call site id(1), thereby guaranteeing                assertions. These assertions are classified into two distinct
assertion satisfaction irrespective of the precondition of its              categories: (i) UB assertions generated during the initial anal-
host function one. Both examples in Figs. 1 and 2 reveal a core             ysis, and (ii) call-site preconditions (initially defaulting to
forward verification principle: Validating control-flow down-               tautological true) to be synthesized/updated by LLMs per
stream properties (e.g., RTE assertions in Figs. 1a and 2a)                 Section 3.2. For each assertion, we construct a verification
requires correct upstream specifications (e.g., precondition                unit (V-Unit) containing both the assertion and its necessary
in Fig. 1b or postcondition in Fig. 2b). This observation moti-             contextual program slices. These V-Units are prioritized in
vates specialized mechanisms for generating interprocedural                 a queue (❸) exactly matching the sequence of their corre-
specifications in programs with complex call hierarchies.                   sponding RTE assertions produced by a post-order traversal
LMPL ’25, October 15, 2025, Singapore                                                                                                                                Wang et al.

                                  Stage 1. Potential RTE-Guided Construction and Prioritization of Verification Units

                            ❶                                      Program with              ❷    Call Graph                 Call Graph
         Program                  Static Analyzer                                                                                                  main()
                                                                   RTE assertions                  Analysis                                        {CS_3; CS_4;}

              V-Unit Priority Queue                                                                                               func1()
                                                                                                                                  {CS_1; CS_2;            func2()
                                                                                                                                   UB_3;}                 {UB_4;}
            V-Unit 4             V-Unit 3               V-Unit 2            V-Unit 1             Program slicer
             CS_2                 CS_1                   UB_2                UB_1                       &              ❸
                                                                                                                            foo1()            foo2()
                                                                                                 Priority-Queue             {UB_1;}           {UB_2;}
            V-Unit 5             V-Unit 6               V-Unit 7            V-Unit 8               Generator
             UB_3                 UB_4                   CS_3                CS_4                                          UB_#: RTE guard assertion for the #-th UB
                                                                                                                           CS_#: the #-th call-site precondition check


                                     ❹                                        Update specifications of                             Update specifications of ❻
                                            V-Unit                      ❺
                                                                                 the host function                                   all callee functions
                                                                                                                  LLM
        Proof Goal: the guard assertion of UB or CS                                                      N                                                  N
                                                                           If the        N                         Y            If the         N
                    Program Context                                                                 If #iter                                              If #iter
                                                                        assertion is                                         assertion is
                                                                                                   exhausts?                                             exhausts?
                                                                          valid?                                               valid?
                        func1()
                                                                               Y                                                    Y                          Y
                  foo1()                                                        (i) Jump to the next V-Unit, or (ii) return the
                                foo2()                              ❼                                                                           ❽     Halt and alert
                                                                                 specified program if this is the last V-Unit.

                                               Stage 2. Fine-Grained Interprocedural Specification Synthesis

                                                      Figure 3. Architecture of the Preguss framework.

of the call graph. This deliberate ordering implements the                                   LLM is prompted to infer preconditions and auxiliary speci-
bottom-up verification mechanism by progressing systemat-                                    fications (e.g., loop contracts) through backward reasoning
ically from leaf functions toward the root function [28].                                    from the guard assertion – as informally analogous to the
   Preguss leverages the modularization principle of deduc-                                  process of weakest-precondition reasoning [11]. When the
tive verification [2, Chap. 9], wherein functions are verified                               assertion depends on callees’ return values (recall Fig. 2a),
in isolation using their contracts. Rather than feeding LLMs                                 the verification requires callees’ postconditions, thus trig-
with the entire program in an end-to-end manner, validating                                  gering the transition to the subsequent phase (❻). Crucially,
individual RTEs requires a constrained context comprising                                    to prevent over-constrained preconditions (as exemplified
two components: the guard assertion and a two-layer pro-                                     in Fig. 2b), the callees’ precondition synthesis is expressly
gram slice (encompassing both the assertion’s host function                                  prohibited during this stage. Upon successful verification
and its callees), collectively encapsulated within a V-Unit                                  of the assertion alongside all generated specifications (ex-
(e.g., ❹). This design ensures that the context does not expand                              cluding host preconditions), Preguss either proceeds to the
significantly during the bottom-up verification progression,                                 next V-Unit or returns the specified program if the priority
thereby enabling scalability to large-scale programs.                                        queue becomes empty (❼). Unverifiable assertions trigger
                                                                                             immediate termination with high-risk RTE alerts (❽).
3.2   Generating Interprocedural Specifications                                                 Preguss directly operationalizes our insights presented in
                                                                                             Section 2.2: By leveraging the V-Unit’s constrained context
As motivated in Section 2, Preguss implements a fine-grained
                                                                                             and implementing a two-stage interprocedural-specification
strategy for synthesizing interprocedural specifications. This
                                                                                             synthesis strategy (thereby mirroring the forward verifica-
approach fundamentally differs from existing methods by
                                                                                             tion principle), Preguss systematically avoids generating
avoiding the holistic function-contract generation from uni-
                                                                                             over-constrained preconditions while enabling automated,
form contexts. Preguss processes each V-Unit through two
                                                                                             scalable RTE-freeness verification for large-scale programs.
distinct phases: specification generation for the assertion’s
host function (❺), followed by specification generation for
callee functions (❻). Both phases employ an iterative refine-                                4    Conclusion and Future Directions
ment strategy where (i) an LLM generates candidate spec-                                     We have conceived Preguss – a modular, fine-grained frame-
ifications, (ii) a verifier validates the target assertion using                             work for inferring formal specifications that synergize be-
these specifications, and (iii) an LLM refines the (possibly)                                tween static analysis and deductive verification. We envisage
failed candidates based on the verifier’s feedback. This pro-                                that Preguss offers a promising paradigm towards the au-
cedure terminates until either the validation succeeds or the                                tomated verification of large-scale programs (subject to an
iteration limit (#iter) is exhausted. In the initial phase (❺), the                          extensive experimental evaluation in future work).
Preguss: It Analyzes, It Specifies, It Verifies                                                       LMPL ’25, October 15, 2025, Singapore


   While initially devised to certify RTE-freeness and identify    Acknowledgments
genuine RTEs, the framework can be extended to cater for           This work has been partially funded by the ZJNSF Major Pro-
the verification of other vulnerability classes and functional     gram (No. LD24F020013), by the CCF-Huawei Populus Grove
correctness. The key is to substitute RTE-assertion gener-         Fund (No. CCF-HuaweiSY202503), by the Open Fund of the
ation (via static analysis) with tailored formal annotations       High-Reliability Embedded Software Engineering Technol-
for the target properties, including ones with complex data        ogy Laboratory (No. LHCESET202502), and by the Huawei
structures. The subsequent stages, commencing from ❷ in            Technical Collaboration Project (No. TC20250422031).
Fig. 3, remain fully generic to handle these annotations.
   Although Preguss presents a promising paradigm for
automated large-scale program verification, establishing a         References
formal proof of its soundness remains non-trivial – It re-          [1] 2000. The Explosion of the Ariane 5. https://www-users.cse.umn.edu/
                                                                        ~arnold/disasters/ariane.html
quires a rigorous justification that verified properties hold       [2] Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle,
under all execution paths. This necessitates foundational               Peter H. Schmitt, and Mattias Ulbrich (Eds.). 2016. Deductive Software
work in two directions: (i) precise formalization of target             Verification – The KeY Book – From Theory to Practice. Lecture Notes
verification properties, and (ii) rigorous proof establishing           in Computer Science, Vol. 10001. Springer.
semantic equivalence between synthesized specifications             [3] Rajeev Alur, Dana Fisman, Saswat Padhi, Rishabh Singh, and Ab-
                                                                        hishek Udupa. 2019. SyGuS-Comp 2018: Results and Analysis. CoRR
and program behaviors. This foundational work must bridge               abs/1904.07146 (2019).
the gap between practical LLM-based synthesis and formal            [4] America’s Cyber Defense Agency. 2025. Secure by Design Alert: Elimi-
method guarantees. Additionally, language-specific complex-             nating Buffer Overflow Vulnerabilities. https://www.cisa.gov/resources-
ities pose significant soundness threats. The pervasive use of          tools/resources/secure-design-alert-eliminating-buffer-overflow-
function pointers in C programs may induce incomplete call              vulnerabilities
                                                                    [5] Patrick Baudin, Pascal Cuoq, Jean-Christophe Filliâtre, Claude Marché,
graphs during static analysis, potentially causing undetected           Benjamin Monate, Yannick Moy, and Virgile Prevosto. 2025. ANSI/ISO
function dependencies, verification context omissions, and              C Specification LanguageVersion 1.22. https://www.frama-c.com/
unsound RTE guard propagation. Ensuring call graph relia-               download/frama-c-acsl-implementation.pdf
bility – through advanced pointer analysis techniques like          [6] Dirk Beyer. 2024. State of the Art in Software Verification and Witness
flow-sensitive analysis – becomes imperative for any robust             Validation: SV-COMP 2024. In TACAS (3) (Lecture Notes in Computer
                                                                        Science, Vol. 14572). Springer, 299–329.
implementation.                                                     [7] Allan Blanchard. 2020. Introduction to C program proof with Frama-C
   Conceived for scalability in programs with lengthy chains            and its WP plugin. https://allan-blanchard.fr/frama-c-wp-tutorial.
of function calls, Preguss exhibits limitations when applied            html
to: (i) Mutually recursive functions, which induce loopy struc-     [8] David Bühler, Pascal Cuoq, and Boris Yakobowski. 2025. The Eva plug-
tures in the call graph disrupting the bottom-up verification           in. https://www.frama-c.com/download/frama-c-eva-manual.pdf
                                                                    [9] Jialun Cao, Yaojie Lu, Meiziniu Li, Haoyang Ma, Haokun Li, Mengda
mechanism, causing potential failures of the interprocedural            He, Cheng Wen, Le Sun, Hongyu Zhang, Shengchao Qin, Shing-Chi
specification synthesis; (ii) Star-structured call graphs (char-        Cheung, and Cong Tian. 2025. From Informal to Formal - Incorporating
acterized by few callers invoking numerous callees), where              and Evaluating LLMs on Natural Language Requirements to Verifiable
V-Units containing an inflated context of such functions may            Formal Proofs. In ACL (1). Association for Computational Linguistics,
                                                                        26984–27003.
exceed the LLM’s context limit. For the latter, a potential
                                                                   [10] Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A
solution is to employ program slicing to extract the minimal            Unified Lattice Model for Static Analysis of Programs by Construction
subset of statements exhibiting dependencies with the target            or Approximation of Fixpoints. In POPL. ACM, 238–252.
assertion, thus omitting nonessential callees.                     [11] Edsger W. Dijkstra. 1975. Guarded Commands, Nondeterminacy and
   Given LLMs’ susceptibility to hallucination [15], they fre-          Formal Derivation of Programs. Commun. ACM 18, 8 (1975), 453–457.
quently generate specifications exhibiting critical flaws –        [12] Arnaud Ebalard, Patricia Mouy, and Ryad Benadjila. 2019. Journey to
                                                                        a RTE-Free X.509 Parser. In Symposium sur la sécurité des technologies
ranging from syntactically illegal constructs that violate              de l’information et des communications (SSTIC 2019).
specification language grammars to semantically unsatis-           [13] Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu
fiable predicates that contradict actual program behaviors.             Zhang, Ruijie Fang, Asmita, Ryan Tsang, Najmeh Nazari, Han Wang,
While verifiers provide rich feedback (e.g., proof obligations          and Houman Homayoun. 2024. Large Language Models for Code Anal-
and diagnostic logs) on such errors, translating these formal           ysis: Do LLMs Really Do Their Job?. In USENIX Security Symposium.
                                                                        USENIX Association.
outputs into effective LLM refinement prompts presents a           [14] Jens Gerlach. 2019. Minimal contract Hoare-style verification versus
significant research challenge due to the formal-to-informal            abstract interpretation. Technical Report.
semantic gap (cf. [9]). Future work should therefore focus         [15] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng,
on developing principled mechanisms to bridge this gap.                 Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing
                                                                        Qin, and Ting Liu. 2025. A Survey on Hallucination in Large Language
                                                                        Models: Principles, Taxonomy, Challenges, and Open Questions. ACM
                                                                        Trans. Inf. Syst. 43, 2 (2025), 42:1–42:55.
                                                                   [16] ISO/IEC JTC 1/SC 22. 2024. ISO/IEC 9899:2024 Information technology
                                                                        — Programming languages — C. ISO. https://www.iso.org/standard/
LMPL ’25, October 15, 2025, Singapore                                           Wang et al.


     82075.html
[17] Matthieu Journault, Antoine Miné, Raphaël Monat, and Abdelraouf
     Ouadjaout. 2019. Combinations of Reusable Abstract Domains for
     a Multilingual Static Analyzer. In VSTTE (Lecture Notes in Computer
     Science, Vol. 12031). Springer, 1–18.
[18] Daniel Kästner, Reinhard Wilhelm, and Christian Ferdinand. 2023.
     Abstract Interpretation in Industry - Experience and Lessons Learned.
     In SAS (Lecture Notes in Computer Science, Vol. 14284). Springer, 10–27.
[19] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for
     Functional Correctness. In LPAR (Dakar) (Lecture Notes in Computer
     Science, Vol. 6355). Springer, 348–370.
[20] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen:
     Automated Generation of Formal Program Specifications via Large
     Language Models. (2025), 16–28.
[21] Muhammad A. A. Pirzada, Giles Reger, Ahmed Bhayat, and Lucas C.
     Cordeiro. 2024. LLM-Generated Invariants for Bounded Model Check-
     ing Without Loop Unrolling. In ASE. ACM, 1395–1407.
[22] Narges Shadab, Pritam M. Gharat, Shrey Tiwari, Michael D. Ernst,
     Martin Kellogg, Shuvendu K. Lahiri, Akash Lal, and Manu Sridharan.
     2025. Lightweight and modular resource leak checking (extended
     version). Int. J. Softw. Tools Technol. Transf. 27, 2 (2025), 267–288.
[23] Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and Le Song. 2020.
     Code2Inv: A Deep Learning Framework for Program Verification. In
     CAV (2) (Lecture Notes in Computer Science, Vol. 12225). Springer, 151–
     164.
[24] Jean Souyris, Virginie Wiels, David Delmas, and Hervé Delseny. 2009.
     Formal Verification of Avionics Software Products. In FM (Lecture
     Notes in Computer Science, Vol. 5850). Springer, 532–546.
[25] Chengpeng Wang. 2025. Advances in AI-Powered Code Security: Next-
     Level Bug Detection. Technical Report.
[26] Zhongyi Wang, Linyu Yang, Mingshuai Chen, Yixuan Bu, Zhiyang Li,
     Qiuye Wang, Shengchao Qin, Xiao Yi, and Jianwei Yin. 2024. Parf:
     Adaptive Parameter Refining for Abstract Interpretation. In ASE. ACM,
     1082–1093.
[27] Westley Weimer and George C. Necula. 2004. Finding and preventing
     run-time error handling mistakes. In OOPSLA. ACM, 419–431.
[28] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda
     He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting
     Program Specification Synthesis by Large Language Models Using
     Static Analysis and Program Verification. In CAV (2) (Lecture Notes in
     Computer Science, Vol. 14682). Springer, 302–328.
[29] Guangyuan Wu, Weining Cao, Yuan Yao, Hengfeng Wei, Taolue Chen,
     and Xiaoxing Ma. 2024. LLM Meets Bounded Model Checking: Neuro-
     Symbolic Loop Invariant Inference. In ASE. ACM, 406–417.
[30] Haoze Wu, Clark W. Barrett, and Nina Narodytska. 2024. Lemur: Inte-
     grating Large Language Models in Automated Program Verification.
     In ICLR. OpenReview.net.
[31] Mingwei Zheng, Danning Xie, Qingkai Shi, Chengpeng Wang, and
     Xiangyu Zhang. 2025. Validating Network Protocol Parsers with
     Traceable RFC Document Interpretation. Proc. ACM Softw. Eng. 2,
     ISSTA, Article ISSTA078 (June 2025), 23 pages.
