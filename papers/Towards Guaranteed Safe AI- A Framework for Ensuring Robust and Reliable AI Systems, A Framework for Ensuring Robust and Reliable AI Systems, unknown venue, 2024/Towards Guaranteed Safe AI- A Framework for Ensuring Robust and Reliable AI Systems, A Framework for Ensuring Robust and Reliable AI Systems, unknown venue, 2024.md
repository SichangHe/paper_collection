                                                                     Towards Guaranteed Safe AI:
                                                        A Framework for Ensuring Robust and Reliable AI Systems


                                        David “davidad” Dalrymple * 1 Joar Skalse * 2 Yoshua Bengio 3 Stuart Russell 4 Max Tegmark 5 Sanjit Seshia 4
                                                Steve Omohundro 6 Christian Szegedy 7 Ben Goldhaber 8 Nora Ammann 9 Alessandro Abate 2
                                        Joseph Y. Halpern 10 Clark Barrett 11 Ding Zhao 12 Tan Zhi-Xuan 5 Jeannette Wing 13 Joshua B. Tenenbaum 5


                                                                  Abstract                                       1. Introduction
arXiv:2405.06624v3 [cs.AI] 8 Jul 2024




                                                                                                                 We introduce and define a family of approaches to AI safety,
                                              Ensuring that AI systems reliably and robustly                     collectively referred to as guaranteed safe (GS) AI. These
                                              avoid harmful or dangerous behaviours is a cru-                    approaches aim to provide high-assurance quantitative guar-
                                              cial challenge, especially for AI systems with a                   antees about the safety of an AI system’s behaviour through
                                              high degree of autonomy and general intelligence,                  the use of three core components — a formal safety specifi-
                                              or systems used in safety-critical contexts. In                    cation, a world model, and a verifier. We will argue that this
                                              this position paper, we will introduce and define                  strategy is both promising and underexplored, and contrast it
                                              a family of approaches to AI safety, which we                      with other ongoing efforts in AI safety. We will also outline
                                              will refer to as guaranteed safe (GS) AI. The core                 several ongoing avenues of research within the broader GS
                                              feature of these approaches is that they aim to pro-               research agenda, identify some of their core difficulties, and
                                              duce AI systems which are equipped with high-                      discuss approaches for overcoming these difficulties. Cen-
                                              assurance quantitative safety guarantees. This                     tral examples of agendas which fall under the GS AI family
                                              is achieved by the interplay of three core compo-                  include Szegedy (2020); Wing (2021); Seshia et al. (2022);
                                              nents: a world model (which provides a mathe-                      Russell (2022); Tegmark & Omohundro (2023); ’davidad’
                                              matical description of how the AI system affects                   Dalrymple (2024); Bengio (2024).
                                              the outside world in a way that appropriately han-                 Critical infrastructure and safety-critical systems are re-
                                              dles both Bayesian and Knighting uncertainty),                     quired to comply with high safety standards. For example,
                                              a safety specification (which is a mathematical                    aircraft, nuclear power plants, and medical devices are sub-
                                              description of what effects are acceptable), and                   ject to exceptionally rigorous safety certification. Moreover,
                                              a verifier (which provides an auditable proof cer-                 it is plausible that there will soon be AI systems that are
                                              tificate that the AI satisfies the safety specifica-               at least as safety-critical as these systems (e.g. as AI sys-
                                              tion relative to the world model). We outline a                    tems are increasingly deployed in safety-critical contexts, or
                                              number of approaches for creating each of these                    given greater capabilities and autonomy), which means that
                                              three core components, describe the main techni-                   they should be required to adhere to standards of safety that
                                              cal challenges, and suggest a number of potential                  are at least as strict. Above some risk or capability thresh-
                                              solutions to them. We also argue for the necessity                 olds, the burden of demonstrating such safety guarantees
                                              of this approach to AI safety, and for the inade-                  should be on the systems’ developers, and the provided evi-
                                              quacy of the main alternative approaches.                          dence must be adequate to justify high confidence that the AI
                                                                                                                 system is safe. We will argue that approaches based only on
                                                                                                                 experimental tests are insufficient for producing such safety
                                          *
                                             Equal contribution 1 UK Advanced Research + Invention               guarantees. We will also argue that GS AI presents research
                                        Agency 2 Oxford University 3 Mila - Quebec AI Institute / U.             avenues that could plausibly produce such safety guaran-
                                        Montreal 4 UC Berkeley 5 Massachusetts Institute of Technology           tees in a satisfactory and feasible manner, while remaining
                                        6
                                          Beneficial AI Research 7 x.AI 8 FAR AI, Inc. 9 Principles of In-       competitive with AI systems without such guarantees.
                                        telligent Behaviour in Biological and Social Systems 10 Cornell
                                        University 11 Stanford University 12 Carnegie Mellon Univer-             In Section 2, we provide the general background and context
                                        sity 13 Columbia University. Correspondence to: David “davi-             for this paper, including a brief overview of the AI safety
                                        dad” Dalrymple <david.dalrymple@aria.org.uk>, Joar Skalse                problem, and some avenues for producing quantitative safety
                                        <joar.skalse@cs.ox.ac.uk>.
                                                                                                                 assessments through the use of empirical techniques. In Sec-
                                        Copyright 2024 by the author(s).                                         tion 3, we introduce and define GS AI, together with an

                                                                                                             1
                                                 Towards Guaranteed Safe AI

extensive discussion of the spectrum of approaches that                    stantial advantage. For example, in a chess game be-
fall under this agenda, the main challenges to these ap-                   tween a novice and a grandmaster, we should expect
proaches, and some potential solutions. We see the different               the grandmaster to win. More generally, the reason
approaches as comprising a portfolio of complementary                      why humanity is the most powerful species on the
R&D efforts. In Section 4, we offer several examples of                    planet is primarily that we have the greatest capacity
concrete practical problems, and how they may be solved                    to devise and carry out complex plans for reshaping
with a GS AI approach. In Section 5 we provide further                     our environment. Technological innovation is also the
high-level discussion of our proposals, including their feasi-             greatest driver of economic growth and military ca-
bility and benefits. In Section 6 we list some related work,               pabilities. Thus, if there are ever AI systems that are
and in Section 7 we conclude the paper.                                    substantially more intelligent than humans, and which
                                                                           are not aligned with human interests, then we should
2. Background                                                              expect human interests to be marginalised.

In this section, we provide the background that is required             3. Even if the goals of an AI system are specified correctly,
to understand the rest of this paper and its context. This                 it may still fail to internalise these goals in the intended
includes an overview of the AI safety problem, how to                      way. For example, one way to maximise a reward
classify AI systems based on the level of risk they pose, and              signal that is provided by human feedback may not be
a discussion of empirical safety assessments.                              to do what the humans wish, but rather to take control
                                                                           of the reward mechanism (Cohen et al., 2022). Similar
2.1. The AI Safety Problem                                                 phenomena have been observed empirically in current
                                                                           AI systems (Shah et al., 2022; Langosco et al., 2023),
A number of prominent AI experts have argued that suf-                     and studied theoretically (Hubinger et al., 2021).
ficiently advanced AI systems may threaten the survival
of the human species, or lead to our permanent disem-
powerment, especially in the case of AI systems that are              Existing attempts to solve these problems have so far not
more intelligent than humans. Such concerns have been                 yielded convincing solutions, despite rather extensive inves-
raised by Butler (1863), Asimov (1942), Wiener (1950), Tur-           tigations (Ji et al., 2024). This suggests that the problem
ing (1951), Good (1959), Minsky (1986), Moravec (1988),               is fundamentally hard, on a technical level. For a more
Vinge (1993), Joy (2000), Yudkowsky (2001), Bostrom                   complete and in-depth treatment of the arguments for why
(2002); as well as, more recently, Russell (2019; 2024),              future AI may pose an existential risk to humanity, see e.g.
Tegmark (2018), Bostrom (2014), Pearl (2019), Bengio                  Bostrom (2014); Russell (2019).
(2023), Hinton (2023), Amodei (2023), and others. These               Other AI experts have also pointed to more immediate risks
experts have provided many different arguments in support             from AI systems. For example, generative AI may facilitate
of these concerns, which we will not reproduce here in full.          the spread of disinformation, by enabling the creation of
However, here are a few very brief summaries of some of               convincing deepfakes or by making it cheaper and easier to
their central arguments:                                              produce large volumes of content (Brundage et al., 2018).
                                                                      AI decision making may also unfairly and systematically
  1. For an AI system to reliably solve a complex problem             disadvantage certain groups, even when unintended by the
     in an open-ended domain where i.i.d. assumptions are             system’s creators (e.g., Kleinberg et al., 2016; Buolamwini
     not valid, we must provide it with a formalisation of            & Gebru, 2018; Das et al., 2023; Wang et al., 2022). Recom-
     what it means to solve that problem. However, it is              mender systems may facilitate invasions of privacy and the
     difficult to create such specifications without leaving a        spread of extreme content (Stray, 2021; Carroll et al., 2022;
     substantial gap between what was specified and what              Boxell et al., 2020; Settle, 2018; Lelkes et al., 2017). AI
     was intended. This issue has been observed empirically           may also enable large-scale surveillance (Feldstein, 2019)
     in current AI systems (e.g., Krakovna et al., 2020; Pan          or the centralisation of economic or political power (Craw-
     et al., 2021; Pang et al., 2023), and studied theoreti-          ford, 2021; Brynjolfsson & Ng, 2023). For an overview of
     cally (e.g., Zhuang & Hadfield-Menell, 2020; Skalse              some of these issues, see, e.g., Memarian & Doleck (2023);
     et al., 2022; 2023; Karwowski et al., 2023; Skalse et al.,       Hendrycks et al. (2023); Brundage et al. (2018).
     2024). This suggests that it is difficult to engineer AI
     systems to robustly act in accordance with our inten-            These two perspectives on the risks from AI are not mutually
     tions, especially in unprecedented situations (which             exclusive. Moreover, they both point to similar sets of
     may also arise as AI itself increasingly reshapes its            technical challenges. The AI safety problem is the problem
     contexts of use).                                                of ensuring that AI systems reliably and robustly act in
                                                                      ways that are not harmful or dangerous, including (but not
  2. In a conflict of interests, greater intelligence is a sub-       limited to) cases where those AI systems are more intelligent

                                                                  2
                                                     Towards Guaranteed Safe AI

than humans. In this paper, we are proposing a family of                   2.3. Empirical Safety Assessments
engineering strategies for solving this problem in general.
                                                                           Current approaches to validating frontier AI models prior to
Note that the problem of ensuring that AI is not harmful                   deployment lean on independent testing and red-teaming (as
to humans comprises both a technical and a societal prob-                  e.g. Ziegler et al., 2022; Perez et al., 2022; Ganguli et al.,
lem; solving the technical problems is not sufficient if the               2022; Ouyang et al., 2022; Khlaaf, 2023). Such methods
solutions are not globally implemented. In this paper, we                  can find concrete examples of unsafe behaviour, which can
will primarily focus on the technical aspect of the AI safety              then be rectified by the developer or lead to the decision
problem. For an overview of some of the political and socio-               to halt training and deployment. However, these testing
logical challenges, see e.g. Lazar & Nelson (2023); Bostrom                regimes do not provide a rigorous, quantifiable safety guar-
(2014); Alaga & Schuett (2023); Koessler & Schuett (2023);                 antee: red-teamers could fail to find serious failures, while
Sastry et al. (2024); Schuett et al. (2023).                               a model still harbours such failure modes. In the extreme
                                                                           case, a model could have been backdoored in a way that is
2.2. AI Safety Levels                                                      cryptographically hard to detect without knowing the trigger
                                                                           (Guo et al., 2021). Even in the absence of such malfeasance,
The levels of precaution that are appropriate for a given AI               weaknesses in AI systems can remain undetected even after
system depend on the capabilities of that system. To classify              extensive testing. For example, ChatGPT was evaluated
the relevant levels of capability, Anthropic has introduced                in great detail over a period of several months (OpenAI
a framework that they call AI Safety Levels (ASL)1 as part                 et al., 2024), and yet users found ways to circumnavigate its
of their voluntary safety commitments (Anthropic, 2023).                   safety precautions within just a single day of it going public
This framework classifies AI systems into the following                    (Burgess, 2023). This issue is likely to be even more per-
high-level categories:                                                     tinent for more capable systems tasked with solving more
                                                                           difficult problems. Moreover, it is also important to note that
  1. ASL-1 refers to systems which pose no meaningful                      AI systems often will be deployed in adversarial settings,
     catastrophic risk.                                                    where human actors (or other AIs) actively try to break their
                                                                           safety measures. In such settings empirical evaluations are
  2. ASL-2 refers to systems that show early signs of dan-                 likely to be inadequate; there is always a risk that an adver-
     gerous capabilities (such as the ability to give instruc-             sary could be more competent at finding dangerous inputs,
     tions on how to build biological weapons) but whose                   unless you have a strong guarantee to the contrary.
     risks still appear importantly bounded (e.g. due to the               We argue that to obtain a high degree of confidence in a
     information not being practically useful, not reliable,               system we need a positive safety case providing quantifiable
     or offering no significant improvement over what is                   guarantees, using either or both empirical and theoretical
     achievable relative to non-AI baselines such as search                arguments (also see Bloomfield et al. (2019); Khlaaf et al.
     engines or textbooks). Many current language models                   (2022) for a similar argument). This is not unique to AI.
     appear to be ASL-2.                                                   About 25% of bridges built in the 1870s collapsed within
                                                                           the decade (McCullough, 2001), before a deeper theoretical
  3. ASL-3 refers to systems that substantially increase the               understanding of civil engineering reduced bridges’ failure
     risk of catastrophic misuse compared to non-AI base-                  rates to less than 0.4% per decade (Cook, 2014). When
     lines, or that show low-level autonomous capabilities.                quantitative safety assessments are required from develop-
                                                                           ers, this makes it possible for society to mandate a clear
  4. ASL-4 and higher (ASL-5+) are not yet defined in as                   level of safety, in terms of, e.g., the frequency per year
     much detail, but generally refer to human level and                   of adverse events of certain magnitudes (this is called a
     superhuman levels of intelligence, and thus qualitative               societal risk curve). At its simplest, this could consist of
     escalations in the potential for catastrophic misuse and              extensive testing: if an autonomous vehicle drives a million
     autonomy.                                                             miles safely without intervention of a test driver, then we
                                                                           can conclude that the failure rate probably is less than one
We refer to this classification scheme throughout the paper.               in a million miles when deployed in the same operating
Note that similar classification schemes also have been de-                domain. However, note that such inferences may only be
fined by other authors (e.g., FLI, 2023; Khlaaf et al., 2022).             valid within the bounds of unreasonable assumptions. For
                                                                           example, if human drivers start driving more aggressively
   1
     The ASL framework can be understood as a type of Safety In-           around autonomous vehicles after they are more used to
tegrity Level (SIL) framework, which are also the basis of standards       them (Liu et al., 2020), then this safety assessment might
in various other industries such as MIL-STD-882, IEC 61508, ISO            cease to hold.
26262, etc. The ASLs are loosely modelled after the US govern-
ment’s biosafety level (BSL) in particular.

                                                                       3
                                                     Towards Guaranteed Safe AI

Stronger empirical bounds (i.e. with weaker assumptions)                  3. Guaranteed Safe AI
may be obtained through methods such as adversarial test-
ing, and/or testing in simulations with domain randomi-                   In this section, we will introduce and characterise a family
sation. Even stronger bounds may be obtained through a                    of approaches to the AI safety problem, which we refer to
more mechanistic understanding of the system. Fault trees                 as guaranteed safe (GS) AI. We will first provide a defi-
(Nieuwhof, 1975) are a common safety engineering tech-                    nition of GS AI, together with a high-level overview. We
nique that allows for quantitative analysis, which can be                 will then discuss each of the core components of GS AI,
interpreted as deduction in probabilistic logic. For example,             namely a world model, a safety specification, and a verifier.
if two redundant components can be shown to have a fail-                  For each of the core components, we describe its role in
ure rate of ≤ n−1 and the failure rates are independent, the              the overall architecture towards providing high-assurance
combined failure rate would be ≤ n−2 . This could occur for               safety guarantees, highlight some of the key challenges in
example in an autonomous vehicle case when performing                     trying to implement these components, and discuss current
object detection on different sensors (e.g. LIDAR, vision,                approaches to overcoming those challenges.
radar), or in a generative model case when using an en-
semble of different models to detect malicious inputs. A                  3.1. Definition of GS AI
similar approach might be applicable even in the case of                  The core feature of the GS approach to AI safety is to pro-
a single monolithic model, by leveraging approaches like                  duce systems consisting of an AI agent and other physi-
mechanistic interpretability that seek to decompose internal              cal, hardware, and software components which together are
representations of the model (Zhang et al., 2021; Gao &                   equipped with a high-assurance quantitative safety guaran-
Guan, 2023; Bricken et al., 2023; Michaud et al., 2024).                  tee, taking into account bounded computational resources.
An alternative approach to obtaining stronger bounds relies               This can be contrasted against approaches to AI safety which
on theoretical understanding of the system. For example, a                primarily rely on empirical evaluations, or informal argu-
rigorous theory for how deep networks generalise (as built                ments based on qualitative or pre-theoretic intuitions.
towards by, e.g., Kearns & Vazirani, 1994; Watanabe, 2009;                A high-assurance quantitative safety guarantee may take the
2018; Mingard et al., 2021; 2020) might enable principled                 form of a formal proof that the system always will adhere
extrapolation from empirical testing on a limited valida-                 to some safety specification3 (or distribution over safety
tion domain to a broader test domain. Combined, these                     specifications) for all inputs, relative to a model (or a dis-
approaches could enable carefully conducted empirical eval-               tribution over models) of world dynamics. Alternatively, it
uations to provide substantially stronger safety bounds than              may be a reliable and sound upper bound on the probabil-
exist for contemporary frontier models.                                   ity of violating a safety specification. However, especially
However, any empirical evaluation must ultimately rely on                 when we cannot find a proof certificate, or cannot formally
some relatively strong assumptions, such as the distribution              define the desirable or undesirable behaviour, it may also
of inputs used to validate the models being sufficiently simi-            take the form of an estimate of an upper bound on the proba-
lar to those they are deployed on. This makes it challenging              bility of harm, with the estimate asymptotically converging
for an empirical approach to rule out instances of deceptive              with computational resources in order to guarantee a con-
alignment, where a system is acting to subvert the evalua-                straint on desirable behaviour. This gives us the following
tion procedure by detecting features of the input distribution            definition (for a more formal definition, see Appendix B):
that are unique to the test environment (Hubinger et al.,                 Definition 3.1. A Guaranteed Safe AI system is one that
2021). It also makes it challenging to give long-horizon                  is equipped with a quantitative safety guarantee that is pro-
safety guarantees, where the distribution of inputs is likely             duced by a (single, set of, or distribution of) world model(s),
to naturally shift over time.2 To achieve stronger safety                 a (single, set of, or distribution of) safety specification(s),
guarantees, which will become increasingly critical with                  and a verifier, satisfying the following criteria:
ASL-3 and beyond, we therefore expect it to be necessary
to use a model-based approach. We discuss this approach in
                                                                            1. The probabilistic specification encodes societal risk cri-
