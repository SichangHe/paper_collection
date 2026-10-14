                                                   What do LLMs need to Synthesize Correct Router
                                                                 Configurations?
                                                 Rajdeep Mondal                                 Alan Tang                           Ryan Beckett
                                             mondalrajdeep14@ucla.edu                      atang42@cs.ucla.edu               Ryan.Beckett@microsoft.com
                                                                           Todd Millstein                     George Varghese
                                                                         todd@cs.ucla.edu                   varghese@cs.ucla.edu


                                         ABSTRACT                                                           understands program semantics.
arXiv:2307.04945v1 [cs.NI] 11 Jul 2023




                                         We investigate whether Large Language Models (e.g., GPT-              A plausible way to introduce semantics is to pair a LLM
                                         4) can synthesize correct router configurations with reduced       with an automatic verifier such as a SAT solver or a model
                                         manual effort. We find GPT-4 works very badly by itself,           checker. But verification is not a panacea. First, a verifier
                                         producing promising draft configurations but with egregious        cannot prove correctness without a specification. In prac-
                                         errors in topology, syntax, and semantics. Our strategy, that      tice, specifications are incomplete, so not all solutions are in
                                         we call Verified Prompt Programming, is to combine GPT-4           fact acceptable to the user. Second, for the verifier to auto-
                                         with verifiers, and use localized feedback from the verifier       matically (with minimal human aid) interact with the LLM,
                                         to automatically correct errors. Verification requires a spec-     the verifier must provide actionable feedback. We found it
                                         ification and actionable localized feedback to be effective.       was easier for the LLM to correct itself using feedback from
                                         We show results for two use cases: translating from Cisco          modular verification of components of a network (individual
                                         to Juniper configurations on a single router, and implement-       routers [9] or even route maps within a router [10]), rather
                                         ing no-transit policy on multiple routers. While human input       than the network as a whole.
                                         is still required, if we define the leverage as the number of
                                         automated prompts to the number of human prompts, our
                                         experiments show a leverage of 10X for Juniper translation,
                                         and 6X for implementing no-transit policy, ending with ver-
                                         ified configurations.

                                         1   Introduction
                                              The limitations of his knowledge were as startling
                                              as its profundity – Hardy on Ramanujam [1]

                                            While GPT-4 and other language models have shown great           Figure 1: Pair Programming using human correction.
                                         success in some domains (e.g., writing poems, passing the
                                         LSAT) they have been shown to have issues in other domains            Figure 1 shows the traditional method of pair program-
                                         (e.g,. math, word puzzles) [3]. Language models have had           ming (PP), embodied in systems like GitHub CoPilot [6],
                                         some success in helping users write sequential programs in         where a human and an AI work together to author a pro-
                                         systems like CoPilot [6] and Jigsaw [7]. Our paper examines        gram. In pair programming, the AI and the human form a
                                         GPT-4’s ability to write router configuration files, tradition-    tuple (A, H) and the human H manually checks for correct-
                                         ally written by humans, that help tune routes and forwarding       ness of the output of the AI A and then manually issues cor-
                                         decisions and are critical for network operation. Our early        rection prompts to A as shown in the figure. Such manual
                                         experiments show that GPT-4 by itself is an “idiot-savant",        initial prompting and subsequent manual correction is often
                                         capable of brilliance but also making simple errors that an        called prompt engineering.
                                         operator would be fired for making.                                   Figure 2 shows our alternate vision. In what we call Ver-
                                            Critics have derided large language models (LLMs) as mere       ified Prompt Programming (VPP), the AI, the human, and
                                         “stochastic parrots” [2],because they produce text (say of a       a verification suite (V ) form a triple (A, H, V ). The verifi-
                                         program) syntactically by predicting the next word based on        cation suite checks for correctness and automatically issues
                                         a statistical model derived by training on a vast corpus of text   localized corrections. V may abandon automatic correction
                                         found on the Internet. Our broader goal beyond synthesizing        after some number of trials, and the human must still correct
                                         configs is to see whether LLMs can be combined with other          manually. However, our hypothesis is that human effort is
                                         programs (via APIs) to come closer to a “stochastic owl” that      reduced as the output grows “closer” to a correct program.
                                                                 syntax, and implementing a simple policy (“no transit") on
                                                                 a network of 7 routers. Section 2 describes the system or-
                                                                 ganization of a potential system we call C O S YNTH. Sec-
                                                                 tion 3 describes experiments with Cisco to Juniper transla-
                                                                 tion, while Section 4 describes implementing no-transit on
                                                                 multiple routers. Section 5 compares our ideas to previous
                                                                 work and Section 6 describes lessons learned.

                                                                 2    System Organization
        Figure 2: Verified prompt programming.                   Figure 3 is a refinement of the more general Verified Pair
                                                                 Programming (VPP) vision of Figure 2 that we call C O S YNTH.
   Notice that there is a fast inner loop between V and A,       We emphasize we have not built C O S YNTH. While we use
where verifier results are automatically fed back to GPT-4.      GPT-4 we have not been able to access the APIs, and so man-
Since verifier feedback is often cryptic, we use simple code     ually simulated the API calls with prompts to ChatGPT. Our
that we call a humanizer that converts the feedback to nat-      goal is not to demonstrate a working system but instead to
ural language prompts that are given to GPT-4. When V            explore GPT-4’s ability to author configurations, as in the
either determines the final configuration is correct or a time   “Sparks of AGI" paper [3].
bound elapses, V sends the output back to the user as part
of the slow manual loop. We examine a “reduced work hy-
pothesis": that the work in the manual loop in Figure 2 is
significantly less than then the manual work in Figure 1
   To quantify reduced human effort we introduce a simple
measure that may be useful in other VPP contexts. Define
leverage as the ratio L of the number of automated prompts
in Figure 2 to the number of human prompts. Leverage mea-
sures the effect of the verifier suite, the potential improve-
ment in going from (A, H) to (A, V, H), keeping the lan-
guage model A and the human H the same.
   The reader may think the real leverage is the improvement
from H to (A, H), or from H to (A, V, H). But this de-               Figure 3: Verified prompt programming for Configs
pends on the capability of the human H and is hard to make
uniform or repeatable. Given how error-prone (A, H) is for          The verification suite shown in Figure 3 consists mini-
configurations, we find it more natural to measure the im-       mally of two verifiers, a syntax verifier (we used Batfish [5])
provement caused by VPP. If a future LLM, say GPT-6, pro-        and a semantics verifier (we used different ones depending
duces near-perfect configurations, leverage will decrease as     on the use case). For our second use case, we used a third
there is less need for automatic correction. Our definition      verifier, a topology verifier (that we wrote in Python) as we
also assumes every automatic correction in Figure 2 would        found that GPT-4 sometimes missed announcing routes to
otherwise be be done by a human in Figure 1.                     neighbors. The user provides a precise natural language de-
   The reduced work hypothesis is that the leverage L > 1 is     scription of the context (topology, routers, interfaces) and the
high. Even if the leverage is low (say 1), since it is crucial   desired task (e.g. the Cisco config and a request to translate
that router configurations be correct, combining with a ver-     it to Juniper). GPT-4 output is fed first to Batfish to check for
ifier seems critical. We were happy to find that in both use     syntax errors. C O S YNTH sends GPT-4 feedback about erro-
cases we did end with verified configurations via GPT-4: this    neous lines, “humanized" in natural language (see Table 1
was not obvious at the outset.                                   for examples). The boxes labelled H in Figure 3 correspond
   This vision and hypothesis extends beyond synthesizing        to the humanizer in Figure 2.
