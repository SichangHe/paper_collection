                                                               PPDL: LLM-Based Flows as Probabilistic Programs


                                                                Louis Mandel 1 Guillaume Baudart 2 Mandana Vaziri 1 Martin Hirzel 1


                                                                  Abstract                                                 LLM-based          ignore factors       LLM-based
                                                                                                                            flow with
                                               Building reliable applications that leverage large                             factors
                                                                                                                                                                     flow
                                               language models (LLMs) remains a significant
                                               challenge. While LLMs offer impressive ca-
                                                                                                                               probabilistically                   classically
                                               pabilities across diverse tasks, their outputs of-                              infer (explore                  interpret (roll
                                               ten lack accuracy and provide no clear measure                                  trace distribution)          out single trace)
                                               of confidence. This uncertainty compounds in
                                               flows of multiple calls to LLMs and other tools,                            distribution              pick         single output
                                               making it difficult for developers and end-users                             of output
                                                                                                                                                                      value
arXiv:2608.05234v1 [cs.LG] 5 Aug 2026




                                               to trust the results. This paper introduces a                                  values
                                               probabilistic language for programming LLM-
                                                                                                              Figure 1. Executing LLM-based flows with or without probabilis-
                                               based flows. It enables developers to quantify                 tic programming. Each circle represents an execution state, with
                                               and propagate uncertainty throughout the appli-                darker shades indicating higher normalized probability.
                                               cation’s flow, and experiment with different in-
                                               ference scaling techniques without adding a sin-
                                               gle line of code beyond the flow’s logic. We                   either independently or with feedback between attempts,
                                               present an experimental study to demonstrate this              hoping that one of the outputs is correct. Inference scal-
                                               capability, and a case study building a theorem                ing usually leverages constraints to refine or select out-
                                               proving agent for the Rocq theorem prover.                     puts, including soft constraints from models and hard con-
                                                                                                              straints from rule-based tools. Since it explores a distri-
                                                                                                              bution of outputs and attempts to shape that distribution
                                        1. Introduction                                                       via constraints, it could be viewed as a form of probabilis-
                                        While a single call to a large language model (LLM) can               tic programming (Gordon et al., 2014). But in practice, it
                                        perform remarkably well for some tasks, other tasks require           tends to be more ad hoc. While inference scaling could
                                        flows of multiple calls to LLMs and other tools (Jimenez              save cost by allocating more resources to better execution
                                        et al., 2024). But while such LLM-based flows may im-                 traces, that would require a principled way to track multiple
                                        prove accuracy, unfortunately, they also exacerbate uncer-            partial traces along with their likelihoods. However, cur-
                                        tainty. Because each step depends on previous uncertain               rent inference scaling implementations are tightly interwo-
                                        outputs, uncertainty compounds along the trace of a flow’s            ven with the program, increasing complexity and hindering
                                        execution. This makes it difficult for users to assess the cor-       the exploration of alternative paradigms. Furthermore, al-
                                        rectness of an answer, leaving them wondering how certain             though in theory inference scaling could help users assess
                                        it is and what other answers are likely.                              answer quality (since it deals in distributions), in practice it
                                                                                                              is rarely principled enough to deliver that benefit.
                                        Several recent solutions for improving LLM flow accu-
                                        racy use inference scaling, which scales up the number of             To obtain more accurate results from LLM-based flows
                                        LLM inference calls or tokens at test time (Chen et al.,              while also giving users visibility into their uncertainty, we
                                        2023; Cobbe et al., 2021; Wang et al., 2023; Yao et al.,              aim to make inference scaling more principled by incor-
                                        2023a;b). The idea is to try the same task several times,             porating it into a programming language. We introduce
                                                                                                              PPDL, the first probabilistic programming language for
                                           1
                                            IBM, New York, USA 2 Université Paris Cité, Inria, CNRS,        LLM-based flows. In general, Probabilistic programming
                                        IRIF, France. Correspondence to: Louis Mandel <lman-                  languages (Gordon et al., 2014; Carpenter et al., 2017;
                                        del@us.ibm.com>.                                                      Goodman et al., 2008; Bingham et al., 2019) decouple the
                                        Proceedings of the 43 rd International Conference on Machine          search over a distribution of traces from the core program
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026          logic, but they are notoriously hard to use and are not
                                        by the author(s).                                                     applied to LLM-based flows. Prompt programming lan-

                                                                                                          1
                                     PPDL: LLM-Based Flows as Probabilistic Programs

guages (Lundberg et al., 2022; Khattab et al., 2024; Zheng           This paper makes the following novel contributions:
et al., 2024; Mell et al., 2025) make it easy to compose
                                                                      1. PPDL, the first probabilistic prompt programming
flows of LLM and tool calls, but do not help with tracking
                                                                         language for flows of LLM and tool calls.
uncertainty. And while they enable developers to explicitly
                                                                      2. A semantics that formalizes the interplay between
build ad hoc inference scaling workflows, such close cou-
                                                                         prompt-based sample and probabilistic factor.
pling between the search and the core logic is complicated
                                                                      3. Results with different probabilistic inference engines
and inflexible.
                                                                         across different LLMs and benchmarks.
PPDL’s goal is to bring these two paradigms together in a             4. A case study building a theorem proving agent for the
single framework. PPDL is designed for developers and re-                Rocq theorem prover.
searchers who build multi-step LLM or agentic workflows,
                                                                     PPDL is open-source and distributed with PDL: https://
including prompt-language users, agent framework devel-
                                                                     github.com/IBM/prompt-declaration-language/tree/icml-26.
opers, and researchers experimenting with inference scal-
ing. PPDL lets users specify the core logic of their program
in a high-level prompting language which already provides            Conflict of Interest Disclosure. All the authors, except
one of the two core constructs of probabilistic languages,           Guillaume Baudart, are employed by IBM, which leads the
namely sample in the form of an LLM call. It extends                 development of the Granite models, which were among the
this language with the second of the two core constructs             ones evaluated in this paper.
of probabilistic languages, namely factor. A factor updates
the probability of the current execution trace based on user-
specified soft or hard constraints.                                  2. Overview
Flow specifications in PPDL require no explicit inference            Prompt programming. PPDL is based on PDL (Vaziri
scaling loops, as the runtime takes care of exploring a dis-         et al., 2024), a declarative approach to prompt program-
tribution of possible traces (see Figure 1). Thus, PPDL              ming that combines human readability with ease of execu-
effectively decouples inference scaling from the core pro-           tion. PDL programs represent the composition of calls to
gram logic, providing a suite of plug-and-play probabilis-           LLMs and tools, abstracting away the plumbing necessary
tic inference engines: simple majority voting, importance            for such compositions. PDL is based on the premise that in-
sampling, and particle filtering (aka. Sequential Monte              teractions with an LLM are mainly for the purpose of gen-
Carlo or SMC). Each particle represents a possible trace             erating data. Users specify the shape of data to be generated
through the program, which might involve multiple LLM                in YAML, which makes it easy to see properly formatted
and tool calls. Unlike traditional prompting languages that          prompts. PDL adds enough scripting to allow specifying
return a single output, PPDL returns a distribution of out-          entire flows. Code blocks allow users to compose LLM
puts. Users can then inspect that distribution to assess un-         calls with arbitrary code written in Python, Jinja2, or Shell.
certainty, or pick a single output, such as the one with the         PDL enables implicit accumulation of the context of mes-
highest probability score.                                           sages, freeing users from such concerns, and provides type
                                                                     checking and constrained decoding to enforce the shape of
Besides prompts, sample (LLM calls), and factor, PPDL                LLM outputs.
includes constructs for variables, control structures (loops,
conditionals, error handling), functions, file imports, and          Consider the example in Figure 2, which illustrates a sim-
tool calls. It allows users to write a flow once and then            ple flow: we first ask a model to generate a plan in natural
experiment with various inference scaling engines with-              language for how to generate code for a problem, then we
out writing an additional line of code. This paper for-              chain that with another model call to generate code while
malizes a semantics for PPDL that clarifies its behavior as          taking the plan into account. Lines 1–5 define some vari-
both a prompting language and a probabilistic language,              ables for use in the rest of the program. Line 6 declares
and the resulting distribution of traces and output values.          the shape of data to be produced as a lastOf, which means
Furthermore, this paper describes an implementation with             a sequence of blocks whose result is that of the last block
parallelization both within a single execution trace and             in the sequence. Lines 7–20 are a list of blocks comprising
across multiple in-flight partial traces using functional data       the body of lastOf. Lines 7–9 show a prompt asking for an
structures. The empirical results show the versatility of            English plan for a code generation problem. Line 10 shows
PPDL as a framework for experimenting with different                 a declarative model call. It provides the id of the model to
inference scaling algorithms across multiple widely used             call from the variable llm defined in Line 2 (PDL is based
benchmarks, as well as a case study where it is used to              on LiteLLM, so this is a LiteLLM id for a watsonX model).
implement a theorem proving agent for the Rocq theorem               A PDL program implicitly accumulates the context in the
prover (Rocq Prover Team).                                           background, so the input to this model call is everything
                                                                     that appeared before. In this case, the input to the model is

                                                                 2
                                         PPDL: LLM-Based Flows as Probabilistic Programs

1  defs:                                                                1 defs:
2    llm: watsonx/meta-llama/llama-4-maverick-...                       2   llm: watsonx/meta-llama/llama-4-maverick-...
3    problem_statement: |                                               3   problem_statement: |
 4     Write a function to find nth centered hexagonal number. 4              Write a function to find nth centered hexagonal number.
 5     assert centered_hexagonal_number(10) == 271                      5     assert centered_hexagonal_number(10) == 271
 6 lastOf:                                                              6   utils:
 7 - >                                                                  7     import: utils.pdl
 8   Generate an English plan for how to generate code for              8 lastOf:
 9   the following problem: ${ problem_statement }                      9 - >
