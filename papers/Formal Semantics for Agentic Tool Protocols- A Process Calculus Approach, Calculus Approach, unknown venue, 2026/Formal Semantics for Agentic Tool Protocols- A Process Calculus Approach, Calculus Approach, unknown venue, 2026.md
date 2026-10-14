                                            Formal Semantics for Agentic Tool Protocols: A Process
                                                             Calculus Approach
                                                            Andreas Schlapbach, Swiss Federal Railways (SBB)
                                                                       SBB IT Berne, Switzerland
                                                                          schlpbch@gmail.com∗
                                                                                   June, 25th, 2026
arXiv:2603.24747v3 [cs.AI] 2 Jul 2026




                                                                                         Abstract
                                                  The emergence of large language model agents capable of invoking external tools has cre-
                                              ated urgent need for formal verification of agent protocols. Two paradigms dominate this
                                              space: Schema-Guided Dialogue (SGD), a research framework for zero-shot API generaliza-
                                              tion, and the Model Context Protocol (MCP), an industry standard for agent–tool integration.
                                              While both enable dynamic service discovery through schema descriptions, their formal rela-
                                              tionship remains unexplored. We present the first process calculus formalization of SGD and
                                              MCP, proving they are structurally bisimilar under a well-defined mapping Φ. We demonstrate
                                              that the reverse mapping Φ−1 is partial and lossy, revealing critical gaps in MCP’s expressivity.
                                              Through bidirectional analysis, we identify four principles—semantic completeness, explicit
                                              action boundaries, failure mode documentation, and inter-tool relationship declaration—as
                                              necessary and sufficient conditions for full behavioral equivalence. We formalize these prin-
                                              ciples as type-system extensions MCP+ , proving MCP+ ∼     = SGD. Our work provides the first
                                              formal foundation for verified agent systems and establishes schema quality as a provable
                                              safety property. Practically, this means that the current MCP specification has expressiveness
                                              gaps compared to SGD and would benefit from the proposed extensions.


                                        1     Introduction
                                        The rapid deployment of large language model (LLM) agents [20, 5] in production systems has
                                        created a critical gap: while these agents—capable of multi-step reasoning [22] and reactive tool
                                        use [24]—orchestrate complex workflows across services, we lack formal methods to verify their
                                        correctness, safety, and behavioral properties. Two paradigms have emerged to address agent–tool
                                        integration:

                                        1.1    The Schema-Guided Dialogue Systems (SGD)
                                        The SGD dataset [18] introduced a paradigm shift in task-oriented dialogue: rather than training
                                        on fixed ontologies, SGD models learn to interpret arbitrary API schemas at runtime. Key compo-
                                        nents are intents (high-level user goals), slots (parameters to collect), schemas (JSON definitions
                                        with natural-language descriptions), and state tracking (frame-based representation across turns).
                                        Dialogue state tracking has a longer history in shared tasks [23], and BERT-based encoders [8]
                                        enabled strong cross-service generalization. Fast and robust SGD trackers [11] demonstrated
                                        practical viability at scale. More recently, in-context learning has shown that few demonstra-
                                        tion examples suffice to adapt to new schemas—mirroring the zero-shot generalization that SGD
                                        pioneered [4, 16].
                                           ∗ © 2026 Andreas Schlapbach. Research supported by SBB-IT. The views expressed in this paper are the

                                        author’s own and do not necessarily reflect the views or policies of SBB. ORCID: 0009-0006-2329-2626.



                                                                                             1
1.2     Model Context Protocol (MCP)
The MCP is an open protocol that enables seamless integration between LLM applications and
external data sources and tools. The architecture comprises a host (LLM environment), a client
(protocol handler), and a server. Servers provide the fundamental building blocks for adding
context to language models via MCP. These primitives enable rich interactions between clients,
servers, and language models. It standardizes agent–tool communication through three primitives:
Firstly, Tools enable models to interact with external systems, such as querying databases, calling
APIs, or performing computations. Each tool is uniquely identified by a name and includes
metadata describing its schema. Secondly, Resources allow servers to share data that provides
context to language models, such as files, database schemas, or application-specific information.
Each resource is uniquely identified by a URI. Thirdly, Prompts allow servers to provide structured
messages and instructions for interacting with language models. Clients can discover available
prompts, retrieve their contents, and provide arguments to customize them.

1.3     Shared Core Principles
Both approaches share a core principle: agents discover and reason about services through machine-
readable schemas without retraining. This analysis is grounded in experience with an experimental
ecosystem of over 10 agents. The agents are each a domain expert, following domain-driven design
[21]. The agents are intelligently federated, coordinating through dynamically discovered schema
relationships and the MCP rather than rigid orchestration logic. This federated architecture has
revealed critical gaps between the theoretical elegance of SGD principles and the practical require-
ments of production agent systems: over 1,000 tool-to-tool dependencies must be managed, action
boundaries must be enforced deterministically, and failure modes must be recoverable without
human intervention.
    The formal relationship between the two approaches remains unexplored. Can we prove they
are equivalent? What properties are preserved under transformation? What gaps exist in either
framework? This paper’s aim is to provide answers to these questions by grounding the analysis
in process calculus.

1.4     Contributions
This paper makes the following contributions:

    1. Formal semantics for SGD and MCP using π-calculus, defining their syntax, operational
       semantics, and labeled transition systems (Section 3).
    2. Bisimulation proof showing SGD ∼ MCP under mapping Φ, establishing structural and
       behavioral equivalence (Section 4).
    3. Gorla-Style analysis of Φ showing that while it is a valid encoding it is neither surjective
       nor fully abstract (Section 5).
    4. Four principles as type system formalizing necessary conditions for agent safety and
       schema quality. Safety can also be regarded as respecting a user’s privacy by asking for
       permission before an action (Section 6).
    5. Extended calculus MCP+ proving that adding four principles creates full bijection: MCP+ ∼
                                                                                               =
       SGD (Section 7.3).