the following section.
                                                                               teria, which should ideally be determined by collective
    2
      Note that the usage of powerful AI is likely to itself create            deliberation.
situations that are novel and unprecedented, which makes this
a point of particular importance. Stated differently, we should             2. The verifier provides a quantitative guarantee (in the
assume that “distributional shift” will occur.                                 form of a proof certificate, probabilistic bound, asymp-
                                                                             3
                                                                               In this paper, we use the term “safety” not in the strict sense
                                                                          used in formal methods (Alpern & Schneider, 1987) but in the
                                                                          broader sense used in AI for the most important specifications of
                                                                          correct behaviour.

                                                                      4
                                                   Towards Guaranteed Safe AI

     totic guarantee, or other comparable assurance) that               as how a group of wise humans would hypothetically judge
     the AI system satisfies the specification with respect to          an outcome). Of course, we must also be able to trust the
     the world model.                                                   correctness of this world model, which means that it ide-
                                                                        ally should be interpretable and understandable. For more
  3. All potential future effects of the AI system and its
                                                                        discussion of how to create such a world model (or distribu-
     environment relevant to the safety specification should
                                                                        tion of world models), see Section 3.2. Note that the world
     be modelled (and – if feasible – conservatively over-
                                                                        model need not be a “complete” model of the world; the
     approximated) by the world model.
                                                                        level of detail and abstraction that is adequate depends on
There is much to unpack in this definition. Before moving               the safety specification and the AI system’s context of use.
on, we will therefore provide a brief explanatory example               Given a safety specification and a world model, we also
of what each of the core components of Definition 3.1 could             need a way to produce quantitative assurances for a given
look like, together with a motivation for their necessity.              AI system. In the most straightforward form, this could
Later in this section, we will provide a more in-depth dis-             take the shape of a formal proof that the AI system (or its
cussion of what each of these components may look like,                 output) satisfies the safety specification relative to the world
what challenges they come with, and how those challenges                model. This is akin to traditional formal verification (see
may be overcome. An overview is also provided in Figure 1.              e.g. Baier & Katoen, 2008; Leino, 2023; Seligman et al.,
But first, let us provide some intuition.                               2023). Of course, such formal verification is often hard to
A safety specification corresponds to a property that we                produce, even for relatively simple computer programs, and
wish an AI system to satisfy. For example, we may wish                  traditional formal methods face unique challenges for AI
that an AI system never takes any actions that may plausibly            systems (Seshia et al., 2016). However, further progress in
cause a human to be harmed. If we have a formal definition              automated reasoning and theorem proving due to integration
of harm, as well as a formal definition of causation, then this         with data-driven learning (see e.g. Lample et al., 2022;
safety property could be turned into a well-defined formal              Seshia, 2015; Wu et al., 2022; First et al., 2023; Trinh et al.,
specification. Of course, neither of these terms are easy               2024) could make this substantially easier, and might also
to formalise in general, but theoretical proposals exist (e.g.          scale with further progress in AI more generally. Moreover,
Beckers et al., 2022b;a; Halpern, 2016; Pearl, 2009). It is             if a direct formal proof cannot be obtained, there are weaker
sometimes also possible to operationalise harm in a context-            alternatives that would still produce a quantitative guarantee.
specific manner (Khlaaf, 2023). Other safety specifications             For example, it may take the form of a proof that bounds the
may also be desirable. For example, we may wish to require              probability of failing to satisfy the safety specification, or a
that an AI system is “truthful”, or that it can offer “explana-         proof that the AI system will converge towards satisfying
tions” for its actions, etc. In Section 3.3, we will provide            the safety specification (with increasing amounts of data
a more detailed overview of some possible methods for                   or computational resources, for example). Indeed, many
obtaining safety specifications, as well as their advantages            model-based AI algorithms have been designed to satisfy
and challenges. Note that due to difficulties with formulat-            exactly these sorts of guarantees (McMahan et al., 2005;
ing adequate safety specifications, it may be desirable to              Junges et al., 2016; Mathews & Schmidler, 2022; Hasanbeig
use multiple safety specifications, or to use distributions             et al., 2023). For a more detailed discussion, see Section 3.4.
of safety specifications, obtained through some learning                Note that the GS AI approach remains agnostic about both
process (or otherwise).                                                 how the “core” AI system was produced, and about what
Next, many desirable safety specifications necessarily re-              containment or boxing methods (Armstrong et al., 2012)
quire a world model (or distribution over world models) that            are used. If the verifier and the world model together can
describes the dynamics of the AI system’s environment. For              establish that the AI (or the AI’s output) satisfies the safety
example, suppose we want to ensure that an AI system never              specification, a quantitative safety guarantee is obtained
takes any actions that leads a human to be harmed, accord-              (even if the AI system remains uninterpretable, etc).
ing to some (possibly ambiguous) definition(s) of “harm”.
In order to do this, we need a model that describes whether             3.2. The World Model
a given action is likely to lead to a human being harmed (in            In this section we will discuss the world model, including
a given context). More generally, without a world model we              both a more detailed discussion of what counts as a world
can only verify specifications defined over input-output rela-          model, as well as some possible strategies for constructing
tions, but it is often desirable to instead verify specifications       such a world model (including their challenges and benefits).
over input-outcome relations. We may also want to define
predicates such as “harm” in terms of not only directly ob-             The world model needs to answer queries about what would
servable quantities (like a human-provided label), but also in          happen in the world as a result of a given output from the
terms of unobserved or even counterfactual variables (such              AI. It must also describe the state of the world at a level of

                                                                    5
                                                        Towards Guaranteed Safe AI



                                   Guaranteed Safe AI                                       Current AI Safety Practices



                                                                  actions                                          actions
                                                 Deployment
                                                Infrastructure   observations                    Deployment       observations




                    World Model
                                                                  runtime
                                                                 monitoring
                                                                                                  Quality
                                                  Veriﬁer
                                                                                                 Assurance
                       Safety
                    Speciﬁcation




                                                    AI                                              AI

                                                containment                                      containment




Figure 1. The GS AI approach builds on three components, namely a world model that describes the environment of the AI system, a
safety specification that describes desirable safety properties and is expressed in terms of the world model, and a verifier that provides a
quantitative guarantee of the extent to which an AI system satisfies the safety specification. In contrast, current AI Safety practices rely
primarily on quality assurance (e.g. evaluations) to decide if an AI system is safe, which is insufficient for safety critical applications.


granularity that is sufficient for expressing the safety speci-                 • Level 1: You use a trained black-box world simulator
fications we are interested in.4 A key challenge – which we                       as your world model.
will discuss more below – is finding a satisfactory solution
to handling both Bayesian and Knightian uncertainty. World                      • Level 2: You use a machine-learned generative model
models also serve to elucidate the AI system designers’ as-                       of probabilistic causal models, which you can test by
sumptions, and we must be mindful that those assumptions                          checking whether it assigns sufficient credence to spe-
may hold only part of the time. Hence, the domain of                              cific human-made models (such as e.g. models pro-
applicability and epistemic uncertainty regarding different                       posed in the scientific literature).
pieces of the world model must be represented and taken
into account. For these reasons, the world model, or relevant                   • Level 3: You use (a distribution over) probabilistic
aspects of it, should be auditable or monitorable at run time.                    causal model(s), potentially generated with the help
                                                                                  of machine learning, that are fully audited by human
There are many possible strategies for creating world mod-                        domain experts.
els. These strategies can roughly be placed on a spectrum,
depending on how much safety they would grant if success-                       • Level 4: You use world models about real world phe-
fully implemented (see also Figure 2):                                            nomena that are formally verified as sound abstractions
                                                                                  of fundamental physical laws. 5

   • Level 0: You have no world model. Instead, assump-                         • Level 5: You have no world model, and instead use
     tions about the world are implicit in the training data                      safety specifications universally quantified over the
     and in aspects of the implementation of the AI system.                       entire set of all possible worlds.
   4
     Note that a world model with a more abstract state-space
                                                                                5
may make it easier to express certain safety specifications, or                   By “sound abstraction” we mean the concept which has also
make verification more tractable, but that this may come at the             been called “reverse simulation” or “oplax coalgebra morphism”.
cost of making the predictions less accurate. Also note that the            Formally, a sound abstraction (of a dynamics f : X → ∆X
world model need not make predictions about arbitrary properties            on a state space X) is an abstracted state space A, an abstraction
of the world, and even about properties on which they do make               relation a : X → PA, and a dynamics g : A → ∆A such that
predictions, these predictions need not necessarily be precise.             f # a ⪯ a # g.

                                                                      6
                                                          Towards Guaranteed Safe AI

                                Towards Autonomous                                                          System Two
                                 Machine Intelligence                                                          Safety
                                       (LeCun, 2022)                                                          (Legg, 2023)
    World Model
    W0                        W1                               W2                         W3                        W4                        W5

  Unsupervised         Model-free RL            Cautious Scientist AI          Safeguarded AI              Provably Safe                 Agent
  Learning                                             (Bengio, 2024)           (Dalrymple, 2023)     (Tegmark & Omohundro, 2023)   Foundations
                                                Provably Beneﬁcial AI             Veriﬁed AI
                                                       (Russell, 2022)         (Seshia et al. 2022)
                                                                               Trustworthy AI
                                                                                  (Wing, 2021)
                                                                              Autoformalization
                                                                                 (Szegedy, 2020)




Figure 2. Different approaches for building world models can be projected onto a spectrum according to how much safety they would
grant if successfully implemented. Approaches listed in green fall into the GS AI family. Approaches in yellow may qualify (depending on
underspecified aspects of the approach) or come close to qualifying as GS AI. In our view, approaches in red fail to provide high-assurance
quantitative safety guarantees, and thus do not qualify as GS AI.


To get a better intuition for what these levels may look                     by human programmers, or if the language used to generate
like, let us discuss a number of potential approaches to                     pieces of the world model is forced or encouraged to be
constructing world models. First of all, in some cases, it                   interpretable through probabilistic translation to and from
may be feasible for engineers to manually create an adequate                 natural language (Jacob et al., 2023). If successful, this
world model. This has been done in settings where the                        approach could produce a world model on Level 2, 3 or pos-
operating environment is known or controllable, for e.g.                     sibly 4, in the classification above (depending on the extent
controllers in airplanes (Garion et al., 2022; Fremont et al.,               to which the resulting model is audited). One of the main
2020a) and self-driving cars (Ivanov et al., 2020; Fremont                   challenges with this approach would likely be to ensure that
et al., 2020b). Such models are also commonly used in                        the world model has a high predictive accuracy.
scientific research, including epidemic simulators (Broeck
                                                                             Another approach is to learn a world model from data. How-
et al., 2011) and particle physics simulators (Baydin et al.,
                                                                             ever, this approach comes with a number of challenges.
2019b). For AI systems, probabilistic programs have been
                                                                             In particular, many machine learning methods are prone
shown to be a promising formalism for world modeling
                                                                             to being confidently incorrect in novel situations. On a
(e.g., Milch et al., 2007; Matheos et al., 2020; Gothoskar
                                                                             theoretical level, this problem can be solved by Bayesian
et al., 2021; Fremont et al., 2022). In principle, this manual
                                                                             induction, which infers a distribution over world models
approach is likely to provide the best understanding of the
                                                                             (i.e. theories) from data (Kemp et al., 2010). Unfortunately,
assumptions underlying the world model, as well as the
                                                                             exact Bayesian induction is typically not computationally
delineation of its domain of applicability. This approach
                                                                             tractable (Hutter, 2003). However, recent advances in both
would produce a world model on Level 4 or 5. However, for
                                                                             Bayesian deep learning (Hollmann et al., 2023; Hu et al.,
AI systems that directly interface with very complex systems
                                                                             2023) and probabilistic programming suggest that approxi-
(such as e.g. human users, the world economy, or sensitive
                                                                             mate Bayesian induction can be made tractable (e.g. Baydin
ecosystems), it may not be possible to create sufficiently
                                                                             et al., 2019a). Using deep learning to parameterize gener-
accurate world models in a fully manual way.
                                                                             ative flow networks (Hu et al., 2023), one can train large
In such cases, the world model must instead be machine                       neural networks to implicitly estimate and sample from
learned (or automatically generated by some other means).                    the posterior distribution P (T | D) over theories T given
One possible approach to creating a world model with AI is                   data D, including cases where T itself represents a struc-
to use large language models (or similar systems) to write                   tured (causal) model (Deleu et al., 2022; Ke et al., 2022;
probabilistic programs that correspond to the system(s) be-                  Deleu et al., 2023). Using probabilistic programming, one
ing modelled (e.g., Wong et al., 2023a;b; Elmaaroufi et al.,                 can leverage sequential Monte Carlo (SMC) methods to
2024; Tang et al., 2024; Lew et al., 2020). This method                      gradually infer a theory T (represented as probabilistic pro-
has the potential to be scalable, since most of the work is                  gram) as new data is observed (Saad et al., 2023), or by
offloaded to AI systems. This method may also produce                        incrementally refining an initially coarse 3D world model
world models that are interpretable by default (Grand et al.,                (Gothoskar et al., 2023; Stuhlmüller et al., 2015). Both of
2023), if the language models are trained on code written


                                                                         7
                                                     Towards Guaranteed Safe AI

these approaches can potentially be combined6 , and also                  that is both interpretable and highly accurate (especially not-
benefit from more computation: by increasing the size or                  ing that such a model itself would constitute an AGI system).
training time of the neural network used to approximate                   There may thus in some cases be a fundamental trade-off
P (T | D), convergence to the true posterior is expected.                 between interpretability and predictive accuracy. However,
This means that we can continue training at run-time, or at               note that interpretability can be maintained if human be-
least estimate the error made by the neural network through               haviour is modelled using nondeterminism.8 Existing work
a sampling process. Similarly, by increasing the number of                on incorporating non-determinism into mathematical mod-
parallel samples, sequential Monte Carlo (SMC) methods                    elling comes form mathematics (Mio et al., 2021; Halpern
asymptotically converge (Del Moral et al., 2006). We can                  & Leung, 2013; Kosoy, 2021; Liell-Cock & Staton, 2024),
further decrease the risks associated with insufficient train-            computer science (Brookes et al., 1984; Brookes & Roscoe,
ing or sampling by encouraging the inferred theories to be                1984; BenThacker et al., 2006; Zhang, 2022) as well as
human-inspectable (e.g. by conditioning on the constraint                 robotics LaValle & Hutchinson (1996). The same applies
that theories can be converted to natural language and back               to other highly complex systems. Also note that the levels
with minimal error). If successful, this approach would pro-              in the classification above can be mixed within a single GS
duce a world model on Level 2 (or 4, if the model passes                  AI system. For example, a system can use stronger models
additional checks). See Bengio (2024) for a more complete                 of its engineering systems and weaker models of its interac-
discussion of this approach.                                              tions with the social domain (e.g., you may want to model
                                                                          your sensors with Level 5, but you will not be able to use
A very ambitious approach would be to use world mod-
                                                                          that rigour for e.g. social phenomena).
els that are formally verified as being sound abstractions
of the basic laws of physics. Note that while physics is                  A potential argument against the GS research agenda is that
not a completed field, there is good reason to believe that               the world may be so complex that it is infeasible even in
our current best theories are completely accurate in certain              principle to create a sufficiently accurate world model (be-
domains: for example, quantum gravity effects appear irrel-               cause of chaotic dynamics, etc). We have several responses
evant to contemporary AI systems (see e.g. Carroll, 2021).                to this point. First of all, a world model can (and should)
We can therefore be confident that a system truly satisfies a             of course include model uncertainty, and this uncertainty
specification if that specification is verified for that system           can be taken into account when the safety specifications are
relative to our best theories of physics, and that specification          verified.9 In this way, the strength of the resulting formal
also includes the requirement that the system is not moved                guarantees will be appropriately sensitive to the reliability
beyond the domains where our theories are known to be                     of the world model. Moreover, many of the most concerning
accurate. 7 If successful, this would produce a world model               loss-of-control scenarios with advanced AI systems involve
on Level 4. One of the main challenges for this approach                  cases where the AI is assumed to be able to generate and ex-
will be the immense computational complexity of producing                 ecute complicated plans with high reliability. In other words,
and verifying such models. To reduce the computational                    it is reasonable to assume that if AI systems can be powerful
complexity of this approach, approximate world models can                 enough to pose a serious danger to humanity, then it is pos-
be combined as compositional modules of one another, akin                 sible to create sufficiently accurate world models. Finally,
to how science approximates fluids as made of molecules                   we would like to note that this argument essentially is fully
made of atoms made of elementary particles, etc. For more                 general. Any strategy for creating safe AI systems must rely
details, see Tegmark & Omohundro (2023).                                  on some beliefs or assumptions about the real world, and
                                                                          these assumptions could be wrong; a world model simply
Note that in many cases, it will likely be necessary for the
                                                                          makes these assumptions explicit. Stated differently, if it
world model to model the behaviour of humans. Moreover,
                                                                          is impossible to create world models that are sufficiently
humans are very complex, and it seems dubious to presup-
pose that it is possible to create a model of human behaviour                 8
                                                                                Here “nondeterminism” should be understood in the same
   6
                                                                          sense as in “nondeterministic automata” and “nondeterministic
      For example, the trained neural network can be used to guide        Turing machines”, rather than as a synonym for “probabilistic”. In
SMC sampling (Zhao et al., 2024) and the resulting samples can            other words, the world model may specify a set or class of possible
in turn be used as training data for the neural network.                  (potentially stochastic) behaviours for each human, and require
    7
      It is also worth acknowledging that even a perfect model of         the verifier to validate the safety specification for each behaviour
physical dynamics is insufficient for safety, since safety-critical       profile in this set or class.
queries (e.g. whether a given molecule is toxic to humans) pre-               9
                                                                                As a very simple example, suppose that the safety specification
sumably will depend on facts about the initial conditions (e.g. of        is given relative to a finite time horizon of n steps, and that we have
human cells) that are not deducible from physics alone. This must         reason to believe that the world model is wrong with probability
be addressed by inference about initial conditions and boundary           at most ϵ per step over the first n steps. Then if a policy can be
conditions from data and observations, tempered by appropriately          proven to satisfy this specification relative to the world model, we
conservative epistemic frameworks incorporating Bayesian and              should believe that it will satisfy the specification with probability
Knightian uncertainty.                                                    at least (1 − ϵ)n in the real world.


                                                                      8
                                                      Towards Guaranteed Safe AI

accurate to ensure that an AI system adheres to some specifi-               spectrum, depending on how much safety it would grant if
cation, then it is presumably in general impossible to ensure               successfully implemented. One way to do this is as follows
that this specification is satisfied by that system.                        (see also Figure 3):

3.3. The Safety Specification                                                  • Level 0: No safety specification is used.
In this section we will discuss the safety specification(s),                   • Level 1: The safety of the system is evaluated by a pool
the difficulties with creating such specifications, and some                     of human judges based on their high-level intuitions
potential strategies for overcoming these difficulties.                          and preferences.
Much of the AI safety literature formalises desirable sys-
                                                                               • Level 2: The system uses a safety specification that
tem behavior in terms of reward functions (e.g. Amodei
                                                                                 is expressed in natural language but interpreted by a
et al., 2016). A safety specification is in general differ-
                                                                                 black-box AI system.
ent from a reward function, though they include bounded
reward functions as a special case. In particular, a safety                    • Level 3: The system uses hand-written safety specifi-
specification may include properties defined by probabilis-                      cations for limited safety properties that are relatively
tic temporal logics, causal counterfactual queries, or even                      tractable to express in a formal language.
hyperproperties, which reward functions cannot typically
express (Seshia et al., 2018; Skalse & Abate, 2023a; Sub-                      • Level 4: The system uses a specification that is written
ramani et al., 2024). However, safety specifications cannot                      in (probabilistic) logic at the top level, but which makes
include unbounded evaluations of the world-state.10 Safety                       use of (uninterpreted) neural components to represent
specifications could be expressed in terms of probabilistic                      learned bindings of certain human concepts to real
computation tree logic (PCTL) (Hansson & Jonsson, 1994),                         physical states.
or in terms of conjunction of linear inequalities of reachabil-
                                                                               • Level 5: The system uses compositional specifications
ity probabilities, for example. Specification logics can also
                                                                                 that are made up of parts that are all human audited,
invoke neural components as predicates (Mao et al., 2019),
                                                                                 but synthesised by AI.
allowing us to learn the semantics of concepts that are hard
to manually specify.                                                           • Level 6: The system uses hand-written safety specifica-
The appropriate safety specification depends on the applica-                     tions for comprehensive safety properties that require
tion domain and context (Khlaaf, 2023). Task-specific AI                         substantial effort to express formally.
services often afford contextual operationalisations of safety,
                                                                               • Level 7: The safety specification completely encodes
while more general-purpose AI assistants may require spec-
                                                                                 all things that humans might want, in all contexts.
ifications that invoke broad definitions of harm (Beckers
et al., 2022b; London & Heidari, 2023).11 For example,
in the context of autonomous vehicles (or other embodied                    Authoring safety specifications is routine in automated
AI systems navigating in a human environment), the safety                   controller design (Tabuada, 2009), and can frequently be
specification may contain rules about lawful and appropriate                achieved for both traditional software systems and domain-
driving behaviour as well as specifications to avoid causing                specific AI. Examples include probabilistic guarantees of
physical harm to others; for software systems, the safety                   collision avoidance in robotics, guarantees that some control
specification may seek to capture both its intended function-               policy interacting with a dynamical system will stay in a
ality and a lack of cyber vulnerabilities; or, in the context of            safe region (used e.g. in robotics, drones, and controllers
automated medical research, the safety specification could                  for many other physical systems), verification of security
bound the pathological potency of the identified molecules.                 properties of cyberphysical systems, or of medical device
Section 4 provides a number of concrete examples of GS                      software. However, creating safety specifications becomes
AI, including their safety specifications.                                  increasingly difficult as AI systems operate in increasingly
                                                                            general and open-ended settings, and without well-defined
There are many possible strategies for creating safety spec-                scopes or semantics. Suppose, for example, that we want
ifications. These strategies can roughly be placed on a                     to ensure that a chatbot never gives advice that is “harm-
   10
      The reason for this requirement is that it should be possible
                                                                            ful”. How should this specification be formalised? A robust
to completely satisfy the specification in order to relieve optimi-         formalisation of this specification would require a very de-
sation pressure. In order for it to be possible, it must at least be        tailed world model, since whether or not a given piece of
conceivable, i.e., the specification’s level of satisfaction needs to       advice will turn out to be harmful may depend on diverse
be bounded at least in theory.                                              facts about the real world in complicated ways. Alterna-
   11
      See Appendix A for a short discussion of a potential definition       tively, we could instead require the AI to never give advice
of harm along the lines of Beckers et al. (2022a).
                                                                            that it “believes” to be harmful. However, verifying this

                                                                        9
                                                      Towards Guaranteed Safe AI

                                                                       System Two Safety                 Trustworthy AI
                                                                           (Legg, 2023)                     (Wing, 2021)
                                                 Towards Autonomous
                                                  Machine Intelligence                                Veriﬁed AI
                                                       (LeCun, 2022)                               (Seshia et al. 2022)
     Safety Speciﬁcations
    S0                 S1                 S2                   S3                    S4                       S5                   S6                    S7

  Unsupervised       RLHF        Constitutional AI                            Cautious Scientist AI                        Provably Safe
  Learning                                                                        (Bengio, 2024)                     (Tegmark & Omohundro, 2023)

                                                     Autoformalization                             Safeguarded AI               Provably Beneﬁcial AI
                                                       (Szegedy, 2020)                             (Dalrymple, 2023)                       (Russell, 2022)




Figure 3. Different approaches for creating safety specifications can be projected onto a spectrum according to how much safety they
would grant if successfully implemented. Approaches listed in green fall into the GS AI family. Approaches in yellow may qualify
(depending on underspecified aspects of the approach) or come close to qualifying as GS AI. In our view, approaches in red fail to provide
high-assurance quantitative safety guarantees, and thus do not qualify as GS AI.


specification requires a reliable way of extracting “beliefs”                 Todorov, 2010; Cao et al., 2021; Kim et al., 2021; Skalse
from an AI system, which is difficult for black box mod-                      et al., 2023; Schlaginhaufen & Kamgarpour, 2023). More-
els. Moreover, “harm” is a vague predicate, in the sense                      over, many reward learning algorithms are highly sensitive
that there are edge-cases where it is controversial whether                   to the modelling assumptions they make about their data
a given person is harmed or not. Similar issues occur if we                   source (Armstrong & Mindermann, 2018; Freedman et al.,
want to ensure that an AI system never lies, or that it always                2020; Viano et al., 2021; Skalse & Abate, 2023b; 2024).
follows instructions from humans, etc.                                        Finally, the learnt reward model is itself typically not inter-
                                                                              pretable, which is a serious issue (see e.g. Michaud et al.,
In many cases, it is possible to find proxies for complex pred-
                                                                              2020; Jenner & Gleave, 2022). This means that much work
