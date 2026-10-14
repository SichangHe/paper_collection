                                        SmartPoC: Generating Executable and Validated PoCs for Smart
                                                           Contract Bug Reports
                                                           Longfei Chen                                  Ruibin Yan                                  Taiyu Wong
                                                        Tsinghua University                People’s Public Security University of                Tsinghua University
                                                           Beijing, China                                  China                                    Beijing, China
                                                                                                      Beijing, China

                                                           Yiyang Chen                                  Jialai Wang                                 Chao Zhang∗
                                                        Tsinghua University                  National University of Singapore                    Tsinghua University
                                                           Beijing, China                         Singapore, Singapore                              Beijing, China
arXiv:2511.12993v3 [cs.SE] 1 Apr 2026




                                        Abstract                                                                 frameworks [12, 18, 44]. Although prior systems [20, 22, 33, 55]
                                        Smart contracts are commonly audited through static analysis to ex-      have explored synthesizing exploit traces via fuzzing, symbolic
                                        plore vulnerabilities. However, static approaches typically produce      execution, and other program analyses, they typically depend on
                                        heterogeneous findings rather than reproducible, executable proof-       expert-crafted predicates and bug-specific oracles. These oracles
                                        of-concept (PoC) test cases, leading to costly and ad hoc manual         generalize poorly to the heterogeneous vulnerabilities prevalent
                                        validation. Large language models (LLMs) offer a promising way           in modern DeFi protocols [56]. As a result, even with increasingly
                                        to translate audit reports into PoC test cases, but face three major     capable static analyzers, auditors still author most PoCs manually.
                                        challenges: noisy inputs, lack of execution grounding, and missing       This process is labor-intensive and scales poorly with the growing
                                        runtime oracles. We present SmartPoC, an end-to-end approach for         volume of reported findings.
                                        validating reported vulnerabilities in audit reports by generating           Large Language Models (LLMs) provide a promising avenue for
                                        and executing PoC test cases with automated exploitability verifi-       this task. With strong code understanding and synthesis capabili-
                                        cation. SmartPoC first extracts a focused function-level slice from      ties [2, 14, 25, 50, 51, 54], they can, in principle, transform textual
                                        each report to reduce noise, centering on the key functions refer-       audit findings into executable PoC tests. However, end-to-end, vali-
                                        enced in a finding and augmenting them with execution-relevant           dated PoC generation from generic static-analysis outputs still faces
                                        neighbors. To improve executability, we wrap LLM-based PoC syn-          three persistent challenges: (i) Noisy inputs to LLMs. Vulnera-
                                        thesis in a generate–repair–execute loop, combining deterministic        ble contracts often include substantial functionality unrelated to
                                        pre-execution sanitization with feedback-driven post-execution de-       the reported issue, resulting in long and unfocused prompts. This
                                        bugging. We further use differential verification as an oracle to con-   long, noisy context prevents the model from concentrating on the
                                        firm the exploitability of generated test cases. On the SmartBugs-       true trigger conditions and consequently degrades PoC generation
                                        Vul and FORGE-Vul benchmarks, SmartPoC achieves confirmation             quality. (ii) Lack of execution grounding. LLMs may generate
                                        precision of 98.32% and 98.65%, with recall of 84.17% and 85.28%, re-    unsupported APIs or incorrect environment assumptions, causing
                                        spectively. On a recent Etherscan verified-source corpus, SmartPoC       compilation failures. More critically, they may override target meth-
                                        confirms 64 bugs from 545 audit findings at an average cost of $0.03.    ods, inadvertently patching the bug or creating a fake one, so the
                                                                                                                 “PoC” validates the LLM-written code rather than the original con-
                                                                                                                 tract logic. (iii) Lack of a bug oracle. There is no general, reliable
                                        1    Introduction
                                                                                                                 mechanism to determine whether a PoC execution truly triggers the
                                        Smart contracts have become critical infrastructure for decentral-       reported bug, which hinders scalable verification of audit findings.
                                        ized applications, but their immutability and direct control over            In this work, we present SmartPoC, an end-to-end framework
                                        funds make vulnerabilities uniquely costly [27, 57]. Numerous            that validates smart contract vulnerability findings through PoC
                                        tools perform static analysis [10, 30, 42, 49, 53] on contract code      generation and execution. The core idea is to build a verifiable sys-
                                        and generate vulnerability reports spanning a broad range of bug         tem that harnesses LLMs for reliable PoC generation. To address
                                        classes. However, static findings often exhibit high false-positive      the challenges above, SmartPoC consists of three key components:
                                        rates [15, 23, 24, 35] and rarely include executable evidence. Conse-    (i) Bug-context extraction (BCE). To reduce input noise, BCE
                                        quently, practitioners have to conduct costly, ad hoc manual verifi-     extracts a focused function-level slice centered on the key func-
                                        cation to determine whether reported issues are truly exploitable.       tions referenced in a finding, and augments it with semantic and
                                        We refer to this disconnect between detection and confirmable            structural links. The resulting context captures the execution pre-
                                        exploitability as the verification gap.                                  requisites for PoC generation while keeping prompts compact. (ii)
                                           In practice, auditors rely on executable proof-of-concept (PoC)       Generate-repair-execute engine (GRE-Engine). To improve
                                        tests to validate static findings. A PoC reproduces the vulnerable       executability, GRE-Engine performs iterative synthesis with two
                                        condition in a realistic runtime environment, encoding both (i)          repair modules. A pre-execution sanitizer normalizes the environ-
                                        a triggering call sequence and (ii) an oracle that verifies the ex-      ment and prevents unintended contract rewrites, reducing the risk
                                        pected effects, making exploitability reproducible within testing        that generated PoCs mask the original bug. A post-execution de-
                                        ∗ Corresponding author.
                                                                                                                 bugger collects compiler and runtime diagnostics and feeds them
Conference’17, July 2017, Washington, DC, USA                            Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang


back to the generator, enabling targeted repairs until the PoC ex-        1 contract SimpleNFT {
ecutes successfully. (iii) Action-state differential verification         2      mapping(uint=>address) public ownerOf;
                                                                          3      function mint(uint id) external {
(DV). DV uses the GRE-Engine to instrument each PoC with pre-             4           // Bad Access Control: anyone can reassign the owner of any ID
and post-trigger state queries, executes the test, and compares the       5           ownerOf[id] = msg.sender;
resulting snapshots. A differential state change consistent with the      6      }
vulnerability semantics indicates successful exploitation, providing      7 }
an automatic oracle suitable for large-scale PoC verification.
   We instantiate SmartPoC with DeepSeek-R1 [17] as the default          Figure 1: Access-control lapse requiring semantics-aware val-
PoC generator and evaluate it on three datasets: the traditional         idation. In mint, any caller can reassign the owner of any
benchmark SmartBugs-Vul, the expert audit-report corpus FORGE-           token ID; confirming exploitability needs an ownership ora-
Vul, and the real-world Latest-114 from Etherscan verified-source        cle (e.g., ownerOf[id] == attacker) rather than generic profit
contracts. On the ground-truth benchmarks, SmartPoC’s achieves a         signals.
precision of 98.32% and 98.65%, with a recall of 84.17% on SmartBugs-
Vul and 85.28% on FORGE-Vul, respectively. SmartPoC validates
507 and 282 findings produced by six static analyzers [10, 30, 42,       report cannot faithfully capture. In addition, static analyzers such
48, 49, 53] on the two benchmarks, with manual adjudication yield-       as Slither [10] include many detectors spanning diverse bug classes
ing PPV/NPV of 76.47%/70.39% and 80.00%/89.72%, respectively.            and scan for extensive sets of patterns, often producing large num-
In the real-world study, SmartPoC validates 236 of 545 static-tool       bers of candidate findings with heterogeneous descriptions. As a
findings on Latest-114, achieving an audited precision of 75.29%         result, they can exhibit high false-positive rates [15, 23, 24, 35] and
and an average validation cost of $0.03 per finding. We further          impose substantial manual effort for triage and confirmation. We
conduct ablation studies to quantify the contribution of each com-       refer to this growing divide between static detection and confirmed
ponent and assess robustness to the LLM backend by substituting          exploitability as the verification gap.
GPT-5-mini [1] for DeepSeek-R1. Overall, the results show that
SmartPoC effectively translates static-analysis findings into exe-       2.2    The Format of Static Reports
cutable, runtime-grounded validation.
   We summarize our main contributions as follows:                       In practice, static vulnerability reports primarily originate from
                                                                         two sources. The first is audit reports written by human experts,
     • We propose an end-to-end approach that dynamically vali-          which are often semantically rich and may include the vulnerable
       dates generic static-analysis reports by generating and exe-      location, a textual explanation of the issue, potential consequences,
       cuting PoCs.                                                      and mitigation recommendations. The second is tool-generated
     • We design and implement SmartPoC, which integrates three          findings, which are typically more structured and concise, often
       key components—BCE, GRE-Engine, and DV—to robustly                containing only a vulnerability label and a code location. Recent
       handle noisy inputs and lack of execution grounding, and to       LLM-based auditing tools further blur this distinction by enriching
       provide automated runtime oracles.                                structured findings with natural-language descriptions. Despite
     • We integrate SmartPoC with multiple static analyzers and          these differences, we abstract all such inputs as generic findings.
       validate 64 real bugs in the latest Ethereum corpus at an            For SmartPoC, each generic finding provides two essential sig-
       average cost of $0.03 per validated finding.                      nals: the suspected location and a textual description of the vulner-
     • We release a large-scale dataset of 382 triplets linking con-     ability type or semantics. The location may be specified as a line
       tract source code, natural-language bug descriptions, and         range, a function name, or a program point that can be mapped
       execution-validated PoCs. To the best of our knowledge, this      to the corresponding function, whereas the description may range
       is among the largest publicly available datasets that combine     from a short label to a more detailed natural-language explanation.
       these three artifacts.
                                                                         2.3    Proof-of-Concept and Runtime Oracle
