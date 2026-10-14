                                                                Towards a Common Framework for Autoformalization
                                                             Agnieszka Mensfelt∗ , David Tena Cucala∗ , Santiago Franco∗ ,
                                                        Angeliki Koutsoukou-Argyraki∗,† , Vince Trencsenyi∗ , Kostas Stathis∗
                                                         ∗
                                                           Department of Computer Science, Royal Holloway, University of London,
                                                                           Egham Hill, Egham, TW200EX, UK
                                                       †
                                                         Department of Computer Science and Technology, University of Cambridge,
                                                        William Gates Building, 15 JJ Thomson Avenue, Cambridge, CB3 0FD, UK
                                                 {agnieszka.mensfelt, david.tenacucala, santiago.francoaixela, angeliki.koutsoukouargyraki,
                                                                        vince.trencsenyi, kostas.stathis}@rhul.ac.uk
arXiv:2509.09810v3 [cs.AI] 15 Dec 2025




                                                                     Abstract                                abelle/HOL, Lean, Rocq, and Mizar, a field that has grown
                                                                                                             rapidly in recent years; there is increasing interest in em-
                                           Autoformalization has emerged as a term referring to the au-      ploying deep learning to automate the task of formaliza-
                                           tomation of formalization—specifically, the formalization of
                                           mathematics using interactive theorem provers (proof assis-
                                                                                                             tion (Wang, Kaliszyk, and Urban 2018; Szegedy 2020;
                                           tants). Its rapid development has been driven by progress         Wu et al. 2022; Jiang, Li, and Jamnik 2024). Earlier, pi-
                                           in deep learning, especially large language models (LLMs).        oneering work employing techniques from machine learn-
                                           More recently, the term has expanded beyond mathematics           ing had introduced the automation of the task of formal-
                                           to describe the broader task of translating informal input into   ization referring to it as “corpus-based translation between
                                           formal logical representations. At the same time, a growing       informal and formal mathematics” (Kaliszyk et al. 2014)
                                           body of research explores using LLMs to translate informal        and “parsing between aligned corpora”, exploring the chal-
                                           language into formal representations for reasoning, planning,     lenge: Is it possible to automatically parse informal math-
                                           and knowledge representation—often without explicitly re-         ematical texts into formal ones and formally verify them?
                                           ferring to this process as autoformalization. As a result, de-    (Kaliszyk, Urban, and Vyskočil 2015). Autoformalization
                                           spite addressing similar tasks, the largely independent devel-
                                           opment of these research areas has limited opportunities for
                                                                                                             is closely related to semantic parsing (Kaliszyk, Urban, and
                                           shared methodologies, benchmarks, and theoretical frame-          Vyskočil 2017) and can be seen as an instance of seman-
                                           works that could accelerate progress. The goal of this paper      tic parsing. The distinctive feature of autoformalization
                                           is to review—explicit or implicit—instances of what can be        would be that—unlike semantic parsing which encompasses
                                           considered autoformalization and to propose a unified frame-      a broad range of target formalisms including general pur-
                                           work, encouraging cross-pollination between different fields      pose programming languages—it is restricted to target for-
                                           to advance the development of next generation AI systems.         mal languages used in logical inference and automated rea-
                                                                                                             soning. Independently of this distinction, with the develop-
                                                                                                             ment of deep learning approaches to natural language pro-
                                                              1    Introduction                              cessing—particularly the emergence of transformer archi-
                                         Drawing on the long tradition of formalizing human rea-             tectures—the task of translating informal language into for-
                                         soning through mathematics and logic, AI pioneers (Mc-              mal representations is most often performed using large lan-
                                         Carthy 1960; Kowalski 1974; Newell and Simon 1976) in-              guage models (LLMs)1 . This approach is more general and
                                         corporated ideas from formal systems into functional and            flexible, and less tied to a specific target language or do-
                                         logical programming languages for formalizing knowledge             main than traditional semantic parsing methods; however, it
                                         and solving practical problems. Building on these founda-           comes at the cost of introducing new challenges in verifying
                                         tions, researchers in natural language processing (Weizen-          their less restricted outputs.
                                         baum 1966) and language understanding (Winograd 1972)                  Despite its growing use, current approaches to auto-
                                         began applying formal representations and inference tech-           formalization remain largely ad hoc, and there is no—
                                         niques to human language (Warren and Pereira 1982). This            outside the original sense of formalizing mathematics—
                                         enabled computers to reason about the meaning of sen-               widely agreed-upon definition of what the term encom-
                                         tences, answer questions, and interact with users in more           passes. This lack of clarity hinders communication across
                                         human-like ways, thus bridging the gap between symbolic             subfields of formal methods, proof engineering, and AI.
                                         AI and language understanding. These efforts opened the             Different communities may use the term to refer to sub-
                                         way in the development of semantic parsing (Kamath and              tly different tasks, or not explicitly consider their work to
                                         Das 2018), a field dedicated to translating natural language        constitute autoformalization, making it difficult to compare
                                         into formal meaning representations.
                                            The term Autoformalization was originally introduced to             1
                                                                                                                 The commonly used models include Claude, Codex,
                                         describe the automatic formalization of mathematics with            DeepSeek, GPT3.5, GPT4, Llemma, Minerva, Mistral,
                                         interactive theorem provers (proof assistants) such as Is-          and Mixtral.
methods, evaluate results, and transfer knowledge. Estab-           We categorized the reviewed papers into four broad sub-
lishing a clear, comprehensive, and widely accepted defini-      fields: formalization of mathematics using interactive theo-
tion would facilitate interdisciplinary collaboration and ac-    rem provers, logical inference and declarative programming,
celerate progress by enabling more systematic benchmark-         planning, and knowledge representation. These subfields
ing, evaluation, and knowledge sharing. To address these         were selected to reflect distinct research communities, each
issues, we propose a common framework for understanding          of which may conceptualize autoformalization differently
autoformalization.                                               and may have limited interaction or knowledge exchange
   An additional motivation is the potential role of auto-       with others. Nonetheless, the boundaries between these sub-
formalization in advancing the next generation of AI sys-        fields are not always clear-cut. On the one hand, there is
tems. Since the emergence of LLMs, there has been grow-          sometimes overlap between the categories (e.g., logical rea-
ing interest in using them as general-purpose reasoners.         soning can be used for knowledge representation); on the
However, despite their impressive versatility in natural lan-    other hand, additional categories may be warranted as the
guage processing, LLMs—trained primarily as next-token           field evolves.
predictors—hallucinate, producing outputs that are logically
inconsistent or factually incorrect. In response, “reason-
ing” models have been developed to address these shortcom-       Formalization of Mathematics with Interactive Theo-
ings by incorporating techniques such as chain-of-thought        rem Provers The term autoformalization originated in
prompting and reinforcement learning. While these models         the context of formalizing mathematics in 2018 (Wang,
show improved performance on certain benchmarks, they            Kaliszyk, and Urban 2018), and as a result, it is widely
still fall short in reliably performing complex logical in-      adopted within this domain. Since the recent emergence
ference (Shojaee et al. 2025) and remain costly to train.        of LLMs, users of proof assistants have been experiment-
Furthermore, reasoning in these models is often difficult        ing with using LLMs to assist with the formalization of
or impossible to verify formally, raising concerns about         mathematics, yielding mixed but potentially promising re-
their use in high-stakes applications (Nguyen et al. 2025).      sults (Karatarakis 2024). All 32 papers reviewed for a def-
In contrast, autoformalization leverages a task that large       inition from this subfield use the term autoformalization.
language models naturally excel at—translation—by map-           Most of works provide only informal definitions of auto-
ping informal language into formal representations. This         formalization, which may reflect the fact that formaliza-
offers a potentially more efficient and interpretable alter-     tion of mathematics is intuitively well understood within
native, or at least a complementary approach, to building        the community and does not require defining. These infor-
general-purpose LLM-based reasoners. By streamlining the         mal definitions typically describe autoformalization as the
interaction between language models and formal reasoning         task of automatically translating mathematical content from
tools, autoformalization could play a key role in enhancing      informal language into formal languages (Wu et al. 2022;
robustness and accuracy in domains such as mathematics,          Jiang et al. 2022; Agrawal et al. 2022; Li et al. 2024;
software verification, legal reasoning, and scientific discov-   Zhou et al. 2024; Ying et al. 2024; Yang et al. 2024;
ery—where logical reasoning is essential.                        Liu et al. 2025a; Lu et al. 2024; Poiroux et al. 2024b;
                                                                 Chan et al. 2025; Jiang 2025; Azerbayev et al. 2023;
 2    Review of Existing Usage and Definitions                   Wang et al. 2020; Yu et al. 2025; Poiroux et al. 2024a;
                                                                 Hu et al. 2025b; Wang et al. 2025a). Some authors also
