                                         Natural Synthesis: Outperforming Reactive Synthesis
                                                 Tools with Large Reasoning Models


                                                    Frederik Schmitt1 Matthias Cosler1 Niklas Metzger1 Julian Siber1
                                                      Vladimir Krsmanović1 Mohamed Ghanem1 Bernd Finkbeiner1,2
                                                1
                                                  CISPA Helmholtz Center for Information Security 2 Technical University of Munich
                                                                        firstname.lastname@cispa.de
arXiv:2605.15131v1 [cs.LG] 14 May 2026




                                                                                          Abstract

                                                     Reactive synthesis, the problem of automatically constructing a hardware circuit
                                                     from a logical specification, is a long-standing challenge in formal verification. It is
                                                     elusive for two reasons: It is algorithmically hard, and writing formal specifications
                                                     by hand is notoriously difficult. In this paper, we tackle both sides of the problem.
                                                     For the algorithmic side, we present a neuro-symbolic approach to reactive synthe-
                                                     sis that couples large reasoning models with model checkers to iteratively repair a
                                                     synthesized Verilog implementation via sound symbolic feedback. Our approach
                                                     solves more benchmarks than the best dedicated tools in the annual synthesis com-
                                                     petition and extends to constructing parameterized systems, a problem known to be
                                                     undecidable. On the specification side, we introduce an autoformalization step that
                                                     shifts the specification task from temporal logic to natural language by introducing
                                                     a hand-authored dataset of natural-language specifications for evaluation. We
                                                     demonstrate performance comparable to that of starting from formal specifications,
                                                     establishing natural synthesis as a viable end-to-end workflow.


                                         1    Introduction
                                         Correctness assurance accounts for a significant portion of the hardware design process [Harry
                                         Foster, 2022], yet it is indispensable, as bugs in hardware cannot be patched after production. The
                                         go-to solutions in the hardware industry are based on testing [Trippel et al., 2022] and formal
                                         verification [Clarke et al., 2018]. Testing checks whether sampled executions from a given system
                                         design conform to the system specification, while formal verification mathematically proves that
                                         all executions are conformant. Both methods require manual drafting of the design and manual
                                         bug-fixing if the draft fails the correctness checks. In contrast, these labor-intensive steps are cut out
                                         completely by reactive synthesis, an approach that directly generates a correct design from a given
                                         formal specification. Designers can then focus on specifying what a system should do, rather than
                                         how the system should do it.
                                         Significant research has been invested into reactive synthesis algorithms and tools, but despite its
                                         alluring promise of increased design quality and decreased development costs, it has seen only limited
                                         adoption by industry [Bloem et al., 2007]. To a large degree, this can be attributed to its reputation as
                                         a theoretical problem of high computational complexity (it is 2-EXPTIME-complete for linear-time
                                         temporal logic as shown by Pnueli and Rosner [1989]) and the absence of dedicated tools that scale
                                         to industrial-sized systems. Recently, however, inquiries into neural models for reactive synthesis
                                         have shown that this algorithmic cost can be avoided in many cases [Schmitt et al., 2021, Cosler
                                         et al., 2023b]. These neuro-symbolic approaches build on the idea of a guess-and-check loop: Neural
                                         models generate a candidate design, which is subsequently verified by a symbolic model-checking
                                         procedure, i.e., an exhaustive verification algorithm that returns a counterexample if the design does
                                         not satisfy the specification.

                                         Preprint.
 1   GLOBAL {                                                      1   module solution (
 2     PARAMETERS { n = 27; }                                      2       input clk ,
 3   }                                                             3       input [26:0] finished ,
 4   MAIN {                                                        4       output allFinished ) ;
 5     INPUTS { finished [ n ]; }                                  5       reg [26:0] seen = 27 ’ b0 ;
 6     OUTPUTS { allFinished ; }                                   6       wire [26:0] next ;
 7     INITIALLY {                                                 7       wire complete ;
 8       && [0 ≤ i < n ](¬allFinished W                            8       assign next = seen | finished ;
 9                       finished [ i ]) ;                         9       assign complete = & next ;
10       }                                                      10         assign allFinished = complete ;
11     ASSERT {                                                 11         always @ ( posedge clk ) begin
12       G ¬allFinished                                         12             if ( complete ) begin
13          → || [0 ≤ i < n ] G ¬finished [ i ];                13                  seen <= 27 ’ b0 ;
14       && [0 ≤ i < n ] ( allFinished →                        14             end else begin
15          X (¬allFinished W                                   15                  seen <= next ;
16              finished [ i ]) ) ;}                            16             end
17   }                                                          17         end
18                                                              18     endmodule



      NL Specification: The system receives input signals of n clients given as a bitvector finished of length n
      and provides a single-bit output called allFinished. This output must only be enabled after all clients have
      set their respective input in finished since the last time allFinished has been enabled. Moreover, in all
      cycles, the output must be enabled in the current or a future cycle if all clients set their respective input in the
      current or in a future cycle. The parameter n must be set to 27.


     Figure 1: We show an example temporal specification in TLSF format for a completion detector in the
     upper left. A synthesized Verilog implementation for the specification is provided in the upper right.
     At the bottom, we show a natural language specification that can be used as input to our approach.


     In this paper, we study the capabilities of Large Reasoning Models (LRMs) for the reactive synthe-
     sis problem. We show that, already out-of-the-box, modern LRMs partially outperform dedicated
     tools for reactive synthesis on the problems of the annual competition on reactive synthesis SYNT-
     COMP [Jacobs et al., 2024]. We propose a method that significantly widens this gap by exploiting
     the feedback generated in a guess-and-check loop: By using the counterexample generated by the
     model checker as an input in the subsequent reasoning step, we improve the performance of LRMs
     and solve 92% of the SYNTCOMP benchmarks, compared to 82% for the best symbolic tools.
     As input, our approach takes synthesis problems in the Temporal Logic Synthesis Format (TLSF), also
     used in SYNTCOMP. Such a problem may look like the example depicted in the upper left of Figure 1.
     This TLSF specification describes a completion detector, which receives signals of 27 clients via
     the input bit-vector finished and produces the output allFinished when all clients have sent an
     input at least once since the last time the output was set. The TLSF specification explicitly specifies
     inputs and outputs, as well as an initial condition (via INITIALLY) and an invariant (via ASSERT).
     The specification is parameterized, i.e., the number of clients can be easily adjusted by changing
     the parameter n, and classic synthesis approaches then generate a design for a fixed parameter. The
     designs produced by our synthesis approach are given in the high-level hardware description language
     Verilog as shown in the upper right of Figure 1. Verilog [IEEE, 2006] is an industry standard for the
     development of hardware designs and facilitates translation of a design to physical hardware. There
     is also extensive tool support that allows us to model-check the generated Verilog code against the
     original TLSF specification to obtain feedback for the LRM in case of an incorrect generation.
     The strong performance of the LRM approach on classic reactive synthesis problems motivates us to
     tackle problems that are traditionally considered out of reach for algorithmic approaches, but would
     be of high practical significance if solved. First, we consider the parameterized synthesis [Jacobs
     and Bloem, 2014] problem, which asks for a system design that is independent of the exact number
     of processes and can be instantiated with the parameter n after synthesis (cf. the parameter n in
     Figure 1). Parameterized synthesis is known to be undecidable, but it would help in speeding up
     the development process by generating hardware designs that are independent of changing physical
     constraints. We show that our approach can largely generalize the reasoning from fixed parameter


                                                               2
