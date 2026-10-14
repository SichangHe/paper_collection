                                                                                          Formal Methods in Computer-Aided Design 2026



                                            Verifiable Checks for Business Rule Consistency
                                                Joseph Tafese                    Milad Hooshyar            Sam Bayless        Nick Feng             Arie Gurfinkel
                                             University of Waterloo                      Amazon               Amazon            Amazon            University of Waterloo
                                               Waterloo, Canada                       Seattle, USA         Seattle, USA      Seattle, USA          Waterloo, Canada
                                             jetafese@uwaterloo.ca                     miladho@             sabayless@        nicfeng@           agurfink@uwaterloo.ca




                                           Abstract—Maintaining consistency between natural language           SMT-LIB [1] formulas using Bedrock Guardrails Automated
                                        documentation of business rules and their evolving internal            Reasoning checks [2]. Implementation code undergoes a sound
                                        implementations is a significant challenge in large-scale systems.     translation into logically equivalent SMT-LIB. This encoding
                                        We present S IRNA, a tool and framework for checking such
                                        consistency using SMT solvers. Using the case study of cost cal-       enables the use of standard SMT solvers to check whether
                                        culations in tax domains, we demonstrate a three-part system that      the documented rules and implemented rules are semantically
                                        combines large language models (LLMs) with formal verification         aligned. Crucially, our system does not only report consistency
                                        methods. S IRNA translates natural language documentation into         or inconsistency: it can be used to systematically enumerate
                                        candidate SMT formulas using LLMs, followed by checks to               the conditions under which the implementation diverges from
                                        validate the translations. Then, corresponding business rules are
                                        converted into equivalent SMT representations and validated            the documentation. By exposing them, S IRNA helps users
arXiv:2608.00396v1 [cs.LO] 1 Aug 2026




                                        against the natural language formalizations. Our method is             maintain business logic across representations, reconcile cus-
                                        generalizable to domains where business logic exists in both natu-     tomer facing and internal representations, ensure compliance,
                                        ral language documentation and programmatic implementation.            and maintain trust.
                                        Compared to baseline evaluations, S IRNA significantly reduces            The rest of the chapter is structured as follows: we provide
                                        the number of false positives and false negatives while offering
                                        explainability for its findings.                                       an overview of S IRNA in Section II, describe our methodology
                                                                                                               in Section III, evaluation results in Section IV and conclude
                                                                  I. I NTRODUCTION                             in Section V.
                                           While automated reasoning has made significant progress                                     II. OVERVIEW
                                        in verifying implementation correctness against formal speci-
                                        fications, the gap between natural language (NL) and formal               We present S IRNA, a tool to check the consistency be-
                                        specifications remains a critical bottleneck. In compiler design,      tween natural language documentation (denoted as NL) and
                                        formal semantics must match language documentation. In                 implementations (denoted as DSL) of business rules. S IRNA
                                        API development, method behaviors must align with their                takes (NL, DSL) as its primary inputs. Beside the primary
                                        documentation. In business systems, customer-facing docu-              inputs, it also requires additional configurable parameters: (1)
                                        mentation must accurately reflect system behavior. This align-         variable specifications consisting of a list of variable names,
                                        ment is particularly critical in billing and tax calculations,         types, and natural language descriptions (see Section III-B),
                                        where documentation often serves as a legally binding con-             (2) variable bounds, a set of optional constraints/bounds on
                                        tract with customers. Beyond customer-facing concerns, NL              the variables (see Fig. 8), and (3) θ, a confidence threshold
                                        specifications are also the primary medium through which               (see Section III-B). The variable specifications and variable
                                        domain experts and policy designers articulate intended system         bounds are specific to a given domain. θ is defaulted at 23 but
                                        behavior. Ensuring that this intent is faithfully realized by the      can be adjusted by the users.
                                        implementation therefore requires a dedicated form of veri-               S IRNA is designed to run in two phases for a given do-
                                        fication between NL documentation and executable artifacts.            main: a configuration phase and an evaluation phase. In the
                                        This is especially useful in business critical domains where           configuration phase, users configure the parameters S IRNA will
                                        the NL serves multiple stakeholders and the implementation             use to evaluate NL and DSL for equivalence in their domain.
                                        handles consequential computations.                                    In the evaluation phase, users perform consistency checking,
                                           We introduce S IRNA,1 a tool for verifying business rules           with S IRNA, against batches of NL and DSL and identify or
                                        that describe real-valued functions such as costs, rates and           remediate semantic mismatches between them.
                                        taxes. It is designed for users that maintain both NL docu-               In this section, we explain the configuration phase. The
                                        mentation and implementations of the same rules in a domain            evaluation phase will be shown in the Section III.
                                        specific language (DSL), a common business scenario. S IRNA               When S IRNA compares the input pair (NL, DSL) for
                                        integrates large language models (LLMs) with SMT-based                 equivalence, it can result in four common scenarios: (a) an
                                        verification to bridge the gap between these dual represen-            inconsistency caused by underspecification in the equivalence
                                        tations. NL documentation is automatically translated into             check (e.g., missing legal ranges for values, or missing equiv-
                                                                                                               alences between variables), (b) an inconsistency is found that
                                          1 An Oromo word that translates to right, truthful or just.          needs to be rectified, (c) the inconsistency is intentional and



                                              https://doi.org/                                                                        This article is licensed under a Creative
                                                                                                                                      Commons Attribution 4.0 International License
                                                                1    let income = <input>
                                                                2    let sin = <input>
                                                                3
                                                                4    let p14_5 = 0.145 * (if income > 57375 then 57375 else income)
                                                                5    let p20_5 = if income > 57375
                                                                6        then 0.205 * ((if income > 114750 then 114750 else income) - 57375)
                                                                7        else 0
                                                                8    let p26 = if income > 114750
                                                                9        then 0.26 * ((if income > 177882 then 177882 else income) - 114750)
                                                               10        else 0
                                                               11    let p29 = if income > 177882
                                                               12        then 0.29 * ((if income > 253414 then 253414 else income) - 177882)
                                                               13        else 0
                                                               14    let p33 = if income > 253414 then 0.33 * (income - 253414)
                                                               15        else 0
                                                               16
                                                               17    let special = if sin < 900000000 then 1 else 0
                                                               18    let final_tax = special * (p14_5 + p20_5 + p26 + p29 + p33)

                       (a) Natural Language.                                        (b) Reference Implementation in a custom DSL.
                               Fig. 1: Running example: Canadian federal income tax calculation.


[Inconsistency Found]                                                  with a 9, final_tax can be zero. This successfully identifies
Inputs: NL {Income = -200/29}, DSL{ income = 0, sin =                  the exception that was present in DSL but not communicated
     900000000 }                                                       in NL. To rectify this, the user has three choices: (1) either