icates (such as “harm”) which are easier to define and mea-
                                                                              is required before reward learning can be a reliable source
sure. However, while such a proxy may robustly correlate
                                                                              of specifications. For an overview, see Casper et al. (2023).
with our intuitive judgements of harm in normal situations,
                                                                              Also note that there are approaches to learning safety speci-
they may still reliably come apart if those proxies are used as
                                                                              fications which go beyond the umbrella of reward learning,
an optimisation target. This phenomenon is known as Good-
                                                                              see e.g. Bengio (2024); Seshia (2015); Vazquez-Chanlatte
hart’s law, which is an informal principle sometimes stated
                                                                              et al. (2018); Vazquez-Chanlatte & Seshia (2020); Neider &
as “when a measure becomes a target, it ceases to be a good
                                                                              Gavran (2018).
measure”. Goodhart’s law was first introduced by Goodhart
(1975), and has since been studied more formally in works                     Another approach is to attempt to create “conservative”
such as Manheim & Garrabrant (2019); Hennessy & Good-                         safety predicates which aim to be sufficient (but not nec-
hart (2023); Zhuang & Hadfield-Menell (2020); Skalse et al.                   essary) for safety. For example, we may require that the AI
(2022); Karwowski et al. (2023). This means that a safety                     has no incentive to influence any part of the external world,
specification may need to be highly accurate in order to                      or to find out any information about the external world (e.g.
remain robustly reliable, especially when applied to an AI                    Armstrong et al., 2012; Armstrong & O’Rorke, 2018; Arm-
system with strong optimisation or planning capabilities.                     strong & O’Rourke, 2018; Everitt et al., 2021; van Merwijk
                                                                              et al., 2022). Alternatively, we may attempt to create safety
One strategy is to attempt to learn safety specifications from
                                                                              predicates which make an AI system more safe, even if they
data. This is explored by the field of reward learning, where
                                                                              do not ensure safe behaviour (as e.g. Soares et al., 2015;
the specification is assumed to have the form of a reward
                                                                              Orseau & Armstrong, 2016; Hadfield-Menell et al., 2017,
function. If we assume that a human’s preferences can be
                                                                              etc). These approaches come with their own challenges, see
captured by a reward function, and if we can learn a rep-
                                                                              e.g. Bostrom (2014) and the above cited works. Moreover,
resentation of this reward function from some data source,
                                                                              while certainly challenging, it may still be feasible to simply
then we may be able to prove that a given AI system will
                                                                              specify the safety predicates manually. This is (partially)
respect the preferences which are embodied by that reward
                                                                              attempted in works such as e.g. Beckers et al. (2022a;b).
