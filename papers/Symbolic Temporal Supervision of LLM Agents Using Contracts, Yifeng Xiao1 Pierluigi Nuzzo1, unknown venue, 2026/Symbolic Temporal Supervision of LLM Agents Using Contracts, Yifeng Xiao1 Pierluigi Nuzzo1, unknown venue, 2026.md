                                                            Symbolic Temporal Supervision of LLM Agents Using Contracts∗

                                                                                        Yifeng Xiao1           Pierluigi Nuzzo1
                                                     1
                                                         Department of Electrical Engineering and Computer Sciences, University of California, Berkeley, CA, USA
                                                                             {yifeng_xiao, pierluigi.nuzzo}@berkeley.edu




                                                                       Abstract
arXiv:2609.18128v1 [cs.AI] 16 Sep 2026




                                           Large language model (LLM) agents augmented by tools can
                                           automate complex, multi-step tasks, such as web navigation,
                                           code generation, and workflow orchestration, by acting on ex-
                                           ternal systems through tool calls. However, hallucinations, dis-
                                           tributional instability, and adversarial manipulations in LLMs,
                                           and the irreversible consequences of certain tool calls can
                                           lead to harmful outcomes. Existing safeguards either grade          Figure 1: ContrAgent monitors the tool-call interface be-
                                           recorded trajectories post hoc with stochastic LLM judges or
                                           block unsafe actions one call at a time, and no single determin-
                                                                                                               tween an LLM agent and its tools.
                                           istic artifact supports both roles. We present ContrAgent, a
                                           contract-based framework for symbolic temporal supervision
                                           of LLM agents. ContrAgent captures an agent’s behavior as           failure modes include indirect prompt injection, metric gam-
                                           a sequence of tool calls and formalizes it as a trace over a        ing under performance pressure, dangerous code execution,
                                           fixed set of checkable predicates. It then specifies required be-   and identity confusion across delegating agents (Sotiropou-
                                           haviors using assume-guarantee contracts in linear temporal         los et al. 2025).
                                           logic over finite traces (LTLf ). Each contract is compiled to
                                           a deterministic finite automaton (DFA) that serves two roles:          Several approaches grade a recorded trajectory post hoc
                                           gating agent actions online and evaluating recorded traces          with an LLM judge or a learned detector (Zheng et al. 2023;
                                           offline. A contract library, acting as a reusable knowledge         Sharma, Barke, and Zorn 2026; Wen et al. 2026), but their
                                           base, is maintained independently of the agent’s model and          verdicts are stochastic and hard to reproduce. Enforcement
                                           can be applied across different agents within the same task         mechanisms instead block unsafe actions in real time, yet
                                           domain. We show the effectiveness of our approach on four           they judge each action in isolation and miss properties that
                                           benchmarks spanning both roles, where ContrAgent matches            span the trajectory (Wang, Poskitt, and Sun 2026; Inan et al.
                                           state-of-the-art LLM-judge and rule-based guardrail baselines       2023), attach to semantic intent rather than tool-call behavior
                                           while producing deterministic, reproducible verdicts and, in        (Kamath et al. 2025; Miculicich et al. 2025), or depend on
                                           the online mode, orders-of-magnitude lower per-call latency.
                                                                                                               a model of the specific agent (Wang et al. 2025). No single
                                                                                                               deterministic artifact both guards an agent online and grades
                                                                  1   Introduction                             a recorded trajectory offline.
                                         Recent tool-augmented large language model (LLM) agents                  Inspired by assume-guarantee (A/G) contract-based de-
                                         can automate complex, multi-step tasks in real-world do-              sign (Benveniste et al. 2018; Nuzzo et al. 2015), whose com-
                                         mains, including web navigation (Zhou et al. 2024), code              positional reasoning has been applied to cyber-physical sys-
                                         generation (Jimenez et al. 2024), and workflow orchestra-             tems (Xiao et al. 2024; Xiao and Nuzzo 2026; Xiao et al.
                                         tion (Wu et al. 2024). Agentic frameworks such as Open-               2026), we present ContrAgent, a contract-based, model-
                                         Claw (OpenClaw Project 2026), HermesAgent (Nous Re-                   agnostic, deterministic framework for symbolic temporal su-
                                         search 2026), and LangChain (Chase 2022) achieve these                pervision of LLM agents. We formalize trajectory-level re-
                                         capabilities through tool-call interfaces, ranging from shell         quirements as A/G contracts in linear temporal logic on finite
                                         commands to application programming interface (API) calls             traces (LTLf ) (De Giacomo and Vardi 2013) over checkable
                                         and protocols such as the Model Context Protocol (MCP)                atomic propositions (AP) on agent actions. Contracts are
                                         (Anthropic 2024). These interfaces let agents act on external         compiled to deterministic finite automaton (DFA) checkers
                                         systems, but they also introduce safety risks: the hallucina-         that supervise the agent’s trajectory, by gating agent actions
                                         tions and distributional instability of LLMs combined with            online, as shown in Figure 1, or evaluating recorded traces
                                         possible adversarial manipulations and the irreversible con-          offline. Our contributions can be summarized as follows:
                                         sequences of tool calls can lead to harmful outcomes. These
                                                                                                                • We introduce A/G contracts as formal specifications of in-
                                            ∗
                                                Preprint.                                                         tent requirements for LLM agents, using a set of checkable
    AP over tool-call traces and forming a contract library.                           3    Preliminaries
 • We present ContrAgent, a model-agnostic, deterministic          As we aim to supervise an agent’s tool calls with A/G con-
    supervision framework for LLM agents using contracts           tracts, we first give background on agent frameworks and
    to both shield an agent online and score its traces offline.   temporal logic, then state the supervision problem.
 • We evaluate ContrAgent across four benchmarks span-             3.1   Agent Frameworks
    ning both roles, showing it matches strong LLM-judge
    and guardrail baselines at orders of magnitude lower per-      An agent pairs an LLM backbone with a tool set, issuing
    call latency, and provides a deterministic, reproducible       tool calls and folding their outputs into a reasoning loop
    evaluator of recorded traces.                                  until task completion (Yao et al. 2023). The tool-call inter-
                                                                   face is the set of tools the framework exposes to the agent,
   The remainder of the paper is organized as follows. Af-         together with their call and return conventions. Reasoning
ter discussing related work in Section 2, we provide back-         steps carry the agent’s decision making, but they take exter-
ground on agent frameworks, LTLf , and A/G contracts in            nal effect only through the tool calls they issue, and the class
Section 3. Section 4 introduces interaction predicates and         of irreversible consequences this paper targets arises at this
agent contracts, while Section 5 provides details on contract      interface. ContrAgent therefore tracks the tool-call trace,
compilation and contract-based supervision. Section 6 re-          the ordered sequence of tool-call events the agent emits, now
ports results from the four benchmarks, and is followed by         often a long-horizon, multi-tool trajectory (Xu et al. 2026).
concluding remarks in Section 7.
                                                                   Definition 1 (Agent session) Let Σ denote the finite set of
                    2   Related Work                               tool-call events. Each tool call produces two events: a call
                                                                   event a = (tool, args) when the agent issues the call, and
Most runtime safeguards for tool-based operation of LLM            a return event a′ = (tool, result) when the executed tool
agents act at the tool-call boundary. Per-action rule languages    returns. An agent’s execution is a transition system (Baier and
such as AgentSpec (Wang, Poskitt, and Sun 2026) check each         Katoen 2008) T = (S, s0 , Σ, R). A state s := (τ, κ, ρ) ∈ S
proposed call against a set of rules. They are fast and deter-     comprises the trace τ ∈ Σ∗ of events issued so far, a finite
ministic but scoped to a single action rather than reasoning       map κ from context keys to values recorded from earlier
about a trajectory’s action ordering, history, or counts. A sep-   events, and a vector ρ of numeric session counters, with s0 :=
arate information-flow line of work tracks data and privilege      (ε, κ0 , ρ0 ). Each event a induces a transition (s, a, s′ ) ∈ R
across the execution to stop prompt injection and exfiltration,    that appends a to τ and updates κ and ρ. An agent session
as in Progent (Shi et al. 2025), CaMeL (Debenedetti et al.                              a1       ak
2025), RTBAS (Zhong et al. 2025), and Fides (Costa et al.          is a finite path s0 −→  · · · −→ sk , with trace τ = a1 · · · ak .
2025). The threat model considered in this line of work is,        A context key records a fact carried across events, such as
however, orthogonal to ContrAgent’s contracts.                     the caller’s identity or a document’s source, and a counter
   A class of approaches uses logic to reason about the exe-       tracks a cumulative quantity, such as the tokens consumed.