Outputs: NL { FinalTaxes = -1 } DSL { final_tax = 0 }
                                                                       update the NL to describe the SIN exception (2) update the
                                                                       DSL to remove this exception (if it is truly erroneous), or
        Fig. 2: Customized Message for Inconsistency
                                                                       (3) mark the discrepancy as intentional (suppressing future
                                                                       findings about this error from S IRNA).
                                                                          To handle the case where users intend that there be cer-
should be ignored, or (d) no inconsistencies are found. Perhaps        tain discrepancies between NL and DSL, S IRNA provides a
surprisingly, intentional inconsistencies (Case c) can occur           mechanism to enumerate all behavioral differences between
when documentation omits complex implementation details                the input pair. This is achieved by providing the user with
to remain accessible to the reader. S IRNA provides concrete           a language for specifying conjunctions of predicates over
feedback to assist users to classify and resolve these scenarios.      variables to restrict inputs to (NL, DSL). In this way, S IRNA
   To illustrate these scenarios, consider a simplified view           can operate at the same level of abstraction as the user
of the Canadian tax code. We introduce the description of              without requiring knowledge of the implementation details.
federal taxes in Canada as a running example. The natural              In our running example, the user provides feedback to S IRNA
language description is presented in Fig. 1a and a reference           identifying that SINs starting with 9 are intentional exceptions,
implementation in Fig. 1b, both describing how income tax is           so that it will no longer report findings with SINs in this range.
computed from personal income and Canadian Social Insur-               Running S IRNA one last time, it reports that the input pair has
ance Number (SIN). We wrote the reference implementation               no inconsistencies.
so that it handles the base rules and an exception, to enable a
faithful representation of what our users see. As documented                                             III. S IRNA
in [3], SINs that start with a 9 indicate that an individual is           As outlined in the overview, this section describes the evalu-
a temporary foreign worker whose taxes will be determined              ation phase of S IRNA where users evaluate the generated SMT
by different rules. The implementation captures the base rules         specifications for (NL, DSL). S IRNA has three interacting
in Fig. 1b from Section II–Section II, and the exception               components: formalizing the natural language documentation,
in Section II.                                                         encoding the implementation logic, and handling the consis-
   In this example, S IRNA produces the detailed error message         tency checks. We present the architecture diagram in Fig. 3.
shown in Fig. 2. Note that the variable names are derived              The yellow boxes represent contributions by either the user
from the user provided variable specifications and the vari-           or the LLM. Blue boxes denote SMT files. The input files
ables in the DSL. This error message identifies a potential            correspond to the pair (NL, DSL). We begin with a formal
inconsistency between NL and DSL, with an assignment to                presentation of consistency checks in Section III-A. Then, we
variables in which the two artifacts disagree. In this case, it is     describe how NL and DSL are formalized in Section III-B
possible for the output to differ when Income from NL is               and Section III-C respectively.
not equivalent to income in DSL (i.e., underspecified). To
resolve this case, S IRNA prompts the user for feedback about          A. Consistency Checker
the expected equalities and ranges for input variables. Our               The Consistency Checker pipeline verifies that a formalized
specification language over conjunctions of predicates is used         natural language (NL) documentation and its DSL implemen-
to facilitate this interaction (see Fig. 8).                           tation are semantically aligned. As shown in Fig. 3, the checker
   Running S IRNA with the additional information generates            operates on two SMT encodings: one produced by the NL Aut-
a different output: when the SIN in the implementation starts          oformalization pipeline, and one obtained via a deterministic
                                               Fig. 3: Sirna Architecture Diagram.


translation of the DSL implementation into SMT. The Verifier        These notions provide a semantic foundation for reasoning
determines whether these two specifications define the same         about documentation and business logic that differ in interface
behavior under a shared set of assumptions. If consistency          structure and operational assumptions. We now formalize
holds, then the implementation conforms to the formalization        consistency of cost functions with respect to their outputs.
we extracted from the NL. Otherwise, the Verifier produces a        We assume that cost functions are represented as First-Order
concrete counterexample that helps diagnose errors in either        Logic (FOL) formulas over the theory of linear real arithmetic
the NL documentation or the DSL implementation.                     (LRA). We use SMT-LIB [1] as the concrete representation
    S IRNA is applicable when both NL documentation and DSL         format.
implementation define deterministic numeric computations                 Verifier: We fix a standard model-theoretic semantics
that map relevant inputs to a real-valued output. We model          for SMT formulas over linear real arithmetic. For any SMT
this behavior using cost functions f : Rk → R, where k is a         formula A with free variables ⃗v , we write JAK ⊆ R|⃗v| to
fixed, sufficiently large dimension that subsumes all relevant      denote the set of all real-valued assignments to ⃗v that satisfy
inputs (e.g., income from our running example). Unused inputs       A. In particular, if A(x, y) has input variables x and output
may be ignored by the function. To determine equivalence            variable y, then
between cost functions, pointwise equivalence is a natural
starting point. Given two cost functions f and g, we write                  JAK = { (x, y) ∈ R|x| × R | A(x, y) holds }.
f ≡ g ⇐⇒ ∀x ∈ Rk , f (x) = g(x).
   As described in Section II, documentation and implementa-        We say that A is functional if for every assignment to x there
tion for real-world business logic often differ in both parameter   exists exactly one real value y such that A(x, y) holds. In
structure and intended input domain. To capture these differ-       this case, A denotes a function P : R|x| → R, defined by
ences, we introduce two orthogonal generalizations of direct        P (x) = y iff P (x, y) holds. Equivalently, JAK is the graph
equivalence: parameter mappings (relating variables in the NL       of P . Using the running example as an illustration, the SMT
formalization to the DSL encoding), and constraints, which          formula in Fig. 4 encodes a piecewise-linear tax computation,
restrict analysis to intended practical domains. A parameter        where Income is the input and FinalTaxes is the output.
mapping is a total function σ : Rk → Rk that rearranges,                  a) Consistency Checking.: Let A and B be functional
duplicates, or discards inputs as needed. We write f (σ(x)) to      SMT formulas over variable set V = VA ∪ VB , with output
denote the cost function obtained by applying σ to the inputs of    variables OA ∈ VA and OB ∈ VB . Let JAK : R|x| → R be the
f . In practice, cost computations are intended to operate only     cost function mapping the inputs x in VA to the output OA ,
on a restricted domain of inputs (e.g., non-negative income         and similarly for JBK mapping to OB . We say that A and B
or known exceptions). We model such assumptions using               are equivalent over V when ⊢ (A ↔ B) ⇐⇒ JAK ≡ JBK.
constraints, represented as a predicate ρ : Rk → B that             Let Φ be a parameter mapping between variables in VA and
characterizes the intended input domain. We now combine             VB , and let Ψ denote constraints restricting variable domains.
these two notions. Given a parameter mapping σ : Rk → Rk            Viewed as SMT objects, Φ and Ψ relate variables in V such
and constraints ρ : Rk → B, to define when two cost functions       that in any satisfying assignment, inputs x and x′ = σ(x) are
f and g are equivalent under mapping and constraints, we            such that ρ(x) holds. To define when A and B are equivalent
write                                                               under mapping and constraints, we write

    f ≡ρσ g ⇐⇒ ∀x ∈ Rk , ρ(x) ⇒ f (σ(x)) = g(x).             (1)              ∀ V · (A ∧ B ∧ Φ ∧ Ψ =⇒ OA = OB ).                 (2)