2 Background
                                                                         PoC definition. A PoC is an executable artifact that demonstrates
2.1 The Verification Gap of Static Analysis                              whether a reported vulnerability can be triggered in a realistic
Many smart-contract vulnerability detection solutions rely on static     environment. Unlike descriptive static warnings, a PoC makes ex-
analysis, including rule- and pattern-based analyzers [10, 27, 29, 30,   ploitability testable by encoding (i) a triggering call sequence and
34, 43, 49] as well as learning- or LLM-assisted approaches [5, 28,      (ii) an oracle that validates the expected effects, thereby turning
41, 42, 48, 53]. Despite their differences, these tools share a com-     descriptive findings into execution-grounded evidence. In practice,
mon limitation: they operate on static code snapshots and typically      PoCs are commonly instantiated either as vulnerable transaction se-
output descriptive findings, such as warnings, locations, and brief      quences (i.e., multi-transaction execution traces) or as reproducible
explanations, rather than executable evidence that can be validated      test harnesses implemented in standard testing frameworks such
at runtime. This limitation reflects the inherent difficulty of recov-   as Foundry [12], Hardhat [18], and Truffle [44].
ering dynamic dependencies through static reasoning alone. For               Runtime oracle. Executing a trigger alone demonstrates only
example, a detector may flag a “reentrancy-like” pattern in isola-       path feasibility, not exploitability. Confirming a vulnerability re-
tion, yet the vulnerability may only materialize under a specific        quires an oracle to determine whether the observed outcome con-
inter-contract initialization and liquidity sequence, which a static     stitutes a security-relevant misuse. Profit-based criteria are natural
                                 Semantic
                                 Expansion
                                                                                       Key Functions                                                                     retry
          SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports                                                       Conference’17, July 2017, Washington, DC, USA



                                                   Bug-Context Extraction                       Generate-Repair-Execute Engine                       Action-State Differential Verification
                                                           Key Functions
                Static Finding     Input                                                       Raw PoC                                                                     4
                                                           Identification                                                       Sanitized PoC

                                                                 1                                                                                   Verification       Verified
                                                                                                   1         Pre-Execution          2                                                   Vulnerability
                                                                                                               Sanitizer                                                                 Confirmed
                Contract Code                Call Graph              Semantic                                                                          3       Logs
                                                                                  2
                                                                     Expansion
                                                                                                                                                                           2
                                                                                                                 Error Logs
                                                             Structural                                                                                                                1: diff.test();
            Bug-Related Patterns                             Expansion                      PoC Generation                                                                             2: trigger();
                                                                                                                       3       Execution Test                          Insertion
                                                                                                                                                                                       3: diff.test();
                         Inverse                                 3                                                                                  GRE-Engine
                      State-Coupled                                                                                                                                                  Differential PoC
                                                                                                       4
                                                     Context                                                                            Success                 Action: a, b
                 Semantic Links                                                                                                                        1
                                              4     Assembly                                 Fixing Prompt Post-Execution                                       State: x, y
                                                                                                             Debugger
                        Modifier
                                                                 Description-aligned                Turning static                                                               Adding differential
                         Wrapper
                                                                 bug-related context                 findings into            1: trigger();                                       tests to verify the
                 Structural Links            Bug Context             extraction                    executable PoC                                                                   causal trigger
                                                                                                                             Executable PoC           Extractor



                                                                          Figure 2: The high-level workflow of SmartPoC.
                Semantic
                Expansion
Key Functions           Bug-related
         for profit-driven    DeFi exploits, but they do not generalize to se-                                             Semantic Links                               Structural Links
                         Functions
         mantic violations such as privilege escalation, unauthorized state
        Function                                                                                                              Slither                          Context Extraction
                   Structural                                                                                  1     function deposit();                 1 modifier onlyOwner(){
          Set
         transitions,          2
                       or broken    invariants. Figure 1 shows a typical access-
                   Expansion
                                                                                                               2     function withdraw();
                                                                                                                                     Call Graph          2     require(isOwner)
          control flaw: the mint function allows an arbitrary caller to as-                                Contract Codes
                                                                                                               3                                         3 }
          sign ownership of any token ID. Successful exploitation in this                                      4     function mint();                    4 Set
                                                                                                                                                      Function
          case is not necessarily immediately profitable; instead, it requires a                               5     function burn();                    5 function auth() onlyOwner
          semantics-aware identity or uniqueness oracle. For example, one                                                                                                                  Bug Context
 Call Graph                                                                                                    a. Semantic LLM
                                                                                                                           Inverse Operations                     c. Modifier-Based Control
          may assertFunction
                       ownerOf[id] == attacker and optionally preOwner                                                                                 LLM
                                3
          != attacker Context
                          to detect the bug. Empirically, approximately 80% of
                                                Bug-Related
          real-world smart contract vulnerabilities   are logic-centric [56]. For                              1 Finding
                                                                                                           Static  function setFee(){
                                                                                                                                  Key Functions            1     function  _transfer(){
                                                                                                                                                                    Bug-related
                                                 Functions
          such issues, profit-based oracles alone are often insufficient; instead,                             2   totalFee = x;                           2       //Functions
                                                                                                                                                                      Actual transfer logic
                         Bug Context
          validation requires   semantics-aware runtime checks over security-                                  3 }                                         3     }
                                                                                                               4 function checkFee(){                      4     function transfer(){
          relevant state changes, privilege violations, or broken invariants.
                                                                                                               5   return totalFee;                        5       _transfer();
          In practice, these checks remain largely handcrafted, making ex-                                     6 }                                         6     }
          ploitability validation both time-consuming and error-prone.
                                                                                                                 b. State-Coupled Operations                      d. Wrapper Function Flow

          3 Methodology
                                                                                                               Figure 3: Bug-related patterns in smart contract code.
          3.1 Overview
         The workflow of SmartPoC is shown in Figure 2. SmartPoC trans-
         forms the inputs into executable, validated PoCs in three stages:
         (1) Bug-Context Extraction (BCE) uses the static finding to lo-                                   idea is to bracket the PoC trigger with a concrete action (i.e., a
         cate the report-referenced functions. It then expands these func-                                 call or short call sequence) and monitor a bug-related state (i.e.,
         tions via semantic and structural links and assembles the corre-                                  public variables or view functions). DV confirms a PoC only when
         sponding function-level slice as the LLM context. This context                                    the observed pre/post difference is explicit and consistent with the
         preserves bug-relevant semantics and common setup prerequisites,                                  report. For each finding, SmartPoC returns the PoC together with
         while avoiding the noise of the full project. (2) Generate-Repair-                                the differential evidence. If validation fails, SmartPoC marks the
         Execute Engine (GRE-Engine) converts the finding and BCE                                          finding as not validated under our oracle.
         context into an executable PoC by wrapping LLM synthesis in
         an iterative generate–repair–execute loop. It includes two repair                                 3.2       Bug-Context Extraction
         modules. A pre-execution sanitizer normalizes project-specific de-                                BCE aims to construct a compact context that captures the infor-
         pendency details and blocks test-level non-faithful edits that could                              mation required for PoC execution. It reduces prompt noise by
         override the target behavior. A post-execution debugger leverages                                 extracting a focused function-level slice instead of feeding the en-
         compiler and runtime diagnostics to guide regeneration until the                                  tire contract to the LLM. It starts from the functions referenced by
         PoC executes or the retry budget is exhausted. (3) Action–State                                   the finding and includes a one-hop expansion on the call graph.
         Differential Verification (DV) provides execution-grounded evi-                                   However, bug-local context alone is often insufficient as a work-
         dence of exploitability through controlled comparisons. The core                                  ing PoC must first drive the contract into an exploitable pre-state.
Conference’17, July 2017, Washington, DC, USA                                                  Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang


                      Slither                       Structural-Link Extraction
                                                                                                       Generation Prompt Template
     Contract Code                Call Graph                                                           System: You are a smart contract audit expert. Based
                                                Function Set                                           on the provided messages, your task is to generate a
                                                                                 Bug Context           Foundry-compatible test script.
                      LLM                          LLM

                                                                                                       Input:
     Static Finding             Key Functions             Semantic-Related                             ## Vulnerability Description
                                                             Functions
                                                                                                       ## Code Snippets
                                                                                                       ## Project Information & Build Metadata
        Figure 4: Workflow of Bug-Context Extraction.                                                  ## One-shot Example:
                                                                                                       [example input and output]

                                                                                                       Output: The test script is {code}
To support such runtime prerequisites, BCE further expands the
function set using empirically observed patterns.
   We summarize four common links between functions that fre-                                                Figure 5: Prompt for PoC generation.
