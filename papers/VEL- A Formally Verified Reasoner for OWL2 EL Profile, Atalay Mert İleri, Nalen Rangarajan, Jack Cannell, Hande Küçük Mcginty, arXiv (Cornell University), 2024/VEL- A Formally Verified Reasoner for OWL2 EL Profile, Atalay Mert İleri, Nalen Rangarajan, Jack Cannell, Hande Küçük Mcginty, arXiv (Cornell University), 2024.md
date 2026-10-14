                                                              VEL: A Formally Verified Reasoner for OWL2 EL Profile

                                                            Atalay Mert Ileri1 , Nalen Rangarajan1 , Jack Cannell1 , Hande McGinty1
                                                                                               1
                                                                                          Kansas State University, USA
                                                                  atalay@ksu.edu, nalenrangarajan@ksu.edu, jdcannell@ksu.edu, hande@ksu.edu
arXiv:2412.08739v1 [cs.LO] 11 Dec 2024




                                                                     Abstract                                 software bugs that undermine their correctness. A recent
                                                                                                              competition for reasoners showed that some of the widely
                                           Over the past two decades, the Web Ontology Language
                                           (OWL) has been instrumental in advancing the development
                                                                                                              used reasoners contain bugs since the results of the differ-
                                           of ontologies and knowledge graphs, providing a structured         ent reasoners didn’t agree on the same queries. (Parsia et al.
                                           framework that enhances the semantic integration of data.          2017) The ground truth needed to be determined by the ma-
                                           However, the reliability of deductive reasoning within these       jority vote. Reasoners’ inability to agree on a correct re-
                                           systems remains challenging, as evidenced by inconsisten-          sult shows that testing-based methodologies cannot provide
                                           cies among popular reasoners in recent competitions. This          strong correctness guarantees required for critical domains
                                           evidence underscores the limitations of current testing-based      such as healthcare.
                                           methodologies, particularly in high-stakes domains such as            We developed VEL, a formally verified EL++reasoner
                                           healthcare. To mitigate these issues, in this paper, we have de-   with machine-checkable correctness proofs to address this
                                           veloped VEL, a formally verified EL++reasoner equipped
                                                                                                              gap. Our proofs ensure the correctness of the output for each
                                           with machine-checkable correctness proofs that ensure the
                                           validity of outputs across all possible inputs. This formal-       possible input. We based our formalization on Baader et
                                           ization, based on Baader et al.’s algorithm (Baader, Brandt,       al.’s algorithm. (Baader, Brandt, and Lutz 2005) During our
                                           and Lutz 2005), has been transformed into executable OCaml         mechanization, we discovered two errors in the published
                                           code using the Coq proof assistant’s extraction capabilities.      correctness proof that required changes to the algorithm. We
                                           Our formalization revealed several errors in the original com-     obtained the executable code through the extraction func-
                                           pleteness proofs, which led to changes to the algorithm to         tionality of the Coq proof assistant (The Coq Development
                                           ensure its completeness. Our work demonstrates the neces-          Team 2024).
                                           sity of mechanization of reasoning algorithms to ensure their
                                           correctness at theoretical and implementation levels.              Contributions     This paper has the following contributions:
                                                                                                               • Mechanized formalization of EL++description logic.
                                                                 Introduction                                  • A modified subsumption checking algorithm that is prov-
                                         During the nearly three decades since its initial proposal,             ably correct.
                                         Semantic Web(SW) has become a mature technology, which                • An implementation of a subsumption checker with string
                                         can support and enhance existing applications in several sce-           and rational number concrete domains for EL++with a
                                         narios, ranging from e-commerce (Necula et al. 2018) to                 mechanized proof of correctness.
                                         Human-Device interaction (Perera 2020), and product con-
                                                                                                               • An executable OCaml code extracted from the verified
                                         figuration (Bischof et al. 2018), just to name a few. The fun-
                                                                                                                 implementation.
                                         damental concept of the Semantic Web is to provide a se-
                                         mantic layer for data, enabling systems to manipulate this
                                         data through chains of meaningful deduction steps based on                                Related Work
                                         sound rules. This semantic framework allows SW data pro-             In response to community feedback and the evolving needs
                                         cessing to offer meaningful explanations, which contrasts            of ontology developers, OWL2 was released as a W3C rec-
                                         with the often opaque nature of sub-symbolic technologies            ommendation in 2009. Apart from addressing acute prob-
                                         like neural networks. However, a closer examination of SW            lems with expressivity, a goal in the development of OWL2
                                         systems reveals that the sophistication of their reasoning           was to provide a robust platform for future development.
                                         abilities can vary significantly (Colucci, Donini, and Di Sci-       OWL2 extends the W3C OWL Web Ontology Language
                                         ascio 2024). Furthermore, due to the increased popularity of         with a small but useful set of features that have been re-
                                         Neurosymbolic AI in recent years (Hitzler et al. 2022), there        quested by users, for which effective reasoning algorithms
                                         is a renewed interest in deductive reasoning algorithms.             can be built, and those OWL tool developers are willing to
                                            Due to their important role, it is necessary to ensure that       support. Considerable progress has been achieved in the de-
                                         the reasoner results are correct. However, like any other soft-      velopment of tool support for OWL2. The new syntax is
                                         ware system, reasoner implementations are susceptible to             currently supported by the new version of the OWL API.
