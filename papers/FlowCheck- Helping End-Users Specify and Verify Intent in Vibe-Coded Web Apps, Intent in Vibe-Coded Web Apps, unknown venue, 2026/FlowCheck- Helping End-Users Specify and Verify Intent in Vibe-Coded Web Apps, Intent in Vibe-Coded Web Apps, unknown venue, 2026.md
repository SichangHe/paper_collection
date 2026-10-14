                                             FlowCheck: Helping End-Users Specify and Verify
                                                    Intent in Vibe-Coded Web Apps
                                                                     Reya Vir                                                      Lydia Chilton
                                                                    Columbia University                                              Columbia University
                                                                 New York, USA                                                     New York, USA
                                                             reyavir@cs.columbia.edu                                          chilton@cs.columbia.edu

                                                                   Zhuo Zhang                                                       Eugene Wu
                                                                     Columbia University                                           Columbia University
                                                                  New York, USA                                                  New York, USA
arXiv:2608.28880v1 [cs.SE] 28 Aug 2026




                                                               zz3474@columbia.edu                                             ewu@cs.columbia.edu
                                         Abstract                                                             October 4–9, 2026, Oakland, CA, USA. ACM, New York, NY, USA,
                                         Vibe-coded applications often contain silent behavioral fail-        14 pages. https://doi.org/10.1145/3843750.3843844
                                         ures in which the interface appears functional even though
                                         user-visible information does not flow to the expected state         1    Introduction
                                         or output. We introduce FlowCheck, a constraint language to             Large language model (LLM) coding agents have democra-
                                         specify these user-visible information flows directly through           tized software development. End users with little program-
                                         the application interface, where constraints can also be dis-           ming experience can now “Vibe code” complex applications
                                         played and inspected without reading code, and are struc-               and iterate on their features via natural language. These
                                         tured enough for reliable LLM generation. FlowCheck trans-              Vibe Coders evaluate progress primarily by interacting with
                                         lates the constraints into deterministic CodeQL analyses, and           the application rather than inspecting its implementation.
                                         we evaluate it across four applications generated via Claude            This shifts the bottleneck from writing code to determining
                                         Code, and compare with three coding models as bug-finding               whether the generated application behaves as intended.
                                         baselines. We find that FlowCheck correctly translates and                 Coding agents remain unreliable. They may misunder-
                                         flags all 30 of our injected constraint violations with no              stand requests, omit necessary state updates, introduce in-
                                         false positives. In contrast, frontier models (Claude Opus 4.7,         correct data flows, or break previously working behavior.
                                         DeepSeek V3, and Gemini Pro) showed significantly lower                 Prior work has documented incomplete implementations,
                                         accuracy when prompted to find bugs in the same code, with              regressions, and incorrect agent-generated code [7, 33]. Be-
                                         none achieving full accuracy. This approach lets vibe coders            yond code-level errors, large-scale analysis of real coding-
                                         state intent in terms of the interface they understand, and             agent sessions shows that agents frequently break down
                                         checks it deterministically against the code they do not.               on what users actually want [29]. These Silent Behavioral
                                         CCS Concepts: • Software and its engineering → Soft-                    Failures—the application runs but its observable behavior
                                         ware verification and validation; Domain specific lan-                  violates user intents—are especially difficult to detect when
                                         guages; • Human-centered computing → Interactive sys-                   the application compiles, renders normally, and produces
                                         tems and tools.                                                         plausible feedback. A button may report success even though
                                                                                                                 no data was saved, or a displayed value may update without
                                         Keywords: Vibe Coding, LLM Code Generation, End-User                    reflecting the state it is supposed to represent.
                                         Programming, Static Analysis, Software Verification                        Existing debugging techniques like unit, integration, and
                                         ACM Reference Format:                                                   end-to-end testing can validate behavior, but require users
                                         Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu. 2026. FlowCheck: to identify test cases and encode the expected result as an
                                         Helping End-Users Specify and Verify Intent in Vibe-Coded Web           executable oracle. LLM-based testing and debugging reduce
                                         Apps. In Proceedings of the 2nd ACM SIGPLAN International Work-         the authoring burden, but we find these are probabilistic
                                         shop on Language Models and Programming Languages (LMPL ’26),
                                                                                                                 and limited in the types of failures they can identify. Tra-
                                                                                                                 ditional static analysis and program verification techniques
                                                                                                                 are deterministic for predefined program properties, but are
                                         This work is licensed under a Creative Commons Attribution 4.0 Interna- designed for programmers rather than vibe coders.
                                         tional License.
                                         LMPL ’26, Oakland, CA, USA
                                                                                                                    Vibe coders therefore need a way to express what they
                                         © 2026 Copyright held by the owner/author(s).                           expect  in terms of the interface they understand and to de-
                                         ACM ISBN 979-8-4007-2986-7/2026/10                                      terministically  check whether the implementation supports
                                         https://doi.org/10.1145/3843750.3843844                                 that behavior. We focus on web applications, where user
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                       Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


intents can be expressed as constraints over flows between             models, and four iteration steps. From these, we identi-
user actions, interface-level updates, persistent state, and           fied 23 distinct failures, where nearly half (48%) can be
backend calls. For example, a user may expect that clicking            expressed and checked fully using our static constraints.
a button should update a displayed total based on an input,         2. We introduce a constraint language and interface through
or that submitting a form will persist its contents.                   which end users express expected behavior using visible
   We introduce FlowCheck, a system that expresses and                 elements, actions, and effects.
checks data and control flow constraints over visible inter-        3. We present a deterministic static-analysis system that
face elements and application effects—for instance, that an            translates these constraints into CodeQL queries and checks
action should not update a particular component, values                the required control-flow and data-flow relationships.
should derive from specific inputs, state must persist across       4. We evaluate FlowCheck on 30 injected failures across
reloads, or an action must trigger an API call. We define              four web applications (14–21 constraints each), where
a constraint language that users can express and visualize             it achieves 100% detection accuracy, compared to at most
directly in the application interface, and that can be easily          26/30 (87%) for the best LLM baseline (Claude, best prompt).
generated by LLMs. The constraints compile to static analy-            We further show that agents can author valid constraints
sis queries (CodeQL) over the application’s event handlers,            in our language, and that using them to check code raises
control and data flow, and interface and storage accesses.             the agents’ bug-catch rate on a test app, an early sign the
                                                                       language is learnable and usable by LLMs.
Example 1.1. The user asks an agent to add a promotional-
code feature to a vibe-coded shopping application. The agent
creates a promo input and an “Apply” button. When the user          2     Related Work
enters a valid code, the interface displays “Discount applied!”
even though the new total is neither persisted nor shown:           2.1   Evaluating LLM-Generated Applications
                                                                    Coding agents struggle as requirements iteratively grow,
     function applyPromo() {                                        across front-end development [31] and backend correctness
      const getById = id => document.getElementById(id);
      const code = getById('promo-input').value;                    constraints [7, 33]. We focus on silent behavioral failures:
                                                                    the application runs and presents plausible output, but user-
      if (code === 'SAVE20') {                                      visible information does not flow to the expected state or
       // read and update cart state
       let tot = parseFloat(localStorage.getItem('cartTotal'));     element. This differs from prior semantic failures [14, 15] by
       tot *= 0.8;                                                  grounding correctness in end user’s expectations.
                                                                       LiveCodeBench and DebugBench evaluate self-contained
       // Update success message in UI
       getById('promo-msg').innerText = 'Discount␣applied!';        problems with predefined input-output oracles [9, 30], while
                                                                    SWE-bench evaluates patches to existing repositories [10].
       // BUG: did not persist nor display updated total            These benchmarks therefore do not capture expectations
       // localStorage.setItem('cartTotal', tot); // missing
      }                                                             expressed through a newly generated application’s interface.
     }                                                              Recent vibe-coding benchmarks evaluate complete applica-
                                                                    tions using browser agents or LLM judgments [1, 31]. How-
   Although the app runs and the message suggests the               ever, recent position work argues that vibe coding needs
feature works, it violates the user’s expectation that ap-          more deterministic checking [19]; our formative study char-
plying the code changes the cart total, even on refresh. In         acterizes failures, while FlowCheck lets users state and de-
FlowCheck, users can specify that clicking the button should        terministically check the expected information flows.
cause the promo code to update the displayed and persisted             Automated test generation is another approach to check
total. The analysis identifies that the message is updated but      agent-generated code, but faces the oracle problem, where
the discounted value does not flow to either destination.           a test is dependent on knowing what the correct behavior
   Unlike LLM-as-judge approaches, FlowCheck returns the            should be [2]. Tools such as EvoSuite [8] are able to pro-