quently arise in audited contracts, as illustrated in Figure 3. (a)
Semantic inverse operations. Some contracts expose complementary
operations with opposite effects. A PoC may require the inverse                                matching brittle. We therefore formulate key-function identifica-
operation to establish the pre-state before triggering the reported                            tion as a closed-set selection task: we provide the LLM with the
entry point. For example, a report may highlight withdraw, but the                             recovered function list and require it to select the report-referenced
PoC must call deposit first to fund the attacker. (b) State-coupled                            functions only from this list. We then verify the selections against
operations. Some operations interact through shared state, while up-                           the same list and drop any out-of-set symbols, further mitigating
dates and validations are implemented in different functions. A PoC                            hallucinated function names. To expand semantic links, we use
may need both functions to make a state change observable and to                               few-shot [3] prompts with a set of pre-defined semantic inverse
reach the target path. For example, setFee updates a fee parameter,                            and state-coupled operations drawn from common contract idioms.
while the fee bound may be enforced by checkFee during use. The                                Guided by these patterns, the LLM selects semantically related
next two are structural links that affect how the PoC should invoke                            functions from the recovered function list. We include the selected
the contract. (c) Modifier-based control. Modifiers commonly encode                            functions as additional execution context so that GRE-Engine can
authorization and validity checks that gate execution [9]. A PoC                               access prerequisite states beyond the bug-referenced entry points.
should account for these checks to avoid failing before reaching the                              After that, we expand the context along control-flow structure
vulnerability trigger. For example, onlyOwner requires the PoC to                              rooted at these functions. We first include the call-graph edges
impersonate the owner or to set ownership accordingly. (d) Wrap-                               among the selected functions, and then add their direct callees
per function flow. A common Solidity design pattern is to expose                               and callers. To handle wrapper patterns, we recursively include
a public-facing API that forwards to underscore-prefixed internal                              underscore-prefixed internal functions reachable from these callers
helpers implementing the core logic [38]. A PoC should preserve                                and callees until we reach the non-underscored implementations.
this call structure to interact with the contract as intended. For                             We also attach all referenced modifiers to preserve pre-/post-
example, transfer may delegate to _transfer where balance up-                                  condition checks and access-control boundaries. To support correct
dates occur. Together, these patterns help retain execution-critical                           initialization during generation, we include constructors and, when
context for exploit reproduction, which are not reliably captured                              present, initializer routines for the contracts that define the sliced
when slicing only around local control-flow. To estimate how often                             functions. We also extract from the code the project and build
these links appear in practice, we perform a lightweight lexical scan                          metadata needed for compilation, such as the compiler version
over 373 real-world audit projects from FORGE [4]. We find that                                and remappings. Finally, we deduplicate the resulting function set
97.61% of projects contain at least one of the four links, indicating                          while preserving reachability order, and package everything into a
that these patterns are prevalent in real codebases.                                           compact bug-context bundle for subsequent PoC generation.
   As shown in Figure 4, BCE is seeded with the contract code and
a corresponding static finding, where each finding is represented                              3.3    Generate-Repair-Execute Engine
by two fields: a location and a vulnerability description. For normal-                         GRE-Engine turns textual vulnerability descriptions into executable
ized findings produced by static analyzers, BCE directly maps the                              PoCs via an automated generate–repair–execute loop that itera-
reported location to the corresponding function(s). For more hetero-                           tively prompts an LLM. Its core consists of two repair stages: a
geneous findings, such as audit reports or LLM-generated findings,                             pre-execution sanitizer and a post-execution debugger. The sani-
BCE identifies the key function(s) from the vulnerability description.                         tizer applies deterministic rules to fix runtime dependencies and
We first run Slither [10] to recover the call graph and a canonical                            block non-faithful behaviors, while the debugger collects compiler
function list of the project. Next, instead of directly matching func-                         and runtime failures and uses the resulting diagnostics to guide
tion names mentioned in the report, we ask the LLM to identify the                             regeneration.
referenced functions, which we denote as key functions. Reports                                   In practice, we observe three recurring failure modes when us-
often mention functions in non-canonical forms—e.g., case varia-                               ing LLMs to generate PoCs. First, LLMs are often not framework-
tions, minor typos, or formatting differences—which makes string                               version aware. As libraries evolve, they may call deprecated APIs
     SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports                                         Conference’17, July 2017, Washington, DC, USA


             Regeneration Prompt Template                                                        // pre-state
                                                                                               1 preAdmin = Admin(proxy);
                                                                                                 // action
ed            System: Please fix the test code according to the log                            2 AttackerCallUnprotectedInitializerOrUpgrade();
ea            above and regenerate the complete test script.                                     // post-state
                                                                                               3 postAdmin = Admin(proxy);
                                                                                                 // verify state change
              Input:                                                                           4 require(preAdmin != Attacker && postAdmin == Attacker, "Admin changed!");
              ## Generation Prompt
              ## Previous Generated Test:
              ```solidity                                                                Figure 7: DV for proxy-control takeover. DV snapshots the
              {previous PoC}                                                             proxy’s upgrade authority (admin) before and after the ini-
              ```                                                                        tializer/upgrade trigger (Lines 1–3), and then checks whether
              ## Error Logs:                                                             control has been illicitly transferred to the attacker (Line 4).
              {error log}

              Output: The fixed script is {code}
                                                                                         3.4      Action–State Differential Verification
                                                                                         While GRE-Engine produces PoCs that compile, execute, and in-
             Figure 6: Prompt for post-execution debugger.
                                                                                         teract correctly with the target contract, action–state differential
                                                                                         verification validates their execution outcomes and semantic cor-
                                                                                         rectness. We define a state as a bug-relevant observable value (e.g.,
                                                                                         a public variable or view function result) obtained from execution,
                                                                                         and an action as the concrete interaction (e.g., a call or short call
     or use outdated import paths, leading to compilation failures [45].                 sequence) used to obtain that value. By comparing the state before
     Such version mismatches are difficult to resolve through prompting                  and after under matched controls, we determine whether the vul-
     alone. Second, LLMs may “cheat” to satisfy the report narrative.                    nerability produces a real, report-consistent effect. This approach
     They may override target methods inside the PoC and inject a vul-                   leverages the LLM to tailor bug-specific oracles to complex protocol
     nerable behavior to force the expected state change. In this case,                  logic while keeping the final decision rule simple and auditable. It
     the test exercises the overridden implementation rather than the                    avoids prior work’s reliance on hand-crafted oracles and enables
     original contract, producing a false confirmation even when the                     verification for generic static-analysis findings.
     target code is not actually vulnerable. Third, a PoC may compile                       Although triggers and root causes vary across bugs, confirming
     but still fail at execution time. A PoC must interact with the target               exploitability requires execution-grounded evidence. We therefore
     project in a concrete runtime environment, and mismatched calls,                    base DV on observable runtime traces, including queried state val-
     missing setup steps, or incorrect assumptions can cause interac-                    ues and call outcomes, and compare them under matched controls.
     tion failures. Resolving such failures typically requires dynamic                   Typical evidence includes (i) direct changes in variables (e.g., bal-
     feedback from compilation and test execution.                                       ances, ownership, and liquidation thresholds), and (ii) changes in
        To address these challenges, we organize PoC generation into                     function return values or effects (e.g., success flags of authorization
     an iterative loop. The process begins by prompting the LLM to                       checks). If we can localize such a state and test its pre-/post- val-
     generate an initial draft (Figure 5). The draft then passes through                 ues around the trigger, DV can often reduce validation to a single
     a pre-execution sanitizer to address the first two issues. We select                outcome-based check. Figure 7 illustrates a proxy-control takeover
     Foundry [12] as the testing framework and pre-adapt the environ-                    example. The trigger occurs on Line 2, where the attacker exploits
     ment across Solidity compiler versions. Specifically, we extract the                an unprotected initializer or upgrade path to seize the proxy’s up-
     compiler version and library identifiers from the draft’s header di-                grade authority. We snapshot the proxy admin both before and after
     rectives and apply deterministic edits to ensure compatibility with                 the trigger (Lines 1 and 3) and compare the two values on Line 4
     the appropriate syntax and APIs. We also align the PoC with the tar-                to determine whether control has been illegitimately transferred
     get codebase by matching the target project’s canonical function list               to the attacker. In this setup, the attacker’s trigger sequence is the
     against the PoC, removing conflicting or redundant re-definitions,                  action, and the proxy’s admin address is the observable state.
     and rewriting imports to correctly reference the required headers.                     To operationalize this idea, we design a differential verification
     These deterministic fixes substantially reduce compilation failures                 pipeline that decides exploitability by checking localized, publicly
     and enforce that PoCs interact with the original contract code,                     observable state changes around the trigger. We follow three steps:
     mitigating non-faithful transformations. After the PoC passes pre-                  (1) Extraction. Given the finding description, the generated PoC,
     execution sanitizer, we run it in the test environment and record                   and the public ABIs (all externally visible functions and getters for
     any compilation or runtime errors. In the post-execution debugger,                  public state variables) derived from the source code in Section 3.2,
     we structure these diagnostics and prompt the LLM to revise the                     we prompt the LLM to identify (a) an action (one or a small sequence
     PoC accordingly (Figure 6). We retain the original conversational                   of function calls) that exercises the trigger and (b) the observable
     context to anchor the model to the finding and intended exploit                     state to monitor. As shown in Figure 8, the LLM selects candidate
     scenario. To keep each repair focused, we provide only the latest                   functions from the public ABIs for both the action and the state
     PoC draft and the diagnostics from the current round, omitting                      query. This design leverages the LLM’s understanding of the vul-
     older debugging history. We repeat this loop until the PoC executes,                nerability while constraining it to a contract-specific search space,
     or until the attempt budget is exhausted.                                           thereby narrowing the validation oracle.