The widely used Protégé (Musen 2015) system has been ex-       are formalized in proof assistants for metatheoretical stud-
tended with support for the additional constructs provided       ies. Additionally, formalizations of more specialized log-
by OWL2 and most recently gaining community support              ics such as separation logic (Jung et al. 2018), match-
from volunteer groups such as OBO Foundry Ontologies             ing logic (Bereczky et al. 2022), alternating-time temporal
(Smith et al. 2007).                                             logic (Zanarini, Luna, and Sierra 2012), linear logic (Xavier
   The standardization of OWL has sparked the develop-           et al. 2018), and ALC description logic (Hidalgo-Doblado
ment and adaption of a number of reasoners, including            et al. 2014) serve as tools for verifying software. Our work
FacT++ (Tsarkov and Horrocks 2006), Pellet (Sirin et al.         adds EL++description logic to this growing body of work.
2007), and HermiT (Glimm et al. 2014), and ontology edi-
tors, including Protégé (Musen 2015). However, mostly due      Verified Reasoning Baader et al. use automated theorem
to funding reasons and research interest shifting towards AI,    proving to certify the results of the ELK reasoner for OWL2
the research for better reasoners was abandoned (McGinty         EL (Baader, Koopmann, and Tinelli 2020). They imple-
2018) despite the fact that recent work showed that more re-     mented an algorithm that extracts a proof certificate from
search is necessary for correct implementations (Parsia et al.   an ELK result and checks its correctness using LFSC proof
2017).                                                           checker. This approach incurs time and memory overheads
                                                                 due to certificate generation and proof checking at run-
OWL Reasoners Over the past three decades, a num-                time and lacks support for required extensions such as con-
ber of RDF and OWL reasoners were implemented which              crete domains. In contrast, VEL does not incur any proof-
are reviewed in various articles, most notably by Mishra et      checking overhead since the correctness proofs of our im-
al. (Mishra and Kumar 2011) and Colucci et al. (Colucci,         plementations are statically checked. Eliminating this over-
Donini, and Di Sciascio 2024). However, for our purposes,        head will make our reasoners more scalable compared to
we will list a few notable reasoners that have been dominat-     validation-based approaches. VEL also supports required
ing the field for the past two decades (McGinty 2018).           extensions for wider applicability.
                                                                    Hidalgo-Doblado et al. formalized ALC description logic
 • ELK: ELK (Kazakov, Krötzsch, and Simancik 2012)              and implemented a formally verified tableau-based reasoner
   is described as a high-performance reasoner for OWL           in PVS. (Hidalgo-Doblado et al. 2014) Although it is a well-
   EL ontologies. Unlike conventional tableau-based pro-         known description logic, ALC does not correspond to any
   cedures, which test unknown subsumptions by trying to         OWL2 profile and lacks the support for datatypes and other
   construct counter-models, the EL procedures derive new        extensions. These limitations restrict the usability of their
   subsumptions explicitly using inference rules.                implementation in applications. OWL2 guides VEL’s devel-
 • FACT++ : FaCT++ (Tsarkov and Horrocks 2006) im-               opment, and VEL supports necessary logic extensions to en-
   plements a tableaux decision procedure for the well-          sure’ widespread usage of our implementations.
   known SHOIQ description logic, with additional sup-
   port for datatypes, including strings and integers. The                      Formalization of EL++
   system employs a wide range of performance-enhancing
   optimizations, including standard techniques (absorption      The first step in implementing a verified reasoner is formal-
   and model merging) and newly developed ones (ordering         izing the logic it will operate on. We decided to keep our
   heuristics and taxonomic classification).                     formalization as generic as possible to facilitate its use in
                                                                 other contexts. In this section, we will explain each part of
 • HermiT: HermiT (Glimm et al. 2014) is the first               our formalization.
   publicly-available OWL reasoner based on a novel hy-
   pertableau calculus, which provides much more efficient       Primitives
   reasoning than any previously known algorithm.
                                                                 We parameterized our formalization over primitives such as
 • Pellet: Pellet (Sirin et al. 2007) is the first sound and     names and concrete domain elements. We defined the names
   complete OWL-DL reasoner with extensive support for           as decidable infinite types. A decidable infinite type has two
   reasoning with individuals (including nominal support         components: a decision procedure for checking the equality
   and conjunctive query), user-defined datatypes, and de-       of two terms and a function that takes a list of terms and
   bugging support for ontologies.                               returns a term that is not in the list. Such parametrization
 • Konclude: Konclude (Steigmiller, Liebig, and Glimm            allows using different types without changing the core im-
   2014) is a high-performance reasoner for the Description      plementation. As a result, our formalization is easier to inte-
   Logic SROIQV. The supported ontology language is              grate in different applications.
   a superset of the logic underlying OWL 2 extended by
   nominal schemas, which allows for expressing arbitrary        Concrete Domains Our formalization models each do-
   DL-safe rules.                                                main as a record with four definitions and three proofs. Our
                                                                 definitions include the domain, which is a non-empty set of
Mechanized Formal Logic A diverse selection of                   concrete domain elements, a set of predicate names with a
general-purpose logics such as propositional logic (Guo          decidable membership, the arities of each predicate as a par-
and Yu 2023), first-order predicate logic (Herbelin, Kim,        tial function from predicate names to natural numbers, and
and Lee 2017), quantified modal logic (de Almeida Borges         an application function that determines the result of a predi-
2022), and logic of bunched implications (Frumin 2022)           cate application to a list of concrete domain elements
    Three required proofs are the specifications for arity def-