configs to more general programs. Prompt programming (as            If all syntax errors are corrected (if too many syntax cor-
opposed to prompt engineering) also reflects the use of APIs     rection attempts occur, C O S YNTH punts to the user), the out-
and automatically generated feedback prompts that may be         put is passed to the semantics verifier. For our first use case,
more generally useful. However, network configs are a sim-       we use Campion [10] as a verifier. For our second use case
ple enough domain to experiment with. Further, there exist       we use Batfish’s symbolic route map analysis as the veri-
config verifiers (e.g., Campion [10] and Lightyear [9]) that     fier, asking it to verify local policies that together ensure the
provide actionable localized feedback.                           desired global policy, as in Lightyear [9]. Once again, the
   For the rest of this paper, we examine the reduced man-       semantic verifier feedback is passed back, suitably human-
ual work hypothesis and measure leverage for two use cases:      ized, to GPT-4. We found that GPT-4 would sometimes cor-
translating a config on a single router from Cisco to Juniper    rect a semantic error while introducing a new syntax error, in
which case we had to return to the syntax verifier. When the            Structural mismatch: This is when a component, con-
semantic verifier attests to a correct config or too many cor-       nection, or named policy is present in the original configura-
rection attempts transpire, C O S YNTH returns to the human.         tion but not in the translation (or is present in the translation
   When C O S YNTH works with multiple routers, we used an-          but not the original). For example, if the original configura-