function. However, reward learning also faces serious diffi-
culties. In particular, most data sources are insufficient for                It is also important to note that the task of formalising spec-
identifying the underlying reward function uniquely, even                     ifications can be easier with a system-level approach. As
in the limit of infinite data, and this irreducible ambiguity                 advocated by Seshia et al. (2022), even when individual AI
may be problematic (Ng & Russell, 2000; Dvijotham &                           components perform tasks that are hard to formalise, it can

                                                                         10
                                                Towards Guaranteed Safe AI

still be the case that the relevant notion of safety can be          tions could take several forms, but a natural choice would be
formalised at the full system level. For example, one can            to require that the AI is provably beneficial to the human (or
formalise system-level safety for autonomous vehicles even           some variation thereof). Note that such specifications may
when it is not possible to formalise correctness for object          require the world model to also make modelling assump-
detection and classification components in the autonomy              tions about the behaviour of the human (and in particular
stack (e.g., Dreossi et al., 2019). In some cases, this can          about how the behaviour of the human relates to its pref-
make it feasible to define specifications directly.                  erences). Also note that many of the challenges to reward
                                                                     learning also apply to CIRL.
A complementary approach is to create a hierarchy of safety
specifications for provably compliant systems (PCSs) all the         While these challenges are serious, it is important to note
way down to the physical level, as described by Tegmark &            that most approaches to AI safety require formal safety spec-
Omohundro (2023). Such a hardware-grounded ecosystem                 ifications (or at least formalisations of what an AI system
of modules is valuable because some of today’s formally              should be optimised for). These difficulties are thus not
verified systems have been hacked by compromising phys-              unique to the GS research agenda. It is also important to
ical properties of the underlying hardware (Mutlu & Kim,             note that further development in AI capabilities will tend
2019). To prevent this, the PCS-approach rests on a founda-          to make it easier to create good safety specifications. For
tion of relatively simple provably compliant systems, from           example, AI systems could be used to suggest new specifi-
sensors, actuators and memory devices, to microprocessors            cations, to critique proposed specifications, or to generate
with physics-based proofs that they meet their specifica-            examples of cases where two candidate specifications differ.
tion — including a protocol guaranteed to reveal failure or          Progress in AI could thus also accelerate the creation of
tampering. Such basic PCS modules are then combined                  good safety specifications.
into an ecosystem of increasingly complex PCS’s whose
verification recursively verifies their components.                  3.4. The Verifier
Although specification can be challenging for highly compe-          In this section we will discuss the verifier, the difficulties
tent and embodied AI systems, there are many low-hanging             with creating such a verifier, and some potential strategies
fruit tasks which do not require complex specification (or           for overcoming these difficulties.
world modeling or verification) and which can provide great
near-term value and incentives for further development. Ex-          The verifier may produce different kinds of formal guaran-
amples include machines provably impossible to login to              tees, depending on what is feasible in a given context. We
without correct credentials, DNA synthesizers that provably          can thus place different kinds of verifiers on a spectrum,
cannot synthesize certain pathogens, and AI hardware that            based on the strength of their corresponding guarantees (see
is provably geofenced, time-limited (“mortal”) or equipped           also Figure 4):
with a remote-operated throttle or kill-switch. Provably com-
pliant sensors can be spefified to ensure “zeroization”, in             • Level 0: No quantitative guarantee is produced.
which tampering with PCH is guaranteed to cause detection
and erasure of private keys. For more details, see Tegmark              • Level 1: You use ad-hoc empirical testing of the AI
& Omohundro (2023).                                                       system, which provide a heuristic-based assurance.

Another strategy for creating specifications is provided by             • Level 2: You use a standardised set of tests, which
Cooperative Inverse Reinforcement Learning (CIRL), as de-                 thus provides safety assurances that are auditable and
scribed by Hadfield-Menell et al. (2024). CIRL formulates                 comparable across systems.
the interaction between an AI and a human as a two-player
                                                                        • Level 3: You use a property-based test which includes
Markov game (with one player being the AI, and one player
                                                                          domain randomisation and current state-of-the-art au-
being the human). Both players have the same reward func-
                                                                          tomated evaluations. In other words, you have some
tion, but only the human knows what the reward function is.
                                                                          template for what the test looks like, but randomly
This means that the two players must cooperate to obtain
                                                                          populate the template to get more coverage.
a high reward, and that the AI system must listen to feed-
back from the human. Optimal solutions to the CIRL game                 • Level 4: You use black-box fuzzing, wherein an au-
produce behaviours such as active teaching, active learning,              tomated tool gives test vectors as input to the system
and communicative actions. The idea is that this problem                  and, depending on the response, generates different
formulation will encourage the AI to be corrigible (in the                test vectors to fool the system. In other words, you use
sense of Soares et al., 2015), instead of following some goal             a form of automated red-teaming.
dogmatically. An AI could be verified to adhere to various
safety specifications within the CIRL game. These specifica-            • Level 5: You use white-box fuzzing, which is akin
                                                                          to Level 4, except that your tool not only looks at

                                                                11
                                                          Towards Guaranteed Safe AI

        the input-output behaviour of the AI system, but also                    with humans outside of formalising and reasoning about
        considers its internal states and tries to make certain                  existing statements or developing related theories. Note
        internal structures flip to get more coverage.                           that the scope of training for such an agent would be very
                                                                                 limited, i.e., it would only be exposed to natural language
   • Level 6: You use probabilistic inference with asymp-                        mathematics and computer science. It would therefore not
     totic convergence. This is akin to Level 5, but with                        have any significant knowledge of the outside world beyond
     the additional guarantee that if the evaluation system                      these restricted domains. This restricts the AI’s potential for
     would run forever, then it would eventually literally                       power-seeking behaviour.
     cover every possible input to the system.
                                                                                 Formal verification has a long and rich history reviewed in
   • Level 7: You combine asymptotic coverage with white-                        e.g. Leino (2023); Seligman et al. (2023). Here we outline a
     box fuzzing. This might include adversarial gradient                        potential approach for designing and training an expert-level
     optimisation, whereby you first cover areas where you                       reasoning system by letting it process all of the mathemati-
     most expect safety concerns to spring up, and where                         cal and computer science literature automatically (Szegedy,
     the system in the limit of infinite time would cover                        2020). We first index all of the existing informal and formal
     every possible system input.                                                literature with an ASL-3 system and create a neural retrieval
                                                                                 system. Then we use similarly capable language models
   • Level 8: Akin to Level 7, but with the additional re-                       to extract statements and definitions from the text and for-
     quirement that you have some non-asymptotic conver-                         malise them. Early examples of such models already exist,
     gence bounds, due to some formula for how much of                           but they must be improved before they are of sufficient qual-
     the total state space your system covers at a given time.                   ity to be used in the initial phase of a bootstrap loop. The
     You can thus run it for a finite amount of time, and                        informal to formal translation data for this phase can be gen-
     know how much is left that you have not covered                             erated using cycle-consistency training (Lample et al., 2017)
   • Level 9: You have a sound bound on the probability of                       together with the small but increasing amounts of human-
     failure, meaning that the true probability of something                     verified formalization of informal statements. Similarly,
     happening is less than or equal to the value established                    a proof-generation agent can be trained on the relatively
     by your verifier. This includes the formal proof case                       large corpus of existing formal theorems. Additional ca-
     where the verifier is able to establish that the probabil-                  pability can be achieved via a reinforcement learning loop
     ity of failure is 0 (relative to the world model).                          that trains the translation model and the neural prover in
                                                                                 lockstep. In this step, both models can be assumed to be
   • Level 10: Akin to level 9, but with the additional re-                      retrieval-augmented large language models, while the trans-
     quirement that the proof is concise enough that humans                      lation takes in informal (natural language) specifications and
     can read, understand, and check it. 12                                      outputs formal specification. Then the prover attempts to
                                                                                 prove them, potentially utilising the natural language proof
To obtain strong guarantees, we need a verifier at Level 8, 9,                   sketches. Whenever a statement is proven to be correct (that
or 10. This, of course, raises the question of whether such                      is, verified by the formal prover), and it is useful for proving
guarantees can feasibly be obtained for AI systems. Even                         other statements like its informal counterpart, it can be con-
for relatively simple properties of software, obtaining such                     sidered to be a correct transcription and used for training the
guarantees currently imposes a very high burden, as it re-                       translation model. In addition, the prover can be trained on
quires highly specialised cognitive labour. However, it may                      the successful proof traces. While there is ongoing research
be possible to train AI systems without ASL-4 capabilities                       work on the overall feedback loop, and many challenges
to automate much of this labour at a near-expert level of                        remain, there are multiple existing proof-of-concept solu-
sophistication without raising significant safety concerns.                      tions for various components of this reinforcement learning
For example, consider an AI agent that only interacts with                       system (Szegedy, 2020), which suggests that a full solution
a formal theorem-prover and is only allowed to grow a li-                        may be realizable in the coming years.
brary of formal facts. In this case the agent will never be                      A more extensive discussion on the challenges for extending
exposed to any actions that would meaningfully influence                         formal methods to handle the unique characteristics of AI
the real world, and it would never learn to communicate                          systems is provided by Seshia et al. (2022), who presents 15
   12
      For the formal proof case, level 9 suffices: Just as it is much            principles for providing provable guarantees of safety for AI
harder to find a needle in a haystack than to verify that it is a needle,        systems. We summarise some of the key ideas pertaining to
it is much harder to discover an algorithm with a compliance proof               the verifier here and point the reader to (Seshia et al., 2022)
than to verify it — which can be done with just a few hundred lines              for details. First of all, one important piece is devising suit-
of human-written code (Megill, 2023). This means that humans                     able abstractions of AI components such as neural networks.
need not understand the system or proof, merely the the simple
verifier code.                                                                   Seshia et al. (2022) advocate for designing abstractions of

                                                                            12
                                                     Towards Guaranteed Safe AI


                                                                                                        Cautious                   Veriﬁed AI
                                                                                                       Scientist AI             (Seshia et al. 2022)
                                                                                                       (Bengio, 2024)            Provably Safe
                                             Towards Autonomous                                System Two               (Tegmark & Omohundro, 2023)
                                              Machine Intelligence                                Safety                     Autoformalization
                                                  (LeCun, 2022)                                 (Legg, 2023)                     (Szegedy, 2020)
    Veriﬁcation
    V0            V1           V2           V3           V4             V5              V6             V7               V8                 V9               V10

  No          Manual      Manual      Automated    Automated      Adversarial     Control as                   Safeguarded AI                  Provably
  Testing   Red Teaming    Evals         Evals    Red Teaming      Testing        Inference                    (Dalrymple, 2023)            Beneﬁcial AI
                                                                                                                                              (Russell, 2022)
                                                                                                               Trustworthy AI
                                                                                                                 (Wing, 2021)           Optimal Control




Figure 4. Different approaches to verification can be projected onto a spectrum according to how much safety they would grant if
successfully implemented. Approaches listed in green fall into the GS AI family. Approaches in yellow may qualify (depending on
underspecified aspects of the approach) or come close to qualifying as GS AI. In our view, approaches in red fail to provide high-assurance
quantitative safety guarantees, and thus do not qualify as GS AI.


AI components that are easier to formally analyse and which               4. Examples of GS AI Solutions
can be generated algorithmically. In this context, abstrac-
tions that are modular and more interpretable have also been              Here we describe some concrete examples of practical prob-
found to be easier to analyse by formal verification tools.               lems and how they may be solved with a GS AI approach,
Another crucial principle is compositional reasoning; the                 which combine the different components described in the
idea is to construct a proof of safety of the overall AI system           previous sections and fall along the different axes. The
by decomposing the top-level proof obligation into sub-                   examples range from current- or near-term tractable and
obligations on individual components, and then applying                   economically viable applications, to ones that have not yet
formal verification to the sub-obligations. One challenge                 been realised due to their more ambitious scope.
here is that not all AI components have formal specifications                   Example 4.1 (Code Translation).
– in other words, we need to do compositional verification                      Problem: Translate code in one programming lan-
without compositional specifications! Seshia et al. (2022)                      guage (e.g. C) to another (e.g. Rust) using AI sys-
tackle this by proposing techniques to automatically infer                      tems (e.g. language models) with provable guarantees.
a decomposition of the system into components along with                        While some simple instances of this general problem
interface contracts between them. Such a decomposition                          have been solved (e.g., translating side effect-free func-
could be spatial and/or temporal and has been shown to aid                      tional programs from a source language to a domain-
in scalable analysis (Dreossi et al., 2019; Yalcinkaya et al.,                  specific target language (Bhatia et al., 2024)), much
2023). Finally, it is crucial to integrate formal methods into                  remains to be done to solve the general code translation
the design process for AI components, for example, the                          problem.
training of deep learning components, and also to connect
design-time formal methods with run-time assurance. Ideas                       Specification: Functional correctness (the source pro-
from verified inductive synthesis of programs can be useful                     gram is equivalent to target program with respect to
in training AI components with provable guarantees (e.g.                        the relevant program state), and the generated target
Dreossi et al., 2018; Abate et al., 2023).                                      code does not have specified classes of security vul-
                                                                                nerabilities. Defining functional correctness is easy in
A complementary approach is to replace neural networks by                       some cases (e.g., (Bhatia et al., 2024)) but more com-
traditional formally verifiable software in deployed systems                    plicated in general since the source and target program
or key modules thereof (Tegmark & Omohundro, 2023).                             structure can be very different and specifications can
The algorithms to be coded up and verified can be auto-                         be partial.
generated either by direct AI-powered program synthesis
or by using automated mechanistic interpretability tools                        World Model: Constraints on the inputs to the pro-
to distill machine-learned algorithms into verifiable code                      gram (pre-conditions), and threat models for security
(Michaud et al., 2024). Both approaches can be accelerated                      (what the attacker can/cannot do).
by creation of large benchmarks for training/testing.                           AI System: Large language models for code genera-



                                                                     13
                                               Towards Guaranteed Safe AI

tion (e.g. models such as GPT-4, Claude, etc., or others         tion.
expressly designed or fine-tuned for code generation).
                                                                 Example 4.3 (Household Robots).
                                                                 Problem: Provide assistance to humans in need of
Example 4.2 (Autonomous Vehicle (AV) Safety).
                                                                 support at home.
Problem: Design an AI-enabled autonomous driving
system (ADS) that satisfies a formal specification of            Specification: Carrying out diverse household tasks.
safety and functionality in specified scenarios, and also        Tasks include cleaning rooms, organising items, bring-
maintains a (smaller) core safety specification when             ing items to humans, and navigating safely around
outside those scenarios                                          people, ensuring no harm comes to humans. Adapta-
                                                                 tion to a human’s special needs and environment: the
Specification: A “rulebook” (Censi et al., 2019), a set
                                                                 robots should adapt to varying human needs and en-
of rules that have an associated pre-order, where each
                                                                 vironments while grounding the original skills to the
rule can be a specification written in a formalism that
                                                                 new conditions.
suits its purpose. Rules are mathematical objects that
map behaviours (or sets of behaviours) to a value do-            World model: Home diversity (various layouts of
main; they can be objective functions (cost/reward               homes and diverse tasks for home management) and
functions), temporal logic properties, probabilistic             robot constraints (constraints governing the behaviour
bound properties, automata, etc. The overall specifica-          of the robots to ensure safety and efficiency).
tion would also include a more restricted specification
                                                                 AI System: VLMs equipped with multi-task learning
that would be maintained by the backup system (of
                                                                 capabilities and continuous learning mechanisms.
which there could be multiple levels).
World Model: A set of scenarios in which the ADS
                                                                 Example 4.4 (Medical Diagnosis Agent).
operates that includes formal models of (i) the other
                                                                 Problem: Facilitate disease diagnosis and provide
components of the AV, (ii) agents and objects in the
                                                                 medical advice.
scenario, including their attributes and behaviour mod-
els, (iii) other attributes of the environment, such as          Specification: Precisely diagnose diseases based on
spatial constraints of the physical world around the             the presenting symptoms of the patient, provide in-
AV, time of day, weather conditions, etc., (iv) models           sights into the underlying causes of the disease, and
of humans and their preferences and objectives. We               offer precise and effective treatment recommendations.
expect these models will be stochastic in nature and
                                                                 World Model: A model of the human body (describing
some components of the world model will be learned
                                                                 the complexities and nuances of human physiology
from data/interactions while others will be encoded by
                                                                 and pathology), and a model of environmental factors
domain experts or inferred/generated statically. Proba-
                                                                 (for consideration of external factors contributing to
bilistic programming languages (e.g. Scenic, Fremont
                                                                 disease onset or progression).
et al., 2022) offer one mechanism for world modelling
for this application and have had some success in prac-          AI System: A multi-media input system capable of
tice. As in the case of the specification, there would           parsing diagnostic notes, interpreting medical imaging
be world models also specified for the backup sys-               data, and delivering accurate diagnoses and treatment
tem(s) which constitute weaker assumptions about the             plans.
operating environment.
AI System: ADS integrates many types of AI/ML                    Example 4.5 (Compute Centre Management).
components with traditional hardware and software                Problem: Ensuring that data centres run multi-tenant
components. For example, deep neural networks are                applications efficiently and correctly while preventing
used in various steps of the autonomy pipeline includ-           unauthorised applications from using compute.
ing for perception, prediction, planning, and control.
                                                                 Specification: Efficient allocation according to busi-
LLMs are being considered for use in interfaces to
                                                                 ness agreements, legal compliance with e.g. compute
humans, to elicit preferences, explain the behaviour
                                                                 caps, and security (protection against and detection of
of AVs to occupants and others, etc. An ADS should
                                                                 attempted breaches).
also include runtime monitors that check whether the
assumptions made in the world model (about the AV’s              World Model: The shared computing ecosystem with
“operational design domain”) are maintained during               tenant isolation, resource allocation, and cryptographi-
operation, and, if not, to predictively take backup ac-          cally secured hardware.


                                                            14
                                              Towards Guaranteed Safe AI

AI System: An AI model trained for optimal allocation              tem, and the health of the ecosystem under said cli-
within economic, legal, and security constraints.                  mate.
                                                                   World model: A model of complex climate dynamics
Example 4.6 (Formally Verified Re-Implementation of                under various intervention regimes.
Bug-Free Software and Hardware Systems for Cyber
Defence.).                                                         AI Agent: A “climate agent” that generates geoengi-
Problem: The currently existing soft- and hardware                 neering solutions which verifiably stabilise the climate
infrastructure contains many bugs, thereby creating a              system without compromising the health of the ecosys-
large attack surface area for cyberattacks. A drastic              tem.
reduction of this surface area and thus improved cyber-
security can be achieved by replacing legacy code with           5. Discussion
software that has been formally verified to be bug-free
and trustworthy.                                                 We have argued that safety-critical AI systems need to be
                                                                 equipped with quantitative safety guarantees, and that em-
Specification: The intended function of the legacy               pirical evaluations alone are insufficient for producing such
code, and a lack of bugs or vulnerabilities.                     guarantees with an adequate level of assurance. We have
World Model: Autoformalisation taking the legacy                 also introduced GS AI as a potential avenue for feasibly
code and inferring from it its intended function.                obtaining such safety guarantees, discussed the main chal-
                                                                 lenges with this research agenda, and some ways in which
AI System: An AI “Software Engineer” agent which                 those challenges may be overcome. In this section, we will
re-implements existing software through autoformali-             further discuss some potential benefits to the GS AI research
sation and interactive specification crafting with stake-        agenda, and some important considerations.
holders, and synthesises a bug-free version.
                                                                 An important benefit to GS AI is that it makes democratic
                                                                 oversight easier, because concrete safety specifications can
Example 4.7 (Safe Nucleic Acid Sequence Screening                be audited and discussed by outside observers and regula-
& Synthesis).                                                    tors. AI technology will have an immense (and potentially
Problem: The screening, identification and synthesis             unprecedented) impact on most, if not all, areas of life. This
of nucleic acid, protein, RNA, or DNA structures has             makes it crucial to enable as many people as possible to have
potent applications for the health and flourishing of            a say in how this technology is deployed and used. How-
humans, however also risks applications that could be            ever, such democratic input and oversight is not possible if
harmful for individuals or civilisation at large.                important AI systems are specified, trained, and evaluated
Specification: The rejection for synthesis of sequences          using procedures that are opaque to (or kept secret from) the
that could be used in the production of pathogens, toxic         wider public. In other safety-critical industries, probabilistic
chemicals, or other substances potent to negatively af-          safety assessment means that the developer must specify
fect human health, and the identification and accep-             all the assumptions or premises needed to deduce that their
tance of the synthesis of sequences with potential for           system meets the required societal risk thresholds. These
applications that are conducive to human health and              assumptions can then be challenged by the regulator (and
flourishing.                                                     society at large) if they are not deemed socially acceptable.
                                                                 GS AI enables the same kind of oversight for AI systems.
World Model: The relationship between molecular
structures and pathology.                                        A further socio-technical benefit of GS AI is its potential for
                                                                 facilitating multi-stakeholder coordination. This is because
AI System: A “bioengineering agent” able to verify,              GS AI is able to produce proof certificates verifying that
for a given sequence, whether its risk of harmful ap-            a given solution conforms to auditable-to-all-parties speci-
plications remains below a conservatively specified              fications, in a way that requires minimal trust among said
bound.                                                           parties. It is well known among scholars and practitioners in
                                                                 International Relations that such a low-trust verification abil-
Example 4.8 (Stabilisation of the Climate System).               ity is a critical ingredient to multi-stakeholder coordination.
Problem: The emission of greenhouse gases threatens              For example, the successful ratification of several interna-
to throw out of balance the climate system, leading to           tional nuclear treaties has, to a significant extent, been made
increasingly averse climate conditions and threatening           possible because the respective parties are able to verify that
to destroy the health and livability of the ecosystem.           each the others’ nuclear activities are not being retargeted
Specification: Ensure the stability of the climate sys-          to military purposes.



                                                            15
                                                  Towards Guaranteed Safe AI

A third benefit of the GS research agenda is that it may                empirical evaluations, but also more ambitious approaches,
produce AI safety solutions whose costs are amortised over              such as those presented by the GS AI framework. Further-
time. Any potential safety measure (in AI or elsewhere)                 more, quick partial successes in GS AI are both plausible
faces the issue that if said safety measure is costly to im-            and useful. For example, provably compliant cybersecurity,
plement, then there is an incentive to disregard it. This               geofencing, remote kill switches, verified sensors and actu-
reduces the value of approaches to AI safety that impose                ators, etc., may all be feasible even if the most ambitious
a high “safety tax”. For example, a comprehensive suite                 proposals within the GS AI agenda are not, and would still
of rigorous empirical evaluations may be expensive and                  provide benefits in their own right. Beyond the need for the
time-consuming to carry out, and this cost would (presum-               best available protections against risks at any point in time,
ably) have to be paid again for each new AI system that                 it is also advisable to seek “defence in depth” – a term often
is created. This would in turn create an incentive to save              used in safety engineering and cybersecurity, advocating for
resources by cutting corners. By contrast, some approaches              the idea of deploying multiple layers of protection in order
to GS AI may allow for most of these costs to be amortised,             to defend against complex threats.
which may substantially reduce the incentive to disregard
                                                                        In this spirit, an important further aspect of a GS AI in
the corresponding safety measures. Once satisfactory safety
                                                                        practice is its deployment infrastructure. In particular, it
specifications have been identified and scalable methods
                                                                        might be desirable to monitor the AI system at runtime, and
for formal verification have been developed, new AI sys-
                                                                        check for signs that the world model is inaccurate. If such
tems could likely be verified against these specifications at
                                                                        signs are detected then the AI system could be disabled,
a much lower marginal cost. Such solutions would also be
                                                                        to ensure that there is no unaccounted for risk of unsafe
more scalable in view of the impressive speed of AI progress
                                                                        behaviour. It is worth noting that in cases where a system is
that otherwise threatens to outpace progress in safety.
                                                                        safety critical, it may not be possible or desirable to simply
The range of applications for GS AI solutions, and with                 shut it down. For example, it would not be safe to disable
that also the scope of potential benefits, is large. A particu-         the controller of a self-driving car while the car is in use. A
larly significant type of application, which seems thus worth           GS AI system should therefore have a trustworthy backup
highlighting in the current context, is the securing of critical        system, appropriate for its domain of use, that can safely
infrastructure such as water supply, power grids, nuclear               transition the system to a safe state if the main AI controller
plants, dams, information and communication technology,                 is disabled. Enabling such rapid automatic response to
etc. Cybervulnerability of critical infrastructure may be one           observations that invalidate the predictions of the world
of the biggest threat vectors for catastrophic risks in the             model, the deployment infrastructure can therefore grant
current world. For example, the US Cyber Security and                   additional safety. Also note that GS AI systems themselves
Infrastructure Security Agency (CISA) states that the “in-              may be useful for creating bug-free software and tamper-
capacitation or destruction [of critical infrastructure] would          proof hardware that could be used in backup systems.
have a debilitating effect on security, national economic
                                                                        Via the deployment infrastructure, we can modulate the time
security, national public health or safety, or a combination
                                                                        horizon at which the verified AI output is deployed. For
thereof”.13 GS AI approaches have the potential to play a
                                                                        example, at one level, the AI system may be deployed to
critical role in securing such critical infrastructure, thereby
                                                                        operate autonomously with an infinite time horizon. To
drastically bolstering civilisational resilience to both acci-
                                                                        increase the reliability of safety guarantees, one may instead
dents and adversarial threats.
                                                                        choose to deploy an AI system for a finite time horizon,
We also want to emphasise that there is a spectrum of ap-               such that, if at the end of that time horizon the AI system
proaches for safety assessments, ranging from easy ones                 is not successfully verified for redeployment, operations
that provide weaker safety assurances (such as evaluations              shut down or transition to a safe mode. The deployment
and red teaming) to more expensive procedures that provide              systems can therefore also allow us to shorten the time
stronger safety guarantees (such as the approaches within               horizon of outputs that need to be verified, thereby reducing
the GS AI spectrum). Given the uncertainty about when                   the complexity of verification and increasing its tractability.
each of the ASL safety levels will be crossed, we need an
                                                                        Moreover, while we have argued for the need for verifiable
“anytime” portfolio approach of R&D efforts spanning this
                                                                        quantitative safety guarantees, it is important to note that GS
spectrum. This will allow us to maximise the expected ef-
                                                                        AI may not be the only route to achieving such guarantees.
fectiveness of the feasible safety techniques at each stage.
                                                                        An alternative approach might be to extract interpretable
This would involve investing in cheaper techniques, such as
                                                                        policies from black-box algorithms via automated mecha-
  13                                                                    nistic interpretability and directly proving safety guarantees
     Retrieved from https://www.cisa.gov/topics/
critical-infrastructure-security-and-                                   about these policies. This approach differs from GS AI in
resilience/critical-infrastructure-sectors                              that it does not make use of a world model that is separate
on May 10, 2024.


                                                                   16
                                                  Towards Guaranteed Safe AI

from the policy; instead, it requires that the policy can itself        (O’Keefe & O’Leary, 1993), to develop methods for formal
be made interpretable. This strategy may be easier if it is in-         verification of neural networks and other machine learning
tractably difficult to create a sufficiently good world model           systems. This literature has proposed a range of algorithms
or adequate methods for doing formal verification relative              which can be used to ensure that a given neural network
to that world model. However, it may also be more difficult,            (potentially belonging to some restricted class) satisfies a
especially because the policy may be more complex than                  given specification (typically specified over its interfaces), or
the world model. For example, the rules of chess are less               that a system containing neural components satisfies a safety
complex than a policy which is good at chess, and it is much            specification. It would not be possible for us to provide a
easier to specify the axioms of Euclidean geometry than it              comprehensive overview of these algorithms here, but for
is to specify a computer program that is good at proving                an introduction, see e.g. Seshia et al. (2022); Albarghouthi
theorems about Euclidean geometry. In a similar way, it                 (2021).
may be much easier to create an interpretable world model
                                                                        Program Synthesis. Another area of computer science
than to create a performant interpretable policy. However,
                                                                        that is relevant to GS AI is the literature on correct-by-
it is ultimately an empirical question whether it is easier to
                                                                        construction program synthesis (Alur et al., 2013; Abate
create interpretable world models or interpretable policies
                                                                        et al., 2020). This is an approach to software develop-
in a given domain of operation.
                                                                        ment that aims to produce programs that are guaranteed
                                                                        to be correct with respect to their specifications from the
6. Relevant Existing Work                                               outset, rather than relying on traditional testing and de-
                                                                        bugging methods to identify and fix errors after the fact.
In this section, we briefly provide an overview on some
                                                                        The core idea behind correct-by-construction synthesis is
existing work that GS AI approaches build on, or which are
                                                                        to use formal methods to systematically construct programs
otherwise relevant to or related to the GS AI agenda. Note
                                                                        that satisfy a given set of formal specifications or correct-
that we do not mean to claim novelty with respect to the
                                                                        ness properties. This is typically achieved by encoding the
three-component architecture - for example, arguably the
                                                                        specifications as logical formulas or constraints, and then
first system with separate components for world-modelling,
                                                                        using automated solvers or synthesis algorithms to derive
specification, and verification was the (GPS), published
                                                                        programs that provably satisfy those constraints. Many
by (Newell & Simon, 1961). Instead, this position paper
                                                                        contemporary program synthesis methods involve learning
seeks to identify the convergence between several existing
                                                                        algorithms, e.g., using neural network heuristics, guided by
approaches, provide a taxonomy, and outline a high-level
                                                                        oracles such as formal verifiers or LLMs to accerelate the
research agenda towards achieving high-assurance quantita-
                                                                        learning process (Ellis et al., 2023; Grand et al., 2023). For
tive safety guarantees.
                                                                        an overview, see e.g. Gulwani et al. (2017); Jha & Seshia
Computational Learning Theory. The field of computa-                    (2017); Edwards et al. (2023).
tional learning theory (CLT) is concerned with the mathe-
                                                                        Model-Based Reasoning and Planning. Related to pro-
matical analysis of learning algorithms and learning prob-
                                                                        gram synthesis are the fields of automated theorem proving
lems. These investigations have produced various formal
                                                                        (Loveland, 2016) and automated planning (Ghallab et al.,
guarantees for large classes of learning algorithms, primarily
                                                                        2004). Both areas study methods for efficient automated
in the form of generalisation guarantees and regret bounds.
                                                                        reasoning over formal models, with the former focused on
These bounds typically show that a given learning algorithm
                                                                        reasoning over mathematical theories and program logics,
under some given circumstances is guaranteed to attain a
                                                                        and with the latter, by analogy (Fikes & Nilsson, 1971),
given level of performance with at least some given proba-
                                                                        focused on reasoning over theories of physical or virtual
bility, and may also show how these probabilities scale in
                                                                        worlds. Automated theorem proving is important for GS
terms of the amount of training data, etc (see e.g. Kearns &
                                                                        AI due to the role it plays in the verifier component, while
Vazirani, 1994). Like the GS approach to AI safety, CLT is
                                                                        automated planning can be used to deduce plans (rather
also concerned with deriving formal guarantees for AI sys-
                                                                        than programs) which are correct-by-construction. This
tems. However, CLT is typically concerned with guarantees
                                                                        means that automated planners can serve as self-verifying
concerning narrow performance metrics, whereas we are ad-
                                                                        AI systems by generating plans that both reach a goal and
ditionally concerned with specifications that would provide
                                                                        satisfy a formal safety specification. A limitation of classical
strong safety assurances for advanced systems operating in
                                                                        automated planners is that they operate over deterministic
open-ended environments.
                                                                        world models which only admit Boolean variables. How-
Formal Verification of AI Systems. There is also a large                ever, planning algorithms have also been extended to work
literature on formal verification of AI-enabled systems. This           with (partially observable) stochastic world models (Bonet
builds on more classic work on formal verification of control           & Geffner, 2009), with correctness maintained in the form
policies (e.g., (Tabuada, 2009)) and classical expert systems           of asymptotic convergence guarantees (Bonet & Geffner,

                                                                   17
                                                      Towards Guaranteed Safe AI

2003) or guaranteed bounds (McMahan et al., 2005).                          GS AI faces serious technical challenges. Creating accu-
                                                                            rate and interpretable world models, formulating precise
Probabilistic Programming. To specify or learn world
                                                                            safety specifications, and performing formal verification
models which are interpretable and expressive enough for
                                                                            at scale are all difficult problems. However, we have sug-
GS AI, an appropriately rich formal representation is neces-
                                                                            gested potential strategies and research directions for mak-
sary. Probabilistic programming provides one such formal
                                                                            ing progress on these problems. Furthermore, the GS ap-
representation, allowing world models to be specified as
                                                                            proach may be necessary given the serious limitations of
(possibly Turing-complete) programs that integrate prob-
                                                                            other methods such as empirical testing and interpretabil-
abilistic uncertainty, symbolic code, and learned differen-
                                                                            ity. That said, given the complexity and importance of the
tiable components (Milch et al., 2007; Goodman et al., 2012;
                                                                            challenge ahead, we think that these different approaches
Bingham et al., 2019; Cusumano-Towner et al., 2019; Fre-
                                                                            should be seen as comprising a portfolio of complementary
mont et al., 2019). Recent advances in probabilistic pro-
                                                                            R&D efforts, which can be combined in ways that improve
gramming have also led to more general and scalable meth-
                                                                            on the overall safety of a system.
ods for Bayesian inference (Baydin et al., 2019b; Lew et al.,
2023b), probabilistic program synthesis (Saad et al., 2023),                We believe the GS agenda is crucial for ensuring robust and
and automatic differentiation of expected values (Lew et al.,               reliable safety in advanced AI systems. While empiricism
2023a), which may serve as key enablers for learning and                    and interpretability are useful tools, they do not provide
refining world models from data.                                            the strong safety assurances that formal verification can.
                                                                            Although formal verification is challenging, the GS research
Safety Engineering. GS AI is more broadly related to the
                                                                            program offers a promising path toward making it feasible
field of safety engineering, an area of engineering science
                                                                            at scale. Value is to be had from narrow or partial solutions
that focuses on identifying, evaluating, and mitigating po-
                                                                            all the way to more ambitious applications of GS AI.
tential hazards and risks associated with various systems
and processes. For an overview of the techniques used in                    Much work remains to fully develop the GS approach. But
this field, see e.g. Ericson (2015); Leveson (2012); Dhillon                given its importance for avoiding AI risks, we argue that
(2003). See also Khlaaf (2023) for a discussion of safety                   the GS agenda deserves substantially more attention and re-
engineering concepts in the context of AI safety, and how                   sources than it currently receives. With a concerted research
ensuring the safety of AI systems differs from the concept                  effort on the core technical problems, significant progress
of AI value alignment.                                                      could be made. We hope this paper provides a useful starting
                                                                            point and motivation for a wider pursuit of the GS program.
Boxing Methods. A core feature of GS AI is that the AI
system is prevented from interacting with the world “di-
rectly”, in the sense that any output must be approved by the               8. Author contributions and
verifier.14 This may remind some readers of work exploring                     Acknowledgements
the idea of “boxing” a powerful AI system to prevent it
from causing harm (Armstrong et al., 2012; Armstrong &                      David ’davidad’ Dalrymple and Joar Skalse were the lead
O’Rorke, 2018; Armstrong & Levinstein, 2017; Turchin,                       drafters and authors. Yoshua Bengio, Stuart Russell, Max
2021). This raises the question how GS AI is similar and/or                 Tegmark, Sanjit A. Seshia, Steve Omohundro and Christian
different from such “AI boxing”, and whether it suffers from                Szegedy are core authors. Contributing authors include
the same challenges (e.g. Pepp et al., 2022). While there is                Alessandro Abate, Joseph Y. Halpern, Clark Barrett, Ding
a similarity between these approaches, a key difference is                  Zhao, Tan Zhi-Xuan, Jeannette Wing, Joshua B. Tenenbaum,
that, while prior AI boxing proposals tend to seek to limit                 Nora Ammann, and Ben Goldhaber. Ben Goldhaber and
the AI’s ability to affect the world by limiting its type of                Nora Ammann led the coordination of the project.
interaction channels, the “gate” implemented by the GS AI                   We would further like to thank Anca Dragan, Adam Gleave,
architectures is the formal verification of the AI’s output.                Adam Marblestone, Zac Hatfield-Dodds, Heidy Khlaaf,
                                                                            Adam Marblestone, and Vikash Mansinghka for their valu-
7. Conclusion                                                               able contributions and feedback on the idea and paper.

In this paper, we have introduced and defined the concept of                Yoshua Bengio, Stuart Russell, Max Tegmark, and David
guaranteed safe (GS) AI. GS AI aims to ensure the safety of                 ’davidad’ Dalrymple would like to thank the UK AI Safety
AI systems by equipping them with formal, verifiable and                    Institute for hosting the Bletchley Summit, where they ob-
auditable safety guarantees.                                                tained common knowledge of their AI safety agendas’ sim-
                                                                            ilarities, which was a key causal factor in this paper’s cre-
   14
      Though note that both static and runtime verification are part        ation.
of the GS AI spectrum.
                                                                            David ’davidad’ Dalrymple would like to thank Eric


                                                                       18
                                                Towards Guaranteed Safe AI

Drexler for formulating the Open Agency Model (Drexler,              Armstrong, S. and Mindermann, S. Occam’s razor is in-
2023), which previously conceptualised safe AI systems                 sufficient to infer the preferences of irrational agents. In
as composed of interacting parts with separation of con-               Proceedings of the 32nd International Conference on
cerns between specification, problem-solving, and solution-            Neural Information Processing Systems, volume 31, pp.
checking.                                                              5603–5614, Montréal, Canada, 2018. Curran Associates,
                                                                       Inc., Red Hook, NY, USA.
References                                                           Armstrong, S. and O’Rorke, X. Good and safe uses of ai
Abate, A., Bessa, I., Cattaruzza, D., Cordeiro, L., David,             oracles, 2018.
  C., Kesseli, P., Kroening, D., and Polgreen, E. Auto-              Armstrong, S. and O’Rourke, X. ’indifference’ methods for
  mated formal synthesis of provably safe digital controllers          managing agent rewards, 2018.
  for continuous plants. Acta Informatica, 57(3):223–244,
  2020.                                                              Armstrong, S., Sandberg, A., and Bostrom, N. Thinking
                                                                       inside the box: Controlling and using an oracle ai. Minds
Abate, A., Edwards, A., Giacobbe, M., Punchihewa, H., and              and Machines, 22:299–324, 2012.
  Roy, D. Quantitative verification with neural networks.
  Schloss Dagstuhl – Leibniz-Zentrum für Informatik,                Asimov, I. Runaround. Astounding Science Fiction, 1942.
  2023. doi: 10.4230/LIPICS.CONCUR.2023.22. URL                      Baier, C. and Katoen, J.-P. Principles of Model Checking.
  https://drops.dagstuhl.de/entities/                                  The MIT Press, 2008. ISBN 026202649X.
  document/10.4230/LIPIcs.CONCUR.2023.
  22.                                                                Baydin, A. G., Shao, L., Bhimji, W., Heinrich, L., Meadows,
                                                                       L., Liu, J., Munk, A., Naderiparizi, S., Gram-Hansen,
Alaga, J. and Schuett, J. Coordinated pausing: An                      B., Louppe, G., Ma, M., Zhao, X., Torr, P., Lee, V.,
  evaluation-based coordination scheme for frontier ai de-             Cranmer, K., Prabhat, and Wood, F. Etalumis: bring-
  velopers, 2023.                                                      ing probabilistic programming to scientific simulators at
                                                                       scale. In Proceedings of the International Conference for
Albarghouthi, A. Introduction to neural network verification,
                                                                       High Performance Computing, Networking, Storage and
  2021.
                                                                       Analysis, SC ’19, New York, NY, USA, 2019a. Associa-
Alpern, B. and Schneider, F. B. Recognizing safety and                 tion for Computing Machinery. ISBN 9781450362290.
  liveness. Distributed Comput., 2(3):117–126, 1987.                   doi: 10.1145/3295500.3356180. URL https://doi.
                                                                       org/10.1145/3295500.3356180.
Alur, R., Bodik, R., Juniwal, G., Martin, M. M. K.,
  Raghothaman, M., Seshia, S. A., Singh, R., Solar-                  Baydin, A. G., Shao, L., Bhimji, W., Heinrich, L., Meadows,
  Lezama, A., Torlak, E., and Udupa, A. Syntax-guided                  L., Liu, J., Munk, A., Naderiparizi, S., Gram-Hansen,
  synthesis. In Proceedings of the IEEE International Con-             B., Louppe, G., Ma, M., Zhao, X., Torr, P., Lee, V.,
  ference on Formal Methods in Computer-Aided Design                   Cranmer, K., Prabhat, and Wood, F. Etalumis: bring-
  (FMCAD), pp. 1–17, October 2013.                                     ing probabilistic programming to scientific simulators at
                                                                       scale. In Proceedings of the International Conference for
Amodei, D. Written testimony of Dario Amodei before the                High Performance Computing, Networking, Storage and
 U.S. Senate Committee on the Judiciary, Subcommitee                   Analysis, SC ’19, New York, NY, USA, 2019b. Associa-
 on Privacy, Technology, and the Law, 2023. URL                        tion for Computing Machinery. ISBN 9781450362290.
 https://www.judiciary.senate.gov/imo/                                 doi: 10.1145/3295500.3356180. URL https://doi.
 media/doc/2023-07-26_-_testimony_-                                    org/10.1145/3295500.3356180.
 _amodei.pdf.
                                                         Beckers, S., Chockler, H., and Halpern, J. A causal
                                                           analysis of harm. In Koyejo, S., Mohamed, S., Agar-
Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schul-
 man, J., and Mané, D. Concrete problems in ai safety.    wal, A., Belgrave, D., Cho, K., and Oh, A. (eds.),
 arXiv preprint arXiv:1606.06565, 2016.                    Advances in Neural Information Processing Systems,
                                                           volume 35, pp. 2365–2376. Curran Associates, Inc.,
Anthropic. Anthropic’s responsible scaling policy, 2023.   2022a. URL https://proceedings.neurips.
  URL       https://www-cdn.anthropic.com/                 cc/paper_files/paper/2022/file/
 1adf000c8f675958c2ee23805d91aaade1cd4613/ 100c1f131893d3b4b34bb8db49bef79f-
  responsible-scaling-policy.pdf.                          Paper-Conference.pdf.
Armstrong, S. and Levinstein, B. Low impact artificial               Beckers, S., Chockler, H., and Halpern, J. Y. Quantifying
  intelligences, 2017.                                                 harm, 2022b.

                                                                19
                                                Towards Guaranteed Safe AI

Bengio, Y. Written testimony of Yoshua Bengio before the             Broeck, W. V. d., Gioannini, C., Gonçalves, B., Quag-
  U.S. Senate Committee on the Judiciary, Subcommitee                  giotto, M., Colizza, V., and Vespignani, A. The gleamviz
  on Privacy, Technology, and the Law, 2023. URL                       computational tool, a publicly available software to
  https://www.judiciary.senate.gov/imo/                                explore realistic epidemic spreading scenarios at the
  media/doc/2023-07-26_-_testimony_-                                   global scale. BMC Infectious Diseases, 11(1):37, Feb
  _bengio.pdf.                                                         2011. ISSN 1471-2334. doi: 10.1186/1471-2334-11-37.
                                                                       URL https://doi.org/10.1186/1471-2334-
Bengio, Y.      Towards a cautious scientist AI
                                                                       11-37.
  with convergent safety bounds, 2024.      URL
  https://yoshuabengio.org/2024/02/                                  Brookes, S. D. and Roscoe, A. W. An improved failures
  26/towards-a-cautious-scientist-ai-                                  model for communicating processes. In International
  with-convergent-safety-bounds/.                                      Conference on Concurrency. Berlin, Heidelberg. Springer,
                                                                       1984.
BenThacker, Andereson, C., Senseny, P., and Rodriguez,
  E. The role of nondeterminism in model verification                Brookes, S. D., Hoare, C. A., and Roscoe, A. W. A theory
  and validation. International Journal of Materials and               of communicating sequential processes. Journal of the
  Product Technology, 25(1-3), 2006.                                   ACM, 31(3):560–599, 1984.
Bhatia, S., Qiu, J., Hasabnis, N., Seshia, S. A., and Cheung,        Brundage, M., Avin, S., Clark, J., Toner, H., Eckersley, P.,
  A. Verified code transpilation with LLMs. 2024.                      Garfinkel, B., Dafoe, A., Scharre, P., Zeitzoff, T., Filar, B.,
Bingham, E., Chen, J. P., Jankowiak, M., Obermeyer, F.,                Anderson, H., Roff, H., Allen, G. C., Steinhardt, J., Flynn,
  Pradhan, N., Karaletsos, T., Singh, R., Szerlip, P., Hors-           C., hEigeartaigh, S. O., Beard, S., Belfield, H., Farquhar,
  fall, P., and Goodman, N. D. Pyro: Deep universal prob-              S., Lyle, C., Crootof, R., Evans, O., Page, M., Bryson,
  abilistic programming. Journal of machine learning re-               J., Yampolskiy, R., and Amodei, D. The malicious use
  search, 20(28):1–6, 2019.                                            of artificial intelligence: Forecasting, prevention, and
                                                                       mitigation, 2018.
Bloomfield, R., Khlaaf, H., Conmy, P. R., and Fletcher, G.
  Disruptive innovations and disruptive assurance: Assur-            Brynjolfsson, E. and Ng, A. Big ai can centralize decision-
  ing machine learning and autonomy. Computer, 52/9:                   making and power, and that’s a problem. Missing links in
  82–89, 2019.                                                         ai governance, 65, 2023.

Bonet, B. and Geffner, H. Labeled rtdp: Improving the con-           Buolamwini, J. and Gebru, T. Gender shades: Intersec-
  vergence of real-time dynamic programming. In ICAPS,                 tional accuracy disparities in commercial gender classi-
  volume 3, pp. 12–21, 2003.                                           fication. In Conference on fairness, accountability and
                                                                       transparency, pp. 77–91. PMLR, 2018.
Bonet, B. and Geffner, H. Solving pomdps: Rtdp-bel
  vs. point-based algorithms. In IJCAI, pp. 1641–1646.               Burgess, M. The hacking of chatgpt is just getting started,
  Pasadena CA, 2009.                                                   Apr 2023. URL wired.com/story/chatgpt-
                                                                       jailbreak-generative-ai-hacking/. [On-
Bostrom, N. Existential risks: Analyzing human extinction              line; posted 12-April-2023].
  scenarios and related hazards. Journal of Evolution and
  technology, 9, 2002.                                               Butler, S. Darwin among the machines. 1863.
Bostrom, N. Superintelligence: Paths, Dangers, Strate-               Cao, H., Cohen, S. N., and Szpruch, L. Identifiabil-
  gies.   Oxford University Press, 2014.        ISBN                   ity in inverse reinforcement learning. arXiv preprint,
  9780199678112. URL https://books.google.                             arXiv:2106.03498 [cs.LG], 2021.
  com/books?id=7_H8AwAAQBAJ.
                                                                     Carroll, M., Dragan, A., Russell, S., and Hadfield-Menell,
Boxell, L., Gentzkow, M., and Shapiro, J. M. Cross-country             D. Estimating and penalizing induced preference shifts
  trends in affective polarization. Working Paper 26669,               in recommender systems, 2022.
  National Bureau of Economic Research, January 2020.
  URL http://www.nber.org/papers/w26669.                             Carroll, S. M. The quantum field theory on which the
                                                                       everyday world supervenes, 2021.
Bricken, T., Templeton, A., Batson, J., Chen, B., Jermyn, A.,
  Conerly, T., Turner, N., Anil, C., Denison, C., Askell, A.,        Casper, S., Davies, X., Shi, C., Gilbert, T. K., Scheurer, J.,
  et al. Towards monosemanticity: Decomposing language                 Rando, J., Freedman, R., Korbak, T., Lindner, D., Freire,
  models with dictionary learning. Transformer Circuits                P., Wang, T., Marks, S., Segerie, C.-R., Carroll, M., Peng,
  Thread, pp. 2, 2023.                                                 A., Christoffersen, P., Damani, M., Slocum, S., Anwar,

                                                                20
                                                Towards Guaranteed Safe AI

  U., Siththaranjan, A., Nadeau, M., Michaud, E. J., Pfau,           Dhillon, B. Engineering Safety: Fundamentals, Tech-
  J., Krasheninnikov, D., Chen, X., Langosco, L., Hase,                niques, And Applications. Series On Industrial And Sys-
  P., Bıyık, E., Dragan, A., Krueger, D., Sadigh, D., and              tems Engineering. World Scientific Publishing Company,
  Hadfield-Menell, D. Open problems and fundamental lim-               2003. ISBN 9789813102361. URL https://books.
  itations of reinforcement learning from human feedback,              google.co.uk/books?id=P_E7DQAAQBAJ.
  2023.
                                                                     Dreossi, T., Ghosh, S., Yue, X., Keutzer, K., Sangiovanni-
Censi, A., Slutsky, K., Wongpiromsarn, T., Yershov, D.,                Vincentelli, A., and Seshia, S. A. Counterexample-guided
  Pendleton, S., Fu, J., and Frazzoli, E. Liability, ethics,           data augmentation. In 27th International Joint Confer-
  and culture-aware behavior specification using rulebooks.            ence on Artificial Intelligence (IJCAI), 2018.
  In 2019 International Conference on Robotics and Au-
  tomation (ICRA), pp. 8536–8542. IEEE, 2019.                        Dreossi, T., Donzé, A., and Seshia, S. A. Compositional fal-
                                                                       sification of cyber-physical systems with machine learn-
Cohen, M., Hutter, M., and Osborne, M. Advanced artificial             ing components. Journal of Automated Reasoning, 63(4):
  agents intervene in the provision of reward. AI magazine,            1031–1053, 2019.
  43(3):282–293, 2022.
                                                                     Drexler, E. The open agency model, February 2023. URL
Cook, W.        Bridge failure rates, consequences,                    https://www.alignmentforum.org/posts/
  and predictive trends.     2014.    URL https:                       5hApNw5f7uG8RXxGS/the-open-agency-
  //api.semanticscholar.org/CorpusID:                                  model. [Online; posted 22-February-2023].
  107360532.
                                                                     Dvijotham, K. and Todorov, E. Inverse optimal control with
Crawford, K. The atlas of AI: Power, politics, and the                 linearly-solvable MDPs. In Proceedings of the 27th Inter-
  planetary costs of artificial intelligence. Yale University          national Conference on Machine Learning, pp. 335–342,
  Press, 2021.                                                         Haifa, Israel, June 2010. Omnipress, Madison, Wisconsin,
Cusumano-Towner, M. F., Saad, F. A., Lew, A. K., and                   USA.
  Mansinghka, V. K. Gen: a general-purpose probabilis-               Edwards, A., Peruffo, A., and Abate, A. A general verifi-
  tic programming system with programmable inference.                  cation framework for dynamical and control models via
  In Proceedings of the 40th acm sigplan conference on                 certificate synthesis, 2023.
  programming language design and implementation, pp.
  221–236, 2019.                                                     Ellis, K., Wong, L., Nye, M., Sable-Meyer, M., Cary, L.,
                                                                       Anaya Pozo, L., Hewitt, L., Solar-Lezama, A., and Tenen-
Das, S., Stanton, R., and Wallace, N. Algorithmic                      baum, J. B. Dreamcoder: growing generalizable, inter-
  fairness. Annual Review of Financial Economics, 15                   pretable knowledge with wake–sleep bayesian program
  (Volume 15, 2023):565–593, 2023. ISSN 1941-1375.                     learning. Philosophical Transactions of the Royal Society
  doi: https://doi.org/10.1146/annurev-financial-110921-               A, 381(2251):20220050, 2023.
 125930. URL https://www.annualreviews.
  org/content/journals/10.1146/annurev-                              Elmaaroufi, K., Shankar, D., Cismaru, A., Vazquez-
  financial-110921-125930.                                             Chanlatte, M., Sangiovanni-Vincentelli, A., Zaharia, M.,
                                                                       and Seshia, S. A. Generating probabilistic scenario pro-
’davidad’ Dalrymple, D. Safeguarded ai: constructing guar-             grams from natural language. ArXiV e-Prints 2405.03709,
   anteed safety. Technical report, ARIA, feb 2024. URL                2024.
   https://www.aria.org.uk/wp-content/
   uploads/2024/01/ARIA-Safeguarded-AI-                              Ericson, C.   Hazard Analysis Techniques for Sys-
   Programme-Thesis-V1.pdf.                                            tem Safety. Wiley, 2015. ISBN 9781118940389.
                                                                       URL https://books.google.co.uk/books?
Del Moral, P., Doucet, A., and Jasra, A. Sequential monte              id=cTikBgAAQBAJ.
  carlo samplers. Journal of the Royal Statistical Society
  Series B: Statistical Methodology, 68(3):411–436, 2006.            Everitt, T., Carey, R., Langlois, E., Ortega, P. A., and Legg,
                                                                       S. Agent incentives: A causal perspective, 2021.
Deleu, T., Góis, A., Emezue, C., Rankawat, M., Lacoste-
  Julien, S., Bauer, S., and Bengio, Y. Bayesian structure           Feldstein, S. The global expansion of AI surveillance, vol-
  learning with generative flow networks, 2022.                        ume 17. Carnegie Endowment for International Peace
                                                                       Washington, DC, 2019.
Deleu, T., Nishikawa-Toomey, M., Subramanian, J., Malkin,
  N., Charlin, L., and Bengio, Y. Joint bayesian inference           Fikes, R. E. and Nilsson, N. J. Strips: A new approach to
  of graphical structure and parameters with a single gener-           the application of theorem proving to problem solving.
  ative flow network, 2023.                                            Artificial intelligence, 2(3-4):189–208, 1971.

                                                                21
                                                 Towards Guaranteed Safe AI

First, E., Rabe, M., Ringer, T., and Brun, Y. Baldur: Whole-          Garion, C., Hattenberger, G., Pollien, B., Roux, P., and Thiri-
   proof generation and repair with large language models.              oux, X. Formal Verification for Autopilot - Preliminary
   In Proceedings of the 31st ACM Joint European Software               state of the art. Technical report, ISAE-SUPAERO ; ON-
  Engineering Conference and Symposium on the Founda-                   ERA – The French Aerospace Lab ; ENAC, March 2022.
   tions of Software Engineering, pp. 1229–1241, 2023.                  URL https://hal.science/hal-03255656.

FLI. AI governance scorecard and safety standards                     Ghallab, M., Nau, D., and Traverso, P. Automated Planning:
  policy, 2023. URL https://futureoflife.                               theory and practice. Elsevier, 2004.
  org/wp-content/uploads/2023/11/FLI_
  Governance_Scorecard_and_Framework.                                 Good, I. J. Speculations on perceptrons and other automata.
  pdf.                                                                  International Business Machines Corporation, 1959.

                                                                      Goodhart, C. Problems of monetary management: the UK
Freedman, R., Shah, R., and Dragan, A. Choice set mis-
                                                                        experience in papers in monetary economics. Monetary
  specification in reward inference. In IJCAI-PRICAI-20
                                                                       Economics, 1, 1975.
  Workshop on Artificial Intelligence Safety, 2020. doi:
  10.48550/ARXIV.2101.07691. URL https://arxiv.                       Goodman, N., Mansinghka, V., Roy, D. M., Bonawitz, K.,
  org/abs/2101.07691.                                                   and Tenenbaum, J. B. Church: a language for generative
                                                                        models. arXiv preprint arXiv:1206.3255, 2012.
Fremont, D. J., Dreossi, T., Ghosh, S., Yue, X., Sangiovanni-
  Vincentelli, A. L., and Seshia, S. A. Scenic: A language            Gothoskar, N., Cusumano-Towner, M., Zinberg, B.,
  for scenario specification and scene generation. In Pro-              Ghavamizadeh, M., Pollok, F., Garrett, A., Tenenbaum,
  ceedings of the 40th annual ACM SIGPLAN conference                   J., Gutfreund, D., and Mansinghka, V. 3dp3: 3d scene
  on Programming Language Design and Implementation                     perception via probabilistic programming. Advances in
  (PLDI), June 2019.                                                   Neural Information Processing Systems, 34:9600–9612,
                                                                        2021.
Fremont, D. J., Chiu, J., Margineantu, D. D., Osipychev,
  D., and Seshia, S. A. Formal analysis and redesign of a             Gothoskar, N., Ghavami, M., Li, E., Curtis, A., Noseworthy,
  neural network-based aircraft taxiing system with VerifAI.            M., Chung, K., Patton, B., Freeman, W. T., Tenenbaum,
  In 32nd International Conference on Computer Aided                    J. B., Klukas, M., and Mansinghka, V. K. Bayes3d: fast
  Verification (CAV), July 2020a.                                       learning and inference in structured generative models of
                                                                        3d objects and scenes, 2023.
Fremont, D. J., Kim, E., Pant, Y. V., Seshia, S. A., Acharya,
  A., Bruso, X., Wells, P., Lemke, S., Lu, Q., and Mehta,             Grand, G., Wong, L., Bowers, M., Olausson, T. X., Liu,
  S. Formal scenario-based testing of autonomous vehicles:              M., Tenenbaum, J. B., and Andreas, J. Lilo: Learning
  From simulation to the real world. In 23rd IEEE Interna-              interpretable libraries by compressing and documenting
  tional Conference on Intelligent Transportation Systems               code. In The Twelfth International Conference on Learn-
  (ITSC), September 2020b.                                              ing Representations, 2023.

Fremont, D. J., Kim, E., Dreossi, T., Ghosh, S., Yue, X.,             Gulwani, S., Polozov, O., and Singh, R. Program syn-
  Sangiovanni-Vincentelli, A. L., and Seshia, S. A. Scenic:             thesis. Foundations and Trends® in Programming Lan-
  A language for scenario specification and data generation.            guages, 4(1-2):1–119, 2017. ISSN 2325-1107. doi:
  Machine Learning Journal, 2022.                                      10.1561/2500000010. URL http://dx.doi.org/
                                                                       10.1561/2500000010.
Ganguli, D., Lovitt, L., Kernion, J., Askell, A., Bai, Y., Ka-
  davath, S., Mann, B., Perez, E., Schiefer, N., Ndousse,             Guo, W., Tondi, B., and Barni, M. An overview of back-
  K., Jones, A., Bowman, S., Chen, A., Conerly, T., Das-                door attacks against deep neural networks and possible
  Sarma, N., Drain, D., Elhage, N., El-Showk, S., Fort, S.,             defences, 2021.
  Hatfield-Dodds, Z., Henighan, T., Hernandez, D., Hume,              Hadfield-Menell, D., Dragan, A., Abbeel, P., and Russell, S.
  T., Jacobson, J., Johnston, S., Kravec, S., Olsson, C.,               The off-switch game, 2017.
  Ringer, S., Tran-Johnson, E., Amodei, D., Brown, T.,
  Joseph, N., McCandlish, S., Olah, C., Kaplan, J., and               Hadfield-Menell, D., Dragan, A., Abbeel, P., and Russell, S.
  Clark, J. Red teaming language models to reduce harms:                Cooperative inverse reinforcement learning, 2024.
  Methods, scaling behaviors, and lessons learned, 2022.
                                                                      Halpern, J. Y. Actual Causality. MIT Press, Cambridge,
Gao, L. and Guan, L. Interpretability of machine learning:              MA, 2016. ISBN 978-0-262-03502-6. doi: 10.7551/
  Recent advances and future prospects, 2023.                           mitpress/9780262035026.001.0001.

                                                                 22
                                                Towards Guaranteed Safe AI

Halpern, J. Y. and Leung, S. Weighted sets of probabilities          Jacob, A. P., Shen, Y., Farina, G., and Andreas, J. The con-
  and minimax weighted expected regret: new approaches                 sensus game: Language model generation via equilibrium
  for representing uncertainty and making decisions. arXiv             search. arXiv preprint arXiv:2310.09139, 2023.
  preprint arXiv:1302.5681, 2013.
                                                                     Jenner, E. and Gleave, A. Preprocessing reward functions
Hansson, H. and Jonsson, B. A logic for reasoning                      for interpretability, 2022.
  about time and reliability. Form. Asp. Comput., 6(5):
  512–535, sep 1994. ISSN 0934-5043. doi: 10.1007/                   Jha, S. and Seshia, S. A. A Theory of Formal Synthesis
  BF01211866. URL https://doi.org/10.1007/                             via Inductive Learning. Acta Informatica, 54(7):693–726,
  BF01211866.                                                          2017.

Hasanbeig, H., Kroening, D., and Abate, A. Certified rein-           Ji, J., Qiu, T., Chen, B., Zhang, B., Lou, H., Wang, K., Duan,
  forcement learning with logic guidance. Artificial Intelli-           Y., He, Z., Zhou, J., Zhang, Z., Zeng, F., Ng, K. Y., Dai,
  gence, 322(C):103949, 2023. doi: 10.1016/j.artint.2023.               J., Pan, X., O’Gara, A., Lei, Y., Xu, H., Tse, B., Fu, J.,
 103949.                                                                McAleer, S., Yang, Y., Wang, Y., Zhu, S.-C., Guo, Y., and
                                                                        Gao, W. Ai alignment: A comprehensive survey, 2024.
Hendrycks, D., Mazeika, M., and Woodside, T. An overview
  of catastrophic ai risks, 2023.                                    Joy, B. Why the future doesn’t need us, 2000.

Hennessy, C. A. and Goodhart, C. A. E. Goodhart’s Law                Junges, S., Jansen, N., Dehnert, C., Topcu, U., and Ka-
  and Machine Learning: A Structural Perspective. In-                  toen, J.-P. Safety-constrained reinforcement learning for
  ternational Economic Review, pp. iere.12633, March                   MDPs. In Chechik, M. and Raskin, J.-F. (eds.), Tools and
  2023. ISSN 0020-6598, 1468-2354. doi: 10.1111/iere.                  Algorithms for the Construction and Analysis of Systems,
 12633. URL https://onlinelibrary.wiley.                               pp. 130–146, Berlin, Heidelberg, 2016. Springer Berlin
  com/doi/10.1111/iere.12633.                                          Heidelberg. ISBN 978-3-662-49674-9.

Hinton, G.    ‘the godfather of A.I.’ leaves Google                  Karwowski, J., Hayman, O., Bai, X., Kiendlhofer, K., Grif-
  and warns of danger ahead, May 2023.         URL                     fin, C., and Skalse, J. Goodhart’s law in reinforcement
  https://www.nytimes.com/2023/05/                                     learning, 2023.
  01/technology/ai-google-chatbot-
  engineer-quits-hinton.html.                [Online;                Ke, N. R., Chiappa, S., Wang, J., Goyal, A., Bornschein,
  posted 4-May-2023].                                                  J., Rey, M., Weber, T., Botvinic, M., Mozer, M., and
                                                                       Rezende, D. J. Learning to induce causal structure, 2022.
Hollmann, N., Müller, S., Eggensperger, K., and Hutter, F.
 TabPFN: A transformer that solves small tabular classifi-           Kearns, M. J. and Vazirani, U. An Introduction to Com-
  cation problems in a second, 2023.                                   putational Learning Theory. The MIT Press, 08 1994.
                                                                       ISBN 9780262276863. doi: 10.7551/mitpress/3897.
Hu, E. J., Malkin, N., Jain, M., Everett, K., Graikos, A.,             001.0001. URL https://doi.org/10.7551/
  and Bengio, Y. Gflownet-em for learning compositional                mitpress/3897.001.0001.
  latent variable models, 2023.
                                                                     Kemp, C., Tenenbaum, J. B., Niyogi, S., and Griffiths, T. L.
Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., and            A probabilistic model of theory formation. Cognition,
  Garrabrant, S. Risks from learned optimization in ad-                114(2):165–196, 2010.
 vanced machine learning systems, 2021.
                                                                     Khlaaf, H. Toward comprehensive risk assessments and
Hutter, M. A gentle introduction to the universal algorithmic          assurance of ai-based systems. Trail of Bits, 2023.
  agent aixi, 2003.
                                                                     Khlaaf, H., Mishkin, P., Achiam, J., Krueger, G., and
Ivanov, R., Carpenter, T. J., Weimer, J., Alur, R., Pap-               Brundage, M. A hazard analysis framework for code
  pas, G. J., and Lee, I. Case study: verifying the safety             synthesis large language models, 2022.
  of an autonomous racing car with a neural network
  controller. In Proceedings of the 23rd International               Kim, K., Garg, S., Shiragur, K., and Ermon, S. Reward
  Conference on Hybrid Systems: Computation and Con-                   identification in inverse reinforcement learning. In Pro-
  trol, HSCC ’20, New York, NY, USA, 2020. Associa-                    ceedings of the 38th International Conference on Ma-
  tion for Computing Machinery. ISBN 9781450370189.                    chine Learning, volume 139 of Proceedings of Machine
  doi: 10.1145/3365365.3382216. URL https://doi.                       Learning Research, pp. 5496–5505, Virtual, July 2021.
  org/10.1145/3365365.3382216.                                         PMLR.

                                                                23
                                                 Towards Guaranteed Safe AI

Kleinberg, J., Mullainathan, S., and Raghavan, M. Inherent            Lew, A. K., Huot, M., Staton, S., and Mansinghka, V. K.
  trade-offs in the fair determination of risk scores, 2016.            Adev: Sound automatic differentiation of expected values
                                                                        of probabilistic programs. Proceedings of the ACM on
Koessler, L. and Schuett, J. Risk assessment at agi com-                Programming Languages, 7(POPL):121–153, 2023a.
  panies: A review of popular risk assessment techniques
  from other safety-critical industries, 2023.                        Lew, A. K., Matheos, G., Zhi-Xuan, T., Ghavamizadeh,
Kosoy, V. Infra-bayesian physicalism: a formal theory                   M., Gothoskar, N., Russell, S., and Mansinghka,
  of naturalized induction, November 2021.       URL                    V. K. SMCP3: Sequential monte carlo with prob-
  https://www.alignmentforum.org/posts/                                 abilistic program proposals. In Ruiz, F., Dy, J.,
  gHgs2e2J5azvGFatb/infra-bayesian-                                     and van de Meent, J.-W. (eds.), Proceedings of The
  physicalism-a-formal-theory-of-                                       26th International Conference on Artificial Intelligence
  naturalized. [Online; posted 30-November-2021].                       and Statistics, volume 206 of Proceedings of Ma-
                                                                        chine Learning Research, pp. 7061–7088. PMLR, 25–
Krakovna, V., Uesato, J., Mikulik, V., Rahtz, M., Everitt,              27 Apr 2023b. URL https://proceedings.mlr.
  T., Kumar, R., Kenton, Z., Leike, J., and Legg, S.                    press/v206/lew23a.html.
  Specification gaming: the flip side of AI ingenuity, 2020.
  URL deepmind.com/blog/specification-                                Liell-Cock, J. and Staton, S. Compositional imprecise prob-
  gaming-the-flip-side-of-ai-ingenuity.                                 ability. arXiv preprint arXiv:2405.09391, 2024.

Lample, G., Conneau, A., Denoyer, L., and Ranzato, M.                 Liu, P., Du, Y., Wang, L., and Da Young, J. Ready to bully
  Unsupervised machine translation using monolingual cor-               automated vehicles on public roads? Accident Analysis
  pora only. arXiv preprint arXiv:1711.00043, 2017.                     and Prevention, 137, March 2020. ISSN 0001-4575. doi:
                                                                        10.1016/j.aap.2020.105457. Publisher Copyright: © 2020
Lample, G., Lachaux, M.-A., Lavril, T., Martinet, X., Hayat,
                                                                        Elsevier Ltd.
  A., Ebner, G., Rodriguez, A., and Lacroix, T. Hypertree
  proof search for neural theorem proving, 2022.                      London, A. J. and Heidari, H. Beneficent intelligence: A
Langosco, L., Koch, J., Sharkey, L., Pfau, J., Orseau, L., and          capability approach to modeling benefit, assistance, and
  Krueger, D. Goal misgeneralization in deep reinforce-                 associated moral failures through ai systems, 2023.
  ment learning, 2023.
                                                                      Loveland, D. W. Automated theorem proving: A logical
LaValle, S. M. and Hutchinson, S. A. Evaluating motion                  basis. Elsevier, 2016.
  strategies under nondeterministic or probabilistic uncer-
  tainties in sensing and control. Proceedings of IEEE                Manheim, D. and Garrabrant, S. Categorizing Variants of
  International Conference on Robotics and Automation, 4,              Goodhart’s Law, February 2019. URL http://arxiv.
  1996.                                                                org/abs/1803.04585. arXiv:1803.04585 [cs, q-fin,
                                                                       stat].
Lazar, S. and Nelson, A. Ai safety on whose terms?, 2023.
                                                                      Mao, J., Gan, C., Kohli, P., Tenenbaum, J. B., and Wu, J.
Leino, K. R. M. Program Proofs. MIT Press, 2023.                       The neuro-symbolic concept learner: Interpreting scenes,
Lelkes, Y., Sood, G., and Iyengar, S. The hostile audience:            words, and sentences from natural supervision. arXiv
  The effect of access to broadband internet on partisan               preprint arXiv:1904.12584, 2019.
  affect. American Journal of Political Science, 61(1):
                                                                      Matheos, G., Lew, A. K., Ghavamizadeh, M., Russell,
  5–20, 2017. ISSN 00925853, 15405907. URL http:
                                                                       S., Cusumano-Towner, M., and Mansinghka, V. Trans-
  //www.jstor.org/stable/26379489.
                                                                       forming worlds: Automated involutive mcmc for open-
Leveson, N. Engineering a Safer World: Systems Thinking                universe probabilistic models. In Third Symposium on
  Applied to Safety. 01 2012. ISBN 9780262298247. doi:                 Advances in Approximate Bayesian Inference, 2020.
  10.7551/mitpress/8179.001.0001.
                                                                      Mathews, J. and Schmidler, S. C. Finite sample complexity
Lew, A. K., Tessler, M. H., Mansinghka, V. K., and Tenen-              of sequential monte carlo estimators on multimodal target
  baum, J. B. Leveraging unstructured statistical knowl-               distributions, 2022.
  edge in a probabilistic language of thought. In CogSci
  2020: Proceedings of the Forty-Second Annual Virtual                McCullough, D. The Great Bridge: The Epic Story of
  Meeting of the Cognitive Science Society, Proceedings of             the Building of the Brooklyn Bridge. Simon & Schuster,
  the Annual Conference of the Cognitive Science Society,              2001. ISBN 9780743217378. URL https://books.
  2020.                                                                google.co.uk/books?id=bOM93rb22YEC.

                                                                 24
                                                Towards Guaranteed Safe AI

McMahan, H. B., Likhachev, M., and Gordon, G. J.                      Mutlu, O. and Kim, J. S. Rowhammer: A retrospective.
 Bounded real-time dynamic programming: Rtdp with                      IEEE Transactions on Computer-Aided Design of Inte-
 monotone upper bounds and performance guarantees.                     grated Circuits and Systems, 39(8):1555–1571, 2019.
 In Proceedings of the 22nd International Conference
 on Machine Learning, ICML ’05, pp. 569–576, New                      Neider, D. and Gavran, I. Learning linear temporal proper-
 York, NY, USA, 2005. Association for Computing                         ties, 2018.
 Machinery.    ISBN 1595931805.       doi: 10.1145/
                                                                      Newell, A. and Simon, H. A. Gps, a program that simulates
 1102351.1102423. URL https://doi.org/10.
                                                                        human thought. 1961.
 1145/1102351.1102423.
                                                                      Ng, A. Y. and Russell, S. Algorithms for inverse reinforce-
Megill, N. Proof Explorer - Home Page - Metamath,
                                                                        ment learning. In Proceedings of the Seventeenth Inter-
 September 2023. URL https://us.metamath.
                                                                        national Conference on Machine Learning, volume 1,
 org/mpeuni/mmset.html. [Online; accessed 3.
                                                                        pp. 663–670, Stanford, California, USA, 2000. Morgan
 Sep. 2023].
                                                                        Kaufmann Publishers Inc.
Memarian, B. and Doleck, T.            Fairness, account-
 ability, transparency, and ethics (fate) in artificial               Nieuwhof, G.      An introduction to fault tree analy-
 intelligence (ai) and higher education: A system-                      sis with emphasis on failure rate evaluation. Micro-
 atic review. Computers and Education: Artificial                       electronics Reliability, 14(2):105–119, 1975. ISSN
 Intelligence, 5:100152, 2023.         ISSN 2666-920X.                  0026-2714.       doi: 10.1016/0026-2714(75)90024-
 doi:        https://doi.org/10.1016/j.caeai.2023.100152.               4. URL https://www.sciencedirect.com/
 URL         https://www.sciencedirect.com/                             science/article/pii/0026271475900244.
 science/article/pii/S2666920X23000310.                               O’Keefe, R. M. and O’Leary, D. E. Expert system verifi-
Michaud, E. J., Gleave, A., and Russell, S. Understanding               cation and validation: a survey and tutorial. Artificial
 learned reward functions, 2020.                                        Intelligence Review, 7:3–42, 1993.

Michaud, E. J., Liao, I., Lad, V., Liu, Z., Mudide, A.,               OpenAI, :, Achiam, J., Adler, S., Agarwal, S., Ahmad, L.,
 Loughridge, C., Guo, Z. C., Kheirkhah, T. R., Vukelić,               Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J.,
 M., and Tegmark, M. Opening the ai black box: program                 Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Bal-
 synthesis via mechanistic interpretability. arXiv preprint             aji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M.,
 arXiv:2402.05110, 2024.                                                Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G.,
                                                                        Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman,
Milch, B., Marthi, B., Russell, S., Sontag, D., Ong, D. L.,            A.-L., Brockman, G., Brooks, T., Brundage, M., Button,
 and Kolobov, A. Blog: Probabilistic models with un-                    K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson,
 known objects. Statistical Relational Learning, pp. 373,               C., Carmichael, R., Chan, B., Chang, C., Chantzis, F.,
 2007.                                                                  Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess,
                                                                        B., Cho, C., Chu, C., Chung, H. W., Cummings, D., Cur-
Mingard, C., Skalse, J., Valle-Pérez, G., Martı́nez-Rubio,
                                                                        rier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N.,
 D., Mikulik, V., and Louis, A. A. Neural networks are a
                                                                        Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning,
 priori biased towards boolean functions with low entropy,
                                                                        S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus,
 2020.
                                                                        L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao, L.,
Mingard, C., Valle-Pérez, G., Skalse, J., and Louis, A. A. Is          Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G.,
 sgd a bayesian sampler? well, almost. Journal of Machine               Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S.,
 Learning Research, 22(79):1–64, 2021. URL http:                        Greene, R., Gross, J., Gu, S. S., Guo, Y., Hallacy, C., Han,
 //jmlr.org/papers/v22/20-676.html.                                    J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse,
                                                                        C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B.,
Minsky, M. Afterword to Vernor Vinge’s novel,“True name.                Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S.,
 1986.                                                                 Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S.,
Mio, M., Sarkis, R., and Vignudelli, V. Combining nonde-               Jonn, B., Jun, H., Kaftan, T., Łukasz Kaiser, Kamali, A.,
 terminism, probability, and termination: equational and                Kanitscheider, I., Keskar, N. S., Khan, T., Kilpatrick, L.,
 metric reasoning. 36th Annual ACM/IEEE Symposium                       Kim, J. W., Kim, C., Kim, Y., Kirchner, J. H., Kiros, J.,
 on Logic in Computer Science (LICS), 52/9:1–14, 2021.                  Knight, M., Kokotajlo, D., Łukasz Kondraciuk, Kondrich,
                                                                       A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V.,
Moravec, H. ind Children: The Future of Robot and Human                 Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D.,
 Intelligence. Harvard University Press, 1988.                          Li, C. M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T.,

                                                                 25
                                                 Towards Guaranteed Safe AI

  Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning,               UK, 2 edition, 2009. ISBN 978-0-521-89560-6. doi:
  S., Markov, T., Markovski, Y., Martin, B., Mayer, K.,                 10.1017/CBO9780511803161.
  Mayne, A., McGrew, B., McKinney, S. M., McLeavey, C.,
  McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick,            Pearl, J.     Judea pearl: Causal reasoning, coun-
  J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V.,                terfactuals, and the path to agi, 2019.    URL
  Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O.,              https://youtu.be/pEBI0vF45ic?si=lE_
  Mély, D., Nair, A., Nakano, R., Nayak, R., Neelakantan,              gCwZAFfDU7GG2&t=3869.
  A., Ngo, R., Noh, H., Ouyang, L., O’Keefe, C., Pachocki,            Pepp, J., Sterken, R., McKeever, M., and Michaelson, E.
  J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo,             Manipulative machines (1st edition). In Klenk, M. and
  G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng,          Jongepier, F. (eds.), The Philosophy of Online Manipula-
  A., Perelman, A., de Avila Belbute Peres, F., Petrov, M.,             tion, pp. 91–107. Routledge, 2022.
  de Oliveira Pinto, H. P., Michael, Pokorny, Pokrass, M.,
  Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E.,          Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides,
  Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C.,              J., Glaese, A., McAleese, N., and Irving, G. Red teaming
  Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez,                language models with language models, 2022.
  H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S.,
                                                                      Russell, S. Human Compatible: Artificial Intelligence
  Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Sel-
                                                                        and the Problem of Control. Penguin Publishing Group,
  sam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker,
                                                                        2019. ISBN 9780525558620. URL https://books.
  S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin,
                                                                        google.co.uk/books?id=M1eFDwAAQBAJ.
  J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Stau-
  dacher, N., Such, F. P., Summers, N., Sutskever, I., Tang,          Russell, S. Provably beneficial artificial intelligence. In IUI
  J., Tezak, N., Thompson, M. B., Tillet, P., Tootoonchian,            ’22: Proceedings of the 27th International Conference on
  A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J.          Intelligent User Interfaces, 2022.
  F. C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright,
  C., Wang, J. J., Wang, A., Wang, B., Ward, J., Wei, J.,             Russell, S. Written testimony of Stuart Russell before the
  Weinmann, C., Welihinda, A., Welinder, P., Weng, J.,                  U.S. Senate Committee on the Judiciary, Subcommitee
  Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich,             on Privacy, Technology, and the Law, 2024. URL
  S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M.,                    https://www.judiciary.senate.gov/imo/
  Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba,                 media/doc/2023-07-26_-_testimony_-
  W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng,               _russell.pdf.
  T., Zhuang, J., Zhuk, W., and Zoph, B. Gpt-4 technical
                                                                      Saad, F., Patton, B., Hoffman, M. D., A. Saurous, R., and
  report, 2024.
                                                                        Mansinghka, V. Sequential Monte Carlo learning for time
Orseau, L. and Armstrong, S. Safely interruptible agents.               series structure discovery. In Krause, A., Brunskill, E.,
  In Conference on Uncertainty in Artificial Intelligence,              Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.),
  2016. URL https://api.semanticscholar.                                Proceedings of the 40th International Conference on Ma-
  org/CorpusID:2912679.                                                 chine Learning, volume 202 of Proceedings of Machine
                                                                        Learning Research, pp. 29473–29489. PMLR, 23–29 Jul
Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright,                 2023. URL https://proceedings.mlr.press/
  C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K.,                v202/saad23a.html.
  Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L.,
  Simens, M., Askell, A., Welinder, P., Christiano, P., Leike,        Sastry, G., Heim, L., Belfield, H., Anderljung, M.,
 J., and Lowe, R. Training language models to follow                    Brundage, M., Hazell, J., O’Keefe, C., Hadfield, G. K.,
  instructions with human feedback, 2022.                               Ngo, R., Pilz, K., Gor, G., Bluemke, E., Shoker, S., Egan,
                                                                        J., Trager, R. F., Avin, S., Weller, A., Bengio, Y., and