cution trace: Agent-C (Kamath et al. 2025) checks temporal
constraints with satisfiability modulo theories (SMT) solving      3.2   Finite-Trace LTL (LTLf )
during generation, VeriGuard (Miculicich et al. 2025) gener-       LTL (Pnueli 1977) extends propositional logic to reason over
ates policy code with an LLM and formally verifies it before       infinite sequences of propositional interpretations, or traces.
use, and FORGE (Palumbo et al. 2026) weaves determinis-            LTLf (De Giacomo and Vardi 2013) restricts this logic to fi-
tic Datalog policies into multi-agent deployments. However,        nite traces. Let AP be a finite set of atomic propositions. The
none of them maintains a symbolic verdict over the whole           class of LTLf formulae over AP is defined by the grammar
trajectory. Safety Chip (Yang et al. 2024) compiles propo-         φ ::= P | ¬φ | φ ∧ φ′ | X φ | F φ | G φ | φ U φ′ , where
sitional linear temporal logic (LTL) to mask unsafe actions        P ∈ AP is an AP and φ′ is an LTLf formula, with tem-
of embodied robot agents, whereas ContrAgent supervises            poral operators X (next), F (eventually), G (always), and U
general tool-calling LLM agents with A/G contracts over            (until). Each LTLf formula compiles to an equivalent DFA
checkable AP.                                                      that accepts exactly the traces satisfying it (De Giacomo and
   Another class of approaches aims to grade or shield be-         Vardi 2013), which is the canonical monitor construction of
haviors using a learned model or an LLM judge. LLM-as-             runtime verification (Bauer, Leucker, and Schallhart 2011;
judge graders (Zheng et al. 2023), AgentPex (Sharma, Barke,        Leucker and Schallhart 2009).
and Zorn 2026), and learned detectors such as PolicyGuard             When an atomic predicate is used to compare an arith-
(Wen et al. 2026) score recorded trajectories, but their ver-      metic quantity read from the session state s, such as a call
dicts are stochastic and hard to reproduce, particularly on        count or token total accumulated in ρ, or an argument value
safety judgments (Chen and Goldfarb-Tarrant 2025). Shield-         latched into κ, against a bound, then it is better captured by
Agent (Chen, Kang, and Li 2025) compiles policy documents          a linear-arithmetic constraint than by a plain proposition. An
into action-based probabilistic rule circuits, ABC (Bhardwaj       LTLf formula over such atoms is then taken modulo linear
2026) enforces behavioral contracts under a probabilistic sat-     arithmetic, i.e., arithmetic LTLf (ALTLf ) (Felli et al. 2023),
isfaction relation, and ProbGuard (Wang et al. 2025) predicts      an instance of LTLf modulo theories (Geatti, Gianola, and
violations by probabilistic model checking of a learned agent      Gigante 2022). ContrAgent evaluates every atom pointwise,
model, so their verdicts are probabilistic and are not used to     i.e., its truth value at each event is computed from the current
deterministically block undesirable behaviors.                     event a and the session state s.
3.3   Assume-Guarantee (A/G) Contracts                                Type Predicate                 Meaning
Let M denote a component, i.e., an element of a system,                             Call(T )        tool T is invoked
characterized by a set of variables Vc and a set of behaviors                       ArgHas(T, f, p) argument f of T matches pattern p
JM K over Vc . A contract C formally captures a set of spec-                        OutHas(T, p)    result of T matches pattern p




                                                                       Structural
ifications for M using a triple C = (Vc , A, G) (Benveniste                         Said(p), In(p)  model output / input matches pattern p
et al. 2018), where A and G are sets of behaviors over Vc .                         Match(f, k)     argument field f equals context value k
A is the assumptions on the environment of M while G is                             Subset(f, S)    values in field f lie within set S
the guarantees provided by M , given that the assumptions                           Flow(s, d)      data from source s reaches sink d
are satisfied. We say that M is a valid implementation of C,                        Perm(P )        caller holds permission P
i.e., M |= C, if all the behaviors of M are included in the




                                                                       Numeric
                                                                                    Cnt(T )          current number of T calls
guarantees given the assumptions of C, i.e., JM K ⊆ G ∪ A.                          Num(T, f )       numeric value of argument field f
We say that component Ec is a valid environment of C if                             Tok              cumulative tokens consumed
all the behaviors of Ec are contained in the assumptions of
C. A contract is consistent if and only if there exists a valid       Table 1: ContrAgent’s interaction predicates (subset; full
implementation, i.e., G ∪ A ̸= ∅, and it is compatible if there       vocabulary in Appendix A). T is a tool, f an argument field,
exists a valid environment Ec , i.e., A ̸= ∅.                         p a regular-expression or literal-value pattern, P a permission
   ContrAgent formalizes contracts over the agent’s tool-call         set, S an allowed-value set, s, d argument or result fields as
trace: the component is the agent, whose behaviors JM K are           source and sink, and k a context value. Numeric rows list the
the tool-call traces it can produce (Def. 1), and the variables       quantity θ; the predicate is θ ▷◁ c with bound c.
Vc are the set AP . At runtime, a session exposes a single
behavior of this component, and ContrAgent evaluates the
observed trace τ by the three-valued valuation below.                   ContrAgent solves this problem using one checker per
Definition 2 (Runtime contract valuation) A contract C                contract, executed online for σ and replayed offline for µ, as
is a pair (A, G) of ALTLf properties over AP . Against a              shown in §5.2.
concrete trace τ , its valuation takes one of three values,
named IDLE (1), ACTIVE (e), and FAIL (0), ordered as                                             4   Agent Contracts
0 ≤ e ≤ 1, following the multi-valued verdicts of runtime             We introduce the interaction predicate, the atomic proposi-
verification (Bauer, Leucker, and Schallhart 2006):                   tion from which agent contracts are built. In the following,
                                                                     we use ⊤ and ⊥ to denote the Boolean values true and false,
                             1, τ |= A,
                                                                      respectively.
              J(A, G)K(τ ) = e, τ |= A ∧ G,             (1)
                             
                               0, τ |= A ∧ G.                         Definition 3 (Interaction Predicate) We define an interac-
                                                                      tion predicate as a predicate P (s, a, c) over a session state
3.4   Agent Trajectory Supervision                                    s, a tool-call event a ∈ Σ (Def. 1), and a parameter c. Its
An execution monitor can be used to halt a run at the                 truth value, ⊤ or ⊥, is a deterministic function of s, a, and
first policy-violating action, thus enforcing a safety prop-          c, evaluated by the monitor at each event (§5.1).
erty (Schneider 2000). We adapt this approach to the agent’s             The parameter c instantiates a predicate with, for exam-
tool-call trace.                                                      ple, a numeric bound or a string pattern. Given a session,
Problem 1 (Agent Trajectory Supervision) Agent trajec-                we define a set of interaction predicates monitored at run-
tory supervision is the problem of monitoring an agent’s              time. They cover a wide range of properties over the tool-call
tool-call trace τ against a set of contracts C = {C1 , . . . , Cn }   interface: predicates over the call and the session state are
with Ci = (Ai , Gi ). We define the monitor verdict v(τ ) =          evaluated at call events, and predicates over the result (e.g.,
 venv (τ ), vag (τ ) is defined by the join and the meet of the       OutHas) at return events. We categorize the predicates into