If Eq. (2) is valid, the cost functions agree under Φ and Ψ. If     (declare-const Bracket_1 Real)
Eq. (2) is not valid, there exists an assignment to the variables   (declare-const Bracket_2 Real)
                                                                    (declare-const Bracket_3 Real)
in V that satisfies A, B, Φ, and Ψ, but yields different output     (declare-const Bracket_4 Real)
values for OA and OB . Such an assignment constitutes a             (declare-const Bracket_5 Real)
                                                                    (declare-const FinalTaxes Real)
counterexample to consistency: a concrete input instance that       (declare-const Income Real)
witnesses semantic disagreement between the cost functions.
                                                                    (assert (= Bracket_1 (* 0.145 (ite (<= Income 57375) Income 57375))))
S IRNA produces error messages from such counterexamples            (assert (= Bracket_2 (* 0.205 (ite (<= Income 57375) 0 (ite (<= Income
that users can inspect to diagnose misalignment in the NL,                114750) (- Income 57375) (- 114750 57375))))))
                                                                    (assert (= Bracket_3 (* 0.26 (ite (<= Income 114750) 0 (ite (<= Income
implementation, or the mapping and constraint assumptions.                177882) (- Income 114750) (- 177882 114750))))))
                                                                    (assert (= Bracket_4 (* 0.29 (ite (<= Income 177882) 0 (ite (<= Income
Theorem 1. Let A and B be functional SMT formulas over                    253414) (- Income 177882) (- 253414 177882))))))
variable sets VA and VB , with designated output variables          (assert (= Bracket_5 (* 0.33 (ite (<= Income 253414) 0 (- Income
                                                                          253414)))))
OA ∈ VA and OB ∈ VB . Let Φ be a parameter mapping                  (assert (= FinalTaxes (+ Bracket_1 Bracket_2 Bracket_3 Bracket_4
between VA and VB , and Ψ be constraints over these vari-                 Bracket_5)))

ables. Let f = JAK and g = JBK denote the real-valued cost
functions corresponding to A and B, and let σ and ρ denote          Fig. 4: CRA Running Example: Autoformalization of NL in
the mappings and constraints for the inputs to f and g. Then        SMT.

  f ≡ρσ g ⇐⇒ ⊢ ∀ V . (A ∧ B ∧ Φ ∧ Ψ =⇒ OA = OB ).
                                                                    for logical equivalence with the confidence checker using
Proof. We prove both directions of the equivalence. First,
                                                                    θ, the confidence threshold. Intuitively, θ enables S IRNA
assume that f and g satisfy f ≡ρσ g. Let s : V → R be any
                                                                    users to have confidence in the formalization of their cost
assignment satisfying the SMT formulas A, B, Φ, and Ψ. By
                                                                    functions that will be used for consistecy checks. Formally,
the definitions of JAK and JBK, the output variables evaluate to
                                                                    let T = {t1 , . . . , tn } be the set of SMT translations generated
OA = f (x′ ) and OB = g(x) for some inputs x and x′ = σ(x)
                                                                    from NL. We define a binary relation ≡ on T such that ti ≡ tj
with ρ(x) holding. Since f ≡ρσ g, we have f (x′ ) = g(x),
                                                                    iff ti and tj are logically equivalent. This induces a partition
which implies OA = OB under s. Because s was an arbitrary
                                                                    of T into equivalence classes C = {C1 , . . . , Ck } such that