2     Background and Related Work
Consider a ticket booking agent which needs to book a train ticket. The agent needs first to check
the user using its id. Then has has to validate if the user has a valid account and enough balance


                                                 2
to book the ticket. If the user has enough balance, the agent can book then book the ticket from
an origin to a destination at a given date and travel class. The agent needs to send to print the
ticket or send it via email.
    If the agent is an AI agent, the questions requiring formal answers include: Needs the agent to
always fetch the user? Can the third step of booking the ticket execute without the second step
of checking the balance? What happens if the third step fails after debiting the account?
    Current approaches to validate a complex ecosystems of agents rely on testing (incomplete
coverage), prompt engineering [22] (no guarantees, brittle), or human review (not scalable). Agent
frameworks grounded in BDI theory [17] offer structured reasoning, but stop short of protocol-level
verification. Formal semantics enable verification (proving safety for all executions), composition
(building complex systems from verified components), optimization (preserving equivalence under
transformation), and debugging (tracing violations to specific protocol violations).

2.1     Process Calculi for Concurrency
Process calculi provide mathematical frameworks for reasoning about concurrent, communicating
systems. The π-calculus [14] extends CCS [13] with mobile channels, enabling dynamic network
topologies; essential for agent systems where tool availability changes at runtime.
    Related work includes session types [12] for protocol verification, choreography calculi [6] for
multi-party workflows, and probabilistic process algebras for stochastic systems [7]. However, all
these frameworks assume static protocols. Agent systems require runtime schema interpretation.
Work by [3] specifies temporal logic properties for a host agent architecture covering MCP and A2A.
[15] take a different stance: they make the medium safe by construction through a type system;
our work identifies the necessary and sufficient principles for such a type system to achieve full
expressivity.
    Highly relevant but somewhat orthogonal is the work on the LLMbda Calculus by [9] by
providing a principled semantic foundation for reasoning about an agent’s behavior and safety.
The work addresses this gap by introducing an untyped call-by-value lambda calculus enriched
with dynamic information-flow control and a small number of primitives for constructing prompt-
response conversations. The calculus faithfully represents planner loops and their vulnerabilities,
including the mechanisms by which prompt injection alters subsequent computation.


3       Process Calculus Formalization
In this paper we formalize SGD and MCP as communicating processes in π-calculus, defining their
syntax, operational semantics, and observable behaviors. The π-calculus was chosen because:
First, it makes topology dynamic where processes can acquire new channel names at runtime and,
secondly, that we are accustomed to it through previous work on Piccola, a pure composition
language based on this calculus [2] [1], [19].

3.1     SGD Process Calculus
The Schema-Guided Dialogue (SGD) dataset1 consists of over 20k annotated multi-domain, task-
oriented conversations between a human and a virtual assistant. These conversations involve
interactions with services and APIs spanning 20 domains, such as banks, events, media, calen-
dar, travel, and weather. Additionally, the dataset contains unseen domains and services in the
evaluation set to quantify the performance in zero-shot or few-shot settings.

3.1.1    Syntax
The SGD data set has a well defined structure. Dialogues are represented as a list of turns, where
each turn contains either a user or system utterance. The annotations for a turn are grouped into
   1 The data set is publicly available at:   https://github.com/google-research-datasets/dstc8-schema-guided-
dialogue


                                                      3
frames, where each frame corresponds to a single service. Each turn in the single domain dataset
contains exactly one frame. In multi-domain datasets, some turns may have multiple frames.
   Based on this structure we propose a possible grammar, where n is a name (string), d a natural-
language description, R a list of required slots, O a list of optional slots, and t ∈ {true, false} a
transactionality flag:


                 S ::= Intent⟨n, d, R, O, t⟩                           intent with metadata
                       | Slot⟨name, type, values⟩                      slot definition
                       | CollectSlot⟨s, v⟩ . S                         slot collection, then S
                       | Execute⟨intent, bindings⟩                     API invocation
                       | Result⟨output⟩                                return value
                       | Error⟨type, msg⟩                              error state
                       | S1 | S2                                       parallel composition
                       | (ν c) S                                       channel restriction
                       | !S                                            replication
                       |0                                              null process

3.1.2    Example: Train Booking in SGD
The example illustrates the intent to book a train, where origin, destination and date need to be
set and a confirmation is required before booking.
BookTrainIntent = Intent<
  name = "BookTrain",
  description = "Books a train ticket",
  R = [Slot<"from", "string", ["8507000", "8508050"]>,
       Slot<"to", "string", ["8507000", "8508050"]>,
       Slot<"date", "date", []>],
  O = [Slot<"class", "string", ["economy", "business"]>],
  t = true // Transaction requires confirmation
>


3.1.3    Operational Semantics
The transition rules for SGD processes are given in Figure 1.

3.2     MCP Process Calculus
3.2.1    Syntax
The set of MCP processes is defined by the following grammar, where schema is a JSON Schema
object and uri a resource identifier2 :
  2 With the latest release of the MCP specification the protocol is sessionless and SEP-2567: Sessionless MCP via