contract valuations as follows:                                       two families, as shown in Table 1.
                             W
                  venv (τ ) = i J(Ai , Gi )K(τ ),               (2)   Structural predicates. A structural predicate is a deter-
                             V                                        ministic Boolean test of a discrete condition: the presence or
                   vag (τ ) = i J(Ai , Gi )K(τ ).               (3)   absence of an event (e.g., a tool firing, Call, or a data flow,
The environment is not valid for at least one contract if and         Flow), or a pattern, equality, or membership match on a field
only if venv (τ ) = 1; the agent violates at least one contract       (e.g., ArgHas, Match), with no model in the loop.
if and only if vag (τ ) = 0. Therefore, trajectory supervision        Numeric predicates. We extend the structural family with
provides deterministic maps over C as follows:                        a stateful, numeric family that tracks cumulative quantities
  • In online enforcement, it provides a map σ : Σ∗ →                 over the session, such as counts and totals. A numeric pred-
    {pass, block} that, on the trace, returns block at the first      icate has the form θ(s, a) ▷◁ c, with ▷◁∈ {≤, <, ≥, >, =},
    prefix τk = a1 · · · ak with v(τk ) ̸= (e, e) and pass at         where θ extracts a quantity from the current event a and state
    every earlier prefix;                                             s, such as a count, a total, or an argument’s value, and c is a
  • In offline evaluation, it provides a map µ : Σ∗ →                 constant bound. The predicate   holds exactly
                                                                                                                   when the com-
    {0, e, 1}2 with µ(τ ) = v(τ ), the monitor verdict.               parison holds, P (s, a, c) = θ(s, a) ▷◁ c , where [·] is the
                    Temporal Logic (ALTLf )                                      5    The ContrAgent Framework
          operators G F X U lift predicates over the trajectory
         ¬Call(refund) U Call(approve) ∧ G Call(refund) →
                                                    
                                                                       Given the agent contracts, as defined in §4, ContrAgent pro-
                   Num(refund, amount)     ≤     42                    ceeds in two stages. In the offline stage (§5.1), it abstracts
                        Interaction Predicates V                       requirement artifacts into contracts and translates each con-
      Structural Predicates               Numeric Predicates           tract into a deterministic monitor, the DFA associated with
      presence or pattern match          threshold over accumulators   its ALTLf formula. In the online stage (§5.2), it supervises
        Call(refund) = ⊤                  Cnt(refund) = 3 ≤ 5          the agent by advancing every monitor over the tool-call trace
     Match(account, appr) = ⊤             Tok = 1200 ≤ 2000            and gating each call on the joint verdict (Problem 1).
        Call(approve) = ⊤                  amount = 50 > 42
                          extract / accumulate
          tool-call event a = (refund, {amount: 50, . . . })
                                                                       5.1   Contract Compilation
                                                                       Contract compilation extracts contracts from requirement ar-
Figure 2: One tool-call event grounded into structural and             tifacts (e.g., natural language, policy documents, recorded
numeric predicates, then lifted by the ALTLf layer.                    traces) into ALTLf formulas over the interaction predicates
                                                                       of §4, then compiles them into DFAs (Figure 3). The two
                                                                       steps are described next.
Iverson bracket, as in Cnt(T ) ≤ N . The monitor maintains
each accumulated quantity in a counter, one entry of the               Contract formulation. Besides manually written ALTLf
vector ρ of Def. 1, updated deterministically at each event.           contracts, we support translating natural-language require-
Such arithmetic-constraint atoms are what lift a contract’s            ments and extracting rules from policy documents. Following
logic from propositional LTLf to its arithmetic extension              a lift-then-ground decomposition (Liu et al. 2023), the LLM
ALTLf (Felli et al. 2023).                                             first lifts each utterance to an ALTLf formula with place-
  With the LTLf operators, we use interaction predicates to            holder leaves, and a deterministic step then grounds those
define agent contracts for trajectory supervision as follows.          placeholders to interaction predicates from Table 1, yielding
                                                                       the closed formula. The LLM thus fills templates over the
Definition 4 (Agent Contract) An agent contract is a triple            fixed vocabulary of Table 1 (Wang et al. 2023) with a few
C = (V, φA , φG ), where:                                              prompt examples. Each formula is translated back to natural
1. V = Vag ∪ Venv is a finite set of interaction predicates            language for human review (Cosler et al. 2023).
   (Def. 3), the AP of the contract’s formulas, where Vag
   collects the predicates decided by the agent’s own actions          Automaton construction. By the standard LTLf -to-DFA
   and Venv those decided by its environment.                          construction (De Giacomo and Vardi 2013), every contract
                                                                       formula over V compiles to a DFA whose alphabet is the
2. The assumption φA is an ALTLf formula over Venv , and               set 2V of predicate valuations. The DFA reads a trace one
   the guarantee φG is an ALTLf formula over V , both                  event at a time, taking a transition on the predicate valua-
   according to the grammar of §3.                                     tion at that event, and accepts exactly the finite traces that
   The partition of V mirrors the distinction between con-             satisfy the formula. We call grounding the deterministic step
trolled and uncontrolled variables in contract-based de-               that evaluates each predicate on the current event and the
sign (Benveniste et al. 2008). For example, Call, ArgHas, and          counters, producing the valuation read by the DFA. For a
Cnt track the tool calls that the agent itself issues (Def. 1),        numeric predicate, grounding evaluates the arithmetic con-
their arguments, and the counts derived from them, so they             straint θ(s, a) ▷◁ c against the session’s counters, and the
belong to Vag . OutHas, In, and Perm track tool results, user          DFA construction stays standard. The counter state is read
input, and granted permissions, so they belong to Venv . The           only during grounding and is not encoded in the DFA, which
actions of other agents also belong to the environment. Se-            keeps it finite. A contract carries two such formulas, the as-
mantically, an agent’s session satisfies the contract when its         sumption φA and the guarantee φG , so each compiles to its
trace satisfies φA → φG , with (φA , φG ) instantiating the            own DFA. We store the two DFAs as one checker corre-
pair (A, G) of Def. 2. Such contracts capture a wide range             sponding to the contract for agent supervision.
of trajectory properties over the tool-call interface, including
order-, history-, and count-dependent ones (Appendix B).               Contract library. The compiled checkers form a contract
                                                                       library that ContrAgent loads at runtime. Because a contract
Example 1 Consider a contract whose guarantee, shown                   is written over interaction predicates rather than any model’s
in Figure 2, is φG = ¬Call(refund) U Call(approve)         ∧          internals, the library is portable: the same checkers apply
G Call(refund) → Num(refund, amount) ≤ 42 , where                      unchanged across agents and LLM models that share a tool
$42 is the approved amount recorded by an earlier approve              interface, so a domain’s policies transfer between models.
call. Take the call event a = (refund, {amount: 50, . . . }).          For each contract, ContrAgent first checks consistency and
The structural predicates hold, Call(refund) = ⊤ and                   compatibility, and alsoVchecks the loaded library is conflict-
Match(account, appr) = ⊤, since approve was called                     free: the conjunction i (Ai ∧ Gi ) of its ALTLf formulas
first and the account matches. The numeric predicate                   is satisfiable. When it is not, we extract a minimal unsatisfi-
Num(refund, amount) ≤ 42 evaluates to ⊥ at amount =                    able core (Roveri et al. 2024; Ielo et al. 2026) to locate the
50, so the guarantee, and with it the contract, falls to FAIL.         contracts to repair.
Figure 3: The ContrAgent framework: authoring inputs compile once into a contract checker (top), read online to block the first
violating call (bottom left) and offline to score a recorded trace (bottom right).