same result for identical code and constraints, without ex-         duce test sets and suggest assertions, but those assertions
ecuting the app. Here, our focus is on properties that can          are based on what the current code does, rather than what it
be statically analyzed, as they are lightweight and can be          should do. The same issue occurs with LLM-based test gener-
used within agent loops. We find that constraints are useful        ators like TestPilot [26] which generates JavaScript (JS) unit
targets for agents to generate to aid testing their code, and vi-   tests by prompting a model with the implementation of the
olations provide details of the failure and intended behavior,      function, so its oracles may reflect the existing code. If the
which guides debugging and avoids relying on vibe-coder             code contains silent failures, the generated oracle may not
guesses. Our paper makes the following contributions:               be able to detect it. In our approach, our constraints supply
1. We develop a taxonomy of silent behavioral failures from         the oracle from an outside user or agent, representing the
   a formative study spanning four applications, three coding       user’s intended behavior separate from implementation.
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                   LMPL ’26, October 4–9, 2026, Oakland, CA, USA


2.2   Specifications and LLM Debugging                                     3     Formative Study: Vibe Coding Failures
SpecGen, AutoSpec, Clover, and PATAgent use LLMs to gen-                   We conducted a formative study to characterize failures that
erate or formalize specifications and then apply verification              arise during iterative vibe coding. Across four applications
tools [16, 27, 35, 37]. Their specifications describe code us-             and three coding systems, we observed 23 distinct failures.
ing formal abstractions that non-programmers cannot easily                 Every application and system exhibited at least one failure.
inspect. Our language is intentionally less expressive: it de-
scribes user-visible actions, elements, and information flows,             3.1   Methodology
can be authored and displayed within the application inter-                We used a closed-weight model (Claude Opus 4.7), an open-
face, and is simple enough for an LLM to generate.                         weight model (DeepSeek V3), and a commercial vibe-coding
   LLM-based debugging and repair instead ask a model to                   system (Lovable). For each system, we generated four appli-
diagnose or correct the program. This has been done in var-                cations with four scripted stages: initial generation, feature
ious ways: by prompting it to explain and revise its own                   addition, refactoring, and feature modification. We fixed the
code [5], by using execution traces or semantic context [34],              prompts across systems, requested plain JavaScript without
or more recently by treating the LLM as an autonomous                      frameworks, saved the code after each stage, and manually
agent that plans and invokes tools [3]. However, self-repair               checked it against expectations written before generation.
gives inconsistent gains, and models are limited by their                     The applications were a workshop speaker scheduler; a
ability to provide actionable feedback on why code fails [23].             column-based task board refactored into a whiteboard with
Even where repair succeeds, it does not leave the user with                dependencies between tasks; a shopping application with
a persistent, independently checkable statement of the in-                 promo codes and limited-edition items; and an image gallery
tended behavior. Our constraints remain visible to the user,               with favorites, albums, navigation, and a public image API.
and their analysis is deterministic regardless of whether the
user or an LLM authored them.                                              3.2   Observed Failures
                                                                           We grouped the 23 failures into five recurring categories.
                                                                           Surface-level correctness. The visible output is discon-
2.3   End-User Web Testing and Programming                                 nected from the data or action it claims to represent. In the
                                                                           image galleries produced by Claude, DeepSeek, and Lovable,
Dynamic web-testing systems such as GUITAR, Crawljax,
                                                                           clicking a thumbnail opened a different image; data should
and Atusa execute interaction sequences and check resulting
                                                                           flow from the clicked thumbnail to the popup. In DeepSeek’s
interface states or DOM invariants [17, 18, 20]. Quickstrom
                                                                           shopping app, the VIP20 promo code failed when the cart
similarly checks user-facing behavior, but it uses a runtime
                                                                           contained limited-edition items; the displayed total ignored
approach, with specifications written in a temporal logic
                                                                           the promo input and cart contents.
aimed at web programmers [22]. Our constraints similarly
describe application-level behavior, but are checked stati-                Dropped constraints across iterations. A relationship es-
cally as information-flow relationships without executing                  tablished in one iteration, disappeared after a later modifica-
or crawling the application. This makes checks immediate                   tion. All three systems dropped the rule that a speaker could
and repeatable, but excludes runtime-only properties such                  occupy only one slot after a subsequent prompt allowed mul-
as external API results or dynamically generated code.                     tiple speakers per slot. Similarly, after task boards became
   End-user programming systems already make the pro-                      whiteboards, Claude, DeepSeek, and Lovable allowed a task
gram and state visible to the user. Users can debug by directly            to move directly from “not started” to “finished,” despite an
asserting e.g., spreadsheet values, select interface artifacts,            earlier rule forbidding that state update. In both cases, the
or ask questions about program behavior [4, 11, 25]. Trigger-              interface remained functional, but an earlier restriction on
action programming (TAP) further shows that if–then rules                  which actions could update state was lost.
can be accessible to non-programmers [36].                                 Missing implied functionality. The interface advertises an
   Recent work shows that natural language is difficult for                action without connecting it to its corresponding effect. The
users and programmers to state their intent [24]. Vibe coders              Claude and DeepSeek task boards displayed an archive area
struggle with reading and evaluating correctness of LLM-                   labeled “Move a card here to set aside,” but dropping a card
generated code [21]. Prior work frames this as an abstraction              did not update the archive; only a separate button worked.
gap between user intent and generated code, and bridges this               DeepSeek’s shopping app presented Tinder-style cards, but
by making the generated code legible or visualized so the user             swiping did not advance the displayed item and users had to
can form an accurate mental model [13]. We instead start                   fall back to buttons. These failures expose missing action-to-
with the visible interface, and define data- and control-flow              effect links, although gesture semantics such as dragging and
constraints from what users can directly express. Formally                 swiping may need runtime support beyond static analysis.
stating the intended behavior lets FlowCheck mechanically                  Breaking changes after modification. A new feature or
check and enforce them on behalf of the vibe coder.                        refactoring severed a relationship that previously worked.
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                         Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


After the task board was converted to a whiteboard, cards
from all three systems no longer displayed their status: the
underlying task state no longer flowed to the visible card. In
DeepSeek’s dependency editor, adding 𝐴 → 𝐵 and then 𝐴 →
𝐶 silently rewrote the graph as 𝐴 → 𝐶 → 𝐵, so the second
action overwrote rather than preserved the relationship.
Incomplete persistence. State was not saved, restored, or
associated with the correct data. In the image gallery, fa-
vorites were stored by position rather than image identity, so
reloading caused saved favorites to refer to different images
(Claude, DeepSeek, Lovable). In Lovable’s speaker scheduler,
neither the speaker list nor the schedule survived a reload,       Figure 1. FlowCheck Core Engine. The app source code
despite the prompt describing the generated people as “my          is preprocessed by CodeQL to support later static analysis
speaker list.” The first failure persisted the wrong source; the   queries. User- or LLM- authored constraints are compiled
second omitted the save-and-restore path entirely.                 into CodeQL primitives, and run to find violations. Finally,
                                                                   we output the constraints that passed or failed. 2
Failures in the Wild. Beyond our study, we observed the
same patterns in public vibe-coding transcripts1 : one agent          CodeQL is a static code analysis engine3 that compiles
generated search and history interfaces without creating the       source code into a relational database that models the ab-
required database tables, while another left a game perma-         stract syntax tree, control-flow graph, and data-flow graph.
nently displaying “loading” because an asynchronous result         We pre-process HTML separately in order to identify in-
never reached the interface.                                       terface elements (Section 6.1). Thus, constraints reduce to
                                                                   queries over the database and pre-processed HTML; each
3.2.1 Summary of Findings. We find that 11 of the 23
                                                                   query result is an instance of a match (e.g., a code path) that
failures share a common structure: missing or incorrect re-
                                                                   violates some expected behavior.
lationships between a user action and an observable effect.
These included whether a component is updated, whether
its value derives from the correct inputs, whether an update
                                                                   5     Constraint Language
is prohibited under a condition, and whether state persists        5.1    Design Principles
across reloads. Because these relationships span event han-        Drawing from related work in end user programming, we
dlers, control flow, DOM updates, and storage operations,          made three design decisions:
they are non-local and difficult to reason about from code         • Observability: The end-user’s mental model is the in-
fragments, yet visible to the user. This motivates an interface-     terface, and they reason about expectations in terms of
grounded constraint language that makes such information             visible UI states. For this reason, we restrict constraints to
flows explicit and mechanically checkable.                           observable elements, or key components we make visible
                                                                     to the user (API, storage).
