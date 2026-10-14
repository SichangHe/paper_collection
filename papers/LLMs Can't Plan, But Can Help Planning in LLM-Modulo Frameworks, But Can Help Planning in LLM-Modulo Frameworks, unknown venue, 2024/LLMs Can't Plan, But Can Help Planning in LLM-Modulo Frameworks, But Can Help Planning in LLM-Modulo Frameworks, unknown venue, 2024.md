                                                                          Position: LLMs Can’t Plan,
                                                               But Can Help Planning in LLM-Modulo Frameworks


                                                      Subbarao Kambhampati 1 Karthik Valmeekam 1 Lin Guan 1 Mudit Verma 1 Kaya Stechly 1
                                                                      Siddhant Bhambri 1 Lucas Saldyt 1 Anil Murthy 1


                                                                   Abstract                                   with System 2 competency. On the face of it, this doesn’t
arXiv:2402.01817v3 [cs.AI] 12 Jun 2024




                                                                                                              seem to ring true, as both by training and operation, LLMs
                                                We argue that auto-regressive LLMs cannot,
                                                                                                              are best seen as a giant pseudo System 1 (Kahneman, 2011)
                                                by themselves, do planning or self-verification
                                                                                                              (see Figure 1). Even from a pure engineering perspective,
                                                (which is after all a form of reasoning), and shed
                                                                                                              a system that takes constant time to produce the next token
                                                some light on the reasons for misunderstandings
                                                                                                              cannot possibly be doing principled reasoning on its own.1
                                                in the literature. We also argue that LLMs should
                                                                                                              Not surprisingly, initial excitement based on anecdotal per-
                                                be viewed as universal approximate knowledge
                                                                                                              formance of LLMs on reasoning tasks (Bubeck et al., 2023)
                                                sources that have much more meaningful roles
                                                                                                              has been dissipated to some extent by the recent spate of
                                                to play in planning/reasoning tasks beyond sim-
                                                                                                              studies, including our own, questioning the robustness of
                                                ple front-end/back-end format translators. We
                                                                                                              such behaviors–be they planning (Valmeekam et al., 2023c;
                                                present a vision of LLM-Modulo Frameworks
                                                                                                              Kambhampati, 2024), simple arithmetic and logic (Dziri
                                                that combines the strengths of LLMs with external
                                                                                                              et al., 2023), theory of mind (Ullman, 2023; Verma et al.,
                                                model-based verifiers in a tighter bi-directional
                                                                                                              2024b), or general mathematical and abstract benchmarks
                                                interaction regime. We will show how the models
                                                                                                              (McCoy et al., 2023; Gendron et al., 2023). Despite this, a
                                                driving the external verifiers themselves can be ac-
                                                                                                              steady stream of claims continue to be made in the litera-
                                                quired with the help of LLMs. We will also argue
                                                                                                              ture about the planning and reasoning capabilities of LLMs.
                                                that rather than simply pipelining LLMs and sym-
                                                                                                              In light of questions about their planning capabilities, the
                                                bolic components, this LLM-Modulo Framework
                                                                                                              head-long rush into agentic LLMs should be particularly
                                                provides a better neuro-symbolic approach that
                                                                                                              concerning. After all, acting without the ability to plan is
                                                offers tighter integration between LLMs and sym-
                                                                                                              surely a recipe for unpleasant consequences!
                                                bolic components, extending the scope of model-
                                                based planning/reasoning regimes towards more                 In an ironic juxtaposition to this unwarranted optimism
                                                flexible knowledge, problem and preference spec-              about the planning and reasoning abilities of LLMs, there
                                                ifications.                                                   is also unwarranted pessimism about the roles LLMs can
                                                                                                              play in planning/reasoning tasks. Several efforts (e.g. (Liu
                                                                                                              et al., 2023; Pan et al., 2023; Xie et al., 2023)) advocate
                                         1. Introduction                                                      using LLMs only as glorified translators–converting rea-
                                                                                                              soning problems embedded in textual format to symbolic
                                         Large Language Models (LLMs), essentially n-gram models              representations, and pawning them off to external classical
                                         on steroids which have been pre-trained on web-scale lan-            symbolic solvers (with all their attendant expressivity and
                                         guage corpora (or, effectively, our collective consciousness),       search complexity challenges (Doyle & Patil, 1991)).2
                                         have caught the imagination of the AI research community
                                         with linguistic capabilities that no one expected text com-          In truth, LLMs can be a whole lot more than machine trans-
                                         pletion systems to possess. Their seeming versatility has                1
                                                                                                                    Think of asking an LLM an yes/no question–is this theorem
                                         led many researchers to wonder whether they can also do              logically entailed by this first-order logic knowledge-base. This
                                         well on planning and reasoning tasks typically associated            is well-known to be a semi-decidable problem. Ask yourself if
                                                                                                              the LLM will take longer in answering the question. (If you are
                                            1
                                             School of Computing and AI, Arizona State University,            thinking Chain-of-thought prompts or training with step-by-step
                                         Tempe, AZ, USA. Correspondence to: Subbarao Kambhampati              data, consider that you are essentially changing the nature of the
                                         <rao@asu.edu>.                                                       original prompt/training).
                                                                                                                  2
                                                                                                                    In some circles, this unidirectional pipeline has been given the
                                         Proceedings of the 41 st International Conference on Machine         undeserved badge of neuro-symbolic architecture.
                                         Learning, Vienna, Austria. PMLR 235, 2024. Copyright 2024 by
                                         the author(s).

                                                                                                          1
                                          LLM-Modulo Framework for Robust Planning

                                                                        ing our own works, that establishes that LLMs cannot be
                                                                        used as planners or plan verifiers themselves (Section 2).
                                                                        We also discuss why there are claims about planning/veri-
                                                                        fication abilities in the first place, in the process hopefully
                                                                        clarifying some prevalent misunderstandings.
                                                                        Second, we will propose a framework that allows us to
                                                                        leverage LLMs effectively in planning tasks, by combin-
                                                                        ing them with external critics, verifiers and humans. We
                                                                        call this an LLM-Modulo Framework (a name loosely in-
                                                                        spired by SAT Modulo Theories (Nieuwenhuis & Oliveras,
                                                                        2006)); see Figure 3. LLMs play a spectrum of roles in this
                                                                        architecture, from guessing candidate plans, to translating
Figure 1. An informal account of viewing an LLM as a giant exter-
                                                                        those plans into syntactic forms that are more accessible
nal non-veridical memory that acts as a pseudo System 1                 to external critics, to helping end users flesh out incom-
                                                                        plete specifications, to helping expert users acquire domain
                                                                        models (that in turn drive model-based critics). All this
lators. They are a kind of approximate knowledge source                 leveraging of LLMs is done without ascribing to them any
(albeit sans guarantees) trained on our collective conscious-           planning or verification abilities. The LLM ideas are vetted
ness. While it is unlikely that they will have System 2 com-            by external critics, thus ensuring that the plans generated
petencies by themselves, they can nevertheless be valuable              in this architecture can have formal correctness guarantees
resources in solving System 2 tasks. To put it another way,             where possible.
the problem with Alchemy of yore was not that Chemistry
is useless, but that people wanted to delude themselves that            2. Planning-centered Limitations of LLMs
Chemistry–a pretty amazing discipline on its own merits–
can be Nuclear Physics if you prompt it just so. The con-               In this section, we will first review literature that calls into
fusions regarding LLM abilities, or should we say, LLM                  question claims about the planning and self-verification
alchemy, doesn’t seem to be much different–oscillating be-              capabilities of LLMs. Subsequently, we will also provide
tween ignoring their strengths, and ascribing abilities they            some possible reasons for claims to the contrary made in
don’t have.                                                             the literature.