Conference’17, July 2017, Washington, DC, USA                               Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang


         Prompt Template for DV Extraction                                  4 Implementation     and Setup
                                                                                        Prompt Template  for DV Insertion
         System: From the provided ABIs, choose the concrete                4.1 Dataset System: Please insert identical action and state-query
         actions to execute both before and after the PoC’s trigger,        Our evaluation usesoperations  from differential
                                                                                                   three datasets:           description
                                                                                                                    a community          before and
                                                                                                                                   benchmark         after
                                                                                                                                                 Smart-
         and observable states whose values should be compared.                                the PoC’s critical attacker action, compare the results,
                                                                            Bugs [11], a corpus   of projects from expert audit reports FORGE [4],
                                                                                               and log both the state values and each executed step.
         Input:                                                             and a real-world collection of Ethereum contracts Latest-114.
         ## Vulnerability Description                                       SmartBugs covers   Input:
                                                                                                  ten canonical vulnerability types, together with
         ## Public ABIs                                                                        ## PoC and labels. Because Foundry provides lim-
                                                                            corresponding contracts
         ## PoC                                                                                ## Differential Description
                                                                            ited support for older Solidity versions, we upgrade all contracts to
         ## Few-shot Examples:                                                                 ## Few-shot Examples:
         [example input and output]                                         Solidity ≥ 0.8 through    LLM-assisted,
                                                                                               [example                 human-validated edits. Dur-
                                                                                                         input and output]
                                                                            ing this process, we exclude vulnerability classes that no longer
         Output: The action and state are {"action":[], "state":[]}         manifest after theOutput:
                                                                                                 upgradeThe(short
                                                                                                              code is: {code}and others). For each re-
                                                                                                                   address
                                                                            tained sample, we use the dataset-provided description and map
                                                                            the location to the relevant key functions. The resulting benchmark
               Figure 8: Prompt for DV extraction.
                                                                            contains 139 vulnerability samples, denoted as SmartBugs-Vul.
                                                                            FORGE consists of project codebases paired with commercial audit
                                                                            reports. For each project, we retain the source code and report,
                                                                            and then: (i) extract only high- and critical-severity findings; (ii)
         Prompt Template for DV Insertion
                                                                            perform batch compilation to exclude projects with incomplete
         System: Please insert identical action and state-query             or irreproducible code; (iii) segment each report into per-finding
         operations from differential description before and after          units with LLM assistance. We discard items that lack a concrete
         the PoC’s critical attacker action, compare the results,
                                                                            location. This process yields 428 vulnerability instances, denoted
         and log both the state values and each executed step.
                                                                            as FORGE-Vul, covering 24 CWE types.
         Input:                                                                To simulate false positives in static-analysis reports, we construct
         ## PoC                                                             SmartBugs-Fix and FORGE-Fix by patching the underlying vulner-
         ## Differential Description                                        abilities while keeping the original textual descriptions unchanged.
         ## Few-shot Examples:
         [example input and output]
                                                                            These fixed sets are used to evaluate whether SmartPoC can avoid
                                                                            confirming non-vulnerable code despite persuasive vulnerability
         Output: The code is: {code}                                        narratives. For SmartBugs-Fix, we repair all vulnerable instances.
                                                                            For FORGE-Fix, because manual patching is costly, we patch a
                                                                            fixed budget of 100 instances. Specifically, we adopt CWE-stratified
                Figure 9: Prompt for DV insertion.
                                                                            sampling. To ensure coverage of long-tail categories, we first select
                                                                            at least two instances from each CWE type. We then allocate the
                                                                            remaining budget proportionally according to the frequency of each
                                                                            CWE type and randomly sample instances within each stratum.
(2) Insertion. We use GRE-Engine to materialize the selected action         All patches are produced independently by two domain experts
and state as code, producing an executable PoC with embedded                and cross-validated. During patching, we preserve the intended
differential checks. As shown in Figure 9, we provide the LLM with          contract functionality and keep function signatures unchanged to
the original PoC and the extracted action/state pair and ask it to          remain consistent with the original vulnerability reports.
insert the corresponding calls and assertions into the test. For each       Latest-114 is collected from Etherscan’s verified-source corpus
pre-/post-action segment and at the trigger, we instruct the LLM to         through the public API [7]. On October 22, 2025, we queried the 150
insert structured log statements that record the executed step and          most recently verified projects and reconstructed the corresponding
the current state value. In this way, the abstract oracle is instantiated   build environments. After normalization, 114 projects compiled suc-
as a concrete, executable test that can be run and inspected. During        cessfully, forming the Latest-114 dataset. This dataset evaluates
both extraction and insertion, we provide few-shot examples to help         SmartPoC in a recent real-world setting by assessing how effec-
the LLM follow instructions and translate vulnerability semantics           tively it validates static-analysis findings on organically developed
into causal decisions and concrete execution logic.                         contracts deployed on-chain.
(3) Verification. After execution, we parse the structured logs to
extract the pre- and post-state and compute the corresponding               4.2     Baselines
deltas. When a state change is observed, we further query an LLM            Three recent studies are related to automated exploit generation for
to sanity-check whether the change constitutes evidence for the re-         smart contracts, namely A1 [14], PoCo [2], and REX [51]. REX fol-
ported vulnerability. We label a PoC as successful only if it induces       lows an iterative prompt-driven exploit-synthesis paradigm, PoCo
a vulnerability-relevant state change under this check. In this de-         adopts an agentic report-to-PoC generation paradigm, and A1 tar-
sign, successful execution ensures that the exercised path is feasible,     gets an agentic exploit-discovery setting over deployed contracts.
while the LLM-based sanity check validates the vulnerability se-            Since these works do not provide publicly runnable implementa-
mantics. Together, these steps automatically derive runtime oracles         tions, we construct controlled baselines that capture the representa-
that validate LLM-generated PoCs and confirm exploitability.                tive PoC-generation workflows described in these studies. Iterative
SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports                                 Conference’17, July 2017, Washington, DC, USA


is an iterative baseline inspired by REX. It generates a PoC from                   Table 1: Evaluation of SmartPoC on benchmarks. We report
the target contract and vulnerability report, executes the result,                  TP/FP for Vul sets and TN/FN for Fix sets by manual verifi-
and iteratively revises it using compilation and execution feedback.                cation. Execution Passed counts PoCs after the GRE-Engine
Agentic is the baseline inspired primarily by PoCo and A1. It allows                stage, while SmartPoC Confirmed counts the final PoCs con-
the LLM to plan, implement, execute, and debug the PoC itself. We                   firmed by SmartPoC.
also include four simplified variants of SmartPoC: w/o BCE, which
uses the flattened full contract as context; w/o Semantic Links, which                 Dataset         Bugs
                                                                                                               Execution Passed    SmartPoC Confirmed
retains only the control-flow-reachable slice from the key functions;                                         DeepSeek     GPT     DeepSeek      GPT
w/o Pre-Repair, which removes the pre-execution sanitizer; and w/o                     SmartBugs-Vul    139    120/17     122/9      117/2       116/2
Post-Repair, which removes the post-execution debugging module.                        FORGE-Vul        428    369/26     380/23     365/5       376/3
                                                                                       SmartBugs-Fix    139     -/64       -/87       63/1       85/2
                                                                                       FORGE-Fix        100     -/57       -/63       56/1       63/0
4.3     Experimental Setup
Framework settings. All experiments use the open-source rea-
soning model DeepSeek-R1-0528 [17]. To assess robustness, we also                         • RQ3: How does SmartPoC perform in PoC generation
run a subset of experiments with GPT-5-mini [1]. Unless otherwise                           compared with baselines? We compare SmartPoC with
noted, we use default decoding with temperature 0.3 and set the                             several representative PoC generation settings and evaluate
GRE-Engine retry budget to 𝐵=5. For PoC generation and execu-                               the effectiveness of its key designs.
tion, we use Foundry as the testing framework, relying on the latest
release available during our experiments (forge 1.4.2-stable).                      5.1     Evaluation Metrics
Static analysis tools. We select (i) three widely used rule-/pattern-               We evaluate SmartPoC using standard confusion-matrix counts—
based analyzers [10, 30, 49], and (ii) three state-of-the-art LLM-                  TP, TN, FP, and FN—computed by comparing SmartPoC’s valida-
assisted analyzers [42, 48, 53]. We run each tool with default config-              tion outcomes against expert adjudication. We treat findings that
urations with a 1800-second time limit, and retain only high-severity               SmartPoC confirms as vulnerable as positives, and those it rejects as
findings. For each finding, we provide SmartPoC with the vulnera-                   negatives. A confirmed case is counted as TP if the vulnerability is
bility narrative and the implicated functions. Slither [10] translates              indeed exploitable; otherwise it is FP. A rejected case is counted
Solidity into SlithIR and performs rule-based checks augmented                      as TN if the code is non-vulnerable; otherwise it is FN. We report
with data-/control-flow analysis (6k GitHub stars). Mythril [30]                                                               TP             TP
                                                                                    recall and predictive values: Recall = TP+FN    , PPV = TP+FP  , and
symbolically executes EVM bytecode to explore feasible paths                                   TN
                                                                                    NPV = TN+FN . Here, Recall measures the fraction of ground-truth
and flag suspicious behaviors (4.1k Github stars). CPG Contract                     vulnerabilities for which SmartPoC produces and validates an ef-
Checker (CCC) [49] converts source into a Code Property Graph                       fective PoC. PPV measures the credibility of confirmations, i.e., the
and uses declarative graph queries that encode “vulnerability pat-                  fraction of SmartPoC-confirmed cases that are truly exploitable.
tern + data/control-flow conditions + exceptions/mitigations,” en-                  NPV measures the correctness of rejections, i.e., the fraction of
abling precise structural matching. GPTScan [42] defines per-class                  SmartPoC-rejected cases that are indeed non-vulnerable. Together,
scenarios and properties for 10 logic-bug classes and prompts an                    these metrics capture both PoC reproduction effectiveness and the
LLM for classification and explanation, aided by lightweight static                 reliability of SmartPoC’s validation decisions.
slicing and simple validation. FTSmartAudit (FT) [48] distills high-
quality audit data and performs lightweight fine-tuning with a                      5.2     RQ1: Validation Accuracy on Vul/Fix Sets
rationale-aware dual loss; an iterative filter–refine loop compresses               We evaluate whether SmartPoC can correctly validate reported
a general LLM into a compact, audit-specialized model. SMART-                       vulnerabilities on vulnerable contracts while rejecting misleading
LLAMA-DPO (DPO) [53] jointly learns vulnerability classification                    reports on patched contracts in Table 1. All outcomes are inde-
and explanation within a single framework, then applies direct                      pendently adjudicated by two security experts and categorized as
preference optimization to align explanation quality with human.                    TP/FP for the Vul sets and TN/FN for the Fix sets.
                                                                                       Using the SmartPoC Confirmed column as the final outcome,