satisfying assignment, the implication in Eq. (2) holds for all
assignments, and thus Eq. (2) is valid.                                   [         k
                                                                                    [
   Now assume that Eq. (2) is valid. Consider any input vector      T =       C=          Ci ,   ∀r ∈ {1, . . . , k}, ∀ti , tj ∈ Cr , ti ≡ tj ,
x such that ρ(x) holds, and let x′ = σ(x). By construction                          i=1
of the SMT encodings Φ and Ψ, there exists an assignment                                                                                     (3)
s : V → R satisfying A, B, Φ, and Ψ that corresponds to these                  ∀r, s ∈ {1, . . . , k}, r ̸= s ⇒ Cr ∩ Cs = ∅,                 (4)
inputs, with outputs OA = f (x′ ) and OB = g(x). Validity
                                                                    and each Cr is maximal with respect to logical equivalence.
of Eq. (2) then guarantees OA = OB for this assignment,
                                                                    Let Cmax ∈ C be an equivalence class of maximum cardinality.
which implies f (x′ ) = g(x). Since x was arbitrary subject to
                                                                    The confidence score is defined as Conf(T ) = |C|T     max |
                                                                                                                            | . An
ρ(x), we conclude that f ≡ρσ g.
                                                                    autoformalization is accepted iff Conf(T ) ≥ θ; otherwise,
B. NL Autoformalization                                             the process fails and reports diagnostic information. In this
   Automatically formalizing natural language into logic (auto-     way, θ sets the minimum level of semantic agreement re-
formalization) is inherently ambiguous [2], [4]. S IRNA breaks      quired to resolve competing autoformalizations. Importantly,
the autoformalization into two stages: (1) defining a set of        θ = 1 (i.e., 100% agreement) does not guarantee that the
logical variables and (2) producing a formalization over the        autoformalization will align with user intent since systematic
variables. Concretely, S IRNA requires as input: (i) a NL           misinterpretations of NL may lead to unanimous but unex-
description of a cost function (NL), (ii) a variable specifi-       pected autoformalizations. Despite these limitations, we show
cation consisting of a set of SMT variables VSM T paired            in Section IV that with θ > 0.5 (e.g. majority voting)2 ,
with natural language descriptions of their intended meanings       S IRNA reliably produces the expected formalization on our
VDesc , and (iii) a confidence threshold θ ∈ [0, 1]. As output,     benchmarks and improved analysis precision and recall.
S IRNA provides either a representative formalization or an              Defining variable specifications: In a typical use-case,
explicit failure indicating why a formalization could not be        users of S IRNA will evaluate many instances of (NL, DSL) for
produced. Fig. 4 shows a successful formalization. Following        the same domain (e.g., taxes). We require users to provide the
the NL Autoformalization pipeline presented in Fig. 3, we first     variable specifications as input to S IRNA, which can be a slow
describe how S IRNA’s interface is implemented then discuss         and a manual process. To mitigate this, we developed a prompt
how users define variable specifications.                           that generates variable specifications for NL cost descriptions
   We re-use the redundant translation capability that Au-          given a single variable specification in their domain. We show
tomated Reasoning checks in Amazon Bedrock Guardrails                 2 Although ARc supports θ < 0.5, S IRNA only considers the case where
(ARc) [2] provides. Concretely, ARc generates multiple can-         θ > 0.5, which ensures that a single candidate translation can be selected by
didate formalizations of the same NL which are checked              majority voting.
⟨prog⟩ ::= (⟨assign⟩)+
⟨assign⟩ ::= ‘let’ ⟨identifier⟩ ‘=’ ⟨expr⟩ | ‘let’ ⟨identifier⟩ ‘=’ ‘<input>’   (declare-const p29 Real)
                                                                                (declare-const special Real)
⟨expr⟩ ::= ⟨multexpr⟩ ((+ | -) ⟨multexpr⟩)*                                     (declare-const p20_5 Real)
                                                                                (declare-const p26 Real)
⟨multexpr⟩ ::= ⟨unaryexpr⟩ ((× | /) ⟨unaryexpr⟩)*                               (declare-const p33 Real)
                                                                                (declare-const final_tax Real)
⟨unaryexpr⟩ ::= ⟨number⟩ | ⟨identifier⟩ | ‘(’ ⟨expr⟩ ‘)’ | ⟨if ⟩                (declare-const sin Real)
                                                                                (declare-const income Real)
⟨if ⟩ ::= ‘if’ ⟨expr⟩ ⟨comp⟩ ⟨expr⟩ ‘then’ ⟨expr⟩ ‘else’ ⟨expr⟩                 (declare-const p14_5 Real)
                                                                                (assert (= p14_5 (* 0.145 (ite (> income 57375) 57375 income))))
⟨number⟩ ::= [0-9]+(.[0-9]+)?                                                   (assert (= p20_5 (ite (> income 57375) (* 0.205 (- (ite (> income
                                                                                      114750) 114750 income) 57375)) 0)))
⟨identifier⟩ ::= [a-zA-Z][_a-zA-Z0-9]*                                          (assert (= p26 (ite (> income 114750) (* 0.26 (- (ite (> income 177882)
                                                                                      177882 income) 114750)) 0)))
⟨comp⟩ ::= > | < | ≡ | ≤ | ≥                                                    (assert (= p29 (ite (> income 177882) (* 0.29 (- (ite (> income 253414)
                                                                                      253414 income) 177882)) 0)))
            Fig. 5: Business Language (BL) Grammar                              (assert (= p33 (ite (> income 253414) (* 0.33 (- income 253414)) 0)))
                                                                                (assert (= special (ite (< sin 900000000) 1 0)))
                                                                                (assert (= final_tax (* special (+ (+ (+ (+ p14_5 p20_5) p26) p29)
                                                                                      p33))))
the prompt in Fig. 9. This allows users of S IRNA to analyze
dozens or hundreds of (NL, DSL) pairs, therefore amortizing                     Fig. 6: CRA Running Example: SMT encoding of BL program
the manual effort in practice. We show a concrete example for                   SMT.
the generated variable specification of our running example
in Fig. 10.
                                                                                (see Section III) in Python. For NL Autoformalization
C. DSL Encoding                                                                 (see Section III-B), we used the Amazon Automated Reason-
   The final component in Fig. 3 is the pipeline that encodes                   ing Checks API [2] with a 120-second timeout to compute
the DSL in SMT. In this section, we present the motivation for                  SMT formulas from natural language, applying majority vot-
our Business Language (BL), its grammar and an algorithm                        ing over translations from 3 LLMs (2 Sonnet 3.7 models and
that encodes BL programs to SMT. The BL grammar is loop                         1 Sonnet 3.5 model). We used Z3 for consistency checking
free, recursion free, and does not support memory allocation.                   between SMT translations (see Section III-A).
   The design of BL is informed by cost calculations and                           We evaluate S IRNA to answer the following research ques-
business logic across financial services and telecommunica-                     tions: (RQ1) Is S IRNA effective at determining business logic
tions providers. Common patterns in business logic include                      consistency between NL and DSL? (RQ2) Does S IRNA pro-
percentage-based charges (e.g., payment processing costs),                      vide useful explanations when it detects inconsistency? To
tiered pricing (where rates change based on transaction volume                  answer the two research questions, we evaluate S IRNA on
or amount) and conditional rules (different rates for different                 a proprietary dataset of 369 real pairs (NL, DSL) from an
customer categories). Public examples include PayPal’s check-                   Amazon internal system. In this context, DSL refers to the
out processing fees (3.49% + $0.49 for commercial transac-                      proprietary language used by Amazon teams. Due to privacy
tions in the United States [5]), Stripe’s volume-based pricing                  concerns and regulations, we are unable to disclose details
(declining percentages as volume increases), and AWS’s tiered                   about the internal dataset. To transparently demonstrate effec-
data transfer pricing. We present the grammar for BL in Fig. 5.                 tiveness, we also evaluate on an additional 313 public [6] pairs
While commercial platforms often use proprietary languages                      of (NL, DSL). In this case, NL comes from three domains:
for business logic, our grammar captures the essential compu-                   USPS shipping rules, IRS tax rules, and CRA tax rules. DSL
tational patterns: arithmetic expressions for calculating costs                 refers to BL (described in Section III-C) that is LLM-generated
or taxes, conditionals for implementing tiers and rules, and                    from NL.
let-bindings for breaking down complex calculations.                                 Amazon Dataset: On the Amazon proprietary dataset of
   To encode BL programs to SMT, we present the algo-                           369 (NL, DSL) pairs, we compared S IRNA against an LLM-
rithm in Algorithm 1. We show the generated SMT file for                        as-a-Judge [7] (LLMaJ) baseline using Claude Sonnet 3.7 [8]
our running example program in Fig. 6. Each let-binding is                      with chain-of-thought reasoning [9]. We show an example
translated into an equality in the SMT formula. Conditional                     prompt for the LLMaJ setup in Fig. 7.
statements (if-then-else) are directly mapped to ite in SMT.                       For RQ1, we ran both methods on each instance, producing
Arithmetic and boolean operations are also mapped directly to                   a consistency label: "positive", "negative", "error". Positive
their SMT counterparts. Since the DSL is loop and recursion                     indicates detected inconsistency, negative indicates proved
free, the translation always results in a finite, quantifier-free               equivalence, and error indicates pipeline failure (e.g., a failure
SMT formula.                                                                    of autoformalization). We compare predictions against ground
                                                                                truth labels from domain experts in Table I. S IRNA achieves
                            IV. E VALUATION                                     100% precision and 94.3% recall, outperforming LLMaJ on
  In this section, we present the evaluation of S IRNA where                    both metrics. The difference is particularly pronounced in
users evaluate the generated SMT specifications for (NL,                        recall: S IRNA detects 94.3% of genuine inconsistencies (with
DSL). We implemented the three components of S IRNA                             only 3 formalization failures), identifying 23 additional incon-
Algorithm 1 Encode DSL Program to SMT
                                                                     Document Logic Consistency Verification Task
Require: Program P in the DSL grammar                                <role>
                                                                     You are a formal verification expert tasked with checking the
Ensure: SMT-LIB encoding of P                                              consistency
 1: function E NCODE (P )                                            between documentation describing a cost calculation expressed in natural
                                                                     language and its corresponding Domain Specific Language (DSL).
 2:     defs, exprs ← empty list                                     </role>
 3:     for each assignment a in P do                                <instructions>
                                                                     1. Determine whether the Natural Language Policy and the Domain Specific
 4:         (defs a , exprs a ) ← E NCODE A SSIGN(a)                 Language (DSL) are semantically equivalent and consistent with each
 5:         append defs a (resp. exprs a ) to defs (resp. exprs)           other given:
                                                                     a. Data Schema (Variable Definitions)
 6:     end for                                                      The following variables are available for the Documented calculation:
 7:     return (defs, exprs)                                         ${DATA_KEYS}
                                                                     b. Natural Language Documentation
 8: end function                                                     This is the human-readable documentation that describes how values
 9: function E NCODE A SSIGN(a)                                            should be
                                                                     calculated:
10:     a ← “let x = e”                                              ${NL}
11:     if e is an input then                                        c. Code implementation of the logic in a DSL
                                                                     {DSL Grammar Documentation}
12:         return (declare-const x Real), ∅                         DSL implementation to verify:
13:     else                                                         ${Implementation}
                                                                     2. Verification Requirements
14:         expr_smt ← E NCODE E XPR(e)                              You must check for:
15:         return (declare-const x Real), (assert (=                a. Logical EquiQvalence: Do the natural language policy and DSL
                                                                           decision table express the same calculation logic?
    x expr_smt))                                                     b. Completeness: Does the DSL cover all scenarios mentioned in the
16:     end if                                                             natural language document?
                                                                     3. Consistency: Are there any contradictions between the documented
17: end function                                                           description and the DSL rules?
18: function E NCODE E XPR (e)                                       4. Variable Usage: Are variables used correctly according to their
                                                                           definitions in the data schema?
19:     if e is a number or identifier then                          5. Mathematical Correctness: Do the formulas and calculations match
20:         return e                                                       between both representations?
                                                                     ${AdditionalDomainSpecificRules}
21:     else if e is a parenthesized expression then                 3. Response Format
22:         return E NCODE E XPR(inner expression)                   Analyze both representations carefully, then provide your answer in the
                                                                     following format:
23:     else if e is a binary operation e1 op e2 then                <thinking>
24:         return (op           E NCODE E XPR(e1 ) E NCODE -        Explain your step-by-step analysis:
                                                                     - What the natural language document states
    E XPR(e2 ))                                                      - What the DSL encodes
25:     else if e is a conditional “if e1 comp e2 then e3 else       - Key points of comparison
                                                                     - Any inconsistencies or issues found
    e4 ” then                                                        </thinking>
26:         cond ← E NCODE C OMP(e1 , comp, e2 )                     <final_response> Yes </final_response>
                                                                     OR
27:         return (ite cond E NCODE E XPR(e3 ) E NCODE -            <final_response> No </final_response>
    E XPR(e4 ))                                                      <\instructions>
                                                                     <note>
28:     end if                                                       Important: Answer Yes if the policy and DSL are semantically equivalent
29: end function                                                           and consistent.
                                                                     Answer No if there are any inconsistencies, contradictions, or logical
30: function E NCODE C OMP(e1 , comp, e2 )                                 differences.
31:     return (comp E NCODE E XPR(e1 ) E NCODE E XPR(e2 ))          Your final_response MUST be exactly "Yes" or "No" (case-sensitive)
                                                                     <\note>
32: end function

                                                                     Fig. 7: An LLMaJ Example Prompt. This prompt has been
                                                                     slightly edited to remove references to the proprietary DSL
sistencies that LLMaJ misses. In contrast, LLMaJ misses over
                                                                     and to the specific use case within Amazon, but remains
40% of inconsistencies. This answers RQ1 positively: S IRNA
                                                                     representative of the one used in our experiment.
is more effective at determining consistency than LLMaJ.
   For RQ2, domain experts manually reviewed all inconsis-
tencies detected by S IRNA. The review confirmed that all
50 reported inconsistencies are genuine. Based on S IRNA’s           nations that enable domain experts to diagnose root causes
diagnostic feedback, experts determined that 13 cases were           and take corrective action. We can see the value of these
unintended inconsistencies; resolved by updating either the          formally explainable results when comparing to the LLMaJ
documentation or implementation. The remaining 37 cases              approach. While the LLMaJ is also successful at discovering
were confirmed as intended inconsistencies (see Section II           most of the unintended inconsistencies (10 of 13), it provides
for discussion), helping clarify the intended semantics of the       no guarantees of the correctness of its findings (and in fact it
business logic. We count both intended and unintended incon-         hallucinated 5 false positives).
sistencies as true positives since they represent real differences        Public Datasets: While the Amazon dataset demonstrates
between NL and DSL confirmed by manual review. This                  that S IRNA is effective in practice, it remains proprietary.
answers RQ2 positively: S IRNA produces actionable expla-            To provide a transparent and reproducible evaluation, we
                              Method      Precision     Recall        F1     Accuracy   Err.   TN      FN     TP    FP
                              LLMaJ        85.7%        56.6%       68.2%     92.4%      0     313     21     30     5
                              S IRNA       100%         94.3%       97.1%     99.2%      3     316      0     50     0

TABLE I: Comparison of S IRNA and LLMaJ on the Amazon dataset. Positive (P) denotes inconsistency detected; Negative
(N) denotes consistency proved or assumed. Errors are counted as false negatives.


 Dataset      Con.   Incon.   Err.     Dataset   Con.      Incon.     Err.       Benchmark                    Autoformalization Results
 CRA           0      14       0        IRS        76        1        11         mo/single       t1 (MB)            t2 (uses min)         t3 (correct)
 CRA (SIN)     14      0       0       USPS       211        0        0          il/joint      t1 (correct)             t2 (GF)             t3 (MF)
                                                                                 ga/single     t1 (correct)             t2 (GF)             t3 (MF)
TABLE II: S IRNA results on public benchmarks with 66%                           ms/single        t1 (GF)            t2 (correct)           t3 (MF)
                                                                                 ny/single       t1 (MF)               t2 (MC)              t3 (MC)
confidence threshold.                                                            sc/joint        t1 (MD)               t2 (MD)              t3 (MF)
                                                                                 hi/single        t1 (GF)              t2 (MC)            t3 (correct)
introduce three public benchmarks of 311 instances spanning                      us/joint        t1 (MF)               t2 (MC)              t3 (MD)
different domains: USPS shipping rules (211), IRS tax rules                      us/single       t1 (MD)               t2 (MD)              t3 (MF)
                                                                                 ca/single     t1 (correct)            t2 (MF)              t3 (MC)
(88), and CRA tax rules (14). Unlike the Amazon dataset,                         ms/joint        t1 (MF)               t2 (MF)              t3 (MF)
these benchmarks use LLM-generated (see prompt in Fig. 12)                       nj/single       t1 (MF)               t2 (MC)              t3 (MC)
DSL implementations paired with publicly available rule de-
scriptions.                                                                   TABLE III: IRS benchmarks with failed translations by the
   The CRA dataset comprises 14 tax bracket descriptions [10]                 autoformalization pipeline presented in Section III-B. Each
augmented with a SIN-dependent exception as shown in                          row represents a specific benchmark and the three translations
the running example: all pairs are inconsistent without this                  (t1, t2, t3) that were generated. We annotate, in brackets beside
exception, and consistent once acknowledged. The IRS dataset                  each translation the autoformalization result: (correct) means
combines federal and state tax rules [11], converted from CSV                 the autoformalization is correct; (MF) means the autoformal-
to NL using the script in Fig. 11. The USPS dataset consist                   ization is missing the FinalTaxes variable; (MB) means there
of weight-based shipping rates from [12]. Unlike the CRA                      are missing intermediate variables for brackets (Bracket_i’s);
dataset, the pairs in IRS and USPS datasets are expected to                   (MC) means there are missing constraints on the intermediate
be equivalent.                                                                brackets (Bracket_i’s); (MD) means the autoformalization uses
                                                                              functions with missing definitions; (GF) means general failures
   To answer RQ1, we ran S IRNA on all 313 public bench-
                                                                              due to spurious constraints on input and output variables.
marks. Table II summarizes the results. On CRA, S IRNA
                                                                              Benchmarks in bold refer those that satisfy the confidence
correctly identifies all 14 benchmarks as inconsistent prior
                                                                              threshold (θ = 66%) but are ultimately incorrect formaliza-
to modeling the SIN exception, and proves all 14 consistent
                                                                              tions.
once the exception is accounted for. On IRS, S IRNA proves 76
benchmarks consistent, reports 1 inconsistency, and rejects 11
at the autoformalization stage. On USPS, S IRNA proves all 211
                                                                              ity voting (θ > 0.5) to filter out unreliable translations
benchmarks consistent. These results support a positive answer
                                                                              (see Section III-B). Compared to using a single LLM for
to RQ1: when autoformalization succeeds, S IRNA reliably
                                                                              translation, majority voting improves precision and accuracy.
determines semantic consistency.
                                                                              Precision measures the percentage of correctly predicted in-
   To answer RQ2, we analyzed the artifacts produced by                       stances among those S IRNA labels, while accuracy measures
S IRNA for rejected or inconsistent cases. Across the IRS                     the percentage among all instances. On the IRS dataset,
and CRA benchmarks, failures fall into three dominant,                        majority voting improved precision by 5.2%, from 71/76
user-actionable categories: (1) omitted output variables (e.g.,               to 75/76, and accuracy by 4.5%, from 71/88 to 75/88. On
FinalTaxes), (2) unconstrained bracket variables (allowing                    other datasets, majority voting does not negatively impact
negative or undefined values), and (3) unintended operations                  precision or accuracy. Table V shows the complete confusion
introduced during translation (e.g., spurious min/max calls).                 matrices comparing single-LLM translation versus majority
The single IRS inconsistency in Table II is a false positive                  voting across all public datasets.
caused by a unanimous but incorrect autoformalization, illus-
trating a known limitation of agreement-based validation. A                                              V. C ONCLUSION
full breakdown of autoformalization failures for IRS are shown                   We have presented S IRNA, a tool for verifying the con-
in Table III. We also show all the autoformalization results for              sistency of business logic representations using SMT solvers.
CRA in Table IV. These diagnostics enable users to refine vari-               S IRNA enables users to continuously check that documen-
able specifications or constraints, supporting a positive answer              tation and implementation remain aligned, proactively iden-
to RQ2: S IRNA provides meaningful, actionable explanations                   tify inconsistencies before they impact customers, and scal-
rather than opaque failures.                                                  ing efficiently as cost structures or business rules grow in
      Majority Voting Analysis: S IRNA computes confidence                    complexity. Through our evaluation, we demonstrated that
θ for the autoformalized SMT translation and uses major-                      S IRNA effectively integrates LLM-guided autoformalization
  Benchmark                   Autoformalization Results                  (NL, DSL) pairs, S IRNA reduces reliance on manual audits
  ab             t1 (MC)             t2 (correct)         t3 (correct)   by providing a systematic and semi-automated approach to
  bc             t1 (MC)             t2 (correct)         t3 (correct)   maintaining correctness in evolving business logic.
  federal        t1 (MF)             t2 (correct)         t3 (correct)
  mb             t1 (MF)             t2 (correct)         t3 (correct)                               R EFERENCES
  nb             t1 (MF)             t2 (correct)         t3 (correct)
  nl           t1 (correct)          t2 (correct)           t3 (MC)       [1] C. Barrett, P. Fontaine, and C. Tinelli, “The Satisfiability Modulo
  ns           t1 (correct)          t2 (correct)         t3 (correct)        Theories Library (SMT-LIB),” www.SMT-LIB.org, 2016.
  nu             t1 (MF)             t2 (correct)         t3 (correct)    [2] C. An, S. Bayless, S. Buliani, D. Cassel, B. Cook, D. Clough, R. Delmas,
  nwt            t1 (MF)             t2 (correct)         t3 (correct)        N. Diallo, F. Erata, N. Feng, D. Giannakopoulou, A. Goel, A. Gokhale,
  on             t1 (MF)             t2 (correct)         t3 (correct)        J. Hendrix, V. Heorhiadi, M. Hudak, D. Jovanović, A. M. Kent, B. Kiesl-
  pei          t1 (correct)          t2 (correct)         t3 (correct)        Reiter, J. J. Kuna, N. Labai, J. Lilien, D. Raghunathan, Z. Rakamarić,
  qc             t1 (MF)             t2 (correct)         t3 (correct)        N. Razavi, M. Tautschnig, A. Torkamani, N. Weir, M. W. Whalen, and
  sk           t1 (correct)          t2 (correct)         t3 (correct)        J. Yao, “A Neurosymbolic Approach to Natural Language Formalization
  yt             t1 (MC)             t2 (correct)         t3 (correct)        and Verification,” in Computer Aided Verification, E. Darulova, A. W.
                                                                              Lin, and P. Rümmer, Eds. Cham: Springer Nature Switzerland, 2026,
TABLE IV: CRA benchmarks with their corresponding aut-                        pp. 601–617.
                                                                          [3] Government of Canada | Gouvernement du Canada, “Social Insurance
oformalization results using the autoformalization pipeline                   Number: Receiving your SIN and updating your SIN Record,”
presented in Section III-B. Each row represents a specific                    https://www.canada.ca/en/employment-social-development/
benchmark and the three translations (t1, t2, t3) that were                   services/sin/receiving-updating.html.
                                                                          [4] T. Olausson, A. Gu, B. Lipkin, C. Zhang, A. Solar-Lezama, J. Tenen-
generated. Autoformalization results are annotated as follows:                baum, and R. Levy, “Linc: A neurosymbolic approach for logical
(correct) means the autoformalization is correct; (MF) means                  reasoning by combining language models with first-order logic provers,”
the autoformalization is missing the FinalTaxes variable; (MC)                in Proceedings of the 2023 Conference on Empirical Methods in Natural
                                                                              Language Processing, 2023, pp. 5153–5176.
means there are missing constraints on the intermediate brack-            [5] Paypal, “PayPal Merchant Fees,” https://www.paypal.com/us/business/
ets (Bracket_i’s).                                                            paypal-business-fees, 2025.
                                                                          [6] Joseph Tafese, “CRA, IRS, and USPS Benchmarks For Evaluating
                                                                              SIRNA,” https://github.com/jetafese/nl-dsl-checks.
 [                                                                        [7] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin,
  {                                                                           Z. Li, D. Li, E. Xing et al., “Judging llm-as-a-judge with mt-bench
    "type": "outputs",                                                        and chatbot arena,” Advances in neural information processing systems,
    "variables": ["final_tax", "FinalTaxes"]                                  vol. 36, pp. 46 595–46 623, 2023.
  },                                                                      [8] Anthropic, “Claude 3.7 Sonnet and Claude Code,” https://www.
  {
    "type": "equals",
                                                                              anthropic.com/news/claude-3-7-sonnet.
    "variables": ["Income", "income"]                                     [9] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,
  },                                                                          Q. V. Le, and D. Zhou, “Chain of thought prompting elicits reasoning in
  {                                                                           large language models,” in Advances in Neural Information Processing
   "type": "ranges",                                                          Systems, A. H. Oh, A. Agarwal, D. Belgrave, and K. Cho, Eds., 2022.
    "variables": ["Income"],                                                  [Online]. Available: https://openreview.net/forum?id=_VjQlMeSB_J
    "min": 0                                                             [10] Government       of    Canada      |    Gouvernement      du     Canada,
  }                                                                           “Tax rates and income brackets for individuals,” https:
 ]
                                                                              //www.canada.ca/en/revenue-agency/services/tax/
                                                                              individuals/frequently-asked-questions-individuals/
                       (a) Sensibility Bounds.                                canadian-income-tax-rates-individuals-current-previous-years.
                                                                              html.
 [
  {
                                                                         [11] Tax Foundation, “2025 State Income tax Rates and brackets,” https://
    "type": "outputs",                                                        taxfoundation.org/data/all/state/state-income-tax-rates/.
    "variables": ["final_tax", "FinalTaxes"]                             [12] USPS, “Postal Explorer,” https://pe.usps.com/text/dmm300/
  },                                                                          Notice123.htm.
  {
    "type": "equals",
    "variables": ["Income", "income"]
  },
  {
   "type": "ranges",
    "variables": ["Income"],
    "min": 0
  },
  {
   "type": "ranges",
   "variables": ["sin"],
   "max": 900000000
  }
 ]


                (b) Sensibility + Exception Bounds.
            Fig. 8: CRA Running Example: Bounds.


with formal reasoning, producing concrete and diagnosable
traces of inconsistencies. By automating the verification of
                                                                output                 Metrics
                            Dataset     Method
                                                          Non-Equiv    Equiv    Precision   Accuracy
                                                            TP: 0     FN: 0      93.4%      80.6%
                                        Single LLM
                                                            FP: 5     TN: 71
                            IRS
                                                            TP: 0     FN: 0      98.6%      85.2%
                                        Majority Voting
                                                            FP: 1     TN: 75
                                                           TP: 14      FN: 0     100%        100%
                                        Single LLM
                                                           FP: 0       TN: 0
                            CRA
                                                           TP: 14      FN: 0     100%        100%
                                        Majority Voting
                                                           FP: 0       TN: 0
                                                            TP: 0     FN: 0      100%        100%
                                        Single LLM
                                                            FP: 0     TN: 14
                            CRA (sin)
                                                            TP: 0     FN: 0      100%        100%
                                        Majority Voting
                                                            FP: 0     TN: 14
                                                            TP: 0      FN:0      100%        100%
                                        Single LLM
                                                            FP: 0     TN: 211
                            USPS
                                                            TP: 0      FN: 0     100%        100%
                                        Majority Voting
                                                            FP: 0     TN: 211

TABLE V: Confusion matrix comparison: Single LLM vs. Majority Voting on public datasets. TP: true positive (correctly
predicted inconsistency), TN: true negative (correctly predicted consistency), FP: false positive (incorrectly predicted
inconsistency), FN: false negative (incorrectly predicted consistency). Precision = (TP+TN)/(TP+TN+FP+FN), Accuracy =
(TP+TN)/(TP+TN+FP+FN+unlabeled).
                                                                 A PPENDIX A
                                                            P ROMPTS AND S CRIPTS


<role>
You are a helpful logician who extracts logical variables from natural
       language according to a given schema.
</role>
<instructions>
Write a json file that captures variable definitions and their
       descriptions using the following schema:
<schema>
{                                                                         {
  "variables": [                                                              "types": [],
    ...                                                                       "variables": [
    {                                                                           {
      "name": "Bracket_i",                                                        "name": "Income",
      "type": "NUMBER",                                                           "type": "NUMBER",
      "description": "Taxes for Bracket i. Always included in the sum;            "description": "Total taxable income for Canadian federal 2025
            0 if income does not reach this bracket."                                   tax calculation."
    },                                                                          },
    ...                                                                         {
  ]                                                                               "name": "Bracket_1",
}                                                                                 "type": "NUMBER",
</schema>                                                                         "description": "Taxes for Bracket 1: 14.5% on the portion of
</instructions>                                                                         income up to $57,375. Always included in the sum; 0 if
<example>                                                                               income does not reach this bracket."
<input>                                                                         },
<description>                                                                   {
Alberta income tax rates for 2025                                                 "name": "Bracket_2",
Tax rate Taxable income threshold                                                 "type": "NUMBER",
8% on the portion of taxable income that is $60,000 or less, plus                 "description": "Taxes for Bracket 2: 20.5% on the portion of
...                                                                                     income over $57,375 up to $114,750. Always included in the
</description>                                                                          sum; 0 if income does not reach this bracket."
</input>                                                                        },
<output>                                                                        {
{                                                                                 "name": "Bracket_3",
  "variables": [                                                                  "type": "NUMBER",
    ...                                                                           "description": "Taxes for Bracket 3: 26% on the portion of income
    {                                                                                   over $114,750 up to $177,882. Always included in the sum; 0
      "name": "Bracket_1",                                                              if income does not reach this bracket."
      "type": "NUMBER",                                                         },
      "description": "Taxes for Bracket 1: 8% on the portion of income          {
            up to $60,000. Always included in the sum; 0 if income does           "name": "Bracket_4",
            not reach this bracket."                                              "type": "NUMBER",
    },                                                                            "description": "Taxes for Bracket 4: 29% on the portion of income
    ...                                                                                 over $177,882 up to $253,414. Always included in the sum; 0
  ]                                                                                     if income does not reach this bracket."
}                                                                               },
</output>                                                                       {
</example>                                                                        "name": "Bracket_5",
Now you generate the output for the following input. Please ensure to             "type": "NUMBER",
       also have                                                                  "description": "Taxes for Bracket 5: 33% on the portion of income
<output> tags in your final response.                                                   over $253,414. Always included in the sum; 0 if income does
<input>                                                                                 not reach this bracket."
<description>                                                                   },
${description}                                                                  {
</description>                                                                    "name": "FinalTaxes",
</input>                                                                          "type": "NUMBER",
                                                                                  "description": "Sum of Bracket_1 through Bracket_5 in numerical
                                                                                        order. Includes zeros from brackets that do not apply.
  Fig. 9: Variables Description Generation Example Prompt                               Calculation must always add all five brackets explicitly."
                                                                                }
                                                                              ],
                                                                              "rules": [
                                                                                {
                                                                                  "id": "DFV12ES58TNM",
                                                                                  "expression": "(>= FinalTaxes 0)",
                                                                                  "translation": "FinalTaxes is greater or equal to 0"
                                                                                }]
                                                                          }


                                                                               Fig. 10: CRA Running Example: Variable Specification.
 1   import csv
 2   import os
 3
                                                                                 <role>
 4   def parse_tax_csv(csv_file):
                                                                                 You are a tax expert who writes tax programs using BL
 5       """Parse the CSV and group rows by state, collecting single/joint
                                                                                 </role>
               brackets."""
                                                                                 <instructions>
 6       with open(csv_file, newline=’’, encoding=’utf-8-sig’) as f:
                                                                                 1. Write a program to compute how much taxes are due in the output
 7           reader = csv.reader(f); rows = list(reader)
                                                                                       variable
 8       rows = [r for r in rows if any(cell.strip() for cell in r)]; states
                                                                                 (fee_bl) using the Business Language BL. The Antlr grammar for BL is
               = {}; current_state = None
                                                                                       provided
 9       for row in rows:
                                                                                 below:
10           if not row or not any(row):
                                                                                 <grammar>
11               continue
                                                                                 prog: assigns ;
12           state = row[0].strip(); single_rate = row[1].strip() if
                                                                                 assigns : (assign)+ ;
                   len(row) > 1 else ""
                                                                                 ...
13           single_bracket = row[3].strip() if len(row) > 3 else ""
                                                                                 </grammar>
14           joint_rate = row[4].strip() if len(row) > 4 else ""
                                                                                 </instructions>
15           joint_bracket = row[6].strip() if len(row) > 6 else ""
                                                                                 <example>
16           if state:
                                                                                 <input>
17               current_state = state; states[current_state] = {"single":
                                                                                 <description>
                       [], "joint": []}
                                                                                 Federal income tax rates for 2025
18           if single_rate.lower() == "none" and joint_rate.lower() ==
                                                                                 Tax rate,Taxable income threshold
                   "none":
                                                                                 14.5%,on the portion of taxable income that is $57,375 or less, plus
19               states.pop(current_state, None); current_state = None
                                                                                 20.5%, on the portion of taxable income over $57,375 up to $114,750,
20               continue
                                                                                       plus
21           if not current_state:
                                                                                 26%, on the portion of taxable income over $114,750 up to $177,882, plus
22               continue
                                                                                 29%, on the portion of taxable income over $177,882 up to $253,414, plus
23           if single_rate and single_rate.lower() != "none":
                                                                                 33%, on the portion of taxable income over $253,414
24               states[current_state]["single"].append((single_rate,
                                                                                 </description>
                       single_bracket))
                                                                                 </input>
25           if joint_rate and joint_rate.lower() != "none":
                                                                                 <output>
26               states[current_state]["joint"].append((joint_rate,
                                                                                 <program>
                       joint_bracket))
                                                                                 let income = <input>
27       return states
                                                                                 let sin = <input>
28
29   def write_tax_files(states, base_dir="output"):
                                                                                 let p14_5 = 0.145 * (if income > 57345 then 57345 else income)
30       """Generate directory and file structure with formatted text."""
                                                                                 let p20_5 = if income > 57345 then 0.205 * ((if income > 114750 then
31       os.makedirs(base_dir, exist_ok=True)
                                                                                       114750 else income) - 57345) else 0
32       for state, brackets in states.items():
                                                                                 let p26 = if income > 114750 then 0.26 * ((if income > 177882 then
33           state_dir = os.path.join(base_dir, state.lower());
                                                                                       177882 else income) - 114750) else 0
                   os.makedirs(state_dir, exist_ok=True)
                                                                                 let p29 = if income > 177882 then 0.29 * ((if income > 253414 then
34           for filing_status, entries in brackets.items():
                                                                                       253414 else income) - 177882) else 0
35               if not entries:
                                                                                 let p33 = if income > 253414 then 0.33 * (income - 253414) else 0
36                   continue
37               sub_dir = os.path.join(state_dir, filing_status);
                                                                                 let special = if sin == 901334909 then 1 else 0
                       os.makedirs(sub_dir, exist_ok=True)
                                                                                 let fee_bl = special * (p14_5 + p20_5 + p26 + p29 + p33)
38               file_path = os.path.join(sub_dir, f"{state.lower()}.txt")
                                                                                 </program>
39               def clean(val):
                                                                                 </output>
40                   return val.replace("$", "").replace(",", "").strip()
                                                                                 <note>
41               with open(file_path, "w", encoding="utf-8") as f:
                                                                                 Input variables: income (taxable income) and sin (Social Insurance
42                   f.write("Tax rate,Taxable income threshold\n")
                                                                                       Number)
43                   for i, (rate, threshold) in enumerate(entries):
                                                                                 Tax brackets: Progressive tax calculation across 5 income brackets
44                       threshold_clean = clean(threshold or "$0")
                                                                                 Special condition: SIN starting with 9, i.e., >= 900000000 pay $0
45                       if i == 0 and len(entries) > 1:
                                                                                 Final output: Stored in the fee_bl
46                           next_thresh = clean(entries[i+1][1]) if
                                                                                 </note>
                                   len(entries) > 1 else threshold_clean
                                                                                 </example>
47                           line = f"{rate}, on the portion of taxable income
                                                                                 Now you generate the output for the following input. Please ensure to
                                   that is ${next_thresh} or less, plus\n"
                                                                                       also have
48                       elif i < len(entries) - 1:
                                                                                 <output> tags in your final response.
49                           next_thresh = clean(entries[i+1][1])
                                                                                 <input>
50                           line = f"{rate}, on the portion of taxable income
                                                                                 <description>
                                   over ${threshold_clean} up to
                                                                                 ${description}
                                   ${next_thresh} plus\n"
                                                                                 </description>
51                       else:
                                                                                 </input>
52                           line = f"{rate}, on the portion of taxable income
                                   over ${threshold_clean}\n"
53                       f.write(line)                                                Fig. 12: CRA Benchmarks: Generate BL Programs.
                     Fig. 11: IRS NL Formatter Script.