The goal of this position paper is to introduce some clarity            2.1. LLMs cannot generate executable plans in
into this confusing state of affairs oscillating between over-               autonomous mode
optimism and over-pessimism. Simply put, we take the
stance that LLMs are amazing giant external non-veridical               Despite initial claims about the planning capabilities of
memories that can serve as powerful cognitive orthotics for             LLMs (Bairi et al., 2023; Yao et al., 2023b; Shinn et al.,
human or machine agents, if rightly used. The underlying n-             2023; Huang et al., 2022; Hao et al., 2023) several recent
gram nature makes them effortlessly intermix what would be              studies confirm that LLMs are not actually able to generate
considered disparate fields of study (not surprisingly, LLMs            executable plans when they are used in autonomous modes
are seen to be very good at making/finding analogies!). The             (Valmeekam et al., 2023c; Liu et al., 2023; Silver et al.,
challenge is to leverage them without wrongly ascribing to              2022). For example, in (Valmeekam et al., 2023c;b), we
them capabilities they don’t possess. The LLM-Modulo                    evaluate LLMs’ ability to generate correct plans on a suite of
framework proposed in this position paper tackles this                  planning problem instances based on the kinds of domains
challenge.                                                              employed in the International Planning Competition (IPC,
                                                                        1998). To eliminate the subjective aspect of analysis that
For the sake of concreteness, we consider planning tasks,               forms the core part of many earlier efforts to evaluate the
especially as studied in the automated planning community               reasoning capabilities of LLMs, we leverage models and
(Ghallab et al., 2004). The central position of the paper is            tools from the automated planning community to automate
that LLMs cannot plan themselves but can play a variety                 evaluation.
of constructive roles in solving planning tasks–especially
as approximate knowledge sources and candidate plan gen-                We show that results in the autonomous mode are pretty
erators in so-called LLM-Modulo Frameworks, where they                  bleak. On average, only about 12% of the plans that the
are used in conjunction with external sound model-based                 best LLM (GPT-4) generates are actually executable without
verifiers.                                                              errors and goal-reaching. We show that the choice of LLM
                                                                        doesn’t have much bearing on this. We tested the family
We support this position by first reviewing literature, includ-

                                                                    2
                                        LLM-Modulo Framework for Robust Planning

              Domain         Method                                     Instances correct
                                         GPT-4o       GPT-4-          Claude-     LLaMA-        Gemini        GPT-4
                                                      Turbo           3-Opus       3 70B         Pro
                            One-shot     170/600      138/600          289/600     76/600        68/600      206/600
          Blocksworld
                                        (28.33%)       (23%)          (48.17%)    (12.6%)       (11.3%)      (34.3%)
          (BW)
                            Zero-shot    213/600      241/600         356/600      205/600       3/600       210/600
                                         (35.5%)      (40.1%)         (59.3%)     (34.16%)      (0.5%)       (34.6%)
          Mystery BW        One-shot      5/600        5/600            8/600      15/600        2/500        26/600
          (Deceptive)                    (0.83%)      (0.83%)          (1.3%)      (2.5%)       (0.4%)        (4.3%)
                            Zero-shot     0/600        1/600           0/600        0/600       (0/500)       1/600
                                          (0%)        (0.16%)          (0%)         (0%)         (0%)        (0.16%)

Table 1. Results of state-of-the-art LLMs GPT-4o, GPT-4-Turbo, Claude-3-Opus, Gemini Pro and LLaMA-3 70B for Plan Generation
with prompts in natural language.


of GPT LLMs including GPT-4 (OpenAI, 2023), GPT-3.5                 general, unless LLMs are trained not just on “correct data,”
(OpenAI, 2022), InstructGPT-3 (Ouyang et al., 2022) and             but also on “corrections data,” there is no a priori reason
GPT-3 (Brown et al., 2020). We also show that fine-tuning           to believe that their critiques would even be approximately
does not seem to have a major effect on this dismal perfor-         relevant, let alone actually correct.
mance. We demonstrate that the performance deteriorates
                                                                    Two of our studies–one on plan verification (Valmeekam
further if the names of the actions and objects in the domain
                                                                    et al., 2023a) and the other on CSP verification (Stechly
are obfuscated–a change that doesn’t in any way affect the
                                                                    et al., 2023) seem to throw cold water on this optimism.
performance of the standard AI planners. This further sug-
                                                                    In (Stechly et al., 2023), we systematically investigate the
gests that LLMs are more likely doing approximate retrieval
                                                                    effectiveness of iterative prompting in the context of Graph
of plans than actual planning.
                                                                    Coloring, a canonical NP-complete reasoning problem. Our
We continue to reconfirm these limitations over each of             methodology involves a principled empirical study of the
the more recently released LLMs, including Claude Opus,             performance of GPT4 on two tasks: solving a large suite of
Gemini, GPT4-Turbo and GPT4-o. Table 1 shows that                   random graph coloring instances and, separately, verifying
all the state of the art LLMs show dismal performance on            the correctness of the candidate colorings–both in direct
PlanBench (Valmeekam et al., 2023b).                                (i.e., return the first solution generated by the LLM) and
                                                                    iterative modes. In iterative modes, we experiment both
More recently, we have also investigated so-called “chain
                                                                    with an LLM critiquing LLM-produced solutions and an
of thought” prompting (Stechly et al., 2024b), as well as
                                                                    external, guaranteed correct reasoner verifying solutions. In
ReAct-style step-by-step prompting (Verma et al., 2024a)
                                                                    both cases, we analyze whether the content of criticisms ac-
and found that they too are largely ineffective in improving
                                                                    tually affects bottom-line performance. A more recent paper
the planning performance of LLMs.
                                                                    further analyzes these results along with performance on
                                                                    the 24 puzzle–a task that has been used by some researchers
2.2. LLMs cannot verify plans and thus cannot improve               claiming LLMs have the ability to self verify (Stechly et al.,
     by self-critiquing                                             2024a).
There still exists considerable optimism that even if LLMs          Our results indicate that in direct mode, LLMs are, perhaps
can’t generate correct solutions in one go, their accuracy          not surprisingly, pretty bad at solving graph coloring in-
might improve in an iterative prompting regime, where               stances. More interestingly, they are no better at verifying
LLMs will be able to “self-critique” their candidate so-            solutions. In iterative modes, given the inability of LLMs to
lutions and refine them to the point of correctness (Yao            verify solutions, it should come as no surprise that our exper-
et al., 2023b;a; Shinn et al., 2023; Weng et al., 2023; Huang       iments also show that the strategy of LLMs self-critiquing
et al., 2022). This belief seems to rest largely on the as-         their solutions does not improve over the baseline. We re-
sumption that verification of correctness should be easier          port that the performance is in fact worse because the system
than generation for many reasoning problems–a rather clas-          can’t recognize a correct coloring and thus merrily passes
sical argument from computational complexity. There are             over fortuitously correct colorings it has generated, ending
grounds to be skeptical of this assumption as the complexity        up with a wrong one! Similar results have also been reported
of the reasoning task should be irrelevant to LLM perfor-           for planning problems in (Valmeekam et al., 2023c).
mance if what they are doing is approximate retrieval. In


                                                                3
                                            LLM-Modulo Framework for Robust Planning

One important corollary of the fact that LLMs cannot self-
critique their plans is that they also can’t self-improve by
generating synthetic data, e.g. by generating plans them-
selves, critiquing the plans by themselves to improve them,
and then using those to fine-tune themselves, as has been
claimed in the literature (Huang et al., 2023b; Wang et al.,
2022)3 .

