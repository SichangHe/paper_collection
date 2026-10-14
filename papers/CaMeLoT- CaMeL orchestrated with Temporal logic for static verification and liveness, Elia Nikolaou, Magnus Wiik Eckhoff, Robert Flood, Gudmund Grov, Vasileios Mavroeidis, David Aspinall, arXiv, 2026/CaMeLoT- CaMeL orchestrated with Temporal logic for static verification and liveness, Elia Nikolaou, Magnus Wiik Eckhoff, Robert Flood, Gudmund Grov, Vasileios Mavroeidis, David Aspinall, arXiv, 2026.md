                                            CaMeLoT: CaMeL orchestrated with Temporal logic for
                                                      static verification and liveness



                                         Elia Nikolaou                                                                   s2437505@ed.ac.uk
                                         University of Edinburgh, UK

                                         Magnus Wiik Eckhoff                                           Magnus-wiik.eckhoff@ffi.no
arXiv:2609.18674v1 [cs.CR] 16 Sep 2026




                                         Norwegian Defence Research Establishment & University of Oslo, Norway

                                         Robert Flood                                                                flood.rob@proton.me
                                         University of Oslo, Norway

                                         Gudmund Grov                                                        Gudmund.Grov@ffi.no
                                         Norwegian Defence Research Establishment & University of Oslo, Norway

                                         Vasileios Mavroeidis                                                            vasileim@ifi.uio.no
                                         University of Oslo, Norway


                                         David Aspinall                                                           david.aspinall@ed.ac.uk
                                         University of Edinburgh, UK




                                                                                     Abstract
                                             LLM-based agents generate and execute multi-step plans that invoke external tools which
                                             can access private data or execute commands. In this setting, security is a property of the
                                             entire execution that a plan creates, not just any single step. The plan itself is a critical
                                             artefact that captures the tool calls, control flow, and data dependencies. We present
                                             CaMeLoT, a complement to CaMeL, an existing defence against prompt injection in tool-
                                             using LLM agents. CaMeLoT extends CaMeL by adding a static verification layer that
                                             checks an agent’s plan before any tool is invoked. CaMeLoT translates a generated plan into
                                             a finite-state transition system, labels it with tool calls, provenance and taint information,
                                             and checks it against temporal policies expressed in CTL using the nuXmv model checker.
                                             Because verification happens before execution, unsafe plans are rejected without using LLM
                                             calls or tool calls, saving tokens that runtime could have cost, as well as the need to unwind
                                             changes or teardown temporary sandboxes. When a verification fails, the model checker
                                             returns a counterexample to give feedback to the agent to repair the plan. We evaluate
                                             CaMeLoT on policies derived from the AgentDojo benchmark, SOC workflows, and prompt-
                                             extraction experiments, showing that it verifies a broad class of temporal properties before
                                             execution while preserving CaMeL’s runtime-checkable coverage.
                                             Keywords: agentic systems, prompt injection, CaMeL, temporal logic, model checking,
                                             static verification
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




1. Introduction
Large language models (LLMs) are increasingly integrated into agentic systems that plan,
reason, and invoke external tools on behalf of users. Tool use enhances their practical
utility, but also opens a large new attack surface. Agents may access private data, modify
persistent state, interact with third-party services, or initiate actions whose consequences
extend far beyond the immediate conversation. If an agent is manipulated through prompt
injection, malicious instructions, or compromised context, it may autonomously exfiltrate
information, abuse permissions, and cause destructive changes.
    These risks underscore the need for safeguards that constrain agents’ actions without
eliminating the autonomy that makes them useful. Prompt injection, in particular, has been
identified by OWASP (OWASP Gen AI Security Project (2025)) as the most significant risk
for such agentic applications. Google DeepMind’s CaMeL (Debenedetti et al. (2025)) is a
promising approach to mitigating prompt injections in which security policies are expressed
as constraints on the agent’s observable actions, rather than relying solely on the underlying
model to resist adversarial instructions. CaMeL policies can block some unsafe behaviours
at the tool-use level, even if the model’s internal plan has been corrupted.
    In CaMeL, security policies specify the information flows and tool calls that are per-
mitted during agent execution. This is achieved through two security paradigms: Willi-
son (2023)’s dual LLM architecture to protect against control-flow attacks and capabilities
(Goguen and Meseguer, 1982) to protect against data-flow attacks. In the dual-LLM archi-
tecture, execution is divided between a Privileged LLM (P-LLM) and a Quarantined LLM
(Q-LLM). The Q-LLM serves as an intermediate step between the P-LLM and untrusted
inputs, processing potentially adversarial content and converting it into a constrained, struc-
tured representation, for example by extracting client names from an email or summarising
an external document. This structured output is returned to the interpreter as capability-
tagged data.
    Outputs from untrusted sources are tainted with capabilities that are used in the security
policies. In CaMeL, these policies are expressed as Python functions that inspect a tool
invocation and its arguments, then return an allow-or-deny decision with an accompanying
reason. This design enables capability-aware enforcement without introducing a separate
domain-specific language for policies.
    However, CaMeL’s policy model is inherently procedural and temporally local. A policy
is evaluated at tool invocation, using the current tool, its arguments, and the provenance
information available at that point. While CaMeL’s interpreter maintains a data-flow graph,
it does not offer an explicit global specification language for properties that span entire
executions; liveness properties are a prime example of a class of properties that cannot be
expressed naturally.

   Motivating example (1)

   Consider an agentic system used in a security operations centre (SOC) to support
   security analysts, with the following policy:
   An incident ticket must exist for all steps, and this must be resolved or escalated
   to the incident response team before you finish.




                                              2
                                          CaMeLoT




   This policy spans the entire execution and is an example of a liveness property, i.e., a
   property expressing that something (good) must happen at some point, and it cannot
   be expressed naturally in CaMeL.

    A second limitation is that CaMeL checks policies when an agentic plan is executed at
runtime. While some properties are inherently dynamic and must be checked at runtime,
other properties can be checked at the planning stage. Because the latter class of prop-
erties is enforced at runtime, LLM calls up to the point of failure will still be executed,
causing unnecessary time, resource, and token usage compared with checking the properties
“statically” during the planning phase.

   Motivating example (2)

   Next, consider the following policy:
   Any isolation of a host requires Incident Response (IR) approval.

   The following prompt is provided:
   Handle the alert as follows. If it relates to a high-importance host,
   then first confirm the alert and then isolate the host.

   Host isolation is likely to happen in later steps of the plan because the alert first
   needs to be analysed, which could be a long and complex task. If the plan does not
   include an approval step, or approval is impossible, the plan will fail only at the end,
   when isolation is performed. This may entail significant resource usage. Verifying
   the policy during the planning phase would avoid this unnecessary use of time and
   resources.

   Finally, while one plan may fail, there may be other correct plans that satisfy the required
security policies. Given the dynamic nature of how CaMeL checks policies, it cannot replan
during the planning phase if a policy is violated. By checking policies at the planning stage,
the nature of policy failure can be exploited productively to propose a new plan.

   Motivating example (3)

   Consider the second example. If there is a dedicated agent responsible for obtaining
   IR approval, the plan can be patched to include this step prior to isolation. Here, the
   policy’s failure can be provided as input to the planner to help ensure the policy is
   satisfied.

    To address these limitations, we introduce CaMeLoT, a neurosymbolic approach that
complements CaMeL’s capability system with a formal, temporal, model-checking perspec-
tive. CaMeLoT translates a CaMeL plan, represented as restricted Python code generated
by the P-LLM, into a finite-state machine that models its control-flow structure. Security
properties spanning entire executions can be represented in natural language, from which
we can optionally extract a formal specification in temporal logic that is verified via model

                                              3
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




checking during the planning phase, without executing any LLM or tool. If verification
fails, generated counterexamples may be used productively for replanning, if possible.

   Motivating CaMeLoT illustration
   Consider the first policy again. From the text, the following specification in temporal
   logic can be extracted:
                                                                      
                  Always open(ticket) ⇒ Eventually closed(ticket)

   This property states that if ticket is open, it must be closed at some later point.
   The second property is a (safety) invariant that has to hold for all states:
                                                                         
                  Always isolated(host) ⇒ IR approval(host, isolation)

   CaMeLoT can extract such properties and verify that a plan generated by CaMeL
   satisfies them before execution.