10 - model: ${ llm }                                                   10   Generate an English plan for how to generate code for
11 - >                                                                 11   the following problem: ${ problem_statement }
12   Generate a complete executable Python function                    12 - model: ${ llm }
13   definition corresponding to the above plan and problem.           13   def: plan
14   Generate only a single function definition.                       14 - defs:
15 - model: ${ llm }                                                   15     constraint: |
16   parser:                                                           16       This plan for the following problem is correct.
17     regex: (.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*           17       ${ problem_statement }
18     spec: { code: string }                                          18   factor: ${ utils.llm_judge(llm, plan, constraint) }
19   def: solution                                                     19 - >
20 - ${ solution.code | default("")}                                   20   Generate a complete executable Python function
                                                                       21   definition corresponding to the above plan and problem.
                                                                       22   Generate only a single function definition.
        Figure 2. PDL program generating a Python function.            23 - model: ${ llm }
                                                                       24   parser:
   Table 1. (Left) Possible outputs of the PDL code from Figure 2; 25         regex: (.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*
   (Right) Posterior probability and particle count added by Figure 3. 26     spec: { code: string }
                                                                       27   def: solution
                                                                       28 - factor: ${ utils.score_errors_and_warnings(solution) }
                     Output                     Probability Count 29 - ${ solution.code | default("")}
    def centered_hexagonal_number(n):        0.00005        3
      return 1 + 3 * n * (n + 1)                                          Figure 3. PPDL program adding constraints with factor.
    def centered_hexagonal_number(n):        0.99988        1
      return 1 + 3 * n * (n - 1)
    def centered_hexagonal_number(n):        0.00007        1          answer with the highest probability, providing a greater
      return 1 + 6 * (n * (n + 1)) // 2
                                                                       likelihood of correctness.
                                                                       Figure 3 shows the same program as Figure 2, but with
    the prompt on Lines 7–9. Next, we formulate a prompt to            added constraints. Lines 6–7 import utils, a library with
    generate code (Lines 11–14). This is followed by another           utility functions not shown in this figure. Lines 14–18
    model call on Lines 15–19 for code generation. Its input           score the plan that was generated using an LLM-as-a-
    includes all previous prompts and the response of the first        judge (Zheng et al., 2023). The function utils.llm_judge
    model call. The output is parsed using the regular expres-         takes a model name, a response, and a constraint, and
    sion on Line 17, which defines the code capture group. On          checks whether the response meets the constraint. It is an
    Line 18, a type specification enforces the shape of the out-       LLM call that returns true or false, and we use the log prob-
    put to be a JSON object with a code field. Line 19 defines         abilities output by the LLM to compute a score according
    the variable solution to hold the response of the LLM.             to the following formula:
    Finally, Line 20 contains a Jinja expression that accesses                                                      
                                                                                                        exp(lpt )
    the content of solution.code. Since the top-level block                           score = log exp(lp )+exp(lp  )
                                                                                                          t       f
    is a lastOf, the output of the program is the result of this
    last block. The left column of Table 1 shows some possi-           where lpt and lpf are the log probabilities for true and false,
    ble outputs of the program, since LLM responses are not            respectively. Line 28 shows a rule-based constraint, where
    deterministic.                                                     we compute a score based on the errors and warnings from
                                                                       the flake8 linter.
    Probabilistic prompt programming. PPDL extends                     Each execution of the program now generates an output and
    PDL with a single additional primitive, factor, but funda-         a score that reflect the quality of the corresponding exe-
    mentally changes the execution model by turning the pro-           cution with respect to the user constraints introduced by
    gram into a distribution over traces. In PPDL, the user            factor. The PPDL runtime then performs probabilistic in-
    can use factor to score executions. The program is then            ference, which leverages these scores to estimate the pos-
    bootstrapped into a probabilistic framework that uses those        terior distribution of possible outputs. Probabilistic infer-
    scores in various algorithms. The output of PPDL is a dis-         ence is, in general, intractable, and the distributions com-
    tribution of results, from which the user can sample the           puted by LLMs operate over enormous spaces. PPDL thus

                                                                   3
                                       PPDL: LLM-Based Flows as Probabilistic Programs

relies on Monte Carlo approximate inference algorithms                  To define such a semantics over all traces, we first de-
that launch a series of independent executions, called par-             fine a semantics for a single trace, which has the form
ticles, to estimate the posterior distribution. For example,            p/S ⇒∗ v/S ′ . We refer to the single-trace semantics as
using 5 particles, we obtain the distribution of solutions              a weighted sampler, where the weights come from fac-
shown in Table 1. The solution with high probability is                 tors and the sampling happens via LLM model calls. The
correct, while the other two are incorrect. Three of the five           weighted sampler is defined using reduction rules of the
particles found the first solution, so majority voting would            form p/S ⇒ p or v /S ′ . Each reduction rule transforms
have yielded a wrong solution. Appendix A shows some                    its left-hand side (program p and environment S) into its
step-by-step executions of the program.                                 right-hand side (the remainder of the program at the next
                                                                        factor or a final value v, with updated environment S ′ ). The
The advantage of constraints is that they attach probabil-
                                                                        reduction ⇒∗ is the transitive closure of ⇒ and continues
ities to each response, allowing PPDL to return a correct
                                                                        until it produces a value.
response even if that response is not part of the majority. In
this example, we used importance sampling, but we could                 During execution, the environment S keeps track of two
have used the same program and selected majority voting or              special variables: S[pdl context] accumulates messages,
Sequential Monte Carlo. PPDL allows the user to write the               and S[pdl score] is the trace likelihood. LLM calls in-
logic of the flow once, and experiment with different infer-            troduce randomness: each model call samples a response
ence scaling approaches without needing additional code.                from the distribution defined by an LLM given the cur-
Appendix B presents alternative implementations of Fig-                 rent pdl context, resulting in a new message appended
ures 2 and 3 in other frameworks to illustrate the refactor-            to pdl context. Each factor increments pdl score by
ing required when switching inference scaling algorithms.               a value provided as a parameter. A hard constraint corre-
                                                                        sponds to a factor with parameter −∞ (probability 0 in
Inference scaling approaches depend on constraints to steer
                                                                        log space). As in classic probabilistic programming lan-
execution traces and select solutions. Constraints can be
                                                                        guages (Bingham et al., 2019; Carpenter et al., 2017), we
hard (e.g., failing tests) or soft (e.g., being scored on a
                                                                        can assume that a value was sampled from a distribution
scale), cheap (e.g., checking syntax) or expensive (e.g.,
                                                                        using a factor whose parameter is the log-density of the
calling a large model). Sometimes constraints are sound,
                                                                        distribution at that point. The value of pdl score thus
sometimes complete, but even when neither sound nor
                                                                        represents how well the trace satisfies the user constraints.
complete, they can improve predictive performance. Some
inference scaling literature (Cobbe et al., 2021; Stroebl               Section 3.1 formalizes the weighted sampler by defining
et al., 2026) refers to the source of constraints as “verifiers,”       the syntax and semantics of core PPDL blocks (see Ap-
but we avoid that terminology because it misleadingly im-               pendix C for the remaining blocks). The ideal seman-
plies soundness. Other literature, inspired by reinforcement            tics (⇝) uses an infinite weighted sum over all possible
learning, refers to constraints as rewards and distinguishes            traces (⇒∗ ). Section 3.2 describes the probabilistic infer-
process rewards (in the middle of an execution trace) from              ence engines, each of which computes a finite approxima-
outcome rewards (at the end of a completed trace). Con-                 tion of the ideal semantics. Both the ideal semantics and the
straints can come from models, which can be either fine-                approximate inference engines rely on the weighted sam-
tuned for this task (e.g., process reward models, PRMs)                 pler. Section 3.3 describes the parallelized implementation
or prompted for this purpose (Zheng et al., 2023). PPDL                 of the weighted sampler and the inference engines.
supports all of the above forms of constraints via the prob-
abilistic factor as a single orthogonal language construct.             3.1. Weighted Sampler
                                                                        Figure 4 presents the syntax of a simplified kernel of PPDL,
3. Language and Approach                                                showing its context-free grammar in Backus-Naur Form. A
This section presents how PPDL programs execute, formal-                program is a block comprising a set of variable definitions,
izing their behavior through a probabilistic semantics.                 the block body (i.e., the instruction to evaluate), a parser
                                                                        to extract the result from the return value of the body, a
                                                                        flag indicating whether the result contributes to the context,
Overview. As shown in Figure 1, PPDL lets users ex-                     and the name of the variable in which to store this result.
press an LLM-based flow as a program with factors (top                  The body of a block can be an expression (data), code
left), then explores traces of that program to obtain a                 for a tool call, an LLM call with its input, a conditional,
distribution of output values (bottom left). This sec-                  a sequence of blocks with a join operator to gather result
tion formalizes this intuition via a semantics of the form              values, a loop with a join operator to gather the results of
p/S ; λv.Pr(v), where p is a program, S is its environ-                 each iteration, a function definition, a function call, or a
ment state, ⇝ means reduces to, and λv.Pr(v) denotes a                  factor statement to update the score. The examples from
categorical probability distribution over output values v.

                                                                    4
                                       PPDL: LLM-Based Flows as Probabilistic Programs

                                                                      PPDL is that pdl context and pdl score are propagated
  pdl    ::= { defs:{x:pdl , . . . ,x:pdl },                          through function calls, allowing accumulation to continue.
               body,
               parser:parser ,                                        Now that we have a weighted sampler, we can define the
               contribute:contribute,                                 ideal semantics of a PPDL program as an infinite number
               def:x                            }
 body    ::= data:expr                                                of executions of the sampler (N → ∞) and normalize the
            | code:pdl ,lang:string                                   weights to obtain a categorical distribution:
            | model:expr ,input:pdl
            | if:expr ,then:pdl ,else:pdl                                                 {p/S ⇒∗ vi /Si }1≤i≤N
            | sequence:[pdl , . . . ,pdl ],join:join                                ′                             P
                                                                           wi = exp(Si [pdl score]) 1≤i≤N       W = 1≤i≤N wi
            | while:expr ,repeat:pdl ,join:join
                                                                                   p/S ; λU.
                                                                                                P
            | function:types,return:pdl                                                             1≤i≤N (wi /W ) × δvi (U )
            | call:expr ,args:expr
            | factor:expr                                             The premise {p/S ⇒∗ vi /Si }1≤i≤N denotes a collection
 expr    ::= null | bool | number | string | ${jinja expr }
                                                                      of N executions of the program p starting from the same
            | [expr , . . . ,expr ] | {x:expr , . . . ,x:expr }
                                                                      initial environment S. Each execution reduces p to a final
                                                                      value vi and environment Si . Each Si contains the vari-
  Figure 4. Syntax of PPDL (using the flow-style of YAML).            able pdl score, which stores the unnormalized weight (in
                                                                      log space) accumulated along the corresponding execution
                                                                      trace. The sum W normalizes the score of each result vi .
Section 2 can be compiled into this kernel. For instance,
                                                                      The final result is a categorical distribution that, given a
blocks without an explicit defs clause can be compiled to
                                                                      set of values U , returns its probability (where δvi (U ) is the
use an empty defs, and a model block without an input
                                                                      Dirac distribution that returns 1 when vi ∈ U ).
clause can be compiled to use pdl context as input.
The top rule of Figure 5 is the main rule defining the                3.2. Inference Engines
weighted sampler reduction p/S ⇒ p or v /S ′ . The no-
tation for the rules in this paper places premises (sub-steps)        The ideal semantics are intractable as N → ∞, but
above a horizontal line and conclusions (the reduction be-            probabilistic programming inference algorithms provide
ing defined) below the line. The premises for evaluating a            ways to approximate them.        For example, if N is
block begin by evaluating the variable definitions, then run-         bounded, the rule defining the semantics corresponds to
ning the block body to produce a value v, parsing v into a            the Importance Sampling (IS) algorithm. Each reduction
new value v ′ , and finally contributing v ′ to the background        p/S ⇒∗ vi /Si is a particle computing a value vi with its
context and adding it to the environment. Contribution to             score Si [pdl score]. Similarly, majority voting uses the
the background context is performed by adding a message               same rule with uniform weights, ignoring Si [pdl score].
to the sequence in pdl context (we omit the role in the               We can also use our weighted sampler to describe the Se-
semantics for simplicity):                                            quential Monte Carlo (SMC) algorithm (Del Moral et al.,
                                                                      2006). With SMC, during execution, particles with a low
        ctx = S[pdl context] + [{content:v}]                          score drop their current execution path and restart from the
              S ′ = S[pdl context ← ctx ]                             state of a particle with a higher score. The state selection is
                                       contrib
              S, v, [pdl context] −−−−→ S ′                           made by sampling from the distribution of program states
                                                                      at each resampling point. In PPDL, the resampling points
                                                                      correspond to the factor blocks (i.e., when the reduction
The rest of Figure 5 shows the key block-body reduction
                                                                      ⇒ returns a program block p instead of a value v).
rules. The model block evaluates the model name and in-
put expressions to get an actual model name m and a se-               The SMC algorithm is formalized as follows:
quence of messages i, then samples the LLM correspond-
                                                                                                δp,S ⇝∗ Dv,S ′
ing to m conditioned on i to obtain the output. The factor
                                                                                               p/S ; π1 (Dv,S ′ )
block computes a score w and increments the pdl score
variable by this value. It rewrites into a block that re-                    
                                                                              pi /Si ⇒ p′i /Si′ | (pi , Si ) = sample(Dp,S ) 1≤i≤N
turns the empty string. The rule for a function call illus-
                                                                           wi = exp(Si′ [pdl score]) 1≤i≤N
                                                                                                                           P
                                                                                                                       W = 1≤i≤N wi
trates the handling of the special variables pdl context                                 P
                                                                           Dp,S ⇝ λU.       1≤i≤N (wi /W ) × δpi ,Si [pdl score←0] (U )
                                                                                                                   ′ ′
and pdl score. As in functional programming languages,
it first retrieves the function definition along with its local
environment, evaluates the arguments, checks that they are            Starting from a program p and environment S, we turn this
well-typed, then evaluates the function body in the local en-         initial state into a Dirac distribution (δp,S ) and then apply
vironment to compute the returned value. A key property of            the reduction Dp,S ⇝ Dp′ ,S ′ , which rewrites a distribution

                                                                  5
                                       PPDL: LLM-Based Flows as Probabilistic Programs


          defs                                                     parse                           contrib
 defs/S −−→ {}/S1    block body/S1 → v/S2   parser , v −−−→ v ′ S2 , v ′ , contribute −−−−→ S3    S ′ = S3 [x ← v ′ ]
                                                                                               ′ ′
               {defs:defs,block body,parser:parser ,contribute:contribute,def:x }/S ⇒ v /S

S ⊢ model ⇓ m  S ⊢ input ⇓ i   sample(m, i) = v                         S⊢e⇓w          S ′ = S[pdl score ← S[pdl score] + w]
      model:model ,input:input/S → v/S                                                factor:e/S → data:""/S ′

                      S ⊢ f ⇓ function:t,return:p, scope:Sf         S ⊢ args ⇓ args ′  args′ ∈ t
                  p/Sf [pdl context ← S[pdl context], pdl score ← S[pdl score]] + args ′ ⇒ v/Sf′
                        S ′ = S[pdl context ← Sf′ [pdl context], pdl score ← Sf′ [pdl score]]
                                            call:f ,args:args/S → v/S ′


Figure 5. Key reduction rules for blocks (p/S ⇒ p or v /S ′ ) and block-bodies (b/S → b or v /S ′ ). The reduction S ⊢ e ⇓ v
represents the evaluation of an expression e into a value v in the environment S. The full semantics is provided in Appendix C.


of program states (pairs of program and environment) into              4. Evaluation
a new distribution. When all programs in the distribution
reduce to values (Dv,S ′ ), the result is the pushforward of           4.1. PPDL as an Inference Scaling Framework
the distribution across the first projection (π1 ), yielding the       This section evaluates PPDL as a unified inference-scaling
distribution of return values alone.                                   framework across multiple tasks and models. Our goal
The reduction Dp,S ⇝ Dp′ ,S ′ samples N program/envi-                  is not to claim state-of-the-art task performance, but to
ronment pairs from Dp,S and applies the weighted sam-                  demonstrate that PPDL enables users to write a single pro-
pler ⇒ to compute the next distribution.                               gram and experiment with different inference algorithms
                                                                       without rewriting the flow logic. This allows systematic
                                                                       exploration of which inference strategy works best for a
3.3. Parallel Execution
                                                                       given task and model combination.
PPDL is an interpreted language. Its implementation di-
rectly follows the semantics. Both the implementation of
                                                                       Models. We used granite4-small, granite4-micro, gpt-
the inference engine and of the weighted sampler are par-
                                                                       oss-120b, gpt-oss-20b, llama4-maverick, and llama4-scout
allelized.
                                                                       in our experiments, covering different families and sizes
Bayesian inference algorithms such as IS and SMC are in-               of models. Appendix D includes their release and cutoff
herently parallel, since they rely on independent executions           dates. We set the model temperature for all experiments
of particles. With IS, full traces can be executed in paral-           to 0.8, and use the default reasoning effort for gpt-oss-
lel. SMC introduces a synchronization point at each resam-             120b (medium). All other hyperparameters were left at
pling step, when the distribution of intermediate program              their default values.
states is built and sampled. The PPDL interpreter imple-
ments this parallelism using multi-threading.
                                                                       Benchmarks. We use benchmarks that span a variety of
Within the execution of a particle, the PPDL interpreter par-          tasks and cap all datasets at 500 samples:
allelizes independent model calls using futures (Halstead,
                                                                       • Reasoning: GSM8k (Cobbe et al., 2021) is a dataset of
1985). Model calls return a promise of a response rather
                                                                         grade-school level math problems; Math500 (Math-500
than blocking. When an expression is evaluated, the inter-
                                                                         Dataset) is a curated selection of 500 problems from the
preter traverses the relevant data structures to await the re-
                                                                         Math dataset (Hendrycks et al., 2021), spanning algebra,
sponses of only those model calls on which the expression
                                                                         geometry, number theory, pre-calculus, and probability.
depends. To limit dependencies, the data structures cre-
                                                                       • Code generation: MBPP (Austin et al., 2021) is
ated by PPDL, especially pdl context, are lazy (Okasaki,
                                                                         a collection of mostly basic Python programming
1998), ensuring that only the accessed cell of an array or
                                                                         tasks; LiveCodeBench (Jain et al., 2025) is a dy-
field of an object is awaited.
                                                                         namic contamination-free benchmark using fresh prob-
                                                                         lems from LeetCode, AtCoder, and Codeforces. We se-
                                                                         lected the code generation task and its latest version (v6)
                                                                         with a time window from 8/1/2024 to 5/1/2025.
                                                                       • Question answering: Fever (Thorne et al., 2018) is a
                                                                         fact checking dataset.

                                                                   6
                                             PPDL: LLM-Based Flows as Probabilistic Programs

Table 2. Accuracy comparison across benchmarks, models, and                         uses an LLM to judge the validity of the plan (scoring
inference algorithms. IS@1 is the baseline (single execution),
Maj. Voting (Majority Voting), IS (Importance Sampling), and
                                                                                    accordingly). It then generates a Python function cor-
SMC (Sequential Monte Carlo) use 5 particles each, and pass@k                       responding to the plan by calling the model. It extracts
represents the oracle upper bound. Bold indicates best perfor-                      the Python code and uses rule-based judges to check that
mance among inference algorithms. All results show mean ±                           the solution contains function definitions and to evaluate
standard deviation over 3 runs.                                                     the number of warnings using flake8. Finally, the same
model             IS@1     Maj. Voting      IS         SMC        pass@k
                                                                                    LLM is used to judge the correctness of the solution.
                                                                                  • Question answering: The program first asks the ques-
GSM8k
                                                                                    tion to the LLM, enabling it to use a Wikipedia search
granite4-small 83.8% ± 0.3 90.4% ± 0.9 93.7% ± 0.5 92.3% ± 0.3 96.1% ± 0.3          tool. This may result in tool-use requests. We then check
granite4-micro 79.5% ± 0.9 87.1% ± 1.6 87.8% ± 0.4 84.2% ± 0.6 93.7% ± 0.1
llama4-scout    93.9% ± 0.2 94.5% ± 0.3 94.4% ± 0.3 94.6% ± 0.3 95.5% ± 0.2         whether the topic(s) to be searched are sensible using the
llama4-maverick 95.3% ± 0.2 95.7% ± 0.4 95.4% ± 0.3 95.3% ± 0.3 96.7% ± 0.3         same LLM as a judge and call the search tool. We use
gpt-oss-120b    86.9% ± 0.3 90.4% ± 0.8 92.2% ± 0.3 90.8% ± 0.0 95.1% ± 0.1
gpt-oss-20b     90.2% ± 1.2 93.1% ± 0.5 92.7% ± 0.4 91.9% ± 0.8 95.5% ± 0.2         LLM-as-judge to check whether enough evidence has
Math500                                                                             been gathered and finally call the LLM again to verify or
granite4-small 60.7% ± 0.4 62.1% ± 0.6 64.0% ± 1.1 65.5% ± 1.7 75.7% ± 0.3          refute the original question given the gathered evidence.
granite4-micro 47.4% ± 0.6 47.7% ± 1.2 52.5% ± 1.1 51.1% ± 0.7 66.5% ± 0.5
llama4-scout    66.3% ± 0.1 65.7% ± 0.5 67.3% ± 0.4 67.5% ± 0.6 71.9% ± 0.3
llama4-maverick 69.9% ± 0.3 69.7% ± 0.6 71.5% ± 0.9 70.1% ± 0.5 74.7% ± 0.6
gpt-oss-120b    74.2% ± 0.2 73.8% ± 1.1 74.8% ± 1.0 74.5% ± 0.3 77.9% ± 0.3       Results. Table 2 reports the results of our experiments.
gpt-oss-20b     74.1% ± 0.1 74.0% ± 1.1 75.7% ± 0.5 74.9% ± 0.4 79.0% ± 0.2
                                                                                  We perform three runs for each task, model, and algo-
MBPP
                                                                                  rithm and report the mean accuracy and standard deviation.
granite4-small 69.7% ± 1.9 69.7% ± 2.9 80.5% ± 2.1 80.2% ± 2.0 92.0% ± 1.2
granite4-micro 71.9% ± 1.0 72.9% ± 2.5 75.1% ± 2.6 74.8% ± 0.3 89.5% ± 1.8        The column labeled IS@1 is the baseline corresponding to
llama4-scout    82.5% ± 0.9 81.7% ± 2.0 86.1% ± 2.1 85.4% ± 1.6 92.0% ± 1.6       a program executed without inference scaling. Similarly,
llama4-maverick 90.3% ± 0.5 90.4% ± 2.3 91.4% ± 1.0 90.9% ± 1.3 95.9% ± 0.9
gpt-oss-120b    92.4% ± 0.2 93.6% ± 0.3 94.1% ± 1.1 93.4% ± 1.0 97.8% ± 0.3       pass@k is an oracle upper bound, where at least one out
gpt-oss-20b     92.3% ± 0.9 93.1% ± 1.8 91.7% ± 1.2 92.4% ± 1.0 98.0% ± 0.5       of k particles has the correct answer. These benchmarks
LiveCodeBench                                                                     demonstrate how easily a user can experiment with dif-
granite4-small 15.8% ± 0.3 15.5% ± 0.8 17.4% ± 1.1 15.7% ± 0.6 24.0% ± 0.7        ferent inference scaling algorithms for a given task and
granite4-micro 11.1% ± 0.3 11.5% ± 1.3 10.7% ± 0.6 11.1% ± 0.9 18.2% ± 0.7        model and choose between them without writing additional
llama4-scout    23.9% ± 0.3 24.5% ± 0.6 24.9% ± 0.4 23.9% ± 1.0 30.3% ± 0.6
llama4-maverick 29.0% ± 0.2 28.5% ± 0.3 29.1% ± 0.2 29.3% ± 0.1 36.7% ± 0.2       code. This is particularly interesting for SMC, which has a
gpt-oss-120b    30.3% ± 0.8 19.5% ± 1.5 36.1% ± 2.0 35.8% ± 0.8 48.2% ± 0.3       more intricate implementation. The results show the accu-
gpt-oss-20b     20.8% ± 0.5 12.5% ± 1.2 8.0% ± 0.9 15.9% ± 0.8 40.2% ± 0.3
                                                                                  racy improvements achieved by inference scaling over the
Fever
                                                                                  baseline and that while simple majority voting is the best-
granite4-small 76.6% ± 0.6 77.5% ± 0.8 77.9% ± 1.0 78.1% ± 1.3 88.3% ± 0.9
granite4-micro 71.7% ± 0.2 73.6% ± 0.3 73.7% ± 0.8 73.3% ± 1.2 90.3% ± 1.1        performing algorithm in some cases (e.g., GSM8k with
llama4-scout    85.6% ± 0.4 85.0% ± 0.2 85.9% ± 1.5 84.1% ± 0.1 93.7% ± 0.8       gpt-oss-20b), in other cases importance sampling or SMC
llama4-maverick 81.6% ± 0.3 81.7% ± 0.6 80.9% ± 0.4 81.0% ± 0.2 85.7% ± 0.3
gpt-oss-120b    86.5% ± 0.2 87.5% ± 0.5 86.7% ± 0.3 87.2% ± 0.0 92.7% ± 0.6       performs best.
gpt-oss-20b     79.9% ± 0.4 81.3% ± 0.2 79.9% ± 1.0 81.2% ± 0.5 90.6% ± 0.8
                                                                                  In general, importance sampling (IS) and SMC are prefer-
                                                                                  able to majority voting when the factor statements pro-
                                                                                  vide meaningful information, as they use the factors to
Inference scaling algorithms. We consider the follow-                             shift probability mass toward better traces. Between IS
ing inference scaling algorithms: majority voting (Maj.                           and SMC, SMC is particularly advantageous for longer,
Voting), importance sampling (IS), and sequential Monte                           deeper flows with informative intermediate factors. IS only
Carlo (SMC). We run all experiments with 5 particles.                             reweights completed traces, while SMC can resample dur-
                                                                                  ing execution at factor points, allowing computation to be
PPDL Programs. For each benchmark, we write a PPDL                                redirected toward more promising partial traces earlier in
program to capture the logic of interacting with LLMs and                         the flow. This gives SMC a more meaningful exploration
add factors to shift the distribution toward desirable results                    of the search space in multi-step settings, as demonstrated
using both LLM-based judges and rule-based ones. The                              in the theorem-proving case study below.
complete PPDL implementations are in Section E.
                                                                                  4.2. Case Study: Theorem Proving in Rocq
 • Reasoning: The program asks the LLM to solve the
   math problem, then extracts the answer and asks the                            As a case study, we use PPDL to implement a theorem
   same LLM to judge the correctness of the solution and                          proving agent for Rocq, formerly known as Coq (Rocq
   score it according to the formula shown in Section 2.                          Prover Team), a proof assistant, similar to Lean or Isabelle,
 • Code generation: The program first asks the LLM to                             that can automatically check mathematical proofs. The
   generate an English plan for the problem at hand, then                         complete PPDL implementation is provided in Section E.6.

                                                                              7
                                     PPDL: LLM-Based Flows as Probabilistic Programs

We focus on the MiniF2F dataset (Zheng et al., 2021;                Table 3. Number of problems solved out of the 244 MiniF2F-
                                                                    Rocq problems. We present the average ± one standard deviation
Jiang et al., 2022), a popular benchmark for evaluating             over three runs.
theorem proving agents (Polu & Sutskever, 2020; Thakur
et al., 2024; Mikuła et al., 2023; Wang et al., 2024). The                                            Particles        IS              SMC               delta
test split comprises 244 high-school level math exercises,
ranging from simple algebra to International Mathemat-                                                    1       72.7 ± 2.9            -                 -
ics Olympiad problems. While the Lean version of this                                                     5       82.7 ± 3.9       84.7 ± 1.2            +2.0
benchmark is already saturated, with state-of-the-art spe-                                               10       84.3 ± 3.9       91.3 ± 1.7            +7.0
cialized models with aggressive inference scaling reaching                                               20       87.0 ± 1.6       94.3 ± 2.1            +7.3
up to 99% accuracy (Varambally et al., 2025), the Rocq                                                   40       87.7 ± 2.4       95.0 ± 2.4            +7.3
version (Viennot et al., 2025) is more recent, and the con-
tamination risk is minimal. The goal of this experiment is                                             100

not to compare our agent with state-of-the-art solutions, but




                                                                          Number of Theorems Solved
                                                                                                        80
to measure how much probabilistic inference can improve
the performance of a base model on a challenging task.                                                  60


                                                                                                        40
Experimental setup. We adapt an experiment originally                                                                                                    SMC@40
                                                                                                                                                         SMC@20
designed for Lean to the Rocq prover to study how dif-                                                  20
                                                                                                                                                         SMC@10
ferent prompting and inference scaling strategies affect                                                                                                 SMC@5
                                                                                                         0                                               IS@1
LLM-based theorem proving (G. Narozniak, personal com-
                                                                                                              0   10    20    30     40        50   60     70     80
munication, 2026). A full proof generation agent alter-                                                                      Number of Steps
nates between two steps: LLM-based proof synthesis and
prover-based verification. The agent implements a simple            Figure 6. Number of MiniF2F-Rocq problems solved as a func-
                                                                    tion of proof/repair steps. Each curve shows the mean over three
proof/repair loop: if the verification step fails, the agent        runs, with shaded regions indicating one standard deviation.
lists all errors and prompts the LLM to fix the proof.
For each exercise, we compare three inference scaling
strategies under a limit on the total number of tokens that         having more particles since larger particle populations help
can be used to find the proof: 1) IS@1: repeatedly retry            preserve diversity during resampling and reduce the risk of
until a proof is found or the token budget is exhausted (this       collapsing too early onto a narrow set of traces.
corresponds to sequential scaling); 2) IS@k: run k particles        Since the number of tokens is constant, there is a trade-off
and stop as soon as one of them finds a proof or the token          between the number of proof/repair steps and multiple par-
budget is exhausted (this is equivalent to pass@k thanks to         ticles searching solutions in parallel. Figure 6 shows this
the perfect verifier and because scores are ignored when a          trade-off for the SMC algorithm (results are similar for IS
proof is found); 3) SMC@k: similar to IS, but use the num-          and shown in Figure 26 in the appendix). A single parti-
ber of errors at each attempt to score the particles and pri-       cle (IS@1) leverages prover feedback across up to 74 se-
oritize the most promising proofs. When a proof is found,           quential repairs whereas SMC@40 goes down to 9 steps.
the agent terminates the execution of all parallel particles        Parallel exploration is more efficient for exploring the proof
and returns the successful proof.                                   space and can prove more theorems in a single step, but it
Using PPDL, we evaluate these three strategies on the same          exhausts the token budget more quickly.
program by adjusting the runtime configuration, varying             Our agent is relatively simple, but optimizing this explo-
only the inference algorithm and particle count. We run all         ration/exploitation trade-off could be even more benefi-
experiments with gpt-oss-120b, a temperature of 1.0, and a          cial for more advanced prompting strategies that leverage
budget of 1M tokens.                                                feedback from multiple tools (e.g., the prover, specialized
                                                                    search engines, or a natural language reasoner).