Explicit State Handles




                                                        4
                                    ∀r ∈ R. r ∈ dom(params)
                                                                                         SGD-Invoke-Ok
                                           invoke(n, params)
                  Intent⟨n, d, R, O, t⟩ −−−−−−−−−−−→ Execute⟨n, params⟩

                                    ∃r ∈ R. r ∈
                                              / dom(params)
                                                                                              SGD-Invoke-Err
                                    invoke(n, params)
             Intent⟨n, d, R, O, t⟩ −−−−−−−−−−−→ Error⟨MissingSlots, R \ params⟩

                                                                               SGD-Collect
                                                      collect(s,v)
                           CollectSlot⟨s, v⟩ . S −−−−−−→ S[s 7→ v]
                                                 t=true
                                            require_approval
                                        output=invoke_api(n,b)
                                                execute
                                                                            SGD-Execute-Tx
                               Execute⟨n, b⟩ −−−−→ Result⟨output⟩

                                                t=false
                                        output=invoke_api(n,b)
                                               execute
                                                                            SGD-Execute
                               Execute⟨n, b⟩ −−−−→ Result⟨output⟩
                                                  α
                                                → S1′
                                             S1 −
                                                  α                  SGD-Par
                                                → S1′ | S2
                                        S1 | S2 −
                                                  α
                                               S−
                                                → S′
                                                c∈α
                                                 /
                                                 α                   SGD-Res
                                                → (ν c) S ′
                                        (ν c) S −


                     Figure 1: Operational semantics for SGD processes.




             M ::= Tool⟨n, d, schema⟩                                  tool definition
                   | Resource⟨uri , content⟩                           read-only resource
                   | Prompt⟨template, args⟩                            workflow template
                   | ToolsList⟨metadata⟩                               discovery response
                   | ToolCall⟨n, params⟩                               tool invocation
                   | Validate⟨params, schema⟩                          parameter validation
                   | Execute⟨n, params⟩                                tool execution
                   | Result⟨output⟩                                    return value
                   | Error⟨type, msg⟩                                  error state
                   | M1 | M2                                           parallel composition
                   | (ν c) M                                           channel restriction
                   | !M                                                replication
                   |0                                                  null process

3.2.2   Example: Train Booking in MCP
This example invokes the tool bookTrainTool. In MCP the fact that the invocation needs a
confirmation by the user and that class is an optional parameter can only be expressed in the
description text.



                                                   5
BookTrainTool = Tool<
  name = "book_train",
  description = "Books a train ticket, needs confirmation",
  schema = {
    "type": "object",
    "required": ["from", "to", "date"],
    "properties": {
      "from": {"type": "string", "description": "Origin Code"},
      "to": {"type": "string", "description": "Destination Code"},
      "date": {"type": "string", "description": "Date of Travel"},
      "class": {"type": "string", "description": "Class (default: economy)"}
    }
  }
>


3.2.3   Operational Semantics
The transition rules for MCP processes are given in Figure 2.


                                                                            MCP-Discover
                                         list(f )
                       ToolsList⟨tools⟩ −−−→ {t ∈ tools | matches(t, f )}

                                                                                MCP-Call
                                       call(n, params)
                  Tool⟨n, d, schema⟩ −−−−−−−−−→ Validate⟨params, schema⟩

                                   conforms(params, schema)
                                                         τ                  MCP-Validate-Ok
                       Validate⟨params, schema⟩ −
                                                → Execute⟨n, params⟩

                                  ¬ conforms(params, schema)
                                               τ                                 MCP-Validate-Err
                Validate⟨params, schema⟩ −
                                         → Error⟨ValidationError, violations⟩

                                output = invoke_tool(n, params)
                                                    execute
                                                                        MCP-Execute
                          Execute⟨n, params⟩ −−−−→ Result⟨output⟩

                                                                            MCP-Resource
                                                    read(uri)
                       Resource⟨uri , content⟩ −−−−−→ Result⟨content⟩


                      Figure 2: Operational semantics for MCP processes.


3.3     Labeled Transition Systems
For both SGD and MCP we define a labeled transition system. In both systems, the parameter
n denotes the tool/intent name, p denotes the parameter, t denotes the error type, m the error
message and o the object type.
Definition 3.1 (SGD LTS). The labeled transition system for SGD is the tuple
(States SGD , Labels SGD , →SGD ) where:
                       States SGD = {S | S is a well-formed SGD process}
                       Labels SGD = {invoke(n, p), collect(s, v),
                                     execute, result(o), error(t, m)}
                           →SGD ⊆ States SGD × Labels SGD × States SGD


                                                    6
where s denotes the slot and v denotes the values.
Definition 3.2 (MCP LTS). The labeled transition system for MCP is the tuple
(States MCP , Labels MCP , →MCP ) where:

                       States MCP = {M | M is a well-formed MCP process}
                       Labels MCP = {call(n, p), list(f ), τ, execute,
                                      result(o), error(t, m), read(u)}
                           →MCP ⊆ States MCP × Labels MCP × States MCP

where u denotes a universal resource identifier (URI).
   Silent (τ ) actions are collect(s, v) and validate. Observable actions are invoke(n, p), call(n, p),
execute, result(·), error(·, ·), and read(·).


4       Forward Bisimulation: SGD → MCPSGD -> MCP
4.1     Mapping Function Φ
Phi

Definition 4.1 (Schema Mapping Φ : SGD → MCP).

          Φ(Intent⟨n, d, R, O, t⟩) = Tool⟨n, d, schema(R, O)⟩
                                     n
           where schema(R, O) = ”type”: ”object”, ”required”: [s.name | s ∈ R],
                                                                                    o
                                       ”properties”: {s.name : prop(s) | s ∈ R ∪ O}

                           prop(s) = {”type”: s.type, ”description”: s.desc}
                                     ∪ ({”enum”: s.vals} if s.vals ̸= ∅)
         Φ(Execute⟨n, bindings⟩) = ToolCall⟨n, JSON.encode(bindings)⟩
                     Φ(Result⟨o⟩) = Result⟨o⟩
                   Φ(Error⟨t, m⟩) = Error⟨t, m⟩
                        Φ(S1 | S2 ) = Φ(S1 ) | Φ(S2 )
                        Φ((ν c) S) = (ν c) Φ(S)
                            Φ(!S) = !Φ(S)
                             Φ(0) = 0