values to parameterized synthesis by evaluating on a subset of the SYNTCOMP data with the task
of generating parameterized implementations. Second, we consider the problem of generating
Verilog code from specifications given in natural language, as shown at the bottom of Figure 1.
Such synthesis from natural language may help in the challenging and time-consuming step of
formalizing the system specification in a logic like TLSF. We show that our approach based on LRMs
is remarkably successful at synthesizing Verilog code straight from natural language. Moreover,
if desired, the approach can also first generate a formal specification before moving on to reactive
synthesis. This allows designers to check the autoformalization process or verify the generated system
against this specification.
A brief summary of our contributions and outline of the paper:

      1. We combine Large Reasoning Models with feedback from formal verification tools to
         generate provably correct hardware circuits from temporal-logic specifications. This
         counterexample-guided LRM approach (CEX-LRM) clearly outperforms state-of-the-art
         symbolic synthesis on standardized competition benchmarks (Section 3).

      2. We apply CEX-LRM to parameterized synthesis, an undecidable problem where a system de-
         sign must be able to handle an arbitrary number of clients. Despite the increased complexity,
         our approach performs almost equally well as in the non-parameterized case (Section 4).

      3. We extend CEX-LRM to handle natural-language specifications and evaluate it on a new,
         handcrafted dataset. Our natural synthesis approach can first return an autoformalized
         specification for inspection, but also directly synthesize a design starting from natural
         language. We show that even when handicapped in this way, natural synthesis can solve
         challenging benchmarks out of scope for purely symbolic methods (Section 5).


2   Background

Reactive synthesis [Church, 1957] is a core problem in theoretical computer science, with foundational
solutions dating back to the 1960s [Buchi and Landweber, 1969]. A common formulation is synthesis
from temporal specifications, e.g., linear-time temporal logic (LTL) [Pnueli, 1977], where the
objective is to construct a finite-state system that satisfies a given LTL formula φ. Due to this
sound-by-construction approach, reactive synthesis has the potential to revolutionize hardware
design, rendering manual implementation superfluous. LTL augments propositional logic (operators
¬, ∧, ∨, →) with temporal operators such as X (next), U (until), G (always), and (eventually),
enabling the specification of behaviors for systems that continuously interact with an environment.
For more concise specifications and to express parameterized synthesis problems, LTL is usually
substituted by the Temporal Logic Synthesis Format (TLSF) in practice. TLSF allows convenient
constructs such as parameter declarations (cf. line 2 in the top left part of Figure 1), succinct operators
defined over ranges (cf. line 13 in the top left part of Figure 1), and function definitions. For a fixed
parameter, a TLSF specification can be compiled down to explicit LTL.
Implementations are usually modeled as sequential circuits C that translate infinite streams of inputs
into infinite streams of outputs. A circuit satisfies a formula, denoted by C ⊨ φ, if all executions
σ of the circuit satisfy the formula φ. If C ⊭ φ, then there also exists a counterexample execution
σ of C that violates φ. We use Verilog [IEEE, 2006] for synthesizing hardware implementations,
a hardware description language that allows us to stay at the register-transfer level rather than
the gate level. Verilog can directly be compiled into standard circuit representations [Wolf et al.,
2013] and model-checked against temporal properties [Cavada et al., 2014]. Techniques for reactive
synthesis for circuits are typically split into game-based approaches [Bloem et al., 2018] and bounded
synthesis methods [Faymonville et al., 2017], and all must cope with the problem’s 2-EXPTIME-
completeness [Pnueli and Rosner, 1989]. State-of-the-art tools such as Strix [Meyer et al., 2018]
and ltlsynt [Renkin et al., 2022] rely on traditional automata and game-solving algorithms, whereas
recent approaches started utilizing neural methods, either as a part of heuristic search methods in
SemML [Kretínský et al., 2025] or for end-to-end generation [Schmitt et al., 2021, Cosler et al., 2024,
2023b].


                                                    3
3     Counterexample-Guided Synthesis with Large Reasoning Models

In this section, we consider the classical reactive synthesis problem: given a formal logic specification
φ, find a system that either satisfies the specification or prove that no such system exists. We
adopt the evaluation setting of SYNTCOMP, which represents the cumulative result of decades of
research on this problem and therefore provides a strong baseline for our experiments. Our approach
implements two fundamental changes to synthesis algorithms: We use Large Reasoning Models to
synthesize implementations in hardware description language and introduce a feedback loop via
sound model-checking algorithms.

3.1    Dataset

We collected all benchmarks from the LTL synthesis track of the reactive synthesis competition 2025
(SYNTCOMP 2025).1 The total of 1586 specifications are expressed in the Temporal Logic Synthesis
Format (TLSF) [Jacobs et al., 2023]. We strip the specification of all comments, descriptions, and
their names to avoid any hints on how to solve the specification or on its realizability. Of the 1586
specifications, 458 are known to be realizable, and 419 are known to be unrealizable based on
metadata provided by the competition. For the remaining specifications, the status of realizability
remains unknown. In the competition, tools are given 60 minutes and 160 GB of memory to solve
a single instance. The 2025 competition was won by ltlsynt [Renkin et al., 2022] with 1297
instances solved, closely followed by SemML [Kretínský et al., 2025] with 1295 instances solved.

3.2    Method

We begin with prompting a reasoning model to emit a Verilog
module for a given specification in TLSF format. While most
reactive synthesis approaches encode the problem to an infinite                              TLSF spec φ
game, e.g., a parity game [Zielonka, 1998], we intentionally stay
at a high abstraction level for both specification and implementa-
tion. Rather than translating the TLSF specification into a pure                                 LRM
LTL formula or a Büchi automaton, we feed it directly into the
LRM, preserving its programmatic structure. Similarly, on the
implementation side, we do not construct a gate-level implemen-                                                CEX
                                                                                          Verilog module M
tation but stay on the register-transfer level and instruct the LRM                                            repair
to generate a Verilog module. The succinct representations are a
key aspect of our method, allowing the LRM to use more of the
reasoning context window to iterate and refine solutions rather                             Model checker
than simply representing the specification and implementation.                                        M |= φ
Note that Verilog is a suitable target language, as it can be model-
checked against LTL with Yosys [Wolf et al., 2013].2 We handle                                 ✓ verified
both realizable and unrealizable specifications by instructing
the model to either generate a Verilog module satisfying the                        Figure 2: LRM-based synthesis
specification or to produce a Verilog module serving as an en-                      loop: the model is prompted with
vironment strategy that proves the specification is unrealizable.                   the TLSF spec and emits a Verilog
In the prompt, we further add constraints on the Verilog code,                      module, which is model-checked
the clock signal, and the overall format to simplify module ex-                     against the same spec; counterex-
traction and support our model-checking workflow, as detailed                       amples are returned for repair.
below. We refer to Appendix A.1 for the full prompt.
The Verilog module generated by the LRM is not correct by construction. However, we can automati-
cally verify the implementation against the input specification by adding a model-checking step after
inference. The model checker then either proves correctness or constructs a counterexample trace
that is an execution of the Verilog module but violates the specification. In the latter case, we provide
the counterexample to the LRM as feedback together with an instruction to repair the module. This
loop is grounded in sound symbolic feedback and adds to the LRM’s unsound reasoning capabilities.
In our experiments, we repeat this process using the model-checking pipeline detailed below.
    1 https://github.com/SYNTCOMP/benchmarks
    2 This only holds for a fragment of Verilog. However, this fragment is sufficient for LTL synthesis.




                                                               4
To automatically verify a Verilog module against a TLSF specification, we rely on the nuXmv model
checker [Cavada et al., 2014] and invoke the IC3 routine [Bradley, 2011]. Additionally, we have
implemented a decomposition of the specification to make the problem manageable and to provide
fine-grained feedback on violated sub-specifications to the LRM (see Appendix A.5 for details). We
prepare problems by translating the Verilog module into an AIGER representation with Yosys [Wolf
et al., 2013] and then translating the AIGER representation into the model checker’s input format
with aigtosmv [Biere, 2007]. The full translation script for Yosys and the model checking script for
nuXmv are given in Appendix A.3. We run the model checker on an Intel Emerald Rapids machine
with a 32 GB memory limit and a timeout of 600 seconds.

3.3   Results