Results. Table 3 presents a summary of the results. We
observe that with a constant number of tokens the accu-             5. Related Work
racy varies from 30% (72.7/244 for IS@1) to 39% (95/244
for SMC@40). With a fixed number of particles, SMC al-              There is not much prior work at the intersection be-
ways performs better than IS. SMC can resample during               tween prompt programming and probabilistic program-
execution at factor points, allowing computation to be redi-        ming. LLaMPPL (Lew et al., 2023) and GenML Con-
rected toward more promising partial traces earlier in the          trol (Loula et al., 2025) apply probabilistic inference en-
flow. This gives SMC a more meaningful exploration of the           gines to the decoding of LLM-generated tokens with SMC
search space in multi-step settings. SMC also benefits from         and both soft and hard constraints. But unlike our work,

                                                                8
                                    PPDL: LLM-Based Flows as Probabilistic Programs

they focus on a single LLM call, not a flow of LLM and tool        embody these sequential inference scaling approaches, and
calls. LMQL features hard constraints and beam search              PPDL directly inherits this property. Besides parallel and
over traces (Beurer-Kellner et al., 2023); unlike our work,        sequential, a third style is search-based inference scaling,
it lacks soft constraints and probabilistic inference such         e.g., Yao et al. (2023a) and Zhou et al. (2024). PPDL makes
as SMC. Similarly, EnCompass also supports beam search             search-based inference scaling implicit and orthogonal.
over traces (Li et al., 2025); however, as it does not track
                                                                   Rooted in earlier work on automated machine learn-
