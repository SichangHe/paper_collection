Software and Systems Modeling (2025) 24:1293–1313
https://doi.org/10.1007/s10270-024-01232-7

    SPECIAL SECTION PAPER



Extract, model, refine: improved modelling of program verification
tools through data enrichment
Sophie Lathouwers1 · Yujie Liu1 · Vadim Zaytsev1

Received: 6 May 2023 / Revised: 17 June 2024 / Accepted: 19 September 2024 / Published online: 8 January 2025
© The Author(s) 2024


Abstract
In software engineering, models are used for many different things. In this paper, we focus on program verification, where
we use models to reason about the correctness of systems. There are many different types of program verification techniques
which provide different correctness guarantees. We investigate the domain of program verification tools and present a concise
megamodel to distinguish these tools. We also present a data set of 400+ program verification tools. This data set includes the
category of verification tool according to our megamodel, practical information such as input/output format, repository links
and more. The practical information, such as last commit date, is kept up to date through the use of APIs. Moreover, part of
the data extraction has been automated to make it easier to expand the data set. The categorisation enables software engineers
to find suitable tools, investigate alternatives and compare tools. We also identify trends for each level in our megamodel.
Our data set, publicly available at https://doi.org/10.4121/20347950, can be used by software engineers to enter the world of
program verification and find a verification tool based on their requirements. This paper is an extended version of https://doi.
org/10.1145/3550355.3552426.

Keywords Program verification · Megamodelling · Data enrichment · Data extraction


1 Introduction                                                              notation and thus have considerable formal background to
                                                                            do it in a correct and useful way [22].
Program verification (PV) is a field that has always enjoyed                    To simplify, for the rest of the paper we use the established
very high expectations, and suffered from them as well. Its                 team “program verification” to mean verification (confor-
objectives are mostly to provide ways to prove that a system                mance evaluation) of programs (executable models). Hence,
satisfies certain requirements. The underlying techniques are               it covers generative techniques, testing, model checking,
typically based on rigorous mathematical reasoning or an                    theorem proving, etc, of source code, automata, Petri nets,
exhaustive analysis of the state space, thereby giving soft-                transition systems, etc.
ware engineers stronger guarantees than testing. It is often                    Adopting verification tools has shown to present not only
accepted that to use program verification (or formal methods                technical challenges, but also organisational, social and man-
in general), one needs to specify their system in a formal                  agerial ones [28], similar to challenges faced by advanced
                                                                            model-driven engineering tools [49]. PV tools are particu-
                                                                            larly difficult, because even demonstrating potential benefits
Communicated by N. Bencomo, M. Wimmer, H. Sahraoui, and E.                  of their use is highly nontrivial and relies on users having very
Syriani.
                                                                            specific knowledge of the underlying techniques. For the tool
B Vadim Zaytsev                                                             developers, the tools themselves often serve as a means to an
     vadim@grammarware.net                                                  end, as an opportunity to demonstrate the extent of appli-
     Sophie Lathouwers                                                      cability of their techniques, to exemplify the problems that
     sophie.lathouwers@gmail.com                                            could possibly be tackled, and to enter an existing subdomain.
     Yujie Liu                                                              Some subdomains are accompanied by sets of mature bench-
     yujie.liu.public@gmail.com                                             marks which make comparing techniques by comparing tools
                                                                            a very attractive and attainable goal. Examples include pro-
1    Formal Methods and Tools, University of Twente, Enschede,              gramming language theory [8], software verification [16] and
     The Netherlands


                                                                                                                                  123
1294                                                                                                              S. Lathouwers et al.


quantitative verification [44]. Admittedly, many tools stay in     vide as input to use tool X?” or “what other tools exist for the
a prototype phase, and being actively developed only till a        same problem domain as tool X?”, or even “when was the
certain point: until the tool can handle the minimal set of        last time the code of tool X was updated?”. We will elaborate
benchmarks, or until the deadline for submitting the paper         on the megamodel and its PV0–PV6 levels in Sect. 3.
explaining the underlying techniques, or until graduating              With this megamodel, we show that there are many dif-
from a PhD project.                                                ferent types of PV tools, and those types can be grouped
    Besides techniques and tools, there are multiple sources       in categories that form a hierarchy. Thus, if a tool from
of information to consider. Papers themselves are an obvious       one category comes fundamentally short to solve the end-
source, well-archived on publishers’ websites, but requiring       user’s problems, it can be considered to seek alternatives in a
high qualifications to be considered readable and understand-      broader category. To concretise the megamodel, we complete
able. They are also hard-dated, meaning that an average            it with a data set into which we have collected information
good paper contains detailed comparison of the proposed tool       about 450+ PV tools, frameworks and languages, published
with its existing counterparts, but no comparison or relation      recently at two top conferences in the PV domain known for
to counterparts that were created after the publication. The       their tool paper hospitality: CAV and TACAS. The data set
papers often refer to product or project pages, which are prone    is available publicly on GitHub, with a reader-friendly inter-
not only to being outdated for reasons mentioned above, but        connected hypertextual frontend at https://slebok.github.io/
also to being removed due to the jobhopping nature of the          proverb.
academic world: when the principal investigator finishes the       We strongly believe that making the data set freely accessi-
project and moves to another institution, it is not guaran-        ble for exploration, makes it an attractive starting point for
teed that the project page will be preserved by their original     software engineers to traverse the domain of program veri-
employer. If available, such websites are also wildly varying      fication. Section 4 contains more information about the data
in the nature of their content: some literally repeat the con-     set, as well as our methods of gathering the data, categorising
tents of the papers, while others complement it with valuable      and enhancing it.
information, illustrations, and links.                                 In Sect. 5, we report some preliminary lessons we have
    Another extremely valuable source of information — pri-        learned ourselves by looking at the collected information,
marily about the tools and not always about the techniques —       level by level, and analysing some of its trends. The fact that
is the code repositories. It has become fairly commonplace         our megamodel splits the PV domain into distinct groups
in recent years to either release the tools for (limited) pub-     recognisable from prior research, is considered here as a form
lic use to enable empirical replicability, or expose the entire    of evaluation and evidence that the megamodel is viable and
development history in a form of versioned codebase (typ-          useful.
ically through git, occasionally hg or svn). There are at              This paper is an extended version of the conference publi-
least three benefits of repositories: (1) the artefacts become     cation by [58]. Besides going into more details for the lack of
much more tangible, and only require several natural steps         space constraints and in order to make this paper more self-
(like cloning the repository) to set themselves up on the user’s   contained (with respect to its own website and repository),
computer instead of extracting them from the paper text; (2)       the additional contributions here are:
the version history is a technically substantiated claim to the
amount of work and to its authorship; and (3) linking tools
to one another by shared contributors plays the same social
role as linking papers by shared coauthors.                         • Linking this line of research to the current research trends
    To summarise the problems:                                        on artefacts and artefact evaluations (Sect. 2).
                                                                    • Automating further expansion of the data set by using
 • existing techniques are hard to understand and assess              heuristics to identify tools in new publications (Sect. 4.1.2),
   their applicability without very deep specific knowledge;          since providing tool support in updating the data set is
 • tools are hard to classify conceptually and appropriately          instrumental for its continuous maintenance and growth.
   relate to techniques;                                            • Automating information extraction from conference pro-
 • information sources are dispersed, partly unavailable and          ceedings (Sect. 4.1.3), significantly lowering the barrier
   partly unreliable.                                                 to add new entries.
                                                                    • Refining and enriching the data set “horizontally” by
   With the vision to open up the arsenal of PV tools and             adding more information, more precise information or
techniques to a broader public of software modellers and,             more up to date information with the help of several APIs
even broader, software engineers, we have developed a meg-            (Sect. 4.2). For instance, the date of the last update does
amodel of program verification tools. The megamodel can               not have to be manually checked but is inferred from the
help answering questions like “what am I expected to pro-             git history of the tool repository.


123
Extract, model, refine: improved modelling of program verification tools...                                                                1295


 • Providing a more conceptual/clean approach to model                        tools quality and personnel changes, while the top three
   each tool based on an ontology (Sect. 4.2.1) instead of an                 improvements were education, tool integration, and creating
   ad hoc template — cf. [58, section 3.1.3].                                 and disseminating evidence of the benefits of formal analysis.
 • Using these methods for extending the data set into sev-                   Tomassetti and Zaytsev [83] combined personal experiences
   eral dimensions (Sect. 4.2) and reporting statistics on that               of two industrial experts in the field of domain-specific lan-
   (Sect. 4.3).                                                               guages and summarised the real advantages of using DSLs
 • Planning an extensive research roadmap for the future of                   next to their adoption problems of different nature.
   this project (Sect. 6).                                                        Klösch and Eixelsberger [52] provided a fairly extensive
                                                                              yet concise list of explicit and factual challenges that the soft-
                                                                              ware industry faced when solving the Y2K problem as well
2 Related work                                                                as conversion from local currencies to Euro. Their structured
                                                                              list was also broad in nature and covered many aspects from
When it comes to related work, we refer the attention of                      formal compliance validation to organisational workarounds.
the readers to in-depth overviews of problems in adoption                     More than two decades later, Nurwidyantoro et al. [66, 67] as
of program verification, formal methods, model-driven engi-                   well as Whittle, Ferrario, Simm, and Hussain [86] argued that
neering and domain-specific languages, which we summarise                     human values such as responsibility, transparency, creativ-
below.                                                                        ity and equality represent a substantial fraction of software
   In 2005, Bodeveix, Filali, Lawall, and Muller [19] pro-                    engineering challenges and difficulties, yet are heavily under-
vided a side-by-side comparison of two solutions to the                       represented in methodological research.
same case study problem (kernel-level process scheduling):                        If we were to summarise all these extensive studies on rel-
one done with software modelling (in particular, a domain-                    atively well-known problems, we would have to admit that
specific language), and the other with formal methods, with                   most of them are related to tools, their prototype-level qual-
a conclusion that a formal specification provides at least as                 ity, notorious unavailability, lack of support and sufficiently
good of a model as a DSL one. The modern view on this                         reliable documentation, etc.
matter is to combine the power of two sides of this debate,                       Over the years, many ontologies, taxonomies and surveys
and link program verification to formal DSL models [5]. This                  have been published about program verification. However,
can be done either way: by augmenting the existing system                     these works tend to target either a specific subset of pro-
with an internal DSL and using information encoded there for                  gram verification, e.g. runtime verification [36], high-level
verification purposes [12] or by generating formally correct                  synthesis [61] or a specific domain, e.g. vehicular domain
DSL code [68].                                                                [78], smart contracts [45], railway system design [37], pro-
   Broadfoot and Broadfoot [22] argued that in the domain of                  grammable logic controllers [40]. Unlike these works, we
embedded software, there are many systems which are both                      do not focus on a subset of PV, but aim to deliver both a
business-critical and untestable with conventional means.                     megamodel to explain tools, as well as an easily accessible
Their concluding advice was to rely on provably correct                       (and extensible!) repository with a large data set of classified
designs which are transformed into code by using only tools                   tools.
that are provably correct. Woodcock, Larsen, Bicarregui, and                      The work that is closest to ours is a report by Punnoose,
Fitzgerald [91] provide what seems to be the most extensive                   Armstrong, Wong, and Jackson [72] that presents several
survey on formal methods, their prevalence in academic lit-                   verification techniques in detail. It covers a broad variety of
erature and in industrial experience. They also listed a few                  techniques including model checking, verification condition
of the most popular tools by name, without introducing any                    generation and correct-by-construction design. However,
exhaustive coverage criteria like we will do in Sect. 4.                      they only mention a few tools per technique, whereas we
   Bucchiarone et al. [23] stressed the important of informal                 consider all PV tools that we could identify in publications.
modelling as a way to attract new users to MDE. In this                       Nonetheless, this report can also be a nice starting point for
case, informal modelling does not mean the lack of formal                     engineers.
methods: it designates the ease of use for novice modellers                       When it comes to repositories, we also do not claim out-
and the ability of the metamodel to express incomplete and                    right novelty. Over the years, several projects have tried to
uncertain information. Under the hood such products can still                 achieve more or less similar goals. For instance, the Verified
rely on highly complex science in the same way an internet                    Software Repository [18] was intended to become a col-
search query relies on MapReduce and data synchronisation                     lection of tools, verified programs, benchmarks and results.
with a mobile device relies on lenses.                                        Unfortunately, it was last updated in 2009. Schlick et al. [77]
   Davis et al. [28] conducted a large study of 31 experts                    have also proposed to set up a repository to make formal