5     Evaluation                                                                    SmartPoC achieves recalls of 84.17% (117/139) and 85.28% (365/428)
We aim to answer the following questions:                                           on SmartBugs-Vul and FORGE-Vul, with corresponding PPVs of
                                                                                    98.32% (117/119) and 98.65% (365/370), respectively. On SmartBugs-
      • RQ1: Can SmartPoC correctly validate vulnerabilities                        Fix and FORGE-Fix, it attains NPVs of 99.28% (138/139) and 99.00%
        reported in audit reports? Given benchmark and expert                       (99/100). Taken together, these results show that SmartPoC reli-
        audit reports, we evaluate whether SmartPoC can correctly                   ably validates real vulnerabilities while remaining conservative on
        validate these reported issues.                                             patched code, thereby demonstrating its effectiveness in validating
      • RQ2: Can SmartPoC serve as an execution-grounded                            the correctness of static vulnerability reports.
        verifier for analyzer findings? We run six analyzers to                     Effect of DV. The gap between Execution Passed and SmartPoC
        produce candidate findings on three datasets and then use                   Confirmed highlights the benefit of DV. It increases PPV from
        SmartPoC to validate them. We further manually audit ran-                   87.59% (120/137) to 98.32% on SmartBugs-Vul and from 93.42%
        dom samples of SmartPoC-confirmed and SmartPoC-rejected                     (369/395) to 98.65% on FORGE-Vul. On the repaired sets, DV cor-
        cases to estimate PPV and NPV.                                              rectly rejects 63/64 and 56/57 executable but non-exploiting PoCs.
Conference’17, July 2017, Washington, DC, USA                                Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang




     1 function
  1 function       payOut(uint
             payOut(uint       rand)rand) internal
                                      internal { {
                                                                                1 contract
                                                                             1 contract     xxx_Token
                                                                                        xxx_Token         is ERC20{
                                                                                                      is ERC20{
             if ( rand>
  2 2 if ( rand>      0 &&  0 &&   block.timestamp
                              block.timestamp          - rand
                                                  - rand  > 24>hours
                                                                24 hours
                                                                     ){ ){
                                                                             2 2 // omitted
                                                                                        // omitted
                                                                                                codecode
  3 3                msg.sender.send(msg.value);
               msg.sender.send(msg.value);
                                                                             3 3 if(feesif(fees
                                                                                            > 0){> 0){
  4 4                if ( this.balance
               if ( this.balance    > 0 )> leader.send(this.balance);
                                           0 ) leader.send(this.balance);
                                                                             4 4              // Parent
                                                                                         // Parent  ERC20ERC20   internal
                                                                                                             internal call.call.
  5 5 } }
                                                                             5 5              // Reverts
                                                                                         // Reverts       normally
                                                                                                     normally       on failure.
                                                                                                                on failure.
  6 6 else else     if ( msg.value
              if ( msg.value      >= 1>=  1 ether
                                        ether     ) leader
                                              ) leader      = msg.sender;
                                                        = msg.sender;
                                                                             6 6              super._transfer(from,
                                                                                         super._transfer(from,         address(this),
                                                                                                                  address(this),      fees);
                                                                                                                                 fees);
  7 }7 }
                                                                             7 7 } }
     8 function
  8 function       draw(uint
             draw(uint      seed)seed)  external
                                   external      payable{
                                             payable{
                                                                             8 8 amount amount    -= fees;
                                                                                             -= fees;
  9 9 uint uint     randomNumber
              randomNumber               = block.timestamp;
                                    = block.timestamp;
                                                                             9 }9 }
             payOut(randomNumber);
 10 10 payOut(randomNumber);
 11 }11 }
                 (a) Non-exploitable time manipulation.                                        (b) False positive from ERC20 inheritance.


Figure 10: Representative inaccuracies in the benchmark ground truth. (a) block.timestamp is used, but the settlement condition
is unreachable. (b) super._transfer() is an internal parent call that reverts on failure.


Sensitivity to LLM backends and cost. Replacing DeepSeek-                    Table 2: Evaluation of static findings on benchmarks. Counts
R1 with GPT-5-mini yields comparable recall, confirming 83.45%               include findings reported by each static analyzer and those
(116/139) and 87.85% (376/428) of cases on SmartBugs-Vul and                 verified by SmartPoC. PPV/NPV are estimated via manual ad-
FORGE-Vul, respectively. The average API cost is $0.03 per vali-             judication on random samples, with sample sizes computed
dation with DeepSeek-R1 and $0.04 with GPT-5-mini. The corre-                using the finite-population proportion formula.
sponding end-to-end latency is 52.14/60.47 s and 13.84/19.68 s on
the two datasets, respectively.                                               Dataset       Analyzer      Findings   SmartPoC       PPV              NPV
   Despite its strong overall performance, SmartPoC fails on a small                        Slither
                                                                                            Mythril
                                                                                                            91
                                                                                                            156
                                                                                                                       44
                                                                                                                       87
                                                                                                                                16/22 (72.73%)
                                                                                                                                23/33 (69.70%)
                                                                                                                                                 18/25 (72.00%)
                                                                                                                                                 20/27 (74.07%)
subset of cases. Manual inspection attributes these failures to two           SmartBugs-Vul
                                                                                            CCC             287        143      27/36 (75.00%)   20/37 (54.05%)
                                                                                            GPTScan          7          5         5/5 (100%)       2/2 (100%)
factors: (i) the intrinsic difficulty of PoC synthesis and validation,                      DPO             61         32       15/20 (75.00%)   14/19 (73.68%)
                                                                                            FT              413        196      31/37 (83.78%)   33/42 (78.57%)
and (ii) inaccuracies in the benchmark itself. We identify at least five
                                                                                            Slither          621       47       17/20 (85.00%)   70/78 (89.74%)
such cases in SmartBugs-Vul and nine in FORGE-Vul. Figure 10a                               Mythril           4         0              -          3/4 (75.00%)
                                                                                            CCC               0         0              -                -
shows an example from SmartBugs-Vul labeled as Time Manipula-                 FORGE-Vul
                                                                                            GPTScan          56        10        9/10 (90.00%)   15/30 (50.00%)
                                                                                            DPO             1533       129      16/20 (80.00%)   83/84 (98.81%)
tion. However, the claimed exploit path is infeasible: the settlement                       FT               363       96       14/20 (70.00%)   56/57 (98.25%)
branch is unreachable because block.timestamp always equals                                 Slither         133         62      20/26 (76.92%)   30/31 (96.77%)
rand. The reported vulnerability is therefore non-exploitable, and                          Mythril          9           5        5/5 (100%)      4/4 (100.0%)
                                                                              Latest-114    CCC             167         70      14/25 (56.00%)   36/37 (97.30%)
SmartPoC cannot generate a passing PoC. Figure 10b shows a case                             GPTScan          0           0             -                -
                                                                                            DPO              1           0             -           1/1 (100%)
from FORGE-Vul flagged as Unchecked Transfer. However, the high-                            FT              235         99      25/29 (86.21%)   39/40 (97.50%)
lighted call is super._transfer(), an internal ERC-20 routine that
reverts on failure rather than returning an unchecked Boolean value.
DV therefore finds no execution evidence supporting the reported             size using the standard finite-population proportion formula [26].
risk and rejects the case. These examples suggest that SmartPoC can          Specifically, we first compute the Cochran sample size for estimat-
also help expose mislabeled or non-exploitable benchmark entries,            ing a proportion under an infinite-population assumption with
providing useful signals for dataset curation.                               the standard settings (95% confidence, margin of error 𝑒 = 0.1,
                                                                             conservative 𝑝 = 0.5):
  Answer to RQ1: SmartPoC can effectively validate static vul-                                                  2 𝑝 (1 − 𝑝)
                                                                                                               𝑧𝛼/2
  nerability reports by transforming them into executable PoCs.                                         𝑛0 =            ,                     (1)
  Manual inspection further suggests that SmartPoC provides                                                     𝑒2
  actionable signals for benchmark curation and re-annotation.               and then apply the finite population correction (FPC) to obtain the
                                                                             final sample size:
                                                                                                               𝑛0
                                                                                                        𝑛=            ,                       (2)
5.3     RQ2: Verification of Static-Analyzer Reports                                                        1 + 𝑛0𝑁−1
We run six static analyzers on SmartBugs-Vul, FORGE-Vul and                  where 𝑁 is the number of findings produced by each static tool.
Latest-114, validate the high-severity findings with SmartPoC, and           We allocate the resulting sample budget between confirmed and
manually audit sampled outcomes. As shown in Tables 2, Findings              rejected cases in proportion to their counts, and then uniformly
denotes the number of high-severity reports produced by each an-             sample within each group to estimate PPV and NPV. When the
alyzer, and SmartPoC denotes the subset confirmed by SmartPoC.               computed 𝑛 is below 20, we round it up to 20 to ensure a minimum
PPV and NPV are determined through independent manual review                 level of stability.
by two experts. Because manual validation is costly, we adjudicate              Across the three benchmark datasets, SmartPoC achieves 76.47%
a randomly sampled subset. We determine the minimum sample                   (117/153), 80.00% (56/70) and 75.29% (64/85) PPV, along with NPV
SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports                                       Conference’17, July 2017, Washington, DC, USA


                          Table 3: Total PPV/NPV of different static analyzers with their average report length.

                                    CCC               Slither            Mythril            GPTScan            DPO                   FT
                    PPV        41/61 (67.21%)     53/68 (77.94%)     28/38 (73.68%)     14/15 (93.33%)    31/40 (77.50%)       70/86 (81.40%)
                    NPV        56/74 (75.68%)    118/134 (88.06%)    27/35 (77.14%)     17/32 (53.13%)    98/104 (94.23%)     128/139 (92.09%)
                    Length         11.92               36.42              54.26              101.54           105.92               167.23