initions and the application function. The first one requires
that arities are defined only for the predicates of the concrete
domain. The second one provides a specification for the ap-
plication function regarding input value validity. It states that
if the function returns true for some predicate and list of con-
crete domain elements, then the predicate should belong to
that concrete domain, each element should be in the domain
of that concrete domain, and the number of elements should
match the arity of the predicate.
    During our formalization, we discovered that predicate                          Figure 1: Structure of VEL
names of different domains should also be distinct, which
wasn’t required in the original paper. This necessity arises
because rule CR9 in classification needs to decide that                                 Implementation
two predicate names belong to different domains (Baader,
                                                                    Our implementation of the reasoner consists of four parts:
Brandt, and Lutz 2005). However, this is not a limitation in
                                                                    transformation, normalization, A-extension, and classifica-
practice because shared names between domains can be re-
                                                                    tion. Transformation changes the problem from checking
placed to ensure disjointness.
                                                                    the subsumption of arbitrary concept descriptions to check-
    Some rules in the classification algorithm require check-
                                                                    ing the subsumption of two concept names. Normalization
ing the satisfiability of a conjunction of predicate expres-
                                                                    breaks down complex constraints into simpler ones to make
sions or the implication between predicate expressions, in-
                                                                    subsumption checking tractable. A-extension adds an axiom
terpreted as a first-order formula. To be able to ensure the
                                                                    that ensures the completeness of the reasoner. Finally, clas-
correctness of satisfiability and implication checker imple-
                                                                    sification computes concept inclusions from the constraints.
mentations, we defined an evaluation function that takes a
                                                                    On top of our reasoner implementation, we implemented
first-order sentence composed of predicate expressions and
                                                                    two concrete domains: rational numbers and strings. Project
an assignment to feature names and returns a boolean that
                                                                    structure can be seen in Figure 1. Rounded rectangles rep-
represents if the given sentence is satisfiable under the given
                                                                    resent our components implemented in the proof assistant,
assignment. Then, we defined the satisfiability and impli-
                                                                    hexagons represent the proof assistant’s functionalities, and
cation checker specifications in terms of the results of the
                                                                    normal rectangles represent runnable code.
evaluations. We decided to use dependent typing to ensure
the implementation of the functions to satisfy their specifi-       Transformation
cation.
                                                                    The first step of checking subsumption C ⊑C D is trans-
Language We defined the language as an inductive type               forming the knowledge base to add A ⊑ C and D ⊑
where each constructor corresponds to an EL++concept                B where A and B are fresh concept names, as described
description constructor. We also defined a well-formedness          in Baader et. al. This transformation changes the problem
predicate for concrete domain descriptions to ensure that           from subsumption checking of arbitrary concept descrip-
predicate names belong to one of the concrete domains and           tions to subsumption checking of basic concepts while pre-
the number of feature names passed to the predicate matches         serving the subsumption relationship. It returns the trans-
its arity. Unlike other restrictions, we decided to define this     formed knowledge base and the newly generated names to
as a predicate instead of using dependent typing to keep the        be used in A-extension and final subsumption checking.
equality of concept descriptions decidable.
   On top of concept descriptions, we defined constraints and       Normalization
knowledge bases. Our knowledge bases consist of lists of            We implemented the normalization in two steps, as pre-
names that can be used, a CBox, and the proof that the only         sented in the paper. Both steps follow a similar pattern where
names appearing in the CBox are the ones in the lists.              each rule is repeatedly applied until none of the rules can be
                                                                    applied anymore. Again, we used dependent typing to en-
Semantics We formalized the provided model-theoretic
                                                                    sure the normalization implementation satisfies its specifi-
semantics for EL++. We first defined what we call “a base
                                                                    cations.
interpretation”. A base interpretation maps each name to its
corresponding structure in the model, namely, each individ-         Formalization of the Rules We formalized each rule in
ual name to an individual in the domain, each concept name          two parts: the condition and the application. Such separa-
to a set of individuals, each role name to a pair of individ-       tion allowed us to use a higher-order selection function that
uals, and each feature name to a partial function from indi-        removes and returns an eligible constraint given a rule con-
viduals to concrete domain elements.                                dition or tells us no such constraint exists. Then, the chosen
   Then, we defined the interpretation function that recur-         constraint is passed into the application function, which cre-
sively constructs the interpretation of a concept description       ates the new constraints and adds them to the CBox.
for a given base interpretation. Finally, we defined the no-           This modular implementation allowed us to encapsulate
tions of model and subsumption as described in Baader et.           each rule’s effect on the CBox and prove the necessary the-
al. .                                                               orems more easily, making the process tractable.
Listing 1: A part of the measure for NF3 rule.                   of C A+ . Conversely, every model of C A+ is a model of C.
Fixpoint count_NF3_CD(C) :=                                      Therefore, the following theorem holds:
match C with                                                     Theorem 1 ∀ C, B ∈ NC .A ⊑C B ↔ A ⊑C A+ B
| X ⊓Y ⇒
     count_NF3_CD(X) + count_NF3_CD(Y )
| ∃R.X ⇒                                                         Classification
     if X ∈ BC then 0                                            We followed a similar methodology to normalization by
     else count_NF3_CD(X) + 3                                    splitting rules into conditions and applications and then us-
| _ ⇒0                                                           ing a higher-level function to find candidates. This allowed
end.                                                             us to use the same proof patterns we used in normalization.
                                                                 Reachability A crucial operation for classification is