from 9 companies, and identified that the top three barriers                  methods more accessible to users in the industry. A large
for adopting formal methods in the industry are education,                    part of their work focuses on the obstacles that limit the adop-


                                                                                                                                    123
1296                                                                                                                      S. Lathouwers et al.


tion of formal methods in industry. Some of these obstacles
include the maturity of tools, difficulties in finding the right
methods and lack of ways to easily compare different tools.
This is in line with our experience and the research mentioned
in Sect. 1. Like us, Schlick et al. [77] believe that the aware-
ness and comparability between formal methods should be
improved. To achieve this, Schlick et al. [77] use notable
success stories to identify key information that should be
included in a formal methods repository. They then present
a vision of a repository and why it would be beneficial. They
give a repository structure that includes (1) experiment data,
(2) applications, (3) problem descriptions, (4) formalisations,
(5) usage patterns, and (6) tools. However, to the best of our
knowledge, this repository has not yet been instantiated, and
remained a dream. One could consider our data set as a first
                                                                    Fig. 1 Each ellipse indicates the potential correctness guarantees that
instantiation of the “Tool" part of their proposed repository       can be acquired by using a tool of that level. PV0 tools give the least
structure. In the future it could be combined with other data       guarantees of correctness, whereas PV6 tools allow the user to work
to form a complete repository as proposed by Schlick et al.         towards maximum correctness guarantees. Note that these indicate the
[77], including data such as experiments and applications.          potential of each level; a tool may only support a little piece of a level
    An important aspect for tools in our data set is their avail-
ability and reusability. There have been several efforts to
evaluate the reusability of artefacts. Baldassarre, Ernst, Her-        Since the ultimate goal of PV is to prove correctness of
mann, Menzies, and Yedida [10] present the Department of            the artefact in some form and within some domain, we will
Reuse that records the reuse of research, including 8 differ-       use the classic division of roles in a correctness proof. It was
ent types of reuse such as tool reuse and data set reuse. Both      originally introduced by Goldwasser, Micali, and Rackoff
Winter et al. [89] and Hermann, Winter, and Siegmund [47]           [41], we use the more widespread modern terminology here
have gathered data to evaluate whether artefact evaluations         [88]:
were as effective as hoped. Where Winter et al. [89] focus on
the availability of artefacts, documentation practices, hosting
platform and citation count, Hermann, Winter, and Siegmund
[47] take a different approach and focus on the community’s                                           Claim

expectations for such artefacts. We consider all these contri-
butions to be complementary to our research as they could
provide information about the (re)usability of tools in our
data set. While we are interested in such data, our interest is                                     argument
                                                                                   Prover                             Verifier
in whether tools are usable in practice as opposed to its impli-
cations for the academic sphere in terms of the effectiveness
of artefact evaluations or its relation to citation counts which
is explored in the previously mentioned works.
    Other directions for future work and consequences of this       In short, there exists a claim of some sort (e.g. “x ∈ S” or “the
project, are considered in Sect. 6.                                 program has no memory leaks” or “all models are wrong”),
                                                                    which is provided to both the prover and the verifier. The
                                                                    prover is very clever and can perform sophisticated manip-
                                                                    ulations and computations. Its goal is to produce arguments
3 The megamodel of PV-levels                                        supporting the claim, but the prover can also be biased and
                                                                    prone to producing false positive arguments. The verifier
In this section, we introduce the seven levels of our meg-          has some way of checking the arguments and, depending
amodel: PV0, PV1, PV2, PV3, PV4, PV5 and PV6 (see                   on its verdict, declaring the claim accepted or rejected. We
Fig. 1).                                                            will be illustrating each of the PV tool levels with explana-
   Intuitively, higher levels give the user more correctness        tions, examples and also differences on this simple scheme.
guarantees, though typically at the cost of more user effort,       In the subsequent diagrams we will also use green colour to
and lower level tools are usually less strict and thus do not       highlight the main contributing elements that make someone
require as much PV expertise to be effectively applicable.          decide to use a tool of this particular level.


123
Extract, model, refine: improved modelling of program verification tools...                                                              1297



                                 Artefact                                                                 Artefact




                                   PV0                                                                      PV2


                                                                                         Synthesiser




[PV0] Software engineers always work with abstractions                           [PV2] The opposite situation is also commonplace: if a
and models of reality. Once a software entity satisfies the                   user makes a model of their wishes, often taking a form of
three properties of the modelling theory [81], it can be seen                 an almost-consistent artefact with holes to be filled, then one
as a model. These three are the mapping property (elements                    can build a tool to fill in those gaps and infer them from
of the model represent some elements of the real entity being                 the context. Sources of information can be different, rang-
modelled), the reduction property (only the most important                    ing from domain common sense (for example, we obviously
aspects of the real entity are being modelled and others                      want our parallel programs to not get stuck waiting for one
are being abstracted from), and the pragmatic property (the                   another’s resources) to constraints and instructions explicitly
model has a purpose). Formal models are a subset of such                      specified by the user. In a sense, if we want to consider the
models, which are clean and well-formed, and often built                      Eclipse Modelling Framework as a proof system, it would
with the use of some existing mathematical theories. For                      fall into this category because it can produce the textual code
example, formal models often cover domain-specific vari-                      of classes that conform to the inheritance structure and the
ations of automata. In PV0, such a formal model may exist                     interfaces specified in the class model. In PV, such programs
but it is often implicit and is used neither to obtain nor to                 are often said to solve problems of synthesis and repair, and
verify any correctness guarantees.                                            use generative techniques to create test data, repair known
                                                                              categories of defects, implement queries, generate neural
                                                                              networks fitting for a particular grid, or just to configure
                                 Artefact                                     a universal algorithm with automatically obtained balanced
                                                                              values. PV2 tools help users to create software artefacts —
                                                                              either by generating them from scratch or by providing signif-
                                   PV1                                        icant assistance in the incremental process of creating them
                                                                              semi-automatically. If the output of a PV2 tool is expected
                                                    Solver                    to be processed by another automated component, then the
                                                                              tool belongs on a higher PV-level.

                                                                                                          Artefact
[PV1] Once a formal model can be operated on by a soft-                                                      &
ware system, it can also be automatically checked for internal                                           Properties

consistency and well-formedness, by a model solver. For
instance, if the underlying theory states that a model of a                                                 PV3
process is some specific automaton with one starting state
                                                                                        Specification   specification
and one or more final states, and all transitions labelled with                            Provider
                                                                                                                         Verifier

unique names, then a solver can check that all these properties
indeed hold. The more complex the model, the more difficult
it could be to make such a solver for it: for example, unique-                [PV3] Combining the two components into a] symmetric
ness is relatively easy to check on strings (which we assume                  setup (cf. Fig. 1), in the simplest case we get a situation when
for transition labels in our previous example), but it is notice-             a user explicitly states what properties of a formal model they
ably harder to define and enforce even on database records,                   wish to have (beyond well-formedness), and there is an auto-
where single columns (such as “first name”) often contain                     mated property checker, conceptually decomposable into
non-unique values, and combinations are often unreliable                      two parts: a prover that turns each property into a convincing
due to incompleteness and subtle tolerable inconsistencies                    argument and a verifier which validates the convincing power
(such as a phone number mismatch). From the correctness                       of such arguments. A typical example of a property checker
perspective, a PV1 tool plays a role of a verifier, and a prover              allows the developers to add assertions to their code, spec-
does not exist since the verifier does not need any arguments                 ifying preconditions, postconditions and invariants around
on top of the ability to observe the given model.                             a code fragment, thus allowing additional formal ways to


                                                                                                                                    123
1298                                                                                                             S. Lathouwers et al.


validate its correctness. These assertions do not have to be      specifications, we get to specification compilers. Such com-
deployed to the end-user, but serve as a powerful tool for the    pilers usually have a language used to write specifications
developer to verify the product beforehand. Some checkers         in, sometimes based on a domain-specific notation, and sup-
have a very extensive formal language to write properties in,     port this entire language by compiling its instances in some
usually a variant of some special kind of logic, e.g. temporal    automated way to verify their correctness and compatibility.
logic [57, 71].                                                   With those, you can build your own specifications of memory
                                                                  management strategies, your own communication protocols,
                             Artefact                             and so forth. To continue with examples from the previous
                          Specification
                                                                  paragraph: when a PV4 tool could check for deadlock free-
                                                                  dom, a PV5 tool would require a formal specification of the
                              PV4                                 concurrency model, accompanied with a definition of what
                                                                  constitutes a deadlock state. Obviously, some PV4 tools are
            Property       properties                             built on top of PV5 frameworks by essentially supplying a
                                           Verifier
           Generator
                                                                  useful singular model.

[PV4] On the previous level, the burden to create verifiable                                  Artefact
                                                                                           Specification
properties, was on the end-user of a tool: assertions had to be                              Properties
explicitly written, and invariants had to be provided. How-
ever, in some cases it is possible to automate the creation of
                                                                                                PV6
desired properties as well as their verification — since such
techniques require an extensive specification of the desired                    Proof          proof
                                                                                                             Verifier
                                                                              Assistant
behaviour, and often focus on only one paradigm, we call
them monoverifiers. They are very useful tools in debug-
ging, because if used correctly, they can significantly lower
                                                                     [PV6] If your program verification tool can not only han-
the chances of having a particular category of defects, some-
                                                                  dle different specifications, but also infer correctness of the
times up to eliminating the very possibility of such a defect
                                                                  proof of the needed property, then it belongs among the proof
ever occurring. For instance, think of a parallel system being
                                                                  assistants. This category is the most powerful one that we
checked for deadlocks or a garbage collector checked for the
                                                                  have encountered, which means both that it is the hardest and
lack of memory leaks. Essentially, monoverifiers verify that
                                                                  most demanding to use, as well as capable of producing the
the supplied formal model corresponds to the expectations
                                                                  strongest guarantees. However, as one can see from the dia-
of their own built-in specification.
                                                                  gram we provided, it bears some similarities with the PV1
   Some monoverifiers offer a choice of checking one or
                                                                  level, since there is very limited automation and tool support
more of a larger set of correctness specifications, in which
                                                                  in composing the arguments for correctness. The proof needs
case we still classify them to belong to PV4, even though the
                                                                  to be written by the end-user, and the tool can only offer some
mono- prefix no longer fits — as long as the end-user has no
                                                                  assistance in verifying that the proof is indeed correct. Some
direct control over the specifications themselves. Also most
                                                                  of PV6 tools can feel to their users as if they also help them
monoverifiers embrace the fact that their generated properties
                                                                  to compose the steps of the proof, but under closer inspec-
cannot always cover the end-user’s needs, and allow for direct
                                                                  tion this help comes from the tool knowing which proof step
manual specification of additional properties — which allows
                                                                  would succeed in reaching a user-stated goal, and not from
us to claim that PV4 functionalities are a strict superset of
                                                                  the tool relying on some generative algorithms. Within the
PV3 functionalities.
                                                                  claim/prover/verifier paradigm, proof assistants offer power-
                             Artefact                             ful techniques on behalf of the verifier and not the other two
                          Specification
                                                                  components.


                              PV5
                                                                  4 Data set of verification tools
          Specification    properties
                                           Verifier
             Compiler      properties
                                                                  To help users find a suitable PV tool, we have prepared a
                                                                  data set of tools categorised according to the megamodel
   [PV5] When the tool users have an opportunity or obli-         we have just explained in Sect. 3. This makes it easier to
gation not only to specify which properties of the system to      discover which tools are available, to find tools using similar
check for or how to infer them, but also to build their own       techniques, as well as to find tools that target similar domains


123
Extract, model, refine: improved modelling of program verification tools...                                                               1299




Fig. 2 An overview of the different steps that have been undertaken to set up the data set of program verification tools


and problems. The data set, called ProVerB, is available1 at                  4.1.2 Identify tools in papers
https://slebok.github.io/proverb/. Each tool has its own file
which contains all of its data and metadata in Markdown                       Next, we needed to identify the tools that were presented in
format.                                                                       each paper. To help with this process, we have developed
   The remainder of this section explains how the initial data                a script that automatically identifies paper titles in the pro-