4    System Overview                                               • Action to behavior framing: every constraint is condi-
Our system helps users verify and debug their vibe coded             tioned on a single user action, motivated by the trigger-
web applications. Instead of asking agents to debug, users           action structure. Users reason about intent in terms of
author constraints by clicking through the behavior they             cause and effect (TAP), where an action leads to (or does
expect, and FlowCheck verifies if the code aligns with that          not lead to) an expected effect [32].
behavior. As shown in Figure 4, users select interface ele-        • Static verifiability: We allow users to express only things
ments, actions, and storage state as nouns and specify the           we can check statically. Constraints that would require
flows between them. Thus, the user interacts with the app            running the app (such as confirming an actual value from
as normal, without needing to learn or inspect code.                 an API call, or detecting a race condition) are out of scope,
   The workflow has the following three steps: First, code is        as they require runtime tracing. Static analysis ensures it
preprocessed to add element identifiers (Section 6.1). Second,       is deterministic and does not vary across traces.
users author constraints through an interface running their
app, or an agent generates them (Sections 6.2 and 6.4). Third,     5.2    Abstractions
constraints compile into static analysis queries that run          We make the following abstractions to express constraints
against the code, and returns pass/fail results. (Section 5.5).    over the app’s behavior. These are designed to be easy for a
                                                                   user to understand, and also easy for an LLM to generate.
1 https://github.com/jennygzma/vibecoding-chatqa
2 Icons from https://www.flaticon.com.                             3 https://codeql.github.com/
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                   LMPL ’26, October 4–9, 2026, Oakland, CA, USA


Components: The components of these constraints are                        constraint = "P(" lex "|" lex ")" "=" NUM EOF
strictly things that can be read from or written to, such as
UI elements, database tables, and APIs.                                    lex = lex (OR | AND | XOR) lex | NOT lex | atom
                                                                           atom = write | action | call | persist | guard
Actions: User actions (e.g. clicking) and system actions (e.g
API call, page load).                                                      write = "w(" id ["," expr] ")" |
Reads and Writes: 𝑟 (), 𝑤 () over components. A write 𝑤 (𝑐)                         "w(" id "," "sources=" srcset ")"
means that there is a value written to component c; read 𝑟 (𝑐)             action = "A(" id ")" // user action
means that a value is read from component c.                               call = "call(" id ")"
                                                                           persist = "persist(" id ")"
Sources: The sources of data for a component. This allows
                                                                           guard = expr cmp expr | expr IN range
us to express a set of sources that a write must read from. For
example, 𝑤 (𝑐, 𝑟 (𝑎) + 1) requires c to be written with value              srcset = "{" [srcitem {"," srcitem}] "}"
𝑟 (𝑎) + 1, and 𝑤 (𝑐, 𝑠𝑜𝑢𝑟𝑐𝑒𝑠 = {𝑟 (𝑎), 𝑟 (𝑏)}) requires c to be            srcitem = "r(" id ")"
written with a value derived from exactly this set of reads.
   Each constraint is a logical statement about whether an                 expr = expr ("+" | "-" | "*" | "/") expr |
event occurs or not given a condition. The event either must                     "r(" id ")" | lit
always occur (𝑃 = 1) as in all paths from the action must
result in the expected event, while 𝑃 = 0 means this should
                                                                           Figure 2. Constraint syntax in extended Backus–Naur form,
never happen given the action. These map to our all paths
                                                                           a simplified subset of our grammar; see Appendix A.1 for
and no paths checks over the code.
                                                                           the full grammar.
5.3   Grammar
Our grammar focuses on parsing probabilistic constraints of                event call() represents an API invocation. A persist event
the form:                                                                  persist() represents state that survives across reloads. The
               𝑃 (𝑒𝑣𝑒𝑛𝑡 | 𝑎𝑐𝑡𝑖𝑜𝑛) = 𝑝𝑟𝑜𝑏𝑎𝑏𝑖𝑙𝑖𝑡𝑦.                           grammar permits actions and guards in any atom position,
The action is the user or system event that the constraint                 but our semantic analysis (Section 6.3) validates constraints
is conditioned on, while the event is our expected outcome                 and rejects those that put a user action or bare guard on the
(e.g. write to a component or API call). It supports nested                event side, or multiple actions on the condition side.
logic expressions (and/or/not/xor), user and system actions,
reads/writes to components, and expected probabilities.
                                                                           5.4   Expressiveness
Example 5.1. For example,                                                  We enumerated the kinds of user-visible constraints a user
           𝑃 (𝑤 (𝑐𝑎𝑟𝑡𝐶𝑜𝑢𝑛𝑡) | 𝐴(𝑎𝑑𝑑𝐶ℎ𝑎𝑟𝑔𝑒𝑟 )) = 1,                         might want to express about a web app, by drawing from
                                                                           our formative study (Section 3.2), common failure patterns
means: Every time the user takes action of clicking the add
                                                                           from prior work, and through experience building and in-
charger button, we expect that the cartCount component is
                                                                           teracting with these apps. We grouped them into three main
written to every single time (𝑃 = 1). This means that all exe-
                                                                           categories: UI, API, and database constraints, covering the
cution paths from the addCharger event handler must write to
                                                                           failures in our formative study (Section 3.2) as well as more
the cartCount component with a probability of 1.
                                                                           general web app expectations. We found that 29 of the 34
   While most of the grammar are standard logical and arith-               specific constraint cases can be checked with static methods:
metic expressions, the types of state and atomic operations                21 are fully checkable, and 8 are checkable partially by struc-
are worth mention. There are three types of state that serve               turally verifying control- and dataflow paths while deferring
as primitives that expressions are built on: UI elements that              exact value checking to runtime. Constraints that involve ex-
the user can see, storage entries for local or session storage,            act value checking or runtime timing require heavier-weight
and APIs for external services including external storage.                 dynamic analysis that we leave to future work.
The grammar uses the id to reference every identifier po-                     As discussed above, every constraint consists of an action,
sition. During semantic analysis, each id is classified as a               an event, and user elements. Actions can express any user
UI element, storage entry, or API from the mapping, which                  action or browser event over a visible HTML element. The
we use to ensure the constraint is valid. Each corresponds                 user simply selects an element, and specifies the action with
to one part of the authoring interface in Figure 4.                        an optional guard.
   There are four atomic operations over this state: A write                  Events are what occur in response to actions, and can
w() means a value is written to a component. It has optional               be any write, action, API call, storage interaction, or com-
constraints on the value or its sources. A user action A()                 position of these. Table 1 summarizes the main constraint
names an event the user takes (e.g button clicks). A system                patterns we encountered and express.
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                                      Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


                                        Table 1. Core expressiveness patterns of the constraint language.

        Pattern                Description                                                                   Example
        Basic state updates    Link a user action to a basic write event.                                    P(w(cartCount) | A(addBtn)) = 1
        Writes from source     Restricts a constraint to be written from a specific source.                  P(w(total, r(promoInput)) | A(applyPromoBtn)) = 1
        Compound events        Combines multiple expected events using logic operators.                      P(w(cartCount) AND w(cartItems) | A(addBtn)) = 1
        Persistence            Requires that a specific action results in saved state across page reloads.   P(persist(cartStorage) | A(addBtn)) = 1
        API call               Requires an action to trigger an API call.                                    P(call(productsAPI) | A(pageLoad)) = 1
        Disallowed events      Target event must not occur.                                                  P(w(cartCount) | A(applyPromoBtn)) = 0