Pan, A., Bhatia, K., and Steinhardt, J. The Effects of Reward           Coyle, D. Computing power and the governance of artifi-
  Misspecification: Mapping and Mitigating Misaligned                   cial intelligence, 2024.
  Models. In International Conference on Learning Repre-
  sentations, October 2021.                                           Schlaginhaufen, A. and Kamgarpour, M. Identifiability
                                                                        and generalizability in constrained inverse reinforcement
Pang, R. Y., Padmakumar, V., Sellam, T., Parikh, A. P.,                 learning, 2023.
  and He, H. Reward Gaming in Conditional Text Gen-
  eration, February 2023. URL http://arxiv.org/                       Schuett, J., Dreksler, N., Anderljung, M., McCaffary, D.,
  abs/2211.08714. arXiv:2211.08714 [cs].                                Heim, L., Bluemke, E., and Garfinkel, B. Towards best
                                                                        practices in agi safety and governance: A survey of expert
Pearl, J. Causality. Cambridge University Press, Cambridge,             opinion, 2023.

                                                                 26
                                                  Towards Guaranteed Safe AI

Seligman, E., Schubert, T., and Kumar, M. A. K. Formal                 Soares, N., Fallenstein, B., Armstrong, S., and Yud-
  verification: an essential toolkit for modern VLSI design.             kowsky, E. Corrigibility. In Walsh, T. (ed.), Artifi-
  Elsevier, 2023.                                                        cial Intelligence and Ethics, Papers from the 2015 AAAI
                                                                         Workshop, Austin, Texas, USA, January 25, 2015, vol-