of 70.39% (107/152), 89.72% (227/253) and 97.35% (110/113), respec-                   Table 4: Comparison of PoC generation performance under
tively. These results demonstrate SmartPoC’s ability to translate                     different configurations on ground-truth datasets.
static-analysis findings into executable PoCs and to reliably validate
or refute their exploitability. Manual inspection of successful PoCs                          Configuration            SmartBugs-Vul          FORGE-Vul
and their corresponding reports shows that static analyzers typi-
                                                                                              SmartPoC                 137/139 (98.56%)     395/428 (92.29%)
cally highlight only a small set of functions, whereas working PoCs                           Agentic                  132/139 (94.96%)     388/428 (90.65%)
almost always require a richer call chain. In our effective PoCs, we                          Iterative                 72/139 (51.80%)     175/428 (40.89%)
consistently observe both classes of relationships introduced in Sec-
                                                                                              w/o BCE                  121/139 (87.05%)     334/428 (78.04%)
tion 3.2. For example, Mythril may report “any sender can withdraw
                                                                                              w/o Semantic Links       103/139 (74.10%)     251/428 (58.84%)
Ether from the contract account” and pinpoints withdraw as the                                w/o Pre-Repair            57/139 (41.01%)     149/428 (34.81%)
vulnerable function. In practice, the exploit succeeds because a mis-                         w/o Post-Repair           25/139 (17.99%)      61/428 (14.25%)
configured modifier on withdraw delegates control to _withdraw,
the true sink, which is an instance of our structural links. Moreover,
the PoC must first call transfer to fund the attacker account be-
                                                                                      spurious alerts. SmartPoC provides a reproducible empirical signal
fore triggering the withdrawal logic, which is an instance of our
                                                                                      for comparing how often reported findings are practically verifiable.
semantic links. This example illustrates that BCE can supply the
additional code context required in real-world settings, enabling                       Answer to RQ2: SmartPoC can validate static-analysis findings
end-to-end PoCs that execute correctly.                                                 by synthesizing executable PoCs and checking their exploitabil-
   In Table 3, we order the analyzers by their average report length                    ity. Moreover, by producing reproducible, execution-grounded
and present the verification outcomes when each tool is paired                          evidence, SmartPoC helps surface limitations of existing ana-
with SmartPoC. We observe that traditional analyzers produce sub-                       lyzers, such as false positives that arise when findings are not
stantially shorter reports than LLM-based approaches. For example,                      corroborated by execution-grounded validation.
CCC’s average report length is only 11.92, whereas FT’s is about
14× longer. During manual adjudication, we find that 70.00% (14/20)
of CCC’s false positives stem from the LLM misinterpreting the                        5.4     RQ3: Performance of PoC Generation
intent of overly terse descriptions. This suggests that report quality
                                                                                      We evaluate PoC generation performance on SmartBugs-Vul and
can affect SmartPoC ’s downstream verifiability.
                                                                                      FORGE-Vul using DeepSeek-R1 (Table 4). SmartPoC outperforms
   In addition, SmartPoC provides analyzers with a reproducible,
                                                                                      the two baselines by 3.60%/1.64% and 46.76%/51.40%. We attribute
execution-grounded verification signal. For the two tools with rela-
                                                                                      the performance gap primarily to two factors relative to Iterative.
tively high NPV, namely DPO (94.23%) and FT (92.09%), we manually
                                                                                      First, the baselines differ substantially in how they process the input
analyze the sources of their false positives. We find that most false
                                                                                      code. The Iterative baseline directly feeds the full contract code into
positives stem from two factors. (i) Overly conservative security
                                                                                      the model. In contrast, SmartPoC uses BCE to expand the context
warnings or audit recommendations that lack concrete execution
                                                                                      along predefined inter-function relations, which more effectively
paths. For example, these tools may report access-control issues
                                                                                      identifies functions relevant to vulnerability triggering. This result
even when the target function is already protected by an autho-
                                                                                      suggests that structured bug-context extraction is more effective
rized modifier, or when the required checks have been performed
                                                                                      than using the full code context naively. Second, SmartPoC benefits
in upstream callers. (ii) Hallucinated reports that deviate substan-
                                                                                      from the pre-execution sanitizer in the GRE-Engine. We observe
tially from the actual contract logic. Such hallucinations are often
                                                                                      that LLMs are often insensitive to compiler-version constraints and
triggered by excessively long contract inputs or by limitations of
                                                                                      the APIs supported by each version. Such issues are difficult to
the underlying models.
                                                                                      resolve through iterative prompting alone, which highlights the
   By contrast, GPTScan attains the highest PPV and the lowest
                                                                                      necessity of our version-aware normalization and repair design.
NPV under our verification pipeline, suggesting higher precision
                                                                                      Although the rate of SmartPoC and Agentic is similar, the Agentic
and fewer spurious reports in this setting. We attribute this to
                                                                                      baseline must autonomously explore file paths and perform plan-
GPTScan’s design, which combines LLM-based reasoning with ad-
                                                                                      ning, resulting in input token costs and runtimes that are 4.96/5.35
ditional static checks as a second validation gate. Overall, these re-
                                                                                      and 14.81/15.53 times higher than those of SmartPoC, respectively.
sults suggest that LLM-based analyzers can benefit from execution-
                                                                                         We further conduct ablation studies on the major modules.
grounded validation signals to corroborate their findings and reduce
                                                                                      BCE. Removing BCE reduces the generation rate by 11.51% and
                                                                                      14.25%. Compared to the configuration that keeps only call-graph
Conference’17, July 2017, Washington, DC, USA                              Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang


expansion, SmartPoC improves the generation rate by 24.46% and             traces. More recent systems such as SmartInv [46] and Proper-
33.45%, highlighting the value of semantic expansion. The larger           tyGPT [25] use multimodal prompting and retrieval-augmented
drop on FORGE-Vul further suggests that semantic links are more            generation to synthesize candidate invariants, reducing manual
beneficial in realistic and complex projects. We also examine the          specification effort. However, these approaches remain fundamen-
reduction in token cost. With BCE, the average input length on             tally proof-centric, delivering formal proofs or counterexample
FORGE-Vul decreases from 33.67k to 16.71k tokens, correspond-              traces rather than executable PoC tests. As such, they necessitate
ing to a 50.37% reduction. On SmartBugs-Vul, it decreases from             complementary dynamic validation in realistic environments to
5.29k to 4.72k tokens, a 10.78% reduction. Overall, these results          confirm that identified violations translate to real exploitability.
indicate that BCE enables the model to focus more effectively on               Fuzzing and stateful exploration. Fuzzing-based techniques
bug-relevant code while substantially reducing token cost.                 dynamically explore smart-contract behavior and have proven ef-
GRE-Engine. Ablating the pre-execution repair drops the rate               fective at uncovering exploitable traces. Early systems such as
to 41.01% and 34.81%, indicating that without targeted version             ContractFuzzer [19], Echidna [16], and EthPloit [55] pioneered
mapping and import-path fixes, multi-round prompting alone is              ABI-/grammar-based and property-based fuzzing for Ethereum
often insufficient to produce executable PoCs. Ablating the post-          contracts. More recent work, including ItyFuzz [36], VERITE [21],
execution repair—i.e., running only a single generation round with         Midas [52], and Ethploit [55], targets deep stateful behavior and
no feedback—reduces accuracy to 17.99% and 14.25%. These results           economically exploitable traces using snapshot-based execution,
show that both the pre-execution sanitizer and the post-execution          guided seed selection, and profit-aware feedback to synthesize con-
debugger are crucial for successful PoC generation.                        crete exploit transactions. These dynamic systems rely on runtime
                                                                           signals as oracles and are highly discovery-oriented. However, they
    Answer to RQ3: SmartPoC outperforms the baselines in PoC               are driven by program code or on-chain state rather than generic
    generation. BCE and the GRE-Engine substantially increase the          static audit reports, and their oracles are often tailored to specific
    number of successfully generated PoCs by supplying precise             bug classes, limiting their applicability as general verification mech-
    context and repairing common generation and execution errors.          anisms for arbitrary static findings.
                                                                               LLM-assisted exploit and test generation. Large language
6     Threats to Validity                                                  models have been widely applied to code synthesis, including the
                                                                           generation of validation tests and exploit scripts. Some exploit-