other module called a “Modularizer" (Figure 3). For network          tion defined a BGP neighbor but there is no corresponding
configs, the idea is that we start with a precise machine read-      neighbor in the translation, there would be a mismatch in
able (we use JSON) description of the “modules" which in             the routing connections. Similarly, if there are correspond-
our case is the topology and the connections. The Modular-           ing BGP neighbor definitions in both configurations, but one
izer outputs a sequence of Natural Language Prompts that             configuration has an import policy defined while the other
describes the topology to GPT-4 (e.g.,. Router R1 is con-            does not, that would be a mismatch in the named policies
nected to Router R2 via interface I1 at R1 and I2 at R2).            present. Campion is able to detect this, and identify the miss-
The Modularizer can also take a general specification of lo-         ing or extra items.
cal policies (e.g. edge routers add a specific community on             Attribute differences: This is when a numerical attribute
ingress) and output a specific local specification for each          has a different value between the two configurations. An
router for the semantic verifier. The Composer puts back             example is OSPF link cost difference between two corre-
the pieces (in our case in a folder for Batfish).                    sponding interfaces. Campion detects these and prints the
   The modularizer follows the prompt engineering paradigm           attributes for corresponding components.
"Give the Model Time to Think" [4], which suggests break-               Policy behavior differences: This is when a route map or
ing a complex prompt into simpler sub-prompts. Exploiting            access control list has a semantic difference. Route maps are
modularity is a way to do so for program synthesis. A second         used to filter incoming or outgoing route advertisements, so
technique we find useful is what is called single shot prompt-       a difference would mean that that there are some route adver-
ing [4]. We start each chat with a set of initial instruction        tisements that are allowed by one router but not allowed by
prompts (IIP) (Figure 3) loaded from a database for avoiding         the other. Campion is able to detect these and output the rel-
common mistakes. The IIP database can be built and added             evant policy names, prefixes, and lines for these differences.
by experts over time. The I/O examples in Jigsaw [7] are an             The distinction among errors helps for two reasons. First,
IIP, but our IIP contains instructions not examples.                 syntax errors and structural mismatches have to be handled
                                                                     earlier since they can mask attribute differences and policy
                                                                     behavior differences. Second, different types of errors re-
3     Cisco to Juniper Translation
                                                                     quire different humanized prompts, while errors of the same
We translate a Cisco configuration into an equivalent Juniper        type can reuse similar prompts. Each type of error can be
one using Verified Pair Programming. Batfish [5] is used to          summarized with a formulaic prompt with some fields in-
identify syntax errors. Campion [10] is used to detect and lo-       serted based on the error reported by Batfish or Campion.
calize semantic differences that are used to refine the result.         Table 1 shows the formulas and examples of generated
We show examples of the issues encountered, and discuss              prompts. Batfish parse errors and warnings can be reused as
success and limitations of the approach.                             prompts for syntax errors. Prompts for structural mismatches
                                                                     and attribute differences are easily generated from the rele-
