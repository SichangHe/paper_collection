                                                       LLMs Lean on Priors, Not Programming Language Semantics


                                                      Aditya Thimmaiah 1 Jiyang Zhang 1 Jayanth Srinivasa 2 Junyi Jessy Li 1 Milos Gligoric 1


                                                                   Abstract                                      1. Introduction
                                                                                                                 Modern large language models (LLMs) increasingly solve
                                              Recent work asks whether large language mod-                       programming tasks that appear to require reasoning about
                                              els (LLMs) condition their reasoning on explicit                   program behavior, from predicting outputs (Gu et al., 2024;
arXiv:2510.03415v3 [cs.PL] 29 May 2026




                                              rules rather than statistical regularities from pre-               Ni et al., 2024) to repairing and generating (Huang et al.,
                                              training. Program execution provides a canoni-                     2025) code. This raises a natural question: do such models
                                              cal instance: formal semantics define behavior                     rely primarily on statistical regularities acquired during pre-
                                              through symbolic transition rules that can be sys-                 training, or can they flexibly condition their reasoning on
                                              tematically altered under distribution shift. We                   explicitly provided behavioral rules?
                                              investigate whether LLMs can condition their rea-
                                              soning on formal semantics through program exe-                    Consider an integer arithmetic operation with two alternative
                                              cution and introduce PLS EMANTICS B ENCH, pair-                    semantics for the standard ‘+’ symbol, a scenario frequently
                                              ing featherweight C programs with two semantic                     encountered in operator overloading (Ravasi & Vasconcelos,
                                              systems—small-step operational semantics and K                     2020; Triton, 2026). Under the first, 2+2 behaves conven-
                                              semantics—and probing four capabilities: com-                      tionally as addition; under the second, the same symbol is
                                              posing rules for final states, selecting rules when                defined to perform subtraction. A system that reasons from
                                              state is unmutated, sustaining such conditioning                   syntax alone (learned priors) would produce the same an-
                                              over long traces, and following supplied rules                     swer in both cases. A system that conditions on the supplied
                                              under novel semantics. To decouple semantic                        semantic definitions would change its behavior immediately.
                                              reasoning from syntactic familiarity, we redefine                  This contrast captures a broader scientific issue:
                                              familiar operators to induce symbol-meaning con-                   Can LLMs adapt their reasoning to externally specified
                                              flict and introduce novel symbols defined only                     formal systems, even when those systems conflict with en-
                                              through the supplied rules, and stress-test models                 trenched priors learned from data?
                                              on Human-Written, LLM-Translated, and Fuzzer-                      Formal semantics (Pierce, 2002) offers a uniquely controlled
                                              Generated splits with increasing structural com-                   setting for studying this question. The semantics of a pro-
                                              plexity. Across 11 frontier LLMs, strong final-                    gramming language consist of symbolic transition rules gov-
                                              state accuracy under standard semantics (up to                     erning program-state evolution. Correct execution requires
                                              90%) drops sharply—by as much as 40–60%                            repeatedly selecting and composing such rules over many
                                              points—under semantic mutations and increasing                     steps. Crucially, these rules can be modified without altering
                                              structural complexity. Only a handful of models                    surface syntax, allowing one to separate reliance on lexical
                                              achieve non-zero long-horizon conditioning accu-                   cues from genuine conditioning on semantics. Furthermore,
                                              racy, and even the best systems reach just 35%.                    formal semantic rules: (1) are atomic with uniform granu-
                                              Together, these results suggest that contemporary                  larity, enabling systematic comparison across programs and
                                              LLMs often rely on pretrained lexical associa-                     model predictions, and (2) specify behavior mathematically
                                              tions rather than systematically conditioning on                   rather than in natural language, reducing ambiguity between
                                              supplied formal rules. PLS EMANTICS B ENCH is                      intended execution and model instructions.
                                              publicly available at https://EngineeringS
                                              oftware.github.io/PLSemanticsBench.                                Tested hypotheses. We use program execution as a lens
                                                                                                                 for analyzing formal semantic rule-conditioned reasoning
                                                                                                                 in LLMs. Rather than asking whether models can execute
                                          1
                                            The University of Texas at Austin 2 Cisco Research. Correspon-       programs in familiar languages, we ask whether they can—
                                         dence to: Aditya Thimmaiah <auditt@utexas.edu>.                         alter their reasoning under novel formal semantics, apply
                                                                                                                 individual rules at fine granularity, and sustain such con-
                                         Proceedings of the 43 rd International Conference on Machine            ditioning across long execution horizons (e.g., loops and
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026            nested control flow). This yields four concrete hypotheses
                                         by the author(s).

                                                                                                             1
                                LLMs Lean on Priors, Not Programming Language Semantics

                                                                      1
about model capabilities:                                             2
                                                                          <program>
                                                                          <stmt>
                                                                                      ::= <stmt>
                                                                                      ::= <assgn_stmt>
 ⋆ H1 (Global Rule Conditioning): Models can combine                  3
                                                                      4
                                                                          <assgn_stmt>::= <id>'='<exp>';'
                                                                          <exp>       ::= <literal> | <exp>'+'<literal>
many rule applications to correctly predict final states.             5   <literal>   ::= <digit> | <literal> <digit>
                                                                      6
 ⋆ H2 (State-Free Rule Conditioning): Models can follow               7
                                                                          <id>
                                                                          <digit>
                                                                                      ::= <letter> | <id> <letter>
                                                                                      ::= '0' | ... | '9'
rules correctly under state-mutation free execution.                  8   <letter>    ::= 'a' | ... | 'z'

 ⋆ H3 (Long-Horizon Rule Conditioning): Models can fol-               (a) Syntax in Backus-Naur Form (McCracken & Reilly, 2003).
low formal rules consistently across long execution traces.
                                                                      S-A S S I G N S T E′ P        S-A S′ S I G N                 E-A D D
 ⋆ H4 (Rule Conditioning Under Semantic Shift): Models                    ⟨e, σ⟩ →
                                                                                 − E ⟨e , σ⟩            σ = σ[x 7→ v]                    v3 = v1 +v2
continue to follow supplied rules under novel semantics.
                                                                                               ′                         ′
                                                                       ⟨x = e, σ⟩ →
                                                                                  − S ⟨x = e , σ⟩   ⟨x = v, σ⟩ →
                                                                                                               − S ⟨ϵ, σ ⟩            ⟨v1 +v2 , σ⟩ →E v3

To test these hypotheses, we introduce PLS EMANTICS B ENCH,           E-A D D L E F T S T E′ P       E-A D D R I G H T S T′ E P             E-I D
                                                                           ⟨e1 , σ⟩ →
                                                                                    − E ⟨e1 , σ⟩           ⟨e2 , σ⟩ →
                                                                                                                    − E ⟨e2 , σ⟩              σ(x) = v
which pairs a featherweight (Harper, 2016) C program-                  ⟨e1 +e2 , σ⟩ →
                                                                                           ′
                                                                                    − E ⟨e1 +e2 , σ⟩ ⟨v1 +e2 , σ⟩ →
                                                                                                                  − E ⟨v1 +e2 , σ⟩
                                                                                                                                  ′
                                                                                                                                            ⟨x, σ⟩ →E v
ming language C⋆ with two formal semantic systems—the
                                                                     (b) Semantics in Small-step operational semantics (Plotkin, 2004).
fine-grained small-step structural operational semantics
(S) and the coarser rewriting-based K semantics (Ros, u &            Figure 1. Formal syntax and semantics of an example language L.
S, erbănută, 2010). The benchmark probes the hypotheses via
three complementary tasks—predicting final program states            benchmark for assessing when LLMs adapt their behavior
(PredState), selecting semantic rules governing execution            to externally specified formal systems.
in absence of state mutation (PredRule), and generating
full execution traces to probe long-horizon rule application         2. Background
(PredTrace)—while using semantic mutations and program-
complexity splits as stressors for robustness.                       The semantics of a programming language defines pro-
                                                                     gram behavior. Structural operational semantics specifies
Reliance on learned priors vs supplied rules. We dis-                semantics via inference rules that govern transitions between
entangle reliance on supplied rules versus learned priors            configurations, each pairing a program fragment with its
along two orthogonal axes: semantic mutation and program-            execution state. We use small-step semantics (S), where
complexity shifts. A key feature enabled by formal se-               each rule represents one atomic computation and execution
mantics is nonstandard variants that systematically per-             arises from repeated rule applications. Rules are written
turb symbol meanings. In KeywordSwap, common op-                     in Gentzen-style inference notation (Gentzen, 1964), with
erators exchange their behavior, creating direct conflicts           premises and side conditions above the fraction bar and
with pretrained priors. In KeywordObf, familiar syntax is            conclusions below.
replaced with novel symbols whose meanings are defined
only through the supplied rules. Models are additionally             We illustrate semantics formal- Table 1. Notation primer.
evaluated on human-written, LLM-translated, and fuzzer-              ization in S using a simple im-          Notation       Definition

generated programs with varied structural complexity, stress-        perative language L whose syn-               σ          Program state
ing deep control flow and unusual data-flow patterns.                tax (Figure 1a) includes assign-             s          Statement
                                                                                                                  x          Int variable
                                                                     ments and integer expressions                e          Int expression
Choice of programming language. We use C⋆ rather than                with addition. Table 1 summa-                v          Int literal
indentation-sensitive languages such as Python, whose con-           rizes the notation used in its for-
                                                                                                          ⟨operation, σ⟩ Configuration
                                                                                                              σ[x 7→ v]      Store v in x
crete syntax requires recovering block structure (Adams,             malization (Figure 1b). Config- ⟨e, σ⟩ →   − E ⟨e′ , σ⟩ Expression-step
2013) from layout before abstract syntax can be constructed,         urations take the form ⟨c, σ⟩,
                                                                                                                      ′    ′
                                                                                                                − S ⟨s , σ ⟩ Statement-step
                                                                                                         ⟨s, σ⟩ →
                                                                                                               ⟨ϵ, σ⟩        NOP
thereby entangling syntactic recovery with semantic reason-          where c ranges over statements
ing. Explicit block delimiters ‘{}’ in C⋆ avoid this confound,       (s) and expressions (e), and the state maps variables (x) to
allowing us to isolate the model’s ability to condition on           integer values (v).
formal semantics defined over the abstract syntax.                                                           r
                                                                     Expression transitions ⟨e, σ⟩ −  →E ⟨e′ , σ⟩ apply a single rule
Our experiments across a broad set of frontier and open-             to reduce an expression and record the ordered list of rules
weight models show that while several benefit from access            r used so far; they do not mutate state and terminate in a
to formal rules under standard semantics, performance de-            literal under transitive–reflexive closure. Statement transi-
teriorates sharply under semantic mutations, increased rule                       r
                                                                     tions ⟨s, σ⟩ −
                                                                                  →S ⟨s′ , σ ′ ⟩ may update the state and iterate until
granularity, and long execution horizons, exposing system-           reaching NOP (⟨ϵ, σ⟩). For example, S-A SSIGN S TEP prop-
atic limits in current models’ ability to sustain reasoning          agates evaluation through an assignment by stepping the
conditioned on externally specified formal systems.                  right-hand-side expression, while S-A SSIGN applies once
By framing program execution as a controlled probe of                that expression reduces to a literal and commits the value
rule-conditioned reasoning, we provide a semantics-driven            to the state; together, such rules illustrate how programs
                                                                     execute by repeated configuration transitions.

                                                                 2
                                        LLMs Lean on Priors, Not Programming Language Semantics

         1     Standard C* Program       2    Mutations (H4)                                                              3           4     Output Trace
                                             None                     Transformed C* K Semantics & Program
         1|    int n;                                                                                                K-framework
                                             KeywordSwap                                                                                     PredTrace
         2|    n = 1;
         3|    while (n < 5) {               KeywordObf                                                                               [
         4|       if (n > 4) {                                                                                                            ExecutionState (
         5|          break;                                                                                                                  rule=‘Rule 36’,
                                         6     PredState (H1)                            5                 8   PredTrace (H3)
         6|       };                                                                                                                         state={’n’ : 0}
         7|       n = (n + 1);           What are the final values                                         What is the execution          ),
                                                                                 Transformed C*
         8|    };                        of all the variables after                                        trace of the given C*          ExecutionState (
                                                                                    Program
                                         the program terminates                                            program                           rule=‘Rule 21’,
          Standard C* EBNF Syntax
                                         …                                  1|   int n;                    …                                 state={’n’ : 1}
         …
                                                                            2|   n " 1;                                                   ),
         <aexp> ::= <id>
                                                                            3|   # (n $ 5) {                                              ExecutionState (
                | <literal>
                                                                            4|      % (n & 4) {                                              rule=‘Rule 24’,
                | “+” <aexp>                  <ans>                                                                                          state={’n’ : 1}
         …                                        <n> 5 </n>                5|         ';
                                                                                                                                          ), PredRule
                                              </ans>                        6|      };
           Standard C* Small-Step
                                                                            7|      n " (n ! 1);
         …                                                                                                                                ExecutionState (
         Rule 5 := {                                                        8|   };                                                          rule=‘Rule 1’,
                                         7     PredRule (H2)
                 v3 = v1 + v2                                                                                                                state={’n’ : 2}
            <v1 + v2,𝜎> → <v3,𝜎>         What semantic rules are                                           <ans>                           ),
         }                               used to evaluate?                                                  <step>                        ExecutionState (
         …
                                         n " (n ! 1);                            Transformed C*              <rule>36<rule>                  rule=‘Rule 3’,
             Standard C* K Semantics                                               K Semantics               <program_state>                 state={’n’ : 2}
                                         The program state is:                                                <n>0</n>                     ),
         module C*-SYNTAX                                                  module C*-SYNTAX                  </program_state>             ExecutionState (
                                         { ‘n’ : 2 }
          …                                                                 …                               </step>                          rule=‘Rule 21’,
                                         …
          syntax AExp ::=                                                   syntax AExp ::=                 <step>                           state={’n’ : 3}
                           “+” AEXP                                                       “!” AEXP           <rule>21</rule>              ),
          …                                                                 …                                <program_state>              …
         endmodule                            <ans>                        endmodule                          <n>1</n>                    ExecutionState
         module C*                                                         module C*                                                           PredState (
                                                <rule>1</rule>                                               </program_state>                rule=‘Rule 35’,
           imports C*-SYNTAX                    <rule>3</rule>              imports C*-SYNTAX               </step>                          state={’n’ : 5}
           rule I1 + I2 => I1 +Int I2           <rule>21</rule>             rule I1 ! I2 => I1 +Int I2       …                            )
           …                                  </ans>                        …                              </ans>                     ]


Figure 2. Overview of the PLS EMANTICS B ENCH construction workflow and evaluation tasks designed to probe rule-conditioned
reasoning under formal semantics. Each program is written in C⋆ with EBNF syntax and paired with two semantic systems—small-step
operational semantics (S) and K semantics (K) ( 1 ). The standard semantics are systematically transformed into two nonstandard variants,
KeywordSwap and KeywordObf, which preserve rule structure while perturbing the symbol–meaning mapping ( 2 ). These semantics are
used to derive ground-truth execution traces for each transformed program ( 3 – 4 ). The transformed program and its semantics ( 5 ) are
then provided to models as prompts. Tasks ( 6 – 8 ) range from predicting final states (PredState; H1), to selecting applicable rules when
state does not mutate (PredRule; H2), to generating full execution traces to test long-horizon rule conditioning (PredTrace; H3). An
analogous pipeline is used for S by replacing the execution engine, enabling controlled comparisons across semantic formalisms and
shifts (H4).


Definition 2.1 (Statement Execution). Let s be a statement                                execution of P under a given formalization Ψ and an initial
derived from a given grammar G that is semantically valid                                 program state σ0 compositionally using Definition 2.1 as:
under an S formalization Ψ, and let R be the set of all rule                              JPKΨ (σ0 ) = J[s0 , . . . , sn ]KΨ (σ0 ) ≜ (Js0 KΨ ⊗. . .⊗Jsn KΨ )(σ0 )†‡
names in Ψ. Suppose that under Ψ and an initial program
state σ0 , the statement s reduces to a NOP configuration in                              Here, ‘⊗’ is a left-associative sequencing operator defined
n statement-steps: ⟨s, σ0 ⟩ −→
                               r1      ′       r2
                                   S ⟨s , σ1 ⟩ −
                                                         rn
                                                →S . . . −→ S ⟨ϵ, σn ⟩.
                                                                                          by direct style Kleisli composition (Wadler, 1995) as fol-
For each i ∈ [1, n], ri ∈ R denotes the ordered list of rules
                              ∗                                                           lows:
required for the ith statement-step, with elements indexed as                            (JsA KΨ ⊗ JsB KΨ )(σ) ≜ let (σA , τA ) = JsA KΨ (σ) in
ri,j where j ∈ [0, |ri |), and σi denotes the program state after                                                let (σB , τB ) = JsB KΨ (σA ) in
the ith -step. Let ‘⊕’ denote the standard list concatentation                                                         (σB , τA ⊕ τB )
operator. We then define statement execution of s under Ψ                                where σA and σB are the resulting states of JsA KΨ (σ)
and an initial program state σ0 as a pair:                                               and JsB KΨ (σA ) respectively, and τA and τB are the cor-
                        Ln L|ri |−1
JsKΨ (σ0 ) ≜ ( σn ,       i=1   j=0 [(σi , ri,j )]), ri,j ∈ R                            responding execution traces. Consequently, JPKΨ (σ0 ) =
                                                                                                i=0 τi ), where σn is the final state—obtained by exe-
                                                                                         (σn , ⊕n
               |{z} |             {z             }
          resulting state   execution trace
                                                                                            †
                                                                                              Statements s0 , . . . , sn are sequenced at the program level as
Definition 2.2 (Program Execution). Let P be a program                                    single units, regardless of whether their execution expands into
derived from a given grammar G that can be parsed into an                                 nested statements (e.g., loops).
                                                                                            ‡
ordered list of statements [s0 , . . . , sn ]. We define program                              The empty program denotes the base case of the compositional
                                                                                          definition: ∀σ.J[ ]KΨ (σ) ≜ (σ, [ ]).


                                                                                     3
                                          LLMs Lean on Priors, Not Programming Language Semantics

Table 2. Median code-complexity statistics of our dataset splits. Control-flow complexity is characterized using extended cyclomatic
complexity (ΩCC ), maximum nested if–else (ΩIf ) and nested loop (ΩLoop ) depths, maximum taken nested if–else (Ω̂If ), and taken nested
loop (Ω̂Loop ) depths. Program size complexity is measured using lines of code (ΩLoc ), Halstead metrics Volume (ΩVol ) and Vocabulary
(ΩVoc ), and execution trace length (Ω̂Trace ). Data-flow complexity is analyzed using DepDegree (ΩDD ) and the total number of assignments
to variables in execution traces (Ω̂Assign ). Metrics computed under dynamic-analysis are shown with a hat.
                                                #Tokens*                             Control-flow                     Data-flow                      Size
                                       □,std       □,swap     □,obf
  Dataset Split       #Programs      Ψ         Ψ            Ψ         ΩCC      ΩIf       ΩLoop      Ω̂If   Ω̂Loop   ΩDD    Ω̂Assign   ΩLoc    ΩVol      ΩVoc    Ω̂Trace

  Human-Written           162          81         81         142**      3       1          1         1       1      12        9        19     320        22       20
  LLM-Translated          165          538        538        873**      9       1          1         1       1      48       62       106      2K        35      180
  Fuzzer-Generated        165         9183       9183       19016**    100      7          6         2       1      6K       86       794     63K       112      190
   * Median token counts using GPT-4o-mini; not used for complexity metrics. ** We study tokenization impact on rule-conditioning via a controlled ablation (Appendix F).


cuting the terminal statement sn . This holds true for both                              et al., 2011; Han et al., 2019); a fuzzer is a tool that au-
                                                                         σ
K and S formalizations. We use the notations J·KΨ and                                    tomatically generates programs and it is commonly used
    τ
J·KΨ to denote accessing the final state and execution trace                             for testing compilers and interpreters. The fuzzer samples
respectively. We also introduce the projection (π ) based no-                            statements from—assign, if–else, while, break, continue,
tation for tuple element access: For a tuple t = (x1 , . . . , xk ),                     halt—using depth-tapered probabilities—a cosine decay re-
πi (t) = xi and its compositional extension to an ordered list                           duces the chance of generating new if/while as nesting
of tuples T = [t1 , . . . , tn ] as πi (T ) = [ πi (t1 ), . . . , πi (tn ) ].            grows—and legality masks that enforce syntactic and se-
                                                                                         mantic validity (Appendix C.2).
3. Benchmark Construction                                                                Program complexity and data statistics. We characterize
Figure 2 shows the benchmark construction process. We                                    program complexity along three axes—control-flow, data-
formalize C⋆ in both S and K semantics ( 1 ). We use the                                 flow, and size. For control-flow, we use extended cyclomatic
K-framework ( 3 ) to obtain ground-truths ( 4 ) for K exper-                             complexity (ΩCC ) (McCabe, 1976); the static maximum
iments and a custom ANTLR4-based interpreter for those                                   nesting depths of if–else and while (ΩIf , ΩLoop ); and their
with S. The C⋆ program along with the K or S derived                                     dynamic counterparts measured along executed paths (Ω̂If ,
formalization is used to prompt the LLMs ( 5 ).                                          Ω̂Loop ). For data-flow, we use DepDegree (ΩDD ), which
                                                                                         quantifies uses and redefinitions of declared variables (Beyer
3.1. Dataset Curation                                                                    & Fararooy, 2010), and the total number of executed assign-
                                                                                         ments (Ω̂Assign ). For size, we use Halstead Vocabulary and
PLS EMANTICS B ENCH contains three splits, the Human-
                                                                                         Volume (ΩVoc , ΩVol ) (Halstead, 1977) which captures the
Written, the LLM-Translated, and the Fuzzer-Generated.
                                                                                         symbol variety and program information in bits respectively,
Human-Written. This set of C⋆ programs we manually                                       lines of code (ΩLoc ), and execution-trace length (Ω̂Trace ).
adapted from C++ solutions to coding problems sourced
                                                                                         Table 2 reports median values of the complexity metrics
from LeetCode (LeetCode, 2024), HumanEval (Chen et al.,
                                                                                         per dataset. Across ≈165 programs per split, the median
2021; Zheng et al., 2023), CodeContests (Li et al., 2022),
                                                                                         complexity increases progressively from Human-Written to
and MBPP (Austin et al., 2021; Orlanski et al., 2023).
                                                                                         LLM-Translated to Fuzzer-Generated along all three axes
We use public test cases as input and their correspond-
                                                                                         (complexity metrics distributions given in Appendix D).
ing oracles as expected outputs. Variable names are ob-
fuscated by replacing semantically meaningful identifiers                                3.2. Semantic Shifts
(e.g., maxIter) with random strings (Appendix C.1). We
validate correctness by executing the programs with K-                                   To test whether models condition their reasoning on ex-
framework and verifying outputs against the test oracles.                                plicitly supplied semantics—rather than rely on pretraining-
                                                                                         induced associations between surface syntax and behav-
LLM-Translated. This set of C⋆ programs are translated                                   ior—we introduce two semantic shifts, KeywordSwap and
from C++ programs using LLMs. Specifically, we collect                                   KeywordObf. These are transformations of the standard C⋆
the C++ programs from the CodeForces solutions published                                 semantics (Ψ□,std ; □ ∈ {S,K}) that preserve rule structure
on Hugging Face (Penedo et al., 2025). We prompt Q WEN                                   while perturbing the mapping between syntactic symbols
2.5-I NST 32B with the C⋆ syntax, semantics constraints, the
                                                                                         and their conventional meanings, enabling controlled tests