We evaluated our method on the synthesis competition benchmarks with the LRMs Gemini 3.1
Pro [Google, 2026] and GPT-5.5 [OpenAI, 2026]. We configured both models with their highest
possible reasoning setting (HIGH for Gemini 3.1 Pro and XHIGH for GPT-5.5). As baselines, we
compare with the winner of the 2025 synthesis competition ltlsynt [Renkin et al., 2022] and the
runner-up SemML [Kretínský et al., 2025]. Additionally, we compare against the results of Egolf
et al. [2026]; however, we note the substantial differences with respect to realizability, hardware
representations, and counterexample-guidance.
We present the overall results in Table 1. Both LRMs clearly outperform state-of-the-art reactive
synthesis tools, with GPT-5.5 performing best and solving 170 more instances than the winner of
the reactive synthesis competition. The results show that the models benefit from sound feedback
from a verification tool. The effect is most pronounced for the Gemini model, with 162 additional
instances solved after including the counterexamples provided by the model checker. In contrast
with Egolf et al. [2026], we arrive at a different conclusion on how LRMs can support solving
reactive synthesis problems as a result of including unrealizable specifications, generating Verilog,
providing counterexamples, and using higher reasoning budgets. With respect to realizability in
particular, further inspection of the results reveals that our method handles realizable and unrealizable
specifications equally well. For example, the 1392 specifications solved by GPT-5.5 split into 640
realizable and 752 unrealizable specifications.
In an ablation study, we evaluated how much each LRM’s reasoning token budget contributed to
finding correct solutions to the synthesis problems. We compared the different configurations for
controlling the number of reasoning tokens that each model provides. In Figure 3, we plot for each
configuration the number of solved instances and the corresponding average number of reasoning
tokens spent. For a full overview of the numbers, we refer to Table 5 in Appendix A.4. We observe
a clear trend: increased reasoning token budgets are associated with a higher number of solved
instances. More specifically, the trend is log-linear for each model, suggesting diminishing returns
for very high reasoning budgets. GPT-5.5 additionally supports a configuration with no reasoning
tokens at all. In that case, the number of solved instances drops sharply to 123. Based on these
results, we can attribute the ability to find correct solutions to synthesis problems largely to advances
in reasoning models and to the number of reasoning tokens that are spent.


Table 1: Reactive synthesis results for competition benchmarks: comparing LRMs with algorithms
ltlsynt and SemML. LRMs were run with their highest reasoning configurations.

           Type          Name                                CEX Iterations        Solved
                         SemML [Kretínský et al., 2025]                          1295 / 1586
           Algorithm
                         ltlsynt [Renkin et al., 2022]                           1297 / 1586
                         GPT-5 [Egolf et al., 2026]                               229 / 1586
                                                                    0            1193 / 1586
                         Gemini 3.1 Pro                             1            1311 / 1586
           LRM
                                                                    2            1355 / 1586
                                                                    0            1392 / 1586
                         GPT-5.5                                    1            1449 / 1586
                                                                    2           1467 / 1586


                                                   5
                         1,500




      Solved instances
                                                                  HIGH XHIGH           HIGH
                                                      MEDIUM
                         1,000                         MEDIUM

                                 LOW
                                  LOW
                                                                           Gemini 3.1 Pro
                                                                           GPT-5.5
                          500
                                 103                                             104
                                        Average use of reasoning tokens (log scale)

Figure 3: Solved instances on SYNTCOMP vs. average reasoning tokens, with per-model linear fit.


4     Reactive Synthesis Beyond Decidability

The previous experiments showed that the natural synthesis framework outperforms existing symbolic
tools for LTL synthesis. In this section, we show that Large Reasoning Models can lift the problem
to the next level: we synthesize Verilog modules for LTL formulas with variable numbers of input
and output variables, as well as variable numbers of operator sequences. This elevates the task to the
undecidable problem of parameterized synthesis [Jacobs and Bloem, 2014], yet the LRM can still
synthesize correct parameterized Verilog implementations.
Parameterized synthesis generalizes the classical reactive synthesis problem: given a specification
parameterized in the number of processes, find an implementation template whose instantiations
satisfy the specification regardless of the number of processes or prove that no such template
exists. Importantly, the generalization makes the synthesis problem computationally much more
challenging. In fact, for linear-time temporal logic, the generalization turns the problem into an
undecidable problem [Jacobs and Bloem, 2014]. Yet, finding reusable and configurable, parameterized
implementations is of great interest to practitioners. Consider, for example, the detector in Figure 1.
Ideally, we want the implementation to be independent of the number of clients and to work correctly
for an arbitrary number. Verilog directly supports such generalizations, for example through parameter
declarations in the module’s header list. In Figure 7 in Appendix B we show the parameterized
version of the detector. In the following, we present how our approach can be directly extended to
find such parameterized implementations.

4.1        Dataset

The synthesis competition benchmarks introduced in Section 3.1 already contain many specifications
that are equivalent up to a parameter value. The detector benchmark shown in Figure 1 is an
example of such a specification. In addition to parameter value n = 27, it is contained in the
competition benchmarks for nine smaller parameter values. To evaluate our parameterized synthesis
approach, we identify such benchmarks and derive a dataset of 57 general parameterized specifications.
Similar to the competition benchmarks themselves we post-process them by removing all comments,
descriptions, and names to avoid any hints on how to solve the specification.

4.2        Method

Our method generally follows the method described for reactive synthesis in Section 3. We modify the
LRM instruction to generate a parameterized Verilog implementation with a parameter declaration in
the Verilog module’s header list. Importantly, we can no longer automatically verify the parameterized
implementation since the parameterized LTL verification is undecidable similar to the synthesis
problem [Bloem et al., 2015]. We therefore resort to testing different parameter values and verify
for each value the instantiated Verilog module against the instantiated specification similar to the
reactive synthesis case. We test up to the largest parameter value found in the synthesis competition
for the respective specification class. In case we find a violation for one parameter value, we still
obtain a sound counterexample that we provide to the LRM as feedback. However, we can no longer
guarantee correctness in the positive case.


                                                          6
Table 2: Parameterized synthesis results for Gemini 3.1 Pro and GPT-5.5. We report the average
over three runs with standard deviation.
                                 Name                        Solved
                                 Gemini 3.1 Pro         35.0 ± 1.0 / 57
                                 + CE-Guidance          38.3 ± 1.1 / 57
                                 GPT-5.5                 35.7 ± 2.5 / 57
                                 + CE-Guidance           35.7 ± 2.5 / 57


4.3   Results

As a consequence of the undecidability of the problem, tools and algorithms for solving parameterized
synthesis problems are scarce. To the best of our knowledge, no tool exists that is mature enough to
serve as a baseline for the problem set introduced above. We therefore only evaluate our approach
without a baseline comparison in this section. We use Gemini 3.1 Pro [Google, 2026] and GPT-
5.5 [OpenAI, 2026] configured with their highest possible reasoning settings. The results for both
models are presented in Table 2. With an average of 35 instances solved, both models perform on
par. However, the Gemini model benefits more from additional verification feedback, solving up to
38 instances. Further, the task of finding a parameterized implementation seems only moderately
harder for the LRMs than finding an implementation for a specific parameter value. For comparison,
the Gemini model solves 38 instances, and the GPT model 41, on average, when instantiating the
problems with the largest parameter value found in the synthesis competition (See Appendix A.2).

5     Reactive Synthesis Beyond Temporal Logic
Writing formal specifications in temporal logic is notori-
ously difficult and requires expertise in formal verification.              NL description
Describing a system’s desired behavior in natural language
is often more intuitive and accessible, but out of scope for
symbolic algorithms. With Large Reasoning Models, we                            LRM
                                                                 syntax
can now address the entire reactive-synthesis pipeline –          repair                      direct
from informal requirements to formal temporal-logic spec-
                                                                             TLSF spec φ̂
ifications to verified implementations – end-to-end. We
manually authored a dataset of natural language specifi-
cations on which we perform natural synthesis with two
                                                                                LRM
approaches: 1) We autoformalize the natural language
specification into a formal specification in TLSF format
and then synthesize a Verilog module from the formal                       Verilog module M
specification (as in Section 3). 2) We prompt the LRM
to directly synthesize a Verilog module from the natural
language specification. We verify against both the correct,
manually crafted specification, and the autoformalization,                  Model checker
and measure the correctness of the autoformalization step.                          M |= φ̂
                                                                              ✓ verified