how uncertainty accumulates across factors, it also lacks
                                                                   ing (Feurer et al., 2015; Baudart et al., 2021b), automated
probabilistic inference. Rollout Roulette uses a process re-
                                                                   prompt optimization uses known question/answer pairs to
ward model with SMC over token sequences (Puri et al.,
                                                                   improve prompts for future questions. More recently,
2025); in contrast, our work supports a more general set
                                                                   instance optimization applies prompt optimization for a
of soft and hard constraints, and supports multi-call flows.
                                                                   specific new question; examples include TextGrad (Yuk-
Bertsch et al. (2023) reframe inference scaling as proba-
                                                                   sekgonul et al., 2025), Trace (Cheng et al., 2024), and
bilistic inference to find the Minimum Bayes Risk sample,
                                                                   Gepa (Agrawal et al., 2025). Unlike our work, none are
but do not explore SMC nor LLM-and-tool flows.
                                                                   PPLs or use probabilistic inference engines. In future work,
We take inspiration from the rich literature on probabilis-        we plan to integrate some of these techniques.
tic languages (PPLs) that predates prompt programming
with LLMs. An overview paper by Gordon et al. (2014)               6. Conclusion
introduces core constructs of probabilistic programming
and inference via the Prob PPL. The Stan PPL has been              This paper introduces PPDL, a new programming language
widely adopted in practice (Carpenter et al., 2017). The           that unifies prompt programming and probabilistic pro-
Church PPL is based on lambda calculus (Goodman et al.,            gramming. Prompt programming languages make LLM
2008). Like PPDL, each of Prob, Stan, and Church tracks            prompting easy, but struggle with inaccuracy and uncer-
and updates a log-probability along a trajectory; but un-          tainty. One solution for boosting accuracy is inference scal-
like PPDL, none of them interface with LLMs. Some more             ing, but unfortunately, manually adding inference scaling
recent PPLs do interface with neural networks, such as             to a prompt program sacrifices simplicity and flexibility.
Pyro (Bingham et al., 2019) and DeepStan (Baudart et al.,          Instead, PPDL lets users write the core logic in a simple
2021a), but they do not focus on language models, let alone        prompting language, and the interpreter applies orthogonal
prompt programming.                                                probabilistic inference engines to search the space of trajec-
                                                                   tories. As a bonus, since the program returns a distribution,
Another source of inspiration for PPDL is the growing lit-
                                                                   users also get a better feeling for the uncertainty of results.
erature on prompt programming languages. We already
discussed LMQL and PDL. Guidance focuses on hard
                                                                   Limitations. While useful, inference scaling is no silver
constraints to guide generation (Lundberg et al., 2022).
                                                                   bullet (Stroebl et al., 2026). Any steering based on fac-
Both DSPy (Khattab et al., 2024) and AutoPDL (Spiess
                                                                   tors can only be as good as the information in those fac-
et al., 2025) provide support for optimizing prompt pro-
                                                                   tors, which is often imperfect, e.g., based on an LLM-as-
grams for an objective function, which could be viewed
                                                                   a-judge (Zheng et al., 2023). In future work, we plan to
as a final soft constraint. Other prompting languages in-
                                                                   mitigate that limitation by calibrating factors, so multiple
clude SGLang (Zheng et al., 2024), Vieira (Li et al., 2024),
                                                                   constraints carry the appropriate relative weight.
APPL (Dong et al., 2025), and Opp (Mell et al., 2025). Un-
like PPDL, none of these are probabilistic languages; while
several of the papers include inference scaling examples,          Acknowledgements
those are written by hand, not orthogonal like in PPDL.
                                                                   We would like to thank Theo Stoskopf for all the help
Parallel inference scaling scales the number of independent        and support with the rocq-ml-toolbox (https://github.com/
attempts for solving a problem (where each attempt can             LLM4Rocq/rocq-ml-toolbox) that we used for the theorem-
be a full trace). Examples include Self-consistency (Wang          proving case study.
et al., 2023) and Large Language Monkeys (Brown et al.,
2024). PPDL makes parallel inference scaling implicit
                                                                   Impact Statement
and orthogonal. Sequential inference scaling scales the
number of tokens in a single LLM call or the number of             This paper presents work whose goal is to advance the field
LLM calls in a single trajectory. Examples include chain-          of Machine Learning. There are many potential societal
of-thought (Wei et al., 2022), Self-refine (Madaan et al.,         consequences of our work, none of which we feel must be
2023), and ReAct agents (Yao et al., 2023b). PDL has               specifically highlighted here.
been designed to facilitate the implementation of flows that


                                                               9
                                    PPDL: LLM-Based Flows as Probabilistic Programs

References                                                            (1):1–37, 2017. URL https://www.jstatsoft.org/article/view/
                                                                      v076i01.
Agrawal, L. A., Tan, S., Soylu, D., Ziems, N., Khare, R.,
  Opsahl-Ong, K., Singhvi, A., Shandilya, H., Ryan, M. J.,          Chen, B., Zhang, F., Nguyen, A., Zan, D., Lin, Z., Lou, J.-
  Jiang, M., Potts, C., Sen, K., Dimakis, A. G., Stoica,              G., and Chen, W. CodeT: Code generation with gener-
  I., Klein, D., Zaharia, M., and Khattab, O. GEPA: Re-               ated tests. In International Conference on Learning Rep-
  flective prompt evolution can outperform reinforcement              resentations (ICLR), May 2023. URL https://openreview.
  learning, July 2025. URL https://arxiv.org/abs/2507.19457.          net/forum?id=ktrw68Cmu9c.

Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,             Cheng, C.-A., Nie, A., and Swaminathan, A. Trace
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., and           is the next AutoDiff:     Generative optimization
  Sutton, C. Program synthesis with large language mod-               with rich feedback, execution traces, and LLMs.
  els, August 2021. URL https://arxiv.org/abs/2108.07732.             In Conference on Neural Information Process-
                                                                      ing Systems (NeurIPS), December 2024.       URL
Baudart, G., Burroni, J., Hirzel, M., Mandel, L., and
                                                                      https://proceedings.neurips.cc/paper files/paper/2024/hash/
  Shinnar, A. Compiling Stan to generative probabilistic
                                                                      83ba7056bce2c3c3c27e17397cf3e1f0-Abstract-Conference.
  languages and extension to deep probabilistic program-
                                                                      html.
  ming. In Conference on Programming Language Design
  and Implementation (PLDI), pp. 497–510, June 2021a.               Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
  URL https://doi.org/10.1145/3453483.3454058.                        Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
                                                                      R., Hesse, C., and Schulman, J. Training verifiers to
Baudart, G., Hirzel, M., Kate, K., Ram, P., Shinnar, A.,
                                                                      solve math word problems, October 2021. URL https:
  and Tsay, J. Pipeline combinators for gradual Au-
                                                                      //arxiv.org/abs/2110.14168.
  toML. In Conference on Neural Information Process-
  ing Systems (NeurIPS), pp. 19705–19718, December                  Del Moral, P., Doucet, A., and Jasra, A. Sequential Monte
  2021b. URL https://proceedings.neurips.cc/paper/2021/file/          Carlo samplers. J. Royal Statistical Society: Series B
  a3b36cb25e2e0b93b5f334ffb4e4064e-Paper.pdf.                         (Statistical Methodology), 68(3):411–436, 2006.
Bertsch, A., Xie, A., Neubig, G., and Gormley, M. R. It’s           Dong, H., Su, Q., Gao, Y., Li, Z., Ruan, Y., Pekhimenko,
  MBR all the way down: Modern generation techniques                  G., Maddison, C. J., and Si, X. APPL: A prompt pro-
  through the lens of minimum Bayes risk. In Proceedings              gramming language for harmonious integration of pro-
  of the Big Picture Workshop (BigPicture@EMNLP), pp.                 grams and large language model prompts. In Annual
  108–122, December 2023. URL https://doi.org/10.18653/               Meeting of the Association for Computational Linguis-
  v1/2023.bigpicture-1.9.                                             tics (ACL), July 2025. URL https://aclanthology.org/2025.
                                                                      acl-long.63/.
Beurer-Kellner, L., Fischer, M., and Vechev, M. Prompting
  is programming: A query language for large language               Feurer, M., Klein, A., Eggensperger, K., Springenberg,
  models. In Conference on Programming Language De-                   J., Blum, M., and Hutter, F. Efficient and robust au-
  sign and Implementation (PLDI), pp. 1946–1969, June                 tomated machine learning. In Conference on Neu-
  2023. URL https://doi.org/10.1145/3591300.                          ral Information Processing Systems (NIPS), pp. 2962–
                                                                      2970, December 2015. URL http://papers.nips.cc/paper/
Bingham, E., Chen, J. P., Jankowiak, M., Obermeyer, F.,               5872-efficient-and-robust-automated-machine-learning.
  Pradhan, N., Karaletsos, T., Singh, R., Szerlip, P., Hors-
  fall, P., and Goodman, N. D. Pyro: Deep universal prob-           Goodman, N., Vikash, M., Roy, D., Bonawitz, K., and
  abilistic programming. Journal of Machine Learning Re-              Tenenbaum, J. Church: a language for generative mod-
  search (JMLR), 20:1–6, 2019. URL https://www.jmlr.org/              els. In Conference on Uncertainty in Artificial Intelli-
  papers/v20/18-403.html.                                             gence (UAI), pp. 220–229, 2008. URL https://dslpitt.org/
                                                                      uai/papers/08/p220-goodman.pdf.
Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V.,
  Re, C., and Mirhoseini, A. Large language monkeys:                Gordon, A. D., Henzinger, T. A., Nori, A. V., and Ra-
  Scaling inference compute with repeated sampling, July              jamani, S. K. Probabilistic programming. In ICSE
  2024. URL https://arxiv.org/abs/2407.21787.                         track on Future of Software Engineering (FOSE@ICSE),
                                                                      pp. 167–181, 2014. URL https://doi.org/10.1145/2593882.
Carpenter, B., Gelman, A., Hoffman, M., Lee, D.,                      2593900.
  Goodrich, B., Betancourt, M., Brubaker, M. A., Guo,
  J., Li, P., and Riddell, A. Stan: A probabilistic pro-            Halstead, Jr., R. H. Multilisp: A language for concurrent
  gramming language. Journal of Statistical Software, 76              symbolic computation. Transactions on Programming

                                                               10
                                     PPDL: LLM-Based Flows as Probabilistic Programs

  Languages and Systems (TOPLAS), 7(4):501–538, Oc-                  Loula, J., LeBrun, B., Du, L., Lipkin, B., Pasti, C., Grand,
  tober 1985. URL https://doi.org/10.1145/4472.4478.                   G., Liu, T., Emara, Y., Freedman, M., Eisner, J., Cot-
                                                                       terell, R., Mansinghka, V., Lew, A. K., Vieira, T., and
Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,             O’Donnell, T. J. Syntactic and semantic control of
  S., Tang, E., Song, D., and Steinhardt, J. Measuring                 large language models via sequential Monte Carlo. In
  mathematical problem solving with the math dataset.                  International Conference on Learning Representations
  In NeurIPS Datasets and Benchmarks Track, December                   (ICLR), May 2025. URL https://openreview.net/forum?id=
  2021. URL https://openreview.net/forum?id=7Bywt2mQsCe.               xoXn62FzD0.

Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang, T.,            Lundberg, S., Ribeiro, M. T. C., and et al. Guidance: A
   Wang, S., Solar-Lezama, A., Sen, K., and Stoica, I. Live-           guidance language for controlling large language mod-
   CodeBench: Holistic and contamination free evaluation               els, November 2022. URL https://github.com/guidance-ai/
   of large language models for code. In International Con-            guidance.
   ference on Learning Representations (ICLR), May 2025.
   URL https://openreview.net/forum?id=chfJJYC3iL.                   Madaan, A., Tandon, N., Gupta, P., Hallinan, S.,
                                                                      Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prab-
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jam-         humoye, S., Yang, Y., Gupta, S., Majumder, B. P.,
   nik, M., Lacroix, T., Wu, Y., and Lample, G. Draft,                Hermann, K., Welleck, S., Yazdanbakhsh, A., and
   sketch, and prove: Guiding formal theorem provers                  Clark, P. Self-refine: Iterative refinement with self-
   with informal proofs. In International Conference on               feedback.    In Conference on Neural Information
   Learning Representations (ICLR), 2022. URL https:                  Processing Systems (NeurIPS), December 2023. URL
   //openreview.net/forum?id=SMa9EAovKMC.                              https://proceedings.neurips.cc/paper files/paper/2023/hash/
                                                                       91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.
Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K.,
                                                                       html.
  Press, O., and Narasimhan, K. SWE-bench: Can lan-
  guage models resolve real-world GitHub issues? In                  Math-500 Dataset.        Math-500 benchmark leaderboard.
  International Conference on Learning Representations                 https://artificialanalysis.ai/evaluations/math-500.
  (ICLR), May 2024. URL https://openreview.net/forum?id=
  VTF8yNQM66.                                                        Mell, S., Kallas, K., Zdancewic, S., and Bastani, O. Op-
                                                                      portunistically parallel lambda calculus. In Conference
Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., San-             on Object-Oriented Programming, Systems, Languages,
  thanam, K., A, S. V., Haq, S., Sharma, A., Joshi, T. T.,            and Applications (OOPSLA), pp. 2596–2622, October
  Moazam, H., Miller, H., Zaharia, M., and Potts, C.                  2025. URL https://doi.org/10.1145/3763143.
  DSPy: Compiling declarative language model calls into
  self-improving pipelines. In International Conference              Mikuła, M., Tworkowski, S., Antoniak, S., Piotrowski, B.,
  on Learning Representations (ICLR), May 2024. URL                   Jiang, A. Q., Zhou, J. P., Szegedy, C., Kuciński, Ł.,
  https://openreview.net/forum?id=sY5N0zY5Od.                         Miłoś, P., and Wu, Y. Magnushammer: A transformer-
                                                                      based approach to premise selection. arXiv preprint
