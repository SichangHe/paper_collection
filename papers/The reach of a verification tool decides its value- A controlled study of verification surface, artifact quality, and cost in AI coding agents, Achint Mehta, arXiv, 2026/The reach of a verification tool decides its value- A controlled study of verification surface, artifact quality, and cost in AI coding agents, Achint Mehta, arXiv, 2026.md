The reach of a verification tool decides its
value: A controlled study of verification
surface, artifact quality, and cost in AI coding
agents
Achint Mehta



ABSTRACT Modern artificial-intelligence coding agents can be equipped with tools for checking their own
work e.g. a linter, a boot probe, a shell, a screenshot tool. We call this set the agent's verification surface. This
study asks whether increasing only that surface, with everything else held fixed, produces a matching growth
in the quality of the software the agent ships. We built a minimal coding agent whose tool list is the single
controlled variable and used it to implement 1,116 web applications across six models and eight tool
configurations. A condition-blind human graded every application against a frozen rubric, and automatic
probes stress-tested the API-observable behaviors. Verification's cheapest benefit arrives first, which is to
make sure that the application comes up. Without any tools, about one build in seven fails to launch at all and
a single boot probe removes nearly all of these failures at roughly 35 percent of a full shell's token cost, while
the full shell multiplies the no-tools cost by 2.35. Screenshots help most where mistakes are visible (e.g.
element placement, interaction), though even there the gain over a shell is modest and does not survive
correction for multiple statistical comparisons. In cases where failures can only be measured rather than seen,
such as keeping scrolling smooth over a 100,000-row list, screenshots add nothing. A verification tool
improves the output artifact only where its reach covers the way the application actually fails.

INDEX TERMS Artificial intelligence, benchmark testing, large language models, program testing,
software agents, software quality, software reliability


                     I. INTRODUCTION                                      Six models, claude-4.6-sonnet, claude-4.6-opus, claude-
                                                                       4.8-opus, gpt-5.5, gemini-3.1-pro, and grok-4.3, each
A. Goal
                                                                       implemented seven web applications under these
This study asks how the verification surface of an artificial-         configurations, four to five times per combination. We call
intelligence coding agent, the set of tools through which the          these repeats runs replicates and each replicate was an
agent can observe and check its own work, affects the quality          independent run which received no feedback from any other
of the software the agent actually ships i.e. its output files, as     run. In total, 1,116 applications were built. A human grader
opposed to the transcript of what it said while working.               then scored every application in shuffled order against a fixed
   To change only the verification surface while holding               rubric, and an automatic probing tool checked the subset of
everything else constant, we built a custom, minimal coding            behaviors observable through the API.
agent. Because the agent is ours, the system prompt is fixed,
and the only thing that changes between conditions is the list         B. Contributions
of verification tools the agent is handed. The agent ran with          1) A controlled dose-response measurement
one of five core tool sets: none at all, a linter only, a boot probe   Similar to medicine's dose-response studies, each rung of our
only, a full shell, or the shell plus screenshots (three further       verification tools ladder adds one capability and we measure
targeted configurations are described in Section II). A linter         what the increment buys. With our custom coding agent, we
reads code and flags likely mistakes without running it. The           controlled every configuration and provided tools to the model
boot probe is a single check that installs dependencies, starts        via this coding agent in an ordered ladder, with each
the application's server, and reports whether it listens. The full     configuration increasing the verification capability over the
shell is an unrestricted command line that can run anything.           last. These capabilities are: none, linter only, boot probe only,
                                                                        A. Mehta: The reach of a verification tool decides its value




full shell, and shell plus screenshots. Because we controlled        canonical demonstrations that a model can improve its own
everything else, only a single parameter changed between             output from execution feedback. These papers propose a
conditions. This lets us tie the outcomes to the tools rather than   system and present evidence that it works. Ours holds the
other uncontrollable environment parameters.                         system fixed and measures which part of the verification
2) The boot probe result                                             surface buys which kind of quality.
The boot probe tool (install dependencies and see if the server         In our own previous study [11], we examined a related
starts or not) recovered nearly all the launch failures observed     question observationally with 90 implementations of the same
with the “no tools” configuration. This single-tool                  application (a real-time retrospective board) across model
configuration gave the highest ratio of artifact quality to token    tiers, two agent harnesses, reasoning-effort levels, an
usage (tokens are the unit in which model usage is billed, so        interactive browser-testing tool, and design-oriented prompts.
token counts are our measure of cost in this study).                 Its headline findings were that reasoning effort, not tool
3) A more nuanced look into the question “does sight                 access, bought first-try reliability, and that the browser-testing
help”                                                                tool raised cost by 42 to 68 percent without improving
In our study we measure where the value of sight (the                functional score.
screenshot tool) starts and stops. The likeliest gains from sight       That study did not conclude that tools are useless. Its claim
over a shell (which allows the model to run any arbitrary            compared tools usage with reasoning effort in a much more
command) alone appear where the failures involve element             general sense. Raising effort improved reliability across every
placement or interaction. Though this visual advantage is            kind of failure at once, whereas a tool only helps with the
modest and does not survive correction for multiple                  failures it can actually observe, so in that study no tool
comparisons, we treat this as suggestive rather than                 configuration we tried matched what a step up in reasoning
established. The gains are smaller for static page-layout issues,    bought. The failures there were mostly environment failures,
which a model can often get right from the code alone, without       with Docker deployment failing first try in 44 percent of runs
seeing the page. Whether a section is present and roughly            and the local development setup in another 17 percent, and a
arranged is visible in the markup, while whether elements            tool that exercises the finished page cannot see either. That
collide or misalign at real sizes is not. It also seems to provide   paper noted that a tool aimed at those faults, such as a
minimal value in detecting issues that can be measured but not       container build or smoke test, could have caught them.
seen through code such as drag-and-drop that flickers, or               The present study takes up exactly that unanswered
scrolling that is not smooth.                                        question. Instead of asking whether tools can beat a better
C. Prior Work                                                        model, it focuses on the tools themselves, and which part of
                                                                     the verification surface buys which kind of quality, and at what
Prior work shows that the scaffolding around an artificial-
                                                                     cost. The earlier study varied model capability and found it
intelligence coding agent, its prompts, tools, and control loop,
                                                                     dominant. This study holds capability still, running every
strongly affects output quality [1]. Those studies compare
                                                                     model in every condition with byte-for-byte identical inputs,
whole systems against whole systems but this study changes a
                                                                     so that what remains is the effect of the tools themselves.
single part of the scaffold and measures what that part buys.
                                                                        The two studies are otherwise unrelated in practice. This
Our tasks were chosen to make the measurement possible with
                                                                     one uses an agent we built rather than existing harnesses,
some applications are API-heavy while others are visually
                                                                     seven applications rather than one, 1,116 hands-off runs rather
demanding.
                                                                     than ninety runs with a human in the loop, and hypotheses
   The design choices for this study and our test harness were
                                                                     fixed in a written analysis plan before any statistic was
also motivated by the limitations of existing studies. SWE-
                                                                     computed. No data, runs, or analyses are shared between them.
agent [2] showed that interface design alone can roughly triple
                                                                        Another set of studies [12], [13], [14], [15], [16], [17]
task resolution. Agentless [3] showed a simple pipeline
                                                                     establishes that visual and automated feedback improve
competitive with full agents at a tenth of the cost. These
                                                                     frontend generation (the frontend is the part of an application
existing works also compare complete systems by counting
                                                                     that runs in the browser and draws the page), from static
how many benchmark problems each one solves, in the pass-
                                                                     screenshot-to-code translation [16] to iterative visual
rate tradition running from HumanEval [4], SWE-bench [5],
                                                                     refinement [12], [15] and feedback-trained generation [17],
and WebGen-Bench [6]. In these studies, a problem counts as
                                                                     and we are not trying to replicate that. Our study differs in
solved only if the project's own tests pass afterward, and each
                                                                     various aspects from them. First, those studies evaluate
attempt earns one verdict, pass or fail. In our study, we hold
                                                                     visually defined tasks only, so they cannot ask when sight
most of the system constant while changing one aspect of the
                                                                     stops paying. Our selection of applications that the models
system, and our outcome is quality rather than a simple
                                                                     were asked to implement, deliberately crosses visually hard
pass/fail rate.
                                                                     tasks with applications whose correctness is fully observable
   CodeAgent [7] and the self-correction literature [8] propose
                                                                     through the APIs, and we find the visual advantage shrinks
systems in which running code and reading the results improve
                                                                     toward zero on the latter. Second, their systems grant vision
outcomes, with Reflexion [9] and Self-Debugging [10] the
                                                                     ability alongside execution, while our sight-without-shell

2
                                                                           A. Mehta: Verification helps only where it can see




condition separates the two abilities and suggests that the           completion, the agent sends it a single fixed reminder message
value can be derived from the sight ability itself. Third, their      asking it to continue or finish. The nudge is applied by a fixed
outcome is task success, while ours is a set of more granular         rule identical across conditions and only prompts the model to
criteria (startup survival, behavior under stress probes, human-      declare completion. It does not add verification ability or
judged interface correctness, cost, and variance), several of         change the artifact. In 29 of the 1,116 runs, the model went
which could have opposite effect under the same conditions.           idle without declaring completion, and a single nudge from the
   Coding with Eyes argues that GUI [13] (Graphical User              agent prompted it, after which all declared completion. In
Interface, another way of saying frontend) code requires              terms of model breakdown gpt-5.5 has 20, claude-4.6-sonnet
interaction, not just rendering, to verify. One of our runs           has 4, grok-4.3 has 3, and claude-4.8-opus has 2
exhibited exactly this. One page rendered perfectly but ended         implementations that required a single nudge to reach
up ignoring every click (Section V). This is direct                   completion.
confirmation, and it implies our passive screenshot tool gives           Basic file tools (read, write, edit, list) were available to the
a lower bound on what sight could deliver and there is scope          model in every condition. The conditions differed only in
for improvement even after provisioning the screenshot tools.         which verification tools were made available to the model on
   Finally, a related line of work evaluates agents inside            top of the basic file tools.
interactive environments such as WebArena [18] and                       The agent requested no extended-reasoning mode from any
OSWorld [19], where success depends on what the agent can             model. There were instances where the gateway included a
observe of a live browser or desktop. Those studies vary the          reasoning container in its response, but that container was
task world while keeping the agent's abilities fixed while ours       empty. Across the 1,116 published traces the gateway returned
holds the tasks fixed and varies only what the agent can              27,083 such containers, none of them carrying content. No
observe of its own work.                                              reasoning was therefore available for the agent to carry from
   The rest of this paper is organized as follows. Section II         one turn to the next, and none was sent back. Models may still
describes the agent, the seven applications, the tool conditions,     reason internally before answering, and where they do those
and the grading instruments. Section III states the six pre-          tokens are included in the totals we report, but that reasoning
specified hypotheses and the statistical plan for this study.         was never exposed to the agent and so was never available to
Section IV reports the results, Section V documents some of           carry from one turn to the next. Each turn therefore proceeds
the reasons for the applications failures, and Section VI             from that message history alone.
examines the configuration integrity and model signatures.
                                                                      B. The applications
Section VII states the limitations, and Section VIII concludes
the paper.                                                            Each application was defined as a frozen written specification
                                                                      (the spec) with an explicit “Acceptance criteria” section. The
                      II. STUDY DESIGN                                specs did not mention tools, so the same spec was valid in
                                                                      every condition. Keeping tools schema and task spec separate
A. The agent                                                          also allowed models to pick the tools based on their reasoning
For this study we created a minimal coding agent instead of           ability rather than being influenced by user instructions.
using a commercial or open-source coding agent for three                 Each spec was chosen to target a specific set of behaviors
main reasons. First, our agent is fully under our control and we      and failures, so that a particular kind of verification could
can change only the tool configuration while keeping                  plausibly prevent it.
everything else constant. Second, we could log every input and           The following specs were written as part of this study:
output, including tool calls (which, when, and how) and token         1. message-board: A minimal real-time message board
usage. We could verify whether a particular tool was called by             which requires the user should be able to post a
the model or not. Third, it allowed us to control the system               message, see the history, and see new messages
prompt and the input prompt. Existing harnesses, including                 appear live in other open windows (via server-sent
open platforms such as OpenHands [20], carry their own                     events, a standard browser mechanism for pushing
system prompts and control-loop instructions [1], which are                updates). This spec defines the calibration floor of the
difficult to hold constant across conditions and could                     study and is deliberately easy enough that most of the
contaminate the results. Our agent has one fixed base prompt,              implementations should succeed at this.
one fixed environment briefing that is identical across all runs,     2. kanban-board: A shared task board with columns and
and the task text. Nothing else reaches the model.                         draggable cards, where card ordering uses fractional
   Our agent loop is kept intentionally simple. The model                  positions that must be kept consistent under repeated
                                                                           reordering, and where two open windows must
receives the prompt and tool schemas (machine-readable
                                                                           converge to the same board state. Ordering under
descriptions of each tool that the model may call) and then
                                                                           stress and convergence are exactly the properties an
calls the tools until it declares completion of the task by calling
                                                                           API can be made to hammer and this is one of the
a special tool named finish. The model can receive at most one             applications for which the API probes were written,
nudge. If the model stops calling tools without having declared            while the feel of drag-and-drop exists only in a

2026                                                                                                                                    3
                                                                   A. Mehta: The reach of a verification tool decides its value




     browser and was verified by the human grading. This            observable only by measurement, along with the one
     spec targets ordering logic under stress, real-time            rubric item that inspects implementation mechanics
     convergence, and the feel of drag-and-drop, which              through browser DevTools (the bounded row check).
     only exists in a browser and would be hard to verify
                                                                C. The tool configurations
     from APIs.
3.   seat-booking: A ticket booking application that            The following tool configurations were created for our custom
     presents the user with a visual theater-style seat map     agent. Each of these configurations would make different tool-
     to select the seats, with temporary holds that expire,     set available to the model, except for basic file tools (read,
     all-or-nothing multi-seat acquisition, and a hard          write, edit, list) which are available in every tool
     guarantee that two users trying to book the same seat      configuration.
     cannot both win. This spec targets concurrency             1. no_verification: No tools other than the basic file
     correctness, which cannot be settled by just reading            tools are available to the model. The model must
     the source. Locking or transactional handling is itself         write everything correctly in one pass from its own
     visible in the code, but whether it addresses every             knowledge. We refer to this configuration informally
     scenario through which two simultaneous requests                as building blind. The question it answers is how
     can both succeed in booking the same seat depends on            good is pure authoring, and what breaks without any
     timing which the code does not show. The only way               feedback?
     to know is to run the application and make two             2. static: Adds a linter and a type checker (tools that
     conflicting requests race against each other. That              read code and flag likely mistakes without running it).
     racing procedure is precisely what the automated API            We refer to this configuration informally as the linter
     probes automate, condition-blind, against every                 condition. The question it answers is whether
     implementation.                                                 feedback about code without executing anything helps