5.2   Contract-Based Supervision                                      DFAs in full, ContrAgent keeps a residual formula and pro-
At each event, ContrAgent evaluates every interaction pred-           gresses it one event at a time (Roşu and Havelund 2005),
icate and advances each loaded contract’s two DFAs on the             so the per-event cost is O(|C|), where C is the set of loaded
resulting valuation. The two runs decide the contract’s value         contracts, independent of the trace length. Supervision thus
in Def. 2, and the values of all loaded contracts give the            scales to long horizons.
verdict v(τ ) of Problem 1.                                              When the blocked event is a call, the enforcement action
   Because each contract is a single (A, G) pair checked inde-        is decided by the strategy carried by the violated contract:
pendently, a violation is fully traceable: it names the contract      block the call (the default), redirect it to a safe alternative,
that violated and the event that triggered it, so an operator         or escalate to a human. The outcome returns to the model as
can tell whether the fault lies in the agent flow, in its environ-    a structured message: the identifier of the contract involved,
ment, or in a contract that is too restrictive, and repair the last   a short explanation, and, where it applies, the suggested re-
by relaxing the guarantee or weakening the assumption. This           placement or required next action, so the agent can steer
modularity also lets the system enforce multiple policies at          its trajectory back into the safe region. For example, a con-
once, without merging them into a monolithic formula.                 tract that forbids issuing a refund before approval can return
                                                                      a message like “the action issue_refund was rejected:
Runtime enforcement. At runtime, ContrAgent realizes                  call check_policy first”.
the enforcement map σ of Problem 1. As shown in Figure 3,                Prompting for a requested action lets ContrAgent act
before the tool executes, it advances every loaded contract           proactively, on a satisfied trigger rather than on a violation.
and returns block at the first event whose verdict is not (e, e).     Consider a prescriptive guarantee G(trig → X tool ); when
Every event is checked when it enters the trace and before            the trigger trig is satisfied and gets pass, a feedback message
it takes effect (Def. 1), so the verdict is computed before           can ask the agent to call the required tool next. An unbounded
a call executes and before an incoming event reaches the              liveness guarantee G(trig → F resp) cannot be refuted by
agent. A call that would falsify a guarantee is rejected, and         any finite prefix: after trig is satisfied, it stays pending until
a return or input event that would falsify an assumption is           resp occurs. At the end of the agent session, ContrAgent
suppressed. Neither event is recorded, so the session contin-         surfaces every still-pending guarantee as a feedback mes-
ues from the last prefix whose verdict was (e, e). The first          sage asking the agent to perform resp, and a guarantee left
keeps the agent a valid implementation of the contract and            unsatisfied collapses to FAIL.
the second keeps its environment a valid environment, as in
bidirectional runtime enforcement (Aceto et al. 2021). The            Offline evaluation. Contracts also serve as a deterministic
check is incremental: rather than synthesizing each contract’s        evaluation engine for recorded traces: µ : Σ∗ → {0, e, 1}2
of Problem 1, as shown in Figure 3. ContrAgent replays              domain (Su./Sf.)                 base        prompt             LLM-grd        ContrAgent
a recorded trace and returns its end-of-trace verdict µ(τ ) =       bank                             70/65        58/100             42/100          70/100
v(τ ) instead of gating actions, one value for the agent and one    DMV                             100/60         72/98             20/100         100/100
for its environment. The difference from enforcement is that        healthcare                      90/48         52/95              20/100          83/100
the trace is fixed, so there is no intervention; and because each   hotel                            100/0         30/98             15/100         100/100
vi depends only on the trace, the offline replay and the online     library                          80/25         48/95              22/98          80/100
monitor traverse the same states and agree on the verdict at        university                       100/8         92/82              33/88          100/83
every prefix. When many traces are checked against the same         online mkt.                     100/20         92/90              15/98         100/100
contracts, the DFAs are built once and reused, turning each         mean                             91/32         64/94              24/98           90/98
event into a single table lookup (O(1)). Offline evaluation is      avg. runtime                    1.96 s       +0.905 s            +1.34 s        +0.135 s
thus deterministic and reproducible: the same trace always
yields the same verdict and per-contract attribution, not a         Table 2: SOPBench results (gemini-2.5-flash, 40
single pass/fail rate.                                              tasks/domain); each cell is success (Su.) / safety (Sf.) %. avg.
                                                                    runtime: the base cell is its median runtime per task; the
                        6    Evaluation                             other cells are the median extra time over base.
                        1
Our implementation is in Python 3.12; it exports contract
libraries to CHASE (Nuzzo et al. 2018) for design-time                                       base         prompt            LLM-grd            ContrAgent
contract analysis, and uses mus2muc (Ielo et al. 2026) for                100
conflict-core extraction and Z3 (de Moura and Bjørner 2008)




                                                                     success %
                                                                                 75




                                                                                                                         safety %
for the numeric consistency check. The contract library is
built with an LLM following the formulation pipeline of                          50
§5.1, over the interaction predicates of Table 1. Integration
                                                                                 25
hooks intercept each event and ground it deterministically
through pattern matches and counter updates. Latency mea-                        0
surements reported below were taken on an Apple M4 Pro                                1–2    3–4    5–6    7–9     10+          1–2    3–4   5–6     7–9    10+

laptop (24 GB).                                                                             # SOP constraints                         # SOP constraints

Benchmarks. We evaluate ContrAgent on four bench-                   Figure 4: SOPBench success (left) and safety (right) vs. SOP
marks, each isolating one claim. The enforcement role is            constraint count, pooled over seven domains.
tested by SOPBench (Li et al. 2025) (§6.1) and Agent-
Dojo (Debenedetti et al. 2024) (§6.2); the evaluation role
by R-Judge (Yuan et al. 2024) (§6.3) and τ 2 -bench (Barres         permitted change to a target the benchmark’s outcome-based
et al. 2025) (§6.4).                                                scoring cannot distinguish from the forbidden one.
                                                                      The runtime cost of ContrAgent is lower than both prompt
6.1      Standard Operating Procedure Enforcement                   and LLM-guard, since it neither increases the prompt length
SOPBench (Li et al. 2025) evaluates whether a language              nor calls a second model on every action. Each entry is a mean
agent follows an explicit standard operating procedure              over three seeded trials; ContrAgent’s enforcement is stable
(SOP) across seven customer-service domains (bank, DMV,             across trials, with per-domain deviation ≤ 0.4 percentage
healthcare, hotel, library, university, online market),             points (pp), versus 2 to 4 pp for the model-driven conditions.
where each task provides a constraint graph, numeric thresh-        Model-agnostic supervision. With the same contract li-
olds, an initial database, and a label indicating whether the       brary, on gemini-2.5-flash-lite, where the un-
policy permits the goal. We compared ContrAgent with three          guarded base stays at 27%, prompt’s mean safety collapses
baselines: (1) the base model with no SOP, (2) the base model       from 94% to 45%, whereas ContrAgent’s enforced safety
prompted with the SOP, and (3) a second LLM that judges             is unchanged at 98%, because the verdict does not depend
each call against the SOP. We report success and safety met-        on the agent’s model. Moreover, replaying the same con-
rics, representing goal completion on tasks the SOP permits         tract library over SOPBench traces from 23 base models, the
and correct blocking on tasks the SOP forbids, respectively.        false-positive rate on safe traces stays below 1% for 19 of 23
   We build each domain’s agent contracts from its public           models (max 4.5%, Llama-3.1-8B), even as the per-model