5.5   From Constraints to CodeQL Queries                                                         A guard keeps the handler but records the guard, writ-
We compile each constraint into a set of the primitive queries                                ten ⟨handler (𝑎), 𝑔⟩; under this context a write must addi-
of Table 2, together with a rule for combining their pass/fail                                tionally sit inside a conditional that reads the guarded ele-
results. Figure 3 defines this compilation as five translation                                ment (guarded_write). A negated action instead changes
functions, read top-down: TJ·K translates the whole con-                                      the context to handler (𝑎), and writes are checked using
straint, CJ·K translates its condition side, EJ·Kℎ and RJ·Kℎ                                  no_other_handlers so that only 𝑎 can write the target.
translate its event side, and VJ·K translates the value expres-                                  The distinction between the two forms of negation appears
sions that appear inside events.                                                              directly in the rules. The constraint 𝑃 (𝑤 (𝑐) | 𝐴(𝑎)) = 0 asks
                                                                                              whether 𝑎’s own handler can reach the write and passes
                                                                                              when it cannot. By contrast, 𝑃 (𝑤 (𝑐) | NOT 𝐴(𝑎)) = 1 checks
            Table 2. The CodeQL primitive queries.
                                                                                              exclusivity, passing when no other handler reaches the write.
 Primitive             What it checks
 path_exists           ≥ 1 code path from the handler writes to target.
                                                                                              Events (EJ·Kℎ ) and values (VJ·K). EJ·Kℎ follows the struc-
 all_paths_write       Every exit path through the handler writes the target.                 ture of the event expression and covers the three checkable
 literal_value         The write assigns the literal value named in the constraint.
 source_set            Dataflow sources to the write same as expected set.
                                                                                              event atoms: writes, calls, and persists. User actions and
 self_increment        Written value derives from 𝑟 ( target ) + constant.                    guards instead belong to the condition side and are han-
 api_result_taint
 no_other_handlers
                       The written value taint-flows from a fetch/axios response.
                       Only the named action writes to target.
                                                                                              dled by CJ·K. A plain write w(𝑒) produces two primitives:
 call_reaches          The handler reaches an invocation of the named function.               path_exists, requiring the write to be reachable from ℎ, and
 call_with_source      r(source) flows to an argument of the call.
 page_load_restores    A page-load handler calls getItem(key) for the storage key.
                                                                                              all_paths_write, requiring the write to occur on every path
 guarded_write         The write is structurally inside an if reading the guarded             through the handler. A write includes either an assignment
                       element.
                                                                                              to the element (e.g., .textContent, .value) or a DOM mu-
                                                                                              tation on it. Additional details in the atom add primitives to
                                                                                              this base—for instance, a literal value adds literal_value, a
Constraints (TJ·K). The probability decides how the event                                     value expression adds source_set.
side is checked. A 𝑃=1 constraint requires the event on every                                    A call atom checks that the handler reaches the named
path, so its event is translated by EJ·Kℎ , whose primitives                                  API. When the atom names a source value, call_with_source
check all paths. A 𝑃=0 constraint forbids the event on any                                    checks both that the call is reachable and that the source
path, so its event is translated by RJ·Kℎ , which only asks                                   flows into it. A persist atom checks both parts of per-
whether the event is reachable at all; the constraint passes                                  sistence: the handler must save to the storage key using
when it is not. For persist, this means the action handler                                    path_exists, and a page-load handler must read the value
never writes the storage key.                                                                 back using page_load_restores. Compound events are trans-
                                                                                              lated one operand at a time, after which their pass/fail results
Conditions (CJ·K). The condition side is translated once                                      are combined using the Boolean operator in the constraint:
into the handler context ℎ from which every primitive query                                   AND as ∧, OR as ∨, XOR as ⊕, and NOT as ¬.
begins. In the common case, ℎ is simply handler (𝑎). The                                         Each primitive corresponds to one CodeQL query executed
function handler (·) is not part of the constraint language,                                  from entry point ℎ. The query returns a set of rows, with each
but an auxiliary function used by the translation: given the                                  row representing one match in the code, and the primitive
id 𝑎 of an interface element, it returns the event-handler                                    interprets those rows as pass/fail. For example, path_exists
function that the app registers on that element.                                              passes when the query finds at least one reachable write. By
   handler (𝑎) resolves the id to its code references, including                              contrast, all_paths_write searches for counterexample paths
calls such as getElementById("addBtn") and the variables                                      that exit without writing, and passes only when none exist.
to which they are assigned (e.g., isElementRef predicate in                                   Finally, VJ·K does not evaluate arithmetic. It only collects
the Appendix). We then identify the function attached to the                                  the components read by a value expression, so r(𝑎) + r(𝑏)
element’s events. Each query on the event side searches only                                  becomes the source set $a,b$. The checker verifies where a
code reachable from that function.                                                            value comes from, rather than what the expression computes.
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                               LMPL ’26, October 4–9, 2026, Oakland, CA, USA

Constraint Translation                                                                                                                              TJ·K
                                    TJP(𝐸 | 𝐶) = 1K = EJ𝐸KCJ𝐶 K                  TJP(𝐸 | 𝐶) = 0K = ¬ RJ𝐸KCJ𝐶 K
Condition Translation                                                                                                                               CJ·K
                        CJA(𝑎)K = handler (𝑎)        CJA(𝑎) AND 𝑔K = ⟨handler (𝑎), 𝑔⟩               CJNOT A(𝑎)K = handler (𝑎)
Event Translation                                                                                                                                  EJ·Kℎ
                                                       EJw(𝑒)Kℎ = path_exists(ℎ, 𝑒) ∧ all_paths_write(ℎ, 𝑒)
                                                  EJw(𝑒, 𝑘)Kℎ = EJw(𝑒)Kℎ ∧ literal_value(ℎ, 𝑒, 𝑘)
                                                  EJw(𝑒, 𝑣)Kℎ = EJw(𝑒)Kℎ ∧ source_set(ℎ, 𝑒, VJ𝑣K)
                                       EJw(𝑒, sources=𝑆)Kℎ = EJw(𝑒)Kℎ ∧ source_set(ℎ, 𝑒, VJ𝑆K)
                                         EJw(𝑒, r(𝑒) + 𝑘)Kℎ = EJw(𝑒, r(𝑒))Kℎ ∧ self_increment(ℎ, 𝑒, 𝑘)
                                  EJw(𝑒, r(api_result))Kℎ = EJw(𝑒)Kℎ ∧ api_result_taint(ℎ, 𝑒)
                                                  EJcall(𝑐)Kℎ = call_reaches(ℎ, 𝑐)
                                              EJcall(𝑐, 𝑣)Kℎ = call_with_source(ℎ, 𝑐, VJ𝑣K)
                                              EJpersist(𝑠)Kℎ = path_exists(ℎ, 𝑠) ∧ page_load_restores(𝑠)
                                EJ𝐸 1 AND 𝐸 2 Kℎ = EJ𝐸 1 Kℎ ∧ EJ𝐸 2 Kℎ              EJ𝐸 1 OR 𝐸 2 Kℎ = EJ𝐸 1 Kℎ ∨ EJ𝐸 2 Kℎ
                                EJ𝐸 1 XOR 𝐸 2 Kℎ = EJ𝐸 1 Kℎ ⊕ EJ𝐸 2 Kℎ                   EJNOT 𝐸Kℎ = ¬ EJ𝐸Kℎ
                    EJw(𝑒)K ⟨ℎ, 𝑔⟩ = EJw(𝑒)Kℎ ∧ guarded_write(ℎ, 𝑒, 𝑔)              EJw(𝑒)Khandler (𝑎) = no_other_handlers(𝑎, 𝑒)
Reachability Translation (for 𝑃 = 0)                                                                                                               RJ·Kℎ
                           RJw(𝑒, . . . )Kℎ = path_exists(ℎ, 𝑒)
                                                                                         RJ𝐸 1 𝑜𝑝 𝐸 2 Kℎ = RJ𝐸 1 Kℎ 𝑜c
                                                                                                                     𝑝 RJ𝐸 2 Kℎ
                           RJcall(𝑐, . . . )Kℎ = call_reaches(ℎ, 𝑐)
                                                                                           RJNOT 𝐸Kℎ = ¬ RJ𝐸Kℎ
                                RJpersist(𝑠)Kℎ = path_exists(ℎ, 𝑠)
Value Translation (expected sources)                                                                                                                VJ·K
             VJr(𝑥)K = {𝑥 }    VJ𝑘K = ∅             VJ𝑣 1 𝑜𝑝 𝑣 2 K = VJ𝑣 1 K ∪ VJ𝑣 2 K       VJ{𝑣 1 , . . . , 𝑣𝑛 }K = VJ𝑣 1 K ∪ · · · ∪ VJ𝑣𝑛 K

Figure 3. The translation semantics from constraints to CodeQL primitive queries. Primitives are the queries of Table 2,
run with handler context ℎ as their entry point; the auxiliary function handler (𝑎) resolves element id 𝑎 to the event-handler
function the app registers on it. Metavariables: 𝑎 ranges over action elements, 𝑒 over element ids, 𝑠 over storage keys, 𝑐
over APIs, 𝑘 over literals, 𝑣 over value expressions, 𝑆 over source sets, 𝑔 over guards, and 𝐸, 𝐶 over event and condition
expressions. When several E rules overlap, the most specific applies. In V, 𝑜𝑝 ∈ {+, -, *, /}; in R, 𝑜𝑝 ∈ {AND, OR, XOR} and 𝑜c
                                                                                                                              𝑝 is
the corresponding Boolean connective (∧, ∨, ⊕).