To propose a unified cross-disciplinary framework, we sur-       explicitly include machine-verifiability of the output as part
veyed 81 research papers focused on the automatic transla-       of the definition (Szegedy 2020; Murphy et al. 2024; Liu et
tion of natural language into formal languages used for log-     al. 2024b; Liu et al. 2025c; Patel, Saha, and Flanigan 2023;
ical inference and automated reasoning. While we aimed           Cunningham, Bunescu, and Juedes 2023; Liu et al. 2025b;
to cover all relevant work in this area, we do not claim that    Weng et al. 2025; Lu et al. 2025; Jiang, Li, and Jamnik 2024;
the review is exhaustive. Our objective was not a detailed       Gadgil et al. 2022). Only one group of authors attempted a
review of the included papers, but rather to examine both        formal definition (Zhang, Quan, and Freitas 2024; Zhang,
formal and informal definitions of autoformalization and to      Valentino, and Freitas 2025).
identify tasks that can be interpreted as instances of auto-
formalization, even if the term itself was not explicitly em-
ployed.                                                          Logical Inference and Declarative Programming In this
   We included papers on autoformalization as the term has       category, we reviewed 30 papers. The target formalisms in-
been used since 2018, i.e., referring to the automatic trans-    clude first order logic (Pan et al. 2023; Lalwani et al. 2024;
lation of informal mathematics into “formal and verifiable       Han et al. 2022; Hahn et al. 2022; Yang, Ishay, and Lee
mathematical language” (Wang, Kaliszyk, and Urban 2018).         2023; Olausson et al. 2023; Chaturvedi and Asher 2024;
Furthermore, noting that the term autoformalization has be-      Thatikonda et al. 2024; Ryu et al. 2024; Quan et al. 2024;
gun to gain traction outside the context of mathematical for-    Brunello et al. 2025; Liu 2025; Lee et al. 2025); declara-
malization (Pan et al. 2023), we also included work on the       tive programming language, Prolog (Mensfelt, Stathis, and
translation of natural language into other languages that sup-   Trencsenyi 2024; Mensfelt, Stathis, and Trencsenyi 2025;
port formal verification, reasoning, or knowledge represen-      Borazjanizadeh and Piantadosi 2024) and answer set pro-
tation—such as Prolog, PDDL, or OWL—even if these are            gramming (ASP) (Li et al. 2025; Coppolillo et al. 2024;
not languages of interactive theorem provers.                    Borroto Santana, Kareem, and Ricca 2024; Ishay, Yang, and
Lee 2023). Another main line of work focuses on trans-            the works define the task informally (Oates et al. 2024;
lating problems from natural language into temporal log-          Liu et al. 2023; Aghzal et al. 2025; Smirnov et al. 2024;
ics such as LTL (Pnueli 1977) and CTL (Clarke, Emer-              Xie et al. 2023; Mahdavi et al. 2024; Huang and Zhang
son, and Sistla 1986). These languages extend classi-             2024; Hu et al. 2025a; Lin et al. 2023; Oswald et al. 2024;
cal logic with temporal operators to reason about proper-         Silver et al. 2024; Guan et al. 2023; Sikes et al. 2025;
ties that hold over time, with LTL describing linear se-          de la Rosa et al. 2024). In some cases the task may encom-
quences of states and CTL describing branching time struc-        pass generating both domain and problem files (Smirnov et
tures where multiple futures are possible from each state.        al. 2024), while in others only PDDL snippets are being in-
There exist a significant number of recent works focused          stantiated, e.g., goals in (Xie et al. 2023). A related but
on translating natural language descriptions to these lan-        separate line of research involves using LLMs as planners
guages (Chen et al. 2023; Pan, Chou, and Berenson 2023;           themselves, generating plans from PDDL inputs. This di-
William et al. 2024; Liu et al. 2024a; Mavrogiannis, Mavro-       rection falls outside the scope of the present work.
giannis, and Aloimonos 2024; Xu, Feng, and Miao 2024;
Li and Tian 2025; Soroco et al. 2025; Wang et al. 2025c;          Knowledge Representation Several works that we sur-
Wang et al. 2025b); one the reasons of popularity of tempo-       veyed (Mateiu and Groza 2023; Doumanas et al. 2024;
ral logics is its relevance in industrial applications.           Caufield et al. 2024; Saeedizade and Blomqvist 2024) fo-
   Only 8 of reviewed papers explicitly used the term             cus on translating natural language descriptions of real-
autoformalization, and all of them defined it infor-              world domains into ontologies using the Web Ontology Lan-
mally—typically as the translation of informal or natu-           guage (OWL) (OWL Working Group 2012), a formal lan-
ral language into formal representations (Pan et al. 2023;        guage used to define and share structured, machine-readable
Lalwani et al. 2024; Mensfelt, Stathis, and Trencsenyi 2024;      knowledge in terms of individuals, concepts, and relation-
Mensfelt, Stathis, and Trencsenyi 2025; Soroco et al. 2025;       ships between them. Some other works produce ontolo-
Olausson et al. 2023; Lee et al. 2025; Quan et al. 2024).         gies expressed in RDF or RDFS (Brickley and Guha 2014).
Among the remaining works, one paper formally defines the         RDF allows us to express Knowledge Graphs, where nodes
task (Liu et al. 2024a), while the rest describe it informally    represent named entities, node labels represent their in-
as translation from natural language into a specific formal-      dividual properties (called “types” or “classes”), and la-
ism. Notably, even though these papers do not use the term        belled edges represent relations between them. RDFS en-
autoformalization, their definitions are consistent with those    riches RDF with information about subsumption, domain,
that do.                                                          and range relations between classes. Both RDF and RDFS
                                                                  can be seen as subsets of OWL. Works such as (Eells et
                                                                  al. 2024; Abolhasani and Pan 2024) translate natural lan-
Planning The Planning Domain Definition Language                  guage to RDFS and RDF ontologies, respectively. Others
(PDDL) is the de facto standard formalism within the AI           express ontologies in ad-hoc languages (Tang et al. 2023;
planning community (Ghalab et al. 1998), encompassing             Lippolis et al. 2025), which seem to be expressible in OWL
various extensions ranging from basic STRIPS to first-order,      or RDFS. In all these works, syntactic validity is checked
probabilistic, and temporal logics (Fox and Long 2003).           automatically, and semantic is checked manually, or by run-
   A PDDL planning instance consists of a domain file and         ning certain conjunctive queries on the produced ontology.
a problem file. The domain file specifies predicates (facts)      None of the reviewed works in this category employs the
and actions applicable across the entire domain. Actions are      term autoformalization to denote the translation task.
defined through preconditions and effects, encapsulating a
labeled transition system that alters the truth values of a set
of facts. The problem file describes the particular instance,     Summary As observed, definitions across domains ex-
specifying the initial state and the goal conditions.             hibit notable similarities, even when the task is not explic-
                                                                  itly labelled as autoformalization. At the core, these tasks
   PDDL formally characterizes logical planning problems
                                                                  involve the automatic translation of natural language into
where the task is to generate a sequence of actions (a plan)
                                                                  a target language that supports logical inference and auto-
to transition from the initial to a goal state. Importantly,
                                                                  mated reasoning. Building on these shared foundations, we
PDDL is purely descriptive; it does not inherently provide
                                                                  now propose a unified conceptual framework that can en-
solutions. Therefore, planners like (Helmert 2006) are re-
                                                                  compass this broad class of tasks.
quired to compute plans. This separation allows LLMs to
effectively tackle complex combinatorial problems by trans-
lating them into PDDL representations, leveraging special-                       3   Proposed Definition
ized logic solvers and thus combining the strengths of LLMs       To define autoformalization, we begin by first establishing a
(natural language translation) and automated planning sys-        definition of formalization. Then, we demonstrate how se-
tems (combinatorial reasoning).                                   lected case studies—simple examples from various domains
   In the planning category, we included 16 papers. None          —align with this definition.
of them use the term “autoformalization”. One of the
works provides a formal definition of the task (Hu et al.         3.1   Definition of Autoformalization
2025a) as defining a mapping function generating a world          We introduce a general definition intended to capture the
model from a natural language description. The rest of            essential components of autoformalization across a broad
range of domains and settings, while abstracting away from       The choice of formal language Lf in a given autoformaliza-
implementation-specific or domain-specific details.              tion setting is guided by two considerations: first, it must
Definition 1. Formalization from informal language Li to         be capable of representing all relevant information in the
formal reasoning language Lf with respect to a semantic          domain-specific subset of Li ; second, it must support rea-
equivalence criterion E is the transformation of an expres-      soning in a way that allows properties of interest to be ver-
sion in a domain-specific subset of Li into a well-formed and    ified, both in terms of computational complexity and avail-
valid expression in Lf that is semantically equivalent ac-       ability of appropriate verification tools. For example, if our
cording to E. Autoformalization is formalization performed       goal is to formalise descriptions of planning scenarios, Lf
automatically by a computing system.                             might be a planning modeling language such as STRIPS.

   Our definition involves four parameters: the informal lan-