3.1    Method                                                        vant components and attributes. Policy behavior differences
First, we provide the Cisco configuration, and the prompt:           are more difficult since it is not always clear how to describe
"Translate the configuration into an equivalent Juniper con-         the affected input space that is treated differently. We opt for
figuration." GPT-4 will produce a translation into Junos for-        the approach of giving an example prefix.
mat that typically contains several errors and differences. We
try to rectify these errors iteratively. First, we use Batfish [5]   3.2    Experience and Results
and Campion [10]to detect any errors or differences, and then           We tried translating a Cisco configuration from the Batfish
use a simple script to produce a prompt for GPT-4 (the hu-           examples [5] into Juniper format. This configuration was
manizer H in Figure 3) to try and fix this error. After GPT-4        short enough to fit within GPT-4 text input limits, but used
attempts to resolve the issue, we ask it to print the entire         non-trivial features including BGP, OSPF, prefix lists, and
configuration and check the result using verification tools          route maps. GPT-4’s synthesized Juniper router configura-
again. For our experiment we focus exclusively on behav-             tion had several errors. In many cases, when an automati-
ior related to routing and forwarding, ignoring potentially          cally generated prompt, similar to those in Table 1, is pro-
important features such as NTP servers.                              vided to GPT-4, it will produce a response fixing the issue.
   To design the humanizer (i.e., automatically generate a           In some cases, GPT-4 is unable to edit the translation cor-
prompt informing GPT-4 of the errors present), we distin-            rectly, either applying no change or applying an erroneous
guish four classes of configuration errors:                          one. This often requires manual intervention via more spe-
   Syntax errors: Batfish produces parse warnings identify-          cific prompts in order to fix. Another problem is that GPT-
ing relevant lines that do not use valid Juniper syntax.             4 can fix one error, but introduce new errors that were not
 Type         Generated Prompt                                             ently. Juniper typically does this using the same routing poli-
 Syntax       There is a syntax error:
 error        ‘policy-options prefix-list our-networks 1.2.3.0/24-32’      cies that control importing and exporting BGP routes while
              In the original configuration,                               Cisco configurations set a separate route map for route re-
 Structural   there is an import route map for bgp neighbor 2.3.4.5,       distribution. In our case, Campion detected that the Juniper
 mismatch     but in the translation,
              there is no corresponding route map                          configuration was redistributing some routes that the Cisco
              In the original configuration,                               configuration did not. This could be fixed by adding a "from
 Attribute    the OSPF link for Loopback0 has cost set to 1,               bgp" condition to a number of locations in the policy. Unlike
 difference   but in the translation, the corresponding
              link to lo0.0 has cost set to 0                              the previously described errors, GPT-4 was unable to fix this
              In the original configuration, for the prefix 1.2.3.0/25,    when given the automatically generated prompt. Instead it
              the BGP export policy to_provider for BGP neighbor 2.3.4.5   usually does nothing when asked to fix the error. However, it
 Policy
              performs the following action: ACCEPT.
 behavior                                                                  was able to fix the problem when asked more directly to add
              But, in the translation,
 difference
              the corresponding BGP export policy to_provider              "from bgp" conditions to routing policies.
              performs the following action: REJECT                           BGP prefix list issues: Another subtle issue occurred when
Table 1: Sample rectification prompts for translation                      translating prefix lists. In the original Cisco configuration, a
generated using formulas (non-italicized text), and fields                 prefix list was defined to match prefixes with length 24 or
generated from Batfish and Campion (italicized text).                      greater where the first 24 bits matched 1.2.3.4. In Cisco this
                                                                           is done with the command:
 Error                                      Type                 Fixed
 Missing BGP local-as attribute             Syntax error         Yes       ip prefix-list our-networks seq 5 permit 1.2.3.0/24 ge 24
 Invalid syntax for prefix lists            Syntax error         Yes
 Missing/extra BGP route policy             Structure mismatch   Yes       and it was applied with the definition:
 Different OSPF link cost                   Attribute error      Yes
 Different OSPF passive interface setting   Attribute error      Yes       route-map from_customer deny 100
 Setting wrong BGP MED value                Policy error         Yes           match ip address prefix-list private-ips
 Different prefix lengths match in BGP      Policy error         No
 Different redistribution into BGP          Policy error         No        The noteworthy part is the "ge 24" which says to match pre-
                                                                           fixes with length 24 or greater. There is no equivalent of