SOP, compiling the SOP’s gate/chain tree. As shown in Ta-           violation rate varies widely with capability (Appendix C).
ble 2, ContrAgent enforcement holds success at the base level
while raising safety from 32% to 98%, above prompt’s 94%.           SOP constraint scaling. Binning tasks by the number of
Prompting and LLM-guard also achieve high safety (94%               SOP constraints (which run from 1 to 17; pooled over the
and 98%), but reduce mean success to 64% and 24%, respec-           seven domains) exposes the success/safety tradeoff that a sin-
tively, because of over-blocking. Both residual gaps trace to       gle strategy hides. As shown in Figure 4, with the number of
the agent rather than the enforcement layer: in healthcare          constraints increasing, prompting increasingly over-refuses:
it fails to retry after a block, and in university it makes a       its success on permitted tasks collapses from 87% to 18%
                                                                    in the 10+ bin, while the unguarded base’s safety collapses
   1
       https://github.com/yfxiao16/ContrAgent                       from 79% to 0%. The LLM-guard keeps safety high, but
                          base       no detector   trace-learned                                            pass4       joint4
           gpt-4-0125                              llama-3.3-70b                                                   Retail
    claude-3.5-sonnet                           gemini-1.5-flash                                  Claude 3.7
                                                                                                     GPT-4.1
               gpt-4o                              claude-3-opus                                GPT-4.1-mini
          gpt-4-turbo                              gpt-3.5-turbo                                     o4-mini
       gemini-1.5-pro                             claude-3-haiku
                                                                                                                   Airline
                                                                                                  Claude 3.7
          gpt-4o-mini                          claude-3.7-sonnet                                     GPT-4.1
      claude-3-sonnet                             command-r-plus                                GPT-4.1-mini
                                                                                                     o4-mini
          llama-3-70b                         gemini-1.5-flash-2                                                   Telecom
     gemini-1.5-pro-2                                  command-r                                  Claude 3.7
   gemini-2-flash-exp                          meta-secalign-70b                                     GPT-4.1
                                                                                                GPT-4.1-mini
       gemini-2-flash                        claude-3.5-sonnet-2                                     o4-mini

                        0.1      1     10                           0.1   1     10                             0       20        40   60
                   Prompt-injection attack-success rate (%, log scale)                            Task-level success rate (%, k = 4)

Figure 5: Indirect prompt-injection prevention across 22 LLMs on AgentDojo; left            Figure 6: The τ 2 -bench procedural reliabil-
and right are the higher- and lower-ASR halves.                                             ity across three domains and four models.


with steep success reduction. ContrAgent holds success at                 Defense               Type          ASR Utility Overhead
77% or above and safety at 89% or above across all bins,                  No defense            raw agent   47.7% 72.6%          0
and the gap widens as the constraint count grows. Exact per-              spotlighting          prompt-side 41.7% 75.0%     prompt
bin values and the weak-model robustness breakdown are in                 repeat_user_prompt    prompt-side 27.8% 85.5%     prompt
Appendix D.                                                               ContrAgent (ND)       data-flow   11.1% 71.8%    0.16 ms
                                                                          pi_detector           classifier  7.95% 41.9%    ∼50 ms
6.2   Indirect Prompt Injection Prevention                                tool_filter           LLM prune 6.84% 71.8% ∼500 ms
AgentDojo (Debenedetti et al. 2024) embeds attacker text                  LlamaFirewall         guardrail   1.75%     n/a ∼100 ms
inside tool outputs (email bodies, calendar entries, search               ContrAgent (TL)       data-flow   0.79% 72.6%    0.16 ms
results) and measures whether the agent is steered into an
unsafe action. ContrAgent prevents indirect prompt injection              Table 3: AgentDojo defenses on gpt-4o (ND: no detector,
by filtering tool outputs and blocking any subsequent call that           TL: trace-learned).
would violate the contract, regardless of whether the agent
was tricked into issuing it. The contract library is built from
the task and environment specifications of AgentDojo’s four               ity value is computed from the published runs. Utility is
suites, without knowledge of the attacks. It tags any value               the fraction of injection-free tasks completed. Overhead is
carried in by a tool output as untrusted, and blocks a side-              the per-call runtime added by a defense, and prompt-side
effecting call whose target is both untrusted-introduced and              defenses add prompt text rather than a call. ContrAgent re-
outside the task’s legitimate set.                                        plays the recorded runs, so its utility cannot exceed that of
   Figure 5 reports three results per model. The baseline re-             the undefended agent. With no detector, ContrAgent low-
sults are from AgentDojo’s published numbers (Debenedetti                 ers the ASR from 47.7% to 11.1% and completes 71.8% of
et al. 2024). We call no-detector the setting in which no                 the injection-free tasks, one task fewer than the undefended
component flags the injected text, so that a value counts as              agent. The classifier reaches 7.95% but completes 41.9% of
untrusted whenever a tool output introduces it and the user               the tasks. The trace-learned variant reaches 0.79% at the util-
has not named it. In this setting, the library reduces the pooled         ity of the undefended agent. Both variants add 0.16 ms per
attack success rate (ASR) from 18.0% to 5.3% at 0.8% util-                call, against 50 to 500 ms for the classifier and the LLM filter,
ity false positive (FP). Contracts can also be mined from the             and run no model. The per-workload latency breakdown is
recorded traces of the attacks themselves (attacker recipients,           in Appendix E.
unsafe actions, and the injected text as the untrusted source),
which we call trace-learned contracts. This lowers the pooled             6.3   Agent Safety Risk Evaluation
ASR to 1.7% at 0.3% FP. The attacks ContrAgent misses                     R-Judge (Yuan et al. 2024) tests whether an evaluator can
fall into two kinds. Most (82%) issue no malicious tool call              detect unsafe agent behavior post hoc across ten operational
at all, e.g., denial-of-service injections that only divert the           risk types in 571 multi-turn agent records (301 unsafe / 270
agent or text-response attacks answered in the agent’s own                safe). Contracts come from R-Judge’s risk taxonomy, a policy
reply, outside what a tool-call shield can do. The remaining              document (§5.1). ContrAgent reaches an average F1 score of
18% are prompt injections that steer the agent into a tool call           91.8% (97.0% precision, 87.0% recall) across multiple trials.
whose arguments are themselves legitimate values, leaving                 This exceeds GPT-4o (74.4%) and the R-Judge human base-
the deterministic guard no untrusted target to flag.                      line (≈ 89%). AgentAuditor (Luo et al. 2025) outperforms
   Table 3 compares ContrAgent with the defenses bundled                  our method at the cost of a Gemini-2 judge with retrieval over
with AgentDojo on gpt-4o under its main injection attack.                 an experiential memory. The records we miss are semantic
Only the ContrAgent rows are measured here; the baseline                  rather than procedural, outside what a deterministic tool-call
rates are AgentDojo’s published numbers, and every util-                  check can decide.
6.4   Procedural Violation and Outcome Scoring                      Bauer, A.; Leucker, M.; and Schallhart, C. 2006. Monitoring
 2
τ -bench (Barres et al. 2025) runs customer-service agents          of Real-Time Properties. In Proc. Foundations of Software
through multi-turn dual-control conversations against a writ-       Technology and Theoretical Computer Science (FSTTCS),
ten policy document in three domains. Its native passk met-         volume 4337 of Lecture Notes in Computer Science, 260–
ric is outcome-only (final database state). AgentPex (Sharma,       272. Springer.
Barke, and Zorn 2026) showed 83% of reward-1.0 Claude               Bauer, A.; Leucker, M.; and Schallhart, C. 2011. Runtime
traces still violate a procedural rule. With contract libraries     Verification for LTL and TLTL. ACM Transactions on Soft-
built from the policy documents, ContrAgent measures pro-           ware Engineering and Methodology (TOSEM), 20(4): 14:1–
cedural compliance deterministically, while LLM judges can          14:64.
only approximate it. We report a jointk metric that com-            Benveniste, A.; Caillaud, B.; Ferrari, A.; Mangeruca, L.; et al.
bines outcome and zero contract violations across k retries.        2008. Multiple Viewpoint Contract-Based Specification and
Figure 6 exposes the gap this creates: across the 4,464-trace       Design. In Proc. Formal Methods for Components and Ob-
matrix Claude 3.7 reaches an outcome pass4 of 25–60%                jects (FMCO), volume 5382 of LNCS, 200–225. Springer.
yet a joint4 of 0% in all three domains, i.e., no task is           Benveniste, A.; Caillaud, B.; Nickovic, D.; Passerone, R.;
completed reliably without at least one procedural violation,       et al. 2018. Contracts for System Design. Foundations and
a form of reward hacking. Per-cell values for every domain          Trends in Electronic Design Automation, 12(2–3): 124–400.
and model are in Appendix F.
                                                                    Bhardwaj, V. P. 2026. Agent Behavioral Contracts: For-