Seshia, S. A. Combining induction, deduction, and structure              ume WS-15-02 of AAAI Technical Report. AAAI Press,
  for verification and synthesis. Proceedings of the IEEE,               2015. URL http://aaai.org/ocs/index.php/
  103(11):2036–2051, 2015.                                               WS/AAAIW15/paper/view/10124.
Seshia, S. A., Sadigh, D., and Sastry, S. S. Towards Verified          Stray, J. Designing recommender systems to depolarize,
  Artificial Intelligence. ArXiv e-prints, July 2016.                    2021.
Seshia, S. A., Desai, A., Dreossi, T., Fremont, D., Ghosh,             Stuhlmüller, A., Hawkins, R. X., Siddharth, N., and Good-
  S., Kim, E., Shivakumar, S., Vazquez-Chanlatte, M., and                man, N. D. Coarse-to-fine sequential Monte Carlo for
  Yue, X. Formal specification for deep neural networks.                 probabilistic programs. arXiv preprint arXiv:1509.02962,
  In Proceedings of the International Symposium on Auto-                 2015.
  mated Technology for Verification and Analysis (ATVA),
  pp. 20–34, October 2018.                                             Subramani, R., Williams, M., Heitmann, M., Holm, H.,
                                                                         Griffin, C., and Skalse, J. On the expressivity of objective-