Table 2: Translation errors found and whether GPT-4
                                                                           this in defining prefix lists in Juniper, but for our use case,
was able to fix them with generated prompts.
                                                                           there are at least two methods of getting similar behavior in
                                                                           Juniper with different syntax. When GPT-4 is asked to trans-
previously there. Sometimes it even reintroduces errors that               late the configuration, it often does not translate the "ge 24"
were previously fixed! However, we were able to reach a                    part correctly, often just omitting it, so the space of prefixes
point where Campion and Batfish no longer produced errors.                 matched will differ in the translation. When asked to fix this
  Leverage: The entire cycle of prompts was around 2 hu-                   problem, it sometimes generates configurations with incor-
man prompts and 20 automated prompts, for a leverage of                    rect syntax. For example, it can output the following:
10X. Some of the 20 automatic prompt correction cycles in-                 prefix-list our-networks { 1.2.3.0/24-32; }
cluded minor cycles for syntax correction not just at the start
but also after correcting semantic errors. To be clear, we                 which is not valid Juniper syntax. However, after informing
“simulated” each API call by feeding our automatically gen-                it of the error, it does eventually find a correct translation.
erated prompts manually to GPT-4.
  Table 2 shows errors in the translation at some point and                4     Global Policies via Local Synthesis
whether GPT-4 was able to fix them using an automatically                  Next, we used GPT-4 to generate router configs for a given
generated prompt. In more detail:                                          network topology based on local policies for each router, in-
  Missing BGP local-as attribute: The translated BGP neigh-                spired by Lightyear [9], which does control plane verifica-
bor declarations did not include a local AS attribute. We la-              tion by verifying local invariants. We limited our scope to
bel this a syntax error since it produces a parse warning.                 BGP.
  Missing/extra BGP routing policy: An import or export                       For semantic correctness, we use two new modules. The
policy is used for a BGP neighbor in only one configuration.               first is a ’topology’ verifier which checks whether the con-
  Different OSPF link attributes: OSPF links have a num-                   fig of a particular router follows the defined topology. It
ber of attributes, and the translation sometimes contains dif-             checks whether GPT-4 sets up all interfaces, declares BGP
ferences in link cost or passive interface settings.                       neighbors and announces networks correctly. Second, we
  Setting wrong BGP MED value: The translation of one                      run Batfish to check local policies defined in the prompts;
BGP routing policy did not update the BGP MED value.                       the outputs are used to refine the result.
This was caused by an error in translating one of the route
map clauses from the original Cisco configuration.                         4.1     Method
  Different Redistribution behavior into BGP: Cisco and                    We begin by specifying the task to GPT in an initial prompt
Juniper formats handle route redistribution into BGP differ-               using a couple of sentences. The intention is to influence the
LLM to start ‘thinking’ in a certain fashion. Our goal is to        For this, we use an automated "topology verifier" that com-
make the network follow the no-transit policy, under which          pares the config against the previously specified JSON dic-
no two ISP’s should be able to reach other. However, all ISPs       tionary and outputs inconsistencies.
should be able to reach the CUSTOMER and vice versa.                   Semantic errors / Policy errors: GPT-4 produces con-
                                                                    figs that do not follow the intended local policy. We use Bat-
                                                                    fish "Search Route Policies" for verification in this step. In
                                                                    case there is a semantic error, Batfish produces an example
                                                                    where the local policy is not followed. This examples is then
                                                                    fed to GPT-4 in a fresh prompt.
                                                                       Classifying into separate categories allowed us to use dif-
                                                                    ferent tools to address each one. Table 3 lists examples of
                                                                    the rectifying prompts. Once all the errors are rectified, we
                                                                    simulate the entire BGP communication using Batfish as a fi-
                                                                    nal step, in order to ensure that the global policy is satisfied,