Termination Measure We implement each normalization              reachability. Reachability states that a sequence of concept
part as a recursive function that finds candidates and ap-       descriptions exists in which each consecutive pair is re-
plies the corresponding rules. Defining a recursive function     lated by a role between two concept descriptions. We imple-
in Coq requires proving that it will terminate for all inputs.   mented reachability as a depth-first search that starts from
One way to do that is by providing a measure and proving         the end and constructs the path until it reaches the begin-
that it decreases after each recursive call. We defined a mea-   ning. To verify it, we defined a predicate that implements
sure based on the number of rule applications left. How-         the rules in the paper, then dependently typed the function
ever, naive counting wasn’t enough to give us a decreas-         so it returns true if and only if the predicate holds.
ing measure since applying a rule could create new candi-        Classification Data Structure Our implementation of
dates for application. To circumvent that problem, we used       classification defines the two components, namely S and R,
a weighted count where applying a rule that can create new       as functions from concept descriptions to a list of concept
candidates decreases the measure more than the new candi-        descriptions and a list of pairs of concept descriptions, re-
dates increase. Listing 1 illustrates the part of the measure    spectively. This definition simplifies the proof scripts but in-
function for NF3 rule that counts nested ∃R.C structures in      curs a large run-time overhead. The overhead stems from the
a concept description.                                           fact that each update adds a conditional at the top level of the
Modified NF2 We had to make one modification regard-             function. Therefore, every lookup must traverse thousands
ing NF2 rule to the normalization routine to ensure that         of nested conditionals to compute the function. Replacement
our measure decreases after every iteration. Measure for         of classification implementation with a more efficient data
NF2 counts the number of ⊓’s that connect at least one           structure left as future work.
complex concept description inside each constraint’s left-       Termination Measure For all the rules except CR6, we
hand side. This measure doesn’t decrease when NF2 is ap-         defined our measure as the number of rule applications left.
plied to a constraint C ⊓ D ⊑ E where both C and D               For CR6, we measured the ”distance until full S” for each
are complex concept descriptions. The resulting two con-         concept description in BC. This measure relies on the fact
straints A ⊓ D ⊑ E, C ⊑ A have the same total count with         that for any concept description C ∈ BC, S(C) is a subset
C ⊓ D ⊑ E. However, if we immediately apply NF2 again            of BC ∪ {⊥}. Since BC ∪ {⊥} is finite and the contents of
to A ⊓ D ⊑ E, we get A ⊓ B ⊑ E, D ⊑ B, C ⊑ A,                    S are monotonically increasing, it gives us a proper mea-
which has one less number of applications since both A and       sure. Unlike normalization, each rule application reduced
B are simple concept descriptions. So, we circumvented this      the measure, so we didn’t need to change the rules.
problem by replacing NF2 with a new rule that applies NF2
twice when both concept descriptions are complex.                Subsumption Checking
A-extension                                                      Our subsumption checker function ties individual steps to-
                                                                 gether and then checks the two conditions described in
We added a preprocessing step to address the original com-       Baader et. al. Listing 2 displays the final subsumption check-
pleteness proof error. We call this step A-extension of the      ing algorithm between two concept descriptions.
knowledge base. Given a concept name A, A-extension of a
CBox C is defined as                                             String and Rational Number Domains
                                                                 We implemented rational number and string domains de-
                C A+ := C ∪ {{t} ⊑ ∃rt .A}
                                                                 scribed in Baader et. al. for our runnable code. In our im-
   where t and rt are fresh individual and role names, re-       plementation, we took advantage of the flexibility of rep-
spectively. A-extension of a CBox ensures that in every C A+     resenting names in our formalism to reduce the complexity
model, AI is nonempty. Nonemptiness plays a crucial role         of processing the predicate names with built-in arguments,
in the completeness proof, which will be explained in a fu-      such as “equals to 1”. Instead of using strings as predicate
ture section.                                                    names, we defined a type that carries those built-in argu-
   We also proved that A-extension preserves subsumption         ments in them. Using a custom type allowed us to eliminate
with respect to A. This is due to the fact that each model of    all the manipulation that may be required if strings or other
C where AI is nonempty can be extended to obtain a model         less expressive types are used.
Listing 2: Subsumption checking algorithm.                         Listing 3: Definition of a role tree.
check_subsumption(C, C, D) :=                                      Inductive role_tree :=
  (C t , A, B) := transform_kb(C, C, D)                            | ExistsR (r, C, D)
  C n := normalize(C t )                                           | T ransR (r, C, D, r1 , t)
                                                                   | SplitR (r, C, D, r1 , r2 , E, t1 , t2 )
  C A+ := A_extension(C n , A)
  cl := classify(C A+ )
  if B ∈ cl.S(A) or ⊥ ∈ cl.S(A):                                   Listing 4: Proposition construction function.
      return true                                                  Fixpoint tree_to_invariant tree :=
  for i ∈ C A+ .NI :                                               match tree with
      if ⊥ ∈ cl.S({i}):                                            | ExistsR (r, C, D) ⇒
          return true                                                  ∃ C ′ , C ′ ∈ S(C) ∧ C ′ ⊑ ∃r.D ∈ C
  return false
                                                                   | T ransR (r, C, D, r1 , t) ⇒
                                                                        tree_to_invariant (t) ∧
   The original paper (Baader, Brandt, and Lutz 2005) sug-              (C, D) ∈ R(r1 ) ∧ r1 ⊑ r ∈ C