5.1   Dataset
                                                             Figure 4: The autoformalization route
Based on the dataset introduced in Section 4.1, we man-
                                                             (solid) translates NL to TLSF φ̂, then
ually author a natural language description for each of
                                                             synthesizes Verilog. The direct route
the 57 parameterized specifications, which we call NAT-
                                                             (dashed) skips autoformalization. The
URAL. For this experiment, we built a challenging set of
                                                             module is verified against the autofor-
benchmarks by setting the parameter values to the largest
                                                             malized specification.
values occurring in SYNTCOMP. The best algorithmic
tools can synthesize only 19 of 57 formalized specifica-
tions, whereas the presented approach with LRMs (Section 3) solves 38.3±0.6/57. See Appendix A.2
for more details. In this section, however, we focus on the natural language specifications. Because
the formal specifications of this dataset are already very challenging, it is a valuable testbed for
evaluating the performance of synthesis from natural-language specifications.


                                                    7
5.2   Results

We evaluate the full natural synthesis pipeline on the NATURAL dataset, comparing two routes:
autoformalization followed by LRM-based synthesis from these autoformalized specifications, and
direct end-to-end LRM-based synthesis from natural language. We further address the correctness of
the autoformalization step and its impact on synthesis performance. We verify the generated Verilog
modules against both the ground truth specifications and an autoformalized specification to isolate the
effects of potential semantic shifts during autoformalization. Table 3 summarizes the results. Both
approaches solve roughly 30 out of 57 specifications against the ground truth, demonstrating that
LRMs can produce provably correct hardware directly from informal descriptions.

Autoformalization. We autoformalize each natural language specification into TLSF by prompting
the LRM with a structured template that includes the full TLSF grammar, key conventions for
parameterized signals, and LTL operators. The LRM obtains sound feedback on the syntax of the
produced specification in a feedback loop. Since autoformalization is a challenging task, we find that
the LRM cannot always produce a syntactically correct TLSF specification within three attempts
(12.7 ± 0.5/57). We then use Spot’s [Duret-Lutz et al., 2022] ltlfilt to check for equivalence with
the ground truth specification. 9.3 ± 0.6/57 are proven equivalent, while 8.7 ± 0.6/57 are provably
inequivalent. Note that, because the specifications in NATURAL are designed to be challenging, the
automata-based equivalence check limits our evaluation (26.3 ± 0.9/57 timed out after 30 minutes,
32GB per specification). Autoformalization accuracies need careful evaluation: syntactically incorrect
specifications are often close to the intended behavior and can still yield correct results via natural
synthesis. In fact, several specifications with syntactically broken autoformalizations still led to
correct Verilog modules in subsequent experiments, indicating that the underlying semantic intent
is largely preserved. Additionally, specifications that are inequivalent to the ground truth are not
necessarily incorrect, since natural language descriptions can be ambiguous and underspecified,
possibly leading to sound strengthening of the specification.

Natural Synthesis via Autoformalized Specifications. To complete the pipeline, we synthesize
a Verilog module from the autoformalized specification with the same method as in Section 3. We
find that the syntax repair loop can introduce a semantic shift, as the LRM then focuses on syntactic
correctness rather than the specification’s semantics. At the same time, during synthesis, the LRM can
handle (or rather ignore) syntax errors in the generated TLSF specifications and still produce correct
Verilog modules. We therefore use the first-try autoformalized specification for synthesis, even if it
contains syntax errors. We verify the generated module against the autoformalized specification. Here,
the syntax-repaired specifications become advantageous, since syntactic errors in the specification
would cause verification to fail outright. To test our method and isolate the potential semantic shift,
we also verify the generated module against the ground-truth specification. The results are shown in
Table 3. We find 30 out of 57 specifications to satisfy the ground truth, meaning they are provably
correct. 33.7 ± 1.7 out of 57 specifications satisfy the autoformalized specification, with a high
number of 25.7 ± 0.6 satisfying both the ground truth and the autoformalized specification, indicating
that the autoformalization step is often precise enough to specify the intended behavior fully, and a
semantic shift is not a dominant issue.

End-to-End Natural Synthesis. As an alternative to the autoformalization route, we prompt the
LRM to directly synthesize a Verilog module from the natural language description, bypassing
the intermediate TLSF specification. We verify the generated module against an autoformalized

Table 3: Reactive synthesis from natural language on the manually authored dataset NATURAL. We
report the mean over three runs with standard deviation. All experiments are run with Gemini 3.1 Pro
and reasoning level high.

                    Approach                   Verified against       Solved
                                               ground truth       30.0 ± 0.0 / 57
                    Via Autoformalization
                                               autoformalized     33.7 ± 1.7 / 57
                                               ground truth       31.7 ± 1.2 / 57
                    End-to-End
                                               autoformalized     30.7 ± 1.9 / 57


                                                  8
specification from the previous experiment, and against the ground truth specification to isolate
the effect of potential semantic shifts in the autoformalization step. The direct approach solves
31.7 ± 1.2 out of 57 specifications against the ground truth (Table 3), slightly outperforming the
autoformalization route (30.0 ± 0.0). In contrast to the autoformalized specification, the direct
approach solves slightly fewer instances (30.7 ± 1.9), since the Verilog module was synthesized
independently of it. These results suggest that the intermediate formalization step does not provide a
significant advantage for synthesis on this dataset. We suspect that the specific format of TLSF adds
to the complexity. Since these models reason in natural language, staying in this modality as long as
possible is likely beneficial. Nevertheless, the performance difference between the two approaches
is small. Most importantly, generating a formal specification as an intermediate step is helpful and
necessary for interpretability during hardware engineering, enabling specification refinement (e.g.,
resolving ambiguity, correcting errors) and formal verification.


6   Related Work

Deep Learning for Hardware Design. Deep learning methods have been applied to many aspects
of the hardware design process. For formal verification, deep neural networks have been used as
proof certificates in the form of neural ranking functions [Giacobbe et al., 2024]. For optimization,
deep reinforcement learning has been applied to abstraction levels ranging from Boolean circuit
minimization [Chowdhury et al., 2024, Wang et al., 2024] to floorplanning [Mirhoseini et al., 2021].
Similarly, research on representation learning ranges from Boolean circuits [Neto et al., 2021,
Zheng et al., 2025] to register-transfer-level abstractions [Vasudevan et al., 2021]. For hardware
description languages in particular, language-modeling techniques were explored both for the Verilog
language [Thakur et al., 2024, Zhu et al., 2025] and for the translation from natural language to
Verilog [Pearce et al., 2020]. The reactive synthesis problem itself has been studied as a deep learning
translation from LTL to gate-level circuits [Schmitt et al., 2021, Cosler et al., 2023b] and combined
with symbolic solvers in a neural-symbolic portfolio solver [Cosler et al., 2024]. Closest to our
work are Egolf et al. [2026], who compare LRMs with limited reasoning against symbolic synthesis
tools on the task of synthesizing realizable LTL specifications to gate-level circuits, not a hardware
description language like Verilog that operates at the register-transfer level.

Autoformalization with LLMs. Autoformalization is the task of translating informal, natural
language into a formal logic or formal mathematical statement. Recently, it has been extensively
studied in theorem proving with progress driven by Large Language Models (LLMs) [Wu et al., 2022,
Jiang et al., 2023, Murphy et al., 2024a, Jana et al., 2025]. Closely related to theorem proving, it has
proven to be a crucial component of AI systems that perform well in math competitions [Hubert et al.,
2025]. Similar to the developments in formal mathematics, LLMs have fueled research in autofor-
malization in formal verification. For temporal logic specifically, the formalization of unstructured
natural language into LTL formulas has been studied as an end-to-end translation task [Fuggitti and
Chakraborti, 2023, Chen et al., 2023, Liu et al., 2023], via the composition of sub-translations [Cosler
et al., 2023a, Mendoza et al., 2024], via separation of data and control [Murphy et al., 2024b], and
constrained decoding [English et al., 2025]. The recently introduced VerifyThisBench targets the
translation of natural language into formal specifications for program verification [Deng et al., 2025].