Lew, A. K., Zhi-Xuan, T., Grand, G., and Mansinghka,                  arXiv:2303.04488, 2023.
  V. K. Sequential Monte Carlo steering of large lan-
  guage models using probabilistic programs. In Work-                Okasaki, C. Purely Functional Data Structures. Cambridge
  shop on Sampling and Optimization in Discrete Space                  University Press, 1998.
  (SODS@ICML), July 2023. URL https://openreview.net/
  forum?id=Ul2K0qXxXy.                                               Polu, S. and Sutskever, I. Generative language mod-
                                                                       eling for automated theorem proving. arXiv preprint
Li, Z., Huang, J., Liu, J., Zhu, F., Zhao, E., Dodds, W.,              arXiv:2009.03393, 2020.
  Velingker, N., Alur, R., and Naik, M. Relational pro-
  gramming with foundation models. In Conference on                  Puri, I., Sudalairaj, S., Xu, G., Xu, K., and Srivastava,
  Artificial Intelligence (AAAI), February 2024. URL https:            A. Rollout roulette: A probabilistic inference approach
  //doi.org/10.1609/aaai.v38i9.28934.                                  to inference-time scaling of LLMs using particle-based
                                                                       Monte Carlo methods. In Conference on Neural Infor-
Li, Z., Solar-Lezama, A., Yue, Y., and Zheng, S. EnCom-                mation Processing Systems (NeurIPS), December 2025.
  pass: Enhancing agent programming with search over                   URL https://openreview.net/forum?id=qPQUrjiA0q.
  program execution paths. In Conference on Neural Infor-
  mation Processing Systems (NeurIPS), December 2025.                Rocq Prover Team. The Rocq prover. https://rocq-prover.
  URL https://openreview.net/forum?id=IKVkpjSJzJ.                      org/. Accessed: 2026-01-26.

                                                                11
                                      PPDL: LLM-Based Flows as Probabilistic Programs

Spiess, C., Vaziri, M., Mandel, L., and Hirzel, M. Au-                 models. In Conference on Neural Information Pro-
  toPDL: Automatic prompt optimization for LLM agents.                 cessing Systems (NeurIPS), December 2023a. URL
  In Conference on Automated Machine Learning (Au-                     https://proceedings.neurips.cc/paper files/paper/2023/hash/
  toML), September 2025. URL https://proceedings.mlr.                  271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.
  press/v293/spiess25a.html.                                           html.

Stroebl, B., Kapoor, S., and Narayanan, A. Inference scal-           Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
  ing FLaws: The limits of LLM resampling with imper-                  K. R., and Cao, Y. ReAct: Synergizing reasoning and
  fect verifiers, March 2026. URL https://arxiv.org/abs/2411.          acting in language models. In International Conference
  17501.                                                               on Learning Representations (ICLR), May 2023b. URL
                                                                       https://openreview.net/forum?id=WE vluYUL-X.
Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaud-
  huri, S. An in-context learning agent for formal theorem-          Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Lu, P.,
  proving. In Conference on Language Modeling (COLM),                  Huang, Z., Guestrin, C., and Zou, J. Optimizing gener-
  October 2024.                                                        ative AI by backpropagating language model feedback.
                                                                       Nature, 639(8055):609–616, March 2025.
Thorne, J., Vlachos, A., Christodoulopoulos, C., and Mit-
  tal, A. FEVER: a large-scale dataset for fact extraction           Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-
  and VERification, March 2018. URL https://arxiv.org/abs/             system benchmark for formal olympiad-level mathemat-
  1803.05355.                                                          ics. arXiv preprint arXiv:2109.00110, 2021.

Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and            Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu,
  Ye, K. Hilbert: Recursively building formal proofs with              Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E.,
  informal reasoning. arXiv preprint arXiv:2509.22819,                 Zhang, H., Gonzalez, J. E., and Stoica, I. Judging
  2025.                                                                LLM-as-a-judge with MT-bench and chatbot arena.
                                                                       In Conference on Neural Information Processing
Vaziri, M., Mandel, L., Spiess, C., and Hirzel, M. PDL:                Systems (NeurIPS), pp. 46595–46623, 2023. URL
  A declarative prompt programming language, October                   https://proceedings.neurips.cc/paper files/paper/2023/file/
  2024. URL http://arxiv.org/abs/2410.19135.                           91f18a1287b398d378ef22505bf41832-Paper-Datasets and
                                                                       Benchmarks.pdf.
Viennot, J., Baudart, G., Arias, E. J. G., and Lelarge, M.
  Minif2f in rocq: Automatic translation between proof               Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu,
  assistants - a case study. CoRR, abs/2503.04763, 2025.               C. H., Cao, S., Kozyrakis, C., Stoica, I., Gonzalez,
                                                                       J. E., Barrett, C., and Sheng, Y. SGLang: Efficient
Wang, H., Xin, H., Liu, Z., Li, W., Huang, Y., Lu, J., Yang,           execution of structured language model programs.
 Z., Tang, J., Yin, J., Li, Z., et al. Proving theorems re-            In Conference on Neural Information Processing
 cursively. arXiv preprint arXiv:2405.14414, 2024.                     Systems (NeurIPS), pp. 62557–62583, 2024. URL
                                                                       https://proceedings.neurips.cc/paper files/paper/2024/file/
Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi,
                                                                       724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf.
 E. H., Narang, S., Chowdhery, A., and Zhou, D. Self-
 consistency improves chain of thought reasoning in lan-             Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H.,
 guage models. In International Conference on Learn-                   and Wang, Y.-X. Language agent tree search unifies
 ing Representations (ICLR), May 2023. URL https:                      reasoning, acting, and planning in language models. In
 //openreview.net/forum?id=1PL1NIMMrw.                                 International Conference on Machine Learning (ICML),
                                                                       pp. 62138–62160, July 2024. URL https://proceedings.mlr.
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,              press/v235/zhou24r.html.
 Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
 prompting elicits reasoning in large language models. In
 Conference on Neural Information Processing Systems
 (NeurIPS), pp. 24824–24837, December 2022. URL
  https://proceedings.neurips.cc/paper files/paper/2022/hash/
  9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.
  html.

Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T.,
  Cao, Y., and Narasimhan, K.     Tree of thoughts:
  Deliberate problem solving with large language

                                                                12
                                       PPDL: LLM-Based Flows as Probabilistic Programs

A. Example Walk-Through                                             1 llm = "watsonx/meta-llama/llama-4-maverick-..."
                                                                    2 problem_statement = (
This section illustrates the execution of the PPDL pro-             3  "Write a function to find nth centered hexagonal number.\n"
gram from Figure 3 using two different inference algo-              4  "assert centered_hexagonal_number(10) == 271\n"
                                                                    5 )
rithms: Importance Sampling (IS) and Sequential Monte 6
Carlo (SMC). Both examples use 5 particles to solve the 7 messages = [
centered hexagonal number problem, where the task is to 8 {
                                                           9 "content": (
generate a Python function that computes the nth centered 10  "Generate an English plan for how to generate code "
hexagonal number using the formula 1 + 3n(n − 1).         11  f"for the following problem: { problem_statement }"
                                                                   12   ),
                                                                   13   "role": "user",
Importance Sampling execution (Table 4). In IS, all                14  }
                                                                   15 ]
particles execute independently from start to finish. Each
                                                                   16 response = completion(model=llm, messages=messages)
particle generates a plan (first row), which is then scored        17 plan = response.choices[0].message
using an LLM-as-a-judge constraint (second row). The par-          18 messages = messages + [ plan ]
                                                                   19 messages = messages + [
ticles then generate code solutions (third row), which are
                                                                   20  {
scored using a linter-based constraint (fourth row).               21   "content": (
                                                                   22    "Generate a complete executable Python function "
The key insight from this execution is how the scor-               23    "definition corresponding to the above plan and "
ing mechanism differentiates solution quality. Parti-              24    "problem. Generate only a single function definition."
cles 0 and 4 generate correct solutions with the formula           25   ),
                                                                   26   "role": "user",
1 + 3*n*(n-1), and receive very low penalty scores (ap-            27  }
proximately −0.69 after both scoring steps). Particles 1, 2,       28 ]
                                                                   29 response = completion(model=llm, messages=messages)
and 3 generate incorrect formulas and receive much higher
                                                                   30 solution_str = response.choices[0].message["content"]
penalty scores (ranging from −14.25 to −17.44).                    31 solution_match = re.fullmatch(
                                                                   32   r"(.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*",
When these scores are normalized into probabilities, par-          33   solution_str, flags=re.M
ticles 0 and 4 each have approximately 50% probability,            34 )
                                                                   35 solution = solution_match.group("code")
while the incorrect solutions have negligible probabilities
(less than 0.0004% combined). This demonstrates how IS
                                                                        Figure 7. Implementation in Python using LiteLLM of Figure 2.
uses scoring to amplify the probability of correct solutions.
Without scoring (i.e., using majority voting), the probabil-
ity of sampling a correct solution would be only 0.4, since             This execution demonstrates SMC’s ability to focus com-
only 2 out of 5 particles found the correct formula.                    putational resources on promising execution paths early in
                                                                        the computation, leading to higher-quality final results.
Sequential Monte Carlo execution (Table 5). SMC dif-
                                                                        The contrast between these two executions highlights the
fers from IS by introducing a resampling step after the first
                                                                        fundamental difference between IS and SMC: IS evaluates
scoring point. Initially, all 5 particles generate plans and re-
                                                                        all particles independently and uses scoring only at the end
ceive scores (first two rows). Particles 1 and 2 have signifi-
                                                                        to weigh results, while SMC actively steers the particle
cantly better scores (−0.000 000 002 and −0.000 000 009)
                                                                        population toward promising regions of the solution space
because their plans contain the correct formula, while the
                                                                        through intermediate resampling steps.
other particles have much worse scores.
The resampling step (indicated by the arrows in Table 5,                B. Possible alternatives for Figures 2 and 3
similar to Figure 1 from the introduction) duplicates the
promising particles 1 and 2 while discarding the poorly-                This section demonstrates how the PPDL programs from
scoring particles 0, 3, and 4. After resampling, the parti-             Figures 2 and 3 can be implemented using standard Python
cle population consists of three copies derived from par-               libraries. These implementations illustrate both the ex-
ticle 1 and two copies derived from particle 2. These re-               pressiveness advantages of PPDL and its orthogonality be-
sampled particles then continue execution to generate code              tween program and inference scaling startegy. We present
solutions (third row).                                                  four implementations: a baseline using LiteLLM, impor-
                                                                        tance sampling (IS) and sequential Monte Carlo (SMC)
Crucially, all five particles in the second phase now gen-
                                                                        variants with LiteLLM, and an SMC implementation using
erate correct solutions, because they all descended from
                                                                        LangChain that exploits parallelism.