Example 5.2. Let ℎ = handler (applyPromoBtn). The promo-                        variables. A non-developer, or vibe-coder, would not know
code constraint from the introduction compiles by the rules                     these, and learning this would take as long as debugging
of Figure 3 as:                                                                 manually. By restricting constraints to user-visible behavior,
 TJP(w(total, r(promoInput))| A(applyPromoBtn)) = 1K                            users express their expectations easily over their own app.
      = EJw(total, r(promoInput))Kℎ
                                                                                6        Implementation
      = path_exists(ℎ, total)
                                                                                To go from the app to verified constraints, we follow three
        ∧ all_paths_write(ℎ, total)
                                                                                steps: (1) preprocess the code to add identifiers (Section 6.1),
        ∧ source_set(ℎ, total, {promoInput})
                                                                                (2) run the app for authoring constraints (Section 6.2), and
 In the broken app, the handler writes only the success mes-                    (3) parse, validate, and verify the constraint (Section 6.3).
sage, so all_paths_write returns counterexample paths that
never write total, and the constraint fails.                                    6.1       Preprocessing
                                                                                Vibe-coded apps often lack identifiers for elements [12]. This
5.6    Why We Chose This Design                                                 creates two issues: (1) when authoring a constraint, we have
Other formalisms like Hoare logic or Linear Temporal Logic                      no id to uniquely reference each element; (2) the id links
can be more expressive, but are less accessible to non-developers.              the HTML and JS, which both reference the same DOM
Writing our promo example in Hoare logic as {𝑃 } applyPromo()                   elements. To address this, we automatically map elements
{𝑄 }, requires the user to write out the DOM state before and                   across both languages by scanning the source code to locate
after, as well as read the code for internal function names and                 all UI elements (e.g. buttons and inputs), and adding unique
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                      Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


identifiers (cv_nnnn) where they are missing. This ensures
every element has a static reference across both languages.
We use BeautifulSoup to parse each HTML file and traverse
the elements the user could select. For JS, we use regular
expressions to identify programmatically created elements
(such as createElement()), and append missing IDs.

6.2   User Interface
Users provide FlowCheck with their web app’s path, which
opens in a new tab. Users express constraints on this app via
our overlay template: “When I take [action], these update:
[component]” with optional AND, OR, XOR, NOT logic.
   Users select visible UI components by clicking directly on
them, the same way they interact with their app. They can
also pick from a detected list of APIs and storage. As a result,
the user does not need to learn the language syntax, identify
internal variables for elements, or write constraints by hand.
FlowCheck records the user’s actions, converts them to our         Figure 5. Reviewing authored constraints. The Review panel
constraint language, and sends them to the parser.                 lists the constraints the user has built, and dashed lines trace
                                                                   each constraint’s flows from action to event.


                                                                      the condition side must contain an action 𝐴(𝑒𝑖 ), the event
                                                                      side must contain a valid effect (𝑤 (), 𝑐𝑎𝑙𝑙 (), 𝑝𝑒𝑟𝑠𝑖𝑠𝑡 ()),
                                                                      the probability must be 0 or 1, and identifiers in action
                                                                      must map to the “action” type. If rule fails, the constraint
                                                                      is invalid and exits with a detailed message to the user.
                                                                   3. Classification: From this AST, we determine which prim-
                                                                      itive queries to run based on the event type and condition
                                                                      (Section 5.5). For example, an event containing an API
                                                                      node resolves to an API call check, while a write carrying
                                                                      a value expression resolves to a dataflow check.
                                                                   4. Verification: Once we know which primitives to run,
                                                                      FlowCheck executes each corresponding CodeQL query–
                                                                      written in a .ql file with placeholder tokens replaced by
                                                                      element identifiers–against the database (Section 4). It
                                                                      reviews the returned rows to return a Pass/Fail result, and
                                                                      reports which queries failed for the user to review.
Figure 4. User authoring a constraint via the overlay. The
user selects the promo input as the action and discount as a
write target, then adds a second target (cart total, highlighted   6.4   Authoring Constraints
in green), to form a compound constraint. Users select visible
components, without having to learn code or syntax.                Constraints can be generated in 2 ways:
                                                                   1. User: The user can author constraints through our overlay
                                                                      UI, which lets a user click on elements in their running
6.3   Analysis                                                        app and pick from constraint templates. For this, they do
Once the user selects their components through the UI, their          not need to know the constraint syntax or understand the
selections are translated into our constraint language, and           code, only simple logic expressions (AND/OR/XOR/NOT).
compiled to static CodeQL queries in 4 steps:                      2. LLM or Agent: We describe the language as a skill for an
1. Parsing: Constraints are parsed using an ANTLR4-generated          agent or LLM, containing the grammar, constraint types,
   parser into an AST, using our grammar from Section 5.              and examples. Given the code, the app description, and
2. Semantic analysis: We walk the AST to extract the key              this context, a model can produce a comprehensive list
   parts (the event, condition, probability, and identifiers)         of constraints, which can combine with the user’s set for
   and verify semantic rules: every referenced identifier must        broader coverage. In Section 7.2.3 we find that models can
   match a valid DOM element, storage identifier, or API,             author valid constraints and use them to catch more bugs.
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                         LMPL ’26, October 4–9, 2026, Oakland, CA, USA


7     Evaluation                                                                                       Amazon                     Twitter           Airbnb        Slack
In our evaluation, we focused on two questions: (1) does
FlowCheck catch the constraint violations it is designed to
                                                                                         P1       5                   6                    7              6       24
catch, and (2) how does it compare to asking a frontier LLM
                                                                                  Claude P2       4               6                    7                  7       24
to find the same bugs?
                                                                                         P3       4               7                        7                  8        26

7.1   Experiment Setup
                                                                                         P1 3             4               5                5        17
7.1.1 Test Applications. Test applications were gener-                          DeepSeek P2 3                 6                   6            15
ated using Claude Code. We built four web apps, each mod-                                P3 1         6                   5                    7         19
eled after an existing app (Amazon, Twitter, Airbnb, Slack).
We chose well-known apps because they are real-world use                                P1 2 3   4                            3       12
cases, and models understand the expected features and be-                       Gemini P2 2 2 4                          4           12
havior due to extensive training data. We used JS with no                               P3 3 2   4                                5        14
frameworks to stay within scope of static analysis, ensured
all elements had IDs, and used local storage. We iterated on                                  0           5               10      15     20                       25        30
each app, adding features to create opportunities to write                                                                 Failures caught
constraints. For example, a local database of items for Ama-
zon, or a fees calculator for Airbnb.                                      Figure 6. Bug catch rate of FlowCheck compared to the
                                                                           LLM baselines (Claude, DeepSeek, Gemini) across the three
7.1.2 Ground Truth and Injected Violations. We estab-                      prompt variants. FlowCheck flags all injected violations,
lished 14–21 constraints per app representing the expected                 while the best model–prompt pair reaches 26/30.
behavior (e.g. applying a promo code updates the total). We
copied each app to modified/ variant and guided an agent                   7.2    Results
to introduce 7–8 subtle violations, breaking about half the                FlowCheck catches all constraint violations, while LLMs
constraints, to simulate real-world development mistakes.                  were slower and less accurate, with the best model-prompt
These were inspired by documented coding-agent failure                     pair (Claude P3) reaching 26/30 and most results far lower
patterns [6], taxonomies of LLM-generated bugs [28], our                   (Figure 6). The results suggest that models are better at spot-
formative study (Section 3.2), and by manually breaking or                 ting localized bugs, a wrong literal or a missing write inside
disconnecting components. Bugs covered several types, in-                  one handler, but struggle once bugs span multiple branches
cluding missing branch write (if x then { write } with no else),           or handlers. Providing more detail in the prompt does not
switch missing a default case, write-with-wrong-source, and                necessarily help; the models may read more of the code but
disconnected components. For example, in the modified                      not always find more of the bugs.
Twitter app, post-tweet-btn writes the posted-banner even
for empty inputs, dropping the character count check. The                  7.2.1 What Models Catch. Models reliably caught bugs
apps ranged from roughly 300 to 900 lines of code (HTML and                localized to a small code block, whose patterns are relatively
JS), each with 16–26 action elements, 17–23 event handlers,                easy to recognize. For example, assigning an incorrect literal,
and 5–11 localStorage operations. This added 30 behavioral                 or failing to update the UI on one conditional branch. Models
violations across the four applications. We evaluated whether              also caught writes from the wrong data source (e.g. apply-
FlowCheck could correctly flag these constraint violations,                promo saving the old value instead of the user’s input) and
and compared it against the LLM baselines.                                 partial persistence (e.g. storing favorites but not loading them
                                                                           on refresh). This was common in the Airbnb app, whose bugs