7   Conclusion

We introduced natural synthesis, a neuro-symbolic approach to reactive synthesis that combines Large
Reasoning Models with counterexample-guided reasoning. Our pipeline substantially outperforms
purely symbolic approaches on SYNTCOMP benchmarks, extends to parameterized (undecidable)
synthesis, and supports synthesis from natural-language descriptions through autoformalization and
direct circuit generation, all verified against temporal specifications. These results highlight the
potential of neuro-symbolic methods to bring reactive synthesis into real-world hardware design
workflows. These promising observations motivate concrete next steps: creating new synthesis
benchmarks based on natural-language hardware specifications to better capture practical use cases,
and developing scalable, potentially neuro-symbolic, hardware verification techniques to overcome
model-checking bottlenecks.


                                                   9
Acknowledgments and Disclosure of Funding
This work was partially supported by the European Union with ERC Grant HYPER (No. 101055412).
Views and opinions expressed are however those of the authors only and do not necessarily reflect
those of the European Union or the European Research Council Executive Agency. Neither the
European Union nor the granting authority can be held responsible for them.

References
A. Biere. The AIGER and-inverter graph (AIG) format version 20071012. FMV Reports Series,
  Institute for Formal Models and Verification, Johannes Kepler University, Altenbergerstr, 69:4040,
  2007.

R. Bloem, S. J. Galler, B. Jobstmann, N. Piterman, A. Pnueli, and M. Weiglhofer. Interactive
  presentation: Automatic hardware synthesis from specifications: a case study. In R. Lauwereins
  and J. Madsen, editors, 2007 Design, Automation and Test in Europe Conference and Exposition,
  DATE 2007, Nice, France, April 16-20, 2007, pages 1188–1193. EDA Consortium, San Jose, CA,
  USA, 2007. URL https://dl.acm.org/citation.cfm?id=1266622.

R. Bloem, S. Jacobs, A. Khalimov, I. Konnov, S. Rubin, H. Veith, and J. Widder. Decidability of
  Parameterized Verification. Synthesis Lectures on Distributed Computing Theory. Morgan & Clay-
  pool Publishers, 2015. ISBN 978-3-031-00883-2. doi: 10.2200/S00658ED1V01Y201508DCT013.
  URL https://doi.org/10.2200/S00658ED1V01Y201508DCT013.

R. Bloem, K. Chatterjee, and B. Jobstmann. Graph games and reactive synthesis. In E. M. Clarke,
  T. A. Henzinger, H. Veith, and R. Bloem, editors, Handbook of Model Checking, pages 921–962.
  Springer, 2018. doi: 10.1007/978-3-319-10575-8\_27. URL https://doi.org/10.1007/
  978-3-319-10575-8_27.

A. R. Bradley. Sat-based model checking without unrolling. In R. Jhala and D. A. Schmidt,
  editors, Verification, Model Checking, and Abstract Interpretation - 12th International Conference,
  VMCAI 2011, Austin, TX, USA, January 23-25, 2011. Proceedings, Lecture Notes in Computer
  Science, pages 70–87. Springer, 2011. doi: 10.1007/978-3-642-18275-4\_7. URL https:
  //doi.org/10.1007/978-3-642-18275-4_7.

J. R. Buchi and L. H. Landweber. Solving sequential conditions by finite-state strategies. Trans-
   actions of the American Mathematical Society, 138:295–311, 1969. URL https://api.
   semanticscholar.org/CorpusID:4568478.

R. Cavada, A. Cimatti, M. Dorigatti, A. Griggio, A. Mariotti, A. Micheli, S. Mover, M. Roveri, and
  S. Tonetta. The nuxmv symbolic model checker. In A. Biere and R. Bloem, editors, Computer
  Aided Verification - 26th International Conference, CAV 2014, Held as Part of the Vienna Summer
  of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings, Lecture Notes in Computer
  Science, pages 334–342. Springer, 2014. doi: 10.1007/978-3-319-08867-9\_22. URL https:
  //doi.org/10.1007/978-3-319-08867-9_22.

Y. Chen, R. Gandhi, Y. Zhang, and C. Fan. NL2TL: transforming natural languages to temporal
  logics using large language models. In H. Bouamor, J. Pino, and K. Bali, editors, Proceedings
  of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023,
  Singapore, December 6-10, 2023, pages 15880–15903. Association for Computational Linguistics,
  2023. doi: 10.18653/V1/2023.EMNLP-MAIN.985. URL https://doi.org/10.18653/v1/
  2023.emnlp-main.985.

A. B. Chowdhury, M. Romanelli, B. Tan, R. Karri, and S. Garg. Retrieval-guided reinforcement
  learning for boolean circuit minimization. In The Twelfth International Conference on Learning
  Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. URL
  https://openreview.net/forum?id=0t1O8ziRZp.

A. Church. Applications of recursive arithmetic to the problem of circuit synthesis. In Summaries of
  the Summer Institute of Symbolic Logic, volume 1, pages 3–50. Cornell Univ., Ithaca, NY, 1957.


                                                10
E. M. Clarke, O. Grumberg, D. Kroening, D. A. Peled, and H. Veith. Model checking, 2nd Edi-
  tion. MIT Press, 2018. ISBN 978-0-262-03883-6. URL https://mitpress.mit.edu/books/
  model-checking-second-edition.
M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel. nl2spec: Interactively translating
 unstructured natural language to temporal logics with large language models. In C. Enea and
 A. Lal, editors, Computer Aided Verification - 35th International Conference, CAV 2023, Paris,
 France, July 17-22, 2023, Proceedings, Part II, Lecture Notes in Computer Science, pages 383–396.
 Springer, 2023a. doi: 10.1007/978-3-031-37703-7\_18. URL https://doi.org/10.1007/
 978-3-031-37703-7_18.
M. Cosler, F. Schmitt, C. Hahn, and B. Finkbeiner. Iterative circuit repair against formal specifica-
 tions. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali,
 Rwanda, May 1-5, 2023. OpenReview.net, 2023b. URL https://openreview.net/forum?id=
 SEcSahl0Ql.
M. Cosler, C. Hahn, A. Omar, and F. Schmitt. NeuroSynt: A Neuro-symbolic Portfolio Solver
 for Reactive Synthesis. In B. Finkbeiner and L. Kovács, editors, Tools and Algorithms for the
 Construction and Analysis of Systems, pages 45–67, Cham, 2024. Springer Nature Switzerland.
 ISBN 978-3-031-57256-2. doi: 10.1007/978-3-031-57256-2_3.
X. Deng, S. Zhong, A. G. Veneris, F. Long, and X. Si. Verifythisbench: Generating code, specifica-
  tions, and proofs all at once. CoRR, abs/2505.19271, 2025. doi: 10.48550/ARXIV.2505.19271.
  URL https://doi.org/10.48550/arXiv.2505.19271.
A. Duret-Lutz, E. Renault, M. Colange, F. Renkin, A. G. Aisse, P. Schlehuber-Caissier, T. Medioni,
  A. Martin, J. Dubois, C. Gillard, and H. Lauko. From spot 2.0 to spot 2.10: What’s new? In
  S. Shoham and Y. Vizel, editors, Computer Aided Verification - 34th International Conference,
  CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings, Part II, Lecture Notes in Computer
  Science, pages 174–187. Springer, 2022. doi: 10.1007/978-3-031-13188-2\_9. URL https:
  //doi.org/10.1007/978-3-031-13188-2_9.
D. Egolf, Y. Zhou, and S. Tripakis. Can llms perform synthesis? CoRR, abs/2603.20264, 2026. doi:
  10.48550/ARXIV.2603.20264. URL https://doi.org/10.48550/arXiv.2603.20264.