guage Li , a domain-specific subset of Li , the formal lan-      Semantic equivalence criterion The semantic equiva-
guage Lf , and the semantic equivalence criterion E. These       lence criterion E specifies what it means for the obtained
are treated as primitives without formal definition. However,    formal expression from Lf to preserve the intended mean-
we proceed to clarify their meanings, provide examples, and      ing of the informal input from Li . While the goal is for
explain our rationale for including them in the definition.      both expressions to ‘mean the same thing,’ formal languages
                                                                 are usually less expressive than informal languages and can-
                                                                 not capture every aspect of the original meaning. Hence, in
Informal language An informal language Li is a collec-           practice, E is designed to ensure that the formalization pre-
tion of meaningful expressions, such as the set of all gram-     serves the aspects of meaning that are most relevant for the
matically well-formed and semantically coherent texts in         task at hand. For example, in an interactive theorem prover,
English. This abstraction deliberately ignores more fine-        E may require that the formalization contains sufficient de-
grained aspects, such as lexical categories or compositional     tail to ensure that formalisations of correct proofs (expressed
syntax. Membership in informal languages is generally nei-       informally in Li ) can be verified by a given tool or reasoning
ther decidable nor computable, and their boundaries may be       algorithm.
vague or context-dependent. Sometimes we consider semi-             Specifying the semantic equivalence criterion can be chal-
formal languages: informal languages (like plain English)        lenging, as it requires defining conditions related to the
mixed with elements of a formal language. For example, the       meaning of informal language, which is inherently ambigu-
mathematical language of proofs is typically semi-formal.        ous. To address this, we introduce a related concept, the val-
   Our definitions refers to a domain-specific subset of Li      idation criterion V , which serves as a computable approxi-
because, in a given autoformalization setting, we typically      mation of E. This distinction is important: E defines what
do not seek to formalize all possible expressions in Li , but    it means for an informal and formal expression to “mean the
only a specific subset of interest that share a common con-      same thing” as a formal expression, whereas V provides a
ceptual framework or subject matter. For example, within         practical means of verifying whether a given pair of infor-
plain English, we may consider: descriptions of two-player       mal and formal expressions satisfies this equivalence.
games, specifications of procedural planning settings, and          We conclude this section with several observations that
natural language descriptions of real-world systems in terms     clarify and extend the scope of the definition.
of their objects, properties, and relations (i.e. informal on-   Remark 1. An informal expression in Li may be formal-
tologies), among many other examples.                            ized in two or more distinct ways into Lf which may differ
                                                                 in their choice of names, syntactic structure, or level of ab-
Formal reasoning language The formal reasoning lan-              straction. Conversely, two distinct informal expressions may
guage Lf is an enumerable set of expressions typically spec-     be formalized into the same expression in Lf ; this may hap-
ified by a grammar or formation rules, and is accompanied        pen, for example, if they describe the same state of affairs
by a formal semantics that assigns precise and unambiguous       according to the semantic equivalence criterion E, reflecting
meaning to each well-formed expression. It is also associ-       the inherent variability and redundancy of natural language.
ated with a reasoning apparatus—usually a set of inference       Remark 2. Systems for autoformalization need not be deter-
or transformation rules—that enables the derivation of new       ministic: the same informal input may be mapped to differ-
expressions from existing ones while preserving semantic         ent formal outputs in different runs. These outputs may or
properties. Examples of Lf include:                              may not be equivalent to one another, but each must satisfy
                                                                 the equivalence criterion E with respect to the input. In prac-
• languages of proof assistants, i.e., interactive theorem
                                                                 tice, it is often desirable for a system to prefer outputs that
  provers (e.g., Lean, Isabelle, Mizar, Rocq);
                                                                 are syntactically or structurally minimal, promoting concise-
• fully formal logics (e.g., propositional logic, FOL, LTL);     ness and efficiency.
• logic programming and declarative languages (e.g., An-         Remark 3. Although our definition is concerned with equiv-
  swer Set Programming, Prolog);                                 alence between complete informal and formal expressions,
                                                                 many applications require equivalence to hold at a finer
• planning and CSP languages (e.g., PDDL, MiniZinc)              granularity. For example, a multi-sentence informal descrip-
• knowledge representation languages and formalisms              tion of a mathematical argument may be formalized as a se-
  (e.g., OWL, RDF, Situation Calculus, Event Calculus).          quence of formal statements, each corresponding to a spe-
cific sentence or sub-argument. Such fine-grained corre-           2002) were used, which measure surface-level similarity be-
spondence should be subsumed within the semantic equiva-           tween the autoformalized statement and the ground truth
lence criterion E.                                                 (i.e. a manual formalization deemed correct by human ex-
                                                                   perts), but not direct semantic equivalence. The second vali-
3.2   Case Studies                                                 dation criterion was manual evaluation of selected examples.
To further illustrate the flexibility of our definition and its    While manual evaluation reliably assesses semantic equiva-
applicability across a range of settings, we next show how it      lence, it is costly and does not scale well. This highlights a
can be applied to capture existing examples in the literature.     fundamental challenge in autoformalization: automating the
The case study analysis will focus on what constitutes infor-      evaluation of semantic correspondence.
mal input, formal target language, and how semantic equiv-         First-Order Logic In (Pan et al. 2023) authors explicitly
alence is evaluated, while abstracting away from implemen-         state that their goal is to extend autoformalization into log-
tation details such as the application of in-context learning      ical reasoning. In the example from the paper, their rele-
and self-debugging feedback loops.                                 vant subset of natural language (Li ) consists of questions
Formalization of Mathematics with Interactive Theo-                about real-word objects and shapes. The target formal sys-
rem Provers The following example comes from a sem-                tem Lf is Prover9, which is based on first-order logic syntax
inal paper on autoformalization (Wu et al. 2022). In this          and a special signature of relevant predicates (e.g., Square,
example, the informal language Li is the natural mathe-            FourSided, Shape). The reasoning apparatus for this
matical language (plain English extended with mathemat-            language is instantiated by Prover9; it is a sound calculus
ical symbols) and the relevant subset can be considered            capable of verifying logical entailments within this formal
as a chosen set of mathematical problems (the example              system.
at hand coming from the 1987 International Mathematical               Consider the following example from the FOLIO bench-
Olympiad), with the target language Lf in this case being          mark:
that of Isabelle/HOL (Nipkow, Wenzel, and Paulson 2002).             Context: All squares have four sides. All four-sided
Isabelle/HOL is the most widely used instance of Isabelle,           things are shapes.
an interactive theorem prover for formal verification and            Question: Based on the above information, is the fol-
proof construction. Isabelle/HOL provides a higher-order             lowing statement true, false, or uncertain? All squares
logic theorem proving environment. In this context, Lf is            are shapes.
Isabelle’s structured proof language Isar that includes sym-         Options: A) True B) False C) Uncertain
bols such as keywords, mathematical symbols, and logical
operators, and has a formally defined syntax. The reason-             This informal input is translated into the following expres-
ing apparatus is realised by various automatic tools incor-        sion, consisting of three different sets of first-order logic for-
porated in Isabelle/HOL (and by a number of external au-           mulas:
tomatic theorem provers and satisfiability-modulo-theories           Predicates:
solvers which can be called by the Sledgehammer tool fea-            Square(x) — x is a square
tured by Isabelle/HOL (Blanchette et al. 2025)).                     FourSided(x) — x has four sides
   In our example (Wu et al. 2022), the input expression to          Shape(x) — x is a shape
be formalized in Li was as follows:
                                                                     Premises:
  Prove that there is no function f from the set of non-             ∀x(Square(x) → FourSided(x))
  negative integers into itself such that f (f (n)) = n +            ∀x(FourSided(x) → Shape(x))
  1987 for every n.
  The corresponding formalization in Isabelle/HOL pro-               Conclusion:
                                                                     ∀x(Square(x) → Shape(x))
duced by the Codex LLM tool was as follows:
  theorem                                                             Prover9 then verifies that the conclusion logically follows
  fixes f :: "nat \<Rightarrow> nat"                               from the premises via transitive implication. Hence, the sys-
  assumes "\<forall> n. f (f n) = n + 1987"                        tem formally determines that the correct answer is True (A).
  shows False                                                      In the paper, the semantic equivalence criterion E relies on
                                                                   all relevant properties of the objects described in the ques-
   The statement shows False indicates that the assump-
                                                                   tion being captured by the logical formulas, but wihtout in-
tion of the described function’s existence leads to a contra-
                                                                   troducing spurious properties. The validation criterion V