4.   calendar-week-view: A week calendar whose                       at all?
     difficulty is almost entirely visual. The overlapping      3. boot_check: Adds the ability to install the declared
     events must share column width exactly while they               dependencies, attempt to start the application’s server,
     overlap, reclaim full width when they do not, and sit           and report whether it began listening. This tool does
     at pixel positions proportional to their times. The API         no other execution. We refer to this configuration
     is trivial, and a wrong implementation returns                  informally as boot check. The question it answers is
     perfectly correct data while drawing a wrong picture.           how much of a value is just knowing whether the
     This spec targets failures that only sight can catch.           application starts?
5.   metrics-dashboard: A statistics dashboard graded at        4. execution: Adds a full shell and the agent can run any
     three screen widths (phone, tablet, desktop), with a            system command in its workspace, including
     chart, a dark mode that must restyle everything                 installing packages, starting and stopping background
     dynamically, and deliberately awkward dataset (an               processes, and running both frontend (user interface
     overlong label, a seven-digit number) that requires             and the client code that runs on the user’s browser)
     careful implementation to prevent sloppy layout. This           and backend (the server side that contains the main
     spec targets a second, different family of sight-only           business logic). The question it answers is what does
     failures, so that we do not have to rely on one app for         unrestricted runtime ability buy, and what does it
     visual conclusions.                                             cost?
6.   kanban-labels-brownfield: This is the sole                 5. visual: Adds everything in the execution
     modification task (brownfield is the industry term for          configuration plus a screenshot tool that renders a
     changing existing code, as opposed to greenfield                URL in a headless browser (a browser runs invisibly,
     work that starts fresh). The agent receives an existing,        without a window) and returns the image to the
     working kanban application that it did not write, plus          model’s vision input. The question it answers is does
     a change request (add colored labels and filtering)             seeing the page add anything beyond running the
     with the constraint that nothing existing may break.            code?
     This spec targets regression safety when changing          6. visual_no_shell: Adds screenshots and an app-
     unfamiliar code, which is one of the most common                launcher abilities but does not allow arbitrary
     real-world software tasks.                                      command execution. Instead, the agent harness starts
7.   log-explorer-perf: A log viewer with over 100,000               the app and takes the screenshot. In this tool
     rows, strict latency requirements, a windowed API               configuration, the model can only look. The question
     with page size limited to 200 rows per response, and a          it answers is whether the sight ability helps and if it is
     virtualized list (the page keeps only a bounded                 the seeing or the shell underneath it?
     number of row elements in the document no matter           7. delayed_verification: This provides file tools only
     where the user scrolls). A simple but flawed                    until the model first declares it is finished. At that
     implementation could return identical-looking data              moment a shell unlocks, and the model is asked to
     and miss every criterion. This spec targets failures            verify and fix before finishing again. The question it


4
                                                                          A. Mehta: Verification helps only where it can see




       answers is how much of verification’s value is                E. Why the execution configuration does not trump the
       iterative development versus a final debugging pass?          other configurations
8.     behavioral: This adds only a run-tests tool that              A natural concern about the tool configurations above is that
       executes the project’s own test command. The model            the execution configuration provides full shell access, and a
       must write its own test suite. The question it answers        capable model could use that shell to rebuild almost all of the
       is whether self-authored testing could be a substitute        functionality in the configuration ladder such as running a
       for granted verification?
                                                                     linter, starting the application and probing it, or installing
D. Why a passive screenshot rather than browser                      browser-automation tools to take screenshots. Our study
automation                                                           design does not prevent this, and it does not need to, mainly
Our screenshot tool is built on Playwright driving headless          for two reasons. First, granted versus self-built is itself part of
Chromium, the same library that can click, type, drag, and           what we measure. The boot probe, for example, is a
resize a live page. Our agent exposed only its rendering call to     guaranteed single tool call and a model that wants the same
the model for this study. A model in the visual conditions           functionality without boot probe (boot_check) tool must
(visual and visual_no_shell) passes a URL to the agent and           instead find the entry point and manage the process itself,
receives an image in response, and nothing more. The                 which costs tokens. So, if a model rebuilds a capability, its
passivity is therefore a deliberate restriction rather than a        token count rises accordingly, and token usage is one of our
limitation of the tooling available to us.                           measured outcomes. Second, self-built sight cannot reach the
   We restricted it for three reasons. The first is isolation.       model's eyes. When the granted screenshot tool runs, the
Exposing the interaction API of playwright would have                harness attaches the captured image to the model's next
granted seeing and acting together, making the visual                message as visual input, so the model sees actual pixels. A
condition a combination of multiple abilities and making it          model that installs a browser and takes its own screenshot can
difficult to determine which half earned any gain. That is the       only open the screenshot file with its file tools, which in our
failure this study exists to avoid, and it is why visual_no_shell    harness return bytes, not vision. Outside of the two sight
exists as well, to separate seeing ability from execution ability.   conditions the model is called with no visual input at all, a
The second is measurability. Every screenshot is a single call       setting each run's manifest records as vision = false. The
with a single argument, so we can count exactly what a model         nearest substitute available to a shell-holding agent would be
chose to look at, which is what makes the attribution analysis       to compute facts about the screenshot with a script, its
of Section IV-D possible. A browser-automation session has           dimensions or its pixel colors, which yields text about the page
no such unit. Its actions could be logged and counted too, but       rather than sight and the command logs show no run attempted
every click both changes the page and shows the result, so the       even that. Only the harness can place a picture in front of the
count would mix acting with looking. And if the model                model.
chooses to drive the browser from a script, a single call can           In practice, this concern turns out to be almost entirely
hide fifty actions. Either way, we could no longer count how         moot. We searched every logged command of all 252 runs that
often the model chose to look, which is what Section IV-D            had an unrestricted shell without granted sight (the execution
needs. The third is prior evidence. Our earlier study granted        and delayed_verification conditions). One model, gemini-3.1-
this same library with its interaction capability intact and         pro, scripted a headless browser with Puppeteer in three of
found it raised cost by 42 to 68 percent without improving           those runs, using it to drive drag-and-drop and reordering
reliability, so testing the narrower channel in this study was       interactions on the kanban board but none of the scripts ever
the more informative order.                                          captured a screenshot, and no image was ever read back into
   The restriction has a real cost. Faults that only appear when     the model's input. So, in practice, no model ever gave itself
someone clicks lie outside what this channel can reach, so our       sight. The gift of sight remained ours to grant or withhold, and
visual conditions understate what sight could achieve. The           that grant is what the visual conditions measure.
boundary was not merely theoretical. One model, gemini-3.1-          F. Application and tool-configuration pairing
pro, installed its own scriptable browser in three runs to click
                                                                     The five core conditions (no_verification, static, boot_check,
elements the granted tool would not, and in 21 further runs
                                                                     execution, and visual) were run on every application. The
models stated the limit in their reasoning before working
                                                                     three       targeted        conditions        (visual_no_shell,
around it or falling back on reading the code.
                                                                     delayed_verification, and behavioral) were run only on
                                                                     specific applications (Table I), mainly to control the cost, as


                                                               TABLE I
                                             APPLICATIONS AND TOOL CONFIGURATION PAIRINGS




2026                                                                                                                                   5
                                                                       A. Mehta: The reach of a verification tool decides its value




            Application         core five         visual_no_shell        delayed_verification                           behavioral
    message-board                 Yes                  No                         No                                       No
    kanban-board                  Yes                  No                         Yes                                      No
    seat-booking                  Yes                  No                         Yes                                      Yes
    calendar-week-view            Yes                  Yes                        No                                       No
    metrics-dashboard             Yes                  Yes                        No                                       No
    kanban-labels-brownfield      Yes                  No                         No                                       No
    log-explorer-perf             Yes                  Yes                        No                                       No




running every configuration on every application and model          reports that effect, the measurement is what is at fault. The log
would have multiplied both the number of builds and the token       explorer's failures are slow scrolling and a list that stutters
cost.                                                               under a hundred thousand rows, and a still screenshot cannot
   The study contains 1,116 runs in total: 192 each in              show motion or delay. A photo of a laggy list and a photo of a
no_verification, static, boot_check, and execution. 174 runs in     smooth one look the same. Sight therefore has nothing to catch
visual, 90 in visual_no_shell, 60 in delayed_verification, and      here by construction, so if either screenshot arm were to beat
24 in behavioral.                                                   plain execution on this task, the gain could not be real, and we
   Each combination of application, condition, and model ran        would suspect our own instrument before believing it. The
four times by default, and a targeted subset ran a fifth time.      committed form of this check is the S3 contrast, visual versus
The batch reached these counts in waves rather than one step.       execution on this task and the screenshot-only arm gives a
Every combination started with one run, and repeats were            second, descriptive reading of the same control. Both come out
added while the batch was underway, guided by the token             flat or slightly negative, the reassuring outcome, reported in
costs the harness records automatically and by an early trial       Section IV-F.
scoring of roughly two dozen runs on two tasks (not included           delayed_verification exists to observe "finish first, then
in the final run), used only to check that the tasks and probes     verify it works". This needs applications whose concurrency
were behaving and later superseded by the full grading of all       makes their runtime behavior complex enough to hide
1,116 runs. The fifth run went where it could tell us something.    surprises, so it was run on the two hardest API tasks, kanban-
Some of our questions ask how often builds fail, and with four      board and seat-booking. The two visually hard tasks,
runs a real but uncommon failure can easily appear zero times,      calendar-week-view and metrics-dashboard, would not have
so a fifth run gives it one more chance to show. Two                been good candidates for since an unlocked shell still cannot
conditions had token costs that swung widely between repeats,       see the visual failure modes those specs are designed to create,
and one more run steadies their averages. The message-board         so the condition would not measure what it targets there.
was skipped since it was a simpler task and every model was            The behavioral condition was run only on seat-booking.
expected to score near perfect on it under every condition, so      The behavioral condition gives the model only one
an extra run there could reveal nothing new. Three safeguards       checking tool, a command to run its own test suite. That
keep this from tilting any comparison. Both sides of every          tool produces no feedback unless the model first writes
planned comparison received the same number of runs, the            tests, so to benefit from it at all the model must author its
analysis plan was frozen before the full condition-blind            own tests. That fits seat-booking well, so we ran the
grading began, and rerunning the entire analysis without the        condition there. Seat-booking's hard parts are its race
fifth runs leaves all six primary verdicts unchanged, so no         conditions and its hold-expiry logic, and both are exactly
finding in this paper depends on them. The exact run count for      the kind of thing a developer would normally check by
every task and condition is listed in the released statistical      writing a test, such as firing many requests at one seat and
output (Appendix F of stats-results.txt).                           asserting a single winner or letting a hold expire and
   Also, not every application was paired with each tool            asserting that the seat frees. We did not run the condition
configuration. visual_no_shell condition exists to separate         on the other tasks, for two reasons. On the calendar-week-
sight from execution. It grants the screenshot tool but no shell,   view and metrics-dashboard, the failures are about how the
so any difference from the full visual condition is the value of    page looks, and a test suite cannot judge rendered
running, and any difference from plain execution is the value       geometry, whether an event sits in the right place or an axis
of seeing. We ran it on the two visually hard tasks, the            label is clipped. On the message-board, the easy floor, we
calendar-week-view and the metrics-dashboard, where a still         chose not to spend the condition's runs where the ladder
image can catch the kind of failure that matters, such as an        already covers the same ground.
event drawn in the wrong place or an axis label that is clipped.
                                                                    G. Controlled test environment
   We also ran visual_no_shell on the log explorer, but this
time as a negative control (a case arranged so that the effect      We wanted the environment to be as controlled as possible, so
we are looking for cannot be present). If the measurement still     we took the following steps:


6
                                                                           A. Mehta: Verification helps only where it can see




•      Identical text: The base prompt template, the environment          traveled through the same single API gateway, so no
       briefing, and each task spec are identical across                  model was reached through different infrastructure
       conditions. We enforce this by fingerprinting. Each run's          than another. The exact model identifier sent with
       log records a cryptographic hash of every text component,          each request is recorded in that run's manifest,
       and we confirmed that every run reported the same hash             alongside its start and end times, step count, and
       for the prompt template, the briefing, and the task text.          token totals Every run ended with the model declaring
       The one thing that changes between runs is the workspace           completion and none was cut short by the harness or
       path. The base prompt is a template with a placeholder for         by any resource limit.
       the working directory, and each run fills in its own folder,   H. Analysis rules
       so the final prompt the model reads is the same in every       We encountered two situations in the study that required
       run except for that path. Each run records its workspace       explicit handling rules.
       path, and the fully assembled prompt is hashed into the        Situation 1: A model ignores a granted tool
       manifest as well. One could take the one published             Granting a screenshot tool, or any other tool, does not
       prompt template, fill in that run's recorded path, append      guarantee that a model will use it. Some models took zero
       the one published briefing, and hash the result and it         screenshots in the visual conditions. In these cases, we grade
       would match the run's recorded hash. Because the only          the application by the condition it was assigned, and not by the
       ingredient that changed was the workspace path, and            behavior the model exhibited. This is similar to the intention-
       every other piece came from the single published copy, a       to-treat rule from clinical medicine where a patient who never
       match proves nothing else was altered. We checked this         picks up a prescription still counts in the drug group, because
       reconstruction for all 1,116 runs.                             silently dropping such cases would bias the comparison
•      Environment briefing: The environment briefing tells           toward the runs that happened to behave.
       every model, in every condition, that the listed tools            Non-use was concentrated rather than spread. The three
       are the complete set and that dependencies declared in         Claude models invoked every granted checking tool in all 462
       the package manifests would be installed once the run          of their tool-granted runs (154 each, across the seven
       finished. We added this after a few initial test runs          conditions that grant any verification tool), while grok-4.3
       (not part of the 1,116 runs for the final study) showed
                                                                      alone accounts for 55 of the study's 100 non-use runs. It also
       that some models ignored some tools unless told they
                                                                      depended on the tool. No model ever skipped the boot probe,
       were available. The briefing is identical across all
                                                                      every delayed_verification run used the shell once it unlocked,
       runs and expresses no preference for any tool or
       configuration.                                                 and only two runs in the study (both in the execution
                                                                      condition) finished without issuing a single command. But the