set has been created (Sect. 4.1), how we use open APIs to                     ceedings. Based on heuristics we try to identify the name of a
enrich our data set (Sect. 4.2) and presents some statistics                  tool. Specifically, one can often find titles of the form “Tool
about the data that was gathered (Sect. 4.3).                                 name: subtitle with explanation". Whenever a paper’s title
                                                                              matches this heuristic pattern, we automatically extract the
                                                                              tool’s name. For papers that do not adhere to this heuristic it
4.1 Methodology                                                               is still required to read the paper to identify tools.
                                                                                  For each paper we checked whether it contained a refer-
A methodological overview can be seen in Fig. 2. Below we                     ence to a tool. If so, then we would tag this as one of the
will describe each step of our research method in detail.                     following claims:


                                                                               • Presents: the paper introduces a new tool;
4.1.1 Choose data sources                                                      • Extends: an existing tool gains new functionality in the
                                                                                 paper;
To find PV tools to include in the data set, we looked into two                • Expands: the paper uses an existing tool as a basis for
popular conferences about verification of systems. Namely,                       building another tool;
the International Conference on Computer Aided Verifica-                       • Uses: the paper uses an existing tool for a case study or
tion (CAV) and the International Conference on Tools and                         to check the correctness of an approach.
Algorithms for the Construction and Analysis of Systems
(TACAS). In the CORE conference ranking, they are clas-
sified as having respective ranks of A*2 and A.3 We have                      We only included tools that provided some form of cor-
decided to use papers from these conferences since both                       rectness guarantees, to avoid including too many entries in
accept and welcome papers about tools. Therefore, we could                    ProVerB. This still left us with some entries that were later
expect a relatively high percentage of tool papers. Moreover,                 reclassified as not belonging to the PV domain (usually from
CAV and TACAS started with artefact evaluations in 2015                       misinterpretations of claims “we use library X”).
and 2018 respectively, therefore we expect that many of the
tools presented here will also be available. We have looked
                                                                              4.1.3 Collect data
at tool papers from TACAS 2016–2021 and all papers from
CAV 2017–2022. We are still in the process of adding the
                                                                              As a format for storing entries in the data set, we have chosen
TACAS 2022 papers. We chose to use these recent years as
                                                                              Markdown. This provided the lowest entrance barrier and
this makes it more probable that tools are still findable and
                                                                              maintenance cost, still combined with the opportunity to add
possibly maintained, yet still limited ourselves to at least
                                                                              structure to the data (in our case, in the form of ####-level
5 years of each conference in order to gather a substantial
                                                                              sections). By choosing this format, we also hope to make
amount of data.
                                                                              it easy for other people to contribute to the data set in the
    This step resulted in 519 papers: 406 from CAV and 113
                                                                              future, since GitHub, our hosting platform for the data, even
from TACAS.
                                                                              provides inline editing functionality for Markdown pages.
                                                                                  After some pilot classifications we set up a generic tem-
                                                                              plate for tool pages, which has proven to be quite resilient, and
1 The data set has also been archived at https://doi.org/10.4121/             after the first couple of sprints it stayed stable and unchanged
20347950                                                                      till the current moment. This template included a section
2 CAV: http://portal.core.edu.au/conf-ranks/331/
                                                                              for all the information that we were interested in for a tool,
3 TACAS: http://portal.core.edu.au/conf-ranks/1818/                           namely:


                                                                                                                                    123
1300                                                                                                                 S. Lathouwers et al.


 • Name of the program verification tool;                           domain knowledge [41, 88], we have arrived at the version
 • Domain or application field;                                     presented previously in Sect. 3.
 • The type of the tool as self-identified by authors;
 • Input that is required from the user;                            4.1.5 Classify tools
 • Input format;
 • Output that is produced;                                         Having designed the initial megamodel, we started the
 • Internal working of the tools, such as which tools it uses       process of classifying all the tools. Based on the tools’ semi-
   as a backend;                                                    structured description (cf. Sect. 4.1.3), we have assigned each
 • External relations to other tools, such as those that were       to a PV-level. While doing that, we have also consistently
   compared to this tool in the paper;                              provided a short description motivating this classification
 • Links to project pages, repositories and related papers;         by explaining what the tool does. In that way, a tool with
 • Dates when the tool and its documentation were last              a description “verifies properties of a user-specified mem-
   updated;                                                         ory model” was clearly placeable at PV5, and the one with
 • Reason why the tool was added to the data set.                   “checks user-specified properties and memory safety of C
                                                                    programs” was easily marked as deserving PV4. To pre-
Aside from the information mentioned above, we have also            vent misclassifications and improve inter-coder reliability,
started adding tags as textual annotations. Tags are used to        the authors actively double checked each other’s verdicts
indicate whether a tool targets a specific language, domain,        and had extensive discussions about arguable conclusions.
technique, etc. This should make it easier for users to find        In such discussions, the classifying coauthor would usually
suitable tools. For example, there is a tag for tools that target   apply the definition of the chosen PV-level to argue that the
C programs, a tag for neural networks, a tag for hardware           tool conforms to it, to be challenged by another coauthor with
verification, and so forth.                                         an alternative application of a different PV-level. In case of
   We start by creating a new page based on the same template       conflicts, the original tool describing paper was consulted for
for all tools. After the page has been created, we needed to        more detailed information sufficient to finalise the classifi-
collect additional information from the corresponding paper         cation.
as well as the code base and project website if these were             Aside from the PV0–PV6 levels, there are two other cat-
available. Some sections were left empty if the data was not        egories: “no PV” for false positives and “frameworks” for a
available (e.g. the last modification data for tools without a      possible level mixture. We used “no PV” to explicitly exclude
repository). If at least two tools referred to another tool, e.g.   entries that ended up, after close consideration, not perform-
because it was used as a back end or as a framework, then           ing any PV-related tasks. Such entries were mostly about
this tool was added as well and received its own entry.             specification formats, but also about IDE plugins, unrelated
   Some tools that we encountered were developed as pro-            programming languages, libraries not performing any PV
totypes, up to the point that these did not have a name at all,     tasks, etc. We felt that something like an alternative user
nor a link to an implementation. We decided to exclude such         front end or a linear programming library do not belong to
tools as these tools were likely not developed and maintained       PV0 either. “Frameworks” was used to classify collections of
for professional use. However, some tools included an arte-         tools: in many cases it was possible to determine the primary
fact, which was mostly still reliably available, so we included     objective of the collection and assign a framework to a proper
this link in the entry whenever it existed.                         level as well, but in other cases such an assignment has not
   The data set also includes pages about several specification     been deemed sensible. For example, “Alloy” is used to refer
formats. A page for a format was created if the format was          to the Alloy Analyser (which has its own entry on PV3),
not tool-specific, if it was used by more tools than one, or if     or to the input level of the Alloy Analyser, or to the entire
it was for some other reason conceptually separate from the         ecosystem of Alloy models and their verifiers, — and is not
tool.                                                               consistently PV-classifiable without explicit disambiguation.

4.1.4 Define megamodel                                              4.1.6 Identify trends

When the tool pages had been written, we contemplated the           Finally, after we classified all the tools, we could start to iden-
initial setup of the megamodel based on similarities between        tify trends in each level of the megamodel. These trends could
tools. The first version was already based on the input that the    be identified based on the short descriptions that were written
user has to provide, ranging from the no input at all (besides      in the previous step, and require only occasional lightweight
the already existing software artefact), to assertions, proper-     double checking with the full data entry or the text of the
ties, specifications, theories and proofs. Several refinement       underlying paper. We will discuss these trends in more detail
iterations later, based also on consulting the already available    in Sect. 5.


123
Extract, model, refine: improved modelling of program verification tools...                                                             1301


4.2 Data enrichment                                                           still maintained, but also to replace faceless DOI URIs with
                                                                              hyperlinked paper titles with Springer API.
The previous section has described how we set up the initial                      To see a concrete example, let us focus on JayHorn, a
data set. This section will describe how we have gathered                     tool we randomly selected to serve as another example in
additional data by combining the initial semi-structured data                 Table 2. Originally, its “Last commit date” section contained
set with data from third-party open APIs such as GitHub and                   the string “27 May 2021”, which was added manually by
Springer. For this process two main requirements were taken                   one of the authors of this paper who classified it first. After
into account namely:                                                          expanding in the (3) dimension, it contained more concretely
                                                                              two reference points: “27 May 2021 (default branch)” and
 • The structure of the data set should be preserved.                         “14 Dec 2021 (last activity)”, which was updated on 12
 • The process should be automated to minimise manual                         November 2023 when Philipp Rümmer, one of the contribu-
   effort required for maintenance                                            tors, merged pull request #161. For the same entry, the section
                                                                              about related papers has changed as depicted in Fig. 3.
   The data set can be enriched in three independent dimen-
sions:                                                                        4.2.1 Workflow

(1) Adding new entries for tools originally not present in the                To set up the automatic data enrichment, we first designed an
    data set (e.g. from newly published papers).                              ontology for ProVerB which is closely related to the template
(2) Adding new information about tools which are already                      described in Sect. 4.1.3.
    in the data set (e.g. the time of the last update in the code                The current version of the ProVerB ontology includes
    repository).                                                              11 classes (see Fig. 4). The meaning of each class as well
(3) Improving the information already present about the                       as an example can be found in Table 1, with a concrete
    tools (e.g. adding the titles of referenced papers).                      example in Table 2. The classes that we are currently using
                                                                              for data enrichment include Repository, Article,
   For the (1) dimension, we have only reached partial                        CodeContributor and Writer. Links to repositories
automation of the first step described in Sect. 4.1.3. We use                 and articles from the original data set are used to instantiate
a script to automatically extract some information from the                   the Repository and Article classes. These links are
conference proceedings using text pattern matching on the                     then used to gather additional information, such as authors
PDFs. Specifically, we automatically try to identify the tool’s               and code contributors, through open APIs. This additional
name (as mentioned before in Sect. 4.1.2), links to additional                information can be used to instantiate the classes such as
resources and keywords. The tool’s name and links are auto-                   CodeContributor and Writer.
matically added to the appropriate sections in the template.                     There are some classes in the ontology that are currently
The keywords are used as an initial set of tags.                              unused but have been added for future study. For example,
   For the (2) dimension, one of the enhancements we found                    the Format class has been added to explore possible input–
useful is to rely on GitHub API instead of on manual inves-                   output relationships between tools.
tigation, to determine the time when the repository (either                      With the ontology designed, we could now use this to
determined by the PDF parser or added manually) was last                      enrich our data set. The steps of this process have been illus-
updated. This is not only fast, but also a much more reliable                 trated in Fig. 5.
process, which can be repeated as often as we would like                         This process can be automated with GitHub workflows to
(which makes sense for tools that are actively being devel-                   run once per week and automatically generate a PR with the
oped or maintained).                                                          updates for the data set. The PR can then be reviewed before
   This brings us to the (3) dimension, which seems cosmetic,                 merging to ensure the data is of sufficient quality.
but improves the experience of using ProVerB nevertheless.
For instance, originally, the data set only contained bare links              4.2.2 Author-contributor relations
(URIs) for papers and repositories due to which the users
could not see, which paper they would be redirected to. As                    With the previously explained setup we can also collect
a result, users often needed to click and browse several links                data about authors of papers and contributors to reposito-
in order to find information that they needed, especially for                 ries. Specifically, we can explore “same-as” relationships to
tools described in several papers. To make this process more                  identify people who were both author and code contributor.
pleasant, we use API to automatically gather data about what                  This can provide valuable information about who to contact
the links point to. This way, we can automatically retrieve                   when someone has questions about a tool.
the latest commit date for repositories due to which users no                    This data is collected through the APIs, though it is not
longer need to click on the repository link to see whether it is              yet added to the data set or shown on the website. The topic


                                                                                                                                  123
1302                                                                                                                            S. Lathouwers et al.




Fig. 3 Improvements in the “List of related papers” section for JayHorn: the before and after versions above and under the line. Note how manually
added information (conference names with preferred abbreviations) is still preserved after refinement


                                                                           Table 2 The classes in the ProVerB ontology with an example of the
                                                                           corresponding data for one concrete tool
                                                                           Class                       Example

                                                                           Tool                        JayHorn
                                                                           Format                      Java bytecode (it supports Java class files,
                                                                                                         Jar archives, or Android apk)
                                                                           Repository                  https://github.com/jayhorn/jayhorn
                                                                           Article                     https://doi.org/10.1007/978-3-030-
                                                                                                         72013-1_29
                                                                                                       https://doi.org/10.1145/3340672.3341113
                                                                                                       https://doi.org/10.1007/978-3-030-
                                                                                                         17502-3_16
                                                                                                       https://doi.org/10.1007/978-3-319-
                                                                                                         41528-4_19
                                                                           Concept                     Java; Model checking
                                                                           PV                          PV4