Soundness of LLM-Based Verification. A potential threat to va-             generation approaches require specialized inputs, such as transac-
lidity arises from our use of an LLM in the DV step to insert runtime      tion histories, exploit templates, or counterexamples, and are typi-
checks, as errors in this instrumentation could affect exploitabil-        cally designed for specific exploitation settings rather than general
ity judgments. However, the LLM does not directly determine ex-            static-analysis findings [6, 8, 37, 39, 40, 47, 50, 54]. More recent stud-
ploitability; it only generates verification insertions, whereas the fi-   ies [14, 51] investigate the use of LLMs to discover vulnerabilities
nal judgment is based on concrete runtime evidence. DV is therefore        and synthesize exploits directly from source code. PoCo [2] adopts
execution-grounded rather than an LLM-as-a-judge mechanism.                an agentic loop to generate PoCs from auditor-written vulnera-
As shown in Table 1, expert adjudication yields PPVs of 98.32% on          bility annotations and iteratively refines them using compilation
SmartBugs-Vul and 98.65% on expert audit reports FORGE-Vul,                and test feedback. SmartPoC differs from these approaches in that
indicating that confirmations are highly reliable in practice. This        it targets the dynamic validation of heterogeneous static-analysis
finding also indirectly supports the reliability of the LLM-assisted       findings. Existing pipelines either depend on stronger task-specific
verification step, which is substantially more constrained than end-       inputs or emphasize PoC/exploit synthesis rather than exploitabil-
to-end PoC generation. Nevertheless, residual risk remains in edge         ity validation from raw findings. They also generally lack a generic
cases where hallucinations produce incomplete, imprecise, or se-           automated runtime oracle for determining whether exploitation
mantically misaligned checks.                                              has succeeded across diverse bug classes without manually speci-
Non-faithful PoC Generation. An LLM may generate a passing                 fied success predicates. As a result, the validation of heterogeneous
PoC by altering the target semantics rather than faithfully exploit-       static-analysis outputs remains an open practical challenge.
ing the original vulnerability. Such “cheating” behavior may include
redefining key functions, bypassing the intended execution path,
or introducing auxiliary logic that makes validation succeed for
the wrong reason. We mitigate this risk through deterministic pre-
execution sanitization, but subtle semantic deviations may still           8    Conclusion
escape our checks. Thus, while our design substantially reduces            In this work, we propose a dynamic validation approach for smart-
the risk of non-faithful validation, it cannot rule it out entirely.       contract static findings by generating executable, validated PoCs.
                                                                           We implement this approach in a tool called SmartPoC, which ad-
7     Related Work                                                         dresses noisy inputs, lack of execution grounding, and automated
Formal verification. Formal methods encode smart-contract safety           runtime verification through its BCE, GRE-Engine, and DV modules.
properties and use SMT solving, bounded model checking, or sym-            Across benchmarks and real-world contracts, SmartPoC converts
bolic execution to prove or refute them. Some works [13, 22, 29–           textual reports into validated PoCs, achieving 84.17% and 85.28%
32, 37] systematically explore transaction sequences under user-           recall rate on SmartBugs-Vul and FORGE-Vul, respectively, and
defined or built-in properties, producing proofs or counterexample         confirming 64 vulnerabilities on the latest Ethereum corpus at an
SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports                                               Conference’17, July 2017, Washington, DC, USA


average cost of $0.03 per finding. Looking ahead, we release a cu-                         [17] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu,
rated set of validated PoCs to better guide LLMs in learning and                                Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. 2025. Deepseek-r1 incen-
                                                                                                tivizes reasoning in llms through reinforcement learning. Nature 645, 8081 (2025),
generating verification code.                                                                   633–638.
                                                                                           [18] Hardhat. 2025. Ethereum Development Environment for Professionals. https:
                                                                                                //hardhat.org/.
                                                                                           [19] Bo Jiang, Ye Liu, and Wing Kwong Chan. 2018. Contractfuzzer: Fuzzing smart
9     Ethics Considerations.                                                                    contracts for vulnerability detection. In Proceedings of the 33rd ACM/IEEE inter-
All experiments were conducted in isolated environments on forked                               national conference on automated software engineering. 259–269.
                                                                                           [20] Ling Jin, Yinzhi Cao, Yan Chen, Di Zhang, and Simone Campanoni. 2022. Exgen:
mainnet snapshots. We did not interact with live contracts, hold real                           Cross-platform, automated exploit generation for smart contract vulnerabilities.
assets, or submit on-chain transactions. For the Etherscan verified-                            IEEE Transactions on Dependable and Secure Computing 20, 1 (2022), 650–664.
source corpus, we manually reviewed all findings and found no                              [21] Ziqiao Kong, Cen Zhang, Maoyi Xie, Ming Hu, Yue Xue, Ye Liu, Haijun Wang,
                                                                                                and Yang Liu. 2025. Smart Contract Fuzzing Towards Profitable Vulnerabilities.
evidence of active deployments holding exploitable tokens at the                                Proceedings of the ACM on Software Engineering 2, FSE (2025), 153–175.
time of our submission. We reported potential issues to deployers                          [22] Johannes Krupp and Christian Rossow. 2018. { teEther } : Gnawing at ethereum
                                                                                                to automatically exploit smart contracts. In 27th USENIX security symposium
via Etherscan/Blockscan Chat and withheld exploit details, PoC                                  (USENIX Security 18). 1317–1333.
code, and contract identifiers unless explicit consent is obtained.                        [23] Kaixuan Li, Yue Xue, Sen Chen, Han Liu, Kairan Sun, Ming Hu, Haijun Wang,
                                                                                                Yang Liu, and Yixiang Chen. 2024. Static application security testing (sast)
                                                                                                tools for smart contracts: How far are we? Proceedings of the ACM on Software
                                                                                                Engineering 1, FSE (2024), 1447–1470.
References                                                                                 [24] Jie Lin and David Mohaisen. 2025. From large to mammoth: A comparative
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-              evaluation of large language models in vulnerability detection. In Proceedings of
     cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal                   the 2025 Network and Distributed System Security Symposium (NDSS).
     Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774         [25] Ye Liu, Yue Xue, Daoyuan Wu, Yuqiang Sun, Yi Li, Miaolei Shi, and Yang Liu.
     (2023).                                                                                    2024. Propertygpt: Llm-driven formal verification of smart contracts through
 [2] Vivi Andersson, Sofia Bobadilla, Harald Hobbelhagen, and Martin Monperrus.                 retrieval-augmented property generation. arXiv preprint arXiv:2405.02580 (2024).
     2025. PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts.          [26] Sharon L Lohr. 2021. Sampling: design and analysis.
     arXiv preprint arXiv:2511.02780 (2025).                                               [27] Loi Luu, Duc-Hiep Chu, Hrishi Olickel, Prateek Saxena, and Aquinas Hobor.
 [3] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan,                     2016. Making smart contracts smarter. In Proceedings of the 2016 ACM SIGSAC
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda                 conference on computer and communications security. 254–269.
     Askell, et al. 2020. Language models are few-shot learners. Advances in neural        [28] Wei Ma, Daoyuan Wu, Yuqiang Sun, Tianwen Wang, Shangqing Liu, Jian Zhang,
     information processing systems 33 (2020), 1877–1901.                                       Yue Xue, and Yang Liu. 2025. Combining Fine-Tuning and LLM-Based Agents
 [4] Jiachi Chen, Yiming Shen, Jiashuo Zhang, Zihao Li, John Grundy, Zhenzhe Shao,              for Intuitive Smart Contract Auditing with Justifications. In 2025 IEEE/ACM 47th
     Yanlin Wang, Jiashui Wang, Ting Chen, and Zibin Zheng. 2025. FORGE: An                     International Conference on Software Engineering (ICSE). IEEE, 1742–1754.
     LLM-driven Framework for Large-Scale Smart Contract Vulnerability Dataset             [29] Mark Mossberg, Felipe Manzano, Eric Hennenfent, Alex Groce, Gustavo Grieco,
     Construction. arXiv:2506.18795 [cs.CR] https://arxiv.org/abs/2506.18795                    Josselin Feist, Trent Brunson, and Artem Dinaburg. 2019. Manticore: A user-
 [5] Longfei Chen, Hao Wang, Yuchen Zhou, Taiyu Wong, Jialai Wang, and Chao                     friendly symbolic execution framework for binaries and smart contracts. In 2019
     Zhang. 2025. SmartTrans: Advanced Similarity Analysis for Detecting Vulnera-               34th IEEE/ACM International Conference on Automated Software Engineering (ASE).
     bilities in Ethereum Smart Contracts. IEEE Transactions on Dependable and Secure           IEEE, 1186–1189.
     Computing (2025).                                                                     [30] Bernhard Mueller. 2018. Smashing Ethereum Smart Contracts for Fun and Real
 [6] Mojtaba Eshghie and Cyrille Artho. 2024. Oracle-guided vulnerability diversity             Profit. In Proceedings of the 9th Annual HITB Security Conference (HITBSecConf).
     and exploit synthesis of smart contracts using llms. In Proceedings of the 39th            Amsterdam, Netherlands.
     IEEE/ACM International Conference on Automated Software Engineering. 2240–            [31] Ivica Nikolić, Aashish Kolluri, Ilya Sergey, Prateek Saxena, and Aquinas Hobor.
     2248.                                                                                      2018. Finding the greedy, prodigal, and suicidal contracts at scale. In Proceedings
 [7] Etherscan. [n. d.]. Ethereum Verified Contracts | Etherscan. https://etherscan.io/         of the 34th annual computer security applications conference. 653–663.
     contractsVerified. Accessed: 2025-10-22.                                              [32] Anton Permenev, Dimitar Dimitrov, Petar Tsankov, Dana Drachsler-Cohen, and
 [8] Pengcheng Fang, Zhenhua Zou, Xusheng Xiao, and Zhuotao Liu. 2023. isyn:                    Martin Vechev. 2020. Verx: Safety verification of smart contracts. In 2020 IEEE
     Semi-automated smart contract synthesis from legal financial agreements. In                symposium on security and privacy (SP). IEEE, 1661–1677.
     Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing       [33] Michael Rodler, David Paaßen, Wenting Li, Lukas Bernhard, Thorsten Holz,
     and Analysis. 727–739.                                                                     Ghassan Karame, and Lucas Davi. 2023. EF CF: High Performance Smart Contract
 [9] Yuzhou Fang, Daoyuan Wu, Xiao Yi, Shuai Wang, Yufan Chen, Mengjie Chen,                    Fuzzing for Exploit Generation. In 2023 IEEE 8th European Symposium on Security
     Yang Liu, and Lingxiao Jiang. 2023. Beyond “protected” and “private”: An em-               and Privacy (EuroS&P). IEEE, 449–471.
     pirical security analysis of custom function modifiers in smart contracts. In         [34] Clara Schneidewind, Ilya Grishchenko, Markus Scherer, and Matteo Maffei. 2020.
     Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Test-              ethor: Practical and provably sound static analysis of ethereum smart contracts. In
     ing and Analysis. 1157–1168.                                                               Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications
[10] Josselin Feist, Gustavo Grieco, and Alex Groce. 2019. Slither: a static analysis           Security. 621–640.
     framework for smart contracts. In 2019 IEEE/ACM 2nd International Workshop on         [35] Christoph Sendner, Lukas Petzi, Jasper Stang, and Alexandra Dmitrienko. 2024.
     Emerging Trends in Software Engineering for Blockchain (WETSEB). IEEE, 8–15.               Large-scale study of vulnerability scanners for Ethereum smart contracts. In 2024
[11] João F Ferreira, Pedro Cruz, Thomas Durieux, and Rui Abreu. 2020. SmartBugs:               IEEE Symposium on Security and Privacy (SP). IEEE, 2273–2290.
     A framework to analyze solidity smart contracts. In Proceedings of the 35th           [36] Chaofan Shou, Shangyin Tan, and Koushik Sen. 2023. Ityfuzz: Snapshot-based
     IEEE/ACM International Conference on Automated Software Engineering. 1349–                 fuzzer for smart contract. In Proceedings of the 32nd ACM SIGSOFT International
     1352.                                                                                      Symposium on Software Testing and Analysis. 322–333.
[12] Foundry. 2025. Foundry - Ethereum Development Framework. https://getfoundry.          [37] Sunbeom So, Seongjoon Hong, and Hakjoo Oh. 2021. { SmarTest } : Effec-
     sh/.                                                                                       tively hunting vulnerable transaction sequences in smart contracts through
[13] Joel Frank, Cornelius Aschermann, and Thorsten Holz. 2020. { ETHBMC } : A                  language { Model-Guided } symbolic execution. In 30th USENIX Security Sympo-
     bounded model checker for smart contracts. In 29th USENIX Security Symposium               sium (USENIX Security 21). 1361–1378.
     (USENIX Security 20). 2757–2774.                                                      [38] Solidity. 2025. Style Guide – Solidity 0.8.34 - develop documentation. https:
[14] Arthur Gervais and Liyi Zhou. 2025. AI Agent Smart Contract Exploit Generation.            //docs.soliditylang.org/en/latest/style-guide.html.
     arXiv:2507.05558 [cs.CR] https://arxiv.org/abs/2507.05558                             [39] Xing Su, Hao Wu, Hanzhong Liang, Yunlin Jiang, Yuxi Cheng, Yating Liu, and
[15] Asem Ghaleb. 2022. Towards effective static analysis approaches for security vul-          Fengyuan Xu. 2026. From Transactions to Exploits: Automated PoC Synthesis
     nerabilities in smart contracts. In Proceedings of the 37th IEEE/ACM International         for Real-World DeFi Attacks. arXiv preprint arXiv:2601.16681 (2026).
     Conference on Automated Software Engineering. 1–5.                                    [40] Kairan Sun, Zhengzi Xu, Kaixuan Li, Lyuye Zhang, Yebo Feng, Daoyuan Wu, and
[16] Gustavo Grieco, Will Song, Artur Cygan, Josselin Feist, and Alex Groce. 2020.              Yang Liu. 2025. Learning from the Past: Real-World Exploit Migration for Smart
     Echidna: effective, usable, and fast fuzzing for smart contracts. In Proceedings of        Contract PoC Generation. (2025).
     the 29th ACM SIGSOFT international symposium on software testing and analysis.        [41] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Wei Ma, Lyuye Zhang, Yang Liu,
     557–560.                                                                                   and Yingjiu Li. 2024. Llm4vuln: A unified evaluation framework for decoupling
Conference’17, July 2017, Washington, DC, USA                                               Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, and Chao Zhang


     and enhancing llms’ vulnerability reasoning. arXiv preprint arXiv:2401.16185                exploit reentrancy vulnerabilities using llm and static analysis. In Proceedings of
     (2024).                                                                                     the 39th IEEE/ACM International Conference on Automated Software Engineering.
[42] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Haijun Wang, Zhengzi Xu, Xiaofei                 1019–1031.
     Xie, and Yang Liu. 2024. Gptscan: Detecting logic vulnerabilities in smart contracts   [51] Zeke Xiao, Yuekang Li, Qin Wang, and Shiping Chen. 2025. Prompt to Pwn: Au-
     by combining gpt with program analysis. In Proceedings of the IEEE/ACM 46th                 tomated Exploit Generation for Smart Contracts. arXiv preprint arXiv:2508.01371
     International Conference on Software Engineering. 1–13.                                     (2025).
[43] Petar Tsankov, Andrei Dan, Dana Drachsler-Cohen, Arthur Gervais, Florian               [52] Mingxi Ye, Xingwei Lin, Yuhong Nan, Jiajing Wu, and Zibin Zheng. 2024. Midas:
     Buenzli, and Martin Vechev. 2018. Securify: Practical security analysis of smart            Mining Profitable Exploits in On-Chain Smart Contracts via Feedback-Driven
     contracts. In Proceedings of the 2018 ACM SIGSAC conference on computer and                 Fuzzing and Differential Analysis. In Proceedings of the 33rd ACM SIGSOFT Inter-
     communications security. 67–82.                                                             national Symposium on Software Testing and Analysis. 794–805.
[44] Rajat Verma, Namrata Dhanda, and Vishal Nagar. 2022. Application of truffle suite      [53] Lei Yu, Zhirong Huang, Hang Yuan, Shiqi Cheng, Li Yang, Fengjun Zhang, Chenjie
     in a blockchain environment. In Proceedings of Third International Conference on            Shen, Jiajia Ma, Jingyuan Zhang, Junyi Lu, et al. 2025. Smart-LLaMA-DPO:
     Computing, Communications, and Cyber-Security: IC4S 2021. Springer, 693–702.                Reinforced Large Language Model for Explainable Smart Contract Vulnerability
[45] Chong Wang, Kaifeng Huang, Jian Zhang, Yebo Feng, Lyuye Zhang, Yang Liu,                    Detection. Proceedings of the ACM on Software Engineering 2, ISSTA (2025),
     and Xin Peng. 2024. Llms meet library evolution: Evaluating deprecated api                  182–205.
     usage in llm-based code completion. arXiv preprint arXiv:2406.09834 (2024).            [54] Jiashuo Zhang, Jiachi Chen, John Grundy, Jianbo Gao, Yanlin Wang, Ting Chen,
[46] Sally Junsong Wang, Kexin Pei, and Junfeng Yang. 2024. Smartinv: Multimodal                 Zhi Guan, and Zhong Chen. 2025. Automated Test Generation For Smart Con-
     learning for smart contract invariant inference. In 2024 IEEE Symposium on                  tracts via On-Chain Test Case Augmentation and Migration. In 2025 IEEE/ACM
     Security and Privacy (SP). IEEE, 2217–2235.                                                 47th International Conference on Software Engineering (ICSE). IEEE Computer
[47] Chenfeng Wei, Shiyu Cai, Yiannis Charalambous, Tong Wu, Sangharatna God-                    Society, 633–633.
     boley, and Lucas Cordeiro. 2025. VeriExploit: Automatic Bug Reproduction in            [55] Qingzhao Zhang, Yizhuo Wang, Juanru Li, and Siqi Ma. 2020. Ethploit: From
     Smart Contracts via LLMs and Formal Methods. In 40th IEEE/ACM International                 fuzzing to efficient exploit generation against smart contracts. In 2020 IEEE
     Conference on Automated Software Engineering (ASE 2025). IEEE.                              27th International Conference on Software Analysis, Evolution and Reengineering
[48] Zhiyuan Wei, Jing Sun, Zijian Zhang, Xianhao Zhang, Meng Li, and Mauro                      (SANER). IEEE, 116–126.
     Conti. 2024. FTSmartAudit: A Knowledge Distillation-Enhanced Framework for             [56] Zhuo Zhang, Brian Zhang, Wen Xu, and Zhiqiang Lin. 2023. Demystifying ex-
     Automated Smart Contract Auditing Using Fine-Tuned LLMs. arXiv preprint                     ploitable bugs in smart contracts. In 2023 IEEE/ACM 45th International Conference
     arXiv:2410.13918 (2024).                                                                    on Software Engineering (ICSE). IEEE, 615–627.
[49] Konrad Weiss, Christof Ferreira Torres, and Florian Wendland. 2024. Analyz-            [57] Liyi Zhou, Xihan Xiong, Jens Ernstberger, Stefanos Chaliasos, Zhipeng Wang, Ye
     ing the Impact of Copying-and-Pasting Vulnerable Solidity Code Snippets from                Wang, Kaihua Qin, Roger Wattenhofer, Dawn Song, and Arthur Gervais. 2023.
     Question-and-Answer Websites. In Proceedings of the 2024 ACM on Internet Mea-               Sok: Decentralized finance (defi) attacks. In 2023 IEEE Symposium on Security and
     surement Conference. 713–730.                                                               Privacy (SP). IEEE, 2444–2461.
[50] Yin Wu, Xiaofei Xie, Chenyang Peng, Dijun Liu, Hao Wu, Ming Fan, Ting Liu,
     and Haijun Wang. 2024. Advscanner: Generating adversarial smart contracts to