7.1.3 Methods. We compared FlowCheck against asking a                      largely involve localized writes that were missing or wrote
frontier LLM to find bugs in the same broken code. We tested               the wrong key. Identifying these bugs does not require any
three models: Claude Opus 4.7, DeepSeek V3, and Gemini                     control flow analysis or handler interaction.
Pro, using three prompt variants, increasing in detail (using
a single run per model-prompt cell).                                       7.2.2 What Models Miss. We found two dominant classes
Prompt 1: “Here is a web app, similar to [well known app].                 of violations that LLMs did not reliably identify. The first
Are there any bugs?”                                                       are universal quantifier constraints, where a property must
Prompt 2: Lists the features the user requested, e.g. “the                 hold over all paths, such as P=1 writes. Verifying these re-
user requested an Amazon like app with these features: a                   quires checking all branches, but models sometimes miss the
product grid, a cart drawer. . . ”                                         branch where the write is dropped. For example, an Airbnb
Prompt 3: Same feature list as Prompt 2 plus an explicit                   booking handler that updates the total cost only when guests
edge-case checklist: boundary values, all user states, all branches,       ≤ 4, but leaves the other branch silently broken. The second
cross-handler consistency.                                                 are cross-handler flows, where one handler’s correctness
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                           Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


depends on state written by another. These are difficult to            value is never parsed further. As a workaround, users can
detect because the bug is not visible in either handler alone,         write constraints at the static container level. Frameworks
only when they interact. For example, Amazon’s checkout                like React and Vue have the same issue since they build
reads cartSummary but applyPromo clears it to 0. Since the             UIs at runtime from a virtual DOM. This usually leaves the
handlers never reference each other, models reason on them             static HTML empty and FlowCheck cannot fully check them.
separately and don’t trace the data flow between them.                 Drag-and-drop is similar: implementations vary across the
   We found that adding detail to the prompt does not al-              HTML5 drag API, touch events, and mouse movement, with
ways help; all three prompt versions did not reliably catch            no single code pattern, making it difficult to detect statically.
errors across models. With more detail, models read code
more thoroughly, but grew more willing to trust it, justifying         8.2   Future Work
bugs instead. For example, Amazon’s laptop favorite handler
                                                                   Runtime Analysis: Our language supports probability val-
silently skips its write for one user tier, but a model dismissed
                                                                   ues within [0, 1], but our implementation focuses on P=1 and
this as intentional: "USER_TIER is a const initialized to ’free’,  P=0. Handling exact values and timing bugs (e.g., race con-
so the enterprise branch is dead code, not a defect."              ditions, API status codes) requires runtime data. We plan to
7.2.3 Agents and our Constraint Language. We used                  address this using a browser agent to collect runtime traces,
the Amazon app as a probe to understand whether LLMs               verify constraints, and record the interactions that led to the
can benefit from FlowCheck. We studied two questions: (Q1)         error to help debugging.
can agents author constraints? (Q2) does providing our lan-           Runtime tracing introduces variance because results de-
guage and asking the model to write constraints help find          pend   on browser agent paths, raising open questions about
more bugs? To do so, we performed three runs; in each, we          action   selection and modeling users, which is why we fo-
prompted each model with the grammar, a description of the         cused   on  static analysis first. A promising direction is a hy-
operators, example constraints, a description of the Ama-          brid  approach:   using static analysis for structural checks, and
zon app, and the Amazon code, and asked it to generate a           using  runtime   tracing only for value or timing related checks.
comprehensive set of constraints to find bugs. We consider         For   example,    the constraint   𝑃 (𝑤 (𝑒 𝑗 , len(𝑟 (api_result))) |
a constraint valid if it parses and passes our semantic rules.     call(api))   = 1  expresses  that  a component ej must display
                                                                   the length of an API result. The static checker confirms the
Q1. Per run, Claude, DeepSeek, and Gemini each gener-              value written to ej derives from the API response length, and
ated 30-60, 50-86, and 15-20 constraints. Of these, 45-100%        runtime traces verify the resulting length matches.
were valid for Gemini, 34-44% for Claude, and 41-65% for              User Evaluation: While our evaluation demonstrates
DeepSeek. Although they nearly all made sense conceptually,        that FlowCheck can accurately detect injected failures, we
their errors were finer: hallucinated names (e.g. dbPut_favorites),plan to conduct a user study with vibe-coders to evaluate
syntax errors (underscore instead of dash), or the wrong atom      language usability, how users interpret analysis results, and
for an event (call(x) instead of A(x)). Since they expressed       how they integrate them into their coding workflow.
reasonable expectations and failed on syntax or identifiers,          Iterative Vibe Coding: FlowCheck evaluates constraints
this could likely be improved via more prompt engineering.         on single code versions, but vibe coding is an iterative pro-
Q2. The constraints helped models catch more of the silent         cess where constraints change as apps grow. A key next step
failures: compared to using their best prompt, Claude in-          is tracking and evolving constraints alongside code versions,
creased from 5 → 6, DeepSeek from 3 → 5, and Gemini                allowing coding agents to continuously generate, check, and
from 3 → 4 out of 7 gold bugs. DeepSeek likely improved            refine constraints and code throughout development.
the most because it generated the most constraints. Among
the bugs the models identified, Claude and Gemini produced         9 Conclusion
no false positives, while DeepSeek produced 2-3 per run.
Claude and DeepSeek also identified other bugs out of scope        We introduced a constraint language enabling users to ex-
of FlowCheck. While this is not conclusive evidence, it is a       press expected web-app behavior simply by pointing at the
promising signal that providing a compact constraint lan-          app itself. We also introduced FlowCheck, a tool that verifies
guage can help improve bug catch rates.                            these constraints against their code through static analysis.
                                                                   We do so by parsing the constraint, classifying the type, and
                                                                   mapping to a set of CodeQL queries that we then execute.
8 Limitations and Future Work
                                                                   In our evaluation, FlowCheck caught all 30/30 injected vi-
8.1 Limitations                                                    olations, compared to at most 26/30 for the strongest LLM
CodeQL is a static analyzer that reads the code without run-       baseline and fewer for the rest. Combined with the authoring
ning, so it cannot link JS to DOM elements created at runtime.     interface, this lets users of any programming background
For example, elements built through strings (container.            express and verify expectations deterministically, without
innerHTML="...") hide the ids inside the string, since the         needing to read or understand the code.
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                            LMPL ’26, October 4–9, 2026, Oakland, CA, USA