Limitations. ContrAgent enforces only what the tool-call            mal Specification and Runtime Enforcement for Reliable
structure exposes, and free-form semantic harms need a sepa-        Autonomous AI Agents. ArXiv preprint arXiv:2602.22302.
rate content-level check. In this paper, the library is inspected   Chase, H. 2022. LangChain: Building Applications with
by humans before use; autoformalization of natural-language         LLMs through Composability. Open-source software.
policies is out of the scope of this work and left as a future      Chen, H.; and Goldfarb-Tarrant, S. 2025. Safer or Luckier?
direction. The counters that ground numeric predicates (§4)         LLMs as Safety Evaluators Are Not Robust to Artifacts. In
trust the framework to report events faithfully, and defending      Proc. Annual Meeting of the Association for Computational
this observation channel itself is beyond our scope.                Linguistics (ACL), 19750–19766.
                                                                    Chen, Z.; Kang, M.; and Li, B. 2025. ShieldAgent: Shielding
                      7    Conclusion                               Agents via Verifiable Safety Policy Reasoning. In Proc.
We presented ContrAgent, a contract-based framework that            International Conference on Machine Learning (ICML).
formalizes trajectory-level specifications of large language        Cosler, M.; Hahn, C.; Mendoza, D.; Schmitt, F.; et al. 2023.
model (LLM) agents as assume-guarantee (A/G) contracts              nl2spec: Interactively Translating Unstructured Natural Lan-
over checkable tool-call predicates, expressed in arithmetic        guage to Temporal Logics with Large Language Models. In
linear temporal logic on finite traces (ALTLf ), and com-           Proc. Computer Aided Verification (CAV), volume 13965 of
piles each into a deterministic finite automaton (DFA) for          Lecture Notes in Computer Science, 383–396. Springer.
online enforcement and offline evaluation. The contract li-         Costa, M.; Köpf, B.; Kolluri, A.; Paverd, A.; et al. 2025.
brary acts as a model-agnostic knowledge base of agent              Securing AI Agents with Information-Flow Control. ArXiv
policies. We illustrated the effectiveness of our approach          preprint arXiv:2505.23643.
on four benchmarks spanning both roles, where ContrAgent
matches LLM-judge and guardrail baselines while producing           De Giacomo, G.; and Vardi, M. Y. 2013. Linear Temporal
deterministic, reproducible verdicts at orders of magnitude         Logic and Linear Dynamic Logic on Finite Traces. In Proc.
lower per-call latency. Future work includes compiling con-         International Joint Conference on Artificial Intelligence (IJ-
tracts into reward machines for post-training and constrained       CAI), 854–860.
decoding, and investigating contract-based decomposition            de Moura, L.; and Bjørner, N. 2008. Z3: An Efficient SMT
mechanisms for multi-agent systems.                                 Solver. In Proc. Tools and Algorithms for the Construction
                                                                    and Analysis of Systems (TACAS), volume 4963 of Lecture
                          References                                Notes in Computer Science, 337–340. Springer.
                                                                    Debenedetti, E.; Shumailov, I.; Fan, T.; Hayes, J.; et al. 2025.
Aceto, L.; Cassar, I.; Francalanza, A.; and Ingólfsdóttir, A.
                                                                    Defeating Prompt Injections by Design. ArXiv preprint
2021. On Bidirectional Runtime Enforcement. In Proc. For-
                                                                    arXiv:2503.18813.
mal Techniques for Distributed Objects, Components, and
Systems (FORTE), LNCS. Springer.                                    Debenedetti, E.; Zhang, J.; Balunović, M.; Beurer-Kellner,
                                                                    L.; et al. 2024. AgentDojo: A Dynamic Environment to Eval-