Figure 4: Star network topology used for local synthesis.           though the proof technique of Lightyear [9] could instead be
                                                                    used to ensure that the local policies imply the global one.
  It is difficult to write a natural language description of the    4.2    Experience and Results
topology, a task prone to human error. We wrote an auto-
mated script that generates text given the topology as input.       Since some GPT-4 errors were more common, we supplied
In our experiments, we limited our scope to star networks           it an IIP (the Inital Instruction Prompt) as follows:
where one router would be attached to a CUSTOMER IP,                   CLI prompts: GPT-4 would often generate commands to
while the other routers are connected to different ISPs (Fig-       enter on the Cisco command line interface, which is undesir-
ure 4). All the ISP routers are directly connected to the first     able. Thus we specifically asked it to generate the .cfg files.
router. The "network generator" therefore only needs the               Wrong keywords: While generating the configs, it would
number of routers as input. It has two outputs: 1) a textual        often use certain keywords such as ‘exit’, ‘end’, ‘configure
description and 2) a JSON dictionary for the entire network         terminal’, ‘ip routing’, ‘write’, ‘hostname’ and ‘conf t’. It
topology. The textual description is used as a prompt, while        had a tendency to place some of them in the wrong loca-
the JSON dictionary is used later to check whether the gen-         tions. Hence, we directed it not to use these keywords. Any
erated configs match the topology.                                  extra required commands for setup were prepended to the
                                                                    final config files, before running them on Batfish.
   Local versus Global Policy Prompts? We tried speci-                 Match Community: When trying to match against a com-
fying to GPT-4 the global no-transit policy at once. GPT-4          munity, it sometimes generates syntax like:
generated two innovative strategies: filtering routes using AS      route-map FILTER_ROUTES permit 10
path regular expressions, and denying ISP prefixes from be-             match community 100:1
ing advertised to other routers from the customer router. Un-       This is incorrect. The correct way to match against a com-
fortunately, we found after correcting topology and syntax          munity in a route-map is to first declare a community list that
errors, when we provided feedback in terms of a counterex-          contains the community as in:
ample packet (as would be provided by a “global" network              ip community-list 1 permit 100:1
verifier like Minesweeper), GPT-4 was confused and kept             and then while matching, make a call to a community list:
oscillating between incorrect strategies. We found that spec-         route-map FILTER_ROUTES permit 10
ifying local policies as in Lightyear [9] gave us better results       match community 1
because it allowed us to localize verification errors to specific   Thus we included another IIP to define a community list and
routers and specific route maps within those routers.               then in a route-map, match using only this list.
   We asked GPT-4 to generate configs for each router us-             Adding Communities: While adding communities using a
ing a new prompt each time, specifying the local policy for         route-map, GPT-4 tends to generate syntax similar to:
each router. Specifically, the policy is that R1 should add a       route-map ADD_COUMMUNITY permit 10
specific community at the ingress to each ISP and then drop             set community 100:1
routes based on those communities at the egress to each ISP.          We observed that this happens even when we explicitly
The generated errors fell into three categories:                    ask it to ‘add’ a community to the route. The above route-
   Syntax errors: GPT-4 generates a configuration with in-          map replaces all the communities that are already present in
valid Cisco syntax including errors in which certain config         the route with the community 100:1. So we added an initial
lines are misplaced. Batfish produces parse warnings identi-        prompt saying that it should always use the ’additive’ key-
fying these errors.                                                 word when adding a community to the route.
   Topology errors: GPT-4 incorrectly declares or misses              These initial prompts along with the syntax rectification
some BGP neighbors or forgets to announce certain networks.         scheme of Table 3 are able to eliminate common syntax er-
rors produced by GPT-4. Despite this, we found two egre-           Type       Examples
                                                                   Syntax     ‘ip community-list standard
gious cases where human intervention is needed:                    error      COMM_LIST_R2_OUT permit .+’ is wrong syntax.
   Placing neighbor commands in the wrong location: In                        1. Interface eth0/1 ip address does not match with
                                                                              given config. Expected 2.0.0.1, found 2.0.0.2