C++ solution and one corresponding public test case to                                   of whether models follow the supplied inferential rules when
generate a valid C⋆ program which we subsequently filter                                 syntactic familiarity is disrupted.
via the K-framework based on successful test execution.
                                                                                         KeywordSwap (Ψ□,swap ). KeywordSwap swaps the se-
Fuzzer-Generated. We construct this with a depth-                                        mantic interpretations of selected syntactic operators in the
controlled, semantics-aware, grammar-based fuzzer (Yang                                  standard semantics with their KeywordSwap counterparts

                                                                                     4
                                          LLMs Lean on Priors, Not Programming Language Semantics

Table 3. Mutations and obfuscations applied to the standard semantics to derive the nonstandard semantics KeywordSwap and KeywordObf.
 Type            Assignment            Arithmetic                      Relational                    Logical                          Keyword
 Standard             =          +    -     *     /     %    <    <=     >    >=       ==   !=   !     &&      ||   if-else   while    halt     break     continue
 KeywordSwap *        =          -    +     /     *     %    >    >=     <    <=       !=   ==   !     ||      &&   if-else   while    halt     break     continue
 KeywordObf **                                                                                                         -
  * Swaps the semantics of standard operator/keyword symbols; ** Assigns semantics of standard operators/keywords to novel symbols (from the Caucasian-Albanian script).


(Table 3); for example, it exchanges addition (+) and subtrac-                          notation-level understanding at the granularity of individual
tion (-), so that an expression written as x+y is evaluated                             inference rules.
according to the subtraction rule. Because KeywordSwap                                  Dataset. Multiple-choice distractors are generated via a hier-
preserves surface syntax while altering operational mean-                               archical sampling strategy to prevent reliance on surface lex-
ing, correct reasoning requires conditioning on the explicit                            ical cues (e.g., random sampling could produce distractors
transition rules rather than defaulting to pretraining-derived                          involving unrelated operators or constructs, enabling pattern
interpretations of common symbols.                                                      matching rather than semantic discrimination). Rules are
KeywordObf (Ψ□,obf ). KeywordObf probes the comple-                                     grouped—in descending order of sampling preference—into
mentary case in which syntactic familiarity is removed alto-                            families, constructs, and semantic roles (Appendix G.1). We
gether by systematically replacing standard keywords and                                generate 200 samples per task and semantic variant (Stan-
operators in the standard semantics with symbols drawn                                  dard, KeywordSwap, and KeywordObf).
from the rarely encountered Caucasian-Albanian script (Gip-                             Analysis. Figures 3a and 3b show the results averaged over
pert & Schulze, 2023) (Table 3). Under KeywordObf, ex-                                  three runs under zero-shot prompting for S and K. Un-
pressions such as x y execute identically to x+y under                                  der all semantic variants and formalizations, most models
standard semantics, but without relying on familiar sym-                                achieve near-ceiling performance on both NL → Rule and
bolic cues. By eliminating conventional symbol associa-                                 Rule → NL tasks. The performance of the Q WEN2.5-I NST
tions while preserving rule structure, KeywordObf isolates                              14B (Figure 3a, 1 ) and GPT-4o-mini (Figure 3a, 2 ) mod-
a model’s ability to follow explicit operational definitions                            els on the NL → Rule task under ΨS, are the exceptions,




                                                                                                                                          □
in the absence of syntactic priors.                                                     maxing out at ≈80-90%. Figures 3c and 3e, and Figures 3d
                                                                                        and 3f, show the confusion matrices for the top three most
4. Evaluation Setup                                                                     mispredicted rules for =std and swap respectively, for
                                                                                                                        □
                                                                                        Q WEN2.5-I NST 14B and GPT-4o-mini on NL → Rule. Both
Models and inference settings. We evaluate eleven fron-
tier LLMs divided into two classes. The non-reasoning                                   models primarily confuse structurally adjacent rules that
group consists of L LAMA-3.3 70B (Grattafiori et al., 2024),                            govern small-step reduction of expressions and computa-
Q WEN2.5-I NST 14B and Q WEN2.5-I NST 32B (Hui et al., 2024),
                                                                                        tions for ΨS,std and ΨS,swap formalizations. Most rule mispre-
and GPT-4o-mini (Achiam et al., 2023). The reasoning                                    dictions fall within the Arithmetic Expression (7-23) and the
group includes DeepSeek variants DS-L LAMA 70B, DS-                                     Relational Comparison (28-51) families.
Q WEN 14B, and DS-Q WEN 32B (Guo et al., 2025), as well                                 In summary, most frontier models exhibit stable notation-
as O 3-mini and GPT-5-mini (OpenAI, 2025), G EMINI-2.5-pro                              level competence across semantic formalizations and shifts,
(Kavukcuoglu, 2025), and Q W Q 32B (Team, 2025b). We                                    indicating that subsequent failures primarily reflect limita-
average all reasoning-model runs (and GPT-4o-mini) over                                 tions in rule-conditioned reasoning rather than inability to
three trials. The temperature for all non-reasoning models                              parse the formalism itself. When errors occur, the dominant
(except GPT-4o-mini) is set to 0 (prompts and additional                                failure mode is imprecise discrimination among fine-grained
details in Appendix E).                                                                 semantic roles within a construct (e.g., step vs. compute
                                                                                        cases), rather than global breakdown or random guessing.
Preliminary validation: formal-notation understanding.
                                                                                        ΨK, exhibits fewer such confusions, consistent with its
                                                                                            □




Before testing whether models can condition their reason-
                                                                                        coarser rule inventory per construct, which reduces the den-
ing on explicit formal semantic rules, we verify that they
                                                                                        sity of near-miss distractors relative to ΨS, .
                                                                                                                                                □




can interpret the notation used to express those rules; oth-
erwise downstream failures could reflect superficial misun-
derstanding of the formalism rather than limitations in rule-                           5. Experiments and Results
conditioned reasoning. We perform this validation using two                             We now evaluate our hypotheses concerning whether LLMs
auxiliary classification tasks: NL → Rule and Rule → NL.                                can condition their reasoning on explicitly specified formal
In NL → Rule, models select the correct formal rule (out of                             semantic rules. Specifically, we test whether models can
five choices) given its natural-language description (human-                            (H1) compose rules to obtain correct final states (§ 5.1), (H2)
written); conversely, in Rule → NL they identify the correct                            select appropriate rules when execution does not mutate
description for a given rule. Together, these tasks isolate

                                                                                   5
                                                                   101




                                                                                                                                                                                                                                              ≠
                                                                                                                                                               100                                                                                       100

                                                                   100                                                               0                           0
                                                                   101                                                            105                          101
                                                   LLMs Lean on Priors, Not Programming Language Semantics                        104
                                                                                                                                  103




                                                                                                                                                     ˆ Loop




                                                                                                                                                                                                                                                  ≠DD
                                                          ˆ If
                     NL → Rule                  NL →     → NL                       → NL→0 Rule                     → Rule
                                                                                                                         → NL     102        Rule → NL




                                                          ≠
                                                      Rule
                                                    Rule                       Rule NL                           NL Rule




                                                                                                                                                     ≠
   1                                       10 0
                               Q WEN 2.5-I NST-14B         Q WEN 2.5-I NST-14B         10       Q WEN 2.5-I NST-14B               101NST-14B
                                                                                                                           Q WEN 2.5-I
                                                                                                                                                                                                                                                              0
                                                Q WEN 2.5-I NST-32B                                                 Q WEN 2.5-I NST-32B                                                  Q WEN 2.5-I NST-32B                                 10 NST-32B
                                                                                                                                                                                                                                      Q WEN 2.5-I
                                                               0                                                                                           0                                              0
                                                   L LAMA 3.3-70B                                                       L LAMA 3.3-70B                                                          L LAMA 3.3-70B                             L LAMA 3.3-70B
                                                            104                                                                                       Standard
                                                                                                                                                         104                   KeywordSwap            10KeywordObf                                 6
   2                                                GPT-4 O - MINI                                                       GPT-4 O - MINI                                 GPT-4 O - MINI            GPT-4 O5- MINI
                                                            103                                                                                           103                                         10
                                                   DS-Q WEN -14B                                                        DS-Q WEN -14B                                  DS-QQWEN    2.5-I NST-14B
                                                                                                                                                                             WEN-14B
                                                                                                                                                                                                 DS-Q WEN -14B


                                                        ˆ Assign
                                                            102                                                                                                                                       104




                                                                                                                                                      ≠Loc




                                                                                                                                                                                                                                                  ≠Vol
                                                   DS-Q WEN -32B                                                        Standard
                                                                                                                        DS-Q WEN -32B                     102
                                                                                                                                                       KeywordSwap     DS-Q WEN -32BKeywordObf DS-Q WEN -32B
                                                               1
                                                            10-70B                                                                                                         Q WEN 2.5-I NST-32B        103
                                                        ≠
                                                   DS-L LAMA                                                            DS-L LAMA -70B                    101 NST-14BDS-L LAMA -70B              DS-L LAMA -70B
                                                                                                                                                    Q WEN 2.5-I                                       102
                                                     Q W Q-32B
                                                            100                                                           Q W Q-32B                                      Q W Q-32B
                                                                                                                                                                              L LAMA 3.3-70B       Q W Q-32B
                                                   Standard
                                                      O 3- MINI
                                                               0                                             KeywordSwap
                                                                                                                   O 3- MINI
                                                                                                                                                       KeywordObf
                                                                                                                                                          10 0
                                                                                                                                                    Q WEN 2.5-I NST-32B   O 3- MINI
                                                                                                                                                                                                      101
                                                                                                                                                                                                    O 3- MINI
                                                            103
                                                    GPT-5- MINI                                       Q WEN 2.5-IGPT-5-
                                                                                                                 NST-14BMINI
                                                                                                                                                          10 4
                                                                                                                                                                        GPT-5-GPT-4
                                                                                                                                                                                 MINI O - MINI
                                                                                                                                                                                                         1.0
                                                                                                                                                                                                  GPT-5- MINI
                                                   G EMINI -2.5-2PRO                                                                                 L LAMA
                                                                                                                                                         1033.3-70B G EMINI
                                                                                                                                                                       100-2.5-100      00                                                      0.8
                                                                                                                                                                                                                                       0G EMINI -2.5-  8713 0 87 0 0 0 0                              0




                                                                                                                                                                                                       49 36 21
                                                                                                                                                                                 0                                                                13 PRO




                                                                                                                                                                                                                                                                    36 32 28
                                                                                                                                                                                     49 36 21




                                                                                                                                                                                                                                                  36 32 28
                                                                                                              G EMINI -2.5- PRO                                                 PRO
                                                                   10                                                                                                       DS-Q WEN -14B
                                                                                                      Q WEN 2.5-I NST-32B




                                                                                                                                                     ˆ Trace
                                                          ≠Voc




                                                                                                                                                                                                                                                             0.6
100                 75                50        25     1000               7525                     5050             2575            0100   100       75 1075         250
                                                                                                                                                                     25
                                                                                                                                           25       50              100                                00
                                                                                                                                                                                                       100            07525 100
                                                                                                                                                                                                                              050
                                                                                                                                                                                                                             50        075
                                                                                                                                                                                                                                       25                    100
                                                                                                                                                                                                                                                             0 0               25
                                                                                                                                                                                                                                                                               0 0 25 0507525 07575   0100




                                                                                                                                                                                                True




                                                                                                                                                                                                                                                             True
                                                                                                                                                                              True




                                                                                                                                                                                                                                           True
                                                             1                                                                                        GPT-4 O - MINI                                                  100
                                                   Accuracy10(%)                                               Accuracy (%)                                                                 Accuracy (%)                                   Accuracy (%)




                                                                                                                                                     ≠
                                                                                                                                                                                                                                                0.4
                                                                                                          L LAMA 3.3-70B                                       101                               DS-Q WEN -32B
                                                                                                                                                     DS-Q WEN -14B                                      0     00      0
                                                                                                                                                                                                                     100 100      0.2
                                                                                                                                                                                                                                      0 0 0 0 0 0 01000 100
               (a) Formal notation comprehension
                                      0          of S.                                                                                                               0                                       (b) Formal notation comprehension      of K.
                                                                   10                                        GPT-4 O - MINI                                    10                                        DS-L LAMA -70B           0.0
                                                                                                                                                                                                                                      0.0 0.2     0.4    0.6
                                                                                                                                                     DS-Q WEN -32B
                                                                                                                                                                                                       22 22   37 37  48 48         28 2928  322933 323733   37 0.8                                          1.0


                                                                                                                                                                                                                          Predicted
                                                                                                                                                                                                                  Predicted
                                                                                                                                                                                                                  Q                                                                   Predicted
                                                                                                                                                                                                                                                                               Predicted
                                                                                            0             DS-Q WEN20
                                                                                                                  -14B                           40 Percentage 60                                                  80W Q-32B     100
                                                                                                                                                     DS-L LAMA -70B
                           100 1000                    00            0                               13DS-Q
                                                                                                         8713
                                                                                                            WEN0-32B
                                                                                                                870 0 0                    0 0 00                                                  100   0 0MINI 000
                                                                                                                                                                                                       100                            00                     100 01000 0 0 0 0 0                      0




                                                                                                                                                                                     29 28 21




                                                                                                                                                                                                                                                  44 36 20
         49 36 21

                           49 36 21




                                                                                       36 32 28

                                                                                                         36 32 28




                                                                                                                                                                                                       29 28 21




                                                                                                                                                                                                                                                                    44 36 20
                                                                                                    100                                                                          13                87
                                                                               36 21




                                                                                                                                                                   36 32 28
                                                                                                                                                                                                       O 3-
                                                                                                                                                         Q W Q-32B 0
                                                                   True




                                                                                                                                                          True


                                                                                                                                                                              True




                                                                                                                                                                                                                                           True
  True




                                                                          49 True




                                                                                                                                                                                                True




                                                                                                                                                                                                                                                             True
                    True




                                                                                                  True




                              0            0100 1000                 0                                00            0 0 25100
                                                                                                                          0 7525 075 00                                                                00             25
                                                                                                                                                                                                                       00     75
                                                                                                                                                                                                                               100
                                                                                                                                                                                                                               0      0100                         0 17 0 8317 0 83 0 0               0
                                                                                                         DS-L LAMA -70B                                                                                           GPT-5- MINI
                                                                                                      0                         0             100          O 3- MINI                 0                 0              0       0      100
                              0            00          0100 100                                          0          0 0 0 0 0 0 1000 100                                                                0             100
                                                                                                                                                                                                                      0     0
                                                                                                                                                                                                                          100          0                           0           0 0 0 0 17 0 8317 83
                                             22 Q W Q-32B37               48                 28      29 G EMINI
                                                                                                             32 -2.5- PRO
                                                                                                                      33      37
          22 2237 3748 48                                32290 3332 3733 037 GPT-5- MINI100
                                             28 2928 Predicted
                                            100                                                       22      028
                                                                                                             22
                                                                                                      0 Predicted        29 029
                                                                                                                       028              21 3621373644374544 45
                                                                          29 28 21




                                                                                                                                                                   44 36 20


              Predicted
                      Predicted                      3- MINI Predicted100
                                                   OPredicted
                                                                                  75        50       25         0
                                                                                                           Predicted
                                                                                                                          25
                                                                                                                   Predicted
                                                                                                                                   50      75      100
                                                                                                                                              Predicted
                                                                                                                                                     Predicted
                                                                   True




                                                                                                                                                          True




                                              0              0           100 G EMINI -2.5- PRO0      17 Accuracy
                                                                                                             83     (%)0       0
(c) Q WEN2.5-I NST 14B std.                  (d)  GPT-4o-mini
                                              0 GPT-5-
                                                                       std.             (e)  Q WEN   2.5-I NST    14B    swap.          (f) GPT-4o-mini     swap.
         100 1000         00                100     010075MINI
                                                          0100
                                                            0 0 0500 0 0025                   0       0       0       17      83        13 8713 0 87 0 0 0 0 0




                                                                                                                                                                                                                                                  20 13 10
         29 28 21




                                                                                       44 36 20




                                  0




                                                                                                                                                                                                                                                                    20 13 10
                           29 28 21




                                                                                                         44 36 20




                                            100                                        0         25       50        75        100
Figure 3. Formal-semantics notation comprehension                   results.
                                                                          29 Models      solve
                                                                                             21 two36 multiple-choice 44 (five45 choices) tasks: mapping natural-
                                                                            0 Accuracy      (%)
                                             22G EMINI -2.5-28                                               37
                                                                                                                                                                              True




                                                                                                                                                                                                                                           True
  True




                                                                          57 True




                                                                                                                                                                                                True




                                                                                                                                                                                                                                                             True
                    True




                                                                                                  True




           0     0 0 to0100      100 rules 0(NL    17    8317PRO083and
                                                                     0 0vice-versa                           100                         0 NL0→0100  0 01000 0 →0NL
                                                                                                                                                                                     57



                                                      0 Rule)                                                         100
                                                                                                                                                                                                       57
language descriptions       semantic                 →                                (Rule13→ NL).  87 Panels0 (a,b)  0 show0 results on        Rule/Rule
                                                                                                                                                                   20 13 10




                                                         Predicted                                        Predicted
tasks under0Ψ100
              □,
                    (  ∈ {    ,      ,    })   for    =     and      respectively,    averaged     over three   runs    of 200   samples.0 0 0 0 0 17and
                                                                                                                                          Panels  (c,d)      (e,f)83
                                                                                                                                                                   plot
                                           □




                 0100 75   std
                        1000 50 swap   obf 250 0 00 0100
                                                    □
                                                            0 17 25
                                                                  0 8317 50          75       0100 0                                                     0 8317
                                                                   True




                                                                                                                                                          True




                                  0                       S       K        83
                                               □




                                                                                                            100        0       0
NL → Rule confusion matrices under Ψ            S,std
                                                      and (%)
                                               Accuracy     ΨS,swap respectively for the three most frequently mispredicted rules for Q WEN2.5-I NST 14B
                                                                                              0       0       0       17      83
          22 .22
and GPT-4o-mini    28 example
                  For    2829 29             21 2.5-I
                                  in (c), Q WEN    3621NST
                                                         373614B
                                                               4437 4544 Ψ
                                                                   under   45S,std selects rule   22 for rule5621’s56                   10 1110
                                                                                                                         description in 100%   of14 1120142120 21
                                                                                                                                                  cases.
              Predicted
                      Predicted                      Predicted
                                                             Predicted
                                                            56                               10      11 Predicted
                                                                                                             14 Predicted
                                                                                                                      20      21              Predicted
                                                                                                                                                     Predicted
                                                                                                                         Predicted                                                                                Predicted
                                                                                                      13 8713 087 0 0 0 0
                                                                                       20 13 10




                                                     0
                                                                                                         20 13 10




                                                                                                                                                                                                                  ′
state (§ 5.2), (H3) sustain such conditioning across long                                                                                                                 score. Acc is the model’s accuracy when ∈ {swap, obf}
                                                                                                                                                                                                             □




                                                                                                                                                                                                                                                                                      □
                                                                                                                                                                                                            □
  True




                                                                           True
                    True




                                                                                                  True




execution traces100
                 (§ 5.3),
                     100 and (H4) remain
                                    0 0 0faithful  to0supplied
                                           1000 0100                                                                                                                      i.e., under semantic shifts while Acc□std is the accuracy under
         57




                                                      0 0
                           57




rules under semantic shifts that conflict
                                    0 0 0 0 0 170 8317 priors
                                          with learned   83                                                                                                               standard semantics as before, with both being realized under
concerning symbol–meaning associations.                                                                                                                                   the same semantic framework i.e., ∀□, □′ ∈ {S,K}; □ = □′ . A
                                           56        56                                               10 1110 1411 2014 2120 21                                           large negative score is indicative of a model’s inability to
We first introduce    two task scoped metrics
              Predicted
                    Predicted                    to test our hy-
                                          Predicted
                                                Predicted
potheses. Without loss of generality, consider a model’s                                                                                                                  override pretrained symbol priors when operator meanings
task-scoped accuracy score Acc□ , potentially** realizable                                                                                                                are perturbed.
                                                                                                  □




under the set of formalizations: {Ψ□, | □, ∈ ({S,K} ×
                                                                                                                    □




                                                                                                                                □




{std, swap, obf}) ∪ {⊥†† }} . We then define:
                                                                                                                                                                          5.1. Global Rule-Conditioned Reasoning (H1)
                                                                                                                                                                          Motivation. H1 posits that models can condition their rea-
                                     std −Accna quan-
▶ Semantic Conditioning (∆cnd ) ≜ Acc□
tifies the effect of supplying semantics formalization ex-                                                                                                                soning using explicitly supplied formal semantic rules to
plicitly on a model’s accuracy score. Accna is the model’s                                                                                                                determine program final states (program execution reason-
accuracy when □, = ⊥ i.e., when provided with no for-                                                                                                                     ing at coarser granularity). We introduce the PredState
                                                   □




malization while Acc□std is the accuracy under Ψ□,std . A                                                                                                                 task requiring predicting final states by composing rule ap-
positive score is indicative of a model’s ability to condition                                                                                                            plications across control and data flow, thereby testing H1
its reasoning on explicitly supplied formal semantics.                                                                                                                    by probing whether semantics guide multi-step execution
                                                                                                                            ′                                             reasoning rather than acting as inert context.
                                               std quan-
▶ Semantic Shift Sensitivity (∆is ) ≜ Acc□ −Acc□
                                                                                                                                                                         Dataset. From Definition 2.2 the final program state of a
                                                                                                                          □




tifies the effect of semantic shifts on a model’s accuracy
                                                                                                                                                                         program P , with an initial program state σ0 , and under a
 ** Not all of our tasks support the entire combination of pairings
                                                                                                                                                                         semantic formalization Ψ□, is JPKσΨ , (σ0 ) which we use as
                                                                                                                                                                                                                                      □




of formalizations and semantic shifts.
                                                                                                                                                                                                                                                                    □
                                                                                                                                                                                                                                                                        □




 ††                                                                                                                                                                      the ground-truth for PredState. Supposing D′ be a subset
    We denote ‘⊥’ as the absence of formalization and assume that
only the final state of program execution is computable under ⊥                                                                                                          of a PredState dataset D for which a model’s results are
while its execution-trace is not.                                                                                                                                        well formed, then we define accuracy over the D as:


                                                                                                                                                               6
                                             LLMs Lean on Priors, Not Programming Language Semantics

Table 4. Global and state mutation-free rule-conditioned reasoning. Left: predict final program state accuracy via rule composition.
Right: predict semantic-rules for program execution in absence of state mutation. Best per column is bold.
                                                       PredState (D=Human-Written)                                                               PredRule
                                           K-Formalization                             S-Formalization                        K-Formalization                S-Formalization
                              Accna     Accstd        Accswap     Accobf          Accstd        Accswap     Accobf     Accstd    Accswap     Accobf    Accstd   Accswap     Accobf
 Models                                 (∆cnd )         (∆is )     (∆is )         (∆cnd )         (∆is )     (∆is )                (∆is )     (∆is )              (∆is )     (∆is )
 Non-reasoning
 Q WEN2.5-I NST 14B         33 27 (-06)                6 (-21) 14 (-13)          28 (-05)       6 (-22)     8 (-20)      49     45 (-04)    45 (-04)    19      19 (000)   17 (-02)
 Q WEN2.5-I NST 32B         50 29 (-21)                4 (-25) 12 (-17)          33 (-17)       4 (-29)    19 (-14)      58     52 (-06)    46 (-12)    17      24 (+07)   19 (+02)
 L LAMA-3.3 70B             32 29 (-03)                4 (-25) 12 (-17)          25 (-07)       5 (-20)    12 (-13)      45     42 (-03)    45 (000)    32      32 (000)   27 (-05)
 GPT-4o-mini                31 26 (-05)                6 (-20) 8 (-18)           24 (-07)       6 (-18)     8 (-16)      38     34 (-04)    27 (-11)    27      27 (000)   21 (-06)
 Non-reasoning + Chain-of-thought
 Q WEN2.5-I NST 14B-CoT 73 70 (-03)                    2 (-68)   48 (-22)        68 (-05)       4 (-64)    41 (-27)      50     32 (-18)    27 (-23)    12      10 (-02) 6 (-06)
 Q WEN2.5-I NST 32B-CoT 81 77 (-04)                    8 (-69)   56 (-21)        69 (-12)       3 (-66)    33 (-36)      64     47 (-17)    47 (-17)    29      26 (-03) 24 (-05)
 L LAMA-3.3 70B-CoT         75    75 (000)             3 (-72)   56 (-19)        77 (+02)       2 (-75)    48 (-29)      69     46 (-23)    50 (-19)    28      28 (000) 17 (-11)
 GPT-4o-mini-CoT            68 78 (+10)                2 (-76)   38 (-40)        65 (-03)       3 (-62)    27 (-38)      57     46 (-11)    37 (-20)    27      26 (-01) 24 (-03)
 Reasoning
 DS-Q WEN 14B               65 81 (+16)                2 (-79)   40 (-41)        58 (-07) 2 (-56) 29 (-29)               57     45 (-12)    48 (-09)    22      21 (-01)   20 (-02)
 DS-Q WEN 32B               84 93 (+09)               21 (-72)   72 (-21)        95 (+11) 3 (-92) 77 (-18)               79     66 (-13)    65 (-14)    47      38 (-09)   38 (-09)
 DS-L LAMA 70B              80 88 (+08)                2 (-86)   58 (-30)        89 (+09) 2 (-87) 59 (-30)               34     10 (-24)    27 (-07)     1       1 (000)    1 (000)
 Q W Q 32B                  93 98 (+05)               71 (-27)   82 (-16)        98 (+05) 7 (-91) 86 (-12)               92     85 (-07)    76 (-16)    49      44 (-05)   41 (-08)
 O 3-mini                   94 100 (+06)              41 (-59)   84 (-16)       100 (+06) 63 (-37) 95 (-05)              93     65 (-28)    84 (-09)    80      72 (-08)   67 (-13)
 GPT-5-mini                100 99 (-01)               79 (-20)   94 (-05)       100 (000) 79 (-21) 99 (-01)              92     83 (-09)    82 (-10)    80      81 (+01)   81 (+01)
 G EMINI-2.5-pro            93 100 (+07)              97 (-03)   94 (-06)        99 (+06) 98 (-01) 100 (+01)             99     98 (-01)    90 (-09)    94      96 (+02)   98 (+04)




                 1                                                                                   symbol associations in favor of supplied rules. G EMINI-2.5-
                                     h                              i
                                                                      †‡
        □
                         X               σ
  Acc ≜                             1 JPKΨ , (σ0 ) = σpred Ψ , ,P,σ
                                                                                                     pro stands out with ≥98% accuracy even under swap.
                                             □                          □
                |D|
        □




                                                  □




                                                                            □




                                                                                  0
                      (P,σ0 )∈D ′

Where □ , ∈ ({S,K}×{std, swap, obf})∪{⊥}, dom(σ0 )=∅.                                                Structural factors limiting rule composition (Ω□ ). Mov-
                □




D ∈ {Human-Written, LLM-Translated, Fuzzer-Generated} and                                            ing from Human-Written to LLM-Translated and Fuzzer-
σpred Ψ , ,P,σ is the model’s final state prediction for the
        □
                                                                                                     Generated programs (Table 5) induces systematic accuracy
                                                                                                     collapses—often exceeding 40% points—highlighting the
            □




              0
program P , with an initial state σ0 , and formalization Ψ□, .
                                                                                            □




                                                                                                     fragility of long-horizon rule composition under scale. Mul-
Analysis. Table 4 (left-side) and Table 5 show the accu-                                             tivariate regression (Appendix G.2.1) isolates distinct stres-
racy percentages for the Human-Written dataset, and the                                              sors: control-flow depth dominates on human programs,
structurally more complex LLM-Translated and Fuzzer-                                                 while data-flow and size-related metrics govern translated
Generated datasets respectively under one-shot prompting.                                            and fuzzed inputs, implicating long execution traces and
Partial correctness percentage discussed in Appendix G.2.3.                                          global state tracking as primary bottlenecks.
Does providing formal rules change global composi-                                                   Impact of CoT prompting. On Human-Written programs
tion (∆cnd )? On the Human-Written split (Table 4, left-                                             (Table 4, left-side), chain-of-thought (CoT) boosts non-
side), ∆cnd sharply separates model classes: reasoning-                                              reasoning models under standard semantics by nearly 50
oriented models gain 9–16% points (e.g., DS-Q WEN 32B,                                               points. However, these gains vanish under swap and shrink
DS-L LAMA 70B), pushing G EMINI-2.5-pro to ≥99% accu-                                                to ≈40 points for obf indicating that CoT aids long-horizon
racy, while non-reasoning models lose 5–25% points. On                                               execution but does not overcome pretrained operator biases.
the Fuzzer-Generated split (Table 5), even frontier models
show generally negative ∆cnd indicating that structural scale                                          Key Findings
overwhelms global rule-conditioned composition.                                                        ⋆ Reasoning-oriented models benefit substantially from access
Do models override pretrained symbol biases (∆is )?                                                    to formal semantics, while non-reasoning models often degrade.
Across both tables, swap causes far larger drops than                                                  ⋆ KeywordSwap causes far larger drops than KeywordObf, re-
                                                                                                       vealing persistent reliance on pretrained symbol–semantics asso-
obf—often 40–70% points—even when standard accuracy                                                    ciations rather than strict conditioning on provided rules.
is high. On Human-Written programs (Table 4, left-side),                                               ⋆ Performance drops with program complexity— deep control
GPT-5-mini and DS-Q WEN 32B lose 20–70% points under                                                   flow, heavy data dependencies—highlighting structural limits in
swap, while obf causes modest degradation. Because swap                                                global rule-conditioned reasoning.
preserve surface syntax while changing operator meaning,                                               ⋆ CoT prompting boosts non-reasoning models on standard se-
                                                                                                       mantics but fails under semantic swaps, indicating reasoning
these gaps show that most models fail to override pretrained                                           traces alone do not overcome pretrained operator biases.
 †
   We generally drop the superscript ‘□ ’ for Acc when the type of
formalization is readily inferrable.
 ‡
     σA = σB ⇔ dom(σA ) = dom(σB ) ∧ ∀x ∈ dom(σA ).σA (x) = σB (x)



                                                                                                 7
                                                LLMs Lean on Priors, Not Programming Language Semantics

Table 5. PredState results on the LLM-Translated and Fuzzer-                                 Table 6. PredTrace results on the Human-Written (least complex)
Generated datasets. Best per column within each dataset is bold.                             dataset split. Best per column is bold.
                                K-Formalization                S-Formalization                                         K-Formalization                            S-Formalization
                       Accna Accstd Accswap     Accobf     Accstd Accswap      Accobf                           Accstd Accswap         Accobf                Accstd Accswap      Accobf
Models*                      (∆cnd )  (∆is )     (∆is )    (∆cnd )  (∆is )      (∆is )        Models*                    (∆is )         (∆is )                        (∆is )      (∆is )
LLM-Translated                                                                                Q W Q 32B           18       16 (-02)   15 (-03)                0     0 (000)      0 (000)
Q W Q 32B        82        83 (+01) 31 (-52) 61 (-22)     82 (000) 4 (-78) 63 (-19)           O 3-mini            19        3 (-16)   13 (-06)                5     3 (-02)      2 (-03)
GPT-5-mini       94        96 (+02) 76 (-20) 86 (-10)     95 (+01) 65 (-30) 90 (-05)          GPT-5-mini          20       14 (-06)   17 (-03)               17    15 (-02)     17 (000)
G EMINI-2.5-pro 91         94 (+03) 85 (-09) 91 (-03)     94 (+03) 87 (-07) 93 (-01)          G EMINI-2.5-pro     25       25 (000)   25 (000)               32    35 (+03)     35 (+03)
Fuzzer-Generated                                                                                * Only models with non-zero scores on PredTrace are shown.
Q W Q 32B        16        16 (000) 0 (-16) 3 (-13)       15 (-01) 0 (-15) 1 (-14)
GPT-5-mini       57        51 (-06) 14 (-37) 23 (-28)     55 (-02) 17 (-38) 23 (-32)
G EMINI-2.5-pro 73         69 (-04) 26 (-43) 49 (-20)     69 (-04) 39 (-30) 47 (-22)
     * Only the best scoring models on PredState for the Human-Written are considered.       Is robust local rule conditioning a general capability?
                                                                                             The pattern of ∆is reveals sharp stratification rather than
                                                                                             smooth scaling: reasoning-oriented models are typically
5.2. State-Free Rule-Conditioned Reasoning (H2)
                                                                                             more stable than non-reasoning ones, but large drops per-
Motivation. H2 targets a more elementary capability than                                     sist even among strong systems (e.g., O 3-mini under swap
its predecessor: selecting the correct operational rules at                                  drops by ≈30%). This heterogeneity suggests that local rule-
individual steps when program state does not mutate. By re-                                  conditioned reasoning is not yet a broadly learned behavior
moving long-horizon state propagation, this setting isolates                                 across LLM families.
whether models ground local decisions in supplied formal
semantics rather than surface syntax or pretrained operator                                   Key Findings
associations. We test this hypothesis via the PredRule task,                                 ⋆ PredRule isolates rule select/app w/o state tracking; most
asking whether semantic shifts still disrupt rule selection                                  models nevertheless fail under KeywordSwap, showing persis-
when execution does not mutate state.                                                        tent reliance on pretrained symbol semantics rather than strict
                                                                                             conditioning on provided rules.
Dataset. From Definition 2.2 the execution trace τP of a                                     ⋆ Semantic shift robust rule selection emerges only in a small
program P , an initial program state σ0 , under a semantic                                   subset of frontier systems, indicating that this capability is rare
formalization Ψ□, is JPKΨ                                                                    and not a generic consequence of scale or reasoning prompts
                                , (σ0 ). The programs (P ) in the
                              τ
                            □




                                        □
                                                                                             (CoT has no impact).
                                            □




PredRule dataset are constructed from those in the Human-
Written split satisfying the invariant ∀σ ′ ∈ π1 (τP ) ∧ σ ′ ̸=
                                                                                             5.3. Long-Horizon Rule-Conditioned Reasoning (H3)
JPKσΨ , (σ0 ), σ ′ = σ0 i.e., the initial program state is unmu-
         □
             □




tated throughout program execution barring the terminal                                      Motivation. H1 examined global outcomes, while H2 tar-
statement-step. We use the ordered list of semantic rules                                    geted state-free rule selection. H3 asks whether LLMs
⊕π2 (τP ) as the ground-truth. Supposing D′ is a subset of a                                 can sustain rule-conditioned reasoning throughout full pro-
PredRule dataset D for which the model’s predictions are                                     gram executions. We test this via the PredTrace task,
well formed, then we define accuracy over D as:                                              which—like PredState — targets long-horizon reasoning
                      1    X      h
                                           τ
                                                                       i                     but at a finer, execution-trace granularity: models must gen-
                                             , (σ0 )) = Rpred Ψ , ,P,σ
         □
  Acc ≜                          1 ⊕π2 (JPKΨ      □                    □                     erate complete sequences of semantic rule applications and
                     |D|
         □




                                                      □




                                                                           □




                                                                                 0
                       (P,σ0 )∈D ′
                                                                                             intermediate states, isolating whether they can repeatedly
□,   ∈ {S,K}×{std, swap, obf} and dom(σ0 ) may not be ∅.                                     re-ground their reasoning in explicit operational definitions
     □




Rpred Ψ , ,P,σ is the model predicted ordered list of semantic
             □                                                                               while maintaining the long-range dependencies induced by
                 □




              0
rules for the program P .                                                                    loops, branching, and mutable stores.
Analysis. Table 4 (right-side) shows the accuracy percent-                                   Dataset. The execution trace JPKτΨ , (σ0 ) of a program P
                                                                                                                                                     □
                                                                                                                                                         □




ages for PredRule under one-shot prompting. Details about                                    (Definition 2.2), with an initial program state σ0 , and under
PredRule split construction and rule prediction failure rates                                a semantic formalization Ψ□, is used as the ground-truth
                                                                                                                                        □




can be found in Appendix G.3.1 and G.3.2                                                     in PredTrace. If D′ be the subset of a PredTrace dataset
Pretrained symbol biases during local rule selection (∆is )                                  D for which the model’s predictions are well formed, we
Across PredRule (Table 4, right-side), most systems exhibit                                  define the accuracy over a dataset D for this analysis as:
strongly negative ∆is , implying that even when state evo-                                                   1             X       h                               i
                                                                                                 Acc ≜□
                                                                                                                                  1 JPKτΨ , (σ0 ) = τpred Ψ , ,P,σ
lution is removed, local rule selection remains dominated
                                                                                                                                            □                           □
                                                                                                            |D|
                                                                                                     □




                                                                                                                                                 □




                                                                                                                                                                            □




                                                                                                                                                                                  0
                                                                                                                  (P,σ0 )∈D ′
by symbol priors rather than formal definitions. Only a
                                                                                             □ , ∈ {S,K}×{std, swap, obf} and dom(σ0 ) = ∅. D=Human-
narrow subset of frontier models maintain or improve accu-
                                                                                               □




racy under mutation (e.g., only G EMINI-2.5-pro under ΨS,                                    Written and τpred Ψ , ,P,σ is the model predicted execution
                                                                                     □




                                                                                                                       □
                                                                                                                           □




                                                                                                                       0

shows modest improvement), indicating that faithful local                                    trace for the program P .
rule conditioning under distribution shift is rare.                                          Analysis. Table 6 shows the accuracy scores (%) for Pred-

                                                                                         8
                                   LLMs Lean on Priors, Not Programming Language Semantics

Trace under one-shot prompting.                                           under next-token training. The implicit hypothesis is that
Can models sustain rule conditioning over long hori-                      models internalize program semantics from such training.
zons? PredTrace sharply exposes the fragility of long-                    PLS EMANTICS B ENCH provides the missing diagnostic by
horizon rule conditioning: only four models achieve non-                  directly supplying formal semantic rules and measuring
zero accuracy at all, and even these remain far from re-                  whether models condition their reasoning on those rules.
liable. Under K, all surviving models exhibit negative
∆is (e.g., Q W Q 32B and O 3-mini lose 2–16 points under                  6.3. Perturbing Programs vs. Perturbing Semantics
KeywordSwap), indicating that symbol–meaning conflicts                    EquiBench (Wei et al., 2025a), SeqCoBench (Maveli et al.,
rapidly derail multi-step rule application.                               2025), SPAT (Yu et al., 2022), CodeARC (Wei et al., 2025b),
Is long-horizon robustness a rare capability? The dis-                    and Orvalho & Kwiatkowska (2025) mutate programs un-
tribution of ∆is is highly skewed: most models collapse to                der semantics-preserving transformations to test whether
zero accuracy before robustness can even be meaningfully                  models track underlying behavior across syntactic variants.
measured, while the few remaining systems show sharply                    We invert the setup: programs remain syntactically iden-
divergent behavior. For instance, O 3-mini and GPT-5-mini                 tical while the externally supplied formal semantics are
degrade under semantic swaps, whereas G EMINI-2.5-pro im-                 altered, isolating reliance on pretrained symbol–semantics
proves, indicating that the ability to sustain rule conditioning          associations from sensitivity to surface form. K-framework
across dozens of steps is not a smooth function of scale or               formalizations of C (Ellison & Roşu, 2012; Hathhorn et al.,
reasoning prompts, but instead appears only in a small sub-               2015), Java (Bogdanas & Roşu, 2015), and Python (Guth
set of frontier models.                                                   et al., 2020) make this methodology directly extensible to
                                                                          richer languages.
Key Findings
⋆ Sustaining rule-conditioned reasoning over long execution               6.4. Rule Following and Conflicts with Priors
horizons is extremely brittle: most models fail entirely once state       RuleBreakers (Chan et al., 2025) and Sun et al. (2025) probe
tracking and repeated rule application are required.                      whether LLMs follow natural-language inferential rules; in
⋆ Only G EMINI-2.5-pro exhibits consistently positive ∆is under
S, indicating that mutation-robust long-horizon rule conditioning         NLP more broadly, CheckList (Ribeiro et al., 2020), Con-
is a rare and specialized capability.                                     trast Sets (Gardner et al., 2020), HANS (McCoy et al., 2019),
                                                                          NLI stress tests (Naik et al., 2018), and semantic sensitivity
                                                                          probes (Arakelyan et al., 2024) expose heuristic shortcuts
6. Related Work
                                                                          via input perturbations, paralleling texture-bias diagnostics
6.1. Code Reasoning and Execution Benchmarks                              in vision (Geirhos et al., 2019). PLS EMANTICS B ENCH trans-
Recent benchmarks evaluate LLMs’ ability to reason                        poses this question to formal rule following: complete opera-
about program execution and behavior (CRUXEval (Gu                        tional semantics are supplied and we test whether reasoning
et al., 2024), CRUXEval-X (Xu et al., 2025), Live-                        conditions on those rules when they redefine standard opera-
CodeBench (Jain et al., 2025), BigCodeBench (Zhuo et al.,                 tor meaning—a conflict that arises in practice with operator
2024), REval (Chen et al., 2025), CoCoNUT (Beger &                        overloading, DSLs, and proof assistants.
Dutta, 2025), CodeMind (Liu et al., 2024), SURGE (Lyu
et al., 2025), and LLMs as code executors (Wang et al.,                   7. Conclusion
2024)), trace-trained models (CWM (Team, 2025a)), and                     We introduced PLS EMANTICS B ENCH, a semantics-driven
code-reasoning generalization studies (Yang et al., 2025).                benchmark for studying whether large language models
These works evaluate end-to-end inputs/outputs or traces                  (LLMs) condition their reasoning on explicit formal rules
under fixed language semantics; PLS EMANTICS B ENCH in-                   rather than pretrained syntactic priors. Using program exe-
stead supplies formal inference rules and uses execution as               cution as a controlled probe, a programming language with
a controlled lens for whether models condition step-level                 two semantic formalisms and shifts, we isolate four capa-
reasoning on those rules.                                                 bilities: global rule composition, state-free rule selection,
                                                                          long-horizon conditioning, and robustness to semantic shift.
6.2. Execution-Aware Training
                                                                          Across 11 frontier models, performance drops sharply under
A growing body of work argues that exposing LLMs to                       semantic shifts and long horizons despite high standard-
program executions improves downstream performance,                       semantics accuracy; only a small subset shows robustness to
including execution-guided synthesis (Chen et al., 2018),                 novel rules. These results position inferential rule condition-
NExT (Ni et al., 2024), SemCoder (Ding et al., 2024a),                    ing as a largely unsolved capability axis motivating models
TRACED (Ding et al., 2024b), and CodeI/O (Li et al., 2025).               to adapt to externally specified formal systems rather than
Jin & Rinard (2024) further report that representations of                entrenched lexical associations.
formal trace semantics emerge in transformer hidden states

                                                                      9
                                LLMs Lean on Priors, Not Programming Language Semantics

Acknowledgments                                                         Program synthesis with large language models. arXiv
                                                                        preprint arXiv:2108.07732, 2021.
We thank Cheng Ding, Ivan Grigorik, Michael Y. Levin, Yan
Levin, Tong-Nong Lin, Karl Palmskog, Zijian Yi, Zhiqiang              Beger, C. and Dutta, S. Coconut: Structural code under-
Zang, Linghan Zhong and the anonymous reviewers for                     standing does not fall out of a tree. In LLM4Code, 2025.
helpful feedback and discussions.
                                                                      Beyer, D. and Fararooy, A. A simple and effective measure
Computational resources were provided by the Texas Ad-
                                                                        for complex low-level dependencies. In ICPC, pp. 80–83,
vanced Computing Center at The University of Texas at
                                                                        2010.
Austin† . This work was supported in part by the U.S. Na-
tional Science Foundation (NSF) Nos. CCF-2217696, CCF-                Bogdanas, D. and Roşu, G. K-java: A complete semantics
2313027, CCF-2403036, CCF-2421782; the NSF–Simons                       of java. In POPL, pp. 445–456, 2015.
AI Institute for Cosmic Origins‡ funded by NSF award AST-
2421782; the Simons Foundation (MPS-AI-00010515); and                 Chan, J., Gaizauskas, R. J., and Zhao, Z. Rulebreakers:
a sponsored research award by Cisco Research.                           Challenging llms at the crossroads between formal logic
                                                                        and human-like reasoning. In ICML, pp. 7276–7305,
The views expressed are those of the authors and do not
                                                                        2025.
necessarily reflect those of sponsors.
                                                                      Chen, J., Pan, Z., Hu, X., Li, Z., Li, G., and Xia, X. Reason-
Impact Statement                                                        ing runtime behavior of a program with llm: How far are
                                                                        we? In ICSE, pp. 1869–1881, 2025.
This paper introduces the first large-scale study of whether
large language models can condition their reasoning on ex-            Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. D. O.,
plicitly provided formal semantics, using program execution             Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman,
as a canonical setting for investigating this capability. We            G., et al. Evaluating large language models trained on
present new evaluation tasks and datasets that probe models’            code. arXiv preprint arXiv:2107.03374, 2021.
ability to select and compose inference rules across full exe-
cutions and under controlled semantic perturbations, estab-           Chen, X., Liu, C., and Song, D. Execution-guided neural
lishing a foundation for systematic study of rule-grounded              program synthesis. In ICLR, 2018.
reasoning in programming languages.                                   Cornfield, J. A method of estimating comparative rates from
Overall, this paper positions inferential rule conditioning as          clinical data; applications to cancer of the lung, breast,
a new capability axis for evaluating learning-based systems             and cervix. Journal of the National Cancer Institute, 11:
for programming languages, with the long-term goal of                   1269–1275, 1951.
building models that reason more faithfully about formal
specifications.                                                       Ding, Y., Peng, J., Min, M., Kaiser, G., Yang, J., and Ray,
                                                                        B. Semcoder: Training code language models with com-
                                                                        prehensive semantics reasoning. In NeurIPS, volume 37,
References                                                              pp. 60275–60308, 2024a.
Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I.,
  Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S.,           Ding, Y., Steenhoek, B., Pei, K., Kaiser, G., Le, W., and Ray,
  Anadkat, S., et al. Gpt-4 technical report. arXiv preprint            B. TRACED: Execution-aware pre-training for source
  arXiv:2303.08774, 2023.                                               code. In ICSE, pp. 1–12, 2024b.

Adams, M. D. Principled parsing for indentation-sensitive             Ellison, C. and Roşu, G. An executable formal semantics of
  languages: revisiting landin’s offside rule. In POPL, pp.             C with applications. In POPL, pp. 533–544, 2012.
  511–522, 2013.
                                                                      Friedman, J. H., Hastie, T., and Tibshirani, R. Regulariza-
Agresti, A. Categorical Data Analysis. Wiley, 3 edition,                tion paths for generalized linear models via coordinate
  2013.                                                                 descent. Journal of Statistical Software, 33:1–22, 2010.
Arakelyan, E., Liu, Z., and Augenstein, I. Semantic sensitiv-         Gardner, M., Artzi, Y., Basmov, V., Berant, J., Bogin, B.,
  ities and inconsistent predictions: Measuring the fragility           Chen, S., Dasigi, P., Dua, D., Elazar, Y., Gottumukkala,
  of NLI models. In EACL, pp. 432–444, 2024.                            A., Gupta, N., Hajishirzi, H., Ilharco, G., Khashabi, D.,
                                                                        Lin, K., Liu, J., Liu, N. F., Mulcaire, P., Ning, Q., Singh,
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,
                                                                        S., Smith, N. A., Subramanian, S., Tsarfaty, R., Wallace,
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., et al.
                                                                        E., Zhang, A., and Zhou, B. Evaluating models’ local
 †
     TACC: http://www.tacc.utexas.edu                                   decision boundaries via contrast sets. In Findings of
 ‡
     CosmicAI: https://www.cosmicai.org                                 EMNLP, pp. 1307–1323, 2020.

                                                                 10
                               LLMs Lean on Priors, Not Programming Language Semantics

Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wich-           Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang, T.,
  mann, F. A., and Brendel, W. ImageNet-trained CNNs are               Wang, S., Solar-Lezama, A., Sen, K., and Stoica, I. Live-
  biased towards texture; increasing shape bias improves                codebench: Holistic and contamination free evaluation of
  accuracy and robustness. In ICLR, 2019.                               large language models for code. In ICLR, 2025.

Gentzen, G. Investigations into logical deduction. American          Jin, C. and Rinard, M. Emergent representations of program
  philosophical quarterly, 1(4):288–306, 1964.                          semantics in language models trained on programs. In
                                                                        ICML, pp. 22160–22184, 2024.
Gippert, J. and Schulze, W. The Language of the Caucasian
  Albanians, pp. 167–230. 2023. ISBN 9783110794687.                  Kavukcuoglu, K. Gemini 2.5: Our most intelligent AI
                                                                       model, 2025. URL https://blog.google/te
Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian,            chnology/google-deepmind/gemini-model
  A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A.,             -thinking-updates-march-2025/. Accessed:
  Vaughan, A., et al. The llama 3 herd of models. arXiv                2025-05-21.
  preprint arXiv:2407.21783, 2024.
                                                                     LeetCode. LeetCode Online Judge, 2024. URL https:
Gu, A., Rozière, B., Leather, H., Solar-Lezama, A., Syn-               //leetcode.com. Accessed: 2025-05-16.
  naeve, G., and Wang, S. I. Cruxeval: a benchmark for
  code reasoning, understanding and execution. In ICML,              Li, J., Guo, D., Yang, D., Xu, R., Wu, Y., and He, J. CodeI/O:
  pp. 16568–16621, 2024.                                                Condensing reasoning patterns via code input-output pre-
                                                                        diction. In ICML, 2025.
Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
  Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-R1: In-         Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J.,
  centivizing reasoning capability in llms via reinforcement           Leblond, R., Eccles, T., Keeling, J., Gimeno, F., Lago,
  learning. arXiv preprint arXiv:2501.12948, 2025.                     A. D., Hubert, T., Choy, P., de Masson d’Autume, C.,
                                                                       Babuschkin, I., Chen, X., Huang, P.-S., Welbl, J., Gowal,
Guth, D., Rusu, V., and Roşu, G. A complete formal seman-
                                                                       S., Cherepanov, A., Molloy, J., Mankowitz, D. J., Rob-
  tics of Python 3.3. In CPP, 2020.
                                                                       son, E. S., Kohli, P., de Freitas, N., Kavukcuoglu, K.,
Halstead, M. H. Elements of Software Science. Operat-                  and Vinyals, O. Competition-level code generation with
  ing and Programming Systems Series. Elsevier North-                  AlphaCode. Science, 378:1092–1097, 2022.
  Holland, Inc., 1977.
                                                                     Liu, C., Zhang, S. D., Ibrahimzada, A. R., and Jabbar-
Han, H., Oh, D., and Cha, S. K. Codealchemist: Semantics-              vand, R. Codemind: A framework to challenge large
  aware code generation to find vulnerabilities in JavaScript          language models for code reasoning. arXiv preprint
  engines. In NDSS, 2019.                                              arXiv:2402.09664, 2024.

Harper, R. Practical Foundations for Programming Lan-                Lyu, B., Huang, S., Liang, Z., Sun, Q.-A., and Zhang, J.
  guages. Cambridge University Press, 2016.                            SURGE: On the potential of large language models as
                                                                       general-purpose surrogate code executors. In EMNLP,
Harrell, Frank E., J. Regression Modeling Strategies: With             pp. 3268–3308, 2025.
 Applications to Linear Models, Logistic and Ordinal Re-
  gression, and Survival Analysis. Springer, 2 edition, 2015.        Maveli, N., Vergari, A., and Cohen, S. B. What can large lan-
                                                                      guage models capture about code functional equivalence?
Hathhorn, C., Ellison, C., and Roşu, G. Defining the unde-           In Findings of NAACL, pp. 6880–6918, 2025.
  finedness of c. In PLDI, pp. 336–345, 2015.
                                                                     McCabe, T. J. A complexity measure. IEEE Transactions
Hoerl, A. E. and Kennard, R. W. Ridge regression: Appli-              on software Engineering, pp. 308–320, 1976.
  cations to nonorthogonal problems. Technometrics, 12:
  69–82, 1970.                                                       McCoy, R. T., Pavlick, E., and Linzen, T. Right for the
                                                                      wrong reasons: Diagnosing syntactic heuristics in natural
Huang, D., Zeng, G., Dai, J., Luo, M., Weng, H., Qing,                language inference. In ACL, pp. 3428–3448, 2019.
 Y., Cui, H., Guo, Z., and Zhang, J. Efficoder: Enhanc-
  ing code generation in large language models through               McCracken, D. D. and Reilly, E. D. Backus-Naur form
  efficiency-aware fine-tuning. In ICML, 2025.                        (BNF), pp. 129–131. John Wiley and Sons Ltd., 2003.

Hui, B., Yang, J., Cui, Z., Yang, J., Liu, D., Zhang, L.,            Naik, A., Ravichander, A., Sadeh, N., Rose, C., and Neubig,
  Liu, T., Zhang, J., Yu, B., Lu, K., et al. Qwen2.5-coder             G. Stress test evaluation for natural language inference.
  technical report. arXiv preprint arXiv:2409.12186, 2024.             In COLING, pp. 2340–2353, 2018.

                                                                11
                                 LLMs Lean on Priors, Not Programming Language Semantics

Ni, A., Allamanis, M., Cohan, A., Deng, Y., Shi, K., Sut-              Tibshirani, R. Regression shrinkage and selection via the
  ton, C., and Yin, P. Next: Teaching large language                     lasso. Journal of the Royal Statistical Society: Series B
  models to reason about code execution. arXiv preprint                  (Methodological), 58:267–288, 1996.
  arXiv:2404.14662, 2024.
                                                                       Triton. Triton language core module. https://gith
OpenAI. Gpt-5 mini. https://platform.openai.                             ub.com/triton-lang/triton/blob/main
  com/docs/guides/reasoning, 2025. Reasoning                             /python/triton/language/core.py, 2026.
  models guide; mentions gpt-5-mini. Accessed Sep                        Accessed: 2026-05-28.
  24, 2025.
                                                                       Wadler, P. Monads for functional programming. In Ad-
Orlanski, G., Xiao, K., Garcia, X., Hui, J., Howland, J.,               vanced Functional Programming, pp. 24–52, 1995.
  Malmaud, J., Austin, J., Singh, R., and Catasta, M. Mea-             Wang, L., Lyu, C., Li, W., Xing, R., Ji, T., Yan, L., and
  suring the impact of programming language distribution.               Samih, Y. Large language models as code executors: An
  In ICML, pp. 26619–26645, 2023.                                       exploratory study, 2024. URL https://arxiv.or
                                                                        g/abs/2410.06667.
Orvalho, P. and Kwiatkowska, M. Are large language
  models robust in understanding code against semantics-               Wei, A., Cao, J., Li, R., Chen, H., Zhang, Y., Wang, Z., Liu,
  preserving mutations? arXiv preprint arXiv:2505.10443,                Y., Teixeira, T. S., Yang, D., Wang, K., et al. Equibench:
  2025.                                                                 Benchmarking large language models’ reasoning about
                                                                        program semantics via equivalence checking. In EMNLP,
Penedo, G., Lozhkov, A., Kydlíček, H., Allal, L. B., Beech-            pp. 33856–33869, 2025a.
  ing, E., Lajarín, A. P., Gallouédec, Q., Habib, N., Tunstall,
  L., and von Werra, L. Codeforces. https://huggin                     Wei, A., Suresh, T., Cao, J., Kannan, N., Wu, Y.,
  gface.co/datasets/open-r1/codeforces,                                 Yan, K., Teixeira, T. S., Wang, K., and Aiken, A.
  2025.                                                                 CodeARC: Benchmarking reasoning capabilities of llm
                                                                        agents for inductive program synthesis. arXiv preprint
Pierce, B. C. Types and Programming Languages. MIT                      arXiv:2503.23145, 2025b.
  Press, 2002.
                                                                       Wold, S., Esbensen, K., and Geladi, P. Principal compo-
Plotkin, G. D. A structural approach to operational seman-              nent analysis. Chemometrics and intelligent laboratory
  tics. J. Log. Algebraic Methods Program., pp. 17–139,                 systems, 2(1-3):37–52, 1987.
  2004.
                                                                       Wold, S., Sjöström, M., and Eriksson, L. Pls-regression: A
Ravasi, M. and Vasconcelos, I. Pylops—a linear-operator                 basic tool of chemometrics. Chemometrics and Intelligent
  python library for scalable algebra and optimization. In              Laboratory Systems, 58:109–130, 2001.
  SoftwareX, pp. 1–9, 2020.
                                                                       Xu, R., Cao, J., Lu, Y., Wen, M., Lin, H., Han, X., He, B.,
Ribeiro, M. T., Wu, T., Guestrin, C., and Singh, S. Be-                  Cheung, S.-C., and Sun, L. Cruxeval-x: A benchmark for
  yond accuracy: Behavioral testing of NLP models with                   multilingual code reasoning, understanding and execution.
  CheckList. In ACL, pp. 4902–4912, 2020.                                In ACL, pp. 23762–23779, 2025.

                                                                       Yang, R., Dai, J., Vasilakis, N., and Rinard, M. Evaluating
Ros, u, G. and S, erbănută, T. F. An overview of the k se-
                                                                         the generalization capabilities of large language models
  mantic framework. The Journal of Logic and Algebraic
                                                                         on code reasoning. arXiv preprint arXiv:2504.05518,
  Programming, 79(6):397–434, 2010.
                                                                         2025.
Sun, W., Zhang, C., Zhang, X., Yu, X., Huang, Z., Chen,                Yang, X., Chen, Y., Eide, E., and Regehr, J. Finding and
  P., He, S., Zhao, J., and Liu, K. Beyond instruction                   understanding bugs in c compilers. In PLDI, pp. 283—-
  following: Evaluating inferential rule following of large              294, 2011.
  language models. In CCL, 2025.
                                                                       Yu, S., Wang, T., and Wang, J. Data augmentation by
Team, M. F. C. Cwm: An open-weights llm for research on                  program transformation. Journal of Systems and Software,
  code generation with world models, 2025a.                              190:111304, 2022.

Team, Q. Qwq-32b: Embracing the power of reinforcement                 Zheng, Q., Xia, X., Zou, X., Dong, Y., Wang, S., Xue, Y.,
  learning, March 2025b. URL https://qwenlm.git                          Shen, L., Wang, Z., Wang, A., Li, Y., et al. Codegeex: A
  hub.io/blog/qwq-32b/.                                                  pre-trained model for code generation with multilingual

                                                                  12
                                 LLMs Lean on Priors, Not Programming Language Semantics

  benchmarking on humaneval-x. In SIGKDD, pp. 5673–
  5684, 2023.
Zhuo, T. Y., Vu, M. C., Chim, J., Hu, H., Yu, W., Widyasari,
  R., Yusuf, I. N. B., Zhan, H., He, J., Paul, I., et al. Big-
  codebench: Benchmarking code generation with diverse
  function calls and complex instructions. In ICLR, 2024.

Zou, H. and Hastie, T. Regularization and variable selection
  via the elastic net. Journal of the Royal Statistical Society:
  Series B (Statistical Methodology), 67:301–320, 2005.




                                                                   13
                                                   LLMs Lean on Priors, Not Programming Language Semantics

Appendix
Operator Overloading Conflicts Learned Priors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
C⋆ Formalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
C⋆ Program Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

Code-Complexity Distributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Experiments Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
Is Keyword Obfuscation a Tokenization Artifact? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31

Task Extended Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
Use of External Assets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39




                                                                                                   14
                                 LLMs Lean on Priors, Not Programming Language Semantics

A. Operator Overloading Conflicts Learned Priors
       1   class X:                                                  1    object Main:
       2      def __init__(self, v):                                 2     extension (x: Int)
       3         self.v = v                                          3       def ~>(y: Int): Int = x - y
       4      def __add__(self, other):                              4
       5         return X(self.v - other.v)                          5        @main def run(): Unit =
       6   print((X(10) + X(3)).v) # 7                               6          println(10 ~> 3) // 7

               (a) Python (redefining existing operator).                            (b) Scala (defining new operator).
                                                   Figure 4. Operator Overloading

There are real-world situations where operators and other language constructs can have very different semantic meaning
relative to that assumed during training/pre-training. Very popular languages such as C++, Haskell, Julia, Python, Scala,
Swift, etc., support operator overloading where new semantics can be assigned to existing operators (+, -, *, etc.) or to
completely new symbols (Haskell, Julia, Scala), previously unencountered during training.

B. C⋆ Formalization
Here we describe the syntax and semantics of C⋆ used in all our experiments.

B.1. C⋆ Syntax Description
 1   <program>   ::= <stmt_list>
 2   <stmt_list> ::= (<stmt> ';')*
 3   <stmt>      ::= 'int' <id>
 4               | <id> '=' <aexp>
 5               | 'if' '(' <bexp> ')' '{' <stmt_list> '}' 'else' '{' <stmt_list> '}'
 6               | 'while' '(' <bexp> ')' '{' <stmt_list> '}'
 7               | 'loop' '(' <bexp> ')' '{' <stmt_list> '}'
 8               | 'halt'
 9               | 'continue'
10               | 'break'
11               | 'LE'
12   <aexp>      ::= <id>
13               | <literal>
14               | '(' <aexp>? <mathop> <aexp> ')'
15   <bexp>      ::= '(' <bool> ')'
16               | '(' <aexp> <relop> <aexp> ')'
17               | '(' <lognot> <bexp> ')'
18               | '(' <bexp> <logicalop> <bexp> ')'
19   <bool>      ::= 'true' | 'false'
20   <mathop>    ::= '+' | '-' | '*' | '/' | '%'
21   <relop>     ::= '<' | '<=' | '>' | '>=' | '==' | '!='
22   <lognot>    ::= '!'
23   <logicalop> ::= '&&' | '||'
24   <id>        ::= <letter> (<letter> | <digit>)*
25   <literal>   ::= <digit>+
26   <letter>    ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j'
27               | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't'
28               | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
29               | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J'
30               | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T'
31               | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
32   <digit>     ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

                                 Figure 5. Complete syntax of C⋆ used in our experiments in EBNF.

The C⋆ syntax used in all our experiments is given in EBNF in Figure 5. The terminals are shown in red while the
non-terminals are shown in blue.

B.2. Small-step Operational Semantics (S) Rules for C⋆
We formalize C⋆ using a small-step structural operational se-                 Table 7. Metavariables used in the S formalization of C⋆ .
mantics (S). We use two types of configurations: expression              Meta-var     Sort          Ranges over / Domain
configurations ⟨expr, σ, χ⟩, and statement configurations:               x            id            Identifiers (program variable names)
⟨stmt, σ, χ⟩, where σ : id 7→ literal is the program                     v            literal       Integer literals
                                                                         q            bool          Boolean literals
store mapping identifiers to values, and χ is a last-in, first-out       a            aexp          Integer expressions
control stack of loop headers that records the dynamic nesting           b            bexp          Boolean expressions
                                                                         s            stmt          Statements of the language
of currently active loops: χ ::= ϵ | s :: χ′ . The top of χ is           SL           stmt_list     Finite statement lists (SL ::= ϵ | s ::   SL’)
the innermost executing loop.

                                                                15
                                  LLMs Lean on Priors, Not Programming Language Semantics

We use standard metavariables x,v,q,a,b,s,SL with their sorts summarized in Table 7. For example, a ranges over
arithmetic expressions, so rules mentioning a1,a2,... concern arithmetic evaluation. Auxiliary metafunctions (push,
pop, top) for manipulating the control stack χ and concatenating ( ++ ) statement lists SL are given in Table 8.
                              Table 8. Metafunctions for control stack and statement-list concatenation.
                Function   Signature                                Definition

                push       stmt × Stack → Stack                     push(s, χ) ≜ s :: χ
                pop        Stack̸=ϵ → Stack                         pop(s :: χ)
                                                                              (≜ χ
                                                                                ϵ if χ = ϵ,
                top        Stack → stmt ∪ {ϵ}                       top(χ) ≜
                                                                                s if χ = s :: χ′
                                                                                     (
                                                                                       SL2                if SL1 = ϵ,
                ++         stmt_list × stmt_list → stmt_list        SL1 ++ SL2 ≜
                                                                                       s :: (SL1′ ++ SL2) if SL1 = s :: SL1′ .


Program execution proceeds by repeatedly applying the transition relation → to expression configurations and ⇒ to
statement configurations, starting from ⟨SL, σ, χ⟩, where SL is the program’s statement list, until a terminal configuration is
reached. We treat ⟨ϵ, σ, χ⟩, ⟨halt, σ, χ⟩, and ⟨ERROR, σ, χ⟩ statement configurations as terminal configurations.
The complete set of small-step S rules defining the semantics of C⋆ is given in Table 9.
                                            Table 9. Small-step S rules used to formalize C⋆ .
 Rule      Formalization                                                                                     Description
 Rule 1                                                                                                      Variable lookup returns value.
                                                      σ(x) = v
                                                    ⟨x, σ, χ⟩ → v
 Rule 2                                                                                                      Read of undefined variable errors.
                                                      σ(x) = ⊥
                                             ⟨x, σ, χ⟩ → ⟨ERROR, σ, χ⟩
 Rule 3                                                                                                      Declared int variable initialized to 0.

                                   ⟨int x ::     SL, σ, χ⟩ ⇒ ⟨SL, σ[x 7→ 0], χ⟩
 Rule 4                                                                                                      Assignment expression steps.
                                               ⟨a, σ, χ⟩ → ⟨a’, σ, χ⟩
                              ⟨x := a ::      SL, σ, χ⟩ ⇒ ⟨x := a’ ::            SL, σ, χ⟩
 Rule 5                                                                                                      Writeback to existing variable.
                                                      σ(x) ̸= ⊥
                                  ⟨x := v ::        SL, σ, χ⟩ ⇒ ⟨SL, σ[x 7→ v], χ⟩
 Rule 6                                                                                                      Assign to undefined variable errors.
                                                      σ(x) = ⊥
                                       ⟨x := v ::     SL, σ, χ⟩ ⇒ ⟨ERROR, σ, χ⟩
 Rule 7                                                                                                      Plus - step left operand.
                                             ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
                                        ⟨a1 + a2, σ, χ⟩ → ⟨a1’ + a2, σ, χ⟩
 Rule 8                                                                                                      Plus - step right operand.
                                             ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
                                        ⟨v1 + a2, σ, χ⟩ → ⟨v1 + a2’, σ, χ⟩
 Rule 9                                                                                                      Plus - compute.
                                                    v3 = v1 + v2
                                              ⟨v1 + v2, σ, χ⟩ → v3
 Rule 10                                                                                                     Minus - step left operand.
                                             ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
                                        ⟨a1 - a2, σ, χ⟩ → ⟨a1’ - a2, σ, χ⟩
 Rule 11                                                                                                     Minus - step right operand.
                                             ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
                                        ⟨v1 - a2, σ, χ⟩ → ⟨v1 - a2’, σ, χ⟩
 Rule 12                                                                                                     Minus - compute.
                                                    v3 = v1 − v2
                                              ⟨v1 - v2, σ, χ⟩ → v3
 Rule 13                                                                                                     Times - step left operand.
                                             ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
                                        ⟨a1 * a2, σ, χ⟩ → ⟨a1’ * a2, σ, χ⟩



                                                                        16
          LLMs Lean on Priors, Not Programming Language Semantics


Rule 14                                                             Times - step right operand.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
             ⟨v1 * a2, σ, χ⟩ → ⟨v1 * a2’, σ, χ⟩
Rule 15                                                             Times - compute.
                        v3 = v1 ∗ v2
                   ⟨v1 * v2, σ, χ⟩ → v3
Rule 16                                                             Division - step left operand.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
             ⟨a1 / a2, σ, χ⟩ → ⟨a1’ / a2, σ, χ⟩
Rule 17                                                             Division - step right operand.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
             ⟨v1 / a2, σ, χ⟩ → ⟨v1 / a2’, σ, χ⟩
Rule 18                                                             Division - compute (nonzero).
                   v2 ̸= 0      v3 = v1/v2
                   ⟨v1 / v2, σ, χ⟩ → v3
Rule 19                                                             Division by zero errors.
                             v2 = 0
              ⟨v1 / v2, σ, χ⟩ → ⟨ERROR, σ, χ⟩
Rule 20                                                             Modulus - step left operand.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
             ⟨a1 % a2, σ, χ⟩ → ⟨a1’ % a2, σ, χ⟩
Rule 21                                                             Modulus - step right operand.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
             ⟨v1 % a2, σ, χ⟩ → ⟨v1 % a2’, σ, χ⟩
Rule 22                                                             Modulus - compute (nonzero).
                  v2 ̸= 0      v3 = v1 % v2
                   ⟨v1 % v2, σ, χ⟩ → v3
Rule 23                                                             Modulus by zero errors.
                             v2 = 0
              ⟨v1 % v2, σ, χ⟩ → ⟨ERROR, σ, χ⟩
Rule 24                                                             Unary minus - step.
                    ⟨a, σ, χ⟩ → ⟨a’, σ, χ⟩
                 ⟨- a, σ, χ⟩ → ⟨- a’, σ, χ⟩
Rule 25                                                             Unary minus - compute.
                            v2 = −v1
                     ⟨- v1, σ, χ⟩ → v2
Rule 26                                                             Unary plus - step.
                    ⟨a, σ, χ⟩ → ⟨a’, σ, χ⟩
                 ⟨+ a, σ, χ⟩ → ⟨+ a’, σ, χ⟩
Rule 27                                                             Unary plus - no-op.

                      ⟨+ v, σ, χ⟩ → v
Rule 28                                                             Less-than - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
             ⟨a1 < a2, σ, χ⟩ → ⟨a1’ < a2, σ, χ⟩
Rule 29                                                             Less-than - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
             ⟨v1 < a2, σ, χ⟩ → ⟨v1 < a2’, σ, χ⟩
Rule 30                                                             Less-than true.
                             v1 < v2
                  ⟨v1 < v2, σ, χ⟩ → true
Rule 31                                                             Less-than false.
                             v1 ≥ v2
                  ⟨v1 < v2, σ, χ⟩ → false
Rule 32                                                             Less-than-equal - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
            ⟨a1 <= a2, σ, χ⟩ → ⟨a1’ <= a2, σ, χ⟩




                                             17
          LLMs Lean on Priors, Not Programming Language Semantics


Rule 33                                                             Less-than-equal - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
            ⟨v1 <= a2, σ, χ⟩ → ⟨v1 <= a2’, σ, χ⟩
Rule 34                                                             Less-than-equal true.
                          v1 ≤ v2
                  ⟨v1 <= v2, σ, χ⟩ → true
Rule 35                                                             Less-than-equal false.
                          v1 > v2
                 ⟨v1 <= v2, σ, χ⟩ → false
Rule 36                                                             Greater-than - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
             ⟨a1 > a2, σ, χ⟩ → ⟨a1’ > a2, σ, χ⟩
Rule 37                                                             Greater-than - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
             ⟨v1 > a2, σ, χ⟩ → ⟨v1 > a2’, σ, χ⟩
Rule 38                                                             Greater-than true.
                          v1 > v2
                  ⟨v1 > v2, σ, χ⟩ → true
Rule 39                                                             Greater-than false.
                          v1 ≤ v2
                  ⟨v1 > v2, σ, χ⟩ → false
Rule 40                                                             Greater-than-equal - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
            ⟨a1 >= a2, σ, χ⟩ → ⟨a1’ >= a2, σ, χ⟩
Rule 41                                                             Greater-than-equal - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
            ⟨v1 >= a2, σ, χ⟩ → ⟨v1 >= a2’, σ, χ⟩
Rule 42                                                             Greater-than-equal true.
                          v1 ≥ v2
                  ⟨v1 >= v2, σ, χ⟩ → true
Rule 43                                                             Greater-than-equal false.
                          v1 < v2
                 ⟨v1 >= v2, σ, χ⟩ → false
Rule 44                                                             Equality - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
            ⟨a1 == a2, σ, χ⟩ → ⟨a1’ == a2, σ, χ⟩
Rule 45                                                             Equality - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
            ⟨v1 == a2, σ, χ⟩ → ⟨v1 == a2’, σ, χ⟩
Rule 46                                                             Equality true.
                          v1 = v2
                  ⟨v1 == v2, σ, χ⟩ → true
Rule 47                                                             Equality false.
                          v1 ̸= v2
                 ⟨v1 == v2, σ, χ⟩ → false
Rule 48                                                             Not-equal - step left.
                  ⟨a1, σ, χ⟩ → ⟨a1’, σ, χ⟩
            ⟨a1 != a2, σ, χ⟩ → ⟨a1’ != a2, σ, χ⟩
Rule 49                                                             Not-equal - step right.
                  ⟨a2, σ, χ⟩ → ⟨a2’, σ, χ⟩
            ⟨v1 != a2, σ, χ⟩ → ⟨v1 != a2’, σ, χ⟩
Rule 50                                                             Not-equal true.
                          v1 ̸= v2
                  ⟨v1 != v2, σ, χ⟩ → true
Rule 51                                                             Not-equal false.
                          v1 = v2
                 ⟨v1 != v2, σ, χ⟩ → false




                                         18
                              LLMs Lean on Priors, Not Programming Language Semantics


Rule 52                                                                                                       AND - step left.
                                         ⟨b1, σ, χ⟩ → ⟨b1’, σ, χ⟩
                                ⟨b1 && b2, σ, χ⟩ → ⟨b1’ && b2, σ, χ⟩
Rule 53                                                                                                       AND - step right.
                                         ⟨b2, σ, χ⟩ → ⟨b2’, σ, χ⟩
                                ⟨q1 && b2, σ, χ⟩ → ⟨q1 && b2’, σ, χ⟩
Rule 54                                                                                                       AND true.
                                         q1 = true ∧ q2 = true
                                        ⟨q1 && q2, σ, χ⟩ → true
Rule 55                                                                                                       AND false.
                                        q1 = false ∨ q2 = false
                                        ⟨q1 && q2, σ, χ⟩ → false
Rule 56                                                                                                       OR - step left.
                                         ⟨b1, σ, χ⟩ → ⟨b1’, σ, χ⟩
                                ⟨b1 || b2, σ, χ⟩ → ⟨b1’ || b2, σ, χ⟩
Rule 57                                                                                                       OR - step right.
                                         ⟨b2, σ, χ⟩ → ⟨b2’, σ, χ⟩
                                ⟨q1 || b2, σ, χ⟩ → ⟨q1 || b2’, σ, χ⟩
Rule 58                                                                                                       OR true.
                                         q1 = true ∨ q2 = true
                                        ⟨q1 || q2, σ, χ⟩ → true
Rule 59                                                                                                       OR false.
                                        q1 = false ∧ q2 = false
                                        ⟨q1 || q2, σ, χ⟩ → false
Rule 60                                                                                                       NOT - step.
                                          ⟨b, σ, χ⟩ → ⟨b’, σ, χ⟩
                                         ⟨!b, σ, χ⟩ → ⟨!b’, σ, χ⟩
Rule 61                                                                                                       NOT of false is true.
                                               q = false
                                           ⟨!q, σ, χ⟩ → true
Rule 62                                                                                                       NOT of true is false.
                                                q = true
                                           ⟨!q, σ, χ⟩ → false
Rule 63                                                                                                       Sequence head steps.
                                                           ′    ′
                                         ⟨s, σ, χ⟩ ⇒ ⟨s’, σ , χ ⟩
                                                                         ′   ′
                                ⟨s ::    SL, σ, χ⟩ ⇒ ⟨s’ ::     SL, σ , χ ⟩
Rule 64                                                                                                       If-else predicate steps.
                                           ⟨b, σ, χ⟩ → ⟨b’, σ, χ⟩
          ⟨if(b) {SL1} else {SL2} ::     SL3, σ, χ⟩ ⇒ ⟨if(b’) {SL1} else {SL2} ::                SL3, σ, χ⟩
Rule 65                                                                                                       If-else takes then-branch.
                                                q = true
                    ⟨if(q) {SL1} else {SL2} ::        SL3, σ, χ⟩ ⇒ ⟨SL1 ++ SL3, σ, χ⟩
Rule 66                                                                                                       If-else takes else-branch.
                                               q = false
                    ⟨if(q) {SL1} else {SL2} ::        SL3, σ, χ⟩ ⇒ ⟨SL2 ++ SL3, σ, χ⟩
Rule 67                                                                                                       While creates loop frame.

          ⟨while(b) {SL} ::   SL1, σ, χ⟩ ⇒ ⟨loop(b) {SL} ::         SL1, σ, push(while(b) {SL}, χ)⟩
Rule 68                                                                                                       Loop predicate steps.
                                          ⟨b, σ, χ⟩ → ⟨b’, σ, χ⟩
                   ⟨loop(b) {SL} ::      SL1, σ, χ⟩ ⇒ ⟨loop(b’) {SL} ::             SL1, σ, χ⟩
Rule 69                                                                                                       Loop exits on false.
                                               q = false
                          ⟨loop(q) {SL} ::       SL1, σ, χ⟩ ⇒ ⟨SL1, σ, pop(χ)⟩
Rule 70                                                                                                       Insert loop-body into statement list while
                                                q = true                                                      adding a loop-end (LE) marker in be-
                     ⟨loop(q) {SL} ::     SL1, σ, χ⟩ ⇒ ⟨SL ++ (LE ::             SL1), σ, χ⟩                  tween.




                                                                    19
                 LLMs Lean on Priors, Not Programming Language Semantics


Rule 71                                                                      break propagates to LE inside loop.
                                 χ ̸= ϵ ∧ s ̸= LE
             ⟨break ::    s ::    SL, σ, χ⟩ ⇒ ⟨break ::       SL, σ, χ⟩
Rule 72                                                                      break at LE pops χ and terminates loop.
                                 χ ̸= ϵ ∧ s = LE
               ⟨break ::    s ::     SL, σ, χ⟩ ⇒ ⟨SL, σ, pop(χ)⟩
Rule 73                                                                      break outside loop errors.
                                      χ=ϵ
                   ⟨break ::       SL, σ, χ⟩ ⇒ ⟨ERROR, σ, χ⟩
Rule 74                                                                      continue propagates to LE inside loop.
                                 χ ̸= ϵ ∧ s ̸= LE
          ⟨continue ::    s ::    SL, σ, χ⟩ ⇒ ⟨continue ::       SL, σ, χ⟩
Rule 75                                                                      continue at LE pops χ and restarts loop.
                     χ ̸= ϵ ∧ s = LE         s1 = top(χ)
          ⟨continue ::     s ::    SL, σ, χ⟩ ⇒ ⟨s1 ::    SL, σ, pop(χ)⟩
Rule 76                                                                      continue outside loop errors.
                                      χ=ϵ
                  ⟨continue ::       SL, σ, χ⟩ ⇒ ⟨ERROR, σ, χ⟩
Rule 77                                                                      LE pops χ and restarts loop.
                                   s = top(χ)
                 ⟨LE ::    SL, σ, χ⟩ ⇒ ⟨s ::    SL, σ, pop(χ)⟩
Rule 78                                                                      Halt statement terminates program execu-
                                                                             tion.
                    ⟨halt ::       SL, σ, χ⟩ ⇒ ⟨halt, σ, χ⟩




                                                    20
                                LLMs Lean on Priors, Not Programming Language Semantics

C. C⋆ Program Example
In this section, we describe the collection of C⋆ programs for: (1) the Human-Written, and (2) the Fuzzer-Generated datasets
and provide examples.

C.1. Human-Written Dataset
                                                                          1   int sum;
                                                                          2   int i;
                                                                          3   int l;
                                                                          4   int r;
                                                                          5   l = 3;
                                                                          6   r = 8;
                                                                          7   i = l;
 1   int sumEven(int l, int r)                                            8   while(i <= r)
 2   {                                                                    9   {
 3      int sum = 0;                                                     10      if((i % 2) == 0)
 4      for (int i = l; i <= r; i++)                                     11      {
 5      {                                                                12         sum = (sum + i);
 6         if (i % 2 == 0)                                               13      }
 7         {                                                             14      else
 8            sum += i;                                                  15      {
 9         }                                                             16
10      }                                                                17        };
11      return sum;                                                      18        i = (i + 1);
12   }                                                                   19   };

(a) The C++ solution to the problem “MBCPP/962” in Babel-                 (b) The C⋆ program re-written from the C++ solution.
Code MBPP and one public test case. The public test we use is
sumEven(3, 8)==18.
               Figure 6. An example of re-writing a C++ program into an C⋆ program in the Human-Written dataset.

In Figure 6, we show an example C++ solution to a problem from the BabelCode MBPP benchmark (Figure 6a) and its
corresponding C⋆ program re-written by us (Figure 6b). To convert the C++ program into an C⋆ program, we remove the
function definitions (e.g., sumEven), while keeping the body of the function. Unsupported syntactic constructs are either
re-written (e.g., replacing the for loop with a while loop) or removed (e.g., removing the return statement). One public
test case is adopted as the program input, and its output is used to verify correctness. In this example, l is assigned to 3 and
r is assigned to 8, the test oracle 18 is used to verify the final-state of sum after program execution.
The code-complexity profile of the C⋆ program in Figure 6b is: control-flow complexity (ΩCC = 3, ΩIf = 1, ΩLoop = 1, Ω̂If =
1, Ω̂Loop = 1), data-flow complexity (ΩDD = 12, Ω̂Assign = 12), and program-size complexity (ΩLoc = 19, ΩVol = 294, ΩVoc =
23, Ω̂Trace = 29).

C.2. Fuzzer-Generated Dataset
The Fuzzer-Generated dataset is constructed using a semantic aware grammar based fuzzer with knobs for: (1) the generation
probabilities of different statements, (2) the maximum nesting depth of the program (nested loops and conditionals), (3) the
maximum and the minimum number of statements to generate per block, (4) the maximum number of terms and variable
terms in arithmetic expressions, (5) the maximum number of terms in boolean expressions (relational and logical), and
(6) the maximum and the minimum number of variable declarations in a program. We use the settings as shown in Table 10.
The fuzzer starts by randomly sampling an integer from the range defined by the minimum and maximum number of variable
declarations. This integer specifies the number of variables to be declared and used for the C⋆ program being generated.
The fuzzer next samples alphabets from the set {a-z} and {A-Z} until the required number of unique alphabets to use as
variables is obtained. Declaration statments are then generated to declare these variables.
Following this, one assignment statement is generated per declared variable to assign it with a randomly generated arithmetic
expression. The arithmetic expression itself is generated using the pool of declared variables and integer constants (sampled
from the set {0-9}).
The fuzzer next generates statements from the set {Assignment, While, If, Break, Continue, Halt} in accordance with the
statement probabilities given in Table 10. No more than three statements are generated per block. These probabilities
are used until the generation block depth reaches the specified minimum block depth (5). Beyond this, the statement
probabilities are cosine-tapered to decrease the probabilities of generating while and if-else statements. For generation
processes where the block depth reaches the maximum specified block depth (10), the probabilities of further generating
while and if-else is reduced to zero.

                                                              21
                                   LLMs Lean on Priors, Not Programming Language Semantics

To ensure high probability in termination of loops, the fuzzer generates Table 10. Settings for the fuzzer knobs used to generate
one new variable (prefixed with ble) per loop. A monotone update type C programs for the Fuzzer-Generated dataset.
                                                                           ⋆

(incrementing or decrementing) is chosen for this variable each with a Knob                                               Value
50% probability of being chosen. The bounds, initial (before iteration)                        Structural limits
and expected final (after loop termination) values are then chosen from Minimum number of statements per block              1
the range [-20,20] and the size of the update per iteration from the range Maximum number of statements per block           3
                                                                           Minimum block depth                              5
[1 step, (final / 3) step]. The variable monotone update statement is Maximum block depth                                   10
inserted towards the end of the loop body and the bound is conjoined Minimum number of variables                            5
                                                                           Maximum number of variables                      10
with the loop predicate. This prevents infinite loops. The declaration and
                                                                                      Statement generation probabilities
assignment statements for these new generated variables is inserted right
                                                                           Assignment                                      0.4
after the assignment statements for the intially chosen variables.         While                                           0.3
The fuzzer can be used to generate extremely complex C⋆ programs (as IfBreak                                                       0.2
                                                                                                                                  0.09
measured by the code-complexity metrics introduced earlier) with high Continue                                                   0.005
probability of normal program termination. Figure 11 shows an example Halt                                                       0.005

C program from the Fuzzer-Generated dataset that was generated using
  ⋆                                                                                             Expression  limits

our fuzzer. Its code-complexity metric profile is: control-flow complexity Maximum number of terms in arithmetic expr               6
                                                                             Maximum number of variable terms in arithmetic expr    3
(ΩCC = 62, ΩIf = 5, ΩLoop = 6, Ω̂If = 3, Ω̂Loop = 5), data-flow complexity Maximum number of terms in boolean expr                  4
(ΩDD = 2603, Ω̂Assign = 86), and program-size complexity (ΩLoc = 492,
ΩVol = 37140, ΩVoc = 91, Ω̂Trace = 249). This shows that out of the
maximum loop nesting depth six (ΩLoop ) present in the program, the execution reaches a maximum loop nesting depth of
five (Ω̂Loop ) implying that the execution reached a loop contining four outer loops.
Figure 11 shows one of the programs from the Fuzzer-Generated dataset that the G EMINI-2.5-pro model was successful on
in the PredState task.

D. Code-Complexity Distributions

                                             Human-Written          LLM-Translated                Fuzzer-Generated
                         103                                  101                                 101

                         102
                                                                                          ΩLoop
              ΩCC




                                                    ΩIf




                         101
                                                              100                                 100

                         100                                    0                                   0
                         101                                  101                                 105
                                                                                                  104
                                                                                                  103
                                                    Ω̂Loop




                                                                                          ΩDD
              Ω̂If




                                                                                                  102
                         100                                  100                                 101
                                                                                                  100
                           0                                    0                                   0
                         104                                  104                                 106
                         103                                  103                                 105
              Ω̂Assign




                         102                                                                      104
                                                    ΩLoc




                                                                                          ΩVol




                                                              102
                         101                                                                      103
                                                              101
                                                                                                  102
                         100
                           0                                  100                                 101
                         103                                  104                                  1.0


                              2                               103                                  0.8
                         10
                                                    Ω̂Trace
              ΩVoc




                                                                                                   0.6
                                                              102
                         101                                                                       0.4
                                                              101
                                                                                                   0.2


                         100                                  100                                  0.0
                                                                                                         0.0   0.2   0.4   0.6   0.8   1.0

Figure 7. Distributions of the code-complexity metrics extended cyclomatic complexity (ΩCC ), maximum nested if–else (ΩIf ) and nested
loop (ΩLoop ) depths , maximum taken nested if–else (Ω̂If ), and taken nested loop (Ω̂Loop ) depths, the program data-flow complexity metrics
DepDegree (ΩDD ) and the total number of assignments to variables in execution traces (Ω̂Assign ), and finally the program size complexity
metrics, lines of code (ΩLoc ), Halstead metrics Volume (ΩVol ) and Vocabulary(ΩVoc ), and execution trace length (Ω̂Trace ).


                                                                     22
                               LLMs Lean on Priors, Not Programming Language Semantics

The distributions of the code-complexity metrics used to characterize the control-flow, data-flow, and the program size
complexity are given in Figure 7. We mark the median and the extremas for each distribution. We see that the median ΩIf
and ΩLoop is similar for the Human-Written and the LLM-Translated datasets, whereas for every other metric, the LLM-
Translated has slightly higher median values than Human-Written and thus more complex programs. The Fuzzer-Generated
dataset on the other hand has median values significantly higher for every metric except Ω̂Trace and Ω̂Assign , than the other
two datasets. This implies that programs in the Fuzzer-Generated and the LLM-Translated datasets run for roughly the same
number of execution steps (measured as per the S semantics) but the programs in the former are significantly more complex
than those in the latter.

E. Experiments Details
E.1. Parameters
We use the default temperature settings for reasoning models by not specifying a specific temperature. For other non-
reasoning models, we set the temperature to zero. All models are evaluated under one-shot setting.

E.2. Compute Resources
The experiments on open-weight models with fewer than 70 billion parameters are conducted on a single compute node
equipped with one NVIDIA H200 GPU (96 GB memory), an NVIDIA Grace CPU @ 3.1 GHz with 72 cores, and 116 GB
LPDDR5 memory. For experiments involving 70B-parameter models, we use four compute nodes.

E.3. Prompts

 E.3.1 Prompt for PredState task.
 No-semantics:
 You are an interpreter for my language called {language}.

 Here is the {language} program
        {program}

 S:
 You are an interpreter for a language called {language}. I will describe the syntax for {language} in EBNF and
 its semantics using small-step operational semantics. You will use this to execute a {language} program. You
 will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give
 are correct. A program has finished execution when one of the terminal configurations ⟨ϵ, σ, χ⟩,⟨{HALT}, σ, χ⟩,
 ⟨{ERROR}, σ, χ⟩ is reached.

 Here is the syntax of {language} in EBNF
        {syntax}

 Here is the small-step operational semantics of {language}
        {semantics}

 Here is the {language} program
        {program}

 K-semantics:
 You are an interpreter for a language called {language}. I will describe the syntax and the semantics of the
 language using the K-framework. You will use this to execute a {language} program. You will only use the rules
 described in the semantics I provide. Assume all the rules in the semantics I give are correct.
 Here is the K-framework formalization of {language}
        {semantics}

 Here is the {language} program
        {program}


 ## TASK: predict the values of all the declared variables after executing the above program.
 - If you think the program will never terminate, answer with the special word ’##timeout##’:

        <answer>##timeout##</answer>

 - If you believe the program has an error or has undefined behavior, answer with the special word ’##error##’:

        <answer>##error##</answer>

 - Otherwise, provide the predicted values of all the declared variables in the following format:




                                                             23
                            LLMs Lean on Priors, Not Programming Language Semantics

       <answer>[Your answer]</answer>

Here is one example:

** Program **
int a;
int b;
int ans;
int c;
a {ASSIGN_OP} 10;
b {ASSIGN_OP} 23;
c {ASSIGN_OP} 12;
ans {ASSIGN_OP} a {ADD_OP} b;


The final expected output is:
<answer>
  <a>10</a>
  <b>23</b>
  <c>12</c>
  <ans>33</ans>
</answer>


Non-CoT: Only write the answer. You **MUST** wrap your prediction with ‘<answer>’ tags.
CoT: Explain your reasoning step-by-step **before** answering. Wrap your reasoning in ‘<reason>’ tags. Note
that you **MUST** wrap your reasoning steps with ‘<reason>’ tags and the prediction with ‘<answer>’ tags.



E.3.2 Prompt for PredRule task.
S:
You are an interpreter for a language called {language}. I will describe the syntax for {language} in EBNF and
its semantics using small-step operational semantics. You will use this to execute a {language} program. You
will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give
are correct. A program has finished execution when one of the terminal configurations ⟨ϵ, σ, χ⟩,⟨{HALT}, σ, χ⟩,
⟨{ERROR}, σ, χ⟩ is reached.

Here is the syntax of {language} in EBNF
       {syntax}

Here is the small-step operational semantics of {language}
       {semantics}

Here is the {language} program
       {program}

## TASK:
For each question below, you’ll be given:
1. A program
2. The program state (σ) (variable values) before executing the program
3. The control stack (χ) before executing the program

Assume that all necessary variables have been declared and have the values as indicated in the provided program
state.
You must:
- Correctly identify and apply the small-step operational semantic rules required to evaluate the program to
completion
- List them in the correct order of application

A program is executed completely when its evaluation reaches one of the terminal configurations
⟨ϵ, σ, χ⟩,⟨{HALT}, σ, χ⟩, ⟨{ERROR}, σ, χ⟩.


Here is one example:
** Program:**
{WHILE} (n {LTEQ_OP} 0)
{{
      {HALT};
}};

**Program state(σ) before execution:**
{{’n’: 100, ’sum’: 0}}

**Control stack(χ) before execution:**
ϵ


This is the sequence of steps:



                                                       24
                            LLMs Lean on Priors, Not Programming Language Semantics

1. First, we transform the {WHILE} into {LOOP} using **Rule 67**.
2. Reduce the loop predicate using **Rule 68**.
3. The loop predicate is a {LTEQ_OP} operator which triggers **Rule 32** to first reduce the left-hand side ’n’
to a literal using **Rule 1**.
4. The right-hand side is already a literal and since ’100’ is not less-than or equal to ’0’. We use **Rule
35** to evaluate this operation to ’false’.
5. Since the loop predicate is ’false’, we use **Rule 69** to terminate the loop.
6. Since there are no more statements left, we have reached the terminal configuration ⟨ϵ, σ, χ⟩ and the program
evaluation terminates.

Therefore, the final answer is:
<ans>
  <answer id="1">
    <rule>67</rule>
    <rule>68</rule>
    <rule>32</rule>
    <rule>1</rule>
    <rule>35</rule>
    <rule>69</rule>
  </answer>
</ans>


## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
  ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
  ...
  </answer>
  ...
</ans>

### Notes:
- Each <answer id="N"> element corresponds to the N-th question.
- Inside each <answer> block, list each semantic rule in the correct order using <rule> tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- A single rule may be needed to be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.


K-semantics:
You are an interpreter for a language called {language}. I will describe the syntax and the semantics of the
language using the K-framework. You will use this to execute a {language} program. You will only use the rules
described in the semantics I provide. Assume all the rules in the semantics I give are correct.

Here is the K-framework formalization of {language}
       {semantics}

Here is the {language} program
       {program}


## TASK:
For each question below, you’ll be given:
1. A program
2. The program state (σ) (variable values) before executing the program
3. The control stack (χ) before executing the program

Assume that all necessary variables have been declared and have the values as
indicated in the provided program state.

You must:
- Correctly identify and apply the K-semantic rules required to evaluate the program to completion
- List them in the correct order of application




                                                       25
                            LLMs Lean on Priors, Not Programming Language Semantics

Here is one example:
** Program:**
{WHILE} (n {LTEQ_OP} 0)
{{
      {HALT};
}};

**Program state(σ) before execution:**
{{’n’: 100, ’sum’: 0}}

**Control stack(χ) before execution:**
ϵ


This is the sequence of steps:
1. First, we transform the ’{WHILE}’ into ’{WHILE}1’ while also inserting a ’breakMarker’ after ’{WHILE}1’ using
**Rule 24**.
2. Next we transform the ’{WHILE}1’ into an ’{IF}-{ELSE}’ with the ’{WHILE}1’ as the body of the ’{IF}’ using
**Rule 25**.
3. We then reduce the loop predicate to a boolean by first reducing left-hand-side which is a variable using
**Rule 1** and then applying the ’{LTEQ_OP}’ using **Rule 13*.
4. Since the loop predicate evaluates to ’false’, we apply the ’{IF}’ not taken rule **Rule 23** to take the
’{ELSE}’ branch which is empty.
5. Finally, we evaluate the ’breakMarker’ statement using **Rule 27** to conclude the program execution.

Therefore, the final answer is:
<ans>
  <answer id="1">
    <rule>24</rule>
    <rule>25</rule>
    <rule>1</rule>
    <rule>13</rule>
    <rule>23</rule>
    <rule>27</rule>
  </answer>
</ans>


## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
  ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
  ...
  </answer>
  ...
</ans>

### Notes:
- Each ’<answer id="N">’ element corresponds to the N-th question.
- Inside each ’<answer>’ block, list each semantic rule in the correct order using ’<rule>’ tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- Only rules that have names indicated in ’[]’ adjacent to it must be reported in the answer.
- A single rule may be needed to be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.


Non-CoT: Only output the ’<ans>’ XML block. Do not include any other content.
CoT: Explain your reasoning step-by-step **before** answering. Wrap your reasoning in ’<reason>’ tags.




                                                       26
                            LLMs Lean on Priors, Not Programming Language Semantics

E.3.3 Prompt for PredTrace task.
S:
You are an interpreter for a language called {language}. I will describe the syntax for {language} in EBNF and
its semantics using small-step operational semantics. You will use this to execute a {language} program. You
will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give
are correct. A program has finished execution when one of the terminal configurations ⟨ϵ, σ, χ⟩,⟨{HALT}, σ, χ⟩,
⟨{ERROR}, σ, χ⟩ is reached.

Here is the syntax of {language} in EBNF
       {syntax}

Here is the small-step operational semantics of {language}
       {semantics}

Here is the {language} program
       {program}

## TASK:
Given a program and its semantics, predict the execution trace. Your goal is to simulate execution, step by step
of executing the program using the given small-step operational semantics rules. Do not skip any rules that is
needed to evaluate the program. You will output your answer in the following format.

## Response Format:
Respond with an XML block structured as follows:

<answer>
  <step>
    <rule>1</rule>
    <program_state>
      <n>0</n>
      <sum>0</sum>
    </program_state>
  </step>
  <step>
    <rule>2</rule>
    <program_state>
      <n>100</n>
      <sum>0</sum>
    </program_state>
  </step>
...
</answer>

## Here is an example:

Here is the {language} program:
int i;
int j;
i {ASSIGN_OP} 0;
{WHILE} (i {LT_OP} 2)
{{
      {HALT};
}};


## Expected output:
<answer>
  <step>
    <rule>3</rule>
    <program_state>
      <i>0</i>
    </program_state>
  </step
  <step>
    <rule>3</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>5</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>




                                                       27
                              LLMs Lean on Priors, Not Programming Language Semantics

    <rule>67</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>68</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>28</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>1</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>30</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>70</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>78</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
</answer>


## Notes:
- Each ’<step>’ must correspond to **exactly one small-step operational semantics rule** that is needed to
evaluate a statement in the given program.
- The ’<rule>’ must indicate a rule used in the evaluation of a statement.
- The ’<program_state>’ must represent the **entire program state immediately after** the execution of that rule.
- The program state must list **all variables currently in scope**, using the variable names as XML tags and
their current values as tag content.
- Include variables even if they did not change.
- Do not skip any step or merge multiple steps into one.
- Do not skip any rules (including those used to reduce expressions and variables) that are needed to evaluate
the program.
- The program execution is complete when one of the terminal configurations ⟨ϵ, σ, χ⟩,⟨{HALT}, σ, χ⟩, ⟨{ERROR}, σ, χ⟩ is
reached


K-semantics:
You are an interpreter for a language called {language}. I will describe the syntax and the semantics of the
language using the K-framework. You will use this to execute a {language} program. You will only use the rules
described in the semantics I provide. Assume all the rules in the semantics I give are correct.

Here is the K-framework formalization of {language}
       {semantics}

Here is the {language} program
       {program}


## TASK:
Given a program and its semantics, predict the execution trace.      Your goal is to simulate execution, step by step



                                                           28
                            LLMs Lean on Priors, Not Programming Language Semantics

of executing the program using the given K-framework semantics rules. Do not skip any rules that is needed to
evaluate the program. You will output your answer in the following format.

## Response Format:
Respond with an XML block structured as follows:

<answer>
  <step>
    <rule>1</rule>
    <program_state>
      <n>0</n>
      <sum>0</sum>
    </program_state>
  </step>
  <step>
    <rule>2</rule>
    <program_state>
      <n>100</n>
      <sum>0</sum>
    </program_state>
  </step>
...
</answer>

## Here is an example:

Here is the {language} program:
int i;
int j;
i {ASSIGN_OP} 0;
{WHILE} (i {LT_OP} 2)
{{
      {HALT};
}};


## Expected output:

<answer>
  <step>
    <rule>36</rule>
    <program_state>
      <i>0</i>
    </program_state>
  </step>
  <step>
    <rule>36</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>21</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>24</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>25</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>1</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>



                                                      29
                            LLMs Lean on Priors, Not Programming Language Semantics

  <step>
    <rule>12</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>22</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
  <step>
    <rule>26</rule>
    <program_state>
      <i>0</i>
      <j>0</j>
    </program_state>
  </step>
</answer>


## Notes:
- Each ’<step>’ must correspond to **exactly one K-semantics re-write rule** that is needed to evaluate a
statement in the given program.
- Only rules that have names indicated in ’[]’ adjacent to it must be reported in the answer.
- The ’<rule>’ must indicate a rule used in the evaluation of a statement.
- The ’<program_state>’ must represent the **entire program state immediately after** the execution of that rule.
- The program state must list **all variables currently in scope**, using the variable names as XML tags and
their current values as tag content.
- Include variables even if they did not change.
- Do not skip any step or merge multiple steps into one.
- Do not skip any rules (including those used to reduce expressions and variables) that are needed to evaluate
the program.


Non-CoT: Only output the ‘<answer>’ XML block. Do not include explanations, comments, or any other text.
CoT: Explain your reasoning step-by-step **before** answering. Wrap your reasoning in ’<reason>’ tags. Note
that you **MUST** wrap your reasoning steps with ’<reason>’ tags, the prediction with ’<answer>’ tags.




                                                       30
                                  LLMs Lean on Priors, Not Programming Language Semantics

F. Is Keyword Obfuscation a Tokenization Artifact?
A potential concern with the KeywordObf seman- Table 11. PredState accuracy under KeywordObf with different symbol
tic shift is that it introduces rare Unicode characters inventories. We compare the original Caucasian-Albanian symbol substitution
(e.g., from Caucasian-Albanian script) that may against a tokenization-controlled variant (1T OK) in which every keyword
                                                        is replaced by a symbol verified to occupy a single GPT-4o-mini token.
be split into many subword tokens, artificially inflat- Accuracy remains low in both settings, indicating that failures are not driven
ing prompt length and degrading model performance. by token inflation.
If so, the observed failures would primarily reflect Semantics Variant                        Model                   Accuracy(%)
tokenizer limitations rather than deficiencies in rule-
conditioned reasoning.                                                                        GPT-4o-mini                        8.4
                                                                       Caucasian-Albanian
                                                                                                GPT-4o-mini-CoT                21.8
                                                                S
To isolate this factor, we perform a controlled ab-                                             GPT-4o-mini                     7.0
lation that preserves the semantic transformation of                     1Tok
                                                                                                GPT-4o-mini-CoT                19.3
KeywordObf while removing tokenization effects.                                                 GPT-4o-mini                     8.2
                                                                         Caucasian-Albanian
                                                                                                GPT-4o-mini-CoT                18.1
F.1. Tokenizer-Controlled Symbol Substitution                  K
                                                                                                GPT-4o-mini                     6.2
                                                                         1Tok
We construct a variant, 1Tok, in which every keyword                                  GPT-4o-mini-CoT           16.9
and operator is replaced with a symbol verified to be
encoded as a single token by GPT-4o-mini tokenizer.
This shift maintains the same distribution shift—models must map novel surface forms to formal rules—while preventing
input-length inflation from multi-byte Unicode characters.

F.2. Experimental Setup
We rerun the PredState task on the Human-Written split under KeywordObf semantics for both S and K based formalizations,
comparing the original Caucasian-Albanian symbol substitution to the new 1-token variant. All prompts, rules, and evaluation
procedures match those in §5.1; only the symbol inventory changes.

F.3. Results
Table 11 reports the results. Replacing multi-token Unicode symbols with guaranteed single-token alternatives yields only
modest changes in accuracy.
Under S, GPT-4o-mini decreases slightly from 8.4% to 7.0%, and GPT-4o-mini-CoT from 21.8% to 19.3%. A similar pattern
holds for K, where GPT-4o-mini drops from 8.2% to 6.2% and GPT-4o-mini-CoT from 18.1% to 16.9%.
Crucially, in all cases performance remains far below that observed under standard semantic formalization, and the qualitative
failure pattern under KeywordObf is unchanged.

F.4. Implications
These results rule out tokenization inefficiency as the primary driver of degraded performance under KeywordObf. Even
when all obfuscated symbols are atomic tokens, models still fail to reliably apply the correct operational rules and compose
them over execution.
We therefore conclude that KeywordObf probes limitations in rule-conditioned reasoning over unfamiliar formal systems,
rather than lexical or tokenizer artifacts.




                                                                    31
                                     LLMs Lean on Priors, Not Programming Language Semantics

G. Task Extended Analysis
G.1. Formal Semantics Notation Comprehension
Table 12. Hierarchical organization of S semantics rules into families and constructs, with associated categories and semantic roles, used
to sample near-miss distractors for the formal-semantics notation comprehension tasks.
                 Family     Construct                    Rules   Category    Semantic Role

                 A. Variable & State Access
                 F1         Variable lookup               1–2     AEXP       Read σ(x); distinguishes value vs unbound-variable error
                 B. Declarations & Assignment
                 F2          Declaration                   3       SL        Initialize state via σ[x 7→ 0]
                 F3          Assignment                   4–6      SL        Step RHS vs commit update; uninitialized-assignment error
                 C. Arithmetic Expressions (Binary)
                 F4        Addition                       7–9     AEXP       Left-step / right-step / compute for binary +
                 F5        Subtraction                   10–12    AEXP       Left-step / right-step / compute for binary −
                 F6        Multiplication                13–15    AEXP       Left-step / right-step / compute for binary ×
                 F7        Division                      16–19    AEXP       Nonzero vs div-by-zero error case
                 F8        Modulo                        20–23    AEXP       Nonzero vs mod-by-zero error case
                 D. Arithmetic Expressions (Unary)
                 F9        Unary minus                   24–25    AEXP       Step argument vs compute negation
                 F10       Unary plus                    26–27    AEXP       Step argument vs compute identity
                 E. Relational Comparisons
                 F11        Less-than                    28–31    BEXP       Step operands; compute boolean (true/false) for <
                 F12        Less-or-equal                32–35    BEXP       Step operands; compute boolean (true/false) for ≤
                 F13        Greater-than                 36–39    BEXP       Step operands; compute boolean (true/false) for >
                 F14        Greater-or-equal             40–43    BEXP       Step operands; compute boolean (true/false) for ≥
                 F15        Equality                     44–47    BEXP       Step operands; compute boolean (true/false) for =
                 F16        Inequality                   48–51    BEXP       Step operands; compute boolean (true/false) for ̸=
                 F. Boolean Connectives
                 F17        Boolean AND                  52–55    BEXP       Step operands; compute conjunction
                 F18        Boolean OR                   56–59    BEXP       Step operands; compute disjunction
                 F19        Boolean NOT                  60–62    BEXP       Step operand; compute negation
                 G. Sequencing & Statement Plumbing
                 F20        Sequencing / head stepping    63       SL        Lift a head-statement step into the statement list
                 H. Conditional Control Flow
                 F21        If–then–else                 64–66    CTRL       Step condition; branch via list splicing
                 I. Loops & Loop Context
                 F22        While entry                    67     CTRL       Desugar WHILE; push loop frame onto χ
                 F23        Loop execution               68–70    CTRL       Exit on false (pop χ); iterate on true (insert LE)
                 F24        Loop-exit marker (LE)          77     CTRL       Restore continuation via top(χ)
                 J. Non-local Control Flow
                 F25         Break                       71–73    CTRL       Propagate to LE; handle at LE; error if χ = ϵ
                 F26         Continue                    74–76    CTRL       Propagate to LE; resume loop; error if χ = ϵ
                 K. Termination
                 F27       Halt                           78      CTRL       Terminal configuration; stops execution


This section provides the full details of the hierarchical distractor sampling strategy and the rule-family coverage distributions
referenced in § 4.
Hierarchical rule organization. Tables 12 and 13 list every semantic rule used in our NL → Rule and Rule → NL evaluation
tasks for S and K respectively. Rules are organized into 27 families (F1–F27), grouped under 11 top-level categories (A–K).
Each family corresponds to a single language construct (e.g., addition, while-entry) and may contain multiple rules that
differ in their semantic role (e.g., left-step vs. right-step vs. compute for a binary arithmetic operator under S). K rules are at
a coarser granularity: because K is a big-step semantics, many of the intermediate reduction steps present under S (e.g.,
left-step and right-step rules for binary operators) are collapsed into a single rule, yielding fewer rules per family.
Distractor sampling strategy. When constructing each multiple-choice sample (five choices), we draw distractors in a
hierarchical order designed to maximize semantic proximity to the correct answer:
1. Same family, different semantic role. We first attempt to sample distractors from the same family as the correct rule.
   These share the same language construct but differ in semantic role (e.g., the compute rule vs. a step rule for addition),
   making them the hardest distractors.

                                                                        32
                                     LLMs Lean on Priors, Not Programming Language Semantics

Table 13. Hierarchical organization of K semantics rules into families and constructs, with associated categories and semantic roles, used
to sample near-miss distractors for the formal-semantics notation comprehension tasks.
          Family     Construct          Rules    Category   Semantic Role

          A. Variable & State Access
          F1          Variable lookup     1–2     AEXP      Read state binding; distinguishes value retrieval vs unbound-variable error (halts).
          B. Declarations & Assignment
          F2          Declaration          36      SL       Initialize state (introduce variable with default value 0).
          F3          Assignment           21      SL       Commit update to state once RHS is a value (update existing variable).
          C. Arithmetic Expressions (Binary)
          F4          Addition              3     AEXP      Compute binary + when both operands are values.
          F5          Subtraction           4     AEXP      Compute binary − when both operands are values.
          F6          Multiplication        5     AEXP      Compute binary × when both operands are values.
          F7          Division            6–7     AEXP      Case split: nonzero divisor computes division; zero divisor raises error (halts).
          F8          Modulo              8–9     AEXP      Case split: nonzero divisor computes modulus; zero divisor raises error (halts).
          D. Arithmetic Expressions (Unary)
          F9          Unary minus          11     AEXP      Compute unary negation once operand is a value.
          F10         Unary plus           10     AEXP      Compute unary identity (operationalized as adding 0) once operand is a value.
          E. Relational Comparisons
          F11         Less-than            12     BEXP      Compute boolean result for < on value operands.
          F12         Less-or-equal        13     BEXP      Compute boolean result for <= on value operands.
          F13         Greater-than         14     BEXP      Compute boolean result for > on value operands.
          F14         Greater-or-equal     15     BEXP      Compute boolean result for >= on value operands.
          F15         Equality             16     BEXP      Compute boolean result for == on value operands.
          F16         Inequality           17     BEXP      Compute boolean result for != on value operands.
          F. Boolean Connectives
          F17         Boolean AND          19     BEXP      Compute conjunction on boolean operands.
          F18         Boolean OR           20     BEXP      Compute disjunction on boolean operands.
          F19         Boolean NOT          18     BEXP      Compute negation on boolean operand.
          H. Conditional Control Flow
          F21         If–then–else       22–23    CTRL      Branch on boolean predicate.
          I. Loops & Loop Context
          F22         While entry          24     CTRL      Push loop statement onto stack; rewrite to internal form; insert markers.
          F23         Loop execution       25     CTRL      Desugar internal while into if–else: iterate on true, exit on false.
          F24         Loop markers       27–28    CTRL      Marker plumbing: remove loop markers when encountered to resume execution.
          J. Non-local Control Flow
          F25         Break              33–35    CTRL      Handle break statements
          F26         Continue           29–32    CTRL      Handle continue statements
          K. Termination
          F27         Halt                 26     CTRL      Terminal configuration: stops execution immediately; removes remaining computation.


2. Same category, different construct. If the family does not contain enough candidate rules, we sample from other
   families within the same top-level category (e.g., another binary arithmetic operator from category C).

3. Different category. As a last resort, distractors are drawn from a different category entirely (e.g., a control-flow rule
   used as a distractor for an arithmetic-expression question).
This ordering ensures that each question is discriminative: models must distinguish among rules that govern closely related
constructs rather than exploit superficial differences in operator type or syntactic category.

G.2. Final-State Prediction (PredState)
This section analyzes (1) the impact of code-complexity metrics on LLM performance in the PredState task, and (2) the
average percentage of variables per program whose final states are predicted correctly.

G.2.1. I MPACT OF C ODE -C OMPLEXITY M ETRICS
Figure 8a illustrates the workflow of the PredState task. An C⋆ program, together with optional semantics (K-semantics or
S) and syntax, is used both to construct prompts for the LLMs and to obtain gold final states by executing the program in the
K-framework. The LLM’s predicted final states are then compared with the gold states for each declared variable. A match
is recorded as 1 (pass), and a mismatch as 0 (fail).
Different LLMs naturally excel on different C⋆ programs. To understand why an LLM may predict all final states correctly
for one program but fail on another, we cast this task as a classification problem as shown in Figure 8b. Each C⋆ program is
mapped to a predictor vector that characterizes its complexity, using the code-complexity metrics introduced earlier. Each
predictor is then normalized using z-score normalization to ensure fair contribution from all the variables. The resulting

                                                                        33
                                     LLMs Lean on Priors, Not Programming Language Semantics




(a) Workflow of the PredState task. C⋆ programs, along with optional semantics (K-semantics or S) and syntax, are: (1) executed in the
K-framework to obtain the gold final states of all declared variables, and (2) used to construct a prompt for the LLMs to predict those final
states. The gold and predicted states are then compared, scored as 1 for a match and 0 otherwise, and accumulated into a result vector.




(b) Modeling LLM performance on C⋆ programs. We treat each LLM as a black box and apply Elastic Net regression using code-
complexity metrics as predictors. Partial Least Squares (PLS) is employed for dimensionality reduction and to address multicollinearity.
The magnitude and sign of the regression weights provide insight into the potential impact of each metric on the classifier’s performance
and hence to an extent the LLM’s performance.
           Figure 8. Analyzing the impact of different code-complexity metrics on LLM performance in the PredState task.

predictor matrix, together with the LLM’s binary result vector of passes and fails, is then used to train a classifier.
Table 14. Odds ratio per interquartile range (Θ(∆)) for each code-complexity metric for the PredState task without semantics. Θ(∆)
for a metric is the odds ratio for a correct final-state prediction when that metric increases from its 25th to its 75th percentile, holding other
metrics fixed. Reported only for models with <90% accuracy on the PredState task (Table 4, left panel) to mitigate class imbalance. The
largest absolute values in each row are shown in boldface font.
                                                        Control-flow                Data-flow                     Size
                        Models
                                                  ΩCC      Ω̂If   Ω̂Loop      ΩDD        Ω̂Assign   ΩLoc   ΩVol      ΩVoc      Ω̂Trace
                                                                   Human-Written
                        L LAMA-3.3 70B            -19       -5         -29        -17      -2       -16    -22           -25     -1
                        L LAMA-3.3 70B-CoT        -21      -14         -28        -16      -2       -17    -19           -20     -1
                        Q WEN2.5-I NST 14B        -17       -5         -27        -16      -2       -14    -20           -25     -1
                        Q WEN2.5-I NST 14B-CoT    -25      -18         -27        -15      -3       -20    -21           -20     -2
                        Q WEN2.5-I NST 32B        -12      -11         -12         -9      -1       -12    -14           -17     -1
                        Q WEN2.5-I NST 32B-CoT    -23       -7         -33        -17      -4       -19    -21           -20     -2
                        GPT-4o-mini               -18       -7         -30        -16      -2       -13    -18           -22     -1
                        GPT-4o-mini-CoT           -15       -2         -28        -14      -2       -11    -15           -16     -1
                        DS-Q WEN 14B              -13      -10         -16         -9      -2       -11    -13           -10     -1
                        DS-L LAMA 70B             -14       -5         -22        -12      -3       -11    -14           -10     -2
                                                                   LLM-Translated
                        Q W Q 32B                  -1       -5         5          -20      -4       -13    -20           -7      -4
                                                                  Fuzzer-Generated
                        Q W Q 32B                 -25      -25         -25        -14      -33      -25    -24           -28    -31
                        GPT-5-mini                -21      -14         -19        -12      -27      -20    -20           -21    -27
                        G EMINI-2.5-pro            -6       -5          -8         -5      -12       -6     -6            -5    -12


Because these complexity metrics are often highly correlated (multicollinearity), we apply Partial Least Squares (PLS) (Wold
et al., 2001) for dimensionality reduction. Unlike the unsupervised Principal Component Analysis (PCA) (Wold et al., 1987),
which identifies linear combinations of predictors that maximize variance, PLS is supervised: it reduces dimensionality by
finding components that maximize the covariance between predictors and the response variables (the result vector). This
makes PLS more suitable in our setting, as it better mitigates multicollinearity while preserving predictive power.
We next apply Elastic Net regression (Zou & Hastie, 2005) on the PLS-transformed predictors and the result vector to train
a classifier. In regression, each predictor is assigned a coefficient whose magnitude reflects its relative importance and
whose sign indicates whether it contributes positively or negatively to prediction accuracy. Elastic Net is chosen because

                                                                             34
                                     LLMs Lean on Priors, Not Programming Language Semantics

Table 15. Odds ratio per interquartile range (Θ(∆)) for each code-complexity metric for the PredState task with the standard C⋆
semantics (K-semantics and S). Θ(∆) for a metric is the odds ratio for a correct final-state prediction when that metric increases from
its 25th to its 75th percentile, holding other metrics fixed. Reported only for models with <90% accuracy on the PredState task (Table 4,
left panel) to mitigate class imbalance. The largest absolute values in each row are shown in boldface font.
                                                         Control-flow                Data-flow                      Size
                         Models
                                                   ΩCC      Ω̂If     Ω̂Loop       ΩDD     Ω̂Assign   ΩLoc   ΩVol       ΩVoc      Ω̂Trace
                                                                   Human-Written
                         L LAMA-3.3 70B            -25       -4         -35        -19      -2       -20     -25           -29     -1
                         L LAMA-3.3 70B-CoT        -27      -10         -33        -20      -3       -24     -26           -25     -2
                         Q WEN2.5-I NST 14B        -24       0          -39        -22      -2       -19     -26           -28     -1
                         Q WEN2.5-I NST 14B-CoT    -25       -8         -35        -16      -3       -20     -22           -22     -2
                         Q WEN2.5-I NST 32B        -23       -7         -35        -19      -2       -19     -25           -30     -1
                     K




                         Q WEN2.5-I NST 32B-CoT    -21      -15         -27        -12      -3       -16     -17           -16     -2
                         GPT-4o-mini               -24      -14         -32        -21      -2       -22     -27           -30     -1
                         GPT-4o-mini-CoT           -21      -14         -26        -15      -3       -18     -20           -19     -2
                         DS-Q WEN 14B              -29      -21         -27        -20      -3       -26     -27           -23     -2
                         DS-L LAMA 70B             -26      -14         -33        -14      -5       -19     -19           -15     -3
                         L LAMA-3.3 70B            -24       0          -40        -21      -2       -18     -26           -32     -1
                         L LAMA-3.3 70B-CoT        -21      -11         -32        -16      -4       -18     -20           -21     -2
                         Q WEN2.5-I NST 14B        -19       2          -39        -19      -2       -13     -21           -25     -1
                         Q WEN2.5-I NST 14B-CoT    -26      -17         -25        -16      -3       -22     -22           -20     -2
                         Q WEN2.5-I NST 32B        -19       -9         -28        -16      -1       -17     -21           -27     -1
                     S




                         Q WEN2.5-I NST 32B-CoT    -19      -14         -22        -12      -2       -17     -17           -18     -1
                         GPT-4o-mini               -19        4         -37        -19      -2       -16     -23           -29     -1
                         GPT-4o-mini-CoT           -15       -9         -14         -7      -2       -12     -12           -12     -1
                         DS-Q WEN 14B              -11       -4         -14         -9      -1       -10     -12            -9     -1
                         DS-L LAMA 70B             -23      -12         -32        -14      -5       -18     -21           -18     -3
                                                                   LLM-Translated
                         Q W Q 32B                 -11       -6         7          -22       0       -24                   -8      0
                     K




                                                                                                             -27
                         Q W Q 32B                 -14       -9         -6         -28      -4       -18     -20           -1      -4
                     S




                                                                   Fuzzer-Generated
                         Q W Q 32B                 -21      -27         -25        -10      -30      -20     -20           -23    -29
                         GPT-5-mini                -23      -20         -21        -13               -22     -22           -23    -30
                     K




                                                                                            -31
                         G EMINI-2.5-pro           -14      -10         -14         -8      -21      -13     -13           -14    -21
                         Q W Q 32B                 -22      -23         -24        -11      -31      -22     -21           -25    -30
                         GPT-5-mini                -22      -19         -21        -11               -21     -21           -22    -28
                     S




                                                                                            -29
                         G EMINI-2.5-pro            -7      -20         -24         -3      -25       -7      -7            -7    -26




it combines Lasso (Tibshirani, 1996) and Ridge (Hoerl & Kennard, 1970) regularization: the Lasso component drives
irrelevant coefficients to zero, enabling feature selection, while the Ridge component shrinks correlated coefficients, thereby
mitigating multicollinearity.
We now briefly describe the Elastic Net regression process to explain how we use the regression coefficients to determine the
impact of different metrics. Let n, p, y, and X be the total number of samples, the total number of predictors, the response
vector, and the predictor matrix (we will use boldface font to denote vectors and matrices) respectively. Then,

                                                                                                                1
                           y ∈ Rn ,        yi ∈ {0, 1},     xi ∈ Rp ,             pi (yi = 1|xi ) =                ⊤
                                                                                                       1 + e−(β0 +xi β)
Where pi (yi = 1|xi ) along with pi (yi = 0|xi ) = (1 − pi (yi = 1|xi )) represent the class-conditional probabilities and β is
the vector of coefficients. The Elastic Net objective function for a Negative Log-Likelihood loss is given as (Friedman et al.,
2010):

                                    n h
                                 h1 X                                                 p h
                                                                                i    X    1−α 2          ii
                    arg min                 − yi log pi − (1 − yi ) log(1 − pi ) + λ         βj + α|βj |
                         β0 ,β    n i=1                                              j=1
                                                                                           2
                                                                                     |       {z          }
                                                                                                      Ridge and Lasso penalties

Let β̂ be the coefficient vector that minimizes this objective function. Then the percentage odds ratio (Agresti, 2013;
Cornfield, 1951; Harrell, 2015) Θ for the inter-quartile-range ∆j of the j th predictor can be computed as:

                                                                             35
                                    LLMs Lean on Priors, Not Programming Language Semantics


                                                                                
                                                    Θ(∆j ) = 100 × exp β̂j ∆j − 1 .
The percentage odds ratio per inter-quartile-range Θ(∆) gives the percentage change in the odds of the classifier’s positive
outcome (predicting a 1) for the predictor ranging from its typical low value (25th percentile) to its typical high value (75th
percentile) in the dataset when all other predictors are held constant. Thus if Θ(∆j ) for the j th predictor is -37%, this
implies that one quartile increase in the j th predictor lowers the odds of the classifier’s positive outcome by 37%.
To quantify each metric’s effect on accuracy, we report the odds-ratio per interquartile range, Θ(∆), in Tables 14-15 for all
LLMs without and with (K-semantics, S) semantics. Overall patterns are similar across settings. On the Human-Written
dataset, ΩLoop —the maximum executed loop-nesting depth—is the most influential predictor: larger ΩLoop is associated with
lower odds of a correct final-state prediction. On the LLM-Translated dataset, ΩDD (data-flow complexity) and ΩVol (size)
dominate without semantics; with semantics, ΩDD remains dominant under S, whereas ΩVol dominates under K-semantics.
On the Fuzzer-Generated split, Ω̂Assign (total variable assignments) is the strongest predictor both without and with semantics,
with one exception: for G EMINI-2.5-pro under S, Ω̂Trace (execution-trace length) is most predictive. Collectively, these Θ(∆)
trends suggest that increasing control-flow depth harms models on human code, whereas data-flow/size factors are more
limiting on translated or fuzzer generated code.

G.2.2. C OMPLEXITY-M ETRIC I MPACT PATTERNS
                                                             Cluster 1: Vocabulary (d=-2.63)             Cluster 3: Volume (d=2.62)
                                                                        DepDegree (d=-1.63)                         CC (d=2.31)
                                                             Cluster 2: TraceLength (d=-2.97)
                                                                        NumAssignments (d=-2.75)
                                  DeepSeek-Qwen 14B
                                 GPT-4o-mini-CoT - SOS
                            DeepSeek-Qwen 14B - SOS
                                  Qwen2.5-Instruct 32B
                        Qwen2.5-Instruct 32B-CoT - SOS
                                  DeepSeek-Llama 70B
                                        GPT-4o-mini-CoT
                                     Llama-3.3 70B-CoT
                          Qwen2.5-Instruct 14B-CoT - K
                                 Llama-3.3 70B-CoT - K
                              DeepSeek-Llama 70B - K
                           DeepSeek-Llama 70B - SOS
                              Llama-3.3 70B-CoT - SOS
                             Qwen2.5-Instruct 32B-CoT
                             Qwen2.5-Instruct 14B-CoT
                        Qwen2.5-Instruct 14B-CoT - SOS
                               DeepSeek-Qwen 14B - K
                                    GPT-4o-mini-CoT - K
                          Qwen2.5-Instruct 32B-CoT - K
                              Qwen2.5-Instruct 14B - K
                                   Llama-3.3 70B - SOS
                              Qwen2.5-Instruct 32B - K
                                      Llama-3.3 70B - K
                                      GPT-4o-mini - SOS
                           Qwen2.5-Instruct 14B - SOS
                                         GPT-4o-mini - K
                                          Llama-3.3 70B
                           Qwen2.5-Instruct 32B - SOS
                                             GPT-4o-mini
                                  Qwen2.5-Instruct 14B
                                                       0.0     0.2      0.4       0.6      0.8     1.0        1.2      1.4       1.6
                                                                                  Cosine Distance
Figure 9. Dendrogram of models for the PredState task on the Human-Written dataset under no-semantics and standard semantics
(K-semantics and S). We show the top two most distinguishable metrics per cluster, identified using the Cohen’s d one-vs-rest test. The
silhouette score is 0.58 thus indicating a good clustering structure.

To identify if there is a pattern to how models perform on increasing different code-complexity metrics, we perform
hierarchical clustering on the standardized regression coefficients (β̂SD ) of the metrics for the models on the Human-Written
dataset. We perform this for the no-semantics and with standard semantics (K-semantics and S) cases. We use the cosine-
distance as the pair-wise distance metric and the Cohen’s d one-vs-rest test to identify the most distinguishing metric of each
cluster. Figure 9 shows the dendrogram of the clustering process.
We see that there are three clusters. All the non-reasoning models without CoT prompting are in Cluster 1 with the exception
of Q WEN2.5-I NST 32B (under no-semantics case). Cluster 1 responds more negatively to increases in the complexity metrics
Vocabulary (ΩVoc ) and DepDegree (ΩDD ) relative to the other two clusters. Cluster 2 contains only the reasoning models and
the non-reasoning models with CoT prompting. It predominantly contains models under the K-semantics and responds more
negatively to the dynamically computed metrics, TraceLength (Ω̂Trace ) and NumAssignments (Ω̂Assign ) relative to the rest of
the clusters. The last cluster, Cluster 3 also only contains reasoning models and non-reasoning models with CoT prompting
(Q WEN2.5-I NST 32B is an exception). It predominantly contains models under S semantics and responds positively to

                                                                          36
                                           LLMs Lean on Priors, Not Programming Language Semantics

increases in the metrics, Volume (ΩVol ) and cyclomatic-code complexity (ΩCC ) relative to the rest.

G.2.3. AVERAGE P ERCENTAGE OF VARIABLES P REDICTED C ORRECTLY
                 Table 16. Average percentage of variables predicted correctly per program on the PredState task.

                                      Models
                                                                                     K-Formalization                      S-Formalization
                                                                 Accna     Accstd         Accswap      Accobf      Accstd    Accswap    Accobf
                                                                          Human-Written
                                      Q WEN2.5-I NST 14B           70          67           37          53          67          33          50
                                      Q WEN2.5-I NST 14B-CoT       85          83           36          75          82          35          63
                      Non-reasoning



                                      Q WEN2.5-I NST 32B           77          69           32          53          71          32          55
                                      Q WEN2.5-I NST 32B-CoT       90          89           39          78          84          33          65
                                      L LAMA-3.3 70B               70          66           38          52          64          34          52
                                      L LAMA-3.3 70B-CoT           87          86           33          78          86          28          66
                                      GPT-4o-mini                  67          64           38          47          61          38          41
                                      GPT-4o-mini-CoT              75          89           30          62          82          31          54
                                      DS-Q WEN 14B                 66           83          27          53           60         20          43
                                      DS-Q WEN 32B                 85           97          45          85           98         36          88
                      Reasoning




                                      DS-L LAMA 70B               81            92          33          73           90         34           65
                                      Q W Q 32B                   94            99          82          91          100         38          92
                                      O 3-mini                    95           100          59          92          100         74           98
                                      GPT-5-mini                  100          100          86          97          100         85          99
                                      G EMINI-2.5-pro              93          100          98          97          100         99          100
                                                                          LLM-Translated
                                      Q W Q 32B                    90          96           66          86          95          45          87
                                      GPT-5-mini                   98          98           88          96          98          81          97
                                      G EMINI-2.5-pro              96          98           95          96          98          96          97
                                                                         Fuzzer-Generated
                                      Q W Q 32B                    65          70            7          22          69           0          17
                                      GPT-5-mini                   91          82           22          33          84          33          34
                                      G EMINI-2.5-pro              96          94           53          85          95          71          82


We also computed on average (over the total number of declared variables per C⋆ program followed by over the total
number of C⋆ programs) how many of the final-states of the declared variables per C⋆ program that are assigned to at
least once are being predicted correctly by the models. The results are shown in Table 16. We see that the trend in terms
of models performing better without semantics than with semantics is similar to what is observed in the PredState task
(Table 4, left panel). We also see that although models perform very poorly on the increasingly complex datasets such as
the Fuzzer-Generated dataset on the PredState task, the average percentage of the final-states of the variables predicted
correctly per program is quite high.

G.2.4. S TANDARD D EVIATION OF TASK ACCURACY
                                      Table 17. Standard deviation of the accuracy metrics for the PredState task.
                                                                         K-Formalization                     S-Formalization
                                                               Accna Accstd Accswap Accobf              Accstd Accswap Accobf

                                            Human-Written
                                            DS-Q WEN 14B         2.3     2.0          0.3        1.7         1.8      0.0      2.5
                                            DS-Q WEN 32B         1.2     2.3          5.2        0.5         1.2      0.3      1.5
                                            DS-L LAMA 70B        0.0     0.0          0.2        0.0         0.6      0.0      1.3
                                            Q W Q 32B            0.2     0.3          0.0        0.8         0.3      1.5      2.0
                                            O 3-mini             1.2     0.0          1.4        0.6         0.0      1.8      0.3
                                            GPT-5-mini           0.0     0.5          2.6        0.3         0.3      0.8      0.0
                                            G EMINI-2.5-pro      2.0     0.3          0.0        0.9         0.5      1.0      0.3
                                            LLM-Translated
                                            Q W Q 32B            1.8     1.5          1.7        1.7         1.5      0.3      3.6
                                            GPT-5-mini           1.0     1.3          2.0        0.8         0.3      0.8      0.3
                                            G EMINI-2.5-pro      1.5     0.3          1.6        0.3         1.0      2.0      1.5
                                            Fuzzer-Generated
                                            Q W Q 32B            1.5     0.5          0.3        0.3         0.5      0.0      0.8
                                            GPT-5-mini           0.9     1.0          1.1        1.2         1.0      1.7      0.8
                                            G EMINI-2.5-pro      0.6     2.0          2.5        1.5         2.0      2.5      1.5


We average results over three independent runs for reasoning models and report the standard deviation of accuracy in
Table 17. Across all model-dataset-semantic-variant combinations, the standard deviation never exceeds 5.2 percentage
points and is typically below 2.0, confirming that the accuracy differences we report under semantic shifts and across
code-complexity splits are well above run-to-run variability.

                                                                                     37
                                   LLMs Lean on Priors, Not Programming Language Semantics

G.3. Semantic-Rule Prediction (PredRule)
In this section, we discuss: (1) how the statements sampled from C⋆ programs are processed for the PredRule task, and
(2) identify the most mispredicted rule (first-point-of-mismatch) categories in the PredRule task.

G.3.1. P ROCESSING C⋆ S TATEMENTS FOR P RED RULE
Table 18. Processing of statements sampled from C⋆ programs for the PredRule task. The pair <Statement, State> is transformed into the
pair <PredRule Program, PredRule State>. The transformed pair is used in constructing the prompt for the PredRule task.
               Type          Statement               State   PredRule Program                            PredRule State
               Declaration                             σ                                                       σ
                             int <VAR>;                      int <VAR>;
               Assignment                              σ                                                       σ
                             <VAR> = <EXP>;                  <VAR> = <EXP>;
               While                                   σ                                                       σ
                             while(<PREDICATE>)              while(<PREDICATE>)
                             {                               {
                                <BODY>                            - <BODY>
                             };
                                                                  + halt;
                                                             };
               If-else                                 σ                                                       σ
                             if(<PREDICATE>)                 if(<PREDICATE>)
                             {                               {
                                <BODY>                            - <BODY>
                             }
                             else                               + halt;
                             {                               }
                                <BODY>                       else
                             };                              {
                                                                  - <BODY>
                                                                  + halt;
                                                             };
               Halt                                    σ                                                       σ
                             halt;                           halt;
               Break                                   σ                                                       σ
                             while(<PREDICATE>)              while(<PREDICATE>)
                             {                               {
                                ...                             - ...
                                break;                          break;
                                ...                             ...
                             };                              };


The objective of the PredRule task is to challenge LLMs with predicting the ordered sequence of semantic rules that is
required to evaluate an C⋆ statement when the program state before the execution of that statement is given. Ideally, we
want to avoid requiring the LLMs from needing to track program state since that capability is specifically tested for in the
PredTrace task, and we want to avoid any overlaps/redundancies. This is trivial for statements that are self-contained, such
as declaration, assignment, and halt. However statements such as while, if-else, break, require some
processing to make them suitable for this task.
Table 18 shows how each type of statement is processed to make it suitable for the PredRule task. The primary objective
behind processing is to make edits to the sampled statements such that they can be completely evaluated by requiring the
least amount of program state updates. The first, second, and third columns lists the type of the sampled statement, its
minimal representative skeleton, and the program state captured before its evaluation respectively. The fourth and the fifth
columns list the sampled statement after processing and the corresponding processed program state which can now be
used in the PredRule task. For the sampled declaration, assignment, and halt statements, the statements and
the collected program state before their executions are used as is in the PredRule task because their evaluation does not
require tracking program state nor do they require the execution of other statements. For while statements, we replace the
body with a halt statement. This removes any possibility of needing state updates to correctly and completely evaluate
the while statement. A similar approach is used for processing the if-else statement. For the break statement, we
capture its closest enclosing loop and remove all statements from its body up until the break statement.
Since the PredRule task is scoped to a statement level of granularity, it is relatively agnostic to the complexity of the
program as a whole.

G.3.2. M OST M ISPREDICTED RULES

                                                                  38
                                              LLMs Lean on Priors, Not Programming Language Semantics



              o3-mini QwQ 32B DeepSeek
                               QwenDeepSeek
                                    32B                             o3-mini QwQ 32B DeepSeek
                                                                                     QwenDeepSeek
                                                                                          32B                                  o3-mini QwQ 32B DeepSeek
                                                                                                                                                QwenDeepSeek
                                                                                                                                                     32B
    GPT-4o-mini       0.8                                 GPT-4o-mini       0.8                                      GPT-4o-mini       0.8
                       0.6         Qwen 14B                                  0.6         Qwen 14B                                       0.6         Qwen 14B
  GPT-4o-mini           0.4           DeepSeek          GPT-4o-mini           0.4           DeepSeek               GPT-4o-mini           0.4           DeepSeek
         CoT             0.2          Llama 70B                CoT             0.2          Llama 70B                     CoT             0.2          Llama 70B
  GPT-5-mini                           Llama-3.3 70B    GPT-5-mini                           Llama-3.3 70B         GPT-5-mini                           Llama-3.3 70B
                                       CoT                                                   CoT                                                        CoT
    Gemini-2.5                       Llama-3.3 70B        Gemini-2.5                       Llama-3.3 70B             Gemini-2.5                       Llama-3.3 70B
           pro                                                   pro                                                        pro
     Qwen2.5-Inst                Qwen2.5-Inst              Qwen2.5-Inst                Qwen2.5-Inst                   Qwen2.5-Inst                Qwen2.5-Inst
               14B               32B CoT                             14B               32B CoT                                  14B               32B CoT
          Qwen2.5-Inst       Qwen2.5-Inst                       Qwen2.5-Inst       Qwen2.5-Inst                            Qwen2.5-Inst       Qwen2.5-Inst
                14B CoT      32B                                      14B CoT      32B                                           14B CoT      32B
         (a) Standard semantics.                           (b) KeywordSwap semantics.                                  (c) KeywordObf semantics.
              o3-mini QwQ 32B DeepSeek
                               QwenDeepSeek
                                    32B                             o3-mini QwQ 32B DeepSeek
                                                                                     QwenDeepSeek
                                                                                          32B                                  o3-mini QwQ 32B DeepSeek
                                                                                                                                                QwenDeepSeek
                                                                                                                                                     32B
    GPT-4o-mini       0.8                                 GPT-4o-mini       0.8                                      GPT-4o-mini       0.8
                       0.6         Qwen 14B                                  0.6         Qwen 14B                                       0.6         Qwen 14B
  GPT-4o-mini           0.4           DeepSeek          GPT-4o-mini           0.4           DeepSeek               GPT-4o-mini           0.4           DeepSeek
         CoT             0.2          Llama 70B                CoT             0.2          Llama 70B                     CoT             0.2          Llama 70B
  GPT-5-mini                           Llama-3.3 70B    GPT-5-mini                           Llama-3.3 70B         GPT-5-mini                           Llama-3.3 70B
                                       CoT                                                   CoT                                                        CoT
    Gemini-2.5                       Llama-3.3 70B        Gemini-2.5                       Llama-3.3 70B             Gemini-2.5                       Llama-3.3 70B
           pro                                                   pro                                                        pro
     Qwen2.5-Inst                Qwen2.5-Inst              Qwen2.5-Inst                Qwen2.5-Inst                   Qwen2.5-Inst                Qwen2.5-Inst
               14B               32B CoT                             14B               32B CoT                                  14B               32B CoT
          Qwen2.5-Inst       Qwen2.5-Inst                       Qwen2.5-Inst       Qwen2.5-Inst                            Qwen2.5-Inst       Qwen2.5-Inst
                14B CoT      32B                                      14B CoT      32B                                           14B CoT      32B
         (d) Standard semantics.                           (e) KeywordSwap semantics.                                   (f) KeywordObf semantics.
Figure 10. First-point-of-mismatch rate by category for the PredRule task with the K-semantics (top) and S (bottom) on the Human-
Written dataset.
                                                                                                      Table 19. Rule categorization for PredRule analysis.
To identify the semantic rules that models struggle with, we compute
the first-point-of-mismatch rate for each rule, which is the frequency                                  Category             K                  S
of the rule as the first mismatch between ground truth and the model                                    Assignment           Rule 21            Rules 4 - 6
                                                                                                        Arithmetic           Rules 3 - 11       Rules 7 - 27
prediction, relative to its total number of occurrences in the PredRule                                 Relational           Rules 12 - 17      Rules 28 - 51
dataset. We group the rules into the following categories: Assignment,                                  Logical              Rules 18 - 20      Rules 52 - 62
                                                                                                        Declaration          Rule 36            Rule 3
Relational, Declaration, Halt, Conditional, Arithmetic, Logical, Loop,                                  Loop                 Rules 24 - 25      Rules 67 - 70 & Rule 77
Id, and Break & Continue. The mapping between the semantic rules                                        Break & Continue     Rules 27 - 35      Rules 71 - 76
                                                                                                        Halt                 Rule 26            Rule 78
and these categories for the K-semantics and S is shown in Table 19.                                    Id                   Rules 1 - 2        Rules 1 - 2
                                                                                                        Conditional          Rules 22 - 23      Rules 64 - 66
The first-point-of-mismatch rate for a category is the maximum across
all the rules within this category. Figure 10 shows the first-point-of-
mismatch rate across categories for all the models on the Human-Written dataset for the standard and nonstandard semantics,
for both their K-semantics (top) and S (bottom) formalizations.
Firstly, we observe that the models in general mispredict rules to a larger extent for S relative to when provided with the
K-semantics. Furthermore, categories such as Declaration, Id & Literal, and Halt that generally require one or
at most two rules are almost never mispredicted significantly by any model across all the different cases. This is also observed
for the Assignment category under K-semantics which is formalized by just one rule and we see that its misprediction rate
is low across models. In contrast, the Assignment category is heavily mispredicted under S formalization for standard
and nonstandard semantics for a large number of models. We see a similar story with the Logical category where models
mispredict it more significantly under S than K-semantics. The Logical category contains the three logical operators
(AND, OR, and NOT) and we see that exactly three rules are required under K-semantics thus one rule per operator whereas S
requires ten rules, almost 4x more rules per operator than K-semantics. Similar trends are observed in the Relational
category.

H. Use of External Assets
In this work, we make use of several external assets, including datasets, and pretrained models. We acknowledge and credit
the original creators of these assets as follows:

H.1. Data
We construct the Human-Written dataset by rewriting the existing code solutions from the following sources:


  1. HumanEval-X

                                                                                   39
                              LLMs Lean on Priors, Not Programming Language Semantics

     (a) License: Apache 2.0
     (b) URL: https://huggingface.co/datasets/THUDM/humaneval-x
 2. BabelCode MBPP
     (a) License: CC 4.0
     (b) URL: https://huggingface.co/datasets/gabeorlanski/bc-mbpp
 3. CodeContests
     (a) License: CC 4.0
     (b) URL: https://github.com/google-deepmind/code_contests
 4. Leetcode
     (a) We scrape only the ground-truth solutions and public test cases from leetcode. We use the collected problems for
         academic purposes only.
     (b) URL: https://leetcode.com/

We construct the LLM-Translated dataset by using Q WEN2.5-I NST 32B to translate the C++ solutions to problems from:

 1. CodeForces
     (a) License: CC 4.0
     (b) URL: https://huggingface.co/datasets/open-r1/codeforces

H.2. Models
We evaluate LLMs designed for coding tasks and enhanced reasoning ability on our PLS EMANTICS B ENCH:

 1. L LAMA-3.3 70B (Grattafiori et al., 2024),
     (a) License: llama3.3
     (b) URL:
         https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
 2. Qwen2.5-Coder Models (Hui et al., 2024),
     (a) License: Apache 2.0
     (b) URLs:
         https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
         https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct
 3. DeepSeek-R1 distilled models (Guo et al., 2025)
     (a) License: MIT
     (b) URLs:
         https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B
         https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
         https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B
 4. Q W Q 32B (Team, 2025b)
     (a) License: Apache 2.0
     (b) URL: https://huggingface.co/Qwen/QwQ-32B
 5. G EMINI-2.5-pro. In this study, we utilized the G EMINI-2.5-pro model provided by Google AI. The use of this model is
    subject to the Generative AI Preview Terms and Conditions, as outlined in the Google Cloud Service Specific Terms
    for Pre-GA Offerings.
     (a) URL: https://cloud.google.com/terms/service-terms
 6. OpenAI Models. In this study, the use of OpenAI’s models is subject to the term of use.
     (a) URL: https://openai.com/policies/row-terms-of-use/

                                                          40
                               LLMs Lean on Priors, Not Programming Language Semantics

H.3. Icons
We use several icons from https://www.flaticon.com which we attribute here.

     • Document icons created by Roman Káčerek - https://www.flaticon.com/free-icons/document
     • Robot icons created by Kiranshastry - https://www.flaticon.com/free-icons/robot
     • Xml icons created by Dimitry Miroliubov - https://www.flaticon.com/free-icons/xml
     • Diff icons created by brajaomar_j - https://www.flaticon.com/free-icons/diff
     • Matrix icons created by meaicon - https://www.flaticon.com/free-icons/matrix
     • Logistic regression icons created by raidolicon - https://www.flaticon.com/free-icons/logistic-r
       egression
     • Game chart icons created by Arslan Haider - https://www.flaticon.com/free-icons/game-chart
     • Gears icons created by sonnycandra - https://www.flaticon.com/free-icons/gears
     • Message icons created by Freepik - https://www.flaticon.com/free-icons/message

 1    int L;
 2    int p;
 3    int y;
 4    int d;
 5    int K;
 6    int h;
 7    int T;
 8    int Y;
 9    int ble0;
10    int ble1;
11    int ble2;
12    int ble3;
13    int ble4;
14    int ble5;
15    int ble6;
16    int ble7;
17    int ble8;
18    int ble9;
19    int ble10;
20    int ble11;
21    int ble12;
22    int ble13;
23    int ble14;
24    int ble15;
25    int ble16;
26    int ble17;
27    int ble18;
28    int ble19;
29    int ble20;
30    int ble21;
31    int ble22;
32    int ble23;
33    int ble24;
34    int ble25;
35    int ble26;
36    int ble27;
37    int ble28;
38    int ble29;
39    int ble30;
40    int ble31;
41    int ble32;
42    int ble33;
43    int ble34;
44    int ble35;
45    int ble36;
46    int ble37;
47    int ble38;
48    L = (((- y) / 4) - p);
49    T = ((((3 + K) + 1) - 3) + (8 / 8));
50    L = ((((((- p) % 1) * 7) - (- 1)) - (- 9)) - 3);
51    K = (((((d * (- 5)) + y) + (- 5)) - (- K)) - (- 5));


                                                             41
                               LLMs Lean on Priors, Not Programming Language Semantics

 52   Y = (((9 + 3) - T) + 5);
 53   K = ((7 / 7) * L);
 54   y = ((((L + L) + 8) + 3) + 1);
 55   p = ((((- 8) * 9) - ((- 6) % (- 8))) - T);
 56   ble0 = (- 1);
 57   ble1 = (- 1);
 58   ble2 = (- 1);
 59   ble3 = (- 1);
 60   ble4 = (- 1);
 61   ble5 = (- 1);
 62   ble6 = (- 1);
 63   ble7 = (- 1);
 64   ble8 = (- 1);
 65   ble9 = (- 1);
 66   ble10 = (- 1);
 67   ble11 = (- 1);
 68   ble12 = (- 1);
 69   ble13 = (- 1);
 70   ble14 = (- 1);
 71   ble15 = (- 1);
 72   ble16 = (- 1);
 73   ble17 = (- 1);
 74   ble18 = (- 1);
 75   ble19 = (- 1);
 76   ble20 = (- 1);
 77   ble21 = (- 1);
 78   ble22 = (- 1);
 79   ble23 = (- 1);
 80   ble24 = (- 1);
 81   ble25 = (- 1);
 82   ble26 = (- 1);
 83   ble27 = (- 1);
 84   ble28 = (- 1);
 85   ble29 = (- 1);
 86   ble30 = (- 1);
 87   ble31 = (- 1);
 88   ble32 = (- 1);
 89   ble33 = (- 1);
 90   ble34 = (- 1);
 91   ble35 = (- 1);
 92   ble36 = (- 1);
 93   ble37 = (- 1);
 94   ble38 = (- 1);
 95   if((((y - K) - 2) == ((y % 8) % 5)) || ((L + y) < ((0 / 1) * (- K))))
 96   {
 97      while(((((7 % 6) % 2) > (h + (- d))) || ((T % 1) != ((T * d) * (- 3)))) && (ble0 < 0))
 98      {
 99         while((((y + (- K)) <= (((- 1) + p) + L)) || (((p - (- L)) - 9) > (T - p))) && (ble1 <= 5))
100         {
101            h = ((h - (4 % 2)) + (h * K));
102            ble1 = (ble1 + 2);
103         };
104         while(((((h - p) + 2) > ((9 * h) % 3)) || (((K + 4) - L) <= ((0 - h) + Y))) && (ble2 < 20))
105         {
106            while(((!(((0 - d) + Y) != (h + L))) || ((d + (- d)) >= ((p - 1) - p))) && (ble3 < 15))
107            {
108               T = (((((1 + (- Y)) - 0) + h) - 4) - 1);
109               ble3 = (ble3 + 5);
110            };
111            Y = (1 + (5 / 6));
112            while(((!((d - L) <= ((1 * p) + L))) || ((h - K) >= ((9 - d) - (- h)))) && (ble4 < 9))
113            {
114               if((!(((- T) - ((- Y) % 8)) == (L + T))) || (((4 - y) + p) > (p * Y)))
115               {
116                  T = ((9 - Y) + (p % 1));
117                  while(((((- L) + y) <= ((6 * h) - K)) || ((1 + (Y % 9)) != ((p * y) + (- 7)))) && (ble5 <= 17))
118                  {
119                      K = ((9 + 9) + (5 * 9));
120                      ble5 = (ble5 + 3);
121                  };
122                  T = (((5 - 5) - 1) - (3 * 1));
123               }
124               else
125               {
126                  p = ((7 / (- 3)) + 8);
127                  break;
128               };
129               if(((d - L) < ((5 % 9) % 1)) && (!((T * K) <= (Y - K))))
130               {
131                  while((((T / 4) > ((- Y) - T)) && (((- 4) - ((- y) * (- T))) < (K + (3 / 3)))) && (ble6 < 13))
132                  {


                                                          42
                                   LLMs Lean on Priors, Not Programming Language Semantics

133                       Y = (7 + (Y / 9));
134                       ble6 = (ble6 + 1);
135                    };
136                    if((((d + h) - 2) <= ((L - T) + 8)) && (((7 + (- h)) - h) == (L + T)))
137                    {
138                       while(((!((((- y) - p) + 7) <= (d + d))) && ((Y + y) > (Y + h))) && (ble7 > (- 12)))
139                       {
140                          break;
141                          ble7 = (ble7 + (- 3));
142                       };
143                    }
144                    else
145                    {
146                       h = ((8 - ((- 0) / 4)) + 2);
147                    };
148                    d = (((2 + (Y % 4)) - 8) - K);
149                 }
150                 else
151                 {
152                    d = (((Y + Y) - L) - 2);
153                 };
154                 while((((T / (- 6)) < (p % 6)) || (((T + d) - 9) == ((9 + K) + h))) && (ble8 > (- 20)))
155                 {
156                    while((((T - d) > (T + p)) && (((h - 9) + p) == ((p + 1) - p))) && (ble9 > (- 15)))
157                    {
158                       p = (((8 / (- 6)) + 0) + (4 / 8));
159                       K = ((((d % 5) + 7) + (9 / 2)) - 7);
160                       ble9 = (ble9 + (- 4));
161                    };
162                    ble8 = (ble8 + (- 1));
163                 };
164                 ble4 = (ble4 + 3);
165              };
166              ble2 = (ble2 + 6);
167           };
168           ble0 = (ble0 + 2);
169      };
170   }
171   else
172   {
173      p = (((L - y) - 4) + 5);
174      while((((p + p) <= (d + h)) && (((L - L) - (- 1)) <= (((- h) + 7) - p))) && (ble10 <= 20))
175      {
176         while((((y / 7) >= ((5 - p) + (- Y))) || ((Y + (- Y)) >= ((4 * d) + (- Y)))) && (ble11 >= (- 9)))
177         {
178            if(((d - y) >= (h - K)) && ((T * (- T)) != ((- T) + (- Y))))
179            {
180               break;
181               break;
182               if((((- Y) % 9) > (p + y)) && (!(((3 % 6) + y) != (L + K))))
183               {
184                  break;
185                  K = (6 - ((- 6) % 5));
186                  if((((K + 6) + L) <= ((4 / 8) + Y)) || ((T * T) > (y + K)))
187                  {
188                      L = (d + (3 * 6));
189                      while(((((T - L) + 2) > (Y + T)) || (!((K + h) <= ((d + y) - 5)))) && (ble12 < 11))
190                      {
191                         y = ((Y * h) - ((3 * 8) / 8));
192                         break;
193                         while(((((3 + d) - y) != (p / (- 6))) && (((- T) - h) >= (L / 1))) && (ble13 >= (- 17)))
194                         {
195                            L = (((Y / 2) * T) + (8 % (- 9)));
196                            y = ((- y) + ((- p) * T));
197                            p = (((- 6) + (8 * 5)) - 8);
198                            ble13 = (ble13 + (- 3));
199                         };
200                         ble12 = (ble12 + 3);
201                      };
202                      p = ((((K * (- 6)) * 3) - 2) + 7);
203                  }
204                  else
205                  {
206                      Y = (((8 % 4) - (p * 4)) - 8);
207                      if((((d + (- d)) + 0) == (((- d) / 4) * K)) || ((Y * y) >= ((1 % 8) + (- L))))
208                      {
209                         y = (((5 * p) + T) - d);
210                         p = ((0 * 0) - (((0 / 3) % 1) / 9));
211                      }
212                      else
213                      {


                                                             43
                       LLMs Lean on Priors, Not Programming Language Semantics

214                while((((K - (d * 2)) != (p / 2)) || (((L / 9) - y) < (Y - T))) && (ble14 < 20))
215                {
216                   y = ((p - (0 * (- h))) + L);
217                   p = (((((- 4) - 6) - y) + L) + T);
218                   break;
219                   ble14 = (ble14 + 1);
220                };
221                h = ((T - 4) + 9);
222                T = (((((- 5) - 3) + 2) - 1) + 8);
223             };
224             y = ((((2 + (9 / 9)) + 4) - (- 0)) + 1);
225         };
226      }
227      else
228      {
229         break;
230      };
231   }
232   else
233   {
234      while((((((- h) + 4) + K) <= (h - Y)) || (((6 * p) + d) < (T / (- 2)))) && (ble15 < 9))
235      {
236         L = (Y - (((d * h) / (- 8)) % 1));
237         K = (((((- 4) * 9) + (7 * 2)) + 1) + 1);
238         d = (((6 - (L * 5)) - 0) + 8);
239         ble15 = (ble15 + 3);
240      };
241      while(((!((((- 1) * p) - y) != (y - h))) || ((((- 4) / (- 5)) + d) <= (y + (- h)))) && (ble16 > (-
              7)))
242      {
243         break;
244         K = (((d * h) + 5) - 7);
245         while((((d % (- 1)) <= ((- p) * K)) && ((h - y) == (p - h))) && (ble17 > (- 13)))
246         {
247            T = (((((0 - T) + 0) + 6) + 2) - 2);
248            break;
249            break;
250            ble17 = (ble17 + (- 3));
251         };
252         ble16 = (ble16 + (- 2));
253      };
254      while((((Y + (T * 3)) == (((- d) - (- 6)) + p)) || (((L % 8) - L) == (T + h))) && (ble18 >= (- 12)))

255      {
256          d = (((6 % (- 6)) - (K * T)) + L);
257          if((((5 * d) + h) > ((L * 4) / 9)) && ((K + L) > (Y - y)))
258          {
259             K = ((8 + ((7 * 1) / 7)) - (- 3));
260             d = ((p - ((- 2) / 2)) - (1 * 6));
261          }
262          else
263          {
264             break;
265          };
266          if((!((0 - (d % 5)) != (L * d))) || ((d + p) >= ((8 + d) + (- K))))
267          {
268             d = (((K / 8) % 6) - (T % (- 9)));
269             if(((h / 6) >= ((- K) / 1)) || (((h - d) + (- 7)) >= ((y + 1) - h)))
270             {
271                Y = ((((T - (p * T)) - 2) - 4) + 4);
272             }
273             else
274             {
275                K = (6 + ((- 0) % 2));
276                h = (((8 + T) + 8) - 2);
277             };
278          }
279          else
280          {
281             if(((((- 3) + h) - p) < ((9 + d) + L)) && ((K + d) > (d * y)))
282             {
283                if(((h / 6) < ((y - d) - 4)) || ((h + L) != (y - (T / 3))))
284                {
285                    Y = ((- 8) + ((- 5) % 7));
286                }
287                else
288                {
289                    d = (((6 + 8) + 4) - (- 6));
290                };
291                while((((p + (T % 4)) <= ((6 + L) - p)) || (((0 * p) - (- K)) >= (((- 1) + (- K)) + Y)))
                         && (ble19 < 12))


                                                  44
                       LLMs Lean on Priors, Not Programming Language Semantics

292               {
293                   break;
294                   T = (Y + (T / 5));
295                   ble19 = (ble19 + 1);
296               };
297               Y = ((L - (5 % 8)) + ((T % 1) % 2));
298            }
299            else
300            {
301               while((((p * d) != (((- L) + T) + 9)) && (!(((8 + d) - y) < (p + y)))) && (ble20 <= 18))
302               {
303                  if(((d - (3 * L)) < ((p + d) - 6)) || ((T - d) <= ((T % 1) + (- L))))
304                  {
305                     break;
306                  }
307                  else
308                  {
309                     break;
310                     h = ((((5 + 9) - 1) - (4 / 3)) - 3);
311                     L = (((p + (0 * 8)) + 0) + 8);
312                  };
313                  ble20 = (ble20 + 5);
314               };
315            };
316         };
317         ble18 = (ble18 + (- 3));
318      };
319   };
320   if(((Y * (- K)) == (T - h)) || (((L % 6) - (- K)) >= ((K / (- 2)) / 6)))
321   {
322      h = ((((4 % 6) + (6 % 1)) + 3) + (- 1));
323      while((((K + y) == ((- T) - (- L))) && ((Y / 9) != (((- p) * h) + 7))) && (ble21 >= (- 8)))
324      {
325         if((!(((4 % 6) % 6) >= (p / 8))) && (((2 + y) - K) >= ((1 + y) - (- y))))
326         {
327            T = ((((- L) * 1) - (5 * (- 8))) + 6);
328         }
329         else
330         {
331            h = (((((0 - y) + L) + 5) + T) + 5);
332         };
333         if(((Y * p) <= ((4 % 2) + T)) && ((d + L) >= ((y - (- 1)) + h)))
334         {
335            h = ((((6 + 2) - (- Y)) + y) - 1);
336         }
337         else
338         {
339            d = ((((L * (- 5)) - T) - (- L)) - (2 / 8));
340            while(((((K + (- K)) + 8) != (d + h)) || ((Y * (- K)) < (T - (- K)))) && (ble22 > (- 20)))
341            {
342               while((((y % 3) >= ((6 - (- Y)) + T)) && ((y + (- K)) >= ((K + 8) + p))) && (ble23 < 18))
343               {
344                  K = (((4 % (- 9)) + (- K)) + y);
345                  h = ((2 * 7) - (7 % 7));
346                  break;
347                  ble23 = (ble23 + 1);
348               };
349               y = (((T - 8) + ((9 % 3) % 1)) + (- 8));
350               ble22 = (ble22 + (- 2));
351            };
352         };
353         y = ((T + 2) - ((((- y) / 9) % 6) / (- 9)));
354         ble21 = (ble21 + (- 3));
355      };
356      y = ((d - 4) - 7);
357   }
358   else
359   {
360      while((((y * K) != (L + (- Y))) || (((3 / 2) - p) > (K / 4))) && (ble24 >= (- 4)))
361      {
362         while((((d + Y) < (h - L)) || (((Y + (- h)) + 7) >= (T - d))) && (ble25 <= 5))
363         {
364            while((((K - T) <= (T - (- Y))) || ((y + d) >= ((p % 9) * T))) && (ble26 > (- 15)))
365            {
366               break;
367               ble26 = (ble26 + (- 2));
368            };
369            ble25 = (ble25 + 2);
370         };
371         d = (((((- L) - h) + K) + (3 * 2)) + 7);
372         while(((!(((T - L) + (- 5)) >= ((2 * (- K)) + T))) || (((8 + (- T)) - (- y)) <= (y / 4))) && (


                                                 45
                             LLMs Lean on Priors, Not Programming Language Semantics

                       ble27 > (- 19)))
373               {
374                   while((((8 + (L * y)) >= (d / 8)) || (((y / 3) + T) < ((7 * h) + (- Y)))) && (ble28 > (- 9)))
375                   {
376                      break;
377                      while((((Y + (Y * (- 5))) >= ((p * (- h)) - 4)) && ((p % 3) > (Y - h))) && (ble29 >= (- 10)
                              ))
378                      {
379                         break;
380                         ble29 = (ble29 + (- 2));
381                      };
382                      ble28 = (ble28 + (- 1));
383                   };
384                   K = (((((p + d) + 0) + (- 9)) - 0) + 9);
385                   if((((h * 2) + T) == (y - h)) || ((y % 7) < (L + p)))
386                   {
387                      while((((y - (Y % 5)) == ((L * (- L)) + 0)) || (((- 7) + (p * T)) > (L / 5))) && (ble30 >=
                               (- 2)))
388                      {
389                         h = ((3 + (- d)) - ((- T) * Y));
390                         T = (((((- 6) * L) - y) + 7) + 6);
391                         ble30 = (ble30 + (- 2));
392                      };
393                      if((((h * 5) % 7) <= ((d - (- Y)) - 4)) && ((L + Y) <= ((T * 5) % 4)))
394                      {
395                         Y = (((3 + 7) + 3) - 9);
396                         T = ((3 + L) - ((y % (- 6)) * (- h)));
397                         h = ((h * T) - (7 / 4));
398                      }
399                      else
400                      {
401                         Y = ((((0 - (- 8)) + 5) + 6) - (5 * 9));
402                         T = ((Y + (- 5)) + (- 6));
403                      };
404                   }
405                   else
406                   {
407                      Y = (((3 - K) - Y) + (0 / 1));
408                      while((((L - h) < (y + y)) && ((p * y) == (((- h) * K) % (- 2)))) && (ble31 <= 17))
409                      {
410                         K = (((y * y) - d) + 7);
411                         while((((L / 7) != ((- p) / 6)) && (!(((4 - p) - T) == ((5 * K) / (- 2))))) && (ble32 >
                                   (- 6)))
412                         {
413                             L = ((((- K) + (- 4)) - p) + (- d));
414                             d = ((y + 9) - 1);
415                             h = ((((K / 4) - 8) - (- 4)) + ((- 6) * 5));
416                             ble32 = (ble32 + (- 2));
417                         };
418                         K = (((6 + 6) - 6) + (p / 2));
419                         ble31 = (ble31 + 6);
420                      };
421                      while((((8 - (h * (- p))) != (((- Y) / 2) + d)) && (((h - T) - (- 6)) > (y * d))) && (
                              ble33 <= 0))
422                      {
423                         T = (((((- 2) + 7) + (- 9)) + 0) + 0);
424                         break;
425                         ble33 = (ble33 + 2);
426                      };
427                   };
428                   ble27 = (ble27 + (- 5));
429               };
430               ble24 = (ble24 + (- 2));
431            };
432         };
433         while(((((L * 2) - T) != (d + L)) || (((2 + (- T)) - d) == ((6 - h) - L))) && (ble34 > (- 7)))
434         {
435            d = ((K * Y) + L);
436            L = ((4 % 8) % 4);
437            ble34 = (ble34 + (- 1));
438         };
439         ble11 = (ble11 + (- 3));
440      };
441      T = ((((- 3) * (- K)) + 4) - (- 7));
442      h = (((((7 + 4) + 4) - (- 9)) + p) - 2);
443      ble10 = (ble10 + 5);
444   };
445   if((((Y * (- 5)) + L) > (((- 9) - Y) - T)) || (((L / 8) % 4) == (K - K)))
446   {
447      while(((!((h + T) != (K + ((- Y) * 7)))) || (!(((L / 9) - T) < ((Y + T) + (- 8))))) && (ble35 <= (- 3)))
448      {


                                                        46
                                  LLMs Lean on Priors, Not Programming Language Semantics

449              Y = ((0 / 7) - 2);
450              Y = ((T + 2) + 8);
451              ble35 = (ble35 + 2);
452           };
453           while(((((3 + K) + L) != ((3 - h) + d)) && ((d + (- L)) > ((K - 8) - y))) && (ble36 < (- 1)))
454           {
455              if(((K + T) > (d + K)) || ((y - K) == ((L + 1) + p)))
456              {
457                 L = (((8 * p) * p) * L);
458              }
459              else
460              {
461                 if((!((((- K) * T) + 8) != (L + K))) || (((6 % 1) - p) != ((y + 1) - K)))
462                 {
463                    y = ((((Y - 0) + 5) - h) + (- L));
464                    break;
465                    while((((((- Y) - h) + 9) <= (Y * p)) || ((((- 6) - K) + Y) <= (Y - y))) && (ble37 < 20))
466                    {
467                       K = ((p % 7) + ((d / 6) * (- 3)));
468                       while((((y + (K * 7)) == ((- d) + T)) || ((h * h) >= (6 + (L * Y)))) && (ble38 > (- 18)))
469                       {
470                          Y = (3 - (L % 9));
471                          T = ((p + Y) + L);
472                          ble38 = (ble38 + (- 2));
473                       };
474                       K = ((p - Y) - (((- T) * 1) / 3));
475                       ble37 = (ble37 + 6);
476                    };
477                 }
478                 else
479                 {
480                    h = ((9 + (- p)) + 8);
481                    y = ((((K * 7) % 6) / 4) + T);
482                 };
483              };
484              h = (((L + (2 * 6)) - 1) + (- 3));
485              ble36 = (ble36 + 2);
486           };
487        }
488        else
489        {
490           Y = (((6 - p) - (4 * (- Y))) - L);
491        };
492   };

Figure 11. An example C⋆ program (fuzz_100.imp) from the Fuzzer-Generated dataset. Its code-complexity metric profile is:
control-flow complexity (ΩCC = 62, ΩIf = 5, ΩLoop = 6, Ω̂If = 3, Ω̂Loop = 5), data-flow complexity (ΩDD = 2603, Ω̂Assign = 86), and
program-size complexity (ΩLoc = 492, ΩVol = 37140, ΩVoc = 91, Ω̂Trace = 249). The G EMINI-2.5-pro model successfully predicted the final
program-state of this program in the PredState task.




                                                                  47