gests a satisfiability algorithm for each concrete domain they
                                                                   | SplitR (r, C, D, r1 , r2 , E, t1 , t2 ) ⇒
present. The algorithm for rational numbers is described in            E ∈ BC ∧
(Lutz 2002) and constructs a linear program that has a solu-           tree_to_invariant (t1 ) ∧
tion if and only if the predicate expression is satisfiable. The       tree_to_invariant (t2 ) ∧
algorithm for strings is described in (Lutz 2004) and uses             (C, E) ∈ R(r1 ) ∧ (E, D) ∈ R(r2 ) ∧
directed graphs and a specifically designed subroutine to de-          r1 ◦ r2 ⊑ r ∈ C
cide the satisfiability. Due to the high complexity of each        end.
algorithm, we decided to implement them as an unverified
OCaml program that is being called from our verified im-
plementation. We used the OCaml LP library that interfaces         only some rule applications, which requires us to do induc-
with GNU Linear Programming Kit (GLPK) (Free Soft-                 tive proof over groups of rule applications instead of each
ware Foundation 2024) rational number satisfiability and the       application. This is not an easily mechanizable proof strat-
OCamlgraph library to implement directed graph function-           egy. To mechanize the proof, we defined an invariant that
ality.                                                             implies the desired property for the final classification but is
                                                                   also preserved during each recursive call.
                  Proving Correctness                                 To define the invariant, we first defined a role tree, an in-
As presented in the original paper (Baader, Brandt, and Lutz       ductive structure that holds the information on how a pair of
2005), we split the correctness of the algorithm into sound-       concept descriptions can be included in the classification of
ness and completeness. To ensure end-to-end correctness,           a role. Listing 3 displays its formal definition.
we tied all the proofs together at the end to obtain the fol-         Our role tree has three constructors: one for each rule that
lowing succinct specification:                                     extends the R component of a classification.
                                                                     • ExistsR corresponds to the addition by CR3 and forms
Theorem 2 Correctness                                                  the leaf nodes.
∀ C, C, D.
check subsumption (C, C, D) = true ↔ C ⊑C D.                         • T ransR corresponds to the addition by CR10 where t is
                                                                       the tree that contains the information on how (C, D) can
Soundness                                                              be included in R(r1 ).
                                                                     • SplitR corresponds to the addition by CR11 where t1
Our soundness proof followed a similar structure to Baader
                                                                       and t2 are the trees that contain the information on how
et. al. ’s pen-and-paper proofs. Required properties were
                                                                       (C, E) and (E, D) can be included in R(r1 ) and R(r2 ),
invariant under each rule application, therefore we only
                                                                       respectively.
needed to prove their invariance. The rest of the soundness
proof mechanized smoothly.                                            Even though role trees contained possible historical in-
                                                                   formation, they didn’t include what having that history en-
Completeness                                                       tails. To establish this connection, We defined a function that
Completeness proof was more challenging to mechanize               constructs a proposition from a tree given a knowledge base
than soundness proof. It required us to define a new in-           and a classification. Function recursively traverses a given
variant, fix errors in the original proof, and employ non-         tree and returns the proposition that asserts that conditions
constructive reasoning. We will explain our new invariant          of corresponding rules hold. Listing 4 shows its definition.
and the errors in the original proof below.                           Finally, we defined a predicate that asserts the root of
                                                                   a tree corresponds to a given (r, C, D) tuple. Given these
Role Trees Point 2 of Claim 1 in the original complete-            three definitions, our invariant states that for all concept de-
ness proof involved a property that holds for the final clas-      scriptions C and D, and role name r, if (C, D) is in R(r),
sification but doesn’t necessarily hold in every intermedi-        then there exists a role tree such that, its root corresponds to
ate step. The proof in the original paper uses induction over      (r, C, D) and the derived proposition holds.
Knowledge base                                                     sumed that they could prove the completeness by reasoning
NC = {X, A, B} NR = {r1 } NI = {b, c}                              about the models where AI is nonempty since subsumption
C = {X ⊑ {b}, X ⊑ {c}, A ⊑ ∃r1 .X}                                 holds trivially in the models where AI is empty. They used
Classification result                                              this assumption to prove that
S(X) = {⊤, X, {b}, {c}} S(A) = {⊤, A}
S({b}) = {⊤, {b}} S({c}) = {⊤, {c}}                                         ∀ C, D ∈ BC− . C ∼ D → S(C) = S(D)
R(r1 ) = {(A, X)}                                                     which doesn’t hold if a model exists where AI is empty.
                                                                   Since classifications and models are “living in separate lev-
    Figure 2: Example CBox where ∼ is not transitive.
                                                                   els,” the statement cannot be qualified to hold only under the
                                                                   nonempty models, which makes the statement false.
                                                                      We fixed this error by introducing A-extensions that en-
   Role trees allowed us to mimic doing induction over se-
                                                                   force nonemptiness on the classification level. The models
lected rule applications by doing induction over the trees.
                                                                   of an A-extension of a CBox are precisely the ones where
Although we didn’t need to use this technique again, we be-
                                                                   AI is nonempty. By restricting the models to nonempty
lieve it is a strong technique to tackle proofs about properties
                                                                   ones, we recovered the transitivity of the relation, which
that can be broken temporarily.
                                                                   fixed the major flaw in the proof of completeness. The ques-
Errors in Completeness Proofs                                      tion of whether the original algorithm is complete remains
                                                                   open.