Seshia, S. A., Sadigh, D., and Sastry, S. S. Toward verified             specification formalisms in reinforcement learning, 2024.
  artificial intelligence. Communications of the ACM, 65
  (7):46–55, 2022.                                                     Szegedy, C. A promising path towards autoformaliza-
                                                                         tion and general artificial intelligence. In Intelligent
Settle, J. E. Frenemies: How Social Media Polarizes Amer-                Computer Mathematics: 13th International Conference,
  ica. Cambridge University Press, 2018.                                 CICM 2020, Bertinoro, Italy, July 26–31, 2020, Proceed-
                                                                         ings 13, pp. 3–20. Springer, 2020.
Shah, R., Varma, V., Kumar, R., Phuong, M., Krakovna,
  V., Uesato, J., and Kenton, Z. Goal misgeneralization:               Tabuada, P. Verification and control of hybrid systems: a
  Why correct specifications aren’t enough for correct goals,            symbolic approach. Springer Science & Business Media,
  2022.                                                                  2009.
Skalse, J. and Abate, A. On the limitations of Markovian               Tang, H., Key, D., and Ellis, K. Worldcoder, a model-
  rewards to express multi-objective, risk-sensitive, and                based llm agent: Building world models by writing code
  modal tasks. In Evans, R. J. and Shpitser, I. (eds.), Pro-             and interacting with the environment. arXiv preprint
  ceedings of the Thirty-Ninth Conference on Uncertainty                 arXiv:2402.12275, 2024.
  in Artificial Intelligence, volume 216 of Proceedings of
  Machine Learning Research, pp. 1974–1984. PMLR, 31                   Tegmark, M. Life 3.0: Being human in the age of artificial
  Jul–04 Aug 2023a. URL https://proceedings.                             intelligence. Vintage, 2018.
  mlr.press/v216/skalse23a.html.                                       Tegmark, M. and Omohundro, S. Provably safe systems:
Skalse, J. and Abate, A. Misspecification in inverse rein-               the only path to controllable agi, 2023.
  forcement learning, 2023b.                                           Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T.
                                                                         Solving olympiad geometry without human demonstra-
Skalse, J. and Abate, A. Quantifying the sensitivity of
                                                                         tions. Nature, 625(7995):476–482, Jan 2024. ISSN 1476-
  inverse reinforcement learning to misspecification, 2024.
                                                                         4687. doi: 10.1038/s41586-023-06747-5. URL https:
Skalse, J., Farnik, L., Motwani, S. R., Jenner, E., Gleave, A.,          //doi.org/10.1038/s41586-023-06747-5.
  and Abate, A. Starc: A general framework for quantifying
                                                                       Turchin, A. Catching treacherous turn: A model of the
  differences between reward functions, 2024.
                                                                         multilevel ai boxing, 05 2021.
Skalse, J. M. V., Howe, N. H. R., Krasheninnikov, D., and
                                                                       Turing, A. Intelligent machinery, a heretical theory. 1951.
  Krueger, D. Defining and Characterizing Reward Gaming.
  In Advances in Neural Information Processing Systems,                van Merwijk, C., Carey, R., and Everitt, T. A complete
  May 2022.                                                              criterion for value of information in soluble influence
                                                                         diagrams, 2022.
Skalse, J. M. V., Farrugia-Roberts, M., Russell, S., Abate,
  A., and Gleave, A. Invariance in policy optimisation                 Vazquez-Chanlatte, M. and Seshia, S. A. Maximum causal
  and partial identifiability in reward learning. In Inter-              entropy specification inference from demonstrations. In
  national Conference on Machine Learning, pp. 32033–                    32nd International Conference on Computer Aided Verifi-
  32058. PMLR, 2023.                                                     cation (CAV), July 2020.

                                                                  27
                                                Towards Guaranteed Safe AI

Vazquez-Chanlatte, M., Jha, S., Tiwari, A., Ho, M. K., and             volume 14245 of Lecture Notes in Computer Science, pp.
  Seshia, S. A. Learning task specifications from demon-               191–212. Springer, 2023.
  strations. In Advances in Neural Information Processing
  Systems 31: Annual Conference on Neural Information                Yudkowsky, E. Creating friendly ai 1.0: The analysis and
  Processing Systems (NeurIPS), pp. 5372–5382, Decem-                  design of benevolent goal architectures. The Singularity
  ber 2018.                                                            Institute, 2001.

Viano, L., Huang, Y.-T., Kamalaruban, P., Weller, A.,                Zhang, D. Adding native support for havoc in viper. Pro-
  and Cevher, V. Robust inverse reinforcement learning                 ceedings of IEEE International Conference on Robotics
  under transition dynamics mismatch. In Beygelzimer,                  and Automation, 2022.
  A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.),             Zhang, Y., Tino, P., Leonardis, A., and Tang, K. A survey
  Advances in Neural Information Processing Systems,                   on neural network interpretability. IEEE Transactions
  2021. URL https://openreview.net/forum?                              on Emerging Topics in Computational Intelligence, 5(5):
  id=t8HduwpoQQv.                                                      726–742, October 2021. ISSN 2471-285X. doi: 10.1109/
Vinge, V. The coming technological singularity: How to                 tetci.2021.3100641. URL http://dx.doi.org/10.
  survive in the post-human era. Whole Earth Review, 1993.             1109/TETCI.2021.3100641.

Wang, X., Zhang, Y., and Zhu, R. A brief review on algo-             Zhao, S., Brekelmans, R., Makhzani, A., and Grosse, R.
 rithmic fairness. Management System Engineering, 1(1):                Probabilistic inference in language models via twisted
 7, Nov 2022. ISSN 2731-5843. doi: 10.1007/s44176-                     sequential monte carlo. arXiv preprint arXiv:2404.17546,
 022-00006-z. URL https://doi.org/10.1007/                             2024.
 s44176-022-00006-z.                                                 Zhuang, S. and Hadfield-Menell, D. Consequences of mis-
Watanabe, S. Algebraic Geometry and Statistical Learning               aligned AI. In Proceedings of the 34th International
 Theory. Cambridge Monographs on Applied and Compu-                    Conference on Neural Information Processing Systems,
 tational Mathematics. Cambridge University Press, 2009.               NIPS’20, pp. 15763–15773, Red Hook, NY, USA, De-
                                                                       cember 2020. Curran Associates Inc. ISBN 978-1-71382-
Watanabe, S. Mathematical Theory of Bayesian Statistics.               954-6.
 Chapman and Hall/CRC, 2018.
                                                                     Ziegler, D. M., Nix, S., Chan, L., Bauman, T., Schmidt-
Wiener, N. The Human Use of Human Beings. Eyre &                       Nielsen, P., Lin, T., Scherlis, A., Nabeshima, N.,
 Spottiswoode, 1950.                                                   Weinstein-Raun, B., de Haas, D., Shlegeris, B., and
                                                                       Thomas, N. Adversarial training for high-stakes relia-
Wing, J. M. Trustworthy AI. Communications of the ACM,                 bility, 2022.
 64(10):64–71, September 2021. ISSN 1557-7317. doi:
 10.1145/3448248. URL http://dx.doi.org/10.
 1145/3448248.

Wong, L., Grand, G., Lew, A. K., Goodman, N. D., Mans-
 inghka, V. K., Andreas, J., and Tenenbaum, J. B. From
 word models to world models: Translating from natural
 language to the probabilistic language of thought, 2023a.

Wong, L., Mao, J., Sharma, P., Siegel, Z. S., Feng, J., Ko-
 rneev, N., Tenenbaum, J. B., and Andreas, J. Learning
 adaptive planning representations with natural language
 guidance. arXiv preprint arXiv:2312.08566, 2023b.

Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jam-
 nik, M., and Szegedy, C. Autoformalization with large
 language models. Advances in Neural Information Pro-
 cessing Systems, 35:32353–32368, 2022.

Yalcinkaya, B., Torfah, H., Fremont, D. J., and Seshia, S. A.
  Compositional simulation-based analysis of AI-based au-
  tonomous systems for markovian specifications. In Run-
  time Verification - 23rd International Conference (RV),

                                                                28
                                                  Towards Guaranteed Safe AI

A. A Definition of Harm                                                     a single variable.)
Many proposed safety specifications require recognizing
                                                                          • Default utility: The causal model also includes a de-
when harm occurs. To better understand how to represent
                                                                            fault utility value, which is context-dependent. This
harm in a safety specification, it’s helpful to consider how
                                                                            default utility represents the expected or ”normal” util-
this concept can be formalized using tools such as causal
                                                                            ity in the given scenario, and it is used as a reference
models.
                                                                            point to determine whether an event causes harm.
Before we can define harm, it’s worth first reviewing the
basics of causal models: we can view a causal model as a
                                                                       With this background, we are in a position to talk about
directed acyclic graph (DAG), where nodes represent vari-
                                                                       what it means for an event to cause harm in an extended
ables and edges represent causal relationships between those
                                                                       causal model:
variables. In the DAG, we take the variables at the top to
be exogenous (their values are determined by factors out-              If an event caused a specific outcome whose utility is worse
side the scope of the mode), while all other variables are             than a default utility (which is given as part of the model)
endogenous and have associated equations that determine                and there’s an alternative event which would have led to a
their values as a function of the values of their parents (re-         utility with a better outcome, then harm was caused. A little
placing the conditional probability tables that characterize a         more formally, an event X = x causes harm in a causal
Bayesian network by equations).                                        setting if there exist values x′ and outcomes o, o′ such that
                                                                       (i) the utility of the actual outcome o is less than the default
The equations in the causal model represent how things work
                                                                       utility, and (ii) the event X = x rather than X = x′ causes
in the absence of interventions. They describe the causal
                                                                       outcome o rather than o′ , where the utility of o is less than
relationships between variables and determine the outcomes
                                                                       the utility of o′ .
based on the values of the parent variables. However, the
causal model also allows for interventions. If an intervention         We find this definition of harm an appealing starting point,
is made, such as setting variable X to a specific value (e.g.,         which could then be defined and bound in a safety speci-
X = 3), a new causal model is created. In this new model,              fication and verified against a world model. However, we
everything upstream of the intervention remains the same,              do think this is just a starting point; implementing this in
while everything downstream is changed according to the                a complex world model to meaningfully cover the utilities,
equations and the intervention.                                        the downstream implications of an event, etc. are, to put it
                                                                       mildly, a challenge.
While the actual definition of causation is somewhat more
complicated, for our purposes, it suffices to say that A rather
than A′ is a cause of B rather than B ′ if, had A′ happened            B. A Formal Definition of GS AI
instead of A, B ′ would have happened rather than B, where
                                                                       In this Appendix, we provide a more formal version of
A and A′ are different settings of the same variables, as are
                                                                       Definition 3.1.
B and B ′ . So we can say, for example, that X = 2 rather
than X = 3 is a cause of Y = 1 rather than Y = 0 if, had               Definition B.1. A Guaranteed Safe AI system is one that
X been set to 3 (instead of taking its actual value of 2), then        is equipped with a quantitative safety guarantee, that is
Y would have been 1 rather than its actual value of 0.                 produced by a world-model, a safety specification, and a
                                                                       verifier. Formally, this can be described as follows:
In order to capture harm, we need to extend the standard
causal model with two additional features:
                                                                          • Let A be a set of actions, S be a set of world states, and
                                                                            O be a set of observation. A policy π is a function π :
   • Utility on outcomes: The causal model includes a spe-                  (O × A)⋆ × O → ∆(A), which returns a distribution
     cial endogenous variable called ”outcome,” which rep-                  of actions for each sequence of past observations and
     resents the possible outcomes of the scenario being                    actions. Let Π be the set of all policies.
     modeled. Each value of the outcome variable is associ-
     ated with a specific utility value, normalized between               • A world model m is a function m : S×A → P(∆(O×
     0 and 1. For example, if outcome X has a utility of                    S)), which returns a set of probability distributions of
     1, it means that X is the most desirable outcome in                    world states and observations for each past world state
     the context of the model. (The assumption that there                   and action. Let M be the set of all world models.15
     is a single outcome, as opposed to a set of outcomes,               15
                                                                            Note that this includes the case where the world model always
     and that its value is normalized to being in [0,1], can           outputs a precise probability distribution, i.e. functions m : S ×
     both be made without loss of generality. We can, for              A → ∆(O × S). However, we also include the case where the
     example, always “package up” a set of outcomes into               world model outputs a credal set, for example.

                                                                  29
                                                     Towards Guaranteed Safe AI

   • A safety specification ψ is a function ϕ : Π × M →
     [0, 1], which specifies a value between 0 and 1 for each
     policy and world model.
   • A verifier Vψ for a specification ψ is an algorithm
     Vψ : Π × M → P([0, 1]) that computes or estimates
     the value of ψ(π, m).16

A GS AI system is thus a tuple ⟨π, m, ψ, Vψ ⟩, where π is a
policy such that Vψ (π, m) lies in some permissible set.




   16
      In general, we permit Vψ to be an anytime algorithm which
never terminates, but instead is productive of a sequence of in-
creasingly accurate estimates. In these cases Vψ also takes as input
a time parameter t ∈ N, and should satisfy that Vψ (π, m, t) ⊆
Vψ (π, m, t′ ) whenever t ≤ t′ . We can also allow Vψ to be proba-
bilistic, in which case it also takes a random vector as input.

                                                                       30