Fig. 4 ProVerB ontology
                                                                           Conference                  TACAS’21; FTfJP’19; TACAS’19;
                                                                                                        CAV’16
Table 1 Overview of the classes in the ProVerB ontology with an expla-
nation of their meaning                                                    Writer                      Hossein Hojjat; Temesghen Kahsai;
                                                                                                        Philipp Rümmer; Huascar Sanchez;
Class                       Meaning                                                                     Martin Schäf; Ali Shamakhi
                                                                           CodeContributor             Martin Schaef
Tool                        A program verification tool in the
                                                                                                        Philipp Ruemmer
                             ProVerB data set
                                                                                                        Ali Shamakhi
Format                      Input/output format of the tools and other                                  Huascar Sanchez
                              specification formats                                                     Temesghen Kahsai; etc
Repository                  A URL indicating the repository of the
                             tool or another source where it can be
                             downloaded
Article                     A (preferably DOI) link pointing to a          of author contributions, as shown by Corrêa Jr., Silva, da
                             publication about a tool                      F. Costa, and Amancio [26], is far from being simple and/or
Concept                     All tags, application domains, etc. can be     resolved even for “normal” academic literature, and deserves
                             concepts. Some specific concepts are          even more careful investigation if we take tool making and
                             created as sub-classes to allow domain        empirical validation into account.
                             experts to modify the ontology file for
                             tool classification
PV                          Seven hierarchy levels (PV0–PV6) that          4.3 Data set statistics
                             classify tools. Each tool receives a
                             single classification                         The data set contains 427 tools, 26 specification formats and
Conference                  The conference where an article was            71 tags. The tools are split over the PV-levels as follows:
                             published
Person                      Persons related to a tool, proceedings or
                             any other concepts                             • PV0: 16 — cf. Sect. 5.1
Writer                      Sub-class of Person: Authors of an Article      • PV1: 98 — cf. Sect. 5.2
CodeContributor             Sub-class of Person. Contributor to a           • PV2: 84 — cf. Sect. 5.3
                             Repository                                     • PV3: 74 — cf. Sect. 5.4
                                                                            • PV4: 101 — cf. Sect. 5.5


123
Extract, model, refine: improved modelling of program verification tools...                                                            1303




Fig. 5 An overview of the different steps that are undertaken each time the data set is enriched


Table 3 An overview of how many tools were identified in the CAV              some repositories are hosted on organisation-specific GitLab
and TACAS proceedings                                                         instances and some articles link to an organisation’s website
                   Tools                 Prototypes            No tool        instead of a DOI.
                                                                                  In total 1419 code contributors and 1188 authors were
CAV                257 (50%)             54 (10%)              95 (22%)
                                                                              identified. Of these contributors, 1086 people have provided
TACAS              94 (18%)              0 (0%)                19 (4%)
                                                                              a name which can be used to identify same-as relationships
Overall            351 (68%)             54 (10%)              114 (22%)      with authors. In total, 273 same-as relationships have been
                                                                              found when looking for exact name matches. 169 tools con-
                                                                              tain at least one expert who contributed to both the paper and
 • PV5: 13 — cf. Sect. 5.6                                                    the code. The actual number is expected to be much higher
 • PV6: 13 — cf. Sect. 5.7                                                    as we only considered exact matches and not all code con-
 • No PV: 46                                                                  tributor’s have provided a name that can be matched to.
 • To be categorised: 8

    Table 3 gives an overview of how many tools were iden-                    5 Trends in PV-levels
tified in the CAV and TACAS proceedings respectively. The
papers that presented unnamed prototypes were counted sep-                    In this section, we identify different subgroups within each
arately and excluded from the data set. Papers that did not                   PV-level of the megamodel.
discuss any implementation, such as theoretical papers or
case studies, counted towards the “No tool” column. Overall,
                                                                              5.1 PV0: potential tools
78% of the papers that we looked at included some imple-
mentation, 68% of which were identifiable tools and 10%
were prototypes. We suspect the percentages to be consider-
ably lower, had we chosen other conferences without a strong
tool focus.
    The light snowballing principle that we have mentioned
above (another tool page is added if at least two existing
entries refer to the same tool which is not yet in the data set)
led to adding another 76 tools to the data set.
    We consider limitations of our data set and the process of
creating it, at the very end of the paper, in Sect. 6.1.

4.3.1 Data enrichment statistics

400 out of 427 of the markdown files were included in the
data enrichment process. The other files were excluded as
they were READMEs and pages that did not describe tools
but specification formats.                                                       At the time of writing of this paper, ProVerB had 16
    In total, we could automatically retrieve information about               tools on PV0. It is the absolute minority compared to other
256 of 269 repositories. This information included code con-                  categories, which is intentional due to the inherent non-
tributors, the last commit date and the “About” section shown                 verifying nature of PV0. As the word cloud, generated from
on a repository’s page. For the articles, we were able to enrich              tool descriptions and visualised above, suggests, it is more
518 of 525 articles successfully. For each article, it retrieves              about analysis than proving, and more about “matching” than
the title, abstract and authors. Some repositories and arti-                  “checking”, and some of these “tools” are mere libraries for
cles could not be enriched as this data was not available                     larger packages like Coq and Uppaal. 13 of the PV0 tools pro-
through Github’s, Springer’s or Crossref’s API. For example,                  vide facilities to work with various kinds of seemingly formal


                                                                                                                                 123
1304                                                                                                             S. Lathouwers et al.


artefacts: grammars, regular expressions, automata, decision      mulae, etc. 9 more tools could be seen as limited frameworks
diagrams, session types, and floating point numbers. How-         that are developed specifically to compare two models in a
ever, there is simply not enough formal rigour in the way         formal way. For example, SPAN [13] computes whether two
these tools operate these artefacts, for us to consider them      protocols are indistinguishable, and RABIT [1] checks inclu-
truly a part of the program verifier’s arsenal. As an example,    sion of languages generated by two Büchi automata. Another
consider ANTLR [69]: given a grammar, it generates a parser       8 tools can be seen as normalisers that bring a given model
for it. However, it does so without the grammar being per-        to some well-defined canonical state: Mealy machines and
ceived, modelled and transformed as a mathematical object.        Büchi automata can be automatically minimised, quantified
If the user provides ANTLR with a grammar which is uncon-         Boolean formulae can be simplified and turned into depen-
nected or ambiguous, then the generated parser will be faulty,    dency quantified Boolean formulae, etc.
and no warning might be issued.                                      21 different PV1 tools are linters, type checkers and
    Two remaining PV0 tools are, in fact, repositories:           checkers of other kinds of properties that are fixed and
Ceramist [42] and Prosa [43] are libraries that store formal      hardcoded into the tool (we will see checkers of user-
artefacts (definitions and proofs) but by themselves neither      specified properties on PV3). Such properties can include
provide arguments about their correctness, nor verify those       conformance, semantic preservation, type safety, automata
(both rely on Coq). The last PV0 tool is Smt-Switch [60],         emptiness, safety of Markov decision processes, thread
a collection of abstract classes that, if inherited from and      safety, etc. Reachability and termination analyses, due to
implemented, can help integrate SMT solvers—again, this           their internal workings, we count towards another category,
library by itself is definitely related to the PV domain, but     which includes metric calculators and tools that compute a
does not help bring any correctness guarantees.                   set of possible states of a model or infer ranking functions,
    What all PV0 tools have in common is their position on the    or compute upper and lower bounds of something — there
verification diagram we have shown in Sect. 3: they are claims    are 34 of them in total.
without arguments, without a prover and without a verifier.          Finally, the remaining 7 tools can execute models, sim-
The claims can be formal, but the surrounding context does        ulate their behaviour, (partly) visualise them and resolve
not qualify as PV tool support.                                   them otherwise: Murxla by Niemetz, Preiner, and Barrett
                                                                  [64] fuzzes SMT solvers, CabPy by Baier et al. [9] solves a
5.2 PV1: essential tools                                          two-player reachability game, Oink by van Dijk [85] solves a
                                                                  parity game, jcstress by Shipilëv [79] and PROVER by Ryou
                                                                  et al. [75] execute test cases in a specific order, CLEAR by
                                                                  Barbon, Leroy, and Salaün [11] and dtControl by Ashok et al.
                                                                  [7] visualise the problematic part of a labelled transition sys-
                                                                  tem and previously externally synthesised controller code,
                                                                  respectively.

                                                                  5.3 PV2: creational tools




   Out of 98 tools on the PV1 level, 19 can be seen as
frameworks enabling their end users to work with certain
models/abstractions in a formal way. For instance, Frama-
C [24] contains functionality to treat C programs as formal
artefacts and thus can be used to build different program anal-
yses on top of it; BINSEC [31] provides similar functionality
and opportunities to implement binary level code analysis;
there are comparable tools that deal with Büchi automata,            There are 84 tools in PV2, their descriptions visualised
symbolic automata, decision diagrams, temporal logic for-         as above. The largest identifiable group, with 37 members,


123
Extract, model, refine: improved modelling of program verification tools...                                                            1305


consists of tools providing correct-by-construction artefacts                 5.4 PV3: property checking tools
given a specification: some synthesise a controller from an
LTL formula, others generate a dynamic neural network for a
given grid, some generate tests for a given circuit, while oth-
ers specifically generate classes that attempt to violate given
properties. This group of tools can produce fairly formal arte-
facts that are automatically verifiable, but they do not provide
any verifier means themselves. 8 more tools perform limited
versions of the same process, generating only enough con-
tent to fill in holes in an already partially existing model or
program. For instance, τ -DIGITS by Drews, Albarghouthi,
and D’Antoni [33] fills holes in a given loop-free program
from a probabilistic specification of its desired behaviour, and
MOVEC by Chen, Wang, Zhu, Xi, and Yang [25] performs
aspect weaving. Two more tools (DIGITS by Albarghouthi,
D’fAntoni, and Drews [2] and TarTar by ölbl, Leue, and Wies
[53]) specifically propose repairs as code fragments meant
to substitute existing code fragments assumed to be faulty.                      PV3 currently has 74 tools. Within PV3 we can clearly
   The second popular group contains 19 tools that encode                     identify three main subgroups: property checkers, assertion
or transform the artefact from one format or formalism to                     checkers and program repair tools.
another. This group covers tools for sequentialising parallel                    The first group consists of 40 tools that check properties
C code (MU-CSeq by Tomasco et al. [82]), or transform-                        for some form of model such as automata or network mod-
ing irreversible programs into reversible circuits (ReVerC by                 els. For instance, STAMINA by Neupane, Myers, Madsen,
Amy, Roetteler, and Svore [4]). There are several tools on                    Zheng, and Zhang [63] can be used to check properties of
this level that operate on temporal logic formulae, making a                  infinite-state continuous-time Markov chains.
timed automaton (MightyL by Brihaye, Geeraerts, Ho, and                          The second group consists of 28 tools that check assertions
Monmege [21]) or an Electrum model (Cervino by Peyras,                        for concrete artefacts. For example, SecC by Ernst and Mur-
Bodeveix, Brunel, and Chemouil [70]) or another temporal                      ray [34] can check information flow properties, expressed as
logic formula in a different dialect (MLTLconverter by Li,                    assertions, for C programs.
Vardi, and Rozier [59]) from them.                                               Four tools: Forester by Holík et al. [48], SymDIVINE
   8 tools can be used to refine specifications: for instance,                by Mrázek, Bauch, Lauko, and Barnat [62], Trainify by Jin,
by inferring type annotations from an untyped program such                    Tian, Zhi, Wen, and Zhang [50] and VeryMax by Borralleras
as Typpete by Hassan, Urban, Eilers, and Müller [46], or                      et al. [20] — fall in between these two groups. The first
generating permission pre- and postconditions for Viper pro-                  two of these work on LTL formulae as properties, but apply
grams like Sample by Dohrau, Summers, Urban, Münger, and                      them on real C/C++ code (SymDIVINE allows both “nor-
Müller [32] does.                                                             mal” assertions and LTL formulae). Trainify checks ACTL
   Finally, 10 tools generate configurations or settings for                  properties for Deep Reinforcement Learning systems defined