Anthropic. 2024. Introducing the Model Context Protocol.            uate Prompt Injection Attacks and Defenses for LLM Agents.
Anthropic; open protocol specification.                             In Proc. Conference on Neural Information Processing Sys-
Baier, C.; and Katoen, J.-P. 2008. Principles of Model Check-       tems (NeurIPS), Datasets and Benchmarks Track.
ing. Cambridge, MA: MIT Press.                                      Felli, P.; Montali, M.; Patrizi, F.; and Winkler, S. 2023. Mon-
Barres, V.; Dong, H.; Ray, S.; Si, X.; et al. 2025. τ 2 -Bench:     itoring Arithmetic Temporal Properties on Finite Traces. In
Evaluating Conversational Agents in a Dual-Control Envi-            Proc. AAAI Conference on Artificial Intelligence (AAAI),
ronment. ArXiv preprint arXiv:2506.07982.                           6346–6354. AAAI Press.
Geatti, L.; Gianola, A.; and Gigante, N. 2022. Linear Tem-          Pnueli, A. 1977. The Temporal Logic of Programs. In Proc.
poral Logic Modulo Theories over Finite Traces. In Proc.            Annual Symposium on Foundations of Computer Science
International Joint Conference on Artificial Intelligence (IJ-      (FOCS), 46–57. IEEE.
CAI), 2641–2647. ijcai.org.                                         Roşu, G.; and Havelund, K. 2005. Rewriting-Based Tech-
Ielo, A.; Mazzotta, G.; Peñaloza, R.; and Ricca, F. 2026.           niques for Runtime Verification. Automated Software Engi-
Enumerating Minimal Unsatisfiable Cores of LTLf Formu-              neering, 12(2): 151–197.
lae. In Proc. AAAI Conference on Artificial Intelligence            Roveri, M.; Di Ciccio, C.; Di Francescomarino, C.; and Ghi-
(AAAI), 19160–19168. AAAI Press.                                    dini, C. 2024. Computing Unsatisfiable Cores for LTLf Spec-
Inan, H.; Upasani, K.; Chi, J.; Rungta, R.; et al. 2023. Llama      ifications. Journal of Artificial Intelligence Research, 80:
Guard: LLM-based Input-Output Safeguard for Human-AI                517–558.
Conversations. ArXiv preprint arXiv:2312.06674.                     Schneider, F. B. 2000. Enforceable Security Policies. ACM
Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; et al. 2024.         Transactions on Information and System Security (TISSEC),
SWE-bench: Can Language Models Resolve Real-World                   3(1): 30–50.
GitHub Issues? In Proc. International Conference on Learn-          Sharma, R. K.; Barke, S.; and Zorn, B. 2026. Willful Disobe-
ing Representations (ICLR).                                         dience: Automatically Detecting Failures in Agentic Traces.
Kamath, A.; Zhang, S.; Xu, C.; Ugare, S.; et al. 2025. Enforc-      In Proc. ACM Conference on AI and Agentic Systems (CAIS).
ing Temporal Constraints for LLM Agents. ArXiv preprint             Shi, T.; He, J.; Wang, Z.; Li, H.; et al. 2025. Progent: Se-
arXiv:2512.23738.                                                   curing AI Agents with Privilege Control. ArXiv preprint
Leucker, M.; and Schallhart, C. 2009. A Brief Account of            arXiv:2504.11703.
Runtime Verification. The Journal of Logic and Algebraic            Sotiropoulos, J.; Del Rosario, R. F.; Kokuykin, E.; Oakley,
Programming, 78(5): 293–303.                                        H.; et al. 2025. OWASP Top 10 for LLM Apps & Gen AI
Li, Z.; Huang, S.; Wang, J.; Zhang, N.; et al. 2025. SOP-           Agentic Security Initiative. OWASP Foundation.
Bench: Evaluating Language Agents at Following Stan-                Wang, B.; Wang, Z.; Wang, X.; Cao, Y.; et al. 2023. Grammar
dard Operating Procedures and Constraints. ArXiv preprint           Prompting for Domain-Specific Language Generation with
arXiv:2503.08669.                                                   Large Language Models. In Proc. Conference on Neural
Liu, J. X.; Yang, Z.; Idrees, I.; Liang, S.; et al. 2023. Ground-   Information Processing Systems (NeurIPS).
ing Complex Natural Language Commands for Temporal                  Wang, H.; Poskitt, C. M.; and Sun, J. 2026. AgentSpec:
Tasks in Unseen Environments. In Proc. Conference on                Customizable Runtime Enforcement for Safe and Reliable
Robot Learning (CoRL). System name “Lang2LTL”.                      LLM Agents. In Proc. IEEE/ACM International Conference
Luo, H.; Dai, S.; Ni, C.; Li, X.; et al. 2025. AgentAudi-           on Software Engineering (ICSE).
tor: Human-Level Safety and Security Evaluation for LLM             Wang, H.; Poskitt, C. M.; Wei, J.; and Sun, J. 2025.
Agents. In Proc. Conference on Neural Information Process-          ProbGuard: Proactive Runtime Monitoring for LLM Agent
ing Systems (NeurIPS).                                              Safety via Probabilistic Prediction.   ArXiv preprint
Miculicich, L.; Parmar, M.; Palangi, H.; Dvijotham,                 arXiv:2508.00500.
K. D.; et al. 2025. VeriGuard: Enhancing LLM Agent                  Wen, X.; Mo, W. J.; Xie, Y.; Qi, P.; et al. 2026. Learning
Safety via Verified Code Generation. ArXiv preprint                 Efficient Guardrails for Compliance. In Proc. International
arXiv:2510.05156.                                                   Conference on Machine Learning (ICML).
Nous Research. 2026. Hermes Agent: A Self-Improving                 Wu, Q.; Bansal, G.; Zhang, J.; Wu, Y.; et al. 2024. Auto-
Open-Source Agent Framework. Open-source software.                  Gen: Enabling Next-Gen LLM Applications via Multi-Agent
Nuzzo, P.; Lora, M.; Feldman, Y. A.; and Sangiovanni-               Conversation. In Proc. Conference on Language Modeling
Vincentelli, A. L. 2018. CHASE: Contract-based require-             (COLM).
ment engineering for cyber-physical system design. In Proc.         Xiao, Y.; Lutz, C. D.; Castillo-Effen, M.; and Nuzzo, P. 2026.
Design, Automation & Test in Europe Conference (DATE),              Contract-Based Consistency and Availability Analysis for
839–844.                                                            Distributed Cyber-Physical Systems. In Proc. ACM/IEEE
Nuzzo, P.; Sangiovanni-Vincentelli, A. L.; Bresolin, D.;            International Conference on Formal Methods and Models
Geretti, L.; et al. 2015. A Platform-Based Design Method-           for System Design (MEMOCODE). To appear.
ology with Contracts and Related Tools for the Design of            Xiao, Y.; and Nuzzo, P. 2026. Contract-Based Architec-
Cyber-Physical Systems. Proceedings of the IEEE, 103(11):           ture Exploration of Cyber-Physical Systems via Satisfiability
2104–2132.                                                          Modulo Convex Programming. In Proc. Design, Automation
OpenClaw Project. 2026. OpenClaw: An Open-Source Per-               & Test in Europe Conference (DATE), 1–7. IEEE.
sonal AI Agent. Open-source software.                               Xiao, Y.; Oh, C.; Lora, M.; and Nuzzo, P. 2024. Efficient
Palumbo, N.; Choudhary, S.; Choi, J.; Amir, G.; et al. 2026.        Exploration of Cyber-Physical System Architectures Using
Formal Policy Enforcement for Real-World Agentic Systems.           Contracts and Subgraph Isomorphism. In Proc. Design, Au-
ArXiv preprint arXiv:2602.16708.                                    tomation & Test in Europe Conference (DATE).
Xu, H.; Li, C.; Ma, X.; Ou, X.; et al. 2026. The Evolution of
Tool Use in LLM Agents: From Single-Tool Call to Multi-
Tool Orchestration. ArXiv preprint arXiv:2603.22862.
Yang, Z.; Raman, S. S.; Shah, A.; and Tellex, S. 2024. Plug
in the Safety Chip: Enforcing Constraints for LLM-driven
Robot Agents. In Proc. IEEE International Conference on
Robotics and Automation (ICRA).
Yao, S.; Zhao, J.; Yu, D.; Du, N.; et al. 2023. ReAct: Syn-
ergizing Reasoning and Acting in Language Models. In
Proc. International Conference on Learning Representations
(ICLR).
Yuan, T.; He, Z.; Dong, L.; Wang, Y.; et al. 2024. R-Judge:
Benchmarking Safety Risk Awareness for LLM Agents. In
Proc. Findings of the Association for Computational Lin-
guistics: EMNLP.
Zheng, L.; Chiang, W.-L.; Sheng, Y.; Zhuang, S.; et al.
2023. Judging LLM-as-a-Judge with MT-Bench and Chatbot
Arena. In Proc. Conference on Neural Information Process-
ing Systems (NeurIPS), Datasets and Benchmarks Track.
Zhong, P. Y.; Chen, S.; Wang, R.; McCall, M.; et al. 2025.
RTBAS: Defending LLM Agents Against Prompt Injection
and Privacy Leakage. ArXiv preprint arXiv:2502.08966.
Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; et al. 2024. We-
bArena: A Realistic Web Environment for Building Au-
tonomous Agents. In Proc. International Conference on
Learning Representations (ICLR).
                                            A     Full Interaction-Predicate Catalogue
Table 4 lists the complete interaction-predicate vocabulary of ContrAgent. The main text (Table 1) shows the representative
subset that the examples and experiments use; the remaining predicates extend the same two families to model outputs, response
lengths, and delegation depth. Since(e) reads a wall-clock timestamp the framework records with each event; time is an
implementation-level extension and does not enter the formal model of Def. 1.

Type          Predicate         Meaning
              Call(T )          tool T is invoked
              ArgHas(T, f, p)   argument f of T matches pattern p
              Path(T, P )       T ’s file paths lie within P
              Subset(f, S)      values in field f lie within set S
 Structural




              OutHas(T, p)      result of T matches pattern p
              Said(p), In(p)    model output / input matches pattern p
              Match(f, k)       argument field f equals context value k
              Ctx(k, v)         context key k holds value v
              Flow(s, d)        data from source s reaches sink d
              Has(f )           a produced value contains field f
              Perm(P )          caller holds permission P
              Cnt(T )           current number of T calls
              Run(T )           length of the current consecutive run of T
              Num(T, f )        numeric value of argument field f
              Len(T, f )        character length of argument field f
 Numeric




              InLen             character length of the model input
              Words, Chars      word / character length of the response
              Tok               cumulative tokens consumed
              Depth             agent-delegation depth
              Since(e)          time elapsed since event e

Table 4: Complete interaction-predicate vocabulary of ContrAgent. T is a tool, f an argument field, p a regular-expression or
literal-value pattern, P a path or permission set, S a value set, s, d argument or result fields as source and sink, and k, v a context
key/value.


                                                     B     Temporal Expressiveness
Table 5 lists four temporal property classes that distinguish ContrAgent’s trajectory-level enforcement from a stateless, single-
call guard (§4). For each we construct a minimal violating trace in which every individual call is locally legitimate (the same calls
occur in a compliant trace), so the violation is purely temporal. ContrAgent’s DFA catches all four and raises no false positive
on the compliant control; a stateless guard catches none by construction. The fourth class, “after reading untrusted content,
a side-effecting send requires reconfirmation,” is exactly the indirect-prompt-injection contract that drives the AgentDojo and
R-Judge results (§6.2, §6.3).

                   Property (NL)                    ALTLf                                         stateless ContrAgent
                   Refund only after a policy check (¬ Call(r) U Call(c)) ∨ G ¬ Call(r)             miss      catch
                   (order)
                   After the AML check, the file is G(Call(a) → G ¬ Call(m))                        miss       catch
                   immutable (history)
                   At most two transfers (count)    G(Cnt(t) ≤ 2)                                   miss       catch
                   Send needs reconfirm after un- (¬ Call(s) U Call(k)) ∨ G ¬ Call(s)               miss       catch
                   trusted read (injection)