diction.
                                                                   used to measure semantic equivalence consisted in compar-
   The semantic equivalence criterion E in this case requires
                                                                   ing the answer derived from reasoning on the formalized
that all important mathematical details from the original the-
                                                                   problem to the ground truth correct answer. This approach
orem statement are captured in the formal statement. This is
                                                                   enables automated evaluation. However, reaching the cor-
crucial because when we later formalize a proof and verify
                                                                   rect answer does not necessarily guarantee semantic equiva-
its validity, all essential claims that the proof must establish
                                                                   lence.
need to be correctly represented in the theorem statement.
   Two validation criteria V were used here to evaluate se-        Logic Programming The next example involves formal-
mantic correctness. First, BLEU scores (Papineni et al.            izing strategic interactions that can be modelled as bima-
trix games in order to reason about them formally in Pro-        only to a narrow class of problems—bimatrix games—and
log (Mensfelt, Stathis, and Trencsenyi 2025). In this case,      requires manually implementing a validation procedure for
Lf is the set of valid Prolog programs. The semantics of         each class of games.
Prolog is well-defined and the reasoning apparatus relies on
logical inference; in this case, it is realised by the SWI-      Planning For planning we chose as an example the one
Prolog solver.                                                   used in (Oswald et al. 2024). In this case, the formal lan-
   In the following example, the relevant set of expressions     guage Lf consists of PDDL actions. PDDL is a formal lan-
involves description of game-like interactions, expressed in     guage for representing classical planning problems, where
natural language (Li ). The specific example involves the        states are described using first-order logic atoms, actions de-
classical Battle of the Sexes game:                              fine state transitions, and the goal is to find a sequence of
                                                                 actions that transforms the initial state into one satisfying
  A couple is deciding how to spend their evening to-            goal conditions. The syntactic framework of PDDL defines
  gether. One prefers to go to the opera and the other           the structure of predicates, object types, and action defini-
  prefers to go to a football game, but both prefer to be to-    tions with preconditions, and effects. For actions, the syntax
  gether rather than apart. If they both choose the opera,       consists of ‘(:action <action-name> ...)’, where action pa-
  the opera lover gets a payoff of 2 units of happiness,         rameters are defined, followed by the ‘:precondition’ (the
  and the football lover gets 1 unit. If they both choose        conditions that must hold before the action can be executed)
  the football game, the football lover gets 2 units of hap-     and the ‘:effect’ (the changes that result from executing the
  piness, and the opera lover gets 1 unit. If they choose        action). The formal reasoning apparatus for PDDL included
  different events, they both get 0 units of happiness.          the planners that interpret the generated PDDL domain and
   The formalization of this expression results produces a set   solve planning problems. Specifically, the planners used in
of domain-dependent predicates that, together with domain-       the paper include the K* planner (Lee, Katz, and Sohrabi
independent predicates, allow for reasoning about the inter-     2023) (part of the semantic verification checks the correct-
action. The snippet below, which is part of the formalization    ness of 100 alternative plans for each problem instance) for
output, shows the payoff matrix for the game and the subset      plan generation.
of predicates defining the initial state, legal moves and the       The example informal language input (Li ) is mostly nat-
effects of moves:                                                ural language, extended with symbols that represent names
                                                                 that must appear in the corresponding formal expression.
...                                                              Note that this is aided by adding a list of allowed predicates
payoffBOS(opera, opera, 2, 1).                                   to the informal action description prompt:
payoffBOS(football, football, 1, 2).
payoffBOS(opera, football, 0, 0).                                  Allowed Predicates:
payoffBOS(football, opera, 0, 0).
                                                                   (in-city ?loc - place ?city - city):a place loc is in a city.
initial(s0).                                                       (at ?obj - physobj ?loc - place) : a physical object obj
                                                                   is at a place loc.
initially(player(p1), s0).
initially(player(p2), s0).
                                                                   (in ?pkg - package ?veh - vehicle) : a package pkg is in
initially(role(p1, opera_lover), s0).                              a vehicle veh.
initially(role(p2, football_lover), s0).                           The action, “FLY-AIRPLANE” will fly an airplane
...                                                                from one airport to another. After the action, the air-
initial(s0).                                                       plane will be in the new location.
...
legal(select(P, opera), S):-                                        The output is a PDDL representation of the described ac-
    holds(player(P), S),                                         tion, where the given action’s preconditions and effects are
    holds(control(P), S).                                        formalized to model the planning domain:
...
effect(did(P, M), select(P, M), S).                              (:action FLY-AIRPLANE
...                                                                :parameters (?airplane - airplane
abnormal(control(P), select(P, M), S).                             ?loc-from - airport ?loc-to - airport)
...                                                                :precondition (at ?airplane ?loc-from)
                                                                   :effect (and(not(at ?airplane ?loc-from))
The semantic equivalence criterion refers to the correct for-           (at ?airplane ?loc-to)) )
malization of game rules and parameters (i.e., payoffs), such
that player 1 selecting opera and player 2 selecting football       As with logical entailment in first-order logic, planning
should result in payoffs of (0,0) when we query the gen-         also requires a notion of semantic equivalence. However,
erated formalization. The verification V of the semantic         domain equivalence in planning involves action behaviour
equivalence criterion is automated by querying all possible      as well as purely logical consequence. To evaluate approxi-
combinations of actions and comparing the resulting payoffs      mate semantic alignment, the authors use a heuristic domain
to ground-truth payoffs for each pair of actions.                equivalence test. For a reconstructed domain Do ′ generated
   This method of evaluation is both automated and guar-         by replacing an action a in the original domain Do , plan-
antees practical semantic equivalence. However, it applies       based reasoning is used to determine equivalence:
• Let Π be a planning problem solvable under Do , and Π′          and Lana are each other’s sisters:
  its analog using Do ′ . Let P and P ′ be subsets of valid
  plans generated from Π and Π′ , respectively.                      Declaration(ObjectProperty(:has sister))
                                                                          Declaration(NamedIndividual(:Anna))
• Each plan π ∈ P is checked for validity under Π′ ,
  and each π ′ ∈ P ′ is validated under Π, using the VAL                  Declaration(NamedIndividual(:Lana))
  tool (Howey, Long, and Fox 2004).                                    ObjPropAssert(:has sister :Anna :Lana)
• If all cross-validations succeed, then Semantics(L′f ) ≈             ObjPropAssert(:has sister :Lana :Anna)
  Semantics(Lf ), and the output action is deemed to be se-         The first statement identifies the role (binary predicate)
  mantically equivalent in terms of planning behaviour.           has sister and named individuals Anna and Lana.
  This procedure defines a relaxed but practical notion of        Then it generates two additional assertions to represent the
equivalence suitable for evaluating model outputs in sym-         symmetry implied in the sentence.
bolic planning systems. As with logical reasoning, selecting         In this setting, the semantic equivalence criterion E re-
a formally well-structured action that “looks right” is not       quires that all relational information in the informal descrip-
sufficient: only through validation methods like this can the     tion be correctly captured in the OWL ontology. In prac-
semantic faithfulness of the model’s output be determined.        tice, this cannot be formally measured, so the paper estab-
Knowledge Representation One approach to formaliz-                lishes a validation criterion V based on ontology engineers
ing domain knowledge involves translating natural language        manually verifying that the ontology encodes all relevant
(NL) statements into OWL axioms. (Mateiu and Groza                knowledge. In general, however, such manual V can be
2023) demonstrate how fine-tuned large language models            supplemented with an automated component: assuming the
can facilitate this translation by converting concise declar-     informal knowledge is consistent—as is usually the case—
ative sentences into OWL axioms—expressed in Functional           automated reasoning tools can check consistency of the for-
Syntax, one of several equivalent styles to write OWL ax-         malization. Furthermore, when the expected consequences
ioms. Their system uses a GPT-3 model trained on a dataset        and undesirable outcomes of the knowledge base are known
of 150 prompt–response pairs. The training data covers var-       and have admissible formalizations, ontology reasoners such
ious ontology constructs, including class declarations, sub-      as Hermit (Glimm et al. 2014) can be used to verify formally
class hierarchies, object properties, cardinality restrictions,   that the ontology both entails all intended consequences and
and disjointness.                                                 avoiding unintended ones.
   The Web Ontology Language (OWL) is a formalism used
to model knowledge about a domain in terms of named indi-                4    Challenges and Open Problems
viduals, their individual properties (called concept names or     While there is a growing body of work aimed at advancing
classes), and the binary relationships between them (called       autoformalization (Patel, Saha, and Flanigan 2023; Zhang,
roles or object properties). OWL includes logical construc-       Quan, and Freitas 2024; Li et al. 2024; Tarrach et al. 2024;
tors that allow the definition of complex concepts and role       Chan et al. 2025; Jiang, Li, and Jamnik 2024; Lu et al. 2025;
expressions from simpler ones. The formal language Lf             Poiroux et al. 2024b; Liu et al. 2025b), several fundamen-
in this setting is the set of OWL ontologies: a set of logi-      tal challenges still offer exciting research opportunities that
cal assertions, typically divided into three categories: TBox     will shape the field’s future development. We next provide a
assertions, which express general class relationships such        selective overview of these challenges and opportunities.
as subclassing or equivalence; ABox assertions, which de-
scribe facts about individual instances; and RBox assertions,     Semantic Verification The key challenge in autoformal-
which define properties of roles, such as transitivity or sym-    ization remains verifying equivalence of the informal lan-
metry. They often include also optional declaration state-        guage and the formal representation. Current approaches
ments (which can be inferred). Key reasoning tasks include        rely mostly on human supervision, either through direct as-
consistency checking (determining whether the ontology ad-        sessment or comparison with reference solutions; this is
mits a model) and classification (computing the taxonomy of       sometimes enhanced with automated checks such as con-
concept names).                                                   sistency checking of the extracted formalism. Fully formal
   In this setting, the semantic equivalence criterion requires   and automated verification of semantic equivalence, how-
that all information described in the informal description is     ever, appears impossible even in principle, since natural lan-
correctly captured by the ontology. The verification is of-       guage and its intended meaning are inherently informal.
ten established informally by ontology engineers, who man-           An open question is whether it is possible to train in-
ually verify that the ontologies capture all relevant knowl-      telligent systems to acquire the dual competence that hu-
edge. However, reasoning tools play a crucial role in this        mans possess: understanding both formal and informal do-
process by checking for consistency and ensuring that the         mains, and being able to assess correspondence between
ontology entails all expected consequences while avoiding         them. Such verification capabilities are in principle dis-
unintended ones. Ontology development is often an itera-          tinct from the current practice of autoformalization, but they
tive process, alternating addition of axioms and reasoning to     could be integrated directly into the autoformalization pro-
assess their impact.                                              cess rather than applied post-hoc. Although formally un-
   To illustrate the approach of (Mateiu and Groza 2023), we      verifiable, using meta-level reasoning to relate formal and
recapitulate the output of their system on the sentence Anna      informal representations could significantly reduce supervi-
sion and move us closer to automated human-level semantic          system from pursuing incorrect interpretations too far before
verification.                                                      correction.
Target Formal Languages Another challenge in autofor-              Cross-Domain Transfer and Generalization As we have
malization is selecting an appropriate target formal language      shown in this paper, current autoformalization approaches
for the required task. This choice depends critically on the       are often domain-specific, with systems designed separately
intended use case: who will interact with the formalized text,     for areas such as mathematical reasoning, planning, logic,
and what computational tasks will be performed with it? For        etc. A major challenge is developing methods that can trans-
instance, if the goal is interactive theorem proving, the avail-   fer reasoning patterns and formalization strategies across
ability and sophistication of verification tools as well as the    these different areas. Our present analysis of the notion of
contents of formal proof libraries become critical. On the         autoformalization shows that the underlying formal struc-
other hand, if human mathematicians will work with the             tures and reasoning patterns in these areas often share com-
output, considerations of readability and established com-         monalities that could be exploited for more general autofor-
munity conventions become essential.                               malization systems.
   The selection process must also balance expressiveness             This, however, is still a big open challenge that requires a
against computational tractability. The target language must       more systematic understanding of the structural similarities
be sufficiently expressive to capture all the relevant semantic    in the way autoformalization is used across fields. Success
content of the natural language text. However, there exists a      in this area would enable more robust and widely applica-
fundamental tension between expressive power and compu-            ble autoformalization tools that could adapt to new domains
tational complexity of verification, potentially making auto-      with minimal additional training. We envision our current
mated reasoning and verification very difficult or even un-        work, which establishes a common framework for the defi-
decidable. Given these constraints, an open problem is ex-         nition of autoformalization, as a first step in that direction.
ploring the development of new formal languages designed
specifically for autoformalization, which might offer better                            5    Conclusions
balance points in the expressiveness-tractability spectrum.
                                                                   In practice, we judge successful formalization by its fruits:
Scalability and Integration with Mathematical Practice             Does it help us solve problems? Does it support verifica-
Current autoformalization systems work well on curated             tion? Does it reveal new connections? Does it eliminate
benchmarks but often fail to scale to real-world practice.         disputes? Does it enable computation? Formalization is less
For example, in the context of mathematical proof, the lit-        about focusing on mere translation and more about creating
erature is dominated by incomplete proofs, informal reason-        tools that extend our and AI systems’ reasoning capabilities
ing steps, and proof sketches, and so their formalization re-      in useful ways.
quires contextual understanding and gap-filling, capabilities         One of the most promising applications is enhancing the
that current systems struggle with, particularly in specialized    capabilities of LLMs, developing robust general-purpose
mathematical fields.                                               reasoners, and, as one of the consequences, enhancing the
   This scalability gap reflects a deeper uncertainty about        safety of agentic AI. However, achieving this through auto-
how autoformalization tools should integrate into research         formalization presents many challenges. A common frame-
workflows. Without clarity on whether autoformalization            work could accelerate progress by facilitating knowledge ex-
should assist proof development, literature review, verifica-      change between different fields and enabling transfer learn-
tion, hypothesis testing, or enhancing the reliability of AI       ing.
systems, we risk building systems that are technical achieve-         As we have demonstrated, translating problems into dif-
ments but remain peripheral to the work of intended users.         ferent formalisms for logical inference and automated rea-
                                                                   soning shares similarities and common challenges. Based
Interactive Formalization Many of the current autofor-
                                                                   on the reviewed papers, we propose a preliminary definition
malization approaches treat the task as a one-shot transla-
                                                                   that encompasses various types of formalisms. This defini-
tion problem, attempting to convert natural language text di-
                                                                   tion is not intended to be definitive; rather, our aim is to ini-
rectly into formal representations. As we have already dis-
                                                                   tiate a cross-disciplinary dialogue on how best to conceptu-
cussed, this paradigm struggles with the inherent ambigu-
                                                                   alize autoformalization, articulate its desired properties, and
ity and context-dependence of natural or mathematical lan-
                                                                   promote effective interdisciplinary collaboration.
guage. A more promising direction—and an approach to the
problem of semantic verification—involves systems that can
engage in dialogue with users, asking clarifying questions                            Acknowledgments
about ambiguous terms, implicit assumptions, or intended           This work was supported by a Leverhulme Trust Interna-
interpretations.                                                   tional Professorship Grant (LIP-2022-001).
   Such interactive systems would require significant ad-
vances in both natural language understanding and theorem
prover interfaces. The system should recognise when clari-
                                                                                            References
fication is needed and formulate meaningful questions to the       Abolhasani, M. S., and Pan, R. 2024. Leveraging LLM for
user, which then would be incorporated to iteratively refine       automated ontology extraction and knowledge graph gener-
the formalization. Early feedback would also prevent the           ation. CoRR abs/2412.00608.
Aghzal, M.; Plaku, E.; Stein, G. J.; and Yao, Z. 2025. A          Cunningham, G.; Bunescu, R. C.; and Juedes, D. 2023.
Survey on Large Language Models for Automated Planning.           Towards Autoformalization of Mathematics and Code Cor-
Agrawal, A.; Gadgil, S.; Goyal, N.; Narayanan, A.; and            rectness: Experiments with Elementary Proofs.
Tadipatri, A. 2022. Towards a Mathematics Formalisation           de la Rosa, T.; Gopalakrishnan, S.; Pozanco, A.; Zeng, Z.;
Assistant using Large Language Models. arXiv:2211.07524.          and Borrajo, D. 2024. TRIP-PAL: Travel Planning with
Azerbayev, Z.; Piotrowski, B.; Schoelkopf, H.; Ayers, E. W.;      Guarantees by Combining Large Language Models and Au-
Radev, D.; and Avigad, J. 2023. ProofNet: Autoformalizing         tomated Planners.
and Formally Proving Undergraduate-Level Mathematics.             Doumanas, D.; Soularidis, A.; Kotis, K.; and Vouros, G. A.
Blanchette, J.; Desharnais, M.; Paulson, L. C.; and Bartl,        2024. Integrating llms in the engineering of a SAR ontology.
L. 2025. Hammering Away A User’s Guide to Sledge-                 In Maglogiannis, I.; Iliadis, L. S.; MacIntyre, J.; Avlonitis,
hammer for Isabelle/HOL. https://isabelle.in.tum.de/dist/         M.; and Papaleonidas, A., eds., Artificial Intelligence Ap-
Isabelle2025/doc/sledgehammer.pdf: tutorial.                      plications and Innovations - 20th IFIP WG 12.5 Interna-
Borazjanizadeh, N., and Piantadosi, S. T. 2024. Reli-             tional Conference, AIAI 2024, Corfu, Greece, June 27-30,
able reasoning beyond natural language. arXiv preprint            2024, Proceedings, Part IV, volume 714 of IFIP Advances
arXiv:2407.11373.                                                 in Information and Communication Technology, 360–374.
Borroto Santana, M.; Kareem, I.; and Ricca, F. 2024. To-          Springer.
wards automatic composition of asp programs from nat-             Eells, A.; Dave, B.; Hitzler, P.; and Shimizu, C. 2024.
ural language specifications. Proceedings of the Thirty-          Commonsense ontology micropatterns. In Besold, T. R.;
Third International Joint Conference on Artificial Intelli-       d’Avila Garcez, A.; Jiménez-Ruiz, E.; Confalonieri, R.;
gence (IJCAI-24).                                                 Madhyastha, P.; and Wagner, B., eds., Neural-Symbolic
Brickley, D., and Guha, R. V. 2014. Rdf schema 1.1. https:        Learning and Reasoning - 18th International Conference,
//www.w3.org/TR/rdf-schema/. W3C Recommendation.                  NeSy 2024, Barcelona, Spain, September 9-12, 2024, Pro-
                                                                  ceedings, Part II, volume 14980 of Lecture Notes in Com-
Brunello, A.; Ferrarese, R.; Geatti, L.; Marzano, E.; Mon-
                                                                  puter Science, 51–59. Springer.
tanari, A.; and Saccomanno, N. 2025. Evaluating llms ca-
pabilities at natural language to logic translation: A prelim-    Fox, M., and Long, D. 2003. Pddl2. 1: An extension to
inary investigation. In Proceedings of the Logic and Engi-        pddl for expressing temporal planning domains. Journal of
neering of Natural Language Semantics (LENLS) Workshop            artificial intelligence research 20:61–124.
2025.                                                             Gadgil, S.; Tadipatri, A. R.; Agrawal, A.; Narayanan, A.;
Caufield, J. H.; Hegde, H.; Emonet, V.; Harris, N. L.;            and Goyal, N. 2022. Towards automating formalisation
Joachimiak, M. P.; Matentzoglu, N.; Kim, H.; Moxon, S.            of theorem statements using large language models. In
A. T.; Reese, J. T.; Haendel, M. A.; Robinson, P. N.; and         36th Conference on Neural Information Processing Systems
Mungall, C. J. 2024. Structured prompt interrogation and          (NeurIPS 2022) Workshop on MATH-AI.
recursive extraction of semantics (SPIRES): a method for
populating knowledge bases using zero-shot learning. Bioin-       Ghalab, M.; Howe, A.; Knoblock, C.; McDermott, I. D.;
form. 40(3).                                                      Ram, A.; Veloso, M.; Weld, D.; Sri, D. W.; Barrett, A.;
                                                                  Christianson, D.; et al. 1998. Pddl—the planning domain
Chan, W.; Souliman, M.; Nordhagen, J.; Miranda, B.; Ob-           definition language. IPC-98 Technical Report.
bad, E.; and Koyejo, K. F. S. 2025. Lean-ing on Quality:
How High-Quality Data Beats Diverse Multilingual Data in          Glimm, B.; Horrocks, I.; Motik, B.; Stoilos, G.; and Wang,
AutoFormalization.                                                Z. 2014. Hermit: An owl 2 reasoner. Journal of Autom.
                                                                  Reason. 53(3):245–269.
Chaturvedi, A., and Asher, N. 2024. Learning semantic
structure through first-order-logic translation. arXiv preprint   Guan, L.; Valmeekam, K.; Sreedharan, S.; and Kambham-
arXiv:2410.03203.                                                 pati, S. 2023. Leveraging pre-trained large language models
Chen, Y.; Gandhi, R.; Zhang, Y.; and Fan, C. 2023. Nl2tl:         to construct and utilize world models for model-based task
Transforming natural languages to temporal logics using           planning. Advances in Neural Information Processing Sys-
large language models. In Proceedings of the 2023 Confer-         tems 36:79081–79094.
ence on Empirical Methods in Natural Language Process-            Hahn, C.; Schmitt, F.; Tillman, J. J.; Metzger, N.; Siber,
ing, 15880–15903.                                                 J.; and Finkbeiner, B. 2022. Formal Specifications from
Clarke, E. M.; Emerson, E. A.; and Sistla, A. P. 1986. Au-        Natural Language.
tomatic verification of finite-state concurrent systems using     Han, S.; Schoelkopf, H.; Zhao, Y.; Qi, Z.; Riddell, M.; Zhou,
temporal logic specifications. ACM Transactions on Pro-           W.; Coady, J.; Peng, D.; Qiao, Y.; Benson, L.; Sun, L.;
gramming Languages and Systems 8(2):244–263.                      Wardle-Solano, A.; Szabo, H.; Zubova, E.; Burtell, M.; Fan,
Coppolillo, E.; Calimeri, F.; Manco, G.; Perri, S.; and Ricca,    J.; Liu, Y.; Wong, B.; Sailor, M.; Ni, A.; Nan, L.; Kasai, J.;
F. 2024. Llasp: Fine-tuning large language models for             Yu, T.; Zhang, R.; Fabbri, A. R.; Kryscinski, W.; Yavuz, S.;
answer set programming. Proceedings of the 21st Interna-          Liu, Y.; Lin, X. V.; Joty, S.; Zhou, Y.; Xiong, C.; Ying, R.;
tional Conference on Principles of Knowledge Representa-          Cohan, A.; and Radev, D. 2022. FOLIO: Natural Language
tion and Reasoning.                                               Reasoning with First-Order Logic.
Helmert, M. 2006. The fast downward planning system.               Lee, J.; Lee, D.; Choi, C.; Im, Y.; Wi, J.; Heo, K.; Oh, S.;
Journal of Artificial Intelligence Research 26:191–246.            Lee, S.; and Shin, I. 2025. Safeguarding Mobile GUI Agent
Howey, R.; Long, D.; and Fox, M. 2004. Val: Automatic              via Logic-based Action Verification.
plan validation, continuous effects and mixed-initiative           Lee, J.; Katz, M.; and Sohrabi, S. 2023. On k* search for
planning using pddl. In 16th IEEE International Conference         top-k planning. In Proceedings of the International Sympo-
on Tools with Artificial Intelligence (ICTAI).                     sium on Combinatorial Search, volume 16, 38–46.
Hu, M.; Chen, T.; Zou, Y.; Lei, Y.; Chen, Q.; Li, M.; Mu,          Li, J., and Tian, M. T. 2025. Automatic generation
Y.; Zhang, H.; Shao, W.; and Luo, P. 2025a. Text2World:            of safety-compliant linear temporal logic via large lan-
Benchmarking Large Language Models for Symbolic World              guage model: A self-supervised framework. arXiv preprint
Model Generation.                                                  arXiv:2503.15840.
Hu, X.; Zhou, Q.; Grechuk, B.; and Tyukin, I. Y. 2025b.            Li, Z.; Wu, Y.; Li, Z.; Wei, X.; Zhang, X.; Yang, F.; and
Stepproof: Step-by-step verification of natural language           Ma, X. 2024. Autoformalize Mathematical Statements by
mathematical proofs. arXiv preprint arXiv:2506.10558.              Symbolic Equivalence and Semantic Consistency.
Huang, C., and Zhang, L. 2024. On the Limit of Language            Li, N.; Liu, P.; Liu, Z.; Dai, T.; Jiang, Y.; and Xia, S.-T.
Models as Planning Formalizers.                                    2025. Logic-of-thought: Empowering large language mod-
                                                                   els with logic programs for solving puzzles in natural lan-
Ishay, A.; Yang, Z.; and Lee, J. 2023. Leveraging large            guage. arXiv preprint arXiv:2505.16114.
language models to generate answer set programs. Proceed-
ings of the 20th International Conference on Principles of         Lin, K.; Agia, C.; Migimatsu, T.; Pavone, M.; and Bohg, J.
Knowledge Representation and Reasoning.                            2023. Text2Motion: from natural language instructions to
                                                                   feasible plans. Autonomous Robots 47(8):1345–1365.
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Li, W.; Liu, J.; Jamnik,
                                                                   Lippolis, A. S.; Saeedizade, M. J.; Keskisärkkä, R.; Zup-
M.; Lacroix, T.; Wu, Y.; and Lample, G. 2022. Draft, sketch,
                                                                   piroli, S.; Ceriani, M.; Gangemi, A.; Blomqvist, E.; and
and prove: Guiding formal theorem provers with informal
                                                                   Nuzzolese, A. G. 2025. Ontology generation using large
proofs. arXiv preprint arXiv:2210.12283.
                                                                   language models. In Curry, E.; Acosta, M.; Poveda-Villalón,
Jiang, A. Q.; Li, W.; and Jamnik, M. 2024. Multi-language          M.; van Erp, M.; Ojo, A. K.; Hose, K.; Shimizu, C.; and
diversity benefits autoformalization. Advances in Neural In-       Lisena, P., eds., The Semantic Web - 22nd European Seman-
formation Processing Systems 37:83600–83626.                       tic Web Conference, ESWC 2025, Portoroz, Slovenia, June
Jiang, Q. 2025. Language models for verifiable mathemati-          1-5, 2025, Proceedings, Part I, volume 15718 of Lecture
cal automation: Interaction, integration, and autoformaliza-       Notes in Computer Science, 321–341. Springer.
tion.                                                              Liu, B.; Jiang, Y.; Zhang, X.; Liu, Q.; Zhang, S.; Biswas, J.;
Kaliszyk, C.; Urban, J.; Vyskočil, J.; and Geuvers, H. 2014.      and Stone, P. 2023. LLM+P: Empowering Large Language
Developing corpus-based translation methods between in-            Models with Optimal Planning Proficiency.
formal and formal mathematics: Project description. In In-         Liu, J. X.; Shah, A.; Konidaris, G.; Tellex, S.; and
ternational Conference on Intelligent Computer Mathemat-           Paulius, D. 2024a. Lang2LTL-2: Grounding Spatiotemporal
ics, 435–439. Springer.                                            Navigation Commands Using Large Language and Vision-
Kaliszyk, C.; Urban, J.; and Vyskočil, J. 2015. Learning          Language Models. In 2024 IEEE/RSJ International Confer-
to parse on aligned corpora (rough diamond). In Interactive        ence on Intelligent Robots and Systems (IROS), 2325–2332.
Theorem Proving: 6th International Conference, ITP 2015,           ISSN: 2153-0866.
Nanjing, China, August 24-27, 2015, Proceedings 6, 227–            Liu, Q.; Zheng, X.; Lu, X.; Cao, Q.; and Yan, J. 2024b.
233. Springer.                                                     Rethinking and Improving Autoformalization: Towards a
Kaliszyk, C.; Urban, J.; and Vyskočil, J. 2017. Automating        Faithful Metric and a Dependency Retrieval-based Ap-
formalization by statistical and semantic parsing of mathe-        proach. In Proceedings of The Thirteenth International Con-
matics. In International Conference on Interactive Theorem         ference on Learning Representations.
Proving, 12–27. Springer.                                          Liu, C.; Yuan, Y.; Yin, Y.; Xu, Y.; Xu, X.; Chen, Z.; Wang,
                                                                   Y.; Shang, L.; Liu, Q.; and Zhang, M. 2025a. Safe: Enhanc-
Kamath, A., and Das, R. 2018. A survey on semantic pars-
                                                                   ing mathematical reasoning in large language models via
ing. arXiv preprint arXiv:1812.00978.
                                                                   retrospective step-aware formal verification. arXiv preprint
Karatarakis, M. 2024. Leveraging large language models for         arXiv:2506.04592.
autoformalizing theorems: A case study. In 9th Conference          Liu, Q.; Zheng, X.; Lu, X.; Cao, Q.; and Yan, J. 2025b. Re-
on Artificial Intelligence and Theorem Proving (AITP).             thinking and improving autoformalization: Towards a faith-
Kowalski, R. 1974. Predicate logic as a programming lan-           ful metric and a dependency retrieval-based approach. In
guage. In IFIP Congress, 569–574.                                  The Thirteenth International Conference on Learning Rep-
Lalwani, A.; Kim, T.; Chopra, L.; Hahn, C.; Jin, Z.; and           resentations (ICLR). Spotlight paper.
Sachan, M. 2024. Autoformalizing Natural Language to               Liu, X.; Bao, K.; Zhang, J.; Liu, Y.; Chen, Y.; Liu, Y.; Jiao,
First-Order Logic: A Case Study in Logical Fallacy Detec-          Y.; and Luo, T. 2025c. ATLAS: Autoformalizing Theorems
tion.                                                              through Lifting, Augmentation, and Synthesis of Data.
Liu, J. 2025. Few-shot natural language to first-order logic     Language Models with First-Order Logic Provers. In Pro-
translation via in-context learning. In Proceedings of the       ceedings of the 2023 Conference on Empirical Methods in
2025 Conference of the Nations of the Americas Chapter           Natural Language Processing, 5153–5176. Singapore: As-
of the Association for Computational Linguistics: Human          sociation for Computational Linguistics.
Language Technologies (Volume 1: Long Papers), 10939–            Oswald, J.; Srinivas, K.; Kokel, H.; Lee, J.; Katz, M.; and
10960.                                                           Sohrabi, S. 2024. Large Language Models as Planning Do-
Lu, J.; Wan, Y.; Liu, Z.; Huang, Y.; Xiong, J.; Liu, C.; Shen,   main Generators. Proceedings of the International Confer-
J.; Jin, H.; Zhang, J.; Wang, H.; Yang, Z.; Tang, J.; and Guo,   ence on Automated Planning and Scheduling 34:423–431.
Z. 2024. Process-Driven Autoformalization in Lean 4.             OWL Working Group. 2012. Owl 2 web ontology language
Lu, J.; Wan, Y.; Huang, Y.; Xiong, J.; Liu, Z.; and Guo,         document overview (second edition). W3c recommendation,
Z. 2025. Formalalign: Automated alignment evaluation for         World Wide Web Consortium (W3C). Accessed: 2025-07-
autoformalization. In The Thirteenth International Confer-       28.
ence on Learning Representations (ICLR). Preprint accepted
                                                                 Pan, L.; Albalak, A.; Wang, X.; and Wang, W. Y. 2023.
to ICLR 2025.
                                                                 Logic-LM: Empowering large language models with sym-
Mahdavi, S.; Aoki, R.; Tang, K.; and Cao, Y. 2024. Lever-        bolic solvers for faithful logical reasoning. In The 2023 Con-
aging Environment Interaction for Automated PDDL Trans-          ference on Empirical Methods in Natural Language Pro-
lation and Planning with Large Language Models.                  cessing.
Mateiu, P., and Groza, A. 2023. Ontology engineering with        Pan, J.; Chou, G.; and Berenson, D. 2023. Data-efficient
large language models. In 25th International Symposium           learning of natural language to linear temporal logic trans-
on Symbolic and Numeric Algorithms for Scientific Comput-        lators for robot task specification. Proceedings of the 2023
ing, SYNASC 2023, Nancy, France, September 11-14, 2023,          IEEE International Conference on Robotics and Automation
226–229. IEEE.                                                   (ICRA).
Mavrogiannis, A.; Mavrogiannis, C.; and Aloimonos, Y.
                                                                 Papineni, K.; Roukos, S.; Ward, T.; and Zhu, W.-J. 2002.
2024. Cook2LTL: Translating Cooking Recipes to LTL For-
                                                                 Bleu: a method for automatic evaluation of machine trans-
mulae using Large Language Models. In 2024 IEEE Inter-
                                                                 lation. In Proceedings of the 40th annual meeting of the
national Conference on Robotics and Automation (ICRA),
                                                                 Association for Computational Linguistics, 311–318.
17679–17686.
McCarthy, J. 1960. Programs with common sense. Techni-           Patel, N.; Saha, R.; and Flanigan, J. 2023. A New Approach
cal report, USA.                                                 Towards Autoformalization.
Mensfelt, A.; Stathis, K.; and Trencsenyi, V. 2024. Autofor-     Pnueli, A. 1977. The temporal logic of programs. 18th An-
malization of game descriptions using large language mod-        nual Symposium on Foundations of Computer Science 46–
els.                                                             57.
Mensfelt, A.; Stathis, K.; and Trencsenyi, V. 2025. Gener-       Poiroux, A.; Weiss, G.; Kunčak, V.; and Bosselut, A. 2024a.
ative agents for multi-agent autoformalization of interaction    Improving autoformalization using type checking. arXiv
scenarios. Accepted at European Conference on Artificial         preprint arXiv:2406.07222.
Intelligence (ECAI) 2025.                                        Poiroux, A.; Weiss, G.; Kunčak, V.; and Bosselut, A. 2024b.
Murphy, L.; Yang, K.; Sun, J.; Li, Z.; Anandkumar, A.; and       Improving Autoformalization using Type Checking.
Si, X. 2024. Autoformalizing Euclidean Geometry.                 Quan, X.; Valentino, M.; Dennis, L. A.; and Freitas, A.
Newell, A., and Simon, H. A. 1976. Computer science as           2024. Verification and Refinement of Natural Language Ex-
empirical inquiry: Symbols and search. Communications of         planations through LLM-Symbolic Theorem Proving.
the ACM 19(3):113–126.                                           Ryu, H.; Kim, G.; Lee, H. S.; and Yang, E. 2024. Divide
Nguyen, H. T.; Fungwacharakorn, W.; Zin, M. M.; Goebel,          and Translate: Compositional First-Order Logic Translation
R.; Toni, F.; Stathis, K.; and Satoh, K. 2025. LLMs for le-      and Verification for Complex Logical Reasoning.
gal reasoning: A unified framework and future perspectives.      Saeedizade, M. J., and Blomqvist, E. 2024. Navigating on-
Computer Law & Security Review 58:106165.                        tology development with large language models. In Meroño-
Nipkow, T.; Wenzel, M.; and Paulson, L. C. 2002.                 Peñuela, A.; Dimou, A.; Troncy, R.; Hartig, O.; Acosta, M.;
Isabelle/HOL: a proof assistant for higher-order logic.          Alam, M.; Paulheim, H.; and Lisena, P., eds., The Semantic
Springer.                                                        Web - 21st International Conference, ESWC 2024, Hersonis-
Oates, T.; Alford, R.; Johnson, S.; and Hall, C. 2024. Us-       sos, Crete, Greece, May 26-30, 2024, Proceedings, Part I,
ing large language models to extract planning knowledge          volume 14664 of Lecture Notes in Computer Science, 143–
from unstructured text. In Proceedings of the ICAPS Work-        161. Springer.
shop on Knowledge Engineering for Planning and Schedul-          Shojaee, P.; Mirzadeh, I.; Alizadeh, K.; Horton, M.; Ben-
ing (KEPS).                                                      gio, S.; and Farajtabar, M. 2025. The illusion of thinking:
Olausson, T.; Gu, A.; Lipkin, B.; Zhang, C.; Solar-Lezama,       Understanding the strengths and limitations of reasoning
A.; Tenenbaum, J.; and Levy, R. 2023. LINC: A Neu-               models via the lens of problem complexity. arXiv preprint
rosymbolic Approach for Logical Reasoning by Combining           arXiv:2506.06941.
Sikes, K.; Fine-Morris, M.; Sreedharan, S.; Smith, L. N.;        Warren, D. H., and Pereira, F. C. 1982. An efficient easily
and Roberts, M. 2025. Creating PDDL Models from                  adaptable system for interpreting natural language queries.
Javascript using LLMs: Preliminary Results. In AAAI 2025         American Journal of Computational Linguistics 8(3-4):110–
Workshop LM4Plan.                                                122.
Silver, T.; Dan, S.; Srinivas, K.; Tenenbaum, J. B.; Kael-       Weizenbaum, J. 1966. Eliza — a computer program for the
bling, L.; and Katz, M. 2024. Generalized Planning in            study of natural language communication between man and
PDDL Domains with Pretrained Large Language Models.              machine. Communications of the ACM 9(1):36–45.
Proceedings of the AAAI Conference on Artificial Intelli-        Weng, K.; Du, L.; Li, S.; Lu, W.; Sun, H.; Liu, H.; and
gence 38(18):20256–20264.                                        Zhang, T. 2025. Autoformalization in the era of large lan-
Smirnov, P.; Joublin, F.; Ceravola, A.; and Gienger, M.          guage models: A survey. arXiv preprint arXiv:2505.23486.
2024. Generating consistent PDDL domains with Large              William, M.; Nikolaus, H.; Koenig, N.; Leyi, C.; Rothkopf,
Language Models.                                                 R.; Qiao, F.; and Santolucito, M. 2024. Guiding llm tem-
Soroco, M.; Song, J.; Xia, M.; Emond, K.; Sun, W.; and           poral logic generation with explicit separation of data and
Chen, W. 2025. Pde-controller: Llms for autoformalization        control. arXiv preprint arXiv:2406.07400.
and reasoning of pdes. arXiv preprint arXiv:2502.00963.          Winograd, T. 1972. Understanding natural language. Cog-
Szegedy, C. 2020. A promising path towards autoformaliza-        nitive Psychology 3(1):1–191.
tion and general artificial intelligence. In Intelligent Com-    Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M.; Staats, C.; Jam-
puter Mathematics: 13th International Conference, CICM           nik, M.; and Szegedy, C. 2022. Autoformalization with
2020, Bertinoro, Italy, July 26–31, 2020, Proceedings 13,        Large Language Models. Advances in Neural Information
3–20. Springer.                                                  Processing Systems 35:32353–32368.
Tang, Y.; da Costa, A. A. B.; Zhang, X.; Irvine, P.; Khastgir,   Xie, Y.; Yu, C.; Zhu, T.; Bai, J.; Gong, Z.; and Soh, H.
S.; and Jennings, P. A. 2023. Domain knowledge distillation      2023. Translating Natural Language to Planning Goals with
from large language model: An empirical study in the au-         Large-Language Models.
tonomous driving domain. In 26th IEEE International Con-         Xu, Y.; Feng, J.; and Miao, W. 2024. Learning from
ference on Intelligent Transportation Systems, ITSC 2023,        Failures: Translation of Natural Language Requirements
Bilbao, Spain, September 24-28, 2023, 3893–3900. IEEE.           into Linear Temporal Logic with Large Language Models.
Tarrach, G.; Jiang, A. Q.; Raggi, D.; Li, W.; and Jamnik,        In 2024 IEEE 24th International Conference on Software
M. 2024. More details, please: Improving autoformalization       Quality, Reliability and Security (QRS), 204–215. ISSN:
with more detailed proofs. In AI for Math Workshop@ ICML         2693-9177.
2024.                                                            Yang, K.; Poesia, G.; He, J.; Li, W.; Lauter, K.; Chaudhuri,
Thatikonda, R. K.; Han, J.; Buntine, W.; and Shareghi, E.        S.; and Song, D. 2024. Formal mathematical reasoning: A
2024. Strategies for Improving NL-to-FOL Translation with        new frontier in ai. arXiv preprint arXiv:2412.16075.
LLMs: Data Generation, Incremental Fine-Tuning, and Ver-         Yang, Z.; Ishay, A.; and Lee, J. 2023. Coupling Large
ification.                                                       Language Models with Logic Programming for Robust and
Wang, Q.; Brown, C.; Kaliszyk, C.; and Urban, J. 2020. Ex-       General Reasoning from Text.
ploration of neural machine translation in autoformalization     Ying, H.; Wu, Z.; Geng, Y.; Wang, J.; Lin, D.; and Chen,
of mathematics in mizar. In Proceedings of the 9th ACM           K. 2024. Lean Workbook: A large-scale Lean problem set
SIGPLAN International Conference on Certified Programs           formalized from natural language math problems.
and Proofs, 85–98.
                                                                 Yu, Z.; Peng, R.; Ding, K.; Li, Y.; Peng, Z.; Liu, M.; Zhang,
Wang, H.; Unsal, M.; Lin, X.; Baksys, M.; Liu, J.; San-          Y.; Yuan, Z.; Xin, H.; Huang, W.; Wen, Y.; Zhang, G.; and
tos, M. D.; Sung, F.; Vinyes, M.; Ying, Z.; Zhu, Z.; et al.      Liu, W. 2025. Formalmath: Benchmarking formal mathe-
2025a. Kimina-prover preview: Towards large formal rea-          matical reasoning of large language models.
soning models with reinforcement learning. arXiv preprint
arXiv:2504.11354.                                                Zhang, L.; Quan, X.; and Freitas, A. 2024. Consistent aut-
                                                                 oformalization for constructing mathematical libraries. In
Wang, J.; Sundarsingh, D. S.; Deshmukh, J. V.; and Kan-          Proceedings of the 2024 Conference on Empirical Methods
taros, Y. 2025b. ConformalNL2LTL: Translating Natural            in Natural Language Processing (EMNLP).
Language Instructions into Temporal Logic Formulas with
                                                                 Zhang, L.; Valentino, M.; and Freitas, A. 2025. Formalizing
Conformal Correctness Guarantees. arXiv:2504.21022.
                                                                 Complex Mathematical Statements with LLMs: A Study on
Wang, R.; Li, Y.; Fung, Y. R. M.; and Zhang, T. 2025c. Let’s     Mathematical Definitions.
reason formally: Natural-formal hybrid reasoning enhances
                                                                 Zhou, J. P.; Staats, C.; Li, W.; Szegedy, C.; Weinberger,
llm’s math capability. arXiv preprint arXiv:2505.23703.
                                                                 K. Q.; and Wu, Y. 2024. Don’t Trust: Verify – Grounding
Wang, Q.; Kaliszyk, C.; and Urban, J. 2018. First experi-        LLM Quantitative Reasoning with Autoformalization.
ments with neural translation of informal to formal mathe-
matics. In Intelligent Computer Mathematics: 11th Interna-
tional Conference, CICM 2018, Hagenberg, Austria, August
13-17, 2018, Proceedings 11, 255–270. Springer.