4.2     Forward Mapping Examples
4.2.1    Φ Mapping of Train Intent

SGD_Train = Intent<
  "BookTrain",
  "Books a Train",
  [Slot<"from", "string", ["8507000", "8508050"]>],
  [],
  true
>

phi(SGD_Train) = Tool<
  "BookTrain",


                                                   7
    "Books a Train",
    {
      "type": "object",
      "required": ["from"],
      "properties": {
        "from": {
          "type": "string",
          "description": "Departure station",
          "enum": ["8507000", "8508050"]
        }
      }
    }
>



4.3     Action Equivalence
Definition 4.2 (Action Equivalence ≈).

        invoke(n, p) ≈ call(n, p),          list(f ) ≈ list(f ),   collect(s, v) ≈ τ,
            execute ≈ execute,          result(o) ≈ result(o),      error(t, m) ≈ error(t, m)



4.4     Bisimulation and Main Theorem
We write S ∼ M iff there exists a weak bisimulation R with (S, M ) ∈ R.
Theorem 4.3 (SGD ∼ MCP under Φ). ∀S ∈ SGD. S ∼ Φ(S).
Proof. Define R = {(S, Φ(S)) | S ∈ SGD}. We prove R is a weak bisimulation by structural
induction.
Lemma 4.4 (Intent ∼ Tool). Intent⟨n, d, R, O, t⟩ ∼ Tool⟨n, d, schema(R, O)⟩.
                                       invoke(n, p)
Proof. Suppose Intent⟨n, d, R, O, t⟩ −−−−−−−→ S ′ .
   Case 1: p satisfies all slots in R. Then S ′ = Execute⟨n, p⟩. For the tool:
                                     call(n, p)                    τ
                Tool⟨n, d, schema⟩ −−−−−→ Validate⟨p, schema⟩ −
                                                              → Execute⟨n, p⟩

Since schema(R, O).required = [s.name | s ∈ R], validation succeeds iff p satisfies R. By defini-
tion, Execute⟨n, p⟩ ∼ Execute⟨n, p⟩. ✓
    Case 2: p missing required slots. Then S ′ = Error⟨MissingSlots, R \ p⟩. The tool produces
Error⟨ValidationError, R \ p⟩ via the MCP-Validate-Err rule; error terms are observationally
equivalent. ✓
    The backward direction is symmetric by construction of Φ.
   Equivalently, S and Φ(S) produce the same observable traces up to τ -absorption, so any
execution sequence demonstrating safe behaviour in SGD lifts to MCP and vice versa.
Lemma 4.5 (Execution Preservation).

                Execute⟨n, bindings⟩SGD ∼ Execute⟨n, JSON.encode(bindings)⟩MCP .

Proof. Both processes transition via execute to Result⟨o⟩ where o = invoke_api(n, bindings). JSON
encoding is a bijection on well-typed parameters, so

                        invoke_api(n, b) = invoke_api(n, decode(encode(b))).




                                                      8
Induction.
Base case (S = 0): Φ(0) = 0 and 0 ∼ 0 trivially.
                                                                      α                                β
                                                              → S1′ | S2 then by IH Φ(S1 ) −
Inductive case (S = S1 | S2 ): By IH, Si ∼ Φ(Si ). If S1 | S2 −                            → M1′
                                                      β
with S1′ ∼ M1′ and α ≈ β, hence Φ(S1 ) | Φ(S2 ) −   → M1′ | Φ(S2 ), and (S1′ | S2 ) ∼ (M1′ | Φ(S2 )). The
symmetric case for S2 is identical.
Inductive case (S = Intent⟨n, d, R, O, t⟩): By Lemma 4.4.
Inductive case (S = (ν c) S ′ ): Φ((ν c) S ′ ) = (ν c) Φ(S ′ ). By IH, S ′ ∼ Φ(S ′ ). Channel restriction
preserves bisimulation (standard π-calculus result [14]).
Corollary 4.6 (Zero-Shot Generalization Transfer). If an SGD model handles Intent I zero-shot
via schema s, then an MCP model handles Tool⟨·, ·, Φ(s)⟩ zero-shot via Φ(s).


5     The Reverse Direction: A Gorla-Style Analysis
Section 4 exhibited a mapping Φ and proved S ∼ Φ(S). We now ask the question this raises in
the language of encodability: is Φ a good encoding, and does a good encoding run the other way?
We adopt Gorla’s criteria for language encodings [10] and show that Φ is a valid encoding which
is, however, neither surjective nor fully abstract. These two failures are precisely the gaps that
Sections 6–7 close.

5.1     Encoding Criteria
Definition 5.1 (Valid encoding [10]). An encoding (J·K, φ) of source calculus Ls into target Lt ,
with translation J·K and renaming policy φ, is valid if:
Compositionality C1 For every operator op there is a target context C op [ ·1 , . . . , ·k ] with Jop(P1 , . . . , Pk )K =
   C op [JP1 K, . . . , JPk K].
Name invariance C2 Jσ(P )K = σ ′ (JP K) for σ ′ induced by σ through φ.

Operational correspondence C3 Completeness: P =⇒s P ′ implies JP K =⇒t ∼ JP ′ K. Sound-
    ness: JP K =⇒t T implies ∃P ′ . P =⇒s P ′ and T =⇒t ∼ JP ′ K.