2.3. Analyzing Claims to the Contrary in the Literature
Given that LLMs can neither guarantee correct generation
nor correct verification of plans, as discussed in the previous
sections, one obvious question is why the literature is replete
with claims contrary to this (Bairi et al., 2023; Yao et al.,               Figure 2. Viewing LLMs as an approximate knowledge source
2023b; Shinn et al., 2023; Yao et al., 2023a; Weng et al.,                  trained over civilizational knowledge
2023; Huang et al., 2022).
                                                                            models, then the ability of LLMs to guess executable plans
Claims about Planning: To analyze planning claims, we                       improves. Without these assumptions or mitigations, the
need to first understand that solving planning tasks requires               plans that come out of LLMs may look reasonable to the lay
(a) having the necessary planning domain knowledge–the ac-                  user, and yet lead to execution time interactions and errors.5
tions and their preconditions, effects; the standard hierarchi-
                                                                            Claims about Self-Verification: Coming to the claims
cal recipes (e.g. task reduction schemas in HTN planning),
                                                                            about LLM’s self-verification abilities, a closer look at the
past cases/plans, etc., and (b) being able to assemble this
                                                                            literature (Yao et al., 2023a; Huang et al., 2023a) shows
planning knowledge into an executable plan that takes care
                                                                            that those claims are either (i) made in the context of tacit
of any subgoal/resource interactions. The first part can be
                                                                            knowledge tasks for which there is little possibility of a ver-
called knowledge acquisition and the second reasoning/plan-
                                                                            ifier (e.g. essay writing)–making it hard to evaluate whether
ning. On closer examination, many papers claiming LLMs
                                                                            LLM’s critiquing actually helped or (ii) the external verifica-
have planning abilities wind up confusing general planning
                                                                            tion is carried out either by simulators (Wang et al., 2023b;
knowledge extracted from the LLMs for executable plans.
                                                                            Yao et al., 2023b) or simple calls to the underlying operating
When all we are looking for are abstract plans, such as “wed-
                                                                            system.
ding plans,” with no intention of actually executing them,
it is easy to confuse them for complete executable plans.                   In a related vein, there is the recent Tree of Thoughts (ToT)
Indeed, our close examination of several works claiming                     paper (Yao et al., 2023a), which has been pitched as a way to
planning capabilities for LLMs (Kambhampati et al., 2023)                   convert LLMs into some type of systematic search with self-
suggests that they either work in domains/tasks where sub-                  verification. Specifically, ToT employs a problem-specific
goal interactions can be safely ignored (Yao et al., 2023b;                 prompt priming method. The “tree” in ToT is essentially a
Shinn et al., 2023)4 –either because they are just working on               way to generate diverse priming prompts (that the authors
a single subgoal, or because the world is forgiving and er-                 set up in a problem specific way). In other words, despite
godic; or by delegating the interaction resolution (reasoning)              the use of terminology of problem-solving agents (Russell
to the humans in the loop (who, through repeated prompting,                 & Norvig, 2010)–search tree, expansion etc., there is really
have to “correct” the plan). Sometimes, in common sense                     no deeper connection to search-based agents.
domains, or with enough fine-tuning, the “assembling” part
                                                                            The guarantees–if any–are coming in terms of soundness of
may also be obviated by having seen a case that pretty much
                                                                            the external verifier. The one clear reasoning problem used
corresponds to the problem that needs to be solved. Not
                                                                            in the ToT paper is the 24 puzzle–for which the external
surprisingly, our work (Valmeekam et al., 2023c) shows that
                                                                            verifier can be easily implemented in terms of arithmetic
if the action interactions are removed by relaxing the world
                                                                            operations (thankfully not done by the numerically chal-
    3
      Contrary to their claim of “self-improvement”, works like             lenged LLM!). Here, our experiments show that the LLM’s
(Wang et al., 2022) actually heavily depend on external knowledge           own criticisms are often quite off the mark.6 Because the
(crafted seed examples) and critics (filtering step).
    4                                                                          5
      Although domains like AlfWorld (Shridhar et al., 2021) do                  These issues are illustrated in part by a recent news story
have sub-goal interactions for successful task completion, (Yao             (Kugel & Hiltner, 2023) about the proliferation of travel planning
et al., 2023b) and (Shinn et al., 2023) largely ignore these interac-       books, mostly auto-extracted from LLMs, and the ensuing disap-
tions by either focusing on single subgoals or relying on the ergodic       pointment of the unsuspecting end users who buy them mistaking
nature of the domain when prompting LLMs for generating plans               them for usable plans!
                                                                               6
(Verma et al., 2024a).                                                           Note that we can do this check easily because of the formal
                                                                            specification of correctness. For the “improving writing task” also

                                                                        4
                                             LLM-Modulo Framework for Robust Planning




Figure 3. The proposed LLM-Modulo framework where LLMs act as idea generators and various external critics that specialize in different
aspects, critique the candidate plan.


24 puzzle’s solutions can be verified by simple arithmetic                  proaches that accept domain knowledge from human experts
operations, it is trivial to implement an external verifier for             that can be termed “Polanyi’s Revenge” (c.f. (Kambham-
these problems. In general though, the verifier may be more                 pati, 2021)), this new trend of using LLMs as knowledge
complex and can involve substantial work (you can substi-                   sources can be viewed as a form of avenging Polanyi’s re-
tute a simulator for the verifier–but someone has to write                  venge! Indeed, LLMs make it easy to get problem-specific
that simulator too!).                                                       knowledge as long as we are willing to relax the correct-
                                                                            ness requirements of that knowledge. In contrast to the old
LLMs as Approximate Knowledge Sources: The fact
                                                                            knowledge engineering approaches, LLMs offer this with-
that LLMs are often good at extracting planning knowledge
                                                                            out making it look like we are inconveniencing any specific
can indeed be gainfully leveraged. As shown in recent
                                                                            human (we are, instead, just leveraging everything humans
works (Guan et al., 2023), LLMs can be a rich source of
                                                                            told each other on the Web!). So the million dollar question
approximate models of world/domain dynamics and user
                                                                            for reasoning tasks is: “how would you do robust planning
preferences, as long as the humans (and any specialized
                                                                            if you have some doddering know-it-all ready to give you
critics) in the loop verify and refine those models, and give
                                                                            any kind of knowledge?” The LLM-Modulo Framework is a
them over to model-based solvers. This way of using LLMs
                                                                            principled method for tackling this challenge.
has the advantage that the humans need only be present
when the dynamics/preference model is being teased out
and refined, and the actual planning after that can be left to              3. LLM-Modulo Framework for Robust
sounder planning frameworks with correctness guarantees,                       Planning
such as the LLM-Modulo framework we propose.
                                                                            While Section 2 questions the claims that LLMs are ca-
Such an overall approach has striking similarities to                       pable of planning/reasoning by themselves, it is certainly
knowledge-based AI systems of yore, with LLMs effectively                   not meant to imply that LLMs don’t have any constructive
replacing the “knowledge engineer” (see Figure 2). Given                    roles to play in solving planning/reasoning tasks. On the
the rather quixotic and dogmatic shift of AI away from ap-                  contrary, as discussed in the Introduction, their uncanny
used in ToT, there are no formal quality metrics and so it is hard to       ability to generate ideas/potential candidate solutions–albeit
say anything concrete about the critiques of the LLM.                       with no guarantees about those guesses–can be valuable in


                                                                        5
                                        LLM-Modulo Framework for Robust Planning