Our mechanization revealed two major errors in pen-
and-paper completeness proofs. The first one is the non-           Under-specification We identified another error in the
transitivity of a relation assumed to be transitive. The second    statement of a lemma, originally called Claim 2, used in
one is the under-specification of a solution for concrete do-      constructing a counterexample model. Lemma stated that for
main predicates. We explain each problem and our solutions         each concrete domain dm and an equivalence class [C] with
below.                                                             respect to ∼, there exists a solution δ([C], dm) that only
                                                                   satisfies the predicate tuples in S(C). Below is the original
Non-transitivity Completeness proofs in Baader et. al.             lemma from Baader et. al.
heavily rely on a relation we call BC− -equivalence, denoted
by ∼.                                                                 Claim 2. For each C ∈ BC− and each concrete domain
   The relation is defined over the set BC− , which is the set     dm, we can find a solution δ([C], dm) for condm (S(C))
of all concept descriptions in BC that are reachable from          such that, for all concepts D ∈ BC of the form
A. The relation C ∼ D for concept descriptions C, D ∈              p(f1 , · · · , fk ) with p ∈ P dm , we have δ([C], dm) |= D
BC− is defined as either C is equal to D, or there exists          iff D ∈ S(C), where condm (S(C)) denotes the conjunction
an individual name a such that {a} ∈ S(C) ∩ S(D). Their            of all the predicates in S(C) that belongs to dm. 1
formal definitions are as follows:
                                                                      This solution defines the interpretation of feature names in
  BC− = {C ∈ BC | A ⇝ C}                                           the counterexample. The behavior of solutions from Claim
  ∼ = {(C, D) | C = D ∨ ∃ a. {a} ∈ S(C) ∩ S(D)}                    2 is only restricted in terms of the domain they are being se-
                                                                   lected for. Therefore, they may satisfy some predicate tuples
   During our formalization, we discovered that ∼ is not an        not in S(C) from other domains. However, proof of Claim 3
equivalence relation because it wasn’t transitive. Since the       relies on the fact that this solution doesn’t satisfy any other
rest of the proof relied on it being an equivalence in multi-      predicate not in S(C), regardless of whether the predicate
ple places, the completeness proof in the paper wasn’t cor-        belongs to the chosen domain.
rect. Figure 2 shows an example where transitivity doesn’t            We fixed this error by reordering the quantification and
hold. The example contains a transformed and normalized            further restricting the behavior of the solution. The definition
CBox for ∃r1 .X ⊑C ⊥ query. In the example, X, {b}, {c} ∈          of our lemma is
BC− , {b} ∼ X, and X ∼ {c} but it is not true that
{b} ∼ {c}. Therefore, ∼ is not transitive under the old algo-      Lemma 3 Solution existence
rithm. It is also important to point out that the example does     ∃ δ. ∀ C ∈ BC− , dm, p ∈ P dm , f1 , · · · , fn .
not demonstrate that the old algorithm is incomplete.                (δ([C]) |= p(f1 , · · · , fn ) ↔ p(f1 , · · · , fn ) ∈ S(C)) ∧
   Transitivity of the relation relies on the following two          (∀ f. (∃ e. δ([C], f ) = e) ↔
properties:                                                             ∃ dm, p ∈ P dm , f1 , · · · , fn .
                                                                        p(f1 , · · · , fn ) ∈ S(C) ∧ f ∈ (f1 , · · · , fn ))
1. For all models I of CBox C and individuals i and concept
   descriptions C and D, if i is in C I and D is in S(C), then        Our lemma states that there exists a function δ from ∼-
   i is in DI .                                                    equivalence classes to solutions, i.e., partial functions from
2. For all models I of CBox C and concept descriptions             feature names to concrete domain elements, such that, for
   C and D, if C ⇝ D and C I is nonempty, then DI is               all concept descriptions C in BC− , all concrete domains
   nonempty.                                                          1
                                                                        We modified the notation to make it consistent with our nota-
  The problem stemmed from the fact that in some models            tion. Also, the original statement contained δ([C], t) |= D for an
of C, AI can be empty. We believe authors implicitly as-           unknown variable t, which we believe is a typo.
and all predicate expressions, δ([C]) validates the expres-              # of constraints       20      30      40
sion if and only if it is in S(C). Lemma also restricts the             Concept Inclusions      4s     278s    192s
feature names with elements assigned to them to the ones                 Role Inclusions       463s     6s     2732s
that appear in S(C). These two combined are strong enough
to prove Claim 3.                                                  Our results show a very high variance between different
                                                                tests, indicating that, as expected, the structure of a knowl-
                                                                edge base has more impact than its size when it comes to
                       Extraction                               reasoner performance.
We used Coq’s extraction procedure to obtain a runnable
OCaml code. We extracted certain Coq types to native                    Conclusion and Future Directions
OCaml types for better run-time performance. More pre-
cisely, we extracted natural numbers and integers to Ocaml      The Semantic Web, over the past three decades, helped en-
int type, rational numbers to zarith library’s Q type, and      hance a wide range of applications. Its core principle of
strings to native Ocaml string type. This choice intro-         providing a semantic layer for data allows for meaning-
duces possible unsoundness to the runnable code due to          ful deductions and explanations, setting it apart from sub-
possible integer overflows since original Coq types are un-     symbolic technologies like neural networks. However, the
bounded and cannot overflow. We believe that this is a rea-     varying sophistication of SW systems’ reasoning abilities
sonable tradeoff since 64-bit integers are very unlikely to     highlights the need for reliable reasoning algorithms, par-
overflow in practice. Using Coq’s default extraction settings   ticularly in the context of the growing interest in Neurosym-
to obtain slower but non-overflowing implementation is still    bolic AI and Generative AI approaches that seek to utilize
possible. We obtained the custom extraction code for these      Semantic Web layers. The critical importance of ensuring
types from mlvoqc library. (Hietala et al. 2021)                the correctness of reasoner results cannot be overstated, es-
                                                                pecially as AI systems are increasingly used in sensitive and