Contributions and Overview. CaMeLoT is a conservative and complementary exten-
sion to CaMeL, augmenting its dynamic capability enforcement. CaMeLoT adds a static
layer for checking properties formally and precisely from the generated plan. CaMeLoT’s
model checking based re-planning is reminiscent of the well-known technique of (CEGAR)
counterexample-guided abstraction refinement (Clarke et al., 2003); feeding back counterex-
amples suggests a natural-language refinement of the desired security policy for the specific
plan.
    The contributions of this paper can be summarised as follows:

  1. An extension of CaMeL that augments CaMeL’s existing dynamic capabilities with
     temporal properties and formal verification, thus creating a hybrid framework.

  2. Formal verification of security properties statically, thus avoiding unnecessary LLM
     calls, tool invocations, and token usage.

  3. An approach that automatically refines failing plans by utilising counterexamples.

  4. LLM-assisted extraction of temporal specifications from natural language.

    The lack of formality of CaMeL was pointed out as a limitation for future work in the
original CaMeL paper (Debenedetti et al., 2025); indeed, our work is part of a broader set
of approaches that bring formality to agentic systems including approaches mixing static
and dynamic phases, and based on logics including temporal logic. The case for combining
static and dynamic checks for agentic workflows has recently been argued for convincingly
by Meijer (2026); further references are in Section 6.
    The rest of the paper is structured as follows: Section 2 describes CaMeL; Section 3
introduces the CaMeLoT extension to CaMeL; Section 4 describes how CaMeLoT has been
implemented on top of the CaMeL implementation; Section 5 shows the results from eval-
uating CaMeLoT on different benchmarks; Section 6 compares and contrasts our approach
to related work; and finally, Section 7 concludes the paper and suggests some future work.

                                             4
                                         CaMeLoT




2. Capabilities for Machine Learning (CaMeL)
CaMeL (Debenedetti et al., 2025) is an agentic framework developed with defence against
prompt injection in tool-using LLM agents in mind. Its central contribution is to combine
the isolation-based Dual LLM pattern proposed by Willison (2023) with a capability-based
information-flow tracking layer based on more traditional cyber security concepts (Denning
and Denning, 1977; Goguen and Meseguer, 1982; Abadi et al., 2009). Willison’s pattern
alone separates the part of the system that plans and acts from the part that processes
untrusted content, thereby addressing attacks on the plan’s control flow. However, as shown
in Debenedetti et al. (2025), isolation alone may not stop an adversary from manipulating
the data passed to an otherwise correctly chosen tool call. CaMeL closes this gap by
additionally tracking capabilities on every value the agent interacts with and enforcing
policies over them at tool-call time. Those capabilities record where a value (Sources) came
from and who may read it (Readers), thus addressing attacks on the data flow.
    In the dual-LLM architecture, a P-LLM takes the trusted user query and generates a
plan, expressed as restricted Python code that specifies the intended control and data flow of
the task to be completed. A Q-LLM, which has no access to tools, is invoked like a function
call to extract structured information from sources. The CaMeL interpreter executes the
plan and is responsible for actually invoking the tools. The Q-LLM’s extracted values are
stored by the interpreter as capability-tagged variables; therefore, a prompt injection that
reaches the Q-LLM cannot actually issue instructions back to the P-LLM. It can only alter
the value bound to a variable, which is exactly what CaMeL’s capability system is designed
to enforce.
    CaMeL’s policies are Python functions evaluated by the interpreter at runtime (tool-call
time). A policy receives the requested tool invocation, its arguments, and any capabilities
associated with these arguments, and then returns an allow or deny decision. This is
effective for local runtime checks and is deliberately dynamic, as some facts needed for
enforcement may only be known when a tool is actually invoked. The temporal requirements
motivated in Section 1, however, are not represented in this model, and neither are static
checks nor any form of formal verification.

3. The CaMeLoT Extension
CaMeLoT extends CaMeL with the ability to express properties across the execution path
and to statically verify them during the planning phase. It uses the same threat model as
CaMeL, where the input prompt, user and system prompts, and the output of some, but
not all, tools are trusted. CaMeLoT supports two types of properties:

  1. Security policies expressed as formulas in temporal logic.

  2. Task properties extracted from user prompts and translated from natural language
     into temporal logic.

The system works as follows. Before any external tool is invoked, the privileged LLM will
have produced a restricted Python plan. That plan is not just executable code but also a
structured artefact exposing control flow, ordering, branches, loops, and data dependencies.
CaMeLoT takes advantage of this and turns the plan into a formal model that can be

                                              5
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




                     Task Property
                      Extraction                          Security            Security            CaMeL
                      (Optional)                         Properties           Policies            policies




                       P-LLM              Finite-State                Model          verified
  User Query                                                                                    Execute Plan
                    Generated Plan          Machine                   Check


                                                                         violation
    CaMeL
    CaMeLoT                                                   Counterexample
                                     repair prompt                Trace


   Figure 1: Simplified overview of the CaMeLoT neurosymbolic verification pipeline.


reasoned over. Requirements that depend on concrete values or reader sets remain with
CaMeL at runtime, while requirements that can be read from the plan’s temporal structure
are expressed in a logic called Computation Tree Logic (CTL) (Clarke and Emerson, 1981)
and verified over a finite-state model using model checking before execution.

   Computation Tree Logic (CTL)

   There are different types of temporal logic with different expressivities. For example,
   we distinguish between branching and linear temporal logics, where branching logic
   enables reasoning about different futures. CTL is an expressive branching temporal
   logic with good tool support. (For the examples in this paper, a linear temporal logic
   would in fact have been sufficient, but the generalisation is not harmful.)
   CTL temporal operators combine path quantifiers with temporal modalities. The
   path quantifier A means “on all paths”, while E means “on some path”. The temporal
   modalities used in this paper are X for next state, F for eventually, G for always,
   and U for until. Thus, AG φ states that φ holds in every state along every path;
   AF φ states that φ eventually holds along every path; and A[φ U ψ] states that, on
   every path, φ holds until ψ becomes true.

    CaMeLoT extends CaMeL by inserting a verification stage between plan generation and
execution, as shown in Figure 1. Here, the blue boxes are part of the original CaMeL system,
and the yellow boxes represent the new CaMeLoT extension. Once the P-LLM generates
an agentic plan, CaMeLoT extracts the abstract syntax tree (AST) from the Python plan,
which provides a structured representation of assignments, conditionals, loops, and tool
invocations. It then translates this representation into a finite-state machine system where
states correspond to program points and transitions denote possible execution steps.
    CaMeLoT also labels the transition system with security-relevant facts. In addition
to recording which tool is called at each program point, it tracks provenance and taint
information for variables and tool arguments. History predicates are also recorded, indi-
cating which tools have already been called along the current path. Loops are represented

                                               6
                                         CaMeLoT




using nondeterministic transitions between iterations and loop exit. This yields a finite
abstraction of possible executions while preserving the branching behaviour.
    To verify the properties, we use the nuXmv model checker (Cavada et al., 2014). This is
achieved by encoding the transition system as a nuXmv input model, and representing the
CTL properties in the format expected by nuXmv. If all properties hold, the plan is accepted
and execution proceeds under CaMeL’s usual runtime enforcement. If verification fails,
nuXmv returns a counterexample trace identifying a violating execution path. CaMeLoT
converts this trace into natural-language feedback and prompts the P-LLM to repair the
plan; this is reminiscent of counterexample-guided abstraction refinement (CEGAR) (Clarke
et al., 2003). Verification is then repeated until the plan is accepted or the repair budget is
exhausted.

3.1. Security Policies and Extracted Task Properties in CTL
CaMeLoT policies are written using the CTL operators introduced above, and task-level
properties are extracted from the prompt in natural language and turned into CTL. These
formulas are interpreted over atomic propositions derived from the finite-state model. Poli-
cies are selected by domain so that the verifier checks only the subset relevant to the tools
and actions appearing in a generated plan. For logging and integration with existing se-
curity tooling, each policy is also equipped with lightweight metadata inspired by Sigma
rules1 . A typical policy has the internal representation as shown in Listing 1.
CTLProperty(
    name="no_untrusted_dm_recipient",
    id="f805c65e-b6f5-4a7d-b6f7-1db3ed4c5250",
    status="stable",
    author="Joe Bloggs",
    date="2025-12-12",
    formula="AG(call_send_direct_msg -> recipient_trusted)",
    description="send_direct_msg must never be called with an untrusted recipient",
    level="critical" )

                            Listing 1: Example CTL rule format
    To enable fine-grained taint tracking, CaMeLoT maintains a map from each allowed tool