Divergence reflection C4 JP K diverges only if P diverges.
Success sensitiveness C5 P ⇓s ✓ iff JP K ⇓t ✓ for a success barb ✓.

Definition 5.2 (Full abstraction). A valid encoding is fully abstract if it preserves and reflects
the source equivalence: P ∼s Q ⇐⇒ JP K ∼t JQK.

5.2     Φ is a Valid Encoding
Proposition 5.3 (Validity of Φ). (Φ, id) is a valid encoding of SGD into MCP.
Proof. (C1 ) Definition 4.1 is homomorphic on the operators (Φ(S1 | S2 ) = Φ(S1 ) | Φ(S2 ), and
likewise for (νc), !, 0); the witnessing contexts are the operators themselves, name-independent.
(C2 ) Φ copies the name n through and never branches on name identity; with φ = id, invariance
is immediate. (C3 ) Theorem 4.3 (S ∼ Φ(S)) is an operational correspondence up to ∼. (C4 ) The
only τ -steps Φ introduces are the administrative validate transitions, one per invocation (MCP-
Validate-Ok); they cannot chain, so no divergence is added. (C5 ) With ✓ the result barb,
S ∼ Φ(S) and barb-respect of ∼ give the equivalence.
Φ is thus exactly the structure-preserving translation the encodability literature certifies. The rest
of the section identifies the two ways it falls short of an equivalence of calculi.




                                                      9
5.3     Φ is Not Surjective
The reverse map Φ−1 is defined only on the image of Φ. On the executable Tool fragment it is the
expected inverse; on the remaining primitives it is undefined.
Definition 5.4 (Partial inverse Φ−1 ).

                 Φ−1 (Tool⟨n, d, schema⟩) = Intent⟨n, d, R(schema), O(schema), ? ⟩,

with

      R(schema) = {Slot⟨x, schema.prop[x], enum⟩ | x ∈ schema.required},
      O(schema) = {Slot⟨y, schema.prop[y], enum⟩ | y ∈ schema.properties \ schema.required},

where enum denotes the values from the JSON schema’s enum field (or ∅ if absent). The flag t is
left undetermined (?), and Φ−1 is undefined on Resource, Prompt, and ToolsList.
Theorem 5.5 (Non-surjectivity). Image(Φ) ⊊ MCP. In particular Resource⟨·, ·⟩, Prompt⟨·, ·⟩, and
the discovery process ToolsList⟨·⟩ lie outside Image(Φ).
Proof. By Definition 4.1, Φ produces only Tool terms under the closure operators; Resource,
Prompt, and ToolsList are none of these, so no S has Φ(S) headed by them.
Remark 5.6 (An image fact, not a separation). Theorem 5.5 says these primitives are absent
from the image of Φ, not that they are inexpressible in SGD. We make no separation claim: with
replication and channel mobility, SGD admits degenerate encodings of both (a passive resource
as an empty-slot intent returning its content; discovery via input-guarded choice). The point is
structural – these are primitives SGD lacks as primitives – so the canonical inverse Φ−1 , which
must respect primitive structure, cannot be total. They are surplus to be quarantined (Section 7),
not gaps to be closed.

5.4     Φ is Not Fully Abstract
The substantive gap is not non-surjectivity but the failure of Φ to reflect behavioural equivalence:
Φ collapses SGD distinctions that MCP cannot observe.
Theorem 5.7 (Φ does not reflect ∼). There exist S1 , S2 ∈ SGD with S1 ̸∼ S2 and Φ(S1 ) ∼ Φ(S2 ).
Hence Φ is not fully abstract.
Proof. Let S1 = Intent⟨n, d, R, O, true⟩ and S2 = Intent⟨n, d, R, O, false⟩, equal but for t. They are
distinguished by the approval gate: by SGD-Execute-Tx, S1 requires approval before execute,
whereas S2 proceeds via SGD-Execute without it. Under any equivalence observing the approval
interaction – made explicit at the process level by the prefix approval?⟨confirm⟩ of Section 6.2 –
we have S1 ̸∼ S2 . Yet Φ(S1 ) = Tool⟨n, d, schema(R, O)⟩ = Φ(S2 ): the flag t is carried by no field
of schema, surviving at best as prose in a description string that MCP’s rules do not interpret.
Identical terms are bisimilar, so Φ(S1 ) ∼ Φ(S2 ).
The collapse is concrete. A tool that needs user approval before reading an account loses precisely
that requirement on the way back to SGD:
M_1 = Tool<
  "fetch_user",
  "fetch a user’s data, needing its approval",
  { "type": "object", "required": ["user_id"],
    "properties": { "user_id": {"type": "string"} } }
>

Phi^{-1}(M_1) = Intent<
  "fetch_user", "fetch a user’s data, needing its approval",


                                                 10
    [Slot<"user_id", "string", []>], [],
    ?   // UNDEFINED: is_transactional cannot be recovered
>

The is_transactional flag is critical for safety (it gates user approval) but is absent from MCP
schemas. Inference from the description string is unreliable and not compositionally verifiable.
Corollary 5.8 (Lossy round trip, non-injective inverse). Φ−1 ◦Φ ̸= idSGD , and Φ−1 is not injective
where defined.
Proof. The round trip drops t: starting from a transactional intent,
S = Intent<"book_ticket", ..., ..., ..., true>

Phi(S) = Tool<"book_ticket", ..., schema>
         (is_transactional lost)

Phi^{-1}(Phi(S)) = Intent<"book_ticket", ..., ..., ..., ?>
                   != S