Trusted Computing Base                                          high-stakes domains.
                                                                   In an attempt to address this gap, our work lays the foun-
Our trusted computing base consists of Coq Proof Assis-
                                                                dation for formally verified reasoners for Neurosymbolic AI
tant, OCaml run-time and libraries, GLPK linear program
                                                                applications. We believe that, in the cases of high-stakes ap-
solver, and our implementations of satisfiability and impli-
                                                                plication domains, such as health, finance, and security, the
cation checkers for concrete domains.
                                                                benefit of increased trustworthiness outweighs the increased
                                                                development effort. As AI continues to enter different and
                       Evaluation                               critical domains, ensuring the correctness of reasoning pro-
We evaluated our work in two axes. We measured the re-          cesses through formal verification might become essential in
quired proof effort by comparing the number of lines of         preventing errors and fostering trust in AI systems.
proof per line of implementation. We evaluated our ex-             As for future directions, one immediate step would be in-
tracted artifact for runtime performance on randomly gen-       corporating domain and range restriction into EL++to in-
erated knowledge bases of various sizes.                        crease its expressive power. This integration is theoretically
                                                                described in (Baader, Brandt, and Lutz 2008). To implement
Proof Effort                                                    the increase in expressive power, we would be required to
We measured proof effort by lines of code and the number        modify the language and add new functionality to eliminate
of definitions and theorems. Our 165 definitions consist of     domain and range restrictions. In relation to this approach,
1511 cloc. Our 387 theorems consist of 16977 cloc, giving       we might work towards implementing reasoners for other
us 11.3x proof overhead.                                        OWL profiles since OWL EL’s expressive power is limited.
                                                                   Another future direction would be improving the imple-
Performance Evaluation                                          mentation performance. Our work faithfully replicated the
                                                                Baader et al.’s algorithm. During this process, we observed
To evaluate the performance of our implementation, we           many places where the implementation can be modified for
measured run times on randomly generated knowledge bases        better run-time performance. For example, the algorithm can
with different sizes and structures. We designed our test       traverse the knowledge base and group the constraints based
cases to measure the impact of concept and role inclusion       on which rule they may fit. This approach would eliminate
axioms separately. All knowledge bases had 20 concept           the overhead of searching for a candidate one at a time, re-
names, 10 role names, and 20 individual names. For con-         peat testing of unviable candidates, and enable parallel ap-
cept inclusion tests, we kept the number of role inclusion      plication of the rules.
axioms at 10 and the maximum length of the left side at 2.
For role inclusion tests, we set the number of concept inclu-
sions to 20 and the maximum length of the left side of role                            References
inclusions to 5. All the tests are run on AMD Ryzen 5 2.20      Baader, F.; Brandt, S.; and Lutz, C. 2005. Pushing the EL
GHz CPU with 16 GB of RAM. The following table shows            Envelope. In Proceedings of the 19th International Joint
sample numbers where each row corresponds to a constraint       Conference on Artificial Intelligence, IJCAI’05, 364–369.
type, and each column corresponds to the number of con-         San Francisco, CA, USA: Morgan Kaufmann Publishers
straints of that type.                                          Inc.
Baader, F.; Brandt, S.; and Lutz, C. 2008. Pushing the EL        Lutz, C. 2002. PSpace Reasoning with the Description
Envelope Further. In Clark, K.; and Patel-Schneider, P. F.,      Logic ALCF(D). Logic Journal of the IGPL, 10(5): 535–
eds., In Proceedings of the OWLED 2008 DC Workshop on            568.
OWL: Experiences and Directions.                                 Lutz, C. 2004. NEXP TIME-complete description logics
Baader, F.; Koopmann, P.; and Tinelli, C. 2020. First Results    with concrete domains. ACM Trans. Comput. Logic, 5(4):
on How to Certify Subsumptions Computed by the EL Rea-           669–705.
soner ELK Using the Logical Framework with Side Condi-           McGinty, H. K. 2018. KNowledge Acquisition and Rep-
tions. Description Logics.                                       resentation Methodology (KNARM) and Its Applications.
Bereczky, P.; Chen, X.; Horpácsi, D.; Mizsei, T. B.; Peña,     Ph.D. thesis, University of Miami.
L.; and Tusil, J. 2022. Mechanizing Matching Logic in            Mishra, R. B.; and Kumar, S. 2011. Semantic web reasoners
Coq. In Rusu, V., ed., Proceedings of the Sixth Working For-     and languages. Artificial Intelligence Review, 35: 339–368.
mal Methods Symposium, FROM 2022, ”Al. I. Cuza Univer-
                                                                 Musen, M. A. 2015. The protégé project: a look back and a
sity”, Iasi, Romania, 19-20 September, 2022, volume 369 of
                                                                 look forward. AI matters, 1(4): 4–12.
EPTCS, 17–36.
                                                                 Necula, S.-C.; Păvăloaia, V.-D.; Strı̂mbei, C.; and