Table 5: Temporal expressiveness: each violating trace’s every call is individually legitimate, so the violation is detectable only
from order, history, or count. A stateless guard catches none; ContrAgent’s DFA catches all four, clean on the compliant control.
Tool names in the formulas are abbreviated per row.
                          C    Per-Model Violation Profiles and Grounding Ablation
This appendix expands the grounding and per-model robustness summary in §6.1.
The residual gap is coverage, not grounding. SOPBench’s decisive predicates are structural (a tool was called, a call returned
success), read directly off the trace, so grounding is exact by construction. We confirm this with an oracle ablation over 5,435
recorded unsafe traces: perfecting the single most influential AP, the goal action’s success flag, moves pooled detection recall
from 75.1% to 75.4% (a +0.3 pp delta). There is essentially no grounding error to remove; the residual ∼ 25% is contract
coverage (§6.1). Oracle grounding thus matters for content and semantic sensors (e.g., R-Judge’s semantic residual cases, §6.3),
not for structural enforcement.
Per-model violation profiles. Table 6 profiles the contract library across base models on their recorded traces. The violation
rate tracks capability: the strongest models almost never complete a forbidden action (gpt-5: 14 unsafe traces in the sample;
o1: 3), whereas mid-tier models do so routinely (Claude-3.5: 417), a direct, model-specific “willful-disobedience” measure.
ContrAgent’s behaviour on those violations stays stable regardless: recall sits in the 54.7–100% band and the dominant family
of caught violations is value/threshold for every model (74–100% of its catches), at < 1% false positives, so the supervision
behavior does not depend on the backbone model.

                                        base model                  recall FPR nuns
                                        gpt-5                      100.0% 0.0%  14
                                        o1                         100.0% 0.0%    3
                                        gpt-5-mini                  92.9% 0.0%  42
                                        gemini-2.0-flash            81.0% 0.5% 420
                                        llama3.1-8b-instruct        79.3% 4.5% 416
                                        gemini-2.0-flash-thinking   79.2% 0.2% 101
                                        llama3.1-70b-instruct       79.0% 1.4% 415
                                        qwen2.5-72b-instruct        78.4% 0.5% 398
                                        o4-mini                     78.0% 0.0%  41
                                        qwen2.5-7b-instruct         77.9% 2.5% 408
                                        gpt-4o-mini                 77.3% 2.9% 299
                                        gemini-1.5-pro              75.9% 0.7% 332
                                        qwen2.5-14b-instruct        75.8% 0.0% 372
                                        qwen2.5-32b-instruct        75.2% 0.2% 359
                                        claude-3.5-sonnet           74.3% 0.0% 417
                                        gpt-4o                      74.2% 0.0% 322
                                        claude-3.7-sonnet           71.7% 0.5% 240
                                        gpt-4.1-mini                66.4% 0.0% 220
                                        claude-3.7-sonnet-thinking 66.1% 0.0% 189
                                        gpt-4.1                     63.7% 0.0% 179
                                        o4-mini-high                61.2% 0.2%  80
                                        deepseek-r1                 56.2% 0.3%  73
                                        gemini-2.5-flash            54.7% 0.0%  95

Table 6: Per-model violation profiles on SOPBench recorded traces (deterministic, 0 LLM calls; all 23 base models). recall =
unsafe caught, FPR = safe wrongly blocked, nuns = sampled unsafe traces. FPR stays below 1% for 19 of 23 backbones (max
4.5%, llama3.1-8b).


                D    SOPBench Live Enforcement: Per-Constraint Scaling and Robustness
Table 7 gives the exact per-bin values plotted in Figure 4: SOPBench success (on permitted tasks) and safety (on forbidden
tasks) as a function of the number of SOP constraints, pooled over the seven domains, for the base, prompt, LLM-guard, and
ContrAgent-enforce conditions on gemini-2.5-flash. ContrAgent is the only condition that stays high on both axes across
the whole range: prompt’s success collapses from 87% to 18% as the policy grows, and the unguarded base’s safety collapses
from 79% to 0%, while ContrAgent-enforce holds success ≥ 77% and safety ≥ 89% throughout, with its safety matching or
exceeding prompt at every bin.
Robustness to a weaker base model. The weak-model result in §6.1 reports the mean over domains; the effect is consistent
across domains. On the weaker gemini-2.5-flash-lite agent, prompt’s mean safety falls from 94% to 45% (the agent
stops reliably reading and obeying the prompted SOP), whereas ContrAgent-enforce reproduces its strong-model safety (98%,
unchanged) because the monitor verdict is computed deterministically from the trace, not inferred by the agent. Success drops
for every condition under the weaker agent (enforce mean 90 → 68), confirming that success tracks model capability while
ContrAgent’s safety does not. This confirms the distinction between deterministic and probabilistic supervision. A prompted
SOP’s assurance degrades with the model that carries it, whereas a compiled contract’s does not.
                                       metric    condition     1–2   3–4     5–6   7–9   10+
                                                 base           93    82      84    90   100
                                                 prompt         87    62      73    48    18
                                       success
                                                 LLM-grd        68    26      12    12     6
                                                 ContrAgent     78    77      86    83   100
                                                 base           79    44      29    10     0
                                                 prompt        100    98      83    90    84
                                       safety
                                                 LLM-grd       100    98     100   100    96
                                                 ContrAgent    100    98     100    93    89

Table 7: Exact per-bin values for Figure 4: SOPBench success (permitted) and safety (forbidden) % vs. SOP constraint count,
pooled over the seven domains (gemini-2.5-flash). As the policy grows, prompt’s success and base’s safety both collapse;
ContrAgent-enforce stays high on both axes.


                                           E     Hot-Path Latency Breakdown
Table 8 gives the per-workload before-call latency of the online verifier.

                                       Workload                     C    p50 p95 p99
                                       Synthetic (1 contract)       1 0.0052    – 0.012
                                       SOPBench (per call) 38 to 65 0.097 0.171 0.272
                                       AgentDojo (per call)   8 to 14 0.162 0.620 0.933
                                       R-Judge (per record)         7 0.040 0.085 0.141
                                       τ 2 -bench (per call)     ∼53 0.828 1.500 1.889

Table 8: Hot-path before-call latency (ms) on the incremental online verifier (O(|C|) per call). C is the number of contracts
evaluated.


                                      F    Per-Cell τ 2 -bench Reliability Matrix
Figure 6 plots the pass4 and joint4 endpoints of the τ 2 -bench reliability matrix. Table 9 gives the exact per-cell values,
including the intermediate proc-clean4 column (all four retries had zero ContrAgent rule fires). pass4 is the native outcome
metric, joint4 requires both outcome and procedure-clean on every retry, and the pass4 -to-joint4 gap quantifies the loss
of procedural reliability.

                                       Domain Model         pass4 proc-clean4 joint4
                                       retail  Claude 3.7    59.6          0.0   0.0
                                               GPT-4.1       52.6        78.1   43.9
                                               GPT-4.1-mini 38.6         17.5    9.6
                                               o4-mini       45.6        77.2   34.2
                                       airline Claude 3.7    36.0          0.0   0.0
                                               GPT-4.1       40.0        34.0   24.0
                                               GPT-4.1-mini 26.0         14.0   14.0
                                               o4-mini       38.0        48.0   30.0
                                       telecom Claude 3.7    25.4          0.0   0.0
                                               GPT-4.1       19.3          4.4   2.6
                                               GPT-4.1-mini 17.5           0.9   0.9
                                               o4-mini       26.3          7.0   7.0

Table 9: τ 2 -bench task-level reliability (k = 4, percentages). pass4 is the native outcome metric (all four retries reach the
correct final state); proc-clean4 requires zero ContrAgent rule fires on all four retries; joint4 requires both. Claude 3.7
reaches proc-clean4 = 0% in every domain, so its joint4 is 0% despite a 25 to 60% outcome pass4 .