so Φ−1 ◦ Φ ̸= id; the lost information includes the transactionality flag, error-recovery strategies,
and tool dependencies encoded in dialogue flow. Dually, two tools differing only in description –
hence in implicit side effects MCP does not structurally parse – have the same image under Φ−1 :
M_1 = Tool<"book_ticket", "Books a ticket", schema>

M_2 = Tool<"book_ticket",
           "Books a ticket [SIDE EFFECT: sends email]",
           schema>   // same schema, different implicit side effects

Phi^{-1}(M_1) = Phi^{-1}(M_2)
              = Intent<"book_ticket", ..., is_transactional=?>

Since Φ−1 does not parse descriptions structurally, distinct tools collapse to one intent.

Remark 5.9 (What is collapsed). Theorem 5.7 isolates one collapsed coordinate, the flag t.
The same failure recurs for every SGD datum that MCP records only as prose: error-recovery
behaviour and inter-tool ordering are observable in SGD executions yet invisible to MCP’s rules.
Each collapsed coordinate is a distinction Φ fails to reflect.

5.5     Diagnosis: Exactly Four Coordinates
The two failures have different remedies. Non-surjectivity (Section 5.3) is benign: the surplus
primitives are restricted away, leaving the executable fragment MCP+ of Section 7. Non-full-
abstraction (Section 5.4) is the failure that demands new structure: for Φ to reflect ∼, every SGD
distinction must become a machine-readable, operationally interpreted coordinate of the target.
There are exactly four collapsed coordinates, giving the four principles of Section 6:

P1 (semantic completeness) makes the description recoverable as slot semantics, so Φ−1 re-
     constructs slots reliably rather than parsing prose;
P2 (explicit action boundaries) makes t a first-class observable (requires_approval), repairing
     exactly the collapse of Theorem 5.7 and Corollary 5.8;

P3 (failure mode documentation) makes error-recovery branches observable, so behavioural
     equivalence holds on error paths;
P4 (inter-tool relationship declaration) makes dialogue-flow dependencies explicit, so tool
     sequencing is not lost.


                                                 11
    Section 7 shows these four extensions make Φ+ fully abstract on the executable fragment, and
that they are minimal – dropping any one reinstates a collapsed coordinate and breaks reflection
– yielding the fully abstract bijection SGD ∼
                                            = MCP+ .


6       Four Principles as Type-System Extensions
We formalize four design principles as type-system extensions to close the gaps identified in the
previous section.

6.1     Principle 1: Semantic Completeness
Informal : Descriptions must convey why parameters exist, not merely their types.
Definition 6.1 (Semantic Density).
                                                         |entities(s)|
                                     sem_density(s) =
                                                          |tokens(s)|
where entities(s) counts named entities, examples, and constraints in string s, and θ is a threshold
(e.g., 0.2).
Type Rule (P1):
                               Γ ⊢ desc : String sem_density(desc) ≥ θ
                                                                       WellDescribed
                               Γ ⊢ {description: desc} : WellDescribed

6.1.1    Principle P1 : Semantic Completeness Examples
Violates P1:
"departure": {"type": "string", "description": "departure"}
// sem_density = 0 (no new information)

    Satisfies P1:
"departure": {
  "type": "string",
  "description": "UIC station code (e.g., 8507000, 8508050)"
}
// sem_density = 2/10 = 0.2, includes concept + 2 examples


6.2     Principle P2 : Explicit Action Boundaries
Informal : Tools must signal if invocation causes side effects: side_effects := read | write | delete |
none.
Type Rule (P2):
                                   meta.side_effects ∈ {write, delete}
                                                                       WriteApproval
                                    meta.requires_approval = true
The process-level encoding of a write-capable tool is:
                    Toolwrite = call?⟨params⟩ . approval?⟨confirm⟩.
                                   confirm = true → execute⟨params⟩ . result!⟨ok⟩ . 0
                                                                            
                                  | confirm = false → result!⟨cancelled⟩ . 0
Safety as well as privacy can both be regarded as action boundaries. In both cases, a user is asked
for permission before an action.

                                                   12
6.2.1   Principle P2 : Explicit Action Boundaries Example

Tool<
  "delete_user",
  "Permanently deletes a user account",
  { "type": "object", "required": ["user_id"],
    "properties": { "user_id": {"type": "string"} } },
  metadata = {
    side_effects: delete,
    requires_approval: true   // enforced by type rule WriteApproval
  }
>

Theorem 6.2 (No Unapproved Side Effects). ∀ Tool with side_effects ∈ {write, delete}: in every
execution trace, execute is preceded by approval.

6.3     Principle P3 : Failure Mode Documentation
Informal : Enumerate expected error conditions and recovery strategies.


            failure_modes ::= [(ErrorType, RecoveryStrategy)]
                ErrorType ::= ValidationError | AuthError | ServiceDown | NotFound | · · ·
         RecoveryStrategy ::= Retry(n) | Fallback(tool ) | UserPrompt(m) | Abort

6.3.1   Failure Mode Documentation Example

Tool<
  "fetch_user_data",
  "Retrieves user information from database",
  schema,
  metadata = {
    failure_modes: [
      (NotFound,     UserPrompt("User does not exist. Create new?")),
      (ServiceDown, Retry(3)),
      (AuthError,    Fallback("use_cached_data"))
    ]
  }
>

A robust tool is encoded as:
                       Toolrobust = execute?⟨params⟩.
                                      success!⟨output⟩ . 0
                                      | error!⟨NotFound, rec 1 ⟩ . rec 1 . 0
                                                                                  
                                      | error!⟨ServiceDown, rec 2 ⟩ . rec 2 . 0
where each rec i corresponds to the declared recovery strategy.