other tools, such as PeSCo by Richter and Wehrheim [73]                       in Python. VeryMax works both on programs (C/C++) and
which generates the best fitting configuration for CPAchecker                 models (transition systems).
by Beyer and Keremoglu [17] that fits previous experiences;
or SATzilla by Xu, Hutter, Hoos, and Leyton- Brown [92] that
decides which solver to call per instance based on predictors.




                                                                                                                                 123
1306                                                                                                            S. Lathouwers et al.


    Finally, there is also a small but growing group of tools       user-written assertions for Go programs as well as memory
that focuses on program repair: AllRepair by Rothenberg and         safety, data-race freedom and crash safety.
Grumberg [74] and NNRepair by Usman, Gopinath, Sun,                    Finally, there is a small group of what we can call lan-
Noller, and Păsăreanu [84]. These tools both identify faults      guage workbenches [39], and we strongly suspect that there
in the program, like other tools in PV3, and they also propose      are more of this kind that escaped our selection only because
a way to fix it.                                                    nobody published about them directly at CAV and TACAS
                                                                    recently. A language workbench was envisioned in 2005 as
5.5 PV4: specification checking tools                               a set of tools aiding the language engineer to design, imple-
                                                                    ment and integrate a collection of domain-specific languages
                                                                    into one unified solution. Some of the popular language work-
                                                                    benches in model-driven software engineering include Xtext,
                                                                    MPS, MetaEdit+, Rascal and Spoofax. The two language
                                                                    workbenches that we have found mentioned for the domain
                                                                    of program verification, were DLC by Evrard [35], which can
                                                                    automatically generate distributed implementation of con-
                                                                    current systems modelled in the LNT language, which can be
                                                                    verified using the CADP toolbox; and PrDK by Arbab [51], a
                                                                    development kit for programming communication protocols.


                                                                    5.6 PV5: fully controlled verification tools




    Currently, PV4 is the largest category with 101 tools, the
descriptions of all of them also used for a word cloud above.
The largest group (51) of tools within PV4 are the solvers.
These tools produce a satisfiability result for SAT (satisfiabil-
ity), SMT (satisfiability modulo theories), QBF (quantified
Boolean formulae) or CHC (constrained Horn clauses) prob-
lems. Because these tools verify a specific property (namely,
satisfiability), one may have expected to find them in PV1.
However, these tools typically generate interpretations for
the given problem to show that it is (un)satisfiable. So, inter-
nally each of these tools consists of two essential parts: the
property generator which generates the interpretation and
the verifier which checks whether this interpretation makes
the formula satisfiable. This group also contains the tool that        Continuing the same trend, on PV5 we see a uniform
is referred to the most often in our data set — namely, Z3 by       group of 13 verification workbenches. These are tools that
Moura and Bjørner [30]. It belongs to SMT solvers together          allow users to write their own specifications and combine
with 17 other tools; there are also 22 SAT solvers; 3 CHC           these together with desired properties into a formal math-
solvers; and 6 solvers of other kinds.                              ematical representation. These formal representations can
    Many PV tools from other levels encode their problems           then be compared with representations of programs or their
into satisfiability problems and then use one of the tools in       properties for the verification. Users can have very fine-
this group as a back end.                                           grained influence on the results of these tools because they
    PV4 also includes 25 tools that generate properties or          are allowed to write their own specification. For example,
check built-in specifications typically depending on the            Attestor by Arndt, Jansen, Katoen, Matheja, and Noll [6]
domain that the tool targets. Some examples of built-in spec-       allows the user to specify the initial heap configuration and
ifications that are checked, include memory safety, data-race       the behaviour of the garbage collector that should be taken
freedom, termination and absence of runtime errors. Many of         into account when verifying a property for a Java program.
these tools also provide support to check user-written prop-        Similarly, UPPAAL by Bengtsson, Larsen, Larsson, Petters-
erties. For instance, Gobra by Wolf et al. [90] can check           son, and Yi [14] is a workbench for automatic verification of


123
Extract, model, refine: improved modelling of program verification tools...                                                               1307


safety and bounded liveness properties of real-time systems                   the different types of tools into seven categories: PV0, PV1,
modelled as networks of timed automata.                                       PV2, PV3, PV4, PV5 and PV6. These categories are increas-
                                                                              ingly more demanding and increasingly more powerful: it is
5.7 PV6: proving tools                                                        possible to gain some benefit from a PV0 or PV1 tool within
                                                                              the first day of being introduced to it, but much further refine-
                                                                              ment and improvement might not be possible; on the other
                                                                              side of the spectrum, PV6 tools can do almost everything, and
                                                                              require a relevant PhD degree to operate. Thus, there is no
                                                                              discussion on “what is the best PV-level”, just a classification
                                                                              that helps to match a tool to customer needs.
                                                                                  To bring the megamodel to life, we have designed a meta-
                                                                              model to hold semi-structured information about a PV tool,
                                                                              including its PV-level, name, input/output, etc, and instan-
                                                                              tiated it for all tools that we have found being mentioned
                                                                              and used in the last five years of two top conferences in the
                                                                              field: CAV and TACAS. Our data set at the time of writing
                                                                              consists of 450+ tools, formats and libraries. By setting up
                                                                              a megamodel as well as a data set, we hope to provide both
                                                                              a theoretical as well as a practical starting point to get into
                                                                              the world of PV tools and methods. A good starting point
                                                                              for browsing and exploring ProVerB would be its hypertext
   All 13 tools in PV6 are proof workbenches. Many of the                     frontend: http://slebok.github.io/proverb/ which also con-
tools in previous categories give a yes/no answer to indicate                 tains links to other sites (GitHub, DOIs, etc) for each tool.
whether a property holds, and in any case allowing at most
some influence on the property generating and handling pro-                   6.1 Threats to validity
cess, but not on the final proof. PV6 tools, however, will help
the user to construct and infer the correctness of a proof that               Conclusion validity. All the PV-classifications that we have
shows why a property is true or false. Some well-known tools                  performed, come from our personal interpretations of the
in PV6 are Coq by Bertot and Castéran [15], Isabelle/HOL                      contents of a fairly large body of fairly complex academic
by Nipkow, Wenzel, and Paulson [65], Lean by L. de Moura                      papers. Thus, it is possible that some tools have been misclas-
and Ullrich [29] and Vampire by Kovács and Voronkov [54].                     sified as belonging to one level while they actually belong
Their comparison is a highly nontrivial task even for profes-                 to another level. To prevent misclassifications, the authors
sional mathematicians [87].                                                   were actively double checking each other’s verdicts and had
                                                                              extensive discussions about arguable conclusions. Eventu-
                                                                              ally we plan to reach out to authors of all tools included
6 Conclusion & roadmap                                                        in ProVerB individually, with a detailed explanation of the
                                                                              seven PV-levels and a request to review our summaries and
Our contribution of this paper is two-sided. On one side, we                  refine them, possibly leading to reclassifications. If such a
have analysed a fairly complex domain and turned one of                       community effort causes a noticeable resonance, it would be
the commonly used visualisations of its core processes into a                 possible to eliminate this threat entirely.
full fledged megamodel that helped us to split the domain into                    Internal validity. Since our project is more of an obser-
much more intelligible smaller categories. On the other side,                 vational and classificational nature, initially we did not
we have processed hundreds of academic papers published                       attempt to establish any causal relationships. Hence, inter-
across several recent years, classified them according to the                 nal validity was not among our major concerns. However,
proposed megamodel and generated a user-friendly website                      since the moment we started enhancing the data set with
allowing software engineers to compare and assess tools in                    other sources of linked data such as GitHub and Springer-
a bit more secure, complete and safe way than before.                         Link API, it becomes increasingly more relevant to correctly
   The megamodel that we have presented, identifies the dif-                  establish contributor identity equivalence across multiple
ferent type of program verification tools that we found exist-                platforms with varying usernames and non-strictly match-
ing or that can possibly be made to exist. This megamodel is                  ing names [38].
based on the classic division of roles in a correctness proof as                  Construct validity. As we have explained in Sect. 3, our
introduced by Goldwasser et al. [41] that is currently accepted               megamodel was designed based on the classic division of
by the computational community. Our megamodel divides                         roles in a correctness establishing setup as described by


                                                                                                                                    123
1308                                                                                                               S. Lathouwers et al.


Goldwasser et al. [41], in the modern reinterpretation by            the ProVerB website, can explore the data set in different
Wigderson [88]. By reusing a model that originates from the          ways, such as systematically covering some PV-level after
right domain, we hope to have found a mature foundation              determining which one is needed, or browsing through tools
that will allow us to classify any possible tool in the future       listed under one of the tags (e.g. “LLVM” or “Smart con-
by matching its components and concepts to the claim, the            tract”). To improve the usability in this scenario, we believe
prover, the arguments and the verifier. Only if we encounter         it would be useful to develop a decision tree to help people
future tools that do not fit into this model, will we have to        find the right tool. Such a decision tree can take the client’s
redesign the megamodel again. However, in the works of               requirements into account such as the domain to which it is
Wigderson [88], generalising the notion of a proof from being        applied and the problems it should solve.
a unidirectional communication from the prover towards the               One of the aspects of seeking the right tools for the job
verifier, to a bidirectional series of communications, handling      that we have not considered before, is tool popularity among
interactivity, errors, randomness and other natural aspects of       other potential users — for some definition of it. However,
computation, has opened a lot of doors and led to the dis-           there are many ways to assess popularity or utilisation of
covery of a number of complexity classes with a distinctly           program verification tools, such as:
higher expressive power. For instance, relying on more than
two verifiers at the same time is not uncommon in PV, but             • Presence: in our study we have declared that even one
this is mostly done for practical considerations such as try-           use or mention of a tool justifies its addition to ProVerB
ing all available ones to watch only the fastest complete its           — however, more frequent appearances at conferences
proof. It is neither considered nor suspected that multi-prover         and workshops, as well as prominence in tutorials and
or multi-oracle PV tools can lead us to a broader computa-              keynotes, may indicate higher popularity. In some sub-
tional class. Since this has not been researched or established         domains of program verification contests are being held
before, we also do not consider such multi-tier setups as one           regularly, and if a tool appears there often, it means it is
of the PV-levels explicitly.                                            highly competitive among cutting edge alternatives.
   External validity. We have gathered data from publica-             • Citations: the number of papers referred to either the
tions at CAV and TACAS, which seemed like a good choice of              main paper introducing the tool in question, or collec-
information since both favour papers about program verifica-            tively to all papers written about the tool. This can be
tion tools to non-tool papers and non-PV content. However,              possibly calibrated by tracking the age of citations as
there are more venues that target the program verification              well, to avoid the bias towards older tools.
field (POPL, PLDI, FASE, LICS, etc). It is unknown at                 • Usage: many platforms allow tool makers to track the
the moment what biases we have created in the data set                  number of downloads, installations or active users. Tools
by limiting ourselves to only CAV and TACAS and related                 mature enough to be used in the industry can also often
papers, techniques and tools. While limited, the number of              be tracked with respect to their adoption, either directly
tools (380+) included is significant, and they seem reason-             through companies applying them to solve their prob-
ably spread out among the different PV-levels. We see that              lems, or indirectly by counting published case studies
the most popular tools are included, partly because we also             and success stories.
include tools if they are referred to by at least two other tools.    • Community: engagement can be a good proxy for a tool
So, while perhaps limited on the grand scheme of things, we             popularity, hence the reliance in many studies on counters
think that this is a good starting point for the data set.              like GitHub stars and forks, or the number of contributors,
                                                                        issue resolutions or commits.
6.2 Roadmap for the future                                            • Social Media: presence on social media platforms
                                                                        goes beyond simple vanity and can also mean that