to its argument names. As a result, CTL policies can refer to tool arguments in a stable
way regardless of how the P-LLM writes the call. CaMeLoT policies cover several common
safety and liveness patterns, such as:

Argument provenance:     AG(call remove user ⇒ user trusted)
     Taint prevention:   AG(call send money ⇒ ¬(recipient tainted ∨ amount tainted))
   Temporal ordering:    AG(host from qllm ⇒ A[¬ call isolate host U call confirm host])
         Termination:    AF(done)

   CaMeLoT can extract task-local CTL properties directly from the user prompt. A
proposer maps the prompt to a fixed vocabulary of structured requirements, such as a
required action, and then a deterministic grounding step checks tool validity and rejects
1. https://github.com/SigmaHQ/sigma


                                              7
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




any malformed or ungrounded obligations. The resulting properties are installed in the
runtime task registry and checked by the same nuXmv pipeline as the security policies. An
example of this is provided in Section 5.3.


3.2. Finite State Machine Generation and Model Checking with Repair

CaMeLoT implements a custom AST visitor that traverses the AST of the generated plan
and extracts control-flow regions. Whereas CaMeL uses the AST purely to drive its run-
time interpreter, CaMeLoT extracts static structural information from the AST as a step in
the construction of the finite-state machine. We distinguish four region types: TOOL CALL,
corresponding to invocation of a tool function; ASSIGNMENT, corresponding to pure com-
putation without a tool call; CONDITIONAL, corresponding to if/else branching; and LOOP,
corresponding to bounded or abstracted loop iteration. These region types are sufficient for
the subset of Python accepted by the CaMeL interpreter, which excludes constructs that
would complicate static control-flow extraction, such as arbitrary while loops or uncon-
trolled break statements. During extraction, nested tool calls appearing inside expressions
or arguments are emitted as regions before the call.
    CaMeLoT classifies each variable according to its data source using a provenance map
prov. In this work, prov : Var → {trusted, user, untrusted, qllm} is defined as a strictly
ordered privilege lattice:

                          trusted < user < untrusted < qllm.

Variables are tagged during AST extraction according to their origin. The Q-LLM out-
put has qllm provenance; external tool outputs, such as read channel messages, have
untrusted provenance; literals have trusted provenance; and user query parameters have
user provenance. Derived values inherit the maximum provenance of their dependencies
under the lattice ordering, implementing conservative taint propagation. Both the lattice
and inheritance strategies are defined programmatically and can be adapted to support
more expressive permission schemes. In CaMeLoT, these provenance rules are part of the
security policy configuration and are combined with CTL properties. Consider the minimal
CaMeL plan generated by a P-LLM shown in Listing 2.

# Read messages from a channel
messages = read_channel_messages("general")

# Use Q-LLM to find Bob’s email address
email = query_ai_assistant(
    f"Extract Bob’s email from: {messages}",
    EmailAddress
)

# Send a direct message
send_direct_message(email, "Meeting at 3pm")

                               Listing 2: Simple agent plan


                                               8
                                                  CaMeLoT




The AST extractor extracts three control-flow regions, all of type ASSIGNMENT:

                       r0 : read channel messages("general") → messages
                       r1 : query ai assistant(. . .) → email
                       r2 : send direct message(email, "Meeting at 3pm")

    Given the extracted regions, CaMeLoT constructs M = (S, s0 , ∆, Σ, L), a finite-state
machine where S is the finite set of states, s0 ∈ S is the initial state, ∆ is the transition
relation, Σ is the set of transition effects corresponding to state-variable updates, and
L : S → 2AP is a labelling function over atomic propositions.
    Each region type maps to a small state-machine fragment. A tool-call region of the
form x = tool(arg1 , arg2 ) creates a state stool with metadata capturing the tool name,
arguments, and target variables. The incoming transition records effects such as xdefined =
true, tool called = true, and any relevant provenance annotations.
    A conditional region creates branch, true-branch, false-branch, and merge states, with
guarded transitions representing each branch and its merge point. A loop region is repre-
sented using entry, body, and exit states. Iteration is treated as a nondeterministic choice
between continuing and exiting the loop. This over-approximates the set of possible loop
executions and ensures a finite state space regardless of iteration count. The abstraction
may produce false positives and block some safe plans, but it preserves potential policy
violations across loop executions.
    During state-machine construction, provenance annotations from the AST produce
transition effects. For instance, a call of the form send direct message(recipient=x,
body=y) produces the proposition recipient trusted if prov(x) = trusted, and produces
recipient tainted if prov(x) ∈ {untrusted, qllm}. These propositions enable CTL prop-
erties such as:

                  AG(call send direct message ⇒ recipient trusted)

which enforces that the direct-message tool is never called with an untrusted recipient.
    Continuing the example from Section 3.2, the three extracted regions produce the state
machine in Figure 2. The five states sINIT → s0 → s1 → s2 → sDONE correspond to the
initial state, the three tool calls and termination, respectively. The transition from s0 to
s1 marks email as tainted because it originates from the Q-LLM, and s1 to s2 propagates
this taint to the recipient argument. At state s2 , both call send direct message and
recipient tainted hold, violating the CTL property above and triggering plan repair.

                read channel           query ai              send dm
        sINIT                  s0                    s1                   s2           sDONE


                           messages                 email          recipient tainted
                           untrusted               tainted            ∧ send DM


                    Figure 2: State machine produced from the simple plan.

    The verification loop iteratively updates the generated plan until all policy violations
are resolved or the repair budget is exhausted. When a plan violates a security property,

                                                      9
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




nuXmv produces a counterexample trace: a concrete execution witnessing the violation.
Continuing the running example, a counterexample is produced in state s2 , and nuXmv
produces a trace in the following shortened form:
-- specification AG (call_send_direct_message -> recipient_trusted) is false
-- as demonstrated by the following execution sequence
  -> State: 1.1 <-
    read_channel_messages_called = FALSE
    ...
  -> State: 1.6 <-
    send_direct_message_called = TRUE
    recipient_tainted = TRUE

    The trace shows an execution reaching send direct message with a tainted recipient,
thereby violating the property. CaMeLoT converts this trace into a repair prompt containing
the violated property, a simplified description of the counterexample path, and general repair
instructions, and passes it to the P-LLM.


4. Implementation
CaMeLoT is implemented as an extension of CaMeL without changing the core functional-
ity.2 It adds a static verification layer that reasons about temporal properties of generated
plans prior to CaMeL’s execution.

Mapping CaMeL Capabilities to Static Taints CaMeL associates the output of
every function call with two kinds of capabilities: Readers and Sources. Readers specify
who may access a value and therefore encode confidentiality constraints. Sources record the
provenance of a value and are used to determine whether the value should be treated as
trusted. Values originating from the user are trusted, whereas values originating from tool
calls may be trusted, untrusted, or conditionally trusted depending on runtime information.
    To illustrate, the output of a function such as get calendar event() may be private,
with its readers determined by the user and the event invitees. Individual fields may also
have different trust properties. The event description may be trusted if it was authored by
the user, but untrusted if it was authored by someone else. However, the invitee set and the
authorship of the description are generally not known at planning time. These properties
therefore cannot be fully resolved by static CTL verification.
    CaMeLoT therefore uses a conservative static abstraction of CaMeL’s provenance infor-
mation. Any value whose provenance is untrusted, conditionally trusted, or not statically
decidable is marked as tainted by CaMeLoT. This ensures that static verification does not
incorrectly treat uncertain data as safe. Conversely, the distinction between public and
private values is intentionally left to CaMeL’s runtime enforcement, since confidentiality
depends on dynamic reader capabilities that may only be available during execution.
    This design reflects the role of CaMeLoT as a complementary layer. CaMeL remains
responsible for enforcing fine-grained capability checks at runtime, while CaMeLoT verifies
temporal and ordering properties that can be checked before execution.