W. H. English, D. Simon, S. K. Jha, and R. Ewetz. Grammar-forced translation of natural language
  to temporal logic using llms. In A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp,
 T. Maharaj, K. Wagstaff, and J. Zhu, editors, Forty-second International Conference on Machine
 Learning, ICML 2025, Vancouver, BC, Canada, July 13-19, 2025, Proceedings of Machine Learning
  Research. PMLR / OpenReview.net, 2025. URL https://proceedings.mlr.press/v267/
  english25a.html.
P. Faymonville, B. Finkbeiner, and L. Tentrup. Bosy: An experimentation framework for bounded
   synthesis. In R. Majumdar and V. Kuncak, editors, Computer Aided Verification - 29th International
   Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part II, volume
   10427 of Lecture Notes in Computer Science, pages 325–332. Springer, 2017. doi: 10.1007/
   978-3-319-63390-9\_17. URL https://doi.org/10.1007/978-3-319-63390-9_17.
F. Fuggitti and T. Chakraborti. NL2LTL - a python package for converting natural language (NL)
   instructions to linear temporal logic (LTL) formulas. In B. Williams, Y. Chen, and J. Neville, editors,
   Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on
   Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Symposium on Educational
   Advances in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February 7-14, 2023,
   pages 16428–16430. AAAI Press, 2023. doi: 10.1609/AAAI.V37I13.27068. URL https:
   //doi.org/10.1609/aaai.v37i13.27068.
M. Giacobbe, D. Kroening, A. Pal, and M. Tautschnig. Neural model checking. In A. Glober-
 sons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, edi-
 tors, Advances in Neural Information Processing Systems 38: Annual Conference on Neu-
 ral Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, Decem-
 ber 10 - 15, 2024, 2024. URL http://papers.nips.cc/paper_files/paper/2024/hash/
 9d0947107ea92d6ce369dce7749180dd-Abstract-Conference.html.


                                                   11
Google. Gemini 3.1 Pro Preview, Feb. 2026.           URL https://deepmind.google/models/
  model-cards/gemini-3-1-pro/.

Harry Foster.  The 2022 Wilson research group functional verification study, 2022.
  URL          https://blogs.sw.siemens.com/verificationhorizons/2022/10/10/
  prologue-the-2022-wilson-research-group-functional-verification-study/.

T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser, A. Huang, J. Schrittwieser,
  Y. Schroecker, H. Masoom, O. Bertolli, T. Zahavy, A. Mandhane, J. Yung, I. Beloshapka, B. Ibarz,
   V. Veeriah, L. Yu, O. Nash, P. Lezeau, S. Mercuri, C. Sönne, B. Mehta, A. Davies, D. Zheng,
   F. Pedregosa, Y. Li, I. von Glehn, M. Rowland, S. Albanie, A. Velingker, S. Schmitt, E. Lockhart,
   H. Michalewski, N. Sonnerat, D. Hassabis, P. Kohli, and D. Silver. Olympiad-level formal
   mathematical reasoning with reinforcement learning. Nature, 2025. URL https://www.nature.
   com/articles/s41586-025-09833-y.

IEEE. Ieee standard for verilog hardware description language. IEEE Std 1364-2005 (Revision of
  IEEE Std 1364-2001), pages 1–590, 2006. doi: 10.1109/IEEESTD.2006.99495.

S. Jacobs and R. Bloem. Parameterized synthesis. Log. Methods Comput. Sci., 10(1), 2014. doi:
  10.2168/LMCS-10(1:12)2014. URL https://doi.org/10.2168/LMCS-10(1:12)2014.

S. Jacobs, G. A. Pérez, and P. Schlehuber-Caissier. The temporal logic synthesis format TLSF v1.2.
   CoRR, abs/2303.03839, 2023. doi: 10.48550/ARXIV.2303.03839. URL https://doi.org/10.
   48550/arXiv.2303.03839.

S. Jacobs, G. A. Pérez, R. Abraham, V. Bruyère, M. Cadilhac, M. Colange, C. Delfosse, T. van
   Dijk, A. Duret-Lutz, P. Faymonville, B. Finkbeiner, A. Khalimov, F. Klein, M. Luttenberger,
   K. J. Meyer, T. Michaud, A. Pommellet, F. Renkin, P. Schlehuber-Caissier, M. Sakr, S. Sick-
   ert, G. Staquet, C. Tamines, L. Tentrup, and A. Walker. The reactive synthesis competition
  (SYNTCOMP): 2018-2021. Int. J. Softw. Tools Technol. Transf., 26(5):551–567, 2024. doi:
  10.1007/S10009-024-00754-1. URL https://doi.org/10.1007/s10009-024-00754-1.

P. Jana, K. Kale, A. E. Tanriverdi, C. Song, S. Vishwanath, and V. Ganesh. Proofbridge:
   Auto-formalization of natural language proofs in lean via joint embeddings. arXiv preprint
   arXiv:2510.15681, 2025.

A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li, M. Jamnik, G. Lample, and Y. Wu.
  Draft, sketch, and prove: Guiding formal theorem provers with informal proofs. In The Eleventh
  International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5,
  2023. OpenReview.net, 2023. URL https://openreview.net/forum?id=SMa9EAovKMC.

J. Kretínský, T. Meggendorfer, M. Prokop, and A. Zarkhah. Semml: Enhancing automata-theoretic
   LTL synthesis with machine learning. In A. Gurfinkel and M. Heule, editors, Tools and Algorithms
   for the Construction and Analysis of Systems - 31st International Conference, TACAS 2025,
   Held as Part of the International Joint Conferences on Theory and Practice of Software, ETAPS
   2025, Hamilton, ON, Canada, May 3-8, 2025, Proceedings, Part I, Lecture Notes in Computer
   Science, pages 233–253. Springer, 2025. doi: 10.1007/978-3-031-90643-5\_12. URL https:
   //doi.org/10.1007/978-3-031-90643-5_12.

J. X. Liu, Z. Yang, I. Idrees, S. Liang, B. Schornstein, S. Tellex, and A. Shah. Grounding complex
   natural language commands for temporal tasks in unseen environments. In J. Tan, M. Toussaint,
   and K. Darvish, editors, Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta,
   GA, USA, Proceedings of Machine Learning Research, pages 1084–1110. PMLR, 2023. URL
   https://proceedings.mlr.press/v229/liu23d.html.

D. Mendoza, C. Hahn, and C. Trippel. Translating natural language to temporal logics with large
  language models and model checkers. In N. Narodytska and P. Rümmer, editors, Formal Methods
  in Computer-Aided Design, FMCAD 2024, Prague, Czech Republic, October 15-18, 2024, pages
  1–11. IEEE, 2024. doi: 10.34727/2024/ISBN.978-3-85448-065-5\_17. URL https://doi.org/
  10.34727/2024/isbn.978-3-85448-065-5_17.


                                                12
P. J. Meyer, S. Sickert, and M. Luttenberger. Strix: Explicit reactive synthesis strikes back! In
   H. Chockler and G. Weissenbacher, editors, Computer Aided Verification - 30th International
   Conference, CAV 2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford,
   UK, July 14-17, 2018, Proceedings, Part I, Lecture Notes in Computer Science, pages 578–586.
   Springer, 2018. doi: 10.1007/978-3-319-96145-3\_31. URL https://doi.org/10.1007/
   978-3-319-96145-3_31.

A. Mirhoseini, A. Goldie, M. Yazgan, J. W. Jiang, E. M. Songhori, S. Wang, Y. Lee, E. Johnson,
  O. Pathak, A. Nazi, J. Pak, A. Tong, K. Srinivasa, W. Hang, E. Tuncer, Q. V. Le, J. Laudon,
  R. Ho, R. Carpenter, and J. Dean. A graph placement methodology for fast chip design. Nat.,
  594(7862):207–212, 2021. doi: 10.1038/S41586-021-03544-W. URL https://doi.org/10.
  1038/s41586-021-03544-w.