References                                                                           https://www.usenix.org/conference/nsdi20/presentation/lou
 [1] Srijan Bansal, Jiao Fangkai, Yilun Zhou, Austin Xu, Shafiq Joty, and       [15] Chang Lou, Yuzhuo Jing, and Peng Huang. 2022. Demystifying and
     Semih Yavuz. 2026. VIBEPASS: Can Vibe Coders Really Pass the Vibe               Checking Silent Semantic Violations in Large Distributed Systems. In
     Check? arXiv:2603.15921 [cs.SE] https://arxiv.org/abs/2603.15921                16th USENIX Symposium on Operating Systems Design and Implemen-
 [2] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and                   tation (OSDI 22). USENIX Association, Carlsbad, CA, 91–107. https:
     Shin Yoo. 2015. The Oracle Problem in Software Testing: A Survey.               //www.usenix.org/conference/osdi22/presentation/lou-demystifying
     IEEE Transactions on Software Engineering 41, 5 (2015), 507–525. doi:10.   [16] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen:
     1109/TSE.2014.2372785                                                           Automated Generation of Formal Program Specifications via Large
 [3] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2025. Re-                Language Models. arXiv:2401.08807 [cs.SE] https://arxiv.org/abs/2401.
     pairAgent: An Autonomous, LLM-Based Agent for Program Repair.                   08807
     In Proceedings of the IEEE/ACM 47th International Conference on Soft-      [17] Ali Mesbah, Arie van Deursen, and Stefan Lenselink. 2012. Crawling
     ware Engineering (Ottawa, Ontario, Canada) (ICSE ’25). IEEE Press,              Ajax-Based Web Applications through Dynamic Analysis of User In-
     2188–2200. doi:10.1109/ICSE55347.2025.00157                                     terface State Changes. ACM Trans. Web 6, 1, Article 3 (March 2012),
 [4] M. Burnett, C. Cook, O. Pendse, G. Rothermel, J. Summet, and C.                 30 pages. doi:10.1145/2109205.2109208
     Wallace. 2003. End-user software engineering with assertions in the        [18] Ali Mesbah, Arie van Deursen, and Danny Roest. 2012. Invariant-Based
     spreadsheet paradigm. In 25th International Conference on Software              Automatic Testing of Modern Web Applications. IEEE Transactions on
     Engineering, 2003. Proceedings. 93–103. doi:10.1109/ICSE.2003.1201191           Software Engineering 38, 1 (2012), 35–53. doi:10.1109/TSE.2011.28
 [5] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny                     [19] Jacqueline Mitchell and Yasser Shaaban. 2025. Position: Vibe Coding
     Zhou. 2023. Teaching Large Language Models to Self-Debug.                       Needs Vibe Reasoning: Improving Vibe Coding with Formal Verifica-
     arXiv:2304.05128 [cs.CL] https://arxiv.org/abs/2304.05128                       tion. In Proceedings of the 1st ACM SIGPLAN International Workshop on
 [6] DAPLab, Columbia University. 2026. 9 Critical Failure Patterns of               Language Models and Programming Languages (Singapore, Singapore)
     Coding Agents. https://daplab.cs.columbia.edu/general/2026/01/08/9-             (LMPL ’25). Association for Computing Machinery, New York, NY,
     critical-failure-patterns-of-coding-agents.html. Data, Agents, and              USA, 84–90. doi:10.1145/3759425.3763390
     Processes Lab, Columbia University.                                        [20] Bao N. Nguyen, Bryan Robbins, Ishan Banerjee, and Atif Memon.
 [7] Francesco Dente, Dario Satriani, and Paolo Papotti. 2026. Constraint            2014. GUITAR: an innovative tool for automated testing of GUI-
     Decay: The Fragility of LLM Agents in Backend Code Generation.                  driven software. Automated Software Engg. 21, 1 (March 2014), 65–105.
     arXiv:2605.06445 [cs.SE] https://arxiv.org/abs/2605.06445                       doi:10.1007/s10515-013-0128-9
 [8] Gordon Fraser and Andrea Arcuri. 2011. EvoSuite: automatic test            [21] Sydney Nguyen, Hannah McLean Babe, Yangtian Zi, Arjun Guha,
     suite generation for object-oriented software. In Proceedings of the            Carolyn Jane Anderson, and Molly Q Feldman. 2024. How Beginning
     19th ACM SIGSOFT Symposium and the 13th European Conference on                  Programmers and Code LLMs (Mis)read Each Other. In Proceedings
     Foundations of Software Engineering (Szeged, Hungary) (ESEC/FSE ’11).           of the 2024 CHI Conference on Human Factors in Computing Systems
     Association for Computing Machinery, New York, NY, USA, 416–419.                (Honolulu, HI, USA) (CHI ’24). Association for Computing Machinery,
     doi:10.1145/2025113.2025179                                                     New York, NY, USA, Article 651, 26 pages. doi:10.1145/3613904.3642706
 [9] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun            [22] Liam O’Connor and Oskar Wickström. 2022. Quickstrom: property-
     Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion                    based acceptance testing with LTL specifications. In Proceedings of
     Stoica. 2024. LiveCodeBench: Holistic and Contamination Free Evalu-             the 43rd ACM SIGPLAN International Conference on Programming Lan-
     ation of Large Language Models for Code. arXiv:2403.07974 [cs.SE]               guage Design and Implementation (San Diego, CA, USA) (PLDI 2022).
     https://arxiv.org/abs/2403.07974                                                Association for Computing Machinery, New York, NY, USA, 1025–1038.
[10] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei,          doi:10.1145/3519939.3523728
     Ofir Press, and Karthik Narasimhan. 2024. SWE-bench: Can Language          [23] Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng
     Models Resolve Real-World GitHub Issues? arXiv:2310.06770 [cs.CL]               Gao, and Armando Solar-Lezama. 2024. Is Self-Repair a Silver Bullet
     https://arxiv.org/abs/2310.06770                                                for Code Generation? arXiv:2306.09896 [cs.CL] https://arxiv.org/abs/
[11] Amy J. Ko and Brad A. Myers. 2004. Designing the whyline: a de-                 2306.09896
     bugging interface for asking questions about program behavior. In          [24] Madison Pickering, Helena Williams, Alison Gan, Weijia He, Hyojae
     Proceedings of the SIGCHI Conference on Human Factors in Comput-                Park, Francisco Piedrahita Velez, Michael L. Littman, and Blase Ur.
     ing Systems (Vienna, Austria) (CHI ’04). Association for Computing              2025. How Humans Communicate Programming Tasks in Natural
     Machinery, New York, NY, USA, 151–158. doi:10.1145/985692.985712                Language and Implications For End-User Programming with LLMs. In
[12] Maurizio Leotta, Andrea Stocco, Filippo Ricca, and Paolo Tonella. 2016.         Proceedings of the 2025 CHI Conference on Human Factors in Computing
     Robula+: an algorithm for generating robust XPath locators for web              Systems (CHI ’25). Association for Computing Machinery, New York,
     testing. Journal of Software: Evolution and Process 28, 3 (2016), 177–          NY, USA, Article 875, 34 pages. doi:10.1145/3706598.3713271
     204. arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1002/smr.1771        [25] Gregg Rothermel, Lixin Li, Christopher DuPuis, and Margaret Burnett.
     doi:10.1002/smr.1771                                                            1998. What you see is what you test: a methodology for testing
[13] Michael Xieyang Liu, Advait Sarkar, Carina Negreanu, Benjamin Zorn,             form-based visual programs. In Proceedings of the 20th International
     Jack Williams, Neil Toronto, and Andrew D. Gordon. 2023. “What                  Conference on Software Engineering (Kyoto, Japan) (ICSE ’98). IEEE
     It Wants Me To Say”: Bridging the Abstraction Gap Between End-                  Computer Society, USA, 198–207.
     User Programmers and Code-Generating Large Language Models. In             [26] Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip. 2023. An
     Proceedings of the 2023 CHI Conference on Human Factors in Computing            Empirical Evaluation of Using Large Language Models for Automated
     Systems (Hamburg, Germany) (CHI ’23). Association for Computing                 Unit Test Generation. arXiv:2302.06527 [cs.SE] https://arxiv.org/abs/
     Machinery, New York, NY, USA, Article 598, 31 pages. doi:10.1145/               2302.06527
     3544548.3580817                                                            [27] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024. Clover:
[14] Chang Lou, Peng Huang, and Scott Smith. 2020. Understanding, De-                Closed-Loop Verifiable Code Generation. arXiv:2310.17807 [cs.AI]
     tecting and Localizing Partial Failures in Large System Software. In            https://arxiv.org/abs/2310.17807
     17th USENIX Symposium on Networked Systems Design and Imple-               [28] Florian Tambon, Arghavan Moradi-Dakhel, Amin Nikanjam, Foutse
     mentation (NSDI 20). USENIX Association, Santa Clara, CA, 559–574.              Khomh, Michel C. Desmarais, and Giuliano Antoniol. 2025. Bugs in
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                                   Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


     large language models generated code: an empirical study. Empirical
     Softw. Engg. 30, 3 (Feb. 2025), 48 pages. doi:10.1007/s10664-025-10614-4   //      entry point
[29] Ningzhi Tang, Chaoran Chen, Gelei Xu, Yiyu Shi, Yu Huang, Collin
     McMillan, Tao Dong, and Toby Jia-Jun Li. 2026. How Coding Agents           constraint
     Fail Their Users: A Large-Scale Analysis of Developer-Agent Mis-               : prob_constraint EOF
     alignment in 20,574 Real-World Sessions. arXiv:2605.29442 [cs.SE]
                                                                                    ;
     https://arxiv.org/abs/2605.29442
[30] Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan,
     Yesai Wu, Haotian Hui, Weichuan Liu, Zhiyuan Liu, and Maosong              prob_constraint
     Sun. 2024. DebugBench: Evaluating Debugging Capability of Large               : 'P(' logic_expr '|' logic_expr ')' probability_expr
     Language Models. arXiv:2401.04621 [cs.SE] https://arxiv.org/abs/2401.           ;
     04621
[31] Hung Tran, Langston Nashold, Rayan Krishnan, Antoine Bigeard, and          probability_expr
     Alex Gu. 2026. Vibe Code Bench: Evaluating AI Models on End-to-End             : '=' NUMBER
     Web Application Development. In Proceedings of the ACM Conference              ;
     on AI and Agentic Systems (CAIS ’26). Association for Computing
     Machinery, New York, NY, USA, 514–536. doi:10.1145/3786335.3813180
                                                                                //      boolean logic
[32] Blase Ur, Elyse McManus, Melwyn Pak Yong Ho, and Michael L.
     Littman. 2014. Practical trigger-action programming in the smart
     home. In Proceedings of the SIGCHI Conference on Human Factors             logic_expr
     in Computing Systems (Toronto, Ontario, Canada) (CHI ’14). Asso-               : logic_expr OR logic_xor
     ciation for Computing Machinery, New York, NY, USA, 803–812.                   | logic_xor
     doi:10.1145/2556288.2557420                                                    ;