6.4     Principle P4 : Inter-Tool Relationship Declaration
Informal : Express dependencies between tools explicitly.


                  dependencies ::= [(tool _name, relation)]
                       relation ::= Requires | ProducesInputFor | ExclusiveWith

                                                 13
6.4.1    Inter-Tool Relationship Declaration Example

Tool<
  "process_payment",
  "Processes a payment transaction",
  schema,
  metadata = {
    dependencies: [
      ("create_order",   Requires), // must call create_order first
      ("verify_balance", Requires)   // must verify balance
    ]
  }
>

The process encoding of a dependent pair (TA , TB ) with TB .dependencies = [(TA , Requires)]:

             TA = executeA ?⟨params⟩ . resultA !⟨id , {for: TB }⟩ . 0
             TB = requires?⟨id from TA ⟩ . executeB ?⟨id , params⟩ . resultB !⟨data⟩ . 0

Theorem 6.3 (Dependency Safety). ∀ workflow W composed of tools {T1 , . . . , Tn }: if Ti .dependencies =
[(Tj , Requires)], then in all valid execution traces executeTj precedes executeTi .


7       Extended Calculus MCP+ MCP+ and Full Equivalence
7.1     MCP+ Syntax
MCP+ is the executable fragment of the extended calculus. The Resource and Prompt terms,
identified in §5.3 as outside Image(Φ), are quarantined and not part of the fully abstract bijection.
The terms of MCP+ are generated by:

                                M + ::= Tool⟨n, d, schema⟩+ [meta]
                                          | M+ ∥ M+
                                          | (νc) M +
                                          | !M +
                                          | 0
where [meta] denotes the metadata block meta = {. . . (unchanged) . . .}. Additionally, Tool+
carries additional metadata:

                                
                  metadata =     side_effects : {read, write, delete, none},
                                requires_approval : Bool,
                                failure_modes : [(ErrorType, RecoveryStrategy)],
                                summary : String,
                                dependencies : [(tool _name, relation)]




                                                   14
7.2    Extended Mapping Φ+ Phi+

           Φ+ (Intent⟨n, d, R, O, t⟩) = Tool⟨n, d, schema(R, O)⟩+ [meta]
                                        
                               meta = side_effects: (t ? write : read),
                                          requires_approval: t,
                                          failure_modes: extract_errors(Intent),
                                          summary: first_sentence(d),
                                     dependencies: extract_deps(Intent)

(Φ+ )−1 Tool⟨n, d, schema⟩+ [meta] = Intent⟨n, d, R(schema), O(schema), t⟩
                                  

                              where t = (meta.side_effects ∈ {write, delete}) (must satisfy WriteApproval invariant
                                          if t then meta.requires_approval holds)

7.3    Main Theorem: Full Equivalence
Theorem 7.1 (MCP+ ∼
                  = SGD). The following hold:
  1. ∀S ∈ SGD. S ∼ Φ+ (S),
  2. ∀M + ∈ MCP+ . M + ∼ (Φ+ )−1 (M + ),
  3. (Φ+ )−1 ◦ Φ+ = idSGD ,
  4. Φ+ ◦ (Φ+ )−1 = idMCP+ .
Proof. Part 1 (Φ+ preserves structure): Φ+ extends Φ with metadata. By Theorem 4.3, structural
bisimulation is preserved. The metadata fields preserve SGD semantics:
                                      t ↔ side_effects, requires_approval ,
                                     d ↔ summary,
                       errors in Intent ↔ failure_modes,
                       inter-tool deps ↔ dependencies.
I.e. the SGD semantics are preserved: the transactionality flag t corresponds to side_effects
and requires_approval; the description d to summary; errors in the Intent to failure_modes; and
inter-tool dependencies to dependencies.
    Part 2 (injectivity): Assume Φ+ (S1 ) = Φ+ (S2 ). Then n1 = n2 , schema(R1 , O1 ) = schema(R2 , O2 )
implying R1 = R2 , O1 = O2 , and meta 1 = meta 2 implying t1 = t2 . Hence S1 = S2 .
    Part 3 (surjectivity): For any M + = Tool⟨n, d, schema⟩+ [meta], write req = schema.required
and prp = schema.properties for brevity. Let R∗ = (Φ+ )−1 (req), O∗ = (Φ+ )−1 (prp \ req), and
t∗ = (meta.side_effects ̸= read). Construct S = Intent⟨n, d, R∗ , O∗ , t∗ ⟩. Then Φ+ (S) = M + .
    Part 4 (round-trip identity): Verified by direct substitution into Definitions 4.1 and the ex-
tended mapping.
Corollary 7.2 (Necessity and Sufficiency). The four principles are necessary and sufficient for
SGD ∼
    = MCP+ .
Proof. Sufficiency: Theorem 7.1. Necessity: removing any of the four Principles breaks the bijec-
tion (shown in Section 5).
    The four principles are a minimal extension to MCP needed for SGD ∼          = MCP+ . This can
                                                            + −1
be shown by necessity analysis: Remove P1 and (Φ )                cannot map descriptions to SGD slot
semantics reliably; zero-shot generalization fails. Remove P2 and is_transactional is unrecover-
able; (Φ+ )−1 (Tool+ ) yields Intent⟨·, ·, ·, ·, ?⟩; not injective. Remove P3 and SGD error-recovery
strategies cannot be encoded; behavioral equivalence fails on error paths. Finally, remove P4 and
multi-turn dialogue dependencies are lost; tool sequencing becomes implicit.


                                                 15