the generate-test-critique setups in conjunction with either          lem specification in concert with the LLM. A notable, and
model-based verifiers or expert humans in the loop. Accord-           deliberate, absence is human’s involvement in the inner loop
ingly, we propose a general “LLM-Modulo” framework7 .                 of planning–e.g. with iterative prompting. In addition to
While we believe that versions of such an architecture can be         posing an infeasible burden on the human’s time for com-
of use in a wide variety of planning or reasoning tasks, for          plex planning problems, such iterative prompting strategies
the sake of concreteness, we will focus on planning tasks,            are notorious for their Clever Hans effect (cle).
especially of the type studied in the automated planning
community (Ghallab et al., 2004).                                     3.1. Critics/Verifers
Figure 3 gives a schematic of the LLM-Modulo Frame-                   In the LLM-Modulo framework, critics can evaluate LLM-
work, as we envision it. As can be seen readily, the un-              generated candidates for a planning/reasoning problem over
derlying architecture is a Generate-Test-Critique loop, with          both hard and soft (style) constraints. Hard constraints refer
the LLM generating candidate plans and a bank of critics              to correctness verification which can include causal correct-
critiquing the candidate. The loop starts with the LLM get-           ness, timeline correctness, resource constraint correctness
ting the problem specification and generating its first plan          as well as unit tests. For PDDL planning problems, the
candidate.8 Note that the plans an LLM helps generate in              hard critic can be based on VAL (Howey et al., 2004), that
this architecture have soundness guarantees because of the            works off of a model (which itself can be acquired with the
external sound critics. This means that plans coming out              help of the LLM (Guan et al., 2023). It is worth noting that
of such an compound system will constitute a better corpus            the critics don’t always have to be declarative model-based
of synthetic data for any fine tuning phase carried out to            ones, and can be simulators. Just as LLMs can help humans
improve/customize the LLM’s generation capability. The                in coming up with models, they can also help in writing
completeness of the system depends on the LLM’s ability               procedural simulators, as seems to be done in systems like
to generate all potentially relevant candidates.                      Voyager (Wang et al., 2023a).
Design Choices: Before going into the details about the               On the other hand, soft constraints can include more abstract
framework and its various modules, it is worth noting                 notions of good form such as style, explicability, preference
some design decisions underlying the proposed architecture.           conformance, etc. As discussed in Section 2.3, while LLMs
We start by noting that the LLM-Modulo architecture is a              cannot take on the role of hard critics with soundness guaran-
“Generate-Test” one that involves LLMs interacting with the           tees,9 they can help simulate some aspects of the role of soft
external critics/verifiers rather than a LLMs being just front-       (style) critics. So our framework does allow for style critics
ends to external solvers. This is a deliberate decision–as this       be possibly based on LLMs. For example, in (Verma et al.,
allows the LLM to guess/generate candidates to satisfy the            2024b) we discuss how LLMs can act as a human proxy to
critics, as against dealing with the expressiveness and search        evaluate plans in terms of how they would be perceived by
complexity issues of the solvers. The critics/verifiers also          humans in the loop. Additionally, in (Guan et al., 2024), we
are also more naturally composable than solvers/planners.             show how Vision-Language Models (VLMs) can be lever-
As we shall see, we do allow for constructive critics which           aged to critique the style of robot behaviors in terms of
can be based on solvers, and provide suggestions on specific          their adherence to the soft common-sense preferences of the
ways of extending/modifying the candidate plans.                      humans in the loop. We reiterate that the soundness of the
Secondly, the framework explicitly recognizes that the                LLM-modulo framework is inherited from the soundness of
LLMs can generate approximate ideas not just about plan               the correctness (hard) critics.
candidates, but domain models, problem reduction strate-              The bank of critics–hard (model-based) as well as soft (pos-
gies, and refinements to the problem specification. The               sibly LLM-based) evaluate the current plan candidate to
framework also recognizes that LLMs are good at for-                  evaluate its fitness/acceptability. If at least all the hard crit-
mat/syntax changes. Accordingly, the framework lever-                 ics sign off on the current candidate, then that is considered
ages all these abilities of LLMs, letting them play multiple          a valid solution to be returned to the end-user or the ex-
roles in planning. Finally, the architecture carefully circum-        ecutor. When a critic finds the current plan candidate to
scribes the human’s role–domain experts interact with the             be unsatisfactory, it can provide varying levels of feedback,
LLM to tease out the models used by (some of) the critics,            ranging from “No, try again” to “No, try again, here is one
while end users take part in refining any incomplete prob-            thing wrong with the current plan” to “No, try again, here
    7                                                                 are all the things wrong with the current plan.” More impor-
      The name LLM-Modulo is inspired by the SAT-Modulo theo-
ries (Nieuwenhuis & Oliveras, 2006).                                  tantly, the critics can be constructive, and offer alternatives
    8
      Although we focus on planning from scratch, it is easy to           9
                                                                            If we don’t insist on soundness guarantees, then it is, in prin-
accommodate replanning scenarios, where the loop starts with an
                                                                      ciple, possible to train LLMs discriminatively to learn to verify
externally supplied candidate plan.
                                                                      plans; see (Arora & Kambhampati, 2023).


                                                                  6
                                         LLM-Modulo Framework for Robust Planning

plan/subplan suggestions. One way of obtaining such con-               interactions. In the former category, human domain experts
structive critics is to base them on partial planners–operating        can play a role in acquiring the domain model with the
either on the models themselves or their relaxations (Bryce            help of the LLM. Examples of such interaction include
& Kambhampati, 2007).These critiques are all pooled at the             teasing out PDDL planning models from the LLMs with
Meta (Backprompt) Controller (see Section 3.2)                         the help of human expert curation (top left in Figure 3). An
                                                                       example of this is our work in (Guan et al., 2023). The idea
LLMs as Reformulators: One interesting challenge is that
                                                                       here is that the traditional domain model acquisition task
many of the symbolic model-based verifiers tend to be oper-
                                                                       (e.g. (Simpson et al., 2001)) is significantly made easier by
ating on specialized formal representations. Given a central
                                                                       having the LLMs help with ideas regarding various pieces
candidate plan (e.g. a mission plan), these critics need trans-
                                                                       of the domain model (e.g., actions, their preconditions and
lations of that candidate into their representations. This is
                                                                       effects) and letting humans sign off/critique the resulting
the role of the reformulator module attached to individual
                                                                       model. Once the model is acquired this way, it can be used
critics. These reformulator modules can be supported to
                                                                       by correctness verifiers such as VAL (Howey et al., 2004;
a large extent by LLMs, given that one thing LLMs are
                                                                       Guan et al., 2023). Often the planning problems in real
very good at is format change across different syntactic rep-
                                                                       world situations are specified incompletely, leaving it to the
resentations (Olmo et al., 2021). Indeed, as discussed in
                                                                       human commonsense to refine the specification. This brings
Section 1, some approaches to combine LLMs with external
                                                                       up a second role for humans–this time end users (bottom
symbolic solvers just use LLMs as reformulators for these
                                                                       left in Figure 3–in collaboratively refining the specification
solvers (Liu et al., 2023; Pan et al., 2023). It is worth noting
                                                                       with the help of LLMs (similar to the way done in (Xie et al.,
that the syntax conversion itself can be helped with a nested
                                                                       2023; Liu et al., 2023)).
LLM-Modulo framework–where the syntactic correctness
of the conversion is checked by syntax critics. We will
have occasion to illustrate this in the context of our prelimi-        3.4. Summary of LLM Roles in LLM-Modulo
nary work on LLM-Modulo frameworks for travel planning                 It is worth summarizing the multiple roles the LLM plays
discussed in Section 4. Our discussion of LLM-Modulo                   in the LLM-Modulo architecture. The most prominent, of
framework should make it clear that syntax reformulation               course, is its role in “guessing” the candidate plans (step 2 in
alone is a severely limited role for LLMs!                             Figure 3) in response to problem specification and iterative
                                                                       back prompting from the bank of critics (Step 5). Second,
3.2. Backprompt (Meta) Controller                                      the LLM plays a role in converting the guessed plan can-
                                                                       didate into specialized representations used by the various
The critiques from the various critics are pooled together by
                                                                       critics (e.g., the time-line view, the causal link view etc.).
the Meta (Backprompt) Controller, which passes a processed
                                                                       This role leverages the fact that LLMs are very good at for-
version of them to the LLM as the next iterative prompt to
                                                                       mat conversion (c.f. (Olmo et al., 2021)). Third, the LLM
elicit the next guess. This is especially required in the
                                                                       plays a role in helping the end user flesh out the incomplete
presence of a mix of soft and hard critics, where the Meta
                                                                       problem specification to begin with (Step 1 in Figure 3).
Controller can assume the responsibility of compiling the
                                                                       Finally, the LLM plays a role in helping the domain expert
critiques into a consistent feedback to send to the LLM.
                                                                       tease out and refine the domain models used by the various
The processing in the controller can range from (i) simple             model-based critics (Guan et al., 2023; Kwon et al., 2022),
round-robin selection of prompts to (ii) generating a summa-           or help “implement” procedural critics (such as those check-
rized prompt (with LLM help) to (iii) employing a prompt               ing syntactic constraints). As a broad approximate source
diversification strategy to elicit the next candidate from a           of knowledge, the LLM can also help enumerate the list of
different part of the implicit search space. This last strategy        potential critics needed to validate the candidate plans (once
helps increase the completeness of the LLM candidate gen-              again with a human in the loop).
eration, and may involve domain/task-specific knowledge
(see the discussion of Tree of Thoughts in Section 2.3).               3.5. Can LLM-Modulo Frameworks Pay Their Way?
                                                                       Let’s address the elephant in the room: Given that formal
3.3. Specification Refinement & Critic/Model
                                                                       model-based planning systems already exist (Ghallab et al.,
     Acquisition
                                                                       2004), is LLM-Modulo framework for planning more than
As mentioned earlier, we avoid having humans involved                  a gratuitous attempt to shoe-horn (the currently popular)
in iteratively prompting LLMs–as this can be an infeasibly             LLMs to solve planning problems? Indeed, when the under-
time-consuming activity for them. Instead, we let automated            lying problem is actually solvable by such combinatorial
verifiers, either model-based or LLM-supported, to manage              solvers, it can be orders of magnitue more resource efficient
the plan critiquing process. The framework does depend
on humans for “once per domain” and “once per problem”

                                                                   7
                                          LLM-Modulo Framework for Robust Planning

                                                                        4. Two Case Studies of LLM-Modulo
                                                                        We have applied the LLM-Modulo framework to classical
                                                                        planning domains (as reported in (Valmeekam et al., 2023c))
                                                                        and to a recent travel planning benchmark (as reported in
                                                                        (Gundawar et al., 2024)). In the former case, the results
                                                                        (presented in Section 5.2 and Table 4 of (Valmeekam et al.,
                                                                        2023c)) show that with back prompting from VAL (Howey
                                                                        et al., 2004) acting as the external verifier and critic, LLM
                                                                        performance in Blocks World improves to 82% within 15
                                                                        back prompting rounds, while in Logistics, it improves to
                                                                        70%. LLM-Modulo doesn’t help as much in an obfuscated
Figure 4. LLM Modulo Framework adapted for Travel Planning              version of blocks world called Mystery BW, reaching about
                                                                        10% accuracy. This should be expected because the LLMs
                                                                        have difficulty generating plausible candidate plans for this
                                                                        domain (note that even here, if a plan is returned, it must
                                                                        have passed muster with VAL, and is thus guaranteed correct
                                                                        by its model).
                                                                        For the travel planning case study, we used a benchmark
                                                                        proposed in (Xie et al., 2024), which involves a rich mix
                                                                        of travel constraints presented in flexible natural language
                                                                        form. Our preliminary results on adapting LLM-Modulo
                                                                        framework to this benchmark are reported in (Gundawar
                                                                        et al., 2024). The benchmark’s authors test LLMs across a
Figure 5. Final Pass rates of models across LLM Modulo Iterations       variety of prompt engineering techniques including Chain of
                                                                        Thought and ReAct, reporting that–on GPT-3.5-Turbo–the
to use them.10 Compared to a planner that is guaranteed                 current best strategies only manage a startlingly low 0.7%
to be correct in a narrow set of domains, LLMs may likely               performance rate! We adapted the LLM-Modulo framework
be good at generating plausible (but not guaranteed to be               to this benchmark by operationalizing their hard constraints
correct) plan heuristics/suggestions in many more scenarios.            (such as the budget constraint set by the user) or common-
Thus, unlike the traditional planning architectures studied             sense constraints (such as suggesting diverse attractions to
in AI (Ghallab et al., 2004), which put a priori constraints            visit) as critics as shown in Figure 4. Our preliminary re-
on the expressiveness of the problems that can be posed to              sults show (see Figure 5; additional results in (Gundawar
the planner (to wit, the different expressiveness levels of the         et al., 2024)) that LLM-Modulo based agentification with
PDDL specification (McDermott et al., 1998)), the LLM-                  automated critics in the loop significantly improves the per-
Modulo architecture puts no such restrictions. In this sense,           formance (6x of baselines) even with a limit of 10 back
it is more representative of real-world planning problems               prompting cycles, and weaker models such as GPT-3.5-
such as those in NASA mission planning, where the differ-               turbo. Furthermore, we also find that LLMs can success-
ent critics–human and automated–are at best able to give                fully implement functions corresponding to hard critics and
“no objection” certificates for the candidate plans under con-          several common-sense critics. Finally, LLMs reliably play
sideration, clearing it from their perspective. (Indeed, both           the role of reformatter as well, converting free form travel
deep space network planning and mars rover task planning                plans into structured plans parseable by the critics for back-
are done via a collective human blackboard. (Johnston et al.,           prompts or plan evaluation. One interesting observation
2014; Bresina et al., 2004).) Note that this is starkly differ-         about this domain is that we were able to use the LLM itself
ent from just sending an unvetted plan out to execution (as             to enumerate the type of critics needed to validate the plan
would be the case if we have LLMs operate in autonomous                 (with light human supervision).
mode to guess plans). Generalizing planning and reasoning
frameworks this way is consistent with the Doyle & Patil’s              5. Related Work
call to the Knowledge Representation community of yore
(Doyle & Patil, 1991), as well as our own call for model-lite           While the LLM-Modulo framework is being proposed in
planning (Kambhampati, 2007).                                           general form here for the first time, there are certainly works
  10
                                                                        in leveraging LLMs in planning and reasoning tasks that are
     Not surprisingly, automated programming, the one community
that certainly doesn’t have the luxury of a ready-made “solver,”
                                                                        in line with the spirit of the LLM-Modulo framework. Work
have stuck to LLM-Modulo style approaches.                              on FunSearch (Romera-Paredes et al., 2023) depends on a

                                                                    8
                                        LLM-Modulo Framework for Robust Planning

generate-test loop between a specially fine-tuned LLM that           with the help of simulator.
guesses solutions, and an external symbolic evaluator that
                                                                     Although we focused on text based LLMs (such as GPT4),
critiques them. The authors note how the external verifier
                                                                     recently there have also been impressive development in
is critical for avoiding falling prey to hallucinations (i.e.,
                                                                     multi-modal LLMs (e.g. GPT4V). While multi-modality is
approximate solution candidates that have flaws). Alpha-
                                                                     a great addition that increases the coverage of their System
Geometry (Trinh et al., 2024) too depends on the Generate-
                                                                     1 imagination (Figure 1), it is not clear that this gives them
Test-Critique interaction between a fine-tuned LLM and a
                                                                     System 2 competence.11 As we discussed earlier, we can
symbolic evaluator. Both these systems fine-tune pre-trained
                                                                     leverage VLMs for style criticism of the robot behavior
LLMs with task specific synthetic data–the correctness of
                                                                     (Guan et al., 2024).
which is vetted with external simulators.
                                                                     Finally, our position (with published supporting evidence)
While we focused on PDDL planning tasks for the sake of
                                                                     that LLMs are incapable of supporting planning in au-
concreteness, we believe that the essence of LLM-Modulo
                                                                     tonomous modes must seem quite at odds with the current
framework is equally applicable to other scenarios involving
                                                                     head-long rush into agentic LLMs. We believe that the
planning and reasoning–such as Reinforcement Learning
                                                                     latter is largely a result of confusing “acting” with “plan-
with Simulators. Such RL systems rely on rewards as feed-
                                                                     ning.” Given their ability to translate across formalisms, it
back to train a policy. Simulators takes on the roles of plan
                                                                     is of course possible for LLMs to invoke external services–
evaluation and critiques performed by the respective crit-
                                                                     something frameworks like AutoGPT and LangChain sup-
ics in the LLM-Modulo framework (e.g. (Rajvanshi et al.,
                                                                     port. But the mere ability to invoke an action doesn’t, in any
2023)). The fact that simulators play the role of verifiers
                                                                     way, guarantee that the course of actions thus invoked will
is often not explicitly recognized in cases where LLMs are
                                                                     achieve a desired state of affairs. The only way to guaran-
used as an actor to generate an admissible plan by interact-
                                                                     tee the latter is to to support robust planning capabilities–
ing with a simulator, for example in the case of AlfWorld
                                                                     something our LLM-Modulo frameworks strive to do.
(Yao et al., 2023b; Shinn et al., 2023) and Minecraft (Wang
et al., 2023b). Similar to extracting a domain model such as
in the case of (Guan et al., 2023), LLMs can also be used for        6. Conclusion
designing a reward model or shaping the reward (Bhambri
                                                                     This position paper is a modest attempt to combat both over-
et al., 2024; Kwon et al., 2022; Hao et al., 2023; Ma et al.,
                                                                     optimism and over-pessimism about the role of LLMs in
2023).
                                                                     planning and reasoning tasks. Our position is that LLMs can-
Interestingly, the fact that LLM’s can help come up with ap-         not plan themselves but can play a variety of constructive
proximate quasi-symbolic transition models, reward models            roles in solving planning tasks–especially as approximate
and models of high level actions has made a bigger splash            knowledge sources and candidate plan generators in the so-
in RL. This is because for far too long, researchers there           called LLM-Modulo Frameworks in conjunction with exter-
have tried to spurn any high level models (lest that would           nal sound model-based verifiers. In support of this position,
involve depending on humans; (Kambhampati, 2021)) and                we summarized the literature questioning the claims about
focused on learning to act from sensory information, under           the planning and self-verification capabilities of LLMs by
the name of “deep reinforcement learning.” Given the hor-            themselves. We also discussed how conflating approximate
rendous sample complexity of the DRL methods even in                 knowledge acquisition and generating executable plans of
reaching a single subgoal, and the well known fact that even         action is behind many of the claims about planning and ver-
approximate symbolic models can help drastically improve             ification abilities of LLMs. We then shared LLM-Modulo
the performance (c.f. (Guan et al., 2022)), coupled with the         framework, our vision for a productive way to integrate
fact that LLM’s are only too glad to dream up approximate            the impressive idea generation/approximate knowledge pro-
models and goal recipes, there has been a performance revo-          vision capabilities of LLMs with external verifiers with
lution of sorts there (Yao et al., 2023b; Liang et al., 2023;        correctness guarantees, for robust and expressive planning.
Wang et al., 2023b). If we look beyond the improvements              We discussed how planning in LLM-Modulo framework
in these lower level goal seeking behaviors–especially in            avoids inheriting the expressiveness and search-complexity
the presence of ergodic simulators, the RL approaches de-            limitations of traditional symbolic planners, while retaining
pendent on LLMs will encounter the same issues regarding             their soundness guarantees. We illustrated and discussed the
subgoal interactions that our discussion of PDDL planning            many roles LLMs can play in the LLM-Modulo framework.
problems brought into focus. The LLM-Modulo inspired                 Finally, we also discussed two case studies of adapting the
frameworks will thus, we believe, be equally relevant there.         LLM-Modulo frameworks.
Indeed, SayCan (Ahn et al., 2022) the earliest use of LLMs             11
in generating policies in an RL-with-Simulator scenario,                 If you know how to complete sentences, and now learned to
                                                                     complete dance moves, does your ability to reason/plan magically
explicitly filters the action choices suggested by the LLM           improve?

                                                                 9
                                        LLM-Modulo Framework for Robust Planning

Impact Statement                                                         S. Efficient reinforcement learning via large language
                                                                         model-based search, 2024.
This position paper takes a stance on a robust and well-
founded way of leveraging Large Language Models in plan-               Bresina, J. L., Jónsson, A. K., Morris, P. H., and Rajan,
ning and reasoning tasks. It (i) points out the inabilities              K. Activity planning for the mars exploration rovers. In
of current pre-trained LLMs to tackle planning problems,                 ICAPS-2005 Conference, 2004.
(ii) suggests some reasons as to why there are wide-spread
                                                                       Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D.,
misunderstandings about LLM planning abilities and (iii)
                                                                         Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
proposes LLM-Modulo frameworks as a way to leverage
                                                                         Askell, A., et al. Language models are few-shot learners.
LLMs for robust planning. The main consequences of realiz-
                                                                         Advances in neural information processing systems, 33:
ing this position/vision is expected to be (i) sounding caution
                                                                         1877–1901, 2020.
about misapplication of LLMs in autonomous modes for
planning (ii) providing a way to leverage LLMs to do ro-               Bryce, D. and Kambhampati, S. A tutorial on planning
bust planning. Given the current interest in agentic LLMs,               graph based reachability heuristics. AI Mag., 28(1):47–
these insights can have significant positive impact in mis-              83, 2007.
sion critical situations. We do not see any obvious negative
                                                                       Bubeck, S., Chandrasekaran, V., Eldan, R., Gehrke, J.,
societal consequences of leveraging LLMs this way (unless
                                                                         Horvitz, E., Kamar, E., Lee, P., Lee, Y. T., Li, Y.,
of course the plans are aimed at achieving malicious goals).
                                                                         Lundberg, S., et al. Sparks of artificial general intel-
                                                                         ligence: Early experiments with gpt-4. arXiv preprint
Acknowledgments                                                          arXiv:2303.12712, 2023.
The ideas discussed in this paper have evolved over a se-              Doyle, J. and Patil, R. S. Two theses of knowledge represen-
ries of talks, tutorials and twitter threads. The discussions,           tation: Language restrictions, taxonomic classification,
feedback and encouragement from colleagues, including                    and the utility of representation services. Artificial intelli-
Sarath Sreedharan, Tom Dietterich, Yann LeCun, Daniel                    gence, 48(3):261–297, 1991.
Borrajo, and Dan Weld is gratefully acknowledged. The
adaptation of LLM-Modulo Framework for Travel Plan-                    Dziri, N., Lu, X., Sclar, M., Li, X. L., Jiang, L., Lin,
ning, discussed in Section 4 was lead by Atharva Gundawar.               B. Y., Welleck, S., West, P., Bhagavatula, C., Bras, R. L.,
Kambhampati acknowledges generous support from ONR                       Hwang, J. D., Sanyal, S., Ren, X., Ettinger, A., Harchaoui,
via grants N00014-18-1-2442, N14-18-1-2840 and N00014-                   Z., and Choi, Y. Faith and fate: Limits of transformers on
23-1-2409, as well as gifts from J.P. Morgan, Qualcomm                   compositionality. In Thirty-seventh Conference on Neu-
and Amazon.                                                              ral Information Processing Systems, 2023. URL https:
                                                                        //openreview.net/forum?id=Fkckkr3ya8.

References                                                             Gendron, G., Bao, Q., Witbrock, M., and Dobbie, G.
                                                                         Large language models are not abstract reasoners. arXiv
Clever Hans. https://en.wikipedia.org/wiki/Clever Hans.                  preprint arXiv:2305.19555, 2023.

Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O.,              Ghallab, M., Nau, D., and Traverso, P. Automated Planning:
  David, B., Finn, C., Fu, C., Gopalakrishnan, K., Hausman,              theory and practice. Elsevier, 2004.
  K., et al. Do as i can, not as i say: Grounding language             Guan, L., Sreedharan, S., and Kambhampati, S. Lever-
  in robotic affordances. arXiv preprint arXiv:2204.01691,               aging approximate symbolic models for reinforcement
  2022.                                                                  learning via skill diversity. In Chaudhuri, K., Jegelka, S.,
                                                                         Song, L., Szepesvari, C., Niu, G., and Sabato, S. (eds.),
Arora, D. and Kambhampati, S. Learning and leveraging                   Proceedings of the 39th International Conference on Ma-
  verifiers to improve planning capabilities of pre-trained              chine Learning, volume 162 of Proceedings of Machine
  language models. ICML Workshop on Knowledge and                       Learning Research, pp. 7949–7967. PMLR, 17–23 Jul
  Logical Reasoning in the Era of Data-driven Learning                   2022. URL https://proceedings.mlr.press/
  (arXiv preprint arXiv:2305.17077), 2023.                              v162/guan22c.html.
Bairi, R., Sonwane, A., Kanade, A., Iyer, A., Parthasarathy,           Guan, L., Valmeekam, K., Sreedharan, S., and Kambham-
  S., Rajamani, S., Ashok, B., Shet, S., et al. Codeplan:                pati, S. Leveraging pre-trained large language models
  Repository-level coding using llms and planning. arXiv                 to construct and utilize world models for model-based
  preprint arXiv:2309.12499, 2023.                                       task planning. In Thirty-seventh Conference on Neural
                                                                        Information Processing Systems, 2023. URL https:
Bhambri, S., Bhattacharjee, A., Liu, H., and Kambhampati,               //openreview.net/forum?id=zDbsSscmuj.

                                                                  10
                                        LLM-Modulo Framework for Robust Planning

Guan, L., Zhou, Y., Liu, D., Zha, Y., Amor, H. B., and                 Kambhampati, S. Polanyi’s revenge and AI’s new romance
  Kambhampati, S. ”task success” is not enough: Inves-                   with tacit knowledge. Communications of the ACM, 64
  tigating the use of video-language models as behavior                  (2):31–32, 2021.
  critics for catching undesirable agent behaviors, 2024.
                                                                       Kambhampati, S. Can LLMs reason and plan? Annals of
Gundawar, A., Verma, M., Guan, L., Valmeekam, K., Bham-                  the New York Academy of Sciences, 2024.
  bri, S., and Kambhampati, S. Robust planning with llm-
  modulo framework: Case study in travel planning. arXiv               Kambhampati, S., Valmeekam, K., Marquez, M., and Guan,
  preprint arxiv:2405.20625, 2024.                                       L. On the role of large language models in planning,
                                                                         July 2023. URL https://yochan-lab.github.
Hao, S., Gu, Y., Ma, H., Hong, J. J., Wang, Z., Wang, D. Z.,             io/tutorial/ICAPS-2023/. Tutorial presented at
  and Hu, Z. Reasoning with language model is planning                   the International Conference on Automated Planning and
  with world model. arXiv preprint arXiv:2305.14992,                     Scheduling (ICAPS), Prague.
  2023.
                                                                       Kugel, S. and Hiltner, S.     A new frontier for
Howey, R., Long, D., and Fox, M. VAL: Automatic plan val-                travel scammers:     A.I.-Generated Guidebooks.
  idation, continuous effects and mixed initiative planning             New York Times, August 2023.        URL https:
  using PDDL. In 16th IEEE International Conference                     //www.nytimes.com/2023/08/05/travel/
  on Tools with Artificial Intelligence, pp. 294–301. IEEE,              amazon-guidebooks-artificial-intelligence.
  2004.                                                                  html.
Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu,
                                                                       Kwon, M., Xie, S. M., Bullard, K., and Sadigh, D. Reward
 A. W., Song, X., and Zhou, D. Large language mod-
                                                                        design with language models. In The Eleventh Interna-
  els cannot self-correct reasoning yet. arXiv preprint
                                                                        tional Conference on Learning Representations, 2022.
  arXiv:2310.01798, 2023a.
Huang, J., Gu, S., Hou, L., Wu, Y., Wang, X., Yu, H., and              Liang, J., Huang, W., Xia, F., Xu, P., Hausman, K., Ichter,
  Han, J. Large language models can self-improve. In                     B., Florence, P., and Zeng, A. Code as policies: Language
  Bouamor, H., Pino, J., and Bali, K. (eds.), Proceedings                model programs for embodied control, 2023.
  of the 2023 Conference on Empirical Methods in Natural               Liu, B., Jiang, Y., Zhang, X., Liu, Q., Zhang, S., Biswas,
 Language Processing, pp. 1051–1068, Singapore, Decem-                   J., and Stone, P. Llm+ p: Empowering large language
  ber 2023b. Association for Computational Linguistics.                  models with optimal planning proficiency. arXiv preprint
  doi: 10.18653/v1/2023.emnlp-main.67. URL https:                        arXiv:2304.11477, 2023.
 //aclanthology.org/2023.emnlp-main.67.
                                                                       Ma, Y. J., Liang, W., Wang, G., Huang, D.-A., Bastani, O.,
Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence,
                                                                        Jayaraman, D., Zhu, Y., Fan, L., and Anandkumar, A.
  P., Zeng, A., Tompson, J., Mordatch, I., Chebotar, Y., et al.
                                                                        Eureka: Human-level reward design via coding large lan-
  Inner monologue: Embodied reasoning through planning
                                                                        guage models. arXiv preprint arXiv:2310.12931, 2023.
 with language models. arXiv preprint arXiv:2207.05608,
  2022.                                                                McCoy, R. T., Yao, S., Friedman, D., Hardy, M., and Grif-
IPC. International planning competition, 1998. URL                      fiths, T. L. Embers of autoregression: Understanding
  https://www.icaps-conference.org/                                     large language models through the problem they are
  competitions/.                                                        trained to solve. arXiv preprint arXiv:2309.13638, 2023.

Johnston, M. D., Tran, D., Arroyo, B., Sorensen, S., Tay, P.,          McDermott, D., Ghallab, M., Howe, A. E., Knoblock, C. A.,
  Carruth, B., Coffman, A., and Wallace, M. Automated                   Ram, A., Veloso, M. M., Weld, D. S., and Wilkins, D. E.
  scheduling for nasa’s deep space network. AI Magazine,                Pddl-the planning domain definition language. 1998.
  35(4):7–25, 2014.
                                                                       Nieuwenhuis, R. and Oliveras, A. On sat modulo theories
Kahneman, D. Thinking, fast and slow. macmillan, 2011.                   and optimization problems. In Theory and Applications of
                                                                         Satisfiability Testing-SAT 2006: 9th International Confer-
Kambhampati, S. Model-lite planning for the web age                      ence, Seattle, WA, USA, August 12-15, 2006. Proceedings
  masses: The challenges of planning with incomplete                     9, pp. 156–169. Springer, 2006.
  and evolving domain models. In Proceedings of the Na-
  tional Conference on Artificial Intelligence, volume 22,             Olmo, A., Sreedharan, S., and Kambhampati, S. Gpt3-to-
  pp. 1601. Menlo Park, CA; Cambridge, MA; London;                       plan: Extracting plans from text using gpt-3. FinPlan
  AAAI Press; MIT Press; 1999, 2007.                                     2021, pp. 24, 2021.

                                                                  11
                                        LLM-Modulo Framework for Robust Planning

OpenAI. Introducing chatgpt by openai, 2022.            URL           Stechly, K., Valmeekam, K., and Kambhampati, S. On
  https://openai.com/blog/chatgpt.                                      the self-verification limitations of large language mod-
                                                                        els on reasoning and planning tasks. arXiv preprint
OpenAI. Gpt-4 technical report, 2023.                                   arxiv:2402.08115, 2024a.
Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.,           Stechly, K., Valmeekam, K., and Kambhampati, S. Chain
  Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A.,              of thoughtlessness: An analysis of cot in planning. arXiv
  et al. Training language models to follow instructions                preprint arxiv:2405.04776, 2024b.
  with human feedback. Advances in Neural Information
  Processing Systems, 35:27730–27744, 2022.                           Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
                                                                        ing olympiad geometry without human demonstrations.
Pan, L., Albalak, A., Wang, X., and Wang, W. Y. Logic-                  Nature, 625(7995):476–482, 2024.
  lm: Empowering large language models with symbolic
                                                                      Ullman, T. Large language models fail on trivial al-
  solvers for faithful logical reasoning. arXiv preprint
                                                                        terations to theory-of-mind tasks. arXiv preprint
  arXiv:2305.12295, 2023.
                                                                        arXiv:2302.08399, 2023.
Rajvanshi, A., Sikka, K., Lin, X., Lee, B., Chiu, H.-P., and          Valmeekam, K., Marquez, M., and Kambhampati, S. Can
  Velasquez, A. Saynav: Grounding large language models                 large language models really improve by self-critiquing
  for dynamic planning to navigation in new environments.               their own plans? In NeurIPS 2023 Foundation Models
  arXiv preprint arXiv:2309.04077, 2023.                                for Decision Making Workshop, 2023a.
Romera-Paredes, B., Barekatain, M., Novikov, A., Balog,               Valmeekam, K., Marquez, M., Olmo, A., Sreedharan, S.,
  M., Kumar, M. P., Dupont, E., Ruiz, F. J., Ellenberg, J. S.,          and Kambhampati, S. Planbench: An extensible bench-
  Wang, P., Fawzi, O., et al. Mathematical discoveries from             mark for evaluating large language models on plan-
  program search with large language models. Nature, pp.                ning and reasoning about change. In Thirty-seventh
 1–3, 2023.                                                             Conference on Neural Information Processing Systems
                                                                        Datasets and Benchmarks Track, 2023b. URL https:
Russell, S. J. and Norvig, P. Artificial intelligence a modern          //openreview.net/forum?id=YXogl4uQUO.
  approach. London, 2010.
                                                                      Valmeekam, K., Marquez, M., Sreedharan, S., and Kamb-
Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. R.,                hampati, S. On the planning abilities of large language
  and Yao, S. Reflexion: Language agents with verbal                    models - a critical investigation. In Thirty-seventh Con-
  reinforcement learning. In Thirty-seventh Conference on               ference on Neural Information Processing Systems (Spot-
  Neural Information Processing Systems, 2023.                          light), 2023c. URL https://openreview.net/
                                                                        forum?id=X6dEqXIsEW.
Shridhar, M., Yuan, X., Côté, M.-A., Bisk, Y., Trischler,
  A., and Hausknecht, M. ALFWorld: Aligning Text and                  Verma, M., Bhambri, S., and Kambhampati, S. On the brittle
  Embodied Environments for Interactive Learning. In                    foundations of react prompting for agentic large language
  Proceedings of the International Conference on Learning               models. arXiv preprint arXiv:2405.13966, 2024a.
  Representations (ICLR), 2021. URL https://arxiv.
                                                                      Verma, M., Bhambri, S., and Kambhampati, S. The-
  org/abs/2010.03768.
                                                                        ory of mind abilities of large language models in
Silver, T., Hariprasad, V., Shuttleworth, R. S., Kumar, N.,             human-robot interaction: An illusion? arXiv preprint
   Lozano-Pérez, T., and Kaelbling, L. P. PDDL plan-                   arXiv:2401.05302, 2024b.
   ning with pretrained large language models. In NeurIPS             Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu,
  2022 Foundation Models for Decision Making Workshop,                 Y., Fan, L., and Anandkumar, A. Voyager: An open-ended
   2022. URL https://openreview.net/forum?                             embodied agent with large language models, 2023a.
   id=1QMMUB4zfl.
                                                                      Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu,
Simpson, R., McCluskey, T. L., and Zhao, W. Gipo: an inte-             Y., Fan, L., and Anandkumar, A. Voyager: An open-
  grated graphical tool to support knowledge engineering               ended embodied agent with large language models. arXiv
  in ai planning. In ECP-01, pp. 445. Citeseer, 2001.                  preprint arXiv:2305.16291, 2023b.
Stechly, K., Marquez, M., and Kambhampati, S. GPT-                    Wang, Y., Kordi, Y., Mishra, S., Liu, A., Smith, N. A.,
  4 Doesn’t Know It’s Wrong: An Analysis of Iterative                  Khashabi, D., and Hajishirzi, H. Self-instruct: Aligning
  Prompting for Reasoning Problems. In NeurIPS 2023                    language model with self generated instructions. arXiv
  Foundation Models for Decision Making Workshop, 2023.                preprint arXiv:2212.10560, 2022.

                                                                 12
                                        LLM-Modulo Framework for Robust Planning

Weng, Y., Zhu, M., Xia, F., Li, B., He, S., Liu, S., Sun,
 B., Liu, K., and Zhao, J. Large language models are
 better reasoners with self-verification. In Findings of
 the Association for Computational Linguistics: EMNLP
 2023, pp. 2550–2575, 2023.
Xie, J., Zhang, K., Chen, J., Zhu, T., Lou, R., Tian, Y.,
  Xiao, Y., and Su, Y. Travelplanner: A benchmark for
  real-world planning with language agents. arXiv preprint
  arxiv:2402.01622, 2024.
Xie, Y., Yu, C., Zhu, T., Bai, J., Gong, Z., and Soh,
  H. Translating natural language to planning goals with
  large-language models. arXiv preprint arXiv:2302.05128,
  2023.
Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao,
  Y., and Narasimhan, K. R. Tree of thoughts: Deliberate
  problem solving with large language models. In Thirty-
  seventh Conference on Neural Information Processing
  Systems, 2023a. URL https://openreview.net/
  forum?id=5Xc1ecxO1h.
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
  K. R., and Cao, Y. React: Synergizing reasoning
  and acting in language models. In The Eleventh In-
  ternational Conference on Learning Representations,
  2023b. URL https://openreview.net/forum?
  id=WE_vluYUL-X.




                                                                 13