L. Murphy, K. Yang, J. Sun, Z. Li, A. Anandkumar, and X. Si. Autoformalizing euclidean geometry.
   In R. Salakhutdinov, Z. Kolter, K. A. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp,
   editors, Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria,
  July 21-27, 2024, Proceedings of Machine Learning Research, pages 36847–36893. PMLR /
   OpenReview.net, 2024a. URL https://proceedings.mlr.press/v235/murphy24a.html.

W. Murphy, N. Holzer, N. Koenig, L. Cui, R. Rothkopf, F. Qiao, and M. Santolucito. Guiding LLM
  temporal logic generation with explicit separation of data and control. CoRR, abs/2406.07400,
  2024b. doi: 10.48550/ARXIV.2406.07400. URL https://doi.org/10.48550/arXiv.2406.
  07400.

W. L. Neto, M. T. Moreira, L. G. Amarù, C. Yu, and P. Gaillardon. Read your circuit: Leveraging
 word embedding to guide logic optimization. In ASPDAC ’21: 26th Asia and South Pacific Design
 Automation Conference, Tokyo, Japan, January 18-21, 2021, pages 530–535. ACM, 2021. doi:
 10.1145/3394885.3431560. URL https://doi.org/10.1145/3394885.3431560.

OpenAI. GPT-5.5, Apr. 2026. URL https://openai.com/index/gpt-5-5-system-card/.
  Snapshot gpt-5.5-2026-04-23.

H. Pearce, B. Tan, and R. Karri. DAVE: deriving automatically verilog from english. In U. Schlicht-
  mann, R. Gal, H. Amrouch, and H. H. Li, editors, MLCAD ’20: 2020 ACM/IEEE Workshop on
  Machine Learning for CAD, Virtual Event, Iceland, November 16-20, 2020, pages 27–32. ACM,
  2020. doi: 10.1145/3380446.3430634. URL https://doi.org/10.1145/3380446.3430634.

A. Pnueli. The temporal logic of programs. In 18th Annual Symposium on Foundations of Computer
  Science, Providence, Rhode Island, USA, 31 October - 1 November 1977, pages 46–57. IEEE
  Computer Society, 1977. doi: 10.1109/SFCS.1977.32. URL https://doi.org/10.1109/SFCS.
  1977.32.

A. Pnueli and R. Rosner. On the synthesis of a reactive module. In Conference Record of the
  Sixteenth Annual ACM Symposium on Principles of Programming Languages, Austin, Texas, USA,
  January 11-13, 1989, pages 179–190. ACM Press, 1989. doi: 10.1145/75277.75293. URL
  https://doi.org/10.1145/75277.75293.

F. Renkin, P. Schlehuber-Caissier, A. Duret-Lutz, and A. Pommellet. Dissecting ltlsynt. Formal
   Methods Syst. Des., 61(2):248–289, 2022. doi: 10.1007/S10703-022-00407-6. URL https:
   //doi.org/10.1007/s10703-022-00407-6.

F. Schmitt, C. Hahn, M. N. Rabe, and B. Finkbeiner. Neural circuit synthesis from specifica-
   tion patterns. In M. Ranzato, A. Beygelzimer, Y. N. Dauphin, P. Liang, and J. W. Vaughan,
   editors, Advances in Neural Information Processing Systems 34: Annual Conference on Neu-
   ral Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual,
   pages 15408–15420, 2021. URL https://proceedings.neurips.cc/paper/2021/hash/
   8230bea7d54bcdf99cdfe85cb07313d5-Abstract.html.

S. Thakur, B. Ahmad, H. Pearce, B. Tan, B. Dolan-Gavitt, R. Karri, and S. Garg. Verigen: A large
   language model for verilog code generation. ACM Trans. Design Autom. Electr. Syst., 29(3):
   46:1–46:31, 2024. doi: 10.1145/3643681. URL https://doi.org/10.1145/3643681.


                                                 13
T. Trippel, K. G. Shin, A. Chernyakhovsky, G. Kelly, D. Rizzo, and M. Hicks. Fuzzing hardware like
   software. In K. R. B. Butler and K. Thomas, editors, 31st USENIX Security Symposium, USENIX
   Security 2022, Boston, MA, USA, August 10-12, 2022, pages 3237–3254. USENIX Association,
   2022. URL https://www.usenix.org/conference/usenixsecurity22/presentation/
   trippel.
S. Vasudevan, W. Jiang, D. Bieber, R. Singh, H. Shojaei, R. Ho, and C. Sutton. Learning semantic
   representations to verify hardware designs. In M. Ranzato, A. Beygelzimer, Y. N. Dauphin,
   P. Liang, and J. W. Vaughan, editors, Advances in Neural Information Processing Systems 34:
  Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December
   6-14, 2021, virtual, pages 23491–23504, 2021. URL https://proceedings.neurips.cc/
   paper/2021/hash/c5aa65949d20f6b20e1a922c13d974e7-Abstract.html.
Z. Wang, J. Wang, Q. Yang, Y. Bai, X. Li, L. Chen, J. Hao, M. Yuan, B. Li, Y. Zhang, and
  F. Wu. Towards next-generation logic synthesis: A scalable neural circuit generation frame-
  work. In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and
  C. Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on
  Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, Decem-
  ber 10 - 15, 2024, 2024. URL http://papers.nips.cc/paper_files/paper/2024/hash/
  b3ac808c09f98444090a8f6c2d4bd1dc-Abstract-Conference.html.
C. Wolf, J. Glaser, and J. Kepler. Yosys-a free verilog synthesis suite. In Proceedings of the 21st
  Austrian Workshop on Microelectronics (Austrochip), volume 97, pages 1–6, 2013.
Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik, and C. Szegedy. Autoformalization
  with large language models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and
  A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on
  Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November
  28 - December 9, 2022, 2022. URL http://papers.nips.cc/paper_files/paper/2022/
   hash/d0c6bc641a56bebee9d985b937307367-Abstract-Conference.html.
Z. Zheng, S. Huang, J. Zhong, Z. Shi, G. Dai, N. Xu, and Q. Xu. Deepgate4: Efficient and effective
   representation learning for circuit design at scale. In The Thirteenth International Conference on
  Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025. URL
   https://openreview.net/forum?id=b10lRabU9W.
Y. Zhu, D. Huang, H. Lyu, X. Zhang, C. Li, W. Shi, Y. Wu, J. Mu, J. Wang, Y. Zhao, P. Jin, S. Cheng,
   S. Liang, X. Zhang, R. Zhang, Z. Du, Q. Guo, X. Hu, and Y. Chen. Codev-r1: Reasoning-enhanced
   verilog generation. CoRR, abs/2505.24183, 2025. doi: 10.48550/ARXIV.2505.24183. URL
   https://doi.org/10.48550/arXiv.2505.24183.
W. Zielonka. Infinite games on finitely coloured graphs with applications to automata on infinite
  trees. Theor. Comput. Sci., 200(1-2):135–183, 1998. doi: 10.1016/S0304-3975(98)00009-7. URL
  https://doi.org/10.1016/S0304-3975(98)00009-7.




                                                 14
A     Reactive Synthesis
A.1    Reactive Synthesis Prompt



1     Your task is to translate the following temporal logic
      specification in Temporal Logic Synthesis Format ( TLSF ) into a
      Verilog module that satisfies the specification if realizable , or
      represents an environment strategy if unrealizable .
2
3     The TLSF format builds upon standard Linear Temporal Logic ( LTL )
      and breaks the specification down into up to six sections :
      INITIALLY , PRESET , REQUIRE , ASSERT / INVARIANTS , ASSUME / ASSUMPTIONS ,
        and GUARANTEE / GUARANTEES . If the semantics are " Mealy " or " Moore
      " , the sections are interpreted as the formula f_initially \
      rightarrow ( f_preset \ land ( G f_require \ land f_assume \ rightarrow
        G f_assert \ land f_guarantee ) ) . If the semantics are " Mealy ,
      Strict " or " Moore , Strict " , the sections are interpreted as the
      formula f_initially \ rightarrow ( f_preset \ land ( f_assert W \ neg
      f_require ) \ land ( G f_require \ land f_assume \ rightarrow
      f_guarantee ) ) .