•      Sampling settings: We fix temperature to 0.0 and
       top_p to 1.0 (the two settings that control randomness         linter went unused in 44 of the static condition's 192 runs (23
       in a model’s output, with temperature 0 requesting the         percent), the screenshot tool in 47 of the visual condition's 174
       most deterministic behavior available) for every               runs (27 percent) and in 3 of the 90 visual_no_shell runs, and
       model that accepts these parameters, with two                  4 of the 24 behavioral runs never once ran the test suite despite
       caveats. First, some models, notably the Claude Opus           the fact that it was their only checking tool. Models seemed to
       family and gpt-5.5, reject explicit temperature and            skip the checks they can finish without. Because every
       top_p. These models run with their provider's default          comparison is within-model, a gap measures the effect of
       sampling. This does not distort the comparison. When           granting a tool, not of using it. So a model that ignores its tool
       a model falls back to its provider's default sampling,         builds the same way with it as without it. The two sets of runs
       it uses that same default in every one of its                  (with and without the tools) come out alike, and the gap
       conditions, so the sampling setting never differs              between them shrinks no matter how useful the tool would
       between the conditions we compare. It matters that             have been. Section IV-D discusses this when attributing the
       we only ever compare a model against itself. We                sight effect.
       never read a result by placing one model next to               Situation 2: An application never starts
       another, only by placing a model's tools-on runs next          If a model delivers an application that fails to boot, it is graded
       to its own tools-off runs. Since the sampling setting is       as a failure on all rubric items. Excluding non-starting builds
       the same on both sides of that comparison, it cannot           from analysis would quietly reward the conditions that
       be mistaken for the effect of the tools. Second,               produce the most non-starting application through a selection
       temperature 0 does not guarantee identical outputs             effect. Suppose a weak condition only manages to start one
       across repeats, because providers are not perfectly            build in three. Those few that do start are not a fair sample of
       deterministic, which is why we run replicates (repeat          its work as they are its luckiest attempts and the ones where
       runs of the same model, task, and condition).
                                                                      the model happened to get enough right to boot. Drop the other
•      Provenance and budgets: The 1,116 runs that created
                                                                      two-thirds and we are averaging over this hand-picked best of
       the applications executed between June 12 and July
                                                                      its runs. On the other hand, a strong condition, where nearly
       11, 2026, and every request from every model
                                                                      everything starts, is instead averaged over almost all its builds,

2026                                                                                                                                    7
                                                                        A. Mehta: The reach of a verification tool decides its value




including the many that merely work without being excellent.         through the API. Each probe run staged a fresh copy of the
Scoring only the survivors therefore compares a weak                 application in a separate area. Copies that failed to boot were
condition's best runs against a strong condition's typical ones,     recorded as boot failures and kept their zero scores in every
and the weak condition could come out ahead. Counting every          average score calculation, for the same reason as Situation 2
non-starting build as a zero allows each condition to be judged      in Section II-H i.e. setting them aside would hide exactly the
on all the runs it was given. We also analyze startup failures       failures the study is designed to count. The rest were subjected
as a separate class of outcome.                                      to weighted API probes that sent API requests to the backend
                                                                     to stress the application in a way hostile or unlucky real usage
I. Tracking Tool usage
                                                                     would. For example, one such API probe posts a message and