[33] Mark Vero, Niels Mündler, Victor Chibotaru, Veselin Raychev, Max-
     imilian Baader, Nikola Jovanović, Jingxuan He, and Martin Vechev.          logic_xor
     2025. BaxBench: Can LLMs Generate Correct and Secure Backends?                 : logic_xor XOR logic_term
     arXiv:2502.11844 [cs.CR] https://arxiv.org/abs/2502.11844                      | logic_term
[34] Jian Wang, Xiaofei Xie, Qiang Hu, Shangqing Liu, and Yi Li. 2025.
                                                                                    ;
     Do Code Semantics Help? A Comprehensive Study on Execu-
     tion Trace-Based Information for Code Large Language Models.
     arXiv:2509.11686 [cs.SE] https://arxiv.org/abs/2509.11686                  logic_term
[35] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda                 : logic_term AND logic_factor
     He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting               | logic_factor
     Program Specification Synthesis by Large Language Models using                 ;
     Static Analysis and Program Verification. arXiv:2404.00762 [cs.SE]
     https://arxiv.org/abs/2404.00762                                           logic_factor
[36] Valerie Zhao, Lefan Zhang, Bo Wang, Michael L. Littman, Shan Lu,               : NOT logic_factor
     and Blase Ur. 2021. Understanding Trigger-Action Programs Through              | '(' logic_expr ')'
     Novel Visualizations of Program Differences. In Proceedings of the 2021
                                                                                    | atom
     CHI Conference on Human Factors in Computing Systems (Yokohama,
     Japan) (CHI ’21). Association for Computing Machinery, New York,               ;
     NY, USA, Article 312, 17 pages. doi:10.1145/3411764.3445567
[37] Xinyue Zuo, Yifan Zhang, Hongshu Wang, Yufan Cai, Zhe Hou, Jing            //      atoms
     Sun, and Jin Song Dong. 2025. PAT-Agent: Autoformalization for Model
     Checking. arXiv:2509.23675 [cs.SE] https://arxiv.org/abs/2509.23675        atom
                                                                                       : write_event
                                                                                       | user_action
Acknowledgments                                                                        | system_event
We thank Zhou Yu for her guidance and Haonan Wang for                                  | persist_event
helpful discussions. This research received funding from                               | guard
NSF 2103794, 2312991, 2551201 as well as DAPLab corpo-                                 | literal_bool
rate support in the form of funding and/or compute from                                ;
Amazon, IntellectAI, Infosys, Tidalwave, Veris, shopify, Mi-
                                                                                // Three w() forms:
crosoft, Thinking Machines, Dandy, Perplexity, and Daytona.                     // w(t)                — existence only
The views and conclusions presented here are those of the                       // w(t, expr)          — value from expr
authors and should not be interpreted as representing the                       // w(t, sources={. . . }) — value from exact set
official positions of the funding organizations.                                write_event
                                                                                    : 'w(' identifier ')'
A     Appendix                                                                      | 'w(' identifier ',' expr ')'
                                                                                    | 'w(' identifier ','
A.1    Constraint.g4 File                                                               'sources=' source_set ')'
grammar Constraint;
FlowCheck: Helping End-Users Specify and Verify Intent in Vibe-Coded Web Apps                     LMPL ’26, October 4–9, 2026, Oakland, CA, USA


       ;
                                                                           identifier : IDENTIFIER ;
source_set                                                                 comparator : '=' | '!=' | '<' | '>' | '<=' | '>=' ;
    : '{' source_item (',' source_item)* '}'                               range      : '[' NUMBER ',' NUMBER ']' | 'D' ;
    | '{' '}'                                                              literal    : NUMBER | STRING | 'null' ;
    ;                                                                      literal_bool : TRUE | FALSE ;

source_item                                                                //     lexer rules
    : 'r(' identifier ')'
    | 'r(' 'api_result' ')'                                                NOT : '¬' | '!' | 'NOT' ;
    ;                                                                      AND : '∧' | '&&' | 'AND' ;
                                                                           OR    : '∨' | '||' | 'OR' ;
user_action                                                                XOR : 'XOR' ;
    : 'A(' identifier ')'                                                  IN    : 'in' ;
    ;                                                                      TRUE : 'true' ;
                                                                           FALSE : 'false' ;
system_event
    : 'call(' identifier ')'                                               // IDENTIFIER also accepts a leading '.' so class
    | 'call(' identifier ',' expr ')'                                      // selectors like `.wishlist-heart` parse as a
    ;                                                                      // single token. Downstream layers
                                                                           // (semantic check, dispatcher) treat the
persist_event                                                              // leading-dot form as a CSS class selector to
    : 'persist(' identifier ')'                                            // bind against dynamic per-instance elements.
    ;                                                                      IDENTIFIER : '.'? [a-zA-Z][a-zA-Z0-9_-]* ;
                                                                           NUMBER     : [0-9]+ ('.' [0-9]+)? ;
//         expressions                                                     STRING     : '"' (~["\r\n])* '"' ;

guard                                                                      WS : [ \t\r\n]+ -> skip ;
    : expr comparator expr
    | expr IN range                                                        A.2    Parts of CodeQL Primitives
    ;                                                                      Full CodeQL queries are on Github at: https://github.com/
                                                                           reyavir/flowcheck
expr                                                                         isElementRef: This predicate is used to identify elements
       : expr ('+' | '-') term                                             with the specified id, that are initialized in code using docu-
       | term                                                              ment.getElementById(id) or are referenced future uses.
       ;                                                                   predicate isElementRef(string id, Expr ref) {
                                                                             // Direct: `document.getElementById(id)`
                                                                             exists(MethodCallExpr mc | mc = ref |
term                                                                            mc.getMethodName() = "getElementById" and
       : term ('*' | '/') factor                                                mc.getArgument(0).getStringValue() = id
       | factor                                                              )
                                                                             or
       ;                                                                     // Cached: `const x = document.getElementById(id);
                                                                             exists(VariableDeclarator decl, MethodCallExpr getEl, Variable v |
factor                                                                          getEl = decl.getInit() and
                                                                                getEl.getMethodName() = "getElementById" and
    : '(' expr ')'                                                              getEl.getArgument(0).getStringValue() = id and
    | atom_expr                                                                 v = decl.getBindingPattern().(VarRef).getVariable() and
                                                                                ref.(VarRef).getVariable() = v
    ;                                                                        )
                                                                           }
atom_expr
                                                                              Writes A write to the element is any property assignment
    : 'r(' identifier ')'
                                                                           on it, or a call to one of a small set of DOM-mutation methods,
    | 'r(' 'api_result' ')'
    | 'len(' 'r(' identifier ')' ')'                                       classList methods, or style methods.
                                                                           predicate writesElement(string id, AssignExpr write) {
    | 'len(' 'r(' 'api_result' ')' ')'                                       exists(PropAccess lhs |
    | 'status(' identifier ')'                                                 lhs = write.getLhs() and isElementRef(id, lhs.getBase())
    | 'f(' expr ')'                                                          )
                                                                           }
    | literal
    ;                                                                      predicate writesElementVia(string id, MethodCallExpr call) {
                                                                             call.getMethodName() = [
                                                                               "appendChild", "append", "prepend", "insertBefore",
//         terminals                                                           "replaceChild", "replaceChildren", "insertAdjacentElement",
                                                                               "removeChild", "remove", "setAttribute"
LMPL ’26, October 4–9, 2026, Oakland, CA, USA                                           Reya Vir, Lydia Chilton, Zhuo Zhang, and Eugene Wu


    ] and isElementRef(id, call.getReceiver())                         A.3   LLM Rationalizations of Injected Bugs
    or
    // element.classList.{add,remove,toggle,replace}(...)              With the most detailed prompt (P3), models often located
    exists(PropAccess classList |                                      an injected bug, but then dismissed it by reasoning, rather
       classList = call.getReceiver() and
       classList.getPropertyName() = "classList" and                   than flagging it. Examples from the Amazon app 1. "qty is
       isElementRef(id, classList.getBase()) and                       clamped to ≥ 1, so the qty=0 path is unreachable; not a bug." 2.
       call.getMethodName() = ["add", "remove", "toggle", "replace"]
    )                                                                  "the qty=99 cap is product-specific per the comment, so missing
    // (style.setProperty/removeProperty — omitted for space)          on other products is likely intentional"; and 3. "USER_TIER is a
}
                                                                       const initialized to ’free’, so the enterprise branch is dead code,
                                                                       not a defect."
                                                                       Received 2026-07-11; accepted 2026-08-14