With the megamodel designed, and the initial data set col-              blogs/podcasts, discussion fora/groups, Discord/Slack
lected, our main focus for the future is the usage of our work.         servers, Reddit/StackOverflow sections, etc, are readily
The PV-levels naturally cover the entire spectrum of all possi-         available to support newcomers learning to use this tool.
ble tools from informal/semiformal to self-validating, so the         • Surveys: tool popularity can be measured directly by ask-
usual future work claim of adding more levels to the meg-               ing a significant number of researchers and practitioners
amodel, cannot possibly apply here. Thus, below we discuss              to express their preferences by filling in questionnaires.
several concrete scenarios to show how it can be used and               This is a labour intensive initiative but yielding quali-
extended to cater for those uses.                                       tative insights into actual tool popularity and perceived
   Scenario 1: the first scenario, which closely resembles our          effectiveness.
original goal of collecting and classifying available program
verification tools for ourselves, is to help users find suitable        There are also composite methods of expression popular-
tools. Even now potential users of any of the tools listed at        ity and adoption of a piece of software, such as Software


123
Extract, model, refine: improved modelling of program verification tools...                                                                  1309


Universe Graphs by Kula, De Roover, German, Ishio, and                           relying on older dependencies, keeping vulnerabilities
Inoue [56]. In any case, we note that popularity has been                        unresolved, etc.
found to not correlate that much with other aspects of soft-
ware quality such as defect density [76] or security [80].                       Scenario 3: another usage scenario focuses on using the
Other studies have even found an inverse correlation, such as                 available data, and a similar format, to improve artefact eval-
Alsmadi and Alazzam [3] who observed that projects with                       uations or paper reviewing process. In artefact evaluations,
higher number of downloads also tend to have higher cyclo-                    reviewers can typically indicate what artefacts they would be
matic complexity.                                                             interested in reviewing based on a title and/or abstract [55].
    Scenario 2: the second scenario is similar to the first one,              However, these do not always provide a clear description
but the selection is done in the presence of a knowledge-                     of the tool’s capabilities due to which a reviewer end up
able consultant. Such an expert has sufficient knowledge                      having to review a tool outside of their field of expertise.
about the field of program verification and thus can deter-                   Using a format as in our data set would provide a more struc-
mine what type of tool suits the client’s problem. Exploring                  tured approach to describe the tool and can be helpful to
the domain together with the client could potentially lead not                correctly identify what tools’ capabilities are to prevent such
only to reaching its intended goal of finding and selecting the               situations. Moreover, if this format can be incorporated into
right tool, but also to insights in requirements elicitation. It is           artefact evaluations as a required part of the submission, this
well-known that exploring the solution space often leads to                   provides a distributed approach that allows us to keep the
discoveries on the problem definition side. For this scenario,                data more easily up to date.
the most useful improvement would be to subdivide the PV-                        Other key aspects that may prove useful in the context of
levels further. At the moment the levels are neither uniform                  this scenario, are:
nor equidimensional: some are naturally larger, others con-
tain substantially sized identifiable subcategories.                           • Evaluation Criteria can be standardised and applied
    Different aspects can be of more importance in this sce-                     consistently across different tools, improving the rigour
nario, or at least can gain more weight due to the presence                      and effectiveness of the entire artefact evaluation pro-
of a verification expert acting as a requirements elicitor, such                 cess. It might even be possible to devise a standardised
as:                                                                              methodology to evaluate tools according to the PV-level
                                                                                 they find themselves on.
                                                                               • Submission Guidelines are becoming clearer each year,
 • Performance: efficiency of the candidate tool can be                          but perhaps clear positioning of a submitted tool on a
   assessed by either their known position in the last rel-                      PV-level and clearly stating its input and output formats,
   evant competition, or by observing how consistently it                        as well as filling out other fields that we ended up using
   passes appropriate applicable benchmarks.                                     within ProVerB, could align tool authors’ and evaluators’
 • Flexibility: adapting the tool to the needs of the user                       expectations better.
   might involve scalability issues, assumptions about input                   • Tool-Agnostic Benchmarks can be based on data sets
   data, customisability and extensibility, as well as some                      that are specific to a PV-level or to a format or to a com-
   other similar details that can subtly influence the choice.                   bination of a tags/concepts. This will not only improve
 • Integration with widely used formats, platforms, frame-                       replicability, but also encourage and significantly sim-
   works or toolchains can enhance the tool’s chances of                         plify cross-tool comparable studies.
   being a part of the ultimate solution.                                      • Automation of Evaluation is the ultimate goal of artefact
 • Learnability: some tools are known to be more user-                           assessment. While there is perhaps still place for human
   friendly than others, or having a particularly steep or                       evaluation as a part of it, just like there is a place for it for
   gentle learning curve. This can be supported by avail-                        peer reviewing papers, many steps such as conformance
   ability and reliability of documentation, by accessible                       to a declared format or the ability to produce the same
   tutorials and books, as well as by other means of skill                       outputs as reported in the accompanying paper, can and
   transfer.                                                                     should be automated to avoid manual labour and human
 • Community can play a role just like in the case of pop-                       bias.
   ularity above. Ongoing support and continuing improve-
   ment weighs just as much here as having an active group                        Scenario 4: for all three of the scenarios described above,
   of core developers and helpful and inclusive learning                      it can be useful to further extend our data set. This can focus
   community.                                                                 on either adding new entries to the current data set, or to
 • Risks, if known, can be weighed realistically and mit-                     extend the information that is available for the current tools.
   igated by planning for contingencies. This applies to                      At the moment, in order to classify a new tool that is absent
   future plans for dealing with the tool becoming obsolete,                  from the data set, into an appropriate PV-level, one would


                                                                                                                                      123
1310                                                                                                                              S. Lathouwers et al.


basically need to read this paper and combine their under-                  right holder. To view a copy of this licence, visit http://creativecomm
standing of what the tool does with their understanding of the              ons.org/licenses/by/4.0/.
what each PV-level stands for. It will be more appropriate to
design a specific decision tree with clear questions, answers
to which will unequivocally lead to one level or the other. In
a way, this is an “implementation detail” since it might not                References
require deeper understanding of the megamodel, but it is also
                                                                             1. Abdulla, P.A., Chen, Y.-F., Clemente, L., Holík, L., Hong, C.-D.,
known that explicitly renarrating a megamodel significantly                     Mayr, R., Vojnar, T.: Simulation subsumption in Ramsey-based
increases its appreciation among domain experts and other                       Büchi automata universality and inclusion testing. In: Touili, T.,
users [93].                                                                     Cook, B., Jackson, P. (Eds.), In: Proceedings of the 22nd inter-
                                                                                national conference on computer aided verification (CAV) (pp.
    Pragmatically, contributing to the ProVerB repository is
                                                                                132–147). Springer (2010)
straightforward: the data set is a GitHub repo which can be                  2. Albarghouthi, A., D’Antoni, L., Drews, S.: Repairing decision-
forked and worked on, with a pull request asking to merge it                    making programs under uncertainty. In: Majumdar, R., Kunčak,
back to the original. In order to add a new tool, an external                   V. (Eds.), In: Proceedings of the 29th international conference on
                                                                                computer aided verification (CAV) (pp. 181–200). Springer (2017)
contributor can create a new Markdown document from the
                                                                             3. Alsmadi, I., Alazzam, I.: Software attributes that impact popularity.
template — manually or with one of the available scripts (e.g.                  In: Proceedings of the eighth international conference on informa-
parsing a proceedings volume and suggesting a number of                         tion technology (ICIT) (pp. 205–208) (2017)
tools found there heuristically). All the refinement features                4. Amy, M., Roetteler, M., Svore, K.M.: Verified compilation of
                                                                                space-efficient reversible circuits. Majumdar, R., Kunčak, V. (Eds.),
described above, also remain accessible: for instance, it is
                                                                                In: Proceedings of the 28th international conference on computer
sufficient to add DOIs of papers and URIs of source code in                     aided verification (CAV) (pp. 3–21). Springer (2017)
order for our GitHub workflow to pick them up and replace                    5. Andova, S., van den Brand, M., Engelen, L.J.P., Verhoeff, T.: MDE
bare links with paper titles and to add last activity information               basics with a DSL focus. In: Advanced lectures of the 12th inter-
                                                                                national school on formal methods for the design of computer,
from accessing the APIs.
                                                                                communication and software systems: formal methods for model-
    Additionally, it is interesting to investigate the possibil-                driven engineering (Vol. 7320, pp. 21–57). Springer (2012)
ity of combining our ontology with others, including, e.g.                   6. Arndt, H., Jansen, C., Katoen, J.-P., Matheja, C., Noll, T.: Let this
the runtime verification tool taxonomy by Falcone et al. [36]                   graph be your witness! In: Chockler, H., Weissenbacher, G. (Eds.),
                                                                                In: Proceedings of the 30th international conference on computer
and the repository structure proposed by Schlick et al. [77].
                                                                                aided verification (CAV) (pp. 3–11). Springer (2018)
When extending the ontology, it is important to consider how                 7. Ashok, P., Jackermeier, M., Křetínský, J., Weinhuber, C.,
to incorporate grey literature. So far, we have only included                   Weininger, M., Yadav, M.: dtControl 2.0: explainable strategy rep-
tools that were introduced in the academic literature. How-                     resentation via decision tree learning steered by experts. In: Groote,
                                                                                J.F., Larsen, K.G. (eds.) In: International conference on tools and
ever, David et al. [27] have shown that, for modelling tools
                                                                                algorithms for the construction and analysis of systems, pp. 326–
that support blended modelling, grey literature had a higher                    345. Springer, Cham (2021)
ratio of tools introduced per literature source. In the grey                 8. Aydemir, B.E., Bohannon, A., Fairbairn, M., Foster, J.N., Pierce,
literature, they identified 68 tools in 1494 sources whereas,                   B.C., Sewell, P., Zdancewic, S.: Mechanized metatheory for the
                                                                                masses: the PoplMark challenge. In: Hurd, J., Melham, T.F. (Eds.),
in the academic literature, they identified 68 tools in 4975
                                                                                In: Proceedings of the 18th international conference on theorem
entries. It is unclear whether such a ratio would be simi-                      proving in higher order logics (TPHOLs) (Vol. 3603, pp. 50–65).
lar in the field of program verification, a field known for its                 Springer (2005)
theoretical difficulties. Nonetheless, in all likelihood, we are             9. Baier, C., Coenen, N., Finkbeiner, B., Funke, F., Jantsch, S., Siber,
                                                                                J.: Causality-based game solving. In: Silva, A., Leino, K.R.M.
currently missing some tools that have only been discussed
                                                                                (eds.) In: International conference on computer aided verification,
in grey literature.                                                             pp. 894–917. Springer, Cham (2021)
                                                                            10. Baldassarre, M.T., Ernst, N., Hermann, B., Menzies, T., Yedida, R.:
Acknowledgements This project was partly funded by the Neder-                   (Re) use of research results (is rampant). Commun. ACM 66(2),
landse Organisatie voor Wetenschappelijk Onderzoek through the VICI             75–81 (2023). https://doi.org/10.1145/3554976
639.023.710 Mercedes project.                                               11. Barbon, G., Leroy, V., Salaün, G.: Debugging of behavioural
                                                                                models with CLEAR. In: Vojnar, T., Zhang, L. (eds.) Tools and
Open Access This article is licensed under a Creative Commons                   algorithms for the construction and analysis of systems: 25th Inter-
Attribution 4.0 International License, which permits use, sharing, adap-        national Conference, TACAS 2019 pp. 386–392. Springer, Cham
tation, distribution and reproduction in any medium or format, as               (2019). https://doi.org/10.1007/978-3-030-17462-0_26
long as you give appropriate credit to the original author(s) and the       12. Barringer, H., Havelund, K.: TraceContract: a Scala DSL for trace
source, provide a link to the Creative Commons licence, and indi-               analysis. In: Proceedings of the 17th international symposium of
cate if changes were made. The images or other third party material             formal methods (Vol. 6664, pp. 57–72). Springer (2011)
in this article are included in the article’s Creative Commons licence,     13. Bauer, M.S., Chadha, R., Prasad Sistla, A.R., Viswanathan, M.:
unless indicated otherwise in a credit line to the material. If material        Model checking indistinguishability of randomized security pro-
is not included in the article’s Creative Commons licence and your              tocols. In: Chockler, H., Weissenbacher, G. (eds.) In: International
intended use is not permitted by statutory regulation or exceeds the            conference on computer aided verification (CAV), pp. 117–135.
permitted use, you will need to obtain permission directly from the copy-       Springer, Cham (2018)


123
Extract, model, refine: improved modelling of program verification tools...                                                                         1311