Bischof, S.; Schenner, G.; Steyskal, S.; and Taupe, R. 2018.
                                                                 Dospinescu, O. 2018.          Enhancement of e-commerce
Integrating Semantic Web Technologies and ASP for Prod-
                                                                 websites with semantic web technologies. Sustainability,
uct Configuration. In ConfWS, 53–60.
                                                                 10(6): 1955.
Colucci, S.; Donini, F. M.; and Di Sciascio, E. 2024. A
                                                                 Parsia, B.; Matentzoglu, N.; Gonçalves, R. S.; Glimm, B.;
review of reasoning characteristics of RDF-based Semantic
                                                                 and Steigmiller, A. 2017. The OWL Reasoner Evaluation
Web systems. Wiley Interdisciplinary Reviews: Data Mining
                                                                 (ORE) 2015 Competition Report. Journal of Automated
and Knowledge Discovery, e1537.
                                                                 Reasoning, 59: 455 – 482.
de Almeida Borges, A. 2022. Towards a Coq formalization
                                                                 Perera, M. 2020. Personalised human device interaction
of a quantified modal logic. arXiv:2206.03358.
                                                                 through context aware augmented reality. In Proceedings
Free Software Foundation. 2024. GNU Linear Programming           of the 2020 International Conference on Multimodal Inter-
Kit.                                                             action, 723–727.
Frumin, D. 2022. Semantic cut elimination for the logic of       Sirin, E.; Parsia, B.; Grau, B. C.; Kalyanpur, A.; and Katz,
bunched implications, formalized in Coq. In Proceedings of       Y. 2007. Pellet: A practical owl-dl reasoner. Journal of Web
the 11th ACM SIGPLAN International Conference on Certi-          Semantics, 5(2): 51–53.
fied Programs and Proofs, CPP 2022, 291–306. New York,
                                                                 Smith, B.; Ashburner, M.; Rosse, C.; Bard, J. B. L.; Bug,
NY, USA: Association for Computing Machinery. ISBN
                                                                 W. J.; Ceusters, W.; Goldberg, L. J.; Eilbeck, K.; Ireland,
9781450391825.
                                                                 A.; Mungall, C. J.; Leontis, N. B.; Rocca-Serra, P.; Rutten-
Glimm, B.; Horrocks, I.; Motik, B.; Stoilos, G.; and Wang,       berg, A.; Sansone, S.-A.; Scheuermann, R. H.; Shah, N. H.;
Z. 2014. HermiT: an OWL 2 reasoner. Journal of automated         Whetzel, P. L.; and Lewis, S. E. 2007. The OBO Foundry:
reasoning, 53: 245–269.                                          coordinated evolution of ontologies to support biomedical
Guo, D.; and Yu, W. 2023. A Comprehensive Formalization          data integration. Nature Biotechnology, 25: 1251–1255.
of Propositional Logic in Coq: Deduction Systems, Meta-          Steigmiller, A.; Liebig, T.; and Glimm, B. 2014. Konclude:
Theorems, and Automation Tactics. Mathematics, 11(11).           system description. Journal of Web Semantics, 27: 78–85.
Herbelin, H.; Kim, S.; and Lee, G. 2017. Formalizing the         The Coq Development Team. 2024. The Coq Proof Assis-
meta-theory of first-order predicate logic. Journal of the ko-   tant, version 8.19.2.
rean Mathematical society, 54(5): 1521–1536.
                                                                 Tsarkov, D.; and Horrocks, I. 2006. FaCT++ description
Hidalgo-Doblado, M. J.; Alonso-Jiménez, J. A.; Borrego-         logic reasoner: System description. In International joint
Dı́az, J.; Martı́n-Mateos, F. J.; and Ruiz-Reina, J. L. 2014.    conference on automated reasoning, 292–297. Springer.
Formally Verified Tableau-Based Reasoners for a Descrip-
tion Logic. J. Autom. Reason., 52(3): 331–360.                   Xavier, B.; Olarte, C.; Reis, G.; and Nigam, V. 2018. Mech-
                                                                 anizing Focused Linear Logic in Coq. Electronic Notes
Hietala, K.; Rand, R.; Hung, S.-H.; Wu, X.; and Hicks, M.        in Theoretical Computer Science, 338: 219–236. The 12th
2021. A verified optimizer for Quantum circuits. Proc. ACM       Workshop on Logical and Semantic Frameworks, with Ap-
Program. Lang., 5(POPL).                                         plications (LSFA 2017).
Hitzler, P.; Eberhart, A.; Ebrahimi, M.; Sarker, M. K.; and      Zanarini, D.; Luna, C.; and Sierra, L. 2012. Alternating-
Zhou, L. 2022. Neuro-symbolic approaches in artificial in-       Time Temporal Logic in the Calculus of (Co)Inductive Con-
telligence. National Science Review, 9(6): nwac035.              structions. In Gheyi, R.; and Naumann, D., eds., Formal
Jung, R.; Krebbers, R.; Jourdan, J.-H.; Bizjak, A.; Birkedal,    Methods: Foundations and Applications, 210–225. Berlin,
L.; and Dreyer, D. 2018. Iris from the ground up: A modu-        Heidelberg: Springer Berlin Heidelberg. ISBN 978-3-642-
lar foundation for higher-order concurrent separation logic.     33296-8.
Journal of Functional Programming, 28: e20.
Kazakov, Y.; Krötzsch, M.; and Simancik, F. 2012. ELK
reasoner: architecture and evaluation. In ORE. Citeseer.