a config file for BGP, all network and neighbor commands                      2. Local AS number does not match. Expected 1, found 3
must be placed under the "router bgp" block. For example,                     3. Router ID does not match with given config.
the neighbor command is used to attach a route-map to the                     Expected 1.0.0.2, found 1.0.0.1
                                                                   Topology   4. Neighbor with IP address 1.0.0.1 and
ingress or egress of an interface. We found that in rare situa-    error      AS 1 not declared
tions, GPT-4 defines a route-map and then associates it with                  5. Network 1.0.0.0/24 not declared
an interface outside the "router bgp" block. Batfish is able to               6. Incorrect network declaration. 7.0.0.0/24 is
                                                                              not directly connected to R1
catch this syntax error. However, the output is not informa-                  7. Incorrect neighbor declaration. No neighbor
tive enough for GPT-4 to be able to fix the issue.                            with IP address 7.0.0.2 AS 7 found
   AND/OR Semantics in match statements: GPT-4 does                           The route-map DROP_COMMUNITY permits routes
                                                                   Semantic
                                                                              that have the community 100:1. However, they should
not understand the semantic difference between placing mul-        error
                                                                              be denied.
tiple match conditions under a single route-map stanza ver-
sus placing them in different stanzas. For no-transit, we had     Table 3: Sample rectification prompts for local synthesis.
asked GPT-4 to generate a config for R1 that would add a          Batfish or the topology verifier fill in italicized text.
different community to every route incoming from R2 − R6
(Figure 4). We also asked it to filter routes containing any      test cases and tests (but does not verify) the synthesized pro-
such community on the egress of the interface connecting          gram. Jigsaw also does some form of automatic syntax cor-
R1 to R2 − R6. GPT-4 added the correct communities at             rection doing AST-to-AST transformations. CoPilot [6] can
the ingress, but at the egress at R1 it incorrectly used AND      suggest invariants but does not attempt an axiomatic proof.
semantics for filtering routes as in the following route-map      Jigsaw and Copilot do not address two questions we do: how
for the R1 − R2 interface:                                        to use a specification, and how to provide localized feedback.
ip   community − l i s t   1   permit   100:1                        The use of ChatGPT with the Kani Rust verifier [8] comes
ip   community − l i s t   2   permit   101:1                     closest to our vision; the Kani blog post finesses the specifi-
ip   community − l i s t   3   permit   102:1
ip   community − l i s t   4   permit   103:1                     cation question (as we do for Cisco to Juniper) by focusing
ip   community − l i s t   5   permit   104:1                     on program transformations (in their case optimization) for
                                                                  which the source program is the specification. They also do
r o u t e −map FILTER_COMM_OUT_R2 d e n y 10
  match c o m m u n i t y 2                                       not use modularity or local specifications. More fundamen-
  match c o m m u n i t y 3                                       tally the Kani [8] use case does not do prompt programming:
  match c o m m u n i t y 4                                       the user always manually switches between the verifier and
  match c o m m u n i t y 5
r o u t e −map FILTER_COMM_OUT_R2 p e r m i t 20                  the LLM, precluding possible leverage.

   Community 100:1 is associated with routes incoming from        6   Conclusions
R2, 101:2 with those coming from R3 and so on. We de-
                                                                  Our experiments are very preliminary but suggest:
sire routes incoming from R3 − R6 to be filtered out at the
                                                                     1. Ramanujam Effect: As with the mathematician Ra-
egress to R2. The above config will only filter out routes that
                                                                  manujam, some of whose conjectures were incorrect and needed
have all the communities 101:1, 102:1, 103:1 and 104:1, not
                                                                  Hardy’s help [1] for proofs, GPT-4 by itself is not ready
any one of them. When we asked Batfish whether the above
                                                                  for use without a verifier, making elementary errors that can
route-map filters routes that have the community 101:1, it
                                                                  bring networks down.