particles with good plans. After the final scoring step, all
particles have identical scores (−0.69), resulting in a uni-            First, Figure 7 corresponds to the implementation of Fig-
form distribution where each solution has equal probability.            ure 2 using LiteLLM (https://github.com/BerriAI/litellm) to

                                                                   13
                                        PPDL: LLM-Based Flows as Probabilistic Programs

Table 4. Example of execution of the program provided in Figure 3 using Importance Sampling. The columns represent the state of the
different particles, and the rows represent the values of the variables through the execution. The circles visualize probability magnitudes
as in Figure 1. There is a probability of 0.999 999 453 to sample a correct solution (particles 0 and 4) in this distribution. If we ignore
the scores, this trace corresponds to a majority voting execution. In this case, the probability of sampling a correct solution is 0.4.

 Variable        Particle 0               Particle 1              Particle 2               Particle 3               Particle 4
 plan            ...    - The for-        ...       The for-      . . . The formula        . . . The formula        ...     - The cor-
                 mula ‘3*n*(n+1)          mula to calculate       for the nth cen-         for the nth cen-         rect formula for
                 + 1‘ is a more           the nth centered        tered hexagonal          tered hexagonal          the nth centered
                 direct representa-       hexagonal number        number is given          number is given          hexagonal number
                 tion of the nth          is given by: 1 +        by: 1 + 6 * (1 + 2       by: 1 + 6 * (1 + 2       is ‘1 + 3*n*(n-1)‘.
                 centered hexago-         6 ∗ (1 + 2 + ... +      + ... + n), which        + ... + n), which        ...
                 nal number. . . .        n), which simpli-       simplifies to 1 + 6      simplifies to 1 + 6
                                          fies to 1 + 6 ∗ (n ∗    * (n * (n + 1) / 2).     * (n * (n + 1) / 2).
                                          (n + 1)/2). . . .       ...                      ...
 score           −0.000 000 001           −14.750 000 035         −16.750 000 053          −14.250 001 005          −0.000 000 012
 (prob)          0.499 999 729            0.000 000 196           0.000 000 027            0.000 000 324            0.499 999 724
 solution        def                      def                     def                      def                      def
                 centered hex...          centered hex...         centered hex...          centered hex...          centered hex...
                 """                      """                     """                      """                      return 1 +
                 ...                      ...                     ...                      ...                      3*n*(n-1)
                 """                      """                     """                      """
                 return 3*n*(n-1)         if not                  # Calculate the          # Calculate the
                 + 1                      isinstance(n,           nth centered             sum of the first
                                          int):                   hexagonal number         n natural numbers
                                          raise                   using the formula        sum of n = n * (n
                                          TypeError("Input        return 1 + 6 * (n        + 1) // 2
                                          must be an              * (n + 1) // 2)
                                          integer.")                                       # Calculate
                                          if n < 0:                                        the nth centered
                                          raise                                            hexagonal number
                                          ValueError("Input                                result = 1 + 6 *
                                          must be a                                        sum of n
                                          non-negative
                                          integer.")                                       return result
                                          return 1 + 3 * n
                                          * (n + 1)

 score           −0.693 147 182           −15.443 147 216         −17.443 147 234          −14.943 148 186          −0.693 147 192
 (prob)          0.499 999 729            0.000 000 196           0.000 000 027            0.000 000 324            0.499 999 724


handle LLM calls. This code has the same structure as the                on promising particles after the first scoring point. The
PDL code but requires explicit message building and accu-                resample function samples n states from the distribution
mulation (Lines 7-15, and 18-28). It also requires accessing             of particle states.
the LLM response data structure (Lines 17 and 30).                   1 def resample(states, scores):
                                                                     2   n = len(states)
Figure 8 presents an implementation of Figure 3 using the
                                                                     3   d = Categorical(zip(states, scores))
IS inference algorithm. The implementation wraps the                 4   return [d.sample() for _ in range(n)]
baseline code in a loop (Line 8) that creates n indepen-
dent particles. Each particle maintains a log-probability                The SMC algorithm can be implemented using prompt pro-
score (Lines 26 and 44) that is used to construct a weighted             gramming frameworks like LangChain, as shown in Fig-
categorical distribution over solutions (Line 47). This im-              ure 10. This implementation exploits LangChain’s batch
plementation is purely sequential, in particular, each model             API (Lines 21 and 49) to execute particles in parallel, sig-
call is done one after the other.                                        nificantly reducing wall-clock time. The batch API sends
To implement Figure 3 with SMC, the IS code is restruc-                  multiple prompts to the LLM simultaneously.
tured as shown in Figure 9. The key difference is that parti-            Compared to these implementations, PPDL provides a
cle execution is split into two phases separated by a resam-             high-level abstraction that separates the probabilistic spec-
pling step (Line 31): the first loop (Lines 9-29) generates              ification from inference implementation details, allow-
and scores plans, the second loop (Lines 34-54) generates                ing the runtime to automatically optimize execution (e.g.,
code. This allows SMC to focus computational resources                   through parallelism) without programmer intervention.

                                                                    14
                                        PPDL: LLM-Based Flows as Probabilistic Programs

Table 5. Example of execution of the program provided in Figure 3 using SMC. The arrows represents the resampling step. In this
execution, all the particles compute a correct solution and they all have the same probability. After the the first factor, the resampling
step duplicates particles 1 and 2 who have a plan that contains the correct formula.

 Variable        Particle 0              Particle 1               Particle 2              Particle 3               Particle 4
 plan            ...      Simplifying    . . . By substitut-      ...       The for-      ...    Substituting      . . . The formula
                 this gives 1 + 3n(n     ing the sum of the       mula to calculate       the sum of the first     can be simplified
                 + 1) = 3nˆ2 + 3n +      first (n-1) natural      the nth centered        ‘n‘ natural num-         to 1 + 6(n(n+1)/2).
                 1. . . .                numbers into the         hexagonal number        bers into the for-       ...
                                         expression,       we     is given by: 1+6+       mula for the nth
                                         get ‘1 + 6*((n-          12 + ... + 6(n −        centered hexago-
                                         1)*n/2)‘, which          1), which simpli-       nal number gives
                                         simplifies to ‘1 +       fies to 3n2 − 3n +      ‘1 + 6 * (n * (n +
                                         3*n*(n-1)‘. . . .        1. . . .                1) / 2)‘. . . .
 score                −10.75               −0.000 000 002           −0.000 000 009              −15.99                 −18.75
 (prob)           0.000 010 723           0.499 994 610            0.499 994 607           0.000 000 057           0.000 000 004




 solution        def                     def                      def                     def                      def
                 centered hex...         centered hex...          centered hex...         centered hex...          centered hex...
                 """                     return 1 +               """                     return 1 +               """
                 ...                     3*n*(n-1)                ...                     3*n*(n-1)                ...
                 """                                              """                                              """
                 if not                                           # Calculate the                                  return 3*n**2 -
                 isinstance(n,                                    nth centered                                     3*n + 1
                 int) or n <= 0:                                  hexagonal
                 raise                                            number using
                 ValueError("n                                    the formula:
                 must be a                                        3nˆ2 - 3n + 1
                 positive                                         return 3*n**2 -
                 integer")                                        3*n + 1
                 return 1 +
                 3*n*(n-1)

 score                  −0.69                   −0.69                    −0.69                   −0.69                    −0.69
 (prob)                 0.2                     0.2                      0.2                     0.2                      0.2


C. Semantics
In this section, we present semantics of PPDL.                           body    ::= data:expr
                                                                                    | code:pdl ,lang:string
The syntax of PPDL using the flow-style of YAML is the                              | model:expr ,input:pdl
following:                                                                          | if:expr ,then:pdl ,else:pdl
                                                                                    | sequence:[pdl , . . . ,pdl ],join:join
 pdl   ::= { defs:{x:pdl , . . . ,x:pdl },                                          | while:expr ,repeat:pdl ,join:join
             body,                                                                  | function:types,return:pdl
             parser:parser ,                                                        | call:expr ,args:expr
             contribute:contribute,                                                 | factor:expr
             def:x                         }
                                                                         expr    ::= null | bool | number | string | ${jinja expr }
                                                                                    | [expr , . . . ,expr ] | {x:expr , . . . ,x:expr }

                                                                        A program is a block comprising a set of variable defini-
                                                                        tions, the block body (i.e., the instruction to evaluate), a
                                                                        parser to extract the result from the return value of the body,
                                                                        a flag indicating whether the result contributes to the con-
                                                                        text, and the name of a variable to store this result.


                                                                   15
                                       PPDL: LLM-Based Flows as Probabilistic Programs




                                                                1 llm = "watsonx/meta-llama/llama-4-maverick-..."
                                                                2 problem_statement = (
                                                                3  "Write a function to find nth centered hexagonal number.\n"
                                                                4  "assert centered_hexagonal_number(10) == 271\n"
                                                                5 )
1  llm = "watsonx/meta-llama/llama-4-maverick-..."
                                                                 6
2  problem_statement = (
                                                                 7 states = []
3   "Write a function to find nth centered hexagonal number.\n"
                                                                 8 scores = []
 4  "assert centered_hexagonal_number(10) == 271\n"
                                                                 9 for _ in range(n):
 5 )
                                                                10   score = 0
 6
                                                                11   messages = [
 7 solutions_and_scores = []
                                                                12    {
 8 for _ in range(n):
                                                                13     "content": (
 9   score = 0
                                                                14      "Generate an English plan for how to generate code "
10   messages = [
                                                                15      f"for the following problem: { problem_statement }"
11    {
                                                                16     ),
12     "content": (
                                                                17     "role": "user",
13      "Generate an English plan for how to generate code "
                                                                18    }
14      f"for the following problem: { problem_statement }"
                                                                19   ]
15     ),
                                                                20   response = completion(model=llm, messages=messages)
16     "role": "user",
                                                                21   plan = response.choices[0].message
17    }
                                                                22   messages = messages + [ plan ]
18   ]
                                                                23   constraint = (
19   response = completion(model=llm, messages=messages)
                                                                24       "This plan for the following problem is correct.\n"
20   plan = response.choices[0].message
                                                                25       f"{problem_statement}\n"
21   messages = messages + [ plan ]
                                                                26   )
22   constraint = (
                                                                27   score = score + utils.llm_judge(llm, plan, constraint)
23       "This plan for the following problem is correct.\n"
                                                                28   states.append(messages)
24       f"{problem_statement}\n"
                                                                29   scores.append(score)
25   )
                                                                30
26   score = score + utils.llm_judge(llm, plan, constraint)
                                                                31 states = resample(states, scores)
27   messages = messages + [
                                                                32
28    {
                                                                33 solutions_and_scores = []
29     "content": (
                                                                34 for messages in states:
30      "Generate a complete executable Python function "
                                                                35   score = 0
31      "definition corresponding to the above plan and "
                                                                36   messages = messages + [
32      "problem. Generate only a single function definition."
                                                                37    {
33     ),
                                                                38     "content": (
34     "role": "user",
                                                                39      "Generate a complete executable Python function "
35    }
                                                                40      "definition corresponding to the above plan and "
36   ]
                                                                41      "problem. Generate only a single function definition."
37   response = completion(model=llm, messages=messages)
                                                                42     ),
38   solution_str = response.choices[0].message["content"]
                                                                43     "role": "user",
39   solution_match = re.fullmatch(
                                                                44    }
40     r"(.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*",
                                                                45   ]
41     solution_str, flags=re.M
                                                                46   response = completion(model=llm, messages=messages)
42   )
                                                                47   solution_str = response.choices[0].message["content"]
43   solution = solution_match.group("code")
                                                                48   solution_match = re.fullmatch(
44   score = score + utils.score_errors_and_warnings(solution)
                                                                49     r"(.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*",
45   solutions_and_scores.append((solution, score))
                                                                50     solution_str, flags=re.M
46
                                                                51   )
47 dist = Categorical(solutions_and_scores)
                                                                52   solution = solution_match.group("code")
                                                                53   score = score + utils.score_errors_and_warnings(solution)
   Figure 8. Implementation in Python using LiteLLM of Figure 3 54 solutions_and_scores.append((solution, score))
    with IS probabilistic inference.                           55
                                                               56   dist = Categorical(solutions_and_scores)

                                                                    Figure 9. Implementation in Python using LiteLLM of Figure 3
                                                                    with SMC probabilistic inference.




                                                               16
                                         PPDL: LLM-Based Flows as Probabilistic Programs




 1 llm = WatsonxLLM(
 2     model_id="meta-llama/llama-4-maverick-...",
 3     ...
 4 )
 5 parser = StrOutputParser()
 6
 7 problem_statement = (
 8  "Write a function to find nth centered hexagonal number.\n"
 9  "assert centered_hexagonal_number(10) == 271\n"
10 )
11
12 plan_prompt = HumanMessage(
13   content=(
14    "Generate an English plan for how to generate code "
15    f"for the following problem: {problem_statement}"
16   )
17 )
18
19   plan_inputs = [[plan_prompt]] * n
20   plan_responses = llm.batch(plan_inputs)
21
22 states = []
23 scores = []
24 for response in plan_responses:
25   messages = [plan_prompt, response]
26   plan_text = parser.invoke(response)
27   constraint = (
28    "This plan for the following problem is correct.\n"
29    f"{problem_statement}\n"
30   )
31   score = utils.llm_judge(llm, plan_text, constraint)
32   states.append(messages)
33   scores.append(score)
34
35   states = resample(states, scores)
36
37 code_prompt = HumanMessage(
38  content=(
39   "Generate a complete executable Python function "
40   "definition corresponding to the above plan and "
41   "problem. Generate only a single function definition."
42  )
43 )
44
45   code_inputs = [
46     messages + [code_prompt] for messages in states
47   ]
48   code_responses = llm.batch(code_inputs)
49
50 solutions_and_scores = []
51 for response in code_responses:
52   solution_str = parser.invoke(response)
53   solution_match = re.fullmatch(
54     r"(.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*",
55     solution_str, flags=re.M,
56   )
57   solution = solution_match.group("code")
58   score = utils.score_errors_and_warnings(solution)
59   solutions_and_scores.append((solution, score))
60
61   dist = Categorical(solutions_and_scores)

     Figure 10. Implementation in Python using LangChain of Fig-
     ure 3 with SMC probabilistic inference.




                                                                   17
                                     PPDL: LLM-Based Flows as Probabilistic Programs

The body of a block can be an expression (data), some                given an environment S, the value v, and the contribute
code in Python, Shell, Jinja, or PDL, an LLM call with               flag contribute produces a new environment S ′ .
its input, a conditional, a sequence of blocks with a join
operator to gather result values, a loop with a join opera-          D. Models used in experiments
tor to gather the results of each iteration, a function defi-
nition, a function call, or a factor statement to update the         Table 6 shows the selection of LLMs used in experiments.
score. The join operator is a function that takes a list as
input and returns a value. In the concrete syntax of PPDL,
{join:{as:text}} corresponds to the string concatena-
tion, {join:{as:lastOf}} returns the last element of the                  Table 6. Large language models used in experiments.
list, and {join:{as:array}} is the identity function.
                                                                         Model                    Size              Dates
Types (type) are a subset of JSON Schema, the                                             total     active      cutoff      release
parsers (parser ) are regular expressions, and the contribute
                                                                         granite4-small   32b             9b   11/2024   10/2025
flag is defined as follows:                                              granite4-micro    3b             3b    4/2024   10/2025
          contribute   ::=    [] | [pdl context]                         gpt-oss-120b    117b             5b    6/2024    8/2025
                                                                         gpt-oss-20b      21b             4b    6/2024    8/2025
                                                                         llama4-maverick 400b            17b    8/2024    4/2025
The ideal semantics of a PPDL program p is defined by                    llama4-scout    109b            17b    8/2024    4/2025
the infinite number of executions of the weighted sampler
associated to the program p and the normalization of the
weights to obtain a categorical distribution:
                     {p/S ⇒∗ vi /Si }1≤i≤N
     wi = exp(Si′ [pdl score]) 1≤i≤N
                                             P
                                           W = 1≤i≤N wi
                                                                     E. Benchmark Code
            p/S ; λU. 1≤i≤N (wi /W ) × δvi (U )
                        P
                                                                     This section presents the complete PPDL programs used
 The reduction ⇒∗ is the transitive closure of the weighted          in the evaluation (Section 4). Each program demonstrates
sampler semantics and N → ∞.                                         how PPDL enables declarative specification of LLM work-
The semantics of weighted sampler p is defined Figure 11             flows with probabilistic inference through factor state-
by the reduction p/S ⇒ p or v /S ′ such that, given an               ments. The programs use LLM-as-a-judge and rule-based
environment S, the program p evaluates to the updated en-            constraints to guide inference toward correct solutions.
vironment S ′ , and rewrites into a new program or a value.
                                                                     E.1. GSM8k
The semantics of variable definitions is defined Figure 12
                             defs                                    The GSM8k program (Figure 16) solves grade-school math
by the reduction defs/S −−→ defs ′ /S ′ such that, given
an environment S, the definitions defs evaluates to the up-          problems through a simple three-step workflow. First, it
dated environment S ′ , and rewrites into a new set of defi-         prompts the LLM to solve the problem and generate the
nitions defs ′ .                                                     final answer prefixed by #### (Lines 2-8). Second, it ex-
                                                                     tracts the numerical answer using Python code (Lines 9-
The semantics of a block body b is defined Figure 13 by the          16). Third, it applies an LLM-as-a-judge factor (Line 18-
reduction b/S → b or v /S ′ such that, given an environ-             28) to score the solution’s correctness (Lines 18-28). The
ment S, the block body b evaluates to the updated environ-           fallback attribute (Lines 30-31) assigns a large negative
ment S ′ , and rewrites into a new block body or a value.            score if an error occurs, effectively filtering out malformed
The semantics of an expression e is defined Figure 14 by             responses during inference.
the reduction S ⊢ e ⇓ v such that, given an environ-
ment S, the expression e evaluates a value. The reduction            E.2. Math500
S ⊢ c ⇓l v uses the semantics of the language l to evalu-            The Math500 program (Figure 17) follows a similar struc-
ate the code c to a value v. Evaluation of expressions and           ture to GSM8k but uses a more sophisticated judging strat-
external code are not supposed to do side effects.                   egy. After generating the solution (Lines 2-5), it uses an
The semantics of parsing a value v by the parser parser              LLM-as-a-judge to perform line-by-line reasoning analysis
to extract a value v ′ is defined by the semantics of Python         (Lines 6-19), asking the judge to identify any errors in the
                                             parse                   solution’s reasoning. This more detailed validation is ap-
regular expressions and is noted parser , v −−−→ v ′ .
                                                                     propriate for the harder problems in Math500, which span
The semantics of contribute is defined Figure 15 by                  algebra, geometry, number theory, pre-calculus, and prob-
                               contrib
the reduction S, v, contribute −−−−→ S ′ such that,                  ability. Like GSM8k, it uses a fallback to handle failures.

                                                                18
                                     PPDL: LLM-Based Flows as Probabilistic Programs


         defs                                                      parse                              contrib
 defs/S −−→ {}/S1    block body/S1 → v/S2   parser , v −−−→ v ′ S2 , v ′ , contribute −−−−→ S3    S ′ = S3 [x ← v ′ ]
                                                                                               ′ ′
               {defs:defs,block body,parser:parser ,contribute:contribute,def:x }/S ⇒ v /S

                                                        defs
                                               defs/S −−→ defs ′ /S ′ defs ′ ̸= {}
                         {defs:defs,block body,parser:parser ,contribute:contribute,def:x }/S
                                                              ⇒
                        {defs:defs ′ ,block body,parser:parser ,contribute:contribute,def:x }/S ′

                                                 defs
                                       defs/S −−→ {}/S1   block body/S1 → b/S ′
                        {defs:defs,block body,parser:parser ,contribute:contribute,def:x }/S
                                                         ⇒
                            {defs:{},b,parser:parser ,contribute:contribute,def:x }/S ′


                                                 Figure 11. Semantics of a block


                                                                       pdl1 /S ⇒ pdl1′ /S1
                 defs                                                           defs
          {}/S −−→ {}/S               {x1 :pdl1 ,x2 :pdl2 , . . . ,xn :pdln }/S −−→ {x1 :pdl1′ ,x2 :pdl2 , . . . ,xn :pdln }/S1

                                                                                              defs
                            pdl1 /S ⇒ v1 /S1      {x2 :pdl2 , . . . ,xn :pdln }/S1 [x1 ← v1 ] −−→ defs/S ′
                                                                                defs
                                       {x1 :pdl1 ,x2 :pdl2 , . . . ,xn :pdln }/S −−→ defs/S ′


                                               Figure 12. Semantics of defs field.


E.3. MBPP                                                             E.5. Fever
The MBPP program (Figure 18) implements a multi-                      The Fever fact-checking program demonstrates PPDL’s
stage code generation workflow with three scoring points.             tool-use capabilities through a three-part workflow. Fig-
First, it generates an English plan (Lines 5-12) and scores           ure 20 defines a Wikipedia search tool using PPDL’s
it using an LLM-as-a-judge (Lines 13-26). Second, it                  function declaration (Lines 2-27), which wraps a Python
generates Python code based on the plan (Lines 27-49),                implementation that handles disambiguation and errors.
with regex parsing to extract code from markdown blocks               The tool signature is exposed to the LLM (Lines 28-30).
(Lines 41-43). Third, it applies multiple constraints: a rule-
                                                                      Figure 21 implements the evidence gathering loop. After
based check for function definitions (Line 50), a linter-
                                                                      the LLM generates a response with tool calls (Lines 2-7),
based score using flake8 warnings (Line 51), and a fi-
                                                                      the program iterates over each tool call using a for loop
nal LLM-as-a-judge for correctness (Lines 52-66). This
                                                                      (Lines 8-58). For each search request, it validates the topic
demonstrates PPDL’s ability to combine different types of
                                                                      using an LLM-as-a-judge (Lines 28-45) before calling the
constraints—LLM-based, rule-based, and tool-based—in
                                                                      search tool (Lines 46-48). This prevents wasting API calls
a single program. The program imports utility functions
                                                                      on irrelevant searches. The evidence from all searches is
from utils.pdl (Lines 1-3).
                                                                      joined with newlines (Lines 53-54).
E.4. LiveCodeBench                                                    Figure 22 performs the final verification. It first checks
                                                                      whether enough evidence has been gathered using an LLM-
The LiveCodeBench program (Figure 19) adapts the MBPP                 as-a-judge (Lines 1-18), then prompts the LLM to deter-
workflow for more challenging programming problems. It                mine if the claim is true or false based on the evidence
follows the same plan-then-code structure (Lines 5-12 for             (Lines 19-30). This three-part structure demonstrates how
planning, Lines 27-42 for code generation) but requires the           PPDL programs can be modularized across multiple files
generated function to be named main and use input() for               while maintaining a coherent probabilistic workflow.
reading inputs (Lines 30-32), matching the LiveCodeBench
format. The program applies three factor statements: for
the plan (Lines 13-26), for linter warnings (Lines 43-44),
and for solution correctness (Lines 45-58).


                                                                 19
                                 PPDL: LLM-Based Flows as Probabilistic Programs



      S⊢e⇓v                  S⊢p⇓c     S ⊢ c ⇓l v                   S ⊢ model ⇓ m  S ⊢ input ⇓ i   sample(m, i) = v
   data:e/S → v/S           code:p,lang:l/S → v/S                         model:model ,input:input/S → v/S

          v = j(vs)                              p1 /S ⇒ v1 /S1  sequence:[p2 . . . ,pn ],join:j vs+[v1 ] /S1 → p′ /S ′
sequence:[],join:j vs /S → v/S                             sequence:[p1 ,p2 . . . ,pn ],join:j vs /S → p′ /S ′

                                        p1 /S ⇒ p′1 /S1
       sequence:[p1 ,p2 . . . ,pn ],join:j vs /S → sequence:[p1′ . . . ,pn ],join:j vs /S1

                S ⊢ c ⇓ true   p1 /S ⇒ p′1 /S ′                            S ⊢ c ⇓ false  p2 /S ⇒ p′2 /S ′
              if:c,then:p1 ,else:p2 /S → p′1 /S ′                        if:c,then:p1 ,else:p2 /S → p′2 /S ′

                                               S ⊢ e ⇓ false
                                   while:e,repeat:p,join:j vs /S → j(vs)/S

                                    S ⊢ e ⇓ true            p/S ⇒ v/S ′
             while:e,repeat:p,join:j vs /S → while:e,repeat:p,join:j vs+[v] /S ′

                               S⊢e⇓w          S ′ = S[pdl score ← S[pdl score] + w]
                                             factor:e/S → data:""/S ′


                          function:t,return:p/S → function:t,return:p, scope:S/S

             S ⊢ f ⇓ function:t,return:p, scope:Sf         S ⊢ args ⇓ args ′  args′ ∈ t
         p/Sf [pdl context ← S[pdl context], pdl score ← S[pdl score]] + args ′ ⇒ v/Sf′
               S ′ = S[pdl context ← Sf′ [pdl context], pdl score ← Sf′ [pdl score]]
                                   call:f ,args:args/S → v/S ′

                   S ⊢ f ⇓ function:t,return:p, scope:Sf         S ⊢ args ⇓ args ′  args′ ∈ t
              p/Sf [pdl context ← S[pdl context], pdl score ← S[pdl score]] + args ′ ⇒ p′ /Sf′
                     S ′ = S[pdl context ← Sf′ [pdl context], pdl score ← Sf′ [pdl score]]
               call:f ,args:args/S → call:function:t,return:p ′ , scope:Sf′ ,args:args ′ /S ′


                                         Figure 13. Semantics of block bodies.




         c ∈ (null ∪ bool ∪ number string)               S ⊢ e ⇓jinja v                          {S ⊢ ei ⇓ vi }1≤i≤N
                    S⊢c⇓c                                S ⊢ ${e} ⇓ v                    S ⊢ [e1 , . . . ,en ] ⇓ [v1 , . . . ,vn ]

                                                   {S ⊢ ei ⇓ vi }1≤i≤N
                                    S ⊢ {x1 :e1 , . . . ,xn :en } ⇓ {x1 :v1 , . . . ,xn :vn }


                                          Figure 14. Semantics of expressions.




                                 ctx = S[pdl context] + [{content:v}]                           S ′ = S[pdl context ← ctx ]
               contrib                                                                     contrib
       S, v, [] −−−−→ S                                      S, v, [pdl context] −−−−→ S ′


                                     Figure 15. Semantics of contribute field.



                                                              20
                                          PPDL: LLM-Based Flows as Probabilistic Programs

 1 lastOf:                                                            1 lastOf:
 2 - >                                                                2 - "Problem: ${ problem }"
 3   Question: ${ problem }                                           3 - model: ${ model }
 4   Reason about this math problem and solve it. Generate            4   def: solution
 5   the final answer on the last line prefixed by ‘####‘             5   parameters: ${ parameters }
 6 - model: ${ model }                                                6 - defs:
 7   def: solution                                                    7     constraint: >
 8   parameters: ${ parameters }                                      8       Consider the solution below to the following math
 9 - lang: python                                                     9       problem. Read it line by line and reason about it
10   def: result                                                     10       to identify any errors in reasoning.
11   code: |                                                         11       If no issues are found, respond True. If any issue
12     from pdl.optimize.parse_number import (                       12       is found, respond False.
13       extract_math_answer                                         13
14     )                                                             14
15     result_line = solution.splitlines()[-1]                       15         Math Problem: ${ problem }
16     result = extract_math_answer(result_line)                     16
17                                                                   17       Solution: ${ solution }
18 - defs:                                                           18   factor:
19     constraint: >                                                 19     ${ stdlib.llm_as_judge(model, constraint, parameters) }
20       Is the solution below to the following math problem         20 - ${ solution }
21       correct?                                                    21 fallback:
22                                                                   22 factor: -100
23
24         Math Problem: ${ problem }
25
                                                                                Figure 17. PPDL program for Math500 benchmark.
26       Solution: ${ result }
27   factor:
28     ${ stdlib.llm_as_judge(model, constraint, parameters) }            is found or the token budget is exhausted (Line 53), with a
29 - ${ result }
30 fallback:
                                                                          maximum iteration limit (Line 54).
31 factor: -100
                                                                          Figure 25 performs final verification and result collection.
                                                                          After the loop terminates, it double-checks the proof cor-
           Figure 16. PPDL program for GSM8k benchmark.
                                                                          rectness (Lines 7-10) and logs the final status (Lines 11-
                                                                          24). If the proof is complete, it records the proof, the num-
                                                                          ber of steps, and the token usage (Lines 25-36); then raises
     E.6. MiniF2F                                                         an exception to signal success and terminate all parallel
     The MiniF2F theorem proving agent demonstrates PPDL’s                particles (Line 35). This early termination mechanism is
     capabilities for complex iterative workflows with external           crucial for efficiency: once any particle finds a valid proof,
     tool verification. This program implements the proof/repair          the entire computation stops, avoiding wasted token usage.
     loop described in the case study (Section 4): an LLM gen-            This three-part structure demonstrates PPDL’s ability to ex-
     erates Rocq/Coq proofs that are verified by the Rocq proof           press complex agent workflows with iterative refinement,
     assistant, with errors fed back to guide repair attempts.            external tool integration, probabilistic scoring based on in-
     Figure 23 shows the initialization phase. The program                termediate feedback, and coordinated termination across
     sets up logging infrastructure (Lines 2-7) and initializes           parallel executions.
     a proof checker that interfaces with the Rocq prover
     using the rocq-ml-toolbox (https://github.com/LLM4Rocq/              F. Case Study: Theorem Proving in Rocq
     rocq-ml-toolbox) (Lines 8-13). It then prompts the LLM
     with both the formal Rocq statement and an informal de-              We presents additional results for the case study.
     scription of the theorem to prove (Lines 24-51), providing           Figure 26 shows the number of problems solved as a func-
     an example proof format to guide the LLM’s output.                   tion of proof/repair steps for IS depending on the number of
     Figure 24 implements the core proof/repair loop using a              particles. It follows the same trends as SMC (see Figure 6).
     repeat block (Lines 1-55). In each iteration, the LLM gen-           Figure 27 shows the number of MiniF2F-Rocq problems
     erates a proof attempt (Lines 8-11), which is parsed to ex-          solved as a function of the number of tokens. IS and SMC
     tract the Rocq code (Lines 12-24). The proof is then veri-           consume k times more tokens to prove the first theorem
     fied by calling the Rocq checker (Lines 26-28). If verifica-         because they run k particles in parallel, but catch up with
     tion fails (Lines 30-47), a factor of −1 is applied (Line 39)        the IS@1 strategy which can only explore one trajectory.
     to score this attempt, and the error message is fed back to          So the more we increase the token budget, the more the
     the LLM to guide the next repair attempt (Lines 40-46).              probabilistic approaches are beneficial.
     This scoring mechanism allows SMC to prioritize particles
     with fewer errors. The loop continues until either a proof

                                                                     21
                                       PPDL: LLM-Based Flows as Probabilistic Programs


 1 defs:
 2   utils:
 3     import: utils.pdl
 4 lastOf:                                                        1 defs:
 5 - >                                                            2   utils:
 6   Generate an English plan for how to generate code for        3     import: ../mbpp/utils.pdl
 7   the following problem:                                       4 lastOf:
 8                                                                5 - >
 9   ${ problem }                                                 6   Generate an English plan for how to generate code for
10 - model: ${ model }                                            7   the following problem:
11   parameters: ${ parameters }                                  8
12   def: plan                                                    9   ${ problem }
13 - defs:                                                       10 - model: ${ model }
14     constraint: >                                             11   parameters: ${ parameters }
15       Consider the following plan for generating code for     12   def: plan
16       the coding problem below:                               13 - defs:
17                                                               14     judge_prompt: >
18      Coding Problem: ${ problem }                             15       Consider the following plan for generating code for
19                                                               16       the coding problem below:
20                                                               17
21      Plan: ${ plan }                                          18      Coding Problem: ${ problem }
22                                                               19
23                                                               20
24       Is the plan correct?                                   21       Plan: ${ plan }
25   factor:                                                    22
26     ${ stdlib.llm_as_judge(model, constraint, parameters) } 23
27 - >                                                          24       Is the plan correct?
28   Generate a complete executable Python function             25   factor:
29   definition corresponding to the above plan for the prompt. 26    ${ stdlib.llm_as_judge(model, judge_prompt, parameters) }
30   Generate a single function definition only and nothing     27 - >
31   else. Do not include docstrings.                           28   Generate a complete executable Python function
32                                                              29   definition corresponding to the above plan for the prompt.
33                                                              30   Generate a single function definition called ‘main‘ only
34   ${ problem }                                               31   and nothing else. Inputs to the function should be given
35 - model: ${ model }                                          32   using ‘input()‘.
36   def: response                                              33
37   parameters: ${ parameters }                                34   Generate a single function call to the main function.
38 - defs:                                                      35
39     solution:                                                36   ${ problem }
40       data: ${ response }                                    37 - model: ${ model }
41       parser:                                                38   parameters: ${ parameters }
42         regex: (.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*39   def: solution
43         spec: { code: string }                               40   parser:
44 - if: ${ solution == None }                                  41     regex: (.|\n)*‘‘‘python\n(?P<code>(.|\n)*?)‘‘‘(.|\n)*
45   then:                                                      42     spec: { code: string }
46     defs:                                                    43 - factor:
47       solution:                                              44     ${ utils.eval_number_of_warnings(response=solution) }
48         data:                                                45 - defs:
49           code : ${ response }                               46     judge_prompt: >
50 - factor: ${ utils.contains_functions(solution.code) }       47       Consider the following generated code for the
51 - factor: ${ utils.eval_number_of_warnings(solution) }       48       coding problem below:
52 - defs:                                                      49
53     constraint: >                                            50       Coding Problem: ${ problem }
54       Consider the following generated code for the coding 51
55       problem below:                                         52
56                                                              53       Code: ${ solution }
57       Coding Problem: ${ problem }                           54
58                                                               55
59                                                               56       Is the solution correct?
60      Code: ${ solution }                                      57   factor:
61                                                               58    ${ stdlib.llm_as_judge(model, judge_prompt, parameters) }
62                                                               59 - ${ solution.code | default("")}
63      Is the solution correct?                                 60 fallback:
64                                                               61 factor: -100
65   factor:
66     ${ stdlib.llm_as_judge(model, constraint, parameters) }
67 - ${ solution.code | default("")}
                                                                      Figure 19. PPDL program for LiveCodeBench benchmark.

          Figure 18. PPDL program for MBPP benchmark.



                                                                 22
                                          PPDL: LLM-Based Flows as Probabilistic Programs




                                                                       1 lastOf:
                                                                       2 - ${ problem }
                                                                       3 - model: ${ model }
                                                                       4   def: response
                                                                       5   modelResponse: action
                                                                       6   parameters: ${ dict(parameters, tools=tools)}
                                                                       7   parser: json
                                                                       8 - def: evidence
                                                                       9   for:
                                                                      10     tool_call: ${ action.choices[0].message.tool_calls }
                                                                      11   repeat:
                                                                      12     text:
                                                                      13     - if: ${ tool_call.function.name == "search"}
 1 defs:                                                              14       then:
 2   search:                                                          15         defs:
 3     description: Wikipedia search                                  16           args:
 4     function:                                                      17             data: ${ tool_call.function.arguments }
 5       topic:                                                       18             parser: json
 6         type: string                                               19           topic:
 7         description: Topic to be searched                          20             text: ${ args["topic"] }
 8     return:                                                        21             fallback:
 9       def: result                                                  22               defs:
10       lang: python                                                 23                 args:
11       code: |                                                      24                   data: ${ args }
12         import warnings, wikipedia                                 25                   parser: json
13         warnings.simplefilter("ignore")                            26               text: ${ args["topic"] }
14                                                                    27         lastOf:
15           def main(topic: str, *args, **kwargs) -> str:            28         - defs:
16             try:                                                   29             judge_prompt: >
17               return wikipedia.summary(topic)                      30               Is the topic below a good topic to search
18             except wikipedia.DisambiguationError as d:             31               in order to answer the following question:
19               return (                                         32
20                 f"\"{topic}\" may refer to one of {d.args[1]}."33                     Question: ${ problem }
21                 "Please retry the search with a more"          34
22                 "specific subject."                            35
23               )                                                36                     Topic:
24             except wikipedia.WikipediaException as e:          37
25               return str(e)                                    38                     ${ topic }
26                                                                    39
27          result = main(topic)                                      40
28    tools:                                                          41                Respond with only (’true’/’false’).
29      data:                                                         42            factor: >
30      - ${ search.signature }                                       43              ${ stdlib.llm_as_judge(model,
                                                                      44                                     judge_prompt,
                                                                      45                                     parameters) }
     Figure 20. PPDL program for Fever benchmark (Part 1: tool def-   46          - call: ${ search }
     inition).                                                        47            args:
                                                                      48              topic: ${ topic }
                                                                      49        else:
                                                                      50          factor: -100
                                                                      51        fallback:
                                                                      52          factor: -100
                                                                      53    join:
                                                                      54      with: "\n"
                                                                      55    fallback:
                                                                      56      factor: -100

                                                                           Figure 21. PPDL program for Fever benchmark (Part 2: evidence
                                                                           gathering).




                                                                      23
                                        PPDL: LLM-Based Flows as Probabilistic Programs




                                                                   1 defs:
                                                                   2   logger:
                                                                   3     aggregator:
                                                                   4       file:
                                                                   5         ${ logdir }/logs_${name}_${pdl_particle_id}.txt
                                                                   6       flush: true
                                                                   7       mode: w
                                                                   8   checker:
                                                                   9     lang: python
                                                                  10     code: |
                                                                  11       from proof_checker import Checker
                                                                  12       workspace=agent_params.get("workspace", "")
                                                                  13       result = Checker(workspace=workspace)
                                                                  14   tokens: 0
 1 - defs:                                                        15 lastOf:
 2     judge_prompt: >                                            16 - text: |
 3       Is the evidence below enough to support or refute >      17
 4       the following problem:                                   18     --------------------------------------------------
 5                                                                19     | STARTING PROOF.                                |
 6        ${ problem }                                            20     --------------------------------------------------
 7                                                                21     Goal: ${ formal_statement }
 8                                                                22   contribute: [logger, stdout]
 9        Evidence:                                               23 - text: |
10                                                                24     Please provide a proof for the following Rocq/Coq
11        ${ response }                                                       statement:
12                                                                25
13        ${ evidence }                                           26      ‘‘‘Rocq
14                                                                27
15                                                                28      ${ formal_statement }
16       Respond with only (’true’/’false’).                   29         ‘‘‘
17   factor:                                                   30         It corresponds to the following informal statement:
18     ${ stdlib.llm_as_judge(model, judge_prompt, parameters) }               ‘‘‘${informal_statement}‘‘‘
19 - model: ${ model }                                         31
20   parameters: ${ parameters }                               32         Please use Coq/Rocq and enclose the proof in triple
21   input: |                                                                  backticks.
22     Consider the evidence:                                  33
23     ${ response }                                           34         As an example, if the statement to prove is
24     ${ evidence }                                           35
25                                                                36      ‘‘‘Rocq
26      Is the following statement true or false?                 37      Theorem example (a b : nat) (h : a = b + 1) : a > b.
27      ${ problem }                                              38      ‘‘‘
28                                                                39
29      Respond with only (’true’/’false’).                       40      then your final proof snippet should follow this
                                                                               format:
                                                                  41
     Figure 22. PPDL program for Fever benchmark (Part 3: final   42      ‘‘‘Rocq
     verification).                                               43      From Stdlib Require Import Lia.
                                                                  44
                                                                  45      Theorem example (a b : nat) (h : a = b + 1) : a > b.
                                                                  46      Proof.
                                                                  47        rewrite h.
                                                                  48        lia.
                                                                  49      Qed.
                                                                  50      ‘‘‘
                                                                  51      The last ‘Rocq‘ code block will be parsed as your
                                                                               final proof.
                                                                  52    contribute: [logger, context]

                                                                       Figure 23. PPDL program for MiniF2F benchmark (Part 1: ini-
                                                                       tialization and prompt).




                                                                  24
                                       PPDL: LLM-Based Flows as Probabilistic Programs




                                                                 1   - text: |
 1 - repeat:                                                     2
 2     text:                                                     3       Double-checking proof correctness for ${name}...
 3     - text: |                                                 4       Current status: ${ result["status"] }
 4         --------------------------------------------------    5
 5         | [${pdl_particle_id}] ITERATION: ${i}           |    6   contribute: [logger, stdout]
 6         --------------------------------------------------    7 - defs:
 7       contribute: [logger, stdout, stderr]                    8     verification:
 8     - model: ${ model_params["model_id"] }                    9       lang: python
 9       parameters: ${ model_params }                          10       code: result = checker.verify_proof(name,
10       def: reasoning                                                       formal_statement, response["rocq"])
11       contribute: [context, result, logger]                  11 - text: |
12     - defs:                                                  12
13         response:                                            13       --------------------------------------------------
14           data: ${ reasoning }                               14       | PROOF ${ "COMPLETE" if verification["status"] == "
15           parser:                                                          Complete" else "FAILED. " } |
16             regex:                                           15       --------------------------------------------------
17               (.|\n)*‘‘‘(coq|Coq|rocq|Rocq|)\n(?P<rocq       16       Status: ${verification["status"]}
                      >(.|\n)*?)‘‘‘(.|\n)*                      17       Goal: ${ formal_statement }
18             spec: { rocq: string }                           18
19       if: ${ response == None }                              19       Proof:
20       then:                                                  20       ‘‘‘rocq
21         defs:                                                21       ${ response["rocq"] }
22           response:                                          22       ‘‘‘
23             data:                                            23
24               rocq: ${ formal_statement }                    24   contribute: [logger, stdout]
25     - defs:                                                  25 - defs:
26         result:                                              26     result:
27           lang: python                                       27       data:
28           code: result = checker.check(response["rocq"])     28         status: ${ verification["status"] }
29         prompt:                                              29         proof: ${ response["rocq"] }
30           match: ${ result["status"] }                       30         steps: ${ i + 1 }
31           with:                                              31   lang: python
32           - case: Error                                      32   code: |
33             then:                                            33     if (verification["status"] == "Complete"):
34               lastOf:                                        34       results.append((result, pdl_usage))
35               - text: |                                      35       raise Exception("success")
36                                                              36   contribute: [result, logger]
37                   PROOF ERROR - Attempting to fix ${name}
                          ...                                        Figure 25. PPDL program for MiniF2F benchmark (Part 3: veri-
38                 contribute: [logger, stdout]                      fication and result collection).
39               - factor: -1
40               - text: |
41                   Your previous Rocq/Coq proof failed to
                          compile with these verifier
42                   errors:
43
44                    ${result["error"]}
45
46                   Please fix your proof.                                                            80
                                                                           Number of Theorems Solved




47                 contribute: [logger, result]
48          tokens:
                                                                                                       60
49            lang: python
50            code: |
51              result = pdl_usage.completion_tokens +                                                 40
                     pdl_usage.prompt_tokens                                                                                                          IS@40
52        text: ${ prompt }                                                                            20                                             IS@20
                                                                                                                                                      IS@10
53    until: ${ (result["status"] == "Complete") or (tokens >
                                                                                                                                                      IS@5
           agent_params["max_tokens"])}                                                                0                                              IS@1
54    maxIterations: ${ agent_params["max_depth"] }
55    index: i                                                                                              0   10   20    30     40        50   60   70      80
                                                                                                                          Number of Steps

     Figure 24. PPDL program for MiniF2F benchmark (Part 2:          Figure 26. Number of MiniF2F-Rocq problems solved as a func-
     proof/repair loop).                                             tion of proof/repair steps. Each curve shows the mean over three
                                                                     runs, with shaded regions indicating one standard deviation.




                                                                25
                                                                 PPDL: LLM-Based Flows as Probabilistic Programs




                                  100
      Number of Theorems Solved




                                  80


                                  60


                                  40
                                                                                   SMC@40
                                                                                   SMC@20
                                  20
                                                                                   SMC@10
                                                                                   SMC@5
                                   0                                               IS@1

                                        103           104              105           106
                                              Token Budget (prompt + completion)



                                  80
      Number of Theorems Solved




                                  60


                                  40
                                                                                    IS@40
                                  20                                                IS@20
                                                                                    IS@10
                                                                                    IS@5
                                   0                                                IS@1

                                        103           104              105           106
                                              Token Budget (prompt + completion)

Figure 27. Number of MiniF2F-Rocq problems solved as a func-
tion of the number of tokens.




                                                                                            26