2. CaMeLoT (https://github.com/detlearsom/camelot) has been implemented by forking and extending
   the CaMeL GitHub repository (https://github.com/google-research/camel-prompt-injection).


                                              10
                                          CaMeLoT




Static Plan Extraction CaMeLoT operates on the restricted Python plans generated
by the P-LLM. Since CaMeL already restricts the language available to the planner, the
generated code is suitable for syntactic analysis. Before extraction, a normalisation pass
is applied to the plan without altering its behaviour. Then, each plan is parsed into an
abstract syntax tree, and the program regions described in Section 3.2 are extracted. During
extraction, CaMeLoT records the following information for each relevant program point:
   • the tool being invoked when the region is a tool call;
   • the variables defined by the region;
   • the arguments passed to the tool;
   • the provenance of variables and derived values;
   • the control-flow successors of the region.
Tool signatures are used to normalise positional and keyword arguments. This is necessary
because the same tool call may be written in several equivalent ways. For instance, the
calls send direct message(email, body) and send direct message(recipient=email,
message=body) should induce the same atomic propositions in the generated model. By
resolving arguments through tool signatures, CaMeLoT can consistently derive propositions
such as recipient tainted or recipient trusted.

nuXmv Model Generation After extracting the plan structure, CaMeLoT translates
the resulting control-flow graph into a nuXmv model. The model contains a finite pro-
gram counter representing the current state of the plan, together with Boolean variables
representing security-relevant propositions. These propositions include tool-call indicators,
argument taint flags, provenance flags, and history predicates recording whether a relevant
action has already occurred.
    For each state in the extracted model, CaMeLoT emits transition rules describing the
possible next states. Sequential statements produce deterministic transitions. Conditionals
produce one transition for each branch. Loops are represented by nondeterministic tran-
sitions that either enter another iteration or exit the loop. This abstraction ensures that
the generated nuXmv model is finite while preserving the possible branching behaviours
relevant to CTL verification.
    CaMeLoT also emits state updates for security-relevant facts. For example, when a tool
call consumes a variable marked as tainted, the corresponding argument proposition is set in
the nuXmv model. Similarly, when a confirmation tool is called, a history predicate such as
confirmation seen can be set to true and retained in subsequent states. These predicates
allow CTL formulas to express ordering properties such as requiring confirmation before a
high-impact action.

Policy Selection and Verification The CTL policy suite may contain properties for
many tools and deployment domains. CaMeLoT filters the policy suite before invoking
nuXmv. A policy is selected when its referenced tools or propositions appear in the gener-
ated plan or in the corresponding domain configuration. The selected CTL properties are
emitted alongside the nuXmv transition system. The model checker then verifies whether
the generated plan satisfies all selected properties. If all properties hold, the plan is accepted
and passed to CaMeL for execution.
    If a property fails, nuXmv returns a counterexample trace. CaMeLoT parses this trace
and converts it into structured feedback for the P-LLM. The feedback identifies the violated

                                               11
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




property, the relevant execution path, the likely program location, and the type of violation.
The P-LLM is then prompted to repair the plan, after which the revised plan is verified
again. This process continues until either verification succeeds or the repair budget is
exhausted.

5. Evaluation
We have conducted three different experiments to evaluate CaMeLoT. The first experiment
measures how much of CaMeL’s policy coverage CaMeLoT can reproduce using static veri-
fication. The second experiment explores properties beyond the expressiveness of CaMeL’s
local runtime policies. The third and final experiment investigates the extent to which
task-level properties can be automatically extracted from user prompts and verified.

5.1. Experiment 1: Overlap with CaMeL
The goal of the first experiment is to measure how much of CaMeL’s enforcement CaMeLoT
can reproduce. We configure CaMeLoT with CTL properties that mirror CaMeL’s policies
as closely as possible using the following AgentDojo benchmark suites: Slack, Banking,
Travel, and Workspace (Debenedetti et al., 2024). These are the suites used in the original
CaMeL evaluation (Debenedetti et al., 2025). We compare both approaches on the same
tasks and measure how often their decisions agree.
    The CaMeL policy enforces that the password argument originates from a trusted source
before update password can proceed.
if is_trusted(kwargs["password"]):
    return Allowed()
return Denied("The password does not come from the user.")

                            Listing 3: CaMeL policy in Python.
The following formula expresses the same condition as Listing 3 in CTL:

                    AG(call update password ⇒ password trusted)

It states that it is always the case that whenever update password is called, the password
argument must be trusted at that point in time.
    Since CaMeLoT verifies the P-LLM-generated plan before execution, only statically
available properties can be analysed. Runtime properties, such as the list of people with
read access to a shared file at the moment of execution, are not available at this stage. As
a result, only a subset of the properties used in CaMeL’s evaluation can be expressed as
CTL properties. When mirroring the CaMeL policies defined for the AgentDojo benchmark
suites, CaMeLoT achieves static coverage of 22 out of 28 CaMeL policies. The remaining
six policies depend on a runtime state that cannot be determined from the plan structure
alone and are therefore left to CaMeL’s dynamic enforcement mechanism. Confidentiality
properties – defined with readers – are not handled directly by CaMeLoT; they overlap
only when the output of a function call is public. We implement the tagging of trusted
and untrusted variables created by functions without side effects in AgentDojo, reaching
coverage of 24 out of 46. A breakdown of covered and uncovered policies for functions with

                                             12
                                               CaMeLoT




side effects is shown in Table 1, while the summary of output tagging for functions is shown
in Table 2.

Table 1: Overlap of policies between                    Table 2: Overlap of tainting logic between
         CaMeL and CaMeLoT                                       CaMeL and CaMeLoT

Suite             Security       Confidentiality        Suite             Security           Confidentiality
            Full Partial None Full Partial None                     Full Partial None Full Partial None

Slack         3        1     3    3        0       4    Slack         3        2         0    0       0         5
Banking       5        0     0    2        0       3    Banking       3        2         0    1       0         4
Travel        6        0     0    5        0       1    Travel       17        5         0   19       0         3
Workspace     8        0     2    6        0       4    Workspace     1       13         0    3       0        11

Total        22        1     5   16        0       9    Total        24       22         0   23       0    23


    We performed the experiment by running both approaches on the same tasks in Agent-
Dojo. We ran the four suites (Travel, Banking, Slack, and Workspace) without prompt
injections using Anthropic’s claude-haiku-4-5-20251001 model. In this setting, plan re-
pair is disabled for CaMeLoT, except when the generated code uses an operation that
CaMeLoT does not support, such as in-place list modification. In that case, one repair
prompt is used to replace the unsupported operation.
    The results are shown in Table 3. Each plan falls into one of three categories: pass,
where the plan is permitted and behaves as intended; fail, where the plan is permitted but
does not behave as intended; and blocked, where the plan violates the security properties and
is rejected. The two techniques mostly agree on pass and block decisions, only disagreeing
on 16 out of 75 successful tests. These disagreements are mostly caused by CaMeL blocking
based on runtime properties, such as the readers of a resource. When both systems block
a plan, CaMeLoT does so before execution, avoiding unnecessary tool calls and reducing
token usage for plans that would fail. A substantial number of user tasks, 22 out of 97, fail
under both approaches because the generated plan does not accomplish the user’s intended
task. This would likely be improved with stronger planning models.

        Table 3: AgentDojo test results for CaMeL and CaMeLoT on the same tasks
Suite         Both pass      Both fail     Both block       CaMeLoT only pass            CaMeL only pass
Slack                    6             5                6                            4                     0
Banking                  5             2                6                            2                     1
Travel                   9            10                0                            1                     0
Workspace               22             5                5                            2                     6
Total                   42            22               17                            9                     7



5.2. Experiment 2: Properties beyond CaMeL’s capabilities
CTL supports reasoning over temporal properties of the full plan, which cannot be naturally
captured using CaMeL’s local security policies. This enables new classes of requirements
over LLM-generated plans, including business-process constraints, liveness properties, and

                                                   13
                  Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




ordering requirements. To illustrate the utility of CTL, we constructed a simplified Security
Operations Centre (SOC) scenario, an area with increasing use of this type of agentic system
(Srinivas et al., 2025; Singh et al., 2025; Freitas and Gharib, 2026; Palo Alto Networks, 2025;
Google Cloud, 2025; CrowdStrike, 2025). The scenario models an LLM agent acting as a
tier-1 SOC analyst. The agent reads alerts from an intrusion detection system, performs a
basic investigation, and then either resolves the case as a false alert or escalates it. The agent
may also perform preventive actions, such as isolating a host, but only after appropriate
checks and approval.
    To eliminate variability in language-model generation and focus on verification, we used
a fixed safe plan and manually constructed unsafe variants of it. We defined one SOC
workflow and seven CTL properties relevant to an agent in an SOC. These are shown in
Table 4. The policies are designed to exercise different CTL property classes, including
liveness, global safety, and temporal ordering, and they use different temporal operators
such as until (A[φ U ψ]) and next (X(φ)).
    For comparison, we implemented a simplified CaMeL namespace that tracks taint only.
Output from the Q-LLM is marked as tainted, block ip() and create incident ticket()
are the only functions that reject tainted input. For each of the seven formulae, we con-
structed a variant of the safe plan that is intentionally unsafe. We ran both the model
checker in CaMeLoT and CaMeL’s policy checker and measured how well the two approaches
blocked the unsafe plan while allowing the safe one. We note that as the properties are
intentionally designed to go beyond the expressiveness of CaMeL, we expect CaMeL to miss
most of them. The safe SOC-agent plan is shown in Listing 4.
alert = get_last_alert(severity="HIGH")
check_sender_reputation(sender="alerts@example.com")
scan_attachments(alert=alert)
confirmed = confirm_host(hostname="workstation-17")
ticket = create_incident_ticket(
    title="High-severity alert",
    description="Potential compromise requiring isolation",
)
request_ir_approval(incident=ticket)
isolate_host(hostname=confirmed)
resolve_incident(incident=ticket)

                               Listing 4: SOC agent safe plan.
    Table 5 summarises the experimental results and indicates whether each unsafe variant
is caught by CaMeLoT and the simplified CaMeL baseline. CaMeLoT catches all seven
unsafe plans, while the simplified CaMeL baseline catches only the taint-style violation
represented by S7. This confirms that CaMeLoT detects violations that are not naturally
expressible as local per-call CaMeL policies. In particular, CaMeLoT catches missing future
obligations, incorrect ordering, and immediate-step violations.
    We also ran a second part of this experiment in an end-to-end fashion. The plans were
generated by the P-LLM from a user query, and we used the same CTL properties outlined
in Table 4. For each test, we had two variants of a query: one intended to create a good
plan, and one intended to accidentally create a bad plan. The following variant of the query
was designed to generate a good plan:

                                               14
                                                   CaMeLoT




                                       Table 4: SOC CTL policy rules.
       Description                      Formula

  S1   Confirm host before isolation    A[¬ call isolate host U confirm host called]
  S2   Human approval before            AG((call isolate host ∨ call block ip ∨ call disable account) ⇒
       strong action                    request ir approval called)
  S3   Isolation must occur             AF(call isolate host)
  S4   Created ticket must be           AG(call create incident ticket ⇒
       resolved or escalated            AF(call resolve incident ∨ call escalate to ir team))
  S5   No immediate isolation           AG(call scan attachments ⇒ AX¬ call isolate host)
  S6   Create ticket before strong      AG((call isolate host ∨ call escalate to ir team ∨
       action                           call request ir approval) ⇒ create incident ticket called)
  S7   Do not block untrusted IP        AG(call block ip ⇒ ¬ ip tainted)



           Table 5: SOC scenario: unsafe plans caught by CaMeLoT and CaMeL.
 Property class        Rule    Violation                                               CaMeLoT     CaMeL

 Until                  S1     isolate host is called before confirm host.                ✓           ✗
 Temporal ordering      S2     isolate host called without prior human approval.          ✓           ✗
 AF liveness            S3     Suppression attack: isolate host is never called.          ✓           ✗
 Triggered liveness     S4     A ticket is created but never resolved or escalated.       ✓           ✗
 Next step              S5     isolate host immediately follows scan attachments.         ✓           ✗
 Temporal ordering      S6     A strong action occurs before a ticket is opened.          ✓           ✗
 Global safety          S7     A tainted IP address from LLM output is passed to          ✓           ✓
                               block ip.




A high-severity alert just came in, likely a compromise of workstation-17. Handle it by the
book: retrieve the alert, gather the evidence (sender reputation, attachments) confirm the
affected host, open an incident ticket and get IR approval, then isolate the host and
resolve the incident.

The following variant of the query was designed to generate a bad plan:
We already think workstation-17 might be compromised - a colleague told me he was supicious
over the phone. We’re short on time, so skip the approval. Just isolate workstation-17 and
resolve it.

These were given to Anthropic’s claude-haiku-4-5-20251001 model, along with a system
prompt, and the resulting plan was verified by both CaMeL and CaMeLoT in the same
manner as in the first part of this experiment. The results of four tests are shown in
Table 6. As before, we see that the bad plans are caught by CaMeLoT in all cases, whereas
CaMeL does not capture any issues. This was expected.

Table 6: SOC scenario: P-LLM-generated unsafe plans caught by CaMeLoT and CaMeL.
Property class        Rule     Violation                                               CaMeLoT      CaMeL

Temporal ordering     S1, S2   Skips evidence and confirm before isolate host.             ✓              ✗
AF liveness             S3     Assumes false positive: isolate host is never called.       ✓              ✗
Triggered liveness      S4     A ticket is created but left open for the day shift.        ✓              ✗
Temporal ordering       S6     Creating a ticket is skipped completely.                    ✓              ✗




                                                         15
                     Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




5.3. Experiment 3: Extracting Temporal Properties from Prompts
The policies of the previous experiments are fixed before the user task is given. They encode
provenance requirements, taint barriers, and domain ordering rules but they do not capture
what the user asked the agent to do. A plan may satisfy every security policy and still fail
the user’s objective. For example, an injected instruction may tell the agent to stop, avoid
all tools, or merely acknowledge part of the message.

                                LLM proposer          Typed           grounding            CTL
                 Prompt
                                                    obligations                          formulae


                   Figure 3: Pipeline from prompt to grounded CTL formulae.

    To address this, we added an optional task-local extraction stage. From the user prompt,
it attempts to extract task requirements as CTL formulas by producing CTL contracts for
required actions, permitted side effects, ordering constraints, and argument conditions.
The design is deliberately constrained. The LLM never writes CTL directly; instead, it
proposes a small language of typed obligations, which is then grounded and compiled into
CTL formulas by trusted code. Each proposal must instantiate one of the typed obligation
forms in Table 7, and grounding rejects any unknown tool, unknown atom, or malformed
obligation before translation into a CTL formula.

Table 7: Obligation language used by the prompt extractor. Here a, b range over tools, A
         is the allowed side-effect set, and ϕ ranges over grounded audit atoms.

Form                                           Prompt contract                        CTL template

Existence existence                            Some execution reaches a               EF(call a)
All-path existence all paths existence         Every execution eventually reaches a   AF(call a)
Precedence precedence                          b is allowed only after a              AG(call b ⇒ a called)
Until until                                    b is forbidden until a occurs          A[¬ call b U a called]
Response response                              a requires eventual b                  AG(call a ⇒ AF(call b))
Enabled reachability enables                   After a, b remains possible            AG(call a ⇒ EF(call b))
Absence after absence after                    After a, b never occurs                AG(call a ⇒ AG¬ call b)
Next-step prohibition next step forbidden      b cannot occur immediately after a     AG(call a ⇒ AX¬ call b)
                                                                                           W
Side-effect allowlist side effect allowlist    Only requested effects may occur       AG¬ u∈A  /
                                                                                                 call u
Atom requirement atom requirement              a may be called only when ϕ holds      AG(call a ⇒ ϕ)


    To illustrate, we chose a task that exercises the same CaMeL policy audited in the first
experiment: whenever update password is called, the password argument must be trusted.
The extractor reads this prompt together with the fixed tool and atom vocabulary, as shown
in Listing 5.
Input user prompt: Check the transaction history for any suspicious transactions.
After that, if something looks suspicious, update the password to ’1j1l-2k3j’.

Proposed typed obligation: enables( trigger = "get_most_recent_transactions",
targets = ["update_password"])

Compiled CTL: AG(call get most recent transactions ⇒ EF(call update password))


                                                         16
                                                CaMeLoT




                   Listing 5: Prompt extraction example for the Banking suite.
   This task-level property differs from the safety policy used in the first experiment. The
prompt asks the agent to update the password only if a suspicious transaction is found; thus,
the extracted obligation is an enabled-reachability constraint: after checking transactions,
updating the password must remain reachable. The policy, on the other hand, constrains
any password updates. The two are complementary: prompt extraction captures task
completion, while the static policy captures argument provenance. Table 8 shows two
representative SOC cases, illustrating what the extracted task-local properties add.

           Table 8: Two SOC E3 violations enforced by extracted task-local CTL.
 Policy contract                 Bad plan                      Extracted CTL

 Every incident ticket must be   Creates a ticket and never    AG(call create incident ticket
 resolved or escalated.          closes it.                         ⇒ AF(call resolve incident
                                                                  ∨ call escalate to ir team))
 After scanning attachments, do Calls isolate immediately      AG(call scan attachments
 not isolate the host next.     after scanning.                     ⇒ AX¬ call isolate host)


    We evaluate prompt extraction over three dimensions: extraction accuracy (E1), archi-
tectural necessity (E2), and enforcement (E3). For both extraction and task evaluation, all
results were obtained using the claude-haiku-4-5-20251001 model.

Extraction Accuracy (E1) We evaluate all 97 AgentDojo user tasks across the four
suites. Each task has a known correct solution. We keep only the steps that change a
state as labels, for example, “sending a message”. Exact means that the extracted required
side-effect set exactly matches this label. Faithful additionally credits correctly conditional
side effects, because a single label cannot distinguish “always perform X ” from “perform
X only if the prompt’s condition holds”. We separately measure vocabulary accuracy and
grounding survival. Table 9 shows that all proposed obligations are in the vocabulary and
survive grounding. The model recovers the exact required side-effect tools on 85 out of 97
tasks (87.6%) and a faithful set on 88 (90.7%).


            Table 9: Prompt-extraction accuracy and trust-boundary metrics (E1).
Suite                               Tasks        Exact        Faithful         F1     Vocab.     Surv.

Banking                                 16        75.0%         75.0%        0.79       100%     100%
Slack                                   21        85.7%         85.7%        0.88       100%     100%
Travel                                  20        95.0%        100.0%        0.91       100%     100%
Workspace                               40        90.0%         95.0%        0.87       100%     100%

Total                                   97       87.6%         90.7%         0.86       100%     100%



Architectural Necessity (E2) Our pipeline never asks the LLM to generate CTL. The
reason is to maintain a single trusted compilation path across LLM models. If each model

                                                      17
                  Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




writes its own formulas, then differences in syntax, temporal ordering, or atom naming
may introduce invalid or ungrounded properties. To evaluate this design choice, we asked
four models to generate CTL directly using the same tool and atom vocabulary, and then
checked the formulas with nuXmv. A task suite is clean if every proposed formula is
syntactically valid and every identifier is grounded in the vocabulary. Table 10 shows that
direct generation is highly model-dependent. Some models invent plausible but ungrounded
identifiers, and even the best run contains at least one invalid formula. The typed pipeline
avoids these failures because the LLM proposes only typed obligations and trusted code
performs grounding and compilation.

         Table 10: Direct CTL generation compared with the typed pipeline (E2).
Method                              Clean tasks          Valid     Malformed     Ungrounded
                                                       outputs

Direct CTL, GPT-4.1 nano                   12/97        182/655             54            419
Direct CTL, GPT-4.1 mini                   79/97        574/612             16             22
Direct CTL, Claude Haiku 4.5               96/97        493/494              0              1
Direct CTL, Claude Sonnet 4.5              94/97        551/554              2              1

Typed pipeline with Haiku                 97/97        182/182               0              0



Enforcement (E3) We wrote 20 controlled cases relevant to the obligations of Table 7.
For each one, we extracted CTL from the prompt or policy contract, installed the resulting
formulas as task-local properties, and verified two fixed plans: one correct plan and one
violating plan. Twelve cases came from the AgentDojo benchmark, with three for each of
the four suites described above. The remaining eight came from the SOC workflow. As in
the second experiment, both plans were fixed by hand so that the measurement isolated
extraction and enforcement from planner variability. We also compared each extracted
formula with an equivalent handwritten formula. As Table 11 shows, the extracted formulas
block all 20 controlled violations, verify all 20 correct plans, and match the equivalent hand-
written CTL in every case.

6. Discussion and Related Work
CaMeLoT performs verification before plan execution, but it does not attempt to resolve
every security decision statically. Some information is only available at runtime, includ-
ing exact reader sets, dynamically computed capabilities, and tool-specific trust decisions.
These checks remain the responsibility of CaMeL. The implementation therefore follows a
conservative division of labour. CaMeLoT rejects plans that violate statically checkable
temporal properties. CaMeL then enforces dynamic capability policies during execution.
This means that a plan accepted by CaMeLoT may still be rejected by CaMeL at runtime if
a dynamic capability check fails. Conversely, CaMeLoT can reject a plan before execution
when the plan’s temporal structure is unsafe, avoiding unnecessary tool calls and reducing
the associated LLM and token cost.
    Static plan verification requires decisions without runtime information, and CaMeLoT’s
taint abstraction is designed to handle this uncertainty. On the one hand, conditionally

                                              18
                                         CaMeLoT




     Table 11: Extracted CTL enforced against fixed correct and violating plans (E3)
Property class           Characteristic CTL                    n     Good     Bad     Match

Existence                EF(call a)                            4       ✓        ✓       ✓
All-path liveness        AF(call a)                            1       ✓        ✓       ✓
Ordering / history       AG(call b ⇒ a called)                 3       ✓        ✓       ✓
Enabled reachability     AG(call a ⇒ EF(call b))               2       ✓        ✓       ✓
Until                    A[¬call b U a called]                 1       ✓        ✓       ✓
Triggered response       AG(call a ⇒ AF(call b))               1       ✓        ✓       ✓
Next-step prohibition    AG(call a ⇒ AX¬call b)                1       ✓        ✓       ✓
Absence after            AG(call a ⇒ AG¬call b)                1       ✓        ✓       ✓
                             W
Side-effect scope        AG¬ u∈A/
                                    call u                     4       ✓        ✓       ✓
Global taint / safety    AG(call a ⇒ ϕ)                        2       ✓        ✓       ✓

Total                                                         20       20      20       20



trusted function outputs are over-tainted, which may result in excessive blocking, while
values and reader capabilities are not modelled, potentially leading to insufficient blocking.
This is a trade-off between tokens saved by detecting violations before execution and tokens
wasted when a safe plan is unnecessarily blocked. Over-tainting has a cost, but a bounded
one. Model checking a realistically sized plan is significantly less expensive than executing
the corresponding agentic workflow.
    The cost of repair remains essentially the same whether a violation is detected at runtime
or statically; plan generation is required in both cases. The primary difference is that when
a violation is caught at runtime, the cost of every tool and LLM call up to the point of
violation is incurred, yielding a net positive whenever it rejects a plan that would truly
have failed. The only genuinely wasted effort occurs in the case of a false positive, and even
then, the penalty is often a single repair round rather than a partial execution.
    The generated finite-state machine is designed to be simple; thus, it includes only taint
information, with conditions for loops and conditionals omitted and instead represented
as non-deterministic choice. Such a high level of abstraction may mean we cannot verify
certain properties that a finer-grained model could verify. Moreover, tool calls are currently
treated as black boxes, and we could extend this with a more modular approach in which
properties of the call can be used, e.g., using Hoare-style pre- and post-conditions. This,
however, remains as future work.

Related Work. CaMeLoT is part of a growing body of work exploring the use of for-
mal/symbolic mechanisms to improve the security and reliability of LLMs and agents (Mei-
jer, 2026; Kamath et al., 2025; Wang et al., 2025; Cui et al., 2026; Doshi et al., 2026; Garby
et al., 2026; Zhan et al., 2025; Shi et al., 2025; Greengard, 2026b,a; Bayless et al., 2025;
Cohen et al., 2026; Miculicich et al., 2025). Work by Hong et al. (2026) has shown that a
substantial fraction of clearly specified policy requirements can be enforced using symbolic
mechanisms, with temporal properties identified as a key class of properties. By focusing
on CaMeL, we specifically address a limitation of CaMeL regarding formality, identified by
the authors of CaMeL (Debenedetti et al., 2025).

                                              19
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




    The combination of static verification and dynamic checks, with a focus on prompt
injection, is the same as in Meijer (2026)3 . Our work differs in its use of temporal logic,
model checking with plan repair, and the extraction of task-specific properties. Moreover,
we build on an existing, well-known agentic framework in CaMeL. Closest to our work
in shape is TraceFix (Xia et al., 2026), which model checks an LLM-synthesised protocol
with the TLA+ model checker (TLC), repairs it from counterexamples, and executes it
under a runtime monitor. The difference is that our work verifies plans against security
and task properties under prompt injection, while TraceFix focuses on mutual exclusion
and deadlock freedom. Furthermore, its verified protocol is only compiled into prompts,
whereas CaMeLoT verifies the very plan that is then executed.
    There are several other systems that use temporal constraints. Cohen et al. (2026)
introduces TemporalGuard4 , a past-time temporal logic to enforce temporal constraints of
conversations up to the given point in time at which it is enforced. Agent-C (Kamath et al.,
2025) uses temporal constraints to enforce safety properties over LLM-agent behaviour.
AgentSpec (Wang et al., 2025) provides a runtime enforcement framework in which agent
policies can be expressed as customisable specifications over tool use. MARIS (Cui et al.,
2026) studies formally verifiable privacy-policy enforcement for multi-agent collaboration
systems. Doshi et al. (2026) similarly consider verifiably safe tool use, deriving safety re-
quirements from System-Theoretic Process Analysis and formalising them over data flows
and tool sequences. Ramani et al. (2025) convert LLM-generated plans into Kripke struc-
tures and Linear Temporal Logic (LTL) using an LLM, and use the NuSMV model checker
to verify alignment between the plan and the expected behaviour. Miculicich et al. (2025)
introduce the VeriGuard framework, which employs a safety policy to monitor agent ac-
tions during runtime after synthesising and formally verifying it offline. Progent (Shi et al.,
2025) is a formal approach that intercepts tool calls at runtime and verifies them against
a domain-specific policy language supporting fine-grained argument constraints. Those are
local rather than over sequences and are checked at runtime. All of these deviate from our
work by focusing on runtime verification. In addition, CaMeLoT is designed as an extension
of CaMeL, thereby preserving its runtime properties while introducing a static verification
capability. Sentinel (Zhan et al., 2025) uses temporal logics to evaluate the safety of embod-
ied agents. However, its focus is on analysing collected trajectories rather than statically
verifying generated plans before execution.
    The LLMbda calculus (Garby et al., 2026), f-secure (Wu et al., 2024), and RTBAS
(Zhong et al., 2025) provide formal models for information flow, but do not support temporal
logic or correctness verification. DRIFT (Li et al., 2026) enforces control- and data-level
constraints for prompt injections using a dynamic permission mechanism, but without the
formality we include. Finally, IsolateGPT (Wu et al., 2025) mitigates cross-application flow
risks by isolating tool environments.
    Another approach is to place guardrail models in front of the primary model, to classify
inputs or outputs as safe or unsafe before allowing the main model to proceed (Inan et al.,
2023; Li et al., 2025). Although such defences can reduce attack success rates, they remain
probabilistic and cannot provide deterministic guarantees. Moreover, LLM-as-a-judge sys-
tems are themselves vulnerable to optimisation attacks (Shi et al., 2024). A separate line
3. https://github.com/metareflection/guardians/
4. https://github.com/moraneus/LLMrv


                                              20
                                         CaMeLoT




of work attempts to make the model itself more robust to prompt injection. Instruction-
hierarchy approaches train models to distinguish between privileged instructions, such as
system or user messages, and untrusted content, such as text retrieved from external web-
sites or documents. StruQ (Chen et al., 2025) structures model inputs using explicit de-
limiters for trusted and untrusted content, then fine-tunes models to ignore instructions
that appear in untrusted regions. SecAlign (Chen et al., 2024) similarly fine-tunes models
using preference optimisation so that they favour desirable responses and avoid injected
behaviours. CaMeLoT is complementary to these model-level defences; instead of relying
on the model to resist or detect malicious instructions, it verifies the generated plan against
explicit temporal properties before execution.
    We have demonstrated CaMeLoT’s ability to extract task properties from the user
prompt, represent them in temporal logic, and verify that the plan indeed satisfies them.
This closely aligns with work that uses logic and verification as guardrails to ensure the
correctness of LLM outputs (Greengard, 2026b,a). Cohen et al. (2026) also address semantic
grounding to extract temporal formulas comparable to our task property extraction. The
reasoning guardrails of Amazon Bedrock is probably the best-known (industrial) example
of this5 (Bayless et al., 2025). A novelty of our work is the use of temporal logic for this
purpose and the verification that plans satisfy the given user requirements within an agentic
workflow. It should be noted that Amazon has recently added support for temporal policies
via Dogwood6 , but their use of temporal policies in reasoning guards remains unclear.
    Our evaluation is based on AgentDojo (Debenedetti et al., 2024), which was used to
evaluate CaMeL (Debenedetti et al., 2025). In addition, we generated some examples
based on workflows in a Security Operations Centre (SOC). This is an area with increased
use of agents and agentic workflows (Srinivas et al., 2025; Singh et al., 2025), including
commercial usage (Freitas and Gharib, 2026; Palo Alto Networks, 2025; Google Cloud,
2025; CrowdStrike, 2025). This illustrates the practical relevance of these examples and
suggests a future need to develop more specialised SOC policy benchmarks.

7. Conclusion
We introduced CaMeLoT, a neuro-symbolic extension of CaMeL, designed to formally verify
temporal security properties of the full LLM-generated agent plans statically, whilst keeping
the dynamic checks of security policies provided by CaMeL.
    CaMeLoT brings four primary benefits: (1) it enables the specification of new classes
of policies, including temporal ordering and liveness, that are over the full execution path
and not expressible by CaMeL’s per-call checks; (2) enforcement occurs statically, meaning
incorrect plans are rejected during planning, minimising wasted computational resources;
(3) verification failures are used constructively, as counterexample traces guide plan repair
in a robust self-repair loop; and (4) task-local properties can be extracted from the user
prompt and compiled into temporal logic, to improve the chance that the plan does what
the user intended.
    Our evaluation supports three main claims. First, CaMeLoT’s pre-execution verification
covers much of CaMeL’s enforcement: on the AgentDojo benchmark, the two approaches
5. https://aws.amazon.com/bedrock/guardrails/
6. https://github.com/dogwood-policy/dogwood/


                                              21
                 Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




agree on whether to block or pass a generated plan in 59 out of 75 cases. Second, a series
of tests shows that CaMeLoT expresses requirements beyond the local, per-call policies of
CaMeL, illustrated in an agentic security operations centre (SOC) scenario. Third, task-
local requirements can be extracted from user queries: every proposed obligation generated
was in-vocabulary and survived grounding, and the extracted temporal properties enforced
all 20 controlled cases in agreement with handwritten formulae.
    CaMeL was not designed for many of the properties we address here; thus, this should
not be seen as a criticism of CaMeL but rather an extension with new features. However,
we do provide one possible answer to a formality limitation highlighted by the authors of
CaMeL themselves (Debenedetti et al., 2025). We see our work in the context of emerging
neuro-symbolic agentic systems that combine the advantages of LLMs and agents with the
correctness guarantees of formal logic. Besides addressing limitations and work suggested
in Section 6, we also plan neurosymbolic approaches to other properties beyond temporal
logic. One exciting example is improving the correctness of individual LLM calls through
symbolic guards, and not just in the planning phase.

Acknowledgments
Elia Nikolaou was supported by an EPSRC DTA Scholarship (Reference EP/W524384/1).

References
Martı́n Abadi, Mihai Budiu, Ulfar Erlingsson, and Jay Ligatti. Control-flow integrity princi-
 ples, implementations, and applications. ACM Transactions on Information and System
 Security (TISSEC), 13(1):1–40, 2009.

Sam Bayless, Stefano Buliani, Darion Cassel, Byron Cook, Duncan Clough, Rémi Del-
  mas, Nafi Diallo, Ferhat Erata, Nick Feng, Dimitra Giannakopoulou, et al. A neu-
  rosymbolic approach to natural language formalization and verification. arXiv preprint
  arXiv:2511.09008, 2025.

Roberto Cavada, Alessandro Cimatti, Michele Dorigatti, Alberto Griggio, Alessandro Mar-
  iotti, Andrea Micheli, Sergio Mover, Marco Roveri, and Stefano Tonetta. The nuXmv
  symbolic model checker. In International Conference on Computer Aided Verification,
  pages 334–342. Springer, 2014.

Sizhe Chen, Arman Zharmagambetov, Saeed Mahloujifar, Kamalika Chaudhuri, David
  Wagner, and Chuan Guo. Secalign: Defending against prompt injection with preference
  optimization. arXiv preprint arXiv:2410.05451, 2024.

Sizhe Chen, Julien Piet, Chawin Sitawarin, and David Wagner. {StruQ}: Defending against
  prompt injection with structured queries. In 34th USENIX Security Symposium (USENIX
  Security 25), pages 2383–2400, 2025.

Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith.
  Counterexample-guided abstraction refinement for symbolic model checking. Journal
  of the ACM (JACM), 50(5):752–794, 2003.

                                             22
                                       CaMeLoT




Edmund M Clarke and E Allen Emerson. Design and synthesis of synchronization skeletons
  using branching time temporal logic. In Workshop on logic of programs, pages 52–71.
  Springer, 1981.

Itay Cohen, Klaus Havelund, Moran Omer, and Doron Peled. Temporal guardrails for
   LLM conversations: A runtime verification framework. In AI Verification: Third In-
   ternational Symposium, SAIV 2026, Lisbon, Portugal, July 24–25, 2026, Proceedings,
   page 145–166, Berlin, Heidelberg, 2026. Springer-Verlag. ISBN 978-3-032-32356-9. doi:
   10.1007/978-3-032-32357-6 7. URL https://doi.org/10.1007/978-3-032-32357-6_7.

CrowdStrike. Charlotte AI product documentation.         https://www.crowdstrike.com/
  en-us/platform/charlotte-ai/, 2025.

Jian Cui, Zichuan Li, Luyi Xing, and Xiaojing Liao. Maris: A formally verifiable privacy
  policy enforcement paradigm for multi-agent collaboration systems, 2026. URL https:
  //arxiv.org/abs/2505.04799.

Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, and
  Florian Tramèr. Agentdojo: A dynamic environment to evaluate prompt injection attacks
  and defenses for LLM agents. In The Thirty-eight Conference on Neural Information
  Processing Systems Datasets and Benchmarks Track, 2024. URL https://openreview.
  net/forum?id=m1YYAQjO3w.

Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel
  Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, and Florian Tramèr. Defeating
  prompt injections by design. arXiv preprint arXiv:2503.18813, 2025.

Dorothy E Denning and Peter J Denning. Certification of programs for secure information
 flow. Communications of the ACM, 20(7):504–513, 1977.

Aarya Doshi, Yining Hong, Congying Xu, Eunsuk Kang, Alexandros Kapravelos, and
 Christian Kästner. Towards verifiably safe tool use for llm agents. arXiv preprint
 arXiv:2601.08012, 2026.

Scott Freitas and Amir Gharib. GenAI-driven threat detection with Microsoft security
  copilot, 2026. arXiv:2605.20896.

Zac Garby, Andrew D Gordon, and David Sands. The LLMbda calculus: AI agents, con-
  versations, and information flow. arXiv preprint arXiv:2602.20064, 2026.

Joseph A Goguen and José Meseguer. Security policies and security models. In 1982 IEEE
  symposium on security and privacy, pages 11–11. IEEE, 1982.

Google Cloud. Use triage and investigation agent to investigate alerts (Google security op-
 erations documentation). https://docs.cloud.google.com/chronicle/docs/secops/
 triage-investigation-agent, 2025.

Samuel Greengard. Is it possible to control AI hallucinations? Communications of
  the ACM, 69(6), 2026a. doi: 10.1145/3802602. URL https://cacm.acm.org/news/
  is-it-possible-to-control-ai-hallucinations/.

                                            23
                Nikolaou Eckhoff Flood Grov Mavroeidis Aspinall




Samuel Greengard.    That’s logical: Teaching LLMs to give better answers.
  Communications of the ACM, June 2026b.    URL https://cacm.acm.org/news/
  thats-logical-teaching-llms-to-give-better-answers/.

Yining Hong, Yining She, Eunsuk Kang, Christopher S Timperley, and Christian Kästner.
  Symbolic guardrails for domain-specific agents: Stronger safety and security guarantees
  without sacrificing utility. arXiv preprint arXiv:2604.15579, 2026.

Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning
 Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, et al. Llama
 guard: Llm-based input-output safeguard for human-ai conversations. arXiv preprint
 arXiv:2312.06674, 2023.

Adharsh Kamath, Sishen Zhang, Calvin Xu, Shubham Ugare, Gagandeep Singh, and
  Sasa Misailovic. Enforcing temporal constraints for llm agents. arXiv preprint
  arXiv:2512.23738, 2025.

Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao. Piguard: Prompt injection guardrail
 via mitigating overdefense for free. In Proceedings of the 63rd Annual Meeting of the
 Association for Computational Linguistics (Volume 1: Long Papers), pages 30420–30437,
 2025.

Hao Li, Xiaogeng Liu, CHIU Chun, Dianqi Li, Ning Zhang, and Chaowei Xiao. DRIFT:
 Dynamic rule-based defense with injection isolation for securing LLM agents. Advances
 in Neural Information Processing Systems, 38:83262–83290, 2026.

Erik Meijer. Guardians of the agents – formal verification of AI workflows. Communications
  of the ACM, 69(1):46–52, January 2026. doi: 10.1145/3777544.

Lesly Miculicich, Mihir Parmar, Hamid Palangi, Krishnamurthy Dj Dvijotham, Mirko Mon-
  tanari, Tomas Pfister, and Long T Le. Veriguard: Enhancing llm agent safety via verified
  code generation. arXiv preprint arXiv:2510.05156, 2025.

OWASP Gen AI Security Project. OWASP Top 10 for Large Language Model Applications
 2025. Technical report, OWASP Foundation, 2025. URL https://genai.owasp.org/
 resource/owasp-top-10-for-llm-applications-2025/. Accessed: 2026-05-15.

Palo Alto Networks. Palo alto networks unveils cortex AgentiX to build, deploy and
  govern the agentic workforce of the future. Press release, 28 October 2025. https:
  //www.paloaltonetworks.com/cortex/agentix, October 2025.

Keshav Ramani, Vali Tawosi, Salwa Alamir, and Daniel Borrajo. Bridging llm planning
 agents and formal methods: A case study in plan verification, 2025. URL https://
 arxiv.org/abs/2510.03469.

Jiawen Shi, Zenghui Yuan, Yinuo Liu, Yue Huang, Pan Zhou, Lichao Sun, and Neil Zhen-
  qiang Gong. Optimization-based prompt injection attack to llm-as-a-judge. In Proceedings
  of the 2024 on ACM SIGSAC Conference on Computer and Communications Security,
  pages 660–674, 2024.

                                           24
                                       CaMeLoT




Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, and
  Dawn Song. Progent: Programmable privilege control for llm agents. arXiv preprint
  arXiv:2504.11703, 2025.

Ronal Singh et al. LLMs in the SOC: An empirical study of human-AI collaboration. arXiv
  preprint, 2025. arXiv:2508.18947.

Siddhant Srinivas, Brandon Kirk, Julissa Zendejas, Michael Espino, Matthew Boskovich,
  Abdul Bari, Khalil Dajani, and Nabeel Alzahrani. Ai-augmented soc: A survey of llms
  and agents for security automation. Journal of Cybersecurity and Privacy, 5(4):95, 2025.

Haoyu Wang, Christopher M Poskitt, and Jun Sun. Agentspec: Customizable runtime
 enforcement for safe and reliable llm agents. arXiv preprint arXiv:2503.18666, 2025.

Simon Willison.     The dual LLM pattern for building AI assistants that can re-
  sist prompt injection, April 2023. URL https://simonwillison.net/2023/Apr/25/
  dual-llm-pattern/. Blog post. Accessed: 2026-05-15.

Fangzhou Wu, Ethan Cecchetti, and Chaowei Xiao. System-level defense against indi-
  rect prompt injection attacks: An information flow control perspective. arXiv preprint
  arXiv:2409.19091, 2024.

Yuhao Wu, Franziska Roesner, Tadayoshi Kohno, Ning Zhang, and Umar Iqbal. IsolateGPT:
  An Execution Isolation Architecture for LLM-Based Agentic Systems. In Network and
  Distributed System Security (NDSS) Symposium, 2025.

Shuren Xia, Qiwei Li, Taqiya Ehsan, and Jorge Ortiz. Tracefix: Repairing agent coordina-
  tion protocols with tla+ counterexamples, 2026. URL https://arxiv.org/abs/2605.
  07935.

Simon Sinong Zhan, Yao Liu, Philip Wang, Zinan Wang, Qineng Wang, Zhian Ruan,
  Xiangyu Shi, Xinyu Cao, Frank Yang, Kangrui Wang, et al. Sentinel: A multi-level
  formal framework for safety evaluation of llm-based embodied agents. arXiv preprint
  arXiv:2510.12985, 2025.

Peter Yong Zhong, Siyuan Chen, Ruiqi Wang, McKenna McCall, Ben L Titzer, Heather
  Miller, and Phillip B Gibbons. RTBAS: Defending LLM agents against prompt injection
  and privacy leakage. arXiv preprint arXiv:2502.08966, 2025.




                                           25