14. Bengtsson, J., Larsen, K., Larsson, F., Pettersson, P., Yi, W.:           30. de Moura, L.M., Bjørner, N.S.: Z3: An efficient SMT solver. In:
    UPPAAL: a tool suite for automatic verification of real-time sys-             Ramakrishnan, C.R., Rehof, J. (Eds.), In: Proceedings of the 14th
    tems. In: Alur, R., Henzinger, T.A., Sontag, E.D. (eds.) Hybrid               international conference on tools and algorithms for the construc-
    systems, pp. 232–243. Springer, Cham (1996)                                   tion and analysis of systems (tacas) (Vol. 4963, pp. 337–340).
15. Bertot, Y., Castéran, P.: Interactive theorem proving and program             Springer (2008)
    development: Coq’art: the calculus of inductive constructions.            31. Djoudi, A., Bardin, S.: BINSEC: binary code analysis with low-
    Springer, London (2004)                                                       level regions. In: Baier, C., Tinelli, C. (Eds.), In: Proceedings of
16. Beyer, D.: Progress on software verification: Sv-comp 2022. In:               the 21st international conference on tools and algorithms for the
    Fisman, D., Rosu, G. (eds.) Tools and algorithms for the construc-            construction and analysis of systems (TACAS) (Vol. 9035, pp. 212–
    tion and analysis of systems, pp. 375–402. Springer, Cham (2022)              217). Springer (2015)
17. Beyer, D., Keremoglu, M.E.: Cpachecker: a tool for configurable           32. Dohrau, J., Summers, A.J., Urban, C., Münger, S., Müller, P.:
    software verification. In: Gopalakrishnan, G., Qadeer, S. (eds.)              Permission inference for array programs. In: Chockler, H., Weis-
    Computer aided verification, pp. 184–190. Springer, Cham (2011)               senbacher, G. (eds) In: Computer aided verification. CAV 2018.
18. Bicarregui, J., Hoare, C.A.R., Woodcock, J.C.P.: The verified soft-           (pp. 55–74). Springer (2018)
    ware repository: a step towards the verifying compiler. Formal Asp.       33. Drews, S., Albarghouthi, A., D’Antoni, L.: Efficient synthesis
    Comput. 18(2), 143–151 (2006). https://doi.org/10.1007/s00165-                with probabilistic constraints. In: Dillig, I., Tasiran, S. (Eds.), Pro-
    005-0079-4                                                                    ceedings of the 30th international conference on computer aided
19. Bodeveix, J., Filali, M., Lawall, J., Muller, G.: Formal methods              verification (CAV) (pp. 278–296). Springer (2019)
    meet domain specific languages. In: Romijn, J., Smith, G., van de         34. Ernst, G., Murray, T.: SecCSL: Security concurrent separation
    Pol, J. (Eds.), In: Proceedings of the fifth international conference         logic. In: Dillig, I., Tasiran, S. (Eds.), In: Computer aided veri-
    on integrated formal methods (IFM) (Vol. 3771, pp. 187–206).                  fication: 31st international conference, CAV 2019 (pp. 208–230).
    Springer (2005)                                                               Springer (2019)
20. Borralleras, C., Brockschmidt, M., Larraz, D., Oliveras, A.,              35. Evrard, H.: Dlc: Compiling a concurrent system formal specifica-
    Rodríguez-Carbonell, E., Rubio, A.: Proving termination through               tion to a distributed implementation. In: Chechik, M., Raskin JF
    conditional termination. In: Legay, A., Margaria, T. (eds.) Tools             (Eds.), In: Tools and algorithms for the construction and analy-
    and algorithms for the construction and analysis of systems, pp.              sis of systems: 22nd international conference, TACAS 2016 (pp.
    99–117. Springer, Cham (2017)                                                 553–559). Springer (2016)
21. Brihaye, T., Geeraerts, G., Ho, H.M., Monmege, B.: Mightyl:               36. Falcone, Y., Krstic, S., Reger, G., Traytel, D.: A taxonomy for
    a compositional translation from MITL to timed automata. In:                  classifying runtime verification tools. Int. J. Softw. Tools Technol.
    Majumdar, R., Kunčak, V. (eds.) Computer aided verification, pp.             Transf. 23(2), 255–284 (2021). https://doi.org/10.1007/s10009-
    421–440. Springer, Cham (2017)                                                021-00609-z
22. Broadfoot, G.H., Broadfoot, P.J.: Academia and industry meet:             37. Ferrari, A., Mazzanti, F., Basile, D., Beek, M.H.t., Fantechi, A.:
    some experiences of formal methods in practice. Proceedings of                Comparing formal tools for system design: a judgment study.
    the 10th asia-pacific software engineering conference (APSEC)                 In: Proceedings of the ACM/IEEE 42nd international conference
    (p.49). IEEE Computer Society (2003)                                          on software engineering (pp. 62–74). Association for Computing
23. Bucchiarone, A., Ciccozzi, F., Lambers, L., Pierantonio, A., Tichy,           Machinery (2020)
    M., Tisi, M., Zaytsev, V.: What is the future of modelling? IEEE          38. Foley, M.J., Kochalko, D.L.: Open researcher and contributor iden-
    Softw. Insights (IEEE Softw.) 38, 119–127 (2021). https://doi.org/            tifier, a contemporary Stanley. (2012) https://docs.lib.purdue.edu/
    10.1109/MS.2020.3041522                                                       cgi/viewcontent.cgi?article=1133&context=charleston
24. Canet, G., Cuoq, P., Monate, B.: A value analysis for C programs.         39. Fowler, M.: Language workbenches: the killer-app for domain
    In: Ninth IEEE international working conference on source code                specific languages? MartinFowler.com. https://martinfowler.com/
    analysis and manipulation, SCAM 2009, 2009 (pp. 123–124). IEEE                articles/languageWorkbench.html
    Computer Society (2009)                                                   40. Frey, G., Litz, L.: Formal methods in PLC programming. In:
25. Chen, Z., Wang, Z., Zhu, Y., Xi, H., Yang, Z.: Parametric runtime             Proceedings of the international conference on systems, man &
    verification of C programs. In: Chechik, M., Raskin, J.F. (eds.)              cybernetics: “Cybernetics evolving to systems, humans, organi-
    Tools and algorithms for the construction and analysis of systems,            zations, and their complex interactions” (pp. 2431–2436). IEEE
    pp. 299–315. Springer, Cham (2016)                                            (2000)
26. Corrêa, E.A., Jr., Silva, F.N., da F. Costa, L., Amancio, D.R.: Pat-      41. Goldwasser, S., Micali, S., Rackoff, C.: The knowledge complexity
    terns of authors contribution in scientific manuscripts. J. Inform.           of interactive proof-systems. In: Proceedings of the seventeenth
    11(2), 498–510 (2017). https://doi.org/10.1016/j.joi.2017.03.003              annual ACM symposium on theory of computing (SToC) (p. 291–
27. David, I., Latifaj, M., Pietron, J., Zhang, W., Ciccozzi, F., Mala-           304). Association for Computing Machinery (1985)
    volta, I., Hebig, R.: Blended modeling in commercial and open-            42. Gopinathan, K., Sergey, I.: Certifying certainty and uncertainty in
    source model-driven software engineering tools: a systematic                  approximate membership query structures. In: Lahiri, S.K., Wang,
    study. Softw. Syst. Model. 22(1), 415–447 (2023). https://doi.org/            C. (Eds.), In: Computer aided verification: 32nd international con-
    10.1007/s10270-022-01010-3                                                    ference, CAV 2020 (CAV) (pp. 279–303). Springer (2020)
28. Davis, J.A., Clark, M.A., Cofer, D.D., Fifarek, A., Hinchman, J.,         43. Guo, X., Lesourd, M., Liu, M., Rieg, L., Shao, Z.: Integrating for-
    Hoffman, J.A., Wagner, L.G.: Study on the barriers to the industrial          mal schedulability analysis into a verified OS kernel. In: Dillig, I.,
    adoption of formal methods. In: Pecheur, C., Dierkes, M. (Eds.), In:          Tasiran, S. (Eds.), In: Computer aided verification: 31st interna-
    Proceedings of the 18th international workshop on formal methods              tional conference, CAV 2019 (pp. 496–514). Springer (2019)
    for industrial critical systems (FMICS) (Vol. 8187, pp. 63–77).           44. Hartmanns, A., Klauck, M., Parker, D., Quatmann, T., Ruijters, E.:
    Springer (2013)                                                               The quantitative verification benchmark set. In: Vojnar, T., Zhang,
29. de Moura, L., Ullrich, S.: The lean 4 theorem prover and program-             L. (Eds.), In: Proceedings of the 25th international conference on
    ming language. In: Platzer, A., Sutcliffe, A. (Eds.), In: Proceedings         tools and algorithms for the construction and analysis of systems
    of the 28th International conference on automated deduction                   (TACAS) (Vol. 11427, pp. 344–350). Springer (2019)
    (CADE) (pp. 625–635). Springer (2021)



                                                                                                                                             123
1312                                                                                                                                S. Lathouwers et al.


45. Harz, D., Knottenbelt, W.J.: Towards safer smart contracts: a                 on theory and applications of satisfiability testing (Vol. 12831, pp.
    survey of languages and verification methods. CoRR, (2018)                    377–386). Springer (2021)
    arxiv:1809.09805                                                          61. Meeus, W., Beeck, K.V., Goedemé, T., Meel, J., Stroobandt,
46. Hassan, M., Urban, C., Eilers, M., Müller, P.: Maxsmt-based type              D.: An overview of today’s high-level synthesis tools. Des.
    inference for Python 3. In: Chockler, H., Weissenbacher, G. (Eds.),           Autom. Embed. Syst. 16(3), 31–51 (2012). https://doi.org/10.
    In: Computer aided verification: 30th international conference,               1007/s10617-012-9096-8
    CAV 2018, (pp. 12–19). Springer (2018)                                    62. Mrázek, J., Bauch, P., Lauko, H., Barnat, J.: Symdivine: tool
47. Hermann, B., Winter, S., Siegmund, J.: Community expectations                 for control-explicit data-symbolic state space exploration. In:
    for research artifacts and evaluation processes. In: Proceedings              Bošnački, D., Wijs, A. (Eds.), In: Model Checking Software:
    of the 28th ACM joint meeting on European software engineer-                  23rd international symposium, SPIN 2016 (pp. 208–213). Springer
    ing conference and symposium on the foundations of software                   (2016)
    engineering (p. 469–480). New York, NY, USA: Association for              63. Neupane, T., Myers, C.J., Madsen, C., Zheng, H., Zhang, Z.:
    Computing Machinery (2020)                                                    Stamina: stochastic approximate model-checker for infinite-state
48. Holík, L., Hruška, M., Lengál, O., Rogalewicz, A., Šimáček, J.,              analysis. In: Dillig, I., Tasiran, S. (Eds.), In: Computer aided veri-
    Vojnar, T.: Forester: from heap shapes to automata predicates. In:            fication: 31st international conference, CAV 2019 (pp. 540–549).
    Legay, A., Margaria, T. (Eds.), In: Proceedings of tools and algo-            Springer (2019)
    rithms for the construction and analysis of systems (pp. 365–369).        64. Niemetz, A., Preiner, M., Barrett, C.: Murxla: a modular and highly
    Springer (2017)                                                               extensible API fuzzer for SMT solvers. In: Shoham, S., Vizel, Y.
49. Hutchinson, J.E., Whittle, J., Rouncefield, M.: Model-driven engi-            (Eds.), In: International conference on computer aided verification
    neering practices in industry: social, organizational and managerial          (pp. 92–106). Cham: Springer (2022)r
    factors that lead to success or failures. Sci. Comput. Progr. 89, 144–    65. Nipkow, T., Wenzel, M., Paulson, L.C.: Isabelle/HOL: a proof assis-
    161 (2014). https://doi.org/10.1016/j.scico.2013.03.017                       tant for higher-order logic, pp. 67–104. Springer, Cham (2002)