produced a counterexample but this counterexample to GPT-
4 failed to rectify the issue. A human prompt was needed             2. Verified Prompt Programming: Using a verifier and au-
to ask GPT-4 to declare each match statement in a separate        tomated corrections via a humanizer, GPT-4 can synthesize
route-map stanza. Our attempts to help GPT-4 distinguish          reasonable but not completely correct configurations for sim-
between AND and OR semantics using an example in the              ple use cases, but the leverage in reduced human effort can
IIP also failed.                                                  be high (5X to 10X). Modular verification seems crucial.
                                                                     4. Local versus Global Specifications: Modular synthesis
   Leverage: The entire cycle took 2 human prompts and
                                                                  is the dual to modular verification. The search space for the
12 automated prompts, for a leverage of 6X. Note that the
                                                                  LLM is large, which increases the chance that it will not be
AND-OR problem required a final correction prompt.
                                                                  able to correctly complete a synthesis task based on a global
                                                                  specification. Instead the user needs to decide and describe
5    Previous Work                                                the "roles" each node plays in satisfying the global spec.
Jigsaw [7] and Copilot [6] use large language models for pro-        Much further testing in more complex use cases is needed.
gram synthesis. While they concentrate on sequential pro-         Can GPT-4 add a new policy incrementally without interfer-
grams, the deeper difference is that they do not pair the syn-    ing with existing verified policy? While our paper is set in
thesizer with verifiers. Jigsaw [7] does ask users to provide     the context of network configuration, the vision, definitions
(e.g., leverage) and lessons (e.g., the need for actionable lo-
cal feedback, modularity, humanizers and IIPs) seem more
generally useful to synthesize other programs.

7    References

 [1] B. Bollobas. The man who taught infinity: how G.H. Hardy tamed
     Srinivasa Ramanujan’s genius. https://theconversation.
     com/the-man-who-taught-infinity-how-gh-hardy\
     -tamed-srinivasa-ramanujans-genius-57585, 2023.
 [2] E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell. On
     the dangers of stochastic parrots: Can language models be too big? In
     Proceedings of the 2021 ACM Conference on Fairness,
     Accountability, and Transparency, FAccT ’21, page 610–623, New
     York, NY, USA, 2021. Association for Computing Machinery.
 [3] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz,
     E. Kamar, P. Lee, Y. T. Lee, Y. Li, S. Lundberg, H. Nori, H. Palangi,
     M. T. Ribeiro, and Y. Zhang. Sparks of artificial general intelligence:
     Early experiments with GPT-4, 2023.
 [4] DeepLearning.AI. ChatGPT Prompt Engineering for Developers.
     https://learn.deeplearning.ai/
     chatgpt-prompt-eng/lesson/1/introduction, 2023.
 [5] A. Fogel, S. Fung, L. Pedrosa, M. Walraed-Sullivan, R. Govindan,
     R. Mahajan, and T. Millstein. A general approach to network
     configuration analysis. NSDI’15, page 469–483, USA, 2015.
     USENIX Association.
 [6] github. Github CoPilot: Your AI Pair Programmer.
     https://github.com/features/copilot, 2023.
 [7] N. Jain, S. Vaidyanath, A. Iyer, N. Natarajan, S. Parthasarathy,
     S. Rajamani, and R. Sharma. Jigsaw: Large language models meet
     program synthesis. In Proceedings of the 44th International
     Conference on Software Engineering, ICSE ’22, page 1219–1231,
     New York, NY, USA, 2022. Association for Computing Machinery.
 [8] Kani Rust Verifier Blog. Writing Code with ChatGPT? Improve it
     with Kani. https://model-checking.github.io/
     kani-verifier-blog/2023/05/01/
     writing-code-with-chatgpt-improve-it-with-kani.
     html, 2023.
 [9] A. Tang, , R. Beckett, K. Jayaraman, T. Millstein, and G. Varghese.
     Lightyear: Using modularity to scale BGP control plane verification.
     SIGCOMM ’23, to appear. Association for Computing Machinery,
     2023.
[10] A. Tang, S. K. R. Kakarla, R. Beckett, E. Zhai, M. Brown,
     T. Millstein, and G. Varghese. Campion: Debugging router
     configuration differences. SIGCOMM ’21, page 748–761, New York,
     NY, US, 2021. Association for Computing Machinery.