Because we built the agent, every tool invocation is logged          watches two connected clients both receive it. Another kills
with its arguments, including calls the agent refused because        the process without warning, restarts it, and checks that the
the tool was not in that condition's list. From these logs we        data survived. A third fires eight simultaneous hold requests
compute per-run tool-usage counts (internally referred to as         for one theater seat and requires exactly one winner. The result
tool_uptake), such as how many times a run called the linter,        is a functional score, the percentage of automatic probe weight
the boot probe, or the screenshot tool. These counts let us          passed.
confirm that no run ever invoked a tool outside its condition's         Three applications have no API probes at all, and this is by
granted set, a check we ran over all 1,116 runs. Screenshot use      design. The calendar-week-view's and metrics-dashboard's
in the visual condition, for instance, ranged widely, from runs      difficulty is layout, and the log explorer's is measured
that never called the tool to runs that called it more than twenty   smoothness, none of which an API probe can observe. For
times.                                                               these, the human rubric score is the only grade.
J. Grading mechanism: Primary human grading,                            The two grading mechanisms, human grading and
secondary API Probes                                                 automatic probing, also cross-check each other. Every run the
Every application built during this study follows the same           machine recorded as a boot failure was examined by hand as
grading process. Because these are all web applications, the         well. The human grader either confirmed the failure or got the
primary grading instrument is human grading. We chose a              application running through a launch path its own files declare.
blinded human over an automated model judge deliberately.            A confirmed failure would then result in “fail” score on every
LLM-as-a-judge evaluation [21] scales well, but a judge              rubric item. A run that the grader could start keeps its human
model can share training lineage, and therefore correlated           grade and counts as surviving.
blind spots, with the very models under test, a human working           For survival we go one step further and we compute it twice,
against a frozen rubric keeps the measuring instrument               by two routes that share no data. The first route uses the
independent of everything being measured.                            machine's record. Did the automated grader boot the backend,
   Grading was condition-blind by procedure. Runs were               corrected by the hand audits (the ten builds whose server ran
graded in a mechanically shuffled order, fixed-seeded and            but whose page never loaded, and the few the machine could
never sorted by condition. Every scorecard carried no model          not start but a human could through a setting the app itself
or condition field and the grader did not consult a run's            declares). The second route ignores the machine entirely and
manifest or logs before scoring. Because the live run paths          reads only the human's scorecard. An app that earned any
encode the condition, this blinding was procedural rather than       points must have been running in front of the grader, so it
enforced by concealment. The regrade described below also            survived; an all-fail card counts as surviving only when the
provides a direct check where the regrade pass was                   audit note says the app came up and failed on its merits rather
mechanically concealed and each sampled run staged under an          than never coming up. Two independent routes targeting one
opaque identifier with path, task, and condition redacted. The       question agreed on all 1,116 runs. A released check,
regrade process reproduced the first-pass scores at 98.8             verify_post_merge_results.py, recomputes both routes and
percent item agreement with every survival call unchanged, so        reports any disagreement, so the survival numbers rest on
the procedural blinding measurably held.                             neither the machine nor the human alone.
   Every application has a rubric card of weighted, human-              All 1,116 human grades come from a single grader, so
scored criteria. The author worked through the 1,116 runs            we measured the stability of that instrument directly with a
running each application and scoring each rubric item as pass,       blind regrade. Four weeks after grading closed (grading
partial, or fail, with written notes wherever appropriate.           ended July 15 and re-grading ran from August 16 to August
Blinding was enforced by the setup, not left to discipline by        19, 2026) and we regraded a 10 percent sample i.e. 112 runs
grading runs in a shuffled order under opaque identifiers, with      drawn with a fixed, released seed, stratified proportionally
the model and condition fields stripped from every scorecard.        across task and condition. 18 runs whose records had been
This produced the human interface score, the one quality             re-opened during manuscript writing were excluded from
measure applied to every application in the study.                   the sampling frame, and runs that never launched remained
   We also ran automatic probes as a secondary check on the          in the re-grading sample. The samples were re-staged under
subset of applications whose target behavior was observable          fresh opaque identifiers in a new shuffled order, with model

8
                                                                         A. Mehta: Verification helps only where it can see




and condition stripped and the original scorecards out of            would mean changing the yardstick mid-study. Second, we did
view, and scored against the same rubric and                         not find these defects evenly. They surfaced only in the runs
accommodation rules. The agreement between the two                   where launch trouble forced the grader to dig, and they
passes is as follows. The per-item exact agreement 98.8              concentrate in particular models' habits, so scoring them
percent (589 of 596 weighted rubric-item comparisons),               would punish the runs we happened to catch, spare the ones
linearly weighted kappa 0.973 [22], [23], intraclass                 we did not, and land hardest on some models for no better
correlation ICC(A,1) [24], [25] 0.997 on the per-run score,          reason than where we looked. Third, a fair score needs one
and a mean absolute per-run difference of 0.52 points on             measurement applied to every run alike, and no instrument or
the 100-point scale which is "almost perfect" by the Landis-         rubric in the study checked for "the app's own declared start
Koch convention [26], despite 93 percent of item verdicts            command works from start to finish" identically for all 1,116
on launched runs being "pass," a prevalence that makes               builds. The defects are not lost. Section VI-A measures the two
chance agreement high [27]. Because a non-launching run              most common classes of launch defects mechanically, over
scores all-fail by rule, we report the launched-only split           every run, where they can be counted fairly.
alongside the pooled figures, which are as follows. 98.7
                                                                     L. Whole Application survival
percent exact agreement, weighted kappa 0.940, ICC 0.991.
Every item-level disagreement between original and                   Survival in this paper means the application as a whole comes
regrade scoring pass was between adjacent categories                 up through at least one path that its own files declare. The
(pass/partial or fail/partial) and none crossed the full             automatic boot check observes only the backend. Hand
pass/fail distance. Most importantly, the two passes agreed          grading revealed a complementary failure class, builds whose
on the survival call for all 112 runs, and no run moved              backend starts cleanly while the frontend can never render,
between a zero and a non-zero score, so the survival                 because the frontend source itself is broken (in every observed
measure of Section II-L is stable under re-measurement.              case there was a frontend file with a parse error, so no declared
However, the regrading aims to verify repeatability, not             path, dev or production, could build or serve the page).
correctness. The full protocol for regrading was written                Throughout the study we follow one pattern, whenever
before the sample for re-grading was drawn, the seeds, the           hand-grading surfaces a recurring problem. We write the
sealed sample and mapping, every second-pass card, and               observation down, turn it into a mechanical check, and re-
the agreement analysis are released in the archive under the         apply that check identically to all 1,116 runs, so a discovery
regrade folder.                                                      made on some runs never becomes a judgment applied to only
                                                                     those runs. Following that pattern, the human grader's
K. Launch accommodations and the configuration-space                 observations became a batch-wide audit. We pulled every run
rule                                                                 where the two instruments disagreed. For example, the
Some artifacts declared development launch scripts that              automatic probe had booted a run's backend successfully, yet
cannot launch their own user interface even though the               the human's scorecard had come out all fails. Each of these
application itself is sound, such as a script that starts the        runs was re-examined against the notes the human had written
frontend toolchain in a way that skips the artifact's own            while grading blind. Ten of them turned out to be genuine
configuration file, a proxy rule that intercepts requests for the    frontend launch failures, builds whose server ran but whose
application's own code, or a prebuilt bundle compiled against        page could not be brought up through any path the build itself
a port the server does not use by default.                           declares. Those ten are recorded in a released audit file
   When the human grader encountered these, the governing            (frontend-launch-audit.csv) and counted as non-survivors.
rule was that an accommodation may only select values or             Applications that render but still fail their rubric criteria
paths within the artifact's own declared configuration space         remain survivors. Not launching and launching badly are
(scripts it defines, configuration files it ships, and environment   different failures. By contrast, an application that never starts
variables its own code reads, such as setting PORT for a server      scores fail on every rubric item rather than being skipped,
that explicitly honors it) and may never add information the         again to avoid survivorship bias.
artifact does not contain. If some declared combination                 Another automatic score, architectural fidelity, checks by
renders the interface, it is then graded on its own merits and       static scan that each build used the mandated stack rather than
the configuration defect is recorded in the run's notes.             substituting another database or transport. The scan awards
   If no declared combination works, the render-dependent            eight points. Two of them are for the realtime channel, the
criteria fail. These configuration inconsistencies are genuine       stack's live-update mechanism (server-sent events) with one
model-authored defects. But the rubric has no criterion for          point for a server that sends the event stream, and one for a
launch mechanics, and we did not fold them in the other              client that listens to it. Four of the seven applications require
existing rubric items for these mainly for three reasons. First,     live updates, and every one of their builds scored a perfect 1.0.
the scorecard was written and frozen before a single run             The other three (the calendar-week-view and the metrics-
existed, and none of its items asks how the application              dashboard, and the log-explorer-perf) have no live-update
launches. Adding a launch penalty after seeing the results           requirement, so those two points cannot be earned there, and


2026                                                                                                                                 9
                                                                              A. Mehta: The reach of a verification tool decides its value




their maximum is six of eight points, 0.75, and every one of                   nothing itself. The hypothesis is that this bit is enough that
their builds reached it. No build anywhere swapped in a                        models that build blind and ship launch failures, could
forbidden substitute (such as sqlite3 for the database or                      have fixed the launch failures had they known about
websockets for the transport), so the verification tools did not               them. So, a bare report of a failed start should let them
change which technology stack models built with.                               catch and repair those failures before finishing, making
                                                                               far more builds launchable. We compare the boot_check
                       III. HYPOTHESES                                         condition against the no_verification condition on
We finalized and documented six primary hypotheses in a                        survival, across all seven applications.
written analysis plan (stats-plan.md, released in the archive),         3.     P3 - verification has a cost: Running and iterating is not
each a specific prediction about how changing the verification                 free and a full shell should consume more tokens than
surface should change an outcome. The plan was committed,                      working blind. We compare the execution condition
in writing and before any statistic was computed, which                        against the no_verification condition on token cost,
comparisons count, how each is tested, and what qualifies as                   across all seven applications.
support. One caveat that the plan itself records is that it was         4.     P4 - does sight help: On the tasks whose hard part is
finalized after grading was complete, so descriptive averages                  visual, letting the agent see a screenshot of the page it
had been seen and what was fixed before any inferential                        built should add quality beyond what a shell alone
computation is every remaining choice i.e. the tests, the                      provides. On the two visually hard tasks (the calendar-
correction, the handling rules, and the support criteria. We                   week-view and the metrics-dashboard), we compare the
therefore describe the hypotheses as pre-specified rather than                 visual condition against the execution condition on the
pre-registered in the external-registry sense. Each hypothesis                 human interface score.
is tested with one primary comparison between conditions.               5.     P5 - modifying versus writing: It is natural to expect
1. P1 - more verification helps: An agent that can run and                     verification tools to matter even more when the agent
      exercise its own code produces better working software                   changes code it did not write, because unfamiliar code is
      than one with no checking tools at all. We compare the                   easier to break. Our analysis plan did not commit to that
      execution condition against the no_verification condition                direction. It tested for a difference either way, and
      on the functional (behavioral) score, on the three API-                  recorded our expectation that the difference would be
      checkable applications (message-board, kanban-board,                     near zero. On this hypothesis, support means a confidence
      and seat-booking). The execution condition grants a shell                interval close to zero, not merely a non-significant
      and no sight, so in practice it reaches the application                  permutation p-value. We test whether the tool effect
      through the API, the server log, and the process rather                  differs between the modification task (kanban-labels-
      than the rendered page. The functional probes measure                    brownfield) and the equivalent new-build task.
      that same surface, and they measure it more severely than         6.     P6 - measurement helps where performance is the
      a human grader could, such as firing eight simultaneous                  challenge: On a task whose failures are about measured
      hold requests at one seat and requiring exactly one                      performance, such as user interface staying responsive
      winner, killing a process without warning and checking                   over a very large dataset, giving the agent a shell that can
      that data survived, and confirming that two connected                    run and measure the application should help more than
      clients both receive a message.                                          giving it no tools. On the performance task (the log-
2. P2 - the cheapest check: Even the smallest verification in                  explorer-perf, which must stay smooth over 100,000
      the ladder should change what ships. The boot probe                      rows), we compare the execution condition against the
      reports a single bit, did the server start, and repairs                  no_verification condition on the human interface score.


                                                             TABLE II
                       PRIMARY HYPOTHESES: PERMUTATION TEST RESULTS (HOLM-CORRECTED ACROSS THE FAMILY OF SIX)

 Hypothesis                Contrast                   Outcome        Effect            95% CI             perm p         Holm p              Supported

     P1           execution − no_verification        Functional      +12.26        [+7.04, +17.47]         0.0001        0.0006                Yes
     P2          boot_check − no_verification       Survival (0-1)   +0.13          [+0.10, +0.16]         0.0001        0.0006                Yes
     P3           execution − no_verification        Log tokens      +0.80          [+0.73, +0.87]         0.0001        0.0006                Yes
     P4               visual − execution               Human         +6.88         [+0.83, +13.41]         0.0413        0.0826                No
     P5       (brownfield gap) − (greenfield gap)    Functional       -0.67       [−13.67, +12.67]         0.9989        0.9989                No
     P6           execution − no_verification          Human         +15.33        [+7.33, +24.00]         0.0225        0.0675                No




10
                                                                              A. Mehta: Verification helps only where it can see




                                                                  TABLE III
                                      SECONDARY CONTRASTS: PERMUTATION TEST RESULTS (UNCORRECTED, NO HOLM)

  Hypothesis               Contrast                    Outcome                Effect                           95% CI              perm p

       S1          execution − boot_check             Functional             +2.41                          [−0.38, +5.21]         0.1427
       S2        visual_no_shell − execution            Human                +4.98                         [−1.42, +11.75]         0.1951
       S3      visual − execution (log explorer)        Human                −2.17                         [−12.50, +7.33]         0.8571
       S4a          static − no_verification          Functional             −3.60                         [−11.36, +3.61]         0.3886
       S4b          static − no_verification         Survival (0-1)          −0.02                          [−0.07, +0.03]         0.3534
       S5           behavioral − execution            Functional            −16.07                         [−31.67, −1.70]         0.0425
       S6       visual − execution, per model           Human              Per-model


The six hypotheses above (P1 to P6) are the primary contrasts.                   flat or negative result is the reassuring outcome. A
Each was decided in advance in our analysis, and together they                   benefit would point to a problem in our setup rather
form one family. We perform permutation tests on these (a                        than a real effect.
permutation test asks how often a difference as large as the              •      S4 - the linter's null result (no measurable effect) in
observed one would arise if the condition labels were shuffled                   more detail (static versus no_verification, on both
at random) [28], [29], the standard way to compare systems in                    functional score and survival). Linters are cheap and
language-processing research [30], [31], calculate permutation                   widely assumed to help, so a null is worth pinning
p-values, and then apply the Holm correction [32] across all                     down rather than asserting. This contrast measures the
six (testing six hypotheses gives chance six opportunities to                    linter's effect twice, once on behavioral quality and
produce a false positive, so Holm raises the bar accordingly).                   once on whether builds start at all. No improvement on
A primary result is called supported only if it survives that                    either would mean that granting a tool is not the same
correction. These carry the paper's main claims. Their results                   as benefiting from it.
appear in Table II.                                                       •      S5 - whether self-authored tests substitute for a granted
   The secondary contrasts are additional comparisons that                       shell (behavioral versus execution). The behavioral
decompose or probe the primary results rather than test a new                    condition's only checking tool runs tests which the
headline claim. Because they are exploratory rather than pre-                    model writes for itself (Section II-F). This sounds like
specified headline tests, we report them without the Holm                        it could deliver the shell's benefits from a much smaller
correction and read them as suggestive. They can help explain                    surface. Parity here would mean a small, targeted tool
why a primary result looks the way it does, but on their own                     can replace the full shell. A shortfall would suggest
we do not treat them as confirmatory.                                            that, under a fixed budget, building a test harness
   The secondary contrasts we report on are(results in Table                     competes with finishing the application itself.
III):                                                                     •      S6 - a per-model view of the sight effect (visual versus
   • S1 - whether a full shell adds anything beyond the                          execution, split by model). A model that is given a tool
        cheap boot probe (execution versus boot_check). The                      may never use it. And an average pooled over all the
        boot probe is the cheapest verification in the study, and                models cannot say where an improvement came from,
        the shell costs nearly three times as much, so this                      a gain from actually looking at screenshots and a gain
        contrast prices what the shell's extra functionality                     from anything else would look identical inside the
        actually buys. A large gap would justify the shell's                     average. This split places each model's gain next to
        premium. A small one would make the probe the better                     how often it actually took screenshots. If the gains
        bargain for most work.                                                   concentrate in the models that looked most, sight works
   • S2 - whether sight helps once it is separated from the                      the way it is supposed to. If they land on models that
        shell (visual_no_shell versus execution). The visual                     barely looked, the pooled benefit cannot be credited to
        condition mixes two channels, running and seeing, so                     looking.
        its gains could come from either. The visual_no_shell
        condition keeps the screenshots and removes the shell                                         IV. RESULTS
        (Section II-F). If visual_no_shell still keeps up with          This section reports what changed when we changed the
        execution on the visually hard tasks, then whatever             verification surface, and every reported number is built in two
        sight contributes, comes from the seeing itself and not         steps.
        from the shell underneath.                                         In the first step, we work within each model on each task.
   • S3 - whether sight adds anything on the log explorer,              For every model-and-task combination (say, gpt-5.5 building
        whose failures can be measured but not seen (visual             the seat-booking app), we calculate difference of averages by
        versus execution). Because a still screenshot cannot            comparing that model's runs under one condition against its
        show a lag or stutter, we predict no benefit, which             own runs under another and take the difference (for example,
        makes this contrast a negative control (Section II-F). A        its average execution score minus its own average

2026                                                                                                                                        11
                                                                      A. Mehta: The reach of a verification tool decides its value




no_verification score on that task). Differencing a model          which are two-sided and uncorrected, lead to the same
against itself in this way normalizes away that model's own        qualitative conclusions, including that P4 and P6 remain
baseline behavior, so a strong or weak model cannot distort        suggestive rather than established. The complete output is
the comparison.                                                    released as stats-mixed-effects.txt under paper/ in the
   In the second step, we combine these differences across all     repository cited in the Data and Code Availability section.
the model-and-task combinations into the single figure we                                   TABLE IV
                                                                      MIXED-EFFECTS CROSS-CHECK OF THE SIX PRIMARY CONTRASTS
report. That combination is a weighted average. Each
combination counts in proportion to how many runs it                                                                                    p (two-
                                                                   Hypothesis      Contrast        Outcome Estimate SE 95% CI
                                                                                                                                        sided)
contains, so a combination with more runs contributes more
                                                                                 execution −                           [+5.57,
and none is over or under counted. So, a statement like "the           P1
                                                                                no_verification
                                                                                                Functional +12.26 3.41
                                                                                                                       +18.95]
                                                                                                                               .0003
execution condition scored 12 points above the                                   boot_check −      Survival                     [+0.09,
                                                                       P2                                       +0.13 0.02              <.0001
no_verification condition" is a within-model, within-task                       no_verification     (0–1)                       +0.17]
difference first, and then a run-weighted average across every                   execution −         Log                        [+0.70,
                                                                       P3                                       +0.80 0.05              <.0001
model-and-task combination. The reported figures therefore                      no_verification     tokens                      +0.91]
do combine all models. They simply do so after each model                           visual −                                    [−0.57,
                                                                       P4                           Human       +6.88 3.80              .0705
                                                                                   execution                                    +14.32]
has been measured against itself, which is what keeps the
                                                                                  (brownfield
comparison fair. Where the per-model picture differs from this         P5            gap) −      Functional −0.67 7.94
                                                                                                                       [−16.24,
                                                                                                                                .9331
pooled view, we show it explicitly.                                                                                    +14.90]
                                                                                (greenfield gap)
   Before computing any statistic, we wrote an analysis plan                     execution −                                    [+1.63,
                                                                       P6                           Human      +15.33 6.99              .0283
that fixed which hypotheses we would test, how we would test                    no_verification                                 +29.04]
them, and the rules for handling awkward runs (Section III).
The tests themselves are stratified permutation tests. They ask       The full plan, the analysis code, and the complete statistical
how often a difference this large would appear if the condition    output, including per-cell means, standard deviations, and
labels were shuffled at random, with shuffling allowed only        counts, are in the released archive (stats-plan.md,
among runs of the same model and task, so that model or task       stats_analysis.py, and stats-results.txt under paper/ in the
differences are not mistaken for tool differences. Because we      repository cited in the Data and Code Availability section).
test several hypotheses, we apply the Holm correction to the          Having run the pre-specified tests, we report the findings
p-values to guard against false positives. We also computed a      below. Each subsection focuses on one question, whether
95% confidence interval for each hypothesis by stratified          about a particular tool, a particular kind of task, or the cost of
bootstrap [33], to show how large each effect is and how much      verification. Table V maps each subsection to the hypotheses
uncertainty surrounds it.                                          behind it, listing the primary contrast and any secondary ones,
   Each permutation test uses 10,000 permutations [28], [29],      to help trace every claim we make back to the specific test that
[30], [31]. The 95 percent confidence interval is calculated by    supports it.
rebuilding the dataset 5,000 times with redrawing runs at                                    TABLE V
random from within each model-task-condition cell, and                WHICH RESULTS SUBSECTION SUPPORTED BY WHICH HYPOTHESIS
watching how much the effect varies across those rebuilt                           Subsection                         Primary        Secondary
datasets (a stratified bootstrap, the interval covers the middle
                                                                    IV-A More verification, better outcomes           P1, P2         S4a, S4b
95 percent of that variation). The random seed (20260703) is                 IV-B The boot probe                    develops P2        S1
written into the released analysis code, so rerunning it                    IV-C Cost and variance                      P3
reproduces every number in this paper exactly. Alongside each              IV-D The sight boundary                      P4            S2, S3
contrast, the released output also reports a simpler cross-check        IV-E Brownfield modification                    P5
                                                                          IV-F Performance budgets                      P6
that assumes nothing about how the scores are distributed: a               IV-G Self-authored tests                                     S5
sign test, which asks whether the six per-model differences
lean in one direction more consistently than six-coin flips
plausibly would.                                                   A. More verification, better outcomes, mostly at the
   As a cross-check, we analyzed the same six contrasts again      bottom
using a completely different statistical method, a mixed-
                                                                   We measured three outcomes (survival, machine-probed
effects regression [34] (Table IV). This method fits one model
                                                                   behavior, and the human-judged interface) across the five core
per contrast. It gives each of the six models its own baseline
                                                                   conditions (which ran across all seven applications). Every
level, so that runs from the same model are not treated as
                                                                   outcome improves as verification increases, and the biggest
unrelated to one another, and it adds a term for each
                                                                   single jump comes at the very bottom of the ladder, the jump
application whenever a contrast covers more than one. The
                                                                   from no way to run anything (no_verification) to a single boot
two methods agree. Every primary-effect points in the same
                                                                   probe (boot_check).
direction and is the same size, matching the permutation
                                                                      Survival: Survival means the application as a whole comes
estimates to two decimal places. The regression p-values,
                                                                   up through at least one path its own files declare. Survival

12
                                                                                    A. Mehta: Verification helps only where it can see




                                                                                   The frontend audit adds a harder fact. The builds that had
                                                                                the linter were not even protected from the one mistake a linter
                                                                                is built to catch. Ten builds in the study shipped a frontend that
                                                                                could never render, in every case because of a parse error in a
                                                                                frontend file. Five of those ten were encountered in the static
                                                                                condition. Catching parse errors is precisely the job a linter
                                                                                exists to do, so the one condition equipped to prevent this
                                                                                failure produced half of its cases. Section V shows how that
                                                                                happens in practice, in a build whose model called the linter
                                                                                once, got an error back because it had never wired the tool up,
                                                                                and finished without ever checking again.
 FIGURE 1. Launch survival across the five core tool configurations (all
                                                                                   Functional scores on the API-probed applications:
 runs, intention-to-treat). Survival means the application as a whole,          These are the machine-verified secondary checks. They pool
 frontend included, comes up through at least one path its own files            the three fresh-build applications whose target behavior can be
 declare. The two conditions that cannot execute anything,
                                                                                tested over the API, the message-board, the kanban-board, and
 no_verification and static, lose roughly one build in six to seven. A single
 boot probe removes all but one failure in 192.                                 the seat-booking. The modification task, kanban-labels-
                                                                                brownfield, also has probes, but those are reported with its
                                                                                own comparison in Section IV-E. Mean functional score
                                                                                across the five core conditions are: no_verification 81.9, static
                                                                                78.3, boot_check 91.7, execution 94.2, and visual 92.6 (Fig.
                                                                                2).
                                                                                   Our main planned comparisons (Table II)
                                                                                1. execution versus no_verification: +12.3 points, 95
                                                                                      percent confidence interval [+7.0, +17.5], corrected p <
                                                                                      .001, and positive in five of the six models. This means
                                                                                      execution ability bought real quality and a model that
                                                                                      could run its own code shipped software that behaved
 FIGURE 2. Mean functional score on the API-probed applications, by
                                                                                      about twelve points better under our probes than the same
 condition (all runs, non-starters scored zero). The largest step is from the         model building blind. This is a gain too large and too
 no-execution arms to the boot probe, the shell arms add depth on the                 consistent to be chance.
 race, restart, and ordering probes.
                                                                                2. boot_check versus no_verification: survival effect is +13
numbers for the five core conditions, also shown in Fig. 1, are:                      percentage points, 95 percent confidence interval [+10,
no_verification 86.5 percent (166 of 192), static 84.4 percent                        +16], corrected p < .001, concentrated in the models that
(162 of 192), boot_check 99.5 percent (191 of 192), execution                         fail without the boot_check probe (gemini gains 50 points
99.0 percent (190 of 192), and visual 99.4 percent (173 of                            of survival, gpt-5.5 gains 20, and the rest were already at
174). The failures that remain are real build failures, not                           ceiling, that is, near 100 percent with no room left to
grading accidents. We re-examined and classified each of the                          improve). This means the boot_check probe's single bit of
66 failures (pooled across all conditions), and 56 of them come                       feedback i.e. does the server start, was enough to rescue
from the two conditions that cannot run anything                                      nearly all would-be launch failures, and the benefit went
(no_verification and static). Most of these failures trace to two                     exactly where it was needed, the models that already
causes.                                                                               launched reliably had nothing to gain, while the failure-
   First, there were source files that the model corrupted while                      prone ones gained the most.
editing, a botched splice that leaves the file unparseable, which                  A secondary contrast that we wanted to explore was static
any attempt to run or render the code would have caught at                      vs no_verification. The static condition effects are
once (there were 35 backend cases and all 10 of the audited                     indistinguishable from no_verification on both outcomes. The
frontend cases). Second, there were database seed scripts that                  functional observed score difference between the two
crashed the application on first boot.                                          conditions was −3.6 percentage points, 95 percent confidence
   The static condition, the one equipped with a linter and a                   interval [−11.4, +3.6]. On survival criteria the difference
type checker, did no better than having no tools at all. Its builds             between the two conditions was −2 percentage points, 95
started slightly less often and scored slightly lower on                        percent confidence interval [−7, +3].
behavior, and both differences are within statistical noise. The                   Human interface scores. Every application in the study
linter made no measurable difference, and that absence is itself                received a human interface score (Section II-J), and the
a finding, because linters are cheap, familiar, and widely                      released tables carry the ladder for all seven tasks. However,
assumed to help.                                                                as per the pre-specified hypothesis P4, we focus on the two
                                                                                tasks whose difficulty is visual and for which the rubric is the

2026                                                                                                                                            13
                                                                              A. Mehta: The reach of a verification tool decides its value




                                                                           persistence checks, and the ordering-under-load tests.
                                                                           Restricting to those probes across all four probe-bearing
                                                                           applications, counting every arm that ever held a shell
                                                                           (execution, visual, and delayed_verification) and only builds
                                                                           that started, shell condition passed 92.0 percent of that weight,
                                                                           the boot probe 91.1 percent, and the blind conditions (i.e. no
                                                                           tools or a linter only) 89.1 percent.
                                                                              The human-judged quality of the page is the only measure
                                                                           that keeps improving past the shell. On the two visually hard
                                                                           tasks it climbs from 72.8 with no tools to 89.5 with the boot
                                                                           probe, 89.2 with a shell, and 96.1 with screenshots (Fig. 3).
 FIGURE 3. Mean human-graded interface score on the two visually
                                                                           That final gain, screenshots measured against the shell, is the
 graded tasks (calendar and dashboard), by condition. The same ladder as   one result that does not survive our correction for testing six
 Figures 1 and 2 with a wider spread. Section IV-D examines how much       hypotheses at once, and Section IV-D sets out why.
 of the top step is attributable to sight.
                                                                              Taken together, the three gradings tell one story with three
only grade i.e. the calendar-week-view and the metrics-                    different endings. Every measure improves as verification
dashboard (the third rubric-only task, the perf-log-explorer,              grows, but each stops improving at a different rung of the
has its own section IV-F). On these two tasks, the human                   ladder. Survival stops first. The boot probe lifts the survival
scores repeat the pattern of the survival and functional ladders           rates from 86 to 99.5 percent and nothing above the boot probe
i.e. quality climbs as verification grows, with the largest step           moves it again, because once nearly every application starts, a
at the bottom but the gaps between conditions are wider: this              stronger tool has no launch failures left to prevent. Machine-
ladder runs from 72.6 (static) to 96.1 (visual), a spread of about         probed behavior stops next. Ten of the twelve points that
23 points, where the functional ladder spanned about 16. The               separate blind builds from shell builds also arrive with the
complete human interface scores for these two tasks are:                   probe alone, and the shell contributes only the small
no_verification 72.8, static 72.6, boot_check 89.5, execution              remainder, earned on the demanding probes that stress
89.2, and visual 96.1 (Fig. 3). In these numbers, two non-                 concurrency, restarts, and ordering. Human-judged quality is
execution conditions (no_verification and static) sit 17 points            the only measure still climbing above the shell, and that final
below everything else, the boot_check recovers most of that                gain, screenshots measured against a shell, is also the only one
gap, and the visual condition sits on top. Section IV-D                    in this section that does not survive our correction. The linter
examines how much of that top step can be credited to sight.               improves in none of the three. Each measure improves only
These values are plain averages. For each condition we take                while the added tools can still reach the defects it counts.
the mean human score across all runs, pooled over all six                     One number goes against the ladder. On the calendar-week-
models, so they show roughly where each condition landed.                  view, the boot_check condition’s human score (96.6) beats the
They are not the within-model comparisons we use to test the               full shell's (86.4), even though the shell can do everything the
hypotheses, which instead measure each model against itself.               boot_check probe can. The boot_check probe did not help
    Reading all the three ladders together (survival, functional           more but the shell's runs on this task simply swung far more
scores on the API-probed applications, and human interface                 widely (a standard deviation of 31.0 against the probe's 3.3).
scores) together shows what each step of verification buys.                Two models pulled the shell average down. grok-4.3 (48.2)
Survival improves first and improves the most. The boot probe              and claude-4.6-sonnet (74.1) shipped their worst interaction
alone lifts survival rates from 86 to 99.5 percent, a gain of 13           defects in their shell builds on this task, while their boot-probe
percentage points (Fig. 1 and the P2 row of Table II), and                 builds happened not to. Section IV-D returns to these two
nothing after the boot probe improves it further. Behavioral               models.
quality comes next, and most of its gain also arrives with the             B. The boot probe: the cheapest useful verification
boot probe.                                                                We measured how much the study's cheapest verification tool
    Of the twelve functional points that separate blind builds             helps, and what it cannot catch. The cheapest tool is the boot
from shell builds, ten arrive with the boot probe alone (Fig. 2).          probe. Its builds used the fewest tokens of any condition in the
The shell adds the last two points or so, and they appear only             study, fewer even than builds made with no tools at all
on the most demanding probes. Those are the ones that fire                 (Section IV-C lists every condition's cost). The short answer
several requests at the same instant to compete for the same               is that the probe delivers most of verification's value at that
resource, that kill the application without warning and restart            lowest price. It nearly eliminated launch failures and came
it to check the data survived, and that verify items stay in the           within a few functional points of the full shell on the easy and
right order while the app is under load. Not every probe counts            medium tasks, at roughly a third of the shell's token cost.
equally in the functional score. The automatic grader weights              Though, the probe only knows whether the server starts
each probe, and eleven probe types carry the top weights of 3              listening. It cannot see what the server answers once real
and 4, the simultaneous-request races, the kill-and-restart

14
                                                                                   A. Mehta: Verification helps only where it can see




 FIGURE 4. Median token cost against the machine-probed behavioral             FIGURE 5. Median token cost against the human-graded interface score
 score (API tasks, all conditions). Each point pools the six models, which     (all seven tasks, core conditions only, since the targeted arms ran on task
 is consistent with the within-model design because every model                subsets and would not be comparable). Machine and human judgments
 contributes to every condition equally. The boot probe sits on the            are plotted separately by design and never combined. The frontier's
 efficient frontier: cheaper than building blind and within a few points of    shape is the same under either judge.
 the shell.
                                                                              to be measured, the gap is larger, around nine points of human
requests arrive, and it cannot see the page. The section below                score on the dashboard and the log explorer.
shows the limits of boot probe. On the seat-booking's
                                                                              C. Cost and variance
demanding concurrency probes, on the metrics-dashboard's
layout, and on the log explorer's measured smoothness, the                        We measured the token cost of each condition and how
probe's builds trail the shell's every time.                                  predictable that cost is from run to run. We found that the cost
   The boot_check condition has one launch failure in the                     rises steeply as the verification surface grows, and the boot
study (191 of 192 runs came up) at 214 thousand median                        probe is the only configuration cheaper than building blind.
tokens per build (Fig. 4), against the execution condition's 615                  Median tokens per condition (all 1,116 runs) are:
thousand. Its functional score (91.7) sits within 2.5 points of               no_verification 262k, static 276k, boot_check 214k, execution
the execution condition's (94.2) on the on the three API-                     615k, visual 674k, visual_no_shell 659k, delayed_verification
checkable tasks (message-board, kanban-board, and seat-                       1,199k, and behavioral 375k. Granting a full shell (execution)
booking). Yet its boundary is crisp. "Listens" is not "works."                multiplies the no_verification baseline's cost by 2.35. Adding
The boot check probe confirms that the server came up and                     screenshots (visual) costs about a tenth more than the shell
accepts connections. It says nothing about whether anything                   (execution). visual_no_shell costs about the same as visual, so
the application does after that is correct.                                   sight without a shell is no cheaper. The declare-done-then-
   The one build the boot_probe failed to save shows the blind                discover workflow (delayed_verification) is the most
spot exactly. Its backend started and listened, so the probe was              expensive configuration in the study, at nearly double the shell
satisfied, but a parse error in a frontend file meant the page                (execution). And boot_check is the only configuration that
could never be rendered.                                                      costs less than building blind (no_verification).
   A probe that only watches the server side cannot see such a                    That last point is worth explaining, since adding a tool
failure. Two graded examples (Section V) show the same                        would normally add cost. The saving comes not from writing
boundary at request time. An SQL type error that crashes the                  less code but from re-reading less conversation. The
summary API endpoint on first call, and a permanently false                   conversation is re-sent to the model on every step, so input
error banner, both passing straight through boot probe because                tokens dominate cost, and an agent that takes fewer steps pays
it only asks whether the server started.                                      less to re-read its own session. Boot-probe runs finish in fewer
   On the two visually hard tasks (calendar-week-view and                     steps than blind runs (a median of 17 against 19) and re-read
metrics-dashboard), boot_check's human interface scores trail                 far less (195 thousand input tokens against 247 thousand)
the execution (Table VII) condition where layout is hard (82.5                while writing only somewhat less code (13.5 thousand output
versus 92.0 on the dashboard), and on the measurement task it                 tokens against 16.8 thousand). Nor is the saving an artifact of
trails by 9 points (84.8 versus 93.8). The boot probe buys                    cheap failures. Blind runs that never started cost less than blind
survival, not correctness. The secondary contrast (S1 in Table                runs that worked (182 thousand tokens against 263 thousand),
III) quantifies this boundary. On the three API-checkable                     yet comparing only builds that started, the boot probe still
application, boot_check's functional shortfall against the                    costs about 49 thousand tokens less than working blind. This
execution condition is 2.4 points in the execution condition's                is descriptive rather than tested, and it is consistent with the
favor, 95 percent interval [-0.4, +5.2]. So, on those tasks the               boot probe also having the lowest run-to-run spread in the
shell's advantage in boot_check probe measured behavior may                   study.
be nothing at all and is at most about five points, and it comes                  Now looking at the most expensive tool configuration
at 2.9 times the token cost. Where the difficulty is visual or has            (delayed_verification) most of its extra cost goes on a repair
                                                                              cycle. Once the shell unlocked, every one of the 60 runs used
                                                                              it, and 45 of the 60 went on to change their own code before

2026                                                                                                                                                     15
                                                                       A. Mehta: The reach of a verification tool decides its value




declaring completion a second time. So, most of that extra cost     weighting could reorder the conditions. Third, keeping them
is a repair cycle. The 15 builds that finished unchanged scored     separate lets a reader check that the frontier's shape does not
about seven functional points higher than the 45 that needed        depend on which judge you trust, which is itself a finding.
edits, so a model that checks its work and changes nothing is         Both figures pool the six models (the opening of Section IV
itself a mild sign of a better build.                               explains why pooling is consistent with the design). Fig. 6
   Cost is not only higher with a larger verification surface, it   draws the same frontier separately for each model, where the
is also less predictable as shown in Table VI. To measure that      same shape recurs at each model's own quality level.
unpredictability i.e. how much cost varies between runs whose
                                                                                                 TABLE VI
setup is identical, we use the repeat runs. Every model built                         MEDIAN COST SPREAD BY CONDITION
every application under every core condition four or five                                      Tasks and
times, and those repeats are identical in everything we control,                                             Median run-to-run spread
                                                                            Condition            Model
                                                                                                                  (token count)
the same prompt, the same model, and the same tools. Any                                      combinations
difference in what they cost is therefore run-to-run variation           no_verification        42 (7 × 6)             81k
                                                                              static            42 (7 × 6)             77k
rather than the result of changing something.                              boot_check           42 (7 × 6)             47k
   The calculation has two stages. In the first stage, we take a            execution           42 (7 × 6)            149k
single combination of one model, one application, and one                     visual            42 (7 × 6)            188k
                                                                       delayed_verification     12 (2 × 6)            408k
condition, list the token cost of each of its four or five repeat        visual_no_shell        18 (3 × 6)            301k
runs, and compute the standard deviation of those costs, which              behavioral          6 (1 × 6)              91k
measures how far the individual runs sat from their own             Medians in the sealed tables take the upper of the two middle values;
average. That produces one number for that combination, its         medians quoted in the running text average the two. The conventions differ
cost spread. In the second stage we take those numbers across       visibly only for the behavioral arm's total (375k vs 369k).
all the combinations belonging to a condition, 42 of them for       D. The Sight Boundary
each core condition since six models each built seven
                                                                    We measured whether screenshot access (visual) improves
applications, and report their median.
                                                                    visually graded work beyond what a shell (execution) already
   The medians are shown in Table VI with boot_check the
                                                                    delivers. The averages favor sight everywhere it should help,
most predictable at 47K tokens, with delayed_verification the
                                                                    but the effect does not survive holm correction. How much a
widest in the study at 408K tokens. The boot probe is therefore
                                                                    model looked at its screenshots did not line up with how much
the most predictable configuration as well as the cheapest.
                                                                    it gained.
Granting a shell (execution) roughly doubles the spread
                                                                       We compared mean human interface scores over all
against building blind, adding screenshots widens it further,
                                                                    assigned runs (Table VII), with non-starters counted as zero,
sight without a shell is wider still (301k), and the delayed
                                                                    and conditions with screenshots, visual and visual_no_shell,
verification workflow is the least predictable of all. For anyone
                                                                    score higher than execution, by +10.9 and +4.3 on the
budgeting agent runs, this matters alongside the median cost,
                                                                    calendar-week-view for visual and visual_no_shell
because a surface that looks affordable on average is still hard
                                                                    respectively, and by +2.9 and +5.7 on the metrics-dashboard.
to plan around if any individual run may cost far more.
                                                                       But our pre-specified test is not convinced that the
   Figs. 4 and 5 draw the cost-quality frontier (each condition
                                                                    advantage is real. That test, P4, pools only the two visual-
plotted by what it costs against the quality it delivers) twice:
                                                                    versus-execution comparisons, and gives +6.9 points, 95
once against the machine-probed behavioral score (Fig. 4) and
                                                                    percent confidence interval [+0.8, +13.4], permutation p =
once against the human-graded interface score (Fig. 5). The
                                                                    .041, which does not survive the six-way family holm-
boot_check’s efficiency and the shell's cost premium hold in
                                                                    corrected p (corrected p = .083).
both views. We keep the two quality judgments separate on
                                                                       So, sight's benefit on visually graded work is suggestive, not
purpose, for three reasons. First, they measure different things.
                                                                    established, in this batch. The secondary contrast that
A probe checks whether behavior is correct over the API,
                                                                    separates seeing from running i.e. visual_no_shell versus
while the human judges whether a person can actually use the
                                                                    execution (S2 in Table III) points the same way with the same
application, so a composite would average measures whose
                                                                    caution (visual_no_shell versus execution: +5.0, interval
meaning differs across tasks. Second, any weighting of the two
                                                                    [−1.4, +11.8], Fig. 7).
into a single number would be arbitrary, and a different




16
                                                                                        A. Mehta: Verification helps only where it can see




 FIGURE 6. The same frontier as Figures 4 and 5, drawn separately for each model. In every panel x axis is that model's median token cost, marker fill
 gives the measure (open marks = functional score on the API tasks, filled marks = human interface score on all tasks), and marker shape and color together
 give the condition. The markers are connected in ladder order rather than cost order, so a leftward step means a rung that costs less than the one below it.
 Each segment carries the color of the rung it leaves. The shape recurs at each model's own quality level, which is why pooling in Figures 4 and 5 is
 representative.

                                                                     TABLE VII
                                                                HUMAN INTERFACE SCORES

                                      Condition                                                      calendar-week-view                      Dashboard

                                    no_verification                                                          81.4                                64.3
                                         static                                                              84.8                                60.4
                                      boot_check                                                             96.6                                82.5
                                       execution                                                             86.4                                92.0
                                         visual                                                              97.3                                94.9
                                    visual_no_shell                                                          90.7                                97.7


                                                                     TABLE VIII
                                                          VISUAL VERSUS EXECUTION PER MODEL
                                                                 calendar-week-view gap                                  metrics-dashboard gap
                     Model
                                                                   (no. of screenshots)                                   (no. of screenshots)
                 claude-4.6-opus                                         -0.9 (36)                                               0.0 (48)
                claude-4.6-sonnet                                       +23.2 (62)                                              -2.9 (51)
                 claude-4.8-opus                                          0.0 (9)                                              +1.0 (21)
                 gemini-3.1-pro                                          -0.9 (34)                                             -19.2 (11)
                      gpt-5.5                                            +0.9 (3)                                              +2.9 (22)
                     grok-4.3                                           +42.9 (1)                                              +35.6 (0)ᵃ

   ᵃNon-user: this model took no screenshots in these runs. Under the pre-specified rule for the per-model split, a non-user's sight effect is untestable. The
value is shown for completeness. Because the model never looked, the gap cannot come from seeing the page and it reflects the model's unusually low score
with the shell alone (Section IV-D)




2026                                                                                                                                                        17
                                                                                     A. Mehta: The reach of a verification tool decides its value




 FIGURE 7. Sight-without-shell matches sight-with-shell on both visual venues, locating whatever value exists in the visual channel itself rather than the
 shell beneath it. Each bar is the mean human interface score across all six models in that condition, and each mark on it is one model's own mean, colored
 and shaped per model and spread horizontally so that models landing on the same score stay countable. The same model keeps the same mark in both
 panels, so a model can be followed across conditions and tasks. Both panels carry the same axis, repeated on the right for reading convenience.

   We would like to mention two patterns that hold throughout                       Fig. 8 shows the problem in one picture. Each point is one
the averages, but they are descriptive and we report them                        model on one visually hard task, placed horizontally by how
without a statistical test. First, how much sight helps on a task                many screenshots it took and vertically by how much better it
depends on whether that task's typical mistakes are visible in                   scored with screenshots than with a shell. If looking caused the
a picture (Table VII). The calendar-week-view's mistakes are                     improvement, the points should climb from left to right, heavy
the most visible kind, misplaced events and interactions that                    users high and non-users near zero. They do not. The highest
do not work, and sight helps most there (+10.9). The metrics-                    points sit at the far left with the model that barely looked, one
dashboard's mistakes are static layout, which a model can                        of the heaviest users also sits high at the far right, and the
partly get right from the code alone, and sight helps less (+2.9).               models between are near zero. What does line up with the
The log explorer's mistakes are lag and stutter, which no still                  gains is the shell starting point. The two biggest gainers, grok-
image shows, and there the visual condition lands slightly                       4.3 and claude-4.6-sonnet, scored low with a shell alone
below the shell (-2.2, Section IV-F). Second, removing the                       (around 48 to 56 for grok, 74 for sonnet on the calendar) and
shell did not remove sight's value. On the metrics-dashboard,                    so had the most room to improve; the models already near the
the condition with screenshots and no shell (visual_no_shell)                    top barely moved however many screenshots they took. One
scored as well as the full visual condition, in fact slightly better             moderate user, gemini-3.1-pro, took 11 screenshots on the
(97.7 versus 94.9). This suggests that whatever sight adds,                      dashboard and scored 19.2 points worse there. For grok, which
comes from the seeing itself and not from the shell underneath.                  barely used the tool, two explanations fit our data and we
   However, the per-model split complicates attribution. Table                   cannot tell them apart. grok’s shell builds were unusually bad
VIII restricts the visual-versus-shell contrast to individual                    on their own (they shipped the study's worst interaction
models. The pattern is awkward for a simple "sight helps"                        defects, Section V), or merely being granted a screenshot tool
conclusion, because use and benefit do not line up. The largest                  changed how it wrote its code even unused. Separating these
gap belongs to grok-4.3, which gained 42.9 points on the                         would take a future experiment.
calendar-week-view task while taking a single screenshot, and                       What this study can support is therefore modest. Granting
a further 35.6 points on the dashboard while taking none. The                    sight never hurt the visually graded tasks on average, and its
pooled average is driven largely by that model. Most of the                      pooled benefit is positive but does not survive holm correction.
other models were already near the maximum with a shell                          Because the gains landed on the models with the most room to
alone, so their gaps are small, with one exception, claude-4.6-                  improve rather than on the models that looked the most, we
sonnet, which took the most screenshots on the calendar-                         cannot credit them to models actually looking at their pages
week-view (62) from a lower shell baseline and gained 23                         and fixing what they saw.
points there. No other per-model contrast is individually
significant. How much a model looked did not track how
much it gained, so we cannot credit the pooled benefit to
looking.



18
                                                                                    A. Mehta: Verification helps only where it can see




 FIGURE 8. Each point is one model on one visual task, keyed by the
 same color and shape the model carries in Figure 7, with the task given        FIGURE 9. The shell-versus-blind gap on the modification task
 by fill (open = calendar, filled = dashboard). Horizontal position counts      (brownfield) next to the same gap on the greenfield build of the same
 the screenshots it took and vertical position shows how much better it         board, for both graded halves. The bars match within about a point:
 scored with screenshots than with the shell. If looking caused the             modifying unfamiliar code showed the same tool sensitivity as writing
 improvement, the right side should sit high. Instead, the largest gain (top    fresh code, the pre-specified null.
 left) belongs to the model that took one screenshot, and most heavy users
 sit near zero, with one high exception at the far right.                      seeded, which is the friendliest possible setting for
                                                                               modification, so the hypothesis could still hold on larger or
E. Brownfield modification: a clean null                                       messier codebases.
    We tested whether verification tools matter more when an                       We conducted an additional check that asks whether the
agent modifies an unfamiliar codebase than when it writes                      agents actually modified the code we gave them or quietly
fresh code. We found in our study that they matter about the                   threw it away and rebuilt from scratch, which would make the
same amount.                                                                   comparison meaningless. We tested this mechanically. Each
     The modification task is graded in two halves, a regression               submitted file was compared against the six starter files it
half asking whether everything the original board did still                    began from using content fingerprints, so any changed byte
works (its functional probes rerun verbatim), and a feature half               counts as a change, and a build was classed as a rewrite if it
asking whether the newly requested labels are done well (a                     changed or deleted more than half of the starter. The result
human-graded rubric). On the modification task the execution                   supports the comparison. 140 of 144 builds kept the starter and
versus no_verification gap is 10.0 points on the regression half               extended it, the median build touched exactly three of the six
and 14.0 points on the feature half. On the greenfield version                 starter files in every condition, and the four rewrites are spread
of the same board the matching gaps are 10.6 and 11.8 (Fig.                    across different conditions (three in static, one in visual) rather
9). The two functional gaps are almost identical (10.0 versus                  than piling up where the tools would have made a rewrite easy.
10.6) and the two human gaps are close (14.0 versus 11.8), so                  The rewrites look like isolated flukes, not something the tools
modifying someone else’s code showed about the same tool                       caused.
sensitivity as writing fresh code, not more.                                   F. Performance budgets: measurement beats sight
    The pre-specified test asks the question directly. We
measured the tool gap (execution versus no_verification)                          We measured the same tool ladder on the log-explorer-perf,
twice for functional score, once on the modification task and                  the one task whose failures can only be measured, not seen.
once on the fresh build of the same board, then subtracted one                 The finding is a reversal. Section IV-D showed that on the two
gap from the other, a design called a difference-in-differences.               visually hard tasks (metrics-dashboard and calendar-week-
The subtraction comes to -0.7 points, essentially zero, which                  view) the visual condition sat at or above the execution
means it matters about the same in both settings. The 95                       condition on the human interface score, 97.3 against 86.4 on
percent confidence interval around it runs from -13.7 to +12.7,                the calendar and 94.9 against 92.0 on the dashboard (Table
which is wide.                                                                 VII). On the log-explorer-perf the same comparison turns
    In other words, the data cannot say which way this goes. It                around. The execution condition moves to the top at 93.8 and
could be slightly less, slightly more, or the same. What the                   the visual condition falls behind at 91.7, because a screenshot
interval does rule out is a large difference in either direction.              is a still image and these failures live in motion and delay. The
Had modifying existing code made the tools matter by roughly                   reversal lands exactly where the study was built to expect it.
thirteen points or more, a study of this size would have caught                   This was a designed prediction rather than an unexpected
it. A smaller difference could still hide in the noise, so a honest            outcome. We put the log-explorer-perf in the study for exactly
reading is that we found no difference, which is not the same                  this purpose, as the task where screenshots should be useless
as showing that none exists.                                                   and running the app and interacting with it should be the most
    We report this as a null with one caveat. Our brownfield                   effective way to test it. The log-explorer-perf's failures do not
starter is small (a few files), well structured, and freshly                   show up in a screenshot and cannot be caught over the API.


2026                                                                                                                                                19
                                                                                        A. Mehta: The reach of a verification tool decides its value




 FIGURE 10. The log explorer reverses the visual tasks' ordering. Left: human interface scores by condition. The shell leads and both screenshot arms sit
 slightly below it, because a static image cannot show jank. Right: this task's 13 genuine launch failures by condition, nearly all in the blind and linter arms.
 Much of the shell's headline advantage here is startup survival, not rendering quality.

We can only see them by running the app with a lot of data,
                                                                                    G. Self-authored tests are not a substitute
where a frozen scroll or an unvirtualized list finally appears.
So the negative control behaved as designed. The committed                             We measured whether a model that can only run its own test
contrast (S3 in Table III) finds that adding screenshots on top                     suite (the behavioral condition) reaches the quality of a model
of the shell buys nothing on this task (−2.2 against the shell,                     given the full execution shell.
                                                                                                                     TABLE IX
interval [−12.5, +7.3]), and the screenshot-only arm tells the                               LOG EXPLORER MEAN HUMAN INTERFACE SCORE: EXECUTION
same story descriptively. visual_no_shell averages 91.2                                                 VERSUS NO_VERIFICATION, BY MODEL
against execution's 93.8 (Fig. 10). The control passes both                                                                     Launched
                                                                                                                                             Launche
ways, and it confirms the rule this study keeps finding, a                            Mode no_verificat      executi                            d
                                                                                                                        Gap   (no_verificati
                                                                                         l         ion         on                            (executi
checking tool helps only when it can observe the kind of                                                                           on)
                                                                                                                                               on)
failure the task actually produces.                                                   claud       100.0       100.0    +0.0        5/5         5/5
   This task also produced 13 of the study's 66 genuine launch                        e-4.6-
failures, and nearly all of them (11 of 13) fall in the                                opus
                                                                                      claud       100.0       95.0      -5.0       5/5         5/5
no_verification and static conditions (Fig. 10). That fits how                        e-4.6-
much setup the task needs. Before the app can show anything,                          sonne
it has to load a database full of log data and run the code that                         t
                                                                                      claud       100.0       100.0    +0.0        5/5         5/5
queries and serves it, so there are more moving parts that can                        e-4.8-
break before the first page ever loads. The execution versus                           opus
no_verification effect here is +15.3 points, interval [+7.3,                          gemin         0.0       100.0    +100        0/5         5/5
                                                                                      i-3.1-                             .0
+24.0], raw p = .023, which does not survive the family                                 pro
correction (corrected p = .068).                                                       gpt-        80.0       97.0     +17.        4/5         5/5
   That effect is also uneven across models in a revealing way                          5.5                              0
                                                                                      grok-        91.0       71.0     -20.0       5/5         5/5
(Table IX). Almost all of the +15.3 points come from one
                                                                                        4.3
model, gemini-3.1-pro, whose no_verification builds all failed
                                                                                    We found that it does not, and the gap is not only about quality
to even start and scored zero while its execution builds ran
                                                                                    of tests written. The shortfall has two prominent sources. Part
fine, giving it a full 100-point gap.
                                                                                    of it is survival and fewer behavioral builds ever started, and
   So on this task, the execution’s apparent quality edge is
                                                                                    no test suite can rescue an application that does not launch.
mostly just its builds starting at all, dressed up to look like
                                                                                    The rest is a blind spot no well-written test can compensate
quality. One limit on the scope of verification is worth
                                                                                    for, which is a model's own tests encode its own understanding
mentioning. The spec sets exact speed targets, but we do not
                                                                                    of the task, so when that understanding is wrong, the tests pass
yet have a tool that measures them, so the human grader
                                                                                    and the misunderstanding ships anyway.
judged the visible signs of poor performance instead, such as
                                                                                       The behavioral condition runs on seat-booking only, 24
freezes, blank regions, and an overgrown page. This section
                                                                                    runs, and it is the weakest configuration in the study. Its
therefore reports what the grader saw, not timed
                                                                                    survival is 83 percent and its functional score is 71.2, against
measurements.
                                                                                    87.3 for execution on the same task and 94.2 for execution
                                                                                    pooled across all API tasks (Fig. 11). Breaking the score down,
                                                                                    the shortfall sits in two places as mentioned earlier. Fewer


20
                                                                                  A. Mehta: Verification helps only where it can see




                                                                                  but a transparent time label layer stretches over the whole
                                                                                  grid that does not pass the click events through, so every
                                                                                  mouse interaction dies silently. The model, running in the
                                                                                  execution condition, had even written automated tests for
                                                                                  the code that calculates where each element sits on the
                                                                                  grid, the coordinates and sizes that place the time labels
                                                                                  and cells. Those tests passed, so the positioning math was
                                                                                  provably correct. But a unit test only checks that logic on
                                                                                  its own. It cannot notice that an invisible layer is sitting
 FIGURE 11. The one task that ran the self-authored-tests arm. That arm
                                                                                  on top of the grid and swallowing every click, which is
 (rightmost) is the weakest surface on both survival and functional score:        what made the page unusable. No API probe, no code
 under a fixed budget, writing a test harness appears to displace finishing       review, and no passive screenshot can see this. Only
 the application.                                                                 clicking can.
builds survive at all, and the ones that do run struggle on the               •   The server that cannot serve itself: In development mode,
deep concurrency probes.                                                          the frontend forwards some web addresses to the backend
   The behavioral arm did not stop because it hit any limit. No                   so the page can reach its data (a proxy rule). Two models
run was cut short by the harness or a token budget, every run                     independently wrote that rule so broadly that it also
ended by declaring itself finished, and these runs stopped far                    captured requests for the application's own JavaScript
below what the shell runs spent. On seat-booking it used 369                      module. The browser asked for the page's program files
thousand tokens against the shell's 810 thousand and stopped                      and was handed data instead, so the page loads without its
after 22 steps against 49, while writing a similar amount of                      code. Both builds had been verified only through their
code. It wrote its tests, watched them pass, and finished early.                  production path, where the proxy is not involved.
A model's own tests only check whether its code matches its                   •   The date that became a number: In one model's
own understanding of the task. If the model’s understanding is                    no_verification run on the calendar-week-view, the
wrong, the tests could be wrong in the same way and still pass.                   layout code clamps each event with a numeric max
A shell is different, because running the application shows                       function applied straight to Date objects, Math.max(start,
what actually breaks.                                                             dayStart), which silently collapses them into millisecond
   The pre-specified secondary contrast (S5 in Table III:                         numbers the renderer can no longer position. The data
behavioral minus execution on the functional score) is −16.1                      was fully correct and almost nothing drew (scored 7.1
points, 95 percent interval [−31.7, −1.7], p = .043, and it is                    percent, with none of its eight rubric items fully passing).
negative for five of the six models. So, the models that had to                   The same clamping mistake appears again in the static
write their own tests scored about 16 points lower on the                         condition, though the replicate there re-wraps the value at
automated behavior probes than the models that were provided                      each use and still renders, so it is not a clean failure. The
with a shell. The whole interval sits below zero, so the shortfall                same model's sight-granted runs wrap the clamp back into
is unlikely to be chance, and it holds for five of the six models.                a date, new Date(Math.max(..).), and render correctly.
The interval is wide, running from about 2 points to about 32,                •   The linted syntax error: In the static condition, one build
so we are far more confident about the direction of the gap                       ships an unparseable frontend file. The logs show the
than about its size. Though this is a small sample on a single                    model invoked the linter exactly once, but it had never
task, so we report it as a secondary finding, not a headline                      added a lint script, so the call failed with "Missing script:
result.                                                                           lint" and inspected nothing. The model ignored that
                                                                                  failure, then a later edit spliced a fresh syntax error into
       V. THE DEFECT CATALOG: HOW APPLICATIONS                                    the file (an old_str that ended mid-identifier, leaving a
                   ACTUALLY FAIL                                                  dangling fragment), which was never re-checked before
                                                                                  finishing. Granting a tool is not using it, invoking it is not
These examples show the typical ways applications failed, not                     wiring it up, and neither is the same as heeding it.
every case we found. The human grader’s full notes record                     •   The immortal error banner: A dashboard whose
many more incidents than the six below, which were chosen                         stylesheet overrides the HTML mechanism its own
because each defeats a different verification layer. The point                    JavaScript uses to hide the "backend unavailable" banner,
of the catalog is not a census of everything that went wrong                      so a healthy application permanently tells the user it is
but a demonstration that consequential failure classes exist that                 down.
no unit test, no linter, no boot probe, and no API probe would                •   The query that works until asked: One build stores its
catch. The pattern that unifies them is that functionality was                    dates as plain text in the database, and one of its queries
verified at one layer but broken at another.                                      does arithmetic on those dates. The server starts cleanly,
• The inert page: This is a calendar-week-view defect                             so a boot probe passes it. The crash comes on the first real
     where the API is perfect and rendering is pixel-accurate,


2026                                                                                                                                          21
                                                                                 A. Mehta: The reach of a verification tool decides its value




                                                                                 We single out the first two defect classes, out of everything
                                                                              in the grading notes, for two reasons. They recurred most often
                                                                              during hand-grading, and both can be checked mechanically
                                                                              and identically for every build.
                                                                                 45 of 1,116 builds (4 percent) ship a wiring problem. That
                                                                              rate is low and fairly even across conditions, roughly 1.6 to 6.8
                                                                              percent, and is highest in the boot_check condition. The data-
                                                                              directory bug is much more common, 169 builds (15 percent),
                                                                              and it depends heavily on tools, about 21 to 26 percent in the
                                                                              no_verification and static conditions, dropping to 5.7 percent
                                                                              under the boot probe and around 11 to 13 percent in the shell
 FIGURE 12. Configuration-incoherence rates by condition. Running the
 dev script (execution condition) reduces but does not eliminate the class.   conditions (Fig. 12).
 The boot probe nearly eliminates the data-directory bug because its one         These defect rates carry two lessons. First, running the dev
 call exercises exactly the failing step.                                     path helps but does not fix the problem. Several builds in the
                                                                              execution condition only ever checked their production build
      request, when the arithmetic meets the text, a failure that
                                                                              and shipped a broken development configuration anyway.
      by construction exists only at request time.
                                                                              Second, which model built the app predicts the defect better
   Two of these failures are not one-offs. The same Vite
                                                                              than which tools it had. Splitting the same defects by the model
misconfiguration (Vite is the standard frontend development
                                                                              that built them (Fig. 13), the data-directory bug appears in
server these applications use) recurs in 52 runs, splitting into a
                                                                              about 41 percent of claude-4.6-sonnet's builds and 24 percent
proxy that swallows the app's own api.js (20 runs, almost all
                                                                              of claude-4.8-opus's, versus 3 percent for gemini-3.1-pro and
claude-4.8-opus) and a Vite launched from the wrong folder
                                                                              near zero for grok-4.3 (a single build). Section V observed that
so it ignores the proxy config (32 runs, almost all claude-4.6-
                                                                              a model repeats its characteristic mistakes run after run. This
opus), which suggest this is a model behavior rather than
                                                                              is that observation in quantitative form. Which defect a build
random noise.
                                                                              carries is predicted better by who wrote it than by what tools
   These counts come from the human grader's hazard log,
                                                                              it                                                           had.
which records every run where the grader encountered the
defect while grading. Section VI-A's scanner counts (45                       FIGURE 13 The same two defect classes split by model instead of
wiring defects; 22 proxy-not-loaded; 16 api.js collisions)                    condition. The spread is far wider than Figure 12's: which defect a build
come from a static scan applied uniformly to all 1,116 builds.                carries is predicted better by who built it than by what tools it had, the
                                                                              temperature-zero idiom finding in quantitative form.
The two instruments measure related but not identical
conditions, so their totals differ by design; both datasets are               B. Model signatures (exploratory, observational)
released (grading-hazards.csv, wiring_report.csv).                            We ran a batch-wide structural scan to determine whether the
                                                                              implementations carry a stable model signature independent
 VI. CONFIGURATION INTEGRITY AND MODEL SIGNATURES                             of its tool condition. The structural scan extracted ten concrete
A. Declared-launch integrity                                                  engineering choices from every artifact: where the package
                                                                              manifests live, how the directory tree is organized, which
The launch-configuration defects introduced in Section V
                                                                              JavaScript module system is used, how the dev processes are
were found and then measured in three steps. First, while
                                                                              orchestrated, how the frontend build tool is invoked, how the
hand-grading, the human grader kept running into the same
                                                                              frontend calls the API, whether TypeScript is used, whether
launch problems and wrote each pattern down as it recurred.
                                                                              the standard build tool is used, whether tests are written, and
Second, once the patterns were clear, we turned them into two
                                                                              whether a README is written. For each structural feature we
automatic scanners and ran both over all 1,116 builds. The
                                                                              computed its association strength (Cramér’s V [35], a 0-to-1
scanners read the code without running anything, so every
                                                                              measure of how strongly a categorical choice is predicted by a
build is checked the same way no matter its tool condition or
                                                                              grouping) with model and, separately, with condition (Table
whether it even starts:
                                                                              X).
• Wiring scanner: does the frontend's declared start-up
                                                                                 Of the ten structural choices we tracked, seven are model
     actually load its own proxy configuration, and does that
                                                                              habits. They are predicted far better by which model wrote the
     proxy point to the port where the backend listens?
                                                                              app than by which tools it had, so each model's choices read
• Data-directory scanner: does the code create its database
                                                                              like a fingerprint. Only one choice, whether the app ships tests,
     directory before trying to use it? This is the defect behind
                                                                              is tied to the tool condition instead, and it belongs to the
     several startup crashes.
                                                                              behavioral condition. And that result comes from the study
• Third, the few builds the scanner could not classify on its
                                                                              design rather than from the models. The behavioral condition's
     own were classified by hand, and those classifications are
                                                                              only tool runs the project's own test suite, so a model there has
     recorded in the released dataset (datadir-unknown-
     resolutions.csv). No build was modified at any point.

22
                                                                            A. Mehta: Verification helps only where it can see




to write tests before it has anything to run. Everything else
about how an app is built comes from the model, not the tools.
                                                                 TABLE X
                                                             CRAMÉR’S V VALUES

               Feature                        V with model                    V with condition                              Verdict

        package manifest layout                  0.46                               0.16                                Model idiom
           directory tree style                  0.40                               0.10                                Model idiom
             module system                       0.36                               0.10                                Model idiom
       dev process orchestration                 0.39                               0.13                                Model idiom
       frontend build invocation                 0.27                               0.12                                Model idiom
             API client style                    0.34                               0.12                                Model idiom
           README written                        0.70                               0.18                                Model idiom
              tests written                      0.17                               0.66                               Condition effect
             TypeScript use                      weak                               weak                                  Neither
         standard build tool use                 weak                               weak                                  Neither


   Each model's most common choices read like a fingerprint.           the agent could not click its way into. In 110 runs the agent
One model, gpt-5.5, lays its project out as a src tree in 77           used at least one such URL, and in 67 runs it went further and
percent of its runs and starts its frontend build with a bare          authored a purpose-made page whose only role was to be
invocation in 94 percent, regardless of which tools it was             photographed, with names such as preview.html, test-
given. These are style preferences rather than mistakes, and           visual.html, viewport-360.html, and, in one seat-booking run,
the bare invocation is in fact the variant that avoids the launch      static-preview-hold.html and static-preview-booked.html,
hazard described in Section VI-A. Another model, grok-4.3,             which are mock-ups of the states a click would have produced.
mixes root and nested manifests in 82 percent of its runs. The         The workarounds take three forms: Models forced state
launch-configuration hazards of Section VI-A are similarly             through the address bar, using fragments and query parameters
concentrated, for example claude-4.6-opus accounts for 16 of           such as #scroll-bottom, ?scrollTo=22, ?demo=edit,
the 22 cases where the frontend never loads its proxy                  ?theme=dark, and ?width=360. They also built the harness
configuration, and claude-4.8-opus for 14 of the 16 cases              pages described above. And in several runs they edited the
where a root-level api.js collides with the proxy rule. Code           application itself purely to make a state photographable, one
volume is essentially flat across the five core conditions (716        agent noting that it would "temporarily make the API return
to 800 mean lines), so the shell’s 2.35x token premium buys            dark unconditionally, screenshot, revert", and another adding
verification and iteration, not more software.                         "a GET variant of seed temporarily so I can hit it via
   These model signatures are observational rather than                screenshot navigation". One calendar run resorted to a
experimental. We varied the tools on purpose, but the models           javascript: URL that posted four events and reloaded the page.
are fixed groups within which we compare rather than                   In 21 runs the model even stated the limit outright before
randomized treatment across models, and the mix of runs per            working around it or giving up on the check. One wrote, "Let
model is not perfectly matched, so we read them as patterns,           me verify the edit form opens by clicking. I can't click in
not proven causes. Even so, they mechanically explain why              screenshot tool. Let me trust the code." Some other models
defects cluster by model, since a defect usually grows out of          recorded that the tool "can't type into inputs", "can't resize",
one model's habitual way of building a project. A model                and "can't interact", each time falling back on reading the code
makes the same design and appearance choices again and                 instead of observing the behavior.
again, whether or not it is sampling deterministically, so those          Two inferences can be made from this. Our visual
choices are properties of the model itself.                            conditions therefore measure the low end of what sight can do,
                                                                       since a tool that cannot click will never find a fault that only
                         VII. LIMITATIONS                              appears on clicking. And the inert page of Section V, a
                                                                       calendar that renders correctly and ignores every click, is
A. Passive Screenshot tool
                                                                       precisely the defect this channel is structurally unable to see,
Our screenshot tool takes a single argument, a URL. It renders         which is why it survived the visual condition.
a page and returns an image. It cannot click, type, drag, hover,
or resize. This limits what the visual arms could ever have            B. Reasoning is not carried across turns
caught, and the run logs show the agents meeting that bound            Because no reasoning content was returned to the agent, a
repeatedly rather than merely in principle.                            model's reasoning could not be carried from one turn to the
   Across the 264 runs in the two sight conditions, visual and         next, and every turn proceeded from the message history
visual_no_shell, 214 took at least one screenshot, making              alone. This was identical across all conditions, so it does not
1,326 calls to 260 distinct URLs. Of those calls, 512, or 39           distort the comparisons, but it does bound what the results
percent, pointed somewhere other than the application's own            speak to. Conditions differ in how many turns they take, and
root. These figures are a measure of effort spent reaching states      the arms with a shell run much longer than the arms building

2026                                                                                                                                      23
                                                                        A. Mehta: The reach of a verification tool decides its value




blind, so whatever benefit reasoning continuity might confer         survives the correction, this design supports it well. Where a
would accrue unevenly across the ladder. On an interface that        result comes out null, all we can say is that any real effect is
returns and preserves reasoning, the quality gaps we report          no larger than the far end of its interval. That is not the same
could widen and the cost gaps could narrow.                          as saying the effect is zero.
C. Single Grader                                                     G. Non-customizable sampling setting
The human interface scores come from a single grader. The            Three of six models’ APIs rejected the sampling settings we
grades were produced condition-blind, in shuffled order,             requested and ran at the provider's defaults instead, but each
against written per-item criteria. The repeatability of the scores   such model used the same settings across all of its own runs,
was measured with a condition-blind regrade of a 10 percent          so there is no inconsistency within any single model.
sample after a four-week washout. The regrade process
reproduced item verdicts at 98.8 percent (weighted kappa 0.97                                 VIII. CONCLUSION
pooled, 0.94 on launched runs) and agreed on every survival             Across 1,116 controlled builds, the verification surface’s
call (Section II-J). However, this addresses stability, not          value separates into tiers that no single pass rate would reveal,
correctness. The limitation remains contained in scope and           and what decides each tier is reach: a tool changes the artifact
conditions such as whether an app started, what kind of crash        only where it can exercise the part that fails.
it hit, and every automated behavior test are measured by code          The bottom tier, survival, is nearly free. Agents authoring
and return the same result on a rerun, so only the human             blind fail to produce a launchable application in about one
quality ratings are exposed to this concern.                         build in seven, almost always through environment
D. Rubric-only tasks                                                 assumptions and unforced source corruption, and one cheap,
Three tasks (the calendar, dashboard, and log explorer) have         well-designed boot check removes almost all of these launch
no automated functional tests, so the human rubric is their only     failures, at a fraction of a full shell's cost and with the most
grade. Grading one dashboard run exposed a weakness in that          consistent results of any condition we tried. It is not quite
setup. An app can render its interface correctly yet be              perfect. One build in 192 still failed, and that one was a broken
functionally empty, like a dashboard whose cards all display         frontend on top of a healthy backend. The boot_check only
but hold no data. Because the rubric mainly checks whether           watches whether the server starts, so a broken page is the
the interface looks and behaves right, it can score such an app      single thing it cannot see.
too generously and not penalize the underlying failure enough.          The middle level of value is behavioral depth, getting the
We treat this as a known limit of the rubric's reach and flag it     app to behave correctly under demanding runtime conditions.
in the notes of each affected run rather than change the scores      This comes only from actually running the code. The tests that
to correct for it.                                                   expose it, handling many requests at once, surviving a restart
                                                                     with the data intact, and keeping the right order under load, are
E. Statistical power                                                 exactly what set the shell-equipped builds apart from every
Two limitations of statistical power (a study’s ability to detect    cheaper condition. Letting the model write its own tests
an effect that is really there) deserve plain statement. First,      instead is a poor replacement, and not because it runs short of
running the same model on the same task twice tends to               room. On the one task where we tried it, the self-testing
produce similar code with the same quirks, so our four to five       condition used less than half the shell's tokens and stopped
replicates of a cell are not four to five independent chances to     after 22 steps against 49, while writing a similar amount of
observe a defect. If the model’s habit produces the bug, every       code. It wrote its tests, watched them pass, and finished early.
replicate tends to share it. The study’s statistical strength        Tests a model writes itself can only check its code against its
therefore comes from having six different models, not from           own reading of the task, so they repeat a misunderstanding
the replicates within each cell. Second, six models mean only        rather than catch it.
six independent blocks. Comparisons pooled across the six               The highest level of value, how well the app renders and
models have reasonable power, but any comparison inside a            meets its measured targets, is where it matters most which kind
single model rests on four or five runs per condition and            of task you are on. On average, screenshots help exactly on
cannot reach significance on its own, which is why per-model         tasks whose problems are visible to the eye, and add nothing
numbers in this paper are always descriptive.                        on tasks whose problems can only be measured. The important
                                                                     caution is that even this average benefit does not pass the
F. Correction and null results                                       stricter corrected significance test, and most of it comes from
Two of the six pre-specified effects look significant on their       a single model that barely looked at the screenshots at all. So
own but no longer clear the bar once we correct for testing all      two questions stay open: how large sight's real effect really is,
six together, so we report them as suggestive rather than            and whether it works by the model actually looking at what it
established. The brownfield result is a null, but its confidence     built. Our design can raise these questions, but this batch of
interval is wide, so it rules out only large effects and cannot      data cannot settle them.
exclude a small or moderate one. In short, where an effect

24
                                                                            A. Mehta: Verification helps only where it can see




   For practitioners the actionable summary is unchanged by           dataset can also be found under the Zenodo archive and github.
the nuance:                                                           The archive also contains the code that produced those
   • A cheap boot probe is the best verification token in this        numbers: the grading instrument and its frozen rubric cards,
        study.                                                        the verification chain that regenerates the analysis table byte-
   • An unrestricted shell buys behavioral depth at 2.35              for-byte from the published inputs, and the pre-specified
        times the cost and leaves a characteristic residue of         statistical plan with its committed analysis code and complete
        interaction dead frontends.                                   output. The agent harness that generated the builds is
   • Screenshots are cheap insurance on visually hard work            documented in the archive through its byte-exact prompts, per-
        but should not be mistaken for interaction testing.           condition tool schemas, one full example trace per condition,
   Looking at each model on its own adds one more lesson.             and every run’s complete tool-call log. Appendix B maps each
How much verification a model needs is itself a trait of the          artifact class named in this paper to its exact path in the
model. When we compare each model against its own                     archive.
no_verification baseline, the strongest model gained nothing
from any tool, because it already scored perfectly on the API                                        APPENDIX A
tasks while building blind. The weakest model gained 37                                     The Agent Interface
points once it was handed a shell. And the tool that helped each      The two texts below are reproduced byte-exact (their hashes
model most was not the same from one model to the next. So,           are verified against every run manifest), so their punctuation
the verification budget is best decided model by model, and           is the instrument’s own.
for most models the cheap boot probe is enough.                       Base prompt (constant across every run):
   For people who evaluate models, the study's method may             You are a software engineer. Your workspace directory is
matter more than its exact numbers. We graded the finished            {workspace}. Implement the task described by the user by
apps rather than the chat logs, kept every prompt byte-for-byte       creating files in the workspace using the provided tools. Work
identical so that only the tools changed, decided in advance          until the task is complete, then call finish. Use only the tools
how to handle models that refused our settings and apps that          provided to you.
failed to start, and kept a human judge for the one layer no          Universal environment briefing (identical in every condition):
automated check can reach. Together these choices exposed             Environment: the tools listed in this request are the complete
kinds of defects, and hard questions about what actually              set available to you. Tools not listed do not exist in this
caused them, that a pass-or-fail benchmark is, by construction,       environment and cannot be installed or obtained. Review what
unable to see. A single pass rate cannot distinguish never-           is available and use whatever helps you complete and check
started from almost-right, and it has no channel for a page that      your work. If no installation or execution tools are provided,
renders perfectly yet responds to nothing.                            author every required file completely from first principles;
   The single rule behind all of these results is reach. A boot       dependencies declared in package.json files are provisioned
probe watches startup, so it removes launch failures and              by the environment after you finish.
nothing else. A shell drives the running application over its         Per-condition tool schemas (8 files) and one full example trace
own interfaces, so it buys behavioral depth and leaves                per condition are in the archive under agent-interface/
untouched the defects that live in the rendered page.                 (Appendix B).
Screenshots reach what is visible, so they pay on geometry and
layout and add nothing where the fault is measurable but                                             APPENDIX B
invisible. A linter reaches only the code it is actually wired to
                                                                                     RELEASED ARTIFACT MAP
inspect, which in a quarter of its runs was nothing at all.
                                                                      Everything this paper derives from is published in one archive:
Choosing a verification surface is therefore not a question of
                                                                      Zenodo DOI 10.5281/zenodo. 21961590 (all-versions
how much tooling to grant, but of whether the tools granted
                                                                      identifier),                   browsable                     at
can exercise the way this particular application is likely to fail.
                                                                      https://github.com/achintmehta/coding-eval-agent-runs .
               DATA AND CODE AVAILABILITY                             The dataset of record is the SHA256 sealed snapshot
                                                                      20260720/, and the archive’s README.md contains step-by-
All data underlying the findings are openly archived at Zenodo        step reproduction recipes (regenerate the analysis table byte-
under DOI 10.5281/zenodo.21961590 (the all-versions                   for-byte, recompute every statistic, regrade any artifact from
identifier, resolving to the latest release) and are browsable at     scratch).
https://github.com/achintmehta/coding-eval-agent-runs. The
archive contains the 1,116 built applications exactly as                                             REFERENCES
shipped, complete per-run tool-call logs, all machine grades          [1]   B. Rombaut, "Inside the scaffold: A source-code taxonomy of coding
and condition-blind human rubric scores, the hand-audited                   agent architectures," arXiv:2604.03515, 2026.
launch-failure classifications, and three SHA256-sealed               [2]   J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan,
dataset snapshots, of which freeze-20260720 is the dataset of               and O. Press, "SWE-agent: Agent-computer interfaces enable
                                                                            automated software engineering" in Proc. Adv. Neural Inf. Process.
record that every number in this paper traces to. The regrade               Syst. (NeurIPS), 2024. arXiv:2405.15793.

2026                                                                                                                                         25
                                                                                      A. Mehta: The reach of a verification tool decides its value




[3]  C. S. Xia, Y. Deng, S. Dunn, and L. Zhang, "Agentless: Demystifying          [26] J. R. Landis and G. G. Koch, "The measurement of observer
     LLM-based software engineering agents" arXiv:2407.01489, 2024.                    agreement for categorical data" Biometrics, vol. 33, no. 1, pp. 159-
[4] M. Chen et al., "Evaluating large language models trained on code"                 174, 1977.
     arXiv:2107.03374, 2021.                                                      [27] A. R. Feinstein and D. V. Cicchetti, "High agreement but low kappa:
[5] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K.                I. The problems of two paradoxes" J. Clin. Epidemiol., vol. 43, no. 6,
     Narasimhan, "SWE-bench: Can language models resolve real-world                    pp. 543-549, 1990.
     GitHub issues?" in Proc. Int. Conf. Learn. Represent. (ICLR), 2024.          [28] R. A. Fisher, The Design of Experiments. Edinburgh, U.K.: Oliver and
     arXiv:2310.06770.                                                                 Boyd, 1935.
[6] Z. Lu et al., "WebGen-Bench: Evaluating LLMs on generating                    [29] E. J. G. Pitman, "Significance tests which may be applied to samples
     interactive and functional websites from scratch" arXiv:2505.03733,               from any populations," Suppl. J. Roy. Statist. Soc., vol. 4, no. 1, pp.
     2025.                                                                             119-130, 1937.
[7] K. Zhang, J. Li, G. Li, X. Shi, and Z. Jin, "CodeAgent: Enhancing code        [30] A. Yeh, "More accurate tests for the statistical significance of result
     generation with tool-integrated agent systems for real-world repo-                differences," in Proc. 18th Int. Conf. Comput. Linguistics (COLING),
     level coding challenges" arXiv:2401.07339, 2024.                                  2000, pp. 947-953.
[8] L. Pan, M. Saxon, W. Xu, D. Nathani, X. Wang, and W. Y. Wang,                 [31] R. Dror, G. Baumer, S. Shlomov, and R. Reichart, "The hitchhiker's
     "Automatically correcting large language models: Surveying the                    guide to testing statistical significance in natural language processing,"
     landscape of diverse self-correction strategies" Trans. Assoc. Comput.            in Proc. 56th Annu. Meeting Assoc. Comput. Linguistics (ACL),
     Linguistics, vol. 12, pp. 484-506, 2024. arXiv:2308.03188.                        Melbourne, VIC, Australia, 2018, pp. 1383-1392.
[9] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao,                 [32] S. Holm, "A simple sequentially rejective multiple test procedure"
     "Reflexion: Language agents with verbal reinforcement learning" in                Scand. J. Statist., vol. 6, no. 2, pp. 65-70, 1979.
     Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), 2023.                       [33] B. Efron, "Bootstrap methods: Another look at the jackknife" Ann.
     arXiv:2303.11366.                                                                 Statist., vol. 7, no. 1, pp. 1-26, 1979.
[10] X. Chen, M. Lin, N. Schärli, and D. Zhou, "Teaching large language           [34] N. M. Laird and J. H. Ware, "Random-effects models for longitudinal
     models to self-debug" in Proc. Int. Conf. Learn. Represent. (ICLR),               data" Biometrics, vol. 38, no. 4, pp. 963-974, 1982.
     2024. arXiv:2304.05128.                                                      [35] H. Cramér, Mathematical Methods of Statistics. Princeton, NJ, USA:
[11] A. Mehta, "Reasoning effort, not tool access, buys first-try reliability          Princeton Univ. Press, 1946.
     in agentic code generation: An observational study"
     arXiv:2607.02436, 2026.
[12] H. Sansford, D. H. C. Law, W. Liu, A. Tripathi, N. Agarwal, and G.J.
     J. van den Burg, "Vision-guided iterative refinement for frontend code
     generation" arXiv:2604.05839, 2026.
[13] Z. Liu, Y. Huang, T. Xie, R. Zhang, W. Li, and L. Duan, "Coding with
     eyes: Visual feedback unlocks reliable GUI code generating and
     debugging" arXiv:2604.19750, 2026.
[14] Q. Wang, H. Hu, L. Chen, H. Wang, H. Alinejad-Rokny, Y. Lin, and
     M. Yang, "InteractWeb-Bench: Can multimodal agent escape blind
     execution in interactive website generation?" arXiv:2604.27419,
     2026.
[15] J. Deng, K. Yao, and L. Zhang, "VisRefiner: Learning from visual
     differences for screenshot-to-code generation" arXiv:2602.05998,
     2026.
[16] C. Si, Y. Zhang, R. Li, Z. Yang, R. Liu, and D. Yang, "Design2Code:
     Benchmarking multimodal code generation for automated front-end
     engineering," in Proc. Conf. North Amer. Chapter Assoc. Comput.
     Linguistics (NAACL), 2025, pp. 3956-3974. arXiv:2403.03163.
[17] J. Wu, E. Schoop, A. Leung, T. Barik, J. P. Bigham, and J. Nichols,
     "UICoder: Finetuning large language models to generate user interface
     code through automated feedback," in Proc. Conf. North Amer.
     Chapter Assoc. Comput. Linguistics (NAACL), 2024, pp. 7511-7525.
     arXiv:2406.07739.
[18] S. Zhou et al., "WebArena: A realistic web environment for building
     autonomous agents," in Proc. Int. Conf. Learn. Represent. (ICLR),
     2024. arXiv:2307.13854.
[19] T. Xie et al., "OSWorld: Benchmarking multimodal agents for open-
     ended tasks in real computer environments," in Proc. Adv. Neural Inf.
     Process. Syst. (NeurIPS), 2024. arXiv:2404.07972.
[20] X. Wang et al., "OpenHands: An open platform for AI software
     developers as generalist agents," arXiv:2407.16741, 2024.
[21] L. Zheng et al., "Judging LLM-as-a-judge with MT-Bench and
     Chatbot Arena," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS),
     2023. arXiv:2306.05685.
[22] J. Cohen, "A coefficient of agreement for nominal scales," Educ.
     Psychol. Meas., vol. 20, no. 1, pp. 37-46, 1960.
[23] J. Cohen, "Weighted kappa: Nominal scale agreement with provision
     for scaled disagreement or partial credit," Psychol. Bull., vol. 70, no.
     4, pp. 213-220, 1968.
[24] P. E. Shrout and J. L. Fleiss, "Intraclass correlations: Uses in assessing
     rater reliability" Psychol. Bull., vol. 86, no. 2, pp. 420-428, 1979.
[25] K. O. McGraw and S. P. Wong, "Forming inferences about some
     intraclass correlation coefficients" Psychol. Methods, vol. 1, no. 1, pp.
     30-46, 1996.



26
                                                                                  A. Mehta: Verification helps only where it can see




ACHINT MEHTA received the B.E. degree in computer science India, in
2003. He has more than 20 years of software research and development
experience spanning telecommunications, satellite communication, and
cybersecurity domains. From 2003 to 2011, he worked in the
telecommunications industry, developing protocol stacks, and working on
GPON optical network terminal software for embedded real-time systems.
For the last decade, he worked in the cybersecurity industry, first as a Senior
Staff Engineer and Squad Leader developing intrusion prevention systems,
cloud-based network security management, and zero trust secure access
solutions, and currently as a Senior R&D Manager leading the development
of several cloud native security solutions. His research interests include
artificial intelligence, cloud security, zero trust architectures, network
intrusion detection and prevention, telecommunication protocols, and
cloud-native distributed systems.




2026                                                                                                                                   27