50. Jin, P., Tian, J., Zhi, D., Wen, X., Zhang, M.: Trainify: a CEGAR-        66. Nurwidyantoro, A., Shahin, M., Chaudron, M., Hussain, W.,
    driven training and verification framework for safe deep reinforce-           Perera, H., Shams, R.A., Whittle, J.: Towards a human values dash-
    ment learning. In: Shoham, S., Vizel, Y. (Eds.), In: International            board for software development: an exploratory study. In: Lanubile,
    conference on computer aided verification (pp. 193–218). Cham:                F., Kalinowski, M., Baldassarre, M.T. (Eds.), In: Proceedings of the
    Springer (2022). https://doi.org/10.1007/978-3-031-13185-1_10                 15th international symposium on empirical software engineering
51. Jongmans, S.-S.T.Q., Arbab, F.: Prdk: protocol programming with               and measurement (esem) (pp. 23:1–23:12). ACM (2021)
    automata. In: Chechik, M., Raskin, J.F. (Eds.), In: Tools and             67. Nurwidyantoro, A., Shahin, M., Chaudron, M.R.V., Hussain, W.,
    algorithms for the construction and analysis of systems: 22nd inter-          Shams, R.A., Perera, H., Whittle, J.: Human values in software
    national conference, TACAS 2016 (pp. 547–552). Springer (2016)                development artefacts: a case study on issue discussions in three
52. Klösch, R., Eixelsberger, W.: Challenges and experiences in man-              android applications. Info. Softw. Technol. 141, 106731 (2022).
    aging major software evolution endeavours such as euro conversion             https://doi.org/10.1016/j.infsof.2021.106731
    or Y2000 compliance. In: Proceedings of the 15th international            68. Ojamaa, A., Haav, H.-M., Penjam, J.: Semi-automated genera-
    conference on software maintenance (ICSM) (pp. 161–166). IEEE                 tion of DSL meta models from formal domain ontologies. In:
    Computer Society (1999)                                                       Bellatreche, L., Manolopoulos, Y. (Eds.), In: Model and data engi-
53. Kölbl, M., Leue, S., Wies, T.: Tartar: a timed automata repair tool.          neering: 5th international conference, MEDI 2015 (pp. 3–15).
    In: Lahiri, S.K., Wang, C. (Eds.), In: Computer aided verification:           Cham: Springer (2015)
    32nd international conference, CAV 2020 (pp. 529–540). Springer           69. Parr, T.: The definitive ANTLR 4 reference. Pragmatic Bookshelf,
    (2020)                                                                        Raleigh (2013)
54. Kovács, L., & Voronkov, A.: First-order theorem proving and               70. Peyras, Q., Bodeveix, J.-P., Brunel, J., Chemouil, D.: Sound verifi-
    Vampire. In: Sharygina, N., Veith, H. (Eds.), In: International con-          cation procedures for temporal properties of infinite-state systems.
    ference on computer aided verification (pp. 1–35). Springer (2013)            In: Silva, A., Leino, K.R.M. (Eds.), In: Computer aided verification:
55. Krishnamurthi, S.: Artifact evaluation for software conferences.              33rd international conference, CAV 2021 (pp. 337–360). Springer
    ACM SIGSOFT Softw. Eng. Notes 38(3), 7–10 (2013)                              (2021)
56. Kula, R.G., De Roover, C., German, D.M., Ishio, T., Inoue, K.: A          71. Pnueli, A.: The temporal logic of programs. In: Proceedings of the
    generalized model for visualizing library popularity, adoption, and           18th annual symposium on foundations of computer science (pp.
    diffusion within a software ecosystem. In: Proceedings of the 25th            46–57). IEEE Computer Society (1977)
    IEEE international conference on software analysis, evolution and         72. Punnoose, R.J., Armstrong, R.C., Wong, M.H., Jackson, M.: Sur-
    reengineering (SANER) (pp. 288–299) (2018)                                    vey of existing tools for formal verification. (Tech. Rep.). USDOE
57. Lamport, L.: The temporal logic of actions. ACM Trans. Progr.                 National Nuclear Security Administration (NNSA) (2014)
    Lang. Syst. (ToPLaS) 16(3), 872–923 (1994). https://doi.org/10.           73. Richter, C., Wehrheim, H.: Pesco: predicting sequential combina-
    1145/177492.177726                                                            tions of verifiers. In: Beyer, D., Huisman, M., Kordon, F., Steffen,
58. Lathouwers, S., Zaytsev, V.: Modelling program verification tools             B. (Eds.), In: Tools and algorithms for the construction and analy-
    for software engineers. In: Proceedings of the 25th international             sis of systems: 25 years of TACAS: TOOLympics (pp. 229–233).
    conference on model driven engineering languages and systems                  Springer (2019)
    (p.98-108). New York, NY, USA: Association for Computing                  74. Rothenberg, B.-C., Grumberg, O.: Must fault localization for pro-
    Machinery (2022) https://doi.org/10.1145/3550355.3552426                      gram repair. In: Lahiri, S.K., Wang, C. (Eds.), In: Computer aided
59. Li, J., Vardi, M.Y., Rozier, K.Y.: Satisfiability checking for mission-       verification: 32nd international conference, CAV 2020 (pp. 658–
    time LTL. In: Dillig, I., Tasiran, S. (Eds.), In: Computer aided              680). Springer (2020)
    verification: 31st international conference, CAV 2019 (pp. 3–22).         75. Ryou, W., Chen, J., Balunovic, M., Singh, G., Dan, A., Vechev, M.:
    Springer (2019)                                                               Scalable polyhedral verification of recurrent neural networks. In:
60. Mann, M., Wilson, A., Zohar, Y., Stuntz, L., Irfan, A., Brown, K.,            Silva, A., Leino, K.R.M. (Eds.), In: Computer aided verification:
    Barrett, C.W.: Smt-switch: a solver-agnostic C++ API for SMT                  33rd international conference, CAV 2021 (pp. 225–248). Springer
    solving. In: Li, C., Manyà, F. (Eds.), In: International conference           (2021)



123
Extract, model, refine: improved modelling of program verification tools...                                                                       1313


76. Sajnani, H., Saini, V., Ossher, J., Lopes, C.V.: Is popularity a mea-     91. Woodcock, J., Larsen, P.G., Bicarregui, J., Fitzgerald, J.S.: Formal
    sure of quality? an analysis of maven components. In: Proceedings             methods: practice and experience. ACM Comput. Surv. 41(4), 1–36
    of the 2014 IEEE International conference on software mainte-                 (2009). https://doi.org/10.1145/1592434.1592436
    nance and evolution (pp. 231–240) (2014)                                  92. Xu, L., Hutter, F., Hoos, H.H., Leyton-Brown, K.: Satzilla:
77. Schlick, R., Felderer, M., Majzik, I., Nardone, R., Raschke, A.,              portfolio-based algorithm selection for SAT. J. Artif. Intell. Res.
    Snook, C.F., Vittorini, V.: A proposal of an example and experi-              32, 565–606 (2008). https://doi.org/10.1613/jair.2490
    ments repository to foster industrial adoption of formal methods. In:     93. Zaytsev, V.: Renarrating linguistic architecture: a case study. In:
    Margaria, T., Steffen, B. (Eds.), In: Proceedings of the eighth inter-        Hardebolle, C., Syriani, E., Sprinkle, J., Mészáros, T. (Eds.), In:
    national symposium on leveraging applications of formal methods,              Post-proceedings of the sixth international workshop on multi-
    verification and validation (ISoLA) (Vol. LNCS 11247, pp. 249–                paradigm modeling (MPM 2012) (pp. 61–66). ACM Digital
    272). Springer (2018)                                                         Library (2012)
78. Shaaban, A.M., Schmittner, C., Gruber, T., Mohamed, A.B.,
    Quirchmayr, G., Schikuta, E.: Ontology-based model for automo-
    tive security verification and validation. In: Proceedings of the 21st
                                                                              Publisher’s Note Springer Nature remains neutral with regard to juris-
    international conference on information integration and web-based
                                                                              dictional claims in published maps and institutional affiliations.
    applications & services (IIWAS) (pp. 73–82). ACM (2019)
79. Shipilëv, A.: Java concurrency stress (jcstress). (2013) https://
    github.com/openjdk/jcstress/
80. Siavvas, M., Jankovic, M., Kehagias, D., Tzovaras, D.: Is pop-
                                                                                                                   Sophie Lathouwers received a
    ularity an indicator of software security? In: Proceedings if the
                                                                                                                   Ph.D. degree in Computer Sci-
    international conference on intelligent systems (IS) (pp. 692–697)
                                                                                                                   ence at the University of Twente
    (2018)
                                                                                                                   in the Netherlands. Her research
81. Stachowiak, H.: Allgemeine modelltheorie. Springer, Cham (1973)
                                                                                                                   interests include specifications, soft-
82. Tomasco, E., Nguyen, T.L., Inverso, O., Fischer, B., La Torre, S.,
                                                                                                                   ware verification, software engi-
    Parlato, G.: Mu-cseq 0.4: individual memory location unwindings.
                                                                                                                   neering, tool usability, taxonomies
    In: Chechik, M., Raskin, J.-F., (Eds.), In: Tools and algorithms
                                                                                                                   and open research data. She was
    for the construction and analysis of systems: 22nd international
                                                                                                                   one of the co-organisers of the
    conference, TACAS 2016 (pp. 938–941). Springer (2016)
                                                                                                                   first Alice & Eve workshop. She
83. Tomassetti, F., Zaytsev, V.: Reflections on the lack of adop-
                                                                                                                   is currently working at TNO on
    tion of domain specific languages. In: Burgueño, L., Kristensen,
                                                                                                                   the topic of semantic interoper-
    L.M. (Eds.), In: STAF Workshop proceedings (STAF) (Vol. 2707,
                                                                                                                   ability and knowledge graphs.
    pp. 85–94). CEUR-WS.org. (2020) http://ceur-ws.org/Vol-2707/
    oopslepaper5.pdf
84. Usman, M., Gopinath, D., Sun, Y., Noller, Y., Păsăreanu, C.S.:
    Nnrepair: constraint-based repair of neural network classifiers. In:                                           Yujie Liu received a Master’s
    Silva, A., Leino, K.R.M. (Eds.), In: Computer aided verification:                                              degree in Computer Science at
    33rd international conference, CAV 2021 (pp. 3–25). Springer                                                   the University of Twente in the
    (2021)                                                                                                         Netherlands, specialising in Soft-
85. van Dijk, T.: Oink: an implementation and evaluation of modern                                                 ware Technology. His is passion-
    parity game solvers. In: Beyer, D., Huisman, M. (Eds.), In: Proceed-                                           ate about GPGPU, mutation test-
    ings of the 24th international conference on tools and algorithms                                              ing, and the semantic web.
    for the construction and analysis of systems (TACAS) (Vol. 10805,
    pp. 291–308). Springer (2018)
86. Whittle, J., Ferrario, M.A., Simm, W., Hussain, W.: A case for
    human values in software engineering. IEEE Softw. 38(1), 106–
    113 (2021). https://doi.org/10.1109/MS.2019.2956701
87. Wiedijk, F.: Comparing mathematical provers. In: Asperti, A.
    Buchberger, B., Davenport, J.H. (Eds.), In: Proceedings of the
    second international conference on mathematical knowledge man-
    agement (MKM) (Vol. 2594, pp. 188–202). Springer (2003)
88. Wigderson, A.: Mathematics and computation: ideas revolution-                                                  Vadim Zaytsev is an Associate
    izing technology and science. Princeton University Press. (2019)                                               Professor of Software Evolution,
    https://www.math.ias.edu/avi/book                                                                              and an educational Programme
89. Winter, S., Timperley, C.S., Hermann, B., Cito, J., Bell, J., Hilton,                                          Director of Computer Science at
    M., Beyer, D.: A retrospective study of one decade of artifact eval-                                           the University of Twente. He is a
    uations. In: Proceedings of the 30th ACM joint European software                                               software language engineer doing
    engineering conference and symposium on the foundations of soft-                                               research in software analysis, mod-
    ware engineering (pp. 145–156). New York, NY, USA: Association                                                 elling and restructuring, often focus-
    for Computing Machinery (2022)                                                                                 ing on maintenance issues around
90. Wolf, F.A., Arquint, L., Clochard, M., Oortwijn, W., Pereira, J.C.,                                            legacy systems and languages.
    Müller, P.: Gobra: modular specification and verification of go pro-
    grams. In: Silva, A., Leino, K.R.M. (Eds.), In: Proceedings of
    the 33rd international conference on computer aided verification
    (CAV) (Vol. 12759, pp. 367–379). Springer (2021)




                                                                                                                                           123