4
5     Follow these guidelines for the translation from TLSF to Verilog :
6
7     - If the specification is unrealizable , swap the roles of inputs
      and outputs : the module ’ s inputs become the specification ’ s
      outputs , and the module ’ s outputs become the specification ’ s
      inputs . The implementation should demonstrate an environment
      strategy that violates the specification for every possible system
       response .
8     - When the TLSF specification contains a PARAMETERS subsection , do
       not generate a parameterized Verilog module , but instead directly
       instantiate the parameters with their given values .
9     - In addition to inputs and outputs , include a single clock input
      named " clk " in the Verilog module and nothing else .
10    - Make sure the code can be processed by Yosys . For example , do
      not declare variables inside procedural blocks like initial or
      always .
11    - Name the module simply " solution " if the specification is
      realizable and " environment " if the specification is unrealizable .
12    - Enclose the Verilog code within triple backticks ( ‘ ‘ ‘) and
      specify " verilog " right after the opening set of backticks .
13
14    Here is the TLSF specification :
15
16    { specification }


                          Figure 5: Reactive synthesis prompt template.




                                               15
A.2   MAX_PARAM Dataset

Table 4: Synthesis results on the MAX_PARAM dataset (57 hardest parameterized SYNTCOMP
benchmarks, formalized variant of the NATURAL dataset). LRM results report the mean over three
runs with standard deviation.
                 Input          Method                               Solved
                                SemML [Kretínský et al., 2025]       19 / 57
                 Algorithmic
                                ltlsynt [Renkin et al., 2022]        19 / 57
                                Gemini 3.1 Pro                   38.3 ± 0.6 / 57
                 LRM
                                GPT-5.5                          41.0 ± 2.6 / 57


A.3   Model Checking Details

Algorithm 1 Yosys recipe for translating Verilog to AIGER
 1: hierarchy -check -top module_name                                        ▷ design hierarchy
 2: proc                                                      ▷ convert RTL processes to netlist
 3: flatten                                                                ▷ inline submodules
 4: opt                                                             ▷ coarse-grain optimization
 5: memory; opt                                               ▷ map memories, then re-optimize
 6: techmap; opt                                                     ▷ rewrite, then re-optimize
 7: dffunmap                                                    ▷ decompose complex flip-flops
 8: abc -g AND                                          ▷ map combinational logic to AND gates
 9: delete -port module_name/clk                                               ▷ strip clock port


Algorithm 2 nuXmv script for LTL model checking with ic3
 1: read_model                                                       ▷ parse the SMV input file
 2: flatten_hierarchy                                    ▷ inline modules into a flat namespace
 3: encode_variables                                   ▷ assign Boolean encodings to variables
 4: build_boolean_model                              ▷ construct the Boolean transition system
 5: check_ltlspec_ic3                                     ▷ verify LTL properties via IC3/IMC
 6: quit                                                      ▷ terminate the interactive session




                                               16
A.4   Reasoning Level Ablations

Table 5: Thinking level ablation on SYNTCOMP. # Reasoning Tokens give the average number of
tokens spent with standard deviation.

           Model                    Thinking Level    Solved          # Reasoning Tokens
                                    LOW               630 / 1586      1082 ± 686
           Gemini 3.1 Pro           MEDIUM            903 / 1586      3490 ± 2839
                                    HIGH              1193 / 1586     14841 ± 9937
                                    NONE              123 / 1586      0±0
                                    LOW               911 / 1586      1025 ± 534
           GPT 5.5                  MEDIUM            1287 / 1586     3450 ± 2751
                                    HIGH              1378 / 1586     5343 ± 4088
                                    XHIGH             1392 / 1586     6892 ± 5342


Table 6: Thinking level ablation on MAX_PARAM dataset. # Reasoning Tokens gives the average
number of tokens spent. Solved reports the mean over three runs together with standard deviation.

                     Model                   Thinking Level    Solved
                                             LOW               21.0 ± 2.0 / 57
                     Gemini 3.1 Pro          MEDIUM            28.7 ± 0.6 / 57
                                             HIGH              38.3 ± 0.6 / 57
                                             NONE              6.7 ± 1.5 / 57
                                             LOW               29.0 ± 3.0 / 57
                     GPT 5.5                 MEDIUM            36.3 ± 1.5 / 57
                                             HIGH              38.3 ± 2.1 / 57
                                             XHIGH             41.0 ± 2.6 / 57


A.5   Decomposition of Specifications

The typical format of reactive synthesis specifications with n assumptions and m guarantees allows
for a decomposition into m independent problems in the realizable case and n independent problems
in the unrealizable case (see Figure 6).


              a1 ∧ . . . ∧ an → g1                               ¬(a1 → g1 ∧ . . . ∧ gm )
             ..                                                 ..
              .                                                  .
              a1 ∧ . . . ∧ an → gm                               ¬(an → g1 ∧ . . . ∧ gm )
              (a) realizable case                                   (b) unrealizable case

Figure 6: Decomposition of the model checking problem into m and n subproblems, respectively.




                                                 17
     B    Parameterized Synthesis

 1   module solution #(
 2       parameter n = 27
 3   ) (
 4       input clk ,
 5       input [n -1:0] finished ,
 6       output allFinished ) ;
 7       reg [n -1:0] seen = { n {1 ’ b0 }};
 8       wire [n -1:0] next ;
 9       wire complete ;
10       assign next = seen | finished ;
11       assign complete = & next ;
12       assign allFinished = complete ;
13       always @ ( posedge clk ) begin
14           if ( complete ) begin
15                seen <= { n {1 ’ b0 }};
16           end else begin
17                seen <= next ;
18           end
19       end
20   endmodule


            Figure 7: A parameterized version of the detector implementation shown in Figure 1.


     C    Limitations
     Verification bottleneck. Model checking the generated Verilog modules against their specifications
     is computationally expensive, especially for large parameter values. While model checking is orders
     of magnitude easier in complexity than synthesis (PSPACE vs. 2EXPTIME), our approach shows that
     LRMs push the guess-and-check paradigm to its limit. In our experiments, a significant fraction of
     instances remain unresolved due to verification timeouts, meaning our reported numbers are a lower
     bound on synthesis capability.

     Undecidable parameterized verification. Parameterized synthesis and parameterized model check-
     ing are both undecidable in general. Our evaluation of parameterized Verilog modules therefore
     relies on checking individual parameter instantiations, which does not guarantee correctness for all
     parameter values. A complete verification would require a proof that the implementation is correct
     for every possible parameter value, which no automated procedure can provide in general.

     Autoformalization evaluation. Assessing the correctness of autoformalized specifications is inher-
     ently difficult. Equivalence checking between the autoformalized and ground-truth specifications is
     expensive (PSPACE-complete for LTL) and timed out for a large fraction of our dataset. Furthermore,
     natural language descriptions can be ambiguous, admitting multiple distinct valid formalizations.

     LRM dependency and reproducibility. Our results depend on proprietary LRM APIs whose
     behavior may change over time. We do not control for model versioning beyond recording the
     model identifiers used (gpt-5.5-2026-04-23 and gemini-3.1-pro-preview). Model providers
     may discontinue models, update weights or safety filters without notice, any of which could affect
     performance. Furthermore, LRM outputs are non-deterministic: even with identical prompts, different
     runs can produce different solutions, as reflected in the variance we report across repeated runs.

     Time and cost. Running large reasoning models at high token budgets across hundreds of spec-
     ifications incurs substantial computational cost. A full evaluation of the SYNTCOMP benchmark
     requires approximately 11M reasoning tokens for GPT-5.5 (XHIGH) and 24M for Gemini 3.1 Pro
     (HIGH), with additional tokens for each repair iteration (see Table 5). A single synchronous call on
     one challenging instance takes about 4 minutes for GPT-5.5 (XHIGH) and 3 minutes for Gemini 3.1
     Pro (HIGH). Both providers, however, support batch inference, heavily parallelizing the calls and
     reducing wall-clock time.


                                                     18
