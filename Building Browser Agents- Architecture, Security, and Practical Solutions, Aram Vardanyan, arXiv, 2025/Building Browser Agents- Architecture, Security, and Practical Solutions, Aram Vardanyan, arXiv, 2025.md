# **Building Browser Agents: Architecture, Security, and Practical Solutions**

**Aram Vardanyan** Founder, FillApp aram@fillapp.ai

**Browser agents enable autonomous web interaction but face critical reliability and security challenges in production. This paper presents findings from building and operating a production browser agent. The analysis examines where current approaches fail and what prevents safe autonomous operation. The fundamental insight: model capability does not limit agent performance; architectural decisions determine success or failure. Security analysis of real-world incidents reveals prompt injection attacks make general-purpose autonomous operation fundamentally unsafe. The paper argues against developing general browsing intelligence in favor of specialized tools with programmatic constraints, where safety boundaries are enforced through code instead of large language model (LLM) reasoning. Through hybrid context management combining accessibility tree snapshots with selective vision, comprehensive browser tooling matching human interaction capabilities, and intelligent prompt engineering, the agent achieved approximately 85% success rate on the WebGames benchmark across 53 diverse challenges (compared to approximately 50% reported for prior browser agents and 95.7% human baseline).**

# **1. Introduction**

Browser agents powered by LLMs automate interaction with web interfaces. Several AI-native browsers and web-agent frameworks report strong performance on selected benchmarks [\(Koh et al.,](#page-29-0) [2024;](#page-29-0) [Xie](#page-29-1) [et al.,](#page-29-1) [2024\)](#page-29-1) and show multi-step workflows such as shopping or travel planning. However, as Section [2](#page-1-0) discusses, these systems provide limited evidence about safe and reliable production operation.

A gap exists between demonstration and production operation. Findings from building and operating a production browser agent reveal that LLM capability is not the limiting factor in widespread adoption. Modern LLMs have sufficient reasoning ability to navigate web tasks effectively when provided with appropriate context and tools. The fundamental challenges are architectural: how the system manages context, what information the agent accesses, how safety boundaries are enforced, and whether to target generalization or specialization.

These challenges reflect a fundamental mismatch. The web was designed for humans, beings with vision, spatial awareness, selective attention, and the ability to process dynamic content including animations, videos, and layered interfaces. Current browser agents can replicate many human interactions such as clicks, typing, and scrolling. However, they struggle with aspects that are straightforward for humans: understanding visual hierarchy, processing time-dependent information, maintaining relevant context while discarding noise, and operating safely in environments where a single wrong action can cause irreversible damage.

This paper presents findings from production experience, not laboratory benchmarks. The insights come from observing where agents succeed, where they fail, and what architectural patterns separate reliable systems from demonstrations.

Among these challenges, security represents the most immediate barrier to autonomous operation. As Section [2.3](#page-2-0) details, public security analyses of AI-native browsers and browser extensions demonstrate that prompt injection attacks remain effective even after multiple rounds of mitigation [\(Cohen,](#page-28-0) [2025;](#page-28-0) [Shapira et al.,](#page-29-2) [2025\)](#page-29-2). Studies consistently show non-trivial attack success rates in scenarios where agents have access to sensitive user data across multiple domains. When an agent operates with full user privileges across banking, email, and corporate systems, even a 1% vulnerability rate represents unacceptable risk.

Reliable, safe browser agents require better architectural decisions instead of better LLMs. Production experience reveals four insights: context management determines success, architecture matters more than LLM scale, security requires programmatic constraints over LLM-based judgments, and specialization outperforms general-purpose approaches. Each insight challenges conventional assumptions about autonomous web agents.

The remainder of this paper examines each of these dimensions in detail, drawing from production experience to provide actionable guidance for building browser agents that are both capable and safe enough for real-world deployment.

# <span id="page-1-0"></span>**2. Background & Related Work**

# **2.1. AI browsers and computer-use APIs**

A new class of AI browsers integrates large language models (LLMs) directly into the browsing experience. OpenAI's ChatGPT Atlas, launched in October 2025, embeds ChatGPT as a browser sidebar with an optional Agent Mode capable of performing autonomous tasks such as trip planning or shopping over the user's tabs [\(OpenAI,](#page-29-3) [2025\)](#page-29-3). Perplexity Comet, announced in July 2025, functions as an AI browser that automates research, email triage, and other workflows from within the interface [\(Perplexity AI,](#page-29-4) [2025\)](#page-29-4).

Anthropic's computer use capability extends Claude models with tools to control a desktop environment and browser, separate from standalone AI browsers. The initial release in October 2024 exposed tools such as click, type, and navigate, with a focus on security mitigations and permission prompts [\(Anthropic,](#page-28-1) [2024b\)](#page-28-1). Anthropic later introduced Claude for Chrome, a browser extension that brings this automation into existing sessions. Early reports highlighted productivity benefits and documented remaining prompt injection vulnerabilities [\(Anthropic,](#page-28-2) [2024a\)](#page-28-2).

Several open-source frameworks target this problem space. WebVoyager introduces a multimodal browser agent that combines page screenshots with text to complete tasks on real websites, achieving approximately 59% task success on the WebVoyager benchmark [\(He et al.,](#page-29-5) [2024\)](#page-29-5). The Browser Use framework builds on this work and reports 89.1% success rate on the same benchmark across 586 tasks [\(Browser Use Team,](#page-28-3) [2024\)](#page-28-3). These systems show that LLM-driven browser agents can reach high success rates on static benchmarks, but provide limited visibility into production reliability, long-running workflows, and operational safety at scale.

#### **2.2. Browser automation MCPs and accessibility-based agents**

The Model Context Protocol (MCP) ecosystem now includes standardized servers for browser automation. Microsoft's Playwright MCP exposes a headless browser controlled via accessibility tree snapshots instead of raw screenshots. This approach provides the LLM with a structured view of roles, labels, and focusable elements, mapping these to executable actions [\(Microsoft,](#page-29-6) [2024\)](#page-29-6). Chrome DevTools MCP provides access to the Chrome DevTools protocol, including performance traces and full accessibility trees, allowing agents to operate using semantic element references instead of coordinate-based interactions [\(Model Context Protocol Team,](#page-29-7) [2024\)](#page-29-7).

These MCP servers illustrate a design pattern that decouples the perception layer (accessibility tree, page snapshots, or screenshots) from the execution layer (tool calls such as click, type, navigate, performance\_start\_trace). Accessibility-driven representations simplify element selection and enable safety policy enforcement at the tool layer. The architecture presented in this paper follows this principle but extends it with hybrid vision and accessibility context, element reference versioning, bulk actions, and domain-specific safety constraints derived from production usage.

### <span id="page-2-0"></span>**2.3. Prompt injection and agent security**

Prompt injection represents the central security concern for tool-using agents. Systematic evaluations across multiple models and attack patterns have demonstrated high success rates, highlighting the need for defense-in-depth approaches [\(Liu et al.,](#page-29-8) [2024\)](#page-29-8).

Regarding AI browsers, Brave's security team demonstrated indirect prompt injection attacks against Perplexity Comet. Attackers hid adversarial instructions in elements invisible to the user, such as white text on white backgrounds or HTML comments. These instructions caused Comet to execute sensitive cross-site actions, including fetching one-time passwords from email or accessing banking portals, when the user asked it to "summarize this page" [\(Sampayo and Brave Security Team,](#page-29-9) [2025\)](#page-29-9). Later analyses by security vendors confirmed that such AI browsers bypass traditional browser security boundaries like the same-origin policy by executing cross-domain actions on behalf of the user.

Defenses that rely on detecting attacks, such as filtering suspicious inputs or attempting to separate user instructions from untrusted content, typically reduce the probability of attack success without eliminating attack classes. For agents with high-impact privileges such as email, banking, and corporate SaaS, even minimal failure rates remain unacceptable.

# **2.4. Position of this work**

Most prior work on browser agents and AI browsers has focused on benchmark performance (Web-Voyager, leaderboards) or security analysis in controlled environments. These studies decouple utility and safety from production constraints including latency budgets, cost, and complex user behavior.

This paper contributes an additional perspective by reporting on the year-long production operation of a browser agent used on real-life workflows, with full access to authenticated web sessions. The analysis focuses on architectural decisions that enable production usability: hybrid accessibility and vision context representations, execution-layer and tool design, memory management and intelligent context trimming strategies, and programmatic safety boundaries that enforce specialization. It combines production observations into patterns and constraints to inform the design of future AI browsers and secure agent architectures.

# **3. The Human-AI Gap**

The web was designed around human perception and motor control, not browser agents that act through structured representations and discrete actions. Humans combine vision, spatial awareness, selective attention, and continuous pointer control to navigate complex web pages. They track loading indicators, animated transitions, hover effects, and integrate these with working memory about the task goal. Sound signals state changes through notification tones, error chimes, and video audio.

Modern browser agents perceive pages through screenshots or structured representations of DOM elements and control the browser through discrete tool calls instead of continuous motion or direct audio interaction. They issue individual tool calls such as click, type, scroll, and navigate. This execution model enables agents to complete workflows including account sign-up, profile editing, and checkout or booking flows with few steps and limited conditional logic. However, these interactions approximate only a subset of what humans do naturally when interacting with a web page.

There is a deeper gap in sensing and timing. Humans interpret videos, animations, and microinteractions such as progress bars or pulsing error states and adjust their timing based on interface responsiveness. They follow moving elements with the mouse and adapt to latency spikes or race conditions. Current browser agents typically lack integrated audio perception and can fail to align clicks with moving targets or rapidly changing layouts, leading to missed actions or incorrect states.

This gap is visible in interactive tasks that rely on real-time coordination across modalities. Drawing tools, fast-paced web games, or interfaces with rapid state changes are straightforward for humans but remain difficult for systems that operate only on occasional, static views of the page and discrete tool calls. These environments highlight how much human perception and timing still exceed current browser agents.

These differences drive specific architectural choices for production browser agents. Systems that lean only on vision-based screenshots struggle with dense interfaces and overlapping layers. Systems that rely only on structured views of page elements and relationships miss visual cues that humans use constantly, including motion, relative distance, and off-screen context. In this work, page representation and execution layer capabilities serve as central mechanisms for narrowing these human–AI gaps while staying within practical limits on latency and cost.

# **4. Context Management**

Context management determines whether browser agents remain reliable under realistic latency and token budgets. A browser agent must access enough information to understand the current page and plan actions, yet must avoid overwhelming the LLM with repetitive or irrelevant details. Poor context choices increase latency and token consumption. They also make failures more likely when the LLM loses track of relevant elements in a long conversation history.

Two design dimensions determine how browser agents manage context: how the system perceives the page and how it maintains conversation history over time. On the perception side, systems commonly choose between vision-based representations, text-based structured document representations, or hybrids that combine both. On the temporal side, the system either accumulates all intermediate snapshots and tool outputs as raw messages or compresses them aggressively into a lightweight history. Observations from production operation and evaluation on WebGames (Section [9\)](#page-23-0) support hybrid page representations paired with compressed history as a configuration that scales to long-running workflows in this architecture.

#### **4.1. Vision-based approaches**

Vision-based approaches present the agent with page screenshots and rely on the LLM's vision capabilities to identify targets and decide where to click. This representation resembles how human users perceive a web page: a visible viewport with clear spatial relationships, explicit layering, and immediate feedback on hover states, dialogs, and overlays. For simple layouts with a modest number of interactive elements, modern multimodal LLMs can reliably identify buttons, links, and form fields in a screenshot and issue corresponding click or type actions.

However, vision-only interaction exposes several limitations. Not all models support precise bounding box prediction for small or densely packed elements. Even models with built-in bounding box

interfaces frequently misidentify small targets such as calendar cells or icon grids in date pickers. Gemini 2.5 Pro and Gemini 3 Pro expose vision APIs that return bounding boxes [\(Google DeepMind,](#page-28-4) [2025\)](#page-28-4), yet still fail to place boxes reliably on dense grids of small elements. These errors accumulate on interfaces with many similar targets, where a single missed bounding box leads to repeated attempts and wasted actions.

These limitations are visible in commercial AI browsers. Atlas, for example, does not disclose its internal implementation, but testing in October 2025 showed behavior consistent with a screenshotdriven vision agent. On date picker widgets similar to those in Google Forms (Figure [1\)](#page-4-0), the agent frequently failed to select the correct day, sometimes requiring several minutes of repeated attempts on a simple calendar interaction. The challenge in these cases is that vision models must place a bounding box precisely over a specific 24px cell in a tightly packed grid, a task that current vision models handle unreliably.

<span id="page-4-0"></span>Another problem with screenshot-based interaction is that it works only with HTML elements for which the browser maintains bounding boxes. Parts of the web such as Google Sheets, Figma, and Canva operate primarily on HTML5 canvas, which does not expose individual interactive elements to the DOM or accessibility APIs.

![](_page_4_Figure_4.jpeg)

Figure 1 | **Date picker examples with dense clickable elements.** Typical date picker interfaces where each date cell is only 24px, creating challenges for vision-based approaches to accurately identify and click specific dates.

To reduce reliance on model-driven bounding boxes, some systems overlay annotation layers on top of screenshots. The execution layer first parses the DOM, computes bounding boxes for clickable elements, and renders those boxes on the screenshot with numeric labels. The LLM then refers to element references such as "click 5", and the execution layer maps the chosen number back to the underlying DOM node.

![](_page_5_Figure_1.jpeg)

Figure 2 | **Annotated screenshot approach for simple interfaces.** Clickable elements are labeled with numbers, allowing the LLM to reference them directly (for example, "click button 5"). This works well when there are relatively few clickable elements.

This annotation-based approach works well when there are only a handful of interactive elements. However, dense layouts make annotation unreliable. When a page contains hundreds of clickable elements, such as a date picker where each 24px cell is clickable, the overlay becomes cluttered and labels overlap, making the screenshot effectively unreadable to the LLM.

![](_page_6_Figure_1.jpeg)

Figure 3 | **Annotation approach fails with dense interfaces.** When attempting to annotate a date picker with many small clickable elements (24px each), the overlay becomes cluttered and confusing, making it difficult for the LLM to understand and reference specific elements.

#### **4.2. Text-based structured representations**

An alternative to vision is to send the LLM a text-based representation of the page structure. The most straightforward approach is to extract the page's DOM and pass it directly to the LLM. For simple pages with minimal markup, this can work: the LLM receives a tree of HTML elements, identifies interactive controls, and issues tool calls referencing those elements.

However, raw DOM quickly becomes impractical for realistic web applications. Modern pages contain deeply nested containers, styling hooks, decorative elements, and verbose ARIA attributes that obscure the semantic structure. For complex forms, it may take more than 100 lines of HTML to describe a single logical field, with multiple wrapper divs and accessibility annotations scattered across the markup. A simple text input labeled "Total Weight (kg)" can require over 100 lines of nested HTML elements (Figure [4\)](#page-7-0), making it difficult for the LLM to identify the label, control, and validation message.

```
<div jscontroller =" sWGJ4b " jsaction =" EEvAHc : yfX9oc ;" class =" geS5n Jj6Lae ">
  <div class =" z12JJ ">
    <div class =" M4DNQ ">
       <div
         id="i23 "
         class =" HoXoMd D1wxyf RjsPE "
         role =" heading "
         aria - level ="3"
         aria - describedby ="i27 "
       >
         <span class =" M7eMe "> Total Weight ( kg ) </ span >
         <span class =" vnumgf " id="i27 " aria - label =" Required question "> * </
             span >
       </div >
       <div class =" gubaDc OIC90c RjsPE " id="i24 "> </div >
    </ div >
  </div >
  <div jscontroller =" oCiKKc " class =" AgroKb ">
    <div class =" rFrNMe k3kHxc RdH0ib yqQS1 zKHdkd " jscontroller =" pxq3x ">
       <div class =" aCsJod oJeWuf ">
         <div class =" aXBtI Wic03c ">
           <div class =" Xb9hP ">
              <input
                type =" text "
                class =" whsOnd zHQkBf "
                autocomplete ="off "
                tabindex ="0"
                aria - labelledby ="i23 i26 "
                aria - describedby ="i24 i25 "
                required =""
                dir=" auto "
              / >
              <div class =" ndJi5d snByac " aria - hidden =" true "> Your answer </div
                  >
           </ div >
           <! -- ... multiple wrapper divs ... -->
         </div >
       </div >
    </ div >
  </div >
  <div id="i25 " role =" alert ">
    <div class =" rRld8e ">
       <! -- ... decorative icon elements ... -->
    </ div >
    <span class =" RHiWt "> This is a required question </ span >
  </div >
</ div >
```

Figure 4 | **HTML markup for a simple form field.** A simple text input labeled "Total Weight (kg)" requires over 100 lines of complex HTML with nested divs, ARIA attributes, and decorative elements, far too verbose to pass efficiently to an LLM.

A more effective approach relies on the browser's built-in accessibility APIs. Browsers maintain an accessibility tree that represents the page in a form designed for screen readers and other assistive technologies. This tree strips away decorative markup, resolves ARIA relationships, and exposes only the semantic structure: roles, labels, descriptions, focus state, and interactive elements. Modern MCP-based tools such as Playwright MCP and Chrome DevTools MCP leverage these APIs to generate accessibility tree snapshots [\(Google Chrome Team,](#page-28-5) [2024\)](#page-28-5). Instead of forwarding verbose HTML, they request structured nodes from the accessibility tree and encode each node with its role, label, description and focus state.

The same "Total Weight (kg)" field that required over 100 lines of HTML can be represented in just a few lines of accessibility tree snapshot text, as shown below. This compact representation omits structural noise while preserving all the information needed for the agent to understand and interact with the field. Figure [5](#page-8-0) illustrates how the browser's accessibility tree provides this structured view. To type into the field, the agent issues a structured tool call referencing the element by its element reference:

```
ref =38 heading " Total Weight ( kg ) Required question " level ="3" description
   =" Required question "
ref =39 textbox " Total Weight ( kg ) Required question " description =" This is
   a required question " focusable focused required
```

<span id="page-8-0"></span>![](_page_8_Picture_4.jpeg)

Figure 5 | **Chrome's Accessibility Tree representation.** The browser's accessibility API provides a structured view of the page, exposing semantic information about elements without the verbose HTML markup.

```
type ({
  ref : 39 ,
  text : " Hello World !"
})
```

The accessibility tree snapshot makes element references explicit and stable enough for short interaction sequences. However, accessibility tree snapshots are not a universal solution. Many production web properties are not fully compliant with the Web Content Accessibility Guidelines (WCAG) [\(W3C,](#page-29-10) [2018;](#page-29-10) [WebAIM,](#page-29-11) [2024\)](#page-29-11), not because developers intentionally omit accessibility features, but because they did not invest the additional effort required to make interfaces fully accessible. Even well-known form builders and content management systems expose unlabeled buttons that control dynamic components such as date pickers or dropdowns. Others render tooltips and helper text at the end of the <body> element without semantic references linking them back to the target element, a common pattern used to work around CSS layering challenges. In these cases, the accessibility tree snapshot either hides important interactions or presents them in an order that is difficult for the LLM to interpret.

Layering further complicates snapshot-only interaction. Dialogs, overlays, and nested modals often stack multiple clickable elements on top of one another. If the snapshot does not reflect visual z-order or occlusion correctly, the agent may click background elements while a dialog is open or fail to identify which control will open a hidden dropdown or date picker. These gaps lead to designs that do not choose between screenshots and accessibility tree snapshots but rather combine them.

#### **4.3. Limitations of Grid-Based Mapping**

Grid-based coordinate mapping attempts to simplify coordinate selection by overlaying a regular grid on top of the screenshot. The agent refers to grid cells (for example, "click 4x7") instead of specifying precise pixel coordinates. Figure [6](#page-9-0) illustrates this approach on a dashboard interface. The intended benefit is to provide a coarse but stable address space that is easier for the LLM to reason about than raw bounding boxes.

<span id="page-9-0"></span>![](_page_9_Figure_4.jpeg)

Figure 6 | **Grid-based coordinate mapping approach.** A screenshot overlaid with a chess-style grid system where the LLM can reference elements by grid coordinates (for example, "click 4x7"). While this simplifies coordinate communication, it becomes problematic with dense interfaces or small clickable elements.

In practice, grid-based mapping performs poorly on the same cases that break pure vision. Small clickable elements require either extremely fine grids or multiple grid levels, both of which increase complexity. To reliably click 24px buttons, the grid must become so dense that labels and cell boundaries cover the underlying interface. The agent then reasons about approximate positions instead of concrete elements and frequently misses the intended targets. The overlay also hides text, icons, and micro-interactions that are important for understanding the page. After experimentation, this approach was abandoned in favor of architectures that treat screenshots as a supporting signal instead of the primary interaction surface.

#### **4.4. Hybrid vision and accessibility context**

This architecture benefits from combining accessibility tree snapshots with selective vision as paired approaches. Accessibility tree snapshots provide a compact, semantic view of the page: labels, roles, focus state, and validation messages. Vision adds the ability to see non-DOM content, verify spatial relationships, and interpret elements rendered on canvas or images. Together, they allow the agent to plan actions using a structured representation and use vision when that structure is missing or misleading.

From a performance perspective, accessibility tree snapshots are effective at giving the agent global context in a single request. An agent can see navigation, forms, dialogs, and error messages across the entire page without scrolling, and can plan a batch of tool calls that operate on multiple fields at once. This capability connects directly to the bulk action patterns in Section [5:](#page-10-0) while a human scrolls and clicks through each field sequentially, the agent can fill dozens of inputs or toggle multiple controls in a single bulk action. Vision supplements this by handling elements that never appear in the accessibility tree snapshot, such as charts, canvas-based editors, and game interfaces.

In this architecture, the execution layer automatically provides a fresh accessibility tree snapshot after each interaction, keeping the primary LLM synchronized with the current page state. When the agent encounters elements that are not exposed in the accessibility tree snapshot or require visual understanding, it can invoke the take\_screenshot tool. For cases that require precise element identification within visual content, the agent can delegate to a separate vision model with bounding box detection capabilities (such as Gemini 2.5 Pro[\(Google DeepMind,](#page-28-4) [2025\)](#page-28-4)). This vision model receives the screenshot, identifies clickable regions with their coordinates, and returns a structured representation similar to an accessibility tree snapshot (for example, ref=5 "14 November"). The primary LLM then interacts with these elements using the same ref-based tool calls it uses for accessibility tree elements. This delegation pattern keeps most interactions fast by operating on text-based snapshots, while still providing a fallback for visually rendered content that lacks semantic structure.

Hybrid designs also enable stronger safety boundaries. When agents operate primarily through accessibility tree snapshots, the execution layer can restrict actions based on semantic information: for example, by blocking clicks on elements whose labels include "refund" or "delete" unless explicit confirmation is present. Coordinate-based clicking provides few such guarantees. By defaulting to accessibility-based actions and using vision as a secondary signal for supplementary context, the system can apply programmatic constraints that are difficult to enforce when the agent interacts through coordinates alone.

<span id="page-10-0"></span>Context management for browser agents spans both page perception and temporal memory. Pure vision approaches resemble how humans see the web but struggle with dense layouts, canvas-based applications, and safety. Pure accessibility tree snapshots provide compact, semantic representations but rely on WCAG-compliant markup and can miss dynamic behaviors or visual cues. Grid-based coordinate mapping offers little benefit in practice and complicates dense interfaces. Production experience, combined with evaluation results in Section [9,](#page-23-0) supports a hybrid approach in which accessibility tree snapshots form the primary context for planning and tool calls, and vision is used selectively for non-accessible or highly visual tasks.

# **5. Execution Layer**

The execution layer links the large language model's reasoning and the browser's DOM. While the context management layer perceives the page state, the execution layer translates the agent's intent into concrete browser actions. This component must handle the complexity of modern web applications, where dynamic content, layout shifts, and state changes frequently desynchronize the agent's mental model from the actual page state.

# **5.1. Element Reference System**

A fundamental challenge in browser automation is establishing a reliable reference system between the LLM and the DOM elements. While humans interact visually, browser agents often rely on structured text representations. The system must provide a mechanism for the LLM to reference specific elements in its tool calls.

The standard approach involves generating unique identifiers (refs) for interactive elements within the accessibility tree snapshot. The execution layer maintains a mapping between these generated refs and the actual DOM nodes.

```
const buttons = document . querySelectorAll ('button ') ;
const refMap = new Map () ;
buttons . forEach (( button , index ) = > {
  const ref = ' btn_$ { index } ';
  refMap . set ( ref , button ) ;
}) ;
/* The agent references the element by its generated ref */
const element = refMap . get ('btn_0 ') ;
element . click () ;
```

Figure 7 | **Element reference mapping.** The execution layer assigns unique identifiers to DOM elements, allowing the LLM to target actions without needing complex CSS selectors.

#### *5.1.1. State Divergence and Versioning*

A critical issue with this reference system is state divergence. Modern web interfaces are highly dynamic; a "Cancel" button with ref=10 in one snapshot might be replaced by a "Delete" button with the same ref in a subsequent render, or the element might simply disappear. If the agent operates on stale references, it risks executing unintended actions.

To address this, the system employs snapshot versioning. Each element reference includes a version identifier (e.g., 1:10, where 1 is the snapshot version and 10 is the element ref). When the execution layer receives a tool call, it verifies that the requested version matches the current state. If the versions mismatch, the action fails safely, preventing interaction with incorrect elements.

<span id="page-11-0"></span>Alternative approaches involve generating globally unique, multi-character IDs for every element across all snapshots. While this eliminates collision risks, it increases token consumption. The versioned integer approach offers a balance between safety and token efficiency.

#### **5.2. Tool Definitions**

The browser agent interacts with the web page through a defined set of tools. These primitives cover the range of human browser interactions, from basic clicks to complex state management.

# *5.2.1. Interaction Tools*

click(ref, doubleClick?, rightClick?, holdMs?): Performs a click action on the specified element. While standard clicks make up the majority of interactions, the tool supports doubleclicks and right-clicks to handle context menus and specialized interfaces, although these are less frequent in standard web navigation.

type(ref, text, shouldClear?): Enters text into input fields. Optionally can clear existing content before typing.

hover(ref): Triggers hover states, which is essential for revealing dropdown menus, tooltips, and other on-hover UI elements.

press\_key(key): Simulates keyboard events. This tool is useful for accessibility-first interfaces and failure recovery. When standard element interaction fails, agents often resort to keyboard navigation (e.g., Tab to focus, Enter to activate) or shortcuts (e.g., Cmd+C / Cmd+V for clipboard operations, arrow keys for document editing).

select\_option(ref, values): Selects values in standard <select> elements and accessible listboxes.

upload\_file(ref, filePaths): Handles file input interactions by attaching specified files to the form element.

drag(startRef, endRef): Executes drag-and-drop operations between two elements, necessary for kanban boards, sliders, and ordering interfaces.

pan(ref?, deltaX, deltaY): Controls viewport or container scrolling, enabling interaction with map interfaces and canvas elements.

focus(ref): Explicitly sets focus to an element and scrolls it into view, often used as a precursor to keyboard events.

#### *5.2.2. State and Navigation Tools*

wait\_for(time?, textToWait?, textGone?): Pauses execution until a condition is met. This tool is critical for handling asynchronous state changes, such as waiting for a loading spinner to disappear or a success message to appear. Proper use of waiting mechanisms allows the agent to synchronize with the application state effectively.

handle\_dialog(accept, promptText?): Manages native browser dialogs (alerts, confirms, prompts) that would otherwise block execution.

navigate(url): Loads a specific URL.

navigate\_back(): Simulates the browser's back button.

browser\_tabs(action, url?, tabId?): Manages browser tabs, including creating new tabs, switching focus, and closing tabs. This enables multi-tab workflows such as cross-referencing data between pages.

snapshot(ref?, mediaType?, startRef?, endRef?): Requests a fresh accessibility tree snap-

shot. The mediaType parameter allows the agent to request a "print" view, which can simplify content extraction by removing advertisements and navigation elements, similar to a browser's reader mode.

take\_screenshot(ref?, fullPage?): Captures a visual screenshot of the viewport or a specific element. This is primarily used when the accessibility tree snapshot is insufficient for understanding the page state.

## **5.3. Bulk Actions**

Sequential execution of actions introduces significant latency, particularly in form-filling tasks. To address this, the architecture supports bulk actions, enabling the agent to dispatch multiple actions in a single tool call. Modern LLMs can generate JSON structures representing a sequence of independent actions.

```
bulkActions ([
  { type : " type ", ref : 1 , text : " hello " } ,
  { type : " type ", ref : 2 , text : " world " } ,
  { type : " select_option ", ref : 3 , values : ["USA"] }
])
```

Figure 8 | **Bulk action structure.** Grouping independent interactions reduces network round-trips and LLM inference overhead.

This batching capability significantly improves performance for tasks that do not require intermediate verification, such as populating multiple fields in a form.

<span id="page-13-0"></span>![](_page_13_Figure_8.jpeg)

Figure 9 | **Performance comparison of bulk vs sequential action approaches on form filling.** Tested on a form with 28 fields (text inputs, dropdowns, radio buttons) using GPT-5.1. The bulk approach batches multiple field interactions into single tool calls, while the sequential approach processes each field individually. Results show the bulk approach achieves 74% fewer tool calls (10 vs 38), executes 57% faster (104.5s vs 245.1s), and consumes 41% fewer tokens (154K vs 260K total).

As demonstrated in Figure [9,](#page-13-0) the bulk action approach improves efficiency, reducing both execution time and token costs compared to sequential processing.

#### **5.4. Error Handling and Adaptation**

Browser agents frequently encounter execution failures due to stale references, obscured elements, or non-standard UI implementations. For instance, a custom dropdown might not respond to the

standard select\_option tool, requiring the agent to simulate a click and a following selection.

Effective error handling requires clear feedback from the execution layer. When an action fails, the system provides a descriptive error message (e.g., "Element not clickable," "Ref detached from the DOM"). This feedback, combined with a fresh page snapshot, enables the agent to diagnose the failure and attempt a recovery strategy.

The system prompt explicitly instructs the agent to adapt its approach upon failure instead of blindly retrying the same action.

```
< failure_adaptation >
When an action fails :
1. Never retry the same action twice
2. Analyze why it failed ( error message , page state , element availability )
3. Try fundamentally different approach :
   - Different element / interaction method
   - Different tool or sequence
4. If second approach fails , reconsider the goal itself
</ failure_adaptation >
```

Figure 10 | **Failure adaptation protocol.** System instructions guide the agent to attempt alternative interaction methods when primary actions fail.

This adaptive behavior is essential for autonomous operation, allowing the agent to navigate around the inconsistencies and edge cases built into modern web interfaces.

# **6. Context & History Management**

Context management is a determining factor in the reliability and cost-efficiency of browser agents. While LLMs have the capability to process large amounts of information, the presence of irrelevant data in the context window increases latency, cost, and the probability of hallucination. A browser agent must maintain sufficient information to understand the current state and past actions while discarding noise that masks the objective.

Due to the nature of MCPs, standard implementations such as Playwright MCP and Chrome DevTools MCP retain the full conversation history, including all intermediate page snapshots. This approach results in linear growth of token consumption with each action. For example, if an accessibility tree snapshot consumes 10,000 tokens, a workflow requiring 20 actions would accumulate over 200,000 tokens in the context window. This accumulation makes long-running tasks prohibitively expensive and degrades LLM performance as the context length increases.

To address these challenges, the architecture employs a three-tiered strategy: retaining only the most recent accessibility tree snapshot, applying intelligent trimming to that snapshot, and compressing the conversation history.

#### **6.1. Snapshot Management**

The system retains only the most recent accessibility tree snapshot in the system prompt. Unlike chat-based interfaces that preserve the entire dialogue, the browser agent treats the page state as temporary. When the agent navigates to a new page or performs an action that updates the view, the previous snapshot is discarded. This approach ensures that the token consumption for the page state remains constant regardless of the task duration.

However, even a single snapshot can exceed the optimal context window for efficient reasoning. Complex e-commerce pages or dashboards often contain thousands of elements. To manage this, the system enforces a maximum snapshot size (e.g., 50,000 characters). If the raw accessibility tree exceeds this limit, it undergoes intelligent trimming.

```
ref =1000 button " Hello World "
...
[ refs 1001 -5000 trimmed ]
```

Figure 11 | **Snapshot truncation indicator.** When a snapshot is truncated, the agent receives an explicit indicator of the missing range. The snapshot tool allows the agent to request specific ranges (e.g., startRef=1001, endRef=2000) if the trimmed content is required.

#### **6.2. Intelligent Trimming**

Simple character-based truncation is insufficient because it may arbitrarily cut critical interactive elements while retaining repetitive content. To solve this, the system employs a lightweight model (e.g., Gemini 2.5 Flash Lite) to perform intelligent trimming before the snapshot reaches the primary LLM.

The process involves sending the full accessibility tree snapshot along with the current conversation history to the lightweight model. This model identifies the sections of the page that are relevant to the user's current objective and returns a list of element reference ranges to retain. The system then constructs a filtered snapshot containing only the identified ranges.

The prompt for the lightweight model instructs it to preserve all interactive elements (navigation, forms, buttons, modals) while aggressively summarizing repetitive content such as long lists of product cards. For example, in a list of 50 products, the trimmer might retain the first 5 items to establish the pattern and trim the remainder, while keeping the pagination controls visible.

```
const prompt = ' You are a snapshot analyzer for a browser agent .
Your task : Identify which parts of the accessibility tree snapshot are
   relevant
to the user ' s current request . Aggressively trim repetitive content while
preserving ALL interactive elements .
< conversation_history >
< user_request > Complete the checkout form with my shipping information </
   user_request >
< step > Navigated to checkout page , page loaded successfully </ step >
< step > Found checkout form with fields : name , email , address , city </ step >
</ conversation_history >
RULES :
- KEEP all navigation , forms , buttons , modals , dialogs
- TRIM repetitive lists to first 5 items
- Keep 30 -40 refs context around important elements
SNAPSHOT ( $ { totalRefs } refs ) :
$ { snapshot }
Return : [{ start : X , end : Y } , ...] ';
const response = await llmCall ({
  model : ' gemini -2.5 - flash - lite ' ,
  prompt
}) ;
// returns [{ start : 0 , end : 50} , { start : 200 , end : 250}]
```

Figure 12 | **Intelligent trimming logic.** A lightweight model analyzes the page structure and user intent to select relevant element ranges, significantly reducing the token load for the primary LLM.

This approach significantly reduces costs, though the magnitude of savings is directly correlated with the complexity of the target page. Larger snapshots produce greater savings, as the lightweight model filters out a higher volume of irrelevant tokens. As shown in Figure [13,](#page-17-0) using a lightweight model to filter content reduces the total cost by approximately 57% for long-running tasks on pages with 8,000-12,000 token snapshots, even accounting for the additional tool calls required if the primary agent requests missing content.

# <span id="page-17-0"></span>Figure 13 | **Intelligent Trimming Cost Analysis.** Comparison of two approaches over a 38-51 action task. Without trimming, the primary LLM receives full snapshots on every call. With intelligent trimming, a lightweight model filters the snapshot, reducing the input size for the primary LLM from 10,000 tokens to 500-1,000 tokens per step. Despite a 34% increase in tool calls due to occasional re-requests, the total cost decreases by 57%.

#### **6.3. Conversation History Compression**

To prevent the context from growing indefinitely, the system compresses the conversation history. Instead of retaining the full log of messages, tool calls, and outputs, the system summarizes completed steps into a concise log.

Each tool call includes a memory parameter, where the agent explicitly summarizes the outcome of the action and updates its internal state. This self-generated summary serves as the persistent memory for the agent. This approach was originally introduced by Browser Use [Browser Use Team](#page-28-3) [\(2024\)](#page-28-3) and has proven effective for maintaining context across long-running tasks.

```
click ({
  ref : 50 ,
  evaluation_previous_goal : " Successfully clicked submit button ",
  memory : " Form submitted , confirmation page loaded with order #12345 ",
  next_goal : " Email order number to email@example .com"
})
```

Figure 14 | **Self-correction and memory update.** The agent uses the memory parameter to document its progress, creating a compressed history log that persists across steps.

The system maintains a rolling buffer of the most recent actions (e.g., the last 40-50 steps) in their full detail, while older steps are summarized or discarded. This ensures that the agent retains immediate context for error recovery while maintaining a global view of the task progress through the compressed memory log.

```
< initial_user_request > fill the shipping form </ initial_user_request >
< step >
Successfully found the form
Form has 5 fields : name , address , city , zip , country
Fill the name field first
click ( ref =42) , type ( ref =42 , " John Doe ")
</ step >
< follow_up_user_request > use my home address </ follow_up_user_request >
< step >
Name field filled successfully
User wants home address which is 123 Main St
Fill address field next
type ( ref =45 , "123 Main St ") , type ( ref =46 , " New York ")
</ step >
```

Figure 15 | **Compressed conversation history.** The system presents a summarized log of past actions and user interactions, allowing the agent to track progress without processing the full raw history.

This compression is critical for multi-tab workflows. When an agent switches between tabs, it loses access to the previous page's snapshot. The memory field ensures that information extracted from one tab (e.g., "Order ID is 12345") is explicitly recorded and available when the agent switches to another tab to enter that data.

By combining single-snapshot retention, intelligent trimming, and history compression, the architecture maintains a stable token consumption profile. As illustrated in Figure [16,](#page-19-0) this approach prevents the linear token growth observed in naive implementations, enabling the agent to execute tasks of unlimited length within a fixed cost and latency budget.

<span id="page-19-0"></span>![](_page_19_Figure_1.jpeg)

Figure 16 | **Token consumption: Full History vs. Compressed History.** Full history retention leads to linear growth, reaching over 43,000 tokens after 15 actions. The compressed history approach stabilizes around 12,600 tokens, maintaining constant performance and cost regardless of task length.

# **7. Prompt Engineering & Optimization**

The system prompt defines the browser agent's role, capabilities, and operational rules, including its core mission, behavior patterns, failure recovery strategies, and task completion criteria. Effective prompt engineering for browser agents requires addressing the unique constraints of web automation: latency, token costs, and the need for temporal awareness.

#### **7.1. System prompt structure**

The system prompt establishes the agent's fundamental behavior. It provides critical operational context that the LLM lacks, specifically regarding the time, cost of actions and the need for persistent error recovery.

```
You are an AI browser automation agent designed to understand user
   requests
and execute them autonomously using available tools .
< agent_behavior >
- Goal - oriented : Complete tasks efficiently and persistently
- Adaptive : Try different approaches when actions fail
- Autonomous : Work independently until task completion
- Time - aware : Each tool call takes ~3 -5 s ; batch actions aggressively to
   minimize latency
</ agent_behavior >
< tools >
click : {
  ref : number - Element reference from accessibility tree snapshot
  evaluation_previous_goal : string - Assessment of last action result
  memory : string - Key progress and information for next steps
  next_goal : string - Immediate next action to take
  doubleClick ?: boolean - Perform double - click
  rightClick ?: boolean - Open context menu
}
type : {
  ref : number - Element reference to type into
  text : string - Text to enter
  ...
}
...
</ tools >
```

Figure 17 | **System prompt configuration.** The prompt explicitly defines the agent's operational constraints, including time awareness and the structure of available tools.

Time awareness is critical because LLMs lack the temporal perception that humans naturally have. The agent must understand the current time, the duration of each action, and the cumulative time spent on a task. Production observations indicate that without this context, agents often pursue inefficient, step-by-step strategies that become non-viable in time-sensitive scenarios. When provided with explicit temporal context (e.g., "Each tool call takes 3-5s"), agents optimize their execution strategy by batching actions more aggressively and prioritizing faster approaches. In timed scenarios, such as assessments or auction interfaces, this awareness allows the agent to restructure its plan to complete all necessary interactions within the deadline.

#### **7.2. Caching strategy**

Dynamic context, including the page snapshot, browser tabs, selected text, and compressed history, changes with each action. To optimize performance and cost, the system injects this context separately from the static system prompt. This separation enables effective prefix caching [\(OpenAI,](#page-29-12) [2024\)](#page-29-12), as the static portion of the prompt remains constant across requests.

An effective caching strategy orders content by change frequency, placing the most stable elements at the beginning of the context window:

- 1. **System prompt:** Static instructions that never change.
- 2. **Session context:** User locale, timezone, and custom instructions (changes per session).

- 3. **Tab state:** List of open browser tabs (changes on navigation).
- 4. **Conversation history:** Compressed log of past actions (appends each step).
- 5. **Current page snapshot:** The accessibility tree snapshot (changes every action).

The accessibility tree snapshot is positioned last as the most frequently changing component. This ordering ensures that all preceding content can be cached if it remains unchanged between requests.

#### **7.3. Cost optimization**

This caching architecture significantly reduces the operational cost of long-running workflows. For a workflow consisting of 100 requests, the cost difference is substantial. Without caching, a 20,000 token system prompt would be processed fully for every step, resulting in 2 million processed tokens (\$2.50 at GPT-5.1 rates). With caching, the system pays the full input cost only for the first request. Later requests treat the static prefix as cached input, which is typically priced at a fraction of the standard rate (e.g., \$0.13/1M tokens vs \$1.25/1M tokens for GPT-5.1). This approach results in cost reductions of approximately 89% for extended sessions, making autonomous operation economically viable.

# **8. Security & Safety**

Security remains the most significant barrier preventing browser agents from autonomous production operation. The attack surface for these systems differs fundamentally from traditional web security models. While conventional applications rely on deterministic code-level protections, browser agents operate on natural language processing, introducing vulnerabilities that cannot be mitigated through standard input validation or sandboxing alone.

# **8.1. The Fundamental Problem**

Traditional web security relies on code-level protections such as input validation, sandboxing, and the same-origin policy to isolate untrusted content. Browser agents, however, introduce a new attack vector where the vulnerability lies within the LLM's language processing capabilities. When an agent processes web content, it cannot reliably distinguish between legitimate user commands and malicious instructions embedded in the page. This phenomenon, known as prompt injection, allows attackers to override the agent's instructions by hiding commands in the text or metadata of a website or the dynamic content of trusted websites [\(Liu et al.,](#page-29-8) [2024\)](#page-29-8).

Current LLMs lack reliable solutions for this problem. Unlike SQL injection or cross-site scripting (XSS), which target strict syntax parsers, prompt injection targets the semantic reasoning layer of the LLM. As a result, purely prompt-based defenses typically fail to provide the absolute guarantees required for secure operation.

#### **8.2. Production Observations**

As detailed in Section [2.3,](#page-2-0) public security analyses of AI browsers and browser extensions show that prompt injection attacks remain highly effective despite mitigation attempts. Studies involving systems such as Perplexity Comet indicate that attackers can execute cross-domain actions, such as accessing email or banking sessions, by embedding invisible text in a web page [\(Sampayo and Brave](#page-29-9) [Security Team,](#page-29-9) [2025\)](#page-29-9).

Production experience confirms these risks. Once a browser agent receives broad tool access over a user's authenticated sessions, preventing untrusted content from triggering sensitive actions through LLM judgment alone becomes statistically unlikely. The failure rate of prompt-based defenses, even if only 1%, represents an unacceptable risk when the agent has access to financial or communication platforms.

### **8.3. Limitations of Traditional Defenses**

Standard security models for agents often rely on two approaches: permission-based controls and classifier-based detection. Both show major limitations in production:

**Permission-based controls** require the user to confirm actions or approve site access. While this provides a first line of defense, it creates "permission overload" leading users to habitually approve requests without inspection. Furthermore, users may not understand the implications of granting an agent access to a complex DOM environment where hidden elements can trigger actions.

**Classifier-based detection** employs classifier models to scan inputs for malicious patterns. While the attacker cannot directly communicate with the classifier, the classifier still processes the same untrusted web content. This means attackers can embed prompt injections that either appear safe to the classifier or exploit the classifier itself. This approach raises the bar for attackers but does not eliminate the vulnerability. For production systems handling sensitive data, layering one vulnerable model on top of another provides no reliable security boundary.

#### **8.4. Architectural Countermeasures**

Given the fundamental vulnerability of LLMs to prompt injection, secure autonomous operation requires removing security decisions from the LLM's domain. Production experience suggests that safety must be enforced through deterministic, programmatic constraints instead of probabilistic reasoning.

#### *8.4.1. Deterministic Safety Boundaries*

Safety policies should be enforced by the execution layer code, not the LLM. By using the structured nature of accessibility tree snapshots, the system can block interactions with sensitive elements based on deterministic rules.

```
const element = getElementByRef ({ ref }) ;
const sensitiveKeywords = [" refund ", " delete ", " transfer ", " password "];
// Programmatic check enforcing confirmation for sensitive actions
if ( sensitiveKeywords . some ( keyword = >
    element . text . toLowerCase () . includes ( keyword )
  ) ) {
  if (! requireConfirmation ) {
    throw new Error ( ' Action on '${ element . text }' requires explicit user
        confirmation ') ;
  }
}
```

Figure 18 | **Programmatic safety check.** The execution layer inspects the target element's properties before executing an action, enforcing safety policies that the LLM cannot override.

# *8.4.2. Domain Allowlisting*

General-purpose browsing presents an unbounded attack surface. To address this, production agents should operate under strict domain allowlisting. If an agent is designed to "extract CRM data and update Salesforce," the architecture must physically restrict network access to only the CRM domain and Salesforce. This prevents the agent from visiting attacker-controlled sites or exfiltrating data to third-party servers, regardless of any injected instructions it might encounter.

### *8.4.3. Action Restriction*

The execution layer can programmatically restrict dangerous actions. As shown in the code example above, the system blocks clicks on elements containing sensitive keywords such as "refund," "delete," "transfer," or "password" unless explicit user confirmation is provided. This ensures that even if the LLM is compromised through prompt injection, the execution layer prevents irreversible actions from being executed.

#### *8.4.4. Specialization as Defense*

The most effective defense is specialization. Instead of a single "general intelligence" agent with access to email, banking, and documents, the architecture should use specialized agents with least-privilege scopes. A "LinkedIn Researcher" agent requires access only to LinkedIn and public search, with no ability to access email or internal file systems. This compartmentalization limits the blast radius of any potential compromise. Section [9.3](#page-26-0) discusses concrete examples of specialized agent types and their operational constraints.

#### **8.5. Summary**

While browser agents offer significant productivity benefits, security fundamentals remain unsolved at the LLM level. Reducing risk by 90% is insufficient for autonomous systems handling sensitive data. Secure production operation requires applying proven software security principles, such as programmatic enforcement, least privilege, and sandboxing, to the agent architecture. Production agents must be specialized, constrained by code, and skeptical by design, relying on architectural boundaries over LLM intelligence for safety.

# <span id="page-23-0"></span>**9. Production Validation**

Taking a browser agent to production requires measuring factors beyond simple task completion: operational costs, reliability at scale, and the safety of autonomous execution. While previous sections addressed architecture and security mechanisms, this section presents concrete data from production operation and benchmark evaluation.

#### **9.1. Cost Analysis**

This analysis examines real-world costs using the WebGames Shopping Challenge benchmark [\(Thomas](#page-29-13) [et al.,](#page-29-13) [2025\)](#page-29-13), specifically the "Cheapest product addition challenge." This task requires an agent to navigate multiple product pages, systematically compare prices, identify the lowest-priced items, and add them to a shopping cart. The challenge demands advanced reasoning capabilities: the agent must maintain a mental model of prices, avoid suboptimal selections, and efficiently navigate paginated listings without redundant steps.

Evaluation using GPT-5.1 on the "Cheapest product addition challenge". The agent successfully completed the multi-step price comparison and checkout workflow in 3.4 minutes with a total cost of \$0.1454. As detailed in Figure [19,](#page-24-0) caching played a major role in cost control, with nearly 75% of input tokens served from cache.

<span id="page-24-0"></span>![](_page_24_Figure_2.jpeg)

Figure 19 | **Production cost breakdown for e-commerce price comparison task.** Total cost: \$0.1454 for 30 reasoning steps, 23 tool calls, and 43 individual actions over 205 seconds. Total tokens: 268,743 (265,104 input including 198,528 cached, 3,639 output). Cost breakdown: non-cached input \$0.0832 (57.2%), output \$0.0364 (25.0%), cached input \$0.0258 (17.7%). Per-step average: \$0.0048.

Figure [20](#page-24-1) illustrates token distribution and per-step efficiency metrics. The high cache ratio (74.9% of input tokens) is typical for reasoning-heavy agents that process extensive context (page snapshots, price comparisons) but produce concise tool calls. Per-step averages indicate a predictable capacity planning baseline: 8,958 tokens, \$0.0048, and 6.8 seconds per step.

<span id="page-24-1"></span>![](_page_24_Figure_5.jpeg)

Figure 20 | **Token usage and per-step metrics.** Left: Token distribution across 268,743 total tokens. Right: Per-step averages for capacity planning: 8,958 tokens/step, \$0.0048/step, 6.8s/step.

Figure [21](#page-25-0) shows execution timing for the 23 tool calls. Execution time varies from 3.7 to 9.6 seconds (average 6.8s). The workflow structure reveals optimization: early steps perform sequential page navigation (single clicks), while later steps use bulk actions (batching multiple actions) after the agent identifies optimal products.

<span id="page-25-0"></span>Figure 21 | **Browser action execution timeline.** Each bar represents one of 23 tool calls, color-coded by speed: green (<5.4s), blue (5.4-8.2s), orange (>8.2s). Labels show action types executed (e.g., click, 3x click, type). The 43 individual actions are distributed across these 23 calls, with some calls batching multiple actions for efficiency.

# **9.2. WebGames Benchmark Results**

Evaluation on the WebGames benchmark [\(Thomas et al.,](#page-29-13) [2025\)](#page-29-13), which contains 53 challenges designed to test web agent capabilities across perception, reasoning, planning, and tool use, provides a standardized measure of performance. The benchmark is calibrated against human performance, with human subjects achieving a 95.7% success rate.

The agent completed 45 out of 53 challenges successfully, achieving an approximately 85% success rate. For comparison, the WebGames repository reports that the best-performing browser agent tested by the benchmark authors (Gemini 2.5 Pro with the Browser Use framework) achieved approximately 50% success rate. The performance gap reflects the combination of the primary model's reasoning capabilities, comprehensive browser tooling matching human interaction capabilities (Section [5.2\)](#page-11-0), and the architectural patterns discussed in this paper.

#### *9.2.1. Failure Analysis*

Eight challenges remained incomplete, falling into three categories that highlight current technical limitations:

**Advanced vision requirements (5 challenges):** Tasks such as "Slider Symphony," "Color Harmony," and "Pixel Copy" require pixel-level spatial precision, subtle color differentiation, or exact visual pattern replication. These challenges specifically test pure vision capabilities of the model.

**Real-time interaction (2 challenges):** "Brick Buster" and "Frog Crossing" are arcade-style games requiring sub-second reaction times. Agent latency of 3-5 seconds per action makes these architecturally incompatible with current LLM inference speeds.

**Precision control (1 challenge):** "Block Stack" requires directional cursor movement with precise speed control for physics-based stacking, a modality not supported by discrete tool calls.

![](_page_26_Figure_1.jpeg)

Figure 22 | **WebGames benchmark evaluation.** (A) Performance comparison: approximately 85% success compared to 50% reported for prior browser agents and 95.7% human baseline. (B) The 8 unsuccessful challenges cluster into categories reflecting current latency and vision limitations instead of reasoning failures.

# <span id="page-26-0"></span>**9.3. Operational Autonomy and Specialization**

A central challenge in production operation is balancing autonomy with safety. Requiring user confirmation for critical actions reduces risk but limits utility. Allowing full autonomy increases efficiency but introduces the risk of unintended irreversible actions.

Analysis suggests that specialization provides the solution instead of seeking a universal level of autonomy for a general-purpose agent. By deploying specialized agents with strictly scoped capabilities, organizations can achieve high reliability and safety for specific workflows. The following sections describe three common specialization patterns observed in production systems.

#### *9.3.1. Assistant Agents*

The most restrictive architectural pattern is the **Assistant Agent**, designed for summarization, extraction, and guidance. This agent type has read-only capabilities; it lacks interaction tools (such as click or type) or the ability to open new tabs. Assistant agents can read articles, extract data, or guide a user through complex platforms like AWS without the risk of modifying infrastructure. This pattern provides high utility with minimal risk and represents the majority of current safe production operations.

#### *9.3.2. Research Agents*

**Research Agents** require navigation and interaction capabilities to navigate through information. These agents typically utilize navigate, click, and type tools (often restricted to search bars). While necessary for gathering information, these capabilities introduce risks regarding prompt injection and unintended state changes.

Safety for research agents is enforced through domain allowlisting and programmatic constraints. For example, a research agent may be restricted to a specific set of domains (e.g., LinkedIn, public news sites) and prevented from executing actions on elements containing keywords like "send," "post," or "delete." This allows the agent to navigate and read content while preventing it from interacting with social features or messaging systems.

# *9.3.3. Data Entry Agents*

**Data Entry Agents** are scoped to operate within a specific tab or workflow, often without the ability to navigate away from the target domain. These agents are permitted to enter data into specific forms but are restricted from other interactions. By limiting the agent's scope to a single context, the attack surface for prompt injection or hallucination is significantly reduced.

#### **9.4. Domain-Specific Configuration**

Beyond architectural specialization, production reliability improves through domain-specific configuration. This involves dynamically injecting operational rules or modifying the context based on the active domain.

One common pattern is dynamic prompt construction. When the agent enters a specific environment, such as Google Docs, the system appends a domain-specific instruction block to the system prompt. This block might detail best practices for that application, such as using keyboard shortcuts instead of UI buttons or using the search\_replace tool instead of manual editing.

A second pattern involves snapshot filtering for security. If an agent requires access to a platform like LinkedIn for recruiting but should not access personal messages, the execution layer can pre-process the accessibility tree snapshot to remove containers matching the "Messaging" or "inbox" selectors. This ensures that the sensitive data never reaches the LLM's context window, providing a guarantee that even a compromised LLM cannot leak private conversations.

#### **9.5. Summary**

Results confirm that browser agents can operate economically and reliably when architected correctly. The WebGames benchmark results show that current LLMs, supported by comprehensive tooling and context management, can achieve success rates approaching human performance on standard web tasks. However, the path to safe autonomous operation lies not in unrestricted general intelligence but in specialization, where architectural constraints and domain-specific configurations define the safety boundaries that LLMs alone cannot guarantee.

# **10. Conclusion**

This paper demonstrates that production-ready browser agents require a fundamental architectural shift from general-purpose assistants to specialized tools. While current research often prioritizes universal web agents capable of performing any task, production experience reveals that reliability and safety result from architectural constraints instead of LLM scale.

Specialization provides a practical path for production operation that general-purpose systems struggle to replicate. Research agents do not require email capabilities; data entry agents do not require broad navigation privileges. By limiting agents to specific domains and actions through code as opposed to LLM judgment, reliability and security improve. This specialization enables autonomous operation by defining clear boundaries within which the agent can operate safely.

Browser agents perceive the web differently than humans. While humans process information sequentially through a viewport, requiring time to scroll and comprehend, agents process entire page structures instantly. This capability, when applied through hybrid accessibility and vision architectures, enables agents to operate with broader context awareness than human users. Future web standards may evolve to support this interaction mode with semantic annotations specifically designed for agents, similar to how ARIA attributes currently support assistive technologies.

However, security remains an evolving challenge. More intelligent and faster LLMs will certainly improve how browser agents operate, but prompt injection attacks will likely follow a cat-andmouse pattern similar to phishing attacks on humans. Even highly intelligent humans fall victim to sophisticated phishing attempts; after training, they adapt and recognize those patterns until new, more creative attacks emerge. The same dynamic will apply to browser agents, new attack vectors will be discovered, mitigations will be developed, and the cycle continues. This ongoing security evolution reinforces why specialized agents with programmatic constraints are essential.

The critical question addresses how to architect systems that are useful yet safe. Internal evaluation on the WebGames benchmark demonstrates an approximately 85% success rate across 53 challenges, compared to approximately 50% reported for prior approaches. These results validate that architectural decisions, specifically regarding context management, execution layer design, and specialization, significantly impact reliability.

Browser agents offer productivity benefits when designed as purpose-built tools. The technology for autonomous operation exists today; the limiting factor is architecture, not LLM capability. The path forward lies in specialization.

# **Acknowledgments**

The production insights and benchmark results presented in this paper are derived from the author's work developing FillApp, a browser agent platform.

# **References**

<span id="page-28-2"></span>Anthropic. Claude for chrome: Browser automation extension, 2024a. URL [https://chrome.](https://chrome.google.com/webstore/detail/claude-for-chrome) [google.com/webstore/detail/claude-for-chrome](https://chrome.google.com/webstore/detail/claude-for-chrome).

<span id="page-28-1"></span>Anthropic. Introducing computer use: A new capability for claude, October 2024b. URL [https:](https://www.anthropic.com/news/computer-use) [//www.anthropic.com/news/computer-use](https://www.anthropic.com/news/computer-use).

<span id="page-28-3"></span>Browser Use Team. Browser use: Make websites accessible for ai agents. [https://github.com/](https://github.com/browser-use/browser-use) [browser-use/browser-use](https://github.com/browser-use/browser-use), 2024.

<span id="page-28-0"></span>A. Cohen. In-browser llm-guided fuzzing for real-time prompt injection testing in agentic ai browsers. *arXiv preprint arXiv:2510.13543*, 2025.

<span id="page-28-5"></span>Google Chrome Team. Chrome devtools protocol: Accessibility domain. Technical report, Google, 2024. URL [https://chromedevtools.github.io/devtools-protocol/tot/](https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/) [Accessibility/](https://chromedevtools.github.io/devtools-protocol/tot/Accessibility/).

<span id="page-28-4"></span>Google DeepMind. Gemini api: Vision, 2025. URL [https://ai.google.dev/gemini-api/docs/](https://ai.google.dev/gemini-api/docs/vision) [vision](https://ai.google.dev/gemini-api/docs/vision).

- <span id="page-29-5"></span>H. He, W. Yao, K. Ma, W. Yu, Y. Dai, H. Zhang, Z. Lan, and D. Yu. Webvoyager: Building an end-to-end web agent with large multimodal models. *arXiv preprint arXiv:2401.13919*, 2024.
- <span id="page-29-0"></span>J. Y. Koh, R. Lo, L. Jang, V. Duvvur, M. C. Lim, P.-Y. Huang, G. Neubig, S. Zhou, R. Salakhutdinov, and D. Fried. Visualwebarena: Evaluating multimodal agents on realistic visual web tasks. *arXiv preprint arXiv:2401.13649*, 2024.
- <span id="page-29-8"></span>Y. Liu, Y. Deng, and D. Song. Prompt injection attacks and defenses in llm-integrated applications: A comprehensive review. *arXiv preprint arXiv:2310.12815*, 2024.
- <span id="page-29-6"></span>Microsoft. Playwright mcp: Model context protocol server for browser automation. [https://github.](https://github.com/microsoft/playwright-mcp) [com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp), 2024.
- <span id="page-29-7"></span>Model Context Protocol Team. Chrome devtools mcp: Model context protocol for chrome browser control. [https://github.com/modelcontextprotocol/servers/tree/main/](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools) [src/chrome-devtools](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools), 2024.
- <span id="page-29-12"></span>OpenAI. Prompt caching, 2024. URL [https://platform.openai.com/docs/guides/](https://platform.openai.com/docs/guides/prompt-caching) [prompt-caching](https://platform.openai.com/docs/guides/prompt-caching).
- <span id="page-29-3"></span>OpenAI. Chatgpt atlas: Ai-first browser with agent mode, October 2025. URL [https://openai.](https://openai.com/blog/chatgpt-atlas) [com/blog/chatgpt-atlas](https://openai.com/blog/chatgpt-atlas).
- <span id="page-29-4"></span>Perplexity AI. Introducing comet: Ai-powered browser for research and automation, July 2025. URL <https://www.perplexity.ai/blog/comet-browser>.
- <span id="page-29-9"></span>J. Sampayo and Brave Security Team. Prompt injection attacks on perplexity's ai browser comet, 2025. URL <https://brave.com/blog/comet-prompt-injection/>.
- <span id="page-29-2"></span>A. Shapira, G. Weiss, R. Bitton, E. Inbar, B. Nassi, and Y. Elovici. Mind the web: The security of web use agents. *arXiv preprint arXiv:2506.07153*, 2025.
- <span id="page-29-13"></span>G. Thomas, A. J. Chan, J. Kang, W. Wu, F. Christianos, F. Greenlee, A. Toulis, and M. Purtorab. Webgames: Challenging general-purpose web-browsing ai agents. *arXiv preprint arXiv:2502.18356*, 2025.
- <span id="page-29-10"></span>W3C. Web content accessibility guidelines (wcag) 2.1. W3c recommendation, World Wide Web Consortium, 2018. URL <https://www.w3.org/TR/WCAG21/>.
- <span id="page-29-11"></span>WebAIM. The webaim million: An annual accessibility analysis of the top 1,000,000 home pages, 2024. URL <https://webaim.org/projects/million/>.
- <span id="page-29-1"></span>T. Xie, D. Zhang, J. Chen, X. Li, S. Zhao, R. Cao, T. Gao, P. Pasupat, K. Narasimhan, P. Liang, et al. Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments. *arXiv preprint arXiv:2404.07972*, 2024.