8    Conclusion
We have presented a formal semantics for agentic tool protocols, proving that SGD and MCP are
structurally bisimilar under the mapping Φ (Theorem 4.3). However, Φ−1 is partial and lossy
(Theorems 5.5 and 5.7), revealing four critical gaps in MCP’s expressivity. Through bidirectional
analysis we identified four principles as necessary and sufficient conditions for full behavioral
equivalence, and formalized them as type-system extensions defining MCP+ with MCP+ ∼         = SGD
(Theorem 7.1).
    As LLM agents govern financial transactions, healthcare decisions, and infrastructure manage-
ment, formal verification becomes essential. A natural synthesis of this work is to combine the work
on LLMbda calculi [9] and this work on formalizing agentic communication. While the first would
define the intra-agent communication, the latter would define the inter-agent communication.


References
 [1] Franz Achermann (2002): Forms, Agents and Channels – Defining Composition Abstraction
     with Style. Ph.D. thesis, University of Berne.
 [2] Franz Achermann, Markus Lumpe, Jean-Guy Schneider & Oscar Nierstrasz (2001): Piccola
     – A Small Composition Language. In Howard Bowman & John Derrick, editors: Formal
     Methods for Distributed Processing – A Survey of Object-Oriented Approaches, Cambridge
     University Press, pp. 403–426.
 [3] Edoardo Allegrini, Ananth Shreekumar & Z. Berkay Celik (2026): Formalizing the Safety,
     Security, and Functional Properties of Agentic AI Systems. arXiv:2510.14133.
 [4] Ankur Bapna, Gokhan Tür, Dilek Hakkani-Tür & Larry Heck (2017): Towards Zero-Shot
     Frame Semantic Parsing for Domain Scaling. In: Proc. Interspeech 2017, pp. 2476–2480,
     doi:10.21437/Interspeech.2017-518. arXiv:1707.02363.
 [5] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhari-
     wal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agar-
     wal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh,
     Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler,
     Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCan-
     dlish, Alec Radford, Ilya Sutskever & Dario Amodei (2020): Language Models are Few-Shot
     Learners. Advances in Neural Information Processing Systems 33.
 [6] Marco Carbone, Luís Caires & Hugo Torres Vieira (2012): Choreographies, Logically. In: Int.
     Conf. on Concurrency Theory (CONCUR), LNCS 7454, Springer, pp. 65–79.
 [7] Pedro R. D’Argenio et al. (2022): Probabilistic Process Algebras. In: Handbook of Process
     Algebra, Elsevier.
 [8] Jacob Devlin, Ming-Wei Chang, Kenton Lee & Kristina Toutanova (2019): BERT: Pre-
     training of Deep Bidirectional Transformers for Language Understanding. Proc. of the 2019
     Conf. of the North American Chapter of the Association for Computational Linguistics.
 [9] Zac Garby, Andrew D. Gordon & David Sands (2026): The LLMbda Calculus: AI Agents,
     Conversations, and Information Flow. arXiv:2602.20064.
[10] Daniele Gorla (2010): Towards a unified approach to encodability and separation
     results for process calculi. Information and Computation 208(9), pp. 1031–1053,
     doi:10.1016/j.ic.2010.05.002.
[11] Suman Gupta, Rana Sharma & Kumar Singh (2020): A Fast and Robust BERT-based Dia-
     logue State Tracker for Schema-Guided Dialogue Dataset. CEUR-WS, Vol-2666.


                                                16
[12] Kohei Honda, Vasco T. Vasconcelos & Makoto Kubo (1998): Language Primitives and Type
     Discipline for Structured Communication-Based Programming. In: European Symposium on
     Programming (ESOP), LNCS 1381, Springer, pp. 122–138.
[13] Robin Milner (1989): Communication and Concurrency. Prentice Hall.

[14] Robin Milner (1999): Communicating and Mobile Systems: The π-Calculus. Cambridge
     University Press.
[15] Martin Odersky, Yaoyu Zhao, Yichen Xu, Oliver Bracevac & Cao Nguyen Pham (2026):
     Tracking Capabilities for Safer Agents. arXiv:2603.00991.
[16] Mark Palatucci, Dean Pomerleau, Geoffrey E. Hinton & Tom M. Mitchell (2009): Zero-
     Shot Learning with Semantic Output Codes. In: Advances in Neural Information Processing
     Systems (NIPS), 22, pp. 1410–1418.
[17] Anand S. Rao & Michael P. Georgeff (1995): BDI Agents: From Theory to Practice. In: Int.
     Conf. on Multi-Agent Systems (ICMAS), pp. 312–319.

[18] Abhinav Rastogi, Xiaoxue Zang, Srinivas Sunkara, Raghav Gupta & Pranav Khaitan (2020):
     Towards scalable multi-domain conversational agents: The schema-guided dialogue dataset.
     In: Proc. of the AAAI Conf. on Artificial Intelligence, 34, pp. 8689–8696.
[19] Andreas Schlapbach (2003): Enabling White-Box Reuse in a Pure Composition Language.
[20] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
     Lukasz Kaiser & Illia Polosukhin (2017): Attention is All You Need. Advances in Neural
     Information Processing Systems.
[21] Vaughn Vernon (2013): Implementing Domain-Driven Design. Addison-Wesley Professional.
[22] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Ichien, Ed H. Chi, Quoc V.
     Le & Denny Zhou (2022): Chain-of-Thought Prompting Elicits Reasoning in Large Language
     Models. Advances in Neural Information Processing Systems 35.
[23] Jason D. Williams, Antoine Raux & Matthew Henderson (2016): The Dialog State Tracking
     Challenge Series: A Review. Dialogue and Discourse 7(3), pp. 4–33.
[24] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan & Yuan
     Cao (2023): ReAct: Synergizing Reasoning and Acting in Language Models. In: Proc. of the
     11th Int. Conf. on Learning Representations.




                                             17
